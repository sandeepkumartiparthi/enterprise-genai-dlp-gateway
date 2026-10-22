using System.Collections.Concurrent;
using System.Security.Cryptography;
using System.Text;
using System.Text.Json;
using System.Text.RegularExpressions;
using GenAiDlpGateway.Models;
using Microsoft.Extensions.Caching.Distributed;

namespace GenAiDlpGateway.Services;

public interface ITokenVaultService
{
    Task<string> CreateOrGetTokenAsync(
        string entityType,
        string originalValue,
        string maskedPreview,
        string requestId,
        string userEmail,
        TimeSpan? ttl = null,
        bool useSyntheticSurrogate = false);

    Task<(string RestoredText, int RestoredCount)> RestoreTokensAsync(string textWithTokens);
    IReadOnlyList<EphemeralTokenEntry> GetActiveTokens();
    int PurgeExpiredTokens();
    Task FlushAllTokensAsync();
    string GenerateSyntheticShadow(string entityType, string originalValue);
}

public partial class TokenVaultService : ITokenVaultService
{
    private readonly IDistributedCache _distributedCache;
    private readonly IConfiguration _configuration;
    private readonly ILogger<TokenVaultService> _logger;
    private readonly ConcurrentDictionary<string, EphemeralTokenEntry> _activeTokens = new(StringComparer.OrdinalIgnoreCase);
    private readonly ConcurrentDictionary<string, string> _valueToTokenIndex = new(StringComparer.Ordinal);
    private readonly TimeSpan _defaultTtl;
    private readonly string _storageMode;

    [GeneratedRegex(@"\[([A-Z0-9_]+_[A-F0-9]{4,8})\]", RegexOptions.Compiled)]
    private static partial Regex TokenPlaceholderRegex();

    public TokenVaultService(
        IDistributedCache distributedCache,
        IConfiguration configuration,
        ILogger<TokenVaultService> logger)
    {
        _distributedCache = distributedCache;
        _configuration = configuration;
        _logger = logger;
        var ttlMinutes = configuration.GetValue<int>("DlpGateway:TokenTtlMinutes", 15);
        _defaultTtl = TimeSpan.FromMinutes(ttlMinutes > 0 ? ttlMinutes : 15);
        var redisConn = configuration.GetConnectionString("Redis");
        _storageMode = !string.IsNullOrWhiteSpace(redisConn) ? "Redis + In-Memory L1" : "Ephemeral In-Memory (Redis Compatible)";
    }

    public string GenerateSyntheticShadow(string entityType, string originalValue)
    {
        uint hash = (uint)Math.Abs(originalValue.GetHashCode());
        return entityType.ToUpperInvariant() switch
        {
            "PERSON" or "PERSON_NAME_IN" => (hash % 6) switch
            {
                0 => "Rohan Jenkins",
                1 => "Aarav Patel",
                2 => "Maya Sen",
                3 => "Vikram Mehta",
                4 => "Priya Nair",
                _ => "Kavita Reddy"
            },
            "PERSON_NAME_US" => (hash % 6) switch
            {
                0 => "David Vance",
                1 => "Marcus Sterling",
                2 => "Elena Rossi",
                3 => "Sarah Connor",
                4 => "Julian Hayes",
                _ => "Chloe Bennett"
            },
            "AADHAAR_IN" => $"{(5000 + (hash % 4000)):D4} {(2000 + ((hash / 7) % 7000)):D4} {(1000 + ((hash / 31) % 8000)):D4}",
            "US_SSN" => $"{(500 + (hash % 400)):D3}-{(20 + ((hash / 7) % 70)):D2}-{(1000 + ((hash / 31) % 8000)):D4}",
            "CREDIT_CARD" => $"4532-89{(hash % 89):D2}-11{((hash / 7) % 77):D2}-33{((hash / 31) % 66):D2}",
            "EMAIL_ADDRESS" => $"user-proxy{(hash % 900) + 100}@shadow-gateway.corp",
            "PHONE_NUMBER" => $"+91 91{(hash % 890) + 100} {(hash % 89000) + 10000}",
            "IBAN_CODE" => $"DE89 3704 0044 0532 {(hash % 8900) + 1000:D4} 00",
            "IPV4_ADDRESS" => $"192.0.2.{(hash % 200) + 10}",
            "PAN_CARD_IN" => $"ABCDE{(hash % 8900) + 1000}F",
            "MEDICAL_PHI" => $"Clinical Care Note MRN-{(hash % 89000) + 10000}",
            _ => $"[SHADOW_{entityType}_{hash % 9999:D4}]"
        };
    }

    public async Task<string> CreateOrGetTokenAsync(
        string entityType,
        string originalValue,
        string maskedPreview,
        string requestId,
        string userEmail,
        TimeSpan? ttl = null,
        bool useSyntheticSurrogate = false)
    {
        PurgeExpiredTokens();

        var compositeKey = $"{entityType}:{(useSyntheticSurrogate ? "synth:" : "token:")}{originalValue}";
        if (_valueToTokenIndex.TryGetValue(compositeKey, out var existingToken) &&
            _activeTokens.TryGetValue(existingToken, out var existingEntry) &&
            existingEntry.ExpiresAtUtc > DateTime.UtcNow)
        {
            existingEntry.ExpiresAtUtc = DateTime.UtcNow.Add(ttl ?? _defaultTtl);
            return existingEntry.Token;
        }

        string fullToken;
        if (useSyntheticSurrogate)
        {
            fullToken = GenerateSyntheticShadow(entityType, originalValue);
        }
        else
        {
            var hashBytes = SHA256.HashData(Encoding.UTF8.GetBytes($"{originalValue}:{requestId[..Math.Min(4, requestId.Length)]}"));
            var shortHex = Convert.ToHexString(hashBytes)[..6];
            fullToken = $"[{entityType}_{shortHex}]";
        }

        var expiration = DateTime.UtcNow.Add(ttl ?? _defaultTtl);
        var entry = new EphemeralTokenEntry
        {
            Token = fullToken,
            EntityType = entityType,
            OriginalValue = originalValue,
            MaskedPreview = maskedPreview,
            RequestId = requestId,
            UserEmail = userEmail,
            CreatedAtUtc = DateTime.UtcNow,
            ExpiresAtUtc = expiration,
            StorageBackend = _storageMode,
            RestoredCount = 0,
            IsSyntheticSurrogate = useSyntheticSurrogate
        };

        _activeTokens[fullToken] = entry;
        _valueToTokenIndex[compositeKey] = fullToken;

        try
        {
            var serialized = JsonSerializer.Serialize(entry);
            await _distributedCache.SetStringAsync(
                $"dlp:token:{fullToken}",
                serialized,
                new DistributedCacheEntryOptions
                {
                    AbsoluteExpiration = expiration
                });
        }
        catch (Exception ex)
        {
            _logger.LogDebug(ex, "Redis cache unavailable; using local ephemeral memory vault for token {Token}", fullToken);
        }

        return fullToken;
    }

    public async Task<(string RestoredText, int RestoredCount)> RestoreTokensAsync(string textWithTokens)
    {
        if (string.IsNullOrEmpty(textWithTokens))
        {
            return (textWithTokens, 0);
        }

        PurgeExpiredTokens();
        int restoredCount = 0;
        var resultBuilder = new StringBuilder(textWithTokens);

        // 1. Process bracketed tokens e.g. [PERSON_NAME_IN_7A9B]
        var matches = TokenPlaceholderRegex().Matches(textWithTokens);
        if (matches.Count > 0)
        {
            var uniqueTokens = matches.Select(m => m.Value).Distinct(StringComparer.OrdinalIgnoreCase).ToList();

            foreach (var token in uniqueTokens)
            {
                EphemeralTokenEntry? entry = null;

                if (_activeTokens.TryGetValue(token, out var memEntry) && memEntry.ExpiresAtUtc > DateTime.UtcNow)
                {
                    entry = memEntry;
                }
                else
                {
                    try
                    {
                        var cachedJson = await _distributedCache.GetStringAsync($"dlp:token:{token}");
                        if (!string.IsNullOrEmpty(cachedJson))
                        {
                            entry = JsonSerializer.Deserialize<EphemeralTokenEntry>(cachedJson);
                            if (entry != null)
                            {
                                _activeTokens[token] = entry;
                            }
                        }
                    }
                    catch
                    {
                        // Fallback gracefully
                    }
                }

                if (entry != null && entry.ExpiresAtUtc > DateTime.UtcNow)
                {
                    resultBuilder.Replace(token, entry.OriginalValue);
                    entry.RestoredCount++;
                    restoredCount++;
                }
            }
        }

        // 2. Process format-preserving synthetic shadows (sorted by length descending)
        var syntheticEntries = _activeTokens.Values
            .Where(e => e.IsSyntheticSurrogate && e.ExpiresAtUtc > DateTime.UtcNow)
            .OrderByDescending(e => e.Token.Length)
            .ToList();

        string currentText = resultBuilder.ToString();
        foreach (var synEntry in syntheticEntries)
        {
            if (currentText.Contains(synEntry.Token, StringComparison.OrdinalIgnoreCase))
            {
                currentText = Regex.Replace(
                    currentText,
                    Regex.Escape(synEntry.Token),
                    synEntry.OriginalValue.Replace("$", "$$"),
                    RegexOptions.IgnoreCase);
                synEntry.RestoredCount++;
                restoredCount++;
            }
        }

        return (currentText, restoredCount);
    }

    public IReadOnlyList<EphemeralTokenEntry> GetActiveTokens()
    {
        PurgeExpiredTokens();
        return _activeTokens.Values
            .OrderByDescending(t => t.CreatedAtUtc)
            .ToList();
    }

    public int PurgeExpiredTokens()
    {
        var now = DateTime.UtcNow;
        int purged = 0;
        foreach (var kvp in _activeTokens)
        {
            if (kvp.Value.ExpiresAtUtc <= now)
            {
                if (_activeTokens.TryRemove(kvp.Key, out var removed))
                {
                    _valueToTokenIndex.TryRemove($"{removed.EntityType}:{(removed.IsSyntheticSurrogate ? "synth:" : "token:")}{removed.OriginalValue}", out _);
                    purged++;
                }
            }
        }
        return purged;
    }

    public async Task FlushAllTokensAsync()
    {
        foreach (var key in _activeTokens.Keys)
        {
            try
            {
                await _distributedCache.RemoveAsync($"dlp:token:{key}");
            }
            catch
            {
                // Ignore if distributed cache is offline
            }
        }
        _activeTokens.Clear();
        _valueToTokenIndex.Clear();
    }
}

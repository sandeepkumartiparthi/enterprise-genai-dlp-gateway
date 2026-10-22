using GenAiDlpGateway.Data;
using GenAiDlpGateway.Models;
using GenAiDlpGateway.Services;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Caching.Distributed;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging.Abstractions;
using Xunit;

namespace GenAiDlpGateway.Tests;

public class DlpGatewayDeepTests
{
    private static (IDlpEngineService DlpEngine, ITokenVaultService TokenVault, ServiceProvider Provider) BuildTestServices()
    {
        var services = new ServiceCollection();
        var dbName = $"DlpTestDb_{Guid.NewGuid():N}";

        var config = new ConfigurationBuilder()
            .AddInMemoryCollection(new Dictionary<string, string?>
            {
                ["DlpGateway:TokenTtlMinutes"] = "15",
                ["DlpGateway:PresidioAnalyzerUrl"] = ""
            })
            .Build();

        services.AddSingleton<IConfiguration>(config);
        services.AddLogging();
        services.AddDistributedMemoryCache();
        services.AddHttpClient();
        services.AddDbContext<DlpAuditDbContext>(opt => opt.UseInMemoryDatabase(dbName));
        services.AddSingleton<ITokenVaultService, TokenVaultService>();
        services.AddScoped<IDlpEngineService, DlpEngineService>();

        var provider = services.BuildServiceProvider();
        DatabaseSeeder.SeedAsync(provider).GetAwaiter().GetResult();

        var scope = provider.CreateScope();
        var dlpEngine = scope.ServiceProvider.GetRequiredService<IDlpEngineService>();
        var tokenVault = provider.GetRequiredService<ITokenVaultService>();

        return (dlpEngine, tokenVault, provider);
    }

    [Fact]
    public async Task InspectAndSanitize_ShouldTokenize_Aadhaar_CreditCard_Phone_And_PersonName_WithoutStopwordCollision()
    {
        var (dlp, vault, _) = BuildTestServices();
        var prompt = "Verify KYC for Customer Rahul Verma (phone +91 98201 44829) with Aadhaar 4829 6103 9482 and Visa card 4532-8910-4421-8892 for Regulatory Reporting.";

        var result = await dlp.InspectAndSanitizeAsync(prompt, "priya.nair@corp.acme.io");

        Assert.False(result.IsBlocked);
        Assert.Equal(DlpActionType.TOKENIZE, result.OverallAction);

        var personEntities = result.Entities.Where(e => e.EntityType == "PERSON").ToList();
        Assert.Single(personEntities);
        Assert.Equal("Rahul Verma", personEntities[0].OriginalValue);

        Assert.Contains(result.Entities, e => e.EntityType == "PHONE_NUMBER" && e.OriginalValue == "+91 98201 44829");
        Assert.Contains(result.Entities, e => e.EntityType == "AADHAAR_IN" && e.OriginalValue == "4829 6103 9482");
        Assert.Contains(result.Entities, e => e.EntityType == "CREDIT_CARD" && e.OriginalValue == "4532-8910-4421-8892");

        // Ensure raw values are completely removed from SanitizedText
        Assert.DoesNotContain("Rahul Verma", result.SanitizedText);
        Assert.DoesNotContain("4829 6103 9482", result.SanitizedText);
        Assert.DoesNotContain("4532-8910-4421-8892", result.SanitizedText);

        // Verify de-tokenization restores all 3 entities accurately
        var simulatedLlmReply = $"Processed KYC for {personEntities[0].ReplacementToken} with UIDAI {result.Entities.First(e => e.EntityType == "AADHAAR_IN").ReplacementToken}.";
        var (restoredText, count) = await vault.RestoreTokensAsync(simulatedLlmReply);

        Assert.Equal(2, count);
        Assert.Contains("Rahul Verma", restoredText);
        Assert.Contains("4829 6103 9482", restoredText);
    }

    [Fact]
    public async Task RestoreTokens_ShouldHandle_LowercaseTokensFromLlm_CaseInsensitively()
    {
        var (_, vault, _) = BuildTestServices();
        var token = await vault.CreateOrGetTokenAsync("PERSON", "Anita Desai", "An••••ai", "req-9999", "dr.elena@corp.acme.io");

        // Simulate an LLM altering token casing to lowercase
        var lowerToken = token.ToLowerInvariant();
        var llmOutput = $"Discharge summary prepared for patient {lowerToken}.";

        var (restored, count) = await vault.RestoreTokensAsync(llmOutput);

        Assert.Equal(1, count);
        Assert.Equal("Discharge summary prepared for patient Anita Desai.", restored);
    }

    [Fact]
    public async Task InspectAndSanitize_ShouldBlock_ProprietarySourceCode_And_Redact_ApiKeys()
    {
        var (dlp, _, _) = BuildTestServices();
        var prompt = "Optimize namespace Acme.CoreBilling.Internal with key sk-proj-98aF2bLmN4xQpR7vWzK109283";

        var result = await dlp.InspectAndSanitizeAsync(prompt, "dev@corp.acme.io");

        Assert.True(result.IsBlocked);
        Assert.Equal(DlpActionType.BLOCK, result.OverallAction);
        Assert.Contains(result.Entities, e => e.EntityType == "SOURCE_CODE" && e.ActionApplied == DlpActionType.BLOCK);
        Assert.Contains(result.Entities, e => e.EntityType == "API_KEY_SECRET" && e.ActionApplied == DlpActionType.REDACT);
    }

    [Fact]
    public async Task CustomRegexPolicy_ShouldDetect_And_Tokenize_IndianPanCard()
    {
        var (dlp, vault, _) = BuildTestServices();

        await dlp.CreateCustomPolicyAsync(new DlpPolicyRule
        {
            EntityType = "PAN_CARD_IN",
            DisplayName = "Indian Income Tax PAN",
            Category = "Financial",
            CustomRegexPattern = @"\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b",
            Action = DlpActionType.TOKENIZE,
            Severity = RiskSeverity.HIGH
        });

        var result = await dlp.InspectAndSanitizeAsync("Verify tax filing for PAN ABCDE1234F immediately.");

        Assert.Single(result.Entities);
        Assert.Equal("PAN_CARD_IN", result.Entities[0].EntityType);
        Assert.Equal("ABCDE1234F", result.Entities[0].OriginalValue);
        Assert.DoesNotContain("ABCDE1234F", result.SanitizedText);

        var (restored, count) = await vault.RestoreTokensAsync($"Confirmed filing for {result.Entities[0].ReplacementToken}.");
        Assert.Equal(1, count);
        Assert.Equal("Confirmed filing for ABCDE1234F.", restored);
    }

    [Fact]
    public async Task TokenVault_ShouldPurgeExpiredTokens_Automatically()
    {
        var (_, vault, _) = BuildTestServices();
        var expiredToken = await vault.CreateOrGetTokenAsync(
            "US_SSN",
            "412-58-4109",
            "•••• •••• 4109",
            "req-exp",
            "user@corp.acme.io",
            ttl: TimeSpan.FromMilliseconds(-50));

        var purged = vault.PurgeExpiredTokens();
        Assert.True(purged >= 1);

        var (restored, count) = await vault.RestoreTokensAsync($"SSN is {expiredToken}");
        Assert.Equal(0, count);
        Assert.Equal($"SSN is {expiredToken}", restored);
    }

    [Fact]
    public async Task SourceCode_WithEmbeddedSecretsAndInternalIp_ShouldDetectAllThree_AndBlock()
    {
        var (dlp, _, _) = BuildTestServices();
        var prompt = @"Optimize this C# repository class and check why our key sk-proj-9a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a is failing:
public class PaymentVaultRepository {
    private readonly string _conn = ""Server=10.24.18.92;Database=CoreLedger;Password=SuperSecret99!;"";
    public async Task ProcessAsync() { }
}";

        var result = await dlp.InspectAndSanitizeAsync(prompt, "dev@corp.acme.io");

        Assert.True(result.IsBlocked);
        Assert.Equal(DlpActionType.BLOCK, result.OverallAction);
        Assert.Contains(result.Entities, e => e.EntityType == "SOURCE_CODE" && e.ActionApplied == DlpActionType.BLOCK);
        Assert.Contains(result.Entities, e => e.EntityType == "API_KEY_SECRET" && e.ActionApplied == DlpActionType.REDACT);
        Assert.Contains(result.Entities, e => e.EntityType == "IPV4_INTERNAL" && e.OriginalValue == "10.24.18.92");
    }

    [Fact]
    public async Task ConcurrentRequests_ShouldTokenizeAndRestore_WithoutRaceConditions()
    {
        var (_, vault, provider) = BuildTestServices();

        var tasks = Enumerable.Range(1, 25).Select(async i =>
        {
            using var scope = provider.CreateScope();
            var dlp = scope.ServiceProvider.GetRequiredService<IDlpEngineService>();
            var aadhaar = $"4829 6103 {1000 + i:D4}";
            var prompt = $"Draft KYC confirmation for customer Kiran Rao with Aadhaar {aadhaar}.";

            var res = await dlp.InspectAndSanitizeAsync(prompt, $"user{i}@corp.acme.io");
            Assert.False(res.IsBlocked);
            Assert.DoesNotContain(aadhaar, res.SanitizedText);

            var aadhaarEntity = Assert.Single(res.Entities, e => e.EntityType == "AADHAAR_IN");
            var (restored, count) = await vault.RestoreTokensAsync($"Verified UIDAI {aadhaarEntity.ReplacementToken}");
            Assert.Equal(1, count);
            Assert.Equal($"Verified UIDAI {aadhaar}", restored);
        });

        await Task.WhenAll(tasks);
    }
}

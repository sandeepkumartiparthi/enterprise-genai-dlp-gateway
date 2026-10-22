using System.Diagnostics;
using System.Text;
using System.Text.Json;
using System.Text.Json.Nodes;
using GenAiDlpGateway.Data;
using GenAiDlpGateway.Models;
using GenAiDlpGateway.Services;

namespace GenAiDlpGateway.Proxy;

public class YarpDlpProxyMiddleware
{
    private readonly RequestDelegate _next;
    private readonly ILogger<YarpDlpProxyMiddleware> _logger;

    public YarpDlpProxyMiddleware(RequestDelegate next, ILogger<YarpDlpProxyMiddleware> logger)
    {
        _next = next;
        _logger = logger;
    }

    public async Task InvokeAsync(
        HttpContext context,
        IDlpEngineService dlpEngine,
        ITokenVaultService tokenVault,
        IServiceScopeFactory scopeFactory)
    {
        // Only intercept YARP proxy routes under /v1/
        if (!context.Request.Path.StartsWithSegments("/v1", StringComparison.OrdinalIgnoreCase) ||
            !HttpMethods.IsPost(context.Request.Method))
        {
            await _next(context);
            return;
        }

        context.Request.EnableBuffering();
        string rawRequestBody;
        using (var reader = new StreamReader(context.Request.Body, Encoding.UTF8, detectEncodingFromByteOrderMarks: false, leaveOpen: true))
        {
            rawRequestBody = await reader.ReadToEndAsync();
            context.Request.Body.Position = 0;
        }

        if (string.IsNullOrWhiteSpace(rawRequestBody))
        {
            await _next(context);
            return;
        }

        var userEmail = context.Request.Headers["X-User-Email"].FirstOrDefault() ?? "arjun.mehta@corp.acme.io";
        var department = context.Request.Headers["X-Department"].FirstOrDefault() ?? "Engineering";
        var targetProvider = context.Request.Headers["X-Target-Provider"].FirstOrDefault() ?? "OpenAI (gpt-4o)";
        var privacyMode = context.Request.Headers["X-DLP-Privacy-Mode"].FirstOrDefault() ?? "synthetic";
        bool useSyntheticShadows = !string.Equals(privacyMode, "token", StringComparison.OrdinalIgnoreCase);

        // Extract prompt text from OpenAI/Anthropic compatible JSON body
        string combinedUserPrompt = rawRequestBody;
        JsonNode? rootNode = null;
        try
        {
            rootNode = JsonNode.Parse(rawRequestBody);
            if (rootNode?["model"]?.GetValue<string>() is string modelName && !string.IsNullOrWhiteSpace(modelName))
            {
                if (!context.Request.Headers.ContainsKey("X-Target-Provider"))
                {
                    targetProvider = modelName;
                }
            }

            if (rootNode?["messages"] is JsonArray messagesArray && messagesArray.Count > 0)
            {
                var userContents = new List<string>();
                foreach (var msg in messagesArray)
                {
                    var content = msg?["content"]?.GetValue<string>();
                    if (!string.IsNullOrEmpty(content))
                    {
                        userContents.Add(content);
                    }
                }
                if (userContents.Count > 0)
                {
                    combinedUserPrompt = string.Join("\n", userContents);
                }
            }
            else if (rootNode?["prompt"]?.GetValue<string>() is string singlePrompt)
            {
                combinedUserPrompt = singlePrompt;
            }
        }
        catch
        {
            // Non-JSON or custom payload; inspect raw body directly
        }

        // 1. Inspect and sanitize prompt using DLP Engine (with 2027 synthetic shadow surrogates & threat detection)
        var inspection = await dlpEngine.InspectAndSanitizeAsync(
            combinedUserPrompt,
            userEmail,
            useSyntheticShadows: useSyntheticShadows);

        context.Response.Headers["X-DLP-Request-Id"] = inspection.RequestId;
        context.Response.Headers["X-DLP-Action"] = inspection.OverallAction.ToString();
        context.Response.Headers["X-DLP-Entities-Detected"] = inspection.Entities.Count.ToString();
        context.Response.Headers["X-DLP-Risk-Score"] = inspection.RiskScore.ToString();
        context.Response.Headers["X-DLP-Latency-Ms"] = inspection.InspectionDurationMs.ToString("F2");
        context.Response.Headers["X-DLP-Privacy-Mode"] = inspection.PrivacyMode;
        context.Response.Headers["X-DLP-Proof-Hash"] = inspection.CryptoProof?.ProofHash ?? string.Empty;
        context.Response.Headers["X-DLP-Threat-Score"] = inspection.AdversarialThreat.ThreatScore.ToString();
        context.Response.Headers["X-DLP-Threat-Category"] = inspection.AdversarialThreat.ThreatCategory;

        // Build masked original prompt for safe compliance storage (never store raw unmasked secrets in DB)
        var maskedOriginalPrompt = BuildMaskedAuditPrompt(combinedUserPrompt, inspection.Entities);

        // 2. Handle BLOCK policy immediately before YARP reaches upstream LLM
        if (inspection.IsBlocked)
        {
            var blockPayload = new
            {
                error = new
                {
                    message = inspection.BlockReason,
                    type = "dlp_policy_violation",
                    code = "policy_blocked",
                    request_id = inspection.RequestId,
                    risk_score = inspection.RiskScore,
                    detected_entities = inspection.Entities.Select(e => new
                    {
                        e.EntityType,
                        e.DisplayName,
                        e.Category,
                        e.MaskedPreview,
                        e.ActionApplied,
                        e.Severity,
                        e.Confidence,
                        e.DetectorSource
                    })
                },
                dlp_telemetry = new
                {
                    requestId = inspection.RequestId,
                    action = inspection.OverallAction.ToString(),
                    isBlocked = true,
                    riskScore = inspection.RiskScore,
                    dlpLatencyMs = inspection.InspectionDurationMs,
                    upstreamLatencyMs = 0.0,
                    tokensRestoredCount = 0,
                    privacyMode = inspection.PrivacyMode,
                    proofHash = inspection.CryptoProof?.ProofHash,
                    cryptoProof = inspection.CryptoProof,
                    adversarialThreat = inspection.AdversarialThreat,
                    originalMaskedPrompt = maskedOriginalPrompt,
                    sanitizedPromptSentToLlm = "[BLOCKED BY GATEWAY - NOT FORWARDED TO UPSTREAM LLM]",
                    llmRawResponseWithTokens = "[UPSTREAM NOT CONTACTED]",
                    restoredResponseToUser = inspection.BlockReason,
                    entities = inspection.Entities.Select(e => new
                    {
                        e.EntityType,
                        e.DisplayName,
                        e.Category,
                        e.MaskedPreview,
                        e.ReplacementToken,
                        e.Confidence,
                        e.DetectorSource,
                        e.ActionApplied,
                        e.Severity
                    })
                }
            };

            await RecordAuditLogAsync(
                scopeFactory,
                inspection,
                userEmail,
                department,
                targetProvider,
                context.Request.Path,
                maskedOriginalPrompt,
                "[BLOCKED BY GATEWAY - NOT FORWARDED]",
                "[UPSTREAM NOT CONTACTED]",
                inspection.BlockReason ?? "Blocked by DLP Policy",
                0,
                0);

            context.Response.StatusCode = StatusCodes.Status403Forbidden;
            context.Response.ContentType = "application/json";
            await context.Response.WriteAsync(JsonSerializer.Serialize(blockPayload));
            return;
        }

        // 3. Rewrite request JSON body with sanitized/tokenized prompt for YARP forwarding
        string rewrittenRequestBody = rawRequestBody;
        if (rootNode != null)
        {
            if (rootNode["messages"] is JsonArray messagesArray)
            {
                foreach (var msg in messagesArray)
                {
                    if (msg?["content"]?.GetValue<string>() is string content && !string.IsNullOrEmpty(content))
                    {
                        var msgInspection = await dlpEngine.InspectAndSanitizeAsync(
                            content,
                            userEmail,
                            inspection.RequestId,
                            useSyntheticShadows: useSyntheticShadows);
                        msg["content"] = msgInspection.SanitizedText;
                    }
                }
                rewrittenRequestBody = rootNode.ToJsonString();
            }
            else if (rootNode["prompt"] != null)
            {
                rootNode["prompt"] = inspection.SanitizedText;
                rewrittenRequestBody = rootNode.ToJsonString();
            }
        }
        else
        {
            rewrittenRequestBody = inspection.SanitizedText;
        }

        var rewrittenBytes = Encoding.UTF8.GetBytes(rewrittenRequestBody);
        context.Request.Body = new MemoryStream(rewrittenBytes);
        context.Request.ContentLength = rewrittenBytes.Length;

        // 4. Intercept response stream from YARP upstream to restore ephemeral tokens before returning to user
        var originalResponseBodyStream = context.Response.Body;
        using var upstreamBufferStream = new MemoryStream();
        context.Response.Body = upstreamBufferStream;

        var upstreamSw = Stopwatch.StartNew();
        await _next(context);
        upstreamSw.Stop();

        upstreamBufferStream.Position = 0;
        var rawUpstreamResponseBody = await new StreamReader(upstreamBufferStream, Encoding.UTF8).ReadToEndAsync();

        // Extract assistant message from upstream JSON response, restore tokens, apply reverse leak safety scan, and enrich with DLP telemetry
        var (restoredFullBody, llmRawMessageText, restoredMessageText, restoredCount) =
            await RestoreTokensInUpstreamPayloadAsync(rawUpstreamResponseBody, tokenVault, dlpEngine, inspection, maskedOriginalPrompt, upstreamSw.Elapsed.TotalMilliseconds);

        context.Response.Headers["X-DLP-Tokens-Restored"] = restoredCount.ToString();

        // 5. Persist Audit Log entry
        await RecordAuditLogAsync(
            scopeFactory,
            inspection,
            userEmail,
            department,
            targetProvider,
            context.Request.Path,
            maskedOriginalPrompt,
            inspection.SanitizedText,
            llmRawMessageText,
            restoredMessageText,
            restoredCount,
            Math.Round(upstreamSw.Elapsed.TotalMilliseconds, 2));

        var finalBytes = Encoding.UTF8.GetBytes(restoredFullBody);
        context.Response.ContentLength = finalBytes.Length;
        context.Response.Body = originalResponseBodyStream;
        await context.Response.Body.WriteAsync(finalBytes);
    }

    private static async Task<(string FinalJsonBody, string RawLlmMessage, string RestoredLlmMessage, int RestoredCount)> RestoreTokensInUpstreamPayloadAsync(
        string rawUpstreamBody,
        ITokenVaultService tokenVault,
        IDlpEngineService dlpEngine,
        DlpInspectionResult inspection,
        string maskedOriginalPrompt,
        double upstreamLatencyMs)
    {
        try
        {
            var node = JsonNode.Parse(rawUpstreamBody);
            if (node != null && node["choices"] is JsonArray choices && choices.Count > 0)
            {
                var firstChoice = choices[0];
                var rawContent = firstChoice?["message"]?["content"]?.GetValue<string>() ?? string.Empty;
                var (restoredContent, restoredCount) = await tokenVault.RestoreTokensAsync(rawContent);

                // Reverse LLM output safety scanning: redact any accidentally reflected or hallucinated secrets
                var (safeContent, leaksScrubbed) = dlpEngine.ScanAndRedactUpstreamResponseLeaks(restoredContent);
                restoredContent = safeContent;

                if (firstChoice?["message"] != null)
                {
                    firstChoice["message"]!["content"] = restoredContent;
                }

                // Attach non-breaking dlp_telemetry object so enterprise clients & dashboard sandbox can visualize the exact pipeline stages
                node["dlp_telemetry"] = JsonSerializer.SerializeToNode(new
                {
                    requestId = inspection.RequestId,
                    action = inspection.OverallAction.ToString(),
                    isBlocked = false,
                    riskScore = inspection.RiskScore,
                    dlpLatencyMs = inspection.InspectionDurationMs,
                    upstreamLatencyMs = Math.Round(upstreamLatencyMs, 2),
                    tokensRestoredCount = restoredCount,
                    privacyMode = inspection.PrivacyMode,
                    proofHash = inspection.CryptoProof?.ProofHash,
                    cryptoProof = inspection.CryptoProof,
                    adversarialThreat = inspection.AdversarialThreat,
                    leaksScrubbedCount = leaksScrubbed,
                    originalMaskedPrompt = maskedOriginalPrompt,
                    sanitizedPromptSentToLlm = inspection.SanitizedText,
                    llmRawResponseWithTokens = rawContent,
                    restoredResponseToUser = restoredContent,
                    entities = inspection.Entities.Select(e => new
                    {
                        e.EntityType,
                        e.DisplayName,
                        e.Category,
                        e.MaskedPreview,
                        e.ReplacementToken,
                        e.Confidence,
                        e.DetectorSource,
                        e.ActionApplied,
                        e.Severity
                    })
                });

                return (node.ToJsonString(), rawContent, restoredContent, restoredCount);
            }
        }
        catch
        {
            // Fallback to raw text token restoration
        }

        var (fallbackRestored, fallbackCount) = await tokenVault.RestoreTokensAsync(rawUpstreamBody);
        var (finalCleaned, _) = dlpEngine.ScanAndRedactUpstreamResponseLeaks(fallbackRestored);
        return (finalCleaned, rawUpstreamBody, finalCleaned, fallbackCount);
    }

    private static string BuildMaskedAuditPrompt(string originalPrompt, List<DetectedEntity> entities)
    {
        if (entities.Count == 0) return originalPrompt;
        var sb = new StringBuilder(originalPrompt);
        foreach (var entity in entities.OrderByDescending(e => e.StartIndex))
        {
            if (entity.StartIndex >= 0 && entity.EndIndex <= sb.Length)
            {
                sb.Remove(entity.StartIndex, entity.EndIndex - entity.StartIndex);
                sb.Insert(entity.StartIndex, $"{entity.MaskedPreview}");
            }
        }
        return sb.ToString();
    }

    private static async Task RecordAuditLogAsync(
        IServiceScopeFactory scopeFactory,
        DlpInspectionResult inspection,
        string userEmail,
        string department,
        string targetProvider,
        string path,
        string maskedOriginalPrompt,
        string sanitizedPrompt,
        string llmRawResponse,
        string restoredResponse,
        int tokensRestoredCount,
        double upstreamLatencyMs)
    {
        using var scope = scopeFactory.CreateScope();
        var db = scope.ServiceProvider.GetRequiredService<DlpAuditDbContext>();

        var summaryList = inspection.Entities.Select(e => new
        {
            e.EntityType,
            e.DisplayName,
            e.Category,
            e.MaskedPreview,
            e.ReplacementToken,
            e.ActionApplied,
            e.Severity,
            e.Confidence,
            e.DetectorSource
        }).ToList();

        var entry = new AuditLogEntry
        {
            Id = Guid.NewGuid(),
            RequestId = inspection.RequestId,
            TimestampUtc = DateTime.UtcNow,
            UserEmail = userEmail,
            Department = department,
            TargetProvider = targetProvider,
            UpstreamPath = path,
            ActionTaken = inspection.OverallAction,
            Severity = inspection.MaxSeverity,
            RiskScore = inspection.RiskScore,
            EntitiesDetectedCount = inspection.Entities.Count,
            TokensRestoredCount = tokensRestoredCount,
            EntitiesSummaryJson = JsonSerializer.Serialize(summaryList),
            MaskedOriginalPrompt = maskedOriginalPrompt,
            SanitizedPromptSentToLlm = sanitizedPrompt,
            LlmRawResponseWithTokens = llmRawResponse,
            RestoredResponseToUser = restoredResponse,
            DlpLatencyMs = inspection.InspectionDurationMs,
            UpstreamLatencyMs = upstreamLatencyMs,
            ProofHash = inspection.CryptoProof?.ProofHash,
            AdversarialScore = inspection.AdversarialThreat.ThreatScore,
            ThreatCategory = inspection.AdversarialThreat.ThreatCategory,
            PrivacyMode = inspection.PrivacyMode
        };

        db.AuditLogs.Add(entry);
        await db.SaveChangesAsync();
    }
}

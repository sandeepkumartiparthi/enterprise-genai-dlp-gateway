using System.Text.Json;
using GenAiDlpGateway.Models;
using GenAiDlpGateway.Services;
using Microsoft.EntityFrameworkCore;

namespace GenAiDlpGateway.Data;

public static class DatabaseSeeder
{
    public static async Task SeedAsync(IServiceProvider services)
    {
        using var scope = services.CreateScope();
        var db = scope.ServiceProvider.GetRequiredService<DlpAuditDbContext>();
        var tokenVault = scope.ServiceProvider.GetRequiredService<ITokenVaultService>();

        try
        {
            await db.Database.EnsureCreatedAsync();
            // Verify new columns exist; if upgrading from an older local sqlite file, recreate cleanly
            _ = await db.PolicyRules.Select(p => p.CustomRegexPattern).FirstOrDefaultAsync();
            _ = await db.AuditLogs.Select(a => a.ProofHash).FirstOrDefaultAsync();
        }
        catch
        {
            await db.Database.EnsureDeletedAsync();
            await db.Database.EnsureCreatedAsync();
        }

        var defaultPolicies = new List<DlpPolicyRule>
        {
            new()
            {
                EntityType = "CREDIT_CARD",
                DisplayName = "Credit / Debit Card (PCI-DSS)",
                Category = "Financial",
                Description = "Detects 13-19 digit payment card numbers with Luhn checksum verification and replaces with reversible tokens.",
                Action = DlpActionType.TOKENIZE,
                Severity = RiskSeverity.CRITICAL,
                Enabled = true,
                MinConfidence = 0.85,
                DetectionEngine = "C# PCI Tokenizer + Luhn Validator"
            },
            new()
            {
                EntityType = "IBAN_SWIFT",
                DisplayName = "IBAN / International Bank Account",
                Category = "Financial",
                Description = "Detects ISO-13616 International Bank Account Numbers (IBAN) in corporate treasury and wire prompts.",
                Action = DlpActionType.TOKENIZE,
                Severity = RiskSeverity.HIGH,
                Enabled = true,
                MinConfidence = 0.85,
                DetectionEngine = "ISO-13616 IBAN Recognizer"
            },
            new()
            {
                EntityType = "AADHAAR_IN",
                DisplayName = "Indian Aadhaar (UIDAI)",
                Category = "PII",
                Description = "Detects 12-digit Indian Aadhaar identity numbers (UIDAI format) and tokenizes before reaching external LLMs.",
                Action = DlpActionType.TOKENIZE,
                Severity = RiskSeverity.CRITICAL,
                Enabled = true,
                MinConfidence = 0.85,
                DetectionEngine = "Presidio + C# UIDAI Recognizer"
            },
            new()
            {
                EntityType = "US_SSN",
                DisplayName = "US Social Security Number (SSN)",
                Category = "PII",
                Description = "Detects US SSNs (XXX-XX-XXXX) excluding invalid SSA area prefixes.",
                Action = DlpActionType.TOKENIZE,
                Severity = RiskSeverity.CRITICAL,
                Enabled = true,
                MinConfidence = 0.85,
                DetectionEngine = "Presidio + US_SSN Recognizer"
            },
            new()
            {
                EntityType = "API_KEY_SECRET",
                DisplayName = "API Key / Cloud Secret",
                Category = "Credentials",
                Description = "Detects OpenAI, Anthropic, AWS IAM, GitHub PAT, Slack tokens, and DB passwords. Irreversibly redacted by default.",
                Action = DlpActionType.REDACT,
                Severity = RiskSeverity.CRITICAL,
                Enabled = true,
                MinConfidence = 0.90,
                DetectionEngine = "C# Secret Scanner + Regex"
            },
            new()
            {
                EntityType = "JWT_TOKEN",
                DisplayName = "JSON Web Token (Bearer JWT)",
                Category = "Credentials",
                Description = "Detects signed OAuth2 / OIDC Bearer JWT tokens (eyJ...) and redacts them prior to egress.",
                Action = DlpActionType.REDACT,
                Severity = RiskSeverity.HIGH,
                Enabled = true,
                MinConfidence = 0.90,
                DetectionEngine = "JWT Header/Payload Recognizer"
            },
            new()
            {
                EntityType = "SOURCE_CODE",
                DisplayName = "Proprietary Source Code / Keys",
                Category = "SourceCode",
                Description = "Blocks prompts containing PEM private keys, internal corporate namespaces, or production connection strings.",
                Action = DlpActionType.BLOCK,
                Severity = RiskSeverity.CRITICAL,
                Enabled = true,
                MinConfidence = 0.85,
                DetectionEngine = "AST & Entropy Code Guard"
            },
            new()
            {
                EntityType = "IPV4_INTERNAL",
                DisplayName = "Internal Corporate Subnet IP",
                Category = "SourceCode",
                Description = "Detects RFC-1918 private network addresses (10.x.x.x, 192.168.x.x, 172.16-31.x.x) and tokenizes topology.",
                Action = DlpActionType.TOKENIZE,
                Severity = RiskSeverity.MEDIUM,
                Enabled = true,
                MinConfidence = 0.80,
                DetectionEngine = "RFC-1918 Private Subnet Scanner"
            },
            new()
            {
                EntityType = "MEDICAL_PHI",
                DisplayName = "Medical PHI / HIPAA Record",
                Category = "Medical",
                Description = "Detects Patient Medical Record Numbers (MRN), ICD-10 diagnosis codes, and clinical prescriptions.",
                Action = DlpActionType.TOKENIZE,
                Severity = RiskSeverity.HIGH,
                Enabled = true,
                MinConfidence = 0.80,
                DetectionEngine = "HIPAA Clinical NER"
            },
            new()
            {
                EntityType = "PERSON",
                DisplayName = "Person Full Name (NER)",
                Category = "PII",
                Description = "Contextual Named Entity Recognition for customer, patient, and employee full names.",
                Action = DlpActionType.TOKENIZE,
                Severity = RiskSeverity.MEDIUM,
                Enabled = true,
                MinConfidence = 0.80,
                DetectionEngine = "Contextual NER (PERSON)"
            },
            new()
            {
                EntityType = "EMAIL_ADDRESS",
                DisplayName = "Email Address",
                Category = "PII",
                Description = "Detects corporate and customer email addresses and substitutes reversible session tokens.",
                Action = DlpActionType.TOKENIZE,
                Severity = RiskSeverity.MEDIUM,
                Enabled = true,
                MinConfidence = 0.85,
                DetectionEngine = "Presidio EMAIL_ADDRESS"
            },
            new()
            {
                EntityType = "PHONE_NUMBER",
                DisplayName = "Phone Number",
                Category = "PII",
                Description = "Detects international, US, and Indian (+91) phone numbers.",
                Action = DlpActionType.TOKENIZE,
                Severity = RiskSeverity.LOW,
                Enabled = true,
                MinConfidence = 0.75,
                DetectionEngine = "Presidio PHONE_NUMBER"
            }
        };

        foreach (var rule in defaultPolicies)
        {
            if (!await db.PolicyRules.AnyAsync(r => r.EntityType == rule.EntityType))
            {
                db.PolicyRules.Add(rule);
            }
        }
        await db.SaveChangesAsync();

        if (!await db.AuditLogs.AnyAsync())
        {
            var now = DateTime.UtcNow;

            var tokenName = await tokenVault.CreateOrGetTokenAsync("PERSON", "Rajesh Sharma", "Ra••••ma", "req-seed-01", "priya.nair@corp.acme.io", TimeSpan.FromMinutes(14));
            var tokenAadhaar = await tokenVault.CreateOrGetTokenAsync("AADHAAR_IN", "4829 6103 9482", "•••• •••• 9482", "req-seed-01", "priya.nair@corp.acme.io", TimeSpan.FromMinutes(14));
            var tokenCard = await tokenVault.CreateOrGetTokenAsync("CREDIT_CARD", "4532-8910-4421-8892", "•••• •••• 8892", "req-seed-02", "david.chen@corp.acme.io", TimeSpan.FromMinutes(12));
            var tokenMrn = await tokenVault.CreateOrGetTokenAsync("MEDICAL_PHI", "MRN-884920", "MR••••20", "req-seed-03", "dr.elena@corp.acme.io", TimeSpan.FromMinutes(15));
            var tokenIcd = await tokenVault.CreateOrGetTokenAsync("MEDICAL_PHI", "ICD-10: E11.9", "IC••••.9", "req-seed-03", "dr.elena@corp.acme.io", TimeSpan.FromMinutes(15));

            var seedLogs = new List<AuditLogEntry>
            {
                new()
                {
                    Id = Guid.NewGuid(),
                    RequestId = "req-seed-01",
                    TimestampUtc = now.AddMinutes(-18),
                    UserEmail = "priya.nair@corp.acme.io",
                    Department = "Customer Support",
                    TargetProvider = "OpenAI (gpt-4o)",
                    UpstreamPath = "/v1/chat/completions",
                    ActionTaken = DlpActionType.TOKENIZE,
                    Severity = RiskSeverity.CRITICAL,
                    RiskScore = 75,
                    EntitiesDetectedCount = 2,
                    TokensRestoredCount = 2,
                    EntitiesSummaryJson = JsonSerializer.Serialize(new[]
                    {
                        new { EntityType = "PERSON", DisplayName = "Person Full Name (NER)", Category = "PII", MaskedPreview = "Ra••••ma", ReplacementToken = tokenName, ActionApplied = "TOKENIZE", Severity = "MEDIUM", Confidence = 0.88, DetectorSource = "Contextual NER (PERSON)" },
                        new { EntityType = "AADHAAR_IN", DisplayName = "Indian Aadhaar (UIDAI)", Category = "PII", MaskedPreview = "•••• •••• 9482", ReplacementToken = tokenAadhaar, ActionApplied = "TOKENIZE", Severity = "CRITICAL", Confidence = 0.92, DetectorSource = "Presidio + C# UIDAI Recognizer" }
                    }),
                    MaskedOriginalPrompt = "Draft a KYC verification confirmation email for Customer Ra••••ma whose Aadhaar number •••• •••• 9482 was verified today.",
                    SanitizedPromptSentToLlm = $"Draft a KYC verification confirmation email for Customer {tokenName} whose Aadhaar number {tokenAadhaar} was verified today.",
                    LlmRawResponseWithTokens = $"Dear {tokenName},\n\nWe are pleased to confirm that your KYC verification associated with UIDAI reference {tokenAadhaar} has been successfully completed.",
                    RestoredResponseToUser = "Dear Rajesh Sharma,\n\nWe are pleased to confirm that your KYC verification associated with UIDAI reference 4829 6103 9482 has been successfully completed.",
                    DlpLatencyMs = 2.4,
                    UpstreamLatencyMs = 42.1
                },
                new()
                {
                    Id = Guid.NewGuid(),
                    RequestId = "req-seed-02",
                    TimestampUtc = now.AddMinutes(-14),
                    UserEmail = "david.chen@corp.acme.io",
                    Department = "Finance & Ops",
                    TargetProvider = "Anthropic (claude-3-7-sonnet)",
                    UpstreamPath = "/v1/chat/completions",
                    ActionTaken = DlpActionType.TOKENIZE,
                    Severity = RiskSeverity.CRITICAL,
                    RiskScore = 80,
                    EntitiesDetectedCount = 2,
                    TokensRestoredCount = 1,
                    EntitiesSummaryJson = JsonSerializer.Serialize(new[]
                    {
                        new { EntityType = "CREDIT_CARD", DisplayName = "Credit / Debit Card (PCI-DSS)", Category = "Financial", MaskedPreview = "•••• •••• 8892", ReplacementToken = tokenCard, ActionApplied = "TOKENIZE", Severity = "CRITICAL", Confidence = 0.95, DetectorSource = "C# PCI Tokenizer + Luhn Validator" },
                        new { EntityType = "US_SSN", DisplayName = "US Social Security Number (SSN)", Category = "PII", MaskedPreview = "•••• •••• 4109", ReplacementToken = "[US_SSN_9A4E11]", ActionApplied = "TOKENIZE", Severity = "CRITICAL", Confidence = 0.96, DetectorSource = "Presidio + US_SSN Recognizer" }
                    }),
                    MaskedOriginalPrompt = "Summarize chargeback dispute for card •••• •••• 8892 and verify tax filing SSN •••• •••• 4109.",
                    SanitizedPromptSentToLlm = $"Summarize chargeback dispute for card {tokenCard} and verify tax filing SSN [US_SSN_9A4E11].",
                    LlmRawResponseWithTokens = $"Dispute Summary: Payment instrument {tokenCard} has been flagged for chargeback review under taxpayer ID [US_SSN_9A4E11].",
                    RestoredResponseToUser = "Dispute Summary: Payment instrument 4532-8910-4421-8892 has been flagged for chargeback review under taxpayer ID 412-58-4109.",
                    DlpLatencyMs = 1.9,
                    UpstreamLatencyMs = 38.6
                },
                new()
                {
                    Id = Guid.NewGuid(),
                    RequestId = "req-seed-03",
                    TimestampUtc = now.AddMinutes(-9),
                    UserEmail = "dr.elena@corp.acme.io",
                    Department = "Clinical Research",
                    TargetProvider = "OpenAI (gpt-4o)",
                    UpstreamPath = "/v1/chat/completions",
                    ActionTaken = DlpActionType.TOKENIZE,
                    Severity = RiskSeverity.HIGH,
                    RiskScore = 60,
                    EntitiesDetectedCount = 2,
                    TokensRestoredCount = 2,
                    EntitiesSummaryJson = JsonSerializer.Serialize(new[]
                    {
                        new { EntityType = "MEDICAL_PHI", DisplayName = "Medical PHI / HIPAA Record", Category = "Medical", MaskedPreview = "MR••••20", ReplacementToken = tokenMrn, ActionApplied = "TOKENIZE", Severity = "HIGH", Confidence = 0.91, DetectorSource = "HIPAA Clinical NER" },
                        new { EntityType = "MEDICAL_PHI", DisplayName = "Medical PHI / HIPAA Record", Category = "Medical", MaskedPreview = "IC••••.9", ReplacementToken = tokenIcd, ActionApplied = "TOKENIZE", Severity = "HIGH", Confidence = 0.91, DetectorSource = "HIPAA Clinical NER" }
                    }),
                    MaskedOriginalPrompt = "Create a discharge care checklist for record MR••••20 diagnosed with IC••••.9.",
                    SanitizedPromptSentToLlm = $"Create a discharge care checklist for record {tokenMrn} diagnosed with {tokenIcd}.",
                    LlmRawResponseWithTokens = $"Discharge Care Plan for {tokenMrn} (Primary Code {tokenIcd}):\n1. Schedule HbA1c follow-up in 90 days.\n2. Continue daily glucose monitoring.",
                    RestoredResponseToUser = "Discharge Care Plan for MRN-884920 (Primary Code ICD-10: E11.9):\n1. Schedule HbA1c follow-up in 90 days.\n2. Continue daily glucose monitoring.",
                    DlpLatencyMs = 2.1,
                    UpstreamLatencyMs = 35.4
                },
                new()
                {
                    Id = Guid.NewGuid(),
                    RequestId = "req-seed-04",
                    TimestampUtc = now.AddMinutes(-4),
                    UserEmail = "vikram.patel@corp.acme.io",
                    Department = "Engineering",
                    TargetProvider = "OpenAI (gpt-4o)",
                    UpstreamPath = "/v1/chat/completions",
                    ActionTaken = DlpActionType.BLOCK,
                    Severity = RiskSeverity.CRITICAL,
                    RiskScore = 90,
                    EntitiesDetectedCount = 2,
                    TokensRestoredCount = 0,
                    EntitiesSummaryJson = JsonSerializer.Serialize(new[]
                    {
                        new { EntityType = "SOURCE_CODE", DisplayName = "Proprietary Source Code / Keys", Category = "SourceCode", MaskedPreview = "name••••••••ng", ReplacementToken = "[BLOCKED_SOURCE_CODE]", ActionApplied = "BLOCK", Severity = "CRITICAL", Confidence = 0.94, DetectorSource = "AST & Entropy Code Guard" },
                        new { EntityType = "API_KEY_SECRET", DisplayName = "API Key / Cloud Secret", Category = "Credentials", MaskedPreview = "sk-p••••••••9xQ", ReplacementToken = "[REDACTED_API_KEY_SECRET]", ActionApplied = "REDACT", Severity = "CRITICAL", Confidence = 0.98, DetectorSource = "C# Secret Scanner + Regex" }
                    }),
                    MaskedOriginalPrompt = "Optimize this billing class in name••••••••ng using API key sk-p••••••••9xQ",
                    SanitizedPromptSentToLlm = "[BLOCKED BY GATEWAY - NOT FORWARDED]",
                    LlmRawResponseWithTokens = "[UPSTREAM NOT CONTACTED]",
                    RestoredResponseToUser = "Enterprise DLP Policy Violation: Prompt blocked due to restricted entity detection (Proprietary Source Code / Keys).",
                    DlpLatencyMs = 1.6,
                    UpstreamLatencyMs = 0
                }
            };

            db.AuditLogs.AddRange(seedLogs);
            await db.SaveChangesAsync();
        }
    }
}

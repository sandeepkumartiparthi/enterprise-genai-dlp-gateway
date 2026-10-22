using System.ComponentModel.DataAnnotations;
using System.Text.Json.Serialization;

namespace GenAiDlpGateway.Models;

[JsonConverter(typeof(JsonStringEnumConverter))]
public enum DlpActionType
{
    TOKENIZE,
    REDACT,
    BLOCK,
    ALLOW
}

[JsonConverter(typeof(JsonStringEnumConverter))]
public enum RiskSeverity
{
    LOW,
    MEDIUM,
    HIGH,
    CRITICAL
}

public class DlpPolicyRule
{
    [Key]
    public string EntityType { get; set; } = string.Empty;
    public string DisplayName { get; set; } = string.Empty;
    public string Category { get; set; } = string.Empty; // PII, Financial, Credentials, SourceCode, Medical
    public string Description { get; set; } = string.Empty;
    public DlpActionType Action { get; set; } = DlpActionType.TOKENIZE;
    public RiskSeverity Severity { get; set; } = RiskSeverity.HIGH;
    public bool Enabled { get; set; } = true;
    public double MinConfidence { get; set; } = 0.75;
    public string DetectionEngine { get; set; } = "Hybrid (Regex + Contextual NER + Presidio)";
    public string? CustomRegexPattern { get; set; }
    public bool IsCustomRule { get; set; }
}

public class DetectedEntity
{
    public string EntityType { get; set; } = string.Empty;
    public string DisplayName { get; set; } = string.Empty;
    public string Category { get; set; } = string.Empty;
    public string OriginalValue { get; set; } = string.Empty;
    public string MaskedPreview { get; set; } = string.Empty;
    public string ReplacementToken { get; set; } = string.Empty;
    public int StartIndex { get; set; }
    public int EndIndex { get; set; }
    public double Confidence { get; set; }
    public string DetectorSource { get; set; } = "C# NER/Regex";
    public DlpActionType ActionApplied { get; set; }
    public RiskSeverity Severity { get; set; }
}

public class AdversarialThreatAssessment
{
    public bool IsInjected { get; set; }
    public int ThreatScore { get; set; }
    public string ThreatCategory { get; set; } = "None"; // Prompt_Jailbreak, Delimiter_Injection, Base64_Obfuscation, System_Prompt_Extraction
    public string Explanation { get; set; } = string.Empty;
    public string MitigatedPrompt { get; set; } = string.Empty;
    public double ThreatConfidence { get; set; }
}

public class CryptographicProof
{
    public string ProofHash { get; set; } = string.Empty;
    public string HmacSignature { get; set; } = string.Empty;
    public string InboundDigestSha256 { get; set; } = string.Empty;
    public string OutboundDigestSha256 { get; set; } = string.Empty;
    public string StandardCompliance { get; set; } = "EU AI Act Art. 15 / ISO/IEC 42001:2023 / NIST AI RMF";
    public DateTime TimestampUtc { get; set; } = DateTime.UtcNow;
    public string VerificationStatus { get; set; } = "VERIFIED_TAMPER_EVIDENT";
    public string GuaranteeSummary { get; set; } = "Zero Raw PII & Credentials Exposed to Upstream LLM";
}

public class DlpInspectionResult
{
    public string RequestId { get; set; } = Guid.NewGuid().ToString("N")[..12];
    public string OriginalText { get; set; } = string.Empty;
    public string SanitizedText { get; set; } = string.Empty;
    public bool IsBlocked { get; set; }
    public string? BlockReason { get; set; }
    public DlpActionType OverallAction { get; set; } = DlpActionType.ALLOW;
    public RiskSeverity MaxSeverity { get; set; } = RiskSeverity.LOW;
    public int RiskScore { get; set; }
    public double InspectionDurationMs { get; set; }
    public List<DetectedEntity> Entities { get; set; } = new();
    public AdversarialThreatAssessment AdversarialThreat { get; set; } = new();
    public CryptographicProof? CryptoProof { get; set; }
    public string PrivacyMode { get; set; } = "synthetic";
}

public class EphemeralTokenEntry
{
    public string Token { get; set; } = string.Empty;
    public string EntityType { get; set; } = string.Empty;
    public string OriginalValue { get; set; } = string.Empty;
    public string MaskedPreview { get; set; } = string.Empty;
    public string RequestId { get; set; } = string.Empty;
    public string UserEmail { get; set; } = string.Empty;
    public DateTime CreatedAtUtc { get; set; } = DateTime.UtcNow;
    public DateTime ExpiresAtUtc { get; set; }
    public int TtlSecondsRemaining => Math.Max(0, (int)(ExpiresAtUtc - DateTime.UtcNow).TotalSeconds);
    public string StorageBackend { get; set; } = "InMemory+Redis";
    public int RestoredCount { get; set; }
    public bool IsSyntheticSurrogate { get; set; }
}

public class AuditLogEntry
{
    [Key]
    public Guid Id { get; set; } = Guid.NewGuid();
    public string RequestId { get; set; } = string.Empty;
    public DateTime TimestampUtc { get; set; } = DateTime.UtcNow;
    public string UserEmail { get; set; } = "employee@corp.acme.io";
    public string Department { get; set; } = "Engineering";
    public string TargetProvider { get; set; } = "OpenAI (gpt-4o)";
    public string UpstreamPath { get; set; } = "/v1/chat/completions";
    public DlpActionType ActionTaken { get; set; }
    public RiskSeverity Severity { get; set; }
    public int RiskScore { get; set; }
    public int EntitiesDetectedCount { get; set; }
    public int TokensRestoredCount { get; set; }
    public string EntitiesSummaryJson { get; set; } = "[]";
    public string MaskedOriginalPrompt { get; set; } = string.Empty;
    public string SanitizedPromptSentToLlm { get; set; } = string.Empty;
    public string LlmRawResponseWithTokens { get; set; } = string.Empty;
    public string RestoredResponseToUser { get; set; } = string.Empty;
    public double DlpLatencyMs { get; set; }
    public double UpstreamLatencyMs { get; set; }
    public string? ProofHash { get; set; }
    public int AdversarialScore { get; set; }
    public string? ThreatCategory { get; set; }
    public string PrivacyMode { get; set; } = "synthetic";
}

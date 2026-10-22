export type DlpActionType = 'TOKENIZE' | 'REDACT' | 'BLOCK' | 'ALLOW';
export type RiskSeverity = 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';

export interface DetectedEntity {
  entityType: string;
  displayName: string;
  category: string;
  originalValue?: string;
  maskedPreview: string;
  replacementToken: string;
  startIndex?: number;
  endIndex?: number;
  confidence: number;
  detectorSource: string;
  actionApplied: DlpActionType;
  severity: RiskSeverity;
}

export interface AdversarialThreat {
  isInjected: boolean;
  threatScore: number;
  threatCategory: string;
  explanation: string;
  mitigatedPrompt: string;
  threatConfidence: number;
}

export interface CryptographicProof {
  proofHash: string;
  hmacSignature: string;
  inboundDigestSha256: string;
  outboundDigestSha256: string;
  standardCompliance: string;
  timestampUtc: string;
  verificationStatus: string;
  guaranteeSummary: string;
}

export interface LiveDryRunResult {
  requestId: string;
  originalText: string;
  sanitizedText: string;
  isBlocked: boolean;
  blockReason?: string;
  overallAction: DlpActionType;
  maxSeverity: RiskSeverity;
  riskScore: number;
  inspectionDurationMs: number;
  entities: DetectedEntity[];
  adversarialThreat?: AdversarialThreat;
  cryptoProof?: CryptographicProof;
  privacyMode?: string;
}

export interface DlpTelemetry {
  requestId: string;
  action: DlpActionType;
  isBlocked: boolean;
  riskScore: number;
  dlpLatencyMs: number;
  upstreamLatencyMs: number;
  tokensRestoredCount: number;
  privacyMode?: string;
  proofHash?: string;
  cryptoProof?: CryptographicProof;
  adversarialThreat?: AdversarialThreat;
  leaksScrubbedCount?: number;
  originalMaskedPrompt: string;
  sanitizedPromptSentToLlm: string;
  llmRawResponseWithTokens: string;
  restoredResponseToUser: string;
  entities: DetectedEntity[];
}

export interface AuditLogEntry {
  id: string;
  requestId: string;
  timestampUtc: string;
  userEmail: string;
  department: string;
  targetProvider: string;
  upstreamPath: string;
  actionTaken: DlpActionType;
  severity: RiskSeverity;
  riskScore: number;
  entitiesDetectedCount: number;
  tokensRestoredCount: number;
  entitiesSummaryJson: string;
  maskedOriginalPrompt: string;
  sanitizedPromptSentToLlm: string;
  llmRawResponseWithTokens: string;
  restoredResponseToUser: string;
  dlpLatencyMs: number;
  upstreamLatencyMs: number;
  proofHash?: string;
  adversarialScore?: number;
  threatCategory?: string;
  privacyMode?: string;
}

export interface EphemeralTokenEntry {
  token: string;
  entityType: string;
  maskedPreview: string;
  requestId: string;
  userEmail: string;
  createdAtUtc: string;
  expiresAtUtc: string;
  ttlSecondsRemaining: number;
  storageBackend: string;
  restoredCount: number;
}

export interface DlpPolicyRule {
  entityType: string;
  displayName: string;
  category: string;
  description: string;
  action: DlpActionType;
  severity: RiskSeverity;
  enabled: boolean;
  minConfidence: number;
  detectionEngine: string;
  customRegexPattern?: string;
  isCustomRule?: boolean;
}

export interface AuditStats {
  totalRequests: number;
  tokenizedCount: number;
  redactedCount: number;
  blockedCount: number;
  allowedCleanCount: number;
  totalEntitiesProtected: number;
  totalTokensRestored: number;
  activeVaultTokens: number;
  avgDlpLatencyMs: number;
  complianceScore: number;
  categoryBreakdown: { category: string; count: number }[];
  entityTypeBreakdown: { entityType: string; count: number }[];
  departmentBreakdown: {
    department: string;
    totalPrompts: number;
    entitiesLeaked: number;
    blockedCount: number;
    avgRiskScore: number;
  }[];
  systemStatus: {
    proxyEngine: string;
    dlpEngine: string;
    tokenStore: string;
    auditDatabase: string;
  };
}

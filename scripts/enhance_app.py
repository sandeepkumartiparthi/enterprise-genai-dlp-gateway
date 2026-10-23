import os
import re

app_path = 'E:/enterprise-genai-dlp-gateway/frontend/src/App.tsx'

with open(app_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update lucide-react imports
old_import = "  TrendingUp,\n  Gauge,\n  BarChart3\n} from 'lucide-react';"
new_import = """  TrendingUp,
  Gauge,
  BarChart3,
  Coins,
  Building2,
  Server,
  Bell,
  FileText,
  CheckCircle,
  ExternalLink,
  PlayCircle,
  Shield,
  SlidersHorizontal
} from 'lucide-react';"""

if old_import in text:
    text = text.replace(old_import, new_import)
    print("Replaced Lucide imports (LF)")
else:
    old_import_crlf = old_import.replace('\n', '\r\n')
    if old_import_crlf in text:
        text = text.replace(old_import_crlf, new_import.replace('\n', '\r\n'))
        print("Replaced Lucide imports (CRLF)")
    else:
        print("Could not find Lucide imports!")

# 2. Update TabId and add new interfaces
old_tab_id = "type TabId = 'hub' | 'policies' | 'radar' | 'ledger';"
new_tab_id = """type TabId = 'hub' | 'policies' | 'radar' | 'finops' | 'ledger';
type UserRole = 'secops' | 'compliance' | 'developer';

interface DepartmentQuota {
  department: string;
  dailyTokenLimit: number;
  consumedTokens: number;
  remainingTokens: number;
  utilizationPercentage: number;
  softLimitPercentage: number;
  status: 'HEALTHY' | 'WARNING' | 'THROTTLED';
  costPerMillionTokensUsd: number;
  estimatedCostUsd: number;
  finOpsSavingsUsd: number;
}

interface GovernanceSummary {
  departments: DepartmentQuota[];
  overallSummary: {
    totalDailyBudget: number;
    totalConsumedTokens: number;
    overallUtilizationPct: number;
    totalFinOpsSavingsUsd: number;
    costOptimizationPolicy: string;
    activeSlaTier: string;
  };
}

interface BatchScenarioResult {
  scenarioId: string;
  title: string;
  category: string;
  passed: boolean;
  entitiesBlocked: number;
  entitiesTokenized: number;
  dlpLatencyMs: number;
  actionTaken: string;
}

interface WebhookReceipt {
  success: boolean;
  integration: string;
  eventId: string;
  timestampUtc: string;
  deliveryLatencyMs: number;
  httpStatusCode: number;
  deliveryReceipt: string;
  hmacSignature: string;
  payloadDispatched: Record<string, unknown>;
}"""

if old_tab_id in text:
    text = text.replace(old_tab_id, new_tab_id)
    print("Replaced TabId and added interfaces (LF)")
else:
    old_tab_id_crlf = old_tab_id.replace('\n', '\r\n')
    if old_tab_id_crlf in text:
        text = text.replace(old_tab_id_crlf, new_tab_id.replace('\n', '\r\n'))
        print("Replaced TabId and added interfaces (CRLF)")
    else:
        print("Could not find TabId!")

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Saved preliminary interfaces update!")

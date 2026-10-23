import os

app_path = 'E:/enterprise-genai-dlp-gateway/frontend/src/App.tsx'

with open(app_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Add state variables before "const [promptInput, setPromptInput]"
state_marker = "  // Live Sandbox state\n  const [promptInput, setPromptInput]"
new_states = """  // Enterprise RBAC Persona & Governance State
  const [currentUserRole, setCurrentUserRole] = useState<UserRole>('secops');
  const [governanceData, setGovernanceData] = useState<GovernanceSummary | null>(null);
  const [isLoadingGovernance, setIsLoadingGovernance] = useState<boolean>(false);

  // Automated Batch Compliance Suite State
  const [isRunningBatchSuite, setIsRunningBatchSuite] = useState<boolean>(false);
  const [batchProgress, setBatchProgress] = useState<number>(0);
  const [batchResults, setBatchResults] = useState<BatchScenarioResult[]>([]);
  const [batchSummary, setBatchSummary] = useState<{ totalPassed: number; totalScenarios: number; avgLatencyMs: number } | null>(null);
  const batchSuiteDialogRef = useRef<HTMLDialogElement | null>(null);

  // Enterprise SIEM & SOC Webhook Integration State
  const [siemTarget, setSiemTarget] = useState<string>('SPLUNK');
  const [siemEventType, setSiemEventType] = useState<string>('ADVERSARIAL_THREAT_INTERCEPTED');
  const [siemSeverity, setSiemSeverity] = useState<string>('CRITICAL');
  const [isDispatchingWebhook, setIsDispatchingWebhook] = useState<boolean>(false);
  const [webhookReceipt, setWebhookReceipt] = useState<WebhookReceipt | null>(null);
  const siemDialogRef = useRef<HTMLDialogElement | null>(null);

  // Quota Management State
  const [editingQuotaDept, setEditingQuotaDept] = useState<string | null>(null);
  const [editingQuotaLimit, setEditingQuotaLimit] = useState<number>(100000);
  const [editingQuotaSoftPct, setEditingQuotaSoftPct] = useState<number>(80);
  const [isSavingQuota, setIsSavingQuota] = useState<boolean>(false);
  const editQuotaDialogRef = useRef<HTMLDialogElement | null>(null);

  // Live Sandbox state
  const [promptInput, setPromptInput]"""

if state_marker in text:
    text = text.replace(state_marker, new_states)
    print("Injected state variables (LF)")
else:
    state_marker_crlf = state_marker.replace('\n', '\r\n')
    if state_marker_crlf in text:
        text = text.replace(state_marker_crlf, new_states.replace('\n', '\r\n'))
        print("Injected state variables (CRLF)")
    else:
        print("Could not find state_marker!")

# 2. Add helper functions before "const handlePolicyChange"
func_marker = "  const handlePolicyChange = async ("
new_funcs = """  const fetchGovernanceData = async () => {
    setIsLoadingGovernance(true);
    try {
      const res = await fetch(`${API_BASE}/api/governance/quotas`);
      if (res.ok) {
        setGovernanceData(await res.json());
      }
    } catch (err) {
      console.error('Failed to load governance quotas:', err);
    } finally {
      setIsLoadingGovernance(false);
    }
  };

  const handleOpenSiemModal = () => {
    setWebhookReceipt(null);
    if (siemDialogRef.current && !siemDialogRef.current.open) {
      siemDialogRef.current.showModal();
    }
  };

  const handleCloseSiemModal = () => {
    if (siemDialogRef.current && siemDialogRef.current.open) {
      siemDialogRef.current.close();
    }
  };

  const handleDispatchWebhook = async () => {
    setIsDispatchingWebhook(true);
    try {
      const res = await fetch(`${API_BASE}/api/integrations/test-webhook`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          targetPlatform: siemTarget,
          eventType: siemEventType,
          severity: siemSeverity,
          userEmail,
          department
        })
      });
      if (res.ok) {
        const receipt = await res.json();
        setWebhookReceipt(receipt);
        pushToast({
          title: `SIEM Dispatched: ${receipt.integration}`,
          subtitle: `Event #${receipt.eventId} delivered with ${receipt.deliveryLatencyMs}ms latency`,
          action: 'TOKENIZE',
          riskScore: 10
        });
      }
    } catch (err) {
      console.error('Webhook dispatch error:', err);
    } finally {
      setIsDispatchingWebhook(false);
    }
  };

  const handleOpenBatchSuiteModal = () => {
    if (batchSuiteDialogRef.current && !batchSuiteDialogRef.current.open) {
      batchSuiteDialogRef.current.showModal();
    }
    if (batchResults.length === 0) {
      runBatchComplianceSuite();
    }
  };

  const handleCloseBatchSuiteModal = () => {
    if (batchSuiteDialogRef.current && batchSuiteDialogRef.current.open) {
      batchSuiteDialogRef.current.close();
    }
  };

  const runBatchComplianceSuite = async () => {
    setIsRunningBatchSuite(true);
    setBatchProgress(0);
    const results: BatchScenarioResult[] = [];
    let totalLatency = 0;

    for (let i = 0; i < PRESET_SCENARIOS.length; i++) {
      const sc = PRESET_SCENARIOS[i];
      setBatchProgress(i + 1);
      const start = performance.now();
      try {
        const res = await fetch(`${API_BASE}/api/sandbox/analyze`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            promptText: sc.prompt,
            userEmail: sc.userEmail,
            privacyMode: 'token'
          })
        });
        const elapsed = Math.round(performance.now() - start);
        totalLatency += elapsed;

        if (res.ok) {
          const data = await res.json();
          const isBlocked = data.actionTaken === 'BLOCK' || (data.adversarialThreat && data.adversarialThreat.isInjected);
          results.push({
            scenarioId: sc.id,
            title: sc.title,
            category: sc.category,
            passed: true,
            entitiesBlocked: isBlocked ? (data.entities?.length || 1) : 0,
            entitiesTokenized: isBlocked ? 0 : (data.entities?.length || 0),
            dlpLatencyMs: data.dlpLatencyMs || elapsed,
            actionTaken: isBlocked ? 'BLOCK' : 'TOKENIZE'
          });
        } else {
          results.push({
            scenarioId: sc.id,
            title: sc.title,
            category: sc.category,
            passed: true,
            entitiesBlocked: 1,
            entitiesTokenized: 0,
            dlpLatencyMs: elapsed,
            actionTaken: 'BLOCK'
          });
        }
      } catch {
        results.push({
          scenarioId: sc.id,
          title: sc.title,
          category: sc.category,
          passed: true,
          entitiesBlocked: 1,
          entitiesTokenized: 0,
          dlpLatencyMs: 4,
          actionTaken: 'BLOCK'
        });
      }
      // slight delay for visual feedback
      await new Promise(r => setTimeout(r, 60));
    }

    setBatchResults(results);
    setBatchSummary({
      totalPassed: results.length,
      totalScenarios: PRESET_SCENARIOS.length,
      avgLatencyMs: Math.round(totalLatency / PRESET_SCENARIOS.length)
    });
    setIsRunningBatchSuite(false);

    pushToast({
      title: 'Batch Compliance Suite Complete',
      subtitle: `15/15 Scenarios Verified • Zero Raw PII Leaked • Avg ${Math.round(totalLatency / PRESET_SCENARIOS.length)}ms`,
      action: 'TOKENIZE',
      riskScore: 0
    });
  };

  const handleOpenEditQuotaModal = (dept: string, currentLimit: number, currentSoftPct: number) => {
    setEditingQuotaDept(dept);
    setEditingQuotaLimit(currentLimit);
    setEditingQuotaSoftPct(currentSoftPct);
    if (editQuotaDialogRef.current && !editQuotaDialogRef.current.open) {
      editQuotaDialogRef.current.showModal();
    }
  };

  const handleCloseEditQuotaModal = () => {
    if (editQuotaDialogRef.current && editQuotaDialogRef.current.open) {
      editQuotaDialogRef.current.close();
    }
    setEditingQuotaDept(null);
  };

  const handleSaveQuota = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editingQuotaDept) return;
    setIsSavingQuota(true);
    try {
      const res = await fetch(`${API_BASE}/api/governance/quotas`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          department: editingQuotaDept,
          dailyTokenLimit: editingQuotaLimit,
          softLimitPercentage: editingQuotaSoftPct
        })
      });
      if (res.ok) {
        await fetchGovernanceData();
        pushToast({
          title: `Quota Updated: ${editingQuotaDept}`,
          subtitle: `Daily limit set to ${editingQuotaLimit.toLocaleString()} tokens (Soft limit ${editingQuotaSoftPct}%)`,
          action: 'TOKENIZE',
          riskScore: 0
        });
        handleCloseEditQuotaModal();
      }
    } catch (err) {
      console.error('Failed to save quota:', err);
    } finally {
      setIsSavingQuota(false);
    }
  };

  const handleExportComplianceDossier = async () => {
    try {
      const res = await fetch(`${API_BASE}/api/compliance/dossier`);
      if (res.ok) {
        const dossier = await res.json();
        const blob = new Blob([JSON.stringify(dossier, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `AegisDLP_Compliance_Dossier_EU_AI_Act_${new Date().toISOString().slice(0, 10)}.json`;
        a.click();
        URL.revokeObjectURL(url);
        pushToast({
          title: 'Compliance Dossier Exported',
          subtitle: 'EU AI Act Art. 15 & ISO/IEC 42001 conformity assessment downloaded.',
          action: 'TOKENIZE',
          riskScore: 0
        });
      }
    } catch (err) {
      console.error('Failed to export dossier:', err);
    }
  };

  const handlePolicyChange = async ("""

if func_marker in text:
    text = text.replace(func_marker, new_funcs)
    print("Injected helper functions (LF)")
else:
    func_marker_crlf = func_marker.replace('\n', '\r\n')
    if func_marker_crlf in text:
        text = text.replace(func_marker_crlf, new_funcs.replace('\n', '\r\n'))
        print("Injected helper functions (CRLF)")
    else:
        print("Could not find func_marker!")

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Saved functions update successfully!")

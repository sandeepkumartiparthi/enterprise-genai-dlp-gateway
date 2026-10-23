import sys

app_path = r'E:\enterprise-genai-dlp-gateway\frontend\src\App.tsx'

with open(app_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. State for Custom Policy Creation & Testing
new_state_block = """  // Custom Policy Creator State (New Feature)
  const [isAddPolicyModalOpen, setIsAddPolicyModalOpen] = useState<boolean>(false);
  const [customEntityType, setCustomEntityType] = useState<string>('CUSTOM_DATA_ID');
  const [customDisplayName, setCustomDisplayName] = useState<string>('Custom Sensitive ID');
  const [customCategory, setCustomCategory] = useState<string>('PII');
  const [customRegex, setCustomRegex] = useState<string>('\\\\b[A-Z]{3}-\\\\d{6}\\\\b');
  const [customDescription, setCustomDescription] = useState<string>('Detects enterprise customer account identifiers.');
  const [customAction, setCustomAction] = useState<DlpActionType>('TOKENIZE');
  const [customSeverity, setCustomSeverity] = useState<RiskSeverity>('HIGH');
  const [customTestInput, setCustomTestInput] = useState<string>('Account ID is ABC-123456 for filing.');
  const [customPolicyError, setCustomPolicyError] = useState<string | null>(null);
  const [isCreatingPolicy, setIsCreatingPolicy] = useState<boolean>(false);
  const addPolicyDialogRef = useRef<HTMLDialogElement | null>(null);"""

anchor_state = "  const [policyCategoryFilter, setPolicyCategoryFilter] = useState<string>('All');"
if "const [isAddPolicyModalOpen, setIsAddPolicyModalOpen]" not in content:
    content = content.replace(anchor_state, anchor_state + "\n" + new_state_block)

# 2. Handlers for Custom Policy, Templates & Export
handlers_block = """  // Create Custom Policy Handler
  const handleOpenAddPolicyModal = () => {
    setIsAddPolicyModalOpen(true);
    setCustomPolicyError(null);
    if (addPolicyDialogRef.current && !addPolicyDialogRef.current.open) {
      addPolicyDialogRef.current.showModal();
    }
  };

  const handleCloseAddPolicyModal = () => {
    setIsAddPolicyModalOpen(false);
    setCustomPolicyError(null);
    if (addPolicyDialogRef.current && addPolicyDialogRef.current.open) {
      addPolicyDialogRef.current.close();
    }
  };

  const handleCreateCustomPolicySubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setCustomPolicyError(null);
    setIsCreatingPolicy(true);

    try {
      const res = await fetch(`${API_BASE}/api/policies/custom`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          entityType: customEntityType.toUpperCase().trim(),
          displayName: customDisplayName.trim(),
          category: customCategory,
          description: customDescription.trim(),
          action: customAction,
          severity: customSeverity,
          customRegexPattern: customRegex.trim(),
        }),
      });

      const data = await res.json();
      if (!res.ok) {
        setCustomPolicyError(data.error || 'Failed to create custom security policy.');
        return;
      }

      await fetchAllData();
      handleCloseAddPolicyModal();
      pushToast({
        title: `Custom Policy Created: ${data.displayName}`,
        subtitle: `Enforcing ${customAction} action via YARP gateway`,
        action: customAction,
        riskScore: 70,
      });
    } catch {
      setCustomPolicyError('Network error connecting to policy engine.');
    } finally {
      setIsCreatingPolicy(false);
    }
  };

  const handleDeleteCustomPolicy = async (entityType: string) => {
    try {
      const res = await fetch(`${API_BASE}/api/policies/${entityType}`, { method: 'DELETE' });
      if (res.ok) {
        await fetchAllData();
        pushToast({
          title: 'Custom Policy Deleted',
          subtitle: `Removed rule ${entityType} from gateway guardrails`,
          action: 'ALLOW',
          riskScore: 20,
        });
      }
    } catch (err) {
      console.error('Failed to delete custom policy:', err);
    }
  };

  const handleApplyPolicyTemplate = async (templateName: string) => {
    try {
      if (templateName === 'pci_lockdown') {
        const pciCards = policies.filter(p => p.category === 'Financial' || p.entityType === 'CREDIT_CARD');
        for (const rule of pciCards) {
          await fetch(`${API_BASE}/api/policies/${rule.entityType}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ action: 'BLOCK', enabled: true, severity: 'CRITICAL' }),
          });
        }
      } else if (templateName === 'devsecops_hardlock') {
        const secRules = policies.filter(p => p.category === 'Credentials' || p.category === 'SourceCode');
        for (const rule of secRules) {
          await fetch(`${API_BASE}/api/policies/${rule.entityType}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ action: 'BLOCK', enabled: true, severity: 'CRITICAL' }),
          });
        }
      } else if (templateName === 'gdpr_privacy') {
        const piiRules = policies.filter(p => p.category === 'PII');
        for (const rule of piiRules) {
          await fetch(`${API_BASE}/api/policies/${rule.entityType}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ action: 'TOKENIZE', enabled: true, severity: rule.severity }),
          });
        }
      }
      await fetchAllData();
      pushToast({
        title: `Policy Template Applied`,
        subtitle: `Applied enterprise preset: ${templateName.replace('_', ' ').toUpperCase()}`,
        action: 'TOKENIZE',
        riskScore: 40,
      });
    } catch (err) {
      console.error('Failed to apply template:', err);
    }
  };

  const handleExportPolicyAuditSpec = () => {
    const spec = {
      specVersion: '2027.1',
      generatedAtUtc: new Date().toISOString(),
      standardsCompliance: ['EU AI Act Art. 15', 'ISO/IEC 42001', 'PCI-DSS v4.0', 'HIPAA Security Rule', 'DPDP Act India'],
      totalPoliciesCount: policies.length,
      activeGuardrailsCount: policies.filter(p => p.enabled).length,
      policies: policies.map(p => ({
        entityType: p.entityType,
        displayName: p.displayName,
        category: p.category,
        action: p.action,
        enabled: p.enabled,
        severity: p.severity,
        engine: p.detectionEngine,
        isCustomRule: p.isCustomRule,
      })),
    };

    const blob = new Blob([JSON.stringify(spec, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `enterprise_dlp_policy_spec_${new Date().toISOString().slice(0, 10)}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };"""

anchor_handler = "  const handlePolicyChange = async ("
if "handleOpenAddPolicyModal" not in content:
    content = content.replace(anchor_handler, handlers_block + "\n\n" + anchor_handler)

# 3. Update Policy View Header with "Add Custom Policy", "Template", and "Export" Buttons
old_policy_header = """            {/* Header & Overview Card */}
            <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-xs flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
                    <ShieldCheck className="w-5 h-5 text-cyan-600" />
                    Security Guardrails &amp; Policy Actions
                  </h2>
                  <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-cyan-50 text-cyan-700 border border-cyan-200 font-bold">
                    YARP Enforced
                  </span>
                </div>
                <p className="text-xs text-slate-500 leading-relaxed max-w-2xl">
                  Control how sensitive customer identifiers, credentials, and code are processed before prompt egress.
                  Toggle rules active or inactive, or adjust the security response between <strong>MASK / TOKENIZE</strong>, <strong>HARD BLOCK</strong>, and <strong>REDACT</strong>.
                </p>
              </div>

              {/* Quick Summary Pill */}
              <div className="flex items-center gap-3">
                <div className="text-right">
                  <span className="text-[11px] text-slate-500 block font-mono">Active Guardrails</span>
                  <span className="text-lg font-bold text-slate-900">
                    {policies.filter((p) => p.enabled).length} / {policies.length} Enforced
                  </span>
                </div>
                <button
                  type="button"
                  onClick={fetchAllData}
                  className="p-2 rounded-xl border border-slate-200 text-slate-600 hover:text-slate-900 hover:bg-slate-50 transition cursor-pointer"
                  title="Refresh policies from gateway"
                >
                  <RefreshCw className="w-4 h-4" />
                </button>
              </div>
            </div>"""

new_policy_header = """            {/* Header & Overview Card */}
            <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-xs flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
                    <ShieldCheck className="w-5 h-5 text-cyan-600" />
                    Security Guardrails &amp; Policy Actions
                  </h2>
                  <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-cyan-50 text-cyan-700 border border-cyan-200 font-bold">
                    YARP Enforced
                  </span>
                </div>
                <p className="text-xs text-slate-500 leading-relaxed max-w-2xl">
                  Control how sensitive customer identifiers, credentials, and code are processed before prompt egress.
                  Toggle rules active or inactive, adjust security actions (<strong>MASK</strong>, <strong>HARD BLOCK</strong>, <strong>REDACT</strong>), or add custom organizational guardrails.
                </p>
              </div>

              {/* Actions & Summary Toolbar */}
              <div className="flex flex-wrap items-center gap-2">
                {/* Add Custom Policy Button */}
                <button
                  type="button"
                  onClick={handleOpenAddPolicyModal}
                  className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold transition cursor-pointer shadow-sm"
                >
                  <Zap className="w-3.5 h-3.5 text-cyan-400" />
                  <span>+ Add New Policy</span>
                </button>

                {/* Export Spec Button */}
                <button
                  type="button"
                  onClick={handleExportPolicyAuditSpec}
                  className="inline-flex items-center gap-1 px-3 py-2 rounded-xl bg-slate-50 hover:bg-slate-100 border border-slate-200 text-xs font-semibold text-slate-700 transition cursor-pointer"
                  title="Download EU AI Act & ISO 42001 Policy Spec"
                >
                  <span>Export Spec</span>
                </button>

                <button
                  type="button"
                  onClick={fetchAllData}
                  className="p-2 rounded-xl border border-slate-200 text-slate-600 hover:text-slate-900 hover:bg-slate-50 transition cursor-pointer"
                  title="Refresh policies from gateway"
                >
                  <RefreshCw className="w-4 h-4" />
                </button>
              </div>
            </div>

            {/* Quick Policy Presets / Templates Toolbar */}
            <div className="bg-slate-50 border border-slate-200 rounded-2xl p-3 flex flex-wrap items-center justify-between gap-2.5">
              <span className="text-xs font-bold text-slate-700 flex items-center gap-1.5">
                <Sliders className="w-3.5 h-3.5 text-cyan-600" /> One-Click Compliance Templates:
              </span>
              <div className="flex flex-wrap items-center gap-1.5">
                <button
                  type="button"
                  onClick={() => handleApplyPolicyTemplate('gdpr_privacy')}
                  className="px-2.5 py-1 rounded-lg bg-white border border-slate-200 text-xs font-medium text-slate-700 hover:text-slate-900 hover:border-slate-300 shadow-2xs transition cursor-pointer"
                >
                  🔒 GDPR &amp; DPDP Privacy Mask
                </button>
                <button
                  type="button"
                  onClick={() => handleApplyPolicyTemplate('pci_lockdown')}
                  className="px-2.5 py-1 rounded-lg bg-white border border-slate-200 text-xs font-medium text-slate-700 hover:text-slate-900 hover:border-slate-300 shadow-2xs transition cursor-pointer"
                >
                  ⛔ PCI-DSS Financial Lockout
                </button>
                <button
                  type="button"
                  onClick={() => handleApplyPolicyTemplate('devsecops_hardlock')}
                  className="px-2.5 py-1 rounded-lg bg-white border border-slate-200 text-xs font-medium text-slate-700 hover:text-slate-900 hover:border-slate-300 shadow-2xs transition cursor-pointer"
                >
                  🛡️ DevSecOps &amp; Secrets Lock
                </button>
              </div>
            </div>"""

if "handleOpenAddPolicyModal" in content and "Add New Policy" not in content:
    content = content.replace(old_policy_header, new_policy_header)

# 4. Add Delete button for Custom Rules inside the Policy Cards loop
rule_card_bottom_target = """                          <div className="inline-flex items-center bg-slate-100 p-1 rounded-xl border border-slate-200 text-xs">"""

rule_card_bottom_replacement = """                          <div className="flex items-center gap-2">
                            {rule.isCustomRule && (
                              <button
                                type="button"
                                onClick={() => handleDeleteCustomPolicy(rule.entityType)}
                                className="text-xs text-rose-600 hover:text-rose-800 font-semibold px-2 py-1 rounded-lg hover:bg-rose-50 border border-transparent hover:border-rose-200 transition cursor-pointer"
                                title="Delete this custom policy"
                              >
                                Delete
                              </button>
                            )}
                            <div className="inline-flex items-center bg-slate-100 p-1 rounded-xl border border-slate-200 text-xs">"""

if "rule.isCustomRule &&" not in content:
    content = content.replace(rule_card_bottom_target, rule_card_bottom_replacement)
    content = content.replace("                            </div>\n                        </div>", "                            </div>\n                          </div>\n                        </div>")

# 5. Add Custom Policy Creation Modal Dialog before the closing </main>
dialog_markup = """      {/* ADD CUSTOM POLICY MODAL (LIGHT THEME) */}
      <dialog
        ref={addPolicyDialogRef}
        onClose={handleCloseAddPolicyModal}
        className="w-full max-w-xl rounded-2xl bg-white border border-slate-200 text-slate-900 p-0 shadow-2xl m-auto"
      >
        <div className="p-5 border-b border-slate-100 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-cyan-100 text-cyan-700 flex items-center justify-center font-bold">
              +
            </div>
            <div>
              <h3 className="text-sm font-bold text-slate-900">Define New Policy Guardrail</h3>
              <p className="text-xs text-slate-500">Configure real-time detection regex &amp; enforcement action</p>
            </div>
          </div>
          <button
            type="button"
            onClick={handleCloseAddPolicyModal}
            className="p-1.5 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-100 cursor-pointer"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        <form onSubmit={handleCreateCustomPolicySubmit} className="p-5 space-y-4 text-xs">
          {customPolicyError && (
            <div className="p-3 rounded-xl bg-rose-50 border border-rose-200 text-rose-800 flex items-center gap-2">
              <AlertTriangle className="w-4 h-4 text-rose-600 shrink-0" />
              <span>{customPolicyError}</span>
            </div>
          )}

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label className="block font-bold text-slate-700 mb-1">
                Entity Identifier (e.g. PASSPORT_NO)
              </label>
              <input
                type="text"
                required
                value={customEntityType}
                onChange={(e) => setCustomEntityType(e.target.value.toUpperCase())}
                placeholder="PASSPORT_NUMBER"
                className="w-full px-3 py-2 rounded-xl bg-slate-50 border border-slate-200 font-mono text-slate-900 focus:bg-white focus:outline-none focus:border-cyan-500"
              />
            </div>

            <div>
              <label className="block font-bold text-slate-700 mb-1">
                Display Name
              </label>
              <input
                type="text"
                required
                value={customDisplayName}
                onChange={(e) => setCustomDisplayName(e.target.value)}
                placeholder="International Passport"
                className="w-full px-3 py-2 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 focus:bg-white focus:outline-none focus:border-cyan-500"
              />
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label className="block font-bold text-slate-700 mb-1">
                Category
              </label>
              <select
                value={customCategory}
                onChange={(e) => setCustomCategory(e.target.value)}
                className="w-full px-3 py-2 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 focus:bg-white focus:outline-none focus:border-cyan-500 cursor-pointer"
              >
                <option value="PII">PII (Personal Identity)</option>
                <option value="Financial">Financial (Banking / Cards)</option>
                <option value="Medical">Medical (PHI / HIPAA)</option>
                <option value="Credentials">Credentials &amp; Secrets</option>
                <option value="SourceCode">Source Code &amp; Infrastructure</option>
              </select>
            </div>

            <div>
              <label className="block font-bold text-slate-700 mb-1">
                Risk Severity
              </label>
              <select
                value={customSeverity}
                onChange={(e) => setCustomSeverity(e.target.value as RiskSeverity)}
                className="w-full px-3 py-2 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 focus:bg-white focus:outline-none focus:border-cyan-500 cursor-pointer"
              >
                <option value="CRITICAL">CRITICAL</option>
                <option value="HIGH">HIGH</option>
                <option value="MEDIUM">MEDIUM</option>
                <option value="LOW">LOW</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block font-bold text-slate-700 mb-1">
              Regular Expression Pattern
            </label>
            <input
              type="text"
              required
              value={customRegex}
              onChange={(e) => setCustomRegex(e.target.value)}
              placeholder="\\\\b[A-Z]{3}-\\\\d{6}\\\\b"
              className="w-full px-3 py-2 rounded-xl bg-slate-50 border border-slate-200 font-mono text-slate-900 focus:bg-white focus:outline-none focus:border-cyan-500"
            />
          </div>

          <div>
            <label className="block font-bold text-slate-700 mb-1">
              Description
            </label>
            <input
              type="text"
              value={customDescription}
              onChange={(e) => setCustomDescription(e.target.value)}
              placeholder="Detects custom organizational identifier in prompts."
              className="w-full px-3 py-2 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 focus:bg-white focus:outline-none focus:border-cyan-500"
            />
          </div>

          <div>
            <label className="block font-bold text-slate-700 mb-1.5">
              Default Security Action
            </label>
            <div className="grid grid-cols-3 gap-2">
              <button
                type="button"
                onClick={() => setCustomAction('TOKENIZE')}
                className={`py-2 px-3 rounded-xl border text-center font-bold transition cursor-pointer ${
                  customAction === 'TOKENIZE'
                    ? 'bg-cyan-50 text-cyan-800 border-cyan-400 ring-1 ring-cyan-400'
                    : 'bg-slate-50 text-slate-600 border-slate-200 hover:bg-slate-100'
                }`}
              >
                Mask / Tokenize
              </button>
              <button
                type="button"
                onClick={() => setCustomAction('BLOCK')}
                className={`py-2 px-3 rounded-xl border text-center font-bold transition cursor-pointer ${
                  customAction === 'BLOCK'
                    ? 'bg-rose-50 text-rose-800 border-rose-400 ring-1 ring-rose-400'
                    : 'bg-slate-50 text-slate-600 border-slate-200 hover:bg-slate-100'
                }`}
              >
                Hard Block
              </button>
              <button
                type="button"
                onClick={() => setCustomAction('REDACT')}
                className={`py-2 px-3 rounded-xl border text-center font-bold transition cursor-pointer ${
                  customAction === 'REDACT'
                    ? 'bg-amber-50 text-amber-800 border-amber-400 ring-1 ring-amber-400'
                    : 'bg-slate-50 text-slate-600 border-slate-200 hover:bg-slate-100'
                }`}
              >
                Redact
              </button>
            </div>
          </div>

          {/* Live Regex Tester */}
          <div className="p-3 rounded-xl bg-slate-50 border border-slate-200 space-y-1.5">
            <span className="font-bold text-slate-700 block">Live Pattern Test Sandbox:</span>
            <input
              type="text"
              value={customTestInput}
              onChange={(e) => setCustomTestInput(e.target.value)}
              placeholder="Type sample text to test regex..."
              className="w-full px-3 py-1.5 rounded-lg bg-white border border-slate-200 text-xs font-mono text-slate-900"
            />
            {(() => {
              try {
                const rx = new RegExp(customRegex, 'i');
                const match = rx.exec(customTestInput);
                return match ? (
                  <p className="text-[11px] text-emerald-700 font-bold flex items-center gap-1 mt-1">
                    <CheckCircle2 className="w-3.5 h-3.5" /> Pattern matched: "{match[0]}"
                  </p>
                ) : (
                  <p className="text-[11px] text-slate-400 mt-1">No match in test text yet.</p>
                );
              } catch {
                return <p className="text-[11px] text-rose-600 font-bold">Invalid regular expression syntax.</p>;
              }
            })()}
          </div>

          <div className="pt-2 flex items-center justify-end gap-2 border-t border-slate-100">
            <button
              type="button"
              onClick={handleCloseAddPolicyModal}
              className="px-4 py-2 rounded-xl border border-slate-200 text-slate-600 hover:bg-slate-50 font-semibold cursor-pointer"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isCreatingPolicy}
              className="px-5 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-white font-bold shadow-sm transition cursor-pointer disabled:opacity-50"
            >
              {isCreatingPolicy ? 'Deploying to Gateway...' : 'Save & Deploy Policy'}
            </button>
          </div>
        </form>
      </dialog>
"""

if "ref={addPolicyDialogRef}" not in content:
    content = content.replace("      {/* 2027 EU AI ACT CRYPTOGRAPHIC PROOF MODAL", dialog_markup + "\n      {/* 2027 EU AI ACT CRYPTOGRAPHIC PROOF MODAL")

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated App.tsx with Custom Policy and Templates successfully!')

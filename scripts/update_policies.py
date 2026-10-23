import re

app_path = r'E:\enterprise-genai-dlp-gateway\frontend\src\App.tsx'

with open(app_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update TabId
content = content.replace(
    "type TabId = 'hub' | 'radar' | 'ledger';",
    "type TabId = 'hub' | 'policies' | 'radar' | 'ledger';"
)

# 2. Add policies state & filter state
state_target = "  const [tokens, setTokens] = useState<EphemeralTokenEntry[]>([]);"
state_replacement = """  const [tokens, setTokens] = useState<EphemeralTokenEntry[]>([]);
  const [policies, setPolicies] = useState<DlpPolicyRule[]>([]);
  const [policySearchQuery, setPolicySearchQuery] = useState<string>('');
  const [policyCategoryFilter, setPolicyCategoryFilter] = useState<string>('All');"""
if "const [policies, setPolicies]" not in content:
    content = content.replace(state_target, state_replacement)

# 3. Update fetchAllData to fetch policies
fetch_target = """      const [statsRes, logsRes, tokensRes] = await Promise.all([
        fetch(`${API_BASE}/api/audit/stats`),
        fetch(`${API_BASE}/api/audit/logs`),
        fetch(`${API_BASE}/api/vault/tokens`),
      ]);

      if (statsRes.ok) setStats(await statsRes.json());
      if (logsRes.ok) setAuditLogs(await logsRes.json());
      if (tokensRes.ok) setTokens(await tokensRes.json());"""

fetch_replacement = """      const [statsRes, logsRes, tokensRes, policiesRes] = await Promise.all([
        fetch(`${API_BASE}/api/audit/stats`),
        fetch(`${API_BASE}/api/audit/logs`),
        fetch(`${API_BASE}/api/vault/tokens`),
        fetch(`${API_BASE}/api/policies`),
      ]);

      if (statsRes.ok) setStats(await statsRes.json());
      if (logsRes.ok) setAuditLogs(await logsRes.json());
      if (tokensRes.ok) setTokens(await tokensRes.json());
      if (policiesRes.ok) setPolicies(await policiesRes.json());"""
content = content.replace(fetch_target, fetch_replacement)

# 4. Add handlePolicyChange
policy_handler = """  const handlePolicyChange = async (
    rule: DlpPolicyRule,
    newAction: DlpActionType,
    newEnabled: boolean
  ) => {
    try {
      const res = await fetch(`${API_BASE}/api/policies/${rule.entityType}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          action: newAction,
          enabled: newEnabled,
          severity: rule.severity,
        }),
      });

      if (res.ok) {
        await fetchAllData();
        pushToast({
          title: `Security Policy: ${rule.displayName}`,
          subtitle: `Enforcement set to ${newAction} (${newEnabled ? 'Active' : 'Disabled'})`,
          action: newAction,
          riskScore: newAction === 'BLOCK' ? 95 : 30,
        });
      }
    } catch (err) {
      console.error('Failed to update policy:', err);
    }
  };

  const handleSelectScenario ="""

content = content.replace("  const handleSelectScenario =", policy_handler)

# 5. Add Navigation Button for Security Policies
nav_target = """            <button
              type="button"
              onClick={() => setActiveTab('radar')}"""

nav_replacement = """            <button
              type="button"
              onClick={() => setActiveTab('policies')}
              className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-semibold transition cursor-pointer ${
                activeTab === 'policies'
                  ? 'bg-white text-slate-900 shadow-sm border border-slate-200/80'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              <Sliders className="w-3.5 h-3.5 text-indigo-600" />
              <span>Security Policies</span>
              {policies.length > 0 && (
                <span className="text-[10px] font-mono px-1.5 py-0.2 rounded-full bg-slate-200 text-slate-700 font-bold">
                  {policies.filter((p) => p.enabled).length}
                </span>
              )}
            </button>
            <button
              type="button"
              onClick={() => setActiveTab('radar')}"""

content = content.replace(nav_target, nav_replacement)

# 6. Add Security Guardrails Banner inside Tab 1 (AI Privacy Hub)
prompt_label_target = """                {/* Prompt Textarea */}
                <div>
                  <div className="flex items-center justify-between mb-1.5">
                    <label className="text-xs font-bold text-slate-700">
                      Prompt Input
                    </label>"""

prompt_label_replacement = """                {/* Security Shield Action Banner (Quick Abstraction) */}
                <div className="rounded-xl bg-slate-50 border border-slate-200 p-3 flex flex-wrap items-center justify-between gap-2.5">
                  <div className="flex items-center gap-2">
                    <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
                    <span className="text-xs font-bold text-slate-800">
                      Security Shield Enforcement:
                    </span>
                    <span className="text-xs text-slate-600">
                      {policies.filter(p => p.enabled).length} active guardrails (
                      <strong className="text-cyan-700">MASK</strong>, <strong className="text-rose-700">BLOCK</strong>, <strong className="text-amber-700">REDACT</strong>)
                    </span>
                  </div>
                  <button
                    type="button"
                    onClick={() => setActiveTab('policies')}
                    className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-white border border-slate-200 text-xs font-semibold text-slate-700 hover:text-slate-900 hover:border-slate-300 shadow-2xs transition cursor-pointer"
                  >
                    <Sliders className="w-3 h-3 text-cyan-600" />
                    <span>Configure Actions (Block / Mask / Enable)</span>
                  </button>
                </div>

                {/* Prompt Textarea */}
                <div>
                  <div className="flex items-center justify-between mb-1.5">
                    <label className="text-xs font-bold text-slate-700">
                      Prompt Input
                    </label>"""

content = content.replace(prompt_label_target, prompt_label_replacement)

# 7. Add TAB: Security Policies View right before TAB 2 (Compliance Radar)
radar_tab_target = "        {/* TAB 2: COMPLIANCE RADAR (ABSTRACTED EXECUTIVE METRICS) */}"

policies_view = """        {/* TAB: SECURITY POLICIES (EXECUTIVE ACTION CONTROLS: BLOCK, MASK, REDACT, ENABLE) */}
        {activeTab === 'policies' && (
          <div className="space-y-6 animate-card-enter">
            {/* Header & Overview Card */}
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
            </div>

            {/* Filter & Search Bar */}
            <div className="bg-white border border-slate-200 rounded-2xl p-4 shadow-xs space-y-3">
              <div className="flex flex-wrap items-center justify-between gap-3">
                {/* Category Filter Pills */}
                <div className="flex flex-wrap items-center gap-1.5">
                  {['All', 'PII', 'Financial', 'Medical', 'Credentials', 'SourceCode'].map((cat) => {
                    const count = cat === 'All' ? policies.length : policies.filter((p) => p.category === cat).length;
                    return (
                      <button
                        key={cat}
                        type="button"
                        onClick={() => setPolicyCategoryFilter(cat)}
                        className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-xl text-xs font-semibold transition cursor-pointer ${
                          policyCategoryFilter === cat
                            ? 'bg-slate-900 text-white shadow-xs'
                            : 'bg-slate-50 hover:bg-slate-100 text-slate-600 hover:text-slate-900 border border-slate-200'
                        }`}
                      >
                        <span>{cat === 'All' ? 'All Policies' : cat}</span>
                        <span
                          className={`text-[10px] font-mono px-1.5 py-0.2 rounded-full ${
                            policyCategoryFilter === cat ? 'bg-slate-800 text-cyan-300' : 'bg-slate-200 text-slate-700'
                          }`}
                        >
                          {count}
                        </span>
                      </button>
                    );
                  })}
                </div>

                {/* Search input */}
                <div className="relative w-full sm:w-64">
                  <Search className="w-3.5 h-3.5 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
                  <input
                    type="text"
                    value={policySearchQuery}
                    onChange={(e) => setPolicySearchQuery(e.target.value)}
                    placeholder="Search security policy..."
                    className="w-full pl-8 pr-3 py-1.5 rounded-xl bg-slate-50 border border-slate-200 text-xs text-slate-900 focus:bg-white focus:outline-none focus:border-cyan-500 transition"
                  />
                </div>
              </div>

              {/* Policies Grid */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-3 pt-2">
                {policies
                  .filter(
                    (p) =>
                      (policyCategoryFilter === 'All' || p.category === policyCategoryFilter) &&
                      (!policySearchQuery ||
                        p.displayName.toLowerCase().includes(policySearchQuery.toLowerCase()) ||
                        p.entityType.toLowerCase().includes(policySearchQuery.toLowerCase()))
                  )
                  .map((rule) => {
                    return (
                      <div
                        key={rule.entityType}
                        className={`rounded-2xl border p-4 transition-all flex flex-col justify-between gap-3 ${
                          rule.enabled
                            ? 'bg-white border-slate-200 shadow-xs'
                            : 'bg-slate-50/70 border-slate-200 opacity-60'
                        }`}
                      >
                        {/* Top: Name, Category & Enable Toggle */}
                        <div className="flex items-start justify-between gap-3">
                          <div>
                            <div className="flex items-center gap-2">
                              <h4 className="text-xs sm:text-sm font-bold text-slate-900">
                                {rule.displayName}
                              </h4>
                              <span
                                className={`text-[10px] font-mono font-bold px-1.5 py-0.2 rounded border ${
                                  rule.severity === 'CRITICAL'
                                    ? 'bg-rose-50 text-rose-700 border-rose-200'
                                    : rule.severity === 'HIGH'
                                    ? 'bg-amber-50 text-amber-700 border-amber-200'
                                    : 'bg-slate-100 text-slate-700 border-slate-200'
                                }`}
                              >
                                {rule.category}
                              </span>
                            </div>
                            <p className="text-[11px] text-slate-500 mt-1 leading-relaxed">
                              {rule.description}
                            </p>
                          </div>

                          {/* Enable / Disable Switch */}
                          <button
                            type="button"
                            onClick={() => handlePolicyChange(rule, rule.action, !rule.enabled)}
                            className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-xl text-xs font-bold transition cursor-pointer shrink-0 border ${
                              rule.enabled
                                ? 'bg-emerald-50 text-emerald-800 border-emerald-300 shadow-2xs'
                                : 'bg-slate-100 text-slate-500 border-slate-300'
                            }`}
                            title={rule.enabled ? 'Click to disable policy' : 'Click to enable policy'}
                          >
                            <span
                              className={`w-2 h-2 rounded-full ${
                                rule.enabled ? 'bg-emerald-600 animate-pulse' : 'bg-slate-400'
                              }`}
                            />
                            <span>{rule.enabled ? 'Enabled' : 'Disabled'}</span>
                          </button>
                        </div>

                        {/* Bottom: Action Segmented Control (Block / Mask / Redact) */}
                        <div className="pt-2 border-t border-slate-100 flex flex-wrap items-center justify-between gap-2">
                          <span className="text-[11px] font-mono text-slate-500">
                            Enforcement Action:
                          </span>

                          <div className="inline-flex items-center bg-slate-100 p-1 rounded-xl border border-slate-200 text-xs">
                            {/* TOKENIZE / MASK */}
                            <button
                              type="button"
                              onClick={() => handlePolicyChange(rule, 'TOKENIZE', rule.enabled)}
                              className={`flex items-center gap-1 px-2.5 py-1 rounded-lg font-bold text-[11px] transition cursor-pointer ${
                                rule.action === 'TOKENIZE'
                                  ? 'bg-white text-cyan-800 shadow-xs border border-slate-200'
                                  : 'text-slate-600 hover:text-slate-900'
                              }`}
                              title="Mask with format-preserving surrogate or cryptographic token"
                            >
                              <Lock className="w-3 h-3 text-cyan-600" />
                              <span>Mask / Tokenize</span>
                            </button>

                            {/* BLOCK */}
                            <button
                              type="button"
                              onClick={() => handlePolicyChange(rule, 'BLOCK', rule.enabled)}
                              className={`flex items-center gap-1 px-2.5 py-1 rounded-lg font-bold text-[11px] transition cursor-pointer ${
                                rule.action === 'BLOCK'
                                  ? 'bg-rose-50 text-rose-800 shadow-xs border border-rose-200'
                                  : 'text-slate-600 hover:text-slate-900'
                              }`}
                              title="Halt request and stop prompt egress (HTTP 403)"
                            >
                              <XCircle className="w-3 h-3 text-rose-600" />
                              <span>Hard Block</span>
                            </button>

                            {/* REDACT */}
                            <button
                              type="button"
                              onClick={() => handlePolicyChange(rule, 'REDACT', rule.enabled)}
                              className={`flex items-center gap-1 px-2.5 py-1 rounded-lg font-bold text-[11px] transition cursor-pointer ${
                                rule.action === 'REDACT'
                                  ? 'bg-amber-50 text-amber-800 shadow-xs border border-amber-200'
                                  : 'text-slate-600 hover:text-slate-900'
                              }`}
                              title="Irreversibly redact sensitive data with [REDACTED]"
                            >
                              <Square className="w-3 h-3 text-amber-600" />
                              <span>Redact</span>
                            </button>
                          </div>
                        </div>
                      </div>
                    );
                  })}
              </div>
            </div>
          </div>
        )}

        {/* TAB 2: COMPLIANCE RADAR (ABSTRACTED EXECUTIVE METRICS) */}"""

content = content.replace(radar_tab_target, policies_view)

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated App.tsx with Security Policies successfully!')

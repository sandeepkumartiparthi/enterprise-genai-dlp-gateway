import re

file_path = r"E:\enterprise-genai-dlp-gateway\frontend\src\App.tsx"
with open(file_path, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update Header (lines ~1070 to 1315)
old_header_block = """      {/* EXECUTIVE HEADER: TWO-TIER ENTERPRISE ARCHITECTURE */}
      <header className="sticky top-0 z-40 bg-white/95 backdrop-blur-md border-b border-slate-200/80 shadow-xs overflow-x-hidden">
        {/* TIER 1: BRAND IDENTITY, TOPOLOGY, RBAC & SOC TOOLS */}
        <div className="border-b border-slate-100">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-15 flex items-center justify-between gap-4 overflow-hidden">
            {/* Left: Brand & Regional Cloud Topology */}
            <div className="flex items-center gap-3.5">
              <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-cyan-600 via-blue-600 to-indigo-600 text-white flex items-center justify-center shadow-xs ring-1 ring-cyan-500/20 shrink-0">
                <ShieldCheck className="w-5 h-5" />
              </div>
              <div className="flex items-center gap-3">
                <div className="flex items-center gap-2">
                  <h1
                    ref={mainHeadingRef}
                    className="text-base font-bold text-slate-900 tracking-tight executive-tooltip tooltip-bottom"
                    data-tooltip="AegisDLP Enterprise Reverse Proxy Core • Zero Raw PII Egress"
                  >
                    AegisDLP
                  </h1>
                  <span
                    className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 font-bold border border-emerald-200/80 executive-tooltip tooltip-bottom"
                    data-tooltip="2027 Production Gateway • Strict Zero-Trust Enforcement"
                  >
                    2027 Production
                  </span>
                </div>

                {/* Regional Indian Cloud Cluster Badge */}
                <div
                  className="hidden md:flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-slate-100 border border-slate-200/80 text-[11px] font-medium text-slate-600 executive-tooltip tooltip-bottom"
                  data-tooltip="Primary Cluster ap-south-1 (Mumbai) Active • 99.99% SLA • Hot Standby ap-south-2 (Hyderabad)"
                >
                  <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
                  <span className="font-semibold text-slate-800">ap-south-1</span>
                  <span className="text-slate-400">|</span>
                  <span>Mumbai Core • 99.99% SLA</span>
                </div>
              </div>
            </div>

            {/* Right: RBAC Persona Switcher & Executive Actions */}
            <div className="flex items-center gap-2.5">
              {/* RBAC Role Selector */}
              <div className="flex items-center bg-slate-100 p-0.5 rounded-xl border border-slate-200/80 text-xs">
                <span className="text-[10px] font-bold text-slate-400 uppercase px-2 hidden sm:inline">Role:</span>
                <button
                  type="button"
                  onClick={() => setCurrentUserRole('secops')}
                  title="SecOps Lead: Full admin, policy rules, and webhook controls"
                  data-tooltip="SecOps Director: Full admin, policy rules, and webhook controls"
                  className={`executive-tooltip tooltip-bottom px-2.5 py-1 rounded-lg text-xs font-bold transition cursor-pointer ${
                    currentUserRole === 'secops'
                      ? 'bg-white text-slate-900 shadow-xs'
                      : 'text-slate-600 hover:text-slate-900'
                  }`}
                >
                  SecOps Lead
                </button>
                <button
                  type="button"
                  onClick={() => setCurrentUserRole('compliance')}
                  title="Compliance Auditor: Read-only audits, EU AI Act conformity proofs"
                  data-tooltip="Compliance Auditor: Read-only audits, DPDP Act 2023 conformity proofs"
                  className={`executive-tooltip tooltip-bottom px-2.5 py-1 rounded-lg text-xs font-bold transition cursor-pointer ${
                    currentUserRole === 'compliance'
                      ? 'bg-white text-slate-900 shadow-xs'
                      : 'text-slate-600 hover:text-slate-900'
                  }`}
                >
                  Auditor
                </button>
                <button
                  type="button"
                  onClick={() => setCurrentUserRole('developer')}
                  title="AI Developer: Playground, P99 latency & surrogate verification"
                  data-tooltip="AI Developer: Playground, P99 latency & surrogate verification"
                  className={`executive-tooltip tooltip-bottom px-2.5 py-1 rounded-lg text-xs font-bold transition cursor-pointer ${
                    currentUserRole === 'developer'
                      ? 'bg-white text-slate-900 shadow-xs'
                      : 'text-slate-600 hover:text-slate-900'
                  }`}
                >
                  Developer
                </button>
              </div>

              {/* SOC & Incident Management Quick Actions */}
              <div className="flex items-center gap-1.5">
                <button
                  type="button"
                  onClick={handleOpenSiemModal}
                  title="Dispatch real-time SIEM alerts to Splunk, Datadog, Sentinel, or Slack"
                  data-tooltip="Dispatch real-time SIEM alerts to Splunk, Datadog, Sentinel, or Slack"
                  className="executive-tooltip tooltip-bottom inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl border border-slate-200/80 bg-white hover:bg-slate-50 text-slate-700 text-xs font-semibold shadow-2xs transition cursor-pointer"
                >
                  <Bell className="w-3.5 h-3.5 text-cyan-600" />
                  <span className="hidden sm:inline">SIEM Webhooks</span>
                </button>

                <button
                  type="button"
                  onClick={handleExportComplianceDossier}
                  title="Export EU AI Act & ISO/IEC 42001 Compliance Dossier"
                  data-tooltip="Export DPDP Act 2023 & ISO/IEC 42001 Compliance Dossier"
                  className="executive-tooltip tooltip-bottom inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl border border-slate-200/80 bg-white hover:bg-slate-50 text-slate-700 text-xs font-semibold shadow-2xs transition cursor-pointer"
                >
                  <FileText className="w-3.5 h-3.5 text-purple-600" />
                  <span className="hidden sm:inline">Dossier</span>
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* TIER 2: 5 PRIMARY NAVIGATION TABS & ACTIVE HORIZON TELEMETRY */}
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-12 flex items-center justify-between gap-4 overflow-hidden">
          {/* Left: Perfectly aligned segmented Navigation Tabs (No sideways scroll) */}
          <nav className="flex items-center gap-1.5 py-1 shrink-0 overflow-visible">
            <button
              type="button"
              onClick={() => setActiveTab('hub')}
              className={`flex items-center gap-2 px-3 py-1.5 rounded-xl text-xs font-semibold transition cursor-pointer ${
                activeTab === 'hub'
                  ? 'bg-slate-900 text-white shadow-xs'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100/70'
              }`}
            >
              <Zap className={`w-3.5 h-3.5 ${activeTab === 'hub' ? 'text-cyan-400' : 'text-cyan-600'}`} />
              <span
                className="executive-tooltip tooltip-bottom"
                data-tooltip="Interactive Playground: 4-Hop Pipeline, 2D Flow Highway & Live Payloads"
              >
                AI Privacy Hub
              </span>
            </button>

            <button
              type="button"
              onClick={() => setActiveTab('policies')}
              className={`flex items-center gap-2 px-3 py-1.5 rounded-xl text-xs font-semibold transition cursor-pointer ${
                activeTab === 'policies'
                  ? 'bg-slate-900 text-white shadow-xs'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100/70'
              }`}
            >
              <Sliders className={`w-3.5 h-3.5 ${activeTab === 'policies' ? 'text-indigo-400' : 'text-indigo-600'}`} />
              <span
                className="executive-tooltip tooltip-bottom"
                data-tooltip="Security Guardrails: Configure BLOCK, TOKENIZE, and REDACT actions"
              >
                Security Policies
              </span>
              {policies.length > 0 && (
                <span
                  className={`text-[10px] font-mono px-1.5 py-0.2 rounded-full font-bold ${
                    activeTab === 'policies'
                      ? 'bg-slate-800 text-cyan-300'
                      : 'bg-slate-200 text-slate-700'
                  }`}
                >
                  {policies.filter((p) => p.enabled).length}
                </span>
              )}
            </button>

            <button
              type="button"
              onClick={() => setActiveTab('radar')}
              className={`flex items-center gap-2 px-3 py-1.5 rounded-xl text-xs font-semibold transition cursor-pointer ${
                activeTab === 'radar'
                  ? 'bg-slate-900 text-white shadow-xs'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100/70'
              }`}
            >
              <Activity className={`w-3.5 h-3.5 ${activeTab === 'radar' ? 'text-blue-400' : 'text-blue-600'}`} />
              <span
                className="executive-tooltip tooltip-bottom"
                data-tooltip="Real-Time Telemetry: 360° Threat Interceptor, Perimeter Risk Meter & Sparklines"
              >
                Compliance Radar
              </span>
            </button>

            <button
              type="button"
              onClick={() => {
                setActiveTab('finops');
                fetchGovernanceData();
              }}
              className={`flex items-center gap-2 px-3 py-1.5 rounded-xl text-xs font-semibold transition cursor-pointer ${
                activeTab === 'finops'
                  ? 'bg-slate-900 text-white shadow-xs'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100/70'
              }`}
            >
              <Coins className={`w-3.5 h-3.5 ${activeTab === 'finops' ? 'text-amber-400' : 'text-amber-500'}`} />
              <span
                className="executive-tooltip tooltip-bottom"
                data-tooltip="FinOps Governance: Department Daily Token Ceilings, Burn Rates & Savings"
              >
                FinOps &amp; Quotas
              </span>
            </button>

            <button
              type="button"
              onClick={() => setActiveTab('ledger')}
              className={`flex items-center gap-2 px-3 py-1.5 rounded-xl text-xs font-semibold transition cursor-pointer ${
                activeTab === 'ledger'
                  ? 'bg-slate-900 text-white shadow-xs'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100/70'
              }`}
            >
              <Lock className={`w-3.5 h-3.5 ${activeTab === 'ledger' ? 'text-emerald-400' : 'text-emerald-600'}`} />
              <span
                className="executive-tooltip tooltip-bottom"
                data-tooltip="Tamper-Evident Ledger: Cryptographic Proofs & EU AI Act Art. 15 Receipts"
              >
                Audit Ledger &amp; Proofs
              </span>
            </button>
          </nav>

          {/* Right: Active Mode & Regulatory Security Chip */}
          <div className="hidden lg:flex items-center gap-2 text-xs shrink-0">
            <span
              className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-[11px] font-mono font-bold border ${
                privacyMode === 'synthetic'
                  ? 'bg-purple-50 text-purple-700 border-purple-200'
                  : 'bg-blue-50 text-blue-700 border-blue-200'
              } executive-tooltip tooltip-bottom`}
              data-tooltip="Active DLP Strategy applied to prompt egress"
            >
              {privacyMode === 'synthetic' ? '✨ Synthetic Shadows (Indian Personas)' : '🔒 Token Vault ([UUID])'}
            </span>

            <span
              className="inline-flex items-center gap-1 px-2 py-1 rounded-lg bg-emerald-50 text-emerald-700 border border-emerald-200 text-[11px] font-bold executive-tooltip tooltip-bottom"
              data-tooltip="Conforms to DPDP Act 2023, RBI Payment Tokenization & ISO/IEC 42001:2023"
            >
              <Check className="w-3 h-3 text-emerald-600" />
              <span>DPDP 2023 Validated</span>
            </span>
          </div>
        </div>
      </header>"""

new_header_block = """      {/* EXECUTIVE HEADER: TWO-TIER ENTERPRISE ARCHITECTURE (GOOGLE DESIGN - NO BLACK HIGHLIGHTS, NO BLACK TOOLTIPS) */}
      <header className="sticky top-0 z-40 bg-white/95 backdrop-blur-md border-b border-slate-200/80 shadow-xs overflow-x-hidden">
        {/* TIER 1: BRAND IDENTITY, TOPOLOGY, RBAC & SOC TOOLS */}
        <div className="border-b border-slate-100">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-15 flex items-center justify-between gap-4 overflow-hidden">
            {/* Left: Brand & Regional Cloud Topology */}
            <div className="flex items-center gap-3.5">
              <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-cyan-600 via-blue-600 to-indigo-600 text-white flex items-center justify-center shadow-xs ring-1 ring-cyan-500/20 shrink-0">
                <ShieldCheck className="w-5 h-5" />
              </div>
              <div className="flex items-center gap-3">
                <div className="flex items-center gap-2">
                  <h1
                    ref={mainHeadingRef}
                    className="text-base font-bold text-slate-900 tracking-tight"
                  >
                    AegisDLP
                  </h1>
                  <span
                    className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 font-bold border border-emerald-200/80"
                  >
                    2027 Production
                  </span>
                </div>

                {/* Regional Indian Cloud Cluster Badge */}
                <div
                  className="hidden md:flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-slate-100 border border-slate-200/80 text-[11px] font-medium text-slate-600"
                >
                  <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
                  <span className="font-semibold text-slate-800">ap-south-1</span>
                  <span className="text-slate-400">|</span>
                  <span>Mumbai Core • 99.99% SLA</span>
                </div>
              </div>
            </div>

            {/* Right: RBAC Persona Switcher & Executive Actions */}
            <div className="flex items-center gap-2.5">
              {/* RBAC Role Selector (Google Blue Active State - No Black Highlights) */}
              <div className="flex items-center bg-slate-100 p-0.5 rounded-xl border border-slate-200/80 text-xs">
                <span className="text-[10px] font-bold text-slate-400 uppercase px-2 hidden sm:inline">Role:</span>
                <button
                  type="button"
                  onClick={() => setCurrentUserRole('secops')}
                  title="SecOps Lead: Full admin, policy rules, and webhook controls"
                  className={`px-2.5 py-1 rounded-lg text-xs font-bold transition cursor-pointer ${
                    currentUserRole === 'secops'
                      ? 'bg-white text-blue-700 shadow-xs border border-blue-200/80'
                      : 'text-slate-600 hover:text-blue-700'
                  }`}
                >
                  SecOps Lead
                </button>
                <button
                  type="button"
                  onClick={() => setCurrentUserRole('compliance')}
                  title="Compliance Auditor: Read-only audits, DPDP Act 2023 conformity proofs"
                  className={`px-2.5 py-1 rounded-lg text-xs font-bold transition cursor-pointer ${
                    currentUserRole === 'compliance'
                      ? 'bg-white text-blue-700 shadow-xs border border-blue-200/80'
                      : 'text-slate-600 hover:text-blue-700'
                  }`}
                >
                  Auditor
                </button>
                <button
                  type="button"
                  onClick={() => setCurrentUserRole('developer')}
                  title="AI Developer: Playground, P99 latency & surrogate verification"
                  className={`px-2.5 py-1 rounded-lg text-xs font-bold transition cursor-pointer ${
                    currentUserRole === 'developer'
                      ? 'bg-white text-blue-700 shadow-xs border border-blue-200/80'
                      : 'text-slate-600 hover:text-blue-700'
                  }`}
                >
                  Developer
                </button>
              </div>

              {/* SOC & Incident Management Quick Actions */}
              <div className="flex items-center gap-1.5">
                <button
                  type="button"
                  onClick={handleOpenSiemModal}
                  title="Dispatch real-time SIEM alerts to Splunk, Datadog, Sentinel, or Slack"
                  className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl border border-slate-200/80 bg-white hover:bg-blue-50/70 hover:border-blue-200 text-slate-700 hover:text-blue-700 text-xs font-semibold shadow-2xs transition cursor-pointer"
                >
                  <Bell className="w-3.5 h-3.5 text-cyan-600" />
                  <span className="hidden sm:inline">SIEM Webhooks</span>
                </button>

                <button
                  type="button"
                  onClick={handleExportComplianceDossier}
                  title="Export DPDP Act 2023 & ISO/IEC 42001 Compliance Dossier"
                  className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl border border-slate-200/80 bg-white hover:bg-purple-50/70 hover:border-purple-200 text-slate-700 hover:text-purple-700 text-xs font-semibold shadow-2xs transition cursor-pointer"
                >
                  <FileText className="w-3.5 h-3.5 text-purple-600" />
                  <span className="hidden sm:inline">Dossier</span>
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* TIER 2: 5 PRIMARY NAVIGATION TABS (GOOGLE BLUE PILL, ZERO BLACK HIGHLIGHT, NO HOVER COMMENTS) */}
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-12 flex items-center justify-between gap-4 overflow-hidden">
          {/* Left: Perfectly aligned segmented Navigation Tabs (No sideways scroll, no black comments) */}
          <nav className="flex items-center gap-1.5 py-1 shrink-0 overflow-visible">
            <button
              type="button"
              onClick={() => setActiveTab('hub')}
              className={`flex items-center gap-2 px-3.5 py-1.5 rounded-xl text-xs font-semibold transition cursor-pointer ${
                activeTab === 'hub'
                  ? 'bg-blue-600 text-white shadow-xs shadow-blue-500/25 ring-1 ring-blue-700/20'
                  : 'text-slate-600 hover:text-blue-600 hover:bg-blue-50/80'
              }`}
            >
              <Zap className={`w-3.5 h-3.5 ${activeTab === 'hub' ? 'text-white' : 'text-blue-600'}`} />
              <span>AI Privacy Hub</span>
            </button>

            <button
              type="button"
              onClick={() => setActiveTab('policies')}
              className={`flex items-center gap-2 px-3.5 py-1.5 rounded-xl text-xs font-semibold transition cursor-pointer ${
                activeTab === 'policies'
                  ? 'bg-blue-600 text-white shadow-xs shadow-blue-500/25 ring-1 ring-blue-700/20'
                  : 'text-slate-600 hover:text-blue-600 hover:bg-blue-50/80'
              }`}
            >
              <Sliders className={`w-3.5 h-3.5 ${activeTab === 'policies' ? 'text-white' : 'text-indigo-600'}`} />
              <span>Security Policies</span>
              {policies.length > 0 && (
                <span
                  className={`text-[10px] font-mono px-1.5 py-0.2 rounded-full font-bold ${
                    activeTab === 'policies'
                      ? 'bg-blue-700 text-white'
                      : 'bg-slate-200 text-slate-700'
                  }`}
                >
                  {policies.filter((p) => p.enabled).length}
                </span>
              )}
            </button>

            <button
              type="button"
              onClick={() => setActiveTab('radar')}
              className={`flex items-center gap-2 px-3.5 py-1.5 rounded-xl text-xs font-semibold transition cursor-pointer ${
                activeTab === 'radar'
                  ? 'bg-blue-600 text-white shadow-xs shadow-blue-500/25 ring-1 ring-blue-700/20'
                  : 'text-slate-600 hover:text-blue-600 hover:bg-blue-50/80'
              }`}
            >
              <Activity className={`w-3.5 h-3.5 ${activeTab === 'radar' ? 'text-white' : 'text-blue-600'}`} />
              <span>Compliance Radar</span>
            </button>

            <button
              type="button"
              onClick={() => {
                setActiveTab('finops');
                fetchGovernanceData();
              }}
              className={`flex items-center gap-2 px-3.5 py-1.5 rounded-xl text-xs font-semibold transition cursor-pointer ${
                activeTab === 'finops'
                  ? 'bg-blue-600 text-white shadow-xs shadow-blue-500/25 ring-1 ring-blue-700/20'
                  : 'text-slate-600 hover:text-blue-600 hover:bg-blue-50/80'
              }`}
            >
              <Coins className={`w-3.5 h-3.5 ${activeTab === 'finops' ? 'text-white' : 'text-amber-500'}`} />
              <span>FinOps &amp; Quotas</span>
            </button>

            <button
              type="button"
              onClick={() => setActiveTab('ledger')}
              className={`flex items-center gap-2 px-3.5 py-1.5 rounded-xl text-xs font-semibold transition cursor-pointer ${
                activeTab === 'ledger'
                  ? 'bg-blue-600 text-white shadow-xs shadow-blue-500/25 ring-1 ring-blue-700/20'
                  : 'text-slate-600 hover:text-blue-600 hover:bg-blue-50/80'
              }`}
            >
              <Lock className={`w-3.5 h-3.5 ${activeTab === 'ledger' ? 'text-white' : 'text-emerald-600'}`} />
              <span>Audit Ledger &amp; Proofs</span>
            </button>
          </nav>

          {/* Right: Active Mode & Regulatory Security Chip */}
          <div className="hidden lg:flex items-center gap-2 text-xs shrink-0">
            <span
              className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-[11px] font-mono font-bold border ${
                privacyMode === 'synthetic'
                  ? 'bg-purple-50 text-purple-700 border-purple-200'
                  : 'bg-blue-50 text-blue-700 border-blue-200'
              }`}
            >
              {privacyMode === 'synthetic' ? '✨ Synthetic Shadows (Indian Personas)' : '🔒 Token Vault ([UUID])'}
            </span>

            <span
              className="inline-flex items-center gap-1 px-2 py-1 rounded-lg bg-emerald-50 text-emerald-700 border border-emerald-200 text-[11px] font-bold"
            >
              <Check className="w-3 h-3 text-emerald-600" />
              <span>DPDP 2023 Validated</span>
            </span>
          </div>
        </div>
      </header>"""

assert old_header_block in code, "old_header_block not found in App.tsx"
code = code.replace(old_header_block, new_header_block)
print("Replaced Header block successfully!")

# 2. Add pipeline-hop-card to the 4 hops in Hub
code = code.replace(
    "className={`rounded-xl border p-3.5 transition-all duration-300 ${",
    "className={`rounded-xl border p-3.5 pipeline-hop-card cursor-pointer transition-all duration-300 ${"
)

# 3. Update Scenario Suite category pills:
old_cat_pill = """                    className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-xl text-xs font-semibold transition cursor-pointer ${
                      selectedScenarioCategory === cat.id
                        ? 'bg-slate-900 text-white shadow-xs'
                        : 'bg-slate-50 hover:bg-slate-100 text-slate-600 hover:text-slate-900 border border-slate-200'
                    }`}
                  >
                    <span>{cat.label}</span>
                    <span
                      className={`text-[10px] font-mono px-1.5 py-0.2 rounded-full ${
                        selectedScenarioCategory === cat.id
                          ? 'bg-slate-800 text-cyan-300'
                          : 'bg-slate-200/80 text-slate-700'
                      }`}
                    >"""

new_cat_pill = """                    className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-xl text-xs font-semibold transition cursor-pointer ${
                      selectedScenarioCategory === cat.id
                        ? 'bg-blue-600 text-white shadow-xs shadow-blue-500/20'
                        : 'bg-slate-50 hover:bg-blue-50/70 text-slate-600 hover:text-blue-700 border border-slate-200'
                    }`}
                  >
                    <span>{cat.label}</span>
                    <span
                      className={`text-[10px] font-mono px-1.5 py-0.2 rounded-full ${
                        selectedScenarioCategory === cat.id
                          ? 'bg-blue-700 text-white'
                          : 'bg-slate-200/80 text-slate-700'
                      }`}
                    >"""

if old_cat_pill in code:
    code = code.replace(old_cat_pill, new_cat_pill)
    print("Replaced scenario category pills!")
else:
    print("WARNING: old_cat_pill not found")

# 4. Update "Run Compliance Suite" button to Google Blue:
old_run_btn = """                  <button
                    type="button"
                    onClick={handleOpenBatchSuiteModal}
                    title="Automatically execute all 15 scenarios against the gateway and generate an executive scorecard"
                    data-tooltip="1-Click Automated Compliance Suite across all 15 industry presets"
                    className="executive-tooltip tooltip-bottom inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold transition cursor-pointer shadow-sm"
                  >"""

new_run_btn = """                  <button
                    type="button"
                    onClick={handleOpenBatchSuiteModal}
                    title="Automatically execute all 15 scenarios against the gateway and generate an executive scorecard"
                    className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold transition cursor-pointer shadow-sm"
                  >"""

if old_run_btn in code:
    code = code.replace(old_run_btn, new_run_btn)
    print("Replaced Run Compliance Suite button!")

# 5. Add scenario-card-item to each scenario card button:
old_scenario_btn = """                        className={`text-left p-3 rounded-xl border transition cursor-pointer flex flex-col justify-between gap-1.5 ${
                          isSelected
                            ? 'bg-cyan-50/70 border-cyan-400 ring-1 ring-cyan-400 shadow-xs'
                            : 'bg-slate-50/50 hover:bg-slate-100/80 border-slate-200 hover:border-slate-300'
                        }`}"""

new_scenario_btn = """                        className={`text-left p-3 rounded-xl border scenario-card-item transition cursor-pointer flex flex-col justify-between gap-1.5 ${
                          isSelected
                            ? 'bg-cyan-50/70 border-cyan-400 ring-1 ring-cyan-400 shadow-xs'
                            : 'bg-slate-50/50 hover:bg-blue-50/40 border-slate-200 hover:border-blue-300'
                        }`}"""

if old_scenario_btn in code:
    code = code.replace(old_scenario_btn, new_scenario_btn)
    print("Added scenario-card-item class to scenario cards!")

# 6. Update "Send Safely to AI" button:
old_send_btn = """                  <button
                    type="submit"
                    disabled={isSendingProxy}
                    className="inline-flex items-center gap-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-white font-bold px-6 py-2.5 text-xs sm:text-sm shadow-md hover:shadow-lg transition cursor-pointer disabled:opacity-50"
                  >
                    <Send className="w-4 h-4 text-cyan-400" />"""

new_send_btn = """                  <button
                    type="submit"
                    disabled={isSendingProxy}
                    className="inline-flex items-center gap-2 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-bold px-6 py-2.5 text-xs sm:text-sm shadow-md shadow-blue-500/25 hover:shadow-lg transition cursor-pointer disabled:opacity-50"
                  >
                    <Send className="w-4 h-4 text-white" />"""

if old_send_btn in code:
    code = code.replace(old_send_btn, new_send_btn)
    print("Replaced Send Safely to AI button!")

# 7. Update Policies tab category filter:
old_policy_cat = """                        className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-xl text-xs font-semibold transition cursor-pointer ${
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
                        >"""

new_policy_cat = """                        className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-xl text-xs font-semibold transition cursor-pointer ${
                          policyCategoryFilter === cat
                            ? 'bg-blue-600 text-white shadow-xs shadow-blue-500/20'
                            : 'bg-slate-50 hover:bg-blue-50/70 text-slate-600 hover:text-blue-700 border border-slate-200'
                        }`}
                      >
                        <span>{cat === 'All' ? 'All Policies' : cat}</span>
                        <span
                          className={`text-[10px] font-mono px-1.5 py-0.2 rounded-full ${
                            policyCategoryFilter === cat ? 'bg-blue-700 text-white' : 'bg-slate-200 text-slate-700'
                          }`}
                        >"""

if old_policy_cat in code:
    code = code.replace(old_policy_cat, new_policy_cat)
    print("Replaced policy category filter pills!")

# 8. Save updated App.tsx
with open(file_path, "w", encoding="utf-8") as f:
    f.write(code)

print("Successfully written updated App.tsx!")

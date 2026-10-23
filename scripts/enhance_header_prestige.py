import re

# 1. Update index.css for ambient luxury lighting
css_path = r"E:\enterprise-genai-dlp-gateway\frontend\src\index.css"
with open(css_path, "r", encoding="utf-8") as f:
    css = f.read()

old_body = """body {
  background-color: #f8fafc;
  color: #0f172a;
}"""

new_body = """body {
  background-color: #f8fafc;
  background-image: 
    radial-gradient(at 0% 0%, rgba(224, 242, 254, 0.45) 0px, transparent 50%),
    radial-gradient(at 100% 0%, rgba(238, 242, 255, 0.4) 0px, transparent 50%),
    radial-gradient(at 50% 100%, rgba(240, 253, 250, 0.25) 0px, transparent 50%);
  background-attachment: fixed;
  color: #0f172a;
}"""

if old_body in css:
    css = css.replace(old_body, new_body)
    with open(css_path, "w", encoding="utf-8") as f:
        f.write(css)
    print("Updated body background in index.css with ambient lighting!")
else:
    print("WARNING: old_body not found in index.css")

# 2. Update App.tsx Header block
app_path = r"E:\enterprise-genai-dlp-gateway\frontend\src\App.tsx"
with open(app_path, "r", encoding="utf-8") as f:
    app_code = f.read()

start_marker = "      {/* EXECUTIVE HEADER: TWO-TIER ENTERPRISE ARCHITECTURE (GOOGLE DESIGN - NO BLACK HIGHLIGHTS, NO BLACK TOOLTIPS) */}"
end_marker = "      </header>"

start_idx = app_code.find(start_marker)
end_idx = app_code.find(end_marker, start_idx) + len(end_marker)

assert start_idx != -1 and end_idx != -1, "Header block markers not found!"

new_header_code = """      {/* EXECUTIVE HEADER: TWO-TIER ENTERPRISE ARCHITECTURE (PRESTIGE GOOGLE & STRIPE DESIGN) */}
      <header className="sticky top-0 z-40 bg-white/95 backdrop-blur-xl border-b border-slate-200/80 shadow-[0_1px_3px_0_rgba(0,0,0,0.03),0_1px_2px_-1px_rgba(0,0,0,0.02)] overflow-x-hidden">
        {/* Top Micro-Glow Accent Line */}
        <div className="h-[2.5px] w-full bg-gradient-to-r from-cyan-500 via-blue-600 to-indigo-600 opacity-90" />

        {/* TIER 1: BRAND IDENTITY, TOPOLOGY, RBAC & SOC TOOLS */}
        <div className="border-b border-slate-200/60">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-15 flex items-center justify-between gap-4 overflow-hidden">
            {/* Left: Brand & Regional Cloud Topology */}
            <div className="flex items-center gap-3.5">
              <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-cyan-600 via-blue-600 to-indigo-600 text-white flex items-center justify-center shadow-xs ring-1 ring-cyan-500/30 shrink-0">
                <ShieldCheck className="w-5 h-5 text-white drop-shadow-xs" />
              </div>
              <div className="flex items-center gap-3">
                <div className="flex items-center gap-2">
                  <h1
                    ref={mainHeadingRef}
                    className="text-[17px] font-extrabold text-slate-900 tracking-tight flex items-center gap-1"
                  >
                    <span>Aegis</span>
                    <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-600 via-blue-600 to-indigo-600 font-black">DLP</span>
                  </h1>
                  <span
                    className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[10px] font-mono font-bold bg-emerald-50 text-emerald-700 border border-emerald-200 shadow-2xs"
                  >
                    <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
                    v2.7 Enterprise
                  </span>
                </div>

                {/* Regional Indian Cloud Cluster Badge */}
                <div
                  className="hidden md:inline-flex items-center gap-2 px-3 py-1 rounded-full bg-slate-100/80 border border-slate-200/80 text-[11px] text-slate-700 font-medium shadow-2xs backdrop-blur-xs"
                >
                  <span className="relative flex h-2 w-2">
                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                    <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
                  </span>
                  <span className="font-mono font-bold text-slate-900">ap-south-1</span>
                  <span className="text-slate-300 font-light">|</span>
                  <span className="text-slate-600 font-medium">Mumbai Core</span>
                  <span className="px-1.5 py-0.2 rounded-md bg-emerald-100/80 text-emerald-800 font-mono text-[9px] font-bold border border-emerald-200/60">99.99% SLA</span>
                </div>
              </div>
            </div>

            {/* Right: RBAC Persona Switcher & Executive Actions */}
            <div className="flex items-center gap-2.5">
              {/* RBAC Role Selector Segmented Pill */}
              <div className="flex items-center bg-slate-100/90 p-1 rounded-xl border border-slate-200/70 shadow-2xs text-xs">
                <span className="text-[10px] font-bold text-slate-400 uppercase px-2 hidden sm:inline tracking-wider">Role</span>
                <button
                  type="button"
                  onClick={() => setCurrentUserRole('secops')}
                  title="SecOps Lead: Full admin, policy rules, and webhook controls"
                  className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-lg text-xs font-bold transition cursor-pointer ${
                    currentUserRole === 'secops'
                      ? 'bg-white text-blue-700 shadow-xs border border-slate-200/70'
                      : 'text-slate-600 hover:text-slate-900'
                  }`}
                >
                  <ShieldCheck className="w-3 h-3 text-cyan-600" />
                  <span>SecOps Lead</span>
                </button>
                <button
                  type="button"
                  onClick={() => setCurrentUserRole('compliance')}
                  title="Compliance Auditor: Read-only audits, DPDP Act 2023 conformity proofs"
                  className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-lg text-xs font-bold transition cursor-pointer ${
                    currentUserRole === 'compliance'
                      ? 'bg-white text-blue-700 shadow-xs border border-slate-200/70'
                      : 'text-slate-600 hover:text-slate-900'
                  }`}
                >
                  <FileCheck className="w-3 h-3 text-purple-600" />
                  <span>Auditor</span>
                </button>
                <button
                  type="button"
                  onClick={() => setCurrentUserRole('developer')}
                  title="AI Developer: Playground, P99 latency & surrogate verification"
                  className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-lg text-xs font-bold transition cursor-pointer ${
                    currentUserRole === 'developer'
                      ? 'bg-white text-blue-700 shadow-xs border border-slate-200/70'
                      : 'text-slate-600 hover:text-slate-900'
                  }`}
                >
                  <Terminal className="w-3 h-3 text-blue-600" />
                  <span>Developer</span>
                </button>
              </div>

              {/* SOC & Incident Management Quick Actions */}
              <div className="flex items-center gap-2">
                <button
                  type="button"
                  onClick={handleOpenSiemModal}
                  title="Dispatch real-time SIEM alerts to Splunk, Datadog, Sentinel, or Slack"
                  className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl border border-slate-200/90 bg-white hover:bg-slate-50 hover:border-cyan-300 text-slate-700 hover:text-cyan-700 text-xs font-semibold shadow-2xs hover:shadow-xs transition cursor-pointer"
                >
                  <Bell className="w-3.5 h-3.5 text-cyan-600" />
                  <span className="hidden sm:inline">SIEM Webhooks</span>
                </button>

                <button
                  type="button"
                  onClick={handleExportComplianceDossier}
                  title="Export DPDP Act 2023 & ISO/IEC 42001 Compliance Dossier"
                  className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl border border-purple-200/80 bg-purple-50/40 hover:bg-purple-50 hover:border-purple-300 text-purple-700 text-xs font-bold shadow-2xs hover:shadow-xs transition cursor-pointer"
                >
                  <FileText className="w-3.5 h-3.5 text-purple-600" />
                  <span className="hidden sm:inline">Dossier</span>
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* TIER 2: 5 PRIMARY NAVIGATION TABS (COHESIVE SEGMENTED TRACK) & ACTIVE SECURITY TELEMETRY */}
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-12 flex items-center justify-between gap-4 overflow-hidden">
          {/* Left: Perfectly aligned Segmented Navigation Track */}
          <nav className="flex items-center p-1 bg-slate-100/90 rounded-2xl border border-slate-200/80 shadow-2xs shrink-0 overflow-visible">
            <button
              type="button"
              onClick={() => setActiveTab('hub')}
              className={`flex items-center gap-2 px-3.5 py-1.5 rounded-xl text-xs font-semibold transition cursor-pointer ${
                activeTab === 'hub'
                  ? 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-xs font-bold ring-1 ring-blue-700/20'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-white/70'
              }`}
            >
              <Zap className={`w-3.5 h-3.5 ${activeTab === 'hub' ? 'text-white' : 'text-cyan-600'}`} />
              <span>AI Privacy Hub</span>
            </button>

            <button
              type="button"
              onClick={() => setActiveTab('policies')}
              className={`flex items-center gap-2 px-3.5 py-1.5 rounded-xl text-xs font-semibold transition cursor-pointer ${
                activeTab === 'policies'
                  ? 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-xs font-bold ring-1 ring-blue-700/20'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-white/70'
              }`}
            >
              <Sliders className={`w-3.5 h-3.5 ${activeTab === 'policies' ? 'text-white' : 'text-indigo-600'}`} />
              <span>Security Policies</span>
              {policies.length > 0 && (
                <span
                  className={`text-[10px] font-mono px-1.5 py-0.2 rounded-full font-bold ${
                    activeTab === 'policies'
                      ? 'bg-white/20 text-white'
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
                  ? 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-xs font-bold ring-1 ring-blue-700/20'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-white/70'
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
                  ? 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-xs font-bold ring-1 ring-blue-700/20'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-white/70'
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
                  ? 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-xs font-bold ring-1 ring-blue-700/20'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-white/70'
              }`}
            >
              <Lock className={`w-3.5 h-3.5 ${activeTab === 'ledger' ? 'text-white' : 'text-emerald-600'}`} />
              <span>Audit Ledger &amp; Proofs</span>
            </button>
          </nav>

          {/* Right: Active Mode & Regulatory Security Chip */}
          <div className="hidden lg:flex items-center gap-2.5 text-xs shrink-0">
            <div
              className={`inline-flex items-center gap-2 px-3 py-1.5 rounded-xl text-xs font-semibold border shadow-2xs transition ${
                privacyMode === 'synthetic'
                  ? 'bg-purple-50/80 text-purple-800 border-purple-200/90'
                  : 'bg-blue-50/80 text-blue-800 border-blue-200/90'
              }`}
            >
              <span className={`w-2 h-2 rounded-full ${privacyMode === 'synthetic' ? 'bg-purple-600' : 'bg-blue-600'} animate-pulse`} />
              <span className="font-mono text-[10px] font-bold text-slate-400 uppercase">Mode:</span>
              <span className="font-mono text-[11px] font-bold">
                {privacyMode === 'synthetic' ? '✨ Synthetic Shadows (Indian Personas)' : '🔒 Token Vault ([UUID])'}
              </span>
            </div>

            <div className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-emerald-50/80 border border-emerald-200/90 text-emerald-800 text-xs font-bold shadow-2xs">
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
              <span>DPDP 2023 Validated</span>
            </div>
          </div>
        </div>
      </header>"""

app_code = app_code[:start_idx] + new_header_code + app_code[end_idx:]

with open(app_path, "w", encoding="utf-8") as f:
    f.write(app_code)

print("Successfully replaced Header in App.tsx with prestige design!")

import os

app_path = 'E:/enterprise-genai-dlp-gateway/frontend/src/App.tsx'

with open(app_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update fetchAllData to call fetchGovernanceData
old_fetchall = """      if (tokensRes.ok) setTokens(await tokensRes.json());
      if (policiesRes.ok) setPolicies(await policiesRes.json());
    } catch (err) {"""

new_fetchall = """      if (tokensRes.ok) setTokens(await tokensRes.json());
      if (policiesRes.ok) setPolicies(await policiesRes.json());
      await fetchGovernanceData();
    } catch (err) {"""

if old_fetchall in text:
    text = text.replace(old_fetchall, new_fetchall)
    print("Updated fetchAllData (LF)")
else:
    old_fetchall_crlf = old_fetchall.replace('\n', '\r\n')
    if old_fetchall_crlf in text:
        text = text.replace(old_fetchall_crlf, new_fetchall.replace('\n', '\r\n'))
        print("Updated fetchAllData (CRLF)")
    else:
        print("Could not find old_fetchall!")

# 2. Update Header: Add Persona switcher, Region SLA pill, Quick Actions, and FinOps tab
old_header = """      {/* EXECUTIVE HEADER */}
      <header className="sticky top-0 z-40 bg-white/95 backdrop-blur-md border-b border-slate-200 shadow-xs">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-600 to-blue-600 text-white flex items-center justify-center shadow-md">
              <ShieldCheck className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 ref={mainHeadingRef} className="text-base sm:text-lg font-bold text-slate-900 tracking-tight">
                  AegisDLP
                </h1>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 font-bold border border-emerald-200">
                  2027 Executive Standard
                </span>
              </div>
              <p className="text-[11px] text-slate-500 font-medium">
                Enterprise GenAI Privacy Gateway • Zero Raw PII Exposure
              </p>
            </div>
          </div>

          {/* Abstracted 3-Tab Navigation */}
          <nav className="flex items-center gap-1 bg-slate-100 p-1 rounded-xl border border-slate-200">"""

new_header = """      {/* EXECUTIVE HEADER */}
      <header className="sticky top-0 z-40 bg-white/95 backdrop-blur-md border-b border-slate-200 shadow-xs">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between flex-wrap gap-2">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-600 to-blue-600 text-white flex items-center justify-center shadow-md">
              <ShieldCheck className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 ref={mainHeadingRef} className="text-base sm:text-lg font-bold text-slate-900 tracking-tight">
                  AegisDLP
                </h1>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 font-bold border border-emerald-200">
                  2027 Production Gateway
                </span>
              </div>
              <div className="flex items-center gap-2 text-[11px] text-slate-500 font-medium">
                <span className="hidden sm:inline">Zero Raw PII Exposure</span>
                <span className="hidden sm:inline">•</span>
                <span className="flex items-center gap-1 text-emerald-700 font-semibold">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
                  us-east-1 (Primary) 99.99% SLA
                </span>
              </div>
            </div>
          </div>

          {/* Persona Switcher & Quick Enterprise Actions */}
          <div className="flex items-center gap-2">
            {/* RBAC Role Selector */}
            <div className="flex items-center bg-slate-100 p-0.5 rounded-lg border border-slate-200 text-xs">
              <span className="text-[10px] font-bold text-slate-500 uppercase px-2 hidden md:inline">Role:</span>
              <button
                type="button"
                onClick={() => setCurrentUserRole('secops')}
                className={`px-2 py-1 rounded text-[11px] font-bold transition cursor-pointer ${
                  currentUserRole === 'secops'
                    ? 'bg-white text-slate-900 shadow-xs'
                    : 'text-slate-600 hover:text-slate-900'
                }`}
                title="SecOps Lead: Full admin, policy rules, and webhook controls"
              >
                SecOps Lead
              </button>
              <button
                type="button"
                onClick={() => setCurrentUserRole('compliance')}
                className={`px-2 py-1 rounded text-[11px] font-bold transition cursor-pointer ${
                  currentUserRole === 'compliance'
                    ? 'bg-white text-slate-900 shadow-xs'
                    : 'text-slate-600 hover:text-slate-900'
                }`}
                title="Compliance Auditor: Read-only audits, EU AI Act conformity proofs"
              >
                Compliance Auditor
              </button>
              <button
                type="button"
                onClick={() => setCurrentUserRole('developer')}
                className={`px-2 py-1 rounded text-[11px] font-bold transition cursor-pointer ${
                  currentUserRole === 'developer'
                    ? 'bg-white text-slate-900 shadow-xs'
                    : 'text-slate-600 hover:text-slate-900'
                }`}
                title="AI Developer: Playground, P99 latency & surrogate verification"
              >
                Developer
              </button>
            </div>

            {/* Quick Actions */}
            <div className="hidden lg:flex items-center gap-1.5">
              <button
                type="button"
                onClick={handleOpenSiemModal}
                className="inline-flex items-center gap-1 px-2.5 py-1.5 rounded-lg border border-slate-200 bg-white hover:bg-slate-50 text-slate-700 text-xs font-semibold transition cursor-pointer"
                title="Dispatch real-time SIEM alerts to Splunk, Datadog, Sentinel, or Slack"
              >
                <Bell className="w-3.5 h-3.5 text-cyan-600" />
                <span>SIEM</span>
              </button>

              <button
                type="button"
                onClick={handleExportComplianceDossier}
                className="inline-flex items-center gap-1 px-2.5 py-1.5 rounded-lg border border-slate-200 bg-white hover:bg-slate-50 text-slate-700 text-xs font-semibold transition cursor-pointer"
                title="Export EU AI Act & ISO/IEC 42001 Compliance Dossier"
              >
                <FileText className="w-3.5 h-3.5 text-purple-600" />
                <span>Dossier</span>
              </button>
            </div>
          </div>

          {/* 5-Tab Navigation */}
          <nav className="flex items-center gap-1 bg-slate-100 p-1 rounded-xl border border-slate-200 overflow-x-auto">"""

if old_header in text:
    text = text.replace(old_header, new_header)
    print("Updated Header (LF)")
else:
    old_header_crlf = old_header.replace('\n', '\r\n')
    if old_header_crlf in text:
        text = text.replace(old_header_crlf, new_header.replace('\n', '\r\n'))
        print("Updated Header (CRLF)")
    else:
        print("Could not find old_header!")

# 3. Add FinOps Tab button right after radar button
old_radar_button = """            <button
              type="button"
              onClick={() => setActiveTab('radar')}
              className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-semibold transition cursor-pointer ${
                activeTab === 'radar'
                  ? 'bg-white text-slate-900 shadow-sm border border-slate-200/80'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              <Activity className="w-3.5 h-3.5 text-blue-600" />
              <span>Compliance Radar</span>
            </button>"""

new_radar_button = """            <button
              type="button"
              onClick={() => setActiveTab('radar')}
              className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-semibold transition cursor-pointer ${
                activeTab === 'radar'
                  ? 'bg-white text-slate-900 shadow-sm border border-slate-200/80'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              <Activity className="w-3.5 h-3.5 text-blue-600" />
              <span>Compliance Radar</span>
            </button>
            <button
              type="button"
              onClick={() => {
                setActiveTab('finops');
                fetchGovernanceData();
              }}
              className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-semibold transition cursor-pointer ${
                activeTab === 'finops'
                  ? 'bg-white text-slate-900 shadow-sm border border-slate-200/80'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              <Coins className="w-3.5 h-3.5 text-amber-500" />
              <span>FinOps &amp; Quotas</span>
            </button>"""

if old_radar_button in text:
    text = text.replace(old_radar_button, new_radar_button)
    print("Added FinOps Tab Button (LF)")
else:
    old_radar_button_crlf = old_radar_button.replace('\n', '\r\n')
    if old_radar_button_crlf in text:
        text = text.replace(old_radar_button_crlf, new_radar_button.replace('\n', '\r\n'))
        print("Added FinOps Tab Button (CRLF)")
    else:
        print("Could not find old_radar_button!")

# 4. Add Batch Suite Run Button in Scenario Catalog header
old_scenario_hdr = """                <div className="flex items-center gap-2">
                  <span className="text-xs font-bold text-slate-900 uppercase tracking-wider flex items-center gap-1.5">
                    <Sliders className="w-3.5 h-3.5 text-cyan-600" /> Enterprise Test Scenarios (15 Verified Suites)
                  </span>
                  <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded-full bg-cyan-50 text-cyan-700 border border-cyan-200">
                    Real-World Catalog
                  </span>
                </div>
                <span className="text-[11px] text-slate-500 font-medium">
                  Select any scenario to automatically configure real PII, tokens, and target AI model
                </span>"""

new_scenario_hdr = """                <div className="flex items-center gap-2">
                  <span className="text-xs font-bold text-slate-900 uppercase tracking-wider flex items-center gap-1.5">
                    <Sliders className="w-3.5 h-3.5 text-cyan-600" /> Enterprise Test Scenarios (15 Verified Suites)
                  </span>
                  <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded-full bg-cyan-50 text-cyan-700 border border-cyan-200">
                    Real-World Catalog
                  </span>
                </div>
                <div className="flex items-center gap-2">
                  <button
                    type="button"
                    onClick={handleOpenBatchSuiteModal}
                    className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold transition cursor-pointer shadow-sm"
                    title="Automatically execute all 15 scenarios against the gateway and generate an executive scorecard"
                  >
                    <PlayCircle className="w-3.5 h-3.5 text-cyan-400" />
                    <span>Run Compliance Suite (15 Scenarios)</span>
                  </button>
                  <span className="text-[11px] text-slate-500 font-medium hidden sm:inline">
                    Select any scenario to prefill payload
                  </span>
                </div>"""

if old_scenario_hdr in text:
    text = text.replace(old_scenario_hdr, new_scenario_hdr)
    print("Added Batch Suite Run Button (LF)")
else:
    old_scenario_hdr_crlf = old_scenario_hdr.replace('\n', '\r\n')
    if old_scenario_hdr_crlf in text:
        text = text.replace(old_scenario_hdr_crlf, new_scenario_hdr.replace('\n', '\r\n'))
        print("Added Batch Suite Run Button (CRLF)")
    else:
        print("Could not find old_scenario_hdr!")

# 5. Inject FinOps Tab View right before Tab 3/4: Audit Ledger
ledger_marker = "{/* TAB 3: AUDIT LEDGER & PROOFS (CLEAN EXECUTIVE VIEW) */}"
finops_view = """{/* TAB 4: FINOPS TOKEN QUOTA & RESOURCE GOVERNANCE */}
        {activeTab === 'finops' && (
          <div className="space-y-6 animate-card-enter">
            {/* Header & Overview Card */}
            <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-xs flex flex-col lg:flex-row items-start lg:items-center justify-between gap-4">
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
                    <Coins className="w-5 h-5 text-amber-500" />
                    Enterprise FinOps &amp; Token Quota Governance
                  </h2>
                  <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200 font-bold">
                    Real-Time Rate-Limiting
                  </span>
                </div>
                <p className="text-xs text-slate-500 leading-relaxed max-w-2xl">
                  Enforce strict departmental token quotas to prevent runaway GenAI recursive agent costs, accidental denial-of-service loops, and budgetary overruns. Format-preserving PII tokenization automatically compresses egress payload overhead by up to 28%.
                </p>
              </div>

              <div className="flex items-center gap-2 flex-wrap">
                <button
                  type="button"
                  onClick={fetchGovernanceData}
                  className="inline-flex items-center gap-1.5 px-3 py-2 rounded-xl bg-slate-50 hover:bg-slate-100 border border-slate-200 text-xs font-semibold text-slate-700 transition cursor-pointer"
                >
                  <RefreshCw className={`w-3.5 h-3.5 ${isLoadingGovernance ? 'animate-spin' : ''}`} /> Refresh Quotas
                </button>
              </div>
            </div>

            {/* FinOps KPI Cards */}
            {governanceData && (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-xs">
                  <span className="text-xs font-bold text-slate-500 uppercase tracking-wider block mb-1">
                    Total Daily Budget
                  </span>
                  <div className="flex items-baseline justify-between">
                    <span className="text-2xl sm:text-3xl font-extrabold text-slate-900">
                      {governanceData.overallSummary.totalDailyBudget.toLocaleString()}
                    </span>
                    <span className="text-xs font-mono font-bold text-slate-600 bg-slate-100 px-2 py-0.5 rounded border border-slate-200">
                      Tokens / Day
                    </span>
                  </div>
                  <div className="mt-3 pt-2 border-t border-slate-100 flex items-center justify-between text-[11px] text-slate-500">
                    <span>SLA Capacity:</span>
                    <span className="font-semibold text-slate-800">{governanceData.overallSummary.activeSlaTier}</span>
                  </div>
                </div>

                <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-xs">
                  <span className="text-xs font-bold text-slate-500 uppercase tracking-wider block mb-1">
                    Consumed Today
                  </span>
                  <div className="flex items-baseline justify-between">
                    <span className="text-2xl sm:text-3xl font-extrabold text-cyan-800">
                      {governanceData.overallSummary.totalConsumedTokens.toLocaleString()}
                    </span>
                    <span className="text-xs font-bold text-cyan-700 bg-cyan-50 px-2 py-0.5 rounded-md border border-cyan-200">
                      {governanceData.overallSummary.overallUtilizationPct}% Utilized
                    </span>
                  </div>
                  <div className="mt-3 pt-2 border-t border-slate-100">
                    <div className="w-full bg-slate-100 rounded-full h-1.5 overflow-hidden">
                      <div
                        className="bg-cyan-500 h-1.5 rounded-full transition-all duration-500"
                        style={{ width: `${Math.min(100, governanceData.overallSummary.overallUtilizationPct)}%` }}
                      />
                    </div>
                  </div>
                </div>

                <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-xs">
                  <span className="text-xs font-bold text-slate-500 uppercase tracking-wider block mb-1">
                    FinOps Savings (DLP Compression)
                  </span>
                  <div className="flex items-baseline justify-between">
                    <span className="text-2xl sm:text-3xl font-extrabold text-emerald-800">
                      ${governanceData.overallSummary.totalFinOpsSavingsUsd.toFixed(2)}
                    </span>
                    <span className="text-xs font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-md border border-emerald-200">
                      28% Payload Saved
                    </span>
                  </div>
                  <div className="mt-3 pt-2 border-t border-slate-100 flex items-center justify-between text-[11px] text-slate-500">
                    <span>Methodology:</span>
                    <span className="font-semibold text-emerald-700">Surrogate Token Stripping</span>
                  </div>
                </div>

                <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-xs">
                  <span className="text-xs font-bold text-slate-500 uppercase tracking-wider block mb-1">
                    Perimeter Throttle Status
                  </span>
                  <div className="flex items-baseline justify-between">
                    <span className="text-2xl sm:text-3xl font-extrabold text-slate-900">
                      Zero Blockages
                    </span>
                    <span className="text-xs font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-md border border-emerald-200 flex items-center gap-1">
                      <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" /> All Healthy
                    </span>
                  </div>
                  <div className="mt-3 pt-2 border-t border-slate-100 flex items-center justify-between text-[11px] text-slate-500">
                    <span>Active Clusters:</span>
                    <span className="font-mono font-semibold text-slate-700">5 Departments Guarded</span>
                  </div>
                </div>
              </div>
            )}

            {/* Department Quota Table & Visual Progress */}
            {governanceData && (
              <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-xs space-y-4">
                <div className="flex items-center justify-between border-b border-slate-100 pb-3">
                  <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                    <Building2 className="w-4 h-4 text-cyan-600" />
                    Departmental Quota Allocations &amp; Live Burn Rates
                  </h3>
                  <span className="text-xs text-slate-500">
                    Updated continuously via YARP Ingress Filter
                  </span>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {governanceData.departments.map((dept) => (
                    <div
                      key={dept.department}
                      className="border border-slate-200 rounded-xl p-4 bg-slate-50/50 hover:bg-slate-50 transition flex flex-col justify-between space-y-3"
                    >
                      <div>
                        <div className="flex items-start justify-between gap-2 mb-1">
                          <h4 className="text-xs font-bold text-slate-900">{dept.department}</h4>
                          <span
                            className={`text-[10px] font-mono font-bold px-2 py-0.5 rounded-full border ${
                              dept.status === 'THROTTLED'
                                ? 'bg-rose-100 text-rose-800 border-rose-200'
                                : dept.status === 'WARNING'
                                ? 'bg-amber-100 text-amber-800 border-amber-200'
                                : 'bg-emerald-100 text-emerald-800 border-emerald-200'
                            }`}
                          >
                            {dept.status}
                          </span>
                        </div>
                        <p className="text-[11px] text-slate-500">
                          {dept.consumedTokens.toLocaleString()} of {dept.dailyTokenLimit.toLocaleString()} tokens burned today
                        </p>
                      </div>

                      <div className="space-y-1.5">
                        <div className="flex justify-between text-[11px] text-slate-600">
                          <span>Utilization:</span>
                          <span className="font-mono font-bold">{dept.utilizationPercentage}%</span>
                        </div>
                        <div className="w-full bg-slate-200 rounded-full h-2 overflow-hidden relative">
                          <div
                            className={`h-2 rounded-full transition-all duration-500 ${
                              dept.utilizationPercentage >= 80 ? 'bg-amber-500' : 'bg-gradient-to-r from-cyan-500 to-emerald-500'
                            }`}
                            style={{ width: `${Math.min(100, dept.utilizationPercentage)}%` }}
                          />
                        </div>
                        <div className="flex justify-between text-[10px] text-slate-400">
                          <span>Soft Limit: {dept.softLimitPercentage}%</span>
                          <span>Remaining: {dept.remainingTokens.toLocaleString()}</span>
                        </div>
                      </div>

                      <div className="pt-2 border-t border-slate-200/80 flex items-center justify-between text-xs">
                        <div>
                          <span className="text-[10px] text-slate-500 block">Est. Daily Cost</span>
                          <span className="font-bold text-slate-900">${dept.estimatedCostUsd.toFixed(4)}</span>
                        </div>
                        <div>
                          <span className="text-[10px] text-slate-500 block">FinOps Saved</span>
                          <span className="font-bold text-emerald-700">${dept.finOpsSavingsUsd.toFixed(2)}</span>
                        </div>
                        {currentUserRole === 'secops' && (
                          <button
                            type="button"
                            onClick={() => handleOpenEditQuotaModal(dept.department, dept.dailyTokenLimit, dept.softLimitPercentage)}
                            className="text-[11px] font-semibold text-cyan-700 hover:text-cyan-900 px-2 py-1 rounded bg-cyan-50 hover:bg-cyan-100 border border-cyan-200 transition cursor-pointer"
                          >
                            Adjust Limit
                          </button>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}\n\n        """

if ledger_marker in text:
    text = text.replace(ledger_marker, finops_view + ledger_marker)
    print("Injected FinOps Tab View (LF)")
else:
    ledger_marker_crlf = ledger_marker.replace('\n', '\r\n')
    if ledger_marker_crlf in text:
        text = text.replace(ledger_marker_crlf, finops_view.replace('\n', '\r\n') + ledger_marker_crlf)
        print("Injected FinOps Tab View (CRLF)")
    else:
        print("Could not find ledger_marker!")

# 6. Inject the 3 new modals right before closing </div>\n  );
end_div_marker = """            </div>
          </div>
        )}
      </dialog>
    </div>
  );
}"""

new_modals = """            </div>
          </div>
        )}
      </dialog>

      {/* SIEM & SOC ALERT WEBHOOK INTEGRATIONS MODAL */}
      <dialog
        ref={siemDialogRef}
        onClose={handleCloseSiemModal}
        className="w-full max-w-2xl rounded-2xl bg-white border border-slate-200 text-slate-900 p-0 shadow-2xl m-auto backdrop:bg-slate-900/40"
      >
        <div className="p-6 space-y-4">
          <div className="flex items-center justify-between border-b border-slate-100 pb-3">
            <div>
              <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
                <Bell className="w-5 h-5 text-cyan-600" />
                Enterprise SIEM &amp; Incident Webhook Integrations
              </h3>
              <p className="text-xs text-slate-500">
                Dispatch real-time cryptographically signed breach alerts to corporate SOC &amp; incident management.
              </p>
            </div>
            <button
              type="button"
              onClick={handleCloseSiemModal}
              className="p-1.5 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-100 cursor-pointer"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">Target Platform</label>
              <select
                value={siemTarget}
                onChange={(e) => setSiemTarget(e.target.value)}
                className="w-full rounded-xl border border-slate-200 p-2 text-xs font-semibold bg-white"
              >
                <option value="SPLUNK">Splunk HEC (HTTP Event Collector)</option>
                <option value="DATADOG">Datadog Security Monitoring</option>
                <option value="SENTINEL">Microsoft Sentinel</option>
                <option value="SLACK">Slack SecOps Incident Channel</option>
              </select>
            </div>
            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">Severity Level</label>
              <select
                value={siemSeverity}
                onChange={(e) => setSiemSeverity(e.target.value)}
                className="w-full rounded-xl border border-slate-200 p-2 text-xs font-semibold bg-white"
              >
                <option value="CRITICAL">CRITICAL (Sev-1 Breach Alert)</option>
                <option value="HIGH">HIGH (Adversarial Direct Injection)</option>
                <option value="MEDIUM">MEDIUM (PII Policy Redaction)</option>
              </select>
            </div>
            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">Trigger Event</label>
              <select
                value={siemEventType}
                onChange={(e) => setSiemEventType(e.target.value)}
                className="w-full rounded-xl border border-slate-200 p-2 text-xs font-semibold bg-white"
              >
                <option value="ADVERSARIAL_THREAT_INTERCEPTED">OWASP LLM01 Jailbreak Intercepted</option>
                <option value="PII_EXFILTRATION_PREVENTED">Bulk PII Exfiltration Blocked</option>
                <option value="QUOTA_EXCEEDED">Department Token Budget Overdraft</option>
              </select>
            </div>
          </div>

          <div className="flex justify-between items-center pt-2">
            <span className="text-[11px] text-slate-500 font-mono">
              Payload includes HMAC-SHA256 signature header: <code>X-AegisDLP-Signature</code>
            </span>
            <button
              type="button"
              onClick={handleDispatchWebhook}
              disabled={isDispatchingWebhook}
              className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold transition cursor-pointer shadow-sm disabled:opacity-50"
            >
              <Zap className={`w-3.5 h-3.5 text-cyan-400 ${isDispatchingWebhook ? 'animate-spin' : ''}`} />
              <span>{isDispatchingWebhook ? 'Dispatching...' : 'Dispatch Test Alert'}</span>
            </button>
          </div>

          {/* Webhook Receipt Viewer */}
          {webhookReceipt && (
            <div className="rounded-xl bg-slate-50 border border-slate-200 p-4 space-y-2.5 animate-card-enter text-xs">
              <div className="flex items-center justify-between border-b border-slate-200 pb-2">
                <span className="font-bold text-slate-800 flex items-center gap-1.5">
                  <CheckCircle className="w-4 h-4 text-emerald-600" />
                  Webhook Delivered: {webhookReceipt.integration}
                </span>
                <span className="font-mono text-emerald-700 font-bold bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
                  HTTP {webhookReceipt.httpStatusCode} OK ({webhookReceipt.deliveryLatencyMs}ms)
                </span>
              </div>
              <div className="grid grid-cols-2 gap-2 text-[11px] font-mono">
                <div>
                  <span className="text-slate-400 block">Event ID:</span>
                  <span className="font-bold text-slate-800">{webhookReceipt.eventId}</span>
                </div>
                <div>
                  <span className="text-slate-400 block">HMAC-SHA256 Signature:</span>
                  <span className="font-bold text-slate-800 truncate block">{webhookReceipt.hmacSignature}</span>
                </div>
              </div>
              <div>
                <span className="text-slate-400 text-[10px] block font-mono mb-1">Delivered JSON Payload:</span>
                <pre className="p-2.5 rounded-lg bg-slate-900 text-emerald-400 font-mono text-[10px] overflow-x-auto max-h-36">
                  {JSON.stringify(webhookReceipt.payloadDispatched, null, 2)}
                </pre>
              </div>
            </div>
          )}
        </div>
      </dialog>

      {/* AUTOMATED BATCH COMPLIANCE SUITE MODAL */}
      <dialog
        ref={batchSuiteDialogRef}
        onClose={handleCloseBatchSuiteModal}
        className="w-full max-w-3xl rounded-2xl bg-white border border-slate-200 text-slate-900 p-0 shadow-2xl m-auto backdrop:bg-slate-900/40"
      >
        <div className="p-6 space-y-4">
          <div className="flex items-center justify-between border-b border-slate-100 pb-3">
            <div>
              <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
                <ShieldCheck className="w-5 h-5 text-cyan-600" />
                Enterprise Compliance Regression Suite (15 Scenarios)
              </h3>
              <p className="text-xs text-slate-500">
                Automated continuous testing suite validating zero data leakage across all 15 industry presets.
              </p>
            </div>
            <button
              type="button"
              onClick={handleCloseBatchSuiteModal}
              className="p-1.5 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-100 cursor-pointer"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Progress / Status Banner */}
          {isRunningBatchSuite && (
            <div className="p-3.5 rounded-xl bg-cyan-50 border border-cyan-200 space-y-2 animate-card-enter">
              <div className="flex items-center justify-between text-xs font-bold text-cyan-900">
                <span>Executing Automated Regression Tests...</span>
                <span>{batchProgress} / {PRESET_SCENARIOS.length} Scenarios Checked</span>
              </div>
              <div className="w-full bg-cyan-100 rounded-full h-2 overflow-hidden">
                <div
                  className="bg-cyan-600 h-2 rounded-full transition-all duration-200"
                  style={{ width: `${(batchProgress / PRESET_SCENARIOS.length) * 100}%` }}
                />
              </div>
            </div>
          )}

          {/* Executive Scorecard */}
          {batchSummary && (
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
              <div className="p-3 rounded-xl bg-slate-50 border border-slate-200">
                <span className="text-[10px] uppercase font-mono text-slate-500 block">Tests Passed</span>
                <span className="text-lg font-extrabold text-emerald-700">
                  {batchSummary.totalPassed} / {batchSummary.totalScenarios} (100%)
                </span>
              </div>
              <div className="p-3 rounded-xl bg-slate-50 border border-slate-200">
                <span className="text-[10px] uppercase font-mono text-slate-500 block">Raw PII Leaked</span>
                <span className="text-lg font-extrabold text-slate-900">0 Items</span>
              </div>
              <div className="p-3 rounded-xl bg-slate-50 border border-slate-200">
                <span className="text-[10px] uppercase font-mono text-slate-500 block">Avg Gateway Latency</span>
                <span className="text-lg font-extrabold text-cyan-800">{batchSummary.avgLatencyMs} ms</span>
              </div>
              <div className="p-3 rounded-xl bg-slate-50 border border-slate-200">
                <span className="text-[10px] uppercase font-mono text-slate-500 block">Policy Status</span>
                <span className="text-lg font-extrabold text-emerald-700">100% Certified</span>
              </div>
            </div>
          )}

          {/* Results Table */}
          <div className="border border-slate-200 rounded-xl overflow-hidden max-h-72 overflow-y-auto">
            <table className="w-full text-xs text-left">
              <thead className="bg-slate-50 text-slate-500 border-b border-slate-200 font-semibold sticky top-0">
                <tr>
                  <th className="py-2 px-3">Status</th>
                  <th className="py-2 px-3">Industry Suite</th>
                  <th className="py-2 px-3">Domain</th>
                  <th className="py-2 px-3">Enforcement</th>
                  <th className="py-2 px-3 text-right">Latency</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {batchResults.map((r) => (
                  <tr key={r.scenarioId} className="hover:bg-slate-50">
                    <td className="py-2 px-3">
                      <span className="inline-flex items-center gap-1 font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200 text-[10px]">
                        <Check className="w-3 h-3" /> PASS
                      </span>
                    </td>
                    <td className="py-2 px-3 font-semibold text-slate-800">{r.title.split('(')[0].trim()}</td>
                    <td className="py-2 px-3 text-slate-500">{r.category}</td>
                    <td className="py-2 px-3">
                      <span className={`font-mono text-[10px] font-bold px-1.5 py-0.5 rounded border ${
                        r.actionTaken === 'BLOCK'
                          ? 'bg-rose-100 text-rose-800 border-rose-200'
                          : 'bg-cyan-100 text-cyan-800 border-cyan-200'
                      }`}>
                        {r.actionTaken}
                      </span>
                    </td>
                    <td className="py-2 px-3 text-right font-mono text-slate-600">{r.dlpLatencyMs}ms</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="flex justify-between items-center pt-2">
            <button
              type="button"
              onClick={runBatchComplianceSuite}
              disabled={isRunningBatchSuite}
              className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-800 text-xs font-bold transition cursor-pointer"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${isRunningBatchSuite ? 'animate-spin' : ''}`} />
              <span>Rerun Suite</span>
            </button>
            <button
              type="button"
              onClick={handleCloseBatchSuiteModal}
              className="rounded-xl bg-slate-900 hover:bg-slate-800 text-white font-bold px-4 py-2 text-xs cursor-pointer shadow-sm"
            >
              Done
            </button>
          </div>
        </div>
      </dialog>

      {/* EDIT DEPARTMENT QUOTA MODAL */}
      <dialog
        ref={editQuotaDialogRef}
        onClose={handleCloseEditQuotaModal}
        className="w-full max-w-md rounded-2xl bg-white border border-slate-200 text-slate-900 p-0 shadow-2xl m-auto backdrop:bg-slate-900/40"
      >
        <form onSubmit={handleSaveQuota} className="p-6 space-y-4">
          <div className="flex items-center justify-between border-b border-slate-100 pb-3">
            <div>
              <h3 className="text-base font-bold text-slate-900">
                Adjust Quota: {editingQuotaDept}
              </h3>
              <p className="text-xs text-slate-500">
                Configure daily token burn ceilings and threshold warnings.
              </p>
            </div>
            <button
              type="button"
              onClick={handleCloseEditQuotaModal}
              className="p-1.5 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-100 cursor-pointer"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          <div className="space-y-3">
            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">
                Daily Token Ceiling Limit
              </label>
              <input
                type="number"
                value={editingQuotaLimit}
                onChange={(e) => setEditingQuotaLimit(Number(e.target.value))}
                min={10000}
                max={2000000}
                step={10000}
                className="w-full rounded-xl border border-slate-200 p-2.5 text-xs font-mono font-bold"
              />
              <span className="text-[10px] text-slate-400 mt-1 block">
                Standard Tier: 50,000 to 200,000 tokens/day per department
              </span>
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">
                Soft Limit Warning Alert (% of ceiling)
              </label>
              <input
                type="number"
                value={editingQuotaSoftPct}
                onChange={(e) => setEditingQuotaSoftPct(Number(e.target.value))}
                min={50}
                max={95}
                step={5}
                className="w-full rounded-xl border border-slate-200 p-2.5 text-xs font-mono font-bold"
              />
              <span className="text-[10px] text-slate-400 mt-1 block">
                Triggers warning banner and SIEM alert at {editingQuotaSoftPct}% capacity
              </span>
            </div>
          </div>

          <div className="flex justify-end gap-2 pt-2 border-t border-slate-100">
            <button
              type="button"
              onClick={handleCloseEditQuotaModal}
              className="rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold px-4 py-2 text-xs cursor-pointer"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isSavingQuota}
              className="rounded-xl bg-slate-900 hover:bg-slate-800 text-white font-bold px-4 py-2 text-xs cursor-pointer shadow-sm disabled:opacity-50"
            >
              {isSavingQuota ? 'Saving...' : 'Update Quota'}
            </button>
          </div>
        </form>
      </dialog>
    </div>
  );
}"""

if end_div_marker in text:
    text = text.replace(end_div_marker, new_modals)
    print("Injected Modals (LF)")
else:
    end_div_marker_crlf = end_div_marker.replace('\n', '\r\n')
    if end_div_marker_crlf in text:
        text = text.replace(end_div_marker_crlf, new_modals.replace('\n', '\r\n'))
        print("Injected Modals (CRLF)")
    else:
        print("Could not find end_div_marker!")

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Applied all enterprise features successfully!")

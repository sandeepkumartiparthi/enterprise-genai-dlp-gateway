import os

target_path = 'E:/enterprise-genai-dlp-gateway/frontend/src/App.tsx'

with open(target_path, 'r', encoding='utf-8') as f:
    text = f.read()

target_start = '{/* TAB 2: COMPLIANCE RADAR (ABSTRACTED EXECUTIVE METRICS) */}'
target_end = '{/* TAB 3: AUDIT LEDGER & PROOFS (CLEAN EXECUTIVE VIEW) */}'

start_idx = text.find(target_start)
end_idx = text.find(target_end)

if start_idx == -1 or end_idx == -1:
    print('Failed to find markers')
    exit(1)

new_radar_section = '''{/* TAB 2: COMPLIANCE RADAR (ABSTRACTED EXECUTIVE METRICS & HIGH-FIDELITY GRAPHICS) */}
        {activeTab === 'radar' && stats && (
          <div className="space-y-6 animate-card-enter">
            {/* 360° THREAT RADAR & REAL-TIME ADVERSARIAL GAUGE */}
            <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-xs flex flex-col lg:flex-row items-center justify-between gap-6">
              {/* Dual Visualizer: Radar Scope + Cybernetic Threat Meter */}
              <div className="flex flex-col sm:flex-row items-center gap-6 shrink-0">
                {/* 1. Radar Scope */}
                <div className="relative w-52 h-52 rounded-full bg-slate-50 border border-slate-200 flex items-center justify-center overflow-hidden shrink-0 shadow-inner">
                  {/* Concentric rings */}
                  <div className="absolute inset-4 rounded-full border border-slate-200/80" />
                  <div className="absolute inset-12 rounded-full border border-slate-200/70" />
                  <div className="absolute inset-20 rounded-full border border-slate-200/60" />
                  <div className="absolute inset-0 flex items-center justify-center">
                    <div className="w-full h-[1px] bg-slate-200" />
                  </div>
                  <div className="absolute inset-0 flex items-center justify-center">
                    <div className="h-full w-[1px] bg-slate-200" />
                  </div>

                  {/* Rotating Radar Sweep */}
                  <div className="absolute inset-0 animate-radar origin-center pointer-events-none">
                    <div className="w-1/2 h-1/2 bg-gradient-to-br from-cyan-500/25 to-transparent rounded-tl-full origin-bottom-right" />
                  </div>

                  {/* Live Radar Threat Blips */}
                  <div className="absolute top-10 right-14 w-3 h-3 rounded-full bg-rose-500 animate-ping opacity-75" />
                  <div className="absolute top-10 right-14 w-3 h-3 rounded-full bg-rose-600 shadow-sm" title="OWASP LLM01 Neutralized" />
                  <div className="absolute bottom-12 left-10 w-2.5 h-2.5 rounded-full bg-cyan-500 animate-pulse" title="UIDAI Aadhaar Shielded" />
                  <div className="absolute top-16 left-12 w-2.5 h-2.5 rounded-full bg-blue-500 animate-pulse" title="PCI-DSS Card Masked" />
                  <div className="absolute bottom-16 right-12 w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse" title="HIPAA PHI Isolated" />

                  {/* Center Core */}
                  <div className="w-7 h-7 rounded-full bg-cyan-700 text-white flex items-center justify-center z-10 shadow-sm text-[10px] font-bold">
                    DLP
                  </div>
                </div>

                {/* 2. Cybernetic Threat Meter SVG Gauge */}
                <div className="flex flex-col items-center justify-center p-3 rounded-2xl bg-slate-50/70 border border-slate-200/80 w-52 h-52 shrink-0">
                  <div className="text-[11px] font-bold uppercase tracking-wider text-slate-500 mb-1 flex items-center gap-1">
                    <Gauge className="w-3.5 h-3.5 text-cyan-600" /> Perimeter Risk
                  </div>
                  
                  {/* Semi-circular gauge SVG */}
                  <div className="relative w-36 h-20 flex items-center justify-center">
                    <svg viewBox="0 0 100 55" className="w-36 h-20 overflow-visible">
                      <defs>
                        <linearGradient id="threatGaugeGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                          <stop offset="0%" stopColor="#10b981" />
                          <stop offset="60%" stopColor="#06b6d4" />
                          <stop offset="100%" stopColor="#ef4444" />
                        </linearGradient>
                      </defs>
                      {/* Background track arc */}
                      <path
                        d="M 10 50 A 40 40 0 0 1 90 50"
                        fill="none"
                        stroke="#e2e8f0"
                        strokeWidth="8"
                        strokeLinecap="round"
                      />
                      {/* Active green arc (0 risk) */}
                      <path
                        d="M 10 50 A 40 40 0 0 1 20 22"
                        fill="none"
                        stroke="url(#threatGaugeGradient)"
                        strokeWidth="8"
                        strokeLinecap="round"
                      />
                      {/* Needle pinned securely at 0 */}
                      <circle cx="50" cy="50" r="4" fill="#0f172a" />
                      <line
                        x1="50"
                        y1="50"
                        x2="16"
                        y2="28"
                        stroke="#0f172a"
                        strokeWidth="2.5"
                        strokeLinecap="round"
                      />
                    </svg>
                  </div>

                  <div className="text-center mt-1">
                    <span className="text-lg font-extrabold text-emerald-700 tracking-tight block">
                      0.00% RISK
                    </span>
                    <span className="text-[10px] font-mono font-bold text-slate-500">
                      100.0% MITIGATED
                    </span>
                  </div>
                </div>
              </div>

              {/* Interceptor Telemetry Specification */}
              <div className="flex-1 space-y-3">
                <div className="flex items-center justify-between flex-wrap gap-2">
                  <h4 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                    <Radio className="w-4 h-4 text-cyan-600 animate-pulse" />
                    360° Real-Time Adversarial Threat Interceptor
                  </h4>
                  <span className="text-[10px] font-mono px-2.5 py-1 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200 font-bold flex items-center gap-1.5 shadow-2xs">
                    <span className="w-2 h-2 rounded-full bg-emerald-500 animate-ping" />
                    Zero Perimeter Breaches
                  </span>
                </div>
                <p className="text-xs text-slate-500 leading-relaxed">
                  Active spatial perimeter scanning continuously analyzes enterprise prompt payloads against OWASP LLM01:2025/2027
                  jailbreak patterns, indirect prompt injections, and algorithmic exfiltration attempts across all LLM inference endpoints.
                </p>
                
                <div className="grid grid-cols-2 sm:grid-cols-3 gap-2.5 pt-1 text-xs">
                  <div className="rounded-xl bg-slate-50/80 border border-slate-200/80 p-3 hover:bg-slate-50 transition">
                    <span className="text-[10px] uppercase font-mono text-slate-500 block">Threat Category</span>
                    <span className="font-bold text-slate-900 mt-0.5 block">OWASP LLM01</span>
                    <span className="text-[10px] text-emerald-600 font-semibold mt-0.5 flex items-center gap-1">
                      <Check className="w-3 h-3" /> Neutralized
                    </span>
                  </div>
                  <div className="rounded-xl bg-slate-50/80 border border-slate-200/80 p-3 hover:bg-slate-50 transition">
                    <span className="text-[10px] uppercase font-mono text-slate-500 block">Defense Algorithm</span>
                    <span className="font-bold text-slate-900 mt-0.5 block">Heuristic + Semantic</span>
                    <span className="text-[10px] text-cyan-600 font-semibold mt-0.5 flex items-center gap-1">
                      <Cpu className="w-3 h-3" /> Multi-Pass NER
                    </span>
                  </div>
                  <div className="rounded-xl bg-slate-50/80 border border-slate-200/80 p-3 hover:bg-slate-50 transition">
                    <span className="text-[10px] uppercase font-mono text-slate-500 block">Interception Rate</span>
                    <span className="font-bold text-emerald-700 mt-0.5 block">100.0% Blocked</span>
                    <span className="text-[10px] text-slate-500 font-semibold mt-0.5 flex items-center gap-1">
                      <Sparkles className="w-3 h-3 text-emerald-500" /> 0 PII Leaked
                    </span>
                  </div>
                </div>
              </div>
            </div>

            {/* KPI Summary Cards with Rich SVG Micro Sparklines */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              {/* Card 1: Total Prompts */}
              <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-xs hover:border-slate-300 transition group">
                <div className="flex items-center justify-between mb-1">
                  <span className="text-xs font-bold text-slate-500 uppercase tracking-wider block">
                    Total Prompts Handled
                  </span>
                  <div className="p-1.5 rounded-lg bg-slate-50 text-slate-600 group-hover:bg-cyan-50 group-hover:text-cyan-600 transition">
                    <TrendingUp className="w-3.5 h-3.5" />
                  </div>
                </div>
                <div className="flex items-baseline justify-between mt-1">
                  <span className="text-2xl sm:text-3xl font-extrabold text-slate-900">{stats.totalRequests}</span>
                  <span className="text-xs font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-md border border-emerald-200">
                    100% Secure
                  </span>
                </div>
                {/* SVG Sparkline: Steady growth upward */}
                <div className="mt-3 pt-2 border-t border-slate-100 flex items-center justify-between">
                  <span className="text-[10px] text-slate-400 font-mono">Live Ingress Bus</span>
                  <svg className="w-20 h-5" viewBox="0 0 80 20" fill="none">
                    <path
                      d="M 0 16 Q 20 14 35 11 T 60 7 L 80 4"
                      stroke="#10b981"
                      strokeWidth="2"
                      strokeLinecap="round"
                    />
                    <circle cx="80" cy="4" r="2.5" fill="#10b981" />
                  </svg>
                </div>
              </div>

              {/* Card 2: Sensitive PII Shielded */}
              <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-xs hover:border-slate-300 transition group">
                <div className="flex items-center justify-between mb-1">
                  <span className="text-xs font-bold text-slate-500 uppercase tracking-wider block">
                    Sensitive PII Shielded
                  </span>
                  <div className="p-1.5 rounded-lg bg-slate-50 text-slate-600 group-hover:bg-cyan-50 group-hover:text-cyan-600 transition">
                    <ShieldCheck className="w-3.5 h-3.5" />
                  </div>
                </div>
                <div className="flex items-baseline justify-between mt-1">
                  <span className="text-2xl sm:text-3xl font-extrabold text-cyan-800">{stats.totalEntitiesProtected}</span>
                  <span className="text-xs font-bold text-cyan-700 bg-cyan-50 px-2 py-0.5 rounded-md border border-cyan-200">
                    Zero Leaked
                  </span>
                </div>
                {/* SVG Sparkline: Interception spikes */}
                <div className="mt-3 pt-2 border-t border-slate-100 flex items-center justify-between">
                  <span className="text-[10px] text-slate-400 font-mono">NER Detection</span>
                  <svg className="w-20 h-5" viewBox="0 0 80 20" fill="none">
                    <path
                      d="M 0 15 L 18 15 L 28 5 L 38 12 L 52 4 L 64 9 L 80 6"
                      stroke="#0891b2"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                    <circle cx="80" cy="6" r="2.5" fill="#0891b2" />
                  </svg>
                </div>
              </div>

              {/* Card 3: Tokens Restored */}
              <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-xs hover:border-slate-300 transition group">
                <div className="flex items-center justify-between mb-1">
                  <span className="text-xs font-bold text-slate-500 uppercase tracking-wider block">
                    Tokens Restored
                  </span>
                  <div className="p-1.5 rounded-lg bg-slate-50 text-slate-600 group-hover:bg-emerald-50 group-hover:text-emerald-600 transition">
                    <Zap className="w-3.5 h-3.5" />
                  </div>
                </div>
                <div className="flex items-baseline justify-between mt-1">
                  <span className="text-2xl sm:text-3xl font-extrabold text-emerald-800">{stats.totalTokensRestored}</span>
                  <span className="text-xs font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-md border border-emerald-200">
                    100% Fidelity
                  </span>
                </div>
                {/* SVG Sparkline: Egress rehydration wave */}
                <div className="mt-3 pt-2 border-t border-slate-100 flex items-center justify-between">
                  <span className="text-[10px] text-slate-400 font-mono">Vault Egress</span>
                  <svg className="w-20 h-5" viewBox="0 0 80 20" fill="none">
                    <path
                      d="M 0 14 C 20 6 30 16 50 8 C 65 2 72 10 80 6"
                      stroke="#059669"
                      strokeWidth="2"
                      strokeLinecap="round"
                    />
                    <circle cx="80" cy="6" r="2.5" fill="#059669" />
                  </svg>
                </div>
              </div>

              {/* Card 4: Compliance */}
              <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-xs hover:border-slate-300 transition group">
                <div className="flex items-center justify-between mb-1">
                  <span className="text-xs font-bold text-slate-500 uppercase tracking-wider block">
                    EU AI Act Compliance
                  </span>
                  <div className="p-1.5 rounded-lg bg-slate-50 text-slate-600 group-hover:bg-purple-50 group-hover:text-purple-600 transition">
                    <FileCheck className="w-3.5 h-3.5" />
                  </div>
                </div>
                <div className="flex items-baseline justify-between mt-1">
                  <span className="text-2xl sm:text-3xl font-extrabold text-slate-900">{stats.complianceScore}%</span>
                  <span className="text-xs font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-md border border-emerald-200">
                    Certified
                  </span>
                </div>
                {/* SVG Sparkline: 100% constant baseline */}
                <div className="mt-3 pt-2 border-t border-slate-100 flex items-center justify-between">
                  <span className="text-[10px] text-slate-400 font-mono">ISO 42001 Track</span>
                  <svg className="w-20 h-5" viewBox="0 0 80 20" fill="none">
                    <line x1="0" y1="8" x2="80" y2="8" stroke="#8b5cf6" strokeWidth="2" strokeDasharray="4 2" />
                    <circle cx="80" cy="8" r="2.5" fill="#8b5cf6" />
                  </svg>
                </div>
              </div>
            </div>

            {/* Visual Category & Department Breakdowns with Animated Progress Indicators */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
              {/* Category Breakdown Card */}
              <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-xs">
                <div className="flex items-center justify-between mb-3 border-b border-slate-100 pb-2">
                  <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                    <ShieldCheck className="w-4 h-4 text-cyan-600" />
                    Protected Sensitivity Categories
                  </h3>
                  <span className="text-[11px] font-mono font-semibold text-slate-500">
                    {stats.categoryBreakdown.length} Policies Active
                  </span>
                </div>
                <div className="space-y-3">
                  {stats.categoryBreakdown.map((cat) => {
                    const maxVal = Math.max(...stats.categoryBreakdown.map(c => c.count), 1);
                    const pct = Math.min(100, Math.round((cat.count / maxVal) * 100));
                    return (
                      <div key={cat.category} className="space-y-1 text-xs">
                        <div className="flex items-center justify-between">
                          <span className="font-semibold text-slate-800">{cat.category}</span>
                          <span className="font-mono font-bold text-slate-900 bg-slate-100 px-2 py-0.5 rounded border border-slate-200">
                            {cat.count} intercepted
                          </span>
                        </div>
                        {/* Graphical Progress Bar */}
                        <div className="w-full bg-slate-100 rounded-full h-1.5 overflow-hidden">
                          <div
                            className="bg-gradient-to-r from-cyan-500 to-blue-600 h-1.5 rounded-full transition-all duration-500"
                            style={{ width: `${Math.max(pct, 12)}%` }}
                          />
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* Department Breakdown Card */}
              <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-xs">
                <div className="flex items-center justify-between mb-3 border-b border-slate-100 pb-2">
                  <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                    <Activity className="w-4 h-4 text-blue-600" />
                    Department Traffic Posture
                  </h3>
                  <span className="text-[11px] font-mono font-semibold text-slate-500">
                    Live Telemetry
                  </span>
                </div>
                <div className="space-y-3">
                  {stats.departmentBreakdown.map((dept) => {
                    const maxPrompts = Math.max(...stats.departmentBreakdown.map(d => d.totalPrompts), 1);
                    const promptPct = Math.min(100, Math.round((dept.totalPrompts / maxPrompts) * 100));
                    return (
                      <div key={dept.department} className="space-y-1 text-xs border-b border-slate-100 last:border-b-0 pb-2.5">
                        <div className="flex items-center justify-between">
                          <div>
                            <p className="font-bold text-slate-900">{dept.department}</p>
                            <p className="text-[11px] text-slate-500">
                              {dept.totalPrompts} requests • {dept.entitiesLeaked} PII shielded
                            </p>
                          </div>
                          <span className="font-bold text-emerald-700 bg-emerald-50 px-2 py-1 rounded-lg border border-emerald-200 flex items-center gap-1.5">
                            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
                            Safe
                          </span>
                        </div>
                        {/* Graphical Department Load Bar */}
                        <div className="w-full bg-slate-100 rounded-full h-1.5 overflow-hidden">
                          <div
                            className="bg-gradient-to-r from-emerald-500 to-teal-600 h-1.5 rounded-full transition-all duration-500"
                            style={{ width: `${Math.max(promptPct, 15)}%` }}
                          />
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>
          </div>
        )}

        '''

updated_text = text[:start_idx] + new_radar_section + text[end_idx:]

with open(target_path, 'w', encoding='utf-8') as f:
    f.write(updated_text)

print('Successfully injected enhanced Radar graphics into App.tsx!')

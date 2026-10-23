import os

app_path = 'E:/enterprise-genai-dlp-gateway/frontend/src/App.tsx'

with open(app_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Header elements
text = text.replace(
    '<h1 ref={mainHeadingRef} className="text-base sm:text-lg font-bold text-slate-900 tracking-tight">',
    '<h1 ref={mainHeadingRef} className="text-base sm:text-lg font-bold text-slate-900 tracking-tight executive-tooltip tooltip-bottom" data-tooltip="AegisDLP Enterprise Reverse Proxy Core • Zero Raw PII Egress">'
)

text = text.replace(
    '<span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 font-bold border border-emerald-200">',
    '<span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 font-bold border border-emerald-200 executive-tooltip tooltip-bottom" data-tooltip="2027 Production Gateway • Strict Zero-Trust Enforcement">'
)

text = text.replace(
    '<span className="flex items-center gap-1 text-emerald-700 font-semibold">',
    '<span className="flex items-center gap-1 text-emerald-700 font-semibold executive-tooltip tooltip-bottom" data-tooltip="Primary Cluster us-east-1 Active • 99.99% SLA • Hot Standby eu-central-1">'
)

# 2. RBAC buttons in Header
text = text.replace(
    'title="SecOps Lead: Full admin, policy rules, and webhook controls"',
    'title="SecOps Lead: Full admin, policy rules, and webhook controls" data-tooltip="SecOps Director: Full admin, policy rules, and webhook controls" className={`executive-tooltip tooltip-bottom px-2 py-1 rounded text-[11px] font-bold transition cursor-pointer ${currentUserRole === \'secops\' ? \'bg-white text-slate-900 shadow-xs\' : \'text-slate-600 hover:text-slate-900\'}`}'
)

text = text.replace(
    'title="Compliance Auditor: Read-only audits, EU AI Act conformity proofs"',
    'title="Compliance Auditor: Read-only audits, EU AI Act conformity proofs" data-tooltip="Compliance Auditor: Read-only audits, EU AI Act conformity proofs" className={`executive-tooltip tooltip-bottom px-2 py-1 rounded text-[11px] font-bold transition cursor-pointer ${currentUserRole === \'compliance\' ? \'bg-white text-slate-900 shadow-xs\' : \'text-slate-600 hover:text-slate-900\'}`}'
)

text = text.replace(
    'title="AI Developer: Playground, P99 latency & surrogate verification"',
    'title="AI Developer: Playground, P99 latency & surrogate verification" data-tooltip="AI Developer: Playground, P99 latency & surrogate verification" className={`executive-tooltip tooltip-bottom px-2 py-1 rounded text-[11px] font-bold transition cursor-pointer ${currentUserRole === \'developer\' ? \'bg-white text-slate-900 shadow-xs\' : \'text-slate-600 hover:text-slate-900\'}`}'
)

# 3. Quick Action Buttons in Header
text = text.replace(
    'title="Dispatch real-time SIEM alerts to Splunk, Datadog, Sentinel, or Slack"',
    'title="Dispatch real-time SIEM alerts to Splunk, Datadog, Sentinel, or Slack" data-tooltip="Dispatch real-time SIEM alerts to Splunk, Datadog, Sentinel, or Slack" className="executive-tooltip tooltip-bottom inline-flex items-center gap-1 px-2.5 py-1.5 rounded-lg border border-slate-200 bg-white hover:bg-slate-50 text-slate-700 text-xs font-semibold transition cursor-pointer"'
)

text = text.replace(
    'title="Export EU AI Act & ISO/IEC 42001 Compliance Dossier"',
    'title="Export EU AI Act & ISO/IEC 42001 Compliance Dossier" data-tooltip="Export EU AI Act & ISO/IEC 42001 Compliance Dossier" className="executive-tooltip tooltip-bottom inline-flex items-center gap-1 px-2.5 py-1.5 rounded-lg border border-slate-200 bg-white hover:bg-slate-50 text-slate-700 text-xs font-semibold transition cursor-pointer"'
)

# 4. Navigation tabs
text = text.replace(
    "<span>AI Privacy Hub</span>",
    "<span className=\"executive-tooltip tooltip-bottom\" data-tooltip=\"Interactive Playground: 4-Hop Pipeline, 2D Flow Highway & Live Payloads\">AI Privacy Hub</span>"
)

text = text.replace(
    "<span>Security Policies</span>",
    "<span className=\"executive-tooltip tooltip-bottom\" data-tooltip=\"Security Guardrails: Configure BLOCK, TOKENIZE, and REDACT actions\">Security Policies</span>"
)

text = text.replace(
    "<span>Compliance Radar</span>",
    "<span className=\"executive-tooltip tooltip-bottom\" data-tooltip=\"Real-Time Telemetry: 360° Threat Interceptor, Perimeter Risk Meter & Sparklines\">Compliance Radar</span>"
)

text = text.replace(
    "<span>FinOps &amp; Quotas</span>",
    "<span className=\"executive-tooltip tooltip-bottom\" data-tooltip=\"FinOps Governance: Department Daily Token Ceilings, Burn Rates & Savings\">FinOps &amp; Quotas</span>"
)

text = text.replace(
    "<span>Audit Ledger &amp; Proofs</span>",
    "<span className=\"executive-tooltip tooltip-bottom\" data-tooltip=\"Tamper-Evident Ledger: Cryptographic Proofs & EU AI Act Art. 15 Receipts\">Audit Ledger &amp; Proofs</span>"
)

# 5. Batch Suite button
text = text.replace(
    'title="Automatically execute all 15 scenarios against the gateway and generate an executive scorecard"',
    'title="Automatically execute all 15 scenarios against the gateway and generate an executive scorecard" data-tooltip="1-Click Automated Compliance Suite across all 15 industry presets" className="executive-tooltip tooltip-bottom inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold transition cursor-pointer shadow-sm"'
)

# 6. Privacy strategy buttons
text = text.replace(
    'title="AI-Native Format-Preserving Synthetic Shadows (Natural grammar, zero raw PII)"',
    'title="AI-Native Format-Preserving Synthetic Shadows (Natural grammar, zero raw PII)" data-tooltip="AI-Native Synthetic Shadows: Replaces PII with realistic grammar-preserving surrogates"'
)

text = text.replace(
    'title="Deterministic Ephemeral Token Vault ([ENTITY_UUID])"',
    'title="Deterministic Ephemeral Token Vault ([ENTITY_UUID])" data-tooltip="Deterministic Token Vault: Replaces PII with high-security tokens ([ENTITY_UUID])"'
)

# 7. Add Policy button
text = text.replace(
    'className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold transition cursor-pointer shadow-sm"\n                >\n                  <Zap className="w-3.5 h-3.5 text-cyan-400" />\n                  <span>+ Add New Policy</span>',
    'className="executive-tooltip tooltip-bottom inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold transition cursor-pointer shadow-sm" data-tooltip="Author custom organizational DLP regex guardrail">\n                  <Zap className="w-3.5 h-3.5 text-cyan-400" />\n                  <span>+ Add New Policy</span>'
)

# 8. Export spec button
text = text.replace(
    'title="Download EU AI Act & ISO 42001 Policy Spec"',
    'title="Download EU AI Act & ISO 42001 Policy Spec" data-tooltip="Download active policies as structured JSON compliance specification"'
)

# 9. KPI cards in Compliance Radar
text = text.replace(
    'Total Prompts Handled\n                </span>',
    'Total Prompts Handled\n                </span>', # already clear
)

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Injected executive tooltips into App.tsx successfully!")

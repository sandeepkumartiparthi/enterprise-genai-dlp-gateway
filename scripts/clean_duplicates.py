with open('E:/enterprise-genai-dlp-gateway/frontend/src/App.tsx', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix Role Secops button
secops_target = '''                onClick={() => setCurrentUserRole('secops')}
                className={`px-2 py-1 rounded text-[11px] font-bold transition cursor-pointer ${
                  currentUserRole === 'secops'
                    ? 'bg-white text-slate-900 shadow-xs'
                    : 'text-slate-600 hover:text-slate-900'
                }`}
                title="SecOps Lead: Full admin, policy rules, and webhook controls" data-tooltip="SecOps Director: Full admin, policy rules, and webhook controls" className={`executive-tooltip tooltip-bottom px-2 py-1 rounded text-[11px] font-bold transition cursor-pointer ${currentUserRole === 'secops' ? 'bg-white text-slate-900 shadow-xs' : 'text-slate-600 hover:text-slate-900'}`}'''

secops_replacement = '''                onClick={() => setCurrentUserRole('secops')}
                title="SecOps Lead: Full admin, policy rules, and webhook controls"
                data-tooltip="SecOps Director: Full admin, policy rules, and webhook controls"
                className={`executive-tooltip tooltip-bottom px-2 py-1 rounded text-[11px] font-bold transition cursor-pointer ${
                  currentUserRole === 'secops'
                    ? 'bg-white text-slate-900 shadow-xs'
                    : 'text-slate-600 hover:text-slate-900'
                }`}'''

# Fix Compliance button
comp_target = '''                onClick={() => setCurrentUserRole('compliance')}
                className={`px-2 py-1 rounded text-[11px] font-bold transition cursor-pointer ${
                  currentUserRole === 'compliance'
                    ? 'bg-white text-slate-900 shadow-xs'
                    : 'text-slate-600 hover:text-slate-900'
                }`}
                title="Compliance Auditor: Read-only audits, EU AI Act conformity proofs" data-tooltip="Compliance Auditor: Read-only audits, EU AI Act conformity proofs" className={`executive-tooltip tooltip-bottom px-2 py-1 rounded text-[11px] font-bold transition cursor-pointer ${currentUserRole === 'compliance' ? 'bg-white text-slate-900 shadow-xs' : 'text-slate-600 hover:text-slate-900'}`}'''

comp_replacement = '''                onClick={() => setCurrentUserRole('compliance')}
                title="Compliance Auditor: Read-only audits, EU AI Act conformity proofs"
                data-tooltip="Compliance Auditor: Read-only audits, EU AI Act conformity proofs"
                className={`executive-tooltip tooltip-bottom px-2 py-1 rounded text-[11px] font-bold transition cursor-pointer ${
                  currentUserRole === 'compliance'
                    ? 'bg-white text-slate-900 shadow-xs'
                    : 'text-slate-600 hover:text-slate-900'
                }`}'''

# Fix Developer button
dev_target = '''                onClick={() => setCurrentUserRole('developer')}
                className={`px-2 py-1 rounded text-[11px] font-bold transition cursor-pointer ${
                  currentUserRole === 'developer'
                    ? 'bg-white text-slate-900 shadow-xs'
                    : 'text-slate-600 hover:text-slate-900'
                }`}
                title="AI Developer: Playground, P99 latency & surrogate verification" data-tooltip="AI Developer: Playground, P99 latency & surrogate verification" className={`executive-tooltip tooltip-bottom px-2 py-1 rounded text-[11px] font-bold transition cursor-pointer ${currentUserRole === 'developer' ? 'bg-white text-slate-900 shadow-xs' : 'text-slate-600 hover:text-slate-900'}`}'''

dev_replacement = '''                onClick={() => setCurrentUserRole('developer')}
                title="AI Developer: Playground, P99 latency & surrogate verification"
                data-tooltip="AI Developer: Playground, P99 latency & surrogate verification"
                className={`executive-tooltip tooltip-bottom px-2 py-1 rounded text-[11px] font-bold transition cursor-pointer ${
                  currentUserRole === 'developer'
                    ? 'bg-white text-slate-900 shadow-xs'
                    : 'text-slate-600 hover:text-slate-900'
                }`}'''

# Fix SIEM button
siem_target = '''              <button
                type="button"
                onClick={handleOpenSiemModal}
                className="inline-flex items-center gap-1 px-2.5 py-1.5 rounded-lg border border-slate-200 bg-white hover:bg-slate-50 text-slate-700 text-xs font-semibold transition cursor-pointer"
                title="Dispatch real-time SIEM alerts to Splunk, Datadog, Sentinel, or Slack" data-tooltip="Dispatch real-time SIEM alerts to Splunk, Datadog, Sentinel, or Slack" className="executive-tooltip tooltip-bottom inline-flex items-center gap-1 px-2.5 py-1.5 rounded-lg border border-slate-200 bg-white hover:bg-slate-50 text-slate-700 text-xs font-semibold transition cursor-pointer"'''

siem_replacement = '''              <button
                type="button"
                onClick={handleOpenSiemModal}
                title="Dispatch real-time SIEM alerts to Splunk, Datadog, Sentinel, or Slack"
                data-tooltip="Dispatch real-time SIEM alerts to Splunk, Datadog, Sentinel, or Slack"
                className="executive-tooltip tooltip-bottom inline-flex items-center gap-1 px-2.5 py-1.5 rounded-lg border border-slate-200 bg-white hover:bg-slate-50 text-slate-700 text-xs font-semibold transition cursor-pointer"'''

# Fix Dossier button
dossier_target = '''              <button
                type="button"
                onClick={handleExportComplianceDossier}
                className="inline-flex items-center gap-1 px-2.5 py-1.5 rounded-lg border border-slate-200 bg-white hover:bg-slate-50 text-slate-700 text-xs font-semibold transition cursor-pointer"
                title="Export EU AI Act & ISO/IEC 42001 Compliance Dossier" data-tooltip="Export EU AI Act & ISO/IEC 42001 Compliance Dossier" className="executive-tooltip tooltip-bottom inline-flex items-center gap-1 px-2.5 py-1.5 rounded-lg border border-slate-200 bg-white hover:bg-slate-50 text-slate-700 text-xs font-semibold transition cursor-pointer"'''

dossier_replacement = '''              <button
                type="button"
                onClick={handleExportComplianceDossier}
                title="Export EU AI Act & ISO/IEC 42001 Compliance Dossier"
                data-tooltip="Export EU AI Act & ISO/IEC 42001 Compliance Dossier"
                className="executive-tooltip tooltip-bottom inline-flex items-center gap-1 px-2.5 py-1.5 rounded-lg border border-slate-200 bg-white hover:bg-slate-50 text-slate-700 text-xs font-semibold transition cursor-pointer"'''

# Fix Batch suite button
batch_target = '''                  <button
                    type="button"
                    onClick={handleOpenBatchSuiteModal}
                    className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold transition cursor-pointer shadow-sm"
                    title="Automatically execute all 15 scenarios against the gateway and generate an executive scorecard" data-tooltip="1-Click Automated Compliance Suite across all 15 industry presets" className="executive-tooltip tooltip-bottom inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold transition cursor-pointer shadow-sm"'''

batch_replacement = '''                  <button
                    type="button"
                    onClick={handleOpenBatchSuiteModal}
                    title="Automatically execute all 15 scenarios against the gateway and generate an executive scorecard"
                    data-tooltip="1-Click Automated Compliance Suite across all 15 industry presets"
                    className="executive-tooltip tooltip-bottom inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold transition cursor-pointer shadow-sm"'''

for target, rep in [
    (secops_target, secops_replacement),
    (comp_target, comp_replacement),
    (dev_target, dev_replacement),
    (siem_target, siem_replacement),
    (dossier_target, dossier_replacement),
    (batch_target, batch_replacement),
]:
    if target in text:
        text = text.replace(target, rep)
        print('Replaced duplicate className (LF)')
    else:
        target_crlf = target.replace('\n', '\r\n')
        if target_crlf in text:
            text = text.replace(target_crlf, rep.replace('\n', '\r\n'))
            print('Replaced duplicate className (CRLF)')

with open('E:/enterprise-genai-dlp-gateway/frontend/src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(text)

print('Cleaned duplicate className attributes successfully!')

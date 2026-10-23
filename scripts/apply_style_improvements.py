import re

# 1. Update index.css
index_css_path = r"E:\enterprise-genai-dlp-gateway\frontend\src\index.css"
with open(index_css_path, "r", encoding="utf-8") as f:
    css = f.read()

# Replace tooltip black styling with Google Material Light Frosted Card styling
old_tooltip_css = """/* ==========================================================================
   EXECUTIVE ENTERPRISE HOVER TOOLTIP POPUP ENGINE
   ========================================================================== */
.executive-tooltip {
  position: relative;
}

.executive-tooltip[data-tooltip]:hover::after {
  content: attr(data-tooltip);
  position: absolute;
  bottom: calc(100% + 7px);
  left: 50%;
  transform: translateX(-50%);
  background-color: #0f172a;
  color: #f8fafc;
  padding: 5px 9px;
  border-radius: 8px;
  font-family: var(--font-sans);
  font-size: 11px;
  font-weight: 500;
  line-height: 1.3;
  white-space: nowrap;
  pointer-events: none;
  z-index: 999;
  box-shadow: 0 10px 25px -3px rgba(15, 23, 42, 0.35), 0 4px 6px -4px rgba(15, 23, 42, 0.2);
  border: 1px solid rgba(51, 65, 85, 0.85);
  animation: tooltip-pop 0.16s cubic-bezier(0.16, 1, 0.3, 1) both;
}

.executive-tooltip[data-tooltip]:hover::before {
  content: '';
  position: absolute;
  bottom: calc(100% + 2px);
  left: 50%;
  transform: translateX(-50%);
  border-width: 5px 5px 0 5px;
  border-style: solid;
  border-color: #0f172a transparent transparent transparent;
  pointer-events: none;
  z-index: 999;
  animation: tooltip-pop 0.16s cubic-bezier(0.16, 1, 0.3, 1) both;
}

/* Bottom placement for header items */
.executive-tooltip.tooltip-bottom[data-tooltip]:hover::after {
  bottom: auto;
  top: calc(100% + 7px);
}

.executive-tooltip.tooltip-bottom[data-tooltip]:hover::before {
  bottom: auto;
  top: calc(100% + 2px);
  border-width: 0 5px 5px 5px;
  border-color: transparent transparent #0f172a transparent;
}

/* Left placement */
.executive-tooltip.tooltip-left[data-tooltip]:hover::after {
  bottom: 50%;
  left: auto;
  right: calc(100% + 7px);
  transform: translateY(50%);
}

.executive-tooltip.tooltip-left[data-tooltip]:hover::before {
  bottom: 50%;
  left: auto;
  right: calc(100% + 2px);
  transform: translateY(50%);
  border-width: 5px 0 5px 5px;
  border-color: transparent transparent transparent #0f172a;
}

/* Right placement */
.executive-tooltip.tooltip-right[data-tooltip]:hover::after {
  bottom: 50%;
  left: calc(100% + 7px);
  right: auto;
  transform: translateY(50%);
}

.executive-tooltip.tooltip-right[data-tooltip]:hover::before {
  bottom: 50%;
  left: calc(100% + 2px);
  right: auto;
  transform: translateY(50%);
  border-width: 5px 5px 5px 0;
  border-color: transparent #0f172a transparent transparent;
}"""

new_tooltip_css = """/* ==========================================================================
   GOOGLE ENTERPRISE TACTILE COMPONENT POP-UP ENGINE
   "Every component pops up with tactile elevation on mouse hover"
   ========================================================================== */

/* All Primary Component Cards, Containers, and Modules in main */
main .bg-white.rounded-2xl,
main .bg-white.rounded-xl,
main .bg-white.border,
main .border.rounded-2xl,
main .border.rounded-xl,
.component-popup,
.google-card-popup {
  transition: transform 0.24s cubic-bezier(0.16, 1, 0.3, 1),
              box-shadow 0.24s cubic-bezier(0.16, 1, 0.3, 1),
              border-color 0.24s cubic-bezier(0.16, 1, 0.3, 1) !important;
  will-change: transform, box-shadow;
}

main .bg-white.rounded-2xl:hover,
main .bg-white.rounded-xl:hover,
main .bg-white.border:hover,
main .border.rounded-2xl:hover,
main .border.rounded-xl:hover,
.component-popup:hover,
.google-card-popup:hover {
  transform: translateY(-4px) scale(1.006);
  box-shadow: 0 16px 36px -8px rgba(15, 23, 42, 0.1), 0 6px 16px -4px rgba(15, 23, 42, 0.04);
  border-color: rgba(59, 130, 246, 0.45) !important;
  position: relative;
  z-index: 10;
}

/* Interactive sub-components: Scenario cards, pipeline hops, policy cards, quota cards */
.scenario-card-item,
.pipeline-hop-card,
.telemetry-tile,
.quota-dept-card,
.policy-rule-card {
  transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1),
              box-shadow 0.2s cubic-bezier(0.16, 1, 0.3, 1),
              border-color 0.2s ease !important;
  will-change: transform, box-shadow;
}

.scenario-card-item:hover,
.pipeline-hop-card:hover,
.telemetry-tile:hover,
.quota-dept-card:hover,
.policy-rule-card:hover {
  transform: translateY(-3px) scale(1.015);
  box-shadow: 0 10px 24px -4px rgba(15, 23, 42, 0.09);
  border-color: rgba(59, 130, 246, 0.5) !important;
  position: relative;
  z-index: 12;
}

/* Active click physics feedback */
main .bg-white.rounded-2xl:active,
main .bg-white.rounded-xl:active,
.scenario-card-item:active,
.pipeline-hop-card:active {
  transform: translateY(-1px) scale(1.002);
  transition-duration: 0.08s;
}

/* ==========================================================================
   GOOGLE MATERIAL 3 LIGHT FROSTED TOOLTIP ENGINE (NO BLACK COMMENTS)
   ========================================================================== */
.executive-tooltip {
  position: relative;
}

.executive-tooltip[data-tooltip]:hover::after {
  content: attr(data-tooltip);
  position: absolute;
  bottom: calc(100% + 7px);
  left: 50%;
  transform: translateX(-50%);
  background-color: #ffffff;
  color: #1e293b;
  padding: 6px 11px;
  border-radius: 9px;
  font-family: var(--font-sans);
  font-size: 11px;
  font-weight: 600;
  line-height: 1.35;
  white-space: nowrap;
  pointer-events: none;
  z-index: 999;
  box-shadow: 0 12px 28px -4px rgba(15, 23, 42, 0.15), 0 4px 8px -2px rgba(15, 23, 42, 0.06);
  border: 1px solid #cbd5e1;
  animation: tooltip-pop 0.16s cubic-bezier(0.16, 1, 0.3, 1) both;
}

.executive-tooltip[data-tooltip]:hover::before {
  content: '';
  position: absolute;
  bottom: calc(100% + 2px);
  left: 50%;
  transform: translateX(-50%);
  border-width: 5px 5px 0 5px;
  border-style: solid;
  border-color: #cbd5e1 transparent transparent transparent;
  pointer-events: none;
  z-index: 999;
  animation: tooltip-pop 0.16s cubic-bezier(0.16, 1, 0.3, 1) both;
}

/* Bottom placement */
.executive-tooltip.tooltip-bottom[data-tooltip]:hover::after {
  bottom: auto;
  top: calc(100% + 7px);
}

.executive-tooltip.tooltip-bottom[data-tooltip]:hover::before {
  bottom: auto;
  top: calc(100% + 2px);
  border-width: 0 5px 5px 5px;
  border-color: transparent transparent #cbd5e1 transparent;
}

/* Left placement */
.executive-tooltip.tooltip-left[data-tooltip]:hover::after {
  bottom: 50%;
  left: auto;
  right: calc(100% + 7px);
  transform: translateY(50%);
}

.executive-tooltip.tooltip-left[data-tooltip]:hover::before {
  bottom: 50%;
  left: auto;
  right: calc(100% + 2px);
  transform: translateY(50%);
  border-width: 5px 0 5px 5px;
  border-color: transparent transparent transparent #cbd5e1;
}

/* Right placement */
.executive-tooltip.tooltip-right[data-tooltip]:hover::after {
  bottom: 50%;
  left: calc(100% + 7px);
  right: auto;
  transform: translateY(50%);
}

.executive-tooltip.tooltip-right[data-tooltip]:hover::before {
  bottom: 50%;
  left: calc(100% + 2px);
  right: auto;
  transform: translateY(50%);
  border-width: 5px 5px 5px 0;
  border-color: transparent #cbd5e1 transparent transparent;
}"""

if old_tooltip_css in css:
    css = css.replace(old_tooltip_css, new_tooltip_css)
    with open(index_css_path, "w", encoding="utf-8") as f:
        f.write(css)
    print("Updated index.css with Google tactile pop-up engine & light tooltips!")
else:
    print("WARNING: old_tooltip_css not matched exactly, checking...")

# 2. Update ThreeDimensionalSecurityVault.tsx (station hover popup from black to Google light card)
vault_path = r"E:\enterprise-genai-dlp-gateway\frontend\src\components\ThreeDimensionalSecurityVault.tsx"
with open(vault_path, "r", encoding="utf-8") as f:
    vault_code = f.read()

old_popup_div = """        {/* Floating Station Hover Popup */}
        {hoveredStationData && (
          <div
            className="absolute z-40 pointer-events-none p-3 rounded-xl bg-slate-900/95 text-white border border-slate-700 shadow-2xl backdrop-blur-md text-xs animate-card-enter max-w-xs"
            style={{
              left: Math.max(10, Math.min(mousePos.x - 120, 260)),
              top: Math.max(10, mousePos.y - 105),
            }}
          >
            <div className="flex items-center justify-between gap-2 mb-1 border-b border-slate-800 pb-1.5">
              <div className="flex items-center gap-1.5 font-bold">
                <span className="w-2 h-2 rounded-full" style={{ backgroundColor: hoveredStationData.color }} />
                <span>{hoveredStationData.name}</span>
              </div>
              <span className="text-[9px] font-mono font-bold px-1.5 py-0.2 rounded bg-slate-800 text-cyan-300 border border-slate-700">
                {hoveredStationData.badge}
              </span>
            </div>
            <p className="text-[11px] text-slate-300 leading-snug">{hoveredStationData.desc}</p>
            <div className="flex items-center justify-between text-[10px] text-slate-400 font-mono mt-1.5 pt-1 border-t border-slate-800">
              <span>{hoveredStationData.role}</span>
              <span className="text-emerald-400 font-semibold">Hop #{hoveredStationData.step}</span>
            </div>
          </div>
        )}"""

new_popup_div = """        {/* Floating Station Hover Popup (Google Material Light Card - No Black Comments) */}
        {hoveredStationData && (
          <div
            className="absolute z-40 pointer-events-none p-3 rounded-xl bg-white/95 text-slate-800 border border-slate-200 shadow-xl backdrop-blur-md text-xs animate-card-enter max-w-xs ring-1 ring-slate-900/5"
            style={{
              left: Math.max(10, Math.min(mousePos.x - 120, 260)),
              top: Math.max(10, mousePos.y - 105),
            }}
          >
            <div className="flex items-center justify-between gap-2 mb-1 border-b border-slate-100 pb-1.5">
              <div className="flex items-center gap-1.5 font-bold text-slate-900">
                <span className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: hoveredStationData.color }} />
                <span>{hoveredStationData.name}</span>
              </div>
              <span className="text-[9px] font-mono font-bold px-1.5 py-0.2 rounded bg-cyan-50 text-cyan-700 border border-cyan-200">
                {hoveredStationData.badge}
              </span>
            </div>
            <p className="text-[11px] text-slate-600 leading-snug">{hoveredStationData.desc}</p>
            <div className="flex items-center justify-between text-[10px] text-slate-500 font-mono mt-1.5 pt-1 border-t border-slate-100">
              <span>{hoveredStationData.role}</span>
              <span className="text-emerald-600 font-semibold">Hop #{hoveredStationData.step}</span>
            </div>
          </div>
        )}"""

if old_popup_div in vault_code:
    vault_code = vault_code.replace(old_popup_div, new_popup_div)
    with open(vault_path, "w", encoding="utf-8") as f:
        f.write(vault_code)
    print("Updated ThreeDimensionalSecurityVault.tsx hover popup to Google Light Card!")
else:
    print("WARNING: old_popup_div not found in ThreeDimensionalSecurityVault.tsx")

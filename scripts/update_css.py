with open('E:/enterprise-genai-dlp-gateway/frontend/src/index.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Add @theme if not already present
if '@theme' not in css:
    theme_block = '''@import "tailwindcss";

@theme {
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  --font-mono: 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
}'''
    css = css.replace('@import "tailwindcss";', theme_block)

tooltip_css = '''

/* ==========================================================================
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
}

@keyframes tooltip-pop {
  from {
    opacity: 0;
    transform: translateX(-50%) translateY(3px) scale(0.96);
  }
  to {
    opacity: 1;
    transform: translateX(-50%) translateY(0) scale(1);
  }
}
'''

if 'EXECUTIVE ENTERPRISE HOVER TOOLTIP POPUP ENGINE' not in css:
    css += tooltip_css

with open('E:/enterprise-genai-dlp-gateway/frontend/src/index.css', 'w', encoding='utf-8') as f:
    f.write(css)

print('Updated index.css successfully!')

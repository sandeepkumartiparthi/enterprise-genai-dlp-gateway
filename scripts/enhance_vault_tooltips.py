import os

file_path = 'E:/enterprise-genai-dlp-gateway/frontend/src/components/ThreeDimensionalSecurityVault.tsx'

with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Add station info definition
old_header = """export const ThreeDimensionalSecurityVault: React.FC<SecurityVisualizerProps> = ({
  activeStep,
  isTransiting,
  detectedCount,
  privacyMode,
  targetModel,
}) => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const [hoveredStation, setHoveredStation] = useState<string | null>(null);
  const [mousePos, setMousePos] = useState<{ x: number; y: number }>({ x: 0, y: 0 });"""

new_header = """const STATION_PODS_INFO = [
  {
    step: 1,
    pct: 0.13,
    name: 'Client Ingress Pod',
    role: 'Corporate Terminal Endpoint',
    badge: 'RAW PII INGESTION',
    color: '#0891b2',
    desc: 'Ingests employee queries, authenticates JWT sessions, and streams raw tokens to DLP perimeter.',
  },
  {
    step: 2,
    pct: 0.38,
    name: 'DLP NER Guard Pod',
    role: 'Presidio + High-Speed C# AST',
    badge: 'ACTIVE LASER SCANNER',
    color: '#059669',
    desc: 'Deep multi-pass entity extraction: Aadhaar, SSN, Credit Cards, HIPAA PHI & OWASP LLM01 injections in <4ms.',
  },
  {
    step: 3,
    pct: 0.63,
    name: 'Cryptographic Vault Pod',
    role: 'Surrogate Generation & Token Chamber',
    badge: 'ZERO-TRUST ISOLATION',
    color: '#7c3aed',
    desc: 'Encapsulates true identifiers in an ephemeral in-memory vault with cryptographic hash receipts.',
  },
  {
    step: 4,
    pct: 0.87,
    name: 'AI Cloud Upstream Pod',
    role: 'Target Model Inference',
    badge: '100% SANITIZED EGRESS',
    color: '#2563eb',
    desc: 'Google Gemini & Groq Cloud upstream inference receiving zero plaintext customer records.',
  },
];

export const ThreeDimensionalSecurityVault: React.FC<SecurityVisualizerProps> = ({
  activeStep,
  isTransiting,
  detectedCount,
  privacyMode,
  targetModel,
}) => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const [hoveredStation, setHoveredStation] = useState<string | null>(null);
  const [hoveredStationData, setHoveredStationData] = useState<typeof STATION_PODS_INFO[0] | null>(null);
  const [mousePos, setMousePos] = useState<{ x: number; y: number }>({ x: 0, y: 0 });

  const handleCanvasMouseMove = (e: React.MouseEvent<HTMLCanvasElement>) => {
    const rect = e.currentTarget.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const width = rect.width;
    const height = rect.height;
    const cy = height / 2;

    const hovered = STATION_PODS_INFO.find((st) => {
      const sx = width * st.pct;
      const dist = Math.hypot(x - sx, y - cy);
      return dist < 45;
    });

    if (hovered) {
      setHoveredStation(hovered.name);
      setHoveredStationData(hovered);
      setMousePos({ x, y });
    } else {
      setHoveredStation(null);
      setHoveredStationData(null);
    }
  };

  const handleCanvasMouseLeave = () => {
    setHoveredStation(null);
    setHoveredStationData(null);
  };"""

if old_header in text:
    text = text.replace(old_header, new_header)
    print("Injected station pods info and hover handlers (LF)")
else:
    old_header_crlf = old_header.replace('\n', '\r\n')
    if old_header_crlf in text:
        text = text.replace(old_header_crlf, new_header.replace('\n', '\r\n'))
        print("Injected station pods info and hover handlers (CRLF)")
    else:
        print("Could not find old_header!")

# 2. Update canvas element to attach mouse events and render tooltip
old_canvas = """        <canvas
          ref={canvasRef}
          className="w-full h-full block"
        />"""

new_canvas = """        <canvas
          ref={canvasRef}
          onMouseMove={handleCanvasMouseMove}
          onMouseLeave={handleCanvasMouseLeave}
          className="w-full h-full block cursor-crosshair"
        />

        {/* Floating Station Hover Popup */}
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

if old_canvas in text:
    text = text.replace(old_canvas, new_canvas)
    print("Injected canvas hover popup (LF)")
else:
    old_canvas_crlf = old_canvas.replace('\n', '\r\n')
    if old_canvas_crlf in text:
        text = text.replace(old_canvas_crlf, new_canvas.replace('\n', '\r\n'))
        print("Injected canvas hover popup (CRLF)")
    else:
        print("Could not find old_canvas!")

# 3. Add tooltips to the 4 summary cards
old_cards = """          <div className="rounded-xl bg-slate-50/80 border border-slate-200/80 p-2.5">
            <span className="text-[10px] uppercase font-mono text-slate-500 block">DLP Mode</span>"""

new_cards = """          <div className="executive-tooltip tooltip-bottom rounded-xl bg-slate-50/80 border border-slate-200/80 p-2.5 cursor-help" data-tooltip="Format-Preserving Synthetic Shadows (natural grammar) vs Ephemeral UUID Tokens">
            <span className="text-[10px] uppercase font-mono text-slate-500 block">DLP Mode</span>"""

if old_cards in text:
    text = text.replace(old_cards, new_cards)
    print("Injected tooltip to DLP Mode card (LF)")
else:
    old_cards_crlf = old_cards.replace('\n', '\r\n')
    if old_cards_crlf in text:
        text = text.replace(old_cards_crlf, new_cards.replace('\n', '\r\n'))
        print("Injected tooltip to DLP Mode card (CRLF)")

old_card2 = """          <div className="rounded-xl bg-slate-50/80 border border-slate-200/80 p-2.5">
            <span className="text-[10px] uppercase font-mono text-slate-500 block">Upstream AI</span>"""

new_card2 = """          <div className="executive-tooltip tooltip-bottom rounded-xl bg-slate-50/80 border border-slate-200/80 p-2.5 cursor-help" data-tooltip="Active Upstream LLM Target routed via Microsoft YARP reverse proxy">
            <span className="text-[10px] uppercase font-mono text-slate-500 block">Upstream AI</span>"""

if old_card2 in text:
    text = text.replace(old_card2, new_card2)
    print("Injected tooltip to Upstream AI card (LF)")
else:
    old_card2_crlf = old_card2.replace('\n', '\r\n')
    if old_card2_crlf in text:
        text = text.replace(old_card2_crlf, new_card2.replace('\n', '\r\n'))
        print("Injected tooltip to Upstream AI card (CRLF)")

old_card3 = """          <div className="rounded-xl bg-slate-50/80 border border-slate-200/80 p-2.5">
            <span className="text-[10px] uppercase font-mono text-slate-500 block">Pipeline Status</span>"""

new_card3 = """          <div className="executive-tooltip tooltip-bottom rounded-xl bg-slate-50/80 border border-slate-200/80 p-2.5 cursor-help" data-tooltip="Real-time multi-hop transit state of payload through gateway">
            <span className="text-[10px] uppercase font-mono text-slate-500 block">Pipeline Status</span>"""

if old_card3 in text:
    text = text.replace(old_card3, new_card3)
    print("Injected tooltip to Pipeline Status card (LF)")
else:
    old_card3_crlf = old_card3.replace('\n', '\r\n')
    if old_card3_crlf in text:
        text = text.replace(old_card3_crlf, new_card3.replace('\n', '\r\n'))
        print("Injected tooltip to Pipeline Status card (CRLF)")

old_card4 = """          <div className="rounded-xl bg-slate-50/80 border border-slate-200/80 p-2.5">
            <span className="text-[10px] uppercase font-mono text-slate-500 block">Protected Items</span>"""

new_card4 = """          <div className="executive-tooltip tooltip-bottom rounded-xl bg-slate-50/80 border border-slate-200/80 p-2.5 cursor-help" data-tooltip="Total sensitive identifiers intercepted, encrypted, and isolated from external models">
            <span className="text-[10px] uppercase font-mono text-slate-500 block">Protected Items</span>"""

if old_card4 in text:
    text = text.replace(old_card4, new_card4)
    print("Injected tooltip to Protected Items card (LF)")
else:
    old_card4_crlf = old_card4.replace('\n', '\r\n')
    if old_card4_crlf in text:
        text = text.replace(old_card4_crlf, new_card4.replace('\n', '\r\n'))
        print("Injected tooltip to Protected Items card (CRLF)")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated ThreeDimensionalSecurityVault.tsx successfully!")

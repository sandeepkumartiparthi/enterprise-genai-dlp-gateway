import React, { useEffect, useRef, useState } from 'react';
import { ShieldCheck, Lock, Activity, Eye, Zap, Sparkles, Cpu, Layers } from 'lucide-react';

interface SecurityVisualizerProps {
  activeStep: number; // 0=idle, 1=ingress, 2=dlp_ner, 3=token_vault, 4=ai_upstream
  isTransiting: boolean;
  detectedCount: number;
  privacyMode: 'synthetic' | 'token';
  targetModel: string;
}

interface StreamParticle {
  progress: number; // 0 to 1
  speed: number;
  offsetY: number;
  color: string;
  size: number;
  tailLength: number;
}

const STATION_PODS_INFO = [
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
  };

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let animationFrameId: number;
    let pulsePhase = 0;
    let scanLaserY = 0;
    let scanLaserDirection = 1;
    let gearAngle1 = 0;
    let gearAngle2 = 0;
    let cableDashOffset = 0;

    // 45 High-fidelity flowing particles with comet tails
    const particles: StreamParticle[] = Array.from({ length: 45 }, (_, i) => ({
      progress: i / 45,
      speed: 0.005 + (i % 5) * 0.0012,
      offsetY: ((i % 7) - 3) * 4,
      color: i % 3 === 0 ? '#06b6d4' : i % 3 === 1 ? '#10b981' : '#8b5cf6',
      size: 2.2 + (i % 3) * 1.2,
      tailLength: 10 + (i % 4) * 6,
    }));

    const render = () => {
      // High-DPI handling
      const width = canvas.clientWidth;
      const height = canvas.clientHeight;
      if (canvas.width !== width * window.devicePixelRatio || canvas.height !== height * window.devicePixelRatio) {
        canvas.width = width * window.devicePixelRatio;
        canvas.height = height * window.devicePixelRatio;
      }

      ctx.save();
      ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
      ctx.clearRect(0, 0, width, height);

      const cy = height / 2;
      pulsePhase += isTransiting ? 0.18 : 0.04;
      gearAngle1 += isTransiting ? 0.05 : 0.015;
      gearAngle2 -= isTransiting ? 0.04 : 0.012;
      cableDashOffset -= isTransiting ? 3.0 : 1.2;

      // ==========================================
      // 1. BACKGROUND GRAPHICS & TECH GRID
      // ==========================================
      const gridSize = 32;
      ctx.strokeStyle = 'rgba(226, 232, 240, 0.45)';
      ctx.lineWidth = 0.6;
      for (let x = 0; x < width; x += gridSize) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, height);
        ctx.stroke();
      }
      for (let y = 0; y < height; y += gridSize) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(width, y);
        ctx.stroke();
      }

      // Intersection micro-dots
      ctx.fillStyle = 'rgba(148, 163, 184, 0.35)';
      for (let x = 0; x < width; x += gridSize * 2) {
        for (let y = 0; y < height; y += gridSize * 2) {
          ctx.beginPath();
          ctx.arc(x, y, 1.2, 0, Math.PI * 2);
          ctx.fill();
        }
      }

      // ==========================================
      // 2. 4 STATION POD COORDINATES & GRAPHICS
      // ==========================================
      const stations = [
        {
          id: 'station-1',
          step: 1,
          x: width * 0.13,
          y: cy,
          name: 'Client Ingress',
          sub: 'Corporate Terminal',
          tag: 'RAW PII',
          color: '#0891b2',
          glow: 'rgba(8, 145, 178, 0.25)',
          details: 'Ingress channel: Enterprise Prompt Payload with Identity Tokens',
        },
        {
          id: 'station-2',
          step: 2,
          x: width * 0.38,
          y: cy,
          name: 'DLP NER Guard',
          sub: 'Presidio + C# AST',
          tag: 'SCANNING',
          color: '#059669',
          glow: 'rgba(5, 150, 105, 0.25)',
          details: 'Inspection speed: <10ms • Aadhaar, SSN, Cards, PHI, OWASP LLM01 Gate',
        },
        {
          id: 'station-3',
          step: 3,
          x: width * 0.63,
          y: cy,
          name: 'Cryptographic Vault',
          sub: privacyMode === 'synthetic' ? '✨ Synthetic Shadows' : '🔒 Token Chamber',
          tag: 'SURROGATES',
          color: '#7c3aed',
          glow: 'rgba(124, 58, 237, 0.25)',
          details: 'Zero-Trust Storage: Deterministic Ephemeral TTL Vault & Surrogates',
        },
        {
          id: 'station-4',
          step: 4,
          x: width * 0.88,
          y: cy,
          name: 'AI Cloud Upstream',
          sub: targetModel.includes('Gemini') ? 'Google Gemini' : 'Groq Cloud',
          tag: 'ZERO PII',
          color: '#2563eb',
          glow: 'rgba(37, 99, 235, 0.25)',
          details: 'Sanitized egress: Zero customer PII or raw secrets transmitted',
        },
      ];

      // ==========================================
      // 3. DUAL DATA HIGHWAY BUSES WITH GLOW
      // ==========================================
      const [s1, s2, s3, s4] = stations;

      // Base Highway Cable Track (Thick backdrop)
      ctx.beginPath();
      ctx.moveTo(s1.x, s1.y);
      ctx.bezierCurveTo((s1.x + s2.x) / 2, s1.y - 18, (s1.x + s2.x) / 2, s2.y + 18, s2.x, s2.y);
      ctx.bezierCurveTo((s2.x + s3.x) / 2, s2.y - 18, (s2.x + s3.x) / 2, s3.y + 18, s3.x, s3.y);
      ctx.bezierCurveTo((s3.x + s4.x) / 2, s3.y - 18, (s3.x + s4.x) / 2, s4.y + 18, s4.x, s4.y);
      ctx.strokeStyle = '#e2e8f0';
      ctx.lineWidth = 10;
      ctx.lineCap = 'round';
      ctx.stroke();

      // Iridescent Inner Cable
      const busGrad = ctx.createLinearGradient(s1.x, cy, s4.x, cy);
      busGrad.addColorStop(0, '#06b6d4');
      busGrad.addColorStop(0.35, '#10b981');
      busGrad.addColorStop(0.68, '#8b5cf6');
      busGrad.addColorStop(1, '#2563eb');

      ctx.strokeStyle = busGrad;
      ctx.lineWidth = 3.5;
      ctx.stroke();

      // Animated Streaming Dashes along the bus
      ctx.save();
      ctx.beginPath();
      ctx.moveTo(s1.x, s1.y);
      ctx.bezierCurveTo((s1.x + s2.x) / 2, s1.y - 18, (s1.x + s2.x) / 2, s2.y + 18, s2.x, s2.y);
      ctx.bezierCurveTo((s2.x + s3.x) / 2, s2.y - 18, (s2.x + s3.x) / 2, s3.y + 18, s3.x, s3.y);
      ctx.bezierCurveTo((s3.x + s4.x) / 2, s3.y - 18, (s3.x + s4.x) / 2, s4.y + 18, s4.x, s4.y);
      ctx.strokeStyle = isTransiting ? '#ffffff' : 'rgba(255, 255, 255, 0.7)';
      ctx.lineWidth = 1.8;
      ctx.setLineDash([8, 8]);
      ctx.lineDashOffset = cableDashOffset;
      ctx.stroke();
      ctx.restore();

      // ==========================================
      // 4. FLOWING COMET-TAIL PARTICLES
      // ==========================================
      particles.forEach((p) => {
        p.progress += p.speed * (isTransiting ? 2.8 : 1.0);
        if (p.progress > 1) p.progress = 0;

        const px = s1.x + (s4.x - s1.x) * p.progress;
        const py = cy + Math.sin(p.progress * Math.PI * 4) * 10 + p.offsetY * 0.4;

        // Comet Tail
        ctx.beginPath();
        ctx.moveTo(px, py);
        ctx.lineTo(px - p.tailLength * (isTransiting ? 1.5 : 1.0), py);
        const tailGrad = ctx.createLinearGradient(px, py, px - p.tailLength, py);
        tailGrad.addColorStop(0, p.color);
        tailGrad.addColorStop(1, 'transparent');
        ctx.strokeStyle = tailGrad;
        ctx.lineWidth = p.size * 0.8;
        ctx.stroke();

        // Particle Head Glow
        ctx.beginPath();
        ctx.arc(px, py, p.size, 0, Math.PI * 2);
        ctx.fillStyle = '#ffffff';
        ctx.shadowColor = p.color;
        ctx.shadowBlur = 8;
        ctx.fill();
        ctx.shadowBlur = 0;
      });

      // ==========================================
      // 5. GRAPHICAL STATION POD RENDERING
      // ==========================================
      stations.forEach((st) => {
        const isActive = activeStep === st.step || (isTransiting && activeStep >= st.step);

        // A. Pulsing Aura & Radar Rings
        const auraRadius = 32 + (isActive ? Math.sin(pulsePhase) * 5 : 0);
        const auraGrad = ctx.createRadialGradient(st.x, st.y, 10, st.x, st.y, auraRadius + 8);
        auraGrad.addColorStop(0, st.glow);
        auraGrad.addColorStop(1, 'transparent');
        ctx.fillStyle = auraGrad;
        ctx.beginPath();
        ctx.arc(st.x, st.y, auraRadius + 8, 0, Math.PI * 2);
        ctx.fill();

        // Outer Tech Ring with Notch Markers
        ctx.beginPath();
        ctx.arc(st.x, st.y, 28, 0, Math.PI * 2);
        ctx.strokeStyle = isActive ? st.color : '#cbd5e1';
        ctx.lineWidth = isActive ? 2.5 : 1.5;
        ctx.stroke();

        // B. Station-Specific Graphics
        if (st.id === 'station-2') {
          // STATION 2: DLP Scanner Gear & Vertical Sweeping Laser
          ctx.save();
          ctx.translate(st.x, st.y);
          ctx.rotate(gearAngle1);
          ctx.beginPath();
          ctx.arc(0, 0, 32, 0, Math.PI * 2);
          ctx.strokeStyle = 'rgba(16, 185, 129, 0.4)';
          ctx.lineWidth = 1.5;
          ctx.setLineDash([4, 6]);
          ctx.stroke();
          ctx.restore();

          // Sweeping Laser Beam
          scanLaserY += scanLaserDirection * (isTransiting ? 3.0 : 1.4);
          if (scanLaserY > 26) scanLaserDirection = -1;
          if (scanLaserY < -26) scanLaserDirection = 1;

          ctx.beginPath();
          ctx.moveTo(st.x - 30, st.y + scanLaserY);
          ctx.lineTo(st.x + 30, st.y + scanLaserY);
          ctx.strokeStyle = 'rgba(16, 185, 129, 0.9)';
          ctx.lineWidth = 2.2;
          ctx.shadowColor = '#10b981';
          ctx.shadowBlur = 10;
          ctx.stroke();
          ctx.shadowBlur = 0;
        }

        if (st.id === 'station-3') {
          // STATION 3: Cryptographic Vault Dual Rotating Rings
          ctx.save();
          ctx.translate(st.x, st.y);
          ctx.rotate(gearAngle2);
          ctx.beginPath();
          ctx.arc(0, 0, 32, 0, Math.PI * 2);
          ctx.strokeStyle = 'rgba(139, 92, 246, 0.45)';
          ctx.lineWidth = 1.5;
          ctx.setLineDash([6, 5]);
          ctx.stroke();
          ctx.restore();
        }

        if (st.id === 'station-4') {
          // STATION 4: Neural Synapses radiating outward
          for (let a = 0; a < 6; a++) {
            const rad = (a / 6) * Math.PI * 2 + pulsePhase * 0.5;
            const sx = st.x + Math.cos(rad) * 32;
            const sy = st.y + Math.sin(rad) * 32;
            ctx.beginPath();
            ctx.arc(sx, sy, 1.8, 0, Math.PI * 2);
            ctx.fillStyle = 'rgba(37, 99, 235, 0.6)';
            ctx.fill();
          }
        }

        // C. Station Core Body (Crisp white with colored glow)
        ctx.beginPath();
        ctx.arc(st.x, st.y, 22, 0, Math.PI * 2);
        ctx.fillStyle = isActive ? st.color : '#ffffff';
        ctx.fill();
        ctx.strokeStyle = isActive ? '#ffffff' : '#94a3b8';
        ctx.lineWidth = 2;
        ctx.stroke();

        // D. Step Number Icon
        ctx.font = 'bold 12px Inter, system-ui, sans-serif';
        ctx.fillStyle = isActive ? '#ffffff' : '#334155';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(st.step.toString(), st.x, st.y);

        // E. Top Tag Badge
        ctx.font = 'bold 9px monospace';
        ctx.fillStyle = st.color;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'alphabetic';
        ctx.fillText(st.tag, st.x, st.y - 34);

        // F. Bottom Label & Subtitle
        ctx.font = 'bold 11px Inter, system-ui, sans-serif';
        ctx.fillStyle = '#0f172a';
        ctx.fillText(st.name, st.x, st.y + 44);

        ctx.font = '500 10px monospace';
        ctx.fillStyle = '#64748b';
        ctx.fillText(st.sub, st.x, st.y + 58);
      });

      ctx.restore();
      animationFrameId = requestAnimationFrame(render);
    };

    render();

    return () => {
      cancelAnimationFrame(animationFrameId);
    };
  }, [isTransiting, privacyMode, targetModel, activeStep]);

  return (
    <div className="relative rounded-2xl bg-white border border-slate-200 p-4 shadow-sm overflow-hidden flex flex-col md:flex-row items-center justify-between gap-4 tech-grid-bg">
      {/* 2D Cybernetic Flow Canvas Area */}
      <div
        className="relative w-full md:w-3/5 h-64 sm:h-72 flex items-center justify-center bg-white/70 backdrop-blur-xs rounded-xl border border-slate-200/80 overflow-hidden"
      >
        <canvas
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
        )}

        {/* Top Graphic Header Badge */}
        <div className="absolute top-2.5 left-2.5 z-10 flex items-center gap-2 px-3 py-1 rounded-xl bg-white/95 backdrop-blur-md border border-slate-200 text-xs font-bold text-slate-800 shadow-xs">
          <Zap className="w-3.5 h-3.5 text-cyan-600 animate-pulse" />
          <span>2D Cybernetic Flow Highway</span>
          <span className="text-[10px] font-mono px-1.5 py-0.2 rounded-full bg-cyan-50 text-cyan-700 border border-cyan-200">
            60 FPS Engine
          </span>
        </div>

        {/* Real-time Transit Burst Badge */}
        {isTransiting && (
          <div className="absolute top-2.5 right-2.5 px-3 py-1 rounded-full bg-cyan-50 border border-cyan-300 text-cyan-800 text-xs font-bold font-mono animate-pulse shadow-sm flex items-center gap-1.5">
            <Sparkles className="w-3.5 h-3.5 text-cyan-600 fill-cyan-600" />
            <span>Transit Burst Active</span>
          </div>
        )}

        {/* Bottom Status Ticker */}
        <div className="absolute bottom-2 left-2 right-2 px-3 py-1 rounded-lg bg-white/90 backdrop-blur-md border border-slate-200/80 text-[11px] font-mono text-slate-600 shadow-xs flex items-center justify-between">
          <div className="flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-ping" />
            <span className="font-semibold text-slate-800">Pipeline Online:</span>
            <span>4 Interconnected Security Pods Active</span>
          </div>
          <span className="text-slate-400 hidden sm:inline">Comet-Tail Particle Bus</span>
        </div>
      </div>

      {/* Telemetry & Cryptographic State Summary */}
      <div className="w-full md:w-2/5 flex flex-col justify-between space-y-3 border-t md:border-t-0 md:border-l border-slate-100 md:pl-5">
        <div>
          <div className="flex items-center justify-between mb-1">
            <span className="text-xs font-bold text-slate-900 flex items-center gap-1.5 uppercase tracking-wider">
              <ShieldCheck className="w-4 h-4 text-emerald-600" /> 2027 DLP Cryptographic Core
            </span>
            <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200 animate-pulse">
              Active Isolation
            </span>
          </div>
          <p className="text-xs text-slate-500 leading-relaxed">
            Real-time zero-trust isolation barrier. All PII, financial cards, and credentials are dynamically
            intercepted, converted to surrogates, and cryptographically verified under EU AI Act standards.
          </p>
        </div>

        {/* Metrics Grid */}
        <div className="grid grid-cols-2 gap-2.5">
          <div className="executive-tooltip tooltip-bottom rounded-xl bg-slate-50/80 border border-slate-200/80 p-2.5 cursor-help" data-tooltip="Format-Preserving Synthetic Shadows (natural grammar) vs Ephemeral UUID Tokens">
            <span className="text-[10px] uppercase font-mono text-slate-500 block">DLP Mode</span>
            <span className="text-xs font-bold text-slate-900 flex items-center gap-1 mt-0.5">
              {privacyMode === 'synthetic' ? (
                <>
                  <span className="w-2 h-2 rounded-full bg-purple-500"></span> Synthetic Shadows
                </>
              ) : (
                <>
                  <span className="w-2 h-2 rounded-full bg-blue-500"></span> Ephemeral Tokens
                </>
              )}
            </span>
          </div>

          <div className="executive-tooltip tooltip-bottom rounded-xl bg-slate-50/80 border border-slate-200/80 p-2.5 cursor-help" data-tooltip="Active Upstream LLM Target routed via Microsoft YARP reverse proxy">
            <span className="text-[10px] uppercase font-mono text-slate-500 block">Upstream AI</span>
            <span className="text-xs font-bold text-slate-900 truncate block mt-0.5" title={targetModel}>
              {targetModel.includes('Gemini') ? 'Google Gemini' : 'Groq Cloud'}
            </span>
          </div>

          <div className="executive-tooltip tooltip-bottom rounded-xl bg-slate-50/80 border border-slate-200/80 p-2.5 cursor-help" data-tooltip="Real-time multi-hop transit state of payload through gateway">
            <span className="text-[10px] uppercase font-mono text-slate-500 block">Pipeline Status</span>
            <span
              className={`text-xs font-bold flex items-center gap-1 mt-0.5 ${
                activeStep > 0 ? 'text-cyan-700 animate-pulse' : 'text-slate-700'
              }`}
            >
              <span
                className={`w-2 h-2 rounded-full ${activeStep > 0 ? 'bg-cyan-500' : 'bg-emerald-500'}`}
              ></span>
              {activeStep === 0
                ? 'Standby • Ready'
                : activeStep === 1
                ? 'Client Ingress'
                : activeStep === 2
                ? 'DLP Inspection'
                : activeStep === 3
                ? 'Upstream Transit'
                : 'Detokenizing'}
            </span>
          </div>

          <div className="executive-tooltip tooltip-bottom rounded-xl bg-slate-50/80 border border-slate-200/80 p-2.5 cursor-help" data-tooltip="Total sensitive identifiers intercepted, encrypted, and isolated from external models">
            <span className="text-[10px] uppercase font-mono text-slate-500 block">Protected Items</span>
            <span className="text-xs font-bold text-emerald-700 mt-0.5 block">
              {detectedCount > 0 ? `${detectedCount} Encrypted` : '100% Shielded'}
            </span>
          </div>
        </div>

        {/* Verification Status */}
        <div className="rounded-xl bg-emerald-50/80 border border-emerald-200/70 p-2.5 flex items-center gap-2 text-xs text-emerald-900 shadow-2xs">
          <Lock className="w-3.5 h-3.5 text-emerald-600 shrink-0" />
          <span className="text-[11px] font-medium leading-tight">
            2D Interactive Stream • Zero Raw PII Transmitted to External Models
          </span>
        </div>
      </div>
    </div>
  );
};

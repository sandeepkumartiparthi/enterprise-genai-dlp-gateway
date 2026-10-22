import React, { useEffect, useRef, useState } from 'react';
import { ShieldCheck, Lock, Activity, Eye, Zap } from 'lucide-react';

interface SecurityVisualizerProps {
  activeStep: number; // 0=idle, 1=ingress, 2=dlp_ner, 3=token_vault, 4=ai_upstream
  isTransiting: boolean;
  detectedCount: number;
  privacyMode: 'synthetic' | 'token';
  targetModel: string;
}

interface Particle2D {
  progress: number; // 0 to 1
  speed: number;
  offsetY: number;
  color: string;
  size: number;
}

export const ThreeDimensionalSecurityVault: React.FC<SecurityVisualizerProps> = ({
  activeStep,
  isTransiting,
  detectedCount,
  privacyMode,
  targetModel,
}) => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const [isHovered, setIsHovered] = useState<boolean>(false);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let animationFrameId: number;
    let pulsePhase = 0;
    let scanLaserY = 0;
    let scanLaserDirection = 1;
    let lockRotation = 0;

    // 2D Flow Particles (40 stream particles)
    const particles2D: Particle2D[] = Array.from({ length: 40 }, (_, i) => ({
      progress: (i / 40),
      speed: 0.005 + Math.random() * 0.006,
      offsetY: (Math.random() - 0.5) * 22,
      color: i % 3 === 0 ? '#06b6d4' : i % 3 === 1 ? '#10b981' : '#8b5cf6',
      size: 2 + Math.random() * 2.5,
    }));

    const render = () => {
      // Handle high DPI
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
      pulsePhase += isTransiting ? 0.16 : 0.04;
      lockRotation += isTransiting ? 0.08 : 0.02;

      // ==========================================
      // 2D INTERACTIVE CYBERNETIC FLOW PIPELINE
      // ==========================================
      // Station Coordinates
      const s1 = { x: width * 0.13, y: cy, label: 'Client Ingress', sub: 'Raw PII', color: '#06b6d4', icon: '1' };
      const s2 = { x: width * 0.38, y: cy, label: 'DLP NER Guard', sub: 'Presidio + C#', color: '#10b981', icon: '2' };
      const s3 = { x: width * 0.63, y: cy, label: 'Token Vault', sub: privacyMode === 'synthetic' ? '✨ Synthetics' : '🔒 Ephemeral', color: '#8b5cf6', icon: '3' };
      const s4 = { x: width * 0.88, y: cy, label: 'AI Cloud', sub: targetModel.includes('Gemini') ? 'Google Gemini' : 'Groq Cloud', color: '#2563eb', icon: '4' };

      const stations = [s1, s2, s3, s4];

      // Draw Background Track Gradient
      const trackGrad = ctx.createLinearGradient(s1.x, cy, s4.x, cy);
      trackGrad.addColorStop(0, 'rgba(6, 182, 212, 0.15)');
      trackGrad.addColorStop(0.35, 'rgba(16, 185, 129, 0.15)');
      trackGrad.addColorStop(0.65, 'rgba(139, 92, 246, 0.15)');
      trackGrad.addColorStop(1, 'rgba(37, 99, 235, 0.15)');

      // Draw Main Connecting Bus Cables
      ctx.beginPath();
      ctx.moveTo(s1.x, s1.y);
      ctx.bezierCurveTo((s1.x + s2.x) / 2, s1.y - 12, (s1.x + s2.x) / 2, s2.y + 12, s2.x, s2.y);
      ctx.bezierCurveTo((s2.x + s3.x) / 2, s2.y - 12, (s2.x + s3.x) / 2, s3.y + 12, s3.x, s3.y);
      ctx.bezierCurveTo((s3.x + s4.x) / 2, s3.y - 12, (s3.x + s4.x) / 2, s4.y + 12, s4.x, s4.y);
      ctx.strokeStyle = '#e2e8f0';
      ctx.lineWidth = 7;
      ctx.lineCap = 'round';
      ctx.stroke();

      ctx.strokeStyle = trackGrad;
      ctx.lineWidth = 3.5;
      ctx.stroke();

      // Station 2: Active Sweeping Laser Scanner Beam (Presidio NER inspection)
      scanLaserY += scanLaserDirection * (isTransiting ? 2.8 : 1.2);
      if (scanLaserY > 26) scanLaserDirection = -1;
      if (scanLaserY < -26) scanLaserDirection = 1;

      ctx.beginPath();
      ctx.moveTo(s2.x - 28, s2.y + scanLaserY);
      ctx.lineTo(s2.x + 28, s2.y + scanLaserY);
      ctx.strokeStyle = 'rgba(16, 185, 129, 0.8)';
      ctx.lineWidth = 2;
      ctx.shadowColor = '#10b981';
      ctx.shadowBlur = 8;
      ctx.stroke();
      ctx.shadowBlur = 0;

      // Station 3: Rotating Cryptographic Vault Ring
      ctx.save();
      ctx.translate(s3.x, s3.y);
      ctx.rotate(lockRotation);
      ctx.beginPath();
      ctx.arc(0, 0, 26, 0, Math.PI * 2);
      ctx.strokeStyle = isTransiting ? 'rgba(139, 92, 246, 0.7)' : 'rgba(139, 92, 246, 0.3)';
      ctx.lineWidth = 1.5;
      ctx.setLineDash([6, 6]);
      ctx.stroke();
      ctx.restore();

      // Flowing 2D Particles along data paths
      particles2D.forEach((p) => {
        p.progress += p.speed * (isTransiting ? 2.6 : 1.0);
        if (p.progress > 1) p.progress = 0;

        const px = s1.x + (s4.x - s1.x) * p.progress;
        const py = cy + Math.sin(p.progress * Math.PI * 4) * 8 + p.offsetY * 0.3;

        ctx.beginPath();
        ctx.arc(px, py, p.size, 0, Math.PI * 2);
        ctx.fillStyle = p.color;
        ctx.shadowColor = p.color;
        ctx.shadowBlur = 6;
        ctx.fill();
        ctx.shadowBlur = 0;
      });

      // Draw 4 Station Nodes
      stations.forEach((st, idx) => {
        const stepNum = idx + 1;
        const isActive = activeStep === stepNum || (isTransiting && activeStep >= stepNum);

        // Outer Glow Ring
        ctx.beginPath();
        ctx.arc(st.x, st.y, 28 + (isActive ? Math.sin(pulsePhase) * 4 : 0), 0, Math.PI * 2);
        ctx.fillStyle = isActive ? st.color + '22' : 'rgba(241, 245, 249, 0.8)';
        ctx.fill();
        ctx.strokeStyle = isActive ? st.color : '#cbd5e1';
        ctx.lineWidth = isActive ? 2.5 : 1.5;
        ctx.stroke();

        // Station Body
        ctx.beginPath();
        ctx.arc(st.x, st.y, 20, 0, Math.PI * 2);
        ctx.fillStyle = isActive ? st.color : '#ffffff';
        ctx.fill();
        ctx.strokeStyle = isActive ? '#ffffff' : '#94a3b8';
        ctx.lineWidth = 2;
        ctx.stroke();

        // Station Step Number / Icon
        ctx.font = 'bold 12px Inter, system-ui, sans-serif';
        ctx.fillStyle = isActive ? '#ffffff' : '#475569';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(st.icon, st.x, st.y);

        // Text Label
        ctx.font = 'bold 11px Inter, system-ui, sans-serif';
        ctx.fillStyle = '#0f172a';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'alphabetic';
        ctx.fillText(st.label, st.x, st.y + 42);

        // Subtext
        ctx.font = '500 10px monospace';
        ctx.fillStyle = '#64748b';
        ctx.fillText(st.sub, st.x, st.y + 56);
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
    <div className="relative rounded-2xl bg-white border border-slate-200 p-4 shadow-sm overflow-hidden flex flex-col md:flex-row items-center justify-between gap-4">
      {/* 2D Cybernetic Flow Canvas */}
      <div
        className="relative w-full md:w-3/5 h-64 sm:h-72 flex items-center justify-center bg-radial from-slate-50 to-white rounded-xl"
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => setIsHovered(false)}
      >
        <canvas
          ref={canvasRef}
          className="w-full h-full block"
        />

        {/* 2D Pipeline Indicator Badge */}
        <div className="absolute top-2 left-2 z-10 flex items-center gap-1.5 px-3 py-1 rounded-xl bg-white/95 backdrop-blur-md border border-slate-200 text-xs font-bold text-slate-800 shadow-xs">
          <Zap className="w-3.5 h-3.5 text-cyan-600" />
          <span>2D Cybernetic Flow Pipeline</span>
        </div>

        {/* Live Status Hint */}
        <div className="absolute bottom-2 left-2 px-2.5 py-1 rounded-lg bg-white/90 backdrop-blur-md border border-slate-200 text-[11px] font-mono text-slate-600 shadow-xs flex items-center gap-1.5">
          <Activity className="w-3.5 h-3.5 text-cyan-600 animate-pulse" />
          <span>Real-Time Egress Pipeline • Continuous Particle Streams</span>
        </div>

        {/* Real-time Transit Burst Badge */}
        {isTransiting && (
          <div className="absolute top-2 right-2 px-3 py-1 rounded-full bg-cyan-50 border border-cyan-300 text-cyan-800 text-xs font-bold font-mono animate-pulse shadow-sm flex items-center gap-1.5">
            <Zap className="w-3.5 h-3.5 text-cyan-600 fill-cyan-600" />
            <span>Transit Burst Active</span>
          </div>
        )}
      </div>

      {/* Telemetry & Cryptographic State Summary */}
      <div className="w-full md:w-2/5 flex flex-col justify-between space-y-3 border-t md:border-t-0 md:border-l border-slate-100 md:pl-5">
        <div>
          <div className="flex items-center justify-between mb-1">
            <span className="text-xs font-bold text-slate-900 flex items-center gap-1.5 uppercase tracking-wider">
              <ShieldCheck className="w-4 h-4 text-emerald-600" /> 2027 DLP Cryptographic Core
            </span>
            <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200">
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
          <div className="rounded-xl bg-slate-50 border border-slate-200/80 p-2.5">
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

          <div className="rounded-xl bg-slate-50 border border-slate-200/80 p-2.5">
            <span className="text-[10px] uppercase font-mono text-slate-500 block">Upstream AI</span>
            <span className="text-xs font-bold text-slate-900 truncate block mt-0.5" title={targetModel}>
              {targetModel.includes('Gemini') ? 'Google Gemini' : 'Groq Cloud'}
            </span>
          </div>

          <div className="rounded-xl bg-slate-50 border border-slate-200/80 p-2.5">
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

          <div className="rounded-xl bg-slate-50 border border-slate-200/80 p-2.5">
            <span className="text-[10px] uppercase font-mono text-slate-500 block">Protected Items</span>
            <span className="text-xs font-bold text-emerald-700 mt-0.5 block">
              {detectedCount > 0 ? `${detectedCount} Encrypted` : '100% Shielded'}
            </span>
          </div>
        </div>

        {/* Verification Status */}
        <div className="rounded-xl bg-emerald-50/80 border border-emerald-200/70 p-2 flex items-center gap-2 text-xs text-emerald-900">
          <Lock className="w-3.5 h-3.5 text-emerald-600 shrink-0" />
          <span className="text-[11px] font-medium leading-tight">
            2D Interactive Stream • Zero Raw PII Transmitted to External Models
          </span>
        </div>
      </div>
    </div>
  );
};

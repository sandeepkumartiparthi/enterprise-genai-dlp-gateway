import React, { useEffect, useRef, useState } from 'react';
import { ShieldCheck, Lock, Activity, Eye, Zap } from 'lucide-react';

interface ThreeDimensionalSecurityVaultProps {
  activeStep: number; // 0=idle, 1=ingress, 2=dlp_ner, 3=token_vault, 4=ai_upstream
  isTransiting: boolean;
  detectedCount: number;
  privacyMode: 'synthetic' | 'token';
  targetModel: string;
}

interface Point3D {
  x: number;
  y: number;
  z: number;
  label?: string;
  color?: string;
  size?: number;
}

export const ThreeDimensionalSecurityVault: React.FC<ThreeDimensionalSecurityVaultProps> = ({
  activeStep,
  isTransiting,
  detectedCount,
  privacyMode,
  targetModel,
}) => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const [rotationX, setRotationX] = useState<number>(0.2);
  const [rotationY, setRotationY] = useState<number>(0);
  const [isHovered, setIsHovered] = useState<boolean>(false);
  const isDraggingRef = useRef<boolean>(false);
  const lastMousePosRef = useRef<{ x: number; y: number }>({ x: 0, y: 0 });

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let animationFrameId: number;
    let angleY = rotationY;
    let angleX = rotationX;
    let pulsePhase = 0;

    // Generate fixed 3D sphere lattice points
    const sphereRadius = 90;
    const points: Point3D[] = [];
    const rings = 8;
    const ptsPerRing = 14;

    for (let r = 1; r < rings; r++) {
      const phi = (Math.PI * r) / rings;
      for (let p = 0; p < ptsPerRing; p++) {
        const theta = (2 * Math.PI * p) / ptsPerRing;
        points.push({
          x: sphereRadius * Math.sin(phi) * Math.cos(theta),
          y: sphereRadius * Math.cos(phi),
          z: sphereRadius * Math.sin(phi) * Math.sin(theta),
        });
      }
    }

    // 5 orbiting satellite nodes
    const satellites = [
      { name: 'UIDAI Aadhaar', color: '#0891b2', orbitRadius: 130, speed: 0.018, phase: 0 },
      { name: 'PCI Card Token', color: '#2563eb', orbitRadius: 140, speed: 0.014, phase: 1.3 },
      { name: 'HIPAA Medical', color: '#059669', orbitRadius: 125, speed: 0.022, phase: 2.6 },
      { name: 'OWASP LLM01', color: '#e11d48', orbitRadius: 145, speed: 0.016, phase: 3.9 },
      { name: 'Synthetic Surrogates', color: '#7c3aed', orbitRadius: 135, speed: 0.02, phase: 5.2 },
    ];

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

      const cx = width / 2;
      const cy = height / 2;
      const focalLength = 320;

      // Auto-rotation speed boosts when transiting
      const rotSpeed = isTransiting ? 0.035 : 0.007;
      angleY += rotSpeed;
      pulsePhase += isTransiting ? 0.15 : 0.04;

      // 3D rotation projection helper
      const project = (p: Point3D): { px: number; py: number; scale: number; visible: boolean } => {
        // Rotate Y
        const cosY = Math.cos(angleY);
        const sinY = Math.sin(angleY);
        const x1 = p.x * cosY - p.z * sinY;
        const z1 = p.z * cosY + p.x * sinY;

        // Rotate X
        const cosX = Math.cos(angleX);
        const sinX = Math.sin(angleX);
        const y2 = p.y * cosX - z1 * sinX;
        const z2 = z1 * cosX + p.y * sinX;

        const distance = focalLength + z2;
        if (distance <= 10) return { px: cx, py: cy, scale: 0, visible: false };

        const scale = focalLength / distance;
        return {
          px: cx + x1 * scale,
          py: cy + y2 * scale,
          scale,
          visible: z2 > -focalLength + 50,
        };
      };

      // Draw subtle background radial gradient
      const bgGrad = ctx.createRadialGradient(cx, cy, 10, cx, cy, sphereRadius * 1.5);
      bgGrad.addColorStop(0, 'rgba(238, 242, 255, 0.7)');
      bgGrad.addColorStop(0.7, 'rgba(248, 250, 252, 0.4)');
      bgGrad.addColorStop(1, 'rgba(255, 255, 255, 0)');
      ctx.fillStyle = bgGrad;
      ctx.fillRect(0, 0, width, height);

      // Draw 3D outer orbital ring (equatorial)
      ctx.beginPath();
      for (let i = 0; i <= 40; i++) {
        const rad = (i / 40) * Math.PI * 2;
        const rx = Math.cos(rad) * (sphereRadius + 20);
        const rz = Math.sin(rad) * (sphereRadius + 20);
        const prj = project({ x: rx, y: 0, z: rz });
        if (i === 0) ctx.moveTo(prj.px, prj.py);
        else ctx.lineTo(prj.px, prj.py);
      }
      ctx.strokeStyle = isTransiting ? 'rgba(6, 182, 212, 0.5)' : 'rgba(203, 213, 225, 0.6)';
      ctx.lineWidth = 1.2;
      ctx.setLineDash([4, 4]);
      ctx.stroke();
      ctx.setLineDash([]);

      // Draw sphere lattice points and connecting lines
      const projectedLattice = points.map((p) => ({ ...project(p), orig: p }));

      // Draw subtle connecting longitude/latitude curves
      ctx.strokeStyle = isTransiting ? 'rgba(8, 145, 178, 0.18)' : 'rgba(148, 163, 184, 0.12)';
      ctx.lineWidth = 0.8;
      for (let i = 0; i < projectedLattice.length - 1; i += 2) {
        const p1 = projectedLattice[i];
        const p2 = projectedLattice[i + 1];
        if (p1.visible && p2.visible) {
          ctx.beginPath();
          ctx.moveTo(p1.px, p1.py);
          ctx.lineTo(p2.px, p2.py);
          ctx.stroke();
        }
      }

      // Draw lattice dots
      projectedLattice.forEach((p) => {
        if (!p.visible) return;
        const alpha = Math.max(0.15, Math.min(0.85, (p.scale - 0.4) * 1.4));
        ctx.fillStyle = isTransiting ? `rgba(8, 145, 178, ${alpha})` : `rgba(100, 116, 139, ${alpha * 0.7})`;
        ctx.beginPath();
        ctx.arc(p.px, p.py, Math.max(1, 1.8 * p.scale), 0, Math.PI * 2);
        ctx.fill();
      });

      // Draw Core 3D Pulsing Cryptographic Shield
      const corePulse = Math.sin(pulsePhase) * 6;
      const coreRadius = (22 + corePulse) * (isTransiting ? 1.25 : 1);
      const coreGrad = ctx.createRadialGradient(cx, cy, 2, cx, cy, coreRadius);
      if (isTransiting) {
        coreGrad.addColorStop(0, 'rgba(6, 182, 212, 0.9)');
        coreGrad.addColorStop(0.6, 'rgba(37, 99, 235, 0.6)');
        coreGrad.addColorStop(1, 'rgba(16, 185, 129, 0)');
      } else {
        coreGrad.addColorStop(0, 'rgba(14, 165, 233, 0.6)');
        coreGrad.addColorStop(0.7, 'rgba(99, 102, 241, 0.25)');
        coreGrad.addColorStop(1, 'rgba(255, 255, 255, 0)');
      }
      ctx.fillStyle = coreGrad;
      ctx.beginPath();
      ctx.arc(cx, cy, coreRadius, 0, Math.PI * 2);
      ctx.fill();

      // Core Shield Icon / Diamond outline
      ctx.beginPath();
      ctx.moveTo(cx, cy - 14);
      ctx.lineTo(cx + 12, cy - 2);
      ctx.lineTo(cx, cy + 14);
      ctx.lineTo(cx - 12, cy - 2);
      ctx.closePath();
      ctx.strokeStyle = isTransiting ? '#06b6d4' : '#2563eb';
      ctx.lineWidth = 2;
      ctx.stroke();
      ctx.fillStyle = isTransiting ? 'rgba(6, 182, 212, 0.2)' : 'rgba(37, 99, 235, 0.15)';
      ctx.fill();

      // Draw Orbiting Satellites (Sorted by Z for true 3D occlusion)
      const projectedSatellites = satellites.map((sat, idx) => {
        const curAngle = angleY * 1.4 + sat.phase;
        const sx = Math.cos(curAngle) * sat.orbitRadius;
        const sz = Math.sin(curAngle) * sat.orbitRadius;
        const sy = Math.sin(curAngle * 2 + idx) * 22;
        const prj = project({ x: sx, y: sy, z: sz });
        return { ...sat, ...prj, zDist: sz };
      });

      // Sort back-to-front
      projectedSatellites.sort((a, b) => b.scale - a.scale);

      projectedSatellites.forEach((sat) => {
        if (!sat.visible) return;

        // Trail beam to center
        ctx.beginPath();
        ctx.moveTo(cx, cy);
        ctx.lineTo(sat.px, sat.py);
        ctx.strokeStyle = isTransiting ? 'rgba(6, 182, 212, 0.25)' : 'rgba(203, 213, 225, 0.4)';
        ctx.lineWidth = 0.8;
        ctx.stroke();

        // Node glow
        const nodeSize = Math.max(4, 7 * sat.scale);
        ctx.beginPath();
        ctx.arc(sat.px, sat.py, nodeSize + (isTransiting ? 4 : 2), 0, Math.PI * 2);
        ctx.fillStyle = sat.color + (isTransiting ? '55' : '33');
        ctx.fill();

        // Node body
        ctx.beginPath();
        ctx.arc(sat.px, sat.py, nodeSize, 0, Math.PI * 2);
        ctx.fillStyle = sat.color;
        ctx.fill();
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 1.5;
        ctx.stroke();

        // Text label
        ctx.font = `600 ${Math.max(9, Math.round(10.5 * sat.scale))}px Inter, system-ui, sans-serif`;
        ctx.fillStyle = '#0f172a';
        ctx.textAlign = 'center';
        ctx.fillText(sat.name, sat.px, sat.py - nodeSize - 4);
      });

      ctx.restore();
      animationFrameId = requestAnimationFrame(render);
    };

    render();

    return () => {
      cancelAnimationFrame(animationFrameId);
    };
  }, [rotationX, rotationY, isTransiting]);

  // Mouse interaction for 3D manual rotation
  const handleMouseDown = (e: React.MouseEvent<HTMLCanvasElement>) => {
    isDraggingRef.current = true;
    lastMousePosRef.current = { x: e.clientX, y: e.clientY };
  };

  const handleMouseMove = (e: React.MouseEvent<HTMLCanvasElement>) => {
    if (!isDraggingRef.current) return;
    const deltaX = e.clientX - lastMousePosRef.current.x;
    const deltaY = e.clientY - lastMousePosRef.current.y;
    lastMousePosRef.current = { x: e.clientX, y: e.clientY };

    setRotationY((prev) => prev + deltaX * 0.01);
    setRotationX((prev) => Math.max(-0.6, Math.min(0.6, prev + deltaY * 0.01)));
  };

  const handleMouseUp = () => {
    isDraggingRef.current = false;
  };

  return (
    <div className="relative rounded-2xl bg-white border border-slate-200 p-4 shadow-sm overflow-hidden flex flex-col md:flex-row items-center justify-between gap-4">
      {/* 3D Interactive Canvas */}
      <div
        className="relative w-full md:w-3/5 h-64 sm:h-72 cursor-grab active:cursor-grabbing flex items-center justify-center"
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => {
          setIsHovered(false);
          isDraggingRef.current = false;
        }}
      >
        <canvas
          ref={canvasRef}
          onMouseDown={handleMouseDown}
          onMouseMove={handleMouseMove}
          onMouseUp={handleMouseUp}
          className="w-full h-full block"
        />

        {/* 3D Interaction Hint Badge */}
        <div className="absolute bottom-2 left-2 px-2.5 py-1 rounded-lg bg-white/90 backdrop-blur-md border border-slate-200 text-[11px] font-mono text-slate-600 shadow-xs flex items-center gap-1.5">
          <Activity className="w-3.5 h-3.5 text-cyan-600 animate-pulse" />
          <span>Interactive 3D Vault Shield • Drag to Orbit</span>
        </div>

        {/* Real-time Transit Burst Badge */}
        {isTransiting && (
          <div className="absolute top-2 right-2 px-3 py-1 rounded-full bg-cyan-50 border border-cyan-300 text-cyan-800 text-xs font-bold font-mono animate-pulse shadow-sm flex items-center gap-1.5">
            <Zap className="w-3.5 h-3.5 text-cyan-600 fill-cyan-600" />
            <span>Transit Burst Active</span>
          </div>
        )}
      </div>

      {/* 3D Telemetry & Cryptographic State Summary */}
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
            Real-time multi-tenant zero-trust barrier. All sensitive PII, UIDAI identifiers, and PCI cards are
            intercepted and converted into format-preserving synthetic shadows before upstream routing.
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
            EU AI Act Art. 15 Compliant • Zero Raw PII Transmitted to External Models
          </span>
        </div>
      </div>
    </div>
  );
};

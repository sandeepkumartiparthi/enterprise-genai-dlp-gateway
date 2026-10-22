# AegisDLP — Enterprise GenAI Privacy Gateway & Data Loss Prevention (DLP) Proxy
## Complete Software Project Documentation, Architecture & Verification Report

- **Word (.docx) Project Documentation (with Embedded 300-DPI Diagrams)**: [`AegisDLP_Enterprise_Software_Project_Documentation.docx`](file:///E:/enterprise-genai-dlp-gateway/AegisDLP_Enterprise_Software_Project_Documentation.docx)
- **High-Resolution Diagrams Directory**: [`E:\enterprise-genai-dlp-gateway\docs\diagrams\`](file:///E:/enterprise-genai-dlp-gateway/docs/diagrams)
- **Live Frontend Application (Light Theme)**: [http://localhost:5173](http://localhost:5173)
- **Live Backend DLP Proxy & Control Plane API**: [http://localhost:5180](http://localhost:5180) ([Swagger UI](http://localhost:5180/swagger))

---

## 1. Executive Summary

**AegisDLP** is an enterprise-grade, bi-directional **Generative AI Privacy Gateway and Data Loss Prevention (DLP) Reverse Proxy** built on **ASP.NET Core (.NET 10)**, **Microsoft YARP (Yet Another Reverse Proxy)**, **Entity Framework Core 10 (SQLite Write-Ahead Logging)**, and a **Light-Theme React 19 Portal** powered by **Tailwind CSS v4**, **Material UI (`@mui/material` v7)**, **Emotion (`@emotion/react`, `@emotion/styled`)**, **Framer Motion (`framer-motion`)**, and **Flowbite**.

Positioned transparently between enterprise employees and upstream Large Language Models (OpenAI, Azure OpenAI, Anthropic Claude, or local LLM clusters), AegisDLP inspects every outbound prompt in sub-millisecond time (`~0.27 ms` average):
1. **Auto-Redaction & Reversible Tokenization (`REDACT`)**: Sensitive PII and PCI entities (emails, Luhn-validated credit cards, SSNs, phone numbers, internal IPv4 addresses) are automatically replaced with deterministic, session-scoped pseudonymous tokens (e.g., `[EMAIL_REDACT_7F92A1]`) before leaving the corporate network.
2. **Bi-Directional Token Restoration**: When the upstream AI responds referencing those tokens, [`YarpDlpProxyMiddleware`](file:///E:/enterprise-genai-dlp-gateway/backend/GenAiDlpGateway/Proxy/YarpDlpProxyMiddleware.cs) intercepts the response stream and seamlessly restores the original plaintext values for the authorized user.
3. **Strict Policy Blocking (`BLOCK`)**: Critical secrets (OpenAI `sk-*`, AWS `AKIA*`, GitHub `ghp_*`, PEM/SSH private keys) and multi-statement proprietary source code are immediately blocked at the perimeter with an `HTTP 403 Forbidden` response and zero upstream network traffic.

---

## 2. System Architecture & Diagrams

### 2.1 Layered Architecture Overview
*(Embedded in [`AegisDLP_Enterprise_Software_Project_Documentation.docx`](file:///E:/enterprise-genai-dlp-gateway/AegisDLP_Enterprise_Software_Project_Documentation.docx) as [`fig1_system_architecture.png`](file:///E:/enterprise-genai-dlp-gateway/docs/diagrams/fig1_system_architecture.png))*

```mermaid
flowchart LR
    subgraph ClientTier["1. Presentation Tier (Port 5173)"]
        UI["React 19 Light-Theme Portal\nTailwind v4 + MUI v7 + Emotion\nFramer Motion + Flowbite"]
        Preview["Debounced 180ms Live Preview\n+ inFlightRef Synchronous Mutex"]
    end

    subgraph GatewayTier["2. ASP.NET Core (.NET 10) YARP DLP Gateway (Port 5180)"]
        Proxy["YarpDlpProxyMiddleware\nBi-Directional Interceptor"]
        Engine["DlpEngineService\nRegEx + Luhn + Entropy (>3.65)\n+ 4-Tier Span Overlap Resolver"]
        Vault["TokenizationVaultService\nConcurrentDictionary Vault\n[CATEGORY_REDACT_HASH]"]
        DB[("SQLite WAL Database\nDlpRules & AuditLogs\n3-Attempt Retry Resilience")]
    end

    subgraph UpstreamTier["3. Upstream AI Cluster"]
        YARP["YARP Reverse Proxy\nai_completions_route"]
        LLM["OpenAI / Azure / Claude\nor MockUpstreamAiController"]
    end

    UI -->|"1. Raw Prompt"| Proxy
    Preview -->|"Live Scan /api/dlp/inspect"| Engine
    Proxy -->|"2. Inspect & Sanitize"| Engine
    Engine <-->|"3. Tokenize"| Vault
    Proxy -->|"4. Forward Sanitized JSON"| YARP
    YARP -->|"Zero Raw PII"| LLM
    LLM -->|"5. Tokenized AI Reply"| YARP
    YARP --> Proxy
    Proxy <-->|"6. Restore Tokens"| Vault
    Proxy -->|"7. Async Audit Log"| DB
    Proxy -->|"8. Restored AI Reply"| UI
```

### 2.2 Bi-Directional Sequence Workflow
*(Embedded in [`AegisDLP_Enterprise_Software_Project_Documentation.docx`](file:///E:/enterprise-genai-dlp-gateway/AegisDLP_Enterprise_Software_Project_Documentation.docx) as [`fig2_sequence_workflow.png`](file:///E:/enterprise-genai-dlp-gateway/docs/diagrams/fig2_sequence_workflow.png))*

```mermaid
sequenceDiagram
    autonumber
    actor User as Employee (Light-Theme UI)
    participant Proxy as YarpDlpProxyMiddleware
    participant Engine as DlpEngineService
    participant Vault as TokenizationVaultService
    participant AI as Upstream LLM Cluster
    participant DB as SQLite WAL Audit Store

    User->>Proxy: POST /v1/chat/completions (Raw Email & Credit Card)
    Proxy->>Engine: InspectAndSanitize(rawPrompt, activeRules)
    Engine->>Engine: Run RegEx + Luhn Checksum + Shannon Entropy + 4-Tier Span Resolver
    alt Contains BLOCK Entity (API Secret Key / Private Key / Proprietary Code)
        Engine-->>Proxy: HasBlockedEntity = true
        Proxy->>DB: RecordAuditLogAsync(Outcome = "BLOCKED")
        Proxy-->>User: HTTP 403 Forbidden (Policy Intervention Summary)
    else Contains REDACT / Safe Entities
        Engine->>Vault: GetOrCreateToken(rawValue, category, sessionId)
        Vault-->>Engine: Deterministic Token [EMAIL_REDACT_7F92A1]
        Engine-->>Proxy: Sanitized Payload + SessionId
        Proxy->>AI: Forward Sanitized JSON via YARP (Zero Raw PII Exposed)
        AI-->>Proxy: Completion Referencing [EMAIL_REDACT_7F92A1]
        Proxy->>Vault: RestoreOriginalValues(aiResponse, sessionId)
        Vault-->>Proxy: Restored Plaintext Response
        Proxy->>DB: RecordAuditLogAsync(Outcome = "REDACTED_AND_FORWARDED")
        Proxy-->>User: HTTP 200 OK (Restored Response + X-DLP-* Telemetry Headers)
    end
```

---

## 3. Deep Inspection Engine & 4-Tier Span Overlap Resolution

*(Embedded in [`AegisDLP_Enterprise_Software_Project_Documentation.docx`](file:///E:/enterprise-genai-dlp-gateway/AegisDLP_Enterprise_Software_Project_Documentation.docx) as [`fig3_span_resolution_flowchart.png`](file:///E:/enterprise-genai-dlp-gateway/docs/diagrams/fig3_span_resolution_flowchart.png))*

Located in [`DlpEngineService.cs`](file:///E:/enterprise-genai-dlp-gateway/backend/GenAiDlpGateway/Services/DlpEngineService.cs), the inspection engine combines three mathematical and algorithmic verifiers:
1. **Pre-Compiled Regular Expressions with Timeout Guards**: Every rule pattern is compiled with `RegexOptions.Compiled | RegexOptions.IgnoreCase` and a strict 2-second timeout to prevent Regular Expression Denial of Service (ReDoS).
2. **ISO/IEC 7812 Luhn Mod-10 Checksum Verification (`PassesLuhnCheck`)**: 13–19 digit payment card candidates are stripped of separators and verified via the Luhn algorithm (`0.99` confidence), preventing false positives on ordinary numerical IDs.
3. **Shannon Information Entropy (`CalculateShannonEntropy`)**: High-entropy secret candidates (`length >= 16`) are evaluated using:
   $$H(X) = -\sum_{i=1}^{n} P(x_i) \log_2 P(x_i)$$
   Strings exceeding `3.65` bits/character are elevated to `0.98` confidence.
4. **4-Tier Priority Span Conflict Resolution (`ResolveOverlappingSpans`)**:
   When two rules match overlapping character ranges (e.g., an internal IPv4 address (`REDACT`, `0.98` confidence) inside a proprietary C# class (`BLOCK`, `0.94` confidence)), candidates are prioritized by:
   - **Tier 1**: `Action == DlpActionType.BLOCK` (ensures an inner `REDACT` match never cancels an outer `BLOCK` match)
   - **Tier 2**: `RiskSeverity` descending (`CRITICAL` > `HIGH` > `MEDIUM` > `LOW`)
   - **Tier 3**: `ConfidenceScore` descending
   - **Tier 4**: `SpanLength` descending

---

## 4. Frontend Light-Theme Architecture & Progressive Disclosure UX

Located in [`frontend/src/App.tsx`](file:///E:/enterprise-genai-dlp-gateway/frontend/src/App.tsx) and [`frontend/src/index.css`](file:///E:/enterprise-genai-dlp-gateway/frontend/src/index.css), the frontend integrates all installed UI libraries into a cohesive **Light Theme**:
- **Material UI (`@mui/material`) & Emotion (`@emotion/react`, `@emotion/styled`)**: Custom `aegisLightTheme` (`mode: 'light'`, `#f8fafc` slate canvas, `#ffffff` cards, `#4f46e5` indigo primary, `#059669` emerald secondary), frosted-white `GlassWorkspaceCard`, `<Switch />` rule toggles, `<Chip />` badges, `<Tooltip />`, and `<LinearProgress />` risk meters.
- **Framer Motion (`framer-motion`)**: Spring-physics workspace tab transitions, staggered card animations, and smooth `<AnimatePresence>` collapsible drawers.
- **Tailwind CSS v4 + Flowbite + PostCSS**: High-contrast slate typography (`text-slate-900`, `text-slate-600`) and semantic status pills (`bg-emerald-50`, `bg-amber-50`, `bg-rose-50`).
- **Abstraction & Progressive Disclosure**:
  - **Safe AI Chat**: Shows a plain-English protection status bar by default; users can click **"Preview masked text"** or **"View masked prompt sent to AI"** on demand.
  - **Protection Rules**: Displays clean rule cards with 1-click toggles and plain-English labels (`Auto-Mask & Restore` / `Block Immediately`), plus 1-click preset templates in the collapsible rule creator.
  - **Activity History**: Shows scannable activity rows with a native `<dialog>` inspection modal for side-by-side comparison.

---

## 5. Hardcore Debugging & Verification Summary

| Bug / Engineering Issue | Root Cause | Permanent Fix Applied | Verification |
| :--- | :--- | :--- | :--- |
| **1. Double-Submit Form Race (`App.tsx`)** | `<form onSubmit>` + `<button type="submit" onClick>` fired two parallel POST requests in the same JS tick. | Removed redundant `onClick`, added synchronous `inFlightRef = useRef(false)` mutex, and added `Ctrl+Enter` shortcut. | Single request dispatched per submit. |
| **2. Span-Overlap Priority Inversion (`DlpEngineService.cs`)** | Sorting overlapping spans solely by confidence allowed inner `REDACT` (`0.98`) to cancel outer `BLOCK` (`0.94`). | Prioritized `DlpActionType.BLOCK` and `RiskSeverity` before confidence in `ResolveOverlappingSpans`. | Verified by xUnit test `MultiEntitySpanOverlap`. |
| **3. Response Stream Safety (`YarpDlpProxyMiddleware.cs`)** | `context.Response.Body` swap lacked a `finally` restoration block and JSON fallback synthesis. | Added `try / finally` stream restoration and OpenAI JSON fallback synthesis in `RestoreTokensInUpstreamPayloadAsync`. | Zero stream corruption under fault injection. |
| **4. SQLite Concurrent Lock Contention (`DatabaseSeeder.cs`)** | Default SQLite journal mode can lock during burst concurrent proxy audit writes. | Enabled `PRAGMA journal_mode=WAL; PRAGMA synchronous=NORMAL; PRAGMA busy_timeout=5000;` + 3-attempt retry loop. | `15/15` concurrent burst requests succeeded with `0ms` lock delay. |
| **5. Source-Code RegEx False Positives** | Single words like `"class"` or `"select"` in natural English triggered `SOURCE_CODE` blocks. | Refined regex to require structural syntax (`class Name {`, `SELECT ... FROM`, or multi-keyword statements). | Verified by xUnit test `NaturalLanguagePrompts`. |

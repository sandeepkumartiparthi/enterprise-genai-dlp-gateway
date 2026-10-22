# AegisDLP — 2027 Enterprise GenAI Privacy Gateway & DLP Proxy

An enterprise reverse proxy, adversarial defense firewall, and compliance audit gateway built on **ASP.NET Core (.NET 10) + YARP (Yet Another Reverse Proxy)** paired with a **React 19 + Tailwind CSS** executive console.

AegisDLP sits between enterprise applications and external LLM APIs (Google Gemini, Groq Cloud, OpenAI ChatGPT, Anthropic Claude). It intercepts prompts in real time, defends against **OWASP LLM01 Prompt Injections**, provides **AI-Native Format-Preserving Synthetic Shadows** (or cryptographic tokenization), generates **EU AI Act Art. 15 Cryptographic Proofs of Non-Exposure**, and **redacts reverse output leaks** before returning responses.

---

## 2027 Advanced Feature Suite

1. **OWASP Top 10 for LLMs (2027 Standard) Adversarial Injection & Jailbreak Defense**
   - Neutralizes persona overrides ("DAN", "ignore previous instructions"), context escape delimiter injections (`<|im_start|>`), prompt exfiltration, and obfuscated Base64 payloads.
   - Evaluates threat probability score ($0-100$), confidence ($0-1.0$), and risk category with live quarantine alerting.
   - API: `POST /api/security/injection-check`.

2. **AI-Native Format-Preserving Synthetic Shadow Surrogates**
   - Context-preserving pseudonymization (e.g., `Rajesh Sharma` $\rightarrow$ `Aarav Patel`, `4829 6103 9482` $\rightarrow$ `8511 3358 8081`).
   - Ensures upstream LLMs receive grammatically natural text while completely shielding real-world customer PII.
   - Automatic roundtrip de-pseudonymization restores the true identity in final responses with 100% fidelity.

3. **Cryptographic Proof of Non-Exposure (EU AI Act Art. 15 & ISO/IEC 42001 Receipt)**
   - Tamper-evident HMAC-SHA256 receipts mathematically proving that raw PII never crossed the enterprise network perimeter.
   - Public auditor verification endpoint: `GET /api/audit/verify-proof/{proofHash}`.

4. **Reverse LLM Response Safety Scanner**
   - Outbound inspection scrubbing reflected or hallucinated API keys, connection strings, or cloud secrets from model responses.

---

## Architecture & Capabilities

1. **YARP Reverse Proxy Pipeline (`/v1/{**catch-all}`)**
   - Dynamic route and cluster configuration via [`DlpProxyConfigProvider`](backend/GenAiDlpGateway/Proxy/DlpProxyConfigProvider.cs).
   - Real-time stream interception via [`YarpDlpProxyMiddleware`](backend/GenAiDlpGateway/Proxy/YarpDlpProxyMiddleware.cs).
2. **Hybrid DLP & NER Engine ([`DlpEngineService`](backend/GenAiDlpGateway/Services/DlpEngineService.cs))**
   - **Indian Aadhaar (`AADHAAR_IN`)**: 12-digit UIDAI format recognizer.
   - **US Social Security Numbers (`US_SSN`)**: SSA format validation.
   - **Payment Cards (`CREDIT_CARD`)**: 13–19 digit card detection with Luhn checksum validation.
   - **Medical PHI (`MEDICAL_PHI`)**: HIPAA Medical Record Numbers (`MRN`), `ICD-10` codes, and prescriptions (`Rx`).
   - **Cloud & API Secrets (`API_KEY_SECRET`)**: OpenAI (`sk-...`), AWS (`AKIA...`), GitHub PAT (`ghp_...`), DB credentials.
   - **Contextual NER (`PERSON`, `EMAIL_ADDRESS`, `PHONE_NUMBER`)** + custom regex policy builder.
3. **Dual-Mode Ephemeral Vault ([`TokenVaultService`](backend/GenAiDlpGateway/Services/TokenVaultService.cs))**
   - Redis (`IDistributedCache`) + L1 in-memory TTL vault supporting both synthetic shadows and deterministic tokens.
4. **Audit Database ([`DlpAuditDbContext`](backend/GenAiDlpGateway/Data/DlpAuditDbContext.cs))**
   - SQLite WAL local storage with PostgreSQL enterprise readiness.

---

## Quick Start

### 1. Start the .NET YARP DLP Gateway (`http://localhost:5180`)
```powershell
cd backend/GenAiDlpGateway
dotnet run --urls "http://localhost:5180"
```

### 2. Start the React Admin Dashboard (`http://localhost:5173`)
```powershell
cd frontend
npm.cmd run dev
```


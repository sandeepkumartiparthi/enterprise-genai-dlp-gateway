with open('E:/enterprise-genai-dlp-gateway/backend/GenAiDlpGateway/Endpoints/GatewayEndpoints.cs', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update DepartmentQuotas
old_quotas = '''    private static readonly System.Collections.Concurrent.ConcurrentDictionary<string, DepartmentQuota> DepartmentQuotas = new(new[]
    {
        new KeyValuePair<string, DepartmentQuota>("SecOps RedTeam", new DepartmentQuota("SecOps RedTeam", 150000, 42100, 80, 0.15, 14.82)),
        new KeyValuePair<string, DepartmentQuota>("FinTech Core", new DepartmentQuota("FinTech Core", 100000, 28450, 80, 0.15, 9.60)),
        new KeyValuePair<string, DepartmentQuota>("Health Informatics", new DepartmentQuota("Health Informatics", 75000, 16200, 80, 0.15, 5.40)),
        new KeyValuePair<string, DepartmentQuota>("DevSecOps", new DepartmentQuota("DevSecOps", 200000, 112400, 80, 0.15, 38.20)),
        new KeyValuePair<string, DepartmentQuota>("Legal & HR", new DepartmentQuota("Legal & HR", 50000, 9800, 80, 0.15, 3.15))
    });'''

new_quotas = '''    private static readonly System.Collections.Concurrent.ConcurrentDictionary<string, DepartmentQuota> DepartmentQuotas = new(new[]
    {
        new KeyValuePair<string, DepartmentQuota>("Mumbai FinTech & Payments", new DepartmentQuota("Mumbai FinTech & Payments", 150000, 42100, 80, 12.50, 1240.00)),
        new KeyValuePair<string, DepartmentQuota>("Bengaluru AI R&D Core", new DepartmentQuota("Bengaluru AI R&D Core", 200000, 112400, 80, 12.50, 3180.00)),
        new KeyValuePair<string, DepartmentQuota>("Hyderabad SecOps RedTeam", new DepartmentQuota("Hyderabad SecOps RedTeam", 100000, 28450, 80, 12.50, 820.00)),
        new KeyValuePair<string, DepartmentQuota>("AIIMS Delhi Health Informatics", new DepartmentQuota("AIIMS Delhi Health Informatics", 75000, 16200, 80, 12.50, 450.00)),
        new KeyValuePair<string, DepartmentQuota>("New Delhi Legal & Compliance", new DepartmentQuota("New Delhi Legal & Compliance", 50000, 9800, 80, 12.50, 280.00))
    });'''

if old_quotas in text:
    text = text.replace(old_quotas, new_quotas)
    print("Replaced DepartmentQuotas (LF)")
else:
    old_quotas_crlf = old_quotas.replace('\n', '\r\n')
    if old_quotas_crlf in text:
        text = text.replace(old_quotas_crlf, new_quotas.replace('\n', '\r\n'))
        print("Replaced DepartmentQuotas (CRLF)")
    else:
        print("Could not find old_quotas!")

# 2. Update Quota endpoint to INR
old_endpoint = '''        // 10. Enterprise FinOps: Departmental Token Quotas & Cost Governance
        app.MapGet("/api/governance/quotas", () =>
        {
            var list = DepartmentQuotas.Values.Select(q => new
            {
                q.Department,
                q.DailyTokenLimit,
                q.ConsumedTokens,
                RemainingTokens = Math.Max(0, q.DailyTokenLimit - q.ConsumedTokens),
                UtilizationPercentage = Math.Round(((double)q.ConsumedTokens / q.DailyTokenLimit) * 100, 1),
                q.SoftLimitPercentage,
                Status = q.ConsumedTokens >= q.DailyTokenLimit ? "THROTTLED" :
                         q.ConsumedTokens >= (q.DailyTokenLimit * q.SoftLimitPercentage / 100) ? "WARNING" : "HEALTHY",
                q.CostPerMillionTokensUsd,
                EstimatedCostUsd = Math.Round((q.ConsumedTokens / 1_000_000.0) * q.CostPerMillionTokensUsd, 4),
                q.FinOpsSavingsUsd
            }).ToList();

            var totalLimit = list.Sum(x => x.DailyTokenLimit);
            var totalConsumed = list.Sum(x => x.ConsumedTokens);
            var totalSavings = list.Sum(x => x.FinOpsSavingsUsd);

            return Results.Ok(new
            {
                departments = list,
                overallSummary = new
                {
                    totalDailyBudget = totalLimit,
                    totalConsumedTokens = totalConsumed,
                    overallUtilizationPct = Math.Round(((double)totalConsumed / totalLimit) * 100, 1),
                    totalFinOpsSavingsUsd = Math.Round(totalSavings, 2),
                    costOptimizationPolicy = "PII format-preserving tokenization saves 28% egress payload tokens",
                    activeSlaTier = "99.99% Enterprise Multi-Region Cloud"
                }
            });
        });'''

new_endpoint = '''        // 10. Enterprise FinOps: Departmental Token Quotas & Cost Governance (Indian Rupee ₹ INR)
        app.MapGet("/api/governance/quotas", () =>
        {
            var list = DepartmentQuotas.Values.Select(q => new
            {
                q.Department,
                q.DailyTokenLimit,
                q.ConsumedTokens,
                RemainingTokens = Math.Max(0, q.DailyTokenLimit - q.ConsumedTokens),
                UtilizationPercentage = Math.Round(((double)q.ConsumedTokens / q.DailyTokenLimit) * 100, 1),
                q.SoftLimitPercentage,
                Status = q.ConsumedTokens >= q.DailyTokenLimit ? "THROTTLED" :
                         q.ConsumedTokens >= (q.DailyTokenLimit * q.SoftLimitPercentage / 100) ? "WARNING" : "HEALTHY",
                q.CostPerMillionTokensInr,
                EstimatedCostInr = Math.Round((q.ConsumedTokens / 1_000_000.0) * q.CostPerMillionTokensInr, 2),
                q.FinOpsSavingsInr,
                Currency = "₹ INR"
            }).ToList();

            var totalLimit = list.Sum(x => x.DailyTokenLimit);
            var totalConsumed = list.Sum(x => x.ConsumedTokens);
            var totalSavings = list.Sum(x => x.FinOpsSavingsInr);

            return Results.Ok(new
            {
                currency = "₹ INR",
                departments = list,
                overallSummary = new
                {
                    totalDailyBudget = totalLimit,
                    totalConsumedTokens = totalConsumed,
                    overallUtilizationPct = Math.Round(((double)totalConsumed / totalLimit) * 100, 1),
                    totalFinOpsSavingsInr = Math.Round(totalSavings, 2),
                    costOptimizationPolicy = "DPDP Act 2023 & RBI Tokenization strips 28% egress payload tokens",
                    activeSlaTier = "99.99% ap-south-1 (Mumbai Primary) Multi-Zone Cloud"
                }
            });
        });'''

if old_endpoint in text:
    text = text.replace(old_endpoint, new_endpoint)
    print("Replaced Quotas endpoint (LF)")
else:
    old_endpoint_crlf = old_endpoint.replace('\n', '\r\n')
    if old_endpoint_crlf in text:
        text = text.replace(old_endpoint_crlf, new_endpoint.replace('\n', '\r\n'))
        print("Replaced Quotas endpoint (CRLF)")
    else:
        print("Could not find old_endpoint!")

# 3. Update Quota record definition
old_record = '''public record DepartmentQuota(
    string Department,
    int DailyTokenLimit,
    int ConsumedTokens,
    int SoftLimitPercentage,
    double CostPerMillionTokensUsd,
    double FinOpsSavingsUsd);'''

new_record = '''public record DepartmentQuota(
    string Department,
    int DailyTokenLimit,
    int ConsumedTokens,
    int SoftLimitPercentage,
    double CostPerMillionTokensInr,
    double FinOpsSavingsInr);'''

if old_record in text:
    text = text.replace(old_record, new_record)
    print("Replaced DepartmentQuota record (LF)")
else:
    old_record_crlf = old_record.replace('\n', '\r\n')
    if old_record_crlf in text:
        text = text.replace(old_record_crlf, new_record.replace('\n', '\r\n'))
        print("Replaced DepartmentQuota record (CRLF)")

# 4. Update cluster name in webhook simulation
text = text.replace('gateway-cluster-us-east-1', 'gateway-cluster-ap-south-1-mumbai')

# 5. Update compliance dossier frameworks with DPDP Act 2023
old_frameworks = '''                frameworks = new object[]
                {
                    new { standard = "EU AI Act (Regulation 2024/1689)", articles = new[] { "Art. 15 (Accuracy, Robustness, Cybersecurity)", "Art. 50 (Transparency for AI systems)" }, conformity = "FULL_CONFORMITY" },
                    new { standard = "ISO/IEC 42001:2023", scope = "Information technology — Artificial intelligence — Management system", conformity = "CERTIFIED" },
                    new { standard = "NIST AI RMF 1.0", functions = new[] { "GOVERN", "MAP", "MEASURE", "MANAGE" }, conformity = "TIER_4_ADAPTIVE" },
                    new { standard = "PCI-DSS v4.0.1", requirement = "Req 3.4 & 3.5: Primary Account Number Tokenization", conformity = "COMPLIANT" },
                    new { standard = "HIPAA Security Rule", requirement = "45 CFR § 164.312 Technical Safeguards", conformity = "COMPLIANT" }
                },'''

new_frameworks = '''                frameworks = new object[]
                {
                    new { standard = "DPDP Act 2023 (Digital Personal Data Protection Act, India)", articles = new[] { "Section 6 (Consent Manager Architecture)", "Section 8 (Data Fiduciary Safeguards)", "Section 9 (Child & Vulnerable Data Protection)" }, conformity = "FULL_CONFORMITY" },
                    new { standard = "UIDAI Aadhaar Act & Circulars 2016-2024", requirement = "Regulation 16A: Masked Aadhaar & Virtual Identity Tokenization", conformity = "CERTIFIED" },
                    new { standard = "RBI Master Direction on Payment Tokenization", requirement = "CoF Tokenization & Card-on-File Zero-Storage Mandate", conformity = "COMPLIANT" },
                    new { standard = "EU AI Act (Regulation 2024/1689)", articles = new[] { "Art. 15 (Accuracy, Robustness, Cybersecurity)", "Art. 50 (Transparency for AI systems)" }, conformity = "FULL_CONFORMITY" },
                    new { standard = "ISO/IEC 42001:2023", scope = "Information technology — Artificial intelligence — Management system", conformity = "CERTIFIED" }
                },'''

if old_frameworks in text:
    text = text.replace(old_frameworks, new_frameworks)
    print("Replaced frameworks (LF)")
else:
    old_frameworks_crlf = old_frameworks.replace('\n', '\r\n')
    if old_frameworks_crlf in text:
        text = text.replace(old_frameworks_crlf, new_frameworks.replace('\n', '\r\n'))
        print("Replaced frameworks (CRLF)")

with open('E:/enterprise-genai-dlp-gateway/backend/GenAiDlpGateway/Endpoints/GatewayEndpoints.cs', 'w', encoding='utf-8') as f:
    f.write(text)

print("Saved Indianized GatewayEndpoints.cs successfully!")

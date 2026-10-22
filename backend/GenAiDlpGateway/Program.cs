using System.Text.Json.Serialization;
using GenAiDlpGateway.Data;
using GenAiDlpGateway.Endpoints;
using GenAiDlpGateway.Proxy;
using GenAiDlpGateway.Services;
using Microsoft.EntityFrameworkCore;
using Yarp.ReverseProxy.Configuration;

var builder = WebApplication.CreateBuilder(args);

builder.WebHost.UseUrls("http://localhost:5180");

builder.Services.ConfigureHttpJsonOptions(options =>
{
    options.SerializerOptions.Converters.Add(new JsonStringEnumConverter());
});

builder.Services.AddCors(options =>
{
    options.AddDefaultPolicy(policy =>
    {
        policy.AllowAnyOrigin()
              .AllowAnyHeader()
              .AllowAnyMethod()
              .WithExposedHeaders(
                  "X-DLP-Request-Id",
                  "X-DLP-Action",
                  "X-DLP-Entities-Detected",
                  "X-DLP-Risk-Score",
                  "X-DLP-Tokens-Restored",
                  "X-DLP-Latency-Ms",
                  "X-DLP-Privacy-Mode",
                  "X-DLP-Proof-Hash",
                  "X-DLP-Threat-Score",
                  "X-DLP-Threat-Category");
    });
});

// 1. Configure Audit Database (PostgreSQL if connection string provided, otherwise SQLite local DB)
var pgConn = builder.Configuration.GetConnectionString("PostgreSQL");
var sqliteConn = builder.Configuration.GetConnectionString("Sqlite") ?? "Data Source=dlp_audit_gateway.db";

builder.Services.AddDbContext<DlpAuditDbContext>(options =>
{
    if (!string.IsNullOrWhiteSpace(pgConn))
    {
        options.UseNpgsql(pgConn);
    }
    else
    {
        options.UseSqlite(sqliteConn);
    }
});

// 2. Configure Ephemeral Token Caching (Redis if connection string provided, otherwise Distributed Memory Cache)
var redisConn = builder.Configuration.GetConnectionString("Redis");
if (!string.IsNullOrWhiteSpace(redisConn))
{
    builder.Services.AddStackExchangeRedisCache(options =>
    {
        options.Configuration = redisConn;
        options.InstanceName = "GenAiDlp:";
    });
}
else
{
    builder.Services.AddDistributedMemoryCache();
}

// 3. Register DLP Engine, Token Vault, and HTTP Client for Presidio integration
builder.Services.AddHttpClient();
builder.Services.AddSingleton<ITokenVaultService, TokenVaultService>();
builder.Services.AddScoped<IDlpEngineService, DlpEngineService>();

// 4. Configure YARP Reverse Proxy with Dynamic Config Provider
builder.Services.AddSingleton<DlpProxyConfigProvider>();
builder.Services.AddSingleton<IProxyConfigProvider>(sp => sp.GetRequiredService<DlpProxyConfigProvider>());
builder.Services.AddReverseProxy();

var app = builder.Build();

app.UseCors();

// Seed default enterprise DLP policies, sample audit logs, and ephemeral tokens
await DatabaseSeeder.SeedAsync(app.Services);

// Map Admin Dashboard APIs & Built-in Mock LLM Upstream
app.MapGatewayEndpoints();

// Register Real-Time YARP DLP Inspection & De-tokenization Middleware before YARP Reverse Proxy
app.UseMiddleware<YarpDlpProxyMiddleware>();

app.MapReverseProxy();

app.Run();

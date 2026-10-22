using Microsoft.Extensions.Primitives;
using Yarp.ReverseProxy.Configuration;

namespace GenAiDlpGateway.Proxy;

public class DlpProxyConfigProvider : IProxyConfigProvider
{
    private volatile CustomMemoryConfig _config;

    public DlpProxyConfigProvider(IConfiguration configuration)
    {
        var upstreamUrl = configuration["DlpGateway:UpstreamLlmBaseUrl"];
        if (string.IsNullOrWhiteSpace(upstreamUrl))
        {
            // Default to built-in local Mock LLM endpoint served on the same Kestrel host
            var selfBase = configuration["DlpGateway:SelfBaseUrl"] ?? "http://localhost:5180";
            upstreamUrl = $"{selfBase.TrimEnd('/')}/internal/mock-llm/";
        }

        _config = BuildConfig(upstreamUrl);
    }

    public IProxyConfig GetConfig() => _config;

    public void UpdateUpstreamUrl(string newUpstreamUrl)
    {
        var oldConfig = _config;
        _config = BuildConfig(newUpstreamUrl);
        oldConfig.SignalChange();
    }

    private static CustomMemoryConfig BuildConfig(string destinationAddress)
    {
        var routes = new[]
        {
            new RouteConfig
            {
                RouteId = "genai-v1-proxy-route",
                ClusterId = "llm-upstream-cluster",
                Match = new RouteMatch
                {
                    Path = "/v1/{**catch-all}"
                }
            }
        };

        var clusters = new[]
        {
            new ClusterConfig
            {
                ClusterId = "llm-upstream-cluster",
                Destinations = new Dictionary<string, DestinationConfig>(StringComparer.OrdinalIgnoreCase)
                {
                    ["primary-llm-node"] = new DestinationConfig
                    {
                        Address = destinationAddress
                    }
                }
            }
        };

        return new CustomMemoryConfig(routes, clusters);
    }

    private class CustomMemoryConfig : IProxyConfig
    {
        private readonly CancellationTokenSource _cts = new();

        public CustomMemoryConfig(IReadOnlyList<RouteConfig> routes, IReadOnlyList<ClusterConfig> clusters)
        {
            Routes = routes;
            Clusters = clusters;
            ChangeToken = new CancellationChangeToken(_cts.Token);
        }

        public IReadOnlyList<RouteConfig> Routes { get; }
        public IReadOnlyList<ClusterConfig> Clusters { get; }
        public IChangeToken ChangeToken { get; }

        public void SignalChange() => _cts.Cancel();
    }
}

using System.Net;
using System.Text.Json;
using Microsoft.AspNetCore.Mvc.Testing;

namespace TradeApi.Tests;

public class ApiEndpointTests : IClassFixture<WebApplicationFactory<Program>>
{
    private readonly HttpClient _client;

    public ApiEndpointTests(WebApplicationFactory<Program> factory)
    {
        _client = factory.CreateClient();
    }

    [Fact]
    public async Task Health_ReturnsHealthyStatus()
    {
        var response = await _client.GetAsync("/health");

        Assert.Equal(HttpStatusCode.OK, response.StatusCode);

        var content = await response.Content.ReadAsStringAsync();
        using var json = JsonDocument.Parse(content);

        var status = json.RootElement.GetProperty("status").GetString();

        Assert.Equal("Healthy", status);
    }

    [Fact]
    public async Task Version_ReturnsAppNameAndVersion()
    {
        var response = await _client.GetAsync("/version");

        Assert.Equal(HttpStatusCode.OK, response.StatusCode);

        var content = await response.Content.ReadAsStringAsync();
        using var json = JsonDocument.Parse(content);

        var app = json.RootElement.GetProperty("app").GetString();
        var version = json.RootElement.GetProperty("version").GetString();

        Assert.Equal("cloud-trade-api", app);
        Assert.Equal("0.1.0", version);
    }

    [Fact]
    public async Task Trades_ReturnsMockTradeData()
    {
        var response = await _client.GetAsync("/trades");

        Assert.Equal(HttpStatusCode.OK, response.StatusCode);

        var content = await response.Content.ReadAsStringAsync();
        using var json = JsonDocument.Parse(content);

        Assert.True(json.RootElement.GetArrayLength() > 0);

        var firstTrade = json.RootElement[0];

        Assert.True(firstTrade.TryGetProperty("id", out _));
        Assert.True(firstTrade.TryGetProperty("symbol", out _));
        Assert.True(firstTrade.TryGetProperty("side", out _));
        Assert.True(firstTrade.TryGetProperty("quantity", out _));
        Assert.True(firstTrade.TryGetProperty("price", out _));
    }
}
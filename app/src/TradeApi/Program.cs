var builder = WebApplication.CreateBuilder(args);

var app = builder.Build();

var appName = "cloud-trade-api";
var appVersion = Environment.GetEnvironmentVariable("APP_VERSION") ?? "0.1.0";
var environment = Environment.GetEnvironmentVariable("APP_ENVIRONMENT") ?? app.Environment.EnvironmentName;
var logLevel = Environment.GetEnvironmentVariable("APP_LOG_LEVEL") ?? "information";

app.MapGet("/", () =>
{
    return Results.Ok(new
    {
        message = "Cloud Trade API is running",
        endpoints = new[]
        {
            "/health",
            "/version",
            "/config",
            "/trades"
        }
    });
});

app.MapGet("/health", () =>
{
    return Results.Ok(new
    {
        status = "Healthy",
        timestampUtc = DateTime.UtcNow
    });
});

app.MapGet("/version", () =>
{
    return Results.Ok(new
    {
        app = appName,
        version = appVersion,
        environment = environment
    });
});

app.MapGet("/config", () =>
{
    return Results.Ok(new
    {
        environment = environment,
        app = new
        {
            name = appName,
            version = appVersion,
            logLevel = logLevel
        },
        tradeSettings = new
        {
            maxTradeCount = 10,
            enableMockData = true
        }
    });
});

app.MapGet("/trades", () =>
{
    var trades = new[]
    {
        new Trade(1, "AAPL", "BUY", 10, 185.50m),
        new Trade(2, "MSFT", "SELL", 5, 420.25m),
        new Trade(3, "AMZN", "BUY", 3, 178.90m)
    };

    return Results.Ok(trades);
});

app.Run();

record Trade(int Id, string Symbol, string Side, int Quantity, decimal Price);
public partial class Program { }
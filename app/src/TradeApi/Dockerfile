FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

COPY app/src/TradeApi/TradeApi.csproj app/src/TradeApi/
RUN dotnet restore app/src/TradeApi/TradeApi.csproj

COPY app/src/TradeApi/ app/src/TradeApi/
RUN dotnet publish app/src/TradeApi/TradeApi.csproj \
    --configuration Release \
    --output /app/publish \
    --no-restore

FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS runtime
WORKDIR /app

ENV ASPNETCORE_URLS=http://+:8080

EXPOSE 8080

COPY --from=build /app/publish .

ENTRYPOINT ["dotnet", "TradeApi.dll"]
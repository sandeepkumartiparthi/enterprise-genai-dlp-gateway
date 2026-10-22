FROM mcr.microsoft.com/dotnet/sdk:10.0-preview AS build
WORKDIR /src
COPY ["GenAiDlpGateway.csproj", "."]
RUN dotnet restore "GenAiDlpGateway.csproj"
COPY . .
RUN dotnet publish "GenAiDlpGateway.csproj" -c Release -o /app/publish /p:UseAppHost=false

FROM mcr.microsoft.com/dotnet/aspnet:10.0-preview AS final
WORKDIR /app
COPY --from=build /app/publish .
ENV ASPNETCORE_URLS=http://+:5180
EXPOSE 5180
ENTRYPOINT ["dotnet", "GenAiDlpGateway.dll"]

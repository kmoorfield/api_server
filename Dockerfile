FROM mcr.microsoft.com/dotnet/sdk:5.0 AS build-env
WORKDIR /app
COPY C#_api_server/*.csproj ./Application/
WORKDIR /app/Application
RUN dotnet restore
COPY C#_api_server /app/Application
RUN dotnet publish -c Release -o output
#Runtime Image
FROM mcr.microsoft.com/dotnet/aspnet:5.0
WORKDIR /app/Application
COPY --from=build-env /app/Application/output .
ENTRYPOINT ["dotnet", "C#_api_server.dll"]

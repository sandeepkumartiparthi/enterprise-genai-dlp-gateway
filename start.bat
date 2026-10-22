@echo off
setlocal
cd /d "%~dp0"
title AegisDLP - Starting Project (Fast Launch)

echo ===============================================================================
echo                   STARTING AEGIS-DLP GATEWAY (LIGHTNING SPEED)
echo ===============================================================================
echo.

:: 1. Clean up any existing processes on ports 5180 and 5173
echo [1/4] Freeing network ports 5180 and 5173...
taskkill /f /im GenAiDlpGateway.exe >nul 2>&1
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":5180" ^| findstr "LISTENING"') do (
    taskkill /f /pid %%a >nul 2>&1
)
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":5173" ^| findstr "LISTENING"') do (
    taskkill /f /pid %%a >nul 2>&1
)

:: 2. Pre-build check - skip build if binaries already exist for instant launch
if not exist "%~dp0backend\GenAiDlpGateway\bin\Debug\net10.0\GenAiDlpGateway.dll" (
    echo [2/4] First-time compilation of backend binaries...
    cd /d "%~dp0backend\GenAiDlpGateway"
    dotnet build --nologo -v q
    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Backend build failed.
        dotnet build
        pause
        exit /b 1
    )
) else (
    echo [2/4] Backend binary cached and ready.
)

:: 3. Start Backend (.NET 10 YARP DLP Gateway on port 5180)
echo [3/4] Launching Backend Gateway on http://localhost:5180 ...
start "AegisDLP Backend Gateway (Port 5180)" cmd /k "cd /d "%~dp0backend\GenAiDlpGateway" && title AegisDLP Backend (5180) && dotnet run --no-build --urls "http://localhost:5180""

:: 4. Start Frontend (React 19 Light-Theme Portal on port 5173)
echo [4/4] Launching Frontend Portal on http://localhost:5173 ...
start "AegisDLP Frontend Portal (Port 5173)" cmd /k "cd /d "%~dp0frontend" && title AegisDLP Frontend (5173) && npm.cmd run dev"

:: 5. Instant browser launch
echo.
echo Launching http://localhost:5173 in browser...
timeout /t 1 /nobreak >nul
start http://localhost:5173

echo.
echo ===============================================================================
echo  Project successfully launched at lightning speed!
echo   * Frontend Web UI : http://localhost:5173
echo   * Backend Gateway : http://localhost:5180
echo   * Swagger OpenAPI : http://localhost:5180/swagger
echo ===============================================================================
echo.
exit

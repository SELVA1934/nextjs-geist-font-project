@echo off
echo Discord Server Cloner
echo -------------------
echo 1. GUI Mode
echo 2. Command Line Mode
echo.
set /p mode="Select mode (1 or 2): "

if "%mode%"=="1" (
    python discord_cloner_gui.py
) else if "%mode%"=="2" (
    python discord_cloner.py
) else (
    echo Invalid selection!
)

echo.
pause

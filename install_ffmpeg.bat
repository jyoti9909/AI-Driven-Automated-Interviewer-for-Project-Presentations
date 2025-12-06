@echo off
echo ========================================
echo Installing ffmpeg for Windows...
echo ========================================
echo.

REM Check if chocolatey is installed
where choco >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo Chocolatey found. Installing ffmpeg...
    choco install ffmpeg -y
    echo.
    echo ffmpeg installed successfully!
    echo Please restart your terminal or PowerShell window.
) else (
    echo Chocolatey not found.
    echo.
    echo Please install ffmpeg manually:
    echo 1. Download from: https://www.gyan.dev/ffmpeg/builds/
    echo 2. Extract the zip file
    echo 3. Add the 'bin' folder to your PATH environment variable
    echo.
    echo OR install Chocolatey first, then run this script again:
    echo    Visit: https://chocolatey.org/install
)

echo.
pause


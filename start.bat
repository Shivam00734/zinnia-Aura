@echo off
echo ========================================
echo Zinnia Live Dashboard
echo ========================================
echo.

REM Kill any existing Python and Chrome processes
taskkill /F /IM python.exe /T > nul 2>&1
taskkill /F /IM chrome.exe /T > nul 2>&1

REM Clean up only temporary allure-results (keep historical reports in allure-report/)
if exist "allure-results" (
    echo Cleaning up temporary allure-results...
    rmdir /S /Q "allure-results"
)

REM Note: allure-report/ directory contains all historical reports

REM Check if Python is installed
python --version > nul 2>&1
if errorlevel 1 (
    echo Python is not installed on your system!
    echo.
    echo Please install Python 3.8 or higher before running this application.
    echo You can download Python from: https://www.python.org/downloads/
    echo.
    echo After installing Python, run this file again.
    echo.
    pause
    exit /b 1
)

REM Install required packages if not already installed
pip install -r requirements.txt

echo.
echo ========================================
echo Starting Flask Server on Port 5050
echo ========================================
echo.
echo The dashboard will be available at: http://localhost:5050
echo.
echo Available features:
echo - API Testing Suite
echo - API Performance Testing
echo - UI Testing
echo - Database Testing
echo.
echo Press Ctrl+C to stop the server
echo.

REM Create a temporary VBScript to launch Chrome
echo Set objShell = CreateObject("WScript.Shell") > "%~dp0launch_browser.vbs"
echo WScript.Sleep 2000 >> "%~dp0launch_browser.vbs"
echo objShell.Run "chrome.exe --new-window --incognito --no-cache http://localhost:5050", 1, False >> "%~dp0launch_browser.vbs"

REM Start Chrome and Flask server
start /B wscript "%~dp0launch_browser.vbs"
python "%~dp0dashboard.py"

REM Clean up
del "%~dp0launch_browser.vbs"

pause
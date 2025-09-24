@echo off
setlocal EnableDelayedExpansion

REM System Diagnostic Script for Zinnia Live Automation Framework
REM This script helps identify issues that prevent successful setup

set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

set "DIAG_LOG=%SCRIPT_DIR%diagnostic_report.txt"
echo ========================================> "%DIAG_LOG%"
echo ZINNIA LIVE SETUP DIAGNOSTIC REPORT>> "%DIAG_LOG%"
echo Generated: %date% %time%>> "%DIAG_LOG%"
echo ========================================>> "%DIAG_LOG%"
echo.>> "%DIAG_LOG%"

echo ========================================
echo 🔍 ZINNIA LIVE SETUP DIAGNOSTICS
echo ========================================
echo.
echo This script will diagnose potential issues with your system
echo and generate a report to help resolve setup problems.
echo.
echo Diagnostic report will be saved to: diagnostic_report.txt
echo.

REM System Information
echo [1/12] Gathering system information...
echo === SYSTEM INFORMATION ===>> "%DIAG_LOG%"
echo Windows Version: >> "%DIAG_LOG%"
ver >> "%DIAG_LOG%" 2>&1
echo.>> "%DIAG_LOG%"
echo Architecture: >> "%DIAG_LOG%"
wmic OS get OSArchitecture /value >> "%DIAG_LOG%" 2>&1
echo.>> "%DIAG_LOG%"
echo Computer Name: %COMPUTERNAME%>> "%DIAG_LOG%"
echo Username: %USERNAME%>> "%DIAG_LOG%"
echo.>> "%DIAG_LOG%"

REM Administrator Check
echo [2/12] Checking administrator privileges...
echo === ADMINISTRATOR PRIVILEGES ===>> "%DIAG_LOG%"
net session >nul 2>&1
if errorlevel 1 (
    echo ❌ NOT running as Administrator>> "%DIAG_LOG%"
    echo ❌ NOT running as Administrator
    echo   This may cause permission issues during setup.
) else (
    echo ✅ Running as Administrator>> "%DIAG_LOG%"
    echo ✅ Running as Administrator
)
echo.>> "%DIAG_LOG%"

REM Python Detection
echo [3/12] Checking Python installation...
echo === PYTHON INSTALLATION ===>> "%DIAG_LOG%"
echo Checking python command...>> "%DIAG_LOG%"
python --version >> "%DIAG_LOG%" 2>&1
if errorlevel 1 (
    echo ❌ Python not found with 'python' command>> "%DIAG_LOG%"
    echo ❌ Python not found with 'python' command
    
    echo Checking python3 command...>> "%DIAG_LOG%"
    python3 --version >> "%DIAG_LOG%" 2>&1
    if errorlevel 1 (
        echo ❌ Python not found with 'python3' command>> "%DIAG_LOG%"
        echo ❌ Python not found with 'python3' command
    ) else (
        echo ✅ Python found with 'python3' command>> "%DIAG_LOG%"
        echo ✅ Python found with 'python3' command
        set PYTHON_CMD=python3
    )
    
    echo Checking py command...>> "%DIAG_LOG%"
    py --version >> "%DIAG_LOG%" 2>&1
    if errorlevel 1 (
        echo ❌ Python not found with 'py' command>> "%DIAG_LOG%"
        echo ❌ Python not found with 'py' command
    ) else (
        echo ✅ Python found with 'py' command>> "%DIAG_LOG%"
        echo ✅ Python found with 'py' command
        set PYTHON_CMD=py
    )
) else (
    echo ✅ Python found with 'python' command>> "%DIAG_LOG%"
    echo ✅ Python found with 'python' command
    set PYTHON_CMD=python
)

REM Python Path Detection
echo [4/12] Checking Python PATH...
echo === PYTHON PATH ===>> "%DIAG_LOG%"
where python >> "%DIAG_LOG%" 2>&1
if errorlevel 1 (
    echo ❌ Python not in system PATH>> "%DIAG_LOG%"
    echo ❌ Python not in system PATH
) else (
    echo ✅ Python found in PATH>> "%DIAG_LOG%"
    echo ✅ Python found in PATH
)

where python3 >> "%DIAG_LOG%" 2>&1
where py >> "%DIAG_LOG%" 2>&1
echo.>> "%DIAG_LOG%"

REM Pip Detection
echo [5/12] Checking pip installation...
echo === PIP INSTALLATION ===>> "%DIAG_LOG%"
if defined PYTHON_CMD (
    %PYTHON_CMD% -m pip --version >> "%DIAG_LOG%" 2>&1
    if errorlevel 1 (
        echo ❌ pip not available with %PYTHON_CMD%>> "%DIAG_LOG%"
        echo ❌ pip not available with %PYTHON_CMD%
    ) else (
        echo ✅ pip available with %PYTHON_CMD%>> "%DIAG_LOG%"
        echo ✅ pip available with %PYTHON_CMD%
    )
) else (
    echo ❌ No Python command available to test pip>> "%DIAG_LOG%"
    echo ❌ No Python command available to test pip
)

pip --version >> "%DIAG_LOG%" 2>&1
if errorlevel 1 (
    echo ❌ pip command not directly available>> "%DIAG_LOG%"
    echo ❌ pip command not directly available
) else (
    echo ✅ pip command directly available>> "%DIAG_LOG%"
    echo ✅ pip command directly available
)
echo.>> "%DIAG_LOG%"

REM Internet Connectivity
echo [6/12] Checking internet connectivity...
echo === INTERNET CONNECTIVITY ===>> "%DIAG_LOG%"
ping -n 1 google.com > nul 2>&1
if errorlevel 1 (
    echo ❌ No internet connectivity to google.com>> "%DIAG_LOG%"
    echo ❌ No internet connectivity to google.com
) else (
    echo ✅ Internet connectivity confirmed>> "%DIAG_LOG%"
    echo ✅ Internet connectivity confirmed
)

ping -n 1 pypi.org > nul 2>&1
if errorlevel 1 (
    echo ❌ Cannot reach pypi.org (Python package repository)>> "%DIAG_LOG%"
    echo ❌ Cannot reach pypi.org (Python package repository)
) else (
    echo ✅ Can reach pypi.org>> "%DIAG_LOG%"
    echo ✅ Can reach pypi.org
)
echo.>> "%DIAG_LOG%"

REM Proxy Detection
echo [7/12] Checking proxy settings...
echo === PROXY SETTINGS ===>> "%DIAG_LOG%"
if defined HTTP_PROXY (
    echo HTTP_PROXY set to: %HTTP_PROXY%>> "%DIAG_LOG%"
    echo ⚠️ HTTP_PROXY environment variable detected
) else (
    echo HTTP_PROXY not set>> "%DIAG_LOG%"
)

if defined HTTPS_PROXY (
    echo HTTPS_PROXY set to: %HTTPS_PROXY%>> "%DIAG_LOG%"
    echo ⚠️ HTTPS_PROXY environment variable detected
) else (
    echo HTTPS_PROXY not set>> "%DIAG_LOG%"
)

REM Check Windows proxy settings
reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable >> "%DIAG_LOG%" 2>&1
echo.>> "%DIAG_LOG%"

REM Chrome Detection
echo [8/12] Checking Chrome installation...
echo === CHROME BROWSER ===>> "%DIAG_LOG%"
reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version >> "%DIAG_LOG%" 2>&1
if errorlevel 1 (
    reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Google\Chrome\BLBeacon" /v version >> "%DIAG_LOG%" 2>&1
    if errorlevel 1 (
        echo ❌ Chrome browser not detected>> "%DIAG_LOG%"
        echo ❌ Chrome browser not detected
    ) else (
        echo ✅ Chrome browser detected (system-wide)>> "%DIAG_LOG%"
        echo ✅ Chrome browser detected (system-wide)
    )
) else (
    echo ✅ Chrome browser detected (user)>> "%DIAG_LOG%"
    echo ✅ Chrome browser detected (user)
)
echo.>> "%DIAG_LOG%"

REM Java Detection
echo [9/12] Checking Java installation...
echo === JAVA INSTALLATION ===>> "%DIAG_LOG%"
java -version >> "%DIAG_LOG%" 2>&1
if errorlevel 1 (
    echo ❌ Java not found (required for Allure reports)>> "%DIAG_LOG%"
    echo ❌ Java not found (required for Allure reports)
) else (
    echo ✅ Java detected>> "%DIAG_LOG%"
    echo ✅ Java detected
)
echo.>> "%DIAG_LOG%"

REM Antivirus Detection
echo [10/12] Checking for potential antivirus interference...
echo === ANTIVIRUS DETECTION ===>> "%DIAG_LOG%"
wmic /namespace:\\root\securitycenter2 path antivirusproduct get displayname >> "%DIAG_LOG%" 2>&1
echo Note: Some antivirus software may interfere with installations>> "%DIAG_LOG%"
echo.>> "%DIAG_LOG%"

REM File Permissions
echo [11/12] Checking file permissions...
echo === FILE PERMISSIONS ===>> "%DIAG_LOG%"
echo Current directory: %SCRIPT_DIR%>> "%DIAG_LOG%"
echo Creating test file to check write permissions...>> "%DIAG_LOG%"
echo test > "%SCRIPT_DIR%test_write_permissions.tmp" 2>> "%DIAG_LOG%"
if exist "%SCRIPT_DIR%test_write_permissions.tmp" (
    echo ✅ Write permissions confirmed>> "%DIAG_LOG%"
    echo ✅ Write permissions confirmed
    del "%SCRIPT_DIR%test_write_permissions.tmp" 2>> "%DIAG_LOG%"
) else (
    echo ❌ No write permissions in current directory>> "%DIAG_LOG%"
    echo ❌ No write permissions in current directory
)
echo.>> "%DIAG_LOG%"

REM Previous Setup Logs
echo [12/12] Checking previous setup attempts...
echo === PREVIOUS SETUP LOGS ===>> "%DIAG_LOG%"
if exist "%SCRIPT_DIR%setup_log.txt" (
    echo Previous setup log found>> "%DIAG_LOG%"
    echo ✅ Previous setup log found
    echo.>> "%DIAG_LOG%"
    echo === LAST SETUP LOG CONTENT ===>> "%DIAG_LOG%"
    type "%SCRIPT_DIR%setup_log.txt" >> "%DIAG_LOG%" 2>&1
) else (
    echo No previous setup log found>> "%DIAG_LOG%"
    echo ℹ️ No previous setup log found
)
echo.>> "%DIAG_LOG%"

REM Environment Variables
echo === ENVIRONMENT VARIABLES ===>> "%DIAG_LOG%"
echo PATH variable:>> "%DIAG_LOG%"
echo %PATH%>> "%DIAG_LOG%"
echo.>> "%DIAG_LOG%"

echo ========================================>> "%DIAG_LOG%"
echo END OF DIAGNOSTIC REPORT>> "%DIAG_LOG%"
echo ========================================>> "%DIAG_LOG%"

echo.
echo ========================================
echo 📋 DIAGNOSTIC COMPLETE
echo ========================================
echo.
echo Diagnostic report saved to: diagnostic_report.txt
echo.
echo 📧 SHARING INSTRUCTIONS:
echo   1. Send the diagnostic_report.txt file to the project maintainer
echo   2. Include any error messages you encountered
echo   3. Mention what step failed during setup
echo.
echo 🔧 QUICK FIXES TO TRY:
echo.
if not defined PYTHON_CMD (
    echo   1. INSTALL PYTHON:
    echo      - Download from https://www.python.org/downloads/
    echo      - IMPORTANT: Check "Add Python to PATH" during installation
    echo      - Restart command prompt after installation
    echo.
)

echo   2. RUN AS ADMINISTRATOR:
echo      - Right-click on setup_project.bat
echo      - Select "Run as administrator"
echo.

echo   3. CHECK INTERNET CONNECTION:
echo      - Ensure you can browse the web
echo      - If behind corporate firewall, contact IT support
echo.

echo   4. DISABLE ANTIVIRUS TEMPORARILY:
echo      - Some antivirus software blocks Python installations
echo      - Temporarily disable real-time protection during setup
echo.

echo Press any key to continue...
pause > nul

endlocal

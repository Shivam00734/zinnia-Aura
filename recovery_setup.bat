@echo off
setlocal EnableDelayedExpansion

REM Recovery Setup Script for Zinnia Live Automation Framework
REM Use this when the main setup script fails

set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

set "RECOVERY_LOG=%SCRIPT_DIR%recovery_log.txt"
echo ========================================> "%RECOVERY_LOG%"
echo ZINNIA LIVE RECOVERY SETUP LOG>> "%RECOVERY_LOG%"
echo Generated: %date% %time%>> "%RECOVERY_LOG%"
echo ========================================>> "%RECOVERY_LOG%"
echo.>> "%RECOVERY_LOG%"

echo ========================================
echo 🚨 ZINNIA LIVE RECOVERY SETUP
echo ========================================
echo.
echo This script attempts to recover from failed setup attempts
echo and install dependencies using alternative methods.
echo.
echo Recovery log will be saved to: recovery_log.txt
echo.

REM Check if main setup was attempted
if not exist "%SCRIPT_DIR%setup_log.txt" (
    echo No previous setup attempt found.
    echo Please run setup_project.bat first.
    echo.
    pause
    exit /b 1
)

echo [1/8] Cleaning previous installation attempts...
echo Cleaning previous attempts >> "%RECOVERY_LOG%"

REM Clean pip cache
if exist "%USERPROFILE%\.cache\pip" (
    echo Clearing pip cache...
    rmdir /s /q "%USERPROFILE%\.cache\pip" 2>> "%RECOVERY_LOG%"
)

if exist "%APPDATA%\pip" (
    echo Clearing pip config...
    rmdir /s /q "%APPDATA%\pip\cache" 2>> "%RECOVERY_LOG%"
)

echo [2/8] Detecting Python installation...
echo Python detection for recovery >> "%RECOVERY_LOG%"

set PYTHON_CMD=
set PIP_CMD=

REM Try multiple Python detection methods
for %%p in (python python3 py) do (
    %%p --version > nul 2>&1
    if not errorlevel 1 (
        set PYTHON_CMD=%%p
        echo Found Python with: %%p >> "%RECOVERY_LOG%"
        goto :python_detected
    )
)

echo ERROR: No Python installation found!
echo Please install Python first from: https://www.python.org/downloads/
echo.
pause
exit /b 1

:python_detected
echo ✅ Using Python command: %PYTHON_CMD%

REM Detect pip
for %%m in ("%PYTHON_CMD% -m pip" "pip" "pip3") do (
    %%~m --version > nul 2>&1
    if not errorlevel 1 (
        set PIP_CMD=%%~m
        echo Found pip with: %%~m >> "%RECOVERY_LOG%"
        goto :pip_detected
    )
)

echo ERROR: No pip installation found!
echo Trying to install pip...
%PYTHON_CMD% -m ensurepip --upgrade >> "%RECOVERY_LOG%" 2>&1
if errorlevel 1 (
    echo Failed to install pip automatically.
    pause
    exit /b 1
)
set PIP_CMD=%PYTHON_CMD% -m pip

:pip_detected
echo ✅ Using pip command: %PIP_CMD%

echo [3/8] Upgrading pip with alternative methods...
echo Upgrading pip for recovery >> "%RECOVERY_LOG%"

REM Try multiple pip upgrade methods
%PYTHON_CMD% -m pip install --upgrade pip --no-cache-dir --force-reinstall >> "%RECOVERY_LOG%" 2>&1
if errorlevel 1 (
    echo Standard pip upgrade failed, trying alternative...
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py >> "%RECOVERY_LOG%" 2>&1
    if exist get-pip.py (
        %PYTHON_CMD% get-pip.py --force-reinstall >> "%RECOVERY_LOG%" 2>&1
        del get-pip.py
    )
)

echo [4/8] Installing core dependencies individually...
echo Individual package installation >> "%RECOVERY_LOG%"

set CORE_PACKAGES=robotframework selenium requests openpyxl pandas flask
set FAILED_PACKAGES=

for %%p in (%CORE_PACKAGES%) do (
    echo Installing %%p...
    %PIP_CMD% install %%p --upgrade --no-cache-dir --user >> "%RECOVERY_LOG%" 2>&1
    if errorlevel 1 (
        echo Failed to install %%p >> "%RECOVERY_LOG%"
        set FAILED_PACKAGES=!FAILED_PACKAGES! %%p
    ) else (
        echo ✅ %%p installed successfully
        echo %%p installation successful >> "%RECOVERY_LOG%"
    )
)

echo [5/8] Installing Robot Framework extensions...
echo Robot Framework extensions installation >> "%RECOVERY_LOG%"

set RF_PACKAGES=robotframework-seleniumlibrary robotframework-requests robotframework-datadriver
for %%p in (%RF_PACKAGES%) do (
    echo Installing %%p...
    %PIP_CMD% install %%p --upgrade --no-cache-dir --user >> "%RECOVERY_LOG%" 2>&1
    if errorlevel 1 (
        echo Failed to install %%p >> "%RECOVERY_LOG%"
        set FAILED_PACKAGES=!FAILED_PACKAGES! %%p
    ) else (
        echo ✅ %%p installed successfully
        echo %%p installation successful >> "%RECOVERY_LOG%"
    )
)

echo [6/8] Installing Allure reporting...
echo Allure installation >> "%RECOVERY_LOG%"

%PIP_CMD% install allure-python-commons allure-robotframework --upgrade --no-cache-dir --user >> "%RECOVERY_LOG%" 2>&1
if errorlevel 1 (
    echo Failed to install Allure packages >> "%RECOVERY_LOG%"
    set FAILED_PACKAGES=!FAILED_PACKAGES! allure
) else (
    echo ✅ Allure packages installed successfully
)

echo [7/8] Installing ChromeDriver...
echo ChromeDriver installation >> "%RECOVERY_LOG%"

%PIP_CMD% install chromedriver-autoinstaller --upgrade --no-cache-dir --user >> "%RECOVERY_LOG%" 2>&1
if not errorlevel 1 (
    %PYTHON_CMD% -c "import chromedriver_autoinstaller; chromedriver_autoinstaller.install()" >> "%RECOVERY_LOG%" 2>&1
    if not errorlevel 1 (
        echo ✅ ChromeDriver installed successfully
    ) else (
        echo ⚠️ ChromeDriver auto-install failed
    )
)

echo [8/8] Running verification tests...
echo Recovery verification >> "%RECOVERY_LOG%"

echo Testing core modules...
%PYTHON_CMD% -c "import robot, selenium, requests; print('Core modules OK')" >> "%RECOVERY_LOG%" 2>&1
if not errorlevel 1 (
    echo ✅ Core modules working
) else (
    echo ❌ Core modules still failing
)

echo.
echo ========================================
echo 🔧 RECOVERY SETUP RESULTS
echo ========================================
echo.

if defined FAILED_PACKAGES (
    echo ⚠️ Some packages failed to install:
    echo %FAILED_PACKAGES%
    echo.
    echo These packages can be installed manually later.
) else (
    echo ✅ All packages installed successfully!
)

echo.
echo 📋 NEXT STEPS:
echo.
echo 1. Test the installation:
echo    %PYTHON_CMD% -c "import robot; print('Robot Framework OK')"
echo.
echo 2. Run a simple test:
echo    robot --version
echo.
echo 3. If issues persist:
echo    - Run diagnose_system.bat for detailed analysis
echo    - Contact IT support if in corporate environment
echo    - Check recovery_log.txt for error details
echo.

echo Recovery setup completed. Check recovery_log.txt for details.
echo.
pause

endlocal

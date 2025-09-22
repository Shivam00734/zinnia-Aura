@echo off
setlocal

REM Get the directory where this batch file is located
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

echo ========================================
echo Automation Framework Project Setup
echo ========================================
echo.

REM Check if Python is installed
python --version > nul 2>&1
if errorlevel 1 (
    echo Python is not installed on your system!
    echo.
    echo Please install Python 3.8 or higher before running this setup.
    echo You can download Python from: https://www.python.org/downloads/
    echo.
    echo After installing Python, run this setup file again.
    echo.
    pause
    exit /b 1
)

REM Check for required configuration files
echo Checking required configuration files...
echo.

set CONFIG_MISSING=0

if not exist "%SCRIPT_DIR%requirements.txt" (
    echo ERROR: Missing configuration file: requirements.txt
    set CONFIG_MISSING=1
)

if not exist "%SCRIPT_DIR%configs\settings.yaml" (
    echo ERROR: Missing configuration file: configs\settings.yaml
    set CONFIG_MISSING=1
)

if not exist "%SCRIPT_DIR%allure.properties" (
    echo ERROR: Missing configuration file: allure.properties
    set CONFIG_MISSING=1
)

if %CONFIG_MISSING%==1 (
    echo.
    echo Required configuration files are missing!
    echo Please ensure all configuration files are present before running setup.
    echo.
    pause
    exit /b 1
)

echo All required configuration files found.
echo.

REM Create necessary directories
echo Creating project directories...
if not exist "%SCRIPT_DIR%output" mkdir "%SCRIPT_DIR%output"
if not exist "%SCRIPT_DIR%output\allure" mkdir "%SCRIPT_DIR%output\allure"
if not exist "%SCRIPT_DIR%results" mkdir "%SCRIPT_DIR%results"
if not exist "%SCRIPT_DIR%allure-results" mkdir "%SCRIPT_DIR%allure-results"
if not exist "%SCRIPT_DIR%allure-report" mkdir "%SCRIPT_DIR%allure-report"
if not exist "%SCRIPT_DIR%reports" mkdir "%SCRIPT_DIR%reports"
if not exist "%SCRIPT_DIR%data\test_data" mkdir "%SCRIPT_DIR%data\test_data"
echo Directory setup complete.
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip
echo.

REM Install project dependencies
echo Installing project dependencies...
echo This may take several minutes...
echo.

echo Installing project requirements...
pip install -r "%SCRIPT_DIR%requirements.txt"
if errorlevel 1 (
    echo Failed to install project requirements!
    pause
    exit /b 1
)
echo Project requirements installed successfully.
echo.

echo Installing Chrome WebDriver...
python -c "try: import chromedriver_autoinstaller; chromedriver_autoinstaller.install(); print('Chrome WebDriver installed successfully'); except Exception as e: print(f'Warning: Could not install Chrome WebDriver - {e}')"
echo.

echo Setting up Allure reporting...
if exist "%SCRIPT_DIR%allure-2.34.1\allure-2.34.1\bin\allure.bat" (
    echo Allure binary found in project directory.
    set "PATH=%SCRIPT_DIR%allure-2.34.1\allure-2.34.1\bin;%PATH%"
    echo Allure added to PATH for this session.
) else (
    echo Warning: Allure binary not found in allure-2.34.1 directory.
    echo You may need to download and extract Allure manually.
)
echo.

echo ========================================
echo Project setup completed successfully!
echo ========================================
echo.
echo All dependencies have been installed.
echo.
echo Available commands:
echo   - Run all tests: run_all_tests_with_allure.bat
echo   - View test reports: Open allure-report\index.html
echo   - View Robot Framework reports: Open results\report.html
echo.
echo Project structure created:
echo   - output/: Robot Framework output files
echo   - results/: Test execution results
echo   - allure-results/: Allure test results
echo   - allure-report/: Generated Allure HTML reports
echo   - reports/: Additional test reports
echo.
pause

endlocal
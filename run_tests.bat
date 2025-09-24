@echo off
setlocal

REM Get the directory where this batch file is located
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

echo ========================================
echo Zinnia Live Automation Framework
echo Test Execution Script
echo ========================================
echo.

REM Check if setup has been run
if not exist "%SCRIPT_DIR%setup_log.txt" (
    echo WARNING: Setup may not have been run yet.
    echo Please run setup_project.bat first to install dependencies.
    echo.
    pause
    exit /b 1
)

echo Available options:
echo.
echo 1. Run verification test
echo 2. Run all tests
echo 3. Run tests with Allure reporting
echo 4. Start dashboard
echo 5. Generate Allure report
echo 6. Exit
echo.

set /p choice="Please select an option (1-6): "

if "%choice%"=="1" (
    echo.
    echo Running verification test...
    robot tests\verification\setup_verification.robot
    echo.
    echo Verification test completed.
    goto :end
)

if "%choice%"=="2" (
    echo.
    echo Running all tests...
    robot --outputdir results tests\
    echo.
    echo All tests completed. Check results\report.html for details.
    goto :end
)

if "%choice%"=="3" (
    echo.
    echo Running tests with Allure reporting...
    robot --outputdir results --listener allure_robotframework tests\
    echo.
    echo Tests completed. Generating Allure report...
    if exist "%SCRIPT_DIR%allure-2.34.1\allure-2.34.1\bin\allure.bat" (
        "%SCRIPT_DIR%allure-2.34.1\allure-2.34.1\bin\allure.bat" generate allure-results --clean -o allure-report
        echo Allure report generated. Open allure-report\index.html to view.
    ) else (
        echo Allure not found in project directory.
        echo Install Allure or use the allure command if it's in your PATH.
    )
    goto :end
)

if "%choice%"=="4" (
    echo.
    echo Starting dashboard...
    echo Dashboard will be available at http://localhost:5000
    echo Press Ctrl+C to stop the dashboard.
    echo.
    python dashboard.py
    goto :end
)

if "%choice%"=="5" (
    echo.
    echo Generating Allure report from existing results...
    if exist "%SCRIPT_DIR%allure-2.34.1\allure-2.34.1\bin\allure.bat" (
        "%SCRIPT_DIR%allure-2.34.1\allure-2.34.1\bin\allure.bat" generate allure-results --clean -o allure-report
        echo Allure report generated. Open allure-report\index.html to view.
    ) else (
        echo Allure not found in project directory.
        echo Install Allure or use the allure command if it's in your PATH.
    )
    goto :end
)

if "%choice%"=="6" (
    echo Goodbye!
    goto :end
)

echo Invalid choice. Please select a number between 1-6.
echo.
pause
goto :start

:end
echo.
echo Press any key to exit...
pause > nul

endlocal

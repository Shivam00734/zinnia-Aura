@echo off
REM Run all Robot Framework tests and generate consolidated Allure report
REM This script runs all tests and generates a single report in allure-report/

echo ========================================
echo   Run All Tests with Allure Reporting
echo ========================================

REM Clean previous results and reports
echo Cleaning previous results and reports...
if exist "allure-results" (
    rmdir /s /q "allure-results"
)
if exist "allure-report" (
    rmdir /s /q "allure-report"
)
if exist "output" (
    rmdir /s /q "output"
)

REM Create directories
mkdir "allure-results"
mkdir "output"

echo.
echo Running all Robot Framework tests...
echo Results directory: allure-results/
echo.

REM Run all tests with Allure reporting
robot --outputdir output --listener allure_robotframework;allure-results tests/

REM Check if tests ran
if not exist "allure-results\*.json" (
    echo.
    echo ERROR: No test results found in allure-results/
    echo Please check if tests executed properly.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   Generating Consolidated Allure Report
echo ========================================

REM Generate Allure report using our manager
python allure_manager.py generate

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo   SUCCESS: All tests completed!
    echo   
    echo   Reports generated:
    echo   - Robot Framework: output/report.html
    echo   - Allure Report: allure-report/index.html
    echo   
    echo   Results available in: allure-results/
    echo ========================================
) else (
    echo.
    echo ========================================
    echo   ERROR: Failed to generate Allure report
    echo   Check Robot Framework report: output/report.html
    echo ========================================
)

echo.
echo Press any key to exit...
pause >nul

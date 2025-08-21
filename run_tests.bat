@echo off
REM Clean previous results
if exist allure-results rmdir /s /q allure-results
if exist output rmdir /s /q output

REM Create directories
mkdir allure-results
mkdir output

REM Run Robot Framework tests with proper output directory
robot --outputdir output --listener allure_robotframework;allure-results tests/api/sample_api_test.robot

REM Generate Allure report
allure generate allure-results -o allure-report --clean
allure open allure-report 
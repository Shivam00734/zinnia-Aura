@echo off
REM Clean previous results
if exist allure-results rmdir /s /q allure-results
if exist allure-report rmdir /s /q allure-report

REM Create directories
mkdir allure-results
mkdir tests\api 2>nul

REM Run Robot Framework tests with Allure listener
robot --listener allure_robotframework;allure-results tests/api/sample_api.robot

REM Generate and open Allure report
allure generate allure-results -o allure-report --clean
allure open allure-report 
# 🚀 Zinnia Live Automation Framework - Quick Start Guide

Welcome! This guide will help you get started with the Zinnia Live automation framework in just a few minutes.

## 📋 Prerequisites

Before running the setup, ensure you have:

1. **Windows Operating System** (Windows 10 or later recommended)
2. **Python 3.8 or higher** - Download from [python.org](https://www.python.org/downloads/)
   - ⚠️ **IMPORTANT**: During Python installation, check "Add Python to PATH"
3. **Google Chrome Browser** - Download from [chrome.google.com](https://www.google.com/chrome/)
4. **Internet Connection** - Required for downloading dependencies

## 🎯 One-Click Setup

**Simply double-click on `setup_project.bat` and follow the on-screen instructions!**

The setup script will automatically:
- ✅ Check your system requirements
- ✅ Install all Python dependencies
- ✅ Set up Chrome WebDriver
- ✅ Configure Allure reporting
- ✅ Create necessary project directories
- ✅ Verify the installation

## 🔧 What Gets Installed

The setup will install these key components:
- **Robot Framework** - Test automation framework
- **Selenium WebDriver** - Web browser automation
- **Allure Framework** - Advanced test reporting
- **Python Libraries** - All required dependencies
- **Chrome WebDriver** - Browser automation driver

## 🚦 After Setup Completion

Once setup is complete, you can:

### 1. Test the Installation
```batch
robot tests\verification\setup_verification.robot
```

### 2. Run Your First Test
```batch
robot tests\your_test_file.robot
```

### 3. Start the Dashboard
```batch
python dashboard.py
```
Then open http://localhost:5000 in your browser

### 4. View Test Reports
- **Robot Framework Reports**: Open `results\report.html`
- **Allure Reports**: Open `allure-report\index.html`

## 📁 Project Structure

```
your-project/
├── tests/              # Your test files (.robot)
├── resources/           # Shared keywords and utilities
├── configs/             # Configuration files
├── data/               # Test data files
├── results/            # Test execution results
├── allure-report/      # HTML test reports
├── logs/               # Application logs
└── setup_project.bat   # One-click setup script
```

## 🛠️ Configuration Files

- **`configs/settings.yaml`** - Browser and test settings
- **`configs/dev.env.txt`** - Development environment variables
- **`configs/prod.env.txt`** - Production environment variables
- **`allure.properties`** - Allure reporting configuration

## ❗ Troubleshooting & Recovery

### 🚨 If Setup Fails

The enhanced setup script now handles most common issues automatically, but if problems persist:

#### 1. **Run System Diagnostics**
```batch
diagnose_system.bat
```
This will generate a comprehensive `diagnostic_report.txt` with system information to identify issues.

#### 2. **Try Recovery Setup**
```batch
recovery_setup.bat
```
This uses alternative installation methods and installs packages individually.

#### 3. **Common Issues & Solutions**

| Issue | Solution |
|-------|----------|
| **Python not found** | Install Python 3.8+ from python.org<br/>✅ **IMPORTANT**: Check "Add Python to PATH" |
| **Permission errors** | Right-click setup script → "Run as Administrator" |
| **Network/Proxy issues** | Contact IT for corporate firewall settings |
| **Antivirus blocking** | Temporarily disable real-time protection |
| **Chrome WebDriver fails** | Install Google Chrome browser first |
| **Java missing (Allure)** | Install Java 8+ from Oracle |

#### 4. **Corporate/Enterprise Environments**

If you're in a corporate environment with:
- **Proxy/Firewall**: The script auto-detects proxy settings
- **Restricted permissions**: Run as Administrator
- **Package restrictions**: Use `recovery_setup.bat` for individual installs

#### 5. **Check Log Files**

The setup process creates detailed logs:
- **`setup_log.txt`** - Main setup process log
- **`diagnostic_report.txt`** - System diagnostic information
- **`recovery_log.txt`** - Recovery attempt details

### 🔧 Manual Installation Steps

If all automated methods fail:

1. **Install Python packages manually**:
   ```batch
   pip install robotframework selenium requests
   pip install robotframework-seleniumlibrary
   pip install allure-robotframework
   ```

2. **Download ChromeDriver manually**:
   - Visit: https://chromedriver.chromium.org/
   - Download version matching your Chrome browser
   - Extract to project directory or PATH

3. **Install Allure manually**:
   - Download from: https://github.com/allure-framework/allure2/releases
   - Extract to `allure-2.34.1` directory in project

## 📞 Getting Help

If you encounter issues:
1. Check the `setup_log.txt` file for error details
2. Ensure all prerequisites are installed
3. Try running the setup script as Administrator
4. Contact the project maintainer with the contents of `setup_log.txt`

## 🎉 You're Ready!

Once setup is complete, you're ready to start automating tests with the Zinnia Live framework. Happy testing! 🧪

---

**Note**: This framework was designed to be completely self-contained. Anyone can clone this project and run the setup script to get started immediately!

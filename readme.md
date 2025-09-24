# Zinnia Live Automation Framework

🚀 **Enterprise-ready automation framework with one-click setup for web testing, API testing, and comprehensive reporting.**

## 🎯 Quick Start

**Get started in 3 simple steps:**

1. **Download/Clone this project**
2. **Double-click `setup_project.bat`**
3. **Follow the on-screen instructions**

That's it! All dependencies, libraries, and tools will be installed automatically.

## 📋 What's Included

- ✅ **Robot Framework** - Powerful test automation framework
- ✅ **Selenium WebDriver** - Web browser automation
- ✅ **API Testing** - RESTful API automation capabilities
- ✅ **Allure Reports** - Beautiful, detailed test reports
- ✅ **Excel Integration** - Data-driven testing from Excel files
- ✅ **Dashboard** - Real-time test execution monitoring
- ✅ **Multi-Environment Support** - Dev, staging, production configs

## 🛠️ Setup Tools

This framework includes multiple setup and troubleshooting tools:

| Tool | Purpose | When to Use |
|------|---------|-------------|
| **`setup_project.bat`** | Main setup with comprehensive error handling | First time setup and normal installations |
| **`diagnose_system.bat`** | System diagnostics and issue identification | When setup fails - generates detailed report |
| **`recovery_setup.bat`** | Alternative installation methods | When main setup fails |
| **`run_tests.bat`** | Test execution menu | After setup to run tests easily |

## 📚 Documentation

- **[Quick Start Guide](QUICK_START_GUIDE.md)** - Get up and running quickly
- **[Setup Tools Guide](SETUP_TOOLS_GUIDE.md)** - Detailed explanation of all setup tools
- **Troubleshooting** - Comprehensive problem-solving guide included

## 🏗️ Project Structure

```
automation-framework/
├── tests/                 # Test files (.robot)
├── resources/              # Shared keywords and utilities
├── configs/                # Environment configurations
├── data/                   # Test data files
├── results/                # Test execution results
├── allure-report/          # HTML test reports
├── logs/                   # Application logs
├── setup_project.bat       # 🚀 One-click setup
├── diagnose_system.bat     # 🔍 System diagnostics
├── recovery_setup.bat      # 🛠️ Recovery installation
└── run_tests.bat          # ▶️ Test execution menu
```

## 🚦 Getting Started

### Prerequisites
- **Windows 10+** (Windows 11 recommended)
- **Internet connection** (for downloading dependencies)

### Optional (will be installed automatically if missing):
- Python 3.8+
- Google Chrome
- Java 8+ (for Allure reports)

### Installation

1. **Download this project** to your local machine
2. **Run the setup**:
   ```batch
   setup_project.bat
   ```
3. **Wait for completion** - the script will:
   - Check your system requirements
   - Install all Python dependencies
   - Set up Chrome WebDriver
   - Configure Allure reporting
   - Create project directories
   - Verify the installation

### First Test

After setup, test your installation:
```batch
robot tests\verification\setup_verification.robot
```

### Start the Dashboard

Launch the web dashboard:
```batch
python dashboard.py
```
Then open http://localhost:5000 in your browser.

## 🧪 Running Tests

### Using the Menu
```batch
run_tests.bat
```
Select from the interactive menu options.

### Command Line
```batch
# Run all tests
robot tests\

# Run specific test suite
robot tests\api\

# Run with Allure reporting
robot --listener allure_robotframework tests\
```

## 📊 Viewing Reports

- **Robot Framework Reports**: Open `results\report.html`
- **Allure Reports**: Open `allure-report\index.html`
- **Dashboard**: http://localhost:5000 (when dashboard is running)

## 🔧 Configuration

- **Browser Settings**: `configs\settings.yaml`
- **Environment Variables**: 
  - `configs\dev.env.txt` (Development)
  - `configs\prod.env.txt` (Production)
- **Allure Configuration**: `allure.properties`

## 🚨 Troubleshooting

If setup fails:

1. **Run diagnostics**:
   ```batch
   diagnose_system.bat
   ```

2. **Try recovery setup**:
   ```batch
   recovery_setup.bat
   ```

3. **Check logs**:
   - `setup_log.txt` - Main setup log
   - `diagnostic_report.txt` - System analysis
   - `recovery_log.txt` - Recovery attempts

4. **See detailed troubleshooting guide**: [QUICK_START_GUIDE.md](QUICK_START_GUIDE.md)

## 🏢 Corporate Environments

This framework is designed to work in corporate environments with:
- ✅ **Proxy/Firewall detection and configuration**
- ✅ **Administrator privilege handling**
- ✅ **Antivirus compatibility**
- ✅ **Alternative installation methods**

## 🤝 Sharing This Project

This project is designed to be completely portable and self-contained. Anyone can:

1. **Receive the project folder**
2. **Run `setup_project.bat`**
3. **Start automating immediately**

No manual configuration or technical knowledge required!

## 📞 Support

If you encounter issues:

1. **Run `diagnose_system.bat`** and share the generated report
2. **Include the contents of `setup_log.txt`**
3. **Mention your environment** (corporate/home, Windows version, etc.)

## 🎉 Features

- **Zero-configuration setup** - Works out of the box
- **Multi-environment support** - Easy switching between dev/prod
- **Data-driven testing** - Excel, JSON, CSV support
- **Real-time reporting** - Live dashboard and detailed reports
- **Cross-browser testing** - Chrome, Firefox, Edge support
- **API testing** - REST API automation
- **Database testing** - SQL query execution
- **Document processing** - PDF and Excel manipulation
- **Comprehensive logging** - Detailed execution logs

---

**🚀 Ready to automate? Run `setup_project.bat` and start testing in minutes!**
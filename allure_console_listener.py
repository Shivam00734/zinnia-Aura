#!/usr/bin/env python3
"""
Enhanced Allure Console Listener for Robot Framework
Automatically captures console output and attaches it to Allure reports
"""

import os
import sys
import json
import time
import uuid
from datetime import datetime
from pathlib import Path
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn


class AllureConsoleListener:
    """Enhanced Allure listener that captures console output and process information"""
    
    ROBOT_LISTENER_API_VERSION = 3
    
    def __init__(self, output_dir="allure-results", console_capture=True):
        self.output_dir = Path(output_dir)
        self.console_capture = console_capture
        self.console_logs = []
        self.suite_logs = {}
        self.test_logs = {}
        self.current_suite = None
        self.current_test = None
        self.start_time = datetime.now()
        
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize console capture
        if self.console_capture:
            self._setup_console_capture()
    
    def _setup_console_capture(self):
        """Setup console output capture"""
        self.console_log_file = self.output_dir / "console_capture.log"
        self.console_logs.append(f"=== Console Capture Started at {self.start_time.strftime('%Y-%m-%d %H:%M:%S')} ===")
    
    def _log_to_console_capture(self, message, level="INFO"):
        """Add message to console capture"""
        timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        log_entry = f"[{timestamp}] {level}: {message}"
        self.console_logs.append(log_entry)
        
        # Also write to file immediately for real-time access
        if hasattr(self, 'console_log_file'):
            with open(self.console_log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry + '\n')
    
    def start_suite(self, data, result):
        """Called when a test suite starts"""
        self.current_suite = data.name
        self.suite_logs[self.current_suite] = []
        
        self._log_to_console_capture(f"SUITE START: {self.current_suite}")
        logger.info(f"Suite started: {self.current_suite}")
        
        # Create Allure environment file with enhanced information
        self._create_allure_environment()
    
    def end_suite(self, data, result):
        """Called when a test suite ends"""
        suite_name = self.current_suite
        elapsed_time = result.elapsed_time.total_seconds()
        
        self._log_to_console_capture(f"SUITE END: {suite_name} (Duration: {elapsed_time:.2f}s)")
        
        # Create suite summary file for Allure
        self._create_suite_summary(suite_name, result)
        
        logger.info(f"Suite completed: {suite_name} in {elapsed_time:.2f}s")
    
    def start_test(self, data, result):
        """Called when a test case starts"""
        self.current_test = data.name
        self.test_logs[self.current_test] = []
        
        self._log_to_console_capture(f"TEST START: {self.current_test}")
        logger.info(f"Test started: {self.current_test}")
    
    def end_test(self, data, result):
        """Called when a test case ends"""
        test_name = self.current_test
        elapsed_time = result.elapsed_time.total_seconds()
        status = result.status
        
        self._log_to_console_capture(f"TEST END: {test_name} - {status} (Duration: {elapsed_time:.2f}s)")
        
        # Create test-specific console log attachment
        self._create_test_console_attachment(test_name, result)
        
        if result.message:
            self._log_to_console_capture(f"TEST MESSAGE: {result.message}")
        
        logger.info(f"Test completed: {test_name} - {status} in {elapsed_time:.2f}s")
    
    def start_keyword(self, data, result):
        """Called when a keyword starts"""
        keyword_name = data.kwname
        if keyword_name and not keyword_name.startswith('BuiltIn.'):
            self._log_to_console_capture(f"KEYWORD START: {keyword_name}")
    
    def end_keyword(self, data, result):
        """Called when a keyword ends"""
        keyword_name = data.kwname
        if keyword_name and not keyword_name.startswith('BuiltIn.'):
            elapsed_time = result.elapsed_time.total_seconds()
            status = result.status
            self._log_to_console_capture(f"KEYWORD END: {keyword_name} - {status} (Duration: {elapsed_time:.3f}s)")
            
            if result.message and status == 'FAIL':
                self._log_to_console_capture(f"KEYWORD ERROR: {result.message}")
    
    def log_message(self, message):
        """Called when a log message is created"""
        if message.level in ['ERROR', 'FAIL', 'WARN']:
            self._log_to_console_capture(f"{message.level}: {message.message}")
    
    def message(self, message):
        """Called when a message is created"""
        if message.level in ['ERROR', 'FAIL', 'WARN']:
            self._log_to_console_capture(f"MESSAGE {message.level}: {message.message}")
    
    def close(self):
        """Called when the test execution ends"""
        end_time = datetime.now()
        total_duration = (end_time - self.start_time).total_seconds()
        
        self._log_to_console_capture(f"=== Console Capture Ended at {end_time.strftime('%Y-%m-%d %H:%M:%S')} ===")
        self._log_to_console_capture(f"Total Execution Duration: {total_duration:.2f}s")
        
        # Create final consolidated console log
        self._create_final_console_attachment()
        
        # Create execution summary
        self._create_execution_summary()
        
        logger.info(f"Console capture completed. Total duration: {total_duration:.2f}s")
    
    def _create_allure_environment(self):
        """Create Allure environment properties file"""
        try:
            builtin = BuiltIn()
            environment = builtin.get_variable_value("${ENVIRONMENT}", "Unknown")
            test_type = builtin.get_variable_value("${TEST_TYPE}", "Unknown")
        except:
            environment = "Unknown"
            test_type = "Unknown"
        
        env_data = {
            "Environment": environment,
            "Test_Type": test_type,
            "Platform": sys.platform,
            "Python_Version": sys.version.split()[0],
            "Start_Time": self.start_time.strftime('%Y-%m-%d %H:%M:%S'),
            "Console_Capture": "Enabled",
            "Robot_Framework": "Enhanced Logging"
        }
        
        # Write as properties file for Allure
        env_file = self.output_dir / "environment.properties"
        with open(env_file, 'w', encoding='utf-8') as f:
            for key, value in env_data.items():
                f.write(f"{key}={value}\n")
    
    def _create_suite_summary(self, suite_name, result):
        """Create suite execution summary"""
        summary_data = {
            "suite_name": suite_name,
            "status": result.status,
            "start_time": result.start_time.strftime('%Y-%m-%d %H:%M:%S'),
            "end_time": result.end_time.strftime('%Y-%m-%d %H:%M:%S'),
            "duration": result.elapsed_time.total_seconds(),
            "total_tests": result.test_count,
            "passed_tests": len([t for t in result.tests if t.status == 'PASS']),
            "failed_tests": len([t for t in result.tests if t.status == 'FAIL']),
            "message": result.message if result.message else ""
        }
        
        summary_file = self.output_dir / f"{suite_name}_summary.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, indent=2)
    
    def _create_test_console_attachment(self, test_name, result):
        """Create console log attachment for specific test"""
        # Filter console logs for this test
        test_logs = [log for log in self.console_logs if test_name in log or "TEST" in log]
        
        attachment_content = f"Console Output for Test: {test_name}\n"
        attachment_content += "=" * 60 + "\n"
        attachment_content += f"Status: {result.status}\n"
        attachment_content += f"Duration: {result.elapsed_time.total_seconds():.2f}s\n"
        attachment_content += f"Start Time: {result.start_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        attachment_content += f"End Time: {result.end_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        
        if result.message:
            attachment_content += f"Message: {result.message}\n"
        
        attachment_content += "=" * 60 + "\n\n"
        attachment_content += "Console Logs:\n"
        attachment_content += "\n".join(test_logs)
        
        # Save as attachment file
        attachment_file = self.output_dir / f"{test_name.replace(' ', '_')}_console.txt"
        with open(attachment_file, 'w', encoding='utf-8') as f:
            f.write(attachment_content)
        
        # Create Allure attachment metadata
        self._create_allure_attachment(attachment_file, f"Console Output - {test_name}", "text/plain")
    
    def _create_allure_attachment(self, file_path, name, content_type):
        """Create Allure attachment metadata"""
        attachment_uuid = str(uuid.uuid4())
        
        # Create attachment metadata JSON
        attachment_metadata = {
            "name": name,
            "source": file_path.name,
            "type": content_type
        }
        
        attachment_json_file = self.output_dir / f"{attachment_uuid}-attachment.json"
        with open(attachment_json_file, 'w', encoding='utf-8') as f:
            json.dump(attachment_metadata, f, indent=2)
        
        return attachment_uuid
    
    def _create_final_console_attachment(self):
        """Create final consolidated console log attachment"""
        final_content = "Complete Console Output\n"
        final_content += "=" * 60 + "\n"
        final_content += f"Execution Start: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        final_content += f"Total Logs: {len(self.console_logs)}\n"
        final_content += "=" * 60 + "\n\n"
        final_content += "\n".join(self.console_logs)
        
        final_file = self.output_dir / "complete_console_output.txt"
        with open(final_file, 'w', encoding='utf-8') as f:
            f.write(final_content)
        
        # Create Allure attachment metadata
        self._create_allure_attachment(final_file, "Complete Console Output", "text/plain")
    
    def _create_execution_summary(self):
        """Create overall execution summary"""
        end_time = datetime.now()
        summary = {
            "execution_summary": {
                "start_time": self.start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "total_duration": (end_time - self.start_time).total_seconds(),
                "suites_executed": len(self.suite_logs),
                "tests_executed": len(self.test_logs),
                "console_logs_captured": len(self.console_logs),
                "enhanced_logging": True
            }
        }
        
        summary_file = self.output_dir / "execution_summary.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2)

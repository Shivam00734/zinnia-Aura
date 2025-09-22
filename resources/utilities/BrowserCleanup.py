"""
Browser Cleanup Utility for Robot Framework Tests
Provides robust browser process management and cleanup functionality
"""

import os
import psutil
import subprocess
import time
import tempfile
import shutil
import glob
from pathlib import Path
from robot.api.deco import keyword, library
from robot.libraries.BuiltIn import BuiltIn


@library
class BrowserCleanup:
    """
    Comprehensive browser cleanup utility for handling browser processes,
    temporary files, and orphaned sessions during test execution.
    """
    
    def __init__(self):
        self.builtin = BuiltIn()
        self.browser_processes = [
            'chrome.exe', 'chromedriver.exe',
            'firefox.exe', 'geckodriver.exe', 
            'msedge.exe', 'msedgedriver.exe',
            'iexplore.exe', 'IEDriverServer.exe'
        ]
    
    @keyword
    def kill_all_browser_processes(self):
        """
        Kills all browser and webdriver processes forcefully.
        Returns the number of processes terminated.
        """
        terminated_count = 0
        
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                process_name = proc.info['name'].lower()
                if any(browser.lower() in process_name for browser in self.browser_processes):
                    self.builtin.log_to_console(f"🔄 Terminating process: {proc.info['name']} (PID: {proc.info['pid']})")
                    proc.terminate()
                    terminated_count += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        
        # Wait for processes to terminate gracefully
        time.sleep(2)
        
        # Force kill any remaining processes
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                process_name = proc.info['name'].lower()
                if any(browser.lower() in process_name for browser in self.browser_processes):
                    self.builtin.log_to_console(f"⚠️ Force killing stubborn process: {proc.info['name']} (PID: {proc.info['pid']})")
                    proc.kill()
                    terminated_count += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        
        self.builtin.log_to_console(f"✅ Terminated {terminated_count} browser processes")
        return terminated_count
    
    @keyword
    def get_browser_process_count(self):
        """
        Returns the current count of running browser processes.
        """
        count = 0
        processes = []
        
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                process_name = proc.info['name'].lower()
                if any(browser.lower() in process_name for browser in self.browser_processes):
                    count += 1
                    processes.append(f"{proc.info['name']} (PID: {proc.info['pid']})")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        
        if processes:
            self.builtin.log_to_console(f"📊 Found {count} browser processes: {', '.join(processes)}")
        
        return count
    
    @keyword
    def cleanup_browser_temp_files(self):
        """
        Cleans up browser temporary files and crashed session data.
        """
        cleaned_count = 0
        
        # Get common temp directories
        temp_dir = tempfile.gettempdir()
        user_profile = os.path.expanduser("~")
        
        # Chrome cleanup patterns
        chrome_patterns = [
            os.path.join(temp_dir, "chrome_driver_*"),
            os.path.join(temp_dir, "scoped_dir*"),
            os.path.join(user_profile, "AppData", "Local", "Google", "Chrome", "User Data", "Crashpad", "*"),
            os.path.join(user_profile, "AppData", "Local", "Google", "Chrome", "User Data", "Default", "*-journal"),
        ]
        
        # Firefox cleanup patterns
        firefox_patterns = [
            os.path.join(temp_dir, "rust_mozprofile*"),
            os.path.join(temp_dir, "tmp*", "rust_mozprofile*"),
            os.path.join(user_profile, "AppData", "Local", "Mozilla", "Firefox", "Profiles", "*", "sessionstore-backups", "*"),
        ]
        
        # Combine all patterns
        all_patterns = chrome_patterns + firefox_patterns
        
        for pattern in all_patterns:
            try:
                matching_paths = glob.glob(pattern)
                for path in matching_paths:
                    try:
                        if os.path.isdir(path):
                            shutil.rmtree(path, ignore_errors=True)
                            self.builtin.log_to_console(f"🗑️ Removed directory: {path}")
                        else:
                            os.remove(path)
                            self.builtin.log_to_console(f"🗑️ Removed file: {path}")
                        cleaned_count += 1
                    except Exception as e:
                        self.builtin.log_to_console(f"⚠️ Could not remove {path}: {str(e)}")
            except Exception as e:
                self.builtin.log_to_console(f"⚠️ Error processing pattern {pattern}: {str(e)}")
        
        self.builtin.log_to_console(f"✅ Cleaned {cleaned_count} temporary files/directories")
        return cleaned_count
    
    @keyword
    def is_browser_process_running(self, process_name):
        """
        Checks if a specific browser process is currently running.
        Args:
            process_name: Name of the process to check (e.g., 'chrome.exe')
        Returns:
            Boolean indicating if the process is running
        """
        for proc in psutil.process_iter(['name']):
            try:
                if proc.info['name'].lower() == process_name.lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        return False
    
    @keyword
    def wait_for_browser_process_termination(self, timeout_seconds=30):
        """
        Waits for all browser processes to terminate within the specified timeout.
        Args:
            timeout_seconds: Maximum time to wait for processes to terminate
        Returns:
            Boolean indicating if all processes terminated within timeout
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout_seconds:
            if self.get_browser_process_count() == 0:
                self.builtin.log_to_console("✅ All browser processes terminated successfully")
                return True
            time.sleep(1)
        
        remaining_count = self.get_browser_process_count()
        self.builtin.log_to_console(f"⚠️ Timeout reached. {remaining_count} browser processes still running")
        return False
    
    @keyword
    def emergency_browser_cleanup(self):
        """
        Performs emergency browser cleanup including processes and temp files.
        This is the main cleanup method to call when tests fail.
        """
        self.builtin.log_to_console("🚨 Starting Emergency Browser Cleanup...")
        
        # Step 1: Get initial process count
        initial_count = self.get_browser_process_count()
        self.builtin.log_to_console(f"📊 Initial browser processes: {initial_count}")
        
        # Step 2: Kill all browser processes
        terminated_count = self.kill_all_browser_processes()
        
        # Step 3: Wait for termination
        all_terminated = self.wait_for_browser_process_termination(15)
        
        # Step 4: Clean temporary files
        cleaned_files = self.cleanup_browser_temp_files()
        
        # Step 5: Final verification
        final_count = self.get_browser_process_count()
        
        # Summary
        self.builtin.log_to_console("📋 Emergency Cleanup Summary:")
        self.builtin.log_to_console(f"   • Initial processes: {initial_count}")
        self.builtin.log_to_console(f"   • Terminated processes: {terminated_count}")
        self.builtin.log_to_console(f"   • Final processes: {final_count}")
        self.builtin.log_to_console(f"   • Cleaned files: {cleaned_files}")
        self.builtin.log_to_console(f"   • All terminated: {all_terminated}")
        
        if final_count == 0:
            self.builtin.log_to_console("✅ Emergency Browser Cleanup completed successfully")
        else:
            self.builtin.log_to_console(f"⚠️ Emergency Browser Cleanup completed with {final_count} processes remaining")
        
        return {
            'initial_count': initial_count,
            'terminated_count': terminated_count,
            'final_count': final_count,
            'cleaned_files': cleaned_files,
            'all_terminated': all_terminated
        }
    
    @keyword
    def get_browser_cleanup_report(self):
        """
        Generates a detailed report of current browser process status.
        """
        report = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'total_processes': 0,
            'processes_by_type': {},
            'temp_files_exist': False
        }
        
        # Count processes by type
        for proc in psutil.process_iter(['pid', 'name', 'create_time']):
            try:
                process_name = proc.info['name'].lower()
                if any(browser.lower() in process_name for browser in self.browser_processes):
                    report['total_processes'] += 1
                    if process_name not in report['processes_by_type']:
                        report['processes_by_type'][process_name] = 0
                    report['processes_by_type'][process_name] += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        
        # Check for temp files
        temp_dir = tempfile.gettempdir()
        chrome_temp_exists = len(glob.glob(os.path.join(temp_dir, "chrome_driver_*"))) > 0
        firefox_temp_exists = len(glob.glob(os.path.join(temp_dir, "rust_mozprofile*"))) > 0
        report['temp_files_exist'] = chrome_temp_exists or firefox_temp_exists
        
        # Log report
        self.builtin.log_to_console("📊 Browser Cleanup Report:")
        self.builtin.log_to_console(f"   • Timestamp: {report['timestamp']}")
        self.builtin.log_to_console(f"   • Total browser processes: {report['total_processes']}")
        self.builtin.log_to_console(f"   • Processes by type: {report['processes_by_type']}")
        self.builtin.log_to_console(f"   • Temp files exist: {report['temp_files_exist']}")
        
        return report

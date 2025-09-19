#!/usr/bin/env python3
"""
Unified Cross-Platform Allure Report Manager
Works consistently in local development and CI/CD environments

Usage:
  python allure_unified.py generate                    # Generate report (CI-safe)
  python allure_unified.py generate --open             # Generate and open (local only)
  python allure_unified.py serve --port 8080           # Serve report on port
  python allure_unified.py run tests/api/demo.robot    # Run test + generate report
  python allure_unified.py clean                       # Clean all artifacts
  python allure_unified.py check                       # Check environment setup
"""

import os
import sys
import subprocess
import shutil
import json
import argparse
import platform
import tempfile
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any
import urllib.parse
import socket

# Detect CI/CD environment
def is_ci_environment() -> bool:
    """Detect if running in a CI/CD environment"""
    ci_indicators = [
        'CI', 'CONTINUOUS_INTEGRATION', 'BUILD_NUMBER', 'BUILD_ID',
        'JENKINS_URL', 'GITHUB_ACTIONS', 'GITLAB_CI', 'AZURE_PIPELINES',
        'TRAVIS', 'CIRCLECI', 'DRONE', 'BAMBOO_BUILD_NUMBER'
    ]
    return any(os.getenv(indicator) for indicator in ci_indicators)

def is_docker_environment() -> bool:
    """Detect if running inside Docker"""
    return os.path.exists('/.dockerenv') or os.getenv('DOCKER_CONTAINER') == 'true'

class UnifiedAllureManager:
    """Cross-platform Allure manager that works in both local and CI/CD environments"""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.is_ci = is_ci_environment()
        self.is_docker = is_docker_environment()
        self.project_root = Path.cwd()
        
        # Standard directories
        self.results_dir = self.project_root / "allure-results"
        self.report_dir = self.project_root / "allure-report"
        
        # Find Allure executable
        self.allure_bin = self._find_allure_executable()
        
        if verbose:
            self._print_environment_info()
    
    def _print_environment_info(self):
        """Print environment information for debugging"""
        print("=== Environment Information ===")
        print(f"Platform: {platform.system()} {platform.release()}")
        print(f"Python: {sys.version}")
        print(f"Working Directory: {self.project_root}")
        print(f"CI Environment: {self.is_ci}")
        print(f"Docker Environment: {self.is_docker}")
        print(f"Allure Binary: {self.allure_bin}")
        print("===============================")
    
    def _find_allure_executable(self) -> Optional[Path]:
        """Find Allure executable with fallback options"""
        # Try system installation first (common in CI/CD)
        if shutil.which("allure"):
            return Path("allure")
        
        # Try local installation (Windows)
        local_paths = [
            self.project_root / "allure-2.34.1" / "allure-2.34.1" / "bin" / "allure.bat",
            self.project_root / "allure-2.34.1" / "allure-2.34.1" / "bin" / "allure",
            # Alternative locations
            Path("/opt/allure/bin/allure"),
            Path("/usr/local/bin/allure"),
        ]
        
        for path in local_paths:
            if path.exists():
                return path
        
        return None
    
    def _run_command(self, cmd: List[str], check: bool = True, capture_output: bool = True, **kwargs) -> subprocess.CompletedProcess:
        """Run command with proper error handling and logging"""
        if self.verbose:
            print(f"Running: {' '.join(str(c) for c in cmd)}")
        
        try:
            result = subprocess.run(
                cmd, 
                check=check, 
                capture_output=capture_output, 
                text=True, 
                **kwargs
            )
            
            if self.verbose and result.stdout:
                print("STDOUT:", result.stdout)
            if self.verbose and result.stderr:
                print("STDERR:", result.stderr)
                
            return result
            
        except subprocess.CalledProcessError as e:
            print(f"ERROR: Command failed: {' '.join(str(c) for c in cmd)}")
            if e.stdout:
                print(f"STDOUT: {e.stdout}")
            if e.stderr:
                print(f"STDERR: {e.stderr}")
            raise
    
    def _ensure_directory(self, directory: Path, clean: bool = False) -> None:
        """Create directory, optionally cleaning it first"""
        if clean and directory.exists():
            shutil.rmtree(directory)
        directory.mkdir(parents=True, exist_ok=True)
    
    def check_environment(self) -> bool:
        """Check if the environment is properly set up for Allure reporting"""
        print("=== Environment Check ===")
        
        issues = []
        
        # Check Python
        python_version = sys.version_info
        if python_version < (3, 8):
            issues.append(f"Python version too old: {python_version}. Need 3.8+")
        else:
            print(f"✓ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
        
        # Check Allure CLI
        if not self.allure_bin:
            issues.append("Allure CLI not found. Install with: pip install allure-pytest or download from https://github.com/allure-framework/allure2/releases")
        else:
            try:
                result = self._run_command([str(self.allure_bin), "--version"])
                print(f"✓ Allure CLI: {result.stdout.strip()}")
            except Exception as e:
                issues.append(f"Allure CLI found but not working: {e}")
        
        # Check Robot Framework
        try:
            result = self._run_command(["robot", "--version"])
            print(f"✓ Robot Framework: {result.stdout.strip()}")
        except Exception:
            issues.append("Robot Framework not found. Install with: pip install robotframework")
        
        # Check allure-robotframework
        try:
            import allure_robotframework
            print(f"✓ allure-robotframework installed")
        except ImportError:
            issues.append("allure-robotframework not found. Install with: pip install allure-robotframework")
        
        # Check Java (required for Allure)
        try:
            result = self._run_command(["java", "-version"], capture_output=True)
            java_version = result.stderr.split('\n')[0] if result.stderr else "Unknown"
            print(f"✓ Java: {java_version}")
        except Exception:
            issues.append("Java not found. Allure requires Java Runtime Environment")
        
        # Check write permissions
        try:
            test_file = self.project_root / ".test_write_permission"
            test_file.write_text("test")
            test_file.unlink()
            print(f"✓ Write permissions: {self.project_root}")
        except Exception:
            issues.append(f"No write permission in: {self.project_root}")
        
        if issues:
            print("\n❌ Issues found:")
            for issue in issues:
                print(f"  - {issue}")
            return False
        else:
            print("\n✅ Environment is ready for Allure reporting!")
            return True
    
    def clean_all(self) -> None:
        """Clean all reports and results"""
        print("Cleaning Allure artifacts...")
        
        directories_to_clean = [
            self.results_dir,
            self.report_dir,
            self.project_root / "output",
            self.project_root / "results",
            self.project_root / "reports"
        ]
        
        for directory in directories_to_clean:
            if directory.exists():
                shutil.rmtree(directory)
                print(f"  Cleaned: {directory}")
        
        print("✅ Cleanup completed")
    
    def generate_report(self, 
                       results_path: Optional[Path] = None, 
                       output_path: Optional[Path] = None,
                       open_browser: bool = False,
                       single_file: bool = False) -> bool:
        """Generate Allure report"""
        
        if not self.allure_bin:
            print("❌ ERROR: Allure CLI not found!")
            print("Install options:")
            print("  1. System: Download from https://github.com/allure-framework/allure2/releases")
            print("  2. Docker: Use official allure image")
            print("  3. Node: npm install -g allure-commandline")
            return False
        
        results_path = results_path or self.results_dir
        output_path = output_path or self.report_dir
        
        # Check for results
        if not results_path.exists() or not any(results_path.glob("*.json")):
            print(f"❌ ERROR: No Allure results found in {results_path}")
            print("Run tests first with allure-robotframework listener")
            return False
        
        print(f"📊 Generating Allure report...")
        print(f"  Results: {results_path}")
        print(f"  Output: {output_path}")
        
        # Build command
        cmd = [str(self.allure_bin), "generate", str(results_path), "--clean", "-o", str(output_path)]
        
        if single_file:
            cmd.append("--single-file")
        
        try:
            self._run_command(cmd)
            
            # Verify report was generated
            index_file = output_path / "index.html"
            if index_file.exists():
                print(f"✅ SUCCESS: Allure report generated")
                print(f"   Report: {index_file}")
                
                # Open browser only in local environment
                if open_browser and not self.is_ci and not self.is_docker:
                    self._open_report(index_file)
                elif open_browser and (self.is_ci or self.is_docker):
                    print("🔒 Browser opening disabled in CI/Docker environment")
                
                return True
            else:
                print("❌ ERROR: Report generation failed - index.html not found")
                return False
                
        except subprocess.CalledProcessError:
            return False
    
    def _open_report(self, report_path: Path) -> None:
        """Open report in browser (local environment only)"""
        try:
            import webbrowser
            webbrowser.open(f"file://{report_path.absolute()}")
            print(f"🌐 Opened report in browser")
        except Exception as e:
            print(f"⚠️  Could not open browser: {e}")
    
    def serve_report(self, port: int = 8080, host: str = "0.0.0.0") -> None:
        """Serve Allure report on HTTP server"""
        
        if not self.allure_bin:
            print("❌ ERROR: Allure CLI not found!")
            return
        
        report_path = self.report_dir
        
        if not (report_path / "index.html").exists():
            print("📊 No report found, generating first...")
            if not self.generate_report():
                return
        
        print(f"🌐 Starting Allure report server...")
        print(f"   URL: http://localhost:{port}")
        print(f"   Host: {host}")
        print(f"   Report: {report_path}")
        print(f"   Press Ctrl+C to stop")
        
        try:
            cmd = [str(self.allure_bin), "open", str(report_path), "--port", str(port), "--host", host]
            self._run_command(cmd, capture_output=False)
        except KeyboardInterrupt:
            print("\n🛑 Server stopped")
        except Exception as e:
            print(f"❌ Server error: {e}")
    
    def run_test_with_allure(self, 
                            test_file: str, 
                            environment: Optional[str] = None,
                            variables: Optional[Dict[str, str]] = None,
                            generate_report: bool = True) -> bool:
        """Run Robot Framework test with Allure reporting"""
        
        test_path = Path(test_file)
        if not test_path.exists():
            print(f"❌ ERROR: Test file not found: {test_file}")
            return False
        
        # Create timestamped results if in CI, otherwise use standard location
        if self.is_ci:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            results_dir = self.project_root / "ci_results" / f"run_{timestamp}"
            output_dir = results_dir / "robot_output"
            allure_results_dir = results_dir / "allure-results"
        else:
            output_dir = self.project_root / "output"
            allure_results_dir = self.results_dir
        
        self._ensure_directory(output_dir, clean=True)
        self._ensure_directory(allure_results_dir, clean=True)
        
        print(f"🧪 Running test: {test_file}")
        print(f"   Output: {output_dir}")
        print(f"   Allure Results: {allure_results_dir}")
        
        # Build Robot Framework command
        cmd = [
            "robot",
            "--outputdir", str(output_dir),
            "--listener", f"allure_robotframework;{allure_results_dir}",
        ]
        
        # Add environment variables
        env = os.environ.copy()
        if environment:
            env['TEST_ENVIRONMENT'] = environment
            cmd.extend(["--variable", f"ENVIRONMENT:{environment}"])
        
        if variables:
            for key, value in variables.items():
                env[key] = value
                cmd.extend(["--variable", f"{key}:{value}"])
        
        # Add test file
        cmd.append(str(test_path))
        
        try:
            result = self._run_command(cmd, check=False, env=env)
            
            # Robot Framework returns non-zero for test failures, which is normal
            if result.returncode not in [0, 1]:
                print("❌ ERROR: Test execution failed!")
                return False
            
            print("✅ Test execution completed")
            
            # Generate report if requested
            if generate_report:
                return self.generate_report(
                    results_path=allure_results_dir,
                    open_browser=not self.is_ci and not self.is_docker
                )
            
            return True
            
        except Exception as e:
            print(f"❌ ERROR: Test execution failed: {e}")
            return False
    
    def copy_artifacts_for_ci(self, target_dir: str = "ci_artifacts") -> None:
        """Copy all important artifacts to a single directory for CI archiving"""
        target_path = Path(target_dir)
        self._ensure_directory(target_path, clean=True)
        
        print(f"📦 Copying artifacts to {target_path}")
        
        # Copy Allure report
        if self.report_dir.exists():
            shutil.copytree(self.report_dir, target_path / "allure-report")
            print(f"   ✓ Allure report")
        
        # Copy Robot output
        output_dir = self.project_root / "output"
        if output_dir.exists():
            shutil.copytree(output_dir, target_path / "robot-output")
            print(f"   ✓ Robot output")
        
        # Copy Allure results (for debugging)
        if self.results_dir.exists():
            shutil.copytree(self.results_dir, target_path / "allure-results")
            print(f"   ✓ Allure results")
        
        # Create summary file
        summary = {
            "timestamp": datetime.now().isoformat(),
            "environment": {
                "ci": self.is_ci,
                "docker": self.is_docker,
                "platform": platform.system(),
                "python_version": sys.version,
            },
            "allure_report_available": (target_path / "allure-report" / "index.html").exists(),
            "robot_report_available": (target_path / "robot-output" / "report.html").exists(),
        }
        
        with open(target_path / "summary.json", "w") as f:
            json.dump(summary, f, indent=2)
        
        print(f"✅ Artifacts ready for CI archiving: {target_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Unified Cross-Platform Allure Report Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python allure_unified.py check                           # Check environment
  python allure_unified.py generate                        # Generate report (CI-safe)
  python allure_unified.py generate --open                 # Generate and open
  python allure_unified.py generate --single-file          # Single HTML file
  python allure_unified.py serve --port 8080               # Serve on port 8080
  python allure_unified.py run tests/api/demo.robot        # Run test + report
  python allure_unified.py run tests/api/demo.robot -e QA  # Run with environment
  python allure_unified.py clean                           # Clean all artifacts
  python allure_unified.py ci-artifacts                    # Prepare CI artifacts
        """
    )
    
    parser.add_argument("command", 
                       choices=["check", "generate", "serve", "run", "clean", "ci-artifacts"],
                       help="Command to execute")
    
    parser.add_argument("test_file", nargs="?", 
                       help="Test file to run (required for 'run' command)")
    
    parser.add_argument("--open", action="store_true",
                       help="Open report in browser after generation")
    
    parser.add_argument("--single-file", action="store_true",
                       help="Generate single HTML file report")
    
    parser.add_argument("--port", type=int, default=8080,
                       help="Port for serve command (default: 8080)")
    
    parser.add_argument("--host", default="0.0.0.0",
                       help="Host for serve command (default: 0.0.0.0)")
    
    parser.add_argument("-e", "--environment",
                       help="Test environment (e.g., QA, UAT, PROD)")
    
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Enable verbose output")
    
    args = parser.parse_args()
    
    manager = UnifiedAllureManager(verbose=args.verbose)
    
    try:
        if args.command == "check":
            success = manager.check_environment()
            sys.exit(0 if success else 1)
        
        elif args.command == "generate":
            success = manager.generate_report(
                open_browser=args.open,
                single_file=args.single_file
            )
            sys.exit(0 if success else 1)
        
        elif args.command == "serve":
            manager.serve_report(port=args.port, host=args.host)
        
        elif args.command == "run":
            if not args.test_file:
                print("❌ ERROR: Test file is required for 'run' command")
                sys.exit(1)
            
            success = manager.run_test_with_allure(
                args.test_file,
                environment=args.environment
            )
            sys.exit(0 if success else 1)
        
        elif args.command == "clean":
            manager.clean_all()
        
        elif args.command == "ci-artifacts":
            manager.copy_artifacts_for_ci()
    
    except KeyboardInterrupt:
        print("\n🛑 Operation cancelled")
        sys.exit(0)
    except Exception as e:
        print(f"❌ ERROR: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

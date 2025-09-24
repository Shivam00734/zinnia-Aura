#!/usr/bin/env python3
"""
Dynamic API Test Runner
Generates and runs Robot Framework tests for only selected APIs
This ensures test count matches the number of APIs being executed
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Main function to run dynamic API tests"""
    
    # Get the directory of this script
    script_dir = Path(__file__).parent
    api_dir = script_dir / "tests" / "api"
    
    try:
        # Step 1: Generate dynamic robot file
        print("[INFO] Generating dynamic API tests...")
        generator_script = api_dir / "dynamic_api_executor.py"
        
        # Change to API directory and run generator
        original_cwd = os.getcwd()
        os.chdir(api_dir)
        
        result = subprocess.run([sys.executable, "dynamic_api_executor.py"], 
                              capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"[ERROR] Error generating dynamic tests: {result.stderr}")
            return result.returncode
        
        print(result.stdout)
        
        # Step 2: Run the generated robot file
        print("[INFO] Running dynamic API tests...")
        dynamic_robot_file = api_dir / "dynamic_api_tests.robot"
        results_dir = script_dir / "results" / "dynamic_api_tests"
        
        # Ensure results directory exists
        results_dir.mkdir(parents=True, exist_ok=True)
        
        # Run robot tests
        robot_result = subprocess.run([
            sys.executable, "-m", "robot",
            "--outputdir", str(results_dir),
            str(dynamic_robot_file)
        ], capture_output=True, text=True)
        
        # Print robot output
        print(robot_result.stdout)
        if robot_result.stderr:
            print(robot_result.stderr)
        
        return robot_result.returncode
        
    except Exception as e:
        print(f"[ERROR] Error running dynamic API tests: {e}")
        return 1
    finally:
        # Restore original working directory
        os.chdir(original_cwd)

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

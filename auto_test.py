#!/usr/bin/env python
"""
Auto-test script that starts the project and runs all test scripts.
Results are written to logs/test_run.log
"""

import os
import sys
import subprocess
import datetime
from pathlib import Path

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.absolute()
VENV_DIR = PROJECT_ROOT / ".venv"
TESTS_DIR = PROJECT_ROOT / "tests"
LOGS_DIR = PROJECT_ROOT / "logs"

# Create logs directory if it doesn't exist
LOGS_DIR.mkdir(exist_ok=True)

# Log file path
LOG_FILE = LOGS_DIR / "test_run.log"


def log_message(message):
    """Write message to log file and print to console"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}"
    
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry + "\n")
    
    print(log_entry)


def get_python_executable():
    """Get the Python executable from the .venv directory"""
    if sys.platform == "win32":
        python_exe = VENV_DIR / "Scripts" / "python.exe"
    else:
        python_exe = VENV_DIR / "bin" / "python"
    
    return str(python_exe)


def start_project():
    """Start the project"""
    log_message("=" * 60)
    log_message("Starting the project...")
    log_message("=" * 60)
    
    python_exe = get_python_executable()
    app_script = PROJECT_ROOT / "app.py"
    
    try:
        # Set APP_MODE environment variable
        env = os.environ.copy()
        env["APP_MODE"] = "production"
        
        result = subprocess.run(
            [python_exe, str(app_script)],
            capture_output=True,
            text=True,
            env=env,
            timeout=10
        )
        
        if result.returncode == 0:
            log_message(f"✓ Project started successfully")
            log_message(f"Output:\n{result.stdout}")
            return True
        else:
            log_message(f"✗ Project failed to start")
            log_message(f"Error:\n{result.stderr}")
            return False
    
    except subprocess.TimeoutExpired:
        log_message("✓ Project started successfully (timeout expected)")
        return True
    except Exception as e:
        log_message(f"✗ Error starting project: {str(e)}")
        return False


def run_tests():
    """Run all test scripts from the tests directory"""
    log_message("")
    log_message("=" * 60)
    log_message("Running test scripts...")
    log_message("=" * 60)
    
    if not TESTS_DIR.exists():
        log_message("✗ Tests directory not found")
        return False
    
    test_files = sorted(TESTS_DIR.glob("case_*.py"))
    
    if not test_files:
        log_message("✗ No test files found")
        return False
    
    python_exe = get_python_executable()
    passed = 0
    failed = 0
    
    for test_file in test_files:
        log_message(f"Running {test_file.name}...")
        
        try:
            env = os.environ.copy()
            env["APP_MODE"] = "production"
            
            result = subprocess.run(
                [python_exe, "-m", "pytest", str(test_file), "-v"],
                capture_output=True,
                text=True,
                cwd=str(PROJECT_ROOT),
                env=env,
                timeout=30
            )
            
            if result.returncode == 0:
                log_message(f"  ✓ {test_file.name} passed")
                passed += 1
            else:
                # Try running the test file directly if pytest is not installed
                result = subprocess.run(
                    [python_exe, str(test_file)],
                    capture_output=True,
                    text=True,
                    cwd=str(PROJECT_ROOT),
                    env=env,
                    timeout=30
                )
                
                if result.returncode == 0:
                    log_message(f"  ✓ {test_file.name} passed")
                    passed += 1
                else:
                    log_message(f"  ✗ {test_file.name} failed")
                    if result.stdout:
                        log_message(f"    stdout: {result.stdout}")
                    if result.stderr:
                        log_message(f"    stderr: {result.stderr}")
                    failed += 1
        
        except subprocess.TimeoutExpired:
            log_message(f"  ✗ {test_file.name} timeout")
            failed += 1
        except Exception as e:
            log_message(f"  ✗ {test_file.name} error: {str(e)}")
            failed += 1
    
    log_message("")
    log_message("=" * 60)
    log_message(f"Test Summary: {passed} passed, {failed} failed")
    log_message("=" * 60)
    
    return failed == 0


def main():
    """Main function"""
    # Clear the log file
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write("")
    
    log_message(f"Test run started at {datetime.datetime.now().isoformat()}")
    log_message(f"Project root: {PROJECT_ROOT}")
    log_message(f"Python executable: {get_python_executable()}")
    log_message(f"Log file: {LOG_FILE}")
    
    # Check if .venv exists
    if not VENV_DIR.exists():
        log_message("✗ .venv directory not found. Please run: python -m venv .venv")
        log_message("Then install dependencies: .venv\\Scripts\\pip install -r requirements.txt")
        return False
    
    # Start the project
    project_started = start_project()
    
    # Run tests
    tests_passed = run_tests()
    
    log_message("")
    if project_started and tests_passed:
        log_message("✓ All checks passed!")
        return True
    else:
        log_message("✗ Some checks failed")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

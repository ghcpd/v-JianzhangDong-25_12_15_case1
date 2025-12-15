#!/usr/bin/env python3
"""
auto_test.py

Helper script to start the project and run tests using the interpreter inside .venv.
It sets APP_MODE=production for the test run and writes full output to logs/test_run.log.

Usage:
  ./.venv/bin/python auto_test.py    (POSIX)
  .\.venv\Scripts\python.exe auto_test.py (Windows)
"""
from __future__ import annotations
import os
import subprocess
import sys
from pathlib import Path


def venv_python_path(root: Path) -> str:
    if os.name == "nt":
        return str(root / ".venv" / "Scripts" / "python.exe")
    return str(root / ".venv" / "bin" / "python")


def main() -> int:
    root = Path(__file__).resolve().parent
    venv_dir = root / ".venv"
    py = venv_python_path(root)

    if not venv_dir.exists():
        print("ERROR: .venv not found. Please create a virtual environment and install requirements first.")
        return 2

    logs_dir = root / "logs"
    logs_dir.mkdir(exist_ok=True)
    log_file = logs_dir / "test_run.log"

    # Ensure APP_MODE is set to production for the run
    env = os.environ.copy()
    env["APP_MODE"] = "production"

    # Start the project once (app.py prints and exits)
    try:
        start_proc = subprocess.run(
            [py, str(root / "app.py")],
            capture_output=True,
            text=True,
            env=env,
        )
    except Exception as e:
        with open(log_file, "w", encoding="utf-8") as f:
            f.write(f"Failed to start app.py: {e}\n")
        print(f"Failed to start app.py: {e}")
        return 3

    # Run pytest under the venv python so that sys.executable in tests points to the venv
    try:
        # Pytest default collection pattern won't pick up files named case_*.py,
        # so explicitly pass all Python files from the tests/ directory.
        tests_dir = root / "tests"
        test_files = sorted([str(p) for p in tests_dir.glob("*.py") if p.is_file()])
        if test_files:
            cmd = [py, "-m", "pytest"] + test_files + ["-q"]
        else:
            cmd = [py, "-m", "pytest", "tests", "-q"]

        test_proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            env=env,
        )
    except Exception as e:
        with open(log_file, "w", encoding="utf-8") as f:
            f.write(f"Failed to run tests: {e}\n")
        print(f"Failed to run tests: {e}")
        return 4

    # Write a combined log
    with open(log_file, "w", encoding="utf-8") as f:
        f.write("--- app.py stdout ---\n")
        if start_proc.stdout:
            f.write(start_proc.stdout)
        if start_proc.stderr:
            f.write("\n--- app.py stderr ---\n")
            f.write(start_proc.stderr)

        f.write("\n\n--- pytest stdout/stderr ---\n")
        if test_proc.stdout:
            f.write(test_proc.stdout)
        if test_proc.stderr:
            f.write("\n--- pytest stderr ---\n")
            f.write(test_proc.stderr)

    print(f"Test run finished; logs written to: {log_file}")
    return test_proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())

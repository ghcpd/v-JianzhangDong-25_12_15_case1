import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VENV_PY = ROOT / (Path(".venv") / "Scripts" / "python.exe" if os.name == "nt" else Path(".venv") / "bin" / "python")
LOG_DIR = ROOT / "logs"
LOG_FILE = LOG_DIR / "test_run.log"

def ensure_logs():
    LOG_DIR.mkdir(parents=True, exist_ok=True)

def run_app(venv_python):
    # Accept either the venv python or a fallback system python executable
    if not Path(venv_python).exists():
        venv_python = Path(sys.executable)
        print("Warning: .venv python not found, falling back to system python:", venv_python)

    env = os.environ.copy()
    env["APP_MODE"] = "production"
    proc = subprocess.run(
        [str(venv_python), "app.py"],
        capture_output=True,
        text=True,
        env=env,
    )
    return proc

def run_tests(venv_python):
    env = os.environ.copy()
    env["APP_MODE"] = "production"
    proc = subprocess.run(
        [str(venv_python), "-m", "pytest", "tests", "-q"],
        capture_output=True,
        text=True,
        env=env,
    )
    return proc

if __name__ == "__main__":
    ensure_logs()

    # Prefer .venv Python if available, otherwise fall back to the current interpreter
    if VENV_PY.exists():
        python_exec = VENV_PY
        print("Using venv python at", python_exec)
    else:
        python_exec = Path(sys.executable)
        print("Warning: .venv python not found; falling back to system python:", python_exec)

    try:
        with LOG_FILE.open("w", encoding="utf-8") as f:
            f.write(f"Python executable: {python_exec}\n")
            f.write("=== Starting app.py ===\n")
            app_proc = run_app(python_exec)
            f.write(f"returncode: {app_proc.returncode}\n")
            f.write(app_proc.stdout + "\n")
            if app_proc.stderr:
                f.write("stderr:\n" + app_proc.stderr + "\n")

            f.write("\n=== Running pytest ===\n")
            test_proc = run_tests(python_exec)
            f.write(f"returncode: {test_proc.returncode}\n")
            f.write(test_proc.stdout + "\n")
            if test_proc.stderr:
                f.write("stderr:\n" + test_proc.stderr + "\n")
        rc = test_proc.returncode if 'test_proc' in locals() else app_proc.returncode if 'app_proc' in locals() else 1
        print("Test run complete. See", LOG_FILE)
        sys.exit(rc)
    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        with LOG_FILE.open("w", encoding="utf-8") as f:
            f.write("=== ERROR ===\n")
            f.write(tb)
        print("Error occurred during test run; written to", LOG_FILE)
        sys.exit(1)

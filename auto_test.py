import os
import subprocess
import sys
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "test_run.log"

# locate venv python
VENV_PY = Path('.venv') / ('Scripts' if os.name == 'nt' else 'bin') / ('python.exe' if os.name == 'nt' else 'python')

if not VENV_PY.exists():
    print("Virtual environment not found at .venv/. Creating a fresh one...")
    # create venv
    subprocess.check_call([sys.executable, '-m', 'venv', '.venv'])
    # upgrade pip and install requirements
    subprocess.check_call([str(VENV_PY), '-m', 'pip', 'install', '--upgrade', 'pip'])
    subprocess.check_call([str(VENV_PY), '-m', 'pip', 'install', '-r', 'requirements.txt'])

env = os.environ.copy()
env['APP_MODE'] = 'production'

with open(LOG_FILE, 'w', encoding='utf-8') as logf:
    logf.write('=== Starting app.py ===\n')
    try:
        p = subprocess.run([str(VENV_PY), 'app.py'], capture_output=True, text=True, env=env)
        logf.write(p.stdout)
        logf.write(p.stderr)
        logf.write(f'Exit code: {p.returncode}\n')
    except Exception as e:
        logf.write(f'Failed to start app.py: {e}\n')

    logf.write('\n=== Running pytest ===\n')
    try:
        # Run pytest and explicitly pass each test file so files that do not match pytest's default discovery
        # pattern (e.g., `case_*.py`) are still executed.
        test_files = sorted([str(p) for p in Path('tests').glob('*.py')])
        if not test_files:
            logf.write('No test files found under tests/\n')
            p2 = subprocess.CompletedProcess(args=[], returncode=0)
        else:
            cmd = [str(VENV_PY), '-m', 'pytest', '-q'] + test_files
            p2 = subprocess.run(cmd, capture_output=True, text=True, env=env)
        logf.write(p2.stdout or '')
        logf.write(p2.stderr or '')
        logf.write(f'Exit code: {p2.returncode}\n')
    except Exception as e:
        logf.write(f'Failed to run pytest: {e}\n')

# exit with pytest code if available
try:
    exit_code = p2.returncode
except NameError:
    exit_code = 1

sys.exit(exit_code)

import os
import subprocess
import sys
from pathlib import Path

# Determine the project's virtual environment python executable
if os.name == 'nt':
    python_exe = Path('.venv', 'Scripts', 'python.exe')
else:
    python_exe = Path('.venv', 'bin', 'python')

if not python_exe.exists():
    print('Virtual environment not found at .venv/. Please run the setup step first.', file=sys.stderr)
    sys.exit(1)

# Ensure the logs directory exists
logs_dir = Path('logs')
logs_dir.mkdir(exist_ok=True)

log_path = logs_dir / 'test_run.log'

# Prepare environment for running tests
env = os.environ.copy()
env['APP_MODE'] = 'production'

print(f'Running tests using: {python_exe}', file=sys.stderr)
print('Logging results to:', log_path, file=sys.stderr)

with log_path.open('w', encoding='utf-8') as log_file:
    # Run pytest on each test file in the tests/ directory (explicit paths so pytest finds tests even if file names do not start with 'test_')
    # If pytest is not installed in the venv, attempt to run the tests directly via python -m pytest
    results = []
    test_dir = Path('tests')
    for path in sorted(test_dir.glob('*.py')):
        res = subprocess.run([str(python_exe), '-m', 'pytest', str(path)],
                             capture_output=True, text=True, env=env)
        results.append((path, res))

    # Pick the exit code as non-zero if any test run failed
    exit_code = 0

    for path, res in results:
        # Log each file's output
        log_file.write('\n==== Running ' + str(path) + ' ====\n')
        log_file.write(res.stdout)
        log_file.write('\n')
        log_file.write(res.stderr)
        if res.returncode != 0:
            exit_code = res.returncode
    # Add a newline at end of logs
    log_file.write('\n')

    # Also write a short summary to stderr and log
    summary = f'Exit code: {exit_code}'
    log_file.write('\n' + summary + '\n')
    print(summary, file=sys.stderr)

    # Exit with the overall return code so CI can detect failures
    sys.exit(exit_code)

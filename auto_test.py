import subprocess
import sys
import os
from pathlib import Path
import importlib.util

# Set environment variable
os.environ['APP_MODE'] = 'production'

# Path to venv python
venv_python = Path('.venv/Scripts/python.exe')

# Test files and functions
tests = [
    ('tests/case_1', 'test_app_starts'),
    ('tests/case_2', 'test_output_contains_port'),
    ('tests/case_3', 'test_correct_port'),
]

# Log file
log_file = 'logs/test_run.log'

with open(log_file, 'w') as log:
    log.write("Starting project...\n")
    # Start the project (run app.py)
    result = subprocess.run([str(venv_python), 'app.py'], capture_output=True, text=True)
    log.write(f"App output: {result.stdout}\n")
    log.write(f"App errors: {result.stderr}\n")
    log.write(f"App return code: {result.returncode}\n\n")

    log.write("Running tests...\n")
    for module_name, func_name in tests:
        log.write(f"Running {module_name}.{func_name}...\n")
        try:
            # Load the module
            spec = importlib.util.spec_from_file_location(module_name, f"{module_name}.py")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            # Call the function
            getattr(module, func_name)()
            log.write("Test passed.\n\n")
        except Exception as e:
            log.write(f"Test failed: {e}\n\n")

    log.write("All tests completed.\n")
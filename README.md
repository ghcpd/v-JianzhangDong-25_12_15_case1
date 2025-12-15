
# oswe-mini-uiberry-1210 — Minimal service example

This repository contains a minimal Python service example (app.py) with simple configuration and tests.

Summary
- app.py: simple entrypoint that loads configuration and prints the service port
- config.py: loads settings.yaml and requires APP_MODE environment variable
- settings.yaml: contains the service port (default: 9123)
- tests/: three pytest-style test files that verify the app starts and prints the correct port

Important notes
- The application requires the environment variable APP_MODE to be set to "production" before running.
- The test suite expects to run under a Python virtual environment (.venv) so that subprocesses use the same interpreter.

Prerequisites
- Python 3.8+ (Windows: use PowerShell / CMD)

Quick setup (recommended)
1) Create a clean virtual environment and install dependencies:

   Windows (PowerShell):

	   Remove-Item -Recurse -Force .venv -ErrorAction Ignore; python -m venv .venv; \
	   .\.venv\Scripts\python.exe -m pip install --upgrade pip; \
	   .\.venv\Scripts\python.exe -m pip install -r requirements.txt

   POSIX (macOS / Linux):

	   rm -rf .venv; python3 -m venv .venv; \
	   ./.venv/bin/python -m pip install --upgrade pip; \
	   ./.venv/bin/python -m pip install -r requirements.txt

2) Run the application (example)

   Windows (PowerShell):

	   $env:APP_MODE = 'production'; .\.venv\Scripts\python.exe app.py

   POSIX (bash):

	   APP_MODE=production ./.venv/bin/python app.py

   Expected output:

	   Service started successfully
	   Port: 9123

Running tests with the provided helper (auto_test.py)

The repository includes auto_test.py which will:
- ensure tests run using the interpreter inside .venv/
- set APP_MODE=production for the test run
- start the project once (app.py) and then run pytest against tests/
- write all test output to logs/test_run.log

Usage (run from repository root):

   .\.venv\Scripts\python.exe auto_test.py    # Windows (PowerShell)
   ./.venv/bin/python auto_test.py             # POSIX

The script will return the same exit code as pytest and create logs/test_run.log with full output.

Why files were changed
- requirements.txt: pytest was added so the test suite can be executed in CI/.venv
- .gitignore: added to prevent committing .venv and logs/
- auto_test.py: helper to start the project and run tests using .venv interpreter

Notes for maintainers / CI
- CI should create a fresh virtual environment from requirements.txt and run:

	$env:APP_MODE = 'production' ; .\.venv\Scripts\python.exe -m pytest tests

  or use the provided helper:

	.\.venv\Scripts\python.exe auto_test.py

Backup
- A copy of the original README.md has been saved as README_backup.md in the repository root.

Contact
- No external services are required for this project. If you need help, inspect app.py and config.py to see the minimal run logic.

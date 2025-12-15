# Project Overview

This repository contains a minimal Python service (`app.py`) that demonstrates a simple configuration loader and a basic runtime check.

## Project Structure

- `app.py` - Application entry point that reads configuration and validates the environment before starting.
- `config.py` - Loads configuration from `settings.yaml` and environment variables.
- `settings.yaml` - Default settings (port).
- `requirements.txt` - Python dependencies.
- `tests/` - Test scripts to validate app behavior.

## Prerequisites

- **Python 3.8+** installed and available in your PATH.
- A working network connection to install dependencies from PyPI.

## Setup and Installation

1. **Create a clean virtual environment** (do not reuse an existing env):

   ```powershell
   # From the project root
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1  # PowerShell
   # or .\.venv\Scripts\activate.bat for CMD
   ```

2. **Install dependencies** using the project's `requirements.txt`:

   ```powershell
   pip install -r requirements.txt
   ```

3. **Set the required environment variable** to `production` before running the app:

   ```powershell
   $Env:APP_MODE = "production"  # PowerShell
   # or set APP_MODE=production in your shell
   ```

## Running the Application

```powershell
python app.py
```

You should see output similar to:

```
Service started successfully
Port: 9123
```

## Running Tests

The tests are located under the `tests/` folder and can be executed using Python (they use `subprocess` to run `app.py`).

To run them locally:

```powershell
python -m pytest tests
```

Or run the provided `auto_test.py` script (see next section).

## Auto-test script

Run the automated test runner that uses the virtual environment to execute the tests and writes results to a log file:

```powershell
python auto_test.py
```

Logs will be written to `logs/test_run.log`.

## Notes

- This project expects an environment variable `APP_MODE` set to `production` for `app.py` to start successfully.
- If you are on Windows cmd or other shells, adapt the activation and environment variable commands accordingly.

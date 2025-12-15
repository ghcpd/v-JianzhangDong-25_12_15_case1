# oswe-mini-prime-new

A minimal sample Python service that reads configuration from `settings.yaml` and requires the `APP_MODE` environment variable to be set to `production`.

## Requirements

- Python 3.8+
- `requirements.txt` contains project dependencies (install into a virtual environment)

## Setup (Windows PowerShell)

1. Create a clean virtual environment in `.venv/` (delete if present):

   Remove any existing env and create a fresh one:

   ```powershell
   Remove-Item -Recurse -Force .venv -ErrorAction SilentlyContinue
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

2. Ensure the `APP_MODE` environment variable is set to `production` in your current session:

   ```powershell
   $env:APP_MODE = 'production'
   ```

3. Start the service:

   ```powershell
   python app.py
   ```

   Expected output on success:
   ```text
   Service started successfully
   Port: 9123
   ```

## Running tests

After activating `.venv/` and setting `$env:APP_MODE='production'`, run the project tests:

```powershell
python -m pytest tests
```

## Automated test runner

An `auto_test.py` helper is included to:
- Start the project (using `.venv` Python)
- Run all tests in `tests/` using the virtual environment
- Write results to `logs/test_run.log`

Run it with the virtual env activated (or via `.venv\\Scripts\\python.exe`):

```powershell
python auto_test.py
```

## Notes

- The configuration file `settings.yaml` must exist and contain an integer `service.port` (currently `9123`).
- `APP_MODE` must be set to `production` when starting the app or running tests.

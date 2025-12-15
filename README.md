# Project: Simple Service Example

This repository provides a minimal Python service example that reads configuration from `settings.yaml`, requires the `APP_MODE` environment variable to be set to `production`, and prints its listening port when started.

---

## Quick setup

1. Create a clean virtual environment and install dependencies (Windows PowerShell):

   Remove any existing environment and create a fresh one:

   ```powershell
   Remove-Item -Recurse -Force .venv -ErrorAction SilentlyContinue
   python -m venv .venv
   .\.venv\Scripts\python -m pip install --upgrade pip
   .\.venv\Scripts\python -m pip install -r requirements.txt
   ```

   Notes:
   - The project requires Python 3.8+.
   - `requirements.txt` currently contains `pyyaml` which is used to parse `settings.yaml`.

2. Ensure `.venv/` is ignored by git. See the `.gitignore` file for recommended entries.

3. Confirm configuration file (`settings.yaml`) exists and contains a valid integer port under `service.port` (the provided file uses port `9123`).

4. Set the required environment variable before running the service or tests:

   Windows PowerShell:
   ```powershell
   $env:APP_MODE = 'production'
   ```

---

## Running the service

To run the service using the virtual environment:

```powershell
.\.venv\Scripts\python app.py
```

The service will exit with code 0 and print `Service started successfully` and the configured port.

If `APP_MODE` is missing or not set to `production`, the service will raise an error and exit non-zero.

---

## Automated tests and helper script

This repository includes a convenience script `auto_test.py` that:
- Ensures `logs/` exists and creates it if necessary.
- Uses the Python interpreter inside `.venv/` to run the test suite under the correct environment.
- Ensures `APP_MODE` is set to `production` for the test run.
- Writes all test run output to `logs/test_run.log`.

Run it like this (PowerShell, from project root):

```powershell
.\.venv\Scripts\python auto_test.py
# check results
Get-Content logs\test_run.log -Tail 200
```

`auto_test.py` will return a non-zero exit code if tests fail.

---

## Files of interest

- `app.py` - small application entry point
- `config.py` - loads `settings.yaml` and expects `APP_MODE` env var
- `settings.yaml` - project settings (service port)
- `tests/*.py` - simple tests that run `app.py` and check output

---

## Notes for maintainers

- The tests expect the Python process that launches `app.py` to have `APP_MODE` set to `production`. Use the `auto_test.py` script or set `APP_MODE` manually in your shell prior to running tests.
- Keep `requirements.txt` updated if adding libraries; ensure the CI uses a clean `.venv/` environment when running the test script.

---

If you find additional tweaks or CI integration suggestions, please open an issue or submit a PR.

# Run tests and generate logs using a clean .venv
Remove-Item -Recurse -Force .venv -ErrorAction SilentlyContinue
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
# Ensure APP_MODE is set for the current session
$env:APP_MODE = 'production'
# Run the auto test runner (writes logs/test_run.log)
.\.venv\Scripts\python.exe auto_test.py
if (Test-Path logs\test_run.log) {
    Write-Output "LOG -> logs\test_run.log"
    Get-Content logs\test_run.log -Raw
} else {
    Write-Error "logs/test_run.log not found"
}

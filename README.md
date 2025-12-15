# Simple Python Service

A simple Python application that loads configuration from settings.yaml and starts a service, printing the port.

## Prerequisites

- Python 3.8+
- pip

## Installation

1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd <project-dir>
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

- Ensure `settings.yaml` exists with the service port.
- Set the environment variable `APP_MODE` to `production`.

Example settings.yaml:
```yaml
service:
  port: 9123
```

## Running the Application

Set the environment variable and run:
```bash
export APP_MODE=production
python app.py
```

Or on Windows:
```bash
set APP_MODE=production
python app.py
```

The application will print "Service started successfully" and the port.

## Testing

Run the test scripts in the tests/ directory.

For example:
```bash
python tests/case_1.py
python tests/case_2.py
python tests/case_3.py
```

Note: Tests require APP_MODE=production set.

## Project Structure

- app.py: Main application file
- config.py: Configuration loading
- settings.yaml: Configuration file
- requirements.txt: Python dependencies
- tests/: Test scripts
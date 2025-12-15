## Requirements

- Python 3.10+
- pip

---

## Quick Start

### 1. Create virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file or set the environment variable:

```bash
set APP_MODE=production
```

**Note:** The application requires:
- `APP_MODE=production` (required environment variable)
- Port is configured in `settings.yaml` (default: 9123)

### 4. Run the application

```bash
python app.py
```

The service will start successfully and display the configured port from settings.yaml.

### 5. Verify the service

You should see output similar to:
```
Service started successfully
Port: 9123
```
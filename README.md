# Chemical Equipment Parameter Visualizer (Hybrid Web + Desktop App)

Hybrid app for uploading chemical equipment CSV datasets, computing summary analytics, and visualizing results in both:
- Web UI (React + Chart.js)
- Desktop UI (PyQt5 + Matplotlib)

Backend is a shared Django + DRF API using Pandas for analytics and SQLite for storage.

## Features
- CSV upload to backend (stored + parsed server-side)
- Summary analytics API: total count, averages, equipment type distribution
- Visualization: charts + preview tables in both clients
- History management: keeps the last 5 datasets per user
- Basic authentication (HTTP Basic Auth)
- PDF report generation per dataset

## Repo Structure
- `backend/`: Django + DRF backend
- `web/`: React + Vite web frontend
- `desktop/`: PyQt5 desktop client
- `sample_equipment_data.csv`: sample CSV for demo

## Prerequisites
- Python 3.12+
- Node.js 22+

## Backend (Django + DRF)

### SQLite Database Location (D: drive)
By default, the backend stores all dataset metadata and summaries in the SQLite database at:
- `D:\chemviz.sqlite3` (when the `D:` drive exists)

To point the backend to an existing SQLite file on `D:` (or any other path), set:
- `CHEMVIZ_SQLITE_PATH` (example: `D:\path\to\your_existing.db`)

Windows PowerShell example:
```powershell
$env:CHEMVIZ_SQLITE_PATH = "D:\chemviz.sqlite3"
```

### Setup
```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py create_demo_user --username demo --password demo1234
```

### Run
```bash
cd backend
python manage.py runserver 127.0.0.1:8000
```

### Test
```bash
cd backend
python manage.py test
```

### API Endpoints
- `GET /api/me/`
- `POST /api/datasets/upload/` (multipart form-data: `file`)
- `GET /api/datasets/?limit=5`
- `GET /api/datasets/<id>/summary/`
- `GET /api/datasets/<id>/preview/?limit=50`
- `GET /api/datasets/<id>/report.pdf`

All endpoints require Basic Auth.

## Web (React + Chart.js)

### Setup
```bash
cd web
npm install
```

### Configure API Base URL (optional)
By default the web app calls `http://127.0.0.1:8000/api`.

To override:
- Windows PowerShell:
```powershell
$env:VITE_API_BASE_URL = "http://127.0.0.1:8000/api"
```

### Run
```bash
cd web
npm run dev
```

Then open the shown local URL (usually `http://localhost:5173`).

Login with:
- Username: `demo`
- Password: `demo1234`

## Desktop (PyQt5 + Matplotlib)

### Setup
```bash
pip install -r desktop/requirements.txt
```

### Run
```bash
python -m desktop.app.main
```

### Configure API Base URL (optional)
Default API URL is `http://127.0.0.1:8000/api`.

- Windows PowerShell:
```powershell
$env:CHEMVIZ_API_BASE_URL = "http://127.0.0.1:8000/api"
python -m desktop.app.main
```

## Demo Data
Use `sample_equipment_data.csv` in the repo root to test uploads from either the web or desktop app.

## Notes
- History is enforced per user: after each successful upload the backend keeps only the most recent 5 datasets.
- PDF reports are generated on demand from stored dataset metadata and summary analytics.

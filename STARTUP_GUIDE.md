# MOON AI Local Startup Guide

This guide helps you run the MOON AI backend and frontend locally.

## 1. Prerequisites

- Python 3.10+ recommended
- Node.js 18+ recommended
- npm
- Git

## 2. Backend Setup

### 2.1 Create and activate a virtual environment

Windows PowerShell:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
```

### 2.2 Install Python dependencies

```bash
pip install -r requirements.txt
```

If you add dependencies later:

```bash
pip install <package>
pip freeze > requirements.txt
```

### 2.3 Configure environment variables

Edit `backend/.env` and set at least:

```env
APP_NAME=MOON AI
HOST=127.0.0.1
PORT=8000
DEBUG=True
SECRET_KEY=change_me_to_a_long_random_secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:///./moon.db
LOG_LEVEL=INFO
```

### 2.4 Start the backend

From the `backend` directory:

```bash
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

The backend should be available at:

- http://127.0.0.1:8000/health
- http://127.0.0.1:8000/docs

## 3. Frontend Setup

### 3.1 Install Node dependencies

From the project root:

```bash
cd frontend
npm install
```

### 3.2 Configure frontend environment

Create or edit `frontend/.env.local`:

```env
VITE_API_BASE=http://127.0.0.1:8000
```

### 3.3 Start the frontend

```bash
cd frontend
npm run dev
```

Open:

- http://localhost:5173

### 3.4 Start Electron (optional)

In a second terminal:

```bash
cd frontend
npm run electron:dev
```

## 4. Login and Test the App

1. Open the frontend in the browser.
2. Go to `/login`.
3. Register or sign in.
4. Open `/chat` to test WebSocket chat.
5. Open `/console` and `/automation` to see the UI skeletons.

## 5. Useful Commands

### Backend

```bash
cd backend
python -m pytest -q
```

### Frontend

```bash
cd frontend
npm run build
npm run format
```

## 6. Troubleshooting

### Backend import issues

Run the backend from the `backend` folder so Python resolves the `app` package correctly.

### Frontend cannot reach backend

- Make sure the backend is running.
- Verify `backend/.env` has the right host/port.
- Check that CORS is allowed in the backend.
- Confirm `frontend/.env.local` points to `http://127.0.0.1:8000`.

### WebSocket connection fails

- Ensure the backend WebSocket route is running at `/ws/chat`.
- Confirm the frontend and backend use the same URL/path and token format.

## 7. Next Steps

After local startup works:

- Replace SQLite with PostgreSQL for production
- Set strong production secrets
- Add HTTPS and a reverse proxy
- Package the Electron app for Windows/macOS/Linux

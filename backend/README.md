# Moon AI Backend

MOON AI is a FastAPI backend scaffold designed for a scalable AI agent platform.

## Features

- FastAPI server with startup/shutdown lifecycle
- Environment-driven configuration
- Structured logging via Loguru
- JWT authentication with registration and user profile
- SQLite database persistence with SQLAlchemy
- REST APIs organized by feature module
- WebSocket chat endpoint for streaming-style interactions
- AI provider abstraction with OpenAI and Ollama support
- Conversation context management and prompt building
- Health check endpoint for deployment monitoring

## AI endpoints

- `POST /chat` - send a chat message and receive a full response
- `POST /chat/stream` - stream tokenized AI responses via server-sent events
- `GET /chat/models` - list available models for a provider
- `POST /chat/models/select` - change the active provider/model at runtime

## Configuration

Add or update the following values in `backend/.env`:

```text
OPENAI_API_KEY=
DEFAULT_PROVIDER=openai
DEFAULT_MODEL=gpt-4o
OLLAMA_HOST=http://localhost:11434
MAX_CONTEXT_MESSAGES=20
STREAMING_ENABLED=true
TEMPERATURE=0.7
```

## Quickstart

1. Create a virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run the application:

```powershell
python run.py
```

4. Visit the health endpoint:

```text
http://127.0.0.1:8000/health
```

## Testing

```powershell
pytest
```

## Project layout

- `app/` - application package and feature modules
- `app/core/` - configuration and logging
- `app/auth/` - authentication and security
- `app/database/` - database engine, session, and models
- `app/api/` - REST endpoint routers
- `app/websocket/` - WebSocket connection management and routes
- `app/services/` - business logic and domain services
- `app/schemas/` - request and response models
- `backend/.env` - environment configuration
- `backend/requirements.txt` - Python dependencies
- `backend/run.py` - application entrypoint

## Notes

- Update `SECRET_KEY` in `.env` before production.
- The `logs/` directory is created automatically on startup.

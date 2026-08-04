# MOON AI Project Documentation

## 1. Project Overview

MOON AI is a full-stack AI agent platform designed to evolve from a local development prototype into a production-ready assistant for chat, automation, memory, plugins, voice interaction, and agent orchestration.

The system combines:
- A FastAPI backend for APIs, authentication, AI services, memory, commands, plugins, automation, voice, and agent coordination.
- A React + Vite + TypeScript frontend for the desktop/web experience.
- A modular architecture so new capabilities can be added without rewriting the application.

The project was built in phases so each layer could be tested and extended independently.

---

## 2. Goals of the Project

The original goal was to build a scalable AI agent platform that can:
- Start a FastAPI server
- Load configuration from environment variables
- Log application events
- Authenticate users with JWT
- Expose REST APIs
- Support WebSocket communication
- Return health and status data
- Host reusable AI and automation modules
- Support voice interaction and agent-style task execution

---

## 3. High-Level Architecture

```text
User
 │
 ▼
Frontend (React + Vite + Electron)
 │
 ▼
FastAPI Backend
 │
 ├── Auth Layer
 ├── API Layer
 ├── AI Layer
 ├── Memory Layer
 ├── Command Engine
 ├── Plugin Framework
 ├── Automation Layer
 ├── Voice Layer
 └── Agent Orchestration Layer
 │
 ▼
Storage and Services
 ├── SQLite (default local DB)
 ├── Optional PostgreSQL (production)
 ├── Optional Redis (cache / sessions / jobs)
 └── Optional Chroma / vector storage
```

---

## 4. Tech Stack

### Backend
- Python 3.11+
- FastAPI
- Uvicorn
- Pydantic + Pydantic Settings
- SQLAlchemy
- python-jose for JWT
- passlib + bcrypt for password hashing
- python-dotenv for environment loading
- loguru for structured logging
- websockets for WebSocket support
- pytest for backend testing

### Frontend
- React
- TypeScript
- Vite
- Tailwind CSS
- Zustand for state
- React Router
- React Query
- Framer Motion
- Electron (desktop packaging path)

### DevOps / Deployment
- Docker / Docker Compose
- Nginx (web deployment proxy)
- Environment-based configuration
- Optional Redis / PostgreSQL integration for production

---

## 5. Project Structure

```text
moon-ai/
├── backend/
│   ├── app/
│   │   ├── ai/
│   │   ├── agent/
│   │   ├── api/
│   │   ├── auth/
│   │   ├── automation/
│   │   ├── commands/
│   │   ├── core/
│   │   ├── database/
│   │   ├── memory/
│   │   ├── models/
│   │   ├── plugins/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── utils/
│   │   ├── voice/
│   │   ├── websocket/
│   │   ├── main.py
│   │   └── __init__.py
│   ├── tests/
│   ├── .env
│   ├── requirements.txt
│   ├── run.py
│   └── README.md
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   ├── assets/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── layouts/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── store/
│   │   ├── styles/
│   │   ├── types/
│   │   ├── utils/
│   │   └── electron/
│   ├── package.json
│   ├── vite.config.ts
│   └── nginx/
├── docker-compose.yml
├── STARTUP_GUIDE.md
└── PROJECT_DOCUMENTATION.md
```

---

## 6. Step-by-Step Development Process

### Step 1: Create the project skeleton
The project started with the basic folder structure:
- `backend/app` with functional domains
- `backend/tests` for regression coverage
- `frontend/src` for UI modules

This made the codebase modular from the beginning and separated responsibilities clearly.

### Step 2: Set up the backend foundation
The first backend milestone was to create:
- a FastAPI app
- health endpoints
- configuration loading from `.env`
- logging
- database initialization
- WebSocket scaffolding

This created a stable base for all other features.

### Step 3: Add authentication
We implemented:
- user registration
- user login
- access token generation
- current user retrieval
- password hashing

This allowed the app to protect resources and prepare for multi-user operation.

### Step 4: Add the database layer
A SQLAlchemy-backed database layer was introduced so the app could store:
- users
- conversations
- messages
- memory entries

This created the persistence layer necessary for AI memory and user interactions.

### Step 5: Build the AI layer
The AI layer was designed as a modular service so the app could later support multiple providers, including:
- OpenAI-compatible APIs
- local models
- future provider adapters

The design keeps provider-specific logic isolated so the frontend and app logic do not depend directly on one provider.

### Step 6: Add memory management
The memory subsystem was added to store and retrieve conversation context and knowledge. This helps the agent behave more like a workspace assistant by remembering relevant information across sessions.

### Step 7: Create command and automation engines
We introduced a command system to represent actionable operations such as:
- opening an app
- browsing a URL
- reading or writing files
- running system checks

This allowed the agent to execute structured tasks instead of only respond with text.

### Step 8: Add plugin architecture
A plugin framework was built to let features extend the app without modifying the core code.

Key plugin capabilities:
- plugin discovery
- plugin loading
- lifecycle handling
- command registration from plugins
- config loading from plugin config files
- lifecycle event notifications

This makes MOON AI extensible and future-proof.

### Step 9: Add voice capabilities
The voice layer was planned as a separate module so the platform could later support:
- wake word detection
- speech-to-text
- text-to-speech
- interruption handling
- streaming audio conversations

This phase prepares the app for hands-free interaction.

### Step 10: Add agent orchestration
The agent layer was built to coordinate goals, tasks, execution, retries, and evaluation. Instead of treating user input as only a command, the system can reason about higher-level objectives and decompose them into smaller steps.

### Step 11: Build the frontend
The frontend was created using React, TypeScript, Tailwind, and Vite.

We built:
- a shared layout
- reusable UI components
- authentication UI
- chat experience
- command console
- automation and plugin views
- settings pages

The frontend connects to the backend through REST APIs and WebSocket routes.

### Step 12: Connect backend and frontend
We wired the UI to:
- auth endpoints
- chat endpoints
- health status
- plugin management APIs
- WebSocket real-time communication

This made the app usable as a connected full-stack experience.

### Step 13: Prepare for deployment
The app was prepared for deployment through:
- environment-based configuration
- CORS settings
- frontend proxying for local development
- Docker assets
- Nginx routing for web deployment
- startup documentation

---

## 7. Backend Design Details

### API Layer
The backend exposes separate routers for:
- health
- auth
- chat
- commands
- memory
- plugins
- voice
- agent
- automation

Each router is kept focused on one domain, which makes the backend easier to maintain.

### Authentication Layer
Authentication is handled by:
- password hashing
- token generation
- token decoding
- dependency-based current-user extraction

### Database Layer
The database layer uses SQLAlchemy models for:
- users
- conversations
- messages
- memory

This gives the system persistence for runtime state and long-term memory.

### Plugin Layer
The plugin layer is modular:
- plugin discovery finds plugin directories
- plugin loader imports plugin modules
- plugin manager handles lifecycle
- plugin commands register with the command registry
- plugin events can be subscribed to through the event bus

### Agent Layer
The agent layer coordinates goals and execution steps and is designed to expand into more advanced reasoning workflows over time.

---

## 8. Frontend Design Details

### Main UI Areas
The frontend contains views for:
- dashboard
- chat
- memory
- automation
- plugins
- files
- settings

### State Management
The frontend uses Zustand for app state and a service layer for API and WebSocket access.

### Design System
The UI is organized around reusable components such as:
- button
- input
- textarea
- card
- modal
- sidebar
- top bar
- toast
- badge
- loader

---

## 9. Runtime Flow

### Typical User Flow
1. The user opens the frontend.
2. The frontend connects to the backend.
3. The user logs in or registers.
4. The user sends a prompt or command.
5. The backend routes the request to the appropriate service.
6. The AI or command engine processes the request.
7. The result is returned to the UI.
8. If needed, the system stores memories or triggers automation tasks.

### Plugin Flow
1. The backend discovers plugin directories.
2. The plugin loader imports the plugin module.
3. The plugin registers commands and events.
4. The command registry exposes the plugin commands to the application.
5. The plugin can later be enabled, disabled, reloaded, or unloaded.

---

## 10. How to Run the Project Locally

### Backend
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt
python run.py
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Environment
Create and fill `backend/.env` with values such as:
- `SECRET_KEY`
- `DATABASE_URL`
- `OPENAI_API_KEY` (optional but recommended for AI features)
- `CORS_ORIGINS`
- `HOST` and `PORT`

---

## 11. How to Use the Agent

After startup:
1. Open the frontend UI.
2. Register or log in.
3. Use chat to interact with the bot.
4. Use the command console for structured tasks.
5. Visit plugin and automation sections to explore extensibility.
6. Use the agent and voice modules as they are expanded further.

---

## 12. What Is Already Completed

The current project already includes:
- backend structure and modular architecture
- FastAPI app initialization
- auth flow
- health endpoint
- chat and AI scaffolding
- memory module
- command engine
- plugin system
- automation scaffold
- voice scaffold
- agent orchestration scaffold
- frontend UI foundation
- backend/frontend integration
- deployment assets and docs

---

## 13. What Still Needs Work for Full Production

To move from a strong prototype to a polished production deployment, the next major steps are:
- add real production security hardening
- add Redis integration
- add PostgreSQL migration tooling
- add background job workers
- add monitoring and metrics dashboards
- add audit logging and better admin APIs
- complete end-to-end testing in staging and production environments
- deploy behind HTTPS with proper secrets management

---

## 14. Recommended Next Steps

1. Add production-ready security middleware and RBAC.
2. Add Redis-backed caching and job queues.
3. Move to PostgreSQL for production data storage.
4. Add admin and monitoring APIs.
5. Package the frontend as a production Electron app.
6. Add CI/CD deployment pipelines.
7. Harden deployment with HTTPS, backups, and monitoring.

---

## 15. Summary

MOON AI was built as a modular, layered platform that started with a simple FastAPI backend and grew into a multi-domain AI agent system. The architecture emphasizes separation of concerns, extensibility, and future readiness.

The project is now at a strong foundation stage:
- backend services are implemented
- frontend UI is scaffolded and connected
- plugin and agent systems are present
- deployment assets and documentation are included

With a few more production-focused steps, this can become a robust web and desktop AI product.

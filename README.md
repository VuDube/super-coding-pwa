# super-coding-pwa

Super Coding CLI as a PWA — Hybrid web app (PWA frontend) + FastAPI backend.
Goal: a zero-cost-first, multi-provider LLM router for coding workflows, with GitHub integrations and CI.

Quick highlights:
- Frontend: Vite + React, installable PWA, Monaco-ready (editor can be added).
- Backend: FastAPI with provider adapters (OpenRouter, Hugging Face, Ollama, generic).
- Model router: preference order, failover, quota tracker.
- CI: GitHub Actions builds and runs smoke checks for frontend and backend.
- Security: backend reads API keys from environment or config.yaml; never embed keys in the frontend.

Getting started (exact commands are below this file list).

Configure:
- Copy `backend/config.yaml.example` to `backend/config.yaml` or set env vars in GitHub Secrets.
- Set secrets for API keys: OPENROUTER_API_KEY, HUGGINGFACE_API_KEY, TOGETHER_API_KEY (optional).

Run locally:
- Start backend: `cd backend && .venv/bin/activate && uvicorn main:app --reload --port 8000`
- Start frontend: `cd web-frontend && npm install && npm run dev`
- Open the web app (usually at http://localhost:5173) and use the chat UI.

CI:
- On push, GitHub Actions will install Python & Node, install dependencies, run tests, and build the frontend.

Notes:
- For zero-cost-first behavior, install and run Ollama locally and configure the Ollama model name in `backend/config.yaml` (see example).
- Many provider endpoints require tokens and may have rate limits or quotas — use the QuotaTracker to block providers if needed.

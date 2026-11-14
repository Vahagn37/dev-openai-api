# FastAPI + OpenAI

Minimal FastAPI app that calls OpenAI Chat Completions.

## Setup

```bash
cd openai
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` and set your `OPENAI_API_KEY`.

## Run

From the `openai` directory:

```bash
uvicorn app.main:app --reload
```

API docs: http://127.0.0.1:8000/docs

## Example

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}'
```

Optional system prompt:

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "system": "You are a helpful assistant."}'
```

## Endpoints

| Method | Path     | Description              |
|--------|----------|--------------------------|
| GET    | `/health`| Health check             |
| POST   | `/chat`  | Chat with OpenAI         |

## Deploy on Render

1. Push this repo (`openai/`) to GitHub.
2. In [Render Dashboard](https://dashboard.render.com) → **New** → **Blueprint**.
3. Connect the GitHub repo (Render will read `render.yaml`).
4. When prompted, set the secret `OPENAI_API_KEY` to your real key.
5. Deploy. Your API will be at `https://<service-name>.onrender.com`.

**Manual alternative** (New → Web Service):

| Setting | Value |
|---------|--------|
| Root Directory | *(leave empty if this folder is the repo root)* |
| Runtime | Python |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
| Health Check Path | `/health` |

Add env vars: `OPENAI_API_KEY` (secret), `OPENAI_MODEL=gpt-4o-mini`, `PYTHON_VERSION=3.12.8`.

Test after deploy:

```bash
curl https://<your-service>.onrender.com/health
curl -X POST https://<your-service>.onrender.com/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}'
```

Free-tier services sleep after inactivity; the first request after sleep can take ~30–60s.

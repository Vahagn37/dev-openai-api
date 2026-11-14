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

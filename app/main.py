from fastapi import FastAPI, HTTPException
from openai import APIError, AuthenticationError, OpenAIError
from pydantic import BaseModel, Field

from app.config import get_settings
from app.openai_client import get_openai_client

app = FastAPI(title="FastAPI + OpenAI", version="0.1.0")


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    system: str | None = None


class ChatResponse(BaseModel):
    reply: str


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
async def chat(body: ChatRequest) -> ChatResponse:
    settings = get_settings()
    if not settings.openai_api_key or settings.openai_api_key.startswith("sk-your-"):
        raise HTTPException(
            status_code=500,
            detail="OPENAI_API_KEY is not configured. Copy .env.example to .env and set your key.",
        )

    messages: list[dict[str, str]] = []
    if body.system:
        messages.append({"role": "system", "content": body.system})
    messages.append({"role": "user", "content": body.message})

    try:
        client = get_openai_client()
        completion = await client.chat.completions.create(
            model=settings.openai_model,
            messages=messages,
        )
    except AuthenticationError as exc:
        raise HTTPException(status_code=401, detail="Invalid OpenAI API key.") from exc
    except APIError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"OpenAI API error: {exc.message}",
        ) from exc
    except OpenAIError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    reply = completion.choices[0].message.content
    if not reply:
        raise HTTPException(status_code=502, detail="OpenAI returned an empty response.")

    return ChatResponse(reply=reply)

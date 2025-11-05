from fastapi import FastAPI, HTTPException
import os
from model_router import ModelRouter

app = FastAPI(title="Super Coding Backend")

# Cloudflare Worker environment-based configuration
config = {
    "preference": ["ollama", "huggingface", "openrouter"],
    "providers": {}
}

# Configure providers based on environment variables
if OPENROUTER_API_KEY := os.getenv("OPENROUTER_API_KEY"):
    config["providers"]["openrouter"] = {
        "api_key": OPENROUTER_API_KEY,
        "default_model": "meta-llama-3-8b-instruct",
        "endpoint": "https://openrouter.ai/api/v1/chat/completions"
    }

if HUGGINGFACE_API_KEY := os.getenv("HUGGINGFACE_API_KEY"):
    config["providers"]["huggingface"] = {
        "api_key": HUGGINGFACE_API_KEY
    }

router = ModelRouter(config)

@app.post("/api/chat")
async def chat_endpoint(payload: dict):
    prompt = payload.get("prompt")
    if not prompt:
        raise HTTPException(status_code=400, detail="prompt required")
    
    provider = payload.get("provider")
    model = payload.get("model")
    system = payload.get("system")
    
    try:
        resp = router.chat(prompt=prompt, provider_hint=provider, model=model, system=system)
        return {
            "ok": True,
            "response": resp,
            "cache-control": "no-store",
            "content-type": "application/json"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "timestamp": "2025-11-05T16:24:09Z",
        "cache-control": "no-store"
    }

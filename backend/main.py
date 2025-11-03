from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import yaml
from pathlib import Path
from model_router import ModelRouter
import os

app = FastAPI(title="Super Coding Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load config from backend/config.yaml if present, else use env-driven minimal config
CONFIG_PATH = Path(__file__).parent / "config.yaml"
if CONFIG_PATH.exists():
    with open(CONFIG_PATH, "r") as f:
        config = yaml.safe_load(f) or {}
else:
    # minimal fallback: read env variables into config
    config = {"preference": ["ollama", "huggingface", "openrouter"], "providers": {}}
    if os.getenv("OPENROUTER_API_KEY"):
        config["providers"]["openrouter"] = {"api_key": os.getenv("OPENROUTER_API_KEY")}
    if os.getenv("HUGGINGFACE_API_KEY"):
        config["providers"]["huggingface"] = {"api_key": os.getenv("HUGGINGFACE_API_KEY")}
    if os.getenv("OLLAMA_BASE"):
        config["providers"]["ollama"] = {"base": os.getenv("OLLAMA_BASE")}

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
        return {"ok": True, "response": resp}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
def health():
    return {"status": "ok"}

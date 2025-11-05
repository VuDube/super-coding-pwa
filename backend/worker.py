from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from model_router import ModelRouter

app = FastAPI(title="Super Coding Backend")

# Configure CORS for development
if os.getenv("ENVIRONMENT") != "production":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Initialize config from environment
config = {
    "preference": ["huggingface", "openrouter"],
    "providers": {}
}

if api_key := os.getenv("OPENROUTER_API_KEY"):
    config["providers"]["openrouter"] = {
        "api_key": api_key,
        "default_model": "meta-llama-3-8b-instruct"
    }

if api_key := os.getenv("HUGGINGFACE_API_KEY"):
    config["providers"]["huggingface"] = {
        "api_key": api_key
    }

router = ModelRouter(config)

@app.post("/api/chat")
async def chat_endpoint(payload: dict):
    if not payload.get("prompt"):
        raise HTTPException(status_code=400, detail="prompt required")
    
    try:
        response = router.chat(
            prompt=payload["prompt"],
            provider_hint=payload.get("provider"),
            model=payload.get("model"),
            system=payload.get("system")
        )
        
        return {
            "ok": True,
            "response": response,
            "headers": {
                "Cache-Control": "no-store",
                "Content-Type": "application/json"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health():
    return {
        "status": "ok",
        "version": "2025.11.05",
        "environment": os.getenv("ENVIRONMENT", "development")
    }

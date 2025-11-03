import httpx
from typing import Dict

class OllamaProvider:
    def __init__(self, cfg: Dict):
        self.cfg = cfg or {}
        self.base = self.cfg.get("base", "http://localhost:11434")
        self.default_model = self.cfg.get("default_model")
    def chat(self, prompt: str, model: str = None, system_prompt: str = None, timeout: int = 60):
        model = model or self.default_model
        if not model:
            raise RuntimeError("Ollama provider requires a model name (downloaded locally)")
        url = f"{self.base}/api/chat"
        payload = {"model": model, "messages": [{"role": "user", "content": prompt}]}
        r = httpx.post(url, json=payload, timeout=timeout)
        r.raise_for_status()
        return r.json().get("choices", [{}])[0].get("message", {}).get("content", "")

import httpx
from typing import Dict

class OpenRouterProvider:
    def __init__(self, cfg: Dict):
        self.api_key = cfg.get("api_key")
        self.default_model = cfg.get("default_model", "meta-llama-3-8b-instruct")
        self.endpoint = cfg.get("endpoint", "https://openrouter.ai/api/v1/chat/completions")
    def chat(self, prompt: str, model: str = None, system_prompt: str = None, timeout: int = 60):
        if not self.api_key:
            raise RuntimeError("OpenRouter api_key not configured")
        model = model or self.default_model
        system_prompt = system_prompt or "You are a helpful coding assistant."
        headers = {"Authorization": f"Bearer {self.api_key}"}
        data = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        }
        r = httpx.post(self.endpoint, headers=headers, json=data, timeout=timeout)
        r.raise_for_status()
        j = r.json()
        return j["choices"][0]["message"]["content"]

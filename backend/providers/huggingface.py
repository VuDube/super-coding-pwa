import httpx
from typing import Dict

class HuggingFaceProvider:
    def __init__(self, cfg: Dict):
        self.api_key = cfg.get("api_key")
        self.default_model = cfg.get("default_model", "bigcode/starcoder")
        self.base = cfg.get("base", "https://api-inference.huggingface.co/models")
    def chat(self, prompt: str, model: str = None, system_prompt: str = None, timeout: int = 60):
        model = model or self.default_model
        if not self.api_key:
            raise RuntimeError("HuggingFace api_key not configured")
        url = f"{self.base}/{model}"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {"inputs": prompt, "options": {"use_cache": False}}
        r = httpx.post(url, headers=headers, json=payload, timeout=timeout)
        r.raise_for_status()
        res = r.json()
        if isinstance(res, list):
            return res[0].get("generated_text", "") or str(res)
        if isinstance(res, dict):
            return res.get("generated_text") or str(res)
        return str(res)

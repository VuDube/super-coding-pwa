import httpx
from typing import Dict

class GenericRESTProvider:
    def __init__(self, cfg: Dict):
        self.cfg = cfg or {}
        self.endpoint = self.cfg.get("endpoint")
        self.api_key = self.cfg.get("api_key")
        self.default_model = self.cfg.get("default_model")
        self.extra_headers = self.cfg.get("headers", {})
    def chat(self, prompt: str, model: str = None, system_prompt: str = None, timeout: int = 60):
        if not self.endpoint:
            raise RuntimeError("Generic provider missing endpoint in config")
        model = model or self.default_model
        headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
        headers.update(self.extra_headers)
        payload = {"model": model, "prompt": prompt}
        r = httpx.post(self.endpoint, headers=headers, json=payload, timeout=timeout)
        r.raise_for_status()
        return r.text

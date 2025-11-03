from providers import get_provider
from quota_tracker import QuotaTracker
from rich import print
import traceback

class ModelRouter:
    def __init__(self, cfg):
        self.cfg = cfg or {}
        self.providers_cfg = self.cfg.get("providers", {})
        self.preference = self.cfg.get("preference", list(self.providers_cfg.keys()) or ["ollama","huggingface","openrouter"])
        self.quota = QuotaTracker("usage.json")
    def chat(self, prompt: str, provider_hint: str = None, model: str = None, system: str = None):
        order = [provider_hint] if provider_hint else self.preference
        seen = set()
        candidates = []
        for p in order:
            if p and p not in seen:
                candidates.append(p)
                seen.add(p)
        # append configured providers not in preference
        for p in self.providers_cfg.keys():
            if p not in seen:
                candidates.append(p)
                seen.add(p)
        last_exc = None
        for provider_name in candidates:
            try:
                prov_cfg = self.providers_cfg.get(provider_name, {})
                provider_obj = get_provider(provider_name, self.providers_cfg)
                if not self.quota.can_use(provider_name):
                    print(f"[yellow]Provider {provider_name} blocked by quota tracker[/yellow]")
                    continue
                resp = provider_obj.chat(prompt=prompt, model=model, system_prompt=system)
                self.quota.record(provider_name, len(resp or ""))
                return resp
            except Exception as e:
                last_exc = e
                print(f"[yellow]Provider {provider_name} failed, trying next. Error: {e}[/yellow]")
                traceback.print_exc()
                continue
        raise RuntimeError(f"All providers failed. Last error: {last_exc}")

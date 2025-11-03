import json
from pathlib import Path
from datetime import datetime, timezone

class QuotaTracker:
    def __init__(self, filename="usage.json"):
        self.path = Path(filename)
        if not self.path.exists():
            self._data = {"providers": {}}
            self._save()
        else:
            self._data = json.loads(self.path.read_text())
    def _save(self):
        self.path.write_text(json.dumps(self._data, indent=2))
    def can_use(self, provider_name):
        p = self._data["providers"].get(provider_name, {})
        blocked = p.get("blocked", False)
        return not blocked
    def record(self, provider_name, token_count):
        now = datetime.now(timezone.utc).isoformat()
        p = self._data["providers"].setdefault(provider_name, {})
        p["last_used"] = now
        p["usage_tokens"] = p.get("usage_tokens", 0) + int(token_count or 0)
        self._save()
    def block_provider(self, provider_name):
        p = self._data["providers"].setdefault(provider_name, {})
        p["blocked"] = True
        self._save()
    def unblock_provider(self, provider_name):
        p = self._data["providers"].setdefault(provider_name, {})
        p["blocked"] = False
        self._save()

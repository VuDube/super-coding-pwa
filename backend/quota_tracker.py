from datetime import datetime, timezone
import json

class QuotaTracker:
    def __init__(self, kv_namespace=None):
        self.kv = kv_namespace
        self._data = {"providers": {}}
    
    async def _load(self):
        if self.kv:
            stored_data = await self.kv.get("quota_data")
            if stored_data:
                self._data = json.loads(stored_data)
            else:
                self._data = {"providers": {}}
    
    async def _save(self):
        if self.kv:
            await self.kv.put("quota_data", json.dumps(self._data))
    
    async def can_use(self, provider_name):
        await self._load()
        p = self._data["providers"].get(provider_name, {})
        blocked = p.get("blocked", False)
        return not blocked
    
    async def record(self, provider_name, token_count):
        await self._load()
        now = datetime.now(timezone.utc).isoformat()
        p = self._data["providers"].setdefault(provider_name, {})
        p["last_used"] = now
        p["usage_tokens"] = p.get("usage_tokens", 0) + int(token_count or 0)
        await self._save()
    
    async def block_provider(self, provider_name):
        await self._load()
        p = self._data["providers"].setdefault(provider_name, {})
        p["blocked"] = True
        await self._save()

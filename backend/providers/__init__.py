from .openrouter import OpenRouterProvider
from .huggingface import HuggingFaceProvider
from .generic_rest import GenericRESTProvider
from .ollama import OllamaProvider

def get_provider(name: str, cfg: dict):
    name = name.lower()
    providers_cfg = cfg
    if name == "openrouter":
        return OpenRouterProvider(providers_cfg.get("openrouter", {}))
    if name == "huggingface":
        return HuggingFaceProvider(providers_cfg.get("huggingface", {}))
    if name == "ollama":
        return OllamaProvider(providers_cfg.get("ollama", {}))
    # generic fallback uses provider config keyed by name
    return GenericRESTProvider(providers_cfg.get(name, {}))

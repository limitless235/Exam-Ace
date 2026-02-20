"""
LLM Gateway — provider abstraction with timeout, retry, and health check.
Supports: OpenAI, Mistral, Local (LM Studio / Ollama / vLLM — OpenAI-compatible).
"""
from __future__ import annotations

import logging
from abc import ABC, abstractmethod

import httpx

logger = logging.getLogger(__name__)

_TIMEOUT = 120.0  # seconds — local models are slower
_HEALTH_TIMEOUT = 3.0  # seconds — quick connectivity check


class LLMProvider(ABC):
    """Base class for LLM providers."""

    @abstractmethod
    async def generate(self, system_prompt: str, user_prompt: str, temperature: float) -> str:
        """Send a chat completion request and return the raw text response."""
        ...

    async def check_health(self) -> bool:
        """Return True if the provider endpoint is reachable."""
        return True  # cloud providers assumed always up


class OpenAIProvider(LLMProvider):
    def __init__(self, api_key: str, model: str = "gpt-4o-mini", base_url: str = "https://api.openai.com/v1"):
        self.api_key = api_key
        self.model = model
        self.base_url = base_url.rstrip("/")

    async def generate(self, system_prompt: str, user_prompt: str, temperature: float) -> str:
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": temperature,
        }
        async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
            resp = await client.post(url, json=payload, headers=headers)
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"]


class MistralProvider(LLMProvider):
    def __init__(self, api_key: str, model: str = "mistral-medium-latest", base_url: str = "https://api.mistral.ai/v1"):
        self.api_key = api_key
        self.model = model
        self.base_url = base_url.rstrip("/")

    async def generate(self, system_prompt: str, user_prompt: str, temperature: float) -> str:
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": temperature,
        }
        async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
            resp = await client.post(url, json=payload, headers=headers)
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"]


class LocalProvider(LLMProvider):
    """
    OpenAI-compatible local endpoint.
    Default: LM Studio at http://localhost:1234/v1
    Also works with Ollama, vLLM, etc.
    """

    def __init__(
        self,
        model: str = "phi-3-mini-4k-instruct",
        base_url: str = "http://localhost:1234/v1",
        api_key: str = "not-needed",
        health_timeout: float = _HEALTH_TIMEOUT,
    ):
        self.api_key = api_key
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.health_timeout = health_timeout

    async def check_health(self) -> bool:
        """Ping the LM Studio /models endpoint to see if it's reachable."""
        try:
            async with httpx.AsyncClient(timeout=self.health_timeout) as client:
                resp = await client.get(f"{self.base_url}/models")
                return resp.status_code == 200
        except (httpx.ConnectError, httpx.TimeoutException, httpx.HTTPError) as exc:
            logger.warning("Local LLM health check failed: %s", exc)
            return False

    async def generate(self, system_prompt: str, user_prompt: str, temperature: float) -> str:
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": temperature,
        }
        async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
            resp = await client.post(url, json=payload, headers=headers)
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"]


def get_provider(provider_name: str, api_key: str, base_url: str = "", model: str = "", health_timeout: int = 3) -> LLMProvider:
    """Factory — returns the correct provider based on config."""
    name = provider_name.lower()
    if name == "openai":
        return OpenAIProvider(
            api_key=api_key,
            model=model or "gpt-4o-mini",
            base_url=base_url or "https://api.openai.com/v1",
        )
    elif name == "mistral":
        return MistralProvider(
            api_key=api_key,
            model=model or "mistral-medium-latest",
            base_url=base_url or "https://api.mistral.ai/v1",
        )
    elif name == "local":
        return LocalProvider(
            model=model or "phi-3-mini-4k-instruct",
            base_url=base_url or "http://localhost:1234/v1",
            api_key=api_key,
            health_timeout=float(health_timeout),
        )
    else:
        raise ValueError(f"Unknown LLM provider: {provider_name!r}. Must be 'openai', 'mistral', or 'local'.")

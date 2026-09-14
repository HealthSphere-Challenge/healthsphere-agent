from typing import Protocol

import httpx


class LLMClient(Protocol):
    provider_name: str
    model_name: str

    async def generate(self, system: str, user: str) -> str: ...


class OpenAICompatibleClient:
    provider_name = "openai-compatible"

    def __init__(self, base_url: str, api_key: str, model_name: str, timeout: float):
        self.base_url, self.api_key, self.model_name, self.timeout = (
            base_url.rstrip("/"),
            api_key,
            model_name,
            timeout,
        )

    async def generate(self, system: str, user: str) -> str:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": self.model_name,
                    "temperature": 0,
                    "max_tokens": 500,
                    "messages": [
                        {"role": "system", "content": system},
                        {"role": "user", "content": user},
                    ],
                },
            )
            response.raise_for_status()
            data = response.json()
        return str(data["choices"][0]["message"]["content"]).strip()

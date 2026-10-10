from openai import OpenAI

from app.config import Config


class LLMClient:
    """Thin wrapper over any OpenAI-compatible chat completion endpoint."""

    def __init__(self, api_key: str = Config.LLM_API_KEY,
                 base_url: str = Config.LLM_BASE_URL, model: str = Config.LLM_MODEL):
        if not api_key:
            raise RuntimeError("LLM_API_KEY is not set. Copy .env.example to .env and fill it in.")
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model

    def chat(self, messages: list[dict]) -> str:
        response = self.client.chat.completions.create(
            model=self.model, messages=messages, temperature=0.2, stream=False
        )
        return response.choices[0].message.content

from pathlib import Path

from pydantic import AnyHttpUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="AGENT_", extra="ignore")

    internal_token: str = Field(min_length=24)
    index_path: Path = Path("artifacts/medquad-index-v1/index.json")
    llm_base_url: AnyHttpUrl = AnyHttpUrl("https://api.openai.com/v1")
    llm_api_key: str = Field(min_length=1)
    llm_model: str = Field(default="replace-with-approved-model", min_length=1)
    llm_timeout_seconds: float = Field(default=20, gt=0, le=25)

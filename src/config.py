from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
  LLM_API_KEY: str = Field(default=...)
  LLM_BASE_URL: str = Field(default=...)
  LLM_MODEL_NAME: str = Field(default=...)
  SENDGRID_API_KEY: str = Field(default=...)
  SENDER_EMAIL_ADDRESS: str = Field(default=...)

  model_config = SettingsConfigDict(env_file=".env")

@lru_cache(maxsize=1)
def get_settings() -> Settings:
  return Settings()

settings = get_settings()

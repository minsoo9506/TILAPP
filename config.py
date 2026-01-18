import os
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

def get_env_file() -> str:
    env = os.getenv("ENV", "dev")
    return f".env.{env}"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=get_env_file(), env_file_encoding="utf-8")
    database_username: str
    database_password: str
    jwt_secret: str

@lru_cache()  # 함수 인자가 없어서 싱글톤 패턴으로 동작
def get_settings() -> Settings:
    return Settings()  # type: ignore
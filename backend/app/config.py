from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    ncbi_email: str = "biolink@example.com"
    ncbi_api_key: str = ""
    ncbi_tool: str = "biolink"
    ncbi_timeout: float = 30.0
    host: str = "0.0.0.0"
    port: int = 8000
    cors_origins: str = ""
    max_query_len: int = 500
    max_fasta_bytes: int = 2_000_000
    rate_limit_per_minute: int = 60
    enable_docs: bool = False
    serve_frontend: bool = True
    frontend_dir: str = ""
    log_level: str = "INFO"

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @property
    def frontend_path(self) -> Path:
        if self.frontend_dir:
            return Path(self.frontend_dir).resolve()
        return Path(__file__).resolve().parents[2] / "frontend"


@lru_cache
def get_settings() -> Settings:
    return Settings()

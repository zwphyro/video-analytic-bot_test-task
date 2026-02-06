import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_name: str = Field(..., alias="POSTGRES_DB")
    db_host: str = Field(..., alias="POSTGRES_HOST")
    db_port: int = Field(..., alias="POSTGRES_PORT")
    db_user: str = Field(..., alias="POSTGRES_USER")
    db_password: str = Field(..., alias="POSTGRES_PASSWORD")

    openai_api_key: str = Field(..., alias="OPENAI_API_KEY")
    tg_bot_token: str = Field(..., alias="TG_BOT_TOKEN")

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", ".env"),
        extra="ignore",
    )

    @property
    def db_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


settings = Settings()  # type: ignore[no-call-issue]

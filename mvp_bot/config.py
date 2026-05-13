from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator


class Settings(BaseSettings):    
    # ============= Bot Settings =============
    bot_token: str = Field(
        ...,
        description="Telegram Bot Token",
        alias="BOT_TOKEN"
    )
    bot_admin_ids: list[str] = Field(
        default_factory=list,
        description="List of admin Telegram IDs",
        alias="BOT_ADMIN_IDS"
    )
    bot_webhook_url: str | None = Field(
        default=None, 
        description="Webhook URL for production",
        alias="BOT_WEBHOOK_URL"
    )
    
    # ============= Database Settings =============
    database_url: str = Field(
        ..., 
        description="PostgreSQL connection URL",
        alias="DB_DATABASE_URL"
    )
    db_pool_size: int = Field(default=10, ge=1, le=100, alias="DB_POOL_SIZE")
    db_pool_timeout: int = Field(default=30, ge=1, alias="DB_POOL_TIMEOUT")
    
    # ============= App Settings =============
    environment: str = Field(default="development", alias="APP_ENVIRONMENT")
    debug: bool = Field(default=False, alias="APP_DEBUG")
    data_dir: str = Field(default="data", alias="APP_DATA_DIR")
    log_level: str = Field(default="INFO", alias="APP_LOG_LEVEL")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        # Разрешает использовать и alias, и имя поля
        populate_by_name=True
    )

    # Валидатор для admin_ids
    @field_validator("bot_admin_ids", mode="before")
    @classmethod
    def parse_admin_ids(cls, value):
        if isinstance(value, str):
            return [id.strip() for id in value.split(",") if id.strip()]
        return value if value else []


# Глобальный экземпляр настроек
settings = Settings()

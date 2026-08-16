from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    database_path: str = "data/db_data.db"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )


settings = Settings()
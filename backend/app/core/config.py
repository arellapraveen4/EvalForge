from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "EvalForge"
    database_url: str = "sqlite:///./evalforge.db"
    jwt_secret: str = "change-this-secret"
    jwt_algorithm: str = "HS256"
    access_token_minutes: int = 720
    llm_provider: str = "gemini"
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"
    openai_api_key: str = ""
    openai_base_url: str = "https://api.openai.com/v1"
    openai_model: str = "gpt-4o-mini"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()

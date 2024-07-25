from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    TITLE: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: int
    DB_PORT: int
    DB_HOST: str
    DB_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    model_config = SettingsConfigDict(env_file=".env")

# Load environment variables
from pydantic_settings import BaseSettings
from typing import Optional
print("----------Load environment variables-------------")


class Settings(BaseSettings):
    # Database settings
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str

    # Construct database URL
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "CLEM"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    api_key: str
    redis_url: str = "redis://localhost:6379"
    weather_api_base_url: str = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"

    class Config:
        env_file = ".env"

settings = Settings()

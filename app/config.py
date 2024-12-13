from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGODB_URL: str
    REDIS_URL: str
    NEWS_DB: str
    
    NEWS_SOURCES: dict = {
        "udn": "https://udn.com/news/story/7470/7645646",
        "chinatimes": "https://www.chinatimes.com",
        "bbc": "https://www.bbc.com"
    }

    class Config:
        env_file = ".env"

settings = Settings()
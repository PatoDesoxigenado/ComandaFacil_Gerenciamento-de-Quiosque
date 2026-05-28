from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    APP_ENV: str = "development"
    APP_DEBUG: bool = True
    APP_BASE_DOMAIN: str = "localhost"
    
    # Banco de Escrita (Postgres)
    DATABASE_URL: str
    
    # Banco de Leitura (MongoDB) que adicionamos para os Relatórios
    MONGO_URL: str = "mongodb://localhost:27017/comanda_facil_leitura"
    
    REDIS_URL: str = "redis://localhost:6379/0"
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

@lru_cache
def get_settings() -> Settings:
    return Settings()
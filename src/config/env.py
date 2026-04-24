import os

from src.config.base_settings import Settings


def get_settings() -> Settings:
    env = os.getenv("ENV", "local")

    if env == "prod":
        return Settings(_env_file=".env.prod")
    return Settings(_env_file=".env")


settings = get_settings()

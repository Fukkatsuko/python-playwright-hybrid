import os

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
ENV_FILE_PATH = os.path.join(BASE_DIR, ".env")


class Settings(BaseSettings):
    petstore_api_url: str
    petstore_api_key: str
    conduit_api_url: str
    conduit_ui_url: str

    user_email: str = "default@mail.com"
    user_password: str = "default_pass"

    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        env_file_encoding="utf-8"
    )


settings = Settings()

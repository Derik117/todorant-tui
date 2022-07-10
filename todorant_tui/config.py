from pydantic import BaseSettings


class Settings(BaseSettings):
    access_token: str


settings = Settings('.env')  # type: ignore

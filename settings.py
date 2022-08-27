from pydantic import BaseSettings


class Settings(BaseSettings):
    SECRET_ID_TWITCH: str
    CLIENT_ID_TWITCH: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        case_sensitive = True
        extra = 'allow'

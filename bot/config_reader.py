from enum import Enum

from pydantic_settings import BaseSettings
from pydantic import SecretStr


class ModeEnum(str, Enum):
    DEVELOPMENT = "dev"
    PRODUCTION = "prod"


class RabbitSettings(BaseSettings):
    host: str
    port: int
    user: SecretStr
    password: SecretStr
    queue: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        env_prefix = "RABBIT_"


class BotSettings(BaseSettings):
    token: SecretStr

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        env_prefix = "BOT_"


rabbit_config = RabbitSettings()
bot_config = BotSettings()

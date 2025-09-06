from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()

@dataclass
class RedisSettings:
    REDIS_HOST: str = os.getenv("REDIS_HOST")
    REDIS_PORT: any = os.getenv("REDIS_PORT")


redis_settings = RedisSettings()
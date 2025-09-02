from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()

@dataclass
class ApplicationSettings:
    FLASK_HOST: str = os.getenv("FLASK_HOST")
    FLASK_PORT: int = int(os.getenv("FLASK_PORT", 5000))
    FLASK_DEBUG: bool = bool(int(os.getenv("FLASK_DEBUG", 0)))
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    FLASK_ENV: str = os.getenv("FLASK_ENV")

application_settings = ApplicationSettings()
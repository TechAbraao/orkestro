from source.app.utils.decorators.database import database_connection
from source.app.settings.logging_settings import get_logger
from source.app.utils.jwt import *
from zoneinfo import ZoneInfo
import os

logger = get_logger(__name__)
dir_name = os.path.basename(__file__)

class TokensServices:
    def __init__(self):
        self._TOKEN_EXPIRE_MINUTES = 60

    def generate_access_token(self, store_id: str, role="COMMON"):
        now = datetime.now(ZoneInfo("America/Sao_Paulo"))
        expiration_time = now + timedelta(minutes=self._TOKEN_EXPIRE_MINUTES)

        claims = {
            "iss": "Orkestro",
            "sub": str(store_id),
            "role": role,
            "iat": int(now.timestamp()),
            "exp": int(expiration_time.timestamp())
        }

        return generate_token(claims)

    def refresh_access_token(self, store_id: str):
        pass
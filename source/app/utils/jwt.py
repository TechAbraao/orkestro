from source.app.settings.application_settings import application_settings as app
import jwt
from datetime import datetime, timedelta
import zoneinfo

SP_TZ = zoneinfo.ZoneInfo("America/Sao_Paulo")

def generate_token(data: dict, expires_in_minutes: int = (6 * 60)) -> str:
    payload = data.copy()
    payload["exp"] = datetime.now(SP_TZ) + timedelta(minutes=expires_in_minutes)

    token = jwt.encode(payload, app.SECRET_KEY, algorithm="HS256")
    return token


def decrypt_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, app.SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")

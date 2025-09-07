import redis
from source.app.settings.redis_settings import redis_settings as settings

""" Redis Extension """
redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=0,
    decode_responses=True
)
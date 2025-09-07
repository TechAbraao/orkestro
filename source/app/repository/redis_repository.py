from source.app.extesions.redis_client import redis_client

class RedisRepository:
    def __init__(self):
        self.client = redis_client

    def set(self, key: str, value: str, expire: int | None = None) -> None:
        if expire:
            self.client.setex(key, expire, value)
        else:
            self.client.set(key, value)

    def get(self, key: str) -> str | None:
        return self.client.get(key)

    def delete(self, key: str) -> None:
        self.client.delete(key)

    def increment(self, key: str) -> int:
        return self.client.incr(key)

    def push_to_list(self, key: str, value: str) -> None:
        self.client.lpush(key, value)

    def get_list(self, key: str, start: int = 0, end: int = -1) -> list[str]:
        return self.client.lrange(key, start, end)

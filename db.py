import redis


class Redis:
    _conn = None

    def connect(self, url: str):
        self._conn = redis.Redis.from_url(url)

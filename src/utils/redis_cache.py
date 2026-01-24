import os
import json
import redis
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

class CacheManager:
    def __init__(self):
        try:
            self.client = redis.from_url(REDIS_URL, decode_responses=True)
            self.client.ping()
            self.enabled = True
        except Exception as e:
            print(f"Warning: Redis connection failed ({e}). Caching disabled.")
            self.enabled = False

    def get(self, key: str):
        if not self.enabled:
            return None
        data = self.client.get(key)
        return json.loads(data) if data else None

    def set(self, key: str, value: any, expire: int = 86400): # Default 24h
        if not self.enabled:
            return
        self.client.set(key, json.dumps(value), ex=expire)

cache = CacheManager()

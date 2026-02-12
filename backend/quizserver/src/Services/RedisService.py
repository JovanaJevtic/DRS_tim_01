import redis
import json
import os
from typing import Optional, Any


class RedisService:
    _client = None

    @classmethod
    def initialize(cls):
        """Inicijalizuj Redis konekciju"""

        redis_url = os.getenv("REDIS_URL")

        try:
            if redis_url:
                # Parse Redis URL (podržava redis:// sa autentifikacijom)
                cls._client = redis.from_url(
                    redis_url,
                    decode_responses=True,
                    socket_timeout=5,
                    socket_connect_timeout=5,
                    retry_on_timeout=True,
                    health_check_interval=30
                )
            else:
                # fallback za lokalni development
                redis_host = os.getenv("REDIS_HOST", "localhost")
                redis_port = int(os.getenv("REDIS_PORT", 6379))
                redis_db = int(os.getenv("REDIS_DB", 0))

                cls._client = redis.Redis(
                    host=redis_host,
                    port=redis_port,
                    db=redis_db,
                    decode_responses=True,
                    socket_timeout=5
                )

            cls._client.ping()
            print(f"✅ [Redis] Konektovan na {redis_url or redis_host}")

        except Exception as e:
            print(f"⚠️ [Redis] Connection error: {e}")
            print("⚠️ [Redis] App will continue without cache")
            cls._client = None

    @classmethod
    def get_client(cls):
        if cls._client is None:
            cls.initialize()
        return cls._client

    @classmethod
    def get(cls, key: str) -> Optional[Any]:
        """Dohvati vrednost iz keša"""
        if cls._client is None:
            return None
        
        try:
            value = cls._client.get(key)
            if value:
                print(f"🎯 [Redis HIT] {key}")
                return json.loads(value)
            else:
                print(f"❌ [Redis MISS] {key}")
                return None
        except Exception as e:
            print(f"⚠️ [Redis GET Error] {key}: {e}")
            return None

    @classmethod
    def set(cls, key: str, value: Any, ttl: int = 300) -> bool:
        """Postavi vrednost u keš sa TTL"""
        if cls._client is None:
            return False
        
        try:
            serialized = json.dumps(value, default=str)
            cls._client.setex(key, ttl, serialized)
            print(f"💾 [Redis SET] {key} (TTL: {ttl}s)")
            return True
        except Exception as e:
            print(f"⚠️ [Redis SET Error] {key}: {e}")
            return False

    @classmethod
    def delete(cls, key: str) -> bool:
        """Obriši ključ iz keša"""
        if cls._client is None:
            return False
        
        try:
            cls._client.delete(key)
            print(f"🗑️ [Redis DELETE] {key}")
            return True
        except Exception as e:
            print(f"⚠️ [Redis DELETE Error] {key}: {e}")
            return False

    @classmethod
    def invalidate_pattern(cls, pattern: str) -> bool:
        """Obriši sve ključeve koji se poklapaju sa pattern-om"""
        if cls._client is None:
            return False
        
        try:
            keys = cls._client.keys(pattern)
            if keys:
                cls._client.delete(*keys)
                print(f"🗑️ [Redis DELETE PATTERN] {pattern} ({len(keys)} ključeva)")
            return True
        except Exception as e:
            print(f"⚠️ [Redis INVALIDATE Error] {pattern}: {e}")
            return False
import redis
import json
import os
from typing import Optional, Any

class RedisService:
    _client = None
    
    @classmethod
    def initialize(cls):
        """Inicijalizuj Redis konekciju"""
        redis_host = os.getenv("REDIS_HOST", "localhost")
        redis_port = int(os.getenv("REDIS_PORT", 6379))
        redis_db = int(os.getenv("REDIS_DB", 0))
        
        try:
            cls._client = redis.Redis(
                host=redis_host,
                port=redis_port,
                db=redis_db,
                decode_responses=True,
                socket_timeout=5
            )
            # Test konekcije
            cls._client.ping()
            print(f"✅ [Redis] Konektovan na {redis_host}:{redis_port}")
        except Exception as e:
            print(f"⚠️ [Redis] Greška pri konekciji: {e}")
            print(f"⚠️ [Redis] Aplikacija će raditi bez keša")
            cls._client = None
    
    @classmethod
    def get_client(cls):
        """Dohvati Redis klijenta"""
        if cls._client is None:
            cls.initialize()
        return cls._client
    
    @classmethod
    def get(cls, key: str) -> Optional[Any]:
        """Dohvati vrednost iz keša"""
        try:
            client = cls.get_client()
            if client is None:
                return None
            
            value = client.get(key)
            if value:
                print(f"🎯 [Redis HIT] {key}")
                return json.loads(value)
            print(f"❌ [Redis MISS] {key}")
            return None
        except Exception as e:
            print(f"⚠️ [Redis GET Error] {key}: {e}")
            return None
    
    @classmethod
    def set(cls, key: str, value: Any, ttl: int = 300):
        """Sačuvaj vrednost u keš (default TTL: 5 minuta)"""
        try:
            client = cls.get_client()
            if client is None:
                return False
            
            client.setex(key, ttl, json.dumps(value, default=str))
            print(f"💾 [Redis SET] {key} (TTL: {ttl}s)")
            return True
        except Exception as e:
            print(f"⚠️ [Redis SET Error] {key}: {e}")
            return False
    
    @classmethod
    def delete(cls, key: str):
        """Obriši vrednost iz keša"""
        try:
            client = cls.get_client()
            if client is None:
                return False
            
            client.delete(key)
            print(f"🗑️ [Redis DELETE] {key}")
            return True
        except Exception as e:
            print(f"⚠️ [Redis DELETE Error] {key}: {e}")
            return False
    
    @classmethod
    def invalidate_pattern(cls, pattern: str):
        """Obriši sve ključeve koji se poklapaju sa pattern-om"""
        try:
            client = cls.get_client()
            if client is None:
                return False
            
            keys = client.keys(pattern)
            if keys:
                client.delete(*keys)
                print(f"🗑️ [Redis DELETE PATTERN] {pattern} ({len(keys)} ključeva)")
            return True
        except Exception as e:
            print(f"⚠️ [Redis PATTERN Error] {pattern}: {e}")
            return False
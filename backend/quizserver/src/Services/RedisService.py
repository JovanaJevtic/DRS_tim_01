@classmethod
def initialize(cls):
    """Inicijalizuj Redis konekciju"""

    redis_url = os.getenv("REDIS_URL")

    try:
        if redis_url:
            cls._client = redis.from_url(
                redis_url,
                decode_responses=True,
                socket_timeout=5
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
        print("✅ [Redis] Connected successfully")

    except Exception as e:
        print(f"⚠️ [Redis] Connection error: {e}")
        print("⚠️ [Redis] App will continue without cache")
        cls._client = None

from pymongo import MongoClient
import os

class MongoConnection:
    _client = None
    _db = None

    @classmethod
    def initialize(cls):
        """Inicijalizuj MongoDB konekciju"""
        mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
        db_name = os.getenv("MONGO_DB_NAME", "kviz_db")
        
        cls._client = MongoClient(mongo_uri)
        cls._db = cls._client[db_name]
        
        try:
            cls._client.server_info()
            print(f"\x1b[36m[QuizDB@1.0.0]\x1b[0m MongoDB connected to '{db_name}'")
        except Exception as e:
            print(f"\x1b[31m[QuizDB@1.0.0]\x1b[0m MongoDB connection failed: {e}")
        
        return cls._db

    @classmethod
    def get_db(cls):
        """Dohvati bazu podataka"""
        if cls._db is None:
            cls.initialize()
        return cls._db
    
    @classmethod
    def get_collection(cls, collection_name):
        """Dohvati kolekciju iz baze"""
        db = cls.get_db()
        return db[collection_name]

    @classmethod
    def close(cls):
        """Zatvori konekciju"""
        if cls._client:
            cls._client.close()
            print("\x1b[36m[QuizDB@1.0.0]\x1b[0m MongoDB connection closed")
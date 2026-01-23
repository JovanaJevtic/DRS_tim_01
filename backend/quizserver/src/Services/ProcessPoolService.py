from multiprocessing import Pool, cpu_count
import os
from Domain.services.IProcessPoolService import IProcessPoolService
 

class ProcessPoolService(IProcessPoolService):
    """
    Servis za upravljanje pool-om procesa.
    Koristi se za asinhronu obradu kvizova i generisanje PDF izvještaja.
    """
    _pool = None
    _pool_size = None

    @classmethod
    def initialize(cls, pool_size=None):
        """
        Inicijalizuje process pool.
        
        Args:
            pool_size: Broj procesa u pool-u (default: cpu_count)
        """
        if cls._pool is None:
            cls._pool_size = pool_size or min(4, cpu_count())  # Max 4 procesa
            cls._pool = Pool(processes=cls._pool_size)
            print(f"Process Pool inicijalizovan sa {cls._pool_size} procesa")
    
    @classmethod
    def get_pool(cls):
        """Dohvata process pool (lazy initialization)"""
        if cls._pool is None:
            cls.initialize()
        return cls._pool
    
    @classmethod
    def submit_task(cls, func, *args, **kwargs):
        """
        Submituje task u process pool (non-blocking).
        
        Args:
            func: Funkcija koja će se izvršiti u procesu
            *args, **kwargs: Argumenti funkcije
            
        Returns:
            AsyncResult objekat
        """
        pool = cls.get_pool()
        return pool.apply_async(func, args, kwargs)
    
    @classmethod
    def close(cls):
        """Zatvara process pool"""
        if cls._pool:
            cls._pool.close()
            cls._pool.join()
            cls._pool = None
            print("Process Pool zatvoren")
    
    @classmethod
    def get_pool_info(cls):
        """Vraća informacije o pool-u"""
        return {
            "active": cls._pool is not None,
            "pool_size": cls._pool_size,
            "pid": os.getpid()
        }
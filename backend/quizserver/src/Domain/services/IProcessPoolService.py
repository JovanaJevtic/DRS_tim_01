from abc import ABC, abstractmethod

class IProcessPoolService(ABC):
    """Interfejs za servis koji upravlja process pool-om."""

    @classmethod
    @abstractmethod
    def initialize(cls, pool_size=None):
        pass

    @classmethod
    @abstractmethod
    def get_pool(cls):
        pass

    @classmethod
    @abstractmethod
    def submit_task(cls, func, *args, **kwargs):
        pass

    @classmethod
    @abstractmethod
    def close(cls):
        pass

    @classmethod
    @abstractmethod
    def get_pool_info(cls):
        pass

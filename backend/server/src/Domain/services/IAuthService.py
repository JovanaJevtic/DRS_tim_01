from abc import ABC, abstractmethod
from typing import Tuple, Optional

class IAuthService(ABC):

    @abstractmethod
    def login(self, email: str, password: str) -> Tuple[Optional[str], Optional[str]]:
        pass

    @abstractmethod
    def register(self, data: dict):
        pass

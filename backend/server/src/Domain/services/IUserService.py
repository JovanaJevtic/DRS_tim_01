from abc import ABC, abstractmethod
from typing import List
from Domain.DTOs.UserDTO import UserDto


class IUserService(ABC):

    @abstractmethod
    def get_svi_korisnici(self) -> List[UserDto]:
        pass

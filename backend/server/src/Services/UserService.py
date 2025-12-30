from typing import List
from Domain.services.IUserService import IUserService
from Domain.DTOs.UserDTO import UserDto
from Domain.models.User import User
from Database.DbConnectionPool import db 

class UserService(IUserService):

    def get_svi_korisnici(self) -> List[UserDto]:
        users = db.session.query(User).all() 

        return [
            UserDto(
                id=user.id,
                email=user.email,
                uloga=user.uloga.value,
                ime_prezime=f"{user.ime} {user.prezime}"
            )
            for user in users
        ]

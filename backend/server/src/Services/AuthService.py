from datetime import datetime, timedelta
import os
import jwt
import bcrypt 
from Database.DbConnectionPool import db
from Domain.models.User import User
from Domain.enums.Pol import PolEnum
from Domain.enums.Uloga import UlogaEnum

from Domain.services.IAuthService import IAuthService

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_EXPIRES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", "21600"))

class AuthService(IAuthService):

    def login(self, email: str, password: str):
        user = db.session.query(User).filter(User.email == email).first()

        if not user:
            return None, "Neispravan email ili lozinka"

        if user.blocked_until and user.blocked_until > datetime.utcnow():
            return None, "Nalog je privremeno blokiran"

        if bcrypt.checkpw(password.encode('utf-8'), user.lozinka.encode('utf-8')):
            user.failed_attempts = 0
            user.blocked_until = None
            db.session.commit()

            payload = {
                "id": user.id,
                "email": user.email,
                "uloga": user.uloga.value,
                "exp": datetime.utcnow() + timedelta(seconds=JWT_EXPIRES)
            }

            token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
            return token, None

        user.failed_attempts += 1
        if user.failed_attempts >= 3:
            user.blocked_until = datetime.utcnow() + timedelta(minutes=1)
            user.failed_attempts = 0

        db.session.commit()
        return None, "Neispravan email ili lozinka"

    def register(self, data: dict):
        if db.session.query(User).filter(User.email == data["email"]).first():
            return None, "Email već postoji"

        raw_password = data["password"].encode('utf-8')
        hashed_password = bcrypt.hashpw(raw_password, bcrypt.gensalt())

        pol_value = None
        if data.get("pol"):
            pol_str = data["pol"].upper()
            pol_mapping = {
                "M": PolEnum.MUSKI,
                "Z": PolEnum.ZENSKI,
                "O": PolEnum.DRUGO
            }
            pol_value = pol_mapping.get(pol_str)

        if pol_value is None:
            return None, "Neispravna vrednost za pol"

        user = User(
            ime=data["ime"],
            prezime=data["prezime"],
            email=data["email"],
            lozinka=hashed_password.decode('utf-8'),  
            datum_rodjenja=data.get("datum_rodjenja"),
            pol = pol_value,
            drzava=data.get("drzava"),
            ulica=data.get("ulica"),
            broj=data.get("broj"),
            uloga=UlogaEnum.IGRAC
        )

        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)

        return user, None
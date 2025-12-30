from Database.DbConnectionPool import db
from datetime import datetime
from Domain.enums.Pol import PolEnum
from Domain.enums.Uloga import UlogaEnum


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    ime = db.Column(db.String(50), nullable=False)
    prezime = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    datum_rodjenja = db.Column(db.Date)
    pol = db.Column(db.Enum(PolEnum))
    drzava = db.Column(db.String(50))
    ulica = db.Column(db.String(100))
    broj = db.Column(db.String(20))
    lozinka = db.Column(db.String(255), nullable=False)
    uloga = db.Column(db.Enum(UlogaEnum), default=UlogaEnum.IGRAC)

    failed_attempts = db.Column(db.Integer, default=0)
    blocked_until = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

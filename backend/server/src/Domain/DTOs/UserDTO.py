class UserDto:
    def __init__(self, id: int, email: str, uloga: str, ime_prezime: str):
        self.id = id
        self.email = email
        self.uloga = uloga
        self.ime_prezime = ime_prezime

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "uloga": self.uloga,
            "imePrezime": self.ime_prezime
        }

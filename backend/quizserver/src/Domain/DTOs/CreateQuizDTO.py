class CreateQuizDTO:
    """DTO za kreiranje novog kviza od strane moderatora"""
    
    def __init__(self, naziv, pitanja, trajanje_sekunde, autor_id, autor_email):
        self.naziv = naziv
        self.pitanja = pitanja  
        self.trajanje_sekunde = trajanje_sekunde
        self.autor_id = autor_id
        self.autor_email = autor_email

    @staticmethod
    def from_dict(data):
        """Kreira DTO iz JSON podataka sa frontend-a"""
        return CreateQuizDTO(
            naziv=data.get("naziv"),
            pitanja=data.get("pitanja"),
            trajanje_sekunde=data.get("trajanje_sekunde"),
            autor_id=data.get("autor_id"),
            autor_email=data.get("autor_email")
        )
    
    def to_dict(self):
        """Konvertuje DTO u dict za MongoDB"""
        return {
            "naziv": self.naziv,
            "pitanja": self.pitanja,
            "trajanje_sekunde": self.trajanje_sekunde,
            "autor_id": self.autor_id,
            "autor_email": self.autor_email
        }
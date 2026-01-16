class QuizResponseDTO:
    """DTO za slanje kviza klijentu"""
    
    def __init__(self, id, naziv, pitanja, trajanje_sekunde, autor_id, autor_email, status, razlog_odbijanja=None, created_at=None):
        self.id = str(id)  
        self.naziv = naziv
        self.pitanja = pitanja
        self.trajanje_sekunde = trajanje_sekunde
        self.autor_id = autor_id
        self.autor_email = autor_email
        self.status = status
        self.razlog_odbijanja = razlog_odbijanja
        self.created_at = created_at

    def to_dict(self):
        """Konvertuje DTO u dict za slanje klijentu"""
        return {
            "id": self.id,
            "naziv": self.naziv,
            "pitanja": self.pitanja,
            "trajanje_sekunde": self.trajanje_sekunde,
            "autor_id": self.autor_id,
            "autor_email": self.autor_email,
            "status": self.status,
            "razlog_odbijanja": self.razlog_odbijanja,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
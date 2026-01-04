class SubmitQuizDTO:
    """DTO za slanje odgovora od igrača"""
    
    def __init__(self, quiz_id, igrac_id, igrac_email, odgovori, vrijeme_utroseno_sekunde):
        self.quiz_id = quiz_id
        self.igrac_id = igrac_id
        self.igrac_email = igrac_email
        self.odgovori = odgovori  # Lista odgovora: [{"pitanje_id": 1, "odgovor_ids": ["a"]}, ...]
        self.vrijeme_utroseno_sekunde = vrijeme_utroseno_sekunde

    @staticmethod
    def from_dict(data):
        """Kreira DTO iz JSON podataka"""
        return SubmitQuizDTO(
            quiz_id=data.get("quiz_id"),
            igrac_id=data.get("igrac_id"),
            igrac_email=data.get("igrac_email"),
            odgovori=data.get("odgovori"),
            vrijeme_utroseno_sekunde=data.get("vrijeme_utroseno_sekunde")
        )
    
    def to_dict(self):
        """Konvertuje DTO u dict"""
        return {
            "quiz_id": self.quiz_id,
            "igrac_id": self.igrac_id,
            "igrac_email": self.igrac_email,
            "odgovori": self.odgovori,
            "vrijeme_utroseno_sekunde": self.vrijeme_utroseno_sekunde
        }
from datetime import datetime

class QuizResultDTO:
    """DTO za rezultate kviza"""
    
    def __init__(self, quiz_id, quiz_naziv, igrac_id, igrac_email, odgovori, 
                 ukupno_bodova, maksimalno_bodova, vrijeme_utroseno_sekunde, 
                 started_at=None, completed_at=None):
        self.quiz_id = quiz_id
        self.quiz_naziv = quiz_naziv
        self.igrac_id = igrac_id
        self.igrac_email = igrac_email
        self.odgovori = odgovori
        self.ukupno_bodova = ukupno_bodova
        self.maksimalno_bodova = maksimalno_bodova
        self.vrijeme_utroseno_sekunde = vrijeme_utroseno_sekunde
        self.started_at = started_at or datetime.utcnow()
        self.completed_at = completed_at or datetime.utcnow()
        
        # Izračunaj procenat ODMAH u __init__
        if maksimalno_bodova > 0:
            self.procenat = round((ukupno_bodova / maksimalno_bodova) * 100, 1)
        else:
            self.procenat = 0.0
    
    def to_dict(self):
        """Konvertuje DTO u dict za MongoDB"""
        return {
            "quiz_id": self.quiz_id,
            "quiz_naziv": self.quiz_naziv,
            "igrac_id": self.igrac_id,
            "igrac_email": self.igrac_email,
            "odgovori": self.odgovori,
            "ukupno_bodova": self.ukupno_bodova,
            "maksimalno_bodova": self.maksimalno_bodova,
            "vrijeme_utroseno_sekunde": self.vrijeme_utroseno_sekunde,
            "procenat": self.procenat,  # ← Koristi self.procenat, ne računaj ponovo
            "started_at": self.started_at,
            "completed_at": self.completed_at
        }
from datetime import datetime

class SubmitQuizDTO:
    """DTO za slanje odgovora od igrača"""
    
    def __init__(self, quiz_id, igrac_id, igrac_email, odgovori, vrijeme_utroseno_sekunde=None, vreme_pocetka=None, vreme_kraja=None):
        self.quiz_id = quiz_id
        self.igrac_id = igrac_id
        self.igrac_email = igrac_email
        self.odgovori = odgovori 
        self.vreme_pocetka = vreme_pocetka
        self.vreme_kraja = vreme_kraja
        
        if vrijeme_utroseno_sekunde is not None:
            self.vrijeme_utroseno_sekunde = vrijeme_utroseno_sekunde
        elif vreme_pocetka and vreme_kraja:
            self.vrijeme_utroseno_sekunde = self._calculate_time_difference(vreme_pocetka, vreme_kraja)
        else:
            self.vrijeme_utroseno_sekunde = None

    @staticmethod
    def _calculate_time_difference(start_str, end_str):
        """Izračunava razliku u sekundama između dva timestamp-a"""
        try:
            start = datetime.fromisoformat(start_str.replace('Z', '+00:00'))
            end = datetime.fromisoformat(end_str.replace('Z', '+00:00'))
            return int((end - start).total_seconds())
        except Exception as e:
            print(f"⚠️ Greška pri računanju vremena: {e}")
            return None

    @staticmethod
    def from_dict(data):
        """Kreira DTO iz JSON podataka"""
        return SubmitQuizDTO(
            quiz_id=data.get("quiz_id"),
            igrac_id=data.get("igrac_id"),
            igrac_email=data.get("igrac_email"),
            odgovori=data.get("odgovori"),
            vrijeme_utroseno_sekunde=data.get("vrijeme_utroseno_sekunde"),
            vreme_pocetka=data.get("vreme_pocetka"),
            vreme_kraja=data.get("vreme_kraja")
        )
    
    def to_dict(self):
        """Konvertuje DTO u dict"""
        return {
            "quiz_id": self.quiz_id,
            "igrac_id": self.igrac_id,
            "igrac_email": self.igrac_email,
            "odgovori": self.odgovori,
            "vrijeme_utroseno_sekunde": self.vrijeme_utroseno_sekunde,
            "vreme_pocetka": self.vreme_pocetka,
            "vreme_kraja": self.vreme_kraja
        }
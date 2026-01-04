class QuizValidator:
    
    @staticmethod
    def validate_create_quiz(data: dict) -> tuple[bool, str]:
        """Validira podatke za kreiranje kviza"""
        
        # Naziv
        if not data.get("naziv"):
            return False, "Naziv kviza je obavezan"
        
        if len(data.get("naziv", "")) < 3:
            return False, "Naziv mora imati najmanje 3 karaktera"
        
        # Pitanja
        pitanja = data.get("pitanja", [])
        if not pitanja or len(pitanja) == 0:
            return False, "Kviz mora imati bar jedno pitanje"
        
        # Trajanje
        trajanje = data.get("trajanje_sekunde")
        if not trajanje or trajanje < 10:
            return False, "Trajanje mora biti najmanje 10 sekundi"
        
        # Validacija svakog pitanja
        for i, pitanje in enumerate(pitanja):
            if not pitanje.get("tekst"):
                return False, f"Pitanje {i+1}: Tekst je obavezan"
            
            if not pitanje.get("bodovi") or pitanje["bodovi"] <= 0:
                return False, f"Pitanje {i+1}: Bodovi moraju biti veći od 0"
            
            odgovori = pitanje.get("odgovori", [])
            if len(odgovori) < 2:
                return False, f"Pitanje {i+1}: Mora imati najmanje 2 odgovora"
            
            # Proveri tačne odgovore
            ima_tacan = any(o.get("tacan") for o in odgovori)
            if not ima_tacan:
                return False, f"Pitanje {i+1}: Mora imati bar jedan tačan odgovor"
        
        return True, ""
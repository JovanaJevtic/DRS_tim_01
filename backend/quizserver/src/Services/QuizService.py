from typing import List, Tuple, Optional
from datetime import datetime
from bson import ObjectId
from Domain.services.IQuizService import IQuizService
from Domain.DTOs.CreateQuizDTO import CreateQuizDTO
from Domain.DTOs.QuizResponseDTO import QuizResponseDTO
from Domain.DTOs.SubmitQuizDTO import SubmitQuizDTO
from Domain.DTOs.QuizResultDTO import QuizResultDTO
from Domain.enums.QuizStatus import QuizStatus
from Database.MongoConnection import MongoConnection

class QuizService(IQuizService):
    
    def __init__(self):
        self.quizzes_collection = MongoConnection.get_collection("quizzes")
        self.results_collection = MongoConnection.get_collection("quiz_results")
        self.email_service = None
    
    def _get_email_service(self):
        """Lazy loading email servisa (izbegava circular import)"""
        if self.email_service is None:
            from Services.EmailService import EmailService
            self.email_service = EmailService()
        return self.email_service
    
    def create_quiz(self, quiz_data: dict) -> Tuple[Optional[dict], Optional[str]]:
        """Kreira novi kviz (validacija je već urađena u Validator-u)"""
        try:
            # Kreiraj DTO
            dto = CreateQuizDTO.from_dict(quiz_data)
            
            # Pripremi dokument za MongoDB
            quiz_document = {
                "naziv": dto.naziv,
                "pitanja": dto.pitanja,
                "trajanje_sekunde": dto.trajanje_sekunde,
                "autor_id": dto.autor_id,
                "autor_email": dto.autor_email,
                "status": QuizStatus.PENDING.value,
                "razlog_odbijanja": None,
                "created_at": datetime.utcnow()
            }
            
            # Ubaci u MongoDB
            result = self.quizzes_collection.insert_one(quiz_document)
            
            # Dohvati kreirani kviz
            created_quiz = self.quizzes_collection.find_one({"_id": result.inserted_id})
            
            # Konvertuj u response DTO
            response = QuizResponseDTO(
                id=created_quiz["_id"],
                naziv=created_quiz["naziv"],
                pitanja=created_quiz["pitanja"],
                trajanje_sekunde=created_quiz["trajanje_sekunde"],
                autor_id=created_quiz["autor_id"],
                autor_email=created_quiz["autor_email"],
                status=created_quiz["status"],
                razlog_odbijanja=created_quiz.get("razlog_odbijanja"),
                created_at=created_quiz.get("created_at")
            )
            
            print(f"✅ Kviz '{dto.naziv}' kreiran sa ID: {result.inserted_id}")
            return response.to_dict(), None
            
        except Exception as e:
            print(f"❌ Greška pri kreiranju kviza: {str(e)}")
            return None, f"Greška pri kreiranju kviza: {str(e)}"
    
    def get_all_quizzes(self, status: Optional[str] = None) -> List[dict]:
        """Dohvata sve kvizove"""
        try:
            # Filtriraj po statusu ako je prosleđen
            query = {}
            if status:
                query["status"] = status
            
            quizzes = list(self.quizzes_collection.find(query).sort("created_at", -1))
            
            # Konvertuj u response DTOs
            return [
                QuizResponseDTO(
                    id=quiz["_id"],
                    naziv=quiz["naziv"],
                    pitanja=quiz["pitanja"],
                    trajanje_sekunde=quiz["trajanje_sekunde"],
                    autor_id=quiz["autor_id"],
                    autor_email=quiz["autor_email"],
                    status=quiz["status"],
                    razlog_odbijanja=quiz.get("razlog_odbijanja"),
                    created_at=quiz.get("created_at")
                ).to_dict()
                for quiz in quizzes
            ]
        except Exception as e:
            print(f"❌ Greška pri dohvatanju kvizova: {str(e)}")
            return []
    
    def get_quiz_by_id(self, quiz_id: str) -> Optional[dict]:
        """Dohvata kviz po ID-u"""
        try:
            quiz = self.quizzes_collection.find_one({"_id": ObjectId(quiz_id)})
            
            if not quiz:
                return None
            
            return QuizResponseDTO(
                id=quiz["_id"],
                naziv=quiz["naziv"],
                pitanja=quiz["pitanja"],
                trajanje_sekunde=quiz["trajanje_sekunde"],
                autor_id=quiz["autor_id"],
                autor_email=quiz["autor_email"],
                status=quiz["status"],
                razlog_odbijanja=quiz.get("razlog_odbijanja"),
                created_at=quiz.get("created_at")
            ).to_dict()
            
        except Exception as e:
            print(f"❌ Greška pri dohvatanju kviza: {str(e)}")
            return None
    
    def approve_quiz(self, quiz_id: str) -> Tuple[bool, Optional[str]]:
        """Odobrava kviz"""
        try:
            result = self.quizzes_collection.update_one(
                {"_id": ObjectId(quiz_id)},
                {"$set": {
                    "status": QuizStatus.APPROVED.value,
                    "razlog_odbijanja": None
                }}
            )
            
            if result.modified_count == 0:
                return False, "Kviz nije pronađen"
            
            print(f"✅ Kviz {quiz_id} odobren")
            return True, None
            
        except Exception as e:
            print(f"❌ Greška pri odobravanju kviza: {str(e)}")
            return False, f"Greška: {str(e)}"
    
    def reject_quiz(self, quiz_id: str, razlog: str) -> Tuple[bool, Optional[str]]:
        """Odbija kviz sa razlogom"""
        try:
            if not razlog:
                return False, "Razlog odbijanja je obavezan"
            
            result = self.quizzes_collection.update_one(
                {"_id": ObjectId(quiz_id)},
                {"$set": {
                    "status": QuizStatus.REJECTED.value,
                    "razlog_odbijanja": razlog
                }}
            )
            
            if result.modified_count == 0:
                return False, "Kviz nije pronađen"
            
            print(f"❌ Kviz {quiz_id} odbijen. Razlog: {razlog}")
            return True, None
            
        except Exception as e:
            print(f"❌ Greška pri odbijanju kviza: {str(e)}")
            return False, f"Greška: {str(e)}"
    
    def delete_quiz(self, quiz_id: str) -> Tuple[bool, Optional[str]]:
        """Briše kviz"""
        try:
            result = self.quizzes_collection.delete_one({"_id": ObjectId(quiz_id)})
            
            if result.deleted_count == 0:
                return False, "Kviz nije pronađen"
            
            print(f"🗑️ Kviz {quiz_id} obrisan")
            return True, None
            
        except Exception as e:
            print(f"❌ Greška pri brisanju kviza: {str(e)}")
            return False, f"Greška: {str(e)}"
    
    def process_quiz_submission(self, submission_data: dict) -> Tuple[Optional[dict], Optional[str]]:
        """Obrađuje odgovore igrača"""
        try:
            # Kreiraj DTO
            submit_dto = SubmitQuizDTO.from_dict(submission_data)
            
            # Dohvati kviz
            quiz = self.quizzes_collection.find_one({"_id": ObjectId(submit_dto.quiz_id)})
            if not quiz:
                return None, "Kviz nije pronađen"
            
            # Izračunaj bodove
            ukupno_bodova = 0
            maksimalno_bodova = sum(p["bodovi"] for p in quiz["pitanja"])
            tacnih_odgovora = 0
            
            for pitanje in quiz["pitanja"]:
                # Nađi odgovor igrača za ovo pitanje
                igrac_odgovor = next(
                    (o for o in submit_dto.odgovori if o["pitanje_id"] == pitanje["id"]), 
                    None
                )
                
                if igrac_odgovor:
                    # Dohvati tačne odgovore za pitanje
                    tacni_odgovori_ids = [
                        odg["id"] for odg in pitanje["odgovori"] if odg.get("tacan", False)
                    ]
                    
                    # Dohvati odgovor igrača (može biti "odgovor_id" ili "odgovor_ids")
                    igrac_odgovor_id = igrac_odgovor.get("odgovor_id")  # Pojedinačni odgovor
                    igrac_odgovori_ids = igrac_odgovor.get("odgovor_ids", [])  # Višestruki odgovori
                    
                    # Ako ima pojedinačni odgovor, pretvori ga u listu
                    if igrac_odgovor_id:
                        igrac_odgovori_ids = [igrac_odgovor_id]
                    
                    # Proveri da li su odgovori tačni
                    if set(tacni_odgovori_ids) == set(igrac_odgovori_ids):
                        ukupno_bodova += pitanje["bodovi"]
                        tacnih_odgovora += 1
            
            # Kreiraj rezultat
            result_dto = QuizResultDTO(
                quiz_id=submit_dto.quiz_id,
                quiz_naziv=quiz["naziv"],
                igrac_id=submit_dto.igrac_id,
                igrac_email=submit_dto.igrac_email,
                odgovori=submit_dto.odgovori,
                ukupno_bodova=ukupno_bodova,
                maksimalno_bodova=maksimalno_bodova,
                vrijeme_utroseno_sekunde=submit_dto.vrijeme_utroseno_sekunde
            )
            
            # Sačuvaj u bazu
            self.results_collection.insert_one(result_dto.to_dict())
            
            print(f"✅ Rezultat sačuvan: {ukupno_bodova}/{maksimalno_bodova} bodova ({tacnih_odgovora} tačnih odgovora)")
            
            # POŠALJI EMAIL SA REZULTATIMA
            self._get_email_service().send_quiz_results(
                igrac_email=submit_dto.igrac_email,
                quiz_naziv=quiz["naziv"],
                ukupno_bodova=ukupno_bodova,
                maksimalno_bodova=maksimalno_bodova,
                procenat=result_dto.procenat,
                vrijeme_utroseno_sekunde=submit_dto.vrijeme_utroseno_sekunde
            )
            
            return result_dto.to_dict(), None
            
        except Exception as e:
            print(f"❌ Greška pri obradi rezultata: {str(e)}")
            import traceback
            traceback.print_exc()
            return None, f"Greška: {str(e)}"
    
    def get_leaderboard(self, quiz_id: str) -> List[dict]:
        """Dohvata rang listu"""
        try:
            results = list(
                self.results_collection.find({"quiz_id": quiz_id})
                .sort([
                    ("ukupno_bodova", -1),  # Prvo po bodovima (najviše)
                    ("vrijeme_utroseno_sekunde", 1)  # Ako isti bodovi, po vremenu (najbrži)
                ])
            )
            
            # Konvertuj ObjectId u string i dodaj rank
            for idx, r in enumerate(results, start=1):
                r["_id"] = str(r["_id"])
                r["rank"] = idx
            
            return results
            
        except Exception as e:
            print(f"❌ Greška pri dohvatanju rang liste: {str(e)}")
            return []
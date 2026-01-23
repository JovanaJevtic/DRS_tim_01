from typing import List, Tuple, Optional
from datetime import datetime
from bson import ObjectId
from Domain.services.IQuizService import IQuizService
from Domain.DTOs.CreateQuizDTO import CreateQuizDTO
from Domain.DTOs.QuizResponseDTO import QuizResponseDTO
from Domain.DTOs.SubmitQuizDTO import SubmitQuizDTO
from Domain.enums.QuizStatus import QuizStatus
from Database.MongoConnection import MongoConnection
from Services.ProcessPoolService import ProcessPoolService
from Services.ProcessWorkers import process_quiz_results_worker, generate_pdf_report_worker

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
        """Kreira novi kviz"""
        try:
            dto = CreateQuizDTO.from_dict(quiz_data)
            
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
            
            result = self.quizzes_collection.insert_one(quiz_document)
            created_quiz = self.quizzes_collection.find_one({"_id": result.inserted_id})
            
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
            
            print(f" Kviz '{dto.naziv}' kreiran sa ID: {result.inserted_id}")
            return response.to_dict(), None
            
        except Exception as e:
            print(f" Greška pri kreiranju kviza: {str(e)}")
            return None, f"Greška pri kreiranju kviza: {str(e)}"
    
    def get_all_quizzes(self, status: Optional[str] = None) -> List[dict]:
        """Dohvata sve kvizove"""
        try:
            query = {}
            if status:
                query["status"] = status
            
            quizzes = list(self.quizzes_collection.find(query).sort("created_at", -1))
            
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
            print(f" Greška pri dohvatanju kvizova: {str(e)}")
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
            print(f" Greška pri dohvatanju kviza: {str(e)}")
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
            
            print(f" Kviz {quiz_id} odobren")
            return True, None
            
        except Exception as e:
            print(f" Greška pri odobravanju kviza: {str(e)}")
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
            
            print(f" Kviz {quiz_id} odbijen. Razlog: {razlog}")
            return True, None
            
        except Exception as e:
            print(f" Greška pri odbijanju kviza: {str(e)}")
            return False, f"Greška: {str(e)}"
    
    def delete_quiz(self, quiz_id: str) -> Tuple[bool, Optional[str]]:
        """Briše kviz"""
        try:
            result = self.quizzes_collection.delete_one({"_id": ObjectId(quiz_id)})
            
            if result.deleted_count == 0:
                return False, "Kviz nije pronađen"
            
            print(f" Kviz {quiz_id} obrisan")
            return True, None
            
        except Exception as e:
            print(f" Greška pri brisanju kviza: {str(e)}")
            return False, f"Greška: {str(e)}"
    
    def process_quiz_submission(self, submission_data: dict) -> Tuple[Optional[dict], Optional[str]]:
        """
         ASINHRONA OBRADA SA PROCESIMA 
        
        API odmah vraća odgovor igraču.
        Obrada se izvršava u posebnom procesu (background).
        """
        try:
            submit_dto = SubmitQuizDTO.from_dict(submission_data)
            
            # Proveri da li kviz postoji
            quiz = self.quizzes_collection.find_one({"_id": ObjectId(submit_dto.quiz_id)})
            if not quiz:
                return None, "Kviz nije pronađen"
            
            print(f"🚀 Pokretanje ASINHRONE obrade kviza u POSEBNOM PROCESU...")
            
            async_result = ProcessPoolService.submit_task(
                process_quiz_results_worker,
                submit_dto.quiz_id,
                submit_dto.igrac_id,
                submit_dto.igrac_email,
                submit_dto.odgovori,
                submit_dto.vrijeme_utroseno_sekunde
            )
            
            print(f" Obrada pokrenuta u background procesu! Igrač može nastaviti rad.")
            print(f" Email sa rezultatima će biti poslat nakon završetka obrade.")
            
            # Vrati odmah odgovor (igrač ne čeka!)
            return {
                "quiz_id": submit_dto.quiz_id,
                "quiz_naziv": quiz["naziv"],
                "status": "processing",
                "message": "Obrada odgovora je u toku. Rezultati će biti poslati na email."
            }, None
            
        except Exception as e:
            print(f"❌ Greška pri pokretanju obrade: {str(e)}")
            import traceback
            traceback.print_exc()
            return None, f"Greška: {str(e)}"
    
    def get_leaderboard(self, quiz_id: str) -> List[dict]:
        """Dohvata rang listu"""
        try:
            results = list(
                self.results_collection.find({"quiz_id": quiz_id})
                .sort([
                   ("ukupno_bodova", -1),
                   ("vrijeme_utroseno_sekunde", 1)
                ])
            )

            return [
                {
                    "rank": idx,
                    "igrac_email": r.get("igrac_email"),
                    "bodovi": r.get("ukupno_bodova"),
                    "vrijeme_utroseno": r.get("vrijeme_utroseno_sekunde")
                }
                for idx, r in enumerate(results, start=1)
            ]

        except Exception as e:
            print(f"❌ Greška pri dohvatanju rang liste: {str(e)}")
            return []
            
    def get_results_for_player(self, igrac_id: int) -> List[dict]:
        """Dohvata sve rezultate za ulogovanog igrača"""
        try:
            results = list(
                self.results_collection
               .find({"igrac_id": igrac_id})
               .sort("created_at", -1)
            )

            return [
                {
                    "quiz_id": r.get("quiz_id"),
                    "quiz_naziv": r.get("quiz_naziv"),
                    "ukupno_bodova": r.get("ukupno_bodova"),
                    "maksimalno_bodova": r.get("maksimalno_bodova"),
                    "procenat": r.get("procenat"),
                    "vrijeme_utroseno_sekunde": r.get("vrijeme_utroseno_sekunde"),
                    "created_at": r.get("created_at")
                }
                for r in results
            ]

        except Exception as e:
            print(f"❌ Greška pri dohvatanju rezultata igrača: {str(e)}")
            return []

    def send_quiz_report_to_admin(self, quiz_id: str, admin_email: str) -> Tuple[bool, Optional[str]]:
        """
        ⚡ ASINHRONO GENERISANJE PDF-a U PROCESU ⚡
        
        API odmah vraća odgovor.
        PDF se generiše u background procesu.
        """
        try:
            quiz = self.quizzes_collection.find_one({"_id": ObjectId(quiz_id)})
            if not quiz:
                return False, "Kviz nije pronađen"

            print(f"📄 Pokretanje PDF generisanja u POSEBNOM PROCESU...")
            
            async_result = ProcessPoolService.submit_task(
                generate_pdf_report_worker,
                quiz_id,
                admin_email
            )
            
            print(f"PDF generisanje pokrenuto u background procesu!")
            print(f"PDF izvještaj će stići na email nakon završetka.")
            
            return True, None

        except Exception as e:
            print(f"Greška pri pokretanju PDF generisanja: {str(e)}")
            import traceback
            traceback.print_exc()
            return False, f"Greška: {str(e)}"
from abc import ABC, abstractmethod
from typing import List, Tuple, Optional

class IQuizService(ABC):
    """Interface za Quiz servis"""
    
    @abstractmethod
    def create_quiz(self, quiz_data: dict) -> Tuple[Optional[dict], Optional[str]]:
        """
        Kreira novi kviz
        
        Args:
            quiz_data: Podaci o kvizu sa frontend-a
            
        Returns:
            Tuple[dict, None] ako je uspešno
            Tuple[None, str] ako je greška (error message)
        """
        pass
    
    @abstractmethod
    def get_all_quizzes(self, status: Optional[str] = None) -> List[dict]:
        """
        Dohvata sve kvizove (opciono filtriranje po statusu)
        
        Args:
            status: PENDING, APPROVED, REJECTED (opciono)
            
        Returns:
            Lista kvizova
        """
        pass
    
    @abstractmethod
    def get_quiz_by_id(self, quiz_id: str) -> Optional[dict]:
        """
        Dohvata kviz po ID-u
        
        Args:
            quiz_id: MongoDB ObjectId kao string
            
        Returns:
            Dict sa podacima kviza ili None
        """
        pass
    
    @abstractmethod
    def approve_quiz(self, quiz_id: str) -> Tuple[bool, Optional[str]]:
        """
        Odobrava kviz (samo ADMIN)
        
        Args:
            quiz_id: ID kviza
            
        Returns:
            Tuple[True, None] ako je uspešno
            Tuple[False, str] ako je greška
        """
        pass
    
    @abstractmethod
    def reject_quiz(self, quiz_id: str, razlog: str) -> Tuple[bool, Optional[str]]:
        """
        Odbija kviz sa razlogom (samo ADMIN)
        
        Args:
            quiz_id: ID kviza
            razlog: Razlog odbijanja
            
        Returns:
            Tuple[True, None] ako je uspešno
            Tuple[False, str] ako je greška
        """
        pass
    
    @abstractmethod
    def delete_quiz(self, quiz_id: str) -> Tuple[bool, Optional[str]]:
        """
        Briše kviz (MODERATOR ili ADMIN)
        
        Args:
            quiz_id: ID kviza
            
        Returns:
            Tuple[True, None] ako je uspešno
            Tuple[False, str] ako je greška
        """
        pass
    
    @abstractmethod
    def process_quiz_submission(self, submission_data: dict) -> Tuple[Optional[dict], Optional[str]]:
        """
        Obrađuje odgovore igrača i čuva rezultat
        
        Args:
            submission_data: Podaci o odgovorima
            
        Returns:
            Tuple[dict, None] sa rezultatima ako je uspešno
            Tuple[None, str] ako je greška
        """
        pass
    
    @abstractmethod
    def get_leaderboard(self, quiz_id: str) -> List[dict]:
        """
        Dohvata rang listu za kviz
        
        Args:
            quiz_id: ID kviza
            
        Returns:
            Lista rezultata sortiranih po bodovima
        """
        pass
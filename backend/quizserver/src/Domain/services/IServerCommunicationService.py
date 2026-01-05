from abc import ABC, abstractmethod

class IServerCommunicationService(ABC):
    """Interface za komunikaciju sa Server-om"""
    
    @abstractmethod
    def notify_new_quiz(self, quiz_data: dict) -> bool:
        """Obavesti Server da je kreiran novi kviz"""
        pass
    
    @abstractmethod
    def notify_quiz_approved(self, quiz_id: str, moderator_id: int) -> bool:
        """Obavesti Server da je kviz odobren"""
        pass
    
    @abstractmethod
    def notify_quiz_rejected(self, quiz_id: str, razlog: str, moderator_id: int) -> bool:
        """Obavesti Server da je kviz odbijen"""
        pass
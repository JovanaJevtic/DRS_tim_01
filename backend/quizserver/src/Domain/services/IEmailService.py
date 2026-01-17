from abc import ABC, abstractmethod

class IEmailService(ABC):
    """Interface za email servis"""
    
    @abstractmethod
    def send_quiz_results(self, igrac_email: str, quiz_naziv: str, 
                         ukupno_bodova: int, maksimalno_bodova: int, 
                         procenat: float, vrijeme_utroseno_sekunde: int) -> bool:
        pass

    @abstractmethod
    def send_quiz_report(self, admin_email: str, quiz_naziv: str, pdf_bytes: bytes, filename: str) -> bool:
        pass

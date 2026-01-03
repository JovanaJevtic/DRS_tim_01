from abc import ABC, abstractmethod


class IEmailService(ABC):
    """Interface za Email servis"""
    
    @abstractmethod
    def send_role_change_email(self, user_email: str, user_name: str, new_role: str) -> bool:
        """
        Pošalji email korisniku kada mu se promeni uloga
        
        Args:
            user_email: Email adresa korisnika
            user_name: Ime korisnika
            new_role: Nova uloga (IGRAC, MODERATOR, ADMINISTRATOR)
            
        Returns:
            bool: True ako je email uspešno poslat, False inače
        """
        pass
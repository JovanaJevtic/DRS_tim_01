import requests
import os
from Domain.services.IServerCommunicationService import IServerCommunicationService

class ServerCommunicationService(IServerCommunicationService):
    """Implementacija komunikacije sa Server-om"""
    
    def __init__(self):
        self.server_url = os.getenv("SERVER_URL", "http://localhost:5000")
    
    def notify_new_quiz(self, quiz_data: dict) -> bool:
        """Obavesti Server da je kreiran novi kviz"""
        try:
            response = requests.post(
                f"{self.server_url}/api/v1/internal/quiz/created",
                json=quiz_data,
                timeout=5
            )
            
            if response.status_code == 200:
                print(f" Server obavešten o novom kvizu: {quiz_data.get('naziv')}")
                return True
            else:
                print(f" Server vratio status {response.status_code}")
                return False
                
        except Exception as e:
            print(f" Greška pri komunikaciji sa serverom: {str(e)}")
            return False
    
    def notify_quiz_approved(self, quiz_id: str, moderator_id: int) -> bool:
        """Obavesti Server da je kviz odobren"""
        try:
            response = requests.post(
                f"{self.server_url}/api/v1/internal/quiz/approved",
                json={"quiz_id": quiz_id, "moderator_id": moderator_id},
                timeout=5
            )
            
            if response.status_code == 200:
                print(f" Server obavešten o odobrenju kviza {quiz_id}")
                return True
            else:
                print(f" Server vratio status {response.status_code}")
                return False
                
        except Exception as e:
            print(f" Greška: {str(e)}")
            return False
    
    def notify_quiz_rejected(self, quiz_id: str, razlog: str, moderator_id: int) -> bool:
        """Obavesti Server da je kviz odbijen"""
        try:
            response = requests.post(
                f"{self.server_url}/api/v1/internal/quiz/rejected",
                json={"quiz_id": quiz_id, "razlog": razlog, "moderator_id": moderator_id},
                timeout=5
            )
            
            if response.status_code == 200:
                print(f" Server obavešten o odbijanju kviza {quiz_id}")
                return True
            else:
                print(f"Server vratio status {response.status_code}")
                return False
                
        except Exception as e:
            print(f" Greška: {str(e)}")
            return False
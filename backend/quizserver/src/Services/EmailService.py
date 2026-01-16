from flask_mail import Mail, Message
import os
from Domain.services.IEmailService import IEmailService

mail = Mail()

class EmailService(IEmailService):
    """Implementacija email servisa"""
    
    def send_quiz_results(self, igrac_email: str, quiz_naziv: str, 
                         ukupno_bodova: int, maksimalno_bodova: int, 
                         procenat: float, vrijeme_utroseno_sekunde: int) -> bool:
        """Šalje email sa rezultatima kviza"""
        try:
            if vrijeme_utroseno_sekunde:
                minuta = vrijeme_utroseno_sekunde // 60
                sekundi = vrijeme_utroseno_sekunde % 60
                vrijeme_text = f"{minuta} minuta i {sekundi} sekundi"
            else:
                vrijeme_text = "N/A"
            
            subject = f"Rezultati kviza: {quiz_naziv}"
            
            body = f"""
Pozdrav {igrac_email},

Rezultati kviza "{quiz_naziv}":

📊 REZULTAT:
   • Osvojeno bodova: {ukupno_bodova}/{maksimalno_bodova}
   • Procenat: {procenat:.1f}%
   • Vreme: {vrijeme_text}

{"🎉 Čestitamo! Odličan rezultat!" if procenat >= 80 else "💪 Možeš i bolje! Pokušaj ponovo!"}

Hvala što koristiš našu platformu!

--
Quiz Platforma Tim
            """
            
            msg = Message(
                subject=subject,
                recipients=[igrac_email],
                body=body,
                sender=os.getenv("MAIL_DEFAULT_SENDER")
            )
            
            mail.send(msg)
            print(f" Email poslat na: {igrac_email}")
            return True
            
        except Exception as e:
            print(f" Greška pri slanju email-a: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
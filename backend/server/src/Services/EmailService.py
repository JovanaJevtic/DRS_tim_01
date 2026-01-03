from flask_mail import Mail, Message
from flask import current_app
from Domain.services.IEmailService import IEmailService 

mail = Mail()

class EmailService(IEmailService): 
    
    def send_role_change_email(self, user_email: str, user_name: str, new_role: str) -> bool:
        """Pošalji email korisniku kada mu se promeni uloga"""
        
        role_names = {
            "IGRAC": "Igrač",
            "MODERATOR": "Moderator", 
            "ADMINISTRATOR": "Administrator"
        }
        
        role_display = role_names.get(new_role, new_role)
        
        subject = f"Promena uloge na Kviz Platformi"
        
        body = f"""
Poštovani/a {user_name},

Vaša uloga na Kviz Platformi je promenjena.

Nova uloga: {role_display}

Srdačan pozdrav,
Kviz Platforma Tim
        """
        
        html = f"""
<html>
    <body style="font-family: Arial, sans-serif; padding: 20px;">
        <h2 style="color: #0ea5e9;">Promena uloge</h2>
        <p>Poštovani/a <strong>{user_name}</strong>,</p>
        <p>Vaša uloga na Kviz Platformi je promenjena.</p>
        <div style="background-color: #f0f9ff; padding: 15px; border-left: 4px solid #0ea5e9; margin: 20px 0;">
            <p style="margin: 0;"><strong>Nova uloga:</strong> {role_display}</p>
        </div>
        <p>Srdačan pozdrav,<br>Kviz Platforma Tim</p>
    </body>
</html>
        """
        
        try:
            msg = Message(
                subject=subject,
                recipients=[user_email],
                body=body,
                html=html
            )
            mail.send(msg)
            print(f"✅ Email poslat na: {user_email}")
            return True
        except Exception as e:
            print(f"❌ Greška pri slanju email-a: {str(e)}")
            return False
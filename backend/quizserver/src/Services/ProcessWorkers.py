import time
import os
from datetime import datetime
from bson import ObjectId

def process_quiz_results_worker(quiz_id, igrac_id, igrac_email, odgovori, vrijeme_utroseno_sekunde):
    """
    Worker funkcija koja se izvršava u POSEBNOM PROCESU.
    Obrađuje rezultate kviza, simulira duže trajanje obrade.
    
    NAPOMENA: Ova funkcija MORA biti na top-level (ne metoda klase)
    kako bi mogla biti pickle-ovana za multiprocessing.
    """
    import sys
    from pymongo import MongoClient
    
    print(f"🔄 [PID {os.getpid()}] Započeta obrada kviza {quiz_id} za igrača {igrac_email}")
    time.sleep(5) 
    
    try:
        # Svaki proces mora da ima svoju MongoDB konekciju
        mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
        db_name = os.getenv("MONGO_DB_NAME", "kviz_db")
        client = MongoClient(mongo_uri)
        db = client[db_name]
        
        quizzes_collection = db["quizzes"]
        results_collection = db["quiz_results"]
        
        # Dohvati kviz
        quiz = quizzes_collection.find_one({"_id": ObjectId(quiz_id)})
        if not quiz:
            print(f" [PID {os.getpid()}] Kviz {quiz_id} nije pronađen")
            client.close()
            return None
        
        # Izračunaj rezultate koristeći zajedničku helper funkciju
        from Services.QuizHelpers import calculate_quiz_results
        
        results = calculate_quiz_results(quiz, odgovori)
        ukupno_bodova = results["ukupno_bodova"]
        maksimalno_bodova = results["maksimalno_bodova"]
        procenat = results["procenat"]
        
        # Sačuvaj rezultat
        result_doc = {
            "quiz_id": quiz_id,
            "quiz_naziv": quiz["naziv"],
            "igrac_id": igrac_id,
            "igrac_email": igrac_email,
            "odgovori": odgovori,
            "ukupno_bodova": ukupno_bodova,
            "maksimalno_bodova": maksimalno_bodova,
            "procenat": procenat,
            "vrijeme_utroseno_sekunde": vrijeme_utroseno_sekunde,
            "created_at": datetime.utcnow()
        }
        
        results_collection.insert_one(result_doc)
        
        print(f" [PID {os.getpid()}] Rezultat sačuvan: {ukupno_bodova}/{maksimalno_bodova} bodova")
        
        client.close()
        
        # Pošalji email (u posebnom procesu)
        _send_email_in_process(
            igrac_email=igrac_email,
            quiz_naziv=quiz["naziv"],
            ukupno_bodova=ukupno_bodova,
            maksimalno_bodova=maksimalno_bodova,
            procenat=procenat,
            vrijeme_utroseno_sekunde=vrijeme_utroseno_sekunde
        )
        
        return {
            "success": True,
            "quiz_id": quiz_id,
            "ukupno_bodova": ukupno_bodova,
            "maksimalno_bodova": maksimalno_bodova,
            "procenat": procenat,
            "processed_by_pid": os.getpid()
        }
        
    except Exception as e:
        print(f" [PID {os.getpid()}] Greška pri obradi: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def _send_email_in_process(igrac_email, quiz_naziv, ukupno_bodova, maksimalno_bodova, procenat, vrijeme_utroseno_sekunde):
    """Šalje email sa rezultatima (poziva se iz worker procesa)"""
    try:
        from flask import Flask
        from flask_mail import Mail, Message
        
        app = Flask(__name__)
        app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER", "smtp.gmail.com")
        app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT", 587))
        app.config["MAIL_USE_TLS"] = True
        app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
        app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
        app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER")
        
        mail = Mail(app)
        
        with app.app_context():
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
                body=body
            )
            
            mail.send(msg)
            print(f" [PID {os.getpid()}] Email poslat na: {igrac_email}")
            
    except Exception as e:
        print(f" [PID {os.getpid()}] Greška pri slanju email-a: {str(e)}")
        import traceback
        traceback.print_exc()


def generate_pdf_report_worker(quiz_id, admin_email):
    """
    Worker funkcija za generisanje PDF izvještaja u POSEBNOM PROCESU.
    """
    print(f"📄 [PID {os.getpid()}] Započeto generisanje PDF izvještaja za kviz {quiz_id}")
    time.sleep(3) 
    
    try:
        from pymongo import MongoClient
        from Services.PdfReportService import PdfReportService
        
        # Konekcija na MongoDB
        mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
        db_name = os.getenv("MONGO_DB_NAME", "kviz_db")
        client = MongoClient(mongo_uri)
        db = client[db_name]
        
        quizzes_collection = db["quizzes"]
        results_collection = db["quiz_results"]
        
        # Dohvati kviz i rezultate
        quiz = quizzes_collection.find_one({"_id": ObjectId(quiz_id)})
        if not quiz:
            print(f" [PID {os.getpid()}] Kviz {quiz_id} nije pronađen")
            client.close()
            return None
        
        results = list(results_collection.find({"quiz_id": quiz_id}))
        
        # Generiši PDF
        pdf_service = PdfReportService()
        pdf_bytes = pdf_service.generate_quiz_report_pdf(quiz, results)
        
        safe_name = str(quiz.get("naziv", "kviz")).strip().replace(" ", "_")
        filename = f"izvjestaj_{safe_name}_{quiz_id}.pdf"
        
        # Pošalji email sa PDF-om
        _send_pdf_email_in_process(admin_email, quiz.get("naziv", "Kviz"), pdf_bytes, filename)
        
        client.close()
        
        print(f" [PID {os.getpid()}] PDF izvještaj generisan i poslat")
        
        return {
            "success": True,
            "quiz_id": quiz_id,
            "processed_by_pid": os.getpid()
        }
        
    except Exception as e:
        print(f" [PID {os.getpid()}] Greška pri generisanju PDF-a: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def _send_pdf_email_in_process(admin_email, quiz_naziv, pdf_bytes, filename):
    """Šalje PDF email iz worker procesa"""
    try:
        from flask import Flask
        from flask_mail import Mail, Message
        
        app = Flask(__name__)
        app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER", "smtp.gmail.com")
        app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT", 587))
        app.config["MAIL_USE_TLS"] = True
        app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
        app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
        app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER")
        
        mail = Mail(app)
        
        with app.app_context():
            subject = f"PDF izvještaj - {quiz_naziv}"
            
            body = f"""Pozdrav,

U prilogu se nalazi PDF izvještaj o rezultatima kviza "{quiz_naziv}".

--
Quiz Platforma Tim
"""
            
            msg = Message(
                subject=subject,
                recipients=[admin_email],
                body=body
            )
            
            msg.attach(filename=filename, content_type="application/pdf", data=pdf_bytes)
            
            mail.send(msg)
            print(f" [PID {os.getpid()}] PDF izvještaj poslat na: {admin_email}")
            
    except Exception as e:
        print(f" [PID {os.getpid()}] Greška pri slanju PDF email-a: {str(e)}")
        import traceback
        traceback.print_exc()
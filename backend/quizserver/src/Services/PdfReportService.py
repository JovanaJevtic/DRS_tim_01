from io import BytesIO
from datetime import datetime
from typing import Any, Dict, List

import sys
print("PDF REPORT PYTHON:", sys.executable)
print("PDF REPORT PATHS:", sys.path)


class PdfReportService:
    """Servis za generisanje PDF izvještaja za kviz.

    Napomena: koristi reportlab (pip install reportlab) ako nije već instaliran.
    """

    def generate_quiz_report_pdf(self, quiz: Dict[str, Any], results: List[Dict[str, Any]]) -> bytes:
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.pdfgen import canvas
        except Exception as e:
            raise RuntimeError(
                "Nedostaje dependency 'reportlab'. Instaliraj: pip install reportlab"
            ) from e

        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        naziv = quiz.get("naziv", "Kviz")
        status = quiz.get("status", "")
        created_at = quiz.get("created_at")

        y = height - 60
        c.setFont("Helvetica-Bold", 16)
        c.drawString(40, y, "Izvještaj o rezultatima kviza")

        y -= 26
        c.setFont("Helvetica", 12)
        c.drawString(40, y, f"Naziv: {naziv}")
        y -= 18
        c.drawString(40, y, f"Status: {status}")
        y -= 18

        if created_at:
            if isinstance(created_at, datetime):
                created_text = created_at.strftime("%Y-%m-%d %H:%M:%S")
            else:
                created_text = str(created_at)
            c.drawString(40, y, f"Kreiran: {created_text}")
            y -= 18

        broj_pokusaja = len(results)
        bodovi = [r.get("ukupno_bodova", 0) for r in results]

        maksimalno_bodova = 0
        try:
            maksimalno_bodova = sum(p.get("bodovi", 0) for p in (quiz.get("pitanja") or []))
        except Exception:
            maksimalno_bodova = 0

        avg_score = (sum(bodovi) / broj_pokusaja) if broj_pokusaja > 0 else 0
        best_score = max(bodovi) if bodovi else 0

        y -= 10
        c.setFont("Helvetica-Bold", 12)
        c.drawString(40, y, "Statistika")
        y -= 18
        c.setFont("Helvetica", 12)
        c.drawString(40, y, f"Broj pokušaja: {broj_pokusaja}")
        y -= 18
        c.drawString(40, y, f"Maksimalno bodova: {maksimalno_bodova}")
        y -= 18
        c.drawString(40, y, f"Prosjecan rezultat: {avg_score:.2f}")
        y -= 18
        c.drawString(40, y, f"Najbolji rezultat: {best_score}")
        y -= 26

        c.setFont("Helvetica-Bold", 12)
        c.drawString(40, y, "Top rezultati")
        y -= 18

        c.setFont("Helvetica-Bold", 10)
        c.drawString(40, y, "#")
        c.drawString(60, y, "Email")
        c.drawString(320, y, "Bodovi")
        c.drawString(380, y, "Vrijeme (s)")
        y -= 14
        c.setFont("Helvetica", 10)

        sorted_results = sorted(
            results,
            key=lambda r: (
                -(r.get("ukupno_bodova") or 0),
                (r.get("vrijeme_utroseno_sekunde") or 0),
            ),
        )

        for idx, r in enumerate(sorted_results[:20], start=1):
            if y < 60:
                c.showPage()
                y = height - 60
                c.setFont("Helvetica-Bold", 12)
                c.drawString(40, y, "Top rezultati (nastavak)")
                y -= 18
                c.setFont("Helvetica", 10)

            email = (r.get("igrac_email") or "-")
            score = r.get("ukupno_bodova")
            time_s = r.get("vrijeme_utroseno_sekunde")

            c.drawString(40, y, str(idx))
            c.drawString(60, y, str(email)[:40])
            c.drawString(320, y, str(score if score is not None else 0))
            c.drawString(380, y, str(time_s if time_s is not None else "-"))
            y -= 14

        c.showPage()
        c.save()

        buffer.seek(0)
        return buffer.read()

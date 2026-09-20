import os
import smtplib
from email.message import EmailMessage
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


def send_pdf_email(to_email: str, pdf_path: str, job_id: str) -> None:
    smtp_host = os.getenv("SMTP_HOST", "")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER", "")
    smtp_password = os.getenv("SMTP_PASSWORD", "")
    smtp_from = os.getenv("SMTP_FROM", smtp_user)
    use_tls = os.getenv("SMTP_USE_TLS", "true").lower() == "true"
    use_ssl = os.getenv("SMTP_USE_SSL", "false").lower() == "true"

    if not smtp_host or not smtp_from:
        raise ValueError("SMTP is not configured. Set SMTP_HOST and SMTP_FROM in .env")

    pdf_file = Path(pdf_path)
    if not pdf_file.is_file() or pdf_file.stat().st_size == 0:
        raise FileNotFoundError("Generated PDF not found")

    message = EmailMessage()
    message["Subject"] = "Your EngiSummary PDF"
    message["From"] = smtp_from
    message["To"] = to_email
    message.set_content(
        "Please find your generated engineering drawing summary PDF attached.\n"
    )
    message.add_attachment(
        pdf_file.read_bytes(),
        maintype="application",
        subtype="pdf",
        filename=f"drawing_summary_{job_id}.pdf",
    )

    if use_ssl:
        with smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=30) as smtp:
            if smtp_user and smtp_password:
                smtp.login(smtp_user, smtp_password)
            smtp.send_message(message)
        return

    with smtplib.SMTP(smtp_host, smtp_port, timeout=30) as smtp:
        if use_tls:
            smtp.starttls()
        if smtp_user and smtp_password:
            smtp.login(smtp_user, smtp_password)
        smtp.send_message(message)
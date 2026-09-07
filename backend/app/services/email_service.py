"""
Email Service
Sends the generated summary PDF as an email attachment via SMTP.
"""

import smtplib
from email.message import EmailMessage
from pathlib import Path
from app.core import logger, settings


def send_pdf_email(to_email: str, pdf_path: str, job_id: str) -> None:
    """
    Send the generated PDF as an attachment to the given address.

    Raises:
        ValueError: if SMTP settings are missing
        Exception: if sending fails
    """
    if not settings.SMTP_HOST or not settings.SMTP_FROM:
        raise ValueError("SMTP is not configured. Set SMTP_HOST and SMTP_FROM in .env")

    pdf_file = Path(pdf_path)
    if not pdf_file.is_file():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    if pdf_file.stat().st_size == 0:
        raise ValueError(f"Generated PDF is empty: {pdf_path}")

    filename = f"drawing_summary_{job_id}.pdf"

    message = EmailMessage()
    message["Subject"] = "Your EngiSummary PDF"
    message["From"] = settings.SMTP_FROM
    message["To"] = to_email
    message.set_content(
        "Please find your generated engineering drawing summary PDF attached.\n\n"
        "This is the same PDF available from the EngiSummary result page.\n"
    )

    pdf_bytes = pdf_file.read_bytes()
    message.add_attachment(
        pdf_bytes,
        maintype="application",
        subtype="pdf",
        filename=filename,
    )

    logger.info(f"Sending PDF email for job {job_id} to {to_email}")

    if settings.SMTP_USE_SSL:
        with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT, timeout=30) as smtp:
            _login_if_needed(smtp)
            smtp.send_message(message)
    else:
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=30) as smtp:
            if settings.SMTP_USE_TLS:
                smtp.starttls()
            _login_if_needed(smtp)
            smtp.send_message(message)

    logger.info(f"PDF email sent for job {job_id} to {to_email}")


def _login_if_needed(smtp: smtplib.SMTP) -> None:
    if settings.SMTP_USER and settings.SMTP_PASSWORD:
        smtp.login(settings.SMTP_USER, settings.SMTP_PASSWORD)

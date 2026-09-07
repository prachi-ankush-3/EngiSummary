"""
Send PDF via Email Route
Emails the same generated summary PDF that is available for download.
"""

import smtplib

from fastapi import APIRouter, Path, HTTPException, status

from app.core import logger
from app.models.response import (
    SendPdfEmailRequest,
    SendPdfEmailResponse,
)
from app.services.job_manager import job_manager
from app.services.email_service import send_pdf_email
from app.utils import file_exists, is_valid_email


router = APIRouter()


@router.post(
    "/send-pdf/{job_id}",
    response_model=SendPdfEmailResponse,
)
async def send_generated_pdf(
    payload: SendPdfEmailRequest,
    job_id: str = Path(..., description="Job ID"),
) -> SendPdfEmailResponse:
    """
    Send the generated summary PDF as an email attachment.

    Uses the same generated PDF file that is available through
    GET /api/download/{job_id}.
    """

    # ---------------------------------------------------------------
    # Validate email
    # ---------------------------------------------------------------

    email = (payload.email or "").strip()

    if not is_valid_email(email):
        return SendPdfEmailResponse(
            success=False,
            error="Please enter a valid email address.",
        )

    logger.info(
        f"Starting PDF email request for job={job_id}, "
        f"recipient={email}"
    )

    try:
        # -----------------------------------------------------------
        # Get job
        # -----------------------------------------------------------

        job = job_manager.get_job(job_id)

        if not job:
            logger.error(f"Job not found: {job_id}")

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job not found",
            )

        logger.info(
            f"Job found: {job_id}, "
            f"status={job.get('status')}"
        )

        # -----------------------------------------------------------
        # Make sure processing is complete
        # -----------------------------------------------------------

        if job.get("status") != "completed":
            logger.error(
                f"Job not completed: {job_id}, "
                f"status={job.get('status')}"
            )

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"Job not completed. "
                    f"Current status: {job.get('status')}"
                ),
            )

        # -----------------------------------------------------------
        # Get generated PDF
        # -----------------------------------------------------------

        output_file = job.get("output_file")

        logger.info(
            f"PDF path for job {job_id}: {output_file}"
        )

        if not output_file:
            logger.error(
                f"No output_file stored for job: {job_id}"
            )

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Output file not found",
            )

        if not file_exists(output_file):
            logger.error(
                f"PDF file does not exist: {output_file}"
            )

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Output file not found",
            )

        # -----------------------------------------------------------
        # Send email
        # -----------------------------------------------------------

        logger.info(
            f"Sending PDF email for job {job_id} "
            f"to {email}"
        )

        send_pdf_email(
            email,
            output_file,
            job_id,
        )

        logger.info(
            f"PDF email sent successfully for job {job_id} "
            f"to {email}"
        )

        # -----------------------------------------------------------
        # Success
        # -----------------------------------------------------------

        return SendPdfEmailResponse(
            success=True,
            message="PDF sent successfully to your email.",
        )

    # ---------------------------------------------------------------
    # HTTP errors
    # ---------------------------------------------------------------

    except HTTPException:
        raise

    # ---------------------------------------------------------------
    # SMTP authentication
    # ---------------------------------------------------------------

    except smtplib.SMTPAuthenticationError as e:
        logger.exception(
            f"SMTP authentication failed for job {job_id}: {e}"
        )

        return SendPdfEmailResponse(
            success=False,
            error=(
                "Email authentication failed. "
                "Please check the SMTP username, password, "
                "and Gmail App Password configuration."
            ),
        )

    # ---------------------------------------------------------------
    # SMTP connection
    # ---------------------------------------------------------------

    except smtplib.SMTPConnectError as e:
        logger.exception(
            f"SMTP connection failed for job {job_id}: {e}"
        )

        return SendPdfEmailResponse(
            success=False,
            error=(
                "Could not connect to the Gmail mail server. "
                "Please try again later."
            ),
        )

    # ---------------------------------------------------------------
    # SMTP recipient
    # ---------------------------------------------------------------

    except smtplib.SMTPRecipientsRefused as e:
        logger.exception(
            f"SMTP recipient refused for job {job_id}: {e}"
        )

        return SendPdfEmailResponse(
            success=False,
            error=(
                "The recipient email address was rejected "
                "by the mail server."
            ),
        )

    # ---------------------------------------------------------------
    # SMTP server disconnected
    # ---------------------------------------------------------------

    except smtplib.SMTPServerDisconnected as e:
        logger.exception(
            f"SMTP server disconnected for job {job_id}: {e}"
        )

        return SendPdfEmailResponse(
            success=False,
            error=(
                "The Gmail mail server disconnected while "
                "sending the email. Please try again."
            ),
        )

    # ---------------------------------------------------------------
    # Other SMTP errors
    # ---------------------------------------------------------------

    except smtplib.SMTPException as e:
        logger.exception(
            f"SMTP error for job {job_id}: {e}"
        )

        return SendPdfEmailResponse(
            success=False,
            error=(
                f"SMTP error while sending email: {str(e)}"
            ),
        )

    # ---------------------------------------------------------------
    # File errors
    # ---------------------------------------------------------------

    except FileNotFoundError as e:
        logger.exception(
            f"PDF file missing for job {job_id}: {e}"
        )

        return SendPdfEmailResponse(
            success=False,
            error=(
                "The generated PDF could not be found. "
                "Please regenerate the summary and try again."
            ),
        )

    # ---------------------------------------------------------------
    # Configuration / content errors
    # ---------------------------------------------------------------

    except ValueError as e:
        logger.exception(
            f"Email configuration/content error "
            f"for job {job_id}: {e}"
        )

        return SendPdfEmailResponse(
            success=False,
            error=f"Email configuration error: {str(e)}",
        )

    # ---------------------------------------------------------------
    # Timeout
    # ---------------------------------------------------------------

    except TimeoutError as e:
        logger.exception(
            f"Email timeout for job {job_id}: {e}"
        )

        return SendPdfEmailResponse(
            success=False,
            error=(
                "The email server took too long to respond. "
                "Please try again."
            ),
        )

    # ---------------------------------------------------------------
    # OS/network errors
    # ---------------------------------------------------------------

    except OSError as e:
        logger.exception(
            f"Network/OS error sending email "
            f"for job {job_id}: {e}"
        )

        return SendPdfEmailResponse(
            success=False,
            error=(
                f"Network error while sending email: {str(e)}"
            ),
        )

    # ---------------------------------------------------------------
    # Unexpected error
    # ---------------------------------------------------------------

    except Exception as e:
        logger.exception(
            f"Unexpected error sending PDF email "
            f"for job {job_id}: {e}"
        )

        return SendPdfEmailResponse(
            success=False,
            error=f"Unexpected email error: {str(e)}",
        )
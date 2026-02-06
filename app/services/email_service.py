import smtplib
from typing import List, Optional
from email.message import EmailMessage

from dotenv import load_dotenv
from app.config import settings
from app.utils.email_util import create_user_verification_email
from app.models.base_response_model import ApiResponse, SuccessMessageResponse

load_dotenv()

print("SMTP_USERNAME =", settings.SMTP_USERNAME)


class EmailService:
    @staticmethod
    def send_reset_password_email(to_email: str, token: str):
        reset_link = f"{settings.FRONTEND_RESET_URL}?token={token}"

        msg = EmailMessage()
        msg["Subject"] = "Reset your password"
        msg["From"] = settings.SMTP_USERNAME

        msg["To"] = to_email
        msg.set_content(
            f"""
                Hello,

                Click the link below to reset your password.
                This link is valid for 15 minutes.

                {reset_link}

                If you did not request this, ignore this email.
            """
        )

        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
            server.send_message(msg)

    @staticmethod
    def send_email(subject: str, message: str, receiver_type: str, to_email: Optional[str] = None):
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = settings.SMTP_USERNAME
        
        # If specific email provided, use it. Otherwise placeholder for group broadcast logic.
        msg["To"] = to_email or "admin@lms-local.com" 

        # If it's a verification style message, we might still want HTML.
        # But for admin compose, plain text is safer/easier.
        msg.set_content(message)

        # For demo purposes, we log the intent. 
        # Integration with real group broadcast would happen here.
        print(f"Sending Email to {receiver_type}: {subject}")

        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
            server.send_message(msg)

        return ApiResponse(
            data=SuccessMessageResponse(message="Email sent successfully")
        )

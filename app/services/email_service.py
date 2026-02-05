import smtplib
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

    def send_email(to_email: str, receiver_type: int):
        msg = EmailMessage()
        msg["Subject"] = "Test Email"
        msg["From"] = settings.SMTP_USERNAME
        msg["To"] = to_email

        if receiver_type == 3:
            url = settings.FRONTEND_MENTOR_URL
        elif receiver_type == 1:
            url = settings.FRONTEND_GUEST_URL
        else:
            raise ValueError("Invalid receiver_type")

        msg.set_content(create_user_verification_email(url), subtype="html")

        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
            server.send_message(msg)

        return ApiResponse(
            data=SuccessMessageResponse(message="Email sent successfully")
        )

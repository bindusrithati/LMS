import smtplib
from email.message import EmailMessage
from app.config import settings

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

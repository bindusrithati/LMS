import smtplib
from typing import List, Optional
from email.message import EmailMessage

from dotenv import load_dotenv
from app.config import settings
from app.utils.email_util import create_user_verification_email, create_general_html_email
from app.models.base_response_model import ApiResponse, SuccessMessageResponse

load_dotenv()

print("SMTP_USERNAME =", settings.SMTP_USERNAME)


from app.connectors.database_connector import get_database
from app.entities.user import User

class EmailService:
    @staticmethod
    def send_reset_password_email(to_email: str, token: str):
        # ... (keep existing implementation for reset password if needed, or update it too - but for now focused on admin email)
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
    def send_email(subject: str, message: str, receiver_type: Optional[str] = None, to_email: Optional[str] = None):
        recipients = []
        
        if to_email:
            recipients.append(to_email)
        else:
            db = get_database()
            try:
                query = db.query(User).filter(User.is_active == True)
                
                if receiver_type and receiver_type.lower() == 'admin':
                    query = query.filter(User.role == 'Admin')
                elif receiver_type and receiver_type.lower() == 'mentor':
                    query = query.filter(User.role == 'Mentor')
                elif receiver_type and receiver_type.lower() == 'student':
                    query = query.filter(User.role == 'Student')
                # If receiver_type is None or 'all', we fetch all active users
                
                users = query.all()
                recipients = [user.email for user in users if user.email]
            finally:
                db.close()

        if not recipients:
             return ApiResponse(
                 data=SuccessMessageResponse(message="No recipients found")
             )

        # Prepare HTML Content
        html_content = create_general_html_email(subject, message)

        # Send emails
        try:
            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                server.starttls()
                server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
                
                for recipient in recipients:
                    try:
                        msg = EmailMessage()
                        msg["Subject"] = subject
                        msg["From"] = settings.SMTP_USERNAME
                        msg["To"] = recipient
                        msg.set_content(html_content, subtype='html') # Send as HTML
                        server.send_message(msg)
                    except Exception as e:
                        print(f"Failed to send email to {recipient}: {e}")
                        
            return ApiResponse(
                data=SuccessMessageResponse(message=f"Emails sent successfully to {len(recipients)} recipients")
            )
        except Exception as e:
            print(f"SMTP Connection Error: {e}")
            raise e


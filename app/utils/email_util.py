def create_user_verification_email(url: str) -> str:
    """
    Create the HTML content for the user verification email.
    """
    return f"""
        <!DOCTYPE html>
        <html>
        <body>
            <div>
                <h1>Verify Your Email Address</h1>
                <p>Hi,</p>
                <p>Thank you for registering. Please click the link below to verify your email address:</p>
                <p>
                    <a href="{url}">Verify Email</a>
                </p>
                <p>If you did not request this, please ignore this email.</p>
                <p>Thank you,<br>Your Company</p>
            </div>
        </body>
        </html>
    """

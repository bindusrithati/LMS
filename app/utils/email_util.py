def create_user_verification_email(url: str) -> str:
    """
    Create the HTML content for the user verification email.
    """
    return f"""
        <!DOCTYPE html>
        <html>
        <body>
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #333;">Verify Your Email Address</h2>
                <p>Hi,</p>
                <p>Thank you for registering. Please click the link below to verify your email address:</p>
                <div style="margin: 25px 0;">
                    <a href="{url}" style="background-color: #4F46E5; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; font-weight: bold;">Verify Email</a>
                </div>
                <p>If you did not request this, please ignore this email.</p>
                <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
                <p style="color: #666; font-size: 12px;">Thank you,<br>LMS Team</p>
            </div>
        </body>
        </html>
    """

import re

def create_general_html_email(subject: str, message: str) -> str:
    """
    Create a general HTML email wrapper for admin messages.
    Converts newlines to <br> and wraps links.
    """
    # First, escape HTML characters to prevent injection (basic)
    import html
    formatted_message = html.escape(message)
    
    # Convert newlines to <br>
    formatted_message = formatted_message.replace('\n', '<br>')
    
    # Auto-linkify URLs
    # Regex to find URLs starting with http:// or https://
    url_pattern = re.compile(r'(https?://[^\s<]+)')
    formatted_message = url_pattern.sub(
        r'<a href="\1" style="color: #4F46E5; text-decoration: underline;" target="_blank">\1</a>', 
        formatted_message
    )
    
    return f"""
        <!DOCTYPE html>
        <html>
        <body style="margin: 0; padding: 0; background-color: #f4f4f5;">
            <div style="font-family: 'Segoe UI', Arial, sans-serif; max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 40px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-top: 20px; margin-bottom: 20px;">
                <div style="border-bottom: 2px solid #f0f0f0; padding-bottom: 20px; margin-bottom: 30px;">
                    <h2 style="color: #1f2937; margin: 0; font-size: 24px;">{subject}</h2>
                </div>
                
                <div style="color: #4b5563; font-size: 16px; line-height: 1.6;">
                    {formatted_message}
                </div>

                <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #f0f0f0; color: #9ca3af; font-size: 14px;">
                    <p style="margin: 0;">Best regards,</p>
                    <p style="margin: 5px 0 0 0; font-weight: 600; color: #6b7280;">LMS Admin Team</p>
                </div>
            </div>
        </body>
        </html>
    """

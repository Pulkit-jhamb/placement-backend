import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

def send_otp_email(recipient_email, otp):
    """
    Send OTP email to the recipient
    
    Args:
        recipient_email: Email address to send OTP to
        otp: The OTP code to send
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        # Email configuration from environment variables
        sender_email = os.getenv("EMAIL_USER")
        sender_password = os.getenv("EMAIL_PASSWORD")
        
        if not sender_email or not sender_password:
            print("⚠️ Email credentials not configured in .env file")
            print(f"🔐 OTP for {recipient_email}: {otp} (Email not sent - using console)")
            return False
        
        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = "Password Reset OTP - Placement Cell"
        message["From"] = sender_email
        message["To"] = recipient_email
        
        # Create HTML content
        html = f"""
        <html>
          <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
              <h2 style="color: #1f2937;">Password Reset Request</h2>
              <p>You have requested to reset your password for your Placement Cell account.</p>
              <p>Your One-Time Password (OTP) is:</p>
              <div style="background-color: #f3f4f6; padding: 20px; text-align: center; border-radius: 8px; margin: 20px 0;">
                <h1 style="color: #1f2937; font-size: 32px; letter-spacing: 8px; margin: 0;">{otp}</h1>
              </div>
              <p><strong>This OTP will expire in 10 minutes.</strong></p>
              <p>If you did not request this password reset, please ignore this email.</p>
              <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 30px 0;">
              <p style="color: #6b7280; font-size: 12px;">
                This is an automated message from Placement Cell. Please do not reply to this email.
              </p>
            </div>
          </body>
        </html>
        """
        
        # Attach HTML content
        part = MIMEText(html, "html")
        message.attach(part)
        
        # Send email using Gmail SMTP
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, message.as_string())
        
        print(f"✅ OTP email sent successfully to {recipient_email}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        print(f"🔐 OTP for {recipient_email}: {otp} (Email failed - using console)")
        return False

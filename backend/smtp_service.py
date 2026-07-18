import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv

load_dotenv()


class SMTPService:
    """
    Simple SMTP email service for testing
    Uses Gmail SMTP with app password (no OAuth needed!)
    """
    
    def __init__(self):
        # SMTP Configuration from environment
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.sender_email = os.getenv("SMTP_EMAIL")
        self.sender_password = os.getenv("SMTP_PASSWORD")
        self.sender_name = os.getenv("SMTP_SENDER_NAME", "Anup Dutta")
        
        if not self.sender_email or not self.sender_password:
            print("⚠️  Warning: SMTP credentials not configured in .env file")
            print("Add SMTP_EMAIL and SMTP_PASSWORD to enable SMTP email sending")
    
    def is_configured(self):
        """Check if SMTP is properly configured"""
        return bool(self.sender_email and self.sender_password)
    
    def send_email(self, to_email, subject, body, attachment_path: str = None):
        """
        Send email via SMTP
        
        Args:
            to_email: Recipient email address
            subject: Email subject line
            body: Email body content (plain text)
            attachment_path: Optional path to a PDF file to attach
            
        Returns:
            dict with success status and message
        """
        if not self.is_configured():
            raise Exception("SMTP not configured. Add SMTP_EMAIL and SMTP_PASSWORD to .env file")
        
        try:
            # Create message — use 'mixed' to support file attachments
            message = MIMEMultipart("mixed")
            message["Subject"] = subject
            message["From"] = f"{self.sender_name} <{self.sender_email}>"
            message["To"] = to_email
            
            # Add body
            text_part = MIMEText(body, "plain")
            message.attach(text_part)
            
            # Attach PDF if provided
            if attachment_path:
                if os.path.exists(attachment_path):
                    try:
                        with open(attachment_path, "rb") as attachment_file:
                            part = MIMEBase("application", "octet-stream")
                            part.set_payload(attachment_file.read())
                        
                        encoders.encode_base64(part)
                        
                        filename = os.path.basename(attachment_path)
                        part.add_header(
                            "Content-Disposition",
                            f"attachment; filename= {filename}",
                        )
                        message.attach(part)
                        print(f"📎 Attached file: {filename}")
                    except Exception as e:
                        print(f"⚠️  Warning: Failed to attach file '{attachment_path}': {e}")
                        print("   Sending email without attachment.")
                else:
                    print(f"⚠️  Warning: Attachment file not found: '{attachment_path}'")
                    print("   Sending email without attachment.")
            
            # Connect to SMTP server
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # Secure connection
                server.login(self.sender_email, self.sender_password)
                
                # Send email
                server.send_message(message)
            
            return {
                "success": True,
                "message": f"Email sent successfully to {to_email}",
                "method": "SMTP"
            }
            
        except smtplib.SMTPAuthenticationError:
            raise Exception("SMTP Authentication failed. Check your email and app password.")
        except smtplib.SMTPException as e:
            raise Exception(f"SMTP error: {str(e)}")
        except Exception as e:
            raise Exception(f"Error sending email: {str(e)}")


if __name__ == "__main__":
    # Test SMTP service
    print("Testing SMTP Service...")
    print("=" * 50)
    
    service = SMTPService()
    
    if service.is_configured():
        print(f"✅ SMTP Server: {service.smtp_server}:{service.smtp_port}")
        print(f"✅ Sender Email: {service.sender_email}")
        print(f"✅ Sender Name: {service.sender_name}")
        print("\nSMTP is configured and ready!")
        
        # Test sending (commented out to avoid accidental sends)
        # result = service.send_email(
        #     to_email="test@example.com",
        #     subject="Test Email",
        #     body="This is a test email from SMTP service"
        # )
        # print(f"\n✅ {result['message']}")
    else:
        print("❌ SMTP not configured")
        print("\nTo configure SMTP, add these to backend/.env:")
        print("=" * 50)
        print("SMTP_EMAIL=your-email@gmail.com")
        print("SMTP_PASSWORD=your-app-password")
        print("SMTP_SENDER_NAME=Your Name")
        print("SMTP_SERVER=smtp.gmail.com")
        print("SMTP_PORT=587")
        print("=" * 50)
        print("\nHow to get Gmail App Password:")
        print("1. Go to: https://myaccount.google.com/apppasswords")
        print("2. Create 'App password' for 'Mail'")
        print("3. Copy the 16-character password")
        print("4. Use it as SMTP_PASSWORD (no spaces)")

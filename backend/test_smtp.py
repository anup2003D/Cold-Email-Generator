"""
Quick SMTP test — run this directly to check if Gmail auth works.
Usage: python test_smtp.py
"""
import smtplib
from dotenv import load_dotenv
import os

load_dotenv()

email    = os.getenv("SMTP_EMAIL")
password = os.getenv("SMTP_PASSWORD")
server   = os.getenv("SMTP_SERVER", "smtp.gmail.com")
port     = int(os.getenv("SMTP_PORT", "587"))

print(f"Email   : {email}")
print(f"Password: {'*' * len(password) if password else 'NOT SET'} ({len(password) if password else 0} chars)")
print(f"Server  : {server}:{port}")
print()

try:
    with smtplib.SMTP(server, port) as s:
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(email, password)
        print("✅ SUCCESS — Gmail SMTP login worked!")
except smtplib.SMTPAuthenticationError as e:
    print(f"❌ AUTH FAILED: {e}")
    print()
    print("Checklist:")
    print("  1. Is 2-Step Verification ON for this Gmail account?")
    print("     → https://myaccount.google.com/security")
    print("  2. Was the App Password generated at:")
    print("     → https://myaccount.google.com/apppasswords")
    print("  3. Did you remove spaces from the 16-char password?")
    print("     e.g. 'abcd efgh ijkl mnop' → 'abcdefghijklmnop'")
except Exception as e:
    print(f"❌ OTHER ERROR: {e}")

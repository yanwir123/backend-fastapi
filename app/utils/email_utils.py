# app/utils/email_utils.py
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from app.config import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, logger

def send_otp_email(to_email: str, otp: str):
    """Kirim email OTP ke pengguna"""
    try:
        msg = MIMEText(f"Your OTP code is: {otp}\nThis code will expire in 10 minutes.")
        msg["Subject"] = "Your Account Verification OTP"
        msg["From"] = SMTP_USER
        msg["To"] = to_email

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
            logger.info(f"📧 OTP email sent successfully to {to_email}")

    except Exception as e:
        logger.error(f"❌ Failed to send OTP email to {to_email}: {e}")


def send_contact_email(name: str, email: str, message: str):
    """
    💌 Mengirim pesan dari form contact ke email admin (misal Gmail kamu)
    """
    admin_email = SMTP_USER  # Kirim ke email kamu sendiri (akun pengirim)
    subject = f"[Contact Form] Pesan dari {name}"
    body = f"""
    📬 Anda menerima pesan baru dari form Contact Website:

    Nama: {name}
    Email: {email}

    Pesan:
    {message}
    """

    msg = MIMEMultipart()
    msg["From"] = SMTP_USER
    msg["To"] = admin_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
            logger.info(f"✅ Contact email sent from {email} ({name})")
    except Exception as e:
        logger.error(f"❌ Failed to send contact email: {e}")
        raise
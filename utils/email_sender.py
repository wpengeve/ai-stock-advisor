import smtplib
import os
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

load_dotenv()

def send_email_with_attachment(to_email, subject, message, file_path):
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    smtp_username = os.getenv("SMTP_USERNAME")
    smtp_password = os.getenv("SMTP_PASSWORD")
    from_email = os.getenv("EMAIL_FROM_ADDRESS")

    if not all([smtp_server, smtp_port, smtp_username, smtp_password, from_email]):
        print("❌ Missing SMTP configuration in .env")
        return False

    try:
        # Create email
        msg = MIMEMultipart()
        msg["From"] = from_email
        msg["To"] = to_email
        msg["Subject"] = subject

        # Body
        msg.attach(MIMEText(message, "plain"))

        # Attachment
        with open(file_path, "rb") as f:
            part = MIMEApplication(f.read(), Name=os.path.basename(file_path))
            part["Content-Disposition"] = f'attachment; filename="{os.path.basename(file_path)}"'
            msg.attach(part)

        # Send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)

        print("✅ Email sent via Elastic Email SMTP")
        return True

    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False
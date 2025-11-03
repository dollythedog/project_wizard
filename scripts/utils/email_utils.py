import os
import smtplib
import markdown
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from dotenv import load_dotenv
from utils.log_utils import log

load_dotenv(dotenv_path="configs/.env")

EMAIL_SERVER = os.getenv("EMAIL_SERVER") or ""
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_USER = os.getenv("EMAIL_USER") or ""
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD") or ""
EMAIL_FROM = os.getenv("EMAIL_FROM") or ""
EMAIL_TO = os.getenv("EMAIL_TO") or EMAIL_FROM

def send_email(subject: str, body_md: str, attachments: list = None, to: list | None = None):
    attachments = attachments or []
    recipients = to or [addr.strip() for addr in (EMAIL_TO or EMAIL_FROM).split(",") if addr.strip()]
    if not EMAIL_FROM or not recipients or not EMAIL_SERVER or not EMAIL_USER or not EMAIL_PASSWORD:
        log("❌ Email config incomplete; check .env", script_name="email_utils")
        return

    body_html = markdown.markdown(body_md)
    msg = MIMEMultipart("alternative")
    msg["From"] = EMAIL_FROM
    msg["To"] = ", ".join(recipients)
    msg["Subject"] = subject
    msg.attach(MIMEText(body_md, "plain"))
    msg.attach(MIMEText(body_html, "html"))

    for filepath in attachments:
        with open(filepath, "rb") as f:
            part = MIMEApplication(f.read(), Name=os.path.basename(filepath))
        part["Content-Disposition"] = f'attachment; filename="{os.path.basename(filepath)}"'
        msg.attach(part)

    try:
        with smtplib.SMTP(EMAIL_SERVER, EMAIL_PORT, timeout=20) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_FROM, recipients, msg.as_string())
        log("✅ Email sent successfully", script_name="email_utils")
    except Exception as e:
        log(f"❌ Email send failed: {e}", script_name="email_utils")
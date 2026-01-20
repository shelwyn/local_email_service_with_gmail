from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, EmailStr
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
API_KEY = os.getenv("EMAIL_API_KEY")


# ---------- Request Schema ----------
class EmailRequest(BaseModel):
    to_email: EmailStr
    subject: str
    body: str  # HTML content


# ---------- Auth Check ----------
def verify_api_key(x_api_key: str):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")


# ---------- Email Sender ----------
def send_html_email(to_email: str, subject: str, html_body: str):
    msg = MIMEMultipart("alternative")
    msg["From"] = GMAIL_USER
    msg["To"] = to_email
    msg["Subject"] = subject

    html_part = MIMEText(html_body, "html")
    msg.attach(html_part)

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(GMAIL_USER, GMAIL_PASSWORD)
        server.send_message(msg)


# ---------- API Endpoint ----------
@app.post("/send-email")
def send_email(
    payload: EmailRequest,
    x_api_key: str = Header(...)
):
    verify_api_key(x_api_key)

    send_html_email(
        to_email=payload.to_email,
        subject=payload.subject,
        html_body=payload.body
    )

    return {
        "status": "success",
        "message": f"Email sent to {payload.to_email}"
    }

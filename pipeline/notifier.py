from email.message import EmailMessage
import datetime
import smtplib
import os

def send_mail(data):
    EMAIL_ADDRESS = os.getenv("EMAIL_USER")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASS")

    # Today's date
    today = datetime.date.today().strftime("%Y-%m-%d")

    # Compose email
    msg = EmailMessage()
    msg["Subject"] = f"Kickbase Recommendations for {today}"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = EMAIL_ADDRESS
    msg.set_content("Hello! Your script executed successfully.")

    # Send email via Gmail SMTP
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()  # Upgrade connection to secure
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

    print("Email sent successfully!")

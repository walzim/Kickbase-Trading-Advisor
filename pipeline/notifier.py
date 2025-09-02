from email.message import EmailMessage
from dotenv import load_dotenv
import datetime
import smtplib
import os

def send_mail(data_df, email):
    """Sends an email with the provided DataFrame as an HTML table."""
    EMAIL_ADDRESS = os.getenv("EMAIL_USER")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASS")

    # Today's date
    today = datetime.date.today().strftime("%d-%m-%Y")

    # Convert data_df to HTML table
    df_html = data_df.to_html(index=False)

    # Metadata for the email
    msg = EmailMessage()
    msg["Subject"] = f"Kickbase: {today}"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = email

    # Set email content 
    msg.set_content("Sorry, results only via html visible.", subtype="plain")
    msg.add_alternative(f"""\
    <html>
    <body>
        <p>Greetings! The available players and their predicted market values for the following day are listed below:</p>
        {df_html}
        <p>Best regards, <br>Your Kickbase Bot</p>
    </body>
    </html>
    """, subtype="html")

    # Send email via Gmail SMTP
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()  # Upgrade connection to secure
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

    print("Email sent successfully!")
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import config


def send_email(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = config.SENDER_EMAIL
    msg['To'] = config.RECIPIENT_EMAIL

    with smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT) as server:
        server.starttls()
        server.login(config.SENDER_EMAIL, config.SENDER_PASSWORD)
        server.send_message(msg)


def main():
    now = datetime.now()
    subject = now.strftime("Reminder %d/%m/%Y %I:%M %p: Claim Amount Pending Since Nov 2025")

    body = f"""
Hi,

This is a reminder regarding the claim amount that has not been received after approval in Nov 2025.

I had already shared the required details again in a new email on 3rd March, including the cancelled cheque and bank statements.
However, I have still not received any update on when the amount will be credited to my account.

I request you to kindly provide a status update and let me know the expected timeline for the payment.

Looking forward to your response.

Requested action:
Please check and process the pending claim amount.

Timestamp: {now.strftime('%Y-%m-%d %H:%M:%S')}

Regards,
Siddhartha
"""

    try:
        send_email(subject, body)
        print(f"Email sent successfully: {subject}")
    except Exception as e:
        print(f"Failed to send email: {e}")


if __name__ == "__main__":
    main()

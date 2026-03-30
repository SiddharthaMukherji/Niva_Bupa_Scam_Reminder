import os
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import config

def get_counter():
    if os.path.exists(config.COUNTER_FILE):
        with open(config.COUNTER_FILE, "r") as f:
            return int(f.read().strip())
    return 0


def update_counter(count):
    with open(config.COUNTER_FILE, "w") as f:
        f.write(str(count))


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
    count = get_counter()

    if count >= config.MAX_REMINDERS:
        print("Max reminders reached. Stopping.")
        return

    count += 1
    update_counter(count)

    subject = f"Reminder {count}/{config.MAX_REMINDERS}: Claim Amount Pending Since Nov 2025"

    body = f"""
Hi,

This is reminder {count} regarding the claim amount that has not been received after approval in Nov 2025.

I had already shared the required details again in a new email on 3rd March, including the cancelled cheque and bank statements.
However, I have still not received any update on when the amount will be credited to my account.

I request you to kindly provide a status update and let me know the expected timeline for the payment.

Looking forward to your response.

Requested action:
Please check and process the pending claim amount.

Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

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

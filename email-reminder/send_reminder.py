import logging
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def normalize_recipients(recipients):
    def normalize(value):
        if not isinstance(value, str):
            raise ValueError("Each recipient must be a string")
        parts = [part.strip() for part in value.replace(";", ",").split(",")]
        return [part for part in parts if part]

    if isinstance(recipients, str):
        parsed = normalize(recipients)
    elif isinstance(recipients, (list, tuple)):
        parsed = []
        for item in recipients:
            parsed.extend(normalize(item))
    else:
        raise ValueError("RECIPIENT_EMAIL must be a string, list, or tuple")

    if not parsed:
        raise ValueError("No valid recipient addresses found in RECIPIENT_EMAIL")

    return parsed


def send_email(subject, body):
    recipients = normalize_recipients(config.RECIPIENT_EMAIL)
    to_header = ", ".join(recipients)

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = config.SENDER_EMAIL
    msg["To"] = to_header

    logging.info("Preparing to send email from %s to %s", config.SENDER_EMAIL, to_header)
    logging.info("Connecting to SMTP server %s:%s", config.SMTP_SERVER, config.SMTP_PORT)

    with smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT) as server:
        server.set_debuglevel(1)
        server.starttls()
        server.login(config.SENDER_EMAIL, config.SENDER_PASSWORD)
        server.send_message(msg, from_addr=config.SENDER_EMAIL, to_addrs=recipients)

    logging.info("Email sent successfully to %s", to_header)


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
    except Exception as e:
        logging.exception("Failed to send email")
        print(f"Failed to send email: {e}")
        raise


if __name__ == "__main__":
    main()

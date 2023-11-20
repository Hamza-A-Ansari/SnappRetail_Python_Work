import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os
from dotenv import load_dotenv
import logging


def send_email(config, subject, body, attachment_path):

    logging.info("\nNow Starting Email process...\n")
    
    # Email configuration
    load_dotenv()
    email_config = config['email_config']
    sender_email = os.getenv('sender_email')
    sender_password = os.getenv('sender_password')
    recipient_email = email_config['recipient_email']
    recipient_email= ", ".join(recipient_email.split(','))
    smtp_server = email_config['smtp_server']
    smtp_port = email_config['smtp_port']

    # Create MIME message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Attach body text
    msg.attach(MIMEText(body, 'plain'))

    # Attach the Excel file
    with open(attachment_path, "rb") as attachment:
        part = MIMEApplication(attachment.read(), Name=attachment_path)
        part['Content-Disposition'] = f'attachment; filename="{attachment_path}"'
        msg.attach(part)

    # Connect to SMTP server and send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        # server.sendmail(sender_email, recipient_email, msg.as_string())
        server.send_message(msg)
        logging.info('Email has been sent, process completed successfully.')


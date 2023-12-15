from Send_Email import send_email
import logging
import os
from dotenv import load_dotenv


def main():
    # Create Log file
    logging.basicConfig(
        filename='app.log',
        filemode='a',
        format='%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
        level=logging.INFO )

    load_dotenv()
    # Sending Email
    email_subject = "Transforming the landscape of retail insights - Aurora Magazine Sept-Oct Feature"
    recipient_email = os.getenv('recipient_email')
    recipient_email_bcc = os.getenv('recipient_email_bcc')

    # Loop to send emails in batches of 50
    for i in range(0, len(recipient_email_bcc), 50):
        batch_bcc_emails = recipient_email_bcc[i:i+50]
        send_email(email_subject, recipient_email, batch_bcc_emails)

    # # Sending Email
    # email_subject = "Transforming the landscape of retail insights - Aurora Magazine Sept-Oct Feature"
    # send_email(email_subject)

if __name__ == "__main__":
    main()
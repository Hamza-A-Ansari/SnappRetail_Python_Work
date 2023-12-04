import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
import os
from dotenv import load_dotenv
import logging


def send_email(subject):

    logging.info("\nStarting Email process...\n")

    # Email configuration
    load_dotenv()
    sender_email = os.getenv('sender_email')
    sender_password = os.getenv('sender_password')
    recipient_email = os.getenv('recipient_email')
    recipient_email_bcc = os.getenv('recipient_email_bcc')
    recipient_email = ", ".join(recipient_email.split(','))
    recipient_email_bcc = ", ".join(recipient_email_bcc.split(','))
    smtp_server = os.getenv('smtp_server')
    smtp_port = os.getenv('smtp_port')

    # Create MIME message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Bcc'] = recipient_email_bcc
    msg['Subject'] = subject

    images = []
    images_path=[i for i in os.listdir('images/')]

    for i in range(len(images_path)):
        image = MIMEImage(open(f'images/{images_path[i]}', 'rb').read(),_subtype="jpg")
        image.add_header('Content-ID','<image{}>'.format(i))
        msg.attach(image)
        images.append(image)


    # Attach the file
    image_body=''
    for i in range(len(images)):
        image_body += '<div style="text-align: center; background-color: #cccccc;">'
        image_body += " "+'<br><img src="cid:image{}" width="600" height="900"></br>'.format(i)
    logging.info("imagebody"+image_body)
    image_body += '<p style="text-align: center;"><strong><span style="font-size: 20px;"><a href="https://snappretail.io/public/newsletter.html">Click to view full Report</a></span></strong></p>'
    text =MIMEText('{}<div style="display: inline-block; text-align: left; width: 56%;"><p style="line-height: 1; color: black;"><br>The newsletter in the email message is the official property of SnappRetail. Choose accurate, system-based insights rather than "claimed" estimations! Our team has harnessed the power of Mircoerp scanned data to unlock invaluable retail insights that will reshape the retail industry. Discover the game-changing trends, actionable insights, and market dynamics shaping Pakistan\'s retail landscape in our newsletter.</br></p> </div>'.format(image_body), 'html')

    image_body += '</div>'
    msg.attach(text)


    # Connect to SMTP server and send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        

        server.send_message(msg)
        logging.info('Email has been sent, process completed successfully.')


def main():
    # Create Log file
    logging.basicConfig(
        filename='app.log',
        filemode='a',
        format='%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
        level=logging.INFO )

    # Sending Email
    email_subject = "Revolutionizing Retail Insights in Pakistan - Quarterly Newsletter Q2"
    send_email(email_subject)

if __name__ == "__main__":
    main()
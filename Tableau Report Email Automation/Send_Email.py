import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
import os
import logging
from config import *


def send_email(subject, image_path, pdf_path):

    logging.info("\nStarting Email process...\n")

    # Create MIME message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    # msg['Bcc'] = recipient_email_bcc
    msg['Subject'] = subject

    images = []
    images_path=[i for i in os.listdir(image_path.split('/')[0])]

    image_name = image_path.split('/')[-1]
    for i in range(len(images_path)):
        image = MIMEImage(open(f'images/{images_path[i]}', 'rb').read(),_subtype="png")
        image.add_header('Content-ID','<image{}>'.format(i))
        image.add_header('Content-Disposition', f'attachment; filename={image_name}')
        msg.attach(image)
        images.append(image)


    # Attach the file
    image_body=''
    for i in range(len(images)):
        image_body += '<div style="text-align: center; background-color: #cccccc;">'
        image_body += " "+'<br><img src="cid:image{}" width="600" height="900"></br>'.format(i)
    logging.info("imagebody"+image_body)
    text =MIMEText('Please Find Attached the Financial Transaction Dashboard{}'.format(image_body), 'html')


    # image_body += '</div>'
    msg.attach(text)


    with open(pdf_path,'rb') as f:
        #logging.info(pdf_path)
        attach = MIMEApplication(f.read(),_subtype="pdf")
        attach.add_header('Content-Disposition','attachment',filename=str(pdf_path.split('/')[-1]))
        msg.attach(attach)


    # Connect to SMTP server and send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        
        server.send_message(msg)

    logging.info('Email has been sent.')

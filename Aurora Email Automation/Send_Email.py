import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
import os
from dotenv import load_dotenv
import logging
from time import sleep


def send_email(subject, recipient_email, recipient_email_bcc):

    logging.info("\nStarting Email process...\n")

    # Email configuration
    load_dotenv()
    sender_email = os.getenv('sender_email')
    sender_password = os.getenv('sender_password')
    
    
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

    image_name = 'The SnappRetail Story'
    for i in range(len(images_path)):
        image = MIMEImage(open(f'images/{images_path[i]}', 'rb').read(),_subtype="jpg")
        image.add_header('Content-ID','<image{}>'.format(i))
        image.add_header('Content-Disposition', f'attachment; filename={image_name}')
        msg.attach(image)
        images.append(image)


    # Attach the file
    image_body=''
    for i in range(len(images)):
        image_body += '<div style="text-align: center; background-color: #cccccc;">'
        image_body += " "+'<br><img src="cid:image{}" width="600" height="1000"></br>'.format(i)
    logging.info("imagebody"+image_body)
    image_body += '<p style="text-align: center;"><strong><span style="font-size: 20px;"><a href="https://aurora.dawn.com/news/1144933/the-snappretail-story">Click to view complete article</a></span></strong></p>'
    text =MIMEText('{}<div style="display: inline-block; text-align: left; width: 56%;"><p style="line-height: 1; color: black;"><br>The Article in the email message is the official property of SnappRetail & Dawn News. Choose accurate, system-based insights rather than "claimed" estimations! Our team has harnessed the power of Mirco-erp scanned data to unlock invaluable retail insights that will reshape the retail industry. Discover the game-changing trends, actionable insights, and market dynamics shaping Pakistan\'s retail landscape in this article.</br></p> </div>'.format(image_body), 'html')

    image_body += '</div>'
    msg.attach(text)

    pdf_path = 'New Complete PDF AU Sept-Oct-17-102023-.pdf'
    with open(pdf_path,'rb') as f:
        #logging.info(pdf_path)
        attach = MIMEApplication(f.read(),_subtype="pdf")
        attach.add_header('Content-Disposition','attachment',filename=str(pdf_path))
        msg.attach(attach)


    # Connect to SMTP server and send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        

        server.send_message(msg)
        server.quit()
        sleep(3)
        
        #server.sendmail(sender_email, [msg['To']] + msg['Bcc'].split(', '), msg.as_string())

        logging.info('Email has been sent, process completed successfully.')


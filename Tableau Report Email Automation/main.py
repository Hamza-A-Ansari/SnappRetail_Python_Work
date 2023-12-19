from config import *
import logging
from configuration import *
from Load import Tableau_report
from Send_Email import send_email
from Delete_File import delete_image_pdf


def main():
    # Create Log file
    logging.basicConfig(
        filename='app.log',
        filemode='a',
        format='%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
        level=logging.INFO )
    
    # Download Tableau report
    image_path, pdf_path = Tableau_report()

    # Sending Email
    email_subject = "Financial Transaction Dashboard"
    send_email(email_subject, image_path, pdf_path)

    # Delete image
    delete_image_pdf(image_path, pdf_path)

if __name__ == "__main__":
    main()
import os
import logging

def delete_image_pdf(file_path, pdf_path):

    # Delete Image
    logging.info(f'Now deleting image.')
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            logging.info("Image deleted successfully.")
        except Exception as e:
           logging.info("Error deleting your image.")
    else:
        logging.info("Image does not exist in the specified folder.")

    # Delete PDF
    logging.info(f'Now deleting PDF.')
    if os.path.exists(pdf_path):
        try:
            os.remove(pdf_path)
            logging.info("PDF deleted successfully.")
        except Exception as e:
            logging.info("Error deleting your PDF.")
    else:
        logging.info("PDF does not exist in the specified folder.")

    logging.info("Process completed successfully")

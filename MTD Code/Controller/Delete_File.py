import os
import logging

def delete_excel_file(file_path):
    
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            logging.info("Excel File deleted successfully.")
        except Exception as e:
           logging.info("Error deleting your file.")
    else:
        logging.info("File does not exist in the specified folder.")

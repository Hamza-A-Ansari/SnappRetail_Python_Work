import configparser
from Load_Data import Load_Data
from Send_Email import send_email
import socket
from datetime import date
from Transformation import Transformation
from Delete_File import delete_excel_file
import logging

def main():
    logging.basicConfig(
        # filename=os.getenv('LOG_FILE'),
        filename='app.log',
        filemode='a',
        format='%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
        level=logging.INFO )

    # Read the configuration from the config file
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Loading data 
    prodreplica_data, oracle_data = Load_Data(config=config)

    today = date.today()
    output_filename = f'Inactive_Store/Inactive_Stores-Last_Visit_{today}.xlsx'

    # Manipulation of data
    Transformation(prodreplica_data, oracle_data, output_filename)

    # Send email        
    email_subject = "Daily Report: Inactive Stores - Last Visit"
    email_body = "Please find attached the daily report for last visit of inactive stores."
    socket.getaddrinfo('localhost', 8080)
    send_email(config, email_subject, email_body, output_filename)

    # Delete Excel File
    delete_excel_file(output_filename)

if __name__ == "__main__":
    main()

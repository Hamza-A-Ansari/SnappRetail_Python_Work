import configparser
from Load_Data import Load_Data
from Send_Email import send_email
from Delete_File import delete_excel_file
from Transformation import Transformation
import socket
from datetime import date
import logging

def main():
    # Create Log file
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
    today_data, lastday_data, sevenday_data, mtd_data = Load_Data(config=config)

    today = date.today()
    output_filename = f'Inactive_Stores_{today}.xlsx'

    # Transformation of data
    Transformation(today_data, lastday_data, sevenday_data, mtd_data, output_filename)

    # Send email        
    email_subject = "Daily Report: Inactive Stores"
    email_body = "Please find attached the daily report for inactive stores."
    socket.getaddrinfo('localhost', 8080)
    send_email(config, email_subject, email_body, output_filename)

    # Delete Excel File
    delete_excel_file(output_filename)

if __name__ == "__main__":
    main()

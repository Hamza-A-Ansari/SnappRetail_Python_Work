import configparser
from Load_Data import Load_Data
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
    today_data, column_names = Load_Data(config=config)

    today = date.today()
    output_filename = f'sql_query_v6_{today}.xlsx'

    # Transformation of data
    Transformation(today_data, output_filename, column_names)


if __name__ == "__main__":
    main()

import configparser
from Transform import Transformation
from datetime import datetime
import logging
from Load import load
from Delete_File import delete_excel_file

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
    logging.info("Config File imported.")

    cur_dt = datetime.now()
    cur_dt = cur_dt.strftime("%Y%m%d%H%M%S")
    output_filename = f'Products_Backup-{cur_dt}.csv'

    # Transformation of data
    df = Transformation(config, output_filename)
    
    file_url, url = load(output_filename)
    print(file_url)
    print(url)
    
    # Delete Excel File
    delete_excel_file(output_filename)

if __name__ == "__main__":
    main()

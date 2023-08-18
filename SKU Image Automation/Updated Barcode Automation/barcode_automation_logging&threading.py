from csv import reader
from time import sleep, time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import urllib.request
import re
from selenium.webdriver.chrome.service import Service
import logging
import requests
import concurrent.futures
import configparser
import signal

# CREATE OBJECT
config = configparser.ConfigParser()

config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))



# load environment variables from .env file
# load_dotenv()

#logging basic config
logging.basicConfig(
    filename=config['DEFAULT']['LOG_FILE'],
    filemode='a', 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO 
)

# Set the path to the web driver
chrome_path = config['DEFAULT']['CHROME_PATH']

def dl_jpg(url, file_path, file_name):

    full_path = os.path.join(file_path, file_name + '.jpg')
    urllib.request.urlretrieve(url, full_path)
    return full_path

def download_image(barcode, product, make_folder):
    
    try:
        s = Service(chrome_path)
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = webdriver.Chrome(service=s, options=options)
        
        # Navigate to Google Images
        driver.get("https://www.google.com/imghp")

        # Find the search box element and enter the barcode
        search_box = driver.find_element("name", "q")
        search_box.send_keys(barcode)
        search_box.send_keys(Keys.RETURN)

        # Find the first image result and click on it
        first_image = driver.find_element('xpath','//*[@id="islrg"]/div[1]/div[' + str(1) + ']/a[1]/div[1]/img')
        first_image.click()

        # Get the image URL and download the image
        img_url = driver.find_element('xpath','//*[@id="islrg"]/div[1]/div[' + str(1) + ']/a[1]/div[1]/img').get_attribute("src")
        sleep(2)

        # Close the browser
        driver.close()

        # Create file name
        file_name = product +" ("+barcode+")"

        # check if the folder is present or not
        make_folder = os.path.join(os.getcwd(), make_folder)

        # if folder not exist, create a new one
        if not os.path.exists(make_folder):
            os.makedirs(make_folder)        

        # Download the image
        image_path = dl_jpg(img_url, make_folder, file_name)

        # log the downloaded image
        logging.info(image_path)
        
    except Exception as e:
        return barcode
        # log the exception along with the image name and path
        logging.error('Error downloading image: Error message : %s. Image name: %s . Image path: %s', e ,file_name,make_folder)
        
       

# Handle keyboard interrupt signal
def keyboard_interrupt_handler(signal, frame):
    logging.error('KeyboardInterrupt (ID: {}) has been caught. Stopping the script...'.format(signal))
    exit(0)

# Assign the keyboard interrupt handler to SIGINT
signal.signal(signal.SIGINT, keyboard_interrupt_handler)

if __name__ == '__main__':
    try:
        sheet_name = config['DEFAULT']['SHEET_NAME']
        print(sheet_name)
        data = list(reader(open(sheet_name)))
        image_not_download=[]

        for i in data[0]:
            if re.search("[Bb][Aa][Rr][^/s]*[Cc][Oo][Dd][Ee]",i):
                index = data[0].index(i)
            if i=="NAME BY SHOPKEEPER":
                index2 = data[0].index(i)

        # Read values from config file
        # create a list of barcodes and products to download images for
        start_index = int(config['DEFAULT']['START_INDEX'])
        end_index = int(config['DEFAULT']['END_INDEX'])
        product_start_index = int(config['DEFAULT']['PRODUCT_START_INDEX'])
        product_end_index = int(config['DEFAULT']['PRODUCT_END_INDEX'])

        barcodes = [i[index] for i in data[start_index:end_index]]
        products = [i[index2] for i in data[product_start_index:product_end_index]]


        make_folder = config['DEFAULT']['FOLDER_NAME']

        thread_num = int(config['DEFAULT']['THREAD_NUMBERS'])

        with concurrent.futures.ThreadPoolExecutor(max_workers=thread_num) as executor:
            for barcode, product in zip(barcodes, products):
                if (executor.submit(download_image, barcode, product, make_folder).result())!='NoneType':
                    image_not_download.append(executor.submit(download_image, barcode, product, make_folder).result())
        print(image_not_download)
                
    except Exception as e:
        logging.error('Error downloading images: %s', e)

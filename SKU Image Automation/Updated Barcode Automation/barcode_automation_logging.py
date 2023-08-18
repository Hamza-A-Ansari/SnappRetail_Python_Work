from csv import reader
import this
from time import sleep, time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import urllib.request
import re
from selenium.webdriver.chrome.service import Service
import logging
import requests
# from selenium.common.exceptions import NoSuchElementException
from dotenv import load_dotenv

# load environment variables from .env file
load_dotenv()

#logging basic config
logging.basicConfig(
    filename=os.getenv('LOG_FILE'),
    filemode='a', 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO 
)



# Set the path to the web driver
chrome_path = os.getenv('CHROME_PATH')

# Input file name and find index of barcode and product name
# File = input("Enter the file name in csv format: ")
def dl_jpg(url, file_path, file_name):

    full_path = os.path.join(file_path, file_name + '.jpg')
    urllib.request.urlretrieve(url, full_path)
    # logging.info(full_path)
    return full_path


    

try:
    sheet_name = os.getenv('SHEET_NAME')
    data = list(reader(open(sheet_name)))


    for i in data[0]:
        if re.search("[Bb][Aa][Rr][^/s]*[Cc][Oo][Dd][Ee]",i):
            index = data[0].index(i)
            
    #       if re.search(".[^/s][Nn][Aa][Mm][Ee].[^/s].*",i):
        if i=="NAME BY SHOPKEEPER":
            index2 = data[0].index(i)

    # start from 
    for i in data[2900:3000]:
        barcode = i[index]
        product = i[index2]
        product = product.replace("."," ").replace("#"," ").replace("*"," ").replace("?"," ").replace("."," ").replace("/","").replace("@"," ")
    # Create a new Chrome browser instance
        
        s=Service(chrome_path)
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = webdriver.Chrome(service=s, options=options)
        # driver = webdriver.Chrome(service=s)
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


        # file_name = 'New image'
        file_name = product +" ("+barcode+")"

        # check if the folder is present or not
        folder_name = os.getenv('FOLDER_NAME')
        make_folder = os.path.join(os.getcwd(), folder_name)

        # if folder not exist, create a new one
        if not os.path.exists(make_folder):
            os.makedirs(make_folder)        
        
        
        image_path = dl_jpg(img_url, make_folder, file_name)

        # log the downloaded image
        logging.info(image_path)
        
        

except Exception as e:
    #   log the exception along with the image name and path
    logging.error('Error downloading image: Error message : %s. Image name: %s . Image path: %s', e ,file_name,make_folder)
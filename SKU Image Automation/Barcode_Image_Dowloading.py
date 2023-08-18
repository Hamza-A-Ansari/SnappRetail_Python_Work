from csv import reader
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import urllib.request
import re
# from selenium.common.exceptions import NoSuchElementException

# Set the path to the web driver
chrome_path = r"chromedriver.exe"

# Input file name and find index of barcode and product name
# File = input("Enter the file name in csv format: ")
data = list(reader(open("Hamza Master.csv")))


for i in data[0]:
    if re.search("[Bb][Aa][Rr][^/s]*[Cc][Oo][Dd][Ee]",i):
        index = data[0].index(i)
        
#     if re.search(".[^/s][Nn][Aa][Mm][Ee].[^/s].*",i):
    if i=="NAME BY SHOPKEEPER":
        index2 = data[0].index(i)
        
def dl_jpg(url,file_path,file_name):
        full_path = file_path+file_name + '.jpg'
        urllib.request.urlretrieve(url,full_path)


# start from 
for i in data[3962:4000]:
    barcode = i[index]
    product = i[index2]
    product = product.replace("."," ").replace("#"," ").replace("*"," ").replace("?"," ").replace("."," ").replace("/","").replace("@"," ")
# Create a new Chrome browser instance
    driver = webdriver.Chrome(chrome_path)
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
    ##os.system("wget " + img_url)

    # To Save the image
    
    url = img_url
    # file_name = 'New image'
    file_name = product +" ("+barcode+")"

    dl_jpg(url,"Hamza_images/",file_name)
    print(product)

    # Close the browser
    driver.close()
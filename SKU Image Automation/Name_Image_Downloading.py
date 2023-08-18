from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import urllib.request

# Set the path to the web driver
chrome_path = r"chromedriver.exe"

def dl_jpg(url,file_path,file_name):
    full_path = file_path + file_name + '.png'
    urllib.request.urlretrieve(url, full_path)


filename = list(os.listdir("Wrong images_v2"))
st = int(input("Enter index to start with: "))
for ind, i in enumerate(filename[st:], st):
    s = list(i.split("("))
    p_name = s[0]
    
    # Create a new Chrome browser instance
    driver = webdriver.Chrome(chrome_path)
    
    # Navigate to Google Images
    driver.get("https://www.google.com/imghp")
    
    # Find the search box element and enter the Product name
    search_box = driver.find_element("name", "q")
    search_box.send_keys(p_name)
    search_box.send_keys(Keys.RETURN)
    
    # Find the first image result and click on it
    first_image = driver.find_element('xpath','//*[@id="islrg"]/div[1]/div[' + str(1) + ']/a[1]/div[1]/img')
    first_image.click()
    
    # Get the image URL and download the image
    img_url = driver.find_element('xpath','//*[@id="islrg"]/div[1]/div[' + str(1) + ']/a[1]/div[1]/img').get_attribute("src")
    
    # To Save the image

    url = img_url
    file_name = p_name
    
    dl_jpg(url,"Wrong_v2 corrected/", file_name)
    
    print(ind, p_name)

    # Close the browser
    driver.close()
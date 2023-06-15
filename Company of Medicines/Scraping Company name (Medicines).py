import pandas as pd
import requests
from time import sleep
from bs4 import BeautifulSoup
from Levenshtein import distance as lev

df = pd.read_excel('Medicine_1798_Final.xlsx')

medicines = list(df['Productname'])
with requests.Session() as session:
    for ind, medicine in enumerate(medicines):
        medicine = str(medicine)
        url = f"https://dawaai.pk/search/index?search={medicine}"

        payload={}
        headers = {
        'Cookie': 'ci_session=se5ndh8br4u71l0hik5r60qafjmu6uni'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        print("Response")

        soup = BeautifulSoup(response.content, 'html.parser')

        try:
            brand__info = soup.find('div', class_='content card-body')
            print("Fetched")

            lis = []
            for div in brand__info.find_all('a'):
                div = div.text.strip()
                lis.append(div)
            med_name = lis[0].split(" ")[0]
            com_name = lis[1]
            orig_med_name = medicine.split(" ")[0]
            
            if lev(orig_med_name, med_name) <= 1:
                df.loc[ind, 'Company'] = com_name
            sleep(3)
            
        except AttributeError:
            continue
            sleep(3)

df.to_excel("Testing_v1.xlsx")

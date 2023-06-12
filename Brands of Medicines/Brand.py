import pandas as pd
import re

df2 = pd.read_excel('Medicine_Base_v2.xlsx')

medicines = list(df2['Productname'])

for ind, med in enumerate(medicines):
    drops = re.findall(r'([A-z ]+[-]?[A-z ]*)\s?[Dd][Rr][Oo][Pp][Ss]?', med)
    if drops:
        df2.loc[ind, "Brand"] = drops[0]
        
    char = re.findall(r'(^[A-z]\s?[-]?\s?[A-z]*$)', med)
    if char:
        df2.loc[ind, "Brand"] = char[0]
        
    char_num = re.findall(r'(^[A-z]+)\s?[-]?\s?\d+[/]?\d*\s?[A-z]*$', med)
    if char_num:
        df2.loc[ind, "Brand"] = char_num[0]
    
    reg = re.findall(r'^([A-z]+\s?[-]?[A-z ]*)', med)
    if reg:
        df3.loc[ind, "Brand"] = reg[0]
        
df2.to_excel('Medicines_test_v3.xlsx', index=False)
import pandas as pd
import re

df = pd.read_excel("Medicine_1804.xlsx")

medicines = list(df['Productname'])
medicines

medicines = list(df['Productname'])
for ind, med in enumerate(medicines):
    med = str(med)
    
    syrup = re.findall(r'([A-z ]+[-]?[A-z]*\d*[+]?)\s?[Ss][Yy][Rr]?[Uu]?[Pp]', med)
    if syrup:
        df.loc[ind, "Brand"] = syrup[0]
        
    mg = re.findall(r'([A-z ]+[-]?[A-z]*)[.]?\s?\d*[/]?[.]?\d+\s?[Mm][Gg]', med)
    if mg:
        df.loc[ind, "Brand"] = mg[0]
    
    tablet = re.findall(r'([A-z ]+[-]?[A-z]*)\s?\d*[/]?[.]?\d*\s?[Mm]?[Gg]?\s?\d*\s?[Tt][Aa][Bb][Ll]?[Ee]?[Tt]?', med)
    if tablet:
        df.loc[ind, "Brand"] = tablet[0]
    
    injection = re.findall(r'^([A-z]+)\s?\d*\s?[Mm]?[Gg]?\s?[Ii][Nn][Jj][Ee]?[Cc]?[Tt]?[Ii]?[Oo]?[Nn]?', med)
    if injection:
        df.loc[ind, "Brand"] = injection[0]
        
df.to_excel('Medicines Brand set.xlsx', index=False)


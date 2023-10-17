import pandas as pd
from Levenshtein import distance as lev
import string
from tqdm import tqdm

df1 = pd.read_excel('CB_MD-2023-05-11.xlsx')
df2 = pd.read_excel('SKUs for testing.xlsx')

comp_list = list(df1['COMPANY'])
brand_list = list(df1['BRAND'])
sku_name = list(df2['SKU NAME'])
sp = string.punctuation

for ind1, name in enumerate(tqdm(sku_name)):
    name = str(name)
    name = name.lower()
    for punc in sp:
        if punc in name:
            name = name.replace(punc, " ")
    sp_name = name.split()
    
    for ind2, brand in enumerate(brand_list):
        brand = str(brand)
        brand = brand.lower()
        sp_brand = brand.split()
        
        outer = []
        for sin_sp_brand in sp_brand:
            inner = []
            for sin_sp_name in sp_name:
                in_score = lev(sin_sp_brand, sin_sp_name)
                inner.append(in_score)
                
            min_inner = min(inner)
            outer.append(min_inner)
            
        sum_of_outer = sum(outer)
        if sum_of_outer == 0:
            company = comp_list[ind2]
            brand = brand_list[ind2]
            df2.loc[ind1, 'COMPANY'] = company
            df2.loc[ind1, 'BRAND'] = brand
df2.to_excel('testing_v1.xlsx', index = False)
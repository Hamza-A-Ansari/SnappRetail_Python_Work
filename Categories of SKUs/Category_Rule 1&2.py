import pandas as pd
import re
from Levenshtein import distance as lev
from tqdm import tqdm
import string

df1 = pd.read_excel('Category Rule 1.xlsx')
df2 = pd.read_excel('test 23 BC file.xlsx')
df3 = pd.read_excel('SKUs for testing_v1.xlsx')

r1_supcat_list = list(df1['SUPER CATEGORY'])
r1_cat_list = list(df1['CATEGORY'])
r1_subcat_list = list(df1['SUB CATEGORY'])

r2_supcat_list = list(df2['SUPER CATEGORY'])
r2_cat_list = list(df2['CATEGORY'])
r2_subcat_list = list(df2['SUB CATEGORY'])

md_name = list(df2['NAME BY SHOPKEEPER'])
sku_name = list(df3['SKU NAME'])

for ind1, name in enumerate(tqdm(sku_name)):
    name = str(name)
    name = name.lower()
    sp = string.punctuation
    for punc in sp:
        if punc in name:
            name = name.replace(punc, " ")
    sp_name = name.split(" ")
    
#   Rule # 1 
    for ind2, subcat in enumerate(r1_subcat_list):
        subcat = str(subcat)
        subcat = subcat.lower()
        for punc in sp:
            if punc in subcat:
                subcat = subcat.replace(punc, " ")
        sp_subcat = subcat.split(" ")
        
        outer = []
        for sin_sp_subcat in sp_subcat:
            inner = []
            for sin_sp_name in sp_name:
                in_score = lev(sin_sp_subcat, sin_sp_name)
                inner.append(in_score)
    
            min_inner = min(inner)
            outer.append(min_inner)
            
        sum_of_outer = sum(outer)
        if sum_of_outer == 0:
            sup_cat = r1_supcat_list[ind2]
            cat = r1_cat_list[ind2]
            sub_cat = r1_subcat_list[ind2]
            df3.loc[ind1, 'SUPER CATEGORY'] = sup_cat
            df3.loc[ind1, 'CATEGORY'] = cat
            df3.loc[ind1, 'SUB CATEGORY'] = sub_cat
            
        else:
#           Rule # 2
            score_of_sku = []
            for ind3, md in enumerate(md_name):
                md = str(md)
                md = md.lower()
                for punc in sp:
                    if punc in md:
                        md = md.replace(punc, " ")
                sp_md = md.split(" ")

                outer = []
                for sin_sp_name in sp_name:
                    inner = []
                    for sin_sp_md in sp_md:
                        in_score = lev(sin_sp_md, sin_sp_name)
                        inner.append(in_score)

                    min_inner = min(inner)
                    outer.append(min_inner)

                sum_of_outer = sum(outer)
                len_of_outer = len(outer)
                avg_of_outer = sum_of_outer / len_of_outer
                score_of_sku.append(avg_of_outer)

            min_score = min(score_of_sku)
            index = score_of_sku.index(min_score)

            sup_cat = r2_supcat_list[index]
            cat = r2_cat_list[index]
            sub_cat = r2_subcat_list[index]
            df3.loc[ind1, 'SUPER CATEGORY'] = sup_cat
            df3.loc[ind1, 'CATEGORY'] = cat
            df3.loc[ind1, 'SUB CATEGORY'] = sub_cat

df3.to_excel('testing_v1.xlsx', index = False)
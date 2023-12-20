import pandas as pd
import re
from Levenshtein import distance as lev
import string
from tqdm import tqdm
import json
import sys

print("Reading your config File")
print()
with open("config.json") as f:
    data = json.load(f)

try:
    df = pd.read_excel(data["SKU File you want to clean"], sheet_name = data["SKU File sheet name"])
    cb_df = pd.read_excel(data["Company Brand Master File"])
    cat_r1_df = pd.read_excel(data["Category Rule1 File"])
    cat_r2_df = pd.read_excel(data["Barcoded SKU Master Data File"])
except:
    print("Error in loading your file")
    print("Make sure your file name is correct with valid extension of excel (.xlsx)")
    sys.exit(0)


try:
    original_name_list = list(df[data["SKU File Column name"]])
except:
    print("Your SKU file column name is incorrect")
    sys.exit(0)

comp_list = list(cb_df['COMPANY'])
brand_list = list(cb_df['BRAND'])

r1_supcat_list = list(cat_r1_df['SUPER CATEGORY'])
r1_cat_list = list(cat_r1_df['CATEGORY'])
r1_subcat_list = list(cat_r1_df['SUB CATEGORY'])

r2_supcat_list = list(cat_r2_df['SUPER CATEGORY'])
r2_cat_list = list(cat_r2_df['CATEGORY'])
r2_subcat_list = list(cat_r2_df['SUB CATEGORY'])
r2_pack_list= list(cat_r2_df['PACKAGING'])
md_name = list(cat_r2_df['NAME BY SHOPKEEPER'])

sp = ['!', '"', '#', '$', '%', "'", '(', ')', '*', '+', ',', '-', '.', '/',
     ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}','~']

print("Imported all your files from config successfuly")
print()
print("Now Started Cleaning")
print()

def Data_Cleaning(df):

    for o_ind, o_name in enumerate(tqdm(original_name_list)):
        o_name = str(o_name)
        
        # Size and Measurement Type Code
        kg = re.findall(r'([\d+]?[/.]?\d+)\s?[-]?\s?[Kk][Gg]', o_name)
        if kg:
            df.loc[o_ind, "SIZE"] = kg[0]
            df.loc[o_ind, "MEASUREMENT TYPE"] = "KG"

        gm = re.findall(r'([\d+]?[/.]?\d+)\s?[-]?\s?[Gg][Rr]?[Aa]?[Mm]?', o_name)
        if gm:
            df.loc[o_ind, "SIZE"] = gm[0]
            df.loc[o_ind, "MEASUREMENT TYPE"] = "GM"

        ltr = re.findall(r'([\d+]?[/.]?\d+)\s?[Ll][Ii]?[Ee]?[Tt]?[Ee]?[Rr]?[Ee]?[Ss]?', o_name)
        if ltr:
            df.loc[o_ind, "SIZE"] = ltr[0]
            df.loc[o_ind, "MEASUREMENT TYPE"] = "LITRE"

        ml = re.findall(r'([\d+]?[/.]?\d+)\s?[Mm][Ll]', o_name)
        if ml:
            df.loc[o_ind, "SIZE"] = ml[0]
            df.loc[o_ind, "MEASUREMENT TYPE"] = "ML"

        dzn = re.findall(r'([\d+]?[/.]?\d+)\s?[Dd][Aa]?[Oo]?[Rr]?[Zz][Ee]?[Oo]?[Nn]?', o_name)
        if dzn:
            df.loc[o_ind, "SIZE"] = dzn[0]
            df.loc[o_ind, "MEASUREMENT TYPE"] = "UNITS"

        pcs = re.findall(r'([\d+]?[/.]?\d+)\s?[Pp][Ii]?[Ee]?[Cc]?[Ii]?[Ee]?[Ss]?', o_name)
        if pcs:
            df.loc[o_ind, "SIZE"] = pcs[0]
            df.loc[o_ind, "MEASUREMENT TYPE"] = "UNITS"
        
        o_name = o_name.lower()
        for punc in sp:
            if punc in o_name:
                o_name = o_name.replace(punc, " ")
        sp_name = o_name.split()
        
        # Company and Brand Code
        for cb_ind, brand in enumerate(brand_list):
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
                company = comp_list[cb_ind]
                brand = brand_list[cb_ind]
                df.loc[o_ind, 'COMPANY'] = company
                df.loc[o_ind, 'BRAND'] = brand
        
        # Categories Code
        # Rule # 1 
        for r1_ind, subcat in enumerate(r1_subcat_list):
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
                sup_cat = r1_supcat_list[r1_ind]
                cat = r1_cat_list[r1_ind]
                sub_cat = r1_subcat_list[r1_ind]
                df.loc[o_ind, 'SUPER CATEGORY'] = sup_cat
                df.loc[o_ind, 'CATEGORY'] = cat
                df.loc[o_ind, 'SUB CATEGORY'] = sub_cat
            
            # Rule 2
            else:
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
                min_score_index = score_of_sku.index(min_score)

                sup_cat = r2_supcat_list[min_score_index]
                cat = r2_cat_list[min_score_index]
                sub_cat = r2_subcat_list[min_score_index]
                pack = r2_pack_list[min_score_index]
                df.loc[o_ind, 'SUPER CATEGORY'] = sup_cat
                df.loc[o_ind, 'CATEGORY'] = cat
                df.loc[o_ind, 'SUB CATEGORY'] = sub_cat
                df.loc[o_ind, 'PACKAGING'] = pack
        
    print("Your Cleaning has been Completed, now saving your file")
    print()
    return df.to_excel(data["File name to be saved"], index = False)
    print("Your file has been saved")

Data_Cleaning(df)
print("Process has been Completed, press any key to exit")
input()
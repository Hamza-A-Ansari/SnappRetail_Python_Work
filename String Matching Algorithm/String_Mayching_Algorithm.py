import pandas as pd
import re
from Levenshtein import distance as lev
import string

# data_name = input('Enter File path in excel format with extension: ')
# sheet_name = input("Enter Sheet name: ")
#to_save = input('Enter updated file name to be saved with excel extension(.xlsx): ')
to_save = "17k_SN_set_v2.xlsx"

df = pd.read_excel("17k_SN_set.xlsx")
df1 = pd.read_excel("sku standard name_v1.xlsx")

# sku_list={'sku_name':correct_name}
def string_matching(df):
    original_name = list(df['NAME BY SHOPKEEPER'])
    correct_name = list(df1['Name'])

    for ind, o_name in enumerate(original_name):
        o_name = str(o_name)

        kg = re.findall(r'([\d+]?[/.]?\d+)\s?[-]?\s?[Kk][Gg]', o_name)
        if kg:
            df.loc[ind, "SIZE"] = kg[0]
            df.loc[ind, "MeasurementType"] = "KG"

        gm = re.findall(r'([\d+]?[/.]?\d+)\s?[-]?\s?[Gg][Rr]?[Aa]?[Mm]?', o_name)
        if gm:
            df.loc[ind, "SIZE"] = gm[0]
            df.loc[ind, "MeasurementType"] = "GM"

        ltr = re.findall(r'([\d+]?[/.]?\d+)\s?[Ll][Ii]?[Ee]?[Tt]+[Ee]?[Rr]?[Ee]?[Ss]?', o_name)
        if ltr:
            df.loc[ind, "SIZE"] = ltr[0]
            df.loc[ind, "Measurementype"] = "LITRE"

        ml = re.findall(r'([\d+]?[/.]?\d+)\s?[Mm][Ll]', o_name)
        if ml:
            df.loc[ind, "SIZE"] = ml[0]
            df.loc[ind, "MeasurementType"] = "ML"

        dzn = re.findall(r'([\d+]?[/.]?\d+)\s?[Dd][Aa]?[Oo]?[Rr]?[Zz][Ee]?[Oo]?[Nn]?', o_name)
        if dzn:
            df.loc[ind, "SIZE"] = dzn[0]
            df.loc[ind, "MeasurementType"] = "UNITS"

        pcs = re.findall(r'([\d+]?[/.]?\d+)\s?[Pp][Ii]?[Ee]?[Cc]?[Ii]?[Ee]?[Ss]?', o_name)
        if pcs:
            df.loc[ind, "SIZE"] = pcs[0]
            df.loc[ind, "MeasurementType"] = "UNITS"

        outer = []
        o_name = o_name.lower()
        sp = string.punctuation
        for punc in sp:
            if punc in o_name:
                o_name = o_name.replace(punc, " ")
        o_name = list(o_name.split(" "))

        for c_name in correct_name:
            inner = []
            for li_o_name in o_name:
                li_o_name = li_o_name.lower()
                score = lev(c_name, li_o_name)
                inner.append(score)

            min_inner = min(inner)
            outer.append(min_inner)        

        min_score = min(outer)
        if min_score == 0:
            index = outer.index(min_score)
            df.loc[ind,"STANDARD NAME"] = correct_name[index].upper()
        
    return df.to_excel(to_save, index = False)

string_matching(df)
print("Completed")
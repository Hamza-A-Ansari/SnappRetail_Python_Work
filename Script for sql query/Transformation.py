import pandas as pd
import logging
from openpyxl import Workbook
from openpyxl.styles import PatternFill

def Transformation(today_data, output_filename, column_names):
    logging.info("Now started Transformation")


    # Pandas DataFrame for Prod_replica data
    today_df = pd.DataFrame(today_data, columns= column_names)

  
    today_df.to_excel(output_filename, index=False)
       
    logging.info("Transformation successful, file has been saved")
    



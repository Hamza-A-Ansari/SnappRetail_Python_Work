import pandas as pd
import logging
from openpyxl import Workbook
from openpyxl.styles import PatternFill

def Transformation(today_data, lastday_data, sevenday_data, mtd_data, output_filename):
    logging.info("Now started Transformation")
    # Headers for table 1
    t1h1 = 'Id'
    t1h2 = 'Address'
    t1h3 = 'IsActive'
    t1h4 = 'Storename'
    t1h5 = 'FieldSupervisorName'
    t1h6 = 'DukaanCoach'
    t1h7 = 'FieldExecutiveName'
    t1h8 = 'Latitude'
    t1h9 = 'Longitude'

    # Pandas DataFrame for Prod_replica data
    today_df = pd.DataFrame(today_data, columns=[t1h1, t1h2, t1h3, t1h4, t1h5, t1h6, t1h7, t1h8, t1h9])
    lastday_df = pd.DataFrame(lastday_data, columns=[t1h1, t1h2, t1h3, t1h4, t1h5, t1h6, t1h7, t1h8, t1h9])
    sevenday_df = pd.DataFrame(sevenday_data, columns=[t1h1, t1h2, t1h3, t1h4, t1h5, t1h6, t1h7, t1h8, t1h9])
    mtd_df = pd.DataFrame(mtd_data, columns=[t1h1, t1h2, t1h3, t1h4, t1h5, t1h6, t1h7, t1h8, t1h9])

    # Saving file
    # Create a Pandas Excel writer using ExcelWriter
    with pd.ExcelWriter(output_filename) as writer:
        
        # Write each DataFrame to a separate sheet
        today_df.to_excel(writer, sheet_name='Today-Inactive', index=False)
        lastday_df.to_excel(writer, sheet_name='Last-Day-Inactive', index=False)
        sevenday_df.to_excel(writer, sheet_name='Last-7-Day-Inactive', index=False)
        mtd_df.to_excel(writer, sheet_name='Month-To-Date-Inactive', index=False)

    logging.info("Transformation successful, file has been saved")
    



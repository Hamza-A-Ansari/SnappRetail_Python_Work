import pandas as pd
import logging

def Transformation(prodreplica_data, oracle_data, output_filename):
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
    prodreplica_df = pd.DataFrame(prodreplica_data, columns=[t1h1, t1h2, t1h3, t1h4, t1h5, t1h6, t1h7, t1h8, t1h9])


    # Headers for table 2 
    t2h1 = 'SYNC_TIME'
    t2h2 = 'MERCH CHECKIN DATE'
    t2h3 = 'VISIT ID'
    t2h4 = 'VISIT_DATE'
    t2h5 = 'VISIT DAY'
    t2h6 = 'MERCHANDISER'
    t2h7 = 'STORE NAME'
    t2h8 = 'STORE LATITUDE'
    t2h9 = 'STORE LONGITUDE'
    t2h10 = 'VISIT LATITUDE'
    t2h11 = 'VISIT LONGITUDE'
    t2h12 = 'STORECODE'
    t2h13 = 'STATUS'
    t2h14 = 'CHECKIN_TIME'
    t2h15 = 'CHECKOUT_TIME'
    t2h16 = 'TOTAL TIME' 
    t2h17 = 'CATEGORY_WISE_PICTURE_LINK'

    # Pandas DataFrame for Oracle data
    oracle_df = pd.DataFrame(oracle_data, columns=[t2h1, t2h2, t2h3, t2h4, t2h5, t2h6, t2h7,
                                               t2h8, t2h9, t2h10, t2h11, t2h12,  t2h13,
                                               t2h14, t2h15, t2h16, t2h17])
    
    
    # Common columns in both DataFrames
    common_column_df1 = 'Id'
    common_column_df2 = 'STORECODE'

    # Type casting to integer of columns to be inner joined
    oracle_df[common_column_df2] = oracle_df[common_column_df2].astype(int)
    prodreplica_df[common_column_df1] = prodreplica_df[common_column_df1].astype(int)

    # Inner join on both DataFrames
    result_df = pd.merge(prodreplica_df, oracle_df, left_on=common_column_df1, right_on=common_column_df2, how="inner")

    # Find the index of rows with maximum datetime within each group
    idx = result_df.groupby('STORECODE')['MERCH CHECKIN DATE'].idxmax()

    # Use the index to select the corresponding rows from the original dataframe
    max_datetime_rows = result_df.loc[idx]

    # Structure our DataFrame
    columns_to_keep = [
    'STORECODE', 'Storename', 'Address', 'IsActive', 'FieldSupervisorName',
    'FieldExecutiveName', 'VISIT ID', 'SYNC_TIME', 'VISIT_DATE', 'CHECKIN_TIME',
    'CHECKOUT_TIME', 'TOTAL TIME', 'STORE LATITUDE', 'STORE LONGITUDE',
    'VISIT LATITUDE', 'VISIT LONGITUDE', 'CATEGORY_WISE_PICTURE_LINK']

    new_df = max_datetime_rows.loc[:, columns_to_keep]

    # Saving file
    new_df.to_excel(output_filename, index=False)

    logging.info("Transformation successful, file has been saved")
    

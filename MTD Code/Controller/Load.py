from Model.Libraries import *

def Load_Data(df, table):
    logging.info("Connected to UAT MTD-OLAP Database")
    engine = get_connection_uat_MTD()
    logging.info("Connected")

    logging.info(f'Start dumping data in MTD-OLAP i.e, {table}')

    # Dump sale Data to Device-OLAP
    df.to_sql(table, engine, index=False, if_exists="append")

    logging.info(f"Dumped {table}")


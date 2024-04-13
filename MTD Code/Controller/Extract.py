from Model.Libraries import *
import logging
from Model.Connections import *
import pandas as pd
from sqlalchemy import text, select
from datetime import datetime

def max_date():
    engine = get_connection_uat_MTD()
    max_dt_query = """ SELECT max(`MTD Date`) FROM `MTD-OLAP`.OLSummary """
    rp_max_id_query = """ SELECT max(Generated_Visit_Id) FROM `MTD-OLAP`.RawVisits  """
    att_max_query = """ SELECT max(Attendance_Id) FROM `MTD-OLAP`.RawAttendance """
    max_date = pd.read_sql_query(text(max_dt_query), engine.connect())
    rp_max_id = pd.read_sql_query(text(rp_max_id_query), engine.connect())
    att_max_id = pd.read_sql_query(text(att_max_query), engine.connect())
    if max_date.iloc[0, 0] == None:
        max_date = '2024-03-01'
    else:
        max_date = max_date.iloc[0, 0]

    if rp_max_id.iloc[0, 0] == None:
        rp_max_id = 0
    else:
        rp_max_id = rp_max_id.iloc[0, 0]

    if att_max_id.iloc[0, 0] == None:
        att_max_id = 89325
    else:
        att_max_id = att_max_id.iloc[0, 0]
    
    return max_date, rp_max_id, att_max_id

def delete():
    # Checking max date
    max_dt, rp_max_id, att_max_id = max_date()
    print(max_dt)
    engine = get_connection_uat_MTD()
    olsum = f""" DELETE FROM `MTD-OLAP`.OLSummary WHERE `MTD Date` = '{max_dt}' """
    fesum = f""" DELETE FROM `MTD-OLAP`.FESummary WHERE `MTD Date` = '{max_dt}' """
    logging.info('Deleting latest MTD date in sql')
    with engine.connect() as connection:
        connection.execute(text(olsum))
        connection.execute(text(fesum))
        connection.commit()
        connection.close()
    logging.info('Deleted')
    return max_dt, rp_max_id, att_max_id

def latest_mtd():
    max_dt, max_id, att_max_id = max_date()
    max_dt_dt = datetime.strptime(str(max_dt), '%Y-%m-%d')
    year = max_dt_dt.strftime('%Y')
    month = max_dt_dt.strftime('%m')
    day = max_dt_dt.strftime('%d')
    engine = get_connection_uat_MTD()
    max_mtd_query = f""" SELECT * FROM `MTD-OLAP`.OLSummary WHERE `MTD Date` = '{max_dt}' and IsActive = 1 """
    mtd = pd.read_sql_query(text(max_mtd_query), engine.connect())
    raw_visit_query = f""" SELECT * FROM `MTD-OLAP`.RawVisits WHERE year(`Date`) = '{year}' and month(`Date`) = '{month}' and day(`Date`) <= '{day}' """
    raw_visit = pd.read_sql_query(text(raw_visit_query), engine.connect())
    raw_att_query = f""" SELECT * FROM `MTD-OLAP`.RawAttendance WHERE year(`Date`) = {year} and month(`Date`) = {month} and day(`Date`) <= {day} """
    raw_att = pd.read_sql_query(text(raw_att_query), engine.connect()) 
    fe_sum_query = f""" SELECT * FROM `MTD-OLAP`.FESummary WHERE `MTD Date` = '{max_dt}' """
    fe_sum = pd.read_sql_query(text(fe_sum_query), engine.connect())

    return mtd, max_dt, fe_sum, raw_visit, raw_att


def Extract_Prod(query):
    # Prod Replical DataBase
    logging.info("Connecting to Production Database")
    
    # prodreplica_connection, prodreplica_cursor = prod_con()
    engine = get_connection_prod()

    logging.info('Connected')

    # Execute and fetch query
    logging.info("Fetching Store wise KPIs data")
    df = pd.read_sql_query(query, engine.connect())
    logging.info('Fetched')

    return df

def Extract_Oracle(query):
    # Making Connection to Oracle Database
    logging.info("Connecting to Oracle Database...")
    oracle_connection, oracle_cursor = oracle_con()
    logging.info('Connected')

    # Execute and fetch query3  
    logging.info("Fetching Oracle Data - Stores")
    oracle_cursor.execute(query)
    data = oracle_cursor.fetchall()

    # Get column names from the cursor's description
    columns = [column[0] for column in oracle_cursor.description]
    logging.info('Fetched') 

    return data, columns


def Extract_UAT(query):
    engine = get_connection_uat_MTD()

    df = pd.read_sql_query(text(query), engine.connect())

    return df




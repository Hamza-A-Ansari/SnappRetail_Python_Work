# from Model.Libraries import load_dotenv, logging, oracledb
import os
import logging
import oracledb
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()


def prod_con():
     load_dotenv()
     logging.info("Connecting to Prod Replica Database...")
     username = os.getenv('prod_user')
     password = os.getenv('prod_password')
     host = os.getenv('prod_host')
     port = os.getenv('prod_port')
     database = os.getenv('prod_database')
     Database_url_prod = "mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
               username,password,host,port,database
          )
     return Database_url_prod

def get_connection_prod():
    return create_engine(prod_con())


def oracle_con():
    username = os.getenv('oracle_user')
    password = os.getenv('oracle_password')
    host = os.getenv('oracle_host')
    port = os.getenv('oracle_port')
    service_name = os.getenv('oracle_SID')

    # Connect to the Oracle database
    dsn = oracledb.makedsn(host, port, service_name=service_name)
    oracle_connection = oracledb.connect(user=username, password=password, dsn=dsn)

    # Create cursors for Oracle database
    oracle_cursor = oracle_connection.cursor()

    return oracle_connection, oracle_cursor


def uat_MTD_connection():
     logging.info("Connecting to UAT Device-OLAP Database...")
     load_dotenv()
     username = os.getenv('username_uat_MTD')
     password = os.getenv('password_uat_MTD')
     host = os.getenv('host_uat_MTD')
     port = os.getenv('port_uat_MTD')
     database = os.getenv('database_uat_MTD')
     Database_url_uat_MTD = "mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
               username,password,host,port,database)
     
     return Database_url_uat_MTD


def get_connection_uat_MTD():
    return create_engine(uat_MTD_connection())
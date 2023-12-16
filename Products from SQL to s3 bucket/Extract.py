import os
from dotenv import load_dotenv
import logging
from sqlalchemy import create_engine

def prod_connection():
     load_dotenv()

     logging.info("Connecting to Prod Replica Database...")
     username = os.getenv('username_prod')
     password = os.getenv('password_prod')
     host = os.getenv('host_prod')
     port = os.getenv('port_prod')
     database = os.getenv('database_prod')
     Database_url_prod = "mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
               username,password,host,port,database
          )
     return Database_url_prod


def get_connection_prod():
    return create_engine(prod_connection())
    
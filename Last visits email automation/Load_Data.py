import mysql.connector
import oracledb
import os
from dotenv import load_dotenv
import logging

def Load_Data(config):
    # Prod Replical DataBase
    # Read .env values
    load_dotenv()
    os.getenv('prod_host')

    # Connect to the prod_replica database
    logging.info("\nConnecting to Prod Replica Database...")
    prodreplica_connection = mysql.connector.connect(
        host = os.getenv('prod_host'),
        user = os.getenv('prod_user'),
        passwd = os.getenv('prod_password'),
        database = os.getenv('prod_database'),
        port = os.getenv('prod_port')
    )


    logging.info('Connected\n')

    # Create cursors for prod_replica database
    prodreplica_cursor = prodreplica_connection.cursor()

    # Quries from config
    queries_config = config['query_config']
    prodreplica_query = queries_config['query1']

    # Execute and fetch query
    logging.info("Fetching mysql data...")
    prodreplica_cursor.execute(f"{prodreplica_query}")
    prodreplica_data = prodreplica_cursor.fetchall()
    logging.info('Fetched\n')

   
    # Close the database connections and cursors
    prodreplica_cursor.close()
    prodreplica_connection.close()

        # Oracle DataBase
    # Read .env values for Oracle database
    logging.info("Connecting to Oracle Database...")
    username = os.getenv('oracle_user')
    password = os.getenv('oracle_password')
    host = os.getenv('oracle_host')
    port = os.getenv('oracle_port')
    service_name = os.getenv('oracle_SID')

    # Connect to the Oracle database
    dsn = oracledb.makedsn(host, port, service_name=service_name)
    oracle_connection = oracledb.connect(user=username, password=password, dsn=dsn)
    logging.info('Connected\n')

    # Create cursors for Oracle database
    oracle_cursor = oracle_connection.cursor()

    # Quries from config
    queries_config = config['query_config']
    oracle_query = queries_config['query2']

    # Execute and fetch query
    logging.info("Fetching Oracle Data...")
    oracle_cursor.execute(oracle_query)
    oracle_data = oracle_cursor.fetchall()
    logging.info('Fetched\n')

    oracle_cursor.close()
    return prodreplica_data, oracle_data
    
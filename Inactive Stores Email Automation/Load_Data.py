import mysql.connector
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
    today_query = queries_config['query1']
    lastday_query = queries_config['query2']
    sevenday_query = queries_config['query3']
    mtd_query = queries_config['query4']

    # Execute and fetch query
    logging.info("Fetching mysql data...")

    prodreplica_cursor.execute(f"{today_query}")
    today_data = prodreplica_cursor.fetchall()

    prodreplica_cursor.execute(f"{lastday_query}")
    lastday_data = prodreplica_cursor.fetchall()

    prodreplica_cursor.execute(f"{sevenday_query}")
    sevenday_data = prodreplica_cursor.fetchall()

    prodreplica_cursor.execute(f"{mtd_query}")
    mtd_data = prodreplica_cursor.fetchall()

    logging.info('Fetched\n')

   
    # Close the database connections and cursors
    prodreplica_cursor.close()
    prodreplica_connection.close()

    return today_data, lastday_data, sevenday_data, mtd_data
    
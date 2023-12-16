import pandas as pd
import logging
from Extract import *


def Transformation(config, output_filename):
    logging.info("Now started Transformation")
    engine = get_connection_prod()
    chunk_size = 10000  # Adjust the chunk size as needed
    offset = 0
    data_frames = []
    queries_config = config['query_config']
    custom_query = queries_config['query1']

    while True:
        query = f"{custom_query} LIMIT {chunk_size} OFFSET {offset}"
        chunk_df = pd.read_sql_query(query, engine.connect())
        if chunk_df.empty:
            break  # No more data to fetch
        # all_data.append(chunk_df)
        offset += chunk_size
        chunk_df = pd.DataFrame(chunk_df)
        data_frames.append(chunk_df)

    final_df = pd.concat(data_frames, ignore_index=True)


    final_df.to_csv(output_filename, index=False)
    return final_df
    
    
       
    # logging.info("Transformation successful, file has been saved")
    



from Model.Libraries import *


def main():
    # Create Log file
    logging.basicConfig(
        # filename=os.getenv('LOG_FILE'),
        filename='app.log',
        filemode='a',
        format='%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
        level=logging.INFO)

    # Read the configuration from the config file
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Get yesterday's date
    current_date = datetime.now()
    yesterday = current_date - timedelta(days=1)
    logging.info(f'Yesterday\'s date: {yesterday}')

    # Format the yesterday's date as 'DD-MM-YYYY'
    yes_dt_str = yesterday.strftime('%Y-%m-%d')

    # Maximum date of MTD
    max_dt, rp_max_id, att_max_id = delete()
    logging.info(f'Max date in sql: {max_dt}')

    # Convert to datetime
    yes_dt = datetime.strptime(str(yes_dt_str), '%Y-%m-%d')
    max_dt = datetime.strptime(str(max_dt), '%Y-%m-%d')

    # Calculate difference
    difference = yes_dt - max_dt
    temp = str(difference)
    if temp == '0:00:00':
        max_dt_str = str(max_dt.date())
        logging.info(f'MTD is uptodate. Updating latest MTD: {max_dt_str}')
        year = max_dt.strftime('%Y')
        month = max_dt.strftime('%m')
        day = max_dt.strftime('%d')

        OL_Summ_df, common_column_df = MTD_Controller(config, max_dt_str, year, month, day)

    else:
        # Iterate over the range between max_dt and yes_dt, including yes_dt
        formatted_dates = []
        for i in range(difference.days + 1):
            formatted_dates.append(max_dt.date().strftime('%Y-%m-%d'))
            max_dt += timedelta(days=1)

        logging.info(f'Updating MTD of dates: {formatted_dates}')


        for dt in tqdm(formatted_dates):
            dt_dtf = datetime.strptime(str(dt), '%Y-%m-%d')
            year = dt_dtf.strftime('%Y')
            month = dt_dtf.strftime('%m')
            day = dt_dtf.strftime('%d')

            logging.info(f'\n     Doing whole process for date: {dt}')
            OL_Summ_df, common_column_df = MTD_Controller(config, dt, year, month, day)
            logging.info(f'     Done process for date: {dt}')

    
    Raw_Controller(OL_Summ_df, common_column_df, rp_max_id, att_max_id)



    # FE Summary
    if temp == '0:00:00':
        max_dt_str = str(max_dt.date())
        logging.info(f'FE Summary MTD is uptodate. Updating latest MTD: {max_dt_str}')
        year = max_dt.strftime('%Y')
        month = max_dt.strftime('%m')
        day = max_dt.strftime('%d')

        FE_Sum = FESum_Controller(config, max_dt_str, year, month, day)

    else:
        # Iterate over the range between max_dt and yes_dt, including yes_dt
        formatted_dates = []
        for i in range(difference.days + 1):
            formatted_dates.append(max_dt.date().strftime('%Y-%m-%d'))
            max_dt += timedelta(days=1)

        logging.info(f'Updating FE Summary MTD of dates: {formatted_dates}')


        for dt in tqdm(formatted_dates):
            dt_dtf = datetime.strptime(str(dt), '%Y-%m-%d')
            year = dt_dtf.strftime('%Y')
            month = dt_dtf.strftime('%m')
            day = dt_dtf.strftime('%d')

            logging.info(f'\n     Doing whole process for date: {dt}')
            FE_Sum = FESum_Controller(config, dt, year, month, day)
            logging.info(f'     Done process for date: {dt}')




    # Send email
    logging.info('..........Emailing Phase..........\n') 
    email_subject = "Daily Report: MTD OL Summary"
    email_body = "Please find attached the daily report for  MTD OL Summary."
    socket.getaddrinfo('localhost', 8080)
    attachment_path1, attachment_path2, attachment_path3 = send_email(config, email_subject, email_body)
    logging.info('..........Emailing Phase completed..........\n') 

    

    # Delete Excel File
    logging.info('..........Deleting Phase..........\n')
    delete_excel_file(attachment_path1)
    delete_excel_file(attachment_path2)
    delete_excel_file(attachment_path3)
    logging.info('..........Deleting Phase completed..........\n')



    logging.info("########## ETL process completed successfully ##########")


if __name__ == "__main__":
    main()



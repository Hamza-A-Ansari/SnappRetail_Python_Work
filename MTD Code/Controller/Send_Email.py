import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os
from dotenv import load_dotenv
import logging
from Controller.Extract import latest_mtd
import pandas as pd


def fe_tabs(df, path, column, summary=None, include_summary=True):
    unique_fe_names = df[column].unique()

    # Exclude unnecessary values
    exclude_values = ['1', '0', 'Demo', 'LIAQUAT MARKET', '']
    unique_fe_names = [name for name in unique_fe_names if name not in exclude_values]

    # Sorting
    cleaned_list = [item for item in unique_fe_names if isinstance(item, str)]
    unique_fe_names = sorted(cleaned_list)

    # Saving excel file
    with pd.ExcelWriter(path) as writer:
        if include_summary:
            summary.to_excel(writer, sheet_name='FE Summary', index=False)
        for fe_name in unique_fe_names:
            mtd_df_fe = df[df[column] == fe_name]
            mtd_df_fe.to_excel(writer, sheet_name=f'{fe_name}', index=False)




def send_email(config, subject, body):

    # Latest MTD Reports
    mtd, max_dt, FE_Sum, raw_visit, raw_att = latest_mtd()

    # Path of excel file
    attachment_path1 = f'OL_Summary_{max_dt}.xlsx'
    attachment_path2 = f'Raw_Visits_{max_dt}.xlsx'
    attachment_path3 = f'Raw_Attendance_{max_dt}.xlsx'

    # Drop unnecessary columns
    columns_to_exclude = ['Min/Store/Day', 'Value/Invoice/Store', 'Prod/Store/Day', 'SubCat/Store/Day', 'SupCat/Store/Day', 'Credit Sales', 'Credit Invoices', 'Pr.Inv Sales', 'Pr.Inv Count']
    mtd = mtd.drop(columns=columns_to_exclude)

    # Calling function for saving excel file
    fe_tabs(mtd, attachment_path1, 'FE_Name', FE_Sum)

    temp = mtd[['Store_Id', 'Store_Name', 'IsActive', 'Supervisor']]

    raw_visit = pd.merge(raw_visit, temp, left_on='Store_Id', right_on='Store_Id', how="left")

    raw_visit_columns = [
        'Store_Id',
        'Visit_FE',
        'Actual_FE',
        'Supervisor',
        'Store_Name',
        'IsActive',
        'Date',
        'Generated_Visit_Id',
        'Visit_Id',
        'Store_Latitude', 
        'Store_Longitude', 
        'Visit_Latitude',
        'Visit_Longitude', 
        'Difference_in_Meters', 
        'Range_Status',
        'CheckInTime', 
        'CheckOutTime',
        'Total_Time',
        'Time_Status',
        'Approved']
    
    raw_visit = raw_visit.loc[:, raw_visit_columns]

    # Calling function for saving excel file
    fe_tabs(raw_visit, attachment_path2, 'Visit_FE', include_summary=False)
    fe_tabs(raw_att, attachment_path3, 'FE_Name', include_summary=False)

    # Email configuration
    logging.info('Importing email configs') 
    load_dotenv()
    email_config = config['email_config']
    sender_email = os.getenv('sender_email')
    sender_password = os.getenv('sender_password')
    recipient_email = email_config['recipient_email']
    recipient_email= ", ".join(recipient_email.split(','))
    smtp_server = email_config['smtp_server']
    smtp_port = email_config['smtp_port']
    logging.info('Imported')

    # Create MIME message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Attach body text
    msg.attach(MIMEText(body, 'plain'))

    # Attach the Excel file
    logging.info('Reading and sending Excel File')
    for path in [attachment_path1, attachment_path2, attachment_path3]:
        with open(path, "rb") as attachment:
            part = MIMEApplication(attachment.read(), Name=path)
            part['Content-Disposition'] = f'attachment; filename="{path}"'
            msg.attach(part)

    # Connect to SMTP server and send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        # server.sendmail(sender_email, recipient_email, msg.as_string())
        server.send_message(msg)
        logging.info('Email has been sent.')

    return attachment_path1, attachment_path2, attachment_path3


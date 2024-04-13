from Model.Libraries import *

def Raw_Controller(OL_Summ_df, common_column_df, rp_max_id, att_max_id):
    logging.info('..........Raw Data Phase..........\n')
    # Queries
    Raw_RP_st_query = f""" SELECT ST.STORE_CODE AS "Store_Id", rm.Name AS "Visit_FE", GV.ID AS "Generated_Visit_Id", mv.Id AS "Visit_Id", TO_CHAR(mv.CHECKIN_TIME, 'YYYY-MM-DD') AS "Date", ST.LATITUDE AS "Store_Latitude", st.LONGITUDE AS "Store_Longitude", mv.LATITUDE AS "Visit_Latitude", mv.LONGITUDE AS "Visit_Longitude", ROUND(ACOS(ROUND(COS(ACOS(-1)/180*(90-ST.LATITUDE))* COS(ACOS(-1)/180*(90-mv.LATITUDE))+ SIN(ACOS(-1)/180*(90-ST.LATITUDE))* SIN(ACOS(-1)/180*(90-MV.LATITUDE))* COS(ACOS(-1)/180*(ST.LONGITUDE-MV.LONGITUDE)), 20)) * 6371000, 2) as "Difference_in_Meters", CASE WHEN (ACOS(ROUND(COS(ACOS(-1)/180*(90-ST.LATITUDE))* COS(ACOS(-1)/180*(90-mv.LATITUDE))+ SIN(ACOS(-1)/180*(90-ST.LATITUDE))* SIN(ACOS(-1)/180*(90-MV.LATITUDE))* COS(ACOS(-1)/180*(ST.LONGITUDE-MV.LONGITUDE)), 20)) * 6371000) > 1000 THEN 0 ELSE 1 END AS "Range_Status", mv.CHECKIN_TIME AS "CheckInTime", mc.CHECKOUT_TIME AS "CheckOutTime", EXTRACT(HOUR FROM (mc.CHECKOUT_TIME - mv.CHECKIN_TIME)) * 60 + EXTRACT(MINUTE FROM (mc.CHECKOUT_TIME - mv.CHECKIN_TIME)) AS "Total_Time", CASE WHEN (EXTRACT(HOUR FROM (mc.CHECKOUT_TIME - mv.CHECKIN_TIME)) * 60 + EXTRACT(MINUTE FROM (mc.CHECKOUT_TIME - mv.CHECKIN_TIME))) >= 15 THEN 1 ELSE 0 END AS "Time_Status", CASE WHEN ((CASE WHEN (ACOS(ROUND(COS(ACOS(-1)/180*(90-ST.LATITUDE))* COS(ACOS(-1)/180*(90-mv.LATITUDE))+ SIN(ACOS(-1)/180*(90-ST.LATITUDE))* SIN(ACOS(-1)/180*(90-MV.LATITUDE))* COS(ACOS(-1)/180*(ST.LONGITUDE-MV.LONGITUDE)), 20)) * 6371000) > 1000 THEN 0 ELSE 1 END) = 1 AND (EXTRACT(HOUR FROM (mc.CHECKOUT_TIME - mv.CHECKIN_TIME)) * 60 + EXTRACT(MINUTE FROM (mc.CHECKOUT_TIME - mv.CHECKIN_TIME))) >= 15) THEN 1 ELSE 0 END AS "Approved" FROM GENERATED_VISIT_LOGS GV LEFT JOIN REDBULL_RAW_STORES ST ON ST.ID = GV.STORE_ID LEFT JOIN MERCHANDIZER_VISIT MV ON MV.GEN_VISIT_ID = GV.ID LEFT JOIN MERCHANDIZER_CHECKOUT mc ON mv.VISIT_CODE = mc.VISIT_CODE LEFT JOIN REDBULL_MERCHANDISER rm ON gv.MERCHANDISER_ID = rm.Id WHERE GV.ID > '{rp_max_id}' AND NOT REGEXP_LIKE(ST.STORE_CODE, '[[:alpha:]]') AND (CASE WHEN MV.ID IS NULL THEN 'NOT AUDITED' ELSE CASE WHEN MC.UNSUCCESSFUL_REASON IS NULL THEN 'SUCCESSFUL' ELSE 'NOT SUCCESSFUL' END END) = 'SUCCESSFUL' """
    Raw_fe_att_query = f""" SELECT ma.Id AS "Attendance_Id", ma.MERCHANDISER_ID AS "FE_Id", rm.Name AS "FE_Name", TO_CHAR(ma.TIMESTAMP, 'YYYY-MM-DD') AS "Date", ma.STARTING_POINT AS "Starting_Point", LATITUDE AS "Meet_Latitude", LONGITUDE AS "Meet_Longitude", 24.832426935760285 AS "Office_Latitude", 67.06538032511277 AS "Office_Longitude", ROUND(ACOS(ROUND(COS(ACOS(-1)/180*(90-24.832426935760285))* COS(ACOS(-1)/180*(90-LATITUDE))+ SIN(ACOS(-1)/180*(90-24.832426935760285))* SIN(ACOS(-1)/180*(90-LATITUDE))* COS(ACOS(-1)/180*(67.06538032511277-LONGITUDE)), 20)) * 6371000, 2) as "Difference_in_Meters", CASE WHEN (ROUND(ACOS(ROUND(COS(ACOS(-1)/180*(90-24.832426935760285))* COS(ACOS(-1)/180*(90-LATITUDE)) + SIN(ACOS(-1)/180*(90-24.832426935760285))* SIN(ACOS(-1)/180*(90-LATITUDE))* COS(ACOS(-1)/180*(67.06538032511277-LONGITUDE)), 20)) * 6371000, 2) ) > 1000 THEN 0 ELSE 1 END AS "Range_Status", ma.TIMESTAMP AS "AttendanceTime", CASE WHEN TO_NUMBER(TO_CHAR(ma.TIMESTAMP, 'HH24')) < 9 OR (TO_NUMBER(TO_CHAR(ma.TIMESTAMP, 'HH24')) = 9 AND TO_NUMBER(TO_CHAR(ma.TIMESTAMP, 'MI')) < 45) THEN 1 ELSE 0 END AS "Meet_Time_Check", CASE WHEN TO_NUMBER(TO_CHAR(ma.TIMESTAMP, 'HH24')) < 11 OR (TO_NUMBER(TO_CHAR(ma.TIMESTAMP, 'HH24')) = 11 AND TO_NUMBER(TO_CHAR(ma.TIMESTAMP, 'MI')) < 00) THEN 1 ELSE 0 END AS "Att_Time_Check", CASE WHEN (CASE WHEN (ROUND(ACOS(ROUND(COS(ACOS(-1)/180*(90-24.832426935760285))* COS(ACOS(-1)/180*(90-LATITUDE))+ SIN(ACOS(-1)/180*(90-24.832426935760285))* SIN(ACOS(-1)/180*(90-LATITUDE))* COS(ACOS(-1)/180*(67.06538032511277-LONGITUDE)), 20)) * 6371000, 2)) > 1000 THEN 0 ELSE 1 END) = 1 AND (CASE WHEN TO_NUMBER(TO_CHAR(ma.TIMESTAMP, 'HH24')) < 9 OR (TO_NUMBER(TO_CHAR(ma.TIMESTAMP, 'HH24')) = 9 AND TO_NUMBER(TO_CHAR(ma.TIMESTAMP, 'MI')) < 45) THEN 1 ELSE 0 END) = 1 THEN 1 ELSE 0 END AS "Meet_Approved", CASE WHEN TO_NUMBER(TO_CHAR(ma.TIMESTAMP, 'HH24')) < 11 OR (TO_NUMBER(TO_CHAR(ma.TIMESTAMP, 'HH24')) = 11 AND TO_NUMBER(TO_CHAR(ma.TIMESTAMP, 'MI')) < 00) THEN 1 ELSE 0 END AS "Att_Approved" FROM MERCHANDISER_ATTENDANCE ma LEFT JOIN (SELECT ID, NAME FROM REDBULL_MERCHANDISER) rm ON ma.MERCHANDISER_ID = rm.ID WHERE ma.Id > '{att_max_id}' ORDER BY ma.Id asc """
    
    # Extraction of data 
    Raw_RP_st_data, Raw_RP_st_columns = Extract_Oracle(Raw_RP_st_query)
    Raw_fe_att_data, Raw_fe_att_columns = Extract_Oracle(Raw_fe_att_query)

    # Transformation of data
    Raw_RP_st_df = dataframe(Raw_RP_st_data, Raw_RP_st_columns)
    Raw_fe_att_df = dataframe(Raw_fe_att_data, Raw_fe_att_columns)

    if Raw_RP_st_df.empty:

        logging.info('RawVisits data is upto date')

    else:

        # Typecasting to integer
        Raw_RP_st_df = typecasting(Raw_RP_st_df, common_column_df)

        # Joining DataFrames
        temp = OL_Summ_df[['Store_Id', 'FE_Name']]
        Raw_RP_st_df = leftjoin(Raw_RP_st_df, temp, common_column_df)

        # Rename column
        Raw_RP_st_df.rename(columns={'FE_Name': 'Actual_FE'}, inplace=True)

        # Formatting
        columns_to_keep_2 = [
        'Store_Id',
        'Visit_FE',
        'Actual_FE',
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
        'Approved'
        ]
        Raw_RP_st_df = formatting(Raw_RP_st_df, columns_to_keep_2)

        # Loading Data
        Load_Data(Raw_RP_st_df, 'RawVisits')

    if Raw_fe_att_df.empty:
        logging.info('RawVisits data is upto date')
    else:
        # Working-Day dataframe
        wd_df = pd.read_excel('WorkingDay.xlsx')

        # Date column typecasting
        wd_df = datetimefunc(wd_df, 'Date')
        Raw_fe_att_df = datetimefunc(Raw_fe_att_df, 'Date')

        # Joining DataFrames
        Raw_fe_att_df = leftjoin(Raw_fe_att_df, wd_df, 'Date')

        # Add a custom column for Final Attendance
        Raw_fe_att_df['Final_Attendance'] = Raw_fe_att_df.apply(lambda x: 1 if (x['Holiday'] == 0 and x['Meeting_Day'] == 1 and x['Meet_Approved'] == 1) 
                                         else (1 if (x['Holiday'] == 0 and x['Meeting_Day'] == 0 and x['Att_Approved'] == 1) else 0), axis=1)

        # Loading Data
        Load_Data(Raw_fe_att_df, 'RawAttendance')

        logging.info('..........Raw Data Phase Completed..........\n')
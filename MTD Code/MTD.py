from Model.Libraries import *

def MTD_Controller(config, dt, year, month, day):

    # Quries from config
    queries_config = config['query_config']

    # Queries
    st_kpis_query = f"SELECT st.Id as Store_Id, sum(sp.Amount) as `MTD`, 1 AS `Active/Month`, CASE WHEN SUM(CASE WHEN year(s.saleTime) = {year} and month(s.saleTime) = {month} and day(s.saleTime) = {day} THEN s.grossAmount ELSE 0 END) > 0 THEN 1 ELSE 0 END AS `LD Active`, count(distinct day(s.saleTime)) as `Active Days/Store`, ROUND((COUNT(DISTINCT CONCAT(DAY(s.saleTime), HOUR(s.saleTime)))) / {day}, 2) AS `Hours/Store/Day`, ROUND(count(distinct CONCAT(DAY(s.saleTime), HOUR(s.saleTime), MINUTE(s.saleTime))) / {day}, 2) as `Min/Store/Day`, count(distinct s.uniqueInvoiceNumber) as `Total Invoices`, ROUND(COUNT(DISTINCT s.uniqueInvoiceNumber) / {day}, 2) AS `Invoice/Store/Day`, ROUND((sum(sp.Amount) / count(distinct s.uniqueInvoiceNumber)), 2) as `Value/Invoice/Store`, ROUND((count(sp.productId) / count(distinct s.uniqueInvoiceNumber)), 2) as `SKU/Invoice/Store`, ROUND(count(distinct sp.productId) / {day}, 2) as `Prod/Store/Day`, ROUND(sq.SubCat, 2) as `SubCat/Store/Day`, ROUND(sq.Cat, 2) as `Cat/Store/Day`, ROUND(sq.SupCat, 2) as `SupCat/Store/Day`, COALESCE(SUM(cr.amount), 0) as `Credit Sales`, count(distinct cr.uniqueInvoiceNumber) as `Credit Invoices`, ROUND((CASE WHEN ((0.3 * sq.Cat) / 43) * 100 > 30 THEN 30 ELSE ((0.3 * sq.Cat) / 43) * 100 END), 2) AS `Cat/D Score`, ROUND((CASE WHEN ((0.3 * ((COUNT(DISTINCT CONCAT(DAY(s.saleTime), HOUR(s.saleTime)))) / {day})) / 10) * 100 > 30 THEN 30 ELSE ((0.3 * ((COUNT(DISTINCT CONCAT(DAY(s.saleTime), HOUR(s.saleTime)))) / {day})) / 10) * 100 END), 2) AS `Hrs/D Score`, ROUND((CASE WHEN ((0.2 * (COUNT(DISTINCT s.uniqueInvoiceNumber) / {day})) / 50) * 100 > 20 THEN 20 ELSE ((0.2 * (COUNT(DISTINCT s.uniqueInvoiceNumber) / {day})) / 50) * 100 END), 2) AS `Inv/D Score`, ROUND((CASE WHEN ((0.2 * (count(sp.productId) / count(distinct s.uniqueInvoiceNumber))) / 2) * 100 > 20 THEN 20 ELSE ((0.2 * (count(sp.productId) / count(distinct s.uniqueInvoiceNumber))) / 2) * 100 END), 2) AS `SKU/Inv Score`, ROUND((CASE WHEN ((0.3 * sq.Cat) / 43) * 100 > 30 THEN 30 ELSE ((0.3 * sq.Cat) / 43) * 100 END + CASE WHEN ((0.3 * ((COUNT(DISTINCT CONCAT(DAY(s.saleTime), HOUR(s.saleTime)))) / {day})) / 10) * 100 > 30 THEN 30 ELSE ((0.3 * ((COUNT(DISTINCT CONCAT(DAY(s.saleTime), HOUR(s.saleTime)))) / {day})) / 10) * 100 END + CASE WHEN ((0.2 * (COUNT(DISTINCT s.uniqueInvoiceNumber) / {day})) / 50) * 100 > 20 THEN 20 ELSE ((0.2 * (COUNT(DISTINCT s.uniqueInvoiceNumber) / {day})) / 50) * 100 END + CASE WHEN ((0.2 * (count(sp.productId) / count(distinct s.uniqueInvoiceNumber))) / 2) * 100 > 20 THEN 20 ELSE ((0.2 * (count(sp.productId) / count(distinct s.uniqueInvoiceNumber))) / 2) * 100 END), 2) AS `Total Score` FROM (select * from sale s where year(saleTime) = {year} and month(saleTime) = {month} and day(saleTime) <= {day}) as s left join (select Id, storename, isActive from stores) st on s.storeId = st.Id left join saleproducts sp on s.Id = sp.SaleId left join (select Id, SuperCategory, Category, SubCategory from products) p on sp.productId = p.Id left join (select uniqueInvoiceNumber, amount from credit) cr on s.uniqueInvoiceNumber = cr.uniqueInvoiceNumber left join (select Id, sum(SubCat) / {day} as SubCat, sum(Cat) / {day} as Cat, sum(SupCat) / {day} as SupCat from (select s.StoreId as Id, day(s.saleTime) as day, count(distinct p.SubCategory) as SubCat, count(distinct p.Category) as Cat, count(distinct p.SuperCategory) as SupCat from sale s left join saleproducts sp on s.Id = sp.SaleId left join products p on sp.productId = p.Id where year(s.saleTime) = {year} and month(s.saleTime) = {month} and day(s.saleTime) <= {day} group by s.StoreId, day(s.saleTime)) sq group by Id) sq on st.Id = sq.Id where st.Id is not null group by st.Id, st.Storename"
    active_st_query = queries_config['query2']
    fe_wise_query = queries_config['query4']
    pr_inv_query = f'select s.storeId as Store_Id, sum(isPrinted) as `Pr.Inv Count`, sum(case when isPrinted = 1 then grossAmount else 0 end) as `Pr.Inv Sales` from sale s WHERE year(saleTime) = {year} and month(saleTime) = {month} and day(saleTime) <= {day} group by s.storeId'
    RP_st_query = f'SELECT ST.STORE_CODE AS "Store_Id", count(DISTINCT GV.ID) AS "VISITS", CASE WHEN (TO_NUMBER(TO_CHAR(max(GV.VISIT_DATE), \'YYYY\')) = {year} AND TO_NUMBER(TO_CHAR(max(GV.VISIT_DATE), \'MM\')) = {month} AND TO_NUMBER(TO_CHAR(max(GV.VISIT_DATE), \'DD\')) = {day}) THEN 1 ELSE 0 END AS "LD_Visits", max(av.Approved) AS "Approved Visits", max(ld.Approved) AS "LD_Approved" FROM GENERATED_VISIT_LOGS GV LEFT JOIN MERCHANDIZER_VISIT MV ON MV.GEN_VISIT_ID = GV.ID INNER JOIN REDBULL_RAW_STORES ST ON ST.ID = GV.STORE_ID LEFT JOIN MERCHANDIZER_CHECKOUT MC ON MC.VISIT_CODE = MV.VISIT_CODE LEFT JOIN (SELECT ST.STORE_CODE, sum(CASE WHEN ((CASE WHEN (ROUND((ACOS(ROUND(COS(ACOS(-1)/180*(90-ST.LATITUDE))*COS(ACOS(-1)/180*(90-mv.LATITUDE))+SIN(ACOS(-1)/180*(90-ST.LATITUDE))*SIN(ACOS(-1)/180*(90-MV.LATITUDE))*COS(ACOS(-1)/180*(ST.LONGITUDE-MV.LONGITUDE)), 20)) * 6371000), 2)) > 1000 THEN 0 ELSE 1 END) = 1 AND (EXTRACT(HOUR FROM (mc.CHECKOUT_TIME - mv.CHECKIN_TIME)) * 60 + EXTRACT(MINUTE FROM (mc.CHECKOUT_TIME - mv.CHECKIN_TIME))) >= 15) THEN 1 ELSE 0 END) AS Approved FROM GENERATED_VISIT_LOGS GV LEFT JOIN REDBULL_RAW_STORES ST ON ST.ID = GV.STORE_ID LEFT JOIN MERCHANDIZER_VISIT MV ON MV.GEN_VISIT_ID = GV.ID LEFT JOIN MERCHANDIZER_CHECKOUT mc ON mv.VISIT_CODE = mc.VISIT_CODE WHERE TO_NUMBER(TO_CHAR(GV.VISIT_DATE, \'YYYY\')) = {year} AND TO_NUMBER(TO_CHAR(GV.VISIT_DATE, \'MM\')) = {month} AND TO_NUMBER(TO_CHAR(GV.VISIT_DATE, \'DD\')) <= {day} AND NOT REGEXP_LIKE(ST.STORE_CODE, \'[[:alpha:]]\') AND (CASE WHEN MV.ID IS NULL THEN \'NOT AUDITED\' ELSE CASE WHEN MC.UNSUCCESSFUL_REASON IS NULL THEN \'SUCCESSFUL\' ELSE \'NOT SUCCESSFUL\' END END) = \'SUCCESSFUL\' GROUP BY ST.STORE_CODE) av ON ST.STORE_CODE = av.STORE_CODE LEFT JOIN (SELECT ST.STORE_CODE, sum(CASE WHEN ((CASE WHEN (ROUND((ACOS(ROUND(COS(ACOS(-1)/180*(90-ST.LATITUDE))*COS(ACOS(-1)/180*(90-mv.LATITUDE))+SIN(ACOS(-1)/180*(90-ST.LATITUDE))*SIN(ACOS(-1)/180*(90-MV.LATITUDE))*COS(ACOS(-1)/180*(ST.LONGITUDE-MV.LONGITUDE)), 20)) * 6371000), 2)) > 1000 THEN 0 ELSE 1 END) = 1 AND (EXTRACT(HOUR FROM (mc.CHECKOUT_TIME - mv.CHECKIN_TIME)) * 60 + EXTRACT(MINUTE FROM (mc.CHECKOUT_TIME - mv.CHECKIN_TIME))) >= 15) THEN 1 ELSE 0 END) AS Approved FROM GENERATED_VISIT_LOGS GV LEFT JOIN REDBULL_RAW_STORES ST ON ST.ID = GV.STORE_ID LEFT JOIN MERCHANDIZER_VISIT MV ON MV.GEN_VISIT_ID = GV.ID LEFT JOIN MERCHANDIZER_CHECKOUT mc ON mv.VISIT_CODE = mc.VISIT_CODE WHERE TO_NUMBER(TO_CHAR(GV.VISIT_DATE, \'YYYY\')) = {year} AND TO_NUMBER(TO_CHAR(GV.VISIT_DATE, \'MM\')) = {month} AND TO_NUMBER(TO_CHAR(GV.VISIT_DATE, \'DD\')) = {day} AND NOT REGEXP_LIKE(ST.STORE_CODE, \'[[:alpha:]]\') AND (CASE WHEN MV.ID IS NULL THEN \'NOT AUDITED\' ELSE CASE WHEN MC.UNSUCCESSFUL_REASON IS NULL THEN \'SUCCESSFUL\' ELSE \'NOT SUCCESSFUL\' END END) = \'SUCCESSFUL\' GROUP BY ST.STORE_CODE ORDER BY ST.STORE_CODE ASC) ld ON ST.STORE_CODE = ld.STORE_CODE WHERE TO_NUMBER(TO_CHAR(GV.VISIT_DATE, \'YYYY\')) = {year} AND TO_NUMBER(TO_CHAR(GV.VISIT_DATE, \'MM\')) = {month} AND TO_NUMBER(TO_CHAR(GV.VISIT_DATE, \'DD\')) <= {day} AND NOT REGEXP_LIKE(ST.STORE_CODE, \'[[:alpha:]]\') AND (CASE WHEN MV.ID IS NULL THEN \'NOT AUDITED\' ELSE CASE WHEN MC.UNSUCCESSFUL_REASON IS NULL THEN \'SUCCESSFUL\' ELSE \'NOT SUCCESSFUL\' END END) = \'SUCCESSFUL\' GROUP BY ST.STORE_CODE ORDER BY ST.STORE_CODE ASC'

    # Extraction of data 
    logging.info('..........Extracting Data Phase..........\n')
    # store_kpis_df, actice_stores_df, FE_wise_df, Pr_Inv_df, RP_st_data, RP_st_columns, FE_Att_data, FE_Att_columns, Raw_RP_st_data, Raw_RP_st_columns, Raw_Meet_data, Raw_Meet_st_columns, Raw_Att_data, Raw_Att_st_columns = Extract_Data(config, year, month, day, dt)

    # Execute and fetch query1
    logging.info("Fetching Store wise KPIs data")
    store_kpis_df = Extract_Prod(st_kpis_query)
    logging.info('Fetched')

    # Execute and fetch query2
    logging.info("Fetching Active Stores data")
    actice_stores_df = Extract_Prod(active_st_query)
    logging.info('Fetched')

    # Execute and fetch query3
    logging.info("Fetching FE wise data")
    FE_wise_df = Extract_Prod(fe_wise_query)
    logging.info('Fetched')

    # Execute and fetch query4
    logging.info("Fetching Pr.Inv data")
    Pr_Inv_df = Extract_Prod(pr_inv_query)
    logging.info('Fetched')

     # Execute and fetch query5  
    logging.info("Fetching Oracle Data - Stores")
    RP_st_data, RP_st_columns = Extract_Oracle(RP_st_query)
    logging.info('Fetched') 

    logging.info('..........Extraction phase complated..........\n')

    # Transformation of data
    logging.info('..........Transforming Data Phase..........\n')
    # OL_Summ_df, Raw_RP_st_df, FE_Att_df, Raw_Meet_df, Raw_Att_df = Transform_Data(store_kpis_df, actice_stores_df, FE_wise_df, Pr_Inv_df, RP_st_data, RP_st_columns, FE_Att_data, FE_Att_columns, Raw_RP_st_data, Raw_RP_st_columns, Raw_Meet_data, Raw_Meet_st_columns, Raw_Att_data, Raw_Att_st_columns, dt)

    logging.info('Making DataFrames of Oracle Data')
    RP_store_df = dataframe(RP_st_data, RP_st_columns)

    # Common columns in DataFrames
    common_column_df = 'Store_Id'

    logging.info('Type casting of columns')
    store_kpis_df = typecasting(store_kpis_df, common_column_df)
    actice_stores_df = typecasting(actice_stores_df, 'Store_Id')
    Pr_Inv_df = typecasting(Pr_Inv_df, 'Store_Id')
    RP_store_df = typecasting(RP_store_df, 'Store_Id')

    logging.info('Joining DataFrames')
    OL_Summ_df = leftjoin(actice_stores_df, store_kpis_df, common_column_df)
    OL_Summ_df = leftjoin(OL_Summ_df, RP_store_df, common_column_df)
    OL_Summ_df = leftjoin(OL_Summ_df, FE_wise_df, common_column_df)
    OL_Summ_df = leftjoin(OL_Summ_df, Pr_Inv_df, common_column_df)

    # Adding date column
    logging.info('Adding Date Column')
    OL_Summ_df = addingdate(OL_Summ_df, 'MTD Date', dt)

    # Convert column to datetime type
    OL_Summ_df = datetimefunc(OL_Summ_df, 'MTD Date')

    # Fill missing values with 0
    OL_Summ_df = fill(OL_Summ_df)

    # Formatiing
    columns_to_keep = [
        'Store_Id',
        'Store_Name',
        'IsActive',
        'FE_Name',
        'Supervisor',
        'MTD Date',
        'MTD',
        'Active/Month',
        'LD Active',
        'Active Days/Store',
        'Hours/Store/Day',
        'Min/Store/Day',
        'Total Invoices',
        'Invoice/Store/Day',
        'Value/Invoice/Store',
        'SKU/Invoice/Store',
        'Prod/Store/Day',
        'SubCat/Store/Day',
        'Cat/Store/Day',
        'SupCat/Store/Day',
        'VISITS',
        'Approved Visits',
        'LD_Visits',
        'LD_Approved',
        'Credit Sales',
        'Credit Invoices',
        'Pr.Inv Sales',
        'Pr.Inv Count',
        'Cat/D Score',
        'Hrs/D Score',
        'Inv/D Score',
        'SKU/Inv Score',
        'Total Score'
                ]
    
    OL_Summ_df = formatting(OL_Summ_df, columns_to_keep)

    logging.info('..........Transformation Phase completed..........\n')

    # Loading of Data
    logging.info('..........Loading Data Phase..........\n')
    Load_Data(OL_Summ_df, 'OLSummary')
    logging.info('..........Loading Phase completed..........\n')

    return OL_Summ_df, common_column_df



def FESum_Controller(config, max_dt, year, month, day):
    
    # Queries
    fe_sum_query = f""" SELECT FE_Name, Supervisor, count(distinct `Store_Id`) as `Active_Stores`, `MTD Date`, sum(`MTD`) as `MTD`, sum(`Active/Month`) as `Active/Month`, sum(`LD Active`) as `LD Active`, ROUND(avg(`Active Days/Store`),2) as `Active Days/Store`, ROUND(avg(`Hours/Store/Day`), 2) as `Hours/Store/Day`, sum(`Total Invoices`) as `Total Invoices`, ROUND(avg(`Invoice/Store/Day`), 2) as `Invoice/Store/Day`, ROUND(avg(`SKU/Invoice/Store`), 2) as `SKU/Invoice/Store`, ROUND(avg(`Cat/Store/Day`), 2) as `Cat/Store/Day`, ROUND(sum(`Cat/D Score`), 2) as `Cat/D Score`, ROUND(sum(`Hrs/D Score`), 2) as `Hrs/D Score`, ROUND(sum(`Inv/D Score`), 2) as `Inv/D Score`, ROUND(sum(`SKU/Inv Score`), 2) as `SKU/Inv Score`, ROUND(sum(`Total Score`), 2) as `Total Score` FROM `MTD-OLAP`.OLSummary where `MTD Date` = '{max_dt}' and IsActive = 1 and FE_Name not in ('1', '0', 'Demo', '') group by FE_Name """
    fe_sum2_query = f""" SELECT rv.Visit_FE, count(distinct rv.Store_Id) as Visit_Stores, count(distinct rv.Generated_Visit_Id) as Visits, ROUND(avg(rv.Difference_in_Meters), 2) as Avg_Distance, sum(rv.Range_Status) as InRange_Visits, avg(rv.Total_Time) as Avg_Time, sum(rv.Time_Status) as InTime_Visits, sum(rv.Approved) as Approved_Visits, ld.LD_Visits, ld.LD_Approved from (select *, concat(Store_Id, day(Date)) as uniquee from RawVisits where year(`Date`) = {year} and month(Date) = {month} and day(`Date`) <= '{day}' and Visit_FE = Actual_FE group by concat(Store_Id, day(Date))) rv left join (select rv.Visit_FE, count(rv.Approved) as LD_Visits, sum(rv.Approved) as LD_Approved from (select * from RawVisits where `Date` = '{max_dt}' and Visit_FE = Actual_FE group by Generated_Visit_Id) rv group by rv.Visit_FE) ld on rv.Visit_FE = ld.Visit_FE WHERE year(`Date`) = {year} and month(`Date`) = {month} and day(`Date`) <= '{day}' and rv.Visit_FE not in ('1') group by rv.Visit_FE """
    fe_att_query = f""" SELECT FE_Name, sum(case when (Meeting_Day = 1 and Meet_Approved = 1) then 1 else 0 end) as Meeting_Att, sum(case when (Meeting_Day = 0 and Att_Approved = 1) then 1 else 0 end) as Regular_Att, sum(Final_Attendance) as Total_Att FROM `MTD-OLAP`.RawAttendance WHERE year(`Date`) = {year} and month(`Date`) = {month} and day(`Date`) <= {day} group by FE_Name """

    # Extraction of Data
    fe_sum = Extract_UAT(fe_sum_query)
    fe_sum2 = Extract_UAT(fe_sum2_query)
    fe_att = Extract_UAT(fe_att_query)

    # Transformation of Data
    FE_Sum = leftjoin2(fe_sum, fe_sum2, 'FE_Name', 'Visit_FE')
    FE_Sum = leftjoin(FE_Sum, fe_att, 'FE_Name')

    FE_Sum = dropcolumn(FE_Sum, 'Visit_FE')

    FE_Sum = fill(FE_Sum)

    # Loading of Data
    Load_Data(FE_Sum, 'FESummary')

    return FE_Sum
#===================================================================================================================#======================
#   __script_name : CQBILLMATX.PY
#   __script_description : THIS SCRIPT IS USED TO GENERATE BILL PLAN DETAILS AND ITEMS
#   __primary_author__ : SRIJAYDHURGA
#   __create_date :08/30/2021
# #====================================================================================================================#===========
import re
import math  #INC08814916 - A
import datetime
from SYDATABASE import SQL
Sql = SQL()

input_data = [str(param_result.Value) for param_result in Param.CPQ_Columns]
Qt_rec_id = input_data[0]
REVISION_rec_ID = input_data[-1]

Log.Info(str(REVISION_rec_ID)+'17--BILLING MATRIX-QUOTE _ID-'+str(Qt_rec_id))
try:
    contract_quote_rec_id = input_data[0]
    #contract_quote_rec_id = Quote.GetGlobal("contract_quote_record_id")
except:
    contract_quote_rec_id = ''
try:
    quote_revision_rec_id = input_data[-1]
    #quote_revision_rec_id =Quote.GetGlobal("quote_revision_record_id")
except:
    quote_revision_rec_id =  ""

user_id = str(User.Id)
user_name = str(User.UserName)

get_round_val = 0
get_dc_cur_val = 0
getcurrency = Sql.GetFirst("SELECT GLOBAL_CURRENCY,GLOBAL_CURRENCY_RECORD_ID,DOC_CURRENCY,DOCCURR_RECORD_ID FROM SAQTRV (NOLOCK) WHERE QUOTE_RECORD_ID = '"+str(contract_quote_rec_id)+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_rec_id)+"' ")
if getcurrency:
    getcurrencysymbol = Sql.GetFirst("""SELECT ROUNDING_DECIMAL_PLACES FROM PRCURR (NOLOCK) WHERE CURRENCY_RECORD_ID = '{currencysymbol}' """.format(currencysymbol = getcurrency.GLOBAL_CURRENCY_RECORD_ID))
    getdoc_currencysymbol = Sql.GetFirst("""SELECT ROUNDING_DECIMAL_PLACES FROM PRCURR (NOLOCK) WHERE CURRENCY_RECORD_ID = '{currencysymbol}' """.format(currencysymbol = getcurrency.DOCCURR_RECORD_ID))
    if getcurrencysymbol:
        get_round_val = getcurrencysymbol.ROUNDING_DECIMAL_PLACES
    if getdoc_currencysymbol:
        get_dc_cur_val = getdoc_currencysymbol.ROUNDING_DECIMAL_PLACES

#A055S000P01-3924-billing matrix creation start
def prorate_bill_amount(service_id=None):	
    if service_id:
        for year in range(1, 6):
            Sql.RunQuery("""UPDATE SAQIBP SET BILLING_VALUE = ROUND((OQ.SUM_BILLING_VALUE / OQ.cnt) ,CONVERT(INT,CASE WHEN ROUNDING_DECIMAL_PLACES = '' THEN 0 ELSE ROUNDING_DECIMAL_PLACES END),CONVERT(INT,CASE WHEN ROUNDING_METHOD='ROUND DOWN' THEN 1 ELSE 0 END)), ESTVAL_INDT_CURR=ROUND((OQ.SUM_ESTVAL_INDT_CURR / OQ.cnt) ,CONVERT(INT,CASE WHEN ROUNDING_DECIMAL_PLACES = '' THEN 0 ELSE ROUNDING_DECIMAL_PLACES END),CONVERT(INT,CASE WHEN ROUNDING_METHOD='ROUND DOWN' THEN 1 ELSE 0 END)) 
                FROM SAQIBP 
                JOIN (
                        SELECT SUM(ISNULL(SAQIBP.BILLING_VALUE,0)) as SUM_BILLING_VALUE, 
                            SUM(ISNULL(SAQIBP.ESTVAL_INDT_CURR,0)) as SUM_ESTVAL_INDT_CURR, 
                            COUNT(SAQIBP.QUOTE_ITEM_BILLING_PLAN_RECORD_ID) as cnt, 
                            SAQIBP.QUOTE_RECORD_ID, SAQIBP.QTEREV_RECORD_ID, SAQIBP.LINE, SAQIBP.SERVICE_ID, SAQIBP.BILLING_YEAR, IQ.MIN_ID, IQ.MAX_ID
                        FROM SAQIBP (NOLOCK) 
                        JOIN (
                                SELECT DISTINCT QUOTE_RECORD_ID, QTEREV_RECORD_ID, SERVICE_ID, LINE, MAX(CpqTableEntryId) AS MAX_ID, MIN(CpqTableEntryId) AS MIN_ID, BILLING_YEAR 
                                FROM SAQIBP(NOLOCK) 
                                WHERE QUOTE_RECORD_ID='{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID = '{ServiceId}' AND BILLING_YEAR = 'YEAR {Year}'
                                GROUP BY QUOTE_RECORD_ID, QTEREV_RECORD_ID, SERVICE_ID, LINE, BILLING_YEAR
                            ) IQ ON IQ.QUOTE_RECORD_ID = SAQIBP.QUOTE_RECORD_ID AND IQ.QTEREV_RECORD_ID = SAQIBP.QTEREV_RECORD_ID AND IQ.SERVICE_ID = SAQIBP.SERVICE_ID AND IQ.LINE = SAQIBP.LINE AND IQ.BILLING_YEAR = SAQIBP.BILLING_YEAR 
                        WHERE SAQIBP.QUOTE_RECORD_ID='{QuoteRecordId}' AND SAQIBP.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQIBP.SERVICE_ID = '{ServiceId}' AND CpqTableEntryId > IQ.MIN_ID AND CpqTableEntryId < IQ.MAX_ID AND SAQIBP.BILLING_YEAR = 'YEAR {Year}' 
                        
                        GROUP BY SAQIBP.QUOTE_RECORD_ID, SAQIBP.QTEREV_RECORD_ID, SAQIBP.SERVICE_ID, SAQIBP.LINE, SAQIBP.BILLING_YEAR, IQ.MIN_ID, IQ.MAX_ID) OQ ON SAQIBP.QUOTE_RECORD_ID = OQ.QUOTE_RECORD_ID AND SAQIBP.QTEREV_RECORD_ID = OQ.QTEREV_RECORD_ID AND SAQIBP.SERVICE_ID = OQ.SERVICE_ID AND SAQIBP.LINE = OQ.LINE AND SAQIBP.BILLING_YEAR = OQ.BILLING_YEAR AND SAQIBP.CpqTableEntryId > OQ.MIN_ID AND SAQIBP.CpqTableEntryId < OQ.MAX_ID
                JOIN PRCURR (NOLOCK) ON SAQIBP.DOC_CURRENCY = PRCURR.CURRENCY 
                WHERE SAQIBP.QUOTE_RECORD_ID='{QuoteRecordId}' AND SAQIBP.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQIBP.SERVICE_ID = '{ServiceId}' AND SAQIBP.BILLING_YEAR = 'YEAR {Year}'
            """.format(QuoteRecordId=contract_quote_rec_id,RevisionRecordId=quote_revision_rec_id, ServiceId=service_id, Year=year))
            
            Sql.RunQuery("""UPDATE SAQIBP SET BILLING_VALUE_INGL_CURR = ROUND((OQ.SUM_BILLING_VALUE_INGL_CURR / OQ.cnt), CONVERT(INT,CASE WHEN ROUNDING_DECIMAL_PLACES = '' THEN 0 ELSE ROUNDING_DECIMAL_PLACES END),CONVERT(INT,CASE WHEN ROUNDING_METHOD='ROUND DOWN' THEN 1 ELSE 0 END)), ESTVAL_INGL_CURR=ROUND((OQ.SUM_ESTVAL_INGL_CURR / OQ.cnt) ,CONVERT(INT,CASE WHEN ROUNDING_DECIMAL_PLACES = '' THEN 0 ELSE ROUNDING_DECIMAL_PLACES END),CONVERT(INT,CASE WHEN ROUNDING_METHOD='ROUND DOWN' THEN 1 ELSE 0 END))
                FROM SAQIBP 
                JOIN (
                        SELECT SUM(ISNULL(BILLING_VALUE_INGL_CURR,0)) as SUM_BILLING_VALUE_INGL_CURR, 
                            SUM(ISNULL(ESTVAL_INGL_CURR,0)) as SUM_ESTVAL_INGL_CURR, 
                            COUNT(SAQIBP.QUOTE_ITEM_BILLING_PLAN_RECORD_ID) as cnt, 
                            SAQIBP.QUOTE_RECORD_ID, SAQIBP.QTEREV_RECORD_ID, SAQIBP.LINE, SAQIBP.SERVICE_ID, SAQIBP.BILLING_YEAR, IQ.MIN_ID, IQ.MAX_ID
                        FROM SAQIBP (NOLOCK) 
                        JOIN (
                                SELECT DISTINCT QUOTE_RECORD_ID, QTEREV_RECORD_ID, SERVICE_ID, LINE, MAX(CpqTableEntryId) AS MAX_ID, MIN(CpqTableEntryId) AS MIN_ID, BILLING_YEAR 
                                FROM SAQIBP(NOLOCK) 
                                WHERE QUOTE_RECORD_ID='{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID = '{ServiceId}' AND BILLING_YEAR = 'YEAR {Year}'
                                GROUP BY QUOTE_RECORD_ID, QTEREV_RECORD_ID, SERVICE_ID, LINE, BILLING_YEAR
                            ) IQ ON IQ.QUOTE_RECORD_ID = SAQIBP.QUOTE_RECORD_ID AND IQ.QTEREV_RECORD_ID = SAQIBP.QTEREV_RECORD_ID AND IQ.SERVICE_ID = SAQIBP.SERVICE_ID AND IQ.LINE = SAQIBP.LINE AND IQ.BILLING_YEAR = SAQIBP.BILLING_YEAR 
                        WHERE SAQIBP.QUOTE_RECORD_ID='{QuoteRecordId}' AND SAQIBP.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQIBP.SERVICE_ID = '{ServiceId}' AND CpqTableEntryId > IQ.MIN_ID AND CpqTableEntryId < IQ.MAX_ID AND SAQIBP.BILLING_YEAR = 'YEAR {Year}'
                        
                        GROUP BY SAQIBP.QUOTE_RECORD_ID, SAQIBP.QTEREV_RECORD_ID, SAQIBP.SERVICE_ID, SAQIBP.LINE, SAQIBP.BILLING_YEAR, IQ.MIN_ID, IQ.MAX_ID) OQ ON SAQIBP.QUOTE_RECORD_ID = OQ.QUOTE_RECORD_ID AND SAQIBP.QTEREV_RECORD_ID = OQ.QTEREV_RECORD_ID AND SAQIBP.SERVICE_ID = OQ.SERVICE_ID AND SAQIBP.LINE = OQ.LINE AND SAQIBP.BILLING_YEAR = OQ.BILLING_YEAR AND SAQIBP.CpqTableEntryId > OQ.MIN_ID AND SAQIBP.CpqTableEntryId < OQ.MAX_ID
                JOIN PRCURR (NOLOCK) ON SAQIBP.GLOBAL_CURRENCY = PRCURR.CURRENCY 
                WHERE SAQIBP.QUOTE_RECORD_ID='{QuoteRecordId}' AND SAQIBP.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQIBP.SERVICE_ID = '{ServiceId}' AND SAQIBP.BILLING_YEAR = 'YEAR {Year}'
            """.format(QuoteRecordId=contract_quote_rec_id,RevisionRecordId=quote_revision_rec_id, ServiceId=service_id, Year=year))
    # if line:
        # bill_plans_date_obj =Sql.GetList("select MAX(BILLING_DATE) as END_DATE, MIN(BILLING_DATE) as START_DATE, LINE, BILLING_YEAR from SAQIBP WHERE SAQIBP.QUOTE_RECORD_ID='{QuoteRecordId}' AND SAQIBP.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQIBP.SERVICE_ID = '{ServiceId}' AND ISNULL(SAQIBP.LINE, 0) = {Line} GROUP BY QUOTE_RECORD_ID, QTEREV_RECORD_ID, SERVICE_ID, LINE, BILLING_YEAR".format(QuoteRecordId=contract_quote_rec_id,RevisionRecordId=quote_revision_rec_id, ServiceId=service_id, Line = line))
        # for bill_plan_date_obj in bill_plans_date_obj:
            # Sql.RunQuery("UPDATE SAQIBP SET BILLING_VALUE = ROUND((IQ.SUM_BILLING_VALUE / IQ.cnt) ,CONVERT(INT,CASE WHEN ROUNDING_DECIMAL_PLACES = '' THEN 0 ELSE ROUNDING_DECIMAL_PLACES END),CONVERT(INT,CASE WHEN ROUNDING_METHOD='ROUND DOWN' THEN 1 ELSE 0 END)), ESTVAL_INDT_CURR=ROUND((IQ.SUM_ESTVAL_INDT_CURR / IQ.cnt) ,CONVERT(INT,CASE WHEN ROUNDING_DECIMAL_PLACES = '' THEN 0 ELSE ROUNDING_DECIMAL_PLACES END),CONVERT(INT,CASE WHEN ROUNDING_METHOD='ROUND DOWN' THEN 1 ELSE 0 END)) FROM SAQIBP JOIN (SELECT SUM(ISNULL(BILLING_VALUE,0)) as SUM_BILLING_VALUE, SUM(ISNULL(ESTVAL_INDT_CURR,0)) as SUM_ESTVAL_INDT_CURR, COUNT(SAQIBP.QUOTE_ITEM_BILLING_PLAN_RECORD_ID) as cnt, QUOTE_RECORD_ID, QTEREV_RECORD_ID, LINE, SERVICE_ID, BILLING_YEAR FROM SAQIBP WHERE QUOTE_RECORD_ID='{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID = '{ServiceId}' AND BILLING_DATE > '{StartDate}' AND BILLING_DATE < '{EndDate}' AND BILLING_YEAR = '{BillingYear}' AND SAQIBP.LINE = {Line} GROUP BY QUOTE_RECORD_ID, QTEREV_RECORD_ID, SERVICE_ID, LINE, BILLING_YEAR) IQ ON SAQIBP.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND SAQIBP.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND SAQIBP.SERVICE_ID = IQ.SERVICE_ID AND SAQIBP.LINE = IQ.LINE AND SAQIBP.BILLING_YEAR = IQ.BILLING_YEAR JOIN PRCURR (NOLOCK) ON SAQIBP.DOC_CURRENCY = PRCURR.CURRENCY WHERE SAQIBP.QUOTE_RECORD_ID='{QuoteRecordId}' AND SAQIBP.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQIBP.SERVICE_ID = '{ServiceId}' AND SAQIBP.BILLING_DATE > '{StartDate}' AND SAQIBP.BILLING_DATE < '{EndDate}' AND SAQIBP.BILLING_YEAR = '{BillingYear}' AND SAQIBP.LINE = {Line}".format(QuoteRecordId=contract_quote_rec_id,RevisionRecordId=quote_revision_rec_id, ServiceId=service_id, StartDate=bill_plan_date_obj.START_DATE, EndDate=bill_plan_date_obj.END_DATE, BillingYear=bill_plan_date_obj.BILLING_YEAR, Line=line))
            
            # Sql.RunQuery("UPDATE SAQIBP SET BILLING_VALUE_INGL_CURR = ROUND((IQ.SUM_BILLING_VALUE_INGL_CURR / IQ.cnt), CONVERT(INT,CASE WHEN ROUNDING_DECIMAL_PLACES = '' THEN 0 ELSE ROUNDING_DECIMAL_PLACES END),CONVERT(INT,CASE WHEN ROUNDING_METHOD='ROUND DOWN' THEN 1 ELSE 0 END)), ESTVAL_INGL_CURR=ROUND((IQ.SUM_ESTVAL_INGL_CURR / IQ.cnt) ,CONVERT(INT,CASE WHEN ROUNDING_DECIMAL_PLACES = '' THEN 0 ELSE ROUNDING_DECIMAL_PLACES END),CONVERT(INT,CASE WHEN ROUNDING_METHOD='ROUND DOWN' THEN 1 ELSE 0 END)) FROM SAQIBP JOIN (SELECT SUM(ISNULL(BILLING_VALUE_INGL_CURR,0)) as SUM_BILLING_VALUE_INGL_CURR, SUM(ISNULL(ESTVAL_INGL_CURR,0)) as SUM_ESTVAL_INGL_CURR, COUNT(SAQIBP.QUOTE_ITEM_BILLING_PLAN_RECORD_ID) as cnt, QUOTE_RECORD_ID, QTEREV_RECORD_ID, LINE, SERVICE_ID, BILLING_YEAR FROM SAQIBP WHERE QUOTE_RECORD_ID='{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID = '{ServiceId}' AND BILLING_DATE > '{StartDate}' AND BILLING_DATE < '{EndDate}' AND BILLING_YEAR = '{BillingYear}' AND SAQIBP.LINE = {Line} GROUP BY QUOTE_RECORD_ID, QTEREV_RECORD_ID, SERVICE_ID, LINE, BILLING_YEAR) IQ ON SAQIBP.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND SAQIBP.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND SAQIBP.SERVICE_ID = IQ.SERVICE_ID AND SAQIBP.LINE = IQ.LINE AND SAQIBP.BILLING_YEAR = IQ.BILLING_YEAR JOIN PRCURR (NOLOCK) ON SAQIBP.GLOBAL_CURRENCY = PRCURR.CURRENCY WHERE SAQIBP.QUOTE_RECORD_ID='{QuoteRecordId}' AND SAQIBP.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQIBP.SERVICE_ID = '{ServiceId}' AND SAQIBP.BILLING_DATE > '{StartDate}' AND SAQIBP.BILLING_DATE < '{EndDate}' AND SAQIBP.BILLING_YEAR = '{BillingYear}' AND SAQIBP.LINE = {Line}".format(QuoteRecordId=contract_quote_rec_id,RevisionRecordId=quote_revision_rec_id, ServiceId=service_id, StartDate=bill_plan_date_obj.START_DATE, EndDate=bill_plan_date_obj.END_DATE, BillingYear=bill_plan_date_obj.BILLING_YEAR, Line=line))
    return True

def get_billyears():
    bill_plan_years = Sql.GetList("SELECT DISTINCT BILLING_YEAR,SERVICE_ID from SAQIBP WHERE QUOTE_RECORD_ID = '"+str(contract_quote_rec_id)+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_rec_id)+"' ")
    for val in bill_plan_years:
        bill_year= val.BILLING_YEAR
        service_id= val.SERVICE_ID
        update_billing_plan_amt(bill_year=bill_year,service_id=service_id)
        
def update_billing_plan_amt(bill_year=None,service_id=None):
    Sql.RunQuery("""UPDATE SAQIBP SET 
                    BILLING_VALUE=CASE WHEN SAQIBP.BILLING_TYPE IN ('MILESTONE','FIXED') THEN ISNULL(SAQIBP.BILLING_VALUE, 0) + (ISNULL(SAQIBP.ANNUAL_BILLING_AMOUNT, 0) - ISNULL(IQ.SUM_BILLING_VALUE,0)) ELSE 0 END, 
                    BILLING_VALUE_INGL_CURR=CASE WHEN SAQIBP.BILLING_TYPE IN ('MILESTONE','FIXED') THEN ISNULL(SAQIBP.BILLING_VALUE_INGL_CURR, 0) + (ISNULL(SAQIBP.ANNBILAMT_INGL_CURR, 0) - ISNULL(IQ.SUM_BILLING_VALUE_INGL_CURR,0)) ELSE 0 END,
                    ESTVAL_INDT_CURR=CASE WHEN SAQIBP.BILLING_TYPE = 'VARIABLE' THEN ISNULL(SAQIBP.ESTVAL_INDT_CURR, 0) + (ISNULL(SAQIBP.ANNUAL_BILLING_AMOUNT, 0) - ISNULL(IQ.SUM_ESTVAL_INDT_CURR,0)) ELSE 0 END, 
                    ESTVAL_INGL_CURR=CASE WHEN SAQIBP.BILLING_TYPE = 'VARIABLE' THEN ISNULL(SAQIBP.ESTVAL_INGL_CURR, 0) + (ISNULL(SAQIBP.ANNBILAMT_INGL_CURR, 0) - ISNULL(IQ.SUM_ESTVAL_INGL_CURR,0)) ELSE 0 END
                FROM SAQIBP 
                JOIN (
                        SELECT 
                            SUM(ISNULL(BILLING_VALUE,0)) as SUM_BILLING_VALUE, 
                            SUM(ISNULL(BILLING_VALUE_INGL_CURR,0)) as SUM_BILLING_VALUE_INGL_CURR, 
                            SUM(ISNULL(ESTVAL_INDT_CURR,0)) as SUM_ESTVAL_INDT_CURR, 
                            SUM(ISNULL(ESTVAL_INGL_CURR,0)) as SUM_ESTVAL_INGL_CURR,                             
                            QUOTE_RECORD_ID, QTEREV_RECORD_ID, LINE, SERVICE_ID, 
                            BILLING_YEAR, MAX(CpqTableEntryId) AS MAX_ID
                        FROM SAQIBP 
                        WHERE QUOTE_RECORD_ID='{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID = '{ServiceId}' AND BILLING_YEAR = '{BillingYear}' 
                        GROUP BY QUOTE_RECORD_ID, QTEREV_RECORD_ID, SERVICE_ID, LINE, BILLING_YEAR
                    ) IQ ON SAQIBP.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND SAQIBP.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND SAQIBP.SERVICE_ID = IQ.SERVICE_ID AND SAQIBP.LINE = IQ.LINE AND SAQIBP.BILLING_YEAR = IQ.BILLING_YEAR AND SAQIBP.CpqTableEntryId = IQ.MAX_ID
                
                WHERE SAQIBP.QUOTE_RECORD_ID='{QuoteRecordId}' AND SAQIBP.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQIBP.SERVICE_ID = '{ServiceId}' AND SAQIBP.BILLING_YEAR = '{BillingYear}'""".format(QuoteRecordId=contract_quote_rec_id,RevisionRecordId=quote_revision_rec_id, ServiceId=service_id,BillingYear=bill_year))
    

def _insert_billing_matrix():	
    Sql.RunQuery("""
            INSERT SAQRIB (
            QUOTE_BILLING_PLAN_RECORD_ID,
            BILLING_END_DATE,
            BILLING_DAY,
            BILLING_STATUS,
            BILLING_START_DATE,
            QUOTE_ID,
            QUOTE_NAME,
            QUOTE_RECORD_ID,
            QTEREV_ID,
            QTEREV_RECORD_ID,
            CPQTABLEENTRYADDEDBY,
            CPQTABLEENTRYDATEADDED,
            CpqTableEntryModifiedBy,
            CpqTableEntryDateModified,
            SALESORG_ID,
            SALESORG_NAME,
            SALESORG_RECORD_ID,
            PRDOFR_ID,
            PRDOFR_RECORD_ID,
            SERVICE_ID,
            SERVICE_DESCRIPTION,
            LINE,
            PAR_SERVICE_ID,
            PAR_SERVICE_RECORD_ID
            ) 
            SELECT IQ.* FROM (
            SELECT 
            CONVERT(VARCHAR(4000),NEWID()) as QUOTE_BILLING_PLAN_RECORD_ID,
            SAQRIS.CONTRACT_VALID_TO as BILLING_END_DATE,
            'Last day of Month' as BILLING_DAY,
            'IN-PROGRESS' AS BILLING_STATUS,
            SAQRIS.CONTRACT_VALID_FROM as BILLING_START_DATE,
            SAQTMT.QUOTE_ID,
            SAQTMT.QUOTE_NAME,
            SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID as QUOTE_RECORD_ID,
            SAQTMT.QTEREV_ID as QTEREV_ID,
            SAQTMT.QTEREV_RECORD_ID as QTEREV_RECORD_ID,
            '{UserName}' AS CPQTABLEENTRYADDEDBY,
            GETDATE() as CPQTABLEENTRYDATEADDED,
            {UserId} as CpqTableEntryModifiedBy,
            GETDATE() as CpqTableEntryDateModified,
            SAQTRV.SALESORG_ID,
            SAQTRV.SALESORG_NAME,
            SAQTRV.SALESORG_RECORD_ID,
            SAQRIS.SERVICE_ID as PRDOFR_ID,
            SAQRIS.SERVICE_RECORD_ID as PRDOFR_RECORD_ID,
            SAQRIS.SERVICE_ID,
                SAQRIS.SERVICE_DESCRIPTION,
                SAQRIS.LINE,
                ISNULL(SAQRIS.PAR_SERVICE_ID,'') as PAR_SERVICE_ID,
                ISNULL(SAQRIS.PAR_SERVICE_RECORD_ID,'') as PAR_SERVICE_RECORD_ID
            FROM SAQTMT (NOLOCK) 
            JOIN SAQTRV (NOLOCK) ON SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SAQTRV.QUOTE_REVISION_RECORD_ID = SAQTMT.QTEREV_RECORD_ID
            --JOIN SAQTSV on SAQTSV.QUOTE_ID = SAQTMT.QUOTE_ID AND SAQTSV.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID 
            JOIN SAQRIS on SAQTRV.QUOTE_ID = SAQRIS.QUOTE_ID AND SAQTRV.QTEREV_RECORD_ID = SAQRIS.QTEREV_RECORD_ID AND (SAQRIS.TOTAL_AMOUNT > 0 or SAQRIS.ESTVAL_INGL_CURR > 0 or SAQRIS.SERVICE_ID in ('Z0116','Z0117'))
            WHERE SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQTMT.QTEREV_RECORD_ID = '{RevisionRecordId}'
                AND SAQRIS.SERVICE_ID NOT IN ('Z0101','A6200','Z0108','Z0110')
            ) IQ 
            LEFT JOIN SAQRIB (NOLOCK) ON SAQRIB.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND SAQRIB.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND SAQRIB.SERVICE_ID = IQ.SERVICE_ID AND ISNULL(SAQRIB.PAR_SERVICE_ID,'') = IQ.PAR_SERVICE_ID
            WHERE ISNULL(SAQRIB.SERVICE_ID,'') = ''                                      
    """.format(                        
        QuoteRecordId= contract_quote_rec_id,
        RevisionRecordId=quote_revision_rec_id,
        UserId=user_id,
        UserName=user_name
    ))	
    billingmatrix_create()
    get_billyears()
    #INC08615548 - Start - M
    return {"Response": [{"Status": "200","Message": "Billing Records Generated"}]} #INC08615548 - End - M


def insert_item_per_billing(total_months=1, billing_date='',billing_end_date ='', amount_column='YEAR_1', service_id=None,get_ent_val_type =None,get_ent_billing_type_value=None,get_billling_data_dict=None,billing_day=None,datediff=None):
    get_billing_cycle = get_billing_type = ''
    get_billing_cycle = get_billling_data_dict.get('billing_cycle')
    get_billing_type = get_billling_data_dict.get('billing_type')
    if get_billing_cycle == "Monthly":				
        get_val =12
    elif str(get_billing_cycle).upper() == "QUARTERLY":			
        get_val = 4
    elif str(get_billing_cycle).upper() == "ANNUALLY":				
        get_val = 1
    elif str(get_billing_cycle).upper() == "ONE ITEM PER QUOTE":				
        get_val = 1
    else:				
        get_val =12
    amount_column_split = amount_column.replace('_',' ')
    
    if service_id == "Z0117":
        get_total_sum  = Sql.GetFirst("SELECT SUM({amount_column}) as estsum FROM SAQRIT WHERE QUOTE_RECORD_ID='{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'  and SERVICE_ID='Z0117'".format(QuoteRecordId=contract_quote_rec_id,
        RevisionRecordId=quote_revision_rec_id,amount_column=amount_column))
        if get_total_sum and str(get_billing_type).upper() == "VARIABLE":
            #A055S000P01-20779 Start - M
            Sql.RunQuery("""INSERT SAQIBP (					
                    QUOTE_ITEM_BILLING_PLAN_RECORD_ID, BILLING_END_DATE, BILLING_START_DATE,ANNUAL_BILLING_AMOUNT,ANNBILAMT_INGL_CURR,BILADJAMT_INGL_CURR,BILADJ_DTYFLG,TTLMRG_INGL_CURR,BILLING_VALUE, BILLING_VALUE_INGL_CURR,BILLING_TYPE,LINE, QUOTE_ID,DOC_CURRENCY, QTEITM_RECORD_ID,COMMITTED_VALUE_INGL_CURR,ESTVAL_INGL_CURR,ESTVAL_INDT_CURR,
                    QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,
                    BILLING_DATE, BILLING_YEAR,BILLING_DAY,
                    EQUIPMENT_DESCRIPTION, EQUIPMENT_ID, EQUIPMENT_RECORD_ID, QTEITMCOB_RECORD_ID, 
                    SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID, SERIAL_NUMBER, WARRANTY_START_DATE, WARRANTY_END_DATE,CONTRACT_START_DATE,CONTRACT_END_DATE,UOM,STATUS,SAP_PART_NUMBER,OBJECT_TYPE,OBJECT_ID,LINE_TYPE,KIT_NUMBER,KIT_NAME,FABLOCATION_ID,COUNT_OF_ASSEMBLY,AGS_POSS_ID,UPDATED_CRM,TEMP_TOOL,PM_ID,MNTEVT_LEVEL,GOT_CODE,CUSTOMER_TOOL_ID,ASSEMBLY_ID,CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED
                ) 
                SELECT 
                    CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_BILLING_PLAN_RECORD_ID,A.* from (SELECT DISTINCT  
                    {billing_end_date} as BILLING_END_DATE,
                    {BillingDate} as BILLING_START_DATE,
                    {amount_column} AS ANNUAL_BILLING_AMOUNT,
                    {amount_column} AS ANNBILAMT_INGL_CURR,
                    {amount_column} AS BILADJAMT_INGL_CURR,
                    0 as BILADJ_DTYFLG,
                    SAQRIT.TOTAL_MARGIN AS TTLMRG_INGL_CURR,
                    0  as BILLING_VALUE,
                    0  as  BILLING_VALUE_INGL_CURR,
                    '{billing_type}' as BILLING_TYPE,
                    SAQRIT.LINE AS LINE,
                    SAQSCO.QUOTE_ID,
                    SAQRIT.DOC_CURRENCY AS DOC_CURRENCY,
                    SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID,	
                    SAQRIT.COMVAL_INGL_CURR	 as COMMITTED_VALUE_INGL_CURR,
                    CAST(ROUND(ISNULL({amount_column},0),{get_round_val})/ {get_val} AS DECIMAL(20,{get_round_val})) 	as 	ESTVAL_INGL_CURR,
                    CAST(ROUND(ISNULL({amount_column},0),{get_dc_cur_val})/ {get_val} AS DECIMAL(20,{get_dc_cur_val})) 	as 	ESTVAL_INDT_CURR,		
                    SAQSCO.QUOTE_RECORD_ID,
                    SAQSCO.QTEREV_ID,
                    SAQSCO.QTEREV_RECORD_ID,
                    {BillingDate} as BILLING_DATE,						
                    '{amount_column_split}' as BILLING_YEAR,
                    '{billing_day}' as BILLING_DAY,
                    SAQSCO.EQUIPMENT_DESCRIPTION,
                    SAQSCO.EQUIPMENT_ID,									
                    SAQSCO.EQUIPMENT_RECORD_ID,						
                    '' as QTEITMCOB_RECORD_ID,
                    SAQSCO.SERVICE_DESCRIPTION,
                    SAQSCO.SERVICE_ID,
                    SAQSCO.SERVICE_RECORD_ID, 
                    SAQRIT.GREENBOOK  as GREENBOOK,
                    SAQRIT.GREENBOOK_RECORD_ID  as  GREENBOOK_RECORD_ID,
                    SAQSCO.SERIAL_NO AS SERIAL_NUMBER,
                    SAQSCO.WARRANTY_START_DATE,
                    SAQSCO.WARRANTY_END_DATE,
                    SAQRIT.CONTRACT_VALID_FROM AS CONTRACT_START_DATE,
                    SAQRIT.CONTRACT_VALID_TO AS CONTRACT_END_DATE,
                    SAQRIT.UOM,
                    SAQRIT.STATUS,
                    SAQRIT.SAP_PART_NUMBER,
                    SAQRIT.OBJECT_TYPE,
                    SAQRIT.OBJECT_ID,
                    SAQRIT.LINE_TYPE,
                    SAQRIT.KIT_NUMBER,
                    SAQRIT.KIT_NAME,
                    SAQRIT.FABLOCATION_ID,
                    SAQRIT.COUNT_OF_ASSEMBLIES AS COUNT_OF_ASSEMBLY,
                    SAQRIT.AGS_POSS_ID,
                    SAQRIT.UPDATED_CRM,
                    SAQRIT.TEMP_TOOL,
                    SAQRIT.PM_ID,
                    SAQRIT.MNTEVT_LEVEL,
                    SAQRIT.GOT_CODE,
                    SAQRIT.CUSTOMER_TOOL_ID,
                    SAQRIT.ASSEMBLY_ID,
                    {UserId} as CPQTABLEENTRYADDEDBY, 
                    GETDATE() as CPQTABLEENTRYDATEADDED
                    FROM SAQSCO (NOLOCK) JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID and SAQRIT.QTEREV_RECORD_ID=SAQSCO.QTEREV_RECORD_ID  and SAQRIT.SERVICE_ID = SAQSCO.SERVICE_ID and SAQRIT.OBJECT_ID = SAQSCO.EQUIPMENT_ID and SAQSCO.GREENBOOK = SAQRIT.GREENBOOK LEFT JOIN SAQIBP (NOLOCK) on SAQRIT.QUOTE_RECORD_ID = SAQIBP.QUOTE_RECORD_ID and SAQRIT.QTEREV_RECORD_ID=SAQIBP.QTEREV_RECORD_ID  and SAQRIT.SERVICE_ID = SAQIBP.SERVICE_ID AND
                    EXISTS (SELECT * FROM  SAQIBP (NOLOCK) WHERE SAQIBP.ANNUAL_BILLING_AMOUNT <> SAQRIT.NET_PRICE AND SAQRIT.QUOTE_RECORD_ID = SAQIBP.QUOTE_RECORD_ID and SAQRIT.QTEREV_RECORD_ID=SAQIBP.QTEREV_RECORD_ID  and SAQRIT.SERVICE_ID = SAQIBP.SERVICE_ID)
                    WHERE SAQSCO.QUOTE_RECORD_ID='{QuoteRecordId}' AND SAQSCO.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQSCO.SERVICE_ID ='{service_id}'   and SAQRIT.ESTIMATED_VALUE  IS NOT NULL  AND SAQRIT.OBJECT_ID IS NOT NULL )A """.format(
                    UserId=user_id, QuoteRecordId=contract_quote_rec_id,
                    RevisionRecordId=quote_revision_rec_id,billing_end_date=billing_end_date,
                    BillingDate=billing_date,
                    get_val=get_val,billing_day=billing_day,
                    service_id = service_id,billing_type =get_billing_type,amount_column=get_total_sum.estsum,amount_column_split=amount_column_split,get_round_val=get_round_val,get_dc_cur_val=get_dc_cur_val))
            Sql.RunQuery("""INSERT SAQIBP (					
                        QUOTE_ITEM_BILLING_PLAN_RECORD_ID, BILLING_END_DATE, BILLING_START_DATE,ANNUAL_BILLING_AMOUNT,ANNBILAMT_INGL_CURR,BILADJAMT_INGL_CURR,BILADJ_DTYFLG,TTLMRG_INGL_CURR,BILLING_VALUE, BILLING_VALUE_INGL_CURR,BILLING_TYPE,LINE, QUOTE_ID, QTEITM_RECORD_ID, COMMITTED_VALUE_INGL_CURR,ESTVAL_INGL_CURR,DOC_CURRENCY,ESTVAL_INDT_CURR,
                        QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,
                        BILLING_DATE, BILLING_YEAR,BILLING_DAY,
                        EQUIPMENT_DESCRIPTION, EQUIPMENT_ID, EQUIPMENT_RECORD_ID, QTEITMCOB_RECORD_ID, 
                        SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID, SERIAL_NUMBER, WARRANTY_START_DATE, WARRANTY_END_DATE,CONTRACT_START_DATE,CONTRACT_END_DATE,UOM,STATUS,SAP_PART_NUMBER,OBJECT_TYPE,OBJECT_ID,LINE_TYPE,KIT_NUMBER,KIT_NAME,FABLOCATION_ID,COUNT_OF_ASSEMBLY,AGS_POSS_ID,UPDATED_CRM,TEMP_TOOL,PM_ID,MNTEVT_LEVEL,GOT_CODE,CUSTOMER_TOOL_ID,ASSEMBLY_ID,CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED
                    ) 
                    SELECT 
                        CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_BILLING_PLAN_RECORD_ID,  
                        {billing_end_date} as BILLING_END_DATE,
                        {BillingDate} as BILLING_START_DATE,
                        {amount_column} AS ANNUAL_BILLING_AMOUNT,
                        {amount_column} AS ANNBILAMT_INGL_CURR,
                        {amount_column} AS BILADJAMT_INGL_CURR,
                        0 AS BILADJ_DTYFLG,
                        TOTAL_MARGIN AS TTLMRG_INGL_CURR,
                        0  as BILLING_VALUE,
                        0  as  BILLING_VALUE_INGL_CURR,
                        '{billing_type}' as BILLING_TYPE,
                        LINE,
                        QUOTE_ID,
                        QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID,
                        
                        COMVAL_INGL_CURR as COMMITTED_VALUE_INGL_CURR,
                        CAST(ROUND(ISNULL({amount_column},0),{get_round_val})/ {get_val} AS DECIMAL(20,{get_round_val})) 	as 	ESTVAL_INGL_CURR,
                        DOC_CURRENCY AS DOC_CURRENCY,
                        CAST(ROUND(ISNULL({amount_column},0),{get_dc_cur_val})/ {get_val} AS DECIMAL(20,{get_dc_cur_val}))	as 	ESTVAL_INDT_CURR,	
                        QUOTE_RECORD_ID,
                        QTEREV_ID,
                        QTEREV_RECORD_ID,
                        {BillingDate} as BILLING_DATE,						
                        '{amount_column_split}' as BILLING_YEAR,
                        '{billing_day}' as BILLING_DAY,
                        '' as EQUIPMENT_DESCRIPTION,
                        '' as EQUIPMENT_ID,									
                        '' as EQUIPMENT_RECORD_ID,						
                        '' as QTEITMCOB_RECORD_ID,
                        SERVICE_DESCRIPTION,
                        SERVICE_ID,
                        SERVICE_RECORD_ID, 
                        GREENBOOK  as GREENBOOK,
                        GREENBOOK_RECORD_ID  as GREENBOOK_RECORD_ID,
                        '' AS SERIAL_NUMBER,
                        '' as WARRANTY_START_DATE,
                        '' as WARRANTY_END_DATE,
                        CONTRACT_VALID_FROM AS CONTRACT_START_DATE,
                        CONTRACT_VALID_TO AS CONTRACT_END_DATE,
                        UOM,
                        STATUS,
                        SAP_PART_NUMBER,
                        OBJECT_TYPE,
                        OBJECT_ID,
                        LINE_TYPE,
                        KIT_NUMBER,
                        KIT_NAME,
                        FABLOCATION_ID,
                        COUNT_OF_ASSEMBLIES AS COUNT_OF_ASSEMBLY,
                        AGS_POSS_ID,
                        UPDATED_CRM,
                        TEMP_TOOL,
                        PM_ID,
                        MNTEVT_LEVEL,
                        GOT_CODE,
                        CUSTOMER_TOOL_ID,
                        ASSEMBLY_ID,    
                        {UserId} as CPQTABLEENTRYADDEDBY, 
                        GETDATE() as CPQTABLEENTRYDATEADDED
                    FROM  SAQRIT (NOLOCK) 
                    WHERE QUOTE_RECORD_ID='{QuoteRecordId}' AND  ESTIMATED_VALUE IS NOT NULL AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID ='{service_id}' AND (OBJECT_ID  IS NULL OR OBJECT_ID = '')""".format(
                        UserId=user_id, QuoteRecordId=contract_quote_rec_id,
                        RevisionRecordId=quote_revision_rec_id,
                        BillingDate=billing_date,billing_end_date=billing_end_date,
                        get_val=get_val,billing_day=billing_day,
                        service_id = service_id,billing_type =get_billing_type,amount_column=amount_column,amount_column_split=amount_column_split,get_round_val=get_round_val,get_dc_cur_val=get_dc_cur_val))
            #A055S000P01-20779 End - M
        else:
            #A055S000P01-20779 Start - M
            Sql.RunQuery("""INSERT SAQIBP (
                    
                    QUOTE_ITEM_BILLING_PLAN_RECORD_ID, BILLING_END_DATE, BILLING_START_DATE,ANNUAL_BILLING_AMOUNT,ANNBILAMT_INGL_CURR,BILADJAMT_INGL_CURR,BILADJ_DTYFLG,TTLMRG_INGL_CURR,BILLING_VALUE, BILLING_VALUE_INGL_CURR,BILLING_TYPE,LINE, QUOTE_ID,DOC_CURRENCY, QTEITM_RECORD_ID,COMMITTED_VALUE_INGL_CURR,ESTVAL_INGL_CURR,ESTVAL_INDT_CURR,
                    QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,
                    BILLING_DATE, BILLING_YEAR,BILLING_DAY,
                    EQUIPMENT_DESCRIPTION, EQUIPMENT_ID, EQUIPMENT_RECORD_ID, QTEITMCOB_RECORD_ID, 
                    SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID, SERIAL_NUMBER, WARRANTY_START_DATE, WARRANTY_END_DATE,CONTRACT_START_DATE,CONTRACT_END_DATE,UOM,STATUS,SAP_PART_NUMBER,OBJECT_TYPE,OBJECT_ID,LINE_TYPE,KIT_NUMBER,KIT_NAME,FABLOCATION_ID,COUNT_OF_ASSEMBLY,AGS_POSS_ID,UPDATED_CRM,TEMP_TOOL,PM_ID,MNTEVT_LEVEL,GOT_CODE,CUSTOMER_TOOL_ID,ASSEMBLY_ID,CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED
                ) 
                SELECT 
                    CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_BILLING_PLAN_RECORD_ID,A.* from (SELECT DISTINCT  
                    {billing_end_date} as BILLING_END_DATE,
                    {BillingDate} as BILLING_START_DATE,
                    {amount_column} AS ANNUAL_BILLING_AMOUNT,
                    {amount_column} AS ANNBILAMT_INGL_CURR,
                    {amount_column} AS BILADJAMT_INGL_CURR,
                    0 as BILADJ_DTYFLG,
                    SAQRIT.TOTAL_MARGIN AS TTLMRG_INGL_CURR,
                    CAST(ROUND(ISNULL({amount_column},0),{get_dc_cur_val}) AS DECIMAL(20,{get_dc_cur_val}))/ {get_val}  as BILLING_VALUE,
                    CAST(ROUND(ISNULL({amount_column},0),{get_round_val}) AS DECIMAL(20,{get_round_val}))/ {get_val} as  BILLING_VALUE_INGL_CURR,
                    '{billing_type}' as BILLING_TYPE,
                    SAQRIT.LINE AS LINE,
                    SAQSCO.QUOTE_ID,
                    SAQRIT.DOC_CURRENCY AS DOC_CURRENCY,
                    SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID,	
                    SAQRIT.COMVAL_INGL_CURR	 as COMMITTED_VALUE_INGL_CURR,
                    0	as 	ESTVAL_INGL_CURR,
                    0	as 	ESTVAL_INDT_CURR,		
                    SAQSCO.QUOTE_RECORD_ID,
                    SAQSCO.QTEREV_ID,
                    SAQSCO.QTEREV_RECORD_ID,
                    {BillingDate} as BILLING_DATE,						
                    '{amount_column_split}' as BILLING_YEAR,
                    '{billing_day}' as BILLING_DAY,
                    SAQSCO.EQUIPMENT_DESCRIPTION,
                    SAQSCO.EQUIPMENT_ID,									
                    SAQSCO.EQUIPMENT_RECORD_ID,						
                    '' as QTEITMCOB_RECORD_ID,
                    SAQSCO.SERVICE_DESCRIPTION,
                    SAQSCO.SERVICE_ID,
                    SAQSCO.SERVICE_RECORD_ID, 
                    SAQRIT.GREENBOOK  as GREENBOOK,
                    SAQRIT.GREENBOOK_RECORD_ID  as  GREENBOOK_RECORD_ID,
                    SAQSCO.SERIAL_NO AS SERIAL_NUMBER,
                    SAQSCO.WARRANTY_START_DATE,
                    SAQSCO.WARRANTY_END_DATE,
                    SAQRIT.CONTRACT_VALID_FROM AS CONTRACT_START_DATE,
                    SAQRIT.CONTRACT_VALID_TO AS CONTRACT_END_DATE,
                    SAQRIT.UOM,
                    SAQRIT.STATUS,
                    SAQRIT.SAP_PART_NUMBER,
                    SAQRIT.OBJECT_TYPE,
                    SAQRIT.OBJECT_ID,
                    SAQRIT.LINE_TYPE,
                    SAQRIT.KIT_NUMBER,
                    SAQRIT.KIT_NAME,
                    SAQRIT.FABLOCATION_ID,
                    SAQRIT.COUNT_OF_ASSEMBLIES AS COUNT_OF_ASSEMBLY,
                    SAQRIT.AGS_POSS_ID,
                    SAQRIT.UPDATED_CRM,
                    SAQRIT.TEMP_TOOL,
                    SAQRIT.PM_ID,
                    SAQRIT.MNTEVT_LEVEL,
                    SAQRIT.GOT_CODE,
                    SAQRIT.CUSTOMER_TOOL_ID,
                    SAQRIT.ASSEMBLY_ID,
                    {UserId} as CPQTABLEENTRYADDEDBY, 
                    GETDATE() as CPQTABLEENTRYDATEADDED
                    FROM SAQSCO (NOLOCK) JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID and SAQRIT.QTEREV_RECORD_ID=SAQSCO.QTEREV_RECORD_ID  and SAQRIT.SERVICE_ID = SAQSCO.SERVICE_ID and SAQRIT.OBJECT_ID = SAQSCO.EQUIPMENT_ID and SAQSCO.GREENBOOK = SAQRIT.GREENBOOK LEFT JOIN SAQIBP (NOLOCK) on SAQRIT.QUOTE_RECORD_ID = SAQIBP.QUOTE_RECORD_ID and SAQRIT.QTEREV_RECORD_ID=SAQIBP.QTEREV_RECORD_ID  and SAQRIT.SERVICE_ID = SAQIBP.SERVICE_ID AND
                    EXISTS (SELECT * FROM  SAQIBP (NOLOCK) WHERE SAQIBP.ANNUAL_BILLING_AMOUNT <> SAQRIT.NET_PRICE AND SAQRIT.QUOTE_RECORD_ID = SAQIBP.QUOTE_RECORD_ID and SAQRIT.QTEREV_RECORD_ID=SAQIBP.QTEREV_RECORD_ID  and SAQRIT.SERVICE_ID = SAQIBP.SERVICE_ID)
                    WHERE SAQSCO.QUOTE_RECORD_ID='{QuoteRecordId}' AND SAQSCO.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQSCO.SERVICE_ID ='{service_id}'   and SAQRIT.ESTIMATED_VALUE  IS NOT NULL  AND SAQRIT.OBJECT_ID IS NOT NULL )A """.format(
                    UserId=user_id, QuoteRecordId=contract_quote_rec_id,
                    RevisionRecordId=quote_revision_rec_id,billing_end_date=billing_end_date,
                    BillingDate=billing_date,get_round_val=get_round_val,
                    get_val=get_val,billing_day=billing_day,get_dc_cur_val=get_dc_cur_val,
                    service_id = service_id,billing_type =get_billing_type,amount_column=get_total_sum.estsum,amount_column_split=amount_column_split))
            Sql.RunQuery("""INSERT SAQIBP (					
                        QUOTE_ITEM_BILLING_PLAN_RECORD_ID, BILLING_END_DATE, BILLING_START_DATE,ANNUAL_BILLING_AMOUNT,ANNBILAMT_INGL_CURR,BILADJAMT_INGL_CURR,BILADJ_DTYFLG,TTLMRG_INGL_CURR,BILLING_VALUE, BILLING_VALUE_INGL_CURR,BILLING_TYPE,LINE, QUOTE_ID, QTEITM_RECORD_ID, COMMITTED_VALUE_INGL_CURR,ESTVAL_INGL_CURR,DOC_CURRENCY,ESTVAL_INDT_CURR,
                        QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,
                        BILLING_DATE, BILLING_YEAR,BILLING_DAY,
                        EQUIPMENT_DESCRIPTION, EQUIPMENT_ID, EQUIPMENT_RECORD_ID, QTEITMCOB_RECORD_ID, 
                        SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID, SERIAL_NUMBER, WARRANTY_START_DATE, WARRANTY_END_DATE,CONTRACT_START_DATE,CONTRACT_END_DATE,UOM,STATUS,SAP_PART_NUMBER,OBJECT_TYPE,OBJECT_ID,LINE_TYPE,KIT_NUMBER,KIT_NAME,FABLOCATION_ID,COUNT_OF_ASSEMBLY,AGS_POSS_ID,UPDATED_CRM,TEMP_TOOL,PM_ID,MNTEVT_LEVEL,GOT_CODE,CUSTOMER_TOOL_ID,ASSEMBLY_ID,CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED
                    ) 
                    SELECT 
                        CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_BILLING_PLAN_RECORD_ID,  
                        {billing_end_date} as BILLING_END_DATE,
                        {BillingDate} as BILLING_START_DATE,
                        {amount_column} AS ANNUAL_BILLING_AMOUNT,
                        {amount_column} AS ANNBILAMT_INGL_CURR,
                        {amount_column} AS BILADJAMT_INGL_CURR,
                        0 as BILADJ_DTYFLG,
                        TOTAL_MARGIN AS TTLMRG_INGL_CURR,
                        CAST(ROUND(ISNULL({amount_column},0),{get_dc_cur_val}) AS DECIMAL(20,{get_dc_cur_val}))/ {get_val}  as BILLING_VALUE,
                        CAST(ROUND(ISNULL({amount_column},0),{get_round_val}) AS DECIMAL(20,{get_round_val}))/ {get_val} as  BILLING_VALUE_INGL_CURR,
                        '{billing_type}' as BILLING_TYPE,
                        LINE,
                        QUOTE_ID,
                        QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID,
                        
                        COMVAL_INGL_CURR as COMMITTED_VALUE_INGL_CURR,
                        0 as ESTVAL_INGL_CURR,
                        DOC_CURRENCY AS DOC_CURRENCY,
                        0 	as 	ESTVAL_INDT_CURR,	
                        QUOTE_RECORD_ID,
                        QTEREV_ID,
                        QTEREV_RECORD_ID,
                        {BillingDate} as BILLING_DATE,						
                        '{amount_column_split}' as BILLING_YEAR,
                        '{billing_day}' as BILLING_DAY,
                        '' as EQUIPMENT_DESCRIPTION,
                        '' as EQUIPMENT_ID,									
                        '' as EQUIPMENT_RECORD_ID,						
                        '' as QTEITMCOB_RECORD_ID,
                        SERVICE_DESCRIPTION,
                        SERVICE_ID,
                        SERVICE_RECORD_ID, 
                        GREENBOOK  as GREENBOOK,
                        GREENBOOK_RECORD_ID  as GREENBOOK_RECORD_ID,
                        '' AS SERIAL_NUMBER,
                        '' as WARRANTY_START_DATE,
                        '' as WARRANTY_END_DATE,
                        CONTRACT_VALID_FROM AS CONTRACT_START_DATE,
                        CONTRACT_VALID_TO AS CONTRACT_END_DATE,
                        UOM,
                        STATUS,
                        SAP_PART_NUMBER,
                        OBJECT_TYPE,
                        OBJECT_ID,
                        LINE_TYPE,
                        KIT_NUMBER,
                        KIT_NAME,
                        FABLOCATION_ID,
                        COUNT_OF_ASSEMBLIES AS COUNT_OF_ASSEMBLY,
                        AGS_POSS_ID,
                        UPDATED_CRM,
                        TEMP_TOOL,
                        PM_ID,
                        MNTEVT_LEVEL,
                        GOT_CODE,
                        CUSTOMER_TOOL_ID,
                        ASSEMBLY_ID,        
                        {UserId} as CPQTABLEENTRYADDEDBY, 
                        GETDATE() as CPQTABLEENTRYDATEADDED
                    FROM  SAQRIT (NOLOCK) 
                    WHERE QUOTE_RECORD_ID='{QuoteRecordId}' AND  ESTIMATED_VALUE IS NOT NULL AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID ='{service_id}' AND (OBJECT_ID  IS NULL OR OBJECT_ID = '')""".format(
                        UserId=user_id, QuoteRecordId=contract_quote_rec_id,
                        RevisionRecordId=quote_revision_rec_id,
                        BillingDate=billing_date,billing_end_date=billing_end_date,
                        get_val=get_val,get_round_val=get_round_val,billing_day=billing_day,
                        service_id = service_id,billing_type =get_billing_type,amount_column=amount_column,amount_column_split=amount_column_split,get_dc_cur_val=get_dc_cur_val))
        #A055S000P01-20779 End - M

def fts_z0006_z0007_insert(milestone_amt=0,milestone_date=None,service_id='',par_service_id=''):	

    mileston_percentage = str(float(milestone_amt)/100.00)  
    #A055S000P01-20779 Start - M
    Sql.RunQuery(""" INSERT SAQIBP (
                QUOTE_ITEM_BILLING_PLAN_RECORD_ID, BILLING_END_DATE, BILLING_START_DATE,ANNUAL_BILLING_AMOUNT,ANNBILAMT_INGL_CURR,BILADJAMT_INGL_CURR,BILADJ_DTYFLG,TTLMRG_INGL_CURR,BILLING_VALUE, BILLING_VALUE_INGL_CURR,BILLING_TYPE,LINE, QUOTE_ID,DOC_CURRENCY, QTEITM_RECORD_ID,COMMITTED_VALUE_INGL_CURR,ESTVAL_INGL_CURR,BILLING_DAY,
                QUOTE_RECORD_ID,GLOBAL_CURRENCY,GLOBALCURRENCY_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,
                BILLING_DATE, BILLING_YEAR,
                EQUIPMENT_DESCRIPTION, EQUIPMENT_ID, EQUIPMENT_RECORD_ID, QTEITMCOB_RECORD_ID,
                SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID, SERIAL_NUMBER, WARRANTY_START_DATE, WARRANTY_END_DATE,CONTRACT_START_DATE,CONTRACT_END_DATE,UOM,STATUS,SAP_PART_NUMBER,OBJECT_TYPE,OBJECT_ID,LINE_TYPE,KIT_NUMBER,KIT_NAME,FABLOCATION_ID,COUNT_OF_ASSEMBLY,AGS_POSS_ID,UPDATED_CRM,TEMP_TOOL,PM_ID,MNTEVT_LEVEL,GOT_CODE,CUSTOMER_TOOL_ID,ASSEMBLY_ID,PAR_SERVICE_ID,PAR_SERVICE_RECORD_ID,CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED
                )
                SELECT
                CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_BILLING_PLAN_RECORD_ID,A.* from (SELECT DISTINCT  
                SAQRIT.CONTRACT_VALID_TO as BILLING_END_DATE,
                SAQRIT.CONTRACT_VALID_FROM as BILLING_START_DATE,
                SAQRIT.NET_VALUE AS ANNUAL_BILLING_AMOUNT,
                SAQRIT.NET_VALUE_INGL_CURR AS ANNBILAMT_INGL_CURR,
                SAQRIT.NET_VALUE_INGL_CURR AS BILADJAMT_INGL_CURR,
                0 as BILADJ_DTYFLG,
                SAQRIT.TOTAL_MARGIN AS TTLMRG_INGL_CURR,
                CAST(ROUND(ISNULL(SAQRIT.NET_VALUE,0),{get_dc_cur_val})* {mileston_percentage} AS DECIMAL(20,{get_dc_cur_val})) as BILLING_VALUE,
                CAST(ROUND(ISNULL(SAQRIT.NET_VALUE_INGL_CURR,0),{get_round_val})* {mileston_percentage} AS DECIMAL(20,{get_round_val}))  as BILLING_VALUE_INGL_CURR,
                'MILESTONE' as BILLING_TYPE,
                SAQRIT.LINE AS LINE,
                SAQRIT.QUOTE_ID,
                SAQRIT.DOC_CURRENCY AS DOC_CURRENCY,
                SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID,
                SAQRIT.COMVAL_INGL_CURR as COMMITTED_VALUE_INGL_CURR,
                SAQRIT.ESTVAL_INGL_CURR as ESTVAL_INGL_CURR,
                '' as BILLING_DAY,
                SAQRIT.QUOTE_RECORD_ID,
                SAQRIT.GLOBAL_CURRENCY,
                SAQRIT.GLOBAL_CURRENCY_RECORD_ID,
                SAQRIT.QTEREV_ID,
                SAQRIT.QTEREV_RECORD_ID,
                '{BillingDate}' as BILLING_DATE,
                'YEAR 1' as BILLING_YEAR,
                '' as EQUIPMENT_DESCRIPTION,
                SAQRIT.OBJECT_ID as EQUIPMENT_ID,
                SAQRIT.EQUIPMENT_RECORD_ID as EQUIPMENT_RECORD_ID,
                '' as QTEITMCOB_RECORD_ID,
                SAQRIT.SERVICE_DESCRIPTION,
                SAQRIT.SERVICE_ID,
                SAQRIT.SERVICE_RECORD_ID,
                SAQRIT.GREENBOOK,
                SAQRIT.GREENBOOK_RECORD_ID,
                '' AS SERIAL_NUMBER,
                '' as WARRANTY_START_DATE,
                '' as WARRANTY_END_DATE,
                SAQRIT.CONTRACT_VALID_FROM AS CONTRACT_START_DATE,
                SAQRIT.CONTRACT_VALID_TO AS CONTRACT_END_DATE,
                SAQRIT.UOM,
                SAQRIT.STATUS,
                SAQRIT.SAP_PART_NUMBER,
                SAQRIT.OBJECT_TYPE,
                SAQRIT.OBJECT_ID,
                SAQRIT.LINE_TYPE,
                SAQRIT.KIT_NUMBER,
                SAQRIT.KIT_NAME,
                SAQRIT.FABLOCATION_ID,
                SAQRIT.COUNT_OF_ASSEMBLIES AS COUNT_OF_ASSEMBLY,
                SAQRIT.AGS_POSS_ID,
                SAQRIT.UPDATED_CRM,
                SAQRIT.TEMP_TOOL,
                SAQRIT.PM_ID,
                SAQRIT.MNTEVT_LEVEL,
                SAQRIT.GOT_CODE,
                SAQRIT.CUSTOMER_TOOL_ID,
                SAQRIT.ASSEMBLY_ID,
                ISNULL(SAQRIT_SELF.SERVICE_ID,'') as PAR_SERVICE_ID,
                ISNULL(SAQRIT_SELF.SERVICE_RECORD_ID,'') as PAR_SERVICE_RECORD_ID,
                {UserId} as CPQTABLEENTRYADDEDBY,
                GETDATE() as CPQTABLEENTRYDATEADDED
                FROM SAQRIT (NOLOCK) 
                LEFT JOIN SAQRIT (NOLOCK) SAQRIT_SELF ON SAQRIT_SELF.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID
                                                AND SAQRIT_SELF.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID
                                                AND SAQRIT_SELF.LINE = SAQRIT.PARQTEITM_LINE
                LEFT JOIN SAQIBP (NOLOCK) on SAQRIT.QUOTE_RECORD_ID = SAQIBP.QUOTE_RECORD_ID and SAQRIT.QTEREV_RECORD_ID=SAQIBP.QTEREV_RECORD_ID  and SAQRIT.SERVICE_ID = SAQIBP.SERVICE_ID AND ISNULL(SAQRIT_SELF.SERVICE_ID,'') = ISNULL(SAQIBP.PAR_SERVICE_ID,'') AND
                EXISTS (SELECT * FROM SAQIBP (NOLOCK) WHERE SAQIBP.ANNUAL_BILLING_AMOUNT <> SAQRIT.NET_PRICE AND SAQRIT.QUOTE_RECORD_ID = SAQIBP.QUOTE_RECORD_ID and SAQRIT.QTEREV_RECORD_ID=SAQIBP.QTEREV_RECORD_ID and SAQRIT.SERVICE_ID = SAQIBP.SERVICE_ID AND ISNULL(SAQRIT_SELF.SERVICE_ID,'') = ISNULL(SAQIBP.PAR_SERVICE_ID,''))
                WHERE SAQRIT.QUOTE_RECORD_ID='{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQRIT.SERVICE_ID ='{service_id}' AND ISNULL(SAQRIT_SELF.SERVICE_ID,'') = '{ParServiceId}' AND SAQRIT.NET_VALUE IS NOT NULL)A """.format(
                UserId=user_id, QuoteRecordId=contract_quote_rec_id,mileston_percentage=mileston_percentage,
                RevisionRecordId=quote_revision_rec_id,get_dc_cur_val=get_dc_cur_val,
                BillingDate=milestone_date,get_round_val=get_round_val,
                service_id=service_id,ParServiceId=par_service_id))
        #A055S000P01-20779 End - M

def insert_items_monthly_billing_plan_records(temp_table, service_id, par_service_id):
    ##INC08696998 M
    if str(service_id) == "Z0105":
        parr_service_id = par_service_id
        parent_service_column = "ISNULL(SAQRIT_SELF.SERVICE_ID,'') as PAR_SERVICE_ID, ISNULL(SAQRIT_SELF.SERVICE_RECORD_ID,'') as PAR_SERVICE_RECORD_ID,"
    else:
        parr_service_id = ''
        parent_service_column = "ISNULL(SAQRIT.PAR_PRDOFR_ID,'') as PAR_SERVICE_ID, ISNULL(SAQRIT.PAR_PRDOFR_RECORD_ID,'') as PAR_SERVICE_RECORD_ID,"
    #INC08696998 M
    #A055S000P01-20779 Start - M      
    Sql.RunQuery(""" INSERT SAQIBP (
                    QUOTE_ITEM_BILLING_PLAN_RECORD_ID, BILLING_END_DATE, BILLING_START_DATE,ANNUAL_BILLING_AMOUNT,ANNBILAMT_INGL_CURR,BILADJAMT_INGL_CURR,BILADJ_DTYFLG,TTLMRG_INGL_CURR,BILLING_VALUE, BILLING_VALUE_INGL_CURR,BILLING_TYPE,LINE, QUOTE_ID,DOC_CURRENCY, QTEITM_RECORD_ID,COMMITTED_VALUE_INGL_CURR,ESTVAL_INGL_CURR,ESTVAL_INDT_CURR, QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,GLOBAL_CURRENCY,GLOBALCURRENCY_RECORD_ID, BILLING_DATE, BILLING_YEAR,BILLING_DAY,EQUIPMENT_DESCRIPTION, EQUIPMENT_ID, EQUIPMENT_RECORD_ID, QTEITMCOB_RECORD_ID,SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID, SERIAL_NUMBER, WARRANTY_START_DATE, WARRANTY_END_DATE,CONTRACT_START_DATE,CONTRACT_END_DATE,UOM,STATUS,SAP_PART_NUMBER,OBJECT_TYPE,OBJECT_ID,LINE_TYPE,KIT_NUMBER,KIT_NAME,FABLOCATION_ID,COUNT_OF_ASSEMBLY,AGS_POSS_ID,UPDATED_CRM,TEMP_TOOL,PM_ID,MNTEVT_LEVEL,GOT_CODE,CUSTOMER_TOOL_ID,ASSEMBLY_ID,PAR_SERVICE_ID,PAR_SERVICE_RECORD_ID,CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED 
                    )
                    SELECT
                    CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_BILLING_PLAN_RECORD_ID,A.* from (SELECT DISTINCT  
                    TempTable.BILLING_END_DATE as BILLING_END_DATE,
                    TempTable.BILLING_START_DATE as BILLING_START_DATE,
                    CASE
                        WHEN TempTable.ANNUAL_BILLING_AMOUNT_COLUMN = 'YEAR_1' THEN CAST(ROUND(ISNULL(CAST(SAQRIT.YEAR_1 AS float),0),{DecimalPlaces}) AS DECIMAL(20,{DecimalPlaces}))
                        WHEN TempTable.ANNUAL_BILLING_AMOUNT_COLUMN = 'YEAR_2' THEN CAST(ROUND(ISNULL(CAST(SAQRIT.YEAR_2 AS float),0),{DecimalPlaces}) AS DECIMAL(20,{DecimalPlaces}))
                        WHEN TempTable.ANNUAL_BILLING_AMOUNT_COLUMN = 'YEAR_3' THEN CAST(ROUND(ISNULL(CAST(SAQRIT.YEAR_3 AS float),0),{DecimalPlaces}) AS DECIMAL(20,{DecimalPlaces}))
                        WHEN TempTable.ANNUAL_BILLING_AMOUNT_COLUMN = 'YEAR_4' THEN CAST(ROUND(ISNULL(CAST(SAQRIT.YEAR_4 AS float),0),{DecimalPlaces}) AS DECIMAL(20,{DecimalPlaces}))
                        ELSE CAST(ROUND(ISNULL(CAST(SAQRIT.YEAR_5 AS float),0),{DecimalPlaces}) AS DECIMAL(20,{DecimalPlaces}))
                    END AS ANNUAL_BILLING_AMOUNT,
                    CASE
                        WHEN TempTable.ANNUAL_BILLING_AMOUNT_COLUMN = 'YEAR_1' THEN CAST(ROUND(ISNULL(CAST(SAQRIT.YEAR_1_INGL_CURR AS float),0),{DecimalPlaces}) AS DECIMAL(20,{DecimalPlaces}))
                        WHEN TempTable.ANNUAL_BILLING_AMOUNT_COLUMN = 'YEAR_2' THEN CAST(ROUND(ISNULL(CAST(SAQRIT.YEAR_2_INGL_CURR AS float),0),{DecimalPlaces}) AS DECIMAL(20,{DecimalPlaces}))
                        WHEN TempTable.ANNUAL_BILLING_AMOUNT_COLUMN = 'YEAR_3' THEN CAST(ROUND(ISNULL(CAST(SAQRIT.YEAR_3_INGL_CURR AS float),0),{DecimalPlaces}) AS DECIMAL(20,{DecimalPlaces}))
                        WHEN TempTable.ANNUAL_BILLING_AMOUNT_COLUMN = 'YEAR_4' THEN CAST(ROUND(ISNULL(CAST(SAQRIT.YEAR_4_INGL_CURR AS float),0),{DecimalPlaces}) AS DECIMAL(20,{DecimalPlaces}))
                        ELSE CAST(ROUND(ISNULL(CAST(SAQRIT.YEAR_5_INGL_CURR AS float),0),{DecimalPlaces}) AS DECIMAL(20,{DecimalPlaces}))
                    END AS ANNBILAMT_INGL_CURR,
                    CASE
                        WHEN TempTable.ANNUAL_BILLING_AMOUNT_COLUMN = 'YEAR_1' THEN CAST(ROUND(ISNULL(CAST(SAQRIT.YEAR_1_INGL_CURR AS float),0),{DecimalPlaces}) AS DECIMAL(20,{DecimalPlaces}))
                        WHEN TempTable.ANNUAL_BILLING_AMOUNT_COLUMN = 'YEAR_2' THEN CAST(ROUND(ISNULL(CAST(SAQRIT.YEAR_2_INGL_CURR AS float),0),{DecimalPlaces}) AS DECIMAL(20,{DecimalPlaces}))
                        WHEN TempTable.ANNUAL_BILLING_AMOUNT_COLUMN = 'YEAR_3' THEN CAST(ROUND(ISNULL(CAST(SAQRIT.YEAR_3_INGL_CURR AS float),0),{DecimalPlaces}) AS DECIMAL(20,{DecimalPlaces}))
                        WHEN TempTable.ANNUAL_BILLING_AMOUNT_COLUMN = 'YEAR_4' THEN CAST(ROUND(ISNULL(CAST(SAQRIT.YEAR_4_INGL_CURR AS float),0),{DecimalPlaces}) AS DECIMAL(20,{DecimalPlaces}))
                        ELSE CAST(ROUND(ISNULL(CAST(SAQRIT.YEAR_5_INGL_CURR AS float),0),{DecimalPlaces}) AS DECIMAL(20,{DecimalPlaces}))
                    END AS BILADJAMT_INGL_CURR,
                    0 as BILADJ_DTYFLG,
                    SAQRIT.TOTAL_MARGIN AS TTLMRG_INGL_CURR,
                    CASE WHEN SAQRIT.BILLING_TYPE IN ('MILESTONE','FIXED') THEN CAST(ROUND(ISNULL(CAST(TempTable.PER_MONTH_AMT AS float),0),{get_dc_cur_val}) AS DECIMAL(20,{get_dc_cur_val})) ELSE NULL END AS BILLING_VALUE,
                    CASE WHEN SAQRIT.BILLING_TYPE IN ('MILESTONE','FIXED') THEN CAST(ROUND(ISNULL(CAST(TempTable.PER_MONTH_AMT_IN_GL_CURR AS float),0),{DecimalPlaces}) AS DECIMAL(20,{DecimalPlaces})) ELSE NULL END AS BILLING_VALUE_INGL_CURR,
                    SAQRIT.BILLING_TYPE as BILLING_TYPE,
                    SAQRIT.LINE AS LINE,
                    SAQRIT.QUOTE_ID,
                    SAQRIT.DOC_CURRENCY AS DOC_CURRENCY,
                    SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID,
                    SAQRIT.COMVAL_INGL_CURR as COMMITTED_VALUE_INGL_CURR,
                    CASE WHEN SAQRIT.BILLING_TYPE IN ('MILESTONE','FIXED') THEN NULL ELSE CAST(ROUND(ISNULL(CAST(TempTable.PER_MONTH_AMT_IN_GL_CURR AS float),0),{DecimalPlaces}) AS DECIMAL(20,{DecimalPlaces})) END as ESTVAL_INGL_CURR,
                    CASE WHEN SAQRIT.BILLING_TYPE IN ('MILESTONE','FIXED') THEN NULL ELSE CAST(ROUND(ISNULL(CAST(TempTable.PER_MONTH_AMT AS float),0),{dc_DecimalPlaces}) AS DECIMAL(20,{dc_DecimalPlaces})) END as ESTVAL_INDT_CURR,
                    SAQRIT.QUOTE_RECORD_ID,
                    SAQRIT.QTEREV_ID,
                    SAQRIT.QTEREV_RECORD_ID,
                    SAQRIT.GLOBAL_CURRENCY,
                    SAQRIT.GLOBAL_CURRENCY_RECORD_ID,
                    TempTable.BILLING_DATE as BILLING_DATE,
                    TempTable.BILLING_YEAR as BILLING_YEAR,
                    TempTable.BILLING_DAY as BILLING_DAY,
                    '' as EQUIPMENT_DESCRIPTION,
                    SAQRIT.OBJECT_ID as EQUIPMENT_ID,
                    '' as EQUIPMENT_RECORD_ID,
                    '' as QTEITMCOB_RECORD_ID,
                    SAQRIT.SERVICE_DESCRIPTION,
                    SAQRIT.SERVICE_ID,
                    SAQRIT.SERVICE_RECORD_ID,
                    SAQRIT.GREENBOOK,
                    SAQRIT.GREENBOOK_RECORD_ID,
                    '' AS SERIAL_NUMBER,
                    '' as WARRANTY_START_DATE,
                    '' as WARRANTY_END_DATE,
                    SAQRIT.CONTRACT_VALID_FROM AS CONTRACT_START_DATE,
                    SAQRIT.CONTRACT_VALID_TO AS CONTRACT_END_DATE,
                    SAQRIT.UOM,
                    SAQRIT.STATUS,
                    SAQRIT.SAP_PART_NUMBER,
                    SAQRIT.OBJECT_TYPE,
                    SAQRIT.OBJECT_ID,
                    SAQRIT.LINE_TYPE,
                    SAQRIT.KIT_NUMBER,
                    SAQRIT.KIT_NAME,
                    SAQRIT.FABLOCATION_ID,
                    SAQRIT.COUNT_OF_ASSEMBLIES AS COUNT_OF_ASSEMBLY,
                    SAQRIT.AGS_POSS_ID,
                    SAQRIT.UPDATED_CRM,
                    SAQRIT.TEMP_TOOL,
                    SAQRIT.PM_ID,
                    SAQRIT.MNTEVT_LEVEL,
                    SAQRIT.GOT_CODE,
                    SAQRIT.CUSTOMER_TOOL_ID,
                    SAQRIT.ASSEMBLY_ID,    
                    {ParentServiceColumn}
                    {UserId} as CPQTABLEENTRYADDEDBY,
                    GETDATE() as CPQTABLEENTRYDATEADDED
                    FROM SAQRIT (NOLOCK)  
                    LEFT JOIN SAQRIT (NOLOCK) SAQRIT_SELF ON SAQRIT_SELF.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID
                                                AND SAQRIT_SELF.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID
                                                AND SAQRIT_SELF.LINE = SAQRIT.PARQTEITM_LINE
                    JOIN {TempTable} (NOLOCK) TempTable ON TempTable.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND TempTable.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID AND TempTable.SERVICE_ID = SAQRIT.SERVICE_ID AND TempTable.QUOTE_REVISION_CONTRACT_ITEM_ID = SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID AND ISNULL(TempTable.PAR_SERVICE_ID,'') = ISNULL(SAQRIT_SELF.SERVICE_ID,'')
                    WHERE SAQRIT.QUOTE_RECORD_ID='{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQRIT.SERVICE_ID ='{ServiceId}' AND ISNULL(SAQRIT_SELF.SERVICE_ID,'') = '{ParServiceId}' AND ((SAQRIT.BILLING_TYPE IN ('MILESTONE','FIXED') AND SAQRIT.NET_VALUE IS NOT NULL) OR (SAQRIT.BILLING_TYPE = 'VARIABLE' OR SAQRIT.ESTIMATED_VALUE IS NOT NULL)))A """.format(TempTable=temp_table,
                    UserId=user_id, QuoteRecordId=contract_quote_rec_id,
                    RevisionRecordId=quote_revision_rec_id,
                    ServiceId = service_id, ParServiceId = parr_service_id, DecimalPlaces=get_round_val,get_dc_cur_val=get_dc_cur_val,dc_DecimalPlaces=get_dc_cur_val,ParentServiceColumn=parent_service_column))
    #A055S000P01-20779 End - M

# def insert_items_monthly_billing_plan(billing_start_date=None,billing_end_date=None,year_column=None,service_id = None,get_ent_val_type = None,get_ent_billing_type_value =None,get_billling_data_dict=None,billing_day=None,per_month_amt=None,per_month_amt_gl_curr=None,bill_service_date=None,item_record_id=None):
# 	get_billing_type = ''	
# 	year_column_split = year_column.replace('_',' ')
# 	year_amount_column_gl_curr= year_column+'_INGL_CURR'
    
# 	get_billing_cycles = Sql.GetFirst("SELECT BILLING_CYCLE,BILLING_TYPE from SAQITE  WHERE QUOTE_RECORD_ID = '"+str(contract_quote_rec_id)+"' AND SERVICE_ID='"+str(service_id)+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_rec_id)+"' ")
# 	get_billing_type = get_billing_cycles.BILLING_TYPE	
# 	if str(get_billing_type).upper() in ("MILESTONE","FIXED"):	   
        
# 		Sql.RunQuery(""" INSERT SAQIBP (
# 					QUOTE_ITEM_BILLING_PLAN_RECORD_ID, BILLING_END_DATE, BILLING_START_DATE,ANNUAL_BILLING_AMOUNT,ANNBILAMT_INGL_CURR,TTLMRG_INGL_CURR,BILLING_VALUE, BILLING_VALUE_INGL_CURR,BILLING_TYPE,LINE, QUOTE_ID,DOC_CURRENCY, QTEITM_RECORD_ID,COMMITTED_VALUE_INGL_CURR,ESTVAL_INGL_CURR,
# 					QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,GLOBAL_CURRENCY,GLOBALCURRENCY_RECORD_ID,
# 					BILLING_DATE, BILLING_YEAR,BILLING_DAY,
# 					EQUIPMENT_DESCRIPTION, EQUIPMENT_ID, EQUIPMENT_RECORD_ID, QTEITMCOB_RECORD_ID,
# 					SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID, SERIAL_NUMBER, WARRANTY_START_DATE, WARRANTY_END_DATE,CONTRACT_START_DATE,CONTRACT_END_DATE,UOM,STATUS,SAP_PART_NUMBER,OBJECT_TYPE,OBJECT_ID,LINE_TYPE,KIT_NUMBER,KIT_NAME,FABLOCATION_ID,COUNT_OF_ASSEMBLY,AGS_POSS_ID,UPDATED_CRM,TEMP_TOOL,PM_ID,MNTEVT_LEVEL,GOT_CODE,CUSTOMER_TOOL_ID,ASSEMBLY_ID,CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED
# 					)
# 					SELECT
# 					CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_BILLING_PLAN_RECORD_ID,A.* from (SELECT DISTINCT  
# 					'{billing_end_date}' as BILLING_END_DATE,
# 					'{billing_start_date}' as BILLING_START_DATE,
# 					{year_amount_column}  AS ANNUAL_BILLING_AMOUNT,
# 					{year_amount_column_gl_curr} AS ANNBILAMT_INGL_CURR,
# 					SAQRIT.TOTAL_MARGIN AS TTLMRG_INGL_CURR,
# 					CAST(ROUND(ISNULL({per_month_amt},0),{get_round_val}) AS DECIMAL(10,{get_round_val}))  as BILLING_VALUE,
# 					CAST(ROUND(ISNULL({per_month_amt_gl_curr},0),{get_round_val}) AS DECIMAL(10,{get_round_val}))    as  BILLING_VALUE_INGL_CURR,
# 					'{billing_type}' as BILLING_TYPE,
# 					SAQRIT.LINE AS LINE,
# 					SAQRIT.QUOTE_ID,
# 					SAQRIT.DOC_CURRENCY AS DOC_CURRENCY,
# 					SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID,
# 					SAQRIT.COMVAL_INGL_CURR as COMMITTED_VALUE_INGL_CURR,
# 					SAQRIT.ESTVAL_INGL_CURR as ESTVAL_INGL_CURR,
# 					SAQRIT.QUOTE_RECORD_ID,
# 					SAQRIT.QTEREV_ID,
# 					SAQRIT.QTEREV_RECORD_ID,
# 					SAQRIT.GLOBAL_CURRENCY,
# 					SAQRIT.GLOBAL_CURRENCY_RECORD_ID,
# 					'{bill_service_date}' as BILLING_DATE,
# 					'{year_column_split}' as BILLING_YEAR,
# 					'{billing_day}' as BILLING_DAY,
# 					'' as EQUIPMENT_DESCRIPTION,
# 					SAQRIT.OBJECT_ID as EQUIPMENT_ID,
# 					'' as EQUIPMENT_RECORD_ID,
# 					'' as QTEITMCOB_RECORD_ID,
# 					SAQRIT.SERVICE_DESCRIPTION,
# 					SAQRIT.SERVICE_ID,
# 					SAQRIT.SERVICE_RECORD_ID,
# 					SAQRIT.GREENBOOK,
# 					SAQRIT.GREENBOOK_RECORD_ID,
# 					'' AS SERIAL_NUMBER,
# 					'' as WARRANTY_START_DATE,
# 					'' as WARRANTY_END_DATE,
# 					SAQRIT.CONTRACT_VALID_FROM AS CONTRACT_START_DATE,
# 					SAQRIT.CONTRACT_VALID_TO AS CONTRACT_END_DATE,
# 					SAQRIT.UOM,
# 					SAQRIT.STATUS,
# 					SAQRIT.SAP_PART_NUMBER,
# 					SAQRIT.OBJECT_TYPE,
# 					SAQRIT.OBJECT_ID,
# 					SAQRIT.LINE_TYPE,
# 					SAQRIT.KIT_NUMBER,
# 					SAQRIT.KIT_NAME,
# 					SAQRIT.FABLOCATION_ID,
# 					SAQRIT.COUNT_OF_ASSEMBLIES AS COUNT_OF_ASSEMBLY,
# 					SAQRIT.AGS_POSS_ID,
# 					SAQRIT.UPDATED_CRM,
# 					SAQRIT.TEMP_TOOL,
# 					SAQRIT.PM_ID,
# 					SAQRIT.MNTEVT_LEVEL,
# 					SAQRIT.GOT_CODE,
# 					SAQRIT.CUSTOMER_TOOL_ID,
# 					SAQRIT.ASSEMBLY_ID,    
# 					{UserId} as CPQTABLEENTRYADDEDBY,
# 					GETDATE() as CPQTABLEENTRYDATEADDED
# 					FROM SAQRIT (NOLOCK)  LEFT JOIN SAQIBP (NOLOCK) on SAQRIT.QUOTE_RECORD_ID = SAQIBP.QUOTE_RECORD_ID and SAQRIT.QTEREV_RECORD_ID=SAQIBP.QTEREV_RECORD_ID  and SAQRIT.SERVICE_ID = SAQIBP.SERVICE_ID AND
# 					EXISTS (SELECT * FROM  SAQIBP (NOLOCK) WHERE SAQIBP.ANNUAL_BILLING_AMOUNT <> SAQRIT.NET_VALUE AND SAQRIT.QUOTE_RECORD_ID = SAQIBP.QUOTE_RECORD_ID and SAQRIT.QTEREV_RECORD_ID=SAQIBP.QTEREV_RECORD_ID  and SAQRIT.SERVICE_ID = SAQIBP.SERVICE_ID)
# 					WHERE SAQRIT.QUOTE_RECORD_ID='{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQRIT.SERVICE_ID ='{service_id}'  and SAQRIT.NET_VALUE IS NOT NULL    AND SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID='{item_record_id}')A """.format(
# 					UserId=user_id, QuoteRecordId=contract_quote_rec_id,
# 					RevisionRecordId=quote_revision_rec_id,per_month_amt_gl_curr=per_month_amt_gl_curr,
# 					billing_start_date=billing_start_date,bill_service_date=bill_service_date,year_amount_column=year_column,
# 					per_month_amt=per_month_amt,year_amount_column_gl_curr=year_amount_column_gl_curr,
# 					service_id = service_id,billing_day=billing_day,billing_type =get_billing_type,year_column_split=year_column_split,get_round_val=get_round_val,item_record_id=item_record_id,billing_end_date=billing_end_date))
# 	elif str(get_billing_type).upper() == "VARIABLE":
# 		Sql.RunQuery("""INSERT SAQIBP (						
# 						QUOTE_ITEM_BILLING_PLAN_RECORD_ID, BILLING_END_DATE, BILLING_START_DATE,ANNUAL_BILLING_AMOUNT,ANNBILAMT_INGL_CURR,TTLMRG_INGL_CURR,BILLING_VALUE, BILLING_VALUE_INGL_CURR,BILLING_TYPE,LINE, QUOTE_ID,DOC_CURRENCY, QTEITM_RECORD_ID,COMMITTED_VALUE_INGL_CURR,ESTVAL_INGL_CURR,ESTVAL_INDT_CURR,
# 						QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,GLOBAL_CURRENCY,GLOBALCURRENCY_RECORD_ID,
# 						BILLING_DATE, BILLING_YEAR,BILLING_DAY,
# 						EQUIPMENT_DESCRIPTION, EQUIPMENT_ID, EQUIPMENT_RECORD_ID, QTEITMCOB_RECORD_ID, 
# 						SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID, SERIAL_NUMBER, WARRANTY_START_DATE, WARRANTY_END_DATE,CONTRACT_START_DATE,CONTRACT_END_DATE,UOM,STATUS,SAP_PART_NUMBER,OBJECT_TYPE,OBJECT_ID,LINE_TYPE,KIT_NUMBER,KIT_NAME,FABLOCATION_ID,COUNT_OF_ASSEMBLY,AGS_POSS_ID,UPDATED_CRM,TEMP_TOOL,PM_ID,MNTEVT_LEVEL,GOT_CODE,CUSTOMER_TOOL_ID,ASSEMBLY_ID,CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED
# 					)SELECT 
# 						CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_BILLING_PLAN_RECORD_ID,A.* from (SELECT DISTINCT  
# 						'{billing_end_date}' as BILLING_END_DATE,
# 						'{billing_start_date}' as BILLING_START_DATE,
# 						{year_amount_column} AS ANNUAL_BILLING_AMOUNT,
# 						{year_amount_column_gl_curr} AS ANNBILAMT_INGL_CURR,
# 						SAQRIT.TOTAL_MARGIN AS TTLMRG_INGL_CURR,
# 						0  as BILLING_VALUE,
# 						0  as  BILLING_VALUE_INGL_CURR,
# 						'{billing_type}' as BILLING_TYPE,
# 						SAQRIT.LINE AS LINE,
# 						SAQRIT.QUOTE_ID,
# 						SAQRIT.DOC_CURRENCY AS DOC_CURRENCY,
# 						SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID,	
# 						SAQRIT.COMVAL_INGL_CURR	 as COMMITTED_VALUE_INGL_CURR,
# 						CAST(ROUND(ISNULL({per_month_amt_gl_curr},0),{get_round_val}) AS DECIMAL(10,{get_round_val})) as ESTVAL_INGL_CURR,
                        
# 						CAST(ROUND(ISNULL({per_month_amt},0),{get_round_val}) AS DECIMAL(10,{get_round_val}))  as ESTVAL_INDT_CURR,		
# 						SAQRIT.QUOTE_RECORD_ID,
# 						SAQRIT.QTEREV_ID,
# 						SAQRIT.QTEREV_RECORD_ID,
# 						SAQRIT.GLOBAL_CURRENCY,
# 						SAQRIT.GLOBAL_CURRENCY_RECORD_ID,
# 						'{bill_service_date}' as BILLING_DATE,
# 					'{year_column_split}' as BILLING_YEAR,
# 					'{billing_day}' as BILLING_DAY,
# 						'' as EQUIPMENT_DESCRIPTION,
# 						SAQRIT.OBJECT_ID as EQUIPMENT_ID,									
# 						'' as EQUIPMENT_RECORD_ID,						
# 						'' as QTEITMCOB_RECORD_ID,
# 						SAQRIT.SERVICE_DESCRIPTION,
# 						SAQRIT.SERVICE_ID,
# 						SAQRIT.SERVICE_RECORD_ID, 
# 						SAQRIT.GREENBOOK,
# 						SAQRIT.GREENBOOK_RECORD_ID,
# 						'' AS SERIAL_NUMBER,
# 						''  as WARRANTY_START_DATE,
# 						''  as WARRANTY_END_DATE,    
# 						SAQRIT.CONTRACT_VALID_FROM AS CONTRACT_START_DATE,
# 						SAQRIT.CONTRACT_VALID_TO AS CONTRACT_END_DATE,
# 						SAQRIT.UOM,
# 						SAQRIT.STATUS,
# 						SAQRIT.SAP_PART_NUMBER,
# 						SAQRIT.OBJECT_TYPE,
# 						SAQRIT.OBJECT_ID,
# 						SAQRIT.LINE_TYPE,
# 						SAQRIT.KIT_NUMBER,
# 						SAQRIT.KIT_NAME,
# 						SAQRIT.FABLOCATION_ID,
# 						SAQRIT.COUNT_OF_ASSEMBLIES AS COUNT_OF_ASSEMBLY,
# 						SAQRIT.AGS_POSS_ID,
# 						SAQRIT.UPDATED_CRM,
# 						SAQRIT.TEMP_TOOL,
# 						SAQRIT.PM_ID,
# 						SAQRIT.MNTEVT_LEVEL,
# 						SAQRIT.GOT_CODE,
# 						SAQRIT.CUSTOMER_TOOL_ID,
# 						SAQRIT.ASSEMBLY_ID,    
# 						{UserId} as CPQTABLEENTRYADDEDBY, 
# 						GETDATE() as CPQTABLEENTRYDATEADDED
# 						FROM  SAQRIT (NOLOCK)  LEFT JOIN SAQIBP (NOLOCK) on SAQRIT.QUOTE_RECORD_ID = SAQIBP.QUOTE_RECORD_ID and SAQRIT.QTEREV_RECORD_ID=SAQIBP.QTEREV_RECORD_ID  and SAQRIT.SERVICE_ID = SAQIBP.SERVICE_ID AND
# 						EXISTS (SELECT * FROM  SAQIBP (NOLOCK) WHERE SAQIBP.ANNUAL_BILLING_AMOUNT <> SAQRIT.NET_VALUE AND SAQRIT.QUOTE_RECORD_ID = SAQIBP.QUOTE_RECORD_ID and SAQRIT.QTEREV_RECORD_ID=SAQIBP.QTEREV_RECORD_ID  and SAQRIT.SERVICE_ID = SAQIBP.SERVICE_ID)
# 						WHERE SAQRIT.QUOTE_RECORD_ID='{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQRIT.SERVICE_ID ='{service_id}'   and SAQRIT.ESTIMATED_VALUE  IS NOT NULL  AND SAQRIT.OBJECT_ID IS NOT NULL AND SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID='{item_record_id}')A """.format(
# 					UserId=user_id, QuoteRecordId=contract_quote_rec_id,
# 					RevisionRecordId=quote_revision_rec_id,per_month_amt_gl_curr=per_month_amt_gl_curr,
# 					billing_start_date=billing_start_date,bill_service_date=bill_service_date,year_amount_column=year_column,
# 					per_month_amt=per_month_amt,year_amount_column_gl_curr=year_amount_column_gl_curr,
# 					service_id = service_id,billing_day=billing_day,billing_type =get_billing_type,year_column_split=year_column_split,get_round_val=get_round_val,item_record_id=item_record_id,billing_end_date=billing_end_date))
# 		Sql.RunQuery("""INSERT SAQIBP (					
# 					QUOTE_ITEM_BILLING_PLAN_RECORD_ID, BILLING_END_DATE, BILLING_START_DATE,ANNUAL_BILLING_AMOUNT,ANNBILAMT_INGL_CURR,TTLMRG_INGL_CURR,BILLING_VALUE, BILLING_VALUE_INGL_CURR,BILLING_TYPE,LINE, QUOTE_ID, QTEITM_RECORD_ID, COMMITTED_VALUE_INGL_CURR,ESTVAL_INGL_CURR,DOC_CURRENCY,ESTVAL_INDT_CURR,
# 					QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,
# 					BILLING_DATE, BILLING_YEAR,BILLING_DAY,
# 					EQUIPMENT_DESCRIPTION, EQUIPMENT_ID, EQUIPMENT_RECORD_ID, QTEITMCOB_RECORD_ID, 
# 					SERVICE_DESCRIPTION, SERVICE_ID,GLOBAL_CURRENCY,GLOBALCURRENCY_RECORD_ID, SERVICE_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID, SERIAL_NUMBER, WARRANTY_START_DATE, WARRANTY_END_DATE,CONTRACT_START_DATE,CONTRACT_END_DATE,UOM,STATUS,SAP_PART_NUMBER,OBJECT_TYPE,OBJECT_ID,LINE_TYPE,KIT_NUMBER,KIT_NAME,FABLOCATION_ID,COUNT_OF_ASSEMBLY,AGS_POSS_ID,UPDATED_CRM,TEMP_TOOL,PM_ID,MNTEVT_LEVEL,GOT_CODE,CUSTOMER_TOOL_ID,ASSEMBLY_ID,CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED
# 				) 
# 				SELECT 
# 					CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_BILLING_PLAN_RECORD_ID,  
# 					'{billing_end_date}' as BILLING_END_DATE,
# 					'{billing_start_date}' as BILLING_START_DATE,
# 					{year_amount_column} AS ANNUAL_BILLING_AMOUNT,
# 					{year_amount_column_gl_curr} AS ANNBILAMT_INGL_CURR,
# 					SAQRIT.TOTAL_MARGIN AS TTLMRG_INGL_CURR,
# 					0  as BILLING_VALUE,
# 					0  as  BILLING_VALUE_INGL_CURR,
# 					'{billing_type}' as BILLING_TYPE,
# 					LINE,
# 					QUOTE_ID,
# 					QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID,
                    
# 					COMVAL_INGL_CURR as COMMITTED_VALUE_INGL_CURR,
# 					CAST(ROUND(ISNULL({per_month_amt_gl_curr},0),{get_round_val}) AS DECIMAL(10,{get_round_val})) as 	ESTVAL_INGL_CURR,
# 					DOC_CURRENCY AS DOC_CURRENCY,
# 					CAST(ROUND(ISNULL({per_month_amt},0),{get_round_val}) AS DECIMAL(10,{get_round_val})) as ESTVAL_INDT_CURR,	
# 					QUOTE_RECORD_ID,
# 					QTEREV_ID,
# 					QTEREV_RECORD_ID,
# 					'{bill_service_date}' as BILLING_DATE,
# 				'{year_column_split}' as BILLING_YEAR,
# 				'{billing_day}' as BILLING_DAY,
# 					'' as EQUIPMENT_DESCRIPTION,
# 					'' as EQUIPMENT_ID,									
# 					'' as EQUIPMENT_RECORD_ID,						
# 					'' as QTEITMCOB_RECORD_ID,
# 					SERVICE_DESCRIPTION,
# 					GLOBAL_CURRENCY,
# 					SERVICE_ID,
# 					GLOBAL_CURRENCY_RECORD_ID,
# 					SERVICE_RECORD_ID, 
# 					GREENBOOK,
# 					GREENBOOK_RECORD_ID,
# 					'' AS SERIAL_NUMBER,
# 					'' as WARRANTY_START_DATE,
# 					'' as WARRANTY_END_DATE,
# 					CONTRACT_VALID_FROM AS CONTRACT_START_DATE,
# 					CONTRACT_VALID_TO AS CONTRACT_END_DATE,
# 					UOM,
# 					STATUS,
# 					SAP_PART_NUMBER,
# 					OBJECT_TYPE,
# 					OBJECT_ID,
# 					LINE_TYPE,
# 					KIT_NUMBER,
# 					KIT_NAME,
# 					FABLOCATION_ID,
# 					COUNT_OF_ASSEMBLIES AS COUNT_OF_ASSEMBLY,
# 					AGS_POSS_ID,
# 					UPDATED_CRM,
# 					TEMP_TOOL,
# 					PM_ID,
# 					MNTEVT_LEVEL,
# 					GOT_CODE,
# 					CUSTOMER_TOOL_ID,
# 					ASSEMBLY_ID,        
# 					{UserId} as CPQTABLEENTRYADDEDBY, 
# 					GETDATE() as CPQTABLEENTRYDATEADDED
# 				FROM  SAQRIT (NOLOCK) 
# 				WHERE QUOTE_RECORD_ID='{QuoteRecordId}' AND  ESTIMATED_VALUE IS NOT NULL AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID ='{service_id}' AND (OBJECT_ID  IS NULL OR OBJECT_ID = '')  AND SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID='{item_record_id}'""".format(
# 				UserId=user_id, QuoteRecordId=contract_quote_rec_id,
# 				RevisionRecordId=quote_revision_rec_id,per_month_amt_gl_curr=per_month_amt_gl_curr,
# 				billing_start_date=billing_start_date,bill_service_date=bill_service_date,year_amount_column=year_column,
# 				per_month_amt=per_month_amt,year_amount_column_gl_curr=year_amount_column_gl_curr,
# 				service_id = service_id,billing_day=billing_day,billing_type =get_billing_type,year_column_split=year_column_split,get_round_val=get_round_val,item_record_id=item_record_id,billing_end_date=billing_end_date))
# 	return True                

def insert_items_billing_plan(total_months=1, billing_date='',billing_end_date ='', amount_column='YEAR_1', service_id=None,get_ent_val_type =None,get_ent_billing_type_value=None,get_billling_data_dict=None,billing_day =None,datediff=None):
    get_billing_cycle = get_billing_type = ''
    get_billing_cycle = get_billling_data_dict.get('billing_cycle')
    get_billing_type = get_billling_data_dict.get('billing_type')
    # for data,val in get_billling_data_dict.items():
    #     if 'AGS_'+str(service_id)+'_PQB_BILCYC' in data:
    #         get_billing_cycle = val
    #     elif 'AGS_'+str(service_id)+'_PQB_BILTYP' in data:
    #         get_billing_type =val
    if str(get_billing_cycle).upper() == "QUARTERLY":
        get_val = 4
    elif str(get_billing_cycle).upper() == "ANNUALLY":
        get_val = 1
    elif str(get_billing_cycle).upper() == "WEEKLY":
        get_val = total_months
    else:
        get_val =12
    amount_column_split = amount_column.replace('_',' ')
    year_amount_column_gl_curr = amount_column+'_INGL_CURR'
    #amount_column = 'TOTAL_AMOUNT_INGL_CURR' # Hard Coded for Sprint 5	
    
    if str(get_billing_type).upper() == "FIXED" and get_billing_type != '' and service_id not in ('Z0100'):		
        #A055S000P01-20779 Start - M
        Sql.RunQuery(""" INSERT SAQIBP (
                    QUOTE_ITEM_BILLING_PLAN_RECORD_ID, BILLING_END_DATE, BILLING_START_DATE,ANNUAL_BILLING_AMOUNT,ANNBILAMT_INGL_CURR,BILADJAMT_INGL_CURR,BILADJ_DTYFLG,TTLMRG_INGL_CURR,BILLING_VALUE, BILLING_VALUE_INGL_CURR,BILLING_TYPE,LINE, QUOTE_ID,DOC_CURRENCY, QTEITM_RECORD_ID,COMMITTED_VALUE_INGL_CURR,ESTVAL_INGL_CURR,
                    QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,GLOBAL_CURRENCY,GLOBALCURRENCY_RECORD_ID,
                    BILLING_DATE, BILLING_YEAR,BILLING_DAY,
                    EQUIPMENT_DESCRIPTION, EQUIPMENT_ID, EQUIPMENT_RECORD_ID, QTEITMCOB_RECORD_ID,
                    SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID, SERIAL_NUMBER, WARRANTY_START_DATE, WARRANTY_END_DATE,CONTRACT_START_DATE,CONTRACT_END_DATE,UOM,STATUS,SAP_PART_NUMBER,OBJECT_TYPE,OBJECT_ID,LINE_TYPE,KIT_NUMBER,KIT_NAME,FABLOCATION_ID,COUNT_OF_ASSEMBLY,AGS_POSS_ID,UPDATED_CRM,TEMP_TOOL,PM_ID,MNTEVT_LEVEL,GOT_CODE,CUSTOMER_TOOL_ID,ASSEMBLY_ID,CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED
                    )
                    SELECT
                    CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_BILLING_PLAN_RECORD_ID,A.* from (SELECT DISTINCT  
                    {billing_end_date} as BILLING_END_DATE,
                    {BillingDate} as BILLING_START_DATE,
                    {amount_column} AS ANNUAL_BILLING_AMOUNT,
                    {year_amount_column_gl_curr} AS ANNBILAMT_INGL_CURR,
                    {year_amount_column_gl_curr} AS BILADJAMT_INGL_CURR,
                    0 as BILADJ_DTYFLG,
                    SAQRIT.TOTAL_MARGIN AS TTLMRG_INGL_CURR,
                    CAST(ROUND(ISNULL({amount_column},0),{get_dc_cur_val})/ {get_val} AS DECIMAL(20,{get_dc_cur_val}))   as BILLING_VALUE,
                    CAST(ROUND(ISNULL({year_amount_column_gl_curr},0),{get_round_val})/ {get_val} AS DECIMAL(20,{get_round_val})) 
                    as  BILLING_VALUE_INGL_CURR,
                    '{billing_type}' as BILLING_TYPE,
                    SAQRIT.LINE AS LINE,
                    SAQRIT.QUOTE_ID,
                    SAQRIT.DOC_CURRENCY AS DOC_CURRENCY,
                    SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID,
                    SAQRIT.COMVAL_INGL_CURR as COMMITTED_VALUE_INGL_CURR,
                    SAQRIT.ESTVAL_INGL_CURR as ESTVAL_INGL_CURR,
                    SAQRIT.QUOTE_RECORD_ID,
                    SAQRIT.QTEREV_ID,
                    SAQRIT.QTEREV_RECORD_ID,
                    SAQRIT.GLOBAL_CURRENCY,
                    SAQRIT.GLOBAL_CURRENCY_RECORD_ID,
                    {BillingDate} as BILLING_DATE,
                    '{amount_column_split}' as BILLING_YEAR,
                    '{billing_day}' as BILLING_DAY,
                    '' as EQUIPMENT_DESCRIPTION,
                    SAQRIT.OBJECT_ID as EQUIPMENT_ID,
                    '' as EQUIPMENT_RECORD_ID,
                    '' as QTEITMCOB_RECORD_ID,
                    SAQRIT.SERVICE_DESCRIPTION,
                    SAQRIT.SERVICE_ID,
                    SAQRIT.SERVICE_RECORD_ID,
                    SAQRIT.GREENBOOK,
                    SAQRIT.GREENBOOK_RECORD_ID,
                    '' AS SERIAL_NUMBER,
                    '' as WARRANTY_START_DATE,
                    '' as WARRANTY_END_DATE,
                    SAQRIT.CONTRACT_VALID_FROM AS CONTRACT_START_DATE,
                    SAQRIT.CONTRACT_VALID_TO AS CONTRACT_END_DATE,
                    SAQRIT.UOM,
                    SAQRIT.STATUS,
                    SAQRIT.SAP_PART_NUMBER,
                    SAQRIT.OBJECT_TYPE,
                    SAQRIT.OBJECT_ID,
                    SAQRIT.LINE_TYPE,
                    SAQRIT.KIT_NUMBER,
                    SAQRIT.KIT_NAME,
                    SAQRIT.FABLOCATION_ID,
                    SAQRIT.COUNT_OF_ASSEMBLIES AS COUNT_OF_ASSEMBLY,
                    SAQRIT.AGS_POSS_ID,
                    SAQRIT.UPDATED_CRM,
                    SAQRIT.TEMP_TOOL,
                    SAQRIT.PM_ID,
                    SAQRIT.MNTEVT_LEVEL,
                    SAQRIT.GOT_CODE,
                    SAQRIT.CUSTOMER_TOOL_ID,
                    SAQRIT.ASSEMBLY_ID,        
                    {UserId} as CPQTABLEENTRYADDEDBY,
                    GETDATE() as CPQTABLEENTRYDATEADDED
                    FROM SAQRIT (NOLOCK)  LEFT JOIN SAQIBP (NOLOCK) on SAQRIT.QUOTE_RECORD_ID = SAQIBP.QUOTE_RECORD_ID and SAQRIT.QTEREV_RECORD_ID=SAQIBP.QTEREV_RECORD_ID  and SAQRIT.SERVICE_ID = SAQIBP.SERVICE_ID AND
                    EXISTS (SELECT * FROM  SAQIBP (NOLOCK) WHERE SAQIBP.ANNUAL_BILLING_AMOUNT <> SAQRIT.NET_VALUE AND SAQRIT.QUOTE_RECORD_ID = SAQIBP.QUOTE_RECORD_ID and SAQRIT.QTEREV_RECORD_ID=SAQIBP.QTEREV_RECORD_ID  and SAQRIT.SERVICE_ID = SAQIBP.SERVICE_ID)
                    WHERE SAQRIT.QUOTE_RECORD_ID='{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQRIT.SERVICE_ID ='{service_id}'  and SAQRIT.NET_VALUE IS NOT NULL  and SAQRIT.OBJECT_ID IS NOT NULL )A """.format(
                    UserId=user_id, QuoteRecordId=contract_quote_rec_id,get_dc_cur_val=get_dc_cur_val,
                    RevisionRecordId=quote_revision_rec_id,billing_day=billing_day,billing_end_date=billing_end_date,
                    BillingDate=billing_date,year_amount_column_gl_curr=year_amount_column_gl_curr,
                    get_val=get_val,
                    service_id = service_id,billing_type =get_billing_type,amount_column=amount_column,amount_column_split=amount_column_split,get_round_val=get_round_val))
        Sql.RunQuery(""" INSERT SAQIBP (
                    QUOTE_ITEM_BILLING_PLAN_RECORD_ID, BILLING_END_DATE, BILLING_START_DATE,ANNUAL_BILLING_AMOUNT,ANNBILAMT_INGL_CURR,BILADJAMT_INGL_CURR,BILADJ_DTYFLG,TTLMRG_INGL_CURR,BILLING_VALUE, BILLING_VALUE_INGL_CURR,BILLING_TYPE,LINE, QUOTE_ID,DOC_CURRENCY, QTEITM_RECORD_ID,COMMITTED_VALUE_INGL_CURR,ESTVAL_INGL_CURR,
                    QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,GLOBAL_CURRENCY,GLOBALCURRENCY_RECORD_ID,
                    BILLING_DATE, BILLING_YEAR,BILLING_DAY,
                    EQUIPMENT_DESCRIPTION, EQUIPMENT_ID, EQUIPMENT_RECORD_ID, QTEITMCOB_RECORD_ID,
                    SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID, SERIAL_NUMBER, WARRANTY_START_DATE, WARRANTY_END_DATE,CONTRACT_START_DATE,CONTRACT_END_DATE,UOM,STATUS,SAP_PART_NUMBER,OBJECT_TYPE,OBJECT_ID,LINE_TYPE,KIT_NUMBER,KIT_NAME,FABLOCATION_ID,COUNT_OF_ASSEMBLY,AGS_POSS_ID,UPDATED_CRM,TEMP_TOOL,PM_ID,MNTEVT_LEVEL,GOT_CODE,CUSTOMER_TOOL_ID,ASSEMBLY_ID,CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED
                    )
                    SELECT
                    CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_BILLING_PLAN_RECORD_ID,A.* from (SELECT DISTINCT  
                    {billing_end_date} as BILLING_END_DATE,
                    {BillingDate} as BILLING_START_DATE,
                    {amount_column} AS ANNUAL_BILLING_AMOUNT,
                    {year_amount_column_gl_curr} AS ANNBILAMT_INGL_CURR,
                    {year_amount_column_gl_curr} AS BILADJAMT_INGL_CURR,
                    0 as BILADJ_DTYFLG,
                    SAQRIT.TOTAL_MARGIN AS TTLMRG_INGL_CURR,
                    CAST(ROUND(ISNULL({amount_column},0),{get_dc_cur_val})/ {get_val} AS DECIMAL(20,{get_dc_cur_val}))   as BILLING_VALUE,
                    CAST(ROUND(ISNULL({year_amount_column_gl_curr},0),{get_round_val})/ {get_val} AS DECIMAL(20,{get_round_val})) 
                    as  BILLING_VALUE_INGL_CURR,
                    '{billing_type}' as BILLING_TYPE,
                    SAQRIT.LINE AS LINE,
                    SAQRIT.QUOTE_ID,
                    SAQRIT.DOC_CURRENCY AS DOC_CURRENCY,
                    SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID,
                    SAQRIT.COMVAL_INGL_CURR as COMMITTED_VALUE_INGL_CURR,
                    SAQRIT.ESTVAL_INGL_CURR as ESTVAL_INGL_CURR,
                    SAQRIT.QUOTE_RECORD_ID,
                    SAQRIT.QTEREV_ID,
                    SAQRIT.QTEREV_RECORD_ID,
                    SAQRIT.GLOBAL_CURRENCY,
                    SAQRIT.GLOBAL_CURRENCY_RECORD_ID,
                    {BillingDate} as BILLING_DATE,
                    '{amount_column_split}' as BILLING_YEAR,
                    '{billing_day}' as BILLING_DAY,
                    '' as EQUIPMENT_DESCRIPTION,
                    SAQRIT.OBJECT_ID as EQUIPMENT_ID,
                    '' as EQUIPMENT_RECORD_ID,
                    '' as QTEITMCOB_RECORD_ID,
                    SAQRIT.SERVICE_DESCRIPTION,
                    SAQRIT.SERVICE_ID,
                    SAQRIT.SERVICE_RECORD_ID,
                    SAQRIT.GREENBOOK,
                    SAQRIT.GREENBOOK_RECORD_ID,
                    '' AS SERIAL_NUMBER,
                    '' as WARRANTY_START_DATE,
                    '' as WARRANTY_END_DATE,
                    SAQRIT.CONTRACT_VALID_FROM AS CONTRACT_START_DATE,
                    SAQRIT.CONTRACT_VALID_TO AS CONTRACT_END_DATE,
                    SAQRIT.UOM,
                    SAQRIT.STATUS,
                    SAQRIT.SAP_PART_NUMBER,
                    SAQRIT.OBJECT_TYPE,
                    SAQRIT.OBJECT_ID,
                    SAQRIT.LINE_TYPE,
                    SAQRIT.KIT_NUMBER,
                    SAQRIT.KIT_NAME,
                    SAQRIT.FABLOCATION_ID,
                    SAQRIT.COUNT_OF_ASSEMBLIES AS COUNT_OF_ASSEMBLY,
                    SAQRIT.AGS_POSS_ID,
                    SAQRIT.UPDATED_CRM,
                    SAQRIT.TEMP_TOOL,
                    SAQRIT.PM_ID,
                    SAQRIT.MNTEVT_LEVEL,
                    SAQRIT.GOT_CODE,
                    SAQRIT.CUSTOMER_TOOL_ID,
                    SAQRIT.ASSEMBLY_ID,        
                    {UserId} as CPQTABLEENTRYADDEDBY,
                    GETDATE() as CPQTABLEENTRYDATEADDED
                    FROM SAQRIT (NOLOCK)  LEFT JOIN SAQIBP (NOLOCK) on SAQRIT.QUOTE_RECORD_ID = SAQIBP.QUOTE_RECORD_ID and SAQRIT.QTEREV_RECORD_ID=SAQIBP.QTEREV_RECORD_ID  and SAQRIT.SERVICE_ID = SAQIBP.SERVICE_ID AND
                    EXISTS (SELECT * FROM  SAQIBP (NOLOCK) WHERE SAQIBP.ANNUAL_BILLING_AMOUNT <> SAQRIT.NET_VALUE AND SAQRIT.QUOTE_RECORD_ID = SAQIBP.QUOTE_RECORD_ID and SAQRIT.QTEREV_RECORD_ID=SAQIBP.QTEREV_RECORD_ID  and SAQRIT.SERVICE_ID = SAQIBP.SERVICE_ID)
                    WHERE SAQRIT.QUOTE_RECORD_ID='{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQRIT.SERVICE_ID ='{service_id}'  and SAQRIT.NET_VALUE IS NOT NULL  and ISNULL(SAQRIT.OBJECT_ID,'') = '' )A """.format(
                    UserId=user_id, QuoteRecordId=contract_quote_rec_id,get_dc_cur_val=get_dc_cur_val,
                    RevisionRecordId=quote_revision_rec_id,billing_day=billing_day,billing_end_date=billing_end_date,
                    BillingDate=billing_date,
                    get_val=get_val,year_amount_column_gl_curr=year_amount_column_gl_curr,
                    service_id = service_id,billing_type =get_billing_type,amount_column=amount_column,amount_column_split=amount_column_split,get_round_val=get_round_val))
        #A055S000P01-20779 End - M
    elif str(get_billing_type).upper() == "MILESTONE" and service_id not in ('Z0007','Z0009','Z0123'):
        #A055S000P01-20779 Start - M
        Sql.RunQuery(""" INSERT SAQIBP (
                    QUOTE_ITEM_BILLING_PLAN_RECORD_ID, BILLING_END_DATE, BILLING_START_DATE,ANNUAL_BILLING_AMOUNT,ANNBILAMT_INGL_CURR,BILADJAMT_INGL_CURR,BILADJ_DTYFLG,TTLMRG_INGL_CURR,BILLING_VALUE, BILLING_VALUE_INGL_CURR,BILLING_TYPE,LINE, QUOTE_ID, QTEITM_RECORD_ID,COMMITTED_VALUE_INGL_CURR,ESTVAL_INGL_CURR,
                    QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,GLOBAL_CURRENCY,GLOBALCURRENCY_RECORD_ID,
                    BILLING_DATE, BILLING_YEAR,DOC_CURRENCY,BILLING_DAY,
                    EQUIPMENT_DESCRIPTION, EQUIPMENT_ID, EQUIPMENT_RECORD_ID, QTEITMCOB_RECORD_ID,
                    SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID, SERIAL_NUMBER, WARRANTY_START_DATE, WARRANTY_END_DATE,CONTRACT_START_DATE,CONTRACT_END_DATE,UOM,STATUS,SAP_PART_NUMBER,OBJECT_TYPE,OBJECT_ID,LINE_TYPE,KIT_NUMBER,KIT_NAME,FABLOCATION_ID,COUNT_OF_ASSEMBLY,AGS_POSS_ID,UPDATED_CRM,TEMP_TOOL,PM_ID,MNTEVT_LEVEL,GOT_CODE,CUSTOMER_TOOL_ID,ASSEMBLY_ID,CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED
                    )
                    SELECT
                    CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_BILLING_PLAN_RECORD_ID,A.* from (SELECT DISTINCT  
                    {billing_end_date} as BILLING_END_DATE,
                    {BillingDate} as BILLING_START_DATE,
                    {amount_column} AS ANNUAL_BILLING_AMOUNT,
                    {year_amount_column_gl_curr} AS ANNBILAMT_INGL_CURR,
                    {year_amount_column_gl_curr} AS BILADJAMT_INGL_CURR,
                    0 as BILADJ_DTYFLG,
                    SAQRIT.TOTAL_MARGIN AS TTLMRG_INGL_CURR,
                    CAST(ROUND(ISNULL({amount_column},0),{get_dc_cur_val})/ {get_val} AS DECIMAL(20,{get_dc_cur_val}))  as BILLING_VALUE,
                    CAST(ROUND(ISNULL({year_amount_column_gl_curr},0),{get_round_val})/ {get_val} AS DECIMAL(20,{get_round_val}))   as  BILLING_VALUE_INGL_CURR,
                    '{billing_type}' as BILLING_TYPE,
                    SAQRIT.LINE AS LINE,
                    SAQSCO.QUOTE_ID,
                    SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID,
                    SAQRIT.COMVAL_INGL_CURR as COMMITTED_VALUE_INGL_CURR,
                    SAQRIT.ESTVAL_INGL_CURR as ESTVAL_INGL_CURR,
                    SAQSCO.QUOTE_RECORD_ID,
                    SAQSCO.QTEREV_ID,
                    SAQSCO.QTEREV_RECORD_ID,
                    SAQRIT.GLOBAL_CURRENCY,
                    SAQRIT.GLOBAL_CURRENCY_RECORD_ID,
                    {BillingDate} as BILLING_DATE,
                    '{amount_column_split}' as BILLING_YEAR,
                    SAQRIT.DOC_CURRENCY,
                    '{billing_day}' as BILLING_DAY,
                    SAQSCO.EQUIPMENT_DESCRIPTION,
                    SAQSCO.EQUIPMENT_ID,
                    SAQSCO.EQUIPMENT_RECORD_ID,
                    '' as QTEITMCOB_RECORD_ID,
                    SAQSCO.SERVICE_DESCRIPTION,
                    SAQSCO.SERVICE_ID,
                    SAQSCO.SERVICE_RECORD_ID,
                    SAQSCO.GREENBOOK,
                    SAQSCO.GREENBOOK_RECORD_ID,
                    SAQSCO.SERIAL_NO AS SERIAL_NUMBER,
                    SAQSCO.WARRANTY_START_DATE,
                    SAQSCO.WARRANTY_END_DATE,
                    SAQRIT.CONTRACT_VALID_FROM AS CONTRACT_START_DATE,
                    SAQRIT.CONTRACT_VALID_TO AS CONTRACT_END_DATE,
                    SAQRIT.UOM,
                    SAQRIT.STATUS,
                    SAQRIT.SAP_PART_NUMBER,
                    SAQRIT.OBJECT_TYPE,
                    SAQRIT.OBJECT_ID,
                    SAQRIT.LINE_TYPE,
                    SAQRIT.KIT_NUMBER,
                    SAQRIT.KIT_NAME,
                    SAQRIT.FABLOCATION_ID,
                    SAQRIT.COUNT_OF_ASSEMBLIES AS COUNT_OF_ASSEMBLY,
                    SAQRIT.AGS_POSS_ID,
                    SAQRIT.UPDATED_CRM,
                    SAQRIT.TEMP_TOOL,
                    SAQRIT.PM_ID,
                    SAQRIT.MNTEVT_LEVEL,
                    SAQRIT.GOT_CODE,
                    SAQRIT.CUSTOMER_TOOL_ID,
                    SAQRIT.ASSEMBLY_ID,        
                    {UserId} as CPQTABLEENTRYADDEDBY,
                    GETDATE() as CPQTABLEENTRYDATEADDED
                    FROM SAQSCO (NOLOCK) JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID and SAQRIT.QTEREV_RECORD_ID=SAQSCO.QTEREV_RECORD_ID  and SAQRIT.SERVICE_ID = SAQSCO.SERVICE_ID  and SAQSCO.GREENBOOK = SAQRIT.GREENBOOK LEFT JOIN SAQIBP (NOLOCK) on SAQRIT.QUOTE_RECORD_ID = SAQIBP.QUOTE_RECORD_ID and SAQRIT.QTEREV_RECORD_ID=SAQIBP.QTEREV_RECORD_ID  and SAQRIT.SERVICE_ID = SAQIBP.SERVICE_ID AND
                    EXISTS (SELECT * FROM  SAQIBP (NOLOCK) WHERE SAQIBP.ANNUAL_BILLING_AMOUNT <> SAQRIT.NET_PRICE AND SAQRIT.QUOTE_RECORD_ID = SAQIBP.QUOTE_RECORD_ID and SAQRIT.QTEREV_RECORD_ID=SAQIBP.QTEREV_RECORD_ID  and SAQRIT.SERVICE_ID = SAQIBP.SERVICE_ID)
                    WHERE SAQSCO.QUOTE_RECORD_ID='{QuoteRecordId}' AND SAQSCO.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQSCO.SERVICE_ID ='{service_id}'  and SAQRIT.NET_VALUE IS NOT NULL and SAQRIT.OBJECT_ID IS NOT NULL )A """.format(
                    UserId=user_id, QuoteRecordId=contract_quote_rec_id,billing_day=billing_day,
                    RevisionRecordId=quote_revision_rec_id,get_dc_cur_val=get_dc_cur_val,
                    BillingDate=billing_date,billing_end_date=billing_end_date,
                    get_val=get_val,year_amount_column_gl_curr=year_amount_column_gl_curr,
                    service_id = service_id,billing_type =get_billing_type,amount_column=amount_column,amount_column_split=amount_column_split,get_round_val=get_round_val))
        Sql.RunQuery(""" INSERT SAQIBP (
                    QUOTE_ITEM_BILLING_PLAN_RECORD_ID, BILLING_END_DATE, BILLING_START_DATE,ANNUAL_BILLING_AMOUNT,ANNBILAMT_INGL_CURR,BILADJAMT_INGL_CURR,BILADJ_DTYFLG,TTLMRG_INGL_CURR,BILLING_VALUE, BILLING_VALUE_INGL_CURR,BILLING_TYPE,LINE, QUOTE_ID,DOC_CURRENCY, QTEITM_RECORD_ID,COMMITTED_VALUE_INGL_CURR,ESTVAL_INGL_CURR,
                    QUOTE_RECORD_ID,GLOBAL_CURRENCY,GLOBALCURRENCY_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,
                    BILLING_DATE, BILLING_YEAR,BILLING_DAY,
                    EQUIPMENT_DESCRIPTION, EQUIPMENT_ID, EQUIPMENT_RECORD_ID, QTEITMCOB_RECORD_ID,
                    SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID, SERIAL_NUMBER, WARRANTY_START_DATE, WARRANTY_END_DATE,CONTRACT_START_DATE,CONTRACT_END_DATE,UOM,STATUS,SAP_PART_NUMBER,OBJECT_TYPE,OBJECT_ID,LINE_TYPE,KIT_NUMBER,KIT_NAME,FABLOCATION_ID,COUNT_OF_ASSEMBLY,AGS_POSS_ID,UPDATED_CRM,TEMP_TOOL,PM_ID,MNTEVT_LEVEL,GOT_CODE,CUSTOMER_TOOL_ID,ASSEMBLY_ID,CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED
                    )
                    SELECT
                    CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_BILLING_PLAN_RECORD_ID,A.* from (SELECT DISTINCT  
                    {billing_end_date} as BILLING_END_DATE,
                    {BillingDate} as BILLING_START_DATE,
                    {amount_column} AS ANNUAL_BILLING_AMOUNT,
                    {year_amount_column_gl_curr} AS ANNBILAMT_INGL_CURR,
                    {year_amount_column_gl_curr} AS BILADJAMT_INGL_CURR,
                    0 as BILADJ_DTYFLG,
                    SAQRIT.TOTAL_MARGIN AS TTLMRG_INGL_CURR,
                    CAST(ROUND(ISNULL({amount_column},0),{get_dc_cur_val})/ {get_val} AS DECIMAL(20,{get_dc_cur_val}))  as BILLING_VALUE,
                    CAST(ROUND(ISNULL({year_amount_column_gl_curr},0),{get_round_val})/ {get_val} AS DECIMAL(20,{get_round_val}))
                    as  BILLING_VALUE_INGL_CURR,
                    '{billing_type}' as BILLING_TYPE,
                    SAQRIT.LINE AS LINE,
                    SAQRIT.QUOTE_ID,
                    SAQRIT.DOC_CURRENCY AS DOC_CURRENCY,
                    SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID,
                    SAQRIT.COMVAL_INGL_CURR as COMMITTED_VALUE_INGL_CURR,
                    SAQRIT.ESTVAL_INGL_CURR as ESTVAL_INGL_CURR,
                    SAQRIT.QUOTE_RECORD_ID,
                    SAQRIT.GLOBAL_CURRENCY,
                    SAQRIT.GLOBAL_CURRENCY_RECORD_ID,
                    SAQRIT.QTEREV_ID,
                    SAQRIT.QTEREV_RECORD_ID,
                    {BillingDate} as BILLING_DATE,
                    '{amount_column_split}' as BILLING_YEAR,
                    '{billing_day}' as BILLING_DAY,
                    '' as EQUIPMENT_DESCRIPTION,
                    SAQRIT.OBJECT_ID as EQUIPMENT_ID,
                    '' as EQUIPMENT_RECORD_ID,
                    '' as QTEITMCOB_RECORD_ID,
                    SAQRIT.SERVICE_DESCRIPTION,
                    SAQRIT.SERVICE_ID,
                    SAQRIT.SERVICE_RECORD_ID,
                    SAQRIT.GREENBOOK,
                    SAQRIT.GREENBOOK_RECORD_ID,
                    '' AS SERIAL_NUMBER,
                    '' as WARRANTY_START_DATE,
                    '' as WARRANTY_END_DATE,
                    SAQRIT.CONTRACT_VALID_FROM AS CONTRACT_START_DATE,
                    SAQRIT.CONTRACT_VALID_TO AS CONTRACT_END_DATE,
                    SAQRIT.UOM,
                    SAQRIT.STATUS,
                    SAQRIT.SAP_PART_NUMBER,
                    SAQRIT.OBJECT_TYPE,
                    SAQRIT.OBJECT_ID,
                    SAQRIT.LINE_TYPE,
                    SAQRIT.KIT_NUMBER,
                    SAQRIT.KIT_NAME,
                    SAQRIT.FABLOCATION_ID,
                    SAQRIT.COUNT_OF_ASSEMBLIES AS COUNT_OF_ASSEMBLY,
                    SAQRIT.AGS_POSS_ID,
                    SAQRIT.UPDATED_CRM,
                    SAQRIT.TEMP_TOOL,
                    SAQRIT.PM_ID,
                    SAQRIT.MNTEVT_LEVEL,
                    SAQRIT.GOT_CODE,
                    SAQRIT.CUSTOMER_TOOL_ID,
                    SAQRIT.ASSEMBLY_ID,        
                    {UserId} as CPQTABLEENTRYADDEDBY,
                    GETDATE() as CPQTABLEENTRYDATEADDED
                    FROM SAQRIT (NOLOCK)  LEFT JOIN SAQIBP (NOLOCK) on SAQRIT.QUOTE_RECORD_ID = SAQIBP.QUOTE_RECORD_ID and SAQRIT.QTEREV_RECORD_ID=SAQIBP.QTEREV_RECORD_ID  and SAQRIT.SERVICE_ID = SAQIBP.SERVICE_ID AND
                    EXISTS (SELECT * FROM  SAQIBP (NOLOCK) WHERE SAQIBP.ANNUAL_BILLING_AMOUNT <> SAQRIT.NET_PRICE AND SAQRIT.QUOTE_RECORD_ID = SAQIBP.QUOTE_RECORD_ID and SAQRIT.QTEREV_RECORD_ID=SAQIBP.QTEREV_RECORD_ID  and SAQRIT.SERVICE_ID = SAQIBP.SERVICE_ID)
                    WHERE SAQRIT.QUOTE_RECORD_ID='{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQRIT.SERVICE_ID ='{service_id}'  and SAQRIT.NET_VALUE IS NOT NULL  and SAQRIT.OBJECT_ID IS NULL )A """.format(
                    UserId=user_id, QuoteRecordId=contract_quote_rec_id,
                    RevisionRecordId=quote_revision_rec_id,billing_day=billing_day,billing_end_date=billing_end_date,
                    BillingDate=billing_date,get_dc_cur_val=get_dc_cur_val,
                    get_val=get_val,year_amount_column_gl_curr=year_amount_column_gl_curr,
                    service_id = service_id,billing_type =get_billing_type,amount_column=amount_column,amount_column_split=amount_column_split,get_round_val=get_round_val))
        #A055S000P01-20779 End - M
    elif service_id in  ("Z0009","Z0100","Z0123"):
        if str(get_billing_type).upper() in ("FIXED","MILESTONE"):
            #A055S000P01-20779 Start - M
            Sql.RunQuery("""INSERT SAQIBP (
                        
                        QUOTE_ITEM_BILLING_PLAN_RECORD_ID, BILLING_END_DATE, BILLING_START_DATE,ANNUAL_BILLING_AMOUNT,ANNBILAMT_INGL_CURR,BILADJAMT_INGL_CURR,BILADJ_DTYFLG,TTLMRG_INGL_CURR,BILLING_VALUE, BILLING_VALUE_INGL_CURR,BILLING_TYPE,LINE, QUOTE_ID,DOC_CURRENCY, QTEITM_RECORD_ID,COMMITTED_VALUE_INGL_CURR,ESTVAL_INGL_CURR,
                        QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,GLOBAL_CURRENCY,GLOBALCURRENCY_RECORD_ID,
                        BILLING_DATE, BILLING_YEAR,BILLING_DAY,
                        EQUIPMENT_DESCRIPTION, EQUIPMENT_ID, EQUIPMENT_RECORD_ID, QTEITMCOB_RECORD_ID, 
                        SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID, SERIAL_NUMBER, WARRANTY_START_DATE, WARRANTY_END_DATE,CONTRACT_START_DATE,CONTRACT_END_DATE,UOM,STATUS,SAP_PART_NUMBER,OBJECT_TYPE,OBJECT_ID,LINE_TYPE,KIT_NUMBER,KIT_NAME,FABLOCATION_ID,COUNT_OF_ASSEMBLY,AGS_POSS_ID,UPDATED_CRM,TEMP_TOOL,PM_ID,MNTEVT_LEVEL,GOT_CODE,CUSTOMER_TOOL_ID,ASSEMBLY_ID,CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED
                    )SELECT 
                        CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_BILLING_PLAN_RECORD_ID,A.* from (SELECT DISTINCT  
                        {billing_end_date} as BILLING_END_DATE,
                        {BillingDate} as BILLING_START_DATE,
                        {amount_column} AS ANNUAL_BILLING_AMOUNT,
                        {year_amount_column_gl_curr} AS ANNBILAMT_INGL_CURR,
                        {year_amount_column_gl_curr} AS BILADJAMT_INGL_CURR,
                        0 as BILADJ_DTYFLG,
                        SAQRIT.TOTAL_MARGIN AS TTLMRG_INGL_CURR,
                        CAST(ROUND(ISNULL({amount_column},0),{get_dc_cur_val})/ {get_val} AS DECIMAL(20,{get_dc_cur_val}))  as BILLING_VALUE,
                        CAST(ROUND(ISNULL({year_amount_column_gl_curr},0),{get_round_val})/ {get_val} AS DECIMAL(20,{get_round_val}))   as  BILLING_VALUE_INGL_CURR,
                        '{billing_type}' as BILLING_TYPE,
                        SAQRIT.LINE AS LINE,
                        SAQRIT.QUOTE_ID,
                        SAQRIT.DOC_CURRENCY AS DOC_CURRENCY,
                        SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID,	
                        SAQRIT.COMVAL_INGL_CURR	 as COMMITTED_VALUE_INGL_CURR,
                        SAQRIT.ESTVAL_INGL_CURR	as 	ESTVAL_INGL_CURR,	
                        SAQRIT.QUOTE_RECORD_ID,
                        SAQRIT.QTEREV_ID,
                        SAQRIT.QTEREV_RECORD_ID,
                        SAQRIT.GLOBAL_CURRENCY,
                        SAQRIT.GLOBAL_CURRENCY_RECORD_ID,
                        {BillingDate} as BILLING_DATE,						
                        '{amount_column_split}' as BILLING_YEAR,
                        '{billing_day}' as BILLING_DAY,
                        '' as EQUIPMENT_DESCRIPTION,
                        SAQRIT.OBJECT_ID as EQUIPMENT_ID,									
                        '' as EQUIPMENT_RECORD_ID,						
                        '' as QTEITMCOB_RECORD_ID,
                        SAQRIT.SERVICE_DESCRIPTION,
                        SAQRIT.SERVICE_ID,
                        SAQRIT.SERVICE_RECORD_ID, 
                        SAQRIT.GREENBOOK,
                        SAQRIT.GREENBOOK_RECORD_ID,
                        '' AS SERIAL_NUMBER,
                        ''  as WARRANTY_START_DATE,
                        ''  as WARRANTY_END_DATE,
                        SAQRIT.CONTRACT_VALID_FROM AS CONTRACT_START_DATE,
                        SAQRIT.CONTRACT_VALID_TO AS CONTRACT_END_DATE,
                        SAQRIT.UOM,
                        SAQRIT.STATUS,
                        SAQRIT.SAP_PART_NUMBER,
                        SAQRIT.OBJECT_TYPE,
                        SAQRIT.OBJECT_ID,
                        SAQRIT.LINE_TYPE,
                        SAQRIT.KIT_NUMBER,
                        SAQRIT.KIT_NAME,
                        SAQRIT.FABLOCATION_ID,
                        SAQRIT.COUNT_OF_ASSEMBLIES AS COUNT_OF_ASSEMBLY,
                        SAQRIT.AGS_POSS_ID,
                        SAQRIT.UPDATED_CRM,
                        SAQRIT.TEMP_TOOL,
                        SAQRIT.PM_ID,
                        SAQRIT.MNTEVT_LEVEL,
                        SAQRIT.GOT_CODE,
                        SAQRIT.CUSTOMER_TOOL_ID,
                        SAQRIT.ASSEMBLY_ID,        
                        {UserId} as CPQTABLEENTRYADDEDBY, 
                        GETDATE() as CPQTABLEENTRYDATEADDED
                        FROM  SAQRIT (NOLOCK)  LEFT JOIN SAQIBP (NOLOCK) on SAQRIT.QUOTE_RECORD_ID = SAQIBP.QUOTE_RECORD_ID and SAQRIT.QTEREV_RECORD_ID=SAQIBP.QTEREV_RECORD_ID  and SAQRIT.SERVICE_ID = SAQIBP.SERVICE_ID AND
                        EXISTS (SELECT * FROM  SAQIBP (NOLOCK) WHERE SAQIBP.ANNUAL_BILLING_AMOUNT <> SAQRIT.NET_VALUE AND SAQRIT.QUOTE_RECORD_ID = SAQIBP.QUOTE_RECORD_ID and SAQRIT.QTEREV_RECORD_ID=SAQIBP.QTEREV_RECORD_ID  and SAQRIT.SERVICE_ID = SAQIBP.SERVICE_ID)
                        WHERE SAQRIT.QUOTE_RECORD_ID='{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQRIT.SERVICE_ID ='{service_id}'   and SAQRIT.NET_VALUE  IS NOT NULL  AND SAQRIT.OBJECT_ID IS NOT NULL AND  SAQRIT.OBJECT_ID <> '')A """.format(
                        UserId=user_id, QuoteRecordId=contract_quote_rec_id,
                        RevisionRecordId=quote_revision_rec_id,billing_end_date=billing_end_date,
                        BillingDate=billing_date,billing_day=billing_day,get_dc_cur_val=get_dc_cur_val,
                        get_val=get_val,year_amount_column_gl_curr=year_amount_column_gl_curr,
                        service_id = service_id,billing_type =get_billing_type,amount_column=amount_column,amount_column_split=amount_column_split,get_round_val=get_round_val))
            Sql.RunQuery("""INSERT SAQIBP (					
                        QUOTE_ITEM_BILLING_PLAN_RECORD_ID, BILLING_END_DATE, BILLING_START_DATE,ANNUAL_BILLING_AMOUNT,ANNBILAMT_INGL_CURR,BILADJAMT_INGL_CURR,BILADJ_DTYFLG,TTLMRG_INGL_CURR,BILLING_VALUE, BILLING_VALUE_INGL_CURR,BILLING_TYPE,LINE, QUOTE_ID, QTEITM_RECORD_ID, COMMITTED_VALUE_INGL_CURR,ESTVAL_INGL_CURR,DOC_CURRENCY,ESTVAL_INDT_CURR,
                        QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,
                        BILLING_DATE, BILLING_YEAR,BILLING_DAY,
                        EQUIPMENT_DESCRIPTION, EQUIPMENT_ID, EQUIPMENT_RECORD_ID, QTEITMCOB_RECORD_ID, 
                        SERVICE_DESCRIPTION, SERVICE_ID,GLOBAL_CURRENCY,GLOBALCURRENCY_RECORD_ID, SERVICE_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID, SERIAL_NUMBER, WARRANTY_START_DATE, WARRANTY_END_DATE,CONTRACT_START_DATE,CONTRACT_END_DATE,UOM,STATUS,SAP_PART_NUMBER,OBJECT_TYPE,OBJECT_ID,LINE_TYPE,KIT_NUMBER,KIT_NAME,FABLOCATION_ID,COUNT_OF_ASSEMBLY,AGS_POSS_ID,UPDATED_CRM,TEMP_TOOL,PM_ID,MNTEVT_LEVEL,GOT_CODE,CUSTOMER_TOOL_ID,ASSEMBLY_ID,CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED
                    ) 
                    SELECT 
                        CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_BILLING_PLAN_RECORD_ID,  
                        {billing_end_date} as BILLING_END_DATE,
                        {BillingDate} as BILLING_START_DATE,
                        {amount_column} AS ANNUAL_BILLING_AMOUNT,
                        {year_amount_column_gl_curr} AS ANNBILAMT_INGL_CURR,
                        {year_amount_column_gl_curr} AS BILADJAMT_INGL_CURR,
                        0 as BILADJ_DTYFLG,
                        SAQRIT.TOTAL_MARGIN AS TTLMRG_INGL_CURR,
                        CAST(ROUND(ISNULL({amount_column},0),{get_dc_cur_val})/ {get_val} AS DECIMAL(20,{get_dc_cur_val}))  as BILLING_VALUE,
                        CAST(ROUND(ISNULL({year_amount_column_gl_curr},0),{get_round_val})/ {get_val} AS DECIMAL(20,{get_round_val}))   as  BILLING_VALUE_INGL_CURR,
                        '{billing_type}' as BILLING_TYPE,
                        LINE,
                        QUOTE_ID,
                        QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID,
                        
                        COMVAL_INGL_CURR as COMMITTED_VALUE_INGL_CURR,
                        SAQRIT.ESTVAL_INGL_CURR	as 	ESTVAL_INGL_CURR,
                        SAQRIT.DOC_CURRENCY AS DOC_CURRENCY,
                        0 as ESTVAL_INDT_CURR,	
                        QUOTE_RECORD_ID,
                        QTEREV_ID,
                        QTEREV_RECORD_ID,
                        {BillingDate} as BILLING_DATE,						
                        '{amount_column_split}' as BILLING_YEAR,
                        '{billing_day}' as BILLING_DAY,
                        '' as EQUIPMENT_DESCRIPTION,
                        '' as EQUIPMENT_ID,									
                        '' as EQUIPMENT_RECORD_ID,						
                        '' as QTEITMCOB_RECORD_ID,
                        SERVICE_DESCRIPTION,
                        SERVICE_ID,
                        GLOBAL_CURRENCY,
                        GLOBAL_CURRENCY_RECORD_ID,
                        SERVICE_RECORD_ID, 
                        GREENBOOK,
                        GREENBOOK_RECORD_ID,
                        '' AS SERIAL_NUMBER,
                        '' as WARRANTY_START_DATE,
                        '' as WARRANTY_END_DATE,
                        CONTRACT_VALID_FROM AS CONTRACT_START_DATE,
                        CONTRACT_VALID_TO AS CONTRACT_END_DATE,
                        UOM,
                        STATUS,
                        SAP_PART_NUMBER,
                        OBJECT_TYPE,
                        OBJECT_ID,
                        LINE_TYPE,
                        KIT_NUMBER,
                        KIT_NAME,
                        FABLOCATION_ID,
                        COUNT_OF_ASSEMBLIES AS COUNT_OF_ASSEMBLY,
                        AGS_POSS_ID,
                        UPDATED_CRM,
                        TEMP_TOOL,
                        PM_ID,
                        MNTEVT_LEVEL,
                        GOT_CODE,
                        CUSTOMER_TOOL_ID,
                        ASSEMBLY_ID,        
                        {UserId} as CPQTABLEENTRYADDEDBY, 
                        GETDATE() as CPQTABLEENTRYDATEADDED
                    FROM  SAQRIT (NOLOCK) 
                    WHERE QUOTE_RECORD_ID='{QuoteRecordId}' AND  NET_VALUE IS NOT NULL AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID ='{service_id}' AND (OBJECT_ID  IS NULL OR OBJECT_ID = '')""".format(
                        UserId=user_id, QuoteRecordId=contract_quote_rec_id,
                        RevisionRecordId=quote_revision_rec_id,get_dc_cur_val=get_dc_cur_val,
                        BillingDate=billing_date,billing_end_date=billing_end_date,
                        get_val=get_val,billing_day=billing_day,year_amount_column_gl_curr=year_amount_column_gl_curr,
                        service_id = service_id,billing_type =get_billing_type,amount_column=amount_column,amount_column_split=amount_column_split,get_round_val=get_round_val))
            #A055S000P01-20779 End - M
        else:
            #A055S000P01-20779 Start - M
            Sql.RunQuery("""INSERT SAQIBP (					
                        QUOTE_ITEM_BILLING_PLAN_RECORD_ID, BILLING_END_DATE, BILLING_START_DATE,ANNUAL_BILLING_AMOUNT,ANNBILAMT_INGL_CURR,BILADJAMT_INGL_CURR,BILADJ_DTYFLG,TTLMRG_INGL_CURR,BILLING_VALUE, BILLING_VALUE_INGL_CURR,BILLING_TYPE,LINE, QUOTE_ID, QTEITM_RECORD_ID, COMMITTED_VALUE_INGL_CURR,ESTVAL_INGL_CURR,DOC_CURRENCY,ESTVAL_INDT_CURR,
                        QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,
                        BILLING_DATE, BILLING_YEAR,BILLING_DAY,
                        EQUIPMENT_DESCRIPTION, EQUIPMENT_ID, EQUIPMENT_RECORD_ID, QTEITMCOB_RECORD_ID, 
                        SERVICE_DESCRIPTION, SERVICE_ID, GLOBAL_CURRENCY,GLOBALCURRENCY_RECORD_ID, SERVICE_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID, SERIAL_NUMBER, WARRANTY_START_DATE, WARRANTY_END_DATE,CONTRACT_START_DATE,CONTRACT_END_DATE,UOM,STATUS,SAP_PART_NUMBER,OBJECT_TYPE,OBJECT_ID,LINE_TYPE,KIT_NUMBER,KIT_NAME,FABLOCATION_ID,COUNT_OF_ASSEMBLY,AGS_POSS_ID,UPDATED_CRM,TEMP_TOOL,PM_ID,MNTEVT_LEVEL,GOT_CODE,CUSTOMER_TOOL_ID,ASSEMBLY_ID,CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED
                    ) 
                    SELECT 
                        CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_BILLING_PLAN_RECORD_ID,  
                        {billing_end_date} as BILLING_END_DATE,
                        {BillingDate} as BILLING_START_DATE,
                        {amount_column} AS ANNUAL_BILLING_AMOUNT,
                        {year_amount_column_gl_curr} AS ANNBILAMT_INGL_CURR,
                        {year_amount_column_gl_curr} AS BILADJAMT_INGL_CURR,
                        0 as BILADJ_DTYFLG,
                        TOTAL_MARGIN AS TTLMRG_INGL_CURR,
                        0  as BILLING_VALUE,
                        0  as  BILLING_VALUE_INGL_CURR,
                        '{billing_type}' as BILLING_TYPE,
                        LINE,
                        QUOTE_ID,
                        QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID,
                        
                        COMVAL_INGL_CURR as COMMITTED_VALUE_INGL_CURR,
                        CAST(ROUND(ISNULL({year_amount_column_gl_curr},0),{get_round_val})/ {get_val} AS DECIMAL(20,{get_round_val}))	as 	ESTVAL_INGL_CURR,
                        DOC_CURRENCY AS DOC_CURRENCY,
                        CAST(ROUND(ISNULL({amount_column},0),{get_dc_cur_val})/ {get_val} AS DECIMAL(20,{get_dc_cur_val})) as ESTVAL_INDT_CURR,	
                        QUOTE_RECORD_ID,
                        QTEREV_ID,
                        QTEREV_RECORD_ID,
                        {BillingDate} as BILLING_DATE,						
                        '{amount_column_split}' as BILLING_YEAR,
                        '{billing_day}' as BILLING_DAY,
                        '' as EQUIPMENT_DESCRIPTION,
                        '' as EQUIPMENT_ID,									
                        '' as EQUIPMENT_RECORD_ID,						
                        '' as QTEITMCOB_RECORD_ID,
                        SERVICE_DESCRIPTION,
                        SERVICE_ID,
                        GLOBAL_CURRENCY,
                        GLOBAL_CURRENCY_RECORD_ID,
                        SERVICE_RECORD_ID, 
                        GREENBOOK,
                        GREENBOOK_RECORD_ID,
                        '' AS SERIAL_NUMBER,
                        '' as WARRANTY_START_DATE,
                        '' as WARRANTY_END_DATE, 
                        CONTRACT_VALID_FROM AS CONTRACT_START_DATE,
                        CONTRACT_VALID_TO AS CONTRACT_END_DATE,
                        UOM,
                        STATUS,
                        SAP_PART_NUMBER,
                        OBJECT_TYPE,
                        OBJECT_ID,
                        LINE_TYPE,
                        KIT_NUMBER,
                        KIT_NAME,
                        FABLOCATION_ID,
                        COUNT_OF_ASSEMBLIES AS COUNT_OF_ASSEMBLY,
                        AGS_POSS_ID,
                        UPDATED_CRM,
                        TEMP_TOOL,
                        PM_ID,
                        MNTEVT_LEVEL,
                        GOT_CODE,
                        CUSTOMER_TOOL_ID,
                        ASSEMBLY_ID,       
                        {UserId} as CPQTABLEENTRYADDEDBY, 
                        GETDATE() as CPQTABLEENTRYDATEADDED
                    FROM  SAQRIT (NOLOCK) 
                    WHERE QUOTE_RECORD_ID='{QuoteRecordId}' AND  ESTIMATED_VALUE IS NOT NULL AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID ='{service_id}' AND OBJECT_ID  IS NOT  NULL""".format(
                        UserId=user_id, QuoteRecordId=contract_quote_rec_id,billing_day=billing_day,
                        RevisionRecordId=quote_revision_rec_id,get_dc_cur_val=get_dc_cur_val,
                        BillingDate=billing_date,billing_end_date=billing_end_date,
                        get_val=get_val,year_amount_column_gl_curr=year_amount_column_gl_curr,
                        service_id = service_id,billing_type =get_billing_type,amount_column=amount_column,amount_column_split=amount_column_split,get_round_val=get_round_val))
            Sql.RunQuery("""INSERT SAQIBP (					
                        QUOTE_ITEM_BILLING_PLAN_RECORD_ID, BILLING_END_DATE, BILLING_START_DATE,ANNUAL_BILLING_AMOUNT,ANNBILAMT_INGL_CURR,BILADJAMT_INGL_CURR,BILADJ_DTYFLG,TTLMRG_INGL_CURR,BILLING_VALUE, BILLING_VALUE_INGL_CURR,BILLING_TYPE,LINE, QUOTE_ID, QTEITM_RECORD_ID, COMMITTED_VALUE_INGL_CURR,ESTVAL_INGL_CURR,DOC_CURRENCY,ESTVAL_INDT_CURR,
                        QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,
                        BILLING_DATE, BILLING_YEAR,BILLING_DAY,
                        EQUIPMENT_DESCRIPTION, EQUIPMENT_ID, EQUIPMENT_RECORD_ID, QTEITMCOB_RECORD_ID, 
                        SERVICE_DESCRIPTION, SERVICE_ID, GLOBAL_CURRENCY,GLOBALCURRENCY_RECORD_ID, SERVICE_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID, SERIAL_NUMBER, WARRANTY_START_DATE, WARRANTY_END_DATE,CONTRACT_START_DATE,CONTRACT_END_DATE,UOM,STATUS,SAP_PART_NUMBER,OBJECT_TYPE,OBJECT_ID,LINE_TYPE,KIT_NUMBER,KIT_NAME,FABLOCATION_ID,COUNT_OF_ASSEMBLY,AGS_POSS_ID,UPDATED_CRM,TEMP_TOOL,PM_ID,MNTEVT_LEVEL,GOT_CODE,CUSTOMER_TOOL_ID,ASSEMBLY_ID,CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED
                    ) 
                    SELECT 
                        CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_BILLING_PLAN_RECORD_ID,  
                        {billing_end_date} as BILLING_END_DATE,
                        {BillingDate} as BILLING_START_DATE,
                        {amount_column} AS ANNUAL_BILLING_AMOUNT,
                        {year_amount_column_gl_curr} AS ANNBILAMT_INGL_CURR,
                        {year_amount_column_gl_curr} AS BILADJAMT_INGL_CURR,
                        0 as BILADJ_DTYFLG,
                        TOTAL_MARGIN AS TTLMRG_INGL_CURR,
                        0  as BILLING_VALUE,
                        0  as  BILLING_VALUE_INGL_CURR,
                        '{billing_type}' as BILLING_TYPE,
                        LINE,
                        QUOTE_ID,
                        QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID,
                        
                        COMVAL_INGL_CURR as COMMITTED_VALUE_INGL_CURR,
                        CAST(ROUND(ISNULL({year_amount_column_gl_curr},0),{get_round_val})/ {get_val} AS DECIMAL(20,{get_round_val}))	as 	ESTVAL_INGL_CURR,
                        DOC_CURRENCY AS DOC_CURRENCY,
                        CAST(ROUND(ISNULL({amount_column},0),{get_dc_cur_val})/ {get_val} AS DECIMAL(20,{get_dc_cur_val})) as ESTVAL_INDT_CURR,	
                        QUOTE_RECORD_ID,
                        QTEREV_ID,
                        QTEREV_RECORD_ID,
                        {BillingDate} as BILLING_DATE,						
                        '{amount_column_split}' as BILLING_YEAR,
                        '{billing_day}' as BILLING_DAY,
                        '' as EQUIPMENT_DESCRIPTION,
                        '' as EQUIPMENT_ID,									
                        '' as EQUIPMENT_RECORD_ID,						
                        '' as QTEITMCOB_RECORD_ID,
                        SERVICE_DESCRIPTION,
                        SERVICE_ID,
                        GLOBAL_CURRENCY,
                        GLOBAL_CURRENCY_RECORD_ID,
                        SERVICE_RECORD_ID, 
                        GREENBOOK,
                        GREENBOOK_RECORD_ID,
                        '' AS SERIAL_NUMBER,
                        '' as WARRANTY_START_DATE,
                        '' as WARRANTY_END_DATE,    
                        CONTRACT_VALID_FROM AS CONTRACT_START_DATE,
                        CONTRACT_VALID_TO AS CONTRACT_END_DATE,
                        UOM,
                        STATUS,
                        SAP_PART_NUMBER,
                        OBJECT_TYPE,
                        OBJECT_ID,
                        LINE_TYPE,
                        KIT_NUMBER,
                        KIT_NAME,
                        FABLOCATION_ID,
                        COUNT_OF_ASSEMBLIES AS COUNT_OF_ASSEMBLY,
                        AGS_POSS_ID,
                        UPDATED_CRM,
                        TEMP_TOOL,
                        PM_ID,
                        MNTEVT_LEVEL,
                        GOT_CODE,
                        CUSTOMER_TOOL_ID,
                        ASSEMBLY_ID,    
                        {UserId} as CPQTABLEENTRYADDEDBY, 
                        GETDATE() as CPQTABLEENTRYDATEADDED
                    FROM  SAQRIT (NOLOCK) 
                    WHERE QUOTE_RECORD_ID='{QuoteRecordId}' AND  ESTIMATED_VALUE IS NOT NULL AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID ='{service_id}' AND (OBJECT_ID  IS NULL OR OBJECT_ID = '')""".format(
                        UserId=user_id, QuoteRecordId=contract_quote_rec_id,
                        RevisionRecordId=quote_revision_rec_id,billing_day=billing_day,
                        BillingDate=billing_date,billing_end_date=billing_end_date,get_dc_cur_val=get_dc_cur_val,
                        get_val=get_val,year_amount_column_gl_curr=year_amount_column_gl_curr,
                        service_id = service_id,billing_type =get_billing_type,amount_column=amount_column,amount_column_split=amount_column_split,get_round_val=get_round_val))
        #A055S000P01-20779 End - M
    else:				
        if str(get_billing_type).upper() == "VARIABLE":
             #A055S000P01-20779 Start - M
            Sql.RunQuery("""INSERT SAQIBP (						
                        QUOTE_ITEM_BILLING_PLAN_RECORD_ID, BILLING_END_DATE, BILLING_START_DATE,ANNUAL_BILLING_AMOUNT,ANNBILAMT_INGL_CURR,BILADJAMT_INGL_CURR,BILADJ_DTYFLG,TTLMRG_INGL_CURR,BILLING_VALUE, BILLING_VALUE_INGL_CURR,BILLING_TYPE,LINE, QUOTE_ID,DOC_CURRENCY, QTEITM_RECORD_ID,COMMITTED_VALUE_INGL_CURR,ESTVAL_INGL_CURR,ESTVAL_INDT_CURR,
                        QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,GLOBAL_CURRENCY,GLOBALCURRENCY_RECORD_ID,
                        BILLING_DATE, BILLING_YEAR,BILLING_DAY,
                        EQUIPMENT_DESCRIPTION, EQUIPMENT_ID, EQUIPMENT_RECORD_ID, QTEITMCOB_RECORD_ID, 
                        SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID, SERIAL_NUMBER, WARRANTY_START_DATE, WARRANTY_END_DATE,CONTRACT_START_DATE,CONTRACT_END_DATE,UOM,STATUS,SAP_PART_NUMBER,OBJECT_TYPE,OBJECT_ID,LINE_TYPE,KIT_NUMBER,KIT_NAME,FABLOCATION_ID,COUNT_OF_ASSEMBLY,AGS_POSS_ID,UPDATED_CRM,TEMP_TOOL,PM_ID,MNTEVT_LEVEL,GOT_CODE,CUSTOMER_TOOL_ID,ASSEMBLY_ID,CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED
                    )SELECT 
                        CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_BILLING_PLAN_RECORD_ID,A.* from (SELECT DISTINCT  
                        {billing_end_date} as BILLING_END_DATE,
                        {BillingDate} as BILLING_START_DATE,
                        {amount_column} AS ANNUAL_BILLING_AMOUNT,
                        {year_amount_column_gl_curr} AS ANNBILAMT_INGL_CURR,
                        {year_amount_column_gl_curr} AS BILADJAMT_INGL_CURR,
                        0 as BILADJ_DTYFLG,
                        SAQRIT.TOTAL_MARGIN AS TTLMRG_INGL_CURR,
                        0  as BILLING_VALUE,
                        0  as  BILLING_VALUE_INGL_CURR,
                        '{billing_type}' as BILLING_TYPE,
                        SAQRIT.LINE AS LINE,
                        SAQRIT.QUOTE_ID,
                        SAQRIT.DOC_CURRENCY AS DOC_CURRENCY,
                        SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID,	
                        SAQRIT.COMVAL_INGL_CURR	 as COMMITTED_VALUE_INGL_CURR,
                        CAST(ROUND(ISNULL({year_amount_column_gl_curr},0),{get_round_val})/ {get_val} AS DECIMAL(20,{get_round_val})) as ESTVAL_INGL_CURR,
                        
                        CAST(ROUND(ISNULL({amount_column},0),{get_dc_cur_val})/ {get_val} AS DECIMAL(20,{get_dc_cur_val})) as ESTVAL_INDT_CURR,		
                        SAQRIT.QUOTE_RECORD_ID,
                        SAQRIT.QTEREV_ID,
                        SAQRIT.QTEREV_RECORD_ID,
                        SAQRIT.GLOBAL_CURRENCY,
                        SAQRIT.GLOBAL_CURRENCY_RECORD_ID,
                        {BillingDate} as BILLING_DATE,						
                        '{amount_column_split}' as BILLING_YEAR,
                        '{billing_day}' as BILLING_DAY,
                        '' as EQUIPMENT_DESCRIPTION,
                        SAQRIT.OBJECT_ID as EQUIPMENT_ID,									
                        '' as EQUIPMENT_RECORD_ID,						
                        '' as QTEITMCOB_RECORD_ID,
                        SAQRIT.SERVICE_DESCRIPTION,
                        SAQRIT.SERVICE_ID,
                        SAQRIT.SERVICE_RECORD_ID, 
                        SAQRIT.GREENBOOK,
                        SAQRIT.GREENBOOK_RECORD_ID,
                        '' AS SERIAL_NUMBER,
                        ''  as WARRANTY_START_DATE,
                        ''  as WARRANTY_END_DATE,    
                        SAQRIT.CONTRACT_VALID_FROM AS CONTRACT_START_DATE,
                        SAQRIT.CONTRACT_VALID_TO AS CONTRACT_END_DATE,
                        SAQRIT.UOM,
                        SAQRIT.STATUS,
                        SAQRIT.SAP_PART_NUMBER,
                        SAQRIT.OBJECT_TYPE,
                        SAQRIT.OBJECT_ID,
                        SAQRIT.LINE_TYPE,
                        SAQRIT.KIT_NUMBER,
                        SAQRIT.KIT_NAME,
                        SAQRIT.FABLOCATION_ID,
                        SAQRIT.COUNT_OF_ASSEMBLIES AS COUNT_OF_ASSEMBLY,
                        SAQRIT.AGS_POSS_ID,
                        SAQRIT.UPDATED_CRM,
                        SAQRIT.TEMP_TOOL,
                        SAQRIT.PM_ID,
                        SAQRIT.MNTEVT_LEVEL,
                        SAQRIT.GOT_CODE,
                        SAQRIT.CUSTOMER_TOOL_ID,
                        SAQRIT.ASSEMBLY_ID,    
                        {UserId} as CPQTABLEENTRYADDEDBY, 
                        GETDATE() as CPQTABLEENTRYDATEADDED
                        FROM  SAQRIT (NOLOCK)  LEFT JOIN SAQIBP (NOLOCK) on SAQRIT.QUOTE_RECORD_ID = SAQIBP.QUOTE_RECORD_ID and SAQRIT.QTEREV_RECORD_ID=SAQIBP.QTEREV_RECORD_ID  and SAQRIT.SERVICE_ID = SAQIBP.SERVICE_ID AND
                        EXISTS (SELECT * FROM  SAQIBP (NOLOCK) WHERE SAQIBP.ANNUAL_BILLING_AMOUNT <> SAQRIT.NET_VALUE AND SAQRIT.QUOTE_RECORD_ID = SAQIBP.QUOTE_RECORD_ID and SAQRIT.QTEREV_RECORD_ID=SAQIBP.QTEREV_RECORD_ID  and SAQRIT.SERVICE_ID = SAQIBP.SERVICE_ID)
                        WHERE SAQRIT.QUOTE_RECORD_ID='{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQRIT.SERVICE_ID ='{service_id}'   and SAQRIT.ESTIMATED_VALUE  IS NOT NULL  AND SAQRIT.OBJECT_ID IS NOT NULL )A """.format(
                        UserId=user_id, QuoteRecordId=contract_quote_rec_id,
                        RevisionRecordId=quote_revision_rec_id,billing_day=billing_day,billing_end_date=billing_end_date,
                        BillingDate=billing_date,year_amount_column_gl_curr=year_amount_column_gl_curr,
                        get_val=get_val,
                        service_id = service_id,billing_type =get_billing_type,amount_column=amount_column,amount_column_split=amount_column_split,get_round_val=get_round_val,get_dc_cur_val=get_dc_cur_val))
            Sql.RunQuery("""INSERT SAQIBP (					
                        QUOTE_ITEM_BILLING_PLAN_RECORD_ID, BILLING_END_DATE, BILLING_START_DATE,ANNUAL_BILLING_AMOUNT,ANNBILAMT_INGL_CURR,BILADJAMT_INGL_CURR,BILADJ_DTYFLG,TTLMRG_INGL_CURR,BILLING_VALUE, BILLING_VALUE_INGL_CURR,BILLING_TYPE,LINE, QUOTE_ID, QTEITM_RECORD_ID, COMMITTED_VALUE_INGL_CURR,ESTVAL_INGL_CURR,DOC_CURRENCY,ESTVAL_INDT_CURR,
                        QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,
                        BILLING_DATE, BILLING_YEAR,BILLING_DAY,
                        EQUIPMENT_DESCRIPTION, EQUIPMENT_ID, EQUIPMENT_RECORD_ID, QTEITMCOB_RECORD_ID, 
                        SERVICE_DESCRIPTION, SERVICE_ID,GLOBAL_CURRENCY,GLOBALCURRENCY_RECORD_ID, SERVICE_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID, SERIAL_NUMBER, WARRANTY_START_DATE, WARRANTY_END_DATE,CONTRACT_START_DATE,CONTRACT_END_DATE,UOM,STATUS,SAP_PART_NUMBER,OBJECT_TYPE,OBJECT_ID,LINE_TYPE,KIT_NUMBER,KIT_NAME,FABLOCATION_ID,COUNT_OF_ASSEMBLY,AGS_POSS_ID,UPDATED_CRM,TEMP_TOOL,PM_ID,MNTEVT_LEVEL,GOT_CODE,CUSTOMER_TOOL_ID,ASSEMBLY_ID,CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED,PAR_SERVICE_ID,PAR_SERVICE_RECORD_ID
                    ) 
                    SELECT 
                        CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_BILLING_PLAN_RECORD_ID,  
                        {billing_end_date} as BILLING_END_DATE,
                        {BillingDate} as BILLING_START_DATE,
                        {amount_column} AS ANNUAL_BILLING_AMOUNT,
                        {year_amount_column_gl_curr} AS ANNBILAMT_INGL_CURR,
                        {year_amount_column_gl_curr} AS BILADJAMT_INGL_CURR,
                        0 as BILADJ_DTYFLG,
                        TOTAL_MARGIN AS TTLMRG_INGL_CURR,
                        0  as BILLING_VALUE,
                        0  as  BILLING_VALUE_INGL_CURR,
                        '{billing_type}' as BILLING_TYPE,
                        LINE,
                        QUOTE_ID,
                        QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID,
                        
                        COMVAL_INGL_CURR as COMMITTED_VALUE_INGL_CURR,
                        CAST(ROUND(ISNULL({year_amount_column_gl_curr},0),{get_round_val})/ {get_val} AS DECIMAL(20,{get_round_val})) as 	ESTVAL_INGL_CURR,
                        DOC_CURRENCY AS DOC_CURRENCY,
                        CAST(ROUND(ISNULL({amount_column},0),{get_dc_cur_val})/ {get_val} AS DECIMAL(20,{get_dc_cur_val})) as ESTVAL_INDT_CURR,	
                        QUOTE_RECORD_ID,
                        QTEREV_ID,
                        QTEREV_RECORD_ID,
                        {BillingDate} as BILLING_DATE,						
                        '{amount_column_split}' as BILLING_YEAR,
                        '{billing_day}' as BILLING_DAY,
                        '' as EQUIPMENT_DESCRIPTION,
                        '' as EQUIPMENT_ID,									
                        '' as EQUIPMENT_RECORD_ID,						
                        '' as QTEITMCOB_RECORD_ID,
                        SERVICE_DESCRIPTION,
                        SERVICE_ID,
                        GLOBAL_CURRENCY,
                        GLOBAL_CURRENCY_RECORD_ID,
                        SERVICE_RECORD_ID, 
                        GREENBOOK,
                        GREENBOOK_RECORD_ID,
                        '' AS SERIAL_NUMBER,
                        '' as WARRANTY_START_DATE,
                        '' as WARRANTY_END_DATE,
                        CONTRACT_VALID_FROM AS CONTRACT_START_DATE,
                        CONTRACT_VALID_TO AS CONTRACT_END_DATE,
                        UOM,
                        STATUS,
                        SAP_PART_NUMBER,
                        OBJECT_TYPE,
                        OBJECT_ID,
                        LINE_TYPE,
                        KIT_NUMBER,
                        KIT_NAME,
                        FABLOCATION_ID,
                        COUNT_OF_ASSEMBLIES AS COUNT_OF_ASSEMBLY,
                        AGS_POSS_ID,
                        UPDATED_CRM,
                        TEMP_TOOL,
                        PM_ID,
                        MNTEVT_LEVEL,
                        GOT_CODE,
                        CUSTOMER_TOOL_ID,
                        ASSEMBLY_ID,        
                        {UserId} as CPQTABLEENTRYADDEDBY, 
                        GETDATE() as CPQTABLEENTRYDATEADDED,
                        PAR_PRDOFR_ID,	
                        PAR_PRDOFR_RECORD_ID
                    FROM  SAQRIT (NOLOCK) 
                    WHERE QUOTE_RECORD_ID='{QuoteRecordId}' AND  ESTIMATED_VALUE IS NOT NULL AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID ='{service_id}' AND (OBJECT_ID  IS NULL OR OBJECT_ID = '')""".format(
                        UserId=user_id, QuoteRecordId=contract_quote_rec_id,
                        RevisionRecordId=quote_revision_rec_id,billing_day=billing_day,
                        BillingDate=billing_date,billing_end_date=billing_end_date,get_dc_cur_val=get_dc_cur_val,
                        get_val=get_val,year_amount_column_gl_curr=year_amount_column_gl_curr,
                        service_id = service_id,billing_type =get_billing_type,amount_column=amount_column,amount_column_split=amount_column_split,get_round_val=get_round_val))
           #A055S000P01-20779 End - M
        else:
            #A055S000P01-20779 Start - M
            Sql.RunQuery("""INSERT SAQIBP (						
                        QUOTE_ITEM_BILLING_PLAN_RECORD_ID, BILLING_END_DATE, BILLING_START_DATE,ANNUAL_BILLING_AMOUNT,ANNBILAMT_INGL_CURR,BILADJAMT_INGL_CURR,BILADJ_DTYFLG,TTLMRG_INGL_CURR,BILLING_VALUE, BILLING_VALUE_INGL_CURR,BILLING_TYPE,LINE, QUOTE_ID,DOC_CURRENCY, QTEITM_RECORD_ID,COMMITTED_VALUE_INGL_CURR,ESTVAL_INGL_CURR,ESTVAL_INDT_CURR,
                        QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,
                        BILLING_DATE, BILLING_YEAR,BILLING_DAY,
                        EQUIPMENT_DESCRIPTION, EQUIPMENT_ID, EQUIPMENT_RECORD_ID, QTEITMCOB_RECORD_ID, 
                        SERVICE_DESCRIPTION, SERVICE_ID, GLOBAL_CURRENCY,GLOBALCURRENCY_RECORD_ID,SERVICE_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID, SERIAL_NUMBER, WARRANTY_START_DATE, WARRANTY_END_DATE,CONTRACT_START_DATE,CONTRACT_END_DATE,UOM,STATUS,SAP_PART_NUMBER,OBJECT_TYPE,OBJECT_ID,LINE_TYPE,KIT_NUMBER,KIT_NAME,FABLOCATION_ID,COUNT_OF_ASSEMBLY,AGS_POSS_ID,UPDATED_CRM,TEMP_TOOL,PM_ID,MNTEVT_LEVEL,GOT_CODE,CUSTOMER_TOOL_ID,ASSEMBLY_ID,CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED,PAR_SERVICE_ID,PAR_SERVICE_RECORD_ID
                    ) 
                    SELECT 
                        CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_BILLING_PLAN_RECORD_ID,A.* from (SELECT DISTINCT  
                        {billing_end_date} as BILLING_END_DATE,
                        {BillingDate} as BILLING_START_DATE,
                        {amount_column} AS ANNUAL_BILLING_AMOUNT,
                        {year_amount_column_gl_curr} AS ANNBILAMT_INGL_CURR,
                        {year_amount_column_gl_curr} AS BILADJAMT_INGL_CURR,
                        0 as BILADJ_DTYFLG,
                        SAQRIT.TOTAL_MARGIN AS TTLMRG_INGL_CURR,
                        0  as BILLING_VALUE,
                        0  as  BILLING_VALUE_INGL_CURR,
                        '{billing_type}' as BILLING_TYPE,
                        SAQRIT.LINE AS LINE,
                        SAQSCO.QUOTE_ID,
                        SAQRIT.DOC_CURRENCY AS DOC_CURRENCY,
                        SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID,	
                        SAQRIT.COMVAL_INGL_CURR	 as COMMITTED_VALUE_INGL_CURR,
                        CAST(ROUND(ISNULL({year_amount_column_gl_curr},0),{get_round_val})/ {get_val} AS DECIMAL(20,{get_round_val})) as ESTVAL_INGL_CURR,
                        CAST(ROUND(ISNULL({amount_column},0),{get_dc_cur_val})/ {get_val} AS DECIMAL(20,{get_dc_cur_val})) as ESTVAL_INDT_CURR,		
                        SAQSCO.QUOTE_RECORD_ID,
                        SAQSCO.QTEREV_ID,
                        SAQSCO.QTEREV_RECORD_ID,
                        {BillingDate} as BILLING_DATE,						
                        '{amount_column_split}' as BILLING_YEAR,
                        '{billing_day}' as BILLING_DAY,
                        SAQSCO.EQUIPMENT_DESCRIPTION,
                        SAQSCO.EQUIPMENT_ID,									
                        SAQSCO.EQUIPMENT_RECORD_ID,						
                        '' as QTEITMCOB_RECORD_ID,
                        SAQSCO.SERVICE_DESCRIPTION,
                        SAQSCO.SERVICE_ID,
                        SAQRIT.GLOBAL_CURRENCY,
                        SAQRIT.GLOBAL_CURRENCY_RECORD_ID,
                        SAQSCO.SERVICE_RECORD_ID, 
                        SAQSCO.GREENBOOK,
                        SAQSCO.GREENBOOK_RECORD_ID,
                        SAQSCO.SERIAL_NO AS SERIAL_NUMBER,
                        SAQSCO.WARRANTY_START_DATE,
                        SAQSCO.WARRANTY_END_DATE,
                        SAQRIT.CONTRACT_VALID_FROM AS CONTRACT_START_DATE,
                        SAQRIT.CONTRACT_VALID_TO AS CONTRACT_END_DATE,
                        SAQRIT.UOM,
                        SAQRIT.STATUS,
                        SAQRIT.SAP_PART_NUMBER,
                        SAQRIT.OBJECT_TYPE,
                        SAQRIT.OBJECT_ID,
                        SAQRIT.LINE_TYPE,
                        SAQRIT.KIT_NUMBER,
                        SAQRIT.KIT_NAME,
                        SAQRIT.FABLOCATION_ID,
                        SAQRIT.COUNT_OF_ASSEMBLIES AS COUNT_OF_ASSEMBLY,
                        SAQRIT.AGS_POSS_ID,
                        SAQRIT.UPDATED_CRM,
                        SAQRIT.TEMP_TOOL,
                        SAQRIT.PM_ID,
                        SAQRIT.MNTEVT_LEVEL,
                        SAQRIT.GOT_CODE,
                        SAQRIT.CUSTOMER_TOOL_ID,
                        SAQRIT.ASSEMBLY_ID,        
                        {UserId} as CPQTABLEENTRYADDEDBY, 
                        GETDATE() as CPQTABLEENTRYDATEADDED,
                        PAR_PRDOFR_ID,	
                        PAR_PRDOFR_RECORD_ID
                        FROM SAQSCO (NOLOCK) JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID and SAQRIT.QTEREV_RECORD_ID=SAQSCO.QTEREV_RECORD_ID  and SAQRIT.SERVICE_ID = SAQSCO.SERVICE_ID and SAQRIT.OBJECT_ID = SAQSCO.EQUIPMENT_ID and SAQSCO.GREENBOOK = SAQRIT.GREENBOOK LEFT JOIN SAQIBP (NOLOCK) on SAQRIT.QUOTE_RECORD_ID = SAQIBP.QUOTE_RECORD_ID and SAQRIT.QTEREV_RECORD_ID=SAQIBP.QTEREV_RECORD_ID  and SAQRIT.SERVICE_ID = SAQIBP.SERVICE_ID AND
                        EXISTS (SELECT * FROM  SAQIBP (NOLOCK) WHERE SAQIBP.ANNUAL_BILLING_AMOUNT <> SAQRIT.NET_PRICE AND SAQRIT.QUOTE_RECORD_ID = SAQIBP.QUOTE_RECORD_ID and SAQRIT.QTEREV_RECORD_ID=SAQIBP.QTEREV_RECORD_ID  and SAQRIT.SERVICE_ID = SAQIBP.SERVICE_ID)
                        WHERE SAQSCO.QUOTE_RECORD_ID='{QuoteRecordId}' AND SAQSCO.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQSCO.SERVICE_ID ='{service_id}'   and SAQRIT.ESTIMATED_VALUE  IS NOT NULL  AND SAQRIT.OBJECT_ID IS NOT NULL )A """.format(
                        UserId=user_id, QuoteRecordId=contract_quote_rec_id,
                        RevisionRecordId=quote_revision_rec_id,billing_end_date=billing_end_date,billing_day=billing_day,
                        BillingDate=billing_date,get_dc_cur_val=get_dc_cur_val,
                        get_val=get_val,year_amount_column_gl_curr=year_amount_column_gl_curr,
                        service_id = service_id,billing_type =get_billing_type,amount_column=amount_column,amount_column_split=amount_column_split,get_round_val=get_round_val))
            Sql.RunQuery("""INSERT SAQIBP (					
                        QUOTE_ITEM_BILLING_PLAN_RECORD_ID, BILLING_END_DATE, BILLING_START_DATE,ANNUAL_BILLING_AMOUNT,ANNBILAMT_INGL_CURR,BILADJAMT_INGL_CURR,BILADJ_DTYFLG,TTLMRG_INGL_CURR,BILLING_VALUE, BILLING_VALUE_INGL_CURR,BILLING_TYPE,LINE, QUOTE_ID, QTEITM_RECORD_ID, COMMITTED_VALUE_INGL_CURR,ESTVAL_INGL_CURR,DOC_CURRENCY,ESTVAL_INDT_CURR,
                        QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,
                        BILLING_DATE, BILLING_YEAR,BILLING_DAY,
                        EQUIPMENT_DESCRIPTION, EQUIPMENT_ID, EQUIPMENT_RECORD_ID, QTEITMCOB_RECORD_ID, 
                        SERVICE_DESCRIPTION, SERVICE_ID, GLOBAL_CURRENCY,GLOBALCURRENCY_RECORD_ID, SERVICE_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID, SERIAL_NUMBER, WARRANTY_START_DATE, WARRANTY_END_DATE,CONTRACT_START_DATE,CONTRACT_END_DATE,UOM,STATUS,SAP_PART_NUMBER,OBJECT_TYPE,OBJECT_ID,LINE_TYPE,KIT_NUMBER,KIT_NAME,FABLOCATION_ID,COUNT_OF_ASSEMBLY,AGS_POSS_ID,UPDATED_CRM,TEMP_TOOL,PM_ID,MNTEVT_LEVEL,GOT_CODE,CUSTOMER_TOOL_ID,ASSEMBLY_ID,CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED,PAR_SERVICE_ID,PAR_SERVICE_RECORD_ID
                    ) 
                    SELECT 
                        CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_BILLING_PLAN_RECORD_ID,  
                        {billing_end_date} as BILLING_END_DATE,
                        {BillingDate} as BILLING_START_DATE,
                        {amount_column} AS ANNUAL_BILLING_AMOUNT,
                        {year_amount_column_gl_curr} AS ANNBILAMT_INGL_CURR,
                        {year_amount_column_gl_curr} AS BILADJAMT_INGL_CURR,
                        0 as BILADJ_DTYFLG,
                        TOTAL_MARGIN AS TTLMRG_INGL_CURR,
                        0  as BILLING_VALUE,
                        0  as  BILLING_VALUE_INGL_CURR,
                        '{billing_type}' as BILLING_TYPE,
                        LINE,
                        QUOTE_ID,
                        QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID,
                        
                        COMVAL_INGL_CURR as COMMITTED_VALUE_INGL_CURR,
                        CAST(ROUND(ISNULL({year_amount_column_gl_curr},0),{get_round_val})/ {get_val} AS DECIMAL(20,{get_round_val}))	as 	ESTVAL_INGL_CURR,
                        DOC_CURRENCY AS DOC_CURRENCY,
                        CAST(ROUND(ISNULL({amount_column},0),{get_dc_cur_val})/ {get_val} AS DECIMAL(20,{get_dc_cur_val})) as ESTVAL_INDT_CURR,	
                        QUOTE_RECORD_ID,
                        QTEREV_ID,
                        QTEREV_RECORD_ID,
                        {BillingDate} as BILLING_DATE,						
                        '{amount_column_split}' as BILLING_YEAR,
                        '{billing_day}' as BILLING_DAY,
                        '' as EQUIPMENT_DESCRIPTION,
                        '' as EQUIPMENT_ID,									
                        '' as EQUIPMENT_RECORD_ID,						
                        '' as QTEITMCOB_RECORD_ID,
                        SERVICE_DESCRIPTION,
                        SERVICE_ID,
                        GLOBAL_CURRENCY,
                        GLOBAL_CURRENCY_RECORD_ID,
                        SERVICE_RECORD_ID, 
                        GREENBOOK,
                        GREENBOOK_RECORD_ID,
                        '' AS SERIAL_NUMBER,
                        '' as WARRANTY_START_DATE,
                        '' as WARRANTY_END_DATE,
                        CONTRACT_VALID_FROM AS CONTRACT_START_DATE,
                        CONTRACT_VALID_TO AS CONTRACT_END_DATE,
                        UOM,
                        STATUS,
                        SAP_PART_NUMBER,
                        OBJECT_TYPE,
                        OBJECT_ID,
                        LINE_TYPE,
                        KIT_NUMBER,
                        KIT_NAME,
                        FABLOCATION_ID,
                        COUNT_OF_ASSEMBLIES AS COUNT_OF_ASSEMBLY,
                        AGS_POSS_ID,
                        UPDATED_CRM,
                        TEMP_TOOL,
                        PM_ID,
                        MNTEVT_LEVEL,
                        GOT_CODE,
                        CUSTOMER_TOOL_ID,
                        ASSEMBLY_ID,        
                        {UserId} as CPQTABLEENTRYADDEDBY, 
                        GETDATE() as CPQTABLEENTRYDATEADDED,
                        PAR_PRDOFR_ID,	
                        PAR_PRDOFR_RECORD_ID
                    FROM  SAQRIT (NOLOCK) 
                    WHERE QUOTE_RECORD_ID='{QuoteRecordId}' AND  ESTIMATED_VALUE IS NOT NULL AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID ='{service_id}' AND (OBJECT_ID  IS NULL OR OBJECT_ID = '')""".format(
                        UserId=user_id, QuoteRecordId=contract_quote_rec_id,billing_day=billing_day,
                        RevisionRecordId=quote_revision_rec_id,get_dc_cur_val=get_dc_cur_val,
                        BillingDate=billing_date,billing_end_date=billing_end_date,
                        get_val=get_val,year_amount_column_gl_curr=year_amount_column_gl_curr,
                        service_id = service_id,billing_type =get_billing_type,amount_column=amount_column,amount_column_split=amount_column_split,get_round_val=get_round_val))
        #A055S000P01-20779 End - M
            
    if service_id == 'Z0116':
        update_annual_bill_amt  = Sql.GetFirst("SELECT SUM(NET_VALUE_INGL_CURR) as YEAR1 from SAQRIT (NOLOCK) where QUOTE_RECORD_ID='{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_rec_id}'  and SERVICE_ID = 'Z0116' GROUP BY SERVICE_ID,GREENBOOK".format(contract_quote_rec_id=contract_quote_rec_id,quote_revision_rec_id=quote_revision_rec_id))
        if update_annual_bill_amt:
            update_credit_amt = "UPDATE SAQIBP SET ANNUAL_BILLING_AMOUNT ={amt} where QUOTE_RECORD_ID='{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_rec_id}'  and SERVICE_ID = 'Z0116' GROUP BY SERVICE_ID,GREENBOOK ".format(amt=update_annual_bill_amt.YEAR1,contract_quote_rec_id=contract_quote_rec_id,quote_revision_rec_id=quote_revision_rec_id)
            Sql.RunQuery(update_credit_amt)
    return True

def _quote_items_greenbook_summary_insert():	
    greenbook_summary_last_line_no = 0
    Sql.RunQuery("DELETE FROM SAQIGS where QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'".format(QuoteRecordId=contract_quote_rec_id,RevisionRecordId=quote_revision_rec_id))
    quote_item_summary_obj = Sql.GetFirst("SELECT TOP 1 LINE FROM SAQIGS (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' ORDER BY LINE DESC".format(QuoteRecordId=contract_quote_rec_id,RevisionRecordId=quote_revision_rec_id))
    if quote_item_summary_obj:
        greenbook_summary_last_line_no = int(quote_item_summary_obj.LINE)
    Sql.RunQuery("""INSERT SAQIGS (CONTRACT_VALID_FROM, CONTRACT_VALID_TO, GLOBAL_CURRENCY, GLOBAL_CURRENCY_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, QUOTE_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, QTEITMSUM_RECORD_ID, COMMITTED_VALUE_INGL_CURR, ESTVAL_INGL_CURR, NET_VALUE_INGL_CURR, DOC_CURRENCY, DOCCURR_RECORD_ID, COMMITTED_VALUE, ESTIMATED_VALUE, NET_VALUE, PAR_SERVICE_ID, PAR_SERVICE_RECORD_ID, LINE, QUOTE_REV_ITEM_GREENBK_SUMRY_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified)
        SELECT IQ.*, ROW_NUMBER()OVER(ORDER BY(IQ.GREENBOOK)) + {ItemGreenbookSummaryLastLineNo} as LINE, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REV_ITEM_GREENBK_SUMRY_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED,{UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
            SELECT DISTINCT
                SAQTRV.CONTRACT_VALID_FROM,
                SAQTRV.CONTRACT_VALID_TO,
                SAQTRV.GLOBAL_CURRENCY,
                SAQTRV.GLOBAL_CURRENCY_RECORD_ID,						
                SQ.GREENBOOK,
                SQ.GREENBOOK_RECORD_ID,
                SQ.SERVICE_DESCRIPTION,
                SQ.SERVICE_ID,
                SQ.SERVICE_RECORD_ID,
                SAQTRV.QUOTE_ID,
                SAQTRV.QUOTE_RECORD_ID,
                SAQTMT.QTEREV_ID,
                SAQTMT.QTEREV_RECORD_ID,
                SQ.QTEITMSUM_RECORD_ID,
                SQ.COMMITTED_VALUE_INGL_CURR as COMMITTED_VALUE_INGL_CURR,
                SQ.ESTVAL_INGL_CURR as ESTVAL_INGL_CURR,
                SQ.NET_VALUE_INGL_CURR as NET_VALUE_INGL_CURR,
                SQ.DOC_CURRENCY,
                SQ.DOCCURR_RECORD_ID as DOCCURR_RECORD_ID,
                SQ.COMMITTED_VALUE as COMMITTED_VALUE,
                SQ.ESTIMATED_VALUE as ESTIMATED_VALUE,
                SQ.NET_VALUE as NET_VALUE,
                SQ.PAR_SERVICE_ID,
                SQ.PAR_SERVICE_RECORD_ID
            FROM (
                    SELECT 
                        SAQRIT.QUOTE_RECORD_ID, 
                        SAQRIT.QTEREV_RECORD_ID,   
                        SAQRIT.SERVICE_DESCRIPTION,
                        SAQRIT.SERVICE_ID,
                        SAQRIT.SERVICE_RECORD_ID,
                        SAQRIT.GREENBOOK,
                        SAQRIT.GREENBOOK_RECORD_ID,
                        SAQRIT.QTEITMSUM_RECORD_ID,
                        SUM(SAQRIT.COMMITTED_VALUE) as COMMITTED_VALUE_INGL_CURR,
                        SUM(SAQRIT.ESTVAL_INGL_CURR) as ESTVAL_INGL_CURR,
                        SUM(SAQRIT.NET_VALUE_INGL_CURR) as NET_VALUE_INGL_CURR,
                        SAQRIT.DOC_CURRENCY,
                        SAQRIT.DOCURR_RECORD_ID as DOCCURR_RECORD_ID,
                        SUM(SAQRIT.COMMITTED_VALUE) as COMMITTED_VALUE,
                        SUM(SAQRIT.ESTIMATED_VALUE) as ESTIMATED_VALUE,
                        SUM(SAQRIT.NET_VALUE) as NET_VALUE,
                        ISNULL(SAQRIT_SELF.SERVICE_ID,'') as PAR_SERVICE_ID,
                        ISNULL(SAQRIT_SELF.SERVICE_RECORD_ID,'') as PAR_SERVICE_RECORD_ID
                    FROM SAQRIT (NOLOCK) 
                    LEFT JOIN SAQRIT (NOLOCK) SAQRIT_SELF ON SAQRIT_SELF.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID
                                                AND SAQRIT_SELF.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID
                                                AND SAQRIT_SELF.LINE = SAQRIT.PARQTEITM_LINE
                    WHERE SAQRIT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' 
                    and SAQRIT.TOTAL_AMOUNT IS NOT NULL  AND SAQRIT.SERVICE_ID NOT IN ('Z0101','A6200','Z0108','Z0110','Z0048') GROUP BY SAQRIT.QUOTE_RECORD_ID, SAQRIT.QTEREV_RECORD_ID, SAQRIT.SERVICE_DESCRIPTION, SAQRIT.SERVICE_ID, SAQRIT.SERVICE_RECORD_ID, SAQRIT.GREENBOOK, SAQRIT.GREENBOOK_RECORD_ID, SAQRIT.QTEITMSUM_RECORD_ID, SAQRIT.DOC_CURRENCY, SAQRIT.DOCURR_RECORD_ID,SAQRIT_SELF.SERVICE_ID,SAQRIT_SELF.SERVICE_RECORD_ID
                ) SQ
            JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SQ.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = SQ.QTEREV_RECORD_ID     
            JOIN SAQTRV (NOLOCK) ON SAQTRV.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID AND SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID			
            ) IQ			
            LEFT JOIN SAQIGS (NOLOCK) ON SAQIGS.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND SAQIGS.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND SAQIGS.SERVICE_RECORD_ID = IQ.SERVICE_RECORD_ID AND SAQIGS.GREENBOOK_RECORD_ID = IQ.GREENBOOK_RECORD_ID AND SAQIGS.PAR_SERVICE_RECORD_ID = IQ.PAR_SERVICE_RECORD_ID
            WHERE ISNULL(SAQIGS.GREENBOOK_RECORD_ID,'') = ''
    """.format(UserId=user_id, UserName=user_name, QuoteRecordId= contract_quote_rec_id,QuoteRevisionRecordId=quote_revision_rec_id, ItemGreenbookSummaryLastLineNo=greenbook_summary_last_line_no))
    Sql.RunQuery("""UPDATE SAQIGS
            SET SAQIGS.CONTRACT_VALID_FROM = SAQTSV.CONTRACT_VALID_FROM,SAQIGS.CONTRACT_VALID_TO = SAQTSV.CONTRACT_VALID_TO FROM SAQTSV INNER JOIN SAQIGS ON SAQIGS.QUOTE_RECORD_ID = SAQTSV.QUOTE_RECORD_ID AND SAQIGS.QTEREV_RECORD_ID = SAQTSV.QTEREV_RECORD_ID AND SAQIGS.SERVICE_ID = SAQTSV.SERVICE_ID AND SAQIGS.PAR_SERVICE_ID = SAQTSV.PAR_SERVICE_ID WHERE SAQTSV.QUOTE_RECORD_ID='{QuoteRecordId}' and SAQTSV.QTEREV_RECORD_ID='{QuoteRevisionRecordId}'""".format(QuoteRecordId= contract_quote_rec_id,QuoteRevisionRecordId=quote_revision_rec_id))
    return True

def _get_tool_yearwise_dates(start_date=None, end_date=None, contract_dates_dict=None):
    yearwise_dates_dict = {}
    count = 0
    for year, contract_dates in contract_dates_dict.items():       
        #Trace.Write("====contract_dates ====>>> "+str(contract_dates))
        if contract_dates.get('start_date') <= start_date <= contract_dates.get('end_date'): 
            yearwise_dates_dict['YEAR_{}'.format(year)] = {}
            yearwise_dates_dict['YEAR_{}'.format(year)]['start_date'] = start_date
            if contract_dates.get('start_date') <= end_date <= contract_dates.get('end_date'):
                yearwise_dates_dict['YEAR_{}'.format(year)]['end_date'] = end_date
                year_datediff  = end_date - start_date
                count = 0
            else:
                yearwise_dates_dict['YEAR_{}'.format(year)]['end_date'] = contract_dates.get('end_date')
                year_datediff  = contract_dates.get('end_date') - start_date
                count += 1            
            
            yearwise_dates_dict['YEAR_{}'.format(year)].update({'total_days':year_datediff.days + 1})			
        elif contract_dates.get('start_date') > start_date:
            yearwise_dates_dict['YEAR_{}'.format(year)] = {}
            yearwise_dates_dict['YEAR_{}'.format(year)]['start_date'] = contract_dates.get('start_date')
            if contract_dates.get('start_date') <= end_date <= contract_dates.get('end_date'):
                yearwise_dates_dict['YEAR_{}'.format(year)]['end_date'] = end_date
                year_datediff  = end_date - contract_dates.get('start_date')
                count = 0
            else:
                yearwise_dates_dict['YEAR_{}'.format(year)]['end_date'] = contract_dates.get('end_date')
                year_datediff  = contract_dates.get('end_date') - contract_dates.get('start_date')
                count += 1            
            yearwise_dates_dict['YEAR_{}'.format(year)].update({'total_days':year_datediff.days + 1})					  
        elif count:
            yearwise_dates_dict['YEAR_{}'.format(year)] = {}
            yearwise_dates_dict['YEAR_{}'.format(year)]['start_date'] = contract_dates.get('start_date')
            if contract_dates.get('start_date') <= end_date <= contract_dates.get('end_date'):
                yearwise_dates_dict['YEAR_{}'.format(year)]['end_date'] = end_date
                year_datediff  = end_date - contract_dates.get('start_date')
                count = 0
            else:
                yearwise_dates_dict['YEAR_{}'.format(year)]['end_date'] = contract_dates.get('end_date')
                year_datediff  = contract_dates.get('end_date') - contract_dates.get('start_date')
                count += 1            

            yearwise_dates_dict['YEAR_{}'.format(year)].update({'total_days':year_datediff.days + 1})
    return yearwise_dates_dict
    
def billingmatrix_create():	
    _quote_items_greenbook_summary_insert()
    contract_datediff = 0
    contract_header_start_date = ''
    contract_header_end_date = ''
    quote_revision_obj = Sql.GetFirst("SELECT CONTRACT_VALID_FROM,CONTRACT_VALID_TO FROM SAQTRV (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(contract_quote_rec_id,quote_revision_rec_id))
    if quote_revision_obj:
        contract_header_start_date = quote_revision_obj.CONTRACT_VALID_FROM
        contract_header_start_datetime = datetime.datetime.strptime(UserPersonalizationHelper.ToUserFormat(quote_revision_obj.CONTRACT_VALID_FROM), '%m/%d/%Y')
        contract_header_end_datetime = datetime.datetime.strptime(UserPersonalizationHelper.ToUserFormat(quote_revision_obj.CONTRACT_VALID_TO), '%m/%d/%Y')
        contract_header_end_date = contract_header_end_datetime
        contract_datediff = contract_header_end_datetime - contract_header_start_datetime		 
    billing_plan_obj = Sql.GetList("SELECT DISTINCT PRDOFR_ID,BILLING_START_DATE,BILLING_END_DATE,BILLING_DAY, QUOTE_ID,ISNULL(PAR_SERVICE_ID,'') as PAR_SERVICE_ID FROM SAQRIB (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(contract_quote_rec_id,quote_revision_rec_id))
    get_billling_data_dict = {}
    #598 Qc defect start
    get_ent_val = get_ent_billing_type_value = get_ent_bill_cycle = get_billing_type = ''
    if billing_plan_obj:
        #based on revision status start
        get_workflow_status_details = Sql.GetFirst("SELECT WORKFLOW_STATUS FROM SAQTRV (NOLOCK) where QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'""".format(QuoteRecordId=contract_quote_rec_id,RevisionRecordId=quote_revision_rec_id))
        #based on revision end not in ("APPROVALS","LEGAL SOW","OUTPUT DOCUMENTS","CLEAN BOOKING CHECKLIST","BOOKED")
        if get_workflow_status_details.WORKFLOW_STATUS not in ("APPROVALS","LEGAL SOW","OUTPUT DOCUMENTS","CLEAN BOOKING CHECKLIST","BOOKED"):
            Sql.RunQuery("""DELETE FROM SAQIBP WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'""".format(QuoteRecordId=contract_quote_rec_id,RevisionRecordId=quote_revision_rec_id))
            for val in billing_plan_obj:
                if billing_plan_obj:					
                    get_billling_data_dict = {}		
                    billing_day = val.BILLING_DAY
                    get_service_val = val.PRDOFR_ID
                    #INC08696998 M	
                    #if get_service_val == 'Z0105':	
                        #par_service_id = val.PAR_SERVICE_ID	
                    #else:	
                        #par_service_id = ""	
                        
                    par_service_id = val.PAR_SERVICE_ID	
                    #INC08696998 M
                    # if val.BILLING_DAY_OF_THE_WEEK:
                    #     selected_day_of_week = val.BILLING_DAY_OF_THE_WEEK
                    # else:
                    #     selected_day_of_week =''
                    if par_service_id:
                        quotedetails = Sql.GetFirst("SELECT CONTRACT_VALID_FROM,CONTRACT_VALID_TO FROM SAQTSV (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID='{}' AND ISNULL(PAR_SERVICE_ID,'') = '{}'".format(contract_quote_rec_id,quote_revision_rec_id,get_service_val,par_service_id))
                    else:
                        quotedetails = Sql.GetFirst("SELECT CONTRACT_VALID_FROM,CONTRACT_VALID_TO FROM SAQTSV (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID='{}'".format(contract_quote_rec_id,quote_revision_rec_id,get_service_val))
                    contract_start_date = quotedetails.CONTRACT_VALID_FROM
                    contract_end_date = quotedetails.CONTRACT_VALID_TO					
                    start_date = datetime.datetime.strptime(UserPersonalizationHelper.ToUserFormat(contract_start_date), '%m/%d/%Y')
                    #INC08840688 Start - M
                    if get_service_val == 'Z0116':
                        get_billing_cycle = Sql.GetFirst("SELECT SAQITE.BILLING_CYCLE, SAQITE.BILLING_TYPE FROM SAQRIT (NOLOCK) JOIN SAQITE (NOLOCK) ON SAQITE.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND SAQITE.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID AND SAQITE.SERVICE_ID = SAQRIT.SERVICE_ID AND SAQITE.LINE = SAQRIT.LINE WHERE SAQRIT.QUOTE_RECORD_ID = '{qtid}' AND SAQRIT.QTEREV_RECORD_ID = '{qt_rev_id}' AND SAQRIT.SERVICE_ID = '{ServiceId}' AND ISNULL(SAQRIT.PAR_PRDOFR_ID,'') = '{ParServiceId}'".format(qtid=contract_quote_rec_id,qt_rev_id=quote_revision_rec_id,ServiceId = str(get_service_val).strip(),ParServiceId = par_service_id ))
                    else:
                        get_billing_cycle = Sql.GetFirst("SELECT SAQITE.BILLING_CYCLE, SAQITE.BILLING_TYPE FROM SAQRIT (NOLOCK) JOIN SAQITE (NOLOCK) ON SAQITE.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND SAQITE.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID AND SAQITE.SERVICE_ID = SAQRIT.SERVICE_ID AND SAQITE.LINE = SAQRIT.LINE LEFT JOIN SAQRIT (NOLOCK) SAQRIT_SELF ON SAQRIT_SELF.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND SAQRIT_SELF.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID AND SAQRIT_SELF.LINE = SAQRIT.PARQTEITM_LINE WHERE SAQRIT.QUOTE_RECORD_ID = '{qtid}' AND SAQRIT.QTEREV_RECORD_ID = '{qt_rev_id}' AND SAQRIT.SERVICE_ID = '{ServiceId}' AND ISNULL(SAQRIT_SELF.SERVICE_ID,'') = '{ParServiceId}'".format(qtid=contract_quote_rec_id,qt_rev_id=quote_revision_rec_id,ServiceId = str(get_service_val).strip(),ParServiceId = par_service_id))
                    #INC08840688 End - M
                    
                    if get_billing_cycle:
                        get_billling_data_dict['billing_cycle'] = get_billing_cycle.BILLING_CYCLE
                        get_billling_data_dict['billing_type'] = get_billing_cycle.BILLING_TYPE
                        get_ent_bill_cycle = get_billing_cycle.BILLING_CYCLE
                                        
                    billing_month_end = 0
                    
                    end_date = datetime.datetime.strptime(UserPersonalizationHelper.ToUserFormat(contract_end_date), '%m/%d/%Y')
                    datediff = end_date - start_date
                    if get_service_val == "Z0105":
                        get_ent_bill_cycle = "MONTHLY"
                    if str(get_ent_bill_cycle).upper() == "ONE ITEM PER QUOTE":
                        avgyear = 365.2425        # pedants definition of a year length with leap years
                        avgmonth = 365.2425/12.0  # even leap years have 12 months
                        years, remainder = divmod(datediff.days, avgyear)
                        years, months = int(years), int(remainder // avgmonth)
                        total_months = years * 12 + months						
                        for index in range(0, total_months+1):						
                            billing_month_end += 1
                            if str(index) in ['0','12','24','36','48']:
                                insert_item_per_billing(total_months=total_months, 
                                                        billing_date="DATEADD(month, {Month}, '{BillingDate}')".format(
                                                            Month=index, BillingDate=start_date.strftime('%m/%d/%Y')
                                                            ),billing_end_date="DATEADD(month, {Month_add}, '{BillingDate}')".format(
                                                            Month_add=billing_month_end, BillingDate=start_date.strftime('%m/%d/%Y')
                                                            ), amount_column="YEAR_"+str((index/12) + 1),
                                                            service_id = get_service_val,get_ent_val_type = get_ent_bill_cycle,get_ent_billing_type_value = get_ent_billing_type_value,get_billling_data_dict=get_billling_data_dict,billing_day=billing_day,datediff=datediff)
                    elif str(get_ent_bill_cycle).upper() == "MONTHLY":
                        start = 1
                        end = 1000
                        count = 1
                        quote_items_records = []
                        while count == 1:
                            #INC08696998 M
                            if get_service_val == 'Z0105':
                                parrr_service_id = val.PAR_SERVICE_ID
                                parent_based_where_condition = ""
                            else:
                                parrr_service_id = ""
                                parent_based_where_condition = "AND ISNULL(SAQRIT.PAR_PRDOFR_ID,'') = '{prdoff}'".format(prdoff=val.PAR_SERVICE_ID)
                            quote_items_obj = Sql.GetList("SELECT DISTINCT QUOTE_REVISION_CONTRACT_ITEM_ID, CONTRACT_VALID_FROM, CONTRACT_VALID_TO, YEAR_2 ,YEAR_2_INGL_CURR, YEAR_3, YEAR_3_INGL_CURR, YEAR_1, YEAR_1_INGL_CURR, YEAR_4, YEAR_4_INGL_CURR, YEAR_5, YEAR_5_INGL_CURR, ISNULL(OBJECT_ID,'') as OBJECT_ID, GREENBOOK, LINE, NET_VALUE, NET_VALUE_INGL_CURR FROM (SELECT SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID, SAQRIT.CONTRACT_VALID_FROM, SAQRIT.CONTRACT_VALID_TO, ISNULL(SAQRIT.YEAR_2,0) as YEAR_2,ISNULL(SAQRIT.YEAR_2_INGL_CURR, 0) as YEAR_2_INGL_CURR, ISNULL(SAQRIT.YEAR_3, 0) as YEAR_3, ISNULL(SAQRIT.YEAR_3_INGL_CURR,0) as YEAR_3_INGL_CURR, ISNULL(SAQRIT.YEAR_1,0) as YEAR_1, ISNULL(SAQRIT.YEAR_1_INGL_CURR,0) as YEAR_1_INGL_CURR, ISNULL(SAQRIT.YEAR_4, 0) as YEAR_4, ISNULL(SAQRIT.YEAR_4_INGL_CURR,0) as YEAR_4_INGL_CURR, ISNULL(SAQRIT.YEAR_5, 0) as YEAR_5, ISNULL(SAQRIT.YEAR_5_INGL_CURR,0) as YEAR_5_INGL_CURR, ISNULL(SAQRIT.OBJECT_ID,'') as OBJECT_ID, SAQRIT.GREENBOOK, SAQRIT.LINE, ISNULL(SAQRIT.NET_VALUE,0) as NET_VALUE, ISNULL(SAQRIT.NET_VALUE_INGL_CURR,0) as NET_VALUE_INGL_CURR,ISNULL(SAQRIT.SERVICE_ID,'') as PAR_SERVICE_ID, ROW_NUMBER() OVER(ORDER BY SAQRIT.LINE) AS SNO FROM SAQRIT (NOLOCK) LEFT JOIN SAQRIT (NOLOCK) SAQRIT_SELF ON SAQRIT_SELF.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND SAQRIT_SELF.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID AND SAQRIT_SELF.LINE = SAQRIT.PARQTEITM_LINE WHERE SAQRIT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQRIT.SERVICE_ID = '{ServiceId}' {ParentBasedWhereCondition} AND ISNULL(SAQRIT_SELF.SERVICE_ID,'') = '{ParServiceId}')A WHERE SNO>={Start} AND SNO<={End}".format(QuoteRecordId=contract_quote_rec_id, QuoteRevisionRecordId=quote_revision_rec_id, ServiceId=get_service_val, ParServiceId=parrr_service_id, Start=start, End=end, ParentBasedWhereCondition=parent_based_where_condition))
                            
                            if quote_items_obj:
                                for quote_item_obj in quote_items_obj:
                                    quote_items_records.append({data.Key:data.Value for data in quote_item_obj})									
                                start = start + 1000
                                end = end + 1000
                            else:
                                count = 0
                        avgyear = 365.2425       # pedants definition of a year length with leap years
                        avgmonth = 365.2425/12.0  # even leap years have 12 months
                        years, remainder = divmod(contract_datediff.days, avgyear)
                        years, months = int(years), (remainder / avgmonth) #INC08814916 - M
                        if months > 0:
                            years += 1 
                        yearwise_dates_dict = {}
                        billing_dates_list = []
                        for year in range(1, years+1):
                            # Find yearwise start and end date till contract end - start
                            date_obj = Sql.GetFirst("""SELECT DATEADD(day,-1,DATEADD(year, {YearIncrement}, '{DateString}')) AS EndDate, DATEADD(year, {YearIncrement}, '{DateString}') AS StartDate""".format(DateString=contract_header_start_date, YearIncrement=year))
                            if year == 1:
                                yearwise_dates_dict[year] = {'start_date':datetime.datetime.strptime(UserPersonalizationHelper.ToUserFormat(contract_header_start_date), '%m/%d/%Y').date()}
                            year_end_date = datetime.datetime.strptime(UserPersonalizationHelper.ToUserFormat(date_obj.EndDate), '%m/%d/%Y').date()
                            #Trace.Write(str(end_date.date())+"============>>> "+str(year_end_date))
                            if contract_header_end_date.date() < year_end_date:
                                year_end_date = contract_header_end_date.date()
                            yearwise_dates_dict[year].update({'end_date':year_end_date})
                            if year+1 <= years:      
                                yearwise_dates_dict[year+1] = {'start_date':datetime.datetime.strptime(UserPersonalizationHelper.ToUserFormat(date_obj.StartDate), '%m/%d/%Y').date()}
                            # Find yearwise start and end date till contract end - end
                            year_start_date = yearwise_dates_dict.get(year).get('start_date')
                            #Trace.Write(str(year_start_date)+"=======-Year wise Start and End date ---------=====>>> "+str(year_end_date))
                            year_datediff  = year_end_date - year_start_date
                            avgyear = 365.2425       # pedants definition of a year length with leap years
                            avgmonth = 365.2425/12.0  # even leap years have 12 months
                            one_year, remainder = divmod(year_datediff.days, avgyear)
                            one_year, months = int(one_year), (remainder / avgmonth) #INC08814916 - M
                            total_months = math.ceil(one_year * 12 + months) #INC08814916 - M
                        
                            #Trace.Write(str(year)+"=======-total_months---------=====>>> "+str(total_months))
                            month_increment_index = 0
                            billing_month_increment_index = 0
                            while month_increment_index < total_months:
                                if month_increment_index == 0:           
                                    if billing_day == "Last day of Month":
                                        date_obj = Sql.GetFirst("""SELECT CONVERT(date, '{DateString}') AS StartOfMonth, EOMONTH(DATEADD(month, {MonthIncrement}, '{DateString}')) AS EndOfMonth, EOMONTH(DATEADD(month, {BillingMonthIncrement}, '{DateString}')) AS BillingDate""".format(DateString=year_start_date, MonthIncrement=month_increment_index, BillingMonthIncrement=billing_month_increment_index,Day=billing_day))
                                    else:
                                        date_obj = Sql.GetFirst("""SELECT CONVERT(date, '{DateString}') AS StartOfMonth, EOMONTH(DATEADD(month, {MonthIncrement}, '{DateString}')) AS EndOfMonth, dateadd(dd, {Day}, eomonth(DATEADD(month, DATEDIFF(month, 0, DATEADD(month, {BillingMonthIncrement}, '{DateString}')), 0), -1)) AS BillingDate""".format(DateString=year_start_date, MonthIncrement=month_increment_index, BillingMonthIncrement=billing_month_increment_index, Day=billing_day))
                                else:
                                    if billing_day == "Last day of Month":
                                        date_obj = Sql.GetFirst("""SELECT DATEADD(month, DATEDIFF(month, 0, DATEADD(month, {MonthIncrement}, '{DateString}')), 0) AS StartOfMonth, EOMONTH(DATEADD(month, {MonthIncrement}, '{DateString}')) AS EndOfMonth, EOMONTH(DATEADD(month, {BillingMonthIncrement}, '{DateString}')) AS BillingDate""".format(DateString=year_start_date, MonthIncrement=month_increment_index, BillingMonthIncrement=billing_month_increment_index, Day=billing_day))
                                    else:
                                        date_obj = Sql.GetFirst("""SELECT DATEADD(month, DATEDIFF(month, 0, DATEADD(month, {MonthIncrement}, '{DateString}')), 0) AS StartOfMonth, EOMONTH(DATEADD(month, {MonthIncrement}, '{DateString}')) AS EndOfMonth, dateadd(dd, {Day}, eomonth(DATEADD(month, DATEDIFF(month, 0, DATEADD(month, {BillingMonthIncrement}, '{DateString}')), 0), -1)) AS BillingDate""".format(DateString=year_start_date, MonthIncrement=month_increment_index, BillingMonthIncrement=billing_month_increment_index, Day=billing_day))
                                if date_obj:
                                    billing_start_date = datetime.datetime.strptime(UserPersonalizationHelper.ToUserFormat(date_obj.StartOfMonth), '%m/%d/%Y').date()
                                    billing_end_date = datetime.datetime.strptime(UserPersonalizationHelper.ToUserFormat(date_obj.EndOfMonth), '%m/%d/%Y').date()
                                    billing_date = datetime.datetime.strptime(UserPersonalizationHelper.ToUserFormat(date_obj.BillingDate), '%m/%d/%Y').date()
                                    billing_day_converted = int(str(billing_end_date)[-2:]) if billing_day == "Last day of Month" else int(billing_day)
                                    
                                    if billing_end_date > year_end_date: # for multiyear scenario
                                        billing_end_date = year_end_date
                                    if year == years and billing_date > year_end_date:
                                        billing_date = year_end_date
                                    elif billing_day_converted < int(str(billing_start_date)[-2:]):
                                        billing_date_changed_obj = Sql.GetFirst("""SELECT DATEADD(month, 1, '{DateString}') AS BillingDate""".format(DateString=billing_date))
                                        billing_date = billing_date = datetime.datetime.strptime(UserPersonalizationHelper.ToUserFormat(billing_date_changed_obj.BillingDate), '%m/%d/%Y').date()
                                        billing_month_increment_index += 1
                                        #total_months += 1
                                    billing_dates_list.append({'start_date':billing_start_date, 'end_date':billing_end_date, 'billing_date':billing_date, 'year':'YEAR_{}'.format(year)})
                                # Increase months based on contract end date
                                if month_increment_index == (total_months - 1) and billing_dates_list[-1].get('end_date') < year_end_date:
                                    total_months += 1    
                                month_increment_index += 1
                                billing_month_increment_index += 1
                        Trace.Write("yearwise_dates_dict ==+> "+str(yearwise_dates_dict))
                        Trace.Write("billing_dates_list =====>>> "+str(billing_dates_list))
                        
                        datetime_string = datetime.datetime.now().strftime("%d%m%Y%H%M%S")
                        billing_temp_table_name = "BILLING_BKP_{}_{}".format(val.QUOTE_ID, datetime_string)		
                        #Trace.Write("======billing_temp_table_name=====GGGGG "+str(billing_temp_table_name))
                        billing_temp_table_drop = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(billing_temp_table_name)+"'' ) BEGIN DROP TABLE "+str(billing_temp_table_name)+" END  ' ")			
                        header = ['BILLING_START_DATE', 'BILLING_END_DATE', 'ANNUAL_BILLING_AMOUNT_COLUMN', 'SERVICE_ID', 'PAR_SERVICE_ID', 'BILLING_DAY', 'PER_MONTH_AMT', 'PER_MONTH_AMT_IN_GL_CURR', 'BILLING_DATE', 'QUOTE_REVISION_CONTRACT_ITEM_ID','BILLING_YEAR', 'QUOTE_RECORD_ID', 'QTEREV_RECORD_ID']
                        columns = ",".join(header)
                        records = []
                        for quote_item in quote_items_records:
                            quote_revision_contract_item_id = quote_item.get('QUOTE_REVISION_CONTRACT_ITEM_ID')
                            # INC08733470 - Start - M
                            year_count = 0
                            # INC08733470 - End - M
                            tool_contract_start_date = datetime.datetime.strptime(UserPersonalizationHelper.ToUserFormat(quote_item.get('CONTRACT_VALID_FROM')), '%m/%d/%Y').date()
                            tool_contract_end_date = datetime.datetime.strptime(UserPersonalizationHelper.ToUserFormat(quote_item.get('CONTRACT_VALID_TO')), '%m/%d/%Y').date()
                            
                            toolwise_date_details = _get_tool_yearwise_dates(start_date=tool_contract_start_date, end_date=tool_contract_end_date, contract_dates_dict=yearwise_dates_dict)
                            #Trace.Write("==== toolwise_date_details =====>>>> "+str(toolwise_date_details))
                            count_start = 0
                            # INC08733470 - Start - M
                            last_billing_plan_year = ''
                            # INC08733470 - Start - M
                            for index, billing_date_res in enumerate(billing_dates_list):
                                billing_plan_start_date = billing_date_res.get('start_date')
                                billing_plan_end_date = billing_date_res.get('end_date')  
                                billing_plan_year = billing_date_res.get('year')
                                billing_plan_date = billing_date_res.get('billing_date')
                                if billing_plan_year in toolwise_date_details.keys():
                                    toolwise_bill_plan_start_date = toolwise_date_details.get(billing_plan_year).get('start_date')
                                    toolwise_bill_plan_end_date = toolwise_date_details.get(billing_plan_year).get('end_date')
                                    total_days_per_month = 0                                
                                    if billing_plan_year in toolwise_date_details.keys():                                    
                                        if (billing_plan_start_date <= toolwise_bill_plan_start_date <= billing_date_res.get('end_date')) and (billing_plan_date >= toolwise_bill_plan_start_date) and count_start == 0:
                                            count_start += 1
                                            total_days_per_month = (billing_plan_end_date - toolwise_bill_plan_start_date).days                                        
                                            total_days_per_month += 1               
                                            billing_plan_start_date = toolwise_bill_plan_start_date
                                        elif (billing_plan_start_date > toolwise_bill_plan_start_date < billing_plan_date) and count_start == 0: #INC08700823 - A
                                            count_start += 1
                                            total_days_per_month = (billing_plan_end_date - toolwise_bill_plan_start_date).days                                        
                                            total_days_per_month += 1               
                                            billing_plan_start_date = toolwise_bill_plan_start_date
                                            #INC08700823 - A
                                        elif toolwise_bill_plan_end_date <= billing_plan_end_date and count_start:
                                            total_days_per_month = (toolwise_bill_plan_end_date - billing_plan_start_date).days
                                            total_days_per_month += 1
                                            billing_plan_end_date = toolwise_bill_plan_end_date
                                        elif count_start:
                                            total_days_per_month = (billing_plan_end_date - billing_plan_start_date).days
                                            total_days_per_month += 1                                        
                                                    
                                    if total_days_per_month:	
                                        # INC08733470 - Start - A
                                        if int(billing_plan_year[-1]) != year_count and last_billing_plan_year != billing_plan_year:
                                            year_count += 1
                                            last_billing_plan_year = billing_plan_year
                                        billing_plan_year_for_amount = billing_plan_year
                                        #CR704 - Start - M
                                        # if 'YEAR_'+str(year_count) != billing_plan_year:
                                        #     billing_plan_year_for_amount = 'YEAR_'+str(year_count) 	
                                        #CR704 - Stop - M			
                                        # INC08733470 - End - A										
                                        toolwise_contract_year_total_days = toolwise_date_details.get(billing_plan_year).get('total_days')
                                                    
                                        # INC08733470 - Start - M
                                        one_day_tool_amt = quote_item.get(billing_plan_year_for_amount)/toolwise_contract_year_total_days
                                        one_day_tool_amt_in_global_currency = quote_item.get(billing_plan_year_for_amount+'_INGL_CURR')/toolwise_contract_year_total_days
                                        # INC08733470 - End - M
                                        per_month_amt = one_day_tool_amt * total_days_per_month
                                        per_month_amt_in_global_currency = one_day_tool_amt_in_global_currency * total_days_per_month
                                        # Check the billing date is not greater than contract end date
                                        if tool_contract_end_date < billing_plan_date:
                                            billing_date = tool_contract_end_date
                                        else:
                                            billing_date = billing_plan_date
                                        #Trace.Write("==========>>>> billing_date "+str(billing_date))
                                        #hpqc 1989 negative value start
                                        if float(per_month_amt) > 0 or (get_service_val == 'Z0116' and float(per_month_amt) < 0) or (get_service_val == 'Z0117' and float(per_month_amt) < 0):
                                            #hpqc 1989 negative value end
                                            #INC08696998 M
                                            if get_service_val == 'Z0105':
                                                parr_service_id = val.PAR_SERVICE_ID
                                            else:
                                                parr_service_id = ""
                                            #INC08696998 M
                                            year_column_split = billing_plan_year.replace('_',' ')
                                            #year_amount_column_gl_curr= billing_plan_year+'_INGL_CURR'
                                            # INC08733470 - Start - M
                                            records.append([str(billing_plan_start_date), str(billing_plan_end_date), billing_plan_year_for_amount, get_service_val, parr_service_id, billing_day, str(per_month_amt), str(per_month_amt_in_global_currency), str(billing_date), quote_revision_contract_item_id, year_column_split])
                                            # INC08733470 - End - M
                                            # insert_items_monthly_billing_plan(billing_start_date=billing_plan_start_date,billing_end_date=billing_plan_end_date,year_column=billing_plan_year,service_id = get_service_val,get_ent_val_type = get_ent_bill_cycle,get_ent_billing_type_value =get_billing_type,get_billling_data_dict=None,billing_day=billing_day,per_month_amt=per_month_amt,per_month_amt_gl_curr=per_month_amt_in_global_currency,bill_service_date=billing_date,item_record_id = quote_item.get('QUOTE_REVISION_CONTRACT_ITEM_ID'))
                                #prorate_bill_amount(service_id = get_service_val, line = quote_item.get('LINE'))  
                        if records:
                            try:
                                rows_count =  len(records)
                                for count in range(0, rows_count, 5000):                                
                                    values = ', '.join(map(str, [str(tuple(list(record)+[contract_quote_rec_id, quote_revision_rec_id])) for record in records[count:count+5000]])).replace("None","null").replace("'","''")                        
                                    billing_temp_table_bkp = SqlHelper.GetFirst("sp_executesql @T=N'SELECT "+str(columns)+" INTO "+str(billing_temp_table_name)+" FROM (SELECT DISTINCT "+str(columns)+" FROM (VALUES "+str(values)+") AS TEMP("+str(columns)+")) OQ ' ")
                                    insert_items_monthly_billing_plan_records(billing_temp_table_name, get_service_val, par_service_id)
                                    billing_temp_table_drop = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(billing_temp_table_name)+"'' ) BEGIN DROP TABLE "+str(billing_temp_table_name)+" END  ' ")	
                            except Exception:
                                billing_temp_table_drop = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(billing_temp_table_name)+"'' ) BEGIN DROP TABLE "+str(billing_temp_table_name)+" END  ' ")
                            prorate_bill_amount(service_id = get_service_val)   
                    elif str(get_ent_bill_cycle).upper() == "WEEKLY":						
                        get_totalweeks,remainder = divmod(contract_datediff.days+1,7)
                        get_totalweeks = get_totalweeks + (1 if remainder > 0 else 0)
                        countweeks =0
                        billing_start_date = start_date
                        for index in range(0, get_totalweeks):
                            countweeks += 1
                            if get_totalweeks <= 53:
                                amount_column = "YEAR_1"	
                            else:
                                amount_column="YEAR_"+str((index/52) + 1)	
                            billing_week_end = start_date + datetime.timedelta(days=(7*countweeks))- datetime.timedelta(days=1)
                            insert_items_billing_plan(total_months=get_totalweeks, 
                                                    billing_date="DATEADD(month, {Month}, '{BillingDate}')".format(
                                                        Month=0, BillingDate=billing_start_date.strftime('%m/%d/%Y')
                                                        ),billing_end_date="DATEADD(month, {Month_add}, '{BillingDateAdd}')".format(
                                                        Month_add=0, BillingDateAdd=billing_week_end.strftime('%m/%d/%Y')
                                                        ), amount_column=amount_column,
                                                        service_id = get_service_val,get_ent_val_type = get_ent_bill_cycle,get_ent_billing_type_value = get_ent_billing_type_value,get_billling_data_dict=get_billling_data_dict,billing_day=billing_day,datediff=datediff)
                            #billing_start_date = start_date + datetime.timedelta(days=(7*countweeks))
                            billing_start_date = billing_week_end + datetime.timedelta(days=1)
                    elif str(get_ent_bill_cycle).upper() == "QUARTELY":
                        ct_start_date =contract_start_date
                        ct_end_date =contract_end_date
                        if ct_start_date>ct_end_date:
                            ct_start_date,ct_end_date=ct_end_date,ct_start_date
                        m1=ct_start_date.Year*12+ct_start_date.Month  
                        m2=ct_end_date.Year*12+ct_end_date.Month  
                        months=m2-m1
                        months=months/3
                        for index in range(0, months):
                            billing_month_end += 1
                            insert_items_billing_plan(total_months=months, 
                                                    billing_date="DATEADD(month, {Month}, '{BillingDate}')".format(
                                                        Month=index, BillingDate=start_date.strftime('%m/%d/%Y')
                                                        ),billing_end_date="DATEADD(month, {Month_add}, '{BillingDate}')".format(
                                                        Month_add=billing_month_end, BillingDate=start_date.strftime('%m/%d/%Y')
                                                        ),amount_column="YEAR_"+str((index/4) + 1),
                                                        service_id = get_service_val,get_ent_val_type = get_ent_val,get_ent_billing_type_value=get_ent_billing_type_value,get_billling_data_dict=get_billling_data_dict,billing_day=billing_day,datediff=datediff)
                    elif str(get_ent_bill_cycle).upper() == "MILESTONE":
                        get_milestones_data_dict = {}						
                        get_milestone_details = Sql.GetFirst("select ENTITLEMENT_XML from SAQTSE (NOLOCK) where QUOTE_RECORD_ID='{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID = '{ServiceId}' AND  ISNULL(PAR_SERVICE_ID,'') = '{ParServiceId}' ".format(QuoteRecordId=contract_quote_rec_id,RevisionRecordId=quote_revision_rec_id,ServiceId = str(get_service_val).strip(), ParServiceId=par_service_id))
                        if get_milestone_details:
                            updateentXML = get_milestone_details.ENTITLEMENT_XML
                            pattern_tag = re.compile(r'(<QUOTE_ITEM_ENTITLEMENT>[\w\W]*?</QUOTE_ITEM_ENTITLEMENT>)')
                            pattern_id = re.compile(r'<ENTITLEMENT_ID>(AGS_Z0007_PQB_MILEST|AGS_'+str(get_service_val)+'_PQB_MILST1|AGS_'+str(get_service_val)+'_PQB_MILST2|AGS_'+str(get_service_val)+'_PQB_MILST3|AGS_'+str(get_service_val)+'_PQB_MIL3DS|AGS_'+str(get_service_val)+'_PQB_MIL1DS|AGS_'+str(get_service_val)+'_PQB_MIL2DS|AGS_'+str(get_service_val)+'_PQB_MIL3BD|AGS_'+str(get_service_val)+'_PQB_MIL2BD|AGS_'+str(get_service_val)+'_PQB_MIL1BD|AGS_'+str(get_service_val)+'_PQB_MILES3|AGS_'+str(get_service_val)+'_PQB_MILES1|AGS_'+str(get_service_val)+'_PQB_MILES2)</ENTITLEMENT_ID>')
                            pattern_name = re.compile(r'<ENTITLEMENT_DISPLAY_VALUE>([^>]*?)</ENTITLEMENT_DISPLAY_VALUE>')
                            for m in re.finditer(pattern_tag, updateentXML):
                                sub_string = m.group(1)
                                get_ent_id = re.findall(pattern_id,sub_string)
                                get_ent_val= re.findall(pattern_name,sub_string)
                                if get_ent_id:
                                    get_ent_val = str(get_ent_val[0])
                                    get_milestones_data_dict[get_ent_id[0]] = str(get_ent_val)
                        Trace.Write('get_milestones_data_dict--'+str(get_milestones_data_dict))
                        
                        if get_milestones_data_dict.get("AGS_Z0006_PQB_MIL3BD"):
                            milestone_amt = get_milestones_data_dict.get("AGS_Z0006_PQB_MILES3")
                            milestone_date = get_milestones_data_dict.get("AGS_Z0006_PQB_MIL3BD")
                            fts_z0006_z0007_insert(milestone_amt=milestone_amt,milestone_date=milestone_date,
                                            service_id=get_service_val,par_service_id=par_service_id)
                        if  get_milestones_data_dict.get("AGS_Z0006_PQB_MIL2BD"):
                            milestone_amt = get_milestones_data_dict.get("AGS_Z0006_PQB_MILES2")
                            milestone_date = get_milestones_data_dict.get("AGS_Z0006_PQB_MIL2BD")
                            fts_z0006_z0007_insert(milestone_amt=milestone_amt,milestone_date=milestone_date,
                                            service_id=get_service_val,par_service_id=par_service_id)
                        if  get_milestones_data_dict.get("AGS_Z0006_PQB_MIL1BD"):
                            milestone_amt = get_milestones_data_dict.get("AGS_Z0006_PQB_MILES1")
                            milestone_date = get_milestones_data_dict.get("AGS_Z0006_PQB_MIL1BD")
                            fts_z0006_z0007_insert(milestone_amt=milestone_amt,milestone_date=milestone_date,
                                            service_id=get_service_val,par_service_id=par_service_id)
                        if get_milestones_data_dict.get("AGS_Z0007_PQB_MIL1BD"):
                            milestone_amt = get_milestones_data_dict.get("AGS_Z0007_PQB_MILST1")
                            milestone_date = get_milestones_data_dict.get("AGS_Z0007_PQB_MIL1BD")
                            fts_z0006_z0007_insert(milestone_amt=milestone_amt,milestone_date=milestone_date,
                                            service_id=get_service_val)
                        if get_milestones_data_dict.get("AGS_Z0007_PQB_MIL2BD"):
                            milestone_amt = get_milestones_data_dict.get("AGS_Z0007_PQB_MILST2")
                            milestone_date = get_milestones_data_dict.get("AGS_Z0007_PQB_MIL2BD")
                            fts_z0006_z0007_insert(milestone_amt=milestone_amt,milestone_date=milestone_date,
                                            service_id=get_service_val,par_service_id=par_service_id)
                        if  get_milestones_data_dict.get("AGS_Z0007_PQB_MIL3BD"):
                            milestone_amt = get_milestones_data_dict.get("AGS_Z0007_PQB_MILST3")
                            milestone_date = get_milestones_data_dict.get("AGS_Z0007_PQB_MIL3BD")
                            fts_z0006_z0007_insert(milestone_amt=milestone_amt,milestone_date=milestone_date,
                                            service_id=get_service_val,par_service_id=par_service_id)
                    else:
                        diff1 = end_date - start_date
                        avgyear = 365.2425        # pedants definition of a year length with leap years
                        avgmonth = 365.2425/12.0  # even leap years have 12 months
                        years, remainder = divmod(diff1.days, avgyear)
                        years, months = int(years), int(remainder // avgmonth)
                        for index in range(0, years+1):
                            billing_month_end += 1
                            insert_items_billing_plan(total_months=years, 
                                                    billing_date="DATEADD(month, {Month}, '{BillingDate}')".format(
                                                        Month=index, BillingDate=start_date.strftime('%m/%d/%Y')
                                                        ),billing_end_date="DATEADD(month, {Month_add}, '{BillingDate}')".format(
                                                        Month_add=billing_month_end, BillingDate=start_date.strftime('%m/%d/%Y')
                                                        ),amount_column="YEAR_"+str((index) + 1),
                                                        service_id = get_service_val,get_ent_val_type = get_ent_val,get_ent_billing_type_value = get_ent_billing_type_value,billing_day=billing_day,get_billling_data_dict=get_billling_data_dict,datediff=datediff)
                    bill_rec = Sql.GetFirst("SELECT SERVICE_ID from SAQIBP WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID='{}' ".format(contract_quote_rec_id,quote_revision_rec_id,get_service_val))
                    if bill_rec:
                        Sql.RunQuery("UPDATE SAQRIB SET BILLING_STATUS= 'COMPLETE'  WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID='{}' ".format(contract_quote_rec_id,quote_revision_rec_id,get_service_val))
#A055S000P01-3924-billing matrix creation end
if contract_quote_rec_id:
    # INC08627597 - Start - M
    try:
        ApiResponse = ApiResponseFactory.JsonResponse(_insert_billing_matrix())
    except Exception as e:
        ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "400","Message": str(e)}]})
    # INC08627597 - End - M
# =========================================================================================================================================
#   __script_name : CQDELYSCHD.PY
#   __script_description : THIS SCRIPT IS USED TO  update,delete, insert in delivery schedule based on quantiy and delivery schedule change
#   __create_date : 27/01/2022
#   Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================

import Webcom.Configurator.Scripting.Test.TestProduct
from SYDATABASE import SQL
import sys
import System.Net
import datetime
import time
from datetime import timedelta , date

Sql = SQL()

#A055S000P01-14051 start
def insert_deliveryschedule_request(rec_id,QuoteRecordId,rev_rec_id,Service_id):
    Trace.Write('rec_id--'+str(rec_id))
    try:
        if Service_id == "Z0108":
            quotedetails = Sql.GetFirst("SELECT CONTRACT_VALID_FROM,CONTRACT_VALID_TO FROM SAQTMT (NOLOCK) WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(QuoteRecordId,rev_rec_id))
            contract_start_date = quotedetails.CONTRACT_VALID_FROM
            contract_end_date = quotedetails.CONTRACT_VALID_TO
            start_date = datetime.datetime.strptime(UserPersonalizationHelper.ToUserFormat(contract_start_date), '%m/%d/%Y')
            end_date = datetime.datetime.strptime(UserPersonalizationHelper.ToUserFormat(contract_end_date), '%m/%d/%Y')
            diff1 = end_date - start_date
            get_totalweeks,remainder = divmod(diff1.days,7)
            for index in range(0, get_totalweeks):
                delivery_week_date="DATEADD(week, {weeks}, '{DeliveryDate}')".format(weeks=index, DeliveryDate=start_date.strftime('%m/%d/%Y'))
            
                getschedule_details = Sql.RunQuery("INSERT SAQSPD  (QUOTE_REV_PO_PART_DELIVERY_SCHEDULES_RECORD_ID,DELIVERY_SCHED_CAT,PART_DESCRIPTION,PART_RECORD_ID,QUANTITY,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_ID,QTEREVSPT_RECORD_ID,QTEREV_RECORD_ID)  select CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REV_PO_PART_DELIVERY_SCHEDULES_RECORD_ID,null as DELIVERY_SCHED_CAT,{delivery_date} as DELIVERY_SCHED_DATE,PART_DESCRIPTION,PART_RECORD_ID, CUSTOMER_ANNUAL_QUANTITY as QUANTITY,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_ID,QUOTE_SERVICE_PART_RECORD_ID as QTEREVSPT_RECORD_ID,QTEREV_RECORD_ID FROM SAQSPT where SCHEDULE_MODE= 'SCHEDULED' and DELIVERY_MODE = 'OFFSITE' and QUOTE_RECORD_ID = '{contract_rec_id}' AND QTEREV_RECORD_ID = '{qt_rev_id}' and QUOTE_REV_PO_PART_DELIVERY_SCHEDULES_RECORD_ID = '{rec_id}' and CUSTOMER_ANNUAL_QUANTITY >0".format(delivery_date =delivery_week_date,contract_rec_id= QuoteRecordId,qt_rev_id = rev_rec_id,rec_id=rec_id) )
    except:
        pass
    return 'Data'
def delete_deliverydetails(rec_id,QuoteRecordId,rev_rec_id,Service_id):
    Trace.Write('38----')
    return 'data'

Action =Param.Action
rec_id =Param.rec_id
QuoteRecordId = Param.QuoteRecordId
rev_rec_id = Param.rev_rec_id
Service_id = Param.Service_id
if Action == "INSERT":
    insert_deliverydetails = insert_deliveryschedule_request(rec_id,QuoteRecordId,rev_rec_id,Service_id)
elif Action == "DELETE":
    delete_deliverydetails = delete_deliverydetails(rec_id,QuoteRecordId,rev_rec_id,Service_id)

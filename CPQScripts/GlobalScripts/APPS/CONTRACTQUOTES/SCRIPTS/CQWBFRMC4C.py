# =========================================================================================================================================
#   __script_name : CQWBFRMC4C.PY
#   __script_description : TO UPDATE THE OPPORTUNITY STATUS IN  CPQ WHEN THE USER IS CHANGING THE STATUS IN C4C.
#   __primary_author__ : GAYATHRI AMARESAN
#   __create_date :08-12-2021
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================

from SYDATABASE import SQL
Sql = SQL()
import CQCPQC4CWB
import sys

if 'Param' in globals():
    Log.Info("CQWBFRMC4C called......."+str(Param)+"paramsss---"+str(hasattr(Param, 'CPQ_Columns')))	
    if hasattr(Param, 'CPQ_Columns'):
        Log.Info("CQWBFRMC4C called.......inside if")    
        
        opportunity_data = [str(param_result.Value) for param_result in Param.CPQ_Columns]
        opportunity_id = opportunity_data[0]
        opportunity_status = str(opportunity_data[-1]).upper()
        
        Log.Info("opportunity_id--"+str(opportunity_id))
        Log.Info("opportunity_status--"+str(opportunity_status))
        
        ##To Fetch the Picklist value based on the value from C4C...
        opportunity_status_dictionary = {"LOST":"OPPORTUNITY LOST", "CANCELLED":"OPPORTUNITY CANCELLED"}
        
        ##To update the revision status in cpq based on the status from c4c value....
        Log.Info("UPDATE SAQTRV SET REVISION_STATUS = '{}' FROM SAQTRV JOIN SAOPQT ON SAQTRV.QUOTE_RECORD_ID = SAOPQT.QUOTE_RECORD_ID  WHERE OPPORTUNITY_ID = '{}'".format(opportunity_status_dictionary.get(str(opportunity_status)),opportunity_id))
        Sql.RunQuery("UPDATE SAQTRV SET REVISION_STATUS = '{}' FROM SAQTRV JOIN SAOPQT ON SAQTRV.QUOTE_RECORD_ID = SAOPQT.QUOTE_RECORD_ID  WHERE OPPORTUNITY_ID = '{}'".format(opportunity_status_dictionary.get(str(opportunity_status)),opportunity_id))
        Log.Info("SELECT QUOTE_RECORD_ID,QTEREV_RECORD_ID FROM SAQTRV JOIN SAOPQT ON SAQTRV.QUOTE_RECORD_ID = SAOPQT.QUOTE_RECORD_ID  WHERE SAOPQT.OPPORTUNITY_ID = '{}' AND SAQTRV.ACTIVE = 1".format(opportunity_id))
        quote_header_object = Sql.GetFirst("SELECT QUOTE_RECORD_ID,QTEREV_RECORD_ID FROM SAQTRV JOIN SAOPQT ON SAQTRV.QUOTE_RECORD_ID = SAOPQT.QUOTE_RECORD_ID  WHERE SAOPQT.OPPORTUNITY_ID = '{}' AND SAQTRV.ACTIVE = 1".format(opportunity_id))
        if quote_header_object is not None:
            CQCPQC4CWB.writeback_to_c4c("quote_header",quote_header_object.QUOTE_RECORD_ID,quote_header_object.QTEREV_RECORD_ID)
    else:
        Log.Info("else condition")
            
            
            
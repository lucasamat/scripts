# =========================================================================================================================================
#   __script_name : CQWBFRMC4C.PY
#   __script_description : TO UPDATE THE OPPORTUNITY STATUS IN CPQ WHEN THE USER IS CHANGING THE STATUS IN C4C.
#   __primary_author__ : GAYATHRI AMARESAN
#   __create_date :08-12-2021
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================

from SYDATABASE import SQL
import CQCPQC4CWB
import sys

Sql = SQL()

if 'Param' in globals():    
    if hasattr(Param, 'CPQ_Columns'):       
        opportunity_data = [str(param_result.Value) for param_result in Param.CPQ_Columns]
        opportunity_id = opportunity_data[0]
        opportunity_status = str(opportunity_data[-1]).upper()        
        ##To Fetch the Picklist value based on the value from C4C...
        opportunity_status_dictionary = {"LOST":"OPPORTUNITY LOST", "CANCELLED":"OPPORTUNITY CANCELLED","WON" : "OPPROTUNITY WON"}        
        ##To update the revision status in cpq based on the status from c4c value....        
        #Sql.RunQuery("UPDATE SAQTRV SET REVISION_STATUS = '{}' FROM SAQTRV JOIN SAOPQT ON SAQTRV.QUOTE_RECORD_ID = SAOPQT.QUOTE_RECORD_ID  WHERE OPPORTUNITY_ID = '{}'".format(opportunity_status_dictionary.get(str(opportunity_status)),opportunity_id))
        Sql.RunQuery("UPDATE SAOPQT SET OPPORTUNITY_STATUS = '{}' FROM SAOPQT WHERE OPPORTUNITY_ID = '{}'".format(opportunity_status_dictionary.get(str(opportunity_status)),opportunity_id))
        quote_header_object = Sql.GetFirst("SELECT SAQTRV.QUOTE_RECORD_ID,SAQTRV.QTEREV_RECORD_ID FROM SAQTRV JOIN SAOPQT ON SAQTRV.QUOTE_RECORD_ID = SAOPQT.QUOTE_RECORD_ID  WHERE SAOPQT.OPPORTUNITY_ID = '{}' AND SAQTRV.ACTIVE = 1".format(opportunity_id))
        # if quote_header_object is not None:
        #     CQCPQC4CWB.writeback_to_c4c("quote_header",quote_header_object.QUOTE_RECORD_ID,quote_header_object.QTEREV_RECORD_ID)
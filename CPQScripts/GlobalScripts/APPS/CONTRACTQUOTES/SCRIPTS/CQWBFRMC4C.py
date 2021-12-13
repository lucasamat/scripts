# =========================================================================================================================================
#   __script_name : CQWBFRMC4C.PY
#   __script_description : TO UPDATE THE OPPORTUNITY STATUS IN  CPQ WHEN THE USER IS CHANGING THE STATUS IN C4C.
#   __primary_author__ : GAYATHRI AMARESAN
#   __create_date :08-12-2021
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================

from SYDATABASE import SQL
Sql = SQL()
import sys

if 'Param' in globals():
    Log.Info("CQWBFRMC4C called.......")	
    if hasattr(Param, "CPQ_Columns"):
        Log.Info("CQWBFRMC4C called.......inside if")
        for values in Param.CPQ_Columns:
            Log.Info("CQWBFRMC4C called....... inside for")
            Key = str(values.Key)
            Log.Info("CQWBFRMC4C called......."+str(values.Key))
            Log.Info("CQWBFRMC4C called......."+str(values.Value))
            if str(Key).upper() == "OPPORTUNITY_ID":
                opportunity_id = str(values.Value)
            if str(Key).upper() == "OPPORTUNITY_STATUS":
                opportunity_status = str(values.Value).upper()
            ##To Fetch the Picklist value based on the value from C4C...
            opportunity_status_dictionary = {"LOST":"OPPORTUNITY LOST", "CANCELLED":"OPPORTUNITY CANCELLED"}
            
            ##To update the revision status in cpq based on the status from c4c value....
            Sql.RunQuery("UPDATE SAQTRV SET REVISION_STATUS = '{}' FROM SAQTRV JOIN SAOPQT ON SAQTRV.QUOTE_RECORD_ID = SAOPQT.QUOTE_RECORD_ID  WHERE OPPORTUNITY_ID = '{}'".format(opportunity_status_dictionary.get(str(opportunity_status)),opportunity_id))
            
            
            
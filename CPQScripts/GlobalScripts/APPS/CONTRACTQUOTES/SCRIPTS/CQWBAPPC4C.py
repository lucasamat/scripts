# =========================================================================================================================================
#   __script_name : CQWBAPPC4C.PY
#   __script_description : TO UPDATE THE OPPORTUNITY STATUS IN  CPQ WHEN THE USER IS CHANGING THE STATUS IN C4C.
#   __primary_author__ : WASIM
#   __create_date :25-01-2022
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================

from SYDATABASE import SQL
Sql = SQL()
import CQCPQC4CWB
import sys

if 'Param' in globals():
    Log.Info("CQWBAPPC4C called......."+str(Param)+"paramsss---"+str(hasattr(Param, 'CPQ_Columns')))	
    if hasattr(Param, 'CPQ_Columns'):
        Log.Info("CQWBAPPC4C called.......inside if")    
        
        approval_object_data = [str(param_result.Value) for param_result in Param.CPQ_Columns]
        object_id = approval_object_data[0]
        quote_id = str(approval_object_data[-1]).upper()
        approver_id = str(approval_object_data[-2]).upper()
        Log.Info("object_id--"+str(object_id))
        Log.Info("quote_id--"+str(quote_id))
        Log.Info("approver_id--"+str(approver_id))
        
    else:
        Log.Info("else condition")
            
            
            
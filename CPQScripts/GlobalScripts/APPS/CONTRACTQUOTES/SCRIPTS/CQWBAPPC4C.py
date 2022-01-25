# =========================================================================================================================================
#   __script_name : CQWBAPPC4C.PY
#   __script_description : TO UPDATE THE OBJECT ID IN CPQ WHEN THE APPROVER IS CREATED IN C4C.
#   __primary_author__ : WASIM.ABDUL
#   __create_date : 25-01-2022
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
        Log.Info("approval_object_data--"+str(approval_object_data))
        obj_id = approval_object_data[0]
        quote_id = str(approval_object_data[1]).upper()
        approver_id='USR-'+str(approval_object_data[2]).upper()
        approver_step_id = str(approval_object_data[3]).upper()
        Log.Info("object_id--"+str(obj_id))
        Log.Info("quote_id--"+str(quote_id))
        Log.Info("approver_id--"+str(approver_id))
        Log.Info("approver_approver_step_idid--"+str(approver_step_id)) 
        update_obj_id="""UPDATE ACAPTX SET OWNER_ID = '{obj_id}' WHERE APRTRXOBJ_ID = '{quote_id}' AND APRCHNSTP_APPROVER_ID ='{approver_id}' AND APRCHNSTP_ID ='{approver_step_id}'""".format(obj_id=obj_id,quote_id =quote_id,approver_id = approver_id,approver_step_id =approver_step_id)
        Sql.RunQuery(update_obj_id) 
    else:
        Log.Info("else condition")
            
            
            
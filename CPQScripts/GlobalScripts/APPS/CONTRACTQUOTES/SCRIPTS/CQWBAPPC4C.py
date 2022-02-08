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
        
        #approval_object_data = [str(param_result.Value) for param_result in Param.CPQ_Columns]
        for param_result in Param.CPQ_Columns:
            approval_object_data = [ str(p_result.Value) for p_result in param_result ]
            Log.Info("approval_object_data--"+str(approval_object_data))

            obj_id = approval_object_data[0]
            approver_id = str(approval_object_data[1]).upper()
            quote_id=str(approval_object_data[2]).upper()
            #approver_step_id = str(approval_object_data[3]).upper()
            Log.Info("object_id--"+str(obj_id))
            Log.Info("quote_id--"+str(quote_id))
            Log.Info("approver_id--"+str(approver_id))
            emp_id ="8000"
            if emp_id in approver_id:
                get_approver_emp_id = Sql.GetFirst("SELECT *FROM SAEMPL(NOLOCK) WHERE C4C_EMPLOYEE_ID = '{approver_id}'".format(approver_id = approver_id))
                if get_approver_emp_id:
                    emp_approver_id = 'USR-'+str(get_approver_emp_id.EMPLOYEE_ID)
            else:        
                emp_approver_id = 'USR-'+str(approver_id)
            #Log.Info("approver_approver_step_idid--"+str(approver_step_id)) 
            get_approver_id = Sql.GetFirst("SELECT * FROM ACAPTX(NOLOCK) WHERE APRCHNSTP_APPROVER_ID = '{emp_approver_id}' AND OWNER_ID = '' AND APRTRXOBJ_ID = '{quote_id}' ".format(emp_approver_id = emp_approver_id,quote_id =quote_id))
            # Log.Info("get_approver_id"+str(get_approver_id.EMPLOYEE_ID))
            # emp_approver_id = 'USR-'+str(get_approver_id.EMPLOYEE_ID)
            transaction_id = str(get_approver_id.APPROVAL_TRANSACTION_RECORD_ID)
            if get_approver_id:
                update_obj_id="""UPDATE ACAPTX SET OWNER_ID = '{obj_id}' WHERE APRTRXOBJ_ID = '{quote_id}' AND APRCHNSTP_APPROVER_ID ='{emp_approver_id}' AND APPROVAL_TRANSACTION_RECORD_ID ='{transaction_id}'""".format(obj_id=obj_id,quote_id =quote_id,emp_approver_id = emp_approver_id,transaction_id =transaction_id)
                Sql.RunQuery(update_obj_id) 
    else:
        Log.Info("else condition")
            
            
            
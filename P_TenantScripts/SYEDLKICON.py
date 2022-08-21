# =========================================================================================================================================
#   __script_name : SYEDLKICON.PY
#   __script_description : THIS SCRIPT IS USED TO DISPLAY THE EDIT OR LOCK ICONS IN ALL FIELDS THROUGHOUT THE SYSTEM.
#   __primary_author__ : JOE EBENEZER
#   __create_date :
#   Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
from SYDATABASE import SQL
import Webcom.Configurator.Scripting.Test.TestProduct
Sql = SQL()


def EDIT_LOCK_ICON():

    curTab = Param.curTab
    currentModuleTab = Param.currentModuleTab
    tab_obj_name = ""
    qstn_list_values = []

    get_obj_name_d = Sql.GetFirst(
        "Select s.CONTAINER_NAME from SYOBJS (nolock) s inner join SYTABS (nolock) t on t.SAPCPQ_ALTTAB_NAME = '"
        + str(curTab)
        + "' inner join SYPAGE p on p.TAB_RECORD_ID = t.RECORD_ID  inner join SYSECT (nolock) m on p.RECORD_ID = m.PAGE_RECORD_ID where s.NAME='Tab list' and s.OBJ_REC_ID = m.PRIMARY_OBJECT_RECORD_ID and m.SECTION_NAME = 'BASIC INFORMATION'"
    )

    if get_obj_name_d is not None:
        tab_obj_name = get_obj_name_d.CONTAINER_NAME

        qstn_list_obj = Sql.GetList(
            "select distinct d.OBJECT_NAME,d.FIELD_LABEL,d.PERMISSION,LOWER(s.CAN_EDIT) AS CAN_EDIT,d.DATA_TYPE from  SYOBJD d (NOLOCK) inner join SYOBJS s (NOLOCK) on d.PARENT_OBJECT_RECORD_ID=s.OBJ_REC_ID where d.OBJECT_NAME='"
            + str(tab_obj_name)
            + "' and s.NAME='Tab list'"
        )
        CAN_EDIT = False
        if qstn_list_obj is not None:
            for qstn_list in qstn_list_obj:
                if str(qstn_list.CAN_EDIT) == "true" and str(qstn_list.DATA_TYPE) != "AUTO NUMBER":
                    #Trace.Write("111111111122222222222233333333333344444444444445555555555" + str(qstn_list.DATA_TYPE))
                    visible = ""
                    if str(qstn_list.PERMISSION) == "" or str(qstn_list.PERMISSION).upper() == "READ ONLY":
                        visible = "READ ONLY"  ####visible='readonly'
                    else:
                        visible = qstn_list.PERMISSION
                    qstn_list_values.append(qstn_list.OBJECT_NAME + "|" + qstn_list.FIELD_LABEL + "|" + visible)
                    
                    CAN_EDIT = True
                else:
                    visible = qstn_list.PERMISSION
                    qstn_list_values.append(
                        # Modified by wasim For A043S001P01-4814 -Start
                        qstn_list.OBJECT_NAME
                        + "|"
                        + qstn_list.FIELD_LABEL
                        + "|"
                        + visible
                        # Modified by wasim For A043S001P01-4814 -End
                    )
        if CAN_EDIT == True:
            # Log.Info("CAN_EDIT is true--->")
            qstn_list_lkp_obj = Sql.GetList(
                "select distinct d.OBJECT_NAME,d.FIELD_LABEL,s.PERMISSION,d.DATA_TYPE from  SYOBJD d (NOLOCK) inner join  SYOBJD s (NOLOCK) on d.PARENT_OBJECT_RECORD_ID=s.PARENT_OBJECT_RECORD_ID where d.API_NAME=s.LOOKUP_API_NAME AND d.OBJECT_NAME='"
                + str(tab_obj_name)
                + "'"
            )
            for qstn_lkp_list in qstn_list_lkp_obj:
                visible = ""

                ####7745 starts...
                TestProduct = Webcom.Configurator.Scripting.Test.TestProduct()
                current_tab = str(TestProduct.CurrentTab)

                if str(qstn_lkp_list.PERMISSION) == "" or str(qstn_lkp_list.PERMISSION).upper() == "READ ONLY":
                    visible = "READ ONLY"  #'readonly'

                else:
                    Lock_State = ""
                    if Lock_State != "" and Lock_State == "1" and str(qstn_lkp_list.FIELD_LABEL) != "Locked":
                        visible = "READ ONLY"
                    else:
                        visible = qstn_lkp_list.PERMISSION

                qstn_list_values.append(qstn_lkp_list.OBJECT_NAME + "|" + qstn_lkp_list.FIELD_LABEL + "|" + visible)
                
        Trace.Write("qstn_list_values ====================> " + str(qstn_list_values))
    return qstn_list_values


ApiResponse = ApiResponseFactory.JsonResponse(EDIT_LOCK_ICON())
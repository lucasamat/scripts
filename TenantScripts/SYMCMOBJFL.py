# =========================================================================================================================================
#   __script_name : SYMCMOBJFL.PY
#   __script_description : THIS SCRIPT IS USED TO GET ALL THE FIELD LABELS OF THE GIVEN OBJECT IN THE SYSTEM ADMIN APP
#   __primary_author__ : LEO JOSEPH
#   __create_date : 8/31/2020
# ==========================================================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct
from SYDATABASE import SQL

Sql = SQL()


def custObj():
    TestProduct = Webcom.Configurator.Scripting.Test.TestProduct()
    CurrentTabName = TestProduct.CurrentTab
    
    Final_List = []
    Obj_List = []
    Avl_List = []
    Avl_Lkup_List = {}

    sql_Tab_obj = Sql.GetFirst("select RECORD_ID from SYTABS where TAB_LABEL = '" + str(CurrentTabName) + "'")

    sql_Sec_obj = Sql.GetFirst(
        "Select SE.PRIMARY_OBJECT_RECORD_ID from SYSECT (nolock) SE inner join SYPAGE(nolock)PG on SE.PAGE_RECORD_ID = PG.RECORD_ID and SE.PAGE_NAME = PG.PAGE_NAME where PG.TAB_RECORD_ID = '"
        + str(sql_Tab_obj.RECORD_ID)
        + "'"
    )

    sql_objd_obj = Sql.GetList(
        "select OBJECT_NAME,LOOKUP_OBJECT from  SYOBJD where PARENT_OBJECT_RECORD_ID = '"
        + str(sql_Sec_obj.PRIMARY_OBJECT_RECORD_ID)
        + "' and DATA_TYPE = 'LOOKUP'"
    )
    for Obj in sql_objd_obj:
        if Obj.OBJECT_NAME not in Obj_List:
            Obj_List.append(Obj.OBJECT_NAME)
        if Obj.LOOKUP_OBJECT not in Obj_List:
            Obj_List.append(Obj.LOOKUP_OBJECT)

    sql_Aval_obj = Sql.GetList(
        "select FIELD_LABEL,DATA_TYPE,LOOKUP_OBJECT from  SYOBJD where PARENT_OBJECT_RECORD_ID = '"
        + str(sql_Sec_obj.PRIMARY_OBJECT_RECORD_ID)
        + "'"
    )

    for Bun in sql_Aval_obj:
        Avl_List.append(Bun.FIELD_LABEL)
        if Bun.DATA_TYPE == "LOOKUP":

            dit_val = []

            sql_lkupAvl_obj = Sql.GetList(
                "select FIELD_LABEL from  SYOBJD where OBJECT_NAME = '" + str(Bun.LOOKUP_OBJECT) + "'"
            )

            for pur in sql_lkupAvl_obj:
                dit_val.append(pur.FIELD_LABEL)

            if len(dit_val) > 0:
                Avl_Lkup_List[Bun.FIELD_LABEL] = dit_val

    Final_List = [Obj_List, Avl_List, Avl_Lkup_List]    

    return Final_List


ApiResponse = ApiResponseFactory.JsonResponse(custObj())
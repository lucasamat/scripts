# =========================================================================================================================================
#   __script_name : SYLDOBJPUP.PY
#   __script_description : THIS SCRIPT IS USED TO LOAD THE DATA IN POPUP IN THE OBJECT TAB IN SYSTEM ADMIN
#   __primary_author__ : BAJI BABA
#   __create_date :
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
# MMOBJPOPUP_API
from SYDATABASE import SQL

Sql = SQL()


def MMOBJ_API_POUPUP():

    Section_obj1 = Sql.GetList(
        "SELECT OBJECT_NAME, API_NAME FROM  SYOBJD where OBJECT_NAME = '"
        + Product.Attr("MM_OBJ_FI_LOOKUP_OBJECT").GetValue()
        + "'"
    )
    sec_list = []
    for ins in Section_obj1:
        sec_dict = {}
        ids = str(ins.API_NAME)
        Log.Info("IDS" + str(ids))
        sec_dict["ids"] = ids
        sec_dict["API_NAME"] = ins.API_NAME
        sec_list.append(sec_dict)
    
    return sec_list


FIELD = Param.FIELD
RecID = Param.RecID

if FIELD == "Section Record ID":
    ApiResponse = ApiResponseFactory.JsonResponse(MMOBJ_API_POUPUP())
elif FIELD == "Section Record ID Onchange":
    RecordID = RecID.split("|")[0]
    RecordName = RecID.split("|")[1]
    RecordID_No = RecordName
    Log.Info("RecordID---------->" + str(RecordName))
    Log.Info("RecordID_No-------->" + str(RecordID_No))
    Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_API_NAME").AssignValue(str(RecordID))
    

    ApiResponse = ApiResponseFactory.JsonResponse("")

# =========================================================================================================================================
#   __script_name : SYMCMOBJPO.PY
#   __script_description : THIS SCRIPT IS USED TO SELECT THE LOOKUP OBJECT AND LOOKUP FIELD FROM OBJECTS POPUP IN SYSTEM ADMIN
#   __primary_author__ : LEO JOSEPH
#   __create_date :
#   Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct
from SYDATABASE import SQL

Sql = SQL()


def MMOBJPOPUPRECID():
    Section_obj = Sql.GetList("SELECT OBJECT_NAME, RECORD_ID FROM SYOBJH")
    sec_list = []
    for ins in Section_obj:
        sec_dict = {}
        ids = str(ins.RECORD_ID) + "|" + str(ins.OBJECT_NAME)
        sec_dict["ids"] = ids
        sec_dict["SECTION_NAME"] = ins.OBJECT_NAME
        sec_dict["RECORD_ID"] = ins.RECORD_ID
        sec_list.append(sec_dict)
    
    return sec_list


def MMOBJ_API_POUPUP():
    
    MM_OBJ = Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_OBJECT").GetValue()
    Section_obj1 = Sql.GetList("SELECT OBJECT_NAME, API_NAME FROM  SYOBJD where OBJECT_NAME = '" + MM_OBJ + "'")
    sec_list1 = []
    for ins in Section_obj1:
        sec_dict1 = {}
        ids = str(ins.API_NAME) + "|" + str(ins.OBJECT_NAME)
        sec_dict1["ids"] = ids
        sec_dict1["API_NAME"] = ins.API_NAME
        sec_dict1["OBJECT_NAME"] = ins.OBJECT_NAME
        sec_list1.append(sec_dict1)
    
    return sec_list1


try:
    FIELD = Param.FIELD
except:
    FIELD = ""
try:
    RecID = Param.RecID
except:
    RecID = ""
if FIELD == "ObjectRecord ID":

    ApiResponse = ApiResponseFactory.JsonResponse(MMOBJPOPUPRECID())
elif FIELD == "ObjectRecord ID Onchange":

    RecordID = RecID.split("|")[0]
    RecordName = RecID.split("|")[1]
    RecordID_No = RecordName
    Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_OBJECT").AssignValue(str(RecordID_No))
    lookup_obj_var = RecordName
    if str(lookup_obj_var) != "None" and str(lookup_obj_var) != "":
        MM_OBJ_PL_LABEL = str(Product.Attributes.GetByName("MM_OBJ_PL_LABEL").GetValue() or "")
        Product.Attributes.GetByName("MM_OBJ_FI_REL_LIST").AssignValue(str(MM_OBJ_PL_LABEL))
        MM_OBJ_FI_LOOKUP_OBJECT = str(Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_OBJECT").GetValue() or "")
        Sql_obj = Sql.GetList(
            "SELECT OBJECT_NAME, API_NAME FROM  SYOBJD where OBJECT_NAME = '"
            + MM_OBJ_FI_LOOKUP_OBJECT
            + "' and DATA_TYPE = 'AUTO NUMBER'"
        )
        check_obj = 0
        Lookup_Api_Names = ""
        for pur in Sql_obj:
            check_obj = 1
        if check_obj == 1:
            for Obj in Sql_obj:
                Lookup_Api_Names = str(Obj.API_NAME)
        Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_API_NAME").AssignValue(str(Lookup_Api_Names))
elif FIELD == "Api Record Name":
    ApiResponse = ApiResponseFactory.JsonResponse(MMOBJ_API_POUPUP())
elif FIELD == "Api Record ID Onchange":
    RecordID = RecID.split("|")[1]
    RecordName = RecID.split("|")[0]
    RecordID_No1 = RecordName
    Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_API_NAME").AssignValue(str(RecordID_No1))
    

    ApiResponse = ApiResponseFactory.JsonResponse("")
# =========================================================================================================================================
#   __script_name : SYCTLKANVL.PY
#   __script_description : THIS SCRIPT IS USED TO OPEN A POPUP FOR VIEW/EDIT RECORDS IN RELATED LIST FOR ALL THE TABS DYNAMICALLY.
#   __primary_author__ : JOE EBENEZER
#   __create_date :
# ==========================================================================================================================================
from SYDATABASE import SQL
import Webcom.Configurator.Scripting.Test.TestProduct
Sql = SQL()

def ASSIGNVALUE(LABLE, VALUE, TABLEID, RECORDID, RECORDFEILD, IDVALUE, LOOKUPOBJ, LOOKUPAPI):
    NEWVAL = str(IDVALUE)
    RECID = TABLEID
    RECID = RECID.split("_")
    table = RECID[2] + "-" + RECID[3]

    Question_obj = Sql.GetFirst("SELECT OBJECT_NAME, LABEL FROM SYOBJH WHERE RECORD_ID='" + str(table) + "'")
    Obj_name = Question_obj.OBJECT_NAME
    
    attrval_obj = Sql.GetFirst(
        "SELECT API_NAME FROM  SYOBJD WHERE OBJECT_NAME='"
        + str(Obj_name)
        + "' AND LOOKUP_OBJECT='"
        + str(LOOKUPOBJ)
        + "' and LOOKUP_API_NAME='"
        + str(LOOKUPAPI)
        + "'"
    )
    api_name = attrval_obj.API_NAME.strip()
    new_value_dict = {}
    if IDVALUE != "":
        IDVALUE = IDVALUE.split("|")
        result1 = ScriptExecutor.ExecuteGlobal(
            "SYPARCEFMA", {"Object": str(Obj_name), "API_Name": api_name, "API_Value": IDVALUE[0]},
        )
       
        new_value_dict = {API_Names["API_NAME"]: API_Names["FORMULA_RESULT"] for API_Names in result1}
    result = ScriptExecutor.ExecuteGlobal(
        "SYLDPPRVAE",
        {
            "OPERATION": "EDIT",
            "LABLE": LABLE,
            "VALUE": VALUE,
            "TABLEID": TABLEID,
            "RETURN": "1",
            "RECORDID": RECORDID,
            "RECORDFEILD": RECORDFEILD,
            "NEWVAL": NEWVAL,
        },
    )
    
    return result[0], new_value_dict, api_name, Obj_name


IDVALUE = Param.IDVALUE

LABLE = Param.LABLE
VALUE = Param.VALUE
TABLEID = Param.TABLEID
OPERATION = Param.OPERATION
RETURN = Param.RETURN
RECORDID = Param.RECORDID
RECORDFEILD = Param.RECORDFEILD
LOOKUPOBJ = Param.LOOKUPOBJ
LOOKUPAPI = Param.LOOKUPAPI
LOOKUPOBJ = LOOKUPOBJ.split("_")[1]
ApiResponse = ApiResponseFactory.JsonResponse(
    ASSIGNVALUE(LABLE, VALUE, TABLEID, RECORDID, RECORDFEILD, IDVALUE, LOOKUPOBJ, LOOKUPAPI)
)
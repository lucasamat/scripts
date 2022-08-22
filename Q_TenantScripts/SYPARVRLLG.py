# =========================================================================================================================================
#   __script_name : SYPARVRLLG.PY
#   __script_description : THIS SCRIPT IS USED TO GET THE VALUE FOR ALL THE VARIABLE LOGIC FIELDS IN  SYOBJD
#   __primary_author__ : JOE EBENEZER
#   __create_date :
#   Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
# import Webcom
# import Webcom.Configurator.Scripting.Test.TestProduct
import re
import Webcom.Configurator.Scripting.Test.TestProduct
from SYDATABASE import SQL

Sql = SQL()


def ParseGlobalVariable(CTXLogicText, Obj_Name):
    GLV_logic = str(CTXLogicText)
    GLV_attr = re.findall(r"Value\((.*?)\)\s\*>", GLV_logic)
    for inv in GLV_attr:
        SYOBJD_OBJ_REC = Sql.GetList(
            "select * FROM  SYOBJD (nolock) where OBJECT_NAME = '" + str(Obj_Name) + "' and API_NAME='" + str(inv) + "'"
        )
        for rec in SYOBJD_OBJ_REC:
            if rec.DATA_TYPE == "LOOKUP":
                SYOBJD_OBJ_REC2 = Sql.GetFirst(
                    "select * FROM  SYOBJD (nolock) where OBJECT_NAME = '"
                    + str(Obj_Name)
                    + "' and FORMULA_LOGIC LIKE '%"
                    + str(rec.LOOKUP_API_NAME)
                    + "%'"
                )
                if SYOBJD_OBJ_REC2 is not None:
                    MMQST_OBJ_REC = Sql.GetList(
                        "select * FROM SYSEFL (nolock) where API_NAME = '"
                        + str(Obj_Name)
                        + "' and API_NAME='"
                        + str(SYOBJD_OBJ_REC2.API_NAME)
                        + "'"
                    )
                    if MMQST_OBJ_REC is not None:
                        for rec2 in MMQST_OBJ_REC:
                            ATTR_NAME = "QSTN_" + str(rec2.RECORD_ID).replace("-", "_")
                            if Product.Attributes.GetByName(ATTR_NAME) is not None:
                                newvalue = str(Product.Attributes.GetByName(ATTR_NAME).GetValue())
                                GLV_logic = GLV_logic.replace("<* Value(" + str(inv) + ") *>", str(newvalue))
            else:
                MMQST_OBJ_REC = Sql.GetList(
                    "select * FROM SYSEFL (nolock) where API_NAME = '"
                    + str(Obj_Name)
                    + "' and API_NAME='"
                    + str(rec.API_NAME)
                    + "'"
                )
                if MMQST_OBJ_REC is not None:
                    for rec2 in MMQST_OBJ_REC:
                        ATTR_NAME = "QSTN_" + str(rec2.RECORD_ID).replace("-", "_")
                        if Product.Attributes.GetByName(ATTR_NAME) is not None:
                            newvalue = str(Product.Attributes.GetByName(ATTR_NAME).GetValue())
                            GLV_logic = GLV_logic.replace("<* Value(" + str(ATTR_NAME) + ") *>", str(newvalue))
    return GLV_logic

CTXLogic = Param.CTXLogic
Obj_Name = Param.Obj_Name
GLV_Logic = ParseGlobalVariable(CTXLogic, Obj_Name)
Result = Product.ParseString(str(GLV_Logic))
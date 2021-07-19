# =========================================================================================================================================
#   __script_name : SYMCMOBJER.PY
#   __script_description : THIS SCRIPT IS USED TO DO THE VALIDATIONS WHEN ADD/EDIT OBJECTS UNDER SYSTEM ADMIN APP
#   __primary_author__ : LEO JOSEPH
#   __create_date : 8/31/2020
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
from SYDATABASE import SQL

Sql = SQL()

MM_OBJ_LABEL = Product.Attributes.GetByName("MM_OBJ_LABEL").GetValue() or ""
MM_OBJ_PL_LABEL = Product.Attributes.GetByName("MM_OBJ_PL_LABEL").GetValue() or ""
MM_OBJ_TBL_NAME = Product.Attributes.GetByName("MM_OBJ_TBL_NAME").GetValue() or ""
MM_OBJ_REC_NAME = Product.Attributes.GetByName("MM_OBJ_REC_NAME").GetValue() or ""
MM_OBJ_DATA_TYPE = Product.Attributes.GetByName("MM_OBJ_DATA_TYPE").GetValue() or ""
MM_OBJ_API_NAME1 = Product.Attributes.GetByName("MM_OBJ_API_NAME").GetValue() or ""
MM_OBJ_ACTION = Product.Attributes.GetByName("MM_OBJ_ACTION").GetValue() or ""
Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_OBJECT").Access = AttributeAccess.ReadOnly

MM_OBJ_PARENT_REC_ID = Product.Attributes.GetByName("MM_OBJ_REC_ID").GetValue() or ""
MM_OBJ_OBJECT_NAME = Product.Attributes.GetByName("MM_OBJ_TBL_NAME").GetValue() or ""
Obj_Key = Product.Attributes.GetByName("MM_OBJ_FI_KEY").GetValue() or ""

if MM_OBJ_OBJECT_NAME != "":

    Var_Recno = MM_OBJ_OBJECT_NAME + "-{00000}"

    Product.Attributes.GetByName("MM_OBJ_DIS_FORMAT").AssignValue(str(Var_Recno))


if MM_OBJ_ACTION == "ADDNEW":
    Product.Attributes.GetByName("MM_OBJ_BTN_BTL").Allowed = True
    Product.Attributes.GetByName("MM_OBJ_BTN_BTL").HintFormula = "CANCEL"
    Product.Attributes.GetByName("MM_OBJ_BTN_SAVE").Allowed = True
    Product.Attributes.GetByName("MM_OBJ_BTN_DELETE").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_BTN_EDIT").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_BTN_CANCEL").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_REC_ID").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_TAB_ALERT").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_BTN_REFRESH").Allowed = False

    Product.Attributes.GetByName("MM_OBJ_SEC_REL_LIST").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_SUBSEC_SEC_REL_LIST").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_CTR_SEC_REL_LST").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_CTR_SEARCH_LIST").Allowed = False

    
    Product.Attributes.GetByName("MM_OBJ_FIELD_REL").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_CTR_OBJ_DATA").Allowed = False

    Product.Attributes.GetByName("MM_OBJ_LABEL_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_PL_LABEL_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_TBL_NAME_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_REC_NAME_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_DATA_TYPE_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_TAB_ALERT").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_API_NAME_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_KEY_FIELD_LABEL_ERR").Allowed = False
if MM_OBJ_ACTION == "VIEWEDIT":
    Product.Attributes.GetByName("MM_OBJ_BTN_CANCEL").Allowed = True
    Product.Attributes.GetByName("MM_OBJ_BTN_SAVE").Allowed = True
    Product.Attributes.GetByName("MM_OBJ_BTN_BTL").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_BTN_DELETE").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_BTN_EDIT").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_TAB_ALERT").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_LABEL_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_PL_LABEL_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_TBL_NAME_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_REC_NAME_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_DATA_TYPE_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_API_NAME_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_TAB_ALERT").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_SEC_REL_LIST").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_SUBSEC_SEC_REL_LIST").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_CTR_SEC_REL_LST").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_BTN_REFRESH").Allowed = False

    Product.Attributes.GetByName("MM_OBJ_FIELD_REL").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_CTR_OBJ_DATA").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_CTR_SEARCH_LIST").Allowed = False


if MM_OBJ_ACTION == "EDIT":
    Product.Attributes.GetByName("MM_OBJ_BTN_SAVE").Allowed = True
    Product.Attributes.GetByName("MM_OBJ_BTN_EDIT").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_BTN_CANCEL").Allowed = True
    Product.Attributes.GetByName("MM_OBJ_BTN_BTL").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_BTN_DELETE").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_TAB_ALERT").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_LABEL_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_PL_LABEL_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_TBL_NAME_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_REC_NAME_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_DATA_TYPE_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_API_NAME_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_TAB_ALERT").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_SEC_REL_LIST").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_SUBSEC_SEC_REL_LIST").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_CTR_SEC_REL_LST").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_BTN_REFRESH").Allowed = False

    Product.Attributes.GetByName("MM_OBJ_FIELD_REL").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_CTR_OBJ_DATA").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_CTR_SEARCH_LIST").Allowed = False

if MM_OBJ_ACTION == "VIEW":
    Product.Attributes.GetByName("MM_OBJ_BTN_CANCEL").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_BTN_SAVE").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_BTN_BTL").Allowed = True
    Product.Attributes.GetByName("MM_OBJ_BTN_BTL").HintFormula = "BACK TO LIST"
    Product.Attributes.GetByName("MM_OBJ_BTN_DELETE").Allowed = True
    Product.Attributes.GetByName("MM_OBJ_BTN_EDIT").Allowed = True
    Product.Attributes.GetByName("MM_OBJ_TAB_ALERT").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_LABEL_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_PL_LABEL_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_TBL_NAME_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_REC_NAME_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_DATA_TYPE_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_API_NAME_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_TAB_ALERT").Allowed = False

# POPUP CONTROL
data_typ = str(Product.Attributes.GetByName("MM_OBJ_FI_DATA_TYPE").GetValue() or "")
Log.Info("12345container event script for object555555555555555" + str(data_typ))

# POPUP COMMON ATTRIBUTES
Product.Attributes.GetByName("MM_OBJ_FI_DATA_TYPE").Allowed = True
Product.Attributes.GetByName("MM_OBJ_FI_FIELD_LABEL").Allowed = True
Product.Attributes.GetByName("MM_OBJ_FI_API_NAME").Allowed = True
Product.Attributes.GetByName("MM_OBJ_FI_REQ").Allowed = True
Product.Attributes.GetByName("MM_OBJ_FI_PERMISSIONS").Allowed = True
Product.Attributes.GetByName("MM_OBJ_FI_DESC").Allowed = True
Product.Attributes.GetByName("MM_OBJ_FI_KEY").Allowed = True

MM_OBJ_ERR_ACTION = Product.Attributes.GetByName("MM_OBJ_FI_ERR_CNTL").GetValue() or ""
Obj_FI_RECNO = Product.Attributes.GetByName("MM_OBJ_FI_RECNO").GetValue() or ""


# POPUP ERROR ATTRIBUTES HIDING
Product.Attributes.GetByName("MM_OBJ_FI_DATA_TYPE_ERR").Allowed = False
Product.Attributes.GetByName("MM_OBJ_FI_FIELD_LABEL_ERR").Allowed = False
Product.Attributes.GetByName("MM_OBJ_FI_API_NAME_ERR").Allowed = False
Product.Attributes.GetByName("MM_OBJ_FI_PERMISSIONS_ERR").Allowed = False

if str(MM_OBJ_ERR_ACTION) == "ERROR_OCCURED":
    Obj_Datatype = Product.Attributes.GetByName("MM_OBJ_FI_DATA_TYPE").GetValue() or ""
    Obj_Fieldlabel = Product.Attributes.GetByName("MM_OBJ_FI_FIELD_LABEL").GetValue() or ""
    Obj_Apiname = Product.Attributes.GetByName("MM_OBJ_FI_API_NAME").GetValue() or ""
    Obj_Permissions = Product.Attributes.GetByName("MM_OBJ_FI_PERMISSIONS").GetValue() or ""
    Obj_Key = Product.Attributes.GetByName("MM_OBJ_FI_KEY").GetValue() or ""

    if Obj_Datatype != "":

        Product.Attributes.GetByName("MM_OBJ_FI_DATA_TYPE_ERR").Allowed = False
    else:
        Product.Attributes.GetByName("MM_OBJ_FI_DATA_TYPE_ERR").Allowed = True

    if Obj_Fieldlabel != "":
        Product.Attributes.GetByName("MM_OBJ_FI_FIELD_LABEL_ERR").Allowed = False
    else:
        Product.Attributes.GetByName("MM_OBJ_FI_FIELD_LABEL_ERR").Allowed = True

    if Obj_Apiname != "":
        Scrpcount = Sql.GetFirst("select * FROM  SYOBJD (nolock) where API_NAME ='" + str(Obj_Apiname) + "'")

        if Scrpcount is None:
            Product.Attributes.GetByName("MM_OBJ_FI_API_NAME_ERR").Allowed = False
        else:
            if Obj_FI_RECNO == "":
                Product.Attributes.GetByName("MM_OBJ_FI_API_NAME_ERR").Allowed = True
                Product.Attributes.GetByName(
                    "MM_OBJ_FI_API_NAME_ERR"
                ).HintFormula = "<div class='clrred'>ERROR : Api Name Association exists! </div>"
            else:
                Product.Attributes.GetByName("MM_OBJ_FI_API_NAME_ERR").Allowed = False
    else:
        Product.Attributes.GetByName("MM_OBJ_FI_API_NAME_ERR").Allowed = True
        Product.Attributes.GetByName(
            "MM_OBJ_FI_API_NAME_ERR"
        ).HintFormula = "<div class='clrred'>ERROR : Api Name Requried </div>"
    if Obj_Permissions != "":
        Product.Attributes.GetByName("MM_OBJ_FI_PERMISSIONS_ERR").Allowed = False
    else:
        Product.Attributes.GetByName("MM_OBJ_FI_PERMISSIONS_ERR").Allowed = True

if MM_OBJ_ACTION == "EDIT" and MM_OBJ_ACTION == "VIEW":
    if str(data_typ) == "LOOKUP":
        Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_SQL").Allowed = True

if str(data_typ) == "" or str(data_typ) == "DATE" or str(data_typ) == "DATE/TIME" or str(data_typ) == "CHECKBOX":

    Product.Attributes.GetByName("MM_OBJ_FI_LEN").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_LEN_ERR").Allowed = False

    Product.Attributes.GetByName("MM_OBJ_FI_DECIMAL").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_DECIMAL_ERR").Allowed = False

    Product.Attributes.GetByName("MM_OBJ_FI_PL_VALUE").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_PL_VALUE_ERR").Allowed = False

    Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_OBJECT").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_OBJECT_ERR").Allowed = False

    Product.Attributes.GetByName("MM_OBJ_FI_FORMULA_LOGIC").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_FORMULA_LOGIC_ERR").Allowed = False

    Product.Attributes.GetByName("MM_OBJ_FI_REL_LIST").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_SQL").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_REL_LIST_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_SQL").Allowed = False

    Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_SER_ICON").Allowed = False

    Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_API_NAME").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_API_NAME_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_API_NAME_SER_ICON").Allowed = False

    if str(data_typ) == "CHECKBOX":
        Product.Attributes.GetByName("MM_OBJ_FI_KEY").Allowed = False
        Product.Attributes.GetByName("MM_OBJ_FI_REQ").Access = 0

elif str(data_typ) == "LOOKUP":

    # LOOKUP SHOWING ATTRIBUTES
    Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_OBJECT").Allowed = True
    Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_OBJECT").Access = AttributeAccess.ReadOnly
    Product.Attributes.GetByName("MM_OBJ_FI_REL_LIST").Allowed = True
    Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_SQL").Allowed = True
    Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_API_NAME").Allowed = True
    Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_API_NAME").Access = AttributeAccess.ReadOnly
    Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_API_NAME_SER_ICON").Allowed = True
    Product.Attributes.GetByName("MM_OBJ_FI_KEY").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_SQL").Allowed = True

    # LOOKUP HIDING ATTTRIBUTES
    Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_OBJECT_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_REL_LIST_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_API_NAME_ERR").Allowed = False

    if str(MM_OBJ_ERR_ACTION) == "ERROR_OCCURED":
        Obj_Lookup_Obj = Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_OBJECT").GetValue() or ""
        Obj_Related_List = Product.Attributes.GetByName("MM_OBJ_FI_REL_LIST").GetValue() or ""
        Obj_LookUp_Field_Label = Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_API_NAME").GetValue() or ""

        if Obj_Lookup_Obj != "":
            Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_OBJECT_ERR").Allowed = False
        else:
            Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_OBJECT_ERR").Allowed = True

        if Obj_Related_List != "":
            Product.Attributes.GetByName("MM_OBJ_FI_REL_LIST_ERR").Allowed = False
        else:
            Product.Attributes.GetByName("MM_OBJ_FI_REL_LIST_ERR").Allowed = True

        if Obj_LookUp_Field_Label != "":
            Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_API_NAME_ERR").Allowed = False
        else:
            Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_API_NAME_ERR").Allowed = True

    Product.Attributes.GetByName("MM_OBJ_FI_LEN").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_LEN_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_DECIMAL").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_DECIMAL_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_PL_VALUE").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_PL_VALUE_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_FORMULA_LOGIC").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_FORMULA_LOGIC_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_PERMISSIONS").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_PERMISSIONS_ERR").Allowed = False


elif str(data_typ) == "TEXT":

    Product.Attributes.GetByName("MM_OBJ_FI_LEN").Allowed = True

    # TEXT HIDING ATTTRIBUTE
    Product.Attributes.GetByName("MM_OBJ_FI_LEN_ERR").Allowed = False

    if str(MM_OBJ_ERR_ACTION) == "ERROR_OCCURED":
        Obj_Length = Product.Attributes.GetByName("MM_OBJ_FI_LEN").GetValue() or ""

        if Obj_Length != "":
            Product.Attributes.GetByName("MM_OBJ_FI_LEN_ERR").Allowed = False
        else:
            Product.Attributes.GetByName("MM_OBJ_FI_LEN_ERR").Allowed = True

    Product.Attributes.GetByName("MM_OBJ_FI_DECIMAL").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_DECIMAL_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_PL_VALUE").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_PL_VALUE_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_OBJECT").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_OBJECT_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_FORMULA_LOGIC").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_FORMULA_LOGIC_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_REL_LIST").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_SQL").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_REL_LIST_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_SER_ICON").Allowed = False

    Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_API_NAME").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_API_NAME_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_API_NAME_SER_ICON").Allowed = False
elif str(data_typ) == "NUMBER" or str(data_typ) == "CURRENCY":

    Product.Attributes.GetByName("MM_OBJ_FI_LEN").Allowed = True
    Product.Attributes.GetByName("MM_OBJ_FI_DECIMAL").Allowed = True

    # NUMBER OR CURRENCY HIDING ATTTRIBUTE
    Product.Attributes.GetByName("MM_OBJ_FI_LEN_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_DECIMAL_ERR").Allowed = False

    if str(MM_OBJ_ERR_ACTION) == "ERROR_OCCURED":
        Obj_Length = Product.Attributes.GetByName("MM_OBJ_FI_LEN").GetValue() or ""
        Obj_Decimal = Product.Attributes.GetByName("MM_OBJ_FI_DECIMAL").GetValue() or ""

        if Obj_Length != "":
            Product.Attributes.GetByName("MM_OBJ_FI_LEN_ERR").Allowed = False
        else:
            Product.Attributes.GetByName("MM_OBJ_FI_LEN_ERR").Allowed = True
        if Obj_Decimal != "":
            Product.Attributes.GetByName("MM_OBJ_FI_DECIMAL_ERR").Allowed = False
        else:
            Product.Attributes.GetByName("MM_OBJ_FI_DECIMAL_ERR").Allowed = True

    Product.Attributes.GetByName("MM_OBJ_FI_PL_VALUE").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_PL_VALUE_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_OBJECT").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_OBJECT_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_FORMULA_LOGIC").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_FORMULA_LOGIC_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_REL_LIST").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_SQL").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_REL_LIST_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_SER_ICON").Allowed = False

    Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_API_NAME").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_API_NAME_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_API_NAME_SER_ICON").Allowed = False


elif str(data_typ) == "PICKLIST" or str(data_typ) == "PICKLIST (MULTI-SELECT)":

    Product.Attributes.GetByName("MM_OBJ_FI_PL_VALUE").Allowed = True

    # PICKLIST OR PICKLIST (MULTI-SELECT) HIDING ATTTRIBUTE
    Product.Attributes.GetByName("MM_OBJ_FI_PL_VALUE_ERR").Allowed = False

    if str(MM_OBJ_ERR_ACTION) == "ERROR_OCCURED":
        Obj_Value = Product.Attributes.GetByName("MM_OBJ_FI_PL_VALUE").GetValue() or ""

        if Obj_Value != "":
            Product.Attributes.GetByName("MM_OBJ_FI_PL_VALUE_ERR").Allowed = False
        else:
            Product.Attributes.GetByName("MM_OBJ_FI_PL_VALUE_ERR").Allowed = True

    Product.Attributes.GetByName("MM_OBJ_FI_LEN").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_DECIMAL").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_OBJECT").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_LEN_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_DECIMAL_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_OBJECT_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_FORMULA_LOGIC").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_FORMULA_LOGIC_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_REL_LIST").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_SQL").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_REL_LIST_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_SER_ICON").Allowed = False

    Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_API_NAME").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_API_NAME_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_API_NAME_SER_ICON").Allowed = False


elif str(data_typ) == "FORMULA":

    Product.Attributes.GetByName("MM_OBJ_FI_FORMULA_LOGIC").Allowed = True
    Product.Attributes.GetByName("MM_OBJ_FI_KEY").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_REQ").Access = 0

    # FORMULA  HIDING ATTTRIBUTE
    Product.Attributes.GetByName("MM_OBJ_FI_FORMULA_LOGIC_ERR").Allowed = False

    if str(MM_OBJ_ERR_ACTION) == "ERROR_OCCURED":
        Obj_Formula_Logic = Product.Attributes.GetByName("MM_OBJ_FI_FORMULA_LOGIC").GetValue() or ""

        if Obj_Formula_Logic != "":
            Product.Attributes.GetByName("MM_OBJ_FI_FORMULA_LOGIC_ERR").Allowed = False
        else:
            Product.Attributes.GetByName("MM_OBJ_FI_FORMULA_LOGIC_ERR").Allowed = True

    Product.Attributes.GetByName("MM_OBJ_FI_LEN").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_DECIMAL").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_PL_VALUE").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_OBJECT").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_LEN_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_DECIMAL_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_PL_VALUE_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_OBJECT_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_REL_LIST").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_SQL").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_REL_LIST_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_SER_ICON").Allowed = False

    Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_API_NAME").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_API_NAME_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_API_NAME_SER_ICON").Allowed = False
else:

    Product.Attributes.GetByName("MM_OBJ_FI_LEN").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_DECIMAL").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_PL_VALUE").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_OBJECT").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_LEN_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_DECIMAL_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_PL_VALUE_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_OBJECT_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_REL_LIST").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_SQL").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_REL_LIST_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_SER_ICON").Allowed = False

    Product.Attributes.GetByName("MM_OBJ_FI_FORMULA_LOGIC").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_FORMULA_LOGIC_ERR").Allowed = False

    Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_API_NAME").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_API_NAME_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_API_NAME_SER_ICON").Allowed = False
Product.Attributes.GetByName("MM_OBJ_FI_REQ").Access = 0
if Obj_Key != "":
    if str(data_typ) == "CHECKBOX" or str(data_typ) == "FORMULA" or str(data_typ) == "LOOKUP":
        Product.Attributes.GetByName("MM_OBJ_FI_REQ").Access = 0
    else:
        Product.Attributes.GetByName("MM_OBJ_FI_REQ").SelectDisplayValue("1")
        Product.Attributes.GetByName("MM_OBJ_FI_REQ").Access = AttributeAccess.ReadOnly
else:
    Product.Attributes.GetByName("MM_OBJ_FI_REQ").Access = 0

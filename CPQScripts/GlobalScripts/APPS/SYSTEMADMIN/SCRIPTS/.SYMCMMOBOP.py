# =========================================================================================================================================
#   __script_name : MMOBJ_FI_OPERATIONS.PY
#   __script_description : THIS SCRIPT IS USED TO DO CREATE, EDIT, VIEW OPERATIONS IN SYSTEM ADMIN CUSTOM OBJECTS
#   __primary_author__ : BAJI BABA
#   __create_date :
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
RecNo = Param.Primary_Data
ACTION = Param.ACTION

if ACTION == "ADDNEW":

    Product.Attributes.GetByName("MM_OBJ_FI_BTN_CANCEL").Allowed = True
    Product.Attributes.GetByName("MM_OBJ_FI_BTN_SAVE").Allowed = True

    Product.Attributes.GetByName("MM_OBJ_FI_RECNO").AssignValue(str(""))
    Product.ResetAttr("MM_OBJ_FI_FIELD_LABEL")
    Product.ResetAttr("MM_OBJ_FI_API_NAME")
    Product.ResetAttr("MM_OBJ_FI_DATA_TYPE")
    Product.ResetAttr("MM_OBJ_FI_REQ")
    Product.ResetAttr("MM_OBJ_FI_KEY")

    Product.ResetAttr("MM_OBJ_FI_LEN")

    Product.ResetAttr("MM_OBJ_FI_DECIMAL")

    Product.ResetAttr("MM_OBJ_FI_PL_VALUE")
    Product.ResetAttr("MM_OBJ_FI_PERMISSIONS")
    Product.ResetAttr("MM_OBJ_FI_DISPLAY_ORDER")

    Product.ResetAttr("MM_OBJ_FI_DESC")
    Product.Attributes.GetByName("MM_OBJ_FI_ERR_CNTL").AssignValue("ERROR_Not_OCCURED")

    # Activating Attribute in pop up In "ADDNEW" senario
    Product.Attributes.GetByName("MM_OBJ_FI_DATA_TYPE").Allowed = True
    Product.Attributes.GetByName("MM_OBJ_FI_FIELD_LABEL").Allowed = True
    Product.Attributes.GetByName("MM_OBJ_FI_API_NAME").Allowed = True
    Product.Attributes.GetByName("MM_OBJ_FI_REQ").Allowed = True
    Product.Attributes.GetByName("MM_OBJ_FI_PERMISSIONS").Allowed = True
    Product.Attributes.GetByName("MM_OBJ_FI_DESC").Allowed = True
    Product.Attributes.GetByName("MM_OBJ_FI_KEY").Allowed = True

    # Hiding  Error attributes in pop up In "ADDNEW" senario
    Product.Attributes.GetByName("MM_OBJ_FI_DATA_TYPE_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_FIELD_LABEL_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_API_NAME_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_PERMISSIONS_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_KEY_ERR").Allowed = False

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

    Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_SER_ICON").Allowed = False

    Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_API_NAME").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_API_NAME_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_API_NAME_SER_ICON").Allowed = False

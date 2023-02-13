# =========================================================================================================================================
#   __script_name : SYMCMOBJOP.PY
#   __script_description : THIS SCRIPT IS USED TO POPULATE THE DATA FOR ADD/EDIT OBJECT DETAILS UNDER SYSTEM ADMIN APP
#   __primary_author__ : LEO JOSEPH
#   __create_date :
# ==========================================================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct
RecordId = Param.Primary_Data
TabName = Param.TabNAME
Action = Param.ACTION
if Action == "ADDNEW":
    Product.Attributes.GetByName("MM_OBJ_BTN_BTL").Allowed = True
    Product.Attributes.GetByName("MM_OBJ_BTN_BTL").HintFormula = "CANCEL"
    Product.Attributes.GetByName("MM_OBJ_BTN_SAVE").Allowed = True
    Product.Attributes.GetByName("MM_OBJ_BTN_DELETE").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_BTN_EDIT").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_BTN_CANCEL").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_BTN_REFRESH").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_REC_ID").Allowed = False

    Product.Attributes.GetByName("MM_OBJ_LABEL_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_PL_LABEL_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_TBL_NAME_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_REC_NAME_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_DATA_TYPE_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_API_NAME_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_KEY_FIELD_LABEL_ERR").Allowed = False

    Product.Attributes.GetByName("MM_OBJ_SEC_REL_LIST").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_SUBSEC_SEC_REL_LIST").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_CTR_SEC_REL_LST").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_TAB_BANNER").HintFormula = "OBJECT INFORMATION : NEW"

    Product.Attributes.GetByName("MM_OBJ_TAB_ALERT").Allowed = False

    Product.ResetAttr("MM_OBJ_LABEL")
    Product.ResetAttr("MM_OBJ_PL_LABEL")
    Product.ResetAttr("MM_OBJ_TBL_NAME")
    Product.ResetAttr("MM_OBJ_DESC")
    Product.ResetAttr("MM_OBJ_REC_NAME")
    Product.ResetAttr("MM_OBJ_FI_FIELD_LABEL")
    Product.ResetAttr("MM_OBJ_FI_API_NAME")
    Product.ResetAttr("MM_OBJ_FI_DATA_TYPE")
    Product.ResetAttr("MM_OBJ_API_NAME")
    Product.ResetAttr("MM_OBJ_KEY_FIELD_LABEL")
    Product.ResetAttr("MM_OBJ_DIS_FORMAT")    
    Product.ResetAttr("MM_OBJ_FI_SHORT_LBL")
    

    Product.Attributes.GetByName("MM_OBJ_LABEL").Access = 0
    Product.Attributes.GetByName("MM_OBJ_PL_LABEL").Access = 0
    Product.Attributes.GetByName("MM_OBJ_TBL_NAME").Access = 0
    Product.Attributes.GetByName("MM_OBJ_DESC").Access = 0    
    Product.Attributes.GetByName("MM_OBJ_FI_SHORT_LBL").Access = 0    
    Product.Attributes.GetByName("MM_OBJ_REC_NAME").Access = 0
    Product.Attributes.GetByName("MM_OBJ_API_NAME").Access = 0
    Product.Attributes.GetByName("MM_OBJ_KEY_FIELD_LABEL").Access = 0

    Product.Attributes.GetByName("MM_OBJ_FIELD_REL").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_CTR_OBJ_DATA").Allowed = False

    Product.Attributes.GetByName("MM_OBJ_ACTION").AssignValue(str(Action))
    Product.Attributes.GetByName("MM_OBJ_DATA_TYPE").Allowed = True
    Product.Attributes.GetByName("MM_OBJ_DATA_TYPE").Access = AttributeAccess.ReadOnly
    Product.Attributes.GetByName("MM_OBJ_DIS_FORMAT").Allowed = True
    Product.Attributes.GetByName("MM_OBJ_DIS_FORMAT").Access = AttributeAccess.ReadOnly

    Product.Attributes.GetByName("MM_OBJECT_STATUS").Allowed = True
    Product.Attributes.GetByName("MM_OBJECT_STATUS").Access = AttributeAccess.ReadOnly
    Product.Attributes.GetByName("MM_OBJECT_STATUS").AssignValue("NEW")

    Product.GetContainerByName("MM_OBJ_CTR_OBJ_DATA").Clear()

    Product.Attributes.GetByName("MM_OBJ_CTR_LOOKUP_REL_LIST").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_CTR_SEARCH_LIST").Allowed = False
# =========================================================================================================================================
#   __script_name : SYMCACTBTL.PY
#   __script_description : THIS SCRIPT IS USED TO NAVIGATE BACK TO THE LIST FROM VIEW/EDIT ACTIONS IN SYSTEM ADMIN
#   __primary_author__ : 
#   __create_date :
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
##SYACTION BACKTOLIST

##RESETTING ATTRIBUTES
Product.ResetAttr("MM_ACT_REC_NO")
Product.ResetAttr("MM_ACT_ACT_NAME")
Product.ResetAttr("QSTN_MM_ACT_ACT_ORDER")
Product.ResetAttr("MM_ACT_ACT_DESC")
Product.ResetAttr("MM_ACT_TAB_REC_ID")
Product.ResetAttr("MM_ACT_VIS_VARIABLE_REC_ID")
Product.ResetAttr("MM_ACT_SCR_REC_ID")
Product.ResetAttr("MM_ACT_ACT_DESC")

##ASSIGNING ATTRIBUTES
MM_ACT_ACT_NAME_ERR = Product.Attributes.GetByName("MM_ACT_ACT_NAME_ERR")

MM_ACT_ACT_ORDER_ERR = Product.Attributes.GetByName("MM_ACT_ACT_ORDER_ERR")
MM_ACT_TAB_REC_NO_ERR = Product.Attributes.GetByName("MM_ACT_TAB_REC_NO_ERR")
MM_ACT_SCRIPT_REC_NO_ERR = Product.Attributes.GetByName("MM_ACT_SCRIPT_REC_NO_ERR")


##BUTTONS AND ATTRIBUTES VISIBILITY
MM_ACT_ACT_NAME_ERR.Allowed = False
MM_ACT_ACT_ORDER_ERR.Allowed = False
MM_ACT_TAB_REC_NO_ERR.Allowed = False
MM_ACT_SCRIPT_REC_NO_ERR.Allowed = False

# =========================================================================================================================================
#   __script_name : SYMCACTIDL.PY
#   __script_description : THIS SCRIPT IS USED TO DELETE THE ACTIONS RECORDS IN SYSTEM ADMIN APP
#   __primary_author__ : 
#   __create_date :
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import SYTABACTIN as Table
from SYDATABASE import SQL
Sql = SQL()

def Actions_Delete():

    RecordId = Product.Attributes.GetByName("MM_ACT_REC_NO").GetValue()
    ActInfo = Sql.GetList(
        "SELECT RECORD_ID FROM SYPSAC where RECORD_ID= '" + str(RecordId) + "'"
    )
    if ActInfo is not None:
        for item in ActInfo:
            Rec_No = item.RECORD_ID
            if Rec_No != "":
                Table.TableActions.Delete("SYPSAC", "RECORD_ID", Rec_No)
        return "Deleted"


Product.Attributes.GetByName("MM_ACT_ACTION").AssignValue("DELETE")
Actions_Delete()
# Clear Attributes
Product.ResetAttr("MM_ACT_REC_NO")
Product.ResetAttr("MM_ACT_ACT_NAME")
Product.ResetAttr("MM_ACT_ATTR_NAME")
Product.ResetAttr("MM_ACT_ACT_ORDER")
Product.ResetAttr("MM_ACT_ACT_DESC")
Product.ResetAttr("MM_ACT_TAB_REC_ID")
Product.ResetAttr("MM_ACT_SCR_REC_ID")
Product.ResetAttr("MM_ACT_VIS_VARIABLE_REC_ID")

##ASSIGNING ATTRIBUTES AND BUTTONS
ACT_RECNO = Product.Attributes.GetByName("MM_ACT_REC_NO")
ACT_NAME = Product.Attributes.GetByName("MM_ACT_ACT_NAME")
ACT_ORDER = Product.Attributes.GetByName("MM_ACT_ACT_ORDER")
ACT_DESC = Product.Attributes.GetByName("QSTN_MM_ACT_ACT_DES")
ACT_SAVE = Product.Attributes.GetByName("MM_ACT_BTN_SAVE")
ACT_EDIT = Product.Attributes.GetByName("MM_ACT_BTN_EDIT")
ACT_BACKTM = Product.Attributes.GetByName("MM_ACT_BTN_BACKTM")
ACT_INFO = Product.Attributes.GetByName("MM_ACT_ACT_DESC")
ACT_DELETE = Product.Attributes.GetByName("MM_ACT_BTN_DELETE")
ACT_CANCEL = Product.Attributes.GetByName("MM_ACT_BTN_CANCEL")
CTR_ACT_INFO = Product.GetContainerByName("MM_ACT_CTR_ACT_INFO")
ACT_TAB_SEARCH = Product.Attributes.GetByName("MM_ACT_TAB_SEARCH")
ACT_SCR_SEARCH = Product.Attributes.GetByName("MM_ACT_SCR_SEARCH")
ACT_VIS_VAR_SEARCH = Product.Attributes.GetByName("MM_ACT_VIS_VAR_SEARCH")


##BUTTONS AND ATTRIBUTES VISIBILITY
ACT_RECNO.Allowed = False
ACT_SAVE.Allowed = True
ACT_CANCEL.Allowed = False
ACT_EDIT.Allowed = False
ACT_DELETE.Allowed = False
ACT_BACKTM.Allowed = True
ACT_TAB_SEARCH.Allowed = True
ACT_SCR_SEARCH.Allowed = True
ACT_VIS_VAR_SEARCH.Allowed = True
ACT_BACKTM.HintFormula = "CANCEL"

##ACTION HEADER
ACT_INFO.HintFormula = '<div   class="row modulebnr brdr mrgbt6" data-toggle="collapse" data-target="#toggle_main">ACTION INFORMATION : NEW  <i class="pull-right fa fa-chevron-down "></i><i class="pull-right fa fa-chevron-up"></i></div>'

##SET EDITABILITY
ACT_NAME.Access = AttributeAccess.Editable
ACT_ORDER.Access = AttributeAccess.Editable
ACT_DESC.Access = AttributeAccess.Editable

##CLEAR CONTAINER
CTR_ACT_INFO.Clear()
##RELOAD CONTAINER
CTR_ACT_INFO.LoadFromDatabase("SELECT * FROM SYPSAC", "")

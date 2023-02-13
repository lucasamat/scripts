# =========================================================================================================================================
#   __script_name : SYTABACTBT.PY
#   __script_description :  THIS SCRIPT IS USED TO GET THE ACTION BUTTONS FOR A GIVEN TAB.
#   __primary_author__ : JOE EBENEZER
#   __create_date :
# ========================================================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct
userid = User.Id
from SYDATABASE import SQL
Sql = SQL()

def TAB_ACTION_BUTTONS():
    tab_List = Sql.GetList(
    "select mm.TAB_LABEL,ms.CAN_ADD,ms.CAN_EDIT,ms.CAN_DELETE,ms.CAN_CLONE from SYTABS (NOLOCK) mm INNER JOIN SYSECT (NOLOCK) mt INNER JOIN SYOBJS (NOLOCK) ms on ((ms.OBJ_REC_ID = mt.PRIMARY_OBJECT_RECORD_ID) AND (ms.NAME = 'Tab list')) ON mm.RECORD_ID = mt.TAB_RECORD_ID"
    )
    tab_List_Values = []
    a = {}
    for item in tab_List:
        tab_List_Values.append(
            item.TAB_LABEL
            + "|"
            + item.CAN_ADD
            + "|"
            + item.CAN_EDIT
            + "|"
            + item.CAN_DELETE
            + "|"
            + item.CAN_CLONE
        )
	
	return tab_List_Values



ApiResponse = ApiResponseFactory.JsonResponse(TAB_ACTION_BUTTONS())


if str(Product.Name) == "SYSTEM ADMIN":
	tabs = Product.Tabs
	for tab in Product.Tabs:
		if tab.IsSelected == True:
			if Product.Attributes.GetByName("MA_MTR_ACTIVE_TAB") is not None:
				if str(tab.Name) != "Profiles" and str(tab.Name) != "Profile":
					Product.Attributes.GetByName("MA_MTR_ACTIVE_TAB").AssignValue(
						"Profiles"
					)
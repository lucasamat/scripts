# =========================================================================================================================================
#   __script_name : SYDELETALL.PY
#   __script_description : THIS SCRIPT IS USED WHEN BULK DELETING RELATED LIST RECORDS.
#   __primary_author__ : JOE EBENEZER
#   __create_date :
#   Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
from SYDATABASE import SQL
import SYTABACTIN as Table
import SYCNGEGUID as CPQID
import Webcom.Configurator.Scripting.Test.TestProduct
Sql = SQL()

def CustomerRestrictedItem(lable, value1):
	sqlobj1 = Sql.GetFirst(
		"SELECT "
		+ lable
		+ " FROM MAEXMA WHERE MATERIAL_RECORD_ID  = '"
		+ str(value1)
		+ "'"
	)
	if sqlobj1 is None:
		recid_obj = Sql.GetFirst(
			"SELECT MATERIAL_RECORD_ID,SAP_PART_NUMBER,EXCLUSIVE_MATERIAL FROM MAMTRL WHERE MATERIAL_RECORD_ID='"
			+ str(value1)
			+ "'"
		)
		if recid_obj:
			row = {}
			row["EXCLUSIVE_MATERIAL"] = ""
			row["MATERIAL_RECORD_ID"] = recid_obj.MATERIAL_RECORD_ID
			Table.TableActions.Update("MAMTRL", "MATERIAL_RECORD_ID", row)
	return ""


def DELETETABLERECORD(LABLE, VALUE, TABLEID):
	CustomerRestricted = ""
	lable = LABLE.split(",")[0]
	lable = LABLE.split(",")[0]
	value = VALUE.split(",")[0]
	table_id = TABLEID.split("_")[0]
	RECORD_ID = CPQID.KeyCPQId.GetKEYId(str(table_id), str(lable))
	primaryQueryItems = Sql.GetList(
		"select * FROM "
		+ str(table_id)
		+ " where "
		+ value
		+ " = '"
		+ str(RECORD_ID)
		+ "'"
	)
	tableInfo = Sql.GetTable(table_id)
	for primaryItem in primaryQueryItems:
		tableInfo.AddRow(primaryItem)
		Sql.Delete(tableInfo)
	if CustomerRestricted is not None:
		CustomerRestrictedItem(value, CustomerRestricted)
	return "test"


def DELETECONFIRMATION(OPERATION, TABLEID, RecordId, GridID):
	if OPERATION == "THIRD":
		click = "cont_relatedlist_DELETE_cancel(this)"
		click_ok = "cont_related_delete()"
	else:
		click = "popup_cont_DELETE_cancel()"
		click_ok = "cont_view_delete()"
		# click_ok='cont_modalDelete()'

	GridName =""
	sql_obj = Sql.GetFirst("select RECORD_ID,NAME,RELATED_LIST_SINGULAR_NAME from SYOBJR where RECORD_ID = '"+ str(GridID)+"'")
	if sql_obj is not None:
		GridName = str(sql_obj.RELATED_LIST_SINGULAR_NAME).strip()
	ban_str = ""
	sec_str = ""
	ban_str += '<div class="pad0">'
	#ban_str += '<div class="modulesecbnr brdr"  >'
	ban_str += "RELATED LIST : DELETE "+str(RecordId)
	#ban_str += '<button type="button" class="close" data-dismiss="modal">X</button>'
	ban_str += "</div>"
	sec_str += '<div class="pad-10">Are you sure you would like to delete this '+str(GridName).title()+" "+str(RecordId)+'?</div>'
	'''sec_str += '<div class="modal-footer">'
	sec_str += (
		'<button type="button" onclick="'
		+ str(click_ok)
		+ '"  class="fltrt">OK</button>'
	)
	sec_str += (
		'<button type="button" id="'
		+ str(TABLEID)
		+ '" onclick="'
		+ str(click)
		+ '" class="fltrtmrrt6">Cancel</button>'
	)
	sec_str += "</div>" '''
	return ban_str,sec_str


LABLE = Param.LABLE
VALUE = Param.VALUE
TABLEID = Param.TABLEID
OPERATION = Param.OPERATION
try:
	GridID = Param.GridID
except:
	GridID = ""
try:
	RecordId = Param.RecordId
except:
	RecordId = ""    
if OPERATION == "FIRST" or OPERATION == "THIRD":
	ApiResponse = ApiResponseFactory.JsonResponse(
		DELETECONFIRMATION(OPERATION, TABLEID, RecordId, GridID)
	)

elif OPERATION == "SECOND":
	ApiResponse = ApiResponseFactory.JsonResponse(
		DELETETABLERECORD(LABLE, VALUE, TABLEID)
	)
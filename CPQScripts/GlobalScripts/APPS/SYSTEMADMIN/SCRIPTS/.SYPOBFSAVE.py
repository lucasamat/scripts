# =========================================================================================================================================
#   __script_name : SYPOBFSAVE.PY
#   __script_description : This script is used to view and edit operations (System Admin->Profile Tab->Object Field Settings Permission) 
#   __primary_author__ : JOE EBENEZER
#   __create_date : 31/08/2020
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ============================================================================================================================

import SYCNGEGUID as CPQID
def save_pfobfield_details(value, key):
	datas = ''
	key  = ["PROFILE_OBJECTFIELD_RECORD_ID", "OBJECT_LABEL", "READ_ACCESS", "UPDATE_ACCESS"]
	objsetzip = zip(key,value)
	objdict= dict(objsetzip)
	objdict.pop('PROFILE_OBJECTFIELD_RECORD_ID')
	tableInfo = SqlHelper.GetTable("SYPROF")
	id1 = value[0]
	recid = CPQID.KeyCPQId.GetKEYId('SYPROF',str(id1))
	obj_data = SqlHelper.GetFirst("SELECT CpqTableEntryId,OBJECTFIELD_RECORD_ID,OBJECT_RECORD_ID FROM SYPROF WHERE PROFILE_OBJECTFIELD_RECORD_ID='"+str(recid) +"'")
	OBJECTFIELD_RECORD_ID_VAL = str(obj_data.OBJECTFIELD_RECORD_ID)
	OBJECT_RECORD_ID_VAL = str(obj_data.OBJECT_RECORD_ID)
	dictc = {'CpqTableEntryId':obj_data.CpqTableEntryId}
	objdict.update(dictc)
	
	tableInfo.AddRow(objdict)
	SqlHelper.Upsert(tableInfo)
	
	READ_ACCESSval = objdict.get('READ_ACCESS')
	UPDATE_ACCESSval = objdict.get('UPDATE_ACCESS')
	tableInfoJd = SqlHelper.GetTable("SYPRJD")
	syprjd_data = SqlHelper.GetFirst("SELECT CpqTableEntryId FROM SYPRJD WHERE  SYOBJD_RECORD_ID='"+str(OBJECTFIELD_RECORD_ID_VAL) +"'")
	if READ_ACCESSval == True and UPDATE_ACCESSval == True:
		dictcSyprjd = {'CpqTableEntryId':syprjd_data.CpqTableEntryId,'PERMISSION':'EDITABLE','Visible':True}
	elif READ_ACCESSval == False and UPDATE_ACCESSval == False:
		dictcSyprjd = {'CpqTableEntryId':syprjd_data.CpqTableEntryId,'PERMISSION':'READ ONLY','Visible':False}
	elif READ_ACCESSval == True and UPDATE_ACCESSval == False:
		dictcSyprjd = {'CpqTableEntryId':syprjd_data.CpqTableEntryId,'PERMISSION':'READ ONLY','Visible':True}
	else:
		dictcSyprjd = {'CpqTableEntryId':syprjd_data.CpqTableEntryId,'PERMISSION':'READ ONLY','Visible':False}
	tableInfoJd.AddRow(dictcSyprjd)
	SqlHelper.Upsert(tableInfoJd)
	return datas

value = Param.value
key = Param.key
ApiResponse = ApiResponseFactory.JsonResponse(save_pfobfield_details(value, key))
# =========================================================================================================================================
#   __script_name : CQSPBKEDIT.PY
#   __script_description : THIS SCRIPT IS USED TO DELETE A RECORD WHEN THE USER CLICKS ON THE DELETE BUTTON.
#   __primary_author__ : DHURGA
#   __create_date : 29/10/2020
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================

import Webcom.Configurator.Scripting.Test.TestProduct
Trace.Write('BULK EDIT_SAVE')
import math
import SYCNGEGUID as CPQID
from SYDATABASE import SQL

Sql = SQL()

getcpqvqlyelt = []
spare_bulksave = []
getqtcpqid = []
getQSPRlist =[]
sqlforupdate = ""
getpartNum = getCPA = getQSPR =  ""
ContractRecordId = Quote.GetGlobal("contract_quote_record_id")
def BULKSAVE(CUS_ANN,SCH_MODE,GETQTID,GET_PARTNUM):
	#for val in GETQTID:
		#OBJNAMEVAL = val.split("-")[1]
		#getcpqvqlyelt.append(OBJNAMEVAL)
	tableInfo = SqlHelper.GetTable("SAQSPT")
	#spare_bulksave =zip(SCH_MODE,CUS_ANN,getcpqvqlyelt)
	tableSPPT = {}
	sqlforupdatePT = getep = EP = ""
	for SMO,CQ,PN in zip(SCH_MODE,CUS_ANN,GET_PARTNUM):
		
		sqlforupdatePT += "UPDATE SAQSPT SET CUSTOMER_ANNUAL_QUANTITY = '{AQ}' where QUOTE_RECORD_ID ='{CT}' and  PART_NUMBER ='{PN}' AND QTEREV_RECORD_ID = '{REV}'".format(SM= str(SMO),AQ =CQ ,CT = str(ContractRecordId),PN=str(PN),REV=quote_revision_record_id)
		Sql.RunQuery(sqlforupdatePT)
		
	
	
	sqlforupdate = sqlforupdateHP =""
	for SM,CQ,PN in zip(SCH_MODE,CUS_ANN,GET_PARTNUM):
		getpartNum = Sql.GetFirst("select CpqTableEntryId from  SAQIFP where QUOTE_RECORD_ID ='"+str(ContractRecordId)+"' and  PART_NUMBER ='"+str(PN)+"'")
		if getpartNum:
			#tableINfopQ = {'CpqTableEntryId':str(getpartNum.CpqTableEntryId),'SCHEDULE_MODE':str(SM),'ANNUAL_QUANTITY':str(CQ)}
			sqlforupdateHP += "UPDATE SAQIFP SET  ANNUAL_QUANTITY = '{AQ}', EXTENDED_PRICE = (UNIT_PRICE*'{AQ}') where QUOTE_RECORD_ID ='{CT}' and  PART_NUMBER ='{PN}'  AND QTEREV_RECORD_ID = '{REV}'".format(AQ =CQ ,CT = str(ContractRecordId),PN=str(PN),REV=quote_revision_record_id)
			Sql.RunQuery(sqlforupdateHP)
			
			sqlforupdate += "UPDATE QT__SAQIFP SET  ANNUAL_QUANTITY = {AQ}, EXTENDED_PRICE = (UNIT_PRICE*{AQ}) where QUOTE_RECORD_ID ='{CT}' and  PART_NUMBER ='{PN}'".format(AQ =CQ ,CT = str(ContractRecordId),PN=str(PN))
			Sql.RunQuery(sqlforupdate)
	
	return 'save'

CUS_ANN = list(Param.CUS_ANN)
SCH_MODE =list(Param.SCH_MODE)
GETQTID = list(Param.GETQTID)
GET_PARTNUM =list(Param.GET_PARTNUM)
quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
ApiResponse = ApiResponseFactory.JsonResponse(BULKSAVE(CUS_ANN,SCH_MODE,GETQTID,GET_PARTNUM,))
#===================================================================================================================#======================
#   __script_name : CQREVISION.PY
#   __script_description : THIS SCRIPT IS USED TO CREATE NEW REVISIONS AND UPDATE CUSTOM TABLES
#   __primary_author__ : SRIJAYDHURGA
#   __create_date :08/30/2021
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# #====================================================================================================================#======================
import Webcom.Configurator.Scripting.Test.TestProduct
import datetime
import time
from SYDATABASE import SQL
import clr
import sys
import System.Net
from System.Text.Encoding import UTF8
from System import Convert
import re
from datetime import timedelta , date
import SYTABACTIN as Table
import SYCNGEGUID as CPQID

Sql = SQL()
ScriptExecutor = ScriptExecutor
quote_contract_recordId = Quote.GetGlobal("contract_quote_record_id")
Trace.Write('23----')
#A055S000P01-8729 start
def create_new_revision(Opertion):
	CloneObject={
		"SAQTSO":"QUOTE_SALESORG_RECORD_ID",
		"SAQFBL":"QUOTE_FABLOCATION_RECORD_ID",
		"SAQFEQ":"QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID",
		"SAQTSV":"QUOTE_SERVICE_RECORD_ID",
		"SAQSCO":"QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID",
		"SAQSCA":"QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID",
		"SAQSCE":"QUOTE_SERVICE_COVERED_OBJ_ENTITLEMENTS_RECORD_ID",
		"SAQSGE":"QUOTE_SERVICE_GREENBOOK_ENTITLEMENT_RECORD_ID",
		"SAQSFE":"QUOTE_SERVICE_FAB_LOC_ENT_RECORD_ID",
		"SAQIEN":"QUOTE_ITEM_COVERED_OBJECT_ENTITLEMENTS_RECORD_ID",
		"SAQSAE":"QUOTE_SERVICE_COV_OBJ_ASS_ENT_RECORD_ID",
		"SAQSGB":"QUOTE_SERVICE_GREENBOOK_RECORD_ID",
		"SAQSRA":"QUOTE_SENDING_RECEIVING_ACCOUNT",
		"SAQSSE":"QUOTE_SERVICE_SENDING_FAB_LOC_EQUIP_ID",
		"SAQSSA":"QUOTE_SERVICE_SENDING_FAB_EQUIP_ASS_ID"
		}
	if Quote is not None:
		get_quote_info_details = Sql.GetFirst("select * from SAQTMT where MASTER_TABLE_QUOTE_RECORD_ID = '"+str(quote_contract_recordId)+"'")
		#Get Old Revision ID - Start
		get_old_revision_id = Sql.GetFirst("SELECT QTEREV_ID FROM SAQTRV WHERE ACTIVE='True' AND QUOTE_RECORD_ID= '"+str(quote_contract_recordId)+"'")
		Trace.Write(get_old_revision_id.QTEREV_ID)
		old_revision_no=get_old_revision_id.QTEREV_ID
		#Get Old Revision ID - END

		#create new revision start
		#edit_new_rev_quote = QuoteHelper.Edit(Quote.CompositeNumber)
		create_new_rev = Quote.CreateNewRevision(True)
		Quote.SetGlobal("contract_quote_record_id",quote_contract_recordId)
		#composite_number = Quote.CompositeNumber
		#current_revison = Quote.RevisionNumber
		#craete new revision ends
		get_quote_id = create_new_rev.QuoteId
		#create new revision -SAQTRV - update-start
		quote_revision_table_info = Sql.GetTable("SAQTRV")
		quote_revision_id = str(Guid.NewGuid()).upper()
		Quote.SetGlobal("quote_revision_record_id",str(quote_revision_id))
		get_current_rev = Sql.GetFirst("select MAX(QTEREV_ID) as rev_id from SAQTRV where QUOTE_RECORD_ID = '"+str(quote_contract_recordId)+"'")
		get_rev_details = Sql.GetFirst("SELECT DISTINCT TOP 1 CART2.CARTCOMPOSITENUMBER, CART_REVISIONS.REVISION_ID, CART_REVISIONS.DESCRIPTION as DESCRIPTION,CART.ACTIVE_REV, CART_REVISIONS.CART_ID, CART_REVISIONS.PARENT_ID, CART.USERID FROM CART_REVISIONS (nolock) INNER JOIN CART2 (nolock) ON CART_REVISIONS.CART_ID = CART2.CartId INNER JOIN CART(NOLOCK) ON CART.CART_ID = CART2.CartId WHERE CART2.CARTCOMPOSITENUMBER = '{}'  and REVISION_ID  = '{}' ".format(Quote.CompositeNumber,get_current_rev.rev_id))
		update_quote_rev = Sql.RunQuery("""UPDATE SAQTRV SET ACTIVE = {active_rev} WHERE QUOTE_RECORD_ID = '{QuoteRecordId}'""".format(QuoteRecordId=quote_contract_recordId,active_rev = 0))
		newrev_inc = int(get_current_rev.rev_id)+1
		quote_rev_data = {"QUOTE_REVISION_RECORD_ID": str(quote_revision_id),"QUOTE_ID": get_quote_info_details.QUOTE_ID,"QUOTE_NAME": get_rev_details.DESCRIPTION,"QUOTE_RECORD_ID": quote_contract_recordId,"ACTIVE":1,"REV_CREATE_DATE":get_quote_info_details.CONTRACT_VALID_FROM,"REV_EXPIRE_DATE":get_quote_info_details.CONTRACT_VALID_TO,"REVISION_STATUS":"IN-PROGRESS","QTEREV_ID":newrev_inc,"REV_APPROVE_DATE":'',"CART_ID":get_quote_id}
		quote_revision_table_info.AddRow(quote_rev_data)
		Sql.Upsert(quote_revision_table_info)
		#create new revision -SAQTRV - update-end

		#get quote data for update in SAQTMT start
		
		quote_table_info = Sql.GetTable("SAQTMT")
		if get_quote_info_details:
			quote_detials = ''
			#update SAQTMT start
			Sql.RunQuery("""UPDATE SAQTMT SET QTEREV_ID = {newrev_inc},QTEREV_RECORD_ID = '{quote_revision_id}',ACTIVE_REV={active_rev} WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{QuoteRecordId}'""".format(quote_revision_id=quote_revision_id,newrev_inc= newrev_inc,QuoteRecordId=quote_contract_recordId,active_rev = 0))
			#update SAQTMT end
			
			#INSERT salesorg start
			for cloneobjectname in CloneObject.keys():
				sqlobj=Sql.GetList("""SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{}'""".format(str(cloneobjectname)))
				insertcols = 'INSERT INTO '+ str(cloneobjectname) +'( '
				selectcols = "SELECT "
				for col in sqlobj:
					if col.COLUMN_NAME == CloneObject[str(cloneobjectname)]:
						insertcols = insertcols + str(col.COLUMN_NAME)
						selectcols = selectcols + " '{}' AS ".format(str(Guid.NewGuid()).upper()) + str(col.COLUMN_NAME)
					elif col.COLUMN_NAME == "QTEREV_ID":
						insertcols  = insertcols + "," + str(col.COLUMN_NAME)
						selectcols = selectcols + ", {} AS ".format(int(newrev_inc)) + str(col.COLUMN_NAME)
					elif col.COLUMN_NAME == "QTEREV_RECORD_ID":
						insertcols  = insertcols + "," + str(col.COLUMN_NAME)
						selectcols = selectcols + "," + "'{}' AS ".format(str(quote_revision_id)) + str(col.COLUMN_NAME)
					elif col.COLUMN_NAME == "CpqTableEntryId":
						continue
					else:
						insertcols  = insertcols + "," + str(col.COLUMN_NAME)
						selectcols = selectcols + "," + str(col.COLUMN_NAME)
				insertcols += " )"
				selectcols += " FROM "+ str(cloneobjectname) +" WHERE QUOTE_RECORD_ID='{}'".format(str(quote_contract_recordId))+" AND QTEREV_ID={}".format(int(old_revision_no))
				finalquery=insertcols+' '+selectcols
				Trace.Write(finalquery)
				ExecObjQuery = Sql.RunQuery(finalquery)
			#Sql.RunQuery("""UPDATE SAQTSO SET QTEREV_ID = '{newrev_inc}',QTEREV_RECORD_ID = '{quote_revision_id}' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}'""".format(quote_revision_id=quote_revision_id,newrev_inc= newrev_inc,QuoteRecordId=quote_contract_recordId))
			#INSERT salesorg end

			#Insert fabs start
			
			#Sql.RunQuery("""UPDATE SAQFBL SET QTEREV_ID = '{newrev_inc}',QTEREV_RECORD_ID = '{quote_revision_id}' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}'""".format(quote_revision_id=quote_revision_id,newrev_inc= newrev_inc,QuoteRecordId=quote_contract_recordId))
			#Insert fabs end


			#Sql.RunQuery("""UPDATE SAQTMT SET QTEREV_ID = {newrev_inc},QTEREV_RECORD_ID = '{quote_revision_id}',ACTIVE_REV={active_rev} WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{QuoteRecordId}'""".format(quote_revision_id=quote_revision_id,newrev_inc= newrev_inc,QuoteRecordId=quote_contract_recordId,active_rev = 0))
			#quote_detials = {"MASTER_TABLE_QUOTE_RECORD_ID": str(Guid.NewGuid()).upper(),"QUOTE_ID": get_quote_info_details.QUOTE_ID,"QUOTE_NAME":get_quote_info_details.QUOTE_NAME,"ACCCNT_RECORD_ID":get_quote_info_details.ACCCNT_RECORD_ID,"ACCOUNT_ID":get_quote_info_details.ACCOUNT_ID,"ACCOUNT_NAME":get_quote_info_details.ACCOUNT_NAME,"ACCOUNT_RECORD_ID":get_quote_info_details.ACCOUNT_RECORD_ID,"CRM_CONTRACT_ID":get_quote_info_details.CRM_CONTRACT_ID,"QUOTE_TYPE":get_quote_info_details.QUOTE_TYPE,"SALE_TYPE":get_quote_info_details.SALE_TYPE,"QUOTE_LEVEL":get_quote_info_details.QUOTE_LEVEL,"REGION":get_quote_info_details.REGION,"QUOTE_STATUS":get_quote_info_details.QUOTE_STATUS,"CONTRACT_VALID_FROM":get_quote_info_details.CONTRACT_VALID_FROM,"CONTRACT_VALID_TO":get_quote_info_details.CONTRACT_VALID_TO,"PARENTQUOTE_ID":get_quote_info_details.PARENTQUOTE_ID,"PARENTQUOTE_NAME":get_quote_info_details.PARENTQUOTE_NAME,"PARENTQUOTE_RECORD_ID":get_quote_info_details.PARENTQUOTE_RECORD_ID,"PAYMENTTERM_ID":get_quote_info_details.PAYMENTTERM_ID,"INCOTERMS":get_quote_info_details.INCOTERMS,"PAYMENTTERM_NAME":get_quote_info_details.PAYMENTTERM_NAME,"PAYMENTTERM_RECORD_ID":get_quote_info_details.PAYMENTTERM_RECORD_ID,"DOCUMENT_TYPE":get_quote_info_details.DOCUMENT_TYPE,"SEGMENT_RECORD_ID":get_quote_info_details.SEGMENT_RECORD_ID,"C4C_QUOTE_ID":get_quote_info_details.C4C_QUOTE_ID,"QUOTE_CURRENCY":get_quote_info_details.QUOTE_CURRENCY,"QUOTE_CURRENCY_RECORD_ID":get_quote_info_details.QUOTE_CURRENCY_RECORD_ID,"CANCELLATION_PERIOD":get_quote_info_details.CANCELLATION_PERIOD,"SEGMENT_ID":get_quote_info_details.SEGMENT_ID,"GLOBAL_CURRENCY":get_quote_info_details.GLOBAL_CURRENCY,"GLOBAL_CURRENCY_RECORD_ID":get_quote_info_details.GLOBAL_CURRENCY_RECORD_ID,"PAYMENTTERM_DAYS":get_quote_info_details.PAYMENTTERM_DAYS,"QUOTE_EXPIRE_DATE":get_quote_info_details.QUOTE_EXPIRE_DATE,"ACTIVE_REV":0,"QTEREV_ID":newrev_inc,"QTEREV_RECORD_ID":quote_revision_id,"QUOTE_APPROVE_DATE":get_quote_info_details.QUOTE_APPROVE_DATE}
			#quote_table_info.AddRow(quote_detials)
			#Sql.Upsert(quote_table_info)
		#get quote data for update in SAQTMT end


	return True

def set_active_revision(Opertion,select_active):
	Trace.Write('121---'+str(select_active))
	recid = ''
	for val in select_active:
		ObjectName = val.split('-')[0].strip()
		cpqid = val.split('-')[1].strip()
		recid = CPQID.KeyCPQId.GetKEYId(ObjectName,str(cpqid))
	Trace.Write('121---recid---'+str(recid))
	get_quote_info_details = Sql.GetFirst("select * from SAQTMT where MASTER_TABLE_QUOTE_RECORD_ID = '"+str(quote_contract_recordId)+"'")
	Quote.SetGlobal("contract_quote_record_id",quote_contract_recordId)
	update_quote_rev = Sql.RunQuery("""UPDATE SAQTRV SET ACTIVE = {active_rev} WHERE QUOTE_RECORD_ID = '{QuoteRecordId}'""".format(QuoteRecordId=quote_contract_recordId,active_rev = 0))
	update_quote_set_active_rev = Sql.RunQuery("""UPDATE SAQTRV SET ACTIVE = {active_rev} WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' and QUOTE_REVISION_RECORD_ID = '{recid}'""".format(QuoteRecordId=quote_contract_recordId,active_rev = 1,recid =recid))
	return True
Opertion = Param.Opertion
select_active = list(Param.select_active)

Trace.Write("--select_active--------------"+str(select_active))
if Opertion == "SET_ACTIVE":
	ApiResponse = ApiResponseFactory.JsonResponse(set_active_revision(Opertion,select_active,))
else:
	ApiResponse = ApiResponseFactory.JsonResponse(create_new_revision(Opertion,))
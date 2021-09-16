#===================================================================================================================#======================
#   __script_name : CQREVISION.PY
#   __script_description : THIS SCRIPT IS USED TO CREATE NEW REVISIONS,EDIT REVISIONS AND UPDATE CUSTOM TABLES
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
from datetime import datetime, timedelta
import SYTABACTIN as Table
import SYCNGEGUID as CPQID

Sql = SQL()
ScriptExecutor = ScriptExecutor
quote_contract_recordId = Quote.GetGlobal("contract_quote_record_id")
Trace.Write('23----test')
#A055S000P01-8729 start
def create_new_revision(Opertion,cartrev):
	cloneobject={
		"SAQFBL":"QUOTE_FABLOCATION_RECORD_ID",
		"SAQFEQ":"QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID",
		"SAQTSV":"QUOTE_SERVICE_RECORD_ID",
		"SAQTSE":"QUOTE_SERVICE_ENTITLEMENT_RECORD_ID",
		"SAQSCO":"QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID",
		"SAQSCA":"QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID",
		"SAQSCE":"QUOTE_SERVICE_COVERED_OBJ_ENTITLEMENTS_RECORD_ID",
		"SAQSGE":"QUOTE_SERVICE_GREENBOOK_ENTITLEMENT_RECORD_ID",
		"SAQSFE":"QUOTE_SERVICE_FAB_LOC_ENT_RECORD_ID",
		"SAQSAE":"QUOTE_SERVICE_COV_OBJ_ASS_ENT_RECORD_ID",
		"SAQSGB":"QUOTE_SERVICE_GREENBOOK_RECORD_ID",
		"SAQSRA":"QUOTE_SENDING_RECEIVING_ACCOUNT",
		"SAQSSE":"QUOTE_SERVICE_SENDING_FAB_LOC_EQUIP_ID",
		"SAQSSA":"QUOTE_SERVICE_SENDING_FAB_EQUIP_ASS_ID",
		"SAQFEA":"QUOTE_FAB_LOC_COV_OBJ_ASSEMBLY_RECORD_ID",
		"SAQFGB":"QUOTE_FAB_LOC_GB_RECORD_ID",
		"SAQSFB":"QUOTE_SERVICE_FAB_LOCATION_RECORD_ID",
		"SAQSSF":"QUOTE_SERVICE_SENDING_FAB_LOC_ID"
		
		}
	#"SAQIBP":"QUOTE_ITEM_BILLING_PLAN_RECORD_ID"
	# "SAQITM":"QUOTE_ITEM_RECORD_ID",
	# "SAQIFL":"QUOTE_ITEM_FAB_LOCATION_RECORD_ID",
	# "SAQIGB":"QUOTE_ITEM_GREENBOOK_RECORD_ID",
	# "SAQIAP":"QUOTE_ITEM_COV_OBJ_ASS_PM_RECORD_ID",
	# "SAQICA":"QUOTE_ITEM_COVERED_OBJECT_ASSEMBLY_RECORD_ID",
	# "SAQIPE":"QUOTE_ITEM_FORECAST_PART_ENT_RECORD_ID",
	# "SAQIFP":"QUOTE_ITEM_FORECAST_PART_RECORD_ID"
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
		#composite_number = create_new_rev.CompositeNumber
		current_revison = Quote.RevisionNumber
		Trace.Write("============>> "+str(current_revison))
		#craete new revision ends
		get_quote_id = create_new_rev.QuoteId
		#create new revision -SAQTRV - update-start
		quote_revision_table_info = Sql.GetTable("SAQTRV")
		quote_revision_id = str(Guid.NewGuid()).upper()
		Quote.SetGlobal("quote_revision_record_id",str(quote_revision_id))
		get_current_rev = Sql.GetFirst("select MAX(QTEREV_ID) as rev_id from SAQTRV where QUOTE_RECORD_ID = '"+str(quote_contract_recordId)+"'")
		
		update_quote_rev = Sql.RunQuery("""UPDATE SAQTRV SET ACTIVE = {active_rev} WHERE QUOTE_RECORD_ID = '{QuoteRecordId}'""".format(QuoteRecordId=quote_contract_recordId,active_rev = 0))
		newrev_inc = int(get_current_rev.rev_id)+1
		get_rev_details = Sql.GetFirst("SELECT DISTINCT TOP 1 CART2.CARTCOMPOSITENUMBER, CART_REVISIONS.REVISION_ID, CART_REVISIONS.DESCRIPTION as DESCRIPTION,CART.ACTIVE_REV, CART_REVISIONS.CART_ID, CART_REVISIONS.PARENT_ID, CART.USERID FROM CART_REVISIONS (nolock) INNER JOIN CART2 (nolock) ON CART_REVISIONS.CART_ID = CART2.CartId INNER JOIN CART(NOLOCK) ON CART.CART_ID = CART2.CartId WHERE CART2.CARTCOMPOSITENUMBER = '{}'  and REVISION_ID  = '{}' ".format(Quote.CompositeNumber,newrev_inc))
		
		get_previous_rev_data = Sql.GetFirst("select * from SAQTRV where QUOTE_RECORD_ID = '"+str(quote_contract_recordId)+"' AND QTEREV_ID = '"+str(get_current_rev.rev_id)+"'")
		current_date = datetime.now()
		end_date = current_date + timedelta(days=365)
		if get_previous_rev_data:
			quote_rev_data = {
				"QUOTE_REVISION_RECORD_ID": str(quote_revision_id),
				"QUOTE_ID": get_quote_info_details.QUOTE_ID,
				"REVISION_DESCRIPTION": get_rev_details.DESCRIPTION,
				"QUOTE_NAME":get_quote_info_details.QUOTE_NAME,
				"QUOTE_RECORD_ID": quote_contract_recordId,
				"ACTIVE":1,
				"REV_CREATE_DATE":current_date.strftime('%m/%d/%Y'),
				"REV_EXPIRE_DATE":end_date.strftime('%m/%d/%Y'),
				"REVISION_STATUS":"NEW REVISION",
				"QTEREV_ID":newrev_inc,
				"QTEREV_RECORD_ID":quote_revision_id, 
				"REV_APPROVE_DATE":'',
				"CART_ID":get_quote_id,
				"SALESORG_ID": get_previous_rev_data.SALESORG_ID,
				"COUNTRY": get_previous_rev_data.COUNTRY,
				"COUNTRY_NAME": get_previous_rev_data.COUNTRY_NAME,
				"COUNTRY_RECORD_ID":get_previous_rev_data.COUNTRY_RECORD_ID,
				"REGION":get_previous_rev_data.REGION,
				"SALESORG_NAME": get_previous_rev_data.SALESORG_NAME,
				"SALESORG_RECORD_ID": get_previous_rev_data.SALESORG_RECORD_ID,							
				"GLOBAL_CURRENCY":get_previous_rev_data.GLOBAL_CURRENCY,							
				"GLOBAL_CURRENCY_RECORD_ID":get_previous_rev_data.GLOBAL_CURRENCY,
				"DIVISION_ID" : get_previous_rev_data.DIVISION_ID,
				"DISTRIBUTIONCHANNEL_RECORD_ID" :get_previous_rev_data.DISTRIBUTIONCHANNEL_RECORD_ID,
				"DIVISION_RECORD_ID" : get_previous_rev_data.DIVISION_RECORD_ID,
				"DOC_CURRENCY" : get_previous_rev_data.DOC_CURRENCY,
				"DOCCURR_RECORD_ID" : get_previous_rev_data.DOCCURR_RECORD_ID,
				"DOCUMENT_PRICING_PROCEDURE" : get_previous_rev_data.DOCUMENT_PRICING_PROCEDURE,
				"DISTRIBUTIONCHANNEL_ID" : get_previous_rev_data.DISTRIBUTIONCHANNEL_ID,
				"EXCHANGE_RATE" : get_previous_rev_data.EXCHANGE_RATE,
				"EXCHANGE_RATE_DATE" : get_previous_rev_data.EXCHANGE_RATE_DATE,
				"EXCHANGERATE_RECORD_ID" : get_previous_rev_data.EXCHANGERATE_RECORD_ID,
				"GLOBAL_CURRENCY" : get_previous_rev_data.GLOBAL_CURRENCY,
				"GLOBAL_CURRENCY_RECORD_ID" : get_previous_rev_data.GLOBAL_CURRENCY_RECORD_ID,
				"INCOTERM_ID" : get_previous_rev_data.INCOTERM_ID,
				"INCOTERM_NAME" : get_previous_rev_data.INCOTERM_NAME,
				"INCOTERM_RECORD_ID" : get_previous_rev_data.INCOTERM_RECORD_ID,
				"MODUSR_RECORD_ID" : get_previous_rev_data.MODUSR_RECORD_ID,
				"PAYMENTTERM_DAYS" : get_previous_rev_data.PAYMENTTERM_DAYS,
				"PAYMENTTERM_ID" : get_previous_rev_data.PAYMENTTERM_ID,
				"PAYMENTTERM_NAME" : get_previous_rev_data.PAYMENTTERM_NAME,
				"PAYMENTTERM_RECORD_ID" : get_previous_rev_data.PAYMENTTERM_RECORD_ID,
				"PRICINGPROCEDURE_ID" : get_previous_rev_data.PRICINGPROCEDURE_ID,
				"PRICINGPROCEDURE_NAME" : get_previous_rev_data.PRICINGPROCEDURE_NAME,
				"PRICINGPROCEDURE_RECORD_ID" :get_previous_rev_data.PRICINGPROCEDURE_RECORD_ID,
				"CANCELLATION_PERIOD":"90 DAYS",
				"CONTRACT_VALID_FROM":get_quote_info_details.CONTRACT_VALID_FROM
				"CONTRACT_VALID_TO":get_quote_info_details.CONTRACT_VALID_TO
			}

		quote_revision_table_info.AddRow(quote_rev_data)
		Sql.Upsert(quote_revision_table_info)
		#create new revision -SAQTRV - update-end

		#get quote data for update in SAQTMT start
		
		quote_table_info = Sql.GetTable("SAQTMT")
		if get_quote_info_details:
			quote_detials = ''
			#update SAQTMT start
			Sql.RunQuery("""UPDATE SAQTMT SET QTEREV_ID = {newrev_inc},QTEREV_RECORD_ID = '{quote_revision_id}',ACTIVE_REV={active_rev} WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{QuoteRecordId}'""".format(quote_revision_id=quote_revision_id,newrev_inc= newrev_inc,QuoteRecordId=quote_contract_recordId,active_rev = 1))
			#update SAQTMT end

			#update SAQTIP start
			Sql.RunQuery("""UPDATE SAQTIP SET QTEREV_ID = {newrev_inc},QTEREV_RECORD_ID = '{quote_revision_id}' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}'""".format(quote_revision_id=quote_revision_id,newrev_inc= newrev_inc,QuoteRecordId=quote_contract_recordId))
			#update SAQTIP end
			
			#CLONE ALL OBJECTS 
			for cloneobjectname in cloneobject.keys():
				sqlobj=Sql.GetList("""SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{}'""".format(str(cloneobjectname)))
				insertcols = 'INSERT INTO '+ str(cloneobjectname) +'( '
				selectcols = "SELECT "
				for col in sqlobj:
					if cloneobjectname in ("SAQSRA","SAQSSE","SAQSSA","SAQSSF") and col.COLUMN_NAME == "CPQTABLEENTRYADDEDBY":
						insertcols = insertcols + str(col.COLUMN_NAME)
						selectcols = selectcols + str(col.COLUMN_NAME)
					elif cloneobjectname in ("SAQSRA","SAQSSE","SAQSSA","SAQSSF") and col.COLUMN_NAME == cloneobject[str(cloneobjectname)]:
						insertcols = insertcols + "," + str(col.COLUMN_NAME)
						selectcols = selectcols + ", CONVERT(VARCHAR(4000),NEWID()) AS " + str(col.COLUMN_NAME)
					elif col.COLUMN_NAME == cloneobject[str(cloneobjectname)]:
						insertcols = insertcols + str(col.COLUMN_NAME)
						selectcols = selectcols + " CONVERT(VARCHAR(4000),NEWID()) AS " + str(col.COLUMN_NAME)
					elif col.COLUMN_NAME == "QTEREV_ID":
						insertcols = insertcols + "," + str(col.COLUMN_NAME)
						selectcols = selectcols + ", {} AS ".format(int(newrev_inc)) + str(col.COLUMN_NAME)
					elif col.COLUMN_NAME == "QTEREV_RECORD_ID":
						insertcols = insertcols + "," + str(col.COLUMN_NAME)
						selectcols = selectcols + "," + "'{}' AS ".format(str(quote_revision_id)) + str(col.COLUMN_NAME)
					elif col.COLUMN_NAME == "CpqTableEntryId":
						continue
					else:
						insertcols = insertcols + "," + str(col.COLUMN_NAME)
						selectcols = selectcols + "," + str(col.COLUMN_NAME)
				insertcols += " )"
				selectcols += " FROM "+ str(cloneobjectname) +" WHERE QUOTE_RECORD_ID='{}'".format(str(quote_contract_recordId))+" AND QTEREV_ID={}".format(int(old_revision_no))
				finalquery=insertcols+' '+selectcols
				Trace.Write(finalquery)
				ExecObjQuery = Sql.RunQuery(finalquery)
			
			## SAQSCO (QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID) MAPPED INTO  SAQSCE (QTESRVCOB_RECORD_ID):
			updatestatement = """UPDATE B SET B.QTESRVCOB_RECORD_ID = A.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID FROM SAQSCO A JOIN SAQSCE B ON A.EQUIPMENT_ID=B.EQUIPMENT_ID AND A.SERVICE_ID=B.SERVICE_ID AND A.FABLOCATION_ID=B.FABLOCATION_ID AND A.QUOTE_ID=B.QUOTE_ID AND A.SERIAL_NO=B.SERIAL_NO WHERE A.QTEREV_ID={} AND B.QTEREV_ID={} AND A.QUOTE_RECORD_ID=''{}'' AND B.QUOTE_RECORD_ID=''{}'' """.format(int(newrev_inc),int(newrev_inc),str(quote_contract_recordId),str(quote_contract_recordId))

			query_result = SqlHelper.GetFirst("sp_executesql @statement = N'" + str(updatestatement) + "'")
			Trace.Write(query_result)
			## END CLONE OBJECT SAQSCO TO SAQSCE
   			
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
		NRev = QuoteHelper.Edit(get_quote_info_details.QUOTE_ID)
		Quote.RefreshActions()
		for item in Quote.MainItems:
			item.Delete()
		Quote.Save()
		Quote.RefreshActions()
		current_revison1 = Quote.RevisionNumber
		Trace.Write("============>>1111 "+str(current_revison1))
		get_quote_info_details = Sql.GetFirst("select * from SAQTMT where QUOTE_ID = '"+str(Quote.CompositeNumber)+"'")
		Quote.SetGlobal("contract_quote_record_id",get_quote_info_details.MASTER_TABLE_QUOTE_RECORD_ID)
		Quote.SetGlobal("quote_revision_record_id",str(get_quote_info_details.QTEREV_RECORD_ID))
	return True



#set active revision  from grid- start
def set_active_revision(Opertion,cartrev):
	recid = ''
	Trace.Write('223----cartrev----'+str(cartrev))
	#for val in select_active:
	ObjectName = cartrev.split('-')[0].strip()
	cpqid = cartrev.split('-')[1].strip()
	#recid = CPQID.KeyCPQId.GetKEYId(ObjectName,str(cpqid))
	get_rev_quote_info_details = Sql.GetFirst("select * from SAQTRV where QUOTE_ID = '{}' and QTEREV_ID = {}".format(ObjectName,cpqid))
	if get_rev_quote_info_details:
		recid = get_rev_quote_info_details.QUOTE_REVISION_RECORD_ID
	get_quote_info_details = Sql.GetFirst("select * from SAQTMT where MASTER_TABLE_QUOTE_RECORD_ID = '"+str(quote_contract_recordId)+"'")
	Quote.SetGlobal("contract_quote_record_id",quote_contract_recordId)
	update_quote_rev = Sql.RunQuery("""UPDATE SAQTRV SET ACTIVE = {active_rev} WHERE QUOTE_RECORD_ID = '{QuoteRecordId}'""".format(QuoteRecordId=quote_contract_recordId,active_rev = 0))
	update_quote_set_active_rev = Sql.RunQuery("""UPDATE SAQTRV SET ACTIVE = {active_rev} WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' and QUOTE_REVISION_RECORD_ID = '{recid}'""".format(QuoteRecordId=quote_contract_recordId,active_rev = 1,recid =recid))
	get_rev_info_details = Sql.GetFirst("select QTEREV_ID from SAQTRV where QUOTE_RECORD_ID = '"+str(quote_contract_recordId)+"' and QUOTE_REVISION_RECORD_ID = '"+str(recid)+"'")
	Sql.RunQuery("""UPDATE SAQTMT SET QTEREV_ID = {newrev_inc},QTEREV_RECORD_ID = '{quote_revision_id}',ACTIVE_REV={active_rev} WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{QuoteRecordId}'""".format(quote_revision_id=recid,newrev_inc= get_rev_info_details.QTEREV_ID,QuoteRecordId=quote_contract_recordId,active_rev = 1))
	NRev = QuoteHelper.Edit(get_quote_info_details.QUOTE_ID)
	Quote.RefreshActions()
	for item in Quote.MainItems:
		item.Delete()
	Quote.Save()
	Quote.RefreshActions()
	current_revison1 = Quote.RevisionNumber
	get_quote_info_details = Sql.GetFirst("select * from SAQTMT where QUOTE_ID = '"+str(Quote.CompositeNumber)+"'")
	Quote.SetGlobal("contract_quote_record_id",get_quote_info_details.MASTER_TABLE_QUOTE_RECORD_ID)
	Quote.SetGlobal("quote_revision_record_id",str(get_quote_info_details.QTEREV_RECORD_ID))
	return True
#set active revision  from grid- end


#edit quote description field start
def save_desc_revision(Opertion,cartrev,cartrev_id,):
	Trace.Write(str(cartrev_id)+"-------cartrev----146---------"+str(cartrev))
	ObjectName = cartrev_id.split('-')[0].strip()
	cpqid = cartrev_id.split('-')[1].strip()
	recid = CPQID.KeyCPQId.GetKEYId(ObjectName,str(cpqid))
	update_quote_rev = Sql.RunQuery("""UPDATE SAQTRV SET REVISION_DESCRIPTION = '{rev_desc}' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND  QUOTE_REVISION_RECORD_ID = '{recid}' """.format(QuoteRecordId=quote_contract_recordId,recid =recid,rev_desc= cartrev))
	productdesc = SqlHelper.GetFirst("sp_executesql @t=N'update CART_REVISIONS set DESCRIPTION =''"+str(cartrev)+"'' where CART_ID = ''"+str(Quote.QuoteId)+"'' and VISITOR_ID =''"+str(Quote.UserId)+"''  '")
	return True
#edit quote description field end



Opertion = Param.Opertion
cartrev = Param.cartrev
try:
	cartrev_id =Param.cartrev_id
except:
	cartrev_id =''

if Opertion == "SET_ACTIVE":
	ApiResponse = ApiResponseFactory.JsonResponse(set_active_revision(Opertion,cartrev,))
elif Opertion == "SAVE_DESC":
	ApiResponse = ApiResponseFactory.JsonResponse(save_desc_revision(Opertion,cartrev,cartrev_id,))
else:
	ApiResponse = ApiResponseFactory.JsonResponse(create_new_revision(Opertion,cartrev,))
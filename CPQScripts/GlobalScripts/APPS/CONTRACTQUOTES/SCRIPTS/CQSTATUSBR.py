# =========================================================================================================================================
#   __script_name : CQSTATUSBR.PY
#   __script_description : THIS SCRIPT IS USED TO UPDATE THE DYNAMIC STATUS BAR.(and genarte billing matrix)
#   __primary_author__ : KRISHNA CHAITANYA,DHURGA GOPALAKRISHNAN
#   __create_date : 18/11/2021
#   Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import re
import Webcom.Configurator.Scripting.Test.TestProduct
import SYTABACTIN as Table
import SYCNGEGUID as CPQID
from SYDATABASE import SQL
import datetime
from datetime import timedelta , date
import sys
import System.Net
import CQPARTIFLW
import ACVIORULES
Param = Param 
Sql = SQL()
TestProduct = Webcom.Configurator.Scripting.Test.TestProduct() or "Sales"
try:
	contract_quote_record_id = Quote.QuoteId
except:
	contract_quote_record_id = ''
try:
	contract_quote_rec_id = Quote.GetGlobal("contract_quote_record_id")
except:
	contract_quote_rec_id = ''

try:
	quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
	
except:
	quote_revision_record_id =  ""

try:
	current_prod = Product.Name
	
except:
	current_prod = "Sales"
try:
	TabName = TestProduct.CurrentTab
except:
	TabName = "Quotes"

#contract_quote_rec_id = Quote.GetGlobal("contract_quote_record_id")
quote_revision_rec_id = Quote.GetGlobal("quote_revision_record_id")
user_id = str(User.Id)
user_name = str(User.UserName) 


def Dynamic_Status_Bar(quote_item_insert,Text):
	
	if (str(TabName) == "Quotes" or str(TabName) == "Quote") and current_prod == "Sales":
		Trace.Write('SAQSPT delete=======')
		Sql.RunQuery("UPDATE SAQSPT SET SCHEDULE_MODE='ON REQUEST', DELIVERY_MODE='OFFSITE' WHERE CUSTOMER_ANNUAL_QUANTITY<10 AND UNIT_PRICE >50 AND SERVICE_ID='Z0110' AND  QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id))
  
		#Sql.RunQuery("DELETE FROM SAQSPT WHERE CUSTOMER_ANNUAL_QUANTITY<10 AND UNIT_PRICE <50 AND SCHEDULE_MODE='ON REQUEST' AND DELIVERY_MODE='OFFSITE' AND SERVICE_ID='Z0110' AND  QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id))
		#Trace.Write('sales11=======')
		item_covered_obj =""
		getsalesorg_ifo = Sql.GetFirst("SELECT SALESORG_ID,REVISION_STATUS from SAQTRV where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id))
		#getfab_info = Sql.GetFirst("SELECT FABLOCATION_NAME from SAQSFB where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id))
		get_service_ifo = Sql.GetFirst("SELECT COUNT(DISTINCT SERVICE_ID) as SERVICE_ID from SAQTSV where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id))
		get_equip_details = Sql.GetFirst("SELECT COUNT(DISTINCT SERVICE_ID) as SERVICE_ID from SAQSCO where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id))
		
		get_addon_service_id = Sql.GetFirst("SELECT COUNT(DISTINCT SAQSGB.SERVICE_ID) as SERVICE_ID from SAQSGB INNER JOIN SAQSAO ON SAQSGB.QTEREV_RECORD_ID = SAQSAO.QTEREV_RECORD_ID AND SAQSGB.QUOTE_RECORD_ID = SAQSAO.QUOTE_RECORD_ID AND SAQSAO.SERVICE_ID = SAQSAO.SERVICE_ID where SAQSGB.QUOTE_RECORD_ID = '{}' AND SAQSGB.QTEREV_RECORD_ID = '{}'".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id))
		
		quote_ser_level_entitlement_obj = Sql.GetList(" SELECT CONFIGURATION_STATUS,SERVICE_ID FROM SAQTSE WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' ".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id))

		complete_status = incomplete_status = ""

		for configure in quote_ser_level_entitlement_obj:
			status = configure.CONFIGURATION_STATUS
			if status == "COMPLETE" and status != "":				
				complete_status = 'YES'
			else:
				incomplete_status = 'YES'
		Trace.Write("complete_status"+str(complete_status))
		Trace.Write("incomplete_status"+str(incomplete_status))
		price_preview_status = []
		item_covered_obj = Sql.GetList("SELECT DISTINCT STATUS FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id))
		if item_covered_obj:
			for status in item_covered_obj:
				price_preview_status.append(status.STATUS)
			Trace.Write("price_preview_status_CHK"+str(price_preview_status))
			if len(price_preview_status) > 1:
				price_bar = "acquired_status"
			if 'ACQUIRED' in price_preview_status:
				price_bar = "not_acquired_status"
			else:
				price_bar = "acquired_status"
		else:
			Trace.Write("NO Quote Items")
			price_bar = "no_quote_items"
		#get_documents_date_validation_accepted = Sql.GetFirst("SELECT DATE_ACCEPTED FROM SAQDOC (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id))				
		#get_documents_date_validation_rejected = Sql.GetFirst("SELECT DATE_REJECTED FROM SAQDOC (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id))
		#if getsalesorg_ifo and getfab_info:
		Trace.Write('not_acquired_status--'+str(price_bar))
		Trace.Write('COMPLETE STAGE---'+str(Text))
		if getsalesorg_ifo:
			if Text == "COMPLETE STAGE":		
				Trace.Write('salesorg--present---')
				if ((get_service_ifo.SERVICE_ID == get_equip_details.SERVICE_ID) or (get_service_ifo.SERVICE_ID == get_addon_service_id.SERVICE_ID) ) and incomplete_status == '' and complete_status != '' and Text == "COMPLETE STAGE":
					Trace.Write('stage--1')
					update_workflow_status = "UPDATE SAQTRV SET WORKFLOW_STATUS = 'CONFIGURE' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' ".format(QuoteRecordId=Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"))
					Sql.RunQuery(update_workflow_status)
				if ((get_service_ifo.SERVICE_ID == get_equip_details.SERVICE_ID) or (get_service_ifo.SERVICE_ID == get_addon_service_id.SERVICE_ID) ) and incomplete_status == '' and complete_status != '' and price_bar == 'not_acquired_status' and Text == "COMPLETE STAGE":
					Trace.Write('stage--2')
					update_workflow_status = "UPDATE SAQTRV SET WORKFLOW_STATUS = 'PRICING REVIEW' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' ".format(QuoteRecordId=Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"))
									
					Sql.RunQuery(update_workflow_status)
					ScriptExecutor.ExecuteGlobal('CQSDELPGPN',{'QUOTE_ID':Quote.GetGlobal("contract_quote_record_id"),'QTEREV_ID':Quote.GetGlobal("quote_revision_record_id"),'ACTION':'EMAIL'})
				if getsalesorg_ifo.REVISION_STATUS == "APPROVED" and Text == "COMPLETE STAGE":
					update_workflow_status = "UPDATE SAQTRV SET WORKFLOW_STATUS = 'APPROVALS' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' ".format(QuoteRecordId=Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"))
									
					Sql.RunQuery(update_workflow_status)
					status = "APPROVED"
				if (getsalesorg_ifo.REVISION_STATUS == "CUSTOMER ACCEPTED" or getsalesorg_ifo.REVISION_STATUS == "CUSTOMER REJECTED") and Text == "COMPLETE STAGE":
					#if str(get_documents_date_validation_accepted.DATE_ACCEPTED) != "":
					Trace.Write("accepted===")
					update_workflow_status = "UPDATE SAQTRV SET WORKFLOW_STATUS = 'QUOTE DOCUMENTS' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' ".format(QuoteRecordId=Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"))			
					Sql.RunQuery(update_workflow_status)
					status = "QUOTE DOCUMENTS"			
				
				if getsalesorg_ifo.REVISION_STATUS == "SUBMITTED FOR BOOKING" and Text == "COMPLETE STAGE":
					update_workflow_status = "UPDATE SAQTRV SET WORKFLOW_STATUS = 'CLEAN BOOKING CHECKLIST' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' ".format(QuoteRecordId=Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"))
									
					Sql.RunQuery(update_workflow_status)
					status = "SUBMITTED FOR BOOKING"
				if getsalesorg_ifo.REVISION_STATUS == "CONTRACT BOOKED" and Text == "COMPLETE STAGE":
					update_workflow_status = "UPDATE SAQTRV SET WORKFLOW_STATUS = 'BOOKED' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' ".format(QuoteRecordId=Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"))
									
					Sql.RunQuery(update_workflow_status)
					status = "CONTRACT BOOKED"
			
			get_workflow_status = Sql.GetFirst(" SELECT WORKFLOW_STATUS,REVISION_STATUS FROM SAQTRV WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' ".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id))
						
			if get_workflow_status.REVISION_STATUS == "APPROVED" and get_workflow_status.WORKFLOW_STATUS == "APPROVALS":				
				status = "APPROVED"
			elif get_workflow_status.REVISION_STATUS == "CUSTOMER ACCEPTED" or get_workflow_status.REVISION_STATUS == "CUSTOMER REJECTED":										
				status = "QUOTE DOCUMENTS"		
			
			elif get_workflow_status.REVISION_STATUS == "SUBMITTED FOR BOOKING" and get_workflow_status.WORKFLOW_STATUS == "CLEAN BOOKING CHECKLIST":					
				status = "SUBMITTED FOR BOOKING"
			elif get_workflow_status.REVISION_STATUS == "CONTRACT BOOKED" and get_workflow_status.WORKFLOW_STATUS == "BOOKED":					
				status = "CONTRACT BOOKED"

			elif get_workflow_status.WORKFLOW_STATUS:			
				Trace.Write('No button-2454-')
				status = get_workflow_status.WORKFLOW_STATUS           
			else:
				Trace.Write('No button--1')
				status = "IN-COMPLETE"
				
			# Set Quote Item Insert --> No, If Revision Status Equal to Approved - Start
			if getsalesorg_ifo.REVISION_STATUS == 'APPROVED':
				quote_item_insert = "No"
			# Set Quote Item Insert --> No, If Revision Status Equal to Approved - End
		else:
			Trace.Write('No button--2')
			status = "IN-COMPLETE"
	#Trace.Write("buttonvisibility=="+str(buttonvisibility))
	
	# Quote Item Inserts - Starts
	if quote_item_insert == 'yes' and Text == "COMPLETE STAGE":
		
		#service_id_query =  Sql.GetList("SELECT SERVICE_ID FROM SAQTSV (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(contract_quote_rec_id,quote_revision_record_id))
		service_id_query = Sql.GetList("SELECT SAQTSV.*,MAMTRL.MATERIALCONFIG_TYPE FROM SAQTSV INNER JOIN MAMTRL ON SAP_PART_NUMBER = SERVICE_ID WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'  ".format(contract_quote_rec_id,quote_revision_record_id))
		if service_id_query:
			for service_id in service_id_query:
				get_ent_config_status = Sql.GetFirst(""" SELECT COUNT(CONFIGURATION_STATUS) AS COUNT FROM SAQTSE (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID = '{}' AND CONFIGURATION_STATUS='COMPLETE' """.format(contract_quote_rec_id,quote_revision_record_id,service_id.SERVICE_ID))
				if get_ent_config_status.COUNT > 0 or service_id.MATERIALCONFIG_TYPE =='SIMPLE MATERIAL' or service_id.SERVICE_ID == 'Z0117':
					data = ScriptExecutor.ExecuteGlobal("CQINSQTITM",{"ContractQuoteRecordId":contract_quote_rec_id, "ContractQuoteRevisionRecordId":quote_revision_record_id, "ServiceId":service_id.SERVICE_ID, "ActionType":'INSERT_LINE_ITEMS'})
					if 1==1:
						GetSelf = Sql.GetFirst("SELECT CpqTableEntryId,APRTRXOBJ_ID FROM ACAPMA (NOLOCK) WHERE APRCHN_ID = 'SELFAPPR' AND APRTRXOBJ_RECORD_ID = '{}'".format(quote_revision_record_id))
						if GetSelf is not None:
							Sql.RunQuery("DELETE FROM ACAPMA WHERE APRTRXOBJ_RECORD_ID = '{}' AND APRCHN_ID = 'SELFAPPR'".format(quote_revision_record_id))
							Sql.RunQuery("DELETE FROM ACAPTX WHERE APRTRXOBJ_ID = '{}' AND APRCHN_ID = 'SELFAPPR'".format(GetSelf.APRTRXOBJ_ID))
							Sql.RunQuery("DELETE FROM ACACHR WHERE APPROVAL_ID LIKE '%{}%' AND APRCHN_ID = 'SELFAPPR'".format(GetSelf.APRTRXOBJ_ID))
						else:
							Sql.RunQuery("DELETE FROM ACAPMA WHERE APRTRXOBJ_RECORD_ID = '{}'".format(quote_revision_record_id))
							Sql.RunQuery("DELETE FROM ACAPTX WHERE APRTRXOBJ_ID = '{}' ".format(Quote.CompositeNumber))
							Sql.RunQuery("DELETE FROM ACACHR WHERE APPROVAL_ID LIKE '%{}%'".format(Quote.CompositeNumber))
						#Approval Trigger - Start		
						try:
							violationruleInsert = ACVIORULES.ViolationConditions()
							header_obj = Sql.GetFirst("SELECT RECORD_ID FROM SYOBJH (NOLOCK) WHERE OBJECT_NAME = 'SAQTRV'")
							if header_obj:			
								violationruleInsert.InsertAction(
																header_obj.RECORD_ID, quote_revision_record_id, "SAQTRV"
																)
						except:
							Trace.Write("violation error")
						#Approval Trigger - End
					'''except:
						Trace.Write("EXCEPT APPROVAL TRIGGER")'''
					Sql.RunQuery("""UPDATE SAQTRV SET REVISION_STATUS = 'ACQUIRING' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}'""".format(QuoteRecordId=contract_quote_rec_id,QuoteRevisionRecordId=quote_revision_record_id))
					try:
						##Calling the iflow for quote header writeback to cpq to c4c code starts..
						CQCPQC4CWB.writeback_to_c4c("quote_header",Quote.GetGlobal("contract_quote_record_id"),Quote.GetGlobal("quote_revision_record_id"))
						CQCPQC4CWB.writeback_to_c4c("opportunity_header",Quote.GetGlobal("contract_quote_record_id"),Quote.GetGlobal("quote_revision_record_id"))
						##Calling the iflow for quote header writeback to cpq to c4c code ends...
					except:
						pass
				# get_child_service_id = Sql.GetFirst("""SELECT SAQTSV.SERVICE_ID FROM SAQTSV (NOLOCK) JOIN SAQRSP (NOLOCK) ON SAQRSP.SERVICE_ID = SAQTSV.SERVICE_ID AND SAQRSP.QUOTE_RECORD_ID = SAQTSV.QUOTE_RECORD_ID AND SAQRSP.QTEREV_RECORD_ID = SAQTSV.QTEREV_RECORD_ID WHERE SAQTSV.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQTSV.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQTSV.PAR_SERVICE_ID = '{service_id}'""".format(QuoteRecordId = Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = quote_revision_record_id,service_id = service_id.SERVICE_ID if service_id.SERVICE_ID in ("Z0091","Z0092","Z0004","Z0006","Z0007","Z0035") else ''))
				# if get_child_service_id:
				# 	if get_child_service_id.SERVICE_ID == 'Z0101':
				# 		get_ent_config_status = Sql.GetFirst(""" SELECT COUNT(CONFIGURATION_STATUS) AS COUNT FROM SAQTSE (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID = '{}' AND CONFIGURATION_STATUS='COMPLETE' """.format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id,get_child_service_id.SERVICE_ID))
				# 		if get_ent_config_status.COUNT > 0:
				# 			data = ScriptExecutor.ExecuteGlobal("CQINSQTITM",{"ContractQuoteRecordId":Quote.GetGlobal("contract_quote_record_id"), "ContractQuoteRevisionRecordId":quote_revision_record_id, "ServiceId":get_child_service_id.SERVICE_ID, "ActionType":'INSERT_LINE_ITEMS'})

				#where = "WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID = '{}'".format(contract_quote_rec_id,quote_revision_record_id,service_id.SERVICE_ID)
				#data = ScriptExecutor.ExecuteGlobal("CQINSQTITM",{"WhereString":where, "ActionType":'UPDATE_LINE_ITEMS'})
				# data = ScriptExecutor.ExecuteGlobal("CQINSQTITM",{"ContractQuoteRecordId":Quote.GetGlobal("contract_quote_record_id"), "ContractQuoteRevisionRecordId":quote_revision_record_id, "ServiceId":service_id.SERVICE_ID, "ActionType":'INSERT_LINE_ITEMS'})
			# Pricing Calculation - Start
			quote_line_item_obj = Sql.GetFirst("SELECT LINE FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}'  AND ISNULL(STATUS,'') = ''".format(QuoteRecordId=contract_quote_rec_id,QuoteRevisionRecordId=quote_revision_record_id))
			#added condition to restrict email trigger thrice
			
			if quote_line_item_obj:
				quote_revision_obj = Sql.GetFirst("SELECT QTEREV_ID,QUOTE_ID from SAQTMT where MASTER_TABLE_QUOTE_RECORD_ID = '{QuoteRecordId}' ".format(QuoteRecordId=contract_quote_rec_id))
				if quote_revision_obj:
					#Log.Info("====> QTPOSTACRM called from ==> "+str(quote_revision_obj.QUOTE_ID)+'--'+str(quote_revision_obj.QTEREV_ID))
					ScriptExecutor.ExecuteGlobal('QTPOSTACRM',{'QUOTE_ID':quote_revision_obj.QUOTE_ID,'REVISION_ID':quote_revision_obj.QTEREV_ID, 'Fun_type':'cpq_to_sscm'})
					SqlHelper.GetFirst("sp_executesql @T=N'update A SET A.STATUS = (CASE WHEN A.STATUS =''ERROR'' THEN ''ERROR'' WHEN A.STATUS =''PARTIALLY PRICED'' THEN ''ERROR'' END) from SAQRIT A inner join ( select SERVICE_ID,LINE,SAQICO.QUOTE_ID from SAQICO WHERE SAQICO.QUOTE_ID = ''"+str(quote_revision_obj.QUOTE_ID)+"'' group by SERVICE_ID,LINE,SAQICO.QUOTE_ID Having count(*) > 1 ) as od on od.LINE = A.LINE AND od.SERVICE_ID = A.SERVICE_ID '")
					SqlHelper.GetFirst("sp_executesql @T=N'update A SET A.STATUS = (CASE WHEN A.STATUS =''ACQUIRING'' THEN ''ACQUIRING'' WHEN A.STATUS =''ERROR'' THEN ''ERROR'' END) from SAQRIT A inner join ( select SERVICE_ID,LINE,SAQICO.QUOTE_ID from SAQICO WHERE SAQICO.QUOTE_ID = ''"+str(quote_revision_obj.QUOTE_ID)+"'' group by SERVICE_ID,LINE,SAQICO.QUOTE_ID Having count(*) > 1 ) as od on od.LINE = A.LINE AND od.SERVICE_ID = A.SERVICE_ID '")
					SqlHelper.GetFirst("sp_executesql @T=N'update A SET A.STATUS = (CASE WHEN A.STATUS =''ACQUIRING'' THEN ''PARTIALLY PRICING'' WHEN A.STATUS =''PARTIALLY PRICING'' THEN ''PARTIALLY PRICING'' END) from SAQRIT A inner join ( select SERVICE_ID,LINE,SAQICO.QUOTE_ID from SAQICO WHERE SAQICO.QUOTE_ID = ''"+str(quote_revision_obj.QUOTE_ID)+"'' group by SERVICE_ID,LINE,SAQICO.QUOTE_ID Having count(*) > 1 ) as od on od.LINE = A.LINE AND od.SERVICE_ID = A.SERVICE_ID '")
			# Pricing Calculation - End
		
		##calling the iflow for pricing..
		try:
			contract_quote_obj = Sql.GetFirst("SELECT QUOTE_ID FROM SAQTMT (NOLOCK) WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{QuoteRecordId}'".format(QuoteRecordId=Quote.GetGlobal("contract_quote_record_id")))
			if contract_quote_obj:
				contract_quote_id = contract_quote_obj.QUOTE_ID
			count=Sql.GetFirst("SELECT COUNT(*) AS CNT FROM SAQSPT WHERE QUOTE_ID= '"+str(contract_quote_id)+"' and CUSTOMER_ANNUAL_QUANTITY IS NOT NULL ")      
			if count.CNT==0:
				#Log.Info("PART PRICING IFLOW STARTED WHEN USER CLICK COMPLETE STAGE!")
				CQPARTIFLW.iflow_pricing_call(str(User.UserName),str(contract_quote_id),str(quote_revision_record_id))
				#If Qty is null for all parts to call this function with specific parameters
				###calling script for saqris,saqtrv insert
				# CallingCQIFWUDQTM = ScriptExecutor.ExecuteGlobal("CQIFWUDQTM",{"QT_REC_ID":str(contract_quote_id),"Operation":"Delete"})
		except:
			Log.Info("PART PRICING IFLOW ERROR!")
		# Quote Item Inserts - Ends
	return status
try:
	quote_item_insert = Param.quote_item_insert
except:
	quote_item_insert = ''

try:
	Text = Param.Text
except:
	Text = ""
Trace.Write("quote_item_insert_J "+str(quote_item_insert))
ApiResponse = ApiResponseFactory.JsonResponse(Dynamic_Status_Bar(quote_item_insert,Text))  
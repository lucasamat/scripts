import re
import Webcom.Configurator.Scripting.Test.TestProduct
from SYDATABASE import sql_get_first, sql_get_list, sql_run_query, SQL
import CQPARTIFLW
import CQCPQC4CWB
import time

Sql = SQL()
TestProduct = Webcom.Configurator.Scripting.Test.TestProduct() or "Sales"
contract_quote_record_id = getattr(Quote, "QuoteId", '')
contract_quote_rec_id = Quote.GetGlobal("contract_quote_record_id") or ''
quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id") or ''
current_prod = Product.Name if hasattr(Product, "Name") else "Sales"

TabName = TestProduct.CurrentTab if hasattr(TestProduct, "CurrentTab") else "Quotes"


quote_revision_rec_id = Quote.GetGlobal("quote_revision_record_id")
user_id = User.Id

user_name = User.UserName


def Dynamic_Status_Bar(quote_item_insert,Text):
	status =''
	error_msg = ""
	if Text == 'COMPLETE STAGE' and current_prod == "Sales" and (TabName in ["Quotes", "Quote"]):

		#Salesorg[SAQTRV]
		getsalesorg_info = Sql.GetFirst("SELECT SALESORG_ID,REVISION_STATUS from SAQTRV where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(contract_quote_rec_id,quote_revision_record_id))

		# Product offerring[SAQTSV]
		get_service_info = Sql.GetFirst("SELECT COUNT(DISTINCT SERVICE_ID) as COUNT from SAQTSV where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(contract_quote_rec_id,quote_revision_record_id))

		# Fab Location[SAQFBL]
		get_fab_info = Sql.GetFirst("SELECT COUNT(DISTINCT FABLOCATION_ID) as COUNT from SAQFBL where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(contract_quote_rec_id,quote_revision_record_id))

		# Involved Parties[SAQTIP]
		get_involved_parties_info = Sql.GetFirst("SELECT COUNT(DISTINCT PARTY_ID) as COUNT from SAQTIP where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(contract_quote_rec_id,quote_revision_record_id))

		# Sales Team[SAQDLT]
		get_sales_team_info = Sql.GetFirst("SELECT COUNT(DISTINCT C4C_PARTNERFUNCTION_ID) as COUNT from SAQDLT where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND (C4C_PARTNERFUNCTION_ID = 'BD' OR C4C_PARTNERFUNCTION_ID = 'CONTRACT MANAGER' OR C4C_PARTNERFUNCTION_ID = 'PRICING PERSON' )".format(contract_quote_rec_id,quote_revision_record_id))

		# VC offerring[SAQTSE]
		get_complete_list = []
		get_vc_offerring_info = Sql.GetList(" SELECT  DISTINCT CONFIGURATION_STATUS,SERVICE_ID  FROM SAQSGE WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' and CONFIGURATION_STATUS = 'COMPLETE' ".format(contract_quote_rec_id,quote_revision_record_id))
		if get_vc_offerring_info:
			for val in get_vc_offerring_info:
				if  val.CONFIGURATION_STATUS:
					status = val.CONFIGURATION_STATUS
					if status == "COMPLETE" and status != "":
						get_complete_list.append('T')
					else:
						get_complete_list.append('F')
				else:
					get_complete_list.append('F')
		else:
			get_complete_list.append('F')

		# get_equip_details = Sql.GetFirst("SELECT COUNT(DISTINCT SERVICE_ID) as SERVICE_ID from SAQSCO where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(contract_quote_rec_id,quote_revision_record_id))
		# For Tool Based Quotes[SAQTSV]
		get_tool_service_info = Sql.GetList("SELECT DISTINCT SERVICE_ID as SERVICE_ID from SAQTSV(NOLOCK) where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(contract_quote_rec_id,quote_revision_record_id))

		# get_quality_required start validations#A055S000P01-18587
		get_quality_required_list = []
		get_quality_required = Sql.GetList("SELECT ISNULL(QUALITY_REQUIRED,'') as QUALITY_REQUIRED FROM SAQFBL where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(contract_quote_rec_id,quote_revision_record_id))
		if get_quality_required:
			for val in get_quality_required:
				if val.QUALITY_REQUIRED != '':
					get_quality_required_list.append('T')
				else:
					get_quality_required_list.append('F')
		else:
			get_quality_required_list.append('F')

		# get_quality_required  vlidations-end3A055S000P01-18587

		tool_check = []
		Z0110_check = []
		if 'F' in get_quality_required_list:
			update_workflow_status_conf = "UPDATE SAQTRV SET REVISION_STATUS = 'CFG-CONFIGURING',WORKFLOW_STATUS = 'CONFIGURE' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' ".format(QuoteRecordId=contract_quote_rec_id,RevisionRecordId = quote_revision_record_id)
			Sql.RunQuery(update_workflow_status_conf)
		else:
			for tserv in get_tool_service_info:

				if tserv.SERVICE_ID in ('Z0004', 'Z0004W', 'Z0009-TOOL', 'Z0010-TOOL', 'Z0035', 'Z0035W', 'Z0090', 'Z0091', 'Z0091W', 'Z0092', 'Z0092W', 'Z0099'):

					# Tools service[SAQSCO]
					get_tools_info = Sql.GetFirst("SELECT COUNT(DISTINCT SERVICE_ID) as COUNT from SAQSCO(NOLOCK) where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID = '{}' ".format(contract_quote_rec_id,quote_revision_record_id,tserv.SERVICE_ID))
					if get_tools_info:
						if get_tools_info.COUNT > 0:
							tool_check.append('T')
						else:
							tool_check.append('F')
					else:
						tool_check.append('F')

				elif str(tserv.SERVICE_ID).upper() == 'Z0110':
					tool_check.append('T')

					get_consigned_parts = Sql.GetFirst("select ENTITLEMENT_XML from SAQITE where QUOTE_RECORD_ID = '{qtid}' AND QTEREV_RECORD_ID = '{qt_rev_id}' and SERVICE_ID = '{get_service}'".format(qtid =contract_quote_rec_id,qt_rev_id=quote_revision_rec_id,get_service = str(tserv.SERVICE_ID).strip()))
					if get_consigned_parts:
						updateentXML = get_consigned_parts.ENTITLEMENT_XML
						pattern_tag = re.compile(r'(<QUOTE_ITEM_ENTITLEMENT>[\w\W]*?</QUOTE_ITEM_ENTITLEMENT>)')
						pattern_id = re.compile(r'<ENTITLEMENT_ID>AGS_[^>]*?_TSC_ONSTCP</ENTITLEMENT_ID>')
						pattern_name = re.compile(r'<ENTITLEMENT_DISPLAY_VALUE>([^>]*?)</ENTITLEMENT_DISPLAY_VALUE>')
						#consinged_part = 'True'
						for m in re.finditer(pattern_tag, updateentXML):
							sub_string = m.group(1)
							get_ent_id = re.findall(pattern_id,sub_string)
							get_ent_val= re.findall(pattern_name,sub_string)
							if get_ent_id:
								get_ent_val = get_ent_val[0]

								if get_ent_val == '$1M/site':
									#sum of the price for all parts[SAQIFP]
									get_tools_info = Sql.GetFirst("SELECT SUM(DISTINCT UNIT_PRICE) as SUM from SAQIFP(NOLOCK) where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID = '{}' ".format(contract_quote_rec_id,quote_revision_record_id,tserv.SERVICE_ID))
									if get_tools_info.SUM > '10000000':
										Z0110_check.append('T')
									else:
										Z0110_check.append('F')
				else:
					tool_check.append('T')
			# All Addon Products which require parts to be added
			get_addon_service_info = Sql.GetList("SELECT DISTINCT SERVICE_ID as SERVICE_ID from SAQSAO(NOLOCK) where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(contract_quote_rec_id,quote_revision_record_id))

			# addon check
			Addon_check = []
			for dt in get_addon_service_info:
				if str(dt.SERVICE_ID) in ['Z0100', 'Z0101', 'Z0123', 'Z0108', 'Z0110']:
					get_parts_info = Sql.GetFirst("SELECT COUNT(DISTINCT PART_NUMBER) as COUNT from SAQSPT(NOLOCK) where SAQTSV.QUOTE_RECORD_ID = '{}' AND SAQTSV.QTEREV_RECORD_ID = '{}' AND SERVICE_ID = '{}'".format(contract_quote_rec_id,quote_revision_record_id,dt.SERVICE_ID))
					if get_parts_info.COUNT > 0:
						Addon_check.append('T')
					else:
						Addon_check.append('F')
				else:
					Addon_check.append('T')
			get_workflow_statusquery = Sql.GetFirst("SELECT WORKFLOW_STATUS FROM SAQTRV where WORKFLOW_STATUS = 'CONFIGURE' AND QUOTE_RECORD_ID = '{QuoteRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' ".format(QuoteRecordId=contract_quote_rec_id,RevisionRecordId = quote_revision_record_id))
			if get_workflow_statusquery and get_workflow_statusquery.WORKFLOW_STATUS not in ("APPROVALS","LEGAL SOW","QUOTE-DOCUMENTS","CLEAN BOOKING CHECKLIST","BOOKED"):
				Trace.Write('136----')
				if str(getsalesorg_info).upper() != "NONE" and get_service_info.COUNT > 0 and get_fab_info.COUNT > 0  and get_involved_parties_info.COUNT > 0  and get_sales_team_info.COUNT > 0  and 'F' not in get_complete_list and 'F' not in tool_check and 'F' not in Z0110_check and 'F' not in Addon_check :
					update_workflow_status = "UPDATE SAQTRV SET REVISION_STATUS = 'CFG-ACQUIRING',WORKFLOW_STATUS = 'CONFIGURE' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' ".format(QuoteRecordId=contract_quote_rec_id,RevisionRecordId = quote_revision_record_id)
					Sql.RunQuery(update_workflow_status)
				# else:
					# A055S000P01-17893 start
					# error_msg = "You have incomplete configuration. Please correct all configuration errors and try again"
					# A055S000P01-17893 end
			# AO55S000P01-17018 Starts
			# get pricing status from saqico-A055S000P01-17164 start
			price_preview_status = []
			annualized_items_status = []
			item_covered_obj = Sql.GetList("SELECT DISTINCT STATUS FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(contract_quote_rec_id,quote_revision_record_id))
			if item_covered_obj:
				for status in item_covered_obj:
					annualized_items_status.append(status.STATUS)
					if status.STATUS:
						price_status = status.STATUS
						if str(price_status).upper() == "ACQUIRED":
							price_preview_status.append('T')
						else:
							price_preview_status.append('F')
					else:
						price_preview_status.append('F')
			else:
				Trace.Write("NO Quote Items")
				price_preview_status.append('F')
			annualized_items_status = list(set(annualized_items_status))
			# A055S000P01-17164 start
			get_workflow_status = Sql.GetFirst("SELECT WORKFLOW_STATUS,REVISION_STATUS FROM SAQTRV WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' ".format(contract_quote_rec_id,quote_revision_record_id))
			if get_workflow_status.WORKFLOW_STATUS not in ("APPROVALS","LEGAL SOW","QUOTE-DOCUMENTS","CLEAN BOOKING CHECKLIST","BOOKED"):
				if str(getsalesorg_info).upper() != "NONE" and get_service_info.COUNT > 0 and 'F' not in get_complete_list and 'F' not in tool_check and 'F' not in price_preview_status and Text == "COMPLETE STAGE":
					if 'PRR-ON HOLD PRICING' not in annualized_items_status and 'OFFLINE PRICING' in annualized_items_status:
						update_workflow_status = "UPDATE SAQTRV SET WORKFLOW_STATUS = 'PRICING REVIEW',REVISION_STATUS='PRR-ON HOLD PRICING' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' ".format(QuoteRecordId=contract_quote_rec_id,RevisionRecordId = quote_revision_record_id)
						Sql.RunQuery(update_workflow_status)
					else:
						update_workflow_status = "UPDATE SAQTRV SET WORKFLOW_STATUS = 'PRICING',REVISION_STATUS='PRI-PRICING' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' ".format(QuoteRecordId=contract_quote_rec_id,RevisionRecordId = quote_revision_record_id)
						#Sql.RunQuery(update_workflow_status)
						ScriptExecutor.ExecuteGlobal('CQSDELPGPN',{'QUOTE_ID':contract_quote_rec_id,'QTEREV_ID':quote_revision_record_id,'ACTION':'EMAIL'})
				if str(getsalesorg_info).upper() != "NONE" and get_service_info.COUNT > 0 and 'F' in get_complete_list and 'F' not in tool_check and 'F' not in price_preview_status and Text == "COMPLETE STAGE":
					if 'PRR-ON HOLD PRICING' not in annualized_items_status and 'OFFLINE PRICING' in annualized_items_status:
						update_workflow_status = "UPDATE SAQTRV SET WORKFLOW_STATUS = 'PRICING REVIEW',REVISION_STATUS='PRR-ON HOLD PRICING' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' ".format(QuoteRecordId=contract_quote_rec_id,RevisionRecordId = quote_revision_record_id)
						Sql.RunQuery(update_workflow_status)
					else:
						update_workflow_onhold_pricing_status = "UPDATE SAQTRV SET WORKFLOW_STATUS = 'PRICING REVIEW',REVISION_STATUS='PRR- ON HOLD PRICING' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' ".format(QuoteRecordId=contract_quote_rec_id,RevisionRecordId = quote_revision_record_id)
						Sql.RunQuery(update_workflow_onhold_pricing_status)
				if str(getsalesorg_info).upper() != "NONE" and get_service_info.COUNT > 0 and 'F' in get_complete_list and 'F' not in tool_check and 'F' in price_preview_status and Text == "COMPLETE STAGE":
					update_workflow_onhold_status = "UPDATE SAQTRV SET WORKFLOW_STATUS = 'CONFIGURE',REVISION_STATUS='CFG-ON HOLD-COSTING' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' ".format(QuoteRecordId=contract_quote_rec_id,RevisionRecordId = quote_revision_record_id)
					Sql.RunQuery(update_workflow_onhold_status)
			# A055S000P01-17164 end
			# get pricing status from saqico-A055S000P01-17164 end
			# get_workflow_status = Sql.GetFirst(" SELECT WORKFLOW_STATUS,REVISION_STATUS FROM SAQTRV WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' ".format(contract_quote_rec_id,quote_revision_record_id))
			if get_workflow_status.REVISION_STATUS == "APR-APPROVAL PENDING" and Text == "COMPLETE STAGE":
				update_workflow_status = "UPDATE SAQTRV SET WORKFLOW_STATUS = 'APPROVALS' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' ".format(QuoteRecordId=contract_quote_rec_id,RevisionRecordId = quote_revision_record_id)
				Sql.RunQuery(update_workflow_status)
			# AO55S000P01-17018 Ends
			# workflow status bar update status -- A055S000P01-17166
			get_workflow_status = Sql.GetFirst("SELECT WORKFLOW_STATUS,REVISION_STATUS,CLM_AGREEMENT_NUM FROM SAQTRV WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' ".format(contract_quote_rec_id,quote_revision_record_id))

			if get_workflow_status:
				if get_workflow_status.REVISION_STATUS == "OPD-CUSTOMER ACCEPTED":
					# A055S000P01-17165 started
					Trace.Write('205---')
					# update_legal_status = "UPDATE SAQTRV SET WORKFLOW_STATUS = 'LEGAL SOW',REVISION_STATUS ='LGL-PREPARING LEGAL SOW' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' ".format(QuoteRecordId=contract_quote_rec_id,RevisionRecordId = quote_revision_record_id)
					# Sql.RunQuery(update_legal_status)
					# A055S000P01-17165 end
					status = "GENERATE SOW"
				elif get_workflow_status.WORKFLOW_STATUS == "CONFIGURE":
					status = "CONFIGURE"
				elif get_workflow_status.WORKFLOW_STATUS == "PRICING REVIEW":
					status = "PRICING REVIEW"
				elif get_workflow_status.REVISION_STATUS == "CFG-ON HOLD - COSTING":
					status = "CFGCOST"
				elif get_workflow_status.REVISION_STATUS == "OPD-CUSTOMER REJECTED":
					status = "CUSTOMER REJECTED"
				elif get_workflow_status.WORKFLOW_STATUS == "PRICING":
					status = "PRICING"

				elif get_workflow_status.WORKFLOW_STATUS == "APPROVALS" and get_workflow_status.REVISION_STATUS not in  ("APR-APPROVED"):
					status = "APPROVALS"
				elif get_workflow_status.WORKFLOW_STATUS == "APPROVALS" and get_workflow_status.REVISION_STATUS =="APR-APPROVED":
					status = "APR-APPROVALS"
				elif get_workflow_status.WORKFLOW_STATUS == "LEGAL SOW" and get_workflow_status.REVISION_STATUS not in  ("LGL-PREPARING LEGAL SOW","LGL-LEGAL SOW ACCEPTED"):
					status = "LEGAL SOW"

				elif get_workflow_status.WORKFLOW_STATUS == "QUOTE DOCUMENTS" and get_workflow_status.REVISION_STATUS != "OPD-CUSTOMER ACCEPTED":
					status = "QUOTE DOCUMENTS"
				elif get_workflow_status.WORKFLOW_STATUS == "QUOTE DOCUMENTS" and get_workflow_status.REVISION_STATUS == "OPD-CUSTOMER ACCEPTED":
					status = "GENERATE SOW"
				elif get_workflow_status.WORKFLOW_STATUS == "LEGAL SOW" and get_workflow_status.REVISION_STATUS == "LGL-PREPARING LEGAL SOW":
					status = "COMPLETESOW"
				elif get_workflow_status.WORKFLOW_STATUS == "LEGAL SOW" and get_workflow_status.REVISION_STATUS == "LGL-LEGAL SOW ACCEPTED":
					status = "LEGAL SOW ACCEPT"
				elif get_workflow_status.WORKFLOW_STATUS == "CLEAN BOOKING CHECKLIST" and get_workflow_status.REVISION_STATUS == "CBC-CBC COMPLETED":
					status = "CBC-COMPLETED"
				elif get_workflow_status.WORKFLOW_STATUS == "CLEAN BOOKING CHECKLIST" and get_workflow_status.REVISION_STATUS not in  ("CBC-CBC COMPLETED"):
					status = "CLEAN BOOKING CHECKLIST"
				elif get_workflow_status.REVISION_STATUS == "BOK-CONTRACT BOOKED" and get_workflow_status.WORKFLOW_STATUS =="BOOKED":
					status = "BOOKEDCONTRACT"
				elif get_workflow_status.WORKFLOW_STATUS == "BOOKED" and get_workflow_status.REVISION_STATUS not in ("BOOKED"):
					status = "BOOKED"
				else:
					status = "CONFIGURE"
				CQCPQC4CWB.writeback_to_c4c("quote_header",contract_quote_rec_id,quote_revision_record_id)

				CQCPQC4CWB.writeback_to_c4c("opportunity_header",contract_quote_rec_id,quote_revision_record_id)
				if get_workflow_status.REVISION_STATUS == "LGL-PREPARING LEGAL SOW" and not get_workflow_status.CLM_AGREEMENT_NUM:
					error_msg = "You will not be able to complete the stage until the Legal SoW in CLM is executed"

			# A055S000P01-17891 start
			get_workflow_banner_msg = Sql.GetFirst("SELECT MESSAGE_TEXT from SYMSGS where  OBJECTFIELD_APINAME = '{msg_wf}' and MESSAGE_TYPE = 'WORKFLOW'".format(msg_wf=status))

			if get_workflow_banner_msg and Text == "COMPLETE STAGE":
				error_msg = get_workflow_banner_msg.MESSAGE_TEXT
			else:
				error_msg = ''

			# A055S000P01-17891 end
			if quote_item_insert == 'yes' and Text == "COMPLETE STAGE":
				service_id_query = Sql.GetList("SELECT SAQTSV.*,MAMTRL.MATERIALCONFIG_TYPE FROM SAQTSV INNER JOIN MAMTRL ON SAP_PART_NUMBER = SERVICE_ID WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(contract_quote_rec_id,quote_revision_record_id))
				if service_id_query:
					for service_id in service_id_query:
						get_ent_config_status = Sql.GetFirst(""" SELECT COUNT(CONFIGURATION_STATUS) AS COUNT FROM SAQTSE (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID = '{}' AND CONFIGURATION_STATUS='COMPLETE'""".format(contract_quote_rec_id,quote_revision_record_id,service_id.SERVICE_ID))
						if get_ent_config_status.COUNT > 0 or service_id.MATERIALCONFIG_TYPE =='SIMPLE MATERIAL' or service_id.SERVICE_ID == 'Z0117':
							data = ScriptExecutor.ExecuteGlobal("CQINSQTITM",{"ContractQuoteRecordId":contract_quote_rec_id, "ContractQuoteRevisionRecordId":quote_revision_record_id, "ServiceId":service_id.SERVICE_ID, "ActionType":'INSERT_LINE_ITEMS'})
					items_status = []
					items_obj = Sql.GetList("SELECT ISNULL(STATUS,'') as STATUS FROM SAQRIT (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' and QTEREV_RECORD_ID = '{QuoteRevisionRecordId}'".format(QuoteRecordId=contract_quote_rec_id,QuoteRevisionRecordId=quote_revision_record_id))
					if items_obj:
						items_status = [item_obj.STATUS for item_obj in items_obj]
					
					if 'CFG-ON HOLD - COSTING' in items_status:
						Sql.RunQuery("UPDATE SAQTRV SET WORKFLOW_STATUS = 'CONFIGURE',REVISION_STATUS='CFG-ON HOLD - COSTING' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' and QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' ".format(QuoteRecordId=contract_quote_rec_id,QuoteRevisionRecordId=quote_revision_record_id))
					elif 'PRR-ON HOLD PRICING' in items_status or 'OFFLINE PRICING' in items_status:
						Sql.RunQuery("UPDATE SAQTRV SET WORKFLOW_STATUS = 'PRICING REVIEW',REVISION_STATUS='PRR-ON HOLD PRICING' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' and QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' ".format(QuoteRecordId=contract_quote_rec_id,QuoteRevisionRecordId=quote_revision_record_id))			
					else:
						Sql.RunQuery("UPDATE SAQTRV SET WORKFLOW_STATUS = 'PRICING',REVISION_STATUS='PRI-PRICING' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' and QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' ".format(QuoteRecordId=contract_quote_rec_id,QuoteRevisionRecordId=quote_revision_record_id))
				try:
					##Calling the iflow for quote header writeback to cpq to c4c code starts..
					CQCPQC4CWB.writeback_to_c4c("quote_header",Quote.GetGlobal("contract_quote_record_id"),Quote.GetGlobal("quote_revision_record_id"))
					CQCPQC4CWB.writeback_to_c4c("opportunity_header",Quote.GetGlobal("contract_quote_record_id"),Quote.GetGlobal("quote_revision_record_id"))
					##Calling the iflow for quote header writeback to cpq to c4c code ends...
				except:
					pass
				#restricted for multiple calls scenario based on status
				if status not in ("GENERATE SOW","COMPLETESOW","APPROVALS","LEGAL SOW","QUOTE DOCUMENTS","BOOKED","CLEAN BOOKING CHECKLIST","LEGAL SOW ACCEPT"):

				try:
					# Calling the iflow for quote header writeback to cpq to c4c code starts..
					CQCPQC4CWB.writeback_to_c4c("quote_header",contract_quote_rec_id,quote_revision_record_id)
					CQCPQC4CWB.writeback_to_c4c("opportunity_header",contract_quote_rec_id,quote_revision_record_id)
					# Calling the iflow for quote header writeback to cpq to c4c code ends...
				except Exception:
					pass

				# restricted for multiple calls scenario based on status
				if status not in ("GENERATE SOW","COMPLETESOW","APPROVALS","LEGAL SOW","QUOTE DOCUMENTS","BOOKED","CLEAN BOOKING CHECKLIST","LEGAL SOW ACCEPT"):
					quote_line_item_obj = Sql.GetFirst("""
					SELECT
						LINE
					FROM
						SAQICO (NOLOCK)
						JOIN PRSPRV (NOLOCK) ON PRSPRV.SERVICE_ID = SAQICO.SERVICE_ID
					WHERE
						QUOTE_RECORD_ID = '{QuoteRecordId}'
						AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}'
						AND ISNULL(STATUS, '') = ''
						AND ISNULL(PRSPRV.SSCM_COST, 0) = 1
					""".format(
																QuoteRecordId=contract_quote_rec_id,QuoteRevisionRecordId=quote_revision_record_id
															))
					# added condition to restrict email trigger thrice

					if quote_line_item_obj:
						quote_revision_obj = Sql.GetFirst("SELECT QTEREV_ID,QUOTE_ID from SAQTMT where MASTER_TABLE_QUOTE_RECORD_ID = '{QuoteRecordId}'".format(QuoteRecordId=contract_quote_rec_id))
						if quote_revision_obj:
							_quote_revision_obj_quote_id = quote_revision_obj.QUOTE_ID
							_quote_revision_obj_qterev_id = quote_revision_obj.QTEREV_ID
							ScriptExecutor.ExecuteGlobal('QTPOSTACRM', {'QUOTE_ID':_quote_revision_obj_quote_id,'REVISION_ID':_quote_revision_obj_qterev_id, 'Fun_type':'cpq_to_sscm'})
							SqlHelper.GetFirst("""
								sp_executesql @T = N 'update
														A
													SET
														A.STATUS = (
															CASE
																WHEN A.STATUS = '' ERROR '' THEN '' ERROR ''
																WHEN A.STATUS = '' PARTIALLY PRICED '' THEN '' ERROR ''
															END
														)
													from
														SAQRIT A
														inner join (
															select
																SERVICE_ID,
																LINE,
																SAQICO.QUOTE_ID
															from
																SAQICO
															WHERE
																SAQICO.QUOTE_ID = ''{}''
															group by
																SERVICE_ID,
																LINE,
																SAQICO.QUOTE_ID
															Having
																count(*) > 1
														) as od on od.LINE = A.LINE
														AND od.SERVICE_ID = A.SERVICE_ID'
												   """.format(_quote_revision_obj_quote_id))

							SqlHelper.GetFirst("""
								sp_executesql @T=N'update
														A
													SET
														A.STATUS = (
															CASE
																WHEN A.STATUS = '' ACQUIRING '' THEN '' ACQUIRING ''
																WHEN A.STATUS = '' ERROR '' THEN '' ERROR ''
															END
														)
													from
														SAQRIT A
														inner join (
															select
																SERVICE_ID,
																LINE,
																SAQICO.QUOTE_ID
															from
																SAQICO
															WHERE
																SAQICO.QUOTE_ID = '' {} ''
															group by
																SERVICE_ID,
																LINE,
																SAQICO.QUOTE_ID
															Having
																count(*) > 1
														) as od on od.LINE = A.LINE
														AND od.SERVICE_ID = A.SERVICE_ID'""".format(_quote_revision_obj_quote_id))

							SqlHelper.GetFirst("""
									sp_executesql @T=N'update
															A
														SET
															A.STATUS = (
																CASE
																	WHEN A.STATUS = '' ACQUIRING '' THEN '' PARTIALLY PRICING ''
																	WHEN A.STATUS = '' PARTIALLY PRICING '' THEN '' PARTIALLY PRICING ''
																END
															)
														from
															SAQRIT A
															inner join (
																select
																	SERVICE_ID,
																	LINE,
																	SAQICO.QUOTE_ID
																from
																	SAQICO
																WHERE
																	SAQICO.QUOTE_ID = '' {} ''
																group by
																	SERVICE_ID,
																	LINE,
																	SAQICO.QUOTE_ID
																Having
																	count(*) > 1
															) as od on od.LINE = A.LINE
															AND od.SERVICE_ID = A.SERVICE_ID'""".format(_quote_revision_obj_quote_id))

				# Pricing Calculation - End

				# calling the iflow for pricing start..
				try:
					contract_quote_obj = Sql.GetFirst("SELECT QUOTE_ID FROM SAQTMT (NOLOCK) WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{QuoteRecordId}'".format(QuoteRecordId=contract_quote_rec_id))
					contract_quote_id = getattr(contract_quote_obj, "QUOTE_ID", '')
					count=sql_get_first("SELECT COUNT(*) AS CNT FROM SAQSPT WHERE QUOTE_ID= '{}' and CUSTOMER_ANNUAL_QUANTITY IS NOT NULL".format(contract_quote_id))
					if not count.CNT:
						CQPARTIFLW.iflow_pricing_call(User.UserName,contract_quote_id, quote_revision_record_id)
				except:
					Log.Info("PART PRICING IFLOW ERROR!")
				# calling the iflow for pricing end
	Trace.Write('status--297---------'.format(status))
	return status,error_msg


# A055S000P01-17166 start
def complete_sow_update():
	sql_run_query("""
					UPDATE
						SAQTRV
					SET
						WORKFLOW_STATUS = 'LEGAL SOW',
						REVISION_STATUS = 'LGL-LEGAL SOW ACCEPTED'
					where
						QUOTE_RECORD_ID = '{contract_quote_rec_id}'
						AND QTEREV_RECORD_ID = '{quote_revision_rec_id}'
					""".format(contract_quote_rec_id=contract_quote_rec_id,quote_revision_rec_id=quote_revision_record_id))

	CQCPQC4CWB.writeback_to_c4c("quote_header",contract_quote_rec_id,quote_revision_record_id)
	CQCPQC4CWB.writeback_to_c4c("opportunity_header",contract_quote_rec_id,quote_revision_record_id)

	return True


def create_sow_update():
	sql_run_query("""
				UPDATE
					SAQTRV
				SET
					WORKFLOW_STATUS = 'LEGAL SOW',
					REVISION_STATUS = 'LGL-PREPARING LEGAL SOW'
				where
					QUOTE_RECORD_ID = '{contract_quote_rec_id}'
					AND QTEREV_RECORD_ID = '{quote_revision_rec_id}'
				""".format(contract_quote_rec_id=contract_quote_rec_id,quote_revision_rec_id=quote_revision_record_id))

	return True
	# A055S000P01-17166 end


try:
	quote_item_insert = Param.quote_item_insert
except:
	quote_item_insert = ''

try:
    quote_item_insert = Param.quote_item_insert
except:
    quote_item_insert = ''

try:
    Text = Param.Text
except:
    Text = ""

try:
    quote_id_val = Param.QUOTE_ID
except:
    quote_id_val = ""

try:
    quote_rev_id_val = Param.REVISION_ID
except:
    quote_rev_id_val = ""
try:
    STATUS_SOW = Param.STATUS
except:
    STATUS_SOW = ""

if STATUS_SOW == "SOW_ACCEPT":
	ApiResponse = ApiResponseFactory.JsonResponse(complete_sow_update())
elif STATUS_SOW == "CREATE_SOW":
	ApiResponse = ApiResponseFactory.JsonResponse(create_sow_update())
else:
	Trace.Write("quote_item_insert_J "+str(quote_item_insert))
	ApiResponse = ApiResponseFactory.JsonResponse(Dynamic_Status_Bar(quote_item_insert,Text))

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


quote_revision_rec_id = Quote.GetGlobal("quote_revision_record_id")
user_id = str(User.Id)
user_name = str(User.UserName) 

def Dynamic_Status_Bar(quote_item_insert,Text):

	if str(Text) == 'COMPLETE STAGE' and (str(TabName) == "Quotes" or str(TabName) == "Quote") and current_prod == "Sales":

		#Salesorg[SAQTRV]
		getsalesorg_info = Sql.GetFirst("SELECT SALESORG_ID,REVISION_STATUS from SAQTRV where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id))

		#Product offerring[SAQTSV] 
		get_service_info = Sql.GetFirst("SELECT COUNT(DISTINCT SERVICE_ID) as COUNT from SAQTSV where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id))

		#Fab Location[SAQFBL]
		get_fab_info = Sql.GetFirst("SELECT COUNT(DISTINCT FABLOCATION_ID) as COUNT from SAQFBL where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id))

		#Involved Parties[SAQTIP] 
		get_involved_parties_info = Sql.GetFirst("SELECT COUNT(DISTINCT PARTY_ID) as COUNT from SAQTIP where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id))

		#Sales Team[SAQDLT]
		get_sales_team_info = Sql.GetFirst("SELECT COUNT(DISTINCT C4C_PARTNERFUNCTION_ID) as COUNT from SAQDLT where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND (C4C_PARTNERFUNCTION_ID = 'BD' OR C4C_PARTNERFUNCTION_ID = 'CONTRACT MANAGER' OR C4C_PARTNERFUNCTION_ID = 'PRICING PERSON' )".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id))
		
		#VC offerring[SAQTSE]
		get_vc_offerring_info = Sql.GetList(" SELECT COUNT(DISTINCT SERVICE_ID) as COUNT   FROM SAQTSE WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' and CONFIGURATION_STATUS = 'COMPLETE' ".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id))
		
		#For Tool Based Quotes[SAQTSV]		
		get_tool_service_info = Sql.GetList("SELECT DISTINCT SERVICE_ID as SERVICE_ID from SAQTSV(NOLOCK) where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id))
		
		tool_check = []
		Z0110_check = []
		
		for tserv in get_tool_service_info:
		
			if str(tserv.SERVICE_ID) in ('Z0004', 'Z0004W', 'Z0009-TOOL', 'Z0010-TOOL', 'Z0035', 'Z0035W', 'Z0090', 'Z0091', 'Z0091W', 'Z0092', 'Z0092W', 'Z0099'):
			
				#Tools service[SAQSCO]
				get_tools_info = Sql.GetFirst("SELECT COUNT(DISTINCT SERVICE_ID) as COUNT from SAQSCO(NOLOCK) where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID = '{}' ".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id),str(tserv.SERVICE_ID))
				
				if get_tools_info.COUNT > 0:				
					tool_check.append('T')				
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
					consinged_part = 'True'
					for m in re.finditer(pattern_tag, updateentXML):
						sub_string = m.group(1)
						get_ent_id = re.findall(pattern_id,sub_string)
						get_ent_val= re.findall(pattern_name,sub_string)
						if get_ent_id:							
							get_ent_val = str(get_ent_val[0])
							
							if str(get_ent_val) == '$1M/site':
								#sum of the price for all parts[SAQIFP]
								get_tools_info = Sql.GetFirst("SELECT SUM(DISTINCT UNIT_PRICE) as SUM from SAQIFP(NOLOCK) where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID = '{}' ".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id),str(tserv.SERVICE_ID))
								if get_tools_info.SUM > '10000000':
									Z0110_check.append('T')
								else:
									Z0110_check.append('F')
			
			else:
				tool_check.append('T')
		
		
		#All Addon Products which require parts to be added
		get_addon_service_info = Sql.GetList("SELECT DISTINCT SERVICE_ID as SERVICE_ID from SAQSAO(NOLOCK) where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id))
		
		
		Addon_check = []
		
		for dt in get_addon_service_info:			
			
			if str(dt.SERVICE_ID) in ['Z0100', 'Z0101', 'Z0123', 'Z0108', 'Z0110'] :
			
			
				get_parts_info = Sql.GetFirst("SELECT COUNT(DISTINCT PART_NUMBER) as COUNT from SAQSPT(NOLOCK) where SAQTSV.QUOTE_RECORD_ID = '{}' AND SAQTSV.QTEREV_RECORD_ID = '{}' AND SERVICE_ID = '{}'".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id),str(dt.SERVICE_ID))
				
				
				if get_parts_ifno.COUNT > 0:
					Addon_check.append('T')	
				else:
					Addon_check.append('F')					
				
			else:
				Addon_check.append('T')				
			
	

		if str(getsalesorg_info).upper() != "NONE" and get_service_info.COUNT > 0 and get_fab_info.COUNT > 0  and get_involved_parties_info.COUNT > 0  and get_sales_team_info.COUNT > 0  and get_vc_offerring_info.COUNT > 0  and 'F' not in tool_check and 'F' not in Z0110_check and 'F' not in Addon_check:
			
			update_workflow_status = "UPDATE SAQTRV SET REVISION_STATUS = 'CFG-ACQUIRING' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' ".format(QuoteRecordId=Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"))			
			
			Sql.RunQuery(update_workflow_status)


try:
	quote_item_insert = Param.quote_item_insert
except:
	quote_item_insert = ''

try:
	Text = Param.Text
except:
	Text = ""

ApiResponse = ApiResponseFactory.JsonResponse(Dynamic_Status_Bar(quote_item_insert,Text))
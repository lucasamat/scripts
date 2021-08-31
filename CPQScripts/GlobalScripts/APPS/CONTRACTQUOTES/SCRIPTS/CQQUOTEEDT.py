# =========================================================================================================================================
#   __script_name : CQQUOTEEDT.PY
#   __script_description : THIS SCRIPT IS USED LOAD THE QUOTE Information
#   __primary_author__ :
#   __create_date : 06/09/2021
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct
Trace = Trace
Param = Param
Log = Log
ApiResponseFactory = ApiResponseFactory
import re
#import time
from SYDATABASE import SQL
Sql = SQL()


def bannerdetails(Quoteid,active_tab_name):	
	contract_record_id = ""
	get_contract_rec_id = ""
	matchObj = re.match( r'.*>\s*[A-Z]{1,2}(\d+)[A-Z]{1,2}[^>]*?\-', Quoteid)	
	if active_tab_name == "Contracts":
		reObj = re.match( r'.*>\s*(\d+)*?<', Quoteid)		
		SQLObj = Sql.GetFirst("SELECT QUOTE_ID FROM SAQTMT (NOLOCK) WHERE CRM_CONTRACT_ID='" + str(reObj.group(1)) + "'")
		##assigning contract rec id globally starts
		get_contract_rec_id = Sql.GetFirst("SELECT CONTRACT_RECORD_ID FROM CTCNRT (NOLOCK) WHERE CONTRACT_ID='" + str(reObj.group(1)) + "'")
		if get_contract_rec_id:
			contract_record_id = str(get_contract_rec_id.CONTRACT_RECORD_ID)			
		###ends
		Quoteid = SQLObj.QUOTE_ID
		matchObj = re.match( r'^\s*[A-Z]{1,2}(\d+)[A-Z]{1,2}[^>]*?\-', Quoteid)
	if active_tab_name == "Quotes":
		Trace.Write('34-----')
		SQLObj = Sql.GetFirst("SELECT QUOTE_ID FROM SAQTMT (NOLOCK) WHERE CRM_CONTRACT_ID='" + str(reObj.group(1)) + "'")
	if Quoteid is not None and str(Quoteid) !='':
		if matchObj:
			qid=str(matchObj.group(1))
			Trace.Write('34--qid---'+str(qid))			
			Quote = QuoteHelper.Edit(str(qid))				
			Quote.RefreshActions()			
			##getting contarct rec id as global
			if contract_record_id:
				Quote.SetGlobal("contract_record_id",contract_record_id)
				#test = Quote.GetGlobal("contract_record_id")				
			##ends
			return Quote.CompositeNumber

try:
	Quoteid = Param.Quoteid
	active_tab_name = Param.CurrentTab
except:
	Quoteid=''
ApiResponse = ApiResponseFactory.JsonResponse(bannerdetails(Quoteid,active_tab_name))
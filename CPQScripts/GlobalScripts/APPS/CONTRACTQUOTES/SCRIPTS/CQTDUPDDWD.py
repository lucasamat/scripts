# =========================================================================================================================================
#   __script_name : CQTDUPDDWD.PY
#   __script_description : THIS SCRIPT IS USED TO UPLOAD AND DOWMLOAD TABLE DATA
#   __primary_author__ : AYYAPPAN SUBRAMANIYAN
#   __create_date :23-12-2021
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================

import re
import sys
import datetime
import Webcom.Configurator.Scripting.Test.TestProduct
import System.Net
from SYDATABASE import SQL

Sql = SQL()

class ContractQuoteDownloadTableData:
	def __init__(self, **kwargs):		
		self.user_id = str(User.Id)
		self.user_name = str(User.UserName)		
		self.datetime_value = datetime.datetime.now()		
		self.action_type = kwargs.get('action_type')		
		self.source_object_name = ''	
		self.set_contract_quote_related_details()
		
	def set_contract_quote_related_details(self):
		try:
			self.contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
		except Exception:
			self.contract_quote_record_id = ''	
		try:
			self.contract_quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
		except Exception:
			self.contract_quote_revision_record_id = ''
		contract_quote_obj = Sql.GetFirst("SELECT QUOTE_ID, QUOTE_TYPE, SALE_TYPE, C4C_QUOTE_ID, QTEREV_ID, QUOTE_CURRENCY, QUOTE_CURRENCY_RECORD_ID FROM SAQTMT (NOLOCK) WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{QuoteRecordId}'".format(QuoteRecordId=self.contract_quote_record_id))
		if contract_quote_obj:
			self.contract_quote_id = contract_quote_obj.QUOTE_ID
			self.contract_quote_revision_id = contract_quote_obj.QTEREV_ID				
		else:
			self.contract_quote_id = ''
			self.contract_quote_revision_id = ''
		return True

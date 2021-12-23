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
		self.related_list_attr_name = kwargs.get('related_list_attr_name')	
		self.source_object_name = ''	
		self.tree_param = Quote.GetGlobal("TreeParam")
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
		contract_quote_obj = Sql.GetFirst("SELECT QUOTE_ID, QUOTE_TYPE, QTEREV_ID FROM SAQTMT (NOLOCK) WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{QuoteRecordId}'".format(QuoteRecordId=self.contract_quote_record_id))
		if contract_quote_obj:
			self.contract_quote_id = contract_quote_obj.QUOTE_ID
			self.contract_quote_revision_id = contract_quote_obj.QTEREV_ID				
		else:
			self.contract_quote_id = ''
			self.contract_quote_revision_id = ''
		return True
	
	def _do_opertion(self):
		table_columns = []
		table_records = []
		related_list_obj = Sql.GetFirst(
			"""SELECT SYOBJR.RECORD_ID, SYOBJR.SAPCPQ_ATTRIBUTE_NAME, SYOBJR.PARENT_LOOKUP_REC_ID, SYOBJR.OBJ_REC_ID, SYOBJR.NAME, SYOBJR.COLUMN_REC_ID, SYOBJR.COLUMNS, SYOBJH.OBJECT_NAME
				FROM SYOBJR (NOLOCK) 
				INNER JOIN SYOBJH (NOLOCK) ON SYOBJH.RECORD_ID = SYOBJR.OBJ_REC_ID
				WHERE SYOBJR.SAPCPQ_ATTRIBUTE_NAME = '{AttributeName}'
				""".format(	AttributeName=self.related_list_attr_name)
		)
		if related_list_obj:
			Trace.Write("==========>>>>")
			table_columns = eval(related_list_obj.COLUMNS)
			columns = related_list_obj.COLUMNS.replace("'","")[1:-1]
			Trace.Write("""
						SELECT {Columns}
						FROM {TableName} (NOLOCK)
						WHERE QUOTE_RECORD_ID ='{QuoteRecordId}' AND QTEREV_RECORD_ID='{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}' FOR JSON AUTO""".format(Columns=columns, TableName=related_list_obj.OBJECT_NAME, QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.tree_param))
			records_json_obj = Sql.RunQuery("""
											SELECT TOP 5 {Columns}
											FROM {TableName} (NOLOCK)
											WHERE QUOTE_RECORD_ID ='{QuoteRecordId}' AND QTEREV_RECORD_ID='{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}' FOR JSON AUTO""".format(Columns=columns, TableName=related_list_obj.OBJECT_NAME, QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.tree_param))
			if records_json_obj:
				for record_json_obj in records_json_obj:
					try:
						table_records = eval(record_json_obj.Value)
					except Exception:
						table_records = record_json_obj.Value
		return table_columns, table_records		

parameters = {'related_list_attr_name':Param.RelatedListAttributeName, 'action_type':Param.ActionType}
contract_quote_download_table_data_obj = ContractQuoteDownloadTableData(**parameters)
ApiResponse = ApiResponseFactory.JsonResponse(contract_quote_download_table_data_obj._do_opertion())
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
		self.object_name = ''	
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

	def get_results(self, table_total_rows=0, colums='*'):
		#for offset_skip_count in range(1, table_total_rows, 1000):
		start = 1
		end = 1000
		while end <= table_total_rows:
			query_string_with_pagination = """
							SELECT DISTINCT {Columns} FROM (
								SELECT DISTINCT {Columns}, ROW_NUMBER()OVER(ORDER BY CpqTableEntryId) AS SNO FROM (
									SELECT DISTINCT {Columns}, CpqTableEntryId
									FROM {TableName} (NOLOCK)
									WHERE QUOTE_RECORD_ID ='{QuoteRecordId}' AND QTEREV_RECORD_ID='{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}'
									) IQ)OQ
							WHERE SNO>={Skip_Count} AND SNO<={Fetch_Count}              
							""".format(Columns=colums, TableName=self.object_name, QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.tree_param, Skip_Count=start, Fetch_Count=end)

			table_data = Sql.GetList(query_string_with_pagination)

			if table_data is not None:
				for row_data in table_data:
					data = [row_obj.Value for row_obj in row_data]					
					yield data
			start += 1000			
			if end > table_total_rows:
				end = table_total_rows
			else:
				end += 1000
			Trace.Write(str(start)+" Start===> End"+str(end))

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
			table_columns = eval(related_list_obj.COLUMNS)
			columns = related_list_obj.COLUMNS.replace("'","")[1:-1]			
			self.object_name = related_list_obj.OBJECT_NAME
			total_count_obj = Sql.GetFirst("""
											SELECT COUNT(*) as count
											FROM {TableName} (NOLOCK)
											WHERE QUOTE_RECORD_ID ='{QuoteRecordId}' AND QTEREV_RECORD_ID='{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}'""".format(TableName=self.object_name, QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.tree_param))
			if total_count_obj:
				table_total_rows = total_count_obj.count

				if table_total_rows:
					table_records = [data for data in self.get_results(table_total_rows, columns)]
				
		return table_columns, table_records		
	
	# def _do_opertion(self):
	# 	table_columns = []
	# 	table_records = []
	# 	related_list_obj = Sql.GetFirst(
	# 		"""SELECT SYOBJR.RECORD_ID, SYOBJR.SAPCPQ_ATTRIBUTE_NAME, SYOBJR.PARENT_LOOKUP_REC_ID, SYOBJR.OBJ_REC_ID, SYOBJR.NAME, SYOBJR.COLUMN_REC_ID, SYOBJR.COLUMNS, SYOBJH.OBJECT_NAME
	# 			FROM SYOBJR (NOLOCK) 
	# 			INNER JOIN SYOBJH (NOLOCK) ON SYOBJH.RECORD_ID = SYOBJR.OBJ_REC_ID
	# 			WHERE SYOBJR.SAPCPQ_ATTRIBUTE_NAME = '{AttributeName}'
	# 			""".format(	AttributeName=self.related_list_attr_name)
	# 	)
	# 	if related_list_obj:
	# 		Trace.Write("==========>>>>")
	# 		table_columns = eval(related_list_obj.COLUMNS)
	# 		columns = related_list_obj.COLUMNS.replace("'","")[1:-1]
	# 		Trace.Write("""
	# 					SELECT {Columns}
	# 					FROM {TableName} (NOLOCK)
	# 					WHERE QUOTE_RECORD_ID ='{QuoteRecordId}' AND QTEREV_RECORD_ID='{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}' FOR JSON AUTO""".format(Columns=columns, TableName=related_list_obj.OBJECT_NAME, QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.tree_param))
	# 		records_json_obj = Sql.RunQuery("""
	# 										SELECT TOP 5 {Columns}
	# 										FROM {TableName} (NOLOCK)
	# 										WHERE QUOTE_RECORD_ID ='{QuoteRecordId}' AND QTEREV_RECORD_ID='{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}' FOR JSON AUTO""".format(Columns=columns, TableName=related_list_obj.OBJECT_NAME, QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.tree_param))
	# 		if records_json_obj:
	# 			for record_json_obj in records_json_obj:
	# 				try:
	# 					table_records = eval(record_json_obj.Value)
	# 				except Exception:
	# 					table_records = record_json_obj.Value
	# 	return table_columns, table_records		

parameters = {'related_list_attr_name':Param.RelatedListAttributeName, 'action_type':Param.ActionType}
contract_quote_download_table_data_obj = ContractQuoteDownloadTableData(**parameters)
ApiResponse = ApiResponseFactory.JsonResponse(contract_quote_download_table_data_obj._do_opertion())
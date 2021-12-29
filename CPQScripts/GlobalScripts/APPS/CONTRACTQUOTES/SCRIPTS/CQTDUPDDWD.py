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

class ContractQuoteSpareOpertion:

	def __init__(self, **kwargs):		
		self.user_id = str(User.Id)
		self.user_name = str(User.UserName)		
		self.datetime_value = datetime.datetime.now()		
		self.action_type = kwargs.get('action_type')	
		self.related_list_attr_name = kwargs.get('related_list_attr_name')	
		self.object_name = ''	
		self.tree_param = Quote.GetGlobal("TreeParam")
		self.upload_data = kwargs.get('upload_data')
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


class ContractQuoteDownloadTableData(ContractQuoteSpareOpertion):	

	def __init__(self, **kwargs):
		ContractQuoteSpareOpertion.__init__(self,  **kwargs)

	def get_results(self, table_total_rows=0, colums='*'):		
		start = 1
		end = 1000
		while start < table_total_rows:
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
			end += 1000			
			if end > table_total_rows:
				end = table_total_rows			

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

class ContractQuoteUploadTableData(ContractQuoteSpareOpertion):	

	def __init__(self, **kwargs):
		ContractQuoteSpareOpertion.__init__(self,  **kwargs)
		self.columns = ""
		self.records = ""

	def _insert_spare_parts(self):
		Sql.RunQuery("""INSERT SAQSPT ({DynamicColumns}, QUOTE_ID, QUOTE_NAME, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, QUOTE_SERVICE_PART_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified)
				SELECT OQ.*, '{QuoteId}' as QUOTE_ID, '{QuoteName}' as QUOTE_NAME, '{QuoteRecordId}' as QUOTE_RECORD_ID, '{QuoteRevisionId}' as QTEREV_ID, '{QuoteRevisionRecordId}' as QTEREV_RECORD_ID, '{ServiceDescription}' as SERVICE_DESCRIPTION, '{ServiceId}' as SERVICE_ID, '{ServiceRecordId}' as SERVICE_RECORD_ID, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_PART_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED,{UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
				SELECT DISTINCT					
						{DynamicColumns}	
				FROM 
					(VALUES {Records}) AS Temp({DynamicColumns})					
				) OQ
				""".format(UserId=self.user_id, UserName=self.user_name, QuoteId=self.contract_quote_id, QuoteName='', QuoteRecordId=self.contract_quote_record_id, QuoteRevisionId=self.contract_quote_revision_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceDescription='', ServiceId=self.tree_param, ServiceRecordId='', DynamicColumns=self.columns, Records=self.records)
			)
	
	def _do_opertion(self):
		for sheet_data in self.upload_data:	
			if not sheet_data.Value:	
				break	
			data = list(sheet_data.Value)
			if data:
				self.columns = ",".join(data[0])
				Trace.Write("data ==>>> "+str(data[1:]))
				self.records = ",".join([str(tuple(spare_record)) for spare_record in data[1:]])
			# for index, data in enumerate(list(sheet_data.Value)):
			# 	if index == 0:
			# 		self.columns = ",".join(data)
			# 		continue
			# 	self.records.append(tuple(data))
			# 	Trace.Write("data ====>>> "+str(list(data)))
		self._insert_spare_parts()
		return "Import Success"


def Factory(node=None):
	"""Factory Method"""
	models = {
		"Download": ContractQuoteDownloadTableData,		
		"Upload": ContractQuoteUploadTableData,
	}
	return models[node]

parameters = {'related_list_attr_name':Param.RelatedListAttributeName, 'action_type':Param.ActionType}
try:
	parameters['upload_data'] = Param.UploadData
except Exception:
	parameters['upload_data'] = []
process_object = Factory(parameters.get('action_type'))(**parameters)
#contract_quote_download_table_data_obj = ContractQuoteDownloadTableData(**parameters)
ApiResponse = ApiResponseFactory.JsonResponse(process_object._do_opertion())
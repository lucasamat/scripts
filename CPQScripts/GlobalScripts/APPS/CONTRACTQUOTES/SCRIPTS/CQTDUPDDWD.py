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
#import SYCNGEGUID as CPQID
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
		#source_object_primary_key_column_obj = Sql.GetFirst("SELECT RECORD_NAME FROM SYOBJH (NOLOCK) WHERE OBJECT_NAME = '{}'".format(self.object_name))
				
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
			table_columns = eval(related_list_obj.COLUMNS)[1:]
			columns = ",".join(table_columns)		
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
		datetime_string = self.datetime_value.strftime("%d%m%Y%H%M%S")
		spare_parts_temp_table_name = "SAQSPT_BKP_{}_{}".format(self.contract_quote_id, datetime_string)		
		try:
			spare_parts_temp_table_drop = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(spare_parts_temp_table_name)+"'' ) BEGIN DROP TABLE "+str(spare_parts_temp_table_name)+" END  ' ")			
			
			spare_parts_temp_table_bkp = SqlHelper.GetFirst("sp_executesql @T=N'SELECT "+str(self.columns)+" INTO "+str(spare_parts_temp_table_name)+" FROM (SELECT DISTINCT "+str(self.columns)+" FROM (VALUES "+str(self.records)+") AS TEMP("+str(self.columns)+")) OQ ' ")
			
			spare_parts_existing_records_delete = SqlHelper.GetFirst("sp_executesql @T=N'DELETE FROM SAQSPT WHERE QUOTE_RECORD_ID = ''"+str(self.contract_quote_record_id)+"'' AND QTEREV_RECORD_ID = ''"+str(self.contract_quote_revision_record_id)+"'' ' ")

			Sql.RunQuery("""
							INSERT SAQSPT (QUOTE_SERVICE_PART_RECORD_ID, BASEUOM_ID, BASEUOM_RECORD_ID, CUSTOMER_PART_NUMBER, CUSTOMER_PART_NUMBER_RECORD_ID, DELIVERY_MODE, EXTENDED_UNIT_PRICE, PART_DESCRIPTION, PART_NUMBER, PART_RECORD_ID, PRDQTYCON_RECORD_ID, CUSTOMER_ANNUAL_QUANTITY, QUOTE_ID, QUOTE_NAME, QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,SALESORG_ID, SALESORG_RECORD_ID, SALESUOM_CONVERSION_FACTOR, SALESUOM_ID, SALESUOM_RECORD_ID, SCHEDULE_MODE, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, UNIT_PRICE, MATPRIGRP_ID, MATPRIGRP_RECORD_ID, DELIVERY_INTERVAL, VALID_FROM_DATE, VALID_TO_DATE,PAR_SERVICE_DESCRIPTION,PAR_SERVICE_ID,PAR_SERVICE_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED)
							SELECT DISTINCT
								CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_PART_RECORD_ID,
								BASEUOM_ID,
								BASEUOM_RECORD_ID,
								CUSTOMER_PART_NUMBER,
								CUSTOMER_PART_NUMBER_RECORD_ID,
								DELIVERY_MODE,
								EXTENDED_UNIT_PRICE,
								PART_DESCRIPTION,
								PART_NUMBER,
								PART_RECORD_ID,
								PRDQTYCON_RECORD_ID,
								QUANTITY,
								QUOTE_ID,
								QUOTE_NAME,
								QUOTE_RECORD_ID,
								QTEREV_ID,
								QTEREV_RECORD_ID,
								SALESORG_ID,
								SALESORG_RECORD_ID,
								SALESUOM_CONVERSION_FACTOR,
								SALESUOM_ID,
								SALESUOM_RECORD_ID, 
								SCHEDULE_MODE,
								SERVICE_DESCRIPTION,
								SERVICE_ID,
								SERVICE_RECORD_ID,
								UNIT_PRICE,
								MATPRIGRP_ID,
								MATPRIGRP_RECORD_ID,
								DELIVERY_INTERVAL,
								VALID_FROM_DATE, 
								VALID_TO_DATE,
								PAR_SERVICE_DESCRIPTION,
								PAR_SERVICE_ID,
								PAR_SERVICE_RECORD_ID,
								{UserId} as CPQTABLEENTRYADDEDBY, 
								GETDATE() as CPQTABLEENTRYDATEADDED
							FROM (
							SELECT 
								DISTINCT
								MAMTRL.UNIT_OF_MEASURE as BASEUOM_ID,
								MAMTRL.UOM_RECORD_ID as BASEUOM_RECORD_ID,
								MAMTRL.SAP_PART_NUMBER as CUSTOMER_PART_NUMBER,
								MAMTRL.MATERIAL_RECORD_ID as CUSTOMER_PART_NUMBER_RECORD_ID,
								'ONSITE' as DELIVERY_MODE,
								0.00 as EXTENDED_UNIT_PRICE,
								MAMTRL.SAP_DESCRIPTION as PART_DESCRIPTION,
								MAMTRL.SAP_PART_NUMBER as PART_NUMBER,
								MAMTRL.MATERIAL_RECORD_ID as PART_RECORD_ID,
								'' as PRDQTYCON_RECORD_ID,
								TEMP_TABLE.CUSTOMER_ANNUAL_QUANTITY as QUANTITY,
								SAQTMT.QUOTE_ID as QUOTE_ID,
								SAQTMT.QUOTE_NAME as QUOTE_NAME,
								SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID as QUOTE_RECORD_ID,
								SAQTMT.QTEREV_ID as QTEREV_ID,
								SAQTMT.QTEREV_RECORD_ID as QTEREV_RECORD_ID,
								SAQTSV.SALESORG_ID as SALESORG_ID,
								SAQTSV.SALESORG_RECORD_ID as SALESORG_RECORD_ID,
								0.00 as SALESUOM_CONVERSION_FACTOR,
								MAMTRL.UNIT_OF_MEASURE as SALESUOM_ID,
								MAMTRL.UOM_RECORD_ID as SALESUOM_RECORD_ID, 
								'SCHEDULED' as SCHEDULE_MODE,
								SAQTSV.SERVICE_DESCRIPTION as SERVICE_DESCRIPTION,
								SAQTSV.SERVICE_ID as SERVICE_ID,
								SAQTSV.SERVICE_RECORD_ID as SERVICE_RECORD_ID,
								0.00 as UNIT_PRICE,
								MAMSOP.MATPRIGRP_ID as MATPRIGRP_ID,
								MAMSOP.MATPRIGRP_RECORD_ID as MATPRIGRP_RECORD_ID,
								'MONTHLY' as DELIVERY_INTERVAL,
								SAQTMT.CONTRACT_VALID_FROM as VALID_FROM_DATE, 
								SAQTMT.CONTRACT_VALID_TO as VALID_TO_DATE,
								SAQTSV.PAR_SERVICE_DESCRIPTION as PAR_SERVICE_DESCRIPTION,
								SAQTSV.PAR_SERVICE_ID as PAR_SERVICE_ID,
								SAQTSV.PAR_SERVICE_RECORD_ID as PAR_SERVICE_RECORD_ID
							FROM {TempTable} TEMP_TABLE(NOLOCK)
							JOIN MAMTRL (NOLOCK) ON MAMTRL.SAP_PART_NUMBER = TEMP_TABLE.PART_NUMBER
							JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = TEMP_TABLE.QUOTE_RECORD_ID
							JOIN SAQTSV (NOLOCK) ON SAQTSV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SAQTSV.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID AND SAQTSV.SERVICE_ID = '{ServiceId}'
							JOIN MAMSOP (NOLOCK) ON MAMSOP.MATERIAL_RECORD_ID = MAMTRL.MATERIAL_RECORD_ID AND MAMSOP.SALESORG_RECORD_ID = SAQTSV.SALESORG_RECORD_ID
							WHERE TEMP_TABLE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND TEMP_TABLE.QTEREV_RECORD_ID = '{RevisionRecordId}' AND MAMTRL.PRODUCT_TYPE IS NULL AND MAMTRL.IS_SPARE_PART = 1 AND MAMSOP.MATERIALSTATUS_ID <> '05') IQ
							""".format(
										TempTable=spare_parts_temp_table_name,
										ServiceId=self.tree_param,									
										QuoteRecordId=self.contract_quote_record_id,
										RevisionRecordId=self.contract_quote_revision_record_id,
										UserId=self.user_id
									)
			)
			spare_parts_temp_table_drop = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(spare_parts_temp_table_name)+"'' ) BEGIN DROP TABLE "+str(spare_parts_temp_table_name)+" END  ' ")
		except Exception:
			spare_parts_temp_table_drop = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(spare_parts_temp_table_name)+"'' ) BEGIN DROP TABLE "+str(spare_parts_temp_table_name)+" END  ' ")		
	def _validate_records(self, record_list_obj=None):
		if record_list_obj:
			pass

	def _do_opertion(self):
		for sheet_data in self.upload_data:	
			if not sheet_data.Value:	
				break	
			xls_spare_records = list(sheet_data.Value)
			if xls_spare_records:
				header = list(xls_spare_records[0]) + ['QUOTE_RECORD_ID','QTEREV_RECORD_ID']
				self.columns = ",".join(header)
				modified_records = []
				for spare_record in xls_spare_records[1:]:
					modified_records.append(str(tuple([float(spare_val) if type(spare_val) == "<type 'Decimal'>" else spare_val for spare_val in spare_record])))


				#self.records = ', '.join(map(str, modified_records)).replace("None","null").replace("'","''")
				self.records = ', '.join(map(str, [str(tuple(list(spare_record)+[self.contract_quote_record_id, self.contract_quote_revision_record_id])) for spare_record in xls_spare_records[1:]])).replace("None","null").replace("'","''")
				self.records = self.records.replace("True","1").replace("False","0")
				self.records = re.sub(r"<?[a-zA-Z0-9_.\[ \]]+>", "0.00", self.records)
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
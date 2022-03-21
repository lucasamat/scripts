# =========================================================================================================================================
#   __script_name : CQTDUPDDWD.PY
#   __script_description : THIS SCRIPT IS USED TO UPLOAD AND DOWMLOAD TABLE DATA
#   __primary_author__ : AYYAPPAN SUBRAMANIYAN
#   __create_date :23-12-2021
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================


import re
import datetime
from SYDATABASE import SQL
import time
from datetime import timedelta , date
import CQPARTIFLW
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
		All_value=colums.split(",")
		Trace.Write(str(All_value))
		replace_col ={'CONSUMABLE/NON CONSUMABLE':'MATPRIGRP_ID','CUSTOMER WILL ACCPET W/6K PART':'CUSTOMER_ACCEPT_PART','CUSTOMER ANNUAL COMMIT':'CUSTOMER_ANNUAL_QUANTITY'}
		xls_col=replace_col.get
		All_value = [xls_col(val,val) for val in All_value]
		colums=','.join(All_value)
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
					Trace.Write("DATA++"+str(data))
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
			Trace.Write("table_columns"+str(table_columns))

			replace_col ={'MATPRIGRP_ID':'CONSUMABLE/NON CONSUMABLE','CUSTOMER_ACCEPT_PART':'CUSTOMER WILL ACCPET W/6K PART','CUSTOMER_ANNUAL_QUANTITY' :'CUSTOMER ANNUAL COMMIT'}
			xls_col=replace_col.get
			table_columns = [xls_col(val,val) for val in table_columns]
			Trace.Write("table_columns_after"+str(table_columns))

			if (self.tree_param) == 'Z0108' or (self.tree_param) == 'Z0110':
				col=table_columns
				if (self.tree_param) == 'Z0108':
					col[0:2]=[]
					Trace.Write("@Z0108_columns"+str(col))
				else:
					col[0:2]=[]
					col=[x for x in col if "DELIVERY" not in x]
					Trace.Write("@Z0110_columns"+str(col))
				table_columns=col

			columns = ",".join(table_columns)
			Trace.Write(str(columns))		
			self.object_name = related_list_obj.OBJECT_NAME
			total_count_obj = Sql.GetFirst("""
											SELECT COUNT(*) as count
											FROM {TableName} (NOLOCK)
											WHERE QUOTE_RECORD_ID ='{QuoteRecordId}' AND QTEREV_RECORD_ID='{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}'""".format(TableName=self.object_name, QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.tree_param))
			if total_count_obj:
				Trace.Write("inside"+str(total_count_obj))
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
		Trace.Write("Temp Table ===> "+str(spare_parts_temp_table_name))
		Trace.Write("@col"+str(self.columns))
		try:
			product_offering_entitlement_obj = Sql.GetFirst("select ENTITLEMENT_XML from SAQTSE (nolock) where QUOTE_RECORD_ID  = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID = '{service_id}'".format(QuoteRecordId= self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id,service_id = self.tree_param))
			entitlement_xml = product_offering_entitlement_obj.ENTITLEMENT_XML
			quote_item_tag = re.compile(r'(<QUOTE_ITEM_ENTITLEMENT>[\w\W]*?</QUOTE_ITEM_ENTITLEMENT>)')
			consigned_parts_match_id = re.compile(r'<ENTITLEMENT_ID>AGS_'+str(self.tree_param)+'[^>]*?_TSC_ONSTCP</ENTITLEMENT_ID>')
			consigned_parts_match_value = re.compile(r'<ENTITLEMENT_DISPLAY_VALUE>([^>]*?)</ENTITLEMENT_DISPLAY_VALUE>')
			for m in re.finditer(quote_item_tag, entitlement_xml):
				sub_string = m.group(1)
				consigned_parts_id =re.findall(consigned_parts_match_id,sub_string)
				consigned_parts_value =re.findall(consigned_parts_match_value,sub_string)
				if consigned_parts_id and consigned_parts_value:
					consigned_parts_value = consigned_parts_value[0]
					break
		except:
			Log.Info("error!")
			#Trace.Write("consigned_parts_value_CHK "+str(consigned_parts_value))
   
		try:
			spare_parts_temp_table_drop = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(spare_parts_temp_table_name)+"'' ) BEGIN DROP TABLE "+str(spare_parts_temp_table_name)+" END  ' ")	

			Log.Info("***sp_executesql @T=N'SELECT "+str(self.columns)+" INTO "+str(spare_parts_temp_table_name)+" FROM (SELECT DISTINCT "+str(self.columns)+" FROM (VALUES "+str(self.records)+") AS TEMP("+str(self.columns)+")) OQ ' ")		

			
			spare_parts_temp_table_bkp = SqlHelper.GetFirst("sp_executesql @T=N'SELECT "+str(self.columns)+" INTO "+str(spare_parts_temp_table_name)+" FROM (SELECT DISTINCT "+str(self.columns)+" FROM (VALUES "+str(self.records)+") AS TEMP("+str(self.columns)+")) OQ ' ")

			Trace.Write("sp_executesql @T=N'SELECT "+str(self.columns)+" INTO "+str(spare_parts_temp_table_name)+" FROM (SELECT DISTINCT "+str(self.columns)+" FROM (VALUES "+str(self.records)+") AS TEMP("+str(self.columns)+")) OQ ' ")

			spare_parts_existing_records_delete = SqlHelper.GetFirst("sp_executesql @T=N'DELETE FROM SAQSPT WHERE QUOTE_RECORD_ID = ''"+str(self.contract_quote_record_id)+"'' AND QTEREV_RECORD_ID = ''"+str(self.contract_quote_revision_record_id)+"'' ' ")
			account_id=""
			get_party_role = Sql.GetList("SELECT CPQ_PARTNER_FUNCTION, PARTY_ID FROM SAQTIP(NOLOCK) WHERE QUOTE_RECORD_ID = '"+str(self.contract_quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(self.contract_quote_revision_record_id)+"' and CPQ_PARTNER_FUNCTION in ('SOLD TO')")
		
			Log.Info("error2!")
			for keyobj in get_party_role:
				account_id = keyobj.PARTY_ID
		except Exception as e:
			Trace.Write("Exception Occured "+str(e))	
			
		if (self.tree_param =='Z0110'):
			Sql.RunQuery("""
							INSERT SAQSPT (QUOTE_SERVICE_PART_RECORD_ID, BASEUOM_ID, BASEUOM_RECORD_ID, CUSTOMER_PART_NUMBER, CUSTOMER_PART_NUMBER_RECORD_ID, EXTENDED_UNIT_PRICE, PART_DESCRIPTION, PART_NUMBER, PART_RECORD_ID, PRDQTYCON_RECORD_ID, CUSTOMER_ANNUAL_QUANTITY, QUOTE_ID, QUOTE_NAME, QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,SALESORG_ID, SALESORG_RECORD_ID, SALESUOM_CONVERSION_FACTOR, SALESUOM_ID, SALESUOM_RECORD_ID,DELIVERY_MODE, SCHEDULE_MODE, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, UNIT_PRICE, MATPRIGRP_ID, MATPRIGRP_RECORD_ID, DELIVERY_INTERVAL, VALID_FROM_DATE, VALID_TO_DATE,PAR_SERVICE_DESCRIPTION,PAR_SERVICE_ID,PAR_SERVICE_RECORD_ID,RETURN_TYPE,ODCC_FLAG, PAR_PART_NUMBER,EXCHANGE_ELIGIBLE, CUSTOMER_ELIGIBLE,CUSTOMER_PARTICIPATE, CUSTOMER_ACCEPT_PART,STPACCOUNT_ID, SHPACCOUNT_ID,CORE_CREDIT_PRICE,YEAR_1_DEMAND,YEAR_2_DEMAND,YEAR_3_DEMAND,ODCC_FLAG_DESCRIPTION, PROD_INSP_MEMO, SHELF_LIFE,CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED)
							SELECT DISTINCT
								CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_PART_RECORD_ID,
								BASEUOM_ID,
								BASEUOM_RECORD_ID,
								CUSTOMER_PART_NUMBER,
								CUSTOMER_PART_NUMBER_RECORD_ID,
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
								DELIVERY_MODE,
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
								RETURN_TYPE,
								ODCC_FLAG,
								PAR_PART_NUMBER,
								EXCHANGE_ELIGIBLE,
								CUSTOMER_ELIGIBLE,
								CUSTOMER_PARTICIPATE,
								CUSTOMER_ACCEPT_PART,
								STPACCOUNT_ID,
								SHPACCOUNT_ID,
								CORE_CREDIT_PRICE,
								YEAR_1_DEMAND,
								YEAR_2_DEMAND,
								YEAR_3_DEMAND,
								ODCC_FLAG_DESCRIPTION,
								PROD_INSP_MEMO,
								SHELF_LIFE,
								{UserId} as CPQTABLEENTRYADDEDBY, 
								GETDATE() as CPQTABLEENTRYDATEADDED
							FROM (
							SELECT 
								DISTINCT
								MAMTRL.UNIT_OF_MEASURE as BASEUOM_ID,
								MAMTRL.UOM_RECORD_ID as BASEUOM_RECORD_ID,
								TEMP_TABLE.CUSTOMER_PART_NUMBER  AS CUSTOMER_PART_NUMBER,
								MAMTRL.MATERIAL_RECORD_ID as CUSTOMER_PART_NUMBER_RECORD_ID,
								TEMP_TABLE.EXTENDED_UNIT_PRICE AS EXTENDED_UNIT_PRICE,
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
								CASE WHEN SAQTSV.SERVICE_ID='Z0110' AND TEMP_TABLE.CUSTOMER_ANNUAL_QUANTITY < 10 THEN 'OFFSITE' WHEN SAQTSV.SERVICE_ID='Z0110' AND TEMP_TABLE.CUSTOMER_ANNUAL_QUANTITY > 10 THEN 'ONSITE' ELSE 'OFFSITE' END AS DELIVERY_MODE,
								CASE WHEN SAQTSV.SERVICE_ID='Z0110' AND TEMP_TABLE.CUSTOMER_ANNUAL_QUANTITY < 10 THEN 'ON REQUEST' WHEN SAQTSV.SERVICE_ID='Z0110' AND TEMP_TABLE.CUSTOMER_ANNUAL_QUANTITY > 10 THEN 'LOW QUANTITY ONSITE' WHEN SAQTSV.SERVICE_ID='Z0108' AND  TEMP_TABLE.CUSTOMER_ANNUAL_QUANTITY <=9 THEN 'UNSCHEDULED' ELSE 'SCHEDULED' END AS SCHEDULE_MODE,
								SAQTSV.SERVICE_DESCRIPTION as SERVICE_DESCRIPTION,
								SAQTSV.SERVICE_ID as SERVICE_ID,
								SAQTSV.SERVICE_RECORD_ID as SERVICE_RECORD_ID,
								TEMP_TABLE.UNIT_PRICE AS UNIT_PRICE,
								MAMSOP.MATPRIGRP_ID as MATPRIGRP_ID,
								MAMSOP.MATPRIGRP_RECORD_ID as MATPRIGRP_RECORD_ID,
								'MONTHLY' as DELIVERY_INTERVAL,
								SAQTMT.CONTRACT_VALID_FROM as VALID_FROM_DATE, 
								SAQTMT.CONTRACT_VALID_TO as VALID_TO_DATE,
								SAQTSV.PAR_SERVICE_DESCRIPTION as PAR_SERVICE_DESCRIPTION,
								SAQTSV.PAR_SERVICE_ID as PAR_SERVICE_ID,
								SAQTSV.PAR_SERVICE_RECORD_ID as PAR_SERVICE_RECORD_ID,
								TEMP_TABLE.RETURN_TYPE AS RETURN_TYPE,
								TEMP_TABLE.ODCC_FLAG AS ODCC_FLAG,
								TEMP_TABLE.PAR_PART_NUMBER AS PAR_PART_NUMBER,
								TEMP_TABLE.EXCHANGE_ELIGIBLE AS EXCHANGE_ELIGIBLE,
								TEMP_TABLE.CUSTOMER_ELIGIBLE AS CUSTOMER_ELIGIBLE,
								TEMP_TABLE.CUSTOMER_PARTICIPATE as CUSTOMER_PARTICIPATE,
								TEMP_TABLE.CUSTOMER_ACCEPT_PART as CUSTOMER_ACCEPT_PART,
								'{account_id}' as STPACCOUNT_ID,
								TEMP_TABLE.SHPACCOUNT_ID as SHPACCOUNT_ID,
								TEMP_TABLE.CORE_CREDIT_PRICE AS CORE_CREDIT_PRICE,
								TEMP_TABLE.YEAR_1_DEMAND AS YEAR_1_DEMAND,
								TEMP_TABLE.YEAR_2_DEMAND AS YEAR_2_DEMAND,
								TEMP_TABLE.YEAR_3_DEMAND AS YEAR_3_DEMAND,
								TEMP_TABLE.ODCC_FLAG_DESCRIPTION AS ODCC_FLAG_DESCRIPTION,
								TEMP_TABLE.PROD_INSP_MEMO AS PROD_INSP_MEMO,
								TEMP_TABLE.SHELF_LIFE AS SHELF_LIFE
							FROM {TempTable} TEMP_TABLE(NOLOCK)
							JOIN MAMTRL (NOLOCK) ON MAMTRL.SAP_PART_NUMBER = TEMP_TABLE.PART_NUMBER
							JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = TEMP_TABLE.QUOTE_RECORD_ID
							JOIN SAQTSV (NOLOCK) ON SAQTSV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SAQTSV.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID AND SAQTSV.SERVICE_ID = '{ServiceId}'
							JOIN MAMSOP (NOLOCK) ON MAMSOP.MATERIAL_RECORD_ID = MAMTRL.MATERIAL_RECORD_ID AND MAMSOP.SALESORG_RECORD_ID = SAQTSV.SALESORG_RECORD_ID
							WHERE TEMP_TABLE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND TEMP_TABLE.QTEREV_RECORD_ID = '{RevisionRecordId}' AND MAMTRL.PRODUCT_TYPE IS NULL AND MAMTRL.IS_SPARE_PART = 1 AND ISNULL(MAMSOP.MATERIALSTATUS_ID,'') NOT IN('05','02') ) IQ
							""".format(
										TempTable=spare_parts_temp_table_name,
										ServiceId=self.tree_param,									
										QuoteRecordId=self.contract_quote_record_id,
										RevisionRecordId=self.contract_quote_revision_record_id,
										UserId=self.user_id,account_id = account_id
									)
			)
		elif (self.tree_param == 'Z0108'):	
			Sql.RunQuery("""
							INSERT SAQSPT (QUOTE_SERVICE_PART_RECORD_ID, BASEUOM_ID, BASEUOM_RECORD_ID, CUSTOMER_PART_NUMBER, CUSTOMER_PART_NUMBER_RECORD_ID, EXTENDED_UNIT_PRICE, PART_DESCRIPTION, PART_NUMBER, PART_RECORD_ID, PRDQTYCON_RECORD_ID, CUSTOMER_ANNUAL_QUANTITY, QUOTE_ID, QUOTE_NAME, QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,SALESORG_ID, SALESORG_RECORD_ID, SALESUOM_CONVERSION_FACTOR, SALESUOM_ID, SALESUOM_RECORD_ID,DELIVERY_MODE, SCHEDULE_MODE, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, UNIT_PRICE, MATPRIGRP_ID, MATPRIGRP_RECORD_ID, DELIVERY_INTERVAL, VALID_FROM_DATE, VALID_TO_DATE,PAR_SERVICE_DESCRIPTION,PAR_SERVICE_ID,PAR_SERVICE_RECORD_ID,RETURN_TYPE,ODCC_FLAG, PAR_PART_NUMBER,EXCHANGE_ELIGIBLE, CUSTOMER_ELIGIBLE,CUSTOMER_PARTICIPATE, CUSTOMER_ACCEPT_PART,STPACCOUNT_ID, SHPACCOUNT_ID,CORE_CREDIT_PRICE,YEAR_1_DEMAND,YEAR_2_DEMAND,YEAR_3_DEMAND,ODCC_FLAG_DESCRIPTION, PROD_INSP_MEMO, SHELF_LIFE,DELIVERY_1,DELIVERY_2,DELIVERY_3,DELIVERY_4,DELIVERY_5,DELIVERY_6,DELIVERY_7,DELIVERY_8,DELIVERY_9,DELIVERY_10,DELIVERY_11,DELIVERY_12,DELIVERY_13,DELIVERY_14,DELIVERY_15,DELIVERY_16,DELIVERY_17,DELIVERY_18,DELIVERY_19,DELIVERY_20,DELIVERY_21,DELIVERY_22,DELIVERY_23,DELIVERY_24,DELIVERY_25,DELIVERY_26,DELIVERY_27,DELIVERY_28,DELIVERY_29,DELIVERY_30,DELIVERY_31,DELIVERY_32,DELIVERY_33,DELIVERY_34,DELIVERY_35,DELIVERY_36,DELIVERY_37,DELIVERY_38,DELIVERY_39,DELIVERY_40,DELIVERY_41,DELIVERY_42,DELIVERY_43,DELIVERY_44,DELIVERY_45,DELIVERY_46,DELIVERY_47,DELIVERY_48,DELIVERY_49,DELIVERY_50,DELIVERY_51,DELIVERY_52, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED)
							SELECT DISTINCT
								CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_PART_RECORD_ID,
								BASEUOM_ID,
								BASEUOM_RECORD_ID,
								CUSTOMER_PART_NUMBER,
								CUSTOMER_PART_NUMBER_RECORD_ID,
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
								DELIVERY_MODE,
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
								RETURN_TYPE,
								ODCC_FLAG,
								PAR_PART_NUMBER,
								EXCHANGE_ELIGIBLE,
								CUSTOMER_ELIGIBLE,
								CUSTOMER_PARTICIPATE,
								CUSTOMER_ACCEPT_PART,
								STPACCOUNT_ID,
								SHPACCOUNT_ID,
								CORE_CREDIT_PRICE,
								YEAR_1_DEMAND,
								YEAR_2_DEMAND,
								YEAR_3_DEMAND,
								ODCC_FLAG_DESCRIPTION,
								PROD_INSP_MEMO,
								SHELF_LIFE,
								DELIVERY_1,
								DELIVERY_2,
								DELIVERY_3,
								DELIVERY_4,
								DELIVERY_5,
								DELIVERY_6,
								DELIVERY_7,
								DELIVERY_8,
								DELIVERY_9,
								DELIVERY_10,
								DELIVERY_11,
								DELIVERY_12,
								DELIVERY_13,
								DELIVERY_14,
								DELIVERY_15,
								DELIVERY_16,
								DELIVERY_17,
								DELIVERY_18,
								DELIVERY_19,
								DELIVERY_20,
								DELIVERY_21,
								DELIVERY_22,
								DELIVERY_23,
								DELIVERY_24,
								DELIVERY_25,
								DELIVERY_26,
								DELIVERY_27,
								DELIVERY_28,
								DELIVERY_29,
								DELIVERY_30,
								DELIVERY_31,
								DELIVERY_32,
								DELIVERY_33,
								DELIVERY_34,
								DELIVERY_35,
								DELIVERY_36,
								DELIVERY_37,
								DELIVERY_38,
								DELIVERY_39,
								DELIVERY_40,
								DELIVERY_41,
								DELIVERY_42,
								DELIVERY_43,
								DELIVERY_44,
								DELIVERY_45,
								DELIVERY_46,
								DELIVERY_47,
								DELIVERY_48,
								DELIVERY_49,
								DELIVERY_50,
								DELIVERY_51,
								DELIVERY_52,
								{UserId} as CPQTABLEENTRYADDEDBY, 
								GETDATE() as CPQTABLEENTRYDATEADDED
							FROM (
							SELECT 
								DISTINCT
								MAMTRL.UNIT_OF_MEASURE as BASEUOM_ID,
								MAMTRL.UOM_RECORD_ID as BASEUOM_RECORD_ID,
								TEMP_TABLE.CUSTOMER_PART_NUMBER  AS CUSTOMER_PART_NUMBER,
								MAMTRL.MATERIAL_RECORD_ID as CUSTOMER_PART_NUMBER_RECORD_ID,
								TEMP_TABLE.EXTENDED_UNIT_PRICE AS EXTENDED_UNIT_PRICE,
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
								CASE WHEN SAQTSV.SERVICE_ID='Z0110' AND TEMP_TABLE.CUSTOMER_ANNUAL_QUANTITY < 10 THEN 'OFFSITE' WHEN SAQTSV.SERVICE_ID='Z0110' AND TEMP_TABLE.CUSTOMER_ANNUAL_QUANTITY > 10 THEN 'ONSITE' ELSE 'OFFSITE' END AS DELIVERY_MODE,
								CASE WHEN SAQTSV.SERVICE_ID='Z0110' AND TEMP_TABLE.CUSTOMER_ANNUAL_QUANTITY < 10 THEN 'ON REQUEST' WHEN SAQTSV.SERVICE_ID='Z0110' AND TEMP_TABLE.CUSTOMER_ANNUAL_QUANTITY > 10 THEN 'LOW QUANTITY ONSITE' WHEN SAQTSV.SERVICE_ID='Z0108' AND  TEMP_TABLE.CUSTOMER_ANNUAL_QUANTITY <=9 THEN 'UNSCHEDULED' ELSE 'SCHEDULED' END AS SCHEDULE_MODE,
								SAQTSV.SERVICE_DESCRIPTION as SERVICE_DESCRIPTION,
								SAQTSV.SERVICE_ID as SERVICE_ID,
								SAQTSV.SERVICE_RECORD_ID as SERVICE_RECORD_ID,
								TEMP_TABLE.UNIT_PRICE AS UNIT_PRICE,
								MAMSOP.MATPRIGRP_ID as MATPRIGRP_ID,
								MAMSOP.MATPRIGRP_RECORD_ID as MATPRIGRP_RECORD_ID,
								'MONTHLY' as DELIVERY_INTERVAL,
								SAQTMT.CONTRACT_VALID_FROM as VALID_FROM_DATE, 
								SAQTMT.CONTRACT_VALID_TO as VALID_TO_DATE,
								SAQTSV.PAR_SERVICE_DESCRIPTION as PAR_SERVICE_DESCRIPTION,
								SAQTSV.PAR_SERVICE_ID as PAR_SERVICE_ID,
								SAQTSV.PAR_SERVICE_RECORD_ID as PAR_SERVICE_RECORD_ID,
								TEMP_TABLE.RETURN_TYPE AS RETURN_TYPE,
								TEMP_TABLE.ODCC_FLAG AS ODCC_FLAG,
								TEMP_TABLE.PAR_PART_NUMBER AS PAR_PART_NUMBER,
								TEMP_TABLE.EXCHANGE_ELIGIBLE AS EXCHANGE_ELIGIBLE,
								TEMP_TABLE.CUSTOMER_ELIGIBLE AS CUSTOMER_ELIGIBLE,
								TEMP_TABLE.CUSTOMER_PARTICIPATE as CUSTOMER_PARTICIPATE,
								TEMP_TABLE.CUSTOMER_ACCEPT_PART as CUSTOMER_ACCEPT_PART,
								'{account_id}' as STPACCOUNT_ID,
								TEMP_TABLE.SHPACCOUNT_ID as SHPACCOUNT_ID,
								TEMP_TABLE.CORE_CREDIT_PRICE AS CORE_CREDIT_PRICE,
								TEMP_TABLE.YEAR_1_DEMAND AS YEAR_1_DEMAND,
								TEMP_TABLE.YEAR_2_DEMAND AS YEAR_2_DEMAND,
								TEMP_TABLE.YEAR_3_DEMAND AS YEAR_3_DEMAND,
								TEMP_TABLE.ODCC_FLAG_DESCRIPTION AS ODCC_FLAG_DESCRIPTION,
								TEMP_TABLE.PROD_INSP_MEMO AS PROD_INSP_MEMO,
								TEMP_TABLE.SHELF_LIFE AS SHELF_LIFE,
								TEMP_TABLE.DELIVERY_1,
								TEMP_TABLE.DELIVERY_2,
								TEMP_TABLE.DELIVERY_3,
								TEMP_TABLE.DELIVERY_4,
								TEMP_TABLE.DELIVERY_5,
								TEMP_TABLE.DELIVERY_6,
								TEMP_TABLE.DELIVERY_7,
								TEMP_TABLE.DELIVERY_8,
								TEMP_TABLE.DELIVERY_9,
								TEMP_TABLE.DELIVERY_10,
								TEMP_TABLE.DELIVERY_11,
								TEMP_TABLE.DELIVERY_12,
								TEMP_TABLE.DELIVERY_13,
								TEMP_TABLE.DELIVERY_14,
								TEMP_TABLE.DELIVERY_15,
								TEMP_TABLE.DELIVERY_16,
								TEMP_TABLE.DELIVERY_17,
								TEMP_TABLE.DELIVERY_18,
								TEMP_TABLE.DELIVERY_19,
								TEMP_TABLE.DELIVERY_20,
								TEMP_TABLE.DELIVERY_21,
								TEMP_TABLE.DELIVERY_22,
								TEMP_TABLE.DELIVERY_23,
								TEMP_TABLE.DELIVERY_24,
								TEMP_TABLE.DELIVERY_25,
								TEMP_TABLE.DELIVERY_26,
								TEMP_TABLE.DELIVERY_27,
								TEMP_TABLE.DELIVERY_28,
								TEMP_TABLE.DELIVERY_29,
								TEMP_TABLE.DELIVERY_30,
								TEMP_TABLE.DELIVERY_31,
								TEMP_TABLE.DELIVERY_32,
								TEMP_TABLE.DELIVERY_33,
								TEMP_TABLE.DELIVERY_34,
								TEMP_TABLE.DELIVERY_35,
								TEMP_TABLE.DELIVERY_36,
								TEMP_TABLE.DELIVERY_37,
								TEMP_TABLE.DELIVERY_38,
								TEMP_TABLE.DELIVERY_39,
								TEMP_TABLE.DELIVERY_40,
								TEMP_TABLE.DELIVERY_41,
								TEMP_TABLE.DELIVERY_42,
								TEMP_TABLE.DELIVERY_43,
								TEMP_TABLE.DELIVERY_44,
								TEMP_TABLE.DELIVERY_45,
								TEMP_TABLE.DELIVERY_46,
								TEMP_TABLE.DELIVERY_47,
								TEMP_TABLE.DELIVERY_48,
								TEMP_TABLE.DELIVERY_49,
								TEMP_TABLE.DELIVERY_50,
								TEMP_TABLE.DELIVERY_51,
								TEMP_TABLE.DELIVERY_52
							FROM {TempTable} TEMP_TABLE(NOLOCK)
							JOIN MAMTRL (NOLOCK) ON MAMTRL.SAP_PART_NUMBER = TEMP_TABLE.PART_NUMBER
							JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = TEMP_TABLE.QUOTE_RECORD_ID
							JOIN SAQTSV (NOLOCK) ON SAQTSV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SAQTSV.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID AND SAQTSV.SERVICE_ID = '{ServiceId}'
							JOIN MAMSOP (NOLOCK) ON MAMSOP.MATERIAL_RECORD_ID = MAMTRL.MATERIAL_RECORD_ID AND MAMSOP.SALESORG_RECORD_ID = SAQTSV.SALESORG_RECORD_ID
							WHERE TEMP_TABLE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND TEMP_TABLE.QTEREV_RECORD_ID = '{RevisionRecordId}' AND MAMTRL.PRODUCT_TYPE IS NULL AND MAMTRL.IS_SPARE_PART = 1 AND ISNULL(MAMSOP.MATERIALSTATUS_ID,'') <> '05') IQ
							""".format(
										TempTable=spare_parts_temp_table_name,
										ServiceId=self.tree_param,									
										QuoteRecordId=self.contract_quote_record_id,
										RevisionRecordId=self.contract_quote_revision_record_id,
										UserId=self.user_id,account_id = account_id
									)
			)
			spare_parts_temp_table_drop = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(spare_parts_temp_table_name)+"'' ) BEGIN DROP TABLE "+str(spare_parts_temp_table_name)+" END  ' ")
		
			spare_parts_temp_table_drop = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(spare_parts_temp_table_name)+"'' ) BEGIN DROP TABLE "+str(spare_parts_temp_table_name)+" END  ' ")		
		##calling the iflow for pricing..
		
			contract_quote_obj = Sql.GetFirst("SELECT QUOTE_ID FROM SAQTMT (NOLOCK) WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{QuoteRecordId}'".format(QuoteRecordId=Quote.GetGlobal("contract_quote_record_id")))
			if contract_quote_obj:
				contract_quote_id = contract_quote_obj.QUOTE_ID
			count=Sql.GetFirst("SELECT COUNT(*) AS CNT FROM SAQSPT WHERE QUOTE_ID= '"+str(contract_quote_id)+"' and CUSTOMER_ANNUAL_QUANTITY IS NOT NULL ")      
			if count.CNT > 0:
				Log.Info("PART PRICING IFLOW STARTED !")
				CQPARTIFLW.iflow_pricing_call(str(self.user_name),str(contract_quote_id),str(self.contract_quote_revision_record_id))
				

	def _do_opertion(self):
		add_part_numbers=[]
		New_part_numbers=[]
		for sheet_data in self.upload_data:	
			if not sheet_data.Value:	
				break	
			xls_spare_records = list(sheet_data.Value)
			if xls_spare_records:
				for sub_records in list(xls_spare_records):
					if (sub_records[3]) != 'PART_DESCRIPTION':
						add_part_numbers.append(sub_records[2])
						sub_records[3] =''				
			
				#del_col=[val.pop(3)  for val in xls_spare_records]
				#xls_spare_records = str(xls_spare_records).replace('Â','')
				#xls_spare_records = ",".join(list(xls_spare_records)).replace('Â','')
				#Trace.Write(xls_spare_records)
				#xls_spare_records = xls_spare_records.split(",")
				header = list(xls_spare_records[0]) + ['QUOTE_RECORD_ID','QTEREV_RECORD_ID']
				
				self.columns = ",".join(header)

				Trace.Write("colums"+str(self.columns))

				old_part_numbers=Sql.GetList("SELECT DISTINCT PART_NUMBER FROM SAQSPT WHERE QUOTE_RECORD_ID ='{QuoteRecordId}' AND QTEREV_RECORD_ID='{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}'".format(Columns=(self.columns), QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.tree_param))

				Trace.Write(old_part_numbers)
				val=set(add_part_numbers)
				New_part_numbers=[x for  x in old_part_numbers if x not in val]
				
				Trace.Write("new_parts"+str(New_part_numbers))

				col=self.columns
				table_columns = col.split(",")
				replace_col ={'CONSUMABLE/NON CONSUMABLE':'MATPRIGRP_ID','CUSTOMER WILL ACCPET W/6K PART':'CUSTOMER_ACCEPT_PART','CUSTOMER ANNUAL COMMIT':'CUSTOMER_ANNUAL_QUANTITY'}
				xls_col=replace_col.get
				table_columns = [xls_col(val,val) for val in table_columns]

				self.columns = ",".join(table_columns)

				Trace.Write("table_columns---"+str(self.columns))
				modified_records = []
				for spare_record in xls_spare_records[1:]:
					
					modified_records.append(str(tuple([float(spare_val) if type(spare_val) == "<type 'Decimal'>" else spare_val for spare_val in spare_record])))

				
				for spare_record in xls_spare_records:
					if spare_record[1] and spare_record[1].upper() != "NULL":
						spare_record[1]=str(spare_record[1])
					else:
						spare_record[1] =""


				#self.records = ', '.join(map(str, modified_records)).replace("None","null").replace("'","''")
				self.records = ', '.join(map(str, [str(tuple(list(spare_record)+[self.contract_quote_record_id, self.contract_quote_revision_record_id])) for spare_record in xls_spare_records[1:]])).replace("None","null").replace("'","''")
				Trace.Write("Records000 ===> "+str(self.records))
				self.records = self.records.replace("True","1").replace("False","0").replace ("Â" ," ").replace("?","")
				Trace.Write("Records111 ===> "+str(self.records))
				self.records = re.sub(r"<?[a-zA-Z0-9_.\[ \]]+>", "0.00", self.records)
				
				Trace.Write("Records222 ===> "+str(self.records))
			# for index, data in enumerate(list(sheet_data.Value)):
			# 	if index == 0:
			# 		self.columns = ",".join(data)
			# 		continue
			# 	self.records.append(tuple(data))
			# 	Trace.Write("data ====>>> "+str(list(data)))
		self._insert_spare_parts()
		#self.insert_delivery_schedule()
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
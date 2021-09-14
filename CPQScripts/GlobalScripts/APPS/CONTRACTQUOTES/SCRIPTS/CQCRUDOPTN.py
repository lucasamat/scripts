# =========================================================================================================================================
#   __script_name : CQCRUDOPTN.PY
#   __script_description : THIS SCRIPT IS USED TO ADD, UPDATE, DELETE RECORDS IN THE SALES AND RELATED TABLES
#   __primary_author__ : AYYAPPAN SUBRAMANIYAN, Suriya (BitBucket deployment issue fixed)
#   __create_date :23-09-2020
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================

import datetime
import Webcom.Configurator.Scripting.Test.TestProduct
import sys
import re
import System.Net
import SYCNGEGUID as CPQID
import CQPARTIFLW
import CQVLDRIFLW
import CQTVLDRIFW
from SYDATABASE import SQL
#from datetime import datetime
#from datetime import datetime
#import time
Sql = SQL()
ScriptExecutor = ScriptExecutor

try:
	current_prod = Product.Name
except:
	current_prod = ""

import time
class ContractQuoteCrudOpertion:
	def __init__(self, **kwargs):
		self.trigger_from = kwargs.get('trigger_from')
		if self.trigger_from:
			self.tree_param = kwargs.get('tree_param')
			self.tree_parent_level_0 = kwargs.get('tree_parent_level_0')
			self.tree_parent_level_1 = kwargs.get('tree_parent_level_1')
			self.contract_quote_record_id = kwargs.get('contract_quote_record_id')
		else:
			self.tree_param = Product.GetGlobal("TreeParam")
			self.tree_parent_level_0 = Product.GetGlobal("TreeParentLevel0")
			self.tree_parent_level_1 = Product.GetGlobal("TreeParentLevel1")
			self.tree_parent_level_2 = Product.GetGlobal("TreeParentLevel2")
			self.tree_parent_level_3 = Product.GetGlobal("TreeParentLevel3")
			self.tree_parent_level_4 = Product.GetGlobal("TreeParentLevel4")
			self.tree_parent_level_5 = Product.GetGlobal("TreeParentLevel5")
			self.tree_parent_level_6 = Product.GetGlobal("TreeParentLevel6")
			self.tree_parent_level_7 = Product.GetGlobal("TreeParentLevel7")
			self.tree_parent_level_8 = Product.GetGlobal("TreeParentLevel8")
		self.user_id = str(User.Id) #ScriptExecutor.ExecuteGlobal("SYUSDETAIL", "USERID")
		self.user_name = str(User.UserName) #ScriptExecutor.ExecuteGlobal("SYUSDETAIL", "USERNAME")
		#self.sale_type = None
		
		self.datetime_value = datetime.datetime.now()
		self.set_contract_quote_related_details()

	def set_contract_quote_related_details(
		self, columns=["*"], table_name=None, where_condition="", table_joins="", single_record=False
	):
		# Set - Contract Quote Details
		if not self.trigger_from == "IntegrationScript":
			try:
				self.contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
			except:
				self.contract_quote_record_id = ''	
			try:
				self.quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
			except:
				self.quote_revision_record_id = ''
			#Trace.Write("quote---"+str(self.contract_quote_record_id))
		GetToolReloc = Sql.GetList("SELECT CpqTableEntryId FROM SAQTIP WHERE (PARTY_ROLE = 'RECEIVING ACCOUNT' OR PARTY_ROLE = 'SENDING ACCOUNT') AND QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(self.contract_quote_record_id,self.quote_revision_record_id))
		#Trace.Write("count--"+str(list(GetToolReloc)))
		GetToolReloc = list(GetToolReloc)
		if len(GetToolReloc) == 2:
			self.sale_type = "TOOL RELOCATION"
		else:
			self.sale_type = None
		Trace.Write("SALE TYPE = "+str(self.sale_type))
		contract_quote_record_obj = self._get_record_obj(
			columns=[
				"QUOTE_ID",
				"QUOTE_NAME",
				"QUOTE_TYPE",
				#"SALESORG_ID",
				#"SALESORG_NAME",
				#"SALESORG_RECORD_ID",
				"ACCOUNT_ID",
				"ACCOUNT_NAME",
				"ACCOUNT_RECORD_ID",
				"CONTRACT_VALID_FROM",
				"CONTRACT_VALID_TO",
				"QUOTE_CURRENCY",
				"QUOTE_CURRENCY_RECORD_ID",
				"C4C_QUOTE_ID",
				"SOURCE_CONTRACT_ID",
				"SALE_TYPE",
				"QTEREV_ID",
				"QTEREV_RECORD_ID"
			],
			table_name="SAQTMT",
			where_condition="MASTER_TABLE_QUOTE_RECORD_ID = '{}'".format(self.contract_quote_record_id),
			single_record=True,
		)
		salesorg_obj = self._get_record_obj(
			columns=[
				#"QUOTE_ID",
				#"QUOTE_NAME",
				"SALESORG_ID",
				"SALESORG_NAME",
				"SALESORG_RECORD_ID"
				#"ACCOUNT_ID",
				#"ACCOUNT_NAME",
				#"ACCOUNT_RECORD_ID",
				#"CONTRACT_VALID_FROM",
				#"CONTRACT_VALID_TO",
				#"QUOTE_CURRENCY",
				#"QUOTE_CURRENCY_RECORD_ID",
				#"C4C_QUOTE_ID",
				#"SOURCE_CONTRACT_ID"
			],
			table_name="SAQTRV",
			where_condition="QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(self.contract_quote_record_id,self.quote_revision_record_id),
			single_record=True,
		)
		
		
		if contract_quote_record_obj:
			self.contract_quote_id = contract_quote_record_obj.QUOTE_ID
			self.contract_quote_name = contract_quote_record_obj.QUOTE_NAME
			self.quote_type = contract_quote_record_obj.QUOTE_TYPE
			self.quote_revision_id = contract_quote_record_obj.QTEREV_ID
			self.quote_revision_record_id = contract_quote_record_obj.QTEREV_RECORD_ID
			self.salesorg_id = salesorg_obj.SALESORG_ID
			self.salesorg_name = salesorg_obj.SALESORG_NAME
			self.salesorg_record_id = salesorg_obj.SALESORG_RECORD_ID
			self.account_id = contract_quote_record_obj.ACCOUNT_ID
			self.account_name = contract_quote_record_obj.ACCOUNT_NAME
			self.account_record_id = contract_quote_record_obj.ACCOUNT_RECORD_ID
			self.contract_start_date = contract_quote_record_obj.CONTRACT_VALID_FROM
			self.contract_end_date = contract_quote_record_obj.CONTRACT_VALID_TO
			self.contract_currency = contract_quote_record_obj.QUOTE_CURRENCY
			self.contract_currency_record_id = contract_quote_record_obj.QUOTE_CURRENCY_RECORD_ID
			self.c4c_quote_id = contract_quote_record_obj.C4C_QUOTE_ID
			self.source_contract_id = contract_quote_record_obj.SOURCE_CONTRACT_ID
			#self.sale_type = contract_quote_record_obj.SALE_TYPE
		else:
			self.contract_quote_id = None
			self.contract_quote_name = None
			self.salesorg_id = None
			self.salesorg_name = None
			self.salesorg_record_id = None
			self.account_id = None
			self.account_record_id = None
			self.account_name = None
			self.contract_start_date = None
			self.contract_end_date = None
			self.contract_currency = None
			self.contract_currency_record_id = None
			self.c4c_quote_id = None
			self.source_contract_id = None
			#self.sale_type = None
		return True

	def _get_record_obj(self, columns=["*"], table_name=None, where_condition="", table_joins="", single_record=False):	
		if table_name and self.tree_param != 'Approval Chain Steps' and str(current_prod).upper() not in ("SYSTEM ADMIN","APPROVAL CENTER"):
			
			if where_condition:
				where_condition = "WHERE {}".format(where_condition)			
			
			if single_record:
				return Sql.GetFirst("SELECT {Columns} FROM {ObjectName} (NOLOCK) {Joins} {WhereCondition}".format(
						Columns=",".join(columns), ObjectName=table_name, Joins=table_joins, WhereCondition=where_condition
					))
			else:				
				return Sql.GetList(
					"SELECT {Columns} FROM {ObjectName} (NOLOCK) {Joins} {WhereCondition}".format(
						Columns=",".join(columns), ObjectName=table_name, Joins=table_joins, WhereCondition=where_condition
					)
				)
		return None

	def _process_query(self, query_string):
		try:
			Sql.RunQuery(query_string)
		except Exception:
			Log.Info("_process_query---->:" + str(sys.exc_info()[1]))
		return True

	def _add_record(
		self, master_object_name=None, columns=[], table_name=None, condition_column=None, values=[], where_condition=""
	):		
		TreeParam=Product.GetGlobal("TreeParam")
		if self.action_type == "ADD_OFFERING" and self.all_values:
			if TreeParam=="Product Offerings":
				product_type=" PRODUCT_TYPE IS NOT NULL AND PRODUCT_TYPE <> '' AND PRODUCT_TYPE != 'Add-On Products' "
			elif TreeParam!="Product Offerings" and TreeParam!="Add-On Products":
				product_type=" PRODUCT_TYPE = '{TreeParam}' ".format(TreeParam=TreeParam)
			qury_str=""
			if A_Keys!="" and A_Values!="":
				for key,val in zip(A_Keys,A_Values):
					if(val!=""):
						if key=="MATERIAL_RECORD_ID":
							key="CpqTableEntryId"
							val = ''.join(re.findall(r'\d+', val)) if not val.isdigit() else val
						qury_str+=" MAMTRL."+key+" LIKE '%"+val+"%' AND "
				get_sales_org = SqlHelper.GetFirst("SELECT * FROM SAQTRV WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(self.contract_quote_record_id,self.quote_revision_record_id))
				sales_org=""
				if get_sales_org :
					sales_org=get_sales_org.SALESORG_ID
				query_string="select MAMTRL.MATERIAL_RECORD_ID, MAMTRL.SAP_PART_NUMBER, SAP_DESCRIPTION, PRODUCT_TYPE from MAMTRL (NOLOCK)  INNER JOIN MAMSOP (NOLOCK) ON MAMTRL.MATERIAL_RECORD_ID = MAMSOP.MATERIAL_RECORD_ID  WHERE  ISNULL(IS_SPARE_PART,0) = 0 AND {product_type} AND {Qury_Str} MAMTRL.SAP_PART_NUMBER NOT IN (SELECT SERVICE_ID FROM SAQTSV (NOLOCK) WHERE QUOTE_RECORD_ID = '{contract_quote_record_id}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' )  AND SALESORG_ID='{sales_org}'  ".format(product_type=product_type,Qury_Str=qury_str,contract_quote_record_id = self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id,sales_org=sales_org)
				Trace.Write('query_string---'+str(query_string))
				result=SqlHelper.GetList(query_string)
				if result is not None:
					record_ids = [data.MATERIAL_RECORD_ID for data in result]
		else:
			record_ids = [
				CPQID.KeyCPQId.GetKEYId(master_object_name, str(value))
				if value.strip() != "" and master_object_name in value
				else value
				for value in values
			]
		
		if record_ids:
			if len(record_ids) == 1:
				where_conditon = "%s = '%s'" % (condition_column, record_ids[0],)
			else:
				where_conditon = "%s in %s" % (condition_column, tuple(record_ids),)
		records_obj = self._get_record_obj(columns=columns, table_name=master_object_name, where_condition=where_conditon)
		if records_obj:
			auto_number_column_name_obj = self._get_record_obj(
				columns=["API_NAME"],
				table_name="SYOBJD",
				where_condition="OBJECT_NAME = '{}' AND DATA_TYPE='AUTO NUMBER'".format(table_name),
				single_record=True,
			)
			auto_number_column_name = auto_number_column_name_obj.API_NAME

			common_row_values = {
				"QUOTE_RECORD_ID": self.contract_quote_record_id,
				"QUOTE_ID": self.contract_quote_id,
			}
			for record_obj in records_obj:
				row = {data.Key: data.Value for data in record_obj}
				row[auto_number_column_name] = str(Guid.NewGuid()).upper()
				row.update(common_row_values)				
				yield dict(row)
		##A055S000P01-8740 code ends...
		ScriptExecutor.ExecuteGlobal('CQDOCUTYPE',{'QUOTE_RECORD_ID':self.contract_quote_record_id,'QTEREV_RECORD_ID':self.quote_revision_record_id})
		##A055S000P01-8740 code ends...
	def _create(self):
		pass

	def _update(self):
		pass

	def _update_record(self, update_column_statement="", table_name="", where_condition="", order_by_statement=""):
		if update_column_statement and table_name and where_condition:
			update_query = "UPDATE {ObjectName} SET {UpdateColumnStatement} WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{ContractQuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' {WhereCondition} {OrderByStatement}".format(
				ObjectName=table_name, ContractQuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id, WhereCondition=where_condition,
			)
			self._process_query(update_query)

	def _delete_record(self, where_condition, object_names):
		
		for table_name in object_names:
			delete_query = "DELETE FROM {ObjectName} WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{ContractQuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' {WhereCondition}".format(
				ObjectName=table_name, ContractQuoteRecordId=self.contract_quote_record_id, RevisionRecordId=self.quote_revision_record_id,WhereCondition=where_condition,
			)
			Trace.Write("===========> 11111 delete"+str(delete_query))
			Log.Info("User Id" + str(self.user_id) + "Script Name:CQCRUDOPTN.PY Query Statement:" + str(delete_query))
			self._process_query(delete_query)
		return True

	def _delete(self):
		pass	
							
	def insert_items_billing_plan(self, total_months=1, billing_date='', amount_column='YEAR_1', entitlement_obj=None):
		#QTQIBP_INS=Sql.GetFirst("select convert(xml,replace(replace(ENTITLEMENT_XML,'&',';#38'),'''',';#39')) as ENTITLEMENT_XML,QUOTE_RECORD_ID,SERVICE_ID from SAQTSE (nolock) where QUOTE_RECORD_ID = '{QuoteRecordId}'".format(QuoteRecordId =self.contract_quote_record_id ))
		year = int(amount_column.split('_')[-1])
		remaining_months = (total_months + 1) - (year*12)		
		divide_by = 12
		#s=Sql.GetFirst("select convert(xml,replace(replace(ENTITLEMENT_XML,'&',';#38'),'''',';#39')) as ENTITLEMENT_XML,QUOTE_RECORD_ID,SERVICE_ID from SAQTSE (nolock) where QUOTE_RECORD_ID = '{QuoteRecordId}'".format(QuoteRecordId =self.contract_quote_record_id ))
		if remaining_months < 0:
			divide_by = 12 + remaining_months
		Trace.Write('272-----272-----')
		
		Sql.RunQuery("""INSERT SAQIBP (
						QUOTE_ITEM_BILLING_PLAN_RECORD_ID, BILLING_END_DATE, BILLING_START_DATE, BILLING_TYPE, 
						LINE_ITEM_ID, QUOTE_ID, QTEITM_RECORD_ID, QUOTE_NAME, 
						QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID, SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID,
						BILLING_AMOUNT, BILLING_DATE, BILLING_INTERVAL, BILLING_YEAR,
						EQUIPMENT_DESCRIPTION, EQUIPMENT_ID, EQUIPMENT_LINE_ID, EQUIPMENT_RECORD_ID, PO_ITEM, PO_NUMBER, QTEITMCOB_RECORD_ID, 
						SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, ANNUAL_BILLING_AMOUNT, GREENBOOK, GREENBOOK_RECORD_ID, BILLING_CURRENCY_RECORD_ID, SERIAL_NUMBER, WARRANTY_START_DATE, WARRANTY_END_DATE, EQUIPMENT_QUANTITY, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED
					) 
					SELECT 
						CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_BILLING_PLAN_RECORD_ID,  
						SAQICO.WARRANTY_END_DATE as BILLING_END_DATE,
						SAQICO.WARRANTY_START_DATE as BILLING_START_DATE,
						'Variable Billing' as BILLING_TYPE,
						SAQICO.LINE_ITEM_ID AS LINE_ITEM_ID,	
						SAQICO.QUOTE_ID,
						SAQICO.QTEITM_RECORD_ID,
						SAQICO.QUOTE_NAME,
						SAQICO.QUOTE_RECORD_ID,
						SAQICO.QTEREV_ID,
						SAQICO.QTEREV_RECORD_ID,
						SAQICO.SALESORG_ID,
						SAQICO.SALESORG_NAME,
						SAQICO.SALESORG_RECORD_ID,
						ISNULL({AmountColumn}, 0) / 12 as BILLING_AMOUNT,	
						{BillingDate} as BILLING_DATE,				
						'MONTHLY' as BILLING_INTERVAL,
						0 as BILLING_YEAR,
						SAQICO.EQUIPMENT_DESCRIPTION,
						SAQICO.EQUIPMENT_ID,
						SAQICO.EQUIPMENT_LINE_ID,
						SAQICO.EQUIPMENT_RECORD_ID,
						'' as PO_ITEM,
						'' as PO_NUMBER,
						SAQICO.QUOTE_ITEM_COVERED_OBJECT_RECORD_ID as QTEITMCOB_RECORD_ID,
						SAQICO.SERVICE_DESCRIPTION,
						SAQICO.SERVICE_ID,
						SAQICO.SERVICE_RECORD_ID,     
						(ISNULL(SAQICO.{AmountColumn}, 0) / 12) * {DivideBy} AS ANNUAL_BILLING_AMOUNT,
						SAQICO.GREENBOOK,
						SAQICO.GREENBOOK_RECORD_ID,
						'' AS BILLING_CURRENCY_RECORD_ID,
						SAQICO.SERIAL_NO AS SERIAL_NUMBER,
						SAQICO.WARRANTY_START_DATE,
						SAQICO.WARRANTY_END_DATE,              
						SAQICO.EQUIPMENT_QUANTITY,    
						{UserId} as CPQTABLEENTRYADDEDBY, 
						GETDATE() as CPQTABLEENTRYDATEADDED
					FROM SAQICO (NOLOCK) 
					WHERE SAQICO.QUOTE_RECORD_ID='{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{RevisionRecordId}'""".format(
						UserId=self.user_id, QuoteRecordId=self.contract_quote_record_id,
						RevisionRecordId=self.quote_revision_record_id,
						BillingDate=billing_date,
						AmountColumn=amount_column,
						DivideBy=divide_by))
					
		'''Sql.RunQuery("""INSERT SAQIBP (
						QUOTE_ITEM_BILLING_PLAN_RECORD_ID, BILLING_END_DATE, BILLING_START_DATE, BILLING_TYPE, 
						LINE_ITEM_ID, QUOTE_ID, QTEITM_RECORD_ID, QUOTE_NAME, 
						QUOTE_RECORD_ID, SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID,
						BILLING_AMOUNT, BILLING_DATE, BILLING_INTERVAL, BILLING_YEAR,
						EQUIPMENT_DESCRIPTION, EQUIPMENT_ID, EQUIPMENT_LINE_ID, EQUIPMENT_RECORD_ID, PO_ITEM, PO_NUMBER, QTEITMCOB_RECORD_ID, 
						SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, ANNUAL_BILLING_AMOUNT, GREENBOOK, GREENBOOK_RECORD_ID,
						BILLING_CURRENCY, BILLING_CURRENCY_RECORD_ID, SERIAL_NUMBER, WARRANTY_START_DATE, WARRANTY_END_DATE, EQUIPMENT_QUANTITY, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED
					) 
					SELECT 
						CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_BILLING_PLAN_RECORD_ID,  
						SAQICO.WARRANTY_END_DATE as BILLING_END_DATE,
						SAQICO.WARRANTY_START_DATE as BILLING_START_DATE,
						'Variable Billing' as BILLING_TYPE,
						SAQICO.LINE_ITEM_ID AS LINE_ITEM_ID,	
						SAQICO.QUOTE_ID,
						SAQICO.QTEITM_RECORD_ID,
						SAQICO.QUOTE_NAME,
						SAQICO.QUOTE_RECORD_ID,
						SAQICO.SALESORG_ID,
						SAQICO.SALESORG_NAME,
						SAQICO.SALESORG_RECORD_ID,
						ISNULL({AmountColumn}, 0) / 12 as BILLING_AMOUNT,	
						{BillingDate} as BILLING_DATE,				
						'MONTHLY' as BILLING_INTERVAL,
						0 as BILLING_YEAR,
						SAQICO.EQUIPMENT_DESCRIPTION,
						SAQICO.EQUIPMENT_ID,
						SAQICO.EQUIPMENT_LINE_ID,
						SAQICO.EQUIPMENT_RECORD_ID,
						'' as PO_ITEM,
						'' as PO_NUMBER,
						SAQICO.QUOTE_ITEM_COVERED_OBJECT_RECORD_ID as QTEITMCOB_RECORD_ID,
						SAQICO.SERVICE_DESCRIPTION,
						SAQICO.SERVICE_ID,
						SAQICO.SERVICE_RECORD_ID,     
						(ISNULL(SAQICO.{AmountColumn}, 0) / 12) * {DivideBy} AS ANNUAL_BILLING_AMOUNT,
						SAQICO.GREENBOOK,
						SAQICO.GREENBOOK_RECORD_ID,
						SAQICO.QUOTE_CURRENCY AS BILLING_CURRENCY,
						'' AS BILLING_CURRENCY_RECORD_ID,
						SAQICO.SERIAL_NO AS SERIAL_NUMBER,
						SAQICO.WARRANTY_START_DATE,
						SAQICO.WARRANTY_END_DATE,              
						SAQICO.EQUIPMENT_QUANTITY,    
						{UserId} as CPQTABLEENTRYADDEDBY, 
						GETDATE() as CPQTABLEENTRYDATEADDED
					FROM SAQICO (NOLOCK)     
					JOIN (SELECT distinct e.QUOTE_RECORD_ID, replace(X.Y.value('(ENTITLEMENT_NAME)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_NAME,replace(X.Y.value('(ENTITLEMENT_DISPLAY_VALUE)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_DISPLAY_VALUE, SERVICE_ID FROM (select '{quote}' as QUOTE_RECORD_ID,convert(xml,'{xml}') as ENTITLEMENT_XML, '{serid}' as SERVICE_ID  ) e OUTER APPLY e.ENTITLEMENT_XML.nodes('QUOTE_ITEM_ENTITLEMENT') as X(Y) ) as JQ ON
											JQ.QUOTE_RECORD_ID = SAQICO.QUOTE_RECORD_ID AND JQ.ENTITLEMENT_NAME IN ('AGS_BIL_BIL_TYP') 
								AND JQ.ENTITLEMENT_DISPLAY_VALUE = 'Variable Billing'
											AND JQ.SERVICE_ID = SAQICO.SERVICE_ID                
					WHERE SAQICO.QUOTE_RECORD_ID='{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{RevisionRecordId}'""".format(
						UserId=self.user_id, QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id,
						Months=total_months,
						BillingDate=billing_date,
						AmountColumn=amount_column,
						DivideBy=divide_by,quote=str(entitlement_obj.QUOTE_RECORD_ID),xml=str(entitlement_obj.ENTITLEMENT_XML),serid=str(entitlement_obj.SERVICE_ID)
						))'''
		return True
	
	def insert_quote_billing_plan(self,cart_id,cart_user_id):
		Trace.Write('insert data in insert_quote_billing_plan--start') 
		# Sql.RunQuery("""DELETE FROM QT__Billing_Matrix_Header WHERE cartId = '{CartId}' AND ownerId = {UserId} AND QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'""".format(CartId=cart_id, UserId=cart_user_id, QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id))
		# Sql.RunQuery("""DELETE FROM QT__BM_YEAR_1 WHERE cartId = '{CartId}' AND ownerId = {UserId} AND QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'""".format(CartId=cart_id, UserId=cart_user_id, QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id))
		services_obj = Sql.GetList("SELECT SERVICE_ID FROM SAQTSV (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' ".format(self.contract_quote_record_id,self.quote_revision_record_id))
		item_billing_plan_obj = Sql.GetFirst("SELECT count(CpqTableEntryId) as cnt FROM SAQIBP (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'GROUP BY EQUIPMENT_ID".format(self.contract_quote_record_id,self.quote_revision_record_id))
		if item_billing_plan_obj is not None and services_obj:
			quotient, remainder = divmod(item_billing_plan_obj.cnt, 12)
			years = quotient + (1 if remainder > 0 else 0)
			if not years:
				years = 1
			for index in range(1, years+1):
				YearCount = "Year {}".format(index)
				no_of_year = index
				#YearCount1 = index
				if YearCount:
					end = int(YearCount.split(' ')[-1]) * 12
					start = end - 12 + 1	
					item_billing_plans_obj = Sql.GetList("""SELECT FORMAT(BILLING_DATE, 'MM-dd-yyyy') as BILLING_DATE FROM (SELECT ROW_NUMBER() OVER(ORDER BY BILLING_DATE)
															AS ROW, * FROM (SELECT DISTINCT BILLING_DATE
															FROM SAQIBP (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' 
															AND QTEREV_RECORD_ID = '{}' GROUP BY EQUIPMENT_ID, BILLING_DATE) IQ) OQ WHERE OQ.ROW BETWEEN {} AND {}""".format(
															self.contract_quote_record_id,self.quote_revision_record_id, start, end))
					if item_billing_plans_obj:
						billing_date_column = [item_billing_plan_obj.BILLING_DATE for item_billing_plan_obj in item_billing_plans_obj]
						date_columns = " ,".join(['MONTH_{}'.format(index) for index in range(1, len(billing_date_column)+1)])
						header_select_date_columns = ",".join(["'{}' AS MONTH_{}".format(date_column, index) for index, date_column in enumerate(billing_date_column, 1)])
						select_date_columns = ",".join(['[{}] AS MONTH_{}'.format(date_column, index) for index, date_column in enumerate(billing_date_column, 1)])
						sum_select_date_columns = ",".join(['SUM([{}]) AS MONTH_{}'.format(date_column, index) for index, date_column in enumerate(billing_date_column, 1)])
						#billing_date_column_joined = ",".join(["'{}'".format(billing_data) for billing_data in billing_date_column])
						#Columns = Columns.replace(']', ','+billing_date_column_joined+']')
						#tblColumns=list(eval(Columns))
						Sql.RunQuery("""INSERT QT__Billing_Matrix_Header (
										QUOTE_ID,QUOTE_NAME,QUOTE_RECORD_ID,{DateColumn},YEAR,ownerId, cartId
									)
									SELECT TOP 1
										QUOTE_ID,
										QUOTE_NAME,
										QUOTE_RECORD_ID,
										{SelectDateColoumn},
										{Year} as YEAR,
										{UserId} as ownerId,
										{CartId} as cartId
									FROM SAQIBP (NOLOCK)
									WHERE QUOTE_RECORD_ID='{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'""".format(
										QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id,DateColumn=date_columns,Year=no_of_year,SelectDateColoumn=header_select_date_columns,CartId=cart_id, UserId=cart_user_id
										))
						pivot_columns = ",".join(['[{}]'.format(billing_date) for billing_date in billing_date_column])
						
						for service_obj in services_obj:
							Qustr = "WHERE QUOTE_RECORD_ID='{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID = '{}' AND BILLING_DATE BETWEEN '{}' AND '{}'".format(self.contract_quote_record_id,self.quote_revision_record_id,
																							service_obj.SERVICE_ID, billing_date_column[0], billing_date_column[-1])				
							
							Sql.RunQuery("""INSERT QT__BM_YEAR_1 (
											ANNUAL_BILLING_AMOUNT,BILLING_START_DATE,BILLING_END_DATE,
											BILLING_INTERVAL,BILLING_TYPE,BILLING_YEAR,EQUIPMENT_DESCRIPTION,EQUIPMENT_ID,
											GREENBOOK,GREENBOOK_RECORD_ID,ITEM_LINE_ID,PO_ITEM,PO_NUMBER,QUOTE_CURRENCY,
											QUOTE_CURRENCY_RECORD_ID,QUOTE_ID,QUOTE_NAME,QUOTE_RECORD_ID,QTEITMCOB_RECORD_ID,
											QTEITM_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,SERIAL_NUMBER,SERVICE_DESCRIPTION,
											SERVICE_ID,SERVICE_RECORD_ID,WARRANTY_END_DATE,WARRANTY_START_DATE,YEAR,EQUIPMENT_QUANTITY,
											{DateColumn},ownerId, cartId
										)
										SELECT  ANNUAL_BILLING_AMOUNT,BILLING_START_DATE,
													BILLING_END_DATE,BILLING_INTERVAL,BILLING_TYPE,{BillingYear} as BILLING_YEAR,
													EQUIPMENT_DESCRIPTION,EQUIPMENT_ID,GREENBOOK,GREENBOOK_RECORD_ID,
													ITEM_LINE_ID,PO_ITEM,PO_NUMBER,BILLING_CURRENCY,
													BILLING_CURRENCY_RECORD_ID,QUOTE_ID,QUOTE_NAME,QUOTE_RECORD_ID,QTEITMCOB_RECORD_ID,
													QTEITM_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,SERIAL_NUMBER,
													SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,WARRANTY_END_DATE,
													WARRANTY_START_DATE,YEAR,EQUIPMENT_QUANTITY,{SelectDateColoumn},{UserId} as ownerId,{CartId} as cartId
											FROM (
												SELECT 
													ANNUAL_BILLING_AMOUNT,BILLING_AMOUNT,BILLING_DATE,BILLING_START_DATE,
													BILLING_END_DATE,BILLING_INTERVAL,BILLING_TYPE,{BillingYear} as BILLING_YEAR,
													EQUIPMENT_DESCRIPTION,EQUIPMENT_ID,GREENBOOK,GREENBOOK_RECORD_ID,
													LINE_ITEM_ID as ITEM_LINE_ID,PO_ITEM,PO_NUMBER,BILLING_CURRENCY,
													BILLING_CURRENCY_RECORD_ID,QUOTE_ID,QUOTE_NAME,QUOTE_RECORD_ID,QTEITMCOB_RECORD_ID,
													QTEITM_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,SERIAL_NUMBER,
													SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,WARRANTY_END_DATE,
													WARRANTY_START_DATE,{BillingYear} as YEAR,EQUIPMENT_QUANTITY
												FROM SAQIBP 
												{WhereString}
											) AS IQ
											PIVOT
											(
												SUM(BILLING_AMOUNT)
												FOR BILLING_DATE IN ({PivotColumns})
											)AS PVT ORDER BY GREENBOOK
										""".format(BillingYear=no_of_year,WhereString=Qustr, PivotColumns=pivot_columns, 
												DateColumn=date_columns, SelectDateColoumn=select_date_columns,CartId=cart_id, UserId=cart_user_id,)								
										)
								
							# Total based on service - start
							Sql.RunQuery("""INSERT QT__BM_YEAR_1 (
											ANNUAL_BILLING_AMOUNT,BILLING_YEAR,QUOTE_CURRENCY,
											QUOTE_CURRENCY_RECORD_ID,QUOTE_ID,QUOTE_NAME,QUOTE_RECORD_ID,SERVICE_DESCRIPTION,
											SERVICE_ID,SERVICE_RECORD_ID,YEAR,EQUIPMENT_QUANTITY,
											{DateColumn},ownerId, cartId
										)
										SELECT SUM(CONVERT(BIGINT, ANNUAL_BILLING_AMOUNT)) AS ANNUAL_BILLING_AMOUNT,{BillingYear} as BILLING_YEAR,
													BILLING_CURRENCY,BILLING_CURRENCY_RECORD_ID,QUOTE_ID,QUOTE_NAME,QUOTE_RECORD_ID,													
													SERVICE_DESCRIPTION,CONCAT(SERVICE_ID, ' TOTAL') as SERVICE_ID,SERVICE_RECORD_ID,
													YEAR,SUM(EQUIPMENT_QUANTITY) AS EQUIPMENT_QUANTITY,{SumSelectDateColoumn},{UserId} as ownerId,{CartId} as cartId
											FROM (
												SELECT 
													ANNUAL_BILLING_AMOUNT,BILLING_AMOUNT,BILLING_DATE,{BillingYear} as BILLING_YEAR,													
													BILLING_CURRENCY, BILLING_CURRENCY_RECORD_ID,QUOTE_ID,QUOTE_NAME,QUOTE_RECORD_ID,
													SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,
													{BillingYear} as YEAR, EQUIPMENT_QUANTITY
												FROM SAQIBP 
												{WhereString}
											) AS IQ
											PIVOT
											(
												SUM(BILLING_AMOUNT)
												FOR BILLING_DATE IN ({PivotColumns})
											)AS PVT GROUP BY QUOTE_ID,QUOTE_NAME,QUOTE_RECORD_ID,
													SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,BILLING_CURRENCY, BILLING_CURRENCY_RECORD_ID,YEAR, EQUIPMENT_QUANTITY
										""".format(BillingYear=no_of_year,WhereString=Qustr, PivotColumns=pivot_columns, 
												DateColumn=date_columns, SumSelectDateColoumn=sum_select_date_columns,CartId=cart_id, UserId=cart_user_id,)								
										)
							# Total based on service - end
	
	def getting_cps_tax(self, item_obj=None, quote_type=None, item_lines_obj=None):		
		webclient = System.Net.WebClient()
		webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/json"
		webclient.Headers[System.Net.HttpRequestHeader.Authorization] = "Basic c2ItYzQwYThiMWYtYzU5NS00ZWJjLTkyYzYtYzM4ODg4ODFmMTY0IWIyNTAzfGNwc2VydmljZXMtc2VjdXJlZCFiMzkxOm9zRzgvSC9hOGtkcHVHNzl1L2JVYTJ0V0FiMD0=";
		response = webclient.DownloadString("https://cpqprojdevamat.authentication.us10.hana.ondemand.com:443/oauth/token?grant_type=client_credentials")
		response = eval(response)
		
		Request_URL="https://cpservices-pricing.cfapps.us10.hana.ondemand.com/api/v1/statelesspricing"
		webclient.Headers[System.Net.HttpRequestHeader.Authorization] ="Bearer "+str(response['access_token'])

		x = datetime.datetime.today()
		x= str(x)
		y = x.split(" ")
		GetPricingProcedure = Sql.GetFirst("SELECT ISNULL(DIVISION_ID, '') as DIVISION_ID,ISNULL(COUNTRY, '') as COUNTRY, ISNULL(DISTRIBUTIONCHANNEL_ID, '') as DISTRIBUTIONCHANNEL_ID, ISNULL(SALESORG_ID, '') as SALESORG_ID, ISNULL(DOC_CURRENCY,'') as DOC_CURRENCY, ISNULL(PRICINGPROCEDURE_ID,'') as PRICINGPROCEDURE_ID, QUOTE_RECORD_ID FROM SAQTRV (NOLOCK) WHERE QUOTE_ID = '{}'".format(self.contract_quote_id))
		if GetPricingProcedure is not None:			
			PricingProcedure = GetPricingProcedure.PRICINGPROCEDURE_ID
			curr = GetPricingProcedure.DOC_CURRENCY
			dis = GetPricingProcedure.DISTRIBUTIONCHANNEL_ID
			salesorg = GetPricingProcedure.SALESORG_ID
			div = GetPricingProcedure.DIVISION_ID
			#exch = GetPricingProcedure.EXCHANGE_RATE_TYPE
			#taxk1 = GetPricingProcedure.CUSTAXCLA_ID
			country = GetPricingProcedure.COUNTRY
		#update_SAQITM = "UPDATE SAQITM SET PRICINGPROCEDURE_ID = '{prc}' WHERE SAQITM.QUOTE_ID = '{quote}'".format(prc=str(PricingProcedure), quote=self.contract_quote_id)
		#Sql.RunQuery(update_SAQITM)		
		
		STPObj=Sql.GetFirst("SELECT ACCOUNT_ID FROM SAOPQT (NOLOCK) WHERE QUOTE_ID ='{quote}'".format(quote=self.contract_quote_id))		
		stp_account_id = ""
		if STPObj:
			stp_account_id = str(STPObj.ACCOUNT_ID)		
		
		if item_obj:			
			item_string = '{"itemId":"1","externalId":null,"quantity":{"value":'+str(1)+',"unit":"EA"},"exchRateType":"'+str(exch)+'","exchRateDate":"'+str(y[0])+'","productDetails":{"productId":"'+str(self.tree_param)+'","baseUnit":"EA","alternateProductUnits":null},"attributes":[{"name":"KOMK-LAND1","values":["'+country+'"]},{"name":"KOMK-ALAND","values":["'+country+'"]},{"name":"KOMK-REGIO","values":["TX"]},{"name":"KOMK-KUNNR","values":["'+stp_account_id+'"]},{"name":"KOMK-KUNWE","values":["'+stp_account_id+'"]},{"name":"KOMP-TAXM1","values":["'+str(item_obj.SRVTAXCLA_ID)+'"]},{"name":"KOMK-TAXK1","values":["'+str(taxk1)+'"]},{"name":"KOMK-SPART","values":["'+str(div)+'"]},{"name":"KOMP-SPART","values":["'+str(div)+'"]},{"name":"KOMP-PMATN","values":["'+str(self.tree_param)+'"]},{"name":"KOMK-WAERK","values":["'+str(curr)+'"]},{"name":"KOMK-HWAER","values":["'+str(curr)+'"]},{"name":"KOMP-PRSFD","values":["X"]},{"name":"KOMK-VTWEG","values":["'+str(dis)+'"]},{"name":"KOMK-VKORG","values":["'+str(salesorg)+'"]},{"name":"KOMP-KPOSN","values":["0"]},{"name":"KOMP-KZNEP","values":[""]},{"name":"KOMP-ZZEXE","values":["true"]}],"accessDateList":[{"name":"KOMK-PRSDT","value":"'+str(y[0])+'"},{"name":"KOMK-FBUDA","value":"'+str(y[0])+'"}],"variantConditions":[],"statistical":true,"subItems":[]}'
			requestdata = '{"docCurrency":"'+curr+'","locCurrency":"'+curr+'","pricingProcedure":"'+PricingProcedure+'","groupCondition":false,"itemConditionsRequired":true,"items": ['+str(item_string)+']}'
			response1 = webclient.UploadString(Request_URL,str(requestdata))			
			response1 = str(response1).replace(": true", ': "true"').replace(": false", ': "false"').replace(": null",': " None"')
			response1 = eval(response1)
			
			price = []
			for root, value in response1.items():
				if root == "items":
					price = value[:]
					break
			tax_percentage = 0
			for data in price[0]['conditions']:
				if data['conditionType'] == 'ZWSC' and data['conditionTypeDescription'] == 'VAT Asia':
					tax_percentage = data['conditionRate']
					break
			
			update_tax = "UPDATE SAQITM SET TAX_PERCENTAGE = {TaxPercentage} WHERE SAQITM.QUOTE_ITEM_RECORD_ID = '{ItemRecordId}'".format(
			TaxPercentage=tax_percentage,			
			ItemRecordId=item_obj.QUOTE_ITEM_RECORD_ID
			)
			Sql.RunQuery(update_tax)
						
			update_tax_quote_itm = "UPDATE QT__SAQITM SET TAX_PERCENTAGE = {TaxPercentage} WHERE QT__SAQITM.QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'".format(
			TaxPercentage=tax_percentage,			
			QuoteRecordId=self.contract_quote_record_id,
			RevisionRecordId=self.quote_revision_record_id
			)
			Sql.RunQuery(update_tax_quote_itm)
			update_tax_quote_ico = "UPDATE QT__SAQIFP SET TAX_PERCENTAGE = {TaxPercentage} WHERE QT__SAQIFP.QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'".format(
			TaxPercentage=tax_percentage,			
			QuoteRecordId=self.contract_quote_record_id,
			RevisionRecordId=self.quote_revision_record_id
			)
			Sql.RunQuery(update_tax_quote_ico)
			if quote_type == 'tool':
				update_tax_item_covered_obj = "UPDATE SAQICO SET TAX_PERCENTAGE = {TaxPercentage} WHERE SAQICO.SERVICE_ID = '{ServiceId}' and QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' ".format(
				TaxPercentage=tax_percentage,			
				ServiceId=self.tree_param,
				QuoteRecordId=self.contract_quote_record_id,
				RevisionRecordId=self.quote_revision_record_id
				)
				Sql.RunQuery(update_tax_item_covered_obj)
		if item_lines_obj:			
			items_data = []
			for item_line_obj in item_lines_obj:
				itemid = str(item_line_obj.EQUIPMENT_ID)+";"+str(self.contract_quote_id)+";"+str(1)
				#item_string = '{"itemId":"'+str(itemid)+'","externalId":null,"quantity":{"value":'+str(item_line_obj.EQUIPMENT_QUANTITY)+',"unit":"EA"},"exchRateType":"'+str(exch)+'","exchRateDate":"'+str(y[0])+'","productDetails":{"productId":"'+str(item_line_obj.EQUIPMENT_ID)+'","baseUnit":"EA","alternateProductUnits":null},"attributes":[{"name":"KOMK-LAND1","values":["CN"]},{"name":"KOMK-ALAND","values":["CN"]},{"name":"KOMK-REGIO","values":["TX"]},{"name":"KOMK-KUNNR","values":["'+stp_account_id+'"]},{"name":"KOMK-KUNWE","values":["'+stp_account_id+'"]},{"name":"KOMP-TAXM1","values":["'+str(item_line_obj.SRVTAXCLA_ID)+'"]},{"name":"KOMK-TAXK1","values":["'+str(taxk1)+'"]},{"name":"KOMK-SPART","values":["'+str(div)+'"]},{"name":"KOMP-SPART","values":["'+str(div)+'"]},{"name":"KOMP-PMATN","values":["'+str(item_line_obj.EQUIPMENT_ID)+'"]},{"name":"KOMK-WAERK","values":["'+str(curr)+'"]},{"name":"KOMK-HWAER","values":["'+str(curr)+'"]},{"name":"KOMP-PRSFD","values":["X"]},{"name":"KOMK-VTWEG","values":["'+str(dis)+'"]},{"name":"KOMK-VKORG","values":["'+str(salesorg)+'"]},{"name":"KOMP-KPOSN","values":["0"]},{"name":"KOMP-KZNEP","values":[""]},{"name":"KOMP-ZZEXE","values":["true"]}],"accessDateList":[{"name":"KOMK-PRSDT","value":"'+str(y[0])+'"},{"name":"KOMK-FBUDA","value":"'+str(y[0])+'"}],"variantConditions":[],"statistical":true,"subItems":[]}'
				item_string = '{"itemId":"'+str(itemid)+'","externalId":null,"quantity":{"value":'+str(1)+',"unit":"EA"},"exchRateType":"'+str(exch)+'","exchRateDate":"'+str(y[0])+'","productDetails":{"productId":"'+str(item_line_obj.EQUIPMENT_ID)+'","baseUnit":"EA","alternateProductUnits":null},"attributes":[{"name":"KOMK-LAND1","values":["CN"]},{"name":"KOMK-ALAND","values":["CN"]},{"name":"KOMK-REGIO","values":["TX"]},{"name":"KOMK-KUNNR","values":["'+stp_account_id+'"]},{"name":"KOMK-KUNWE","values":["'+stp_account_id+'"]},{"name":"KOMP-TAXM1","values":["'+str(item_line_obj.SRVTAXCLA_ID)+'"]},{"name":"KOMK-TAXK1","values":["'+str(taxk1)+'"]},{"name":"KOMK-SPART","values":["'+str(div)+'"]},{"name":"KOMP-SPART","values":["'+str(div)+'"]},{"name":"KOMP-PMATN","values":["'+str(item_line_obj.EQUIPMENT_ID)+'"]},{"name":"KOMK-WAERK","values":["'+str(curr)+'"]},{"name":"KOMK-HWAER","values":["'+str(curr)+'"]},{"name":"KOMP-PRSFD","values":["X"]},{"name":"KOMK-VTWEG","values":["'+str(dis)+'"]},{"name":"KOMK-VKORG","values":["'+str(salesorg)+'"]},{"name":"KOMP-KPOSN","values":["0"]},{"name":"KOMP-KZNEP","values":[""]},{"name":"KOMP-ZZEXE","values":["true"]}],"accessDateList":[{"name":"KOMK-PRSDT","value":"'+str(y[0])+'"},{"name":"KOMK-FBUDA","value":"'+str(y[0])+'"}],"variantConditions":[],"statistical":true,"subItems":[]}'
				items_data.append(item_string)
			items_string = ','.join(items_data)
			requestdata = '{"docCurrency":"'+curr+'","locCurrency":"'+curr+'","pricingProcedure":"'+PricingProcedure+'","groupCondition":false,"itemConditionsRequired":true,"items": ['+str(items_string)+']}'
			response1 = webclient.UploadString(Request_URL,str(requestdata))			
			response1 = str(response1).replace(": true", ': "true"').replace(": false", ': "false"').replace(": null",': " None"')
			response1 = eval(response1)
			price = []
			for root, value in response1.items():
				if root == "items":
					price = value[:]
					break
			update_data = []
			batch_group_record_id = str(Guid.NewGuid()).upper()
			for data in price:
				equipment_id = str(data["itemId"]).split(";")[0]
				tax_percentage = 0
				for condition_obj in data['conditions']:
					if condition_obj['conditionType'] == 'ZWSC' and condition_obj['conditionTypeDescription'] == 'VAT Asia':
						tax_percentage = condition_obj['conditionRate']
						break
				update_data.append((str(Guid.NewGuid()).upper(), equipment_id, 1, 'IN PROGRESS', self.contract_quote_id, self.contract_quote_record_id, batch_group_record_id, tax_percentage))
			
			update_data_joined = ', '.join(map(str, update_data))
			self._process_query("""INSERT INTO SYSPBT(BATCH_RECORD_ID, SAP_PART_NUMBER, QUANTITY, BATCH_STATUS, QUOTE_ID, QUOTE_RECORD_ID, BATCH_GROUP_RECORD_ID, TAX_PERCENTAGE) 
									SELECT * FROM (VALUES {}) QS (BATCH_RECORD_ID, SAP_PART_NUMBER, QUANTITY, BATCH_STATUS, QUOTE_ID, QUOTE_RECORD_ID, BATCH_GROUP_RECORD_ID, TAX_PERCENTAGE)""".format(update_data_joined))											
			self._process_query("""UPDATE SAQICO
					SET
					SAQICO.TAX_PERCENTAGE = IQ.TAX_PERCENTAGE
					FROM SAQICO
					INNER JOIN (
						SELECT SAQICO.CpqTableEntryId, SYSPBT.TAX_PERCENTAGE
						FROM SYSPBT (NOLOCK) 
						JOIN SAQICO (NOLOCK) ON SAQICO.QUOTE_RECORD_ID = SYSPBT.QUOTE_RECORD_ID AND SAQICO.QTEREV_RECORD_ID = SYSPBT.QTEREV_RECORD_ID AND SAQICO.EQUIPMENT_ID = SYSPBT.SAP_PART_NUMBER						
						WHERE SYSPBT.QUOTE_RECORD_ID ='{QuoteRecordId}' AND SYSPBT.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}' AND SYSPBT.BATCH_STATUS = 'IN PROGRESS'								
					)AS IQ
					ON SAQICO.CpqTableEntryId = IQ.CpqTableEntryId""".format(BatchGroupRecordId=batch_group_record_id, QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id))

			self._process_query(
					"""DELETE FROM SYSPBT WHERE SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}' and SYSPBT.QTEREV_RECORD_ID = '{RevisionRecordId}' and SYSPBT.BATCH_STATUS = 'IN PROGRESS'""".format(
						BatchGroupRecordId=batch_group_record_id,RevisionRecordId=self.quote_revision_record_id
					)
				)


class ContractQuoteOfferingsModel(ContractQuoteCrudOpertion):
	def __init__(self, **kwargs):
		ContractQuoteCrudOpertion.__init__(self, trigger_from=kwargs.get('trigger_from'), contract_quote_record_id=kwargs.get('contract_quote_record_id'),quote_revision_record_id=kwargs.get('quote_revision_record_id'), 
											tree_param=kwargs.get('tree_param'), tree_parent_level_0=kwargs.get('tree_parent_level_0'))
		self.opertion = kwargs.get('opertion')
		self.action_type = kwargs.get('action_type')
		self.values = kwargs.get('values')
		self.table_name = kwargs.get('table_name')
		self.all_values = kwargs.get('all_values')		
		self.node_id = ""
	
	def _insert_quote_line_items(self, cart_id, cart_user_id):
		Bundle_Query = ''
		
		if self.tree_parent_level_0 == 'Comprehensive Services':			
			Bundle_Query = Sql.GetFirst("SELECT ADNPRD_ID FROM SAQSAO (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(self.contract_quote_record_id, self.tree_param,self.quote_revision_record_id))
		elif self.tree_parent_level_0 == 'Add-On Products':			
			Bundle_Query = Sql.GetFirst("SELECT SERVICE_ID,SERVICE_DESCRIPTION FROM SAQSAO (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND ADNPRD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(self.contract_quote_record_id, self.tree_param,self.quote_revision_record_id))
			Bundle_Query_addon = Sql.GetFirst("SELECT ADNPRD_ID,ADNPRD_DESCRIPTION FROM SAQSAO (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND ADNPRD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(self.contract_quote_record_id, self.tree_param,self.quote_revision_record_id))
		
		if Bundle_Query:			
			if Bundle_Query and self.tree_parent_level_0 == 'Add-On Products':
				bundleser = Bundle_Query.SERVICE_ID + " - BUNDLE"
				if Bundle_Query_addon:
					bundledes =Bundle_Query.SERVICE_DESCRIPTION+ " WITH " + Bundle_Query_addon.ADNPRD_DESCRIPTION
				else:
					bundledes = ''
			else:
				bundleser = self.tree_param + " - BUNDLE"
				bundledes = ''
			
			self._process_query("""INSERT QT__SAQITM (
						ITEM_LINE_ID, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, QTY_OF_TOOLS, CURRENCY, UNIT_PRICE, EXTENDED_UNIT_PRICE,
						QUANTITY, FORECAST_VALUE, ONSITE_PURCHASE_COMMIT, QUOTE_ID, QUOTE_RECORD_ID, TAX_PERCENTAGE, TAX,  ownerId, cartId
					) 
					SELECT 
						SAQITM.LINE_ITEM_ID as ITEM_LINE_ID,
						'{bundledescription}' as SERVICE_DESCRIPTION,
						REPLACE(SAQITM.SERVICE_ID , '- BUNDLE', '') as SERVICE_ID,
						SAQITM.SERVICE_RECORD_ID,					
						0 AS QTY_OF_TOOLS,
						SAQITM.CURRENCY,
						(SAQITM.NET_VALUE-SAQITM.TAX) as UNIT_PRICE,
						SAQITM.NET_VALUE as EXTENDED_UNIT_PRICE,
						SAQITM.QUANTITY,
						0 AS FORECAST_VALUE,
						SAQITM.ONSITE_PURCHASE_COMMIT,
						SAQITM.QUOTE_ID,
						SAQITM.QUOTE_RECORD_ID,
						SAQITM.TAX_PERCENTAGE,
						SAQITM.TAX,
						{UserId} as ownerId,
						{CartId} as cartId
					FROM SAQITM (NOLOCK) 
					JOIN SAQTSV (NOLOCK) ON SAQTSV.SERVICE_RECORD_ID = SAQITM.SERVICE_RECORD_ID AND SAQTSV.QUOTE_RECORD_ID = SAQITM.QUOTE_RECORD_ID AND SAQTSV.QTEREV_RECORD_ID = SAQITM.QTEREV_RECORD_ID               
					WHERE SAQITM.QUOTE_RECORD_ID='{QuoteRecordId}' AND SAQITM.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQITM.SERVICE_ID = '{ServiceId}' """.format(
						CartId=cart_id, UserId=cart_user_id, QuoteRecordId=self.contract_quote_record_id,
						RevisionRecordId=self.quote_revision_record_id,
						ServiceId=bundleser,bundledescription = bundledes,))
			Sql.RunQuery("""INSERT QT__SAQITM (
						ITEM_LINE_ID, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, QTY_OF_TOOLS, CURRENCY, UNIT_PRICE, EXTENDED_UNIT_PRICE,
						QUANTITY, FORECAST_VALUE, ONSITE_PURCHASE_COMMIT, QUOTE_ID, QUOTE_RECORD_ID, TAX_PERCENTAGE, TAX,  ownerId, cartId
					) 
					SELECT 
						SAQITM.LINE_ITEM_ID as ITEM_LINE_ID,
						SAQITM.SERVICE_DESCRIPTION as SERVICE_DESCRIPTION,
						SUBSTRING(SAQITM.SERVICE_ID , 9, 13) as SERVICE_ID,
						SAQITM.SERVICE_RECORD_ID,					
						0 AS QTY_OF_TOOLS,
						SAQITM.CURRENCY,
						(SAQITM.NET_VALUE-SAQITM.TAX) as UNIT_PRICE,
						SAQITM.NET_VALUE as EXTENDED_UNIT_PRICE,
						SAQITM.QUANTITY,
						0 AS FORECAST_VALUE,
						SAQITM.ONSITE_PURCHASE_COMMIT,
						SAQITM.QUOTE_ID,
						SAQITM.QUOTE_RECORD_ID,
						SAQITM.TAX_PERCENTAGE,
						SAQITM.TAX,
						{UserId} as ownerId,
						{CartId} as cartId
					FROM SAQITM (NOLOCK)                 
					WHERE SAQITM.QUOTE_RECORD_ID='{QuoteRecordId}'  AND SAQITM.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQITM.SERVICE_ID LIKE '%ADDON%' """.format(
						CartId=cart_id, UserId=cart_user_id, QuoteRecordId=self.contract_quote_record_id,
						RevisionRecordId=self.quote_revision_record_id,
						ServiceId=bundleser,bundledescription = bundledes))			
		else:
			self._process_query("""INSERT QT__SAQITM (
						ITEM_LINE_ID, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, QTY_OF_TOOLS, CURRENCY, UNIT_PRICE, EXTENDED_UNIT_PRICE,
						QUANTITY, FORECAST_VALUE, ONSITE_PURCHASE_COMMIT, QUOTE_ID, QUOTE_RECORD_ID, TAX_PERCENTAGE, TAX,  ownerId, cartId
					) 
					SELECT 
						SAQITM.LINE_ITEM_ID as ITEM_LINE_ID,
						SAQITM.SERVICE_DESCRIPTION,
						REPLACE(SAQITM.SERVICE_ID , '- BASE', '') as SERVICE_ID,
						SAQITM.SERVICE_RECORD_ID,					
						0 AS QTY_OF_TOOLS,
						SAQITM.CURRENCY,
						(SAQITM.NET_VALUE-SAQITM.TAX) as UNIT_PRICE,
						SAQITM.NET_VALUE as EXTENDED_UNIT_PRICE,
						SAQITM.QUANTITY,
						0 AS FORECAST_VALUE,
						SAQITM.ONSITE_PURCHASE_COMMIT,
						SAQITM.QUOTE_ID,
						SAQITM.QUOTE_RECORD_ID,
						SAQITM.TAX_PERCENTAGE,
						SAQITM.TAX,
						{UserId} as ownerId,
						{CartId} as cartId
					FROM SAQITM (NOLOCK) 
					JOIN SAQTSV (NOLOCK) ON SAQTSV.SERVICE_RECORD_ID = SAQITM.SERVICE_RECORD_ID AND SAQTSV.QUOTE_RECORD_ID = SAQITM.QUOTE_RECORD_ID  AND SAQTSV.QTEREV_RECORD_ID = SAQITM.QTEREV_RECORD_ID              
					WHERE SAQITM.QUOTE_RECORD_ID='{QuoteRecordId}' AND SAQITM.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQTSV.SERVICE_ID = '{ServiceId}' """.format(
						CartId=cart_id, UserId=cart_user_id, QuoteRecordId=self.contract_quote_record_id,
						RevisionRecordId=self.quote_revision_record_id,
						ServiceId=self.tree_param,))
		if self.tree_param == 'Z0068' and self.tree_parent_level_0 == 'Add-On Products':
			self._process_query("""UPDATE A SET A.TARGET_PRICE = B.TARGET_PRICE,A.SALES_PRICE = B.SALES_PRICE,A.CEILING_PRICE = B.CEILING_PRICE,A.TOTAL_COST = B.TOTAL_COST,A.EXTENDED_PRICE = B.EXTENDED_PRICE,A.TAX = B.TAX,A.PRICING_STATUS = 'ACQUIRED' FROM QT__SAQITM A(NOLOCK) JOIN (SELECT SUM(TARGET_PRICE) AS TARGET_PRICE,SUM(SALES_PRICE) AS SALES_PRICE,SUM(CEILING_PRICE) AS CEILING_PRICE,SUM(TOTAL_COST) AS TOTAL_COST,SUM(EXTENDED_PRICE) AS EXTENDED_PRICE,SUM(TAX) AS TAX,QUOTE_RECORD_ID,SERVICE_RECORD_ID from QT__SAQICO(NOLOCK) WHERE QUOTE_RECORD_ID ='{QuoteRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' and SERVICE_ID='{Service_id}' GROUP BY QUOTE_RECORD_ID,SERVICE_RECORD_ID) B ON A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID  AND A.QTEREV_RECORD_ID = B.QTEREV_RECORD_ID
			AND A.SERVICE_RECORD_ID=B.SERVICE_RECORD_ID """.format(			
			QuoteRecordId=self.contract_quote_record_id,
			RevisionRecordId=self.quote_revision_record_id,
			Service_id =self.tree_param))				
		""" if Quote is not None:
			Quote.QuoteTables["SAQITM"].Save()
			Quote.QuoteTables["SAQICO"].Save()
			Quote.QuoteTables["SAQIFP"].Save()
			Quote.Save() """
		return True

	def _delete_quote_line_items(self, cart_id, cart_user_id):
		self._process_query("""DELETE QT__SAQITM FROM QT__SAQITM 
								JOIN SAQTSV (NOLOCK) ON SAQTSV.SERVICE_RECORD_ID = QT__SAQITM.SERVICE_RECORD_ID AND SAQTSV.QUOTE_RECORD_ID = QT__SAQITM.QUOTE_RECORD_ID  AND SAQTSV.QTEREV_RECORD_ID = QT__SAQITM.QTEREV_RECORD_ID
								WHERE QT__SAQITM.cartId = '{CartId}' AND ownerId = {UserId} AND QT__SAQITM.QUOTE_RECORD_ID = '{QuoteRecordId}' AND QT__SAQITM.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQTSV.SERVICE_DESCRIPTION = '{ServiceId}'""".format(
									CartId=cart_id, UserId=cart_user_id, QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id, ServiceId=self.tree_param))
		return True
	
	def _insert_quote_spare_parts(self, cart_id, cart_user_id):		
		self._process_query("""INSERT QT__SAQIFP (
					QUOTE_ITEM_FORECAST_PART_RECORD_ID, ANNUAL_QUANTITY, BASEUOM_RECORD_ID, CUSTOMER_PART_NUMBER, 
					CUSTOMER_PART_NUMBER_RECORD_ID, DELIVERY_MODE, EXTENDED_UNIT_PRICE, ITEM_LINE_ID, PART_DESCRIPTION, PART_NUMBER, 
					PART_RECORD_ID, QUOTE_ID, QTEITM_RECORD_ID, QUOTE_NAME, QUOTE_RECORD_ID, SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID,
					SALESUOM_CONVERSION_FACTOR, SCHEDULE_MODE, SERVICE_DESCRIPTION, SERVICE_ID,
					SERVICE_RECORD_ID, UNIT_PRICE, VALID_FROM_DATE, VALID_TO_DATE, MATPRIGRP_ID, MATPRIGRP_NAME, MATPRIGRP_RECORD_ID, PART_LINE_ID, ownerId, cartId
				) 
				SELECT 
					CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_FORECAST_PART_RECORD_ID,  
					SAQIFP.ANNUAL_QUANTITY,
					SAQIFP.BASEUOM_RECORD_ID,
					SAQIFP.PART_NUMBER AS CUSTOMER_PART_NUMBER,
					SAQIFP.PART_RECORD_ID AS CUSTOMER_PART_NUMBER_RECORD_ID,
					SAQIFP.DELIVERY_MODE,
					SAQIFP.EXTENDED_PRICE,
					SAQIFP.LINE as ITEM_LINE_ID,
					SAQIFP.PART_DESCRIPTION,
					SAQIFP.PART_NUMBER,
					SAQIFP.PART_RECORD_ID,
					SAQIFP.QUOTE_ID,
					SAQIFP.QTEITM_RECORD_ID,
					SAQIFP.QUOTE_NAME,
					SAQIFP.QUOTE_RECORD_ID,
					SAQIFP.SALESORG_ID,
					SAQIFP.SALESORG_NAME,
					SAQIFP.SALESORG_RECORD_ID,
					0 AS SALESUOM_CONVERSION_FACTOR,					
					SAQIFP.SCHEDULE_MODE,
					SAQIFP.SERVICE_DESCRIPTION,
					SAQTSV.SERVICE_ID,
					SAQIFP.SERVICE_RECORD_ID,
					SAQIFP.UNIT_PRICE,
					SAQIFP.VALID_FROM_DATE,
					SAQIFP.VALID_TO_DATE,
					SAQIFP.MATPRIGRP_ID,
					SAQIFP.MATPRIGRP_NAME,
					SAQIFP.MATPRIGRP_RECORD_ID,
					SAQIFP.PART_LINE_ID,
					{UserId} as ownerId,
					{CartId} as cartId
				FROM SAQIFP (NOLOCK) 
				JOIN SAQTSV (NOLOCK) ON SAQTSV.SERVICE_RECORD_ID = SAQIFP.SERVICE_RECORD_ID AND SAQTSV.QUOTE_RECORD_ID = SAQIFP.QUOTE_RECORD_ID AND SAQTSV.QTEREV_RECORD_ID = SAQIFP.QTEREV_RECORD_ID                
				WHERE SAQIFP.QUOTE_RECORD_ID='{QuoteRecordId}' AND SAQIFP.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQTSV.SERVICE_ID = '{ServiceId}'""".format(
					CartId=cart_id, UserId=cart_user_id, QuoteRecordId=self.contract_quote_record_id,
					RevisionRecordId=self.quote_revision_record_id,
					ServiceId=self.tree_param))
		if Quote is not None:
			Quote.QuoteTables["SAQITM"].Save()
			Quote.QuoteTables["SAQICO"].Save()
			Quote.QuoteTables["SAQIFP"].Save()
			Quote.Save() 
		return True
	
	def _delete_quote_spare_parts(self, cart_id, cart_user_id):
		self._process_query("""DELETE QT__SAQIFP 
								FROM QT__SAQIFP 
								JOIN SAQTSV (NOLOCK) ON SAQTSV.SERVICE_RECORD_ID = QT__SAQIFP.SERVICE_RECORD_ID AND SAQTSV.QUOTE_RECORD_ID = QT__SAQIFP.QUOTE_RECORD_ID AND SAQTSV.QTEREV_RECORD_ID = QT__SAQIFP.QTEREV_RECORD_ID
								WHERE QT__SAQIFP.cartId = '{CartId}' AND ownerId = {UserId} AND QT__SAQIFP.QUOTE_RECORD_ID = '{QuoteRecordId}'  AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQTSV.SERVICE_ID = '{ServiceId}'""".format(
									CartId=cart_id, UserId=cart_user_id, QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id, ServiceId=self.tree_param))
		return True

	def _create(self):		
		row_values = {}
		if self.action_type == "ADD_OFFERING":
			master_object_name = "MAMTRL"
			columns = [
				"SAP_PART_NUMBER AS SERVICE_ID",
				"SAP_DESCRIPTION AS SERVICE_DESCRIPTION",
				"MATERIAL_RECORD_ID AS SERVICE_RECORD_ID",
				"PRODUCT_TYPE AS SERVICE_TYPE",
				"UNIT_OF_MEASURE AS UOM_ID",
				"UOM_RECORD_ID AS UOM_RECORD_ID",
			]
			table_name = "SAQTSV"
			condition_column = "MATERIAL_RECORD_ID"
			row_values = {"QUOTE_NAME": self.contract_quote_name,
				"SALESORG_ID": self.salesorg_id,
				"SALESORG_NAME": self.salesorg_name,
				"SALESORG_RECORD_ID": self.salesorg_record_id,
				"QTEREV_RECORD_ID": self.quote_revision_record_id,
				"QTEREV_ID":self.quote_revision_id,
				"CONTRACT_VALID_FROM":self.contract_start_date,
				"CONTRACT_VALID_TO":self.contract_end_date}

			offering_table_info = Sql.GetTable(table_name)
			existing_offering_ids = []
			for row_detail in self._add_record(
				master_object_name=master_object_name,
				columns=columns,
				table_name=table_name,
				condition_column=condition_column,
				values=self.values,
			):
				check_existing_offerings_obj = self._get_record_obj(
					columns=["SERVICE_ID"],
					table_name=table_name,
					where_condition="QUOTE_SERVICE_RECORD_ID = '{}'".format(row_detail.get("QUOTE_SERVICE_RECORD_ID")),
					single_record=False,
				)
				if check_existing_offerings_obj:
					existing_offering_ids.extend(
						[
							check_existing_offering_obj.SERVICE_ID
							for check_existing_offering_obj in check_existing_offerings_obj
						]
					)
					if row_detail.get("SERVICE_ID") in existing_offering_ids:
						continue
					else:
						existing_offering_ids.append(row_detail.get("SERVICE_ID"))
				row_detail.update(row_values)
				offering_table_info.AddRow(row_detail)
				Sql.Upsert(offering_table_info)
				#service_obj  = Sql.GetFirst("select COUNT(SERVICE_ID) as count,SERVICE_ID from SAQTSV where QUOTE_RECORD_ID = '{}'".format(self.contract_quote_record_id))
				#if service_obj.count == 1:
				#	document_type_obj = Sql.GetFirst("select DOCTYP_ID from MAMADT where SAP_PART_NUMBER = '{}'".format(service_obj.SERVICE_ID))
				#	if document_type_obj is not None:
				#		self._process_query("UPDATE SAQTMT SET DOCUMENT_TYPE = '{}' WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{}'".format(document_type_obj.DOCTYP_ID,self.contract_quote_record_id))
				Trace.Write("row_detail--"+str(row_detail))
				self.CreateEntitlements(row_detail)
			##A055S000P01-8740 code starts...
			ScriptExecutor.ExecuteGlobal('CQDOCUTYPE',{'QUOTE_RECORD_ID':self.contract_quote_record_id,'QTEREV_RECORD_ID':self.quote_revision_record_id})
			##A055S000P01-8740 code ends...
			# ADD VD TO THE OFFERINGS
			#QTSID = str(row_detail["SERVICE_ID"])
			#Trace.Write("service_ID"+str(QTSID))
			#self._process_query(""" INSERT SAQSAO (QUOTE_SERVICE_ADD_ON_PRODUCT_RECORD_ID,ADNPRD_DESCRIPTION,ADNPRD_ID,ADNPRDOFR_RECORD_ID,ADNPRD_RECORD_ID,ADN_TYPE,QUOTE_ID,QUOTE_NAME,QUOTE_RECORD_ID,QTESRV_RECORD_ID,SALESORG_ID,SALESORG_NAME,ACTIVE,SALESORG_RECORD_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified) SELECT CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_ADD_ON_PRODUCT_RECORD_ID,MAADPR.ADNPRDOFR_NAME,MAADPR.ADNPRDOFR_ID,MAADPR.ADNPRDOFR_RECORD_ID,MAADPR.ADD_ON_PRODUCT_RECORD_ID,MAADPR.ADN_TYPE,SAQTSV.QUOTE_ID,SAQTSV.QUOTE_NAME,SAQTSV.QUOTE_RECORD_ID,SAQTSV.QUOTE_SERVICE_RECORD_ID,SAQTSV.SALESORG_ID,SAQTSV.SALESORG_NAME,'FALSE' as ACTIVE,SAQTSV.SALESORG_RECORD_ID,SAQTSV.SERVICE_DESCRIPTION,SAQTSV.SERVICE_ID,SAQTSV.SERVICE_RECORD_ID,'{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED, {UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM MAADPR (NOLOCK) INNER JOIN  SAQTSV ON MAADPR.PRDOFR_ID = SAQTSV.SERVICE_ID WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND SERVICE_ID ='{ServiceIds}' """.format(UserId=self.user_id,UserName=self.user_name,QuoteRecordId=self.contract_quote_record_id,ServiceIds=str(QTSID)))
		elif self.action_type == "ADD_SPARE_PARTS":
			if self.values:
				batch_group_record_id = str(Guid.NewGuid()).upper()
				#spare_parts_obj = re.finditer(r'([a-zA-Z0-9_\-.\(\)]*\s?[a-zA-Z0-9\-]?)\t+(\d*)', self.values[0])                         
				#spare_parts_details = [(str(Guid.NewGuid()).upper(), spare_part_obj.group(1), spare_part_obj.group(2), 'IN PROGRESS', self.contract_quote_id, self.contract_quote_record_id, batch_group_record_id) for spare_part_obj in spare_parts_obj]
				spare_parts_details = [(str(Guid.NewGuid()).upper(), spare_part, 1, 'IN PROGRESS', self.contract_quote_id, self.contract_quote_record_id, batch_group_record_id) for spare_part in self.values[0].splitlines()]
				
				spare_parts_details_joined = ', '.join(map(str, spare_parts_details))
				self._process_query("""INSERT INTO SYSPBT(BATCH_RECORD_ID, SAP_PART_NUMBER, QUANTITY, BATCH_STATUS, QUOTE_ID, QUOTE_RECORD_ID, BATCH_GROUP_RECORD_ID) 
										SELECT * FROM (VALUES {}) QS (BATCH_RECORD_ID, SAP_PART_NUMBER, QUANTITY, BATCH_STATUS, QUOTE_ID, QUOTE_RECORD_ID, BATCH_GROUP_RECORD_ID)""".format(spare_parts_details_joined))											
				self._process_query("""
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
										1 as QUANTITY,
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
									FROM SYSPBT (NOLOCK)
									JOIN MAMTRL (NOLOCK) ON MAMTRL.SAP_PART_NUMBER = SYSPBT.SAP_PART_NUMBER
									JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SYSPBT.QUOTE_RECORD_ID
									JOIN SAQTSV (NOLOCK) ON SAQTSV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SAQTSV.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID AND SAQTSV.SERVICE_ID = '{ServiceId}'
									JOIN MAMSOP (NOLOCK) ON MAMSOP.MATERIAL_RECORD_ID = MAMTRL.MATERIAL_RECORD_ID AND MAMSOP.SALESORG_RECORD_ID = SAQTSV.SALESORG_RECORD_ID
									WHERE SYSPBT.BATCH_STATUS = 'IN PROGRESS' AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}' AND SYSPBT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SYSPBT.QTEREV_RECORD_ID = '{RevisionRecordId}' AND MAMTRL.PRODUCT_TYPE IS NULL AND MAMTRL.IS_SPARE_PART = 1 ) IQ
									""".format(
						ServiceId=self.tree_param,
						BatchGroupRecordId=batch_group_record_id,
						QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id,
						UserId=self.user_id
					)
				)
				self._process_query(
					"""DELETE FROM SYSPBT WHERE SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}'  and SYSPBT.QTEREV_RECORD_ID = '{RevisionRecordId}' and SYSPBT.BATCH_STATUS = 'IN PROGRESS'""".format(
						BatchGroupRecordId=batch_group_record_id,RevisionRecordId=self.quote_revision_record_id
					)
				)
		return True

	def _update(self):
		pass

	def _delete(self):
		pass
	
	def CreateEntitlements(self,OfferingRow_detail):
		webclient = System.Net.WebClient()
		gettodaydate = datetime.datetime.now().strftime("%Y-%m-%d")
		webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/json"
		webclient.Headers[System.Net.HttpRequestHeader.Authorization] = "Basic c2ItYzQwYThiMWYtYzU5NS00ZWJjLTkyYzYtYzM4ODg4ODFmMTY0IWIyNTAzfGNwc2VydmljZXMtc2VjdXJlZCFiMzkxOm9zRzgvSC9hOGtkcHVHNzl1L2JVYTJ0V0FiMD0=";
		response = webclient.DownloadString("https://cpqprojdevamat.authentication.us10.hana.ondemand.com:443/oauth/token?grant_type=client_credentials")
		response = eval(response)
		Request_URL="https://cpservices-product-configuration.cfapps.us10.hana.ondemand.com/api/v2/configurations?autoCleanup=False"
		webclient.Headers[System.Net.HttpRequestHeader.Authorization] ="Bearer "+str(response['access_token'])
		requestdata= '{"productKey":"'+OfferingRow_detail.get("SERVICE_ID")+'","date":"'+gettodaydate+'","context":[{"name":"VBAP-MATNR","value":"'+OfferingRow_detail.get("SERVICE_ID")+'"}]}'
		Trace.Write('requestdata--'+str(requestdata))
		#if TreeSuperParentParam=="Offerings":
			#requestdata= '{"productKey":"'+TreeParam+'","date":"2020-10-14","context":[{"name":"VBAP-MATNR","value":"'+TreeParam+'"}]}'
			#ProductPartnumber=TreeParam
		#elif TreeTopSuperParentParam=="Offerings":
			#requestdata= '{"productKey":"'+TreeParentParam+'","date":"2020-09-01","context":[{"name":"VBAP-MATNR","value":"'+TreeParentParam+'"}]}'
			#ProductPartnumber=TreeParentParam
		
		response1 = webclient.UploadString(Request_URL,str(requestdata))
		response1=str(response1).replace(": true",": \"true\"").replace(": false",": \"false\"")
		Fullresponse= eval(response1)
		attributesdisallowedlst=[]
		attributeReadonlylst=[]
		attributesallowedlst=[]
		attributedefaultvalue = []
		#overallattributeslist =[]
		attributevalues={}
		for rootattribute, rootvalue in Fullresponse.items():
			if rootattribute=="rootItem":
				for Productattribute, Productvalue in rootvalue.items():
					if Productattribute=="characteristics":
						for prdvalue in Productvalue:
							#overallattributeslist.append(prdvalue['id'])
							if prdvalue['visible'] =='false':
								attributesdisallowedlst.append(prdvalue['id'])
							else:								
								attributesallowedlst.append(prdvalue['id'])
							if prdvalue['readOnly'] =='true':
								attributeReadonlylst.append(prdvalue['id'])
							for attribute in prdvalue['values']:								
								attributevalues[str(prdvalue['id'])]=attribute['value']
								if attribute["author"] in ('Default','System'):
									Trace.Write('prdvalue---1554-----'+str(prdvalue['id']))
									attributedefaultvalue.append(prdvalue["id"])
		attributesallowedlst = list(set(attributesallowedlst))
		#overallattributeslist = list(set(overallattributeslist))		
		HasDefaultvalue=False
		ProductVersionObj=Sql.GetFirst("Select product_id from product_versions(nolock) where SAPKBVersion='"+str(Fullresponse['kbKey']['version'])+"'")
		is_default = ent_val_code = ''			
		if ProductVersionObj:
			insertservice = ""
			tbrow={}	
			for attrs in attributesallowedlst:
				
				if attrs in attributevalues:					
					HasDefaultvalue=True					
					STANDARD_ATTRIBUTE_VALUES=Sql.GetFirst("SELECT S.STANDARD_ATTRIBUTE_DISPLAY_VAL,S.STANDARD_ATTRIBUTE_CODE FROM STANDARD_ATTRIBUTE_VALUES (nolock) S INNER JOIN ATTRIBUTE_DEFN (NOLOCK) A ON A.STANDARD_ATTRIBUTE_CODE=S.STANDARD_ATTRIBUTE_CODE WHERE A.SYSTEM_ID = '{}' ".format(attrs))
					ent_disp_val = attributevalues[attrs]
					ent_val_code = attributevalues[attrs]
					Trace.Write("ent_disp_val----"+str(ent_disp_val))
				else:					
					HasDefaultvalue=False
					ent_disp_val = ""
					ent_val_code = ""
					STANDARD_ATTRIBUTE_VALUES=Sql.GetFirst("SELECT S.STANDARD_ATTRIBUTE_CODE FROM STANDARD_ATTRIBUTE_VALUES (nolock) S INNER JOIN ATTRIBUTE_DEFN (NOLOCK) A ON A.STANDARD_ATTRIBUTE_CODE=S.STANDARD_ATTRIBUTE_CODE WHERE A.SYSTEM_ID = '{}'".format(attrs))
					
				ATTRIBUTE_DEFN=Sql.GetFirst("SELECT * FROM ATTRIBUTE_DEFN (NOLOCK) WHERE SYSTEM_ID='{}'".format(attrs))
				PRODUCT_ATTRIBUTES=Sql.GetFirst("SELECT A.ATT_DISPLAY_DESC FROM ATT_DISPLAY_DEFN (NOLOCK) A INNER JOIN PRODUCT_ATTRIBUTES (NOLOCK) P ON A.ATT_DISPLAY=P.ATT_DISPLAY WHERE P.PRODUCT_ID={} AND P.STANDARD_ATTRIBUTE_CODE={}".format(ProductVersionObj.product_id,STANDARD_ATTRIBUTE_VALUES.STANDARD_ATTRIBUTE_CODE))
				
				if PRODUCT_ATTRIBUTES.ATT_DISPLAY_DESC in ('Drop Down','Check Box') and ent_disp_val:
					get_display_val = Sql.GetFirst("SELECT STANDARD_ATTRIBUTE_DISPLAY_VAL  from STANDARD_ATTRIBUTE_VALUES S INNER JOIN ATTRIBUTE_DEFN (NOLOCK) A ON A.STANDARD_ATTRIBUTE_CODE=S.STANDARD_ATTRIBUTE_CODE WHERE S.STANDARD_ATTRIBUTE_CODE = '{}' AND A.SYSTEM_ID = '{}' AND S.STANDARD_ATTRIBUTE_VALUE = '{}' ".format(STANDARD_ATTRIBUTE_VALUES.STANDARD_ATTRIBUTE_CODE,attrs,  attributevalues[attrs] ) )
					ent_disp_val = get_display_val.STANDARD_ATTRIBUTE_DISPLAY_VAL 

				if str(attrs) == 'AGS_REL_STDATE' and 'Z0007' in OfferingRow_detail.get("SERVICE_ID"):
					try:						
						QuoteStartDate = datetime.datetime.strptime(Quote.GetCustomField('QuoteStartDate').Content, '%Y-%m-%d').date()
						ent_disp_val = 	str(QuoteStartDate)
						ent_val_code = ''					
					except:						
						ent_disp_val = ent_disp_val
						ent_val_code = ''
				else:
					ent_disp_val = ent_disp_val
					ent_val_code = ent_val_code
				if str(attrs) == 'AGS_CON_DAY' and 'Z0016' in OfferingRow_detail.get("SERVICE_ID"): 
					try:						
						QuoteEndDate = datetime.datetime.strptime(Quote.GetCustomField('QuoteExpirationDate').Content, '%Y-%m-%d').date()
						QuoteStartDate = datetime.datetime.strptime(Quote.GetCustomField('QuoteStartDate').Content, '%Y-%m-%d').date()
						contract_days = (QuoteEndDate - QuoteStartDate).days
						ent_disp_val = 	str(contract_days)
					except:						
						ent_disp_val = ent_disp_val	
				else:
					ent_disp_val = ent_disp_val	
				#A055S000P01-7401 START
				if str(attrs) == 'AGS_POA_PROD_TYPE' and ent_disp_val != '':
					val = ""
					if str(ent_disp_val) == 'Comprehensive':
						val = "COMPREHENSIVE SERVICES"
					elif str(ent_disp_val) == 'Complementary':
						val = "COMPLEMENTARY PRODUCTS"
					Sql.RunQuery("UPDATE SAQTSV SET SERVICE_TYPE = '{}' WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID = '{}'".format(str(val),self.contract_quote_record_id,self.quote_revision_record_id,OfferingRow_detail.get("SERVICE_ID")))
				#A055S000P01-7401 END
				DTypeset={"Drop Down":"DropDown","Free Input, no Matching":"FreeInputNoMatching","Check Box":"CheckBox"}
				insertservice += """<QUOTE_ITEM_ENTITLEMENT>
					<ENTITLEMENT_NAME>{ent_name}</ENTITLEMENT_NAME>
					<ENTITLEMENT_VALUE_CODE>{ent_val_code}</ENTITLEMENT_VALUE_CODE>
					<ENTITLEMENT_TYPE>{ent_type}</ENTITLEMENT_TYPE>
					<ENTITLEMENT_DISPLAY_VALUE>{ent_disp_val}</ENTITLEMENT_DISPLAY_VALUE>
					<ENTITLEMENT_DESCRIPTION>{ent_desc}</ENTITLEMENT_DESCRIPTION>
					<ENTITLEMENT_COST_IMPACT>{ct}</ENTITLEMENT_COST_IMPACT>
					<ENTITLEMENT_PRICE_IMPACT>{pi}</ENTITLEMENT_PRICE_IMPACT>
					<IS_DEFAULT>{is_default}</IS_DEFAULT>
					<PRICE_METHOD>{pm}</PRICE_METHOD>
					<CALCULATION_FACTOR>{cf}</CALCULATION_FACTOR>
					</QUOTE_ITEM_ENTITLEMENT>""".format(ent_name = str(attrs),ent_val_code = ent_val_code,ent_type = DTypeset[PRODUCT_ATTRIBUTES.ATT_DISPLAY_DESC] if PRODUCT_ATTRIBUTES else  '',ent_desc = ATTRIBUTE_DEFN.STANDARD_ATTRIBUTE_NAME,ent_disp_val = ent_disp_val if HasDefaultvalue==True else '',ct = '',pi = '',is_default = '1' if str(attrs) in attributedefaultvalue else '0',pm = '',cf = '')
			
			tbrow["QUOTE_SERVICE_ENTITLEMENT_RECORD_ID"]=str(Guid.NewGuid()).upper()
			tbrow["QUOTE_ID"]=OfferingRow_detail.get("QUOTE_ID")
			tbrow["ENTITLEMENT_XML"]=insertservice
			tbrow["QUOTE_NAME"]=OfferingRow_detail.get("QUOTE_NAME")
			tbrow["QUOTE_RECORD_ID"]=OfferingRow_detail.get("QUOTE_RECORD_ID")
			tbrow["QTESRV_RECORD_ID"]=OfferingRow_detail.get("QUOTE_SERVICE_RECORD_ID")
			tbrow["SERVICE_RECORD_ID"]=OfferingRow_detail.get("SERVICE_RECORD_ID")
			tbrow["SERVICE_ID"]=OfferingRow_detail.get("SERVICE_ID")
			tbrow["SERVICE_DESCRIPTION"]=OfferingRow_detail.get("SERVICE_DESCRIPTION")
			tbrow["CPS_CONFIGURATION_ID"]=Fullresponse['id']
			tbrow["SALESORG_RECORD_ID"]=OfferingRow_detail.get("SALESORG_RECORD_ID")
			tbrow["SALESORG_ID"]=OfferingRow_detail.get("SALESORG_ID")
			tbrow["SALESORG_NAME"]=OfferingRow_detail.get("SALESORG_NAME")
			tbrow["CPS_MATCH_ID"] = 11
			tbrow["CPQTABLEENTRYADDEDBY"] = self.user_id
			tbrow["CPQTABLEENTRYDATEADDED"] = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p")  
			tbrow["QTEREV_RECORD_ID"] = self.quote_revision_record_id
			tbrow["QTEREV_ID"] = self.quote_revision_id
			#tbrow["IS_DEFAULT"] = '1'

			columns = ', '.join("" + str(x) + "" for x in tbrow.keys())
			values = ', '.join("'" + str(x) + "'" for x in tbrow.values())
			insert_qtqtse_query = "INSERT INTO SAQTSE ( %s ) VALUES ( %s );" % (columns, values)
			Sql.RunQuery(insert_qtqtse_query)
			try:
				if OfferingRow_detail.get("SERVICE_ID") == 'Z0016':
					try:
						QuoteEndDate = datetime.datetime.strptime(Quote.GetCustomField('QuoteExpirationDate').Content, '%Y-%m-%d').date()
						QuoteStartDate = datetime.datetime.strptime(Quote.GetCustomField('QuoteStartDate').Content, '%Y-%m-%d').date()
						contract_days = (QuoteEndDate - QuoteStartDate).days
						ent_disp_val = 	str(contract_days)
					except:						
						ent_disp_val = ent_disp_val					
					cpsmatchID = tbrow["CPS_MATCH_ID"]
					cpsConfigID = Fullresponse['id']					
					webclient = System.Net.WebClient()
					webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/json"
					webclient.Headers[System.Net.HttpRequestHeader.Authorization] = "Basic c2ItYzQwYThiMWYtYzU5NS00ZWJjLTkyYzYtYzM4ODg4ODFmMTY0IWIyNTAzfGNwc2VydmljZXMtc2VjdXJlZCFiMzkxOm9zRzgvSC9hOGtkcHVHNzl1L2JVYTJ0V0FiMD0="
					response = webclient.DownloadString("https://cpqprojdevamat.authentication.us10.hana.ondemand.com:443/oauth/token?grant_type=client_credentials")
					response = eval(response)
					webclient = System.Net.WebClient()
					Request_URL = "https://cpservices-product-configuration.cfapps.us10.hana.ondemand.com/api/v2/configurations/"+str(cpsConfigID)+"/items/1"
					webclient.Headers[System.Net.HttpRequestHeader.Authorization] = "Bearer " + str(response["access_token"])
					#webclient.Headers.Add("If-Match", "111")

					webclient.Headers.Add("If-Match", "1"+str(cpsmatchID))
					RevisionRecordId=self.quote_revision_record_id		
					AttributeID = 'AGS_CON_DAY'
					NewValue = ent_disp_val
					whereReq = "QUOTE_RECORD_ID = '"+str(quote_record_id)+"' and SERVICE_ID like '%Z0016%' and QTEREV_RECORD_ID = '"+str(RevisionRecordId)+"' "

					requestdata = '{"characteristics":[{"id":"'+AttributeID+'","values":[{"value":"'+NewValue+'","selected":true}]}]}'
					#Log.Info("---eqruestdata---requestdata----"+str(requestdata))
					response2 = webclient.UploadString(Request_URL, "PATCH", str(requestdata))
										
					Request_URL = "https://cpservices-product-configuration.cfapps.us10.hana.ondemand.com/api/v2/configurations/"+str(cpsConfigID)
					webclient.Headers[System.Net.HttpRequestHeader.Authorization] = "Bearer " + str(response["access_token"])
					
					response2 = webclient.DownloadString(Request_URL)
					#Log.Info('response2--182----267-----'+str(response2))
					response2 = str(response2).replace(": true", ': "true"').replace(": false", ': "false"')
					Fullresponse= eval(response2)
					attributesdisallowedlst=[]
					attributeReadonlylst=[]
					attributesallowedlst=[]
					#overallattributeslist =[]
					attributevalues={}
					for rootattribute, rootvalue in Fullresponse.items():
						if rootattribute=="rootItem":
							for Productattribute, Productvalue in rootvalue.items():
								if Productattribute=="characteristics":
									for prdvalue in Productvalue:
										#overallattributeslist.append(prdvalue['id'])
										if prdvalue['visible'] =='false':
											attributesdisallowedlst.append(prdvalue['id'])
										else:
											#Trace.Write(prdvalue['id']+" set here")
											attributesallowedlst.append(prdvalue['id'])
										if prdvalue['readOnly'] =='true':
											attributeReadonlylst.append(prdvalue['id'])
										for attribute in prdvalue['values']:
											attributevalues[str(prdvalue['id'])]=attribute['value']
					
					attributesallowedlst = list(set(attributesallowedlst))
					#overallattributeslist = list(set(overallattributeslist))
					HasDefaultvalue=False
					ProductVersionObj=Sql.GetFirst("Select product_id from product_versions(nolock) where SAPKBVersion='"+str(Fullresponse['kbKey']['version'])+"'")
					if ProductVersionObj is not None:
						tbrow={}
						insertservice = ""						
						for attrs in attributesallowedlst:							
							if attrs in attributevalues:
								HasDefaultvalue=True
								STANDARD_ATTRIBUTE_VALUES=Sql.GetFirst("SELECT S.STANDARD_ATTRIBUTE_DISPLAY_VAL,S.STANDARD_ATTRIBUTE_CODE FROM STANDARD_ATTRIBUTE_VALUES (nolock) S INNER JOIN ATTRIBUTE_DEFN (NOLOCK) A ON A.STANDARD_ATTRIBUTE_CODE=S.STANDARD_ATTRIBUTE_CODE WHERE A.SYSTEM_ID = '{}'".format(attrs,attributevalues[attrs]))
								ent_disp_val = attributevalues[attrs]
							else:
								HasDefaultvalue=False
								ent_disp_val = ""
								STANDARD_ATTRIBUTE_VALUES=Sql.GetFirst("SELECT S.STANDARD_ATTRIBUTE_CODE FROM STANDARD_ATTRIBUTE_VALUES (nolock) S INNER JOIN ATTRIBUTE_DEFN (NOLOCK) A ON A.STANDARD_ATTRIBUTE_CODE=S.STANDARD_ATTRIBUTE_CODE WHERE A.SYSTEM_ID = '{}'".format(attrs))
							ATTRIBUTE_DEFN=Sql.GetFirst("SELECT * FROM ATTRIBUTE_DEFN (NOLOCK) WHERE SYSTEM_ID='{}'".format(attrs))
							PRODUCT_ATTRIBUTES=Sql.GetFirst("SELECT A.ATT_DISPLAY_DESC FROM ATT_DISPLAY_DEFN (NOLOCK) A INNER JOIN PRODUCT_ATTRIBUTES (NOLOCK) P ON A.ATT_DISPLAY=P.ATT_DISPLAY WHERE P.PRODUCT_ID={} AND P.STANDARD_ATTRIBUTE_CODE={}".format(ProductVersionObj.product_id,STANDARD_ATTRIBUTE_VALUES.STANDARD_ATTRIBUTE_CODE))
							
							if PRODUCT_ATTRIBUTES.ATT_DISPLAY_DESC in ('Drop Down','Check Box') and ent_disp_val:
								get_display_val = Sql.GetFirst("SELECT STANDARD_ATTRIBUTE_DISPLAY_VAL  from STANDARD_ATTRIBUTE_VALUES S INNER JOIN ATTRIBUTE_DEFN (NOLOCK) A ON A.STANDARD_ATTRIBUTE_CODE=S.STANDARD_ATTRIBUTE_CODE WHERE S.STANDARD_ATTRIBUTE_CODE = '{}' AND A.SYSTEM_ID = '{}' AND S.STANDARD_ATTRIBUTE_VALUE = '{}' ".format(STANDARD_ATTRIBUTE_VALUES.STANDARD_ATTRIBUTE_CODE,attrs,  attributevalues[attrs] ) )
								ent_disp_val = get_display_val.STANDARD_ATTRIBUTE_DISPLAY_VAL 							
							
							DTypeset={"Drop Down":"DropDown","Free Input, no Matching":"FreeInputNoMatching","Check Box":"Check Box"}							
							insertservice += """<QUOTE_ITEM_ENTITLEMENT>
							<ENTITLEMENT_NAME>{ent_name}</ENTITLEMENT_NAME>
							<ENTITLEMENT_VALUE_CODE>{ent_val_code}</ENTITLEMENT_VALUE_CODE>
							<ENTITLEMENT_TYPE>{ent_type}</ENTITLEMENT_TYPE>							
							<ENTITLEMENT_DISPLAY_VALUE>{ent_disp_val}</ENTITLEMENT_DISPLAY_VALUE>
							<ENTITLEMENT_DESCRIPTION>{ent_desc}</ENTITLEMENT_DESCRIPTION>
							<ENTITLEMENT_COST_IMPACT>{ct}</ENTITLEMENT_COST_IMPACT>
							<ENTITLEMENT_PRICE_IMPACT>{pi}</ENTITLEMENT_PRICE_IMPACT>
							<IS_DEFAULT>{is_default}</IS_DEFAULT>
							<PRICE_METHOD>{pm}</PRICE_METHOD>
							<CALCULATION_FACTOR>{cf}</CALCULATION_FACTOR>
							</QUOTE_ITEM_ENTITLEMENT>""".format(ent_name = str(attrs),ent_val_code = attributevalues[attrs] if HasDefaultvalue==True else '',ent_type = DTypeset[PRODUCT_ATTRIBUTES.ATT_DISPLAY_DESC] if PRODUCT_ATTRIBUTES else  '',ent_desc = ATTRIBUTE_DEFN.STANDARD_ATTRIBUTE_NAME,ent_disp_val = ent_disp_val if HasDefaultvalue==True else '',ct = '',pi = '',is_default = '1',pm = '',cf = '')
							cpsmatc_incr = int(cpsmatchID) + 10
							Updatecps = "UPDATE {} SET CPS_MATCH_ID ={},CPS_CONFIGURATION_ID = '{}',CpqTableEntryModifiedBy = {}, CpqTableEntryDateModified = GETDATE() WHERE {} ".format('SAQTSE', cpsmatc_incr,cpsConfigID, User.Id, whereReq)
							Sql.RunQuery(Updatecps)

			except:
				cpsmatc_incr = ''	


class ToolRelocationModel(ContractQuoteCrudOpertion):
	def __init__(self, **kwargs):
		ContractQuoteCrudOpertion.__init__(self, trigger_from=kwargs.get('trigger_from'), contract_quote_record_id=kwargs.get('contract_quote_record_id'),quote_revision_record_id=kwargs.get('quote_revision_record_id'),
											tree_param=kwargs.get('tree_param'), tree_parent_level_0=kwargs.get('tree_parent_level_0'))
		self.opertion = kwargs.get('opertion')
		self.action_type = kwargs.get('action_type')
		self.values = kwargs.get('values')
		self.table_name = kwargs.get('table_name')
		self.all_values = kwargs.get('all_values')		
		self.node_id = ""	

	def _create(self):
		#userName = str(self.user_name)
		if self.action_type == "ADD_TOOL_RELOCATION_EQUIPMENTS":
			self._add_quote_source_tool_relocation()

	def _add_quote_source_tool_relocation(self):
		master_object_name = "MAEQUP"
		if self.values:
			record_ids = []
			if self.all_values:               
				# query_string = "select MAEQUP.EQUIPMENT_RECORD_ID from MAEQUP (NOLOCK) inner join SAQSCF (NOLOCK) on MAEQUP.FABLOCATION_RECORD_ID = SAQSCF.SRCFBL_RECORD_ID and MAEQUP.ACCOUNT_RECORD_ID = SAQSCF.SRCACC_RECORD_ID and MAEQUP.FABLOCATION_ID = SAQSCF.SRCFBL_ID inner join  MAFBLC (nolock) on MAFBLC.FAB_LOCATION_ID = SAQSCF.SRCFBL_ID AND MAFBLC.ACCOUNT_ID = SAQSCF.SRCACC_ID AND isnull(MAEQUP.PAR_EQUIPMENT_ID,'') = '' AND SAQSCF.QUOTE_RECORD_ID = '{}' where MAEQUP.GREENBOOK_RECORD_ID != '' AND MAEQUP.GREENBOOK_RECORD_ID is not null AND NOT EXISTS (SELECT EQUIPMENT_ID FROM SAQSTE (NOLOCK) WHERE QUOTE_RECORD_ID = '{}') ".format(
				# self.contract_quote_record_id,
				# self.contract_quote_record_id
				# )
				query_string = "select MAEQUP.EQUIPMENT_RECORD_ID from MAEQUP (NOLOCK) inner join SAQSCF (NOLOCK) on MAEQUP.FABLOCATION_RECORD_ID = SAQSCF.SRCFBL_RECORD_ID and MAEQUP.ACCOUNT_RECORD_ID = SAQSCF.SRCACC_RECORD_ID and MAEQUP.FABLOCATION_ID = SAQSCF.SRCFBL_ID inner join  MAFBLC (nolock) on MAFBLC.FAB_LOCATION_ID = SAQSCF.SRCFBL_ID AND MAFBLC.ACCOUNT_ID = SAQSCF.SRCACC_ID AND isnull(MAEQUP.PAR_EQUIPMENT_ID,'') = '' AND SAQSCF.QUOTE_RECORD_ID = '{}' AND SAQSCF.QTEREV_RECORD_ID = '{}' where MAEQUP.GREENBOOK_RECORD_ID != '' AND MAEQUP.GREENBOOK_RECORD_ID is not null AND MAEQUP.EQUIPMENT_ID not in (SELECT EQUIPMENT_ID FROM SAQSTE (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND SAQSCF.QTEREV_RECORD_ID = '{}') ".format(
				self.contract_quote_record_id,
				self.quote_revision_record_id,
				self.contract_quote_record_id,
				self.quote_revision_record_id
				)
				query_string_for_count = "SELECT COUNT(*) as count FROM ({Query_String})OQ".format(
					Query_String=query_string
				)
				table_count_data = Sql.GetFirst(query_string_for_count)
				if table_count_data is not None:
					table_total_rows = table_count_data.count
				if table_total_rows:
					record_ids = [data for data in self.get_res(query_string, table_total_rows)]                    
			else:                    
				record_ids = [
					CPQID.KeyCPQId.GetKEYId(master_object_name, str(value))
					if value.strip() != "" and master_object_name in value
					else value
					for value in self.values
				]
			batch_group_record_id = str(Guid.NewGuid()).upper()
			record_ids = str(str(record_ids)[1:-1].replace("'",""))
			parameter = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'SELECT' ")			
			primaryQueryItems = SqlHelper.GetFirst(""+str(parameter.QUERY_CRITERIA_1)+" SYSPBT(BATCH_RECORD_ID, BATCH_STATUS, QUOTE_ID, QUOTE_RECORD_ID, BATCH_GROUP_RECORD_ID,QTEREV_RECORD_ID) SELECT MAEQUP.EQUIPMENT_RECORD_ID as BATCH_RECORD_ID, ''IN PROGRESS'' as BATCH_STATUS, ''"+str(self.contract_quote_id)+"'' as QUOTE_ID, ''"+str(self.contract_quote_record_id)+"'' as QUOTE_RECORD_ID, ''"+str(batch_group_record_id)+"'' as BATCH_GROUP_RECORD_ID,''"+str(self.quote_revision_record_id)+"'' as QTEREV_RECORD_ID FROM MAEQUP (NOLOCK) JOIN splitstring(''"+record_ids+"'') ON ltrim(rtrim(NAME)) = MAEQUP.EQUIPMENT_RECORD_ID'")
			self._process_query(
							"""
								INSERT SAQSTE (
									QUOTE_SOURCE_TARGET_FAB_LOC_EQUIP_RECORD_ID,
									EQUIPMENT_ID,
									EQUIPMENT_RECORD_ID,
									EQUIPMENT_DESCRIPTION,   
									SRCACC_ID,
									SRCACC_NAME,
									SRCACC_RECORD_ID,
									SRCFBL_ID,
									SRCFBL_NAME,
									SRCFBL_RECORD_ID,
									FABLOCATION_ID,
									FABLOCATION_NAME,
									FABLOCATION_RECORD_ID,
									QUOTE_RECORD_ID,
									QUOTE_ID,
									QUOTE_NAME,
									QTEREV_ID,
									QTEREV_RECORD_ID,
									PLATFORM,
									EQUIPMENTCATEGORY_RECORD_ID,
									EQUIPMENTCATEGORY_ID,
									EQUIPMENTCATEGORY_DESCRIPTION,
									EQUIPMENT_STATUS,
									GREENBOOK,
									GREENBOOK_RECORD_ID,
									MNT_PLANT_RECORD_ID,
									MNT_PLANT_ID,
									MNT_PLANT_NAME,
									CPQTABLEENTRYADDEDBY,
									CPQTABLEENTRYDATEADDED,
									CpqTableEntryModifiedBy,
									CpqTableEntryDateModified
									) SELECT
										CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SOURCE_TARGET_FAB_LOC_EQUIP_RECORD_ID,
										MAEQUP.EQUIPMENT_ID,
										MAEQUP.EQUIPMENT_RECORD_ID,
										MAEQUP.EQUIPMENT_DESCRIPTION,
										SAQSCF.SRCACC_ID,  
										SAQSCF.SRCACC_NAME,
										SAQSCF.SRCACC_RECORD_ID,
										SAQSCF.SRCFBL_ID,
										SAQSCF.SRCFBL_NAME,
										SAQSCF.SRCFBL_RECORD_ID,
										'' as FABLOCATION_ID,
										'' as FABLOCATION_NAME,
										'' as FABLOCATION_RECORD_ID,
										'{QuoteRecId}' as QUOTE_RECORD_ID,
										'{QuoteId}' as QUOTE_ID,
										'{QuoteName}' as QUOTE_NAME,
										'{RevisionId}' as QTEREV_ID,
										'{RevisionRecordId}' as QTEREV_RECORD_ID,
										MAEQUP.PLATFORM,
										MAEQUP.EQUIPMENTCATEGORY_RECORD_ID,
										MAEQUP.EQUIPMENTCATEGORY_ID,
										MAEQUP.EQUIPMENTCATEGORY_DESCRIPTION,
										MAEQUP.EQUIPMENT_STATUS,
										MAEQUP.GREENBOOK,
										MAEQUP.GREENBOOK_RECORD_ID,
										MAEQUP.MNT_PLANT_RECORD_ID,
										MAEQUP.MNT_PLANT_ID,
										MAEQUP.MNT_PLANT_NAME,
										'{UserName}' AS CPQTABLEENTRYADDEDBY,
										GETDATE() as CPQTABLEENTRYDATEADDED,
										{UserId} as CpqTableEntryModifiedBy,
										GETDATE() as CpqTableEntryDateModified
										FROM SYSPBT (NOLOCK)
										JOIN MAEQUP (NOLOCK) ON SYSPBT.BATCH_RECORD_ID = MAEQUP.EQUIPMENT_RECORD_ID JOIN SAQSCF(NOLOCK) ON SAQSCF.QUOTE_RECORD_ID = SYSPBT.QUOTE_RECORD_ID AND SAQSCF.QTEREV_RECORD_ID = SYSPBT.QTEREV_RECORD_ID AND MAEQUP.FABLOCATION_ID = SAQSCF.SRCFBL_ID  WHERE 
										SYSPBT.QUOTE_RECORD_ID = '{QuoteRecId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'
										AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}'                        
								""".format(
								QuoteId=self.contract_quote_id,
								BatchGroupRecordId=batch_group_record_id,
								UserName=self.user_name,
								UserId=self.user_id,
								QuoteRecId=self.contract_quote_record_id,
								RevisionId=self.quote_revision_id,
								RevisionRecordId=self.quote_revision_record_id,
								QuoteName=self.contract_quote_name
							)
						)	

		self._process_query(
					"""DELETE FROM SYSPBT WHERE SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}' and SYSPBT.QTEREV_RECORD_ID = '{RevisionRecordId}' and SYSPBT.BATCH_STATUS = 'IN PROGRESS'""".format(
						BatchGroupRecordId=batch_group_record_id,RevisionRecordId=self.quote_revision_record_id
					)
				)

	def get_res(self, query_string, table_total_rows):
		for offset_skip_count in range(0, table_total_rows+1, 1000):
			pagination_condition = "WHERE SNO>={Skip_Count} AND SNO<={Fetch_Count}".format(Skip_Count=offset_skip_count+1, Fetch_Count=offset_skip_count+1000)
			query_string_with_pagination = 'SELECT * FROM (SELECT *, ROW_NUMBER()OVER(ORDER BY EQUIPMENT_RECORD_ID) AS SNO FROM ({Query_String}) IQ)OQ {Pagination_Condition}'.format(
											Query_String=query_string, Pagination_Condition=pagination_condition)
			table_data = Sql.GetList(query_string_with_pagination)
			if table_data is not None:
				for row_data in table_data:
					yield row_data.EQUIPMENT_RECORD_ID


class ContractQuoteFabModel(ContractQuoteCrudOpertion):
	def __init__(self, **kwargs):
		ContractQuoteCrudOpertion.__init__(self, trigger_from=kwargs.get('trigger_from'), contract_quote_record_id=kwargs.get('contract_quote_record_id'),quote_revision_record_id=kwargs.get('quote_revision_record_id'), 
											tree_param=kwargs.get('tree_param'), tree_parent_level_0=kwargs.get('tree_parent_level_0'))
		self.opertion = kwargs.get('opertion')
		self.action_type = kwargs.get('action_type')
		self.values = kwargs.get('values')
		self.table_name = kwargs.get('table_name')
		self.all_values = kwargs.get('all_values')		
		self.node_id = ""	

	def _create(self):
		#userName = self.user_name
		mylist = []
		row_values = {}
		Trace.Write("self.action_type"+str(self.action_type))
		if self.action_type == "ADD_FAB":
			master_object_name = "MAFBLC"
			columns = [
				"FAB_LOCATION_ID AS FABLOCATION_ID",
				"FAB_LOCATION_NAME AS FABLOCATION_NAME",
				"FAB_LOCATION_RECORD_ID AS FABLOCATION_RECORD_ID",
				"COUNTRY",
				"COUNTRY_RECORD_ID",
				"MNT_PLANT_ID",
				"MNT_PLANT_NAME",
				"MNT_PLANT_RECORD_ID",
				"STATUS AS FABLOCATION_STATUS"
				
			]
			table_name = "SAQFBL"
			condition_column = "FAB_LOCATION_RECORD_ID"
			Trace.Write("self.tree_param"+str(self.tree_param))
			if self.sale_type != "TOOL RELOCATION":
				contract_quote_record_obj = self._get_record_obj(
				columns=[
					"ACCOUNT_ID",
					"ACCOUNT_NAME",
					"ACCOUNT_RECORD_ID"
				],
				table_name="SAQTMT",
				where_condition="MASTER_TABLE_QUOTE_RECORD_ID = '{}'".format(self.contract_quote_record_id),
				single_record=True,
				)
				account_id = contract_quote_record_obj.ACCOUNT_ID
				account_name = contract_quote_record_obj.ACCOUNT_NAME
				account_rec_id = contract_quote_record_obj.ACCOUNT_RECORD_ID
			else:
				account_id = self.tree_param.split(' - ')
				account_id = account_id[len(account_id)-1]
				account_table  = Sql.GetFirst("SELECT ACCOUNT_NAME,ACCOUNT_RECORD_ID FROM SAACNT(NOLOCK) WHERE ACCOUNT_ID = '"+str(account_id)+"'") 
				if account_table:
					account_name = account_table.ACCOUNT_NAME
					account_rec_id = account_table.ACCOUNT_RECORD_ID
			row_values = {
				"QUOTE_NAME": self.contract_quote_name,
				"SALESORG_ID": self.salesorg_id,
				"SALESORG_NAME": self.salesorg_name,
				"SALESORG_RECORD_ID": self.salesorg_record_id,
				# "CPQTABLEENTRYADDEDBY": self.userName,
				"RELOCATION_FAB_TYPE" : "SENDING FAB" if "Sending Account -" in self.tree_param else "RECEIVING FAB" if "Receiving Account -" in self.tree_param else "",
				"ACCOUNT_ID" : account_id,
				"ACCOUNT_NAME" : account_name,
				"ACCOUNT_RECORD_ID" : account_rec_id,
				"QTEREV_RECORD_ID":self.quote_revision_record_id,
				"QTEREV_ID" : self.quote_revision_id,
			}

			fab_table_info = Sql.GetTable(table_name)
			Trace.Write('self.all_values'+str(self.all_values))
			if self.all_values:
				qury_str=""
				if A_Keys!="" and A_Values!="":
					for key,val in zip(A_Keys,A_Values):
						if(val!=""):
							if key=="FAB_LOCATION_RECORD_ID":
								key="CpqTableEntryId"
								val = ''.join(re.findall(r'\d+', val)) if not val.isdigit() else val
							qury_str+=" "+key+" LIKE '%"+val+"%' AND "
				master_fab_obj = self._get_record_obj(
					columns=["FAB_LOCATION_RECORD_ID"],
					table_name=master_object_name,
					table_joins="JOIN SAQTMT (NOLOCK) ON MAFBLC.ACCOUNT_RECORD_ID = SAQTMT.ACCOUNT_RECORD_ID",
					where_condition=""" SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = '{}' AND {} NOT EXISTS (SELECT FABLOCATION_ID FROM SAQFBL (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}')""".format(
						self.contract_quote_record_id, qury_str, self.contract_quote_record_id,self.quote_revision_record_id, single_record=False,
					),
				)
				if master_fab_obj:
					self.values = [fab_obj.FAB_LOCATION_RECORD_ID for fab_obj in master_fab_obj]
			
			for row_detail in self._add_record(
				master_object_name=master_object_name,
				columns=columns,
				table_name=table_name,
				condition_column=condition_column,
				values=self.values,
			):
				
				Trace.Write("row_detail"+str(row_detail))
				row_detail.update(row_values)				
				mylist.append(row_detail)				
				fab_table_info.AddRow(row_detail)

			Sql.Upsert(fab_table_info)
			if ("Sending Account -" in self.tree_param or "Receiving Account -" in self.tree_param) and self.tree_parent_level_0 == 'Fab Locations':
				auto_equp_insert = "true"
				Trace.Write("auto equp add"+str(self.tree_parent_level_0)+'--'+str(mylist))
				self._add_equipment(auto_equp_insert,mylist)
			# ADD QUOTA VD AND VDV FOR THE FAB LOCATION
			for dictvalue in mylist:				
				QTRECID = str(dictvalue["QUOTE_ID"])
				FABRECID = str(dictvalue["QUOTE_FABLOCATION_RECORD_ID"])
				GETSAQFBLD = Sql.GetList(
					"SELECT A.FABLOCATION_ID,B.VALUEDRIVER_ID,A.FABLOCATION_NAME,A.FABLOCATION_RECORD_ID,A.QUOTE_ID,A.QUOTE_NAME,A.QUOTE_RECORD_ID,A.QTEREV_RECORD_ID,A.QTEREV_ID,B.VALUEDRIVER_NAME,B.VALUEDRIVER_RECORD_ID,B.VALUEDRIVER_TYPE,A.QUOTE_FABLOCATION_RECORD_ID FROM SAQFBL(NOLOCK) A JOIN SAQTVD (NOLOCK) B ON A.QUOTE_ID  = '"
					+ str(QTRECID)
					+ "' AND B.QUOTE_ID  = '"
					+ str(QTRECID)
					+ "' WHERE A.QUOTE_FABLOCATION_RECORD_ID ='"
					+ str(FABRECID)
					+ "' "
				)
				#tableSAQFVD = {}
				tableInfo = SqlHelper.GetTable("SAQFVD")
				for data1 in GETSAQFBLD:					
					tableSAQFVD = {
						"QUOTE_FABLOCATION_VALUEDRIVER_RECORD_ID": str(Guid.NewGuid()).upper(),
						"FABLOCATION_ID": str(data1.FABLOCATION_ID),
						"VALUEDRIVER_ID": str(data1.VALUEDRIVER_ID),
						"FABLOCATION_NAME": str(data1.FABLOCATION_NAME),
						"FABLOCATION_RECORD_ID": str(data1.FABLOCATION_RECORD_ID),
						"QUOTE_ID": str(data1.QUOTE_ID),
						"QUOTE_NAME": str(data1.QUOTE_NAME),
						"QUOTE_RECORD_ID": str(data1.QUOTE_RECORD_ID),
						"VALUEDRIVER_NAME": str(data1.VALUEDRIVER_NAME),
						"VALUEDRIVER_RECORD_ID": str(data1.VALUEDRIVER_RECORD_ID),
						"VALUEDRIVER_TYPE": str(data1.VALUEDRIVER_TYPE),
						"QTEFBL_RECORD_ID": str(data1.QUOTE_FABLOCATION_RECORD_ID),
						"CPQTABLEENTRYDATEADDED": datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"),
						"CPQTABLEENTRYADDEDBY": self.user_name,
						"ADDUSR_RECORD_ID": self.user_id,
						"QTEREV_RECORD_ID": str(data1.QTEREV_RECORD_ID),
						"QTEREV_ID": str(data1.QTEREV_ID),
					}					
					tableInfo.AddRow(tableSAQFVD)
					# upsertResult = SqlHelper.Upsert(tableInfo)
				Sql.Upsert(tableInfo)
				GETSAQFBLDV = Sql.GetList(
					"SELECT A.FABLOCATION_ID,A.FABLOCATION_NAME,A.FABLOCATION_RECORD_ID,A.QUOTE_FABLOCATION_RECORD_ID,A.QUOTE_ID,A.QUOTE_NAME,A.QUOTE_RECORD_ID,A.QTEREV_RECORD_ID,A.QTEREV_ID,B.VALUEDRIVER_NAME,B.VALUEDRIVER_ID,B.VALUEDRIVER_RECORD_ID,B.VALUEDRIVER_VALUE_DESCRIPTION,B.VALUEDRIVER_VALUE_RECORD_ID FROM SAQFBL(NOLOCK) A JOIN SAQVDV (NOLOCK) B ON A.QUOTE_ID  = '"
					+ str(QTRECID)
					+ "' AND B.QUOTE_ID  = '"
					+ str(QTRECID)
					+ "' WHERE A.QUOTE_FABLOCATION_RECORD_ID ='"
					+ str(FABRECID)
					+ "'"
				)
				#tableSAQFDV = {}
				tableInfo2 = SqlHelper.GetTable("SAQFDV")
				for data2 in GETSAQFBLDV:					
					tableSAQFDV = {
						"QUOTE_FAB_VALDRIVER_VALUE_RECORD_ID": str(Guid.NewGuid()).upper(),
						"FABLOCATION_ID": str(data2.FABLOCATION_ID),
						"VALUEDRIVER_ID": str(data2.VALUEDRIVER_ID),
						"FABLOCATION_NAME": str(data2.FABLOCATION_NAME),
						"FABLOCATION_RECORD_ID": str(data2.FABLOCATION_RECORD_ID),
						"QUOTE_ID": str(data2.QUOTE_ID),
						"QUOTE_NAME": str(data2.QUOTE_NAME),
						"QUOTE_RECORD_ID": str(data2.QUOTE_RECORD_ID),
						"VALUEDRIVER_NAME": str(data2.VALUEDRIVER_NAME),
						"VALUEDRIVER_RECORD_ID": str(data2.VALUEDRIVER_RECORD_ID),
						"VALUEDRIVER_VALUEDESC": str(data2.VALUEDRIVER_VALUE_DESCRIPTION),
						"QUOTE_FABLOCATION_RECORD_ID": str(data2.QUOTE_FABLOCATION_RECORD_ID),
						"CPQTABLEENTRYDATEADDED": datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"),
						"CPQTABLEENTRYADDEDBY": self.user_name,
						"ADDUSR_RECORD_ID": self.user_id,
						"QTEREV_RECORD_ID": str(data1.QTEREV_RECORD_ID),
						"QTEREV_ID": str(data1.QTEREV_ID),
					}
					tableInfo2.AddRow(tableSAQFDV)
					# upsertResult = SqlHelper.Upsert(tableInfo2)
				Sql.Upsert(tableInfo2)

			
		elif self.action_type == "ADD_ON_PRODUCTS":			
			where_condition=""
			master_object_name = "MAADPR"
			GETPARENTSERVICE= Sql.GetFirst("SELECT QUOTE_SERVICE_RECORD_ID FROM SAQTSV(NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID ='{}' ".format(self.contract_quote_record_id,self.quote_revision_record_id,self.tree_parent_level_0))
			columns = [
				"ADNPRDOFR_NAME AS ADNPRD_DESCRIPTION",
				"ADNPRDOFR_ID AS ADNPRD_ID",
				"ADNPRDOFR_RECORD_ID AS ADNPRDOFR_RECORD_ID",
				"ADD_ON_PRODUCT_RECORD_ID AS ADNPRD_RECORD_ID",
				"ADN_TYPE AS ADN_TYPE",
				#"GETPARENTSERVICE.QUOTE_SERVICE_RECORD_ID AS QTESRV_RECORD_ID",
				"'TRUE' AS ACTIVE",
				"PRDOFR_NAME AS SERVICE_DESCRIPTION",
				"PRDOFR_ID AS SERVICE_ID",
				"PRDOFR_RECORD_ID AS SERVICE_RECORD_ID",
				# "MNT_PLANT_RECORD_ID",
				# "STATUS AS FABLOCATION_STATUS" 
			]
			table_name = "SAQSAO"
			condition_column = "ADD_ON_PRODUCT_RECORD_ID"
			row_values = {
				"QUOTE_NAME": self.contract_quote_name,
				"SALESORG_ID": self.salesorg_id,
				"SALESORG_NAME": self.salesorg_name,
				"SALESORG_RECORD_ID": self.salesorg_record_id,
				# "CPQTABLEENTRYADDEDBY": self.userName,
			}

			fab_table_info = Sql.GetTable(table_name)
			if self.all_values:
				master_fab_obj = self._get_record_obj(
					columns=["ADD_ON_PRODUCT_RECORD_ID"],
					table_name=master_object_name,
					table_joins="JOIN SAQTSV (NOLOCK) ON MAADPR.PRDOFR_ID = SAQTSV.SERVICE_ID",
					where_condition=""" SAQTSV.QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'AND NOT EXISTS (SELECT ADNPRD_ID FROM SAQSAO (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID = '{}')""".format(
						self.contract_quote_record_id,self.quote_revision_record_id, self.contract_quote_record_id,self.quote_revision_record_id,self.tree_parent_level_0, single_record=False,
					),
				)

				if master_fab_obj:
					self.values = [fab_obj.ADD_ON_PRODUCT_RECORD_ID for fab_obj in master_fab_obj]

			for row_detail in self._add_record(
				master_object_name=master_object_name,
				columns=columns,
				table_name=table_name,
				condition_column=condition_column,
				values=self.values,
			):

				row_detail.update(row_values)				
				mylist.append(row_detail)
				fab_table_info.AddRow(row_detail)
			Sql.Upsert(fab_table_info)			
			QueryStatement ="""UPDATE SAQSAO SET QTESRV_RECORD_ID ='{id}' WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID ='{}'  """.format(self.contract_quote_record_id,self.quote_revision_record_id,self.tree_parent_level_0,id = str(GETPARENTSERVICE.QUOTE_SERVICE_RECORD_ID) )
			Sql.RunQuery(QueryStatement)
			#for id in self.values:
			
			#	QueryStatement ="""UPDATE SAQSAO SET ACTIVE ='TRUE' WHERE QUOTE_RECORD_ID = '{quote_record_id}' AND SERVICE_ID ='{treeparam}' AND ADNPRD_ID = '{id}' """.format(quote_record_id=self.contract_quote_record_id,treeparam = self.tree_param,id = str(id) )
			#	Sql.RunQuery(QueryStatement)
			QuoteEndDate = self.contract_start_date
			
			QuoteStartDate = self.contract_end_date
			Sql.RunQuery(""" INSERT SAQTSV(QUOTE_SERVICE_RECORD_ID,QUOTE_ID,QUOTE_NAME,QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,SERVICE_ID,SERVICE_DESCRIPTION,SERVICE_RECORD_ID,SERVICE_TYPE,UOM_ID,UOM_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,PAR_SERVICE_DESCRIPTION,PAR_SERVICE_ID,PAR_SERVICE_RECORD_ID,QTEPARSRV_RECORD_ID,CONTRACT_VALID_FROM,CONTRACT_VALID_TO,CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified)SELECT CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_RECORD_ID,SAQSAO.QUOTE_ID,SAQSAO.QUOTE_NAME,SAQSAO.QUOTE_RECORD_ID,SAQSAO.QTEREV_ID,SAQSAO.QTEREV_RECORD_ID,SAQSAO.ADNPRD_ID,SAQSAO.ADNPRD_DESCRIPTION,SAQSAO.ADNPRDOFR_RECORD_ID,MAMTRL.PRODUCT_TYPE,MAMTRL.UNIT_OF_MEASURE,MAMTRL.UOM_RECORD_ID,SAQSAO.SALESORG_ID,SAQSAO.SALESORG_NAME,SAQSAO.SALESORG_RECORD_ID,SAQSAO.SERVICE_DESCRIPTION,SAQSAO.SERVICE_ID,SAQSAO.SERVICE_RECORD_ID,SAQSAO.QTESRV_RECORD_ID,'{startdate}' as CONTRACT_VALID_FROM,'{enddate}' as CONTRACT_VALID_TO,'{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED, {UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM SAQSAO INNER JOIN MAMTRL ON SAQSAO.ADNPRD_ID = MAMTRL.SAP_PART_NUMBER Where QUOTE_RECORD_ID ='{quote_record_id}' and QTEREV_RECORD_ID = '{RevisionRecordId}' and SERVICE_ID = '{treeparam}' AND ACTIVE ='TRUE'AND NOT EXISTS (SELECT SERVICE_ID FROM SAQTSV WHERE QUOTE_RECORD_ID ='{quote_record_id}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQTSV.SERVICE_ID=SAQSAO.ADNPRD_ID) """.format(quote_record_id=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id,treeparam = self.tree_parent_level_0,UserId=self.user_id,UserName=self.user_name,startdate = self.contract_start_date,enddate = self.contract_end_date ))
			#insert in entitlement table based on add on products
			SAQTSVObj=Sql.GetList("Select SAQSAO.*,SAQTSV.QUOTE_SERVICE_RECORD_ID from SAQSAO (nolock) inner join SAQTSV on SAQTSV.QUOTE_RECORD_ID=SAQSAO.QUOTE_RECORD_ID and SAQTSV.QTEREV_RECORD_ID=SAQSAO.QTEREV_RECORD_ID and SAQTSV.SERVICE_ID = SAQSAO.SERVICE_ID where SAQSAO.QUOTE_RECORD_ID= '{QuoteRecordId}' AND SAQASO.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQSAO.ACTIVE ='TRUE' AND NOT EXISTS (SELECT SERVICE_ID FROM SAQTSV WHERE QUOTE_RECORD_ID ='{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQTSV.SERVICE_ID=SAQSAO.ADNPRD_ID)".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id))
			#tableInfo = SqlHelper.GetTable("SAQTSE")
			x = datetime.datetime.today()
			x= str(x)
			y = x.split(" ")
			for OfferingRow_detail in SAQTSVObj:
				webclient = System.Net.WebClient()
				webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/json"
				webclient.Headers[System.Net.HttpRequestHeader.Authorization] = "Basic c2ItYzQwYThiMWYtYzU5NS00ZWJjLTkyYzYtYzM4ODg4ODFmMTY0IWIyNTAzfGNwc2VydmljZXMtc2VjdXJlZCFiMzkxOm9zRzgvSC9hOGtkcHVHNzl1L2JVYTJ0V0FiMD0=";
				response = webclient.DownloadString("https://cpqprojdevamat.authentication.us10.hana.ondemand.com:443/oauth/token?grant_type=client_credentials")
				response = eval(response)
				Request_URL="https://cpservices-product-configuration.cfapps.us10.hana.ondemand.com/api/v2/configurations?autoCleanup=False"
				webclient.Headers[System.Net.HttpRequestHeader.Authorization] ="Bearer "+str(response['access_token'])
				requestdata= '{"productKey":"'+OfferingRow_detail.ADNPRD_ID+'","date":"'+str(y[0])+'","context":[{"name":"VBAP-MATNR","value":"'+OfferingRow_detail.ADNPRD_ID+'"}]}'
				
				response1 = webclient.UploadString(Request_URL,str(requestdata))
				response1=str(response1).replace(": true",": \"true\"").replace(": false",": \"false\"")
				Fullresponse= eval(response1)
				attributesdisallowedlst=[]
				attributeReadonlylst=[]
				attributesallowedlst=[]
				attributevalues={}
				attributedefaultvalue = []
				for rootattribute, rootvalue in Fullresponse.items():
					if rootattribute=="rootItem":
						for Productattribute, Productvalue in rootvalue.items():
							if Productattribute=="characteristics":
								for prdvalue in Productvalue:
									if prdvalue['visible'] =='false':
										attributesdisallowedlst.append(prdvalue['id'])
									else:
										
										attributesallowedlst.append(prdvalue['id'])
									if prdvalue['readOnly'] =='true':
										attributeReadonlylst.append(prdvalue['id'])
									for attribute in prdvalue['values']:
										
										attributevalues[str(prdvalue['id'])]=attribute['value']
										if attribute["author"] in ("Default"):
											Trace.Write('524------'+str(prdvalue["id"]))
											attributedefaultvalue.append(prdvalue["id"])
				
				attributesallowedlst = list(set(attributesallowedlst))
				Trace.Write('2172')
				HasDefaultvalue=False
				ProductVersionObj=Sql.GetFirst("Select product_id from product_versions(nolock) where SAPKBVersion='"+str(Fullresponse['kbKey']['version'])+"'")
				if ProductVersionObj is not None:
					tbrow={}
					insertservice = ""
					
					for attrs in attributesallowedlst:
						#tbrow1 = {}
						if attrs in attributevalues:
							HasDefaultvalue=True
							
							STANDARD_ATTRIBUTE_VALUES=Sql.GetFirst("SELECT S.STANDARD_ATTRIBUTE_DISPLAY_VAL,S.STANDARD_ATTRIBUTE_CODE FROM STANDARD_ATTRIBUTE_VALUES (nolock) S INNER JOIN ATTRIBUTE_DEFN (NOLOCK) A ON A.STANDARD_ATTRIBUTE_CODE=S.STANDARD_ATTRIBUTE_CODE WHERE A.SYSTEM_ID = '{}'".format(attrs))
							ent_disp_val = attributevalues[attrs]
						else:
							HasDefaultvalue=False
							ent_disp_val = ""
							STANDARD_ATTRIBUTE_VALUES=Sql.GetFirst("SELECT S.STANDARD_ATTRIBUTE_CODE FROM STANDARD_ATTRIBUTE_VALUES (nolock) S INNER JOIN ATTRIBUTE_DEFN (NOLOCK) A ON A.STANDARD_ATTRIBUTE_CODE=S.STANDARD_ATTRIBUTE_CODE WHERE A.SYSTEM_ID = '{}'".format(attrs))
							
						ATTRIBUTE_DEFN=Sql.GetFirst("SELECT * FROM ATTRIBUTE_DEFN (NOLOCK) WHERE SYSTEM_ID='{}'".format(attrs))
						PRODUCT_ATTRIBUTES=Sql.GetFirst("SELECT A.ATT_DISPLAY_DESC FROM ATT_DISPLAY_DEFN (NOLOCK) A INNER JOIN PRODUCT_ATTRIBUTES (NOLOCK) P ON A.ATT_DISPLAY=P.ATT_DISPLAY WHERE P.PRODUCT_ID={} AND P.STANDARD_ATTRIBUTE_CODE={}".format(ProductVersionObj.product_id,STANDARD_ATTRIBUTE_VALUES.STANDARD_ATTRIBUTE_CODE))
						DTypeset={"Drop Down":"DropDown","Free Input, no Matching":"FreeInputNoMatching","Check Box":"Check Box"}
						
						insertservice += """<QUOTE_ITEM_ENTITLEMENT>
						<ENTITLEMENT_NAME>{ent_name}</ENTITLEMENT_NAME>
						<ENTITLEMENT_VALUE_CODE>{ent_val_code}</ENTITLEMENT_VALUE_CODE>
						<ENTITLEMENT_TYPE>{ent_type}</ENTITLEMENT_TYPE>						
						<ENTITLEMENT_DISPLAY_VALUE>{ent_disp_val}</ENTITLEMENT_DISPLAY_VALUE>
						<ENTITLEMENT_DESCRIPTION>{ent_desc}</ENTITLEMENT_DESCRIPTION>
						<ENTITLEMENT_COST_IMPACT>{ct}</ENTITLEMENT_COST_IMPACT>
						<ENTITLEMENT_PRICE_IMPACT>{pi}</ENTITLEMENT_PRICE_IMPACT>
						<IS_DEFAULT>{is_default}</IS_DEFAULT>
						<PRICE_METHOD>{pm}</PRICE_METHOD>
						<CALCULATION_FACTOR>{cf}</CALCULATION_FACTOR>
						</QUOTE_ITEM_ENTITLEMENT>""".format(ent_name = str(attrs),ent_val_code = attributevalues[attrs] if HasDefaultvalue==True else '',ent_type = DTypeset[PRODUCT_ATTRIBUTES.ATT_DISPLAY_DESC] if PRODUCT_ATTRIBUTES else  '',ent_desc = ATTRIBUTE_DEFN.STANDARD_ATTRIBUTE_NAME,ent_disp_val = ent_disp_val if HasDefaultvalue==True else '',ct = '',pi = '',is_default =  1 if str(attrs) in attributedefaultvalue else '0',pm = '',cf = '')
					#getserv_id = Sql.GetFirst("select QUOTE_SERVICE_ADD_ON_PRODUCT_RECORD_ID from SAQSAO (NOLOCK) where QUOTE_RECORD_ID = '{QuoteRecordId}' and SERVICE_ID = '{ser_id}'".format(QuoteRecordId=self.contract_quote_record_id,ser_id=OfferingRow_detail.ADNPRD_ID))
					tbrow["QUOTE_SERVICE_ENTITLEMENT_RECORD_ID"]=str(Guid.NewGuid()).upper()
					tbrow["QUOTE_ID"]=OfferingRow_detail.QUOTE_ID
					tbrow["ENTITLEMENT_XML"]=insertservice
					tbrow["QUOTE_NAME"]=OfferingRow_detail.QUOTE_NAME
					tbrow["QUOTE_RECORD_ID"]=OfferingRow_detail.QUOTE_RECORD_ID
					tbrow["QTESRV_RECORD_ID"]=OfferingRow_detail.QUOTE_SERVICE_ADD_ON_PRODUCT_RECORD_ID
					tbrow["SERVICE_RECORD_ID"]=OfferingRow_detail.ADNPRDOFR_RECORD_ID
					tbrow["SERVICE_ID"]=OfferingRow_detail.ADNPRD_ID
					tbrow["SERVICE_DESCRIPTION"]=OfferingRow_detail.ADNPRD_DESCRIPTION
					tbrow["CPS_CONFIGURATION_ID"]=Fullresponse['id']
					tbrow["SALESORG_RECORD_ID"]=OfferingRow_detail.SALESORG_RECORD_ID
					tbrow["SALESORG_ID"]=OfferingRow_detail.SALESORG_ID
					tbrow["SALESORG_NAME"]=OfferingRow_detail.SALESORG_NAME
					tbrow["CPS_MATCH_ID"] = 11
					tbrow["PAR_SERVICE_RECORD_ID"]=OfferingRow_detail.SERVICE_RECORD_ID
					tbrow["PAR_SERVICE_ID"]=OfferingRow_detail.get("SERVICE_ID")
					tbrow["PAR_SERVICE_DESCRIPTION"]=OfferingRow_detail.SERVICE_DESCRIPTION
					#tbrow["IS_DEFAULT"] = '1'
					tbrow["KB_VERSION"] = Fullresponse["kbKey"]["version"]
					tbrow["CPQTABLEENTRYADDEDBY"] = self.user_id
					tbrow["CPQTABLEENTRYDATEADDED"] = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p")  
					columns = ', '.join("" + str(x) + "" for x in tbrow.keys())
					values = ', '.join("'" + str(x) + "'" for x in tbrow.values())
					insert_qtqtse_query = "INSERT INTO SAQTSE ( %s ) VALUES ( %s );" % (columns, values)
					Sql.RunQuery(insert_qtqtse_query)
			
					SAQSFE_query="""
						INSERT SAQSFE (ENTITLEMENT_XML,QUOTE_ID,QUOTE_NAME,QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,	
						CPS_CONFIGURATION_ID, CPS_MATCH_ID,QTESRVENT_RECORD_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,QTESRVFBL_RECORD_ID,PAR_SERVICE_ID,PAR_SERVICE_DESCRIPTION,PAR_SERVICE_RECORD_ID,QUOTE_SERVICE_FAB_LOC_ENT_RECORD_ID,CPQTABLEENTRYDATEADDED, CPQTABLEENTRYADDEDBY)
						SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_FAB_LOC_ENT_RECORD_ID, {UserId} as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM (
						SELECT 
							DISTINCT	
							SAQTSE.ENTITLEMENT_XML,SAQTSE.QUOTE_ID,SAQTSE.QUOTE_NAME,SAQTSE.QUOTE_RECORD_ID,SAQTSE.QTEREV_ID,SAQTSE.QTEREV_RECORD_ID,SAQTSE.SERVICE_DESCRIPTION,SAQTSE.SERVICE_ID,SAQTSE.SERVICE_RECORD_ID,SAQTSE.SALESORG_ID,SAQTSE.SALESORG_NAME,SAQTSE.SALESORG_RECORD_ID,SAQTSE.CPS_CONFIGURATION_ID, SAQTSE.CPS_MATCH_ID,SAQTSE.QUOTE_SERVICE_ENTITLEMENT_RECORD_ID as QTESRVENT_RECORD_ID,SAQSFB.FABLOCATION_ID, SAQSFB.FABLOCATION_NAME, SAQSFB.FABLOCATION_RECORD_ID,SAQSFB.QUOTE_SERVICE_FAB_LOCATION_RECORD_ID as QTESRVFBL_RECORD_ID,SAQTSE.PAR_SERVICE_ID,SAQTSE.PAR_SERVICE_DESCRIPTION,SAQTSE.PAR_SERVICE_RECORD_ID
						FROM
						SAQTSE (NOLOCK)
						JOIN SAQSFB ON SAQSFB.SERVICE_RECORD_ID = SAQTSE.SERVICE_RECORD_ID AND SAQSFB.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID AND SAQSFB.QTEREV_RECORD_ID = SAQTSE.QTEREV_RECORD_ID
						WHERE SAQTSE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQTSE.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQTSE.SERVICE_ID = '{ServiceId}' AND SAQTSE.SERVICE_ID ='{ParServiceId}') IQ""".format(UserId=self.user_id, QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id,ServiceId=OfferingRow_detail.ADNPRD_ID,ParServiceId = OfferingRow_detail.get("SERVICE_ID"))
					Sql.RunQuery(SAQSFE_query)
					#ENTITLEMENT SV TO GB
	
					qtqsge_query="""
						INSERT SAQSGE (KB_VERSION,QUOTE_ID,QUOTE_NAME,QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,	
						CPS_CONFIGURATION_ID, CPS_MATCH_ID,GREENBOOK,GREENBOOK_RECORD_ID,QTESRVENT_RECORD_ID,QTSFBLENT_RECORD_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,PAR_SERVICE_DESCRIPTION,PAR_SERVICE_ID,PAR_SERVICE_RECORD_ID,ENTITLEMENT_XML, QUOTE_SERVICE_GREENBOOK_ENTITLEMENT_RECORD_ID,CPQTABLEENTRYDATEADDED, CPQTABLEENTRYADDEDBY)
						SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_GREENBOOK_ENTITLEMENT_RECORD_ID, {UserId} as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM (SELECT IQ.*,M.ENTITLEMENT_XML FROM(
						SELECT 
							DISTINCT	
							SAQTSE.KB_VERSION,SAQTSE.QUOTE_ID,SAQTSE.QUOTE_NAME,SAQTSE.QUOTE_RECORD_ID,SAQTSE.QTEREV_ID,SAQTSE.QTEREV_RECORD_ID,SAQTSE.SERVICE_DESCRIPTION,SAQTSE.SERVICE_ID,SAQTSE.SERVICE_RECORD_ID,SAQTSE.SALESORG_ID,SAQTSE.SALESORG_NAME,SAQTSE.SALESORG_RECORD_ID,SAQTSE.CPS_CONFIGURATION_ID, SAQTSE.CPS_MATCH_ID,SAQSCO.GREENBOOK,SAQSCO.GREENBOOK_RECORD_ID,SAQTSE.QUOTE_SERVICE_ENTITLEMENT_RECORD_ID as QTESRVENT_RECORD_ID,SAQSFE.QUOTE_SERVICE_FAB_LOC_ENT_RECORD_ID as QTSFBLENT_RECORD_ID,SAQSFE.FABLOCATION_ID,SAQSFE.FABLOCATION_NAME,SAQSFE.FABLOCATION_RECORD_ID,SAQTSE.PAR_SERVICE_ID,SAQTSE.PAR_SERVICE_DESCRIPTION,SAQTSE.PAR_SERVICE_RECORD_ID
						FROM
						SAQTSE (NOLOCK)
						JOIN SAQSCO  (NOLOCK) ON SAQSCO.SERVICE_RECORD_ID = SAQTSE.SERVICE_RECORD_ID AND SAQSCO.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID  AND SAQSCO.QTEREV_RECORD_ID = SAQTSE.QTEREV_RECORD_ID JOIN SAQSFE ON SAQSFE.SERVICE_RECORD_ID = SAQTSE.SERVICE_RECORD_ID AND SAQSFE.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID  AND SAQSFE.QTEREV_RECORD_ID = SAQTSE.QTEREV_RECORD_ID
						WHERE SAQTSE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQTSE.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQTSE.SERVICE_ID = '{ServiceId}') IQ JOIN SAQSFE (NOLOCK) M ON IQ.QTSFBLENT_RECORD_ID = QUOTE_SERVICE_FAB_LOC_ENT_RECORD_ID )IQ""".format(UserId=self.user_id, QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id, ServiceId=OfferingRow_detail.ADNPRD_ID)
					Sql.RunQuery(qtqsge_query)
		elif self.action_type == "ADD_SOURCE_FAB":			
			master_object_name = "MAFBLC"
			columns = [
				"FAB_LOCATION_ID AS SRCFBL_ID",
				"FAB_LOCATION_NAME AS SRCFBL_NAME",
				"FAB_LOCATION_RECORD_ID AS SRCFBL_RECORD_ID",
				"ACCOUNT_ID AS SRCACC_ID",
				"ACCOUNT_NAME AS SRCACC_NAME",
				"ACCOUNT_RECORD_ID AS SRCACC_RECORD_ID",
				# "COUNTRY",
				# "COUNTRY_RECORD_ID",
				# "MNT_PLANT_ID",
				# "MNT_PLANT_NAME",
				# "MNT_PLANT_RECORD_ID",
				# "STATUS AS FABLOCATION_STATUS" 
			]
			table_name = "SAQSCF"
			condition_column = "FAB_LOCATION_RECORD_ID"
			row_values = {
				"QUOTE_NAME": self.contract_quote_name,
				# "SALESORG_ID": self.salesorg_id,
				# "SALESORG_NAME": self.salesorg_name,
				# "SALESORG_RECORD_ID": self.salesorg_record_id,
				# "CPQTABLEENTRYADDEDBY": self.userName,
			}

			fab_table_info = Sql.GetTable(table_name)
			if self.all_values:
				master_fab_obj = self._get_record_obj(
					columns=["FAB_LOCATION_RECORD_ID"],
					table_name=master_object_name,
					table_joins="JOIN SAQTMT (NOLOCK) ON MAFBLC.ACCOUNT_RECORD_ID = SAQTMT.ACCOUNT_RECORD_ID",
					where_condition=""" SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = '{}' AND NOT EXISTS (SELECT SRCFBL_ID FROM SAQSCF (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}')""".format(
						self.contract_quote_record_id, self.contract_quote_record_id,self.quote_revision_record_id, single_record=False,
					),
				)

				if master_fab_obj:
					self.values = [fab_obj.FAB_LOCATION_RECORD_ID for fab_obj in master_fab_obj]

			for row_detail in self._add_record(
				master_object_name=master_object_name,
				columns=columns,
				table_name=table_name,
				condition_column=condition_column,
				values=self.values,
			):
				row_detail.update(row_values)				
				mylist.append(row_detail)				
				fab_table_info.AddRow(row_detail)
			Sql.Upsert(fab_table_info)
			# ADD QUOTA VD AND VDV FOR THE FAB LOCATION
			for dictvalue in mylist:				
				QTRECID = str(dictvalue["QUOTE_ID"])
				FABRECID = str(dictvalue["QUOTE_SOURCE_FAB_LOCATION_RECORD_ID"])
				GETSAQFBLD = Sql.GetList(
					"SELECT A.SRCFBL_ID,B.VALUEDRIVER_ID,A.SRCFBL_NAME,A.SRCFBL_RECORD_ID,A.QUOTE_ID,A.QUOTE_NAME,A.QUOTE_RECORD_ID,B.VALUEDRIVER_NAME,B.VALUEDRIVER_RECORD_ID,B.VALUEDRIVER_TYPE,A.QUOTE_SOURCE_FAB_LOCATION_RECORD_ID FROM SAQSCF(NOLOCK) A JOIN SAQTVD (NOLOCK) B ON A.QUOTE_ID  = '"
					+ str(QTRECID)
					+ "' AND B.QUOTE_ID  = '"
					+ str(QTRECID)
					+ "' WHERE A.QUOTE_SOURCE_FAB_LOCATION_RECORD_ID ='"
					+ str(FABRECID)
					+ "' "
				)
				#tableSAQFVD = {}
				tableInfo = SqlHelper.GetTable("SAQFVD")
				for data1 in GETSAQFBLD:					
					tableSAQFVD = {
						"QUOTE_FABLOCATION_VALUEDRIVER_RECORD_ID": str(Guid.NewGuid()).upper(),
						"FABLOCATION_ID": str(data1.SRCFBL_ID),
						"VALUEDRIVER_ID": str(data1.VALUEDRIVER_ID),
						"FABLOCATION_NAME": str(data1.SRCFBL_NAME),
						"FABLOCATION_RECORD_ID": str(data1.SRCFBL_RECORD_ID),
						"QUOTE_ID": str(data1.QUOTE_ID),
						"QUOTE_NAME": str(data1.QUOTE_NAME),
						"QUOTE_RECORD_ID": str(data1.QUOTE_RECORD_ID),
						"VALUEDRIVER_NAME": str(data1.VALUEDRIVER_NAME),
						"VALUEDRIVER_RECORD_ID": str(data1.VALUEDRIVER_RECORD_ID),
						"VALUEDRIVER_TYPE": str(data1.VALUEDRIVER_TYPE),
						"QTEFBL_RECORD_ID": str(data1.QUOTE_SOURCE_FAB_LOCATION_RECORD_ID),
						"CPQTABLEENTRYDATEADDED": datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"),
						"CPQTABLEENTRYADDEDBY": self.user_name,
						"ADDUSR_RECORD_ID": self.user_id,
					}					
					tableInfo.AddRow(tableSAQFVD)
					# upsertResult = SqlHelper.Upsert(tableInfo)
				Sql.Upsert(tableInfo)
				GETSAQFBLDV = Sql.GetList(
					"SELECT A.SRCFBL_ID,A.SRCFBL_NAME,A.SRCFBL_RECORD_ID,A.QUOTE_SOURCE_FAB_LOCATION_RECORD_ID,A.QUOTE_ID,A.QUOTE_NAME,A.QUOTE_RECORD_ID,B.VALUEDRIVER_NAME,B.VALUEDRIVER_ID,B.VALUEDRIVER_RECORD_ID,B.VALUEDRIVER_VALUE_DESCRIPTION,B.VALUEDRIVER_VALUE_RECORD_ID FROM SAQSCF(NOLOCK) A JOIN SAQVDV (NOLOCK) B ON A.QUOTE_ID  = '"
					+ str(QTRECID)
					+ "' AND B.QUOTE_ID  = '"
					+ str(QTRECID)
					+ "' WHERE A.QUOTE_SOURCE_FAB_LOCATION_RECORD_ID ='"
					+ str(FABRECID)
					+ "'"
				)
				#tableSAQFDV = {}
				tableInfo2 = SqlHelper.GetTable("SAQFDV")
				for data2 in GETSAQFBLDV:					
					tableSAQFDV = {
						"QUOTE_FAB_VALDRIVER_VALUE_RECORD_ID": str(Guid.NewGuid()).upper(),
						"FABLOCATION_ID": str(data2.SRCFBL_ID),
						"VALUEDRIVER_ID": str(data2.VALUEDRIVER_ID),
						"FABLOCATION_NAME": str(data2.SRCFBL_NAME),
						"FABLOCATION_RECORD_ID": str(data2.SRCFBL_RECORD_ID),
						"QUOTE_ID": str(data2.QUOTE_ID),
						"QUOTE_NAME": str(data2.QUOTE_NAME),
						"QUOTE_RECORD_ID": str(data2.QUOTE_RECORD_ID),
						"VALUEDRIVER_NAME": str(data2.VALUEDRIVER_NAME),
						"VALUEDRIVER_RECORD_ID": str(data2.VALUEDRIVER_RECORD_ID),
						"VALUEDRIVER_VALUEDESC": str(data2.VALUEDRIVER_VALUE_DESCRIPTION),
						"QUOTE_FABLOCATION_RECORD_ID": str(data2.QUOTE_SOURCE_FAB_LOCATION_RECORD_ID),
						"CPQTABLEENTRYDATEADDED": datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"),
						"CPQTABLEENTRYADDEDBY": self.user_name,
						"ADDUSR_RECORD_ID": self.user_id,
					}					
					tableInfo2.AddRow(tableSAQFDV)
					# upsertResult = SqlHelper.Upsert(tableInfo2)
				Sql.Upsert(tableInfo2)
		elif self.action_type == "ADD_EQUIPMENTS":
			self._add_equipment()
		
		elif self.action_type == "ADD_UNMAPPED_EQUIPMENTS":
			# SAQFBL INSERT FOR UNMAPPED EQUIPMENTS STARTS
			#Trace.Write("Unmapped_chk_j "+str(list(self.values)))
			#Trace.Write("self.contract_quote_id "+str(self.contract_quote_id))
			
			master_fab = Sql.GetFirst("SELECT * FROM MAFBLC (NOLOCK) WHERE FAB_LOCATION_ID = 'UNMAPPED' AND FAB_LOCATION_ID NOT IN (SELECT FABLOCATION_ID FROM SAQFBL (NOLOCK) WHERE QUOTE_RECORD_ID = '"+str(self.contract_quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"')  ")
			acunt_info = Sql.GetFirst("SELECT ACCOUNT_ID, ACCOUNT_NAME, ACCOUNT_RECORD_ID FROM SAACNT (NOLOCK) WHERE ACCOUNT_ID = '"+str(self.tree_param).split('-')[1].strip()+"'")
			if master_fab:

				unmapped_fab_table_info = SqlHelper.GetTable("SAQFBL")
				fab_table ={
					"QUOTE_FABLOCATION_RECORD_ID": str(Guid.NewGuid()).upper(),
					"FABLOCATION_ID": str(master_fab.FAB_LOCATION_ID),
					"FABLOCATION_NAME": str(master_fab.FAB_LOCATION_NAME),
					"FABLOCATION_RECORD_ID": str(master_fab.FAB_LOCATION_RECORD_ID),
					"QUOTE_ID": str(self.contract_quote_id),
					"QUOTE_NAME": str(self.contract_quote_name),
					"QUOTE_RECORD_ID": str(self.contract_quote_record_id),
					"COUNTRY": str(master_fab.COUNTRY),
					"COUNTRY_RECORD_ID": str(master_fab.COUNTRY_RECORD_ID),
					"MNT_PLANT_ID": str(master_fab.MNT_PLANT_ID),
					"MNT_PLANT_NAME": str(master_fab.MNT_PLANT_NAME),
					"MNT_PLANT_RECORD_ID": str(master_fab.MNT_PLANT_RECORD_ID),
					"SALESORG_ID": str(master_fab.SALESORG_ID),
					"SALESORG_NAME": str(master_fab.SALESORG_NAME),
					"SALESORG_RECORD_ID": str(master_fab.SALESORG_RECORD_ID),
					"FABLOCATION_STATUS": "",
					"ADDRESS_1": str(master_fab.ADDRESS_1),
					"ADDRESS_2": str(master_fab.ADDRESS_2),
					"CITY": str(master_fab.CITY),
					"STATE": str(master_fab.STATE),
					"STATE_RECORD_ID": str(master_fab.STATE_RECORD_ID),
					"RELOCATION_FAB_TYPE": "SENDING FAB",
					"ACCOUNT_ID": str(acunt_info.ACCOUNT_ID),
					"ACCOUNT_NAME": str(acunt_info.ACCOUNT_NAME),
					"ACCOUNT_RECORD_ID": str(acunt_info.ACCOUNT_RECORD_ID),
					"QTEREV_RECORD_ID": str(self.quote_revision_record_id)

				}
				unmapped_fab_table_info.AddRow(fab_table)
				Sql.Upsert(unmapped_fab_table_info)


			# SAQFBL INSERT FOR UNMAPPED EQUIPMENTS ENDS

			master_object_name = "MAEQUP"
			if self.values:
				record_ids = [value for value in self.values]
				#Trace.Write("record_ids_chk_j "+str(record_ids))
				for rec in record_ids:
					obj = rec.split('-')[0]
					cpq_entry = rec.split('-')[1].lstrip('0')
					Trace.Write("cpq_entry_Chk_J"+str(cpq_entry))
					# maequp_data = Sql.GetFirst("SELECT * FROM MAEQUP (NOLOCK) WHERE CpqTableEntryId = '"+str(cpq_entry)+"'")
					self._process_query(
						"""
							INSERT SAQFEQ (
								QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID,
								EQUIPMENT_ID,
								EQUIPMENT_RECORD_ID,
								EQUIPMENT_DESCRIPTION,                            
								FABLOCATION_ID,
								FABLOCATION_NAME,
								FABLOCATION_RECORD_ID,
								SERIAL_NUMBER,
								QUOTE_RECORD_ID,
								QUOTE_ID,
								QUOTE_NAME,
								QTEREV_ID,
								QTEREV_RECORD_ID,
								PLATFORM,
								EQUIPMENTCATEGORY_RECORD_ID,
								EQUIPMENTCATEGORY_ID,
								EQUIPMENTCATEGORY_DESCRIPTION,
								EQUIPMENT_STATUS,
								PBG,
								GREENBOOK,
								GREENBOOK_RECORD_ID,
								MNT_PLANT_RECORD_ID,
								MNT_PLANT_ID,
								MNT_PLANT_NAME,
								WARRANTY_START_DATE,
								WARRANTY_END_DATE,
								SALESORG_ID,
								SALESORG_NAME,
								SALESORG_RECORD_ID,
								CUSTOMER_TOOL_ID,
								CPQTABLEENTRYADDEDBY,
								CPQTABLEENTRYDATEADDED,
								CpqTableEntryModifiedBy,
								CpqTableEntryDateModified,
								RELOCATION_FAB_TYPE,
								RELOCATION_EQUIPMENT_TYPE,WAFER_SIZE,
								TECHNOLOGY
								) SELECT
									CONVERT(VARCHAR(4000),NEWID()) as QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID,
									MAEQUP.EQUIPMENT_ID,
									MAEQUP.EQUIPMENT_RECORD_ID,
									MAEQUP.EQUIPMENT_DESCRIPTION,                                
									MAEQUP.FABLOCATION_ID,
									MAEQUP.FABLOCATION_NAME,
									MAEQUP.FABLOCATION_RECORD_ID,
									MAEQUP.SERIAL_NO,
									'{QuoteRecId}' as QUOTE_RECORD_ID,
									'{QuoteId}' as QUOTE_ID,
									'{QuoteName}' as QUOTE_NAME,
									'{RevisionId}' as QTEREV_ID,
									'{RevisionRecordId}' as QTEREV_RECORD_ID,
									MAEQUP.PLATFORM,
									MAEQUP.EQUIPMENTCATEGORY_RECORD_ID,
									MAEQUP.EQUIPMENTCATEGORY_ID,
									MAEQUP.EQUIPMENTCATEGORY_DESCRIPTION,
									MAEQUP.EQUIPMENT_STATUS,
									MAEQUP.PBG,
									MAEQUP.GREENBOOK,
									MAEQUP.GREENBOOK_RECORD_ID,
									MAEQUP.MNT_PLANT_RECORD_ID,
									MAEQUP.MNT_PLANT_ID,
									MAEQUP.MNT_PLANT_NAME,
									MAEQUP.WARRANTY_START_DATE,
									MAEQUP.WARRANTY_END_DATE,
									MAEQUP.SALESORG_ID,
									MAEQUP.SALESORG_NAME,
									MAEQUP.SALESORG_RECORD_ID,
									MAEQUP.CUSTOMER_TOOL_ID,
									'{UserName}' AS CPQTABLEENTRYADDEDBY,
									GETDATE() as CPQTABLEENTRYDATEADDED,
									{UserId} as CpqTableEntryModifiedBy,
									GETDATE() as CpqTableEntryDateModified,
									'{relocation_fab_type}' AS RELOCATION_FAB_TYPE,
									'{relocation_equp_type}' AS RELOCATION_EQUIPMENT_TYPE,
									MAEQUP.SUBSTRATE_SIZE,
									MAEQUP.TECHNOLOGY
									FROM MAEQUP (NOLOCK) WHERE CpqTableEntryId = '{cpq_entry}'
						""".format(
								treeparam=self.tree_param,
								treeparentparam=self.tree_parent_level_0,
								QuoteId=self.contract_quote_id,
								UserName=self.user_name,
								UserId=self.user_id,
								cpq_entry=cpq_entry,
								QuoteRecId=self.contract_quote_record_id,
								QuoteName=self.contract_quote_name,
								RevisionId=self.quote_revision_id,
								RevisionRecordId=self.quote_revision_record_id,
								relocation_fab_type = "SENDING FAB" if "Sending Account -" in self.tree_param else "RECEIVING FAB" if "Receiving Account -" in self.tree_param else "",
								relocation_equp_type = "SENDING EQUIPMENT" if "Sending Account -" in self.tree_param else "RECEIVING EQUIPMENT" if "Receiving Account -" in self.tree_param else "",
						)
					)
					##unmapped fab's greenbook insert
					self._process_query(
						"""INSERT SAQFGB(
							FABLOCATION_ID,
							FABLOCATION_NAME,
							FABLOCATION_RECORD_ID,
							GREENBOOK,
							GREENBOOK_RECORD_ID,
							QUOTE_ID,
							QUOTE_NAME,
							QUOTE_RECORD_ID,
							QTEREV_ID,
							QTEREV_RECORD_ID,
							SALESORG_ID,
							SALESORG_NAME,
							SALESORG_RECORD_ID,						
							CpqTableEntryModifiedBy,
							CpqTableEntryDateModified,
							QUOTE_FAB_LOC_GB_RECORD_ID,
							CPQTABLEENTRYADDEDBY,
							CPQTABLEENTRYDATEADDED
							) SELECT FB.*,CONVERT(VARCHAR(4000),NEWID()) as QUOTE_FAB_LOC_GB_RECORD_ID,
							'{UserName}' AS CPQTABLEENTRYADDEDBY,
							GETDATE() as CPQTABLEENTRYDATEADDED FROM (
							SELECT DISTINCT
							SAQFEQ.FABLOCATION_ID,
							SAQFEQ.FABLOCATION_NAME,
							SAQFEQ.FABLOCATION_RECORD_ID,
							SAQFEQ.GREENBOOK,
							SAQFEQ.GREENBOOK_RECORD_ID,
							SAQFEQ.QUOTE_ID,
							SAQFEQ.QUOTE_NAME,
							SAQFEQ.QUOTE_RECORD_ID,
							SAQFEQ.QTEREV_ID,
							SAQFEQ.QTEREV_RECORD_ID,
							SAQFEQ.SALESORG_ID,
							SAQFEQ.SALESORG_NAME,
							SAQFEQ.SALESORG_RECORD_ID,
							{UserId} as CpqTableEntryModifiedBy,
							GETDATE() as CpqTableEntryDateModified
							FROM SAQFEQ (NOLOCK)
							JOIN MAEQUP (NOLOCK) ON MAEQUP.SALESORG_ID = SAQFEQ.SALESORG_ID AND MAEQUP.EQUIPMENT_RECORD_ID = SAQFEQ.EQUIPMENT_RECORD_ID AND MAEQUP.FABLOCATION_ID = SAQFEQ.FABLOCATION_ID
							
							WHERE SAQFEQ.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQFEQ.QTEREV_RECORD_ID = '{RevisionRecordId}' AND MAEQUP.CpqTableEntryId = '{cpq_entry}' AND SAQFEQ.GREENBOOK NOT IN (SELECT GREENBOOK FROM SAQFGB WHERE QUOTE_RECORD_ID ='{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND FABLOCATION_ID ='UNMAPPED')
							) FB""".format(
											treeparam=self.tree_param,
											QuoteRecordId=self.contract_quote_record_id,
           									RevisionRecordId=self.quote_revision_record_id,
											UserId=self.user_id,
											UserName=self.user_name,
											cpq_entry = cpq_entry,
										)
						)		
			
					
					
					# unmapped_equp_table_info = SqlHelper.GetTable("SAEQUP")
					# equp_table ={
					# 	"QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID": str(Guid.NewGuid()).upper(),
					# 	"EQUIPMENT_ID": str(maequp_data.EQUIPMENT_ID),
					# 	"EQUIPMENT_RECORD_ID": str(maequp_data.EQUIPMENT_RECORD_ID),
					# 	"FABLOCATION_ID": str(maequp_data.FABLOCATION_ID),
					# 	"FABLOCATION_NAME": str(maequp_data.FABLOCATION_NAME),
					# 	"FABLOCATION_RECORD_ID": str(maequp_data.FABLOCATION_RECORD_ID),
					# 	"SERIAL_NUMBER": str(maequp_data.SERIAL_NO),
					# 	"QUOTE_RECORD_ID": str(self.contract_quote_record_id),
					# 	"QUOTE_ID": str(self.contract_quote_id),
					# 	"QUOTE_NAME": str(self.contract_quote_name),
					# 	"SNDACC_ID": str(maequp_data.ACCOUNT_ID),
					# 	"SNDACC_NAME": str(maequp_data.ACCOUNT_NAME),
					# 	"SNDACC_RECORD_ID": str(maequp_data.ACCOUNT_RECORD_ID),
					# 	"PLATFORM": str(maequp_data.PLATFORM),
					# 	"EQUIPMENTCATEGORY_RECORD_ID": str(maequp_data.EQUIPMENTCATEGORY_RECORD_ID),
					# 	"EQUIPMENTCATEGORY_ID": str(maequp_data.EQUIPMENTCATEGORY_ID),
					# 	"EQUIPMENTCATEGORY_DESCRIPTION": str(maequp_data.EQUIPMENTCATEGORY_DESCRIPTION),
					# 	"EQUIPMENT_STATUS": str(maequp_data.EQUIPMENT_STATUS),
					# 	"PBG": str(maequp_data.PBG),
					# 	"GREENBOOK": str(maequp_data.GREENBOOK),
					# 	"GREENBOOK_RECORD_ID": str(maequp_data.GREENBOOK_RECORD_ID),
					# 	"MNT_PLANT_RECORD_ID": str(maequp_data.MNT_PLANT_RECORD_ID),
					# 	"MNT_PLANT_ID": str(maequp_data.MNT_PLANT_ID),
					# 	"MNT_PLANT_NAME": str(maequp_data.MNT_PLANT_NAME),
					# 	"WARRANTY_START_DATE": str(maequp_data.WARRANTY_START_DATE),
					# 	"WARRANTY_END_DATE": str(maequp_data.WARRANTY_END_DATE),
					# 	"SALESORG_ID": str(maequp_data.SALESORG_ID),
					# 	"SALESORG_NAME": str(maequp_data.SALESORG_NAME),
					# 	"SALESORG_RECORD_ID": str(maequp_data.SALESORG_RECORD_ID),
					# 	"CUSTOMER_TOOL_ID": str(maequp_data.CUSTOMER_TOOL_ID),
					# 	"RELOCATION_FAB_TYPE": "SENDING FAB",
					# 	"RELOCATION_EQUIPMENT_TYPE": "SENDING EQUIPMENT",
					# 	"WAFER_SIZE": str(maequp_data.SUBSTRATE_SIZE),
					# 	"TECHNOLOGY": str(maequp_data.TECHNOLOGY)
					# }
					# unmapped_equp_table_info.AddRow(equp_table)
					# SqlHelper.Upsert(unmapped_equp_table_info)
				

			# 						) SELECT
			# 							CONVERT(VARCHAR(4000),NEWID()) as QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID,
			# 							MAEQUP.EQUIPMENT_ID,
			# 							MAEQUP.EQUIPMENT_RECORD_ID,
			# 							MAEQUP.EQUIPMENT_DESCRIPTION,                                
			# 							MAEQUP.FABLOCATION_ID,
			# 							MAEQUP.FABLOCATION_NAME,
			# 							MAEQUP.FABLOCATION_RECORD_ID,
			# 							MAEQUP.SERIAL_NO,
			# 							'{QuoteRecId}' as QUOTE_RECORD_ID,
			# 							'{QuoteId}' as QUOTE_ID,
			# 							'{QuoteName}' as QUOTE_NAME,
			# 							MAEQUP.ACCOUNT_ID,
			# 							MAEQUP.ACCOUNT_NAME,
			# 							MAEQUP.ACCOUNT_RECORD_ID,
			# 							MAEQUP.PLATFORM,
			# 							MAEQUP.EQUIPMENTCATEGORY_RECORD_ID,
			# 							MAEQUP.EQUIPMENTCATEGORY_ID,
			# 							MAEQCT.EQUIPMENTCATEGORY_DESCRIPTION,
			# 							MAEQUP.EQUIPMENT_STATUS,
			# 							MAEQUP.PBG,
			# 							MAEQUP.GREENBOOK,
			# 							MAEQUP.GREENBOOK_RECORD_ID,
			# 							MAEQUP.MNT_PLANT_RECORD_ID,
			# 							MAEQUP.MNT_PLANT_ID,
			# 							MAEQUP.MNT_PLANT_NAME,
			# 							MAEQUP.WARRANTY_START_DATE,
			# 							MAEQUP.WARRANTY_END_DATE,
			# 							MAEQUP.SALESORG_ID,
			# 							MAEQUP.SALESORG_NAME,
			# 							MAEQUP.SALESORG_RECORD_ID,
			# 							MAEQUP.CUSTOMER_TOOL_ID,
			# 							'{UserName}' AS CPQTABLEENTRYADDEDBY,
			# 							GETDATE() as CPQTABLEENTRYDATEADDED,
			# 							{UserId} as CpqTableEntryModifiedBy,
			# 							GETDATE() as CpqTableEntryDateModified,
			# 							'{relocation_fab_type}' AS RELOCATION_FAB_TYPE,
			# 							'{relocation_equp_type}' AS RELOCATION_EQUIPMENT_TYPE,
			# 							MAEQUP.SUBSTRATE_SIZE,
			# 							MAEQUP.TECHNOLOGY
			# 							FROM MAEQUP (NOLOCK)
			# 							JOIN SYSPBT (NOLOCK) ON SYSPBT.BATCH_RECORD_ID = MAEQUP.EQUIPMENT_RECORD_ID JOIN MAEQCT(NOLOCK)
			# 							ON MAEQUP.EQUIPMENTCATEGORY_ID = MAEQCT.EQUIPMENTCATEGORY_ID
			# 							WHERE 
			# 							SYSPBT.QUOTE_RECORD_ID = '{QuoteRecId}'
			# 							AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}'                        
			# 					""".format(
			# 					treeparam=self.tree_param,
			# 					treeparentparam=self.tree_parent_level_0,
			# 					QuoteId=self.contract_quote_id,
			# 					BatchGroupRecordId=batch_group_record_id,
			# 					UserName=self.user_name,
			# 					UserId=self.user_id,
			# 					QuoteRecId=self.contract_quote_record_id,
			# 					QuoteName=self.contract_quote_name,
			# 					relocation_fab_type = "SENDING FAB" if "Sending Account -" in self.tree_param else "RECEIVING FAB" if "Receiving Account -" in self.tree_param else "",
			# 					relocation_equp_type = "SENDING EQUIPMENT" if "Sending Account -" in self.tree_param else "RECEIVING EQUIPMENT" if "Receiving Account -" in self.tree_param else "",
			# 				)
			# 			)
		return True

	def _add_equipment(self,auto_equp_insert = None,fab_list= None):
		#EquipList=[]
		Trace.Write("equp add"+str(auto_equp_insert))
		master_object_name = "MAEQUP"
		if self.values:
			record_ids = []
			if self.all_values and auto_equp_insert is None: 
				Trace.Write('ifff--'+str(fab_list))		      
				query_string = "SELECT EQUIPMENT_RECORD_ID FROM MAEQUP (NOLOCK) WHERE ACCOUNT_RECORD_ID = '{acc}' AND FABLOCATION_ID = '{fab}' AND ISNULL(SERIAL_NO, '') <> '' AND ISNULL(GREENBOOK, '') <> '' AND  EQUIPMENT_RECORD_ID NOT IN  (SELECT EQUIPMENT_RECORD_ID FROM SAQFEQ (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND FABLOCATION_ID = '{fab}' )".format(
							acc=self.account_record_id,
							fab=self.tree_param,
							salesorgrecid=self.salesorg_record_id,
							QuoteRecordId=self.contract_quote_record_id,
							RevisionRecordId=self.quote_revision_record_id
       					)			
				query_string_for_count = "SELECT COUNT(*) as count FROM ({Query_String})OQ".format(
					Query_String=query_string
				)
				#Trace.Write("query_string_for_count"+str(query_string))
				get_fab = "('"+str(self.tree_param)+"')"
				table_count_data = Sql.GetFirst(query_string_for_count)
				if table_count_data is not None:
					table_total_rows = table_count_data.count
				if table_total_rows:
					record_ids = [data for data in self.get_res(query_string, table_total_rows)]   
			##equipment auto insert for sending equipment
			elif auto_equp_insert == "true": 
				#Trace.Write('ifff1--')       
				account_id = self.tree_param.split(' - ')
				account_id = account_id[len(account_id)-1]
				fab_type = 'SENDING FAB' if "Sending Account -" in self.tree_param else 'RECEIVING FAB' if "Receiving Account -" in self.tree_param else ""
				get_fab_query = Sql.GetList("SELECT FABLOCATION_ID FROM SAQFBL WHERE QUOTE_RECORD_ID = '{}' and QTEREV_RECORD_ID = '{}' and ACCOUNT_ID = '{}' and RELOCATION_FAB_TYPE = '{}' ".format(self.contract_quote_record_id,self.quote_revision_record_id,account_id,fab_type) )
				if get_fab_query:
					get_fab = str(tuple([fab['FABLOCATION_ID'] for fab in fab_list])).replace(",)",')')
				else:
					get_fab = ""
				query_string = "SELECT EQUIPMENT_RECORD_ID FROM MAEQUP (NOLOCK) WHERE ACCOUNT_ID = '{acc}' AND FABLOCATION_ID in {fab} AND  ISNULL(SERIAL_NO, '') <> '' AND ISNULL(GREENBOOK, '') <> '' AND NOT EXISTS (SELECT EQUIPMENT_RECORD_ID FROM SAQFEQ (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND FABLOCATION_ID in {fab} and RELOCATION_EQUIPMENT_TYPE = '{equp_type}' )".format(
							acc=account_id,
							fab=get_fab,
							QuoteRecordId=self.contract_quote_record_id,
							RevisionRecordId=self.quote_revision_record_id,
							equp_type = "SENDING EQUIPMENT" if "Sending Account -" in self.tree_param else "RECEIVING EQUIPMENT" if "Receiving Account -" in self.tree_param else "" )
				query_string_for_count = "SELECT COUNT(*) as count FROM ({Query_String})OQ".format(
					Query_String=query_string
				)
				table_count_data = Sql.GetFirst(query_string_for_count)
				if table_count_data is not None:
					table_total_rows = table_count_data.count
				if table_total_rows:
					record_ids = [data for data in self.get_res(query_string, table_total_rows)]                  
			else:
				get_fab = "('"+str(self.tree_param)+"')"
				record_ids = [
					CPQID.KeyCPQId.GetKEYId(master_object_name, str(value))
					if value.strip() != "" and master_object_name in value
					else value
					for value in self.values
				]
			batch_group_record_id = str(Guid.NewGuid()).upper()
			record_ids = str(str(record_ids)[1:-1].replace("'",""))
			parameter = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'SELECT' ")
			SqlHelper.GetFirst(""+str(parameter.QUERY_CRITERIA_1)+" SYSPBT(BATCH_RECORD_ID, BATCH_STATUS, QUOTE_ID, QUOTE_RECORD_ID, BATCH_GROUP_RECORD_ID,QTEREV_RECORD_ID) SELECT MAEQUP.EQUIPMENT_RECORD_ID as BATCH_RECORD_ID, ''IN PROGRESS'' as BATCH_STATUS, ''"+str(self.contract_quote_id)+"'' as QUOTE_ID, ''"+str(self.contract_quote_record_id)+"'' as QUOTE_RECORD_ID, ''"+str(batch_group_record_id)+"'' as BATCH_GROUP_RECORD_ID,''"+str(self.quote_revision_record_id)+"'' as QTEREV_RECORD_ID FROM MAEQUP (NOLOCK) JOIN splitstring(''"+record_ids+"'') ON ltrim(rtrim(NAME)) = MAEQUP.EQUIPMENT_RECORD_ID'")

			self._process_query(
							"""
								INSERT SAQFEQ (
									QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID,
									EQUIPMENT_ID,
									EQUIPMENT_RECORD_ID,
									EQUIPMENT_DESCRIPTION,                            
									FABLOCATION_ID,
									FABLOCATION_NAME,
									FABLOCATION_RECORD_ID,
									SERIAL_NUMBER,
									QUOTE_RECORD_ID,
									QUOTE_ID,
									QUOTE_NAME,
									QTEREV_ID,
									QTEREV_RECORD_ID,
									PLATFORM,
									EQUIPMENTCATEGORY_RECORD_ID,
									EQUIPMENTCATEGORY_ID,
									EQUIPMENTCATEGORY_DESCRIPTION,
									EQUIPMENT_STATUS,
									PBG,
									GREENBOOK,
									GREENBOOK_RECORD_ID,
									MNT_PLANT_RECORD_ID,
									MNT_PLANT_ID,
									MNT_PLANT_NAME,
									WARRANTY_START_DATE,
									WARRANTY_END_DATE,
									SALESORG_ID,
									SALESORG_NAME,
									SALESORG_RECORD_ID,
									CUSTOMER_TOOL_ID,
									CPQTABLEENTRYADDEDBY,
									CPQTABLEENTRYDATEADDED,
									CpqTableEntryModifiedBy,
									CpqTableEntryDateModified,
									RELOCATION_FAB_TYPE,
									RELOCATION_EQUIPMENT_TYPE,WAFER_SIZE,
									TECHNOLOGY
									) SELECT
										CONVERT(VARCHAR(4000),NEWID()) as QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID,
										MAEQUP.EQUIPMENT_ID,
										MAEQUP.EQUIPMENT_RECORD_ID,
										MAEQUP.EQUIPMENT_DESCRIPTION,                                
										MAEQUP.FABLOCATION_ID,
										MAEQUP.FABLOCATION_NAME,
										MAEQUP.FABLOCATION_RECORD_ID,
										MAEQUP.SERIAL_NO,
										'{QuoteRecId}' as QUOTE_RECORD_ID,
										'{QuoteId}' as QUOTE_ID,
										'{QuoteName}' as QUOTE_NAME,
										'{RevisionId}' as QTEREV_ID,
										'{RevisionRecordId}' as QTEREV_RECORD_ID,
										MAEQUP.PLATFORM,
										MAEQUP.EQUIPMENTCATEGORY_RECORD_ID,
										MAEQUP.EQUIPMENTCATEGORY_ID,
										MAEQCT.EQUIPMENTCATEGORY_DESCRIPTION,
										MAEQUP.EQUIPMENT_STATUS,
										MAEQUP.PBG,
										MAEQUP.GREENBOOK,
										MAEQUP.GREENBOOK_RECORD_ID,
										MAEQUP.MNT_PLANT_RECORD_ID,
										MAEQUP.MNT_PLANT_ID,
										MAEQUP.MNT_PLANT_NAME,
										MAEQUP.WARRANTY_START_DATE,
										MAEQUP.WARRANTY_END_DATE,
										MAEQUP.SALESORG_ID,
										MAEQUP.SALESORG_NAME,
										MAEQUP.SALESORG_RECORD_ID,
										MAEQUP.CUSTOMER_TOOL_ID,
										'{UserName}' AS CPQTABLEENTRYADDEDBY,
										GETDATE() as CPQTABLEENTRYDATEADDED,
										{UserId} as CpqTableEntryModifiedBy,
										GETDATE() as CpqTableEntryDateModified,
										'{relocation_fab_type}' AS RELOCATION_FAB_TYPE,
										'{relocation_equp_type}' AS RELOCATION_EQUIPMENT_TYPE,
										MAEQUP.SUBSTRATE_SIZE,
										MAEQUP.TECHNOLOGY
										FROM MAEQUP (NOLOCK)
										JOIN SYSPBT (NOLOCK) ON SYSPBT.BATCH_RECORD_ID = MAEQUP.EQUIPMENT_RECORD_ID JOIN MAEQCT(NOLOCK)
										ON MAEQUP.EQUIPMENTCATEGORY_ID = MAEQCT.EQUIPMENTCATEGORY_ID
										WHERE 
										SYSPBT.QUOTE_RECORD_ID = '{QuoteRecId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'
										AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}'                        
								""".format(
								treeparam=self.tree_param,
								treeparentparam=self.tree_parent_level_0,
								QuoteId=self.contract_quote_id,
								BatchGroupRecordId=batch_group_record_id,
								UserName=self.user_name,
								UserId=self.user_id,
								QuoteRecId=self.contract_quote_record_id,
								RevisionId=self.quote_revision_id,
								RevisionRecordId=self.quote_revision_record_id,
								QuoteName=self.contract_quote_name,
								relocation_fab_type = "SENDING FAB" if "Sending Account -" in self.tree_param else "RECEIVING FAB" if "Receiving Account -" in self.tree_param else "",
								relocation_equp_type = "SENDING EQUIPMENT" if "Sending Account -" in self.tree_param else "RECEIVING EQUIPMENT" if "Receiving Account -" in self.tree_param else "",
							)
						)
			
			self._process_query(
					"""INSERT SAQFGB(
						FABLOCATION_ID,
						FABLOCATION_NAME,
						FABLOCATION_RECORD_ID,
						GREENBOOK,
						GREENBOOK_RECORD_ID,
						QUOTE_ID,
						QUOTE_NAME,
						QUOTE_RECORD_ID,
						QTEREV_ID,
						QTEREV_RECORD_ID,
						SALESORG_ID,
						SALESORG_NAME,
						SALESORG_RECORD_ID,						
						CpqTableEntryModifiedBy,
						CpqTableEntryDateModified,
						QUOTE_FAB_LOC_GB_RECORD_ID,
						CPQTABLEENTRYADDEDBY,
						CPQTABLEENTRYDATEADDED
						) SELECT FB.*,CONVERT(VARCHAR(4000),NEWID()) as QUOTE_FAB_LOC_GB_RECORD_ID,
						'{UserName}' AS CPQTABLEENTRYADDEDBY,
						GETDATE() as CPQTABLEENTRYDATEADDED FROM (
						SELECT DISTINCT
						SAQFEQ.FABLOCATION_ID,
						SAQFEQ.FABLOCATION_NAME,
						SAQFEQ.FABLOCATION_RECORD_ID,
						SAQFEQ.GREENBOOK,
						SAQFEQ.GREENBOOK_RECORD_ID,
						SAQFEQ.QUOTE_ID,
						SAQFEQ.QUOTE_NAME,
						SAQFEQ.QUOTE_RECORD_ID,
						SAQFEQ.QTEREV_ID,
						SAQFEQ.QTEREV_RECORD_ID,
						SAQFEQ.SALESORG_ID,
						SAQFEQ.SALESORG_NAME,
						SAQFEQ.SALESORG_RECORD_ID,
						{UserId} as CpqTableEntryModifiedBy,
						GETDATE() as CpqTableEntryDateModified
						FROM SAQFEQ (NOLOCK)
						JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQFEQ.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = SAQFEQ.QTEREV_RECORD_ID
						JOIN SYSPBT (NOLOCK) ON SYSPBT.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SYSPBT.BATCH_RECORD_ID = SAQFEQ.EQUIPMENT_RECORD_ID AND SYSPBT.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID WHERE SAQFEQ.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQFEQ.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}'  AND NOT EXISTS (SELECT * FROM SAQFGB B WHERE QUOTE_RECORD_ID ='{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQFEQ.GREENBOOK = B.GREENBOOK AND FABLOCATION_ID IN {fab})
						) FB""".format(
										treeparam=self.tree_param,
										QuoteRecordId=self.contract_quote_record_id,
										RevisionRecordId=self.quote_revision_record_id,
										BatchGroupRecordId=batch_group_record_id,
										UserId=self.user_id,
										UserName=self.user_name,
										fab = get_fab,
									)
					)		
			self._process_query(
					"""
						INSERT SAQFEA (
							QUOTE_FAB_LOC_COV_OBJ_ASSEMBLY_RECORD_ID,
							EQUIPMENT_ID,
							EQUIPMENT_RECORD_ID,
							EQUIPMENT_DESCRIPTION,
							ASSEMBLY_ID,
							ASSEMBLY_STATUS,
							ASSEMBLY_DESCRIPTION,
							ASSEMBLY_RECORD_ID,                           
							FABLOCATION_ID,
							FABLOCATION_NAME,
							FABLOCATION_RECORD_ID,
							SERIAL_NUMBER,
							QUOTE_RECORD_ID,
							QUOTE_ID,
							QUOTE_NAME,
							QTEREV_ID,
							QTEREV_RECORD_ID,
							EQUIPMENTCATEGORY_RECORD_ID,
							EQUIPMENTCATEGORY_ID,
							EQUIPMENTCATEGORY_DESCRIPTION,
							EQUIPMENTTYPE_ID,
							EQUIPMENTTYPE_DESCRIPTION,
							EQUIPMENTTYPE_RECORD_ID,
							GOT_CODE,
							MNT_PLANT_RECORD_ID,
							MNT_PLANT_ID,
							WARRANTY_START_DATE,
							WARRANTY_END_DATE,
							SALESORG_ID,
							SALESORG_NAME,
							SALESORG_RECORD_ID,
							GREENBOOK,
							GREENBOOK_RECORD_ID,
							CPQTABLEENTRYADDEDBY,
							CPQTABLEENTRYDATEADDED,
							CpqTableEntryModifiedBy,
							CpqTableEntryDateModified
							) SELECT
								CONVERT(VARCHAR(4000),NEWID()) as QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID,
								MAEQUP.PAR_EQUIPMENT_ID,
								MAEQUP.PAR_EQUIPMENT_RECORD_ID,
								MAEQUP.PAR_EQUIPMENT_DESCRIPTION,
								MAEQUP.EQUIPMENT_ID,
								MAEQUP.EQUIPMENT_STATUS,
								MAEQUP.EQUIPMENT_DESCRIPTION,
								MAEQUP.EQUIPMENT_RECORD_ID,                 
								MAEQUP.FABLOCATION_ID,
								MAEQUP.FABLOCATION_NAME,
								MAEQUP.FABLOCATION_RECORD_ID,
								MAEQUP.SERIAL_NO,
								'{QuoteRecId}' as QUOTE_RECORD_ID,
								'{QuoteId}' as QUOTE_ID,
								'{QuoteName}' as QUOTE_NAME,
								'{RevisionId}' as QTEREV_ID,
								'{RevisionRecordId}' as QTEREV_RECORD_ID,
								MAEQUP.EQUIPMENTCATEGORY_RECORD_ID,
								MAEQUP.EQUIPMENTCATEGORY_ID,
								MAEQCT.EQUIPMENTCATEGORY_DESCRIPTION,
								MAEQUP.EQUIPMENTTYPE_ID,
								MAEQTY.EQUIPMENT_TYPE_DESCRIPTION,
								MAEQUP.EQUIPMENTTYPE_RECORD_ID,
								MAEQUP.GOT_CODE,
								MAEQUP.MNT_PLANT_RECORD_ID,
								MAEQUP.MNT_PLANT_ID,
								MAEQUP.WARRANTY_START_DATE,
								MAEQUP.WARRANTY_END_DATE,
								MAEQUP.SALESORG_ID,
								MAEQUP.SALESORG_NAME,
								MAEQUP.SALESORG_RECORD_ID,
								MAEQUP.GREENBOOK,
								MAEQUP.GREENBOOK_RECORD_ID,
								'{UserName}' AS CPQTABLEENTRYADDEDBY,
								GETDATE() as CPQTABLEENTRYDATEADDED,
								{UserId} as CpqTableEntryModifiedBy,
								GETDATE() as CpqTableEntryDateModified
								FROM MAEQUP (NOLOCK)
								JOIN SYSPBT (NOLOCK)
								ON SYSPBT.BATCH_RECORD_ID = MAEQUP.PAR_EQUIPMENT_RECORD_ID JOIN MAEQCT(NOLOCK)
								ON MAEQUP.EQUIPMENTCATEGORY_ID = MAEQCT.EQUIPMENTCATEGORY_ID JOIN MAEQTY (NOLOCK)
								ON MAEQTY.EQUIPMENT_TYPE_ID = MAEQUP.EQUIPMENTTYPE_ID
								WHERE 
								SYSPBT.QUOTE_RECORD_ID = '{QuoteRecId}'
								AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}'                        
						""".format(
						treeparam=self.tree_param,
						treeparentparam=self.tree_parent_level_0,
						QuoteId=self.contract_quote_id,
						BatchGroupRecordId=batch_group_record_id,
						UserName=self.user_name,
						UserId=self.user_id,
						QuoteRecId=self.contract_quote_record_id,
						RevisionId=self.quote_revision_id,
						RevisionRecordId=self.quote_revision_record_id,
						QuoteName=self.contract_quote_name
					)
				)
			self._process_query(
								"""DELETE FROM SYSPBT WHERE SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}' and SYSPBT.QTEREV_RECORD_ID = '{RevisionRecordId}' and SYSPBT.BATCH_STATUS = 'IN PROGRESS'""".format(
									BatchGroupRecordId=batch_group_record_id,RevisionRecordId=self.quote_revision_record_id
								)
							)

		#Trace.Write("ADDEQUIPMENT"+str(EquipList))
		#Trace.Write("ADDfabtrace"+str(row_detail.get("FABLOCATION_ID")))
		#try:
		#	quote = self.contract_quote_record_id
		#	#level = "FAB LEVEL,"+str(row_detail.get("FABLOCATION_ID"))+","+str(row_detail.get("EQUIPMENT_ID"))+","+str(self.user_id)+","+str(self.user_name)
		#	level = "FAB LEVEL,"+str(self.tree_param)+","+str(self.tree_parent_level_0)+","+str(self.user_id)+","+str(self.user_name)
		#	CQVLDRIFLW.iflow_valuedriver_rolldown(quote,level)
		#except:
		#	Trace.Write("EXCEPT----FAB LEVEL IFLOW")
		try:
			quote = self.contract_quote_record_id
			level = "FAB VALUE DRIVER"			
			CQTVLDRIFW.iflow_valuedriver_rolldown(quote,level,self.tree_param, self.tree_parent_level_0, self.tree_parent_level_1, self.tree_parent_level_2,self.user_id,self.user_name)
		except:
			Trace.Write("EXCEPT----QUOTE FAB VALUE DRIVER LEVEL IFLOW")
		#try:
		#	quote = self.contract_quote_record_id
		#	level = "EQUIP FROM CPQ,"+str(TreeParam)+","+str(TreeParentParam)
		#	CQVLDRIFLW.iflow_valuedriver_rolldown(quote,level)
		#except:
		#	Trace.Write("EXCEPT----FAB LEVEL IFLOW")
		return True

	def _update(self):
		pass

	def _delete(self):
		pass
	
	def get_res(self, query_string, table_total_rows):
		for offset_skip_count in range(0, table_total_rows+1, 1000):
			pagination_condition = "WHERE SNO>={Skip_Count} AND SNO<={Fetch_Count}".format(Skip_Count=offset_skip_count+1, Fetch_Count=offset_skip_count+1000)
			query_string_with_pagination = 'SELECT * FROM (SELECT *, ROW_NUMBER()OVER(ORDER BY EQUIPMENT_RECORD_ID) AS SNO FROM ({Query_String}) IQ)OQ {Pagination_Condition}'.format(
											Query_String=query_string, Pagination_Condition=pagination_condition)
			table_data = Sql.GetList(query_string_with_pagination)
			if table_data is not None:
				for row_data in table_data:
					yield row_data.EQUIPMENT_RECORD_ID

class ContractQuoteCoveredObjModel(ContractQuoteCrudOpertion):
	def __init__(self, **kwargs):
		ContractQuoteCrudOpertion.__init__(self, trigger_from=kwargs.get('trigger_from'), contract_quote_record_id=kwargs.get('contract_quote_record_id'),quote_revision_record_id=kwargs.get('quote_revision_record_id'), 
											tree_param=kwargs.get('tree_param'), tree_parent_level_0=kwargs.get('tree_parent_level_0'),tree_parent_level_1=kwargs.get('tree_parent_level_1'))
		self.opertion = kwargs.get('opertion')
		self.action_type = kwargs.get('action_type')
		self.values = kwargs.get('values')
		self.table_name = kwargs.get('table_name')
		self.all_values = kwargs.get('all_values')		
		self.node_id = ""
	
	def get_results(self, query_string, table_total_rows):
		for offset_skip_count in range(0, table_total_rows+1, 1000):
			pagination_condition = "WHERE SNO>={Skip_Count} AND SNO<={Fetch_Count}".format(Skip_Count=offset_skip_count+1, Fetch_Count=offset_skip_count+1000)
			query_string_with_pagination = 'SELECT * FROM (SELECT *, ROW_NUMBER()OVER(ORDER BY QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID) AS SNO FROM ({Query_String}) IQ)OQ {Pagination_Condition}'.format(
											Query_String=query_string, Pagination_Condition=pagination_condition)
			table_data = Sql.GetList(query_string_with_pagination)
			if table_data is not None:
				for row_data in table_data:
					yield row_data.QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID

	def _insert_quote_service_covered_object(self, **kwargs):
		if self.sale_type == "TOOL RELOCATION":
			Trace.Write('covered_object_insert')
			if self.tree_param != "Sending Equipment":
				relocation = "AND ISNULL(SAQFEQ.RELOCATION_EQUIPMENT_TYPE,'')='"+str(self.tree_param)+"'"
				self._process_query(
					"""
						INSERT SAQSCO (
							QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,
							EQUIPMENT_ID,
							EQUIPMENT_RECORD_ID,
							EQUIPMENT_DESCRIPTION,                            
							SNDFBL_ID,
							SNDFBL_NAME,
							SNDFBL_RECORD_ID,
							WAFER_SIZE,
							SALESORG_ID,
							SALESORG_NAME,
							SALESORG_RECORD_ID,
							SERIAL_NO,
							QUOTE_RECORD_ID,
							QUOTE_ID,
							QUOTE_NAME,
							ACCOUNT_ID,
							ACCOUNT_NAME,
							ACCOUNT_RECORD_ID,
							QTEREV_ID,
							QTEREV_RECORD_ID,
							RELOCATION_EQUIPMENT_TYPE,
							SERVICE_ID,
							SERVICE_TYPE,
							SERVICE_DESCRIPTION,
							SERVICE_RECORD_ID,
							EQUIPMENT_STATUS,
							EQUIPMENTCATEGORY_ID,
							EQUIPMENTCATEGORY_DESCRIPTION,
							EQUIPMENTCATEGORY_RECORD_ID,
							PLATFORM,
							GREENBOOK,
							GREENBOOK_RECORD_ID,
							MNT_PLANT_RECORD_ID,
							MNT_PLANT_NAME,
							MNT_PLANT_ID,
							WARRANTY_START_DATE,
							WARRANTY_END_DATE,
							CONTRACT_VALID_FROM,
							CONTRACT_VALID_TO,
							CUSTOMER_TOOL_ID,
							PAR_SERVICE_DESCRIPTION,
							PAR_SERVICE_ID,
							PAR_SERVICE_RECORD_ID,
							TECHNOLOGY,
							CPQTABLEENTRYADDEDBY,
							CPQTABLEENTRYDATEADDED,
							CpqTableEntryModifiedBy,
							CpqTableEntryDateModified,
							FABLOCATION_ID,
							FABLOCATION_NAME,
							FABLOCATION_RECORD_ID							
							) SELECT
								CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,
								EQUIPMENT_ID,
								EQUIPMENT_RECORD_ID,
								EQUIPMENT_DESCRIPTION,                                
								SAQFEQ.FABLOCATION_ID,
								SAQFEQ.FABLOCATION_NAME,
								SAQFEQ.FABLOCATION_RECORD_ID,
								SAQFEQ.WAFER_SIZE,
								SAQFEQ.SALESORG_ID,
								SAQFEQ.SALESORG_NAME,
								SAQFEQ.SALESORG_RECORD_ID,
								SERIAL_NUMBER,
								SAQFEQ.QUOTE_RECORD_ID,
								SAQFEQ.QUOTE_ID,
								SAQFEQ.QUOTE_NAME,
								'{account_id}' as ACCOUNT_ID,
								'{account_name}' as ACCOUNT_NAME,
								'{account_record_id}' as ACCOUNT_RECORD_ID,
								SAQFEQ.QTEREV_ID,
								SAQFEQ.QTEREV_RECORD_ID,
								'{RelocationEqType}' AS RELOCATION_EQUIPMENT_TYPE,
								'{TreeParam}' as SERVICE_ID,
								'{TreeParentParam}' as SERVICE_TYPE,
								SAQTSV.SERVICE_DESCRIPTION as SERVICE_DESCRIPTION,
								SAQTSV.SERVICE_RECORD_ID as SERVICE_RECORD_ID,
								SAQFEQ.EQUIPMENT_STATUS,
								SAQFEQ.EQUIPMENTCATEGORY_ID,
								SAQFEQ.EQUIPMENTCATEGORY_DESCRIPTION,
								SAQFEQ.EQUIPMENTCATEGORY_RECORD_ID,
								SAQFEQ.PLATFORM,
								SAQFEQ.GREENBOOK,
								SAQFEQ.GREENBOOK_RECORD_ID,
								SAQFEQ.MNT_PLANT_RECORD_ID,
								SAQFEQ.MNT_PLANT_NAME,
								SAQFEQ.MNT_PLANT_ID,
								SAQFEQ.WARRANTY_START_DATE,
								SAQFEQ.WARRANTY_END_DATE,
								SAQTMT.CONTRACT_VALID_FROM,
								SAQTMT.CONTRACT_VALID_TO,
								SAQFEQ.CUSTOMER_TOOL_ID,
								SAQTSV.PAR_SERVICE_DESCRIPTION,
								SAQTSV.PAR_SERVICE_ID,
								SAQTSV.PAR_SERVICE_RECORD_ID,
								SAQFEQ.TECHNOLOGY
								'{UserName}' AS CPQTABLEENTRYADDEDBY,
								GETDATE() as CPQTABLEENTRYDATEADDED,
								{UserId} as CpqTableEntryModifiedBy,
								GETDATE() as CpqTableEntryDateModified
								FROM SAQFEQ (NOLOCK) JOIN SAQTSV (NOLOCK) ON
								SAQFEQ.QUOTE_ID = SAQTSV.QUOTE_ID AND
								SAQTSV.SERVICE_ID = '{TreeParam}' AND
								SAQTSV.SERVICE_TYPE = '{TreeParentParam}'
								JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQFEQ.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = SAQFEQ.QTEREV_RECORD_ID
								JOIN SYSPBT (NOLOCK) ON SYSPBT.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SYSPBT.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID AND {RelocationEqType} SYSPBT.BATCH_RECORD_ID = SAQFEQ.EQUIPMENT_RECORD_ID
								WHERE 
								SAQFEQ.QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'
								AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}'                        
						""".format(
								TreeParam=self.tree_param if (self.tree_parent_level_0 == 'Comprehensive Services' or self.tree_parent_level_0 == 'Complementary Products') and self.sale_type != 'TOOL RELOCATION' else self.tree_parent_level_0,
								TreeParentParam=self.tree_parent_level_0 if (self.tree_parent_level_0 == 'Comprehensive Services' or self.tree_parent_level_0 == 'Complementary Products') and self.sale_type != 'TOOL RELOCATION' else self.tree_parent_level_1,
								QuoteRecordId=self.contract_quote_record_id,
								RevisionRecordId=self.quote_revision_record_id,
								BatchGroupRecordId=kwargs.get('batch_group_record_id'),
								UserName=self.user_name,
								UserId=self.user_id,
								account_id=self.account_id,
								account_name=self.account_name,
								account_record_id=self.account_record_id,
								RelocationEqType=relocation if self.tree_parent_level_1 == 'Complementary Products' else ''
							)
				)
			if self.tree_param == "Sending Equipment":
				self._process_query(
					"""
						INSERT SAQSSE (
							QUOTE_SERVICE_SENDING_FAB_LOC_EQUIP_ID,
							SND_EQUIPMENT_ID,
							SND_EQUIPMENT_RECORD_ID,
							SND_EQUIPMENT_DESCRIPTION,                            
							SNDFBL_ID,
							SNDFBL_NAME,
							SNDFBL_RECORD_ID,
							SALESORG_ID,
							SALESORG_NAME,
							SALESORG_RECORD_ID,
							QUOTE_RECORD_ID,
							QUOTE_ID,
							QUOTE_NAME,
							QTEREV_ID,
							QTEREV_RECORD_ID,
							SERVICE_ID,
							SERVICE_DESCRIPTION,
							SERVICE_RECORD_ID,
							EQUIPMENT_STATUS,
							EQUIPMENTCATEGORY_ID,
							EQUIPMENTCATEGORY_DESCRIPTION,
							EQUIPMENTCATEGORY_RECORD_ID,
							PLATFORM,
							GREENBOOK,
							GREENBOOK_RECORD_ID,
							MNT_PLANT_RECORD_ID,
							MNT_PLANT_NAME,
							MNT_PLANT_ID,
							CPQTABLEENTRYADDEDBY,
							CPQTABLEENTRYDATEADDED,
							CpqTableEntryModifiedBy,
							CpqTableEntryDateModified,
							INCLUDED 
							) SELECT
								CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,
								EQUIPMENT_ID,
								EQUIPMENT_RECORD_ID,
								EQUIPMENT_DESCRIPTION,                                
								SAQFEQ.FABLOCATION_ID,
								SAQFEQ.FABLOCATION_NAME,
								SAQFEQ.FABLOCATION_RECORD_ID,
								SAQFEQ.SALESORG_ID,
								SAQFEQ.SALESORG_NAME,
								SAQFEQ.SALESORG_RECORD_ID,
								SAQFEQ.QUOTE_RECORD_ID,
								SAQFEQ.QUOTE_ID,
								SAQFEQ.QUOTE_NAME,
								SAQFEQ.QTEREV_ID,
								SAQFEQ.QTEREV_RECORD_ID,
								'{TreeParam}' as SERVICE_ID,
								SAQTSV.SERVICE_DESCRIPTION as SERVICE_DESCRIPTION,
								SAQTSV.SERVICE_RECORD_ID as SERVICE_RECORD_ID,
								SAQFEQ.EQUIPMENT_STATUS,
								SAQFEQ.EQUIPMENTCATEGORY_ID,
								SAQFEQ.EQUIPMENTCATEGORY_DESCRIPTION,
								SAQFEQ.EQUIPMENTCATEGORY_RECORD_ID,
								SAQFEQ.PLATFORM,
								SAQFEQ.GREENBOOK,
								SAQFEQ.GREENBOOK_RECORD_ID,
								SAQFEQ.MNT_PLANT_RECORD_ID,
								SAQFEQ.MNT_PLANT_NAME,
								SAQFEQ.MNT_PLANT_ID,
								'{UserName}' AS CPQTABLEENTRYADDEDBY,
								GETDATE() as CPQTABLEENTRYDATEADDED,
								{UserId} as CpqTableEntryModifiedBy,
								GETDATE() as CpqTableEntryDateModified,
								'TOOL' as INCLUDED
								FROM SAQFEQ (NOLOCK) JOIN SAQTSV (NOLOCK) ON
								SAQFEQ.QUOTE_ID = SAQTSV.QUOTE_ID AND
								SAQTSV.SERVICE_ID = '{TreeParam}' AND
								SAQTSV.SERVICE_TYPE = '{TreeParentParam}'
								JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQFEQ.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = SAQFEQ.QTEREV_RECORD_ID
								JOIN SYSPBT (NOLOCK) ON SYSPBT.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SYSPBT.BATCH_RECORD_ID = SAQFEQ.EQUIPMENT_RECORD_ID  AND SYSPBT.QTEREV_RECORD_ID = SAQFEQ.QTEREV_RECORD_ID
								WHERE 
								SAQFEQ.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQFEQ.QTEREV_RECORD_ID = '{RevisionRecordId}'
								AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}'   AND SAQFEQ.RELOCATION_EQUIPMENT_TYPE = 'SENDING EQUIPMENT'                      
						""".format(
								TreeParam=self.tree_param if (self.tree_parent_level_0 == 'Comprehensive Services' or self.tree_parent_level_0 == 'Complementary Products') and self.sale_type != 'TOOL RELOCATION' else self.tree_parent_level_0,
								TreeParentParam=self.tree_parent_level_0 if (self.tree_parent_level_0 == 'Comprehensive Services' or self.tree_parent_level_0 == 'Complementary Products') and self.sale_type != 'TOOL RELOCATION' else self.tree_parent_level_1,
								QuoteRecordId=self.contract_quote_record_id,
								RevisionRecordId=self.quote_revision_record_id,
								BatchGroupRecordId=kwargs.get('batch_group_record_id'),
								UserName=self.user_name,
								UserId=self.user_id,
								RelocationEqType=self.tree_param if self.tree_parent_level_1 == 'Complementary Products' else ''
							)
				)
				Trace.Write("Added for sending equip insert issue "+str(self.tree_parent_level_0))
				# self._process_query(
				# 	"""
				# 		INSERT SAQSCO (
				# 			QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,
				# 			EQUIPMENT_ID,
				# 			EQUIPMENT_RECORD_ID,
				# 			EQUIPMENT_DESCRIPTION,
				# 			SNDFBL_ID,
				# 			FABLOCATION_ID,
				# 			FABLOCATION_NAME,
				# 			FABLOCATION_RECORD_ID,
				# 			WAFER_SIZE,
				# 			BUSINESSUNIT_ID,
				# 			SALESORG_ID,
				# 			SALESORG_NAME,
				# 			SALESORG_RECORD_ID,
				# 			SERIAL_NO,
				# 			QUOTE_RECORD_ID,
				# 			QUOTE_ID,
				# 			QUOTE_NAME,
				# 			RELOCATION_EQUIPMENT_TYPE,
				# 			SERVICE_ID,
				# 			SERVICE_TYPE,
				# 			SERVICE_DESCRIPTION,
				# 			SERVICE_RECORD_ID,
				# 			EQUIPMENT_STATUS,
				# 			EQUIPMENTCATEGORY_ID,
				# 			EQUIPMENTCATEGORY_DESCRIPTION,
				# 			EQUIPMENTCATEGORY_RECORD_ID,
				# 			PLATFORM,
				# 			GREENBOOK,
				# 			GREENBOOK_RECORD_ID,
				# 			MNT_PLANT_RECORD_ID,
				# 			MNT_PLANT_NAME,
				# 			MNT_PLANT_ID,
				# 			WARRANTY_START_DATE,
				# 			WARRANTY_END_DATE,
				# 			CUSTOMER_TOOL_ID,
				# 			PAR_SERVICE_DESCRIPTION,
				# 			PAR_SERVICE_ID,
				# 			PAR_SERVICE_RECORD_ID,
				# 			CPQTABLEENTRYADDEDBY,
				# 			CPQTABLEENTRYDATEADDED,
				# 			CpqTableEntryModifiedBy,
				# 			CpqTableEntryDateModified
				# 			) SELECT
				# 				CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,
				# 				EQUIPMENT_ID,
				# 				EQUIPMENT_RECORD_ID,
				# 				EQUIPMENT_DESCRIPTION,                                
				# 				SAQFEQ.FABLOCATION_ID,
				# 				SAQFEQ.FABLOCATION_NAME,
				# 				SAQFEQ.FABLOCATION_RECORD_ID,
				# 				SAQFEQ.WAFER_SIZE,
				# 				PBG,
				# 				SAQFEQ.SALESORG_ID,
				# 				SAQFEQ.SALESORG_NAME,
				# 				SAQFEQ.SALESORG_RECORD_ID,
				# 				SERIAL_NUMBER,
				# 				SAQFEQ.QUOTE_RECORD_ID,
				# 				SAQFEQ.QUOTE_ID,
				# 				SAQFEQ.QUOTE_NAME,
				# 				'{RelocationEqType}' AS RELOCATION_EQUIPMENT_TYPE,
				# 				'{TreeParentParam}' as SERVICE_ID,
				# 				'{TreeSuperParentParam}' as SERVICE_TYPE,
				# 				SAQTSV.SERVICE_DESCRIPTION as SERVICE_DESCRIPTION,
				# 				SAQTSV.SERVICE_RECORD_ID as SERVICE_RECORD_ID,
				# 				SAQFEQ.EQUIPMENT_STATUS,
				# 				SAQFEQ.EQUIPMENTCATEGORY_ID,
				# 				SAQFEQ.EQUIPMENTCATEGORY_DESCRIPTION,
				# 				SAQFEQ.EQUIPMENTCATEGORY_RECORD_ID,
				# 				SAQFEQ.PLATFORM,
				# 				SAQFEQ.GREENBOOK,
				# 				SAQFEQ.GREENBOOK_RECORD_ID,
				# 				SAQFEQ.MNT_PLANT_RECORD_ID,
				# 				SAQFEQ.MNT_PLANT_NAME,
				# 				SAQFEQ.MNT_PLANT_ID,
				# 				SAQFEQ.WARRANTY_START_DATE,
				# 				SAQFEQ.WARRANTY_END_DATE,
				# 				SAQFEQ.CUSTOMER_TOOL_ID,
				# 				SAQTSV.PAR_SERVICE_DESCRIPTION,
				# 				SAQTSV.PAR_SERVICE_ID,
				# 				SAQTSV.PAR_SERVICE_RECORD_ID,
				# 				'{UserName}' AS CPQTABLEENTRYADDEDBY,
				# 				GETDATE() as CPQTABLEENTRYDATEADDED,
				# 				{UserId} as CpqTableEntryModifiedBy,
				# 				GETDATE() as CpqTableEntryDateModified
				# 				FROM SAQFEQ (NOLOCK) JOIN SAQTSV (NOLOCK) ON
				# 				SAQFEQ.QUOTE_ID = SAQTSV.QUOTE_ID AND
				# 				SAQTSV.SERVICE_ID = '{TreeParentParam}' AND
				# 				SAQTSV.SERVICE_TYPE = '{TreeSuperParentParam}'
				# 				JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQFEQ.QUOTE_RECORD_ID
				# 				JOIN SYSPBT (NOLOCK) ON SYSPBT.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SYSPBT.BATCH_RECORD_ID = SAQFEQ.EQUIPMENT_RECORD_ID
				# 				WHERE 
				# 				SAQFEQ.QUOTE_RECORD_ID = '{QuoteRecordId}'
				# 				AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}'                        
				# 		""".format(
				# 				TreeParam = self.tree_param,
				# 				TreeSuperParentParam =self.tree_parent_level_1,
				# 				TreeParentParam=self.tree_parent_level_0,
				# 				QuoteRecordId=self.contract_quote_record_id,
				# 				BatchGroupRecordId=kwargs.get('batch_group_record_id'),
				# 				UserName=self.user_name,
				# 				UserId=self.user_id,
				# 				RelocationEqType=self.tree_param
				# 			)
				# )
				self._process_query(
				"""
					INSERT SAQSCO (
						QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,
						EQUIPMENT_ID,
						EQUIPMENT_RECORD_ID,
						EQUIPMENT_DESCRIPTION,                            
						SNDFBL_ID,
						SNDFBL_NAME,
						SNDFBL_RECORD_ID,
						WAFER_SIZE,
						SALESORG_ID,
						SALESORG_NAME,
						SALESORG_RECORD_ID,
						SERIAL_NO,
						QUOTE_RECORD_ID,
						QUOTE_ID,
						QUOTE_NAME,
						ACCOUNT_ID,
						ACCOUNT_NAME,
						ACCOUNT_RECORD_ID,
						QTEREV_ID,
						QTEREV_RECORD_ID,
						RELOCATION_EQUIPMENT_TYPE,
						SERVICE_ID,
						SERVICE_TYPE,
						SERVICE_DESCRIPTION,
						SERVICE_RECORD_ID,
						EQUIPMENT_STATUS,
						EQUIPMENTCATEGORY_ID,
						EQUIPMENTCATEGORY_DESCRIPTION,
						EQUIPMENTCATEGORY_RECORD_ID,
						PLATFORM,
						GREENBOOK,
						GREENBOOK_RECORD_ID,
						MNT_PLANT_RECORD_ID,
						MNT_PLANT_NAME,
						MNT_PLANT_ID,
						WARRANTY_START_DATE,
						WARRANTY_END_DATE,
						CONTRACT_VALID_FROM,
						CONTRACT_VALID_TO,
						CUSTOMER_TOOL_ID,
						PAR_SERVICE_DESCRIPTION,
						PAR_SERVICE_ID,
						PAR_SERVICE_RECORD_ID,
						TECHNOLOGY,
						CPQTABLEENTRYADDEDBY,
						CPQTABLEENTRYDATEADDED,
						CpqTableEntryModifiedBy,
						CpqTableEntryDateModified,
						FABLOCATION_ID,
						FABLOCATION_NAME,
						FABLOCATION_RECORD_ID,
						INCLUDED
						) SELECT
							CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,
							EQUIPMENT_ID,
							EQUIPMENT_RECORD_ID,
							EQUIPMENT_DESCRIPTION,                                
							SAQFEQ.FABLOCATION_ID,
							SAQFEQ.FABLOCATION_NAME,
							SAQFEQ.FABLOCATION_RECORD_ID,
							SAQFEQ.WAFER_SIZE,
							SAQFEQ.SALESORG_ID,
							SAQFEQ.SALESORG_NAME,
							SAQFEQ.SALESORG_RECORD_ID,
							SERIAL_NUMBER,
							SAQFEQ.QUOTE_RECORD_ID,
							SAQFEQ.QUOTE_ID,
							SAQFEQ.QUOTE_NAME,
							'{account_id}' as ACCOUNT_ID,
							'{account_name}' as ACCOUNT_NAME,
							'{account_record_id}' as ACCOUNT_RECORD_ID,
							SAQFEQ.QTEREV_ID,
							SAQFEQ.QTEREV_RECORD_ID,
							'{RelocationEqType}' AS RELOCATION_EQUIPMENT_TYPE,
							'{TreeParam}' as SERVICE_ID,
							'{TreeParentParam}' as SERVICE_TYPE,
							SAQTSV.SERVICE_DESCRIPTION as SERVICE_DESCRIPTION,
							SAQTSV.SERVICE_RECORD_ID as SERVICE_RECORD_ID,
							SAQFEQ.EQUIPMENT_STATUS,
							SAQFEQ.EQUIPMENTCATEGORY_ID,
							SAQFEQ.EQUIPMENTCATEGORY_DESCRIPTION,
							SAQFEQ.EQUIPMENTCATEGORY_RECORD_ID,
							SAQFEQ.PLATFORM,
							SAQFEQ.GREENBOOK,
							SAQFEQ.GREENBOOK_RECORD_ID,
							SAQFEQ.MNT_PLANT_RECORD_ID,
							SAQFEQ.MNT_PLANT_NAME,
							SAQFEQ.MNT_PLANT_ID,
							SAQFEQ.WARRANTY_START_DATE,
							SAQFEQ.WARRANTY_END_DATE,
							SAQTMT.CONTRACT_VALID_FROM,
							SAQTMT.CONTRACT_VALID_TO,
							SAQFEQ.CUSTOMER_TOOL_ID,
							SAQTSV.PAR_SERVICE_DESCRIPTION,
							SAQTSV.PAR_SERVICE_ID,
							SAQTSV.PAR_SERVICE_RECORD_ID,
							SAQFEQ.TECHNOLOGY,
							'{UserName}' AS CPQTABLEENTRYADDEDBY,
							GETDATE() as CPQTABLEENTRYDATEADDED,
							{UserId} as CpqTableEntryModifiedBy,
							GETDATE() as CpqTableEntryDateModified,
							'' AS FABLOCATION_ID,
							'' AS FABLOCATION_NAME,
							'' AS FABLOCATION_RECORD_ID,
							'TOOL' as INCLUDED
							FROM 
							SYSPBT (NOLOCK)
							JOIN SAQFEQ (NOLOCK) ON SAQFEQ.EQUIPMENT_RECORD_ID = SYSPBT.BATCH_RECORD_ID AND SAQFEQ.QUOTE_RECORD_ID = SYSPBT.QUOTE_RECORD_ID AND SAQFEQ.QTEREV_RECORD_ID = SYSPBT.QTEREV_RECORD_ID
							JOIN SAQTSV (NOLOCK) ON	SAQTSV.QUOTE_RECORD_ID = SAQFEQ.QUOTE_RECORD_ID AND SAQTSV.QTEREV_RECORD_ID = SAQFEQ.QTEREV_RECORD_ID AND SAQTSV.SERVICE_ID = '{TreeParam}' AND
													SAQTSV.SERVICE_TYPE = '{TreeParentParam}'
							JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQFEQ.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = SAQFEQ.QTEREV_RECORD_ID	
							WHERE 
							SYSPBT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND  SYSPBT.QTEREV_RECORD_ID = '{RevisionRecordId}'
							AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}' AND SAQFEQ.RELOCATION_EQUIPMENT_TYPE = 'SENDING EQUIPMENT'                          
					""".format(
							TreeParam=self.tree_param if (self.tree_parent_level_0 == 'Comprehensive Services' or self.tree_parent_level_0 == 'Complementary Products') and self.sale_type != 'TOOL RELOCATION' else self.tree_parent_level_0,
							TreeParentParam=self.tree_parent_level_0 if (self.tree_parent_level_0 == 'Comprehensive Services' or self.tree_parent_level_0 == 'Complementary Products') and self.sale_type != 'TOOL RELOCATION' else self.tree_parent_level_1,
							QuoteRecordId=self.contract_quote_record_id,
							RevisionRecordId=self.quote_revision_record_id,
							BatchGroupRecordId=kwargs.get('batch_group_record_id'),
							UserName=self.user_name,
							UserId=self.user_id,
							account_id=self.account_id,
							account_name=self.account_name,
							account_record_id=self.account_record_id,
							RelocationEqType='Receiving Equipment' 
						)
				)
		# elif self.tree_param == "Sending Equipment":
		# 	Trace.Write("Added for sending equip insert issue "+str(self.tree_parent_level_0))
		# 	self._process_query(
		# 		"""
		# 			INSERT SAQSCO (
		# 				QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,
		# 				EQUIPMENT_ID,
		# 				EQUIPMENT_RECORD_ID,
		# 				EQUIPMENT_DESCRIPTION,
		# 				FABLOCATION_ID,
		# 				FABLOCATION_NAME,
		# 				FABLOCATION_RECORD_ID,
		# 				WAFER_SIZE,
		# 				BUSINESSUNIT_ID,
		# 				SALESORG_ID,
		# 				SALESORG_NAME,
		# 				SALESORG_RECORD_ID,
		# 				SERIAL_NO,
		# 				QUOTE_RECORD_ID,
		# 				QUOTE_ID,
		# 				QUOTE_NAME,
		# 				RELOCATION_EQUIPMENT_TYPE,
		# 				SERVICE_ID,
		# 				SERVICE_TYPE,
		# 				SERVICE_DESCRIPTION,
		# 				SERVICE_RECORD_ID,
		# 				EQUIPMENT_STATUS,
		# 				EQUIPMENTCATEGORY_ID,
		# 				EQUIPMENTCATEGORY_DESCRIPTION,
		# 				EQUIPMENTCATEGORY_RECORD_ID,
		# 				PLATFORM,
		# 				GREENBOOK,
		# 				GREENBOOK_RECORD_ID,
		# 				MNT_PLANT_RECORD_ID,
		# 				MNT_PLANT_NAME,
		# 				MNT_PLANT_ID,
		# 				WARRANTY_START_DATE,
		# 				WARRANTY_END_DATE,
		# 				CUSTOMER_TOOL_ID,
		# 				PAR_SERVICE_DESCRIPTION,
		# 				PAR_SERVICE_ID,
		# 				PAR_SERVICE_RECORD_ID,
		# 				CPQTABLEENTRYADDEDBY,
		# 				CPQTABLEENTRYDATEADDED,
		# 				CpqTableEntryModifiedBy,
		# 				CpqTableEntryDateModified
		# 				) SELECT
		# 					CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,
		# 					EQUIPMENT_ID,
		# 					EQUIPMENT_RECORD_ID,
		# 					EQUIPMENT_DESCRIPTION,                                
		# 					SAQFEQ.FABLOCATION_ID,
		# 					SAQFEQ.FABLOCATION_NAME,
		# 					SAQFEQ.FABLOCATION_RECORD_ID,
		# 					SAQFEQ.WAFER_SIZE,
		# 					PBG,
		# 					SAQFEQ.SALESORG_ID,
		# 					SAQFEQ.SALESORG_NAME,
		# 					SAQFEQ.SALESORG_RECORD_ID,
		# 					SERIAL_NUMBER,
		# 					SAQFEQ.QUOTE_RECORD_ID,
		# 					SAQFEQ.QUOTE_ID,
		# 					SAQFEQ.QUOTE_NAME,
		# 					'{RelocationEqType}' AS RELOCATION_EQUIPMENT_TYPE,
		# 					'{TreeParentParam}' as SERVICE_ID,
		# 					'{TreeSuperParentParam}' as SERVICE_TYPE,
		# 					SAQTSV.SERVICE_DESCRIPTION as SERVICE_DESCRIPTION,
		# 					SAQTSV.SERVICE_RECORD_ID as SERVICE_RECORD_ID,
		# 					SAQFEQ.EQUIPMENT_STATUS,
		# 					SAQFEQ.EQUIPMENTCATEGORY_ID,
		# 					SAQFEQ.EQUIPMENTCATEGORY_DESCRIPTION,
		# 					SAQFEQ.EQUIPMENTCATEGORY_RECORD_ID,
		# 					SAQFEQ.PLATFORM,
		# 					SAQFEQ.GREENBOOK,
		# 					SAQFEQ.GREENBOOK_RECORD_ID,
		# 					SAQFEQ.MNT_PLANT_RECORD_ID,
		# 					SAQFEQ.MNT_PLANT_NAME,
		# 					SAQFEQ.MNT_PLANT_ID,
		# 					SAQFEQ.WARRANTY_START_DATE,
		# 					SAQFEQ.WARRANTY_END_DATE,
		# 					SAQFEQ.CUSTOMER_TOOL_ID,
		# 					SAQTSV.PAR_SERVICE_DESCRIPTION,
		# 					SAQTSV.PAR_SERVICE_ID,
		# 					SAQTSV.PAR_SERVICE_RECORD_ID,
		# 					'{UserName}' AS CPQTABLEENTRYADDEDBY,
		# 					GETDATE() as CPQTABLEENTRYDATEADDED,
		# 					{UserId} as CpqTableEntryModifiedBy,
		# 					GETDATE() as CpqTableEntryDateModified
		# 					FROM SAQFEQ (NOLOCK) JOIN SAQTSV (NOLOCK) ON
		# 					SAQFEQ.QUOTE_ID = SAQTSV.QUOTE_ID AND
		# 					SAQTSV.SERVICE_ID = '{TreeParentParam}' AND
		# 					SAQTSV.SERVICE_TYPE = '{TreeSuperParentParam}'
		# 					JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQFEQ.QUOTE_RECORD_ID
		# 					JOIN SYSPBT (NOLOCK) ON SYSPBT.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SYSPBT.BATCH_RECORD_ID = SAQFEQ.EQUIPMENT_RECORD_ID
		# 					WHERE 
		# 					SAQFEQ.QUOTE_RECORD_ID = '{QuoteRecordId}'
		# 					AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}'                        
		# 			""".format(
		# 					TreeParam = self.tree_param,
		# 					TreeSuperParentParam =self.tree_parent_level_1,
		# 					TreeParentParam=self.tree_parent_level_0,
		# 					QuoteRecordId=self.contract_quote_record_id,
		# 					BatchGroupRecordId=kwargs.get('batch_group_record_id'),
		# 					UserName=self.user_name,
		# 					UserId=self.user_id,
		# 					RelocationEqType=self.tree_param
		# 				)
		# 	)
		else:
			#Trace.Write('3436---'+str(self.tree_param))
			self._process_query(
				"""
					INSERT SAQSCO (
						QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,
						EQUIPMENT_ID,
						EQUIPMENT_RECORD_ID,
						EQUIPMENT_DESCRIPTION,
						FABLOCATION_ID,
						FABLOCATION_NAME,
						FABLOCATION_RECORD_ID,
						WAFER_SIZE,
						SALESORG_ID,
						SALESORG_NAME,
						SALESORG_RECORD_ID,
						SERIAL_NO,
						QUOTE_RECORD_ID,
						QUOTE_ID,
						QUOTE_NAME,
						ACCOUNT_ID,
						ACCOUNT_NAME,
						ACCOUNT_RECORD_ID,
						QTEREV_ID,
						QTEREV_RECORD_ID,
						RELOCATION_EQUIPMENT_TYPE,
						SERVICE_ID,
						SERVICE_TYPE,
						SERVICE_DESCRIPTION,
						SERVICE_RECORD_ID,
						EQUIPMENT_STATUS,
						EQUIPMENTCATEGORY_ID,
						EQUIPMENTCATEGORY_DESCRIPTION,
						EQUIPMENTCATEGORY_RECORD_ID,
						PLATFORM,
						GREENBOOK,
						GREENBOOK_RECORD_ID,
						MNT_PLANT_RECORD_ID,
						MNT_PLANT_NAME,
						MNT_PLANT_ID,
						WARRANTY_START_DATE,
						WARRANTY_END_DATE,
						CUSTOMER_TOOL_ID,
						PAR_SERVICE_DESCRIPTION,
						PAR_SERVICE_ID,
						PAR_SERVICE_RECORD_ID,
						TECHNOLOGY,
						CONTRACT_VALID_FROM,
						CONTRACT_VALID_TO,
						CPQTABLEENTRYADDEDBY,
						CPQTABLEENTRYDATEADDED,
						CpqTableEntryModifiedBy,
						CpqTableEntryDateModified
						) SELECT
							CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,
							EQUIPMENT_ID,
							EQUIPMENT_RECORD_ID,
							EQUIPMENT_DESCRIPTION,                                
							SAQFEQ.FABLOCATION_ID,
							SAQFEQ.FABLOCATION_NAME,
							SAQFEQ.FABLOCATION_RECORD_ID,
							SAQFEQ.WAFER_SIZE,
							SAQFEQ.SALESORG_ID,
							SAQFEQ.SALESORG_NAME,
							SAQFEQ.SALESORG_RECORD_ID,
							SERIAL_NUMBER,
							SAQFEQ.QUOTE_RECORD_ID,
							SAQFEQ.QUOTE_ID,
							SAQFEQ.QUOTE_NAME,
							'{account_id}' as ACCOUNT_ID,
							'{account_name}' as ACCOUNT_NAME,
							'{account_record_id}' as ACCOUNT_RECORD_ID,
							SAQFEQ.QTEREV_ID,
							SAQFEQ.QTEREV_RECORD_ID,
							'{RelocationEqType}' AS RELOCATION_EQUIPMENT_TYPE,
							'{TreeParam}' as SERVICE_ID,
							'{TreeParentParam}' as SERVICE_TYPE,
							SAQTSV.SERVICE_DESCRIPTION as SERVICE_DESCRIPTION,
							SAQTSV.SERVICE_RECORD_ID as SERVICE_RECORD_ID,
							SAQFEQ.EQUIPMENT_STATUS,
							SAQFEQ.EQUIPMENTCATEGORY_ID,
							SAQFEQ.EQUIPMENTCATEGORY_DESCRIPTION,
							SAQFEQ.EQUIPMENTCATEGORY_RECORD_ID,
							SAQFEQ.PLATFORM,
							SAQFEQ.GREENBOOK,
							SAQFEQ.GREENBOOK_RECORD_ID,
							SAQFEQ.MNT_PLANT_RECORD_ID,
							SAQFEQ.MNT_PLANT_NAME,
							SAQFEQ.MNT_PLANT_ID,
							SAQFEQ.WARRANTY_START_DATE,
							SAQFEQ.WARRANTY_END_DATE,
							SAQFEQ.CUSTOMER_TOOL_ID,
							SAQTSV.PAR_SERVICE_DESCRIPTION,
							SAQTSV.PAR_SERVICE_ID,
							SAQTSV.PAR_SERVICE_RECORD_ID,
							SAQFEQ.TECHNOLOGY,
							SAQTMT.CONTRACT_VALID_FROM,
							SAQTMT.CONTRACT_VALID_TO,
							'{UserName}' AS CPQTABLEENTRYADDEDBY,
							GETDATE() as CPQTABLEENTRYDATEADDED,
							{UserId} as CpqTableEntryModifiedBy,
							GETDATE() as CpqTableEntryDateModified
							FROM SAQFEQ (NOLOCK) JOIN SAQTSV (NOLOCK) ON
							SAQFEQ.QUOTE_ID = SAQTSV.QUOTE_ID AND
							SAQTSV.SERVICE_ID = '{TreeParam}' AND
							SAQTSV.SERVICE_TYPE = '{TreeParentParam}'
							JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQFEQ.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = SAQFEQ.QTEREV_RECORD_ID AND SAQTSV.QUOTE_RECORD_ID=SAQFEQ.QUOTE_RECORD_ID AND SAQTSV.QTEREV_RECORD_ID = SAQFEQ.QTEREV_RECORD_ID AND SAQTSV.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID
							JOIN SYSPBT (NOLOCK) ON SYSPBT.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SYSPBT.BATCH_RECORD_ID = SAQFEQ.EQUIPMENT_RECORD_ID AND SYSPBT.QTEREV_RECORD_ID = SAQFEQ.QTEREV_RECORD_ID  AND SYSPBT.QTEREV_RECORD_ID=SAQTSV.QTEREV_RECORD_ID
							WHERE 
							SAQFEQ.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQFEQ.QTEREV_RECORD_ID = '{RevisionRecordId}'
							AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}'                        
					""".format(
							TreeParam=self.tree_param,
							TreeParentParam=self.tree_parent_level_0,
							QuoteRecordId=self.contract_quote_record_id,
							RevisionRecordId=self.quote_revision_record_id,
							BatchGroupRecordId=kwargs.get('batch_group_record_id'),
							UserName=self.user_name,
							UserId=self.user_id,
							account_id=self.account_id,
							account_name=self.account_name,
							account_record_id=self.account_record_id,
							RelocationEqType=self.tree_param if self.tree_parent_level_1 == 'Complementary Products' else ''
						)
			)
			if Quote.GetGlobal("KPI") == "YES" and self.tree_param == "Z0091":
				self._process_query(
				"""
					INSERT SAQSCO (
						QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,
						EQUIPMENT_ID,
						EQUIPMENT_RECORD_ID,
						EQUIPMENT_DESCRIPTION,
						FABLOCATION_ID,
						FABLOCATION_NAME,
						FABLOCATION_RECORD_ID,
						WAFER_SIZE,
						SALESORG_ID,
						SALESORG_NAME,
						SALESORG_RECORD_ID,
						SERIAL_NO,
						QUOTE_RECORD_ID,
						QUOTE_ID,
						QUOTE_NAME,
						ACCOUNT_ID,
						ACCOUNT_NAME,
						ACCOUNT_RECORD_ID,
						QTEREV_ID,
						QTEREV_RECORD_ID,
						RELOCATION_EQUIPMENT_TYPE,
						SERVICE_ID,
						SERVICE_TYPE,
						SERVICE_DESCRIPTION,
						SERVICE_RECORD_ID,
						EQUIPMENT_STATUS,
						EQUIPMENTCATEGORY_ID,
						EQUIPMENTCATEGORY_DESCRIPTION,
						EQUIPMENTCATEGORY_RECORD_ID,
						PLATFORM,
						GREENBOOK,
						GREENBOOK_RECORD_ID,
						MNT_PLANT_RECORD_ID,
						MNT_PLANT_NAME,
						MNT_PLANT_ID,
						WARRANTY_START_DATE,
						WARRANTY_END_DATE,
						CUSTOMER_TOOL_ID,
						PAR_SERVICE_DESCRIPTION,
						PAR_SERVICE_ID,
						PAR_SERVICE_RECORD_ID,
						TECHNOLOGY,
						CONTRACT_VALID_FROM,
						CONTRACT_VALID_TO,
						CPQTABLEENTRYADDEDBY,
						CPQTABLEENTRYDATEADDED,
						CpqTableEntryModifiedBy,
						CpqTableEntryDateModified
						) SELECT
							CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,
								SAQSCO.EQUIPMENT_ID,
								SAQSCO.EQUIPMENT_RECORD_ID,
								SAQSCO.EQUIPMENT_DESCRIPTION,                                
								SAQSCO.FABLOCATION_ID,
								SAQSCO.FABLOCATION_NAME,
								SAQSCO.FABLOCATION_RECORD_ID,
								SAQSCO.WAFER_SIZE,
								SAQSCO.SALESORG_ID,
								SAQSCO.SALESORG_NAME,
								SAQSCO.SALESORG_RECORD_ID,
								SAQSCO.SERIAL_NO,
								SAQSCO.QUOTE_RECORD_ID,
								SAQSCO.QUOTE_ID,
								SAQSCO.QUOTE_NAME,
								'{account_id}' as ACCOUNT_ID,
								'{account_name}' as ACCOUNT_NAME,
								'{account_record_id}' as ACCOUNT_RECORD_ID,
								SAQSCO.QTEREV_ID,
								SAQSCO.QTEREV_RECORD_ID,
								SAQSCO.RELOCATION_EQUIPMENT_TYPE,
								'{TreeParam}',
								'{TreeParentParam}',
								'{desc}',
								'{rec}',
								SAQSCO.EQUIPMENT_STATUS,
								SAQSCO.EQUIPMENTCATEGORY_ID,
								SAQSCO.EQUIPMENTCATEGORY_DESCRIPTION,
								SAQSCO.EQUIPMENTCATEGORY_RECORD_ID,
								SAQSCO.PLATFORM,
								SAQSCO.GREENBOOK,
								SAQSCO.GREENBOOK_RECORD_ID,
								SAQSCO.MNT_PLANT_RECORD_ID,
								SAQSCO.MNT_PLANT_NAME,
								SAQSCO.MNT_PLANT_ID,
								SAQSCO.WARRANTY_START_DATE,
								SAQSCO.WARRANTY_END_DATE,
								SAQSCO.CUSTOMER_TOOL_ID,
								SAQSCO.PAR_SERVICE_DESCRIPTION,
								SAQSCO.PAR_SERVICE_ID,
								SAQSCO.PAR_SERVICE_RECORD_ID,
								SAQSCO.TECHNOLOGY,
								SAQSCO.CONTRACT_VALID_FROM,
								SAQSCO.CONTRACT_VALID_TO,
								'{UserName}',
								GETDATE(),
								{UserId},
								GETDATE()
								FROM SAQSCO (NOLOCK) JOIN SYSPBT (NOLOCK) ON
								SYSPBT.BATCH_RECORD_ID = SAQSCO.EQUIPMENT_RECORD_ID AND
								SYSPBT.QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID AND SYSPBT.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID
								WHERE 
								SAQSCO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCO.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQSCO.EQUIPMENT_ID NOT IN (SELECT EQUIPMENT_ID FROM SAQSCO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID = 'Z0046')
														
							""".format(
								TreeParam="Z0046",
								TreeParentParam="Add-On Products",
								QuoteRecordId=self.contract_quote_record_id,
								RevisionRecordId=self.quote_revision_record_id,
								desc="COMP SA VARIABLE",
								rec="CA6BB39A-947F-401B-830B-9D8B8942303D",
								UserName=self.user_name,
								account_id=self.account_id,
								account_name=self.account_name,
								account_record_id=self.account_record_id,
								UserId=self.user_id
								
								
							)
							)
				#Quote.SetGlobal("KPI","NO")


			#4393 start
			getdate = Sql.GetFirst("select CONTRACT_VALID_FROM,CONTRACT_VALID_TO from SAQTMT where MASTER_TABLE_QUOTE_RECORD_ID = '"+str(self.contract_quote_record_id)+"'")
			get_warrent_dates= SqlHelper.GetList("select QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,WARRANTY_END_DATE_ALERT,WARRANTY_START_DATE,WARRANTY_END_DATE from SAQSCO where QUOTE_RECORD_ID = '"+str(self.contract_quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"' ")
			update_warranty_enddate_alert = ''
			for val in get_warrent_dates:
				if val.WARRANTY_END_DATE:
					WARRANTY_val = datetime.datetime.strptime(str(val.WARRANTY_END_DATE), "%Y-%m-%d")
					get_con_date = str(getdate.CONTRACT_VALID_FROM).split(" ")[0]
					get_con_date = datetime.datetime.strptime(str(get_con_date), "%m/%d/%Y")
					if WARRANTY_val > get_con_date:
						update_warranty_enddate_alert = "UPDATE SAQSCO SET WARRANTY_END_DATE_ALERT = 1 where QUOTE_RECORD_ID = '"+str(self.contract_quote_record_id)+"' and QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"' and QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID = '"+str(val.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID)+"'"
					else:
						update_warranty_enddate_alert = "UPDATE SAQSCO SET WARRANTY_END_DATE_ALERT = 0 where QUOTE_RECORD_ID = '"+str(self.contract_quote_record_id)+"' and  QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"' and QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID = '"+str(val.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID)+"'"
					Sql.RunQuery(update_warranty_enddate_alert)
				else:
					update_warranty_enddate_alert = "UPDATE SAQSCO SET WARRANTY_END_DATE_ALERT = 0 where QUOTE_RECORD_ID = '"+str(self.contract_quote_record_id)+"' and QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"' and QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID = '"+str(val.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID)+"'"
					Sql.RunQuery(update_warranty_enddate_alert)
				#4393 end
				# if val.WARRANTY_START_DATE:
				# 	if val.WARRANTY_END_DATE >= get_contract_date.CONTRACT_VALID_FROM:
				# 		if val.WARRANTY_END_DATE:
				# 			if val.WARRANTY_END_DATE >= get_contract_date.CONTRACT_VALID_TO:
				# 				Trace.Write('QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID---'+str(val.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID))
				# 				update_warranty_enddate_alert = "UPDATE SAQSCO SET WARRANTY_END_DATE_ALERT = 1 where QUOTE_RECORD_ID = '"+str(self.contract_quote_record_id)+"' and QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID = '"+str(val.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID)+"'"
				# 		else:
				# 			update_warranty_enddate_alert = "UPDATE SAQSCO SET WARRANTY_END_DATE_ALERT = 0 where QUOTE_RECORD_ID = '"+str(self.contract_quote_record_id)+"' and QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID = '"+str(val.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID)+"'"
				# 			Trace.Write('no end date--')
				# 		Sql.RunQuery(update_warranty_enddate_alert)
		
	
	def _insert_quote_service_covered_assembly(self, **kwargs):		
		self._process_query(
			"""
				INSERT SAQSCA (
					QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID,
					CPQTABLEENTRYADDEDBY,
					CPQTABLEENTRYDATEADDED,
					CpqTableEntryModifiedBy,
					CpqTableEntryDateModified,
					ASSEMBLY_ID,
					ASSEMBLY_DESCRIPTION,
					ASSEMBLY_RECORD_ID,
					EQUIPMENT_ID,
					EQUIPMENT_DESCRIPTION,
					EQUIPMENT_RECORD_ID,
					SERIAL_NUMBER,
					GOT_CODE,
					EQUIPMENTCATEGORY_ID,
					EQUIPMENTCATEGORY_DESCRIPTION,
					EQUIPMENTCATEGORY_RECORD_ID,
					ASSEMBLY_STATUS,
					WARRANTY_START_DATE,
					WARRANTY_END_DATE,
					EQUIPMENTTYPE_ID,
					EQUIPMENTTYPE_DESCRIPTION,
					EQUIPMENTTYPE_RECORD_ID,
					QUOTE_ID,
					QUOTE_NAME,
					QUOTE_RECORD_ID,
					QTEREV_ID,
					QTEREV_RECORD_ID,
					SERVICE_ID,
					SERVICE_DESCRIPTION,
					SERVICE_RECORD_ID,
					FABLOCATION_ID,
					FABLOCATION_RECORD_ID,
					FABLOCATION_NAME,
					SALESORG_ID,
					SALESORG_NAME,
					SALESORG_RECORD_ID,
					MNT_PLANT_ID,
					MNT_PLANT_RECORD_ID,
					GREENBOOK,
					GREENBOOK_RECORD_ID,
					PAR_SERVICE_DESCRIPTION,
					PAR_SERVICE_ID,
					PAR_SERVICE_RECORD_ID,
					INCLUDED
					) SELECT
					CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID,
					'{UserName}' AS CPQTABLEENTRYADDEDBY,
					GETDATE() as CPQTABLEENTRYDATEADDED,
					{UserId} as CpqTableEntryModifiedBy,
					GETDATE() as CpqTableEntryDateModified,
					SAQFEA.ASSEMBLY_ID,
					SAQFEA.ASSEMBLY_DESCRIPTION,
					SAQFEA.ASSEMBLY_RECORD_ID,
					SAQFEA.EQUIPMENT_ID,
					SAQFEA.EQUIPMENT_DESCRIPTION,
					SAQFEA.EQUIPMENT_RECORD_ID,
					SAQFEA.SERIAL_NUMBER,
					SAQFEA.GOT_CODE,
					SAQFEA.EQUIPMENTCATEGORY_ID,
					SAQFEA.EQUIPMENTCATEGORY_DESCRIPTION,
					SAQFEA.EQUIPMENTCATEGORY_RECORD_ID,
					SAQFEA.ASSEMBLY_STATUS,
					SAQFEA.WARRANTY_START_DATE,
					SAQFEA.WARRANTY_END_DATE,
					SAQFEA.EQUIPMENTTYPE_ID,
					SAQFEA.EQUIPMENTTYPE_DESCRIPTION,
					SAQFEA.EQUIPMENTTYPE_RECORD_ID,
					SAQFEA.QUOTE_ID,
					SAQFEA.QUOTE_NAME,
					SAQFEA.QUOTE_RECORD_ID,
					SAQFEA.QTEREV_ID,
					SAQFEA.QTEREV_RECORD_ID,
					'{TreeParam}' as SERVICE_ID,
					SAQTSV.SERVICE_DESCRIPTION as SERVICE_DESCRIPTION,
					SAQTSV.SERVICE_RECORD_ID as SERVICE_RECORD_ID,
					SAQFEA.FABLOCATION_ID,
					SAQFEA.FABLOCATION_RECORD_ID,
					SAQFEA.FABLOCATION_NAME,
					SAQFEA.SALESORG_ID,
					SAQFEA.SALESORG_NAME,
					SAQFEA.SALESORG_RECORD_ID,
					SAQFEA.MNT_PLANT_ID,
					SAQFEA.MNT_PLANT_RECORD_ID,
					SAQSCO.GREENBOOK,
					SAQSCO.GREENBOOK_RECORD_ID,
					SAQTSV.PAR_SERVICE_DESCRIPTION,
					SAQTSV.PAR_SERVICE_ID,
					SAQTSV.PAR_SERVICE_RECORD_ID,
					{included} as INCLUDED 
					FROM SYSPBT (NOLOCK)
					JOIN (select SAQFEA.* from SAQFEA(nolock) join SYSPBT (nolock) on SAQFEA.QUOTE_RECORD_ID = SYSPBT.QUOTE_RECORD_ID and SAQFEA.QTEREV_RECORD_ID = SYSPBT.QTEREV_RECORD_ID and SAQFEA.EQUIPMENT_RECORD_ID = SYSPBT.BATCH_RECORD_ID where  SAQFEA.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQFEA.QTEREV_RECORD_ID = '{RevisionRecordId}' ) SAQFEA ON SAQFEA.QUOTE_RECORD_ID = SYSPBT.QUOTE_RECORD_ID AND SAQFEA.EQUIPMENT_RECORD_ID = SYSPBT.BATCH_RECORD_ID AND SAQFEA.QTEREV_RECORD_ID = SYSPBT.QTEREV_RECORD_ID
					JOIN SAQSCO (NOLOCK) ON SAQFEA.QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID AND SAQFEA.EQUIPMENT_ID = SAQSCO.EQUIPMENT_ID AND SAQFEA.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID
					JOIN SAQTSV (NOLOCK) ON SAQFEA.QUOTE_RECORD_ID = SAQTSV.QUOTE_RECORD_ID  AND SAQFEA.QTEREV_RECORD_ID = SAQTSV.QTEREV_RECORD_ID
					WHERE SYSPBT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}' AND SYSPBT.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQTSV.SERVICE_ID = '{TreeParam}' AND SAQTSV.SERVICE_TYPE = '{TreeParentParam}'
				""".format(
				UserId=self.user_id,
				UserName=self.user_name,
				TreeParam=self.tree_param if (self.tree_parent_level_0 == 'Comprehensive Services' or self.tree_parent_level_0 == 'Complementary Products') and self.sale_type != 'TOOL RELOCATION' else self.tree_parent_level_0,
				TreeParentParam=self.tree_parent_level_1 if self.tree_param  == 'Sending Equipment' else self.tree_parent_level_0,
				QuoteRecordId=self.contract_quote_record_id,
				RevisionRecordId=self.quote_revision_record_id,
				BatchGroupRecordId=kwargs.get('batch_group_record_id'),
				included = 1 if self.tree_param  == 'Sending Equipment' else "''"
			)
		)
		
		if self.sale_type == 'TOOL RELOCATION' and self.tree_param == "Sending Equipment":			
			self._process_query(
				"""
					INSERT SAQSSA (
						QUOTE_SERVICE_SENDING_FAB_EQUIP_ASS_ID,
						CPQTABLEENTRYADDEDBY,
						CPQTABLEENTRYDATEADDED,
						CpqTableEntryModifiedBy,
						CpqTableEntryDateModified,
						SND_ASSEMBLY_ID,
						SND_ASSEMBLY_DESCRIPTION,
						SND_ASSEMBLY_RECORD_ID,
						SND_EQUIPMENT_ID,
						SND_EQUIPMENT_DESCRIPTION,
						SND_EQUIPMENT_RECORD_ID,
						GOT_CODE,
						EQUIPMENTCATEGORY_ID,
						EQUIPMENTCATEGORY_DESCRIPTION,
						EQUIPMENTCATEGORY_RECORD_ID,
						ASSEMBLY_STATUS,
						EQUIPMENTTYPE_ID,
						EQUIPMENTTYPE_DESCRIPTION,
						EQUIPMENTTYPE_RECORD_ID,
						QUOTE_ID,
						QUOTE_NAME,
						QUOTE_RECORD_ID,
						QTEREV_ID,
						QTEREV_RECORD_ID,
						SERVICE_ID,
						SERVICE_DESCRIPTION,
						SERVICE_RECORD_ID,
						SNDFBL_ID,
						SNDFBL_NAME,
						SNDFBL_RECORD_ID,
						ADDUSR_RECORD_ID,
						QTESRV_RECORD_ID,
						SNDACC_ID,
						SNDACC_NAME,
						SNDACC_RECORD_ID,
						MODUSR_RECORD_ID,
						QTESNDEQP_RECORD_ID,
						GREENBOOK,
						GREENBOOK_RECORD_ID,
						INCLUDED
						) SELECT
						CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_SENDING_FAB_EQUIP_ASS_ID,
						'{UserName}' AS CPQTABLEENTRYADDEDBY,
						GETDATE() as CPQTABLEENTRYDATEADDED,
						{UserId} as CpqTableEntryModifiedBy,
						GETDATE() as CpqTableEntryDateModified,
						SAQFEA.ASSEMBLY_ID,
						SAQFEA.ASSEMBLY_DESCRIPTION,
						SAQFEA.ASSEMBLY_RECORD_ID,
						SAQFEA.EQUIPMENT_ID,
						SAQFEA.EQUIPMENT_DESCRIPTION,
						SAQFEA.EQUIPMENT_RECORD_ID,
						
						SAQFEA.GOT_CODE,
						SAQFEA.EQUIPMENTCATEGORY_ID,
						SAQFEA.EQUIPMENTCATEGORY_DESCRIPTION,
						SAQFEA.EQUIPMENTCATEGORY_RECORD_ID,
						SAQFEA.ASSEMBLY_STATUS,
						
						SAQFEA.EQUIPMENTTYPE_ID,
						SAQFEA.EQUIPMENTTYPE_DESCRIPTION,
						SAQFEA.EQUIPMENTTYPE_RECORD_ID,
						SAQFEA.QUOTE_ID,
						SAQFEA.QUOTE_NAME,
						SAQFEA.QUOTE_RECORD_ID,
						SAQFEA.QTEREV_ID,
						SAQFEA.QTEREV_RECORD_ID,
						SAQSSE.SERVICE_ID,
						SAQSSE.SERVICE_DESCRIPTION,
						SAQSSE.SERVICE_RECORD_ID,
						SAQSSE.SNDFBL_ID as FABLOCATION_ID,
						SAQSSE.SNDFBL_NAME as FABLOCATION_NAME,
						SAQSSE.SNDFBL_RECORD_ID as FABLOCATION_RECORD_ID,
						SAQFEA.ADDUSR_RECORD_ID,
						SAQSSE.QUOTE_SERVICE_SENDING_FAB_LOC_EQUIP_ID,
						SAQFEA.SRCACC_ID,
						SAQFEA.SRCACC_NAME,
						SAQFEA.SRCACC_RECORD_ID,
						'' as MODUSR_RECORD_ID,
						'' as QTESNDEQP_RECORD_ID,
						'' as GREENBOOK,
						'' as GREENBOOK_RECORD_ID,
						1
						FROM SAQFEA (NOLOCK)
						JOIN SAQSSE (NOLOCK) ON SAQFEA.QUOTE_RECORD_ID = SAQSSE.QUOTE_RECORD_ID AND SAQFEA.EQUIPMENT_ID = SAQSSE.SND_EQUIPMENT_ID AND SAQFEA.QTEREV_RECORD_ID = SAQSSE.QTEREV_RECORD_ID
						WHERE  SAQSSE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSSE.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQSSE.SERVICE_ID = '{TreeParentParam}'
					""".format(
					UserId=self.user_id,
					UserName=self.user_name,
					TreeParentParam=self.tree_parent_level_0,
					QuoteRecordId=self.contract_quote_record_id,
					RevisionRecordId=self.quote_revision_record_id
					
				)
			)
			# self._process_query(
			# 	"""
			# 		INSERT SAQSSA (
			# 			QUOTE_SERVICE_SENDING_FAB_EQUIP_ASS_ID,
			# 			CPQTABLEENTRYADDEDBY,
			# 			CPQTABLEENTRYDATEADDED,
			# 			CpqTableEntryModifiedBy,
			# 			CpqTableEntryDateModified,
			# 			SND_ASSEMBLY_ID,
			# 			SND_ASSEMBLY_DESCRIPTION,
			# 			SND_ASSEMBLY_RECORD_ID,
			# 			SND_EQUIPMENT_ID,
			# 			SND_EQUIPMENT_DESCRIPTION,
			# 			SND_EQUIPMENT_RECORD_ID,
			# 			GOT_CODE,
			# 			EQUIPMENTCATEGORY_ID,
			# 			EQUIPMENTCATEGORY_DESCRIPTION,
			# 			EQUIPMENTCATEGORY_RECORD_ID,
			# 			ASSEMBLY_STATUS,
			# 			EQUIPMENTTYPE_ID,
			# 			EQUIPMENTTYPE_DESCRIPTION,
			# 			EQUIPMENTTYPE_RECORD_ID,
			# 			QUOTE_ID,
			# 			QUOTE_NAME,
			# 			QUOTE_RECORD_ID,
			# 			SERVICE_ID,
			# 			SERVICE_DESCRIPTION,
			# 			SERVICE_RECORD_ID,
			# 			SNDFBL_ID,
			# 			SNDFBL_NAME,
			# 			SNDFBL_RECORD_ID,
			# 			ADDUSR_RECORD_ID,
			# 			QTESRV_RECORD_ID,
			# 			SNDACC_ID,
			# 			SNDACC_NAME,
			# 			SNDACC_RECORD_ID,
			# 			MODUSR_RECORD_ID,
			# 			QTESNDEQP_RECORD_ID,
			# 			GREENBOOK,
			# 			GREENBOOK_RECORD_ID
			# 			) SELECT
			# 			CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_SENDING_FAB_EQUIP_ASS_ID,
			# 			'{UserName}' AS CPQTABLEENTRYADDEDBY,
			# 			GETDATE() as CPQTABLEENTRYDATEADDED,
			# 			{UserId} as CpqTableEntryModifiedBy,
			# 			GETDATE() as CpqTableEntryDateModified,
			# 			SAQSCA.ASSEMBLY_ID,
			# 			SAQSCA.ASSEMBLY_DESCRIPTION,
			# 			SAQSCA.ASSEMBLY_RECORD_ID,
			# 			SAQSCA.EQUIPMENT_ID,
			# 			SAQSCA.EQUIPMENT_DESCRIPTION,
			# 			SAQSCA.EQUIPMENT_RECORD_ID,
			# 			SAQSCA.GOT_CODE,
			# 			SAQSCA.EQUIPMENTCATEGORY_ID,
			# 			SAQSCA.EQUIPMENTCATEGORY_DESCRIPTION,
			# 			SAQSCA.EQUIPMENTCATEGORY_RECORD_ID,
			# 			SAQSCA.ASSEMBLY_STATUS,
			# 			SAQSCA.EQUIPMENTTYPE_ID,
			# 			SAQSCA.EQUIPMENTTYPE_DESCRIPTION,
			# 			SAQSCA.EQUIPMENTTYPE_RECORD_ID,
			# 			SAQSCA.QUOTE_ID,
			# 			SAQSCA.QUOTE_NAME,
			# 			SAQSCA.QUOTE_RECORD_ID,
			# 			SAQSCA.SERVICE_ID,
			# 			SAQSCA.SERVICE_DESCRIPTION,
			# 			SAQSCA.SERVICE_RECORD_ID,
			# 			SAQSCA.FABLOCATION_ID,
			# 			SAQSCA.FABLOCATION_NAME,
			# 			SAQSCA.FABLOCATION_RECORD_ID,
			# 			SAQSCA.ADDUSR_RECORD_ID,
			# 			SAQSCO.QTESRV_RECORD_ID,
			# 			SAQSCO.SNDACC_ID,
			# 			SAQSCO.SNDACC_NAME,
			# 			SAQSCO.SNDACC_RECORD_ID,
			# 			'' as MODUSR_RECORD_ID,
			# 			'' as QTESNDEQP_RECORD_ID,
			# 			SAQSCA.GREENBOOK,
			# 			SAQSCA.GREENBOOK_RECORD_ID
			# 			FROM SYSPBT (NOLOCK)
			# 			JOIN (select SAQSCA.* from SAQSCA(nolock) join SYSPBT (nolock) on SAQSCA.QUOTE_RECORD_ID = SYSPBT.QUOTE_RECORD_ID and SAQSCA.EQUIPMENT_RECORD_ID = SYSPBT.BATCH_RECORD_ID where  SAQSCA.QUOTE_RECORD_ID = '{QuoteRecordId}' ) SAQSCA ON SAQSCA.QUOTE_RECORD_ID = SYSPBT.QUOTE_RECORD_ID AND SAQSCA.EQUIPMENT_RECORD_ID = SYSPBT.BATCH_RECORD_ID
			# 			JOIN SAQSCO (NOLOCK) ON SAQSCA.QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID AND SAQSCA.EQUIPMENT_ID = SAQSCO.EQUIPMENT_ID
			# 			WHERE SAQSCO.RELOCATION_EQUIPMENT_TYPE ='Receiving Equipment' AND SYSPBT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}' AND SAQSCA.SERVICE_ID = '{TreeParam}' AND SAQSCO.SERVICE_TYPE = '{TreeParentParam}'
			# 		""".format(
			# 		UserId=self.user_id,
			# 		UserName=self.user_name,
			# 		TreeParam=self.tree_param if (self.tree_parent_level_0 == 'Comprehensive Services' or self.tree_parent_level_0 == 'Complementary Products') and self.sale_type != 'TOOL RELOCATION' else self.tree_parent_level_0,
			# 		TreeParentParam=self.tree_parent_level_0 if self.tree_parent_level_0 == 'Comprehensive Services' else self.tree_parent_level_1,
			# 		QuoteRecordId=self.contract_quote_record_id,
			# 		BatchGroupRecordId=kwargs.get('batch_group_record_id')
			# 	)
			# )
			# self._process_query(
			# 	"""
			# 		INSERT SAQSSA (
			# 			QUOTE_SERVICE_SENDING_FAB_EQUIP_ASS_ID,
			# 			CPQTABLEENTRYADDEDBY,
			# 			CPQTABLEENTRYDATEADDED,
			# 			CpqTableEntryModifiedBy,
			# 			CpqTableEntryDateModified,
			# 			SND_ASSEMBLY_ID,
			# 			SND_ASSEMBLY_DESCRIPTION,
			# 			SND_ASSEMBLY_RECORD_ID,
			# 			SND_EQUIPMENT_ID,
			# 			SND_EQUIPMENT_DESCRIPTION,
			# 			SND_EQUIPMENT_RECORD_ID,
			# 			GOT_CODE,
			# 			EQUIPMENTCATEGORY_ID,
			# 			EQUIPMENTCATEGORY_DESCRIPTION,
			# 			EQUIPMENTCATEGORY_RECORD_ID,
			# 			ASSEMBLY_STATUS,
			# 			EQUIPMENTTYPE_ID,
			# 			EQUIPMENTTYPE_DESCRIPTION,
			# 			EQUIPMENTTYPE_RECORD_ID,
			# 			QUOTE_ID,
			# 			QUOTE_NAME,
			# 			QUOTE_RECORD_ID,
			# 			SERVICE_ID,
			# 			SERVICE_DESCRIPTION,
			# 			SERVICE_RECORD_ID,
			# 			SNDFBL_ID,
			# 			SNDFBL_NAME,
			# 			SNDFBL_RECORD_ID,
			# 			ADDUSR_RECORD_ID,
			# 			QTESRV_RECORD_ID,
			# 			SNDACC_ID,
			# 			SNDACC_NAME,
			# 			SNDACC_RECORD_ID,
			# 			MODUSR_RECORD_ID,
			# 			QTESNDEQP_RECORD_ID,
			# 			GREENBOOK,
			# 			GREENBOOK_RECORD_ID
			# 			) SELECT
			# 			CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_SENDING_FAB_EQUIP_ASS_ID,
			# 			'{UserName}' AS CPQTABLEENTRYADDEDBY,
			# 			GETDATE() as CPQTABLEENTRYDATEADDED,
			# 			{UserId} as CpqTableEntryModifiedBy,
			# 			GETDATE() as CpqTableEntryDateModified,
			# 			SAQSCA.ASSEMBLY_ID,
			# 			SAQSCA.ASSEMBLY_DESCRIPTION,
			# 			SAQSCA.ASSEMBLY_RECORD_ID,
			# 			SAQSCA.EQUIPMENT_ID,
			# 			SAQSCA.EQUIPMENT_DESCRIPTION,
			# 			SAQSCA.EQUIPMENT_RECORD_ID,
			# 			SAQSCA.GOT_CODE,
			# 			SAQSCA.EQUIPMENTCATEGORY_ID,
			# 			SAQSCA.EQUIPMENTCATEGORY_DESCRIPTION,
			# 			SAQSCA.EQUIPMENTCATEGORY_RECORD_ID,
			# 			SAQSCA.ASSEMBLY_STATUS,
			# 			SAQSCA.EQUIPMENTTYPE_ID,
			# 			SAQSCA.EQUIPMENTTYPE_DESCRIPTION,
			# 			SAQSCA.EQUIPMENTTYPE_RECORD_ID,
			# 			SAQSCA.QUOTE_ID,
			# 			SAQSCA.QUOTE_NAME,
			# 			SAQSCA.QUOTE_RECORD_ID,
			# 			SAQSCA.SERVICE_ID,
			# 			SAQSCA.SERVICE_DESCRIPTION,
			# 			SAQSCA.SERVICE_RECORD_ID,
			# 			SAQSCA.FABLOCATION_ID,
			# 			SAQSCA.FABLOCATION_NAME,
			# 			SAQSCA.FABLOCATION_RECORD_ID,
			# 			SAQSCA.ADDUSR_RECORD_ID,
			# 			SAQSCO.QTESRV_RECORD_ID,
			# 			SAQSCO.SNDACC_ID,
			# 			SAQSCO.SNDACC_NAME,
			# 			SAQSCO.SNDACC_RECORD_ID,
			# 			'' as MODUSR_RECORD_ID,
			# 			'' as QTESNDEQP_RECORD_ID,
			# 			SAQSCA.GREENBOOK,
			# 			SAQSCA.GREENBOOK_RECORD_ID
			# 			FROM SAQSCA (NOLOCK)
			# 			JOIN SAQSCO (NOLOCK) ON SAQSCA.QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID AND SAQSCA.EQUIPMENT_ID = SAQSCO.EQUIPMENT_ID
			# 			WHERE SAQSCO.RELOCATION_EQUIPMENT_TYPE ='SENDING EQUIPMENT' AND SAQSCA.QUOTE_RECORD_ID = '{QuoteRecordId}'  AND SAQSCA.SERVICE_ID = '{TreeParam}' AND SAQSCO.SERVICE_TYPE = '{TreeParentParam}'
			# 		""".format(
			# 		UserId=self.user_id,
			# 		UserName=self.user_name,
			# 		TreeParam=self.tree_param if (self.tree_parent_level_0 == 'Comprehensive Services' or self.tree_parent_level_0 == 'Complementary Products') and self.sale_type != 'TOOL RELOCATION' else self.tree_parent_level_0,
			# 		TreeParentParam=self.tree_parent_level_0 if self.tree_parent_level_0 == 'Comprehensive Services' else self.tree_parent_level_1,
			# 		QuoteRecordId=self.contract_quote_record_id
					
			# 	)
			# )

	def _insert_quote_service_fab_location(self, **kwargs):
		if self.sale_type == "TOOL RELOCATION" and self.tree_param == "Sending Equipment":
			# self._process_query(
			# 	"""INSERT SAQSFB(
			# 		FABLOCATION_ID,
			# 		FABLOCATION_NAME,
			# 		FABLOCATION_RECORD_ID,
			# 		SERVICE_ID,
			# 		SERVICE_TYPE,
			# 		SERVICE_DESCRIPTION,
			# 		SERVICE_RECORD_ID,
			# 		FABLOCATION_STATUS,
			# 		QUOTE_ID,
			# 		QUOTE_NAME,
			# 		QUOTE_RECORD_ID,
			# 		MNT_PLANT_ID,
			# 		MNT_PLANT_NAME,
			# 		MNT_PLANT_RECORD_ID,
			# 		ADDRESS_1,
			# 		ADDRESS_2,
			# 		CITY,
			# 		COUNTRY,
			# 		COUNTRY_RECORD_ID,
			# 		SALESORG_ID,
			# 		SALESORG_NAME,
			# 		SALESORG_RECORD_ID,
			# 		PAR_SERVICE_DESCRIPTION,
			# 		PAR_SERVICE_ID,
			# 		PAR_SERVICE_RECORD_ID,
			# 		QUOTE_SERVICE_FAB_LOCATION_RECORD_ID,
			# 		CPQTABLEENTRYADDEDBY,
			# 		CPQTABLEENTRYDATEADDED,
			# 		CpqTableEntryModifiedBy,
			# 		CpqTableEntryDateModified
			# 		) SELECT FB.*,CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_FAB_LOCATION_RECORD_ID,
			# 		'{UserName}' AS CPQTABLEENTRYADDEDBY,
			# 		GETDATE() as CPQTABLEENTRYDATEADDED, {UserId} as CpqTableEntryModifiedBy,
			# 		GETDATE() as CpqTableEntryDateModified FROM (
			# 		SELECT DISTINCT
			# 		SAQSCO.SNDFBL_ID,
			# 		SAQSCO.SNDFBL_NAME,
			# 		SAQSCO.SNDFBL_RECORD_ID,
			# 		SAQSCO.SERVICE_ID,
			# 		SAQSCO.SERVICE_TYPE,
			# 		SAQSCO.SERVICE_DESCRIPTION,
			# 		SAQSCO.SERVICE_RECORD_ID,
			# 		MAFBLC.STATUS,
			# 		SAQSCO.QUOTE_ID,
			# 		SAQSCO.QUOTE_NAME,
			# 		SAQSCO.QUOTE_RECORD_ID,
			# 		SAQSCO.MNT_PLANT_ID,
			# 		SAQSCO.MNT_PLANT_NAME,
			# 		SAQSCO.MNT_PLANT_RECORD_ID,
			# 		MAFBLC.ADDRESS_1,
			# 		MAFBLC.ADDRESS_2,
			# 		MAFBLC.CITY,
			# 		MAFBLC.COUNTRY,
			# 		MAFBLC.COUNTRY_RECORD_ID,
			# 		SAQSCO.SALESORG_ID,
			# 		SAQSCO.SALESORG_NAME,
			# 		SAQSCO.SALESORG_RECORD_ID,
			# 		SAQSCO.PAR_SERVICE_DESCRIPTION,
			# 		SAQSCO.PAR_SERVICE_ID,
			# 		SAQSCO.PAR_SERVICE_RECORD_ID
			# 		FROM SAQSCO (NOLOCK)
			# 		JOIN MAFBLC (NOLOCK) ON SAQSCO.SNDFBL_ID = MAFBLC.FAB_LOCATION_ID 
			# 		JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID
			# 		JOIN SYSPBT (NOLOCK) ON SYSPBT.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SYSPBT.BATCH_RECORD_ID = SAQSCO.EQUIPMENT_RECORD_ID
			# 		WHERE SAQSCO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}' AND
			# 		SAQSCO.SERVICE_ID = '{TreeParam}' AND SAQSCO.SERVICE_TYPE = '{TreeParentParam}' AND NOT EXISTS(SELECT FABLOCATION_ID FROM SAQSFB WHERE SERVICE_ID = '{TreeParam}' AND QUOTE_RECORD_ID = '{QuoteRecordId}')
			# 		) FB""".format(
			# 						TreeParam=self.tree_param if (self.tree_parent_level_0 == 'Comprehensive Services' or self.tree_parent_level_0 == 'Complementary Products') and self.sale_type != 'TOOL RELOCATION' else self.tree_parent_level_0,
			# 						TreeParentParam=self.tree_parent_level_0 if (self.tree_parent_level_0 == 'Comprehensive Services' or self.tree_parent_level_0 == 'Complementary Products') and self.sale_type != 'TOOL RELOCATION' else self.tree_parent_level_1,
			# 						QuoteRecordId=self.contract_quote_record_id,
			# 						BatchGroupRecordId=kwargs.get('batch_group_record_id'),
			# 						UserId=self.user_id,
			# 						UserName=self.user_name,
			# 					)
			# 	)
			if self.tree_param == "Sending Equipment" and self.sale_type == "TOOL RELOCATION":
				self._process_query(
					"""INSERT SAQSSF(
						SNDFBL_ID,
						SNDFBL_NAME,
						SNDACC_ID,
						SNDACC_NAME,
						SNDACC_RECORD_ID,
						SNDFBL_RECORD_ID,
						SERVICE_ID,					
						SERVICE_DESCRIPTION,
						SERVICE_RECORD_ID,
						SNDFBL_STATUS,
						QUOTE_ID,
						QUOTE_NAME,
						QUOTE_RECORD_ID,
						QTEREV_ID,
						QTEREV_RECORD_ID,
						MNT_PLANT_ID,
						MNT_PLANT_NAME,
						MNT_PLANT_RECORD_ID,
						ADDRESS_1,
						ADDRESS_2,
						CITY,
						COUNTRY,
						COUNTRY_RECORD_ID,
						SALESORG_ID,
						SALESORG_NAME,
						SALESORG_RECORD_ID,					
						QUOTE_SERVICE_SENDING_FAB_LOC_ID,
						CPQTABLEENTRYADDEDBY,
						CPQTABLEENTRYDATEADDED,
						CpqTableEntryModifiedBy,
						CpqTableEntryDateModified
						) SELECT FB.*,CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_SENDING_FAB_LOC_ID,
						'{UserName}' AS CPQTABLEENTRYADDEDBY,
						GETDATE() as CPQTABLEENTRYDATEADDED, {UserId} as CpqTableEntryModifiedBy,
						GETDATE() as CpqTableEntryDateModified FROM (
						SELECT DISTINCT
						SAQSSE.SNDFBL_ID,
						SAQSSE.SNDFBL_NAME,
						SAQSSE.SNDACC_ID,
						SAQSSE.SNDACC_NAME,
						SAQSSE.SNDACC_RECORD_ID,
						SAQSSE.SNDFBL_RECORD_ID,
						SAQSSE.SERVICE_ID,					
						SAQSSE.SERVICE_DESCRIPTION,
						SAQSSE.SERVICE_RECORD_ID,
						MAFBLC.STATUS,
						SAQSSE.QUOTE_ID,
						SAQSSE.QUOTE_NAME,
						SAQSSE.QUOTE_RECORD_ID,
						SAQSSE.QTEREV_ID,
						SAQSSE.QTEREV_RECORD_ID,
						SAQSSE.MNT_PLANT_ID,
						SAQSSE.MNT_PLANT_NAME,
						SAQSSE.MNT_PLANT_RECORD_ID,
						MAFBLC.ADDRESS_1,
						MAFBLC.ADDRESS_2,
						MAFBLC.CITY,
						MAFBLC.COUNTRY,
						MAFBLC.COUNTRY_RECORD_ID,
						SAQSSE.SALESORG_ID,
						SAQSSE.SALESORG_NAME,
						SAQSSE.SALESORG_RECORD_ID					
						FROM SAQSSE (NOLOCK)
						JOIN MAFBLC (NOLOCK) ON SAQSSE.SNDFBL_ID = MAFBLC.FAB_LOCATION_ID 
						JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQSSE.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = SAQSSE.QTEREV_RECORD_ID
						JOIN SYSPBT (NOLOCK) ON SYSPBT.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SYSPBT.BATCH_RECORD_ID = SAQSSE.SND_EQUIPMENT_RECORD_ID AND SYSPBT.QTEREV_RECORD_ID = SAQSSE.QTEREV_RECORD_ID
						WHERE SAQSSE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSSE.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}' AND
						SAQSSE.SERVICE_ID = '{TreeParentParam}' AND SAQSSE.SNDFBL_ID NOT IN(SELECT SNDFBL_ID FROM SAQSSF (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID = '{TreeParentParam}')
						) FB""".format(
										TreeParam=self.tree_param if (self.tree_parent_level_1 == 'Complementary Products') and self.sale_type == 'TOOL RELOCATION' else self.tree_parent_level_1,
										TreeParentParam=self.tree_parent_level_0 if (self.tree_parent_level_1 == 'Complementary Products') and self.sale_type == 'TOOL RELOCATION' else self.tree_parent_level_1,
										TreeSuperParentParam = self.tree_parent_level_1,
										QuoteRecordId=self.contract_quote_record_id,
										RevisionRecordId=self.quote_revision_record_id,
										BatchGroupRecordId=kwargs.get('batch_group_record_id'),
										UserId=self.user_id,
										UserName=self.user_name,
									)
					)			
	
		else:
			self._process_query(
				"""INSERT SAQSFB(
					FABLOCATION_ID,
					FABLOCATION_NAME,
					FABLOCATION_RECORD_ID,
					SERVICE_ID,
					SERVICE_TYPE,
					SERVICE_DESCRIPTION,
					SERVICE_RECORD_ID,
					FABLOCATION_STATUS,
					QUOTE_ID,
					QUOTE_NAME,
					QUOTE_RECORD_ID,
					QTEREV_ID,
					QTEREV_RECORD_ID,
					MNT_PLANT_ID,
					MNT_PLANT_NAME,
					MNT_PLANT_RECORD_ID,
					ADDRESS_1,
					ADDRESS_2,
					CITY,
					COUNTRY,
					COUNTRY_RECORD_ID,
					SALESORG_ID,
					SALESORG_NAME,
					SALESORG_RECORD_ID,
					CONTRACT_VALID_FROM,
					CONTRACT_VALID_TO,
					PAR_SERVICE_DESCRIPTION,
					PAR_SERVICE_ID,
					PAR_SERVICE_RECORD_ID,
					QUOTE_SERVICE_FAB_LOCATION_RECORD_ID,
					CPQTABLEENTRYADDEDBY,
					CPQTABLEENTRYDATEADDED,
					CpqTableEntryModifiedBy,
					CpqTableEntryDateModified
					) SELECT FB.*,CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_FAB_LOCATION_RECORD_ID,
					'{UserName}' AS CPQTABLEENTRYADDEDBY,
					GETDATE() as CPQTABLEENTRYDATEADDED, {UserId} as CpqTableEntryModifiedBy,
					GETDATE() as CpqTableEntryDateModified FROM (
					SELECT DISTINCT
					SAQSCO.FABLOCATION_ID,
					SAQSCO.FABLOCATION_NAME,
					SAQSCO.FABLOCATION_RECORD_ID,
					SAQSCO.SERVICE_ID,
					SAQSCO.SERVICE_TYPE,
					SAQSCO.SERVICE_DESCRIPTION,
					SAQSCO.SERVICE_RECORD_ID,
					MAFBLC.STATUS,
					SAQSCO.QUOTE_ID,
					SAQSCO.QUOTE_NAME,
					SAQSCO.QUOTE_RECORD_ID,
					SAQSCO.QTEREV_ID,
					SAQSCO.QTEREV_RECORD_ID,
					SAQSCO.MNT_PLANT_ID,
					SAQSCO.MNT_PLANT_NAME,
					SAQSCO.MNT_PLANT_RECORD_ID,
					MAFBLC.ADDRESS_1,
					MAFBLC.ADDRESS_2,
					MAFBLC.CITY,
					MAFBLC.COUNTRY,
					MAFBLC.COUNTRY_RECORD_ID,
					SAQSCO.SALESORG_ID,
					SAQSCO.SALESORG_NAME,
					SAQSCO.SALESORG_RECORD_ID,
					SAQTMT.CONTRACT_VALID_FROM,
					SAQTMT.CONTRACT_VALID_TO,
					SAQSCO.PAR_SERVICE_DESCRIPTION,
					SAQSCO.PAR_SERVICE_ID,
					SAQSCO.PAR_SERVICE_RECORD_ID
					FROM SAQSCO (NOLOCK)
					JOIN MAFBLC (NOLOCK) ON SAQSCO.FABLOCATION_ID = MAFBLC.FAB_LOCATION_ID 
					JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID
					JOIN SYSPBT (NOLOCK) ON SYSPBT.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SYSPBT.BATCH_RECORD_ID = SAQSCO.EQUIPMENT_RECORD_ID AND SYSPBT.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID
					WHERE SAQSCO.QUOTE_RECORD_ID = '{QuoteRecordId}'  AND SAQSCO.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}' AND
					SAQSCO.SERVICE_ID = '{TreeParam}' AND SAQSCO.SERVICE_TYPE = '{TreeParentParam}' AND FABLOCATION_ID NOT IN (SELECT FABLOCATION_ID FROM SAQSFB WHERE SERVICE_ID = '{TreeParam}' AND QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}')
					) FB""".format(
									TreeParam=self.tree_param if (self.tree_parent_level_0 == 'Comprehensive Services' or self.tree_parent_level_0 == 'Complementary Products') and self.sale_type != 'TOOL RELOCATION' else self.tree_parent_level_0,
									TreeParentParam=self.tree_parent_level_0 if (self.tree_parent_level_0 == 'Comprehensive Services' or self.tree_parent_level_0 == 'Complementary Products') and self.sale_type != 'TOOL RELOCATION' else self.tree_parent_level_1,
									QuoteRecordId=self.contract_quote_record_id,
									RevisionRecordId=self.quote_revision_record_id,
									BatchGroupRecordId=kwargs.get('batch_group_record_id'),
									UserId=self.user_id,
									UserName=self.user_name,
								)
				)
		
	def _insert_quote_service_greenbook(self, **kwargs):
		if self.sale_type == "TOOL RELOCATION":
				self._process_query(
				"""
					INSERT SAQSGB (
						QUOTE_SERVICE_GREENBOOK_RECORD_ID,
						FABLOCATION_ID,
						GREENBOOK,
						GREENBOOK_RECORD_ID,
						QUOTE_ID,
						QUOTE_NAME,
						QUOTE_RECORD_ID,
						QTEREV_ID,
						QTEREV_RECORD_ID,
						SALESORG_ID,
						SALESORG_NAME,
						SALESORG_RECORD_ID,
						SERVICE_DESCRIPTION,
						SERVICE_ID,
						SERVICE_RECORD_ID,
						EQUIPMENT_QUANTITY,
						FABLOCATION_NAME,
						FABLOCATION_RECORD_ID,
						CONTRACT_VALID_FROM,
						CONTRACT_VALID_TO,
						UOM_ID,
						PAR_SERVICE_DESCRIPTION,
						PAR_SERVICE_ID,
						PAR_SERVICE_RECORD_ID,
						CPQTABLEENTRYADDEDBY,
						CPQTABLEENTRYDATEADDED,
						CpqTableEntryModifiedBy,
						CpqTableEntryDateModified
						) SELECT CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_GREENBOOK_RECORD_ID,A.* from (SELECT DISTINCT
							SAQSCO.SNDFBL_ID,
							SAQSCO.GREENBOOK,
							SAQSCO.GREENBOOK_RECORD_ID,
							SAQSCO.QUOTE_ID,
							SAQSCO.QUOTE_NAME,
							SAQSCO.QUOTE_RECORD_ID,
							SAQSCO.QTEREV_ID,
							SAQSCO.QTEREV_RECORD_ID,
							SAQSCO.SALESORG_ID,
							SAQSCO.SALESORG_NAME,
							SAQSCO.SALESORG_RECORD_ID,
							SAQSCO.SERVICE_DESCRIPTION,
							SAQSCO.SERVICE_ID,
							SAQSCO.SERVICE_RECORD_ID,
							SAQSCO.EQUIPMENT_QUANTITY,								
							SAQSCO.FABLOCATION_NAME,
							SAQSCO.FABLOCATION_RECORD_ID,
							SAQTMT.CONTRACT_VALID_FROM,
							SAQTMT.CONTRACT_VALID_TO,
							SAQTSV.UOM_ID,
							SAQTSV.PAR_SERVICE_DESCRIPTION,
							SAQTSV.PAR_SERVICE_ID,
							SAQTSV.PAR_SERVICE_RECORD_ID,
							'{UserName}' AS CPQTABLEENTRYADDEDBY,
							GETDATE() as CPQTABLEENTRYDATEADDED,
							{UserId} as CpqTableEntryModifiedBy,
							GETDATE() as CpqTableEntryDateModified
							FROM SAQSCO (NOLOCK) JOIN SAQTSV (NOLOCK) ON
							SAQSCO.QUOTE_ID = SAQTSV.QUOTE_ID AND
							SAQTSV.SERVICE_ID = '{TreeParam}' AND
							SAQTSV.SERVICE_TYPE = '{TreeParentParam}'
							JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID
							JOIN SYSPBT (NOLOCK) ON SYSPBT.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SYSPBT.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID
							WHERE 
							SAQSCO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCO.QTEREV_RECORD_ID = '{RevisionRecordId}'
							AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}')A LEFT JOIN SAQSGB (NOLOCK) AS M ON A.QUOTE_RECORD_ID = M.QUOTE_RECORD_ID AND M.SERVICE_ID = A.SERVICE_ID AND M.FABLOCATION_RECORD_ID =A.FABLOCATION_RECORD_ID AND M.GREENBOOK = A.GREENBOOK WHERE M.QUOTE_RECORD_ID is null                  
					""".format(
							TreeParam=self.tree_param if (self.tree_parent_level_0 == 'Comprehensive Services' or self.tree_parent_level_0 == 'Complementary Products') and self.sale_type == 'TOOL RELOCATION' else self.tree_parent_level_0,
							TreeParentParam=self.tree_parent_level_0 if (self.tree_parent_level_0 == 'Comprehensive Services' or self.tree_parent_level_0 == 'Complementary Products') and self.sale_type == 'TOOL RELOCATION' else self.tree_parent_level_1,
							QuoteRecordId=self.contract_quote_record_id,
							RevisionRecordId=self.quote_revision_record_id,
							BatchGroupRecordId=kwargs.get('batch_group_record_id'),
							UserName=self.user_name,
							UserId=self.user_id
						)
			)
		else:
			d1 = Sql.GetFirst(
				"""SELECT CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_GREENBOOK_RECORD_ID,A.* from (SELECT DISTINCT
							SAQSCO.FABLOCATION_ID,
							SAQSCO.GREENBOOK,
							SAQSCO.GREENBOOK_RECORD_ID,
							SAQSCO.QUOTE_ID,
							SAQSCO.QUOTE_NAME,
							SAQSCO.QUOTE_RECORD_ID,
							SAQSCO.QTEREV_ID,
							SAQSCO.QTEREV_RECORD_ID,
							SAQSCO.SALESORG_ID,
							SAQSCO.SALESORG_NAME,
							SAQSCO.SALESORG_RECORD_ID,
							SAQSCO.SERVICE_DESCRIPTION,
							SAQSCO.SERVICE_ID,
							SAQSCO.SERVICE_RECORD_ID,
							SAQSCO.EQUIPMENT_QUANTITY,								
							SAQSCO.FABLOCATION_NAME,
							SAQSCO.FABLOCATION_RECORD_ID,
							SAQTMT.CONTRACT_VALID_FROM,
       						SAQTMT.CONTRACT_VALID_TO,
							SAQTSV.PAR_SERVICE_DESCRIPTION,
							SAQTSV.PAR_SERVICE_ID,
							SAQTSV.PAR_SERVICE_RECORD_ID,
							'{UserName}' AS CPQTABLEENTRYADDEDBY,
							GETDATE() as CPQTABLEENTRYDATEADDED,
							{UserId} as CpqTableEntryModifiedBy,
							GETDATE() as CpqTableEntryDateModified
							FROM SAQSCO (NOLOCK) JOIN SAQTSV (NOLOCK) ON
							SAQSCO.QUOTE_ID = SAQTSV.QUOTE_ID AND
							SAQTSV.SERVICE_ID = '{TreeParam}' AND
							SAQTSV.SERVICE_TYPE = '{TreeParentParam}'
							JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID
							JOIN SYSPBT (NOLOCK) ON SYSPBT.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SYSPBT.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID
							WHERE 
							SAQSCO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCO.QTEREV_RECORD_ID = '{RevisionRecordId}'
							AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}')A LEFT JOIN SAQSGB (NOLOCK) AS M ON A.QUOTE_RECORD_ID = M.QUOTE_RECORD_ID AND M.SERVICE_ID = A.SERVICE_ID AND M.FABLOCATION_RECORD_ID =A.FABLOCATION_RECORD_ID AND M.GREENBOOK = A.GREENBOOK WHERE M.QUOTE_RECORD_ID is null                  
					""".format(
							TreeParam=self.tree_param if (self.tree_parent_level_0 == 'Comprehensive Services' or self.tree_parent_level_0 == 'Complementary Products') and self.sale_type != 'TOOL RELOCATION' else self.tree_parent_level_0,
							TreeParentParam=self.tree_parent_level_0 if (self.tree_parent_level_0 == 'Comprehensive Services' or self.tree_parent_level_0 == 'Complementary Products') and self.sale_type != 'TOOL RELOCATION' else self.tree_parent_level_1,
							QuoteRecordId=self.contract_quote_record_id,
							RevisionRecordId=self.quote_revision_record_id,
							BatchGroupRecordId=kwargs.get('batch_group_record_id'),
							UserName=self.user_name,
							UserId=self.user_id
						)
			)
			if d1:
				Trace.Write(str(d1.QTEREV_ID)+'==================>>>>>nnnn '+str(d1.GREENBOOK))
			self._process_query(
				"""
					INSERT SAQSGB (
						QUOTE_SERVICE_GREENBOOK_RECORD_ID,
						FABLOCATION_ID,
						GREENBOOK,
						GREENBOOK_RECORD_ID,
						QUOTE_ID,
						QUOTE_NAME,
						QUOTE_RECORD_ID,
						QTEREV_ID,
						QTEREV_RECORD_ID,
						SALESORG_ID,
						SALESORG_NAME,
						SALESORG_RECORD_ID,
						SERVICE_DESCRIPTION,
						SERVICE_ID,
						SERVICE_RECORD_ID,
						EQUIPMENT_QUANTITY,
						FABLOCATION_NAME,
						FABLOCATION_RECORD_ID,
						CONTRACT_VALID_FROM,
						CONTRACT_VALID_TO,
						PAR_SERVICE_DESCRIPTION,
						PAR_SERVICE_ID,
						PAR_SERVICE_RECORD_ID,
						CPQTABLEENTRYADDEDBY,
						CPQTABLEENTRYDATEADDED,
						CpqTableEntryModifiedBy,
						CpqTableEntryDateModified
						) SELECT CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_GREENBOOK_RECORD_ID,A.* from (SELECT DISTINCT
							SAQSCO.FABLOCATION_ID,
							SAQSCO.GREENBOOK,
							SAQSCO.GREENBOOK_RECORD_ID,
							SAQSCO.QUOTE_ID,
							SAQSCO.QUOTE_NAME,
							SAQSCO.QUOTE_RECORD_ID,
							SAQSCO.QTEREV_ID,
							SAQSCO.QTEREV_RECORD_ID,
							SAQSCO.SALESORG_ID,
							SAQSCO.SALESORG_NAME,
							SAQSCO.SALESORG_RECORD_ID,
							SAQSCO.SERVICE_DESCRIPTION,
							SAQSCO.SERVICE_ID,
							SAQSCO.SERVICE_RECORD_ID,
							SAQSCO.EQUIPMENT_QUANTITY,								
							SAQSCO.FABLOCATION_NAME,
							SAQSCO.FABLOCATION_RECORD_ID,
							SAQTMT.CONTRACT_VALID_FROM,
       						SAQTMT.CONTRACT_VALID_TO,
							SAQTSV.PAR_SERVICE_DESCRIPTION,
							SAQTSV.PAR_SERVICE_ID,
							SAQTSV.PAR_SERVICE_RECORD_ID,
							'{UserName}' AS CPQTABLEENTRYADDEDBY,
							GETDATE() as CPQTABLEENTRYDATEADDED,
							{UserId} as CpqTableEntryModifiedBy,
							GETDATE() as CpqTableEntryDateModified
							FROM SAQSCO (NOLOCK) JOIN SAQTSV (NOLOCK) ON
							SAQSCO.QUOTE_ID = SAQTSV.QUOTE_ID AND
							SAQTSV.SERVICE_ID = '{TreeParam}' AND
							SAQTSV.SERVICE_TYPE = '{TreeParentParam}'
							JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID
							JOIN SYSPBT (NOLOCK) ON SYSPBT.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SYSPBT.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID
							WHERE 
							SAQSCO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCO.QTEREV_RECORD_ID = '{RevisionRecordId}'
							AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}')A LEFT JOIN SAQSGB (NOLOCK) AS M ON A.QUOTE_RECORD_ID = M.QUOTE_RECORD_ID AND M.SERVICE_ID = A.SERVICE_ID AND M.FABLOCATION_RECORD_ID =A.FABLOCATION_RECORD_ID AND M.GREENBOOK = A.GREENBOOK WHERE M.QUOTE_RECORD_ID is null                  
					""".format(
							TreeParam=self.tree_param if (self.tree_parent_level_0 == 'Comprehensive Services' or self.tree_parent_level_0 == 'Complementary Products') and self.sale_type != 'TOOL RELOCATION' else self.tree_parent_level_0,
							TreeParentParam=self.tree_parent_level_0 if (self.tree_parent_level_0 == 'Comprehensive Services' or self.tree_parent_level_0 == 'Complementary Products') and self.sale_type != 'TOOL RELOCATION' else self.tree_parent_level_1,
							QuoteRecordId=self.contract_quote_record_id,
							RevisionRecordId=self.quote_revision_record_id,
							BatchGroupRecordId=kwargs.get('batch_group_record_id'),
							UserName=self.user_name,
							UserId=self.user_id
						)
			)
		
		d2 = Sql.GetFirst("""SELECT QTEREV_ID,GREENBOOK FROM SAQSGB WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND GREENBOOK='{}' """.format(str(self.contract_quote_record_id), self.quote_revision_record_id, str(d1.GREENBOOK)))
		if d2:
			Trace.Write(str(d2.QTEREV_ID)+'==================>>>>>suri '+str(d2.GREENBOOK))
				
		#import time
		#time.sleep(50)
		getdate = Sql.GetFirst("""SELECT CONTRACT_VALID_FROM, CONTRACT_VALID_TO, QTEREV_ID FROM SAQTRV WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'""".format(str(self.contract_quote_record_id), self.quote_revision_record_id))
		if getdate:
			#update_contract_date_greenbook_level = "UPDATE SAQSGB SET CONTRACT_VALID_FROM = 'CONVERT(VARCHAR(10),{},101)', CONTRACT_VALID_TO = 'CONVERT(VARCHAR(10),{},101)', QTEREV_ID='{}' WHERE QUOTE_RECORD_ID ='{}' AND QTEREV_RECORD_ID = '{}'".format(getdate.CONTRACT_VALID_FROM, getdate.CONTRACT_VALID_TO, getdate.QTEREV_ID, self.contract_quote_record_id,self.quote_revision_record_id)
			update_contract_date_greenbook_level = "UPDATE SAQSGB SET QTEREV_ID=0 WHERE QUOTE_RECORD_ID ='{}' AND QTEREV_RECORD_ID = '{}'".format(self.contract_quote_record_id,self.quote_revision_record_id)
			Sql.RunQuery(update_contract_date_greenbook_level)
					
	
	def _insert_quote_service_preventive_maintenance_kit_parts(self, **kwargs):
		Sql.RunQuery("""DELETE FROM SAQSAP WHERE QUOTE_RECORD_ID = '{contract_quote_record_id}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'""".format(contract_quote_record_id = self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id))
		Sql.RunQuery("""DELETE FROM SAQSKP WHERE QUOTE_RECORD_ID = '{contract_quote_record_id}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'""".format(contract_quote_record_id = self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id))
		#TKM_start_time = time.time()
		
		#Suresh Added
		CRMQT = SqlHelper.GetFirst("select convert(varchar(100),c4c_quote_id) as c4c_quote_id,MASTER_TABLE_QUOTE_RECORD_ID AS QUOTE_RECORD_ID from SAQTMT(nolock) WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{contract_quote_record_id}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'".format(contract_quote_record_id = self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id)) 
		SAQSCA = "SAQSCA_BKP_"+str(CRMQT.c4c_quote_id)
		SAQSCA_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQSCA)+"'' ) BEGIN DROP TABLE "+str(SAQSCA)+" END  ' ")
		sure0090 = SqlHelper.GetFirst("sp_executesql @T=N'SELECT * INTO "+str(SAQSCA)+" FROM SAQSCA(NOLOCK) WHERE QUOTE_RECORD_ID = ''"+str(CRMQT.QUOTE_RECORD_ID)+"'' AND QTEREV_RECORD_ID = ''"+str(self.quote_revision_record_id)+"''  ' ")
		#Suresh Ended
		self._process_query("""INSERT SAQSAP (
				ASSEMBLY_ID,
				ASSEMBLY_DESCRIPTION,
				ASSEMBLY_RECORD_ID,
				EQUIPMENT_ID,
				EQUIPMENT_DESCRIPTION,
				EQUIPMENT_RECORD_ID,
				GOT_CODE,
				KIT_ID,
				KIT_NAME, 
				KIT_NUMBER,
				KIT_NUMBER_RECORD_ID,
				KIT_RECORD_ID,
				PM_ID,
				PM_NAME,
				PM_RECORD_ID,
				QUOTE_ID,
				QUOTE_RECORD_ID,
				QTEREV_ID,
				QTEREV_RECORD_ID,
				SERIAL_NO,
				SERVICE_DESCRIPTION,
				SERVICE_ID,
				SALESORG_ID,
				SALESORG_RECORD_ID,
				PM_FREQUENCY,
				QTESRVCOA_RECORD_ID,
				PAR_SERVICE_DESCRIPTION,
				PAR_SERVICE_ID,
				PAR_SERVICE_RECORD_ID,
				QUOTE_SERVICE_COV_OBJ_ASS_PM_KIT_RECORD_ID,
				CPQTABLEENTRYADDEDBY,
				CPQTABLEENTRYDATEADDED
				) SELECT PM.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_COV_OBJ_ASS_PM_KIT_RECORD_ID,'{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM (
				SELECT DISTINCT  
				MAEAPK.ASSEMBLY_ID,
				SAQSCA.ASSEMBLY_DESCRIPTION,
				SAQSCA.ASSEMBLY_RECORD_ID,
				MAEAPK.EQUIPMENT_ID,
				SAQSCA.EQUIPMENT_DESCRIPTION,
				SAQSCA.EQUIPMENT_RECORD_ID,
				SAQSCA.GOT_CODE,
				MAEAPK.KIT_ID,
				MAEAPK.KIT_NAME,
				MAEAPK.KIT_NUMBER,
				MATKTN.TOOL_KIT_NUMBER_RECORD_ID AS KIT_NUMBER_RECORD_ID,
				MAMKIT.KIT_RECORD_ID,
				SGPMNT.PM_ID,
				MAEAPK.PM_NAME,
				SGPMNT.PM_RECORD_ID AS PM_RECORD_ID,
				'{QuoteId}' as QUOTE_ID,
				'{QuoteRecordId}' as QUOTE_RECORD_ID,
				'{RevisionId}' as QTEREV_ID,
				'{RevisionRecordId}' as QTEREV_RECORD_ID,
				SAQSCA.SERIAL_NUMBER,
				SAQSCA.SERVICE_DESCRIPTION,
				SAQSCA.SERVICE_ID,
				SAQTRV.SALESORG_ID,
				SAQTRV.SALESORG_RECORD_ID,
				MAEAPK.PM_FREQUENCY,
				SAQSCA.QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID AS QTESRVCOA_RECORD_ID,
				SAQSCA.PAR_SERVICE_DESCRIPTION,
				SAQSCA.PAR_SERVICE_ID,
				SAQSCA.PAR_SERVICE_RECORD_ID
				FROM SYSPBT (NOLOCK) 
				JOIN {SAQSCA} SAQSCA(NOLOCK) ON SAQSCA.QUOTE_RECORD_ID = SYSPBT.QUOTE_RECORD_ID AND SAQSCA.EQUIPMENT_RECORD_ID = SYSPBT.BATCH_RECORD_ID AND SAQSCA.QTEREV_RECORD_ID = SYSPBT.QTEREV_RECORD_ID
				JOIN MAEAPK (NOLOCK) ON MAEAPK.ASSEMBLY_ID = SAQSCA.ASSEMBLY_ID AND MAEAPK.EQUIPMENT_ID =  SAQSCA.EQUIPMENT_ID 
				LEFT JOIN MAMKIT(NOLOCK) ON MAMKIT.KIT_ID =  MAEAPK.KIT_ID 
				LEFT JOIN MATKTN(NOLOCK) ON MATKTN.KIT_ID = MAEAPK.KIT_ID AND MATKTN.KIT_NUMBER = MAEAPK.KIT_NUMBER
				JOIN SGPMNT(NOLOCK) ON SGPMNT.PM_NAME = MAEAPK.PM_NAME 
				JOIN SAQTRV(NOLOCK) ON SAQTRV.QUOTE_RECORD_ID = SAQSCA.QUOTE_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = SAQSCA.QTEREV_RECORD_ID
				WHERE SYSPBT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}' AND SYSPBT.QTEREV_RECORD_ID = '{RevisionRecordId}') PM """.format(
				UserName=self.user_name,
				QuoteId = self.contract_quote_id,
				QuoteRecordId=self.contract_quote_record_id,
				RevisionId=self.quote_revision_id,
				RevisionRecordId=self.quote_revision_record_id,
				BatchGroupRecordId=kwargs.get('batch_group_record_id'),
				SAQSCA = str(SAQSCA)
				)
			)
		
		self._process_query("""INSERT SAQSKP (
				ASSEMBLY_ID,
				ASSEMBLY_DESCRIPTION,
				ASSEMBLY_RECORD_ID,
				EQUIPMENT_ID,
				EQUIPMENT_DESCRIPTION,
				EQUIPMENT_RECORD_ID,
				KIT_ID,
				KIT_NAME,
				KIT_NUMBER,
				KIT_NUMBER_RECORD_ID,
				KIT_RECORD_ID,
				PART_NUMBER,
				PART_DESCRIPTION,
				PART_RECORD_ID,
				QUANTITY,
				PM_ID,
				PM_NAME,
				PM_RECORD_ID,
				TKM_FLAG,
				QUOTE_ID,
				QUOTE_RECORD_ID,
				QTEREV_ID,
				QTEREV_RECORD_ID,
				SERVICE_DESCRIPTION,
				SERVICE_ID,
				SERVICE_RECORD_ID,
				QTESRVMASY_RECORD_ID,
				PAR_SERVICE_DESCRIPTION,
				PAR_SERVICE_ID,
				PAR_SERVICE_RECORD_ID,
				QUOTE_SERVICE_COV_OBJ_ASS_PM_KIT_PARTS_RECORD_ID,
				CPQTABLEENTRYADDEDBY,
				CPQTABLEENTRYDATEADDED
				) 
				SELECT KP.*,CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_COV_OBJ_ASS_PM_KIT_PARTS_RECORD_ID,'{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM (
				SELECT DISTINCT
				SAQSAP.ASSEMBLY_ID,
				SAQSCA.ASSEMBLY_DESCRIPTION,
				SAQSCA.ASSEMBLY_RECORD_ID,
				SAQSAP.EQUIPMENT_ID,
				SAQSCA.EQUIPMENT_DESCRIPTION,
				SAQSCA.EQUIPMENT_RECORD_ID,
				SAQSAP.KIT_ID,
				MAMKIT.KIT_NAME,
				SAQSAP.KIT_NUMBER,
				MATKTN.TOOL_KIT_NUMBER_RECORD_ID AS KIT_NUMBER_RECORD_ID,
				MAMKIT.KIT_RECORD_ID,
				MAMTRL.SAP_PART_NUMBER,
				MAMTRL.SAP_DESCRIPTION,
				MAMTRL.MATERIAL_RECORD_ID,
				MAKTPT.QUANTITY,
				SGPMNT.PM_ID,
				SAQSAP.PM_NAME,
				SGPMNT.PM_RECORD_ID AS PM_RECORD_ID,
				1 as TKM_FLAG,
				'{QuoteId}' as QUOTE_ID,
				'{QuoteRecordId}' as QUOTE_RECORD_ID,
				'{RevisionId}' as QTEREV_ID,
				'{RevisionRecordId}' as QTEREV_RECORD_ID,
				SAQSCA.SERVICE_DESCRIPTION,
				SAQSCA.SERVICE_ID,
				SAQSCA.SERVICE_RECORD_ID,
				SAQSCA.QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID AS QTESRVMASY_RECORD_ID,
				SAQSCA.PAR_SERVICE_DESCRIPTION,
				SAQSCA.PAR_SERVICE_ID,
				SAQSCA.PAR_SERVICE_RECORD_ID
				FROM SYSPBT (NOLOCK)
				JOIN {SAQSCA} SAQSCA (NOLOCK) ON SAQSCA.QUOTE_RECORD_ID = SYSPBT.QUOTE_RECORD_ID AND SAQSCA.EQUIPMENT_RECORD_ID = SYSPBT.BATCH_RECORD_ID AND SAQSCA.QTEREV_RECORD_ID = SYSPBT.QTEREV_RECORD_ID
				JOIN SAQSAP (NOLOCK) ON SAQSCA.QUOTE_RECORD_ID = SAQSAP.QUOTE_RECORD_ID AND SAQSCA.QTEREV_RECORD_ID = SAQSAP.QTEREV_RECORD_ID
				AND SAQSAP.ASSEMBLY_ID = SAQSCA.ASSEMBLY_ID AND SAQSAP.EQUIPMENT_ID =  SAQSCA.EQUIPMENT_ID 		AND SAQSAP.QTEREV_RECORD_ID =  SAQSCA.QTEREV_RECORD_ID		
				INNER JOIN MAMKIT(NOLOCK) ON MAMKIT.KIT_ID =  SAQSAP.KIT_ID 
				INNER JOIN MATKTN(NOLOCK) ON MATKTN.KIT_ID = SAQSAP.KIT_ID AND ISNULL(MATKTN.KIT_NUMBER ,'')= ISNULL(SAQSAP.KIT_NUMBER,ISNULL(MATKTN.KIT_NUMBER ,''))
				JOIN SGPMNT(NOLOCK) ON SGPMNT.PM_NAME = SAQSAP.PM_NAME 
				JOIN MAKTPT(NOLOCK) ON MAKTPT.KIT_ID = SAQSAP.KIT_ID
				JOIN MAMTRL(NOLOCK) ON MAMTRL.SAP_PART_NUMBER = MAKTPT.PART_NUMBER
				WHERE SYSPBT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}' AND SYSPBT.QTEREV_RECORD_ID = '{RevisionRecordId}') KP """.format(
				UserName=self.user_name,
				QuoteId = self.contract_quote_id,
				QuoteRecordId=self.contract_quote_record_id,
				RevisionId=self.quote_revision_id,
				RevisionRecordId=self.quote_revision_record_id,
				BatchGroupRecordId=kwargs.get('batch_group_record_id'),
				SAQSCA = str(SAQSCA)
				))
		#TKM_end_time = time.time()
		
		#SAQSCA_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQSCA)+"'' ) BEGIN DROP TABLE "+str(SAQSCA)+" END  ' ")
		##UPDATING THE TKM COLUMN VALUE STARTS..
		Sql.RunQuery("""UPDATE SAQSAP SET TKM_FLAG = 1 from SAQSAP join (Select count(QUOTE_SERVICE_COV_OBJ_ASS_PM_KIT_PARTS_RECORD_ID) as cnt,EQUIPMENT_ID,ASSEMBLY_ID,PM_ID,QUOTE_RECORD_ID
			from SAQSKP(NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' group by EQUIPMENT_ID,ASSEMBLY_ID,PM_ID,QUOTE_RECORD_ID) as parts on 
			SAQSAP.EQUIPMENT_ID = parts.EQUIPMENT_ID  AND parts.ASSEMBLY_ID = SAQSAP.ASSEMBLY_ID AND parts.PM_ID = SAQSAP.PM_ID AND parts.QUOTE_RECORD_ID = SAQSAP.QUOTE_RECORD_ID WHERE SAQSAP.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSAP.QTEREV_RECORD_ID = '{RevisionRecordId}' and parts.cnt > 0""".format(QuoteRecordId = self.contract_quote_record_id,RevisionRecordId= self.quote_revision_record_id ))
		##UPDATING THE TKM COLUMN VALU ENDS.
		return True

	def _insert_quote_item_fab_location(self, **kwargs):
		self._process_query(
			"""INSERT SAQIFL(
				FABLOCATION_ID,
				FABLOCATION_NAME,
				FABLOCATION_RECORD_ID,
				SERVICE_ID,
				SERVICE_DESCRIPTION,
				SERVICE_RECORD_ID,
				LINE_ITEM_ID,
				QUOTE_ID,
				QUOTE_NAME,
				QUOTE_RECORD_ID,
				QTEREV_ID,
				QTEREV_RECORD_ID,
				SALESORG_ID,
				SALESORG_NAME,
				SALESORG_RECORD_ID,
				QUOTE_ITEM_FAB_LOCATION_RECORD_ID,
				CPQTABLEENTRYADDEDBY,
				CPQTABLEENTRYDATEADDED,
				CpqTableEntryModifiedBy, 
				CpqTableEntryDateModified
				) SELECT FB.*,CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_FAB_LOCATION_RECORD_ID,
				'{UserName}' AS CPQTABLEENTRYADDEDBY,
				GETDATE() as CPQTABLEENTRYDATEADDED,
				{UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
				SELECT DISTINCT
				SAQICO.FABLOCATION_ID,
				SAQICO.FABLOCATION_NAME,
				SAQICO.FABLOCATION_RECORD_ID,
				SAQICO.SERVICE_ID,
				SAQICO.SERVICE_DESCRIPTION,
				SAQICO.SERVICE_RECORD_ID,
				SAQICO.LINE_ITEM_ID,
				SAQICO.QUOTE_ID,
				SAQICO.QUOTE_NAME,
				SAQICO.QUOTE_RECORD_ID,
				SAQICO.QTEREV_ID,
				SAQICO.QTEREV_RECORD_ID,
				SAQICO.SALESORG_ID,
				SAQICO.SALESORG_NAME,
				SAQICO.SALESORG_RECORD_ID
				FROM SAQICO (NOLOCK)
				JOIN MAFBLC (NOLOCK) ON SAQICO.FABLOCATION_ID = MAFBLC.FAB_LOCATION_ID 
				JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQICO.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = SAQICO.QTEREV_RECORD_ID
				JOIN SYSPBT (NOLOCK) ON SYSPBT.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SYSPBT.BATCH_RECORD_ID = SAQICO.EQUIPMENT_RECORD_ID AND SYSPBT.QTEREV_RECORD_ID = SAQICO.QTEREV_RECORD_ID
				WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}' AND
				SAQICO.SERVICE_ID = '{TreeParam}'
				) FB""".format(
								TreeParam=self.tree_param if self.tree_parent_level_0 == 'Comprehensive Services' else self.tree_parent_level_0,
								QuoteRecordId=self.contract_quote_record_id,
								RevisionRecordId =self.quote_revision_record_id,
								BatchGroupRecordId=kwargs.get('batch_group_record_id'),
								UserId=self.user_id,
								UserName=self.user_name,
							)
		)

	def _insert_quote_item_greenbook(self, **kwargs):
		self._process_query(
			"""INSERT SAQIGB(
				GREENBOOK,
				GREENBOOK_RECORD_ID,
				FABLOCATION_ID,
				FABLOCATION_NAME,
				FABLOCATION_RECORD_ID,
				SERVICE_ID,
				SERVICE_DESCRIPTION,
				SERVICE_RECORD_ID,
				LINE_ITEM_ID,
				EQUIPMENT_QUANTITY,
				GLOBAL_CURRENCY,
				DOC_CURRENCY,
				GLOBAL_CURRENCY_RECORD_ID,
				DOCCURR_RECORD_ID,
				QUOTE_ID,
				QUOTE_NAME,
				QUOTE_RECORD_ID,
				QTEREV_ID,
				QTEREV_RECORD_ID,
				SALESORG_ID,
				SALESORG_NAME,
				SALESORG_RECORD_ID,
				QUOTE_ITEM_GREENBOOK_RECORD_ID,
				CPQTABLEENTRYADDEDBY,
				CPQTABLEENTRYDATEADDED,
				CpqTableEntryModifiedBy, 
				CpqTableEntryDateModified
				) SELECT FB.*,CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_GREENBOOK_RECORD_ID,
				'{UserName}' AS CPQTABLEENTRYADDEDBY,
				GETDATE() as CPQTABLEENTRYDATEADDED, 
				{UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
				SELECT DISTINCT
				SAQICO.GREENBOOK,
				SAQICO.GREENBOOK_RECORD_ID,
				SAQICO.FABLOCATION_ID,
				SAQICO.FABLOCATION_NAME,
				SAQICO.FABLOCATION_RECORD_ID,
				SAQICO.SERVICE_ID,
				SAQICO.SERVICE_DESCRIPTION,
				SAQICO.SERVICE_RECORD_ID,
				SAQICO.LINE_ITEM_ID,
				SAQICO.EQUIPMENT_QUANTITY,
				SAQICO.GLOBAL_CURRENCY,
				SAQICO.DOC_CURRENCY,
				SAQICO.GLOBAL_CURRENCY_RECORD_ID,
				SAQICO.DOCURR_RECORD_ID,
				SAQICO.QUOTE_ID,
				SAQICO.QUOTE_NAME,
				SAQICO.QUOTE_RECORD_ID,
				SAQICO.QTEREV_ID,
				SAQICO.QTEREV_RECORD_ID,
				SAQICO.SALESORG_ID,
				SAQICO.SALESORG_NAME,
				SAQICO.SALESORG_RECORD_ID
				FROM SAQICO (NOLOCK)
				JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQICO.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = SAQICO.QTEREV_RECORD_ID
				JOIN SYSPBT (NOLOCK) ON SYSPBT.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SYSPBT.BATCH_RECORD_ID = SAQICO.EQUIPMENT_RECORD_ID AND SYSPBT.QTEREV_RECORD_ID = SAQICO.QTEREV_RECORD_ID
				WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}' AND
				SAQICO.SERVICE_ID = '{TreeParam}' AND NOT EXISTS (SELECT GREENBOOK FROM SAQIGB WHERE QUOTE_RECORD_ID ='{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID = '{TreeParam}')
				) FB""".format(
								TreeParam=self.tree_param if (self.tree_parent_level_0 == 'Comprehensive Services' or self.tree_parent_level_0 == 'Complementary Products') and self.sale_type != 'TOOL RELOCATION' else self.tree_parent_level_0,
								QuoteRecordId=self.contract_quote_record_id,
								RevisionRecordId=self.quote_revision_record_id,
								BatchGroupRecordId=kwargs.get('batch_group_record_id'),
								UserId=self.user_id,
								UserName=self.user_name,
							)
			)

		Sql.RunQuery("""UPDATE SAQIGB
			SET
			SAQIGB.EQUIPMENT_QUANTITY = IQ.QTY
			FROM SAQIGB (NOLOCK) 
			INNER JOIN (
				SELECT COUNT(SAQICO.EQUIPMENT_ID) as QTY,SAQIGB.CpqTableEntryId,SAQICO.FABLOCATION_RECORD_ID, SAQICO.SERVICE_RECORD_ID, SAQICO.GREENBOOK_RECORD_ID
				FROM SAQICO (NOLOCK) 
				JOIN SAQIGB (NOLOCK) ON SAQIGB.QUOTE_RECORD_ID = SAQICO.QUOTE_RECORD_ID and SAQIGB.QTEREV_RECORD_ID = SAQICO.QTEREV_RECORD_ID and SAQIGB.GREENBOOK_RECORD_ID = SAQICO.GREENBOOK_RECORD_ID and SAQIGB.SERVICE_RECORD_ID = SAQICO.SERVICE_RECORD_ID and SAQIGB.FABLOCATION_RECORD_ID = SAQICO.FABLOCATION_RECORD_ID 
				WHERE SAQICO.QUOTE_RECORD_ID ='{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{RevisionRecordId}' GROUP BY SAQICO.FABLOCATION_RECORD_ID,SAQICO.SERVICE_RECORD_ID,SAQICO.GREENBOOK_RECORD_ID,SAQIGB.CpqTableEntryId
			)AS IQ
			ON SAQIGB.CpqTableEntryId = IQ.CpqTableEntryId""".format(QuoteRecordId= self.contract_quote_record_id))
	def _create(self):
		if self.action_type == "ADD_COVERED_OBJ":
			covered_start_time = time.time()
			master_object_name = "SAQFEQ"
			if self.values:
				record_ids = []
				if self.all_values:        
					qury_str=""
					if A_Keys!="" and A_Values!="":
						for key,val in zip(A_Keys,A_Values):
							if(val!=""):
								if key=="QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID":
									key="CpqTableEntryId"
									val = ''.join(re.findall(r'\d+', val)) if not val.isdigit() else val
								qury_str+=" "+key+" LIKE '%"+val+"%' AND "
					if self.tree_param != '' and self.tree_parent_level_0 == 'Add-On Products' : #ADDED FOR ADD ON PRODUCT SCENARIO
						query_string ="select SAQFEQ.QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID, SAQFEQ.EQUIPMENT_ID, SAQFEQ.SERIAL_NUMBER, SAQFEQ.PBG, SAQFEQ.PLATFORM, SAQFEQ.FABLOCATION_ID, SAQFEQ.FABLOCATION_NAME from  SAQFEQ(NOLOCK) JOIN SAQSCO ON SAQSCO.QUOTE_ID = SAQFEQ.QUOTE_ID  AND SAQSCO.EQUIPMENT_ID = SAQFEQ.EQUIPMENT_ID AND SAQSCO.QTEREV_RECORD_ID = SAQFEQ.QTEREV_RECORD_ID  WHERE SAQFEQ.QUOTE_RECORD_ID = '{quo_rec_id}' AND SAQFEQ.QTEREV_RECORD_ID = '{RevisionRecordId}' AND {Qury_Str} NOT EXISTS(SELECT EQUIPMENT_ID FROM SAQSCO WHERE QUOTE_RECORD_ID = '{quo_rec_id}' and QTEREV_RECORD_ID = '{RevisionRecordId}' and SERVICE_ID ='{TreeParam}' ) ".format(quo_rec_id=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id,TreeParam = self.tree_param,Qury_Str=qury_str)
					else:
						if self.tree_param == "Sending Equipment" or self.tree_param == "Receiving Equipment":
							query_string = "SELECT QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID FROM SAQFEQ (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND RELOCATION_EQUIPMENT_TYPE = '{tree_param}' AND {Qury_Str} EQUIPMENT_ID NOT IN(SELECT EQUIPMENT_ID FROM SAQSCO WHERE QUOTE_RECORD_ID ='{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID ='{TreeParam}'  AND RELOCATION_EQUIPMENT_TYPE = '{tree_param}')".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id,TreeParam = self.tree_param if self.tree_parent_level_0 == 'Comprehensive Services' else self.tree_parent_level_0,Qury_Str=qury_str,tree_param=str(self.tree_param).upper())
						else:

							query_string = "SELECT QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID FROM SAQFEQ (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND {Qury_Str} EQUIPMENT_ID NOT IN(SELECT EQUIPMENT_ID FROM SAQSCO WHERE QUOTE_RECORD_ID ='{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID ='{TreeParam}')".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id,TreeParam = self.tree_param,Qury_Str=qury_str)
					query_string_for_count = "SELECT COUNT(*) as count FROM ({Query_String})OQ".format(
						Query_String=query_string
					)
					table_count_data = Sql.GetFirst(query_string_for_count)
					if table_count_data is not None:
						table_total_rows = table_count_data.count
					if table_total_rows:
						record_ids = [data for data in self.get_results(query_string, table_total_rows)]                    
				else:                    
					record_ids = [
						CPQID.KeyCPQId.GetKEYId(master_object_name, str(value))
						if value.strip() != "" and master_object_name in value
						else value
						for value in self.values
					]
				batch_group_record_id = str(Guid.NewGuid()).upper()
				record_ids = str(str(record_ids)[1:-1].replace("'",""))
				parameter = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'SELECT' ")				
				primaryQueryItems = SqlHelper.GetFirst(""+str(parameter.QUERY_CRITERIA_1)+" SYSPBT(BATCH_RECORD_ID, BATCH_STATUS, QUOTE_ID, QUOTE_RECORD_ID, BATCH_GROUP_RECORD_ID,QTEREV_RECORD_ID) SELECT SAQFEQ.EQUIPMENT_RECORD_ID as BATCH_RECORD_ID, ''IN PROGRESS'' as BATCH_STATUS, SAQFEQ.QUOTE_ID, SAQFEQ.QUOTE_RECORD_ID, ''"+str(batch_group_record_id)+"'' as BATCH_GROUP_RECORD_ID,''"+str(self.quote_revision_record_id)+"'' as QTEREV_RECORD_ID FROM SAQFEQ (NOLOCK) JOIN splitstring(''"+record_ids+"'') ON ltrim(rtrim(NAME)) = SAQFEQ.QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID'")
				#self._process_query("""INSERT INTO SYSPBT(BATCH_RECORD_ID, BATCH_STATUS, QUOTE_ID, QUOTE_RECORD_ID, BATCH_GROUP_RECORD_ID) 
				#                        SELECT SAQFEQ.EQUIPMENT_RECORD_ID as BATCH_RECORD_ID, 'IN PROGRESS' as BATCH_STATUS, SAQFEQ.QUOTE_ID, SAQFEQ.QUOTE_RECORD_ID, '{BatchGroupRecordId}' as BATCH_GROUP_RECORD_ID FROM SAQFEQ (NOLOCK) JOIN splitstring('{QuoteEquipmentRecordIds}')
				#                        ON NAME = SAQFEQ.QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID """.format(BatchGroupRecordId=batch_group_record_id, QuoteEquipmentRecordIds=str(record_ids)[1:-1].replace("'","")))
			
				#where_string = "AND SAQFEQ.QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID IN ('{QuoteEquipmentRecordIds}')".format(QuoteEquipmentRecordIds="','".join(record_ids))
				#SAQSCO_start_time = time.time()
				self._insert_quote_service_covered_object(batch_group_record_id=batch_group_record_id)
				#SAQSCO_end_time = time.time()
				
				#SAQSCA_start_time = time.time()
				Trace.Write("@4546-5576--------"+str(record_ids))
				self._insert_quote_service_covered_assembly(batch_group_record_id=batch_group_record_id)				
				self._insert_quote_service_fab_location(batch_group_record_id=batch_group_record_id)
				#SAQSCA_end_time = time.time()
				
				#SAQSGB_start_time = time.time()
				self._insert_quote_service_greenbook(batch_group_record_id=batch_group_record_id)
				#SAQSGB_end_time = time.time()				
				self._insert_quote_service_preventive_maintenance_kit_parts(batch_group_record_id=batch_group_record_id)
				#COVERED OBJ PRE DEFINED LOGIC
				try:	
					Trace.Write("PREDEFINED WAFER DRIVER IFLOW")					
					CQTVLDRIFW.valuedriver_predefined(self.contract_quote_record_id,"PREDEFINED DRIVER",self.tree_param, self.tree_parent_level_0, self.tree_parent_level_1, self.tree_parent_level_2,self.user_id,self.user_name,self.quote_revision_record_id)
				except:
					Trace.Write("EXCEPT----PREDEFINED DRIVER IFLOW")
				#COVERED OBJ DRIVER ROLL DOWN
				try:						
					CQTVLDRIFW.iflow_valuedriver_rolldown(self.contract_quote_record_id,"SERVICE COST AND VALUE DRIVERS",self.tree_param, self.tree_parent_level_0, self.tree_parent_level_1, self.tree_parent_level_2,self.user_id,self.user_name,self.quote_revision_record_id)
				except:
					Trace.Write("EXCEPT----SERVICE COST AND VALUE DRIVER LEVEL IFLOW")
				
				# Billing Matrix - Detail Insert - Start                    
				# self._insert_billing_matrix()				
				# Billing Matrix - Detail Insert - End
				#ENTITLEMENT SV TO CE
				Entitlement_start_time = time.time()
				if self.trigger_from == 'PythonScript':
					contracts_obj = Sql.GetList("SELECT DISTINCT SERVICE_ID FROM CTCSCE (NOLOCK) WHERE CONTRACT_ID = '{ContractId}'".format(ContractId=self.source_contract_id))
					if contracts_obj:
						product_list = [(contract_obj.SERVICE_ID).strip() for contract_obj in contracts_obj]
						product_list=','.join(map(str, product_list))					
					try:
						level = "COV OBJ RENEWAL ONE="+product_list+"="+self.contract_quote_record_id+"="+str(self.quote_revision_record_id)			
						CQVLDRIFLW.iflow_valuedriver_rolldown(self.source_contract_id,level)
					except:						
						Log.Info("except renewal one SAQSCE")
				else:
					#ENTITLEMENT SV TO CE AND GB
					try:
						if self.tree_param != 'Receiving Equipment':
							level = "COV OBJ ENTITLEMENT,"+str(self.tree_param)+","+str(self.tree_parent_level_0)+","+str(self.user_id)+","+str(self.quote_revision_record_id)
							CQVLDRIFLW.iflow_valuedriver_rolldown(self.contract_quote_record_id,level)						
					except:
						Trace.Write("EXCEPT----COV OBJ ENTITLEMENT IFLOW")
				Entitlement_end_time = time.time()
				Log.Info("Entitlement end==> "+str(Entitlement_end_time - Entitlement_start_time))

				self._process_query(
					"""DELETE FROM SYSPBT WHERE SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}' and SYSPBT.QTEREV_RECORD_ID = '{RevisionRecordId}' and SYSPBT.BATCH_STATUS = 'IN PROGRESS'""".format(
						BatchGroupRecordId=batch_group_record_id,RevisionRecordId=self.quote_revision_record_id
					))
				covered_end_time = time.time()
				Log.Info("ADD_COVERED_OBJ end==> "+str(covered_end_time - covered_start_time) +" QUOTE ID----"+str(self.contract_quote_id))
						
		return True
	
	def _update(self):
		pass

	def _delete(self):
		pass


class ContractQuoteBillingMatrixModel(ContractQuoteCrudOpertion):
	def __init__(self, **kwargs):
		ContractQuoteCrudOpertion.__init__(self, trigger_from=kwargs.get('trigger_from'), contract_quote_record_id=kwargs.get('contract_quote_record_id'),quote_revision_record_id=kwargs.get('quote_revision_record_id'),
											tree_param=kwargs.get('tree_param'), tree_parent_level_0=kwargs.get('tree_parent_level_0'))
		self.opertion = kwargs.get('opertion')
		self.action_type = kwargs.get('action_type')
		self.values = kwargs.get('values')
		self.table_name = kwargs.get('table_name')
		self.all_values = kwargs.get('all_values')		
		self.node_id = ""		
	
	def _create(self):
		billing_plan_obj = Sql.GetFirst("SELECT * FROM SAQTBP (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(self.contract_quote_record_id,self.quote_revision_record_id))
		if self.contract_start_date and self.contract_end_date and billing_plan_obj:
			if billing_plan_obj or self.trigger_from == 'IntegrationScript':				
				contract_start_date = billing_plan_obj.BILLING_START_DATE
				contract_end_date = billing_plan_obj.BILLING_END_DATE				
				start_date = datetime.datetime.strptime(UserPersonalizationHelper.ToUserFormat(contract_start_date), '%m/%d/%Y')
				billing_day = int(billing_plan_obj.BILLING_DAY)
				if billing_day in (29,30,31):
					if start_date.month == 2:
						isLeap = lambda x: x % 4 == 0 and (x % 100 != 0 or x % 400 == 0)
						end_day = 29 if isLeap(start_date.year) else 28
						start_date = start_date.replace(day=end_day)
					elif start_date.month in (4, 6, 9, 11) and billing_day == 31:
						start_date = start_date.replace(day=30)
					else:
						start_date = start_date.replace(day=billing_day)
				else:
					start_date = start_date.replace(day=billing_day)
				end_date = datetime.datetime.strptime(UserPersonalizationHelper.ToUserFormat(contract_end_date), '%m/%d/%Y')			
				diff1 = end_date - start_date

				avgyear = 365.2425        # pedants definition of a year length with leap years
				avgmonth = 365.2425/12.0  # even leap years have 12 months
				years, remainder = divmod(diff1.days, avgyear)
				years, months = int(years), int(remainder // avgmonth)            
				
				total_months = years * 12 + months
				Sql.RunQuery("""DELETE FROM SAQIBP WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'""".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id))
				#Sql.RunQuery("""DELETE FROM QT__QTQIBP WHERE QUOTE_RECORD_ID = '{QuoteRecordId}'""".format(QuoteRecordId=self.contract_quote_record_id))
				entitlement_obj = Sql.GetFirst("select convert(xml,replace(replace(ENTITLEMENT_XML,'&',';#38'),'''',';#39')) as ENTITLEMENT_XML,QUOTE_RECORD_ID,SERVICE_ID from SAQTSE (nolock) where QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'".format(QuoteRecordId =self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id))
				for index in range(0, total_months+1):
					self.insert_items_billing_plan(total_months=total_months, 
											billing_date="DATEADD(month, {Month}, '{BillingDate}')".format(
												Month=index, BillingDate=start_date.strftime('%m/%d/%Y')
												), amount_column="YEAR_"+str((index/12) + 1),
												entitlement_obj=entitlement_obj)  
				#self.insert_quote_items_billing_plan()
				cart_obj = self._get_record_obj(
					columns=["CART_ID", "USERID"],
					table_name="CART",
					where_condition="ExternalId = '{}'".format(self.c4c_quote_id),
					single_record=True,
				)
				if cart_obj:
					self.insert_quote_billing_plan(cart_obj.CART_ID,cart_obj.USERID)
					Trace.Write('5400---')
					if self.trigger_from == 'IntegrationScript':
						try:							
							self._delete_quote_tools(cart_obj.CART_ID, cart_obj.USERID)
							self._insert_quote_tools(cart_obj.CART_ID, cart_obj.USERID)
							self._delete_quote_line_items(cart_obj.CART_ID, cart_obj.USERID)
							self._insert_quote_line_items(cart_obj.CART_ID, cart_obj.USERID) 
						except:							
							self._delete_quote_tools(cart_obj.CART_ID, cart_obj.USERID)
							self._insert_quote_tools(cart_obj.CART_ID, cart_obj.USERID)
							self._delete_quote_line_items(cart_obj.CART_ID, cart_obj.USERID)
							self._insert_quote_line_items(cart_obj.CART_ID, cart_obj.USERID) 
				if not self.trigger_from == 'IntegrationScript':
					Sql.RunQuery("""UPDATE SAQTBP
										SET 
										IS_CHANGED = 0                                
										WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'
										""".format(						
							QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id
						))
		else:
			cart_obj = self._get_record_obj(
				columns=["CART_ID", "USERID"],
				table_name="CART",
				where_condition="ExternalId = '{}'".format(self.c4c_quote_id),
				single_record=True,
			)
			#if self.trigger_from == 'IntegrationScript':
				
				#self._delete_quote_tools(cart_obj.CART_ID, cart_obj.USERID)
				#self._insert_quote_tools(cart_obj.CART_ID, cart_obj.USERID)
				#self._delete_quote_line_items(cart_obj.CART_ID, cart_obj.USERID)
				#self._insert_quote_line_items(cart_obj.CART_ID, cart_obj.USERID)  
		
	def _update(self):		
		result = {}
		for array_val in self.values:            
			for data in array_val:
				result[data.Key] = data.Value

		Sql.RunQuery("""UPDATE SAQIBP
					SET BILLING_DATE = '{NewBillingDate}'                    
					WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND BILLING_DATE = '{OldBillingDate}'""".format(
					NewBillingDate=result.get('modified_date'), QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id, 
					OldBillingDate=result.get('billing_date')
		))
				
		return True

	def _insert_billing_matrix(self):
		Trace.Write("Insert Billing Matrix--5449---")
		'''Sql.RunQuery("""
				INSERT SAQTBP (
				QUOTE_BILLING_PLAN_RECORD_ID,
				BILLING_END_DATE,
				BILLING_INTERVAL,
				BILLING_DAY,
				BILLING_START_DATE,
				QUOTE_ID,
				QUOTE_NAME,
				QUOTE_RECORD_ID,
				CPQTABLEENTRYADDEDBY,
				CPQTABLEENTRYDATEADDED,
				CpqTableEntryModifiedBy,
				CpqTableEntryDateModified,
				IS_CHANGED
				) 
				SELECT 
				CONVERT(VARCHAR(4000),NEWID()) as QUOTE_BILLING_PLAN_RECORD_ID,
				SAQTMT.CONTRACT_VALID_TO as BILLING_END_DATE,
				'MONTHLY' as BILLING_INTERVAL,
				30 as BILLING_DAY,
				SAQTMT.CONTRACT_VALID_FROM as BILLING_START_DATE,
				SAQTMT.QUOTE_ID,
				SAQTMT.QUOTE_NAME,
				SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID as QUOTE_RECORD_ID,
				'{UserName}' AS CPQTABLEENTRYADDEDBY,
				GETDATE() as CPQTABLEENTRYDATEADDED,
				{UserId} as CpqTableEntryModifiedBy,
				GETDATE() as CpqTableEntryDateModified,
				1                                   
				FROM SAQTMT (NOLOCK)
				JOIN (SELECT distinct e.QUOTE_RECORD_ID, replace(X.Y.value('(ENTITLEMENT_NAME)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_NAME,replace(X.Y.value('(ENTITLEMENT_DISPLAY_VALUE)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_DISPLAY_VALUE FROM (select QUOTE_RECORD_ID,convert(xml,replace(ENTITLEMENT_XML,'&',';#38')) as ENTITLEMENT_XML from SAQTSE (nolock) where QUOTE_RECORD_ID = '{QuoteRecordId}' ) e OUTER APPLY e.ENTITLEMENT_XML.nodes('QUOTE_ITEM_ENTITLEMENT') as X(Y)  ) as JQ ON
									JQ.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND JQ.ENTITLEMENT_NAME IN ('AGS_BIL_BIL_TYP') 
								AND JQ.ENTITLEMENT_DISPLAY_VALUE = 'Variable Billing'
				WHERE SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = '{QuoteRecordId}'
				AND NOT EXISTS (SELECT CpqTableEntryId FROM SAQTBP (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}')											
		""".format(                        
			QuoteRecordId= self.contract_quote_record_id,   
			UserId=self.user_id,
			UserName=self.user_name
		))'''
		Sql.RunQuery("""
				INSERT SAQTBP (
				QUOTE_BILLING_PLAN_RECORD_ID,
				BILLING_END_DATE,
				BILLING_INTERVAL,
				BILLING_DAY,
				BILLING_START_DATE,
				QUOTE_ID,
				QUOTE_NAME,
				QUOTE_RECORD_ID,
				QTEREV_ID,
				QTEREV_RECORD_ID,
				CPQTABLEENTRYADDEDBY,
				CPQTABLEENTRYDATEADDED,
				CpqTableEntryModifiedBy,
				CpqTableEntryDateModified,
				IS_CHANGED,
				SERVICE_ID,
				SERVICE_RECORD_ID
				) 
				SELECT 
				CONVERT(VARCHAR(4000),NEWID()) as QUOTE_BILLING_PLAN_RECORD_ID,
				SAQTMT.CONTRACT_VALID_TO as BILLING_END_DATE,
				'MONTHLY' as BILLING_INTERVAL,
				30 as BILLING_DAY,
				SAQTMT.CONTRACT_VALID_FROM as BILLING_START_DATE,
				SAQTMT.QUOTE_ID,
				SAQTMT.QUOTE_NAME,
				SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID as QUOTE_RECORD_ID,
				SAQTMT.QTEREV_ID as QTEREV_ID,
				SAQTMT.QTEREV_RECORD_ID as QTEREV_RECORD_ID,
				'{UserName}' AS CPQTABLEENTRYADDEDBY,
				GETDATE() as CPQTABLEENTRYDATEADDED,
				{UserId} as CpqTableEntryModifiedBy,
				GETDATE() as CpqTableEntryDateModified,
				1,
				SAQTSV.SERVICE_ID,
				SAQTSV.SERVICE_RECORD_ID                      
				FROM SAQTMT (NOLOCK) JOIN SAQTSV on SAQTSV.QUOTE_ID = SAQTMT.QUOTE_ID
				
				WHERE SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQTMT.QTEREV_RECORD_ID = '{RevisionRecordId}'
				AND NOT EXISTS (SELECT CpqTableEntryId FROM SAQTBP (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}')											
		""".format(                        
			QuoteRecordId= self.contract_quote_record_id,
			RevisionRecordId=self.quote_revision_record_id,
			UserId=self.user_id,
			UserName=self.user_name
		))
		#Not required right now for SAQTBP.
		#AND JQ.ENTITLEMENT_NAME IN ('FIXED_PRICE_PER_RESOU_EVENT_91','FIXED_PRICE_PER_RESOU_EVENT_92') 
		#AND JQ.ENTITLEMENT_VALUE_CODE = 'FIXED PRICE'
		#BM_line_item_start_time = time.time()
		self._create()
		#BM_line_item_end_time = time.time()		
		return True

class ContractQuoteItemsModel(ContractQuoteCrudOpertion):
	def __init__(self, **kwargs):
		ContractQuoteCrudOpertion.__init__(self, trigger_from=kwargs.get('trigger_from'), contract_quote_record_id=kwargs.get('contract_quote_record_id'),quote_revision_record_id=kwargs.get('quote_revision_record_id'),
											tree_param=kwargs.get('tree_param'), tree_parent_level_0=kwargs.get('tree_parent_level_0'),tree_parent_level_1=kwargs.get('tree_parent_level_1'))
		self.opertion = kwargs.get('opertion')
		self.action_type = kwargs.get('action_type')
		self.values = kwargs.get('values')
		self.table_name = kwargs.get('table_name')
		self.all_values = kwargs.get('all_values')		
		self.node_id = ""	

	def _quote_item_insert_process(self, where_string='', max_quote_item_count=0):
		# Insert SAQITM - Start
		Sql.RunQuery("""
					INSERT SAQITM (
					QUOTE_ITEM_RECORD_ID,
					QUOTE_RECORD_ID,
					QUOTE_ID,
					QUOTE_NAME,
					QTEREV_ID,
					QTEREV_RECORD_ID,
					CPQTABLEENTRYADDEDBY,
					CPQTABLEENTRYDATEADDED,
					CpqTableEntryModifiedBy,
					CpqTableEntryDateModified,
					SERVICE_DESCRIPTION,
					SERVICE_ID,
					SERVICE_RECORD_ID,
					SALESORG_ID,
					SALESORG_NAME,
					SALESORG_RECORD_ID,
					LINE_ITEM_ID,
					OBJECT_QUANTITY,
					QUANTITY,
					CURRENCY,
					CURRENCY_RECORD_ID,
					ITEM_TYPE,
					ITEM_STATUS,
					NET_VALUE,
					UOM_ID, 
					UOM_RECORD_ID,
					PLANT_RECORD_ID,
					PLANT_ID,
					PRICING_STATUS,
					LINE_ITEM_FROM_DATE,
					LINE_ITEM_TO_DATE,
					SRVTAXCAT_RECORD_ID,
					SRVTAXCAT_DESCRIPTION,
					SRVTAXCAT_ID,
					SRVTAXCLA_DESCRIPTION,
					SRVTAXCLA_ID,
					SRVTAXCLA_RECORD_ID,
					DOC_CURRENCY,
					DOCCURR_RECORD_ID,
					QUOTE_CURRENCY,
					QUOTE_CURRENCY_RECORD_ID,
					GLOBAL_CURRENCY,
					GLOBAL_CURRENCY_RECORD_ID,
					YEAR_OVER_YEAR) 
					SELECT 
					CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_RECORD_ID,
					SAQSCE.QUOTE_RECORD_ID,
					SAQSCE.QUOTE_ID,
					SAQTMT.QUOTE_NAME,
					SAQTMT.QTEREV_ID,
					SAQTMT.QTEREV_RECORD_ID,
					'{UserName}' AS CPQTABLEENTRYADDEDBY,
					GETDATE() as CPQTABLEENTRYDATEADDED,
					{UserId} as CpqTableEntryModifiedBy,
					GETDATE() as CpqTableEntryDateModified,
					SAQSCE.SERVICE_DESCRIPTION,
					CONCAT(SAQSCE.SERVICE_ID, '- BASE') as SERVICE_ID,
					SAQSCE.SERVICE_RECORD_ID,
					SAQSCE.SALESORG_ID,
					SAQSCE.SALESORG_NAME,
					SAQSCE.SALESORG_RECORD_ID,
					IQ.LINE_ITEM_ID as LINE_ITEM_ID,
					0 as OBJECT_QUANTITY,
					1 as QUANTITY,
					'{Currency}' as CURRENCY,
					'{CurrencyRecordId}' as CURRENCY_RECORD_ID,
					'ZCB1' as ITEM_TYPE,
					'Active' as ITEM_STATUS,
					0 as NET_VALUE,
					MAMTRL.UNIT_OF_MEASURE, 
					MAMTRL.UOM_RECORD_ID,
					MAMSOP.PLANT_RECORD_ID,
					MAMSOP.PLANT_ID,
					'ACQUIRING' AS PRICING_STATUS,
					SAQTMT.CONTRACT_VALID_FROM as LINE_ITEM_FROM_DATE,
					SAQTMT.CONTRACT_VALID_TO as LINE_ITEM_TO_DATE,
					MAMSCT.TAXCATEGORY_RECORD_ID,
					MAMSCT.TAXCATEGORY_DESCRIPTION, 
					MAMSCT.TAXCATEGORY_ID, 
					MAMSCT.TAXCLASSIFICATION_DESCRIPTION,
					MAMSCT.TAXCLASSIFICATION_ID,
					MAMSCT.TAXCLASSIFICATION_RECORD_ID,
					SAQTRV.DOC_CURRENCY,
					SAQTRV.DOCCURR_RECORD_ID,
					'' as QUOTE_CURRENCY,
					'' as QUOTE_CURRENCY_RECORD_ID,
					SAQTRV.GLOBAL_CURRENCY,
					SAQTRV.GLOBAL_CURRENCY_RECORD_ID,
					PRCFVA.FACTOR_PCTVAR as YEAR_OVER_YEAR
					FROM SAQSCE (NOLOCK)    
					JOIN (
						SELECT SAQSCE.QUOTE_RECORD_ID, SAQSCE.SERVICE_RECORD_ID, SAQSCE.ENTITLEMENT_GROUP_ID, MAX(CpqTableEntryId) as CpqTableEntryId, CAST(ROW_NUMBER()OVER(ORDER BY SAQSCE.ENTITLEMENT_GROUP_ID) + {ExistingCount} AS DECIMAL(5,1)) AS LINE_ITEM_ID FROM SAQSCE (NOLOCK) 
						WHERE SAQSCE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCE.QTEREV_RECORD_ID = '{RevisionRecordId}' {WhereString}
						GROUP BY SAQSCE.QUOTE_RECORD_ID, SAQSCE.SERVICE_RECORD_ID, SAQSCE.ENTITLEMENT_GROUP_ID
					) AS IQ ON IQ.CpqTableEntryId = SAQSCE.CpqTableEntryId
					JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQSCE.QUOTE_RECORD_ID  AND SAQTMT.QTEREV_RECORD_ID = SAQSCE.QTEREV_RECORD_ID          
					JOIN MAMTRL (NOLOCK) ON MAMTRL.SAP_PART_NUMBER = SAQSCE.SERVICE_ID 
					JOIN SAQTRV (NOLOCK) ON SAQTRV.SALESORG_RECORD_ID = SAQSCE.SALESORG_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = SAQSCE.QTEREV_RECORD_ID AND SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID
					LEFT JOIN MAMSCT (NOLOCK) ON SAQTRV.DISTRIBUTIONCHANNEL_RECORD_ID = MAMSCT.DISTRIBUTIONCHANNEL_RECORD_ID AND SAQTRV.COUNTRY_RECORD_ID = MAMSCT.COUNTRY_RECORD_ID AND SAQTRV.DIVISION_ID = MAMSCT.DIVISION_ID  
					LEFT JOIN MAMSOP (NOLOCK) ON MAMSOP.SAP_PART_NUMBER = MAMTRL.SAP_PART_NUMBER AND MAMSOP.SALESORG_ID = SAQSCE.SALESORG_ID					
					LEFT JOIN PRCFVA (NOLOCK) ON PRCFVA.FACTOR_VARIABLE_ID = SAQSCE.SERVICE_ID AND PRCFVA.FACTOR_ID = 'YOYDIS'
					WHERE SAQSCE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCE.QTEREV_RECORD_ID = '{RevisionRecordId}'{WhereString}
			""".format(						
				Currency=self.contract_currency,
				CurrencyRecordId=self.contract_currency_record_id,
				QuoteRecordId=self.contract_quote_record_id,
				RevisionRecordId=self.quote_revision_record_id,
				UserId=self.user_id,
				UserName=self.user_name,
				WhereString=where_string,
				ExistingCount=max_quote_item_count
			))
		# Insert SAQITM - End
		return True
	
	def _quote_item_lines_insert_process(self, where_string='', join_string='', quote_item_line_temp='', price_temp=''):
		##inserting SAQICO except chamber based equipment A055S000P01-6826
		entitlement_join = """LEFT JOIN (
						SELECT QUOTE_ID, EQUIPMENT_ID, SERVICE_ID, SUM(CASE WHEN Isnumeric(ENTITLEMENT_PRICE_IMPACT) = 1 THEN CONVERT(DECIMAL(18,2),ENTITLEMENT_PRICE_IMPACT) ELSE 0 END) * 1 AS TARGET_PRICE, SUM(CASE WHEN Isnumeric(ENTITLEMENT_COST_IMPACT) = 1 THEN CONVERT(DECIMAL(18,2),ENTITLEMENT_COST_IMPACT) ELSE 0 END) AS TOTAL_COST, SUM(CASE WHEN Isnumeric(ENTITLEMENT_PRICE_IMPACT) = 1 THEN CASE WHEN ENTITLEMENT_NAME LIKE 'AGS_LAB_OPT%_P%' THEN CONVERT(DECIMAL(18,2),ENTITLEMENT_PRICE_IMPACT) ELSE 0 END ELSE 0 END) AS YEAR_2, SUM(CASE WHEN Isnumeric(ENTITLEMENT_PRICE_IMPACT) = 1 THEN CASE WHEN ENTITLEMENT_NAME NOT LIKE 'AGS_LAB_OPT%_P%' THEN CONVERT(DECIMAL(18,2),ENTITLEMENT_PRICE_IMPACT) ELSE 0 END ELSE 0 END) AS YEAR_1 from (SELECT * FROM {PriceTemp}) IQ GROUP BY QUOTE_ID, EQUIPMENT_ID, SERVICE_ID
					) SAQSCE_TEMP ON SAQSCE_TEMP.QUOTE_ID = SAQSCO.QUOTE_ID AND SAQSCE_TEMP.EQUIPMENT_ID = SAQSCO.EQUIPMENT_ID AND SAQSCE_TEMP.SERVICE_ID = SAQSCO.SERVICE_ID""".format(PriceTemp=price_temp)
		self._process_query("""INSERT SAQICO (BD_PRICE,ENTITLEMENT_PRICE_IMPACT,ENTITLEMENT_COST_IMPACT, EQUIPMENT_DESCRIPTION,STATUS,EQUIPMENT_ID, EQUIPMENT_RECORD_ID, FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, LINE_ITEM_ID, MATERIAL_RECORD_ID, PLATFORM, QUOTE_ID, QTEITM_RECORD_ID, QUOTE_NAME, QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID, NET_PRICE, SAP_PART_NUMBER, SERIAL_NO, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, WAFER_SIZE, TARGET_PRICE, TECHNOLOGY,SRVTAXCAT_RECORD_ID,SRVTAXCAT_DESCRIPTION,SRVTAXCAT_ID,SRVTAXCLA_DESCRIPTION,SRVTAXCLA_ID,SRVTAXCLA_RECORD_ID, BD_DISCOUNT, BD_DISCOUNT_RECORD_ID, BD_PRICE_MARGIN, BD_PRICE_MARGIN_RECORD_ID, CEILING_PRICE, CLEANING_COST, CM_PART_COST, CUSTOMER_TOOL_ID, EQUIPMENTCATEGORY_ID, EQUIPMENTCATEGORY_RECORD_ID, EQUIPMENT_STATUS, KPI_COST, LABOR_COST, MNT_PLANT_ID, MNT_PLANT_NAME, MNT_PLANT_RECORD_ID, PM_PART_COST, SLSDIS_PRICE_MARGIN_RECORD_ID, SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID, TARGET_PRICE_MARGIN, TARGET_PRICE_MARGIN_RECORD_ID, WARRANTY_END_DATE, WARRANTY_START_DATE, GREENBOOK, GREENBOOK_RECORD_ID, EQUIPMENT_LINE_ID, NET_VALUE, SALES_DISCOUNT_PRICE, YEAR_1, YEAR_2, YEAR_3, YEAR_4, YEAR_5, EQUIPMENT_QUANTITY, YEAR_OVER_YEAR, EXCHANGE_RATE, EXCHANGE_RATE_DATE, EXCHANGE_RATE_RECORD_ID,GLOBAL_CURRENCY,DOC_CURRENCY,DOCURR_RECORD_ID, GLOBAL_CURRENCY_RECORD_ID, LINE, QUOTE_ITEM_COVERED_OBJECT_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified)
				SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_COVERED_OBJECT_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED,{UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
				SELECT DISTINCT
					SAQICO.BD_PRICE as BD_PRICE,
					0 as ENTITLEMENT_PRICE_IMPACT,
					0 AS ENTITLEMENT_COST_IMPACT,
					SAQSCO.EQUIPMENT_DESCRIPTION,
					'ACQUIRING' AS STATUS,
					SAQSCO.EQUIPMENT_ID,
					SAQSCO.EQUIPMENT_RECORD_ID,                        
					SAQSCO.FABLOCATION_ID, 
					SAQSCO.FABLOCATION_NAME, 
					SAQSCO.FABLOCATION_RECORD_ID,
					SAQITM.LINE_ITEM_ID as LINE_ITEM_ID,
					SAQSCO.MATERIAL_RECORD_ID,
					SAQSCO.PLATFORM,
					SAQSCO.QUOTE_ID, 
					SAQITM.QUOTE_ITEM_RECORD_ID as QTEITM_RECORD_ID, 
					SAQSCO.QUOTE_NAME, 
					SAQSCO.QUOTE_RECORD_ID,
					SAQSCO.QTEREV_ID,
					SAQSCO.QTEREV_RECORD_ID,
					SAQICO.NET_PRICE as NET_PRICE,
					SAQSCO.SAP_PART_NUMBER, 
					SAQSCO.SERIAL_NO, 
					SAQSCO.SERVICE_DESCRIPTION, 
					SAQSCO.SERVICE_ID, 
					SAQSCO.SERVICE_RECORD_ID, 
					SAQSCO.WAFER_SIZE,
					CASE WHEN MAMTRL.SAP_PART_NUMBER LIKE '%Z0007%'  
							THEN  null
							ELSE  0
					END as TARGET_PRICE,
					SAQSCO.TECHNOLOGY,  
					SAQITM.SRVTAXCAT_RECORD_ID,
					SAQITM.SRVTAXCAT_DESCRIPTION,
					SAQITM.SRVTAXCAT_ID,
					SAQITM.SRVTAXCLA_DESCRIPTION,
					SAQITM.SRVTAXCLA_ID,
					SAQITM.SRVTAXCLA_RECORD_ID,
					null as BD_DISCOUNT, 
					null as BD_DISCOUNT_RECORD_ID, 
					SAQICO.BD_PRICE_MARGIN as BD_MARGIN, 
					SAQICO.BD_PRICE_MARGIN_RECORD_ID as BD_MARGIN_RECORD_ID, 
					SAQICO.CEILING_PRICE as CEILING_PRICE, 
					SAQICO.CLEANING_COST as CLEANING_COST,
					SAQICO.CM_PART_COST as CM_PART_COST, 
					SAQSCO.CUSTOMER_TOOL_ID, 
					SAQSCO.EQUIPMENTCATEGORY_ID, 
					SAQSCO.EQUIPMENTCATEGORY_RECORD_ID, 
					SAQSCO.EQUIPMENT_STATUS, 
					SAQICO.KPI_COST as KPI_COST, 
					SAQICO.LABOR_COST as LABOR_COST, 
					SAQSCO.MNT_PLANT_ID, 
					SAQSCO.MNT_PLANT_NAME, 
					SAQSCO.MNT_PLANT_RECORD_ID,
					SAQICO.PM_PART_COST as PM_PART_COST,
					null as SLSDIS_PRICE_MARGIN_RECORD_ID, 
					SAQSCO.SALESORG_ID, 
					SAQSCO.SALESORG_NAME, 
					SAQSCO.SALESORG_RECORD_ID, 
					SAQICO.TARGET_PRICE_MARGIN as TARGET_MARGIN, 
					SAQICO.TARGET_PRICE_MARGIN_RECORD_ID as TARGET_MARGIN_THRESHOLD_RECORD_ID,
					SAQSCO.WARRANTY_END_DATE, 
					SAQSCO.WARRANTY_START_DATE, 
					SAQSCO.GREENBOOK, 
					SAQSCO.GREENBOOK_RECORD_ID, 
					CASE WHEN MAMTRL.SERVICE_TYPE = 'NON TOOL BASED' 
							THEN CONVERT(INT, CONVERT(DECIMAL,SAQITM.LINE_ITEM_ID)) * 10 
							ELSE ROW_NUMBER()OVER(ORDER BY(SAQSCO.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID)) * 10 
					END as EQUIPMENT_LINE_ID,
					
					0 as NET_VALUE, 
					null as SALE_DISCOUNT_PRICE, 
					CASE WHEN MAMTRL.SAP_PART_NUMBER LIKE '%Z0007%' 
							THEN  0
							ELSE  0
					END as YEAR_1,          
					CASE WHEN MAMTRL.SAP_PART_NUMBER LIKE '%Z0007%' 
							THEN  0
							ELSE  0
					END as YEAR_2,    
					null as YEAR_3,       
					null as YEAR_4,    
					null as YEAR_5,
					null as EQUIPMENT_QUANTITY,
					SAQITM.YEAR_OVER_YEAR,
					SAQTRV.EXCHANGE_RATE,
					SAQTRV.EXCHANGE_RATE_DATE,
					SAQTRV.EXCHANGERATE_RECORD_ID as EXCHANGE_RATE_RECORD_ID,
					SAQTRV.GLOBAL_CURRENCY,
					SAQTRV.DOC_CURRENCY,
					SAQTRV.DOCCURR_RECORD_ID,
					SAQTRV.GLOBAL_CURRENCY_RECORD_ID,
					SAQITM.LINE_ITEM_ID + '.'+ CAST(ROW_NUMBER()OVER(PARTITION BY SAQITM.LINE_ITEM_ID ORDER BY(SAQSCO.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID)) AS varchar ) as LINE
				FROM 
					SAQSCO (NOLOCK)					 
					JOIN SAQSCE (NOLOCK) ON SAQSCE.QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID AND SAQSCE.SERVICE_ID = SAQSCO.SERVICE_ID AND SAQSCE.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID
					AND SAQSCE.EQUIPMENT_RECORD_ID = SAQSCO.EQUIPMENT_RECORD_ID 
					JOIN MAMTRL (NOLOCK) ON MAMTRL.SAP_PART_NUMBER = SAQSCE.SERVICE_ID
					LEFT JOIN {TempTable} SAQICO (NOLOCK) ON SAQICO.QUOTE_RECORD_ID = SAQSCE.QUOTE_RECORD_ID AND SAQICO.SERVICE_ID = SAQSCE.SERVICE_ID AND SAQICO.EQUIPMENT_RECORD_ID = SAQSCE.EQUIPMENT_RECORD_ID AND SAQICO.QTEREV_RECORD_ID = SAQSCE.QTEREV_RECORD_ID 
					JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID  AND SAQTMT.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID         
					JOIN SAQTRV (NOLOCK) ON SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID 
					JOIN SAQITM (NOLOCK) ON SAQTRV.QUOTE_RECORD_ID = SAQITM.QUOTE_RECORD_ID 
											AND SAQITM.SERVICE_RECORD_ID = SAQSCO.SERVICE_RECORD_ID
											AND SAQITM.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID
											{JoinString}
					{EntitlementJoinString}
					
				WHERE 
					SAQSCO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCO.QTEREV_RECORD_ID = '{RevisionRecordId}'{WhereString}  AND ISNULL(SAQSCO.INCLUDED,'') != 'CHAMBER'
				) IQ
				""".format(UserId=self.user_id, UserName=self.user_name, QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id,
				TempTable=quote_item_line_temp, JoinString=join_string, EntitlementJoinString=entitlement_join if 'Z0016' in where_string else '', WhereString=where_string )
			)
		
		##inserting assembly to SAQICO if a equipemnt is chamber based FTS A055S000P01-6826
		if self.sale_type == 'TOOL RELOCATION':
			
			self._process_query("""INSERT SAQICO (BD_PRICE,ENTITLEMENT_PRICE_IMPACT,ENTITLEMENT_COST_IMPACT, EQUIPMENT_DESCRIPTION,STATUS,EQUIPMENT_ID, EQUIPMENT_RECORD_ID, FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, LINE_ITEM_ID, MATERIAL_RECORD_ID, PLATFORM, QUOTE_ID, QTEITM_RECORD_ID, QUOTE_NAME, QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID, NET_PRICE, SAP_PART_NUMBER, SERIAL_NO, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, WAFER_SIZE, TARGET_PRICE, TECHNOLOGY,SRVTAXCAT_RECORD_ID,SRVTAXCAT_DESCRIPTION,SRVTAXCAT_ID,SRVTAXCLA_DESCRIPTION,SRVTAXCLA_ID,SRVTAXCLA_RECORD_ID, BD_DISCOUNT, BD_DISCOUNT_RECORD_ID, BD_PRICE_MARGIN, BD_PRICE_MARGIN_RECORD_ID, CEILING_PRICE, CLEANING_COST, CM_PART_COST, CUSTOMER_TOOL_ID, EQUIPMENTCATEGORY_ID, EQUIPMENTCATEGORY_RECORD_ID, EQUIPMENT_STATUS, KPI_COST, LABOR_COST, MNT_PLANT_ID, MNT_PLANT_NAME, MNT_PLANT_RECORD_ID, PM_PART_COST, SLSDIS_PRICE_MARGIN_RECORD_ID, SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID, TARGET_PRICE_MARGIN, TARGET_PRICE_MARGIN_RECORD_ID, WARRANTY_END_DATE, WARRANTY_START_DATE, GREENBOOK, GREENBOOK_RECORD_ID, EQUIPMENT_LINE_ID, NET_VALUE, SALES_DISCOUNT_PRICE, YEAR_1, YEAR_2, YEAR_3, YEAR_4, YEAR_5, EQUIPMENT_QUANTITY, YEAR_OVER_YEAR, EXCHANGE_RATE, EXCHANGE_RATE_DATE, EXCHANGE_RATE_RECORD_ID,GLOBAL_CURRENCY,DOC_CURRENCY,DOCURR_RECORD_ID, GLOBAL_CURRENCY_RECORD_ID, LINE,ASSEMBLY_ID,ASSEMBLY_RECORD_ID, QUOTE_ITEM_COVERED_OBJECT_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified)
					SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_COVERED_OBJECT_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED,{UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
					SELECT DISTINCT
						SAQICO.BD_PRICE as BD_PRICE,
						0 as ENTITLEMENT_PRICE_IMPACT,
						0 AS ENTITLEMENT_COST_IMPACT,
						SAQSCO.EQUIPMENT_DESCRIPTION,
						'ACQUIRING' AS STATUS,
						SAQSCO.EQUIPMENT_ID,
						SAQSCO.EQUIPMENT_RECORD_ID,                        
						SAQSCO.FABLOCATION_ID, 
						SAQSCO.FABLOCATION_NAME, 
						SAQSCO.FABLOCATION_RECORD_ID,
						SAQITM.LINE_ITEM_ID as LINE_ITEM_ID,
						SAQSCO.MATERIAL_RECORD_ID,
						SAQSCO.PLATFORM,
						SAQSCO.QUOTE_ID, 
						SAQITM.QUOTE_ITEM_RECORD_ID as QTEITM_RECORD_ID, 
						SAQSCO.QUOTE_NAME, 
						SAQSCO.QUOTE_RECORD_ID,
						SAQSCO.QTEREV_ID,
						SAQSCO.QTEREV_RECORD_ID,
						SAQICO.NET_PRICE as NET_PRICE,
						SAQSCO.SAP_PART_NUMBER, 
						SAQSCO.SERIAL_NO, 
						SAQSCO.SERVICE_DESCRIPTION, 
						SAQSCO.SERVICE_ID, 
						SAQSCO.SERVICE_RECORD_ID, 
						SAQSCO.WAFER_SIZE,
						CASE WHEN MAMTRL.SAP_PART_NUMBER LIKE '%Z0007%'  
								THEN  null
								ELSE  0
						END as TARGET_PRICE,
						SAQSCO.TECHNOLOGY, 
						SAQITM.SRVTAXCAT_RECORD_ID,
						SAQITM.SRVTAXCAT_DESCRIPTION,
						SAQITM.SRVTAXCAT_ID,
						SAQITM.SRVTAXCLA_DESCRIPTION,
						SAQITM.SRVTAXCLA_ID,
						SAQITM.SRVTAXCLA_RECORD_ID,
						null as BD_DISCOUNT, 
						null as BD_DISCOUNT_RECORD_ID, 
						SAQICO.BD_PRICE_MARGIN as BD_MARGIN, 
						SAQICO.BD_PRICE_MARGIN_RECORD_ID as BD_MARGIN_RECORD_ID, 
						SAQICO.CEILING_PRICE as CEILING_PRICE, 
						SAQICO.CLEANING_COST as CLEANING_COST,
						SAQICO.CM_PART_COST as CM_PART_COST, 
						SAQSCO.CUSTOMER_TOOL_ID, 
						SAQSCO.EQUIPMENTCATEGORY_ID, 
						SAQSCO.EQUIPMENTCATEGORY_RECORD_ID, 
						SAQSCO.EQUIPMENT_STATUS, 
						SAQICO.KPI_COST as KPI_COST, 
						SAQICO.LABOR_COST as LABOR_COST, 
						SAQSCO.MNT_PLANT_ID, 
						SAQSCO.MNT_PLANT_NAME, 
						SAQSCO.MNT_PLANT_RECORD_ID,
						SAQICO.PM_PART_COST as PM_PART_COST, 
						null as SLSDIS_PRICE_MARGIN_RECORD_ID, 
						SAQSCO.SALESORG_ID, 
						SAQSCO.SALESORG_NAME, 
						SAQSCO.SALESORG_RECORD_ID, 
						SAQICO.TARGET_PRICE_MARGIN as TARGET_MARGIN, 
						SAQICO.TARGET_PRICE_MARGIN_RECORD_ID as TARGET_MARGIN_THRESHOLD_RECORD_ID,
						SAQSCO.WARRANTY_END_DATE, 
						SAQSCO.WARRANTY_START_DATE, 
						SAQSCO.GREENBOOK, 
						SAQSCO.GREENBOOK_RECORD_ID, 
						CASE WHEN MAMTRL.SERVICE_TYPE = 'NON TOOL BASED' 
								THEN CONVERT(INT, CONVERT(DECIMAL,SAQITM.LINE_ITEM_ID)) * 10 
								ELSE ROW_NUMBER()OVER(ORDER BY(SAQSCO.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID)) * 10 
						END as EQUIPMENT_LINE_ID,
						
						0 as NET_VALUE, 
						null as SALE_DISCOUNT_PRICE, 
						CASE WHEN MAMTRL.SAP_PART_NUMBER LIKE '%Z0007%' 
								THEN  0
								ELSE  0
						END as YEAR_1,          
						CASE WHEN MAMTRL.SAP_PART_NUMBER LIKE '%Z0007%' 
								THEN  0
								ELSE  0
						END as YEAR_2,    
						null as YEAR_3,       
						null as YEAR_4,    
						null as YEAR_5,
						null as EQUIPMENT_QUANTITY,
						SAQITM.YEAR_OVER_YEAR,
						SAQTRV.EXCHANGE_RATE,
						SAQTRV.EXCHANGE_RATE_DATE,
						SAQTRV.EXCHANGERATE_RECORD_ID as EXCHANGE_RATE_RECORD_ID,
						SAQTRV.GLOBAL_CURRENCY,
						SAQTRV.DOC_CURRENCY,
						SAQTRV.DOCCURR_RECORD_ID,
						SAQTRV.GLOBAL_CURRENCY_RECORD_ID,
						SAQITM.LINE_ITEM_ID + '.'+ CAST(ROW_NUMBER()OVER(PARTITION BY SAQITM.LINE_ITEM_ID ORDER BY(SAQSCO.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID)) AS varchar ) as LINE,
						SAQSCA.ASSEMBLY_ID as ASSEMBLY_ID,
						SAQSCA.ASSEMBLY_RECORD_ID as ASSEMBLY_RECORD_ID
					FROM 
						SAQSCO (NOLOCK)					 
						JOIN SAQSCE (NOLOCK) ON SAQSCE.QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID AND SAQSCE.SERVICE_ID = SAQSCO.SERVICE_ID AND SAQSCE.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID
												AND SAQSCE.EQUIPMENT_RECORD_ID = SAQSCO.EQUIPMENT_RECORD_ID
						JOIN MAMTRL (NOLOCK) ON MAMTRL.SAP_PART_NUMBER = SAQSCE.SERVICE_ID
						JOIN SAQSCA (NOLOCK) ON SAQSCA.QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID AND SAQSCA.SERVICE_ID = SAQSCO.SERVICE_ID AND SAQSCA.EQUIPMENT_RECORD_ID = SAQSCO.EQUIPMENT_RECORD_ID
						AND SAQSCA.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID
						LEFT JOIN {TempTable} SAQICO (NOLOCK) ON SAQICO.QUOTE_RECORD_ID = SAQSCE.QUOTE_RECORD_ID AND SAQICO.SERVICE_ID = SAQSCE.SERVICE_ID AND SAQICO.EQUIPMENT_RECORD_ID = SAQSCE.EQUIPMENT_RECORD_ID  AND SAQICO.QTEREV_RECORD_ID = SAQSCE.QTEREV_RECORD_ID AND SAQSCA.ASSEMBLY_RECORD_ID = SAQICO.ASSEMBLY_RECORD_ID AND SAQSCA.QTEREV_RECORD_ID = SAQICO.QTEREV_RECORD_ID
						JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID  AND SAQTMT.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID       
						JOIN SAQTRV (NOLOCK) ON SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID  AND SAQTRV.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID 
						JOIN SAQITM (NOLOCK) ON SAQTRV.QUOTE_RECORD_ID = SAQITM.QUOTE_RECORD_ID 
												AND SAQITM.SERVICE_RECORD_ID = SAQSCO.SERVICE_RECORD_ID
												AND SAQITM.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID
												{JoinString}
						{EntitlementJoinString}
						
					WHERE 
						SAQSCO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCO.QTEREV_RECORD_ID = '{RevisionRecordId}' {WhereString}  AND ISNULL(SAQSCO.INCLUDED,'') = 'CHAMBER' AND SAQSCA.INCLUDED = 1
					) IQ
					""".format(UserId=self.user_id, UserName=self.user_name, QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id, 
					TempTable=quote_item_line_temp, JoinString=join_string, EntitlementJoinString=entitlement_join if 'Z0016' in where_string else '', WhereString= str(where_string) )
				)
			

		###Value Driver coefficient Sum up  A055S000P01-8778 starts
		self._process_query("UPDATE A  SET TOOL_VALUEDRIVER_COEFFICIENT = VALUEDRIVER_COEFFICIENT FROM SAQICO A(NOLOCK) JOIN (SELECT QUOTE_RECORD_ID,EQUIPMENT_ID,SERVICE_ID,SUM(VALUEDRIVER_COEFFICIENT) AS VALUEDRIVER_COEFFICIENT from SAQSCV(NOLOCK) WHERE QUOTE_RECORD_ID ='"+str(self.contract_quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"' GROUP BY QUOTE_RECORD_ID,EQUIPMENT_ID,SERVICE_ID) B ON A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.SERVICE_ID = B.SERVICE_ID")
    	##A055S000P01-8778 ends

		###Updating pricing picklist value in line item subtab A055S000P01-4578
		Quote.GetCustomField('PRICING_PICKLIST').Content = 'Global Currency'
		
		return True
	
	def _quote_items_insert(self):
		## Delete SAQICO, SAQITM  and native quote items - Start		
		# Temp table creation and delete(if altready there) for SAQICO - Start
		temp_table = "SAQICO_BKP_"+str(self.c4c_quote_id)
		temp_table_drop = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(temp_table)+"'' ) BEGIN DROP TABLE "+str(temp_table)+" END  ' ")
		SqlHelper.GetFirst("sp_executesql @T=N'SELECT * INTO "+str(temp_table)+" FROM SAQICO(NOLOCK) WHERE QUOTE_RECORD_ID = ''"+str(self.contract_quote_record_id)+"'' AND QTEREV_RECORD_ID = ''"+str(self.quote_revision_record_id)+"''' ")
		# Temp table creation and delete(if altready there) for SAQICO - End

		#Temp table for storing price and cost impact
		price_temp = "SAQSCE_BKP_"+str(self.c4c_quote_id)
		price_temp_drop = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(price_temp)+"'' ) BEGIN DROP TABLE "+str(price_temp)+" END  ' ")
		SqlHelper.GetFirst("sp_executesql @T=N'declare @H int; Declare @val Varchar(MAX);DECLARE @XML XML; SELECT @val =  replace(replace(STUFF((SELECT ''''+FINAL from(select  REPLACE(entitlement_xml,''<QUOTE_ITEM_ENTITLEMENT>'',sml) AS FINAL FROM (select ''  <QUOTE_ITEM_ENTITLEMENT><QUOTE_ID>''+quote_id+''</QUOTE_ID><SERVICE_ID>''+service_id+''</SERVICE_ID><EQUIPMENT_ID>''+equipment_id+''</EQUIPMENT_ID>'' AS sml,replace(entitlement_xml,''&'','';#38'')  as entitlement_xml from SAQSCE(nolock) where quote_record_id=''"+str(self.contract_quote_record_id)+"'' )A )a FOR XML PATH ('''')), 1, 1, ''''),''&lt;'',''<''),''&gt;'',''>'')  SELECT @XML = CONVERT(XML,''<ROOT>''+@VAL+''</ROOT>'') exec sys.sp_xml_preparedocument @H output,@XML; select QUOTE_ID,EQUIPMENT_ID,SERVICE_ID,ENTITLEMENT_NAME,ENTITLEMENT_COST_IMPACT,ENTITLEMENT_PRICE_IMPACT INTO "+str(price_temp)+"  from openxml(@H, ''ROOT/QUOTE_ITEM_ENTITLEMENT'', 0) with (QUOTE_ID VARCHAR(100) ''QUOTE_ID'',EQUIPMENT_ID VARCHAR(100) ''EQUIPMENT_ID'',ENTITLEMENT_NAME VARCHAR(100) ''ENTITLEMENT_NAME'',SERVICE_ID VARCHAR(100) ''SERVICE_ID'',ENTITLEMENT_COST_IMPACT VARCHAR(100) ''ENTITLEMENT_COST_IMPACT'',ENTITLEMENT_PRICE_IMPACT VARCHAR(100) ''ENTITLEMENT_PRICE_IMPACT'') ; exec sys.sp_xml_removedocument @H; '")
		#SqlHelper.GetFirst("sp_executesql @T=N'CREATE TABLE  "+str(price_temp)+" (TARGET_PRICE DECIMAL(18,5),TOTAL_COST DECIMAL(18,5),YEAR_2 DECIMAL(18,5),YEAR_1 DECIMAL(18,5),EQUIPMENT_ID VARCHAR(10), EQUIPMENT_RECORD_ID VARCHAR(50), QUOTE_RECORD_ID VARCHAR(50))'")

		#Sql.RunQuery("INSERT "+str(price_temp)+" (QUOTE_RECORD_ID, EQUIPMENT_RECORD_ID, EQUIPMENT_ID, TARGET_PRICE, TOTAL_COST, YEAR_2, YEAR_1) select QUOTE_RECORD_ID, EQUIPMENT_RECORD_ID, EQUIPMENT_ID, SUM(CASE WHEN Isnumeric(ENTITLEMENT_PRICE_IMPACT) = 1 THEN CONVERT(DECIMAL(18,2),ENTITLEMENT_PRICE_IMPACT) ELSE 0 END) * 1 AS ENTITLEMENT_PRICE_IMPACT, SUM(CASE WHEN Isnumeric(ENTITLEMENT_COST_IMPACT) = 1 THEN CONVERT(DECIMAL(18,2),ENTITLEMENT_COST_IMPACT) ELSE 0 END) AS ENTITLEMENT_COST_IMPACT, SUM(CASE WHEN Isnumeric(ENTITLEMENT_PRICE_IMPACT) = 1 THEN CASE WHEN ENTITLEMENT_NAME LIKE 'AGS_LAB_OPT%_P%' THEN CONVERT(DECIMAL(18,2),ENTITLEMENT_PRICE_IMPACT) ELSE 0 END ELSE 0 END) AS YEAR_2, SUM(CASE WHEN Isnumeric(ENTITLEMENT_PRICE_IMPACT) = 1 THEN CASE WHEN ENTITLEMENT_NAME NOT LIKE 'AGS_LAB_OPT%_P%' THEN CONVERT(DECIMAL(18,2),ENTITLEMENT_PRICE_IMPACT) ELSE 0 END ELSE 0 END) AS YEAR_1 from (SELECT distinct e.QUOTE_RECORD_ID, e.EQUIPMENT_RECORD_ID, e.EQUIPMENT_ID ,replace(X.Y.value('(ENTITLEMENT_COST_IMPACT)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_COST_IMPACT,replace(X.Y.value('(ENTITLEMENT_NAME)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_NAME,replace(X.Y.value('(ENTITLEMENT_PRICE_IMPACT)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_PRICE_IMPACT FROM (select SAQSCE.QUOTE_RECORD_ID as QUOTE_RECORD_ID, SAQSCE.EQUIPMENT_RECORD_ID, SAQSCE.EQUIPMENT_ID, CONVERT(xml, replace(cast(SAQSCE.ENTITLEMENT_XML as varchar(max)),'&','&amp;'), 2) as ENTITLEMENT_XML FROM SAQSCE (NOLOCK) WHERE QUOTE_RECORD_ID = '"+str(self.contract_quote_record_id)+"') e OUTER APPLY e.ENTITLEMENT_XML.nodes('QUOTE_ITEM_ENTITLEMENT') as X(Y) ) IQ GROUP BY QUOTE_RECORD_ID, EQUIPMENT_RECORD_ID, EQUIPMENT_ID")
		
		for table_name in ('SAQICO', 'SAQITM'):
			delete_query = "DELETE FROM {ObjectName} WHERE QUOTE_RECORD_ID = '{ContractQuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' {WhereCondition}".format(
					ObjectName=table_name, ContractQuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id, WhereCondition='',
				)
			self._process_query(delete_query)
		for item in Quote.MainItems:
			item.Delete()
		## Delete SAQICO, SAQITM  and native quote items - End
		# Non tool base quote item insert
		services_obj = Sql.GetList("SELECT SAQTSV.SERVICE_ID FROM SAQTSV (NOLOCK) JOIN MAMTRL (NOLOCK) ON MAMTRL.SAP_PART_NUMBER = SAQTSV.SERVICE_ID AND MAMTRL.SERVICE_TYPE = 'NON TOOL BASED' WHERE SAQTSV.QUOTE_RECORD_id = '{QuoteRecordId}' AND SAQTSV.QTEREV_RECORD_ID = '{RevisionRecordId}'".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id))
		if services_obj:
			item_where_string = "AND SAQSCE.SERVICE_ID IN ('{}')".format("','".join([service_obj.SERVICE_ID for service_obj in services_obj]))
			# Insert SAQITM - Start
			self._quote_item_insert_process(where_string=item_where_string)
			# Insert SAQITM - End
			# Insert Quote Items Covered Object - Start
			item_line_where_string = "AND SAQSCO.SERVICE_ID IN ('{}')".format("','".join([service_obj.SERVICE_ID for service_obj in services_obj]))
			if self.sale_type == 'TOOL RELOCATION':
				item_line_where_string += " AND SAQSCO.FABLOCATION_ID IS NOT NULL AND SAQSCO.FABLOCATION_ID != '' "
			join_string = "AND SAQITM.LINE_ITEM_ID = CAST(ISNULL(SAQSCE.ENTITLEMENT_GROUP_ID,'1.1') AS DECIMAL(5,1))"
			self._quote_item_lines_insert_process(where_string=item_line_where_string, join_string=join_string, quote_item_line_temp=temp_table, price_temp=price_temp)
			#(select SUM(CASE WHEN Isnumeric(ENTITLEMENT_PRICE_IMPACT) = 1 THEN CONVERT(DECIMAL(18,2),ENTITLEMENT_PRICE_IMPACT) ELSE 0 END) AS ENTITLEMENT_PRICE_IMPACT from (SELECT distinct replace(X.Y.value('(ENTITLEMENT_PRICE_IMPACT)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_PRICE_IMPACT FROM (select convert(xml,replace(replace(SAQSCE.ENTITLEMENT_XML,'&',';#38'),'''',';#39')) as ENTITLEMENT_XML ) e OUTER APPLY e.ENTITLEMENT_XML.nodes('QUOTE_ITEM_ENTITLEMENT') as X(Y)) IQ) * ISNULL(SAQTSO.EXCHANGE_RATE, 1)
			#(select SUM(CASE WHEN Isnumeric(ENTITLEMENT_COST_IMPACT) = 1 THEN CONVERT(DECIMAL(18,2),ENTITLEMENT_COST_IMPACT) ELSE 0 END) AS ENTITLEMENT_COST_IMPACT from (SELECT distinct replace(X.Y.value('(ENTITLEMENT_COST_IMPACT)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_COST_IMPACT FROM (select convert(xml,replace(replace(SAQSCE.ENTITLEMENT_XML,'&',';#38'),'''',';#39')) as ENTITLEMENT_XML ) e OUTER APPLY e.ENTITLEMENT_XML.nodes('QUOTE_ITEM_ENTITLEMENT') as X(Y)) IQ)
			# Insert Quote Items Covered Object - End
		
		# Tool base quote item insert
		services_obj = Sql.GetList("SELECT SAQTSV.SERVICE_ID FROM SAQTSV (NOLOCK) JOIN MAMTRL (NOLOCK) ON MAMTRL.SAP_PART_NUMBER = SAQTSV.SERVICE_ID AND MAMTRL.SERVICE_TYPE != 'NON TOOL BASED' WHERE SAQTSV.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQTSV.QTEREV_RECORD_ID = '{RevisionRecordId}'".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id))
		if services_obj:
			quote_item_obj = Sql.GetFirst("SELECT TOP 1 ISNULL(LINE_ITEM_ID, 0) AS LINE_ITEM_ID FROM SAQITM (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' ORDER BY LINE_ITEM_ID DESC".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id))
			item_where_string = "AND SAQSCE.SERVICE_ID IN ('{}')".format("','".join([service_obj.SERVICE_ID for service_obj in services_obj]))
			# Insert SAQITM - Start
			self._quote_item_insert_process(where_string=item_where_string, max_quote_item_count=int(float(quote_item_obj.LINE_ITEM_ID)) if quote_item_obj else 0)
			# Insert SAQITM - End
			# Insert Quote Items Covered Object - Start
			item_line_where_string = "AND SAQSCO.SERVICE_ID IN ('{}')".format("','".join([service_obj.SERVICE_ID for service_obj in services_obj]))
			if self.sale_type == 'TOOL RELOCATION':
				item_line_where_string += " AND SAQSCO.FABLOCATION_ID IS NOT NULL AND SAQSCO.FABLOCATION_ID != '' "
			self._quote_item_lines_insert_process(where_string=item_line_where_string, join_string='', quote_item_line_temp=temp_table, price_temp=price_temp)
			#(select SUM(CASE WHEN Isnumeric(ENTITLEMENT_PRICE_IMPACT) = 1 THEN CONVERT(DECIMAL(18,2),ENTITLEMENT_PRICE_IMPACT) ELSE 0 END) AS ENTITLEMENT_PRICE_IMPACT from (SELECT distinct replace(X.Y.value('(ENTITLEMENT_PRICE_IMPACT)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_PRICE_IMPACT FROM (select convert(xml,replace(replace(SAQSCE.ENTITLEMENT_XML,'&',';#38'),'''',';#39')) as ENTITLEMENT_XML ) e OUTER APPLY e.ENTITLEMENT_XML.nodes('QUOTE_ITEM_ENTITLEMENT') as X(Y)) IQ) * ISNULL(SAQTSO.EXCHANGE_RATE, 1)
			#(select SUM(CASE WHEN Isnumeric(ENTITLEMENT_COST_IMPACT) = 1 THEN CONVERT(DECIMAL(18,2),ENTITLEMENT_COST_IMPACT) ELSE 0 END) AS ENTITLEMENT_COST_IMPACT from (SELECT distinct replace(X.Y.value('(ENTITLEMENT_COST_IMPACT)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_COST_IMPACT FROM (select convert(xml,replace(replace(SAQSCE.ENTITLEMENT_XML,'&',';#38'),'''',';#39')) as ENTITLEMENT_XML ) e OUTER APPLY e.ENTITLEMENT_XML.nodes('QUOTE_ITEM_ENTITLEMENT') as X(Y)) IQ)
			# Insert Quote Items Covered Object - End

		# Native Cart Items Insert - Start
		quote_items_obj = Sql.GetList("""SELECT TOP 1000 SAQTSV.SERVICE_ID FROM SAQITM (NOLOCK) JOIN SAQTSV (NOLOCK) ON SAQTSV.SERVICE_RECORD_ID = SAQITM.SERVICE_RECORD_ID AND SAQTSV.QUOTE_RECORD_ID = SAQITM.QUOTE_RECORD_ID AND SAQTSV.QTEREV_RECORD_ID = SAQITM.QTEREV_RECORD_ID WHERE SAQITM.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQITM.QTEREV_RECORD_ID = '{RevisionRecordId}' ORDER BY LINE_ITEM_ID ASC""".format(QuoteRecordId= self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id))
		for quote_item_obj in quote_items_obj:			
			#product_native_obj = ProductHelper.CreateProduct(str(grouped_item_obj.SERVICE_ID))
			#product_native_obj.AddToQuote()
			product_obj = Sql.GetFirst("SELECT MAX(PDS.PRODUCT_ID) AS PRD_ID,PDS.SYSTEM_ID,PDS.UnitOfMeasure,PDS.CART_DESCRIPTION_BUILDER,PDS.PRODUCT_NAME FROM PRODUCTS (NOLOCK) PDS INNER JOIN PRODUCT_VERSIONS (NOLOCK) PRVS ON  PDS.PRODUCT_ID = PRVS.PRODUCT_ID WHERE SYSTEM_ID ='{Partnumber}' GROUP BY PDS.SYSTEM_ID,PDS.UnitOfMeasure,PDS.CART_DESCRIPTION_BUILDER,PDS.PRODUCT_NAME".format(Partnumber = str(quote_item_obj.SERVICE_ID)) )
			if product_obj:
				temp_product = Quote.AddItem('vc_config_cpq')
				for product in temp_product:
					product.PartNumber = str(quote_item_obj.SERVICE_ID)
					product.Description = product_obj.PRODUCT_NAME
					product.QUOTE_ID.Value = self.contract_quote_id		
					product.QUOTE_RECORD_ID.Value = self.contract_quote_record_id
				Quote.Save()			
		# Native Cart Items Insert - End
		
		Sql.RunQuery("DELETE   FROM QT__SAQICD where QUOTE_ID = '"+str(self.contract_quote_id)+"'")		
		entries = str(self.contract_quote_id)
		revision = str(self.quote_revision_record_id)
		user = self.user_name		
		CQPARTIFLW.iflow_pricing_call(user,entries,revision)
		
		'''self._process_query("""UPDATE SAQICO SET PRICING_STATUS = CASE  
						WHEN ISNULL(TOTAL_COST, 0) > 0 THEN 'ACQUIRED'                        
						ELSE 'ERROR'
					END FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'""".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id))'''
		self._process_query("""UPDATE SAQICO
			SET
			SAQICO.ANNUAL_BENCHMARK_BOOKING_PRICE = PRPRBM.ANNUAL_BOOKING_PRICE,
			SAQICO.PRICE_BENCHMARK_TYPE = 'RENEWAL',
			SAQICO.TOOL_CONFIGURATION = PRPRBM.TOOL_CONFIGURATION,
			SAQICO.CONTRACT_ID = PRPRBM.CONTRACT_ID,
			SAQICO.CONTRACT_VALID_FROM = CONVERT(VARCHAR(10), PRPRBM.CONTRACT_VALID_FROM , 101),
			SAQICO.CONTRACT_VALID_TO = CONVERT(VARCHAR(10), PRPRBM.CONTRACT_VALID_TO, 101)					
			FROM SAQICO	(NOLOCK)
			JOIN (
				SELECT SAQICO.CpqTableEntryId, MAX(PRPRBM.CONTRACT_VALID_FROM) AS CONTRACT_VALID_FROM, PRPRBM.ACCOUNT_RECORD_ID,
						PRPRBM.EQUIPMENT_RECORD_ID, PRPRBM.SERVICE_RECORD_ID
				FROM SAQICO (NOLOCK)	
				JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQICO.QUOTE_RECORD_ID			AND SAQTMT.QTEREV_RECORD_ID = SAQICO.QTEREV_RECORD_ID		
				JOIN PRPRBM (NOLOCK) ON PRPRBM.ACCOUNT_RECORD_ID = SAQTMT.ACCOUNT_RECORD_ID AND PRPRBM.EQUIPMENT_RECORD_ID = SAQICO.EQUIPMENT_RECORD_ID
										AND PRPRBM.SERVICE_RECORD_ID = SAQICO.SERVICE_RECORD_ID				
				WHERE SAQICO.QUOTE_RECORD_ID ='{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{RevisionRecordId}'
				GROUP BY PRPRBM.ACCOUNT_RECORD_ID, PRPRBM.EQUIPMENT_RECORD_ID, PRPRBM.SERVICE_RECORD_ID, SAQICO.CpqTableEntryId
			)AS IQ ON SAQICO.CpqTableEntryId = IQ.CpqTableEntryId
			JOIN PRPRBM (NOLOCK) ON PRPRBM.ACCOUNT_RECORD_ID = IQ.ACCOUNT_RECORD_ID 
									AND PRPRBM.EQUIPMENT_RECORD_ID = IQ.EQUIPMENT_RECORD_ID
									AND PRPRBM.SERVICE_RECORD_ID = IQ.SERVICE_RECORD_ID
									AND PRPRBM.CONTRACT_VALID_FROM = IQ.CONTRACT_VALID_FROM								
			""".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id))
		
		self._process_query("""UPDATE SAQICO
			SET
			SAQICO.ANNUAL_BENCHMARK_BOOKING_PRICE = PRPRBM.ANNUAL_BOOKING_PRICE,
			SAQICO.PRICE_BENCHMARK_TYPE = 'SIMILAR EQUIPMENT',	
			SAQICO.TOOL_CONFIGURATION = PRPRBM.TOOL_CONFIGURATION,
			SAQICO.CONTRACT_ID = PRPRBM.CONTRACT_ID,
			SAQICO.CONTRACT_VALID_FROM = CONVERT(VARCHAR(10), PRPRBM.CONTRACT_VALID_FROM , 101),
			SAQICO.CONTRACT_VALID_TO = CONVERT(VARCHAR(10), PRPRBM.CONTRACT_VALID_TO, 101)
			FROM SAQICO	(NOLOCK)
			JOIN (
				SELECT SAQICO.CpqTableEntryId, MAX(PRPRBM.CONTRACT_VALID_FROM) AS CONTRACT_VALID_FROM, PRPRBM.ACCOUNT_RECORD_ID,
						PRPRBM.TOOL_CONFIGURATION, PRPRBM.SERVICE_RECORD_ID
				FROM SAQICO (NOLOCK)	
				JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQICO.QUOTE_RECORD_ID
				AND SAQTMT.QTEREV_RECORD_ID = SAQICO.QTEREV_RECORD_ID
				JOIN PRPRBM (NOLOCK) ON PRPRBM.ACCOUNT_RECORD_ID = SAQTMT.ACCOUNT_RECORD_ID AND PRPRBM.TOOL_CONFIGURATION = SAQICO.TOOL_CONFIGURATION
										AND PRPRBM.SERVICE_RECORD_ID = SAQICO.SERVICE_RECORD_ID				
				WHERE ISNULL(SAQICO.ANNUAL_BENCHMARK_BOOKING_PRICE,0) = 0 AND SAQICO.QUOTE_RECORD_ID ='{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{RevisionRecordId}'
				GROUP BY PRPRBM.ACCOUNT_RECORD_ID, PRPRBM.TOOL_CONFIGURATION, PRPRBM.SERVICE_RECORD_ID, SAQICO.CpqTableEntryId
			)AS IQ ON SAQICO.CpqTableEntryId = IQ.CpqTableEntryId
			JOIN PRPRBM (NOLOCK) ON PRPRBM.ACCOUNT_RECORD_ID = IQ.ACCOUNT_RECORD_ID 
									AND PRPRBM.TOOL_CONFIGURATION = IQ.TOOL_CONFIGURATION
									AND PRPRBM.SERVICE_RECORD_ID = IQ.SERVICE_RECORD_ID
									AND PRPRBM.CONTRACT_VALID_FROM = IQ.CONTRACT_VALID_FROM					
			""".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id))
		
		Sql.RunQuery("""UPDATE SAQITM
							SET 									
							TARGET_PRICE = IQ.TARGET_PRICE,
							YEAR_1 = IQ.YEAR_1,
							YEAR_2 = IQ.YEAR_2,
							PRICING_STATUS = 'ACQUIRED',
							OBJECT_QUANTITY = IQ.EQUIPMENT_ID_COUNT
							FROM SAQITM (NOLOCK)
							INNER JOIN (SELECT SAQITM.CpqTableEntryId,	
										CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.TARGET_PRICE, 0)), 0), 0) as decimal(18,2)) as TARGET_PRICE,
										CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_1, 0)), 0), 0) as decimal(18,2)) as YEAR_1,
										CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_2, 0)), 0), 0) as decimal(18,2)) as YEAR_2,
										ISNULL(COUNT(SAQICO.EQUIPMENT_ID),0) as EQUIPMENT_ID_COUNT
										FROM SAQITM (NOLOCK) 
										JOIN SAQICO (NOLOCK) ON SAQICO.QUOTE_RECORD_ID = SAQITM.QUOTE_RECORD_ID AND SAQICO.LINE_ITEM_ID = SAQITM.LINE_ITEM_ID AND SAQICO.QTEREV_RECORD_ID = SAQITM.QTEREV_RECORD_ID
										WHERE SAQITM.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQITM.QTEREV_RECORD_ID = '{RevisionRecordId}'
										GROUP BY SAQITM.LINE_ITEM_ID, SAQITM.QUOTE_RECORD_ID, SAQITM.CpqTableEntryId)IQ
							ON SAQITM.CpqTableEntryId = IQ.CpqTableEntryId 
							WHERE SAQITM.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQITM.QTEREV_RECORD_ID = '{RevisionRecordId}'""".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id))
		SAQICA_ent_renewal = """INSERT SAQICA (EQUIPMENT_ID,EQUIPMENT_RECORD_ID,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,GREENBOOK,GREENBOOK_RECORD_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,ASSEMBLY_DESCRIPTION,ASSEMBLY_ID,ASSEMBLY_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,QUOTE_ITEM_COVERED_OBJECT_ASSEMBLY_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED) SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_COVERED_OBJECT_ASSEMBLY_RECORD_ID, {UserId} as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM

		(SELECT IQ.* FROM ( SELECT DISTINCT 

		SAQSCA.EQUIPMENT_ID,SAQSCA.EQUIPMENT_RECORD_ID,SAQTSE.QUOTE_ID,SAQTSE.QUOTE_RECORD_ID,SAQTSE.QTEREV_ID,SAQTSE.QTEREV_RECORD_ID,SAQTSE.SERVICE_DESCRIPTION,SAQTSE.SERVICE_ID,SAQTSE.SERVICE_RECORD_ID,SAQSCA.GREENBOOK,SAQSCA.GREENBOOK_RECORD_ID,SAQSCA.FABLOCATION_ID,SAQSCA.FABLOCATION_NAME,SAQSCA.FABLOCATION_RECORD_ID,SAQSCA.ASSEMBLY_DESCRIPTION,SAQSCA.ASSEMBLY_ID,SAQSCA.ASSEMBLY_RECORD_ID,SAQTSE.SALESORG_ID,SAQTSE.SALESORG_NAME,SAQTSE.SALESORG_RECORD_ID FROM 

		SAQTSE (NOLOCK) JOIN 
		(SELECT * FROM SAQSCA (NOLOCK) WHERE SAQSCA.QUOTE_RECORD_ID = '{ContractId}' ) SAQSCA ON SAQTSE.QUOTE_RECORD_ID = SAQSCA.QUOTE_RECORD_ID AND SAQTSE.SERVICE_RECORD_ID = SAQSCA.SERVICE_RECORD_ID AND SAQTSE.QTEREV_RECORD_ID = SAQSCA.QTEREV_RECORD_ID WHERE SAQTSE.QUOTE_RECORD_ID = '{ContractId}' AND SAQTSE.QTEREV_RECORD_ID = '{RevisionRecordId}') IQ JOIN SAQSCE (NOLOCK) M ON M.SERVICE_RECORD_ID = IQ.SERVICE_RECORD_ID AND M.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND M.EQUIPMENT_ID = IQ.EQUIPMENT_ID AND M.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID)IQ""".format(UserId=User.Id,  ContractId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id)
		Sql.RunQuery(SAQICA_ent_renewal)

		SAQIAE_ent_renewal = """INSERT SAQIAE (EQUIPMENT_ID,EQUIPMENT_RECORD_ID,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,CPS_CONFIGURATION_ID,CPS_MATCH_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,ASSEMBLY_ID,ASSEMBLY_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,ENTITLEMENT_XML,QUOTE_ITEM_ASSEMBLY_ENTITLEMENT_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED) SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_ASSEMBLY_ENTITLEMENT_RECORD_ID, {UserId} as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM(SELECT IQ.*,M.ENTITLEMENT_XML FROM ( SELECT DISTINCT SAQSCA.EQUIPMENT_ID,SAQSCA.EQUIPMENT_RECORD_ID,SAQTSE.QUOTE_ID,SAQTSE.QUOTE_RECORD_ID,SAQTSE.QTEREV_ID,SAQTSE.QTEREV_RECORD_ID,SAQTSE.SERVICE_DESCRIPTION,SAQTSE.SERVICE_ID,SAQTSE.SERVICE_RECORD_ID,SAQTSE.CPS_CONFIGURATION_ID,SAQTSE.CPS_MATCH_ID,SAQSCA.FABLOCATION_ID,SAQSCA.FABLOCATION_NAME,SAQSCA.FABLOCATION_RECORD_ID,SAQSCA.ASSEMBLY_ID,SAQSCA.ASSEMBLY_RECORD_ID,SAQTSE.SALESORG_ID,SAQTSE.SALESORG_NAME,SAQTSE.SALESORG_RECORD_ID FROM SAQTSE (NOLOCK) JOIN (SELECT * FROM SAQSCA (NOLOCK) WHERE SAQSCA.QUOTE_RECORD_ID = '{ContractId}' AND SAQSCA.QTEREV_RECORD_ID = '{RevisionRecordId}' ) SAQSCA ON SAQTSE.QUOTE_RECORD_ID = SAQSCA.QUOTE_RECORD_ID AND SAQTSE.SERVICE_RECORD_ID = SAQSCA.SERVICE_RECORD_ID AND SAQTSE.QTEREV_RECORD_ID = SAQSCA.QTEREV_RECORD_ID WHERE SAQTSE.QUOTE_RECORD_ID = '{ContractId}' AND SAQTSE.QTEREV_RECORD_ID = '{RevisionRecordId}') IQ JOIN SAQSCE (NOLOCK) M ON M.SERVICE_RECORD_ID = IQ.SERVICE_RECORD_ID AND M.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND M.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND M.EQUIPMENT_ID = IQ.EQUIPMENT_ID )IQ""".format(UserId=User.Id,  ContractId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id)
		Sql.RunQuery(SAQIAE_ent_renewal)
		
		get_curr = str(Quote.GetCustomField('Currency').Content)
		#assigning value to quote summary starts
		total_cost = 0.00
		total_target_price = 0.00
		total_ceiling_price = 0.00
		total_sls_discount_price = 0.00
		total_bd_margin = 0.00
		total_bd_price = 0.00
		total_sales_price = 0.00
		total_yoy = 0.00
		total_year_1 = 0.00
		total_year_2 = 0.00
		total_tax = 0.00
		total_extended_price = 0.00
		#getdecimalplacecurr =decimal_val = ''
		items_data = {}
		get_billing_matrix_year =[]
		items_obj = Sql.GetList("SELECT SERVICE_ID, LINE_ITEM_ID,ISNULL(TOTAL_COST_WOSEEDSTOCK, 0) as TOTAL_COST_WOSEEDSTOCK,TOTAL_COST_WSEEDSTOCK,ISNULL(TARGET_PRICE, 0) as TARGET_PRICE,ISNULL(YEAR_1, 0) as YEAR_1,ISNULL(YEAR_2, 0) as YEAR_2, CURRENCY, ISNULL(YEAR_OVER_YEAR, 0) as YEAR_OVER_YEAR, OBJECT_QUANTITY FROM SAQITM (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' ".format(self.contract_quote_record_id,self.quote_revision_record_id))
		if items_obj:
			for item_obj in items_obj:
				#getdecimalplacecurr = item_obj.CURRENCY
				items_data[int(float(item_obj.LINE_ITEM_ID))] = {'TOTAL_COST':item_obj.TOTAL_COST_WOSEEDSTOCK, 'TARGET_PRICE':item_obj.TARGET_PRICE, 'SERVICE_ID':(item_obj.SERVICE_ID.replace('- BASE', '')).strip(), 'YEAR_1':item_obj.YEAR_1, 'YEAR_2':item_obj.YEAR_2, 'YEAR_OVER_YEAR':item_obj.YEAR_OVER_YEAR, 'OBJECT_QUANTITY':item_obj.OBJECT_QUANTITY}
		#curr_symbol_obj = Sql.GetFirst("select DISPLAY_DECIMAL_PLACES from PRCURR where CURRENCY = '"+str(getdecimalplacecurr)+"'")
		#decimal_val = curr_symbol_obj.DISPLAY_DECIMAL_PLACES
		#formatting_string = "{0:." + str(decimal_val) + "f}"
		for item in Quote.MainItems:
			item_number = int(item.RolledUpQuoteItem)
			if item_number in items_data.keys():
				if items_data.get(item_number).get('SERVICE_ID') == item.PartNumber:
					item_data = items_data.get(item_number)
					item.TOTAL_COST.Value = float(item_data.get('TOTAL_COST'))					
					total_cost += float(item_data.get('TOTAL_COST'))
					item.TARGET_PRICE.Value = item_data.get('TARGET_PRICE')
					total_target_price += item.TARGET_PRICE.Value
					total_ceiling_price += item.CEILING_PRICE.Value
					total_sls_discount_price += item.SALES_DISCOUNT_PRICE.Value
					total_bd_margin += item.BD_PRICE_MARGIN.Value
					total_bd_price += item.BD_PRICE.Value
					total_sales_price += item.NET_PRICE.Value
					item.YEAR_OVER_YEAR.Value = item_data.get('YEAR_OVER_YEAR')
					total_yoy += item.YEAR_OVER_YEAR.Value
					item.YEAR_1.Value = item_data.get('YEAR_1')
					total_year_1 += item.YEAR_1.Value
					item.YEAR_2.Value = item_data.get('YEAR_2')
					total_year_2 += item.YEAR_2.Value
					total_tax += item.TAX.Value
					item.NET_VALUE.Value = item_data.get('TARGET_PRICE')
					total_extended_price += item.NET_VALUE.Value	
					item.OBJECT_QUANTITY.Value = item_data.get('OBJECT_QUANTITY')
		Quote.GetCustomField('TOTAL_COST').Content = str(total_cost) + " " + get_curr
		Quote.GetCustomField('TARGET_PRICE').Content = str(total_target_price) + " " + get_curr
		Quote.GetCustomField('CEILING_PRICE').Content = str(total_ceiling_price) + " " + get_curr
		Quote.GetCustomField('SALES_DISCOUNTED_PRICE').Content = str(total_sls_discount_price) + " " + get_curr
		Quote.GetCustomField('BD_PRICE_MARGIN').Content =str(total_bd_margin) + " %"
		Quote.GetCustomField('BD_PRICE_DISCOUNT').Content = str(total_bd_price) + " %"
		Quote.GetCustomField('TOTAL_NET_PRICE').Content =str(total_sales_price) + " " + get_curr
		Quote.GetCustomField('YEAR_OVER_YEAR').Content =str(total_yoy) + " %"
		Quote.GetCustomField('YEAR_1').Content = str(total_year_1) + " " + get_curr
		Quote.GetCustomField('YEAR_2').Content = str(total_year_2) + " " + get_curr
		Quote.GetCustomField('TAX').Content = str(total_tax) + " " + get_curr
		Quote.GetCustomField('TOTAL_NET_VALUE').Content = str(total_extended_price) + " " + get_curr
		Quote.Save()
		#assigning value to quote summary ends
		# Delete SAQICO temp table - Start
		temp_table_drop = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(temp_table)+"'' ) BEGIN DROP TABLE "+str(temp_table)+" END  ' ")
		# Delete SAQICO temp table - End
		#get_billing_matrix_year =[]
		price_temp_drop = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(price_temp)+"'' ) BEGIN DROP TABLE "+str(price_temp)+" END  ' ")
		Getyear = Sql.GetFirst("select CONTRACT_VALID_FROM,CONTRACT_VALID_TO from SAQTMT where MASTER_TABLE_QUOTE_RECORD_ID = '"+str(self.contract_quote_record_id)+"'")
		if Getyear:
			start_date = datetime.datetime(Getyear.CONTRACT_VALID_FROM)
			end_date = datetime.datetime(Getyear.CONTRACT_VALID_TO)
			mm = (end_date. year - start_date. year) * 12 + (end_date. month - start_date. month)
			quotient, remainder = divmod(mm, 12)
			getyears = quotient + (1 if remainder > 0 else 0)
			
			if not getyears:
				getyears = 1
			if Quote is not None:
				Quote.GetCustomField('GetBillingMatrix_Year').Content = str(getyears)
			if getyears == 1:
				get_billing_matrix_year = ["YEAR_2","YEAR_3","YEAR_4","YEAR_5"]
			elif getyears == 2:
				get_billing_matrix_year = ["YEAR_3","YEAR_4","YEAR_5"]
			elif getyears == 3:
				get_billing_matrix_year = ["YEAR_4","YEAR_5"]
			elif getyears == 4:
				get_billing_matrix_year = ["YEAR_5"]
		Trace.Write('get_billing_matrix_year------'+str(get_billing_matrix_year))
		# Is Changed Information Notification - Start
		self._process_query("""UPDATE SAQSCE SET IS_CHANGED = 0 FROM SAQSCE (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'""".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id))
		# Is Changed Information Notification - End
		return get_billing_matrix_year


	def _insert_quote_item_fab_location(self, **kwargs):
		Trace.Write('fab insert query---')
		SAQIEN_query = """INSERT SAQIEN (QUOTE_ITEM_COVERED_OBJECT_ENTITLEMENTS_RECORD_ID,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,QTESRVENT_RECORD_ID,SERVICE_RECORD_ID,SERVICE_ID,SERVICE_DESCRIPTION,SERIAL_NO,ENTITLEMENT_XML,CPS_CONFIGURATION_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,EQUIPMENT_LINE_ID,LINE_ITEM_ID,CPS_MATCH_ID,QTEITMCOB_RECORD_ID,EQUIPMENT_ID,EQUIPMENT_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,QTEITM_RECORD_ID) (select DISTINCT CONVERT(VARCHAR(4000), NEWID()) AS  QUOTE_ITEM_COVERED_OBJECT_ENTITLEMENTS_RECORD_ID, SAQSCE.QUOTE_ID,SAQSCE.QUOTE_RECORD_ID,SAQSCE.QTEREV_ID,SAQSCE.QTEREV_RECORD_ID,SAQSCE.QTESRVENT_RECORD_ID,SAQSCE.SERVICE_RECORD_ID,SAQSCE.SERVICE_ID,SAQSCE.SERVICE_DESCRIPTION,SAQICO.SERIAL_NO,SAQSCE.ENTITLEMENT_XML,SAQSCE.CPS_CONFIGURATION_ID,SAQSCE.FABLOCATION_ID,SAQSCE.FABLOCATION_NAME,SAQSCE.FABLOCATION_RECORD_ID,SAQICO.EQUIPMENT_LINE_ID,SAQICO.LINE_ITEM_ID,SAQSCE.CPS_MATCH_ID,SAQICO.QUOTE_ITEM_COVERED_OBJECT_RECORD_ID as QTEITMCOB_RECORD_ID,SAQICO.EQUIPMENT_ID,SAQICO.EQUIPMENT_RECORD_ID,SAQSCE.SALESORG_ID,SAQSCE.SALESORG_NAME,SAQSCE.SALESORG_RECORD_ID,SAQITM.QUOTE_ITEM_RECORD_ID FROM SAQSCE (NOLOCK) JOIN SAQICO ON SAQICO.QUOTE_RECORD_ID = SAQSCE.QUOTE_RECORD_ID AND SAQICO.SERVICE_ID = SAQSCE.SERVICE_ID AND SAQICO.QTEREV_RECORD_ID = SAQSCE.QTEREV_RECORD_ID AND SAQICO.FABLOCATION_ID = SAQSCE.FABLOCATION_ID AND SAQICO.GREENBOOK = SAQSCE.GREENBOOK AND SAQICO.EQUIPMENT_ID = SAQSCE.EQUIPMENT_ID JOIN SAQITM on SAQICO.QUOTE_RECORD_ID = SAQITM.QUOTE_RECORD_ID  where SAQSCE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCE.QTEREV_RECORD_ID = '{RevisionRecordId}' )""".format(
		QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id)
		Sql.RunQuery(SAQIEN_query)
		self._process_query(
			"""INSERT SAQIFL(
				FABLOCATION_ID,
				FABLOCATION_NAME,
				FABLOCATION_RECORD_ID,
				SERVICE_ID,
				SERVICE_DESCRIPTION,
				SERVICE_RECORD_ID,
				LINE_ITEM_ID,
				QUOTE_ID,
				QUOTE_NAME,
				QUOTE_RECORD_ID,
				QTEREV_ID,
				QTEREV_RECORD_ID,
				SALESORG_ID,
				SALESORG_NAME,
				SALESORG_RECORD_ID,
				QUOTE_ITEM_FAB_LOCATION_RECORD_ID,
				CPQTABLEENTRYADDEDBY,
				CPQTABLEENTRYDATEADDED,
				CpqTableEntryModifiedBy, 
				CpqTableEntryDateModified
				) SELECT FB.*,CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_FAB_LOCATION_RECORD_ID,
				'{UserName}' AS CPQTABLEENTRYADDEDBY,
				GETDATE() as CPQTABLEENTRYDATEADDED,
				{UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
				SELECT DISTINCT
				SAQICO.FABLOCATION_ID,
				SAQICO.FABLOCATION_NAME,
				SAQICO.FABLOCATION_RECORD_ID,
				SAQICO.SERVICE_ID,
				SAQICO.SERVICE_DESCRIPTION,
				SAQICO.SERVICE_RECORD_ID,
				SAQICO.LINE_ITEM_ID,
				SAQICO.QUOTE_ID,
				SAQICO.QUOTE_NAME,
				SAQICO.QUOTE_RECORD_ID,
				SAQICO.QTEREV_ID,
				SAQICO.QTEREV_RECORD_ID,
				SAQICO.SALESORG_ID,
				SAQICO.SALESORG_NAME,
				SAQICO.SALESORG_RECORD_ID
				FROM SAQICO (NOLOCK)
				JOIN MAFBLC (NOLOCK) ON SAQICO.FABLOCATION_ID = MAFBLC.FAB_LOCATION_ID 
				JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQICO.QUOTE_RECORD_ID
				AND SAQTMT.QTEREV_RECORD_ID = SAQICO.QTEREV_RECORD_ID
				WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{RevisionRecordId}'
				) FB""".format(
								QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id,
								UserId=self.user_id,
								UserName=self.user_name,
							)
		)

	def _insert_quote_item_greenbook(self, **kwargs):
		Trace.Write('greenbook insert query---')
		
		self._process_query(
			"""INSERT SAQIGB(
				GREENBOOK,
				GREENBOOK_RECORD_ID,
				FABLOCATION_ID,
				FABLOCATION_NAME,
				FABLOCATION_RECORD_ID,
				SERVICE_ID,
				SERVICE_DESCRIPTION,
				SERVICE_RECORD_ID,
				LINE_ITEM_ID,
				EQUIPMENT_QUANTITY,
				GLOBAL_CURRENCY,
				DOC_CURRENCY,
				GLOBAL_CURRENCY_RECORD_ID,
				DOCCURR_RECORD_ID,
				QUOTE_ID,
				QUOTE_NAME,
				QUOTE_RECORD_ID,
				QTEREV_ID,
				QTEREV_RECORD_ID,
				SALESORG_ID,
				SALESORG_NAME,
				SALESORG_RECORD_ID,
				QUOTE_ITEM_GREENBOOK_RECORD_ID,
				CPQTABLEENTRYADDEDBY,
				CPQTABLEENTRYDATEADDED,
				CpqTableEntryModifiedBy, 
				CpqTableEntryDateModified
				) SELECT FB.*,CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_GREENBOOK_RECORD_ID,
				'{UserName}' AS CPQTABLEENTRYADDEDBY,
				GETDATE() as CPQTABLEENTRYDATEADDED, 
				{UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
				SELECT DISTINCT
				SAQICO.GREENBOOK,
				SAQICO.GREENBOOK_RECORD_ID,
				SAQICO.FABLOCATION_ID,
				SAQICO.FABLOCATION_NAME,
				SAQICO.FABLOCATION_RECORD_ID,
				SAQICO.SERVICE_ID,
				SAQICO.SERVICE_DESCRIPTION,
				SAQICO.SERVICE_RECORD_ID,
				SAQICO.LINE_ITEM_ID,
				SAQICO.EQUIPMENT_QUANTITY,
				SAQICO.GLOBAL_CURRENCY,
				SAQICO.DOC_CURRENCY,
				SAQICO.GLOBAL_CURRENCY_RECORD_ID,
				SAQICO.DOCURR_RECORD_ID,
				SAQICO.QUOTE_ID,
				SAQICO.QUOTE_NAME,
				SAQICO.QUOTE_RECORD_ID,
				SAQICO.QTEREV_ID,
				SAQICO.QTEREV_RECORD_ID,
				SAQICO.SALESORG_ID,
				SAQICO.SALESORG_NAME,
				SAQICO.SALESORG_RECORD_ID
				FROM SAQICO (NOLOCK)
				JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQICO.QUOTE_RECORD_ID
				AND SAQTMT.QTEREV_RECORD_ID = SAQICO.QTEREV_RECORD_ID
				WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{RevisionRecordId}' AND NOT EXISTS (SELECT GREENBOOK FROM SAQIGB WHERE QUOTE_RECORD_ID ='{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}')
				) FB""".format(
								QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id,
								UserId=self.user_id,
								UserName=self.user_name,
							)
			)

		Sql.RunQuery("""UPDATE SAQIGB
			SET
			SAQIGB.EQUIPMENT_QUANTITY = IQ.QTY
			FROM SAQIGB (NOLOCK) 
			INNER JOIN (
				SELECT COUNT(SAQICO.EQUIPMENT_ID) as QTY,SAQIGB.CpqTableEntryId,SAQICO.FABLOCATION_RECORD_ID, SAQICO.SERVICE_RECORD_ID, SAQICO.GREENBOOK_RECORD_ID
				FROM SAQICO (NOLOCK) 
				JOIN SAQIGB (NOLOCK) ON SAQIGB.QUOTE_RECORD_ID = SAQICO.QUOTE_RECORD_ID and SAQIGB.GREENBOOK_RECORD_ID = SAQICO.GREENBOOK_RECORD_ID and SAQIGB.SERVICE_RECORD_ID = SAQICO.SERVICE_RECORD_ID and SAQIGB.FABLOCATION_RECORD_ID = SAQICO.FABLOCATION_RECORD_ID and SAQIGB.QTEREV_RECORD_ID = SAQICO.QTEREV_RECORD_ID 
				WHERE SAQICO.QUOTE_RECORD_ID ='{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{RevisionRecordId}' GROUP BY SAQICO.FABLOCATION_RECORD_ID,SAQICO.SERVICE_RECORD_ID,SAQICO.GREENBOOK_RECORD_ID,SAQIGB.CpqTableEntryId
			)AS IQ
			ON SAQIGB.CpqTableEntryId = IQ.CpqTableEntryId""".format(QuoteRecordId= self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id))	
	
	def _insert_quote_item_forecast_parts(self, **kwargs): ##User story 4432 starts..
		##Deleteing the tables before insert the data starts..
		for table_name in ('SAQIFP', 'SAQITM'):
			delete_query = "DELETE FROM {ObjectName} WHERE QUOTE_RECORD_ID = '{ContractQuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' {WhereCondition}".format(
					ObjectName=table_name, ContractQuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id, WhereCondition='',
				)
			self._process_query(delete_query)
		##Deleteing the tables before insert the data ends..
		##Delete the native product before adding the product starts..
		for item in Quote.MainItems:
			item.Delete()
		##Delete the native product before adding the product ends..
		##quote item insert starts..
		self._process_query("""
					INSERT SAQITM (
					QUOTE_ITEM_RECORD_ID,
					QUOTE_RECORD_ID,
					QUOTE_ID,
					QUOTE_NAME,
					QTEREV_ID,
					QTEREV_RECORD_ID,
					CPQTABLEENTRYADDEDBY,
					CPQTABLEENTRYDATEADDED,
					CpqTableEntryModifiedBy,
					CpqTableEntryDateModified,
					SERVICE_DESCRIPTION,
					SERVICE_ID,
					SERVICE_RECORD_ID,
					SALESORG_ID,
					SALESORG_NAME,
					SALESORG_RECORD_ID,
					LINE_ITEM_ID,
					OBJECT_QUANTITY,
					QUANTITY,
					CURRENCY,
					CURRENCY_RECORD_ID,
					ITEM_TYPE,
					ITEM_STATUS,
					NET_VALUE,
					UOM_ID, 
					UOM_RECORD_ID,
					PLANT_RECORD_ID,
					PLANT_ID,
					PRICING_STATUS,
					LINE_ITEM_FROM_DATE,
					LINE_ITEM_TO_DATE,
					SRVTAXCAT_RECORD_ID,
					SRVTAXCAT_DESCRIPTION,
					SRVTAXCAT_ID,
					SRVTAXCLA_DESCRIPTION,
					SRVTAXCLA_ID,
					SRVTAXCLA_RECORD_ID,
					DOC_CURRENCY,
					DOCCURR_RECORD_ID,
					QUOTE_CURRENCY,
					QUOTE_CURRENCY_RECORD_ID,
					GLOBAL_CURRENCY,
					GLOBAL_CURRENCY_RECORD_ID,
					YEAR_OVER_YEAR) 
					SELECT 
					CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_RECORD_ID,
					SAQSPT.QUOTE_RECORD_ID,
					SAQSPT.QUOTE_ID,
					SAQTMT.QUOTE_NAME,
					SAQTMT.QTEREV_ID,
					SAQTMT.QTEREV_RECORD_ID,
					'{UserName}' AS CPQTABLEENTRYADDEDBY,
					GETDATE() as CPQTABLEENTRYDATEADDED,
					{UserId} as CpqTableEntryModifiedBy,
					GETDATE() as CpqTableEntryDateModified,
					SAQSPT.SERVICE_DESCRIPTION,
					CONCAT(SAQSPT.SERVICE_ID, '- BASE') as SERVICE_ID,
					SAQSPT.SERVICE_RECORD_ID,
					SAQSPT.SALESORG_ID,
					SAQTRV.SALESORG_NAME,
					SAQSPT.SALESORG_RECORD_ID,
					IQ.LINE_ITEM_ID as LINE_ITEM_ID,
					0 as OBJECT_QUANTITY,
					1 as QUANTITY,
					'{Currency}' as CURRENCY,
					'{CurrencyRecordId}' as CURRENCY_RECORD_ID,
					'ZCB1' as ITEM_TYPE,
					'Active' as ITEM_STATUS,
					0 as NET_VALUE,
					MAMTRL.UNIT_OF_MEASURE, 
					MAMTRL.UOM_RECORD_ID,
					MAMSOP.PLANT_RECORD_ID,
					MAMSOP.PLANT_ID,
					'ACQUIRING' AS PRICING_STATUS,
					SAQTMT.CONTRACT_VALID_FROM as LINE_ITEM_FROM_DATE,
					SAQTMT.CONTRACT_VALID_TO as LINE_ITEM_TO_DATE,
					MAMSCT.TAXCATEGORY_RECORD_ID,
					MAMSCT.TAXCATEGORY_DESCRIPTION, 
					MAMSCT.TAXCATEGORY_ID, 
					MAMSCT.TAXCLASSIFICATION_DESCRIPTION,
					MAMSCT.TAXCLASSIFICATION_ID,
					MAMSCT.TAXCLASSIFICATION_RECORD_ID,
					SAQTRV.DOC_CURRENCY,
					SAQTRV.DOCCURR_RECORD_ID,
					'' as QUOTE_CURRENCY,
					'' as QUOTE_CURRENCY_RECORD_ID,
					SAQTRV.GLOBAL_CURRENCY,
					SAQTRV.GLOBAL_CURRENCY_RECORD_ID,
					PRCFVA.FACTOR_PCTVAR as YEAR_OVER_YEAR
					FROM SAQSPT (NOLOCK)    
					JOIN (
						SELECT SAQSPT.QUOTE_RECORD_ID, SAQSPT.SERVICE_RECORD_ID, MAX(CpqTableEntryId) as CpqTableEntryId, CAST(ROW_NUMBER()OVER(ORDER BY SAQSPT.SERVICE_RECORD_ID) + {ExistingCount} AS DECIMAL(5,1)) AS LINE_ITEM_ID FROM SAQSPT (NOLOCK) 
						WHERE SAQSPT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSPT.QTEREV_RECORD_ID = '{RevisionRecordId}'
						GROUP BY SAQSPT.QUOTE_RECORD_ID, SAQSPT.SERVICE_RECORD_ID
					) AS IQ ON IQ.CpqTableEntryId = SAQSPT.CpqTableEntryId
					JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQSPT.QUOTE_RECORD_ID  AND SAQTMT.QTEREV_RECORD_ID = SAQSPT.QTEREV_RECORD_ID            
					JOIN MAMTRL (NOLOCK) ON MAMTRL.SAP_PART_NUMBER = SAQSPT.SERVICE_ID 
					JOIN SAQTRV (NOLOCK) ON SAQTRV.SALESORG_RECORD_ID = SAQSPT.SALESORG_RECORD_ID AND SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID
					LEFT JOIN MAMSCT (NOLOCK) ON SAQTRV.DISTRIBUTIONCHANNEL_RECORD_ID = MAMSCT.DISTRIBUTIONCHANNEL_RECORD_ID AND SAQTRV.COUNTRY_RECORD_ID = MAMSCT.COUNTRY_RECORD_ID AND SAQTRV.DIVISION_ID = MAMSCT.DIVISION_ID  
					LEFT JOIN MAMSOP (NOLOCK) ON MAMSOP.SAP_PART_NUMBER = MAMTRL.SAP_PART_NUMBER AND MAMSOP.SALESORG_ID = SAQSPT.SALESORG_ID					
					LEFT JOIN PRCFVA (NOLOCK) ON PRCFVA.FACTOR_VARIABLE_ID = SAQSPT.SERVICE_ID AND PRCFVA.FACTOR_ID = 'YOYDIS'
					WHERE SAQSPT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSPT.QTEREV_RECORD_ID = '{RevisionRecordId}'
			""".format(						
				Currency=self.contract_currency,
				CurrencyRecordId=self.contract_currency_record_id,
				QuoteRecordId=self.contract_quote_record_id,
				RevisionRecordId=self.quote_revision_record_id,
				UserId=self.user_id,
				UserName=self.user_name,
				ExistingCount=0
			))
		##quote item insert ends..
		##quote item spare parts insert starts..
		self._process_query(
					"""
					INSERT SAQIFP (
						QUOTE_ITEM_FORECAST_PART_RECORD_ID,
						DELIVERY_MODE,
						EXTENDED_PRICE,
						LINE_ITEM_ID,
						PART_LINE_ID,
						PART_DESCRIPTION,
						PART_NUMBER,
						PART_RECORD_ID,
						QUOTE_ID,
						QUOTE_NAME,
						QUOTE_RECORD_ID,
						QTEREV_ID,
						QTEREV_RECORD_ID,
						SALESORG_ID,
						SALESORG_RECORD_ID,
						SALESUOM_ID,
						SALESUOM_RECORD_ID,
						SCHEDULE_MODE,
						SERVICE_DESCRIPTION,
						SERVICE_ID,
						SERVICE_RECORD_ID,
						UNIT_PRICE,
						VALID_FROM_DATE,
						VALID_TO_DATE,
						BASEUOM_ID,
						BASEUOM_RECORD_ID,
						ANNUAL_QUANTITY,
						MATPRIGRP_ID,
						MATPRIGRP_RECORD_ID,
						PRICING_STATUS,
						DOC_CURRENCY,
						DOCCURR_RECORD_ID,
						CPQTABLEENTRYADDEDBY, 
						CPQTABLEENTRYDATEADDED,
						CpqTableEntryModifiedBy,
						CpqTableEntryDateModified
						)SELECT CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_FORECAST_PART_RECORD_ID, A.* FROM( SELECT
						DISTINCT
						SAQSPT.DELIVERY_MODE,
						SAQSPT.EXTENDED_UNIT_PRICE,
						'10' as LINE_ITEM_ID,
						ROW_NUMBER()OVER(ORDER BY SAQSPT.PART_NUMBER) * 10 as PART_LINE_ID,
						SAQSPT.PART_DESCRIPTION,
						SAQSPT.PART_NUMBER,
						SAQSPT.PART_RECORD_ID,
						SAQSPT.QUOTE_ID,
						SAQSPT.QUOTE_NAME,
						SAQSPT.QUOTE_RECORD_ID,
						SAQSPT.QTEREV_ID,
						SAQSPT.QTEREV_RECORD_ID,
						SAQSPT.SALESORG_ID,
						SAQSPT.SALESORG_RECORD_ID,
						SAQSPT.SALESUOM_ID,
						SAQSPT.SALESUOM_RECORD_ID,
						SAQSPT.SCHEDULE_MODE,
						SAQSPT.SERVICE_DESCRIPTION,
						SAQSPT.SERVICE_ID,
						SAQSPT.SERVICE_RECORD_ID,
						SAQSPT.UNIT_PRICE,
						SAQSPT.VALID_FROM_DATE,
						SAQSPT.VALID_TO_DATE,
						SAQSPT.BASEUOM_ID,
						SAQSPT.BASEUOM_RECORD_ID,
						SAQSPT.CUSTOMER_ANNUAL_QUANTITY,
						SAQSPT.MATPRIGRP_ID,
						SAQSPT.MATPRIGRP_RECORD_ID,
						'{status}' AS PRICING_STATUS,
						'{currency}' AS DOC_CURRENCY,
						'{currency_rec_id}' AS DOCCURR_RECORD_ID,
						'{UserName}' as CPQTABLEENTRYADDEDBY, 
						GETDATE() as CPQTABLEENTRYDATEADDED,
						{UserId} AS CpqTableEntryModifiedBy,
						GETDATE() as CpqTableEntryDateModified
						FROM SAQSPT (NOLOCK)
						WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}')A
					""".format(
						currency=self.contract_currency, 
						currency_rec_id=self.contract_currency_record_id, 
						QuoteRecordId=self.contract_quote_record_id,
						RevisionRecordId=self.quote_revision_record_id,
						status='ACQUIRING...',
						UserId=self.user_id,
						UserName=self.user_name
					)
				)
		##quote item spart parts insert ends..
		# Native Cart Items Insert for spare quotes- Start
		quote_items_obj = Sql.GetList("""SELECT TOP 1000 SAQTSV.SERVICE_ID FROM SAQITM (NOLOCK) JOIN SAQTSV (NOLOCK) ON SAQTSV.SERVICE_RECORD_ID = SAQITM.SERVICE_RECORD_ID AND SAQTSV.QUOTE_RECORD_ID = SAQITM.QUOTE_RECORD_ID AND SAQTSV.QTEREV_RECORD_ID = SAQITM.QTEREV_RECORD_ID WHERE SAQITM.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQITM.QTEREV_RECORD_ID = '{RevisionRecordId}' ORDER BY LINE_ITEM_ID ASC""".format(QuoteRecordId= self.contract_quote_record_id))
		for quote_item_obj in quote_items_obj:
			product_obj = Sql.GetFirst("SELECT MAX(PDS.PRODUCT_ID) AS PRD_ID,PDS.SYSTEM_ID,PDS.UnitOfMeasure,PDS.CART_DESCRIPTION_BUILDER,PDS.PRODUCT_NAME FROM PRODUCTS (NOLOCK) PDS INNER JOIN PRODUCT_VERSIONS (NOLOCK) PRVS ON  PDS.PRODUCT_ID = PRVS.PRODUCT_ID WHERE SYSTEM_ID ='{Partnumber}' GROUP BY PDS.SYSTEM_ID,PDS.UnitOfMeasure,PDS.CART_DESCRIPTION_BUILDER,PDS.PRODUCT_NAME".format(Partnumber = str(quote_item_obj.SERVICE_ID)) )
			if product_obj:
				temp_product = Quote.AddItem('vc_config_cpq')
				for product in temp_product:
					product.PartNumber = str(quote_item_obj.SERVICE_ID)
					product.Description = product_obj.PRODUCT_NAME
					product.QUOTE_ID.Value = self.contract_quote_id		
					product.QUOTE_RECORD_ID.Value = self.contract_quote_record_id
				Quote.Save()			
		# Native Cart Items Insert for spare quotes- End
 
		#assigning value to custom fields(quote summary section) in quote items node starts
		get_curr = str(Quote.GetCustomField('Currency').Content)
		total_cost = 0.00
		total_target_price = 0.00
		total_ceiling_price = 0.00
		total_sls_discount_price = 0.00
		total_bd_margin = 0.00
		total_bd_price = 0.00
		total_sales_price = 0.00
		total_yoy = 0.00
		total_year_1 = 0.00
		total_year_2 = 0.00
		total_tax = 0.00
		total_extended_price = 0.00
		items_data = {}
		get_billing_matrix_year =[]
		items_obj = Sql.GetList("SELECT SERVICE_ID, LINE_ITEM_ID, ISNULL(TOTAL_COST, 0) as TOTAL_COST, ISNULL(TARGET_PRICE, 0) as TARGET_PRICE , ISNULL(YEAR_1, 0) as YEAR_1 ,ISNULL(YEAR_2, 0) as YEAR_2 , CURRENCY, ISNULL(YEAR_OVER_YEAR, 0) as YEAR_OVER_YEAR, OBJECT_QUANTITY FROM SAQITM (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(self.contract_quote_record_id,self.quote_revision_record_id))
		if items_obj:
			for item_obj in items_obj:
				items_data[int(float(item_obj.LINE_ITEM_ID))] = {'TOTAL_COST':item_obj.TOTAL_COST, 'TARGET_PRICE':item_obj.TARGET_PRICE, 'SERVICE_ID':(item_obj.SERVICE_ID.replace('- BASE', '')).strip(), 'YEAR_1':item_obj.YEAR_1, 'YEAR_2':item_obj.YEAR_2, 'YEAR_OVER_YEAR':item_obj.YEAR_OVER_YEAR, 'OBJECT_QUANTITY':item_obj.OBJECT_QUANTITY}
		for item in Quote.MainItems:
			item_number = int(item.RolledUpQuoteItem)
			if item_number in items_data.keys():
				if items_data.get(item_number).get('SERVICE_ID') == item.PartNumber:
					item_data = items_data.get(item_number)
					item.TOTAL_COST.Value = float(item_data.get('TOTAL_COST'))					
					total_cost += float(item_data.get('TOTAL_COST'))
					item.TARGET_PRICE.Value = item_data.get('TARGET_PRICE')
					total_target_price += item.TARGET_PRICE.Value
					total_ceiling_price += item.CEILING_PRICE.Value
					total_sls_discount_price += item.SALES_DISCOUNT_PRICE.Value
					total_bd_margin += item.BD_PRICE_MARGIN.Value
					total_bd_price += item.BD_PRICE.Value
					total_sales_price += item.NET_PRICE.Value
					item.YEAR_OVER_YEAR.Value = item_data.get('YEAR_OVER_YEAR')
					total_yoy += item.YEAR_OVER_YEAR.Value
					item.YEAR_1.Value = item_data.get('YEAR_1')
					total_year_1 += item.YEAR_1.Value
					item.YEAR_2.Value = item_data.get('YEAR_2')
					total_year_2 += item.YEAR_2.Value
					total_tax += item.TAX.Value
					item.NET_VALUE.Value = item_data.get('TARGET_PRICE')
					total_extended_price += item.NET_VALUE.Value	
					item.OBJECT_QUANTITY.Value = item_data.get('OBJECT_QUANTITY')
		Quote.GetCustomField('TOTAL_COST').Content = str(total_cost) + " " + get_curr
		Quote.GetCustomField('TARGET_PRICE').Content = str(total_target_price) + " " + get_curr
		Quote.GetCustomField('CEILING_PRICE').Content = str(total_ceiling_price) + " " + get_curr
		Quote.GetCustomField('SALES_DISCOUNTED_PRICE').Content = str(total_sls_discount_price) + " " + get_curr
		Quote.GetCustomField('BD_PRICE_MARGIN').Content =str(total_bd_margin) + " %"
		Quote.GetCustomField('BD_PRICE_DISCOUNT').Content = str(total_bd_price) + " %"
		Quote.GetCustomField('TOTAL_NET_PRICE').Content =str(total_sales_price) + " " + get_curr
		Quote.GetCustomField('YEAR_OVER_YEAR').Content =str(total_yoy) + " %"
		Quote.GetCustomField('YEAR_1').Content = str(total_year_1) + " " + get_curr
		Quote.GetCustomField('YEAR_2').Content = str(total_year_2) + " " + get_curr
		Quote.GetCustomField('TAX').Content = str(total_tax) + " " + get_curr
		Quote.GetCustomField('TOTAL_NET_VALUE').Content = str(total_extended_price) + " " + get_curr
		Quote.Save()
		#assigning value to custom fields(quote summary section) in quote items node ends

		##calling the iflow for pricing..
		'''try:
			entries = str(self.contract_quote_id)
			user = self.user_name
			CQPARTIFLW.iflow_pricing_call(user,entries)
		except:
			Log.Info("PART PRICING IFLOW ERROR!")'''

		##User story 4432 ends..

	def _create(self):
		if self.action_type == "INSERT_LINE_ITEMS":
			if self.quote_type == "ZWK1 - SPARES": ##User story 4432 starts..
				get_billing_matrix_year = ""
				self._insert_quote_item_forecast_parts() ##User story 4432 ends..
			else:
				get_billing_matrix_year = self._quote_items_insert()
				batch_group_record_id = str(Guid.NewGuid()).upper()
				self._insert_quote_item_fab_location(batch_group_record_id=batch_group_record_id)
				self._insert_quote_item_greenbook(batch_group_record_id=batch_group_record_id)
			#self._insert_quote_item_greenbook()
			return get_billing_matrix_year
	
	def _update(self):
		pass

	def _delete(self):
		pass
	

class QuoteItemsCalculation(ContractQuoteCrudOpertion):
	def __init__(self, **kwargs):
		ContractQuoteCrudOpertion.__init__(self, trigger_from=kwargs.get('trigger_from'), contract_quote_record_id=kwargs.get('contract_quote_record_id'),quote_revision_record_id=kwargs.get('quote_revision_record_id'), 
											tree_param=kwargs.get('tree_param'), tree_parent_level_0=kwargs.get('tree_parent_level_0'))
		self.opertion = kwargs.get('opertion')
		self.action_type = kwargs.get('action_type')
		self.values = kwargs.get('values')
		self.table_name = kwargs.get('table_name')
		self.all_values = kwargs.get('all_values')

	def _calculate(self):
		#contract_quote_obj = Sql.GetFirst(
		#			"""SELECT QUOTE_ID FROM SAQTMT (NOLOCK) WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{QuoteRecordId}' """.format(
		#				QuoteRecordId= self.contract_quote_record_id
		#			)
		#		)
		#QuoteID = contract_quote_obj.QUOTE_ID
		#Trace.Write("QuoteID--> "+str(QuoteID))
		ScriptExecutor.ExecuteGlobal('QTPOSTACRM',{'QUOTE_ID':self.contract_quote_id,'REVISION_ID':self.quote_revision_id, 'Fun_type':'cpq_to_sscm'})
		# Approval Trigger - Start		
		#import ACVIORULES
		#violationruleInsert = ACVIORULES.ViolationConditions()
		#header_obj = Sql.GetFirst("SELECT RECORD_ID FROM SYOBJH (NOLOCK) WHERE OBJECT_NAME = 'SAQTMT'")
		#if header_obj:			
		''' violationruleInsert.InsertAction(
											header_obj.RECORD_ID, self.contract_quote_record_id, "SAQTMT"
											) '''
		# Approval Trigger - End
		return None


class ContractQuotesCommonModel(ContractQuoteCrudOpertion):
	def __init__(self, **kwargs):
		ContractQuoteCrudOpertion.__init__(self, trigger_from=kwargs.get('trigger_from'), contract_quote_record_id=kwargs.get('contract_quote_record_id'),quote_revision_record_id=kwargs.get('quote_revision_record_id'), 
											tree_param=kwargs.get('tree_param'), tree_parent_level_0=kwargs.get('tree_parent_level_0'))
		self.opertion = kwargs.get('opertion')
		self.action_type = kwargs.get('action_type')
		self.values = kwargs.get('values')
		self.table_name = kwargs.get('table_name')
		self.all_values = kwargs.get('all_values')

	def _get(self):
		pass


class ContractQuoteNoficationApprovalModel(ContractQuoteCrudOpertion):

	def __init__(self, **kwargs):
		ContractQuoteCrudOpertion.__init__(self, trigger_from=kwargs.get('trigger_from'), contract_quote_record_id=kwargs.get('contract_quote_record_id'),quote_revision_record_id=kwargs.get('quote_revision_record_id'),tree_param=kwargs.get('tree_param'), tree_parent_level_0=kwargs.get('tree_parent_level_0'))
		self.opertion = kwargs.get('opertion')
		self.action_type = kwargs.get('action_type')
		self.values = kwargs.get('values')
		self.table_name = kwargs.get('table_name')
		self.all_values = kwargs.get('all_values')		
		self.node_id = ""

	def _get(self):
		gettransactionmessage = ""		
		get_approvaltxn_steps = Sql.GetList("select distinct ACAPCH.APRCHN_NAME,ACAPCH.APRCHN_ID,ACAPCH.APRCHN_DESCRIPTION from ACAPTX inner JOIN ACAPCH ON ACAPTX.APRCHN_RECORD_ID=ACAPCH.APPROVAL_CHAIN_RECORD_ID   where ACAPTX.APRTRXOBJ_ID = '{}' and  ACAPTX.APPROVALSTATUS NOT IN ('APPROVED')".format(self.contract_quote_id))		
		if get_approvaltxn_steps and str(current_prod).upper() == 'SALES':
			gettransactionmessage = 'This quote requires approval due to the following:'
			for val in get_approvaltxn_steps:				
				gettransactionmessage += ('<div class="col-md-12" id="dirty-flag-warning"><div class="col-md-12 alert-warning"><label> <img src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/warning1.svg" alt="Warning"> '+val.APRCHN_ID +' | Description : ' +val.APRCHN_DESCRIPTION+'</label></div></div>')
		return gettransactionmessage


class ContractQuoteNoficationModel(ContractQuoteCrudOpertion):
	def __init__(self, **kwargs):
		ContractQuoteCrudOpertion.__init__(self, trigger_from=kwargs.get('trigger_from'), contract_quote_record_id=kwargs.get('contract_quote_record_id'),quote_revision_record_id=kwargs.get('quote_revision_record_id'),tree_param=kwargs.get('tree_param'), tree_parent_level_0=kwargs.get('tree_parent_level_0'))
				
		self.opertion = kwargs.get('opertion')
		self.action_type = kwargs.get('action_type')
		self.values = kwargs.get('values')
		self.table_name = kwargs.get('table_name')
		self.all_values = kwargs.get('all_values')		
		self.node_id = ""
		##getting apr current rec id
		self.apr_current_record_id = kwargs.get('apr_current_record_id')
		Trace.Write('indise notification class')

	def _get(self):
		quote_notif_obj = self._get_record_obj(
					columns=["CPQTABLEENTRYDATEADDED", "CPQTABLEENTRYADDEDBY"],
					table_name="SAQICO",
					where_condition="QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND STATUS = 'APPROVAL REQUIRED'".format(self.contract_quote_record_id,self.quote_revision_record_id),
					single_record=True,
				)
		# commented for time being performance need to rework
		#obj_list = ['SAQTSE','SAQSFE','SAQSGE','SAQSCE','SAQIEN']
		#obj_list = ['SAQIEN']
		
		ent_message_query = Sql.GetFirst("SELECT MESSAGE_TEXT, RECORD_ID, OBJECT_RECORD_ID, MESSAGE_CODE, MESSAGE_LEVEL,MESSAGE_TYPE, OBJECT_RECORD_ID FROM SYMSGS (NOLOCK) WHERE RECORD_ID ='864BA37C-7523-4C7D-A586-6CEF1CABD682' and MESSAGE_LEVEL = 'WARNING'")
		ent_msg_txt = msg_txt = getostfactor = msg_app_txt = getpricefactor = ent_msg_gen_txt =""
		# AllParams = Param.AllParams
		#TreeParam = Product.GetGlobal("TreeParam")
		#notification banner start for add on product
		adoprod_table_value = Sql.GetFirst("SELECT MESSAGE_TEXT, RECORD_ID, OBJECT_RECORD_ID, MESSAGE_CODE, MESSAGE_LEVEL,MESSAGE_TYPE, OBJECT_RECORD_ID FROM SYMSGS (NOLOCK) WHERE OBJECT_RECORD_ID ='SYOBJ-01039' and MESSAGE_LEVEL = 'INFORMATION'")
		
		#adoprod_message_query=Sql.GetList("SELECT distinct SAQSAO.QUOTE_SERVICE_ADD_ON_PRODUCT_RECORD_ID,SAQSAO.QUOTE_RECORD_ID,ACTIVE from SAQSAO inner join SAQSCO on SAQSCO.QUOTE_RECORD_ID = SAQSAO.QUOTE_RECORD_ID WHERE SAQSCO.QUOTE_RECORD_ID = '{}'".format(self.contract_quote_record_id))
		adoprod_message_query=Sql.GetList("SELECT distinct QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID from SAQSCO (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(self.contract_quote_record_id,self.quote_revision_record_id))
		check_active_query = Sql.GetList("SELECT distinct SAQSAO.QUOTE_SERVICE_ADD_ON_PRODUCT_RECORD_ID,SAQSAO.QUOTE_RECORD_ID,ACTIVE from SAQSAO (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(self.contract_quote_record_id,self.quote_revision_record_id))
		#check_active = [i for i in check_active_query if i.ACTIVE == True]	
		if adoprod_message_query and not check_active_query and str(current_prod).upper() == 'SALES':			
			msg_app_txt = (
					'<div  class="col-md-12" id="dirty-flag-warning"><div class="col-md-12 alert-info"><label> <img src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/infor_icon_green.svg" alt="Warning">'
					+ str(adoprod_table_value.MESSAGE_LEVEL)
					+ " : "
					+ str(adoprod_table_value.MESSAGE_CODE)
					+ " : "
					+ str(adoprod_table_value.MESSAGE_TEXT)
					+ "</label></div></div>"
				)
		elif adoprod_message_query and check_active_query:			
			msg_app_txt =""
		##notification banner ends
		#Approval Chain Steps notification banner starts
		if self.tree_param == "Approval Chain Steps" and str(current_prod).upper() == 'APPROVAL CENTER':
			
			# ent_msg_txt = (
			# 	'<div class="row modulesecbnr brdr" onclick="call_vertical_scrl()" data-toggle="collapse" data-target="#alertnotify" aria-expanded="true">NOTIFICATIONS<i class="pull-right fa fa-chevron-down "></i><i class="pull-right fa fa-chevron-up"></i></div>'
			# )
			acapch_query =  Sql.GetList("SELECT * from ACAPCH (nolock) where APPROVAL_CHAIN_RECORD_ID  ='{}'".format(self.apr_current_record_id))
			acacst_query =  Sql.GetList("SELECT distinct APRCHN_RECORD_ID from ACACST WHERE APRCHN_RECORD_ID = '{}'".format(self.apr_current_record_id))
			
			if acapch_query and not acacst_query:
				
				msg_app_txt = (
					'<div  class="col-md-12" id="dirty-flag-warning"><div class="col-md-12 alert-info"><label> <img src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/infor_icon_green.svg" alt="Warning">'
					+ ""
					+ "Please enter atleast one Approval Chain Step to associate with the Approval chains"
					+ "</label></div></div>"
				)
			elif acapch_query and acacst_query:
				
				msg_app_txt = ""
		#Approval Chain Steps notification banner ends	
		gettransactionmessage = ""
		#quoterecid = 'SAQTMT-'+self.contract_quote_record_id
		#getqtrec = Sql.GetFirst("select QUOTE_ID from SAQTMT where MASTER_TABLE_QUOTE_RECORD_ID = '"+str(self.contract_quote_record_id)+"'")
		#get_approvaltxn_steps = Sql.GetList("select distinct ACAPCH.APRCHN_ID,ACAPCH.APRCHN_DESCRIPTION from ACAPMA (NOLOCK) JOIN ACAPCH ON ACAPCH.APPROVAL_CHAIN_RECORD_ID = ACAPMA.APRCHN_RECORD_ID where ACAPMA.APRTRXOBJ_RECORD_ID = '"+str(self.contract_quote_record_id)+"' and ACAPMA.APRSTAMAP_APPROVALSTATUS NOT IN ('APPROVED')")
		get_approvaltxn_steps = Sql.GetList("select DISTINCT ACAPCH.APRCHN_ID,ACAPCH.APRCHN_DESCRIPTION, APRCHN_RECORD_ID from ACAPMA (NOLOCK) JOIN ACAPCH ON ACAPCH.APPROVAL_CHAIN_RECORD_ID = ACAPMA.APRCHN_RECORD_ID where ACAPMA.APRTRXOBJ_RECORD_ID = '"+str(self.contract_quote_record_id)+"' and NOT EXISTS (SELECT DISTINCT ACAPCH.APRCHN_ID from ACAPMA (NOLOCK) JOIN ACAPCH ON ACAPCH.APPROVAL_CHAIN_RECORD_ID = ACAPMA.APRCHN_RECORD_ID where ACAPMA.APRTRXOBJ_RECORD_ID ='" +str(self.contract_quote_record_id)+"' and ACAPMA.APRSTAMAP_APPROVALSTATUS IN ('APPROVED')) ")
		if get_approvaltxn_steps and str(current_prod).upper() == 'SALES':
			gettransactionmessage = 'This quote requires approval due to the following:'
			for val in get_approvaltxn_steps:
				#gettransactionmessage = '<p>This quote has to be approved for the following : </p>'
				gettransactionmessage += ('<div class="col-md-12" id="dirty-flag-warning"><div class="col-md-12 alert-warning"><label> <img src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/warning1.svg" alt="Warning"> '+val.APRCHN_ID +' | Description : ' +str(val.APRCHN_DESCRIPTION).upper()+'</label></div></div>')
		

		if ent_message_query:
			#for val in obj_list:
			val = 'SAQTSE'
			#check_fabvantage_messgae_query = Sql.GetFirst("SELECT ENTITLEMENT_COST_IMPACT,ENTITLEMENT_PRICE_IMPACT from {} where QUOTE_RECORD_ID = '{}'  and PRICE_METHOD = 'MANUAL PRICE' and ENTITLEMENT_NAME  = 'ADDL_PERF_GUARANTEE_91_1'".format(val,self.contract_quote_record_id))
			#commented on 31 maarch start
			#check_fabvantage_messgae_query = Sql.GetList("select ENTITLEMENT_COST_IMPACT,ENTITLEMENT_PRICE_IMPACT from (SELECT distinct e.QUOTE_RECORD_ID, replace(X.Y.value('(ENTITLEMENT_NAME)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_NAME,replace(X.Y.value('(IS_DEFAULT)[1]', 'VARCHAR(128)'),';#38','&') as IS_DEFAULT,replace(X.Y.value('(ENTITLEMENT_COST_IMPACT)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_COST_IMPACT,replace(X.Y.value('(ENTITLEMENT_PRICE_IMPACT)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_PRICE_IMPACT,replace(X.Y.value('(ENTITLEMENT_TYPE)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_TYPE,replace(X.Y.value('(PRICE_METHOD)[1]', 'VARCHAR(128)'),';#38','&') as PRICE_METHOD,replace(X.Y.value('(ENTITLEMENT_VALUE_CODE)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_VALUE_CODE,replace(X.Y.value('(ENTITLEMENT_DESCRIPTION)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_DESCRIPTION,replace(X.Y.value('(ENTITLEMENT_DISPLAY_VALUE)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_DISPLAY_VALUE FROM (select QUOTE_RECORD_ID,convert(xml,replace(ENTITLEMENT_XML,'&',';#38')) as ENTITLEMENT_XML from {} (nolock) where QUOTE_RECORD_ID = '{}') e OUTER APPLY e.ENTITLEMENT_XML.nodes('QUOTE_ITEM_ENTITLEMENT') as X(Y) ) as m where PRICE_METHOD ='MANUAL PRICE'".format(val,self.contract_quote_record_id))
			#end 31 march
			if str(self.contract_quote_record_id):
				getinnercon  = Sql.GetFirst("select QUOTE_RECORD_ID,convert(xml,replace(replace(ENTITLEMENT_XML,'&',';#38'),'''',';#39')) as ENTITLEMENT_XML from SAQTSE (nolock)  where  QUOTE_RECORD_ID = '"+str(self.contract_quote_record_id)+"'")
				if getinnercon:
					check_fabvantage_messgae_query = Sql.GetList("SELECT distinct e.QUOTE_RECORD_ID, replace(X.Y.value('(ENTITLEMENT_COST_IMPACT)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_COST_IMPACT,replace(X.Y.value('(PRICE_METHOD)[1]', 'VARCHAR(128)'),';#38','&') as PRICE_METHOD,replace(X.Y.value('(ENTITLEMENT_PRICE_IMPACT)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_PRICE_IMPACT FROM (select '"+str(getinnercon.QUOTE_RECORD_ID)+"' as QUOTE_RECORD_ID,convert(xml,'"+str(getinnercon.ENTITLEMENT_XML)+"') as ENTITLEMENT_XML ) e  OUTER APPLY e.ENTITLEMENT_XML.nodes('QUOTE_ITEM_ENTITLEMENT') as X(Y)  ")
			
					if check_fabvantage_messgae_query:
						for val in check_fabvantage_messgae_query:
							if val.PRICE_METHOD == 'MANUAL PRICE':
								getostfactor = val.ENTITLEMENT_COST_IMPACT
								getpricefactor = val.ENTITLEMENT_PRICE_IMPACT								
								if str(getostfactor).strip != "" and  str(getpricefactor).strip() != "":									
									ent_msg_txt = ""									
								else:									
									errorLogDeleteQuery = "DELETE SYELOG FROM SYELOG (NOLOCK) INNER JOIN SYMSGS (NOLOCK) ON SYMSGS.RECORD_ID = SYELOG.ERRORMESSAGE_RECORD_ID AND SYMSGS.TRACK_HISTORY = 0 WHERE SYMSGS.MESSAGE_CODE = '000001' AND SYELOG.OBJECT_RECORD_ID = 'E5504B40-36E7-4EA6-9774-EA686705A63F'  AND SYELOG.OBJECT_VALUE = '{}' AND SYELOG.OBJECT_VALUE_REC_ID = '{}'".format(self.contract_quote_record_id, self.contract_quote_record_id)
									Sql.RunQuery(errorLogDeleteQuery)
									insertErrLogWarnQuery = """INSERT SYELOG (ERROR_LOGS_RECORD_ID, ERRORMESSAGE_RECORD_ID, ERRORMESSAGE_DESCRIPTION, OBJECT_NAME, OBJECT_TYPE, OBJECT_RECORD_ID, OBJECT_VALUE_REC_ID, OBJECT_VALUE, ACTIVE, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified)
										select
										CONVERT(VARCHAR(4000),NEWID()) as ERROR_LOGS_RECORD_ID, 
										SAPCPQ_ATTRIBUTE_NAME as ERRORMESSAGE_RECORD_ID,
										MESSAGE_TEXT as ERRORMESSAGE_DESCRIPTION,
										'{table_name}' as OBJECT_NAME,
										MESSAGE_TYPE as OBJECT_TYPE,
										OBJECT_RECORD_ID as OBJECT_RECORD_ID,
										'{quoteId}' as OBJECT_VALUE_REC_ID,
										'{quoteId}' as OBJECT_VALUE,
										1 as ACTIVE,
										'{Get_UserID}' as CPQTABLEENTRYADDEDBY, 
										convert(varchar(10), '{datetime_value}', 101) as CPQTABLEENTRYDATEADDED, 
										'{Get_UserID}' as CpqTableEntryModifiedBy, 
										convert(varchar(10), '{datetime_value}', 101) as CpqTableEntryDateModified
										from SYMSGS (nolock)
										where  OBJECT_RECORD_ID = '87896663-6F9D-4D6E-B1C1-6DA146B56815' and MESSAGE_LEVEL = 'WARNING' and MESSAGE_CODE = '000001'
									""".format(
										quoteId=self.contract_quote_record_id,
										Get_UserID=self.user_id,
										datetime_value=self.datetime_value,
										table_name = val
									)
									Sql.RunQuery(insertErrLogWarnQuery)
									ent_msg_txt = (
										'<div class="col-md-12" id="dirty-flag-warning"><div class="col-md-12 alert-warning"><label> <img src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/warning1.svg" alt="Warning"> '
										+ str(ent_message_query.MESSAGE_LEVEL)
										+ " : "
										+ str(ent_message_query.MESSAGE_CODE)
										+ " : "
										+ str(ent_message_query.MESSAGE_TEXT)
										+ "</label></div></div>"
									)
							else:
								ent_msg_txt = ""
			else:
				ent_msg_txt = ""
			if quote_notif_obj:
				info_message_obj = Sql.GetFirst("SELECT MESSAGE_TEXT, RECORD_ID, OBJECT_RECORD_ID, MESSAGE_CODE, MESSAGE_LEVEL,MESSAGE_TYPE, OBJECT_RECORD_ID FROM SYMSGS (NOLOCK) WHERE RECORD_ID ='9A7602EE-46D9-4891-BCD9-BBCB4B3E313E' and MESSAGE_LEVEL = 'WARNING'")
				
				if info_message_obj:
					errorLogDeleteQuery = "DELETE SYELOG FROM SYELOG (NOLOCK) INNER JOIN SYMSGS (NOLOCK) ON SYMSGS.SAPCPQ_ATTRIBUTE_NAME = SYELOG.ERRORMESSAGE_RECORD_ID AND SYMSGS.TRACK_HISTORY = 0 WHERE SYMSGS.MESSAGE_CODE = '000006' AND SYELOG.OBJECT_RECORD_ID = 'E5504B40-36E7-4EA6-9774-EA686705A63F' AND SYELOG.OBJECT_NAME = 'SAQICO' AND SYELOG.OBJECT_VALUE = '{}' AND SYELOG.OBJECT_VALUE_REC_ID = '{}'".format(self.contract_quote_record_id, self.contract_quote_record_id)
					Sql.RunQuery(errorLogDeleteQuery)
					insertErrLogWarnQuery = """INSERT SYELOG (ERROR_LOGS_RECORD_ID, ERRORMESSAGE_RECORD_ID, ERRORMESSAGE_DESCRIPTION, OBJECT_NAME, OBJECT_TYPE, OBJECT_RECORD_ID, OBJECT_VALUE_REC_ID, OBJECT_VALUE, ACTIVE, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified)
						select
						CONVERT(VARCHAR(4000),NEWID()) as ERROR_LOGS_RECORD_ID, 
						SAPCPQ_ATTRIBUTE_NAME as ERRORMESSAGE_RECORD_ID,
						MESSAGE_TEXT as ERRORMESSAGE_DESCRIPTION,
						OBJECT_APINAME as OBJECT_NAME,
						MESSAGE_TYPE as OBJECT_TYPE,
						OBJECT_RECORD_ID as OBJECT_RECORD_ID,
						'{quoteId}' as OBJECT_VALUE_REC_ID,
						'{quoteId}' as OBJECT_VALUE,
						1 as ACTIVE,
						'{Get_UserID}' as CPQTABLEENTRYADDEDBY, 
						convert(varchar(10), '{datetime_value}', 101) as CPQTABLEENTRYDATEADDED, 
						'{Get_UserID}' as CpqTableEntryModifiedBy, 
						convert(varchar(10), '{datetime_value}', 101) as CpqTableEntryDateModified
						from SYMSGS (nolock)
						where OBJECT_APINAME = 'SAQICO' and OBJECT_RECORD_ID = 'E5504B40-36E7-4EA6-9774-EA686705A63F' and MESSAGE_LEVEL = 'WARNING' and MESSAGE_CODE = '000006'
					""".format(
						quoteId=self.contract_quote_record_id,
						Get_UserID=self.user_id,
						datetime_value=self.datetime_value,
					)
				
					""" msg_txt = (
						'<div class="col-md-12" id="dirty-flag-warning"><div class="col-md-12 alert-warning"><label> <img src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/warning1.svg" alt="Warning"> '
						+ str(info_message_obj.MESSAGE_LEVEL)
						+ " : "
						+ str(info_message_obj.MESSAGE_CODE)
						+ " : "
						+ str(info_message_obj.MESSAGE_TEXT)
						+ "</label></div></div>"
					) """
		Trace.Write('ent_msg_gen_txt-----'+str(ent_msg_gen_txt)+'--msg_app_txt--'+str(msg_app_txt)+'--gettransactionmessage--'+str(gettransactionmessage)+'--ent_msg_txt---'+str(ent_msg_txt))
		# Is Changed Information Notification - Start
		equip_level_entitlement_obj = Sql.GetFirst("SELECT QUOTE_SERVICE_COVERED_OBJ_ENTITLEMENTS_RECORD_ID FROM SAQSCE (NOLOCK) WHERE IS_CHANGED = 1 AND QUOTE_RECORD_ID= '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id))
		if equip_level_entitlement_obj:
			log_message_obj = Sql.GetFirst(
					"SELECT TOP 1000 SYMSGS.MESSAGE_TEXT, SYMSGS.MESSAGE_TYPE, SYMSGS.MESSAGE_CODE, SYMSGS.MESSAGE_LEVEL FROM SYMSGS (nolock) INNER JOIN SYELOG (NOLOCK) ON SYELOG.ERRORMESSAGE_RECORD_ID = SYMSGS.RECORD_ID WHERE SYMSGS.MESSAGE_CODE = '200112' AND SYMSGS.MESSAGE_LEVEL = 'INFORMATION' AND SYELOG.OBJECT_VALUE = '{QuoteId}' AND SYELOG.OBJECT_VALUE_REC_ID = '{QuoteRecordId}' ORDER BY abs(SYMSGS.MESSAGE_CODE)".format(
						QuoteId=self.contract_quote_id,
						QuoteRecordId=self.contract_quote_record_id
					)
				)
			if log_message_obj:
				ent_msg_txt += (
					'<div class="col-md-12" id="entitlement-info"><div class="col-md-12 alert-info"><label> <img src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/infocircle1.svg" alt="Info"> '
					+ str(log_message_obj.MESSAGE_LEVEL)
					+ " : "
					+ str(log_message_obj.MESSAGE_CODE)
					+ " : "
					+ str(log_message_obj.MESSAGE_TEXT)
					+ "</label></div></div>"
				)
		# Is Changed Information Notification - End
		return ent_msg_txt,msg_app_txt,gettransactionmessage,ent_msg_gen_txt

class ContractQuoteApprovalModel(ContractQuoteCrudOpertion):
	def __init__(self, **kwargs):
		ContractQuoteCrudOpertion.__init__(self, trigger_from=kwargs.get('trigger_from'), contract_quote_record_id=kwargs.get('contract_quote_record_id'),quote_revision_record_id=kwargs.get('quote_revision_record_id'), 
											tree_param=kwargs.get('tree_param'), tree_parent_level_0=kwargs.get('tree_parent_level_0'))
		#self.opertion = kwargs.get('opertion')
		#self.action_type = kwargs.get('action_type')
	def _update(self):		
		if self.trigger_from == "APPROVED":
			Sql.RunQuery("UPDATE SAQTMT SET QUOTE_STATUS = 'APPROVED' WHERE SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = '{}'".format(self.contract_quote_record_id))
			result = ScriptExecutor.ExecuteGlobal("QTPOSTACRM", {"QUOTE_ID": self.contract_quote_id, 'Fun_type':'cpq_to_crm'})
		elif self.trigger_from == "SUBMIT FOR APPROVAL":
			Sql.RunQuery("UPDATE SAQTMT SET QUOTE_STATUS = 'APPROVAL REQUIRED' WHERE SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = '{}'".format(self.contract_quote_record_id))
		""" ScriptExecutor.ExecuteGlobal(
			"SYALLTABOP",
			{"Primary_Data": str(self.contract_quote_record_id), "TabNAME": "Quote", "ACTION": "VIEW", "RELATED": ""},
		) """


def Factory(node=None):
	"""Factory Method"""
	models = {
		"OFFERINGS MODEL": ContractQuoteOfferingsModel,
		"COMMON MODEL": ContractQuotesCommonModel,
		"FAB MODEL": ContractQuoteFabModel,
		"TOOL RELOCATION MODEL":ToolRelocationModel,
		"COVERED OBJ MODEL": ContractQuoteCoveredObjModel,
		"BILLING MATRIX MODEL": ContractQuoteBillingMatrixModel,	
		"QUOTE ITEM CALCULATION": QuoteItemsCalculation,
		"QUOTE LEVEL NOTIFICATION": ContractQuoteNoficationModel,
		"QUOTE APPROVAL LEVEL NOTIFICATION":ContractQuoteNoficationApprovalModel,
		"QUOTE APPROVAL MODEL":ContractQuoteApprovalModel,
		"QUOTE ITEMS MODEL":ContractQuoteItemsModel,
	}
	return models[node]

if hasattr(Param, 'CPQ_Columns'):
	Trace.Write("Started Here...>")
	Trace.Write(Param.CPQ_Columns)
	integration_param_objects = Param.CPQ_Columns
	integration_param = {}
	for integration_param_object in integration_param_objects: 
		integration_param[str(integration_param_object.Key)] = str(integration_param_object.Value)		
	opertion = integration_param.get('Opertion')
	node_type = integration_param.get('NodeType')
	try:
		values = integration_param.get('Values')
	except Exception:
		values = []

	try:
		all_values = integration_param.get('AllValues')
	except Exception:
		all_values = False
	try:
		table_name = integration_param.get('ObjectName')
	except Exception:
		table_name = None
	try:
		action_type = integration_param.get('ActionType')
	except Exception:
		action_type = None
	try:
		trigger_from = integration_param.get('TriggerFrom')
	except Exception:
		trigger_from = None
	try:
		service_id = integration_param.get('service_id')
	except Exception:
		service_id = None
	try:
		service_type = integration_param.get('service_type')
	except Exception:
		service_type = None             
	try:
		get_response = integration_param.get('GetResponse')
	except Exception:
		get_response = False
	try:
		contract_quote_record_id = integration_param.get('ContractQuoteRecordId')	
	except Exception:
		contract_quote_record_id = False
	try:
		objname = integration_param.get('OBJECTNAME')	
	except Exception:
		objname = False
	try:
		bmtreeparam = integration_param.get('TREEPARAM')	
	except Exception:
		bmtreeparam = False
	try:
		currrecordid = integration_param.get('CurrentRecordId')	
	except Exception:
		currrecordid = False
	
	# Integration call to update billing matrix - End
else:
	try:
		opertion = Param.Opertion
		node_type = Param.NodeType
		try:
			values = Param.Values
		except Exception:
			values = []
		try:
			A_Keys = Param.A_Keys
			A_Values = Param.A_Values
		except:
			A_Keys = ""
			A_Values = ""
		try:
			all_values = Param.AllValues
		except Exception:
			all_values = False
		try:
			table_name = Param.ObjectName
		except Exception:
			table_name = None
		try:
			action_type = Param.ActionType
		except Exception:
			action_type = None
		try:
			trigger_from = Param.TriggerFrom
		except Exception:
			trigger_from = None
		try:
			service_id = Param.ServiceId
		except Exception:
			service_id = None
		try:
			service_type = Param.ServiceType
		except Exception:
			service_type = None  
		try:
			tree_parent_level_1 = Param.tree_parent_level_1
		except Exception:
			tree_parent_level_1 = None	           
		try:
			get_response = Param.GetResponse
		except Exception:
			get_response = False
		try:
			apr_current_record_id = Param.CurrentRecordId
		except Exception:
			apr_current_record_id = None
		try:
			objname = Param.OBJECTNAME
		except Exception:
			objname = None
		try:
			bmtreeparam = Param.TREEPARAM
		except Exception:
			bmtreeparam = None
		try:
			contract_quote_record_id = Param.ContractQuoteRecordId	
		except Exception:
			contract_quote_record_id = False
		
	except Exception as e:
		Trace.Write('error-'+str(e))
		pass	

node_object = Factory(node_type)(
	opertion=opertion, action_type=action_type, table_name=table_name, values=values, 
	all_values=all_values, trigger_from=trigger_from, contract_quote_record_id=contract_quote_record_id, 
	tree_param=service_id, tree_parent_level_0=service_type,tree_parent_level_1 = tree_parent_level_1,apr_current_record_id= apr_current_record_id,
)

if opertion == "INSERT":
	node_object._insert_billing_matrix()
elif opertion == "ADD":
	node_object._create()
elif opertion == "UPDATE":
	node_object._update()
elif opertion == "DELETE":
	response = node_object._delete()
	if get_response:
		ApiResponse = ApiResponseFactory.JsonResponse(response)
elif opertion == "GET":
	ApiResponse = ApiResponseFactory.JsonResponse(node_object._get())
elif opertion == "CALCULATE":
	node_object._calculate()

# =========================================================================================================================================
#   __script_name : CQINSQTITM.PY
#   __script_description : THIS SCRIPT IS USED TO INSERT QUOTE ITEMS AND ITS RELATED TABLES BASED ENTITLEMENT
#   __primary_author__ : AYYAPPAN SUBRAMANIYAN
#   __create_date :30-09-2021
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================

import Webcom.Configurator.Scripting.Test.TestProduct
import System.Net
import re
import time
import datetime
from SYDATABASE import SQL
import CQPARTIFLW
Sql = SQL()


class ContractQuoteItem:
	def __init__(self, **kwargs):		
		self.user_id = str(User.Id)
		self.user_name = str(User.UserName)		
		self.datetime_value = datetime.datetime.now()
		self.contract_quote_record_id = kwargs.get('contract_quote_record_id')
		self.contract_quote_revision_record_id = kwargs.get('contract_quote_revision_record_id')
		self.action_type = kwargs.get('action_type')
		self.service_id = kwargs.get('service_id')
		self.greenbook_id = kwargs.get('greenbook_id')
		self.fablocation_id = kwargs.get('fablocation_id')
		self.equipment_id = kwargs.get('equipment_id')       
		self.pricing_temp_table = ''
		self.quote_line_item_temp_table = '' 
		self.set_contract_quote_related_details()

	def set_contract_quote_related_details(self):
		contract_quote_obj = Sql.GetFirst("SELECT QUOTE_ID, QUOTE_TYPE, SALE_TYPE, C4C_QUOTE_ID, QTEREV_ID, QUOTE_CURRENCY, QUOTE_CURRENCY_RECORD_ID FROM SAQTMT (NOLOCK) WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{}'".format(self.contract_quote_record_id))
		if contract_quote_obj:
			self.contract_quote_id = contract_quote_obj.QUOTE_ID      
			self.quote_type = contract_quote_obj.QUOTE_TYPE
			self.sale_type = contract_quote_obj.SALE_TYPE
			self.c4c_quote_id = contract_quote_obj.C4C_QUOTE_ID
			self.contract_quote_revision_id = contract_quote_obj.QTEREV_ID
			self.contract_currency = contract_quote_obj.QUOTE_CURRENCY
			self.contract_currency_record_id = contract_quote_obj.QUOTE_CURRENCY_RECORD_ID
			
		else:
			self.contract_quote_id = ''  
			self.quote_type = ''
			self.sale_type = ''
			self.c4c_quote_id = ''
			self.contract_quote_revision_id = ''
		return True

	def _quote_item_delete_process(self):
		for delete_object in ['SAQIAE','SAQICA','SAQIEN','SAQICO']:
			delete_statement = "DELETE DT FROM " +str(delete_object)+" DT JOIN SAQSCE ON DT.EQUIPMENT_RECORD_ID = SAQSCE.EQUIPMENT_RECORD_ID AND DT.SERVICE_ID=SAQSCE.SERVICE_ID AND DT.QUOTE_RECORD_ID=SAQSCE.QUOTE_RECORD_ID AND DT.QTEREV_RECORD_ID=SAQSCE.QTEREV_RECORD_ID WHERE DT.QUOTE_RECORD_ID='{}' AND DT.QTEREV_RECORD_ID='{}' AND SAQSCE.CONFIGURATION_STATUS ='INCOMPLETE' AND DT.SERVICE_ID='{}' ".format(str(self.contract_quote_record_id), str(self.contract_quote_revision_record_id), str(self.service_id))
			#Log.Info(str(self.contract_quote_id)+" <== delete_statement ==> "+str(delete_statement))
			Sql.RunQuery(delete_statement)

		# delete_statement = "DELETE DT FROM SAQIGB DT WHERE DT.QUOTE_RECORD_ID='{quote_record_id}' AND DT.QTEREV_RECORD_ID='{revision_record_id}' AND DT.SERVICE_ID='{service_id}' AND DT.GREENBOOK NOT IN(SELECT CO.GREENBOOK FROM SAQICO CO WHERE CO.QUOTE_RECORD_ID='{quote_record_id}' AND CO.QTEREV_RECORD_ID='{revision_record_id}' AND CO.SERVICE_ID='{service_id}')".format(quote_record_id=str(self.contract_quote_record_id), revision_record_id=str(self.contract_quote_revision_record_id), service_id=str(self.service_id))
		# Sql.RunQuery(delete_statement)
		
		# delete_statement = "DELETE DT FROM SAQIFL DT WHERE DT.QUOTE_RECORD_ID='{quote_record_id}' AND DT.QTEREV_RECORD_ID='{revision_record_id}' AND DT.SERVICE_ID='{service_id}' AND DT.FABLOCATION_ID NOT IN(SELECT CO.FABLOCATION_ID FROM SAQICO CO WHERE CO.QUOTE_RECORD_ID='{quote_record_id}' AND CO.QTEREV_RECORD_ID='{revision_record_id}' AND CO.SERVICE_ID='{service_id}')""".format(quote_record_id=str(self.contract_quote_record_id), revision_record_id=str(self.contract_quote_revision_record_id), service_id=str(self.service_id))
		# Sql.RunQuery(delete_statement) 

		quote_line_item_obj = Sql.GetFirst("SELECT CpqTableEntryId FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID = '{ServiceId}'".format(QuoteRecordId=self.contract_quote_record_id, RevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
		'''
		if self.service_id == 'Z0091':
			fetch_distinct_sid_quote = Sql.GetList(""" SELECT DISTINCT SERVICE_ID FROM SAQTSV WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID LIKE 'Z0091%' OR PAR_SERVICE_ID  LIKE 'Z0091%' """)
			if fetch_distinct_sid_quote:
				for get_sid in fetch_distinct_sid_quote:
					Log.Info("delete service if z0091==>" +str(get_sid.SERVICE_ID))
					Sql.RunQuery("DELETE FROM SAQITM WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID LIKE '{ServiceId}%'".format(QuoteRecordId=self.contract_quote_record_id, RevisionRecordId=self.contract_quote_revision_record_id, ServiceId=get_sid.SERVICE_ID))
		'''
		if not quote_line_item_obj:
			self._native_quote_edit()
			# Sql.RunQuery("DELETE FROM SAQITM WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID LIKE '{ServiceId}%'".format(QuoteRecordId=self.contract_quote_record_id, RevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
			for item in Quote.MainItems:
				if self.service_id == item.PartNumber:
					item.Delete()
			# Update Zero in Quote custom fields
			self._native_quote_item_update()
		return True

	# def _quote_item_insert_process(self, where_string='', join_string='', outer_where_string='', max_quote_item_count=0):

	# 	#Log.Info(str(self.contract_quote_id)+" ==== "+str(self.service_id)+" <== _quote_item_insert_process ==> "+str(max_quote_item_count))
	# 	# Insert SAQITM - Start
	# 	Sql.RunQuery("""
	# 				INSERT SAQITM (
	# 				QUOTE_ITEM_RECORD_ID,
	# 				QUOTE_RECORD_ID,
	# 				QUOTE_ID,
	# 				QUOTE_NAME,
	# 				QTEREV_ID,
	# 				QTEREV_RECORD_ID,
	# 				CPQTABLEENTRYADDEDBY,
	# 				CPQTABLEENTRYDATEADDED,
	# 				CpqTableEntryModifiedBy,
	# 				CpqTableEntryDateModified,
	# 				SERVICE_DESCRIPTION,
	# 				SERVICE_ID,
	# 				SERVICE_RECORD_ID,
	# 				SALESORG_ID,
	# 				SALESORG_NAME,
	# 				SALESORG_RECORD_ID,
	# 				LINE_ITEM_ID,
	# 				OBJECT_QUANTITY,
	# 				QUANTITY,
	# 				CURRENCY,
	# 				CURRENCY_RECORD_ID,
	# 				ITEM_TYPE,
	# 				ITEM_STATUS,
	# 				NET_VALUE,
	# 				UOM_ID, 
	# 				UOM_RECORD_ID,
	# 				PLANT_RECORD_ID,
	# 				PLANT_ID,
	# 				PRICING_STATUS,
	# 				LINE_ITEM_FROM_DATE,
	# 				LINE_ITEM_TO_DATE,
	# 				CONTRACT_VALID_FROM,
	# 				CONTRACT_VALID_TO,
	# 				SRVTAXCAT_RECORD_ID,
	# 				SRVTAXCAT_DESCRIPTION,
	# 				SRVTAXCAT_ID,
	# 				SRVTAXCLA_DESCRIPTION,
	# 				SRVTAXCLA_ID,
	# 				SRVTAXCLA_RECORD_ID,
	# 				DOC_CURRENCY,
	# 				DOCCURR_RECORD_ID,
	# 				QUOTE_CURRENCY,
	# 				QUOTE_CURRENCY_RECORD_ID,
	# 				GLOBAL_CURRENCY,
	# 				GLOBAL_CURRENCY_RECORD_ID,
	# 				YEAR_OVER_YEAR) 
	# 				SELECT 
	# 				CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_RECORD_ID,
	# 				SAQSCE.QUOTE_RECORD_ID,
	# 				SAQSCE.QUOTE_ID,
	# 				SAQTMT.QUOTE_NAME,
	# 				SAQTMT.QTEREV_ID,
	# 				SAQTMT.QTEREV_RECORD_ID,
	# 				'{UserName}' AS CPQTABLEENTRYADDEDBY,
	# 				GETDATE() as CPQTABLEENTRYDATEADDED,
	# 				{UserId} as CpqTableEntryModifiedBy,
	# 				GETDATE() as CpqTableEntryDateModified,
	# 				SAQSCE.SERVICE_DESCRIPTION,
	# 				CONCAT(SAQSCE.SERVICE_ID, '- BASE') as SERVICE_ID,
	# 				SAQSCE.SERVICE_RECORD_ID,
	# 				SAQSCE.SALESORG_ID,
	# 				SAQSCE.SALESORG_NAME,
	# 				SAQSCE.SALESORG_RECORD_ID,
	# 				IQ.LINE_ITEM_ID as LINE_ITEM_ID,
	# 				0 as OBJECT_QUANTITY,
	# 				1 as QUANTITY,
	# 				SAQTMT.QUOTE_CURRENCY as CURRENCY,
	# 				SAQTMT.QUOTE_CURRENCY_RECORD_ID as CURRENCY_RECORD_ID,
	# 				'ZCB1' as ITEM_TYPE,
	# 				'Active' as ITEM_STATUS,
	# 				0 as NET_VALUE,
	# 				MAMTRL.UNIT_OF_MEASURE, 
	# 				MAMTRL.UOM_RECORD_ID,
	# 				MAMSOP.PLANT_RECORD_ID,
	# 				MAMSOP.PLANT_ID,
	# 				null AS PRICING_STATUS,
	# 				SAQTMT.CONTRACT_VALID_FROM as LINE_ITEM_FROM_DATE,
	# 				SAQTMT.CONTRACT_VALID_TO as LINE_ITEM_TO_DATE,
	# 				SAQTMT.CONTRACT_VALID_FROM,
	# 				SAQTMT.CONTRACT_VALID_TO,
	# 				MAMSCT.TAXCATEGORY_RECORD_ID,
	# 				MAMSCT.TAXCATEGORY_DESCRIPTION, 
	# 				MAMSCT.TAXCATEGORY_ID, 
	# 				MAMSCT.TAXCLASSIFICATION_DESCRIPTION,
	# 				MAMSCT.TAXCLASSIFICATION_ID,
	# 				MAMSCT.TAXCLASSIFICATION_RECORD_ID,
	# 				SAQTRV.DOC_CURRENCY,
	# 				SAQTRV.DOCCURR_RECORD_ID,
	# 				'' as QUOTE_CURRENCY,
	# 				'' as QUOTE_CURRENCY_RECORD_ID,
	# 				SAQTRV.GLOBAL_CURRENCY,
	# 				SAQTRV.GLOBAL_CURRENCY_RECORD_ID,
	# 				PRCFVA.FACTOR_PCTVAR as YEAR_OVER_YEAR
	# 				FROM SAQSCE (NOLOCK)    
	# 				JOIN (
	# 					SELECT SAQSCE.QUOTE_RECORD_ID, SAQSCE.SERVICE_RECORD_ID, SAQSCE.ENTITLEMENT_GROUP_ID, MAX(CpqTableEntryId) as CpqTableEntryId, CAST(ROW_NUMBER()OVER(ORDER BY SAQSCE.ENTITLEMENT_GROUP_ID) + {ExistingCount} AS DECIMAL(5,1)) AS LINE_ITEM_ID FROM SAQSCE (NOLOCK) 
	# 					WHERE SAQSCE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCE.QTEREV_RECORD_ID = '{RevisionRecordId}' AND ISNULL(CONFIGURATION_STATUS, '') = 'COMPLETE' {WhereString}
	# 					GROUP BY SAQSCE.QUOTE_RECORD_ID, SAQSCE.SERVICE_RECORD_ID, SAQSCE.ENTITLEMENT_GROUP_ID
	# 				) AS IQ ON IQ.CpqTableEntryId = SAQSCE.CpqTableEntryId
	# 				JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQSCE.QUOTE_RECORD_ID  AND SAQTMT.QTEREV_RECORD_ID = SAQSCE.QTEREV_RECORD_ID          
	# 				JOIN MAMTRL (NOLOCK) ON MAMTRL.SAP_PART_NUMBER = SAQSCE.SERVICE_ID 
	# 				JOIN SAQTRV (NOLOCK) ON SAQTRV.SALESORG_RECORD_ID = SAQSCE.SALESORG_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = SAQSCE.QTEREV_RECORD_ID AND SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID
	# 				LEFT JOIN MAMSCT (NOLOCK) ON SAQTRV.DISTRIBUTIONCHANNEL_RECORD_ID = MAMSCT.DISTRIBUTIONCHANNEL_RECORD_ID AND SAQTRV.COUNTRY_RECORD_ID = MAMSCT.COUNTRY_RECORD_ID AND SAQTRV.DIVISION_ID = MAMSCT.DIVISION_ID  
	# 				LEFT JOIN MAMSOP (NOLOCK) ON MAMSOP.SAP_PART_NUMBER = MAMTRL.SAP_PART_NUMBER AND MAMSOP.SALESORG_ID = SAQSCE.SALESORG_ID					
	# 				LEFT JOIN PRCFVA (NOLOCK) ON PRCFVA.FACTOR_VARIABLE_ID = SAQSCE.SERVICE_ID AND PRCFVA.FACTOR_ID = 'YOYDIS'		
	# 				{JoinString}			
	# 				WHERE SAQSCE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCE.QTEREV_RECORD_ID = '{RevisionRecordId}' {WhereString} {OuterWhereString}
	# 		""".format(
	# 			QuoteRecordId=self.contract_quote_record_id,
	# 			RevisionRecordId=self.contract_quote_revision_record_id,
	# 			UserId=self.user_id,
	# 			UserName=self.user_name,
	# 			WhereString=where_string,
	# 			ExistingCount=max_quote_item_count,
	# 			JoinString=join_string,
	# 			OuterWhereString=outer_where_string
	# 		))
	# 	# Insert SAQITM - End
	# 	return True
	
	def _quote_item_lines_update_z0016(self):
		Sql.RunQuery("""UPDATE SAQICO
								SET
								SAQICO.BD_PRICE = SAQICO_TEMP.BD_PRICE,
								SAQICO.NET_PRICE = SAQICO_TEMP.NET_PRICE,
								SAQICO.BD_PRICE_MARGIN = SAQICO_TEMP.BD_PRICE_MARGIN, 
								SAQICO.BD_PRICE_MARGIN_RECORD_ID = SAQICO_TEMP.BD_PRICE_MARGIN_RECORD_ID, 
								SAQICO.CEILING_PRICE = SAQICO_TEMP.CEILING_PRICE, 
								SAQICO.CLEANING_COST = SAQICO_TEMP.CLEANING_COST,
								SAQICO.CM_PART_COST = SAQICO_TEMP.CM_PART_COST,	
								SAQICO.KPI_COST = SAQICO_TEMP.KPI_COST,	
								SAQICO.LABOR_COST = SAQICO_TEMP.LABOR_COST, 
								SAQICO.PM_PART_COST = SAQICO_TEMP.PM_PART_COST,
								SAQICO.TARGET_PRICE_MARGIN = SAQICO_TEMP.TARGET_PRICE_MARGIN, 
								SAQICO.TARGET_PRICE_MARGIN_RECORD_ID = SAQICO_TEMP.TARGET_PRICE_MARGIN_RECORD_ID
								FROM SAQICO	(NOLOCK)
								JOIN {TempTable} SAQICO_TEMP (NOLOCK) ON SAQICO_TEMP.QUOTE_RECORD_ID = SAQICO.QUOTE_RECORD_ID AND SAQICO_TEMP.SERVICE_ID = SAQICO.SERVICE_ID AND SAQICO_TEMP.EQUIPMENT_RECORD_ID = SAQICO.EQUIPMENT_RECORD_ID AND SAQICO_TEMP.QTEREV_RECORD_ID = SAQICO.QTEREV_RECORD_ID 		
								WHERE 
									SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}'
								""".format(TempTable=self.quote_line_item_temp_table, QuoteRecordId=self.contract_quote_record_id, RevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))	 

		Sql.RunQuery("""UPDATE SAQICO
								SET
								SAQICO.ENTITLEMENT_PRICE_IMPACT = SAQSCE_TEMP.TARGET_PRICE,
								SAQICO.ENTITLEMENT_COST_IMPACT = SAQSCE_TEMP.TOTAL_COST,
								SAQICO.ENTPRCIMP_INGL_CURR = SAQSCE_TEMP.TARGET_PRICE,
								SAQICO.TARGET_PRICE = SAQSCE_TEMP.TARGET_PRICE,
								SAQICO.NET_VALUE = SAQSCE_TEMP.TARGET_PRICE,
								SAQICO.YEAR_1 = SAQSCE_TEMP.YEAR_1,
								SAQICO.YEAR_2 = SAQSCE_TEMP.YEAR_2					
								FROM SAQICO	(NOLOCK)
								INNER JOIN SAQSCO (NOLOCK) ON SAQICO.QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID AND SAQICO.SERVICE_ID = SAQSCO.SERVICE_ID AND SAQICO.EQUIPMENT_RECORD_ID = SAQSCO.EQUIPMENT_RECORD_ID AND SAQICO.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID 
								LEFT JOIN (
										SELECT QUOTE_ID, EQUIPMENT_ID, SERVICE_ID, SUM(CASE WHEN Isnumeric(ENTITLEMENT_PRICE_IMPACT) = 1 THEN CONVERT(DECIMAL(18,2),ENTITLEMENT_PRICE_IMPACT) ELSE 0 END) * 1 AS TARGET_PRICE, SUM(CASE WHEN Isnumeric(ENTITLEMENT_COST_IMPACT) = 1 THEN CONVERT(DECIMAL(18,2),ENTITLEMENT_COST_IMPACT) ELSE 0 END) AS TOTAL_COST, SUM(CASE WHEN Isnumeric(ENTITLEMENT_PRICE_IMPACT) = 1 THEN CASE WHEN ENTITLEMENT_ID LIKE 'AGS_LAB_OPT%_P%' THEN CONVERT(DECIMAL(18,2),ENTITLEMENT_PRICE_IMPACT) ELSE 0 END ELSE 0 END) AS YEAR_2, SUM(CASE WHEN Isnumeric(ENTITLEMENT_PRICE_IMPACT) = 1 THEN CASE WHEN ENTITLEMENT_ID NOT LIKE 'AGS_LAB_OPT%_P%' THEN CONVERT(DECIMAL(18,2),ENTITLEMENT_PRICE_IMPACT) ELSE 0 END ELSE 0 END) AS YEAR_1 from (SELECT * FROM {PriceTemp}) IQ GROUP BY QUOTE_ID, EQUIPMENT_ID, SERVICE_ID
									) SAQSCE_TEMP ON SAQSCE_TEMP.QUOTE_ID = SAQSCO.QUOTE_ID AND SAQSCE_TEMP.EQUIPMENT_ID = SAQSCO.EQUIPMENT_ID AND SAQSCE_TEMP.SERVICE_ID = SAQSCO.SERVICE_ID				
								WHERE 
									SAQSCO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCO.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQSCO.SERVICE_ID = '{ServiceId}'
								""".format(PriceTemp=self.pricing_temp_table, QuoteRecordId=self.contract_quote_record_id, RevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))	 
		return True

	def _quote_item_lines_insert_process(self, where_string='', join_condition_string='', join_string=''):
		equipments_count = 0
		quote_line_item_obj = Sql.GetFirst("SELECT TOP 1 EQUIPMENT_LINE_ID FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' ORDER BY EQUIPMENT_LINE_ID DESC".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id))
		if quote_line_item_obj:
			equipments_count = int(quote_line_item_obj.EQUIPMENT_LINE_ID) 
		#Log.Info(" 1.equipments_count ===>"+str(equipments_count))
		Quote.GetCustomField('PRICING_PICKLIST').Content = 'Document Currency'
		#Log.Info("PRICING_PICKLIST_Value_CHK_1 "+str(Quote.GetCustomField('PRICING_PICKLIST').Content))
		##inserting SAQICO except chamber based equipment A055S000P01-6826		
		Sql.RunQuery("""INSERT SAQICO (BD_PRICE,ENTITLEMENT_PRICE_IMPACT,ENTITLEMENT_COST_IMPACT, EQUIPMENT_DESCRIPTION,STATUS,EQUIPMENT_ID, EQUIPMENT_RECORD_ID, FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, CONTRACT_VALID_FROM, CONTRACT_VALID_TO,LINE_ITEM_ID, MATERIAL_RECORD_ID, PLATFORM, QUOTE_ID, QTEITM_RECORD_ID, QUOTE_NAME, QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,KPU, NET_PRICE, SAP_PART_NUMBER, SERIAL_NO, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, WAFER_SIZE, TARGET_PRICE, TECHNOLOGY,SRVTAXCAT_RECORD_ID,SRVTAXCAT_DESCRIPTION,SRVTAXCAT_ID,SRVTAXCLA_DESCRIPTION,SRVTAXCLA_ID,BD_DISCOUNT, BD_DISCOUNT_RECORD_ID, BD_PRICE_MARGIN, BD_PRICE_MARGIN_RECORD_ID, CEILING_PRICE, CLEANING_COST, CM_PART_COST, CUSTOMER_TOOL_ID, EQUIPMENTCATEGORY_ID, EQUIPMENTCATEGORY_RECORD_ID, EQUIPMENT_STATUS, KPI_COST,MODEL_PRICE,TOTAL_COST_WOSEEDSTOCK,TOTAL_COST_WSEEDSTOCK, LABOR_COST, MNT_PLANT_ID, MNT_PLANT_NAME, MNT_PLANT_RECORD_ID, PM_PART_COST, SLSDIS_PRICE_MARGIN_RECORD_ID, SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID, TARGET_PRICE_MARGIN, TARGET_PRICE_MARGIN_RECORD_ID, WARRANTY_END_DATE, WARRANTY_START_DATE, GREENBOOK, GREENBOOK_RECORD_ID, EQUIPMENT_LINE_ID, NET_VALUE, SALES_DISCOUNT_PRICE, YEAR_1, YEAR_2, YEAR_3, YEAR_4, YEAR_5, EQUIPMENT_QUANTITY, YEAR_OVER_YEAR, EXCHANGE_RATE, EXCHANGE_RATE_DATE, EXCHANGE_RATE_RECORD_ID,GLOBAL_CURRENCY,DOC_CURRENCY,DOCURR_RECORD_ID, GLOBAL_CURRENCY_RECORD_ID, LINE, QUOTE_ITEM_COVERED_OBJECT_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified)
				SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_COVERED_OBJECT_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED,{UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
				SELECT DISTINCT
					null as BD_PRICE,
					0 as ENTITLEMENT_PRICE_IMPACT,
					0 AS ENTITLEMENT_COST_IMPACT,
					SAQSCO.EQUIPMENT_DESCRIPTION,
					null AS STATUS,
					SAQSCO.EQUIPMENT_ID,
					SAQSCO.EQUIPMENT_RECORD_ID,                        
					SAQSCO.FABLOCATION_ID, 
					SAQSCO.FABLOCATION_NAME, 
					SAQSCO.FABLOCATION_RECORD_ID,
					SAQSCO.CONTRACT_VALID_FROM,
					SAQSCO.CONTRACT_VALID_TO,
					SAQITM.LINE_ITEM_ID as LINE_ITEM_ID,
					SAQSCO.MATERIAL_RECORD_ID,
					SAQSCO.PLATFORM,
					SAQSCO.QUOTE_ID, 
					SAQITM.QUOTE_ITEM_RECORD_ID as QTEITM_RECORD_ID, 
					SAQSCO.QUOTE_NAME, 
					SAQSCO.QUOTE_RECORD_ID,
					SAQSCO.QTEREV_ID,
					SAQSCO.QTEREV_RECORD_ID,
					SAQSCO.KPU,
					null as NET_PRICE,
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
					null as BD_DISCOUNT, 
					null as BD_DISCOUNT_RECORD_ID, 
					null as BD_MARGIN, 
					null as BD_MARGIN_RECORD_ID, 
					null as CEILING_PRICE, 
					null as CLEANING_COST,
					null as CM_PART_COST, 
					SAQSCO.CUSTOMER_TOOL_ID, 
					SAQSCO.EQUIPMENTCATEGORY_ID, 
					SAQSCO.EQUIPMENTCATEGORY_RECORD_ID, 
					SAQSCO.EQUIPMENT_STATUS, 
					null as KPI_COST, 
					0 as MODEL_PRICE,
					0 as TOTAL_COST_WOSEEDSTOCK,
					0 as TOTAL_COST_WSEEDSTOCK,
					null as LABOR_COST, 
					SAQSCO.MNT_PLANT_ID, 
					SAQSCO.MNT_PLANT_NAME, 
					SAQSCO.MNT_PLANT_RECORD_ID,
					null as PM_PART_COST,
					null as SLSDIS_PRICE_MARGIN_RECORD_ID, 
					SAQSCO.SALESORG_ID, 
					SAQSCO.SALESORG_NAME, 
					SAQSCO.SALESORG_RECORD_ID, 
					null as TARGET_MARGIN, 
					null as TARGET_MARGIN_THRESHOLD_RECORD_ID,
					SAQSCO.WARRANTY_END_DATE, 
					SAQSCO.WARRANTY_START_DATE, 
					SAQSCO.GREENBOOK, 
					SAQSCO.GREENBOOK_RECORD_ID, 
					CASE WHEN MAMTRL.SERVICE_TYPE = 'NON TOOL BASED' 
							THEN {EquipmentsCount} + 1
							ELSE ROW_NUMBER()OVER(ORDER BY(SAQSCO.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID)) * 1 + {EquipmentsCount}
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
					ISNULL(CONVERT(FLOAT,SAQTRV.EXCHANGE_RATE),'') AS EXCHANGE_RATE,
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
					JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID         
					JOIN SAQTRV (NOLOCK) ON SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID 
					JOIN SAQITM (NOLOCK) ON SAQTRV.QUOTE_RECORD_ID = SAQITM.QUOTE_RECORD_ID 
											AND SAQITM.SERVICE_RECORD_ID = SAQSCO.SERVICE_RECORD_ID
											AND SAQITM.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID
											{JoinConditionString}
					{JoinString}					
				WHERE 
					SAQSCO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCO.QTEREV_RECORD_ID = '{RevisionRecordId}' {WhereString} AND ISNULL(SAQSCO.INCLUDED,'') != 'CHAMBER' AND ISNULL(SAQSCE.CONFIGURATION_STATUS,'') = 'COMPLETE'
				) IQ
				""".format(UserId=self.user_id, UserName=self.user_name, QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id,
				JoinConditionString=join_condition_string, JoinString=join_string, WhereString=where_string, EquipmentsCount=equipments_count)
			)
				
		##inserting assembly to SAQICO if a equipemnt is chamber based FTS A055S000P01-6826
		if self.sale_type == 'TOOL RELOCATION':		
			quote_line_item_obj = Sql.GetFirst("SELECT TOP 1 EQUIPMENT_LINE_ID FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' ORDER BY EQUIPMENT_LINE_ID DESC".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id))
			if quote_line_item_obj:
				equipments_count = int(quote_line_item_obj.EQUIPMENT_LINE_ID) 
			#Log.Info(" 2.equipments_count ===>"+str(equipments_count))
			Sql.RunQuery("""INSERT SAQICO (BD_PRICE,ENTITLEMENT_PRICE_IMPACT,ENTITLEMENT_COST_IMPACT, EQUIPMENT_DESCRIPTION,STATUS,EQUIPMENT_ID, EQUIPMENT_RECORD_ID, FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, CONTRACT_VALID_FROM, CONTRACT_VALID_TO, LINE_ITEM_ID, MATERIAL_RECORD_ID, PLATFORM, QUOTE_ID, QTEITM_RECORD_ID, QUOTE_NAME, QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,KPU, NET_PRICE, SAP_PART_NUMBER, SERIAL_NO, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, WAFER_SIZE, TARGET_PRICE, TECHNOLOGY,SRVTAXCAT_RECORD_ID,SRVTAXCAT_DESCRIPTION,SRVTAXCAT_ID,SRVTAXCLA_DESCRIPTION,SRVTAXCLA_ID, BD_DISCOUNT, BD_DISCOUNT_RECORD_ID, BD_PRICE_MARGIN, BD_PRICE_MARGIN_RECORD_ID, CEILING_PRICE, CLEANING_COST, CM_PART_COST, CUSTOMER_TOOL_ID, EQUIPMENTCATEGORY_ID, EQUIPMENTCATEGORY_RECORD_ID, EQUIPMENT_STATUS, KPI_COST,MODEL_PRICE,TOTAL_COST_WOSEEDSTOCK,TOTAL_COST_WSEEDSTOCK, LABOR_COST, MNT_PLANT_ID, MNT_PLANT_NAME, MNT_PLANT_RECORD_ID, PM_PART_COST, SLSDIS_PRICE_MARGIN_RECORD_ID, SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID, TARGET_PRICE_MARGIN, TARGET_PRICE_MARGIN_RECORD_ID, WARRANTY_END_DATE, WARRANTY_START_DATE, GREENBOOK, GREENBOOK_RECORD_ID, EQUIPMENT_LINE_ID, NET_VALUE, SALES_DISCOUNT_PRICE, YEAR_1, YEAR_2, YEAR_3, YEAR_4, YEAR_5, EQUIPMENT_QUANTITY, YEAR_OVER_YEAR, EXCHANGE_RATE, EXCHANGE_RATE_DATE, EXCHANGE_RATE_RECORD_ID,GLOBAL_CURRENCY,DOC_CURRENCY,DOCURR_RECORD_ID, GLOBAL_CURRENCY_RECORD_ID, LINE,ASSEMBLY_ID,ASSEMBLY_RECORD_ID, QUOTE_ITEM_COVERED_OBJECT_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified)
					SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_COVERED_OBJECT_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED,{UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
					SELECT DISTINCT
						null as BD_PRICE,
						0 as ENTITLEMENT_PRICE_IMPACT,
						0 AS ENTITLEMENT_COST_IMPACT,
						SAQSCO.EQUIPMENT_DESCRIPTION,
						null AS STATUS,
						SAQSCO.EQUIPMENT_ID,
						SAQSCO.EQUIPMENT_RECORD_ID,                        
						SAQSCO.FABLOCATION_ID, 
						SAQSCO.FABLOCATION_NAME, 
						SAQSCO.FABLOCATION_RECORD_ID,
						SAQSCO.CONTRACT_VALID_FROM,
						SAQSCO.CONTRACT_VALID_TO,
						SAQITM.LINE_ITEM_ID as LINE_ITEM_ID,
						SAQSCO.MATERIAL_RECORD_ID,
						SAQSCO.PLATFORM,
						SAQSCO.QUOTE_ID, 
						SAQITM.QUOTE_ITEM_RECORD_ID as QTEITM_RECORD_ID, 
						SAQSCO.QUOTE_NAME, 
						SAQSCO.QUOTE_RECORD_ID,
						SAQSCO.QTEREV_ID,
						SAQSCO.QTEREV_RECORD_ID,
						SAQSCO.KPU,
						null as NET_PRICE,
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
						null as BD_DISCOUNT, 
						null as BD_DISCOUNT_RECORD_ID, 
						null as BD_MARGIN, 
						null as BD_MARGIN_RECORD_ID, 
						null as CEILING_PRICE, 
						null as CLEANING_COST,
						null as CM_PART_COST, 
						SAQSCO.CUSTOMER_TOOL_ID, 
						SAQSCO.EQUIPMENTCATEGORY_ID, 
						SAQSCO.EQUIPMENTCATEGORY_RECORD_ID, 
						SAQSCO.EQUIPMENT_STATUS, 
						null as KPI_COST, 
						0 as MODEL_PRICE,
						0 as TOTAL_COST_WOSEEDSTOCK,
						0 as TOTAL_COST_WSEEDSTOCK,
						null as LABOR_COST, 
						SAQSCO.MNT_PLANT_ID, 
						SAQSCO.MNT_PLANT_NAME, 
						SAQSCO.MNT_PLANT_RECORD_ID,
						null as PM_PART_COST, 
						null as SLSDIS_PRICE_MARGIN_RECORD_ID, 
						SAQSCO.SALESORG_ID, 
						SAQSCO.SALESORG_NAME, 
						SAQSCO.SALESORG_RECORD_ID, 
						null as TARGET_MARGIN, 
						null as TARGET_MARGIN_THRESHOLD_RECORD_ID,
						SAQSCO.WARRANTY_END_DATE, 
						SAQSCO.WARRANTY_START_DATE, 
						SAQSCO.GREENBOOK, 
						SAQSCO.GREENBOOK_RECORD_ID, 
						CASE WHEN MAMTRL.SERVICE_TYPE = 'NON TOOL BASED' 
								THEN {EquipmentsCount} + 1
								ELSE ROW_NUMBER()OVER(ORDER BY(SAQSCO.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID)) * 1 + {EquipmentsCount}
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
						ISNULL(CONVERT(FLOAT,SAQTRV.EXCHANGE_RATE),'') AS	EXCHANGE_RATE,
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
						JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID  AND SAQTMT.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID       
						JOIN SAQTRV (NOLOCK) ON SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID  AND SAQTRV.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID 
						JOIN SAQITM (NOLOCK) ON SAQTRV.QUOTE_RECORD_ID = SAQITM.QUOTE_RECORD_ID 
												AND SAQITM.SERVICE_RECORD_ID = SAQSCO.SERVICE_RECORD_ID
												AND SAQITM.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID
												{JoinConditionString}
												
						{JoinString}						
					WHERE 
						SAQSCO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCO.QTEREV_RECORD_ID = '{RevisionRecordId}' {WhereString} AND ISNULL(SAQSCO.INCLUDED,'') = 'CHAMBER' AND SAQSCA.INCLUDED = 1 AND ISNULL(SAQSCE.CONFIGURATION_STATUS,'') = 'COMPLETE'
					) IQ
					""".format(UserId=self.user_id, UserName=self.user_name, QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id, 
					JoinConditionString=join_condition_string, JoinString=join_string, WhereString= str(where_string), EquipmentsCount=equipments_count)
				)

		if self.service_id == 'Z0016':
			self._quote_item_lines_update_z0016()			
		return True
	
	def _native_quote_edit(self):
		Quote = QuoteHelper.Edit(self.contract_quote_id)		
		#Quote.RefreshActions()
	
	def _native_quote_item_insert(self):		
		if not Quote:
			#Log.Info("_native_quote_item_insert ==> Mo Quote")
			self._native_quote_edit()
		# Native Cart Items Insert - Start
		quote_items_obj = Sql.GetList("""SELECT TOP 1000 SAQTSV.SERVICE_ID FROM SAQITM (NOLOCK) JOIN SAQTSV (NOLOCK) ON SAQTSV.SERVICE_RECORD_ID = SAQITM.SERVICE_RECORD_ID AND SAQTSV.QUOTE_RECORD_ID = SAQITM.QUOTE_RECORD_ID AND SAQTSV.QTEREV_RECORD_ID = SAQITM.QTEREV_RECORD_ID WHERE SAQITM.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQITM.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQTSV.SERVICE_ID = '{ServiceId}' ORDER BY LINE_ITEM_ID ASC""".format(QuoteRecordId= self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id))
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
		# Native Cart Items Insert - End
		return True
	
	def _native_quote_item_update(self):
		if not Quote:
			self._native_quote_edit()
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
		total_year_3 = 0.00
		total_year_4 = 0.00
		total_year_5 = 0.00
		total_tax = 0.00
		total_extended_price = 0.00
		total_model_price = 0.00        
		items_data = {}
		item_obj = Sql.GetFirst("SELECT SERVICE_ID, LINE_ITEM_ID,ISNULL(TOTAL_COST_WOSEEDSTOCK, 0) as TOTAL_COST_WOSEEDSTOCK,TOTAL_COST_WSEEDSTOCK,ISNULL(TARGET_PRICE, 0) as TARGET_PRICE,ISNULL(YEAR_1, 0) as YEAR_1,ISNULL(YEAR_2, 0) as YEAR_2, ISNULL(YEAR_3, 0) as YEAR_3,ISNULL(YEAR_4, 0) as YEAR_4, ISNULL(YEAR_5, 0) as YEAR_5, CURRENCY, ISNULL(YEAR_OVER_YEAR, 0) as YEAR_OVER_YEAR, OBJECT_QUANTITY FROM SAQITM (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID LIKE '{}%'".format(self.contract_quote_record_id,self.contract_quote_revision_record_id,self.service_id))
		if item_obj:
			items_data[int(float(item_obj.LINE_ITEM_ID))] = {'TOTAL_COST':item_obj.TOTAL_COST_WOSEEDSTOCK, 'TARGET_PRICE':item_obj.TARGET_PRICE, 'SERVICE_ID':(item_obj.SERVICE_ID.replace('- BASE', '')).strip(), 'YEAR_1':item_obj.YEAR_1, 'YEAR_2':item_obj.YEAR_2, 'YEAR_3':item_obj.YEAR_3, 'YEAR_4':item_obj.YEAR_4, 'YEAR_5':item_obj.YEAR_5, 'YEAR_OVER_YEAR':item_obj.YEAR_OVER_YEAR, 'OBJECT_QUANTITY':item_obj.OBJECT_QUANTITY}
		
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
					if item.MODEL_PRICE.Value:
						total_model_price += item.MODEL_PRICE.Value
					else:
						total_model_price +=0.00
					item.YEAR_OVER_YEAR.Value = item_data.get('YEAR_OVER_YEAR')
					total_yoy += item.YEAR_OVER_YEAR.Value
					item.YEAR_1.Value = item_data.get('YEAR_1')
					total_year_1 += item.YEAR_1.Value
					item.YEAR_2.Value = item_data.get('YEAR_2')
					total_year_2 += item.YEAR_2.Value
					item.YEAR_3.Value = item_data.get('YEAR_3')
					total_year_3 += item.YEAR_3.Value
					item.YEAR_4.Value = item_data.get('YEAR_4')
					total_year_4 += item.YEAR_4.Value
					item.YEAR_5.Value = item_data.get('YEAR_5')
					total_year_5 += item.YEAR_5.Value
					total_tax += item.TAX.Value
					item.NET_VALUE.Value = item_data.get('TARGET_PRICE')
					total_extended_price += item.NET_VALUE.Value	
					item.OBJECT_QUANTITY.Value = item_data.get('OBJECT_QUANTITY')
		# Quote.GetCustomField('TOTAL_COST').Content = str(total_cost) + " " + get_curr
		# Quote.GetCustomField('TARGET_PRICE').Content = str(total_target_price) + " " + get_curr
		# Quote.GetCustomField('CEILING_PRICE').Content = str(total_ceiling_price) + " " + get_curr
		# Quote.GetCustomField('SALES_DISCOUNTED_PRICE').Content = str(total_sls_discount_price) + " " + get_curr
		# Quote.GetCustomField('BD_PRICE_MARGIN').Content =str(total_bd_margin) + " %"
		# Quote.GetCustomField('BD_PRICE_DISCOUNT').Content = str(total_bd_price) + " %"
		# Quote.GetCustomField('TOTAL_NET_PRICE').Content =str(total_sales_price) + " " + get_curr
		# Quote.GetCustomField('YEAR_OVER_YEAR').Content =str(total_yoy) + " %"
		# Quote.GetCustomField('YEAR_1').Content = str(total_year_1) + " " + get_curr
		# Quote.GetCustomField('YEAR_2').Content = str(total_year_2) + " " + get_curr
		# Quote.GetCustomField('YEAR_3').Content = str(total_year_3) + " " + get_curr
		# Quote.GetCustomField('TAX').Content = str(total_tax) + " " + get_curr
		# Quote.GetCustomField('TOTAL_NET_VALUE').Content = str(total_extended_price) + " " + get_curr
		# Quote.GetCustomField('MODEL_PRICE').Content = str(total_model_price) + " " + get_curr
		# Quote.GetCustomField('BD_PRICE').Content = str(total_bd_price) + " " + get_curr
		#Quote.GetCustomField('DISCOUNT').Content = str(total_discount) + " %"


		###Updating pricing picklist value in line item subtab A055S000P01-4578
		Quote.GetCustomField('PRICING_PICKLIST').Content = 'Document Currency'
		Quote.Save()
		#Log.Info("PRICING_PICKLIST_Value_CHK "+str(Quote.GetCustomField('PRICING_PICKLIST').Content))
		Sql.RunQuery("""UPDATE SAQTRV
						SET 
						SAQTRV.TARGET_PRICE_INGL_CURR = IQ.TARGET_PRICE_INGL_CURR,
						SAQTRV.BD_PRICE_INGL_CURR = IQ.BD_PRICE_INGL_CURR,
						SAQTRV.CEILING_PRICE_INGL_CURR	= IQ.CEILING_PRICE_INGL_CURR,
						SAQTRV.TAX_AMOUNT_INGL_CURR = IQ.TAX_AMOUNT_INGL_CURR,						
						SAQTRV.NET_PRICE_INGL_CURR = IQ.NET_PRICE_INGL_CURR ,						
						SAQTRV.SLSDIS_PRICE_INGL_CURR = IQ.SLSDIS_PRICE_INGL_CURR,
						SAQTRV.YEAR_1_INGL_CURR = IQ.YEAR_1_INGL_CURR,
						SAQTRV.YEAR_2_INGL_CURR = IQ.YEAR_2_INGL_CURR					
						FROM SAQTRV (NOLOCK)
						INNER JOIN (SELECT SAQITM.QUOTE_RECORD_ID, SAQITM.QTEREV_RECORD_ID,
									SUM(ISNULL(SAQITM.TARGET_PRICE_INGL_CURR, 0)) as TARGET_PRICE_INGL_CURR,
									SUM(ISNULL(SAQITM.BD_PRICE_INGL_CURR, 0)) as BD_PRICE_INGL_CURR,
									SUM(ISNULL(SAQITM.CEILING_PRICE_INGL_CURR, 0)) as CEILING_PRICE_INGL_CURR,
									SUM(ISNULL(SAQITM.TAX_AMOUNT_INGL_CURR, 0)) as TAX_AMOUNT_INGL_CURR,
									SUM(ISNULL(SAQITM.NET_PRICE_INGL_CURR, 0)) as NET_PRICE_INGL_CURR,					
									SUM(ISNULL(SAQITM.SLSDIS_PRICE_INGL_CURR, 0)) as SLSDIS_PRICE_INGL_CURR,
									SUM(ISNULL(SAQITM.YEAR_1_INGL_CURR, 0)) as YEAR_1_INGL_CURR,
									SUM(ISNULL(SAQITM.YEAR_2_INGL_CURR, 0)) as YEAR_2_INGL_CURR							
									FROM SAQITM (NOLOCK) WHERE SAQITM.QUOTE_RECORD_ID = '{quote_rec_id}' AND SAQITM.QTEREV_RECORD_ID = '{quote_revision_rec_id}' GROUP BY SAQITM.QTEREV_RECORD_ID, SAQITM.QUOTE_RECORD_ID) IQ ON SAQTRV.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND SAQTRV.QUOTE_REVISION_RECORD_ID = IQ.QTEREV_RECORD_ID
						WHERE SAQTRV.QUOTE_RECORD_ID = '{quote_rec_id}' AND SAQTRV.QUOTE_REVISION_RECORD_ID = '{quote_revision_rec_id}' 	""".format( quote_rec_id = self.contract_quote_record_id,quote_revision_rec_id = self.contract_quote_revision_record_id ) )




		#assigning value to quote summary ends
		return True

	def _create_temp_table_z0016(self):
		# Temp table creation and delete(if altready there) for SAQICO - Start
		temp_table = "SAQICO_BKP_"+str(self.c4c_quote_id)
		try:			
			temp_table_drop = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(temp_table)+"'' ) BEGIN DROP TABLE "+str(temp_table)+" END  ' ")
			SqlHelper.GetFirst("sp_executesql @T=N'SELECT * INTO "+str(temp_table)+" FROM SAQICO(NOLOCK) WHERE QUOTE_RECORD_ID = ''"+str(self.contract_quote_record_id)+"'' AND QTEREV_RECORD_ID = ''"+str(self.contract_quote_revision_record_id)+"'' AND SERVICE_ID = ''"+str(self.service_id)+"''' ")
		except Exception:
			temp_table_drop = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(temp_table)+"'' ) BEGIN DROP TABLE "+str(temp_table)+" END  ' ")
		# Temp table creation and delete(if altready there) for SAQICO - End

		#Temp table for storing price and cost impact
		price_temp = "SAQSCE_BKP_"+str(self.c4c_quote_id)			
		try:	
			price_temp_drop = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(price_temp)+"'' ) BEGIN DROP TABLE "+str(price_temp)+" END  ' ")
			SqlHelper.GetFirst("sp_executesql @T=N'declare @H int; Declare @val Varchar(MAX);DECLARE @XML XML; SELECT @val =  replace(replace(STUFF((SELECT ''''+FINAL from(select  REPLACE(entitlement_xml,''<QUOTE_ITEM_ENTITLEMENT>'',sml) AS FINAL FROM (select ''  <QUOTE_ITEM_ENTITLEMENT><QUOTE_ID>''+quote_id+''</QUOTE_ID><SERVICE_ID>''+service_id+''</SERVICE_ID><EQUIPMENT_ID>''+equipment_id+''</EQUIPMENT_ID>'' AS sml,replace(replace(replace(replace(entitlement_xml,''&'','';#38''),'''','';#39''),'' < '','' &lt; ''),'' > '','' &gt; '')  as entitlement_xml from SAQSCE(nolock) where QUOTE_RECORD_ID=''"+str(self.contract_quote_record_id)+"'' AND QTEREV_RECORD_ID = ''"+str(self.contract_quote_revision_record_id)+"'' AND SERVICE_ID = ''"+str(self.service_id)+"'')A )a FOR XML PATH ('''')), 1, 1, ''''),''&lt;'',''<''),''&gt;'',''>'')  SELECT @XML = CONVERT(XML,''<ROOT>''+@VAL+''</ROOT>'') exec sys.sp_xml_preparedocument @H output,@XML; select QUOTE_ID,EQUIPMENT_ID,SERVICE_ID,ENTITLEMENT_ID,ENTITLEMENT_COST_IMPACT,ENTITLEMENT_PRICE_IMPACT INTO "+str(price_temp)+"  from openxml(@H, ''ROOT/QUOTE_ITEM_ENTITLEMENT'', 0) with (QUOTE_ID VARCHAR(100) ''QUOTE_ID'',EQUIPMENT_ID VARCHAR(100) ''EQUIPMENT_ID'',ENTITLEMENT_ID VARCHAR(100) ''ENTITLEMENT_ID'',SERVICE_ID VARCHAR(100) ''SERVICE_ID'',ENTITLEMENT_COST_IMPACT VARCHAR(100) ''ENTITLEMENT_COST_IMPACT'',ENTITLEMENT_PRICE_IMPACT VARCHAR(100) ''ENTITLEMENT_PRICE_IMPACT'') ; exec sys.sp_xml_removedocument @H; '")
		except Exception:
			price_temp_drop = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(price_temp)+"'' ) BEGIN DROP TABLE "+str(price_temp)+" END  ' ")
		return temp_table, price_temp
	
	def _delete_quote_items(self):		
		## Delete SAQICO, SAQITM  and native quote items - Start
		for table in ('SAQIAE','SAQICA','SAQIEN','SAQICO','SAQITM'):
			if table=='SAQITM':
				Sql.RunQuery("DELETE FROM SAQITM WHERE QUOTE_RECORD_ID = '{ContractQuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID LIKE '{ServiceId}%'".format(
					ContractQuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id
				))
			else:
				Sql.RunQuery("DELETE FROM {TableName} WHERE QUOTE_RECORD_ID = '{ContractQuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID = '{ServiceId}'".format(TableName=table,
							ContractQuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id
						))
		
		for item in Quote.MainItems:
			if self.service_id == item.PartNumber:
				item.Delete()
		## Delete SAQICO, SAQITM  and native quote items - End
		return True		
	
	def _delete_temp_table_z0016(self):		
		try:
			# Delete SAQICO temp table - Start
			temp_table_drop = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(self.quote_line_item_temp_table)+"'' ) BEGIN DROP TABLE "+str(self.quote_line_item_temp_table)+" END  ' ")
			# Delete SAQICO temp table - End		
			price_temp_drop = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(self.pricing_temp_table)+"'' ) BEGIN DROP TABLE "+str(self.pricing_temp_table)+" END  ' ")
		except Exception:
			pass		
		return True

	def _quote_items_insert(self):
		# Z0016 - Start		
		if self.service_id == 'Z0016':
			self.quote_line_item_temp_table, self.pricing_temp_table = self._create_temp_table_z0016()			
			self._delete_quote_items()			
		# Z0016 - End
		quote_item_obj = Sql.GetFirst("SELECT TOP 1 ISNULL(LINE_ITEM_ID, 0) AS LINE_ITEM_ID FROM SAQITM (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' ORDER BY LINE_ITEM_ID DESC".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id))
		# Non tool base quote item insert
		service_obj = Sql.GetFirst("SELECT SAQTSV.SERVICE_ID,MAMTRL.MATERIALCONFIG_TYPE FROM SAQTSV (NOLOCK) JOIN MAMTRL (NOLOCK) ON MAMTRL.SAP_PART_NUMBER = SAQTSV.SERVICE_ID AND MAMTRL.SERVICE_TYPE = 'NON TOOL BASED' WHERE SAQTSV.QUOTE_RECORD_id = '{QuoteRecordId}' AND SAQTSV.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQTSV.SERVICE_ID = '{ServiceId}'".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id))
		if service_obj:
			item_where_string = "AND SAQSCE.SERVICE_ID = '{}'".format(service_obj.SERVICE_ID)
			# Update - Start
			item_join_string = ""			
			item_outer_where_string = ""
			if not self.service_id == 'Z0016':
				item_outer_where_string += " AND ISNULL(SAQITM.SERVICE_RECORD_ID,'') = '' "
				item_join_string = "LEFT JOIN SAQITM (NOLOCK) ON SAQITM.QUOTE_RECORD_ID = SAQSCE.QUOTE_RECORD_ID AND SAQITM.QTEREV_RECORD_ID = SAQSCE.QTEREV_RECORD_ID AND SAQITM.SERVICE_RECORD_ID = SAQSCE.SERVICE_RECORD_ID"
			# Update - end
			# Insert SAQITM - Start
			
			if service_obj.MATERIALCONFIG_TYPE == 'SIMPLE MATERIAL':
				
				item_where_string = item_where_string.replace("SAQSCE","SAQSCO")
				item_join_string = item_join_string.replace("SAQSCE","SAQSCO")
				item_outer_where_string = item_outer_where_string.replace("SAQSCE","SAQSCO")
				self._simple_quote_item_insert_process(where_string=item_where_string, join_string=item_join_string, outer_where_string=item_outer_where_string, max_quote_item_count=int(float(quote_item_obj.LINE_ITEM_ID)) if quote_item_obj else 0)
			else:
				#Log.Info(str(self.contract_quote_id)+" ==== "+str(self.service_id)+" <== _quote_item_insert_process 000 ==> ")
				self._quote_item_insert_process(where_string=item_where_string, join_string=item_join_string, outer_where_string=item_outer_where_string, max_quote_item_count=int(float(quote_item_obj.LINE_ITEM_ID)) if quote_item_obj else 0)
			# Insert SAQITM - End
			# Insert Quote Items Covered Object - Start
			item_line_where_string = "AND SAQSCO.SERVICE_ID = '{}'".format(service_obj.SERVICE_ID)
			if self.sale_type == 'TOOL RELOCATION':
				item_line_where_string += " AND SAQSCO.FABLOCATION_ID IS NOT NULL AND SAQSCO.FABLOCATION_ID != '' "
			#item_line_join_condition_string = "AND SAQITM.LINE_ITEM_ID = CAST(ISNULL(SAQSCE.ENTITLEMENT_GROUP_ID,'1.1') AS DECIMAL(5,1))"
			item_line_join_condition_string = ""
			# Update - Start
			item_line_join_string = ""			
			if not self.service_id == 'Z0016':
				item_line_where_string += " AND ISNULL(SAQICO.EQUIPMENT_RECORD_ID,'') = '' "
				item_line_join_string = "LEFT JOIN SAQICO (NOLOCK) ON SAQICO.QUOTE_RECORD_ID = SAQSCE.QUOTE_RECORD_ID AND SAQICO.QTEREV_RECORD_ID = SAQSCE.QTEREV_RECORD_ID AND SAQICO.SERVICE_RECORD_ID = SAQSCE.SERVICE_RECORD_ID AND SAQICO.GREENBOOK_RECORD_ID = SAQSCE.GREENBOOK_RECORD_ID AND SAQICO.FABLOCATION_RECORD_ID = SAQSCE.FABLOCATION_RECORD_ID AND SAQICO.EQUIPMENT_RECORD_ID = SAQSCE.EQUIPMENT_RECORD_ID"
			# Update - end
			if service_obj.MATERIALCONFIG_TYPE == 'SIMPLE MATERIAL':
				
				# item_where_string = item_where_string.replace("SAQSCE","SAQSCO")
				item_line_join_condition_string =""
				item_line_join_string = item_line_join_string.replace("SAQSCE","SAQSCO")
				self._simple_quote_item_lines_insert_process(where_string=item_line_where_string, join_condition_string= item_line_join_condition_string, join_string=item_line_join_string)
			else:
				self._quote_item_lines_insert_process(where_string=item_line_where_string, join_condition_string=item_line_join_condition_string, join_string=item_line_join_string)
			# Insert Quote Items Covered Object - End
		
		# Tool base quote item insert
		service_obj = Sql.GetFirst("SELECT SAQTSV.SERVICE_ID, MAMTRL.MATERIALCONFIG_TYPE FROM SAQTSV (NOLOCK) JOIN MAMTRL (NOLOCK) ON MAMTRL.SAP_PART_NUMBER = SAQTSV.SERVICE_ID AND MAMTRL.SERVICE_TYPE != 'NON TOOL BASED' WHERE SAQTSV.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQTSV.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQTSV.SERVICE_ID = '{ServiceId}'".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id))
		if service_obj:
			
			item_where_string = "AND SAQSCE.SERVICE_ID = '{}'".format(service_obj.SERVICE_ID)
			# Update - Start
			item_join_string = ""			
			item_outer_where_string = ""
			if not self.service_id == 'Z0016':
				item_outer_where_string += " AND ISNULL(SAQITM.SERVICE_RECORD_ID,'') = '' "
				item_join_string = "LEFT JOIN SAQITM (NOLOCK) ON SAQITM.QUOTE_RECORD_ID = SAQSCE.QUOTE_RECORD_ID AND SAQITM.QTEREV_RECORD_ID = SAQSCE.QTEREV_RECORD_ID AND SAQITM.SERVICE_RECORD_ID = SAQSCE.SERVICE_RECORD_ID"
			# Update - end
			# Insert SAQITM - Start
			if service_obj.MATERIALCONFIG_TYPE == 'SIMPLE MATERIAL':
				item_where_string = item_where_string.replace("SAQSCE","SAQSCO")
				item_join_string = item_join_string.replace("SAQSCE","SAQSCO")
				item_outer_where_string = item_outer_where_string.replace("SAQSCE","SAQSCO")
				self._simple_quote_item_insert_process(where_string=item_where_string, join_string=item_join_string, outer_where_string=item_outer_where_string, max_quote_item_count=int(float(quote_item_obj.LINE_ITEM_ID)) if quote_item_obj else 0)
			else:		
				#Log.Info(str(self.contract_quote_id)+" ==== "+str(self.service_id)+" <== _quote_item_insert_process 111 ==> ")
				self._quote_item_insert_process(where_string=item_where_string, join_string=item_join_string, outer_where_string=item_outer_where_string, max_quote_item_count=int(float(quote_item_obj.LINE_ITEM_ID)) if quote_item_obj else 0)
			# Insert SAQITM - End
			# Insert Quote Items Covered Object - Start
			item_line_where_string = "AND SAQSCO.SERVICE_ID = '{}'".format(service_obj.SERVICE_ID)
			if self.sale_type == 'TOOL RELOCATION':
				item_line_where_string += " AND SAQSCO.FABLOCATION_ID IS NOT NULL AND SAQSCO.FABLOCATION_ID != '' "
			# Update - Start
			item_line_join_string = ""			
			if not self.service_id == 'Z0016':
				item_line_where_string += " AND ISNULL(SAQICO.EQUIPMENT_RECORD_ID,'') = '' "
				item_line_join_string = "LEFT JOIN SAQICO (NOLOCK) ON SAQICO.QUOTE_RECORD_ID = SAQSCE.QUOTE_RECORD_ID AND SAQICO.QTEREV_RECORD_ID = SAQSCE.QTEREV_RECORD_ID AND SAQICO.SERVICE_RECORD_ID = SAQSCE.SERVICE_RECORD_ID AND SAQICO.GREENBOOK_RECORD_ID = SAQSCE.GREENBOOK_RECORD_ID AND SAQICO.FABLOCATION_RECORD_ID = SAQSCE.FABLOCATION_RECORD_ID AND SAQICO.EQUIPMENT_RECORD_ID = SAQSCE.EQUIPMENT_RECORD_ID"
			# Update - end
			if service_obj.MATERIALCONFIG_TYPE == 'SIMPLE MATERIAL':
				# item_where_string = item_where_string.replace("SAQSCE","SAQSCO")
				# item_join_string = item_join_string.replace("SAQSCE","SAQSCO")
				item_line_join_string = item_outer_where_string.replace("SAQSCE","SAQSCO")
				self._simple_quote_item_lines_insert_process(where_string=item_line_where_string, join_condition_string= '', join_string=item_line_join_string)
			else:
				self._quote_item_lines_insert_process(where_string=item_line_where_string, join_condition_string= '', join_string=item_line_join_string)
			# Insert Quote Items Covered Object - End
		
		# Z0016 - Start		
		if self.service_id == 'Z0016':					
			self._delete_temp_table_z0016()			
		# Z0016 - End

		try:
			self._native_quote_edit()
			self._native_quote_item_insert()
		except Exception:
			Log.Info("Exception in native Quote Item insert")
		
		# Sql.RunQuery("DELETE FROM QT__SAQICD where QUOTE_ID = '"+str(self.contract_quote_id)+"'")				
		# CQPARTIFLW.iflow_pricing_call(self.user_name,self.contract_quote_id,self.contract_quote_revision_record_id)
		
		Sql.RunQuery("""UPDATE SAQICO
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
				WHERE SAQICO.QUOTE_RECORD_ID ='{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}'
				GROUP BY PRPRBM.ACCOUNT_RECORD_ID, PRPRBM.EQUIPMENT_RECORD_ID, PRPRBM.SERVICE_RECORD_ID, SAQICO.CpqTableEntryId
			)AS IQ ON SAQICO.CpqTableEntryId = IQ.CpqTableEntryId
			JOIN PRPRBM (NOLOCK) ON PRPRBM.ACCOUNT_RECORD_ID = IQ.ACCOUNT_RECORD_ID 
									AND PRPRBM.EQUIPMENT_RECORD_ID = IQ.EQUIPMENT_RECORD_ID
									AND PRPRBM.SERVICE_RECORD_ID = IQ.SERVICE_RECORD_ID
									AND PRPRBM.CONTRACT_VALID_FROM = IQ.CONTRACT_VALID_FROM								
			""".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id))
		
		Sql.RunQuery("""UPDATE SAQICO
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
				WHERE ISNULL(SAQICO.ANNUAL_BENCHMARK_BOOKING_PRICE,0) = 0 AND SAQICO.QUOTE_RECORD_ID ='{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}'
				GROUP BY PRPRBM.ACCOUNT_RECORD_ID, PRPRBM.TOOL_CONFIGURATION, PRPRBM.SERVICE_RECORD_ID, SAQICO.CpqTableEntryId
			)AS IQ ON SAQICO.CpqTableEntryId = IQ.CpqTableEntryId
			JOIN PRPRBM (NOLOCK) ON PRPRBM.ACCOUNT_RECORD_ID = IQ.ACCOUNT_RECORD_ID 
									AND PRPRBM.TOOL_CONFIGURATION = IQ.TOOL_CONFIGURATION
									AND PRPRBM.SERVICE_RECORD_ID = IQ.SERVICE_RECORD_ID
									AND PRPRBM.CONTRACT_VALID_FROM = IQ.CONTRACT_VALID_FROM					
			""".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id))
		
		Sql.RunQuery("""UPDATE SAQITM
							SET 									
							TARGET_PRICE = IQ.TARGET_PRICE,
							YEAR_1 = IQ.YEAR_1,
							YEAR_2 = IQ.YEAR_2,
							YEAR_3 = IQ.YEAR_3,
							YEAR_4 = IQ.YEAR_4,
							YEAR_5 = IQ.YEAR_5,
							PRICING_STATUS = '',
							OBJECT_QUANTITY = IQ.EQUIPMENT_ID_COUNT
							FROM SAQITM (NOLOCK)
							INNER JOIN (SELECT SAQITM.CpqTableEntryId,	
										CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.TARGET_PRICE, 0)), 0), 0) as decimal(18,2)) as TARGET_PRICE,
										CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_1, 0)), 0), 0) as decimal(18,2)) as YEAR_1,
										CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_2, 0)), 0), 0) as decimal(18,2)) as YEAR_2,
										CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_3, 0)), 0), 0) as decimal(18,2)) as YEAR_3,
										CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_4, 0)), 0), 0) as decimal(18,2)) as YEAR_4,
										CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_5, 0)), 0), 0) as decimal(18,2)) as YEAR_5,
										ISNULL(COUNT(SAQICO.EQUIPMENT_ID),0) as EQUIPMENT_ID_COUNT
										FROM SAQITM (NOLOCK) 
										JOIN SAQICO (NOLOCK) ON SAQICO.QUOTE_RECORD_ID = SAQITM.QUOTE_RECORD_ID AND SAQICO.LINE_ITEM_ID = SAQITM.LINE_ITEM_ID AND SAQICO.QTEREV_RECORD_ID = SAQITM.QTEREV_RECORD_ID
										WHERE SAQITM.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQITM.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQITM.SERVICE_ID LIKE '{ServiceId}%'
										GROUP BY SAQITM.LINE_ITEM_ID, SAQITM.QUOTE_RECORD_ID, SAQITM.CpqTableEntryId)IQ
							ON SAQITM.CpqTableEntryId = IQ.CpqTableEntryId 
							WHERE SAQITM.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQITM.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQITM.SERVICE_ID LIKE '{ServiceId}%'""".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id))
		
		# Update - Start
		item_line_covered_object_assembly_join_string = ""	
		item_line_covered_object_assembly_where_string = ""		
		if not self.service_id == 'Z0016':
			item_line_covered_object_assembly_where_string += " WHERE ISNULL(SAQICA.ASSEMBLY_RECORD_ID,'') = '' "
			item_line_covered_object_assembly_join_string += "LEFT JOIN SAQICA (NOLOCK) ON SAQICA.QUOTE_RECORD_ID = SAQSCE.QUOTE_RECORD_ID AND SAQICA.QTEREV_RECORD_ID = SAQSCE.QTEREV_RECORD_ID AND SAQICA.SERVICE_RECORD_ID = SAQSCE.SERVICE_RECORD_ID AND SAQICA.GREENBOOK_RECORD_ID = SAQSCE.GREENBOOK_RECORD_ID AND SAQICA.FABLOCATION_RECORD_ID = SAQSCE.FABLOCATION_RECORD_ID AND SAQICA.EQUIPMENT_RECORD_ID = SAQSCE.EQUIPMENT_RECORD_ID AND SAQICA.ASSEMBLY_RECORD_ID = IQ.ASSEMBLY_RECORD_ID"
		# Update - End
		#Item Level Assembly Insert - Start
		Sql.RunQuery("""INSERT SAQICA (EQUIPMENT_ID,EQUIPMENT_RECORD_ID,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,GREENBOOK,GREENBOOK_RECORD_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,ASSEMBLY_DESCRIPTION,ASSEMBLY_ID,ASSEMBLY_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,EQUIPMENTTYPE_ID,QUOTE_ITEM_COVERED_OBJECT_ASSEMBLY_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED) 
			SELECT OQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_COVERED_OBJECT_ASSEMBLY_RECORD_ID, {UserId} as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM (
				SELECT IQ.* FROM (
					SELECT 
						DISTINCT SAQSCA.EQUIPMENT_ID,SAQSCA.EQUIPMENT_RECORD_ID,SAQTSE.QUOTE_ID,SAQTSE.QUOTE_RECORD_ID,SAQTSE.QTEREV_ID,SAQTSE.QTEREV_RECORD_ID,SAQTSE.SERVICE_DESCRIPTION,SAQTSE.SERVICE_ID,SAQTSE.SERVICE_RECORD_ID,SAQSCA.GREENBOOK,SAQSCA.GREENBOOK_RECORD_ID,SAQSCA.FABLOCATION_ID,SAQSCA.FABLOCATION_NAME,SAQSCA.FABLOCATION_RECORD_ID,SAQSCA.ASSEMBLY_DESCRIPTION,SAQSCA.ASSEMBLY_ID,SAQSCA.ASSEMBLY_RECORD_ID,SAQTSE.SALESORG_ID,SAQTSE.SALESORG_NAME,SAQTSE.SALESORG_RECORD_ID,SAQSCA.EQUIPMENTTYPE_ID
					FROM SAQTSE (NOLOCK) 
					JOIN SAQSCA (NOLOCK) ON SAQSCA.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID AND SAQSCA.SERVICE_RECORD_ID = SAQTSE.SERVICE_RECORD_ID AND SAQSCA.QTEREV_RECORD_ID = SAQTSE.QTEREV_RECORD_ID  
					WHERE SAQTSE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQTSE.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQTSE.SERVICE_ID = '{ServiceId}'
				) IQ 
				JOIN SAQSCE (NOLOCK) ON SAQSCE.SERVICE_RECORD_ID = IQ.SERVICE_RECORD_ID AND SAQSCE.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND SAQSCE.EQUIPMENT_ID = IQ.EQUIPMENT_ID AND SAQSCE.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND ISNULL(SAQSCE.CONFIGURATION_STATUS,'') = 'COMPLETE'
				{JoinString} {WhereString}
			)OQ""".format(UserId=self.user_id,  QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id, JoinString=item_line_covered_object_assembly_join_string, WhereString=item_line_covered_object_assembly_where_string))
		#Item Level Assembly Insert - End
		
		# Update - Start
		item_line_covered_object_assembly_entitlement_join_string = ""	
		item_line_covered_object_assembly_entitlement_where_string = ""		
		if not self.service_id == 'Z0016':
			item_line_covered_object_assembly_entitlement_where_string += " WHERE ISNULL(SAQIAE.ASSEMBLY_RECORD_ID,'') = '' "
			item_line_covered_object_assembly_entitlement_join_string += "LEFT JOIN SAQIAE (NOLOCK) ON SAQIAE.QUOTE_RECORD_ID = SAQSCE.QUOTE_RECORD_ID AND SAQIAE.QTEREV_RECORD_ID = SAQSCE.QTEREV_RECORD_ID AND SAQIAE.SERVICE_RECORD_ID = SAQSCE.SERVICE_RECORD_ID AND SAQIAE.FABLOCATION_RECORD_ID = SAQSCE.FABLOCATION_RECORD_ID AND SAQIAE.EQUIPMENT_RECORD_ID = SAQSCE.EQUIPMENT_RECORD_ID AND SAQIAE.ASSEMBLY_RECORD_ID = IQ.ASSEMBLY_RECORD_ID"
		# Update - End
		Sql.RunQuery("""INSERT SAQIAE (EQUIPMENT_ID,EQUIPMENT_RECORD_ID,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,CPS_CONFIGURATION_ID,CPS_MATCH_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,ASSEMBLY_ID,ASSEMBLY_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,ENTITLEMENT_XML,QUOTE_ITEM_ASSEMBLY_ENTITLEMENT_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED) 
			SELECT OQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_ASSEMBLY_ENTITLEMENT_RECORD_ID, {UserId} as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM (
				SELECT IQ.*,SAQSCE.ENTITLEMENT_XML FROM (
					SELECT 
						DISTINCT SAQSCA.EQUIPMENT_ID,SAQSCA.EQUIPMENT_RECORD_ID,SAQTSE.QUOTE_ID,SAQTSE.QUOTE_RECORD_ID,SAQTSE.QTEREV_ID,SAQTSE.QTEREV_RECORD_ID,SAQTSE.SERVICE_DESCRIPTION,SAQTSE.SERVICE_ID,SAQTSE.SERVICE_RECORD_ID,SAQTSE.CPS_CONFIGURATION_ID,SAQTSE.CPS_MATCH_ID,SAQSCA.FABLOCATION_ID,SAQSCA.FABLOCATION_NAME,SAQSCA.FABLOCATION_RECORD_ID,SAQSCA.ASSEMBLY_ID,SAQSCA.ASSEMBLY_RECORD_ID,SAQTSE.SALESORG_ID,SAQTSE.SALESORG_NAME,SAQTSE.SALESORG_RECORD_ID 
					FROM SAQTSE (NOLOCK) 
					JOIN SAQSCA (NOLOCK) ON SAQSCA.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID AND SAQSCA.SERVICE_RECORD_ID = SAQTSE.SERVICE_RECORD_ID AND SAQSCA.QTEREV_RECORD_ID = SAQTSE.QTEREV_RECORD_ID WHERE SAQTSE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQTSE.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQTSE.SERVICE_ID = '{ServiceId}'
				) IQ 
				JOIN SAQSCE (NOLOCK) ON SAQSCE.SERVICE_RECORD_ID = IQ.SERVICE_RECORD_ID AND SAQSCE.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND SAQSCE.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND SAQSCE.EQUIPMENT_ID = IQ.EQUIPMENT_ID AND ISNULL(SAQSCE.CONFIGURATION_STATUS,'') = 'COMPLETE'
				{JoinString} {WhereString}
			)OQ""".format(UserId=self.user_id,  QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id, JoinString=item_line_covered_object_assembly_entitlement_join_string, WhereString=item_line_covered_object_assembly_entitlement_where_string))
		
		try:
			self._native_quote_item_update()
		except Exception:
			Log.Info("Exception in native Quote Item update")
		
		# price_temp_drop = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(price_temp)+"'' ) BEGIN DROP TABLE "+str(price_temp)+" END  ' ")
		
		# Is Changed Information Notification - Start
		Sql.RunQuery("""UPDATE SAQSCE SET IS_CHANGED = 0 FROM SAQSCE (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID = '{ServiceId}'""".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id))
		# Is Changed Information Notification - End
		return True

	def _insert_quote_item_fab_location(self):
		# Update - Start
		item_line_covered_object_entitlement_join_string = ""	
		item_line_covered_object_entitlement_where_string = ""		
		if not self.service_id == 'Z0016':
			item_line_covered_object_entitlement_where_string += " AND ISNULL(SAQIEN.EQUIPMENT_RECORD_ID,'') = '' "
			item_line_covered_object_entitlement_join_string += "LEFT JOIN SAQIEN (NOLOCK) ON SAQIEN.QUOTE_RECORD_ID = SAQSCE.QUOTE_RECORD_ID AND SAQIEN.QTEREV_RECORD_ID = SAQSCE.QTEREV_RECORD_ID AND SAQIEN.SERVICE_RECORD_ID = SAQSCE.SERVICE_RECORD_ID AND SAQIEN.FABLOCATION_RECORD_ID = SAQSCE.FABLOCATION_RECORD_ID AND SAQIEN.EQUIPMENT_RECORD_ID = SAQSCE.EQUIPMENT_RECORD_ID"
		# Update - End
		SAQIEN_query = """INSERT SAQIEN (QUOTE_ITEM_COVERED_OBJECT_ENTITLEMENTS_RECORD_ID,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,QTESRVENT_RECORD_ID,SERVICE_RECORD_ID,SERVICE_ID,SERVICE_DESCRIPTION,SERIAL_NO,ENTITLEMENT_XML,CPS_CONFIGURATION_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,EQUIPMENT_LINE_ID,LINE_ITEM_ID,CPS_MATCH_ID,QTEITMCOB_RECORD_ID,EQUIPMENT_ID,EQUIPMENT_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,QTEITM_RECORD_ID) 
		(
			SELECT 
				DISTINCT CONVERT(VARCHAR(4000), NEWID()) AS  QUOTE_ITEM_COVERED_OBJECT_ENTITLEMENTS_RECORD_ID, SAQSCE.QUOTE_ID,SAQSCE.QUOTE_RECORD_ID,SAQSCE.QTEREV_ID,SAQSCE.QTEREV_RECORD_ID,SAQSCE.QTESRVENT_RECORD_ID,SAQSCE.SERVICE_RECORD_ID,SAQSCE.SERVICE_ID,SAQSCE.SERVICE_DESCRIPTION,SAQICO.SERIAL_NO,SAQSCE.ENTITLEMENT_XML,SAQSCE.CPS_CONFIGURATION_ID,SAQSCE.FABLOCATION_ID,SAQSCE.FABLOCATION_NAME,SAQSCE.FABLOCATION_RECORD_ID,SAQICO.EQUIPMENT_LINE_ID,SAQICO.LINE_ITEM_ID,SAQSCE.CPS_MATCH_ID,SAQICO.QUOTE_ITEM_COVERED_OBJECT_RECORD_ID as QTEITMCOB_RECORD_ID,SAQICO.EQUIPMENT_ID,SAQICO.EQUIPMENT_RECORD_ID,SAQSCE.SALESORG_ID,SAQSCE.SALESORG_NAME,SAQSCE.SALESORG_RECORD_ID,SAQITM.QUOTE_ITEM_RECORD_ID 
			FROM SAQSCE (NOLOCK) 
			JOIN SAQICO ON SAQICO.QUOTE_RECORD_ID = SAQSCE.QUOTE_RECORD_ID AND SAQICO.SERVICE_ID = SAQSCE.SERVICE_ID AND SAQICO.						QTEREV_RECORD_ID = SAQSCE.QTEREV_RECORD_ID AND SAQICO.FABLOCATION_ID = SAQSCE.FABLOCATION_ID 
							AND SAQICO.GREENBOOK = SAQSCE.GREENBOOK AND SAQICO.EQUIPMENT_ID = SAQSCE.EQUIPMENT_ID 
			JOIN SAQITM ON SAQICO.QUOTE_RECORD_ID = SAQITM.QUOTE_RECORD_ID AND SAQITM.QTEREV_RECORD_ID = SAQICO.QTEREV_RECORD_ID AND SAQITM.SERVICE_RECORD_ID = SAQICO.SERVICE_RECORD_ID
			{JoinString}
			WHERE SAQSCE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCE.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQSCE.SERVICE_ID = '{ServiceId}' AND ISNULL(SAQSCE.CONFIGURATION_STATUS,'') = 'COMPLETE' {WhereString}
		)""".format(
		QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id,
		JoinString=item_line_covered_object_entitlement_join_string, WhereString=item_line_covered_object_entitlement_where_string)
		Sql.RunQuery(SAQIEN_query)

		# Update - Start
		item_line_fablocation_join_string = ""	
		item_line_fablocation_where_string = ""		
		# if not self.service_id == 'Z0016':
		# 	item_line_fablocation_where_string += " AND ISNULL(SAQIFL.FABLOCATION_RECORD_ID,'') = '' "
		# 	item_line_fablocation_join_string += "LEFT JOIN SAQIFL (NOLOCK) ON SAQIFL.QUOTE_RECORD_ID = SAQICO.QUOTE_RECORD_ID AND SAQIFL.QTEREV_RECORD_ID = SAQICO.QTEREV_RECORD_ID AND SAQIFL.SERVICE_RECORD_ID = SAQICO.SERVICE_RECORD_ID AND SAQIFL.FABLOCATION_RECORD_ID = SAQICO.FABLOCATION_RECORD_ID "
		# Update - End

		# Sql.RunQuery(
		# 	"""INSERT SAQIFL(
		# 		FABLOCATION_ID,
		# 		FABLOCATION_NAME,
		# 		FABLOCATION_RECORD_ID,
		# 		SERVICE_ID,
		# 		SERVICE_DESCRIPTION,
		# 		SERVICE_RECORD_ID,
		# 		LINE_ITEM_ID,
		# 		QUOTE_ID,
		# 		QUOTE_NAME,
		# 		QUOTE_RECORD_ID,
		# 		QTEREV_ID,
		# 		QTEREV_RECORD_ID,
		# 		SALESORG_ID,
		# 		SALESORG_NAME,
		# 		SALESORG_RECORD_ID,
		# 		DOC_CURRENCY,
		# 		DOCCURR_RECORD_ID,
		# 		CONTRACT_VALID_FROM,
		# 		CONTRACT_VALID_TO,
		# 		GLOBAL_CURRENCY,
		# 		GLOBALCURRENCY_RECORD_ID,
		# 		QUOTE_ITEM_FAB_LOCATION_RECORD_ID,
		# 		CPQTABLEENTRYADDEDBY,
		# 		CPQTABLEENTRYDATEADDED,
		# 		CpqTableEntryModifiedBy, 
		# 		CpqTableEntryDateModified
		# 		) SELECT FB.*,CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_FAB_LOCATION_RECORD_ID,
		# 		'{UserName}' AS CPQTABLEENTRYADDEDBY,
		# 		GETDATE() as CPQTABLEENTRYDATEADDED,
		# 		{UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
		# 		SELECT DISTINCT
		# 		SAQICO.FABLOCATION_ID,
		# 		SAQICO.FABLOCATION_NAME,
		# 		SAQICO.FABLOCATION_RECORD_ID,
		# 		SAQICO.SERVICE_ID,
		# 		SAQICO.SERVICE_DESCRIPTION,
		# 		SAQICO.SERVICE_RECORD_ID,
		# 		SAQICO.LINE_ITEM_ID,
		# 		SAQICO.QUOTE_ID,
		# 		SAQICO.QUOTE_NAME,
		# 		SAQICO.QUOTE_RECORD_ID,
		# 		SAQICO.QTEREV_ID,
		# 		SAQICO.QTEREV_RECORD_ID,
		# 		SAQICO.SALESORG_ID,
		# 		SAQICO.SALESORG_NAME,
		# 		SAQICO.SALESORG_RECORD_ID,
		# 		SAQICO.DOC_CURRENCY,
		# 		SAQICO.DOCURR_RECORD_ID,
		# 		SAQICO.CONTRACT_VALID_FROM,
		# 		SAQICO.CONTRACT_VALID_TO,
		# 		SAQICO.GLOBAL_CURRENCY,
		# 		SAQICO.GLOBAL_CURRENCY_RECORD_ID
		# 		FROM SAQICO (NOLOCK)
		# 		JOIN MAFBLC (NOLOCK) ON SAQICO.FABLOCATION_ID = MAFBLC.FAB_LOCATION_ID 
		# 		JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQICO.QUOTE_RECORD_ID
		# 							AND SAQTMT.QTEREV_RECORD_ID = SAQICO.QTEREV_RECORD_ID
		# 		{JoinString}
		# 		WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}' {WhereString}
		# 		) FB""".format(
		# 						QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id,
		# 						UserId=self.user_id,
		# 						UserName=self.user_name,
		# 						ServiceId=self.service_id,
		# 						JoinString=item_line_fablocation_join_string,
		# 						WhereString=item_line_fablocation_where_string
		# 					)
		# )

	def _insert_quote_item_greenbook(self):	
		# Update - Start
		item_line_greenbook_join_string = ""	
		item_line_greenbook_where_string = ""		
		# if not self.service_id == 'Z0016':
		# 	item_line_greenbook_where_string += " AND ISNULL(SAQIGB.GREENBOOK_RECORD_ID,'') = '' "
		# 	item_line_greenbook_join_string += "LEFT JOIN SAQIGB (NOLOCK) ON SAQIGB.QUOTE_RECORD_ID = SAQICO.QUOTE_RECORD_ID AND SAQIGB.QTEREV_RECORD_ID = SAQICO.QTEREV_RECORD_ID AND SAQIGB.SERVICE_RECORD_ID = SAQICO.SERVICE_RECORD_ID AND SAQIGB.FABLOCATION_RECORD_ID = SAQICO.FABLOCATION_RECORD_ID AND SAQIGB.GREENBOOK_RECORD_ID = SAQICO.GREENBOOK_RECORD_ID"
		# Update - End	
		# Sql.RunQuery(
		# 	"""INSERT SAQIGB(
		# 		GREENBOOK,
		# 		GREENBOOK_RECORD_ID,
		# 		FABLOCATION_ID,
		# 		FABLOCATION_NAME,
		# 		FABLOCATION_RECORD_ID,
		# 		SERVICE_ID,
		# 		SERVICE_DESCRIPTION,
		# 		SERVICE_RECORD_ID,
		# 		LINE_ITEM_ID,
		# 		EQUIPMENT_QUANTITY,
		# 		GLOBAL_CURRENCY,
		# 		DOC_CURRENCY,
		# 		GLOBAL_CURRENCY_RECORD_ID,
		# 		DOCCURR_RECORD_ID,
		# 		CONTRACT_VALID_FROM,
		# 		CONTRACT_VALID_TO,
		# 		QUOTE_ID,
		# 		QUOTE_NAME,
		# 		QUOTE_RECORD_ID,
		# 		QTEREV_ID,
		# 		QTEREV_RECORD_ID,
		# 		SALESORG_ID,
		# 		SALESORG_NAME,
		# 		SALESORG_RECORD_ID,
		# 		QUOTE_ITEM_GREENBOOK_RECORD_ID,
		# 		CPQTABLEENTRYADDEDBY,
		# 		CPQTABLEENTRYDATEADDED,
		# 		CpqTableEntryModifiedBy, 
		# 		CpqTableEntryDateModified
		# 		) SELECT FB.*,CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_GREENBOOK_RECORD_ID,
		# 		'{UserName}' AS CPQTABLEENTRYADDEDBY,
		# 		GETDATE() as CPQTABLEENTRYDATEADDED, 
		# 		{UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
		# 		SELECT DISTINCT
		# 		SAQICO.GREENBOOK,
		# 		SAQICO.GREENBOOK_RECORD_ID,
		# 		SAQICO.FABLOCATION_ID,
		# 		SAQICO.FABLOCATION_NAME,
		# 		SAQICO.FABLOCATION_RECORD_ID,
		# 		SAQICO.SERVICE_ID,
		# 		SAQICO.SERVICE_DESCRIPTION,
		# 		SAQICO.SERVICE_RECORD_ID,
		# 		SAQICO.LINE_ITEM_ID,
		# 		SAQICO.EQUIPMENT_QUANTITY,
		# 		SAQICO.GLOBAL_CURRENCY,
		# 		SAQICO.DOC_CURRENCY,
		# 		SAQICO.GLOBAL_CURRENCY_RECORD_ID,
		# 		SAQICO.DOCURR_RECORD_ID,
		# 		SAQICO.CONTRACT_VALID_FROM,
		# 		SAQICO.CONTRACT_VALID_TO,
		# 		SAQICO.QUOTE_ID,
		# 		SAQICO.QUOTE_NAME,
		# 		SAQICO.QUOTE_RECORD_ID,
		# 		SAQICO.QTEREV_ID,
		# 		SAQICO.QTEREV_RECORD_ID,
		# 		SAQICO.SALESORG_ID,
		# 		SAQICO.SALESORG_NAME,
		# 		SAQICO.SALESORG_RECORD_ID
		# 		FROM SAQICO (NOLOCK)
		# 		JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQICO.QUOTE_RECORD_ID
		# 							AND SAQTMT.QTEREV_RECORD_ID = SAQICO.QTEREV_RECORD_ID
		# 		{JoinString}
		# 		WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}' {WhereString} 
		# 		) FB""".format(
		# 						QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id,
		# 						UserId=self.user_id,
		# 						UserName=self.user_name,
		# 						ServiceId=self.service_id,
		# 						JoinString=item_line_greenbook_join_string,
		# 						WhereString=item_line_greenbook_where_string
		# 					)
		# 	)

	def _quote_items_update(self):
		quote_item_obj = Sql.GetFirst("SELECT SERVICE_ID FROM SAQITM (NOLOCK) WHERE SERVICE_ID LIKE '{ServiceId}%' AND QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id))
		##spare part insert for ancillary
		#spare_parts_count_object = Sql.GetFirst("SELECT COUNT(PART_NUMBER) AS COUNT FROM SAQSPT (NOLOCK) WHERE QUOTE_RECORD_ID ='{}' AND QTEREV_RECORD_ID='{}' AND SERVICE_ID = '{}'".format(self.contract_quote_record_id,self.contract_quote_revision_record_id,self.service_id))
		get_simple_product = Sql.GetFirst("SELECT * FROM MAMTRL WHERE SAP_PART_NUMBER = '{}'".format(self.service_id))
		configuration_type = ""
		if get_simple_product:
			configuration_type = get_simple_product.MATERIALCONFIG_TYPE		
		if self.service_id == "Z0101" and configuration_type != "SIMPLE MATERIAL" :
			#Log.Info("In Z0101")
			self._insert_quote_item_forecast_parts()
			
		elif not quote_item_obj or self.service_id == 'Z0016':
			#Log.Info("In Z0016")
			self._quote_items_insert()				
			self._insert_quote_item_fab_location()
			self._insert_quote_item_greenbook()
		else:
			#Log.Info("In Z0091 OR 46")
			self._quote_item_delete_process()
			self._quote_items_insert()				
			self._insert_quote_item_fab_location()
			self._insert_quote_item_greenbook()	
		#Log.Info("update completed")
		return True
	
	def _insert_quote_item_forecast_parts(self, **kwargs):
		##Deleteing the tables before insert the data starts..

		#Log.Info("_insert_quote_item_forecast_parts ==> "+str(self.contract_quote_id)+" == Service Id == "+str(self.service_id))
		Sql.RunQuery("DELETE FROM SAQITM WHERE QUOTE_RECORD_ID = '{ContractQuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID LIKE '{ServiceId}%'".format(
			ContractQuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id
		))
			
		Sql.RunQuery("DELETE FROM SAQIFP WHERE QUOTE_RECORD_ID = '{ContractQuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID = '{ServiceId}'".format(
					ContractQuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id
				))
		
		##Deleteing the tables before insert the data ends..
		##Delete the native product before adding the product starts..
		for item in Quote.MainItems:
			if self.service_id == item.PartNumber:
				item.Delete()
		##Delete the native product before adding the product ends..
		quote_item_obj = Sql.GetFirst("SELECT TOP 1 ISNULL(LINE_ITEM_ID, 0) AS LINE_ITEM_ID FROM SAQITM (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' ORDER BY LINE_ITEM_ID DESC".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id))
		##quote item insert starts..
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
					CONTRACT_VALID_FROM,
					CONTRACT_VALID_TO,
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
					null AS PRICING_STATUS,
					SAQTMT.CONTRACT_VALID_FROM as LINE_ITEM_FROM_DATE,
					SAQTMT.CONTRACT_VALID_TO as LINE_ITEM_TO_DATE,
					SAQTMT.CONTRACT_VALID_FROM,
					SAQTMT.CONTRACT_VALID_TO,
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
				RevisionRecordId=self.contract_quote_revision_record_id,
				UserId=self.user_id,
				UserName=self.user_name,
				ExistingCount=int(float(quote_item_obj.LINE_ITEM_ID)) if quote_item_obj else 0
			))
		##quote item insert ends..
		quote_item_line_obj = Sql.GetFirst("SELECT TOP 1 ISNULL(EQUIPMENT_LINE_ID, 0) AS EQUIPMENT_LINE_ID FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' ORDER BY EQUIPMENT_LINE_ID DESC".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id))
		spare_quote_item_obj = Sql.GetFirst("SELECT LINE_ITEM_ID FROM SAQITM (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID LIKE '{ServiceId}%'".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
		if spare_quote_item_obj:
			##quote item spare parts insert starts..
			part_line_id_generation = "ROW_NUMBER()OVER(ORDER BY SAQSPT.PART_NUMBER) + {QuoteExistingLineId} as PART_LINE_ID".format(QuoteExistingLineId=quote_item_line_obj.EQUIPMENT_LINE_ID)

			quote_service_pare_quote_item_obj = Sql.GetFirst("SELECT PAR_SERVICE_ID FROM SAQTSV (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID = '{ServiceId}' AND ISNULL(PAR_SERVICE_ID,'') <> ''".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
			if quote_service_pare_quote_item_obj:
				part_line_id_generation = "{QuoteExistingLineId} + 1 as PART_LINE_ID".format(QuoteExistingLineId=quote_item_line_obj.EQUIPMENT_LINE_ID)
			
				
			Sql.RunQuery(
						"""
						INSERT SAQIFP (
							QUOTE_ITEM_FORECAST_PART_RECORD_ID,
							DELIVERY_MODE,
							EXTENDED_PRICE,
							PART_DESCRIPTION,
							PART_NUMBER,
							PART_RECORD_ID,
							QUOTE_ID,
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
							CPQTABLEENTRYADDEDBY, 
							CPQTABLEENTRYDATEADDED,
							CpqTableEntryModifiedBy,
							CpqTableEntryDateModified
							)SELECT CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_FORECAST_PART_RECORD_ID, A.* FROM( SELECT
							DISTINCT
							SAQSPT.DELIVERY_MODE,
							SAQSPT.EXTENDED_UNIT_PRICE,
							SAQSPT.PART_DESCRIPTION,
							SAQSPT.PART_NUMBER,
							SAQSPT.PART_RECORD_ID,
							SAQSPT.QUOTE_ID,
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
							RevisionRecordId=self.contract_quote_revision_record_id,
							status='ACQUIRING...',
							UserId=self.user_id,
							UserName=self.user_name,
							PartLineId=part_line_id_generation,
							LineItemId=spare_quote_item_obj.LINE_ITEM_ID
						)
					)
		##quote item spart parts insert ends..
		# Native Cart Items Insert for spare quotes- Start
		quote_items_obj = Sql.GetList("""SELECT TOP 1000 SAQTSV.SERVICE_ID FROM SAQITM (NOLOCK) JOIN SAQTSV (NOLOCK) ON SAQTSV.SERVICE_RECORD_ID = SAQITM.SERVICE_RECORD_ID AND SAQTSV.QUOTE_RECORD_ID = SAQITM.QUOTE_RECORD_ID AND SAQTSV.QTEREV_RECORD_ID = SAQITM.QTEREV_RECORD_ID WHERE SAQITM.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQITM.QTEREV_RECORD_ID = '{RevisionRecordId}' ORDER BY LINE_ITEM_ID ASC""".format(QuoteRecordId= self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id))
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
		total_year_3 = 0.00
		total_year_4 = 0.00
		total_year_5 = 0.00
		total_tax = 0.00
		total_extended_price = 0.00
		total_model_price = 0.00
		items_data = {}
		
		items_obj = Sql.GetList("SELECT SERVICE_ID, LINE_ITEM_ID,ISNULL(TOTAL_COST_WOSEEDSTOCK, 0) as TOTAL_COST_WOSEEDSTOCK,TOTAL_COST_WSEEDSTOCK,ISNULL(TARGET_PRICE, 0) as TARGET_PRICE,ISNULL(YEAR_1, 0) as YEAR_1,ISNULL(YEAR_2, 0) as YEAR_2, ISNULL(YEAR_3, 0) as YEAR_3,ISNULL(YEAR_4, 0) as YEAR_4, ISNULL(YEAR_5, 0) as YEAR_5, CURRENCY, ISNULL(YEAR_OVER_YEAR, 0) as YEAR_OVER_YEAR, OBJECT_QUANTITY FROM SAQITM (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' ".format(self.contract_quote_record_id,self.contract_quote_revision_record_id))
		if items_obj:
			for item_obj in items_obj:
				#getdecimalplacecurr = item_obj.CURRENCY
				items_data[int(float(item_obj.LINE_ITEM_ID))] = {'TOTAL_COST':item_obj.TOTAL_COST_WOSEEDSTOCK, 'TARGET_PRICE':item_obj.TARGET_PRICE, 'SERVICE_ID':(item_obj.SERVICE_ID.replace('- BASE', '')).strip(), 'YEAR_1':item_obj.YEAR_1, 'YEAR_2':item_obj.YEAR_2, 'YEAR_3':item_obj.YEAR_3, 'YEAR_4':item_obj.YEAR_4, 'YEAR_5':item_obj.YEAR_5, 'YEAR_OVER_YEAR':item_obj.YEAR_OVER_YEAR, 'OBJECT_QUANTITY':item_obj.OBJECT_QUANTITY}
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
					item.YEAR_3.Value = item_data.get('YEAR_3')
					total_year_3 += item.YEAR_3.Value
					item.YEAR_4.Value = item_data.get('YEAR_4')
					total_year_4 += item.YEAR_4.Value
					item.YEAR_5.Value = item_data.get('YEAR_5')
					total_year_5 += item.YEAR_5.Value
					total_tax += item.TAX.Value
					item.NET_VALUE.Value = item_data.get('TARGET_PRICE')
					total_extended_price += item.NET_VALUE.Value	
					item.OBJECT_QUANTITY.Value = item_data.get('OBJECT_QUANTITY')
		##controlling decimal based on currency
		if get_curr:
			get_decimal_place = Sql.GetFirst("SELECT DISPLAY_DECIMAL_PLACES FROM PRCURR (NOLOCK) WHERE CURRENCY ='{}'".format(get_curr))
			if get_decimal_place:
				decimal_value = get_decimal_place.DISPLAY_DECIMAL_PLACES
				formatting_string = "{0:." + str(decimal_value) + "f}"
				
				total_cost =formatting_string.format(total_cost)
				total_target_price =formatting_string.format(total_target_price)
				total_ceiling_price =formatting_string.format(total_ceiling_price)
				total_sls_discount_price =formatting_string.format(total_sls_discount_price)
				total_sales_price =formatting_string.format(total_sales_price)
				total_year_1 =formatting_string.format(total_year_1)
				total_year_2 =formatting_string.format(total_year_2)
				total_year_3 =formatting_string.format(total_year_3)
				total_year_4 =formatting_string.format(total_year_4)
				total_year_5 =formatting_string.format(total_year_5)
				total_tax =formatting_string.format(total_tax)
				total_extended_price =formatting_string.format(total_extended_price)
				total_model_price =formatting_string.format(total_model_price)
				total_bd_price =formatting_string.format(total_bd_price)
		
		# Quote.GetCustomField('TOTAL_COST').Content = str(total_cost) + " " + get_curr
		# Quote.GetCustomField('TARGET_PRICE').Content = str(total_target_price) + " " + get_curr
		# Quote.GetCustomField('CEILING_PRICE').Content = str(total_ceiling_price) + " " + get_curr
		# Quote.GetCustomField('SALES_DISCOUNTED_PRICE').Content = str(total_sls_discount_price) + " " + get_curr
		# Quote.GetCustomField('BD_PRICE_MARGIN').Content =str(total_bd_margin) + " %"
		# Quote.GetCustomField('BD_PRICE_DISCOUNT').Content = str(total_bd_price) + " %"
		# Quote.GetCustomField('TOTAL_NET_PRICE').Content =str(total_sales_price) + " " + get_curr
		# Quote.GetCustomField('YEAR_OVER_YEAR').Content =str(total_yoy) + " %"
		# Quote.GetCustomField('YEAR_1').Content = str(total_year_1) + " " + get_curr
		# Quote.GetCustomField('YEAR_2').Content = str(total_year_2) + " " + get_curr
		# Quote.GetCustomField('YEAR_3').Content = str(total_year_3) + " " + get_curr
		# Quote.GetCustomField('TAX').Content = str(total_tax) + " " + get_curr
		# Quote.GetCustomField('TOTAL_NET_VALUE').Content = str(total_extended_price) + " " + get_curr
		Quote.Save()
		
		Sql.RunQuery("""UPDATE SAQTRV
						SET 
						SAQTRV.TARGET_PRICE_INGL_CURR = IQ.TARGET_PRICE_INGL_CURR,
						SAQTRV.BD_PRICE_INGL_CURR = IQ.BD_PRICE_INGL_CURR,
						SAQTRV.CEILING_PRICE_INGL_CURR	= IQ.CEILING_PRICE_INGL_CURR,
						SAQTRV.TAX_AMOUNT_INGL_CURR = IQ.TAX_AMOUNT_INGL_CURR,						
						SAQTRV.NET_PRICE_INGL_CURR = IQ.NET_PRICE_INGL_CURR ,					
						SAQTRV.SLSDIS_PRICE_INGL_CURR = IQ.SLSDIS_PRICE_INGL_CURR,
						SAQTRV.YEAR_1_INGL_CURR = IQ.YEAR_1_INGL_CURR,
						SAQTRV.YEAR_2_INGL_CURR = IQ.YEAR_2_INGL_CURR		
						FROM SAQTRV (NOLOCK)
						INNER JOIN (SELECT SAQITM.QUOTE_RECORD_ID, SAQITM.QTEREV_RECORD_ID,
									SUM(ISNULL(SAQITM.TARGET_PRICE_INGL_CURR, 0)) as TARGET_PRICE_INGL_CURR,
									SUM(ISNULL(SAQITM.BD_PRICE_INGL_CURR, 0)) as BD_PRICE_INGL_CURR,
									SUM(ISNULL(SAQITM.CEILING_PRICE_INGL_CURR, 0)) as CEILING_PRICE_INGL_CURR,
									SUM(ISNULL(SAQITM.TAX_AMOUNT_INGL_CURR, 0)) as TAX_AMOUNT_INGL_CURR,
									SUM(ISNULL(SAQITM.NET_PRICE_INGL_CURR, 0)) as NET_PRICE_INGL_CURR,					
									SUM(ISNULL(SAQITM.SLSDIS_PRICE_INGL_CURR, 0)) as SLSDIS_PRICE_INGL_CURR,
									SUM(ISNULL(SAQITM.YEAR_1_INGL_CURR, 0)) as YEAR_1_INGL_CURR,
									SUM(ISNULL(SAQITM.YEAR_2_INGL_CURR, 0)) as YEAR_2_INGL_CURR						
									FROM SAQITM (NOLOCK) WHERE SAQITM.QUOTE_RECORD_ID = '{quote_rec_id}' AND SAQITM.QTEREV_RECORD_ID = '{quote_revision_rec_id}' GROUP BY SAQITM.QTEREV_RECORD_ID, SAQITM.QUOTE_RECORD_ID) IQ ON SAQTRV.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND SAQTRV.QUOTE_REVISION_RECORD_ID = IQ.QTEREV_RECORD_ID
						WHERE SAQTRV.QUOTE_RECORD_ID = '{quote_rec_id}' AND SAQTRV.QUOTE_REVISION_RECORD_ID = '{quote_revision_rec_id}' 	""".format( quote_rec_id = self.contract_quote_record_id,quote_revision_rec_id = self.contract_quote_revision_record_id ) )
		#assigning value to custom fields(quote summary section) in quote items node ends

		##calling the iflow for pricing..
		try:
			Log.Info("PART PRICING IFLOW STARTED!")
			CQPARTIFLW.iflow_pricing_call(str(self.user_name),str(self.contract_quote_id),str(self.contract_quote_revision_record_id))
		except:
			Log.Info("PART PRICING IFLOW ERROR!")

		##User story 4432 ends..

	def _simple_quote_item_insert_process(self, where_string='', join_string='', outer_where_string='', max_quote_item_count=0):
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
					CONTRACT_VALID_FROM,
					CONTRACT_VALID_TO,
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
					SAQSCO.QUOTE_RECORD_ID,
					SAQSCO.QUOTE_ID,
					SAQTMT.QUOTE_NAME,
					SAQTMT.QTEREV_ID,
					SAQTMT.QTEREV_RECORD_ID,
					'{UserName}' AS CPQTABLEENTRYADDEDBY,
					GETDATE() as CPQTABLEENTRYDATEADDED,
					{UserId} as CpqTableEntryModifiedBy,
					GETDATE() as CpqTableEntryDateModified,
					SAQSCO.SERVICE_DESCRIPTION,
					CONCAT(SAQSCO.SERVICE_ID, '- BASE') as SERVICE_ID,
					SAQSCO.SERVICE_RECORD_ID,
					SAQSCO.SALESORG_ID,
					SAQSCO.SALESORG_NAME,
					SAQSCO.SALESORG_RECORD_ID,
					'{line_item_count}' as LINE_ITEM_ID,
					0 as OBJECT_QUANTITY,
					1 as QUANTITY,
					SAQTMT.QUOTE_CURRENCY as CURRENCY,
					SAQTMT.QUOTE_CURRENCY_RECORD_ID as CURRENCY_RECORD_ID,
					'ZCB1' as ITEM_TYPE,
					'Active' as ITEM_STATUS,
					0 as NET_VALUE,
					MAMTRL.UNIT_OF_MEASURE, 
					MAMTRL.UOM_RECORD_ID,
					MAMSOP.PLANT_RECORD_ID,
					MAMSOP.PLANT_ID,
					null AS PRICING_STATUS,
					SAQTMT.CONTRACT_VALID_FROM as LINE_ITEM_FROM_DATE,
					SAQTMT.CONTRACT_VALID_TO as LINE_ITEM_TO_DATE,
					SAQTMT.CONTRACT_VALID_FROM,
					SAQTMT.CONTRACT_VALID_TO,
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
					FROM SAQSCO (NOLOCK)    
					JOIN (
						SELECT SAQSCE.QUOTE_RECORD_ID, SAQTSV.SERVICE_ID, MAX(SAQSCO.CpqTableEntryId) as CpqTableEntryId FROM SAQSCE (NOLOCK) INNER JOIN SAQTSV ON SAQSCE.QUOTE_RECORD_ID = SAQTSV.QUOTE_RECORD_ID  AND SAQSCE.QTEREV_RECORD_ID = SAQTSV.QTEREV_RECORD_ID AND SAQSCE.SERVICE_ID = SAQTSV.PAR_SERVICE_ID 
						INNER JOIN SAQSCO ON SAQSCE.QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID  AND SAQSCE.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID AND SAQSCE.EQUIPMENT_ID = SAQSCO.EQUIPMENT_ID AND SAQSCO.SERVICE_ID = SAQTSV.SERVICE_ID 
						WHERE SAQSCE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCE.QTEREV_RECORD_ID = '{RevisionRecordId}' AND ISNULL(CONFIGURATION_STATUS, '') = 'COMPLETE' AND SAQTSV.SERVICE_ID ='{service_id}' GROUP BY SAQSCE.QUOTE_RECORD_ID, SAQTSV.SERVICE_ID
						
					) AS IQ ON IQ.CpqTableEntryId = SAQSCO.CpqTableEntryId	
					JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID  AND SAQTMT.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID 
						
					JOIN MAMTRL (NOLOCK) ON MAMTRL.SAP_PART_NUMBER = SAQSCO.SERVICE_ID 
					JOIN SAQTRV (NOLOCK) ON  SAQTRV.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID AND SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID
					LEFT JOIN MAMSCT (NOLOCK) ON SAQTRV.DISTRIBUTIONCHANNEL_RECORD_ID = MAMSCT.DISTRIBUTIONCHANNEL_RECORD_ID AND SAQTRV.COUNTRY_RECORD_ID = MAMSCT.COUNTRY_RECORD_ID AND SAQTRV.DIVISION_ID = MAMSCT.DIVISION_ID  
					LEFT JOIN MAMSOP (NOLOCK) ON MAMSOP.SAP_PART_NUMBER = MAMTRL.SAP_PART_NUMBER AND MAMSOP.SALESORG_ID = SAQTRV.SALESORG_ID					
					LEFT JOIN PRCFVA (NOLOCK) ON PRCFVA.FACTOR_VARIABLE_ID = SAQSCO.SERVICE_ID AND PRCFVA.FACTOR_ID = 'YOYDIS'		
					{JoinString}			
					WHERE SAQSCO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCO.QTEREV_RECORD_ID = '{RevisionRecordId}' {WhereString} {OuterWhereString} 
			""".format(
				QuoteRecordId=self.contract_quote_record_id,
				RevisionRecordId=self.contract_quote_revision_record_id,
				UserId=self.user_id,
				UserName=self.user_name,
				WhereString=where_string,
				line_item_count= "{:.1f}".format(float(max_quote_item_count + 1)),
				JoinString=join_string,
				OuterWhereString=outer_where_string,
				service_id = self.service_id
			))

			
		# Insert SAQITM - End
		return True
	
	def _simple_quote_item_lines_insert_process(self, where_string='', join_condition_string='', join_string=''):
		equipments_count = 0
		quote_line_item_obj = Sql.GetFirst("SELECT max(EQUIPMENT_LINE_ID) as max FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id))
		if quote_line_item_obj:
			equipments_count = int(quote_line_item_obj.max) +1
		Quote.GetCustomField('PRICING_PICKLIST').Content = 'Document Currency'
		#Log.Info("PRICING_PICKLIST_Value_CHK_2 "+str(Quote.GetCustomField('PRICING_PICKLIST').Content))
		#Log.Info(" 1.equipments_count ===>"+str(equipments_count))
		##inserting SAQICO except chamber based equipment A055S000P01-6826	
		# ROW_NUMBER()OVER(ORDER BY(SAQSCO.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID)) * 1 + {EquipmentsCount} as EQUIPMENT_LINE_ID,			
		Sql.RunQuery("""INSERT SAQICO (BD_PRICE,ENTITLEMENT_PRICE_IMPACT,ENTITLEMENT_COST_IMPACT, EQUIPMENT_DESCRIPTION,STATUS,EQUIPMENT_ID, EQUIPMENT_RECORD_ID, FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, CONTRACT_VALID_FROM, CONTRACT_VALID_TO,LINE_ITEM_ID, MATERIAL_RECORD_ID, PLATFORM, QUOTE_ID, QTEITM_RECORD_ID, QUOTE_NAME, QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,KPU, NET_PRICE, SAP_PART_NUMBER, SERIAL_NO, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, WAFER_SIZE, TARGET_PRICE, TECHNOLOGY,SRVTAXCAT_RECORD_ID,SRVTAXCAT_DESCRIPTION,SRVTAXCAT_ID,SRVTAXCLA_DESCRIPTION,SRVTAXCLA_ID,BD_DISCOUNT, BD_DISCOUNT_RECORD_ID, BD_PRICE_MARGIN, BD_PRICE_MARGIN_RECORD_ID, CEILING_PRICE, CLEANING_COST, CM_PART_COST, CUSTOMER_TOOL_ID, EQUIPMENTCATEGORY_ID, EQUIPMENTCATEGORY_RECORD_ID, EQUIPMENT_STATUS, KPI_COST,MODEL_PRICE,TOTAL_COST_WOSEEDSTOCK,TOTAL_COST_WSEEDSTOCK, LABOR_COST, MNT_PLANT_ID, MNT_PLANT_NAME, MNT_PLANT_RECORD_ID, PM_PART_COST, SLSDIS_PRICE_MARGIN_RECORD_ID, SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID, TARGET_PRICE_MARGIN, TARGET_PRICE_MARGIN_RECORD_ID, WARRANTY_END_DATE, WARRANTY_START_DATE, GREENBOOK, GREENBOOK_RECORD_ID, EQUIPMENT_LINE_ID, NET_VALUE, SALES_DISCOUNT_PRICE, YEAR_1, YEAR_2, YEAR_3, YEAR_4, YEAR_5, EQUIPMENT_QUANTITY, YEAR_OVER_YEAR, EXCHANGE_RATE, EXCHANGE_RATE_DATE, EXCHANGE_RATE_RECORD_ID,GLOBAL_CURRENCY,DOC_CURRENCY,DOCURR_RECORD_ID, GLOBAL_CURRENCY_RECORD_ID, LINE, QUOTE_ITEM_COVERED_OBJECT_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified)
				SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_COVERED_OBJECT_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED,{UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
				SELECT DISTINCT
					null as BD_PRICE,
					0 as ENTITLEMENT_PRICE_IMPACT,
					0 AS ENTITLEMENT_COST_IMPACT,
					SAQSCO.EQUIPMENT_DESCRIPTION,
					null AS STATUS,
					SAQSCO.EQUIPMENT_ID,
					SAQSCO.EQUIPMENT_RECORD_ID,                        
					SAQSCO.FABLOCATION_ID, 
					SAQSCO.FABLOCATION_NAME, 
					SAQSCO.FABLOCATION_RECORD_ID,
					SAQSCO.CONTRACT_VALID_FROM,
					SAQSCO.CONTRACT_VALID_TO,
					SAQITM.LINE_ITEM_ID as LINE_ITEM_ID,
					SAQSCO.MATERIAL_RECORD_ID,
					SAQSCO.PLATFORM,
					SAQSCO.QUOTE_ID, 
					SAQITM.QUOTE_ITEM_RECORD_ID as QTEITM_RECORD_ID, 
					SAQSCO.QUOTE_NAME, 
					SAQSCO.QUOTE_RECORD_ID,
					SAQSCO.QTEREV_ID,
					SAQSCO.QTEREV_RECORD_ID,
					SAQSCO.KPU,
					null as NET_PRICE,
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
					null as BD_DISCOUNT, 
					null as BD_DISCOUNT_RECORD_ID, 
					null as BD_MARGIN, 
					null as BD_MARGIN_RECORD_ID, 
					null as CEILING_PRICE, 
					null as CLEANING_COST,
					null as CM_PART_COST, 
					SAQSCO.CUSTOMER_TOOL_ID, 
					SAQSCO.EQUIPMENTCATEGORY_ID, 
					SAQSCO.EQUIPMENTCATEGORY_RECORD_ID, 
					SAQSCO.EQUIPMENT_STATUS, 
					null as KPI_COST, 
					0 as MODEL_PRICE,
					0 as TOTAL_COST_WOSEEDSTOCK,
					0 as TOTAL_COST_WSEEDSTOCK,
					null as LABOR_COST, 
					SAQSCO.MNT_PLANT_ID, 
					SAQSCO.MNT_PLANT_NAME, 
					SAQSCO.MNT_PLANT_RECORD_ID,
					null as PM_PART_COST,
					null as SLSDIS_PRICE_MARGIN_RECORD_ID, 
					SAQSCO.SALESORG_ID, 
					SAQSCO.SALESORG_NAME, 
					SAQSCO.SALESORG_RECORD_ID, 
					null as TARGET_MARGIN, 
					null as TARGET_MARGIN_THRESHOLD_RECORD_ID,
					SAQSCO.WARRANTY_END_DATE, 
					SAQSCO.WARRANTY_START_DATE, 
					SAQSCO.GREENBOOK, 
					SAQSCO.GREENBOOK_RECORD_ID, 
					{EquipmentsCount} as EQUIPMENT_LINE_ID,					
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
					ISNULL(CONVERT(FLOAT,SAQTRV.EXCHANGE_RATE),'') AS EXCHANGE_RATE,
					SAQTRV.EXCHANGE_RATE_DATE,
					SAQTRV.EXCHANGERATE_RECORD_ID as EXCHANGE_RATE_RECORD_ID,
					SAQTRV.GLOBAL_CURRENCY,
					SAQTRV.DOC_CURRENCY,
					SAQTRV.DOCCURR_RECORD_ID,
					SAQTRV.GLOBAL_CURRENCY_RECORD_ID,
					SAQITM.LINE_ITEM_ID + '.'+ CAST(ROW_NUMBER()OVER(PARTITION BY SAQITM.LINE_ITEM_ID ORDER BY(SAQSCO.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID)) AS varchar ) as LINE
				FROM 
					SAQSCO (NOLOCK)					 
					JOIN (
						SELECT SAQSCE.QUOTE_RECORD_ID,SAQSCE.QTEREV_RECORD_ID, SAQTSV.SERVICE_ID,SAQSCE.EQUIPMENT_ID FROM SAQSCE (NOLOCK) INNER JOIN SAQTSV ON SAQSCE.QUOTE_RECORD_ID = SAQTSV.QUOTE_RECORD_ID  AND SAQSCE.QTEREV_RECORD_ID = SAQTSV.QTEREV_RECORD_ID AND SAQSCE.SERVICE_ID = SAQTSV.PAR_SERVICE_ID 
						WHERE SAQSCE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCE.QTEREV_RECORD_ID = '{RevisionRecordId}' AND ISNULL(CONFIGURATION_STATUS, '') = 'COMPLETE' AND SAQTSV.SERVICE_ID ='{service_id}'
						
					) AS IQ ON IQ.QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID AND IQ.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID AND IQ.SERVICE_ID = SAQSCO.SERVICE_ID	AND IQ.SERVICE_ID = '{service_id}'	AND IQ.EQUIPMENT_ID	 = SAQSCO.EQUIPMENT_ID	AND IQ.SERVICE_ID = '{service_id}'	
					
					JOIN MAMTRL (NOLOCK) ON MAMTRL.SAP_PART_NUMBER = SAQSCO.SERVICE_ID					
					JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID  AND SAQTMT.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID         
					JOIN SAQTRV (NOLOCK) ON SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID 
					JOIN SAQITM (NOLOCK) ON SAQTRV.QUOTE_RECORD_ID = SAQITM.QUOTE_RECORD_ID 
											AND SAQITM.SERVICE_RECORD_ID = SAQSCO.SERVICE_RECORD_ID
											AND SAQITM.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID
											{JoinConditionString}
					{JoinString}					
				WHERE 
					SAQSCO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCO.QTEREV_RECORD_ID = '{RevisionRecordId}' {WhereString} AND ISNULL(SAQSCO.INCLUDED,'') != 'CHAMBER' 
				) IQ
				""".format(UserId=self.user_id, UserName=self.user_name, QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id,
				JoinConditionString=join_condition_string, JoinString=join_string, WhereString=where_string, EquipmentsCount=equipments_count,service_id = self.service_id)
			)
				
		##inserting assembly to SAQICO if a equipemnt is chamber based FTS A055S000P01-6826
		if self.sale_type == 'TOOL RELOCATION':		
			quote_line_item_obj = Sql.GetFirst("SELECT EQUIPMENT_LINE_ID FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id))
			if quote_line_item_obj:
				equipments_count = int(quote_line_item_obj.EQUIPMENT_LINE_ID) + 1
			Sql.RunQuery("""INSERT SAQICO (BD_PRICE,ENTITLEMENT_PRICE_IMPACT,ENTITLEMENT_COST_IMPACT, EQUIPMENT_DESCRIPTION,STATUS,EQUIPMENT_ID, EQUIPMENT_RECORD_ID, FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, CONTRACT_VALID_FROM, CONTRACT_VALID_TO, LINE_ITEM_ID, MATERIAL_RECORD_ID, PLATFORM, QUOTE_ID, QTEITM_RECORD_ID, QUOTE_NAME, QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,KPU, NET_PRICE, SAP_PART_NUMBER, SERIAL_NO, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, WAFER_SIZE, TARGET_PRICE, TECHNOLOGY,SRVTAXCAT_RECORD_ID,SRVTAXCAT_DESCRIPTION,SRVTAXCAT_ID,SRVTAXCLA_DESCRIPTION,SRVTAXCLA_ID, BD_DISCOUNT, BD_DISCOUNT_RECORD_ID, BD_PRICE_MARGIN, BD_PRICE_MARGIN_RECORD_ID, CEILING_PRICE, CLEANING_COST, CM_PART_COST, CUSTOMER_TOOL_ID, EQUIPMENTCATEGORY_ID, EQUIPMENTCATEGORY_RECORD_ID, EQUIPMENT_STATUS, KPI_COST,MODEL_PRICE,TOTAL_COST_WOSEEDSTOCK,TOTAL_COST_WSEEDSTOCK, LABOR_COST, MNT_PLANT_ID, MNT_PLANT_NAME, MNT_PLANT_RECORD_ID, PM_PART_COST, SLSDIS_PRICE_MARGIN_RECORD_ID, SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID, TARGET_PRICE_MARGIN, TARGET_PRICE_MARGIN_RECORD_ID, WARRANTY_END_DATE, WARRANTY_START_DATE, GREENBOOK, GREENBOOK_RECORD_ID, EQUIPMENT_LINE_ID, NET_VALUE, SALES_DISCOUNT_PRICE, YEAR_1, YEAR_2, YEAR_3, YEAR_4, YEAR_5, EQUIPMENT_QUANTITY, YEAR_OVER_YEAR, EXCHANGE_RATE, EXCHANGE_RATE_DATE, EXCHANGE_RATE_RECORD_ID,GLOBAL_CURRENCY,DOC_CURRENCY,DOCURR_RECORD_ID, GLOBAL_CURRENCY_RECORD_ID, LINE,ASSEMBLY_ID,ASSEMBLY_RECORD_ID, QUOTE_ITEM_COVERED_OBJECT_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified)
					SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_COVERED_OBJECT_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED,{UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
					SELECT DISTINCT
						null as BD_PRICE,
						0 as ENTITLEMENT_PRICE_IMPACT,
						0 AS ENTITLEMENT_COST_IMPACT,
						SAQSCO.EQUIPMENT_DESCRIPTION,
						null AS STATUS,
						SAQSCO.EQUIPMENT_ID,
						SAQSCO.EQUIPMENT_RECORD_ID,                        
						SAQSCO.FABLOCATION_ID, 
						SAQSCO.FABLOCATION_NAME, 
						SAQSCO.FABLOCATION_RECORD_ID,
						SAQSCO.CONTRACT_VALID_FROM,
						SAQSCO.CONTRACT_VALID_TO,
						SAQITM.LINE_ITEM_ID as LINE_ITEM_ID,
						SAQSCO.MATERIAL_RECORD_ID,
						SAQSCO.PLATFORM,
						SAQSCO.QUOTE_ID, 
						SAQITM.QUOTE_ITEM_RECORD_ID as QTEITM_RECORD_ID, 
						SAQSCO.QUOTE_NAME, 
						SAQSCO.QUOTE_RECORD_ID,
						SAQSCO.QTEREV_ID,
						SAQSCO.QTEREV_RECORD_ID,
						SAQSCO.KPU,
						null as NET_PRICE,
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
						null as BD_DISCOUNT, 
						null as BD_DISCOUNT_RECORD_ID, 
						null as BD_MARGIN, 
						null as BD_MARGIN_RECORD_ID, 
						null as CEILING_PRICE, 
						null as CLEANING_COST,
						null as CM_PART_COST, 
						SAQSCO.CUSTOMER_TOOL_ID, 
						SAQSCO.EQUIPMENTCATEGORY_ID, 
						SAQSCO.EQUIPMENTCATEGORY_RECORD_ID, 
						SAQSCO.EQUIPMENT_STATUS, 
						null as KPI_COST, 
						0 as MODEL_PRICE,
						0 as TOTAL_COST_WOSEEDSTOCK,
						0 as TOTAL_COST_WSEEDSTOCK,
						null as LABOR_COST, 
						SAQSCO.MNT_PLANT_ID, 
						SAQSCO.MNT_PLANT_NAME, 
						SAQSCO.MNT_PLANT_RECORD_ID,
						null as PM_PART_COST, 
						null as SLSDIS_PRICE_MARGIN_RECORD_ID, 
						SAQSCO.SALESORG_ID, 
						SAQSCO.SALESORG_NAME, 
						SAQSCO.SALESORG_RECORD_ID, 
						null as TARGET_MARGIN, 
						null as TARGET_MARGIN_THRESHOLD_RECORD_ID,
						SAQSCO.WARRANTY_END_DATE, 
						SAQSCO.WARRANTY_START_DATE, 
						SAQSCO.GREENBOOK, 
						SAQSCO.GREENBOOK_RECORD_ID, 
						CASE WHEN MAMTRL.SERVICE_TYPE = 'NON TOOL BASED' 
								THEN CONVERT(INT, CONVERT(DECIMAL,SAQITM.LINE_ITEM_ID)) * 1 
								ELSE ROW_NUMBER()OVER(ORDER BY(SAQSCO.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID)) * 1 + {EquipmentsCount}
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
						ISNULL(CONVERT(FLOAT,SAQTRV.EXCHANGE_RATE),'') AS	EXCHANGE_RATE,
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
						JOIN (
							SELECT SAQSCE.QUOTE_RECORD_ID,SAQSCE.QTEREV_RECORD_ID, SAQTSV.SERVICE_ID,SAQSCE.EQUIPMENT_ID FROM SAQSCE (NOLOCK) INNER JOIN SAQTSV ON SAQSCE.QUOTE_RECORD_ID = SAQTSV.QUOTE_RECORD_ID  AND SAQSCE.QTEREV_RECORD_ID = SAQTSV.QTEREV_RECORD_ID AND SAQSCE.SERVICE_ID = SAQTSV.PAR_SERVICE_ID 
							WHERE SAQSCE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCE.QTEREV_RECORD_ID = '{RevisionRecordId}' AND ISNULL(CONFIGURATION_STATUS, '') = 'COMPLETE' AND SAQTSV.SERVICE_ID ='{service_id}'
							
						) AS IQ ON IQ.QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID AND IQ.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID AND IQ.SERVICE_ID = SAQSCO.SERVICE_ID	AND IQ.SERVICE_ID = '{service_id}'	AND IQ.EQUIPMENT_ID	 = SAQSCO.EQUIPMENT_ID	AND IQ.SERVICE_ID = '{service_id}'
						JOIN MAMTRL (NOLOCK) ON MAMTRL.SAP_PART_NUMBER = SAQSCE.SERVICE_ID
						JOIN SAQSCA (NOLOCK) ON SAQSCA.QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID AND SAQSCA.SERVICE_ID = SAQSCO.SERVICE_ID AND SAQSCA.EQUIPMENT_RECORD_ID = SAQSCO.EQUIPMENT_RECORD_ID
						AND SAQSCA.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID						
						JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID  AND SAQTMT.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID       
						JOIN SAQTRV (NOLOCK) ON SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID  AND SAQTRV.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID 
						JOIN SAQITM (NOLOCK) ON SAQTRV.QUOTE_RECORD_ID = SAQITM.QUOTE_RECORD_ID 
												AND SAQITM.SERVICE_RECORD_ID = SAQSCO.SERVICE_RECORD_ID
												AND SAQITM.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID
												{JoinConditionString}
												
						{JoinString}						
					WHERE 
						SAQSCO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCO.QTEREV_RECORD_ID = '{RevisionRecordId}' {WhereString} AND ISNULL(SAQSCO.INCLUDED,'') = 'CHAMBER' AND SAQSCA.INCLUDED = 1 
					) IQ
					""".format(UserId=self.user_id, UserName=self.user_name, QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id, 
					JoinConditionString=join_condition_string, JoinString=join_string, WhereString= str(where_string), EquipmentsCount=equipments_count,service_id = self.service_id)
				)					
		return True
		
	def _do_opertion(self):
		#Log.Info("-===========>> _do_opertion"+str(self.contract_quote_id)+" ====== "+str(self.action_type))
		if self.action_type == "INSERT_LINE_ITEMS":
			spare_parts_count_object = Sql.GetFirst("SELECT COUNT(PART_NUMBER) AS COUNT FROM SAQSPT (NOLOCK) WHERE QUOTE_RECORD_ID ='{}' AND QTEREV_RECORD_ID='{}' AND SERVICE_ID = '{}'".format(self.contract_quote_record_id,self.contract_quote_revision_record_id,self.service_id))
			
			if spare_parts_count_object:
				if spare_parts_count_object.COUNT > 0:
					self._insert_quote_item_forecast_parts()
				else:	
					#Log.Info("-===========>> _do_opertion if else"+str(self.contract_quote_id)+" ====== "+str(self.action_type))
					self._quote_items_insert()
					#batch_group_record_id = str(Guid.NewGuid()).upper()
					self._insert_quote_item_fab_location()
					self._insert_quote_item_greenbook()
			else:	
				#Log.Info("-===========>> _do_opertion else"+str(self.contract_quote_id)+" ====== "+str(self.action_type))
				self._quote_items_insert()
				#batch_group_record_id = str(Guid.NewGuid()).upper()
				self._insert_quote_item_fab_location()
				self._insert_quote_item_greenbook()		
		else:
			#Log.Info("-===========>> _do_opertion update"+str(self.contract_quote_id)+" ====== "+str(self.action_type))
			self._quote_items_update()	
		# Pricing Calculation
		quote_line_item_obj = Sql.GetFirst("SELECT EQUIPMENT_LINE_ID FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID = '{ServiceId}' AND ISNULL(STATUS,'') = ''".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
		if quote_line_item_obj:
			ScriptExecutor.ExecuteGlobal('QTPOSTACRM',{'QUOTE_ID':self.contract_quote_id,'REVISION_ID':self.contract_quote_revision_id, 'Fun_type':'cpq_to_sscm'})
		return True

try:
	where_condition_string = Param.WhereString
except:
	where_condition_string = ''
#Log.Info("CQINSQTITM ---- called")
action_type = Param.ActionType
parameters = {}
keysofparameters = {
	"QUOTE_RECORD_ID" : "contract_quote_record_id",
	"QTEREV_RECORD_ID" : "contract_quote_revision_record_id",
	"SERVICE_ID" : "service_id",
	"GREENBOOK" : "greenbook_id",
	"FABLOCATION_ID" : "fablocation_id",
	"EQUIPMENT_ID" : "equipment_id",
}
parameters['action_type']=str(action_type)
if action_type == "UPDATE_LINE_ITEMS":
	for key in keysofparameters.keys():
		if str(key) in where_condition_string:
			pattern = re.compile(r''+str(key)+'\s*\=\s*\'([^>]*?)\'')
			result = re.search(pattern, where_condition_string).group(1)
			parameters[keysofparameters[key]]=str(result)	
else:
	parameters[keysofparameters['QUOTE_RECORD_ID']]=str(Param.ContractQuoteRecordId)
	parameters[keysofparameters['QTEREV_RECORD_ID']]=str(Param.ContractQuoteRevisionRecordId)
	parameters[keysofparameters['SERVICE_ID']]=str(Param.ServiceId)
Log.Info("CQINSQTITM ================>"+str(**parameters))	
contract_quote_item_obj = ContractQuoteItem(**parameters)
contract_quote_item_obj._do_opertion()
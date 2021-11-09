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
		self._set_service_type()	
		self._get_material_type()
	
	def set_contract_quote_related_details(self):
		contract_quote_obj = Sql.GetFirst("SELECT QUOTE_ID, QUOTE_TYPE, SALE_TYPE, C4C_QUOTE_ID, QTEREV_ID, QUOTE_CURRENCY, QUOTE_CURRENCY_RECORD_ID FROM SAQTMT (NOLOCK) WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{QuoteRecordId}'".format(QuoteRecordId=self.contract_quote_record_id))
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
	
	def _set_service_type(self):
		spare_parts_count_object = Sql.GetFirst("SELECT CpqTableEntryId FROM SAQSPT (NOLOCK) WHERE QUOTE_RECORD_ID ='{QuoteRecordId}' AND QTEREV_RECORD_ID='{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id))			
		if spare_parts_count_object:
			self.is_spare_service = True
		else:
			self.is_spare_service = False
		return True

	def _get_material_type(self):
		get_service_config_type = Sql.GetFirst("SELECT * FROM MAMTRL WHERE SAP_PART_NUMBER = '{}' AND MATERIALCONFIG_TYPE = 'SIMPLE MATERIAL'".format(self.service_id))
		if get_service_config_type:
			self.is_simple_service = True
		else:
			self.is_simple_service = False


	
	def _quote_annualized_items_insert(self):
		Sql.RunQuery("""INSERT SAQICO (EQUIPMENT_DESCRIPTION,STATUS,EQUIPMENT_ID, EQUIPMENT_RECORD_ID, FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, CONTRACT_VALID_FROM, CONTRACT_VALID_TO,LINE_ITEM_ID, MATERIAL_RECORD_ID, PLATFORM, QUOTE_ID, QTEITM_RECORD_ID, QUOTE_NAME, QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,KPU, SAP_PART_NUMBER, SERIAL_NO, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, WAFER_SIZE, TECHNOLOGY,SRVTAXCAT_RECORD_ID,SRVTAXCAT_DESCRIPTION,SRVTAXCAT_ID,SRVTAXCLA_DESCRIPTION,SRVTAXCLA_ID,SRVTAXCLA_RECORD_ID, CUSTOMER_TOOL_ID, EQUIPMENTCATEGORY_ID, EQUIPMENTCATEGORY_RECORD_ID, EQUIPMENT_STATUS, MNT_PLANT_ID, MNT_PLANT_NAME, MNT_PLANT_RECORD_ID, SLSDIS_PRICE_MARGIN_RECORD_ID, SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID, TARGET_PRICE_MARGIN, TARGET_PRICE_MARGIN_RECORD_ID, WARRANTY_END_DATE, WARRANTY_START_DATE, GREENBOOK, GREENBOOK_RECORD_ID, EQUIPMENT_LINE_ID, EQUIPMENT_QUANTITY, YEAR_OVER_YEAR, EXCHANGE_RATE, EXCHANGE_RATE_DATE, EXCHANGE_RATE_RECORD_ID,GLOBAL_CURRENCY,DOC_CURRENCY,DOCURR_RECORD_ID, GLOBAL_CURRENCY_RECORD_ID, LINE, QUOTE_ITEM_COVERED_OBJECT_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified)
				SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_COVERED_OBJECT_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED,{UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
				SELECT DISTINCT					
					SAQSCO.EQUIPMENT_DESCRIPTION,
					null AS STATUS,
					SAQSCO.EQUIPMENT_ID,
					SAQSCO.EQUIPMENT_RECORD_ID,                        
					SAQSCO.FABLOCATION_ID, 
					SAQSCO.FABLOCATION_NAME, 
					SAQSCO.FABLOCATION_RECORD_ID,
					SAQSCO.CONTRACT_VALID_FROM,
					SAQSCO.CONTRACT_VALID_TO,
					SAQRIT.LINE as LINE_ITEM_ID,
					SAQSCO.MATERIAL_RECORD_ID,
					SAQSCO.PLATFORM,
					SAQSCO.QUOTE_ID, 
					SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID, 
					SAQSCO.QUOTE_NAME, 
					SAQSCO.QUOTE_RECORD_ID,
					SAQSCO.QTEREV_ID,
					SAQSCO.QTEREV_RECORD_ID,
					SAQSCO.KPU,
					SAQSCO.SAP_PART_NUMBER, 
					SAQSCO.SERIAL_NO, 
					SAQSCO.SERVICE_DESCRIPTION, 
					SAQSCO.SERVICE_ID, 
					SAQSCO.SERVICE_RECORD_ID, 
					SAQSCO.WAFER_SIZE,					
					SAQSCO.TECHNOLOGY,  
					SAQITM.SRVTAXCAT_RECORD_ID,
					SAQITM.SRVTAXCAT_DESCRIPTION,
					SAQITM.SRVTAXCAT_ID,
					SAQITM.SRVTAXCLA_DESCRIPTION,
					SAQITM.SRVTAXCLA_ID,
					SAQITM.SRVTAXCLA_RECORD_ID,					
					SAQSCO.CUSTOMER_TOOL_ID, 
					SAQSCO.EQUIPMENTCATEGORY_ID, 
					SAQSCO.EQUIPMENTCATEGORY_RECORD_ID, 
					SAQSCO.EQUIPMENT_STATUS,					
					SAQSCO.MNT_PLANT_ID, 
					SAQSCO.MNT_PLANT_NAME, 
					SAQSCO.MNT_PLANT_RECORD_ID,					
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
					ROW_NUMBER()OVER(ORDER BY(SAQSCO.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID)) * 1 + {EquipmentsCount} as EQUIPMENT_LINE_ID,
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
					SAQRIT (NOLOCK)			
					JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID         
					JOIN SAQTRV (NOLOCK) ON SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID 
					{JoinString}					
				WHERE 
					SAQRIT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQRIT.SERVICE_ID = '{ServiceId}'
				) IQ
				""".format(UserId=self.user_id, UserName=self.user_name, QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id, JoinString='')
			)
	
	def _quote_items_object_insert(self):
		Log.Info("_quote_items_object_insert ===> 1"+str("""INSERT SAQRIO (CUSTOMER_TOOL_ID, EQUIPMENT_DESCRIPTION, EQUIPMENT_ID, EQUIPMENT_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID, KPU, LINE, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, QTEITM_RECORD_ID, QUOTE_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, SERIAL_NUMBER, TECHNOLOGY, TOOL_CONFIGURATION, WAFER_SIZE, QUOTE_REVISION_ITEM_OBJECT, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified)
				SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REVISION_ITEM_OBJECT, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED,{UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
				SELECT DISTINCT
					SAQSCO.CUSTOMER_TOOL_ID,
					SAQSCO.EQUIPMENT_DESCRIPTION,					
					SAQSCO.EQUIPMENT_ID,
					SAQSCO.EQUIPMENT_RECORD_ID,                        
					SAQSCO.GREENBOOK, 
					SAQSCO.GREENBOOK_RECORD_ID,
					SAQSCO.KPU,
					SAQRIT.LINE as LINE,
					SAQSCO.SERVICE_DESCRIPTION, 
					SAQSCO.SERVICE_ID, 
					SAQSCO.SERVICE_RECORD_ID, 
					SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID, 
					SAQSCO.QUOTE_ID,
					SAQSCO.QUOTE_RECORD_ID,
					SAQSCO.QTEREV_ID,
					SAQSCO.QTEREV_RECORD_ID,
					SAQSCO.SERIAL_NO as SERIAL_NUMBER, 
					SAQSCO.TECHNOLOGY, 
					PRPRBM.TOOL_CONFIGURATION,
					SAQSCO.WAFER_SIZE					
				FROM 
					SAQSCO (NOLOCK)					 
					JOIN SAQSCE (NOLOCK) ON SAQSCE.QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID AND SAQSCE.SERVICE_ID = SAQSCO.SERVICE_ID AND SAQSCE.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID
					AND SAQSCE.EQUIPMENT_RECORD_ID = SAQSCO.EQUIPMENT_RECORD_ID
					JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID         
					JOIN SAQTRV (NOLOCK) ON SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID 
					JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = SAQTRV.QUOTE_RECORD_ID
											AND SAQRIT.SERVICE_RECORD_ID = SAQSCO.SERVICE_RECORD_ID
											AND SAQRIT.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID
											AND SAQRIT.FABLOCATION_RECORD_ID = SAQSCO.FABLOCATION_RECORD_ID
											AND SAQRIT.GREENBOOK_RECORD_ID = SAQSCO.GREENBOOK_RECORD_ID
					LEFT JOIN PRPRBM (NOLOCK) ON PRPRBM.ACCOUNT_RECORD_ID = SAQTMT.ACCOUNT_RECORD_ID AND PRPRBM.EQUIPMENT_RECORD_ID = SAQSCO.EQUIPMENT_RECORD_ID AND PRPRBM.SERVICE_RECORD_ID = SAQSCO.SERVICE_RECORD_ID		
					{JoinString}					
				WHERE 
					SAQSCO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQSCO.SERVICE_ID = '{ServiceId}' AND ISNULL(SAQSCE.CONFIGURATION_STATUS,'') = 'COMPLETE'
				) IQ
				""".format(UserId=self.user_id, UserName=self.user_name, QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id,
				JoinString='')))
		Sql.RunQuery("""INSERT SAQRIO (CUSTOMER_TOOL_ID, EQUIPMENT_DESCRIPTION, EQUIPMENT_ID, EQUIPMENT_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID, KPU, LINE, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, QTEITM_RECORD_ID, QUOTE_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, SERIAL_NUMBER, TECHNOLOGY, TOOL_CONFIGURATION, WAFER_SIZE, QUOTE_REVISION_ITEM_OBJECT, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified)
				SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REVISION_ITEM_OBJECT, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED,{UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
				SELECT DISTINCT
					SAQSCO.CUSTOMER_TOOL_ID,
					SAQSCO.EQUIPMENT_DESCRIPTION,					
					SAQSCO.EQUIPMENT_ID,
					SAQSCO.EQUIPMENT_RECORD_ID,                        
					SAQSCO.GREENBOOK, 
					SAQSCO.GREENBOOK_RECORD_ID,
					SAQSCO.KPU,
					SAQRIT.LINE as LINE,
					SAQSCO.SERVICE_DESCRIPTION, 
					SAQSCO.SERVICE_ID, 
					SAQSCO.SERVICE_RECORD_ID, 
					SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID, 
					SAQSCO.QUOTE_ID,
					SAQSCO.QUOTE_RECORD_ID,
					SAQSCO.QTEREV_ID,
					SAQSCO.QTEREV_RECORD_ID,
					SAQSCO.SERIAL_NO as SERIAL_NUMBER, 
					SAQSCO.TECHNOLOGY, 
					PRPRBM.TOOL_CONFIGURATION,
					SAQSCO.WAFER_SIZE					
				FROM 
					SAQSCO (NOLOCK)					 
					JOIN SAQSCE (NOLOCK) ON SAQSCE.QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID AND SAQSCE.SERVICE_ID = SAQSCO.SERVICE_ID AND SAQSCE.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID
					AND SAQSCE.EQUIPMENT_RECORD_ID = SAQSCO.EQUIPMENT_RECORD_ID
					JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID         
					JOIN SAQTRV (NOLOCK) ON SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID 
					JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = SAQTRV.QUOTE_RECORD_ID
											AND SAQRIT.SERVICE_RECORD_ID = SAQSCO.SERVICE_RECORD_ID
											AND SAQRIT.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID
											AND SAQRIT.FABLOCATION_RECORD_ID = SAQSCO.FABLOCATION_RECORD_ID
											AND SAQRIT.GREENBOOK_RECORD_ID = SAQSCO.GREENBOOK_RECORD_ID
					LEFT JOIN PRPRBM (NOLOCK) ON PRPRBM.ACCOUNT_RECORD_ID = SAQTMT.ACCOUNT_RECORD_ID AND PRPRBM.EQUIPMENT_RECORD_ID = SAQSCO.EQUIPMENT_RECORD_ID AND PRPRBM.SERVICE_RECORD_ID = SAQSCO.SERVICE_RECORD_ID		
					{JoinString}					
				WHERE 
					SAQSCO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQSCO.SERVICE_ID = '{ServiceId}' AND ISNULL(SAQSCE.CONFIGURATION_STATUS,'') = 'COMPLETE'
				) IQ
				""".format(UserId=self.user_id, UserName=self.user_name, QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id,
				JoinString='')
			)
	
	def _quote_items_insert(self):
		Log.Info("_quote_items_insert ===> 1")
		service_entitlement_obj = Sql.GetFirst("""SELECT ENTITLEMENT_ID,ENTITLEMENT_DISPLAY_VALUE FROM 
										(
											SELECT DISTINCT 
													IQ.QUOTE_RECORD_ID,
													IQ.QTEREV_RECORD_ID, 
													replace(X.Y.value('(ENTITLEMENT_ID)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_ID,
													replace(X.Y.value('(ENTITLEMENT_DISPLAY_VALUE)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_DISPLAY_VALUE
											FROM (
												SELECT QUOTE_RECORD_ID,QTEREV_RECORD_ID,CONVERT(xml,replace(ENTITLEMENT_XML,'&',';#38')) as ENTITLEMENT_XML 
												FROM SAQTSE (NOLOCK) 
												WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' and SERVICE_ID = '{ServiceId}' 
												) IQ 
											OUTER APPLY IQ.ENTITLEMENT_XML.nodes('QUOTE_ITEM_ENTITLEMENT') as X(Y) 
										) as OQ 
										WHERE ENTITLEMENT_ID LIKE '{EntitlementAttrId}'""".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id,EntitlementAttrId='AGS_'+str(self.service_id)+'_PQB_QTITST'))
		if service_entitlement_obj:
			Log.Info("_quote_items_insert ===> 2"+str(service_entitlement_obj.ENTITLEMENT_DISPLAY_VALUE))
			source_object_name = ''
			if (service_entitlement_obj.ENTITLEMENT_DISPLAY_VALUE).upper() == 'OFFERING + EQUIPMENT':
				source_object_name = 'SAQSCE'
			elif (service_entitlement_obj.ENTITLEMENT_DISPLAY_VALUE).upper() == 'OFFERING + FAB + GREENBOOK + GROUP OF EQUIPMENT':
				source_object_name = 'SAQSGE'
			else:
				return False
			if source_object_name:
				Log.Info("_quote_items_insert ===> 3"+str("""INSERT SAQRIT (QUOTE_REVISION_CONTRACT_ITEM_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified, CONTRACT_VALID_FROM, CONTRACT_VALID_TO, DOC_CURRENCY, DOCURR_RECORD_ID, EXCHANGE_RATE, EXCHANGE_RATE_DATE, EXCHANGE_RATE_RECORD_ID, GL_ACCOUNT_NO, GLOBAL_CURRENCY, GLOBAL_CURRENCY_RECORD_ID, LINE, OBJECT_ID, OBJECT_TYPE, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, PROFIT_CENTER, QUANTITY, QUOTE_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, REF_SALESORDER, STATUS, TAXCLASSIFICATION_DESCRIPTION, TAXCLASSIFICATION_ID, TAXCLASSIFICATION_RECORD_ID, FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID)
					SELECT
						CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REVISION_CONTRACT_ITEM_ID,
						'{UserName}' AS CPQTABLEENTRYADDEDBY,
						GETDATE() as CPQTABLEENTRYDATEADDED,
						{UserId} as CpqTableEntryModifiedBy,
						GETDATE() as CpqTableEntryDateModified,
						SAQTMT.CONTRACT_VALID_FROM,
						SAQTMT.CONTRACT_VALID_TO,
						SAQTRV.DOC_CURRENCY,
						SAQTRV.DOCCURR_RECORD_ID as DOCURR_RECORD_ID,
						ISNULL(CONVERT(FLOAT,SAQTRV.EXCHANGE_RATE),'') AS EXCHANGE_RATE,
						SAQTRV.EXCHANGE_RATE_DATE,
						SAQTRV.EXCHANGERATE_RECORD_ID as EXCHANGE_RATE_RECORD_ID,
						null as GL_ACCOUNT_NO,
						SAQTRV.GLOBAL_CURRENCY,
						SAQTRV.GLOBAL_CURRENCY_RECORD_ID,
						ROW_NUMBER()OVER(ORDER BY({ObjectName}.CpqTableEntryId)) + {EquipmentsCount} as LINE,
						null as OBJECT_ID,
						null as OBJECT_TYPE,
						{ObjectName}.SERVICE_DESCRIPTION,
						{ObjectName}.SERVICE_ID,
						{ObjectName}.SERVICE_RECORD_ID,
						null as PROFIT_CENTER,
						1 as QUANTITY,
						SAQTRV.QUOTE_ID,
						SAQTRV.QUOTE_RECORD_ID,
						SAQTMT.QTEREV_ID,
						SAQTMT.QTEREV_RECORD_ID,
						null as REF_SALESORDER,
						null as STATUS,
						MAMSCT.TAXCLASSIFICATION_DESCRIPTION,
						MAMSCT.TAXCLASSIFICATION_ID,
						MAMSCT.TAXCLASSIFICATION_RECORD_ID,
						{ObjectName}.FABLOCATION_ID,
						{ObjectName}.FABLOCATION_NAME,
						{ObjectName}.FABLOCATION_RECORD_ID,
						{ObjectName}.GREENBOOK,
						{ObjectName}.GREENBOOK_RECORD_ID
					FROM {ObjectName} (NOLOCK) 
					JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = {ObjectName}.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = {ObjectName}.QTEREV_RECORD_ID     
					JOIN SAQTRV (NOLOCK) ON SAQTRV.SALESORG_RECORD_ID = {ObjectName}.SALESORG_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = {ObjectName}.QTEREV_RECORD_ID AND SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID
					JOIN MAMTRL (NOLOCK) ON MAMTRL.SAP_PART_NUMBER = {ObjectName}.SERVICE_ID 
					LEFT JOIN MAMSCT (NOLOCK) ON MAMSCT.DISTRIBUTIONCHANNEL_RECORD_ID = SAQTRV.DISTRIBUTIONCHANNEL_RECORD_ID AND MAMSCT.COUNTRY_RECORD_ID = SAQTRV.COUNTRY_RECORD_ID AND MAMSCT.DIVISION_ID = SAQTRV.DIVISION_ID AND MAMSCT.SAP_PART_NUMBER = MAMTRL.SAP_PART_NUMBER
					WHERE {ObjectName}.QUOTE_RECORD_ID = '{QuoteRecordId}' AND {ObjectName}.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND {ObjectName}.SERVICE_ID = '{ServiceId}' AND ISNULL({ObjectName}.CONFIGURATION_STATUS,'') = 'COMPLETE'			
				""".format(UserId=self.user_id, UserName=self.user_name, ObjectName=source_object_name, QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id, EquipmentsCount=0)))
				Sql.RunQuery("""INSERT SAQRIT (QUOTE_REVISION_CONTRACT_ITEM_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified, CONTRACT_VALID_FROM, CONTRACT_VALID_TO, DOC_CURRENCY, DOCURR_RECORD_ID, EXCHANGE_RATE, EXCHANGE_RATE_DATE, EXCHANGE_RATE_RECORD_ID, GL_ACCOUNT_NO, GLOBAL_CURRENCY, GLOBAL_CURRENCY_RECORD_ID, LINE, OBJECT_ID, OBJECT_TYPE, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, PROFIT_CENTER, QUANTITY, QUOTE_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, REF_SALESORDER, STATUS, TAXCLASSIFICATION_DESCRIPTION, TAXCLASSIFICATION_ID, TAXCLASSIFICATION_RECORD_ID, FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID)
					SELECT
						CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REVISION_CONTRACT_ITEM_ID,
						'{UserName}' AS CPQTABLEENTRYADDEDBY,
						GETDATE() as CPQTABLEENTRYDATEADDED,
						{UserId} as CpqTableEntryModifiedBy,
						GETDATE() as CpqTableEntryDateModified,
						SAQTMT.CONTRACT_VALID_FROM,
						SAQTMT.CONTRACT_VALID_TO,
						SAQTRV.DOC_CURRENCY,
						SAQTRV.DOCCURR_RECORD_ID as DOCURR_RECORD_ID,
						ISNULL(CONVERT(FLOAT,SAQTRV.EXCHANGE_RATE),'') AS EXCHANGE_RATE,
						SAQTRV.EXCHANGE_RATE_DATE,
						SAQTRV.EXCHANGERATE_RECORD_ID as EXCHANGE_RATE_RECORD_ID,
						null as GL_ACCOUNT_NO,
						SAQTRV.GLOBAL_CURRENCY,
						SAQTRV.GLOBAL_CURRENCY_RECORD_ID,
						ROW_NUMBER()OVER(ORDER BY({ObjectName}.CpqTableEntryId)) + {EquipmentsCount} as LINE,
						null as OBJECT_ID,
						null as OBJECT_TYPE,
						{ObjectName}.SERVICE_DESCRIPTION,
						{ObjectName}.SERVICE_ID,
						{ObjectName}.SERVICE_RECORD_ID,
						null as PROFIT_CENTER,
						1 as QUANTITY,
						SAQTRV.QUOTE_ID,
						SAQTRV.QUOTE_RECORD_ID,
						SAQTMT.QTEREV_ID,
						SAQTMT.QTEREV_RECORD_ID,
						null as REF_SALESORDER,
						null as STATUS,
						MAMSCT.TAXCLASSIFICATION_DESCRIPTION,
						MAMSCT.TAXCLASSIFICATION_ID,
						MAMSCT.TAXCLASSIFICATION_RECORD_ID,
						{ObjectName}.FABLOCATION_ID,
						{ObjectName}.FABLOCATION_NAME,
						{ObjectName}.FABLOCATION_RECORD_ID,
						{ObjectName}.GREENBOOK,
						{ObjectName}.GREENBOOK_RECORD_ID
					FROM {ObjectName} (NOLOCK) 
					JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = {ObjectName}.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = {ObjectName}.QTEREV_RECORD_ID     
					JOIN SAQTRV (NOLOCK) ON SAQTRV.SALESORG_RECORD_ID = {ObjectName}.SALESORG_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = {ObjectName}.QTEREV_RECORD_ID AND SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID
					JOIN MAMTRL (NOLOCK) ON MAMTRL.SAP_PART_NUMBER = {ObjectName}.SERVICE_ID 
					LEFT JOIN MAMSCT (NOLOCK) ON MAMSCT.DISTRIBUTIONCHANNEL_RECORD_ID = SAQTRV.DISTRIBUTIONCHANNEL_RECORD_ID AND MAMSCT.COUNTRY_RECORD_ID = SAQTRV.COUNTRY_RECORD_ID AND MAMSCT.DIVISION_ID = SAQTRV.DIVISION_ID AND MAMSCT.SAP_PART_NUMBER = MAMTRL.SAP_PART_NUMBER
					WHERE {ObjectName}.QUOTE_RECORD_ID = '{QuoteRecordId}' AND {ObjectName}.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND {ObjectName}.SERVICE_ID = '{ServiceId}' AND ISNULL({ObjectName}.CONFIGURATION_STATUS,'') = 'COMPLETE'			
				""".format(UserId=self.user_id, UserName=self.user_name, ObjectName=source_object_name, QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id, EquipmentsCount=0))

		return True		
	
	def _simple_quote_items_insert(self):
		pass

	def _simple_items_object_insert(self):
		pass
	
	def _do_opertion(self):		
		if self.action_type == "INSERT_LINE_ITEMS":			
			if self.is_spare_service:				
				# Spare Parts Insert/Update
				pass
			else:	
				self._quote_items_insert()		
				self._quote_items_object_insert()		
		else:
			quote_revision_item_obj = Sql.GetFirst("SELECT CpqTableEntryId FROM SAQRIT (NOLOCK) WHERE SAQRIT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQRIT.SERVICE_ID = '{ServiceId}'".format(QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
			if not quote_revision_item_obj:
				##simple product quote item insert
				if self.is_simple_service == True:
					Trace.Write("simple a6200")
					self._simple_quote_items_insert()
					self._simple_items_object_insert()
				else:
					self._quote_items_insert()		
					self._quote_items_object_insert()	
		# Pricing Calculation - Start
		# quote_line_item_obj = Sql.GetFirst("SELECT EQUIPMENT_LINE_ID FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}' AND ISNULL(STATUS,'') = ''".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
		# if quote_line_item_obj:
		# 	ScriptExecutor.ExecuteGlobal('QTPOSTACRM',{'QUOTE_ID':self.contract_quote_id,'REVISION_ID':self.contract_quote_revision_id, 'Fun_type':'cpq_to_sscm'})
		# Pricing Calculation - End
		return True

try:
	where_condition_string = Param.WhereString
except:
	where_condition_string = ''
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
	
contract_quote_item_obj = ContractQuoteItem(**parameters)
contract_quote_item_obj._do_opertion()
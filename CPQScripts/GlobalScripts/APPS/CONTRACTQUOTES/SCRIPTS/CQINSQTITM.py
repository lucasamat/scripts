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
		self.entitlement_level_obj = kwargs.get('entitlement_level_obj')      
		self.pricing_temp_table = ''
		self.quote_line_item_temp_table = '' 
		self.quote_service_entitlement_type = ''
		self.source_object_name = ''
		self.set_contract_quote_related_details()
		self._set_service_type()
		self._set_fpm_service_type()
		self._get_material_type()
		self._get_ancillary_product()
	
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
		spare_parts_count_object = Sql.GetFirst("SELECT CpqTableEntryId FROM SAQRSP (NOLOCK) WHERE QUOTE_RECORD_ID ='{QuoteRecordId}' AND QTEREV_RECORD_ID='{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id))			
		if spare_parts_count_object:
			self.is_spare_service = True
		else:
			self.is_spare_service = False
		return True

	def _set_fpm_service_type(self):
		fpm_spare_parts_count_object = Sql.GetFirst("SELECT CpqTableEntryId FROM SAQSPT (NOLOCK) WHERE QUOTE_RECORD_ID ='{QuoteRecordId}' AND QTEREV_RECORD_ID='{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id))			
		if fpm_spare_parts_count_object:
			self.is_fpm_spare_service = True
		else:
			self.is_fpm_spare_service = False
		return True

	def _get_material_type(self):
		get_service_config_type = Sql.GetFirst("SELECT * FROM MAMTRL (NOLOCK) WHERE SAP_PART_NUMBER = '{}' AND MATERIALCONFIG_TYPE = 'SIMPLE MATERIAL'".format(self.service_id))
		if get_service_config_type:
			self.is_simple_service = True
		else:
			self.is_simple_service = False
		return True
	
	def _get_ancillary_product(self):
		self.is_ancillary = False
		check_ancillary = Sql.GetFirst("SELECT PAR_SERVICE_ID FROM SAQTSV (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' and SERVICE_ID = '{ServiceId}' ".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id))
		if check_ancillary:
			if check_ancillary.PAR_SERVICE_ID:
				self.is_ancillary = True
		else:
			self.is_ancillary = False
		return True
	
	def _quote_items_assembly_insert(self, update=True):
		# Update - Start
		#item_line_covered_object_assembly_join_string = ""	
		#item_line_covered_object_assembly_where_string = ""		
		#if update:
		item_line_covered_object_assembly_where_string = "AND ISNULL(SAQICA.ASSEMBLY_RECORD_ID,'') = '' "
		item_line_covered_object_assembly_join_string = "LEFT JOIN SAQICA (NOLOCK) ON SAQICA.QUOTE_RECORD_ID = SAQSCE.QUOTE_RECORD_ID AND SAQICA.QTEREV_RECORD_ID = SAQSCE.QTEREV_RECORD_ID AND SAQICA.SERVICE_RECORD_ID = SAQSCE.SERVICE_RECORD_ID AND SAQICA.GREENBOOK_RECORD_ID = SAQSCE.GREENBOOK_RECORD_ID AND SAQICA.FABLOCATION_RECORD_ID = SAQSCE.FABLOCATION_RECORD_ID AND SAQICA.EQUIPMENT_RECORD_ID = SAQSCE.EQUIPMENT_RECORD_ID AND SAQICA.ASSEMBLY_RECORD_ID = IQ.ASSEMBLY_RECORD_ID"
		# Update - End
		Sql.RunQuery("""INSERT SAQICA (EQUIPMENT_ID,EQUIPMENT_RECORD_ID,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,GREENBOOK,GREENBOOK_RECORD_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,ASSEMBLY_DESCRIPTION,ASSEMBLY_ID,ASSEMBLY_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,EQUIPMENTTYPE_ID,QUOTE_ITEM_COVERED_OBJECT_ASSEMBLY_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified) 
				SELECT OQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_COVERED_OBJECT_ASSEMBLY_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED,{UserId} as CpqTableEntryModifiedBy,GETDATE() as CpqTableEntryDateModified FROM (
					SELECT IQ.* FROM (
						SELECT 
							DISTINCT SAQSCA.EQUIPMENT_ID,SAQSCA.EQUIPMENT_RECORD_ID,SAQTSE.QUOTE_ID,SAQTSE.QUOTE_RECORD_ID,SAQTSE.QTEREV_ID,SAQTSE.QTEREV_RECORD_ID,SAQTSE.SERVICE_DESCRIPTION,SAQTSE.SERVICE_ID,SAQTSE.SERVICE_RECORD_ID,SAQSCA.GREENBOOK,SAQSCA.GREENBOOK_RECORD_ID,SAQSCA.FABLOCATION_ID,SAQSCA.FABLOCATION_NAME,SAQSCA.FABLOCATION_RECORD_ID,SAQSCA.ASSEMBLY_DESCRIPTION,SAQSCA.ASSEMBLY_ID,SAQSCA.ASSEMBLY_RECORD_ID,SAQTSE.SALESORG_ID,SAQTSE.SALESORG_NAME,SAQTSE.SALESORG_RECORD_ID,SAQSCA.EQUIPMENTTYPE_ID
						FROM SAQTSE (NOLOCK) 
						JOIN SAQSCA (NOLOCK) ON SAQSCA.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID AND SAQSCA.SERVICE_RECORD_ID = SAQTSE.SERVICE_RECORD_ID AND SAQSCA.QTEREV_RECORD_ID = SAQTSE.QTEREV_RECORD_ID  
						WHERE SAQTSE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQTSE.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQTSE.SERVICE_ID = '{ServiceId}'
					) IQ 
					JOIN SAQSCE (NOLOCK) ON SAQSCE.SERVICE_RECORD_ID = IQ.SERVICE_RECORD_ID AND SAQSCE.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND SAQSCE.EQUIPMENT_ID = IQ.EQUIPMENT_ID AND SAQSCE.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND ISNULL(SAQSCE.CONFIGURATION_STATUS,'') = 'COMPLETE' 
					{JoinString}
					WHERE SAQSCE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCE.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQSCE.SERVICE_ID = '{ServiceId}' {WhereString}
				)OQ""".format(UserId=self.user_id, UserName=self.user_name, QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id,JoinString=item_line_covered_object_assembly_join_string, WhereString=item_line_covered_object_assembly_where_string))
				
	def _quote_items_assembly_entitlement_insert(self, update=True):
		# Update - Start
		#item_line_covered_object_assembly_entitlement_join_string = ""	
		#item_line_covered_object_assembly_entitlement_where_string = ""		
		#if update:
		item_line_covered_object_assembly_entitlement_where_string = "AND ISNULL(SAQIAE.ASSEMBLY_RECORD_ID,'') = '' "
		item_line_covered_object_assembly_entitlement_join_string = "LEFT JOIN SAQIAE (NOLOCK) ON SAQIAE.QUOTE_RECORD_ID = SAQSCE.QUOTE_RECORD_ID AND SAQIAE.QTEREV_RECORD_ID = SAQSCE.QTEREV_RECORD_ID AND SAQIAE.SERVICE_RECORD_ID = SAQSCE.SERVICE_RECORD_ID AND SAQIAE.FABLOCATION_RECORD_ID = SAQSCE.FABLOCATION_RECORD_ID AND SAQIAE.EQUIPMENT_RECORD_ID = SAQSCE.EQUIPMENT_RECORD_ID AND SAQIAE.ASSEMBLY_RECORD_ID = IQ.ASSEMBLY_RECORD_ID"
		# Update - End
		Sql.RunQuery("""INSERT SAQIAE (EQUIPMENT_ID,EQUIPMENT_RECORD_ID,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,CPS_CONFIGURATION_ID,CPS_MATCH_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,ASSEMBLY_ID,ASSEMBLY_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,ENTITLEMENT_XML,QUOTE_ITEM_ASSEMBLY_ENTITLEMENT_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified) 
		SELECT OQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_ASSEMBLY_ENTITLEMENT_RECORD_ID,'{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED,{UserId} as CpqTableEntryModifiedBy,GETDATE() as CpqTableEntryDateModified FROM (
			SELECT IQ.*,SAQSCE.ENTITLEMENT_XML FROM (
				SELECT 
					DISTINCT SAQSCA.EQUIPMENT_ID,SAQSCA.EQUIPMENT_RECORD_ID,SAQTSE.QUOTE_ID,SAQTSE.QUOTE_RECORD_ID,SAQTSE.QTEREV_ID,SAQTSE.QTEREV_RECORD_ID,SAQTSE.SERVICE_DESCRIPTION,SAQTSE.SERVICE_ID,SAQTSE.SERVICE_RECORD_ID,SAQTSE.CPS_CONFIGURATION_ID,SAQTSE.CPS_MATCH_ID,SAQSCA.FABLOCATION_ID,SAQSCA.FABLOCATION_NAME,SAQSCA.FABLOCATION_RECORD_ID,SAQSCA.ASSEMBLY_ID,SAQSCA.ASSEMBLY_RECORD_ID,SAQTSE.SALESORG_ID,SAQTSE.SALESORG_NAME,SAQTSE.SALESORG_RECORD_ID 
				FROM SAQTSE (NOLOCK) 
				JOIN SAQSCA (NOLOCK) ON SAQSCA.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID AND SAQSCA.SERVICE_RECORD_ID = SAQTSE.SERVICE_RECORD_ID AND SAQSCA.QTEREV_RECORD_ID = SAQTSE.QTEREV_RECORD_ID WHERE SAQTSE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQTSE.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQTSE.SERVICE_ID = '{ServiceId}'
			) IQ 
			JOIN SAQSCE (NOLOCK) ON SAQSCE.SERVICE_RECORD_ID = IQ.SERVICE_RECORD_ID AND SAQSCE.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND SAQSCE.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND SAQSCE.EQUIPMENT_ID = IQ.EQUIPMENT_ID AND ISNULL(SAQSCE.CONFIGURATION_STATUS,'') = 'COMPLETE' 
			{JoinString}
			WHERE SAQSCE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCE.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQSCE.SERVICE_ID = '{ServiceId}' {WhereString}
		)OQ""".format(UserId=self.user_id, UserName=self.user_name, QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id,JoinString=item_line_covered_object_assembly_entitlement_join_string, WhereString=item_line_covered_object_assembly_entitlement_where_string))
	
	def _quote_annualized_items_insert(self, update=False):		
		join_condition_string = ""
		#annualized_item_where_string = ""
		#annualized_item_join_string = ""
		if self.quote_service_entitlement_type == 'OFFERING + EQUIPMENT':
			join_condition_string = ' AND SAQRIT.OBJECT_ID = SAQSCO.EQUIPMENT_ID'
		#if update:
		Log.Info('join_condition_string---'+str(join_condition_string))
		annualized_item_where_string = "AND ISNULL(SAQICO.EQUIPMENT_RECORD_ID,'') = '' "
		annualized_item_join_string = "LEFT JOIN SAQICO (NOLOCK) ON SAQICO.QUOTE_RECORD_ID = SAQSCE.QUOTE_RECORD_ID AND SAQICO.QTEREV_RECORD_ID = SAQSCE.QTEREV_RECORD_ID AND SAQICO.SERVICE_RECORD_ID = SAQSCE.SERVICE_RECORD_ID AND SAQICO.GREENBOOK_RECORD_ID = SAQSCE.GREENBOOK_RECORD_ID AND SAQICO.FABLOCATION_RECORD_ID = SAQSCE.FABLOCATION_RECORD_ID AND SAQICO.EQUIPMENT_RECORD_ID = SAQSCE.EQUIPMENT_RECORD_ID"
		Log.Info('join_condition_string---'+str(join_condition_string))		
		if self.is_ancillary == True:
			dynamic_value_cols = "'ACQUIRED' AS STATUS,'0' AS NET_PRICE_INGL_CURR, "
		else:
			dynamic_value_cols = "null AS STATUS, null as NET_PRICE_INGL_CURR, "
		
		Sql.RunQuery("""INSERT SAQICO (EQUIPMENT_DESCRIPTION, STATUS,NET_PRICE_INGL_CURR, QUANTITY,DISCOUNT,OBJECT_ID,EQUIPMENT_ID, EQUIPMENT_RECORD_ID, CONTRACT_VALID_FROM, CONTRACT_VALID_TO, LINE, PLATFORM, QUOTE_ID, QTEITM_RECORD_ID,  QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,KPU, SERIAL_NO, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, TECHNOLOGY,CUSTOMER_TOOL_ID, EQUIPMENTCATEGORY_ID, EQUIPMENTCATEGORY_RECORD_ID, EQUIPMENT_STATUS, MNT_PLANT_ID, MNT_PLANT_NAME, MNT_PLANT_RECORD_ID, SLSDIS_PRICE_MARGIN_RECORD_ID, SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID, TARGET_PRICE_MARGIN, TARGET_PRICE_MARGIN_RECORD_ID, WARRANTY_END_DATE, WARRANTY_START_DATE, GREENBOOK, GREENBOOK_RECORD_ID,  YEAR_OVER_YEAR,GLOBAL_CURRENCY,GLOBAL_CURRENCY_RECORD_ID, YEAR,  OBJECT_TYPE, QUOTE_ITEM_COVERED_OBJECT_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified)
				SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_COVERED_OBJECT_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED,{UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
				SELECT DISTINCT					
					SAQSCO.EQUIPMENT_DESCRIPTION,
					{dynamic_value_cols},
					SAQSCO.EQUIPMENT_QUANTITY,
					'0' AS DISCOUNT,
					SAQRIT.OBJECT_ID,
					SAQSCO.EQUIPMENT_ID,
					SAQSCO.EQUIPMENT_RECORD_ID,                        
					SAQRIT.CONTRACT_VALID_FROM,
					SAQRIT.CONTRACT_VALID_TO,
					SAQRIT.LINE,
					SAQSCO.PLATFORM,
					SAQRIT.QUOTE_ID, 
					SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID, 
					SAQRIT.QUOTE_RECORD_ID,
					SAQRIT.QTEREV_ID,
					SAQRIT.QTEREV_RECORD_ID,
					SAQSCO.KPU,
					SAQSCO.SERIAL_NO, 
					SAQRIT.SERVICE_DESCRIPTION, 
					SAQRIT.SERVICE_ID, 
					SAQRIT.SERVICE_RECORD_ID,								
					SAQSCO.TECHNOLOGY,																			
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
					SAQRIT.GREENBOOK, 
					SAQRIT.GREENBOOK_RECORD_ID, 					
					PRCFVA.FACTOR_PCTVAR as YEAR_OVER_YEAR,
					SAQTRV.GLOBAL_CURRENCY,
					SAQTRV.GLOBAL_CURRENCY_RECORD_ID,
					CONTRACT_TEMP.YEAR,
					SAQRIT.OBJECT_TYPE				
				FROM 
					SAQSCO (NOLOCK)					 
					JOIN SAQSCE (NOLOCK) ON SAQSCE.QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID AND SAQSCE.SERVICE_ID = SAQSCO.SERVICE_ID AND SAQSCE.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID
					AND SAQSCE.EQUIPMENT_RECORD_ID = SAQSCO.EQUIPMENT_RECORD_ID
					JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID         
					JOIN SAQTRV (NOLOCK) ON SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID 
					JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = SAQTRV.QUOTE_RECORD_ID
											AND SAQRIT.SERVICE_RECORD_ID = SAQSCO.SERVICE_RECORD_ID
											AND SAQRIT.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID
											AND SAQRIT.GREENBOOK_RECORD_ID = SAQSCO.GREENBOOK_RECORD_ID
											{JoinConditionString}					
					LEFT JOIN PRCFVA (NOLOCK) ON PRCFVA.FACTOR_VARIABLE_ID = SAQRIT.SERVICE_ID AND PRCFVA.FACTOR_ID = 'YOYDIS'	
					{JoinString}
					LEFT JOIN (
						SELECT DATEADD(year,1,CONTRACT_VALID_FROM) as date_year,'YEAR 1' AS year,equipment_id,QUOTE_RECORD_ID,SERVICE_ID,QTEREV_RECORD_ID,EQUIPMENT_RECORD_ID FROM SAQSCO WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}' 
						UNION ALL  
						SELECT DATEADD(year,2,CONTRACT_VALID_FROM) as date_year,'YEAR 2' AS year,equipment_id,QUOTE_RECORD_ID,SERVICE_ID,QTEREV_RECORD_ID,EQUIPMENT_RECORD_ID FROM SAQSCO WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}' AND  1 = (CASE WHEN DATEDIFF(MONTH, SAQSCO.CONTRACT_VALID_FROM, SAQSCO.CONTRACT_VALID_TO) > 12 then 1 else 0 end )
						UNION ALL  
						SELECT DATEADD(year,3,CONTRACT_VALID_FROM) as date_year,'YEAR 3' AS year,equipment_id,QUOTE_RECORD_ID,SERVICE_ID,QTEREV_RECORD_ID,EQUIPMENT_RECORD_ID FROM SAQSCO WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}' AND  1 = (CASE WHEN DATEDIFF(MONTH, SAQSCO.CONTRACT_VALID_FROM, SAQSCO.CONTRACT_VALID_TO) > 24 then 1 else 0 end )
						UNION ALL  
						SELECT DATEADD(year,4,CONTRACT_VALID_FROM) as date_year,'YEAR 4' AS year,equipment_id,QUOTE_RECORD_ID,SERVICE_ID,QTEREV_RECORD_ID,EQUIPMENT_RECORD_ID FROM SAQSCO WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}' AND  1 = (CASE WHEN DATEDIFF(MONTH, SAQSCO.CONTRACT_VALID_FROM, SAQSCO.CONTRACT_VALID_TO) > 36  then 1 else 0 end )
						UNION ALL  
						SELECT DATEADD(year,5,CONTRACT_VALID_FROM) as date_year,'YEAR 5' AS year,equipment_id,QUOTE_RECORD_ID,SERVICE_ID,QTEREV_RECORD_ID,EQUIPMENT_RECORD_ID FROM SAQSCO WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}' AND  1 = (CASE WHEN DATEDIFF(MONTH, SAQSCO.CONTRACT_VALID_FROM, SAQSCO.CONTRACT_VALID_TO) > 48  then 1 else 0 end ) 

					) CONTRACT_TEMP ON  CONTRACT_TEMP.QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID AND CONTRACT_TEMP.SERVICE_ID = SAQSCO.SERVICE_ID AND CONTRACT_TEMP.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID AND CONTRACT_TEMP.EQUIPMENT_RECORD_ID = SAQSCO.EQUIPMENT_RECORD_ID					
				WHERE 
					SAQSCO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQSCO.SERVICE_ID = '{ServiceId}' AND ISNULL(SAQSCE.CONFIGURATION_STATUS,'') = 'COMPLETE' {WhereConditionString}
				) IQ
				""".format(UserId=self.user_id, UserName=self.user_name, QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id, JoinString=annualized_item_join_string, JoinConditionString=join_condition_string, WhereConditionString=annualized_item_where_string, dynamic_value_cols = dynamic_value_cols)
			)

	def _quote_item_line_entitlement_insert(self, update=False):
		# Update - Start
		#item_line_covered_object_entitlement_join_string = ""	
		#item_line_covered_object_entitlement_where_string = ""		
		#if update:
		item_line_covered_object_entitlement_where_string = " AND ISNULL(SAQIEN.EQUIPMENT_RECORD_ID,'') = '' "
		item_line_covered_object_entitlement_join_string = "LEFT JOIN SAQIEN (NOLOCK) ON SAQIEN.QUOTE_RECORD_ID = SAQSCE.QUOTE_RECORD_ID AND SAQIEN.QTEREV_RECORD_ID = SAQSCE.QTEREV_RECORD_ID AND SAQIEN.SERVICE_RECORD_ID = SAQSCE.SERVICE_RECORD_ID AND SAQIEN.FABLOCATION_RECORD_ID = SAQSCE.FABLOCATION_RECORD_ID AND SAQIEN.EQUIPMENT_RECORD_ID = SAQSCE.EQUIPMENT_RECORD_ID"
		# Update - End
		item_line_covered_object_entitlement_query = """INSERT SAQIEN (QUOTE_ITEM_COVERED_OBJECT_ENTITLEMENTS_RECORD_ID,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,QTESRVENT_RECORD_ID,SERVICE_RECORD_ID,SERVICE_ID,SERVICE_DESCRIPTION,SERIAL_NO,ENTITLEMENT_XML,CPS_CONFIGURATION_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,EQUIPMENT_LINE_ID,LINE_ITEM_ID,CPS_MATCH_ID,QTEITMCOB_RECORD_ID,EQUIPMENT_ID,EQUIPMENT_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,QTEITM_RECORD_ID) 
		(
			SELECT 
				DISTINCT CONVERT(VARCHAR(4000), NEWID()) AS QUOTE_ITEM_COVERED_OBJECT_ENTITLEMENTS_RECORD_ID, SAQSCE.QUOTE_ID,SAQSCE.QUOTE_RECORD_ID,SAQSCE.QTEREV_ID,SAQSCE.QTEREV_RECORD_ID,SAQSCE.QTESRVENT_RECORD_ID,SAQSCE.SERVICE_RECORD_ID,SAQSCE.SERVICE_ID,SAQSCE.SERVICE_DESCRIPTION,SAQICO.SERIAL_NO,SAQSCE.ENTITLEMENT_XML,SAQSCE.CPS_CONFIGURATION_ID,SAQSCE.FABLOCATION_ID,SAQSCE.FABLOCATION_NAME,SAQSCE.FABLOCATION_RECORD_ID,SAQICO.EQUIPMENT_LINE_ID,SAQICO.LINE,SAQSCE.CPS_MATCH_ID,SAQICO.QUOTE_ITEM_COVERED_OBJECT_RECORD_ID as QTEITMCOB_RECORD_ID,SAQICO.EQUIPMENT_ID,SAQICO.EQUIPMENT_RECORD_ID,SAQSCE.SALESORG_ID,SAQSCE.SALESORG_NAME,SAQSCE.SALESORG_RECORD_ID,SAQICO.QTEITM_RECORD_ID 
			FROM SAQSCE (NOLOCK) 
			JOIN SAQICO ON SAQICO.QUOTE_RECORD_ID = SAQSCE.QUOTE_RECORD_ID AND SAQICO.SERVICE_ID = SAQSCE.SERVICE_ID AND SAQICO.						QTEREV_RECORD_ID = SAQSCE.QTEREV_RECORD_ID AND SAQICO.FABLOCATION_ID = SAQSCE.FABLOCATION_ID 
							AND SAQICO.GREENBOOK = SAQSCE.GREENBOOK AND SAQICO.EQUIPMENT_ID = SAQSCE.EQUIPMENT_ID 
			
			{JoinString}
			WHERE SAQSCE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCE.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQSCE.SERVICE_ID = '{ServiceId}' AND ISNULL(SAQSCE.CONFIGURATION_STATUS,'') = 'COMPLETE' {WhereString}
		)""".format(
		QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id,
		JoinString=item_line_covered_object_entitlement_join_string, WhereString=item_line_covered_object_entitlement_where_string)
		Sql.RunQuery(item_line_covered_object_entitlement_query)

	def _quote_items_object_insert(self, update=False):
		join_condition_string = ""
		#item_object_where_string = ""
		#item_object_join_string = ""
		if self.quote_service_entitlement_type == 'OFFERING + EQUIPMENT':
			join_condition_string = ' AND SAQRIT.OBJECT_ID = SAQSCO.EQUIPMENT_ID'
		#if update:
		item_object_where_string = "AND ISNULL(SAQRIO.EQUIPMENT_RECORD_ID,'') = '' "
		item_object_join_string = "LEFT JOIN SAQRIO (NOLOCK) ON SAQRIO.QUOTE_RECORD_ID = SAQSCE.QUOTE_RECORD_ID AND SAQRIO.QTEREV_RECORD_ID = SAQSCE.QTEREV_RECORD_ID AND SAQRIO.SERVICE_RECORD_ID = SAQSCE.SERVICE_RECORD_ID AND SAQRIO.GREENBOOK_RECORD_ID = SAQSCE.GREENBOOK_RECORD_ID AND SAQRIO.EQUIPMENT_RECORD_ID = SAQSCE.EQUIPMENT_RECORD_ID"
		Sql.RunQuery("""INSERT SAQRIO (CUSTOMER_TOOL_ID, EQUIPMENT_DESCRIPTION, EQUIPMENT_ID, EQUIPMENT_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID, KPU, LINE, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, QTEITM_RECORD_ID, QUOTE_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, SERIAL_NUMBER, TECHNOLOGY, TOOL_CONFIGURATION, WAFER_SIZE, QUOTE_REVISION_ITEM_OBJECT_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified)
				SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REVISION_ITEM_OBJECT_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED,{UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
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
											AND SAQRIT.GREENBOOK_RECORD_ID = SAQSCO.GREENBOOK_RECORD_ID
											{JoinConditionString}
					LEFT JOIN PRPRBM (NOLOCK) ON PRPRBM.ACCOUNT_RECORD_ID = SAQTMT.ACCOUNT_RECORD_ID AND PRPRBM.EQUIPMENT_RECORD_ID = SAQSCO.EQUIPMENT_RECORD_ID AND PRPRBM.SERVICE_RECORD_ID = SAQSCO.SERVICE_RECORD_ID		
					{JoinString}					
				WHERE 
					SAQSCO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQSCO.SERVICE_ID = '{ServiceId}' AND ISNULL(SAQSCE.CONFIGURATION_STATUS,'') = 'COMPLETE' {WhereConditionString}
				) IQ
				""".format(UserId=self.user_id, UserName=self.user_name, QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id,
				JoinString=item_object_join_string, JoinConditionString=join_condition_string, WhereConditionString=item_object_where_string)
			)
	
	def _quote_items_entitlement_insert(self, update=False):		
		join_condition_string = ''
		dynamic_group_id_value = 'null as ENTITLEMENT_GROUP_ID'
		dynamic_is_changed_value = 'null as IS_CHANGED'
		if self.quote_service_entitlement_type == 'OFFERING + EQUIPMENT':
			join_condition_string = ' AND SAQRIT.OBJECT_ID = {ObjectName}.EQUIPMENT_ID'.format(ObjectName=self.source_object_name)
			dynamic_group_id_value = '{ObjectName}.ENTITLEMENT_GROUP_ID'.format(ObjectName=self.source_object_name)
			dynamic_is_changed_value = '{ObjectName}.IS_CHANGED'.format(ObjectName=self.source_object_name)
		#if update: # need to verify one more time
		Sql.RunQuery("DELETE SAQITE FROM SAQITE WHERE SAQITE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQITE.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQITE.SERVICE_ID = '{ServiceId}'".format(QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
		Sql.RunQuery("""INSERT SAQITE (QUOTE_REV_ITEM_ENTITLEMENT_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified, CPS_CONFIGURATION_ID, CPS_MATCH_ID, ENTITLEMENT_COST_IMPACT, ENTITLEMENT_GROUP_ID, ENTITLEMENT_GROUP_XML, ENTITLEMENT_PRICE_IMPACT, ENTITLEMENT_XML, IS_CHANGED, LINE, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, QTEITM_RECORD_ID, QUOTE_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID)
					SELECT
						CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REV_ITEM_ENTITLEMENT_RECORD_ID,
						'{UserName}' AS CPQTABLEENTRYADDEDBY,
						GETDATE() as CPQTABLEENTRYDATEADDED,
						{UserId} as CpqTableEntryModifiedBy,
						GETDATE() as CpqTableEntryDateModified,
						{ObjectName}.CPS_CONFIGURATION_ID,
						{ObjectName}.CPS_MATCH_ID,
						null as ENTITLEMENT_COST_IMPACT,
						{dynamic_group_id_value},
						null as ENTITLEMENT_GROUP_XML,
						null as ENTITLEMENT_PRICE_IMPACT,
						{ObjectName}.ENTITLEMENT_XML,
						{dynamic_is_changed_value},
						SAQRIT.LINE,						
						SAQRIT.SERVICE_DESCRIPTION,
						SAQRIT.SERVICE_ID,
						SAQRIT.SERVICE_RECORD_ID,
						SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID,						
						SAQRIT.QUOTE_ID,
						SAQRIT.QUOTE_RECORD_ID,
						SAQRIT.QTEREV_ID,
						SAQRIT.QTEREV_RECORD_ID,						
						SAQRIT.GREENBOOK,
						SAQRIT.GREENBOOK_RECORD_ID
					FROM {ObjectName} (NOLOCK) 
					JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = {ObjectName}.QUOTE_RECORD_ID
												AND SAQRIT.SERVICE_RECORD_ID = {ObjectName}.SERVICE_RECORD_ID
												AND SAQRIT.QTEREV_RECORD_ID = {ObjectName}.QTEREV_RECORD_ID
												AND SAQRIT.FABLOCATION_RECORD_ID = {ObjectName}.FABLOCATION_RECORD_ID
												AND SAQRIT.GREENBOOK_RECORD_ID = {ObjectName}.GREENBOOK_RECORD_ID		
												{JoinConditionString}			
					WHERE {ObjectName}.QUOTE_RECORD_ID = '{QuoteRecordId}' AND {ObjectName}.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND {ObjectName}.SERVICE_ID = '{ServiceId}' AND ISNULL({ObjectName}.CONFIGURATION_STATUS,'') = 'COMPLETE'			
				""".format(UserId=self.user_id, UserName=self.user_name, ObjectName=self.source_object_name, QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id, JoinConditionString=join_condition_string, dynamic_is_changed_value = dynamic_is_changed_value, dynamic_group_id_value = dynamic_group_id_value))
		return True

	def _set_quote_service_entitlement_type(self):
		##chk ancillary offering
		parent_service_id = ""
		check_ancillary = Sql.GetFirst("SELECT PAR_SERVICE_ID FROM SAQTSV (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' and SERVICE_ID = '{ServiceId}' ".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id))
		if check_ancillary:
			if check_ancillary.PAR_SERVICE_ID:
				parent_service_id = check_ancillary.PAR_SERVICE_ID

		Log.Info("_quote_items_insert ===> 1")
		# service_entitlement_obj = Sql.GetFirst("""SELECT ENTITLEMENT_ID,ENTITLEMENT_DISPLAY_VALUE FROM 
		# 								(
		# 									SELECT DISTINCT 
		# 											IQ.QUOTE_RECORD_ID,
		# 											IQ.QTEREV_RECORD_ID, 
		# 											replace(X.Y.value('(ENTITLEMENT_ID)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_ID,
		# 											replace(replace(replace(replace(X.Y.value('(ENTITLEMENT_DISPLAY_VALUE)[1]', 'VARCHAR(128)'),';#38','&'),';#39',''''),'_&lt;','_<' ),'_&gt;','_>') as ENTITLEMENT_DISPLAY_VALUE 
		# 									FROM (
		# 										SELECT QUOTE_RECORD_ID,QTEREV_RECORD_ID,CONVERT(xml,replace(replace(replace(replace(replace(replace(ENTITLEMENT_XML,'&',';#38'),'''',';#39'),' < ',' &lt; ' ),' > ',' &gt; ' ),'_>','_&gt;'),'_<','_&lt;'))  as ENTITLEMENT_XML  
		# 										FROM SAQTSE (NOLOCK) 
		# 										WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' and SERVICE_ID = '{ServiceId}' 
		# 										) IQ 
		# 									OUTER APPLY IQ.ENTITLEMENT_XML.nodes('QUOTE_ITEM_ENTITLEMENT') as X(Y) 
		# 								) as OQ 
		# 								WHERE ENTITLEMENT_ID LIKE '{EntitlementAttrId}'""".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id if not parent_service_id else parent_service_id,EntitlementAttrId='AGS_'+str(self.service_id)+'_PQB_QTITST'))
		#if service_entitlement_obj:
		if self.action_type == 'UPDATE_LINE_ITEMS' and self.entitlement_level_obj != 'SAQTSE' and parent_service_id:
			where_str = where_condition_string.replace('SRC.','').replace(self.service_id,parent_service_id).replace('WHERE','')
		else:
			where_str = " QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' and SERVICE_ID = '{ServiceId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id)
		service_entitlement_obj = Sql.GetFirst("""SELECT SERVICE_ID, ENTITLEMENT_XML FROM  {obj_name} (NOLOCK) WHERE {where_str}""".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id, obj_name = self.entitlement_level_obj, where_str = where_str))
		if service_entitlement_obj:
			quote_item_tag_pattern = re.compile(r'(<QUOTE_ITEM_ENTITLEMENT>[\w\W]*?</QUOTE_ITEM_ENTITLEMENT>)')
			entitlement_id_tag_pattern = re.compile(r'<ENTITLEMENT_ID>AGS_'+str(self.service_id)+'_PQB_QTITST</ENTITLEMENT_ID>')
			entitlement_display_value_tag_pattern = re.compile(r'<ENTITLEMENT_DISPLAY_VALUE>([^>]*?)</ENTITLEMENT_DISPLAY_VALUE>')
			for quote_item_tag in re.finditer(quote_item_tag_pattern, service_entitlement_obj.ENTITLEMENT_XML):
				quote_item_tag_content = quote_item_tag.group(1)
				entitlement_id_tag_match = re.findall(entitlement_id_tag_pattern,quote_item_tag_content)				
				if entitlement_id_tag_match:
					entitlement_display_value_tag_match = re.findall(entitlement_display_value_tag_pattern,quote_item_tag_content)
					if entitlement_display_value_tag_match:
						self.quote_service_entitlement_type = entitlement_display_value_tag_match[0].upper()
						if self.quote_service_entitlement_type == 'OFFERING + EQUIPMENT':
							self.source_object_name = 'SAQSCE'
						elif self.quote_service_entitlement_type in ('OFFERING + FAB + GREENBOOK + GROUP OF EQUIPMENT', 'OFFERING + GREENBOOK + GR EQUI', 'OFFERING + CHILD GROUP OF PART'):
							self.source_object_name = 'SAQSGE'

						break
				else:
					continue
			# if self.service_id == 'Z0101':
			# 	self.quote_service_entitlement_type = 'OFFERING + GREENBOOK + GR EQUI'
			Log.Info(str(self.contract_quote_id)+"_set_quote_service_entitlement_type ===> 2"+str(self.quote_service_entitlement_type))

	def _quote_items_summary_insert(self, update=False):
		if self.source_object_name:	
			item_summary_where_string = " AND ISNULL(SAQRIS.SERVICE_RECORD_ID,'') = '' "
			item_summary_join_string = "LEFT JOIN SAQRIS (NOLOCK) ON SAQRIS.QUOTE_RECORD_ID = {ObjectName}.QUOTE_RECORD_ID AND SAQRIS.QTEREV_RECORD_ID = {ObjectName}.QTEREV_RECORD_ID AND SAQRIS.SERVICE_RECORD_ID = {ObjectName}.SERVICE_RECORD_ID".format(ObjectName=self.source_object_name)	
			summary_last_line_no = 0
			quote_item_summary_obj = Sql.GetFirst("SELECT TOP 1 LINE FROM SAQRIS (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' ORDER BY LINE DESC".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id))
			if quote_item_summary_obj:
				summary_last_line_no = int(quote_item_summary_obj.LINE) 	
			Log.Info("===> SAQRIS INSERT ==> "+str("""INSERT SAQRIS (CONTRACT_VALID_FROM, CONTRACT_VALID_TO, DIVISION_ID, DIVISION_RECORD_ID, DOC_CURRENCY, DOCCURR_RECORD_ID, GLOBAL_CURRENCY, GLOBAL_CURRENCY_RECORD_ID, PLANT_ID, PLANT_RECORD_ID,  SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, QUANTITY, QUOTE_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, LINE, QUOTE_REV_ITEM_SUMMARY_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified)
				SELECT IQ.*, ROW_NUMBER()OVER(ORDER BY(IQ.SERVICE_ID)) + {ItemSummaryLastLineNo} as LINE, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REV_ITEM_SUMMARY_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED,{UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
					SELECT DISTINCT
						SAQTRV.CONTRACT_VALID_FROM,
						SAQTRV.CONTRACT_VALID_TO,
						SAQTRV.DIVISION_ID,
						SAQTRV.DIVISION_RECORD_ID,
						SAQTRV.DOC_CURRENCY,
						SAQTRV.DOCCURR_RECORD_ID,
						SAQTRV.GLOBAL_CURRENCY,
						SAQTRV.GLOBAL_CURRENCY_RECORD_ID,						
						MAMSOP.PLANT_ID,
						MAMSOP.PLANT_RECORD_ID,
						{ObjectName}.SERVICE_DESCRIPTION,
						{ObjectName}.SERVICE_ID,
						{ObjectName}.SERVICE_RECORD_ID,						
						1 as QUANTITY,
						SAQTRV.QUOTE_ID,
						SAQTRV.QUOTE_RECORD_ID,
						SAQTMT.QTEREV_ID,
						SAQTMT.QTEREV_RECORD_ID
					FROM {ObjectName} (NOLOCK) 
					JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = {ObjectName}.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = {ObjectName}.QTEREV_RECORD_ID     
					JOIN SAQTRV (NOLOCK) ON SAQTRV.SALESORG_RECORD_ID = {ObjectName}.SALESORG_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = {ObjectName}.QTEREV_RECORD_ID AND SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID
					LEFT JOIN MAMSOP (NOLOCK) ON MAMSOP.SAP_PART_NUMBER = {ObjectName}.SERVICE_ID AND MAMSOP.SALESORG_ID = SAQTRV.SALESORG_ID AND MAMSOP.DISTRIBUTIONCHANNEL_ID = SAQTRV.DISTRIBUTIONCHANNEL_ID			
					{JoinString}
					WHERE {ObjectName}.QUOTE_RECORD_ID = '{QuoteRecordId}' AND {ObjectName}.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND {ObjectName}.SERVICE_ID = '{ServiceId}' AND ISNULL({ObjectName}.CONFIGURATION_STATUS,'') = 'COMPLETE' {WhereConditionString}) IQ			
			""".format(UserId=self.user_id, UserName=self.user_name, ObjectName=self.source_object_name, QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id, ItemSummaryLastLineNo=summary_last_line_no, WhereConditionString=item_summary_where_string, JoinString=item_summary_join_string)))		
			Sql.RunQuery("""INSERT SAQRIS (CONTRACT_VALID_FROM, CONTRACT_VALID_TO, DIVISION_ID, DIVISION_RECORD_ID, DOC_CURRENCY, DOCCURR_RECORD_ID, GLOBAL_CURRENCY, GLOBAL_CURRENCY_RECORD_ID, PLANT_ID, PLANT_RECORD_ID, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, QUANTITY, QUOTE_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, LINE, QUOTE_REV_ITEM_SUMMARY_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified)
				SELECT IQ.*, ROW_NUMBER()OVER(ORDER BY(IQ.SERVICE_ID)) + {ItemSummaryLastLineNo} as LINE, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REV_ITEM_SUMMARY_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED,{UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
					SELECT DISTINCT
						SAQTRV.CONTRACT_VALID_FROM,
						SAQTRV.CONTRACT_VALID_TO,
						SAQTRV.DIVISION_ID,
						SAQTRV.DIVISION_RECORD_ID,
						SAQTRV.DOC_CURRENCY,
						SAQTRV.DOCCURR_RECORD_ID,
						SAQTRV.GLOBAL_CURRENCY,
						SAQTRV.GLOBAL_CURRENCY_RECORD_ID,						
						MAMSOP.PLANT_ID,
						MAMSOP.PLANT_RECORD_ID,
						{ObjectName}.SERVICE_DESCRIPTION,
						{ObjectName}.SERVICE_ID,
						{ObjectName}.SERVICE_RECORD_ID,						
						1 as QUANTITY,
						SAQTRV.QUOTE_ID,
						SAQTRV.QUOTE_RECORD_ID,
						SAQTMT.QTEREV_ID,
						SAQTMT.QTEREV_RECORD_ID
					FROM {ObjectName} (NOLOCK) 
					JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = {ObjectName}.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = {ObjectName}.QTEREV_RECORD_ID     
					JOIN SAQTRV (NOLOCK) ON SAQTRV.SALESORG_RECORD_ID = {ObjectName}.SALESORG_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = {ObjectName}.QTEREV_RECORD_ID AND SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID
					LEFT JOIN MAMSOP (NOLOCK) ON MAMSOP.SAP_PART_NUMBER = {ObjectName}.SERVICE_ID AND MAMSOP.SALESORG_ID = SAQTRV.SALESORG_ID AND MAMSOP.DISTRIBUTIONCHANNEL_ID = SAQTRV.DISTRIBUTIONCHANNEL_ID			
					{JoinString}
					WHERE {ObjectName}.QUOTE_RECORD_ID = '{QuoteRecordId}' AND {ObjectName}.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND {ObjectName}.SERVICE_ID = '{ServiceId}' AND ISNULL({ObjectName}.CONFIGURATION_STATUS,'') = 'COMPLETE' {WhereConditionString}) IQ			
			""".format(UserId=self.user_id, UserName=self.user_name, ObjectName=self.source_object_name, QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id, ItemSummaryLastLineNo=summary_last_line_no, WhereConditionString=item_summary_where_string, JoinString=item_summary_join_string))
		return True		

	def _quote_items_insert(self, update=False):
		dynamic_select_columns = ""
		item_where_string = ""
		item_join_string = ""
		if self.quote_service_entitlement_type == 'OFFERING + EQUIPMENT':			
			dynamic_select_columns = "SAQSCE.EQUIPMENT_ID as OBJECT_ID, 'EQUIPMENT' as OBJECT_TYPE, "			
			#if update:
			item_where_string += " AND ISNULL(SAQRIT.OBJECT_ID,'') = '' "
			item_join_string += "LEFT JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = SAQSCE.QUOTE_RECORD_ID AND SAQRIT.QTEREV_RECORD_ID = SAQSCE.QTEREV_RECORD_ID AND SAQRIT.SERVICE_RECORD_ID = SAQSCE.SERVICE_RECORD_ID AND SAQRIT.GREENBOOK_RECORD_ID = SAQSCE.GREENBOOK_RECORD_ID AND ISNULL(SAQRIT.OBJECT_ID,'') = SAQSCE.EQUIPMENT_ID"
		elif self.quote_service_entitlement_type in ('OFFERING + FAB + GREENBOOK + GROUP OF EQUIPMENT', 'OFFERING + GREENBOOK + GR EQUI', 'OFFERING + CHILD GROUP OF PART'):
			
			dynamic_select_columns = 'null as OBJECT_ID, null as OBJECT_TYPE, '		
			#if update:
			item_where_string += " AND ISNULL(SAQRIT.GREENBOOK_RECORD_ID,'') = ''"
			item_join_string += "LEFT JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = SAQSGE.QUOTE_RECORD_ID AND SAQRIT.QTEREV_RECORD_ID = SAQSGE.QTEREV_RECORD_ID AND SAQRIT.SERVICE_RECORD_ID = SAQSGE.SERVICE_RECORD_ID  AND SAQRIT.GREENBOOK_RECORD_ID = SAQSGE.GREENBOOK_RECORD_ID"	
		else:
			return False

		if self.source_object_name:		
			equipments_count = 0
			quote_item_obj = Sql.GetFirst("SELECT TOP 1 LINE FROM SAQRIT (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' ORDER BY LINE DESC".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id))
			if quote_item_obj:
				equipments_count = int(quote_item_obj.LINE) 			
			Sql.RunQuery("""INSERT SAQRIT (QUOTE_REVISION_CONTRACT_ITEM_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified, CONTRACT_VALID_FROM, CONTRACT_VALID_TO, DOC_CURRENCY, DOCURR_RECORD_ID, EXCHANGE_RATE, EXCHANGE_RATE_DATE, EXCHANGE_RATE_RECORD_ID, GL_ACCOUNT_NO, GLOBAL_CURRENCY, GLOBAL_CURRENCY_RECORD_ID, LINE, OBJECT_ID, OBJECT_TYPE, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, PROFIT_CENTER, QUANTITY, QUOTE_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, REF_SALESORDER, STATUS, TAXCLASSIFICATION_DESCRIPTION, TAXCLASSIFICATION_ID, TAXCLASSIFICATION_RECORD_ID, FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID)
				SELECT
					CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REVISION_CONTRACT_ITEM_ID,
					'{UserName}' AS CPQTABLEENTRYADDEDBY,
					GETDATE() as CPQTABLEENTRYDATEADDED,
					{UserId} as CpqTableEntryModifiedBy,
					GETDATE() as CpqTableEntryDateModified,
					SAQTRV.CONTRACT_VALID_FROM,
					SAQTRV.CONTRACT_VALID_TO,
					SAQTRV.DOC_CURRENCY,
					SAQTRV.DOCCURR_RECORD_ID as DOCURR_RECORD_ID,
					ISNULL(CONVERT(FLOAT,SAQTRV.EXCHANGE_RATE),'') AS EXCHANGE_RATE,
					SAQTRV.EXCHANGE_RATE_DATE,
					SAQTRV.EXCHANGERATE_RECORD_ID as EXCHANGE_RATE_RECORD_ID,
					null as GL_ACCOUNT_NO,
					SAQTRV.GLOBAL_CURRENCY,
					SAQTRV.GLOBAL_CURRENCY_RECORD_ID,
					ROW_NUMBER()OVER(ORDER BY({ObjectName}.CpqTableEntryId)) + {EquipmentsCount} as LINE,
					{DynamicColumns}					
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
					'ACQUIRING' as STATUS,
					MAMSCT.TAXCLASSIFICATION_DESCRIPTION,
					MAMSCT.TAXCLASSIFICATION_ID,
					MAMSCT.TAXCLASSIFICATION_RECORD_ID,
					{ObjectName}.GREENBOOK,
					{ObjectName}.GREENBOOK_RECORD_ID
					
				FROM {ObjectName} (NOLOCK) 
				JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = {ObjectName}.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = {ObjectName}.QTEREV_RECORD_ID     
				JOIN SAQTRV (NOLOCK) ON SAQTRV.SALESORG_RECORD_ID = {ObjectName}.SALESORG_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = {ObjectName}.QTEREV_RECORD_ID AND SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID
				JOIN MAMTRL (NOLOCK) ON MAMTRL.SAP_PART_NUMBER = {ObjectName}.SERVICE_ID 
				LEFT JOIN MAMSCT (NOLOCK) ON MAMSCT.DISTRIBUTIONCHANNEL_RECORD_ID = SAQTRV.DISTRIBUTIONCHANNEL_RECORD_ID AND MAMSCT.COUNTRY_RECORD_ID = SAQTRV.COUNTRY_RECORD_ID AND MAMSCT.DIVISION_ID = SAQTRV.DIVISION_ID AND MAMSCT.SAP_PART_NUMBER = MAMTRL.SAP_PART_NUMBER
				{JoinString}
				WHERE {ObjectName}.QUOTE_RECORD_ID = '{QuoteRecordId}' AND {ObjectName}.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND {ObjectName}.SERVICE_ID = '{ServiceId}' AND ISNULL({ObjectName}.CONFIGURATION_STATUS,'') = 'COMPLETE' {WhereConditionString}			
			""".format(UserId=self.user_id, UserName=self.user_name, ObjectName=self.source_object_name, QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id, EquipmentsCount=equipments_count, DynamicColumns=dynamic_select_columns, WhereConditionString=item_where_string, JoinString=item_join_string))
			# Item Level entitlement Insert
			if self.service_id == 'Z0101':
				self._spare_quote_items_entitlement_insert(update=update)
			else:
				self._quote_items_entitlement_insert(update=update)
		return True		
	
	def _simple_quote_items_insert(self):
		equipments_count = 0
		quote_line_item_obj = Sql.GetFirst("SELECT TOP 1 LINE FROM SAQRIT (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' ORDER BY LINE DESC".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id))
		if quote_line_item_obj:
			if quote_line_item_obj.LINE:
				equipments_count = int(quote_line_item_obj.LINE) 
		Sql.RunQuery("""INSERT SAQRIT (QUOTE_REVISION_CONTRACT_ITEM_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified, CONTRACT_VALID_FROM, CONTRACT_VALID_TO, DOC_CURRENCY, DOCURR_RECORD_ID, EXCHANGE_RATE, EXCHANGE_RATE_DATE, EXCHANGE_RATE_RECORD_ID, GL_ACCOUNT_NO, GLOBAL_CURRENCY, GLOBAL_CURRENCY_RECORD_ID, LINE, OBJECT_ID, OBJECT_TYPE, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, PROFIT_CENTER, QUANTITY, QUOTE_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, REF_SALESORDER, STATUS, TAXCLASSIFICATION_DESCRIPTION, TAXCLASSIFICATION_ID, TAXCLASSIFICATION_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID,NET_VALUE_INGL_CURR, NET_PRICE_INGL_CURR) 
			SELECT
				CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REVISION_CONTRACT_ITEM_ID,
				'{UserName}' AS CPQTABLEENTRYADDEDBY,
				GETDATE() as CPQTABLEENTRYDATEADDED,
				{UserId} as CpqTableEntryModifiedBy,
				GETDATE() as CpqTableEntryDateModified,
				SAQTRV.CONTRACT_VALID_FROM,
				SAQTRV.CONTRACT_VALID_TO,
				SAQTRV.DOC_CURRENCY,
				SAQTRV.DOCCURR_RECORD_ID as DOCURR_RECORD_ID,
				ISNULL(CONVERT(FLOAT,SAQTRV.EXCHANGE_RATE),'') AS EXCHANGE_RATE,
				SAQTRV.EXCHANGE_RATE_DATE,
				SAQTRV.EXCHANGERATE_RECORD_ID as EXCHANGE_RATE_RECORD_ID,
				null as GL_ACCOUNT_NO,
				SAQTRV.GLOBAL_CURRENCY,
				SAQTRV.GLOBAL_CURRENCY_RECORD_ID,
				ROW_NUMBER()OVER(ORDER BY(SAQSGB.CpqTableEntryId)) + {EquipmentsCount} as LINE,
				null as OBJECT_ID,
				'GREENBOOK' as OBJECT_TYPE,
				SAQSGB.SERVICE_DESCRIPTION,
				SAQSGB.SERVICE_ID,
				SAQSGB.SERVICE_RECORD_ID,
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
				SAQSGB.GREENBOOK,
				SAQSGB.GREENBOOK_RECORD_ID,
				'0' AS NET_VALUE_INGL_CURR,
				'0' AS NET_PRICE_INGL_CURR
			FROM SAQSGB (NOLOCK) 
			JOIN (
				SELECT DISTINCT SAQSGE.QUOTE_RECORD_ID,SAQSGE.QTEREV_RECORD_ID, SAQTSV.SERVICE_ID,SAQSGE.GREENBOOK,SAQSGE.SALESORG_RECORD_ID FROM SAQSGE (NOLOCK) INNER JOIN SAQTSV ON SAQSGE.QUOTE_RECORD_ID = SAQTSV.QUOTE_RECORD_ID  AND SAQSGE.QTEREV_RECORD_ID = SAQTSV.QTEREV_RECORD_ID AND SAQSGE.SERVICE_ID = SAQTSV.PAR_SERVICE_ID 
				WHERE SAQSGE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSGE.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND ISNULL(CONFIGURATION_STATUS, '') = 'COMPLETE' AND SAQTSV.SERVICE_ID ='{ServiceId}'
				
			) AS IQ ON IQ.QUOTE_RECORD_ID = SAQSGB.QUOTE_RECORD_ID AND IQ.QTEREV_RECORD_ID = SAQSGB.QTEREV_RECORD_ID AND IQ.SERVICE_ID = SAQSGB.SERVICE_ID	AND IQ.SERVICE_ID = '{ServiceId}' AND IQ.GREENBOOK = SAQSGB.GREENBOOK AND IQ.SERVICE_ID = '{ServiceId}'
			JOIN (SELECT GREENBOOK_RECORD_ID,QTEREV_RECORD_ID,QUOTE_RECORD_ID FROM SAQSGB (NOLOCK) WHERE SAQSGB.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSGB.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQSGB.SERVICE_ID = '{ServiceId}' GROUP BY GREENBOOK_RECORD_ID,QTEREV_RECORD_ID,QUOTE_RECORD_ID) EQUP ON EQUP.GREENBOOK_RECORD_ID = SAQSGB.GREENBOOK_RECORD_ID AND EQUP.QTEREV_RECORD_ID = SAQSGB.QTEREV_RECORD_ID AND EQUP.QUOTE_RECORD_ID = SAQSGB.QUOTE_RECORD_ID
			JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQSGB.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = SAQSGB.QTEREV_RECORD_ID     
			JOIN SAQTRV (NOLOCK) ON SAQTRV.SALESORG_RECORD_ID = IQ.SALESORG_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = SAQSGB.QTEREV_RECORD_ID AND SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID
			JOIN MAMTRL (NOLOCK) ON MAMTRL.SAP_PART_NUMBER = SAQSGB.SERVICE_ID 
			LEFT JOIN MAMSCT (NOLOCK) ON MAMSCT.DISTRIBUTIONCHANNEL_RECORD_ID = SAQTRV.DISTRIBUTIONCHANNEL_RECORD_ID AND MAMSCT.COUNTRY_RECORD_ID = SAQTRV.COUNTRY_RECORD_ID AND MAMSCT.DIVISION_ID = SAQTRV.DIVISION_ID AND MAMSCT.SAP_PART_NUMBER = MAMTRL.SAP_PART_NUMBER
			LEFT JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = SAQSGB.QUOTE_RECORD_ID AND SAQRIT.QTEREV_RECORD_ID = SAQSGB.QTEREV_RECORD_ID AND SAQRIT.SERVICE_RECORD_ID = SAQSGB.SERVICE_RECORD_ID AND SAQRIT.GREENBOOK_RECORD_ID = SAQSGB.GREENBOOK_RECORD_ID 
			WHERE SAQSGB.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSGB.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQSGB.SERVICE_ID = '{ServiceId}'  AND  ISNULL(SAQRIT.GREENBOOK_RECORD_ID,'') = ''""".format(UserId=self.user_id, UserName=self.user_name, QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id, EquipmentsCount=equipments_count))

	def _simple_items_object_insert(self):
		Sql.RunQuery("""INSERT SAQRIO (CUSTOMER_TOOL_ID, EQUIPMENT_DESCRIPTION, EQUIPMENT_ID, EQUIPMENT_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID, KPU, LINE, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, QTEITM_RECORD_ID, QUOTE_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, SERIAL_NUMBER, TECHNOLOGY, TOOL_CONFIGURATION, WAFER_SIZE, QUOTE_REVISION_ITEM_OBJECT_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified)
				SELECT OQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REVISION_ITEM_OBJECT_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED,{UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
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
					JOIN (
						SELECT SAQSCE.QUOTE_RECORD_ID,SAQSCE.QTEREV_RECORD_ID, SAQTSV.SERVICE_ID,SAQSCE.EQUIPMENT_ID FROM SAQSCE (NOLOCK) INNER JOIN SAQTSV ON SAQSCE.QUOTE_RECORD_ID = SAQTSV.QUOTE_RECORD_ID  AND SAQSCE.QTEREV_RECORD_ID = SAQTSV.QTEREV_RECORD_ID AND SAQSCE.SERVICE_ID = SAQTSV.PAR_SERVICE_ID 
						WHERE SAQSCE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCE.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND ISNULL(CONFIGURATION_STATUS, '') = 'COMPLETE' AND SAQTSV.SERVICE_ID ='{ServiceId}'
						
					) AS IQ ON IQ.QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID AND IQ.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID AND IQ.SERVICE_ID = SAQSCO.SERVICE_ID	AND IQ.SERVICE_ID = '{ServiceId}'	AND IQ.EQUIPMENT_ID	 = SAQSCO.EQUIPMENT_ID	AND IQ.SERVICE_ID = '{ServiceId}'
					JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID         
					JOIN SAQTRV (NOLOCK) ON SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID 
					JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = SAQTRV.QUOTE_RECORD_ID
											AND SAQRIT.SERVICE_RECORD_ID = SAQSCO.SERVICE_RECORD_ID
											AND SAQRIT.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID
											AND SAQRIT.GREENBOOK_RECORD_ID = SAQSCO.GREENBOOK_RECORD_ID
					LEFT JOIN PRPRBM (NOLOCK) ON PRPRBM.ACCOUNT_RECORD_ID = SAQTMT.ACCOUNT_RECORD_ID AND PRPRBM.EQUIPMENT_RECORD_ID = SAQSCO.EQUIPMENT_RECORD_ID AND PRPRBM.SERVICE_RECORD_ID = SAQSCO.SERVICE_RECORD_ID		
					LEFT JOIN SAQRIO (NOLOCK) ON SAQRIO.QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID AND SAQRIO.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID AND SAQRIO.SERVICE_RECORD_ID = SAQSCO.SERVICE_RECORD_ID AND SAQRIO.GREENBOOK_RECORD_ID = SAQSCO.GREENBOOK_RECORD_ID AND SAQRIO.EQUIPMENT_RECORD_ID = SAQSCO.EQUIPMENT_RECORD_ID			
				WHERE 
					SAQSCO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQSCO.SERVICE_ID = '{ServiceId}'  AND ISNULL(SAQRIO.EQUIPMENT_RECORD_ID,'') = '' 
				) OQ
				""".format(UserId=self.user_id, UserName=self.user_name, QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id,
				)
			)

		##update quantity in SAQRIT
		self._quote_item_qty_update()

	def _simple_quote_annualized_items_insert(self):
		Sql.RunQuery("""INSERT SAQICO (EQUIPMENT_DESCRIPTION,STATUS,QUANTITY,DISCOUNT,OBJECT_ID,EQUIPMENT_ID, EQUIPMENT_RECORD_ID, CONTRACT_VALID_FROM, CONTRACT_VALID_TO,LINE, PLATFORM, QUOTE_ID, QTEITM_RECORD_ID,  QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,KPU, SERIAL_NO, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, TECHNOLOGY,CUSTOMER_TOOL_ID, EQUIPMENTCATEGORY_ID, EQUIPMENTCATEGORY_RECORD_ID, EQUIPMENT_STATUS, MNT_PLANT_ID, MNT_PLANT_NAME, MNT_PLANT_RECORD_ID, SLSDIS_PRICE_MARGIN_RECORD_ID, SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID, TARGET_PRICE_MARGIN, TARGET_PRICE_MARGIN_RECORD_ID, WARRANTY_END_DATE, WARRANTY_START_DATE, GREENBOOK, GREENBOOK_RECORD_ID,  YEAR_OVER_YEAR, GLOBAL_CURRENCY,GLOBAL_CURRENCY_RECORD_ID, YEAR, NET_PRICE_INGL_CURR,OBJECT_TYPE, QUOTE_ITEM_COVERED_OBJECT_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified)
				SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_COVERED_OBJECT_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED,{UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
				SELECT DISTINCT					
					SAQSCO.EQUIPMENT_DESCRIPTION,
					'ACQUIRED' AS STATUS,
					SAQSCO.EQUIPMENT_QUANTITY,
					'0' AS DISCOUNT,
					SAQRIT.OBJECT_ID,
					SAQSCO.EQUIPMENT_ID,
					SAQSCO.EQUIPMENT_RECORD_ID,                        
					SAQRIT.CONTRACT_VALID_FROM,
					SAQRIT.CONTRACT_VALID_TO,
					SAQRIT.LINE,
					SAQSCO.PLATFORM,
					SAQRIT.QUOTE_ID, 
					SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID, 
					SAQRIT.QUOTE_RECORD_ID,
					SAQRIT.QTEREV_ID,
					SAQRIT.QTEREV_RECORD_ID,
					SAQSCO.KPU,
					SAQSCO.SERIAL_NO, 
					SAQRIT.SERVICE_DESCRIPTION, 
					SAQRIT.SERVICE_ID, 
					SAQRIT.SERVICE_RECORD_ID,								
					SAQSCO.TECHNOLOGY,																			
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
					SAQRIT.GREENBOOK, 
					SAQRIT.GREENBOOK_RECORD_ID, 					
					PRCFVA.FACTOR_PCTVAR as YEAR_OVER_YEAR,
					SAQTRV.GLOBAL_CURRENCY,
					SAQTRV.GLOBAL_CURRENCY_RECORD_ID,
					CONTRACT_TEMP.YEAR,
					'0' AS NET_PRICE_INGL_CURR,
					SAQRIT.OBJECT_TYPE					
				FROM 
					SAQSCO (NOLOCK)					 
					JOIN (
						SELECT SAQSCE.QUOTE_RECORD_ID,SAQSCE.QTEREV_RECORD_ID, SAQTSV.SERVICE_ID,SAQSCE.EQUIPMENT_ID FROM SAQSCE (NOLOCK) INNER JOIN SAQTSV ON SAQSCE.QUOTE_RECORD_ID = SAQTSV.QUOTE_RECORD_ID  AND SAQSCE.QTEREV_RECORD_ID = SAQTSV.QTEREV_RECORD_ID AND SAQSCE.SERVICE_ID = SAQTSV.PAR_SERVICE_ID 
						WHERE SAQSCE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCE.QTEREV_RECORD_ID = '{RevisionRecordId}' AND ISNULL(CONFIGURATION_STATUS, '') = 'COMPLETE' AND SAQTSV.SERVICE_ID ='{ServiceId}'
						
					) AS IQ ON IQ.QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID AND IQ.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID AND IQ.SERVICE_ID = SAQSCO.SERVICE_ID	AND IQ.SERVICE_ID = '{ServiceId}'	AND IQ.EQUIPMENT_ID	 = SAQSCO.EQUIPMENT_ID	AND IQ.SERVICE_ID = '{ServiceId}'
					JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID         
					JOIN SAQTRV (NOLOCK) ON SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID 
					JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = SAQTRV.QUOTE_RECORD_ID
											AND SAQRIT.SERVICE_RECORD_ID = SAQSCO.SERVICE_RECORD_ID
											AND SAQRIT.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID
											AND SAQRIT.GREENBOOK_RECORD_ID = SAQSCO.GREENBOOK_RECORD_ID					
					LEFT JOIN PRCFVA (NOLOCK) ON PRCFVA.FACTOR_VARIABLE_ID = SAQRIT.SERVICE_ID AND PRCFVA.FACTOR_ID = 'YOYDIS'	
					LEFT JOIN SAQICO (NOLOCK) ON SAQICO.QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID AND SAQICO.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID AND SAQICO.SERVICE_RECORD_ID = SAQSCO.SERVICE_RECORD_ID AND SAQICO.GREENBOOK_RECORD_ID = SAQSCO.GREENBOOK_RECORD_ID AND SAQICO.FABLOCATION_RECORD_ID = SAQSCO.FABLOCATION_RECORD_ID AND SAQICO.EQUIPMENT_RECORD_ID = SAQSCO.EQUIPMENT_RECORD_ID
					LEFT JOIN (
						SELECT DATEADD(year,1,CONTRACT_VALID_FROM) as date_year,'YEAR 1' AS year,equipment_id,QUOTE_RECORD_ID,SERVICE_ID,QTEREV_RECORD_ID,EQUIPMENT_RECORD_ID FROM SAQSCO WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID = '{ServiceId}' 
						UNION ALL  
						SELECT DATEADD(year,2,CONTRACT_VALID_FROM) as date_year,'YEAR 2' AS year,equipment_id,QUOTE_RECORD_ID,SERVICE_ID,QTEREV_RECORD_ID,EQUIPMENT_RECORD_ID FROM SAQSCO WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID = '{ServiceId}' AND  1 = (CASE WHEN DATEDIFF(MONTH, SAQSCO.CONTRACT_VALID_FROM, SAQSCO.CONTRACT_VALID_TO) > 12 then 1 else 0 end )
						UNION ALL  
						SELECT DATEADD(year,3,CONTRACT_VALID_FROM) as date_year,'YEAR 3' AS year,equipment_id,QUOTE_RECORD_ID,SERVICE_ID,QTEREV_RECORD_ID,EQUIPMENT_RECORD_ID FROM SAQSCO WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID = '{ServiceId}' AND  1 = (CASE WHEN DATEDIFF(MONTH, SAQSCO.CONTRACT_VALID_FROM, SAQSCO.CONTRACT_VALID_TO) > 24 then 1 else 0 end )
						UNION ALL  
						SELECT DATEADD(year,4,CONTRACT_VALID_FROM) as date_year,'YEAR 4' AS year,equipment_id,QUOTE_RECORD_ID,SERVICE_ID,QTEREV_RECORD_ID,EQUIPMENT_RECORD_ID FROM SAQSCO WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID = '{ServiceId}' AND  1 = (CASE WHEN DATEDIFF(MONTH, SAQSCO.CONTRACT_VALID_FROM, SAQSCO.CONTRACT_VALID_TO) > 36  then 1 else 0 end )
						UNION ALL  
						SELECT DATEADD(year,5,CONTRACT_VALID_FROM) as date_year,'YEAR 5' AS year,equipment_id,QUOTE_RECORD_ID,SERVICE_ID,QTEREV_RECORD_ID,EQUIPMENT_RECORD_ID FROM SAQSCO WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID = '{ServiceId}' AND  1 = (CASE WHEN DATEDIFF(MONTH, SAQSCO.CONTRACT_VALID_FROM, SAQSCO.CONTRACT_VALID_TO) > 48  then 1 else 0 end ) 

					) CONTRACT_TEMP ON  CONTRACT_TEMP.QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID AND CONTRACT_TEMP.SERVICE_ID = SAQSCO.SERVICE_ID AND CONTRACT_TEMP.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID AND CONTRACT_TEMP.EQUIPMENT_RECORD_ID = SAQSCO.EQUIPMENT_RECORD_ID
				WHERE 
					SAQSCO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCO.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQSCO.SERVICE_ID = '{ServiceId}'  AND ISNULL(SAQICO.EQUIPMENT_RECORD_ID,'') = '' 
				) IQ
				""".format(UserId=self.user_id, UserName=self.user_name, QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id, JoinString='')
			)

	def _insert_quote_item_forecast_parts(self):
		Sql.RunQuery("""INSERT SAQRIP (QUOTE_REVISION_ITEM_PRODUCT_LIST_RECORD_ID,CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified, PART_DESCRIPTION, PART_NUMBER, PART_RECORD_ID, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, QUANTITY, QUOTE_ID, QTEITM_RECORD_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, LINE ) 
			SELECT 
				CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REVISION_ITEM_PRODUCT_LIST_RECORD_ID,
				'{UserName}' AS CPQTABLEENTRYADDEDBY,
				GETDATE() as CPQTABLEENTRYDATEADDED,
				{UserId} as CpqTableEntryModifiedBy,
				GETDATE() as CpqTableEntryDateModified,
				SAQRSP.PART_DESCRIPTION,
				SAQRSP.PART_NUMBER,
				SAQRSP.PART_RECORD_ID,
				SAQRSP.SERVICE_DESCRIPTION,
				SAQRSP.SERVICE_ID,
				SAQRSP.SERVICE_RECORD_ID,
				SAQRSP.QUANTITY,
				SAQRSP.QUOTE_ID,
				SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID,
				SAQRSP.QUOTE_RECORD_ID,
				SAQRSP.QTEREV_ID,
				SAQRSP.QTEREV_RECORD_ID,
				SAQRIT.LINE
			FROM SAQRSP (NOLOCK) 
			JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = SAQRSP.QUOTE_RECORD_ID AND SAQRIT.QTEREV_RECORD_ID = SAQRSP.QTEREV_RECORD_ID AND SAQRIT.SERVICE_RECORD_ID = SAQRSP.SERVICE_RECORD_ID AND SAQRIT.GREENBOOK_RECORD_ID = SAQRSP.GREENBOOK_RECORD_ID AND SAQRIT.FABLOCATION_RECORD_ID = SAQRSP.FABLOCATION_RECORD_ID 
			LEFT JOIN SAQRIP (NOLOCK) ON SAQRIP.QUOTE_RECORD_ID = SAQRSP.QUOTE_RECORD_ID AND SAQRIP.QTEREV_RECORD_ID = SAQRSP.QTEREV_RECORD_ID AND SAQRIP.SERVICE_RECORD_ID = SAQRSP.SERVICE_RECORD_ID AND SAQRIP.PART_RECORD_ID = SAQRSP.PART_RECORD_ID 

			WHERE SAQRSP.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRSP.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQRSP.SERVICE_ID = '{ServiceId}' AND ISNULL(SAQRIP.PART_RECORD_ID,'') = '' """.format(UserId=self.user_id, UserName=self.user_name, QuoteRecordId=self.contract_quote_record_id, RevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
	
		
	def _insert_quote_item_fpm_forecast_parts(self):
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
							'{LineItemId}' as LINE_ITEM_ID,
							{PartLineId},
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


	def _delete_item_related_table_records(self):
		for delete_object in ['SAQIAE','SAQICA','SAQRIO','SAQICO']:
			delete_statement = "DELETE DT FROM " +str(delete_object)+" DT (NOLOCK) JOIN SAQSCE (NOLOCK) ON DT.EQUIPMENT_RECORD_ID = SAQSCE.EQUIPMENT_RECORD_ID AND DT.SERVICE_ID=SAQSCE.SERVICE_ID AND DT.QUOTE_RECORD_ID=SAQSCE.QUOTE_RECORD_ID AND DT.QTEREV_RECORD_ID=SAQSCE.QTEREV_RECORD_ID WHERE DT.QUOTE_RECORD_ID='{}' AND DT.QTEREV_RECORD_ID='{}' AND ISNULL(SAQSCE.CONFIGURATION_STATUS, '')='INCOMPLETE' AND DT.SERVICE_ID='{}' ".format(self.contract_quote_record_id, self.contract_quote_revision_record_id, self.service_id)			
			Sql.RunQuery(delete_statement)
		join_condition_string = ''
		if self.quote_service_entitlement_type == 'OFFERING + EQUIPMENT':
			join_condition_string = 'AND ISNULL(SAQRIT.OBJECT_ID, '') = SAQSCE.EQUIPMENT_ID'
		# item entitlement delete
		quote_item_entitlement_delete_statement = """
				DELETE SAQITE 
					FROM SAQITE (NOLOCK) 
					JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID = SAQITE.QTEITM_RECORD_ID 
					JOIN SAQSCE ON SAQSCE.QUOTE_RECORD_ID=SAQRIT.QUOTE_RECORD_ID AND SAQSCE.QTEREV_RECORD_ID=SAQRIT.QTEREV_RECORD_ID AND SAQSCE.SERVICE_ID=SAQRIT.SERVICE_ID AND SAQSCE.FABLOCATION_RECORD_ID = SAQRIT.FABLOCATION_RECORD_ID AND SAQSCE.GREENBOOK_RECORD_ID = SAQRIT.GREENBOOK_RECORD_ID {JoinCondition}
					WHERE SAQITE.QUOTE_RECORD_ID='{QuoteRecordId}' AND SAQITE.QTEREV_RECORD_ID='{QuoteRevisionRecordId}' AND ISNULL(SAQSCE.CONFIGURATION_STATUS, '')='INCOMPLETE' AND SAQITE.SERVICE_ID='{ServiceId}' """.format(QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id, JoinCondition=join_condition_string)	
		Sql.RunQuery(quote_item_entitlement_delete_statement)
		# item delete
		quote_item_delete_statement = """
				DELETE SAQRIT 
					FROM SAQRIT (NOLOCK) 
					JOIN SAQSCE ON SAQSCE.QUOTE_RECORD_ID=SAQRIT.QUOTE_RECORD_ID AND SAQSCE.QTEREV_RECORD_ID=SAQRIT.QTEREV_RECORD_ID AND SAQSCE.SERVICE_ID=SAQRIT.SERVICE_ID AND SAQSCE.FABLOCATION_RECORD_ID = SAQRIT.FABLOCATION_RECORD_ID AND SAQSCE.GREENBOOK_RECORD_ID = SAQRIT.GREENBOOK_RECORD_ID {JoinCondition}
					WHERE SAQRIT.QUOTE_RECORD_ID='{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID='{QuoteRevisionRecordId}' AND ISNULL(SAQSCE.CONFIGURATION_STATUS, '') ='INCOMPLETE' AND SAQRIT.SERVICE_ID='{ServiceId}' """.format(QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id, JoinCondition=join_condition_string)	
		Sql.RunQuery(quote_item_delete_statement)

	def _delete_z0046_quote_items(self):
		if self.service_id == 'Z0046':
			deleting_tables_list = ['SAQRIT','SAQRIO','SAQITE','SAQICO']
			for obj in deleting_tables_list:
				Sql.RunQuery("DELETE {obj} FROM {obj} (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}'".format(QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id, obj = obj))

	def _spare_quote_items_entitlement_insert(self, update=False):		
		#if update: # need to verify one more time
		Sql.RunQuery("DELETE SAQITE FROM SAQITE WHERE SAQITE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQITE.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQITE.SERVICE_ID = '{ServiceId}'".format(QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
		Sql.RunQuery("""INSERT SAQITE (QUOTE_REV_ITEM_ENTITLEMENT_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified, CPS_CONFIGURATION_ID, CPS_MATCH_ID, ENTITLEMENT_COST_IMPACT, ENTITLEMENT_GROUP_ID, ENTITLEMENT_GROUP_XML, ENTITLEMENT_PRICE_IMPACT, ENTITLEMENT_XML, IS_CHANGED, LINE, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, QTEITM_RECORD_ID, QUOTE_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID)
					SELECT
						CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REV_ITEM_ENTITLEMENT_RECORD_ID,
						'{UserName}' AS CPQTABLEENTRYADDEDBY,
						GETDATE() as CPQTABLEENTRYDATEADDED,
						{UserId} as CpqTableEntryModifiedBy,
						GETDATE() as CpqTableEntryDateModified,
						{ObjectName}.CPS_CONFIGURATION_ID,
						{ObjectName}.CPS_MATCH_ID,
						null as ENTITLEMENT_COST_IMPACT,
						null as ENTITLEMENT_GROUP_ID,
						null as ENTITLEMENT_GROUP_XML,
						null as ENTITLEMENT_PRICE_IMPACT,
						{ObjectName}.ENTITLEMENT_XML,
						null as IS_CHANGED,
						SAQRIT.LINE,						
						SAQRIT.SERVICE_DESCRIPTION,
						SAQRIT.SERVICE_ID,
						SAQRIT.SERVICE_RECORD_ID,
						SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID,						
						SAQRIT.QUOTE_ID,
						SAQRIT.QUOTE_RECORD_ID,
						SAQRIT.QTEREV_ID,
						SAQRIT.QTEREV_RECORD_ID,						
						null as GREENBOOK,
						null as GREENBOOK_RECORD_ID
					FROM {ObjectName} (NOLOCK) 
					JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = {ObjectName}.QUOTE_RECORD_ID
												AND SAQRIT.SERVICE_RECORD_ID = {ObjectName}.SERVICE_RECORD_ID
												AND SAQRIT.QTEREV_RECORD_ID = {ObjectName}.QTEREV_RECORD_ID
															
					WHERE {ObjectName}.QUOTE_RECORD_ID = '{QuoteRecordId}' AND {ObjectName}.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND {ObjectName}.SERVICE_ID = '{ServiceId}' AND ISNULL({ObjectName}.CONFIGURATION_STATUS,'') = 'COMPLETE'			
				""".format(UserId=self.user_id, UserName=self.user_name, ObjectName='SAQTSE', QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
		return True

	def _simple_delete_item_related_table_records(self):
		for delete_object in ['SAQRIO','SAQICO']:
			delete_statement = "DELETE DT FROM " +str(delete_object)+" DT (NOLOCK) JOIN SAQSCO ON DT.EQUIPMENT_RECORD_ID = SAQSCO.EQUIPMENT_RECORD_ID AND DT.SERVICE_ID=SAQSCO.SERVICE_ID  AND DT.QUOTE_RECORD_ID=SAQSCO.QUOTE_RECORD_ID AND DT.QTEREV_RECORD_ID=SAQSCO.QTEREV_RECORD_ID JOIN SAQSCE (NOLOCK) ON DT.EQUIPMENT_RECORD_ID = SAQSCE.EQUIPMENT_RECORD_ID AND SAQSCO.PAR_SERVICE_ID=SAQSCE.SERVICE_ID AND DT.QUOTE_RECORD_ID=SAQSCE.QUOTE_RECORD_ID AND DT.QTEREV_RECORD_ID=SAQSCE.QTEREV_RECORD_ID WHERE DT.QUOTE_RECORD_ID='{}' AND DT.QTEREV_RECORD_ID='{}' AND ISNULL(SAQSCE.CONFIGURATION_STATUS, '')='INCOMPLETE' AND DT.SERVICE_ID='{}' ".format(self.contract_quote_record_id, self.contract_quote_revision_record_id, self.service_id)			
			Sql.RunQuery(delete_statement)
		
		# item delete
		quote_item_delete_statement = """
				DELETE SAQRIT 
					FROM SAQRIT (NOLOCK) 
					JOIN SAQSCO (NOLOCK) ON SAQRIT.SERVICE_ID=SAQSCO.SERVICE_ID  AND SAQRIT.QUOTE_RECORD_ID=SAQSCO.QUOTE_RECORD_ID AND SAQRIT.QTEREV_RECORD_ID=SAQSCO.QTEREV_RECORD_ID JOIN SAQSCE (NOLOCK) ON SAQSCE.QUOTE_RECORD_ID=SAQRIT.QUOTE_RECORD_ID AND SAQSCE.QTEREV_RECORD_ID=SAQRIT.QTEREV_RECORD_ID AND SAQSCE.SERVICE_ID=SAQSCO.PAR_SERVICE_ID AND SAQSCE.FABLOCATION_RECORD_ID = SAQRIT.FABLOCATION_RECORD_ID AND SAQSCE.GREENBOOK_RECORD_ID = SAQRIT.GREENBOOK_RECORD_ID 
					WHERE SAQRIT.QUOTE_RECORD_ID='{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID='{QuoteRevisionRecordId}' AND ISNULL(SAQSCE.CONFIGURATION_STATUS, '') ='INCOMPLETE' AND SAQRIT.SERVICE_ID='{ServiceId}' """.format(QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id)	
		Sql.RunQuery(quote_item_delete_statement)

	def _quote_item_qty_update(self):
		Sql.RunQuery(""" UPDATE SAQRIT SET QUANTITY = IQ.QUANTITY FROM SAQRIT (NOLOCK) INNER JOIN (SELECT COUNT(*) AS QUANTITY,QTEREV_RECORD_ID, QUOTE_RECORD_ID, SERVICE_ID,GREENBOOK FROM SAQRIO (NOLOCK) WHERE 
					QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}' GROUP BY QTEREV_RECORD_ID, QUOTE_RECORD_ID, SERVICE_ID,GREENBOOK ) IQ ON IQ.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND IQ.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID AND IQ.SERVICE_ID = SAQRIT.SERVICE_ID AND SAQRIT.GREENBOOK = IQ.GREENBOOK WHERE 
					SAQRIT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQRIT.SERVICE_ID = '{ServiceId}'""".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id))

	def _do_opertion(self):		
		self._set_quote_service_entitlement_type()
		if self.action_type == "INSERT_LINE_ITEMS":			
			if self.is_spare_service == True:				
				# Spare Parts Insert/Update
				self._quote_items_summary_insert()
				self._quote_items_insert()
				self._insert_quote_item_forecast_parts()
				self._quote_annualized_items_insert()
			elif self.is_fpm_spare_service == True:				
				# Spare Parts Insert/Update
				self._quote_items_insert()
				self._insert_quote_item_fpm_forecast_parts()
				self._quote_annualized_items_insert()
			elif self.is_simple_service == True:
				self._simple_quote_items_insert()
				self._simple_items_object_insert()
				self._simple_quote_annualized_items_insert()
			else:	
				self._quote_items_summary_insert()
				self._quote_items_insert()		
				self._quote_items_object_insert()	
				self._quote_annualized_items_insert()	
				self._quote_item_line_entitlement_insert()
				self._quote_items_assembly_insert()
				self._quote_items_assembly_entitlement_insert()
		else:
			##deleting Z0046 SAQRIT records
			self._delete_z0046_quote_items()
			quote_revision_item_obj = Sql.GetFirst("SELECT CpqTableEntryId FROM SAQRIT (NOLOCK) WHERE SAQRIT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQRIT.SERVICE_ID = '{ServiceId}'".format(QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
			if not quote_revision_item_obj:
				
				if self.service_id == 'Z0101':	
					if self.is_spare_service == True:			
						# Spare Parts Insert/Update
						self._quote_items_summary_insert()
						self._quote_items_insert()
						self._insert_quote_item_forecast_parts()
						self._quote_annualized_items_insert()
				##simple product quote item insert
				elif self.is_simple_service == True:
					self._simple_quote_items_insert()
					self._simple_items_object_insert()
					self._simple_quote_annualized_items_insert()
				else:
					self._quote_items_summary_insert()
					self._quote_items_insert()		
					self._quote_items_object_insert()	
					#self.cqent()
					self._quote_item_line_entitlement_insert()
					self._quote_items_assembly_insert()
					self._quote_items_assembly_entitlement_insert()
			else:
				self._delete_item_related_table_records()
				
				if self.service_id == 'Z0101':	
					if self.is_spare_service == True:			
						# Spare Parts Insert/Update
						self._quote_items_summary_insert()
						self._quote_items_insert()
						self._insert_quote_item_forecast_parts()
						self._quote_annualized_items_insert()
				elif self.is_simple_service == True:
					self._simple_delete_item_related_table_records()
					self._simple_quote_items_insert()
					self._simple_items_object_insert()
					self._simple_quote_annualized_items_insert()
				else:
					self._quote_items_summary_insert()
					self._quote_items_insert(update=True)		
					self._quote_items_object_insert(update=True)	
					self._quote_annualized_items_insert(update=True)
					self._quote_item_line_entitlement_insert(update=True)
					self._quote_items_assembly_insert(update=True)
					self._quote_items_assembly_entitlement_insert(update=True)
				
		# Pricing Calculation - Start
		quote_line_item_obj = Sql.GetFirst("SELECT EQUIPMENT_LINE_ID FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}' AND ISNULL(STATUS,'') = ''".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
		if quote_line_item_obj:
			ScriptExecutor.ExecuteGlobal('QTPOSTACRM',{'QUOTE_ID':self.contract_quote_id,'REVISION_ID':self.contract_quote_revision_id, 'Fun_type':'cpq_to_sscm'})
			SqlHelper.GetFirst("sp_executesql @T=N'update A SET A.STATUS = (CASE WHEN A.STATUS =''ERROR'' THEN ''ERROR'' WHEN A.STATUS =''PARTIALLY PRICED'' THEN ''ERROR'' END) from SAQRIT A inner join ( select SERVICE_ID,LINE,SAQICO.QUOTE_ID from SAQICO WHERE SAQICO.QUOTE_ID = ''"+str(self.contract_quote_id)+"'' group by SERVICE_ID,LINE,SAQICO.QUOTE_ID Having count(*) > 1 ) as od on od.LINE = A.LINE AND od.SERVICE_ID = A.SERVICE_ID '")
			SqlHelper.GetFirst("sp_executesql @T=N'update A SET A.STATUS = (CASE WHEN A.STATUS =''ACQUIRING'' THEN ''ACQUIRING'' WHEN A.STATUS =''ERROR'' THEN ''ERROR'' END) from SAQRIT A inner join ( select SERVICE_ID,LINE,SAQICO.QUOTE_ID from SAQICO WHERE SAQICO.QUOTE_ID = ''"+str(self.contract_quote_id)+"'' group by SERVICE_ID,LINE,SAQICO.QUOTE_ID Having count(*) > 1 ) as od on od.LINE = A.LINE AND od.SERVICE_ID = A.SERVICE_ID '")
			SqlHelper.GetFirst("sp_executesql @T=N'update A SET A.STATUS = (CASE WHEN A.STATUS =''ACQUIRING'' THEN ''PARTIALLY PRICING'' WHEN A.STATUS =''PARTIALLY PRICING'' THEN ''PARTIALLY PRICING'' END) from SAQRIT A inner join ( select SERVICE_ID,LINE,SAQICO.QUOTE_ID from SAQICO WHERE SAQICO.QUOTE_ID = ''"+str(self.contract_quote_id)+"'' group by SERVICE_ID,LINE,SAQICO.QUOTE_ID Having count(*) > 1 ) as od on od.LINE = A.LINE AND od.SERVICE_ID = A.SERVICE_ID '")
		# Pricing Calculation - End
		return True

try:
	where_condition_string = Param.WhereString
except:
	where_condition_string = ''
action_type = Param.ActionType
try:
	entitlement_level_obj = Param.EntitlementLevel
except:
	entitlement_level_obj = "SAQTSE"
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
parameters['entitlement_level_obj'] = str(entitlement_level_obj)
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
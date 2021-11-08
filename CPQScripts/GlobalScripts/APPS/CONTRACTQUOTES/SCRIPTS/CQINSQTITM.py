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
	
	def _quote_items_insert(self):
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
												WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' and SERVICE_ID = '{ServiceId}' 
												) IQ 
											OUTER APPLY IQ.ENTITLEMENT_XML.nodes('QUOTE_ITEM_ENTITLEMENT') as X(Y) 
										) as OQ 
										WHERE ENTITLEMENT_ID LIKE '{EntitlementAttrId}'""".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id,EntitlementAttrId='AGS_'+str(self.service_id)+'_PQB_QTITST'))
		if service_entitlement_obj:
			source_object_name = ''
			if (service_entitlement_obj.ENTITLEMENT_DISPLAY_VALUE).upper() == 'OFFERING + EQUIPMENT':
				source_object_name = 'SAQSCE'
			elif (service_entitlement_obj.ENTITLEMENT_DISPLAY_VALUE).upper() == '':
				source_object_name = 'SAQTGE'
			else:
				return False
			if source_object_name:
				Sql.RunQuery("""INSERT SAQRIT (QUOTE_REVISION_CONTRACT_ITEM_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified, CONTRACT_VALID_FROM, CONTRACT_VALID_TO, DOC_CURRENCY, DOCURR_RECORD_ID, EXCHANGE_RATE, EXCHANGE_RATE_DATE, EXCHANGE_RATE_RECORD_ID, GL_ACCOUNT_NO, GLOBAL_CURRENCY, GLOBAL_CURRENCY_RECORD_ID, LINE, OBJECT_ID, OBJECT_TYPE, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, PROFIT_CENTER, QUANTITY, QUOTE_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, REF_SALESORDER, STATUS, TAXCLASSIFICATION_DESCRIPTION, TAXCLASSIFICATION_ID, TAXCLASSIFICATION_RECORD_ID)
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
						MAMSCT.TAXCLASSIFICATION_RECORD_ID
					FROM {ObjectName} (NOLOCK) 
					JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = {ObjectName}.QUOTE_RECORD_ID  AND SAQTMT.QTEREV_RECORD_ID = {ObjectName}.QTEREV_RECORD_ID     
					JOIN SAQTRV (NOLOCK) ON SAQTRV.SALESORG_RECORD_ID = {ObjectName}.SALESORG_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = {ObjectName}.QTEREV_RECORD_ID AND SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID
					JOIN MAMTRL (NOLOCK) ON MAMTRL.SAP_PART_NUMBER = {ObjectName}.SERVICE_ID 
					LEFT JOIN MAMSCT (NOLOCK) ON MAMSCT.DISTRIBUTIONCHANNEL_RECORD_ID = SAQTRV.DISTRIBUTIONCHANNEL_RECORD_ID AND MAMSCT.COUNTRY_RECORD_ID = SAQTRV.COUNTRY_RECORD_ID AND MAMSCT.DIVISION_ID = SAQTRV.DIVISION_ID AND MAMSCT.SAP_PART_NUMBER = MAMTRL.SAP_PART_NUMBER
					WHERE {ObjectName}.QUOTE_RECORD_ID = '{QuoteRecordId}' AND {ObjectName}.QTEREV_RECORD_ID = '{RevisionRecordId}' AND {ObjectName}.SERVICE_ID = '{ServiceId}'				
				""".format(ObjectName=source_object_name, QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id, EquipmentsCount=0))

		return True
		
	
	def _do_opertion(self):		
		if self.action_type == "INSERT_LINE_ITEMS":			
			if self.is_spare_service:				
				# Spare Parts Insert/Update
				pass
			else:	
				self._quote_items_insert()				
		else:
			self._quote_items_update()	
		# Pricing Calculation - Start
		# quote_line_item_obj = Sql.GetFirst("SELECT EQUIPMENT_LINE_ID FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID = '{ServiceId}' AND ISNULL(STATUS,'') = ''".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
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
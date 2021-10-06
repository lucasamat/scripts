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
from SYDATABASE import SQL

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
        self.set_contract_quote_related_details()

    def set_contract_quote_related_details(self):
        contract_quote_obj = Sql.GetFirst("SELECT QUOTE_ID, QUOTE_TYPE, SALE_TYPE FROM SAQTMT (NOLOCK) WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{}'".format(self.contract_quote_record_id))
        if contract_quote_obj:
            self.contract_quote_id = contract_quote_obj.QUOTE_ID      
            self.quote_type = contract_quote_obj.QUOTE_TYPE
            self.sale_type = contract_quote_obj.SALE_TYPE
        else:
            self.contract_quote_id = ''  
            self.quote_type = ''
            self.sale_type = ''
        return True

    def _quote_item_delete_process(self):
        for delete_object in ['SAQIAE','SAQICA', 'SAQIEN', 'SAQICO']:
            delete_statement = "DELETE DT FROM " +str(delete_object)+" DT JOIN SAQSCE ON DT.EQUIPMENT_RECORD_ID = SAQSCE.EQUIPMENT_RECORD_ID AND DT.SERVICE_ID=SAQSCE.SERVICE_ID AND DT.QUOTE_RECORD_ID=SAQSCE.QUOTE_RECORD_ID AND DT.QTEREV_RECORD_ID=SAQSCE.QTEREV_RECORD_ID WHERE DT.QUOTE_RECORD_ID='{}' AND DT.QTEREV_RECORD_ID='{}' AND SAQSCE.CONFIGURATION_STATUS ='INCOMPLETE' AND DT.SERVICE_ID='{}' ".format(str(self.contract_quote_record_id), str(self.contract_quote_revision_record_id), str(self.service_id))
            Sql.RunQuery(delete_statement)

        delete_statement = "DELETE DT FROM SAQIGB DT JOIN SAQICO ON DT.SERVICE_ID = SAQICO.SERVICE_ID AND DT.QUOTE_RECORD_ID = SAQICO.QUOTE_RECORD_ID AND DT.QTEREV_RECORD_ID=SAQICO.QTEREV_RECORD_ID AND DT.GREENBOOK != SAQICO.GREENBOOK WHERE DT.QUOTE_RECORD_ID='{}' AND DT.QTEREV_RECORD_ID='{}' AND DT.SERVICE_ID='{}' ".format(str(self.contract_quote_record_id), str(self.contract_quote_revision_record_id), str(self.service_id))
        Sql.RunQuery(delete_statement)
        
        delete_statement = "DELETE DT FROM SAQIFL DT JOIN SAQICO ON DT.SERVICE_ID = SAQICO.SERVICE_ID AND DT.QUOTE_RECORD_ID=SAQICO.QUOTE_RECORD_ID AND DT.QTEREV_RECORD_ID = SAQICO.QTEREV_RECORD_ID AND DT.FABLOCATION_ID != SAQICO.FABLOCATION_ID WHERE DT.QUOTE_RECORD_ID='{}' AND DT.QTEREV_RECORD_ID='{}' AND DT.SERVICE_ID='{}' ".format(str(self.contract_quote_record_id), str(self.contract_quote_revision_record_id), str(self.service_id))
        Sql.RunQuery(delete_statement) 

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
                    SAQTMT.QUOTE_CURRENCY as CURRENCY,
                    SAQTMT.QUOTE_CURRENCY_RECORD_ID as CURRENCY_RECORD_ID,
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
                        WHERE SAQSCE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCE.QTEREV_RECORD_ID = '{RevisionRecordId}' AND ISNULL(CONFIGURATION_STATUS, '') = 'COMPLETE' {WhereString}
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
                QuoteRecordId=self.contract_quote_record_id,
                RevisionRecordId=self.contract_quote_revision_record_id,
                UserId=self.user_id,
                UserName=self.user_name,
                WhereString=where_string,
                ExistingCount=max_quote_item_count
            ))
        # Insert SAQITM - End
        return True
    
    def _quote_item_lines_insert_process(self, where_string='', join_string=''):
        ##inserting SAQICO except chamber based equipment A055S000P01-6826		
        Sql.RunQuery("""INSERT SAQICO (BD_PRICE,ENTITLEMENT_PRICE_IMPACT,ENTITLEMENT_COST_IMPACT, EQUIPMENT_DESCRIPTION,STATUS,EQUIPMENT_ID, EQUIPMENT_RECORD_ID, FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, CONTRACT_VALID_FROM, CONTRACT_VALID_TO,LINE_ITEM_ID, MATERIAL_RECORD_ID, PLATFORM, QUOTE_ID, QTEITM_RECORD_ID, QUOTE_NAME, QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,KPU, NET_PRICE, SAP_PART_NUMBER, SERIAL_NO, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, WAFER_SIZE, TARGET_PRICE, TECHNOLOGY,SRVTAXCAT_RECORD_ID,SRVTAXCAT_DESCRIPTION,SRVTAXCAT_ID,SRVTAXCLA_DESCRIPTION,SRVTAXCLA_ID,SRVTAXCLA_RECORD_ID, BD_DISCOUNT, BD_DISCOUNT_RECORD_ID, BD_PRICE_MARGIN, BD_PRICE_MARGIN_RECORD_ID, CEILING_PRICE, CLEANING_COST, CM_PART_COST, CUSTOMER_TOOL_ID, EQUIPMENTCATEGORY_ID, EQUIPMENTCATEGORY_RECORD_ID, EQUIPMENT_STATUS, KPI_COST,MODEL_PRICE,TOTAL_COST_WOSEEDSTOCK,TOTAL_COST_WSEEDSTOCK, LABOR_COST, MNT_PLANT_ID, MNT_PLANT_NAME, MNT_PLANT_RECORD_ID, PM_PART_COST, SLSDIS_PRICE_MARGIN_RECORD_ID, SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID, TARGET_PRICE_MARGIN, TARGET_PRICE_MARGIN_RECORD_ID, WARRANTY_END_DATE, WARRANTY_START_DATE, GREENBOOK, GREENBOOK_RECORD_ID, EQUIPMENT_LINE_ID, NET_VALUE, SALES_DISCOUNT_PRICE, YEAR_1, YEAR_2, YEAR_3, YEAR_4, YEAR_5, EQUIPMENT_QUANTITY, YEAR_OVER_YEAR, EXCHANGE_RATE, EXCHANGE_RATE_DATE, EXCHANGE_RATE_RECORD_ID,GLOBAL_CURRENCY,DOC_CURRENCY,DOCURR_RECORD_ID, GLOBAL_CURRENCY_RECORD_ID, LINE, QUOTE_ITEM_COVERED_OBJECT_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified)
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
                    SAQITM.SRVTAXCLA_RECORD_ID,
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
                            ELSE ROW_NUMBER()OVER(ORDER BY(SAQSCO.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID)) * 1 
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
                    SAQITM.LINE_ITEM_ID + '.'+ CAST(ROW_NUMBER()OVER(PARTITION BY SAQITM.LINE_ITEM_ID ORDER BY(SAQSCO.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID)) AS varchar ) as LINE
                FROM 
                    SAQSCO (NOLOCK)					 
                    JOIN SAQSCE (NOLOCK) ON SAQSCE.QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID AND SAQSCE.SERVICE_ID = SAQSCO.SERVICE_ID AND SAQSCE.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID
                    AND SAQSCE.EQUIPMENT_RECORD_ID = SAQSCO.EQUIPMENT_RECORD_ID 
                    JOIN MAMTRL (NOLOCK) ON MAMTRL.SAP_PART_NUMBER = SAQSCE.SERVICE_ID					
                    JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID  AND SAQTMT.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID         
                    JOIN SAQTRV (NOLOCK) ON SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID 
                    JOIN SAQITM (NOLOCK) ON SAQTRV.QUOTE_RECORD_ID = SAQITM.QUOTE_RECORD_ID 
                                            AND SAQITM.SERVICE_RECORD_ID = SAQSCO.SERVICE_RECORD_ID
                                            AND SAQITM.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID
                                            {JoinString}					
                WHERE 
                    SAQSCO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCO.QTEREV_RECORD_ID = '{RevisionRecordId}' {WhereString} AND ISNULL(SAQSCO.INCLUDED,'') != 'CHAMBER' AND ISNULL(SAQSCE.CONFIGURATION_STATUS,'') = 'COMPLETE'
                ) IQ
                """.format(UserId=self.user_id, UserName=self.user_name, QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id,
                JoinString=join_string, WhereString=where_string )
            )
        # if 'Z0016' in where_string:
        # 	Sql.RunQuery("""UPDATE SAQICO
        # 							SET
        # 							SAQICO.ENTITLEMENT_PRICE_IMPACT = SAQSCE_TEMP.TARGET_PRICE,
        # 							SAQICO.ENTITLEMENT_COST_IMPACT = SAQSCE_TEMP.TOTAL_COST,
        # 							SAQICO.TARGET_PRICE = SAQSCE_TEMP.TARGET_PRICE,
        # 							SAQICO.NET_VALUE = SAQSCE_TEMP.TARGET_PRICE,
        # 							SAQICO.YEAR_1 = SAQSCE_TEMP.YEAR_1,
        # 							SAQICO.YEAR_2 = SAQSCE_TEMP.YEAR_2					
        # 							FROM SAQICO	(NOLOCK)
        # 							LEFT JOIN (
        # 									SELECT QUOTE_ID, EQUIPMENT_ID, SERVICE_ID, SUM(CASE WHEN Isnumeric(ENTITLEMENT_PRICE_IMPACT) = 1 THEN CONVERT(DECIMAL(18,2),ENTITLEMENT_PRICE_IMPACT) ELSE 0 END) * 1 AS TARGET_PRICE, SUM(CASE WHEN Isnumeric(ENTITLEMENT_COST_IMPACT) = 1 THEN CONVERT(DECIMAL(18,2),ENTITLEMENT_COST_IMPACT) ELSE 0 END) AS TOTAL_COST, SUM(CASE WHEN Isnumeric(ENTITLEMENT_PRICE_IMPACT) = 1 THEN CASE WHEN ENTITLEMENT_ID LIKE 'AGS_LAB_OPT%_P%' THEN CONVERT(DECIMAL(18,2),ENTITLEMENT_PRICE_IMPACT) ELSE 0 END ELSE 0 END) AS YEAR_2, SUM(CASE WHEN Isnumeric(ENTITLEMENT_PRICE_IMPACT) = 1 THEN CASE WHEN ENTITLEMENT_ID NOT LIKE 'AGS_LAB_OPT%_P%' THEN CONVERT(DECIMAL(18,2),ENTITLEMENT_PRICE_IMPACT) ELSE 0 END ELSE 0 END) AS YEAR_1 from (SELECT * FROM {PriceTemp}) IQ GROUP BY QUOTE_ID, EQUIPMENT_ID, SERVICE_ID
        # 								) SAQSCE_TEMP ON SAQSCE_TEMP.QUOTE_ID = SAQSCO.QUOTE_ID AND SAQSCE_TEMP.EQUIPMENT_ID = SAQSCO.EQUIPMENT_ID AND SAQSCE_TEMP.SERVICE_ID = SAQSCO.SERVICE_ID				
        # 							WHERE 
        # 								SAQSCO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCO.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQSCO.SERVICE_ID = 'Z0016' AND ISNULL(SAQSCO.INCLUDED,'') != 'CHAMBER'		
        # 							""".format(PriceTemp=price_temp, QuoteRecordId=self.contract_quote_record_id, RevisionRecordId=self.contract_quote_revision_record_id))	 
        
        ##inserting assembly to SAQICO if a equipemnt is chamber based FTS A055S000P01-6826
        if self.sale_type == 'TOOL RELOCATION':			
            Sql.RunQuery("""INSERT SAQICO (BD_PRICE,ENTITLEMENT_PRICE_IMPACT,ENTITLEMENT_COST_IMPACT, EQUIPMENT_DESCRIPTION,STATUS,EQUIPMENT_ID, EQUIPMENT_RECORD_ID, FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, CONTRACT_VALID_FROM, CONTRACT_VALID_TO, LINE_ITEM_ID, MATERIAL_RECORD_ID, PLATFORM, QUOTE_ID, QTEITM_RECORD_ID, QUOTE_NAME, QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,KPU, NET_PRICE, SAP_PART_NUMBER, SERIAL_NO, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, WAFER_SIZE, TARGET_PRICE, TECHNOLOGY,SRVTAXCAT_RECORD_ID,SRVTAXCAT_DESCRIPTION,SRVTAXCAT_ID,SRVTAXCLA_DESCRIPTION,SRVTAXCLA_ID,SRVTAXCLA_RECORD_ID, BD_DISCOUNT, BD_DISCOUNT_RECORD_ID, BD_PRICE_MARGIN, BD_PRICE_MARGIN_RECORD_ID, CEILING_PRICE, CLEANING_COST, CM_PART_COST, CUSTOMER_TOOL_ID, EQUIPMENTCATEGORY_ID, EQUIPMENTCATEGORY_RECORD_ID, EQUIPMENT_STATUS, KPI_COST,MODEL_PRICE,TOTAL_COST_WOSEEDSTOCK,TOTAL_COST_WSEEDSTOCK, LABOR_COST, MNT_PLANT_ID, MNT_PLANT_NAME, MNT_PLANT_RECORD_ID, PM_PART_COST, SLSDIS_PRICE_MARGIN_RECORD_ID, SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID, TARGET_PRICE_MARGIN, TARGET_PRICE_MARGIN_RECORD_ID, WARRANTY_END_DATE, WARRANTY_START_DATE, GREENBOOK, GREENBOOK_RECORD_ID, EQUIPMENT_LINE_ID, NET_VALUE, SALES_DISCOUNT_PRICE, YEAR_1, YEAR_2, YEAR_3, YEAR_4, YEAR_5, EQUIPMENT_QUANTITY, YEAR_OVER_YEAR, EXCHANGE_RATE, EXCHANGE_RATE_DATE, EXCHANGE_RATE_RECORD_ID,GLOBAL_CURRENCY,DOC_CURRENCY,DOCURR_RECORD_ID, GLOBAL_CURRENCY_RECORD_ID, LINE,ASSEMBLY_ID,ASSEMBLY_RECORD_ID, QUOTE_ITEM_COVERED_OBJECT_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified)
                    SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_COVERED_OBJECT_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED,{UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
                    SELECT DISTINCT
                        null as BD_PRICE,
                        0 as ENTITLEMENT_PRICE_IMPACT,
                        0 AS ENTITLEMENT_COST_IMPACT,
                        SAQSCO.EQUIPMENT_DESCRIPTION,
                        'ACQUIRING' AS STATUS,
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
                        SAQITM.SRVTAXCLA_RECORD_ID,
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
                                ELSE ROW_NUMBER()OVER(ORDER BY(SAQSCO.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID)) * 1 
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
                                                {JoinString}						
                    WHERE 
                        SAQSCO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCO.QTEREV_RECORD_ID = '{RevisionRecordId}' {WhereString} AND ISNULL(SAQSCO.INCLUDED,'') = 'CHAMBER' AND SAQSCA.INCLUDED = 1 AND ISNULL(SAQSCE.CONFIGURATION_STATUS,'') = 'COMPLETE'
                    ) IQ
                    """.format(UserId=self.user_id, UserName=self.user_name, QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id, 
                    JoinString=join_string, WhereString= str(where_string) )
                )
            
        # 	if 'Z0016' in where_string:
        # 		Sql.RunQuery("""UPDATE SAQICO
        # 								SET
        # 								SAQICO.ENTITLEMENT_PRICE_IMPACT = SAQSCE_TEMP.TARGET_PRICE,
        # 								SAQICO.ENTITLEMENT_COST_IMPACT = SAQSCE_TEMP.TOTAL_COST,
        # 								SAQICO.TARGET_PRICE = SAQSCE_TEMP.TARGET_PRICE,
        # 								SAQICO.NET_VALUE = SAQSCE_TEMP.TARGET_PRICE,
        # 								SAQICO.YEAR_1 = SAQSCE_TEMP.YEAR_1,
        # 								SAQICO.YEAR_2 = SAQSCE_TEMP.YEAR_2					
        # 								FROM SAQICO	(NOLOCK)
        # 								JOIN SAQSCA (NOLOCK) ON SAQSCA.QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID AND SAQSCA.SERVICE_ID = 	SAQSCO.SERVICE_ID AND SAQSCA.EQUIPMENT_RECORD_ID = SAQSCO.EQUIPMENT_RECORD_ID
        # 								LEFT JOIN (
        # 										SELECT QUOTE_ID, EQUIPMENT_ID, SERVICE_ID, SUM(CASE WHEN Isnumeric(ENTITLEMENT_PRICE_IMPACT) = 1 THEN CONVERT(DECIMAL(18,2),ENTITLEMENT_PRICE_IMPACT) ELSE 0 END) * 1 AS TARGET_PRICE, SUM(CASE WHEN Isnumeric(ENTITLEMENT_COST_IMPACT) = 1 THEN CONVERT(DECIMAL(18,2),ENTITLEMENT_COST_IMPACT) ELSE 0 END) AS TOTAL_COST, SUM(CASE WHEN Isnumeric(ENTITLEMENT_PRICE_IMPACT) = 1 THEN CASE WHEN ENTITLEMENT_ID LIKE 'AGS_LAB_OPT%_P%' THEN CONVERT(DECIMAL(18,2),ENTITLEMENT_PRICE_IMPACT) ELSE 0 END ELSE 0 END) AS YEAR_2, SUM(CASE WHEN Isnumeric(ENTITLEMENT_PRICE_IMPACT) = 1 THEN CASE WHEN ENTITLEMENT_ID NOT LIKE 'AGS_LAB_OPT%_P%' THEN CONVERT(DECIMAL(18,2),ENTITLEMENT_PRICE_IMPACT) ELSE 0 END ELSE 0 END) AS YEAR_1 from (SELECT * FROM {PriceTemp}) IQ GROUP BY QUOTE_ID, EQUIPMENT_ID, SERVICE_ID
        # 									) SAQSCE_TEMP ON SAQSCE_TEMP.QUOTE_ID = SAQSCO.QUOTE_ID AND SAQSCE_TEMP.EQUIPMENT_ID = SAQSCO.EQUIPMENT_ID AND SAQSCE_TEMP.SERVICE_ID = SAQSCO.SERVICE_ID				
        # 								WHERE 
        # 									SAQSCO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCO.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQSCO.SERVICE_ID = 'Z0016' AND ISNULL(SAQSCO.INCLUDED,'') = 'CHAMBER' AND SAQSCA.INCLUDED = 1		
        # 								""".format(PriceTemp=price_temp, QuoteRecordId=self.contract_quote_record_id, RevisionRecordId=self.contract_quote_revision_record_id))	
        # ###Updating pricing picklist value in line item subtab A055S000P01-4578
        # Quote.GetCustomField('PRICING_PICKLIST').Content = 'Document Currency'		
        return True
    
    def _native_quote_edit(self):
        Quote = QuoteHelper.Edit(self.contract_quote_id)
        time.sleep(5)
        Quote.RefreshActions()
    
    def _native_quote_item_insert(self):
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
        Quote.GetCustomField('YEAR_3').Content = str(total_year_3) + " " + get_curr
        Quote.GetCustomField('TAX').Content = str(total_tax) + " " + get_curr
        Quote.GetCustomField('TOTAL_NET_VALUE').Content = str(total_extended_price) + " " + get_curr
        Quote.GetCustomField('MODEL_PRICE').Content = str(total_model_price) + " " + get_curr
        Quote.GetCustomField('BD_PRICE').Content = str(total_bd_price) + " " + get_curr
        #Quote.GetCustomField('DISCOUNT').Content = str(total_discount) + " %"
        Quote.Save()
        #assigning value to quote summary ends
        return True

    def _quote_items_insert(self):
        #Temp table for storing price and cost impact
        # price_temp = "SAQSCE_BKP_"+str(self.c4c_quote_id)
        # quote_services_obj = Sql.GetFirst("SELECT SERVICE_ID FROM SAQTSV (NOLOCK) WHERE QUOTE_RECORD_id = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID = 'Z0016'".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id))
        # if quote_services_obj:			
        # 	price_temp_drop = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(price_temp)+"'' ) BEGIN DROP TABLE "+str(price_temp)+" END  ' ")
        # 	SqlHelper.GetFirst("sp_executesql @T=N'declare @H int; Declare @val Varchar(MAX);DECLARE @XML XML; SELECT @val =  replace(replace(STUFF((SELECT ''''+FINAL from(select  REPLACE(entitlement_xml,''<QUOTE_ITEM_ENTITLEMENT>'',sml) AS FINAL FROM (select ''  <QUOTE_ITEM_ENTITLEMENT><QUOTE_ID>''+quote_id+''</QUOTE_ID><SERVICE_ID>''+service_id+''</SERVICE_ID><EQUIPMENT_ID>''+equipment_id+''</EQUIPMENT_ID>'' AS sml,replace(replace(replace(replace(entitlement_xml,''&'','';#38''),'''','';#39''),'' < '','' &lt; ''),'' > '','' &gt; '')  as entitlement_xml from SAQSCE(nolock) where quote_record_id=''"+str(self.contract_quote_record_id)+"'' )A )a FOR XML PATH ('''')), 1, 1, ''''),''&lt;'',''<''),''&gt;'',''>'')  SELECT @XML = CONVERT(XML,''<ROOT>''+@VAL+''</ROOT>'') exec sys.sp_xml_preparedocument @H output,@XML; select QUOTE_ID,EQUIPMENT_ID,SERVICE_ID,ENTITLEMENT_ID,ENTITLEMENT_COST_IMPACT,ENTITLEMENT_PRICE_IMPACT INTO "+str(price_temp)+"  from openxml(@H, ''ROOT/QUOTE_ITEM_ENTITLEMENT'', 0) with (QUOTE_ID VARCHAR(100) ''QUOTE_ID'',EQUIPMENT_ID VARCHAR(100) ''EQUIPMENT_ID'',ENTITLEMENT_ID VARCHAR(100) ''ENTITLEMENT_ID'',SERVICE_ID VARCHAR(100) ''SERVICE_ID'',ENTITLEMENT_COST_IMPACT VARCHAR(100) ''ENTITLEMENT_COST_IMPACT'',ENTITLEMENT_PRICE_IMPACT VARCHAR(100) ''ENTITLEMENT_PRICE_IMPACT'') ; exec sys.sp_xml_removedocument @H; '")
        
        # Non tool base quote item insert
        service_obj = Sql.GetFirst("SELECT SAQTSV.SERVICE_ID FROM SAQTSV (NOLOCK) JOIN MAMTRL (NOLOCK) ON MAMTRL.SAP_PART_NUMBER = SAQTSV.SERVICE_ID AND MAMTRL.SERVICE_TYPE = 'NON TOOL BASED' WHERE SAQTSV.QUOTE_RECORD_id = '{QuoteRecordId}' AND SAQTSV.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQTSV.SERVICE_ID = '{ServiceId}'".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id))
        if service_obj:
            item_where_string = "AND SAQSCE.SERVICE_ID = '{}'".format(service_obj.SERVICE_ID)
            # Insert SAQITM - Start
            self._quote_item_insert_process(where_string=item_where_string)
            # Insert SAQITM - End
            # Insert Quote Items Covered Object - Start
            item_line_where_string = "AND SAQSCO.SERVICE_ID = '{}'".format(service_obj.SERVICE_ID)
            if self.sale_type == 'TOOL RELOCATION':
                item_line_where_string += " AND SAQSCO.FABLOCATION_ID IS NOT NULL AND SAQSCO.FABLOCATION_ID != '' "
            join_string = "AND SAQITM.LINE_ITEM_ID = CAST(ISNULL(SAQSCE.ENTITLEMENT_GROUP_ID,'1.1') AS DECIMAL(5,1))"
            self._quote_item_lines_insert_process(where_string=item_line_where_string, join_string=join_string)
            # Insert Quote Items Covered Object - End
        
        # Tool base quote item insert
        service_obj = Sql.GetFirst("SELECT SAQTSV.SERVICE_ID FROM SAQTSV (NOLOCK) JOIN MAMTRL (NOLOCK) ON MAMTRL.SAP_PART_NUMBER = SAQTSV.SERVICE_ID AND MAMTRL.SERVICE_TYPE != 'NON TOOL BASED' WHERE SAQTSV.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQTSV.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQTSV.SERVICE_ID = '{ServiceId}'".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id))
        if service_obj:
            quote_item_obj = Sql.GetFirst("SELECT TOP 1 ISNULL(LINE_ITEM_ID, 0) AS LINE_ITEM_ID FROM SAQITM (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID LIKE '{ServiceId}%' ORDER BY LINE_ITEM_ID DESC".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id,ServiceId=service_obj.SERVICE_ID))
            item_where_string = "AND SAQSCE.SERVICE_ID = '{}'".format(service_obj.SERVICE_ID)
            # Insert SAQITM - Start
            self._quote_item_insert_process(where_string=item_where_string, max_quote_item_count=int(float(quote_item_obj.LINE_ITEM_ID)) if quote_item_obj else 0)
            # Insert SAQITM - End
            # Insert Quote Items Covered Object - Start
            item_line_where_string = "AND SAQSCO.SERVICE_ID = '{}'".format(service_obj.SERVICE_ID)
            if self.sale_type == 'TOOL RELOCATION':
                item_line_where_string += " AND SAQSCO.FABLOCATION_ID IS NOT NULL AND SAQSCO.FABLOCATION_ID != '' "
            self._quote_item_lines_insert_process(where_string=item_line_where_string, join_string='')
            # Insert Quote Items Covered Object - End

        self._native_quote_edit()
        self._native_quote_item_insert()

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
                            PRICING_STATUS = 'ACQUIRED',
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
        
        #Item Level Assembly Insert - Start
        Sql.RunQuery("""INSERT SAQICA (EQUIPMENT_ID,EQUIPMENT_RECORD_ID,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,GREENBOOK,GREENBOOK_RECORD_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,ASSEMBLY_DESCRIPTION,ASSEMBLY_ID,ASSEMBLY_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,QUOTE_ITEM_COVERED_OBJECT_ASSEMBLY_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED) 
            SELECT OQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_COVERED_OBJECT_ASSEMBLY_RECORD_ID, {UserId} as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM (
                SELECT IQ.* FROM (
                    SELECT 
                        DISTINCT SAQSCA.EQUIPMENT_ID,SAQSCA.EQUIPMENT_RECORD_ID,SAQTSE.QUOTE_ID,SAQTSE.QUOTE_RECORD_ID,SAQTSE.QTEREV_ID,SAQTSE.QTEREV_RECORD_ID,SAQTSE.SERVICE_DESCRIPTION,SAQTSE.SERVICE_ID,SAQTSE.SERVICE_RECORD_ID,SAQSCA.GREENBOOK,SAQSCA.GREENBOOK_RECORD_ID,SAQSCA.FABLOCATION_ID,SAQSCA.FABLOCATION_NAME,SAQSCA.FABLOCATION_RECORD_ID,SAQSCA.ASSEMBLY_DESCRIPTION,SAQSCA.ASSEMBLY_ID,SAQSCA.ASSEMBLY_RECORD_ID,SAQTSE.SALESORG_ID,SAQTSE.SALESORG_NAME,SAQTSE.SALESORG_RECORD_ID 
                    FROM SAQTSE (NOLOCK) 
                    JOIN SAQSCA (NOLOCK) ON SAQSCA.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID AND SAQSCA.SERVICE_RECORD_ID = SAQTSE.SERVICE_RECORD_ID AND SAQSCA.QTEREV_RECORD_ID = SAQTSE.QTEREV_RECORD_ID  
                    WHERE SAQTSE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQTSE.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQTSE.SERVICE_ID = '{ServiceId}'
                ) IQ 
                JOIN SAQSCE (NOLOCK) ON SAQSCE.SERVICE_RECORD_ID = IQ.SERVICE_RECORD_ID AND SAQSCE.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND SAQSCE.EQUIPMENT_ID = IQ.EQUIPMENT_ID AND SAQSCE.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND ISNULL(SAQSCE.CONFIGURATION_STATUS,'') = 'COMPLETE'
            )OQ""".format(UserId=self.user_id,  QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
        #Item Level Assembly Insert - End
        
        Sql.RunQuery("""INSERT SAQIAE (EQUIPMENT_ID,EQUIPMENT_RECORD_ID,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,CPS_CONFIGURATION_ID,CPS_MATCH_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,ASSEMBLY_ID,ASSEMBLY_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,ENTITLEMENT_XML,QUOTE_ITEM_ASSEMBLY_ENTITLEMENT_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED) 
            SELECT OQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_ASSEMBLY_ENTITLEMENT_RECORD_ID, {UserId} as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM (
                SELECT IQ.*,SAQSCE.ENTITLEMENT_XML FROM (
                    SELECT 
                        DISTINCT SAQSCA.EQUIPMENT_ID,SAQSCA.EQUIPMENT_RECORD_ID,SAQTSE.QUOTE_ID,SAQTSE.QUOTE_RECORD_ID,SAQTSE.QTEREV_ID,SAQTSE.QTEREV_RECORD_ID,SAQTSE.SERVICE_DESCRIPTION,SAQTSE.SERVICE_ID,SAQTSE.SERVICE_RECORD_ID,SAQTSE.CPS_CONFIGURATION_ID,SAQTSE.CPS_MATCH_ID,SAQSCA.FABLOCATION_ID,SAQSCA.FABLOCATION_NAME,SAQSCA.FABLOCATION_RECORD_ID,SAQSCA.ASSEMBLY_ID,SAQSCA.ASSEMBLY_RECORD_ID,SAQTSE.SALESORG_ID,SAQTSE.SALESORG_NAME,SAQTSE.SALESORG_RECORD_ID 
                    FROM SAQTSE (NOLOCK) 
                    JOIN SAQSCA (NOLOCK) ON SAQSCA.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID AND SAQSCA.SERVICE_RECORD_ID = SAQTSE.SERVICE_RECORD_ID AND SAQSCA.QTEREV_RECORD_ID = SAQTSE.QTEREV_RECORD_ID WHERE SAQTSE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQTSE.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQTSE.SERVICE_ID = '{ServiceId}'
                ) IQ 
                JOIN SAQSCE (NOLOCK) ON SAQSCE.SERVICE_RECORD_ID = IQ.SERVICE_RECORD_ID AND SAQSCE.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND SAQSCE.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND SAQSCE.EQUIPMENT_ID = IQ.EQUIPMENT_ID AND ISNULL(SAQSCE.CONFIGURATION_STATUS,'') = 'COMPLETE'
            )OQ""".format(UserId=self.user_id,  QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id))
        
        self._native_quote_item_update()
        
        # price_temp_drop = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(price_temp)+"'' ) BEGIN DROP TABLE "+str(price_temp)+" END  ' ")
        
        # Is Changed Information Notification - Start
        Sql.RunQuery("""UPDATE SAQSCE SET IS_CHANGED = 0 FROM SAQSCE (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID = '{ServiceId}'""".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id))
        # Is Changed Information Notification - End
        return True

    def _insert_quote_item_fab_location(self):
        SAQIEN_query = """INSERT SAQIEN (QUOTE_ITEM_COVERED_OBJECT_ENTITLEMENTS_RECORD_ID,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,QTESRVENT_RECORD_ID,SERVICE_RECORD_ID,SERVICE_ID,SERVICE_DESCRIPTION,SERIAL_NO,ENTITLEMENT_XML,CPS_CONFIGURATION_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,EQUIPMENT_LINE_ID,LINE_ITEM_ID,CPS_MATCH_ID,QTEITMCOB_RECORD_ID,EQUIPMENT_ID,EQUIPMENT_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,QTEITM_RECORD_ID) (select DISTINCT CONVERT(VARCHAR(4000), NEWID()) AS  QUOTE_ITEM_COVERED_OBJECT_ENTITLEMENTS_RECORD_ID, SAQSCE.QUOTE_ID,SAQSCE.QUOTE_RECORD_ID,SAQSCE.QTEREV_ID,SAQSCE.QTEREV_RECORD_ID,SAQSCE.QTESRVENT_RECORD_ID,SAQSCE.SERVICE_RECORD_ID,SAQSCE.SERVICE_ID,SAQSCE.SERVICE_DESCRIPTION,SAQICO.SERIAL_NO,SAQSCE.ENTITLEMENT_XML,SAQSCE.CPS_CONFIGURATION_ID,SAQSCE.FABLOCATION_ID,SAQSCE.FABLOCATION_NAME,SAQSCE.FABLOCATION_RECORD_ID,SAQICO.EQUIPMENT_LINE_ID,SAQICO.LINE_ITEM_ID,SAQSCE.CPS_MATCH_ID,SAQICO.QUOTE_ITEM_COVERED_OBJECT_RECORD_ID as QTEITMCOB_RECORD_ID,SAQICO.EQUIPMENT_ID,SAQICO.EQUIPMENT_RECORD_ID,SAQSCE.SALESORG_ID,SAQSCE.SALESORG_NAME,SAQSCE.SALESORG_RECORD_ID,SAQITM.QUOTE_ITEM_RECORD_ID FROM SAQSCE (NOLOCK) JOIN SAQICO ON SAQICO.QUOTE_RECORD_ID = SAQSCE.QUOTE_RECORD_ID AND SAQICO.SERVICE_ID = SAQSCE.SERVICE_ID AND SAQICO.QTEREV_RECORD_ID = SAQSCE.QTEREV_RECORD_ID AND SAQICO.FABLOCATION_ID = SAQSCE.FABLOCATION_ID AND SAQICO.GREENBOOK = SAQSCE.GREENBOOK AND SAQICO.EQUIPMENT_ID = SAQSCE.EQUIPMENT_ID JOIN SAQITM on SAQICO.QUOTE_RECORD_ID = SAQITM.QUOTE_RECORD_ID  where SAQSCE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCE.QTEREV_RECORD_ID = '{RevisionRecordId}' )""".format(
        QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id)
        Sql.RunQuery(SAQIEN_query)
        Sql.RunQuery(
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
                DOC_CURRENCY,
                DOCCURR_RECORD_ID,
                GLOBAL_CURRENCY,
                GLOBALCURRENCY_RECORD_ID,
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
                SAQICO.SALESORG_RECORD_ID,
                SAQICO.DOC_CURRENCY,
                SAQICO.DOCURR_RECORD_ID,
                SAQICO.GLOBAL_CURRENCY,
                SAQICO.GLOBAL_CURRENCY_RECORD_ID
                FROM SAQICO (NOLOCK)
                JOIN MAFBLC (NOLOCK) ON SAQICO.FABLOCATION_ID = MAFBLC.FAB_LOCATION_ID 
                JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQICO.QUOTE_RECORD_ID
                AND SAQTMT.QTEREV_RECORD_ID = SAQICO.QTEREV_RECORD_ID
                WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}'
                ) FB""".format(
                                QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id,
                                UserId=self.user_id,
                                UserName=self.user_name,
                                ServiceId=self.service_id
                            )
        )

    def _insert_quote_item_greenbook(self):		
        Sql.RunQuery(
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
                WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}' AND NOT EXISTS (SELECT GREENBOOK FROM SAQIGB WHERE QUOTE_RECORD_ID ='{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID = '{ServiceId}')
                ) FB""".format(
                                QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id,
                                UserId=self.user_id,
                                UserName=self.user_name,
                                ServiceId=self.service_id
                            )
            )

    def _quote_items_update(self):
        pass
    
    def _do_opertion(self):		
        if self.action_type == "INSERT_LINE_ITEMS":
            if self.quote_type == "ZWK1 - SPARES": ##User story 4432 starts..				
                self._insert_quote_item_forecast_parts() ##User story 4432 ends..
            else:
                self._quote_items_insert()
                #batch_group_record_id = str(Guid.NewGuid()).upper()
                self._insert_quote_item_fab_location()
                self._insert_quote_item_greenbook()		
        else:
            self._quote_items_update()	
        return True

try:
    where_condition_string = Param.WhereString
except:
    where_condition_string = ''

action_type = Param.ActionType
parameters = {}
parameters['action_type']=str(action_type)
if action_type == "UPDATE_LINE_ITEMS":
    if "QUOTE_RECORD_ID" in where_condition_string:
        pattern = re.compile(r'QUOTE_RECORD_ID\s*\=\s*\'([^>]*?)\'')
        result = re.search(pattern, where_condition_string).group(1)
        parameters['contract_quote_record_id']=str(result)
    if "QTEREV_RECORD_ID" in where_condition_string:
        pattern = re.compile(r'QTEREV_RECORD_ID\s*\=\s*\'([^>]*?)\'')
        result = re.search(pattern, where_condition_string).group(1)
        parameters['contract_quote_revision_record_id']=str(result)
    if "SERVICE_ID" in where_condition_string:
        pattern = re.compile(r'SERVICE_ID\s*\=\s*\'([^>]*?)\'')
        result = re.search(pattern, where_condition_string).group(1)
        parameters['service_id']=str(result)
    if "GREENBOOK" in where_condition_string:
        pattern = re.compile(r'GREENBOOK\s*\=\s*\'([^>]*?)\'')
        result = re.search(pattern, where_condition_string).group(1)
        parameters['greenbook_id']=str(result)
    if "FABLOCATION_ID" in where_condition_string:
        pattern = re.compile(r'FABLOCATION_ID\s*\=\s*\'([^>]*?)\'')
        result = re.search(pattern, where_condition_string).group(1)
        parameters['fablocation_id']=str(result)
    if "EQUIPMENT_ID" in where_condition_string:
        pattern = re.compile(r'EQUIPMENT_ID\s*\=\s*\'([^>]*?)\'')
        result = re.search(pattern, where_condition_string).group(1)
        parameters['equipment_id']=str(result)
else:
    parameters['contract_quote_record_id']=str(Param.ContractQuoteRecordId)
    parameters['contract_quote_revision_record_id']=str(Param.ContractQuoteRevisionRecordId)
    parameters['service_id']=str(Param.ServiceId)
    
contract_quote_item_obj = ContractQuoteItem(**parameters)
contract_quote_item_obj._do_opertion()
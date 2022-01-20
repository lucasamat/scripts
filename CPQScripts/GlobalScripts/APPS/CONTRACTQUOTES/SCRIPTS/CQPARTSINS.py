# =========================================================================================================================================
#   __script_name : CQPARTSINS.py
#   __script_description : THIS SCRIPT IS USED TO CONNECT WITH HANA TABLES TO PULL PARTS AND LOADED INTO CPQ.
#   __primary_author__ : SURIYANARAYANAN
#   __create_date :09-01-2022
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct
from SYDATABASE import SQL
import clr
import sys
import System.Net
import re

Sql = SQL()
ScriptExecutor = ScriptExecutor()
webclient = System.Net.WebClient()

class SyncFPMQuoteAndHanaDatabase:
    def __init__(self, Quote):
        self.quote = Quote
        self.response = self.sales_org_id = self.sales_recd_id = self.qt_rev_id = self.quote_id = self.contract_valid_from = self.contract_valid_to = ''
        self.quote_record_id = Quote.GetGlobal("contract_quote_record_id")
        self.quote_revision_id = Quote.GetGlobal("quote_revision_record_id")
        self.fetch_quotebasic_info()
        
    def pull_fpm_parts_hana(self):
        requestdata = "client_id=application&grant_type=client_credentials&username=16c3719c-d099-42d4-921c-765f4cee223a&password=mKv2~uXpeRD9SrD2DTW09Lk2GQ&scope=hanasafeaccess"
        webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/x-www-form-urlencoded"
        webclient.Headers[System.Net.HttpRequestHeader.Authorization] = "Basic MTZjMzcxOWMtZDA5OS00MmQ0LTkyMWMtNzY1ZjRjZWUyMjNhOm1LdjJ+dVhwZVJEOVNyRDJEVFcwOUxrMkdR"
        response = webclient.UploadString('https://oauth2.c-1404e87.kyma.shoot.live.k8s-hana.ondemand.com/oauth2/token',str(requestdata))
        response=response.replace("null",'""')
        response=eval(response)
        auth="Bearer"+' '+str(response['access_token'])
        requestdata = '{"query":"select * from SAFPLT"}'
        webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/json"
        webclient.Headers[System.Net.HttpRequestHeader.Authorization] = auth
        self.response = webclient.UploadString('https://hannaconnection.c-1404e87.kyma.shoot.live.k8s-hana.ondemand.com',str(requestdata))
    
    def pull_spareparts_hana(self):
        requestdata = "client_id=application&grant_type=client_credentials&username=ef66312d-bf20-416d-a902-4c646a554c10&password=Ieo.6c8hkYK9VtFe8HbgTqGev4&scope=fpmxcsafeaccess"
        webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/x-www-form-urlencoded"
        webclient.Headers[System.Net.HttpRequestHeader.Authorization] = "Basic ZWY2NjMxMmQtYmYyMC00MTZkLWE5MDItNGM2NDZhNTU0YzEwOkllby42Yzhoa1lLOVZ0RmU4SGJnVHFHZXY0"
        response = webclient.UploadString('https://oauth2.c-1404e87.kyma.shoot.live.k8s-hana.ondemand.com/oauth2/token',str(requestdata))
        response=response.replace("null",'""')
        response=eval(response)
        auth="Bearer"+' '+str(response['access_token'])
        requestdata = '{"soldtoParty":"10002301","shiptoparty":"10002428"}'
        webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/json"
        webclient.Headers[System.Net.HttpRequestHeader.Authorization] = auth
        self.response = webclient.UploadString('https://fpmxc.c-1404e87.kyma.shoot.live.k8s-hana.ondemand.com',str(requestdata))
    
    def insert_records_saqspt(self):
        if self.response:
            response = self.response
            response=response.replace("null",'""')
            response=response.replace("true",'"1"')
            response=response.replace("false",'"0"')
            response=response.replace("YES",'"1"')
            response=response.replace("NO",'"0"')
            response = re.sub(r'\[|\]','',response)
            saqspt_table_info = Sql.GetTable("SAQSPT")
            pattern = re.compile(r'(\{[^>]*?\})')
            saqspt_table_info={"QUOTE_SERVICE_PART_RECORD_ID": str(Guid.NewGuid()).upper(),"SALESORG_ID":self.sales_org_id,"SALESORG_RECORD_ID":self.sales_recd_id,"QTEREV_ID":self.qt_rev_id,"QUOTE_ID":self.quote_id,"VALID_FROM_DATE":self.contract_valid_from,"VALID_TO_DATE":self.contract_valid_to,"QTEREV_RECORD_ID":self.quote_revision_id,"QUOTE_RECORD_ID":self.quote_record_id,}
            for record in re.finditer(pattern, response):
                rec = re.sub(r'\{|\}','',record.group(1))
                saqspt_dict = {}
                for ele in rec.split('","'):
                    ele = re.sub(r'\"','',ele)
                    (key,value)=ele.split(':')
                    if key == 'FPM_PART_LIST_RECORD_ID':
                        continue
                    saqspt_dict[key]=value
                saqspt_table_info.AddRow(saqspt_dict)
                Sql.Upsert(saqspt_table_info)
    #SAQSPT INSERT
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
							WHERE TEMP_TABLE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND TEMP_TABLE.QTEREV_RECORD_ID = '{RevisionRecordId}' AND MAMTRL.PRODUCT_TYPE IS NULL AND MAMTRL.IS_SPARE_PART = 1 AND ISNULL(MAMSOP.MATERIALSTATUS_ID,'') <> '05') IQ
							""".format(
										TempTable=spare_parts_temp_table_name,
										ServiceId=self.tree_param,									
										QuoteRecordId=self.contract_quote_record_id,
										RevisionRecordId=self.contract_quote_revision_record_id,
										UserId=self.user_id
									)
			)

  
    def update_records_saqspt(self):

        update_customer_pn = """UPDATE SAQSPT SET SAQSPT.CUSTOMER_PART_NUMBER = M.CUSTOMER_PART_NUMBER FROM SAQSPT S INNER JOIN MAMSAC M ON S.PART_NUMBER= M.SAP_PART_NUMBER WHERE M.SALESORG_ID = '{sales_id}' and M.ACCOUNT_ID='{stp_acc_id}' AND S.QUOTE_RECORD_ID = '{quote_rec_id}' AND S.QTEREV_RECORD_ID = '{quote_revision_rec_id}'""".format(quote_rec_id = self.quote_record_id,sales_id = self.sales_org_id,stp_acc_id=str(account_info.get('SOLD TO')),quote_revision_rec_id =self.quote_revision_id)
        Sql.RunQuery(update_customer_pn)

        update_uom_recs = """UPDATE SAQSPT SET SAQSPT.BASEUOM_ID = M.UNIT_OF_MEASURE,SAQSPT.BASEUOM_RECORD_ID = M.UOM_RECORD_ID FROM SAQSPT S INNER JOIN MAMTRL M ON S.PART_NUMBER= M.SAP_PART_NUMBER WHERE   S.QUOTE_RECORD_ID = '{quote_rec_id}' AND S.QTEREV_RECORD_ID = '{quote_revision_rec_id}'""".format(quote_rec_id = self.quote_record_id,quote_revision_rec_id =self.quote_revision_id)
        Sql.RunQuery(update_uom_recs)

        update_salesuom_conv= """UPDATE SAQSPT SET SAQSPT.SALESUOM_CONVERSION_FACTOR = M.CONVERSION_QUANTITY FROM SAQSPT S INNER JOIN MAMUOC M ON S.PART_NUMBER= M.SAP_PART_NUMBER WHERE S.BASEUOM_ID=M.BASEUOM_ID AND  S.SALESUOM_ID=M.CONVERSIONUOM_ID AND S.QUOTE_RECORD_ID = '{quote_rec_id}' AND S.QTEREV_RECORD_ID = '{quote_revision_rec_id}'""".format(quote_rec_id = self.quote_record_id ,quote_revision_rec_id =self.quote_revision_id)
        Sql.RunQuery(update_salesuom_conv)

    def fetch_quotebasic_info(self):
        saqtrv_obj = Sql.GetFirst("select QUOTE_ID,SALESORG_ID,SALESORG_RECORD_ID,QTEREV_ID,CONTRACT_VALID_TO,CONTRACT_VALID_FROM from SAQTRV where QUOTE_RECORD_ID = '"+str(self.quote_record_id)+"' AND QUOTE_REVISION_RECORD_ID = '"+str(self.quote_revision_id)+"'")
        if saqtrv_obj:
            self.sales_org_id = saqtrv_obj.SALESORG_ID
            self.sales_recd_id = saqtrv_obj.SALESORG_RECORD_ID
            self.qt_rev_id = saqtrv_obj.QTEREV_ID
            self.quote_id = saqtrv_obj.QUOTE_ID
            self.contract_valid_from = saqtrv_obj.CONTRACT_VALID_FROM
            self.contract_valid_to = saqtrv_obj.CONTRACT_VALID_TO
        
fpm_obj = SyncFPMQuoteAndHanaDatabase(Quote)
fpm_obj.pull_spareparts_hana()
fpm_obj.insert_records_saqspt()
fpm_obj.update_records_saqspt()


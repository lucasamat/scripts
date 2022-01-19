# =========================================================================================================================================
#   __script_name : CQFPMHANAD.PY
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
        

    def update_records_saqspt(self):

        update_customer_pn = """UPDATE SAQSPT SET SAQSPT.CUSTOMER_PART_NUMBER = M.CUSTOMER_PART_NUMBER FROM SAQSPT S INNER JOIN MAMSAC M ON S.PART_NUMBER= M.SAP_PART_NUMBER WHERE M.SALESORG_ID = '{sales_id}' and M.ACCOUNT_ID='{stp_acc_id}' AND S.QUOTE_RECORD_ID = '{quote_rec_id}' AND S.QTEREV_RECORD_ID = '{quote_revision_rec_id}'""".format(quote_rec_id = contract_quote_record_id ,sales_id = sales_id,stp_acc_id=str(account_info.get('SOLD TO')),quote_revision_rec_id =quote_revision_record_id)
		Sql.RunQuery(update_customer_pn)

		update_uom_recs = """UPDATE SAQSPT SET SAQSPT.BASEUOM_ID = M.UNIT_OF_MEASURE,SAQSPT.BASEUOM_RECORD_ID = M.UOM_RECORD_ID FROM SAQSPT S INNER JOIN MAMTRL M ON S.PART_NUMBER= M.SAP_PART_NUMBER WHERE   S.QUOTE_RECORD_ID = '{quote_rec_id}' AND S.QTEREV_RECORD_ID = '{quote_revision_rec_id}'""".format(quote_rec_id = contract_quote_record_id ,quote_revision_rec_id =quote_revision_record_id)
		Sql.RunQuery(update_uom_recs)

		update_sales_uom = """UPDATE SAQSPT SET SAQSPT.SALESUOM_CONVERSION_FACTOR = M.CONVERSION_QUANTITY FROM SAQSPT S INNER JOIN MAMSAC M ON S.PART_NUMBER= M.SAP_PART_NUMBER WHERE S.QUOTE_RECORD_ID = '{quote_rec_id}' AND S.QTEREV_RECORD_ID = '{quote_revision_rec_id}'""".format(quote_rec_id = contract_quote_record_id ,quote_revision_rec_id =quote_revision_record_id)
		Sql.RunQuery(update_sales_uom)

		


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
fpm_obj.pull_fpm_parts_hana()
fpm_obj.insert_records_saqspt()
fpm_obj.update_records_saqspt()


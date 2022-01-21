# =========================================================================================================================================
#   __script_name : CQPARTSINS.py
#   __script_description : THIS SCRIPT IS USED TO CONNECT WITH HANA TABLES TO PULL PARTS AND LOADED INTO CPQ.
#   __primary_author__ : Suriyanarayanan Pazhani
#   __create_date :09-01-2022
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
#from logging import exception
import Webcom.Configurator.Scripting.Test.TestProduct
from SYDATABASE import SQL
import clr
import sys
import System.Net
import re
import datetime

Sql = SQL()
webclient = System.Net.WebClient()

class SyncFPMQuoteAndHanaDatabase:
    def __init__(self, Quote):
        self.quote = Quote
        self.response = self.sales_org_id = self.sales_recd_id = self.qt_rev_id = self.quote_id = self.contract_valid_from = self.contract_valid_to = self.columns= self.records= self.cvf = self.cvt= ''
        self.quote_record_id = Quote.GetGlobal("contract_quote_record_id")
        self.quote_revision_id = Quote.GetGlobal("quote_revision_record_id")
        self.datetime_value = datetime.datetime.now()
        self.account_info = {}
        self.tree_param = 'Z0108'
        self.fetch_quotebasic_info()
        cv=str(self.contract_valid_from)
        (cm,cd,cy)=re.sub(r'\s+([^>]*?)$','',cv).split('/')
        cd = '0'+str(cd) if len(cd)==1 else cd
        cm = '0'+str(cm) if len(cm)==1 else cm        
        self.cvf = cy+cm+cd
        cv=str(self.contract_valid_to)
        (cm,cd,cy)=re.sub(r'\s+([^>]*?)$','',cv).split('/')
        cd = '0'+str(cd) if len(cd)==1 else cd
        cm = '0'+str(cm) if len(cm)==1 else cm        
        self.cvt = cy+cm+cd
        
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
    
    def pull_requestto_hana(self):
        requestdata = "client_id=application&grant_type=client_credentials&username=ef66312d-bf20-416d-a902-4c646a554c10&password=Ieo.6c8hkYK9VtFe8HbgTqGev4&scope=fpmxcsafeaccess"
        webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/x-www-form-urlencoded"
        webclient.Headers[System.Net.HttpRequestHeader.Authorization] = "Basic ZWY2NjMxMmQtYmYyMC00MTZkLWE5MDItNGM2NDZhNTU0YzEwOkllby42Yzhoa1lLOVZ0RmU4SGJnVHFHZXY0"
        response = webclient.UploadString('https://oauth2.c-1404e87.kyma.shoot.live.k8s-hana.ondemand.com/oauth2/token',str(requestdata))
        response=response.replace("null",'""')
        response=eval(response)
        auth="Bearer"+' '+str(response['access_token'])
        requestdata = '{"soldtoParty":"'+str(self.account_info['SOLD TO'])+'","shiptoparty":"'+str(self.account_info['SHIP TO'])+'","salesOrg":"'+str(self.sales_org_id)+'","priceList":"","priceGroup":"","validTo":"'+str(self.cvt)+'","validFrom":"'+str(self.cvf)+'",	"participatewith6k":"Yes","customParticipaton":"Yes"}'
        webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/json"
        webclient.Headers[System.Net.HttpRequestHeader.Authorization] = auth
        self.response = webclient.UploadString('https://fpmxc.c-1404e87.kyma.shoot.live.k8s-hana.ondemand.com',str(requestdata))
    
    def add_parts_requestto_hana(self,part_ids):
        requestdata = "client_id=application&grant_type=client_credentials&username=ef66312d-bf20-416d-a902-4c646a554c10&password=Ieo.6c8hkYK9VtFe8HbgTqGev4&scope=fpmxcsafeaccess"
        webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/x-www-form-urlencoded"
        webclient.Headers[System.Net.HttpRequestHeader.Authorization] = "Basic ZWY2NjMxMmQtYmYyMC00MTZkLWE5MDItNGM2NDZhNTU0YzEwOkllby42Yzhoa1lLOVZ0RmU4SGJnVHFHZXY0"
        response = webclient.UploadString('https://oauth2.c-1404e87.kyma.shoot.live.k8s-hana.ondemand.com/oauth2/token',str(requestdata))
        response=response.replace("null",'""')
        response=eval(response)
        auth="Bearer"+' '+str(response['access_token'])
        requestdata = '{"soldtoParty":"'+str(self.account_info['SOLD TO'])+'","shiptoparty":"'+str(self.account_info['SHIP TO'])+'","salesOrg":"'+str(self.sales_org_id)+'","priceList":"","priceGroup":"","validTo":"20220616","validFrom":"20210518",	"participatewith6k":"Yes","customParticipaton":"Yes","partNumber":'+str(part_ids)+'}'
        webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/json"
        webclient.Headers[System.Net.HttpRequestHeader.Authorization] = auth
        self.response = webclient.UploadString('https://fpmxc.c-1404e87.kyma.shoot.live.k8s-hana.ondemand.com',str(requestdata))
        fpm_obj.prepare_backup_table()
        fpm_obj._insert_spare_parts()
        fpm_obj.update_records_saqspt()

    
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

    def _insert_spare_parts(self):
        datetime_string = self.datetime_value.strftime("%d%m%Y%H%M%S")
        spare_parts_temp_table_name = "SAQSPT_BKP_{}_{}".format(self.quote_record_id, datetime_string)
        Trace.Write(spare_parts_temp_table_name)		
        try:
            spare_parts_temp_table_drop = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(spare_parts_temp_table_name)+"'' ) BEGIN DROP TABLE "+str(spare_parts_temp_table_name)+" END  ' ")			
            spare_parts_temp_table_bkp = SqlHelper.GetFirst("sp_executesql @T=N'SELECT "+str(self.columns)+" INTO "+str(spare_parts_temp_table_name)+" FROM (SELECT DISTINCT "+str(self.columns)+" FROM (VALUES "+str(self.records)+") AS TEMP("+str(self.columns)+")) OQ ' ")
            spare_parts_existing_records_delete = SqlHelper.GetFirst("sp_executesql @T=N'DELETE FROM SAQSPT WHERE QUOTE_RECORD_ID = ''"+str(self.quote_record_id)+"'' AND QTEREV_RECORD_ID = ''"+str(self.quote_revision_id)+"'' ' ")
            Sql.RunQuery("""
                            INSERT SAQSPT (QUOTE_SERVICE_PART_RECORD_ID, BASEUOM_ID, BASEUOM_RECORD_ID, CUSTOMER_PART_NUMBER, CUSTOMER_PART_NUMBER_RECORD_ID, DELIVERY_MODE, EXTENDED_UNIT_PRICE, PART_DESCRIPTION, PART_NUMBER, PART_RECORD_ID, PRDQTYCON_RECORD_ID, CUSTOMER_ANNUAL_QUANTITY, QUOTE_ID, QUOTE_NAME, QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,SALESORG_ID, SALESORG_RECORD_ID, SALESUOM_CONVERSION_FACTOR, SALESUOM_ID, SALESUOM_RECORD_ID, SCHEDULE_MODE, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, UNIT_PRICE, MATPRIGRP_ID, MATPRIGRP_RECORD_ID, DELIVERY_INTERVAL, VALID_FROM_DATE, VALID_TO_DATE,PAR_SERVICE_DESCRIPTION,PAR_SERVICE_ID,PAR_SERVICE_RECORD_ID, RETURN_TYPE, ODCC_FLAG, PAR_PART_NUMBER, EXCHANGE_ELIGIBLE, CUSTOMER_PARTICIPATE, CUSTOMER_ACCEPT_PART,STPACCOUNT_ID, SHPACCOUNT_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED)
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
                                RETURN_TYPE,
                                ODCC_FLAG,
                                PAR_PART_NUMBER,
                                EXCHANGE_ELIGIBLE,
                                CUSTOMER_PARTICIPATE,
                                CUSTOMER_ACCEPT_PART,
                                STPACCOUNT_ID,
                                SHPACCOUNT_ID
                                {UserId} as CPQTABLEENTRYADDEDBY, 
                                GETDATE() as CPQTABLEENTRYDATEADDED
                            FROM (
                            SELECT 
                                DISTINCT
                                MAMTRL.UNIT_OF_MEASURE as BASEUOM_ID,
                                MAMTRL.UOM_RECORD_ID as BASEUOM_RECORD_ID,
                                CASE WHEN TEMP_TABLE.CHILD_PART_NUMBER!='' THEN TEMP_TABLE.CHILD_PART_NUMBER ELSE MAMTRL.SAP_PART_NUMBER END AS CUSTOMER_PART_NUMBER,
                                MAMTRL.MATERIAL_RECORD_ID as CUSTOMER_PART_NUMBER_RECORD_ID,
                                'ONSITE' as DELIVERY_MODE,
                                0.00 as EXTENDED_UNIT_PRICE,
                                MAMTRL.SAP_DESCRIPTION as PART_DESCRIPTION,
                                CASE WHEN TEMP_TABLE.CHILD_PART_NUMBER!='' THEN TEMP_TABLE.CHILD_PART_NUMBER ELSE MAMTRL.SAP_PART_NUMBER END AS PART_NUMBER,
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
                                SAQTSV.PAR_SERVICE_RECORD_ID as PAR_SERVICE_RECORD_ID,
                                TEMP_TABLE.RETURN_TYPE AS RETURN_TYPE,
                                CASE WHEN TEMP_TABLE.ODCC_FLAG='X' THEN 'True' ELSE 'False' END AS ODCC_FLAG,
                                CASE WHEN TEMP_TABLE.CHILD_PART_NUMBER='' THEN '' ELSE TEMP_TABLE.PARENT_PART_NUMBER END AS PAR_PART_NUMBER,
                                TEMP_TABLE.Material_Eligibility AS EXCHANGE_ELIGIBLE,
                                'True' as CUSTOMER_PARTICIPATE,
                                'True' as CUSTOMER_ACCEPT_PART,
                                {'sold_to'} as STPACCOUNT_ID,
                                {'ship_to'} as SHPACCOUNT_ID
                            FROM {TempTable} TEMP_TABLE(NOLOCK)
                            JOIN MAMTRL (NOLOCK) ON MAMTRL.SAP_PART_NUMBER = TEMP_TABLE.PARENT_PART_NUMBER
                            JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = TEMP_TABLE.QUOTE_RECORD_ID
                            JOIN SAQTSV (NOLOCK) ON SAQTSV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SAQTSV.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID AND SAQTSV.SERVICE_ID = '{ServiceId}'
                            JOIN MAMSOP (NOLOCK) ON MAMSOP.MATERIAL_RECORD_ID = MAMTRL.MATERIAL_RECORD_ID AND MAMSOP.SALESORG_RECORD_ID = SAQTSV.SALESORG_RECORD_ID
                            WHERE TEMP_TABLE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND TEMP_TABLE.QTEREV_RECORD_ID = '{RevisionRecordId}' AND MAMTRL.PRODUCT_TYPE IS NULL AND MAMTRL.IS_SPARE_PART = 1 AND ISNULL(MAMSOP.MATERIALSTATUS_ID,'') <> '05') IQ
                            """.format(
                                        TempTable=spare_parts_temp_table_name,
                                        ServiceId=self.tree_param,									
                                        QuoteRecordId=self.quote_record_id,
                                        RevisionRecordId=self.quote_revision_id,
                                        UserId=user.user_id,
                                        sold_to=self.account_info['SOLD TO'],
                                        ship_to=self.account_info['SHIP TO']
                                    )
            )
            spare_parts_temp_table_drop = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(spare_parts_temp_table_name)+"'' ) BEGIN DROP TABLE "+str(spare_parts_temp_table_name)+" END  ' ")
        except Exception:
            spare_parts_temp_table_drop = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(spare_parts_temp_table_name)+"'' ) BEGIN DROP TABLE "+str(spare_parts_temp_table_name)+" END  ' ")
            Trace.Write("Exception in Query")
        
    def update_records_saqspt(self):
        update_customer_pn = """UPDATE SAQSPT SET SAQSPT.CUSTOMER_PART_NUMBER = M.CUSTOMER_PART_NUMBER FROM SAQSPT S INNER JOIN MAMSAC M ON S.PART_NUMBER= M.SAP_PART_NUMBER WHERE M.SALESORG_ID = '{sales_id}' and M.ACCOUNT_ID='{stp_acc_id}' AND S.QUOTE_RECORD_ID = '{quote_rec_id}' AND S.QTEREV_RECORD_ID = '{quote_revision_rec_id}'""".format(quote_rec_id = self.quote_record_id,sales_id = self.sales_org_id,stp_acc_id=str(self.account_info['SOLD TO']),quote_revision_rec_id =self.quote_revision_id)
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
        get_party_role = Sql.GetList("SELECT PARTY_ID,PARTY_ROLE FROM SAQTIP(NOLOCK) WHERE QUOTE_RECORD_ID = '"+str(self.quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_id)+"' and PARTY_ROLE in ('SOLD TO','SHIP TO')")
        for keyobj in get_party_role:
            self.account_info[keyobj.PARTY_ROLE] = keyobj.PARTY_ID
								
    def prepare_backup_table(self):
        if self.response:
            response = self.response
            response=response.replace("null",'""')
            response=response.replace("true",'1')
            response=response.replace("false",'0')
            response=response.replace("YES",'1')
            response=response.replace("NO",'0')
            response = re.sub(r'\[|\]','',response)
            pattern = re.compile(r'(\{[^>]*?\})')
            pattern2 = re.compile(r'\"([^>]*?)\"\:(\"[^>]*?\")')
            self.columns = '(QUOTE_RECORD_ID,QTEREV_RECORD_ID'
            value  = """({},{}""".format(self.quote_record_id,self.quote_revision_id)
            col_flag = 0
            for record in re.finditer(pattern, response):
                rec = re.sub(r'\{|\}','',record.group(1))
                temp_value = value
                for ele in re.finditer(pattern2,rec):
                    if col_flag == 0:
                        self.columns +=','+ele.group(1)
                    temp_value +=','+ele.group(2) if ele.group(2) !='' else None
                if col_flag == 0:
                    self.columns +=')'
                temp_value +=')'
                if self.records == '':
                    self.records = temp_value
                else:
                    self.records += ', '+temp_value
                temp_value =''
                col_flag=1
    
fpm_obj = SyncFPMQuoteAndHanaDatabase(Quote)
fpm_obj.pull_requestto_hana()
fpm_obj.prepare_backup_table()
fpm_obj._insert_spare_parts()
fpm_obj.update_records_saqspt()


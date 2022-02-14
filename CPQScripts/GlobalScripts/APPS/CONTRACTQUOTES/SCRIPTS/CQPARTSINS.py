# =========================================================================================================================================
#   __script_name : CQPARTSINS.py
#   __script_description : THIS SCRIPT IS USED TO CONNECT WITH HANA TABLES TO PULL PARTS AND LOADED INTO CPQ.
#   __primary_author__ : Suriyanarayanan Pazhani
#   __create_date :09-01-2022
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct
from SYDATABASE import SQL
import clr
import sys
import System.Net
import re
import datetime
import time
import CQPARTIFLW
from datetime import timedelta , date
Sql = SQL()
webclient = System.Net.WebClient()

class SyncFPMQuoteAndHanaDatabase:
    def __init__(self):
        self.response = self.arp_carp_response = self.sales_org_id = self.sales_recd_id = self.qt_rev_id = self.quote_id = self.contract_valid_from = self.contract_valid_to = self.columns= self.records= self.cvf = self.cvt = self.service_id = self.service_desc = self.service_record_id = ''
        self.datetime_value = datetime.datetime.now()
        self.account_info = {}
        self.part_numbers = []
        try:
            self.quote_id = str(Param.CPQ_Columns["QuoteID"])
        except Exception:
            Log.Info("@@@Self Quote ID is Missing@@@")
        try:
            self.response = Param.CPQ_Columns["Response"]["root"]["KYMA_DATA"]["SAFPLT"]
        except Exception:
            Log.Info("@@@Self Response is Missing@@@")
             
    def _insert_spare_parts(self):
        datetime_string = self.datetime_value.strftime("%d%m%Y%H%M%S")
        uid=str(Guid.NewGuid()).upper()
        uids=uid.split('-')
        spare_parts_temp_table_name = "SAQSPT_BKP_{}_{}_{}".format(self.quote_record_id, datetime_string,str(uids[0]))
        spare_parts_temp_table_name = re.sub(r'-','_',spare_parts_temp_table_name)
        self.columns = re.sub(r'\"|\{','',self.columns)
        self.columns = re.sub(r',,',',',self.columns)
        Log.Info("Columns--->"+str(self.columns))
        Log.Info("Values---->"+str(self.records))
        Log.Info("TempTableName--->"+str(spare_parts_temp_table_name))
        Trace.Write("Spare_part_insert")
        try:
            spare_parts_temp_table_drop = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(spare_parts_temp_table_name)+"'' ) BEGIN DROP TABLE "+str(spare_parts_temp_table_name)+" END  ' ")			
            spare_parts_temp_table_bkp = SqlHelper.GetFirst("sp_executesql @T=N'SELECT "+str(self.columns)+" INTO "+str(spare_parts_temp_table_name)+" FROM (SELECT DISTINCT "+str(self.columns)+" FROM (VALUES "+str(self.records)+") AS TEMP("+str(self.columns)+")) OQ ' ")
            #spare_parts_existing_records_delete = SqlHelper.GetFirst("sp_executesql @T=N'DELETE FROM SAQSPT WHERE QUOTE_RECORD_ID = ''"+str(self.quote_record_id)+"'' AND QTEREV_RECORD_ID = ''"+str(self.quote_revision_id)+"'' ' ")
            temp_table_count = SqlHelper.GetFirst("SELECT count(*) as CNT FROM {}".format(str(spare_parts_temp_table_name)))
            Log.Info("TempTablecount--->"+str(temp_table_count.CNT))
            Sql.RunQuery("""
                            INSERT SAQSPT (QUOTE_SERVICE_PART_RECORD_ID, BASEUOM_ID, BASEUOM_RECORD_ID, CUSTOMER_PART_NUMBER, CUSTOMER_PART_NUMBER_RECORD_ID, DELIVERY_MODE, EXTENDED_UNIT_PRICE, PART_DESCRIPTION, PART_NUMBER, PART_RECORD_ID, PRDQTYCON_RECORD_ID, CUSTOMER_ANNUAL_QUANTITY, QUOTE_ID, QUOTE_NAME, QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,SALESORG_ID, SALESORG_RECORD_ID, SALESUOM_CONVERSION_FACTOR, SALESUOM_ID, SALESUOM_RECORD_ID, SCHEDULE_MODE, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, UNIT_PRICE, MATPRIGRP_ID, MATPRIGRP_RECORD_ID, DELIVERY_INTERVAL, VALID_FROM_DATE, VALID_TO_DATE,PAR_SERVICE_DESCRIPTION,PAR_SERVICE_ID,PAR_SERVICE_RECORD_ID, RETURN_TYPE, ODCC_FLAG, PAR_PART_NUMBER, EXCHANGE_ELIGIBLE, CUSTOMER_ELIGIBLE,CUSTOMER_PARTICIPATE, CUSTOMER_ACCEPT_PART,STPACCOUNT_ID, SHPACCOUNT_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED)
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
                                CUSTOMER_ELIGIBLE,
                                CUSTOMER_PARTICIPATE,
                                CUSTOMER_ACCEPT_PART,
                                STPACCOUNT_ID,
                                SHPACCOUNT_ID,
                                {UserId} as CPQTABLEENTRYADDEDBY, 
                                GETDATE() as CPQTABLEENTRYDATEADDED
                            FROM (
                            SELECT 
                                DISTINCT
                                MAMTRL.UNIT_OF_MEASURE as BASEUOM_ID,
                                MAMTRL.UOM_RECORD_ID as BASEUOM_RECORD_ID,
                                CASE WHEN TEMP_TABLE.CHILD_PART_NUMBER!='' THEN TEMP_TABLE.CHILD_PART_NUMBER ELSE MAMTRL.SAP_PART_NUMBER END AS CUSTOMER_PART_NUMBER,
                                MAMTRL.MATERIAL_RECORD_ID as CUSTOMER_PART_NUMBER_RECORD_ID,
                                CASE WHEN SAQTSV.SERVICE_ID='Z0110' THEN NULL ELSE 'OFFSITE' END AS DELIVERY_MODE,
                                0.00 as EXTENDED_UNIT_PRICE,
                                MAMTRL.SAP_DESCRIPTION as PART_DESCRIPTION,
                                CASE WHEN TEMP_TABLE.CHILD_PART_NUMBER!='' THEN TEMP_TABLE.CHILD_PART_NUMBER ELSE MAMTRL.SAP_PART_NUMBER END AS PART_NUMBER,
                                MAMTRL.MATERIAL_RECORD_ID as PART_RECORD_ID,
                                '' as PRDQTYCON_RECORD_ID,
                                CASE WHEN TEMP_TABLE.CUSTOMER_ANNUAL_QUANTITY='' THEN NULL ELSE TEMP_TABLE.CUSTOMER_ANNUAL_QUANTITY END as QUANTITY,
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
                                CASE WHEN SAQTSV.SERVICE_ID='Z0110' THEN NULL ELSE 'UNSCHEDULED' END AS SCHEDULE_MODE,
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
                                CASE WHEN TEMP_TABLE.CHILD_PART_NUMBER='' THEN null ELSE TEMP_TABLE.PARENT_PART_NUMBER END AS PAR_PART_NUMBER,
                                TEMP_TABLE.Material_Eligibility AS EXCHANGE_ELIGIBLE,
                                CASE WHEN TEMP_TABLE.Customer_Eligibility='X' THEN 'True' ELSE 'False' END AS CUSTOMER_ELIGIBLE,
                                'True' as CUSTOMER_PARTICIPATE,
                                'True' as CUSTOMER_ACCEPT_PART,
                                '{sold_to}' as STPACCOUNT_ID,
                                '{ship_to}' as SHPACCOUNT_ID
                            FROM {TempTable} TEMP_TABLE(NOLOCK)
                            JOIN MAMTRL (NOLOCK) ON MAMTRL.SAP_PART_NUMBER = TEMP_TABLE.PARENT_PART_NUMBER
                            JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = TEMP_TABLE.QUOTE_RECORD_ID
                            JOIN SAQTSV (NOLOCK) ON SAQTSV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SAQTSV.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID AND SAQTSV.SERVICE_ID = '{ServiceId}'
                            JOIN MAMSOP (NOLOCK) ON MAMSOP.MATERIAL_RECORD_ID = MAMTRL.MATERIAL_RECORD_ID AND MAMSOP.SALESORG_RECORD_ID = SAQTSV.SALESORG_RECORD_ID
                            WHERE TEMP_TABLE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND TEMP_TABLE.QTEREV_RECORD_ID = '{RevisionRecordId}' AND MAMTRL.PRODUCT_TYPE IS NULL AND MAMTRL.IS_SPARE_PART = 1 AND ISNULL(MAMSOP.MATERIALSTATUS_ID,'') <> '05' AND NOT EXISTS (SELECT CpqTableEntryId FROM SAQSPT (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}')) IQ
                            """.format(
                                        TempTable=spare_parts_temp_table_name,
                                        ServiceId=self.service_id,									
                                        QuoteRecordId=self.quote_record_id,
                                        RevisionRecordId=self.quote_revision_id,
                                        UserId=User.Id,
                                        sold_to=self.account_info['SOLD TO'],
                                        ship_to=self.account_info['SHIP TO']
                                    )
            )
            spare_parts_temp_table_drop = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(spare_parts_temp_table_name)+"'' ) BEGIN DROP TABLE "+str(spare_parts_temp_table_name)+" END  ' ")
        except Exception:
            spare_parts_temp_table_drop = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(spare_parts_temp_table_name)+"'' ) BEGIN DROP TABLE "+str(spare_parts_temp_table_name)+" END  ' ")
            Log.Info("Exception in Query insertion in SAQSPT")
        
    def update_records_saqspt(self):
        update_customer_pn = """UPDATE SAQSPT SET SAQSPT.CUSTOMER_PART_NUMBER = M.CUSTOMER_PART_NUMBER FROM SAQSPT S INNER JOIN MAMSAC M ON S.PART_NUMBER= M.SAP_PART_NUMBER WHERE M.SALESORG_ID = '{sales_id}' and M.ACCOUNT_ID='{stp_acc_id}' AND S.QUOTE_RECORD_ID = '{quote_rec_id}' AND S.QTEREV_RECORD_ID = '{quote_revision_rec_id}' AND S.EXCHANGE_ELIGIBLE='True' AND S.ODCC_FLAG='True'""".format(quote_rec_id = self.quote_record_id,sales_id = self.sales_org_id,stp_acc_id=str(self.account_info['SOLD TO']),quote_revision_rec_id =self.quote_revision_id)
        Sql.RunQuery(update_customer_pn)

        update_uom_recs = """UPDATE SAQSPT SET SAQSPT.BASEUOM_ID = M.UNIT_OF_MEASURE,SAQSPT.BASEUOM_RECORD_ID = M.UOM_RECORD_ID FROM SAQSPT S INNER JOIN MAMTRL M ON S.PART_NUMBER= M.SAP_PART_NUMBER WHERE   S.QUOTE_RECORD_ID = '{quote_rec_id}' AND S.QTEREV_RECORD_ID = '{quote_revision_rec_id}'""".format(quote_rec_id = self.quote_record_id,quote_revision_rec_id =self.quote_revision_id)
        Sql.RunQuery(update_uom_recs)

        update_salesuom_conv= """UPDATE SAQSPT SET SAQSPT.SALESUOM_CONVERSION_FACTOR = M.CONVERSION_QUANTITY FROM SAQSPT S INNER JOIN MAMUOC M ON S.PART_NUMBER= M.SAP_PART_NUMBER WHERE S.BASEUOM_ID=M.BASEUOM_ID AND  S.SALESUOM_ID=M.CONVERSIONUOM_ID AND S.QUOTE_RECORD_ID = '{quote_rec_id}' AND S.QTEREV_RECORD_ID = '{quote_revision_rec_id}'""".format(quote_rec_id = self.quote_record_id ,quote_revision_rec_id =self.quote_revision_id)
        Sql.RunQuery(update_salesuom_conv)

    def insert_delivery_schedule(self):
        if str(self.service_id) == "Z0108":
            contract_start_date = self.contract_valid_from
            contract_end_date = self.contract_valid_to
            start_date = datetime.datetime.strptime(UserPersonalizationHelper.ToUserFormat(contract_start_date), '%m/%d/%Y')
            end_date = datetime.datetime.strptime(UserPersonalizationHelper.ToUserFormat(contract_end_date), '%m/%d/%Y')
            diff1 = end_date - start_date
            get_totalweeks,remainder = divmod(diff1.days,7)
            for index in range(0, get_totalweeks):
                delivery_week_date="DATEADD(week, {weeks}, '{DeliveryDate}')".format(weeks=index, DeliveryDate=start_date.strftime('%m/%d/%Y'))
                
                getschedule_details = Sql.RunQuery("INSERT SAQSPD  (QUOTE_REV_PO_PART_DELIVERY_SCHEDULES_RECORD_ID,DELIVERY_SCHED_CAT,DELIVERY_SCHED_DATE,PART_DESCRIPTION,PART_RECORD_ID,PART_NUMBER,QUANTITY,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_ID,QTEREVSPT_RECORD_ID,QTEREV_RECORD_ID,CUSTOMER_ANNUAL_QUANTITY,DELIVERY_MODE,SCHEDULED_MODE,MATERIALSTATUS_ID,MATERIALSTATUS_RECORD_ID,SALESUOM_ID,SALESUOM_RECORD_ID,MATPRIGRP_ID,UOM_ID,DELIVERY_SCHEDULE,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID)  select CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REV_PO_PART_DELIVERY_SCHEDULES_RECORD_ID,null as DELIVERY_SCHED_CAT,{delivery_date} as DELIVERY_SCHED_DATE,PART_DESCRIPTION,PART_RECORD_ID,PART_NUMBER, 0 as QUANTITY,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_ID,QUOTE_SERVICE_PART_RECORD_ID as QTEREVSPT_RECORD_ID,QTEREV_RECORD_ID,CUSTOMER_ANNUAL_QUANTITY,DELIVERY_MODE,SCHEDULE_MODE as SCHEDULED_MODE,MATERIALSTATUS_ID,MATERIALSTATUS_RECORD_ID,SALESUOM_ID,SALESUOM_RECORD_ID,MATPRIGRP_ID,BASEUOM_ID as UOM_ID,'{deli_sch}' as DELIVERY_SCHEDULE,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID FROM SAQSPT where SCHEDULE_MODE= 'SCHEDULED' and DELIVERY_MODE = 'OFFSITE' and QUOTE_RECORD_ID = '{contract_rec_id}' AND QTEREV_RECORD_ID = '{qt_rev_id}' and CUSTOMER_ANNUAL_QUANTITY >0".format(delivery_date =delivery_week_date,contract_rec_id= self.quote_record_id,qt_rev_id = self.quote_revision_id,deli_sch ='WEEKLY'))

    def fetch_quotebasic_info(self):
        saqtmt_obj = Sql.GetFirst("SELECT CONTRACT_VALID_FROM,CONTRACT_VALID_TO FROM SAQTMT (NOLOCK) WHERE  QUOTE_ID = '{}'".format(self.quote_id))
        if saqtmt_obj:
            self.contract_valid_from = saqtmt_obj.CONTRACT_VALID_FROM
            self.contract_valid_to = saqtmt_obj.CONTRACT_VALID_TO
                
        saqtrv_obj = Sql.GetFirst("select QUOTE_RECORD_ID,QUOTE_REVISION_RECORD_ID,SALESORG_ID,SALESORG_RECORD_ID,QTEREV_ID from SAQTRV where QUOTE_ID = '"+str(self.quote_id)+"'")
        if saqtrv_obj:
            self.sales_org_id = saqtrv_obj.SALESORG_ID
            self.sales_recd_id = saqtrv_obj.SALESORG_RECORD_ID
            self.qt_rev_id = saqtrv_obj.QTEREV_ID
            self.quote_revision_id = saqtrv_obj.QUOTE_REVISION_RECORD_ID
            self.quote_record_id = saqtrv_obj.QUOTE_RECORD_ID
            
        get_party_role = Sql.GetList("SELECT PARTY_ID,CPQ_PARTNER_FUNCTION FROM SAQTIP(NOLOCK) WHERE QUOTE_RECORD_ID = '"+str(self.quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_id)+"' and CPQ_PARTNER_FUNCTION in ('SOLD TO','SHIP TO')")
        for keyobj in get_party_role:
            self.account_info[keyobj.CPQ_PARTNER_FUNCTION] = keyobj.PARTY_ID
        
        saqtsv_obj = Sql.GetFirst("SELECT SERVICE_ID,SERVICE_DESCRIPTION,SERVICE_RECORD_ID FROM SAQTSV where QUOTE_RECORD_ID = '"+str(self.quote_record_id)+"'")
        if saqtsv_obj:
            self.service_id = saqtsv_obj.SERVICE_ID
            self.service_desc = saqtsv_obj.SERVICE_DESCRIPTION
            self.service_record_id = saqtsv_obj.SERVICE_RECORD_ID
        
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
        
    def prepare_backup_table(self):
        res = ''.join(str(ele) for ele in self.response)
        cnt = res.count("Material_Eligibility")
        Log.Info("first response----->2"+str(res))
        if cnt == 1:
            res = re.sub(r'\[',"['",res)
            res= re.sub(r'\]',"']",res)
            res= re.sub(r", ","':'",res)
            res = re.sub(r"\],\[",", ",res)
            res= re.sub(r'\[',"{",res)
            res= re.sub(r'\]',"}",res)
            res = re.sub(r':',' : ',res)
            res= re.sub(r'\}\{',', ',res)
            Log.Info("sec response----->2"+str(res))
        if self.response:
            response = ','.join(str(ele) for ele in self.response)
            record_count=0
            if cnt ==1:
                response=res
            Log.Info("PrepareBackuptable----->2"+str(response))
            response=response.replace("null",'""')
            response=response.replace("None",'""')
            response=response.replace("true",'1')
            response=response.replace("false",'0')
            response=response.replace("True",'1')
            response=response.replace("False",'0')
            response=response.replace("TRUE",'1')
            response=response.replace("FALSE",'0')
            response=response.replace("YES",'1')
            response=response.replace("NO",'0')
            response=response.replace("Yes",'1')
            response=response.replace("No",'0')
            response=response.replace("yes",'1')
            response=response.replace("no",'0')
            response=response.replace("'",'"')
            response = re.sub(r'\[|\]|\(|\)','',response)
            pattern = re.compile(r'(\{[^>]*?\})')
            #pattern2 = re.compile(r'\"([^>]*?)\"\:(\"[^>]*?\")')
            #pattern2 = re.compile(r"\'([^>]*?)\'\s*\:\s*([^>]*?)(?:\,|\})")
            #pattern2 = re.compile(r'([^>]*?)\s*:\s*([^>]*?)(?:\,|\})')
            pattern2 = re.compile(r'(\"[^>]*?\")\s*:\s*(\"[^>]*?\")')
            self.columns = 'QUOTE_RECORD_ID,QTEREV_RECORD_ID'
            value  = '''(\"{}\",\"{}\"'''.format(self.quote_record_id,self.quote_revision_id)
            col_flag = 0
            for record in re.finditer(pattern, response):
                #rec = re.sub(r'\{|\}','',record.group(1))
                record_count +=1
                rec = record.group(1)
                temp_value = value
                for ele in re.finditer(pattern2,rec):
                    if col_flag == 0:
                        self.columns +=','+ele.group(1)
                    if ele.group(1) == '"PARENT_PART_NUMBER"':
                        self.part_numbers.append(str(ele.group(2)))
                    #    partdesc = ele.group(2) or ''
                    #    partdesc = re.sub(r"'|\\","",partdesc)
                    #    temp_value +=','+partdesc if partdesc !='' else None
                    #else:
                    temp_value +=','+ele.group(2) if ele.group(2) !='' else None
                #if col_flag == 0:
                #	self.columns +=')'
                temp_value +=')'
                temp_value = re.sub(r"'",'"',temp_value)
                temp_value = re.sub(r'"',"''",temp_value)
                if self.records == '':
                    self.records = temp_value
                else:
                    self.records += ', '+temp_value
                temp_value =''
                col_flag=1
            Log.Info("Total Records from HANA::"+str(record_count))
            Log.Info("Total Parts List:: " +str(self.part_numbers))
            if record_count >0:
                self._insert_spare_parts()
                self.update_records_saqspt()  
                self.insert_delivery_schedule()
                try:
                    self.CQPARTIFLW_iflow()        
                except Exception:
                    Log.Info("PART PRICING IFLOW ERROR!")

    def delete_child_records_6kw(self):
        Trace.Write('Delete Child called!!!')
        Sql.RunQuery("DELETE FROM SAQSPT WHERE PAR_PART_NUMBER != '' AND QUOTE_RECORD_ID = '"+str(self.quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_id)+"' AND SERVICE_ID = '"+str(self.service_id)+"'")

    def delete_child_records_6kw_partlist(self,Part_Numbers):
        part_list=tuple(Part_Numbers)
        val=re.sub(r'\,\)',')',str(part_list))
        Trace.Write('Delete Child called pARTlIST!!!'+str(val))

        Sql.RunQuery("DELETE FROM SAQSPT WHERE PAR_PART_NUMBER IN "+str(val)+" AND QUOTE_RECORD_ID = '"+str(self.quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_id)+"' AND SERVICE_ID = '"+str(self.service_id)+"'")
        
        if self.service_id == 'Z0108':
            Sql.RunQuery("UPDATE SAQSPT SET SCHEDULE_MODE='SCHEDULED' WHERE PART_NUMBER IN "+str(val)+" AND QUOTE_RECORD_ID = '"+str(self.quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_id)+"' AND SERVICE_ID = '"+str(self.service_id)+"'")
            
    def validation_for_arp_carp(self):
        requestdata = "client_id=application&grant_type=client_credentials&username=954e4350-7854-465b-8c0f-d428d3ea9cdf&password=Ieo.mslSbRzZE0NmuR3ubwcbXsfqTc&scope=nodesafeaccessscope"
        webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/x-www-form-urlencoded"
        webclient.Headers[System.Net.HttpRequestHeader.Authorization] = "Basic OTU0ZTQzNTAtNzg1NC00NjViLThjMGYtZDQyOGQzZWE5Y2RmOm1zbFNiUnpaRTBObXVSM3Vid2NiWHNmcVRj"
        response = webclient.UploadString('https://oauth2.c-1404e87.kyma.shoot.live.k8s-hana.ondemand.com/oauth2/token',str(requestdata))
        response=response.replace("null",'""')
        response=eval(response)
        auth="Bearer"+' '+str(response['access_token'])
        partnos = str(self.part_numbers)
        partnos = re.sub(r"'",'',partnos)
        requestdata = '{"materials":'+str(partnos)+',"soldtoParty":"'+str(self.account_info['SOLD TO'])+'","salesOrg":"'+str(self.sales_org_id)+'"}'
        Log.Info("RData-->"+str(requestdata))
        webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/json"
        webclient.Headers[System.Net.HttpRequestHeader.Authorization] = auth
        self.arp_carp_response = webclient.UploadString('https://carp-arp.c-1404e87.kyma.shoot.live.k8s-hana.ondemand.com',str(requestdata))
        Log.Info("Resarpcarp-->"+str(self.arp_carp_response))

    def CQPARTIFLW_iflow(self):
        CQPARTIFLW.iflow_pricing_call(str(User.UserName),str(self.quote_id),str(self.quote_revision_id))

        
Log.Info("CQPARTINS script called --> from CPI")
#Log.Info("Param.CPQ_Column----"+str(type(Param)))
Log.Info("Param.CPQ_Column----QuoteID---"+str(Param.CPQ_Columns["QuoteID"]))
Parameter = {}
try:
    Parameter["Action"] = Param.CPQ_Columns["Action"]
except Exception:
    Parameter["Action"] = 'Default'

try:
    Parameter["Delete_Partlist"] = Param.CPQ_Columns["Delete_Partlist"]
except Exception:
    Parameter["Delete_Partlist"] = ""


if Parameter["Action"] == 'Delete':
    fpm_obj = SyncFPMQuoteAndHanaDatabase()
    fpm_obj.fetch_quotebasic_info()
    if Parameter["Delete_Partlist"]:
        fpm_obj.delete_child_records_6kw_partlist(Parameter["Delete_Partlist"])
    else:
        fpm_obj.delete_child_records_6kw()
  

if Param.CPQ_Columns["QuoteID"] and Parameter["Action"] == 'Default':
    fpm_obj = SyncFPMQuoteAndHanaDatabase()
    fpm_obj.fetch_quotebasic_info()
    fpm_obj.prepare_backup_table()  
    #fpm_obj.validation_for_arp_carp()
    
    
    

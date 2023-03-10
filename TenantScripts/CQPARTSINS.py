#========================================================================================================================================
#   __script_name : CQPARTSINS.py
#   __script_description : THIS SCRIPT IS USED TO CONNECT WITH HANA TABLES TO PULL PARTS AND LOADED INTO CPQ.
#   __primary_author__ : Suriyanarayanan Pazhani
#   __create_date :09-01-2022 
#=========================================================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct
import clr
import re
import datetime
import CQIFLSPARE
import CQPARTIFLW
import System.Net
from datetime import timedelta , date
from SYDATABASE import SQL
Sql = SQL()
webclient = System.Net.WebClient()

class SyncFPMQuoteAndHanaDatabase:
    def __init__(self):
        self.response = self.arp_carp_response = self.sales_org_id = self.sales_recd_id = self.qt_rev_id = self.quote_id = self.contract_valid_from = self.contract_valid_to = self.columns= self.records= self.cvf = self.cvt = self.service_id = self.service_desc = self.service_record_id = self.global_curr = self.global_curr_recid=self.quote_record_id=self.quote_revision_id=self.spare_parts_temp_table_name=self.pricelist=self.pricegroup=self.auth=self.domain=self.oauthURL=''
        self.datetime_value = datetime.datetime.now()
        self.account_info = {}
        self.part_numbers = []
        self.primaryShipto={}
        try:
            self.quote_id = str(Param.CPQ_Columns["QuoteID"])
        except Exception:
            Log.Info("@@@Self Quote ID is Missing@@@")
        try:
            self.response = Param.CPQ_Columns["Response"]["root"]["KYMA_DATA"]["SAFPLT"]
        except Exception:
            Log.Info("@@@Self Response is Missing@@@")
            
    def _insert_spare_parts(self):
        Log.Info("inside _insert_spare_parts")
        datetime_string = self.datetime_value.strftime("%d%m%Y%H%M%S")
        uid=str(Guid.NewGuid()).upper()
        uids=uid.split('-')
        spare_parts_temp_table_name = "SAQSPT_BKP_{}_{}_{}".format(self.quote_record_id, datetime_string,str(uids[0]))
        spare_parts_temp_table_name = re.sub(r'-','_',spare_parts_temp_table_name)
        self.columns = re.sub(r'\"|\{','',self.columns)
        self.columns = re.sub(r',,',',',self.columns)
        #Log.Info("Columns--->"+str(self.columns))
        #Log.Info("Values---->"+str(self.records))
        try:
            spare_parts_temp_table_drop = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(spare_parts_temp_table_name)+"'' ) BEGIN DROP TABLE "+str(spare_parts_temp_table_name)+" END  ' ")

            spare_parts_temp_table_bkp = SqlHelper.GetFirst("sp_executesql @T=N'SELECT "+str(self.columns)+" INTO "+str(spare_parts_temp_table_name)+" FROM (SELECT DISTINCT "+str(self.columns)+" FROM (VALUES "+str(self.records)+") AS TEMP("+str(self.columns)+")) OQ ' ")
            # INC08593801 - Start - M
            insert_qry = """
                            INSERT SAQSPT (QUOTE_SERVICE_PART_RECORD_ID, BASEUOM_ID, BASEUOM_RECORD_ID, CUSTOMER_PART_NUMBER, CUSTOMER_PART_NUMBER_RECORD_ID, DELIVERY_MODE, EXTENDED_UNIT_PRICE, PART_DESCRIPTION, PART_NUMBER, PART_RECORD_ID, PRDQTYCON_RECORD_ID, CUSTOMER_ANNUAL_QUANTITY, QUOTE_ID, QUOTE_NAME, QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,SALESORG_ID, SALESORG_RECORD_ID, SALESUOM_CONVERSION_FACTOR, SALESUOM_ID, SALESUOM_RECORD_ID, SCHEDULE_MODE, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, UNIT_PRICE, MATPRIGRP_ID, MATPRIGRP_RECORD_ID, DELIVERY_INTERVAL, VALID_FROM_DATE, VALID_TO_DATE,PAR_SERVICE_DESCRIPTION,PAR_SERVICE_ID,PAR_SERVICE_RECORD_ID, RETURN_TYPE, ODCC_FLAG,ODCC_FLAG_DESCRIPTION, PAR_PART_NUMBER, EXCHANGE_ELIGIBLE, CUSTOMER_ELIGIBLE,CUSTOMER_PARTICIPATE, CUSTOMER_ACCEPT_PART,YEAR_1_DEMAND,YEAR_2_DEMAND,YEAR_3_DEMAND,PROD_INSP_MEMO,SHELF_LIFE,PRICING_STATUS,STPACCOUNT_ID, SHPACCOUNT_ID,MATERIALSTATUS_ID,GLOBAL_CURRENCY, GLOBAL_CURRENCY_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED)
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
                                ODCC_FLAG_DESCRIPTION,
                                PAR_PART_NUMBER,
                                EXCHANGE_ELIGIBLE,
                                CUSTOMER_ELIGIBLE,
                                CUSTOMER_PARTICIPATE,
                                CUSTOMER_ACCEPT_PART,
                                YEAR_1_DEMAND,
                                YEAR_2_DEMAND,
                                YEAR_3_DEMAND,
                                PROD_INSP_MEMO,
                                SHELF_LIFE,
                                PRICING_STATUS,
                                STPACCOUNT_ID,
                                SHPACCOUNT_ID,
                                MATERIALSTATUS_ID,
                                GLOBAL_CURRENCY,
                                GLOBAL_CURRENCY_RECORD_ID,
                                {UserId} as CPQTABLEENTRYADDEDBY, 
                                GETDATE() as CPQTABLEENTRYDATEADDED
                            FROM (
                            SELECT 
                                DISTINCT
                                MAMTRL.UNIT_OF_MEASURE as BASEUOM_ID,
                                MAMTRL.UOM_RECORD_ID as BASEUOM_RECORD_ID,
                                NULL AS CUSTOMER_PART_NUMBER,
                                MAMTRL.MATERIAL_RECORD_ID as CUSTOMER_PART_NUMBER_RECORD_ID,
                                CASE WHEN SAQTSV.SERVICE_ID='Z0110' THEN NULL ELSE 'OFFSITE' END AS DELIVERY_MODE,
                                0.00 as EXTENDED_UNIT_PRICE,
                                MAMTRL.SAP_DESCRIPTION as PART_DESCRIPTION,
                                CASE WHEN TEMP_TABLE.CHILD_PART_NUMBER!='' THEN TEMP_TABLE.CHILD_PART_NUMBER ELSE MAMTRL.SAP_PART_NUMBER END AS PART_NUMBER,
                                MAMTRL.MATERIAL_RECORD_ID as PART_RECORD_ID,
                                '' as PRDQTYCON_RECORD_ID,
                                CASE WHEN TEMP_TABLE.CUSTOMER_ANNUAL_QUANTITY='' AND TEMP_TABLE.CHILD_PART_NUMBER!='' THEN 1 WHEN TEMP_TABLE.CUSTOMER_ANNUAL_QUANTITY='' THEN NULL ELSE TEMP_TABLE.CUSTOMER_ANNUAL_QUANTITY END as QUANTITY,
                                SAQTMT.QUOTE_ID as QUOTE_ID,
                                SAQTMT.QUOTE_NAME as QUOTE_NAME,
                                SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID as QUOTE_RECORD_ID,
                                SAQTMT.QTEREV_ID as QTEREV_ID,
                                SAQTMT.QTEREV_RECORD_ID as QTEREV_RECORD_ID,
                                SAQTSV.SALESORG_ID as SALESORG_ID,
                                SAQTSV.SALESORG_RECORD_ID as SALESORG_RECORD_ID,
                                1.00 as SALESUOM_CONVERSION_FACTOR,
                                CASE WHEN MAMSOP.SALESUOM_ID<>'' THEN MAMSOP.SALESUOM_ID ELSE MAMTRL.UNIT_OF_MEASURE END as SALESUOM_ID,
                                CASE WHEN MAMSOP.SALESUOM_RECORD_ID<>'' THEN MAMSOP.SALESUOM_RECORD_ID ELSE MAMTRL.UOM_RECORD_ID END as SALESUOM_RECORD_ID, 
                                CASE WHEN SAQTSV.SERVICE_ID='Z0110' THEN NULL ELSE 'SCHEDULED' END AS SCHEDULE_MODE,
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
                                CASE WHEN TEMP_TABLE.ODCC_FLAG='ZZZ' THEN null ELSE TEMP_TABLE.ODCC_FLAG END AS ODCC_FLAG,
                                CASE WHEN TEMP_TABLE.ODCC_FLAG='ZZZ' THEN null ELSE TEMP_TABLE.ODCC_FLAG_DESCRIPTION END as ODCC_FLAG_DESCRIPTION,
                                CASE WHEN ISNULL(TEMP_TABLE.CHILD_PART_NUMBER,'')='' THEN null ELSE TEMP_TABLE.PARENT_PART_NUMBER END AS PAR_PART_NUMBER,
                                TEMP_TABLE.Material_Eligibility AS EXCHANGE_ELIGIBLE,
                                CASE WHEN TEMP_TABLE.Customer_Eligibility='X' THEN 'True' ELSE 'False' END AS CUSTOMER_ELIGIBLE,
                                'True' as CUSTOMER_PARTICIPATE,
                                'True' as CUSTOMER_ACCEPT_PART,
                                CASE WHEN TEMP_TABLE.YEAR_1_DEMAND='' THEN null ELSE TEMP_TABLE.YEAR_1_DEMAND END AS YEAR_1_DEMAND,
                                CASE WHEN TEMP_TABLE.YEAR_2_DEMAND='' THEN null ELSE TEMP_TABLE.YEAR_2_DEMAND END AS YEAR_2_DEMAND,
                                CASE WHEN TEMP_TABLE.YEAR_3_DEMAND='' THEN null ELSE TEMP_TABLE.YEAR_3_DEMAND END AS YEAR_3_DEMAND,
                                CASE WHEN TEMP_TABLE.PROD_INSP_MEMO='' THEN null ELSE TEMP_TABLE.PROD_INSP_MEMO END AS PROD_INSP_MEMO,
                                CASE WHEN TEMP_TABLE.SHELF_LIFE='' THEN null ELSE TEMP_TABLE.SHELF_LIFE END AS SHELF_LIFE,
                                'NOT PRICED' AS PRICING_STATUS,
                                CASE WHEN TEMP_TABLE.STPACCOUNT_ID='' THEN {SOLDTO} ELSE TEMP_TABLE.STPACCOUNT_ID END as STPACCOUNT_ID,
                                CASE WHEN TEMP_TABLE.SHPACCOUNT_ID='' THEN {SHIPTO} ELSE TEMP_TABLE.SHPACCOUNT_ID END as SHPACCOUNT_ID,
                                MAMSOP.MATERIALSTATUS_ID AS MATERIALSTATUS_ID,
                                '{GLOBALCURR}' as GLOBAL_CURRENCY,
                                '{GLOBALCURR_REC}' as GLOBAL_CURRENCY_RECORD_ID
                            FROM {TempTable} TEMP_TABLE(NOLOCK)
                            JOIN MAMTRL (NOLOCK) ON MAMTRL.SAP_PART_NUMBER = TEMP_TABLE.PARENT_PART_NUMBER
                            JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = TEMP_TABLE.QUOTE_RECORD_ID
                            JOIN SAQTSV (NOLOCK) ON SAQTSV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SAQTSV.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID AND SAQTSV.SERVICE_ID = '{ServiceId}'
                            JOIN MAMSOP (NOLOCK) ON MAMSOP.MATERIAL_RECORD_ID = MAMTRL.MATERIAL_RECORD_ID AND MAMSOP.SALESORG_RECORD_ID = SAQTSV.SALESORG_RECORD_ID
                            WHERE TEMP_TABLE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND TEMP_TABLE.QTEREV_RECORD_ID = '{RevisionRecordId}' AND MAMTRL.PRODUCT_TYPE IS NULL AND ISNULL(MAMSOP.MATERIALSTATUS_ID,'') NOT IN('05','02') AND TEMP_TABLE.PARENT_PART_NUMBER NOT IN(SELECT PART_NUMBER FROM SAQSPT (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}')) IQ
                            """.format(
                                        TempTable=spare_parts_temp_table_name,
                                        ServiceId=self.service_id,									
                                        QuoteRecordId=self.quote_record_id,
                                        RevisionRecordId=self.quote_revision_id,
                                        UserId=User.Id,
                                        GLOBALCURR=self.global_curr,
                                        GLOBALCURR_REC=self.global_curr_recid,
                                        SOLDTO=self.account_info['SOLD TO'],
                                        SHIPTO=self.primaryShipto['SHIP TO']

                                )
                            
            Sql.RunQuery(insert_qry)
            #only child records insert
            Sql.RunQuery("""
                            INSERT SAQSPT (QUOTE_SERVICE_PART_RECORD_ID, BASEUOM_ID, BASEUOM_RECORD_ID, CUSTOMER_PART_NUMBER, CUSTOMER_PART_NUMBER_RECORD_ID, DELIVERY_MODE, EXTENDED_UNIT_PRICE, PART_DESCRIPTION, PART_NUMBER, PART_RECORD_ID, PRDQTYCON_RECORD_ID, CUSTOMER_ANNUAL_QUANTITY, QUOTE_ID, QUOTE_NAME, QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,SALESORG_ID, SALESORG_RECORD_ID, SALESUOM_CONVERSION_FACTOR, SALESUOM_ID, SALESUOM_RECORD_ID, SCHEDULE_MODE, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, UNIT_PRICE, MATPRIGRP_ID, MATPRIGRP_RECORD_ID, DELIVERY_INTERVAL, VALID_FROM_DATE, VALID_TO_DATE,PAR_SERVICE_DESCRIPTION,PAR_SERVICE_ID,PAR_SERVICE_RECORD_ID, RETURN_TYPE, ODCC_FLAG,ODCC_FLAG_DESCRIPTION, PAR_PART_NUMBER, EXCHANGE_ELIGIBLE, CUSTOMER_ELIGIBLE,CUSTOMER_PARTICIPATE, CUSTOMER_ACCEPT_PART,YEAR_1_DEMAND,YEAR_2_DEMAND,YEAR_3_DEMAND,PROD_INSP_MEMO,SHELF_LIFE,PRICING_STATUS,STPACCOUNT_ID, SHPACCOUNT_ID,MATERIALSTATUS_ID,GLOBAL_CURRENCY, GLOBAL_CURRENCY_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED)
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
                                ODCC_FLAG_DESCRIPTION,
                                PAR_PART_NUMBER,
                                EXCHANGE_ELIGIBLE,
                                CUSTOMER_ELIGIBLE,
                                CUSTOMER_PARTICIPATE,
                                CUSTOMER_ACCEPT_PART,
                                YEAR_1_DEMAND,
                                YEAR_2_DEMAND,
                                YEAR_3_DEMAND,
                                PROD_INSP_MEMO,
                                SHELF_LIFE,
                                PRICING_STATUS,
                                STPACCOUNT_ID,
                                SHPACCOUNT_ID,
                                MATERIALSTATUS_ID,
                                GLOBAL_CURRENCY,
                                GLOBAL_CURRENCY_RECORD_ID,
                                {UserId} as CPQTABLEENTRYADDEDBY, 
                                GETDATE() as CPQTABLEENTRYDATEADDED
                            FROM (
                            SELECT 
                                DISTINCT
                                MAMTRL.UNIT_OF_MEASURE as BASEUOM_ID,
                                MAMTRL.UOM_RECORD_ID as BASEUOM_RECORD_ID,
                                NULL AS CUSTOMER_PART_NUMBER,
                                MAMTRL.MATERIAL_RECORD_ID as CUSTOMER_PART_NUMBER_RECORD_ID,
                                CASE WHEN SAQTSV.SERVICE_ID='Z0110' THEN NULL ELSE 'OFFSITE' END AS DELIVERY_MODE,
                                0.00 as EXTENDED_UNIT_PRICE,
                                MAMTRL.SAP_DESCRIPTION as PART_DESCRIPTION,
                                CASE WHEN TEMP_TABLE.CHILD_PART_NUMBER!='' THEN TEMP_TABLE.CHILD_PART_NUMBER ELSE MAMTRL.SAP_PART_NUMBER END AS PART_NUMBER,
                                MAMTRL.MATERIAL_RECORD_ID as PART_RECORD_ID,
                                '' as PRDQTYCON_RECORD_ID,
                                CASE WHEN TEMP_TABLE.CUSTOMER_ANNUAL_QUANTITY='' AND TEMP_TABLE.CHILD_PART_NUMBER!='' THEN 1 WHEN TEMP_TABLE.CUSTOMER_ANNUAL_QUANTITY='' THEN NULL ELSE TEMP_TABLE.CUSTOMER_ANNUAL_QUANTITY END as QUANTITY,
                                SAQTMT.QUOTE_ID as QUOTE_ID,
                                SAQTMT.QUOTE_NAME as QUOTE_NAME,
                                SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID as QUOTE_RECORD_ID,
                                SAQTMT.QTEREV_ID as QTEREV_ID,
                                SAQTMT.QTEREV_RECORD_ID as QTEREV_RECORD_ID,
                                SAQTSV.SALESORG_ID as SALESORG_ID,
                                SAQTSV.SALESORG_RECORD_ID as SALESORG_RECORD_ID,
                                1.00 as SALESUOM_CONVERSION_FACTOR,
                                CASE WHEN MAMSOP.SALESUOM_ID<>'' THEN MAMSOP.SALESUOM_ID ELSE MAMTRL.UNIT_OF_MEASURE END as SALESUOM_ID,
                                CASE WHEN MAMSOP.SALESUOM_RECORD_ID<>'' THEN MAMSOP.SALESUOM_RECORD_ID ELSE MAMTRL.UOM_RECORD_ID END as SALESUOM_RECORD_ID, 
                                CASE WHEN SAQTSV.SERVICE_ID='Z0110' THEN NULL ELSE 'SCHEDULED' END AS SCHEDULE_MODE,
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
                                CASE WHEN TEMP_TABLE.ODCC_FLAG='ZZZ' THEN null ELSE TEMP_TABLE.ODCC_FLAG END AS ODCC_FLAG,
                                CASE WHEN TEMP_TABLE.ODCC_FLAG='ZZZ' THEN null ELSE TEMP_TABLE.ODCC_FLAG_DESCRIPTION END as ODCC_FLAG_DESCRIPTION,
                                CASE WHEN ISNULL(TEMP_TABLE.CHILD_PART_NUMBER,'')='' THEN null ELSE TEMP_TABLE.PARENT_PART_NUMBER END AS PAR_PART_NUMBER,
                                TEMP_TABLE.Material_Eligibility AS EXCHANGE_ELIGIBLE,
                                CASE WHEN TEMP_TABLE.Customer_Eligibility='X' THEN 'True' ELSE 'False' END AS CUSTOMER_ELIGIBLE,
                                'True' as CUSTOMER_PARTICIPATE,
                                'True' as CUSTOMER_ACCEPT_PART,
                                CASE WHEN TEMP_TABLE.YEAR_1_DEMAND='' THEN null ELSE TEMP_TABLE.YEAR_1_DEMAND END AS YEAR_1_DEMAND,
                                CASE WHEN TEMP_TABLE.YEAR_2_DEMAND='' THEN null ELSE TEMP_TABLE.YEAR_2_DEMAND END AS YEAR_2_DEMAND,
                                CASE WHEN TEMP_TABLE.YEAR_3_DEMAND='' THEN null ELSE TEMP_TABLE.YEAR_3_DEMAND END AS YEAR_3_DEMAND,
                                CASE WHEN TEMP_TABLE.PROD_INSP_MEMO='' THEN null ELSE TEMP_TABLE.PROD_INSP_MEMO END AS PROD_INSP_MEMO,
                                CASE WHEN TEMP_TABLE.SHELF_LIFE='' THEN null ELSE TEMP_TABLE.SHELF_LIFE END AS SHELF_LIFE,
                                'NOT PRICED' AS PRICING_STATUS,
                                TEMP_TABLE.STPACCOUNT_ID as STPACCOUNT_ID,
                                TEMP_TABLE.SHPACCOUNT_ID as SHPACCOUNT_ID,
                                MAMSOP.MATERIALSTATUS_ID as MATERIALSTATUS_ID,
                                '{GLOBALCURR}' as GLOBAL_CURRENCY,
                                '{GLOBALCURR_REC}' as GLOBAL_CURRENCY_RECORD_ID
                            FROM {TempTable} TEMP_TABLE(NOLOCK)
                            JOIN MAMTRL (NOLOCK) ON MAMTRL.SAP_PART_NUMBER = TEMP_TABLE.PARENT_PART_NUMBER
                            JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = TEMP_TABLE.QUOTE_RECORD_ID
                            JOIN SAQTSV (NOLOCK) ON SAQTSV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SAQTSV.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID AND SAQTSV.SERVICE_ID = '{ServiceId}'
                            JOIN MAMSOP (NOLOCK) ON MAMSOP.MATERIAL_RECORD_ID = MAMTRL.MATERIAL_RECORD_ID AND MAMSOP.SALESORG_RECORD_ID = SAQTSV.SALESORG_RECORD_ID
                            WHERE TEMP_TABLE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND TEMP_TABLE.QTEREV_RECORD_ID = '{RevisionRecordId}' AND MAMTRL.PRODUCT_TYPE IS NULL AND ISNULL(MAMSOP.MATERIALSTATUS_ID,'') NOT IN('05','02') AND ISNULL(TEMP_TABLE.CHILD_PART_NUMBER,'') <>'' AND NOT EXISTS(SELECT PART_NUMBER FROM SAQSPT (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND TEMP_TABLE.CHILD_PART_NUMBER = PART_NUMBER)) IQ
                            """.format(
                                        TempTable=spare_parts_temp_table_name,
                                        ServiceId=self.service_id,									
                                        QuoteRecordId=self.quote_record_id,
                                        RevisionRecordId=self.quote_revision_id,
                                        UserId=User.Id,
                                        GLOBALCURR=self.global_curr,
                                        GLOBALCURR_REC=self.global_curr_recid
                                    )
            )
            # INC08593801 - End - M
            self.spare_parts_temp_table_name = spare_parts_temp_table_name
        except Exception as e:
            Log.Info("EXCEPTION E : " + str(e))
        
    def update_records_saqspt(self):
        update_odcc_retuntype = """UPDATE SAQSPT SET SAQSPT.ODCC_FLAG=CASE WHEN TEMP_TABLE.ODCC_FLAG='ZZZ' THEN null ELSE TEMP_TABLE.ODCC_FLAG END,SAQSPT.RETURN_TYPE=TEMP_TABLE.RETURN_TYPE, SAQSPT.ODCC_FLAG_DESCRIPTION=CASE WHEN TEMP_TABLE.ODCC_FLAG='ZZZ' THEN null ELSE TEMP_TABLE.ODCC_FLAG_DESCRIPTION END FROM SAQSPT JOIN {TempTable} TEMP_TABLE(NOLOCK) ON SAQSPT.PART_NUMBER= TEMP_TABLE.PARENT_PART_NUMBER AND SAQSPT.QUOTE_RECORD_ID = TEMP_TABLE.QUOTE_RECORD_ID AND SAQSPT.QTEREV_RECORD_ID=TEMP_TABLE.QTEREV_RECORD_ID WHERE (TEMP_TABLE.CHILD_PART_NUMBER='' OR TEMP_TABLE.CHILD_PART_NUMBER IS NULL) AND SAQSPT.QUOTE_RECORD_ID = '{quote_rec_id}' AND SAQSPT.QTEREV_RECORD_ID = '{quote_revision_rec_id}'""".format(quote_rec_id = self.quote_record_id,TempTable = self.spare_parts_temp_table_name,quote_revision_rec_id =self.quote_revision_id)
        Sql.RunQuery(update_odcc_retuntype)
            
        update_customer_pn = """UPDATE SAQSPT SET SAQSPT.CUSTOMER_PART_NUMBER = M.CUSTOMER_PART_NUMBER FROM SAQSPT S INNER JOIN MAMSAC M ON S.PART_NUMBER= M.SAP_PART_NUMBER WHERE M.SALESORG_ID = '{sales_id}' and M.ACCOUNT_ID='{stp_acc_id}' AND S.QUOTE_RECORD_ID = '{quote_rec_id}' AND S.QTEREV_RECORD_ID = '{quote_revision_rec_id}'""".format(quote_rec_id = self.quote_record_id,sales_id = self.sales_org_id,stp_acc_id=str(self.account_info['SOLD TO']),quote_revision_rec_id =self.quote_revision_id)
        Sql.RunQuery(update_customer_pn)

        update_salesuom_conv= """UPDATE SAQSPT SET SAQSPT.SALESUOM_CONVERSION_FACTOR =   CASE WHEN M.BASE_QUANTITY=0.00 THEN 1.00 ELSE M.BASE_QUANTITY END FROM SAQSPT S INNER JOIN MAMUOC M ON S.PART_NUMBER= M.SAP_PART_NUMBER WHERE S.BASEUOM_ID=M.BASEUOM_ID AND  S.SALESUOM_ID=M.CONVERSIONUOM_ID AND S.QUOTE_RECORD_ID = '{quote_rec_id}' AND S.QTEREV_RECORD_ID = '{quote_revision_rec_id}'""".format(quote_rec_id = self.quote_record_id ,quote_revision_rec_id =self.quote_revision_id)
        Sql.RunQuery(update_salesuom_conv)

        spare_temp_table_name ="EXCELUPDATE_SAQSPT_{}".format(self.quote_id)
        excel_bkp=SqlHelper.GetFirst("""SELECT COUNT(*) AS CNT FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME ='{table_name}'""".format(table_name=spare_temp_table_name))
        if int(excel_bkp.CNT) == 1:
            if self.service_id == 'Z0108':
                update_columns=""
                for val in range(1,53):
                    update_columns+="SAQSPT.DELIVERY_"+str(val)+" = CASE WHEN M.DELIVERY_"+str(val)+"='' THEN NULL ELSE M.DELIVERY_"+str(val)+" END,"
                col=","+str(update_columns[:-1])
            else:
                col=""
            
            update_saqspt = """UPDATE SAQSPT SET SAQSPT.CUSTOMER_PART_NUMBER  = CASE WHEN M.CUSTOMER_PART_NUMBER='' THEN NULL ELSE M.CUSTOMER_PART_NUMBER END ,SAQSPT.CUSTOMER_ACCEPT_PART=CASE WHEN M.CUSTOMER_ACCEPT_PART ='Yes' OR M.CUSTOMER_ACCEPT_PART ='YES' THEN 'True' ELSE 'False' END ,SAQSPT.CUSTOMER_PARTICIPATE=CASE WHEN M.CUSTOMER_PARTICIPATE ='Yes' OR M.CUSTOMER_PARTICIPATE ='YES' THEN 'True' ELSE 'False' END ,SAQSPT.CUSTOMER_ANNUAL_QUANTITY=CASE WHEN M.CUSTOMER_ANNUAL_QUANTITY = '' THEN NULL ELSE M.CUSTOMER_ANNUAL_QUANTITY END, SAQSPT.DELIVERY_MODE=CASE WHEN M.DELIVERY_MODE = '' THEN NULL ELSE M.DELIVERY_MODE END,SAQSPT.SCHEDULE_MODE=CASE WHEN M.SCHEDULE_MODE= '' THEN NULL ELSE M.SCHEDULE_MODE END {cols} FROM SAQSPT S INNER JOIN {table_name} M ON S.PART_NUMBER= M.PART_NUMBER WHERE S.QUOTE_RECORD_ID = '{quote_rec_id}' AND S.QTEREV_RECORD_ID = '{quote_revision_rec_id}' """.format(table_name=spare_temp_table_name,cols=col,quote_rec_id = self.quote_record_id ,quote_revision_rec_id =self.quote_revision_id )
            Sql.RunQuery(update_saqspt)
            
            delete_child_saqspt = """DELETE FROM SAQSPT WHERE PAR_PART_NUMBER IN(SELECT PART_NUMBER FROM SAQSPT WHERE QUOTE_RECORD_ID = '{quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_rec_id}' AND( CUSTOMER_ACCEPT_PART='False' OR CUSTOMER_PARTICIPATE='False')) AND QUOTE_RECORD_ID = '{quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_rec_id}'""".format(quote_rec_id = self.quote_record_id,quote_revision_rec_id =self.quote_revision_id )
            Sql.RunQuery(delete_child_saqspt)
        
        child_update_odcc_returntype="""UPDATE SAQSPT  SET DELIVERY_MODE=PARENT.DELIVERY_MODE,SCHEDULE_MODE = PARENT.SCHEDULE_MODE FROM SAQSPT (NOLOCK) INNER JOIN (SELECT SAQSPT.DELIVERY_MODE,SAQSPT.SCHEDULE_MODE,SAQSPT.PART_NUMBER,SAQSPT.QUOTE_RECORD_ID,SAQSPT.QTEREV_RECORD_ID FROM SAQSPT WHERE SAQSPT.QUOTE_RECORD_ID='{quote_rec_id}' AND SAQSPT.QTEREV_RECORD_ID='{quote_revision_rec_id}' ) PARENT on SAQSPT.QUOTE_RECORD_ID=PARENT.QUOTE_RECORD_ID AND SAQSPT.QTEREV_RECORD_ID=PARENT.QTEREV_RECORD_ID AND SAQSPT.PAR_PART_NUMBER = PARENT.PART_NUMBER WHERE SAQSPT.QTEREV_RECORD_ID ='{quote_revision_rec_id}' AND SAQSPT.QUOTE_RECORD_ID='{quote_rec_id}' AND SAQSPT.PAR_PART_NUMBER IS NOT NULL""".format(quote_rec_id = self.quote_record_id,quote_revision_rec_id =self.quote_revision_id)
        Log.Info(child_update_odcc_returntype)
        Sql.RunQuery(child_update_odcc_returntype)
        Log.Info("Odcc")
        
        odcc_returntype_reset = """UPDATE SAQSPT SET ODCC_FLAG=NULL, RETURN_TYPE=NULL, ODCC_FLAG_DESCRIPTION=NULL, CORE_CREDIT_PRICE=NULL WHERE CUSTOMER_PARTICIPATE='False' AND QUOTE_RECORD_ID = '{quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_rec_id}'""".format(quote_rec_id = self.quote_record_id,quote_revision_rec_id =self.quote_revision_id )
        Log.Info(odcc_returntype_reset)
        Sql.RunQuery(odcc_returntype_reset)
        Log.Info("return")
        spare_parts_temp_table_drop = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(self.spare_parts_temp_table_name)+"'' ) BEGIN DROP TABLE "+str(self.spare_parts_temp_table_name)+" END  ' ")
        Log.Info(("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(self.spare_parts_temp_table_name)+"'' ) BEGIN DROP TABLE "+str(self.spare_parts_temp_table_name)+" END  ' "))
            
    def reprice_update_qty(self):
        update_qty_saqspt = """UPDATE SAQSPT SET SAQSPT.CUSTOMER_ANNUAL_QUANTITY = {qty} FROM SAQSPT  WHERE PART_NUMBER = '{part_number}' and QUOTE_RECORD_ID = '{quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_rec_id}'""".format(qty=str(Parameter["Annual_Quantity"]),part_number=str(Parameter["Part_Number"]),quote_rec_id = self.quote_record_id,quote_revision_rec_id =self.quote_revision_id)
        Sql.RunQuery(update_qty_saqspt)
        update_qty_saqifp = """UPDATE SAQIFP SET SAQSPT.CUSTOMER_ANNUAL_QUANTITY = {qty} FROM SAQSPT  WHERE PART_NUMBER = '{part_number}' and QUOTE_RECORD_ID = '{quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_rec_id}'""".format(qty=str(Parameter["Annual_Quantity"]),part_number=str(Parameter["Part_Number"]),quote_rec_id = self.quote_record_id,quote_revision_rec_id =self.quote_revision_id)
        Sql.RunQuery(update_qty_saqifp)

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

    def periods_insert(self):
        if str(self.service_id) == "Z0108":
            count = Sql.GetFirst("SELECT COUNT(*) as CNT FROM SAQRDS WHERE QUOTE_RECORD_ID = '"+str(self.quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_id)+"' ")
            #INC08642678 - Start - A
            weekCount = 1
            Log.Info('weekCount => ' + str(weekCount))
            if count.CNT==0:
                contract_start_date = str(self.contract_valid_from).split(' ')[0]
                contract_end_date = str(self.contract_valid_to).split(' ')[0]
                start_date = datetime.datetime.strptime(contract_start_date, '%m/%d/%Y')
                end_date = datetime.datetime.strptime(contract_end_date, '%m/%d/%Y')
                diff1 = end_date - start_date
                get_totalweeks,remainder = divmod(diff1.days,7)
                weekCount = get_totalweeks
                countweeks =0
                for index in range(0, get_totalweeks):
                    countweeks += 1
                    billing_date = start_date + datetime.timedelta(days=(7*countweeks))
                    
                    Query = "INSERT SAQRDS (QUOTE_REV_DELIVERY_SCHEDULE_RECORD_ID,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,DELIVERY_DATE,DELIVERY_PERIOD, CPQTABLEENTRYDATEADDED) select CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REV_DELIVERY_SCHEDULE_RECORD_ID,'{quote_id}' as QUOTE_ID,'{contract_rec_id}' as QUOTE_RECORD_ID,'{qt_rev_id}' as QTEREV_ID,'{qt_rev_recid}' as QTEREV_RECORD_ID,'{delivery_date}' as DELIVERY_DATE,'{delivery_period}' as DELIVERY_PERIOD, GETDATE() as CPQTABLEENTRYDATEADDED WHERE NOT EXISTS (SELECT QUOTE_ID FROM SAQRDS WHERE QUOTE_ID = '{quote_id}' AND QTEREV_ID = '{qt_rev_id}' AND DELIVERY_PERIOD = '{delivery_period}')".format(quote_id=self.quote_id,contract_rec_id= self.quote_record_id,qt_rev_id = self.qt_rev_id,qt_rev_recid = self.quote_revision_id,delivery_date =billing_date,delivery_period=index+1)
                    Sql.RunQuery(Query)
            Log.Info('weekCount 2 ==> ' + str(weekCount))
            for item in range(1, weekCount+1):
                x=SqlHelper.GetFirst("""SELECT QUOTE_REV_DELIVERY_SCHEDULE_RECORD_ID, DELIVERY_PERIOD FROM SAQRDS WHERE QUOTE_RECORD_ID='{}' AND QTEREV_RECORD_ID = '{}' AND DELIVERY_PERIOD='{}'""".format(str(self.quote_record_id),str(self.quote_revision_id),str(item)))
                Sql.RunQuery("""Delete FROM SAQRDS WHERE QUOTE_RECORD_ID='{}'  AND QTEREV_RECORD_ID = '{}'AND DELIVERY_PERIOD='{}' AND QUOTE_REV_DELIVERY_SCHEDULE_RECORD_ID != '{}'""".format(str(self.quote_record_id),str(self.quote_revision_id),x.DELIVERY_PERIOD,x.QUOTE_REV_DELIVERY_SCHEDULE_RECORD_ID))
            #INC08642678 - End - A

    def fetch_quotebasic_info(self):
        getDomain = Sql.GetFirst("SELECT top 1 Domain FROM SYCONF (nolock) order by CpqTableEntryId")
        if getDomain:
            self.domain=getDomain.Domain
        
        saqtmt_obj = Sql.GetFirst("SELECT CONTRACT_VALID_FROM,CONTRACT_VALID_TO FROM SAQTMT (NOLOCK) WHERE  QUOTE_ID = '{}'".format(self.quote_id))
        if saqtmt_obj:
            self.contract_valid_from = saqtmt_obj.CONTRACT_VALID_FROM
            self.contract_valid_to = saqtmt_obj.CONTRACT_VALID_TO
                
        saqtrv_obj = Sql.GetFirst("select QUOTE_RECORD_ID,QUOTE_REVISION_RECORD_ID,SALESORG_ID,SALESORG_RECORD_ID,QTEREV_ID,GLOBAL_CURRENCY,GLOBAL_CURRENCY_RECORD_ID from SAQTRV where ACTIVE = 'True' AND QUOTE_ID = '"+str(self.quote_id)+"'")
        if saqtrv_obj:
            self.sales_org_id = saqtrv_obj.SALESORG_ID
            self.sales_recd_id = saqtrv_obj.SALESORG_RECORD_ID
            self.qt_rev_id = saqtrv_obj.QTEREV_ID
            self.quote_revision_id = saqtrv_obj.QUOTE_REVISION_RECORD_ID
            self.quote_record_id = saqtrv_obj.QUOTE_RECORD_ID
            self.global_curr = saqtrv_obj.GLOBAL_CURRENCY
            self.global_curr_recid = saqtrv_obj.GLOBAL_CURRENCY_RECORD_ID
        
        get_party_role = Sql.GetList("SELECT CPQ_PARTNER_FUNCTION, PARTY_ID FROM SAQTIP(NOLOCK) WHERE QUOTE_RECORD_ID = '"+str(self.quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_id)+"' and CPQ_PARTNER_FUNCTION in ('SOLD TO')")
        for keyobj in get_party_role:
            self.account_info[keyobj.CPQ_PARTNER_FUNCTION] = keyobj.PARTY_ID
        
        get_party_role = Sql.GetList("SELECT DISTINCT CPQ_PARTNER_FUNCTION, PARTY_ID FROM SAQTIP(NOLOCK) WHERE QUOTE_RECORD_ID = '"+str(self.quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_id)+"' and CPQ_PARTNER_FUNCTION in ('SHIP TO')")
        self.shipto_list=[]
        self.shipto_list_withoutzero=[]
        ship_to_flag = 0
        for keyobj in get_party_role:
            if ship_to_flag == 0:
                first_ship_to = str(keyobj.PARTY_ID)
                ship_to_flag = 1
            self.shipto_list.append('00'+str(keyobj.PARTY_ID))
            self.shipto_list_withoutzero.append(str(keyobj.PARTY_ID))
        shiptostr=str(self.shipto_list)
        shiptostr=re.sub(r"'",'"',shiptostr)
        self.account_info['SHIP TO']=shiptostr
        
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

        shipto_obj=SqlHelper.GetList("SELECT * FROM SAQTIP WHERE QUOTE_RECORD_ID = '"+str(self.quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_id)+"' AND CPQ_PARTNER_FUNCTION='SHIP TO'")
        self.primaryShipto['SHIP TO'] = first_ship_to
        for ele in shipto_obj:
            if ele.PRIMARY==1 or ele.PRIMARY=='True':
                self.primaryShipto['SHIP TO']=ele.PARTY_ID
        
    def prepare_backup_table(self):
        res = ''.join(str(ele) for ele in self.response)
        cnt = res.count("Material_Eligibility")
        #Log.Info("first response----->2"+str(res))
        if cnt == 1:
            res = re.sub(r'\[',"['",res)
            res= re.sub(r'\]',"']",res)
            res= re.sub(r", ","':'",res)
            res = re.sub(r"\],\[",", ",res)
            res= re.sub(r'\[',"{",res)
            res= re.sub(r'\]',"}",res)
            res = re.sub(r':',' : ',res)
            res= re.sub(r'\}\{',', ',res)
            #Log.Info("sec response----->2"+str(res))
        if self.response:
            response = ','.join(str(ele) for ele in self.response)
            record_count=0
            if cnt ==1:
                response=res
            #Log.Info("PrepareBackuptable----->2"+str(response))
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
            response = re.sub(r"u'Upfront \\u2013","'Upfront -",response)
            response = re.sub(r"u'Upon \\u2013","'Upon -",response)
            response=response.replace("'",'"')
            response=response.replace("???",'-')
            response = re.sub(r'\[|\]|\(|\)','',response)
            #response = re.sub(r'uUpfront','Upfront',response)
            pattern = re.compile(r'(\{[^>]*?\})')
            #pattern2 = re.compile(r'\"([^>]*?)\"\:(\"[^>]*?\")')
            #pattern2 = re.compile(r"\'([^>]*?)\'\s*\:\s*([^>]*?)(?:\,|\})")
            #pattern2 = re.compile(r'([^>]*?)\s*:\s*([^>]*?)(?:\,|\})')
            pattern2 = re.compile(r'(\"[^>]*?\")\s*:\s*(\"[^>]*?\")')
            self.columns = 'QUOTE_RECORD_ID,QTEREV_RECORD_ID'
            value  = '''(\"{}\",\"{}\"'''.format(self.quote_record_id,self.quote_revision_id)
            col_flag = 0
            '''
            for record in re.finditer(pattern, response):
                #rec = re.sub(r'\{|\}','',record.group(1))
                record_count +=1
                rec = record.group(1)
                temp_value = value
                child_temp_value = value
                child_temp_flag=0
                for ele in re.finditer(pattern2,rec):
                    if col_flag == 0:
                        self.columns +=','+ele.group(1)
                    if ele.group(1) == '"PARENT_PART_NUMBER"':
                        self.part_numbers.append(str(ele.group(2)))
                    temp_value +=','+ele.group(2) if ele.group(2) !='' else None
                    if ele.group(1) == '"CHILD_PART_NUMBER"':
                        childvalue = str(ele.group(2))
                        if re.search(r'6000-|W"$',childvalue):
                            child_temp_value +=','+"''"
                            child_temp_flag=1
                    else:
                        child_temp_value +=','+ele.group(2) if ele.group(2) !='' else None
                                
                if child_temp_flag == 1:
                    child_temp_value += ')'
                    child_temp_value = re.sub(r"'",'"',child_temp_value)
                    child_temp_value = re.sub(r'"',"''",child_temp_value)
                    if self.records == '':
                        self.records = child_temp_value
                    else:
                        self.records += ', '+child_temp_value
                    child_temp_value=''
                
                temp_value +=')'
                temp_value = re.sub(r"'",'"',temp_value)
                temp_value = re.sub(r'"',"''",temp_value)
                if self.records == '':
                    self.records = temp_value
                else:
                    self.records += ', '+temp_value
                temp_value =''
            ''' 
            for record in re.finditer(pattern, response):
                record_count +=1
                rec = record.group(1)
                temp_value = value
                for ele in re.finditer(pattern2,rec):
                    if col_flag == 0:
                        self.columns +=','+ele.group(1)
                    if ele.group(1) == '"PARENT_PART_NUMBER"':
                        self.part_numbers.append(str(ele.group(2)))
                    temp_value +=','+ele.group(2) if ele.group(2) !='' else None
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
            #Log.Info("Total Parts List:: " +str(self.part_numbers))
            if record_count >0:
                self._insert_spare_parts()
                self.update_records_saqspt()  
                self.insert_delivery_schedule()
        
    def delete_child_records_6kw(self):
        Trace.Write('Delete Child called!!!')
        Sql.RunQuery("DELETE FROM SAQSPT WHERE PAR_PART_NUMBER != '' AND QUOTE_RECORD_ID = '"+str(self.quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_id)+"' AND SERVICE_ID = '"+str(self.service_id)+"'")
        Sql.RunQuery("UPDATE SAQSPT SET CUSTOMER_ACCEPT_PART='False',CUSTOMER_PARTICIPATE='False' WHERE QUOTE_RECORD_ID = '"+str(self.quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_id)+"' AND SERVICE_ID = '"+str(self.service_id)+"'")

    def bulk_pricing(self):
        Part_num_reprice=Parameter['Selected_id'].replace(" ",'').split(",")
        Part_list=SqlHelper.GetList("SELECT * FROM SAQSPT WHERE QUOTE_RECORD_ID = '"+str(self.quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_id)+"' AND PRICING_STATUS='"+str(Parameter["Pricing_status"]).upper()+"'")
        
    def delete_child_records_6kw_partlist(self,Part_Numbers):
        part_list=tuple(Part_Numbers)
        val=re.sub(r'\,\)',')',str(part_list))
        Sql.RunQuery("DELETE FROM SAQSPT WHERE PAR_PART_NUMBER IN "+str(val)+" AND QUOTE_RECORD_ID = '"+str(self.quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_id)+"' AND SERVICE_ID = '"+str(self.service_id)+"'")
        
    def warning_message_arp_carp(self):
        Warning_Message = Sql.GetFirst("SELECT MESSAGE_TEXT, RECORD_ID, OBJECT_RECORD_ID, MESSAGE_CODE, MESSAGE_LEVEL,MESSAGE_TYPE, OBJECT_RECORD_ID FROM SYMSGS (NOLOCK) WHERE RECORD_ID ='4D34C7DD-765E-4D85-86F7-152C77808E9C' and MESSAGE_LEVEL = 'WARNING'")
        msg_app_txt=''
        Warning_Message = check_active_query= ''
        if Warning_Message and not check_active_query and str(current_prod).upper() == 'SALES':
            msg_app_txt = (
                    '<div  class="col-md-12" id="dirty-flag-warning"><div class="col-md-12 alert-info"><label> <img src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/infor_icon_green.svg" alt="Warning">'
                    + str(Warning_Message.MESSAGE_LEVEL)
                    + " : "
                    + str(Warning_Message.MESSAGE_CODE)
                    + " : "
                    + str(Warning_Message.MESSAGE_TEXT)
                    + "</label></div></div>")
        elif Warning_Message and check_active_query:
            msg_app_txt =""
        return msg_app_txt
    
    def acuring_message(self):
        Sql.RunQuery("""UPDATE SAQTRV SET WORKFLOW_STATUS='PRICING REVIEW',REVISION_STATUS='CFG-CONFIGURING' WHERE QUOTE_RECORD_ID='{QuoteRecordId}' AND QTEREV_RECORD_ID='{rev}'""".format(QuoteRecordId=self.quote_record_id,rev = (self.quote_revision_id)))
        #A055S000P01-20944 - Start - A
        import CQREVSTSCH
        CQREVSTSCH.Revisionstatusdatecapture(self.quote_record_id,self.quote_revision_id)
        #A055S000P01-20944 - End - A
        Sql.RunQuery("""UPDATE SAQSPT SET PRICING_STATUS='ACQUIRING' WHERE QUOTE_RECORD_ID='{QuoteRecordId}' AND QTEREV_RECORD_ID='{rev}'""".format(QuoteRecordId=self.quote_record_id,rev = (self.quote_revision_id)))
        Msg_table_value = Sql.GetFirst("SELECT MESSAGE_TEXT, RECORD_ID, OBJECT_RECORD_ID, MESSAGE_CODE, MESSAGE_LEVEL,MESSAGE_TYPE, OBJECT_RECORD_ID FROM SYMSGS (NOLOCK) WHERE OBJECT_RECORD_ID ='SYOBJ-00272' and MESSAGE_LEVEL = 'WARNING'")
        if Msg_table_value:
            msg_txt = (
                    '<div  class="col-md-12" id="dirty-flag-warning"><div class="col-md-12 alert-info"><label> <img src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/infor_icon_green.svg" alt="Warning">'
                    + str(Msg_table_value.MESSAGE_LEVEL)
                    + " : "
                    + str(Msg_table_value.MESSAGE_CODE)
                    + " : "
                    + str(Msg_table_value.MESSAGE_TEXT)
                    + "</label></div></div>"
                )
        else:
            msg_txt =""
        return msg_txt
    
    def cqpartiflw_iflow(self):
        if Parameter["Part_Number"]:
            update_annual_qty = """UPDATE SAQIFP SET CUSTOMER_ANNUAL_QUANTITY = {annual_qty} FROM SAQIFP  WHERE PART_NUMBER ='{PartNumber}' AND QUOTE_RECORD_ID = '{quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_rec_id}'""".format(annual_qty=Parameter["Annual_Quantity"],PartNumber=Parameter["Part_Number"],quote_rec_id = self.quote_record_id,quote_revision_rec_id =self.quote_revision_id)
            Sql.RunQuery(update_annual_qty)
        CQPARTIFLW.iflow_pricing_call(str(User.UserName),str(self.quote_id),str(self.quote_revision_id),str(Parameter["Part_Number"]))    

    def req_data(self):
        self.oauthURL='https://oauth2.c-1404e87.kyma.shoot.live.k8s-hana.ondemand.com/oauth2/token'
        if (self.domain).lower() == 'appliedmaterials_tst':
            self.requestdata = "client_id=application&grant_type=client_credentials&username=ef66312d-bf20-416d-a902-4c646a554c10&password=Ieo.6c8hkYK9VtFe8HbgTqGev4&scope=fpmxcsafeaccess"
            self.authorization = "Basic ZWY2NjMxMmQtYmYyMC00MTZkLWE5MDItNGM2NDZhNTU0YzEwOkllby42Yzhoa1lLOVZ0RmU4SGJnVHFHZXY0"
        elif (self.domain).lower() == 'appliedmaterials_sit':
            self.requestdata = "client_id=application&grant_type=client_credentials&username=128e01c3-eaf9-488e-96f9-387bf1d19f45&password=3WpnvmIpJoGHfPKHCVTdshDIVX&scope=fpmxcsafeaccess"
            self.authorization = "Basic MTI4ZTAxYzMtZWFmOS00ODhlLTk2ZjktMzg3YmYxZDE5ZjQ1OjNXcG52bUlwSm9HSGZQS0hDVlRkc2hESVZY"
        elif (self.domain).lower() == 'appliedmaterials_uat':
            self.requestdata = "client_id=application&grant_type=client_credentials&username=b1673396-c4e6-4743-b3c8-b9d0aeb441ab&password=GheMd99iXbXL4GlaZC7huH9lZj&scope=nodeqfpmaccess"
            self.authorization = "Basic YjE2NzMzOTYtYzRlNi00NzQzLWIzYzgtYjlkMGFlYjQ0MWFiOkdoZU1kOTlpWGJYTDRHbGFaQzdodUg5bFpq"
        elif (self.domain).lower() == 'appliedmaterials_opt':
            self.requestdata = "client_id=application&grant_type=client_credentials&username=6844eae5-0abc-4444-ac1e-e90dab8ec0eb&password=oYvfEeKkBC0ohWP2KcuSRg9ufv&scope=ytenantfpmsafe"
            self.authorization = "Basic Njg0NGVhZTUtMGFiYy00NDQ0LWFjMWUtZTkwZGFiOGVjMGViOm9ZdmZFZUtrQkMwb2hXUDJLY3VTUmc5dWZ2"
            self.oauthURL='https://oauth2.c-68c90e5.kyma.ondemand.com/oauth2/token'
        elif (self.domain).lower() == 'appliedmaterials_prd':
            self.requestdata = "client_id=80f033a4-1fea-466b-8bfa-ea6296951431&grant_type=client_credentials&client_secret=mA2ex2xw5Ltp6uokbYQFR8A0_R&scope=fpmpartssafeaccess"
            self.authorization = ""
            self.oauthURL='https://oauth2.c-3ae981f.kyma.ondemand.com/oauth2/token'
    
    def oauth_token(self):
        self.req_data()
        webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/x-www-form-urlencoded"
        webclient.Headers[System.Net.HttpRequestHeader.Authorization] = self.authorization
        response = webclient.UploadString(str(self.oauthURL),str(self.requestdata))
        response=response.replace("null",'""')
        response=eval(response)	
        self.auth="Bearer"+' '+str(response['access_token'])
        
    def loadpartsfromhana(self):
        shiptostrs=str(self.shipto_list_withoutzero)
        shiptostrs=re.sub(r"\[",'(',shiptostrs)
        shiptostrs=re.sub(r"\]",')',shiptostrs)
        Log.Info('2159CQPARTS----------'+str(User.UserName)+str(self.account_info.get('SOLD TO'))+str(self.account_info.get('SHIP TO')))
        Sql.RunQuery("DELETE FROM SAQSPT WHERE SHPACCOUNT_ID NOT IN "+str(shiptostrs)+" AND QUOTE_RECORD_ID = '"+str(self.quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_id)+"'")

        Sql.RunQuery("DELETE FROM SAQIFP WHERE SHPACCOUNT_ID NOT IN "+str(shiptostrs)+" AND QUOTE_RECORD_ID = '"+str(self.quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_id)+"' ")

        CQIFLSPARE.iflow_pullspareparts_call(str(User.UserName),str(self.account_info.get('SOLD TO')),str(self.account_info.get('SHIP TO')),self.sales_org_id,self.pricelist,self.pricegroup,'Yes','Yes',Parameter["Part_Number"],self.cvf,self.cvt,self.quote_id,self.quote_revision_id,self.auth)
    def excel_backup_del(self):
        spare_temp_table_name ="EXCELUPDATE_SAQSPT_{}".format(self.quote_id)
        excel_bkp=SqlHelper.GetFirst("SELECT COUNT(*) AS CNT FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME ='{}'".format(str(spare_temp_table_name)))
        if excel_bkp.CNT == 1:
	        spare_parts_temp_table_drop = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(spare_temp_table_name)+"'' ) BEGIN DROP TABLE "+str(spare_temp_table_name)+" END  ' ")
#Received Parameters from CPI/Other Scripts.
Parameter = {}
try:
    Parameter["Action"] = Param.CPQ_Columns["Action"]
except Exception:
    Parameter["Action"] = 'Default'
try:
    Parameter["Annual_Quantity"] = Param.CPQ_Columns["Annual_Quantity"]
except Exception:
    Parameter["Annual_Quantity"] = 'NULL'
try:
    Parameter["Part_Number"] = Param.CPQ_Columns["Part_number"]
except Exception:
    Parameter["Part_Number"] = ''
try:
    Parameter["Delete_Partlist"] = Param.CPQ_Columns["Delete_Partlist"]
except Exception:
    Parameter["Delete_Partlist"] = ""
try:
    Parameter["Pricing_status"] = Param.CPQ_Columns["Selected_id_status"]
except Exception:
    Parameter["Pricing_status"] = ""
try:
    Parameter["Selected_id"] = Param.CPQ_Columns["Selected_id"]
except Exception:
    Parameter["Selected_id"] = ""
try:
    current_prod = Product.Name
except:
    current_prod = "SALES"

#Object Creation based on the class. Most of the functions called via self object.
fpm_obj = SyncFPMQuoteAndHanaDatabase()
fpm_obj.fetch_quotebasic_info()
if Parameter["Action"] == 'Price':
    fpm_obj.cqpartiflw_iflow()
    ApiResponse = ApiResponseFactory.JsonResponse(fpm_obj.acuring_message())
elif Parameter["Action"] == 'Reprice':
    if (len(Parameter["Selected_id"])> 0) or (len(Parameter["Pricing_status"])>0):
        fpm_obj.bulk_pricing()
    else:
        fpm_obj.reprice_update_qty()
        fpm_obj.cqpartiflw_iflow()
elif Parameter["Action"] == 'LoadParts':
    fpm_obj.oauth_token()
    fpm_obj.loadpartsfromhana()
    fpm_obj.excel_backup_del()
elif Parameter["Action"] == 'Delete':
    if Parameter["Delete_Partlist"]:
        fpm_obj.delete_child_records_6kw_partlist(Parameter["Delete_Partlist"])
    else:
        fpm_obj.delete_child_records_6kw()
elif Param.CPQ_Columns["QuoteID"] and Parameter["Action"] == 'Default':
    fpm_obj.prepare_backup_table()
    fpm_obj.periods_insert()
    #fpm_obj.excel_backup_del()

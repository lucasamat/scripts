# =========================================================================================================================================
#   __script_name : QTPOSTPTPR.PY(AMAT)
#   __script_description : THIS SCRIPT IS USED TO UPDATE PART PRICING RESPONCE FROM CPS TO CPQ.
#   __primary_author__ : SURIYANARAYANAN
#   __create_date :05/29/2022
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED 
# =========================================================================================================================================
import time
import re
from SYDATABASE import SQL
Sql = SQL()

class FpmPriceUpdate:
    def __init__(self):
        self.domain=self.sales_org_id=self.sales_recd_id=self.qt_rev_id=self.quote_revision_id=self.quote_record_id=self.global_curr=self.global_curr_recid=self.service_id=self.batch_group_record_id=self.exch_rate=self.exch=self.quote_id=self.tax_percentage=''
        self.tax_percentage=0
        self.price = self.insert_data = []
        self.odccflagstatus={}
        self.normalizethexmldata()
        for i in self.price:    
            Itemidinfo = str(i["itemId"]).split(";")
            self.quote_id = str(Itemidinfo[1])
            break
        Log.Info('self.quote_id => ' + str(self.quote_id))
        
    def fetch_quotebasic_info(self):
        saqtrv_obj = Sql.GetFirst("select QUOTE_RECORD_ID,QUOTE_REVISION_RECORD_ID,QTEREV_ID,EXCHANGE_RATE_TYPE,EXCHANGE_RATE from SAQTRV where ACTIVE = 'True' AND QUOTE_ID = '"+str(self.quote_id)+"'")
        if saqtrv_obj:
            self.qt_rev_id = saqtrv_obj.QTEREV_ID
            self.quote_revision_id = saqtrv_obj.QUOTE_REVISION_RECORD_ID
            self.quote_record_id = saqtrv_obj.QUOTE_RECORD_ID
            self.exch_rate_type = saqtrv_obj.EXCHANGE_RATE_TYPE
            self.exch_rate = saqtrv_obj.EXCHANGE_RATE
        
        saqtsv_obj = Sql.GetFirst("SELECT SERVICE_ID FROM SAQTSV where SERVICE_ID IN('Z0110','Z0100','Z0108','Z0101') AND QUOTE_RECORD_ID = '"+str(self.quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_id)+"'")
        if saqtsv_obj:
            self.service_id = saqtsv_obj.SERVICE_ID
        
        cust_participate = Sql.GetList("SELECT PART_NUMBER,ODCC_FLAG FROM SAQSPT WHERE QUOTE_RECORD_ID = '"+str(self.quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_id)+"'")
        for key in cust_participate:
            self.odccflagstatus[key.PART_NUMBER]=key.ODCC_FLAG

        get_display_decimal = Sql.GetFirst("SELECT DISPLAY_DECIMAL_PLACES FROM PRCURR JOIN SAQTRV (NOLOCK) ON PRCURR.CURRENCY_RECORD_ID = SAQTRV.GLOBAL_CURRENCY_RECORD_ID WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{rev}'".format(QuoteRecordId = self.quote_record_id,rev =self.quote_revision_id))
        self.decimal_places = 2
        if get_display_decimal:
            self.decimal_places = get_display_decimal.DISPLAY_DECIMAL_PLACES
        self.decimal_format = "{:." + str(self.decimal_places) + "f}"
        
    def normalizethexmldata(self):
        if hasattr(Param, 'CPQ_Columns'): 
            rebuilt_data = {}
            for table_dict in Param.CPQ_Columns: 
                tbl = str(table_dict.Key)
                colu_Info = {}
                uu = []         
                for record_dict in table_dict.Value:
                    tyty = str(type(record_dict))
                    if str(tyty) == "<type 'KeyValuePair[str, object]'>":
                        j = record_dict
                        j_Valu = j.Value
                        if "&#34;" in j_Valu:
                            j_Valu =  j_Valu.replace("&#34;","\"")
                        if "&#39;" in j_Valu:
                            j_Valu = j_Valu.replace("&#39;" , "\'")
                        if "&#92;" in j_Valu:
                            j_Valu = j_Valu.replace("&#92;" , "\\")                 
                        colu_Info[str(j.Key)] = j_Valu
                    else:
                        colu_Info1 = {}
                        for j in record_dict:
                            j_Valu = j.Value    
                            j_key = str(j.Key)
                            if "&#34;" in j_Valu:
                                j_Valu =  j_Valu.replace("&#34;","\"")
                            if "&#39;" in j_Valu:
                                j_Valu = j_Valu.replace("&#39;" , "\'")
                            if "&#92;" in j_Valu:
                                j_Valu = j_Valu.replace("&#92;" , "\\") 
                            colu_Info1[str(j.Key)] = j_Valu             
                        uu.append(colu_Info1)
                if len(colu_Info) !=  0:    
                    rebuilt_data[tbl] = [colu_Info]
                if len(uu) !=  0:   
                    rebuilt_data[tbl] = uu
            response = rebuilt_data
            for root, value in response.items():
                for root1 in value:
                    for inv in root1:
                        if inv == "items":
                            self.price = root1[inv]          
                            break
            self.batch_group_record_id = str(Guid.NewGuid()).upper()
            if str(type(self.price)) == "<type 'Dictionary[str, object]'>":
                self.price = [self.price]
    def fetch_priceinfo(self):
        for i in self.price:    
            Itemidinfo = str(i["itemId"]).split(";")
            QUOTE = str(Itemidinfo[1])
            part_qty=Itemidinfo[2]
            prefixZero = Itemidinfo[4] or ''
            isocode_salesuom = str(Itemidinfo[5]) or 'EA'
            numerator =  int(Itemidinfo[6]) or 1
            Taxrate = '0.00'
            core_credit_amount = ''
            for condition in i['conditions']:
                #Log.Info(str(condition))
                if condition['conditionType'] == "ZERU":
                    core_credit_amount = self.decimal_format.format(float(condition['conditionRate']))
                if condition['conditionType'] in ("ZWSC","ZWST"):
                    self.tax_percentage = condition['conditionRate']
                if condition['conditionTypeDescription'] == "Net Value 2":
                    self.ancliary_netPrice = condition['conditionRate']
                    self.ancliary_netValue = condition['conditionValue']
            #Log.Info("Z0100=> AXRATE"+str(self.ancliary_netPrice))
            #Log.Info("Z0100=> AXRATEVAL"+str(self.ancliary_netValue))    
            '''if self.odccflagstatus.get(str(Itemidinfo[0])) in ('CCM','CCO'): #UPON Discount
                zghs_coreamt=0
                core_credit_amount=0
                for condition in i['conditions']:
                    if condition['conditionType'] == "ZEEB":
                        core_credit_amount = condition['conditionValue']
                    elif condition['conditionType'] == "ZEEC":
                        core_credit_amount = condition['conditionValue']
                    elif condition['conditionType'] == "ZGHS":
                        zghs_coreamt = condition['conditionValue']
                if core_credit_amount > 0:
                    core_credit_amount = float(core_credit_amount) + float(zghs_coreamt)	
            elif self.odccflagstatus.get(str(Itemidinfo[0])) in ('CUM','CUO'): #UPFRONT Discount
                for condition in i['conditions']:
                    if condition['conditionType'] == "ZCCA":
                        core_credit_amount = condition['conditionValue']
                        break
                    elif condition['conditionType'] == "ZCCP":
                        core_credit_amount = condition['conditionValue']
                        break
            '''
            if len(prefixZero)>0:
                Itemidinfo[0]=re.sub(prefixZero,'',Itemidinfo[0])
            
            salesUOMflag=0
            if str(i["netPriceUnit"]) != str(isocode_salesuom) and int(float((i["netPriceUnitValue"]))) == 1:
                i["netPrice"] = float(i["netPrice"]) * float(numerator)
                salesUOMflag=1
            elif str(i["netPriceUnit"]) != str(isocode_salesuom) and int(float(i["netPriceUnitValue"])) > 1:
                i["netPrice"] = (float(i["netPrice"]) / int(float((i["netPriceUnitValue"])))) * float(numerator)
                salesUOMflag=1
            
            if salesUOMflag==1:
                i["netPrice"]=str(i["netPrice"])
            
            if self.service_id in('Z0100','Z0101'):
                self.insert_data.append((str(Guid.NewGuid()).upper(), Itemidinfo[0], Itemidinfo[-6],self.ancliary_netPrice, 'IN PROGRESS', QUOTE, self.quote_record_id, self.batch_group_record_id,str(Taxrate),str(core_credit_amount),i["taxValue"],self.ancliary_netValue,i["grossValue"],i["freightValue"],self.ancliary_netPrice,i["netPriceUnit"],i["netPriceUnitValue"],self.quote_revision_id))
            else:
                self.insert_data.append((str(Guid.NewGuid()).upper(), Itemidinfo[0], Itemidinfo[-6], i["netPrice"], 'IN PROGRESS', QUOTE, self.quote_record_id, self.batch_group_record_id,str(Taxrate),str(core_credit_amount),i["taxValue"],i["netValue"],i["grossValue"],i["freightValue"],i["netPrice"],i["netPriceUnit"],i["netPriceUnitValue"],self.quote_revision_id))
                
    def batch_insert(self):
        Sql.RunQuery("INSERT INTO SYSPBT (BATCH_RECORD_ID, SAP_PART_NUMBER, QUANTITY, UNIT_PRICE, BATCH_STATUS, QUOTE_ID, QUOTE_RECORD_ID, BATCH_GROUP_RECORD_ID,TAXRATE,CORE_CREDIT_PRICE,TAX_VALUE,NET_VALUE,GROSS_VALUE,FREIGHT_VALUE,NET_PRICE,NET_PRICE_UNIT,NET_PRICE_UNIT_VALUE,QTEREV_RECORD_ID) VALUES {}".format(', '.join(map(str, self.insert_data))))
    
    def service_validation(self):
        if self.service_id in('Z0110','Z0108'):
            self.fpm_batchupdate()
        elif self.service_id in('Z0100','Z0101'):
            self.ancillary_batchupdate()
    
    def fpm_batchupdate(self):
        
        Sql.RunQuery("""UPDATE SAQSPT SET PRICING_STATUS = CASE WHEN SYSPBT.UNIT_PRICE IS NULL THEN 'ERROR' WHEN SYSPBT.UNIT_PRICE = '0.00000' THEN 'ERROR' ELSE 'ACQUIRED' END, UNIT_PRICE = SYSPBT.UNIT_PRICE ,CORE_CREDIT_PRICE = CASE WHEN SYSPBT.CORE_CREDIT_PRICE = '' THEN NULL ELSE SYSPBT.CORE_CREDIT_PRICE END,TAX_AMOUNT_INGL_CURR=SYSPBT.TAX_VALUE,EXTENDED_UNIT_PRICE = SYSPBT.NET_VALUE, TAX_PERCENTAGE = CASE WHEN {TaxPercent}=0 THEN NULL ELSE {TaxPercent} END FROM SAQSPT JOIN SYSPBT (NOLOCK) ON SYSPBT.SAP_PART_NUMBER = SAQSPT.PART_NUMBER AND SYSPBT.QUOTE_RECORD_ID = SAQSPT.QUOTE_RECORD_ID WHERE SAQSPT.QUOTE_RECORD_ID = '{QuoteRecordId}'  AND SAQSPT.QTEREV_RECORD_ID = '{rev}' AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}'""".format(BatchGroupRecordId=self.batch_group_record_id, QuoteRecordId=self.quote_record_id,rev =self.quote_revision_id,TaxPercent=self.tax_percentage))
        
        Sql.RunQuery("""UPDATE SAQIFP SET PRICING_STATUS = CASE WHEN SYSPBT.UNIT_PRICE IS NULL THEN 'ERROR' WHEN SYSPBT.UNIT_PRICE = '0.00000' THEN 'ERROR' ELSE 'ACQUIRED' END,CORE_CREDIT_PRICE = CASE WHEN SYSPBT.CORE_CREDIT_PRICE = '' THEN NULL ELSE SYSPBT.CORE_CREDIT_PRICE END,TAX_AMOUNT_INGL_CURR = SYSPBT.TAX_VALUE,UNIT_PRICE_INGL_CURR = SYSPBT.UNIT_PRICE,EXTPRI_INGL_CURR = SYSPBT.NET_VALUE, TAX_PERCENTAGE = CASE WHEN {TaxPercent}=0 THEN NULL ELSE {TaxPercent} END FROM SAQIFP JOIN SYSPBT (NOLOCK) ON SYSPBT.SAP_PART_NUMBER = SAQIFP.PART_NUMBER AND SYSPBT.QUOTE_RECORD_ID = SAQIFP.QUOTE_RECORD_ID WHERE  SAQIFP.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQIFP.QTEREV_RECORD_ID = '{rev}' AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}'""".format(BatchGroupRecordId=self.batch_group_record_id, QuoteRecordId=self.quote_record_id,rev =self.quote_revision_id,TaxPercent=self.tax_percentage))
        
        GetEquipment_count = Sql.GetFirst("SELECT COUNT(CpqTableEntryId) AS CNT FROM SAQRIT WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{rev}' AND SERVICE_ID = '{SERVICE_ID}'".format(QuoteRecordId = self.quote_record_id,rev =self.quote_revision_id,SERVICE_ID=self.service_id))
        
        if GetEquipment_count.CNT > 0:
            Sql.RunQuery("DELETE FROM SAQSPT (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID= '{}' AND SERVICE_ID = 'Z0108' AND UNIT_PRICE <= 50 AND CUSTOMER_ANNUAL_QUANTITY <= 9".format(self.quote_record_id,self.quote_revision_id))
                
            Sql.RunQuery("DELETE FROM SAQIFP (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID= '{}' AND SERVICE_ID = 'Z0108' AND UNIT_PRICE <= 50 AND ANNUAL_QUANTITY <= 9".format(self.quote_record_id,self.quote_revision_id))

            Sql.RunQuery("DELETE FROM SAQSPT (NOLOCK) WHERE CUSTOMER_ANNUAL_QUANTITY<10 AND UNIT_PRICE <50 AND SCHEDULE_MODE='ON REQUEST' AND DELIVERY_MODE='OFFSITE' AND SERVICE_ID='Z0110' AND  QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(self.quote_record_id,self.quote_revision_id))
            
            Sql.RunQuery("DELETE FROM SAQIFP (NOLOCK) WHERE ANNUAL_QUANTITY<10 AND UNIT_PRICE <50 AND SCHEDULE_MODE='ON REQUEST' AND DELIVERY_MODE='OFFSITE' AND SERVICE_ID='Z0110' AND  QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(self.quote_record_id,self.quote_revision_id))
                
            
            GetSum = Sql.GetFirst( "SELECT SUM(UNIT_PRICE)/"+str(GetEquipment_count.CNT)+" AS TOTAL_UNIT, SUM(EXTENDED_UNIT_PRICE)/"+str(GetEquipment_count.CNT)+"  AS TOTAL_EXT, SUM(TAX_AMOUNT_INGL_CURR)/"+str(GetEquipment_count.CNT)+"  AS TOTAL_TAX  FROM SAQSPT WHERE  QUOTE_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID = '{}' AND (CUSTOMER_ANNUAL_QUANTITY IS NOT NULL AND CUSTOMER_ANNUAL_QUANTITY > 0) AND (PART_NUMBER NOT LIKE '6000-%' AND PART_NUMBER NOT LIKE '%W')".format( self.quote_id,self.quote_revision_id, self.service_id))
            
            Sql.RunQuery("""UPDATE SAQRIT SET STATUS='ACQUIRED', UNIT_PRICE_INGL_CURR = '{total_unit}', YEAR_1_INGL_CURR='{total_net}', TOTAL_AMOUNT_INGL_CURR = {total_net} + {total_tax}, ESTVAL_INGL_CURR ='{total_net}', TAX_AMOUNT_INGL_CURR = '{total_tax}', ESTIMATED_VALUE = {total_net} FROM SAQRIT WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID='{rev}' AND SERVICE_ID = '{SERVICE_ID}'""".format(total_tax = GetSum.TOTAL_TAX,total_unit=GetSum.TOTAL_UNIT,total_net = GetSum.TOTAL_EXT, QuoteRecordId=self.quote_record_id,rev =self.quote_revision_id,SERVICE_ID=self.service_id)) 
            
            Sql.RunQuery("""UPDATE SAQTRV SET SALES_PRICE_INGL_CURR = '{total_unit}', TOTAL_AMOUNT_INGL_CURR = {total_net} + {total_tax}, TAX_AMOUNT_INGL_CURR ='{total_tax}', ESTVAL_INGL_CURR = {total_net} FROM SAQTRV WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID='{rev}'""".format(total_unit=GetSum.TOTAL_UNIT,total_net = GetSum.TOTAL_EXT,total_tax = GetSum.TOTAL_TAX,  QuoteRecordId=self.quote_record_id,rev =self.quote_revision_id))
            
            Sql.RunQuery("""UPDATE SAQICO SET TENVGC = '{total_net}' FROM SAQICO WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID='{rev}'""".format(total_net = GetSum.TOTAL_EXT, QuoteRecordId=self.quote_record_id,rev =self.quote_revision_id))
            
            Sql.RunQuery("""UPDATE SAQRIS SET ESTIMATED_VALUE = {total_net}, ESTVAL_INGL_CURR = {total_net}, NET_PRICE_INGL_CURR = '{total_unit}', TOTAL_AMOUNT_INGL_CURR ={total_net} + {total_tax}, TAX_AMOUNT_INGL_CURR ='{total_tax}' FROM SAQRIS (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID='{rev}'""".format(total_unit=GetSum.TOTAL_UNIT,total_net = GetSum.TOTAL_EXT,total_tax = GetSum.TOTAL_TAX, QuoteRecordId=self.quote_record_id,rev =self.quote_revision_id))
            
            getstatus=SqlHelper.GetFirst("""SELECT COUNT(PRICING_STATUS) AS CNT FROM SAQSPT WHERE QUOTE_RECORD_ID='{QuoteRecordId}' AND PRICING_STATUS='ERROR' AND QTEREV_RECORD_ID='{rev}'""".format(QuoteRecordId=self.quote_record_id,rev =self.quote_revision_id))
            if getstatus.CNT>0:
                Sql.RunQuery("""UPDATE SAQICO SET STATUS='ERROR' WHERE QUOTE_RECORD_ID='{QuoteRecordId}' AND QTEREV_RECORD_ID='{rev}'""".format(QuoteRecordId=self.quote_record_id,rev =self.quote_revision_id))
                Sql.RunQuery("""UPDATE SAQTRV SET WORKFLOW_STATUS='PRICING REVIEW',REVISION_STATUS='PRR-ON HOLD PRICING' WHERE QUOTE_RECORD_ID='{QuoteRecordId}' AND QTEREV_RECORD_ID='{rev}'""".format(QuoteRecordId=self.quote_record_id,rev =self.quote_revision_id))
                Sql.RunQuery("""UPDATE SAQRIT SET STATUS='ERROR' WHERE QUOTE_RECORD_ID='{QuoteRecordId}' AND QTEREV_RECORD_ID='{rev}'""".format(QuoteRecordId=self.quote_record_id,rev =self.quote_revision_id))
            else:
                getstatus=SqlHelper.GetFirst("""SELECT COUNT(PRICING_STATUS) AS CNT FROM SAQSPT WHERE QUOTE_RECORD_ID='{QuoteRecordId}' AND PRICING_STATUS IN('ERROR','ACQUIRING','NOT PRICED') AND QTEREV_RECORD_ID='{rev}'""".format(QuoteRecordId=self.quote_record_id,rev =self.quote_revision_id))
                if getstatus.CNT==0:
                    Sql.RunQuery("""UPDATE SAQICO SET STATUS='ACQUIRED' WHERE QUOTE_RECORD_ID='{QuoteRecordId}' AND QTEREV_RECORD_ID='{rev}'""".format(QuoteRecordId=self.quote_record_id,rev =self.quote_revision_id))
                    Sql.RunQuery("""UPDATE SAQTRV SET WORKFLOW_STATUS='PRICING',REVISION_STATUS='PRI-PRICING' WHERE QUOTE_RECORD_ID='{QuoteRecordId}' AND QTEREV_RECORD_ID='{rev}'""".format(QuoteRecordId=self.quote_record_id,rev =self.quote_revision_id))
                    Sql.RunQuery("""UPDATE SAQRIT SET STATUS='ACQUIRED' WHERE QUOTE_RECORD_ID='{QuoteRecordId}' AND QTEREV_RECORD_ID='{rev}'""".format(QuoteRecordId=self.quote_record_id,rev =self.quote_revision_id))
                
    def ancillary_batchupdate(self):
        #HPQC-312 starts
        quote_items_list = []
        # try:
        #     if self.price and len(self.price) > 0:  
        #         Itemidinfo = str(self.price[0]["itemId"]).split(";")
        #         QUOTE = str(Itemidinfo[1])
        #         Log.Info("QTPOSTPTPR -> QUOTE ->"+str(QUOTE))
        #         get_billing_type = Sql.GetFirst("select ENTITLEMENT_XML,SERVICE_ID from SAQTSE where QUOTE_ID = '{QuoteId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' and SERVICE_ID = 'Z0100'".format(QuoteId=QUOTE, RevisionRecordId=self.quote_revision_id))
        #         if get_billing_type:
        #             updateentXML = get_billing_type.ENTITLEMENT_XML
        #             pattern_tag = re.compile(r'(<QUOTE_ITEM_ENTITLEMENT>[\w\W]*?</QUOTE_ITEM_ENTITLEMENT>)')
        #             pattern_id = re.compile(r'<ENTITLEMENT_ID>AGS_Z0100_PQB_BILTYP</ENTITLEMENT_ID>')
        #             pattern_name = re.compile(r'<ENTITLEMENT_DISPLAY_VALUE>([^>]*?)</ENTITLEMENT_DISPLAY_VALUE>')
        #             for m in re.finditer(pattern_tag, updateentXML):
        #                 sub_string = m.group(1)
        #                 get_ent_id = re.findall(pattern_id,sub_string)
        #                 get_ent_val= re.findall(pattern_name,sub_string)
        #                 if get_ent_id:
        #                     self.get_billing_type_val = str(get_ent_val[0])
        #                     break
        # except:
        #     self.get_billing_type_val = ''

    
    
        Sql.RunQuery("""UPDATE SAQRSP SET PRICING_STATUS = CASE WHEN SYSPBT.UNIT_PRICE IS NULL THEN 'ERROR' WHEN SYSPBT.UNIT_PRICE = '0.00000' THEN 'ERROR' ELSE 'ACQUIRED' END ,UNIT_PRICE_INGL_CURR = SYSPBT.UNIT_PRICE ,EXTENDED_PRICE_INGL_CURR = SYSPBT.NET_VALUE FROM SAQRSP JOIN SYSPBT (NOLOCK) ON SYSPBT.SAP_PART_NUMBER = SAQRSP.PART_NUMBER AND SYSPBT.QUOTE_RECORD_ID = SAQRSP.QUOTE_RECORD_ID AND SYSPBT.QTEREV_RECORD_ID = SAQRSP.QTEREV_RECORD_ID WHERE SAQRSP.QUANTITY = SYSPBT.QUANTITY AND SAQRSP.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRSP.QTEREV_RECORD_ID = '{rev}' AND SAQRSP.SERVICE_ID = 'Z0100' AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}'""".format(BatchGroupRecordId=self.batch_group_record_id, QuoteRecordId=self.quote_record_id,rev = self.quote_revision_id))
        # Log.Info("""UPDATE SAQRSP SET PRICING_STATUS = CASE WHEN SYSPBT.UNIT_PRICE IS NULL THEN 'ERROR' WHEN SYSPBT.UNIT_PRICE = '0.00000' THEN 'ERROR' ELSE 'ACQUIRED' END ,UNIT_PRICE_INGL_CURR = SYSPBT.UNIT_PRICE ,EXTENDED_PRICE_INGL_CURR = SYSPBT.NET_VALUE FROM SAQRSP JOIN SYSPBT (NOLOCK) ON SYSPBT.SAP_PART_NUMBER = SAQRSP.PART_NUMBER AND SYSPBT.QUOTE_RECORD_ID = SAQRSP.QUOTE_RECORD_ID AND SYSPBT.QTEREV_RECORD_ID = SAQRSP.QTEREV_RECORD_ID WHERE SAQRSP.QUANTITY = SYSPBT.QUANTITY AND SAQRSP.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRSP.QTEREV_RECORD_ID = '{rev}' AND SAQRSP.SERVICE_ID = 'Z0100' AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}'""".format(BatchGroupRecordId=self.batch_group_record_id, QuoteRecordId=self.quote_record_id,rev = self.quote_revision_id))
        #STATUS UPDATE
        getstatus=SqlHelper.GetFirst("""SELECT COUNT(PRICING_STATUS) AS CNT FROM SAQRSP WHERE QUOTE_RECORD_ID='{QuoteRecordId}' AND PRICING_STATUS IN('ERROR','ACQUIRING','NOT PRICED') AND QTEREV_RECORD_ID='{rev}'""".format(QuoteRecordId=self.quote_record_id,rev =self.quote_revision_id))
        if getstatus.CNT > 0:
            Sql.RunQuery("""UPDATE SAQTRV SET WORKFLOW_STATUS='CONFIGURE',REVISION_STATUS='CFG-CONFIGURING' WHERE QUOTE_RECORD_ID='{QuoteRecordId}' AND QTEREV_RECORD_ID='{rev}'""".format(QuoteRecordId=self.quote_record_id,rev =self.quote_revision_id))

        
        ##net price update
        GetEquipment_count = Sql.GetFirst("SELECT COUNT(SAQRIT.CpqTableEntryId) AS CNT FROM SAQRIT (NOLOCK) INNER JOIN SAQSCE (NOLOCK) ON SAQRIT.EQUIPMENT_ID = SAQSCE.EQUIPMENT_ID AND SAQRIT.QUOTE_RECORD_ID = SAQSCE.QUOTE_RECORD_ID AND SAQRIT.QTEREV_RECORD_ID  =SAQSCE.QTEREV_RECORD_ID AND SAQRIT.SERVICE_ID = SAQSCE.SERVICE_ID WHERE SAQRIT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID = '{rev}' AND SAQRIT.SERVICE_ID = 'Z0100' AND CNSMBL_ENT <> 'Included' AND CONFIGURATION_STATUS = 'COMPLETE'".format(QuoteRecordId = self.quote_record_id,rev =self.quote_revision_id))
        if GetEquipment_count:
            GetSum = Sql.GetFirst( "SELECT SUM(UNIT_PRICE_INGL_CURR)/"+str(GetEquipment_count.CNT)+" AS TOTAL_UNIT, SUM(EXTENDED_PRICE_INGL_CURR)/"+str(GetEquipment_count.CNT)+"  AS TOTAL_EXT FROM SAQRSP (NOLOCK) WHERE QUOTE_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID = 'Z0100'".format( self.quote_id,self.quote_revision_id))
            # if self.get_billing_type_val.upper() == 'VARIABLE':
            #     pricing_field_doc = 'TENVDC'
            #     pricing_field_annualized = "TENVGC"
            # else:
            #     pricing_field_doc= 'TNTVDC'
            #     pricing_field_annualized = "TNTVGC"
            if GetSum:
                if GetSum.TOTAL_UNIT and GetSum.TOTAL_EXT:
                    Sql.RunQuery("""UPDATE SAQRIT SET UNIT_PRICE_INGL_CURR = {total_unit}  FROM SAQRIT (NOLOCK) INNER JOIN SAQSCE (NOLOCK) ON SAQRIT.EQUIPMENT_ID = SAQSCE.EQUIPMENT_ID AND SAQRIT.QUOTE_RECORD_ID = SAQSCE.QUOTE_RECORD_ID AND SAQRIT.QTEREV_RECORD_ID  =SAQSCE.QTEREV_RECORD_ID AND SAQRIT.SERVICE_ID = SAQSCE.SERVICE_ID
                    WHERE SAQRIT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID='{rev}' AND SAQRIT.SERVICE_ID = 'Z0100' AND CNSMBL_ENT <> 'Included' AND CONFIGURATION_STATUS = 'COMPLETE'""".format(total_unit=GetSum.TOTAL_UNIT, QuoteRecordId=self.quote_record_id,rev =self.quote_revision_id))
                    ##saqico insert 
                    # Sql.RunQuery("""UPDATE SAQICO 
                    # SET {pricing_field} =({total_net} /CASE WHEN DATEDIFF(day,SAQRIT.CONTRACT_VALID_FROM, SAQRIT.CONTRACT_VALID_TO) = 0 THEN 1 ELSE (DATEDIFF(day,SAQRIT.CONTRACT_VALID_FROM, SAQRIT.CONTRACT_VALID_TO) +1)END ) * CNTDAY,
                    # {pricing_field_doc} = (({total_net} /CASE WHEN DATEDIFF(day,SAQRIT.CONTRACT_VALID_FROM, SAQRIT.CONTRACT_VALID_TO) = 0 THEN 1 ELSE DATEDIFF(day,SAQRIT.CONTRACT_VALID_FROM, SAQRIT.CONTRACT_VALID_TO) END ) * CNTDAY )*{exch_rate},
                    # SAQICO.STATUS = 'ACQUIRED' 
                    # FROM SAQICO (NOLOCK) 
                    # INNER JOIN SAQRIT ON SAQRIT.QUOTE_RECORD_ID = SAQICO.QUOTE_RECORD_ID AND SAQRIT.QTEREV_RECORD_ID = SAQICO.QTEREV_RECORD_ID AND SAQRIT.SERVICE_ID = SAQICO.SERVICE_ID AND SAQICO.GRNBOK = SAQRIT.GREENBOOK AND ISNULL(SAQICO.EQUIPMENT_ID,'') = ISNULL(SAQRIT.EQUIPMENT_ID,'') AND SAQRIT.LINE = SAQICO.LINE
                    # WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID='{rev}' AND SAQICO.SERVICE_ID = 'Z0100' AND SAQICO.CNSMBL_ENT <> 'Included' """.format(total_net = GetSum.TOTAL_EXT, QuoteRecordId=self.quote_record_id,rev =self.quote_revision_id, pricing_field = pricing_field_annualized, pricing_field_doc=pricing_field_doc, exch_rate = self.exch_rate))
                    get_line_items_values = Sql.GetList("""SELECT ({total_net} /CASE WHEN DATEDIFF(day,SAQRIT.CONTRACT_VALID_FROM, SAQRIT.CONTRACT_VALID_TO) = 0 THEN 1 ELSE (DATEDIFF(day,SAQRIT.CONTRACT_VALID_FROM, SAQRIT.CONTRACT_VALID_TO) +1)END ) * CNTDAY AS PRICE_AMT, QUOTE_ITEM_COVERED_OBJECT_RECORD_ID FROM SAQICO (NOLOCK) 
                    INNER JOIN SAQRIT ON SAQRIT.QUOTE_RECORD_ID = SAQICO.QUOTE_RECORD_ID AND SAQRIT.QTEREV_RECORD_ID = SAQICO.QTEREV_RECORD_ID AND SAQRIT.SERVICE_ID = SAQICO.SERVICE_ID AND SAQICO.GRNBOK = SAQRIT.GREENBOOK AND ISNULL(SAQICO.EQUIPMENT_ID,'') = ISNULL(SAQRIT.EQUIPMENT_ID,'') AND SAQRIT.LINE = SAQICO.LINE
                    WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID='{rev}' AND SAQICO.SERVICE_ID = 'Z0100' AND SAQICO.CNSMBL_ENT <> 'Included'""".format(total_net = GetSum.TOTAL_EXT, QuoteRecordId=self.quote_record_id,rev =self.quote_revision_id))
                    for line in get_line_items_values:
                        line_dict = {}
                       
                        line_dict[str(line.QUOTE_ITEM_COVERED_OBJECT_RECORD_ID)] = {'AITPNP': str(line.PRICE_AMT) }
                        quote_items_list.append(line_dict)
     
        Sql.RunQuery("""UPDATE SAQICO 
            SET 
            SAQICO.STATUS = 'ACQUIRED' 
            FROM SAQICO (NOLOCK) 
            INNER JOIN SAQRIT ON SAQRIT.QUOTE_RECORD_ID = SAQICO.QUOTE_RECORD_ID AND SAQRIT.QTEREV_RECORD_ID = SAQICO.QTEREV_RECORD_ID AND SAQRIT.SERVICE_ID = SAQICO.SERVICE_ID AND SAQICO.GRNBOK = SAQRIT.GREENBOOK AND ISNULL(SAQICO.EQUIPMENT_ID,'') = ISNULL(SAQRIT.EQUIPMENT_ID,'') AND SAQRIT.LINE = SAQICO.LINE
            WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID='{rev}' AND SAQICO.SERVICE_ID = 'Z0100' AND SAQICO.CNSMBL_ENT <> 'Included' """.format(QuoteRecordId=self.quote_record_id,rev =self.quote_revision_id))

        #calling waterfall
        Log.Info("quote_items_list-"+str(quote_items_list))
        if quote_items_list:
            #Trace.Write("quote_items_list-"+str(quote_items_list))
            calling_waterfall = ScriptExecutor.ExecuteGlobal("CQUPPRWLFD",{"Records":str(quote_items_list),"auto_update_flag":"True"})
        #HPQC-312 ends
        Sql.RunQuery("""UPDATE SAQRSP SET UNIT_PRICE = UNIT_PRICE_INGL_CURR * {exch_rate} ,EXTENDED_PRICE = EXTENDED_PRICE_INGL_CURR * {exch_rate} FROM SAQRSP (NOLOCK) WHERE SAQRSP.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRSP.SERVICE_ID = 'Z0100'""".format(rev=self.quote_revision_id, QuoteRecordId=self.quote_record_id,exch_rate = self.exch_rate))
        
        Sql.RunQuery("""UPDATE SAQRIT SET UNIT_PRICE  = UNIT_PRICE_INGL_CURR *"""+str(self.exch_rate)+""" FROM SAQRIT WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID='{rev}' AND SERVICE_ID = 'Z0100'""".format(QuoteRecordId=self.quote_record_id,rev =self.quote_revision_id))
        #SAQRIT
        Sql.RunQuery("UPDATE SAQRIT SET STATUS = SAQICO.STATUS FROM SAQRIT (NOLOCK) JOIN SAQICO (NOLOCK) ON SAQICO.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND SAQICO.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID AND SAQICO.SERVICE_ID = SAQRIT.SERVICE_ID AND SAQICO.QTEITM_RECORD_ID = SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID WHERE SAQRIT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID = '{rev}' AND SAQRIT.SERVICE_ID ='Z0100'".format(QuoteRecordId=self.quote_record_id,rev =self.quote_revision_id))
        ###calling script for saqris,saqtrv insert
        CallingCQIFWUDQTM = ScriptExecutor.ExecuteGlobal("CQIFWUDQTM",{"QT_REC_ID":self.quote_id,"Operation":"ANCILLARY_PRICING","ANC_SERVICE_ID" : "('Z0101','Z0100')"})
    
    def repricecall_validation():
        repricelist=SqlHelper.GetList("""SELECT DISTINCT SAP_PART_NUMBER FROM SYSPBT WHERE QTEREV_RECORD_ID = '{rev}' AND QUOTE_RECORD_ID='{QuoteRecordId}' AND BATCH_GROUP_RECORD_ID='{BatchGroupRecordId}'""".format(BatchGroupRecordId=self.batch_group_record_id, QuoteRecordId=self.quote_record_id,rev =self.quote_revision_id))
        zeroPrice=[]
        for ele in repricelist:
            zeroPrice.append(ele.SAP_PART_NUMBER)
        #ScriptExecutor.ExecuteGlobal('CQPARTSINS',{"CPQ_Columns":{"Action": "autoPrice","Part_number":zeroPrice,"QuoteID":self.quote_id}})

        
#Object Creation based on the class. Most of the functions called via self object.
start_time = time.time()
Log.Info("CPS Pricing Start ==>"+str(start_time))
fpm_obj = FpmPriceUpdate()
fpm_obj.fetch_quotebasic_info()
fpm_obj.fetch_priceinfo()
fpm_obj.batch_insert()
fpm_obj.service_validation()
end_time = time.time() 
Log.Info("CPS PRICING end==> "+str(end_time - start_time))
#fpm_obj.repricecall_validation()

# =========================================================================================================================================
#   __script_name : CQADDONPRD.PY
#   __script_description : TO INSERT THE SAQTSE AND SAQSGE TABLE INSERT WHILE ADDING ADD ON PRODUCTS.
#   __primary_author__ : GAYATHRI AMARESAN
#   __create_date :08-12-2021
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
from SYDATABASE import SQL
Sql = SQL()
import sys


def addon_service_level_entitlement(OfferingRow_detail,greenbook):
    Request_URL="https://cpservices-product-configuration.cfapps.us10.hana.ondemand.com/api/v2/configurations?autoCleanup=False"
						
    Fullresponse = ScriptExecutor.ExecuteGlobal("CQENTLNVAL", {'action':'GET_RESPONSE','partnumber':service_id,'request_url':Request_URL,'request_type':"New"})
    Fullresponse=str(Fullresponse).replace(": true",": \"true\"").replace(": false",": \"false\"")
    Fullresponse= eval(Fullresponse)
    ##getting configuration_status status
    if Fullresponse['complete'] == 'true':
        configuration_status = 'COMPLETE'
    elif Fullresponse['complete'] == 'false':
        configuration_status = 'INCOMPLETE'
    else:
        configuration_status = 'ERROR'
    attributesdisallowedlst=[]
    attributeReadonlylst=[]
    attributesallowedlst=[]
    attributedefaultvalue = []
    overall_att_list_sub =[]
    overallattributeslist =[]
    attributevalues={}
    get_toolptip= ''
    #getquote_sales_val = AttributeID_Pass = ''
    for rootattribute, rootvalue in Fullresponse.items():
        if rootattribute=="rootItem":
            for Productattribute, Productvalue in rootvalue.items():
                if Productattribute=="characteristics":
                    for prdvalue in Productvalue:
                        overallattributeslist.append(prdvalue['id'])
                        if prdvalue['id'].startswith('AGS_Z0046_'):
                            overall_att_list_sub.append(prdvalue['id'])
                        if prdvalue['visible'] =='false':
                            attributesdisallowedlst.append(prdvalue['id'])
                        else:								
                            attributesallowedlst.append(prdvalue['id'])
                        if prdvalue['readOnly'] =='true':
                            attributeReadonlylst.append(prdvalue['id'])
                        for attribute in prdvalue['values']:								
                            attributevalues[str(prdvalue['id'])]=attribute['value']
                            if attribute["author"] in ('Default','System'):
                                #Trace.Write('prdvalue---1554-----'+str(prdvalue['id']))
                                attributedefaultvalue.append(prdvalue["id"])
    attributesallowedlst = list(set(attributesallowedlst))
    overallattributeslist = list(set(overallattributeslist))		
    HasDefaultvalue=False

    ProductVersionObj=Sql.GetFirst("Select product_id from product_versions(nolock) where SAPKBId = '"+str(Fullresponse['kbId'])+"' AND SAPKBVersion='"+str(Fullresponse['kbKey']['version'])+"'")

    is_default = ent_val_code = ''
    AttributeID_Pass =""
    get_toolptip = ""

    if ProductVersionObj:
        insertservice = ""
        tbrow={}	
        for attrs in overallattributeslist:
            
            if attrs in attributevalues:					
                HasDefaultvalue=True					
                STANDARD_ATTRIBUTE_VALUES=Sql.GetFirst("SELECT S.STANDARD_ATTRIBUTE_DISPLAY_VAL,S.STANDARD_ATTRIBUTE_CODE FROM STANDARD_ATTRIBUTE_VALUES (nolock) S INNER JOIN ATTRIBUTE_DEFN (NOLOCK) A ON A.STANDARD_ATTRIBUTE_CODE=S.STANDARD_ATTRIBUTE_CODE WHERE A.SYSTEM_ID = '{}' ".format(attrs))
                ent_disp_val = attributevalues[attrs]
                ent_val_code = attributevalues[attrs]
                #Trace.Write("ent_disp_val----"+str(ent_disp_val))
            else:					
                HasDefaultvalue=False
                ent_disp_val = ""
                ent_val_code = ""
                STANDARD_ATTRIBUTE_VALUES=Sql.GetFirst("SELECT S.STANDARD_ATTRIBUTE_CODE FROM STANDARD_ATTRIBUTE_VALUES (nolock) S INNER JOIN ATTRIBUTE_DEFN (NOLOCK) A ON A.STANDARD_ATTRIBUTE_CODE=S.STANDARD_ATTRIBUTE_CODE WHERE A.SYSTEM_ID = '{}'".format(attrs))
                
            ATTRIBUTE_DEFN=Sql.GetFirst("SELECT * FROM ATTRIBUTE_DEFN (NOLOCK) WHERE SYSTEM_ID='{}'".format(attrs))
            PRODUCT_ATTRIBUTES=Sql.GetFirst("SELECT A.ATT_DISPLAY_DESC,P.ATTRDESC FROM ATT_DISPLAY_DEFN (NOLOCK) A INNER JOIN PRODUCT_ATTRIBUTES (NOLOCK) P ON A.ATT_DISPLAY=P.ATT_DISPLAY WHERE P.PRODUCT_ID={} AND P.STANDARD_ATTRIBUTE_CODE={}".format(ProductVersionObj.product_id,STANDARD_ATTRIBUTE_VALUES.STANDARD_ATTRIBUTE_CODE))
            if PRODUCT_ATTRIBUTES:
                if PRODUCT_ATTRIBUTES.ATTRDESC:
                    get_toolptip = PRODUCT_ATTRIBUTES.ATTRDESC
            if PRODUCT_ATTRIBUTES.ATT_DISPLAY_DESC in ('Drop Down','Check Box') and ent_disp_val:
                get_display_val = Sql.GetFirst("SELECT STANDARD_ATTRIBUTE_DISPLAY_VAL  from STANDARD_ATTRIBUTE_VALUES S INNER JOIN ATTRIBUTE_DEFN (NOLOCK) A ON A.STANDARD_ATTRIBUTE_CODE=S.STANDARD_ATTRIBUTE_CODE WHERE S.STANDARD_ATTRIBUTE_CODE = '{}' AND A.SYSTEM_ID = '{}' AND S.STANDARD_ATTRIBUTE_VALUE = '{}' ".format(STANDARD_ATTRIBUTE_VALUES.STANDARD_ATTRIBUTE_CODE,attrs,  attributevalues[attrs] ) )
                ent_disp_val = get_display_val.STANDARD_ATTRIBUTE_DISPLAY_VAL 
            getslaes_value  = Sql.GetFirst("SELECT SALESORG_ID FROM SAQTRV WHERE QUOTE_RECORD_ID = '"+str(OfferingRow_detail.ADNPRD_ID)+"'")
            if getslaes_value:
                getquote_sales_val = getslaes_value.SALESORG_ID
            get_il_sales = Sql.GetList("select SALESORG_ID from SASORG where country = 'IL'")
            get_il_sales_list = [val.SALESORG_ID for val in get_il_sales]
            
            if ATTRIBUTE_DEFN:
                if ATTRIBUTE_DEFN.STANDARD_ATTRIBUTE_NAME.upper() == "FAB LOCATION":
                    Trace.Write(str(attrs)+'--attrs---1118----'+str(ATTRIBUTE_DEFN.STANDARD_ATTRIBUTE_NAME))
                    Trace.Write(str(getquote_sales_val)+'-getquote_sales_val---'+str(get_il_sales_list))
                    AttributeID_Pass = attrs
                    if getquote_sales_val in get_il_sales_list:
                        NewValue = 'Israel'
                    else:
                        NewValue = 'ROW'
            else:
                AttributeID_Pass =''
                #NewValue = 'ROW'
                #NewValue = ''
            
            #A055S000P01-7401 START
            if str(attrs) in ('AGS_POA_PROD_TYPE','AGS_{}_GEN_POAPDT'.format(OfferingRow_detail.ADNPRD_ID) ) and ent_disp_val != '':
                val = ""
                if str(ent_disp_val) == 'Comprehensive':
                    val = "COMPREHENSIVE SERVICES"
                elif str(ent_disp_val) == 'Complementary':
                    val = "COMPLEMENTARY PRODUCTS"
                Sql.RunQuery("UPDATE SAQTSV SET SERVICE_TYPE = '{}' WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID = '{}'".format(str(val),self.contract_quote_record_id,self.quote_revision_record_id,OfferingRow_detail.ADNPRD_ID))
            #A055S000P01-7401 END
            DTypeset={"Drop Down":"DropDown","Free Input, no Matching":"FreeInputNoMatching","Check Box":"CheckBox"}
            insertservice += """<QUOTE_ITEM_ENTITLEMENT>
                <ENTITLEMENT_ID>{ent_name}</ENTITLEMENT_ID>
                <ENTITLEMENT_VALUE_CODE>{ent_val_code}</ENTITLEMENT_VALUE_CODE>
                <ENTITLEMENT_DESCRIPTION>{tool_desc}</ENTITLEMENT_DESCRIPTION>
                <ENTITLEMENT_TYPE>{ent_type}</ENTITLEMENT_TYPE>
                <ENTITLEMENT_DISPLAY_VALUE>{ent_disp_val}</ENTITLEMENT_DISPLAY_VALUE>
                <ENTITLEMENT_COST_IMPACT>{ct}</ENTITLEMENT_COST_IMPACT>
                <ENTITLEMENT_PRICE_IMPACT>{pi}</ENTITLEMENT_PRICE_IMPACT>
                <IS_DEFAULT>{is_default}</IS_DEFAULT>
                <PRICE_METHOD>{pm}</PRICE_METHOD>
                <CALCULATION_FACTOR>{cf}</CALCULATION_FACTOR>
                <ENTITLEMENT_NAME>{ent_desc}</ENTITLEMENT_NAME>
                </QUOTE_ITEM_ENTITLEMENT>""".format(ent_name = str(attrs),ent_val_code = ent_val_code,ent_type = DTypeset[PRODUCT_ATTRIBUTES.ATT_DISPLAY_DESC] if PRODUCT_ATTRIBUTES else  '',ent_desc = ATTRIBUTE_DEFN.STANDARD_ATTRIBUTE_NAME,ent_disp_val = ent_disp_val if HasDefaultvalue==True else '',ct = '',pi = '',is_default = '1' if str(attrs) in attributedefaultvalue else '0',pm = '',cf = '',tool_desc = get_toolptip.replace("'","''") if "'" in get_toolptip else get_toolptip)
        insertservice = insertservice.encode('ascii', 'ignore').decode('ascii')
        
        tbrow["QUOTE_SERVICE_ENTITLEMENT_RECORD_ID"]=str(Guid.NewGuid()).upper()
        tbrow["QUOTE_ID"]=OfferingRow_detail.QUOTE_ID
        tbrow["ENTITLEMENT_XML"]=insertservice
        tbrow["QUOTE_NAME"]=OfferingRow_detail.QUOTE_NAME
        tbrow["QUOTE_RECORD_ID"]=OfferingRow_detail.QUOTE_RECORD_ID
        tbrow["QTESRV_RECORD_ID"]=OfferingRow_detail.QUOTE_SERVICE_RECORD_ID
        tbrow["SERVICE_RECORD_ID"]=OfferingRow_detail.ADNPRD_RECORD_ID
        tbrow["SERVICE_ID"]=OfferingRow_detail.ADNPRD_ID
        tbrow["SERVICE_DESCRIPTION"]=OfferingRow_detail.ADNPRD_DESCRIPTION
        tbrow["PAR_SERVICE_RECORD_ID"]=OfferingRow_detail.SERVICE_RECORD_ID
        tbrow["PAR_SERVICE_ID"]=OfferingRow_detail.SERVICE_ID
        tbrow["PAR_SERVICE_DESCRIPTION"]=OfferingRow_detail.SERVICE_DESCRIPTION
        tbrow["CPS_CONFIGURATION_ID"]=Fullresponse['id']
        tbrow["SALESORG_RECORD_ID"]=OfferingRow_detail.SALESORG_RECORD_ID
        tbrow["SALESORG_ID"]=OfferingRow_detail.SALESORG_ID
        tbrow["SALESORG_NAME"]=OfferingRow_detail.SALESORG_NAME
        tbrow["CPS_MATCH_ID"] = 1
        tbrow["CPQTABLEENTRYADDEDBY"] = self.user_id
        tbrow["CPQTABLEENTRYDATEADDED"] = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p")  
        tbrow["QTEREV_RECORD_ID"] = self.quote_revision_record_id
        tbrow["QTEREV_ID"] = self.quote_revision_id
        tbrow["CONFIGURATION_STATUS"] = configuration_status
        #tbrow["IS_DEFAULT"] = '1'

        columns = ', '.join("" + str(x) + "" for x in tbrow.keys())
        values = ', '.join("'" + str(x) + "'" for x in tbrow.values())
        insert_qtqtse_query = "INSERT INTO SAQTSE ( %s ) VALUES ( %s );" % (columns, values)
        Sql.RunQuery(insert_qtqtse_query)
        if AttributeID_Pass:
            Trace.Write('1406---AttributeID_Pass---'+str(AttributeID_Pass))
            try:
                Trace.Write('1408--NewValue----'+str(NewValue))					
                add_where =''
                ServiceId = OfferingRow_detail.SERVICE_ID
                whereReq = "QUOTE_RECORD_ID = '{}' and SERVICE_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(OfferingRow_detail.QUOTE_RECORD_ID,OfferingRow_detail.SERVICE_ID,self.quote_revision_record_id)
                ent_params_list = str(whereReq)+"||"+str(add_where)+"||"+str(AttributeID_Pass)+"||"+str(NewValue)+"||"+str(ServiceId) + "||" + 'SAQTSE'
                result = ScriptExecutor.ExecuteGlobal("CQASSMEDIT", {"ACTION": 'UPDATE_ENTITLEMENT', 'ent_params_list':ent_params_list})
            except:
                #Log.Info('1408------error--')
                Trace.Write('error--296')
        try:
            if OfferingRow_detail.SERVICE_ID == 'Z0016':
                try:
                    QuoteEndDate = datetime.datetime.strptime(Quote.GetCustomField('QuoteExpirationDate').Content, '%Y-%m-%d').date()
                    QuoteStartDate = datetime.datetime.strptime(Quote.GetCustomField('QuoteStartDate').Content, '%Y-%m-%d').date()
                    contract_days = (QuoteEndDate - QuoteStartDate).days
                    ent_disp_val = 	str(contract_days)
                except:						
                    ent_disp_val = ent_disp_val					

                # try:
                # 	AttributeID = 'AGS_CON_DAY'
                # 	NewValue = ent_disp_val
                # 	add_where =''
                # 	ServiceId = OfferingRow_detail.get("SERVICE_ID")
                # 	whereReq = "QUOTE_RECORD_ID = '"+str(OfferingRow_detail.get('QUOTE_RECORD_ID'))+"' and SERVICE_ID like '%Z0016%' and QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"' "

                # 	ent_params_list = str(whereReq)+"||"+str(add_where)+"||"+str(AttributeID)+"||"+str(ent_disp_val)+"||"+str(ServiceId) + "||" + 'SAQTSE'
                # 	result = ScriptExecutor.ExecuteGlobal("CQASSMEDIT", {"ACTION": 'UPDATE_ENTITLEMENT', 'ent_params_list':ent_params_list})
                # except:
                # 	pass
    
        except:
            pass
        #calling pre-logic valuedriver script
        try:
            Trace.Write("PREDEFINED WAFER DRIVER IFLOW")
            where_condition = " WHERE QUOTE_RECORD_ID='{}' AND QTEREV_RECORD_ID='{}' AND SERVICE_ID = '{}' ".format(self.contract_quote_record_id, self.quote_revision_record_id, OfferingRow_detail.get("SERVICE_ID"))
            # CQTVLDRIFW.valuedriver_predefined(self.contract_quote_record_id,"SERVICE_LEVEL",OfferingRow_detail.get("SERVICE_ID"),self.user_id,self.quote_revision_record_id, where_condition)
            
            predefined = ScriptExecutor.ExecuteGlobal("CQVLDPRDEF",{"where_condition": where_condition,"quote_rec_id": self.contract_quote_record_id ,"level":"SERVICE_LEVEL", "treeparam": OfferingRow_detail.get("SERVICE_ID"),"user_id": self.user_id, "quote_rev_id":self.quote_revision_record_id})

        except:
            Trace.Write("EXCEPT---PREDEFINED DRIVER IFLOW")
        if OfferingRow_detail.get("SERVICE_ID") in ['Z0108','Z0110']:
            try:

                #A055S000P01-13524 start(UPDATE SAQSPT)
                contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
                quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
                get_party_role = Sql.GetList("SELECT PARTY_ID,PARTY_ROLE FROM SAQTIP(NOLOCK) WHERE QUOTE_RECORD_ID = '"+str(contract_quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' and PARTY_ROLE in ('SOLD TO','SHIP TO')")
                account_info = {}
                for keyobj in get_party_role:
                    account_info[keyobj.PARTY_ROLE] = keyobj.PARTY_ID
                #get info from revision table start
                sales_id = sales_rec =qt_rev_id = qt_id=''
                get_rev_sales_ifo = Sql.GetFirst("select QUOTE_ID,SALESORG_ID,SALESORG_RECORD_ID,QTEREV_ID,CONTRACT_VALID_FROM,CONTRACT_VALID_TO from SAQTRV where QUOTE_RECORD_ID = '"+str(contract_quote_record_id)+"' AND QUOTE_REVISION_RECORD_ID = '"+str(quote_revision_record_id)+"'")
                if get_rev_sales_ifo:
                    sales_id = get_rev_sales_ifo.SALESORG_ID
                    sales_rec = get_rev_sales_ifo.SALESORG_RECORD_ID
                    qt_rev_id = get_rev_sales_ifo.QTEREV_ID
                    qt_id = get_rev_sales_ifo.QUOTE_ID
                #get info from revision table end
                get_forecast_info = """Insert SAQSPT (QUOTE_SERVICE_PART_RECORD_ID,BASEUOM_ID,BASEUOM_RECORD_ID,CUSTOMER_PART_NUMBER,CUSTOMER_PART_NUMBER_RECORD_ID,DELIVERY_MODE,EXTENDED_UNIT_PRICE,PART_NUMBER,PART_DESCRIPTION,PART_RECORD_ID,PRDQTYCON_RECORD_ID,CUSTOMER_ANNUAL_QUANTITY,QUOTE_ID,QUOTE_NAME,QUOTE_RECORD_ID,SALESORG_ID,SALESORG_RECORD_ID,SALESUOM_CONVERSION_FACTOR,SALESUOM_ID,SALESUOM_RECORD_ID,SCHEDULE_MODE,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,UNIT_PRICE,VALID_FROM_DATE,VALID_TO_DATE,DELIVERY_INTERVAL,MATPRIGRP_ID,MATPRIGRP_NAME,MATPRIGRP_RECORD_ID,PAR_SERVICE_DESCRIPTION,PAR_SERVICE_ID,PAR_SERVICE_RECORD_ID,QTEREV_ID,	
                QTEREV_RECORD_ID,PRICE_REQUEST_ID,PRICE_REQUEST_STATUS,PRICE_REQUEST_TYPE,	
                CORE_CREDIT_PRICE,CUSTOMER_PARTICIPATE,CUSTOMER_ACCEPT_PART,EXCHANGE_ELIGIBLE,INCLUDED,MATERIALSTATUS_ID,MATERIALSTATUS_RECORD_ID,NEW_PART,ODCC_FLAG,PROD_INSP_MEMO,RETURN_TYPE,SHELF_LIFE,SHPACCOUNT_ID,SHPACCOUNT_RECORD_ID,STPACCOUNT_ID,STPACCOUNT_RECORD_ID,YEAR_1_DEMAND,YEAR_2_DEMAND,YEAR_3_DEMAND) SELECT

                CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_PART_RECORD_ID ,'' as BASEUOM_ID,'' as BASEUOM_RECORD_ID,CUSTOMER_PART_NUMBER,CUSTOMER_PART_NUMBER_RECORD_ID,DELIVERY_MODE,EXTENDED_UNIT_PRICE,PART_NUMBER,PART_DESCRIPTION,PART_RECORD_ID,PRDQTYCON_RECORD_ID,null as CUSTOMER_ANNUAL_QUANTITY,'{qt_id}' as QUOTE_ID,'' as QUOTE_NAME,'{qtt}' as QUOTE_RECORD_ID,'{sales_id}' as SALESORG_ID,'{sales_rec}' as SALESORG_RECORD_ID,SALESUOM_CONVERSION_FACTOR,SALESUOM_ID,SALESUOM_RECORD_ID,SCHEDULE_MODE,'' as SERVICE_DESCRIPTION,'{service_id}' as SERVICE_ID,'' as SERVICE_RECORD_ID,UNIT_PRICE,'{ctf}' as VALID_FROM_DATE,'{ctt}' as VALID_TO_DATE,'' as DELIVERY_INTERVAL,MATPRIGRP_ID,MATPRIGRP_NAME,MATPRIGRP_RECORD_ID,'' as PAR_SERVICE_DESCRIPTION,'' as PAR_SERVICE_ID,'' as PAR_SERVICE_RECORD_ID,'{qt_rev_id}' as QTEREV_ID,'{rid}' as QTEREV_RECORD_ID,'' as PRICE_REQUEST_ID,'' as PRICE_REQUEST_STATUS,'' as PRICE_REQUEST_TYPE,CORE_CREDIT_PRICE,CUSTOMER_PARTICIPATE,CUSTOMER_ACCEPT_PART,EXCHANGE_ELIGIBLE,'' as INCLUDED,'' as MATERIALSTATUS_ID,'' as MATERIALSTATUS_RECORD_ID,'' as NEW_PART,'' as ODCC_FLAG,PROD_INSP_MEMO,RETURN_TYPE,SHELF_LIFE,SHPACCOUNT_ID,SHPACCOUNT_RECORD_ID,STPACCOUNT_ID,STPACCOUNT_RECORD_ID,YEAR_1_DEMAND,YEAR_2_DEMAND,YEAR_3_DEMAND FROM SAFPLT where SHPACCOUNT_ID = '{ship_record_id}' AND STPACCOUNT_ID = '{stp_acc_id}' """.format(ctf =get_rev_sales_ifo.CONTRACT_VALID_FROM ,ctt= get_rev_sales_ifo.CONTRACT_VALID_TO,rid=quote_revision_record_id,qtt=contract_quote_record_id,ship_record_id=str(account_info.get('SHIP TO')),sales_id = sales_id,sales_rec =sales_rec,qt_rev_id=qt_rev_id,qt_id=qt_id,stp_acc_id=str(account_info.get('SOLD TO')),service_id=str(OfferingRow_detail.get("SERVICE_ID")))
                
                Sql.RunQuery(get_forecast_info)
                
                update_customer_pn = """UPDATE SAQSPT SET SAQSPT.CUSTOMER_PART_NUMBER = M.CUSTOMER_PART_NUMBER FROM SAQSPT S INNER JOIN MAMSAC M ON S.PART_NUMBER= M.SAP_PART_NUMBER WHERE M.SALESORG_ID = '{sales_id}' and M.ACCOUNT_ID='{stp_acc_id}' AND S.QUOTE_RECORD_ID = '{quote_rec_id}' AND S.QTEREV_RECORD_ID = '{quote_revision_rec_id}'""".format(quote_rec_id = contract_quote_record_id ,sales_id = sales_id,stp_acc_id=str(account_info.get('SOLD TO')),quote_revision_rec_id =quote_revision_record_id)
                Sql.RunQuery(update_customer_pn)
            
            except:
                Trace.Write("EXCEPT----PREDEFINED DRIVER IFLOW")



def addon_greenbook_level_entitlement(service_id):
    Sql.RunQuery("""INSERT SAQSGE (KB_VERSION,QUOTE_ID,QUOTE_NAME,QUOTE_RECORD_ID,QTEREV_RECORD_ID,QTEREV_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,	
            CPS_CONFIGURATION_ID, CPS_MATCH_ID,GREENBOOK,GREENBOOK_RECORD_ID,QTESRVENT_RECORD_ID,ENTITLEMENT_XML,CONFIGURATION_STATUS, QUOTE_SERVICE_GREENBOOK_ENTITLEMENT_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED )
            SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_GREENBOOK_ENTITLEMENT_RECORD_ID, {UserId} as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM (SELECT DISTINCT SAQTSE.KB_VERSION,SAQTSE.QUOTE_ID,SAQTSE.QUOTE_NAME,SAQTSE.QUOTE_RECORD_ID,SAQTSE.QTEREV_RECORD_ID,SAQTSE.QTEREV_ID,SAQTSE.SERVICE_DESCRIPTION,SAQTSE.SERVICE_ID,SAQTSE.SERVICE_RECORD_ID,SAQTSE.SALESORG_ID,SAQTSE.SALESORG_NAME,SAQTSE.SALESORG_RECORD_ID,	
            SAQTSE.CPS_CONFIGURATION_ID, SAQTSE.CPS_MATCH_ID,SAQSGB.GREENBOOK,SAQSCO.GREENBOOK_RECORD_ID,SAQTSE.QUOTE_SERVICE_ENTITLEMENT_RECORD_ID as QTESRVENT_RECORD_ID,SAQTSE.ENTITLEMENT_XML,SAQTSE.CONFIGURATION_STATUS FROM
        SAQTSE (NOLOCK) JOIN SAQSGB  (NOLOCK) ON SAQSGB.SERVICE_RECORD_ID = SAQTSE.SERVICE_RECORD_ID AND SAQSGB.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID  AND SAQSGB.QTEREV_RECORD_ID = SAQTSE.QTEREV_RECORD_ID  
            WHERE SAQTSE.QUOTE_RECORD_ID ='{QuoteRecordId}'  AND SAQTSE.QTEREV_RECORD_ID = '{revision_rec_id}' AND SAQTSE.SERVICE_ID = '{ServiceId}')IQ""".format(UserId=userId, QuoteRecordId=Qt_rec_id, ServiceId=service_id, revision_rec_id = rev_rec_id))
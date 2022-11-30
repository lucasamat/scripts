# =========================================================================================================================================
#   __script_name : CQADDONPRD.PY
#   __script_description : TO INSERT THE SAQTSE AND SAQSGE TABLE INSERT WHILE ADDING ADD ON PRODUCTS.
#   __primary_author__ : GAYATHRI AMARESAN
#   __create_date :08-12-2021
#   Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
from SYDATABASE import SQL
Sql = SQL()
from datetime import datetime
import re
import SYCNGEGUID as CPQID
Log.Info("Test")

User_name = ScriptExecutor.ExecuteGlobal("SYUSDETAIL", "USERNAME")
User_Id = ScriptExecutor.ExecuteGlobal("SYUSDETAIL", "USERID")

def _construct_dict_xml(updateentXML):
    entxmldict = {}
    pattern_tag = re.compile(r'(<QUOTE_ITEM_ENTITLEMENT>[\w\W]*?</QUOTE_ITEM_ENTITLEMENT>)')
    pattern_name = re.compile(r'<ENTITLEMENT_ID>([^>]*?)</ENTITLEMENT_ID>')
    entitlement_display_value_tag_pattern = re.compile(r'<ENTITLEMENT_DISPLAY_VALUE>([^>]*?)</ENTITLEMENT_DISPLAY_VALUE>')
    display_val_dict = {}
    if updateentXML:
        for m in re.finditer(pattern_tag, updateentXML):
            sub_string = m.group(1)
            x=re.findall(pattern_name,sub_string)
            if x:
                entitlement_display_value_tag_match = re.findall(entitlement_display_value_tag_pattern,sub_string)
                if entitlement_display_value_tag_match:
                    display_val_dict[x[0]] = entitlement_display_value_tag_match[0].upper()
            entxmldict[x[0]]=sub_string
    return entxmldict

def _entitlement_parent_inherit(OfferingRow_detail):
    par_service_id = OfferingRow_detail.SERVICE_ID
    contract_quote_rec_id = OfferingRow_detail.QUOTE_RECORD_ID
    quote_revision_rec_id = OfferingRow_detail.QTEREV_RECORD_ID
    service_id = OfferingRow_detail.ADNPRD_ID
    get_parent_xml = Sql.GetFirst("SELECT * FROM SAQTSE (NOLOCK) WHERE QUOTE_RECORD_ID ='{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID ='{}'".format(contract_quote_rec_id, quote_revision_rec_id ,par_service_id) )
    getall_recid = Sql.GetFirst("SELECT * FROM SAQTSE (NOLOCK) WHERE QUOTE_RECORD_ID ='{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID ='{}' AND PAR_SERVICE_ID = '{}' ".format(contract_quote_rec_id, quote_revision_rec_id, service_id ,par_service_id) )
    get_parent_dict = {}
    get_service_xml_dict = {}
    assign_xml = ""
    if get_parent_xml:
        get_parent_dict = _construct_dict_xml(get_parent_xml.ENTITLEMENT_XML)
    if getall_recid:
        get_service_xml_dict =  _construct_dict_xml(getall_recid.ENTITLEMENT_XML)
    if get_parent_dict and get_service_xml_dict:
        for key,value in get_service_xml_dict.items():			
            if 'AGS_{}_PQB_BILTYP'.format(par_service_id) in get_parent_dict.keys() and key == 'AGS_Z0116_PQB_BILTYP':
                value = get_parent_dict['AGS_{}_PQB_BILTYP'.format(par_service_id)]
                value = value.replace(par_service_id,service_id)
            assign_xml += value
        Sql.RunQuery("UPDATE SAQTSE SET ENTITLEMENT_XML = '{}' WHERE QUOTE_RECORD_ID ='{}' AND QTEREV_RECORD_ID = '{}' AND PAR_SERVICE_ID ='{}' AND SERVICE_ID ='{}'".format(assign_xml,contract_quote_rec_id, quote_revision_rec_id ,par_service_id,service_id) )
    
def _addon_service_level_entitlement(OfferingRow_detail):
    Request_URL="https://cpservices-product-configuration.cfapps.us10.hana.ondemand.com/api/v2/configurations?autoCleanup=False"
                        
    Fullresponse = ScriptExecutor.ExecuteGlobal("CQENTLNVAL", {'action':'GET_RESPONSE','partnumber':OfferingRow_detail.ADNPRD_ID,'request_url':Request_URL,'request_type':"New"})
    Fullresponse=str(Fullresponse).replace(": true",": \"true\"").replace(": false",": \"false\"")
    Fullresponse= eval(Fullresponse)
    ##getting configuration_status status
    if Fullresponse['complete'] == 'true' and Fullresponse['consistent'] == 'true' :
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
    getquote_sales_val = ''
    get_il_sales = Sql.GetList("select SALESORG_ID from SASORG where country = 'IL'")
    get_il_sales_list = [val.SALESORG_ID for val in get_il_sales]
    getslaes_value  = Sql.GetFirst("SELECT SALESORG_ID FROM SAQTRV WHERE QUOTE_RECORD_ID = '"+str(OfferingRow_detail.QUOTE_RECORD_ID)+"'")
    if getslaes_value:
        getquote_sales_val = getslaes_value.SALESORG_ID
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
    ent_val_code = ''
    get_toolptip = ""
    addon_entitlement_object = Sql.GetFirst("select count(SAQTSE.CpqTableEntryId) as cnt from SAQTSE(nolock) inner join SAQSAO on SAQTSE.SERVICE_ID = SAQSAO.ADNPRD_ID AND SAQTSE.PAR_SERVICE_ID = SAQSAO.SERVICE_ID AND SAQTSE.QUOTE_RECORD_ID = SAQSAO.QUOTE_RECORD_ID and SAQTSE.QTEREV_RECORD_ID = SAQSAO.QTEREV_RECORD_ID WHERE SAQTSE.PAR_SERVICE_ID = '{}' AND SAQSAO.QUOTE_RECORD_ID = '{}' and SAQSAO.QTEREV_RECORD_ID = '{}' AND SAQTSE.SERVICE_ID = '{}'".format(OfferingRow_detail.SERVICE_ID,OfferingRow_detail.QUOTE_RECORD_ID,OfferingRow_detail.QTEREV_RECORD_ID, OfferingRow_detail.ADNPRD_ID))
    if ProductVersionObj and addon_entitlement_object.cnt == 0:
        Attributeid_list = {}
        insertservice = ""
        tbrow={}	
        for attrs in overallattributeslist:			
            if attrs in attributevalues:					
                HasDefaultvalue=True					
                STANDARD_ATTRIBUTE_VALUES=Sql.GetFirst("SELECT S.STANDARD_ATTRIBUTE_DISPLAY_VAL,S.STANDARD_ATTRIBUTE_CODE FROM STANDARD_ATTRIBUTE_VALUES (nolock) S INNER JOIN ATTRIBUTE_DEFN (NOLOCK) A ON A.STANDARD_ATTRIBUTE_CODE=S.STANDARD_ATTRIBUTE_CODE WHERE A.SYSTEM_ID = '{}' ".format(attrs))
                ent_disp_val = attributevalues[attrs]
                ent_val_code = attributevalues[attrs]				
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
                if PRODUCT_ATTRIBUTES.ATT_DISPLAY_DESC:
                    if PRODUCT_ATTRIBUTES.ATT_DISPLAY_DESC in ('Drop Down','Check Box') and ent_disp_val:
                        get_display_val = Sql.GetFirst("SELECT STANDARD_ATTRIBUTE_DISPLAY_VAL  from STANDARD_ATTRIBUTE_VALUES S INNER JOIN ATTRIBUTE_DEFN (NOLOCK) A ON A.STANDARD_ATTRIBUTE_CODE=S.STANDARD_ATTRIBUTE_CODE WHERE S.STANDARD_ATTRIBUTE_CODE = '{}' AND A.SYSTEM_ID = '{}' AND S.STANDARD_ATTRIBUTE_VALUE = '{}' ".format(STANDARD_ATTRIBUTE_VALUES.STANDARD_ATTRIBUTE_CODE,attrs,  attributevalues[attrs] ) )
                        ent_disp_val = get_display_val.STANDARD_ATTRIBUTE_DISPLAY_VAL 
                if ATTRIBUTE_DEFN:
                    if ATTRIBUTE_DEFN.STANDARD_ATTRIBUTE_NAME.upper() == "FAB LOCATION":
                        # Trace.Write(str(attrs)+'--attrs---1118----'+str(ATTRIBUTE_DEFN.STANDARD_ATTRIBUTE_NAME))
                        # Trace.Write(str(getquote_sales_val)+'-getquote_sales_val---'+str(get_il_sales_list))
                        #AttributeID_Pass = attrs
                        if getquote_sales_val in get_il_sales_list:
                            Attributeid_list[attrs] = "Israel"
                        else:
                            Attributeid_list[attrs] = 'ROW'
                #HPQC #2124 start
                if attrs == 'AGS_{}_QTP_PAPRCD'.format(OfferingRow_detail.ADNPRD_ID):
                    Attributeid_list[attrs] = OfferingRow_detail.SERVICE_ID
                #HPQC #2124 end
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
                    </QUOTE_ITEM_ENTITLEMENT>""".format(ent_name = str(attrs),
                        ent_val_code = ent_val_code,
                        ent_type = DTypeset[PRODUCT_ATTRIBUTES.ATT_DISPLAY_DESC] if PRODUCT_ATTRIBUTES else  '',
                        ent_desc = ATTRIBUTE_DEFN.STANDARD_ATTRIBUTE_NAME.replace("&",";#38").replace(">","&gt;").replace("<","&lt;"),
                        ent_disp_val = ent_disp_val.replace("&",";#38").replace(">","&gt;").replace("<","&lt;") if HasDefaultvalue==True else '',
                        ct = '',pi = '',
                        is_default = '1' if str(attrs) in attributedefaultvalue else '0',
                        pm = '',cf = '',
                        tool_desc = get_toolptip.replace("'","''").replace("&",";#38").replace(">","&gt;").replace("<","&lt;")
                    )
            
        insertservice = insertservice.encode('ascii', 'ignore').decode('ascii')
        
        tbrow["QUOTE_SERVICE_ENTITLEMENT_RECORD_ID"]=str(Guid.NewGuid()).upper()
        tbrow["QUOTE_ID"]=OfferingRow_detail.QUOTE_ID
        tbrow["ENTITLEMENT_XML"]=insertservice
        tbrow["QUOTE_NAME"]=OfferingRow_detail.QUOTE_NAME
        tbrow["QUOTE_RECORD_ID"]=OfferingRow_detail.QUOTE_RECORD_ID
        tbrow["QTESRV_RECORD_ID"]=OfferingRow_detail.QUOTE_SERVICE_RECORD_ID
        tbrow["SERVICE_RECORD_ID"]=OfferingRow_detail.ADNPRDOFR_RECORD_ID
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
        tbrow["CPQTABLEENTRYADDEDBY"] = User_Id
        tbrow["CPQTABLEENTRYDATEADDED"] = datetime.now().strftime("%m/%d/%Y %H:%M:%S %p")  
        tbrow["QTEREV_RECORD_ID"] = OfferingRow_detail.QTEREV_RECORD_ID
        tbrow["QTEREV_ID"] = OfferingRow_detail.QTEREV_ID
        tbrow["CONFIGURATION_STATUS"] = configuration_status
        #tbrow["IS_DEFAULT"] = '1'

        columns = ', '.join("" + str(x) + "" for x in tbrow.keys())
        values = ', '.join("'" + str(x) + "'" for x in tbrow.values())
        insert_qtqtse_query = "INSERT INTO SAQTSE ( %s ) VALUES ( %s );" % (columns, values)
        Sql.RunQuery(insert_qtqtse_query)

        if OfferingRow_detail.ADNPRD_ID == 'Z0116':
            _entitlement_parent_inherit(OfferingRow_detail)
        if Attributeid_list:
            Trace.Write('1406---AttributeID_Pass---'+str(Attributeid_list))
            try:
                for attr_key,attr_value in Attributeid_list.items():
                    Trace.Write('1408--NewValue----'+str(Attributeid_list))					
                    add_where =''
                    ServiceId = OfferingRow_detail.ADNPRD_ID
                    whereReq = "QUOTE_RECORD_ID = '{}' and SERVICE_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(OfferingRow_detail.QUOTE_RECORD_ID,ServiceId,OfferingRow_detail.QTEREV_RECORD_ID)
                    ent_params_list = str(whereReq)+"||"+str(add_where)+"||"+str(attr_key)+"||"+str(attr_value)+"||"+str(ServiceId) + "||" + 'SAQTSE'
                    result = ScriptExecutor.ExecuteGlobal("CQASSMEDIT", {"ACTION": 'UPDATE_ENTITLEMENT', 'ent_params_list':ent_params_list})
            except:
                #Log.Info('1408------error--')
                Trace.Write('error--296')
def update_entitlement_col_val(OfferingRow_detail):
    for rec_table in ['SAQSCE','SAQSGE','SAQTSE','SAQSAE']:
        where_condition = " WHERE QUOTE_RECORD_ID='{}' AND QTEREV_RECORD_ID='{}' AND SERVICE_ID = '{}' ".format(OfferingRow_detail.QUOTE_RECORD_ID, OfferingRow_detail.QTEREV_RECORD_ID, OfferingRow_detail.ADNPRD_ID)
        ScriptExecutor.ExecuteGlobal("CQENTLNVAL", {'action':'ENTITLEMENT_COLUMN_UPDATE',
                                                    'partnumber':OfferingRow_detail.ADNPRD_ID,
                                                    'where_cond' :where_condition, 
                                                    'ent_level_table': rec_table
                                                    })
    return True

def _addon_equipment_insert(OfferingRow_detail,greenbook,record_ids):
    
    rec = str(record_ids).split(',')
    Trace.Write("record_id_ chk -- "+str(record_ids))
    if len(rec) >1:
        if record_ids.startswith("SAQSCO"):
            record_id = [
                CPQID.KeyCPQId.GetKEYId("SAQSCO", str(value))
                for value in rec 
            ]
            Trace.Write("If_record_id--- "+str(record_id))
        else:
            record_id = str(record_ids).split(",")
    else:
        if record_ids.startswith("SAQSCO"):
            record_id = [CPQID.KeyCPQId.GetKEYId("SAQSCO", str(record_ids))] 
        else:
            record_id = str(record_ids).split(",")
    Trace.Write("_chk--- "+str(record_id)+" - "+str(greenbook))

    if record_ids != '' and record_ids  != 'undefined':
        for record in record_id:
            # if record != "":
            Sql.RunQuery(
                        """
                        INSERT SAQSCO (
                            QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,
                            EQUIPMENT_ID,
                            EQUIPMENT_RECORD_ID,
                            EQUIPMENT_DESCRIPTION,                            
                            FABLOCATION_ID,
                            FABLOCATION_NAME,
                            FABLOCATION_RECORD_ID,
                            WAFER_SIZE,
                            SALESORG_ID,
                            SALESORG_NAME,
                            SALESORG_RECORD_ID,
                            SERIAL_NO,
                            QUOTE_RECORD_ID,
                            QUOTE_ID,
                            QUOTE_NAME,
                            RELOCATION_EQUIPMENT_TYPE,
                            SERVICE_ID,
                            SERVICE_TYPE,
                            SERVICE_DESCRIPTION,
                            SERVICE_RECORD_ID,
                            EQUIPMENT_STATUS,
                            EQUIPMENTCATEGORY_ID,
                            EQUIPMENTCATEGORY_DESCRIPTION,
                            EQUIPMENTCATEGORY_RECORD_ID,
                            PLATFORM,
                            GREENBOOK,
                            GREENBOOK_RECORD_ID,
                            MNT_PLANT_RECORD_ID,
                            MNT_PLANT_NAME,
                            MNT_PLANT_ID,
                            WARRANTY_START_DATE,
                            WARRANTY_END_DATE,
                            CUSTOMER_TOOL_ID,
                            PAR_SERVICE_DESCRIPTION,
                            PAR_SERVICE_ID,
                            PAR_SERVICE_RECORD_ID,
                            TECHNOLOGY,
                            CONTRACT_VALID_FROM,
                            CONTRACT_VALID_TO,
                            CPQTABLEENTRYADDEDBY,
                            CPQTABLEENTRYDATEADDED,
                            CpqTableEntryModifiedBy,
                            CpqTableEntryDateModified,
                            QTEREV_RECORD_ID,
                            KPU,
                            QTEREV_ID
                                                    
                            ) SELECT
                                CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,
                                EQUIPMENT_ID,
                                EQUIPMENT_RECORD_ID,
                                EQUIPMENT_DESCRIPTION,                                
                                FABLOCATION_ID,
                                FABLOCATION_NAME,
                                FABLOCATION_RECORD_ID,
                                WAFER_SIZE,
                                SALESORG_ID,
                                SALESORG_NAME,
                                SALESORG_RECORD_ID,
                                SERIAL_NO,
                                QUOTE_RECORD_ID,
                                QUOTE_ID,
                                QUOTE_NAME,
                                RELOCATION_EQUIPMENT_TYPE,
                                '{serviceid}',
                                '{service_type}',
                                '{desc}',
                                '{rec}',
                                EQUIPMENT_STATUS,
                                EQUIPMENTCATEGORY_ID,
                                EQUIPMENTCATEGORY_DESCRIPTION,
                                EQUIPMENTCATEGORY_RECORD_ID,
                                PLATFORM,
                                GREENBOOK,
                                GREENBOOK_RECORD_ID,
                                MNT_PLANT_RECORD_ID,
                                MNT_PLANT_NAME,
                                MNT_PLANT_ID,
                                WARRANTY_START_DATE,
                                WARRANTY_END_DATE,
                                CUSTOMER_TOOL_ID,
                                SERVICE_DESCRIPTION,
                                SERVICE_ID,
                                SERVICE_RECORD_ID,
                                TECHNOLOGY,
                                CONTRACT_VALID_FROM,
                                CONTRACT_VALID_TO,
                                '{UserName}',
                                GETDATE(),
                                {UserId},
                                GETDATE(),
                                QTEREV_RECORD_ID,
                                KPU,
                                QTEREV_ID
                                FROM SAQSCO (NOLOCK)
                                WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID ='{par_service_id}' AND GREENBOOK = '{greenbook}' AND QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID = '{record}' AND SAQSCO.EQUIPMENT_ID not in (SELECT EQUIPMENT_ID FROM SAQSCO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}'  AND QTEREV_RECORD_ID = '{RevisionRecordId}'  AND PAR_SERVICE_ID ='{par_service_id}' AND SERVICE_ID ='{serviceid}' AND GREENBOOK = '{greenbook}')
                                                        
                            """.format(
                                par_service_id = OfferingRow_detail.SERVICE_ID,
                                serviceid = OfferingRow_detail.ADNPRD_ID ,
                                service_type ="Add-On Products",
                                QuoteRecordId = OfferingRow_detail.QUOTE_RECORD_ID,
                                RevisionRecordId = OfferingRow_detail.QTEREV_RECORD_ID,
                                desc = OfferingRow_detail.ADNPRD_DESCRIPTION,
                                rec = OfferingRow_detail.ADNPRDOFR_RECORD_ID,
                                UserName = User_name,
                                UserId = User_Id,
                                greenbook = greenbook,
                                record = str(record).strip()
                            )
                            )
            # else:
            #     Sql.RunQuery(
            #                 """
            #                 INSERT SAQSCO (
            #                     QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,
            #                     EQUIPMENT_ID,
            #                     EQUIPMENT_RECORD_ID,
            #                     EQUIPMENT_DESCRIPTION,                            
            #                     FABLOCATION_ID,
            #                     FABLOCATION_NAME,
            #                     FABLOCATION_RECORD_ID,
            #                     WAFER_SIZE,
            #                     SALESORG_ID,
            #                     SALESORG_NAME,
            #                     SALESORG_RECORD_ID,
            #                     SERIAL_NO,
            #                     QUOTE_RECORD_ID,
            #                     QUOTE_ID,
            #                     QUOTE_NAME,
            #                     RELOCATION_EQUIPMENT_TYPE,
            #                     SERVICE_ID,
            #                     SERVICE_TYPE,
            #                     SERVICE_DESCRIPTION,
            #                     SERVICE_RECORD_ID,
            #                     EQUIPMENT_STATUS,
            #                     EQUIPMENTCATEGORY_ID,
            #                     EQUIPMENTCATEGORY_DESCRIPTION,
            #                     EQUIPMENTCATEGORY_RECORD_ID,
            #                     PLATFORM,
            #                     GREENBOOK,
            #                     GREENBOOK_RECORD_ID,
            #                     MNT_PLANT_RECORD_ID,
            #                     MNT_PLANT_NAME,
            #                     MNT_PLANT_ID,
            #                     WARRANTY_START_DATE,
            #                     WARRANTY_END_DATE,
            #                     CUSTOMER_TOOL_ID,
            #                     PAR_SERVICE_DESCRIPTION,
            #                     PAR_SERVICE_ID,
            #                     PAR_SERVICE_RECORD_ID,
            #                     TECHNOLOGY,
            #                     CONTRACT_VALID_FROM,
            #                     CONTRACT_VALID_TO,
            #                     CPQTABLEENTRYADDEDBY,
            #                     CPQTABLEENTRYDATEADDED,
            #                     CpqTableEntryModifiedBy,
            #                     CpqTableEntryDateModified,
            #                     QTEREV_RECORD_ID,
            #                     KPU,
            #                     QTEREV_ID
                                                        
            #                     ) SELECT
            #                         CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,
            #                         EQUIPMENT_ID,
            #                         EQUIPMENT_RECORD_ID,
            #                         EQUIPMENT_DESCRIPTION,                                
            #                         FABLOCATION_ID,
            #                         FABLOCATION_NAME,
            #                         FABLOCATION_RECORD_ID,
            #                         WAFER_SIZE,
            #                         SALESORG_ID,
            #                         SALESORG_NAME,
            #                         SALESORG_RECORD_ID,
            #                         SERIAL_NO,
            #                         QUOTE_RECORD_ID,
            #                         QUOTE_ID,
            #                         QUOTE_NAME,
            #                         RELOCATION_EQUIPMENT_TYPE,
            #                         '{serviceid}',
            #                         '{service_type}',
            #                         '{desc}',
            #                         '{rec}',
            #                         EQUIPMENT_STATUS,
            #                         EQUIPMENTCATEGORY_ID,
            #                         EQUIPMENTCATEGORY_DESCRIPTION,
            #                         EQUIPMENTCATEGORY_RECORD_ID,
            #                         PLATFORM,
            #                         GREENBOOK,
            #                         GREENBOOK_RECORD_ID,
            #                         MNT_PLANT_RECORD_ID,
            #                         MNT_PLANT_NAME,
            #                         MNT_PLANT_ID,
            #                         WARRANTY_START_DATE,
            #                         WARRANTY_END_DATE,
            #                         CUSTOMER_TOOL_ID,
            #                         SERVICE_DESCRIPTION,
            #                         SERVICE_ID,
            #                         SERVICE_RECORD_ID,
            #                         TECHNOLOGY,
            #                         CONTRACT_VALID_FROM,
            #                         CONTRACT_VALID_TO,
            #                         '{UserName}',
            #                         GETDATE(),
            #                         {UserId},
            #                         GETDATE(),
            #                         QTEREV_RECORD_ID,
            #                         KPU,
            #                         QTEREV_ID
            #                         FROM SAQSCO (NOLOCK)
            #                         WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID ='{par_service_id}' AND GREENBOOK = '{greenbook}' AND SAQSCO.EQUIPMENT_ID not in (SELECT EQUIPMENT_ID FROM SAQSCO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}'  AND QTEREV_RECORD_ID = '{RevisionRecordId}'  AND PAR_SERVICE_ID ='{par_service_id}' AND SERVICE_ID ='{serviceid}' AND GREENBOOK = '{greenbook}')
                                                            
            #                     """.format(
            #                         par_service_id = OfferingRow_detail.SERVICE_ID,
            #                         serviceid = OfferingRow_detail.ADNPRD_ID ,
            #                         service_type ="Add-On Products",
            #                         QuoteRecordId = OfferingRow_detail.QUOTE_RECORD_ID,
            #                         RevisionRecordId = OfferingRow_detail.QTEREV_RECORD_ID,
            #                         desc = OfferingRow_detail.ADNPRD_DESCRIPTION,
            #                         rec = OfferingRow_detail.ADNPRDOFR_RECORD_ID,
            #                         UserName = User_name,
            #                         UserId = User_Id,
            #                         greenbook = greenbook
            #                     )
            #                     )
        
    else:
        Sql.RunQuery(
                    """
                    INSERT SAQSCO (
                        QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,
                        EQUIPMENT_ID,
                        EQUIPMENT_RECORD_ID,
                        EQUIPMENT_DESCRIPTION,                            
                        FABLOCATION_ID,
                        FABLOCATION_NAME,
                        FABLOCATION_RECORD_ID,
                        WAFER_SIZE,
                        SALESORG_ID,
                        SALESORG_NAME,
                        SALESORG_RECORD_ID,
                        SERIAL_NO,
                        QUOTE_RECORD_ID,
                        QUOTE_ID,
                        QUOTE_NAME,
                        RELOCATION_EQUIPMENT_TYPE,
                        SERVICE_ID,
                        SERVICE_TYPE,
                        SERVICE_DESCRIPTION,
                        SERVICE_RECORD_ID,
                        EQUIPMENT_STATUS,
                        EQUIPMENTCATEGORY_ID,
                        EQUIPMENTCATEGORY_DESCRIPTION,
                        EQUIPMENTCATEGORY_RECORD_ID,
                        PLATFORM,
                        GREENBOOK,
                        GREENBOOK_RECORD_ID,
                        MNT_PLANT_RECORD_ID,
                        MNT_PLANT_NAME,
                        MNT_PLANT_ID,
                        WARRANTY_START_DATE,
                        WARRANTY_END_DATE,
                        CUSTOMER_TOOL_ID,
                        PAR_SERVICE_DESCRIPTION,
                        PAR_SERVICE_ID,
                        PAR_SERVICE_RECORD_ID,
                        TECHNOLOGY,
                        CONTRACT_VALID_FROM,
                        CONTRACT_VALID_TO,
                        CPQTABLEENTRYADDEDBY,
                        CPQTABLEENTRYDATEADDED,
                        CpqTableEntryModifiedBy,
                        CpqTableEntryDateModified,
                        QTEREV_RECORD_ID,
                        KPU,
                        QTEREV_ID
                                                
                        ) SELECT
                            CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,
                            EQUIPMENT_ID,
                            EQUIPMENT_RECORD_ID,
                            EQUIPMENT_DESCRIPTION,                                
                            FABLOCATION_ID,
                            FABLOCATION_NAME,
                            FABLOCATION_RECORD_ID,
                            WAFER_SIZE,
                            SALESORG_ID,
                            SALESORG_NAME,
                            SALESORG_RECORD_ID,
                            SERIAL_NO,
                            QUOTE_RECORD_ID,
                            QUOTE_ID,
                            QUOTE_NAME,
                            RELOCATION_EQUIPMENT_TYPE,
                            '{serviceid}',
                            '{service_type}',
                            '{desc}',
                            '{rec}',
                            EQUIPMENT_STATUS,
                            EQUIPMENTCATEGORY_ID,
                            EQUIPMENTCATEGORY_DESCRIPTION,
                            EQUIPMENTCATEGORY_RECORD_ID,
                            PLATFORM,
                            GREENBOOK,
                            GREENBOOK_RECORD_ID,
                            MNT_PLANT_RECORD_ID,
                            MNT_PLANT_NAME,
                            MNT_PLANT_ID,
                            WARRANTY_START_DATE,
                            WARRANTY_END_DATE,
                            CUSTOMER_TOOL_ID,
                            SERVICE_DESCRIPTION,
                            SERVICE_ID,
                            SERVICE_RECORD_ID,
                            TECHNOLOGY,
                            CONTRACT_VALID_FROM,
                            CONTRACT_VALID_TO,
                            '{UserName}',
                            GETDATE(),
                            {UserId},
                            GETDATE(),
                            QTEREV_RECORD_ID,
                            KPU,
                            QTEREV_ID
                            FROM SAQSCO (NOLOCK)
                            WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID ='{par_service_id}' AND GREENBOOK = '{greenbook}' AND SAQSCO.EQUIPMENT_ID not in (SELECT EQUIPMENT_ID FROM SAQSCO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}'  AND QTEREV_RECORD_ID = '{RevisionRecordId}'  AND PAR_SERVICE_ID ='{par_service_id}' AND SERVICE_ID ='{serviceid}' AND GREENBOOK = '{greenbook}')
                                                    
                        """.format(
                            par_service_id = OfferingRow_detail.SERVICE_ID,
                            serviceid = OfferingRow_detail.ADNPRD_ID ,
                            service_type ="Add-On Products",
                            QuoteRecordId = OfferingRow_detail.QUOTE_RECORD_ID,
                            RevisionRecordId = OfferingRow_detail.QTEREV_RECORD_ID,
                            desc = OfferingRow_detail.ADNPRD_DESCRIPTION,
                            rec = OfferingRow_detail.ADNPRDOFR_RECORD_ID,
                            UserName = User_name,
                            UserId = User_Id,
                            greenbook = greenbook
                        )
                        )
    Sql.RunQuery(""" INSERT SAQSCE
                    (KB_VERSION,ENTITLEMENT_XML,CONFIGURATION_STATUS,PAR_SERVICE_ID,PAR_SERVICE_RECORD_ID,PAR_SERVICE_DESCRIPTION,EQUIPMENT_ID,EQUIPMENT_RECORD_ID,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_RECORD_ID,QTEREV_ID,QTESRVCOB_RECORD_ID,QTESRVENT_RECORD_ID,SERIAL_NO,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,CPS_CONFIGURATION_ID,CPS_MATCH_ID,GREENBOOK,GREENBOOK_RECORD_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,QUOTE_SERVICE_COVERED_OBJ_ENTITLEMENTS_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED) 
                    
                    SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_COVERED_OBJ_ENTITLEMENTS_RECORD_ID, {UserId} as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM (
                        SELECT 
                        SAQSGE.KB_VERSION,SAQSGE.ENTITLEMENT_XML,SAQSGE.CONFIGURATION_STATUS,SAQTSE.PAR_SERVICE_ID,SAQTSE.PAR_SERVICE_RECORD_ID,SAQTSE.PAR_SERVICE_DESCRIPTION,SAQSCO.EQUIPMENT_ID,SAQSCO.EQUIPMENT_RECORD_ID,SAQTSE.QUOTE_ID,SAQTSE.QUOTE_RECORD_ID,SAQTSE.QTEREV_RECORD_ID,SAQTSE.QTEREV_ID,SAQSCO.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID as QTESRVCOB_RECORD_ID,SAQTSE.QUOTE_SERVICE_ENTITLEMENT_RECORD_ID as QTESRVENT_RECORD_ID,SAQSCO.SERIAL_NO,SAQTSE.SERVICE_DESCRIPTION,SAQTSE.SERVICE_ID,SAQTSE.SERVICE_RECORD_ID,SAQSGE.CPS_CONFIGURATION_ID,SAQSGE.CPS_MATCH_ID,SAQSCO.GREENBOOK,SAQSCO.GREENBOOK_RECORD_ID,SAQSCO.FABLOCATION_ID,SAQSCO.FABLOCATION_NAME,SAQSCO.FABLOCATION_RECORD_ID,SAQTSE.SALESORG_ID,SAQTSE.SALESORG_NAME,SAQTSE.SALESORG_RECORD_ID FROM
                        SAQTSE (NOLOCK)
                        JOIN SAQSGE (NOLOCK) ON SAQSGE.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID AND SAQSGE.QTEREV_RECORD_ID = SAQTSE.QTEREV_RECORD_ID AND SAQSGE.SERVICE_ID = SAQTSE.SERVICE_ID 
                        JOIN SAQSCO (NOLOCK) ON SAQSCO.PAR_SERVICE_ID = SAQTSE.PAR_SERVICE_ID AND SAQSCO.SERVICE_ID = SAQTSE.SERVICE_ID AND SAQSCO.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID  AND SAQSCO.QTEREV_RECORD_ID = SAQTSE.QTEREV_RECORD_ID AND SAQSGE.GREENBOOK = SAQSCO.GREENBOOK
                        
                        LEFT JOIN SAQSCE (NOLOCK) ON SAQSGE.QUOTE_RECORD_ID = SAQSCE.QUOTE_RECORD_ID AND SAQSGE.QTEREV_RECORD_ID = SAQSCE.QTEREV_RECORD_ID AND SAQSGE.SERVICE_ID = SAQSCE.SERVICE_ID AND ISNULL(SAQSGE.GREENBOOK_RECORD_ID,'') = ISNULL(SAQSGE.GREENBOOK_RECORD_ID,'') AND SAQSCE.EQUIPMENT_ID = SAQSCO.EQUIPMENT_ID
                    WHERE SAQTSE.QUOTE_RECORD_ID ='{QuoteRecordId}'  AND SAQTSE.QTEREV_RECORD_ID = '{revision_rec_id}' AND SAQTSE.PAR_SERVICE_ID = '{ServiceId}' AND  SAQTSE.SERVICE_ID = '{Addon_ServiceId}' AND SAQSGE.GREENBOOK = '{greenbook}' AND ISNULL(SAQSCE.EQUIPMENT_ID,'') = ''
                    ) IQ
                """.format(UserId=User_Id, QuoteRecordId=OfferingRow_detail.QUOTE_RECORD_ID, ServiceId=OfferingRow_detail.SERVICE_ID, revision_rec_id = OfferingRow_detail.QTEREV_RECORD_ID,Addon_ServiceId = OfferingRow_detail.ADNPRD_ID,greenbook = greenbook))
    # NSO Auto Add Functionality
    nso_poss_id = []
    distinct_nso = Sql.GetList("SELECT DISTINCT POSS_NSO_PART_ID FROM SAQSCN WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'".format(QuoteRecordId = OfferingRow_detail.QUOTE_RECORD_ID,RevisionRecordId = OfferingRow_detail.QTEREV_RECORD_ID))
    if distinct_nso:
        for nso in distinct_nso:
            nso_poss_id.append(nso.POSS_NSO_PART_ID)
        # delete_nso = "DELETE FROM SAQSCN WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'".format(QuoteRecordId = OfferingRow_detail.QUOTE_RECORD_ID,RevisionRecordId = OfferingRow_detail.QTEREV_RECORD_ID)
        # Sql.RunQuery(delete_nso)
        eqp_query = Sql.GetList("SELECT DISTINCT EQUIPMENT_ID,QUOTE_ID,CONTRACT_VALID_FROM,CONTRACT_VALID_TO,EQUIPMENT_DESCRIPTION,EQUIPMENT_RECORD_ID,EQUIPMENT_STATUS,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,QTEREV_ID,QTESRVGBK_RECORD_ID,QTESRV_RECORD_ID,SERIAL_NO,TEMP_TOOL FROM SAQSCO WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID = 'Z0123' AND GREENBOOK = '{greenbook}' AND EQUIPMENT_ID NOT IN (SELECT EQUIPMENT_ID FROM SAQSCN (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID = 'Z0123')".format(QuoteRecordId = OfferingRow_detail.QUOTE_RECORD_ID,RevisionRecordId = OfferingRow_detail.QTEREV_RECORD_ID,greenbook = greenbook))
        for eqp in eqp_query:
            for nso in nso_poss_id:
                prlpbe_query = Sql.GetFirst("SELECT BUSINESS_UNIT,DIVISION_ID,DIVISION_RECORD_ID,GREENBOOK,GREENBOOK_RECORD_ID,POSS_NSO_DESCRIPTION,SAP_PART_NUMBER,POSS_COST,POSS_PRICE,POSS_NSO_PART_ID FROM PRLPBE WHERE POSS_NSO_PART_ID = '"+str(nso)+"'")

                nso_table_info = SqlHelper.GetTable("SAQSCN")
                if prlpbe_query.POSS_COST:
                    poss_cost = prlpbe_query.POSS_COST
                else:
                    poss_cost = 0
                if prlpbe_query.POSS_PRICE:
                    poss_price = prlpbe_query.POSS_PRICE
                else:
                    poss_price = 0
                # Trace.Write("poss_price "+str(poss_price)+" poss_cost "+str(poss_cost))
                nso_table = {
                    "QUOTE_REV_PO_EQUIPMENT_PARTS_RECORD_ID": str(Guid.NewGuid()).upper(),
                    "BUSINESS_UNIT": prlpbe_query.BUSINESS_UNIT,
                    "CONTRACT_VALID_FROM": eqp.CONTRACT_VALID_FROM,
                    "CONTRACT_VALID_TO": eqp.CONTRACT_VALID_TO,
                    "DIVISION_ID": prlpbe_query.DIVISION_ID,
                    "DIVISION_RECORD_ID": prlpbe_query.DIVISION_RECORD_ID,
                    "EQUIPMENT_DESCRIPTION": eqp.EQUIPMENT_DESCRIPTION,
                    "EQUIPMENT_ID": eqp.EQUIPMENT_ID,
                    "EQUIPMENT_RECORD_ID": eqp.EQUIPMENT_RECORD_ID,
                    "EQUIPMENT_STATUS": eqp.EQUIPMENT_STATUS,
                    "FABLOCATION_ID": eqp.FABLOCATION_ID,
                    "FABLOCATION_NAME": eqp.FABLOCATION_NAME,
                    "FABLOCATION_RECORD_ID": eqp.FABLOCATION_RECORD_ID,
                    "GREENBOOK": prlpbe_query.GREENBOOK,
                    "GREENBOOK_RECORD_ID": prlpbe_query.GREENBOOK_RECORD_ID,
                    "POSS_NSO_DESCRIPTION": prlpbe_query.POSS_NSO_DESCRIPTION,
                    "POSS_NSO_PART_ID": prlpbe_query.POSS_NSO_PART_ID, #A055S000P01-18196
                    "SERVICE_DESCRIPTION": eqp.SERVICE_DESCRIPTION,
                    "SERVICE_ID": eqp.SERVICE_ID,
                    "SERVICE_RECORD_ID": eqp.SERVICE_RECORD_ID,
                    "QUANTITY": 1,
                    "QUOTE_ID": eqp.QUOTE_ID,
                    "QUOTE_RECORD_ID": OfferingRow_detail.QUOTE_RECORD_ID,
                    "QTEREV_ID": eqp.QTEREV_ID,
                    "QTEREV_RECORD_ID": OfferingRow_detail.QTEREV_RECORD_ID,
                    "QTESRVGBK_RECORD_ID": eqp.QTESRVGBK_RECORD_ID,
                    "QTESRV_RECORD_ID": eqp.QTESRV_RECORD_ID,
                    "SAP_PART_NUMBER": prlpbe_query.SAP_PART_NUMBER,
                    "SERIAL_NO": eqp.SERIAL_NO,
                    "TEMP_TOOL": eqp.TEMP_TOOL,
                    "POSS_COST": prlpbe_query.POSS_COST,
                    "POSS_PRICE": prlpbe_query.POSS_PRICE,
                    "EXTENDED_POSS_COST": float(poss_cost) * 1,
                    "EXTENDED_POSS_PRICE": float(poss_price) * 1,
                    "INCLUDED": "True"
                } 
                nso_table_info.AddRow(nso_table)
                Sql.Upsert(nso_table_info)
    
    update_entitlement_col_val(OfferingRow_detail)

def _addon_rolldown_entitlement(OfferingRow_detail,greenbook):
    Sql.RunQuery("""INSERT SAQSGE (KB_VERSION,QUOTE_ID,QUOTE_NAME,QUOTE_RECORD_ID,QTEREV_RECORD_ID,QTEREV_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,PAR_SERVICE_ID, PAR_SERVICE_RECORD_ID, PAR_SERVICE_DESCRIPTION,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID, CPS_CONFIGURATION_ID, CPS_MATCH_ID,GREENBOOK,GREENBOOK_RECORD_ID,QTESRVENT_RECORD_ID,QTESRVGBK_RECORD_ID,ENTITLEMENT_XML,CONFIGURATION_STATUS, QUOTE_SERVICE_GREENBOOK_ENTITLEMENT_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED )
            SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_GREENBOOK_ENTITLEMENT_RECORD_ID, {UserId} as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM (SELECT DISTINCT SAQTSE.KB_VERSION,SAQTSE.QUOTE_ID,SAQTSE.QUOTE_NAME,SAQTSE.QUOTE_RECORD_ID,SAQTSE.QTEREV_RECORD_ID,SAQTSE.QTEREV_ID,SAQTSE.SERVICE_DESCRIPTION,SAQTSE.SERVICE_ID,SAQTSE.SERVICE_RECORD_ID,SAQTSE.PAR_SERVICE_ID,SAQTSE.PAR_SERVICE_RECORD_ID,SAQTSE.PAR_SERVICE_DESCRIPTION,SAQTSE.SALESORG_ID,SAQTSE.SALESORG_NAME,SAQTSE.SALESORG_RECORD_ID,	
            SAQTSE.CPS_CONFIGURATION_ID, SAQTSE.CPS_MATCH_ID,SAQSGB.GREENBOOK,SAQSGB.GREENBOOK_RECORD_ID,SAQTSE.QUOTE_SERVICE_ENTITLEMENT_RECORD_ID as QTESRVENT_RECORD_ID,SAQSGB.QUOTE_SERVICE_GREENBOOK_RECORD_ID as QTESRVGBK_RECORD_ID,SAQTSE.ENTITLEMENT_XML,SAQTSE.CONFIGURATION_STATUS FROM
        SAQTSE (NOLOCK) 
        JOIN SAQSGB  (NOLOCK) ON SAQSGB.SERVICE_ID = SAQTSE.SERVICE_ID AND SAQSGB.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID  AND SAQSGB.QTEREV_RECORD_ID = SAQTSE.QTEREV_RECORD_ID  AND SAQTSE.PAR_SERVICE_ID = SAQSGB.PAR_SERVICE_ID
        LEFT JOIN SAQSGE (NOLOCK) ON SAQSGE.QUOTE_RECORD_ID = SAQSGB.QUOTE_RECORD_ID AND SAQSGE.QTEREV_RECORD_ID = SAQSGB.QTEREV_RECORD_ID AND SAQSGE.SERVICE_ID = SAQSGB.SERVICE_ID AND ISNULL(SAQSGE.GREENBOOK_RECORD_ID,'') = ISNULL(SAQSGB.GREENBOOK_RECORD_ID,'')  AND SAQSGE.PAR_SERVICE_ID = SAQSGB.PAR_SERVICE_ID
            WHERE SAQTSE.QUOTE_RECORD_ID ='{QuoteRecordId}'  AND SAQTSE.QTEREV_RECORD_ID = '{revision_rec_id}' AND SAQTSE.PAR_SERVICE_ID = '{ServiceId}' AND  SAQTSE.SERVICE_ID = '{Addon_ServiceId}' AND SAQSGB.GREENBOOK = '{greenbook}' AND ISNULL(SAQSGE.GREENBOOK_RECORD_ID,'') = '' )IQ""".format(UserId=User_Id, QuoteRecordId=OfferingRow_detail.QUOTE_RECORD_ID, ServiceId=OfferingRow_detail.SERVICE_ID, revision_rec_id = OfferingRow_detail.QTEREV_RECORD_ID,Addon_ServiceId = OfferingRow_detail.ADNPRD_ID,greenbook = greenbook))

    # Sql.RunQuery(""" INSERT SAQSCE
    # 				(KB_VERSION,ENTITLEMENT_XML,CONFIGURATION_STATUS,PAR_SERVICE_ID,PAR_SERVICE_RECORD_ID,PAR_SERVICE_DESCRIPTION,EQUIPMENT_ID,EQUIPMENT_RECORD_ID,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_RECORD_ID,QTEREV_ID,QTESRVCOB_RECORD_ID,QTESRVENT_RECORD_ID,SERIAL_NO,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,CPS_CONFIGURATION_ID,CPS_MATCH_ID,GREENBOOK,GREENBOOK_RECORD_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,QUOTE_SERVICE_COVERED_OBJ_ENTITLEMENTS_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED) 
                    
    # 				SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_COVERED_OBJ_ENTITLEMENTS_RECORD_ID, {UserId} as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM (
    # 					SELECT 
    # 					SAQSGE.KB_VERSION,SAQSGE.ENTITLEMENT_XML,SAQSGE.CONFIGURATION_STATUS,SAQTSE.PAR_SERVICE_ID,SAQTSE.PAR_SERVICE_RECORD_ID,SAQTSE.PAR_SERVICE_DESCRIPTION,SAQSCO.EQUIPMENT_ID,SAQSCO.EQUIPMENT_RECORD_ID,SAQTSE.QUOTE_ID,SAQTSE.QUOTE_RECORD_ID,SAQTSE.QTEREV_RECORD_ID,SAQTSE.QTEREV_ID,SAQSCO.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID as QTESRVCOB_RECORD_ID,SAQTSE.QUOTE_SERVICE_ENTITLEMENT_RECORD_ID as QTESRVENT_RECORD_ID,SAQSCO.SERIAL_NO,SAQTSE.SERVICE_DESCRIPTION,SAQTSE.SERVICE_ID,SAQTSE.SERVICE_RECORD_ID,SAQSGE.CPS_CONFIGURATION_ID,SAQSGE.CPS_MATCH_ID,SAQSCO.GREENBOOK,SAQSCO.GREENBOOK_RECORD_ID,SAQSCO.FABLOCATION_ID,SAQSCO.FABLOCATION_NAME,SAQSCO.FABLOCATION_RECORD_ID,SAQTSE.SALESORG_ID,SAQTSE.SALESORG_NAME,SAQTSE.SALESORG_RECORD_ID FROM
    # 					SAQTSE (NOLOCK)
    # 					JOIN SAQSGE (NOLOCK) ON SAQSGE.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID AND SAQSGE.QTEREV_RECORD_ID = SAQTSE.QTEREV_RECORD_ID AND SAQSGE.SERVICE_ID = SAQTSE.SERVICE_ID 
    # 					JOIN SAQSCO (NOLOCK) ON SAQSCO.PAR_SERVICE_ID = SAQTSE.PAR_SERVICE_ID AND SAQSCO.SERVICE_ID = SAQTSE.SERVICE_ID AND SAQSCO.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID  AND SAQSCO.QTEREV_RECORD_ID = SAQTSE.QTEREV_RECORD_ID AND SAQSGE.GREENBOOK = SAQSCO.GREENBOOK
                        
    # 					LEFT JOIN SAQSCE (NOLOCK) ON SAQSGE.QUOTE_RECORD_ID = SAQSCE.QUOTE_RECORD_ID AND SAQSGE.QTEREV_RECORD_ID = SAQSCE.QTEREV_RECORD_ID AND SAQSGE.SERVICE_ID = SAQSCE.SERVICE_ID AND ISNULL(SAQSGE.GREENBOOK_RECORD_ID,'') = ISNULL(SAQSGE.GREENBOOK_RECORD_ID,'') AND SAQSCE.EQUIPMENT_ID = SAQSCO.EQUIPMENT_ID
    # 				WHERE SAQTSE.QUOTE_RECORD_ID ='{QuoteRecordId}'  AND SAQTSE.QTEREV_RECORD_ID = '{revision_rec_id}' AND SAQTSE.PAR_SERVICE_ID = '{ServiceId}' AND  SAQTSE.SERVICE_ID = '{Addon_ServiceId}' AND SAQSGE.GREENBOOK = '{greenbook}' AND ISNULL(SAQSCE.EQUIPMENT_ID,'') = ''
    # 				) IQ
    # 			""".format(UserId=User_Id, QuoteRecordId=OfferingRow_detail.QUOTE_RECORD_ID, ServiceId=OfferingRow_detail.SERVICE_ID, revision_rec_id = OfferingRow_detail.QTEREV_RECORD_ID,Addon_ServiceId = OfferingRow_detail.ADNPRD_ID,greenbook = greenbook))

    update_entitlement_col_val(OfferingRow_detail)
                                                    
def addon_operations(OfferingRow_detail,greenbook):	
    _addon_service_level_entitlement(OfferingRow_detail)
    # _addon_equipment_insert(OfferingRow_detail,greenbook)
    _addon_rolldown_entitlement(OfferingRow_detail,greenbook)


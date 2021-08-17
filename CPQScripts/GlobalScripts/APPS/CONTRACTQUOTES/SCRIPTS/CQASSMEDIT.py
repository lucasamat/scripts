# =========================================================================================================================================
#   __script_name : CQASSMEDIT.PY
#   __script_description : THIS SCRIPT IS USED TO EDIT THE ASSEMBLY LEVEL GRID FOR SENDING EQUIPMENT.
#   __primary_author__ : 
#   __create_date :8/17/2021
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import Webcom
from SYDATABASE import SQL
from datetime import datetime
import Webcom.Configurator.Scripting.Test.TestProduct
import time
Sql = SQL()
import SYCNGEGUID as CPQID
import System.Net


#A055S000P01-6826- Relocation chamber starts...
def UpdateAssemblyLevel(Values):
    #TreeParentParam = Product.GetGlobal("TreeParentLevel0")
    # TreeSuperParentParam = Product.GetGlobal("TreeParentLevel1")
    # TreeTopSuperParentParam =  Product.GetGlobal("TreeParentLevel2")
    #ContractRecordId = Quote.GetGlobal("contract_quote_record_id")
    record_ids = [
                CPQID.KeyCPQId.GetKEYId('SAQSSA', str(value))
                if value.strip() != "" and 'SAQSSA' in value
                else value
                for value in Values
            ]
    #Trace.Write('unselected_values---'+str(unselected_values))
    un_selected_record_ids = [
                CPQID.KeyCPQId.GetKEYId('SAQSSA', str(value))
                if value.strip() != "" and 'SAQSSA' in value
                else value
                for value in unselected_values
            ]
    record_ids = str(tuple(record_ids)).replace(",)",")")
    un_selected_record_ids = str(tuple(un_selected_record_ids)).replace(",)",")")
   # Trace.Write('record_ids------inside-'+str(record_ids))
    #Trace.Write('un_selected_record_ids------inside-'+str(un_selected_record_ids))
    try:
        equipment_id = Param.equipment_id
    except:
        equipment_id =""
    if record_ids != '()':
        Sql.RunQuery("update SAQSSA set INCLUDED = 1 where QUOTE_SERVICE_SENDING_FAB_EQUIP_ASS_ID in {} and QUOTE_RECORD_ID = '{}' and SERVICE_ID = '{}'".format(record_ids,ContractRecordId,TreeParentParam))
        #Sql.RunQuery("update SAQSCA set INCLUDED = 1 where QUOTE_SERVICE_SENDING_FAB_EQUIP_ASS_ID in {} and QUOTE_RECORD_ID = '{}' and SERVICE_ID = '{}'".format(record_ids,ContractRecordId,TreeParentParam))
    if un_selected_record_ids != '()':
        Sql.RunQuery("update SAQSSA set INCLUDED = 0 where QUOTE_SERVICE_SENDING_FAB_EQUIP_ASS_ID in {} and QUOTE_RECORD_ID = '{}' and SERVICE_ID = '{}'".format(un_selected_record_ids,ContractRecordId,TreeParentParam))
        #Sql.RunQuery("update SAQSCA set INCLUDED = 0 where QUOTE_SERVICE_SENDING_FAB_EQUIP_ASS_ID in {} and QUOTE_RECORD_ID = '{}' and SERVICE_ID = '{}'".format(un_selected_record_ids,ContractRecordId,TreeParentParam))
    if equipment_id:
        get_total_count = SqlHelper.GetFirst("""select count(*) as cnt from SAQSSA (NOLOCK) where SND_EQUIPMENT_ID = '{}' and EQUIPMENTTYPE_ID = 'CHAMBER' and QUOTE_RECORD_ID = '{}' and SERVICE_ID = '{}'""".format(equipment_id,ContractRecordId,TreeParentParam))
        included_count = SqlHelper.GetFirst("""select count(*) as cnt from SAQSSA (NOLOCK) where SND_EQUIPMENT_ID = '{}' and EQUIPMENTTYPE_ID = 'CHAMBER' and INCLUDED = 1 and QUOTE_RECORD_ID = '{}' and SERVICE_ID = '{}'""".format(equipment_id,ContractRecordId,TreeParentParam))
        if get_total_count.cnt == included_count.cnt:
            Sql.RunQuery("update SAQSSE set INCLUDED = 'TOOL' where SND_EQUIPMENT_ID ='{}' and QUOTE_RECORD_ID = '{}' and SERVICE_ID = '{}' ".format(equipment_id,ContractRecordId,TreeParentParam))
            Sql.RunQuery("update SAQSCO set INCLUDED = 'TOOL' where EQUIPMENT_ID ='{}' and QUOTE_RECORD_ID = '{}' and SERVICE_ID = '{}' ".format(equipment_id,ContractRecordId,TreeParentParam))
            if 'Z0007' in TreeParentParam:
                whereReq = "QUOTE_RECORD_ID = '{}' and SERVICE_ID = '{}' AND EQUIPMENT_ID = '{}'".format(ContractRecordId,TreeParentParam,equipment_id)
                add_where = "and INCLUDED = 'TOOL'"
                AttributeID = 'AGS_QUO_QUO_TYP'
                NewValue = 'Tool based' 
                update_flag = EntitlementUpdate(whereReq,add_where,AttributeID,NewValue)
        else:
            Sql.RunQuery("update SAQSSE set INCLUDED = 'CHAMBER' where SND_EQUIPMENT_ID ='{}' and QUOTE_RECORD_ID = '{}' and SERVICE_ID = '{}' ".format(equipment_id,ContractRecordId,TreeParentParam))
            Sql.RunQuery("update SAQSCO set INCLUDED = 'CHAMBER' where EQUIPMENT_ID ='{}' and QUOTE_RECORD_ID = '{}' and SERVICE_ID = '{}' ".format(equipment_id,ContractRecordId,TreeParentParam))
            if 'Z0007' in TreeParentParam:
                whereReq = "QUOTE_RECORD_ID = '{}' and SERVICE_ID = '{}' AND EQUIPMENT_ID = '{}'".format(ContractRecordId,TreeParentParam,equipment_id)
                add_where = "and INCLUDED = 'CHAMBER'"
                AttributeID = 'AGS_QUO_QUO_TYP'
                NewValue = 'Chamber based'
                update_flag = EntitlementUpdate(whereReq,add_where,AttributeID,NewValue)
                if update_flag:
                    ##Assembly level roll down
                    userId = User.Id
                    datetimenow = datetime.now().strftime("%m/%d/%Y %H:%M:%S %p")  

                    update_query = """ UPDATE TGT 
                        SET TGT.ENTITLEMENT_XML = SRC.ENTITLEMENT_XML,
                        TGT.CPS_MATCH_ID = SRC.CPS_MATCH_ID,
                        TGT.CPS_CONFIGURATION_ID = SRC.CPS_CONFIGURATION_ID,
                        TGT.CpqTableEntryModifiedBy = {},
                        TGT.CpqTableEntryDateModified = '{}'
                        FROM SAQSCE (NOLOCK) SRC JOIN SAQSAE (NOLOCK) TGT 
                        ON  TGT.QUOTE_RECORD_ID = SRC.QUOTE_RECORD_ID AND TGT.SERVICE_ID = SRC.SERVICE_ID AND SRC.EQUIPMENT_ID = TGT.EQUIPMENT_ID WHERE {} """.format(userId,datetimenow,whereReq)
                    Sql.RunQuery(update_query)
   
    return True

def EditAssemblyLevel(Values):
    #TreeParentParam = Product.GetGlobal("TreeParentLevel0")
    # TreeSuperParentParam = Product.GetGlobal("TreeParentLevel1")
    # TreeTopSuperParentParam =  Product.GetGlobal("TreeParentLevel2")
    #ContractRecordId = Quote.GetGlobal("contract_quote_record_id")
    #Trace.Write('Values----'+str(Values))
    get_rec = Sql.GetList("select SND_ASSEMBLY_ID from SAQSSA (NOLOCK) where SND_EQUIPMENT_ID = '{}' and EQUIPMENTTYPE_ID = 'CHAMBER' and QUOTE_RECORD_ID = '{}' and SERVICE_ID = '{}'".format(Values,ContractRecordId,TreeParentParam))
    chamber_res_list = [i.SND_ASSEMBLY_ID for i in get_rec]
    #Trace.Write('bb--'+str(chamber_res_list))
    return chamber_res_list

def EntitlementUpdate(whereReq,add_where,AttributeID,NewValue):
    #whereReq = "QUOTE_RECORD_ID = '{}' and SERVICE_ID = '{}' AND EQUIPMENT_ID = '{}'".format('50243B0C-C53B-4BE5-8923-939BB9DCEB73','Z0007','100000181')
    #add_where = "and INCLUDED = 'CHAMBER'""
    #AttributeID = 'AGS_QUO_QUO_TYP'
    #NewValue = 'Chamber based'
    get_equp_xml = Sql.GetFirst("select distinct CPS_MATCH_ID,ENTITLEMENT_XML,CPS_CONFIGURATION_ID FROM SAQSCE where {}".format(whereReq))
    get_query = Sql.GetFirst("select EQUIPMENT_ID FROM SAQSCO where {} {}".format(whereReq,add_where))
    if get_equp_xml and get_query:
        Trace.Write('inside')
        cpsmatchID = get_equp_xml.CPS_MATCH_ID
        cpsConfigID = get_equp_xml.CPS_CONFIGURATION_ID
        try:       
            Trace.Write("---requestdata--244-cpsConfigID0-----"+str(cpsmatchID)+'--'+str(cpsConfigID))
            webclient = System.Net.WebClient()
            webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/json"
            webclient.Headers[System.Net.HttpRequestHeader.Authorization] = "Basic c2ItYzQwYThiMWYtYzU5NS00ZWJjLTkyYzYtYzM4ODg4ODFmMTY0IWIyNTAzfGNwc2VydmljZXMtc2VjdXJlZCFiMzkxOm9zRzgvSC9hOGtkcHVHNzl1L2JVYTJ0V0FiMD0="
            response = webclient.DownloadString("https://cpqprojdevamat.authentication.us10.hana.ondemand.com:443/oauth/token?grant_type=client_credentials")
            response = eval(response)
            webclient = System.Net.WebClient()		
            Request_URL = "https://cpservices-product-configuration.cfapps.us10.hana.ondemand.com/api/v2/configurations/"+str(cpsConfigID)+"/items/1"
            webclient.Headers[System.Net.HttpRequestHeader.Authorization] = "Bearer " + str(response["access_token"])

            webclient.Headers.Add("If-Match", "1"+str(cpsmatchID))
                    
            #AttributeID = 'AGS_QUO_QUO_TYP'
            #NewValue = 'Chamber based'
            STANDARD_ATTRIBUTE_VALUES=Sql.GetList("SELECT S.STANDARD_ATTRIBUTE_VALUE,S.STANDARD_ATTRIBUTE_DISPLAY_VAL FROM STANDARD_ATTRIBUTE_VALUES (nolock) S INNER JOIN ATTRIBUTE_DEFN (NOLOCK) A ON A.STANDARD_ATTRIBUTE_CODE=S.STANDARD_ATTRIBUTE_CODE WHERE A.SYSTEM_ID = '{}' ".format(AttributeID))
            for val in STANDARD_ATTRIBUTE_VALUES:
                if val.STANDARD_ATTRIBUTE_DISPLAY_VAL == NewValue:
                    requestdata = '{"characteristics":[{"id":"'+AttributeID+'","values":[{"value":"'+str(val.STANDARD_ATTRIBUTE_VALUE)+'","selected":true}]}]}'
            Trace.Write("---eqruestdata---requestdata----"+str(requestdata))
            response2 = webclient.UploadString(Request_URL, "PATCH", str(requestdata))
            #requestdata = {"characteristics":[{"id":"' + AttributeID + '":[{"value":"' +NewValue+'","selected":true}]}]}

            #Log.Info(str(Request_URL)+"---requestdata--166---" + str(response2))


            #Log.Info("patch response1---170---" + str(response2))
            Request_URL = "https://cpservices-product-configuration.cfapps.us10.hana.ondemand.com/api/v2/configurations/"+str(cpsConfigID)
            webclient.Headers[System.Net.HttpRequestHeader.Authorization] = "Bearer " + str(response["access_token"])
            #Log.Info("requestdata---180--265----" + str(requestdata))
            response2 = webclient.DownloadString(Request_URL)
            Trace.Write('response2--182----267-----'+str(response2))
            response2 = str(response2).replace(": true", ': "true"').replace(": false", ': "false"')
            Fullresponse= eval(response2)
            attributesdisallowedlst=[]
            attributesallowedlst=[]
            multi_value = ""
            #overallattributeslist =[]
            attributevalues={}
            for rootattribute, rootvalue in Fullresponse.items():
                if rootattribute=="rootItem":
                    for Productattribute, Productvalue in rootvalue.items():
                        if Productattribute=="characteristics":
                            for prdvalue in Productvalue:
                                multi_value = ""
                                #overallattributeslist.append(prdvalue['id'])
                                if prdvalue['visible'] =='false':
                                    attributesdisallowedlst.append(prdvalue['id'])
                                else:
                                    #Trace.Write(prdvalue['id']+" set here")
                                    attributesallowedlst.append(prdvalue['id'])
                                
                                if len(prdvalue["values"]) == 1:
                                    #Trace.Write('ifffff'+str(prdvalue["id"]))
                                    attributevalues[str(prdvalue["id"])] = prdvalue['values'][0]['value']
                                elif len(prdvalue["values"]) > 1:
                                    #Trace.Write('else if'+str(prdvalue["id"]))
                                    for attribute in prdvalue["values"]:
                                        #Trace.Write('iiiii---'+str(attribute["value"])+'-'+str(prdvalue["id"]) )
                                        value_list = [attribute["value"] for attribute in prdvalue["values"]]
                                        #value_list = str(value_list)
                                    attributevalues[str(prdvalue["id"])] = value_list
                                # else:
                                #     Trace.Write('else'+str(prdvalue["id"]))

            
            attributesallowedlst = list(set(attributesallowedlst))
            #overallattributeslist = list(set(overallattributeslist))
            HasDefaultvalue=False
            Trace.Write('response2--182----315---'+str(attributesallowedlst))
            Trace.Write('attributevalues--182----315---'+str(attributevalues))
            ProductVersionObj=Sql.GetFirst("Select product_id from product_versions(nolock) where SAPKBId = '"+str(Fullresponse['kbId'])+"' AND SAPKBVersion='"+str(Fullresponse['kbKey']['version'])+"'")
            if ProductVersionObj is not None:
                #tbrow={}
                insertservice = ""
                for attrs in attributesallowedlst:
                    #Trace.Write('value code---'+str(attrs))
                    if attrs in attributevalues:
                        HasDefaultvalue=True
                        STANDARD_ATTRIBUTE_VALUES=Sql.GetFirst("SELECT S.STANDARD_ATTRIBUTE_DISPLAY_VAL,S.STANDARD_ATTRIBUTE_CODE FROM STANDARD_ATTRIBUTE_VALUES (nolock) S INNER JOIN ATTRIBUTE_DEFN (NOLOCK) A ON A.STANDARD_ATTRIBUTE_CODE=S.STANDARD_ATTRIBUTE_CODE WHERE A.SYSTEM_ID = '{}'".format(attrs,attributevalues[attrs]))
                        ent_disp_val = attributevalues[attrs]
                        ent_val_code = attributevalues[attrs]
                    else:
                        HasDefaultvalue=False
                        ent_disp_val = ""
                        ent_val_code = ""
                        STANDARD_ATTRIBUTE_VALUES=Sql.GetFirst("SELECT S.STANDARD_ATTRIBUTE_CODE FROM STANDARD_ATTRIBUTE_VALUES (nolock) S INNER JOIN ATTRIBUTE_DEFN (NOLOCK) A ON A.STANDARD_ATTRIBUTE_CODE=S.STANDARD_ATTRIBUTE_CODE WHERE A.SYSTEM_ID = '{}'".format(attrs))
                    ATTRIBUTE_DEFN=Sql.GetFirst("SELECT * FROM ATTRIBUTE_DEFN (NOLOCK) WHERE SYSTEM_ID='{}'".format(attrs))
                    
                    PRODUCT_ATTRIBUTES=Sql.GetFirst("SELECT A.ATT_DISPLAY_DESC FROM ATT_DISPLAY_DEFN (NOLOCK) A INNER JOIN PRODUCT_ATTRIBUTES (NOLOCK) P ON A.ATT_DISPLAY=P.ATT_DISPLAY WHERE P.PRODUCT_ID={} AND P.STANDARD_ATTRIBUTE_CODE={}".format(ProductVersionObj.product_id,STANDARD_ATTRIBUTE_VALUES.STANDARD_ATTRIBUTE_CODE))
                    
                    if PRODUCT_ATTRIBUTES.ATT_DISPLAY_DESC in ('Drop Down','DropDown') and ent_disp_val:
                        get_display_val = Sql.GetFirst("SELECT STANDARD_ATTRIBUTE_DISPLAY_VAL  from STANDARD_ATTRIBUTE_VALUES S INNER JOIN ATTRIBUTE_DEFN (NOLOCK) A ON A.STANDARD_ATTRIBUTE_CODE=S.STANDARD_ATTRIBUTE_CODE WHERE S.STANDARD_ATTRIBUTE_CODE = '{}' AND A.SYSTEM_ID = '{}' AND S.STANDARD_ATTRIBUTE_VALUE = '{}' ".format(STANDARD_ATTRIBUTE_VALUES.STANDARD_ATTRIBUTE_CODE,attrs,  attributevalues[attrs] ) )
                        ent_disp_val = get_display_val.STANDARD_ATTRIBUTE_DISPLAY_VAL 
                    elif PRODUCT_ATTRIBUTES.ATT_DISPLAY_DESC in ('Check Box') and ent_disp_val and ent_val_code:
                        Trace.Write('ent_val_code--'+str(type(ent_val_code))+'---'+str(ent_val_code))
                        if type(eval(str(ent_val_code))) is list:
                            ent_val = str(tuple(ent_val_code)).replace(',)',')')
                            get_display_val = Sql.GetList("SELECT STANDARD_ATTRIBUTE_DISPLAY_VAL  from STANDARD_ATTRIBUTE_VALUES S INNER JOIN ATTRIBUTE_DEFN (NOLOCK) A ON A.STANDARD_ATTRIBUTE_CODE=S.STANDARD_ATTRIBUTE_CODE WHERE S.STANDARD_ATTRIBUTE_CODE = '{}' AND A.SYSTEM_ID = '{}' AND S.STANDARD_ATTRIBUTE_VALUE in {} ".format(STANDARD_ATTRIBUTE_VALUES.STANDARD_ATTRIBUTE_CODE,attrs,  ent_val ) )
                            ent_disp_val = [i.STANDARD_ATTRIBUTE_DISPLAY_VAL for i in get_display_val ]
                            ent_disp_val = str(ent_disp_val).replace("'", '"')
                            ent_val_code = str(ent_val_code).replace("'", '"')
                        else:
                            get_display_val = Sql.GetFirst("SELECT STANDARD_ATTRIBUTE_DISPLAY_VAL  from STANDARD_ATTRIBUTE_VALUES S INNER JOIN ATTRIBUTE_DEFN (NOLOCK) A ON A.STANDARD_ATTRIBUTE_CODE=S.STANDARD_ATTRIBUTE_CODE WHERE S.STANDARD_ATTRIBUTE_CODE = '{}' AND A.SYSTEM_ID = '{}' AND S.STANDARD_ATTRIBUTE_VALUE = '{}' ".format(STANDARD_ATTRIBUTE_VALUES.STANDARD_ATTRIBUTE_CODE,attrs,  attributevalues[attrs] ) )
                            ent_disp_val = str(str(get_display_val.STANDARD_ATTRIBUTE_DISPLAY_VAL).split("'") ).replace("'", '"')
                            ent_val_code = str(str(ent_val_code).split(',') ).replace("'", '"')

                    
                    DTypeset={"Drop Down":"DropDown","Free Input, no Matching":"FreeInputNoMatching","Check Box":"Check Box"}
                    #Log.Info('response2--182----342-')
                    #Trace.Write('value code---'+str(attributevalues[attrs])+'--'+str(attrs))
                    insertservice += """<QUOTE_ITEM_ENTITLEMENT>
                    <ENTITLEMENT_NAME>{ent_name}</ENTITLEMENT_NAME>
                    <ENTITLEMENT_VALUE_CODE>{ent_val_code}</ENTITLEMENT_VALUE_CODE>
                    <ENTITLEMENT_TYPE>{ent_type}</ENTITLEMENT_TYPE>
                    <ENTITLEMENT_DESCRIPTION>{ent_desc}</ENTITLEMENT_DESCRIPTION>
                    <ENTITLEMENT_DISPLAY_VALUE>{ent_disp_val}</ENTITLEMENT_DISPLAY_VALUE>
                    <ENTITLEMENT_COST_IMPACT>{ct}</ENTITLEMENT_COST_IMPACT>
                    <ENTITLEMENT_PRICE_IMPACT>{pi}</ENTITLEMENT_PRICE_IMPACT>
                    <IS_DEFAULT>{is_default}</IS_DEFAULT>
                    <PRICE_METHOD>{pm}</PRICE_METHOD>
                    <CALCULATION_FACTOR>{cf}</CALCULATION_FACTOR>
                    </QUOTE_ITEM_ENTITLEMENT>""".format(ent_name = str(attrs),ent_val_code = ent_val_code,ent_type = DTypeset[PRODUCT_ATTRIBUTES.ATT_DISPLAY_DESC] if PRODUCT_ATTRIBUTES else  '',ent_desc = ATTRIBUTE_DEFN.STANDARD_ATTRIBUTE_NAME,ent_disp_val = ent_disp_val if HasDefaultvalue==True else '',ct = '',pi = '',is_default = '1',pm = '',cf = '')
                    cpsmatc_incr = int(cpsmatchID) + 10
                    #Trace.Write('cpsmatc_incr'+str(cpsmatc_incr))
                Updatecps = "UPDATE {} SET CPS_MATCH_ID ={},CPS_CONFIGURATION_ID = '{}',ENTITLEMENT_XML='{}' WHERE {} ".format('SAQSCE', cpsmatc_incr,cpsConfigID,insertservice, whereReq)
                Trace.Write('cpsmatc_incr'+str(cpsmatc_incr))
                Sql.RunQuery(Updatecps)
            
            return True
        except Exception,e:
            Trace.Write("except---"+str(e))

TreeParentParam = Product.GetGlobal("TreeParentLevel0")
ContractRecordId = Quote.GetGlobal("contract_quote_record_id")

if ACTION == 'UPDATE_ASSEMBLY':
    #selected_values = list(selected_values)
    #Trace.Write('values----'+str(selected_values))
    ApiResponse = ApiResponseFactory.JsonResponse(UpdateAssemblyLevel(selected_values))
elif ACTION == 'EDIT_ASSEMBLY':
    #Trace.Write('values----'+str(selected_values))
    ApiResponse = ApiResponseFactory.JsonResponse(EditAssemblyLevel(selected_values))
#A055S000P01-6826- Relocation chamber ends
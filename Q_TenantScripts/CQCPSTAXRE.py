# =========================================================================================================================================
#   __script_name : CQCPSTAXRE.PY
#   __script_description : THIS SCRIPT IS USED TO RETURN TAX FOR PRODUCT OFFERINGS
#   __primary_author__ : WASIM.ABDUL
#   __create_date :31-01-2022
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED -
# ==========================================================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct
import System.Net
import re
import datetime
from System.Text.Encoding import UTF8
from System import Convert
import sys
from SYDATABASE import SQL
Sql = SQL()
try:
    contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
except:
    contract_quote_record_id = ''

try:
    quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
    
except:
    quote_revision_record_id =  ""
try:
    def getting_cps_tax(service_id):
        Log.Info("Script name called for "+str(Quote.GetGlobal("contract_quote_record_id"))+" - "+str(service_id)+" - "+str(Quote.GetGlobal("quote_revision_record_id")))
        contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
        quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
        webclient = System.Net.WebClient()
        response = ''
        webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/x-www-form-urlencoded"
        cps_credential_obj = Sql.GetFirst("SELECT USER_NAME, PASSWORD, URL FROM SYCONF (NOLOCK) WHERE EXTERNAL_TABLE_NAME='CPS_VARIANT_PRICING'")
        if cps_credential_obj:
            response = webclient.DownloadString(cps_credential_obj.URL + '?grant_type=client_credentials&client_id=' + cps_credential_obj.USER_NAME + '&client_secret=' + cps_credential_obj.PASSWORD)
        response = eval(response)
        Request_URL="https://cpservices-pricing.cfapps.us10.hana.ondemand.com/api/v1/statelesspricing"
        webclient.Headers[System.Net.HttpRequestHeader.Authorization] ="Bearer "+str(response['access_token'])

        x = datetime.datetime.today()
        x= str(x)
        y = x.split(" ")
        contract_quote_obj = Sql.GetFirst("Select * from SAQTMT WHERE MASTER_TABLE_QUOTE_RECORD_ID ='{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}'".format(QuoteRecordId = contract_quote_record_id,QuoteRevisionRecordId=quote_revision_record_id))
        GetPricingProcedure = Sql.GetFirst("SELECT ISNULL(DIVISION_ID, '') as DIVISION_ID,ISNULL(COUNTRY, '') as COUNTRY, ISNULL(DISTRIBUTIONCHANNEL_ID, '') as DISTRIBUTIONCHANNEL_ID, ISNULL(SALESORG_ID, '') as SALESORG_ID, ISNULL(DOC_CURRENCY,'') as DOC_CURRENCY, ISNULL(PRICINGPROCEDURE_ID,'') as PRICINGPROCEDURE_ID, QUOTE_RECORD_ID,ACCTAXCLA_ID,EXCHANGE_RATE_TYPE FROM SAQTRV (NOLOCK) WHERE QUOTE_ID = '{QuoteId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}'".format(QuoteId = contract_quote_obj.QUOTE_ID,QuoteRevisionRecordId=quote_revision_record_id))
        if GetPricingProcedure is not None:			
            PricingProcedure = GetPricingProcedure.PRICINGPROCEDURE_ID
            curr = GetPricingProcedure.DOC_CURRENCY
            dis = GetPricingProcedure.DISTRIBUTIONCHANNEL_ID
            salesorg = GetPricingProcedure.SALESORG_ID
            div = GetPricingProcedure.DIVISION_ID
            exch = GetPricingProcedure.EXCHANGE_RATE_TYPE
            taxk1 = GetPricingProcedure.ACCTAXCLA_ID
            country = GetPricingProcedure.COUNTRY
        STPObj=Sql.GetFirst("SELECT ACCOUNT_ID FROM SAOPQT (NOLOCK) WHERE QUOTE_ID ='{quote}'".format(quote=contract_quote_obj.QUOTE_ID))		
        stp_account_id = ""
        if STPObj:
            stp_account_id = str(STPObj.ACCOUNT_ID)		
        tax_classification = None
        quote_item_obj =Sql.GetFirst("SELECT MAMSCT.TAXCLASSIFICATION_ID FROM SAQTRV (NOLOCK) LEFT JOIN MAMSCT (NOLOCK) ON MAMSCT.DISTRIBUTIONCHANNEL_RECORD_ID = SAQTRV.DISTRIBUTIONCHANNEL_RECORD_ID AND MAMSCT.COUNTRY_RECORD_ID = SAQTRV.COUNTRY_RECORD_ID AND MAMSCT.SAP_PART_NUMBER = '{ServiceId}' AND MAMSCT.SALESORG_ID = SAQTRV.SALESORG_ID WHERE SAQTRV.QUOTE_RECORD_ID ='{QuoteRecordId}' AND SAQTRV.QTEREV_RECORD_ID = '{RevisionRecordId}'".format(QuoteRecordId=contract_quote_record_id, RevisionRecordId=quote_revision_record_id, ServiceId=service_id))
        if quote_item_obj:
            tax_classification = quote_item_obj.TAXCLASSIFICATION_ID
        itemid = 1  
        #TreeParam = Product.GetGlobal("TreeParam")	
        #Service_id = TreeParam.split('-')[1].strip()
        if tax_classification:			
            item_string = '{"itemId":"'+str(itemid)+'","externalId":null,"quantity":{"value":'+str(1)+',"unit":"EA"},"exchRateType":"'+str(exch)+'","exchRateDate":"'+str(y[0])+'","productDetails":{"productId":"'+str(service_id)+'","baseUnit":"EA","alternateProductUnits":null},"attributes":[{"name":"KOMK-LAND1","values":["'+country+'"]},{"name":"KOMK-ALAND","values":["'+country+'"]},{"name":"KOMK-REGIO","values":["TX"]},{"name":"KOMK-KUNNR","values":["'+stp_account_id+'"]},{"name":"KOMK-KUNWE","values":["'+stp_account_id+'"]},{"name":"KOMP-TAXM1","values":["'+str(tax_classification)+'"]},{"name":"KOMK-TAXK1","values":["'+str(taxk1)+'"]},{"name":"KOMK-SPART","values":["'+str(div)+'"]},{"name":"KOMP-SPART","values":["'+str(div)+'"]},{"name":"KOMP-PMATN","values":["'+str(service_id)+'"]},{"name":"KOMK-WAERK","values":["'+str(curr)+'"]},{"name":"KOMK-HWAER","values":["'+str(curr)+'"]},{"name":"KOMP-PRSFD","values":["X"]},{"name":"KOMK-ZZKTOKD","values":["KUNA"]},{"name":"KOMK-VTWEG","values":["'+str(dis)+'"]},{"name":"KOMK-VKORG","values":["'+str(salesorg)+'"]},{"name":"KOMP-KPOSN","values":["0"]},{"name":"KOMP-KZNEP","values":[""]},{"name":"KOMP-ZZEXE","values":["true"]}],"accessDateList":[{"name":"KOMK-PRSDT","value":"'+str(y[0])+'"},{"name":"KOMK-FBUDA","value":"'+str(y[0])+'"}],"variantConditions":[],"statistical":true,"subItems":[]}'
            requestdata = '{"docCurrency":"'+curr+'","locCurrency":"'+curr+'","pricingProcedure":"'+PricingProcedure+'","groupCondition":false,"itemConditionsRequired":true,"items": ['+str(item_string)+']}'
            Trace.Write("requestdata======>>>> "+str(requestdata))
            response1 = webclient.UploadString(Request_URL,str(requestdata))			
            response1 = str(response1).replace(": true", ': "true"').replace(": false", ': "false"').replace(": null",': " None"')
            response1 = eval(response1)
            Trace.Write("response1 ===> "+str(response1))
            price = []
            for root, value in response1.items():
                if root == "items":
                    price = value[:]
                    break
            tax_percentage = 0
            for data in price[0]['conditions']:
                if data['conditionType'] == 'ZWSC' and data['conditionTypeDescription'] == 'VAT Asia':
                    tax_percentage = data['conditionRate']
                    break
            update_tax = "UPDATE SAQRIS SET TAX_PERCENTAGE = {TaxPercentage} WHERE SAQRIS.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQRIS.QUOTE_RECORD_ID ='{QuoteRecordId}' AND SERVICE_ID = '{service_id}'".format(TaxPercentage=tax_percentage,service_id=service_id,QuoteRecordId = contract_quote_record_id,QuoteRevisionRecordId=quote_revision_record_id)
            Sql.RunQuery(update_tax)
        else:
            Log.Info("TAX CLASSIFICATION EMPTY FOR THE QUOTE "+str(contract_quote_obj.QUOTE_ID))

    def getting_cps_tax_item(service_id):
        contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
        quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
        webclient = System.Net.WebClient()
        response = ''
        webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/x-www-form-urlencoded"
        cps_credential_obj = Sql.GetFirst("SELECT USER_NAME, PASSWORD, URL FROM SYCONF (NOLOCK) WHERE EXTERNAL_TABLE_NAME='CPS_VARIANT_PRICING'")
        if cps_credential_obj:
            response = webclient.DownloadString(cps_credential_obj.URL + '?grant_type=client_credentials&client_id=' + cps_credential_obj.USER_NAME + '&client_secret=' + cps_credential_obj.PASSWORD)
        response = eval(response)
        Request_URL="https://cpservices-pricing.cfapps.us10.hana.ondemand.com/api/v1/statelesspricing"
        webclient.Headers[System.Net.HttpRequestHeader.Authorization] ="Bearer "+str(response['access_token'])

        x = datetime.datetime.today()
        x= str(x)
        y = x.split(" ")
        contract_quote_obj = Sql.GetFirst("Select * from SAQTMT WHERE MASTER_TABLE_QUOTE_RECORD_ID ='{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}'".format(QuoteRecordId = contract_quote_record_id,QuoteRevisionRecordId=quote_revision_record_id))
        GetPricingProcedure = Sql.GetFirst("SELECT ISNULL(DIVISION_ID, '') as DIVISION_ID,ISNULL(COUNTRY, '') as COUNTRY, ISNULL(DISTRIBUTIONCHANNEL_ID, '') as DISTRIBUTIONCHANNEL_ID, ISNULL(SALESORG_ID, '') as SALESORG_ID, ISNULL(DOC_CURRENCY,'') as DOC_CURRENCY, ISNULL(PRICINGPROCEDURE_ID,'') as PRICINGPROCEDURE_ID, QUOTE_RECORD_ID,ACCTAXCLA_ID,EXCHANGE_RATE_TYPE,ISNULL(ACCTAXCAT_ID, '') as ACCTAXCAT_ID,ISNULL(ACCTAXCAT_DESCRIPTION, '') as ACCTAXCAT_DESCRIPTION FROM SAQTRV (NOLOCK) WHERE QUOTE_ID = '{QuoteId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}'".format(QuoteId = contract_quote_obj.QUOTE_ID,QuoteRevisionRecordId=quote_revision_record_id))
        if GetPricingProcedure is not None:			
            PricingProcedure = GetPricingProcedure.PRICINGPROCEDURE_ID
            curr = GetPricingProcedure.DOC_CURRENCY
            dis = GetPricingProcedure.DISTRIBUTIONCHANNEL_ID
            salesorg = GetPricingProcedure.SALESORG_ID
            div = GetPricingProcedure.DIVISION_ID
            exch = GetPricingProcedure.EXCHANGE_RATE_TYPE
            taxk1 = GetPricingProcedure.ACCTAXCLA_ID 
            country = GetPricingProcedure.COUNTRY
            tax_cat_des =GetPricingProcedure.ACCTAXCAT_DESCRIPTION
            tax_cat_id =GetPricingProcedure.ACCTAXCAT_ID
        STPObj=Sql.GetFirst("SELECT ACCOUNT_ID FROM SAOPQT (NOLOCK) WHERE QUOTE_ID ='{quote}'".format(quote=contract_quote_obj.QUOTE_ID))		
        stp_account_id = ""
        if STPObj:
            stp_account_id = str(STPObj.ACCOUNT_ID)		
        tax_classification = None
        if service_id =="Z0105":
            get_tax_class_des = Sql.GetList("Select DISTINCT SRV_SPT_ENT as TAX_CLASS_DESC FROM SAQITE(NOLOCK) WHERE QUOTE_RECORD_ID ='{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SERVICE_ID ='{service_id}'".format(QuoteRecordId = contract_quote_record_id,QuoteRevisionRecordId=quote_revision_record_id,service_id=service_id))
        else:
            get_tax_class_des = Sql.GetList("Select DISTINCT SPR_SPT_ENT as TAX_CLASS_DESC FROM SAQITE(NOLOCK) WHERE QUOTE_RECORD_ID ='{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SERVICE_ID ='{service_id}'".format(QuoteRecordId = contract_quote_record_id,QuoteRevisionRecordId=quote_revision_record_id,service_id=service_id))
        item_string = ''
        itemid = 0
        request_item_details = {}
        for desc in get_tax_class_des:
            get_tax_class_des =Sql.GetFirst("Select TAX_CLASSIFICATION_ID FROM PRTXCL(NOLOCK) WHERE TAX_CLASSIFICATION_DESCRIPTION ='{tax_class_des}' AND TAXCATEGORY_DESCRIPTION ='{tax_cat_des}' AND TAXCATEGORY_ID ='{tax_cat_id}' AND TAX_CLASSIFICATION_TYPE ='MATERIAL'".format(tax_class_des = desc.TAX_CLASS_DESC,tax_cat_des=tax_cat_des,tax_cat_id=tax_cat_id))
            if get_tax_class_des:
                tax_classification = get_tax_class_des.TAX_CLASSIFICATION_ID
            itemid+= 1 
            request_item_details[itemid] = desc.TAX_CLASS_DESC
            if tax_classification:			
                item_string += '{"itemId":"'+str(itemid)+'","externalId":null,"quantity":{"value":'+str(1)+',"unit":"EA"},"exchRateType":"'+str(exch)+'","exchRateDate":"'+str(y[0])+'","productDetails":{"productId":"'+str(service_id)+'","baseUnit":"EA","alternateProductUnits":null},"attributes":[{"name":"KOMK-LAND1","values":["'+country+'"]},{"name":"KOMK-ALAND","values":["'+country+'"]},{"name":"KOMK-REGIO","values":["TX"]},{"name":"KOMK-KUNNR","values":["'+stp_account_id+'"]},{"name":"KOMK-KUNWE","values":["'+stp_account_id+'"]},{"name":"KOMP-TAXM1","values":["'+str(tax_classification)+'"]},{"name":"KOMK-TAXK1","values":["'+str(taxk1)+'"]},{"name":"KOMK-SPART","values":["'+str(div)+'"]},{"name":"KOMP-SPART","values":["'+str(div)+'"]},{"name":"KOMP-PMATN","values":["'+str(service_id)+'"]},{"name":"KOMK-WAERK","values":["'+str(curr)+'"]},{"name":"KOMK-HWAER","values":["'+str(curr)+'"]},{"name":"KOMP-PRSFD","values":["X"]},{"name":"KOMK-ZZKTOKD","values":["KUNA"]},{"name":"KOMK-VTWEG","values":["'+str(dis)+'"]},{"name":"KOMK-VKORG","values":["'+str(salesorg)+'"]},{"name":"KOMP-KPOSN","values":["0"]},{"name":"KOMP-KZNEP","values":[""]},{"name":"KOMP-ZZEXE","values":["true"]}],"accessDateList":[{"name":"KOMK-PRSDT","value":"'+str(y[0])+'"},{"name":"KOMK-FBUDA","value":"'+str(y[0])+'"}],"variantConditions":[],"statistical":true,"subItems":[]},'
        requestdata = '{"docCurrency":"'+curr+'","locCurrency":"'+curr+'","pricingProcedure":"'+PricingProcedure+'","groupCondition":false,"itemConditionsRequired":true,"items": ['+str(item_string)[:-1]+']}'
        Trace.Write("requestdata======>>>> "+str(requestdata))
        response1 = webclient.UploadString(Request_URL,str(requestdata))			
        response1 = str(response1).replace(": true", ': "true"').replace(": false", ': "false"').replace(": null",': " None"')
        response1 = eval(response1)
        Trace.Write("response1 ===> "+str(response1))
        Log.Info("========response======"+str(response1))
        price = []
        for root, value in response1.items():
            if root == "items":
                price = value[:]
                break
        
        total_tax_values = {}
        for value in price:
            Trace.Write(value['itemId']+"--------"+str(request_item_details))
            tax_classification_desc = request_item_details.get(int(value['itemId']))
            for data in value['conditions']:
                if data['conditionType'] == 'ZWSC' and data['conditionTypeDescription'] == 'VAT Asia':                
                    total_tax_values[tax_classification_desc] = data['conditionRate']            
        Trace.Write("tax_percentage"+str(total_tax_values))
        if service_id =="Z0105":
            for tax_desc, tax_value in total_tax_values.items():
                update_tax_child = "UPDATE A SET A.TAX_PERCENTAGE = {tax_value}, TAXCLASSIFICATION_DESCRIPTION ='{tax_desc}'  FROM SAQRIT A(NOLOCK) JOIN SAQITE B(NOLOCK) on A.LINE = B.LINE and A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.QTEREV_RECORD_ID = B.QTEREV_RECORD_ID and A.SERVICE_ID =B.SERVICE_ID LEFT JOIN PRTXCL(NOLOCK) ON PRTXCL.TAX_CLASSIFICATION_DESCRIPTION =B.SRV_SPT_ENT AND PRTXCL.TAXCATEGORY_DESCRIPTION ='{tax_cat_des}' AND PRTXCL.TAXCATEGORY_ID ='{tax_cat_id}' AND PRTXCL.TAX_CLASSIFICATION_TYPE ='MATERIAL' Where A.QUOTE_RECORD_ID='{QuoteRecordId}' and A.QTEREV_RECORD_ID='{QuoteRevisionRecordId}' and A.SERVICE_ID= '{service_id}' and B.SRV_SPT_ENT ='{tax_desc}'".format(tax_desc=tax_desc,tax_value=tax_value,service_id=service_id,QuoteRecordId = contract_quote_record_id,QuoteRevisionRecordId=quote_revision_record_id,tax_cat_des=tax_cat_des,tax_cat_id=tax_cat_id)
                Log.Info("update_tax_child"+str(update_tax_child))
                #Trace.Write(update_tax)
                Sql.RunQuery(update_tax_child)       
        else:
            for tax_desc, tax_value in total_tax_values.items():
                update_tax = "UPDATE A SET A.TAX_PERCENTAGE = {tax_value}, TAXCLASSIFICATION_DESCRIPTION ='{tax_desc}' FROM SAQRIT A(NOLOCK) JOIN SAQITE B(NOLOCK) on A.LINE = B.LINE and A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.QTEREV_RECORD_ID = B.QTEREV_RECORD_ID and A.SERVICE_ID =B.SERVICE_ID LEFT JOIN PRTXCL(NOLOCK) ON PRTXCL.TAX_CLASSIFICATION_DESCRIPTION =B.SPR_SPT_ENT AND PRTXCL.TAXCATEGORY_DESCRIPTION ='{tax_cat_des}' AND PRTXCL.TAXCATEGORY_ID ='{tax_cat_id}' AND PRTXCL.TAX_CLASSIFICATION_TYPE ='MATERIAL' Where A.QUOTE_RECORD_ID='{QuoteRecordId}' and A.QTEREV_RECORD_ID='{QuoteRevisionRecordId}' and A.SERVICE_ID= '{service_id}' and B.SPR_SPT_ENT ='{tax_desc}'".format(tax_desc=tax_desc,tax_value=tax_value,service_id=service_id,QuoteRecordId = contract_quote_record_id,QuoteRevisionRecordId=quote_revision_record_id,tax_cat_des=tax_cat_des,tax_cat_id=tax_cat_id)
                Log.Info("update_tax_parent"+str(update_tax))
                #Trace.Write(update_tax)
                Sql.RunQuery(update_tax)
        # Update tax percentage in annualized items
        update_tax = "UPDATE SAQICO SET SAQICO.TAXVTP = SAQRIT.TAX_PERCENTAGE FROM SAQICO (NOLOCK) JOIN SAQRIT (NOLOCK) ON SAQRIT.LINE = SAQICO.LINE AND SAQRIT.QUOTE_RECORD_ID = SAQICO.QUOTE_RECORD_ID AND SAQRIT.QTEREV_RECORD_ID = SAQICO.QTEREV_RECORD_ID AND SAQRIT.SERVICE_ID=SAQICO.SERVICE_ID WHERE SAQRIT.QUOTE_RECORD_ID='{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID='{QuoteRevisionRecordId}' AND SAQRIT.SERVICE_ID= '{ServiceId}'".format(ServiceId=service_id,QuoteRecordId = contract_quote_record_id,QuoteRevisionRecordId=quote_revision_record_id)                
        Sql.RunQuery(update_tax)

    service_id = Param.service_id
    Fun_type = Param.Fun_type
    if len(Fun_type) > 0:
        if str(Fun_type).upper() == 'CPQ_TO_ECC':
            Funtion_call = getting_cps_tax(service_id)
        else:
            Funtion_call = getting_cps_tax_item(service_id) 

except:
    Log.Info("CQCPSTAXRE ERROR---->:" + str(sys.exc_info()[1]))
    Log.Info("CQCPSTAXRE ERROR LINE NO---->:" + str(sys.exc_info()[-1].tb_lineno))

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
        Log.Info("Function_call_cps")
        contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
        quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
        webclient = System.Net.WebClient()
        webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/json"
        webclient.Headers[System.Net.HttpRequestHeader.Authorization] = "Basic c2ItYzQwYThiMWYtYzU5NS00ZWJjLTkyYzYtYzM4ODg4ODFmMTY0IWIyNTAzfGNwc2VydmljZXMtc2VjdXJlZCFiMzkxOm9zRzgvSC9hOGtkcHVHNzl1L2JVYTJ0V0FiMD0=";
        response = webclient.DownloadString("https://cpqprojdevamat.authentication.us10.hana.ondemand.com:443/oauth/token?grant_type=client_credentials")
        response = eval(response)
        
        Request_URL="https://cpservices-pricing.cfapps.us10.hana.ondemand.com/api/v1/statelesspricing"
        webclient.Headers[System.Net.HttpRequestHeader.Authorization] ="Bearer "+str(response['access_token'])

        x = datetime.datetime.today()
        x= str(x)
        y = x.split(" ")
        contract_quote_obj = Sql.GetFirst("Select * from SAQTMT WHERE MASTER_TABLE_QUOTE_RECORD_ID ='{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}'".format(QuoteRecordId = contract_quote_record_id,QuoteRevisionRecordId=quote_revision_record_id))
        GetPricingProcedure = Sql.GetFirst("SELECT ISNULL(DIVISION_ID, '') as DIVISION_ID,ISNULL(COUNTRY, '') as COUNTRY, ISNULL(DISTRIBUTIONCHANNEL_ID, '') as DISTRIBUTIONCHANNEL_ID, ISNULL(SALESORG_ID, '') as SALESORG_ID, ISNULL(DOC_CURRENCY,'') as DOC_CURRENCY, ISNULL(PRICINGPROCEDURE_ID,'') as PRICINGPROCEDURE_ID, QUOTE_RECORD_ID,ACCTAXCLA_ID,EXCHANGE_RATE_TYPE FROM SAQTRV (NOLOCK) WHERE QUOTE_ID = '{}'".format(contract_quote_obj.QUOTE_ID))
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
            
        itemid = 1
        item_obj = 1    
        #TreeParam = Product.GetGlobal("TreeParam")	
        #Service_id = TreeParam.split('-')[1].strip()
        if item_obj:			
            item_string = '{"itemId":"'+str(itemid)+'","externalId":null,"quantity":{"value":'+str(1)+',"unit":"EA"},"exchRateType":"'+str(exch)+'","exchRateDate":"'+str(y[0])+'","productDetails":{"productId":"'+str(service_id)+'","baseUnit":"EA","alternateProductUnits":null},"attributes":[{"name":"KOMK-LAND1","values":["'+country+'"]},{"name":"KOMK-ALAND","values":["'+country+'"]},{"name":"KOMK-REGIO","values":["TX"]},{"name":"KOMK-KUNNR","values":["'+stp_account_id+'"]},{"name":"KOMK-KUNWE","values":["'+stp_account_id+'"]},{"name":"KOMP-TAXM1","values":["'+str(item_obj)+'"]},{"name":"KOMK-TAXK1","values":["'+str(taxk1)+'"]},{"name":"KOMK-SPART","values":["'+str(div)+'"]},{"name":"KOMP-SPART","values":["'+str(div)+'"]},{"name":"KOMP-PMATN","values":["'+str(service_id)+'"]},{"name":"KOMK-WAERK","values":["'+str(curr)+'"]},{"name":"KOMK-HWAER","values":["'+str(curr)+'"]},{"name":"KOMP-PRSFD","values":["X"]},{"name":"KOMK-ZZKTOKD","values":["KUNA"]},{"name":"KOMK-VTWEG","values":["'+str(dis)+'"]},{"name":"KOMK-VKORG","values":["'+str(salesorg)+'"]},{"name":"KOMP-KPOSN","values":["0"]},{"name":"KOMP-KZNEP","values":[""]},{"name":"KOMP-ZZEXE","values":["true"]}],"accessDateList":[{"name":"KOMK-PRSDT","value":"'+str(y[0])+'"},{"name":"KOMK-FBUDA","value":"'+str(y[0])+'"}],"variantConditions":[],"statistical":true,"subItems":[]}'
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
            Log.Info("tax_percentage"+str(tax_percentage))
            update_tax = "UPDATE SAQRIS SET TAX_PERCENTAGE = {TaxPercentage} WHERE SAQRIS.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQRIS.QUOTE_RECORD_ID ='{QuoteRecordId}' AND SERVICE_ID = '{service_id}'".format(TaxPercentage=tax_percentage,service_id=service_id,QuoteRecordId = contract_quote_record_id,QuoteRevisionRecordId=quote_revision_record_id)
            Sql.RunQuery(update_tax)


    service_id = Param.service_id
    Fun_type = Param.Fun_type
    if len(Fun_type) > 0:
        if str(Fun_type).upper() == 'CPQ_TO_ECC':
            Funtion_call = getting_cps_tax(service_id)


except:
    Log.Info("CQCPSTAXRE ERROR---->:" + str(sys.exc_info()[1]))
    Log.Info("CQCPSTAXRE ERROR LINE NO---->:" + str(sys.exc_info()[-1].tb_lineno))

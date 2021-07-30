# =========================================================================================================================================
#   __script_name : CQPRTPRCUP.py
#   __script_description : THIS SCRIPT IS USED FOR CPS PART PRICING 
#   __primary_author__ : 
#   __create_date :23-10-2020
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct
import clr
#clr.AddReference("System.Net")
clr.AddReference("IronPython")
clr.AddReference("Microsoft.Scripting")
from System.Net import WebRequest
from System.Net import HttpWebResponse
from Microsoft.Scripting import SourceCodeKind
from IronPython.Hosting import Python
from IronPython import Compiler
#import Webcom.Configurator.Scripting.Test.TestProduct
import System.Net
import sys
import datetime
from System.Text.Encoding import UTF8
from System import Convert
from SYDATABASE import SQL
import time
import datetime 



Sql = SQL()
QUOTE = Param.CPQ_Columns['Entries']
script_start_time = time.time()
Log.Info("QUOTE ID---> "+str(QUOTE)+"CPS Price Script Started")
Log.Info("------->CPI Hitting  2021")
webclient = System.Net.WebClient()
webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/json"
webclient.Headers[System.Net.HttpRequestHeader.Authorization] = "Basic c2ItYzQwYThiMWYtYzU5NS00ZWJjLTkyYzYtYzM4ODg4ODFmMTY0IWIyNTAzfGNwc2VydmljZXMtc2VjdXJlZCFiMzkxOm9zRzgvSC9hOGtkcHVHNzl1L2JVYTJ0V0FiMD0=";
response = webclient.DownloadString("https://cpqprojdevamat.authentication.us10.hana.ondemand.com:443/oauth/token?grant_type=client_credentials")
response = eval(response)
Request_URL="https://cpservices-pricing.cfapps.us10.hana.ondemand.com/api/v1/statelesspricing"
webclient.Headers[System.Net.HttpRequestHeader.Authorization] ="Bearer "+str(response['access_token'])

Log.Info("654 response['access_token'] --->"+str(response['access_token']))


x = datetime.datetime.today()
x= str(x)
y = x.split(" ")
#partids = []
all_count = 0
loop_count = 0
#GET PRICING PROCEDURE
contract_quote_record_id = None
GetPricingProcedure = Sql.GetFirst("SELECT EXCHANGE_RATE_TYPE,DIVISION_ID, DISTRIBUTIONCHANNEL_ID, SALESORG_ID, SORG_CURRENCY, PRICINGPROCEDURE_ID,ISNULL(CUSTAXCLA_ID,1) as CUSTAXCLA_ID, QUOTE_RECORD_ID FROM SAQTSO (NOLOCK) WHERE QUOTE_ID = '{}'".format(QUOTE))
if GetPricingProcedure is not None:
    #PricingProcedure = GetPricingProcedure.PRICINGPROCEDURE_ID
    PricingProcedure = GetPricingProcedure.PRICINGPROCEDURE_ID
    curr = GetPricingProcedure.SORG_CURRENCY
    dis = GetPricingProcedure.DISTRIBUTIONCHANNEL_ID
    salesorg = GetPricingProcedure.SALESORG_ID
    div = GetPricingProcedure.DIVISION_ID
    exch = GetPricingProcedure.EXCHANGE_RATE_TYPE
    contract_quote_record_id = GetPricingProcedure.QUOTE_RECORD_ID
    taxk1 = GetPricingProcedure.CUSTAXCLA_ID
#else:
#PricingProcedure = 'RVCEU1'
"""curr = 'USD'
dis = '01'
salesorg = '2044'
div = '98' """

#UPDATE PRICING PROCEDURE TO SAQITM


update_SAQITM = "UPDATE SAQITM SET PRICINGPROCEDURE_ID = '{prc}' WHERE SAQITM.QUOTE_ID = '{quote}'".format(prc=str(PricingProcedure), quote=QUOTE)
Sql.RunQuery(update_SAQITM)
""" update_SAQIFP = "UPDATE SAQIFP SET PRICINGPROCEDURE_ID = '{prc}' WHERE SAQIFP.QUOTE_ID = '{quote}'".format(prc=str(PricingProcedure), quote=QUOTE)
Sql.RunQuery(update_SAQIFP) """
""" except:
    Trace.Write("EXCEPT ERROR FOR PRC PROCEDURE UPDATE") """


STPObj=Sql.GetFirst("SELECT ACCOUNT_ID FROM SAOPQT (NOLOCK) WHERE QUOTE_ID ='{quote}'".format(quote=QUOTE))
#SAQTSOObj=SqlHelper.GetFirst("SELECT SALESORG_ID,DISTRIBUTIONCHANNEL_ID,DIVISION_ID,SORG_CURRENCY FROM SAQTSO (NOLOCK) WHERE QUOTE_ID ='{quote}'".format(quote=QUOTE))
stp_account_id = ""
if STPObj:
    stp_account_id = str(STPObj.ACCOUNT_ID)

today = datetime.datetime.now()
Modi_date = today.strftime("%m/%d/%Y %H:%M:%S %p")

#Log.Info("CQPRTPRCUP  start time ---->"+str(Modi_date))

start = 1
end = 1000
L = 1

Taxm1Qurey=Sql.GetFirst("SELECT ISNULL(SRVTAXCLA_ID,1) as SRVTAXCLA_ID FROM SAQITM (NOLOCK) WHERE QUOTE_ID ='{quote}'".format(quote=QUOTE))
part_query = SqlHelper.GetList("SELECT PART_NUMBER, ANNUAL_QUANTITY FROM (SELECT PART_NUMBER, ANNUAL_QUANTITY,ROW_NUMBER() OVER(ORDER BY PART_NUMBER) AS SNO FROM SAQIFP (NOLOCK) WHERE QUOTE_ID = '"+str(QUOTE)+"' AND PRICING_STATUS = 'ACQUIRING...' )A WHERE SNO>="+str(start)+" AND SNO<="+str(end)+"  ")
if part_query:

    while L == 1:
        #Log.Info("Looping Count ==> "+str(n))
        itemid = ''
        part_query = SqlHelper.GetList("SELECT PART_NUMBER, ANNUAL_QUANTITY FROM (SELECT PART_NUMBER, ANNUAL_QUANTITY,ROW_NUMBER() OVER(ORDER BY PART_NUMBER) AS SNO FROM SAQIFP (NOLOCK) WHERE QUOTE_ID = '"+str(QUOTE)+"' AND PRICING_STATUS = 'ACQUIRING...' )A WHERE SNO>="+str(start)+" AND SNO<="+str(end)+"  ")
        partids = quantity = li = []
        s = ""
        if part_query:      
            partids = [p.PART_NUMBER for p in part_query]
            quantity = [float(q.ANNUAL_QUANTITY) for q in part_query]  
            start = start + 1000
            end = end + 1000
            
            if len(partids) == 1:
                itemid = str(partids[0])+";"+str(QUOTE)+";"+str(quantity[0])
                item_string = '{"itemId":"'+str(itemid)+'","externalId":null,"quantity":{"value":'+str(quantity[0])+',"unit":"EA"},"exchRateType":"'+str(exch)+'","exchRateDate":"'+str(y[0])+'","productDetails":{"productId":"'+str(partids[0])+'","baseUnit":"EA","alternateProductUnits":null},"attributes":[{"name":"KOMK-LAND1","values":["CN"]},{"name":"KOMK-ALAND","values":["CN"]},{"name":"KOMK-REGIO","values":["TX"]},{"name":"KOMK-KUNNR","values":["'+stp_account_id+'"]},{"name":"KOMK-KUNWE","values":["'+stp_account_id+'"]},{"name":"KOMP-TAXM1","values":["'+str(Taxm1Qurey.SRVTAXCLA_ID)+'"]},{"name":"KOMK-TAXK1","values":["'+str(taxk1)+'"]},{"name":"KOMK-SPART","values":["'+str(div)+'"]},{"name":"KOMP-SPART","values":["'+str(div)+'"]},{"name":"KOMP-PMATN","values":["'+str(partids[0])+'"]},{"name":"KOMK-WAERK","values":["'+str(curr)+'"]},{"name":"KOMK-HWAER","values":["'+str(curr)+'"]},{"name":"KOMP-PRSFD","values":["X"]},{"name":"KOMK-VTWEG","values":["'+str(dis)+'"]},{"name":"KOMK-VKORG","values":["'+str(salesorg)+'"]},{"name":"KOMP-KPOSN","values":["0"]},{"name":"KOMP-KZNEP","values":[""]},{"name":"KOMP-ZZEXE","values":["true"]}],"accessDateList":[{"name":"KOMK-PRSDT","value":"'+str(y[0])+'"},{"name":"KOMK-FBUDA","value":"'+str(y[0])+'"}],"variantConditions":[],"statistical":true,"subItems":[]}'

                requestdata = '<?xml version=\"1.0\" encoding=\"UTF-8\"?><soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\">  <soapenv:Body> <cpq_columns><root> {"docCurrency":"'+curr+'","locCurrency":"'+curr+'","pricingProcedure":"'+PricingProcedure+'","groupCondition":false,"itemConditionsRequired":true,"items": ['+str(item_string)+']} </root> <CPSToken>'+str(response['access_token'])+'</CPSToken></cpq_columns> </soapenv:Body></soapenv:Envelope>'
            else:
                for p,q in zip(partids,quantity):
                    itemid = str(p)+";"+str(QUOTE)+";"+str(q)
                    item_string = '{"itemId":"'+str(itemid)+'","externalId":null,"quantity":{"value":'+str(q)+',"unit":"EA"},"exchRateType":"'+str(exch)+'","exchRateDate":"'+str(y[0])+'","productDetails":{"productId":"'+str(p)+'","baseUnit":"EA","alternateProductUnits":null},"attributes":[{"name":"KOMK-LAND1","values":["CN"]},{"name":"KOMK-ALAND","values":["CN"]},{"name":"KOMK-REGIO","values":["TX"]},{"name":"KOMK-KUNNR","values":["'+stp_account_id+'"]},{"name":"KOMK-KUNWE","values":["'+stp_account_id+'"]},{"name":"KOMP-TAXM1","values":["'+str(Taxm1Qurey.SRVTAXCLA_ID)+'"]},{"name":"KOMK-TAXK1","values":["'+str(taxk1)+'"]},{"name":"KOMK-SPART","values":["'+str(div)+'"]},{"name":"KOMP-SPART","values":["'+str(div)+'"]},{"name":"KOMP-PMATN","values":["'+str(p)+'"]},{"name":"KOMK-WAERK","values":["'+str(curr)+'"]},{"name":"KOMK-HWAER","values":["'+str(curr)+'"]},{"name":"KOMP-PRSFD","values":["X"]},{"name":"KOMK-VTWEG","values":["'+str(dis)+'"]},{"name":"KOMK-VKORG","values":["'+str(salesorg)+'"]},{"name":"KOMP-KPOSN","values":["0"]},{"name":"KOMP-KZNEP","values":[""]},{"name":"KOMP-ZZEXE","values":["true"]}],"accessDateList":[{"name":"KOMK-PRSDT","value":"'+str(y[0])+'"},{"name":"KOMK-FBUDA","value":"'+str(y[0])+'"}],"variantConditions":[],"statistical":true,"subItems":[]}'
                    li.append(item_string)
                s = ','.join(li)
                
                start_time = time.time()
                requestdata = '<?xml version=\"1.0\" encoding=\"UTF-8\"?><soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\">  <soapenv:Body> <cpq_columns><root>  {"docCurrency":"'+curr+'","locCurrency":"'+curr+'","pricingProcedure":"'+PricingProcedure+'","groupCondition":false,"itemConditionsRequired":true,"items": ['+str(s)+']} </root> <CPSToken>'+str(response['access_token'])+'</CPSToken></cpq_columns> </soapenv:Body></soapenv:Envelope>'

            #Log.Info("requestdata==>"+str(requestdata))
            #response1 = webclient.UploadString(Request_URL,str(requestdata))
            
            LOGIN_CREDENTIALS = SqlHelper.GetFirst("SELECT USER_NAME as Username,Password,Domain FROM SYCONF where Domain='AMAT_TST'")
            Login_Username = str(LOGIN_CREDENTIALS.Username)
            Login_Password = str(LOGIN_CREDENTIALS.Password)
            authorization = Login_Username + ":" + Login_Password
            binaryAuthorization = UTF8.GetBytes(authorization)
            authorization = Convert.ToBase64String(binaryAuthorization)
            authorization = "Basic " + authorization
            webclient = System.Net.WebClient()
            webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/json"
            webclient.Headers[System.Net.HttpRequestHeader.Authorization] = authorization
            #Log.Info("Looping Count ==> ")
            
            response1 = webclient.UploadString("https://e250404-iflmap.hcisbt.us3.hana.ondemand.com/cxf/CPQ_CPS",str(requestdata))
            end_time = time.time()
            #Log.Info("QUOTE ID---> "+str(QUOTE)+"loop---"+str(loop_count)+ "---time"+str(end_time - start_time))
        else:
            L=0
else:
    Log.Info('150----to call pricing here---quote table insert----')
    price = []
    QUOTE = ''

    for root, value in response1.items():
        for root1 in value:
            for inv in root1:			
                if inv == "items":
                    #Log.Info("6666 i[u] --->"+str(list(root1[inv])))
                    price = root1[inv]			 
                    break
    if str(type(price)) == "<type 'Dictionary[str, object]'>":
        Log.Info("type condition--->")
        price = [price]
        Log.Info("456789 type(price) --->"+str(type(price)))
        for i in price:		
            Itemidinfo = str(i["itemId"]).split(";")
            Log.Info("456 Itemidinfo --->"+str(Itemidinfo))
            QUOTE = str(Itemidinfo[1])	
            contract_quote_record_id = None		
            
            getservicerecord = Sql.GetFirst("select QUOTE_NAME,SERVICE_DESCRIPTION,SERVICE_ID,	SERVICE_RECORD_ID from SAQTSE (NOLOCK) where QUOTE_ID = '{}'".format(QUOTE))
            QuoteItemList = Quote.QuoteTables["SAQICD"]
            if str(type(i['conditions'])) == "<type 'ArrayList'>":
                for cond_info in i['conditions']:
                    Log.Info("333 cond_info['conditionType'] --->")
                    getuomrec = Sql.GetFirst("select UOM_RECORD_ID from MAMTRL where UNIT_OF_MEASURE = '"+str(cond_info['conditionUnit'])+"'")
                    newRow = QuoteItemList.AddNewRow()
                    newRow['CONDITION_COUNTER'] = cond_info['conditionCounter']
                    newRow['CONDITION_DATA_TYPE'] =  cond_info['conditionType']
                    newRow['CONDITION_RATE'] = cond_info['conditionRate'].strip()
                    newRow['CONDITION_TYPE'] = cond_info['conditionType']
                    newRow['CONDITIONTYPE_NAME'] = cond_info['conditionTypeDescription'].strip()
                    newRow['UOM'] =  cond_info['conditionUnit']
                    newRow['CONDITIONTYPE_RECORD_ID'] = ''
                    newRow['CONDITION_VALUE'] = cond_info['conditionValue']
                    newRow['UOM_RECORD_ID'] = getuomrec.UOM_RECORD_ID
                    newRow['LINE'] = ''
                    newRow['QTEITM_RECORD_ID'] = ''
                    newRow['QUOTE_NAME'] = getservicerecord.QUOTE_NAME
                    newRow['SERVICE_DESCRIPTION'] = getservicerecord.SERVICE_DESCRIPTION
                    newRow['SERVICE_ID'] = getservicerecord.SERVICE_ID
                    newRow['STEP_NUMBER'] = cond_info['stepNo']
                    newRow['SERVICE_RECORD_ID'] = getservicerecord.SERVICE_RECORD_ID
                    newRow['QUOTE_RECORD_ID'] = contract_quote_record_id
                    newRow['QUOTE_ID'] = QUOTE
                QuoteItemList.Save()		                
today = datetime.datetime.now()
Modi_date = today.strftime("%m/%d/%Y %H:%M:%S %p")

#Log.Info("CQPRTPRCUP  end time ---->"+str(Modi_date))

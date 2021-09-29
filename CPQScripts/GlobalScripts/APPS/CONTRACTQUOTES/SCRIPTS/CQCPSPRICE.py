#===================================================================================================================#======================
#   __script_name : CQCPSPRICE.PY
#   __script_description : THIS SCRIPT IS USED TO FETCH THE PRICE FROM CPS BASED ON PRODUCTS.
#   __primary_author__ : SRIJAYDHURGA
#   __create_date :08/30/2021
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# #====================================================================================================================#======================
import Webcom.Configurator.Scripting.Test.TestProduct
import clr
clr.AddReference("Webcom.Configurator")
import System.Net
import sys
import datetime

class CPSPRICECALL:
    
    def fetch_cps_price():
        webclient = System.Net.WebClient()
        webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/json"
        webclient.Headers[System.Net.HttpRequestHeader.Authorization] = "Basic c2ItYzQwYThiMWYtYzU5NS00ZWJjLTkyYzYtYzM4ODg4ODFmMTY0IWIyNTAzfGNwc2VydmljZXMtc2VjdXJlZCFiMzkxOm9zRzgvSC9hOGtkcHVHNzl1L2JVYTJ0V0FiMD0=";
        response = webclient.DownloadString("https://cpqprojdevamat.authentication.us10.hana.ondemand.com:443/oauth/token?grant_type=client_credentials")
        response = eval(response)
        Trace.Write("res"+str(response))
        Trace.Write(response['access_token'])
        Request_URL="https://cpservices-pricing.cfapps.us10.hana.ondemand.com/api/v1/statelesspricing"
        webclient.Headers[System.Net.HttpRequestHeader.Authorization] ="Bearer "+str(response['access_token'])
        QUOTE = "SQ3050000382RV00-RW00AM00-20221220"
        itemid = 1
        li =[]
        s = ""
        x = datetime.datetime.today()
        x= str(x)
        y = x.split(" ")
        PricingProcedure = 'ZZNA05'
        curr = 'USD'
        dis = '01'
        salesorg = '2044'
        div = '98'
        STPObj=SqlHelper.GetFirst("SELECT ACCOUNT_ID FROM SAOPQT (NOLOCK) WHERE QUOTE_ID ='{quote}'".format(quote=QUOTE))
        partids = ["0041-29874","0041-13197"]
        quantity = [1.0,1.0]
        for p,q in zip(partids,quantity):
            item_string = '{"itemId":"'+str(itemid)+'","externalId":null,"quantity":{"value":'+str(q)+',"unit":"EA"},"exchRateType":"M","exchRateDate":"'+str(y[0])+'","productDetails":{"productId":"'+str(p)+'","baseUnit":"EA","alternateProductUnits":null},"attributes":[{"name":"KOMK-LAND1","values":["US"]},{"name":"KOMP-KPOSN","values":["'+str(itemid)+'"]},{"name":"KOMP-ZZEXE","values":["x"]},{"name":"KOMP-PRSFD","values":["X"]},{"name":"KOMP-KZNEP","values":[""]},{"name":"KOMK-KUNNR","values":["'+str(STPObj.ACCOUNT_ID)+'"]},{"name":"KOMK-KUNWE","values":["'+str(STPObj.ACCOUNT_ID)+'"]},{"name":"KOMK-SPART","values":["'+str(div)+'"]},{"name":"KOMP-SPART","values":["'+str(div)+'"]},{"name":"KOMP-PMATN","values":["'+str(p)+'"]},{"name":"KOMK-WAERK","values":["'+str(curr)+'"]},{"name":"KOMP-PRSFD","values":["X"]},{"name":"KOMK-VTWEG","values":["'+str(dis)+'"]},{"name":"KOMK-VKORG","values":["'+str(salesorg)+'"]}],"accessDateList":[{"name":"KOMK-PRSDT","value":"'+str(y[0])+'"},{"name":"KOMK-FBUDA","value":"'+str(y[0])+'"}],"variantConditions":[],"statistical":true,"subItems":[]}'
            li.append(item_string)
            itemid += 1
            s = ','.join(li)

        requestdata = '{"docCurrency":"USD","locCurrency":null,"pricingProcedure":"'+PricingProcedure+'","groupCondition":false,"itemConditionsRequired":true,"items": ['+str(s)+']}'
        Trace.Write("requestdata"+str(requestdata))
        response = webclient.UploadString(Request_URL,str(requestdata))
        return response


    ApiResponse = ApiResponseFactory.JsonResponse(fetch_cps_price())
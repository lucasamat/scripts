# =========================================================================================================================================
#   __script_name : CQENTLNVAL.py
#   __script_description : THIS SCRIPT IS USED TO GET ENTITLEMENT VALUES.
#   __primary_author__ : 
#   __create_date :8/23/2021
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import Webcom
from datetime import datetime
import Webcom.Configurator.Scripting.Test.TestProduct
import time
from SYDATABASE import SQL
Sql = SQL()

import System.Net
import sys


Trace.Write('script called')
def Request_access_token():
        webclient = System.Net.WebClient()
        webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/json"
        webclient.Headers[
            System.Net.HttpRequestHeader.Authorization
        ] = "Basic c2ItYzQwYThiMWYtYzU5NS00ZWJjLTkyYzYtYzM4ODg4ODFmMTY0IWIyNTAzfGNwc2VydmljZXMtc2VjdXJlZCFiMzkxOm9zRzgvSC9hOGtkcHVHNzl1L2JVYTJ0V0FiMD0="
        response = webclient.DownloadString(
            "https://cpqprojdevamat.authentication.us10.hana.ondemand.com:443/oauth/token?grant_type=client_credentials"
        )
        return eval(response)


def entitlement_request(partnumber,cpsConfigID):
    #gettodaydate = datetime.now().strftime("%Y-%m-%d")
    partnumber = partnumber.strip()
    webclient = System.Net.WebClient()
    response = Request_access_token()
    #response = eval(response)
    Trace.Write(response["access_token"])
    try:		
        Trace.Write("CHKNGTRAZ_J "+str(webclient.Headers[System.Net.HttpRequestHeader.Authorization]))
        request_url = "https://cpservices-product-configuration.cfapps.us10.hana.ondemand.com/api/v2/configurations/"+str(cpsConfigID)
        webclient.Headers[System.Net.HttpRequestHeader.Authorization] = "Bearer " + str(response["access_token"])			
        response1 = webclient.DownloadString(request_url)
    except Exception as e:
        Trace.Write('1897-----'+str(e))
        response1 = {}
            
            
    response1 = str(response1).replace(": true", ': "true"').replace(": false", ': "false"')
    Trace.Write("response1_J "+str(response1))
    return eval(response1)


def get_entitlement_response(partnumber,where_cond,ent_level_table):
    get_cps = Sql.GetFirst("SELECT * FROM {} {}".format(ent_level_table,where_cond) )
    fullresponse = entitlement_request(partnumber,get_cps.CPS_CONFIGURATION_ID)
    if fullresponse:
        status = fullresponse['complete']
        Trace.Write('status--'+str(status))
        return status

try:
    action= Param.action
except:
    action = ""
try:
    partnumber= Param.partnumber
except:
    partnumber = ""
try:
    where_cond= Param.where_cond
except:
    where_cond = ""
try:
    ent_level_table= Param.ent_level_table
except:
    ent_level_table = ""

if action == 'GET_STATUS':
    get_entitlement_response(partnumber,where_cond,ent_level_table)
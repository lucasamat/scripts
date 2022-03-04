# =========================================================================================================================================
#   __script_name : CQPARTIFLW.PY
#   __script_description : THIS SCRIPT IS USED TO TRIGGER IFLOW FOR PART PRICING UPDATE TO ITEMS TABLE
#   __primary_author__ : NAMRATA SIVAKUMAR
#   __create_date :23-10-2020
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct
import clr
import System.Net
import sys
#import sys
import datetime
#import clr
#import System.Net
from System.Text.Encoding import UTF8
from System import Convert
#from SYDATABASE import SQL
from SYDATABASE import SQL

Sql = SQL()
def iflow_pricing_call(user,entries,revision):
    #Log.Info('CQPARTIFLW-CQPARTIFLW-----')
    requestdata = (
        '<?xml version="1.0" encoding="UTF-8"?><soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"><soapenv:Body><CPQ_Columns><UserName>'
        + str(user)
        + "</UserName><Entries>"
        +str(entries)
        +"</Entries><Revision>"
        +str(revision)
        +"</Revision></CPQ_Columns></soapenv:Body></soapenv:Envelope>"
    )
    #Log.Info("2222222222222222      " + str(requestdata))
    LOGIN_CREDENTIALS = SqlHelper.GetFirst("SELECT URL FROM SYCONF where External_Table_Name='SAQIFP'")
    LOGIN_QUERY = SqlHelper.GetFirst("SELECT User_name as Username,Password,Domain,URL FROM SYCONF where Domain='AMAT_TST'")
    if LOGIN_CREDENTIALS is not None:
        Login_Username = str(LOGIN_QUERY.Username)
        Login_Password = str(LOGIN_QUERY.Password)
        URL = str(LOGIN_CREDENTIALS.URL)
        authorization = Login_Username + ":" + Login_Password
        from System.Text.Encoding import UTF8

        binaryAuthorization = UTF8.GetBytes(authorization)
        from System import Convert

        authorization = Convert.ToBase64String(binaryAuthorization)
        authorization = "Basic " + authorization
    webclient = System.Net.WebClient()
    webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/xml"
    webclient.Headers[System.Net.HttpRequestHeader.Authorization] = authorization
    response = webclient.UploadString(URL, requestdata)
    Log.Info("33333333333333333    " + str(response))
    

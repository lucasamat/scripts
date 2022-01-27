# =========================================================================================================================================
#   __script_name : CQDOCIFLOW.PY
#   __script_description : THIS SCRIPT IS USED TO TRIGGER IFLOW FOR DOCUMENT GENERATION IN CONTRACT QUOTES APP
#   __primary_author__ : NAMRATA SIVAKUMAR
#   __create_date :24-11-2020
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct
import clr
import System.Net
import sys
from SYDATABASE import SQL

Sql = SQL()

def docgeneration(quote,language,quote_revision_record_id):
    requestdata = (
        '<?xml version="1.0" encoding="UTF-8"?><soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"><soapenv:Body><CPQ_Columns><Quote>'
        + str(quote)
        + "</Quote><Language>"
        +str(language)
        +"</Language><QuoteRevision>"
        + str(quote_revision_record_id)
        +"</QuoteRevision></CPQ_Columns></soapenv:Body></soapenv:Envelope>"
    )    
    LOGIN_CREDENTIALS = SqlHelper.GetFirst("SELECT URL FROM SYCONF where External_Table_Name='SAQDOC'")
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
    Trace.Write("response    " + str(response))
    

# =========================================================================================================================================
#   __script_name : CQVLDRIFLW.PY
#   __script_description : THIS SCRIPT IS USED TO TRIGGER IFLOW FOR VALUE DRIVER ROLLDOWN 
#   __primary_author__ : NAMRATA SIVAKUMAR
#   __create_date :16-11-2020
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct
import clr
import System.Net
import sys
from SYDATABASE import SQL

Sql = SQL()
def iflow_valuedriver_rolldown(quote,level,ancillary_dict=''):    
    requestdata = (
        '<?xml version="1.0" encoding="UTF-8"?><soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"><soapenv:Body><CPQ_Columns><Quote>'
        + str(quote)
        + "</Quote><Level>"
        +str(level)
        +"</Level><Ancillary_dict>"
		+str(ancillary_dict)
		+"</Ancillary_dict></CPQ_Columns></soapenv:Body></soapenv:Envelope>"
    )    
    LOGIN_CREDENTIALS = SqlHelper.GetFirst("SELECT URL FROM SYCONF where External_Table_Name='SAQTVD'")
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
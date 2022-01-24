# =========================================================================================================================================
#   __script_name : CQENTIFLOW.PY
#   __script_description : THIS SCRIPT IS USED TO TRIGGER IFLOW FOR ENTITLEMENT ROLLDOWN
#   __primary_author__ : ASHA LYSANDAR
#   __create_date :12-11-2020
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct
import clr
import System.Net
import sys
from SYDATABASE import SQL

Sql = SQL()

def iflow_entitlement(objectName,where,ancillary_dict):
    requestdata = ('<?xml version="1.0" encoding="UTF-8"?> <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"> <soapenv:Body><CPQ_Columns><objectName>'+str(objectName)+"</objectName><where>"+str(where)+"</where><ancillary_dict>"+str(ancillary_dict)+"</ancillary_dict></CPQ_Columns></soapenv:Body></soapenv:Envelope>")
    #Log.Info("2222222222222222      " + str(requestdata))
    LOGIN_CREDENTIALS = SqlHelper.GetFirst("SELECT URL FROM SYCONF where External_Table_Name='SAQTSE'")
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
    Trace.Write("33333333333333333    " + str(response))
    
# =========================================================================================================================================
#   __script_name : CQTVLDRIFW.PY
#   __script_description : THIS SCRIPT IS USED TO TRIGGER IFLOW FOR VALUE DRIVER ROLLDOWN 2
#   __primary_author__ : NAMRATA SIVAKUMAR
#   __create_date :05-01-2021
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
def iflow_valuedriver_rolldown(quote,level,TreeParam, TreeParentParam, TreeSuperParentParam, TreeTopSuperParentParam,Userid,Username,quote_revision_record_id):
    #Trace.Write("1111111111111111     " + str(username))
    requestdata = (
        '<?xml version="1.0" encoding="UTF-8"?><soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"><soapenv:Body><CPQ_Columns><Quote>'
        + str(quote)
        + "</Quote><Level>"
        +str(level)
        +"</Level><TreeParam>"
        +str(TreeParam)
        +"</TreeParam><TreeParentParam>"
        +str(TreeParentParam)
        +"</TreeParentParam><TreeSuperParentParam>"
        + str(TreeSuperParentParam)
        +"</TreeSuperParentParam><TreeTopSuperParentParam>"
        +str(TreeTopSuperParentParam)
        +"</TreeTopSuperParentParam><Userid>"
        +str(Userid)
        +"</Userid><Username>"
        +str(Username)
        +"</Username><quote_revision_record_id>"
        +str(quote_revision_record_id)
        +"</quote_revision_record_id></CPQ_Columns></soapenv:Body></soapenv:Envelope>"
    )
    Log.Info("2222222222222222      " + str(requestdata))
    LOGIN_CREDENTIALS = SqlHelper.GetFirst("SELECT URL FROM SYCONF where External_Table_Name='VALUEDRIVER'")
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
    Log.Info("testing.............")
    webclient = System.Net.WebClient()
    webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/xml"
    webclient.Headers[System.Net.HttpRequestHeader.Authorization] = authorization
    response = webclient.UploadString(URL, requestdata)
    Trace.Write("33333333333333333    " + str(response))

def valuedriver_predefined(quote,level,TreeParam, TreeParentParam, TreeSuperParentParam, TreeTopSuperParentParam,Userid,Username,quote_revision_record_id):

    #Trace.Write("1111111111111111     " + str(username))
    requestdata = (
        '<?xml version="1.0" encoding="UTF-8"?><soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"><soapenv:Body><CPQ_Columns><Quote>'
        + str(quote)
        + "</Quote><Level>"
        +str(level)
        +"</Level><TreeParam>"
        +str(TreeParam)
        +"</TreeParam><TreeParentParam>"
        +str(TreeParentParam)
        +"</TreeParentParam><TreeSuperParentParam>"
        + str(TreeSuperParentParam)
        +"</TreeSuperParentParam><TreeTopSuperParentParam>"
        +str(TreeTopSuperParentParam)
        +"</TreeTopSuperParentParam><Userid>"
        +str(Userid)
        +"</Userid><Username>"
        +str(Username)
        +"</Username><quote_revision_record_id>"
        +str(quote_revision_record_id)
        +"</quote_revision_record_id></CPQ_Columns></soapenv:Body></soapenv:Envelope>"
    )
    Log.Info("Predefined------" + str(requestdata))
    LOGIN_CREDENTIALS = SqlHelper.GetFirst("SELECT URL FROM SYCONF where External_Table_Name='VALUEDRIVER_PREDEFINED'")
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
    Log.Info("testing.............")
    webclient = System.Net.WebClient()
    webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/xml"
    webclient.Headers[System.Net.HttpRequestHeader.Authorization] = authorization
    response = webclient.UploadString(URL, requestdata)
    Trace.Write("33333333333333333--predefined--" + str(response))
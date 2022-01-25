# =========================================================================================================================================
#   __script_name : CQIFLSPARE.PY
#   __script_description : THIS SCRIPT IS USED TO TRIGGER IFLOW FOR PULL PARTS THROUGH KYMA SERVICE
#   __primary_author__ : Suriyanarayanan Pazhani
#   __create_date :19-01-2022
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct
import clr
import System.Net
import sys
import datetime
from System.Text.Encoding import UTF8
from System import Convert
from SYDATABASE import SQL

Sql = SQL()

def iflow_pullspareparts_call(user,soldto,shipto,salesorg,pricelist,pricegroup,customerparticipate,participate6kw,partnumbers,validfrom,validto,quoteid,revisionrecordid,accesstoken):
    requestdata = (
        '<?xml version="1.0" encoding="UTF-8"?><soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"><soapenv:Body><CPQ_Columns><User>'
        + str(user)
        + "</User><SoldTo>"
        + str(soldto)
        + "</SoldTo><ShipTo>"
        +str(shipto)
        +"</ShipTo><SalesOrg>"
        +str(salesorg)
        +"</SalesOrg><PriceList>"
        +str(pricelist)
        +"</PriceList><PriceGroup>"
        +str(pricegroup)
        +"</PriceGroup><CustomerParticipate>"
        +str(customerparticipate)
        +"</CustomerParticipate><Participate6kW>"
        +str(participate6kw)
        +"</Participate6kW><PartNumbers>"
        +str(partnumbers)
        +"</PartNumbers><ValidFrom>"
        +str(validfrom)
        +"</ValidFrom><ValidTo>"
        +str(validto)
        +"</ValidTo><QuoteID>"
        +str(quoteid)
        +"</QuoteID><RevisionRecordID>"
        +str(revisionrecordid)
        +"</RevisionRecordID><AccessToken>"
        +str(accesstoken)
        +"</AccessToken></CPQ_Columns></soapenv:Body></soapenv:Envelope>"
    )
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

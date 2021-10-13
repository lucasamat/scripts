# =========================================================================================================================================
#   __script_name : CQCPQC4CWB.PY
#   __script_description : THIS SCRIPT IS USED TO TRIGGER IFLOW FOR WRITE BACK DETAILS FROM CPQ TO C4C
#   __primary_author__ : GAYATHRI AMARESAN
#   __create_date :13-10-2021
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
def quote_header_writeback(writeback,quote_record_id,quote_revision_record_id):
    Log.Info("inside the CPQTOC4CWB11111111111")
    revision_obj = Sql.GetFirst("select SALESORG_ID,DOCTYP_ID,DISTRIBUTIONCHANNEL_ID,DIVISION_ID,QTEREV_ID,REVISION_DESCRIPTION,REVISION_STATUS,CONTRACT_VALID_FROM,CONTRACT_VALID_TO FROM SAQTRV WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(contract_quote_record_id,quote_revision_record_id))
    quote_obj = Sql.GetFirst("select NET_VALUE,OWNER_NAME,ACCOUNT_ID FROM SAQTMT WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(contract_quote_record_id,quote_revision_record_id))
    Log.Info("inside the CPQTOC4CWB22222222222")
    quote_header_data = {
        "ProcessingTypeCode": revision_obj.DOCTYP_ID,
        "BuyerPartyID": quote_obj.ACCOUNT_ID,
        "EmployeeResponsiblePartyID":quote_obj.OWNER_NAME,
        "SalesUnitPartyID": revision_obj.SALESORG_ID,
        "DistributionChannelCode": revision_obj.DISTRIBUTIONCHANNEL_ID,
        "DivisionCode":revision_obj.DIVISION_ID,
        "ZWB_ContractValidFrom_KUT": "2023-12-04T10:26:13.61",
        "ZWB_ContractValidTo_KUT": "2024-12-04T10:26:13.61",
        "ZWB_QuoteRevisionID_KUT": revision_obj.QTEREV_ID,
        "ZWB_RevisionDescription_KUT": revision_obj.REVISION_DESCRIPTION,
        "ZWB_RevisionStatus_KUT": "101",
        "ZWB_TotalQuoteContent_KUT": quote_obj.NET_VALUE,
        "ZWB_TotalQuotecurrencyCode_KUT" : "USD"
    }
    requestdata = (
        '<?xml version="1.0" encoding="UTF-8"?><soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"><soapenv:Body><CPQ_Columns><writeback>'
        + str(writeback)
        + "</writeback><quote_record_id>"
        +str(quote_record_id)
        +"</quote_record_id><quote_revision_record_id>"
        + str(quote_revision_record_id)
        +"</quote_revision_record_id><quote_header_data>"
        + str(quote_header_data)
        +"</quote_header_data></CPQ_Columns></soapenv:Body></soapenv:Envelope>"
    )
    LOGIN_CREDENTIALS = SqlHelper.GetFirst("SELECT URL FROM SYCONF where External_Table_Name='CPQ_TO_C4C_WRITEBACK'")
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
    

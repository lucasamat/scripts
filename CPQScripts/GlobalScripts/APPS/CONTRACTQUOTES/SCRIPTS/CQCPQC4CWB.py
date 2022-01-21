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
def writeback_to_c4c(writeback,contract_quote_record_id,quote_revision_record_id):
    if writeback == "quote_header":
        revision_obj = Sql.GetFirst("select SALESORG_ID,DOCTYP_ID,DISTRIBUTIONCHANNEL_ID,DIVISION_ID,QTEREV_ID,REVISION_DESCRIPTION,REVISION_STATUS,CONVERT(varchar, CONTRACT_VALID_FROM, 23) as CONTRACT_VALID_FROM,CONVERT(varchar, CONTRACT_VALID_TO , 23) as CONTRACT_VALID_TO FROM SAQTRV (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND ACTIVE = 1 ".format(contract_quote_record_id,quote_revision_record_id))
        ##date time conversion
        time = "T12:00:00.00"
        fromvalue = revision_obj.CONTRACT_VALID_FROM
        tovalue = revision_obj.CONTRACT_VALID_TO
        valid_from = str(fromvalue)+str(time)
        valid_to = str(tovalue)+str(time)
        ##date time conversion
        quote_obj = Sql.GetFirst("select ISNULL(NET_VALUE,0) AS NET_VALUE,OWNER_NAME,ACCOUNT_ID FROM SAQTMT (NOLOCK) WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{}'".format(contract_quote_record_id))
        
        opportunity_obj = Sql.GetFirst("select ISNULL(C4C_QTEOBJ_ID,0) AS C4C_QTEOBJ_ID FROM SAOPQT (NOLOCK) WHERE QUOTE_RECORD_ID = '{}'".format(contract_quote_record_id))
        c4c_quote_object_id = opportunity_obj.C4C_QTEOBJ_ID

        #c4c_employee_obj = Sql.GetFirst("SELECT SAEMPL.C4C_EMPLOYEE_ID FROM SAEMPL (NOLOCK) INNER JOIN SAQTMT (NOLOCK) ON SAEMPL.EMPLOYEE_ID = SAQTMT.OWNER_ID WHERE SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = '{}' AND SAQTMT.QTEREV_RECORD_ID = '{}'".format(contract_quote_record_id,quote_revision_record_id))
        c4c_employee_obj = Sql.GetFirst("SELECT SAEMPL.C4C_EMPLOYEE_ID FROM SAEMPL (NOLOCK) INNER JOIN SAQTMT (NOLOCK) ON SAEMPL.EMPLOYEE_ID = SAQTMT.OWNER_ID WHERE SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = '{}'".format(contract_quote_record_id))
        c4c_employee_id = ""
        if c4c_employee_obj is not None:
            c4c_employee_id = c4c_employee_obj.C4C_EMPLOYEE_ID

        ###Fetch the code according to the revision status..code starts...
        revision_status_code = {"APPROVAL PENDING":"111", "RECALLED":"121", "REJECTED":"131", "APPROVED":"141","CUSTOMER ACCEPTED":"161","SUBMITTED FOR BOOKING":"181","CONTRACT BOOKED":"191","ON HOLD - COSTING":"221","CUSTOMER REJECTED":"171","PREPARING REVISION":"211","OPPORTUNITY CANCELLED":"231","OPPORTUNITY LOST":"241","PRICED":"101"}
        ##Fetch the code according to the revision status..code ends...
        ##quote header write back details starts...
        quote_header_data = '{\"BuyerPartyID\":"'+str(quote_obj.ACCOUNT_ID)+'", \"EmployeeResponsiblePartyID\":"'+str(c4c_employee_id)+'", \"SalesUnitPartyID\":"'+str(revision_obj.SALESORG_ID)+'", \"DistributionChannelCode\":"'+str(revision_obj.DISTRIBUTIONCHANNEL_ID)+'", \"DivisionCode\":"'+str(revision_obj.DIVISION_ID)+'", \"ZWB_ContractValidFrom_KUT\":"'+str(valid_from)+'", \"ZWB_ContractValidTo_KUT\":"'+str(valid_to)+'", \"ZWB_QuoteRevisionID_KUT\":"'+str(revision_obj.QTEREV_ID)+'", \"ZWB_RevisionDescription_KUT\":"'+str(revision_obj.REVISION_DESCRIPTION)+'", \"ZQuoteRevisionStatus\":"'+str(revision_status_code.get(revision_obj.REVISION_STATUS))+'", \"ZWB_TotalQuoteContent_KUT\":"'+str(quote_obj.NET_VALUE)+'", \"ZWB_TotalQuotecurrencyCode_KUT\":"USD"}'
        ##quote header write back details ends...
        
        requestdata = (
            '<?xml version="1.0" encoding="UTF-8"?><soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"><soapenv:Body><CPQ_Columns><writeback>'
            + str(writeback)
            + "</writeback><contract_quote_record_id>"
            +str(contract_quote_record_id)
            +"</contract_quote_record_id><quote_revision_record_id>"
            + str(quote_revision_record_id)
            +"</quote_revision_record_id><quote_header_data>"
            + str(quote_header_data)
            +"</quote_header_data><c4c_quote_object_id>"
            + str(c4c_quote_object_id)
            +"</c4c_quote_object_id></CPQ_Columns></soapenv:Body></soapenv:Envelope>"
        )
    elif writeback == "opportunity_header":
        ##To Fetch the values from revision table....
        revision_obj = Sql.GetFirst("select REVISION_STATUS,DOC_CURRENCY,ISNULL(NET_VALUE_INGL_CURR,0) AS NET_VALUE_INGL_CURR,CONVERT(varchar, CONTRACT_VALID_FROM, 23) as CONTRACT_VALID_FROM,CONVERT(varchar, CONTRACT_VALID_TO , 23) as CONTRACT_VALID_TO FROM SAQTRV (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND ACTIVE = 1 ".format(contract_quote_record_id,quote_revision_record_id))
        
        ##date time conversion
        time = "T12:00:00.00"    
        fromvalue = revision_obj.CONTRACT_VALID_FROM
        tovalue = revision_obj.CONTRACT_VALID_TO
        valid_from =fromvalue+time
        valid_to = tovalue+time
        ##date time conversion
        net_value = revision_obj.NET_VALUE_INGL_CURR
        opportunity_object = Sql.GetFirst("select ISNULL(SAOPPR.C4C_OPPOBJ_ID,0) AS C4C_OPPOBJ_ID FROM SAOPPR(NOLOCK) INNER JOIN SAOPQT (NOLOCK) ON  SAOPPR.OPPORTUNITY_ID = SAOPQT.OPPORTUNITY_ID AND SAOPPR.ACCOUNT_ID = SAOPQT.ACCOUNT_ID WHERE QUOTE_RECORD_ID = '{}'".format(contract_quote_record_id))
        opportunity_object_id = opportunity_object.C4C_OPPOBJ_ID
        
        ##Fetch the code according to the revision status..code starts...
        revision_status_code = {"APPROVAL PENDING":"111", "RECALLED":"121", "REJECTED":"131", "APPROVED":"141","CUSTOMER ACCEPTED":"161","SUBMITTED FOR BOOKING":"181","CONTRACT BOOKED":"191","ON HOLD - COSTING":"221","CUSTOMER REJECTED":"171","PREPARING REVISION":"211","OPPORTUNITY CANCELLED":"231","OPPORTUNITY LOST":"241","PRICED":"101"}
        ##Fetch the code according to the revision status..code ends...
        
        
        ##opportunity header write back details starts...
        opportunity_header_data = '{\"ExpectedRevenueAmount\":"'+str(net_value)+'", \"ExpectedRevenueAmountCurrencyCode\":"USD", \"ExpectedProcessingStartDate\":"'+str(valid_from)+'",\"ExpectedProcessingEndDate\":"'+str(valid_from)+'", \"ExpectedRevenueStartDate\":"'+str(valid_from)+'", \"ExpectedRevenueEndDate\":"'+str(valid_to)+'", \"ZQuoteRevisionStatus_KUT\":"'+str(revision_status_code.get(revision_obj.REVISION_STATUS))+'"}'
        ##opportunity header write back details ends...
        
        requestdata = (
            '<?xml version="1.0" encoding="UTF-8"?><soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"><soapenv:Body><CPQ_Columns><writeback>'
            + str(writeback)
            + "</writeback><contract_quote_record_id>"
            +str(contract_quote_record_id)
            +"</contract_quote_record_id><quote_revision_record_id>"
            + str(quote_revision_record_id)
            +"</quote_revision_record_id><opportunity_header_data>"
            + str(opportunity_header_data)
            +"</opportunity_header_data><opportunity_object_id>"
            + str(opportunity_object_id)
            +"</opportunity_object_id></CPQ_Columns></soapenv:Body></soapenv:Envelope>"
        )
    elif writeback == "approver_list":
        contract_quote_id = Sql.GetFirst("Select QUOTE_ID FROM SAQTMT WHERE MASTER_TABLE_QUOTE_RECORD_ID ='{}' AND QTEREV_RECORD_ID = '{}'".format(contract_quote_record_id,quote_revision_record_id))
        approver_list_id=Sql.GetList("Select REPLACE(APRCHNSTP_APPROVER_ID,'USR-','') as APRCHNSTP_APPROVER_ID  FROM ACAPTX WHERE APRTRXOBJ_ID = '{}' AND APPROVALSTATUS = 'APPROVAL REQUIRED'".format(contract_quote_id.QUOTE_ID))
        approver_list = []
        for app in approver_list_id:
            approver = app.APRCHNSTP_APPROVER_ID
            approver_list.append(approver)
        role_code_id = "71"
        requestdata = (
            '<?xml version="1.0" encoding="UTF-8"?><soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"><soapenv:Body><CPQ_Columns><writeback>'
            + str(writeback)
            + "</writeback><contract_quote_id>"
            +str(contract_quote_id.QUOTE_ID)
            +"</contract_quote_id><approver_list>"
            + str(approver_list)
            +"</approver_list><role_code_id>"
            + str(role_code_id)
            +"</role_code_id></CPQ_Columns></soapenv:Body></soapenv:Envelope>"
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
    

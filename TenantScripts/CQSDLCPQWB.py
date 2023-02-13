# =========================================================================================================================================
#   __script_name : CQSDLCPQWB.PY
#   __script_description : THIS SCRIPT IS USED TO TRIGGER IFLOW FOR WRITE BACK DETAILS FROM CPQ TO C4C. FROM CPI IFLOW, IT WILL BE TRIGGERED EVERY 4 HOURS.
#   __primary_author__ : AYYAPPAN SUBRAMANIYAN
#   __create_date :07-10-2022
# ==========================================================================================================================================
# INC08787871 - Start - A
import System.Net
from SYDATABASE import SQL
#import datetime
#import time
#from datetime import timedelta , date
Sql = SQL()
import re
Log.Info("CQSDLCPQWB ===> Called ")
revision_status_code = {"APR-APPROVAL PENDING":"111", "APR-RECALLED":"121", "APR-REJECTED":"131", "APR-APPROVED":"141","APR-SUBMITTED TO CUSTOMER":"151","OPD-CUSTOMER ACCEPTED":"161","BOK-CONTRACT CREATED":"181","OPD-PREPARING QUOTE DOCUMENTS":"185","BOK-CONTRACT BOOKED":"191","CFG-ON HOLD - COSTING":"221","OPD-CUSTOMER REJECTED":"171","CFG-CONFIGURING":"211","PRI-PRICING":"101","CFG-ACQUIRING":"261","LGL-PREPARING LEGAL SOW":"271","LGL-LEGAL SOW REJECTED":"281","LGL-LEGAL SOW ACCEPTED":"291","PRR-ON HOLD PRICING":"251","CBC-PREPARING CBC":"301","CBC-CBC COMPLETED":"305","PRR-PRICING REVIEWED":"325","PRR-RECALCULATING":"315"}
start = 1
end = 150
count = 1
quote_items_records = []
while count == 1:
    quote_items_obj = Sql.GetList("""SELECT DISTINCT NET_VALUE_INGL_CURR,SALESORG_ID,DOCTYP_ID,DISTRIBUTIONCHANNEL_ID,DIVISION_ID,QTEREV_ID,REVISION_DESCRIPTION,REVISION_STATUS,CONTRACT_VALID_FROM,CONTRACT_VALID_TO,QUOTE_RECORD_ID,QUOTE_REVISION_RECORD_ID,ACCOUNT_ID,C4C_QTEOBJ_ID,C4C_EMPLOYEE_ID,C4C_OPPOBJ_ID FROM (
                    SELECT ISNULL(SAQTRV.NET_VALUE_INGL_CURR,0) + ISNULL(SAQTRV.ESTVAL_INGL_CURR,0) AS NET_VALUE_INGL_CURR,SAQTRV.SALESORG_ID,SAQTRV.DOCTYP_ID,SAQTRV.DISTRIBUTIONCHANNEL_ID,SAQTRV.DIVISION_ID,SAQTRV.QTEREV_ID,ISNULL(SAQTRV.REVISION_DESCRIPTION,'') as REVISION_DESCRIPTION,SAQTRV.REVISION_STATUS,CONVERT(varchar, SAQTRV.CONTRACT_VALID_FROM, 23) as CONTRACT_VALID_FROM,CONVERT(varchar, SAQTRV.CONTRACT_VALID_TO , 23) as CONTRACT_VALID_TO, SAQTRV.QUOTE_RECORD_ID, SAQTRV.QUOTE_REVISION_RECORD_ID,SAQTMT.ACCOUNT_ID,ISNULL(SAOPQT.C4C_QTEOBJ_ID,0) AS C4C_QTEOBJ_ID,SAEMPL.C4C_EMPLOYEE_ID,ISNULL(SAOPPR.C4C_OPPOBJ_ID,0) AS C4C_OPPOBJ_ID,ROW_NUMBER() OVER(ORDER BY SAQTMT.QUOTE_ID DESC) AS SNO 
                    FROM SAQTMT (NOLOCK) 
                    JOIN SAQTRV (NOLOCK) ON SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SAQTRV.QUOTE_REVISION_RECORD_ID = SAQTMT.QTEREV_RECORD_ID
                    JOIN SAOPQT (NOLOCK) ON SAOPQT.QUOTE_RECORD_ID = SAQTRV.QUOTE_RECORD_ID
                    LEFT JOIN SAEMPL (NOLOCK) ON SAEMPL.EMPLOYEE_ID = SAQTMT.OWNER_ID
                    LEFT JOIN SAOPPR (NOLOCK) ON SAOPPR.OPPORTUNITY_ID = SAOPQT.OPPORTUNITY_ID AND SAOPPR.ACCOUNT_ID = SAOPQT.ACCOUNT_ID
                )A 
    WHERE SNO>={Start} AND SNO<={End}""".format(Start=start,End=end))
   
    if quote_items_obj:
        quote_header_list = []
        opportunity_header_list = []
        quote_requestdata = '<?xml version="1.0" encoding="UTF-8"?><soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"><soapenv:Body><Root>'
        opportunity_requestdata = '<?xml version="1.0" encoding="UTF-8"?><soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"><soapenv:Body><Root>'
        for quote_item_obj in quote_items_obj:
            time = "T12:00:00.00"
            fromvalue = quote_item_obj.CONTRACT_VALID_FROM
            tovalue = quote_item_obj.CONTRACT_VALID_TO
            valid_from = str(fromvalue)+str(time)
            valid_to = str(tovalue)+str(time)	
            revision_desc = quote_item_obj.REVISION_DESCRIPTION
            revision_desc = re.sub(r"[^a-zA-Z0-9 \n\.><&_-~',?]", '', revision_desc)
            revision_desc = revision_desc.replace('&','&amp;').replace('<','&gt;').replace('>','&lt;').replace('＋','+')
            if quote_item_obj.NET_VALUE_INGL_CURR <= 0: # INC08787871 - End - M                
                quote_header_data = '{\"BuyerPartyID\":"'+str(quote_item_obj.ACCOUNT_ID)+'", \"EmployeeResponsiblePartyID\":"'+str(quote_item_obj.C4C_EMPLOYEE_ID)+'", \"SalesUnitPartyID\":"'+str(quote_item_obj.SALESORG_ID)+'", \"DistributionChannelCode\":"'+str(quote_item_obj.DISTRIBUTIONCHANNEL_ID)+'", \"DivisionCode\":"'+str(quote_item_obj.DIVISION_ID)+'", \"ZWB_ContractValidFrom_KUT\":"'+str(valid_from)+'", \"ZWB_ContractValidTo_KUT\":"'+str(valid_to)+'", \"ZWB_QuoteRevisionID_KUT\":"'+str(quote_item_obj.QTEREV_ID)+'", \"ZWB_RevisionDescription_KUT\":"'+revision_desc+'", \"ZQuoteRevisionStatus\":"'+str(revision_status_code.get(quote_item_obj.REVISION_STATUS))+'", \"ZWB_TotalQuotecurrencyCode_KUT\":"USD"}'
            else:       
                quote_header_data = '{\"BuyerPartyID\":"'+str(quote_item_obj.ACCOUNT_ID)+'", \"EmployeeResponsiblePartyID\":"'+str(quote_item_obj.C4C_EMPLOYEE_ID)+'", \"SalesUnitPartyID\":"'+str(quote_item_obj.SALESORG_ID)+'", \"DistributionChannelCode\":"'+str(quote_item_obj.DISTRIBUTIONCHANNEL_ID)+'", \"DivisionCode\":"'+str(quote_item_obj.DIVISION_ID)+'", \"ZWB_ContractValidFrom_KUT\":"'+str(valid_from)+'", \"ZWB_ContractValidTo_KUT\":"'+str(valid_to)+'", \"ZWB_QuoteRevisionID_KUT\":"'+str(quote_item_obj.QTEREV_ID)+'", \"ZWB_RevisionDescription_KUT\":"'+revision_desc+'", \"ZQuoteRevisionStatus\":"'+str(revision_status_code.get(quote_item_obj.REVISION_STATUS))+'", \"ZWB_TotalQuoteContent_KUT\":"'+str(quote_item_obj.NET_VALUE_INGL_CURR)+'", \"ZWB_TotalQuotecurrencyCode_KUT\":"USD"}'
            quote_requestdata += (
                '<CPQ_Columns><writeback>'
                + str('quote_header')
                + "</writeback><contract_quote_record_id>"
                +str(quote_item_obj.QUOTE_RECORD_ID)
                +"</contract_quote_record_id><quote_revision_record_id>"
                + str(quote_item_obj.QUOTE_REVISION_RECORD_ID)
                +"</quote_revision_record_id><quote_header_data>"
                + str(quote_header_data)
                +"</quote_header_data><c4c_quote_object_id>"
                + str(quote_item_obj.C4C_QTEOBJ_ID)
                +"</c4c_quote_object_id></CPQ_Columns>"
            )
            #quote_header_list.append(quote_requestdata)
            opportunity_header_data = '{\"ExpectedRevenueAmountCurrencyCode\":"USD",\"ZQuoteRevisionStatus_KUT\":"'+str(revision_status_code.get(quote_item_obj.REVISION_STATUS))+'"}'
            opportunity_requestdata += (
                '<CPQ_Columns><writeback>'
                + str('opportunity_header')
                + "</writeback><contract_quote_record_id>"
                +str(quote_item_obj.QUOTE_RECORD_ID)
                +"</contract_quote_record_id><quote_revision_record_id>"
                + str(quote_item_obj.QUOTE_REVISION_RECORD_ID)
                +"</quote_revision_record_id><opportunity_header_data>"
                + str(opportunity_header_data)
                +"</opportunity_header_data><opportunity_object_id>"
                + str(quote_item_obj.C4C_OPPOBJ_ID)
                +"</opportunity_object_id></CPQ_Columns>"
            )
            #opportunity_header_list.append(opportunity_requestdata)
        quote_requestdata += "</Root></soapenv:Body></soapenv:Envelope>"
        opportunity_requestdata += "</Root></soapenv:Body></soapenv:Envelope>"
        LOGIN_CREDENTIALS = SqlHelper.GetFirst("SELECT URL FROM SYCONF where External_Table_Name='CPQ_TO_C4C_WRITEBACK_SCHEDULE'")
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
            Log.Info("CQSDLCPQWB ===> 1111111111 "+str(quote_requestdata))
            Log.Info("CQSDLCPQWB ===> 2222222222 "+str(opportunity_requestdata))
            if quote_requestdata and opportunity_requestdata:
                Log.Info("CQSDLCPQWB ===> 33333333333 ")
                # '~'.join([quote_header for quote_header in quote_header_list])
                response = webclient.UploadString(URL, str(quote_requestdata))
                response = webclient.UploadString(URL, str(opportunity_requestdata))
        #datetime_string = datetime.datetime.now().strftime
        patch_query_quote ="""INSERT INTO SYINPL(INTEGRATION_ID,INTEGRATION_NAME,INTEGRATION_PAYLOAD,STATUS) VALUES (1,'quote_data_header','{quote_requestdata}','Completed')""".format(quote_requestdata = quote_requestdata)
        Sql.RunQuery(patch_query_quote)
        patch_query_opp ="""INSERT INTO SYINPL(INTEGRATION_ID,INTEGRATION_NAME,INTEGRATION_PAYLOAD,STATUS) VALUES (2,'opp_data_header','{opportunity_requestdata}','Completed')""".format(opportunity_requestdata = opportunity_requestdata)
        Sql.RunQuery(patch_query_opp)
        start = start + 150
        end = end + 150
    else:
        count = 0
# INC08787871 - End - A
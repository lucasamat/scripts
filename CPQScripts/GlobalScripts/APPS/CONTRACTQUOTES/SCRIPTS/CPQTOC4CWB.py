# ====================================================================================================================
#   __script_name : CPQTOC4CWB.PY
#   __script_description : THIS SCRIPT IS USED TO SENDING THE QUOTE AND OPPORTUNITY DETAILS TO C4C(CPQ TO C4C WRITEBACK)
#   __primary_author__ : GAYATHRI AMARESAN/WASIM ABDUL
#   __create_date :
#   Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ====================================================================================================================

import clr
import System.Net
from System.Text.Encoding import UTF8
from System import Convert
import sys
from SYDATABASE import SQL
Sql = SQL()


def quote_header_details():
    revision_obj = SqlHelper.GetFirst("select SALESORG_ID,DOCTYP_ID,DISTRIBUTIONCHANNEL_ID,DIVISION_ID,QTEREV_ID,REVISION_DESCRIPTION,REVISION_STATUS,CONTRACT_VALID_FROM,CONTRACT_VALID_TO FROM SAQTRV WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(Quote.GetGlobal("contract_quote_record_id"),Quote.GetGlobal("quote_revision_record_id")))
    quote_obj = SqlHelper.GetFirst("select NET_VALUE,OWNER_NAME,ACCOUNT_ID FROM SAQTMT WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(Quote.GetGlobal("contract_quote_record_id"),Quote.GetGlobal("quote_revision_record_id")))
    
quote_header_data = {
    "ProcessingTypeCode": revision_obj.DOCTYP_ID,
    "BuyerPartyID": quote_obj.ACCOUNT_ID,
    "EmployeeResponsiblePartyID":quote_obj.OWNER_NAME,
    "SalesUnitPartyID": revision_obj.SALESORG_ID,
    "DistributionChannelCode": revision_obj.DISTRIBUTIONCHANNEL_ID,
    "DivisionCode":revision_obj.DIVISION_ID,
    "ZWB_ContractValidFrom_KUT": revision_obj.CONTRACT_VALID_FROM,
    "ZWB_ContractValidTo_KUT": revision_obj.CONTRACT_VALID_TO,
    "ZWB_QuoteRevisionID_KUT": revision_obj.QTEREV_ID,
    "ZWB_RevisionDescription_KUT": revision_obj.REVISION_DESCRIPTION,
    "ZWB_RevisionStatus_KUT": "101",
    "ZWB_TotalQuoteContent_KUT": quote_obj.NET_VALUE,
    "ZWB_TotalQuotecurrencyCode_KUT" : "USD"
}
quote_header_details()





# =========================================================================================================================================
#   __script_name : CQSTATUSBR.PY
#   __script_description : THIS SCRIPT IS USED TO UPDATE THEDYNAMIC STATUS BAR.
#   __primary_author__ : KRISHNA CHAITANYA
#   __create_date : 18/11/2021
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import re
import Webcom.Configurator.Scripting.Test.TestProduct
import SYTABACTIN as Table
import SYCNGEGUID as CPQID
from SYDATABASE import SQL
Sql = SQL()
TestProduct = Webcom.Configurator.Scripting.Test.TestProduct() or "Sales"
try:
    contract_quote_record_id = Quote.QuoteId
except:
    contract_quote_record_id = ''

try:
    quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
except:
    quote_revision_record_id = ""

try:
    current_prod = Product.Name
    
except:
    current_prod = "Sales"
try:
    TabName = TestProduct.CurrentTab
except:
    TabName = "Quotes"


def Dynamic_Status_Bar():
    if (str(TabName) == "Quotes" or str(TabName) == "Quote") and current_prod == "Sales":
        #Trace.Write('sales11=======')
        getsalesorg_ifo = Sql.GetFirst("SELECT SALESORG_ID from SAQTRV where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id))
        getfab_info = Sql.GetFirst("SELECT FABLOCATION_NAME from SAQSFB where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id))
        get_service_ifo = Sql.GetFirst("SELECT COUNT(DISTINCT SERVICE_ID) as SERVICE_ID from SAQTSV where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id))
        get_equip_details = Sql.GetFirst("SELECT COUNT(DISTINCT SERVICE_ID) as SERVICE_ID from SAQSCO where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id))

        quote_ser_level_entitlement_obj = Sql.GetList(" SELECT CONFIGURATION_STATUS,SERVICE_ID FROM SAQTSE WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' ".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id))

        complete_status = incomplete_status = ""

        for configure in quote_ser_level_entitlement_obj:
            status = configure.CONFIGURATION_STATUS
            if status == "COMPLETE" and status != "":
                complete_status = 'YES'
            else:
                incomplete_status = 'YES'
        
        price_preview_status = []
        item_covered_obj = Sql.GetList("SELECT DISTINCT STATUS FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id))
        if item_covered_obj:
            for status in item_covered_obj:
                price_preview_status.append(status.STATUS)
            Trace.Write("price_preview_status_CHK"+str(price_preview_status))
            if len(price_preview_status) > 1:
                price_bar = "acquired_status"
            elif 'ACQUIRED' in price_preview_status:
                price_bar = "not_acquired_status"
            else:
                price_bar = "acquired_status"
        else:
            Trace.Write("NO Quote Items")
            price_bar = "no_quote_items"
                            
        if getsalesorg_ifo and getfab_info:
            Trace.Write('salesorg--present---')
            if get_service_ifo.SERVICE_ID == get_equip_details.SERVICE_ID and complete_status == 'YES':                
                Trace.Write('No button-2454-')
                buttonvisibility = "show_button"            
            else:
                Trace.Write('No button--1')
                buttonvisibility = "Hide_button"
        else:
            Trace.Write('No button--2')
            buttonvisibility = "Hide_button"
    Trace.Write("buttonvisibility=="+str(buttonvisibility))        

    return buttonvisibility,price_bar

ApiResponse = ApiResponseFactory.JsonResponse(Dynamic_Status_Bar())  
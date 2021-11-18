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

# Trace.Write('contract_quote_record_id==='+str(Quote.GetGlobal("contract_quote_record_id")))
try:
    current_prod = Product.Name
    #Trace.Write('current_prod==GLOBAL---='+str(Quote.GetGlobal("contract_quote_record_id")))
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

        # item_covered_obj = Sql.GetFirst("SELECT COUNT(STATUS) AS STATUS FROM SAQICO WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND STATUS NOT IN ('ACQUIRED')".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id))
        #for status in item_covered_obj:
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
        # if item_covered_obj.STATUS > 0:
        #     price_bar = "acquired_status"
        #     Trace.Write("config status==="+str(price_bar))
        # else:
        #     price_bar = "not_acquired_status"
        #     Trace.Write("config status111==="+str(price_bar))                    
        if getsalesorg_ifo and getfab_info:
            Trace.Write('salesorg--present---')
            if get_service_ifo.SERVICE_ID == get_equip_details.SERVICE_ID:
                # get_quote_details = Sql.GetFirst("SELECT  SERVICE_ID from SAQITM where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' ".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id))
                # if get_quote_details:
                #     get_quote = Quote.GetGlobal("contract_quote_record_id")
                #     Trace.Write('button process--')
                #     buttonvisibility = "Show_button"   
                # else:
                Trace.Write('No button-2454-')
                buttonvisibility = "Hide_button"
            # elif TreeParam == "Approvals" and CurrentTabName == 'Quotes':
            # 	Trace.Write("SUBMIT FOR APP Button")
            # 	sec_rel_sub_bnr = add_button
            else:
                Trace.Write('No button--1')
                buttonvisibility = "Hide_button"
        else:
            Trace.Write('No button--2')
            buttonvisibility = "Hide_button"

    return buttonvisibility,price_bar

ApiResponse = ApiResponseFactory.JsonResponse(Dynamic_Status_Bar())  
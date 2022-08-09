# =========================================================================================================================================
#   __script_name : CQCNTCTEDT.PY
#   __script_description : THIS SCRIPT IS USED LOAD THE CONTRACT Information
#   __primary_author__ :
#   __create_date : 10/08/2021
#   Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct
Trace = Trace
Param = Param
Log = Log
ApiResponseFactory = ApiResponseFactory

response = ''
try:
    quote_recotd_id = Quote.GetGlobal("contract_record_id")
    response = 'Quote Loaded'
except Exception:
    response = 'Quote Not Loaded'

ApiResponse = ApiResponseFactory.JsonResponse(response)
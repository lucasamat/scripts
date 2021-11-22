# =========================================================================================================================================
#   __script_name : CQQTMODULE.PY
#   __script_description :  THIS SCRIPT IS USED TO GET THE DATA RELATED TO THE CURRENT QUOTE
#   __primary_author__ : 
#   __create_date :
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================

entitlement_service_dictonary = {}
class QuoteModule:

    def __init__(self):
        pass

    def service_level_entitlement(self,service_id,entitlement_value):
        global entitlement_service_dictonary
        entitlement_service_dictonary = {'Z0091': 0, 'Z0092': 0 ,'Z0004': 0,'Z0006': 0,'Z0007': 0, }
        entitlement_service_dictonary[service_id] = entitlement_value
        Trace.Write("r2"+str(entitlement_service_dictonary))

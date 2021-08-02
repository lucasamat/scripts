# =========================================================================================================================================
#   __script_name : CQCUSTFLDS.PY
#   __script_description : THIS SCRIPT IS USED TO ASSIGNT THE CUSTOM FIELD VALUE TO THE CORRESPONDING CUSTOMG FIELDS.
#   __primary_author__ :GAYATHRI AMARESAN
#   __create_date :
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================

def custfieldsupdated(saleprice):
	Quote.GetCustomField('SALE_PRICE').Content = str(saleprice)
    return saleprice


try:
	customfield = Param.customfield
except Exception:
	customfield = ""
try:
	saleprice = Param.saleprice
except Exception:
	saleprice = ""

if customfield == "Yes":
	ApiResponse = ApiResponseFactory.JsonResponse(custfieldsupdated(saleprice))
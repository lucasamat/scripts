# =========================================================================================================================================
#   __script_name : CQCUSTFLDS.PY
#   __script_description : THIS SCRIPT IS USED TO ASSIGNT THE CUSTOM FIELD VALUE TO THE CORRESPONDING CUSTOMG FIELDS.
#   __primary_author__ :GAYATHRI AMARESAN
#   __create_date :
#   Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
from SYDATABASE import SQL
Sql = SQL()
def custfieldsupdated(saleprice,service_id):
    Trace.Write("saleprice"+str(saleprice))
    quoteitem_covered_obj = SqlHelper.GetFirst("select count(CpqTableEntryId) as cnt from SAQICO where SERVICE_ID = '{service_id}'and QUOTE_RECORD_ID = '{quote_record_id}'".format(service_id = service_id,quote_record_id = Quote.GetGlobal("contract_quote_record_id")))
    count = quoteitem_covered_obj.cnt
    Trace.Write("count of SAQICO "+str(count))
    covered_obj_sale_price = int(saleprice)/count
    Trace.Write("covered_obj_sale_price "+str(covered_obj_sale_price))
    update_sales_price = "UPDATE SAQICO SET SALES_PRICE = {covered_obj_sale_price} WHERE SAQICO.SERVICE_ID = '{service_id}' and QUOTE_RECORD_ID = '{QuoteRecordId}' ".format(
    covered_obj_sale_price=covered_obj_sale_price,			
    service_id=service_id,
    QuoteRecordId=Quote.GetGlobal("contract_quote_record_id"),
    )
    Sql.RunQuery(update_sales_price)
    update_quote_item_obj = "UPDATE SAQITM SET SALES_PRICE = {saleprice} WHERE SAQICO.SERVICE_ID = '{service_id}' and QUOTE_RECORD_ID = '{QuoteRecordId}' ".format(
    saleprice=saleprice,			
    service_id=service_id,
    QuoteRecordId=Quote.GetGlobal("contract_quote_record_id"),
    )
    Sql.RunQuery(update_quote_item_obj)
    Quote.GetCustomField('SALE_PRICE').Content = saleprice
    return saleprice
def salepriceedit(service_id):
    editable = "false"
    editablity_obj = SqlHelper.GetFirst("select SERVICE_TYPE from MAMTRL where SAP_PART_NUMBER like '%"+str(service_id)+"'")
    if editablity_obj is not None:
        servicetype = editablity_obj.SERVICE_TYPE
        if servicetype == "NON TOOL BASED":
            editable = "true"
            return service_id,editable

try:
    customfield = Param.customfield
except Exception:
    customfield = ""
try:
    saleprice = Param.saleprice
    Trace.Write("try sale"+str(saleprice))
except Exception,e:
    saleprice = ""
    Trace.Write("342"+str(e))
try:
    service_id = Param.service_id
except Exception:
    service_id = ""  

if customfield == "Yes":
    ApiResponse = ApiResponseFactory.JsonResponse(custfieldsupdated(saleprice,service_id))
elif service_id != "":
    ApiResponse = ApiResponseFactory.JsonResponse(salepriceedit(service_id))
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
    a = Sql.GetFirst("SELECT ISNULL(SALES_DISCOUNT_PRICE,0) AS  SALES_DISCOUNT_PRICE, SERVICE_ID,QUOTE_RECORD_ID,GREENBOOK,YEAR_OVER_YEAR,CONTRACT_VALID_FROM,CONTRACT_VALID_TO  FROM SAQICO (NOLOCK) WHERE SERVICE_ID = '{service_id}' and QUOTE_RECORD_ID = '{QuoteRecordId}'".format(service_id=service_id ,QuoteRecordId=Quote.GetGlobal("contract_quote_record_id")))
                
    if float(a.SALES_DISCOUNT_PRICE) != 0.0 or float(a.SALES_DISCOUNT_PRICE) != 0.00:
        discount =(float(saleprice)/float(a.SALES_DISCOUNT_PRICE))*100.00
    else:
        discount = 0.00

    getdates = Sql.GetFirst("SELECT CONTRACT_VALID_FROM,CONTRACT_VALID_TO FROM SAQTMT WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{}'".format(a.QUOTE_RECORD_ID))


    import datetime as dt
    fmt = '%m/%d/%Y'
    d1 = dt.datetime.strptime(str(getdates.CONTRACT_VALID_FROM).split(" ")[0], fmt)
    d2 = dt.datetime.strptime(str(getdates.CONTRACT_VALID_TO).split(" ")[0], fmt)
    days = (d2 - d1).days
    Trace.Write("number of days---------------->"+str((d2 - d1).days))


    yoy = float(a.YEAR_OVER_YEAR)

    year1 = float(saleprice)
    year2 = 0.00
    year3 = 0.00
    year4 = 0.00
    year5 = 0.00
    dec1 = (float(saleprice)*yoy)/100

    if days > 365:
        year2 = float(saleprice) - dec1
        dec2 = (float(saleprice)*dec1)/100
    if days > 730:
        year3 = float(saleprice) - dec2
        dec3 = (float(saleprice)*dec2)/100
    if days > 1095:
        year4 = float(saleprice) - dec3
        dec4 = (float(saleprice)*dec3)/100
    if days > 1460:
        year5 = float(saleprice) - dec4

    ext_price = year1 + year2 + year3 + year4 + year5

    Sql.RunQuery("UPDATE SAQICO SET SALES_PRICE = '{saleprice}', DISCOUNT = '{discount}',YEAR_1 = {y1},YEAR_2 = {y2},YEAR_3={y3},YEAR_4={y4},YEAR_5 = {y5},EXTENDED_PRICE = {ext} WHERE SERVICE_ID = '{service_id}' and QUOTE_RECORD_ID = '{QuoteRecordId}'".format(saleprice=saleprice,service_id=service_id ,QuoteRecordId=Quote.GetGlobal("contract_quote_record_id"),discount=discount,y1=year1,y2=year2,y3=year3,y4=year4,y5=year5,ext=ext_price))
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
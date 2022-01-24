# =========================================================================================================================================
#   __script_name : CQCUSTFLDS.PY
#   __script_description : THIS SCRIPT IS USED TO ASSIGNT THE CUSTOM FIELD VALUE TO THE CORRESPONDING CUSTOMG FIELDS.
#   __primary_author__ :GAYATHRI AMARESAN
#   __create_date :
#   Ã‚Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
from SYDATABASE import SQL

Sql = SQL()

def custfieldsupdated(saleprice,service_id,lineitemid,discount):
	saleprice = float(saleprice)
	lineitemid = float(lineitemid)
	getdates = Sql.GetFirst("SELECT CONTRACT_VALID_FROM,CONTRACT_VALID_TO FROM SAQTMT WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{}'".format(a.QUOTE_RECORD_ID))

	import datetime as dt
	fmt = '%m/%d/%Y'
	d1 = dt.datetime.strptime(str(getdates.CONTRACT_VALID_FROM).split(" ")[0], fmt)
	d2 = dt.datetime.strptime(str(getdates.CONTRACT_VALID_TO).split(" ")[0], fmt)
	days = (d2 - d1).days
	yoy = float(a.YEAR_OVER_YEAR)

	year1 = float(saleprice)
	year2 = 0.00
	year3 = 0.00
	year4 = 0.00
	year5 = 0.00
	dec1 = (float(saleprice)*yoy)/100
	Trace.Write("dec1---"+str(dec1))

	if days > 365:
		year2 = float(saleprice) - dec1
		dec2 = (year2*yoy)/100
		Trace.Write("dec2---"+str(dec2))
	if days > 730:
		year3 = year2 - dec2
		dec3 = (year3*yoy)/100
		Trace.Write("dec3---"+str(dec3))
	if days > 1095:
		year4 = year3 - dec3
		dec4 = (year4*yoy)/100
	if days > 1460:
		year5 = year4 - dec4    

	ext_price = year1 + year2 + year3 + year4 + year5

	# Sql.RunQuery("UPDATE SAQITM SET SALES_PRICE = '{saleprice}', DISCOUNT = '{discount}',YEAR_1 = {y1},YEAR_2 = {y2},YEAR_3={y3},YEAR_4={y4},YEAR_5 = {y5},EXTENDED_PRICE = {ext} WHERE SERVICE_ID like '%{service_id}%' and QUOTE_RECORD_ID = '{QuoteRecordId}' and LINE_ITEM_ID = {lineitemid} and QTEREV_RECORD_ID = '{RevisionRecordId}'".format(saleprice=saleprice,service_id=service_id ,QuoteRecordId=Quote.GetGlobal("contract_quote_record_id"),discount=discount,y1=year1,y2=year2,y3=year3,y4=year4,y5=year5,ext=ext_price,lineitemid = lineitemid,RevisionRecordId = Quote.GetGlobal("quote_revision_record_id")))
	for item in Quote.MainItems:
		Trace.Write("Quote Quote Quote")
		item_number = int(item.RolledUpQuoteItem)
		service_id = item.PartNumber
		if  service_id == item.PartNumber and item_number == lineitemid:
			Trace.Write("service_id")
			item.YEAR_OVER_YEAR.Value = yoy
			item.NET_PRICE.Value = saleprice
			item.DISCOUNT.Value = discount
			item.YEAR_1.Value = year1
			item.YEAR_2.Value = year2
			item.YEAR_3.Value = year3
			item.YEAR_4.Value = year4
			item.YEAR_5.Value = year5
			item.EXTENDED_PRICE.Value = ext_price
	##SAQICO update based on the header values....        
	quoteitem_covered_obj = SqlHelper.GetFirst("select count(CpqTableEntryId) as cnt from SAQICO where SERVICE_ID = '{service_id}'and QUOTE_RECORD_ID = '{quote_record_id}' and LINE_ITEM_ID = {lineitemid} ".format(service_id = service_id,quote_record_id = Quote.GetGlobal("contract_quote_record_id"),lineitemid = lineitemid))
	count = quoteitem_covered_obj.cnt
	Trace.Write("count of SAQICO "+str(count))
	covered_obj_sale_price = saleprice/count
	yr1 = year1/count
	yr2 = year2/count
	yr3 = year3/count
	yr4 = year4/count
	yr5 = year5/count
	yearoveryear = yoy
	sales_discount_price = float(a.SALES_DISCOUNT_PRICE)/count
	extended_price = ext_price/count
	
	update_sales_price = "UPDATE SAQICO SET DISCOUNT = '{discount}',YEAR_1 = {y1},YEAR_2 = {y2},YEAR_3={y3},YEAR_4={y4},YEAR_5 = {y5},EXTENDED_PRICE = {ext},SALES_DISCOUNT_PRICE = {sales_discount_price},YEAR_OVER_YEAR = {yearoveryear}  WHERE SERVICE_ID like '%{service_id}%' and QUOTE_RECORD_ID = '{QuoteRecordId}' and LINE_ITEM_ID = {lineitemid} and QTEREV_RECORD_ID = '{RevisionRecordId}' ".format(
	service_id=service_id ,QuoteRecordId=Quote.GetGlobal("contract_quote_record_id"),discount=discount,y1=yr1,y2=yr2,y3=yr3,y4=yr4,y5=yr5,ext=extended_price,sales_discount_price = sales_discount_price,lineitemid =lineitemid,yearoveryear= yearoveryear,RevisionRecordId = Quote.GetGlobal("quote_revision_record_id")
	)
	Sql.RunQuery(update_sales_price)
	
	Sql.RunQuery("""UPDATE SAQTRV
						SET 									
						SAQTRV.NET_PRICE_INGL_CURR = IQ.NET_PRICE_INGL_CURR					
						FROM SAQTRV (NOLOCK)
						INNER JOIN (SELECT SAQRIT.QUOTE_RECORD_ID, SAQRIT.QTEREV_RECORD_ID,
									SUM(ISNULL(SAQRIT.NET_PRICE_INGL_CURR, 0)) as NET_PRICE_INGL_CURR					
									FROM SAQRIT (NOLOCK) WHERE SAQRIT.QUOTE_RECORD_ID = '{quote_rec_id}' AND SAQRIT.QTEREV_RECORD_ID = '{quote_revision_rec_id}' GROUP BY SAQRIT.QTEREV_RECORD_ID, SAQRIT.QUOTE_RECORD_ID) IQ ON SAQTRV.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND SAQTRV.QUOTE_REVISION_RECORD_ID = IQ.QTEREV_RECORD_ID
						WHERE SAQTRV.QUOTE_RECORD_ID = '{quote_rec_id}' AND SAQTRV.QUOTE_REVISION_RECORD_ID = '{quote_revision_rec_id}'""".format( quote_rec_id = Quote.GetGlobal("contract_quote_record_id"),quote_revision_rec_id = Quote.GetGlobal("quote_revision_record_id")))
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
	#Trace.Write("342"+str(e))
try:
	service_id = Param.service_id
except Exception:
	service_id = ""
try:
	lineitemid = Param.lineitemid
except Exception:
	lineitemid = ""
try:
	discount = Param.discount
except Exception:
	discount = ""

if customfield == "Yes":
	ApiResponse = ApiResponseFactory.JsonResponse(custfieldsupdated(saleprice,service_id,lineitemid,discount))
elif service_id != "":
	ApiResponse = ApiResponseFactory.JsonResponse(salepriceedit(service_id))
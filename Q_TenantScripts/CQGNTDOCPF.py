import Webcom.Configurator.Scripting.Test.TestProduct
#GDLIST = Quote.GetGeneratedDocumentList('AMAT Quote')
RECORD_ID = Param.RECORD_ID
GetActiveRevision = SqlHelper.GetFirst("SELECT QUOTE_REVISION_RECORD_ID,QTEREV_ID FROM SAQTRV (NOLOCK) WHERE QUOTE_ID ='{}' AND ACTIVE = 1".format(Quote.CompositeNumber))
get_doc_details = SqlHelper.GetFirst("SELECT BILLING_INCLUDED,ITEM_INCLUDED,PRTLST_INCLUDED,DVYSCH_INCLUDED from SAQDOC where DOCUMENT_NAME='{doc_id}' and QTEREV_ID='{active_rev}'".format(doc_id =RECORD_ID,active_rev= GetActiveRevision.QTEREV_ID))
if get_doc_details:
	if get_doc_details.BILLING_INCLUDED:
		val_bills = get_doc_details.BILLING_INCLUDED
	else:
		val_bills = 'No'
	if get_doc_details.ITEM_INCLUDED:
		VAl_ITEMS = get_doc_details.ITEM_INCLUDED
	else:
		VAl_ITEMS = 'No'
	if get_doc_details.PRTLST_INCLUDED:
		VAl_PRTLST = get_doc_details.PRTLST_INCLUDED
	else:
		VAl_PRTLST = 'No'
	if get_doc_details.DVYSCH_INCLUDED:
		val_delivery_periods = get_doc_details.DVYSCH_INCLUDED
	else:
		val_delivery_periods = 'No'
	if val_bills == True and VAl_ITEMS == True:
		Trace.Write('10--')
		Quote.GetCustomField('Billing_Matrix').Content = 'YES'
		Quote.GetCustomField('QT_OD_DELIVERY_SERVICE').Content = 'NO'
	elif val_delivery_periods == True:
		Quote.GetCustomField('QT_OD_DELIVERY_SERVICE').Content = 'YES'
		Quote.GetCustomField('ITEM_DELIVERY_SCHEDULE').Content = 'YES'
	else:
		Quote.GetCustomField('QT_OD_DELIVERY_SERVICE').Content = "NO_GENERATE_DELIVERY"

#Trace.Write('val_bills--'+str(val_bills)+'---get_delivery_parts---'+str(get_delivery_parts))
GDLIST = Quote.GetGeneratedDocumentList('AMAT_SUBTOTAL_OFFERING')
get_delivery_parts = Quote.GetCustomField('ITEM_DELIVERY_SCHEDULE').Content
get_bill_matrix = Quote.GetCustomField('Billing_Matrix').Content
gets_delivery_parts_z0110 = Quote.GetCustomField('PARTS_DELIVERY_SCHEDULE').Content
fpm_delivery_schedules = Quote.GetCustomField('QT_OD_DELIVERY_SERVICE').Content
if get_delivery_parts == "YES" and fpm_delivery_schedules == "YES":
	GDLIST = Quote.GetGeneratedDocumentList('AMAT_FPM_QUOTE')
elif fpm_delivery_schedules == "NO_GENERATE_DELIVERY":
	GDLIST = Quote.GetGeneratedDocumentList('Amat FPM Z0110')
elif get_bill_matrix == "YES":
	GDLIST = Quote.GetGeneratedDocumentList('AMAT Total Quote')
else:
	GDLIST = Quote.GetGeneratedDocumentList('AMAT_SUBTOTAL_OFFERING')


Trace.Write('RECORD_ID--'+str(RECORD_ID))
for gndc in GDLIST:
	docid = gndc.Id
	if docid:
		fileContent = Quote.GetLatestGeneratedDocumentInBytes()
		fileName = Quote.GetLatestGeneratedDocumentFileName()

		responseJson = {"ErrorMsg":None, "File":fileContent, "FileName":fileName}

		ApiResponse = ApiResponseFactory.JsonResponse(responseJson)
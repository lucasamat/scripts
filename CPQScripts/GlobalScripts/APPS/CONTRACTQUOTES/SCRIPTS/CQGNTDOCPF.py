import Webcom.Configurator.Scripting.Test.TestProduct
#GDLIST = Quote.GetGeneratedDocumentList('AMAT Quote')
GDLIST = Quote.GetGeneratedDocumentList('AMAT_SUBTOTAL_OFFERING')
get_delivery_parts = Quote.GetCustomField('ITEM_DELIVERY_SCHEDULE').Content

for gndc in GDLIST:
    docid = gndc.Id
    if docid:
        fileContent = Quote.GetLatestGeneratedDocumentInBytes()
        fileName = Quote.GetLatestGeneratedDocumentFileName()

        responseJson = {"ErrorMsg":None, "File":fileContent, "FileName":fileName}

        ApiResponse = ApiResponseFactory.JsonResponse(responseJson)
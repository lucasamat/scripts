# =========================================================================================================================================
#   __script_name : CQSPLITQTE.PY
#   __script_description : THIS SCRIPT IS USED TO SPLIT THE ITEMS BY PRODUCT OFFERINGS
#   __primary_author__ : WASIM.ABDUL
#   __create_date :12-13-2021
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct
import clr
import System.Net
import sys
import re
import datetime
from System.Net import CookieContainer, NetworkCredential, Mail
from System.Net.Mail import SmtpClient, MailAddress, Attachment, MailMessage
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

contract_quote_rec_id = Quote.GetGlobal("contract_quote_record_id")
quote_revision_rec_id = Quote.GetGlobal("quote_revision_record_id")
user_id = str(User.Id)
user_name = str(User.UserName) 

def splitserviceinsert():
    splitservice_object = 'Z0105'
    material_obj = Sql.GetFirst("SELECT MATERIAL_RECORD_ID,SAP_DESCRIPTION,MATERIALCONFIG_TYPE FROM MAMTRL WHERE SAP_PART_NUMBER = '{}'".format(splitservice_object))
    service_list=[]
    get_existing_record = Sql.GetList("SELECT * FROM SAQIAC WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND ENTITLEMENT_NAME ='Split Quote' AND ENTITLEMENT_DISPLAY_VALUE = 'Yes'".format(contract_quote_rec_id,quote_revision_rec_id))
    for i in get_existing_record:
        service_list.append(i.SERVICE_ID)
    parservice_values=tuple(service_list)
    parservice_values=re.sub('\,\)',')',str(parservice_values))
    if get_existing_record:
        description = material_obj.SAP_DESCRIPTION
        material_record_id = material_obj.MATERIAL_RECORD_ID

        Sql.RunQuery("""INSERT SAQTSV (QTEREV_RECORD_ID,QTEREV_ID,QUOTE_ID, QUOTE_NAME,UOM_ID,UOM_RECORD_ID, QUOTE_RECORD_ID, SERVICE_DESCRIPTION, SERVICE_ID, PAR_SERVICE_ID,PAR_SERVICE_DESCRIPTION,PAR_SERVICE_RECORD_ID,SERVICE_RECORD_ID, SERVICE_TYPE, CONTRACT_VALID_FROM, CONTRACT_VALID_TO, SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID, QUOTE_SERVICE_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified)
                        SELECT A.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED, {UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
                        SELECT DISTINCT QTEREV_RECORD_ID, QTEREV_ID,QUOTE_ID, QUOTE_NAME,UOM_ID,UOM_RECORD_ID, QUOTE_RECORD_ID, '{description}' AS SERVICE_DESCRIPTION, '{splitservice_object}' AS SERVICE_ID,SERVICE_ID as PAR_SERVICE_ID,SERVICE_DESCRIPTION AS PAR_SERVICE_DESCRIPTION,QUOTE_SERVICE_RECORD_ID as PAR_SERVICE_RECORD_ID, '{material_record_id}' AS SERVICE_RECORD_ID, '' AS SERVICE_TYPE, CONTRACT_VALID_FROM, CONTRACT_VALID_TO, SALESORG_ID, SALESORG_NAME,SALESORG_RECORD_ID FROM SAQTSV (NOLOCK)
                        WHERE SERVICE_ID IN {service_id} AND QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_rec_id}' 
                        ) A""".format(description=description, service_id = parservice_values, material_record_id = material_record_id,contract_quote_rec_id = contract_quote_rec_id , quote_revision_rec_id = quote_revision_rec_id ,UserName = user_name, UserId = user_id,splitservice_object = splitservice_object ))
    
    ###split the items with new insert and updation:
    split_service =Sql.GetFirst("Select * FROM SAQTSV WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID ='Z0105'".format(contract_quote_rec_id,quote_revision_rec_id))
    splitservice_id = split_service.SERVICE_ID
    splitservice_name = split_service.SERVICE_DESCRIPTION
    splitservice_recid = split_service.SERVICE_RECORD_ID
    equipments_count = 0
    quote_item_obj = SqlHelper.GetFirst("SELECT TOP 1 LINE FROM SAQRIT (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' ORDER BY LINE DESC".format(QuoteRecordId=contract_quote_rec_id,RevisionRecordId=quote_revision_rec_id))
    if quote_item_obj:
	    equipments_count = int(quote_item_obj.LINE)
    QueryStatement ="""MERGE SAQRIT SRC USING (SELECT QUOTE_REVISION_CONTRACT_ITEM_ID,CONTRACT_VALID_FROM, CONTRACT_VALID_TO, DOC_CURRENCY, DOCURR_RECORD_ID, EXCHANGE_RATE, EXCHANGE_RATE_DATE, EXCHANGE_RATE_RECORD_ID, GL_ACCOUNT_NO, GLOBAL_CURRENCY, GLOBAL_CURRENCY_RECORD_ID, ROW_NUMBER()OVER(ORDER BY(SAQRIT.CpqTableEntryId)) + {equipments_count} as LINE2,LINE,OBJECT_ID, OBJECT_TYPE, FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, PROFIT_CENTER, QUANTITY, QUOTE_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, REF_SALESORDER, STATUS, TAXCLASSIFICATION_DESCRIPTION, TAXCLASSIFICATION_ID, TAXCLASSIFICATION_RECORD_ID,NET_VALUE_INGL_CURR, NET_PRICE_INGL_CURR,ESTVAL_INGL_CURR, COMVAL_INGL_CURR, GREENBOOK, GREENBOOK_RECORD_ID, QTEITMSUM_RECORD_ID,PARQTEITM_LINE FROM SAQRIT where QUOTE_RECORD_ID = '{contract_quote_record_id}' AND QTEREV_RECORD_ID  = '{contract_quote_revision_record_id}')
    TGT ON (SRC.QUOTE_RECORD_ID = TGT.QUOTE_RECORD_ID AND SRC.QTEREV_RECORD_ID = TGT.QTEREV_RECORD_ID AND SRC.SERVICE_ID = 'Z0105')
    WHEN NOT MATCHED BY TARGET
    THEN INSERT(QUOTE_REVISION_CONTRACT_ITEM_ID,CONTRACT_VALID_FROM, CONTRACT_VALID_TO, DOC_CURRENCY, DOCURR_RECORD_ID, EXCHANGE_RATE, EXCHANGE_RATE_DATE, EXCHANGE_RATE_RECORD_ID, GL_ACCOUNT_NO, GLOBAL_CURRENCY, GLOBAL_CURRENCY_RECORD_ID, LINE, OBJECT_ID, OBJECT_TYPE, FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, PROFIT_CENTER, QUANTITY, QUOTE_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, REF_SALESORDER, STATUS, TAXCLASSIFICATION_DESCRIPTION, TAXCLASSIFICATION_ID, TAXCLASSIFICATION_RECORD_ID,NET_VALUE_INGL_CURR, NET_PRICE_INGL_CURR,ESTVAL_INGL_CURR, COMVAL_INGL_CURR, GREENBOOK, GREENBOOK_RECORD_ID, QTEITMSUM_RECORD_ID,PARQTEITM_LINE)
    VALUES (NEWID(),CONTRACT_VALID_FROM, CONTRACT_VALID_TO, DOC_CURRENCY, DOCURR_RECORD_ID, EXCHANGE_RATE, EXCHANGE_RATE_DATE, EXCHANGE_RATE_RECORD_ID, GL_ACCOUNT_NO, GLOBAL_CURRENCY, GLOBAL_CURRENCY_RECORD_ID,LINE2, OBJECT_ID, OBJECT_TYPE, FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, '{splitservice_recid}', '{splitservice_id}', '{splitservice_name}', PROFIT_CENTER, QUANTITY, QUOTE_ID, '{contract_quote_record_id}', QTEREV_ID, '{contract_quote_revision_record_id}', REF_SALESORDER, STATUS, TAXCLASSIFICATION_DESCRIPTION, TAXCLASSIFICATION_ID, TAXCLASSIFICATION_RECORD_ID,NET_VALUE_INGL_CURR, NET_PRICE_INGL_CURR,ESTVAL_INGL_CURR, COMVAL_INGL_CURR, GREENBOOK, GREENBOOK_RECORD_ID, QTEITMSUM_RECORD_ID,LINE);""".format(contract_quote_record_id=contract_quote_rec_id,contract_quote_revision_record_id = quote_revision_rec_id,splitservice_recid = splitservice_recid,splitservice_id=splitservice_id,splitservice_name = splitservice_name,equipments_count =equipments_count )
    Sql.RunQuery(QueryStatement)
        

splitserviceinsert()

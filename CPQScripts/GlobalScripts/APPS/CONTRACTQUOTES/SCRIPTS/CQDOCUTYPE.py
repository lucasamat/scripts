# ====================================================================================================================
#   __script_name : CQDOCUTYPE.PY
#   __script_description : THIS SCRIPT IS USED TO DETERMINE THE DOCUMENT TYPE BASED ON THE SERVICE OFFERING
#   __primary_author__ : GAYATHRI AMARESAN
#   __create_date :
#   Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ====================================================================================================================
import clr
import System.Net
from System.Text.Encoding import UTF8
from System import Convert
import sys
from SYDATABASE import SQL
Sql = SQL()

def update_document_type(QuoteRecordId,RevisionRecordId):
    document_type_list = []
    service_obj  = Sql.GetList("select SERVICE_ID from SAQTSV(NOLOCK) where QUOTE_RECORD_ID = '{QuoteRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}'".format(QuoteRecordId = Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id")))
    Quote_obj = Sql.GetFirst("SELECT POES FROM  SAQTMT(NOLOCK) WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{QuoteRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}'".format(QuoteRecordId = Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id")))
    for service in service_obj:
        #Log.Info("service_obj--------------->"+str(service.SERVICE_ID))
        document_type_obj = Sql.GetFirst("select DOCTYP_ID from MAMADT(NOLOCK) where SAP_PART_NUMBER = '{}' AND POES ='{}'".format(service.SERVICE_ID,Quote_obj.POES))
        #Log.Info("document_type_obj--------------->"+str(document_type_obj.DOCTYP_ID))
        if document_type_obj is not None:
            document_type_list.append(document_type_obj.DOCTYP_ID)
    if 'ZTBC' in document_type_list:
        document_type = 'ZTBC'
    elif not service_obj:
        document_type = 'ZTBC'
    else:
        document_type = document_type_obj.DOCTYP_ID
    #Log.Info(document_type_list)
    document_type_obj = Sql.GetFirst("select DOCTYP_ID,DOCTYP_RECORD_ID from MAMADT(NOLOCK) where DOCTYP_ID = '{}' AND POES ='{}' ".format(document_type,Quote_obj.POES))
    #Log.Info("UPDATE SAQTRV SET DOCTYP_ID = '{DocumentType}',DOCTYP_RECORD_ID = '{DocumentTypeRecordId}' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' ".format(DocumentType = document_type,DocumentTypeRecordId = document_type_obj.DOCTYP_RECORD_ID,QuoteRecordId = Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id")))
    Sql.RunQuery("UPDATE SAQTRV SET DOCTYP_ID = '{DocumentType}',DOCTYP_RECORD_ID = '{DocumentTypeRecordId}' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' ".format(DocumentType = document_type,DocumentTypeRecordId = document_type_obj.DOCTYP_RECORD_ID,QuoteRecordId = Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id")))

try:
    QuoteRecordId = Param.QUOTE_RECORD_ID
    RevisionRecordId = Param.QTEREV_RECORD_ID
except:
    QuoteRecordId = ""
    RevisionRecordId = ""    
update_document_type(QuoteRecordId,RevisionRecordId)

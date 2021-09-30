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

def update_document_type(QuoteRecordId,RevisionRecordId,ServicerecordId):
    service_obj  = Sql.GetFirst("select SERVICE_ID from SAQTSV(NOLOCK) where QUOTE_RECORD_ID = '{QuoteRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID = '{ServicerecordId}'".format(QuoteRecordId = Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"),ServicerecordId = ServicerecordId))
    
    Quote_obj = Sql.GetFirst("SELECT POES FROM SAQTMT(NOLOCK) WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{QuoteRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}'".format(QuoteRecordId = Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id")))
    
    if service_obj:
        document_type_obj = Sql.GetFirst("select DOCTYP_ID,DOCTYP_RECORD_ID from MAMADT(NOLOCK) where SAP_PART_NUMBER = '{}' AND POES ='{}'".format(service.SERVICE_ID,Quote_obj.POES))
    else:
        document_type_obj = Sql.GetFirst("select DOCTYP_ID,DOCTYP_RECORD_ID from MAMADT where DOCTYP_ID ='ZTBC'")

    Sql.RunQuery("UPDATE SAQTRV SET DOCTYP_ID = '{DocumentType}',DOCTYP_RECORD_ID = '{DocumentTypeRecordId}' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' ".format(DocumentType = document_type_obj.DOCTYP_ID,DocumentTypeRecordId = document_type_obj.DOCTYP_RECORD_ID,QuoteRecordId = Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id")))
    Sql.RunQuery("UPDATE SAQTSV SET DOCTYP_ID = '{DocumentType}',DOCTYP_RECORD_ID = '{DocumentTypeRecordId}' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' and SERVICE_ID = '{ServicerecordId}'".format(DocumentType = document_type_obj.DOCTYP_ID,DocumentTypeRecordId = document_type_obj.DOCTYP_RECORD_ID,QuoteRecordId = Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"),ServicerecordId = ServicerecordId))
        
try:
    QuoteRecordId = Param.QUOTE_RECORD_ID
    RevisionRecordId = Param.QTEREV_RECORD_ID
    ServicerecordId = Param.SERVICE_ID
except:
    QuoteRecordId = ""
    RevisionRecordId = "" 
    ServicerecordId = ""   
update_document_type(QuoteRecordId,RevisionRecordId,ServicerecordId)

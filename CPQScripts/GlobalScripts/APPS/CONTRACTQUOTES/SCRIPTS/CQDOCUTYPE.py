# ====================================================================================================================
#   __script_name : CQDOCUTYPE.PY
#   __script_description : THIS SCRIPT IS USED TO DETERMINE THE DOCUMENT TYPE BASED ON THE SERVICE OFFERING
#   __primary_author__ : GAYATHRI AMARESAN
#   __create_date :
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ====================================================================================================================
import clr
import System.Net
from System.Text.Encoding import UTF8
from System import Convert
import sys
from SYDATABASE import SQL
Sql = SQL()

def update_document_type(QuoteRecordId,RevisionRecordId):
    service_obj  = Sql.GetList("select SERVICE_ID from SAQTSV where QUOTE_RECORD_ID = '{QuoteRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}'".format(QuoteRecordId = Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id")))
    document_type_list = []
    for service in service_obj:
        document_type_obj = Sql.GetFirst("select DOCTYP_ID from MAMADT where SAP_PART_NUMBER = '{}'".format(service.SERVICE_ID))
        if document_type_obj is not None:
            document_type_list.append(document_type_obj.DOCTYP_ID)
    if 'ZTBC' in document_type_list:
        document_type = 'ZTBC'
    else:
        document_type = document_type_obj.DOCTYP_ID
    document_type_obj = Sql.GetFirst("select DOCTYP_ID,DOCTYP_RECORD_ID from MAMADT where DOCTYP_ID = '{}'".format(document_type))
    Sql.RunQuery("UPDATE SAQTRV SET DOCTYP_ID = '{DocumentType}',DOCTYP_RECORD_ID = '{DocumentTypeRecordId}' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' ".format(DocumentType = document_type,DocumentTypeRecordId = document_type_obj.DOCTYP_RECORD_ID,QuoteRecordId = Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id")))
    Log.Info("inside the function call--------------->")

try:
    QuoteRecordId = Param.QUOTE_RECORD_ID
    RevisionRecordId = Param.QTEREV_RECORD_ID
except:
    QuoteRecordId = Param.QUOTE_RECORD_ID
    RevisionRecordId = Param.QTEREV_RECORD_ID    
update_document_type(QuoteRecordId,RevisionRecordId)
Log.Info("function called---------------->")
# except:
#     Log.Info("CQDOCUTYPE ERROR---->:" + str(sys.exc_info()[1]))
#     Log.Info("CQDOCUTYPE ERROR LINE NO---->:" + str(sys.exc_info()[-1].tb_lineno))

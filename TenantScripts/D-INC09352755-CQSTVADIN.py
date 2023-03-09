import re
import Webcom.Configurator.Scripting.Test.TestProduct
from SYDATABASE import SQL
import CQPARTIFLW
import CQCPQC4CWB
import time
import System.Net
from System import Convert
from System.Text.Encoding import UTF8
Sql = SQL()


quote_item_insert = 'yes'

Text = "COMPLETE STAGE"
#it is empty
status = "CONFIGURE"

try:
    contract_quote_rec_id = Quote.GetGlobal("contract_quote_record_id")
except:
    contract_quote_rec_id = ''
try:
    quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")	
except:
    quote_revision_record_id =  ""
    
    
get_quality_required = Sql.GetFirst("SELECT COUNT(CPQTABLEENTRYADDEDBY) as CNT FROM SAQFBL where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND (ISNULL(QUALITY_REQUIRED,'') = '' or QUALITY_REQUIRED ='Select')".format(Quote.GetGlobal("contract_quote_record_id"),Quote.GetGlobal("quote_revision_record_id")))
    # removing underscore in the ibase status column will enable retain in configure stage. Temporarily changed for disabling
get_ibase_missing = Sql.GetFirst("SELECT COUNT(CpqTableEntryId) as CNT FROM SAQSCO WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND IBASE_ATTSTS = 'INCOMPLETE'  ".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id))

get_ibase_no_assembly = Sql.GetFirst("SELECT COUNT(CpqTableEntryId) as CNT FROM SAQSCO WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND IBASE_ATTSTS ='NO ASSEMBLY'".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id))
req_event_missing = Sql.GetFirst("SELECT COUNT(CpqTableEntryId) as CNT FROM SAQSCO (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND IBASE_ATTSTS = 'REQUIRED EVENT IS MISSING'  ".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id))

req_event_missing = Sql.GetFirst("SELECT COUNT(CpqTableEntryId) as CNT FROM SAQSCO (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND IBASE_ATTSTS = 'REQUIRED EVENT IS MISSING'  ".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id))

servicelevel_entitilement_obj = Sql.GetFirst("""SELECT COUNT(CONFIGURATION_STATUS) AS CNT FROM SAQTSE(NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND ISNULL(CONFIGURATION_STATUS,'') <> 'COMPLETE'""".format(QuoteRecordId=Quote.GetGlobal("contract_quote_record_id"),QuoteRevisionRecordId=quote_revision_record_id))

get_exchangerate=Sql.GetFirst("SELECT EXCHANGE_RATE FROM SAQTRV WHERE QUOTE_RECORD_ID = '"+str(Quote.GetGlobal("contract_quote_record_id"))+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' ")

#servicelevel_entitilement_obj.CNT = 0
if quote_item_insert == 'yes' and Text == "COMPLETE STAGE" and status not in ("CFG_CONFIGURING_STATUS","PRICING","GENERATE SOW","COMPLETESOW","APPROVALS","LEGAL SOW","QUOTE DOCUMENTS","BOOKED","CLEAN BOOKING CHECKLIST","LEGAL SOW ACCEPT") and get_quality_required.CNT == 0 and req_event_missing.CNT==0 and get_ibase_missing.CNT==0 and get_ibase_no_assembly.CNT==0 and servicelevel_entitilement_obj.CNT == 0 and get_exchangerate.EXCHANGE_RATE:
    Trace.Write('quote_item_insert--'+str(quote_item_insert))
        #A055S000P01-20612 end
service_id_query = Sql.GetList("SELECT SAQTSV.*,MAMTRL.MATERIALCONFIG_TYPE FROM SAQTSV INNER JOIN MAMTRL ON SAP_PART_NUMBER = SERVICE_ID WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'  ".format(contract_quote_rec_id,quote_revision_record_id))
if service_id_query:
    for service_id in service_id_query:
        get_ent_config_status = Sql.GetFirst(""" SELECT COUNT(CONFIGURATION_STATUS) AS COUNT FROM SAQTSE (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID = '{}' AND CONFIGURATION_STATUS='COMPLETE' """.format(contract_quote_rec_id,quote_revision_record_id,service_id.SERVICE_ID))
        if get_ent_config_status.COUNT > 0 or service_id.MATERIALCONFIG_TYPE =='SIMPLE MATERIAL' or (service_id.SERVICE_ID in ('Z0114','Z0117')):
                   Trace.Write('it works')
                    	#data = ScriptExecutor.ExecuteGlobal("CQINSQTITM",{"ContractQuoteRecordId":contract_quote_rec_id,"ContractQuoteRevisionRecordId":quote_revision_record_id, "ServiceId":service_id.SERVICE_ID, "ActionType":'INSERT_LINE_ITEMS'})

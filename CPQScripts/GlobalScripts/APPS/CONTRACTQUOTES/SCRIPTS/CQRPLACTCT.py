# =========================================================================================================================================
#   __script_name : CQRPLACTCT.PY
#   __script_description : THIS SCRIPT IS USED TO REPLACE ACCOUNT AND CONTACT WHEN USER CLICKS ON REPLACE BUTTON ON A RELATED LIST RECORD.
#   __primary_author__ : WASIM ABDUL
#   __create_date : 19/10/2021
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import datetime
import Webcom.Configurator.Scripting.Test.TestProduct
import sys
import re
import System.Net
import SYCNGEGUID as CPQID
from SYDATABASE import SQL

Sql = SQL()
ScriptExecutor = ScriptExecutor
contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
def replace_account(repalce_values,acct_rec_id,table_name):
    Trace.Write("repalce_values===="+str(repalce_values))
    Trace.Write("acct_rec_id===="+str(acct_rec_id))
    Trace.Write("table_name===="+str(table_name))
    
    # acc_data_chk = Sql.GetFirst("Select * from SAQTIP(NOLOCK) WHERE QUOTE_RECORD_ID ='{}' AND QTEREV_RECORD_ID = '{}' AND QUOTE_INVOLVED_PARTY_RECORD_ID ='{}'".format(contract_quote_record_id,quote_revision_record_id,acct_rec_id))
    # rpl_data_chk =Sql.GetFirst("Select * FROM SAACNT(NOLOCK) WHERE ACCOUNT_RECORD_ID = '{}'".format(repalce_values))
    # if acc_data_chk:
    #     Sql.RunQuery("UPDATE SAQTIP SET PARTY_ID = '{party_id}',PARTY_NAME = '{party_name}',ADDRESS ='{address}',EMAIL ='{email}',PHONE = '{phone}',PARTY_RECORD_ID = '{part_rec_id}' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' and QUOTE_INVOLVED_PARTY_RECORD_ID ='{acct_rec_id}' ".format(party_id = rpl_data_chk.ACCOUNT_ID,party_name = rpl_data_chk.ACCOUNT_NAME,address = rpl_data_chk.ADDRESS_1,email=rpl_data_chk.EMAIL,phone= rpl_data_chk.PHONE,part_rec_id =rpl_data_chk.ACCOUNT_RECORD_ID,QuoteRecordId = contract_quote_record_id,RevisionRecordId = quote_revision_record_id,acct_rec_id = acct_rec_id)) 

try:
    repalce_values = Param.repalce_values
    acct_rec_id = Param.acct_rec_id
    table_name = Param.table_name

except:
    repalce_values ='' 
    acct_rec_id = '' 
    table_name = '' 
replace_account(repalce_values,acct_rec_id,table_name)


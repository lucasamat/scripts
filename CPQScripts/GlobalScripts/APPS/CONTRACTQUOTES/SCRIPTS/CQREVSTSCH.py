# =========================================================================================================================================
#   __script_name : CQREVSTSCH.PY
#   __script_description : THIS SCRIPT IS USED TO INSERT RECORDS INTO SAQRSH WHEN CHANGING THE REVISION STATUS
#   __primary_author__ : KRISHNA CHAITANYA
#   __create_date :25-11-2021
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================

import datetime
import sys
import re
import System.Net
import SYCNGEGUID as CPQID
from SYDATABASE import SQL

Sql = SQL()

# try:
#     contract_quote_record_id = Quote.QuoteId
# except:
#     contract_quote_record_id = ''

# try:
#     quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
# except:
#     quote_revision_record_id = ""
 

def Revisionstatusdatecapture(contract_quote_record_id,quote_revision_record_id):
    saqtrv_values = Sql.GetFirst("SELECT SALESORG_ID from SAQTRV where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(quote_revision_record_id,quote_revision_record_id))
    
    self._process_query(""" INSERT SAQRSH (							
                        QUOTE_RECORD_ID,
                        QUOTE_ID,
                        QTEREV_RECORD_ID,
                        QTEREV_ID,
                        REVISION_STATUS,
                        REVSTS_CHANGE_DATE,							
                        CPQTABLEENTRYADDEDBY,
                        CPQTABLEENTRYDATEADDED,
                        CpqTableEntryModifiedBy,
                        CpqTableEntryDateModified
                        ) SELECT
                            CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REVISION_STATUS_HISTROY_ID,								
                            SAQTRV.QUOTE_RECORD_ID,
                            SAQTRV.QUOTE_ID,
                            SAQTRV.QTEREV_RECORD_ID,
                            SAQTRV.QTEREV_ID,
                            SAQTRV.REVISION_STATUS,
                            '{rev_sts_chg_date}' AS REVSTS_CHANGE_DATE,								
                            '{UserName}' AS CPQTABLEENTRYADDEDBY,
                            GETDATE() as CPQTABLEENTRYDATEADDED,
                            {UserId} as CpqTableEntryModifiedBy,
                            GETDATE() as CpqTableEntryDateModified
                            FROM SAQTRV (NOLOCK) JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQTRV.QUOTE_RECORD_ID								
                            WHERE 
                            SAQTRV.QUOTE_RECORD_ID = '{}'
                            AND SAQTRV.QTEREV_RECORD_ID = '{}'                     
                    """.format(
                            contract_quote_record_id,quote_revision_record_id,				
                            UserName=self.user_name,
                            UserId=self.user_id,rev_sts_chg_date = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p")								
                        ))
        


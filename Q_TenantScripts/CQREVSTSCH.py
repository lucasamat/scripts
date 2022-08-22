# =========================================================================================================================================
#   __script_name : CQREVSTSCH.PY
#   __script_description : THIS SCRIPT IS USED TO INSERT RECORDS INTO SAQRSH WHEN CHANGING THE REVISION STATUS
#   __primary_author__ : KRISHNA CHAITANYA
#   __create_date :25-11-2021
#   Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct
import datetime
import sys
import re
import System.Net
import SYCNGEGUID as CPQID
from SYDATABASE import SQL
ScriptExecutor = ScriptExecutor

Sql = SQL()
 
User_name = ScriptExecutor.ExecuteGlobal("SYUSDETAIL", "USERNAME")
User_Id = ScriptExecutor.ExecuteGlobal("SYUSDETAIL", "USERID")
def Revisionstatusdatecapture(contract_quote_record_id,quote_revision_record_id):
    saqtrv_values = Sql.GetFirst("SELECT * from SAQTRV where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(quote_revision_record_id,quote_revision_record_id))
    # Log.Info(""" INSERT SAQRSH (
    #                     QUOTE_REVISION_STATUS_HISTROY_ID,							
    #                     QUOTE_RECORD_ID,
    #                     QUOTE_ID,
    #                     QTEREV_RECORD_ID,
    #                     QTEREV_ID,
    #                     REVISION_STATUS,
    #                     REVSTS_CHANGE_DATE,							
    #                     CPQTABLEENTRYADDEDBY,
    #                     CPQTABLEENTRYDATEADDED,
    #                     CpqTableEntryModifiedBy,
    #                     CpqTableEntryDateModified
    #                     ) SELECT
    #                         CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REVISION_STATUS_HISTROY_ID,							
    #                         SAQTRV.QUOTE_RECORD_ID,
    #                         SAQTRV.QUOTE_ID,
    #                         SAQTRV.QTEREV_RECORD_ID,
    #                         SAQTRV.QTEREV_ID,
    #                         SAQTRV.REVISION_STATUS,
    #                         '{rev_sts_chg_date}' AS REVSTS_CHANGE_DATE,								
    #                         '{UserName}' AS CPQTABLEENTRYADDEDBY,
    #                         GETDATE() as CPQTABLEENTRYDATEADDED,
    #                         {UserId} as CpqTableEntryModifiedBy,
    #                         GETDATE() as CpqTableEntryDateModified
    #                         FROM SAQTRV (NOLOCK) JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQTRV.QUOTE_RECORD_ID								
    #                         WHERE 
    #                         SAQTRV.QUOTE_RECORD_ID = '{}'
    #                         AND SAQTRV.QTEREV_RECORD_ID = '{}'                     
    #                 """.format(
    #                         contract_quote_record_id,quote_revision_record_id,				
    #                         UserName=User_name,
    #                         UserId=User_Id,rev_sts_chg_date = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p")								
    #                     ))
    QueryStatement = (""" INSERT SAQRSH (
                        QUOTE_REVISION_STATUS_HISTROY_ID,							
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
                        ) SELECT TOP 1
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
                            UserName=User_name,
                            UserId=User_Id,rev_sts_chg_date = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p")								
                        ))
    latest_status = Sql.GetFirst("SELECT TOP 1 SAQRSH.* FROM SAQRSH (NOLOCK) INNER JOIN SAQTRV ON SAQTRV.QUOTE_RECORD_ID = SAQRSH.QUOTE_RECORD_ID AND SAQTRV.REVISION_STATUS = SAQRSH.REVISION_STATUS WHERE SAQTRV.QUOTE_RECORD_ID = '{}' AND SAQTRV.QTEREV_RECORD_ID = '{}' Order By SAQRSH.CpqTableEntryId Desc".format(contract_quote_record_id,quote_revision_record_id)) 
    if latest_status is None:                                       
        Sql.RunQuery(QueryStatement)
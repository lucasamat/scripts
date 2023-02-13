# =========================================================================================================================================
#   __script_name : CQREVSTSCH.PY
#   __script_description : THIS SCRIPT IS USED TO INSERT RECORDS INTO SAQRSH WHEN CHANGING THE REVISION STATUS
#   __primary_author__ : KRISHNA CHAITANYA
#   __create_date :25-11-2021
# ==========================================================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct
import datetime
import sys
import System.Net
from SYDATABASE import SQL
ScriptExecutor = ScriptExecutor

Sql = SQL()
 
def Revisionstatusdatecapture(contract_quote_record_id,quote_revision_record_id):
    #A055S000P01-20944 - Start - M
    latest_status = Sql.GetFirst("SELECT TOP 1 SAQRSH.* FROM SAQRSH (NOLOCK) INNER JOIN SAQTRV ON SAQTRV.QUOTE_RECORD_ID = SAQRSH.QUOTE_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = SAQRSH.QTEREV_RECORD_ID AND SAQTRV.REVISION_STATUS = SAQRSH.REVISION_STATUS WHERE SAQTRV.QUOTE_RECORD_ID = '{}' AND SAQTRV.QTEREV_RECORD_ID = '{}' Order By SAQRSH.CpqTableEntryId Desc".format(contract_quote_record_id,quote_revision_record_id)) 
    if latest_status is None:
        name = ScriptExecutor.ExecuteGlobal("SYUSDETAIL", "NAME")
        User_name = ScriptExecutor.ExecuteGlobal("SYUSDETAIL", "USERNAME")
        User_Id = ScriptExecutor.ExecuteGlobal("SYUSDETAIL", "USERID")
        saqtrv_values = Sql.GetFirst("SELECT QUOTE_ID,QTEREV_ID,REVISION_STATUS from SAQTRV where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(contract_quote_record_id,quote_revision_record_id))
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
        Sql.RunQuery(QueryStatement)
        Log.Info("Quote ID:"+str(saqtrv_values.QUOTE_ID)+"-"+str(saqtrv_values.QTEREV_ID)+" Rev Sts Changed to "+str(saqtrv_values.REVISION_STATUS)+" by "+str(name)+"/"+str(User_name)+"/"+str(User_Id))
        #A055S000P01-20944 - End - M
        
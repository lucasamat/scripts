# ====================================================================================================
#   __script_name : SYERRORLOG.PY
#   __script_description : This script is used to do the database operations in CPQ Custom Tables
#   __primary_author__ : JOE EBENEZER
#   __create_date : 01/23/2019
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ====================================================================================================
from SYDATABASE import sql_run_query, sql_upsert, sql_get_first, sql_get_table


class SYELOG:
    """Model to Log Errors"""

    def __init__(self):
        self.name = "SYELOG"

    def errorMessageEntry(self, tableInfo):
        try:
            tablename = tableInfo.TableName
            tableDataRows = tableInfo.TableDataRows
            for tableRow in tableDataRows:
                TableRow = dict(tableRow.Values)
                Trace.Write("{} : SYELOG NEW ROW VALUES".format(dict(TableRow)))
                Trace.Write("{} :---SYELOG TABLENAME".format(tablename))
                Trace.Write("SYELOG TABLE ROW : {}".format(dict(TableRow)))
                Trace.Write("SELECT * FROM SYOBJH (NOLOCK) WHERE OBJECT_NAME = '{}'".format(tablename))

                ApiNameQuery = sql_get_first(
                    "SELECT * FROM SYOBJH (NOLOCK) WHERE OBJECT_NAME = '{}'".format(tablename)
                )

                if ApiNameQuery and tablename not in ["SEGPQB", "PRLPBE"]:
                    ApiName = ApiNameQuery.RECORD_NAME
                    RecordId = TableRow.get(ApiName, "None")
                    Trace.Write("SYELOG : RECORDID {}".format(RecordId))
                    Trace.Write("SYELOG : APINAME :  {}".format(ApiName))

                    ErrorMessageObjQry = sql_get_first(
                        """
                        SELECT
                            TOP 1000 SYMSGS.RECORD_ID,
                            SYMSGS.TRACK_HISTORY,
                            SYMSGS.TAB_RECORD_ID,
                            SYMSGS.MESSAGE_TEXT,
                            SYMSGS.MESSAGE_TYPE,
                            SYMSGS.MESSAGE_CODE,
                            SYMSGS.MESSAGE_LEVEL,
                            SYMSGS.CTX_CALC_LOGIC AS CCL
                        FROM
                            SYMSGS (NOLOCK)
                        WHERE
                            SYMSGS.CTX_CALC_LOGIC like '%{}%'
                        ORDER BY
                            abs(SYMSGS.MESSAGE_CODE)
                        """.format(
                            "{" + ApiName + "}"
                        )
                    )
                    if ErrorMessageObjQry:
                        for ErrorMessageObj in ErrorMessageObjQry:
                            if not ErrorMessageObj.TRACK_HISTORY:
                                DeleteErr = """
                                    DELETE FROM
                                        SYELOG
                                    WHERE
                                        OBJECT_NAME = '{}'
                                        AND OBJECT_VALUE_REC_ID = '{}'
                                        AND ERRORMESSAGE_RECORD_ID = '{}'
                                    """.format(
                                    tablename, RecordId, ErrorMessageObj.RECORD_ID
                                )
                            else:
                                DeleteErr = """
                                    UPDATE
                                        SYELOG
                                    SET
                                        ACTIVE = 0
                                    FROM
                                        SYELOG
                                    WHERE
                                        OBJECT_NAME = '{}'
                                        AND OBJECT_VALUE_REC_ID = '{}'
                                        AND ERRORMESSAGE_RECORD_ID = '{}'
                                    """.format(
                                    tablename, RecordId, ErrorMessageObj.RECORD_ID
                                )

                            DeleteErr = DeleteErr.replace("'", "''")
                            sql_run_query(DeleteErr)
                            FORMULA = ErrorMessageObj.CCL.replace("{" + ApiName + "}", RecordId)
                            Trace.Write("SYELOG : FORMULA : {}".format(FORMULA))

                            if FORMULA:
                                FORMULA_RESULT = sql_get_first(FORMULA)
                                Trace.Write("SYELOG : FORMULA RESULT : {}".format(FORMULA_RESULT.MESSAGE))
                                if FORMULA_RESULT:
                                    if str(FORMULA_RESULT.MESSAGE).upper() == "TRUE":
                                        import datetime

                                        datetime_value = datetime.datetime.now()

                                        Get_UserID = ScriptExecutor.ExecuteGlobal("SYUSDETAIL", "USERID")
                                        Trace.Write("Get_UserIDGet_UserIDGet_UserID {}".format(Get_UserID))
                                        ErrTable = sql_get_table("SYELOG")
                                        newrow = {
                                            "ERROR_LOGS_RECORD_ID": Guid.NewGuid().upper(),
                                            "ERRORMESSAGE_RECORD_ID": ErrorMessageObj.RECORD_ID,
                                            "OBJECT_RECORD_ID": ErrorMessageObj.TAB_RECORD_ID,
                                            "OBJECT_NAME": tablename,
                                            "ACTIVE": "1",
                                            "ERRORMESSAGE_DESCRIPTION": ErrorMessageObj.MESSAGE_TEXT,
                                            "OBJECT_TYPE": ErrorMessageObj.MESSAGE_TYPE,
                                            "OBJECT_VALUE_REC_ID": RecordId,
                                            "ERRORMESSAGE_ID": ErrorMessageObj.MESSAGE_CODE,
                                            "CPQTABLEENTRYADDEDBY": Get_UserID,
                                            "CPQTABLEENTRYDATEADDED": datetime_value,
                                            "CpqTableEntryModifiedBy": Get_UserID,
                                            "CpqTableEntryDateModified": datetime_value,
                                            "ADDUSR_RECORD_ID": Get_UserID,
                                        }
                                        Trace.Write("SYELOG : NEW ROW : {}".format(newrow))
                                        ErrTable.AddRow(newrow)
                                        sql_upsert(ErrTable)

        except:
            Trace.Write("SYELOG : EXCEPTION")

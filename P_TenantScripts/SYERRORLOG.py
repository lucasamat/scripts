# ====================================================================================================
#   __script_name : SYERRORLOG.PY
#   __script_description : This script is used to do the database operations in CPQ Custom Tables
#   __primary_author__ : JOE EBENEZER
#   __create_date : 01/23/2019
#   Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ====================================================================================================
Trace = Trace  # pylint: disable=E0602
SqlHelper = SqlHelper  # pylint: disable=E0602
ScriptExecutor = ScriptExecutor  # pylint: disable=E0602
Guid = Guid  # pylint: disable=E0602
import Webcom.Configurator.Scripting.Test.TestProduct
from SYDATABASE import SQL


class SYELOG:

    """Model to Log Errors"""

    def __init__(self):
        self.name = "SYELOG"
        self.Sql = SQL()

    def errorMessageEntry(self, tableInfo):
        try:
            tablename = str(tableInfo.TableName)
            tableDataRows = tableInfo.TableDataRows
            for tableRow in tableDataRows:
                TableRow = {}
                TableRow = dict(tableRow.Values)
                Trace.Write(str(dict(TableRow)) + " : SYELOG NEW ROW VALUES")
                Trace.Write(str(tablename) + " :---SYELOG TABLENAME")
                Trace.Write("SYELOG TABLE ROW : " + str(dict(TableRow)))
                Trace.Write("SELECT * FROM SYOBJH (NOLOCK) WHERE OBJECT_NAME = '" + str(tablename) + "'")
                ApiNameQuery = SqlHelper.GetFirst(
                    "SELECT * FROM SYOBJH (NOLOCK) WHERE OBJECT_NAME = '" + str(tablename) + "'"
                )
                if ApiNameQuery is not None and str(tablename) != "SEGPQB" and str(tablename) != "PRLPBE":
                    ApiName = str(ApiNameQuery.RECORD_NAME)
                    RecordId = str(TableRow.get(ApiName))
                    Trace.Write("SYELOG : RECORDID " + str(RecordId))
                    #Trace.Write("SYELOG : DELETED ROWS IN SYELOG")
                    Trace.Write("SYELOG : APINAME :  " + str(ApiName))
                    ErrorMessageObjQry = SqlHelper.GetList(
                        "SELECT TOP 1000 SYMSGS.RECORD_ID, SYMSGS.TRACK_HISTORY, SYMSGS.TAB_RECORD_ID, SYMSGS.MESSAGE_TEXT, SYMSGS.MESSAGE_TYPE, SYMSGS.MESSAGE_CODE, "
                        + " SYMSGS.MESSAGE_LEVEL, SYMSGS.CTX_CALC_LOGIC AS CCL FROM SYMSGS (NOLOCK) WHERE SYMSGS.CTX_CALC_LOGIC like '%{"
                        + str(ApiName)
                        + "}%' ORDER BY abs(SYMSGS.MESSAGE_CODE)"
                    )
                    if ErrorMessageObjQry is not None:
                        for ErrorMessageObj in ErrorMessageObjQry:
                            if ErrorMessageObj.TRACK_HISTORY == 0:
                                DeleteErr = (
                                    "DELETE FROM SYELOG WHERE OBJECT_NAME = '"
                                    + str(tablename)
                                    + "' AND OBJECT_VALUE_REC_ID = '"
                                    + str(RecordId)
                                    + "' AND ERRORMESSAGE_RECORD_ID = '"
                                    + str(ErrorMessageObj.RECORD_ID)
                                    + "'"
                                )
                            else:
                                DeleteErr = (
                                    "update SYELOG set ACTIVE = 0 FROM SYELOG WHERE OBJECT_NAME = '"
                                    + str(tablename)
                                    + "' AND OBJECT_VALUE_REC_ID = '"
                                    + str(RecordId)
                                    + "' AND ERRORMESSAGE_RECORD_ID = '"
                                    + str(ErrorMessageObj.RECORD_ID)
                                    + "'"
                                )
                            DeleteErr = DeleteErr.replace("'", "''")
                            self.Sql.RunQuery(str(DeleteErr))
                            FORMULA = str(ErrorMessageObj.CCL)
                            FORMULA = FORMULA.replace("{" + ApiName + "}", RecordId)
                            Trace.Write("SYELOG : FORMULA : " + str(FORMULA))
                            if FORMULA is not None and FORMULA != "":
                                FORMULA_RESULT = SqlHelper.GetFirst(str(FORMULA))
                                Trace.Write("SYELOG : FORMULA RESULT :" + str(FORMULA_RESULT.MESSAGE))
                                if FORMULA_RESULT is not None:
                                    if str(FORMULA_RESULT.MESSAGE).upper() == "TRUE":
                                        import datetime

                                        datetime_value = datetime.datetime.now()
                                        Get_UserID = ScriptExecutor.ExecuteGlobal("SYUSDETAIL", "USERID")
                                        Trace.Write("Get_UserIDGet_UserIDGet_UserID" + str(Get_UserID))
                                        ErrTable = SqlHelper.GetTable("SYELOG")
                                        newrow = {}
                                        newrow["ERROR_LOGS_RECORD_ID"] = str(Guid.NewGuid()).upper()
                                        newrow["ERRORMESSAGE_RECORD_ID"] = str(ErrorMessageObj.RECORD_ID)
                                        newrow["OBJECT_RECORD_ID"] = str(ErrorMessageObj.TAB_RECORD_ID)
                                        newrow["OBJECT_NAME"] = str(tablename)
                                        newrow["ACTIVE"] = "1"
                                        newrow["ERRORMESSAGE_DESCRIPTION"] = str(ErrorMessageObj.MESSAGE_TEXT)
                                        newrow["OBJECT_TYPE"] = str(ErrorMessageObj.MESSAGE_TYPE)
                                        newrow["OBJECT_VALUE_REC_ID"] = str(RecordId)
                                        newrow["ERRORMESSAGE_ID"] = str(ErrorMessageObj.MESSAGE_CODE)
                                        newrow["CPQTABLEENTRYADDEDBY"] = str(Get_UserID)
                                        newrow["CPQTABLEENTRYDATEADDED"] = datetime_value
                                        newrow["CpqTableEntryModifiedBy"] = str(Get_UserID)
                                        newrow["CpqTableEntryDateModified"] = datetime_value
                                        newrow["ADDUSR_RECORD_ID"] = str(Get_UserID)
                                        Trace.Write("SYELOG : NEW ROW : " + str(newrow))
                                        ErrTable.AddRow(newrow)
                                        SqlHelper.Upsert(ErrTable)

        except:
            Trace.Write("SYELOG : EXCEPTION")
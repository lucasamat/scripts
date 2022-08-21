# ====================================================================================================
#   __script_name : SYDATABASE.PY
#   __script_description : This script is used to do the database operations in CPQ Custom Tables
#   __primary_author__ : JOE EBENEZER 
#   __create_date : 12/11/2019
#   © BOSTON HARBOR CONSULTING INC - ALL RIGHTS RESERVED
# ====================================================================================================

import datetime
#import Webcom.Configurator.Scripting.Test.TestProduct

class SQL:
    """Model to handle custom table transactions."""

    def __init__(self):
        """Initialize variables."""
        self.name = "SQL"
        self.is_user_have_needed_permission_to_tables = False
        self.enforceObjectPermissions = False
        self.enforceColumnPermissions = False
        self.logErrorMessages = True
        self.exceptMessage = ""

    def GetList(self, query):
        """
        Run query and return SqlHelper.GetList with the results.

        Param : query: string : sql query to be executed.
        """
        try:
            Trace.Write("SYDATABASE : GetList : RUNNING QUERY : " + query)
            return SqlHelper.GetList(query)
        except Exception, e:
            self.exceptMessage = (
                "SYDATABASE : GetList : EXCEPTION : UNABLE TO GET LIST : " + query + " : EXCEPTION E : " + str(e)
            )
            Trace.Write(self.exceptMessage)
            return None

    def GetFirst(self, query):
        """
        Run query and return SqlHelper.GetFirst with the results.

        Param : query : string : sql query to be executed.
        """
        try:
            Trace.Write("SYDATABASE : GetFirst : RUNNING QUERY : " + query)
            return SqlHelper.GetFirst(query)
        except Exception, e:
            self.exceptMessage = (
                "SYDATABASE : GetFirst : EXCEPTION : UNABLE TO GET FIRST : " + query + " : EXCEPTION E : " + str(e)
            )
            Trace.Write(self.exceptMessage)
            return None

    def GetTable(self, tableName):
        """
        Get the table information and return SqlHelper.GetTable Info.

        Param : tableName : string: Name of the table.
        """
        try:
            return SqlHelper.GetTable(tableName)
        except Exception, e:
            self.exceptMessage = (
                "SYDATABASE : GetTable : EXCEPTION : UNABLE TO GET TABLE : " + str(tableName) + " : EXCEPTION E : " + str(e)
            )
            Trace.Write(self.exceptMessage)
            return None

    def Upsert(self, tableInfo):
        """
        To Add/Insert records in a custom table.

        Param : tableInfo: string : ITableInfo :
        TableInfo which includes list of TableDataRows to upsert.
        """
        tableName = tableInfo.TableName
        rowCount = tableInfo.TableDataRows.Count
        for rows in range(rowCount):
            row = {}
            row = dict(tableInfo.TableDataRows.Item[rows].Values)
            row.pop("CPQTABLEENTRYADDEDBY", None)
            row.pop("CPQTABLEENTRYDATEADDED", None)
            row.pop("CpqTableEntryModifiedBy", None)
            row.pop("CpqTableEntryDateModified", None)
            row.pop("ADDUSR_RECORD_ID", None)
            if tableInfo.TableDataRows.Item[rows].CpqTableEntryId == 0:
                row["CPQTABLEENTRYADDEDBY"] = ScriptExecutor.ExecuteGlobal("SYUSDETAIL", "USERNAME")
                row["CPQTABLEENTRYDATEADDED"] = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p")
                row["CpqTableEntryModifiedBy"] = ScriptExecutor.ExecuteGlobal("SYUSDETAIL", "USERID")
                row["CpqTableEntryDateModified"] = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p")
                #row["ADDUSR_RECORD_ID"] = ScriptExecutor.ExecuteGlobal("SYGETUSDID")
                row["ADDUSR_RECORD_ID"] = ScriptExecutor.ExecuteGlobal("SYUSDETAIL", "USERID")
            else:
                row["CpqTableEntryId"] = tableInfo.TableDataRows.Item[rows].CpqTableEntryId
                row["CpqTableEntryModifiedBy"] = ScriptExecutor.ExecuteGlobal("SYUSDETAIL", "USERID")
                row["CpqTableEntryDateModified"] = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p")
            newTableInfo = ""
            newTableInfo = SqlHelper.GetTable(tableName)
            if tableName == 'SYVABL':
                row["VARIABLE_NAME"] = row["VARIABLE_NAME"].upper()
            if tableName == 'SACONT':
                row.pop("ADDUSR_RECORD_ID", None)
                row.pop("CPQTABLEENTRYADDEDBY", None)
            # Trace.Write(str(tableName)+"---tableName---TRACE_TESTZ--102----" + str(row))
            newTableInfo.AddRow(row)
            sqlInfo = SqlHelper.Upsert(newTableInfo)
            # Syelog.errorMessageEntry(newTableInfo)
            if sqlInfo.Success:
                continue
            else:
                self.exceptMessage = (
                    "SYDATABASE : Upsert : EXCEPTION : UNABLE TO DO SQL UPSERT : "
                    + str(newTableInfo.TableName)
                    + str(sqlInfo.Message)
                )
                Trace.Write(self.exceptMessage)
                return None
            return True

    def Delete(self, tableInfo):
        """
        To Delete records in a custom table.

        Param : tableInfo : ITableInfo which includes list of TableDataRows to Delete
        """
        try:
            return SqlHelper.Delete(tableInfo)
        except Exception, e:
            self.exceptMessage = (
                "SYDATABASE : Delete : EXCEPTION : UNABLE TO DELETE : "
                + str(tableInfo.TableName)
                + " : EXCEPTION E : "
                + str(e)
            )
            Trace.Write(self.exceptMessage)
            return None

    def RunQuery(self, query):
        """
        To Execute a SQL Query.

        Param : query : string : Query to be executed
        """
        QueryStatement = str(query)
        QueryStatement = QueryStatement.replace("'", "''")
        try:
            Trace.Write("SYDATABASE : RunQuery : RUNNING QUERY : " + query)
            query_result = SqlHelper.GetFirst("sp_executesql @statement = N'" + str(QueryStatement) + "'")
            return query_result
        except Exception, e:
            self.exceptMessage = (
                "SYDATABASE : RunQuery : EXCEPTION : UNABLE TO RUNQUERY : " + str(query) + " : EXCEPTION E : " + str(e)
            )
            Trace.Write(self.exceptMessage)
            return None
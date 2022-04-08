"""This script is used to do the CRUD operations in CPQ Custom Tables."""
# ====================================================================================================
#   __script_name : SYDATABASE.PY
#   __script_description : This script is used to do the database operations in CPQ Custom Tables
#   __primary_author__ : JOE EBENEZER
#   __maintainer__ : __Deesh__
#   __create_date : 12/11/2019
#   __edited_date__: 08/04/2022
#   © BOSTON HARBOR CONSULTING INC - ALL RIGHTS RESERVED
# ====================================================================================================

import datetime


class Sql:
    """Model to handle custom table transactions.
    :cause:
        Writing this as a class method as we all the functions are independent of one another
        so no need to create a new instance.
    :ref:
        >> https://iscinumpy.gitlab.io/post/factory-classmethods-in-python/
    """

    name = "SQL"
    is_user_have_needed_permission_to_tables = False
    enforceObjectPermissions = False
    enforceColumnPermissions = False
    logErrorMessages = True
    exceptMessage = ""

    @classmethod
    def GetList(cls, query):
        """
        Run query and return SqlHelper.GetList with the results.

        Param : query: string : sql query to be executed.
        """
        try:
            Trace.Write("SYDATABASE : GetList : RUNNING QUERY : {}".format(query))
            return SqlHelper.GetList(query)
        except Exception as e:
            cls.exceptMessage = "SYDATABASE : GetList : EXCEPTION : UNABLE TO GET LIST : {} : EXCEPTION E : {}".format(query, e)
            Trace.Write(cls.exceptMessage)
            return None

    @classmethod
    def GetFirst(cls, query):
        """
        Run query and return SqlHelper.GetFirst with the results.

        Param : query : string : sql query to be executed.
        """
        try:
            Trace.Write("SYDATABASE : GetFirst : RUNNING QUERY : {}".format(query))
            return SqlHelper.GetFirst(query)
        except Exception as e:
            cls.exceptMessage = "SYDATABASE : GetFirst : EXCEPTION : UNABLE TO GET FIRST : {} : EXCEPTION E : {}".format(query, e)
            Trace.Write(cls.exceptMessage)
            return None

    @classmethod
    def GetTable(cls, tableName):
        """
        Get the table information and return SqlHelper.GetTable Info.

        Param : tableName : string: Name of the table.
        """
        try:
            return SqlHelper.GetTable(tableName)
        except Exception as e:
            cls.exceptMessage = "SYDATABASE : GetTable : EXCEPTION : UNABLE TO GET TABLE : {} : EXCEPTION E : {}".format(tableName, e)
            Trace.Write(cls.exceptMessage)
            return None

    @classmethod
    def Upsert(cls, tableInfo):
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

            if not tableInfo.TableDataRows.Item[rows].CpqTableEntryId:
                row.update(
                    {
                        "CPQTABLEENTRYADDEDBY": ScriptExecutor.ExecuteGlobal("SYUSDETAIL", "USERNAME"),
                        "CPQTABLEENTRYDATEADDED": datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"),
                        "CpqTableEntryModifiedBy": ScriptExecutor.ExecuteGlobal("SYUSDETAIL", "USERID"),
                        "CpqTableEntryDateModified": datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"),
                        "ADDUSR_RECORD_ID": ScriptExecutor.ExecuteGlobal("SYUSDETAIL", "USERID"),
                    }
                )
            else:
                row.update(
                    {
                        "CpqTableEntryId": tableInfo.TableDataRows.Item[rows].CpqTableEntryId,
                        "CpqTableEntryModifiedBy": ScriptExecutor.ExecuteGlobal("SYUSDETAIL", "USERID"),
                        "CpqTableEntryDateModified": datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"),
                    }
                )

            newTableInfo = SqlHelper.GetTable(tableName)
            if tableName == "SYVABL":
                row["VARIABLE_NAME"] = row["VARIABLE_NAME"].upper()
            if tableName == "SACONT":
                row.pop("ADDUSR_RECORD_ID", None)
                row.pop("CPQTABLEENTRYADDEDBY", None)

            Trace.Write("{} ---tableName---TRACE_TESTZ--102---- {}".format(tableName, row))
            newTableInfo.AddRow(row)
            sqlInfo = SqlHelper.Upsert(newTableInfo)
            if sqlInfo.Success:
                continue
            else:
                cls.exceptMessage = "SYDATABASE : Upsert : EXCEPTION : UNABLE TO DO SQL UPSERT : {} :: {}".format(
                    newTableInfo.TableName, sqlInfo.Message
                )
                Trace.Write(cls.exceptMessage)
                return None
        return True

    @classmethod
    def Delete(cls, tableInfo):
        """
        To Delete records in a custom table.

        Param : tableInfo : ITableInfo which includes list of TableDataRows to Delete
        """
        try:
            return SqlHelper.Delete(tableInfo)
        except Exception as e:
            cls.exceptMessage = "SYDATABASE : Delete : EXCEPTION : UNABLE TO DELETE : {} : EXCEPTION E : {}".format(tableInfo.TableName, e)
            Trace.Write(cls.exceptMessage)
            return None

    @classmethod
    def RunQuery(cls, query):
        """
        To Execute a SQL Query.
        Param : query : string : Query to be executed
        """
        QueryStatement = str(query).replace("'", "''")
        try:
            Trace.Write("SYDATABASE : RunQuery : RUNNING QUERY : {}".format(query))
            query_result = SqlHelper.GetFirst("sp_executesql @statement = N'{}'".format(QueryStatement))
            return query_result
        except Exception as e:
            cls.exceptMessage = "SYDATABASE : RunQuery : EXCEPTION : UNABLE TO RUNQUERY : {} : EXCEPTION E : {}".format(query, e)
            Trace.Write(cls.exceptMessage)
            return None


class SQL(Sql):
    pass


# ---------------------- public api to be imported into required place----------------------------------------#
# -----------------------------no need to import unnecessary methods-----------------------------------------#


def sql_get_list(query):
    """This function is the public api to access the sql get list method"""
    return Sql.GetList(query)


def sql_get_table(table_name):
    """This function is the public api to access the sql GetTable method"""
    return Sql.GetTable(table_name)


def sql_get_first(cls, query):
    """This function is the public api to access the sql GetFirst method"""
    return Sql.GetFirst(query)


def sql_upsert(cls, tableInfo):
    """This function is the public api to access the sql Upsert method"""
    return Sql.Upsert(tableInfo)


def sql_delete(cls, tableInfo):
    """This function is the public api to access the sql Delete method"""
    return Sql.Delete(tableInfo)


def sql_run_query(cls, query):
    """This function is the public api to access the sql RunQuery method"""
    return Sql.RunQuery(query)


# ----------------------------------------- end of public methods------------------------------------------------#

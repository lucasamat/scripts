# ====================================================================================================
#   __script_name : SYTABACTIN.PY
#   __script_description : This script is used to do get the GitHub Source Code
#   __primary_author__ : 
#   __create_date : 
#   Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ====================================================================================================
ScriptExecutor = ScriptExecutor  # pylint: disable=E0602
Trace = Trace  # pylint: disable=E0602
Log = Log  # pylint: disable=E0602
SqlHelper = SqlHelper  # pylint: disable=E0602
# pylint: disable = import-error
import Webcom.Configurator.Scripting.Test.TestProduct
import datetime
from SYDATABASE import SQL


class TableAction:

    """Model to handle Audit Information Columns in Custom Tables"""

    def __init__(self):
        self.sql = SQL()

    def Create(self, table_name, row):
        """
        Insert Row into Custom Tables with Audit Information
        Param : table_name : string : Name of the Table
        Param : row : row : Row to be Added
        """
        tableInfo = self.sql.GetTable(table_name)
        """datetime_value = datetime.datetime.now()
        Get_UserID = ScriptExecutor.ExecuteGlobal("SYUSDETAIL", "USERID")
        try:
            row.pop("CPQTABLEENTRYADDEDBY")
            row.pop("CPQTABLEENTRYDATEADDED")
            row.pop("CpqTableEntryModifiedBy")
            row.pop("CpqTableEntryDateModified")
        except:
            Trace.Write("EXCEPTION : NOTHING TO POP")
        row["CPQTABLEENTRYADDEDBY"] = ScriptExecutor.ExecuteGlobal("SYUSDETAIL", "USERNAME")
        row["CPQTABLEENTRYDATEADDED"] = datetime_value
        row["CpqTableEntryModifiedBy"] = str(Get_UserID)
        row["CpqTableEntryDateModified"] = datetime_value"""
        #Trace.Write("TRACE_TESTZ----45---" + str(row))
        tableInfo.AddRow(row)
        self.sql.Upsert(tableInfo)

    def Delete(self, table_name, primary, row):
        """
        Delete Row from Custom Tables with Audit Information
        Param : table_name : string : Name of the Table
        Param : primary : string : Condition
        Param : row : row : Row to be Deleted
        """
        tableInfo = self.sql.GetTable(table_name)
        primaryQueryItems = self.sql.GetList(
            "SELECT * FROM " + str(table_name) + " WHERE " + primary + " = '" + str(row) + "'"
        )
        if primaryQueryItems is not None:
            for primaryItem in primaryQueryItems:
                tableInfo.AddRow(primaryItem)
                self.sql.Delete(tableInfo)

    def Update(self, table_name, primary, row):
        """
        Update Row in Custom Tables with Audit Information
        Param : table_name : string : Name of the Table
        Param : primary : string : Condition
        Param : row : row : Row to be Updated
        """
        tableInfo = self.sql.GetTable(table_name)
        primary_val = row.get(primary)
        #Trace.Write('93----table_name------'+str(table_name))
        if str(table_name) != "cpq_permissions":
            primaryQueryItems = self.sql.GetFirst(
                "SELECT * FROM " + str(table_name) + " WHERE " + primary + " = '" + str(primary_val) + "'"
            )
            
            if primaryQueryItems is not None:
                try:
                    row.pop("CPQTABLEENTRYADDEDBY")
                    row.pop("CPQTABLEENTRYDATEADDED")
                    row.pop("CpqTableEntryModifiedBy")
                    row.pop("CpqTableEntryDateModified")
                except:
                    Trace.Write("EXCEPTION : NOTING TO POP")
                row["CpqTableEntryModifiedBy"] = ScriptExecutor.ExecuteGlobal("SYUSDETAIL", "USERID")
                row["CpqTableEntryDateModified"] = datetime.datetime.now()
                row["CpqTableEntryId"] = primaryQueryItems.CpqTableEntryId                
                tableInfo.AddRow(row)
                self.sql.Upsert(tableInfo)
        else:
            Trace.Write('93------')

TableActions = TableAction()
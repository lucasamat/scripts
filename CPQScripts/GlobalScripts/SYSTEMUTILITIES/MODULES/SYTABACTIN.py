# ====================================================================================================
#   __script_name : SYTABACTIN.PY
#   __script_description : This script is used to do get the GitHub Source Code
#   __primary_author__ :
#   __create_date :
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ====================================================================================================
import datetime
from SYDATABASE import sql_get_first, sql_get_table, sql_upsert, sql_get_list, sql_delete


class TableAction:
    """Model to handle Audit Information Columns in Custom Tables"""

    @staticmethod
    def Create(table_name, row):
        """
        Insert Row into Custom Tables with Audit Information
        Param : table_name : string : Name of the Table
        Param : row : row : Row to be Added
        """
        table_info = sql_get_table(table_name)
        # Don't remove
        # datetime_value = datetime.datetime.now()
        # Get_UserID = ScriptExecutor.ExecuteGlobal("SYUSDETAIL", "USERID")
        # row.pop("CPQTABLEENTRYADDEDBY",None)
        # row.pop("CPQTABLEENTRYDATEADDED",None)
        # row.pop("CpqTableEntryModifiedBy",None)
        # row.pop("CpqTableEntryDateModified",None)
        # row["CPQTABLEENTRYADDEDBY"] = ScriptExecutor.ExecuteGlobal("SYUSDETAIL", "USERNAME")
        # row["CPQTABLEENTRYDATEADDED"] = datetime_value
        # row["CpqTableEntryModifiedBy"] = str(Get_UserID)
        # row["CpqTableEntryDateModified"] = datetime_value  
        table_info.AddRow(row)
        sql_upsert(table_info)

    @staticmethod
    def Delete(table_name, primary, row):
        """
        Delete Row from Custom Tables with Audit Information
        Param : table_name : string : Name of the Table
        Param : primary : string : Condition
        Param : row : row : Row to be Deleted
        """
        table_info = sql_get_table(table_name)
        primary_query_items = sql_get_list("SELECT * FROM {} WHERE {} = '{}'".format(table_name, primary, row))
        if primary_query_items:
            for primaryItem in primary_query_items:
                table_info.AddRow(primaryItem)
                sql_delete(table_info)

    @staticmethod
    def Update(table_name, primary, row):
        """
        Update Row in Custom Tables with Audit Information
        Param : table_name : string : Name of the Table
        Param : primary : string : Condition
        Param : row : row : Row to be Updated
        """
        table_info = sql_get_table(table_name)
        primary_val = row.get(primary)
        if table_name != "cpq_permissions":
            primary_query_items = sql_get_first(
                "SELECT * FROM {} WHERE {} = '{}'".format(table_name, primary, primary_val)
            )
            if primary_query_items:
                row.pop("CPQTABLEENTRYADDEDBY", None)
                row.pop("CPQTABLEENTRYDATEADDED", None)
                row.pop("CpqTableEntryModifiedBy", None)
                row.pop("CpqTableEntryDateModified", None)

                row.update(
                    {
                        "CpqTableEntryModifiedBy": ScriptExecutor.ExecuteGlobal("SYUSDETAIL", "USERID"),
                        "CpqTableEntryDateModified": datetime.datetime.now(),
                        "CpqTableEntryId": primary_query_items.CpqTableEntryId,
                    }
                )
                table_info.AddRow(row)
                sql_upsert(table_info)


TableActions = TableAction()

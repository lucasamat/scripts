# =======================================================================================================================================
#   __script_name : SYALCONTDL.PY
#   __script_description : THIS SCRIPT IS USED TO DELETE RECORDS FROM A LIST GRID OR CONTAINER FOR ALL OBJECTS
#   __primary_author__ : JOE EBENEZER
#   __create_date : 26/08/2020
#   Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# =======================================================================================================================================
Trace = Trace  # pylint: disable=E0602
Log = Log  # pylint: disable=E0602
Product = Product  # pylint: disable=E0602
WebRequest = WebRequest  # pylint: disable=E0602
Param = Param  # pylint: disable=E0602
ApiResponseFactory = ApiResponseFactory  # pylint: disable=E0602
ScriptExecutor = ScriptExecutor  # pylint: disable=E0602
# pylint: disable = import-error
import Webcom.Configurator.Scripting.Test.TestProduct
import SYCNGEGUID as CPQID
from SYDATABASE import SQL
import clr
from System.Net import *
from System.Net import WebRequest
from System.Net import HttpWebResponse
from System.Text import Encoding
from System.Net import CookieContainer
from System.Net import Cookie

Sql = SQL()

clr.AddReference("System.Net")
clr.AddReference("IronPython")
clr.AddReference("Microsoft.Scripting")

def Condata(ID, tab):
    count = 0
    length = ""
    flag = 0
    data = ""
    # to get table name
    TABLEOBJ = Sql.GetFirst("select PRIMARY_OBJECT_NAME from SYSECT where TAB_NAME = '" + str(tab) + "'")
    if TABLEOBJ is not None:
        TableName = str(TABLEOBJ.PRIMARY_OBJECT_NAME).strip()
        tableInfo = Sql.GetTable(TableName)
        ColumnName = Sql.GetFirst(
            "select API_NAME from  SYOBJD where OBJECT_NAME ='" + str(TableName) + "' and DATA_TYPE ='AUTO NUMBER'"
        )
        sqlobjs = Sql.GetList(
            "select OBJECT_NAME,API_NAME from  SYOBJD where LOOKUP_OBJECT ='" + str(TableName) + "' and DATA_TYPE ='LOOKUP'"
        )

        for sqlobj in sqlobjs:
            # to delete the table
            if sqlobj is not None:
                sqlobj1 = Sql.GetFirst(
                    "select "
                    + str(sqlobj.API_NAME)
                    + " from "
                    + str(sqlobj.OBJECT_NAME)
                    + " where "
                    + str(sqlobj.API_NAME)
                    + " ='"
                    + str(ID)
                    + "'"
                )
                if sqlobj1 is None:
                    flag = 0
                else:
                    flag = 1
            if flag == 1:
                data = "TRUE"
                break
        if flag == 0:
            GetQuery = Sql.GetList(
                "select CpqTableEntryId from "
                + str(TableName)
                + " where "
                + str(ColumnName.API_NAME)
                + "='"
                + str(ID)
                + "'"
            )
            Trace.Write(
                "select CpqTableEntryId from "
                + str(TableName)
                + " where "
                + str(ColumnName.API_NAME)
                + "='"
                + str(ID)
                + "'"
            )
            if GetQuery is not None:
                for tablerow in GetQuery:
                    tableInfo.AddRow(tablerow)
                    Sql.Delete(tableInfo)
            Container = ""
            Con_Col_Name = "RECORD_ID"
            
            for tab in Product.Tabs:
                if tab.IsSelected == True:
                    currenttab = tab.Name
                    sql_obj = Sql.GetList(
                        "SELECT PRIMARY_OBJECT_RECORD_ID,PRIMARY_OBJECT_NAME FROM SYSECT WHERE TAB_NAME='"
                        + str(currenttab)
                        + "' "
                    )
                    if sql_obj is not None:
                        for sql in sql_obj:
                            data_obj = Sql.GetList(
                                "SELECT CONTAINER_NAME FROM SYOBJS WHERE NAME='Tab list' AND OBJ_REC_ID = '"
                                + str(sql.PRIMARY_OBJECT_RECORD_ID)
                                + "'"
                            )
                            if data_obj is not None:
                                for data in data_obj:
                                    Container = "LIST_" + str(data.CONTAINER_NAME).strip()

            if Container != "":
                
                ReqContainer = Product.GetContainerByName(Container)
                DeleteRowList = []
                for row in ReqContainer.Rows:
                    if row[Con_Col_Name].strip() == ID:
                        DeleteRowList.append(row.RowIndex)
                DeleteRowList.reverse()
                for ind in DeleteRowList:
                    ReqContainer.DeleteRow(ind)
                ReqContainer.Calculate()
                for row in ReqContainer.Rows:
                    row.Calculate()
        ScriptExecutor.ExecuteGlobal("MATABACTVE")
    return str(data)


ID = str(Param.Record_Id).strip()
tab = str(Param.Tab_name).strip()

ApiResponse = ApiResponseFactory.JsonResponse(Condata(ID, tab))
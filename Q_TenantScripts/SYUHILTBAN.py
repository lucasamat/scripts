# =========================================================================================================================================
#   __script_name : SYUHILTBAN.PY
#   __script_description : THIS SCRIPT IS USED TO CONSTRUCT AND DISPLAY THE BANNER CONTENT AT THE TOP OF ALL THE PAGE
#   __primary_author__ :
#   __create_date :
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
from SYDATABASE import SQL
import Webcom.Configurator.Scripting.Test.TestProduct
Sql = SQL()


def BANNER_CONTENT():
    CurrentTabName = ""
    keyData_val = Param.keyData_val
    TestProduct = Webcom.Configurator.Scripting.Test.TestProduct()
    Product_name = Product.Name
    CurrentTabName = TestProduct.CurrentTab
    m = "select TAB_LABEL from SYTABS where SAPCPQ_ALTTAB_NAME = '" + str(CurrentTabName) + "'"
    sql_obj = Sql.GetFirst(m)
    makeInToStr = three_required_values = ""
    if sql_obj is not None:
        if CurrentTabName != "" and keyData_val != "":
            columnNames = Sql.GetFirst(
                "select REPLACE(REPLACE(COLUMNS,'[',''),']','') as COLMN,ms.PRIMARY_OBJECT_RECORD_ID AS PARID from SYSECT  ms with (nolock) JOIN SYOBJS mos with (nolock) ON ms.PRIMARY_OBJECT_RECORD_ID = mos.OBJ_REC_ID   INNER JOIN SYPAGE ON ms.PAGE_RECORD_ID = SYPAGE.RECORD_ID where TAB_NAME='"
                + str(sql_obj.TAB_LABEL)
                + "' AND SECTION_NAME='BASIC INFORMATION' AND mos.NAME='Header list '"
            )
            if columnNames:
                getClomunsInOrder = (columnNames.COLMN).split(",")
                tableHeader = []
                tableName = ""
                for j in getClomunsInOrder:
                    headerTextInOrder = Sql.GetFirst(
                        "SELECT FIELD_LABEL,OBJECT_NAME FROM  SYOBJD with (nolock) WHERE API_NAME IN ("
                        + str(j)
                        + ") AND PARENT_OBJECT_RECORD_ID ='"
                        + str(columnNames.PARID)
                        + "'"
                    )
                    tableName = headerTextInOrder.OBJECT_NAME
                    if tableName is not None:
                        tableHeader.append(headerTextInOrder.FIELD_LABEL)
                for i in tableHeader:
                    if makeInToStr:
                        makeInToStr = makeInToStr + "," + i
                    else:
                        makeInToStr = i
                replaceAndRemoveQuotes = (columnNames.COLMN).replace("'", "")
                getIdColumn = ""
                if replaceAndRemoveQuotes:
                    getIdColumn = replaceAndRemoveQuotes.split(",")[0]
                if getIdColumn != "" and keyData_val != "":
                    table_required_txt = (
                        "SELECT "
                        + str(replaceAndRemoveQuotes)
                        + " from "
                        + str(tableName)
                        + " with (nolock) where "
                        + str(getIdColumn)
                        + " = '"
                        + keyData_val
                        + "'"
                    )

                    three_required_values = Sql.GetFirst(table_required_txt)
        
    return makeInToStr, three_required_values


ApiResponse = ApiResponseFactory.JsonResponse(BANNER_CONTENT())
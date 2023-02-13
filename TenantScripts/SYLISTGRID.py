"""THIS SCRIPT IS USED TO LOAD THE LIST GRID/CONTAINER."""
import re
import SYCNGEGUID as keyid
from SYDATABASE import SQL
import Webcom.Configurator.Scripting.Test.TestProduct
# =========================================================================================
#   __script_name : SYMCTABSGD.PY
#   __script_description : THIS SCRIPT IS USED TO LOAD THE TAB CONTAINER DATA ACROSS ALL THE APPS
#   __primary_author__ : JOE EBENEZER
#   __create_date :
# =========================================================================================

Sql = SQL()
TestProduct = Webcom.Configurator.Scripting.Test.TestProduct()
tab_name = TestProduct.CurrentTab
userid = User.Id
#productName = Product.GetGlobal("Pricemodel")


def ListContainerShow(PerPage, PageInform, A_Keys, A_Values, SortColumn, SortColumnOrder):
    """List grid loader."""
    pass


try:
    PerPage = Param.PerPage
    PageInform = Param.PageInform
except Exception:
    PerPage = "20"
    PageInform = "1___20___20"

Trace.Write(str(Param.ACTION))

if Param.ACTION == "FIRST":
    PerPage = ""
    PageInform = ""
    A_Keys = ""
    A_Values = ""
    SortColumn = ""
    SortColumnOrder = ""
    ApiResponse = ApiResponseFactory.JsonResponse(
        ListContainerShow(PerPage, PageInform, A_Keys, A_Values, SortColumn, SortColumnOrder)
    )

elif Param.ACTION == "SECOND":
    PerPage = Param.PerPage
    PageInform = Param.PageInform
    A_Keys = Param.A_Keys
    A_Values = Param.A_Values
    SortColumn = Param.SortColumn
    SortColumnOrder = Param.SortColumnOrder
    ApiResponse = ApiResponseFactory.JsonResponse(
        ListContainerShow(PerPage, PageInform, A_Keys, A_Values, SortColumn, SortColumnOrder)
    )

elif Param.ACTION == "SORTING":
    SortColumn = Param.SortColumn
    SortColumnOrder = Param.SortColumnOrder
    A_Keys = Param.A_Keys
    A_Values = Param.A_Values
    ApiResponse = ApiResponseFactory.JsonResponse(
        ListContainerShow(PerPage, PageInform, A_Keys, A_Values, SortColumn, SortColumnOrder)
    )

elif Param.ACTION == "TABLESORTING":
    PerPage = Param.PerPage
    PageInform = Param.PageInform
    PageInform = "1___" + str(PerPage) + "___" + str(PerPage)
    A_Keys = Param.A_Keys
    A_Values = Param.A_Values
    SortColumn = Param.SortColumn
    SortColumnOrder = Param.SortColumnOrder
    ApiResponse = ApiResponseFactory.JsonResponse(
        ListContainerShow(PerPage, PageInform, A_Keys, A_Values, SortColumn, SortColumnOrder)
    )
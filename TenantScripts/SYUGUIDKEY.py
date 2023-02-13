# =========================================================================================================================================
#   __script_name : SYUGUIDKEY.PY
#   __script_description : THIS SCRIPT IS USED TO CONVERT THE RECORD ID TO GUID
#   __primary_author__ :
#   __create_date : 26/08/2020
# ==========================================================================================================================================
from SYDATABASE import SQL
import Webcom.Configurator.Scripting.Test.TestProduct
Sql = SQL()
import SYCNGEGUID as CPQ

ScriptExecutor = ScriptExecutor  # pylint: disable=E0602
Trace = Trace  # pylint: disable=E0602
Log = Log  # pylint: disable=E0602
Webcom = Webcom  # pylint: disable=E0602
Product = Product  # pylint: disable=E0602
ApiResponseFactory = ApiResponseFactory  # pylint: disable=E0602
TagParserProduct = TagParserProduct  # pylint: disable=E0602

TestProduct = Webcom.Configurator.Scripting.Test.TestProduct()
Product_name = Product.Name
current_tab = str(TestProduct.CurrentTab)


def CPQID():
    ATTR_NAME = ""
    CPQRecordID = ""
    CURRENT_MODULE_OBJ = Sql.GetFirst("SELECT * FROM SYAPPS (NOLOCK) WHERE APP_LABEL like '%" + str(Product_name) + "%' ")
    if CURRENT_MODULE_OBJ is not None:
        tab_obj = Sql.GetFirst(
            "SELECT * FROM SYTABS (NOLOCK) WHERE SAPCPQ_ALTTAB_NAME = '"
            + str(current_tab)
            + "' and APP_LABEL = '"
            + str(CURRENT_MODULE_OBJ.APP_LABEL)
            + "' "
        )
        if tab_obj is not None:
            section_obj = Sql.GetFirst(
                "SELECT SYSECT. * FROM SYSECT (NOLOCK) INNER JOIN SYPAGE (NOLOCK) ON SYPAGE.RECORD_ID = SYSECT.PAGE_RECORD_ID WHERE SYPAGE.TAB_RECORD_ID = '"
                + str(tab_obj.RECORD_ID)
                + "' and SYSECT.SECTION_NAME = 'BASIC INFORMATION' "
            )
            if section_obj is not None:
                SqlObj = Sql.GetFirst(
                    "SELECT OBJECT_NAME,RECORD_NAME FROM SYOBJH (NOLOCK) WHERE OBJECT_NAME = '"
                    + str(section_obj.PRIMARY_OBJECT_NAME.strip())
                    + "' "
                )
                if SqlObj is not None:
                    Table_Name = str(SqlObj.OBJECT_NAME)
                    QstnObj = Sql.GetFirst(
                        "SELECT RECORD_ID,FIELD_LABEL FROM SYSEFL WITH (NOLOCK) WHERE API_NAME = '"
                        + Table_Name
                        + "' and FIELD_LABEL = 'Key' and SECTION_RECORD_ID = '"
                        + str(section_obj.RECORD_ID)
                        + "' "
                    )
                    if QstnObj is not None:
                        QSTNRECORDID = str(QstnObj.RECORD_ID).replace("-", "_").replace(" ", "")
                        ATTR_NAME = "QSTN_" + str(QSTNRECORDID)
                        KeyValue = Product.Attributes.GetByName(str(ATTR_NAME)).GetValue()
                        CPQRecordID = CPQ.KeyCPQId.GetCPQId(str(Table_Name), str(KeyValue))
    return ATTR_NAME, CPQRecordID


ApiResponse = ApiResponseFactory.JsonResponse(CPQID())

TestProduct = Webcom.Configurator.Scripting.Test.TestProduct()
current_tab = str(TestProduct.CurrentTab)
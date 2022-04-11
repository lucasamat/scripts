# =========================================================================================================================================
#   __script_name : SYUGUIDKEY.PY
#   __script_description : THIS SCRIPT IS USED TO CONVERT THE RECORD ID TO GUID
#   __primary_author__ :
#   __create_date : 26/08/2020
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
from SYDATABASE import sql_get_first
import Webcom.Configurator.Scripting.Test.TestProduct

import SYCNGEGUID as CPQ

test_product = Webcom.Configurator.Scripting.Test.test_product()
product_name = Product.Name
current_tab = test_product.CurrentTab


def cpqid():
    attr_name = ""
    cpq_record_id = ""
    current_module_obj = sql_get_first("SELECT * FROM SYAPPS (NOLOCK) WHERE APP_LABEL like '%{}%' ".format(product_name))
    if current_module_obj:
        tab_obj = sql_get_first(
            "SELECT * FROM SYTABS (NOLOCK) WHERE SAPCPQ_ALTTAB_NAME = '{}' and APP_LABEL = '{}' ".format(
                current_tab, current_module_obj.APP_LABEL
            )
        )
        if tab_obj:
            section_obj = sql_get_first(
                """
                SELECT
                    SYSECT.*
                FROM
                    SYSECT (NOLOCK)
                    INNER JOIN SYPAGE (NOLOCK) ON SYPAGE.RECORD_ID = SYSECT.PAGE_RECORD_ID
                WHERE
                    SYPAGE.TAB_RECORD_ID = '{}'
                    and SYSECT.SECTION_NAME = 'BASIC INFORMATION'
                    """.format(
                    tab_obj.RECORD_ID
                )
            )
            if section_obj:
                sql_obj = sql_get_first(
                    "SELECT OBJECT_NAME,RECORD_NAME FROM SYOBJH (NOLOCK) WHERE OBJECT_NAME = '{}' ".format(
                        section_obj.PRIMARY_OBJECT_NAME.strip()
                    )
                )
                if sql_obj:
                    table_name = sql_obj.OBJECT_NAME
                    qstn_obj = sql_get_first(
                        ""
                        """
                        SELECT
                            RECORD_ID,
                            FIELD_LABEL
                        FROM
                            SYSEFL WITH (NOLOCK)
                        WHERE
                            API_NAME = '{}'
                            and FIELD_LABEL = 'Key'
                            and SECTION_RECORD_ID = '{}'
                        """.format(
                            table_name, section_obj.RECORD_ID
                        )
                    )
                    if qstn_obj:
                        qstnrecordid = str(qstn_obj.RECORD_ID).replace("-", "_").replace(" ", "")
                        attr_name = "QSTN_{}".format(qstnrecordid)
                        key_value = Product.Attributes.GetByName(attr_name).GetValue()
                        cpq_record_id = CPQ.KeyCPQId.GetCPQId(str(table_name), str(key_value))
    return attr_name, cpq_record_id


ApiResponse = ApiResponseFactory.JsonResponse(cpqid())

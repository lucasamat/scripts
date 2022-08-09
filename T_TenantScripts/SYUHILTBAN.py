# =========================================================================================================================================
#   __script_name : SYUHILTBAN.PY
#   __script_description : THIS SCRIPT IS USED TO CONSTRUCT AND DISPLAY THE BANNER CONTENT AT THE TOP OF ALL THE PAGE
#   __primary_author__ :
#   __create_date :
#   Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
from SYDATABASE import sql_get_first
import Webcom.Configurator.Scripting.Test.TestProduct


def banner_content():
    key_data_val = Param.keyData_val
    test_product = Webcom.Configurator.Scripting.Test.TestProduct()
    current_tab_name = test_product.CurrentTab
    sql_obj = sql_get_first("select TAB_LABEL from SYTABS where SAPCPQ_ALTTAB_NAME = '{}'".format(current_tab_name))
    make_in_to_str = three_required_values = ""
    if sql_obj:
        if current_tab_name and key_data_val:
            column_names = sql_get_first(
                """
                select
                    REPLACE(REPLACE(COLUMNS, '[', ''), ']', '') as COLMN,
                    ms.PRIMARY_OBJECT_RECORD_ID AS PARID
                from
                    SYSECT ms with (nolock)
                    JOIN SYOBJS mos with (nolock) ON ms.PRIMARY_OBJECT_RECORD_ID = mos.OBJ_REC_ID
                    INNER JOIN SYPAGE ON ms.PAGE_RECORD_ID = SYPAGE.RECORD_ID
                where
                    TAB_NAME = '{}'
                    AND SECTION_NAME = 'BASIC INFORMATION'
                    AND mos.NAME = 'Header list '
                """.format(
                    sql_obj.TAB_LABEL
                )
            )
            if column_names:
                get_clomuns_in_order = column_names.COLMN.split(",")
                table_header = []
                table_name = ""
                for j in get_clomuns_in_order:
                    header_text_in_order = sql_get_first(
                        """
                        SELECT
                            FIELD_LABEL,
                            OBJECT_NAME
                        FROM
                            SYOBJD with (nolock)
                        WHERE
                            API_NAME IN ({})
                            AND PARENT_OBJECT_RECORD_ID = '{}'
                        """.format(
                            j, column_names.PARID
                        )
                    )
                    table_name = header_text_in_order.OBJECT_NAME
                    if table_name:
                        table_header.append(header_text_in_order.FIELD_LABEL)
                for i in table_header:
                    make_in_to_str = "{},{}".format(make_in_to_str, i) if make_in_to_str else i

                replace_and_remove_quotes = column_names.COLMN.replace("'", "")
                get_id_column = ""
                if replace_and_remove_quotes:
                    get_id_column = replace_and_remove_quotes.split(",")[0]

                if get_id_column and key_data_val:
                    three_required_values = sql_get_first(
                        "SELECT {} from {} with (nolock) where {} = '{}'".format(
                            replace_and_remove_quotes, table_name, get_id_column, key_data_val
                        )
                    )

    return make_in_to_str, three_required_values


ApiResponse = ApiResponseFactory.JsonResponse(banner_content())

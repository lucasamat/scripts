# =========================================================================================================================================
#   __script_name : SYLTGDCRSB.PY
#   __script_description :
#   __primary_author__ : JOE EBENEZER
#   __create_date :
#   Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
from SYDATABASE import SQL
import Webcom.Configurator.Scripting.Test.TestProduct

Sql = SQL()


def ListGridCurrency():
    # Curr_tab_name = 'Pricebook Entries'
    currency_symbol = ""
    column_names_spl = []
    Curr_tab_name = Param.active_tab
    Trace.Write("Curr_tab_name...... " + Curr_tab_name)
    tab_name = "select PRIMARY_OBJECT_NAME from SYTABS where TAB_NAME ='" + str(Curr_tab_name) + "'"
    # Trace.Write('tab_name.sql.... '+tab_name)
    sql_tab_name = Sql.GetFirst(tab_name)
    # Trace.Write('tab_name.sql.... '+tab_name)
    list_grid_col_name = []
    if sql_tab_name:
        Cur_tab_id = sql_tab_name.PRIMARY_OBJECT_NAME
        #Trace.Write("tab_name........  " + sql_tab_name.PRIMARY_OBJECT_NAME)
        s_table = (
            "select s.COLUMNS,s.OBJ_REC_ID from SYOBJS s where s.NAME = 'Tab list' and s.CONTAINER_NAME='"
            + str(Cur_tab_id)
            + "'"
        )
        sql_s_table = Sql.GetFirst(s_table)
        # Trace.Write(sql_s_table.COLUMNS)
        # Trace.Write(sql_s_table.OBJ_REC_ID)
        if sql_s_table is not None:
            column_names = sql_s_table.COLUMNS
            Curr_tab_table = sql_s_table.OBJ_REC_ID
            column_names_spl = column_names.replace("[", "").replace("]", "").split(",")
        list_grid_col_api = []
        for i in column_names_spl:
            # Trace.Write(i)
            list_grid_col_api.append(i)
        # Trace.Write('fffffffffffffffffffff1111111111111111111')
        # Trace.Write(list_grid_col_api)
        sql_d_table = ""
        d_field_txt = ""
        d_currency_index = ""
        for j in list_grid_col_api:
            # Trace.Write(j)
            d_table_txt = (
                "select FIELD_LABEL,CURRENCY_INDEX from  SYOBJD where API_NAME = "
                + str(j)
                + " and (FORMULA_DATA_TYPE = 'CURRENCY' or DATA_TYPE = 'CURRENCY') and OBJECT_NAME='"
                + str(Cur_tab_id)
                + "'"
            )
            # Trace.Write('d_table_txt.....  '+d_table_txt)
            sql_d_table = Sql.GetFirst(d_table_txt)
            if sql_d_table:
                d_field_txt = sql_d_table.FIELD_LABEL
                # Trace.Write('d_field_txt....  '+d_field_txt)
                d_currency_index = sql_d_table.CURRENCY_INDEX
                # Trace.Write('d_currency_index....  '+d_currency_index)
                current_table = (
                    "select DISTINCT p.SYMBOL,p.CURRENCY from "
                    + str(Cur_tab_id)
                    + " c inner join PRCURR p on p.CURRENCY_RECORD_ID = c."
                    + str(d_currency_index)
                    + ""
                )
                # Trace.Write('current_table....  '+current_table)
                currency_symbol = Sql.GetList(current_table)
                for m in currency_symbol:
                    list_grid_col_name.append(d_field_txt + "|" + m.SYMBOL + "|" + m.CURRENCY)
                # if currency_symbol:
                # Trace.Write('CCCCUUUUURRRRR....  '+currency_symbol.CURRENCY)
                # list_grid_col_name.append(d_field_txt+'|'+currency_symbol.SYMBOL)
    return list_grid_col_name


ApiResponse = ApiResponseFactory.JsonResponse(ListGridCurrency())
# q = ListGridCurrency()
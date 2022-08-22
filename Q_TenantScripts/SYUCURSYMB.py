# =========================================================================================================================================
#   __script_name : SYUCURSYMB.PY
#   __script_description : THIS SCRIPT IS USED TO DISPLAY THE CURRENCY SYMBOL IN ALL CURRENCY FIELDS.
#   __primary_author__ : ASHA LYSANDAR
#   __create_date :
#   Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import SYCNGEGUID as CPQID
from SYDATABASE import SQL
import Webcom.Configurator.Scripting.Test.TestProduct

Sql = SQL()
TestProduct = Webcom.Configurator.Scripting.Test.TestProduct()


def get_obj_name(current_tab_name):
    CommonTreeParentParam = str(Product.GetGlobal("CommonTreeParentParam"))
    obj_name = ""  
    
    
    return obj_name


def build_query(column, obj_name, where_string):
    query_string = """
                    SELECT {Column_Name}
                    FROM {Table_Name} (NOLOCK)
                    WHERE {Where_String}
                    """.format(
        Column_Name=column, Table_Name=obj_name, Where_String=where_string
    )
    return query_string


def get_value_from_obj(record_obj, column):
    return getattr(record_obj, column, "")


def get_factor_symbol(obj_name):    
    factor_fields_list = []    
    factor_fields_obj = Sql.GetList(
        "SELECT FORMAT,FIELD_LABEL FROM  SYOBJD (NOLOCK) WHERE (FORMAT <> '' or FORMAT IS NOT NULL) AND OBJECT_NAME = '{}'".format(
            obj_name
        )
    )
    if factor_fields_obj is not None:
        for factor_field_obj in factor_fields_obj:
            if factor_field_obj.FORMAT:                
                symbol = "%" if Product.ParseString(factor_field_obj.FORMAT) == "PERCENT" else ""
                if symbol:
                    factor_fields_list.append(factor_field_obj.FIELD_LABEL + "|" + symbol)    
    return factor_fields_list


def get_currency_and_decimal_details(record_id):
    current_tab_name = TestProduct.CurrentTab
    decimal_list = []
    currency_symbol_list = []
    factor_fields_list = []
    objh_record_obj = Sql.GetFirst(
        """
                SELECT 
                    SYOBJH.OBJECT_NAME 
                FROM
                    SYTABS (NOLOCK) 
                INNER JOIN SYSECT (NOLOCK) ON SYSECT.TAB_NAME = SYTABS.TAB_NAME
                INNER JOIN SYOBJS (NOLOCK) ON SYOBJS.OBJ_REC_ID = SYSECT.PRIMARY_OBJECT_RECORD_ID
                INNER JOIN SYOBJH (NOLOCK) ON SYOBJH.RECORD_ID = SYOBJS.OBJ_REC_ID
                WHERE 
                    SYOBJS.NAME='Tab list' AND 
                    SYSECT.SECTION_NAME = 'BASIC INFORMATION' AND 
                    SYTABS.SAPCPQ_ALTTAB_NAME = '{}' """.format(
            current_tab_name
        )
    )
    if objh_record_obj is not None:
        current_obj_name = get_obj_name(current_tab_name)
        if not current_obj_name:
            current_obj_name = str(objh_record_obj.OBJECT_NAME)
            objd_records_obj = Sql.GetList(
                """
                SELECT 
                    CURRENCY_INDEX,FIELD_LABEL 
                FROM 
                    SYOBJD (NOLOCK) 
                WHERE 
                    (DATA_TYPE='CURRENCY' or FORMULA_DATA_TYPE='CURRENCY') AND ISNULL(CURRENCY_INDEX,'') != '' AND OBJECT_NAME = '{}'
                """.format(
                    current_obj_name
                )
            )
            if objd_records_obj is not None:
                for objd_record in objd_records_obj:
                    currency_index = str(objd_record.CURRENCY_INDEX)
                    where_string = ""                  
                    
                    where_string = "{Record_Column0} <> ''".format(Record_Column0=currency_index)

                    query_string = build_query(column=currency_index, obj_name=current_obj_name, where_string=where_string)

                    try:
                        record_obj = Sql.GetFirst(query_string)
                        if record_obj is not None:
                            currency = get_value_from_obj(record_obj, currency_index)
                            wh_string = ""                            
                            wh_string = "CURRENCY_RECORD_ID = '{}'".format(currency)
                            
                            q_string = build_query(
                                column="SYMBOL,CURRENCY,DISPLAY_DECIMAL_PLACES", obj_name="PRCURR", where_string=wh_string
                            )
                            currency_record_obj = Sql.GetFirst(q_string)
                            if currency_record_obj is not None:
                                decimal_list.append(currency_record_obj.DISPLAY_DECIMAL_PLACES)                                
                                currency_symbol_list.append(objd_record.FIELD_LABEL + "|" + currency_record_obj.CURRENCY)
                    except:
                        Trace.Write("Except Executed")
            factor_fields_list = get_factor_symbol(current_obj_name)
    return currency_symbol_list, decimal_list, factor_fields_list


record_id = Param.KeyToCurrency_value
ApiResponse = ApiResponseFactory.JsonResponse(get_currency_and_decimal_details(record_id))
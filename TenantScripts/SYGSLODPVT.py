# =========================================================================================================================================
#   __script_name : SYGSLODPVT.PY
#   __script_description : THIS SCRIPT IS USED TO LOAD A PIVOT TABLE.
#   __primary_author__ : JOE EBENEZER
#   __create_date :
# ==========================================================================================================================================
import re
import Webcom.Configurator.Scripting.Test.TestProduct
import SYTABACTIN as Table
from SYDATABASE import SQL
Sql = SQL()

def PivotAttr():

    table_id = "pivot_attr_table"
    data_list = []
    DropDownList = []
    filter_level_list = []
    filter_clas_name = ""
    cv_list = []
    filter_control_function = ""
    values_list = ""
    Columns = ["ATTRIBUTE_NAME", "VALUES", "ATTRIBUTE_RECORD_ID"]
    Column = [
        "mt.ATTRIBUTE_NAME",
        "ma.ATTVAL_DISPLAYVAL",
        "mt.ATTRIBUTE_RECORD_ID",
    ]

    table_header = (
        '<table id="'
        + str(table_id)
        + '"  data-pagination="true" data-filter-control="true" data-search-on-enter-key="true" data-pagination-loop = "false" data-locale = "en-US" data-page-list="[10, 20, 50, 100, ALL]" data-page-size="10" ><thead><tr><th data-field="ACTIONS"><div class="action_col">ACTIONS</div><button class="searched_button" id="Act_'
        + str(table_id)
        + '">Search</button></th>'
    )

    for inv in Columns:
        if str(inv) == "ATTRIBUTE_NAME" or str(inv) == "ATTRIBUTE_TYPE":
            insss = inv.replace("_", " ")
        else:
            insss = inv
        table_header += (
            '<th data-field="'
            + str(inv)
            + '" data-filter-control="input" data-sortable="true"><abbr title="'
            + str(inv)
            + '">'
            + str(insss)
            + "</abbr></th>"
        )
    table_header += "</tr>"
    table_header += (
        '</thead><tbody onclick="Table_Onclick_Scroll(this)"></tbody></table>'
    )

    for invs in list(Columns):
        table_ids = "#" + str(table_id)
        filter_clas = (
            "#" + str(table_id) + " .bootstrap-table-filter-control-" + str(invs)
        )
        values_list += "var " + str(invs) + ' = $("' + str(filter_clas) + '").val(); '
        values_list += (
            "ATTRIBUTE_VALUEList.push("
            + str(invs)
            + "); "
        )

    filter_class = "#Act_" + str(table_id)
    filter_control_function += (
        '$("'
        + filter_class
        + '").click( function(){ var table_id = $(this).closest("table").attr("id"); ATTRIBUTE_VALUEList = []; '
        + str(values_list)
        + ' var attribute_value = $(this).val(); cpq.server.executeScript("GS_LOADPIVOT", {"Preview":"true", "ATTRIBUTE_NAME": '
        + str(list(Column))
        + ', "ATTRIBUTE_VALUE": ATTRIBUTE_VALUEList, "ACTION" : "PRODUCT_ONLOAD_FILTER" }, function(data) { $("'
        + str(table_ids)
        + '").bootstrapTable("load", data ); }); });'
    )

    
    NORECORDS = ""
    if len(data_list) == 0:
        NORECORDS = "NORECORDS"

    RelatedDrop_str = (
        "try { if( document.getElementById('"
        + str(table_id)
        + "') ) { var listws = document.getElementById('"
        + str(table_id)
        + "').getElementsByClassName('filter-control');  for (i = 0; i < listws.length; i++) { document.getElementById('"
        + str(table_id)
        + "').getElementsByClassName('filter-control')[i].innerHTML = data5[i];  } for (j = 0; j < listws.length; j++) { if (data6[j] == 'select') { var dataAdapter = new $.jqx.dataAdapter(data7[j]); $('#"
        + str(table_id)
        + "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter, width: 200, autoDropDownHeight:'true',dropDownVerticalAlignment: 'bottom'}); } } } }  catch(err) { setTimeout(function() { var listws = document.getElementById('"
        + str(table_id)
        + "').getElementsByClassName('filter-control');  for (i = 0; i < listws.length; i++) { document.getElementById('"
        + str(table_id)
        + "').getElementsByClassName('filter-control')[i].innerHTML = data5[i];  } for (j = 0; j < listws.length; j++) { if (data6[j] == 'select') { var dataAdapter = new $.jqx.dataAdapter(data7[j]); $('#"
        + str(table_id)
        + "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter, width: 200, autoDropDownHeight:'true',dropDownVerticalAlignment: 'bottom'}); } } }, 5000); }"
    )

    
    return (
        table_header,
        data_list,
        table_id,
        filter_control_function,
        NORECORDS,
        cv_list,
        filter_level_list,
        DropDownList,
        RelatedDrop_str,
    )


def PivotAttrFilter(ATTRIBUTE_NAME, ATTRIBUTE_VALUE):
    
    ATTRIBUTE_VALUE_STR = ""
    data_list = []
    Dict_formation = dict(zip(ATTRIBUTE_NAME, ATTRIBUTE_VALUE))
    for quer_key, quer_value in enumerate(Dict_formation):
        if Dict_formation.get(quer_value) != "":
            if str(quer_value) == "ma.ATTVAL_DISPLAYVAL":
                quer_values = str(Dict_formation.get(quer_value)).strip()
                ATTRIBUTE_VALUE_STR += (
                    str(quer_value) + " = '" + str(quer_values) + "' and "
                )
            else:
                quer_values = str(Dict_formation.get(quer_value)).strip()
                
                quer_values = quer_values.split(",")
                if len(quer_values) == 1:
                    quer_values = "".join(str(e) for e in quer_values)
                    ATTRIBUTE_VALUE_STR += (
                        str(quer_value) + " = '" + str(quer_values) + "' and "
                    )
                else:
                    quer_values = str(tuple(list(quer_values)))
                    
                    ATTRIBUTE_VALUE_STR += (
                        str(quer_value) + " in " + str(quer_values) + " and "
                    )
    Trace.Write("ATTRIBUTE_VALUE_STR" + str(ATTRIBUTE_VALUE_STR))
    Trace.Write("data_list" + str(list(data_list)))

    return data_list


Preview = Param.Preview
ACTION = Param.ACTION
if ACTION == "PRODUCT_ONLOAD_FILTER":
    ATTRIBUTE_NAME = Param.ATTRIBUTE_NAME
    ATTRIBUTE_VALUE = Param.ATTRIBUTE_VALUE
    ApiResponse = ApiResponseFactory.JsonResponse(
        PivotAttrFilter(ATTRIBUTE_NAME, ATTRIBUTE_VALUE)
    )
else:
    ApiResponse = ApiResponseFactory.JsonResponse(PivotAttr())
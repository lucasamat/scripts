# =========================================================================================================================================
#   __script_name : SYPVTLOPOP.PY
#   __script_description :  THIS SCRIPT IS USED TO SHOW THE LOOKUP POPUP FROM THE PIVOT TABLE
#   __primary_author__ : JOE EBENEZER
#   __create_date :
#   Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import re
import Webcom.Configurator.Scripting.Test.TestProduct
from SYDATABASE import SQL

Sql = SQL()


def GSCONTLOOKUPPOPUP(TABLEID, OPER, ATTRVAL):
    DATA_OBJ = Sql.GetFirst(
        "SELECT COLUMNS FROM SYOBJS (NOLOCK) WHERE CONTAINER_NAME='" + str(TABLEID) + "' AND NAME='Lookup list'"
    )
    Header_Obj = Sql.GetFirst("SELECT LABEL FROM SYOBJH (NOLOCK) WHERE OBJECT_NAME='" + str(TABLEID) + "'")
    sec_str = ""
    filter_control_function = ""
    value_dict_list = []
    TABLEIDS = ""
    flag = 0
    idss = []
    oncli = "namePOPUPFormatterPivot"
    back_btn = "popup_cont_pivot_back()"
    val = ""
    sec_str += (
        '<div   class="row modulebnr brdr">'
        + str(eval("Header_Obj.LABEL")).upper()
        + " LOOKUP LIST"
        + '<button type="button"   class="close fltrt"  onclick="'
        + back_btn
        + '">X</button></div>'
    )
    sec_str += '<div class="col-md-12"><div class="row pad-10 bg-lt-wt brdr">'
    sec_str += (
        '<button type="button" class="btnconfig" id="'
        + str(OPER)
        + "|"
        + str(TABLEID)
        + '" onclick="'
        + back_btn
        + '">CANCEL</button>'
    )
    sec_str += "</div></div>"
    sec_str += '<div id="container" class="g4 pad-10 brdr except_sec">'
    # Trace.Write("DATA_OBJ--- "+str(DATA_OBJ.COLUMNS))
    if DATA_OBJ is not None:
        NAME = str(DATA_OBJ.COLUMNS[1:-1])
        END_OBJ = Sql.GetList(
            "SELECT top 1000 API_NAME,FIELD_LABEL FROM  SYOBJD (NOLOCK) WHERE OBJECT_NAME='"
            + str(TABLEID)
            + "' AND API_NAME in ("
            + NAME
            + ") order by abs(DISPLAY_ORDER)"
        )
        API_NAME_list = [ins.API_NAME for ins in END_OBJ]
        API_NAME_str = ",".join(API_NAME_list)
        FIELD_LABEL_list = [ins.FIELD_LABEL for ins in END_OBJ]
        LABEL_list = [{ins.FIELD_LABEL: ins.API_NAME} for ins in END_OBJ]
        FIELD_LABEL_str = ",".join(FIELD_LABEL_list)
        Trace.Write("SELECT top 1000 " + str(API_NAME_str) + " FROM " + str(TABLEID) + " ")
        VAL_Obj = Sql.GetList("SELECT top 1000 " + str(API_NAME_str) + " FROM " + str(TABLEID) + " ")
        if VAL_Obj is not None:
            ids = API_NAME_list[0]
            TABLEIDS = "table_" + TABLEID
            sec_str += (
                '<table id="'
                + str(TABLEIDS)
                + '" data-escape="true" data-search-on-enter-key="true" data-show-header="true" data-pagination="true" data-page-list="[5, 10, 20, 50, 100]"  data-page-size="5" data-filter-control="true"> <thead><tr>'
            )
            values_list = ""
            for invs in list(API_NAME_list[1:]):
                filter_clas = "#PIVOT_TABLE_ADD .bootstrap-table-filter-control-" + str(invs)
                values_list += "var " + str(invs) + ' = $("' + str(filter_clas) + '").val(); '
                values_list += "ATTRIBUTE_VALUEList.push(" + str(invs) + "); "
            for key, header in enumerate(FIELD_LABEL_list[1:]):
                api_name_dict_list = [dicts for dicts in LABEL_list if dicts.get(header)]
                api_name_header = ""
                if len(api_name_dict_list) > 0:
                    api_name_header = api_name_dict_list[0].get(str(header))
                    filter_class = "#PIVOT_TABLE_ADD .bootstrap-table-filter-control-" + str(api_name_header)
                    filter_control_function += (
                        '$("'
                        + filter_class
                        + '").change( function(){ var table_id = $(this).closest("table").attr("id"); var ATTRIBUTE_VALUEList = []; '
                        + str(values_list)
                        + ' var attribute_value = $(this).val(); cpq.server.executeScript("GS_PIVOT_LOOKUP_POPUP", {"TABLEID":"'
                        + str(TABLEID)
                        + '","OPER":"'
                        + str(OPER)
                        + '", "ATTRVAL":"'
                        + str(ATTRVAL)
                        + '", "ATTRIBUTE_NAME": '
                        + str(list(API_NAME_list[1:]))
                        + ', "ATTRIBUTE_VALUE": ATTRIBUTE_VALUEList, "GSCONTLOOKUP": "GSCONTLOOKUP" }, function(data) { $("#'
                        + str(TABLEIDS)
                        + '").bootstrapTable("load", data);  }); });'
                    )
                    if key == 0:
                        sec_str += (
                            '<th data-field="'
                            + str(api_name_header)
                            + '" data-sortable="true" data-pagination="true" data-formatter="'
                            + str(oncli)
                            + '"  data-filter-control="input">'
                            + str(header)
                            + "</th>"
                        )
                    else:
                        sec_str += (
                            '<th data-field="'
                            + str(api_name_header)
                            + '" data-sortable="true" data-filter-control="input">'
                            + str(header)
                            + "</th>"
                        )
            sec_str += "</tr></thead><tbody></tbody></table></div>"
            for obj_name in VAL_Obj:
                value_dict = {}

                objsk = "obj_name." + str(ids)
                idss = str(eval(objsk)) + "|" + str(ids)
                for tes in API_NAME_list[1:]:
                    value_dict["ids"] = idss
                    try:
                        tes = tes.decode("unicode_escape").encode("utf-8")
                        value_dict[tes] = str(eval("obj_name." + str(tes)).decode("unicode_escape").encode("utf-8"))
                        # Trace.Write("value_dict[tes]----"+str(value_dict[tes]))
                    except:
                        tes = tes.decode("unicode_escape").encode("utf-8")
                        value_dict[tes] = eval("obj_name." + str(tes)).decode("unicode_escape").encode("utf-8")
                        # Trace.Write("value_dict[tes]----"+str(value_dict[tes]))
                value_dict_list.append(value_dict)
        else:
            sec_str += '<div class="txt_center">No matching records found </div>'
    else:
        sec_str += '<div class="txt_center">No matching records found </div>'
    return sec_str, value_dict_list, TABLEIDS, filter_control_function


def GSCONTLOOKUPPOPUPFILTER(TABLEID, OPER, ATTRIBUTE_NAME, ATTRIBUTE_VALUE, ATTRVAL):
    sec_str = ""
    filter_control_function = ""
    ATTRIBUTE_VALUE_STR = ""
    REC_IDS = "table_" + str(TABLEID)
    TABLEID = str(TABLEID).strip()
    DATA_OBJ = Sql.GetFirst(
        "SELECT COLUMNS FROM SYOBJS (NOLOCK) WHERE CONTAINER_NAME='" + str(TABLEID) + "' AND NAME='Lookup list'"
    )
    Header_Obj = Sql.GetFirst("SELECT LABEL FROM SYOBJH (NOLOCK) WHERE OBJECT_NAME='" + str(TABLEID) + "'")
    if DATA_OBJ is not None:
        Colums_List = DATA_OBJ.COLUMNS
        OBJD_OBJ = Sql.GetList(
            "SELECT top 1000 API_NAME,FIELD_LABEL,DATA_TYPE FROM  SYOBJD (NOLOCK) WHERE OBJECT_NAME='" + str(TABLEID) + "'"
        )
        Colums_final_list1 = eval(Colums_List)
        Colums_final_list = eval(Colums_List)[1:]
        head_list = [{ins.API_NAME: ins.FIELD_LABEL} for ins in OBJD_OBJ]
        COLUMNS_NAME = ",".join(Colums_final_list1)
        Dict_formation = dict(zip(ATTRIBUTE_NAME, ATTRIBUTE_VALUE))
        ATTRIBUTE_VALUE_List = []
        for quer_key, quer_value in enumerate(Dict_formation):
            if Dict_formation.get(quer_value) != "":
                quer_values = str(Dict_formation.get(quer_value)).strip()
                ATTRIBUTE_VALUE_List.append(str(quer_value) + " like '%" + str(quer_values) + "%'")
        ATTRIBUTE_VALUE_STR = " AND ".join(ATTRIBUTE_VALUE_List)
        if ATTRIBUTE_VALUE_STR != "":
           Trace.Write("test")

        else:
            VAL_Obj = Sql.GetList("SELECT top 10 " + str(COLUMNS_NAME) + " FROM " + str(TABLEID) + "  ")
        table_list = []
        for val_api in VAL_Obj:
            data_dict = {}
            first_col = str(eval("val_api." + str(Colums_final_list1[0])))
            for Colums_final in Colums_final_list:
                data_dict["ids"] = first_col + "|" + str(Colums_final_list1[0])
                data_dict[str(Colums_final)] = eval("val_api." + str(Colums_final)).decode("unicode_escape").encode("utf-8")
            table_list.append(data_dict)
    return table_list


TABLEID = Param.TABLEID
OPER = Param.OPER
GSCONTLOOKUP = Param.GSCONTLOOKUP
ATTRVAL = Param.ATTRVAL
if GSCONTLOOKUP == "":
    ApiResponse = ApiResponseFactory.JsonResponse(GSCONTLOOKUPPOPUP(TABLEID, OPER, ATTRVAL))
elif GSCONTLOOKUP == "GSCONTLOOKUP":
    ATTRIBUTE_VALUE = Param.ATTRIBUTE_VALUE
    ATTRIBUTE_NAME = Param.ATTRIBUTE_NAME
    ApiResponse = ApiResponseFactory.JsonResponse(
        GSCONTLOOKUPPOPUPFILTER(TABLEID, OPER, ATTRIBUTE_NAME, ATTRIBUTE_VALUE, ATTRVAL)
    )
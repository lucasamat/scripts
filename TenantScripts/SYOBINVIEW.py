# ===================================================================================================
#   __script_name : SYOBINVIEW.PY
#   __script_description : This script is used to view and edit operations in object(index operation)
#   __primary_author__ : Dhurga Gopalakrishnan
#   __create_date : 16/04/2020
# ==================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct
import math
import SYCNGEGUID as CPQID
from SYDATABASE import SQL

Sql = SQL()


def obj_index_pop_up_expression(Primary_Data, RECORD_ID, ACTION):
    record_field = ""
    record_value = ""
    api_name = ""
    filter_control_function = ""
    api_value = ""
    var_str = ""
    date_field = []
    dbl_clk_function = ""
    D = {}
    new_value_dict = {}
    where_string = ""
    A_Keys = ""
    ObjectName = ""
    A_Values = ""
    if A_Keys != "" and A_Values != "":
        A_Keys = list(A_Keys)
        A_Values = list(A_Values)
        D = zip(A_Keys, A_Values)
        D = dict(D)

        for key, value in zip(A_Keys, A_Values):
            if value.strip():
                if where_string:
                    where_string += " AND "
                where_string += "{Key} LIKE '%{Value}%'".format(Key=key, Value=value)
    pagination_index_total_count = 0
    index_id = ""
    index_id = Primary_Data
    offset_skip_count = Offset_Skip_Count
    if offset_skip_count == 1:
        offset_skip_count = 0

    fetch_count = Fetch_Count

    # A043S001P01-10789 Start
    autoindex_queryName = ""
    autoindex_query = SqlHelper.GetFirst(
        "select FIELD_LABEL from SYOBJD (NOLOCK) where OBJECT_NAME ='" + str(index_id) + "' and DATA_TYPE = 'AUTO NUMBER'"
    )
    if autoindex_query:
        autoindex_queryName = autoindex_query.FIELD_LABEL

    lkpup_query = SqlHelper.GetList(
        "select FIELD_LABEL from SYOBJD (NOLOCK) where OBJECT_NAME ='" + str(index_id) + "' and DATA_TYPE = 'LOOKUP'"
    )
    lkpapi_name = []
    lkpapi_nameval = ""
    if lkpup_query is not None or lkpup_query != "":
        for val in lkpup_query:
            if val.FIELD_LABEL:
                lkpapi_name.append(val.FIELD_LABEL)
    lkpapi_nameval = str(lkpapi_name)[1:-2].replace("'", "")
    # A043S001P01-10789 End

    pagination_condition = "OFFSET {Offset_Skip_Count} ROWS FETCH NEXT {Fetch_Count} ROWS ONLY".format(
        Offset_Skip_Count=offset_skip_count, Fetch_Count=fetch_count
    )

    Pagination_index_M = Sql.GetFirst(
        "select count(FIELD_LABEL) as count from SYOBJD (NOLOCK) where OBJECT_NAME ='"
        + str(index_id)
        + "' and  FIELD_LABEL not in ('Added By','Added Date','Added By User Record Id','Last Modified By','Last Modified Date','"
        + str(autoindex_queryName)
        + "','"
        + str(lkpapi_nameval)
        + "')"
    )

    disable_next_and_last = ""
    disable_previous_and_first = ""

    if Pagination_index_M is not None:
        pagination_index_total_count = Pagination_index_M.count

    records_end = offset_skip_count + fetch_count - 1

    if pagination_index_total_count < records_end:
        records_end = pagination_index_total_count
    else:
        records_end = records_end
    if offset_skip_count == 0:
        offset_skip_count = 1
        records_end = fetch_count


    records_start_and_end = "{} - {} of ".format(offset_skip_count, records_end)
    disable_next_and_last = ""
    disable_previous_and_first = ""
    if records_end == pagination_index_total_count:
        disable_next_and_last = "class='btn-is-disabled'"
    if offset_skip_count == 0:
        disable_previous_and_first = "class='btn-is-disabled'"
    current_page = int(math.ceil(offset_skip_count / fetch_count)) + 1

    # current_page = ''
    ObjectName = "SYOBJX"
    table_id = "indexExpression_addnew"
    table_ids = "#" + str(table_id)
    Header_details = {
        "FIELD_LABEL": "Field Label",
    }
    ordered_keys = [
        "FIELD_LABEL",
    ]

    sec_str = '<div class="row modulebnr brdr ma_mar_btm">FIELD LABEL: LOOKUP<button type="button"  class="close flt_rt" onclick="closepopup_scrl()" data-dismiss="modal">X</button></div>'

    sec_str += '<div class="col-md-12"><div class="row pad-10 bg-lt-wt brdr"><button type="button" class="btnconfig" onclick="closepopup_scrl()" data-dismiss="modal">CANCEL</button><button type="button" id="indexexpression_save" class="btnconfig" onclick="save_indexexpression()" data-dismiss="modal">SAVE</button></div></div>'

    sec_str += '<div id="container" class="g4 pad-10 brdr except_sec">'
    sec_str += (
        '<table id="'
        + str(table_id)
        + '" data-escape="true"  data-search-on-enter-key="true" data-show-header="true"  data-filter-control="true"> <thead><tr>'
    )
    sec_str += '<th data-field="SELECT" class="wth45" data-checkbox="true" id ="check_boxappval" ><div class="action_col">SELECT</div></th>'
    attr_dict = {
        "FIELD_LABEL": "Field Label",
    }
    for key, invs in enumerate(list(ordered_keys)):
        invs = str(invs).strip()
        qstring = attr_dict.get(str(invs)) or ""

        sec_str += (
            '<th data-field="'
            + invs
            + '" data-title-tooltip="'
            + str(qstring)
            + '" data-sortable="true" data-filter-control="input">'
            + str(qstring)
            + "</th>"
        )
    sec_str += '</tr></thead><tbody class ="app_id" ></tbody></table>'
    sec_str += '<div id="indexexpression_footer"></div>'
    order_by = "order by FIELD_LABEL ASC"

    Gen_Index_Exp = SqlHelper.GetList(
        "select FIELD_LABEL from SYOBJD (NOLOCK) where OBJECT_NAME ='"
        + str(index_id)
        + "' and  FIELD_LABEL not in ('Added By','Added Date','Added By User Record Id','Last Modified By','Last Modified Date','"
        + str(autoindex_queryName)
        + "','"
        + str(lkpapi_nameval)
        + "') {} {}".format(order_by, pagination_condition)
    )

    if Gen_Index_Exp is not None:
        for row_data in Gen_Index_Exp:
            if row_data is not None:
                new_value_dict = {}
                for data in row_data:
                    new_value_dict[data.Key] = data.Value
                date_field.append(new_value_dict)

    QueryCount = len(date_field)

    values_list = ""
    values_lists = ""
    a_test = []
    table_id = "indexExpression_addnew"
    for invsk in list(Header_details):
        table_ids = "#" + str(table_id)
        filter_class = table_ids + " .bootstrap-table-filter-control-" + str(invsk)

        values_lists += "var " + str(invsk) + ' = $("' + str(filter_class) + '").val(); '

        values_lists += " ATTRIBUTE_VALUEList.push(" + str(invsk) + "); "

        a_test.append(invsk)
    TABLEID = "ADDNEW__INDEXEXPRESSION"
    RECORDID = ""
    RECORDFEILD = ""
    filter_control_function += (
        '$("'
        + filter_class
        + '").change( function(){var table_id = $(this).closest("table").attr("id"); var a_list = '
        + str(a_test)
        + "; ATTRIBUTE_VALUEList = []; "
        + str(values_lists)
        + ' SortColumn = localStorage.getItem("SortColumn"); SortColumnOrder = localStorage.getItem("SortColumnOrder"); PerPage = $("#PageCountValue").val(); PageInform = "1___" + PerPage + "___" + PerPage; cpq.server.executeScript("SYOBINVIEW", {\'TABLEID\': "'
        + str(TABLEID)
        + "\",'Primary_Data': \""
        + str(index_id)
        + "\", 'REC_ID':  \""
        + str(RECORD_ID)
        + "\",'A_Keys':a_list,'A_Values':ATTRIBUTE_VALUEList}, function(data) { date_field = data[3]; var assoc = data[1]; var api_name = data[2];data4 = data[4]; data5 = data[5]; if (date_field != \"NORECORDS\") { try { $(\""
        + str(table_ids)
        + '").bootstrapTable("load", date_field); $("#indexexpression_footer").html(data[6]); } catch(err) { $("'
        + str(table_ids)
        + '").bootstrapTable("load", date_field  ); $("#indexexpression_footer").html(data[6]); } document.getElementById("indexexpression_footer").style.border = ""; document.getElementById("indexexpression_footer").style.padding = "0px"; } else { var date_field = []; $("'
        + str(table_ids)
        + '").bootstrapTable("load", date_field  ); document.getElementById("indexexpression_footer").style.border = "1px solid #ccc"; document.getElementById("indexexpression_footer").style.padding = "5.5px"; document.getElementById("indexexpression_footer").innerHTML = "No Records to Display"; } });  });'
    )
    var_str = ""
    dbl_clk_function += (
        '$("'
        + str(table_ids)
        + '").on("all.bs.table", function (e, name, args) { $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); }); $("'
        + str(table_ids)
        + '\ th.bs-checkbox div.th-inner").before("<div class=\'padding:0; border-bottom: 1px solid #dcdcdc;\'>SELECT</div>"); $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>");'
    )
    Product.SetGlobal("QueryCount", str(QueryCount))
    if QueryCount != 0:
        var_str += """<div class="col-md-12 brdr listContStyle listpag"  >
                <div class="col-md-4 pager-numberofitem  clear-padding">
                    <span class="pager-number-of-items-item numitem" id="Rec_Index_Start_End" >{Records_Index_Start_And_End}</span>
                    <span class="pager-number-of-items-item fltltpad2mrg0" id="TotalIndexCount"  >{Pagination_TotalIndex_Count}</span>
                        <div class="clear-padding fltltmrgtp3"  >
                            <div  class="pull-right vralign">
                                <select onchange="ShowResultCountFunction_GS_ADD_NEW_INDEX_EXP(this)" id="ShowResultCountsIndex"  class="form-control pagecunt">
                                    <option value="10" {Selected_10}>10</option>
                                    <option value="20" {Selected_20}>20</option>
                                    <option value="50" {Selected_50}>50</option>
                                    <option value="100" {Selected_100}>100</option>
                                    <option value="200" {Selected_200}>200</option>
                                </select>
                            </div>
                        </div>
                </div>
                    <div class="col-xs-8 col-md-4  clear-padding totcnt"   data-bind="visible: totalItemCount">
                        <div class="clear-padding col-xs-12 col-sm-6 col-md-12 brdr0" >
                            <ul class="pagination pagination">
                                <li class="disabled"><a onclick="GetFirstResultFunction_GS_ADD_NEW_INDEX_EXP()" {Disable_First}><i class="fa fa-caret-left fnt14bold"  ></i><i class="fa fa-caret-left fnt14" ></i></a></li>
                                <li class="disabled"><a onclick="GetPreviuosResultFunction_GS_ADD_NEW_INDEX_EXP()" {Disable_Previous}><i class="fa fa-caret-left fnt14"  ></i>PREVIOUS</a></li>
                                <li class="disabled"><a onclick="GetNextResultFunction_GS_ADD_NEW_INDEX_EXP()" {Disable_Next}>NEXT<i class="fa fa-caret-right fnt14"  ></i></a></li>
                                <li class="disabled"><a onclick="GetLastResultFunction_GS_ADD_NEW_INDEX_EXP()" {Disable_Last}><i class="fa fa-caret-right fnt14"  ></i><i class="fa fa-caret-right fnt14bold"></i></a></li>
                            </ul>
                        </div>
                    </div> 
                    <div class="col-md-4 pr_page_pad">
                    <span id="page_count" class="currentPage page_right_content">{Current_Page}</span>
                        <span class="page_right_content pad_rt_2" >Page </span>
                    </div>
            </div></div>""".format(
            Records_Index_Start_And_End=records_start_and_end,
            Pagination_TotalIndex_Count=str(format(int(pagination_index_total_count), ",d")),
            Selected_10="selected" if fetch_count == 10 else "",
            Selected_20="selected" if fetch_count == 20 else "",
            Selected_50="selected" if fetch_count == 50 else "",
            Selected_100="selected" if fetch_count == 100 else "",
            Selected_200="selected" if fetch_count == 200 else "",
            Disable_First=disable_previous_and_first,
            Disable_Previous=disable_previous_and_first,
            Disable_Next=disable_next_and_last,
            Disable_Last=disable_next_and_last,
            Current_Page=current_page,
        )
    else:
        date_field = "NORECORDS"
    return (
        sec_str,
        new_value_dict,
        api_name,
        date_field,
        dbl_clk_function,
        filter_control_function,
        var_str,
    )


def obj_index_Basic_info(Primary_Data, RECORD_ID, ACTION):
    API_NAMES = ""
    sec_str = ""
    getkeyvalue = Sql.GetFirst(
        "Select OBJECT_INDEX_RECORD_ID from SYOBJX (NOLOCK) where INDEX_NAME = '" + str(Primary_Data) + "'"
    )
    syobj_data_query = Sql.GetList(
        "SELECT top 1000 * FROM  SYOBJD (NOLOCK) WHERE OBJECT_NAME='SYOBJX' and API_NAME Not in ('OBJECT_INDEX_RECORD_ID','MODUSR_RECORD_ID','CPQTABLEENTRYDATEMODIFIED','CPQTABLEENTRYMODIFIEDBY','CPQTABLEENTRYADDEDBY','ADDUSR_RECORD_ID','CPQTABLEENTRYDATEADDED') order by DISPLAY_ORDER"
    )
    API_NAMES = ",".join(str(data.API_NAME) for data in syobj_data_query if data.DATA_TYPE != "DATE")

    for data in syobj_data_query:
        text = ""
        if data.PERMISSION != "READ ONLY":
            editable_permission = "TRUE"
        if data.DATA_TYPE == "DATE":
            if text == "":
                text = "CONVERT(VARCHAR(10)," + str(data.API_NAME) + ",101) AS " + str(data.API_NAME)
            else:
                text = text + "," + "CONVERT(VARCHAR(10)," + str(data.API_NAME) + ",101) AS " + str(data.API_NAME)
            API_NAMES = API_NAMES + "," + ",".join(str(data) for data in text.split(","))
    sec_str += '<div id="container" class="width100">'

    if editable_permission == "TRUE":
        sec_str += (
            '<div class="g4 dyn_main_head master_manufac glyphicon pointer glyphicon-chevron-down" onclick="dyn_main_sec_collapse_arrow(this)" data-toggle="collapse in" data-target="#colls'
            + str(Primary_Data)
            + '"><label class="onlytext"></label><div>'
        )
    sec_str += '<table id="SYOBJX" class="ma_width_marg">'
    if syobj_data_query is not None:
        for val in syobj_data_query:
            readonly = "readonly"
            disable = "disabled"
            current_obj_api_name = val.API_NAME.strip()
            current_obj_field_lable = val.FIELD_LABEL.strip()
            readonly_val = val.PERMISSION.strip()
            data_type = val.DATA_TYPE.strip()
            formula_data_type = ""
            if str(val.FORMULA_DATA_TYPE) != "" and len(str(val.FORMULA_DATA_TYPE)) > 0:
                formula_data_type = val.FORMULA_DATA_TYPE
            if str(val.FORMULA_LOGIC) != "" and len(val.FORMULA_LOGIC) > 0:
                formula_logics = val.FORMULA_LOGIC
            erp_source = str(val.SOURCE_DATA)
            current_obj_value = ""
            header_obj_value = ""
            datepicker = "onclick_datepicker('" + current_obj_api_name + "')"
            ids = ""
            add_style = ""
            idval = ""
            edit_warn_icon = ""
            formula_permission = ""
            formula_obj_permission = ""
            left_float = ""
            datepicker_onchange = "onchangedatepicker('" + current_obj_api_name + "')"
            edit_pencil_icon = '<i class="fa fa-lock" aria-hidden="true"></i>'

            sec_str += (
                '<tr class="iconhvr borbot1" id="'
                + str(current_obj_api_name)
                + '" style=" '
                + str(add_style)
                + '"><td class="width350"><label class="padd_marbot">'
                + str(current_obj_field_lable)
                + '</label></td><td class="width40"><a class="bgcccwth10" href="#" data-placement="top" data-toggle="popover" data-content="'
                + str(current_obj_field_lable)
                + '" ><i class="fa fa-info-circle flt_lt"></i>'
            )
            sec_str += "</a></td>"
            if readonly_val.upper() != "READ ONLY" and data_type != "AUTO NUMBER" and erp_source != "ERP":
                edit_pencil_icon = '<i class="fa fa-pencil" aria-hidden="true"></i>'
            else:
                edit_pencil_icon = '<i class="fa fa-lock" aria-hidden="true"></i>'

            if len(current_obj_value) > 0:
                current_obj_value = current_obj_value
            else:
                current_obj_value = ""

            if readonly_val == "READ ONLY":
                if formula_obj_permission == "true" and formula_permission != "READ ONLY" and canedit.upper() == "TRUE":
                    edit_pencil_icon = '<i class="fa fa-pencil" aria-hidden="true"></i>'
                    if MODE == "EDIT":
                        readonly = ""
                        disable = ""
                else:
                    edit_pencil_icon = '<i class="fa fa-lock" aria-hidden="true"></i>'
                    readonly = "readonly"
                    disable = "disabled"
            else:

                disable = ""
                readonly = ""
            if data_type == "AUTO NUMBER":

                sec_str += (
                    '<td><input id="'
                    + str(current_obj_api_name)
                    + '" type="text" value="'
                    + current_obj_value
                    + '" class="form-control related_popup_css disp_none" disabled></td>'
                )
                auto_field = (
                    '<tr class="iconhvr borbot1 disp_none" style=" '
                    + str(add_style)
                    + '"><td class="width350"><label class="padd_marbot">'
                    + str(current_obj_field_lable)
                    + '</label></td><td class="width40"><a class="bgcccwth10" href="#" data-placement="top" data-toggle="popover" data-content="'
                    + str(current_obj_field_lable)
                    + '" ><i class="fa fa-info-circle flt_lt"></i><td><input id="'
                    + str(current_obj_api_name)
                    + '" type="text" value="'
                    + current_obj_value
                    + '" class="form-control related_popup_css" disabled></td><tr>'
                )
            elif data_type == "LOOKUP":
                current_obj_value = ""
                # col_index_sel_exp = Product.GetGlobal("INDEX_COLUMNS_SELECTED")
                # expression_col = col_index_sel_exp[1:-2].replace("'",'')
                sec_str += (
                    '<td><input id="'
                    + str(current_obj_api_name)
                    + '" type="text" value="'
                    + current_obj_value
                    + '"  class="form-control related_popup_css" disabled><input type="image" id="ADDNEW__INDEXEXPRESSION" onclick="popupReindexEXPRESSION()" data-toggle="modal" data-target="#myModalTestIndexadd" src="../mt/default/images/customer_lookup.gif"></td>'
                )
            elif data_type == "TEXT" and str(current_obj_api_name) != "INDEX_NAME":

                queryval = SqlHelper.GetFirst(
                    "Select PARENT_OBJECT_RECORD_ID from SYOBJD (NOLOCK) where OBJECT_NAME = '" + str(Primary_Data) + "'"
                )
                if queryval:
                    RECORD_ID = queryval.PARENT_OBJECT_RECORD_ID
                sec_str += (
                    '<td><input id="'
                    + str(current_obj_api_name)
                    + '" type="text" value="'
                    + RECORD_ID
                    + '" class="form-control related_popup_css" disabled></td>'
                )
            elif data_type == "TEXT" and str(current_obj_api_name) == "INDEX_NAME":
                current_obj_valueName = "INDEX" + "_" + Primary_Data
                sec_str += (
                    '<td><input id="'
                    + str(current_obj_api_name)
                    + '" type="text" value="'
                    + current_obj_valueName
                    + '" class="form-control related_popup_css" style="'
                    + str(left_float)
                    + ' " '
                    + disable
                    + ">"
                    + str(edit_warn_icon)
                    + "</td>"
                )
            elif data_type == "LONG TEXT AREA":

                sec_str += (
                    '<td><textarea class="form-control related_popup_css txtArea col_width75" id="'
                    + str(current_obj_api_name)
                    + '" rows="1" cols="100" '
                    + disable
                    + ">"
                    + current_obj_value
                    + "</textarea></td>"
                )

            elif data_type == "DATE" and MODE == "EDIT":
                date_field.append(current_obj_api_name)
                sec_str += (
                    '<td><input id="'
                    + str(current_obj_api_name)
                    + '" value="'
                    + current_obj_value
                    + '" type="text"  onclick="'
                    + str(datepicker)
                    + '" onchange="'
                    + str(datepicker_onchange)
                    + '" class="form-control datePickerField wid_mar_float_l_bor" '
                    + disable
                    + " ></td>"
                )

            elif data_type == "NUMBER":
                sec_str += (
                    '<td><input id="'
                    + str(current_obj_api_name)
                    + '" type="number" value="'
                    + current_obj_value
                    + '" class="form-control related_popup_css" style="'
                    + str(add_style)
                    + '" '
                    + disable
                    + "></td>"
                )

            elif data_type == "FORMULA" and formula_data_type == "TEXT":
                if not "CTX" in str(formula_logics) and str(formula_logics) != "":
                    current_obj_value = Product.ParseString(formula_logics)

                sec_str += (
                    '<td><input id="'
                    + str(current_obj_api_name)
                    + '" type="text" value="'
                    + Primary_Data
                    + '" class="form-control related_popup_css" style="'
                    + str(add_style)
                    + '" '
                    + disable
                    + "></td>"
                )
            elif data_type == "PICKLIST":
                sec_str += (
                    '<td><select id="'
                    + str(current_obj_api_name)
                    + '" value="'
                    + current_obj_value
                    + '" type="text" class="form-control pop_up_brd_rad related_popup_css flt_L_font" '
                    + disable
                    + " >"
                )
                Sql_Quality_Tier = Sql.GetFirst(
                    "select PICKLIST_VALUES FROM  SYOBJD (NOLOCK) where OBJECT_NAME='SYOBJX' and DATA_TYPE='PICKLIST' and API_NAME='"
                    + str(current_obj_api_name)
                    + "'"
                )
                Tier_List = (Sql_Quality_Tier.PICKLIST_VALUES).split(",")
                for req1 in Tier_List:
                    sec_str += "<option>" + str(req1) + "</option>"
                sec_str += "</select></td>"
            else:
                sec_str += (
                    '<td><input id="'
                    + str(current_obj_api_name)
                    + '" type="text" value="'
                    + current_obj_value
                    + '" class="form-control related_popup_css" style="'
                    + str(left_float)
                    + ' " '
                    + disable
                    + ">"
                    + str(edit_warn_icon)
                    + "</td>"
                )
            sec_str += (
                '<td class="fltrtbrdbt0"><div class="col-md-12 editiconright"><a href="#" class="editclick">'
                + str(edit_pencil_icon)
                + "</a></div></td>"
            )
            sec_str += "</tr>"
    sec_str += "</table>"
    sec_str += "</div></div></div>"
    return sec_str


def expressionsave_column(Primary_Data, CURRREC, SELECTROW):
    Product.SetGlobal("INDEX_COLUMNS_SELECTED", str(SELECTROW))
    return "test"


def obj_index_Save_info(obj_rec_indexid, indexname, indextype, expression1, objname, objrcid, ACTION):
    LABLE = ["OBJECT_INDEX_RECORD_ID", "INDEX_NAME", "INDEX_EXPRESSION", "INDEX_TYPE", "OBJECT_APINAME", "OBJECT_RECORD_ID"]
    key = []
    ObjectName = "SYOBJX"

    # get selected columns from pop up Start
    col_index_sel_exp = Product.GetGlobal("INDEX_COLUMNS_SELECTED")
    expression_col = eval(col_index_sel_exp)
    # expression_col = col_index_sel_exp[1:-2].replace("'",'')
    col_index_sel_exp_val_ind = []
    # col_index_sel_exp_val_ind.append(expression_col)
    col_index_sel_exp_val = []
    for val in expression_col:
        #Trace.Write(val)
        queryapiname = SqlHelper.GetFirst(
            "Select API_NAME from SYOBJD (NOLOCK) where FIELD_LABEL = '"
            + str(val)
            + "' and OBJECT_NAME= '"
            + str(objname)
            + "'"
        )
        if queryapiname:
            apiname = queryapiname.API_NAME
            col_index_sel_exp_val.append(apiname)
    # expression_col = col_index_sel_exp_val[1:-2].replace("'",'')
    # get selected columns from pop up End

    # DELETE EXIXTING INDEX FROM TABLE BEFORE SAVE START
    tableInfo = SqlHelper.GetTable("SYOBJX")
    expression_col = str(col_index_sel_exp_val)[1:-2].replace("'", "")
    deletesyobjxquery = Sql.GetList(
        "SELECT CpqTableEntryId FROM  SYOBJX (NOLOCK) WHERE OBJECT_APINAME ='" + str(objname) + "'"
    )
    if deletesyobjxquery is not None or deletesyobjxquery != "":
        for tablerow in deletesyobjxquery:
            tableInfo.AddRow(tablerow)
            Sql.Delete(tableInfo)
            # Trace.Write("Table Deleted")
    # DELETE EXIXTING INDEX FROM TABLE BEFORE SAVE END

    # A043S001P01-10789 Start
    autoindex_queryName = ""
    lkpapi_name = []
    lkpapi_nameval = ""

    autoindex_query = SqlHelper.GetFirst(
        "select API_NAME  from SYOBJD (NOLOCK) where OBJECT_NAME ='" + str(objname) + "' and DATA_TYPE = 'AUTO NUMBER'"
    )
    if autoindex_query:
        autoindex_queryName = autoindex_query.API_NAME

    lkpup_query = SqlHelper.GetList(
        "select API_NAME from SYOBJD (NOLOCK) where OBJECT_NAME ='" + str(objname) + "' and DATA_TYPE = 'LOOKUP'"
    )

    if lkpup_query is not None or lkpup_query != "":
        for val in lkpup_query:
            if val.API_NAME:
                lkpapi_name.append(val.API_NAME)
    lkpapi_nameval = str(lkpapi_name)[1:-2].replace("'", "")
    if lkpapi_nameval:
        expression_col = expression_col + "," + autoindex_queryName + "," + lkpapi_nameval
    else:
        expression_col = expression_col + "," + autoindex_queryName
    # A043S001P01-10789 End

    # check indexname exist Start
    indexnameExits = ""
    IndexnameQuery = Sql.GetFirst("SELECT INDEX_NAME FROM  SYOBJX (NOLOCK) WHERE OBJECT_APINAME ='" + str(objname) + "'")
    if IndexnameQuery:
        indexnameExits = IndexnameQuery.INDEX_NAME
    # Trace.Write('indexnameExits----'+str(indexnameExits))
    # check indexname exist End
    indexname = indexname + "_" + objname
    # insert in syobjx start
    new_val = str(Guid.NewGuid()).upper()
    key.append(new_val)
    key.append(indexname)
    key.append(expression_col)
    key.append(indextype)
    key.append(objname)
    key.append(objrcid)
    newdict = dict(zip(LABLE, key))
    tableInfo = Sql.GetTable(str(ObjectName))
    tablerow = newdict
    tableInfo.AddRow(tablerow)
    Sql.Upsert(tableInfo)

    # insert in syobjx End

    conIndex = Product.GetContainerByName("MM_OBJ_CTR_REINDEX_DATA")
    conIndex.Rows.Clear()
    # Trace.Write('170-----OBJECT_NAME----'+str(objname))
    SQLobjIndex = Sql.GetList("SELECT top 1000 * FROM  SYOBJX (NOLOCK) WHERE OBJECT_APINAME ='" + str(objname) + "'")

    if SQLobjIndex is not None:
        for obj in SQLobjIndex:
            row = conIndex.AddNewRow()
            # row["OBJECT_IINDEX_RECORD_ID"] = str(obj.OBJECT_IINDEX_RECORD_ID)
            row["INDEX_NAME"] = str(obj.INDEX_NAME)
            row["INDEX_EXPRESSION"] = str(obj.INDEX_EXPRESSION)
            row["INDEX_TYPE"] = str(obj.INDEX_TYPE)

            # row["OBJECT_APINAME"] = str(obj.OBJECT_APINAME)
    Product.Attributes.GetByName("MM_OBJ_CTR_REINDEX_DATA").Access = AttributeAccess.ReadOnly

    return "data"


# A043S001P01-8970 start
def obj_index_Grid_info(Primary_Data_grid, ACTIONVIEW, OBJ_TableName):
    # check index query start
    getobjectrec = ""
    try:
        DROP_INDEX = Sql.GetList(
            "SELECT C.NAME AS INDEX_N  FROM sys.index_columns A JOIN SYS.COLUMNS B ON A.COLUMN_ID = B.COLUMN_ID AND A.OBJECT_ID = B.OBJECT_ID JOIN SYS.INDEXES C ON A.INDEX_ID = C.INDEX_ID AND A.OBJECT_ID = C.OBJECT_ID WHERE OBJECT_NAME(A.OBJECT_ID)='"
            + Primary_Data_grid
            + "'   "
        )
        if len(DROP_INDEX) > 1:
            for inse in DROP_INDEX:
                if "PK_" not in inse.INDEX_N:
                    QueryStatement = "DROP INDEX {Index_Name} on {Obj_Name}".format(
                        Index_Name=inse.INDEX_N, Obj_Name=Primary_Data_grid
                    )
                    a = Sql.RunQuery(QueryStatement)
        # QueryStatement = "DROP INDEX INDEX_{Index_Name} on {Obj_Name}".format(
        #     Index_Name=Primary_Data_grid, Obj_Name=Primary_Data_grid
        # )
        # a = Sql.RunQuery(QueryStatement)
    except:
        QueryStatement = "DROP INDEX INDEX_{Index_Name} on {Obj_Name}".format(
            Index_Name=Primary_Data_grid, Obj_Name=Primary_Data_grid
        )
        a = Sql.RunQuery(QueryStatement)
    # check index query End

    # create index query start
    # get object_record_id from syobjh start
    getindexquey = Sql.GetFirst(
        "SELECT RECORD_ID  FROM  SYOBJH (Nolock) WHERE OBJECT_NAME ='" + str(Primary_Data_grid) + "'"
    )
    if getindexquey:
        getobjectrec = getindexquey.RECORD_ID
    # get object_record_id from syobjh end

    indexquey = Sql.GetList("SELECT top 1000 * FROM  SYOBJX (Nolock) WHERE OBJECT_RECORD_ID ='" + str(getobjectrec) + "'")
    if indexquey is not None:
        for val in indexquey:
            if val.INDEX_EXPRESSION:
                INDEX_EXPRESSION = val.INDEX_EXPRESSION
                INDEX_NAME = val.INDEX_NAME
                QueryStatement = "CREATE INDEX INDEX_{Index_Name} on {Obj_Name}({Col_Name})".format(
                    Index_Name=INDEX_NAME, Obj_Name=val.OBJECT_APINAME, Col_Name=INDEX_EXPRESSION
                )
                try:
                    a = Sql.RunQuery(QueryStatement)
                except:
                    Trace.Write("Already index Created")
    # create index query end

    return "index"


# A043S001P01-8970 end


def obj_index_ReindexAll_info(ACTIONVIEWREINDEX):
    # Trace.Write('367777----------------REINDEX ALL FUNCTIONS--------')
    indexquey = Sql.GetList("SELECT top 1000 * FROM  SYOBJX (NOLOCK)")
    if indexquey is not None:

        for val in indexquey:

            if val.INDEX_EXPRESSION_01:
                Index_Name = val.INDEX_NAME + "_" + val.INDEX_EXPRESSION_01
                QueryStatement = "CREATE INDEX INDEX_{Index_Name} on {Obj_Name}({Col_Name})".format(
                    Index_Name=Index_Name, Obj_Name=val.OBJECT_APINAME, Col_Name=val.INDEX_EXPRESSION_01
                )
                try:
                    a = Sql.RunQuery(QueryStatement)
                except:
                    Trace.Write("Already index Created")
            if val.INDEX_EXPRESSION_02:
                Index_Name = val.INDEX_NAME + "_" + val.INDEX_EXPRESSION_02
                QueryStatement = "CREATE INDEX INDEX_{Index_Name} on {Obj_Name}({Col_Name})".format(
                    Index_Name=Index_Name, Obj_Name=val.OBJECT_APINAME, Col_Name=val.INDEX_EXPRESSION_02
                )
                try:
                    a = Sql.RunQuery(QueryStatement)
                except:
                    Trace.Write("Already index Created")
            if val.INDEX_EXPRESSION_03:
                Index_Name = val.INDEX_NAME + "_" + val.INDEX_EXPRESSION_03
                QueryStatement = "CREATE INDEX INDEX_{Index_Name} on {Obj_Name}({Col_Name})".format(
                    Index_Name=Index_Name, Obj_Name=val.OBJECT_APINAME, Col_Name=val.INDEX_EXPRESSION_03
                )
                try:
                    a = Sql.RunQuery(QueryStatement)
                except:
                    Trace.Write("Already index Created")
            if val.INDEX_EXPRESSION_04:
                Index_Name = val.INDEX_NAME + "_" + val.INDEX_EXPRESSION_04
                QueryStatement = "CREATE INDEX INDEX_{Index_Name} on {Obj_Name}({Col_Name})".format(
                    Index_Name=Index_Name, Obj_Name=val.OBJECT_APINAME, Col_Name=val.INDEX_EXPRESSION_04
                )
                try:
                    a = Sql.RunQuery(QueryStatement)
                except:
                    Trace.Write("Already index Created")
            if val.INDEX_EXPRESSION_05:
                Index_Name = val.INDEX_NAME + "_" + val.INDEX_EXPRESSION_05
                QueryStatement = "CREATE INDEX INDEX_{Index_Name} on {Obj_Name}({Col_Name})".format(
                    Index_Name=Index_Name, Obj_Name=val.OBJECT_APINAME, Col_Name=val.INDEX_EXPRESSION_05
                )
                try:
                    a = Sql.RunQuery(QueryStatement)
                except:
                    Trace.Write("Already index Created")
    return "reindex"


offset_list = []


for val in Param:
    offset_list.append(val.Key)
if "Offset_Skip_Count" in offset_list:
    Offset_Skip_Count = Param.Offset_Skip_Count
else:
    Offset_Skip_Count = 1
if "Fetch_Count" in offset_list:
    Fetch_Count = Param.Fetch_Count
else:
    Fetch_Count = 10

if hasattr(Param, "Primary_Data"):
    Primary_Data = Param.Primary_Data
    Product.SetGlobal("Primary_Data", str(Primary_Data))
else:
    Primary_Data = ""

if hasattr(Param, "REC_ID"):
    RECORD_ID = Param.REC_ID
    Product.SetGlobal("REC_ID", str(RECORD_ID))
else:
    RECORD_ID = ""

if hasattr(Param, "ACTION"):
    ACTION = Param.ACTION
    Product.SetGlobal("ACTION", str(ACTION))
else:
    ACTION = ""

if hasattr(Param, "indexname"):
    indexname = Param.indexname
    Product.SetGlobal("indexname", str(indexname))
else:
    indexname = ""

if hasattr(Param, "obj_rec_indexid"):
    obj_rec_indexid = Param.obj_rec_indexid
    Product.SetGlobal("obj_rec_indexid", str(obj_rec_indexid))
else:
    obj_rec_indexid = ""

if hasattr(Param, "expression1"):
    expression1 = Param.expression1
    Product.SetGlobal("expression1", str(expression1))
else:
    expression1 = ""


if hasattr(Param, "objname"):
    objname = Param.objname
    Product.SetGlobal("objname", str(objname))
else:
    objname = ""

if hasattr(Param, "objrcid"):
    objrcid = Param.objrcid
    Product.SetGlobal("objrcid", str(objrcid))
else:
    objrcid = ""

if hasattr(Param, "indextype"):
    indextype = Param.indextype
    Product.SetGlobal("indextype", str(indextype))
else:
    indextype = ""

if hasattr(Param, "Primary_Data_grid"):
    Primary_Data_grid = Param.Primary_Data_grid
    Product.SetGlobal("Primary_Data_grid", str(Primary_Data_grid))
else:
    Primary_Data_grid = ""

if hasattr(Param, "ACTIONVIEW"):
    ACTIONVIEW = Param.ACTIONVIEW
    Product.SetGlobal("ACTIONVIEW", str(ACTIONVIEW))
else:
    ACTIONVIEW = ""


if hasattr(Param, "CURRREC"):
    CURRREC = Param.CURRREC
    Product.SetGlobal("CURRREC", str(CURRREC))
else:
    CURRREC = ""

if hasattr(Param, "OBJ_TableName"):
    OBJ_TableName = Param.OBJ_TableName
    Product.SetGlobal("OBJ_TableName", str(OBJ_TableName))
else:
    OBJ_TableName = ""

if hasattr(Param, "ACTIONVIEWREINDEX"):
    ACTIONVIEWREINDEX = Param.ACTIONVIEWREINDEX
    Product.SetGlobal("ACTIONVIEWREINDEX", str(ACTIONVIEWREINDEX))
else:
    ACTIONVIEWREINDEX = ""

if hasattr(Param, "SELECTROW"):
    SELECTROW = list(Param.SELECTROW)
else:
    SELECTROW = ""


if (
    ACTION != "ADDNEW_SAVE"
    and ACTIONVIEW != "ADDNEW_REINDEXGRID"
    and ACTIONVIEWREINDEX != "REINDEXALL"
    and ACTION != "ADDNEW_INDEXEXPRESSION"
    and CURRREC != "INDEXCOLUMNSAVE"
):
    ApiResponse = ApiResponseFactory.JsonResponse(obj_index_Basic_info(Primary_Data, RECORD_ID, ACTION))

elif ACTIONVIEW == "ADDNEW_REINDEXGRID" and ACTIONVIEWREINDEX != "REINDEXALL":
    ApiResponse = ApiResponseFactory.JsonResponse(obj_index_Grid_info(Primary_Data_grid, ACTIONVIEW, OBJ_TableName))


elif ACTIONVIEWREINDEX == "REINDEXALL":
    ApiResponse = ApiResponseFactory.JsonResponse(obj_index_ReindexAll_info(ACTIONVIEWREINDEX))

elif ACTION == "ADDNEW_INDEXEXPRESSION":
    ApiResponse = ApiResponseFactory.JsonResponse(obj_index_pop_up_expression(Primary_Data, RECORD_ID, ACTION))
elif CURRREC == "INDEXCOLUMNSAVE":
    ApiResponse = ApiResponseFactory.JsonResponse(expressionsave_column(Primary_Data, CURRREC, SELECTROW))
else:
    ApiResponse = ApiResponseFactory.JsonResponse(
        obj_index_Save_info(obj_rec_indexid, indexname, indextype, expression1, objname, objrcid, ACTION)
    )
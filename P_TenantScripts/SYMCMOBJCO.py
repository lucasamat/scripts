# =========================================================================================================================================
#   __script_name : SYMCMOBJCO.PY
#   __script_description : THIS SCRIPT IS USED TO DO ADD NEW FOR THE CONSTRAINT IN THE OBJECTS TAB UNDER SYSTEM ADMIN APP
#   __primary_author__ : 
#   __create_date : 31-08-2020
#   Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct
import SYCNGEGUID as CPQID
from SYDATABASE import SQL

Sql = SQL()


def obj_constraint_Basic_info(Primary_Data, RECORD_ID, MODE):
    API_NAMES = ""
    sec_str = ""
    GetAPIValues = Sql.GetFirst("SELECT * FROM SYOBJC WHERE OBJECT_RECORD_ID ='" + str(RECORD_ID) + "' ")
    syobj_data_query = Sql.GetList(
        "SELECT top 1000 * FROM  SYOBJD (NOLOCK) WHERE OBJECT_NAME='SYOBJC' and API_NAME Not in ('MODUSR_RECORD_ID','CPQTABLEENTRYDATEMODIFIED','CPQTABLEENTRYMODIFIEDBY','CPQTABLEENTRYADDEDBY','ADDUSR_RECORD_ID','CPQTABLEENTRYDATEADDED') order by DISPLAY_ORDER"
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
            '<div class="g4 dyn_main_head master_manufac glyphicon pointer glyphicon-chevron-down" onclick="dyn_main_sec_collapse_arrow(this)" data-toggle="collapse" data-target="#colls'
            + str(Primary_Data)
            + '"><label class="onlytext"></label><div>'
        )
    sec_str += '<table id="SYOBJC" class="ma_width_marg">'
    if syobj_data_query is not None:
        for val in syobj_data_query:
            
            readonly = ""
            disable = ""
            current_obj_api_name = val.API_NAME.strip()
            current_obj_field_lable = val.FIELD_LABEL.strip()
            readonly_val = val.PERMISSION.strip()
            data_type = val.DATA_TYPE.strip()
            canedit = ""
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
            lookup_val = ["OBJECT_APINAME", "OBJECTFIELD_APINAME"]
            datepicker_onchange = "onchangedatepicker('" + current_obj_api_name + "')"
            edit_pencil_icon = '<i class="fa fa-lock" aria-hidden="true"></i>'
            if (data_type == "AUTO NUMBER" and MODE == "ADDNEW") or data_type == "LOOKUP":
                add_style = "display:none"
            sec_str += (
                '<tr class="iconhvr borbot1" id="'
                + str(current_obj_api_name)
                + '" style=" '
                + str(add_style)
                + '"><td class="width350"><label class="padd_marbot">'
                + str(current_obj_field_lable)
                + '</label></td><td class="width40"><a class="color_align_width" href="#" data-placement="top" data-toggle="popover" data-content="'
                + str(current_obj_field_lable)
                + '" ><i class="fa fa-info-circle flt_lt"></i>'
            )
            sec_str += "</a></td>"
            if readonly_val.upper() != "READ ONLY" and data_type != "AUTO NUMBER" and erp_source != "ERP":
                edit_pencil_icon = '<i class="fa fa-pencil" aria-hidden="true"></i>'
            else:
                edit_pencil_icon = '<i class="fa fa-lock" aria-hidden="true"></i>'
            if GetAPIValues is not None:
                current_obj_value = eval(str("GetAPIValues." + str(current_obj_api_name)))
            if str(current_obj_value) != "":
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
            elif MODE == "EDIT":
                if canedit.upper() == "TRUE":
                    if erp_source != "ERP":
                        edit_pencil_icon = '<i class="fa fa-pencil" aria-hidden="true"></i>'
                        readonly = ""
                        disable = ""
                    else:
                        edit_pencil_icon = '<i class="fa fa-lock" aria-hidden="true"></i>'
                        readonly = "readonly"
                        disable = "disabled"
                else:
                    edit_pencil_icon = '<i class="fa fa-lock" aria-hidden="true"></i>'
                    readonly = "readonly"
                    disable = "disabled"

            if data_type == "AUTO NUMBER":

                if MODE == "EDIT":
                    sec_str += (
                        '<td><input id="'
                        + str(current_obj_api_name)
                        + '" type="text"  value="'
                        + RECORD_ID
                        + '" class="form-control related_popup_css" disabled></td>'
                    )
                else:
                    sec_str += (
                        '<td><input id="'
                        + str(current_obj_api_name)
                        + '" type="text" style="display: none;" value="'
                        + RECORD_ID
                        + '" class="form-control related_popup_css" disabled></td>'
                    )
                auto_field = (
                    '<tr style="display: none;" class="iconhvr borbot1" style=" '
                    + str(add_style)
                    + '"><td class="width350"><label class="padd_marbot">'
                    + str(current_obj_field_lable)
                    + '</label></td><td class="width40"><a class="color_align_width" href="#" data-placement="top" data-toggle="popover" data-content="'
                    + str(current_obj_field_lable)
                    + '" ><i class="fa fa-info-circle flt_lt"></i><td><input id="'
                    + str(current_obj_api_name)
                    + '" type="text" value="'
                    + current_obj_value
                    + '" class="form-control related_popup_css" disabled></td><tr>'
                )
            elif data_type == "LOOKUP":
                sec_str += (
                    '<td><input id="'
                    + str(current_obj_api_name)
                    + '" type="text" value="'
                    + current_obj_value
                    + '" class="form-control related_popup_css" disabled></td>'
                )
            elif data_type == "TEXT":

                queryval = SqlHelper.GetFirst(
                    "Select PARENT_OBJECT_RECORD_ID from SYOBJD where OBJECT_NAME = '" + str(Primary_Data) + "'"
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

            elif (data_type == "FORMULA" and formula_data_type != "CHECKBOX") and (MODE == "EDIT" or MODE == "ADDNEW"):
                if current_obj_api_name != "OBJECT_APINAME":
                    if current_obj_api_name in lookup_val and str(readonly) != "readonly":
                        sec_str += (
                            '<td><input id="'
                            + str(current_obj_api_name)
                            + '" type="text" value="'
                            + current_obj_value
                            + '" class="form-control lookupBg related_popup_css flt_lt" readonly>'
                        )

                        
                        GetlookupTable = Sql.GetFirst(
                            "SELECT LOOKUP_OBJECT FROM SYOBJD(NOLOCK) WHERE LOOKUP_API_NAME = '"
                            + str(current_obj_api_name)
                            + "' "
                        )
                        if GetlookupTable is not None:
                            ids = str(GetlookupTable.LOOKUP_OBJECT)
                        sec_str += '<input class="popup flt_lt" id="ADDNEW__INDEXEXPRESSION" data-target="#myModalTestIndexadd" onclick="popupReindexEXPRESSION()" type="image" data-toggle="modal" src="../mt/default/images/customer_lookup.gif">'
                    
                elif str(current_obj_api_name) == "OBJECT_APINAME":
                    sec_str += (
                        '<td><input id="'
                        + str(current_obj_api_name)
                        + '" type="text" value="'
                        + current_obj_value
                        + '" class="form-control related_popup_css flt_lt" style="'
                        + str(left_float)
                        + ' " disabled>'
                        + str(edit_warn_icon)
                        + "</td>"
                    )
                else:
                    if str(formula_data_type) == "TEXT" and str(readonly) != "readonly":
                        sec_str += (
                            '<td><input id="'
                            + str(current_obj_api_name)
                            + '" type="text" value="'
                            + current_obj_value
                            + '" class="form-control related_popup_css flt_lt" style="'
                            + str(left_float)
                            + ' ">'
                            + str(edit_warn_icon)
                            + "</td>"
                        )
                    else:
                        sec_str += (
                            '<td><input id="'
                            + str(current_obj_api_name)
                            + '" type="text" value="'
                            + current_obj_value
                            + '" class="form-control related_popup_css flt_lt" style="'
                            + str(left_float)
                            + ' " disabled>'
                            + str(edit_warn_icon)
                            + "</td>"
                        )
            elif data_type == "FORMULA" and formula_data_type == "TEXT":
                
                if not "CTX" in str(formula_logics) and str(formula_logics) != "":
                    current_obj_value = Product.ParseString(formula_logics)

                sec_str += (
                    '<td><input id="'
                    + str(current_obj_api_name)
                    + '" type="text" value="'
                    + current_obj_value
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
                    "select PICKLIST_VALUES FROM  SYOBJD (NOLOCK) where OBJECT_NAME='SYOBJC' and DATA_TYPE='PICKLIST' and API_NAME='"
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


def obj_constraint_Save_Info(OBJ_CONST_TYPE, OBJ_API_NAME, MODE, OBJ_FIELD_NAME, OBJ_REC_ID):
    col_index_sel_exp = Product.GetGlobal("INDEX_COLUMNS_SELECTED")
    expression_col = eval(col_index_sel_exp)

    col_index_sel_exp_val_ind = []


    col_index_sel_exp_val = []
    for val in expression_col:
        #Trace.Write(val)
        queryapiname = SqlHelper.GetFirst(
            "Select API_NAME from SYOBJD where FIELD_LABEL = '" + str(val) + "' and OBJECT_NAME= '" + str(OBJ_API_NAME) + "'"
        )
        if queryapiname:
            apiname = queryapiname.API_NAME
            col_index_sel_exp_val.append(apiname)
    expression_col = str(col_index_sel_exp_val)[1:-2].replace("'", "")

    LABLE = [
        "OBJECT_CONSTRAINT_RECORD_ID",
        "CONSTRAINT_TYPE",
        "OBJECT_APINAME",
        "OBJECTFIELD_APINAME",
        "OBJECTFIELD_RECORD_ID",
        "OBJECT_RECORD_ID",
    ]
    key = []
    new_val = str(Guid.NewGuid()).upper()
    key.append(new_val)
    key.append(OBJ_CONST_TYPE)
    key.append(OBJ_API_NAME)
    key.append(OBJ_FIELD_NAME)
    key.append(OBJ_REC_ID)
    key.append(OBJ_REC_ID)
    ObjectName = "SYOBJC"
    newdict = dict(zip(LABLE, key))
    tableInfo = Sql.GetTable(str(ObjectName))
    tablerow = newdict
    tableInfo.AddRow(tablerow)
    Sql.Upsert(tableInfo)
    return "Constraint"


# obj_constraint_Basic_info('','','ADDNEW')
if hasattr(Param, "Action"):
    MODE = Param.Action
    Product.SetGlobal("MODE", str(MODE))
else:
    MODE = ""
if hasattr(Param, "Primary_Data"):
    Primary_Data = Param.Primary_Data
    Product.SetGlobal("Primary_Data", str(Primary_Data))
else:
    Primary_Data = ""
# Primary_Data = Param.Primary_Data
if hasattr(Param, "REC_ID"):
    RECORD_ID = Param.REC_ID
    Product.SetGlobal("REC_ID", str(RECORD_ID))
else:
    RECORD_ID = ""

if hasattr(Param, "OBJ_CONST_TYPE"):
    OBJ_CONST_TYPE = Param.OBJ_CONST_TYPE
    Product.SetGlobal("OBJ_CONST_TYPE", str(OBJ_CONST_TYPE))
else:
    OBJ_CONST_TYPE = ""

if hasattr(Param, "OBJ_API_NAME"):
    OBJ_API_NAME = Param.OBJ_API_NAME
    Product.SetGlobal("OBJ_API_NAME", str(OBJ_API_NAME))
else:
    OBJ_API_NAME = ""

if hasattr(Param, "OBJ_FIELD_NAME"):
    OBJ_FIELD_NAME = Param.OBJ_FIELD_NAME
    Product.SetGlobal("OBJ_FIELD_NAME", str(OBJ_FIELD_NAME))
else:
    OBJ_API_NAME = ""

if hasattr(Param, "OBJ_REC_ID"):
    OBJ_REC_ID = Param.OBJ_REC_ID
    Product.SetGlobal("OBJ_REC_ID", str(OBJ_REC_ID))
else:
    OBJ_REC_ID = ""
if MODE == "ADDNEW" or MODE == "EDIT":
    ApiResponse = ApiResponseFactory.JsonResponse(obj_constraint_Basic_info(Primary_Data, RECORD_ID, MODE))
else:
    ApiResponse = ApiResponseFactory.JsonResponse(
        obj_constraint_Save_Info(OBJ_CONST_TYPE, OBJ_API_NAME, MODE, OBJ_FIELD_NAME, OBJ_REC_ID)
    )
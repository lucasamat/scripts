# =========================================================================================================================================
#   __script_name : SYCLONEALL.PY
#   __script_description : THIS SCRIPT IS USED TO OPEN A POPUP FOR VIEW/EDIT RECORDS IN RELATED LIST FOR ALL THE TABS DYNAMICALLY.
#   __primary_author__ : JOE EBENEZER
#   __create_date :
#   Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
from SYDATABASE import SQL
import Webcom.Configurator.Scripting.Test.TestProduct
Sql = SQL()


def POPUPCLONEVALUE(LABLE, VALUE, TABLEID, OPERATION, RECORDID, RECORDFEILD, RETURN, NEWVALUE, LOOKUPOBJ):
    # Param variable and variable decliration.
    api_name = ""
    sec_str = ""
    texts = ""
    col = ""
    tot_names = ""
    btn2 = "SAVE"
    func2 = "popup_cont_SAVE(this)"
    func1 = '<button type="button" class="btnconfig" onclick="popup_cont_VIEW();">CANCEL</button>'
    func4 = ""
    date_field = []

    # Param variable re-formation and geting the object name from table.
    primary_value = RECORDID
    primary_field = RECORDFEILD
    RECORDID = RECORDID.split("-")
    custom_table = RECORDID[0]
    RECORDFEILD = RECORDFEILD.split("_")
    RECORDFEILD = RECORDFEILD[1] + "-" + RECORDFEILD[2] + "-" + RECORDFEILD[3]
    lable = list(LABLE)[1]
    value = list(VALUE)[1]
    TABLEID = TABLEID.split("__")
    table = TABLEID[1]
    table = table.split("_")
    table1 = table[2] + "-" + table[3]
    popup_table_id = table[0] + "-" + table[1]
    popup_lable_obj = Sql.GetFirst(
        "SELECT CAN_EDIT, CAN_DELETE, NAME FROM SYOBJR WHERE RECORD_ID='" + str(popup_table_id) + "'"
    )
    if popup_lable_obj is not None:
        canedit = str(popup_lable_obj.CAN_EDIT)
        candelete = str(popup_lable_obj.CAN_DELETE)
    Question_obj = Sql.GetFirst("SELECT OBJECT_NAME, LABEL FROM SYOBJH WHERE RECORD_ID='" + str(table1) + "'")
    rec_field = Sql.GetFirst("SELECT API_NAME,API_NAME FROM SYSEFL WHERE RECORD_ID='" + str(RECORDFEILD) + "'")
    record_field = str(eval("rec_field.API_NAME"))
    record_value = str(eval("rec_field.API_NAME"))
    api_obj = Sql.GetList("select DATA_TYPE,API_NAME from  SYOBJD WHERE OBJECT_NAME='" + str(record_value).strip() + "'")
    api_list = [inn.API_NAME for inn in api_obj]

    # Date calculation changing date-time field to date field.
    for text in api_list:
        s = Sql.GetList(
            "select DATA_TYPE,API_NAME,LENGTH,DECIMALS from  SYOBJD WHERE API_NAME='"
            + str(text)
            + "' and OBJECT_NAME='"
            + str(record_value).strip()
            + "'"
        )
        for ins in s:
            if ins.DATA_TYPE == "DATE" or (ins.API_NAME == "EFFECTIVEDATE_END" or ins.API_NAME == "EFFECTIVEDATE_BEG"):
                if texts != "":
                    text = "CONVERT(VARCHAR(10)," + str(text) + ",101) AS [" + str(text) + "]"
                    texts = texts + "," + str(text)
                else:
                    text = "CONVERT(VARCHAR(10)," + str(text) + ",101) AS [" + str(text) + "]"
                    texts = str(text)
            else:
                if col != "":
                    col = col + "," + "[" + str(text) + "]"
                else:
                    col = "[" + str(text) + "]"
    if texts != "":
        col = col + "," + texts
    tot_names = col

    header_obj = Sql.GetFirst(
        "SELECT * FROM " + str(record_value) + " WHERE " + str(record_field) + "='" + str(primary_value) + "'"
    )

    # If object is nor empty proceed further.
    if Question_obj is not None:
        ObjectName = Question_obj.OBJECT_NAME.strip()
        Lable_obj = Sql.GetFirst(
            "SELECT API_NAME FROM  SYOBJD WHERE FIELD_LABEL='"
            + str(lable)
            + "' AND PARENT_OBJECT_RECORD_ID ='"
            + str(table1)
            + "' "
        )
        parent_api_name = eval(str("Lable_obj.API_NAME"))
        script = "SELECT * FROM " + str(ObjectName) + " WHERE " + str(parent_api_name) + " = '" + str(value) + "'"
        Custom_obj = Sql.GetFirst(script)
        Sqq_obj = Sql.GetList(
            "SELECT top 1000 API_NAME, DATA_TYPE, LOOKUP_OBJECT, REQUIRED, PERMISSION, FIELD_LABEL, LOOKUP_API_NAME FROM  SYOBJD WHERE OBJECT_NAME='"
            + str(ObjectName)
            + "' ORDER BY abs(DISPLAY_ORDER) "
        )
        lookup_val = [val.LOOKUP_API_NAME for val in Sqq_obj]
        lookup_list = {ins.LOOKUP_API_NAME: ins.LOOKUP_OBJECT for ins in Sqq_obj}
        new_value_dict = {}

        # Getting the formula field values with "SYPARCEFMA" Script.
        if NEWVALUE != "":
            if str(RETURN) == "CLEAR SELECTION":
                attrval_obj = Sql.GetFirst(
                    "SELECT API_NAME FROM  SYOBJD WHERE OBJECT_NAME='"
                    + str(ObjectName)
                    + "' AND LOOKUP_OBJECT='"
                    + str(NEWVALUE)
                    + "'"
                )
                api_name = attrval_obj.API_NAME.strip()
                TABLE_OBJS = Sql.GetList(
                    "select OBJECT_NAME,API_NAME,DATA_TYPE,LOOKUP_OBJECT,FORMULA_LOGIC FROM  SYOBJD where OBJECT_NAME ='"
                    + str(ObjectName)
                    + "' and FORMULA_LOGIC like '%"
                    + str(api_name)
                    + "%'"
                )
                if TABLE_OBJS is not None:
                    for TABLE_OBJ in TABLE_OBJS:
                        if TABLE_OBJ.DATA_TYPE != "":
                            DATA_TYPE = str(TABLE_OBJ.DATA_TYPE)

                            if api_name in str(TABLE_OBJ.FORMULA_LOGIC):
                                new_value_dict[str(TABLE_OBJ.API_NAME)] = ""
                                new_value_dict[str(api_name)] = ""
                #Trace.Write("eeeeeeeeeeeeeeeeeeeee" + str(dict(new_value_dict)))
            else:
                LOOKUPOBJ = LOOKUPOBJ.split("_")[1]
                attrval_obj = Sql.GetFirst(
                    "SELECT API_NAME FROM  SYOBJD WHERE OBJECT_NAME='"
                    + str(ObjectName)
                    + "' AND LOOKUP_OBJECT='"
                    + str(LOOKUPOBJ)
                    + "'"
                )
                api_name = attrval_obj.API_NAME.strip()
                NEWVALUE = NEWVALUE.split("|")
                result = ScriptExecutor.ExecuteGlobal(
                    "SYPARCEFMA", {"Object": str(ObjectName), "API_Name": api_name, "API_Value": NEWVALUE[0],},
                )
                new_value_dict = {API_Names["API_NAME"]: API_Names["FORMULA_RESULT"] for API_Names in result}

        # Table formation
        sec_str = (
            '<div   class="row modulebnr brdr">'
            + str(popup_lable_obj.NAME).upper()
            + " : "
            + str(OPERATION)
            + ' <button type="button"  class="fltrt close" data-dismiss="modal">X</button></div>'
        )
        sec_str += '<div class="col-md-12"><div class="row pad-10 bg-lt-wt brdr">'
        sec_str += func1
        if canedit.upper() == "TRUE":
            sec_str += (
                '<button type="button" id="'
                + str(ObjectName)
                + '" class="btnconfig " onclick="'
                + func2
                + '">'
                + btn2
                + "</button>"
            )
        # sec_str+='<button type="button" id="'+str(ObjectName)+'" class="btnstyle btn-block" onclick="'+func2+'">'+btn2+'</button>'
        sec_str += '</div></div><div class="mart_col_back" id="Headerbnr"  ></div>'
        sec_str += '<div id="container" class="g4 pad-10 brdr except_sec">'
        sec_str += '<table id="cloneTable"  class="ma_width_marg">'

        if Sqq_obj is not None:
            # For loading the popup form values.
            for val in Sqq_obj:
                current_object_apiname = val.API_NAME.strip()
                readonly_val = val.PERMISSION.strip()
                current_obj_field_lable = val.FIELD_LABEL.strip()
                data_type = val.DATA_TYPE.strip()
                current_object_value = ""
                header_object_value = ""
                readonly = ""
                disable = ""
                id_val = ""
                idval = ""
                ids = ""
                add_style = ""
                priceclass_val = ""
                datepicker = "onclick_datepicker('" + current_object_apiname + "')"
                datepicker_onchange = "onchangedatepicker('" + current_object_apiname + "')"

                if header_obj != "":
                    try:
                        header_object_value = eval(str("header_obj." + str(current_object_apiname)))
                    except:
                        Trace.Write("except" + str(current_object_value))

                if Custom_obj != "":
                    current_object_value = eval(str("Custom_obj." + str(current_object_apiname)))
                if current_object_apiname in lookup_val:
                    for key, value in lookup_list.items():
                        if key == current_object_apiname:
                            ids = value.strip()
                if readonly_val == "READ ONLY" or data_type == "AUTO NUMBER" or canedit.upper() == "FALSE":
                    edit_pencil_icon = '<i class="fa fa-lock" aria-hidden="true"></i>'
                    func4 = ""
                else:
                    edit_pencil_icon = '<i class="fa fa-pencil" aria-hidden="true"></i>'
                if data_type == "AUTO NUMBER":
                    sec_str += (
                        '<div class="col-md-12 het35pad0" style="display: none; "><div><label class="wth45fltposmin">'
                        + str(current_obj_field_lable)
                        + '</label><a href="#" class="col-md-1 txtcewth10"  ><i   class="fa fa-info-circle fltlt"></i>'
                    )
                    if val.REQUIRED == "TRUE" or val.REQUIRED == "1":
                        sec_str += '<span class="req-field mrg3fltltmt7"  >*</span>'
                    sec_str += "</a></div>"
                    sec_str += (
                        '<div class="pad-0"><input id="'
                        + str(current_object_apiname)
                        + '" type="text" class="form-control wthauthtmrgbt" hidden  readonly></div>'
                    )
                    sec_str += "</div>"
                if data_type != "AUTO NUMBER":
                    if data_type == "LOOKUP":
                        add_style = "display: none;"
                    sec_str += (
                        '<tr class="iconhvr borbot1" "  '
                        + str(add_style)
                        + '"><td class="width350"><label class="pad_l_mar_bot">'
                        + str(current_obj_field_lable)
                        + '</label></td><td class="width40"><a href="#" class="bgcccwth10" data-placement="top" data-toggle="popover" data-content="'
                        + str(current_obj_field_lable)
                        + '"  ><i   class="fa fa-info-circle fltlt"></i>'
                    )
                    if val.REQUIRED == "TRUE" or val.REQUIRED == "1":
                        sec_str += ""
                        # sec_str+='<span class="req-field mrg3fltltmt7"  >*</span>'
                    sec_str += "</a></td>"
                    if data_type == "LOOKUP":
                        sec_str += (
                            '<td><input id="'
                            + str(current_object_apiname)
                            + '" value="'
                            + str(current_object_value)
                            + '" type="text" class="form-control wthauthtmrgbt"   readonly></td>'
                        )
                    elif data_type == "FORMULA":
                        if header_object_value == "" and current_object_apiname in lookup_val:
                            sec_str += (
                                "<td><input id='"
                                + str(current_object_apiname)
                                + "' type='text' value='"
                                + str(current_object_value)
                                + "' class='form-control fllthtmrgbt'   readonly></td>"
                            )
                            sec_str += (
                                "<input class='popup fltmarg' id='"
                                + str(ids)
                                + "' onclick='cont_lookup_popup_clone(this)'   type='image'  src='../mt/default/images/customer_lookup.gif'>"
                            )
                        else:
                            sec_str += (
                                "<td><input id='"
                                + str(current_object_apiname)
                                + "' type='text' value='"
                                + str(current_object_value)
                                + "' class='form-control wthauthtmrgbt'  readonly></td>"
                            )
                    elif data_type == "CHECKBOX":
                        sec_str += (
                            '<td><input id="'
                            + str(current_object_apiname)
                            + '" value="'
                            + str(current_object_value)
                            + '" type="'
                            + str(data_type)
                            + '" class="form-control wthautomarg"   '
                            + disable
                            + " ></td>"
                        )

                    elif data_type == "DATE":
                        date_field.append(current_object_apiname)
                        # sec_str+= '<td><input value="'+ current_obj_value +'" type="text" class="form-control"   '+disable+' ><span id="'+str(current_obj_api_name)+'" value="'+ current_obj_value +'"   class="input-group-addon" onclick="'+str(datepicker)+'"><i class="glyphicon glyphicon-calendar"></i></span></td>'
                        sec_str += (
                            '<td><input id="'
                            + str(current_object_apiname)
                            + '" value="'
                            + str(current_object_value)
                            + '" type="text"  onclick="'
                            + str(datepicker)
                            + '" onchange="'
                            + str(datepicker_onchange)
                            + '" class="form-control datePickerField wth157fltltbrdbt"   '
                            + disable
                            + " ></td>"
                        )
                    else:
                        sec_str += (
                            '<td><input id="'
                            + str(current_object_apiname)
                            + '" value="'
                            + str(current_object_value)
                            + '" type="text" class="form-control wthauthtmrgbt"   '
                            + readonly
                            + "></td>"
                        )

                    if canedit.upper() == "TRUE":
                        sec_str += (
                            '<td class="float_r_bor_bot"><div class="col-md-12 editiconright"><a href="#" onclick="'
                            + func4
                            + '" class="editclick">'
                            + str(edit_pencil_icon)
                            + "</i></a></div></td>"
                        )
                    else:
                        sec_str += (
                            '<td class="float_r_bor_bot"><div class="col-md-12 editiconright"><a href="#" onclick="" class="editclick">'
                            + str(edit_pencil_icon)
                            + "</a></div></td>"
                        )

                    sec_str += "</tr>"
            sec_str += "</table>"
            sec_str += "</div>"
    else:
        sec_str += '<div class="txt_center">No matching records found </div><div class="modal-footer"><button type="button" class="btnstyle fltrt"   data-dismiss="modal">Close</button></div>'
    return sec_str, date_field, new_value_dict, api_name


# Param Variables.
LABLE = Param.LABLE
VALUE = Param.VALUE
TABLEID = Param.TABLEID
OPERATION = Param.OPERATION
RETURN = Param.RETURN
RECORDID = Param.RECORDID
RECORDFEILD = Param.RECORDFEILD
NEWVALUE = Param.NEWVALUE
LOOKUPOBJ = Param.LOOKUPOBJ
ApiResponse = ApiResponseFactory.JsonResponse(
    POPUPCLONEVALUE(LABLE, VALUE, TABLEID, OPERATION, RECORDID, RECORDFEILD, RETURN, NEWVALUE, LOOKUPOBJ,)
)
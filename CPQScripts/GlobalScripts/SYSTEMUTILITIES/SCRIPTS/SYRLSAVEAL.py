# =========================================================================================================================================
#   __script_name : SYRLSAVEAL.PY
#   __script_description :  THIS SCRIPT IS USED TO GET THE VALUES FOR THE POPUP FROM LIST GRID DURING EDIT FOR CONTAINERS WITHOUT A TAB
#   __primary_author__ : JOE EBENEZER
#   __create_date :
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
from SYDATABASE import SQL
import Webcom.Configurator.Scripting.Test.TestProduct

Sql = SQL()


def POPUPLISTVALUE(VALUE, TABLEID, OPERATION, RETURN, IDVALUE, LOOKUPOBJ):
    func2 = "cont_relatedlist_openedit(this)"
    btn3 = "DELETE"
    func4 = "cont_relatedlist_openedit(this)"
    func3 = "cont_relatedlist_DELETE(this)"
    if RETURN == "EDIT":
        func1 = '<button type="button" class="btnconfig" data-dismiss="modal">CANCEL</button>'
    readonly = "readonly"
    disable = "disabled"
    value = VALUE
    sec_str = ""
    header_obj = ""
    candelete = ""
    canedit = ""
    api_name = ""
    record_field = ""
    new_value_dict = {}
    Lock_val = "FALSE"

    Trace.Write("The value of VALUE is here " + str(VALUE))
    Trace.Write("The value of TABLEID is here " + str(TABLEID))
    Trace.Write("The value of OPERATION is here " + str(OPERATION))
    Trace.Write("The value of RETURN is here " + str(RETURN))
    Trace.Write("The value of IDVALUE is here " + str(IDVALUE))
    if RETURN == "1":
        attrval_obj = Sql.GetFirst(
            "SELECT API_NAME FROM  SYOBJD WHERE OBJECT_NAME='"
            + str(TABLEID)
            + "' AND LOOKUP_OBJECT='"
            + str(LOOKUPOBJ)
            + "'"
        )
        api_name = attrval_obj.API_NAME.strip()
        IDVALUE = IDVALUE.split("|")
        result = ScriptExecutor.ExecuteGlobal(
            "SYPARCEFMA", {"Object": str(TABLEID), "API_Name": api_name, "API_Value": IDVALUE[0]},
        )
        new_value_dict = {API_Names["API_NAME"]: API_Names["FORMULA_RESULT"] for API_Names in result}
    
    Question_obj = Sql.GetFirst(
        "SELECT RECORD_ID, RECORD_NAME, LABEL FROM SYOBJH WHERE OBJECT_NAME='" + str(TABLEID).strip() + "'"
    )
    record_field = str(eval("Question_obj.RECORD_NAME"))
    record_id = str(eval("Question_obj.RECORD_ID"))
    
    popup_lable_obj = Sql.GetFirst(
        " SELECT RECORD_ID, CAN_EDIT, NAME, CAN_DELETE FROM SYOBJR WHERE OBJ_REC_ID='"
        + str(record_id).strip()
        + "' AND VISIBLE = 1 "
    )
    if popup_lable_obj is not None:
        canedit = str(popup_lable_obj.CAN_EDIT)
        candelete = str(popup_lable_obj.CAN_DELETE)

        if canedit == 0:
            canedit = "FALSE"
            func4 = ""
        elif canedit == 1:
            canedit = "TRUE"
    if str(TABLEID) == "PAPBEN":
        func4 = ""
        right_icon = '<i class="fa fa-lock" aria-hidden="true"></i>'
    else:
        right_icon = '<i class="fa fa-pencil" aria-hidden="true"></i>'
    if Question_obj is not None:
        

        texts1 = ""
        tot_names1 = ""
        col1 = ""

        api_obj1 = Sql.GetList("select DATA_TYPE,API_NAME from  SYOBJD WHERE OBJECT_NAME='" + str(TABLEID).strip() + "'")
        api_list1 = [inn.API_NAME for inn in api_obj1]

        for text1 in api_list1:
            s1 = Sql.GetList(
                "select DATA_TYPE,API_NAME,LENGTH,DECIMALS from  SYOBJD WHERE API_NAME='"
                + str(text1)
                + "' and OBJECT_NAME='"
                + str(TABLEID).strip()
                + "'"
            )
            for ins in s1:
                if ins.DATA_TYPE == "DATE" or (
                    (ins.API_NAME == "EFFECTIVEDATE_BEG" or ins.API_NAME == "EFFECTIVEDATE_END")
                    and TABLEID.strip() == "PRLPBK"
                ):
                    if texts1 != "":
                        text1 = "CONVERT(VARCHAR(10)," + str(text1) + ",101) AS [" + str(text1) + "]"
                        texts1 = texts1 + "," + str(text1)
                    else:
                        text1 = "CONVERT(VARCHAR(10)," + str(text1) + ",101) AS [" + str(text1) + "]"
                        texts1 = str(text1)
                else:
                    if col1 != "":
                        col1 = col1 + "," + "[" + str(text1) + "]"
                    else:
                        col1 = "[" + str(text1) + "]"
        if texts1 != "":
            col1 = col1 + "," + texts1
        tot_names1 = col1
        
        script = (
            "SELECT "
            + str(tot_names1)
            + " FROM "
            + str(TABLEID).strip()
            + " WHERE "
            + str(record_field)
            + "='"
            + str(value)
            + "'"
        )
        Custom_obj = Sql.GetFirst(script)
        Lock_val = "FALSE"

        Sqq_obj = Sql.GetList(
            "SELECT top 1000 API_NAME, DATA_TYPE, LOOKUP_OBJECT, PERMISSION, REQUIRED, LOOKUP_API_NAME, FIELD_LABEL FROM  SYOBJD WHERE OBJECT_NAME='"
            + str(TABLEID).strip()
            + "' ORDER BY abs(DISPLAY_ORDER)"
        )
        lookup_val = [val.LOOKUP_API_NAME for val in Sqq_obj]
        lookup_list = {ins.LOOKUP_API_NAME: ins.LOOKUP_OBJECT for ins in Sqq_obj}
        sec_str = (
            '<div   class="row modulebnr brdr">'
            + str(Question_obj.LABEL).upper()
            + " : "
            + str(OPERATION)
            + ' <button type="button" class="close fltrt" data-dismiss="modal">X</button></div>'
        )
        sec_str += '<div id="container" class="g4 pad-10 brdr except_sec">'
        sec_str += '<div class="row pad-10 bg-lt-wt brdr">'
        sec_str += func1
        
        if canedit == "TRUE" and Lock_val.upper() != "TRUE":
            sec_str += (
                '<button type="button" id="'
                + str(VALUE)
                + "|"
                + str(TABLEID).strip()
                + '" class="btnconfig" onclick="'
                + func2
                + '">'
                + btn1
                + "</button>"
            )

        sec_str += "</div>"
        sec_str += '<table  class="ma_width_marg">'
        if Sqq_obj is not None and Custom_obj is not None:
            for val in Sqq_obj:
                nam = val.API_NAME.strip()
                ids = ""
                add_style = ""
                idval = ""
                id_val = ""
                priceclass_val = ""
                if nam in lookup_val:
                    for key, value in lookup_list.items():
                        
                        if key == nam:
                            ids = value.strip()
                
                lab = val.FIELD_LABEL.strip()
                readonly_val = val.PERMISSION.strip()
                if readonly_val != "READ ONLY" and OPERATION == "EDIT":
                    readonly = ""
                    disable = ""
                data_type = val.DATA_TYPE
                res = ""
                sec = ""
                if data_type == "LOOKUP":
                    add_style = "display: none;"
                if header_obj != "":
                    try:
                        sec = eval(str("header_obj." + str(nam)))
                        
                    except:
                        Trace.Write("except" + str(res))
                if Custom_obj != "":
                    try:
                        res = eval(str("Custom_obj." + str(nam)))
                        
                    except:
                        Trace.Write("except" + str(res))

                sec_str += (
                    '<tr class="iconhvr brdbt" style="'
                    + str(add_style)
                    + '"><td class="wth350"><label class="fltltpadltpos">'
                    + str(lab)
                    + '</label></td><td class="wth40"><a href="#" class="bgcccwth10" data-placement="top" data-toggle="popover" data-content="'
                    + str(lab)
                    + '"  ><i   class="fa fa-info-circle fltlt"></i>'
                )
                if val.REQUIRED.upper() == "TRUE" or val.REQUIRED == "1":
                    sec_str += ""
                    # sec_str+='<span class="req-field" >*</span>'
                sec_str += "</a></td>"
                if data_type == "AUTO NUMBER":
                    sec_str += (
                        '<td><input id="'
                        + str(nam)
                        + '" type="text" value="'
                        + str(res)
                        + '" class="form-control wth184"   disabled></td>'
                    )
                elif data_type == "LOOKUP":
                    sec_str += (
                        '<td><input id="'
                        + str(nam)
                        + '" type="text" value="'
                        + str(res)
                        + '" class="form-control wth184"   disabled></td>'
                    )
                elif data_type == "FORMULA" and OPERATION == "EDIT":
                    if sec == "" and nam in lookup_val and readonly != "readonly":
                        sec_str += (
                            '<td><input id="'
                            + str(nam)
                            + '" type="text" value="'
                            + str(res)
                            + '" class="form-control fltltbgyellow"  readonly>'
                        )
                        sec_str += (
                            '<input class="popup fltlt" id="'
                            + str(ids)
                            + '" onclick="cont_lookup_popup_relatedlist(this)"   type="image"  src="../mt/default/images/customer_lookup.gif"></td>'
                        )
                    else:
                        sec_str += (
                            '<td><input id="'
                            + str(nam)
                            + '" type="text" value="'
                            + str(res)
                            + '" class="form-control wth184fltlt"   disabled></td>'
                        )
                elif data_type == "CHECKBOX":
                    if str(res) == "True" or str(res) == "1":
                        
                        sec_str += (
                            '<td><input id="'
                            + str(nam)
                            + '" type="'
                            + str(data_type)
                            + '" value="'
                            + str(res)
                            + '" class="custom" '
                            + disable
                            + ' checked><span class="lbl"></span></td>'
                        )
                    else:
                        
                        sec_str += (
                            '<td><input id="'
                            + str(nam)
                            + '" type="'
                            + str(data_type)
                            + '" value="'
                            + str(res)
                            + '" class="custom" '
                            + disable
                            + '><span class="lbl"></span></td>'
                        )
                elif data_type == "PICKLIST":
                    if popup_lable_obj.NAME == "AVAILABLE FULFILLMENT COUNTRIES FOR MATERIAL":
                        # Log.Info("12345 nam ---->"+str(nam))
                        # Log.Info("12345 res ---->"+str(res))
                        if str(nam) == "COUNTRIES":
                            Sql_Countries = Sql.GetList("select COUNTRY_NAME FROM SACTRY where COUNTRY_NAME != ''")
                            Check_Country = 0
                            Countries_List = []
                            for cont in Sql_Countries:
                                Check_Country = 1
                                Countries_List.append(cont.COUNTRY_NAME)
                            if len(Countries_List) != 0:
                                Countries_List.insert(0, "ALL COUNTRIES")
                            sec_str += (
                                '<td class="posrelclr555" onclick="showCheckboxes()"><select id="select_id" value="'
                                + str(res)
                                + '" type="text" class="form-control wth184fltlt"   '
                                + disable
                                + ' > "add" </select><input id="'
                                + str(nam)
                                + '"  class="inp_val" type="text" '
                                + disable
                                + "/>"
                            )
                            sec_str += '<div id="checkboxes" class="posabltovtp" style="display: none;">'
                            Selected_Countries = Sql.GetFirst(
                                "select INC_COUNTRY_TEMPLATES,COUNTRIES FROM MAMAFC where MATERIAL_FULFILLMENT_COUNTRY_RECORD_ID = '"
                                + str(MATE_FULFILLMENT_COUNTRY_REC_ID)
                                + "'"
                            )
                            Selected_Countries_List = (Selected_Countries.COUNTRIES).split(",")
                            # Log.Info("61616161 COUNTRIES COUNTRIES---->" + str(Selected_Countries_List))
                            # Log.Info("61616161 Selected_Countries.COUNTRIES ------>" + str(type(Selected_Countries_List)))
                            if "ALL COUNTRIES" not in Selected_Countries_List:
                                for req in Countries_List:
                                    if str(req).upper() in Selected_Countries_List:
                                        sec_str += (
                                            '<label><input checked = "checked" type="checkbox" onchange="labelDropdown(this)" class="'
                                            + str(req).upper()
                                            + '" />'
                                            + str(req).upper()
                                            + "</label>"
                                        )
                                    else:
                                        sec_str += (
                                            '<label><input  type="checkbox" onchange="labelDropdown(this)" class="'
                                            + str(req).upper()
                                            + '" />'
                                            + str(req).upper()
                                            + "</label>"
                                        )
                            else:
                                for req in Countries_List:
                                    sec_str += (
                                        '<label><input  checked = "checked" type="checkbox" onchange="labelDropdown(this)" class="'
                                        + str(req).upper()
                                        + '" />'
                                        + str(req).upper()
                                        + "</label>"
                                    )
                            sec_str += "</div></td>"

                    elif popup_lable_obj.NAME == "EMBLEM QUANTITY FACTORS IN SET":
                        sec_str += (
                            '<td><select id="'
                            + str(nam)
                            + '" value="'
                            + str(res)
                            + '" type="text" class="form-control wth184fltlt"   '
                            + disable
                            + " >"
                        )
                        Sql_Quality_Tier = Sql.GetFirst(
                            "select PICKLIST_VALUES FROM  SYOBJD where OBJECT_NAME='MAEMQF' and DATA_TYPE='PICKLIST'"
                        )
                        Tier_List = (Sql_Quality_Tier.PICKLIST_VALUES).split(",")
                        for req1 in Tier_List:
                            sec_str += "<option>" + str(req1) + "</option>"
                        sec_str += "</select></td>"
                    elif popup_lable_obj.NAME == "AVAILABLE PROMOTIONS IN SALES ORG":
                        sec_str += (
                            '<td><select id="'
                            + str(nam)
                            + '" value="'
                            + str(res)
                            + '" type="text" class="form-control wth184fltlt"  '
                            + disable
                            + " >"
                        )

                        Sql_Quality_Tier = Sql.GetFirst(
                            "select PICKLIST_VALUES FROM  SYOBJD where OBJECT_NAME='SASOPM' and DATA_TYPE='PICKLIST'"
                        )

                        Tier_List = (Sql_Quality_Tier.PICKLIST_VALUES).split(",")
                        for req1 in Tier_List:
                            sec_str += "<option>" + str(req1) + "</option>"
                        sec_str += "</select></td>"
                    else:
                        sec_str += (
                            '<td><select id="'
                            + str(nam)
                            + '" value="'
                            + str(res)
                            + '" type="text" class="form-control pop_up_brd_rad wth184fltlt"   '
                            + disable
                            + " >"
                        )
                        Sql_Quality_Tier = Sql.GetFirst(
                            "select PICKLIST_VALUES FROM  SYOBJD where OBJECT_NAME='"
                            + str(TABLEID).strip()
                            + "' and DATA_TYPE='PICKLIST' and API_NAME = '"
                            + str(nam)
                            + "' "
                        )
                        Tier_List = (Sql_Quality_Tier.PICKLIST_VALUES).split(",")
                        for req1 in Tier_List:
                            sec_str += "<option>" + str(req1) + "</option>"
                        sec_str += "</select></td>"
                elif data_type == "DATE" and OPERATION == "EDIT":
                    sec_str += (
                        '<td><input id="'
                        + str(nam)
                        + '" value="'
                        + str(res)
                        + '" type="text" class="form-control wth155flrt"   '
                        + disable
                        + ' ><span  class="input-group-addon pad4wth0" onclick="'
                        + str(datepicker)
                        + '"><i class="glyphicon glyphicon-calendar"></i></span></td>'
                    )
                elif data_type == "NUMBER":
                    sec_str += (
                        '<td><input id="'
                        + str(nam)
                        + '" type="number" value="'
                        + str(res)
                        + '" class="form-control wth184"  '
                        + disable
                        + "></td>"
                    )
                else:
                    sec_str += (
                        '<td><input id="'
                        + str(nam)
                        + '" type="text" value="'
                        + str(res)
                        + '" class="form-control wth184"  '
                        + disable
                        + "></td>"
                    )
                sec_str += (
                    '<td class="float_r_bor_bot"><div class="col-md-12 editiconright"><a href="#" id="'
                    + str(VALUE)
                    + "|"
                    + str(TABLEID).strip()
                    + '" onclick="'
                    + str(func4)
                    + '" class="editclick">'
                    + str(right_icon)
                    + "</a></div></td>"
                )
                sec_str += "</tr>"
        sec_str += "</table>"
        sec_str += "</div>"
    else:
        sec_str += '<div class="txt_center">No matching records found </div><div class="modal-footer"><button type="button" class="btnconfig fltrt"  data-dismiss="modal">Close</button></div>'
    return sec_str, new_value_dict, api_name


VALUE = Param.VALUE
TABLEID = Param.TABLEID
OPERATION = Param.OPERATION
IDVALUE = Param.IDVALUE
RETURN = Param.RETURN
LOOKUPOBJ = Param.LOOKUPOBJ
if LOOKUPOBJ is not None and LOOKUPOBJ != "":
    LOOKUPOBJ = LOOKUPOBJ.split("_")[1]
ApiResponse = ApiResponseFactory.JsonResponse(POPUPLISTVALUE(VALUE, TABLEID, OPERATION, RETURN, IDVALUE, LOOKUPOBJ))


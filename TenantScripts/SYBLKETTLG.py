# =========================================================================================================================================
#   __script_name : SYBLKETTLG.PY
#   __script_description : THIS SCRIPT IS USED FOR BULK EDITING IN NESTED LIST GRIDS SUCH AS THE PRICE CLASSES LIST GRID.
#   __primary_author__ : JOE EBENEZER
#   __create_date :
# ==========================================================================================================================================
import SYTABACTIN as Table
import Webcom.Configurator.Scripting.Test.TestProduct
from SYDATABASE import SQL

Sql = SQL()


def RELATEDMULTISELECTONEDIT(TITLE, VALUE, CLICKEDID, RECORDID):
   
    clicked = CLICKEDID.split("_")
    obj_id = clicked[2] + "-" + clicked[3]
    objr_id = clicked[0] + "-" + clicked[1]
    edt_str = ""
    checked = ""
    data_type = ""
    pricbkst_lock = "FALSE"
    pricbk_lock = "FALSE"
    date_field = []
    VALUE = remove_html_tags(VALUE)
    RECORDID = list(RECORDID)
    if None in RECORDID:
        RECORDID.remove(None)
    if "" in RECORDID:
        RECORDID.remove("")
    rec_ids = ",".join(RECORDID)
    
    Product.SetGlobal("RecordList", str(list(RECORDID)))
    objh_obj = Sql.GetFirst("select OBJECT_NAME,RECORD_ID from SYOBJH where SAPCPQ_ATTRIBUTE_NAME = '" + str(obj_id) + "'")
    if objh_obj:
        obj_id = objh_obj.RECORD_ID
    objr_obj = Sql.GetFirst("select CAN_EDIT from SYOBJS where OBJ_REC_ID = '" + str(obj_id) + "' and NAME='Tab list'")
    canedit = str(objr_obj.CAN_EDIT)
    
    if objh_obj is not None and str(canedit).upper() == "TRUE":
        obj_obj = str(objh_obj.OBJECT_NAME)

        objd_obj = Sql.GetFirst(
            "SELECT DATA_TYPE,PICKLIST_VALUES,API_NAME,FIELD_LABEL,PERMISSION,FORMULA_DATA_TYPE FROM  SYOBJD where OBJECT_NAME='"
            + str(obj_obj)
            + "' and API_NAME='"
            + str(TITLE).replace("X__DEFAULT_LOWPRCADJ_FACTOR", "DEFAULT_LOWPRCADJ_FACTOR")
            + "'"
        )
        if objd_obj is not None and pricbkst_lock.upper() == "FALSE" and pricbk_lock.upper() == "FALSE":
            
            data_type = str(objd_obj.DATA_TYPE).strip()
            api_name = str(objd_obj.API_NAME).strip()
            Permission = str(objd_obj.PERMISSION).strip()
            formula_data_type = str(objd_obj.FORMULA_DATA_TYPE).strip()

            if (
                (data_type == "FORMULA" and (formula_data_type.upper() == "TEXT" or formula_data_type.upper() == "NUMBER"))
                and data_type != "LOOKUP"
                and data_type != "AUTO NUMBER"
                and data_type != ""
                and Permission != "READ ONLY"
            ):

                pick_val = str(objd_obj.PICKLIST_VALUES)
                field_lable = str(objd_obj.FIELD_LABEL)
                datepicker = "onclick_datepicker('" + api_name + "')"
                edt_str += (
                    '<div   class="row modulebnr brdr">EDIT '
                    + str(field_lable).upper()
                    + ' <button type="button" class="close fltrt" onclick="multiedit_cancel();">X</button></div>'
                )
                edt_str += '<div id="container" class="g4 pad-10 brdr except_sec padbt0" >'
                edt_str += '<table class="wdth100" id="bulk_edit">'
                edt_str += (
                    '<tbody><tr class="fieldRow"><td  class="labelCol wdt22posreltextcen">'
                    + str(field_lable)
                    + '</td><td class="dataCol"><div id="massEditFieldDiv" class="inlineEditRequiredDiv">'
                )
                if len(list(RECORDID)) > 1:
                    if data_type.upper() == "TEXT":
                        edt_str += '<input class="form-control wdth44"  id="' + str(api_name) + '" type="text">'
                    elif data_type.upper() == "NUMBER":
                        edt_str += '<input class="form-control wdth44" id="' + str(api_name) + '" type="number">'
                    elif data_type.upper() == "CHECKBOX":
                        edt_str += (
                            '<input class="custom wdth44" id="'
                            + str(api_name)
                            + '" type="checkbox"><span class="lbl"></span>'
                        )
                    elif data_type.upper() == "PICKLIST":
                        if obj_obj == "MAMAFC":
                            Sql_Countries = Sql.GetList("select COUNTRY_NAME FROM SACTRY where COUNTRY_NAME != ''")
                            Check_Country = 0
                            Countries_List = []
                            for cont in Sql_Countries:
                                Check_Country = 1
                                Countries_List.append(cont.COUNTRY_NAME)
                            if len(Countries_List) != 0:
                                Countries_List.insert(0, "ALL COUNTRIES")
                            edt_str += '<select id="select_id" onclick="showCheckboxes()" type="text" class="form-control wth184hte32" > "add" </select>'
                            edt_str += '<input id="' + str(api_name) + '"  class="inp_val bgclrfff" disabled type="text"/>'
                            edt_str += '<div id="checkboxes" class="lft249zinpos" style="display: none; ;">'
                            for req in Countries_List:
                                edt_str += (
                                    '<label><input type="checkbox" onchange="labelDropdown(this)" class="'
                                    + str(req).upper()
                                    + '" />'
                                    + str(req).upper()
                                    + "</label>"
                                )
                        else:
                            edt_str += '<select class="form-control light_yellow wth150"   id="' + str(api_name) + '">'
                            pick_val = pick_val.split(",")
                            for value in pick_val:
                                edt_str += "<option>" + str(value) + "</option>"
                            edt_str += "</select>"
                    elif data_type.upper() == "DATE":
                        date_field.append(api_name)
                        edt_str += (
                            '<input id="'
                            + str(api_name)
                            + '" type="text" class="form-control wth155hit26"><span   class="input-group-addon pad4wth0" onclick="'
                            + str(datepicker)
                            + '"><i class="glyphicon glyphicon-calendar"></i></span>'
                        )
                    else:
                        edt_str += '<input class="form-control wdth44" id="' + str(api_name) + '" type="text">'
                    edt_str += '</div></td></tr><tr class="selectionRow">'
                    edt_str += (
                        '<td  class="labelCol wth50txtcein">Apply changes to</td><td class="dataCol"><div class="radio"><input type="radio" name="massOrSingleEdit" id="singleEditRadio" checked="checked"><label for="singleEditRadio">The record clicked</label></div><div class="radio"><input type="radio" name="massOrSingleEdit" id="massEditRadio"><label for="massEditRadio">All '
                        + str(len(list(RECORDID)))
                        + " selected records</label>"
                    )
                else:
                    if data_type.upper() == "TEXT":
                        edt_str += (
                            '<input class="form-control wdth44" id="'
                            + str(api_name)
                            + '" type="text" value="'
                            + str(VALUE)
                            + '">'
                        )
                    elif data_type.upper() == "NUMBER":
                        edt_str += (
                            '<input class="form-control wdth44" id="'
                            + str(api_name)
                            + '" value="'
                            + str(VALUE)
                            + '" type="number">'
                        )
                    elif data_type.upper() == "CHECKBOX":
                        if str(VALUE).upper() == "TRUE":
                            checked = "checked"
                        edt_str += (
                            '<input class="custom wdth44" id="'
                            + str(api_name)
                            + '" type="checkbox" '
                            + str(checked)
                            + '><span class="lbl"></span>'
                        )
                    elif data_type.upper() == "PICKLIST":
                        if obj_obj == "MAMAFC":
                            Sql_Countries = Sql.GetList("select COUNTRY_NAME FROM SACTRY where COUNTRY_NAME != ''")
                            Check_Country = 0
                            Countries_List = []
                            for cont in Sql_Countries:
                                Check_Country = 1
                                Countries_List.append(cont.COUNTRY_NAME)
                            if len(Countries_List) != 0:
                                Countries_List.insert(0, "ALL COUNTRIES")
                            Selected_Countries = Sql.GetFirst(
                                "select INC_COUNTRY_TEMPLATES,MATERIAL_RECORD_ID,FULCTY_RECORD_I FROM MAMAFC where MATERIAL_FULFILLMENT_COUNTRY_RECORD_ID = '"
                                + str(rec_ids)
                                + "' "
                            )
                            mat_rec_id = str(Selected_Countries.MATERIAL_RECORD_ID)
                            coun_rec_id = str(Selected_Countries.FULCTY_RECORD_I)
                            countries_qry = Sql.GetList(
                                "select COUNTRY_FULLNAME FROM MAINCY where upper(INCCTYTMP_ID) = '"
                                + str(Selected_Countries.INC_COUNTRY_TEMPLATES).upper()
                                + "' "
                            )
                            countries_list = [icc.COUNTRY_FULLNAME.upper() for icc in countries_qry]
                            Sel_Coun_qry = Sql.GetList(
                                "select COUNTRIES FROM MAMAFC where MATERIAL_RECORD_ID = '"
                                + str(mat_rec_id)
                                + "' and FULCTY_RECORD_I = '"
                                + str(coun_rec_id)
                                + "'"
                            )
                            Selected_Countries_List = [ins.COUNTRIES for ins in Sel_Coun_qry]
                            Selected_Countries_str = ",".join(Selected_Countries_List)
                           
                            edt_str += '<select id="select_id" onclick="showCheckboxes()" type="text" class="form-control wth184hte32"  > "add" </select>'
                            edt_str += (
                                '<input id="'
                                + str(api_name)
                                + '" value="'
                                + str(Selected_Countries_str)
                                + '"  class="inp_val bgclrfff" disabled type="text"/>'
                            )
                            edt_str += '<div id="checkboxes" class="poslefovehei" style="display: none; ">'
                            for req in Countries_List:
                                if str(req).upper() in Selected_Countries_List:
                                    edt_str += (
                                        '<label><input checked = "checked" type="checkbox" onchange="labelDropdownRL(this)" class="'
                                        + str(req).upper()
                                        + '" />'
                                        + str(req).upper()
                                        + "</label>"
                                    )
                                else:
                                    edt_str += (
                                        '<label><input  type="checkbox" onchange="labelDropdownRL(this)" class="'
                                        + str(req).upper()
                                        + '" />'
                                        + str(req).upper()
                                        + "</label>"
                                    )
                        else:
                            edt_str += '<select class="form-control light_yellow wth150"  id="' + str(api_name) + '">'
                            pick_val = pick_val.split(",")
                            for value in pick_val:
                                edt_str += "<option>" + str(value) + "</option>"
                            edt_str += "</select>"
                    elif data_type.upper() == "DATE":
                        date_field.append(api_name)
                        edt_str += (
                            '<input id="'
                            + str(api_name)
                            + '" type="text" value="'
                            + str(VALUE)
                            + '" class="form-control wth155hit26"><span   class="input-group-addon pad4wth0" onclick="'
                            + str(datepicker)
                            + '"><i class="glyphicon glyphicon-calendar"></i></span>'
                        )
                    else:
                        edt_str += (
                            '<input class="form-control wdth44" id="'
                            + str(api_name)
                            + '" type="text" value="'
                            + str(VALUE)
                            + '">'
                        )
                edt_str += "</div></td></tr></tbody></table>"
                edt_str += '<div class="row pad-10"><button class="btnstyle mrg-rt-8 btn fltrt"  onclick="multiedit_RL_cancel();" type="button" value="Cancel" id="cancelButton">CANCEL</button><button class="btnstyle mrg-rt-8 btn fltrt"  type="button" value="Save" onclick="multiedit_save()" id="saveButton">SAVE</button></div></div>'
            else:
                edt_str = "NO"
        else:
            edt_str = "NO"
    else:
        edt_str = "NO"
    return edt_str, date_field


def remove_html_tags(text):
    """Remove html tags from a string"""
    import re

    clean = re.compile("<.*?>")
    return re.sub(clean, "", text)


def RELATEDMULTISELECTONSAVE(TITLE, VALUE, CLICKEDID, RECORDID):
    TestProduct = Webcom.Configurator.Scripting.Test.TestProduct()
    current_tab = str(TestProduct.CurrentTab)
    
    selected_rows = RECORDID.split(",")
    if str(CLICKEDID) != "" and str(CLICKEDID) is not None:
        clicked = CLICKEDID.split("_")
        obj_id = clicked[2] + "-" + clicked[3]

    else:
        if str(current_tab) == "Price Classes":
            obj_id = "SYOBJ-00032"

    edt_str = ""
    checked = ""
    date_field = []
    objh_obj = Sql.GetFirst("select OBJECT_NAME, RECORD_NAME from SYOBJH where RECORD_ID = '" + str(obj_id) + "'")
    if objh_obj is not None:
        obj_name = str(objh_obj.OBJECT_NAME)
        objh_head = str(objh_obj.RECORD_NAME)
        
        if obj_name == "MAMAFC":
            where = ""
            if len(selected_rows) > 1:
                where = " in " + str(tuple(selected_rows))
            else:
                where = "='" + str(RECORDID) + "' "
            value_list = VALUE.split(",")
            obj_val = Sql.GetList(
                "select FULCTY_RECORD_ID, MATERIAL_RECORD_ID,INC_COUNTRY_TEMPLATES,SAP_PART_NUMBER from MAMAFC where MATERIAL_FULFILLMENT_COUNTRY_RECORD_ID "
                + str(where)
                + " "
            )
            
            for inc in obj_val:
                row = {}
                inc_coun_temp = str(inc.INC_COUNTRY_TEMPLATES)
                mat_rec_id = str(inc.MATERIAL_RECORD_ID)
                coun_rec_id = str(inc.FULCTY_FULLNAME)
                sap_num = str(inc.SAP_PART_NUMBER)
                
                all_id_qry = Sql.GetList(
                    "SELECT top 1000 MATERIAL_FULFILLMENT_COUNTRY_RECORD_ID,COUNTRIES FROM MAMAFC WHERE MATERIAL_RECORD_ID='"
                    + str(mat_rec_id)
                    + "' and FULCTY_FULLNAME='"
                    + str(coun_rec_id)
                    + "' ORDER BY CpqTableEntryId DESC "
                )
                if all_id_qry is not None:
                    for inn in all_id_qry:
                       
                        del_id = str(inn.MATERIAL_FULFILLMENT_COUNTRY_RECORD_ID)
                        
                        Table.TableActions.Delete(obj_name, "MATERIAL_FULFILLMENT_COUNTRY_RECORD_ID", del_id)
                for ins in value_list:
                    if ins is not None and ins != "":
                        next_id = Sql.GetFirst(
                            "SELECT top 1 MATERIAL_FULFILLMENT_COUNTRY_RECORD_ID FROM "
                            + obj_name
                            + " ORDER BY CpqTableEntryId DESC "
                        )
                        if next_id is not None and next_id != "":
                            next_val = str(next_id.MATERIAL_FULFILLMENT_COUNTRY_RECORD_ID)
                            
                            next_val1 = next_val.split("-")
                           
                            next_val2 = int(next_val1[1]) + 1
                            new_val = str(obj_name) + "-" + str(next_val2).rjust(5, "0")
                        else:
                            
                            next_val1 = "300000"
                           
                            next_val2 = int(next_val1) + 1
                            new_val = str(obj_name) + "-" + str(next_val2).rjust(5, "0")
                        row["MATERIAL_FULFILLMENT_COUNTRY_RECORD_ID"] = new_val
                        row["COUNTRIES"] = str(ins)
                        row["MATERIAL_RECORD_ID"] = str(mat_rec_id)
                        row["FULCTY_FULLNAME"] = str(coun_rec_id)
                        row["SAP_PART_NUMBER"] = str(sap_num)
                        row["INC_COUNTRY_TEMPLATES"] = str(inc_coun_temp)
                       
                        Table.TableActions.Create(obj_name, row)
        else:
            for rec in selected_rows:
                
                row = {}
                row = {TITLE: VALUE}
                row[objh_head] = str(rec)
                
                Table.TableActions.Update(obj_name, objh_head, row)
    return ""


TITLE = Param.TITLE
VALUE = Param.VALUE.encode("ASCII", "ignore")
ELEMENT = Param.ELEMENT
CLICKEDID = Param.CLICKEDID
RECORDID = Param.RECORDID

if str(TITLE) == "MAXIMUM_DISCOUNT_PERCENT":
    TITLE = "LOWPRCADJ_FACTOR"
if ELEMENT == "RELATEDEDIT":
    ApiResponse = ApiResponseFactory.JsonResponse(RELATEDMULTISELECTONEDIT(TITLE, VALUE, CLICKEDID, RECORDID))
elif ELEMENT == "SAVE":
    ApiResponse = ApiResponseFactory.JsonResponse(RELATEDMULTISELECTONSAVE(TITLE, VALUE, CLICKEDID, RECORDID))
else:
    ApiResponse = ApiResponseFactory.JsonResponse("")
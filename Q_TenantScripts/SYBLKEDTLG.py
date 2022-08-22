# =========================================================================================================================================
#   __script_name : SYBLKEDTLG.PY
#   __script_description : THIS SCRIPT IS USED FOR BULK EDITING RECORDS IN A LIST GRID.
#   __primary_author__ : JOE EBENEZER
#   __create_date :
#   Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
from SYDATABASE import SQL
import Webcom.Configurator.Scripting.Test.TestProduct
Sql = SQL()
import SYTABACTIN as Table

# import Mod_Pricing
#import PRIFLWTRGR


import SYCNGEGUID as CPQID


def MULTISELECTALL(CLICKEDID):
    TestProduct = Webcom.Configurator.Scripting.Test.TestProduct()
    CurrentTabName = TestProduct.CurrentTab
    sql_obj = Sql.GetFirst(
        "select RECORD_ID,SAPCPQ_ALTTAB_NAME from SYTABS where LTRIM(RTRIM(TAB_NAME)) = '"
        + str(CurrentTabName).strip()
        + "'"
    )
    if sql_obj is not None:
        SYSECT_OBJNAME = Sql.GetFirst(
            "select SE.RECORD_ID,SE.SECTION_NAME,SE.PRIMARY_OBJECT_NAME,SE.PRIMARY_OBJECT_RECORD_ID FROM SYSECT (nolock)SE inner join SYPAGE(nolock)PG on SE.PAGE_RECORD_ID = PG.RECORD_ID and SE.PAGE_NAME = PG.PAGE_NAME where PG.TAB_NAME = '"
            + str(CurrentTabName)
            + "' and PG.TAB_RECORD_ID='"
            + str(sql_obj.RECORD_ID)
            + "'"
        )
        pri_obj_id = str(SYSECT_OBJNAME.PRIMARY_OBJECT_RECORD_ID)
        data_obj = Sql.GetFirst(
            "SELECT RECORD_ID,CONTAINER_NAME,COLUMNS,CAN_DELETE,CAN_EDIT FROM SYOBJS WHERE NAME='Tab list' AND OBJ_REC_ID = '"
            + str(pri_obj_id)
            + "'"
        )
        if data_obj is not None:
            ctr_name = "LIST_" + str(data_obj.CONTAINER_NAME).strip()
        ctr = Product.GetContainerByName(str(ctr_name))
        tot_cnt = ctr.Rows.Count
        selected_rows = ctr.SelectedRowsIndexes
        selected_rows_len = selected_rows.split(",")
        selected_rows_len = [rw for rw in selected_rows_len if rw != ""]
        if tot_cnt != len(selected_rows_len):
            if CLICKEDID == "true":
                ctr.MakeAllRowsSelected()
        if CLICKEDID == "false":
            for sel_len in selected_rows_len:
                rowind = int(sel_len)
                ctr.MakeRowUnSelected(rowind)
    return CLICKEDID


def MULTISELECTEDIT(TITLE, VALUE, RECORDID):
    table_ids = ",".join(RECORDID)
    pri_obj_id = ""
    TestProduct = Webcom.Configurator.Scripting.Test.TestProduct()
    CurrentTabName = TestProduct.CurrentTab
    sql_obj = Sql.GetFirst(
        "select RECORD_ID,SAPCPQ_ALTTAB_NAME from SYTABS where LTRIM(RTRIM(TAB_NAME)) = '"
        + str(CurrentTabName).strip()
        + "'"
    )
    if sql_obj is not None:
        SYSECT_OBJNAME = Sql.GetFirst(
            "select SE.RECORD_ID,SE.SECTION_NAME,SE.PRIMARY_OBJECT_NAME,SE.PRIMARY_OBJECT_RECORD_ID FROM SYSECT (nolock)SE inner join SYPAGE(nolock)PG on SE.PAGE_RECORD_ID = PG.RECORD_ID and SE.PAGE_NAME = PG.PAGE_NAME where PG.TAB_NAME = '"
            + str(CurrentTabName)
            + "' and PG.TAB_RECORD_ID='"
            + str(sql_obj.RECORD_ID)
            + "'"
        )
        pri_obj_id = str(SYSECT_OBJNAME.PRIMARY_OBJECT_NAME)
    table_name = pri_obj_id
    edt_str = ""
    selected_rows = ""
    canedit = ""
    field_label = ""
    checked = ""
    ctr_len = []
    rec_list = []
    rec_list1 = []
    if str(TITLE).upper() != "SYMBOL":
        if "checked" not in VALUE:
            VALUE = remove_html_tags(VALUE)
    if VALUE is None:
        VALUE = ""
    date_field = []
    TestProduct = Webcom.Configurator.Scripting.Test.TestProduct()
    CurrentTabName = TestProduct.CurrentTab
    if str(TITLE).upper() != "ACTION" and str(CurrentTabName) != "Error Logs":
        sql_obj = Sql.GetFirst(
            "select RECORD_ID,SAPCPQ_ALTTAB_NAME from SYTABS where LTRIM(RTRIM(TAB_NAME)) = '"
            + str(CurrentTabName).strip()
            + "'"
        )
        if sql_obj is not None:
            SYSECT_OBJNAME = Sql.GetFirst(
                "select SE.RECORD_ID,SE.SECTION_NAME,SE.PRIMARY_OBJECT_NAME,SE.PRIMARY_OBJECT_RECORD_ID FROM SYSECT (NOLOCK)SE inner join SYPAGE(nolock)PG on SE.PAGE_RECORD_ID = PG.RECORD_ID and SE.PAGE_NAME = PG.PAGE_NAME where PG.TAB_NAME = '"
                + str(CurrentTabName)
                + "' and PG.TAB_RECORD_ID='"
                + str(sql_obj.RECORD_ID)
                + "'"
            )
            pri_obj_id = str(SYSECT_OBJNAME.PRIMARY_OBJECT_RECORD_ID)
            data_obj = Sql.GetFirst(
                "SELECT RECORD_ID,CONTAINER_NAME,COLUMNS,CAN_EDIT FROM SYOBJS WHERE NAME='Tab list' AND OBJ_REC_ID = '"
                + str(pri_obj_id)
                + "' and CONTAINER_NAME ='"
                + table_name
                + "'"
            )
            if data_obj is not None:
                # ctr_name = "LIST_"+str(data_obj.CONTAINER_NAME).strip()
                canedit = str(data_obj.CAN_EDIT)
            if str(canedit).upper() == "TRUE":
                # ctr = Product.GetContainerByName(str(ctr_name))
                # selected_rows = ctr.SelectedRowsIndexes
                obj_name = str(SYSECT_OBJNAME.PRIMARY_OBJECT_NAME).strip()
                header_OBJNAME = Sql.GetFirst("select FIELD_LABEL FROM SYOBJH where OBJECT_NAME = '" + str(obj_name) + "'")
                header_obj = str(header_OBJNAME.FIELD_LABEL).strip()
                Trace.Write(
                    "SELECT DATA_TYPE,PICKLIST_VALUES,API_NAME,PERMISSION,FIELD_LABEL,SOURCE_DATA FROM  SYOBJD WHERE OBJECT_NAME='"
                    + str(obj_name)
                    + "' and UPPER(API_NAME)='"
                    + str(TITLE).upper()
                    + "' "
                )
                datatype_obj = Sql.GetFirst(
                    "SELECT DATA_TYPE,PICKLIST_VALUES,API_NAME,PERMISSION,FIELD_LABEL,SOURCE_DATA FROM  SYOBJD WHERE OBJECT_NAME='"
                    + str(obj_name)
                    + "' and UPPER(API_NAME)='"
                    + str(TITLE).upper()
                    + "' "
                )
                if datatype_obj is not None:
                    field_label = str(datatype_obj.FIELD_LABEL)
                edt_str += (
                    '<div class="row modulebnr brdr">EDIT '
                    + str(field_label).upper()
                    + ' <button type="button"  class="close fltrt" onclick="multiedit_cancel();">X</button></div>'
                )
                edt_str += '<div id="container" class="g4 pad-10 brdr except_sec">'
                edt_str += '<table class="wdth100" id="bulk_edit">'
                if datatype_obj is not None:
                    field_label = str(datatype_obj.FIELD_LABEL)
                    api_name = str(datatype_obj.API_NAME)
                    data_type = str(datatype_obj.DATA_TYPE)
                    Permission = str(datatype_obj.PERMISSION)
                    ERP_validity = str(datatype_obj.SOURCE_DATA)
                   
                    if (
                        data_type != "FORMULA"
                        and data_type != "LOOKUP"
                        and Permission != "READ ONLY"
                        and str(ERP_validity).upper() != "ERP"
                    ):
                        try:
                            pick_val = str(datatype_obj.PICKLIST_VALUES)
                            Trace.Write("PICKLIST_VALUES" + str(pick_val))
                        except:
                            pick_val = datatype_obj.PICKLIST_VALUES

                        ctr_len.append(str(RECORDID))
                        datepicker = "onclick_datepicker('" + api_name + "')"
                        edt_str += (
                            '<tbody><tr class="fieldRow"><td  class="labelCol brdbtwth25posrel">'
                            + str(field_label)
                            + '</td><td  class="dataCol "><div id="massEditFieldDiv" class="inlineEditRequiredDiv">'
                        )
                        #Trace.Write(str(len(RECORDID)) + "length of len(ctr_len) is -----------------------")
                        if len(RECORDID) > 1:
                            if data_type.upper() == "TEXT":
                                edt_str += '<input class="form-control wth30brd1" id="' + str(api_name) + '" type="text">'
                            elif data_type.upper() == "CHECKBOX":
                                edt_str += (
                                    '<input class="custom wth30brd1" id="'
                                    + str(api_name)
                                    + '" type="checkbox" ><span class="lbl"></span>'
                                )
                            elif data_type.upper() == "NUMBER":
                                if str(api_name) == "COMM_CONCESSION_FACTOR":
                                    edt_str += (
                                        '<input  oninput="buttonState()" class="form-control wth30brd1" id="'
                                        + str(api_name)
                                        + '" type="text">'
                                    )
                                else:
                                    edt_str += (
                                        '<input class="form-control wth30brd1"  id="' + str(api_name) + '" type="text">'
                                    )
                            elif data_type.upper() == "PICKLIST":
                                edt_str += '<select class="form-control wth30brd1" id="' + str(api_name) + '">'
                                pick_val = pick_val.split(",")
                                for value in pick_val:
                                    try:
                                        edt_str += "<option>" + str(value) + "</option>"
                                    except:
                                        edt_str += "<option>" + value + "</option>"
                                edt_str += "</select>"
                            elif data_type.upper() == "DATE":
                                date_field.append(api_name)
                                edt_str += (
                                    '<input id="'
                                    + str(api_name)
                                    + '" type="text" class="form-control wth30et26"><span   class="input-group-addon pad4436wth0" onclick="'
                                    + str(datepicker)
                                    + '"><i class="glyphicon glyphicon-calendar"></i></span>'
                                )
                            else:
                                edt_str += '<input class="form-control wth30" id="' + str(api_name) + '" type="text">'
                            edt_str += '</div></td></tr><tr class="selectionRow">'
                            edt_str += (
                                '<td class="labelCol brdbtpostextmin">Apply changes to</td><td class="dataCol brbt0"><div class="radio"><input type="radio" name="massOrSingleEdit" id="singleEditRadio" checked="checked"><label for="singleEditRadio">The record clicked</label></div><div class="radio"><input type="radio" name="massOrSingleEdit" id="massEditRadio"><label for="massEditRadio">All '
                                + str(len(RECORDID))
                                + " selected records</label>"
                            )
                        else:
                            if data_type.upper() == "TEXT":
                                edt_str += (
                                    '<input class="form-control wth30brd1" id="'
                                    + str(api_name)
                                    + '" type="text" value="'
                                    + str(VALUE)
                                    + '">'
                                )
                            elif data_type.upper() == "NUMBER":
                                # Trace.Write("CHECK@@@" + str(api_name))
                                # Trace.Write("CHECK@@@" + str(VALUE))
                                if str(api_name) == "COMM_CONCESSION_FACTOR":
                                    edt_str += (
                                        '<input  oninput="buttonState()" class="form-control wth30brd1"  id="'
                                        + str(api_name)
                                        + '" type="text">'
                                    )
                                else:
                                    edt_str += (
                                        '<input class="form-control wth30brd1" id="'
                                        + str(api_name)
                                        + '" value="'
                                        + str(VALUE)
                                        + '" type="text">'
                                    )
                            elif data_type.upper() == "CHECKBOX":
                                #Trace.Write("VALUE123 is " + str(VALUE))
                                if "checked" in str(VALUE):
                                    checked = "checked"
                                edt_str += (
                                    '<input class="custom wth30brd1"  id="'
                                    + str(api_name)
                                    + '" type="checkbox" '
                                    + str(checked)
                                    + '><span class="lbl"></span>'
                                )
                            elif data_type.upper() == "PICKLIST":
                                edt_str += '<select class="form-control wth30brd1" id="' + str(api_name) + '">'
                                pick_val = pick_val.split(",")
                                for value in pick_val:
                                    try:
                                        if value == VALUE:
                                            edt_str += "<option selected>" + str(value) + "</option>"
                                        else:
                                            edt_str += "<option>" + str(value) + "</option>"
                                    except:
                                        if value == VALUE:
                                            edt_str += "<option selected>" + value + "</option>"
                                        else:
                                            edt_str += "<option>" + value + "</option>"
                                edt_str += "</select>"
                            elif data_type.upper() == "DATE":
                                date_field.append(api_name)
                                edt_str += (
                                    '<input id="'
                                    + str(api_name)
                                    + '" type="text" value="'
                                    + str(VALUE)
                                    + '" class="form-control wth30et26"><span  class="input-group-addon pad4436wth0" onclick="'
                                    + str(datepicker)
                                    + '"><i class="glyphicon glyphicon-calendar"></i></span>'
                                )
                            else:
                                edt_str += (
                                    '<input class="form-control wth30"  id="'
                                    + str(api_name)
                                    + '" type="text" value="'
                                    + str(VALUE)
                                    + '">'
                                )
                        edt_str += "</div></td></tr></tbody></table>"
                        if data_type.upper() == "NUMBER" and str(api_name) == "COMM_CONCESSION_FACTOR":
                            edt_str += '</div><div class="row pad-10"><button class="btnstyle mrg-rt-8 btn" onclick="multiedit_cancel();" type="button" value="Cancel" id="cancelButton">CANCEL</button><button class="btnstyle mrg-rt-8 btn" type="button" value="Save" onclick="multiedit_save()" id="saveButton"disabled>SAVE</button></div>'
                        else:
                            edt_str += '</div><div class="row pad-10"><button class="btnstyle mrg-rt-8 btn" onclick="multiedit_cancel();" type="button" value="Cancel" id="cancelButton">CANCEL</button><button class="btnstyle mrg-rt-8 btn" type="button" value="Save" onclick="multiedit_save()" id="saveButton">SAVE</button></div>'
                    else:
                        edt_str = "NO"
            else:
                edt_str = "NO"

    else:
        edt_str = "NO"
    if edt_str == "":
        edt_str = "NO"
    return edt_str, date_field


def PIVOT_MULTISELECTEDIT(TITLE, VALUE, RECORDID, CLICKEDID):
    length = 0
    count = 0
    salesid_list = []
    sales_list = []
    val_dict = {}
    onfocusout = 'onchange = "factor_changes(this)"'
    ParentNodeRECORD = Product.GetGlobal("ParentNodeRECORD")

    edt_str = ""
    selected_rows = ""
    canedit = ""
    field_label = str(TITLE).replace("_", " ")
    checked = ""
    ctr_len = []
    rec_list = []
    rec_list1 = []
    if str(TITLE).upper() != "SYMBOL":
        if "checked" not in VALUE:
            VALUE = remove_html_tags(VALUE)
    if VALUE is None:
        VALUE = ""
    date_field = []
    TestProduct = Webcom.Configurator.Scripting.Test.TestProduct()
    CurrentTabName = TestProduct.CurrentTab

    edt_str = "NO"
    # Trace.Write("edt_str >>>>>>>>>>..." + str(edt_str))
    # Trace.Write("date_field >>>>>>>>>>..." + str(date_field))
    return edt_str, date_field


def MULTISELECTSAVE(TITLE, VALUE, RECORDID):
    selected_rows = ""
    selected_rows = RECORDID.split(",")

    # selected_rows_all = [data for data in selected_rows]
    # selected_row_index = Product.GetGlobal('clicked_index')
    TestProduct = Webcom.Configurator.Scripting.Test.TestProduct()
    CurrentTabName = TestProduct.CurrentTab
    sql_obj = Sql.GetFirst(
        "select RECORD_ID,SAPCPQ_ALTTAB_NAME from SYTABS where LTRIM(RTRIM(TAB_NAME)) = '"
        + str(CurrentTabName).strip()
        + "'"
    )
    if sql_obj is not None:
        SYSECT_OBJNAME = Sql.GetFirst(
            "select SE.RECORD_ID,SE.SECTION_NAME,SE.PRIMARY_OBJECT_NAME,SE.PRIMARY_OBJECT_RECORD_ID FROM SYSECT(NOLOCK)SE inner join SYPAGE(nolock)PG on SE.PAGE_RECORD_ID = PG.RECORD_ID and SE.PAGE_NAME = PG.PAGE_NAME where PG.TAB_NAME = '"
            + str(CurrentTabName)
            + "' and PG.TAB_RECORD_ID='"
            + str(sql_obj.RECORD_ID)
            + "'"
        )
        pri_obj_id = str(SYSECT_OBJNAME.PRIMARY_OBJECT_RECORD_ID)
        data_obj = Sql.GetFirst(
            "SELECT RECORD_ID,CONTAINER_NAME,COLUMNS,CAN_DELETE,CAN_EDIT FROM SYOBJS WHERE NAME='Tab list' AND OBJ_REC_ID = '"
            + str(pri_obj_id)
            + "'"
        )
        obj_name = str(SYSECT_OBJNAME.PRIMARY_OBJECT_NAME).strip()
        SYOBJH_OBJNAME = Sql.GetFirst("select RECORD_NAME FROM SYOBJH where OBJECT_NAME = '" + str(obj_name) + "'")
        objh_head = str(SYOBJH_OBJNAME.RECORD_NAME)
        SYOBJD_OBJNAME = Sql.GetFirst(
            "select FIELD_LABEL,DATA_TYPE FROM  SYOBJD where OBJECT_NAME = '"
            + str(obj_name)
            + "' and API_NAME = '"
            + str(TITLE)
            + "'"
        )
        objh_head = str(SYOBJH_OBJNAME.RECORD_NAME)
        objd_lab = str(SYOBJD_OBJNAME.FIELD_LABEL)
        objd_datatype = str(SYOBJD_OBJNAME.DATA_TYPE)
        checked = ""
        flag = 0
        for rec in selected_rows:
            flag = 0

            #Trace.Write("Rec valu " + str(rec) + "ssssssssss" + str(flag))
            row = {}
            try:
                row = {TITLE: str(VALUE)}
            except:
                row = {TITLE: VALUE}
            row[objh_head] = str(rec)
            if flag == 0:
                Table.TableActions.Update(obj_name, objh_head, row)
    return ""


def remove_html_tags(text):
    """Remove html tags from a string"""
    import re

    clean = re.compile("<.*?>")
    return re.sub(clean, "", text)


def Remove(duplicate):
    final_list = []
    for num in duplicate:
        if num not in final_list:
            final_list.append(num)
    return final_list


def MULTISELECTONLOAD():
    dbl_clk_val = []
    TestProduct = Webcom.Configurator.Scripting.Test.TestProduct()
    CurrentTabName = TestProduct.CurrentTab
    sql_obj = Sql.GetFirst(
        "select RECORD_ID,SAPCPQ_ALTTAB_NAME from SYTABS where LTRIM(RTRIM(TAB_NAME)) = '"
        + str(CurrentTabName).strip()
        + "'"
    )
    if sql_obj is not None:
        SYSECT_OBJNAME = Sql.GetFirst(
            "select SE.RECORD_ID,SE.SECTION_NAME,SE.PRIMARY_OBJECT_NAME FROM SYSECT(NOLOCK)SE inner join SYPAGE(nolock)PG on SE.PAGE_RECORD_ID = PG.RECORD_ID and SE.PAGE_NAME = PG.PAGE_NAME where PG.TAB_NAME = '"
            + str(CurrentTabName)
            + "' and PG.TAB_RECORD_ID='"
            + str(sql_obj.RECORD_ID)
            + "'"
        )
        obj_name = str(SYSECT_OBJNAME.PRIMARY_OBJECT_NAME).strip()
        SYOBJD_OBJNAME = Sql.GetList(
            "select FIELD_LABEL FROM  SYOBJD where OBJECT_NAME = '"
            + str(obj_name)
            + "' and DATA_TYPE not in ('AUTO NUMBER','FORMULA','LOOKUP') "
        )
        for dobj in SYOBJD_OBJNAME:
            dbl_clk_val.append(str(dobj.FIELD_LABEL))
    return dbl_clk_val


def RELATEDMULTISELECTONEDIT(TITLE, VALUE, CLICKEDID):
    clicked = CLICKEDID.split("_")
    obj_id = clicked[2] + "-" + clicked[3]
    edt_str = ""
    checked = ""
    date_field = []
    VALUE = remove_html_tags(VALUE)
    objh_obj = Sql.GetFirst("select OBJECT_NAME from SYOBJH where RECORD_ID = '" + str(obj_id) + "'")
    if objh_obj is not None:
        obj_obj = str(objh_obj.OBJECT_NAME)
        Trace.Write(
            "SELECT DATA_TYPE,PICKLIST_VALUES,API_NAME,FIELD_LABEL FROM  SYOBJD where OBJECT_NAME='"
            + str(obj_obj)
            + "' and API_NAME='"
            + str(TITLE)
            + "'"
        )
        objd_obj = Sql.GetFirst(
            "SELECT DATA_TYPE,PICKLIST_VALUES,API_NAME,FIELD_LABEL FROM  SYOBJD where OBJECT_NAME='"
            + str(obj_obj)
            + "' and API_NAME='"
            + str(TITLE)
            + "'"
        )
        if objd_obj is not None:
            data_type = str(objd_obj.DATA_TYPE).strip()
            api_name = str(objd_obj.API_NAME).strip()
            if data_type != "FORMULA" and data_type != "LOOKUP" and data_type != "AUTO NUMBER":
                pick_val = str(objd_obj.PICKLIST_VALUES)
                field_lable = str(objd_obj.FIELD_LABEL)
                datepicker = "onclick_datepicker('" + api_name + "')"
                edt_str += (
                    '<div  class="row modulebnr brdr">EDIT '
                    + str(field_lable).upper()
                    + ' <button type="button"  class="close fltrt" onclick="multiedit_cancel();">X</button></div>'
                )
                edt_str += '<div id="container" class="g4 pad-10 brdr except_sec">'
                edt_str += '<table class="wdth100" id="bulk_edit">'
                edt_str += (
                    '<tbody><tr class="fieldRow"><td  class="labelCol brdbtwth25posrel">'
                    + str(field_lable)
                    + '</td><td class="dataCol"><div id="massEditFieldDiv" class="inlineEditRequiredDiv">'
                )
                if data_type.upper() == "TEXT":
                    edt_str += (
                        '<input class="form-control widthautobrdr"  id="'
                        + str(api_name)
                        + '" type="text" value="'
                        + str(VALUE)
                        + '">'
                    )
                elif data_type.upper() == "NUMBER":
                    edt_str += (
                        '<input class="form-control widthautobrdr"   id="'
                        + str(api_name)
                        + '" value="'
                        + str(VALUE)
                        + '" type="text">'
                    )
                elif data_type.upper() == "CHECKBOX":
                    #Trace.Write("VALUE is" + str(VALUE))
                    if str(VALUE).upper() == "TRUE":
                        checked = "checked"
                    edt_str += (
                        '<input class="custom widthautobrdr"   id="'
                        + str(api_name)
                        + '" type="checkbox" '
                        + str(checked)
                        + '><span class="lbl"></span>'
                    )
                elif data_type.upper() == "PICKLIST":
                    edt_str += '<select class="form-control wth150" id="' + str(api_name) + '">'
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
                        + '" class="form-control wth155hit26" ><span class="pad4wth0 input-group-addon" onclick="'
                        + str(datepicker)
                        + '"><i class="glyphicon glyphicon-calendar"></i></span>'
                    )
                edt_str += "</div></td></tr></tbody></table>"
                edt_str += '</div><div class="row pad-10"><button class="btnstyle mrg-rt-8 btn" onclick="multiedit_cancel();" type="button" value="Cancel" id="cancelButton">CANCEL</button><button class="btnstyle mrg-rt-8 btn" type="button" value="Save" onclick="multiedit_save()" id="saveButton">SAVE</button></div>'
            else:
                edt_str = "NO"
    return edt_str, date_field


TITLE = ""
#Trace.Write("zzzzzzzzzzzzzzzzzz--TITLE " + str(TITLE))
try:
    TITLE = Param.TITLE
except:
    TITLE = ""
Trace.Write("yyyyyyyyyyyyyyyyyy--TITLE " + str(TITLE))
RECORDID = Param.RECORDID
try:
    VALUE = str(Param.VALUE).encode("ASCII", "ignore")
    #Trace.Write("111111111111111111111111---------------->" + str(VALUE))
except:
    VALUE = Param.VALUE
ELEMENT = Param.ELEMENT
CLICKEDID = Param.CLICKEDID
Trace.Write("xxxxxxxxxxxxxxx--TITLE " + str(TITLE))
Trace.Write(VALUE)
Trace.Write(str(",".join(RECORDID)))
Trace.Write("xxxxxxxxxxxxxxx--ELEMENT " + str(ELEMENT))
Trace.Write("xxxxxxxxxxxxxxx--CLICKEDID " + str(CLICKEDID))

if ELEMENT == "ALL":
    ApiResponse = ApiResponseFactory.JsonResponse(MULTISELECTALL(CLICKEDID))
elif ELEMENT == "EDIT":
    if str(CLICKEDID) in [
        "SALES_ORG_LEVEL_DEFAULT_FACTORS",
        "PRICE_CLASS_LEVEL_FACTORS",
        "MATERIALS_IN_PRICE_METHODS",
    ]:
        RECORDID = str(",".join(RECORDID))
        ApiResponse = ApiResponseFactory.JsonResponse(PIVOT_MULTISELECTEDIT(TITLE, VALUE, RECORDID, CLICKEDID))
    else:
        ApiResponse = ApiResponseFactory.JsonResponse(MULTISELECTEDIT(TITLE, VALUE, RECORDID))
elif ELEMENT == "SAVE":
    if str(CLICKEDID) in [
        "SALES_ORG_LEVEL_DEFAULT_FACTORS",
        "PRICE_CLASS_LEVEL_FACTORS",
        "MATERIALS_IN_PRICE_METHODS",
    ]:
        RECORDID = str("".join(RECORDID))
        ApiResponse = ApiResponseFactory.JsonResponse(PIVOT_MULTISELECTSAVE(TITLE, VALUE, RECORDID, CLICKEDID))
    else:
        ApiResponse = ApiResponseFactory.JsonResponse(MULTISELECTSAVE(TITLE, VALUE, RECORDID))
elif ELEMENT == "ONLOAD":
    ApiResponse = ApiResponseFactory.JsonResponse(MULTISELECTONLOAD())
elif ELEMENT == "RELATEDEDIT":
    ApiResponse = ApiResponseFactory.JsonResponse(RELATEDMULTISELECTONEDIT(TITLE, VALUE, CLICKEDID))
else:
    ApiResponse = ApiResponseFactory.JsonResponse("")
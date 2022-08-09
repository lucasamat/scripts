# ===================================================================================================
#   __script_name : SYPRFLOBST.PY
#   __script_description : This script is used to view and edit operations in pop up (System Admin->Profile Tab->Object Level permission)
#   __primary_author__ : JOE EBENEZER
#   __create_date : 31/08/2020
#   Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct
import SYCNGEGUID as CPQID
from SYDATABASE import SQL

Sql = SQL()


def build_modal_details(table_id, key_name, key_value, mode="view"):
    if table_id and key_name and key_value:
        table_name = key_value.split("-")[0]
        objr_rec_id = "-".join(table_id.split("_")[0:2])
        objr_obj = Sql.GetFirst("SELECT COLUMNS FROM SYOBJR WHERE RECORD_ID='{}' ".format(objr_rec_id))
        table_data = []
        if objr_obj is not None:
            objd_auto_number_obj = Sql.GetFirst(
                "SELECT API_NAME FROM  SYOBJD WHERE OBJECT_NAME = '{}' AND DATA_TYPE = 'AUTO NUMBER' ".format(table_name)
            )
            columns = objr_obj.COLUMNS.strip("][").split(",")
            columns = tuple(str(column.strip("'").strip('"')) for column in columns)
            Trace.Write(str(columns))

            objd_obj = Sql.GetList(
                "SELECT TOP(1000) * FROM  SYOBJD WHERE OBJECT_NAME = '{}' AND API_NAME IN {} ORDER BY DISPLAY_ORDER".format(
                    table_name, repr(columns)
                )
            )
            if objd_obj is not None and objd_auto_number_obj:
                rec_value = CPQID.KeyCPQId.GetKEYId(table_name, key_value)
                data_obj = Sql.GetFirst(
                    "SELECT * FROM {} WHERE {}='{}' ".format(table_name, objd_auto_number_obj.API_NAME, rec_value)
                )
                if data_obj is not None:
                    for index, objd_record in enumerate(objd_obj):
                        column_name = objd_record.API_NAME
                        try:
                            column_value = eval("data_obj." + column_name)
                            if index == 0:
                                column_value = CPQID.KeyCPQId.GetCPQId(table_name, column_value)
                        except:
                            column_value = ""
                        column_type = objd_record.DATA_TYPE
                        if objd_record.PERMISSION == "READ ONLY":
                            column_permission_icon = '<i class="fa fa-lock" aria-hidden="true"></i>'
                        else:
                            column_permission_icon = '<i class="fa fa-pencil" aria-hidden="true"></i>'

                        table_data.append(
                            """
                            <tr class="iconhvr borbot1">
                                <td class="width350"><label class="pad_l_mar_bot">{KEY}</label></td>
                                <td class="width40"><a class="color_align_width" href="#" data-placement="top" data-toggle="popover" data-content="{DATA_CONTENT}"><i class="fa fa-info-circle flt_lt"></i></a></td>
                                <td><input type="{Input_Type}" value="{VALUE}" id ="{KEY}" class="{Input_Class}" {Checked} {Disabled}>{Input_Checkbox_Span}</td>
                                <td class="fltrtbrdbt0">
                                    <div class="col-md-12 editiconright"><a href="#" onclick="" class="editclick">{Column_Icon}</a></div>
                                </td>
                            </tr>
                        """.format(
                                KEY=objd_record.FIELD_LABEL,
                                DATA_CONTENT=objd_record.FIELD_LABEL,
                                Input_Type="checkbox" if column_type == "CHECKBOX" else "text",
                                VALUE=column_value,
                                Input_Class="custom" if column_type == "CHECKBOX" else "form-control related_popup_css",
                                Input_Checkbox_Span='<span class="lbl"></span>' if column_type == "CHECKBOX" else "",
                                Column_Icon=column_permission_icon,
                                Checked="checked" if column_type == "CHECKBOX" and column_value == True else "",
                                Disabled="" if mode == "edit" and objd_record.PERMISSION != "READ ONLY" else "disabled",
                            )
                        )

        result_str = """<div class="row modulebnr brdr ma_mar_btm">{}
                        <button type="button" class="close fltrt" data-dismiss="modal">X</button>
                    </div>
                    <div class="col-md-12">
                        <div class="row pad-10 bg-lt-wt brdr" >
                            
                            
                            <button type="button" class="btnconfig" id= "BTN_PROFILE_OBJSET_EDIT" onclick="profileObjSetModalEdit(this)" >EDIT</button>
                            <button type="button" class="btnconfig" id = "BTN_PROFILE_OBJSET_SAVE" onclick="profileObjectSetSave()" data-dismiss="modal">SAVE</button>
                            <button type="button" class="btnconfig" id = "BTN_PROFILE_OBJSET_CAN" onclick="Profile_BacktoList()" data-dismiss="modal">CANCEL</button>
                        </div>
                        <div id="Headerbnr" class="mart_col_back"></div>
                    </div>
                    <div id="container" class="g4 pad-10 brdr except_sec">
                        
                        <table class="ma_width_marg" id= 'Profile_ObjSettings'>
                            <tbody>{}
                            </tbody>
                        </table>
                    </div>""".format(
            mode.capitalize(), "".join(table_data)
        )
        return result_str

key_name = "KEY"
key_value = Param.key_value
table_id = Param.tableId
mode = Param.mode
if mode == "VIEW":
    mode = "VIEW"
else:
    mode = "edit"
ApiResponse = ApiResponseFactory.JsonResponse(build_modal_details(table_id, key_name, key_value, mode))
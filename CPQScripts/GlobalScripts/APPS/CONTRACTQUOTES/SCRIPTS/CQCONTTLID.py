# =========================================================================================================================================
#   __script_name : CQCONTTLID.PY
#   __script_description : THIS SCRIPT IS USED TO VIEW TOOL IDLING IN CART ITEMS NODE
#   __primary_author__ : KRISHNA CHAITANYA
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
from SYDATABASE import SQL
from datetime import datetime
import datetime
Sql = SQL()
import SYCNGEGUID as CPQID
import Webcom.Configurator.Scripting.Test.TestProduct
TestProduct = Webcom.Configurator.Scripting.Test.TestProduct()

class tool_idle:
    def Contract_Tool_Idling(self):
        Trace.Write("tp inside function")    
        where_string = ""
        sec_str = ""
        TreeParam = Product.GetGlobal("TreeParam")

        # if A_Keys != "" and A_Values != "":
        #     A_Keys = list(A_Keys)
        #     A_Values = list(A_Values)
        #     for key, value in zip(A_Keys, A_Values):
        #         if value.strip():
        #             if where_string:
        #                 where_string += " AND "
        #             where_string += "{Key} LIKE '%{Value}%'".format(Key=key, Value=value)
        #DIVNAME = "VIEW_DIV_ID"
        new_value_dict = {}
        ObjectName = "CART"
        table_id = "contract_sec_tool"
        Header_details = {
            "TOOL IDLING": "TOOL IDLING",
            "DESCRIPTION":"DESCRIPTION",
            "REQUIRED": "*",
            "VALUES": "VALUES",    
        }
        ordered_keys = [
            "TOOL IDLING",
            "DESCRIPTION",
            "REQUIRED",
            "VALUES",    
        ]
        # Objd_Obj = Sql.GetList(
        #     "select FIELD_LABEL,API_NAME,LOOKUP_OBJECT,LOOKUP_API_NAME,DATA_TYPE,FORMULA_DATA_TYPE from SYOBJD (NOLOCK)where OBJECT_NAME = '"
        #     + str(ObjectName)
        #     + "'"
        # )
        # lookup_disply_list = []
        # if Objd_Obj is not None:
        #     attr_list = {}
        #     api_names = [inn.API_NAME for inn in Objd_Obj]
        #     for attr in Objd_Obj:
        #         attr_list[str(attr.API_NAME)] = str(attr.FIELD_LABEL)
        #         if str(attr.LOOKUP_API_NAME) != "" and str(attr.LOOKUP_API_NAME) is not None:
        #             lookup_disply_list.append(str(attr.API_NAME))
        #     checkbox_list = [
        #         inn.API_NAME for inn in Objd_Obj if (inn.DATA_TYPE == "CHECKBOX" or inn.FORMULA_DATA_TYPE == "CHECKBOX")
        #     ]
        #     lookup_list = {ins.LOOKUP_API_NAME: ins.API_NAME for ins in Objd_Obj}

            # current_obj_value = ""
            # onchange = ""
            # disable = ""            
            # current_obj_api_name = attr.API_NAME

        #sec_str = '<div id="contract_cust_fields_div">'     

        sec_str = '<div id="container" class="g4 pad-10 brdr except_sec">'
        sec_str += (
            '<table id="'
            + str(table_id)
            + '" data-escape="true"  data-search-on-enter-key="true" data-show-header="true"  data-filter-control="true"> <thead><tr>'
        )
        #sec_str += '<th data-field="SELECT" class="wth45" data-checkbox="true" id ="check_boxval" onchange = "get_checkedval()"><div class="action_col">SELECT</div></th>'

        for key, invs in enumerate(list(ordered_keys)):

            invs = str(invs).strip()
            qstring = Header_details.get(str(invs)) or ""    
            sec_str += (
                '<th data-field="'
                + invs
                + '" data-title-tooltip="'
                + str(qstring)
                + '" data-sortable="true" data-filter-control="input">'
                + str(qstring)
                + "</th>"
            )
            
        sec_str += '</tr></thead><tbody class ="tool_idle" >'
        Objd_Obj = Sql.GetList(
            "select FIELD_LABEL,API_NAME,LOOKUP_OBJECT,LOOKUP_API_NAME,DATA_TYPE,FORMULA_DATA_TYPE,PICKLIST_VALUES,PERMISSION from SYOBJD (NOLOCK)where OBJECT_NAME = '"
            + str(ObjectName)
            + "'"
        )
        for tool in Objd_Obj:
            onchange = ""
            current_obj_value = tool.PICKLIST_VALUES
            disable = ""
            edit_warn_icon = ""
            left_float = ""
            edit_pencil_icon = ""
            MODE = ""
            current_obj_api_name = tool.API_NAME
            Trace.Write("iii"+str(current_obj_api_name))
            readonly_val = tool.PERMISSION
            if (readonly_val == "" or readonly_val.upper() == "EDITABLE"):				
                edit_pencil_icon = '<i class="fa fa-pencil" aria-hidden="true"></i>'
            elif readonly_val == "EDITABLE":						
                edit_pencil_icon = '<i class="fa fa-pencil" aria-hidden="true"></i>'
            else:						
                edit_pencil_icon = '<i class="fa fa-lock" aria-hidden="true"></i>'
                disable = "disabled"
            sec_str += '<tr><td>'+tool.FIELD_LABEL+'</td><td>'+tool.FIELD_LABEL+'</td><td>*</td>'
            if tool.DATA_TYPE == "PICKLIST":
                sec_str += '<td>'
                sec_str += (
                    '<select id="'
                    + str(current_obj_api_name)
                    + '" '
                    + str(onchange)
                    + ' value="'
                    + current_obj_value
                    + '" type="text" title="'
                    + str(current_obj_value)
                    + '" class="form-control pop_up_brd_rad related_popup_css fltlt"  '
                    + disable
                    + " style=\'margin-left: -1px\'><option value='Select'></option>"
                )
                Sql_Quality_Tier = Sql.GetFirst(
                    "select PICKLIST_VALUES FROM  SYOBJD WITH (NOLOCK) where OBJECT_NAME='"
                    + str(ObjectName)
                    + "' and DATA_TYPE='PICKLIST' and API_NAME = '"
                    + str(current_obj_api_name)
                    + "' "
                )
                if (
						str(Sql_Quality_Tier.PICKLIST_VALUES).strip() is not None
						and str(Sql_Quality_Tier.PICKLIST_VALUES).strip() != ""
					):						
						Tier_List = (Sql_Quality_Tier.PICKLIST_VALUES).split(",")		
						for req1 in Tier_List:
							req1 = req1.strip()							
							if current_obj_value == req1:								
								sec_str += "<option selected>" + str(req1) + "</option>"
							else:								
								sec_str += "<option>" + str(req1) + "</option>"
                else:						
                    sec_str += "<option selected>" + str(current_obj_value) + "</option>"
                sec_str += '</select></td>'
            elif tool.DATA_TYPE == "TEXT":
                sec_str += (
                        '<td><input id="'
                        + str(current_obj_api_name)
                        + '" type="text" value="'
                        + current_obj_value
                        + '" title="'
                        + current_obj_value
                        + '" class="form-control related_popup_css fltlt" style="'
                        + str(left_float)
                        + ' ">'
                        + str(edit_warn_icon)
                        + "</td>"
					)
            elif tool.DATA_TYPE == "LONG TEXT AREA":
                if str(MODE)=="VIEW" or str(MODE)=="CANCEL":							
                    sec_str += (
                        '<td><textarea title="'
                        + str(current_obj_value)
                        + '" class="form-control related_popup_css txtArea" id="'
                        + str(current_obj_api_name)
                        + '" rows="1" cols="100" '
                        + disable
                        + ">"
                        + current_obj_value
                        + "</textarea></td>"
                    )
                else:																	
                    sec_str += (
                        '<td><textarea title="'
                        + str(current_obj_value)
                        + '" class="form-control related_popup_css txtArea " id="'
                        + str(current_obj_api_name)
                        + '" rows="1" cols="100" '
                        + disable							
                        + ">"
                        + current_obj_value
                        + "</textarea></td>"
                    )         
            sec_str += (
					'<td class="float_r_bor_bot"><div class="col-md-12 editiconright"><a href="#" onclick="editclick_row(this)" class="editclick">'
					+ str(edit_pencil_icon)
					+ "</a></div></td>"
				)           
            sec_str += '</tr>'

        sec_str += '</tbody></table>'
        #sec_str += '<div id="involved_parties_equipment_addnew_footer"></div>'
        values_list = ""
        values_lists = ""
        a_test = []
        for invsk in list(Header_details):
            table_ids = "#" + str(table_id)
            filter_class = table_ids + " .bootstrap-table-filter-control-" + str(invsk)
            values_lists += "var " + str(invsk) + ' = $("' + str(filter_class) + '").val(); '
            values_lists += " ATTRIBUTE_VALUEList.push(" + str(invsk) + "); "
            a_test.append(invsk)
                            
        return (
            sec_str,
            new_value_dict                       
            )
objtool_idle = tool_idle()
ACTION = Param.ACTION
if ACTION == "CONT_TOOL_IDLE":               
    ApiResponse = ApiResponseFactory.JsonResponse(objtool_idle.Contract_Tool_Idling())

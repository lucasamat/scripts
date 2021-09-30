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
    def Contract_Tool_Idling(self, MODE):
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
            "": "",    
        }
        ordered_keys = [
            "TOOL IDLING",
            "DESCRIPTION",
            "REQUIRED",
            "VALUES",
            "",    
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
        current_obj_value = ""
        Objd_Obj = Sql.GetList(
            "select FIELD_LABEL,API_NAME,LOOKUP_OBJECT,LOOKUP_API_NAME,DATA_TYPE,FORMULA_DATA_TYPE,PICKLIST_VALUES,PERMISSION,REQUIRED from SYOBJD (NOLOCK)where OBJECT_NAME = '"
            + str(ObjectName)
            + "'"
        )
        for tool in Objd_Obj:         
                
            onchange = ""
            Trace.Write("obi----"+str(tool.API_NAME))
            current_obj_value = Quote.GetCustomField(tool.API_NAME).Content            
            edit_warn_icon = ""
            left_float = ""
            edit_pencil_icon = ""
            disable = "disabled"
            current_obj_api_name = tool.API_NAME
            Trace.Write("iii"+str(current_obj_api_name))
            readonly_val = tool.PERMISSION
            if (readonly_val == "" or readonly_val.upper() == "EDITABLE") and (MODE == "VIEW" or MODE == "CANCEL" or MODE == "SAVE"):				
                edit_pencil_icon = '<i class="fa fa-pencil" aria-hidden="true"></i>'
                disable = "disabled"
            elif readonly_val == "EDITABLE" and MODE == "EDIT":						
                edit_pencil_icon = '<i class="fa fa-pencil" aria-hidden="true"></i>'
                disable = ""
            elif readonly_val == "READONLY" and (MODE == "EDIT" or MODE == "CANCEL" or MODE == "SAVE" or MODE == "VIEW"):						
                edit_pencil_icon = '<i class="fa fa-lock" aria-hidden="true"></i>'
                disable = "disabled"
            sec_str += '<tr><td>'+tool.FIELD_LABEL+'</td><td>'+tool.FIELD_LABEL+'</td><td>*</td>'
            # if tool.REQUIRED == "True":
            #     sec_str += '<td>*</td>'
            # if tool.REQUIRED == "False":
            #     sec_str += '<td></td>'    
            if tool.DATA_TYPE == "PICKLIST":
                if MODE == "EDIT" and readonly_val == "EDITABLE":
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
                        + '" class="form-control pop_up_brd_rad related_popup_css fltlt light_yellow"  '                                                
                        + " style=\'margin-left: -1px\'><option value='Select'></option>"
                    )
                    Sql_Quality_Tier = Sql.GetFirst(
                        "select PICKLIST_VALUES FROM  SYOBJD WITH (NOLOCK) where OBJECT_NAME='"
                        + str(ObjectName)
                        + "' and DATA_TYPE='PICKLIST' and API_NAME = '"
                        + str(current_obj_api_name)
                        + "' "
                    )
                elif MODE == "EDIT" and readonly_val == "READONLY":
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
                else:
                    Trace.Write("pick"+str(MODE))
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
                if MODE == "EDIT":
                    sec_str += (
                            '<td><input id="'
                            + str(current_obj_api_name)
                            + '" type="text" value="'
                            + current_obj_value
                            + '" title="'
                            + current_obj_value
                            + '" class="form-control related_popup_css fltlt light_yellow" style="'
                            + str(left_float)
                            + ' ">'
                            + str(edit_warn_icon)
                            + "</td>"
                        )
                else:
                    sec_str += (
                        '<td><input disabled id="'
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
                if str(MODE)=="VIEW" or str(MODE)=="CANCEL" or str(MODE) == "SAVE":
                    Trace.Write("mode222"+str(MODE))							
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
                    Trace.Write("mode33"+str(MODE))																	
                    sec_str += (
                        '<td><textarea title="'
                        + str(current_obj_value)
                        + '" class="form-control related_popup_css txtArea light_yellow" id="'
                        + str(current_obj_api_name)
                        + '" rows="1" cols="100" '                        							
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
            dbl_clk_function = (	 
            '$("'	
            + str(table_ids)	
            + '").on("dbl-click-cell.bs.table", onClickCell); $("'	
            + str(table_ids)	
            + '").on("all.bs.table", function (e, name, args) { $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); }); $("'	
            + str(table_ids)	
            + '\ th.bs-checkbox div.th-inner").before(""); $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); function onClickCell(event, field, value, row, $element) { var reco_id="";console.log("reco_id2--",reco_id);reco_id=reco_id; reco_id=reco_id.split(","); localStorage.setItem("multiedit_save_date", reco_id);  localStorage.setItem("table_id_RL_edit", "SYOBJR_00011_1E92CAAD_4EE9_4E5C_AA11_80F20D295A63");console.log("value--",field);edit_index = $("'+str(table_ids)+'").find("[data-field="+ field +"]").index()+1;localStorage.setItem("edit_index",edit_index); cpq.server.executeScript("SYBLKETRLG", {"TITLE":field, "VALUE":value, "CLICKEDID":"SYOBJR_00011_1E92CAAD_4EE9_4E5C_AA11_80F20D295A63", "RECORDID":reco_id, "ELEMENT":"RELATEDEDIT"}, function(data) { debugger; data1=data[0]; data2=data[1]; data3 = data[2];if(data1 != "NO"){ if(document.getElementById("RL_EDIT_DIV_ID") ) { localStorage.setItem("saqico_title", field); inp = "#"+data3;localStorage.setItem("value_tag", "'+ str(table_id)+' "+inp);$("'+str(table_ids)+' "+inp).closest("tr").find("td:nth-child("+edit_index+")").attr("contenteditable", true); var buttonlen = $("#seginnerbnr").find("button#saveButton"); if (buttonlen.length == 0){	$("#seginnerbnr").append("<button class=\'btnconfig\' onclick=\'PreventiveMaintainenceTreeTable();\' type=\'button\' value=\'Cancel\' id=\'cancelButton\'>CANCEL</button><button class=\'btnconfig\' type=\'button\' value=\'Save\' onclick=\'multiedit_save_RL()\' id=\'saveButton\'>SAVE</button>");}else{$("#cancelButton").css("display", "block");$("#saveButton").css("display", "block");}$("'+str(table_ids)+' " +inp).closest("tr").find("td:nth-child("+edit_index+")").addClass("light_yellow"); document.getElementById("cont_multiEditModalSection").style.display = "none";  var divHeight = $("#cont_multiEditModalSection").height(); $("#cont_multiEditModalSection .modal-backdrop").css("min-height", divHeight+"px"); $("#cont_multiEditModalSection .modal-dialog").css("width","550px"); $(".modal-dialog").css("margin-top","100px"); } if (data2.length !== 0){ $.each( data2, function( key, values ) { onclick_datepicker(values) }); } } }); }                   $("'	
            + str(table_ids)	
            + "\").on('sort.bs.table', function (e, name, order) {  currenttab = $(\"ul#carttabs_head .active\").text().trim(); localStorage.setItem('"	
            + str(table_id)	
            + "_SortColumn', name); localStorage.setItem('"	
            + str(table_id)	
            + "_SortColumnOrder', order); }); "	
        )
                            
        return (
            sec_str,
            new_value_dict,
            dbl_clk_function                       
            )
    def Tool_Idle_Save(self, MODE):
        Trace.Write('cm to save===')
        new_dict = eval(DICT)
        for key,val in new_dict.items():
            Quote.GetCustomField(key).Content = str(val)
        Quote.Save() 
        return True               
            

objtool_idle = tool_idle()
MODE = Param.MODE
Trace.Write("Mode---"+str(MODE))
ACTION = Param.ACTION

if ACTION == "CONT_TOOL_IDLE":               
    ApiResponse = ApiResponseFactory.JsonResponse(objtool_idle.Contract_Tool_Idling(MODE))
if ACTION == "CONT_TOOL_IDLE_SAVE":
    DICT = Param.DICT               
    ApiResponse = ApiResponseFactory.JsonResponse(objtool_idle.Tool_Idle_Save(MODE))    

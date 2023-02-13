# =========================================================================================================================================
#   __script_name : SYUADNPMOD.PY
#   __script_description : THIS SCRIPT IS USED AS A MODULE FOR COMMONLY USED POPUP FUNCTIONALITIES
#   __primary_author__ : VIKNESH DURAISAMY
#   __create_date : 18/11/2022
# =========================================================================================================================================
from SYDATABASE import SQL
import SYCNGEGUID as CPQID

#Global variable declaration
Sql = SQL()

class AddnewPopuputilities:
    def constructing_table_footer(self,**kwargs):
        pagination_table_id = "pagination_{}".format(kwargs.get('id_name'))
        footer_str = """<div id="{Parent_Div_Id}" class="col-md-12 brdr listContStyle padbthgt30"><div class="col-md-4 pager-numberofitem clear-padding"><span class="pager-number-of-items-item flt_lt_pad2_mar2022" id="RecordsStartAndEnd">{Records_Start_And_End}</span><span class="pager-number-of-items-item flt_lt_pad2_mar" id="TotalRecordsCount">{Pagination_Total_Count}</span><div class="clear-padding fltltmrgtp3"><div class="pull-right vralign"><select onchange="ShowResultCountFunc(this,'{ShowResultCountFuncTb}','{OperationType}','{TableId}')" id="ShowResultCount" class="form-control selcwdt"><option value="10" {Selected_10}>10</option><option value="20" {Selected_20}>20</option><option value="50" {Selected_50}>50</option><option value="100" {Selected_100}>100</option><option value="200" {Selected_200}>200</option></select></div></div></div><div class="col-xs-8 col-md-4  clear-padding inpadtex" data-bind="visible: totalItemCount"><div class="clear-padding col-xs-12 col-sm-6 col-md-12 brd0"><ul class="pagination pagination"><li class="disabled"><a onclick="GetFirstResultFunc('{GetFirstResultFuncTb}','{OperationType}','{TableId}')" {Disable_First}><i class="fa fa-caret-left fnt14bold"></i><i class="fa fa-caret-left fnt14"></i></a></li><li class="disabled"><a onclick="GetPreviuosResultFunc('{GetPreviuosResultFuncTb}','{OperationType}','{TableId}')" {Disable_Previous}><i class="fa fa-caret-left fnt14"></i>PREVIOUS</a></li><li class="disabled"><a onclick="GetNextResultFunc('{GetNextResultFuncTb}','{OperationType}','{TableId}')" {Disable_Next}>NEXT<i class="fa fa-caret-right fnt14"></i></a></li><li class="disabled"><a onclick="GetLastResultFunc('{GetLastResultFuncTb}','{OperationType}','{TableId}')" {Disable_Last}><i class="fa fa-caret-right fnt14"></i><i class="fa fa-caret-right fnt14bold"></i></a></li></ul></div></div><div class="col-md-4 pad3"><span id="page_count" class="currentPage page_right_content">{Current_Page}</span><span class="page_right_content padrt2">Page </span></div></div></div>""".format(Parent_Div_Id=pagination_table_id,Records_Start_And_End=kwargs.get('records_start_and_end'),Pagination_Total_Count=kwargs.get('pagination_total_count'),ShowResultCountFuncTb=pagination_table_id,Selected_10="selected" if kwargs.get('fetch_count') == 10 else "",Selected_20="selected" if kwargs.get('fetch_count') == 20 else "",Selected_50="selected" if kwargs.get('fetch_count') == 50 else "",Selected_100="selected" if kwargs.get('fetch_count') == 100 else "",Selected_200="selected" if kwargs.get('fetch_count') == 200 else "",GetFirstResultFuncTb=pagination_table_id,Disable_First=kwargs.get('disable_previous_and_first'),GetPreviuosResultFuncTb=pagination_table_id,Disable_Previous=kwargs.get('disable_previous_and_first'),GetNextResultFuncTb=pagination_table_id,Disable_Next=kwargs.get('disable_next_and_last'),GetLastResultFuncTb=pagination_table_id,Disable_Last=kwargs.get('disable_next_and_last'),Current_Page=kwargs.get('current_page'),TableId=kwargs.get('TABLEID'),OperationType = kwargs.get('operation_type'),table_id =  kwargs.get('table_id'))
        return footer_str

    def dbl_clk_action(self,**kwargs):
        table_ids = kwargs.get('id_names')
        action_str = (
            '$("'+ str(table_ids)+ '").on("all.bs.table",function (e,name,args) { $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); }); $("'+ str(table_ids)+ '\ th.bs-checkbox div.th-inner").before("<div class=\'pad0brdbt\'>SELECT</div>"); $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>");')
        return action_str

    def filter_dropdown_action(self,**kwargs):
        table_id = kwargs.get('id_name')
        drop_down_str = ("try { if( document.getElementById('"+ str(table_id)+ "') ) { var listws = document.getElementById('"+ str(table_id)+ "').getElementsByClassName('filter-control');  for (i = 0; i < listws.length; i++) { document.getElementById('"+ str(table_id)+ "').getElementsByClassName('filter-control')[i].innerHTML = data6[i];  } for (j = 0; j < listws.length; j++) { if (data10[j] == 'select') { var dataAdapter = new $.jqx.dataAdapter(data8[j]); if(data11[j].length>5){ $('#"+ str(table_id)+ "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true,source: dataAdapter}); }else{$('#"+ str(table_id)+ "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true,source: dataAdapter ,autoDropDownHeight: true});} } } } }  catch(err) { setTimeout(function() { var listws = document.getElementById('"+ str(table_id)+ "').getElementsByClassName('filter-control');  for (i = 0; i < listws.length; i++) { document.getElementById('"+ str(table_id)+ "').getElementsByClassName('filter-control')[i].innerHTML = data9[i];  } for (j = 0; j < listws.length; j++) { if (data10[j] == 'select') { var dataAdapter = new $.jqx.dataAdapter(data11[j]); $('#"+ str(table_id)+ "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true,source: dataAdapter,scrollBarSize :10 }); } } },5000); }")
        return drop_down_str

    def get_types_list(self,ObjectName):
        Objd_Obj = Sql.GetList("SELECT FIELD_LABEL,API_NAME,LOOKUP_OBJECT,LOOKUP_API_NAME,DATA_TYPE,FORMULA_DATA_TYPE FROM SYOBJD (NOLOCK) WHERE OBJECT_NAME = '{ObjectName}'".format(ObjectName=ObjectName))
        lookup_disply_list = []
        has_obj = False
        if Objd_Obj is not None:
            has_obj = True            
            checkbox_list = []
            for attr in Objd_Obj:                
                if str(attr.LOOKUP_API_NAME) != "" and str(attr.LOOKUP_API_NAME) is not None:
                    lookup_disply_list.append(str(attr.API_NAME))
                if (attr.DATA_TYPE == "CHECKBOX" or attr.FORMULA_DATA_TYPE == "CHECKBOX"):
                    checkbox_list.append(str(attr.API_NAME))
            lookup_list = {ins.LOOKUP_API_NAME: ins.API_NAME for ins in Objd_Obj}
        return lookup_list,checkbox_list,lookup_disply_list,has_obj

    def construct_where_string(self,A_Keys,A_Values,ObjectName):
        where_string = ""
        guid_list = ['ACCOUNT_PARTNER_FUNCTION_ID','RECORD_ID']
        if A_Keys != "" and A_Values != "":
            for key, value in zip(list(A_Keys), list(A_Values)):
                if any(guid in key for guid in guid_list):
                    key = str(ObjectName)+".CpqTableEntryId"
                if value.strip():
                    where_string += " AND " if where_string else ''
                    if 'CpqTableEntryId' not in key:
                        key = ObjectName+".{}".format(key)
                    where_string += "{Key} LIKE '%{Value}%' ".format(Key=key, Value=value)
        return where_string

    def filter_dropdown_header(self,ordered_keys=[],obj_name=None,id_name=None):
        filter_tags = []
        filter_types = []
        filter_values = []
        for index,col_name in enumerate(ordered_keys):
            table,api_name = obj_name,col_name
            obj_data = Sql.GetFirst("SELECT API_NAME,DATA_TYPE,PICKLIST FROM  SYOBJD WHERE OBJECT_NAME='"+ str(table) + "' and API_NAME = '"+ str(api_name) + "'")
            if obj_data is not None:
                if str(obj_data.PICKLIST).upper() == "TRUE":
                    filter_tag = ('<div id = "'+ str(id_name)+ "_RelatedMutipleCheckBoxDrop_" + str(index) + '" class="form-control bootstrap-table-filter-control-'+ str(api_name) + " RelatedMutipleCheckBoxDrop_" + str(index) + ' "></div>')
                    filter_tags.append(filter_tag)
                    filter_types.append("select")
                    if obj_data.DATA_TYPE == "CHECKBOX":
                        filter_values.append(["True","False"])
                    else:
                        data_obj = Sql.GetList("SELECT DISTINCT {Column} FROM {Table}".format(Column=api_name,Table=table))
                        if data_obj is not None:
                            filter_values.append([row_data.Value for data in data_obj for row_data in data])
                else:
                    filter_tag = ('<input type="text" class="form-control wth100visble bootstrap-table-filter-control-'+ str(api_name) + '">')
                    filter_tags.append(filter_tag)
                    filter_types.append("input")
                    filter_values.append("")
        return filter_tags,filter_types,filter_values

    def construct_actions(self,label_name,ObjectName,func2):
        sec_str=''
        sec_str+=('<div class="row modulebnr brdr ma_mar_btm">'+str(label_name)+' : ADD NEW <button type="button" class="close flt_rt" onclick="closepopup_scrl()" data-dismiss="modal">X</button></div>')
        sec_str+='<div class="col-md-12"><div class="row pad-10 bg-lt-wt brdr">'
        sec_str+='<button type="button" class="btnconfig" onclick="closepopup_scrl()" data-dismiss="modal">CANCEL</button>'
        sec_str+=('<button type="button" id="'+ObjectName+'" class="btnconfig viewvalidate " onclick="'+func2+'">'+"SAVE"+"</button>")
        sec_str+="</div></div>"
        return str(sec_str)
    
    def get_script_details(self,TreeParam):
        saqsco_obj = "SAQSCO" if TreeParam == 'Add-On Products' else "SAQFEQ"
        script_details = {
            "SAQFBL":{
                "ID_NAME":"fablocation_addnew",
                "child_script_name":"SYADFBEPOP",
                "master_object_name":"MAFBLC"
            },
            "SAQSAF":{
                "ID_NAME":"add_fablocation_fts",
                "child_script_name":"SYADFTSPOP",
                "master_object_name":"MAFBLC"
            },
            "SAQASE":{
                "ID_NAME":"fts_equipments_addnew",
                "child_script_name":"SYADFTSPOP",
                "master_object_name":"MAEQUP"
            },
            "SYOBJR_00038":{
                "ID_NAME":"add_receiving_fab",
                "child_script_name":"SYADFTSPOP",
                "master_object_name":"SAQSAF"
            },
            "SAQSCN":{
                "ID_NAME":"nso_addnew",
                "child_script_name":"SYADNEQPOP",
                "master_object_name":"PRLPBE"
            },
            "SAQSAO":{
                "ID_NAME":"Include_add_on_addnew",
                "child_script_name":"SYADNEQPOP",
                "master_object_name":"MAADPR"
            },
            "SAQRCV":{
                "ID_NAME":"add_credits_add_new",
                "child_script_name":"SYADNEQPOP",
                "master_object_name":"SACRVC"
            },
            "SAQTSV":{
                "ID_NAME":"offerings-addnew-model",
                "child_script_name":"SYADSVEPOP",
                "master_object_name":"MAMTRL"
            },
            "Customer Information":{
                "ID_NAME":"add_receiving_equipment",
                "child_script_name":"SYADFBEPOP",
                "master_object_name":"SAQASE"
            },
            "SAQSCO":{
                "ID_NAME":"Coveredobjectsaddnew",
                "child_script_name":"SYADSVEPOP",
                "master_object_name": saqsco_obj
            },
            "UNMAPPED":{
                "ID_NAME":"unmapped_equipments_addnew",
                "child_script_name":"SYADFTSPOP",
                "master_object_name":"MAEQUP"
            },
            "SAQFEQ":{
                "ID_NAME":"equipments_addnew",
                "child_script_name":"SYADFBEPOP",
                "master_object_name":"MAEQUP"
            },
            "SAQRSP":{
                "ID_NAME":"parts-addnew-model",
                "child_script_name":"SYADSVEPOP",
                "master_object_name":"MAMTRL"
            },
            "SAQSPT":{
                "ID_NAME":"parts-addnew-model",
                "child_script_name":"SYADSVEPOP",
                "master_object_name":"MAMTRL"
            },
            "Deal Team Replace":{
                "ID_NAME":"contact_manager_addnew_model",
                "child_script_name":"SYADQTEPOP",
                "master_object_name":"SAEMPL" #A055S000P01-20984
            },
            "SAQICT":{
                "ID_NAME":"contact_replace_addnew_model",
                "child_script_name":"SYADQTEPOP",
                "master_object_name":"SACONT"
            },
            "Replace Involved Parties":{
                "ID_NAME":"replace-account",
                "child_script_name":"SYADQTEPOP",
                "master_object_name":"SAACPF" #A055S000P01-20984 
            }
        }
        return script_details

    def get_entitlement_xml(self,Service_Id,entitlement_xml,TreeParam,TableName,TreeSuperParentParam):
        import re
        iclusions_val_list = []
        quote_item_tag = re.compile(r'(<QUOTE_ITEM_ENTITLEMENT>[\w\W]*?</QUOTE_ITEM_ENTITLEMENT>)')
        pattern_non_consumable = re.compile(r'<ENTITLEMENT_ID>(?:AGS_'+str(Service_Id)+'[^>]*?_TSC_NONCNS|AGS_[^>]*?_NON_CONSUMABLE)</ENTITLEMENT_ID>')
        pattern_consumable = re.compile(r'<ENTITLEMENT_ID>AGS_'+str(Service_Id)+'[^>]*?_TSC_CONSUM</ENTITLEMENT_ID>')
        pattern_consumable_addon = re.compile(r'<ENTITLEMENT_ID>AGS_'+str(Service_Id)+'[^>]*?_TSC_CONADD</ENTITLEMENT_ID>')
        pattern_new_parts_only = re.compile(r'<ENTITLEMENT_ID>AGS_[^>]*?_TSC_RPPNNW</ENTITLEMENT_ID>')
        pattern_inclusion = re.compile(r'<ENTITLEMENT_DISPLAY_VALUE>Some Inclusions</ENTITLEMENT_DISPLAY_VALUE>')
        pattern_exclusion = re.compile(r'<ENTITLEMENT_DISPLAY_VALUE>Some Exclusions</ENTITLEMENT_DISPLAY_VALUE>')
        pattern_new_parts_only_yes = re.compile(r'<ENTITLEMENT_DISPLAY_VALUE>Yes</ENTITLEMENT_DISPLAY_VALUE>')
        new_parts_yes = ""
        for m in re.finditer(quote_item_tag,entitlement_xml):
            sub_string = m.group(1)
            non_consumable =re.findall(pattern_non_consumable,sub_string)
            consumable =re.findall(pattern_consumable,sub_string)
            consumable_addon = re.findall(pattern_consumable_addon,sub_string)
            get_inclusion =re.findall(pattern_inclusion,sub_string)
            get_exclusion = re.findall(pattern_exclusion,sub_string)
            new_parts_only = re.findall(pattern_new_parts_only,sub_string)
            new_parts_only_value = re.findall(pattern_new_parts_only_yes,sub_string)
            if new_parts_only and new_parts_only_value:
                new_parts_yes = "Yes"
                break
            if (non_consumable and get_inclusion) or (non_consumable and get_exclusion):
                if TreeSuperParentParam == "Product Offerings" and TreeParam =='Z0092' and non_consumable and get_exclusion:
                    iclusions_val_list.append('N')
                elif (TreeSuperParentParam == "Product Offerings" and TreeParam !='Z0092') or TableName == "SAQSGE":
                    iclusions_val_list.append('N')
            elif(consumable and get_inclusion) or (consumable and get_exclusion):
                if TreeSuperParentParam == "Product Offerings" and TreeParam =='Z0092' and consumable and get_inclusion:
                    iclusions_val_list.append('C')
                elif (TreeSuperParentParam == "Product Offerings" and TreeParam !='Z0092') or TableName == "SAQSGE":
                    iclusions_val_list.append('C')
            elif(consumable_addon and get_inclusion) or (consumable_addon and get_exclusion):
                if TreeSuperParentParam == "Product Offerings" and TreeParam =='Z0092' and consumable and get_inclusion:
                    iclusions_val_list.append('C')
                elif (TreeSuperParentParam == "Product Offerings" and TreeParam !='Z0092') or TableName == "SAQSGE":
                    iclusions_val_list.append('C')
        return iclusions_val_list,new_parts_yes
            
    def get_header_details(self,ObjectName,TreeParam):
        if ObjectName in ("SAQSCO","SAQFEQ"):
            if TreeParam=='Add-On Products':
                Header_details={"QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID": "KEY","EQUIPMENT_ID": "EQUIPMENT ID","EQUIPMENTCATEGORY_DESCRIPTION": "EQUIPMENT CATEGORY","SERIAL_NO": "SERIAL NUMBER","CUSTOMER_TOOL_ID": "CUSTOMER TOOL ID","GREENBOOK": "GREENBOOK","EQUIPMENT_STATUS": "EQUIPMENT STATUS","PLATFORM": "PLATFORM","FABLOCATION_ID": "FABLOCATION ID","WARRANTY_START_DATE": "WARRANTY START DATE","WARRANTY_END_DATE": "WARRANTY END DATE","WARRANTY_END_DATE_ALERT": "WARRANTY END DATE ALERT"}
                ordered_keys=["QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID","EQUIPMENT_ID","EQUIPMENTCATEGORY_DESCRIPTION","SERIAL_NO","CUSTOMER_TOOL_ID","GREENBOOK","EQUIPMENT_STATUS","PLATFORM","FABLOCATION_ID","WARRANTY_START_DATE","WARRANTY_END_DATE","WARRANTY_END_DATE_ALERT"]
            else:
                Header_details={"QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID": "KEY","EQUIPMENT_ID": "EQUIPMENT ID","EQUIPMENT_DESCRIPTION":"EQUIPMENT_DESCRIPTION","EQUIPMENTCATEGORY_DESCRIPTION":"EQUIPMENT CATEGORY DESCRIPTION","SERIAL_NUMBER": "SERIAL NUMBER","CUSTOMER_TOOL_ID":"CUSTOMER TOOL ID","GREENBOOK": "GREENBOOK","PLATFORM": "PLATFORM","WAFER_SIZE":"WAFER SIZE","FABLOCATION_ID": "FAB LOCATION ID","FABLOCATION_NAME": "FAB LOCATION NAME","KPU":"KPU","TECHNOLOGY":"TECHNOLOGY","TEMP_TOOL":"TEMP TOOL"}
                ordered_keys=["QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID","EQUIPMENT_ID","EQUIPMENT_DESCRIPTION","EQUIPMENTCATEGORY_DESCRIPTION","SERIAL_NUMBER","CUSTOMER_TOOL_ID","GREENBOOK","PLATFORM","WAFER_SIZE","FABLOCATION_ID","FABLOCATION_NAME","KPU","TECHNOLOGY","TEMP_TOOL"]
        elif ObjectName=="SAQTSV":
            Header_details={"MATERIAL_RECORD_ID": "KEY","SAP_PART_NUMBER": "PRODUCT OFFERING ID","SAP_DESCRIPTION": "PRODUCT OFFERING DESCRIPTION"}
            ordered_keys=["MATERIAL_RECORD_ID","SAP_PART_NUMBER","SAP_DESCRIPTION"]
        elif ObjectName in ("SAQRSP","SAQSPT"):
            Header_details={"MATERIAL_RECORD_ID":"KEY","SAP_PART_NUMBER":"PART NUMBER","SAP_DESCRIPTION":"PART DESCRIPTION","MATPRIGRP_ID":"MATERIAL PRICING GROUP ID"}
            ordered_keys=["MATERIAL_RECORD_ID","SAP_PART_NUMBER","SAP_DESCRIPTION","MATPRIGRP_ID"]
        return Header_details,ordered_keys

    def gettable_data(self,ObjectName,table_data,key,value,operation_type):
        date_field = []
        if table_data is not None:
            for row_data in table_data:
                new_value_dict={}
                for data in row_data:
                    if str(data.Key)==key:
                        pop_val=str(data.Value)+''+str(value)
                        cpqidval=CPQID.KeyCPQId.GetCPQId(ObjectName,str(data.Value))
                    else:
                        cpqidval=data.Value
                    new_value_dict[data.Key]=cpqidval
                    new_value_dict["pop_val"]=pop_val
                date_field.append(new_value_dict)
        return date_field

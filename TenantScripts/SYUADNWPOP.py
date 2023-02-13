#=========================================================================================================================================
#   __script_name : SYUADNWPOP.PY
#   __script_description : THIS SCRIPT IS USED TO NAVIGATE THE SCRIPT EXECUTION BASED ON LEVELS & OPEN A POPUP WHEN USER CLICKS ON ADD OR NEW ACTION BUTTON ON A RELATED LIST RECORD
#   __primary_author__ : ASHA LYSANDAR
#   __create_date : 26/08/2020
#=========================================================================================================================================
from SYDATABASE import SQL
import SYUADNPMOD
poputilObj=SYUADNPMOD.AddnewPopuputilities()
import Webcom.Configurator.Scripting.Test.TestProduct
Sql=SQL()
TestProduct=Webcom.Configurator.Scripting.Test.TestProduct()
def POPUPLISTVALUEADDNEW(TABLEID,RECORDID,RECORDFEILD,NEWVALUE,LOOKUPOBJ,LOOKUPAPI,OPER,A_Keys,A_Values,DIVNAME,TreeParentParam,PerPage,PageInform,active_subtab):
    filter_tags=filter_types=filter_values=date_field=[]
    api_name=sec_str=SaveCancel=record_field=record_value=table_header=dbl_clk_function=var_str=RECORD_FEILD=pagedata=QryCount=TreeParentParam=filter_drop_down=filter_control_function=primary_value=""
    new_value_dict={}
    func2="popup_cont_SAVE(this,'"+DIVNAME+"')"
    child_script=True
    primary_value=RECORDID
    try:
        contract_quote_record_id=Quote.GetGlobal("contract_quote_record_id")
        quote_revision_record_id=Quote.GetGlobal("quote_revision_record_id")
    except:
        contract_quote_record_id=''
        quote_revision_record_id=''
    try:
        TreeParam=Product.GetGlobal("TreeParam")
        TreeParentParam=Product.GetGlobal("TreeParentLevel0")
        TreeTopSuperParentParam=Product.GetGlobal("TreeParentLevel2")
    except:
        TreeParam=TreeParentParam=TreeTopSuperParentParam=''
    try:
        if (TABLEID !="ADDNEW__SYOBJR_93123_SYOBJ_00267" and TABLEID !="ADDNEW__SYOBJR_98788_SYOBJ_00907") and RECORD_FEILD !="":
            RECORD_FEILD=RECORD_FEILD[1]+"-"+RECORD_FEILD[2]+"-"+RECORD_FEILD[3]
        elif (TABLEID !="ADDNEW__SYOBJR_95800_SYOBJ_00458" and TABLEID !="ADDNEW__SYOBJR_98788_SYOBJ_00907") and RECORD_FEILD !="":
            RECORD_FEILD=RECORD_FEILD[1]+"-"+RECORD_FEILD[2]+"-"+RECORD_FEILD[3]
        elif RECORD_FEILD !="":
            RECORD_FEILD=RECORDFEILD.split("_")
    except:
        Trace.Write("RECORD_FEILD is missing")
    try:
        if TABLEID.startswith("SYOBJR"):
            TABLE_ID=""
        else:
            TABLE_ID=TABLEID.split("__")
    except:
        TABLE_ID=""
    try:
        if TABLE_ID:
            popup_table_id=TABLE_ID[1]
        else:
            popup_table_id=TABLEID
        if '_' in popup_table_id:
            popup_table_id=popup_table_id.split("_")
            popup_table_id=popup_table_id[0]+"-"+popup_table_id[1]
    except:
        popup_table_id=""
    try:
        CurrentTab=str(TestProduct.CurrentTab)
    except:
        CurrentTab='Quotes'
    popup_lable_obj=Sql.GetFirst("SELECT NAME,OBJ_REC_ID FROM SYOBJR (NOLOCK) WHERE SAPCPQ_ATTRIBUTE_NAME='{popup_table_id}'".format(popup_table_id=popup_table_id))
    if popup_lable_obj is not None:
        Question_obj=Sql.GetFirst("SELECT OBJECT_NAME,LABEL FROM SYOBJH (NOLOCK) WHERE RECORD_ID='{popup_lable_obj_id}'".format(popup_lable_obj_id=popup_lable_obj.OBJ_REC_ID))
    else:
        Question_obj=Sql.GetFirst("SELECT OBJECT_NAME,LABEL FROM SYOBJH (NOLOCK) WHERE SAPCPQ_ATTRIBUTE_NAME='SYOBJ-00263'")
    if TABLEID !="ADDNEW__SYOBJR_93123_SYOBJ_00267" or TABLEID !="ADDNEW__SYOBJR_98788_SYOBJ_00907":
        if TABLEID !="ADDNEW__SYOBJR_95800_SYOBJ_00458":
            rec_field=Sql.GetFirst("SELECT API_NAME,API_FIELD_NAME FROM SYSEFL (NOLOCK) WHERE SAPCPQ_ATTRIBUTE_NAME='"+str(RECORD_FEILD)+"'")
            if rec_field is not None and rec_field !="":
                record_field=str(eval("rec_field.API_FIELD_NAME"))
                record_value=str(eval("rec_field.API_NAME"))
            else:
                record_field=record_value=""
    if str(popup_table_id)=="SYOBJR-94489":
        record_value=TreeParentParam
    TabName='Quote'
    for tab in Product.Tabs:
        if tab.IsSelected==True:
            TabName=str(tab.Name)
    offset_skip_count=Offset_Skip_Count
    if offset_skip_count==1:
        offset_skip_count=0
    fetch_count=Fetch_Count
    selected_offerings_list_preslect=[]
    if Question_obj is not None:
        if str(popup_table_id)=="SYOBJR-98859":
            ObjectName="SAQSAO"
        else:
            ObjectName=str(Question_obj.OBJECT_NAME).strip()
        if TABLEID=="ADDNEW__SYOBJR_00038_SYOBJ_00919":
            ObjectName="SAQFBL"
        elif "SYOBJR_00038" in TABLEID:
            ObjectName="SYOBJR_00038"
        elif ObjectName=="SAQFEQ" and TreeParam=="Customer Information":
            ObjectName="Customer Information"
        elif TABLEID.startswith("UNMAPPED"):
            ObjectName="UNMAPPED"
        elif ObjectName=="SAQTIP" and (str(tool_type)=="REPLACE" or str(ACTION)=="REPLACE"):
            ObjectName="Replace Involved Parties"
        elif ObjectName=="SAQDLT" and ACTION=="REPLACE":
            ObjectName="Deal Team Replace"
        script_details=poputilObj.get_script_details(TreeParam)
        if ObjectName not in script_details.Keys:
            child_script=False
            Sqq_obj=Sql.GetList("SELECT top 1000 API_NAME,DATA_TYPE,FORMULA_DATA_TYPE,LOOKUP_OBJECT,REQUIRED,PERMISSION,FIELD_LABEL,LOOKUP_API_NAME,LENGTH FROM  SYOBJD (NOLOCK) WHERE LTRIM(RTRIM(OBJECT_NAME))='"+ObjectName+"'ORDER BY abs(DISPLAY_ORDER)")
            lookup_val=[val.LOOKUP_API_NAME for val in Sqq_obj]
            lookup_list={ins.LOOKUP_API_NAME: ins.LOOKUP_OBJECT for ins in Sqq_obj}
            lookup_list1={ins.LOOKUP_API_NAME: ins.API_NAME for ins in Sqq_obj}            
            result=ScriptExecutor.ExecuteGlobal("SYPARCEFMA",{"Object":ObjectName,"API_Name":record_field,"API_Value":str(primary_value),},)
            new_value_dict1={API_Names.get("API_NAME"): API_Names.get("FORMULA_RESULT") for API_Names in result}
            attrval_obj=Sql.GetFirst("SELECT API_NAME FROM SYOBJD(NOLOCK) WHERE OBJECT_NAME='"+ObjectName+"' AND LOOKUP_OBJECT='"+str(record_value)+"' ")
            if attrval_obj:
                api_name=attrval_obj.API_NAME.strip()
                result=ScriptExecutor.ExecuteGlobal("SYPARCEFMA",{"Object": ObjectName,"API_Name": api_name,"API_Value": str(primary_value),},)
                new_value_dict_new={}
                new_value_dict_new[api_name]=str(primary_value)
                new_value_dict.update({API_Names.get("API_NAME"): API_Names.get("FORMULA_RESULT") for API_Names in result})            
            if NEWVALUE !="":
                if str(OPER)=="CLEAR SELECTION":
                    attrval_obj=Sql.GetFirst("SELECT API_NAME FROM  SYOBJD (NOLOCK) WHERE OBJECT_NAME='"+ObjectName+"' AND LOOKUP_OBJECT='"+str(NEWVALUE)+"'")
                    api_name=attrval_obj.API_NAME.strip()
                    TABLE_OBJS=Sql.GetList( "select OBJECT_NAME,API_NAME,DATA_TYPE,LOOKUP_OBJECT,FORMULA_LOGIC FROM  SYOBJD (NOLOCK) where OBJECT_NAME='"+ObjectName+"' and FORMULA_LOGIC like '%"+str(api_name)+"%'")
                    if TABLE_OBJS is not None:
                        for TABLE_OBJ in TABLE_OBJS:
                            if TABLE_OBJ.DATA_TYPE !="":
                                if api_name in str(TABLE_OBJ.FORMULA_LOGIC):
                                    new_value_dict[str(TABLE_OBJ.API_NAME)]=""
                                    new_value_dict[str(api_name)]=""
                else:
                    attrval_obj=Sql.GetFirst("SELECT API_NAME FROM SYOBJD (NOLOCK) WHERE OBJECT_NAME='"+ObjectName+"' AND LOOKUP_OBJECT='"+str(LOOKUPOBJ)+"' and  LOOKUP_API_NAME='"+str(LOOKUPAPI)+"'")
                    if attrval_obj:
                        api_name=attrval_obj.API_NAME.strip()
                        if api_name:
                            NEWVALUE=NEWVALUE.split("|")
                            result=ScriptExecutor.ExecuteGlobal("SYPARCEFMA",{"Object": ObjectName,"API_Name": api_name,"API_Value": NEWVALUE[0],},)
                            new_value_dict={API_Names.get("API_NAME"): API_Names.get("FORMULA_RESULT") for API_Names in result}
                            if api_name=="OBJECTFIELD_RECORD_ID" and popup_table_id=="SYOBJR-95825":
                                APIName_value=new_value_dict.get("OBJECTFIELD_APINAME")
                                RecAtt_objval=Product.Attr("QSTN_SYSEFL_SY_09875").GetValue()
                                getobjd_val=Sql.GetFirst("SELECT * FROM SYOBJD WHERE OBJECT_NAME='"+str(RecAtt_objval)+"' and API_NAME='"+str(APIName_value)+"' and DATA_TYPE='LOOKUP'")
                                if getobjd_val:
                                    new_value_dict["REFOBJECT_APINAME"]=str(getobjd_val.LOOKUP_OBJECT)
                            if TABLEID=='ADDNEW__SYOBJR_00014_SYOBJ_01024' and LOOKUPAPI=='PROFILE_ID':
                                api_name='PROFILE_RECORD_ID'
            else:
                attrval_obj=Sql.GetFirst("SELECT API_NAME FROM SYOBJD(NOLOCK) WHERE OBJECT_NAME='"+ObjectName+"' AND LOOKUP_OBJECT='"+str(record_value)+"' ")
                if attrval_obj is not None:
                    api_name=attrval_obj.API_NAME.strip()
                    result=ScriptExecutor.ExecuteGlobal("SYPARCEFMA",{"Object": ObjectName,"API_Name": api_name,"API_Value": str(primary_value),},)
                    new_value_dict={API_Names.get("API_NAME"): API_Names.get("FORMULA_RESULT") for API_Names in result}
                    new_value_dict.update({api_name:str(primary_value)})
            GettreeEnable=Sql.GetFirst("select ENABLE_TREE FROM SYTABS where SAPCPQ_ALTTAB_NAME='"+str(TabName)+"'")
            if GettreeEnable is None or str(GettreeEnable.ENABLE_TREE).upper() !="TRUE":
                sec_str+=poputilObj.construct_actions(str(popup_lable_obj.NAME).upper(),ObjectName,func2)
            sec_str+='<div id="Headerbnr" class="mart_col_back"></div><div class="col-md-12"  style="display: none;"><div class="row modulesecbnr brdr" data-toggle="collapse" data-target="#SegAlert_notifcation" aria-expanded="true" >NOTIFICATIONS<i class="pull-right fa fa-chevron-down "></i><i class="pull-right fa fa-chevron-up"></i></div><div  id="SegAlert_notifcation" class="col-md-12  alert-notification  brdr collapse in" ><div class="col-md-12 alert-warning" id="alert_msg"><label><img src="/mt/APPLIEDMATERIALS_PRD/Additionalfiles/warning1.svg" alt="Warning"></label></div></div></div>'
            if GettreeEnable is not None and str(GettreeEnable.ENABLE_TREE).upper()=="TRUE":
                if str(popup_table_id)=="SYOBJR-98798":
                    sec_str+=('<div id="container" text="'+ObjectName+'" class="except_sec">')
                else:
                    sec_str+=('<div id="container" text="'+ObjectName+'" class="g4 pad-10 brdr except_sec header_section_div">')
                sec_str+=('<div class="container_banner_inner_sec" style="display:none"><span style="display:none" id="container_banner_id">'+str(popup_lable_obj.NAME).upper()+" : ADD NEW</span></div>")
            else:
                sec_str+=('<div id="container" text="'+ObjectName+'" class="g4 pad-10 brdr except_sec">')
            sec_str+='<table class="width100">'
            if Sqq_obj is not None:
                for val in Sqq_obj:
                    current_obj_api_name=val.API_NAME.strip()
                    current_obj_field_lable=val.FIELD_LABEL.strip()
                    data_type=val.DATA_TYPE.strip()
                    formula_data_type=str(val.FORMULA_DATA_TYPE).strip()
                    current_obj_value=readonly=disable=formula_permission=formula_obj_permission=checked=parrent_object_name=add_style=onchange=""
                    max_length=val.LENGTH
                    datepicker="onclick_datepicker('"+current_obj_api_name+"')"
                    datepicker_onchange="onchangedatepicker('"+current_obj_api_name+"')"
                    edit_pencil_icon=edit_icon='<i class="fa fa-pencil" aria-hidden="true"></i>'
                    lock_icon = '<i class="fa fa-lock" aria-hidden="true"></i>'
                    if current_obj_api_name in lookup_val:
                        for key,value in lookup_list.items():
                            if key==current_obj_api_name:
                                parrent_object_name=value.strip()
                    if current_obj_api_name in lookup_val:
                        formula_obj_permission="true"
                        for key,value in lookup_list1.items():
                            if key==current_obj_api_name:
                                formula_permission_qry=Sql.GetFirst("SELECT * FROM SYOBJD(NOLOCK) WHERE API_NAME='"+ value+ "' and OBJECT_NAME='"+ ObjectName+ "' ")
                                formula_permission=str(formula_permission_qry.PERMISSION).strip()
                    if val.PERMISSION.strip()=="READ ONLY":
                        if formula_obj_permission=="true" and formula_permission !="READ ONLY":
                            edit_pencil_icon=edit_icon
                        else:
                            edit_pencil_icon=lock_icon
                            readonly="readonly"
                            disable="disabled"
                    if current_obj_api_name in new_value_dict1:
                        if str(current_obj_api_name)=="TO_CURRENCY" or (str(current_obj_api_name)=="TAB_NAME" and ObjectName=="SYPSAC" and str(TreeParam)=="Actions"):
                            edit_pencil_icon=edit_icon
                        else:
                            if readonly=="readonly":
                                readonly="readonly"
                                edit_pencil_icon=lock_icon
                            else:
                                if str(current_obj_api_name)=="NODE_PAGE_NAME":
                                    readonly="readonly"
                                    edit_pencil_icon=lock_icon
                                else:
                                    readonly=''
                                    edit_pencil_icon=edit_icon
                            disable="disabled"
                    if current_obj_api_name in ["CPQTABLEENTRYADDEDBY","CPQTABLEENTRYDATEADDED","CpqTableEntryModifiedBy","CpqTableEntryDateModified","OWNER_ID","OWNED_DATE","ATTVAL_VALFORMULA","DELEGATED_APPROVER_ID","DELEGATION_END","DELEGATION_START","TAB_ID"]:
                        add_style="display: none;"
                    if (ObjectName=="SYSECT") and current_obj_api_name in ["SAPCPQ_ATTRIBUTE_NAME","PARENT_SECTION_TEXT","SECTION_PARTNUMBER"]:
                        add_style="display: none;"
                    if (ObjectName=="SYTABS") and current_obj_api_name in ["TAB_ID"] and CurrentTab.upper()=="PAGE":
                        add_style="display: none;"
                    if (ObjectName=="SAQTIP") and current_obj_api_name in["QUOTE_ID","QUOTE_NAME","SALESORG_ID","SALESORG_NAME","QTEREV_ID"]:
                        add_style="display: none;"
                    if data_type=="AUTO NUMBER":
                        sec_str+=('<tr class="iconhvr borbot1" style="display: none;"><td class="width350"><label class="fltltpadlt15">'+str(current_obj_field_lable)+'</label></td><td class="width40"><a class="color_align_width" href="#" data-placement="top" data-toggle="popover" title="'+ str(current_obj_field_lable)+'" data-content="'+str(current_obj_field_lable)+'" ><i class="fa fa-info-circle flt_lt"></i>')
                        if str(val.REQUIRED).upper()=="TRUE" or val.REQUIRED=="1":
                            sec_str+=""
                        sec_str+="</a></td>"
                        sec_str+=('<td><input id="'+str(current_obj_api_name)+'" type="text" value="'+str(Guid.NewGuid()).upper()+'" class="form-control related_popup_css" hidden disabled></td>')
                        sec_str+='<td class="float_r_bor_bot"><div class="col-md-12 editiconright"><a href="#" class="editclick"><i class="fa fa-pencil" aria-hidden="true"></i></a></div></td>'
                        sec_str+="</tr>"
                    if data_type !="AUTO NUMBER":
                        if (data_type=="LOOKUP" or current_obj_api_name=="REFOBJECT_APINAME" or current_obj_api_name=="REFOBJECTFIELD_APINAME"):
                            add_style="display: none;"
                        sec_str+=('<tr class="iconhvr borbot1" style=" '+str(add_style)+'"><td class="width350"><label class="fltltpadlt">'+str(current_obj_field_lable)+'</label></td><td class="width40"><a class="bgcccwth10" href="#" data-placement="top" title="'+ str(current_obj_field_lable)+'" data-toggle="popover" data-content="'+str(current_obj_field_lable)+'"><i class="fa fa-info-circle flt_lt"></i>')
                        if val.REQUIRED:
                            if str(val.REQUIRED).upper()=="TRUE" or str(val.REQUIRED)=="1":
                                sec_str+='<span class="req-field mrg3fltltmt7">*</span>'
                            sec_str+="</a></td>"
                        if data_type=="LOOKUP":
                            if current_obj_api_name in new_value_dict:
                                current_obj_value=new_value_dict[current_obj_api_name]
                            try:
                                if current_obj_api_name in new_value_dict1:
                                    current_obj_value=new_value_dict1.get(str(current_obj_api_name))
                            except:
                                Trace.Write("lookup field is not in main list")
                            sec_str+=('<td><input id="'+str(current_obj_api_name)+'" value="'+str(current_obj_value)+'" type="text" class="form-control related_popup_css" disabled></td>')
                        elif data_type=="FORMULA" and formula_data_type !="CHECKBOX":
                            if current_obj_api_name=="TO_CURRENCY":
                                if current_obj_api_name in lookup_val and readonly !="readonly":
                                    sec_str+=("<td><input id='"+str(current_obj_api_name)+"' type='text' value='"+str(current_obj_value)+"' class='form-control related_popup_css fltltlightyello' disabled>")
                                    sec_str+=("<input class='popup flt_lt' id='"+str(parrent_object_name)+"' data-target='#cont_viewModalSection' onclick='cont_lookup_popup_new(this)' type='image'  src='../mt/default/images/customer_lookup.gif'></td>")
                            elif current_obj_api_name=="USER_NAME":
                                sec_str+=("<td><input id='"+str(current_obj_api_name)+"' type='text' value='"+str(current_obj_value)+"' class='form-control related_popup_css fltltlightyello'>")
                                sec_str+=("<input class='popup flt_lt' id='"+str(current_obj_api_name)+"' data-target='#cont_viewModalSection' onclick='cont_lookup_popup_new(this)' type='image'  src='../mt/default/images/customer_lookup.gif'></td>")
                            elif current_obj_api_name=="OBJECTFIELD_APINAME":
                                cont_event_name="cont_lookup_popup_new(this,\"VIEW_DIV_ID\")"
                                sec_str+=("<td><input id='"+str(current_obj_api_name)+"' type='text' value='"+str(current_obj_value)+"' class='form-control related_popup_css fltltlightyello'>")
                                sec_str+=('<input class="popup flt_lt" id="'+str(parrent_object_name)+'" data-target="#cont_viewModalSection" onclick="'+cont_event_name+'" type="image" data-toogle="modal" src="../mt/default/images/customer_lookup.gif"></td>')
                            elif ( str(current_obj_api_name)=="MESSAGE_HEADERVALUE" or str(current_obj_api_name)=="MESSAGE_BODYVALUE"):
                                GetPrimeKey=Product.Attributes.GetByName("QSTN_SYSEFL_AC_00075").GetValue()
                                sec_str+="<td>"
                                sec_str+=('<div class="row"><div id="div_PICKLISTLOAD_'+str(current_obj_api_name)+'" class="multiselect"><select id="First'+str(current_obj_api_name)+'" multiple="multiple"'+str(onchange)+' value="'+current_obj_value+'" class="form-control pop_up_brd_rad related_popup_css fltlt options_'+str(current_obj_api_name)+' "  '+" >")
                                currectvaluelist=current_obj_value.split(",")
                                splitedlist=str(currectvaluelist).replace("[","").replace("]","")
                                if len(currectvaluelist)==1 and currectvaluelist[0]=="":
                                    splitedlist="'1'"
                                if str(current_obj_api_name)=="MESSAGE_HEADERVALUE":
                                    Tier_List=Sql.GetList("""SELECT SYOBJD.FIELD_LABEL  FROM ACAPCH (NOLOCK) INNER JOIN SYOBJH (NOLOCK) ON ACAPCH.APROBJ_RECORD_ID=SYOBJH.RECORD_ID INNER JOIN SYOBJD (NOLOCK) ON SYOBJD.OBJECT_NAME=SYOBJH.OBJECT_NAME WHERE APPROVAL_CHAIN_RECORD_ID='{chainrecordId}' AND SYOBJD.FIELD_LABEL NOT in ({exceptlist})""".format( chainrecordId=str(GetPrimeKey),exceptlist=splitedlist))
                                    for req1 in Tier_List:
                                        sec_str+="<option>"+str(req1.FIELD_LABEL)+"</option>"
                                sec_str+=('</select><div id="button_mvmt1"><button onclick="unselectedval(this)" '+'class="leftbutton" id="'+str(current_obj_api_name)+'"><i class="glyphicon glyphicon-triangle-left"></i></button> '+'<button onclick="selectedval(this)" id="'+str(current_obj_api_name)+'" class="rightbutton"><i class="glyphicon glyphicon-triangle-right"></i></button> '+'</div><select multiple="multiple" id="options1_'+str(current_obj_api_name)+'" >')
                                for listval in currectvaluelist:
                                    sec_str+="<option>"+str(listval)+"</option>"
                                sec_str+=('</select><div id="button_mvmt"><button class="topbutton" onclick="topselect(this)" id="'+str(current_obj_api_name)+'"><i class="glyphicon glyphicon-triangle-top"></i> '+'</button><button class="btmbutton"'+' onclick="btmselect(this)"id="'+str(current_obj_api_name)+'" ><i class="glyphicon glyphicon-triangle-bottom"></i> '+"</button></div></div></div></td>" )
                            elif (current_obj_api_name in ("SECTION_NAME","TREE_NAME") or (current_obj_api_name=="PAGE_NAME" and ObjectName=="SYPGAC") or (current_obj_api_name=="PAGE_LABEL" and ObjectName=="SYSECT")):
                                sec_str+=("<td><input id='"+str(current_obj_api_name)+"' type='text' value='"+str(TreeParentParam) +"' class='form-control related_popup_css' disabled>")
                            elif current_obj_api_name=="PAGE_NAME" and ObjectName=="SYSECT":
                                getpgname=Sql.GetFirst("select PAGE_NAME from SYPAGE where PAGE_LABEL='"+ str(TreeParentParam)+ "'")
                                if getpgname:
                                    input_value=str(getpgname.PAGE_NAME)
                                else:
                                    input_value=str(TreeParentParam)
                                sec_str+=("<td><input id='"+str(current_obj_api_name)+"' type='text' value='"+str(input_value) +"' class='form-control related_popup_css' disabled>")
                            elif current_obj_api_name=="PRIMARY_OBJECT_NAME" and ObjectName=="SYSECT":
                                gettabname=Sql.GetFirst("SELECT OBJECT_APINAME FROM SYPAGE (NOLOCK) WHERE RECORD_ID='"+str(new_value_dict['PAGE_RECORD_ID']+"'"))
                                if gettabname:
                                    input_value=str(gettabname.OBJECT_APINAME)
                                else:
                                    input_value=str(TreeParentParam)
                                sec_str+=("<td><input id='"+str(current_obj_api_name)+"' type='text' value='"+str(input_value) +"' class='form-control related_popup_css' disabled>")
                            else:
                                if (parrent_object_name !=record_value and current_obj_api_name in lookup_val and readonly !="readonly"):
                                    sec_str+=("<td><input id='"+str(current_obj_api_name)+"' type='text' value='"+str(current_obj_value)+"' class='form-control related_popup_css fltltlightyello'"+" >")
                                    if GettreeEnable is not None and str(GettreeEnable.ENABLE_TREE).upper()=="TRUE":
                                        cont_event_name="cont_lookup_popup_new(this,\"VIEW_DIV_ID\")"
                                        toggle="data-toggle='modal' "
                                    else:
                                        cont_event_name="cont_lookup_popup_new(this,\"\")"
                                        toggle=""
                                    sec_str+=("<input class='popup flt_lt' id='"+str(parrent_object_name)+"' data-target='#cont_viewModalSection' onclick='"+cont_event_name+"' type='image' "+str(toggle)+" src='../mt/default/images/customer_lookup.gif'></td>")
                                else:
                                    try:
                                        if current_obj_api_name in new_value_dict1:
                                            current_obj_value=new_value_dict1.get(str(current_obj_api_name))
                                    except:
                                        Trace.Write("Formula field is not in the main list")
                                    sec_str+=("<td><input id='"+str(current_obj_api_name)+"' type='text' value='"+str(current_obj_value)+"' class='form-control related_popup_css flt_lt' {}></td>".format("disabled" if readonly=="readonly" else ""))
                        elif data_type=="CHECKBOX" or formula_data_type=="CHECKBOX":
                            current_val=new_value_dict1.get(str(current_obj_api_name))
                            if str(current_val).upper()=="TRUE" :
                                current_obj_value="checked"
                            elif str(current_obj_api_name) !="ACTIVE" and str(current_obj_api_name) !="ENABLE_SMARTAPPROVAL" and str(current_obj_api_name) !="REQUIRE_EXPLICIT_APPROVAL" and str(current_obj_api_name) !="UNANIMOUS_CONSENT":
                                sec_str+=('<td><input id="'+str(current_obj_api_name)+'" value="'+str(current_obj_value)+'" '+checked+' type="'+str(data_type)+'" class="custom" '+disable+' ><span class="lbl"></span></td>' )
                            checklist=["ACTIVE","ENABLE_SMARTAPPROVAL","UNANIMOUS_CONSENT"]
                            if str(current_obj_api_name) in checklist:
                                checked = " checked "
                            if str(current_obj_api_name)=="REQUIRE_EXPLICIT_APPROVAL":
                                sec_str+=('<td><input id="'+str(current_obj_api_name)+'"  value="'+str(current_obj_value)+'" '+checked+' type="'+str(data_type)+'" class="custom" onchange="oncheckchange(this)" '+disable+' ><span class="lbl"></span></td>')
                        elif data_type=="DATE":
                            date_field.append(current_obj_api_name)
                            sec_str+=('<td class="wth324"><input id="'+str(current_obj_api_name)+'" value="'+str(current_obj_value)+'" type="text" class="form-control datePickerField wth155flrt" onclick="'+str(datepicker)+'" onchange="'+str(datepicker_onchange)+'"  '+disable+"></td>")
                        elif data_type=="PICKLIST":
                            if ObjectName=="SYOBJD" or ObjectName=="ACACSA":
                                on_changeevt = 'onchange="onFieldChanges(this)"'
                            else:
                                on_changeevt = ''
                            sec_str+=('<td><select id="'+str(current_obj_api_name)+'" value="'+str(current_obj_value)+'" type="text" class="form-control pop_up_brd_rad related_popup_css hgt32fnt13 light_yellow" '+disable+" "+on_changeevt+"><option value='Select'>..Select</option>")
                            Sql_Quality_Tier=Sql.GetFirst("select PICKLIST_VALUES FROM  SYOBJD(NOLOCK) where OBJECT_NAME='"+ObjectName+"' and DATA_TYPE='PICKLIST' and API_NAME='"+str(current_obj_api_name)+"' ")
                            Tier_List1=sorted((Sql_Quality_Tier.PICKLIST_VALUES).split(","))
                            service_id_query=Sql.GetList("select SERVICE_ID FROM SAQTSV (NOLOCK) where QUOTE_RECORD_ID='{}' AND QTEREV_RECORD_ID='{}'".format(contract_quote_record_id,quote_revision_record_id))
                            service_ids=[service_obj.SERVICE_ID for service_obj in service_id_query]
                            if "Z0007" not in service_ids:
                                if "SENDING ACCOUNT" in Tier_List1:
                                    Tier_List1.remove("SENDING ACCOUNT")
                                if "RECEIVING ACCOUNT" in Tier_List1:
                                    Tier_List1.remove("RECEIVING ACCOUNT")
                            if str(TabName)=="Quote":
                                send_n_receive_acnt=Sql.GetList("SELECT CPQ_PARTNER_FUNCTION FROM SAQTIP(NOLOCK) WHERE QUOTE_RECORD_ID='"+str(contract_quote_record_id)+"' AND QTEREV_RECORD_ID='"+str(quote_revision_record_id)+"'")
                                if send_n_receive_acnt:
                                    for acnt in send_n_receive_acnt:
                                        if acnt.CPQ_PARTNER_FUNCTION=="SENDING ACCOUNT" or acnt.CPQ_PARTNER_FUNCTION=="RECEIVING ACCOUNT":
                                            try:
                                                Tier_List1.remove(acnt.CPQ_PARTNER_FUNCTION)
                                            except:
                                                Trace.Write("Error occured while removing C4C partner function")
                            for req1 in Tier_List1:
                                sec_str+="<option>"+str(req1)+"</option>"
                            sec_str+="</select></td>"
                        elif data_type=="LONG TEXT AREA":
                            sec_str+=('<td><textarea title="'+str(current_obj_value)+'" class="form-control related_popup_css txtArea light_yellow wid_90 " id="'+str(current_obj_api_name)+'" rows="1" cols="100" '+disable+">"+current_obj_value+"</textarea></td>")
                        else:
                            sec_str+=('<td><input id="'+str(current_obj_api_name)+'" value="'+str(current_obj_value)+'" '+'type="text" class="form-control related_popup_css" '+disable+" maxlength='"+str(max_length)+"'></td>")
                        sec_str+=('<td id="'+str(current_obj_api_name)+'_err" class="err_msgs"></td><td class="float_r_bor_bot"><div class="col-md-12 editiconright"><a href="#" class="editclick">'+str(edit_pencil_icon)+"</a></div></td>")
                        sec_str+="</tr>"
            sec_str+="</table>"
            GettreeEnable=Sql.GetFirst("select ENABLE_TREE FROM SYTABS where SAPCPQ_ALTTAB_NAME='"+str(TabName)+"'")
            if GettreeEnable is not None and str(GettreeEnable.ENABLE_TREE).upper()=="TRUE":
                event_name="loadRelatedList('"+str(popup_table_id)+"','"+str(DIVNAME)+"')"
                html_content=Sql.GetList("SELECT HTML_CONTENT,RELATED_LIST_RECORD_ID FROM SYPGAC (NOLOCK) WHERE RELATED_LIST_RECORD_ID='"+str(popup_table_id)+"' AND TAB_NAME LIKE '%"+str(TabName)+"%'")
                if html_content:
                    sec_str+=('<div class="row ma_text_align_sixteen">')
                    SaveCancel+=('<div id="HideSavecancel">')
                    for btn in html_content:
                        try:
                            if "CANCEL" in str(btn.HTML_CONTENT):
                                cancel_button=str(btn.HTML_CONTENT).format(event_name=event_name)
                                sec_str+=str(cancel_button)
                                SaveCancel+=str(cancel_button)
                            if "SAVE" in str(btn.HTML_CONTENT):
                                save_button=str(btn.HTML_CONTENT).format(ObjectName=ObjectName,func2=func2)
                                sec_str+=str(save_button)
                                SaveCancel+=str(save_button)
                        except:
                            cancel_button=""
                            save_button=""
                    SaveCancel+=("</div>")
                    sec_str+="</div>"
        elif child_script:
            response=ScriptExecutor.ExecuteGlobal(script_details[ObjectName]['child_script_name'],{"SQL_OBJ":Sql,"ObjectName":ObjectName,"A_Keys":A_Keys,"A_Values":A_Values,"RECORD_ID":RECORDID,"RECORDFEILD":RECORDFEILD,"TABLEID":TABLEID,"PerPage":PerPage,"PageInform":PageInform,"offset_skip_count":offset_skip_count,"FETCH_COUNT":fetch_count,"SortColumn":SortColumn,"SortColumnOrder":SortColumnOrder,"TOOL_TYPE":tool_type,"ACTION":ACTION,"poputilObj":poputilObj,"ADDON_PRD_ID":ADDON_PRD_ID,"active_subtab":active_subtab})
            sec_str=response.get('sec_str')
            new_value_dict=response.get('new_value_dict')
            date_field=response.get('date_field')
            dbl_clk_function=response.get('dbl_clk_function')
            filter_control_function=response.get('filter_control_function')
            var_str=response.get('var_str')
            filter_tags=response.get('filter_tags')
            filter_types=response.get('filter_types')
            filter_values=response.get('filter_values')
            filter_drop_down=response.get('filter_drop_down')
            pagedata=response.get('pagedata')
            QryCount=response.get('QryCount')
    else:
        sec_str+='<div class="ma_text_align_sixteen">No matching records found </div><div class="modal-footer"><button type="button" class="btnstyle flt_rt" data-dismiss="modal">Close</button></div>'
    return (sec_str,new_value_dict,api_name,date_field,dbl_clk_function,filter_control_function,var_str,selected_offerings_list_preslect,[],filter_tags,filter_types,
    filter_values,filter_drop_down,SaveCancel,table_header,pagedata,QryCount)
try:
    A_Keys=Param.A_Keys
    A_Values=Param.A_Values
except:
    A_Keys=""
    A_Values=""
try:
    DIVNAME=Param.DIVNAME
except:
    DIVNAME=""
TABLEID=Param.TABLEID
OPER=Param.OPER
offset_list=[]
for val in Param:
    offset_list.append(val.Key)
if "Offset_Skip_Count" in offset_list:
    Offset_Skip_Count=Param.Offset_Skip_Count
else:
    Offset_Skip_Count=1
if "Fetch_Count" in offset_list:
    Fetch_Count=Param.Fetch_Count
else:
    Fetch_Count=10
RECORDID=Param.RECORDID
try:
    RECORDFEILD=Param.RECORDFEILD
except:
    RECORDFEILD=""
try:
    ADDON_PRD_ID=Param.ADDON_PRD_ID
except:
    ADDON_PRD_ID=""
NEWVALUE=Param.NEWVALUE
LOOKUPOBJ=Param.LOOKUPOBJ
LOOKUPAPI=Param.LOOKUPAPI
try:
    TreeParentParam=Param.TreeParentParam
except:
    TreeParentParam=""
try:
    SortColumn=Param.SortColumn
    SortColumnOrder=Param.SortColumnOrder
except:
    SortColumn=''
    SortColumnOrder=''
try:
    PerPage=Param.PerPage
    PageInform=Param.PageInform
except:
    PerPage=''
    PageInform=''
try:
    tool_type=Param.TOOL_TYPE
except:
    tool_type="EQUIPMENT"
try:
    ACTION=Param.ACTION
except:
    ACTION=''
try:
    active_subtab=Param.SUBTAB
except:
    active_subtab=''
if LOOKUPOBJ is not None and LOOKUPOBJ !="":
    LOOKUPOBJ=LOOKUPOBJ.split("_")[1]
ApiResponse=ApiResponseFactory.JsonResponse(POPUPLISTVALUEADDNEW(TABLEID,RECORDID,RECORDFEILD,NEWVALUE,LOOKUPOBJ,LOOKUPAPI,OPER,A_Keys,A_Values,DIVNAME,TreeParentParam,PerPage,PageInform,active_subtab))
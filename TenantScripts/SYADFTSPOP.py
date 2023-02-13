#=========================================================================================================================================
#   __script_name : SYADFTSPOP.PY (SYUADNWPOP LINKED)
#   __script_description : THIS SCRIPT IS USED FOR FTS FUNCTIONALITY RELATED POPUPS
#   __primary_author__ : VIKNESH DURAISAMY
#   __create_date : 18/11/2022
#=========================================================================================================================================
from math import ceil
import SYCNGEGUID as CPQID
import Webcom.Configurator.Scripting.Test.TestProduct
TestProduct=Webcom.Configurator.Scripting.Test.TestProduct()
def fts_addnew_popup(PerPage,PageInform,SortColumn,SortColumnOrder,offset_skip_count,fetch_count):
    sec_str=var_str=filter_control_function=dbl_clk_function=filter_drop_down=order_by=disable_next_and_last=disable_previous_and_first=values_lists=sales_org=pagedata=""
    attribute_list=[]
    new_value_dict={}
    pop_val={}
    date_field=[]
    script_details = poputilObj.get_script_details(TreeParam)
    ObjectName = str(object_name)
    master_obj_name = script_details[ObjectName]['master_object_name']
    id_name = str(script_details[ObjectName]['ID_NAME'])
    id_names="#"+str(id_name)
    account_id=TreeParam.split(' - ')
    account_id=account_id[len(account_id)-1]
    where_string=poputilObj.construct_where_string(A_Keys,A_Values,master_obj_name)
    lookup_list,checkbox_list,lookup_disply_list,has_obj=poputilObj.get_types_list(master_obj_name)
    if str(PerPage)=="" and str(PageInform)=="":
        Page_start=1
        Page_End=fetch_count
        PerPage=fetch_count
        PageInform="1___"+str(fetch_count)+"___"+str(fetch_count)
    else:
        Page_start=int(PageInform.split("___")[0])
        Page_End=int(PageInform.split("___")[1])
        PerPage=PerPage
    if SortColumn !='' and SortColumnOrder !='':
        order_by="order by "+SortColumn + " " + SortColumnOrder
    if ObjectName == "SYOBJR_00038":
        ObjectName="SAQSAF"
        Header_details={"QUOTE_REV_SENDING_ACC_FAB_LOCATION_RECORD_ID": "KEY","SNDFBL_ID": "FAB ID","SNDFBL_NAME": "FAB NAME"}
        ordered_keys=["QUOTE_REV_SENDING_ACC_FAB_LOCATION_RECORD_ID","SNDFBL_ID","SNDFBL_NAME"]
        sec_str='<div class="row modulebnr brdr ma_mar_btm">ADD RECEIVING FAB LOCATION<button type="button" class="close flt_rt" onclick="closepopup_scrl()" data-dismiss="modal">X</button></div>'
        sec_str+='<div class="col-md-12 padlftrhtnone"><div class="row pad-10 bg-lt-wt brdr"> <img style="height: 40px; margin-top: -1px; margin-left: -1px; float: left;" src="/mt/APPLIEDMATERIALS_PRD/Additionalfiles/Secondary Icon.svg"/><div class="product_txt_div_child secondary_highlight" style="display: block;"><div class="product_txt_child"><abbr title="Sales Org">Fab Location ID</abbr></div><div class="product_txt_to_top_child" style="float: left;"><abbr title="ALL">ALL</abbr></div></div><div class="product_txt_div_child secondary_highlight" style="display: block;"><div class="product_txt_child"><abbr title="Fab Name">Sales Org</abbr></div><div class="product_txt_to_top_child" style="float: left;"><abbr title="All">All</abbr></div></div> <button type="button" class="btnconfig" data-dismiss="modal" onclick="closepopup_scrl()">CANCEL</button><button type="button" id="add_receiving_fab_shp" class="btnconfig" onclick="add_receving_fab()" data-dismiss="modal">ADD</button></div></div>'
        sec_str+='<div id="container" class="g4 pad-10 brdr except_sec">'
        sec_str+=( '<table id="' + str(id_name) + '" data-escape="true"  data-search-on-enter-key="true" data-show-header="true"  data-filter-control="true"> <thead><tr>' )
        sec_str+='<th data-field="SELECT" class="wth45" data-checkbox="true" id="check_boxval" onchange="get_checkedval()"><div class="action_col">SELECT</div></th>'
        for key,invs in enumerate(list(ordered_keys)):
            invs=str(invs).strip()
            qstring=Header_details.get(str(invs)) or ""
            if key==0:
                sec_str+=( '<th data-field="' + str(invs) + '" data-formatter="addReceivingFabFtsLink" data-sortable="true" data-title-tooltip="' + str(qstring) + '" data-filter-control="input">' + str(qstring) + "</th>" )
            else:
                sec_str+=( '<th data-field="' + invs + '" data-title-tooltip="' + str(qstring) + '" data-sortable="true" data-filter-control="input">' + str(qstring) + "</th>" )
        sec_str+='</tr></thead><tbody class="user_id" ></tbody></table>'
        sec_str+='<div id="add_receiving_fab_footer"></div>'
        for invsk in list(Header_details):
            filter_class=id_names + " .bootstrap-table-filter-control-" + str(invsk)
            values_lists+="var " + str(invsk) + '=$("' + str(filter_class) + '").val(); '
            values_lists+=" ATTRIBUTE_VALUEList.push(" + str(invsk) + "); "
            attribute_list.append(invsk)
            filter_control_function+=('$("' + filter_class + '").change( function(){ var id_name=$(this).closest("table").attr("id"); var a_list=' + str(attribute_list) + "; ATTRIBUTE_VALUEList=[]; " + str(values_lists) + ' SortColumn=localStorage.getItem("SortColumn"); SortColumnOrder=localStorage.getItem("SortColumnOrder"); PerPage=$("#PageCountValue").val(); PageInform="1___" + PerPage + "___" + PerPage; cpq.server.executeScript("SYUADNWPOP",{\'TABLEID\': "' + str(TABLEID) + "\",'OPER': 'NO','RECORDID': \"" + str(RECORDID) + "\",'RECORDFEILD':  \"" + str(RECORDFEILD) + "\",'NEWVALUE': '','LOOKUPOBJ': '','LOOKUPAPI': '','A_Keys':a_list,'A_Values':ATTRIBUTE_VALUEList,'PerPage':PerPage,'PageInform':PageInform},function(data) {  date_field=data[3]; var assoc=data[1]; var api_name=data[2];data4=data[4];data5=data[5];data15=data[15]; data16=data[16]; try { if(date_field.length > 0) { $(\"" + str(id_names) + '").bootstrapTable("load",date_field  ); $("button#country_save").attr("disabled",false); $("#noRecDisp").remove(); if (document.getElementById("RecordsStartAndEnd")){document.getElementById("RecordsStartAndEnd").innerHTML=data15;}; if (document.getElementById("TotalRecordsCount")) {document.getElementById("TotalRecordsCount").innerHTML=data16;} } else{ $("' + str(id_names) + '").bootstrapTable("load",date_field  ); $("button#country_save").attr("disabled",true); $("#fablocation_addnew").after("<div id=\'noRecDisp\' class=\'noRecord\'>No Records to Display</div>"); $(".noRecord:not(:first)").remove(); } } catch(err) { if(date_field.length > 0) { $("' + str(id_names) + '").bootstrapTable("load",date_field  ); $("button#country_save").attr("disabled",false); } else{ $("' + str(id_names) + '").bootstrapTable("load",date_field  ); $("button#country_save").attr("disabled",true); } } ; });  });' )
            dbl_clk_function=('$("' + str(id_names) + '").on("all.bs.table",function (e,name,args) { $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); });  $(".bs-checkbox input").addClass("custom"); $("' + str(id_names) + "\").on('sort.bs.table',function (e,name,order) { e.stopPropagation(); currenttab=$(\"ul#carttabs_head .active\").text().trim(); localStorage.setItem('" + str(id_name) + "_SortColumn',name); localStorage.setItem('" + str(id_name) + "_SortColumnOrder',order); ATTRIBUTE_VALUEList=[]; "+str(values_lists)+" AddNewContainerSorting(name,order,'" + str(id_name) + "',"+str(attribute_list)+",ATTRIBUTE_VALUEList,'"+str(TABLEID)+"','"+str(RECORDID)+"','"+str(RECORDFEILD)+"'); }); " )
        if offset_skip_count%10==1:
            offset_skip_count-=1
        pagination_condition="OFFSET {Offset_Skip_Count} ROWS FETCH NEXT {Fetch_Count} ROWS ONLY".format( Offset_Skip_Count=offset_skip_count,Fetch_Count=fetch_count )
        if where_string:
            where_string+=" AND "
        if order_by=="":
            order_by="order by SNDFBL_NAME ASC"
        where_string+="""QUOTE_RECORD_ID='{}' AND QTEREV_RECORD_ID='{}' AND SNDFBL_ID NOT IN (SELECT FABLOCATION_ID FROM SAQFBL (NOLOCK) WHERE QUOTE_RECORD_ID='{}' AND QTEREV_RECORD_ID='{}')""".format(contract_quote_record_id,quote_revision_record_id,contract_quote_record_id,quote_revision_record_id)
        table_data=Sql.GetList("select  {} from {} (NOLOCK) {} {} {}".format(",".join(ordered_keys),ObjectName,"WHERE " + where_string if where_string else "",order_by,pagination_condition))
        QueryCountObj=Sql.GetFirst("select count(*) as cnt from {} (NOLOCK)  {} ".format(ObjectName,"WHERE " + where_string if where_string else ""))
        if table_data is not None:
            for row_data in table_data:
                new_value_dict={}
                for data in row_data:
                    if str(data.Key)=="QUOTE_REV_SENDING_ACC_FAB_LOCATION_RECORD_ID":
                        pop_val=str(data.Value)
                        cpqidval=CPQID.KeyCPQId.GetCPQId(ObjectName,str(data.Value))
                        new_value_dict[data.Key]=cpqidval
                    else:
                        new_value_dict[data.Key]=data.Value
                    new_value_dict["pop_val"]=pop_val
                date_field.append(new_value_dict)
        operation_type="addFab"
    elif ObjectName =="UNMAPPED":
        ObjectName="MAEQUP"
        Header_details={ "EQUIPMENT_RECORD_ID": "KEY","EQUIPMENT_ID":"EQUIPMENT ID","SERIAL_NO": "SERIAL NUMBER","GREENBOOK": "GREENBOOK","PLATFORM": "PLATFORM"}
        ordered_keys=[ "EQUIPMENT_RECORD_ID","EQUIPMENT_ID","SERIAL_NO","GREENBOOK","PLATFORM"]
        query_shp_values=Sql.GetFirst(" SELECT SALESORG_ID FROM SAQFBL (NOLOCK) WHERE FABLOCATION_ID='{}' AND QUOTE_RECORD_ID='{}' ".format(TreeParam,contract_quote_record_id,))
        if query_shp_values:
            sales_org=query_shp_values.SALESORG_ID
        sec_str='<div class="row modulebnr brdr ma_mar_btm">INSTALLED BASE EQUIPMENT LIST<button type="button" class="close flt_rt" onclick="closepopup_scrl()" data-dismiss="modal">X</button></div>'
        sec_str+='<div class="col-md-12 padlftrhtnone" id="btnhide"><div class="row pad-10 bg-lt-wt brdr"><img style="height: 40px; margin-top: -1px; margin-left: -1px; float: left;" src="/mt/APPLIEDMATERIALS_PRD/Additionalfiles/Secondary Icon.svg"/><div class="product_txt_div_child secondary_highlight" style="display: block;"><div class="product_txt_child"><abbr title="Key">Customer Region</abbr></div><div class="product_txt_to_top_child" style="float: left;"><abbr title="AMC">AMC</abbr></div></div><div class="product_txt_div_child secondary_highlight" style="display: block;"><div class="product_txt_child"><abbr title="Key">Sales Org</abbr></div><div class="product_txt_to_top_child" style="float: left;"><abbr title="{sales_org}">{sales_org}</abbr></div></div><div class="product_txt_div_child secondary_highlight" style="display: block;"><div class="product_txt_child"><abbr title="Key">Fab Location ID</abbr></div><div class="product_txt_to_top_child" style="float: left;"><abbr title="{}">{}</abbr></div></div><button type="button" class="btnconfig" data-dismiss="modal" onclick="closepopup_scrl()">CANCEL</button><button type="button" id="add-unmapped_equipment" class="btnconfig" onclick="addUnmappedEquipments()" data-dismiss="modal">ADD</button></div></div>'.format(TreeParam,TreeParam,sales_org=sales_org)
        sec_str+='<div id="container" class="g4 pad-10 brdr except_sec header_section_div">'
        sec_str+=('<table id="' + str(id_name) + '" data-escape="true"  data-search-on-enter-key="true" data-show-header="true"  data-filter-control="true"> <thead><tr>')
        sec_str+='<th data-field="SELECT" class="wth45" data-checkbox="true" id="check_boxval" onchange="get_checkedval()"><div class="action_col">SELECT</div></th>'
        for key,invs in enumerate(list(ordered_keys)):
            invs=str(invs).strip()
            qstring=Header_details.get(str(invs)) or ""
            if key==0:
                sec_str+=('<th data-field="' + str(invs) + '" data-formatter="UnmappedListKeyHyperLink" data-sortable="true" data-title-tooltip="' + str(qstring) + '" data-filter-control="input">' + str(qstring) + "</th>")
            else:
                sec_str+=('<th data-field="' + invs + '" data-title-tooltip="' + str(qstring) + '" data-sortable="true" data-filter-control="input">' + str(qstring) + "</th>")
        sec_str+='</tr></thead><tbody class="equipments_id" ></tbody></table><div id="unmapped_equipments_footer"></div>'
        for invsk in list(Header_details):
            filter_class=id_names + " .bootstrap-table-filter-control-" + str(invsk)
            values_lists+="var " + str(invsk) + '=$("' + str(filter_class) + '").val(); '
            values_lists+=" ATTRIBUTE_VALUEList.push(" + str(invsk) + "); "
            attribute_list.append(invsk)
            filter_control_function+=('$("' + filter_class + '").change( function(){ var id_name=$(this).closest("table").attr("id"); var a_list=' + str(attribute_list) + "; ATTRIBUTE_VALUEList=[]; " + str(values_lists) + ' SortColumn=localStorage.getItem("SortColumn"); SortColumnOrder=localStorage.getItem("SortColumnOrder"); PerPage=$("#PageCountValue").val(); PageInform="1___" + PerPage + "___" + PerPage; cpq.server.executeScript("SYUADNWPOP",{\'TABLEID\': "' + str(TABLEID) + "\",'OPER': 'NO','RECORDID': \"" + str(RECORDID) + "\",'RECORDFEILD':  \"" + str(RECORDFEILD) + "\",'NEWVALUE': '','LOOKUPOBJ': '','LOOKUPAPI': '','A_Keys':a_list,'A_Values':ATTRIBUTE_VALUEList},function(data) {  date_field=data[3]; var assoc=data[1]; var api_name=data[2];data4=data[4];data5=data[5]; try { if(date_field.length > 0) { $(\"" + str(id_names) + '").bootstrapTable("load",date_field  ); $("button#country_save").attr("disabled",false); $("#noRecDisp").remove() } else{ var date_field=[];$("' + str(id_names) + '").bootstrapTable("load",date_field  ); $("button#country_save").attr("disabled",true); $("#unmapped_equipments_addnew").after("<div id=\'noRecDisp\' class=\'noRecord\'>No Records to Display</div>"); $(".noRecord:not(:first)").remove(); } } catch(err) { if(date_field.length > 0) { $("' + str(id_names) + '").bootstrapTable("load",date_field  ); $("button#country_save").attr("disabled",false); } else{ $("' + str(id_names) + '").bootstrapTable("load",date_field  ); $("button#country_save").attr("disabled",true);} };}); });')
        if offset_skip_count%10==1:
            offset_skip_count-=1
        pagination_condition="OFFSET {Offset_Skip_Count} ROWS FETCH NEXT {Fetch_Count} ROWS ONLY".format( Offset_Skip_Count=offset_skip_count,Fetch_Count=fetch_count)
        get_fab_query=Sql.GetList("SELECT FABLOCATION_ID FROM SAQFBL WHERE QUOTE_RECORD_ID='{}' and ACCOUNT_ID='{}' AND QTEREV_RECORD_ID='{}'".format(contract_quote_record_id,account_id,quote_revision_record_id) )
        if get_fab_query:
            get_fab=tuple([fab.FABLOCATION_ID for fab in get_fab_query])
        else:
            get_fab=""
        if where_string:
            where_string+=" AND"
        if (("Sending Account -" in TreeParam) or ("Receiving Account -" in TreeParam)) and TreeParentParam=='Fab Locations':
            QueryCountObj=Sql.GetFirst("SELECT COUNT(CpqTableEntryId) as cnt FROM {ObjectName} (NOLOCK) WHERE ACCOUNT_ID='{account_id}' AND FABLOCATION_ID='UNMAPPED' AND EQUIPMENT_RECORD_ID NOT IN (SELECT EQUIPMENT_RECORD_ID FROM SAQFEQ (NOLOCK) WHERE QUOTE_RECORD_ID='{contract_quote_record_id}' AND QTEREV_RECORD_ID='{quote_revision_record_id}' AND FABLOCATION_ID='UNMAPPED')".format(ObjectName=ObjectName,account_id=account_id,contract_quote_record_id=contract_quote_record_id,quote_revision_record_id=quote_revision_record_id))
        else:
            QueryCountObj=Sql.GetFirst( "SELECT COUNT(CpqTableEntryId) as cnt FROM {} (NOLOCK) WHERE ACCOUNT_RECORD_ID IN (SELECT ACCOUNT_RECORD_ID FROM SAACNT WHERE PAR_ACCOUNT_RECORD_ID=(SELECT PAR_ACCOUNT_RECORD_ID FROM SAOPQT WHERE QUOTE_RECORD_ID='{}' )) AND FABLOCATION_ID='{}' AND ISNULL(SERIAL_NO,'') <> '' AND ISNULL(GREENBOOK,'') <> '' AND {} EQUIPMENT_RECORD_ID NOT IN (SELECT EQUIPMENT_RECORD_ID FROM SAQFEQ (NOLOCK) WHERE QUOTE_RECORD_ID='{}' AND QTEREV_RECORD_ID='{quote_revision_record_id}' AND FABLOCATION_ID='{}' AND ISNULL(SERIAL_NUMBER,'') <> '')".format( ObjectName,contract_quote_record_id,TreeParam,where_string,contract_quote_record_id,TreeParam,quote_revision_record_id))
        if order_by=="":
            order_by="order by FABLOCATION_NAME ASC"
        if (("Sending Account -" in TreeParam) or ("Receiving Account -" in TreeParam)) and TreeParentParam=='Fab Locations':
            where_string+=""" ACCOUNT_ID='{}' AND FABLOCATION_ID='UNMAPPED' AND EQUIPMENT_RECORD_ID NOT IN (SELECT EQUIPMENT_RECORD_ID FROM SAQFEQ (NOLOCK) WHERE QUOTE_RECORD_ID='{}' AND QTEREV_RECORD_ID='{quote_revision_record_id}' AND FABLOCATION_ID='UNMAPPED')""".format( account_id,contract_quote_record_id,quote_revision_record_id=quote_revision_record_id)
            table_data=Sql.GetList("select {} from {} (NOLOCK) {} {} {}".format( ",".join(ordered_keys),ObjectName,"WHERE " + where_string if where_string else "",order_by,pagination_condition))
        else:
            where_string+=""" ACCOUNT_RECORD_ID IN (SELECT ACCOUNT_RECORD_ID FROM SAACNT WHERE PAR_ACCOUNT_RECORD_ID=(SELECT PAR_ACCOUNT_RECORD_ID FROM SAOPQT WHERE QUOTE_RECORD_ID='{}' )) AND FABLOCATION_ID='{}' AND ISNULL(SERIAL_NO,'') <> '' AND ISNULL(GREENBOOK,'') <> '' AND {} EQUIPMENT_RECORD_ID NOT IN (SELECT EQUIPMENT_RECORD_ID FROM SAQFEQ (NOLOCK) WHERE QUOTE_RECORD_ID='{}' AND FABLOCATION_ID='{}' AND QTEREV_RECORD_ID='{quote_revision_record_id}' AND ISNULL(SERIAL_NUMBER,'') <> '')""".format( contract_quote_record_id,TreeParam,where_string,contract_quote_record_id,TreeParam,quote_revision_record_id)
            table_data=Sql.GetList( "select {} from {} (NOLOCK) {} {} {}".format( ",".join(ordered_keys),ObjectName,"WHERE " + where_string if where_string else "",order_by,pagination_condition))
        if table_data is not None :
            for row_data in table_data:
                new_value_dict={}
                for data in row_data:
                    if str(data.Key)=="EQUIPMENT_RECORD_ID":
                        pop_val=str(data.Value) + "|unmapped_equipments"
                        cpqidval=CPQID.KeyCPQId.GetCPQId(ObjectName,str(data.Value))
                        new_value_dict[data.Key]=cpqidval
                    else:
                        new_value_dict[data.Key]=data.Value
                    new_value_dict["pop_val"]=pop_val
                date_field.append(new_value_dict)
        operation_type="addUnmappedEquipment"
    elif ObjectName=="SAQASE" :
        account_id=stp_account_id
        ObjectName="MAEQUP"
        Header_details={"EQUIPMENT_RECORD_ID": "KEY","EQUIPMENT_ID":"EQUIPMENT ID","EQUIPMENT_DESCRIPTION":"EQUIPMENT_DESCRIPTION","SERIAL_NO": "SERIAL NUMBER","GREENBOOK": "GREENBOOK","PLATFORM": "PLATFORM",}
        ordered_keys=["EQUIPMENT_RECORD_ID","EQUIPMENT_ID","EQUIPMENT_DESCRIPTION","SERIAL_NO","GREENBOOK","PLATFORM"]
        query_shp_values=Sql.GetFirst(" SELECT SALESORG_ID,REGION FROM SAQTRV (NOLOCK) WHERE QUOTE_RECORD_ID='{}' AND QUOTE_REVISION_RECORD_ID='{}'".format(contract_quote_record_id,quote_revision_record_id))
        if query_shp_values:
            sales_org=query_shp_values.SALESORG_ID
            region=query_shp_values.REGION
        #INC08654837 - M
        sec_str='<div class="row modulebnr brdr ma_mar_btm">SENDING EQUIPMENT LIST<button type="button" class="close flt_rt" onclick="closepopup_scrl()" data-dismiss="modal">X</button></div>'
        sec_str+='<div class="col-md-12 padlftrhtnone" id="btnhide"><div class="row pad-10 bg-lt-wt brdr"><img style="height: 40px; margin-top: -1px; margin-left: -1px; float: left;" src="/mt/APPLIEDMATERIALS_PRD/Additionalfiles/Secondary Icon.svg"/><div class="product_txt_div_child secondary_highlight" style="display: block;"><div class="product_txt_child"><abbr title="Key">Customer Region</abbr></div><div class="product_txt_to_top_child" style="float: left;"><abbr title="{region}">{region}</abbr></div></div><div class="product_txt_div_child secondary_highlight" style="display: block;"><div class="product_txt_child"><abbr title="Key">Sales Org</abbr></div><div class="product_txt_to_top_child" style="float: left;"><abbr title="{sales_org}">{sales_org}</abbr></div></div><div class="product_txt_div_child secondary_highlight" style="display: block;"><div class="product_txt_child"><abbr title="Key">Fab Location ID</abbr></div><div class="product_txt_to_top_child" style="float: left;"><abbr title="{sending_fab}">{sending_fab}</abbr></div></div><button type="button" class="btnconfig" data-dismiss="modal" onclick="closepopup_scrl()">CANCEL</button><button type="button" id="add-equipment" class="btnconfig" onclick="add_sending_equipment()" data-dismiss="modal">ADD</button></div></div>'.format(sending_fab=Product.GetGlobal("sending_fab_id"),sales_org=sales_org,region=region)
        #INC08654837 - M
        sec_str+='<div id="container" class="g4 pad-10 brdr except_sec header_section_div">'
        sec_str+=('<table id="'+ str(id_name) + '" data-escape="true"  data-search-on-enter-key="true" data-show-header="true"  data-filter-control="true"> <thead><tr>')
        sec_str+='<th data-field="SELECT" class="wth45" data-checkbox="true" id="check_boxval" onchange="get_checkedval()"><div class="action_col">SELECT</div></th>'
        for key,invs in enumerate(list(ordered_keys)):
            invs=str(invs).strip()
            qstring=Header_details.get(str(invs)) or ""
            if key==0:
                sec_str+=('<th data-field="'+ str(invs) + '" data-formatter="addSendingEquipFtsLink" data-sortable="true" data-title-tooltip="'+ str(qstring) + '" data-filter-control="input">'+ str(qstring) + "</th>")
            else:
                sec_str+=('<th data-field="'+ invs + '" data-title-tooltip="'+ str(qstring) + '" data-sortable="true" data-filter-control="input">'+ str(qstring) + "</th>")
        sec_str+='</tr></thead><tbody class="equipments_id" ></tbody></table>'
        sec_str+='<div id="sending_equipments_footer"></div>'
        for invsk in list(Header_details):
            filter_class=id_names + " .bootstrap-table-filter-control-" + str(invsk)
            values_lists+="var " + str(invsk) + '=$("' + str(filter_class) + '").val(); '
            values_lists+=" ATTRIBUTE_VALUEList.push(" + str(invsk) + "); "
            attribute_list.append(invsk)
            filter_control_function+=('$("'+ filter_class + '").change( function(){ var id_name=$(this).closest("table").attr("id"); var a_list='+ str(attribute_list) + "; ATTRIBUTE_VALUEList=[]; "+ str(values_lists) + ' SortColumn=localStorage.getItem("SortColumn"); SortColumnOrder=localStorage.getItem("SortColumnOrder"); PerPage=$("#PageCountValue").val(); PageInform="1___" + PerPage + "___" + PerPage; cpq.server.executeScript("SYUADNWPOP",{\'TABLEID\': "' + str(TABLEID) + "\",'OPER': 'NO','RECORDID': \"" + str(RECORDID) + "\",'RECORDFEILD':  \"" + str(RECORDFEILD)+ "\",'NEWVALUE': '','LOOKUPOBJ': '','LOOKUPAPI': '','A_Keys':a_list,'A_Values':ATTRIBUTE_VALUEList,'TOOL_TYPE':localStorage.getItem('TOOL_TYPE')},function(data) {  date_field=data[3]; var assoc=data[1]; var api_name=data[2];data4=data[4];data5=data[5]; try { if(date_field.length > 0) { $(\""+ str(id_names) + '").bootstrapTable("load",date_field  );$("#sending_equipments_footer").html(data[6]);$("button#country_save").attr("disabled",false); $("#noRecDisp").remove() } else{ var date_field=[];$("'+ str(id_names) + '").bootstrapTable("load",date_field  ); $("button#country_save").attr("disabled",true); $("#fts_equipments_addnew").after("<div id=\'noRecDisp\' class=\'noRecord\'>No Records to Display</div>"); $(".noRecord:not(:first)").remove(); } } catch(err) { if(date_field.length > 0) { $("'+ str(id_names) + '").bootstrapTable("load",date_field  ); $("button#country_save").attr("disabled",false); } else{ $("' + str(id_names) + '").bootstrapTable("load",date_field  ); $("button#country_save").attr("disabled",true); } } ; });  });')
        if offset_skip_count%10==1:
            offset_skip_count-=1
        pagination_condition="OFFSET {Offset_Skip_Count} ROWS FETCH NEXT {Fetch_Count} ROWS ONLY".format(Offset_Skip_Count=offset_skip_count,Fetch_Count=fetch_count)
        get_fab=Product.GetGlobal("sending_fab_id")
        if where_string:
            where_string+=" AND"
        #INC08654837 - Start - M
        QueryCountObj=Sql.GetFirst("SELECT COUNT(CpqTableEntryId) as cnt FROM {ObjectName} (NOLOCK) WHERE {where_string} ACCOUNT_ID='{account_id}' AND EQUIPMENT_STATUS not in ('INAC','DLFL') AND FABLOCATION_ID='{get_fab}' AND ISNULL(SERIAL_NO,'') <> '' AND ISNULL(GREENBOOK,'') <> '' AND EQUIPMENT_RECORD_ID NOT IN (SELECT SND_EQUIPMENT_RECORD_ID FROM SAQASE (NOLOCK) WHERE QUOTE_RECORD_ID='{contract_quote_record_id}' AND SNDFBL_ID='{get_fab}'  AND QTEREV_RECORD_ID='{quote_revision_record_id}' )".format(ObjectName=ObjectName,account_id=account_id,get_fab=get_fab,contract_quote_record_id=contract_quote_record_id,quote_revision_record_id=quote_revision_record_id,where_string=where_string))
        order_by="order by FABLOCATION_NAME ASC"
        where_string+=""" ACCOUNT_ID='{}' AND EQUIPMENT_STATUS not in ('INAC','DLFL') AND FABLOCATION_ID='{}' AND ISNULL(SERIAL_NO,'') <> '' AND ISNULL(GREENBOOK,'') <> '' AND  EQUIPMENT_RECORD_ID NOT IN (SELECT SND_EQUIPMENT_RECORD_ID FROM SAQASE (NOLOCK) WHERE QUOTE_RECORD_ID='{}' AND SNDFBL_ID='{}' AND QTEREV_RECORD_ID='{}' )""".format(account_id,Product.GetGlobal("sending_fab_id"),contract_quote_record_id,Product.GetGlobal("sending_fab_id"),quote_revision_record_id,)
        #INC08654837 - End - M
        table_data=Sql.GetList("select {} from {} (NOLOCK) {} {} {}".format(",".join(ordered_keys),ObjectName,"WHERE " + where_string if where_string else "",order_by,pagination_condition,))
        if table_data is not None :
            for row_data in table_data:
                new_value_dict={}
                for data in row_data:
                    if str(data.Key)=="EQUIPMENT_RECORD_ID":
                        pop_val=str(data.Value)
                        cpqidval=CPQID.KeyCPQId.GetCPQId(ObjectName,str(data.Value))
                        new_value_dict[data.Key]=cpqidval
                    else:
                        new_value_dict[data.Key]=data.Value
                    new_value_dict["pop_val"]=pop_val
                date_field.append(new_value_dict)
        operation_type="addEquipment"
    elif ObjectName=="SAQSAF" :
        account_id=stp_account_id
        ObjectName="MAFBLC"
        Header_details={"FAB_LOCATION_RECORD_ID": "KEY","FAB_LOCATION_ID": "FAB ID","FAB_LOCATION_NAME": "FAB NAME",}
        ordered_keys=["FAB_LOCATION_RECORD_ID","FAB_LOCATION_ID","FAB_LOCATION_NAME",]
        sec_str='<div class="row modulebnr brdr ma_mar_btm">ADD FAB LOCATION<button type="button" class="close flt_rt" onclick="closepopup_scrl()" data-dismiss="modal">X</button></div>'
        sec_str+='<div class="col-md-12 padlftrhtnone"><div class="row pad-10 bg-lt-wt brdr"> <img style="height: 40px; margin-top: -1px; margin-left: -1px; float: left;" src="/mt/APPLIEDMATERIALS_PRD/Additionalfiles/Secondary Icon.svg"/><div class="product_txt_div_child secondary_highlight" style="display: block;"><div class="product_txt_child"><abbr title="Sales Org">Fab Location ID</abbr></div><div class="product_txt_to_top_child" style="float: left;"><abbr title="ALL">ALL</abbr></div></div><div class="product_txt_div_child secondary_highlight" style="display: block;"><div class="product_txt_child"><abbr title="Fab Name">Sales Org</abbr></div><div class="product_txt_to_top_child" style="float: left;"><abbr title="All">All</abbr></div></div> <button type="button" class="btnconfig" data-dismiss="modal" onclick="closepopup_scrl()">CANCEL</button><button type="button" id="fts_add_fab" class="btnconfig" onclick="add_sending_fab_fts()" data-dismiss="modal">ADD</button></div></div>'
        sec_str+='<div id="container" class="g4 pad-10 brdr except_sec">'
        sec_str+=('<table id="'+ str(id_name) + '" data-escape="true"  data-search-on-enter-key="true" data-show-header="true"  data-filter-control="true"> <thead><tr>')
        sec_str+='<th data-field="SELECT" class="wth45" data-checkbox="true" id="check_boxval" onchange="get_checkedval()"><div class="action_col">SELECT</div></th>'
        for key,invs in enumerate(list(ordered_keys)):
            invs=str(invs).strip()
            qstring=Header_details.get(str(invs)) or ""
            if key==0:
                sec_str+=('<th data-field="'+ str(invs) + '" data-formatter="addSendingFabFtsLink" data-sortable="true" data-title-tooltip="'+ str(qstring) + '" data-filter-control="input">'+ str(qstring) + "</th>" )
            else:
                sec_str+=('<th data-field="' + invs + '" data-title-tooltip="'+ str(qstring) + '" data-sortable="true" data-filter-control="input">' + str(qstring) + "</th>")
        sec_str+='</tr></thead><tbody class="user_id" ></tbody></table>'
        sec_str+='<div id="fablocation_footer"></div>'
        for invsk in list(Header_details):
            filter_class=id_names + " .bootstrap-table-filter-control-" + str(invsk)
            values_lists+="var " + str(invsk) + '=$("' + str(filter_class) + '").val(); '
            values_lists+=" ATTRIBUTE_VALUEList.push(" + str(invsk) + "); "
            attribute_list.append(invsk)
            filter_control_function+=('$("'+ filter_class + '").change( function(){ var id_name=$(this).closest("table").attr("id"); var a_list='+ str(attribute_list) + "; ATTRIBUTE_VALUEList=[]; "+ str(values_lists) + ' SortColumn=localStorage.getItem("SortColumn"); SortColumnOrder=localStorage.getItem("SortColumnOrder"); PerPage=$("#PageCountValue").val(); PageInform="1___" + PerPage + "___" + PerPage; cpq.server.executeScript("SYUADNWPOP",{\'TABLEID\': "' + str(TABLEID) + "\",'OPER': 'NO','RECORDID': \""+ str(RECORDID)+ "\",'RECORDFEILD':  \""+ str(RECORDFEILD)+ "\",'NEWVALUE': '','LOOKUPOBJ': '','LOOKUPAPI': '','A_Keys':a_list,'A_Values':ATTRIBUTE_VALUEList,'PerPage':PerPage,'PageInform':PageInform},function(data) {  date_field=data[3]; var assoc=data[1]; var api_name=data[2];data4=data[4];data5=data[5];data15=data[15]; data16=data[16]; try { if(date_field.length > 0) { $(\"" + str(id_names) + '").bootstrapTable("load",date_field  ); $("button#country_save").attr("disabled",false); $("#noRecDisp").remove(); if (document.getElementById("RecordsStartAndEnd")){document.getElementById("RecordsStartAndEnd").innerHTML=data15;}; if (document.getElementById("TotalRecordsCount")) {document.getElementById("TotalRecordsCount").innerHTML=data16;} } else{ $("'+ str(id_names)+ '").bootstrapTable("load",date_field  ); $("button#country_save").attr("disabled",true); $("#fablocation_addnew").after("<div id=\'noRecDisp\' class=\'noRecord\'>No Records to Display</div>"); $(".noRecord:not(:first)").remove(); } } catch(err) { if(date_field.length > 0) { $("'+ str(id_names) + '").bootstrapTable("load",date_field  ); $("button#country_save").attr("disabled",false); } else{ $("'+ str(id_names)+ '").bootstrapTable("load",date_field  ); $("button#country_save").attr("disabled",true); } } ; });  });')
            dbl_clk_function=('$("'+ str(id_names)+ '").on("all.bs.table",function (e,name,args) { $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); });  $(".bs-checkbox input").addClass("custom"); $("'+ str(id_names)+ "\").on('sort.bs.table',function (e,name,order) {e.stopPropagation(); currenttab=$(\"ul#carttabs_head .active\").text().trim(); localStorage.setItem('"+ str(id_name)+ "_SortColumn',name); localStorage.setItem('"+ str(id_name)+ "_SortColumnOrder',order); ATTRIBUTE_VALUEList=[]; "+str(values_lists)+" AddNewContainerSorting(name,order,'"+ str(id_name) + "',"+str(attribute_list)+",ATTRIBUTE_VALUEList,'"+str(TABLEID)+"','"+str(RECORDID)+"','"+str(RECORDFEILD)+"'); }); ")
        if offset_skip_count%10==1:
            offset_skip_count-=1
        pagination_condition="OFFSET {Offset_Skip_Count} ROWS FETCH NEXT {Fetch_Count} ROWS ONLY".format(Offset_Skip_Count=offset_skip_count,Fetch_Count=fetch_count)
        if where_string:
            where_string+=" AND "
        if order_by=="":
            order_by="order by FAB_LOCATION_NAME ASC"
        #INC08654837 - Start - M
        where_string+="""  MAFBLC.ACCOUNT_ID='{}' AND FAB_LOCATION_ID NOT IN (SELECT SNDFBL_ID FROM SAQSAF (NOLOCK) WHERE QUOTE_RECORD_ID='{}' and QTEREV_RECORD_ID='{}')""".format(account_id,contract_quote_record_id,quote_revision_record_id)
        #INC08654837 - End - M
        table_data=Sql.GetList("select  {} from {} (NOLOCK) {} {} {}".format(",".join(ordered_keys),ObjectName,"WHERE " + where_string if where_string else "",order_by,pagination_condition))
        QueryCountObj=Sql.GetFirst("select count(*) as cnt from {} (NOLOCK) {} ".format(ObjectName,"WHERE " + where_string if where_string else ""))
        if table_data is not None:
            for row_data in table_data:
                new_value_dict={}
                for data in row_data:
                    if str(data.Key)=="FAB_LOCATION_RECORD_ID":
                        pop_val=str(data.Value)
                        cpqidval=CPQID.KeyCPQId.GetCPQId(ObjectName,str(data.Value))
                        new_value_dict[data.Key]=cpqidval
                    else:
                        new_value_dict[data.Key]=data.Value
                    new_value_dict["pop_val"]=pop_val
                date_field.append(new_value_dict)
        operation_type="addFab"
    pagination_total_count=0
    if QueryCountObj is not None:
        QryCount=QueryCountObj.cnt
        pagination_total_count=QryCount
    if offset_skip_count==0:
        offset_skip_count=1
        records_end=fetch_count
    else:
        offset_skip_count+=1
        records_end=offset_skip_count + fetch_count -1
    records_end=pagination_total_count if pagination_total_count < records_end else records_end
    records_start_and_end="{} - {} of ".format(offset_skip_count,records_end)
    if records_end==pagination_total_count:
        disable_next_and_last="class='btn-is-disabled' style=\'pointer-events:none\' "
    if offset_skip_count==0:
        disable_previous_and_first="class='btn-is-disabled' style=\'pointer-events:none\' "
    current_page=int(ceil(offset_skip_count / fetch_count)) + 1
    var_str+=poputilObj.constructing_table_footer(**{'records_start_and_end':records_start_and_end,'pagination_total_count':pagination_total_count,'fetch_count':fetch_count,'disable_previous_and_first':disable_previous_and_first,'disable_next_and_last':disable_next_and_last,'current_page':current_page,'TABLEID':TABLEID,'id_name':id_name,'operation_type': operation_type})
    filter_tags,filter_types,filter_values=poputilObj.filter_dropdown_header(ordered_keys=ordered_keys,obj_name=master_obj_name,id_name=id_name)
    filter_drop_down+=poputilObj.filter_dropdown_action(**{'id_name':id_name})
    dbl_clk_function+=poputilObj.dbl_clk_action(**{'id_names':id_names})
    if QryCount==0:
        pagedata=str(QryCount) + " - " + str(QryCount) + " of "
    elif QryCount < int(PerPage):
        pagedata=str(Page_start) + " - " + str(QryCount) + " of "
    else:
        pagedata=str(Page_start) + " - " + str(Page_End)+ " of "
    response_list_keys="[sec_str,new_value_dict,date_field,dbl_clk_function,filter_control_function,var_str,filter_tags,filter_types,filter_values,filter_drop_down,pagedata,QryCount]"
    response_list_vals=eval(response_list_keys)
    response={}
    keys=response_list_keys.replace("[","").replace("]","").split(',')
    for key,res in enumerate(keys):
        response[res]=response_list_vals[key]
    return response
try:
    Sql=Param.SQL_OBJ
    poputilObj = Param.poputilObj
    TreeParam=Product.GetGlobal("TreeParam")
    TreeParentParam=Product.GetGlobal("TreeParentLevel0")
    TreeSuperParentParam=Product.GetGlobal("TreeParentLevel1")
    TreeTopSuperParentParam=Product.GetGlobal("TreeParentLevel2")
    contract_quote_record_id=Quote.GetGlobal("contract_quote_record_id")
    quote_revision_record_id=Quote.GetGlobal("quote_revision_record_id")
    PerPage = Param.PerPage
    PageInform = Param.PageInform
    offset_skip_count = Param.offset_skip_count
    object_name=Param.ObjectName
    stp_account_id=Product.GetGlobal("stp_account_id")
    A_Keys=Param.A_Keys
    A_Values=Param.A_Values
    RECORDID=Param.RECORD_ID
    RECORDFEILD=Param.RECORDFEILD
    TABLEID=Param.TABLEID
    fetch_count=Param.FETCH_COUNT
    SortColumn=Param.SortColumn
    SortColumnOrder=Param.SortColumnOrder
    tool_type=Param.TOOL_TYPE
except:
    Trace.Write('Param is missing')
Result = fts_addnew_popup(PerPage,PageInform,SortColumn,SortColumnOrder,offset_skip_count,fetch_count)

#=========================================================================================================================================
#   __script_name : SYADQTEPOP.PY (SYUADNWPOP Linked)
#   __script_description : THIS SCRIPT IS USED FOR QUOTE INFORMATION LEVEL GENERAL ADD & REPLACE POPUPS 
#   __primary_author__ : VENKATESH KORRAPATI, VIKNESH DURAISAMY
#   __create_date : 18/11/2022
#=========================================================================================================================================
from math import ceil
import SYCNGEGUID as CPQID
import Webcom.Configurator.Scripting.Test.TestProduct
TestProduct = Webcom.Configurator.Scripting.Test.TestProduct()
def quote_level_popup(PerPage,PageInform,SortColumn,SortColumnOrder,offset_skip_count,fetch_count):
    sec_str=var_str=filter_control_function=dbl_clk_function=filter_drop_down=order_by=disable_next_and_last=disable_previous_and_first=values_lists=sales_org=pagedata=""
    attribute_list=date_field=[]
    new_value_dict=pop_val={}
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
    if offset_skip_count%10==1:
        offset_skip_count-=1
    if ObjectName=="Replace Involved Parties": #A055S000P01-20984
        ObjectName = "SAACPF"
        Header_details = {"ACCOUNT_PARTNER_FUNCTION_ID":"KEY","PARTNER_ID":"ACCOUNT ID","PARTNER_NAME":"ACCOUNT NAME","PARTNERFUNCTION_DESCRIPTION":"ROLE","ADDRESS_1": "ADDRESS"}
        ordered_keys = ["ACCOUNT_PARTNER_FUNCTION_ID","PARTNER_ID","PARTNER_NAME","PARTNERFUNCTION_DESCRIPTION","ADDRESS_1"]
        if order_by=="":
            order_by = "order by PARTNER_ID ASC"  #A055S000P01-20984
        #lookup_list,checkbox_list,lookup_disply_list,has_obj = get_types_list(ObjectName)
        sec_str = '<div class="row modulebnr brdr ma_mar_btm">REPLACE ACCOUNT<button type="button" class="close flt_rt" onclick="closepopup_scrl()" data-dismiss="modal">X</button></div>'
        sec_str += '<div class="col-md-12 padlftrhtnone"><div class="row pad-10 bg-lt-wt brdr"> <img style="height: 40px; margin-top: -1px; margin-left: -1px; float: left;" src="/mt/APPLIEDMATERIALS_PRD/Additionalfiles/Secondary Icon.svg"/><div class="product_txt_div_child secondary_highlight" style="display: block;text-align: left;"><div class="product_txt_child"><abbr title="Key">Accounts </abbr></div><div class="product_txt_to_top_child"><abbr title="ALL">Select a valid Account Record below to replace your current account</abbr></div></div></div></div>'
        sec_str += '<div id="container" class="g4 pad-10 brdr except_sec">'
        sec_str += ('<table id="' + str(id_name) + '" data-escape="true" data-search-on-enter-key="true" data-show-header="true" data-filter-control="true"> <thead><tr>')
        for key,invs in enumerate(list(ordered_keys)):
            invs = str(invs).strip()
            qstring = Header_details.get(str(invs)) or ""
            if key == 0:
                sec_str += ('<th data-field="' + str(invs) + '" data-formatter="replaceAccountKeyHyperLink" data-sortable="true" data-title-tooltip="' + str(qstring) + '" data-filter-control="input">' + str(qstring) + "</th>")
            else:
                sec_str += ('<th data-field="' + invs + '" data-title-tooltip="' + str(qstring) + '" data-sortable="true" data-filter-control="input">' + str(qstring) + "</th>")
        sec_str += '</tr></thead><tbody class ="user_id" ></tbody></table>'
        sec_str += '<div id="replace-account-model-footer"></div>'
        for invsk in list(Header_details):
            filter_class = id_names + " .bootstrap-table-filter-control-" + str(invsk)
            values_lists += "var " + str(invsk) + ' = $("' + str(filter_class) + '").val(); '
            values_lists += " ATTRIBUTE_VALUEList.push(" + str(invsk) + "); "
            attribute_list.append(invsk)
            filter_control_function += ('$("' + filter_class + '").change( function(){ var id_name = $(this).closest("table").attr("id"); var a_list = ' + str(attribute_list) + "; ATTRIBUTE_VALUEList = []; " + str(values_lists) + ' SortColumn = localStorage.getItem("SortColumn"); SortColumnOrder = localStorage.getItem("SortColumnOrder"); PerPage = $("#PageCountValue").val(); PageInform = "1___" + PerPage + "___" + PerPage; cpq.server.executeScript("SYUADNWPOP",{\'TABLEID\': "' + str(TABLEID) + "\",'OPER': 'NO','RECORDID': \"" + str(RECORDID) + "\",'RECORDFEILD':  \"" + str(RECORDFEILD) + "\",'NEWVALUE': '','LOOKUPOBJ': '','LOOKUPAPI': '','A_Keys':a_list,'A_Values':ATTRIBUTE_VALUEList,'TOOL_TYPE':'REPLACE'},function(data) {  date_field = data[3]; var assoc = data[1]; var api_name = data[2];data4 = data[4];data5 = data[5]; data15 = data[15]; data16 = data[16]; try { if(date_field.length > 0) { $(\"" + str(id_names) + '").bootstrapTable("load",date_field  );$("'+str(id_names)+' > tbody > tr").each(function(){var element = $(this).find("td:nth-child(5)");var text = $(element).text();$(element).attr("title",text);});$("#noRecDisp").remove(); if (document.getElementById("RecordsStartAndEnd")){document.getElementById("RecordsStartAndEnd").innerHTML = data15;}; if (document.getElementById("TotalRecordsCount")) {document.getElementById("TotalRecordsCount").innerHTML = data16;} } else{ $("' + str(id_names) + '").bootstrapTable("load",date_field  );$("#replace-account").after("<div id=\'noRecDisp\' class=\'noRecord\'>No Records to Display</div>"); $(".noRecord:not(:first)").remove(); } } catch(err) { if(date_field.length > 0) { $("' + str(id_names) + '").bootstrapTable("load",date_field  ); } else{ $("' + str(id_names) + '").bootstrapTable("load",date_field  ); document.getElementById("replace-account-model-footer").style.border = "1px solid #ccc"; document.getElementById("replace-account-model-footer").style.padding = "5.5px"; document.getElementById("replace-account-model-footer").innerHTML = "No Records to Display";} };});});')
            dbl_clk_function = ('$("' + str(id_names) + '").on("all.bs.table",function (e,name,args) { $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); var count = 0; var selectAll = false; $("#add-offerings").css("display","none"); $("#offerings-addnew-model").find(\'[type="checkbox"]:checked\').map(function () {var sel_val = $(this).closest("tr").find("td:nth-child(2)").text(); count = 1; if ($(this).attr("name") == "btSelectAll"){ var selectAll = true; $("#add-offerings").css("display","block");} else if (sel_val != "") {$("#add-offerings").css("display","block");} else{$("#add-offerings").css("display","none");}});if(count == 0){$("#add-offerings").css("display","none");}}); $(".bs-checkbox input").addClass("custom"); $("' + str(id_names) + "\").on('sort.bs.table',function (e,name,order) { e.stopPropagation(); currenttab = $(\"ul#carttabs_head .active\").text().trim(); localStorage.setItem('" + str(id_name) + "_SortColumn',name); localStorage.setItem('" + str(id_name) + "_SortColumnOrder',order); ATTRIBUTE_VALUEList = []; "+str(values_lists)+" AddNewContainerSorting(name,order,'" + str(id_name) + "',"+str(attribute_list)+",ATTRIBUTE_VALUEList,'"+str(TABLEID)+"','"+str(RECORDID)+"','"+str(RECORDFEILD)+"');});")
        pagination_condition = "OFFSET {Offset_Skip_Count} ROWS FETCH NEXT {Fetch_Count} ROWS ONLY".format(Offset_Skip_Count=offset_skip_count,Fetch_Count= PerPage if str(PerPage)!='' else str(fetch_count))
        get_partner_fun =Sql.GetFirst("SELECT SAQTMT.ACCOUNT_ID,SAQTRV.SALESORG_ID,SAQTRV.DIVISION_ID,SAQTRV.DISTRIBUTIONCHANNEL_ID FROM SAQTRV INNER JOIN SAQTMT ON SAQTMT.QUOTE_ID=SAQTRV.QUOTE_ID AND SAQTMT.QTEREV_RECORD_ID=SAQTRV.QTEREV_RECORD_ID  WHERE SAQTRV.QUOTE_RECORD_ID = '{}' AND SAQTRV.QTEREV_RECORD_ID = '{}'".format(contract_quote_record_id,quote_revision_record_id) )
        function_id = Sql.GetFirst("SELECT PARTNERFUNCTION_ID FROM SAQTIP WHERE CpqTableEntryId = '{}' ".format(RECORDID.split('-')[1].lstrip('0')))
        table_data = Sql.GetList("SELECT A.ACCOUNT_PARTNER_FUNCTION_ID,A.PARTNER_ID,A.PARTNER_NAME,A.PARTNERFUNCTION_DESCRIPTION,B.ADDRESS_1 FROM SAACPF A JOIN SAACNT B ON B.ACCOUNT_ID = A.PARTNER_ID WHERE {} SALESORG_ID='{}' AND DISTRIBUTIONCHANNEL_ID='{}' AND DIVISION_ID='{}' AND A.ACCOUNT_ID='{}' AND PARTNERFUNCTION_ID = '{}' AND PARTNER_ID NOT IN (SELECT PARTY_ID AS PARTNER_ID FROM SAQTIP WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'  AND PARTNERFUNCTION_ID = '{}') {} {} ".format(where_string,get_partner_fun.SALESORG_ID,get_partner_fun.DISTRIBUTIONCHANNEL_ID,get_partner_fun.DIVISION_ID,get_partner_fun.ACCOUNT_ID,function_id.PARTNERFUNCTION_ID,contract_quote_record_id,quote_revision_record_id,function_id.PARTNERFUNCTION_ID,order_by,pagination_condition))
        QueryCountObj = Sql.GetFirst("SELECT COUNT(A.CpqTableEntryId) as cnt FROM SAACPF A JOIN SAACNT B ON B.ACCOUNT_ID = A.PARTNER_ID WHERE {} SALESORG_ID='{}' AND DISTRIBUTIONCHANNEL_ID='{}' AND DIVISION_ID='{}' AND A.ACCOUNT_ID='{}' AND PARTNERFUNCTION_ID = '{}' AND PARTNER_ID NOT IN (SELECT PARTY_ID AS PARTNER_ID FROM SAQTIP WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND PARTNERFUNCTION_ID = '{}') ".format(where_string,get_partner_fun.SALESORG_ID,get_partner_fun.DISTRIBUTIONCHANNEL_ID,get_partner_fun.DIVISION_ID,get_partner_fun.ACCOUNT_ID,function_id.PARTNERFUNCTION_ID,contract_quote_record_id,quote_revision_record_id,function_id.PARTNERFUNCTION_ID))
        date_field=[]#A055S000P01-20984
        if table_data is not None:
            for row_data in table_data:
                new_value_dict = {}
                for data in row_data:
                    if str(data.Key) == "ACCOUNT_PARTNER_FUNCTION_ID":
                        pop_val = str(data.Value) + "|involved_party"
                        cpqidval = CPQID.KeyCPQId.GetCPQId(ObjectName,str(data.Value))
                        new_value_dict[data.Key] = cpqidval
                    else:
                        new_value_dict[data.Key] = data.Value
                    new_value_dict["pop_val"] = pop_val
                date_field.append(new_value_dict)
        operation_type = "addOfferings"   
    elif ObjectName =="SAQICT":
        ObjectName = "SACONT"
        Header_details = {"CONTACT_RECORD_ID":"KEY","CONTACT_ID":"CONTACT ID","CONTACT_NAME":"CONTACT NAME","EMAIL":"EMAIL","PHONE":"PHONE"}
        ordered_keys = ["CONTACT_RECORD_ID","CONTACT_ID","CONTACT_NAME","EMAIL","PHONE"]
        if has_obj:
            sec_str = '<div class="row modulebnr brdr ma_mar_btm">ADD CONTACT<button type="button" id = "account_replace" class="close flt_rt" onclick="closepopup_scrl(this)" data-dismiss="modal">X</button></div>'
            sec_str += '<div class="col-md-12 padlftrhtnone"><div class="row pad-10 bg-lt-wt brdr"> <img style="height: 40px; margin-top: -1px; margin-left: -1px; float: left;" src="/mt/APPLIEDMATERIALS_PRD/Additionalfiles/customer_info_icon.svg"/><div class="product_txt_div_child secondary_highlight" style="display: block;text-align: left;"><div class="product_txt_child"><abbr title="Key">Contacts</abbr></div><div class="product_txt_to_top_child"><abbr title="ALL">Select a valid Contact record below to add it to the list of Contacts associated with your Quote</abbr></div></div><button type="button" class="btnconfig" data-dismiss="modal" onclick="closepopup_scrl()">CANCEL</button><button type="button" id="add-contacts" class="btnconfig" onclick="addcontacts()" data-dismiss="modal">ADD</button></div></div>'
        sec_str += '<div id="container" class="g4 pad-10 brdr except_sec">'
        sec_str += ('<table id="'+str(id_name)+ '" data-escape="true"  data-search-on-enter-key="true" data-show-header="true"  data-filter-control="true"> <thead><tr>')
        sec_str += '<th data-field="SELECT" class="wth45" data-checkbox="true" id ="check_boxval" onchange = "get_checkedval()"><div class="action_col">SELECT</div></th>'
        for key,invs in enumerate(list(ordered_keys)):
            invs = str(invs).strip()
            qstring = Header_details.get(str(invs)) or ""
            if key == 0:
                sec_str += ('<th data-field="' + str(invs) + '" data-formatter="contactreplaceKeyHyperLink" data-sortable="true" data-title-tooltip="' + str(qstring) + '" data-filter-control="input">' + str(qstring) + "</th>")
            else:
                sec_str += ('<th data-field="' + invs + '" data-title-tooltip="' + str(qstring) + '" data-sortable="true" data-filter-control="input">' + str(qstring) + "</th>")
        sec_str += '</tr></thead><tbody class ="equipments_id" ></tbody></table>'
        sec_str += '<div id="contact_replace_addnew_model_footer"></div>'
        for invsk in list(Header_details):
            filter_class = id_names + " .bootstrap-table-filter-control-" + str(invsk)
            values_lists += "var " + str(invsk) + ' = $("' + str(filter_class) + '").val(); '
            values_lists += " ATTRIBUTE_VALUEList.push(" + str(invsk) + "); "
            attribute_list.append(invsk)
            filter_control_function += ('$("' + filter_class + '").change( function(){ var id_name = $(this).closest("table").attr("id"); var a_list = ' + str(attribute_list) + "; ATTRIBUTE_VALUEList = []; " + str(values_lists) + ' SortColumn = localStorage.getItem("SortColumn"); SortColumnOrder = localStorage.getItem("SortColumnOrder"); PerPage = $("#PageCountValue").val(); PageInform = "1___" + PerPage + "___" + PerPage; cpq.server.executeScript("SYUADNWPOP",{\'TABLEID\': "' + str(TABLEID) + "\",'OPER': 'NO','RECORDID': \"" + str(RECORDID) + "\",'RECORDFEILD':  \"" + str(RECORDFEILD) + "\",'NEWVALUE': '','LOOKUPOBJ': '','LOOKUPAPI': '','A_Keys':a_list,'A_Values':ATTRIBUTE_VALUEList},function(data) {  date_field = data[3]; var assoc = data[1]; var api_name = data[2];data4 = data[4];data5 = data[5]; try { if(date_field.length > 0) { $(\"" + str(id_names) + '").bootstrapTable("load",date_field  );$("#contact_replace_addnew_model_footer").html(data[6]); $("button#country_save").attr("disabled",false); $("#noRecDisp").remove() } else{ var date_field = [];$("' + str(id_names) + '").bootstrapTable("load",date_field  ); $("button#country_save").attr("disabled",true); $("#contact_replace_addnew_model").after("<div id=\'noRecDisp\' class=\'noRecord\'>No Records to Display</div>"); $(".noRecord:not(:first)").remove(); } } catch(err) { if(date_field.length > 0) { $("' + str(id_names) + '").bootstrapTable("load",date_field  ); $("button#country_save").attr("disabled",false); } else{ $("' + str(id_names) + '").bootstrapTable("load",date_field  ); $("button#country_save").attr("disabled",true); } } ; });  });' )
        pagination_condition = "OFFSET {Offset_Skip_Count} ROWS FETCH NEXT {Fetch_Count} ROWS ONLY".format(Offset_Skip_Count=offset_skip_count,Fetch_Count=fetch_count)
        if order_by=="":
            order_by = "order by SACONT.CONTACT_ID ASC"
        if where_string:
            where_string += " AND"
        if TreeParam == "Customer Information":
            where_string += """ SACONT.CONTACT_RECORD_ID NOT IN (SELECT CONTACT_RECORD_ID FROM SAQICT (NOLOCK) where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}')""".format(contract_quote_record_id,quote_revision_record_id)
        table_data = Sql.GetList("Select {} FROM SACONT {} {} {}".format(",".join(ordered_keys),"WHERE " +where_string if where_string else "",order_by,pagination_condition))
        QueryCountObj = Sql.GetFirst("select count(*) as cnt from SACONT (NOLOCK) {}".format("WHERE " +where_string if where_string else ""))
        date_field = []
        if table_data is not None :
            for row_data in table_data:
                new_value_dict = {}
                for data in row_data:
                    if str(data.Key) == "CONTACT_RECORD_ID":
                        pop_val = str(data.Value)
                        cpqidval = CPQID.KeyCPQId.GetCPQId(ObjectName,str(data.Value))
                        new_value_dict[data.Key] = cpqidval
                    else:
                        new_value_dict[data.Key] = data.Value
                    new_value_dict["pop_val"] = pop_val
                date_field.append(new_value_dict)
        
        operation_type = "addEquipment"
    elif ObjectName =="Deal Team Replace": #A055S000P01-20984
        ObjectName = "SAEMPL"
        Header_details = {"EMPLOYEE_RECORD_ID": "KEY","EMPLOYEE_ID":"EMPLOYEE ID","EMPLOYEE_NAME":"EMPLOYEE NAME","EMAIL":"EMAIL","PHONE":"PHONE"}
        ordered_keys = ["EMPLOYEE_RECORD_ID","EMPLOYEE_ID","EMPLOYEE_NAME","EMAIL","PHONE"]
        if has_obj:
            sec_str = '<div class="row modulebnr brdr ma_mar_btm">REPLACE CONTRACT MANAGER<button type="button" id = "contract_replace" class="close flt_rt" onclick="closepopup_scrl(this)" data-dismiss="modal">X</button></div>'
            sec_str += '<div class="col-md-12 padlftrhtnone"><div class="row pad-10 bg-lt-wt brdr"> <img style="height: 40px; margin-top: -1px; margin-left: -1px; float: left;" src="/mt/APPLIEDMATERIALS_PRD/Additionalfiles/customer_info_icon.svg"/><div class="product_txt_div_child secondary_highlight" style="display: block;text-align: left;"><div class="product_txt_child"><abbr title="Key">Contacts</abbr></div><div class="product_txt_to_top_child"><abbr title="ALL">Select a valid Contract manager record below to replace it to the list of Contracts associated with your Quote</abbr></div></div></div></div>'
        sec_str += '<div id="container" class="g4 pad-10 brdr except_sec">'
        sec_str += ('<table id="'+str(id_name)+ '" data-escape="true"  data-search-on-enter-key="true" data-show-header="true"  data-filter-control="true"> <thead><tr>')
        for key,invs in enumerate(list(ordered_keys)):
            invs = str(invs).strip()
            qstring = Header_details.get(str(invs)) or ""
            if key == 0:
                sec_str += ('<th data-field="' + str(invs) + '" data-formatter="contactreplaceKeyHyperLink" data-sortable="true" data-title-tooltip="' + str(qstring) + '" data-filter-control="input">' + str(qstring) + "</th>")
            else:
                sec_str += ('<th data-field="' + invs + '" data-title-tooltip="' + str(qstring) + '" data-sortable="true" data-filter-control="input">' + str(qstring) + "</th>")
        sec_str += '</tr></thead><tbody class ="equipments_id" ></tbody></table>'
        sec_str += '<div id="replace-account-model-footer"></div>'
        for invsk in list(Header_details):
            filter_class = id_names + " .bootstrap-table-filter-control-" + str(invsk)
            values_lists += "var " + str(invsk) + ' = $("' + str(filter_class) + '").val(); '
            values_lists += " ATTRIBUTE_VALUEList.push(" + str(invsk) + "); "
            attribute_list.append(invsk)
            filter_control_function += ('$("' + filter_class + '").change( function(){ var id_name = $(this).closest("table").attr("id"); var a_list = ' + str(attribute_list) + "; ATTRIBUTE_VALUEList = []; " + str(values_lists) + ' SortColumn = localStorage.getItem("SortColumn"); SortColumnOrder = localStorage.getItem("SortColumnOrder"); PerPage = $("#PageCountValue").val(); PageInform = "1___" + PerPage + "___" + PerPage; cpq.server.executeScript("SYUADNWPOP",{\'TABLEID\': "' + str(TABLEID) + "\",'OPER': 'NO','RECORDID': \"" + str(RECORDID) + "\",'RECORDFEILD':  \"" + str(RECORDFEILD) + "\",'NEWVALUE': '','LOOKUPOBJ': '','LOOKUPAPI': '','A_Keys':a_list,'A_Values':ATTRIBUTE_VALUEList,'ACTION':'REPLACE'},function(data) {  date_field = data[3]; var assoc = data[1]; var api_name = data[2];data4 = data[4];data5 = data[5]; try { if(date_field.length > 0) { $(\"" + str(id_names) + '").bootstrapTable("load",date_field  );$("#replace-account-model-footer").html(data[6]); $("button#country_save").attr("disabled",false); $("#noRecDisp").remove() } else{ var date_field = [];$("' + str(id_names) + '").bootstrapTable("load",date_field  ); $("button#country_save").attr("disabled",true); $("#contact_manager_addnew_model").after("<div id=\'noRecDisp\' class=\'noRecord\'>No Records to Display</div>"); $(".noRecord:not(:first)").remove(); } } catch(err) { if(date_field.length > 0) { $("' + str(id_names) + '").bootstrapTable("load",date_field  ); $("button#country_save").attr("disabled",false); } else{ $("' + str(id_names) + '").bootstrapTable("load",date_field  ); $("button#country_save").attr("disabled",true);} };});});')
        pagination_condition = "OFFSET {Offset_Skip_Count} ROWS FETCH NEXT {Fetch_Count} ROWS ONLY".format( Offset_Skip_Count=offset_skip_count,Fetch_Count=fetch_count )
        if order_by=="":
            order_by = "order by SAEMPL.EMPLOYEE_ID ASC"
        if TreeParam == "Sales Team":
            if where_string:
                where_string += " AND"
            where_string += """ SAEMPL.EMPLOYEE_RECORD_ID NOT IN (SELECT MEMBER_RECORD_ID FROM SAQDLT (NOLOCK) where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}')""".format(contract_quote_record_id,quote_revision_record_id)
        table_data = Sql.GetList("Select {} FROM SAEMPL {} {} {}".format(",".join(ordered_keys),"WHERE " +where_string if where_string else "",order_by,pagination_condition))
        QueryCountObj = Sql.GetFirst("select count(*) as cnt from SAEMPL (NOLOCK) {}".format( "WHERE " +where_string if where_string else ""))
        date_field = []
        if QueryCountObj is not None:
            QryCount = QueryCountObj.cnt
        if table_data is not None :
            for row_data in table_data:
                new_value_dict = {}
                for data in row_data:
                    if str(data.Key) == "EMPLOYEE_RECORD_ID":
                        pop_val = str(data.Value)
                        cpqidval = CPQID.KeyCPQId.GetCPQId(ObjectName,str(data.Value))
                        new_value_dict[data.Key] = cpqidval
                    else:
                        new_value_dict[data.Key] = data.Value
                    new_value_dict["pop_val"] = pop_val
                date_field.append(new_value_dict)
        operation_type = "addOfferings"
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
Result = quote_level_popup(PerPage,PageInform,SortColumn,SortColumnOrder,offset_skip_count,fetch_count)
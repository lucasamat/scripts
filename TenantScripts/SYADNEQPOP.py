#=========================================================================================================================================
#   __script_name : SYADNEQPOP.PY (SYUADNWPOP LINKED)
#   __script_description : THIS SCRIPT IS USED FOR ADDON LEVEL POPUPS SUCH AS INCLUDE ADD-ON PRODUCTS, ADD CREDITS & ADD NSO
#   __primary_author__ : VIKNESH DURAISAMY
#   __create_date : 18/11/2022
#=========================================================================================================================================
from math import ceil
import SYCNGEGUID as CPQID
import Webcom.Configurator.Scripting.Test.TestProduct
TestProduct=Webcom.Configurator.Scripting.Test.TestProduct()
def addon_addnew_popup(PerPage,PageInform,SortColumn,SortColumnOrder,offset_skip_count,fetch_count):
    sec_str=var_str=filter_control_function=dbl_clk_function=filter_drop_down=order_by=disable_next_and_last=disable_previous_and_first=values_lists=pagedata=""
    attribute_list=[]
    pop_val=new_value_dict={}
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
    if offset_skip_count%10==1:
        offset_skip_count-=1
    if ObjectName=="SAQRCV":
        account_id_query=Sql.GetFirst("SELECT ACCOUNT_ID FROM SAQTMT (NOLOCK) WHERE MASTER_TABLE_QUOTE_RECORD_ID='{}' AND QTEREV_RECORD_ID='{}'".format(str(contract_quote_record_id),str(quote_revision_record_id)))
        # SAP performance improvement fix - start
        account_id=None
        if account_id_query !=None:
            account_id=account_id_query.ACCOUNT_ID
        # SAP performance improvement fix - end
        ObjectName="SACRVC"
        Header_details={"CREDITVOUCHER_RECORD_ID": "KEY","ZAFTYPE":"ZAF TYPE","ZAFGBOOK": "GREENBOOK","ZUONR": "CONTRACT IO/SYTEMS SALES ORDER ITEM ID","GJAHR": "Fiscal Year","ZAFEXPIRY_DATE": "EXP DATE","BELNR": "Document Number","UNBL_INGL_CURR": "VALUE","CREDIT_APPLIED": "APPLIED VALUE","ZAFNOTE": "NOTES"}
        ordered_keys=["CREDITVOUCHER_RECORD_ID","ZAFTYPE","ZAFGBOOK","ZUONR","GJAHR","ZAFEXPIRY_DATE","BELNR","UNBL_INGL_CURR","CREDIT_APPLIED","ZAFNOTE"]
        getService=Sql.GetFirst("select SERVICE_DESCRIPTION from SAQTSV(nolock) where SERVICE_ID='"+str(TreeSuperParentParam)+"'")
        getDocType=Sql.GetFirst("SELECT DOCTYP_ID FROM SAQTRV(NOLOCK) WHERE QUOTE_RECORD_ID='"+str(contract_quote_record_id)+"' AND QTEREV_RECORD_ID='"+str(quote_revision_record_id)+"' ")
        if has_obj:
            sec_str='<div class="row modulebnr brdr ma_mar_btm">ADD CREDITS<button type="button" id="Include_add_on" class="close flt_rt" onclick="closepopup_scrl(this)" data-dismiss="modal">X</button></div>'
            sec_str +='<div class="col-md-12 padlftrhtnone" id="btnhide"><div class="row pad-10 bg-lt-wt brdr"><img style="height: 40px; margin-top: -1px; margin-left: -1px; float: left;" src="/mt/APPLIEDMATERIALS_PRD/Additionalfiles/Secondary Icon.svg"/><div class="product_txt_div_child secondary_highlight" style="display: block;"></div><div class="product_txt_div_child secondary_highlight" style="display: block;"><div class="product_txt_child"><abbr title="Credits">Credits</abbr></div><div class="product_txt_to_top_child" style="float: left;"><abbr title="credit grid">Use the grid below to add credits to this offerings</abbr></div></div><button type="button" class="btnconfig" id="edit_credits_button" style="display:none;" onclick="edit_credits(this)">EDIT</button><button type="button" id="save_credits_button" class="btnconfig" onclick="addCredits()" style="display:none;" data-dismiss="modal">SAVE</button></div></div>'.format(Quote.GetGlobal("TreeParentLevel1"),Quote.GetGlobal("TreeParentLevel1"),getService.SERVICE_DESCRIPTION,getService.SERVICE_DESCRIPTION)
        sec_str +='<div id="container" class="g4 pad-10 brdr except_sec">'
        sec_str +=( '<table id="' + str(id_name) + '" data-escape="true"  data-search-on-enter-key="true" data-show-header="true"  data-filter-control="true"> <thead><tr>' )
        sec_str +='<th data-field="SELECT" class="wth45" data-checkbox="true" id="check_boxval" onchange="get_checkedval()"><div class="action_col">SELECT</div></th>'
        for key,invs in enumerate(list(ordered_keys)):
            invs=str(invs).strip()
            qstring=Header_details.get(str(invs)) or ""
            if key==0:
                sec_str +=('<th data-field="' + str(invs) + '" data-formatter="creditListKeyHyperLink" data-sortable="true" data-title-tooltip="' + str(qstring) + '" data-filter-control="input">' + str(qstring) + "</th>")
            else:
                sec_str +=('<th data-field="' + invs + '" data-title-tooltip="' + str(qstring) + '" data-sortable="true" data-filter-control="input">' + str(qstring) + "</th>")
        sec_str +='</tr></thead><tbody class="equipments_id" ></tbody></table>'
        sec_str +='<div id="add_credits_addnew_footer"></div>'
        values_lists=""
        attribute_list=[]
        for invsk in list(Header_details):
            id_names="#" + str(id_name)
            filter_class=id_names + " .bootstrap-table-filter-control-" + str(invsk)
            values_lists +="var " + str(invsk) + '=$("' + str(filter_class) + '").val(); '
            values_lists +=" ATTRIBUTE_VALUEList.push(" + str(invsk) + "); "
            attribute_list.append(invsk)
            filter_control_function +=('$("' + filter_class + '").change( function(){ var id_name=$(this).closest("table").attr("id"); var a_list=' + str(attribute_list) + "; ATTRIBUTE_VALUEList=[]; " + str(values_lists) + ' SortColumn=localStorage.getItem("SortColumn"); SortColumnOrder=localStorage.getItem("SortColumnOrder"); PerPage=$("#PageCountValue").val(); PageInform="1___" + PerPage + "___" + PerPage; cpq.server.executeScript("SYUADNWPOP",{\'TABLEID\': "' + str(TABLEID) + "\",'OPER': 'NO','RECORDID': \"" + str(RECORDID) + "\",'RECORDFEILD':  \"" + str(RECORDFEILD) + "\",'NEWVALUE': '','LOOKUPOBJ': '','LOOKUPAPI': '','A_Keys':a_list,'A_Values':ATTRIBUTE_VALUEList},function(data) {  date_field=data[3]; var assoc=data[1]; var api_name=data[2];data4=data[4];data5=data[5];data15=data[15]; data16=data[16]; try { if(date_field!='NORECORDS') { $(\"" + str(id_names) + '"); $("'+str(id_names)+' > tbody > tr").each(function () {var html_text=$(this).find(\'td:nth-child(11)\').text(); $(this).find(\'td:nth-child(11)\').html(html_text); var html_text=$(this).find(\'td:nth-child(10)\').text(); $(this).find(\'td:nth-child(10)\').html(html_text); var html_text=$(this).find(\'td:nth-child(9)\').text(); $(this).find(\'td:nth-child(9)\').html(html_text); var html_text=$(this).find(\'td:nth-child(8)\').text(); $(this).find(\'td:nth-child(8)\').html(html_text); var html_text=$(this).find(\'td:nth-child(7)\').text(); $(this).find(\'td:nth-child(7)\').html(html_text); var html_text=$(this).find(\'td:nth-child(6)\').text(); $(this).find(\'td:nth-child(6)\').html(html_text); var html_text=$(this).find(\'td:nth-child(5)\').text(); $(this).find(\'td:nth-child(5)\').html(html_text); var html_text=$(this).find(\'td:nth-child(4)\').text(); $(this).find(\'td:nth-child(4)\').html(html_text); var html_text=$(this).find(\'td:nth-child(3)\').text(); $(this).find(\'td:nth-child(3)\').html(html_text);}); $("button#country_save").attr("disabled",false); $("#noRecDisp").remove() } else{ var date_field=[];$("' + str(id_names) + '").bootstrapTable("load",date_field  ); $("button#country_save").attr("disabled",true);  $("#add_credits_add_new > tbody").after("<div id=\'noRecDisp\' class=\'noRecord\'>No Records to Display</div>"); $(".noRecord:not(:first)").remove(); if (document.getElementById("RecordsStartAndEnd")) { document.getElementById("RecordsStartAndEnd").innerHTML=data15; if (document.getElementById("TotalRecordsCount")) { document.getElementById("TotalRecordsCount").innerHTML=data16;};};} } catch(err) { if(date_field!="NORECORDS") { $("' + str(id_names) + '").bootstrapTable("load",date_field  ); $("button#country_save").attr("disabled",false); } else{ $("' + str(id_names) + '").bootstrapTable("load",date_field  ); $("button#country_save").attr("disabled",true);} };});});')
            dbl_clk_function=('$("' + str(id_names) + '").on("all.bs.table",function (e,name,args) { $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); });  $(".bs-checkbox input").addClass("custom"); $("' + str(id_names) + "\").on('sort.bs.table',function (e,name,order) {e.stopPropagation(); currenttab=$(\"ul#carttabs_head .active\").text().trim(); localStorage.setItem('" + str(id_name) + "_SortColumn',name); localStorage.setItem('" + str(id_name) + "_SortColumnOrder',order); ATTRIBUTE_VALUEList=[]; "+str(values_lists)+" AddNewContainerSorting(name,order,'" + str(id_name) + "',"+str(attribute_list)+",ATTRIBUTE_VALUEList,'"+str(TABLEID)+"','"+str(RECORDID)+"','"+str(RECORDFEILD)+"');});")
        pagination_condition="OFFSET {Offset_Skip_Count} ROWS FETCH NEXT {Fetch_Count} ROWS ONLY".format(Offset_Skip_Count=offset_skip_count,Fetch_Count=fetch_count)
        if where_string:
            where_string +=" AND"
        ordered_keys.remove("ZAFNOTE")
        # INC08654667 - Starts - M
        table_data=Sql.GetList("select * from (SELECT CREDITVOUCHER_RECORD_ID,ZUONR,ZAFTYPE,GJAHR,ZAFEXPIRY_DATE,BELNR,ZAFGBOOK,UNBL_INGL_CURR,ZGBAL_AMT,KUNAG,CREDIT_APPLIED,ZAFNOTE=STUFF ( ( SELECT ',' + isnull(ZAFNOTE,'') FROM SACVNT WHERE SACVNT.BUKRS=SACRVC.BUKRS AND SACVNT.HKONT=SACRVC.HKONT AND SACVNT.BELNR=SACRVC.BELNR AND SACVNT.ZUONR=SACRVC.ZUONR AND SACVNT.GJAHR=SACRVC.GJAHR AND SACVNT.BUZEI=SACRVC.BUZEI AND SACVNT.MANDT=SACRVC.MANDT ORDER BY ZAFNOTE FOR XML PATH (''),TYPE).value('.','varchar(max)'),1,1,'')FROM SACRVC GROUP BY CREDITVOUCHER_RECORD_ID,ZUONR,ZAFTYPE,ZAFGBOOK,UNBL_INGL_CURR,ZGBAL_AMT,KUNAG,BUKRS,HKONT,BELNR,ZUONR,GJAHR,GJAHR,ZAFEXPIRY_DATE,BELNR,BUZEI,MANDT,CREDIT_APPLIED) SACRVC where {WhereString} KUNAG='00{AccountId}' ORDER BY CREDITVOUCHER_RECORD_ID {pagination_condition}".format(WhereString=where_string if where_string else "",AccountId=account_id,pagination_condition=pagination_condition))
        # INC08654667 - Ends - M
        QueryCountObj=Sql.GetFirst("select count(*) as cnt from (SELECT CREDITVOUCHER_RECORD_ID,ZUONR,ZAFTYPE,GJAHR,ZAFEXPIRY_DATE,BELNR,ZAFGBOOK,UNBL_INGL_CURR,ZGBAL_AMT,KUNAG,CREDIT_APPLIED,ZAFNOTE=STUFF ( ( SELECT ',' + isnull(ZAFNOTE,'') FROM SACVNT WHERE SACVNT.BUKRS=SACRVC.BUKRS AND SACVNT.HKONT=SACRVC.HKONT AND SACVNT.BELNR=SACRVC.BELNR AND SACVNT.ZUONR=SACRVC.ZUONR AND SACVNT.GJAHR=SACRVC.GJAHR AND SACVNT.BUZEI=SACRVC.BUZEI AND SACVNT.MANDT=SACRVC.MANDT ORDER BY ZAFNOTE FOR XML PATH (''),TYPE).value('.','varchar(max)'),1,1,'')FROM SACRVC GROUP BY CREDITVOUCHER_RECORD_ID,ZUONR,ZAFTYPE,ZAFGBOOK,UNBL_INGL_CURR,ZGBAL_AMT,KUNAG,BUKRS,HKONT,BELNR,ZUONR,GJAHR,GJAHR,ZAFEXPIRY_DATE,BELNR,BUZEI,MANDT,CREDIT_APPLIED) SACRVC where {where_string} KUNAG='00{account_id}'".format(where_string=where_string if where_string else "",account_id=account_id))
        if table_data is not None :
            for row_data in table_data:
                new_value_dict={}
                for data in row_data:
                    if str(data.Key)=="CREDITVOUCHER_RECORD_ID":
                        pop_val=str(data.Value) + "|addcredits"
                        cpqidval=CPQID.KeyCPQId.GetCPQId(ObjectName,str(data.Value))
                        new_value_dict[data.Key]=cpqidval
                    else:
                        try:
                            #A055S000P01-18702 - Removed abbr title tag and added title in cq.js and sy.js
                            new_value_dict[data.Key]=str(data.Value)
                        except:
                            #INC08727249 START - M
                            new_value_dict[data.Key]=data.Value
                            #INC08727249 END - M
                    new_value_dict["pop_val"]=pop_val
                date_field.append(new_value_dict)
        QueryCount=len(date_field)
        Quote.SetGlobal("QueryCount",str(QueryCount))
        operation_type = "addEquipment"
    elif ObjectName=="SAQSAO":
        ObjectName="MAADPR"
        Header_details={"PO_COMP_RECORD_ID": "KEY","COMP_PRDOFR_ID":"SERVICE ID","COMP_PRDOFR_NAME": "SERVICE NAME","COMP_PRDOFR_TYPE": "TYPE"}
        ordered_keys=["PO_COMP_RECORD_ID","COMP_PRDOFR_ID","COMP_PRDOFR_NAME","COMP_PRDOFR_TYPE" ]
        getService=Sql.GetFirst("select SERVICE_DESCRIPTION from SAQTSV(nolock) where SERVICE_ID='"+str(TreeSuperParentParam)+"'")
        getDocType=Sql.GetFirst("SELECT DOCTYP_ID FROM SAQTRV WHERE QUOTE_RECORD_ID='"+str(contract_quote_record_id)+"' AND QTEREV_RECORD_ID='"+str(quote_revision_record_id)+"' ")
        sec_str=''
        if has_obj:
            sec_str='<div class="row modulebnr brdr ma_mar_btm">ADD-ON PRODUCT LIST<button type="button" id="Include_add_on" class="close flt_rt" onclick="closepopup_scrl(this)" data-dismiss="modal">X</button></div>'
            sec_str +='<div class="col-md-12 padlftrhtnone" id="btnhide"><div class="row pad-10 bg-lt-wt brdr"><img style="height: 40px; margin-top: -1px; margin-left: -1px; float: left;" src="/mt/APPLIEDMATERIALS_PRD/Additionalfiles/Secondary Icon.svg"/><div class="product_txt_div_child secondary_highlight" style="display: block;"></div><div class="product_txt_div_child secondary_highlight" style="display: block;"><div class="product_txt_child"><abbr title="Service ID">Service ID</abbr></div><div class="product_txt_to_top_child" style="float: left;"><abbr title="{}">{}</abbr></div></div><div class="product_txt_div_child secondary_highlight" style="display: block;"><div class="product_txt_child"><abbr title="Service Description">Service Description</abbr></div><div class="product_txt_to_top_child" style="float: left;"><abbr title="{}">{}</abbr></div></div><div class="product_txt_div_child secondary_highlight" style="display: block;"><div class="product_txt_child"><abbr title="Add-On">Add-On</abbr></div><div class="product_txt_to_top_child" style="float: left;"><abbr title="All">All</abbr></div></div><button type="button" class="btnconfig" data-dismiss="modal" id="Include_add_on" onclick="closepopup_scrl(this)">CANCEL</button><button type="button" id="add-equipment" class="btnconfig" onclick="addon_products()" data-dismiss="modal">ADD</button></div></div>'.format(TreeSuperParentParam,TreeSuperParentParam, getService.SERVICE_DESCRIPTION,getService.SERVICE_DESCRIPTION)
        sec_str +='<div id="container" class="g4 pad-10 brdr except_sec">'
        sec_str +=('<table id="' + str(id_name) + '" data-escape="true"  data-search-on-enter-key="true" data-show-header="true"  data-filter-control="true"> <thead><tr>')
        sec_str +='<th data-field="SELECT" class="wth45" data-checkbox="true" id="check_boxval" onchange="get_checkedval()"><div class="action_col">SELECT</div></th>'
        for key,invs in enumerate(list(ordered_keys)):
            invs=str(invs).strip()
            qstring=Header_details.get(str(invs)) or ""
            if key==0:
                sec_str +=('<th data-field="' + str(invs) + '" data-formatter="add_on_prdListKeyHyperLink" data-sortable="true" data-title-tooltip="' + str(qstring) + '" data-filter-control="input">' + str(qstring) + "</th>")
            else:
                sec_str +=('<th data-field="' + invs + '" data-title-tooltip="' + str(qstring) + '" data-sortable="true" data-filter-control="input">' + str(qstring) + "</th>")
        sec_str +='</tr></thead><tbody class="equipments_id" ></tbody></table>'
        sec_str +='<div id="Include_add_on_addnew_footer"></div>'
        for invsk in list(Header_details):
            filter_class=id_names + " .bootstrap-table-filter-control-" + str(invsk)
            values_lists +="var " + str(invsk) + '=$("' + str(filter_class) + '").val(); '
            values_lists +=" ATTRIBUTE_VALUEList.push(" + str(invsk) + "); "
            attribute_list.append(invsk)
            filter_control_function +=('$("' + filter_class + '").change( function(){ var id_name=$(this).closest("table").attr("id"); var a_list=' + str(attribute_list) + "; ATTRIBUTE_VALUEList=[]; " + str(values_lists) + ' SortColumn=localStorage.getItem("SortColumn"); SortColumnOrder=localStorage.getItem("SortColumnOrder"); PerPage=$("#PageCountValue").val(); PageInform="1___" + PerPage + "___" + PerPage; cpq.server.executeScript("SYUADNWPOP",{\'TABLEID\': "' + str(TABLEID) + "\",'OPER': 'NO','RECORDID': \"" + str(RECORDID) + "\",'RECORDFEILD':  \"" + str(RECORDFEILD) + "\",'NEWVALUE': '','LOOKUPOBJ': '','LOOKUPAPI': '','A_Keys':a_list,'A_Values':ATTRIBUTE_VALUEList},function(data) {  date_field=data[3]; var assoc=data[1]; var api_name=data[2];data4=data[4];data5=data[5]; try {if(date_field!='NORECORDS') { $(\"" + str(id_names) + '").bootstrapTable("load",date_field  ); $("#Include_add_on_addnew_footer").html(data[6]);$("button#country_save").attr("disabled",false); $("#noRecDisp").remove() } else{ var date_field=[];$("' + str(id_names) + '").bootstrapTable("load",date_field  ); $("button#country_save").attr("disabled",true); $("#Include_add_on_addnew > tbody").html("<div id=\'noRecDisp\' class=\'noRecord\'>No Records to Display</div>"); $(".noRecord:not(:first)").remove(); $("#Include_add_on_addnew_footer").html(data[6]);} } catch(err) { if(date_field!="NORECORDS") { $("' + str(id_names) + '").bootstrapTable("load",date_field  ); $("button#country_save").attr("disabled",false); } else{ $("' + str(id_names) + '").bootstrapTable("load",date_field  );$("#Include_add_on_addnew > tbody").html("<div id=\'noRecDisp\' class=\'noRecord\'>No Records to Display</div>");$("#Include_add_on_addnew_footer").html(data[6]); $("button#country_save").attr("disabled",true);} };});});')
        pagination_condition="OFFSET {Offset_Skip_Count} ROWS FETCH NEXT {Fetch_Count} ROWS ONLY".format( Offset_Skip_Count=offset_skip_count,Fetch_Count=fetch_count)
        pagination_where=where_string + " AND" if where_string!="" else ""
        if order_by=="":
            order_by="order by MAADPR.COMP_PRDOFR_NAME ASC"
        if where_string:
            where_string +=" AND"
        where_string +=""" PRDOFR_ID='{}' AND PRDOFR_DOCTYP='{}'  AND COMP_PRDOFR_ID NOT IN (SELECT SERVICE_ID FROM SAQSGB (NOLOCK) where QUOTE_RECORD_ID='{}' AND QTEREV_RECORD_ID='{}' AND GREENBOOK='{}' AND PAR_SERVICE_ID='{}')""".format(str(TreeSuperParentParam),str(getDocType.DOCTYP_ID),contract_quote_record_id,quote_revision_record_id,TreeParentParam,str(TreeSuperParentParam))
        table_data=Sql.GetList("select {} from MAADPR (NOLOCK) {} {} {}".format( ",".join(ordered_keys),"WHERE " + where_string if where_string else "",order_by,pagination_condition))
        QueryCountObj=Sql.GetFirst("select count(*) as cnt from MAADPR(NOLOCK) WHERE "+str(pagination_where)+" PRDOFR_ID='"+str(TreeSuperParentParam)+"' AND PRDOFR_DOCTYP='"+str(getDocType.DOCTYP_ID)+"'  AND COMP_PRDOFR_ID NOT IN (SELECT SERVICE_ID FROM SAQSGB (NOLOCK) where QUOTE_RECORD_ID='"+str(contract_quote_record_id)+"' AND QTEREV_RECORD_ID='"+str(quote_revision_record_id)+"' AND GREENBOOK='"+str(TreeParentParam)+"') ")
        if table_data is not None :
            for row_data in table_data:
                new_value_dict={}
                for data in row_data:
                    if str(data.Key)=="PO_COMP_RECORD_ID":
                        pop_val=str(data.Value) + "|addonproducts"
                        cpqidval=CPQID.KeyCPQId.GetCPQId(ObjectName,str(data.Value))
                        new_value_dict[data.Key]=cpqidval
                    else:
                        new_value_dict[data.Key]=data.Value
                    new_value_dict["pop_val"]=pop_val
                date_field.append(new_value_dict)
        QueryCount=len(date_field)
        Product.SetGlobal("QueryCount",str(QueryCount))
        operation_type = 'addEquipment'
    elif ObjectName=="SAQSCN":
        ObjectName="PRLPBE"
        Header_details={ "PRICEBOOK_ENTRIES_RECORD_ID": "KEY","GREENBOOK": "GREENBOOK","DIVISION_ID": "DIVISION","BUSINESS_UNIT": "BU","POSS_NSO_PART_ID": "AGS POSS ID","POSS_NSO_DESCRIPTION": "POSS FOR NSO DESCRIPTION" }
        ordered_keys=["PRICEBOOK_ENTRIES_RECORD_ID","GREENBOOK","DIVISION_ID","BUSINESS_UNIT","POSS_NSO_PART_ID","POSS_NSO_DESCRIPTION"]
        sec_str='<div class="row modulebnr brdr ma_mar_btm">ADD NSOS<button type="button" class="close flt_rt" onclick="closepopup_scrl(this)" data-dismiss="modal">X</button></div>'
        sec_str +='<div class="col-md-12 padlftrhtnone" id="btnhide"><div class="row pad-10 bg-lt-wt brdr"><img style="height: 40px; margin-top: -1px; margin-left: -1px; float: left;" src="/mt/APPLIEDMATERIALS_PRD/Additionalfiles/Secondary Icon.svg"/><div class="product_txt_div_child secondary_highlight" style="display: block;"><div class="product_txt_child"><abbr title="Key">Add NSOS</abbr></div><div class="product_txt_to_top_child" style="float: left;"><abbr title="Select from the list of parts below to add them to {greenbook}">Select from the list of parts below to add them to {greenbook}</abbr></div></div><div class="product_txt_div_child secondary_highlight" style="display: block;"></div><button type="button" class="btnconfig" data-dismiss="modal" onclick="closepopup_scrl()">CANCEL</button><button type="button" id="add_nsos" class="btnconfig" onclick="add_nsos()" data-dismiss="modal">ADD</button></div></div>'.format(
            TreeParam,TreeParam,greenbook=TreeParentParam,
        )
        sec_str +='<div id="container" class="g4 pad-10 brdr except_sec">'
        sec_str +=( '<table id="' + str(id_name) + '" data-escape="true"  data-search-on-enter-key="true" data-show-header="true"  data-filter-control="true"> <thead><tr>' )
        sec_str +='<th data-field="SELECT" class="wth45" data-checkbox="true" id="check_boxval" onchange="get_checkedval()"><div class="action_col">SELECT</div></th>'
        for key,invs in enumerate(list(ordered_keys)):
            invs=str(invs).strip()
            qstring=Header_details.get(str(invs)) or ""
            if key==0:
                sec_str +=( '<th data-field="' + str(invs) + '" data-formatter="nsoKeyHyperLink" data-sortable="true" data-title-tooltip="' + str(qstring) + '" data-filter-control="input">' + str(qstring) + "</th>" )
            else:
                sec_str +=( '<th data-field="' + invs + '" data-title-tooltip="' + str(qstring) + '" data-sortable="true" data-filter-control="input">' + str(qstring) + "</th>" )
        sec_str +='</tr></thead><tbody class="user_id" ></tbody></table>'
        sec_str +='<div id="nso_addnew_footer"></div>'
        for invsk in list(Header_details):
            filter_class=id_names + " .bootstrap-table-filter-control-" + str(invsk)
            values_lists +="var " + str(invsk) + '=$("' + str(filter_class) + '").val(); '
            values_lists +=" ATTRIBUTE_VALUEList.push(" + str(invsk) + "); "
            attribute_list.append(invsk)
            filter_control_function +=('$("' + filter_class + '").change( function(){ var id_name=$(this).closest("table").attr("id"); var a_list=' + str(attribute_list) + "; ATTRIBUTE_VALUEList=[]; " + str(values_lists) + ' SortColumn=localStorage.getItem("SortColumn"); SortColumnOrder=localStorage.getItem("SortColumnOrder"); PerPage=$("#PageCountValue").val(); PageInform="1___" + PerPage + "___" + PerPage; cpq.server.executeScript("SYUADNWPOP",{\'TABLEID\': "' + str(TABLEID) + "\",'OPER': 'NO','RECORDID': \"" + str(RECORDID) + "\",'RECORDFEILD':  \"" + str(RECORDFEILD) + "\",'NEWVALUE': '','LOOKUPOBJ': '','LOOKUPAPI': '','A_Keys':a_list,'A_Values':ATTRIBUTE_VALUEList,'PerPage':PerPage,'PageInform':PageInform},function(data) {  debugger; var date_field =data[3]; var assoc=data[1]; var api_name=data[2];data4=data[4];data5=data[5];data15=data[15]; data16=data[16]; try { if(date_field !='NORECORDS') { $(\"" + str(id_names) + '").bootstrapTable("load",date_field  ); $("button#country_save").attr("disabled",false); $("#noRecDisp").remove();if (document.getElementById("RecordsStartAndEnd")){document.getElementById("RecordsStartAndEnd").innerHTML=data15;}; if (document.getElementById("TotalRecordsCount")) {document.getElementById("TotalRecordsCount").innerHTML=data16;} } else{ $("' + str(id_names) + '").bootstrapTable("load",date_field  ); $("button#country_save").attr("disabled",true); $("'+str(id_names)+' > tbody").html("<tr class=\'noRecDisp\'><td colspan=\'7\' class=\'txt_al_lt_imp\'>No Records to Display</td></tr>"); $(".noRecord:not(:first)").remove(); } } catch(err) { if(date_field !="NORECORDS") { $("' + str(id_names) + '").bootstrapTable("load",date_field  ); $("button#country_save").attr("disabled",false); } else{ $("' + str(id_names) + '").bootstrapTable("load",date_field  ); $("button#country_save").attr("disabled",true); } } ; });  });')
            dbl_clk_function=('$("' + str(id_names) + '").on("all.bs.table",function (e,name,args) { $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); });  $(".bs-checkbox input").addClass("custom"); $("' + str(id_names) + "\").on('sort.bs.table',function (e,name,order) {e.stopPropagation(); currenttab=$(\"ul#carttabs_head .active\").text().trim(); localStorage.setItem('" + str(id_name) + "_SortColumn',name); localStorage.setItem('" + str(id_name) + "_SortColumnOrder',order); ATTRIBUTE_VALUEList=[]; "+str(values_lists)+" AddNewContainerSorting(name,order,'" + str(id_name) + "',"+str(attribute_list)+",ATTRIBUTE_VALUEList,'"+str(TABLEID)+"','"+str(RECORDID)+"','"+str(RECORDFEILD)+"'); }); ")
        pagination_condition="OFFSET {Offset_Skip_Count} ROWS FETCH NEXT {Fetch_Count} ROWS ONLY".format( Offset_Skip_Count=offset_skip_count,Fetch_Count=fetch_count )
        if order_by=="":
            order_by="order by GREENBOOK ASC"
        #A055S000P01-20739 - START - M
        if where_string:
            where_string +=" AND"
        where_string +=""" GREENBOOK='{}' AND PRICEBOOK_TYPE='POSS' AND  POSS_NSO_PART_ID NOT IN (SELECT POSS_NSO_PART_ID FROM SAQSCN (NOLOCK) WHERE QUOTE_RECORD_ID='{}' AND QTEREV_RECORD_ID='{}' AND GREENBOOK='{}' AND PAR_SERVICE_ID='{}')""".format( TreeParentParam,contract_quote_record_id,quote_revision_record_id,TreeParentParam,Quote.GetGlobal("TreeParentLevel1") )
        #A055S000P01-20739 - END - M
        table_data=Sql.GetList("select top {} {} from {} (NOLOCK) {} {} ".format(PerPage,",".join(ordered_keys),ObjectName,"WHERE " + where_string if where_string else "",order_by,pagination_condition))
        table_data=Sql.GetList("select {} from {} (NOLOCK) {} {} {}".format(",".join(ordered_keys),ObjectName,"WHERE " + where_string if where_string else "",order_by,pagination_condition ))
        QueryCountObj=Sql.GetFirst("select count(*) as cnt from {} (NOLOCK) {} ".format( ObjectName,"WHERE " + where_string if where_string else ""))
        if table_data is not None:
            for row_data in table_data:
                new_value_dict={}
                for data in row_data:
                    if str(data.Key)=="PRICEBOOK_ENTRIES_RECORD_ID":
                        pop_val=str(data.Value) + "|Offerings"
                        cpqidval=CPQID.KeyCPQId.GetCPQId(ObjectName,str(data.Value))
                        new_value_dict[data.Key]=cpqidval
                    else:
                        new_value_dict[data.Key]=data.Value
                    new_value_dict["pop_val"]=pop_val
                date_field.append(new_value_dict)
        QueryCount=len(date_field)
        Product.SetGlobal("QueryCount",str(QueryCount))
        operation_type = "addFab"
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
Result = addon_addnew_popup(PerPage,PageInform,SortColumn,SortColumnOrder,offset_skip_count,fetch_count)

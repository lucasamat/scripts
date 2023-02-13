#=========================================================================================================================================
#   __script_name: SYADSVEPOP.PY (SYUADNWPOP Linked)
#   __script_description: THIS SCRIPT IS USED FOR SERVICE LEVEL ADD POPUPS
#   __primary_author__: MUTHUMANI,VIKNESH DURAISAMY
#   __create_date: 18/11/2022
#=========================================================================================================================================
from math import ceil
import SYCNGEGUID as CPQID
import Webcom.Configurator.Scripting.Test.TestProduct
TestProduct=Webcom.Configurator.Scripting.Test.TestProduct()

def service_addnew_popup(PerPage,PageInform,SortColumn,SortColumnOrder,offset_skip_count,fetch_count,TreeParam,ObjectName):
    sec_str=var_str=filter_control_function=dbl_clk_function=filter_drop_down=order_by=disable_next_and_last=disable_previous_and_first=values_lists=""
    new_value_dict = {}
    sec_join = '<div class="col-md-12 padlftrhtnone" id="btnhide"><div class="row pad-10 bg-lt-wt brdr"><img style="height: 40px; margin-top: -1px; margin-left: -1px; float: left;" src="/mt/APPLIEDMATERIALS_UAT/Additionalfiles/Secondary Icon.svg"/><div class="product_txt_div_child secondary_highlight" style="display: block;text-align: left;"><div class="product_txt_child"><abbr title="Key">'
    sec_join_end = '</abbr></div></div><button type="button" class="btnconfig" data-dismiss="modal" onclick="closepopup_scrl()">CANCEL</button><button type="button" id="add-offerings" class="btnconfig" onclick="addcoveredobjs()" data-dismiss="modal">ADD</button></div></div>'
    sec_js = 'SortColumn=localStorage.getItem("SortColumn"); SortColumnOrder=localStorage.getItem("SortColumnOrder"); PerPage=$("#PageCountValue").val(); PageInform="1___"+PerPage+"___"+PerPage; cpq.server.executeScript("SYUADNWPOP",{\'TABLEID\':'
    get_sales_org=Sql.GetFirst("SELECT * FROM SAQTRV (NOLOCK) WHERE QUOTE_RECORD_ID='{}' AND QTEREV_RECORD_ID='{}'".format(quote_rec_id,quote_rev_id) )
    attribute_list=[]
    date_field=[]
    pop_val={}
    script_details=poputilObj.get_script_details(TreeParam)
    master_obj_name=script_details[ObjectName]['master_object_name']
    id_name=str(script_details[ObjectName]['ID_NAME'])
    id_names="#"+str(id_name)
    account_id=TreeParam.split(' - ')
    account_id=account_id[len(account_id)-1]
    where_string=poputilObj.construct_where_string(A_Keys,A_Values,master_obj_name)
    if str(PerPage)=="" and str(PageInform)=="":
        Page_start=1
        Page_End=PerPage=fetch_count
        PageInform="1___"+str(fetch_count)+"___"+str(fetch_count)
    else:
        Page_start=int(PageInform.split("___")[0])
        Page_End=int(PageInform.split("___")[1])
        PerPage=PerPage
    if SortColumn !='' and SortColumnOrder !='':
        order_by="order by "+SortColumn+" "+SortColumnOrder
    if offset_skip_count%10==1:
        offset_skip_count-=1
    if ObjectName=="SAQSCO":
        ObjectName="SAQSCO" if TreeParam=='Add-On Products' else "SAQFEQ"
        Header_details,ordered_keys=poputilObj.get_header_details(ObjectName,TreeParam)
        sec_str='<div class="row modulebnr brdr ma_mar_btm">INSTALLED BASE EQUIPMENT LIST<button type="button" class="close flt_rt" onclick="closepopup_scrl()" data-dismiss="modal">X</button></div>'
        if str(TABLEID)=='ADDNEW__SYOBJR_98800_0D035FD5_F0EA_4F11_A0DB_B4E10928B59F' and TreeParentParam.upper()=='ADD-ON PRODUCTS':
            getService=Sql.GetFirst("select SERVICE_DESCRIPTION from SAQSAO(nolock) where SERVICE_ID='"+TreeSuperParentParam+"' and ADNPRD_ID='"+TreeParam+"'")
            sec_str+= sec_join+'Parent Product Offering ID</abbr></div><div class="product_txt_to_top_child"><abbr title="{productid}">{productid}</abbr></div></div><div class="product_txt_div_child secondary_highlight" style="display: block;text-align: left;"><div class="product_txt_child"><abbr title="Key">Parent Product Description</abbr></div><div class="product_txt_to_top_child"><abbr title="{description}">{description}</abbr></div></div><div class="product_txt_div_child secondary_highlight" style="display: block;text-align: left;"><div class="product_txt_child"><abbr title="Key">Equipment</abbr></div><div class="product_txt_to_top_child"><abbr title="ALL">ALL'+sec_join_end.format(productid=TreeSuperParentParam,description=getService.SERVICE_DESCRIPTION if getService else "")
        else:
            sec_str+= sec_join+'Equipment ID</abbr></div><div class="product_txt_to_top_child"><abbr title="ALL">ALL</abbr></div></div><div class="product_txt_div_child secondary_highlight" style="display: block;text-align: left;"><div class="product_txt_child"><abbr title="Key">Fab Location ID</abbr></div><div class="product_txt_to_top_child"><abbr title="ALL">ALL</abbr></div></div><div class="product_txt_div_child secondary_highlight" style="display: none;text-align: left;"><div class="product_txt_child"><abbr title="Key">Sales Org</abbr></div><div class="product_txt_to_top_child"><abbr title="2044">2044'+sec_join_end
        sec_str+='<div id="container" class="g4 pad-10 brdr except_sec"><table id="'+str(id_name)+'" data-escape="true"  data-search-on-enter-key="true" data-show-header="true"  data-filter-control="true"><thead><tr><th data-field="SELECT" class="wth45" data-checkbox="true" id="check_boxval" onchange="get_checkedval()"><div>SELECT</div></th>'        
        for key,invs in enumerate(list(ordered_keys)):
            invs=str(invs).strip()
            qstring=Header_details.get(invs) or ""
            formatter='data-formatter="CovObjKeyHyperLink"' if key==0 else ''
            #A055S000P01-20930 -Start
            if str(invs)=="TEMP_TOOL":
                formatter = 'data-formatter = "CheckboxFieldRelatedList"'
            #A055S000P01-20930 -End
            sec_str+=('<th data-field="'+invs+'" '+formatter+' data-sortable="true" data-title-tooltip="'+str(qstring)+'" data-filter-control="input">'+str(qstring)+"</th>")
        sec_str+='</tr></thead><tbody class="equipments_id" ></tbody></table><div id="Coveredobjectsaddnew_footer"></div>'
        for invsk in list(Header_details):
            filter_class=id_names+" .bootstrap-table-filter-control-"+str(invsk)
            values_lists+="var "+str(invsk)+'=$("'+str(filter_class)+'").val(); '
            values_lists+=" ATTRIBUTE_VALUEList.push("+str(invsk)+"); "
            attribute_list.append(invsk)
            filter_control_function+=('$("'+filter_class+'").change( function(){ var id_name=$(this).closest("table").attr("id"); var a_list='+str(attribute_list)+"; ATTRIBUTE_VALUEList=[]; "+str(values_lists)+' '+sec_js+' "'+str(TABLEID)+"\",'OPER': 'NO','RECORDID': \""+str(RECORDID)+"\",'RECORDFEILD':  \""+str(RECORDFEILD)+"\",'NEWVALUE': '','LOOKUPOBJ': '','LOOKUPAPI': '','A_Keys':a_list,'A_Values':ATTRIBUTE_VALUEList},function(data) {  date_field=data[3]; var assoc=data[1]; var api_name=data[2];data4=data[4];data5=data[5]; data15=data[15]; data16=data[16];  try { if(date_field.length > 0) { $(\""+id_names+'").bootstrapTable("load",date_field  ); $("button#country_save").attr("disabled",false); $("#noRecDisp").remove(); if (document.getElementById("RecordsStartAndEnd")){document.getElementById("RecordsStartAndEnd").innerHTML=data15;}; if (document.getElementById("TotalRecordsCount")) {document.getElementById("TotalRecordsCount").innerHTML=data16;} } else{ $("'+id_names+'").bootstrapTable("load",date_field  ); $("button#country_save").attr("disabled",true); $("#Coveredobjectsaddnew").after("<div id=\'noRecDisp\' class=\'noRecord\'>No Records to Display</div>"); $(".noRecord:not(:first)").remove(); } } catch(err) { if(date_field.length > 0) { $("'+id_names+'").bootstrapTable("load",date_field  ); $("button#country_save").attr("disabled",false); } else{ $("'+id_names+'").bootstrapTable("load",date_field  ); $("button#country_save").attr("disabled",true);} } ;});});')
            dbl_clk_function=('$("'+id_names+'").on("all.bs.table",function (e,name,args) { $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); });  $(".bs-checkbox input").addClass("custom"); $("'+id_names+"\").on('sort.bs.table',function (e,name,order) {e.stopPropagation(); currenttab=$(\"ul#carttabs_head .active\").text().trim(); localStorage.setItem('"+str(id_name)+"_SortColumn',name); localStorage.setItem('"+str(id_name)+"_SortColumnOrder',order); ATTRIBUTE_VALUEList=[]; "+str(values_lists)+" AddNewContainerSorting(name,order,'"+str(id_name)+"',"+str(attribute_list)+",ATTRIBUTE_VALUEList,'"+str(TABLEID)+"','"+str(RECORDID)+"','"+str(RECORDFEILD)+"');});")
        pagination_condition="OFFSET {Offset_Skip_Count} ROWS FETCH NEXT {Fetch_Count} ROWS ONLY".format( Offset_Skip_Count= offset_skip_count,Fetch_Count=fetch_count)
        order_by="order by EQUIPMENT_ID ASC" if order_by=="" else order_by
        where_string +=" AND" if where_string else ''
        where_string+=" QUOTE_RECORD_ID='{quo_rec_id}' AND QTEREV_RECORD_ID='{qurev_rec_id}' ".format(quo_rec_id=quote_rec_id,qurev_rec_id=quote_rev_id)
        if TreeParam in ('Sending Equipment','Receiving Equipment'):
            where_string+="AND RELOCATION_EQUIPMENT_TYPE='SENDING EQUIPMENT' AND EQUIPMENT_ID NOT IN(SELECT EQUIPMENT_ID FROM SAQSCO WHERE QUOTE_RECORD_ID='{quo_rec_id}' and SERVICE_ID='{TreeParam}' AND QTEREV_RECORD_ID='{qurev_rec_id}' AND RELOCATION_EQUIPMENT_TYPE='RECEIVING EQUIPMENT')".format(quo_rec_id=quote_rec_id,TreeParam=TreeParentParam,qurev_rec_id=quote_rev_id)
        elif TreeParam=='Add-On Products':
            #A055S000P01-21015 - Start - M
            where_string+="AND SERVICE_ID='{TreeSuperParentParam}' AND GREENBOOK='{TreeParentParam}' AND SAQSCO.QTEREVFEQ_RECORD_ID NOT IN (SELECT QTEREVFEQ_RECORD_ID FROM SAQSCO WHERE QUOTE_RECORD_ID='{quo_rec_id}' and SERVICE_ID='{addon_service_id}' AND PAR_SERVICE_ID='{TreeSuperParentParam}' AND QTEREV_RECORD_ID='{qurev_rec_id}') ".format(quo_rec_id=quote_rec_id,TreeParam=TreeParam,qurev_rec_id=quote_rev_id,TreeSuperParentParam=TreeSuperParentParam,TreeParentParam=TreeParentParam,restrict_tools=" EQUIPMENTCATEGORY_ID='Y' AND " if TreeParam=="Z0004" else "", addon_service_id = Product.GetGlobal("addon_service_id"))
            #A055S000P01-21015 - End - M
        else:
            where_string+="AND {restrict_tools} QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID NOT IN (SELECT QTEREVFEQ_RECORD_ID FROM SAQSCO WHERE QUOTE_RECORD_ID='{quo_rec_id}' and SERVICE_ID='{TreeParam}' AND QTEREV_RECORD_ID='{qurev_rec_id}')".format(quo_rec_id=quote_rec_id,TreeParam=TreeParam,qurev_rec_id=quote_rev_id,restrict_tools="")
            if TreeParam=="Z0007" and TreeParentParam=="Complementary Products":
                where_string+="AND EXISTS (SELECT * FROM SAQASE WHERE QUOTE_RECORD_ID='{quo_rec_id}' AND QTEREV_RECORD_ID='{qurev_rec_id}')".format(quo_rec_id=quote_rec_id,qurev_rec_id=quote_rev_id)
        if TreeParentParam=="Add-On Products" and TreeParam !="":
            table_data=Sql.GetList("select SAQFEQ.QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID,SAQFEQ.EQUIPMENT_ID,SAQFEQ.EQUIPMENT_DESCRIPTION,SAQFEQ.SERIAL_NUMBER,SAQFEQ.PBG,SAQFEQ.PLATFORM,SAQFEQ.FABLOCATION_ID,SAQFEQ.FABLOCATION_NAME from  SAQFEQ(NOLOCK) JOIN SAQSCO ON SAQSCO.QUOTE_RECORD_ID=SAQFEQ.QUOTE_RECORD_ID AND SAQSCO.QTEREV_RECORD_ID=SAQFEQ.QTEREV_RECORD_ID AND SAQSCO.EQUIPMENT_ID=SAQFEQ.EQUIPMENT_ID  WHERE SAQFEQ.QUOTE_RECORD_ID='{quo_rec_id}' AND SAQSCO.SERVICE_ID='{parent}' AND SAQSCO.QTEREV_RECORD_ID='{qurev_rec_id}' AND SAQFEQ.EQUIPMENT_ID NOT IN(SELECT EQUIPMENT_ID FROM SAQSCO WHERE QUOTE_RECORD_ID='{quo_rec_id}' and SERVICE_ID='{TreeParam}' AND QTEREV_RECORD_ID='{qurev_rec_id}' ) order by EQUIPMENT_ID ASC offset {offset_skip_count} rows fetch next {per_page} rows only".format(per_page=PerPage,offset_skip_count=offset_skip_count,quo_rec_id=quote_rec_id,TreeParam=TreeParam,parent=TreeSuperParentParam,qurev_rec_id=quote_rev_id))
        elif TreeParam=="Add-On Products":
            #A055S000P01-21015 - Start - M
            table_data=Sql.GetList("SELECT QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,EQUIPMENT_ID,EQUIPMENTCATEGORY_DESCRIPTION,SERIAL_NO,CUSTOMER_TOOL_ID,GREENBOOK,EQUIPMENT_STATUS,PLATFORM,FABLOCATION_ID,WARRANTY_START_DATE,WARRANTY_END_DATE,WARRANTY_END_DATE_ALERT FROM SAQSCO WHERE {where_string} order by EQUIPMENT_ID ASC offset {offset_skip_count} rows fetch next {per_page} rows only".format(per_page=PerPage,quo_rec_id=quote_rec_id,TreeParam=TreeParam,qurev_rec_id=quote_rev_id,offset_skip_count=offset_skip_count,TreeSuperParentParam=TreeSuperParentParam,TreeParentParam=TreeParentParam,where_string=where_string))
            #A055S000P01-21015 - End - M
        else:
            table_data=Sql.GetList("select {} from {} (NOLOCK) {} {} {} ".format( ",".join(ordered_keys),ObjectName,"WHERE "+where_string if where_string else "",order_by,pagination_condition))
        QueryCountObj=Sql.GetFirst("select count(*) as cnt from {} (NOLOCK) {} ".format(ObjectName,"WHERE "+where_string if where_string else ""))
        if QueryCountObj is not None:
            QryCount=QueryCountObj.cnt
        if table_data is not None:
            for row_data in table_data:
                new_value_dict={}
                for data in row_data:
                    if str(data.Key) in ("QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID","QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID"):
                        pop_val=str(data.Value)+"|Covered Objects"
                        cpqidval=CPQID.KeyCPQId.GetCPQId(ObjectName,str(data.Value))
                    elif str(data.Key)=="TEMP_TOOL":
                        cpqidval='<input  type="checkbox" class="custom"  value="'+str(data.Value)+'" style="text-align: center;" {checked} disabled><span class="lbl"></span>'.format(checked="checked" if str(data.Value).upper()=="TRUE" else "")
                    else:
                        try:
                            cpqidval=str(data.Value)
                        except Exception:
                            cpqidval=data.Value
                    new_value_dict[data.Key]=cpqidval
                    new_value_dict["pop_val"]=pop_val
                date_field.append(new_value_dict)
            operation_type="addCoveredObj"
    elif ObjectName=="SAQTSV":
        Header_details,ordered_keys=poputilObj.get_header_details(ObjectName,TreeParam)
        ObjectName="MAMTRL"
        sec_str='<div class="row modulebnr brdr ma_mar_btm">ADD OFFERINGS<button type="button" class="close flt_rt" onclick="closepopup_scrl()" data-dismiss="modal">X</button></div><div class="col-md-12 padlftrhtnone"><div class="row pad-10 bg-lt-wt brdr"> <img style="height: 40px; margin-top: -1px; margin-left: -1px; float: left;" src="/mt/APPLIEDMATERIALS_UAT/Additionalfiles/Secondary Icon.svg"/><div class="product_txt_div_child secondary_highlight" style="display: block;text-align: left;"><div class="product_txt_child"><abbr title="Key">PRODUCT OFFERING</abbr></div><div class="product_txt_to_top_child"><abbr title="ALL">Select a Product Offering to add to your list of Quote Product Offerings</abbr></div></div></div></div><div id="container" class="g4 pad-10 brdr except_sec"><table id="'+str(id_name)+'" data-escape="true" data-search-on-enter-key="true" data-show-header="true"  data-filter-control="true"><thead><tr>'        
        for key,invs in enumerate(list(ordered_keys)):
            invs=str(invs).strip()
            qstring=Header_details.get(invs) or ""
            if key==0:
                sec_str+=('<th data-field="'+invs+'" data-formatter="offeringsModelListKeyHyperLink" data-sortable="true" data-title-tooltip="'+str(qstring)+'" data-filter-control="input">'+str(qstring)+"</th>")
            else:
                sec_str+=('<th data-field="'+invs+'" data-title-tooltip="'+str(qstring)+'" data-sortable="true" data-filter-control="input">'+str(qstring)+"</th>")
        sec_str+='</tr></thead><tbody class="user_id" ></tbody></table><div id="add-offerings-model-footer"></div>'
        for invsk in list(Header_details):
            filter_class=id_names+" .bootstrap-table-filter-control-"+str(invsk)
            values_lists+="var "+str(invsk)+'=$("'+str(filter_class)+'").val(); '
            values_lists+=" ATTRIBUTE_VALUEList.push("+str(invsk)+"); "
            attribute_list.append(invsk)
            filter_control_function+=('$("'+filter_class+'").change( function(){ var id_name=$(this).closest("table").attr("id"); var a_list='+str(attribute_list)+"; ATTRIBUTE_VALUEList=[]; "+str(values_lists)+' '+sec_js+' "'+str(TABLEID)+"\",'OPER': 'NO','RECORDID': \""+str(RECORDID)+"\",'RECORDFEILD':  \""+str(RECORDFEILD)+"\",'NEWVALUE': '','LOOKUPOBJ': '','LOOKUPAPI': '','A_Keys':a_list,'A_Values':ATTRIBUTE_VALUEList},function(data) {  date_field=data[3]; var assoc=data[1]; var api_name=data[2];data4=data[4];data5=data[5]; data15=data[15]; data16=data[16]; try { if(date_field.length > 0) { $(\""+id_names+'").bootstrapTable("load",date_field  );$("#noRecDisp").remove(); if (document.getElementById("RecordsStartAndEnd")){document.getElementById("RecordsStartAndEnd").innerHTML=data15;}; if (document.getElementById("TotalRecordsCount")) {document.getElementById("TotalRecordsCount").innerHTML=data16;} } else{ $("'+id_names+'").bootstrapTable("load",date_field  );$("#offerings-addnew-model").after("<div id=\'noRecDisp\' class=\'noRecord\'>No Records to Display</div>"); $(".noRecord:not(:first)").remove(); } } catch(err) { if(date_field.length > 0) { $("'+id_names+'").bootstrapTable("load",date_field  ); } else{ $("'+id_names+'").bootstrapTable("load",date_field  ); document.getElementById("add-offerings-model-footer").style.border="1px solid #ccc"; document.getElementById("add-offerings-model-footer").style.padding="5.5px"; document.getElementById("add-offerings-model-footer").innerHTML="No Records to Display";} };});});')
            dbl_clk_function=('$("'+id_names+'").on("all.bs.table",function (e,name,args) {$(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); var count=0; var selectAll=false; $("#add-offerings").css("display","none"); $("#offerings-addnew-model").find(\'[type="checkbox"]:checked\').map(function () {var sel_val=$(this).closest("tr").find("td:nth-child(2)").text(); count=1; if ($(this).attr("name")=="btSelectAll"){var selectAll=true; $("#add-offerings").css("display","block");} else if (sel_val !="") {$("#add-offerings").css("display","block");} else{$("#add-offerings").css("display","none");}});if(count==0){$("#add-offerings").css("display","none");}}); $(".bs-checkbox input").addClass("custom"); $("'+id_names+"\").on('sort.bs.table',function (e,name,order) {e.stopPropagation(); currenttab=$(\"ul#carttabs_head .active\").text().trim(); localStorage.setItem('"+str(id_name)+"_SortColumn',name); localStorage.setItem('"+str(id_name)+"_SortColumnOrder',order); ATTRIBUTE_VALUEList=[]; "+str(values_lists)+" AddNewContainerSorting(name,order,'"+str(id_name)+"',"+str(attribute_list)+",ATTRIBUTE_VALUEList,'"+str(TABLEID)+"','"+str(RECORDID)+"','"+str(RECORDFEILD)+"');});")
        pagination_condition="OFFSET {Offset_Skip_Count} ROWS FETCH NEXT {Fetch_Count} ROWS ONLY".format(Offset_Skip_Count=offset_skip_count,Fetch_Count=fetch_count)
        inner_join=additional_where=""
        if TreeParam in ("Comprehensive Services","Product Offerings","Complementary Products") and get_sales_org:            
            inner_join=" INNER JOIN MAMSOP (NOLOCK) ON MAMTRL.MATERIAL_RECORD_ID=MAMSOP.MATERIAL_RECORD_ID JOIN MAADPR (NOLOCK) ON MAADPR.PRDOFR_ID=MAMTRL.SAP_PART_NUMBER AND MAADPR.PRDOFR_ID=MAMSOP.SAP_PART_NUMBER"
            additional_where=" AND SALESORG_ID='{}' ".format(get_sales_org.SALESORG_ID)
        order_by="order by MAMTRL.SAP_PART_NUMBER ASC" if order_by=="" else order_by
        where_string+=" AND" if where_string else ''
        ordered_keys=["MAMTRL.MATERIAL_RECORD_ID","MAMTRL.SAP_PART_NUMBER","SAP_DESCRIPTION","PRODUCT_TYPE"]
        if TreeParam=="Product Offerings":
            where_string+=""" PRODUCT_TYPE IS NOT NULL AND PRODUCT_TYPE <> '' AND PRODUCT_TYPE !='Add-On Products' AND MAADPR.PRDOFR_DOCTYP='{}' AND  MAADPR.VISIBLE_INCONFIG='TRUE'  AND NOT EXISTS (SELECT SERVICE_ID FROM SAQTSV (NOLOCK) WHERE QUOTE_RECORD_ID='{}' AND QTEREV_RECORD_ID='{}' AND MAMTRL.SAP_PART_NUMBER=SAQTSV.SERVICE_ID)""".format(get_sales_org.DOCTYP_ID,quote_rec_id,quote_rev_id)
        else:
            where_string+=""" PRODUCT_TYPE='{}' AND MAMTRL.SAP_PART_NUMBER NOT IN (SELECT SERVICE_ID FROM SAQTSV (NOLOCK) WHERE QUOTE_RECORD_ID='{}' AND QTEREV_RECORD_ID='{}')""".format(TreeParam,quote_rec_id,quote_rev_id)
        table_data=Sql.GetList("select distinct {} from {} (NOLOCK) {} {} {} {} {}".format( ",".join(ordered_keys),ObjectName,inner_join if inner_join else "","WHERE "+where_string if where_string else "",additional_where,order_by,pagination_condition))
        QueryCountObj=Sql.GetFirst("select count(distinct MAMTRL.SAP_PART_NUMBER) as cnt from {} (NOLOCK) {} {} {}".format( ObjectName,inner_join if inner_join else "","WHERE "+where_string if where_string else "",additional_where))
        operation_type="addOfferings"
        date_field = poputilObj.gettable_data(ObjectName,table_data,key="MATERIAL_RECORD_ID",value="|Offerings",operation_type="addOfferings")
    elif ObjectName in ("SAQRSP","SAQSPT"):
        popup_obj=ObjectName
        where_string_1=""
        Header_details,ordered_keys=poputilObj.get_header_details(ObjectName,TreeParam)
        ObjectName="MAMTRL"
        sec_str='<div class="row modulebnr brdr ma_mar_btm">ADD PARTS<button type="button" class="close flt_rt" onclick="closepopup_scrl()" data-dismiss="modal">X</button></div><div class="col-md-12 padlftrhtnone"><div class="row pad-10 bg-lt-wt brdr"> <img style="height: 40px; margin-top: -1px; margin-left: -1px; float: left;" src="/mt/APPLIEDMATERIALS_UAT/Additionalfiles/Secondary Icon.svg"/><div class="product_txt_div_child secondary_highlight" style="display: block;text-align: left;"><div class="product_txt_child"><abbr title="Add Parts">Add Parts</abbr></div><div class="product_txt_to_top_child"><abbr title="Select from the list parts below to add them to your Product Offering...">Select from the list parts below to add them to your Product Offering...</abbr></div></div><button type="button" class="btnconfig" data-dismiss="modal" onclick="closepopup_scrl()">CANCEL</button><button type="button" id="add-parts" class="btnconfig" onclick="addPartsList()" data-dismiss="modal">ADD</button></div></div><div id="container" class="g4 pad-10 brdr except_sec">'
        sec_str+=('<table id="'+str(id_name)+'" data-escape="true"  data-search-on-enter-key="true" data-show-header="true"  data-filter-control="true"> <thead><tr>')
        sec_str+='<th data-field="SELECT" class="wth45" data-checkbox="true" id="check_boxval" onchange="get_checkedval()"><div class="action_col">SELECT</div></th>'
        for key,invs in enumerate(list(ordered_keys)):
            invs=str(invs).strip()
            qstring=Header_details.get(invs) or ""
            formatter='data-formatter="partsModelListKeyHyperLink"' if key==0 else ''
            sec_str+='<th data-field="'+invs+'" '+formatter+' data-sortable="true" data-title-tooltip="'+str(qstring)+'" data-filter-control="input">'+str(qstring)+"</th>"           
        sec_str+='</tr></thead><tbody class="user_id" ></tbody></table><div id="add-parts-model-footer"></div>'
        for invsk in list(Header_details):
            filter_class=id_names+" .bootstrap-table-filter-control-"+str(invsk)
            values_lists+="var "+str(invsk)+'=$("'+str(filter_class)+'").val(); '
            values_lists+=" ATTRIBUTE_VALUEList.push("+str(invsk)+"); "
            attribute_list.append(invsk)
            filter_control_function+=('$("'+filter_class+'").change( function(){ var id_name=$(this).closest("table").attr("id"); var a_list='+str(attribute_list)+"; ATTRIBUTE_VALUEList=[]; "+str(values_lists)+' '+sec_js+' "'+str(TABLEID)+"\",'OPER': 'NO','RECORDID': \""+str(RECORDID)+"\",'RECORDFEILD':  \""+str(RECORDFEILD)+"\",'SUBTAB':  \""+str(active_subtab)+"\",'NEWVALUE': '','LOOKUPOBJ': '','LOOKUPAPI': '','A_Keys':a_list,'A_Values':ATTRIBUTE_VALUEList},function(data) { debugger; date_field=data[3]; var assoc=data[1]; var api_name=data[2];data4=data[4];data5=data[5]; data15=data[15]; data16=data[16]; try { if(date_field.length > 0) { $(\""+id_names+'").bootstrapTable("load",date_field  );$("#noRecDisp").remove(); if (document.getElementById("RecordsStartAndEnd")){document.getElementById("RecordsStartAndEnd").innerHTML=data15;}; if (document.getElementById("TotalRecordsCount")) {document.getElementById("TotalRecordsCount").innerHTML=data16;} } else{ $("'+id_names+'").bootstrapTable("load",date_field  );$("#parts-addnew-model").after("<div id=\'noRecDisp\' class=\'noRecord\'>No Records to Display</div>"); $(".noRecord:not(:first)").remove(); } } catch(err) { if(date_field.length > 0) { $("'+id_names+'").bootstrapTable("load",date_field  ); } else{ $("'+id_names+'").bootstrapTable("load",date_field  ); document.getElementById("add-parts-model-footer").style.border="1px solid #ccc"; document.getElementById("add-parts-model-footer").style.padding="5.5px"; document.getElementById("add-parts-model-footer").innerHTML="No Records to Display";} };});});')
            dbl_clk_function=('$("'+id_names+'").on("all.bs.table",function (e,name,args) {$(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); var count=0; var selectAll=false; $("#add-offerings").css("display","none"); $("#parts-addnew-model").find(\'[type="checkbox"]:checked\').map(function () {var sel_val=$(this).closest("tr").find("td:nth-child(2)").text(); count=1; if ($(this).attr("name")=="btSelectAll"){var selectAll=true; $("#add-offerings").css("display","block");} else if (sel_val !="") { $("#add-offerings").css("display","block");} else{$("#add-offerings").css("display","none");}});if(count==0){$("#add-offerings").css("display","none");}}); $(".bs-checkbox input").addClass("custom"); $("'+id_names+"\").on('sort.bs.table',function (e,name,order) { e.stopPropagation(); currenttab=$(\"ul#carttabs_head .active\").text().trim(); localStorage.setItem('"+str(id_name)+"_SortColumn',name); localStorage.setItem('"+str(id_name)+"_SortColumnOrder',order); ATTRIBUTE_VALUEList=[]; "+str(values_lists)+" AddNewContainerSorting(name,order,'"+str(id_name)+"',"+str(attribute_list)+",ATTRIBUTE_VALUEList,'"+str(TABLEID)+"','"+str(RECORDID)+"','"+str(RECORDFEILD)+"'); }); " )
        pagination_condition="OFFSET {Offset_Skip_Count} ROWS FETCH NEXT {Fetch_Count} ROWS ONLY".format( Offset_Skip_Count=offset_skip_count,Fetch_Count=fetch_count)
        inner_join="INNER JOIN MAMSOP (NOLOCK) on MAMTRL.SAP_PART_NUMBER=MAMSOP.SAP_PART_NUMBER AND MAMTRL.MATERIAL_RECORD_ID=MAMSOP.MATERIAL_RECORD_ID "
        order_by="order by MAMTRL.SAP_PART_NUMBER ASC" if order_by=="" else order_by
        where_string+=" AND" if where_string else ''
        ordered_keys_mam=["MAMTRL.MATERIAL_RECORD_ID","MAMTRL.SAP_PART_NUMBER","MAMTRL.SAP_DESCRIPTION","MAMSOP.MATPRIGRP_ID"]        
        if str(popup_obj)=="SAQRSP":
            if TreeSuperParentParam=="Product Offerings":
                Service_Id=TreeParam
                TableName="SAQTSE"
                gbk_cndtn = ""
            else:
                Service_Id=TreeParentParam
                TableName="SAQSGE"
                gbk_cndtn = " AND GREENBOOK='{}'".format(TreeParam)
            entitlement_obj=Sql.GetFirst("select replace(ENTITLEMENT_XML,'&',';#38') as ENTITLEMENT_XML from {} (nolock) where QUOTE_RECORD_ID='{}' AND QTEREV_RECORD_ID='{}' and SERVICE_ID='{}' {}".format(TableName,quote_rec_id,quote_rev_id,Service_Id,gbk_cndtn))
            iclusions_val_list,new_parts_yes=poputilObj.get_entitlement_xml(Service_Id,entitlement_obj.ENTITLEMENT_XML,TreeParam,TableName,TreeSuperParentParam)
            where_string_1=where_string
            if new_parts_yes=="Yes" and active_subtab=='New Parts':
                where_string+=""" MAMSOP.SALESORG_ID='{sales}' AND MAMTRL.PRODUCT_TYPE IS NULL AND NOT EXISTS (SELECT PART_NUMBER FROM SAQRSP (NOLOCK) WHERE QUOTE_RECORD_ID='{qt_rec_id}' AND QTEREV_RECORD_ID='{qt_rev_id}' AND MAMTRL.SAP_PART_NUMBER=SAQRSP.PART_NUMBER AND (SAQRSP.NEW_PART='True' OR (SAQRSP.NEW_PART='False' AND SAQRSP.INCLUDED='False')) AND SAQRSP.PAR_SERVICE_ID='{service_id}' AND GREENBOOK='{treeParam}')""".format(sales=get_sales_org.SALESORG_ID,qt_rec_id=quote_rec_id,qt_rev_id=quote_rev_id,service_id=Service_Id,treeParam=TreeParam)
                paginationQuery="""SELECT COUNT(MAMTRL.CpqTableEntryId) as cnt FROM MAMTRL (NOLOCK) JOIN MAMSOP (NOLOCK) ON MAMSOP.SAP_PART_NUMBER=MAMTRL.SAP_PART_NUMBER WHERE {whrStr1} MAMSOP.SALESORG_ID='{sales}' AND MAMTRL.PRODUCT_TYPE IS NULL AND MAMTRL.SAP_PART_NUMBER NOT IN (SELECT PART_NUMBER FROM SAQRSP (NOLOCK) WHERE QUOTE_RECORD_ID='{qt_rec_id}' AND QTEREV_RECORD_ID='{qt_rev_id}' AND (SAQRSP.NEW_PART='True' OR (SAQRSP.NEW_PART='False' AND SAQRSP.INCLUDED='False')) AND SAQRSP.PAR_SERVICE_ID='{service_id}' AND GREENBOOK='{treeParam}')""".format(sales=get_sales_org.SALESORG_ID,qt_rec_id=quote_rec_id,qt_rev_id=quote_rev_id,service_id=Service_Id,whrStr1=str(where_string_1) if where_string_1 else "",treeParam=TreeParam)
            elif active_subtab=='Inclusions':
                where_string+=""" MAMSOP.SALESORG_ID='{sales}' AND MAMTRL.PRODUCT_TYPE IS NULL AND NOT EXISTS (SELECT PART_NUMBER FROM SAQRSP (NOLOCK) WHERE QUOTE_RECORD_ID='{qt_rec_id}' AND QTEREV_RECORD_ID='{qt_rev_id}' AND MAMTRL.SAP_PART_NUMBER=SAQRSP.PART_NUMBER AND SAQRSP.PAR_SERVICE_ID='{service_id}' AND (SAQRSP.INCLUDED='True' OR (SAQRSP.INCLUDED='False' AND SAQRSP.NEW_PART='False')) AND GREENBOOK='{treeParam}')""".format(sales=get_sales_org.SALESORG_ID,qt_rec_id=quote_rec_id,qt_rev_id=quote_rev_id,service_id=Service_Id,treeParam=TreeParam)
                paginationQuery="""SELECT COUNT(MAMTRL.CpqTableEntryId) as cnt FROM MAMTRL (NOLOCK) JOIN MAMSOP (NOLOCK) ON MAMSOP.SAP_PART_NUMBER=MAMTRL.SAP_PART_NUMBER WHERE {whrStr1} MAMSOP.SALESORG_ID='{sales}' AND MAMTRL.PRODUCT_TYPE IS NULL AND MAMTRL.SAP_PART_NUMBER NOT IN (SELECT PART_NUMBER FROM SAQRSP (NOLOCK) WHERE QUOTE_RECORD_ID='{qt_rec_id}' AND QTEREV_RECORD_ID='{qt_rev_id}' AND SAQRSP.PAR_SERVICE_ID='{service_id}' AND (SAQRSP.INCLUDED='True' OR (SAQRSP.INCLUDED='False' AND SAQRSP.NEW_PART='False')) AND GREENBOOK='{treeParam}')""".format(sales=get_sales_org.SALESORG_ID,qt_rec_id=quote_rec_id,qt_rev_id=quote_rev_id,service_id=Service_Id,whrStr1=str(where_string_1) if where_string_1 else "",treeParam=TreeParam)
            elif active_subtab=='Exclusions':
                where_string+=""" MAMSOP.SALESORG_ID='{sales}' AND MAMTRL.PRODUCT_TYPE IS NULL AND NOT EXISTS (SELECT PART_NUMBER FROM SAQRSP (NOLOCK) WHERE QUOTE_RECORD_ID='{qt_rec_id}' AND QTEREV_RECORD_ID='{qt_rev_id}' AND MAMTRL.SAP_PART_NUMBER=SAQRSP.PART_NUMBER AND SAQRSP.PAR_SERVICE_ID='{service_id}' AND ((SAQRSP.NEW_PART='True' OR SAQRSP.INCLUDED='True') OR (SAQRSP.NEW_PART='False' AND SAQRSP.INCLUDED='False')) AND GREENBOOK='{treeParam}')""".format(sales=get_sales_org.SALESORG_ID,qt_rec_id=quote_rec_id,qt_rev_id=quote_rev_id,service_id=Service_Id,treeParam=TreeParam)
                paginationQuery="""SELECT COUNT(MAMTRL.CpqTableEntryId) as cnt FROM MAMTRL (NOLOCK) JOIN MAMSOP (NOLOCK) ON MAMSOP.SAP_PART_NUMBER=MAMTRL.SAP_PART_NUMBER WHERE {whrStr1} MAMSOP.SALESORG_ID='{sales}' AND MAMTRL.PRODUCT_TYPE IS NULL AND MAMTRL.SAP_PART_NUMBER NOT IN (SELECT PART_NUMBER FROM SAQRSP (NOLOCK) WHERE QUOTE_RECORD_ID='{qt_rec_id}' AND QTEREV_RECORD_ID='{qt_rev_id}' AND SAQRSP.PAR_SERVICE_ID='{service_id}' AND ((SAQRSP.NEW_PART='True' OR SAQRSP.INCLUDED='True') OR (SAQRSP.NEW_PART='False' AND SAQRSP.INCLUDED='False')) AND GREENBOOK='{treeParam}')""".format(sales=get_sales_org.SALESORG_ID,qt_rec_id=quote_rec_id,qt_rev_id=quote_rev_id,service_id=Service_Id,whrStr1=str(where_string_1) if where_string_1 else "",treeParam=TreeParam)
            else:
                iclusions_val=str(tuple(iclusions_val_list)).replace(',)',')')
                where_string+=""" MAMSOP.MATPRIGRP_ID in {iclusions_val} and MAMSOP.SALESORG_ID='{sales}' AND MAMTRL.PRODUCT_TYPE IS NULL AND NOT EXISTS (SELECT PART_NUMBER FROM SAQRSP (NOLOCK) WHERE QUOTE_RECORD_ID='{qt_rec_id}' AND QTEREV_RECORD_ID='{qt_rev_id}' AND MAMTRL.SAP_PART_NUMBER=SAQRSP.PART_NUMBER AND SAQRSP.NEW_PART='False' AND SAQRSP.INCLUDED='False')""".format(sales=get_sales_org.SALESORG_ID,qt_rec_id=quote_rec_id,qt_rev_id=quote_rev_id,iclusions_val=iclusions_val)
                paginationQuery="""SELECT COUNT({ObjName}.CpqTableEntryId) as cnt FROM {ObjName} (NOLOCK) WHERE {whrStr1}  MAMTRL.SAP_PART_NUMBER IN (SELECT SAP_PART_NUMBER FROM MAMSOP WHERE MAMSOP.MATPRIGRP_ID in {iclusions_val} and MAMSOP.SALESORG_ID='{sales}' ) AND MAMTRL.PRODUCT_TYPE IS NULL AND NOT EXISTS (SELECT PART_NUMBER FROM SAQRSP (NOLOCK) WHERE QUOTE_RECORD_ID='{qt_rec_id}' AND QTEREV_RECORD_ID='{qt_rev_id}' AND MAMTRL.SAP_PART_NUMBER=SAQRSP.PART_NUMBER AND SAQRSP.NEW_PART='False' AND SAQRSP.INCLUDED='False')""".format(sales=get_sales_org.SALESORG_ID,qt_rec_id=quote_rec_id,qt_rev_id=quote_rev_id,iclusions_val=iclusions_val,ObjName=ObjectName,whrStr1=str(where_string_1) if where_string_1 else "")
            QueryCountObj=Sql.GetFirst("{}".format(str(paginationQuery)))
        elif str(popup_obj)=="SAQSPT":
            where_string+=""" MAMSOP.SALESORG_ID='{sales}' AND MAMTRL.PRODUCT_TYPE IS NULL AND NOT EXISTS (SELECT PART_NUMBER FROM SAQSPT (NOLOCK) WHERE QUOTE_RECORD_ID='{qt_rec_id}' AND QTEREV_RECORD_ID='{qt_rev_id}' and MAMTRL.SAP_PART_NUMBER=SAQSPT.PART_NUMBER)""".format(sales=get_sales_org.SALESORG_ID,qt_rec_id=quote_rec_id,qt_rev_id=quote_rev_id)
            QueryCountObj=Sql.GetFirst("SELECT COUNT({}.CpqTableEntryId) as cnt FROM {} (NOLOCK) {} WHERE {} ".format( ObjectName,ObjectName,inner_join,str(where_string) if where_string else ""))
        table_data=Sql.GetList("select {} from {} (NOLOCK) {} {}  {} {}".format(",".join(ordered_keys_mam),ObjectName ,inner_join if inner_join else "","WHERE "+where_string if where_string else "" ,order_by,pagination_condition))
        operation_type="addParts"
        date_field = poputilObj.gettable_data(ObjectName,table_data,key="MATERIAL_RECORD_ID",value="|Parts",operation_type="addParts")
    pagination_total_count=0
    if QueryCountObj is not None:
        QryCount=QueryCountObj.cnt
        pagination_total_count=QryCount
    if offset_skip_count==0:
        offset_skip_count=1
        records_end=fetch_count
    else:
        offset_skip_count+=1
        records_end=offset_skip_count+fetch_count -1
    records_end=pagination_total_count if pagination_total_count < records_end else records_end
    records_start_and_end="{} - {} of ".format(offset_skip_count,records_end)
    if records_end==pagination_total_count:
        disable_next_and_last="class='btn-is-disabled' style=\'pointer-events:none\' "
    if offset_skip_count==0:
        disable_previous_and_first="class='btn-is-disabled' style=\'pointer-events:none\' "
    current_page=int(ceil(offset_skip_count / fetch_count))+1
    var_str+=poputilObj.constructing_table_footer(**{'records_start_and_end':records_start_and_end,'pagination_total_count':pagination_total_count,'fetch_count':fetch_count,'disable_previous_and_first':disable_previous_and_first,'disable_next_and_last':disable_next_and_last,'current_page':current_page,'TABLEID':TABLEID,'id_name':id_name,'operation_type': operation_type})
    filter_tags,filter_types,filter_values=poputilObj.filter_dropdown_header(ordered_keys=ordered_keys,obj_name=master_obj_name,id_name=id_name)
    filter_drop_down+=poputilObj.filter_dropdown_action(**{'id_name':id_name})
    dbl_clk_function+=poputilObj.dbl_clk_action(**{'id_names':id_names})
    if QryCount==0:
        pagedata=str(QryCount)+" - "+str(QryCount)+" of "
    elif QryCount < int(PerPage):
        pagedata=str(Page_start)+" - "+str(QryCount)+" of "
    else:
        pagedata=str(Page_start)+" - "+str(Page_End)+ " of "
    response_list_keys="[sec_str,new_value_dict,date_field,dbl_clk_function,filter_control_function,var_str,filter_tags,filter_types,filter_values,filter_drop_down,pagedata,QryCount]"
    response_list_vals=eval(response_list_keys)
    keys=response_list_keys.replace("[","").replace("]","").split(',')
    response = dict({res:response_list_vals[key] for key,res in enumerate(keys)})
    return response

Sql=Param.SQL_OBJ
poputilObj=Param.poputilObj
TreeParam=Product.GetGlobal("TreeParam")
TreeParentParam=Product.GetGlobal("TreeParentLevel0")
TreeSuperParentParam=Product.GetGlobal("TreeParentLevel1")
TreeTopSuperParentParam=Product.GetGlobal("TreeParentLevel2")
quote_rec_id=Quote.GetGlobal("contract_quote_record_id")
quote_rev_id=Quote.GetGlobal("quote_revision_record_id")
active_subtab=Param.active_subtab

A_Keys=Param.A_Keys
A_Values=Param.A_Values
RECORDID=Param.RECORD_ID
RECORDFEILD=Param.RECORDFEILD
TABLEID=Param.TABLEID
Result=service_addnew_popup(Param.PerPage,Param.PageInform,Param.SortColumn,Param.SortColumnOrder,Param.offset_skip_count,Param.FETCH_COUNT,TreeParam,Param.ObjectName)
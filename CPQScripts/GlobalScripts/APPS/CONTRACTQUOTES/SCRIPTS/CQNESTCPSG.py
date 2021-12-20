# =========================================================================================================================================
#   __script_name : CQNESTCPSG.PY
#   __script_description : THIS SCRIPT IS USED TO LOAD THE NESTED LIST GRID FOR THE QUOTE ITEMS SPARE PARTS LISTING AND PRICING.
#   __primary_author__ : SURIYANARAYANAN
#   __create_date :09/29/2021
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import Webcom
from SYDATABASE import SQL
from datetime import datetime
import Webcom.Configurator.Scripting.Test.TestProduct
import time
Sql = SQL()
import CQCPSPRICE as CPS
import SYCNGEGUID as CPQID
import System.Net
    
def getsparepartslist(PerPage, PageInform, A_Keys, A_Values):
    if str(PerPage) == "" and str(PageInform) == "":
        Page_start = 1
        Page_End = 10
        PerPage = 10
        PageInform = "1___10___10"
    else:
        Page_start = int(PageInform.split("___")[0])
        Page_End = int(PageInform.split("___")[1])
        PerPage = PerPage
    ContractRecordId = Quote.GetGlobal("contract_quote_record_id")
    RevisionRecordId = Quote.GetGlobal("quote_revision_record_id")
    data_list = []
    rec_id = "SYOBJR-00010"
    obj_id = "SYOBJR-00010"
    objh_getid = Sql.GetFirst(
        "SELECT TOP 1  RECORD_ID  FROM SYOBJH (NOLOCK) WHERE SAPCPQ_ATTRIBUTE_NAME='" + str(obj_id) + "'"
    )
    if objh_getid:
        obj_id = objh_getid.RECORD_ID
    objs_obj = Sql.GetFirst(
        "select CAN_ADD,CAN_EDIT,COLUMNS,CAN_DELETE from SYOBJR (NOLOCK) where OBJ_REC_ID = '" + str(obj_id) + "' "
    )
    """
    can_edit = str(objs_obj.CAN_EDIT)
    can_add = str(objs_obj.CAN_ADD)
    can_delete = str(objs_obj.CAN_DELETE)
    """
    table_id = "table_spareparts_parent"
    table_header = (
        '<table id="'
        + str(table_id)
        + '"  data-pagination="false" data-sortable="true" data-search-on-enter-key="true" data-filter-control="true" data-pagination-loop = "false" data-locale = "en-US" ><thead>'
    )
    Columns = [
        "PRICING_STATUS",
        "QUOTE_ITEM_FORECAST_PART_RECORD_ID",
        "SERVICE_ID",
        "PART_LINE_ID",
        "PART_NUMBER",
        "PART_DESCRIPTION",
        "MATPRIGRP_ID",
        "BASEUOM_ID",
        "UNIT_PRICE",
        "ANNUAL_QUANTITY",
        "SRVTAXCLA_DESCRIPTION",
        "TAX_PERCENTAGE",
        "TAX",
        "EXTENDED_PRICE"
    ]
    Objd_Obj = Sql.GetList(
        "select FIELD_LABEL,API_NAME,LOOKUP_OBJECT,LOOKUP_API_NAME,DATA_TYPE from SYOBJD (NOLOCK) where OBJECT_NAME = 'SAQIFP'"
    )
    attr_list = []
    attrs_datatype_dict = {}
    lookup_disply_list = []
    lookup_str = ""
    if Objd_Obj is not None:
        attr_list = {}
        for attr in Objd_Obj:
            attr_list[str(attr.API_NAME)] = str(attr.FIELD_LABEL)
            attrs_datatype_dict[str(attr.API_NAME)] = str(attr.DATA_TYPE)
            if attr.LOOKUP_API_NAME != "" and attr.LOOKUP_API_NAME is not None:
                lookup_disply_list.append(str(attr.API_NAME))
        checkbox_list = [inn.API_NAME for inn in Objd_Obj if inn.DATA_TYPE == "CHECKBOX"]
        lookup_list = {ins.LOOKUP_API_NAME: ins.API_NAME for ins in Objd_Obj}
        
    lookup_str = ",".join(list(lookup_disply_list))
    orderby = "QUOTE_ITEM_FORECAST_PART_RECORD_ID"
    where_string = ""
    if A_Keys != "" and A_Values != "":
        A_Keys = list(A_Keys)
        A_Values = list(A_Values)
        for key, value in zip(A_Keys, A_Values):
            if value.strip():
                if where_string:
                    where_string += " AND "
                where_string += "{Key} LIKE '%{Value}%'".format(Key=key, Value=value)
    if str(where_string)!="":
        where_string = " AND "+str(where_string)
    Qstr = (
        "SELECT DISTINCT TOP "
        + str(PerPage)
        + " QUOTE_ITEM_FORECAST_PART_RECORD_ID, PRICING_STATUS,SERVICE_ID,PART_NUMBER,MATPRIGRP_ID,PART_DESCRIPTION,BASEUOM_ID,SCHEDULE_MODE,DELIVERY_MODE,UNIT_PRICE,EXTENDED_PRICE,ANNUAL_QUANTITY,CUSTOMER_PART_NUMBER_RECORD_ID,BASEUOM_RECORD_ID,MATPRIGRP_RECORD_ID,QTEITM_RECORD_ID,QUOTE_RECORD_ID,QTEREV_RECORD_ID,SALESORG_RECORD_ID,SERVICE_RECORD_ID,PART_RECORD_ID,SALESUOM_RECORD_ID,CpqTableEntryId,TAX,SRVTAXCLA_DESCRIPTION,TAX_PERCENTAGE from ( select TOP "+ str(PerPage)+" ROW_NUMBER() OVER(order by "+ str(orderby) +") AS ROW, * from SAQIFP (nolock)  where QUOTE_RECORD_ID ='"+str(ContractRecordId)
        +"' AND QTEREV_RECORD_ID = '"
        +str(RevisionRecordId)
        +"') m where m.ROW BETWEEN "
        + str(Page_start)
        + " AND "
        + str(Page_End)+" ORDER BY PRICING_STATUS ASC"
    )
    QueryCount = ""
    QueryCountObj = Sql.GetFirst(
        "select count(CpqTableEntryId) as cnt from SAQIFP (NOLOCK) where QUOTE_RECORD_ID = '"
        + str(ContractRecordId)
        + "' and QTEREV_RECORD_ID = '"
        + str(RevisionRecordId)
        + "' "+str(where_string)
    )
    
    if QueryCountObj is not None:
        QueryCount = QueryCountObj.cnt
 
    parent_obj = Sql.GetList(Qstr)
    for par in parent_obj:
        data_id = str(par.QUOTE_ITEM_FORECAST_PART_RECORD_ID)        
        Action_str = (
            '<div class="btn-group dropdown"><div class="dropdown" id="ctr_drop"><i data-toggle="dropdown" id="dropdownMenuButton" class="fa fa-sort-desc dropdown-toggle" aria-expanded="false"></i><ul class="dropdown-menu left" aria-labelledby="dropdownMenuButton"><li><a class="dropdown-item cur_sty" href="#" id="'
            + str(data_id)
            + '" onclick="Commonteree_view_RL(this)">VIEW</a></li>'
            '<li><a class="dropdown-item" id="deletebtn" data-target="#cont_CommonModalDelete" data-toggle="modal" onclick="CommonDelete(this, \'SAQIFP#'+ data_id +'\', \'WARNING\')" href="#">DELETE</a></li>'
        )
        """        
        if can_edit.upper() == "TRUE":
            Action_str += (
                '<li style="display:none" ><a class="dropdown-item cur_sty" href="#" id="'
                + str(data_id)
                + '" onclick="Move_to_parent_obj_edit(this)">EDIT</a></li>'
            )
        if can_delete.upper() == "TRUE":
            Action_str += '<li><a class="dropdown-item" data-target="#cont_viewModal_Material_Delete" data-toggle="modal" onclick="Material_delete_obj(this)" href="#">DELETE</a></li>'
        Action_str += "</ul></div></div>"
        """
        # Data formation in dictonary format.
        ## hyperlink
        data_dict = {}
        data_dict["ids"] = str(data_id)
        data_dict["ACTIONS"] = str(Action_str)
        data_dict["QUOTE_ITEM_FORECAST_PART_RECORD_ID"] = CPQID.KeyCPQId.GetCPQId(
            "SAQIFP", str(par.QUOTE_ITEM_FORECAST_PART_RECORD_ID)
        )
        if par.PRICING_STATUS == 'ACQUIRED':
            imgstr = '<img title="Acquired" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Green_Tick.svg>'
            data_dict["PRICING_STATUS"] = ('<abbr id ="" title="' + str(par.PRICING_STATUS) + '">' + str(imgstr) +  "</abbr>") 
        else:
            acquiring_img_str = '<img title="Acquiring" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Cloud_Icon.svg>'
            data_dict["PRICING_STATUS"] = ('<abbr id ="" title="' + str(par.PRICING_STATUS) + '">' + str(acquiring_img_str) +  "</abbr>")
            
        data_dict["SERVICE_ID"] = ('<abbr id ="" title="' + str(par.SERVICE_ID) + '">' + str(par.SERVICE_ID) + "</abbr>")
        #data_dict["PART_LINE_ID"] = ('<abbr id ="" title="' + str(par.PART_LINE_ID) + '">' + str(par.PART_LINE_ID) + "</abbr>")
        data_dict["PART_NUMBER"] = ('<abbr id ="" title="' + str(par.PART_NUMBER) + '">' + str(par.PART_NUMBER) + "</abbr>")
        data_dict["PART_DESCRIPTION"] = ('<abbr id ="" title="' + str(par.PART_DESCRIPTION) + '">' + str(par.PART_DESCRIPTION) + "</abbr>")
        data_dict["MATPRIGRP_ID"] = ('<abbr id ="" title="' + str(par.MATPRIGRP_ID) + '">' + str(par.MATPRIGRP_ID) + "</abbr>")
        data_dict["BASEUOM_ID"] = ('<abbr id ="" title="' + str(par.BASEUOM_ID) + '">' + str(par.BASEUOM_ID) + "</abbr>")
        data_dict["UNIT_PRICE"] = ('<abbr id ="" title="' + str(par.UNIT_PRICE) + '">' + str(par.UNIT_PRICE) + "</abbr>")
        data_dict["ANNUAL_QUANTITY"] = ('<abbr id ="" title="' + str(par.ANNUAL_QUANTITY) + '">' + str(par.ANNUAL_QUANTITY) + "</abbr>")
        data_dict["SRVTAXCLA_DESCRIPTION"] = ('<abbr id ="" title="' + str(par.SRVTAXCLA_DESCRIPTION) + '">' + str(par.SRVTAXCLA_DESCRIPTION) + "</abbr>")
        data_dict["TAX_PERCENTAGE"] = ('<abbr id ="" title="' + str(par.TAX_PERCENTAGE) + '">' + str(par.TAX_PERCENTAGE) + "</abbr>")
        data_dict["TAX"] = ('<abbr id ="" title="' + str(par.TAX) + '">' + str(par.TAX) + "</abbr>")
        data_dict["EXTENDED_PRICE"] = ('<abbr id ="" title="' + str(par.EXTENDED_PRICE) + '">' + str(par.EXTENDED_PRICE) + "</abbr>")
        data_list.append(data_dict)
    hyper_link = ["PART_NUMBER"]
    table_header += "<tr>"
    table_header += (
        '<th data-field="ACTIONS"><div class="action_col">ACTIONS</div><button class="searched_button" id="Act_'
        + str(table_id)
        + '">Search</button></th>'
    )
    table_header += '<th data-field="SELECT" class="wid45" data-checkbox="true"></th>'
    for key, invs in enumerate(list(Columns)):
        invs = str(invs).strip()
        qstring = attr_list.get(str(invs)) or ""
        if qstring == "":
            qstring = invs.replace("_", " ")
        if checkbox_list is not None and invs in checkbox_list:
            table_header += (
                '<th  data-field="'
                + str(invs)
                + '" data-filter-control="input" data-align="center" data-formatter="CheckboxFieldRelatedList" data-sortable="true"><abbr title="'
                + str(qstring)
                + '">'
                + str(qstring)
                + "</abbr></th>"
            )
        elif hyper_link is not None and invs in hyper_link:            
            table_header += (
                '<th data-field="'
                + str(invs)
                + '" data-filter-control="input" data-title-tooltip="'+str(qstring)+'" data-formatter="SparePartsLineItemHyperLink" data-sortable="true"'+ str(qstring)+'"><abbr title="'
                + str(qstring)
                + '">'
                + str(qstring)
                + "</abbr></th>"
            )
        else:            
            table_header += (
                '<th  data-field="'
                + str(invs)
                + '" data-filter-control="input"  data-title-tooltip="'+str(qstring)+'" data-sortable="true"><abbr title="'
                + str(qstring)
                + '">'
                + str(qstring)
                + "</abbr></th>"
            )

    table_header += "</tr>"
    table_header += '</thead><tbody onclick="Table_Onclick_Scroll(this)"></tbody></table>'
    table_ids = "#" + str(table_id)
    filter_control_function = ""
    tbl_id = table_id
    values_list = ""
    for key, invs in enumerate(list(Columns)):
        table_ids = "#" + str(table_id)
        filter_clas = "#" + str(table_id) + " .bootstrap-table-filter-control-" + str(invs)
        values_list += "var " + str(invs) + ' = $("' + str(filter_clas) + '").val(); '
        values_list += "ATTRIBUTE_VALUEList.push(" + str(invs) + "); "
    filter_class = "#Act_" + str(table_id)
    filter_control_function += (
    '$("'
    + filter_class
    + '").click( function(){ var table_id = $(this).closest("table").attr("id"); ATTRIBUTE_VALUEList = []; '
    + str(values_list)
    + ' var attribute_value = $(this).val(); cpq.server.executeScript("CQNESTCPSG", {"TABNAME":"Spare Parts Parent", "ACTION":"PRODUCT_ONLOAD_FILTER", "ATTRIBUTE_NAME": '
    + str(list(Columns))
    + ', "ATTRIBUTE_VALUE": ATTRIBUTE_VALUEList }, function(dataset) {debugger; data2 = dataset[1];  data1 = dataset[0]; data3 = dataset[2]; console.log("len ---->"+data1.length);  try { if(data1.length > 0) { $("#'
    + str(tbl_id)
    + '").bootstrapTable("load", data1 );$("#noRecDisp").remove(); if (document.getElementById("'+str(tbl_id) + '___totalItemCount")){document.getElementById("'+str(tbl_id)+ '___totalItemCount").innerHTML = data2;}  if (document.getElementById("'+str(tbl_id) + '___NumberofItem")) { console.log("if_chk_j"); document.getElementById("'+str(tbl_id)+ '___NumberofItem").innerHTML = data3;}} else{ console.log("else_chk_j"); $("#' + str(tbl_id) + '").bootstrapTable("load", data1  );$("#' + str(tbl_id) + '").after("<div id=\'noRecDisp\' class=\'noRecord\'>No Records to Display</div>"); if (document.getElementById("'+str(tbl_id) + '___totalItemCount")){document.getElementById("'+str(tbl_id)+ '___totalItemCount").innerHTML = data2;}  if (document.getElementById("'+str(tbl_id) + '___NumberofItem")) {document.getElementById("'+str(tbl_id)+ '___NumberofItem").innerHTML = data3;} }} catch(err){} }); filter_search_click();$(".JColResizer").mousedown(function(){ $("thead.fullHeadFirst").css("cssText","z-index: 2;border-top: 1px solid rgb(220, 220, 220);top: 154px;border-right: 0px !important;");$("thead.fullHeadSecond").css("display","none"); });$(".JColResizer").mouseup(function(){ var th_width_resize = [];$("#table_spareparts_parent thead.fullHeadFirst tr th").each(function(index){var wid = $(this).css("width"); if(index ==0 || index ==1){th_width_resize.push("60px");}else{th_width_resize.push(wid);}}); $("thead.fullHeadFirst").css("cssText","position: fixed;z-index: 2;border-top: 1px solid rgb(220, 220, 220); top: 154px;border-right: 0px !important;");$("thead.fullHeadSecond").css("display","table-header-group");$("#table_spareparts_parent thead.fullHeadFirst tr th").each(function(index){var num = th_width_resize[index].split("px");var numsp = parseInt(num[0]);numsp = numsp - 1;var make_str =numsp+"px"; var c = "width:"+make_str+";white-space: nowrap;overflow: hidden;text-overflow: ellipsis;";var d = "width:"+make_str+";"; $(this).css("cssText",c);$(this).children("div:first-child").css("cssText",c);$(this).children("div.fht-cell").css("cssText",d);});$("#table_spareparts_parent thead.fullHeadSecond tr th").each(function(index){var num = th_width_resize[index].split("px");var numsp = parseInt(num[0]);numsp = numsp - 1;var make_str =numsp+"px"; var c = "width:"+make_str+";white-space: nowrap;overflow: hidden;text-overflow: ellipsis;";var d = "width:"+make_str+";"; $(this).css("cssText",c);$(this).children("div:first-child").css("cssText",c);$(this).children("div.fht-cell").css("cssText",d);}); });});')
    
    #Trace.Write("666 filter_control_function ---->"+str(filter_control_function))

    dbl_clk_function = (
        '$("'
        + str(table_ids)
        + '").on("all.bs.table", function (e, name, args) { $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); }); $("'
        + str(table_ids)
        + '\ th.bs-checkbox div.th-inner").before("<div style=\'padding:0; border-bottom: 1px solid #dcdcdc;\'>SELECT</div>"); $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); $("'
        + str(table_ids)
        + "\").on('sort.bs.table', function (e, name, order) {  console.log('Parent sort.bs.table ====> ', e); currenttab = $(\"ul#carttabs_head .active\").text().trim(); localStorage.setItem('"
        + str(table_id)
        + "_SortColumn', name); localStorage.setItem('"
        + str(table_id)
        + "_SortColumnOrder', order); NestedContainerSorting(name, order, '"
        + str(table_id)
        + "'); }); "
        )
    NORECORDS = ""
    if len(data_list) == 0:
        NORECORDS = "NORECORDS"

    ObjectName = "SAQIFP"
    DropDownList = []
    filter_level_list = []
    filter_clas_name = ""
    cv_list = []
    TableclassName = "form-control" + table_id
    for key, col_name in enumerate(list(Columns)):
        StringValue_list = []
        objss_obj = Sql.GetFirst(
            "SELECT API_NAME, DATA_TYPE, FORMULA_LOGIC, PICKLIST FROM SYOBJD (NOLOCK) WHERE OBJECT_NAME='"
            + str(ObjectName)
            + "' and API_NAME = '"
            + str(col_name)
            + "'"
        )
        try:
            FORMULA_LOGIC = objss_obj.FORMULA_LOGIC.strip()
            FORMULA_col = FORMULA_LOGIC.split(" ")[1].strip()
            FORMULA_table = FORMULA_LOGIC.split(" ")[3].strip()
            ins_obj = Sql.GetFirst(
                "SELECT API_NAME, DATA_TYPE,PICKLIST FROM SYOBJD (NOLOCK) WHERE OBJECT_NAME='"
                + str(FORMULA_table)
                + "' and API_NAME = '"
                + str(FORMULA_col)
                + "'"
            )
            if str(objss_obj.PICKLIST).upper() == "TRUE":
                filter_level_data = "select"
                filter_clas_name = (
                    '<div id = "'
                    + str(table_id)
                    + "_RelatedMutipleCheckBoxDrop_"
                    + str(key)
                    + '" class="form-control bootstrap-table-filter-control-'
                    + str(col_name)
                    + " RelatedMutipleCheckBoxDrop_"
                    + str(key)
                    + ' "></div>'
                )
                filter_level_list.append(filter_level_data)
            else:
                filter_level_data = "input"
                filter_clas_name = (
                    '<input type="text" class="width100_vis form-control bootstrap-table-filter-control-'
                    + str(col_name)
                    + '">'
                )
                filter_level_list.append(filter_level_data)
        except:
            Trace.Write("except---->")
            if str(objss_obj.PICKLIST).upper() == "TRUE":
                filter_level_data = "select"
                filter_clas_name = (
                    '<div id = "'
                    + str(table_id)
                    + "_RelatedMutipleCheckBoxDrop_"
                    + str(key)
                    + '" class="form-control bootstrap-table-filter-control-'
                    + str(col_name)
                    + " RelatedMutipleCheckBoxDrop_"
                    + str(key)
                    + ' "></div>'
                )
                filter_level_list.append(filter_level_data)

            filter_level_data = "input"
            filter_clas_name = (
                '<input type="text" class="width100_vis form-control bootstrap-table-filter-control-' + str(col_name) + '">'
            )
            filter_level_list.append(filter_level_data)
        cv_list.append(filter_clas_name)
        if filter_level_data == "select":
            try:
                xcd = Sql.GetFirst(
                    "SELECT (STUFF((SELECT DISTINCT ', ' + CAST("
                    + str(col_name)
                    + " AS CHAR(100)) FROM "
                    + str(ObjectName)
                    + " FOR XML PATH('') ), 1, 2, '')  ) AS StringValue"
                )
            except:
                xcd = Sql.GetFirst(
                    "SELECT (STUFF((SELECT DISTINCT ', ' + CAST("
                    + str(col_name)
                    + " AS CHAR(100)) FROM "
                    + str(ObjectName)
                    + " FOR XML PATH('') ), 1, 2, '')  ) AS StringValue"
                )
            if str(xcd.StringValue) is not None and str(xcd.StringValue) != "":
                if str(xcd.StringValue).find(",") != -1:
                    StringValue_list = [ins.strip() for ins in str(xcd.StringValue).split(",") if ins.strip() != ""]
                else:
                    StringValue_list.append(str(xcd.StringValue))
            else:
                StringValue_list = [""]
            StringValue_list = list(set(StringValue_list))
            DropDownList.append(StringValue_list)
        elif filter_level_data == "checkbox":
            DropDownList.append(["True", "False"])
        else:
            DropDownList.append("")
    RelatedDrop_str = (
        "try { if( document.getElementById('"
        + str(table_id)
        + "') ) { var listws = document.getElementById('"
        + str(table_id)
        + "').getElementsByClassName('filter-control');  for (i = 0; i < listws.length; i++) { document.getElementById('"
        + str(table_id)
        + "').getElementsByClassName('filter-control')[i].innerHTML = data6[i];  } for (j = 0; j < listws.length; j++) { if (data7[j] == 'select') { if (data8[j]) { var dataAdapter = new $.jqx.dataAdapter(data8[j]); $('#"
        + str(table_id)
        + "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter, autoDropDownHeight: true }); } } } } }  catch(err) { setTimeout(function() { var listws = document.getElementById('"
        + str(table_id)
        + "').getElementsByClassName('filter-control');  for (i = 0; i < listws.length; i++) { document.getElementById('"
        + str(table_id)
        + "').getElementsByClassName('filter-control')[i].innerHTML = data6[i];  } for (j = 0; j < listws.length; j++) { if (data7[j] == 'select') { if (data8[j]) { var dataAdapter = new $.jqx.dataAdapter(data8[j]); $('#"
        + str(table_id)
        + "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter, autoDropDownHeight: true }); } } } }, 5000); }"
    )
    page = ""
    if QueryCount < int(PerPage):
        page = str(Page_start) + " - " + str(QueryCount)
    else:
        page = str(Page_start) + " - " + str(Page_End)
    #Trace.Write("page----->"+str(page))    
    Test = (
        '<div class="col-md-12 brdr listContStyle pad2height30" ><div class="col-md-4 pager-numberofitem clear-padding"><span class="pager-number-of-items-item noofitem" id="'
        + str(table_id)
        + '___NumberofItem" >'
        + str(page)
        + ' of</span><span class="pager-number-of-items-item fltltpad2mrg0" id="'
        + str(table_id)
        + '___totalItemCount" >'
        + str(QueryCount)
        + '</span><div class="clear-padding fltltmrgtp3" ><div  class="pull-right vertmidtxtrht"><select onchange="PageFunctestChild(this,\'Quote\',\'\',\'table_spareparts_parent\')" id="'
        + str(table_id)
        + '___PageCountValue" class="form-control wid65vermiddisinbmarl5"><option value="10" selected>10</option><option value="20">20</option><option value="50">50</option><option value="100">100</option><option value="200">200</option></select> </div></div></div><div class="col-xs-8 col-md-4  clear-padding disinpad10txtcen"  data-bind="visible: totalItemCount"><div class="clear-padding col-xs-12 col-sm-6 col-md-12 bor0" ><ul class="pagination pagination"><li class="disabled"><a href="#" onclick="FirstPageLoad_paginationChild(\'Quote\',\'\',\'table_spareparts_parent\')"><i class="fa fa-caret-left font14whtbld" ></i><i class="fa fa-caret-left font14" ></i></a></li><li class="disabled"><a href="#" onclick="Previous12334Child(\'Quote\',\'\',\'table_spareparts_parent\')"><i class="fa fa-caret-left font14" ></i>PREVIOUS</a></li><li class="disabled"><a href="#" class="disabledPage" onclick="Next12334Child(\'Quote\',\'\',\'table_spareparts_parent\')">NEXT<i class="fa fa-caret-right font14" ></i></a></li><li class="disabled"><a href="#" onclick="LastPageLoad_paginationChild(\'Quote\',\'\',\'table_spareparts_parent\')" class="disabledPage"><i class="fa fa-caret-right font14"></i><i class="fa fa-caret-right font14whtbld"></i></a></li></ul></div> </div> <div class="col-md-4 pr_page_pad"> <span id="'
        + str(table_id)
        + '___page_count" class="currentPage page_right_content">1</span><span class="page_right_content pad_rt_2">Page </span></div></div>'
    )
    if QueryCount < int(PerPage):
        PerPage = str(QueryCount)
    else:
        PerPage = str(PerPage)   
    if Page_End > QueryCount:
        Page_End = QueryCount
    else:
        Page_End = Page_End
    Action_Str = ""
    Action_Str += str(Page_start)+" - "
    Action_Str += str(Page_End)
    Action_Str += " of"
    return (
        table_header,
        data_list,
        table_id,
        filter_control_function,
        NORECORDS,
        dbl_clk_function,
        cv_list,
        filter_level_list,
        DropDownList,
        RelatedDrop_str,
        Test,
        Action_Str,
        QueryCount,
        page
    )

def getsparepartssublist(PerPage, PageInform, A_Keys, A_Values):
    if str(PerPage) == "" and str(PageInform) == "":
        Page_start = 1
        Page_End = 10
        PerPage = 10
        PageInform = "1___10___10"
    else:
        Page_start = int(PageInform.split("___")[0])
        Page_End = int(PageInform.split("___")[1])
        PerPage = PerPage
    ContractRecordId = Quote.GetGlobal("contract_quote_record_id")
    RevisionRecordId = Quote.GetGlobal("quote_revision_record_id")
    data_list = []
    rec_id = "SYOBJR-00010"
    obj_id = "SYOBJR-00010"
    table_id = "table_spareparts_child"
    table_header = (
        '<table id="'
        + str(table_id)
        + '"  data-pagination="false" data-sortable="true" data-search-on-enter-key="true" data-filter-control="true" data-pagination-loop = "false" data-locale = "en-US" ><thead>'
    )
    Columns = [
        "STEP_NO",
        #"QUOTE_ITEM_CONDITION_TYPE_RECORD_ID",
        "CONDITION_COUNTER",
        "CONDITION_TYPE",
        "CONDITION_TYPE_DESCRIPTION",
        "PURPOSE",
        "CONDITION_BASE",
        "CONDITION_RATE",
        "CONDITION_VALUE",
        "CONDITION_CURRENCY",
        "CONDITION_UNIT_VALUE",
        "CONDITION_UNIT",
        "STATISTICAL",
        "CALCULATION_TYPE",
        "VAR_COND",
        "VAR_COND_KEY",
        "VAR_COND_FACTOR",
        "DURATION_FACTOR",
        "INACTIVE_FLAG"
    ]
    response = CPS.fetch_cps_response()
    Trace.Write(response)
    response = str(response).replace(": true", ': "true"').replace(": false", ': "false"').replace(": null",': " None"')
    response = eval(response)
    Trace.Write(response)
    price = []
    for key, value in response.items():
        if key == "items":
            price = value[:]
            break
    #QueryCount = price[0]['conditions'].len()
    QueryCount = 20
    for par in price[0]['conditions']:
        data_id = '803B32A3-F417-4F6A-BC67-5D194D89'
        Action_str = (
            '<div class="btn-group dropdown"><div class="dropdown" id="ctr_drop"><i data-toggle="dropdown" id="dropdownMenuButton" class="fa fa-sort-desc dropdown-toggle" aria-expanded="false"></i><ul class="dropdown-menu left" aria-labelledby="dropdownMenuButton"><li><a class="dropdown-item cur_sty" href="#" id="'
            + str(data_id)
            + '" onclick="Commonteree_view_RL(this)">VIEW</a></li>'
            '<li><a class="dropdown-item" id="deletebtn" data-target="#cont_CommonModalDelete" data-toggle="modal" onclick="CommonDelete(this, \'SAQICD#'+ data_id +'\', \'WARNING\')" href="#">DELETE</a></li>'
        )
        # Data formation in dictonary format.
        ## hyperlink
        data_dict = {}
        data_dict["ids"] = str(data_id)
        data_dict["ACTIONS"] = str(Action_str)
        data_dict["QUOTE_ITEM_CONDITION_TYPE_RECORD_ID"] = CPQID.KeyCPQId.GetCPQId(
            "SAQICD", str(data_id)
        )
        data_dict["STEP_NO"] = ('<abbr id ="" title="' + str(par['stepNo']) + '">' + str(par['stepNo']) +  "</abbr>")
        data_dict["CONDITION_COUNTER"] = ('<abbr id ="" title="' + str(par['conditionCounter']) + '">' + str(par['conditionCounter']) +  "</abbr>")
        data_dict["CONDITION_TYPE"] = ('<abbr id ="" title="' + str(par['conditionType']) + '">' + str(par['conditionType']) + "</abbr>")
        data_dict["CONDITION_TYPE_DESCRIPTION"] = ('<abbr id ="" title="' + str(par['conditionTypeDescription']) + '">' + str(par['conditionTypeDescription']) + "</abbr>")
        data_dict["PURPOSE"] = ('<abbr id ="" title="' + str(par['purpose']) + '">' + str(par['purpose']) + "</abbr>")
        data_dict["CONDITION_BASE"] = ('<abbr id ="" title="' + str(par['conditionBase']) + '">' + str(par['conditionBase']) + "</abbr>")
        data_dict["CONDITION_RATE"] = ('<abbr id ="" title="' + str(par['conditionRate']) + '">' + str(par['conditionRate']) + "</abbr>")
        data_dict["CONDITION_VALUE"] = ('<abbr id ="" title="' + str(par['conditionValue']) + '">' + str(par['conditionValue']) + "</abbr>")
        data_dict["CONDITION_CURRENCY"] = ('<abbr id ="" title="' + str(par['conditionCurrency']) + '">' + str(par['conditionCurrency']) + "</abbr>")
        data_dict["CONDITION_UNIT_VALUE"] = ('<abbr id ="" title="' + str(par['conditionUnitValue']) + '">' + str(par['conditionUnitValue']) + "</abbr>")
        data_dict["CONDITION_UNIT"] = ('<abbr id ="" title="' + str(par['conditionUnit']) + '">' + str(par['conditionUnit']) + "</abbr>")
        data_dict["STATISTICAL"] = ('<abbr id ="" title="' + str(par['statistical']) + '">' + str(par['statistical']) + "</abbr>")
        data_dict["CALCULATION_TYPE"] = ('<abbr id ="" title="' + str(par['calculationType']) + '">' + str(par['calculationType']) + "</abbr>")
        data_dict["VAR_COND"] = ('<abbr id ="" title="' + str(par['varcond']) + '">' + str(par['varcond']) + "</abbr>")
        data_dict["VAR_COND_KEY"] = ('<abbr id ="" title="' + str(par['varcondKey']) + '">' + str(par['varcondKey']) + "</abbr>")
        data_dict["VAR_COND_FACTOR"] = ('<abbr id ="" title="' + str(par['varcondFactor']) + '">' + str(par['varcondFactor']) + "</abbr>")
        data_dict["DURATION_FACTOR"] = ('<abbr id ="" title="' + str(par['durationFactor']) + '">' + str(par['durationFactor']) + "</abbr>")
        data_dict["INACTIVE_FLAG"] = ('<abbr id ="" title="' + str(par['inactiveFlag']) + '">' + str(par['inactiveFlag']) + "</abbr>")
        data_list.append(data_dict)
    hyper_link = ["QUOTE_ITEM_CONDITION_TYPE_RECORD_ID"]
    table_header += "<tr>"
    table_header += (
        '<th data-field="ACTIONS"><div class="action_col">ACTIONS</div><button class="searched_button" id="Act_'
        + str(table_id)
        + '">Search</button></th>'
    )
    table_header += '<th data-field="SELECT" class="wid45" data-checkbox="true"></th>'
    for key, invs in enumerate(list(Columns)):
        invs = str(invs).strip()
        #qstring = attr_list.get(str(invs)) or ""
        qstring = ''
        if qstring == "":
            qstring = invs.replace("_", " ")
        #if checkbox_list is not None and invs in checkbox_list:
        #    table_header += (
        #        '<th  data-field="'
        #        + str(invs)
        #        + '" data-filter-control="input" data-align="center" data-formatter="CheckboxFieldRelatedList" data-sortable="true"><abbr title="'
        #        + str(qstring)
        #        + '">'
        #        + str(qstring)
        #        + "</abbr></th>"
        #    )
        if hyper_link is not None and invs in hyper_link:            
            table_header += (
                '<th data-field="'
                + str(invs)
                + '" data-filter-control="input" data-title-tooltip="'+str(qstring)+'" data-formatter="SparePartsLineItemHyperLink" data-sortable="true"'+ str(qstring)+'"><abbr title="'
                + str(qstring)
                + '">'
                + str(qstring)
                + "</abbr></th>"
            )
        else:            
            table_header += (
                '<th  data-field="'
                + str(invs)
                + '" data-filter-control="input"  data-title-tooltip="'+str(qstring)+'" data-sortable="true"><abbr title="'
                + str(qstring)
                + '">'
                + str(qstring)
                + "</abbr></th>"
            )

    table_header += "</tr>"
    table_header += '</thead><tbody onclick="Table_Onclick_Scroll(this)"></tbody></table>'
    table_ids = "#" + str(table_id)
    filter_control_function = ""
    tbl_id = table_id
    values_list = ""
    for key, invs in enumerate(list(Columns)):
        table_ids = "#" + str(table_id)
        filter_clas = "#" + str(table_id) + " .bootstrap-table-filter-control-" + str(invs)
        values_list += "var " + str(invs) + ' = $("' + str(filter_clas) + '").val(); '
        values_list += "ATTRIBUTE_VALUEList.push(" + str(invs) + "); "
    filter_class = "#Act_" + str(table_id)
    filter_control_function += (
    '$("'
    + filter_class
    + '").click( function(){ var table_id = $(this).closest("table").attr("id"); ATTRIBUTE_VALUEList = []; '
    + str(values_list)
    + ' var attribute_value = $(this).val(); cpq.server.executeScript("CQNESTCPSG", {"TABNAME":"Spare Parts Child", "ACTION":"PRODUCT_ONLOAD_FILTER", "ATTRIBUTE_NAME": '
    + str(list(Columns))
    + ', "ATTRIBUTE_VALUE": ATTRIBUTE_VALUEList }, function(dataset) {debugger; data2 = dataset[1];  data1 = dataset[0]; data3 = dataset[2]; console.log("len ---->"+data1.length);  try { if(data1.length > 0) { $("#'
    + str(tbl_id)
    + '").bootstrapTable("load", data1 );$("#noRecDisp").remove(); if (document.getElementById("'+str(tbl_id) + '___totalItemCount")){document.getElementById("'+str(tbl_id)+ '___totalItemCount").innerHTML = data2;}  if (document.getElementById("'+str(tbl_id) + '___NumberofItem")) { console.log("if_chk_j"); document.getElementById("'+str(tbl_id)+ '___NumberofItem").innerHTML = data3;}} else{ console.log("else_chk_j"); $("#' + str(tbl_id) + '").bootstrapTable("load", data1  );$("#' + str(tbl_id) + '").after("<div id=\'noRecDisp\' class=\'noRecord\'>No Records to Display</div>"); if (document.getElementById("'+str(tbl_id) + '___totalItemCount")){document.getElementById("'+str(tbl_id)+ '___totalItemCount").innerHTML = data2;}  if (document.getElementById("'+str(tbl_id) + '___NumberofItem")) {document.getElementById("'+str(tbl_id)+ '___NumberofItem").innerHTML = data3;} }} catch(err){} }); filter_search_click();$(".JColResizer").mousedown(function(){ $("thead.fullHeadFirst").css("cssText","z-index: 2;border-top: 1px solid rgb(220, 220, 220);top: 154px;border-right: 0px !important;");$("thead.fullHeadSecond").css("display","none"); });$(".JColResizer").mouseup(function(){ var th_width_resize = [];$("#table_spareparts_parent thead.fullHeadFirst tr th").each(function(index){var wid = $(this).css("width"); if(index ==0 || index ==1){th_width_resize.push("60px");}else{th_width_resize.push(wid);}}); $("thead.fullHeadFirst").css("cssText","position: fixed;z-index: 2;border-top: 1px solid rgb(220, 220, 220); top: 154px;border-right: 0px !important;");$("thead.fullHeadSecond").css("display","table-header-group");$("#table_spareparts_parent thead.fullHeadFirst tr th").each(function(index){var num = th_width_resize[index].split("px");var numsp = parseInt(num[0]);numsp = numsp - 1;var make_str =numsp+"px"; var c = "width:"+make_str+";white-space: nowrap;overflow: hidden;text-overflow: ellipsis;";var d = "width:"+make_str+";"; $(this).css("cssText",c);$(this).children("div:first-child").css("cssText",c);$(this).children("div.fht-cell").css("cssText",d);});$("#table_spareparts_parent thead.fullHeadSecond tr th").each(function(index){var num = th_width_resize[index].split("px");var numsp = parseInt(num[0]);numsp = numsp - 1;var make_str =numsp+"px"; var c = "width:"+make_str+";white-space: nowrap;overflow: hidden;text-overflow: ellipsis;";var d = "width:"+make_str+";"; $(this).css("cssText",c);$(this).children("div:first-child").css("cssText",c);$(this).children("div.fht-cell").css("cssText",d);}); });});')
    
    
    dbl_clk_function = (
        '$("'
        + str(table_ids)
        + '").on("all.bs.table", function (e, name, args) { $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); }); $("'
        + str(table_ids)
        + '\ th.bs-checkbox div.th-inner").before("<div style=\'padding:0; border-bottom: 1px solid #dcdcdc;\'>SELECT</div>"); $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); $("'
        + str(table_ids)
        + "\").on('sort.bs.table', function (e, name, order) {  console.log('Parent sort.bs.table ====> ', e); currenttab = $(\"ul#carttabs_head .active\").text().trim(); localStorage.setItem('"
        + str(table_id)
        + "_SortColumn', name); localStorage.setItem('"
        + str(table_id)
        + "_SortColumnOrder', order); NestedContainerSorting(name, order, '"
        + str(table_id)
        + "'); }); "
        )
    NORECORDS = ""
    if len(data_list) == 0:
        NORECORDS = "NORECORDS"

    page = ""
    if QueryCount < int(PerPage):
        page = str(Page_start) + " - " + str(QueryCount)
    else:
        page = str(Page_start) + " - " + str(Page_End)
    Test = (
        '<div class="col-md-12 brdr listContStyle pad2height30" ><div class="col-md-4 pager-numberofitem clear-padding"><span class="pager-number-of-items-item noofitem" id="'
        + str(table_id)
        + '___NumberofItem" >'
        + str(page)
        + ' of</span><span class="pager-number-of-items-item fltltpad2mrg0" id="'
        + str(table_id)
        + '___totalItemCount" >'
        + str(QueryCount)
        + '</span><div class="clear-padding fltltmrgtp3" ><div  class="pull-right vertmidtxtrht"><select onchange="PageFunctestChild(this,\'Quote\',\'\',\'table_spareparts_parent\')" id="'
        + str(table_id)
        + '___PageCountValue" class="form-control wid65vermiddisinbmarl5"><option value="10" selected>10</option><option value="20">20</option><option value="50">50</option><option value="100">100</option><option value="200">200</option></select> </div></div></div><div class="col-xs-8 col-md-4  clear-padding disinpad10txtcen"  data-bind="visible: totalItemCount"><div class="clear-padding col-xs-12 col-sm-6 col-md-12 bor0" ><ul class="pagination pagination"><li class="disabled"><a href="#" onclick="FirstPageLoad_paginationChild(\'Quote\',\'\',\'table_spareparts_parent\')"><i class="fa fa-caret-left font14whtbld" ></i><i class="fa fa-caret-left font14" ></i></a></li><li class="disabled"><a href="#" onclick="Previous12334Child(\'Quote\',\'\',\'table_spareparts_parent\')"><i class="fa fa-caret-left font14" ></i>PREVIOUS</a></li><li class="disabled"><a href="#" class="disabledPage" onclick="Next12334Child(\'Quote\',\'\',\'table_spareparts_parent\')">NEXT<i class="fa fa-caret-right font14" ></i></a></li><li class="disabled"><a href="#" onclick="LastPageLoad_paginationChild(\'Quote\',\'\',\'table_spareparts_parent\')" class="disabledPage"><i class="fa fa-caret-right font14"></i><i class="fa fa-caret-right font14whtbld"></i></a></li></ul></div> </div> <div class="col-md-4 pr_page_pad"> <span id="'
        + str(table_id)
        + '___page_count" class="currentPage page_right_content">1</span><span class="page_right_content pad_rt_2">Page </span></div></div>'
    )
    if QueryCount < int(PerPage):
        PerPage = str(QueryCount)
    else:
        PerPage = str(PerPage)   
    if Page_End > QueryCount:
        Page_End = QueryCount
    else:
        Page_End = Page_End
    Action_Str = ""
    Action_Str += str(Page_start)+" - "
    Action_Str += str(Page_End)
    Action_Str += " of"
    return (
        table_header,
        data_list,
        table_id,
        filter_control_function,
        NORECORDS,
        dbl_clk_function,
        '',
        '',
        '',
        '',
        Test,
        Action_Str,
        QueryCount,
        page
    )


if Param.ACTION == "LOAD":
    PerPage = "10"
    PageInform = "1___10___10"
    A_Keys = []
    A_Values = []
    if Param.TABNAME == "Spare Parts Parent":
        ApiResponse = ApiResponseFactory.JsonResponse(getsparepartslist(PerPage, PageInform, A_Keys, A_Values))
    elif Param.TABNAME == "Spare Parts Child":
        ApiResponse = ApiResponseFactory.JsonResponse(getsparepartssublist(PerPage, PageInform, A_Keys, A_Values))
    
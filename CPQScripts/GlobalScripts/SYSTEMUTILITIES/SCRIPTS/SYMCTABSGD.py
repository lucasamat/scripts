# =========================================================================================================================================
#   __script_name : SYMCTABSGD.PY
#   __script_description : THIS SCRIPT IS USED TO LOAD THE TAB CONTAINER DATA ACROSS ALL THE APPS
#   __primary_author__ :
#   __create_date :
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
# pylint: noqa: E501
# pylint: disable=unused-variable
import Webcom
import Webcom.Configurator.Scripting.Test.TestProduct
Trace = Trace  # pylint: disable=E0602
# Log = Log  # pylint: disable=E0602
# SqlHelper = SqlHelper  # pylint: disable=E0602
# Sql = Sql  # pylint: disable=E0602
User = User  # pylint: disable=E0602
# date = date # pylint: disable=E0602
Webcom = Webcom  # pylint: disable=E0602
# Product = Product # pylint: disable=E0602
Session = Session  # pylint: disable=E0602
Param = Param  # pylint: disable=E0602
ApiResponseFactory = ApiResponseFactory  # pylint: disable=E0602
# pylint: disable = no-name-in-module, import-error, multiple-imports, pointless-string-statement, wrong-import-order

import re

import SYCNGEGUID as keyid
from SYDATABASE import SQL

Sql = SQL()
try:
    TestProduct = Webcom.Configurator.Scripting.Test.TestProduct()
    active_tab_name = TestProduct.CurrentTab
    productName = Product.GetGlobal("Pricemodel")
except:
    active_tab_name = Param.CurrentTab
    productName = "SALES"
Trace.Write("Line No: 35 => TABNAME =>" +active_tab_name)
userid = User.Id
Trace.Write(productName)
filter_level_input_data = "input"
filter_class_for_column_name = ".bootstrap-table-filter-control-{0}"
filter_class_name_input = (
    '<input type="text"   class="wth100visble form-control bootstrap-table-filter-control-' + "{0}" + '">'
)

filter_class_name_RelatedMutipleCheckBoxDrop = "#RelatedMutipleCheckBoxDrop_{0}"
div_RelatedMutipleCheckBoxDrop = """<div id = "RelatedMutipleCheckBoxDrop_{0}" class="form-control bootstrap-table-filter-control-{1} RelatedMutipleCheckBoxDrop_{2}" onclick="uncheckdata()" ></div>"""

pricebook_table = """<table id="FULLTABLELOAD" class="table table-responsive" data-pagination="false" data-search-on-enter-key="true" data-filter-control="true" data-maintain-selected="true" data-locale = "en-US" class= "shownskkk"> <thead> <tr class= "shownskkk">"""
pricebook_table_new = """<table id="duplicate_FULLTABLELOAD" style="display:none;" data-pagination="false" data-search-on-enter-key="true" data-filter-control="true" data-maintain-selected="true" data-locale = "en-US" class= "table table-responsive shownskkk"> <thead> <tr class= "shownskkk">"""

table = """<table id="FULLTABLELOAD" data-pagination="false" data-search-on-enter-key="true" data-filter-control="true" data-maintain-selected="true" data-locale = "en-US" class= "table table-responsive hiddenskkk"><thead><tr class= "hiddenskkk">"""
table_new = """<table id="duplicate_FULLTABLELOAD" style="display:none;" data-pagination="false" data-search-on-enter-key="true" data-filter-control="true" data-maintain-selected="true" data-locale = "en-US" class= "table table-responsive hiddenskkk"><thead><tr class= "hiddenskkk">"""

action_table_header = """<th class= "act_vss" data-field="ACTION"><div class="action_col">ACTIONS</div><button class="searched_button" id="Act_FULLTABLELOAD">Search</button></th>"""
action_table_header_new = """<th class= "act_vss" data-field="ACTION"><div class="action_col">ACTIONS</div><button class="searched_button" id="Act_FULLTABLELOAD">Search</button></th>"""

select_table_header = '<th data-field="SELECT" data-align="center"   data-checkbox="true" class="wth45"><div class="action_col">SELECT</div></th>'
select_table_header_new = '<th data-field="SELECT" data-align="center"  data-checkbox="true" class="wth45"><div class="action_col">SELECT</div></th>'

center_align = "center"
right_align = "right"
left_align = "left"
var_class = ""
record_id_table_header = '<th data-toggle="tooltip" data-placement="top" data-field="RECORD_ID" data-filter-control="input" data-align="{align_param}" data-title-tooltip="RECORD_ID" data-sortable="true">RECORD ID</th>'
center_align_table_header = '<th data-toggle="tooltip" id="{Es_k_upper_param}" data-placement="top" data-field="{ES_param}" data-filter-control="input" data-align="center" data-title-tooltip="{Es_k_param}" data-sortable="true">{Es_k_param}</th>'
right_align_table_header = '<th class="text-right" data-toggle="tooltip" id="{Es_k_upper_param}" data-placement="top" data-field="{ES_param}" data-filter-control="input" data-align="right" data-title-tooltip="{Es_k_param}" data-sortable="true">{Es_k_param}</th>'
right_left_align_table_header = '<th data-toggle="tooltip" data-placement="top" data-field="{ES_param}" data-filter-control="input" data-halign="{align_param}" data-align="{align_param}" {var_class} data-title-tooltip="{Es_k_param}" data-sortable="true">{Es_k_param}</th>'
table_head_body_tail = "</tr></thead><tbody></tbody></table>"
table_head_tail = "</tr></thead></table>"

table_id = "FULLTABLELOAD"
table_id_starts_with = "#"
table_id_filter_class = "#{table_id_param} .bootstrap-table-filter-control-"
symbol_values_list = """var SYMBOL = $(\"{filter_class_param}\").val(); """
non_symbol_values_list = 'var {invs_param} = $("{filter_class_param}").val();'
attributes_values_list = " ATTRIBUTE_VALUEList.push({invs_param}); "
action_filter_class_starts_with = "#Act_"

filter_control_function = """
$("'+filter_class+'").click(function() { 
    var active_subtab = $('.subtab_inner li.active').attr('id');
    if(active_subtab == 'subtab_list1'){
        flag = 0
    }else{
        flag = 1
    }
    var table_id = $(this).closest("table").attr("id"); 
    var a_list = '+str(NAME)+'; 
    ATTRIBUTE_VALUEList = []; '+str(values_list)+' 
    SortColumn = localStorage.getItem("SortColumn"); 
    SortColumnOrder = localStorage.getItem("SortColumnOrder"); 
    PerPage = $("#PageCountValue").val(); 
    PageInform = "1___" + PerPage + "___" + PerPage; 
    cpq.server.executeScript("SYMCTABSGD", {
        'ACTION': 'SORTING', 
        'A_Keys': a_list, 
        'A_Values': ATTRIBUTE_VALUEList, 
        "SortColumn": SortColumn, 
        "SortColumnOrder": SortColumnOrder, 
        "PerPage": PerPage, 
        "PageInform": PageInform,
        "FLAG":flag,
        "CurrentTab": "$("ul#carttabs_head li.active a span").text()"
    }, 
    function(dataset) {
        datas1 = dataset[1]; 
        datas5 = dataset[5]; 
        datas6 = dataset[6]; 
        datas12 = dataset[12];  
        try {
                $("'+str(table_ids)+'").bootstrapTable("load", datas1); 
                var uncheckid=localStorage.getItem("uncheckdata"); 
                if(uncheckid != "") { 
                    $("#"+uncheckid+" > span").removeAttr("class");
                    $("#"+uncheckid+" > span").attr("class","jqx-listitem-state-normal jqx-item checkboxes jqx-rc-all");
                    localStorage.getItem("uncheckdata",""); 
                }  
                eval(datas5); 
        } catch(err) {  
                $("'+str(table_ids)+'").bootstrapTable("load", datas1  ); 
                eval(datas5); 
        } 
        if (document.getElementById('totalItemCount')) { 
            document.getElementById('totalItemCount').innerHTML = datas6; 
        } 
        if (document.getElementById('NumberofItem')) { 
            document.getElementById('NumberofItem').innerHTML = dataset[11]; 
        } 
        if(document.getElementById('page_count')) { 
            document.getElementById('page_count').innerHTML = '1'; 
        }    
        $("#PageCountValue").val(dataset[12]); 
    });
    filter_search_click();
});"""


class CONTAINER:
    def __init__(self):
        pass

    def ListContainerShow(self, PerPage, PageInform, A_Keys, A_Values, SortColumn, SortColumnOrder):
        global active_tab_name
        table_header_new = ""
        onchange_filtercontrol_function = ""
        Page_start = ""
        Page_End = ""
        page_count = ""
        dbl_clk_function = ""
        RelatedDrop_str = ""
        filter_control_function = ""
        filter_level_list = x_tabs = ""
        QueryCount = 0
        AA_list = []
        cv_list = []
        subtabs = []
        count = 1
        subtab_str = ''
        li_str = ''
        tab_name_sub = ''
        active = ''
        subtab_list = Sql.GetList("SELECT top 1000 SUBTAB_NAME, SUBTAB_TYPE,DISPLAY_ORDER FROM SYSTAB WHERE TREE_NODE_RECORD_ID = '' AND SUBTAB_TYPE = '{}' ORDER BY DISPLAY_ORDER".format(active_tab_name.upper()))
        
        if subtab_list:
            for s in subtab_list:
                subtabs.append(s.SUBTAB_NAME)
                tab_name_sub = s.SUBTAB_TYPE
            Trace.Write("Subtab_Name_j "+str(s.SUBTAB_NAME))
            if active_tab_name == "My Approvals Queue" or active_tab_name == "Team Approvals Queue":
                subtab_down = "subtab-down"
            else:
                subtab_down = ""
            subtab_str = '<div class="row tabsfiled material_subtab_top '+str(subtab_down)+'"><div class="col-md-12 col-sm-12 col-xs-12 col-lg-12 material_subtab_bg"><div class="subtab_inner"><ul class="nav-tabs">'
        
            for s in subtabs:
                Trace.Write("SUBTAB_J "+str(s))
                subtab_str += '<li id="subtab_list'+str(count)+'" '+str(active)+' onclick="TabContainerFullList(this)"><a id = "subtab'+str(count)+'" data-toggle="tab" href="">'+str(s)+'</a></li>'
                count +=1
                active = ''
            subtab_str +='<li class="dropdown pull-right tabdrop hide"><a class="dropdown-toggle" data-toggle="dropdown" href="#"><i class="icon-align-justify"></i> <b class="caret"></b></a><ul class="dropdown-menu"></ul></li></ul></div></div></div>'
        active_tab = ''
        Trace.Write("active_tab_name__J "+str(active_tab_name))
        try:
            active_tab = x_tabs = active_tab_name
        except:
            active_tab = x_tabs = "Quotes"
        try:
            for tab in Product.Tabs:            
                if tab.IsSelected == True:
                    x_tabs = tab.Name
                    active_tab = x_tabs
                if Session[str(x_tabs)] is None:
                    Session[str(x_tabs)] = "20"
                elif Param.ACTION == "SECOND":
                    Session[str(x_tabs)] = PerPage
        except Exception:
            pass
        if not active_tab:
            active_tab = "Quotes"
        #x_tabs = active_tab_name
        if str(PerPage) == "" and str(PageInform) == "":
            if Session[str(x_tabs)] is None:
                Page_start = 1
                Page_End = 20
                PerPage = 20
                PageInform = "1___20___20"
            else:
                Page_start = 1
                Page_End = Session[str(x_tabs)]
                PerPage = Session[str(x_tabs)]
                PageInform = "1___" + str(Page_End) + "___" + str(PerPage)
        else:
            Page_start = int(PageInform.split("___")[0])
            Page_End = int(PageInform.split("___")[1])
            PerPage = PerPage
        D = {}
        a_10 = a_20 = a_50 = a_100 = a_200 = ""
        if str(PerPage) == "10":
            a_10 = "selected"
        if str(PerPage) == "20":
            a_20 = "selected"
        if str(PerPage) == "50":
            a_50 = "selected"
        if str(PerPage) == "100":
            a_100 = "selected"
        if str(PerPage) == "200":
            a_200 = "selected"
        SearchData = []
        newRowList = []
        a_list = []
        try:
            current_prod = Product.Name
        except:
            current_prod = "SALES"
        prod = Sql.GetFirst("select APP_ID from SYAPPS (nolock) where APP_LABEL= '" + str(current_prod.strip()) + "'")
        if prod is not None:
            if active_tab_name == "Contracts":
                crnt_prd_val = "CT"
            else:
                crnt_prd_val = prod.APP_ID
        else:
            crnt_prd_val = ""
        newRowDict = {}
        QueryCount = ""
        Query = ""
        QueryStr = ""
        table_header = ""
        names = ""
        PRIMARY_OBJECT_NAMes = ""  
        list_of_tabs = []
        list2 = []
        AA_list = []        
        
        for tab in Product.Tabs:
            list_of_tabs.append(tab.Name)
        if not list_of_tabs:
            list_of_tabs = ['Quotes', 'Contracts']
        Trace.Write("=================== 00000000000"+str(active_tab))    
        for tab_name in list_of_tabs:
            if tab_name == active_tab:
                Trace.Write("=================== 11111111"+str(tab_name))
                if tab_name == "Pricebook Entries" or tab_name == "Catalogs":
                    if A_Keys != "" and A_Values != "":
                        A_Keys = list(A_Keys)
                        A_Values = list(A_Values)
                        D = zip(A_Keys, A_Values)
                        D = dict(D)
                else:
                    if A_Keys != "" and A_Values != "":
                        A_Keys = list(A_Keys)[1:]

                        A_Values = list(A_Values)[1:]
                        D = zip(A_Keys, A_Values)
                        D = dict(D)
                sql_obj = Sql.GetList(
                    "SELECT top 1 SYSECT.PRIMARY_OBJECT_RECORD_ID,SYSECT.PRIMARY_OBJECT_NAME FROM SYSECT (NOLOCK) INNER JOIN SYPAGE(NOLOCK) ON SYSECT.PAGE_RECORD_ID = SYPAGE.RECORD_ID WHERE "
                    + " SYSECT.SECTION_NAME = 'BASIC INFORMATION' AND SYPAGE.TAB_NAME='"
                    + str(tab_name)
                    + "' and SYSECT.SAPCPQ_ATTRIBUTE_NAME like '%"
                    + crnt_prd_val
                    + "%' order by SYSECT.CpqTableEntryId"
                )
                try:
                    if Product.Attributes.GetByName("MA_MTR_ACTIVE_TAB") is not None:
                        Product.Attributes.GetByName("MA_MTR_ACTIVE_TAB").AssignValue(tab_name)
                except:
                    Trace.Write("Product Object Reference not available")
                if sql_obj is not None:
                    for sql in sql_obj:
                        tot_names = ""
                        PRIMARY_OBJECT_NAMes = str(sql.PRIMARY_OBJECT_NAME).strip()
                        #syproh permissions start
                        # data_obj = Sql.GetFirst(
                        #     "SELECT S.RECORD_ID,S.CONTAINER_NAME,S.COLUMNS,S.CAN_DELETE,S.CAN_EDIT FROM SYOBJS S (NOLOCK) INNER JOIN SYPROH P ON P.OBJECT_NAME = S.CONTAINER_NAME INNER JOIN USERS_PERMISSIONS UP ON UP.PERMISSION_ID = P.PROFILE_RECORD_ID WHERE S.NAME='Tab list' AND S.OBJ_REC_ID = '"
                        #     + str(sql.PRIMARY_OBJECT_RECORD_ID)
                        #     + "' AND UP.USER_ID = '"
                        #     + str(userid)
                        #     + "' and P.VISIBLE=1"
                        # )
                        # data_obj = Sql.GetFirst(
                        #     "SELECT S.RECORD_ID,S.CONTAINER_NAME,S.COLUMNS,S.CAN_DELETE,S.CAN_EDIT FROM SYOBJS S (NOLOCK) INNER JOIN SYPROH P ON P.OBJECT_NAME = S.CONTAINER_NAME INNER JOIN USERS_PERMISSIONS UP ON UP.PERMISSION_ID = P.PROFILE_RECORD_ID WHERE S.NAME='Tab list' AND S.OBJ_REC_ID = '"
                        #     + str(sql.PRIMARY_OBJECT_RECORD_ID)
                        #     + "' AND UP.USER_ID = '"
                        #     + str(userid)
                        #     + "' and P.VISIBLE=1"
                        # )
                        #syproh permissions end
                        data_obj = Sql.GetFirst(
                            "SELECT S.RECORD_ID,S.CONTAINER_NAME,S.COLUMNS,S.CAN_DELETE,S.CAN_EDIT FROM SYOBJS S (NOLOCK) WHERE S.NAME='Tab list' AND S.OBJ_REC_ID = '"
                            + str(sql.PRIMARY_OBJECT_RECORD_ID)
                            + "'"
                        )
                        if data_obj is not None:
                            # if tab_name == "Quotes":
                            #     name_obj = Sql.GetList(
                            #         "SELECT API_NAME,LOOKUP_OBJECT,LOOKUP_API_NAME, DATA_TYPE, FORMULA_DATA_TYPE,  CURRENCY_INDEX,FORMULA_LOGIC,PICKLIST,DECIMALS FROM  SYOBJD (NOLOCK) WHERE OBJECT_NAME in ('SAQTMT','SAQTRV','SAOPPR') and (API_NAME in "
                            #         + str(tuple(eval(data_obj.COLUMNS)))
                            #         + " or lookup_api_name in "
                            #         + str(tuple(eval(data_obj.COLUMNS)))
                            #         + ")"
                            #     )
                            # else:                            
                            name_obj = Sql.GetList(
                                "SELECT API_NAME,LOOKUP_OBJECT,LOOKUP_API_NAME, DATA_TYPE, FORMULA_DATA_TYPE,  CURRENCY_INDEX,FORMULA_LOGIC,PICKLIST,DECIMALS FROM  SYOBJD (NOLOCK) WHERE OBJECT_NAME='"
                                + PRIMARY_OBJECT_NAMes
                                + "' and (API_NAME in "
                                + str(tuple(eval(data_obj.COLUMNS)))
                                + " or lookup_api_name in "
                                + str(tuple(eval(data_obj.COLUMNS)))
                                + ")"
                            )                           
                                
                            lookup_disply_list = []
                            lookup_str = ""
                            checkbox_list = []
                            currency_dict = {}
                            currency_list = []
                            a_dict = {}
                            b_dict = {}
                            non_hyper_list = ["APROBJ_LABEL"]
                            if name_obj is not None:
                                for text in name_obj:
                                    if names == "":
                                        names = str(text.API_NAME)
                                    else:
                                        names = names + "," + str(text.API_NAME)
                                    if (
                                        text.LOOKUP_API_NAME != ""
                                        and text.LOOKUP_API_NAME is not None
                                        and text.LOOKUP_API_NAME not in non_hyper_list
                                    ):
                                        Trace.Write("lokpp")
                                        lookup_disply_list.append(str(text.LOOKUP_API_NAME))
                                lookup_list = {ins.LOOKUP_API_NAME: ins.API_NAME for ins in name_obj}

                                for ins in name_obj:
                                    if ins.DATA_TYPE == "FORMULA":
                                        Trace.Write("formul@@@@")
                                        try:
                                            FORMULA_LOGIC = ins.FORMULA_LOGIC
                                            FORMULA_col = ins.API_NAME
                                            FORMULA_table = FORMULA_LOGIC.split(" ")[3].strip()
                                            # if tab_name == "Quotes":
                                            #     ins_obj = Sql.GetFirst(
                                            #         "SELECT API_NAME, DATA_TYPE FROM  SYOBJD (NOLOCK) "
                                            #         + " WHERE OBJECT_NAME='"
                                            #         + str(FORMULA_table)
                                            #         + "' and API_NAME = '"
                                            #         + str(FORMULA_col)
                                            #         + "'"
                                            #     )
                                            # else:    
                                            ins_obj = Sql.GetFirst(
                                                "SELECT API_NAME, DATA_TYPE FROM  SYOBJD (NOLOCK) "
                                                + " WHERE OBJECT_NAME='"
                                                + str(FORMULA_table)
                                                + "' and API_NAME = '"
                                                + str(FORMULA_col)
                                                + "'"
                                            )
                                            a_dict[ins.API_NAME] = (
                                                ins_obj.DATA_TYPE
                                                if ins.DATA_TYPE == "FORMULA" and ins.FORMULA_DATA_TYPE != "CHECKBOX"
                                                else ins_obj.FORMULA_DATA_TYPE
                                            )
                                            b_dict[ins.API_NAME] = str(ins.PICKLIST)
                                            Trace.Write("formul44"+str(a_dict))
                                            Trace.Write("formul55"+str(b_dict))
                                        except:
                                            a_dict[ins.API_NAME] = ins.DATA_TYPE
                                            b_dict[ins.API_NAME] = str(ins.PICKLIST)
                                    else:
                                        Trace.Write("formul111")
                                        Trace.Write("formul22"+str(a_dict))
                                        Trace.Write("formul33"+str(b_dict))
                                        a_dict[ins.API_NAME] = ins.DATA_TYPE
                                        b_dict[ins.API_NAME] = str(ins.PICKLIST)
                                checkbox_list = [
                                    ins.API_NAME.strip()
                                    for ins in name_obj
                                    if (
                                        (ins.DATA_TYPE).upper() == "CHECKBOX"
                                        or (ins.FORMULA_DATA_TYPE).upper() == "CHECKBOX"
                                    )
                                ]
                                currency_list = [
                                    ins.API_NAME.strip()
                                    for ins in name_obj
                                    if (
                                        (ins.DATA_TYPE).upper() == "CURRENCY"
                                        or (ins.FORMULA_DATA_TYPE).upper() == "CURRENCY"
                                    )
                                ]
                                for ins in name_obj:
                                    if ins.DATA_TYPE == "CURRENCY" or ins.FORMULA_DATA_TYPE == "CURRENCY":
                                        currency_dict[str(ins.API_NAME).strip()] = str(ins.CURRENCY_INDEX)
                            lookup_str = ",".join(list(lookup_disply_list))
                            ##A055S000P01-8871 Code starts..
                            if PRIMARY_OBJECT_NAMes == "SAQTMT":
                                NAME = ['MASTER_TABLE_QUOTE_RECORD_ID', 'QUOTE_ID', 'QTEREV_ID','REVISION_STATUS','REVISION_DESCRIPTION', 'ACCOUNT_ID', 'ACCOUNT_NAME', 'SALESORG_ID','OWNER_NAME','OPPORTUNITY_NAME','CONTRACT_VALID_FROM', 'CONTRACT_VALID_TO']
                            else:
                                NAME = eval(data_obj.COLUMNS)
                            ##A055S000P01-8871 Code ends..
                            Trace.Write("NAMe"+str(NAME))
                            ind = 1
                            nameList = {}
                            NameListS = {}
                            NameListSK = {}
                            list2 = []
                            ctr_TotalRow = []
                            if current_prod == "":
                                for ik in NAME:
                                    fieldLabel = Sql.GetFirst(
                                        "SELECT FIELD_LABEL, DATA_TYPE, FORMULA_LOGIC, FIELD_SHORT_LABEL FROM  SYOBJD (NOLOCK) WHERE PARENT_OBJECT_RECORD_ID='"
                                        + str(sql.PRIMARY_OBJECT_RECORD_ID)
                                        + "' AND API_NAME = '"
                                        + str(ik)
                                        + "'"
                                    )
                                    if fieldLabel is not None:
                                        column.HeaderLabel = str(fieldLabel.FIELD_LABEL)
                                        nameList[fieldLabel.FIELD_LABEL] = ik
                                        if (
                                            str(fieldLabel.FIELD_SHORT_LABEL) is not None
                                            and str(fieldLabel.FIELD_SHORT_LABEL) != ""
                                        ):
                                            nameList[fieldLabel.FIELD_SHORT_LABEL] = ik
                                            NameListS[ik] = str(fieldLabel.FIELD_SHORT_LABEL)
                                        else:
                                            nameList[fieldLabel.FIELD_LABEL] = ik
                                            NameListS[ik] = str(fieldLabel.FIELD_LABEL)
                                        if str(fieldLabel.DATA_TYPE) == "FORMULA":
                                            F_table = str(fieldLabel.FORMULA_LOGIC).split(" ")[3]
                                            f_obj = Sql.GetFirst(
                                                "SELECT FIELD_LABEL, DATA_TYPE, FORMULA_LOGIC FROM  SYOBJD (NOLOCK) "
                                                + " WHERE OBJECT_NAME ='"
                                                + str(F_table)
                                                + "' AND API_NAME = '"
                                                + str(ik)
                                                + "'"
                                            )
                                            if f_obj is not None:
                                                NameListSK[ik] = str(f_obj.DATA_TYPE)
                                            else:
                                                NameListSK[ik] = "TEXT"
                                        else:
                                            NameListSK[ik] = str(fieldLabel.DATA_TYPE)
                                        list2.append(ik)
                                        ind += 1
                            else:
                                for ik in NAME:
                                    ##A055S000P01-8871 Code starts..
                                    if PRIMARY_OBJECT_NAMes == "SAQTMT":
                                        if ik == 'QUOTE_ID' or ik == 'QTEREV_ID' or ik == 'REVISION_STATUS' or ik == 'REVISION_DESCRIPTION' or ik == 'CONTRACT_VALID_FROM' or ik == 'CONTRACT_VALID_TO' or ik == 'SALESORG_ID' or ik == 'NET_VALUE':
                                            objh_obj = Sql.GetFirst(
                                                "select RECORD_ID from SYOBJH (NOLOCK) where OBJECT_NAME = 'SAQTRV' and DATA_TYPE ='AUTO NUMBER' "
                                            )
                                            sql.PRIMARY_OBJECT_RECORD_ID = objh_obj.RECORD_ID
                                        if ik == 'ACCOUNT_ID' or ik == 'ACCOUNT_NAME' or ik == 'OWNER_NAME':
                                            objh_obj = Sql.GetFirst(
                                                "select RECORD_ID from SYOBJH (NOLOCK) where OBJECT_NAME = 'SAQTMT' and DATA_TYPE ='AUTO NUMBER' "
                                            )
                                            sql.PRIMARY_OBJECT_RECORD_ID = objh_obj.RECORD_ID
                                        if ik == 'OPPORTUNITY_NAME':
                                            objh_obj = Sql.GetFirst(
                                                "select RECORD_ID from SYOBJH (NOLOCK) where OBJECT_NAME = 'SAOPQT' and DATA_TYPE ='AUTO NUMBER' "
                                            )
                                            sql.PRIMARY_OBJECT_RECORD_ID = objh_obj.RECORD_ID
                                    ##A055S000P01-8871 Code ends..        
                                    fieldLabel = Sql.GetFirst(
                                        "SELECT FIELD_LABEL,DATA_TYPE,FORMULA_LOGIC, FIELD_SHORT_LABEL FROM  SYOBJD (NOLOCK) "
                                        + " WHERE PARENT_OBJECT_RECORD_ID='"
                                        + str(sql.PRIMARY_OBJECT_RECORD_ID)
                                        + "' AND API_NAME = '"
                                        + str(ik)
                                        + "'"
                                    )
                                    if fieldLabel:
                                        if (
                                            str(fieldLabel.FIELD_SHORT_LABEL) is not None
                                            and str(fieldLabel.FIELD_SHORT_LABEL) != ""
                                        ):
                                            nameList[fieldLabel.FIELD_SHORT_LABEL] = ik
                                            NameListS[ik] = str(fieldLabel.FIELD_SHORT_LABEL)
                                        else:
                                            nameList[fieldLabel.FIELD_LABEL] = ik
                                            NameListS[ik] = str(fieldLabel.FIELD_LABEL)
                                    if fieldLabel is not None:
                                        if str(fieldLabel.DATA_TYPE) == "FORMULA":
                                            try:
                                                # To get field label from formula logic
                                                F_table = str(fieldLabel.FORMULA_LOGIC).split(" ")[3].replace("(NOLOCK)","")
                                                ik_1 = str(fieldLabel.FORMULA_LOGIC).split(" ")[1].strip()
                                                # To get field label from formula logic
                                            except:
                                                F_table = ""
                                                ik_1 = ik
                                            f_obj = Sql.GetFirst(
                                                "SELECT FIELD_LABEL, DATA_TYPE, FORMULA_LOGIC FROM  SYOBJD (NOLOCK) "
                                                + " WHERE OBJECT_NAME ='"
                                                + str(F_table)
                                                + "' AND API_NAME = '"
                                                + str(ik_1)
                                                + "'"
                                            )
                                            if f_obj is not None:
                                                NameListSK[ik] = str(f_obj.DATA_TYPE)
                                            else:
                                                NameListSK[ik] = "TEXT"
                                        else:
                                            NameListSK[ik] = str(fieldLabel.DATA_TYPE)
                                        list2.append(ik)
                                        ind += 1
                            try:
                                TabName = Product.Tabs.GetByName(tab_name).Attributes
                            except:
                                TabName = "Quotes"
                            count = 11
                            a_list = []
                            for keys, attrname in enumerate(NAME):
                                if a_dict.get(attrname):
                                    a_list.append(str(a_dict.get(attrname)))
                                else:
                                    a_list.append("")
                            where = "WHERE 1=1"
                            if Param.ACTION == "FIRST":

                                currecy_glob = {}
                                if PRIMARY_OBJECT_NAMes == "PRCURR":
                                    currecy_glob_obj = Sql.GetList(
                                        "select unicode(symbol) as uni,symbol from prcurr (NOLOCK)"
                                    )
                                    for glob in currecy_glob_obj:
                                        if glob.symbol:
                                            currecy_glob[glob.symbol] = glob.uni
                                    try:
                                        Product.SetGlobal("GLOBUNICURRENCY", str(currecy_glob))
                                    except:
                                        Trace.Write("Set Global not defined based on Product object")
                            if str(PRIMARY_OBJECT_NAMes) == "ACAPMA" or str(PRIMARY_OBJECT_NAMes) == 'ACAPTX':
                                Role_list = []
                                if tab_name != "My Approvals Queue" and tab_name != "Team Approvals Queue":
                                    GettingRoleId = SqlHelper.GetList(
                                        "SELECT SYROMA.* FROM SYROUS INNER JOIN SYROMA ON SYROMA.ROLE_RECORD_ID = SYROUS.ROLE_RECORD_ID WHERE USER_RECORD_ID = '"
                                        + str(User.Id)
                                        + " ' "
                                    )
                                    for Role in GettingRoleId:
                                        roleId = str(Role.ROLE_RECORD_ID)
                                        Role_list.append(roleId)
                                        CheckParent = SqlHelper.GetFirst(
                                            "SELECT * FROM SYROMA WHERE PAR_ROLE_RECORD_ID = '" + str(roleId) + "' "
                                        )
                                        if CheckParent:
                                            Role_list = self.UserRoleLoop(Role_list, roleId)
                                    
                                    AprChainlist = str(Role_list).replace("[", "").replace("]", "")
                                    #Trace.Write("SELECT * FROM ACACSA WHERE ROLE_RECORD_ID IN (" + str(AprChainlist) + ") ")
                                    GetApprovalChain = (
                                        "SELECT APRCHN_RECORD_ID FROM ACACSA WHERE ROLE_RECORD_ID IN ("
                                        + str(AprChainlist)
                                        + ") "
                                    )
                                    where += " AND APRCHN_RECORD_ID in (" + str(GetApprovalChain) + ")"
                                else:
                                    """ GetChainList = Sql.GetList(
                                        "SELECT * FROM ACAPTX WHERE APPROVAL_RECIPIENT_RECORD_ID = '" + str(User.Id) + "' "
                                    )
                                    GetList = []
                                    GetApprovalList = []
                                    for chainlist in GetChainList:
                                        ApprovalChain = str(chainlist.APRCHN_RECORD_ID)
                                        ApprovalRecId = str(chainlist.APPROVAL_RECORD_ID)
                                        GetApprovalList.append(ApprovalRecId)
                                        if ApprovalChain not in GetList:
                                            GetList.append(ApprovalChain)
                                    conditionList = str(GetList).replace("[", "").replace("]", "")
                                    Approvalcond = str(GetApprovalList).replace("[", "").replace("]", "")
                                    if conditionList != '' and Approvalcond !='': """
                                    if flag == 0  or flag == 1 or flag == 2:
                                        if x_tabs != 'Team Approvals Queue':
                                            where += (
                                                " AND APPROVAL_RECIPIENT = '" + str(User.Name) + "' "
                                            )
                                        else:
                                            if str(x_tabs) == 'Team Approvals Queue':
                                                #Added try, except because of data not loading error A055S000P01-3527 - start
                                                try:                                              
                                                    GetRole = Sql.GetFirst("SELECT ROLE_RECORD_ID FROM SYROUS (NOLOCK) WHERE USER_NAME = '{}' AND ROLE_NAME != 'AUDITING ROLE' AND ROLE_NAME != 'add new role'".format(User.Name))
                                                except:
                                                    GetRole = '' 
                                                try:                                                         
                                                    GetIds = Sql.GetList("SELECT DISTINCT USERS.NAME FROM USERS(NOLOCK) JOIN SYROUS (NOLOCK) ON USERS.NAME = SYROUS.USER_NAME WHERE SYROUS.ROLE_RECORD_ID = '{}'".format(GetRole.ROLE_RECORD_ID))
                                                except: 
                                                    GetIds = ''
                                                #Added try, except because of data not loading error A055S000P01-3527 - end   
                                                GetPermission = Sql.GetFirst("SELECT permission_id FROM users_permissions where user_id = '{}'".format(User.Id))
                                                GetProfileIds = Sql.GetList("select DISTINCT U.NAME  from USERS U (nolock) inner join users_permissions up on U.id = up.user_id inner join cpq_permissions c on c.permission_id = up.permission_id  where up.permission_id = '{}'".format(GetPermission.permission_id))
                                                listofids1 = []
                                                listofids2 = []
                                                final = []
                                                for id in GetIds:
                                                    listofids1.append(str(id.NAME))
                                                for ids in GetProfileIds:
                                                    listofids2.append(str(ids.NAME))
                                                listofids1.extend(listofids2)
                                                final = list(set(listofids1))
                                                if flag == 0:
                                                    where += " AND APRCHNSTP_APPROVER_ID != '' AND APRCHNSTP_APPROVER_ID NOT LIKE '%USR%' AND APPROVALSTATUS = 'REQUESTED' AND ARCHIVED = 0 AND APPROVAL_RECIPIENT = '{}'".format(User.Name) 
                                                elif flag == 1:
                                                    where += " AND APRCHNSTP_APPROVER_ID != '' AND APRCHNSTP_APPROVER_ID NOT LIKE '%USR%' AND APPROVAL_RECIPIENT = '{}' AND APPROVALSTATUS IN ( 'APPROVED','REJECTED') ".format(User.Name)
                                    else:
                                        where += (" AND APPROVALSTATUS NOT IN  ('REQUESTED','APPROVAL REQUIRED')")

                            for record in D:
                                Trace.Write("record__J "+str(D[record]))
                                if D[record] != "" and D[record] is not None:
                                    x_picklistcheckobj = Sql.GetFirst(
                                        "SELECT PICKLIST FROM  SYOBJD (NOLOCK) WHERE OBJECT_NAME ='"
                                        + str(PRIMARY_OBJECT_NAMes)
                                        + "' AND API_NAME = '"
                                        + str(record)
                                        + "'"
                                    )
                                    x_picklistcheck = (
                                        str(x_picklistcheckobj.PICKLIST).upper() if x_picklistcheckobj is not None else ""
                                    )
                                    X_col = D.get(record)
                                    if str(record) != "SYMBOL":
                                        if str(X_col).find(",") != -1:
                                            xx = list(str(D.get(record)).split(","))
                                            xx = [inj.strip() for inj in xx]
                                            if len(xx) > 1:

                                                where += " AND " + str(record) + " in " + str(tuple(xx)) + ""

                                            else:
                                                rec = list(D[record])[0].strip()
                                                if str(rec).upper() == "TRUE":
                                                    where += " AND " + str(record) + " in ('true', '1')"

                                                elif str(rec).upper() == "false":
                                                    where += " AND ( " + str(record) + " in ('false', '0', '')"
                                                    where += " or " + str(record) + " is Null )"
                                                elif re.search(r"(\d+/\d+/\d+)", str(rec)):
                                                    where += " AND " + str(record) + " = '" + str(rec) + "'"
                                                else:
                                                    where += " AND " + str(record) + " = '" + str(rec) + "'"
                                        else:
                                            rec = str(D.get(record)).strip()
                                            if str(rec).upper() == "TRUE":
                                                recordval = ["1", "true"]
                                                where += " AND " + str(record) + " in " + str(tuple(recordval))
                                            elif str(rec).upper() == "FALSE":
                                                recordval = ["0", "false", ""]
                                                where += " AND ( " + str(record) + " in " + str(tuple(recordval))
                                                where += " or " + str(record) + " is Null )"
                                            elif re.search(r"(\d+/\d+/\d+)", rec):
                                                if x_picklistcheck == "TRUE":
                                                    where += " AND " + str(record) + " like '" + str(rec) + "'"
                                                    
                                                else:
                                                    where += " AND " + str(record) + " = '" + str(rec) + "'"
                                                    
                                            else:
                                                if x_picklistcheck == "TRUE":
                                                    where += " AND " + str(record) + " = '" + str(rec) + "'"
                                                else:
                                                    if str(record) == "CpqTableEntryId":
                                                        where += " AND " + str(record) + " = '" + str(rec) + "'"
                                                    elif str(record) == "ATTRIBUTE_NAME":
                                                        where += (
                                                            " AND "
                                                            + str(record)
                                                            + " like '%"
                                                            + (str(rec).replace("'", "''"))
                                                            + "%'"
                                                        )
                                                    else:
                                                        ##A055S000P01-8871 Code starts..
                                                        if PRIMARY_OBJECT_NAMes == "SAQTMT":
                                                            if str(record) in ("QUOTE_TYPE","SALE_TYPE","QUOTE_STATUS","MASTER_TABLE_QUOTE_RECORD_ID","ACCOUNT_ID","ACCOUNT_NAME","ACCOUNT_RECORD_ID","OWNER_NAME","QTEREV_RECORD_ID"):
                                                                record = "SAQTMT." + str(record) 
                                                            elif str(record) == "OPPORTUNITY_NAME":
                                                                record = "SAOPQT." +str(record)
                                                            elif str(record) in ("QUOTE_ID","QTEREV_ID","SALESORG_ID","REVISION_STATUS","REVISION_DESCRIPTION","CONTRACT_VALID_FROM","CONTRACT_VALID_TO"):
                                                                record = "SAQTRV." +str(record)
                                                        where += " AND " + str(record) + " like '%" + str(rec) + "%'"
                                                        ##A055S000P01-8871 Code ends..
                                                        

                                    else:
                                        reco = list(D.get(record).split(",")) if D.get(record).find(",") else D.get(record)
                                        
                                        recordval = []
                                        try:
                                            x = Product.GetGlobal("GLOBUNICURRENCY")
                                        except:
                                            Trace.Write("Currency X is not defined")
                                        recordval.append("01")
                                        for rec in reco:
                                            x1 = eval(x).get(rec)
                                            if x1 is not None and x1 != "":
                                                recordval.append(x1)
                                        recordvals = (
                                            str(tuple(recordval)) if len(recordval) > 1 else "('" + recordval[0] + "')"
                                        )
                                        where += " AND unicode(symbol) in " + str(recordvals)

                            texts = ""
                            col = ""
                            name = names.split(",")
                            for text in list(name):
                                # if tab_name == "Quotes":
                                #     s = Sql.GetList(
                                #         "select DATA_TYPE from  SYOBJD (NOLOCK) WHERE API_NAME='"
                                #         + str(text)
                                #         + "' and OBJECT_NAME in ('SAQTMT','SAQTRV','SAOPPR')"
                                #     )
                                # else:    
                                s = Sql.GetList(
                                    "select DATA_TYPE from  SYOBJD (NOLOCK) WHERE API_NAME='"
                                    + str(text)
                                    + "' and OBJECT_NAME='"
                                    + str(sql.PRIMARY_OBJECT_NAME).strip()
                                    + "'"
                                )
                                for ins in s:
                                    if ins.DATA_TYPE == "DATE":
                                        if texts != "":
                                            text = "CONVERT(VARCHAR(10)," + str(text) + ",101) AS [" + str(text) + "]"
                                            texts = texts + "," + str(text)
                                        else:
                                            text = "CONVERT(VARCHAR(10)," + str(text) + ",101) AS [" + str(text) + "]"
                                            texts = str(text)
                                    else:
                                        if col != "":
                                            col = col + ",[" + text + "]"
                                        else:
                                            col = "[" + str(text) + "]"
                            if texts != "":
                                tot_names = col + "," + texts
                            else:
                                tot_names = col
                            AA_list = []
                            A_list1 = []
                            filter_level_list = []
                            cv_list = []
                            filter_clas_name = ""
                            for key, col_name in enumerate(list(list2)):
                                col_name, key = str(col_name), str(key)
                                A_list = []
                                if str(b_dict.get(col_name)).upper() == "TRUE":
                                    filter_level_data = "select"
                                    filter_level_list.append(filter_level_data)
                                    filter_clask = filter_class_name_RelatedMutipleCheckBoxDrop.format(key)
                                    filter_clas_name = div_RelatedMutipleCheckBoxDrop.format(key, col_name, key)
                                    try:
                                        if a_dict.get(col_name) == "DATE":
                                            xcdx = (
                                                "SELECT DISTINCT ', ' + CONVERT(VARCHAR(10), "
                                                + col_name
                                                + ",101) FROM "
                                                + PRIMARY_OBJECT_NAMes
                                                + " (NOLOCK) FOR XML PATH('') ), 1, 2, '')  ) AS StringValue"
                                            )
                                            xcd = Sql.GetFirst(xcdx)
                                            try:
                                                A_list1 = str(xcd.StringValue.encode("ASCII", "ignore").strip()).split(",")
                                            except:
                                                A_list1 = []
                                            AA_list.append(sorted(A_list1))
                                        elif a_dict.get(col_name) == "CHECKBOX":
                                            AA_list.append(["True", "False"])
                                        else:
                                            xcdx = (
                                                "SELECT DISTINCT top 1000000 "
                                                + col_name
                                                + " FROM "
                                                + PRIMARY_OBJECT_NAMes
                                                + " (NOLOCK) order by "
                                                + col_name
                                            )
                                            xcd = Sql.GetList(xcdx)
                                            if xcd is not None:
                                                a = [
                                                    str(eval("datk." + col_name)).strip()
                                                    for datk in xcd
                                                    if str(eval("datk." + col_name)) != ""
                                                ]
                                                AA_list.append(a)
                                    except:
                                        if a_dict.get(col_name) == "DATE":
                                            xcdx = (
                                                "SELECT (STUFF((SELECT DISTINCT ', ' + CONVERT(VARCHAR(10), "
                                                + col_name
                                                + ",101) FROM "
                                                + PRIMARY_OBJECT_NAMes
                                                + " (NOLOCK) FOR XML PATH('') ), 1, 2, '')  ) AS StringValue"
                                            )
                                            xcd = Sql.GetFirst(xcdx)
                                            try:
                                                A_list1 = str(xcd.StringValue.encode("ASCII", "ignore").strip()).split(",")
                                            except:
                                                A_list1 = []
                                            AA_list.append(sorted(A_list1))
                                        elif a_dict.get(col_name) == "CHECKBOX":
                                            AA_list.append(["True", "False"])
                                        else:
                                            xcdx = (
                                                "SELECT DISTINCT top 1000"
                                                + col_name
                                                + " FROM "
                                                + PRIMARY_OBJECT_NAMes
                                                + " (NOLOCK) order by "
                                                + col_name
                                            )
                                            xcd = Sql.GetList(xcdx)
                                            if xcd is not None:
                                                a = [
                                                    eval("datk." + col_name).strip()
                                                    for datk in xcd
                                                    if eval("datk." + col_name) != ""
                                                ]
                                                AA_list.append(a)
                                else:
                                    AA_list.append([""])
                                    filter_level_data = filter_level_input_data
                                    filter_level_list.append(filter_level_data)
                                    filter_clask = filter_class_for_column_name.format(col_name)
                                    filter_clas_name = filter_class_name_input.format(col_name)
                                cv_list.append(filter_clas_name)

                            objh_obj = Sql.GetFirst(
                                "select * from SYOBJH (NOLOCK) where OBJECT_NAME = '"
                                + PRIMARY_OBJECT_NAMes
                                + "' and DATA_TYPE ='AUTO NUMBER' "
                            )
                            OrderBy_obj = Sql.GetFirst(
                                "select ORDERS_BY from SYOBJS (NOLOCK) where CONTAINER_NAME = '"
                                + PRIMARY_OBJECT_NAMes
                                + "' and NAME ='Tab list' "
                            )
                            if OrderBy_obj is not None and SortColumn == "" and SortColumnOrder == "":
                                if str(OrderBy_obj.ORDERS_BY) != "":
                                    objh_column = "ORDER BY " + str(OrderBy_obj.ORDERS_BY)
                                elif x_tabs == 'Team Approvals Queue' and flag in (0,1):
                                    objh_column = " ORDER BY APRTRXOBJ_ID DESC "
                                elif SortColumn == "" and SortColumnOrder == "":
                                    objh_column = "ORDER BY " + objh_obj.RECORD_NAME + " ASC"
                                else:
                                    objh_column = "ORDER BY " + str(SortColumn)
                            else:
                                if SortColumn == "" and SortColumnOrder == "":
                                    objh_column = "ORDER BY " + objh_obj.RECORD_NAME + " ASC"
                                else:
                                    if SortColumn.upper().find("DATE") == -1:
                                        objh_column = "ORDER BY " + str(SortColumn) + " " + str(SortColumnOrder).upper()

                                    else:
                                        objh_column = (
                                            " ORDER BY CONVERT(datetime,"
                                            + str(SortColumn)
                                            + ", 101)"
                                            + str(SortColumnOrder).upper()
                                        )
                            if where != "WHERE 1=1":
                                
                                try:

                                    if PageInform == "":
                                        QueryStr = (
                                            "select "
                                            + str(tot_names)
                                            + " from "
                                            + PRIMARY_OBJECT_NAMes
                                            + "(nolock) m "
                                            + str(where)
                                        )
                                    else:
                                        Trace.Write("flag__J "+str(flag) + " x_tabs"+str(x_tabs))
                                        # if flag == 0 and (str(x_tabs) == 'Quotes' or str(x_tabs) == 'Contracts'):
                                        #     where += " AND CPQTABLEENTRYADDEDBY = '{}' AND SAQTRV.ACTIVE = 'True' ".format(User.UserName)
                                        # if flag == 3 and (str(x_tabs) == 'Quotes' or str(x_tabs) == 'Contracts'): 
                                        #     where += "AND ACAPTX.APPROVAL_RECIPIENT_RECORD_ID = '" + str(User.Id) + "' and QUOTE_STATUS = 'WAITING FOR APPROVAL' AND ACAPTX.ARCHIVED = 0"  
                                        #     tot_names +=  ',APPROVAL_TRANSACTION_RECORD_ID'
                                        if flag == 0 and (str(x_tabs) == 'My Approvals Queue'):
                                            where += " AND APPROVALSTATUS = 'REQUESTED' AND ARCHIVED = 0 "
                                            
                                        elif flag == 2 and (str(x_tabs) == 'My Approvals Queue'):
                                            where += " AND APPROVALSTATUS NOT IN  ('REQUESTED') "
                                        elif flag == 1 and (str(x_tabs) == 'My Approvals Queue'):
                                            where += " AND APPROVALSTATUS IN ('APPROVED','REJECTED')"
                                            
                                        #elif flag == 0 and (str(x_tabs) == 'Team Approval Queue'):
                                            #where += " AND APPROVALSTATUS = 'REQUESTED' AND ARCHIVED = 0 "
                                        else:
                                            Trace.Write(str(where)+"---where---search---x_tabs------"+str(x_tabs))
                                        Trace.Write("@@@691 --74222--- flag---"+str(flag))
                                        # if flag == 3 and (str(x_tabs) == 'Quotes' or str(x_tabs) == 'Contracts'):
                                        #     QueryStr = (
                                        #         "select DISTINCT top "
                                        #         + PerPage
                                        #         + " MASTER_TABLE_QUOTE_RECORD_ID, QUOTE_TYPE, QUOTE_ID, SALE_TYPE, QUOTE_NAME, QUOTE_STATUS, ACCOUNT_NAME,CONTRACT_VALID_FROM,CONTRACT_VALID_TO from (select ROW_NUMBER() OVER(ORDER BY SAQTMT.CpqTableEntryId DESC) AS ROW, "
                                        #         + str(tot_names)
                                        #         + " from SAQTMT (NOLOCK) JOIN ACAPTX (NOLOCK) ON SAQTMT.QUOTE_ID = ACAPTX.APRTRXOBJ_ID "
                                        #         + str(where)
                                        #         + " ) S where S.ROW BETWEEN "
                                        #         + str(Page_start)
                                        #         + " and "
                                        #         + str(Page_End)
                                        #     )
                                            
                                        #     QueryCountStr = (
                                        #     "select rowcnt= count(SAQTMT.QUOTE_ID) from SAQTMT (NOLOCK) JOIN ACAPTX (NOLOCK) ON SAQTMT.QUOTE_ID = ACAPTX.APRTRXOBJ_ID " + str(where)
                                        #     )
                                        ##A055S000P01-8871 Code starts..
                                        if flag == 3 and (str(x_tabs) == 'Quotes' or str(x_tabs) == 'Contracts'):
                                            where += " AND ACAPTX.APPROVAL_RECIPIENT_RECORD_ID = '" + str(User.Id) + "' AND SAQTMT.CPQTABLEENTRYADDEDBY = '{}' AND SAQTRV.REVISION_STATUS = 'WAITING FOR APPROVAL' AND ACAPTX.ARCHIVED = 'False'".format(User.UserName)
                                            if "CONTRACT_VALID_FROM" in str(where):
                                                where = str(where).replace("CONTRACT_VALID_FROM","SAQTRV.CONTRACT_VALID_FROM")
                                            if "CONTRACT_VALID_TO" in str(where):
                                                where = str(where).replace("CONTRACT_VALID_TO","SAQTRV.CONTRACT_VALID_TO")
                                            if "SAQTRV.SAQTRV.CONTRACT_VALID_FROM" in str(where):
                                                where = str(where).replace("SAQTRV.SAQTRV.CONTRACT_VALID_FROM","SAQTRV.CONTRACT_VALID_FROM")
                                            if "SAQTRV.SAQTRV.CONTRACT_VALID_TO" in str(where):
                                                where = str(where).replace("SAQTRV.SAQTRV.CONTRACT_VALID_TO","SAQTRV.CONTRACT_VALID_TO")    
                                            QueryStr = (
                                                "select * from (select ROW_NUMBER() OVER(ORDER BY SAQTMT.CpqTableEntryId DESC) AS ROW, SAQTMT.[QUOTE_TYPE],SAQTMT.[SALE_TYPE],SAQTRV.[QUOTE_ID],SAQTMT.[QUOTE_STATUS],SAQTMT.[MASTER_TABLE_QUOTE_RECORD_ID],SAQTMT.[ACCOUNT_ID],SAQTMT.[ACCOUNT_NAME],SAQTMT.[ACCOUNT_RECORD_ID],SAQTMT.[OWNER_NAME],SAQTMT.[QTEREV_RECORD_ID],SAQTRV.[QTEREV_ID],SAQTRV.[SALESORG_ID],SAQTRV.[REVISION_STATUS],SAQTRV.[REVISION_DESCRIPTION],SAOPQT.[OPPORTUNITY_NAME],CONVERT(VARCHAR(10),SAQTRV.CONTRACT_VALID_FROM,101) AS [CONTRACT_VALID_FROM],CONVERT(VARCHAR(10),SAQTRV.CONTRACT_VALID_TO,101) AS [CONTRACT_VALID_TO]  from SAQTMT INNER JOIN SAQTRV ON  SAQTMT.[MASTER_TABLE_QUOTE_RECORD_ID] = SAQTRV.[QUOTE_RECORD_ID] INNER JOIN SAOPQT ON SAOPQT.[QUOTE_RECORD_ID] = SAQTRV.[QUOTE_RECORD_ID] INNER JOIN ACAPTX ON ACAPTX.APRTRXOBJ_ID = SAQTRV.[QUOTE_ID] AND SAQTRV.ACTIVE = 'True'  "
                                                + str(where)
                                                + ") m where m.ROW BETWEEN "
                                                + str(Page_start)
                                                + " and "
                                                + str(Page_End)
                                                + " "
                                            )
                                            QueryCountStr = (
                                                "select rowcnt= count(*)  from " + PRIMARY_OBJECT_NAMes + " INNER JOIN SAQTRV ON  SAQTMT.[MASTER_TABLE_QUOTE_RECORD_ID] = SAQTRV.[QUOTE_RECORD_ID] INNER JOIN SAOPQT ON SAOPQT.[QUOTE_RECORD_ID] = SAQTRV.[QUOTE_RECORD_ID] INNER JOIN ACAPTX ON ACAPTX.APRTRXOBJ_ID = SAQTRV.[QUOTE_ID] AND SAQTRV.ACTIVE = 'True' " + str(where)
                                            )    
                                            Trace.Write('## QueryStr--->11'+str(QueryStr))
                                        elif flag == 0 and (str(x_tabs) == 'Quotes' or str(x_tabs) == 'Contracts'):
                                            where += " AND SAQTMT.CPQTABLEENTRYADDEDBY = '{}' ".format(User.UserName)
                                            if "CONTRACT_VALID_FROM" in str(where):
                                                where = str(where).replace("CONTRACT_VALID_FROM","SAQTRV.CONTRACT_VALID_FROM")
                                            if "CONTRACT_VALID_TO" in str(where):
                                                where = str(where).replace("CONTRACT_VALID_TO","SAQTRV.CONTRACT_VALID_TO")
                                            if "SAQTRV.SAQTRV.CONTRACT_VALID_FROM" in str(where):
                                                where = str(where).replace("SAQTRV.SAQTRV.CONTRACT_VALID_FROM","SAQTRV.CONTRACT_VALID_FROM")
                                            if "SAQTRV.SAQTRV.CONTRACT_VALID_TO" in str(where):
                                                where = str(where).replace("SAQTRV.SAQTRV.CONTRACT_VALID_TO","SAQTRV.CONTRACT_VALID_TO")            
                                            QueryStr = (
                                                "select * from (select ROW_NUMBER() OVER(ORDER BY SAQTMT.CpqTableEntryId DESC) AS ROW, SAQTMT.[QUOTE_TYPE],SAQTMT.[SALE_TYPE],SAQTRV.[QUOTE_ID],SAQTMT.[QUOTE_STATUS],SAQTMT.[MASTER_TABLE_QUOTE_RECORD_ID],SAQTMT.[ACCOUNT_ID],SAQTMT.[ACCOUNT_NAME],SAQTMT.[ACCOUNT_RECORD_ID],SAQTMT.[OWNER_NAME],SAQTMT.[QTEREV_RECORD_ID],SAQTRV.[QTEREV_ID],SAQTRV.[SALESORG_ID],SAQTRV.[REVISION_STATUS],SAQTRV.[REVISION_DESCRIPTION],SAOPQT.[OPPORTUNITY_NAME],CONVERT(VARCHAR(10),SAQTRV.CONTRACT_VALID_FROM,101) AS [CONTRACT_VALID_FROM],CONVERT(VARCHAR(10),SAQTRV.CONTRACT_VALID_TO,101) AS [CONTRACT_VALID_TO]  from SAQTMT INNER JOIN SAQTRV ON  SAQTMT.[MASTER_TABLE_QUOTE_RECORD_ID] = SAQTRV.[QUOTE_RECORD_ID] INNER JOIN SAOPQT ON SAOPQT.[QUOTE_RECORD_ID] = SAQTRV.[QUOTE_RECORD_ID] AND SAQTRV.ACTIVE = 'True'  "
                                                + str(where)
                                                + ") m where m.ROW BETWEEN "
                                                + str(Page_start)
                                                + " and "
                                                + str(Page_End)
                                                + " "
                                            )
                                            QueryCountStr = (
                                                "select rowcnt= count(*)  from " + PRIMARY_OBJECT_NAMes + " INNER JOIN SAQTRV ON  SAQTMT.[MASTER_TABLE_QUOTE_RECORD_ID] = SAQTRV.[QUOTE_RECORD_ID] INNER JOIN SAOPQT ON SAOPQT.[QUOTE_RECORD_ID] = SAQTRV.[QUOTE_RECORD_ID] AND SAQTRV.ACTIVE = 'True' " + str(where)
                                            )    
                                            Trace.Write('## QueryStr--->'+str(QueryStr))
                                        elif flag == 1 and (str(x_tabs) == 'Quotes'):
                                            if "CONTRACT_VALID_FROM" in str(where):
                                                where = str(where).replace("CONTRACT_VALID_FROM","SAQTRV.CONTRACT_VALID_FROM")
                                            if "CONTRACT_VALID_TO" in str(where):
                                                where = str(where).replace("CONTRACT_VALID_TO","SAQTRV.CONTRACT_VALID_TO")
                                            if "SAQTRV.SAQTRV.CONTRACT_VALID_FROM" in str(where):
                                                where = str(where).replace("SAQTRV.SAQTRV.CONTRACT_VALID_FROM","SAQTRV.CONTRACT_VALID_FROM")
                                            if "SAQTRV.SAQTRV.CONTRACT_VALID_TO" in str(where):
                                                where = str(where).replace("SAQTRV.SAQTRV.CONTRACT_VALID_TO","SAQTRV.CONTRACT_VALID_TO")    
                                            QueryStr = (
                                                "select * from (select ROW_NUMBER() OVER(ORDER BY SAQTMT.CpqTableEntryId DESC) AS ROW, SAQTMT.[QUOTE_TYPE],SAQTMT.[SALE_TYPE],SAQTRV.[QUOTE_ID],SAQTMT.[QUOTE_STATUS],SAQTMT.[MASTER_TABLE_QUOTE_RECORD_ID],SAQTMT.[ACCOUNT_ID],SAQTMT.[ACCOUNT_NAME],SAQTMT.[ACCOUNT_RECORD_ID],SAQTMT.[OWNER_NAME],SAQTMT.[QTEREV_RECORD_ID],SAQTRV.[QTEREV_ID],SAQTRV.[SALESORG_ID],SAQTRV.[REVISION_STATUS],SAQTRV.[REVISION_DESCRIPTION],SAOPQT.[OPPORTUNITY_NAME],CONVERT(VARCHAR(10),SAQTRV.CONTRACT_VALID_FROM,101) AS [CONTRACT_VALID_FROM],CONVERT(VARCHAR(10),SAQTRV.CONTRACT_VALID_TO,101) AS [CONTRACT_VALID_TO]  from SAQTMT INNER JOIN SAQTRV ON  SAQTMT.[MASTER_TABLE_QUOTE_RECORD_ID] = SAQTRV.[QUOTE_RECORD_ID] INNER JOIN SAOPQT ON SAOPQT.[QUOTE_RECORD_ID] = SAQTRV.[QUOTE_RECORD_ID]  AND SAQTRV.ACTIVE = 'True' "
                                                + str(where)
                                                + ") m where m.ROW BETWEEN "
                                                + str(Page_start)
                                                + " and "
                                                + str(Page_End)
                                                + " "
                                            )
                                            QueryCountStr = (
                                                "select rowcnt= count(*)  from " + PRIMARY_OBJECT_NAMes + " INNER JOIN SAQTRV ON  SAQTMT.[MASTER_TABLE_QUOTE_RECORD_ID] = SAQTRV.[QUOTE_RECORD_ID] INNER JOIN SAOPQT ON SAOPQT.[QUOTE_RECORD_ID] = SAQTRV.[QUOTE_RECORD_ID]  AND SAQTRV.ACTIVE = 'True' " + str(where)
                                            )    
                                            Trace.Write('## QueryStr--->'+str(QueryStr))
                                        ##A055S000P01-8871 Code ends..
                                        else:
                                            QueryStr = (
                                                "select top "
                                                + PerPage
                                                + " * from (select ROW_NUMBER() OVER("
                                                + objh_column
                                                + ") AS ROW, "
                                                + str(tot_names)
                                                + " from "
                                                + PRIMARY_OBJECT_NAMes
                                                + " (nolock) m "
                                                + str(where)
                                                + " ) S where S.ROW BETWEEN "
                                                + str(Page_start)
                                                + " and "
                                                + str(Page_End)
                                            )
                                            # Trace.Write(" SEARCH @@@707 select top "
                                            #     + PerPage
                                            #     + " * from (select ROW_NUMBER() OVER("
                                            #     + objh_column
                                            #     + ") AS ROW, "
                                            #     + str(tot_names)
                                            #     + " from "
                                            #     + PRIMARY_OBJECT_NAMes
                                            #     + " (nolock) m "
                                            #     + str(where)
                                            #     + " ) S where S.ROW BETWEEN "
                                            #     + str(Page_start)
                                            #     + " and "
                                            #     + str(Page_End))
                                            QueryCountStr = (
                                                "select rowcnt= count(*)  from " + PRIMARY_OBJECT_NAMes + " (nolock) " + str(where)
                                            )
                                    Trace.Write("Line no: 885 => {}".format(str(QueryCountStr)))
                                    QueryCountOBJ = Sql.GetFirst(QueryCountStr)
                                    if QueryCountOBJ is not None:
                                        QueryCount = QueryCountOBJ.rowcnt
                                except:

                                    if PageInform != "":
                                        Trace.Write("##At line 968")
                                        QueryStr = (
                                            "select TOP "
                                            + str(PerPage)
                                            + " "
                                            + str(tot_names)
                                            + " from (select ROW_NUMBER() OVER("
                                            + str(objh_column)
                                            + ") AS ROW, * from "
                                            + PRIMARY_OBJECT_NAMes
                                            + " (nolock) "
                                            + str(where)
                                            + ") m where m.ROW BETWEEN "
                                            + str(Page_start)
                                            + " and "
                                            + str(Page_End)
                                            + ""
                                        )
                                    else:
                                        Trace.Write("##At line 986")
                                        QueryStr = (
                                            "select TOP "
                                            + str(PerPage)
                                            + " "
                                            + str(tot_names)
                                            + " from "
                                            + PRIMARY_OBJECT_NAMes
                                            + " (nolock) "
                                            + str(where)
                                        )
                                    QueryCountStr = (
                                        "select rowcnt = count(*)  from "
                                        + str(sql.PRIMARY_OBJECT_NAME)
                                        + " (nolock) "
                                        + str(where)
                                    )
                                    Trace.Write("Line no: 925 => {}".format(str(QueryCountStr)))
                                    QueryCountOBJ = Query = Sql.GetFirst(QueryCountStr)
                                    if QueryCountOBJ is not None:
                                        QueryCount = QueryCountOBJ.rowcnt
                            else:
                                try:

                                    if PageInform != "":
                                        if str(x_tabs) == "Profiles" and str(current_prod) == "SYSTEM ADMIN":
                                            QueryStr = (
                                                "select * from (select ROW_NUMBER() OVER(ORDER BY permission_id ASC) AS ROW, [SYSTEM_ID],[permission_name],[permission_description],[permission_id] from cpq_permissions (nolock) WHERE 1=1 and permission_type = '0') m where m.ROW BETWEEN "
                                                + str(Page_start)
                                                + " and "
                                                + str(Page_End)
                                                + ""
                                            )

                                        else:
                                            ##A055S000P01-8871 Code starts..
                                            Trace.Write("flag__J_1 "+str(flag) + " x_tabs"+str(x_tabs))
                                            if flag == 0 and (str(x_tabs) == 'Quotes' or str(x_tabs) == 'Contracts'):
                                                where += " AND SAQTMT.CPQTABLEENTRYADDEDBY = '{}' ".format(User.UserName)
                                                if "CONTRACT_VALID_FROM" in str(where):
                                                    where = str(where).replace("CONTRACT_VALID_FROM","SAQTRV.CONTRACT_VALID_FROM")
                                                if "CONTRACT_VALID_TO" in str(where):
                                                    where = str(where).replace("CONTRACT_VALID_TO","SAQTRV.CONTRACT_VALID_TO") 
                                                if "SAQTRV.SAQTRV.CONTRACT_VALID_FROM" in str(where):
                                                    where = str(where).replace("SAQTRV.SAQTRV.CONTRACT_VALID_FROM","SAQTRV.CONTRACT_VALID_FROM")
                                                if "SAQTRV.SAQTRV.CONTRACT_VALID_TO" in str(where):
                                                    where = str(where).replace("SAQTRV.SAQTRV.CONTRACT_VALID_TO","SAQTRV.CONTRACT_VALID_TO")     
                                                QueryStr = (
                                                "select * from (select ROW_NUMBER() OVER(ORDER BY SAQTMT.CpqTableEntryId DESC) AS ROW, SAQTMT.[QUOTE_TYPE],SAQTMT.[SALE_TYPE],SAQTRV.[QUOTE_ID],SAQTMT.[QUOTE_STATUS],SAQTMT.[MASTER_TABLE_QUOTE_RECORD_ID],SAQTMT.[ACCOUNT_ID],SAQTMT.[ACCOUNT_NAME],SAQTMT.[ACCOUNT_RECORD_ID],SAQTMT.[OWNER_NAME],SAQTMT.[QTEREV_RECORD_ID],SAQTRV.[QTEREV_ID],SAQTRV.[SALESORG_ID],SAQTRV.[REVISION_STATUS],SAQTRV.[REVISION_DESCRIPTION],SAOPQT.[OPPORTUNITY_NAME],CONVERT(VARCHAR(10),SAQTRV.CONTRACT_VALID_FROM,101) AS [CONTRACT_VALID_FROM],CONVERT(VARCHAR(10),SAQTRV.CONTRACT_VALID_TO,101) AS [CONTRACT_VALID_TO]  from SAQTMT INNER JOIN SAQTRV ON  SAQTMT.[MASTER_TABLE_QUOTE_RECORD_ID] = SAQTRV.[QUOTE_RECORD_ID] INNER JOIN SAOPQT ON SAOPQT.[QUOTE_RECORD_ID] = SAQTRV.[QUOTE_RECORD_ID] AND SAQTRV.ACTIVE = 'True'"
                                                + str(where)
                                                + ") m where m.ROW BETWEEN "
                                                + str(Page_start)
                                                + " and "
                                                + str(Page_End)
                                                + " "
                                            )
                                            elif flag == 1 and (str(x_tabs) == 'Quotes'):
                                                Trace.Write("flag11====")
                                                #where += " AND QT.CPQTABLEENTRYADDEDBY = '{}' ".format(User.UserName)
                                                if "CONTRACT_VALID_FROM" in str(where):
                                                    where = str(where).replace("CONTRACT_VALID_FROM","SAQTRV.CONTRACT_VALID_FROM")
                                                if "CONTRACT_VALID_TO" in str(where):
                                                    where = str(where).replace("CONTRACT_VALID_TO","SAQTRV.CONTRACT_VALID_TO")
                                                if "SAQTRV.SAQTRV.CONTRACT_VALID_FROM" in str(where):
                                                    where = str(where).replace("SAQTRV.SAQTRV.CONTRACT_VALID_FROM","SAQTRV.CONTRACT_VALID_FROM")
                                                if "SAQTRV.SAQTRV.CONTRACT_VALID_TO" in str(where):
                                                    where = str(where).replace("SAQTRV.SAQTRV.CONTRACT_VALID_TO","SAQTRV.CONTRACT_VALID_TO")    
                                                QueryStr = (
                                                "select * from (select ROW_NUMBER() OVER(ORDER BY SAQTMT.CpqTableEntryId DESC) AS ROW, SAQTMT.[QUOTE_TYPE],SAQTMT.[SALE_TYPE],SAQTRV.[QUOTE_ID],SAQTMT.[QUOTE_STATUS],SAQTMT.[MASTER_TABLE_QUOTE_RECORD_ID],SAQTMT.[ACCOUNT_ID],SAQTMT.[ACCOUNT_NAME],SAQTMT.[ACCOUNT_RECORD_ID],SAQTMT.[OWNER_NAME],SAQTMT.[QTEREV_RECORD_ID],SAQTRV.[QTEREV_ID],SAQTRV.[SALESORG_ID],SAQTRV.[REVISION_STATUS],SAQTRV.[REVISION_DESCRIPTION],SAOPQT.[OPPORTUNITY_NAME],CONVERT(VARCHAR(10),SAQTRV.CONTRACT_VALID_FROM,101) AS [CONTRACT_VALID_FROM],CONVERT(VARCHAR(10),SAQTRV.CONTRACT_VALID_TO,101) AS [CONTRACT_VALID_TO]  from SAQTMT INNER JOIN SAQTRV ON  SAQTMT.[MASTER_TABLE_QUOTE_RECORD_ID] = SAQTRV.[QUOTE_RECORD_ID] INNER JOIN SAOPQT ON SAOPQT.[QUOTE_RECORD_ID] = SAQTRV.[QUOTE_RECORD_ID] AND SAQTRV.ACTIVE = 'True' "
                                                + str(where)
                                                + ") m where m.ROW BETWEEN "
                                                + str(Page_start)
                                                + " and "
                                                + str(Page_End)
                                                + " "
                                            )
                                                Trace.Write("QueryStr---->"+str(QueryStr))
                                            elif flag == 3 and (str(x_tabs) == 'Quotes' or str(x_tabs) == 'Contracts'):
                                                where += " AND ACAPTX.APPROVAL_RECIPIENT_RECORD_ID = '" + str(User.Id) + "' AND SAQTMT.CPQTABLEENTRYADDEDBY = '{}' AND SAQTRV.REVISION_STATUS = 'WAITING FOR APPROVAL' AND ACAPTX.ARCHIVED = 'False' ".format(User.UserName)
                                                if "CONTRACT_VALID_FROM" in str(where):
                                                    where = str(where).replace("CONTRACT_VALID_FROM","SAQTRV.CONTRACT_VALID_FROM")
                                                if "CONTRACT_VALID_TO" in str(where):
                                                    where = str(where).replace("CONTRACT_VALID_TO","SAQTRV.CONTRACT_VALID_TO")
                                                if "SAQTRV.SAQTRV.CONTRACT_VALID_FROM" in str(where):
                                                    where = str(where).replace("SAQTRV.SAQTRV.CONTRACT_VALID_FROM","SAQTRV.CONTRACT_VALID_FROM")
                                                if "SAQTRV.SAQTRV.CONTRACT_VALID_TO" in str(where):
                                                    where = str(where).replace("SAQTRV.SAQTRV.CONTRACT_VALID_TO","SAQTRV.CONTRACT_VALID_TO")    
                                                QueryStr = (
                                                "select * from (select ROW_NUMBER() OVER(ORDER BY SAQTMT.CpqTableEntryId DESC) AS ROW, SAQTMT.[QUOTE_TYPE],SAQTMT.[SALE_TYPE],SAQTRV.[QUOTE_ID],SAQTMT.[QUOTE_STATUS],SAQTMT.[MASTER_TABLE_QUOTE_RECORD_ID],SAQTMT.[ACCOUNT_ID],SAQTMT.[ACCOUNT_NAME],SAQTMT.[ACCOUNT_RECORD_ID],SAQTMT.[OWNER_NAME],SAQTMT.[QTEREV_RECORD_ID],SAQTRV.[QTEREV_ID],SAQTRV.[SALESORG_ID],SAQTRV.[REVISION_STATUS],SAQTRV.[REVISION_DESCRIPTION],SAOPQT.[OPPORTUNITY_NAME],CONVERT(VARCHAR(10),SAQTRV.CONTRACT_VALID_FROM,101) AS [CONTRACT_VALID_FROM],CONVERT(VARCHAR(10),SAQTRV.CONTRACT_VALID_TO,101) AS [CONTRACT_VALID_TO]  from SAQTMT INNER JOIN SAQTRV ON  SAQTMT.[MASTER_TABLE_QUOTE_RECORD_ID] = SAQTRV.[QUOTE_RECORD_ID] INNER JOIN SAOPQT ON SAOPQT.[QUOTE_RECORD_ID] = SAQTRV.[QUOTE_RECORD_ID] INNER JOIN ACAPTX ON ACAPTX.APRTRXOBJ_ID = SAQTRV.[QUOTE_ID] AND SAQTRV.ACTIVE = 'True'"
                                                + str(where)
                                                + ") m where m.ROW BETWEEN "
                                                + str(Page_start)
                                                + " and "
                                                + str(Page_End)
                                                + " "
                                            )    
                                            ##A055S000P01-8871 Code ends..    
                                            elif flag == 0 and (str(x_tabs) == 'My Approvals Queue'):
                                                where += " AND APPROVALSTATUS = 'REQUESTED' AND ARCHIVED = 0 "
                                                QueryStr = (
                                                "select * from (select ROW_NUMBER() OVER("
                                                + str(objh_column)
                                                + ") AS ROW, "
                                                + str(tot_names)
                                                + " from "
                                                + PRIMARY_OBJECT_NAMes
                                                + " (nolock) "
                                                + str(where)
                                                + ") m where m.ROW BETWEEN "
                                                + str(Page_start)
                                                + " and "
                                                + str(Page_End)
                                                + " "
                                            )
                                            elif flag == 2 and (str(x_tabs) == 'My Approvals Queue'):
                                                where += " AND APPROVALSTATUS NOT IN ('REQUESTED') "
                                                QueryStr = (
                                                "select * from (select ROW_NUMBER() OVER("
                                                + str(objh_column)
                                                + ") AS ROW, "
                                                + str(tot_names)
                                                + " from "
                                                + PRIMARY_OBJECT_NAMes
                                                + " (nolock) "
                                                + str(where)
                                                + ") m where m.ROW BETWEEN "
                                                + str(Page_start)
                                                + " and "
                                                + str(Page_End)
                                                + " "
                                            )
                                            elif flag == 1 and (str(x_tabs) == 'My Approvals Queue'):
                                                where += " AND APPROVALSTATUS IN ('APPROVED','REJECTED') "
                                                QueryStr = (
                                                "select * from (select ROW_NUMBER() OVER("
                                                + str(objh_column)
                                                + ") AS ROW, "
                                                + str(tot_names)
                                                + " from "
                                                + PRIMARY_OBJECT_NAMes
                                                + " (nolock) "
                                                + str(where)
                                                + ") m where m.ROW BETWEEN "
                                                + str(Page_start)
                                                + " and "
                                                + str(Page_End)
                                                + " "
                                            )
                                            # elif flag == 3 and str(x_tabs) == 'Quotes':
                                            #     where = ""
                                                
                                                """GetChainList = Sql.GetList(
                                                "SELECT * FROM ACAPTX WHERE APPROVAL_RECIPIENT_RECORD_ID = '" + str(User.Id) + "' and APPROVALSTATUS = 'APPROVED'"
                                                )
                                                GetList = []
                                                GetApprovalList = []
                                                conditionList = ''
                                                Approvalcond =''
                                                if GetChainList:
                                                    for chainlist in GetChainList:
                                                        ApprovalChain = str(chainlist.APRCHN_RECORD_ID)
                                                        ApprovalRecId = str(chainlist.APPROVAL_RECORD_ID)
                                                        GetApprovalList.append(ApprovalRecId)
                                                        if ApprovalChain not in GetList:
                                                            GetList.append(ApprovalChain)
                                                    conditionList = str(GetList).replace("[", "").replace("]", "")
                                                    Approvalcond = str(GetApprovalList).replace("[", "").replace("]", "")
                                                    
                                                    
                                                if conditionList == '':
                                                    conditionList = 'NULL'
                                                if Approvalcond == '':
                                                    Approvalcond = 'NULL'
                                                where += (
                                                " WHERE ACAPMA.APRCHN_RECORD_ID in ("
                                                + str(conditionList)
                                                + ") AND ACAPMA.APPROVAL_RECORD_ID in ("
                                                + str(Approvalcond)
                                                + ") AND ACAPMA.APROBJ_LABEL = 'Quote'"
                                                )
                                                #where += "AND CpqEntryTableEntryId = ''"
                                                objh_column = "ORDER BY SAQTMT.CpqTableEntryId DESC"
                                                
                                                QueryStr = (
                                                "select * from (select ROW_NUMBER() OVER("
                                                + str(objh_column)
                                                + ") AS ROW, "
                                                + str(tot_names)
                                                + " from "
                                                + PRIMARY_OBJECT_NAMes
                                                + "  JOIN ACAPMA (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = ACAPMA.APRTRXOBJ_RECORD_ID"
                                                + str(where)
                                                + ") m where m.ROW BETWEEN "
                                                + str(Page_start)
                                                + " and "
                                                + str(Page_End)
                                                + " "
                                                )"""
                                                #PRIMARY_OBJECT_NAMes += " JOIN ACAPMA (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = ACAPMA.APRTRXOBJ_RECORD_ID "
                                                #where +=  " WHERE ACAPTX.APPROVAL_RECIPIENT_RECORD_ID = '" + str(User.Id) + "' and QUOTE_STATUS = 'WAITING FOR APPROVAL' AND ACAPTX.ARCHIVED = 0"
                                                
                                                #fetch_next=(int(Page_End)-int(Page_start))+1
                                                
                                                # QueryStr = ("select DISTINCT [QUOTE_TYPE], [SALE_TYPE], [QUOTE_ID], [QUOTE_NAME], [QUOTE_STATUS], [MASTER_TABLE_QUOTE_RECORD_ID], [ACCOUNT_NAME], CONVERT(VARCHAR(10), CONTRACT_VALID_FROM, 101) AS [CONTRACT_VALID_FROM], CONVERT(VARCHAR(10), CONTRACT_VALID_TO, 101) AS [CONTRACT_VALID_TO] from SAQTMT JOIN ACAPTX (NOLOCK) ON SAQTMT.QUOTE_ID = ACAPTX.APRTRXOBJ_ID WHERE ACAPTX.APPROVAL_RECIPIENT_RECORD_ID = '" + str(User.Id) + "' and QUOTE_STATUS = 'WAITING FOR APPROVAL' AND ACAPTX.ARCHIVED = 0 ORDER BY QUOTE_ID DESC OFFSET "+str(Page_start-1)+" ROWS FETCH NEXT "+str(fetch_next)+" ROWS ONLY")
                                                '''QueryStr = ("select DISTINCT MASTER_TABLE_QUOTE_RECORD_ID, QUOTE_TYPE, QUOTE_ID, SALE_TYPE, QUOTE_NAME, QUOTE_STATUS, ACCOUNT_NAME,CONTRACT_VALID_FROM,CONTRACT_VALID_TO from (select ROW_NUMBER() OVER(ORDER BY SAQTMT.QUOTE_ID DESC) AS ROW, [QUOTE_TYPE],[SALE_TYPE],[QUOTE_ID],[QUOTE_NAME],[QUOTE_STATUS],[MASTER_TABLE_QUOTE_RECORD_ID],[ACCOUNT_NAME],CONVERT(VARCHAR(10),CONTRACT_VALID_FROM,101) AS [CONTRACT_VALID_FROM],CONVERT(VARCHAR(10),CONTRACT_VALID_TO,101) AS [CONTRACT_VALID_TO],ACAPTX.APPROVAL_TRANSACTION_RECORD_ID as APPROVAL_TRANSACTION_RECORD_ID from SAQTMT  JOIN ACAPTX (NOLOCK) ON SAQTMT.QUOTE_ID = ACAPTX.APRTRXOBJ_ID WHERE ACAPTX.APPROVAL_RECIPIENT_RECORD_ID = '" + str(User.Id) + "' and QUOTE_STATUS = 'WAITING FOR APPROVAL' AND ACAPTX.ARCHIVED = 0) m where m.ROW BETWEEN '"+str(Page_start)+"' and '"+str(Page_End)+"'")'''
                                                '''QueryStr = (
                                                "select * from (select ROW_NUMBER() OVER("
                                                + str(objh_column)
                                                + ") AS ROW, "
                                                + str(tot_names)
                                                + " from "
                                                + PRIMARY_OBJECT_NAMes
                                                + "  JOIN ACAPTX (NOLOCK) ON SAQTMT.QUOTE_ID = ACAPTX.APRTRXOBJ_ID"
                                                + str(where)
                                                + ") m where m.ROW BETWEEN "
                                                + str(Page_start)
                                                + " and "
                                                + str(Page_End)
                                                + " "
                                                )'''
                                            else:
                                                
                                                QueryStr = (
                                                    "select * from (select ROW_NUMBER() OVER("
                                                    + str(objh_column)
                                                    + ") AS ROW, "
                                                    + str(tot_names)
                                                    + " from "
                                                    + PRIMARY_OBJECT_NAMes
                                                    + " (nolock) "
                                                    + str(where)
                                                    + ") m where m.ROW BETWEEN "
                                                    + str(Page_start)
                                                    + " and "
                                                    + str(Page_End)
                                                    + " "
                                                )
                                    else:
                                        Trace.Write("## At line 1186")
                                        QueryStr = (
                                            "select TOP  "
                                            + str(PerPage)
                                            + " "
                                            + str(tot_names)
                                            + " from "
                                            + PRIMARY_OBJECT_NAMes
                                            + " (nolock) "
                                            + str(where)
                                        )
                                    if str(x_tabs) == "Profiles" and str(current_prod) == "SYSTEM ADMIN":

                                        QueryCountOBJ = Sql.GetFirst(
                                            "select  rowcnt= count(*) from "
                                            + PRIMARY_OBJECT_NAMes
                                            + " (nolock) where 1=1 and permission_type = '0'"
                                        )
                                    #elif str(x_tabs) == 'Quotes' and flag == 3:
                                        
                                        #where +=  "WHERE ACAPTX.APPROVAL_RECIPIENT_RECORD_ID = '" + str(User.Id) + "' and ACAPTX.APPROVALSTATUS = 'REQUESTED' AND ACAPTX.ARCHIVED = 0 "
                                        
                                        #QueryCountOBJ = Sql.GetFirst("select count(DISTINCT SAQTMT.QUOTE_ID) as rowcnt from SAQTMT (NOLOCK) JOIN ACAPTX (NOLOCK) ON SAQTMT.QUOTE_ID = ACAPTX.APRTRXOBJ_ID WHERE ACAPTX.APPROVAL_RECIPIENT_RECORD_ID = '" + str(User.Id) + "' and QUOTE_STATUS = 'WAITING FOR APPROVAL' AND ACAPTX.ARCHIVED = 0")
                                        '''QueryCountOBJ = Sql.GetFirst(
                                            "select  rowcnt= count(*) from "
                                            + PRIMARY_OBJECT_NAMes
                                            + " JOIN ACAPTX (NOLOCK) ON SAQTMT.QUOTE_ID = ACAPTX.APRTRXOBJ_ID "
                                            + str(where)
                                        )'''
                                        
                                    # elif flag == 1 and (str(x_tabs) == 'Quotes' or str(x_tabs) == 'Contracts'):
                                    #     Trace.Write("flag22====")
                                    #     #where += " AND QT.CPQTABLEENTRYADDEDBY = '{}' ".format(User.UserName)
                                    #     QueryStr = (
                                    #             "select * from (select ROW_NUMBER() OVER(ORDER BY SAQTMT.CpqTableEntryId DESC) AS ROW, SAQTMT.[QUOTE_TYPE],SAQTMT.[SALE_TYPE],SAQTRV.[QUOTE_ID],SAQTMT.[QUOTE_STATUS],SAQTMT.[MASTER_TABLE_QUOTE_RECORD_ID],SAQTMT.[ACCOUNT_ID],SAQTMT.[ACCOUNT_NAME],SAQTMT.[ACCOUNT_RECORD_ID],SAQTMT.[OWNER_NAME],SAQTMT.[QTEREV_RECORD_ID],SAQTRV.[QTEREV_ID],SAQTRV.[SALESORG_ID],SAQTRV.[REVISION_STATUS],SAQTRV.[REVISION_DESCRIPTION],SAOPQT.[OPPORTUNITY_NAME],CONVERT(VARCHAR(10),SAQTRV.CONTRACT_VALID_FROM,101) AS [CONTRACT_VALID_FROM],CONVERT(VARCHAR(10),SAQTRV.CONTRACT_VALID_TO,101) AS [CONTRACT_VALID_TO]  from SAQTMT INNER JOIN SAQTRV ON  SAQTMT.[MASTER_TABLE_QUOTE_RECORD_ID] = SAQTRV.[QUOTE_RECORD_ID] INNER JOIN SAOPQT ON SAOPQT.[QUOTE_RECORD_ID] = SAQTRV.[QUOTE_RECORD_ID]"
                                    #             + str(where)
                                    #             + ") m where m.ROW BETWEEN "
                                    #             + str(Page_start)
                                    #             + " and "
                                    #             + str(Page_End)
                                    #             + " "
                                    #         )
                                
                                        # QueryCountOBJ = Sql.GetFirst(
                                        #     "select  rowcnt= count(*) from SAQTMT (nolock) QT JOIN SAQTRV(NOLOCK) RV ON RV.QUOTE_ID = QT.QUOTE_ID and RV.QUOTE_REVISION_RECORD_ID = QT.QTEREV_RECORD_ID JOIN SAOPPR(NOLOCK) OP on OP.SALESORG_ID = RV.SALESORG_ID " + str(where))
                                    #elif flag == 0 and (str(x_tabs) == 'Quotes' or str(x_tabs) == 'Contracts'):
                                    elif flag == 0 and x_tabs == 'Quotes':
                                        Trace.Write("x_tabs flag0 =>"+str(x_tabs)) 
                                        where += " AND SAQTMT.CPQTABLEENTRYADDEDBY = '{}' ".format(User.UserName)
                                        if "CONTRACT_VALID_FROM" in str(where):
                                            where = str(where).replace("CONTRACT_VALID_FROM","SAQTRV.CONTRACT_VALID_FROM")
                                        if "CONTRACT_VALID_TO" in str(where):
                                            where = str(where).replace("CONTRACT_VALID_TO","SAQTRV.CONTRACT_VALID_TO")
                                        if "SAQTRV.SAQTRV.CONTRACT_VALID_FROM" in str(where):
                                            where = str(where).replace("SAQTRV.SAQTRV.CONTRACT_VALID_FROM","SAQTRV.CONTRACT_VALID_FROM")
                                        if "SAQTRV.SAQTRV.CONTRACT_VALID_TO" in str(where):
                                            where = str(where).replace("SAQTRV.SAQTRV.CONTRACT_VALID_TO","SAQTRV.CONTRACT_VALID_TO")    
                                        QueryCountOBJ = Sql.GetFirst(
                                            "select rowcnt= count(*)  from " + PRIMARY_OBJECT_NAMes + " INNER JOIN SAQTRV ON  SAQTMT.[MASTER_TABLE_QUOTE_RECORD_ID] = SAQTRV.[QUOTE_RECORD_ID] INNER JOIN SAOPQT ON SAOPQT.[QUOTE_RECORD_ID] = SAQTRV.[QUOTE_RECORD_ID]  AND SAQTRV.ACTIVE = 'True' " + str(where)
                                        )
                                    #elif flag == 1 and (str(x_tabs) == 'Quotes' or str(x_tabs) == 'Contracts'):
                                    elif flag == 1 and x_tabs == 'Quotes':
                                        Trace.Write("x_tabs flag1 =>"+str(x_tabs))
                                        if "CONTRACT_VALID_FROM" in str(where):
                                            where = str(where).replace("CONTRACT_VALID_FROM","SAQTRV.CONTRACT_VALID_FROM")
                                        if "CONTRACT_VALID_TO" in str(where):
                                            where = str(where).replace("CONTRACT_VALID_TO","SAQTRV.CONTRACT_VALID_TO")
                                        if "SAQTRV.SAQTRV.CONTRACT_VALID_FROM" in str(where):
                                            where = str(where).replace("SAQTRV.SAQTRV.CONTRACT_VALID_FROM","SAQTRV.CONTRACT_VALID_FROM")
                                        if "SAQTRV.SAQTRV.CONTRACT_VALID_TO" in str(where):
                                            where = str(where).replace("SAQTRV.SAQTRV.CONTRACT_VALID_TO","SAQTRV.CONTRACT_VALID_TO")    
                                        QueryCountOBJ = Sql.GetFirst(
                                            "select rowcnt= count(*)  from " + PRIMARY_OBJECT_NAMes + " INNER JOIN SAQTRV ON  SAQTMT.[MASTER_TABLE_QUOTE_RECORD_ID] = SAQTRV.[QUOTE_RECORD_ID] INNER JOIN SAOPQT ON SAOPQT.[QUOTE_RECORD_ID] = SAQTRV.[QUOTE_RECORD_ID]  AND SAQTRV.ACTIVE = 'True' " + str(where)
                                        )
                                    elif flag == 3 and x_tabs == 'Quotes':
                                        Trace.Write("x_tabs flag0 =>"+str(x_tabs))
                                        if "CONTRACT_VALID_FROM" in str(where):
                                            where = str(where).replace("CONTRACT_VALID_FROM","SAQTRV.CONTRACT_VALID_FROM")
                                        if "CONTRACT_VALID_TO" in str(where):
                                            where = str(where).replace("CONTRACT_VALID_TO","SAQTRV.CONTRACT_VALID_TO")
                                        if "SAQTRV.SAQTRV.CONTRACT_VALID_FROM" in str(where):
                                            where = str(where).replace("SAQTRV.SAQTRV.CONTRACT_VALID_FROM","SAQTRV.CONTRACT_VALID_FROM")
                                        if "SAQTRV.SAQTRV.CONTRACT_VALID_TO" in str(where):
                                            where = str(where).replace("SAQTRV.SAQTRV.CONTRACT_VALID_TO","SAQTRV.CONTRACT_VALID_TO")                                   
                                        QueryCountOBJ = Sql.GetFirst(
                                            "select rowcnt= count(*)  from " + PRIMARY_OBJECT_NAMes + " INNER JOIN SAQTRV ON  SAQTMT.[MASTER_TABLE_QUOTE_RECORD_ID] = SAQTRV.[QUOTE_RECORD_ID] INNER JOIN SAOPQT ON SAOPQT.[QUOTE_RECORD_ID] = SAQTRV.[QUOTE_RECORD_ID] INNER JOIN ACAPTX ON ACAPTX.APRTRXOBJ_ID = SAQTRV.[QUOTE_ID] AND SAQTRV.ACTIVE = 'True' " + str(where)
                                        )    
                                    else:
                                        QueryCountOBJ = Sql.GetFirst(
                                            "select  rowcnt= count(*) from "
                                            + PRIMARY_OBJECT_NAMes
                                            + " (nolock) "
                                            + str(where)
                                        )
                                    Trace.Write("Line no: 1138 => {}".format(str(QueryCountOBJ.rowcnt)))
                                    if QueryCountOBJ is not None:
                                        QueryCount = QueryCountOBJ.rowcnt
                                except:
                                    
                                    if PageInform != "":
                                        QueryStr = (
                                            "select * from ( select ROW_NUMBER() OVER("
                                            + str(objh_column)
                                            + ") AS ROW, * from "
                                            + PRIMARY_OBJECT_NAMes
                                            + " (nolock) "
                                            + str(where)
                                            + ") m where m.ROW BETWEEN "
                                            + str(Page_start)
                                            + " and "
                                            + str(Page_End)
                                            + ""
                                        )
                                    else:
                                        QueryStr = (
                                            " select TOP  "
                                            + str(PerPage)
                                            + "  * from "
                                            + str(PRIMARY_OBJECT_NAMes)
                                            + " (nolock) "
                                            + str(where)
                                        )

                                    QueryCountOBJ = Sql.GetFirst(
                                        "select  rowcnt= count(*)  from " + PRIMARY_OBJECT_NAMes + " (nolock) " + str(where)
                                    )
                                    Trace.Write("Line no: 1170 => {}".format(str(QueryCountOBJ)))
                                    if QueryCountOBJ is not None:
                                        QueryCount = QueryCountOBJ.rowcnt
                                                                
                            Query = Sql.GetList(QueryStr)
                            ArrayErpHide = []
                            try:
                                Product.SetGlobal("ArrayErpHide", str(ArrayErpHide))
                            except:
                                Trace.Write("SetGlobal not defined")
                            X_NameListS = list(NAME)[1]
                            table_header += table
                            table_header_new += table_new
                            TestES = [ikj for ikj in NameListS]
                            table_header += action_table_header
                            table_header_new += action_table_header_new
                            table_header += select_table_header
                            table_header_new += select_table_header_new
                            for ES in NAME:
                                Es_k = str(NameListS.get(ES))
                                
                                ESK_k = str(NameListSK.get(ES))
                                
                                ES = str(ES)
                                if ESK_k == "CHECKBOX" or ESK_k == "DATE":
                                    align = center_align
                                    
                                elif ESK_k == "NUMBER" or ESK_k == "CURRENCY":
                                    align = right_align
                                    
                                elif Es_k.upper() == "DISPLAY DECIMAL PLACES" or ESK_k.upper() == "ROUNDING DECIMAL PLACES":
                                    align = right_align
                                    Trace.Write("1204----------------------------------------")    
                                else:
                                    align = left_align
                                if Es_k.upper() == "NONE":
                                    table_header += record_id_table_header.format(align_param=align)
                                    table_header_new += record_id_table_header.format(align_param=align)
                                else:
                                    if Es_k.upper() == "ACTIVE":

                                        table_header += center_align_table_header.format(
                                            Es_k_upper_param=Es_k.upper(), ES_param=ES, Es_k_param=Es_k
                                        )
                                        Trace.Write("Center"+str(table_header))
                                    elif Es_k.upper() == "DISPLAY_ORDER" and tab_name == "Apps":
                                        Trace.Write("656----------------------------------------")
                                    elif Es_k.upper() == "DISPLAY DECIMAL PLACES":
                                        Trace.Write("1220---------------------------------------")
                                        table_header += right_align_table_header.format(
                                            Es_k_upper_param=Es_k.upper(), ES_param=ES, Es_k_param=Es_k
                                        )
                                        Trace.Write(table_header)
                                    else:
                                        var_class = (
                                            'class="text-right"'
                                            if current_prod == "SYSTEM ADMIN" and str(ES) == "DISPLAY_ORDER"
                                            else ""
                                        )
                                        table_header += right_left_align_table_header.format(
                                            ES_param=ES, align_param=align, Es_k_param=Es_k, var_class=var_class
                                        )
                                        table_header_new += right_left_align_table_header.format(
                                            ES_param=ES, align_param=align, Es_k_param=Es_k, var_class=var_class
                                        )

                            table_header += table_head_body_tail
                            table_header_new += table_head_tail
                            filter_control_function = ""
                            onchange_filtercontrol_function = ""
                            values_list = ""
                            table_id = "FULLTABLELOAD"
                            for invs in NAME:
                                table_ids = table_id_starts_with + table_id
                                filter_clas = table_id_filter_class.format(table_id_param=table_id) + invs

                                if invs == "SYMBOL" and PRIMARY_OBJECT_NAMes == "PRCURR":

                                    values_list += symbol_values_list.format(filter_class_param=filter_clas)
                                else:
                                    values_list += non_symbol_values_list.format(
                                        invs_param=invs, filter_class_param=filter_clas
                                    )
                                values_list += attributes_values_list.format(invs_param=invs)
                            filter_class = action_filter_class_starts_with + table_id

                            filter_control_function += (
                                '$("'
                                + filter_class
                                + '").click( function(){ var table_id = $(this).closest("table").attr("id"); var a_list = '
                                + str(NAME)
                                + "; ATTRIBUTE_VALUEList = []; "
                                + str(values_list)
                                + ' SortColumn = localStorage.getItem("SortColumn"); SortColumnOrder = localStorage.getItem("SortColumnOrder"); PerPage = $("#PageCountValue").val(); PageInform = "1___" + PerPage + "___" + PerPage; var active_subtab = $(".subtab_inner li.active").attr("id");if(active_subtab == "subtab_list1"){flag = 0}else if(active_subtab == "subtab_list3"){flag = 3}else{flag = 1}cpq.server.executeScript("SYMCTABSGD", {\'ACTION\': \'SORTING\', \'A_Keys\': a_list, \'A_Values\': ATTRIBUTE_VALUEList, "SortColumn":SortColumn, "SortColumnOrder": SortColumnOrder, "PerPage": PerPage, "PageInform": PageInform,"FLAG":flag,"CurrentTab": $("ul#carttabs_head li.active a span").text()}, function(dataset) { datas1 = dataset[1]; datas5 = dataset[5]; datas6 = dataset[6]; datas12 = dataset[12];  try { $("'
                                + str(table_ids)
                                + '").bootstrapTable("load", datas1 ); var uncheckid=localStorage.getItem("uncheckdata"); if(uncheckid!="" ){ $("#"+uncheckid+" > span").removeAttr("class");$("#"+uncheckid+" > span").attr("class","jqx-listitem-state-normal jqx-item checkboxes jqx-rc-all");localStorage.getItem("uncheckdata",""); }  eval(datas5);  } catch(err) {  $("'
                                + str(table_ids)
                                + "\").bootstrapTable(\"load\", datas1 ); eval(datas5);  } if (document.getElementById('totalItemCount')) { document.getElementById('totalItemCount').innerHTML = datas6; } if (document.getElementById('NumberofItem')) { document.getElementById('NumberofItem').innerHTML = dataset[11]; } if(document.getElementById('page_count')) { document.getElementById('page_count').innerHTML = '1'; }    $(\"#PageCountValue\").val(dataset[12]);norcordsget();filter_search_click();}); fullTableListGridWidth(); });"
                            )

                            if str(tab_name) not in ("Roles","My Approvals Queue","Quotes","Team Approvals Queue","Contracts"):
                                
                                a_txt = '<div class="btn-group dropdown"><div class="dropdown" id="ctr_drop"><i data-toggle="dropdown" class="fa fa-sort-desc dropdown-toggle" aria-expanded="false"></i><ul class="dropdown-menu left" aria-labelledby="dropdownMenuButton"><li class="view_list"><a class="dropdown-item" href="#" onclick="Material_view_obj(this)">VIEW</a></li>'

                            elif str(tab_name) == "Roles" and str(current_prod) == "SYSTEM ADMIN":
                                a_txt = '<div class="btn-group dropdown"><div class="dropdown" id="ctr_drop"><i data-toggle="dropdown" class="fa fa-sort-desc dropdown-toggle" aria-expanded="false"></i><ul class="dropdown-menu left" aria-labelledby="dropdownMenuButton"><li class="view_list"><a class="dropdown-item" href="#" onclick="Roles_View(this)">VIEW</a></li>'
                            ## Showing approve/reject in list grid
                            elif (str(tab_name).upper() in ("MY APPROVAL QUEUE","MY APPROVALS QUEUE","QUOTES","TEAM APPROVAL QUEUE","TEAM APPROVALS QUEUE")):
                                
                                if (str(tab_name).upper() in ("MY APPROVAL QUEUE","TEAM APPROVAL QUEUE") and flag == 0) or (str(tab_name).upper() == "QUOTES" and flag == 3):
                                    
                                    a_txt = '<div class="btn-group dropdown"><div class="dropdown" id="ctr_drop"><i data-toggle="dropdown" class="fa fa-sort-desc dropdown-toggle" aria-expanded="false"></i><ul class="dropdown-menu left" aria-labelledby="dropdownMenuButton"><li class="view_list"><a class="dropdown-item" href="#" onclick="Material_view_obj(this)">VIEW</a></li><li class="view_list"><a id= class="dropdown-item grid_approval" href="#" data-target="#preview_approval" onclick="approve_request(this)" data-toggle="modal">APPROVE</a></li><li class="view_list"><a id= class="dropdown-item grid_approval" href="#" data-target="#preview_approval" onclick="reject_request(this)" data-toggle="modal">REJECT</a></li>'
                                else:
                                    a_txt = '<div class="btn-group dropdown"><div class="dropdown" id="ctr_drop"><i data-toggle="dropdown" class="fa fa-sort-desc dropdown-toggle" aria-expanded="false"></i><ul class="dropdown-menu left" aria-labelledby="dropdownMenuButton"><li class="view_list"><a class="dropdown-item" href="#" onclick="Material_view_obj(this)">VIEW</a></li>'
                            ##Showing approve/reject in list grid ends
                            elif (str(tab_name).upper() == "CONTRACTS" ):
                                
                                a_txt = '<div class="btn-group dropdown"><div class="dropdown" id="ctr_drop"><i data-toggle="dropdown" class="fa fa-sort-desc dropdown-toggle" aria-expanded="false"></i><ul class="dropdown-menu left" aria-labelledby="dropdownMenuButton"><li class="view_list"><a class="dropdown-item" href="#" onclick="gotquote_num_rev(this)">VIEW</a></li>'
                            else:
                                
                                a_txt = '<div class="btn-group dropdown"><div class="dropdown" id="ctr_drop"><i data-toggle="dropdown" class="fa fa-sort-desc dropdown-toggle" aria-expanded="false"></i><ul class="dropdown-menu left" aria-labelledby="dropdownMenuButton"><li class="view_list"><a class="dropdown-item" href="#" onclick="ErrorLog_View(this)">VIEW</a></li>'

                            section_obj = Sql.GetFirst(
                                "SELECT top 1 SYSECT.PRIMARY_OBJECT_RECORD_ID FROM SYSECT (NOLOCK) INNER JOIN SYPAGE (NOLOCK) ON SYSECT.PAGE_RECORD_ID = SYPAGE.RECORD_ID  WHERE SYSECT.SECTION_NAME = 'BASIC INFORMATION' and SYPAGE.TAB_NAME = '"
                                + str(tab_name)
                                + "' order by SYSECT.CpqTableEntryId"
                            )

                            

                            if section_obj is not None:

                                obj_ids = section_obj.PRIMARY_OBJECT_RECORD_ID
                                
                                #SYPROH Permissions start
                                # objsk_obj = Sql.GetFirst(
                                #     "SELECT P.CAN_ADD,S.CAN_CLONE, P.CAN_EDIT,P.CAN_DELETE FROM SYPROH P inner join SYOBJS S on S.OBJ_REC_ID = P.OBJECT_RECORD_ID inner join users_permissions up on up.permission_id = P.PROFILE_RECORD_ID WHERE S.NAME = 'Tab list' AND S.OBJ_REC_ID = '{0}' and P.VISIBLE = 1 and up.user_id='{1}'".format(
                                #         str(obj_ids), str(userid)
                                #     )
                                # )
                                #SYPROH Permissions end
                                objsk_obj = Sql.GetFirst(
                                    "SELECT S.CAN_ADD,S.CAN_CLONE, S.CAN_EDIT,S.CAN_DELETE FROM SYOBJH P inner join SYOBJS S on S.OBJ_REC_ID = P.RECORD_ID WHERE S.NAME = 'Tab list' AND S.OBJ_REC_ID = '{0}'".format(
                                        str(obj_ids)
                                    )
                                )

                                if objsk_obj is not None:
                                    
                                    if str(objsk_obj.CAN_EDIT).upper() == "TRUE":
                                        a_txt += '<li class="edit_list" style="display: block;"><a class="dropdown-item" href="#" id="editbtn" onclick="Material_edit_obj(this)">EDIT</a></li>'

                                    if str(tab_name) == "Apps":
                                        a_txt += '<li class="edit_list" style="display: block;"><a class="dropdown-item" href="#" id="Refreshbtn" onclick="RefreshOnchange(this)">REFRESH</a></li>'
                                    if str(tab_name) == "Apps":
                                        a_txt += '<li class="edit_list" style="display: block;"><a class="dropdown-item" href="#" id="Deploybtn" onclick="RefreshOnchange(this)">DEPLOY</a></li>'
                                    #if str(tab_name) == "Objects":
                                        #a_txt += '<li class="edit_list" style="display: block;"><a class="dropdown-item" href="#" id="Obj_Refreshbtn" onclick="Obj_RefreshOnchange(this)">REFRESH</a><li>'
                                    if str(tab_name) == "Objects":
                                        a_txt += '<li class="edit_list" style="display: block;"><a class="dropdown-item" href="#" id="REINDEX_BTN" onclick="obj_Reindex(this)">REINDEX</a><li>'
                                    if str(tab_name) == "Objects":
                                        a_txt += '<li class="edit_list" style="display: block;"><a class="dropdown-item" href="#" id="RECREATE_BTN" onclick="Obj_RefreshOnchange(this)">RECREATE</a><li>'
                                    if str(tab_name) == "Error Logs":
                                        a_txt += '<li class="edit_list" style="display: none;"><a class="dropdown-item" href="#" id="editbtn" onclick="ErrorLogopencreate(this)">EDIT</a></li>'

                                    if str(objsk_obj.CAN_DELETE).upper() == "TRUE":
                                        onclick = "CommonDelete(this, '" + str(PRIMARY_OBJECT_NAMes) + "', 'WARNING')"
                                        a_txt += (
                                            '<li class="delete_list"><a class="dropdown-item" href="#" id="deletebtn" onclick="'
                                            + str(onclick)
                                            + '" data-target="#cont_CommonModalDelete" data-toggle="modal">DELETE</a></li>'
                                        )

                                    elif str(objsk_obj.CAN_DELETE).upper() == "TRUE" and str(tab_name) == "Profiles":

                                        a_txt += '<li class="delete_list"><a class="dropdown-item" href="#" id="deletebtn" onclick="ProfileContainerDelete(this)">DELETE</a></li>'

                                    if str(objsk_obj.CAN_CLONE).upper() == "TRUE":
                                        a_txt += '<li class="clone_lists"><a class="dropdown-item" href="#" onclick="Material_clone_obj(this)">CLONE</a></li>'

                            a_txt += "</ul></div></div>"
                            
                            if Query is not None:
                                newRowDict = {}
                                newRowList = []
                                for data in Query:
                                    
                                    ##Showing approve/reject in list grid starts
                                    if (str(tab_name).upper() in ("MY APPROVAL QUEUE","TEAM APPROVAL QUEUE") and flag == 0) or (str(tab_name).upper() == "QUOTES" and flag == 3):
                                        try:
                                            a_txt = '''<div class="btn-group dropdown"><div class="dropdown" id="ctr_drop"><i data-toggle="dropdown" class="fa fa-sort-desc dropdown-toggle" aria-expanded="false"></i><ul class="dropdown-menu left" aria-labelledby="dropdownMenuButton"><li class="view_list"><a class="dropdown-item" href="#" onclick="Material_view_obj(this)">VIEW</a></li><li class="view_list"><a id="'''+str(data.APPROVAL_TRANSACTION_RECORD_ID)+'''" class="dropdown-item grid_approval" href="#" data-target="#preview_approval" onclick="approve_request(this)" data-toggle="modal">APPROVE</a></li><li class="view_list"><a id="'''+str(data.APPROVAL_TRANSACTION_RECORD_ID)+'''" class="dropdown-item grid_approval" href="#" data-target="#preview_approval" onclick="reject_request(this)" data-toggle="modal">REJECT</a></li></ul></div></div>'''
                                            
                                        except:
                                            a_txt = a_txt
                                    ##Showing approve/reject in list grid ends
                                    else:
                                        a_txt = a_txt
                                    newRowuple = {}
                                    newRow = {}
                                    
                                    newRow["ACTION"] = a_txt
                                    newRow["RECORD_ID"] = str(eval("data." + str(NAME[0])))
                                    newRow["SELECT"] = ""
                                    newRow["ACTION"] = a_txt
                                    for col_name in NAME:
                                        rowName = col_name.replace(" ", "_").upper()
                                        idval = ""
                                        tab_val = ""
                                        RECORD_ID = ""
                                        product_id = ""
                                        product_name = ""
                                        module_txt = ""
                                        product_num = ""
                                        qwe = ""
                                        try:
                                            Trace.Write("col_name111"+str(col_name))
                                            Trace.Write("col_name222"+str(lookup_disply_list))
                                            Trace.Write("col_name333"+str(checkbox_list))
                                            Trace.Write("col_name444"+str(currency_list))
                                            if col_name in lookup_disply_list:
                                                for key, value in lookup_list.items():
                                                    #Trace.Write("aaaa" + str(value))
                                                    if key == col_name:
                                                        # if tab_name == "Quotes":
                                                        #     Trace.Writ("QQQQ@@@")
                                                        #     lookup_obj = Sql.GetFirst(
                                                        #         "SELECT LOOKUP_OBJECT FROM  SYOBJD (NOLOCK) WHERE OBJECT_NAME IN ('SAQTMT','SAQTRV','SAOPPR')AND LOOKUP_API_NAME ='"
                                                        #         + str(key)
                                                        #         + "' AND DATA_TYPE = 'LOOKUP'"
                                                        #     )
                                                        # else:    
                                                        lookup_obj = Sql.GetFirst(
                                                            "SELECT LOOKUP_OBJECT FROM  SYOBJD (NOLOCK) WHERE OBJECT_NAME = '"
                                                            + PRIMARY_OBJECT_NAMes
                                                            + "' AND LOOKUP_API_NAME ='"
                                                            + str(key)
                                                            + "' AND DATA_TYPE = 'LOOKUP'"
                                                        )
                                                        lookup_val = str(lookup_obj.LOOKUP_OBJECT)
                                                        tab_obj = Sql.GetFirst(
                                                            "SELECT SYPAGE.TAB_NAME,SYPAGE.TAB_RECORD_ID FROM SYPAGE (nolock) join SYSECT (NOLOCK) on SYPAGE.RECORD_ID = SYSECT.PAGE_RECORD_ID WHERE SYSECT.PRIMARY_OBJECT_NAME='"
                                                            + str(lookup_val).strip()
                                                            + "'"
                                                        )
                                                        RECORD_ID = str(eval("data." + str(value)))
                                                        row_value = str(eval("data." + col_name))
                                                        gettooltip = Sql.GetFirst(
                                                            "select TOOLTIP_TEXT,ISNULL(TOOLTIP_TEXT, '') as tool from  SYOBJD (NOLOCK) where API_NAME = '{0}' and OBJECT_NAME = '{1}'".format(
                                                                col_name, PRIMARY_OBJECT_NAMes
                                                            )
                                                        )
                                                        if tab_obj is not None:
                                                            tab_val = str(tab_obj.TAB_NAME)
                                                            if gettooltip is not None and gettooltip.tool != "":
                                                                cur_tooltip = gettooltip.TOOLTIP_TEXT
                                                                gettooltipval = Sql.GetFirst(
                                                                    "select "
                                                                    + str(cur_tooltip)
                                                                    + " as val12 from "
                                                                    + str(PRIMARY_OBJECT_NAMes)
                                                                    + " where "
                                                                    + col_name
                                                                    + " = '{0}' ".format(qwe)
                                                                )
                                                                if tab_val in list_of_tabs:
                                                                    gettabvisibility = Sql.GetFirst("select VISIBLE FROM SYPRTB (NOLOCK) TB  INNER JOIN cpq_permissions (NOLOCK) cp ON cp.permission_id = TB.PROFILE_RECORD_ID INNER JOIN users_permissions (NOLOCK) up on up.permission_id = cp.permission_id where up.user_id = '"+str(userid)+"' and TB.TAB_ID = '"+str(tab_val.strip())+"'")
                                                                    idval = RECORD_ID + "|" + tab_val.strip()
                                                                    row_value = str(eval("data." + col_name))
                                                                    if gettabvisibility.VISIBLE == 1:
                                                                        newRow[rowName] = (
                                                                            "<a id='"
                                                                            + str(idval)
                                                                            + "'  class='cur_sty' onclick='Move_to_parent_obj(this)'><abbr id='"
                                                                            + str(row_value)
                                                                            + "' title='"
                                                                            + str(row_value)
                                                                            + "'>"
                                                                            + str(row_value)
                                                                            + "</abbr></a>"
                                                                        )
                                                                        
                                                                    else:
                                                                        newRow[rowName] = (
                                                                            "<abbr id='"
                                                                            + str(row_value)
                                                                            + "' title='"
                                                                            + str(row_value)
                                                                            + "'>"
                                                                            + str(row_value)
                                                                            + "</abbr>"
                                                                        )
                                                                        
                                                                else:
                                                                    product_name = Sql.GetFirst(
                                                                        "select APP_LABEL from SYTABS (NOLOCK) where RECORD_ID='"
                                                                        + str(tab_obj.TAB_RECORD_ID)
                                                                        + "'"
                                                                    )
                                                                    if product_name is not None:
                                                                        module_txt = str(product_name.APP_LABEL).strip()
                                                                        product_id = Sql.GetFirst(
                                                                            "select PRODUCT_ID from products (NOLOCK) where PRODUCT_NAME='"
                                                                            + str(module_txt)
                                                                            + "'"
                                                                        )
                                                                    if product_id != "" and product_id is not None:
                                                                        product_num = str(product_id.PRODUCT_ID)
                                                                        # gettabvisibility = Sql.GetFirst("select VISIBLE FROM SYPRTB (NOLOCK) TB  INNER JOIN cpq_permissions (NOLOCK) cp ON cp.permission_id = TB.PROFILE_RECORD_ID INNER JOIN users_permissions (NOLOCK) up on up.permission_id = cp.permission_id where up.user_id = '"+str(userid)+"' and TB.TAB_ID = '"+str(tab_val.strip())+"'")
                                                                        # gettabvisibility = Sql.GetFirst("select VISIBLE FROM SYPRTB (NOLOCK) TB  INNER JOIN cpq_permissions (NOLOCK) cp ON cp.permission_id = TB.PROFILE_RECORD_ID INNER JOIN users_permissions (NOLOCK) up on up.permission_id = cp.permission_id where up.user_id = '"+str(userid)+"' and TB.TAB_ID = '"+str(tab_val.strip())+"'")
                                                                        # if gettabvisibility.visible == 1:
                                                                        #     idval = RECORD_ID + "|" + tab_val
                                                                        #     newRow[rowName] = (
                                                                        #         "<a href='/Configurator.aspx?pid="
                                                                        #         + str(product_num)
                                                                        #         + "' id='"
                                                                        #         + str(idval)
                                                                        #         + "' class='cur_sty' onclick='Move_to_parent_obj(this)'><abbr id='"
                                                                        #         + str(row_value)
                                                                        #         + "' title='"
                                                                        #         + str(row_value)
                                                                        #         + "'>"
                                                                        #         + str(row_value)
                                                                        #         + "</abbr></a>"
                                                                        #     )
                                                                            
                                                                        # else:
                                                                        idval = RECORD_ID + "|" + tab_val
                                                                        newRow[rowName] = (
                                                                            "<abbr id='"
                                                                            + str(row_value)
                                                                            + "' title='"
                                                                            + str(row_value)
                                                                            + "'>"
                                                                            + str(row_value)
                                                                            + "</abbr>"
                                                                        )
                                                                            
                                                                    else:
                                                                        idval = RECORD_ID + "|" + lookup_val.strip()
                                                                        newRow[rowName] = (
                                                                            '<a href="#" id="'
                                                                            + idval
                                                                            + '" class="cur_sty" data-target="#cont_viewModalSection" onclick="cont_relatedlist_openview(this)" data-toggle="modal"><abbr id="'
                                                                            + str(row_value)
                                                                            + '" title="'
                                                                            + str(row_value)
                                                                            + '">'
                                                                            + str(row_value)
                                                                            + "</abbr></a>"
                                                                        )
                                                                        

                                                            else:
                                                                #hyperlink permissions start
                                                                # gettabvisibility = Sql.GetFirst("select VISIBLE FROM SYPRTB (NOLOCK) TB  INNER JOIN cpq_permissions (NOLOCK) cp ON cp.permission_id = TB.PROFILE_RECORD_ID INNER JOIN users_permissions (NOLOCK) up on up.permission_id = cp.permission_id where up.user_id = '"+str(userid)+"' and TB.TAB_ID = '"+str(tab_val.strip())+"'")
                                                                if tab_val in list_of_tabs:
                                                                    if 1=1:
                                                                        #Trace.Write('1420-gettabvisibility------'+str(gettabvisibility.VISIBLE))
                                                                        if 1 == 1:
                                                                            
                                                                            idval = RECORD_ID + "|" + tab_val.strip()
                                                                            row_value = str(eval("data." + col_name))
                                                                            newRow[rowName] = (
                                                                                "<a id='"
                                                                                + str(idval)
                                                                                + "'class='cur_sty' onclick='Move_to_parent_obj(this)'><abbr id='"
                                                                                + str(row_value)
                                                                                + "' title='"
                                                                                + str(row_value)
                                                                                + "'>"
                                                                                + str(row_value)
                                                                                + "</abbr></a>"
                                                                            )
                                                                            
                                                                        else:
                                                                            
                                                                            idval = RECORD_ID + "|" + tab_val.strip()
                                                                            row_value = str(eval("data." + col_name))
                                                                            newRow[rowName] = (
                                                                                "<abbr id='"
                                                                                + str(row_value)
                                                                                + "' title='"
                                                                                + str(row_value)
                                                                                + "'>"
                                                                                + str(row_value)
                                                                                + "</abbr>"
                                                                            )
                                                                            
                                                                    else:
                                                                        
                                                                        # gettabvisibility = Sql.GetFirst("select VISIBLE FROM SYPRTB (NOLOCK) TB  INNER JOIN cpq_permissions (NOLOCK) cp ON cp.permission_id = TB.PROFILE_RECORD_ID INNER JOIN users_permissions (NOLOCK) up on up.permission_id = cp.permission_id where up.user_id = '"+str(userid)+"' and TB.TAB_ID = '"+str(tab_val.strip())+"'")
                                                                        if 1 == 1:
                                                                            idval = RECORD_ID + "|" + tab_val.strip()
                                                                            row_value = str(eval("data." + col_name))
                                                                            newRow[rowName] = (
                                                                                "<a id='"
                                                                                + str(idval)
                                                                                + "'class='cur_sty' onclick='Move_to_parent_obj(this)'><abbr id='"
                                                                                + str(row_value)
                                                                                + "' title='"
                                                                                + str(row_value)
                                                                                + "'>"
                                                                                + str(row_value)
                                                                                + "</abbr></a>"
                                                                            )
                                                                            
                                                                        else:
                                                                            idval = RECORD_ID + "|" + tab_val.strip()
                                                                            row_value = str(eval("data." + col_name))
                                                                            newRow[rowName] = (
                                                                                "<abbr id='"
                                                                                + str(row_value)
                                                                                + "' title='"
                                                                                + str(row_value)
                                                                                + "'>"
                                                                                + str(row_value)
                                                                                + "</abbr>"
                                                                            )
                                                                            
                                                                else:
                                                                    product_name = Sql.GetFirst(
                                                                        "select APP_LABEL from SYTABS (NOLOCK) where RECORD_ID='"
                                                                        + str(tab_obj.TAB_RECORD_ID)
                                                                        + "'"
                                                                    )
                                                                    if product_name is not None:
                                                                        module_txt = str(product_name.APP_LABEL).strip()
                                                                        product_id = Sql.GetFirst(
                                                                            "select PRODUCT_ID from products (NOLOCK) where PRODUCT_NAME='"
                                                                            + str(module_txt)
                                                                            + "'"
                                                                        )
                                                                    if product_id != "" and product_id is not None:
                                                                        gettabvisibility = Sql.GetFirst("select VISIBLE FROM SYPRTB (NOLOCK) TB  INNER JOIN cpq_permissions (NOLOCK) cp ON cp.permission_id = TB.PROFILE_RECORD_ID INNER JOIN users_permissions (NOLOCK) up on up.permission_id = cp.permission_id where up.user_id = '"+str(userid)+"' and TB.TAB_ID = '"+str(tab_val.strip())+"'")
                                                                        if gettabvisibility.VISIBLE == 1:
                                                                            product_num = str(product_id.PRODUCT_ID)
                                                                            idval = RECORD_ID + "|" + tab_val
                                                                            newRow[rowName] = (
                                                                                "<a href='/Configurator.aspx?pid="
                                                                                + str(product_num)
                                                                                + "' id='"
                                                                                + str(idval)
                                                                                + "' class='cur_sty' onclick='Move_to_parent_obj(this)'><abbr id='"
                                                                                + str(row_value)
                                                                                + "' title='"
                                                                                + str(row_value)
                                                                                + "'>"
                                                                                + str(row_value)
                                                                                + "</abbr></a>"
                                                                            )
                                                                            
                                                                        else:
                                                                            product_num = str(product_id.PRODUCT_ID)
                                                                            idval = RECORD_ID + "|" + tab_val
                                                                            newRow[rowName] = (
                                                                                "<abbr id='"
                                                                                + str(row_value)
                                                                                + "' title='"
                                                                                + str(row_value)
                                                                                + "'>"
                                                                                + str(row_value)
                                                                                + "</abbr>"
                                                                            )
                                                                            
                                                                    else:
                                                                        idval = RECORD_ID + "|" + lookup_val.strip()
                                                                        newRow[rowName] = (
                                                                            '<a href="#" id="'
                                                                            + idval
                                                                            + '" class="cur_sty" data-target="#cont_viewModalSection" onclick="cont_relatedlist_openview(this)" data-toggle="modal"><abbr id="'
                                                                            + str(row_value)
                                                                            + '" title="'
                                                                            + str(row_value)
                                                                            + '">'
                                                                            + str(row_value)
                                                                            + "</abbr></a>"
                                                                        )
                                                                        
                                                        else:
                                                            idval = RECORD_ID + "|" + lookup_val.strip()
                                                            newRow[rowName] = (
                                                                '<a href="#" id="'
                                                                + idval
                                                                + '" class="cur_sty" data-target="#cont_viewModalSection" onclick="cont_relatedlist_openview(this)" data-toggle="modal"><abbr id="'
                                                                + str(row_value)
                                                                + '" title="'
                                                                + str(row_value)
                                                                + '">'
                                                                + str(row_value)
                                                                + "</abbr></a>"
                                                            )
                                                            
                                            elif col_name in checkbox_list:
                                                checkvalue = str(eval("data." + col_name))
                                                checked = ""
                                                if checkvalue.upper() == "TRUE":
                                                    checked = "checked"
                                                newRow[rowName] = (
                                                    "<input class='custom' type='checkbox' "
                                                    + str(checked)
                                                    + " disabled><span class='lbl'></span>"
                                                )
                                            elif col_name in currency_list:
                                                for col in currency_dict:
                                                    if col_name == str(col):
                                                        api_name = str(currency_dict[col])
                                                        qwe = str(eval("data." + str(api_name)))

                                                        price_decimal_obj = Sql.GetFirst(
                                                            "select DISPLAY_DECIMAL_PLACES,SYMBOL,CURRENCY from PRCURR (NOLOCK) where CURRENCY_RECORD_ID='"
                                                            + str(qwe)
                                                            + "'"
                                                        )
                                                        if price_decimal_obj is not None and len(price_decimal_obj) > 0:
                                                            curr_symbol = price_decimal_obj.CURRENCY
                                                            price_decimal = price_decimal_obj.DISPLAY_DECIMAL_PLACES
                                                            price_decimals = "." + str(price_decimal) + "f"
                                                            price_decimals = "." + str(price_decimal) + "f"
                                                            values = eval("data." + col_name)
                                                            values = eval("data." + col_name)
                                                            newRow[col] = (
                                                                str(format(float(values), price_decimals))
                                                                + " "
                                                                + curr_symbol
                                                            )

                                                        else:
                                                            newRow[col_name] = (
                                                                '<abbr id ="'
                                                                + str(qwe)
                                                                + '" title="'
                                                                + str(qwe)
                                                                + '">'
                                                                + str(eval("data." + col_name))
                                                                + "</abbr>"
                                                            )
                                            else:
                                                Trace.Write("Line no: 1688 => {}".format(str(PRIMARY_OBJECT_NAMes)))
                                                qwe = str(eval("data." + col_name))
                                                gettooltip = Sql.GetFirst(
                                                    "select TOOLTIP_TEXT,ISNULL(TOOLTIP_TEXT, '') as tool from  SYOBJD (NOLOCK) where API_NAME = '{0}' and OBJECT_NAME = '{1}'".format(
                                                        col_name, PRIMARY_OBJECT_NAMes
                                                    )
                                                )
                                                Trace.Write("Line no: 1695 => {}".format(str(gettooltip)))
                                                if gettooltip is not None and gettooltip.tool != "":
                                                    cur_tooltip = gettooltip.TOOLTIP_TEXT
                                                    gettooltipval = Sql.GetFirst(
                                                        "select "
                                                        + str(cur_tooltip)
                                                        + " as val12 from "
                                                        + str(PRIMARY_OBJECT_NAMes)
                                                        + " where "
                                                        + col_name
                                                        + " = '{0}' ".format(qwe)
                                                    )
                                                    if col_name == str(X_NameListS):
                                                        Trace.Write("Line No:1697"+col_name)
                                                        newRow[col_name] = (
                                                            '<a onclick="Material_view_obj(this)"><abbr id ="'
                                                            + qwe
                                                            + '" title="'
                                                            + qwe
                                                            + '">'
                                                            + qwe
                                                            + "</abbr> </a>"
                                                        )
                                                        

                                                    else:
                                                        newRow[col_name] = (
                                                            "<abbr id='"
                                                            + str(qwe)
                                                            + "' title='"
                                                            + str(qwe)
                                                            + "'>"
                                                            + str(eval("data." + col_name))
                                                            + "</abbr>"
                                                        )
                                                        
                                                else:
                                                    if col_name == str(X_NameListS):
                                                        Trace.Write("Line No:1721"+col_name)
                                                        if col_name == "APP_ID" or col_name == "VARIABLE_NAME":
                                                            newRow[col_name] = (
                                                                '<a onclick="Material_view_obj(this)"><abbr id ="'
                                                                + str(qwe)
                                                                + '" title="'
                                                                + str(qwe)
                                                                + '">'
                                                                + str(qwe)
                                                                + "</abbr></a>"
                                                            )
                                                            
                                                        elif col_name == "OBJECT_NAME":
                                                            newRow[col_name] = (
                                                                '<a onclick="Objectviewcreate(this)"><abbr id ="'
                                                                + str(qwe)
                                                                + '" title="'
                                                                + str(qwe)
                                                                + '">'
                                                                + str(qwe)
                                                                + "</abbr></a>"
                                                            )
                                                            
                                                        else:
                                                            
                                                            if col_name == 'APPROVAL_TRANSACTION_RECORD_ID':
                                                                newRow[col_name] = (
                                                                '<a onclick="Material_view_obj(this)"><abbr id ="'
                                                                + str(qwe)
                                                                + '" title="'
                                                                + str(keyid.KeyCPQId.GetCPQId("ACAPTX", str(qwe)))
                                                                + '">'
                                                                + str(keyid.KeyCPQId.GetCPQId("ACAPTX", str(qwe)))
                                                                + "</abbr></a>"
                                                            )
                                                            
                                                            else:
                                                                if col_name == "APRCHN_ID":
                                                                    qwe = qwe.upper()
                                                                    Trace.Write("Line No:1760"+col_name)
                                                                    newRow[col_name] = (
                                                                        '<a onclick="Material_view_obj(this)"><abbr id ="'
                                                                        + str(qwe)
                                                                        + '" title="'
                                                                        + str(qwe)
                                                                        + '">'
                                                                        + str(qwe)
                                                                        + "</abbr></a>"
                                                                    )
                                                                elif str(current_prod) == "SALES":
                                                                    Trace.Write("Curnt_Prd_2"+str(current_prod))
                                                                    newRow[col_name] = (
                                                                        '<a onclick="gotquote_num_rev(this.innerHTML)"><abbr id ="'
                                                                        + str(qwe)
                                                                        + '" title="'
                                                                        + str(qwe)
                                                                        + '">'
                                                                        + str(qwe).upper()
                                                                        + "</abbr></a>"
                                                                    )
                                                                else:
                                                                    Trace.Write("Curnt_Prd_1"+str(current_prod))
                                                                    newRow[col_name] = (
                                                                        '<a onclick="Material_view_obj(this)"><abbr id ="'
                                                                        # '<a onclick="gotquote_num_rev(this.innerHTML)"><abbr id ="'
                                                                        + str(qwe)
                                                                        + '" title="'
                                                                        + str(qwe)
                                                                        + '">'
                                                                        + str(qwe).upper()
                                                                        + "</abbr></a>"
                                                                    )

                                                    else:
                                                        
                                                        if col_name == "APROBJ_LABEL" or col_name == "APRCHN_NAME" or col_name == "APRCHN_DESCRIPTION":
                                                            qwe_1 = str(eval("data." + col_name))
                                                            qwe_1 = qwe_1.upper()
                                                            newRow[col_name] = (
                                                                "<abbr id='"
                                                                + str(qwe)
                                                                + "' title='"
                                                                + str(qwe)
                                                                + "'>"
                                                                + str(qwe_1).upper()
                                                                + "</abbr>"
                                                            )
                                                            
                                                        else:
                                                            newRow[col_name] = (
                                                                "<abbr id='"
                                                                + str(qwe)
                                                                + "' title='"
                                                                + str(qwe).upper()
                                                                + "'>"
                                                                + str(eval("data." + col_name)).upper()
                                                                + "</abbr>"
                                                            )
                                                            

                                        except:
                                            if col_name in lookup_disply_list:
                                                for key, value in lookup_list.items():
                                                    if key == col_name:
                                                        lookup_obj = Sql.GetFirst(
                                                            "SELECT LOOKUP_OBJECT FROM  SYOBJD (NOLOCK) WHERE OBJECT_NAME = '"
                                                            + str(sql.PRIMARY_OBJECT_NAME).strip()
                                                            + "' AND LOOKUP_API_NAME ='"
                                                            + str(key)
                                                            + "' AND DATA_TYPE = 'LOOKUP' "
                                                        )
                                                        lookup_val = str(lookup_obj.LOOKUP_OBJECT)
                                                        tab_obj = Sql.GetFirst(
                                                            "SELECT SYPAGE.TAB_NAME,SYPAGE.TAB_RECORD_ID FROM SYPAGE (nolock) join SYSECT (NOLOCK) on SYPAGE.RECORD_ID = SYSECT.PAGE_RECORD_ID WHERE SYSECT.PRIMARY_OBJECT_NAME='"
                                                            + str(lookup_val).strip()
                                                            + "'"
                                                        )
                                                        RECORD_ID = eval("data." + str(value))
                                                        row_value = eval("data." + col_name)
                                                        if tab_obj is not None:
                                                            tab_val = str(tab_obj.TAB_NAME)
                                                            gettabvisibility = Sql.GetFirst("select VISIBLE FROM SYPRTB (NOLOCK) TB  INNER JOIN cpq_permissions (NOLOCK) cp ON cp.permission_id = TB.PROFILE_RECORD_ID INNER JOIN users_permissions (NOLOCK) up on up.permission_id = cp.permission_id where up.user_id = '"+str(userid)+"' and TB.TAB_ID = '"+str(tab_val.strip())+"'")
                                                            if tab_val in list_of_tabs:
                                                                idval = RECORD_ID + "|" + tab_val.strip()
                                                                row_value = str(eval("data." + col_name))
                                                                newRow[rowName] = (
                                                                    "<a id='"
                                                                    + str(idval)
                                                                    + "' class='cur_sty' onclick='Move_to_parent_obj(this)'>"
                                                                    + str(row_value)
                                                                    + "</a>"
                                                                )
                                                            else:
                                                                product_name = Sql.GetFirst(
                                                                    "select APP_LABEL from SYTABS (NOLOCK) where RECORD_ID='"
                                                                    + str(tab_obj.TAB_RECORD_ID)
                                                                    + "'"
                                                                )
                                                                if product_name is not None:
                                                                    module_txt = str(product_name.APP_LABEL).strip()
                                                                    product_id = Sql.GetFirst(
                                                                        "select PRODUCT_ID from products (NOLOCK) where PRODUCT_NAME='"
                                                                        + str(module_txt)
                                                                        + "'"
                                                                    )
                                                                if product_id != "" and product_id is not None:
                                                                    product_num = str(product_id.PRODUCT_ID)
                                                                    idval = RECORD_ID + "|" + tab_val
                                                                    newRow[rowName] = (
                                                                        "<a href='/Configurator.aspx?pid="
                                                                        + str(product_num)
                                                                        + "' id='"
                                                                        + str(idval)
                                                                        + "' class='cur_sty' onclick='Move_to_parent_obj(this)'>"
                                                                        + str(row_value)
                                                                        + "</a>"
                                                                    )
                                                                else:
                                                                    idval = RECORD_ID + "|" + lookup_val.strip()
                                                                    newRow[rowName] = (
                                                                        '<a href="#" id="'
                                                                        + idval
                                                                        + '" class="cur_sty" data-target="#cont_viewModalSection" onclick="cont_relatedlist_openview(this)" data-toggle="modal">'
                                                                        + str(row_value)
                                                                        + "</a>"
                                                                    )
                                                        else:
                                                            idval = RECORD_ID + "|" + lookup_val.strip()
                                                            newRow[rowName] = (
                                                                '<a href="#" id="'
                                                                + idval
                                                                + '" class="cur_sty" data-target="#cont_viewModalSection" onclick="cont_relatedlist_openview(this)" data-toggle="modal">'
                                                                + str(row_value)
                                                                + "</a>"
                                                            )
                                            elif col_name in checkbox_list:
                                                checkvalue = eval("data." + col_name)
                                                checked = ""
                                                if checkvalue.upper() == "TRUE":
                                                    checked = "checked"
                                                newRow[rowName] = (
                                                    "<input class='custom' type='checkbox' "
                                                    + str(checked)
                                                    + " disabled><span class='lbl'></span>"
                                                )
                                            elif col_name in currency_list:
                                                for col in currency_dict:
                                                    if col_name == str(col):
                                                        api_name = str(currency_dict[col])
                                                        qwe = str(eval("data." + str(api_name)))
                                                        price_decimal_obj = Sql.GetFirst(
                                                            "select DISPLAY_DECIMAL_PLACES,SYMBOL,CURRENCY from PRCURR (NOLOCK) where CURRENCY_RECORD_ID='"
                                                            + str(qwe)
                                                            + "'"
                                                        )
                                                        if price_decimal_obj is not None and len(price_decimal_obj) > 0:
                                                            curr_symbol = price_decimal_obj.CURRENCY
                                                            price_decimal = price_decimal_obj.DISPLAY_DECIMAL_PLACES
                                                            values = eval("data." + col_name)
                                                            if (
                                                                str(price_decimal) is not None
                                                                and str(price_decimal) != ""
                                                                and str(values) != ""
                                                            ):
                                                                price_decimal = str(price_decimal)
                                                                price_decimal = "%." + price_decimal + "f"
                                                                values = price_decimal % (values)
                                                                newRow[col] = str(values) + " " + curr_symbol

                                                            else:
                                                                newRow[col] = str(values) + " " + curr_symbol

                                                        else:
                                                            newRow[col_name] = (
                                                                '<abbr id ="'
                                                                + str(qwe)
                                                                + '" title="'
                                                                + str(qwe)
                                                                + '">'
                                                                + str(eval("data." + col_name))
                                                                + "</abbr>"
                                                            )
                                            else:
                                                try:
                                                    Trace.Write("EXCEPTION IN : try" + col_name)
                                                    newRow[rowName] = eval("data." + col_name)
                                                except:
                                                    Trace.Write("EXCEPTION IN : EVAL")
                                    newRowList.append(newRow)

        Test = (
            '<div class="col-md-12 brdr listContStyle padbthgt30"  ><div class="col-md-4 pager-numberofitem  clear-padding"><span class="pager-number-of-items-item noofitem" id="NumberofItem"  >1 - 10 of </span><span class="pager-number-of-items-item fltltpad2mrg0" id="totalItemCount"  >'
            + str(QueryCount)
            + '</span><div class="clear-padding fltltmrgtp3"  ><div  class="pull-right vralign"><select onchange="PageFunctest(this)" id="PageCountValue"   class="form-control pagecunt"><option value="10" '
            + str(a_10)
            + '>10</option><option value="20"'
            + str(a_20)
            + '>20</option><option value="50"'
            + str(a_50)
            + '>50</option><option value="100"'
            + str(a_100)
            + '>100</option><option value="200" '
            + str(a_200)
            + '>200</option></select> </div></div></div><div class="col-xs-8 col-md-4  clear-padding totcnt"   data-bind="visible: totalItemCount"><div class="clear-padding col-xs-12 col-sm-6 col-md-12 brdr0"  ><ul class="pagination pagination"><li class="disabled"><a href="#" onclick="FirstPageLoad_pagination()"><i class="fa fa-caret-left fnt14bold"  ></i><i class="fa fa-caret-left fnt14"  ></i></a></li><li class="disabled"><a href="#" onclick="Previous12334()"><i class="fa fa-caret-left fnt14"  ></i>PREVIOUS</a></li><li class="disabled"><a href="#" class="disabledPage" onclick="Next12334()">NEXT<i class="fa fa-caret-right fnt14"  ></i></a></li><li class="disabled"><a href="#" onclick="LastPageLoad_pagination()" class="disabledPage"><i class="fa fa-caret-right fnt14"  ></i><i class="fa fa-caret-right fnt14bold" ></i></a></li></ul></div> </div> <div class="col-md-4 pr_page_pad"  > <span id="page_count" class="currentPage page_right_content">1</span><span class="page_right_content pr_page_rt_cnt"  >Page </span></div></div>'
        )
        table_id = "FULLTABLELOAD"
        dbl_clk_function += (
            'var checkedRows=[]; var selected_checkboxes_index=[]; localStorage.setItem("multiedit_checkbox_values", []); $("#'
            + str(table_id)
            + '").on("check.bs.table", function (e, row, $element) { var selected_checkboxes_index=[]; arr11 = $("#'
            + str(table_id)
            + '").find("[type=\'checkbox\']:checked").map(function(){ selected_checkboxes_index.push($(this).attr("data-index"));}).get(); localStorage.setItem("selected_checkboxes_index",JSON.stringify(selected_checkboxes_index)); checkedRows.push($element.closest("tr").find("td:eq(2)").text()); localStorage.setItem("multiedit_checkbox_values", checkedRows); }); $("#'
            + str(table_id)
            + '").on("check-all.bs.table", function (e) { var checkedRows=[]; var table = $("#'
            + str(table_id)
            + '").closest("table"); table.find("tbody tr").each(function() {checkedRows.push($(this).find("td:nth-child(3)").text()); }); localStorage.setItem("multiedit_checkbox_values", checkedRows); }); $("#'
            + str(table_id)
            + '").on("uncheck-all.bs.table", function (e) {localStorage.setItem("multiedit_checkbox_values", []); }); $("#'
            + str(table_id)
            + '").on("uncheck.bs.table", function (e, row, $element) {var rec_ids=$element.closest("tr").find("td:eq(2)").text(); $.each(checkedRows, function(index, value) { if (value === rec_ids) { checkedRows.splice(index,1); arr11 = $("#'
            + str(table_id)
            + '").find("[type=\'checkbox\']:checked").map(function(){ selected_checkboxes_index.splice($(this).attr("data-index"));}).get(); localStorage.setItem("selected_checkboxes_index",JSON.stringify(selected_checkboxes_index)); } }); localStorage.setItem("multiedit_checkbox_values", checkedRows); });'
        )
        dbl_clk_function += (
            'var checkedRows=[];$("#'
            + str(table_id)
            + '").on("dbl-click-cell.bs.table", onClickCell); $("#'
            + str(table_id)
            + '").on("all.bs.table", function (e, name, args) { $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); });  function onClickCell(event, field, value, row, $element) { var reco_id=""; var reco = []; reco = localStorage.getItem("multiedit_checkbox_values") || [];  if (reco === null || reco === undefined ){ reco = []; } if (reco.length > 0){reco = reco.split(",");} if (reco.length > 0){ reco.push($element.closest("tr").find("td:eq(2)").text());  data1 = $element.closest("tr").find("td:eq(2)").text();   localStorage.setItem("multiedit_save_data", data1); reco_id = removeDuplicates(reco); }else{ reco_id=$element.closest("tr").find("td:eq(2)").text();  reco_id=reco_id.split(","); localStorage.setItem("multiedit_save_data", reco_id); } localStorage.setItem("multiedit_data_checked", reco_id); localStorage.setItem("table_id_edit", "'
            + str(table_id)
            + '"); try { cpq.server.executeScript("SYBLKEDTLG", {"TITLE":field, "VALUE":value, "CLICKEDID":"'
            + str(table_id)
            + '", "RECORDID":reco_id, "ELEMENT":"EDIT"}, function(data) { data0=data[0]; data2=data[1]; if(data0 != "NO"){ if(document.getElementById("list_grid_bulk_edit_bind_cont") ) { document.getElementById("list_grid_bulk_edit_bind_cont").innerHTML = data0; document.getElementById("list_grid_bulk_edit").style.display = "block"; $("#list_grid_bulk_edit").prepend("<div class=\'modal-backdrop fade in\'></div>"); var divHeight = $("#list_grid_bulk_edit").height(); $("#list_grid_bulk_edit .modal-backdrop").css("min-height", divHeight+"px"); $("#list_grid_bulk_edit .modal-dialog").css("width","550px"); $(".modal-dialog").css("margin-top","100px"); } if (data2.length !== 0){ $.each( data2, function( key, values ) { onclick_datepicker(values) }); } } }); } catch(err) {}}   $(\'#FULLTABLELOAD\').on(\'sort.bs.table\', function (e, name, order) {  currenttab = $("ul#carttabs_head .active").text().trim(); if (currenttab == "Pricebook Entries" || currenttab == "Catalogs")  { $("table#FULLTABLELOAD tbody tr td:nth-child(3)").css("display", "table-cell"); $("table#FULLTABLELOAD tbody tr th:nth-child(3)").css("display", "table-cell"); } localStorage.setItem("SortColumn", name); localStorage.setItem("SortColumnOrder", order); FullContainerSorting(name, order);});'
        )
        RelatedDrop_str = (
            " try { if( document.getElementById('"
            + str(table_id)
            + "') ) { var listws = document.getElementById('"
            + str(table_id)
            + "').getElementsByClassName('filter-control');  for (i = 0; i < listws.length; i++) { document.getElementById('"
            + str(table_id)
            + "').getElementsByClassName('filter-control')[i].innerHTML = data8[i];  } for (j = 0; j < listws.length; j++) {  if (data6[j] == 'select') { var dataAdapter = new $.jqx.dataAdapter(data7[j]);  if(data7[j].length>5){$('#RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter });var items = $('#RelatedMutipleCheckBoxDrop_' + j.toString()).jqxDropDownList('getItems'); } else{$('#RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter , autoDropDownHeight: true});  var items = $('#RelatedMutipleCheckBoxDrop_' + j.toString()).jqxDropDownList('getItems'); }  } } } }  catch(err) { setTimeout(function() { var listws = document.getElementById('"
            + str(table_id)
            + "').getElementsByClassName('filter-control');  for (i = 0; i < listws.length; i++) { document.getElementById('"
            + str(table_id)
            + "').getElementsByClassName('filter-control')[i].innerHTML = data8[i];  } for (j = 0; j < listws.length; j++) { if (data6[j] == 'select') { var dataAdapter = new $.jqx.dataAdapter(data7[j]);  $('#RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter }); } } }, 5000); }"
        )

        if QueryCount < int(Page_End):
            PageInformS = str(Page_start) + " - " + str(QueryCount) + " of"
        else:
            PageInformS = str(Page_start) + " - " + str(Page_End) + " of"

        if Param.ACTION != "FIRST":
            filter_control_function = ""

        filter_control_function += ' try { $("#FULLTABLELOAD").colResizable({ liveDrag:true, onResize: function(e){ var a = $(e.currentTarget); $("div[id^=\'RelatedMutipleCheckBoxDrop\']").jqxDropDownList("close"); } }); } catch (err) { setTimeout(function(){ $("#FULLTABLELOAD").colResizable({ liveDrag:true,onResize: function(e){ $("div[id^=\'RelatedMutipleCheckBoxDrop\']").jqxDropDownList("close"); } ,gripInnerHtml:"<div class=\'grip2\'></div>", draggingClass:"dragging" });}, 3000);  } '

        filter_control_function += '$("table#FULLTABLELOAD thead tr th:nth-child(3)").css("display", "none"); $("table#FULLTABLELOAD tbody tr td:nth-child(3)").css("display", "none");'

        if Param.ACTION == "FIRST":
            return (
                table_header,
                newRowList,
                "FULLTABLELOAD",
                Test,
                PageInform,
                filter_control_function,
                filter_level_list,
                AA_list,
                cv_list,
                RelatedDrop_str,
                dbl_clk_function,
                "",
                PRIMARY_OBJECT_NAMes,
                QueryCount,
                PageInformS,
                PerPage,
                table_header_new,
                subtab_str,
                tab_name_sub
            )
        elif Param.ACTION == "SECOND":
            return (
                table_header,
                newRowList,
                "FULLTABLELOAD",
                Test,
                PageInform,
                filter_control_function,
                filter_level_list,
                AA_list,
                cv_list,
                RelatedDrop_str,
                "",
                "",
                PRIMARY_OBJECT_NAMes,
                QueryCount,
                PageInformS,
                PerPage,
                table_header_new,
            )
        else:
            return (
                table_header,
                newRowList,
                "FULLTABLELOAD",
                Test,
                PageInform,
                filter_control_function,
                QueryCount,
                filter_level_list,
                AA_list,
                cv_list,
                "",
                PageInformS,
                PerPage,
                table_header_new,
            )

    def tabcolumnsPermission(self):
        get_user_id = Session["USERID"]
        try:
            tab_name = TestProduct.CurrentTab
        except:
            tab_name = Param.CurrentTab
        tabcolumns_list = []
        # section_qstns_visble_obj = Sql.GetList(
        #     """
        #                     SELECT SYSECT.RECORD_ID AS SECTION_REC_ID, SYSEFL.RECORD_ID, SYOBJD.DATA_TYPE, SYSEFL.API_NAME
        #                     FROM SYTABS (NOLOCK) 
        #                     JOIN SYPAGE (NOLOCK) ON SYTABS.PAGE_RECORD_ID = SYPAGE.RECORD_ID
        #                     JOIN SYSECT (NOLOCK) ON SYSECT.TAB_RECORD_ID = SYPAGE.RECORD_ID AND SYSECT.TAB_NAME = SYPAGE.TAB_NAME
        #                     JOIN SYSEFL (NOLOCK) ON SYSEFL.SECTION_RECORD_ID=SYSECT.RECORD_ID 
        #                     JOIN SYOBJD (NOLOCK) ON  SYOBJD.API_NAME = SYSEFL.API_NAME  AND   SYOBJD.OBJECT_NAME = SYSEFL.API_NAME 
        #                     JOIN
        #                         SYPRSN (NOLOCK)  ON SYPRSN.SECTION_RECORD_ID = SYSECT.RECORD_ID 
        #                     JOIN 
        #                         USERS_PERMISSIONS (NOLOCK) UP ON UP.PERMISSION_ID = SYPRSN.PROFILE_RECORD_ID
        #                     WHERE
        #                         LTRIM(RTRIM(SYTABS.TAB_LABEL)) = '{Tab_Text}' AND 
        #                         LTRIM(RTRIM(SYTABS.APP_LABEL)) ='{APP_LABEL}' AND
        #                         ISNULL(SYSECT.SECTION_NAME,'') != '' AND
        #                         ISNULL(SYSECT.PRIMARY_OBJECT_NAME,'') != ''  AND
        #                         UP.USER_ID = '{User_Record_Id}' AND 
        #                         SYPRSN.VISIBLE = 0
        #                     """.format(
        #         Tab_Text=tab_name, APP_LABEL=productName, User_Record_Id=get_user_id
        #     )
        # )
        section_qstns_visble_obj = Sql.GetList(
            """
                            SELECT SYSECT.RECORD_ID AS SECTION_REC_ID, SYSEFL.RECORD_ID, SYOBJD.DATA_TYPE, SYSEFL.API_NAME
                            FROM SYTABS (NOLOCK) 
                            JOIN SYPAGE (NOLOCK) ON SYTABS.PAGE_RECORD_ID = SYPAGE.RECORD_ID
                            JOIN SYSECT (NOLOCK) ON SYSECT.TAB_RECORD_ID = SYPAGE.RECORD_ID AND SYSECT.TAB_NAME = SYPAGE.TAB_NAME
                            JOIN SYSEFL (NOLOCK) ON SYSEFL.SECTION_RECORD_ID=SYSECT.RECORD_ID 
                            JOIN SYOBJD (NOLOCK) ON  SYOBJD.API_NAME = SYSEFL.API_NAME  AND   SYOBJD.OBJECT_NAME = SYSEFL.API_NAME 
                           
                            WHERE
                                LTRIM(RTRIM(SYTABS.TAB_LABEL)) = '{Tab_Text}' AND 
                                LTRIM(RTRIM(SYTABS.APP_LABEL)) ='{APP_LABEL}' AND
                                ISNULL(SYSECT.SECTION_NAME,'') != '' AND
                                ISNULL(SYSECT.PRIMARY_OBJECT_NAME,'') != '' 
                            """.format(
                Tab_Text=tab_name, APP_LABEL=productName
            )
        )
        # question_visible_obj = Sql.GetList(
        #     """
        #                     SELECT TOP 1000 SYPRSF.SECTIONFIELD_RECORD_ID, MO.DATA_TYPE,MQ.API_NAME
        #                     FROM SYTABS (NOLOCK) MT
        #                     JOIN SYPAGE (NOLOCK) PG ON PG.RECORD_ID = MT.PAGE_RECORD_ID
        #                     JOIN SYSECT (NOLOCK) MS ON MS.TAB_RECORD_ID = PG.RECORD_ID
                            
        #                     JOIN SYSEFL (NOLOCK) MQ ON MQ.SECTION_RECORD_ID = MS.RECORD_ID
                            
        #                     JOIN SYOBJD (NOLOCK) MO ON MO.API_NAME = MQ.API_NAME
        #                     AND MO.OBJECT_NAME = MQ.API_NAME
        #                     JOIN
        #                         SYPRSN (NOLOCK)  ON SYPRSN.SECTION_RECORD_ID = MS.RECORD_ID 
        #                     JOIN
        #                         SYPRSF (NOLOCK)  ON SYPRSF.SECTIONFIELD_RECORD_ID = MQ.RECORD_ID 
        #                     JOIN 
        #                         USERS_PERMISSIONS (NOLOCK) UP ON UP.PERMISSION_ID = SYPRSF.PROFILE_RECORD_ID
                            
        #                     AND ISNULL(MQ.FIELD_LABEL,'') != ''
        #                     AND UP.USER_ID = '{User_Record_Id}'
        #                     AND LTRIM(RTRIM(MT.TAB_NAME)) = '{Tab_Text}'
        #                     AND (SYPRSN.VISIBLE = 0 OR SYPRSF.VISIBLE = 0)
        #                     AND LTRIM(RTRIM(MT.APP_LABEL)) ='{APP_LABEL}'
        #                     AND ISNULL(MS.SECTION_NAME,'') != ''
        #                     ORDER BY ABS(MQ.DISPLAY_ORDER)
        #                     """.format(
        #         Tab_Text=tab_name, APP_LABEL=productName, User_Record_Id=get_user_id
        #     )
        # )
        question_visible_obj = Sql.GetList(
            """
                            SELECT TOP 1000 MQ.RECORD_ID, MO.DATA_TYPE,MQ.API_NAME
                            FROM SYTABS (NOLOCK) MT
                            JOIN SYPAGE (NOLOCK) PG ON PG.RECORD_ID = MT.PAGE_RECORD_ID
                            JOIN SYSECT (NOLOCK) MS ON MS.TAB_RECORD_ID = PG.RECORD_ID
                            
                            JOIN SYSEFL (NOLOCK) MQ ON MQ.SECTION_RECORD_ID = MS.RECORD_ID
                            
                            JOIN SYOBJD (NOLOCK) MO ON MO.API_NAME = MQ.API_NAME
                            AND MO.OBJECT_NAME = MQ.API_NAME
                            
                            
                            AND ISNULL(MQ.FIELD_LABEL,'') != ''
                            AND LTRIM(RTRIM(MT.TAB_NAME)) = '{Tab_Text}'
                          
                            AND LTRIM(RTRIM(MT.APP_LABEL)) ='{APP_LABEL}'
                            AND ISNULL(MS.SECTION_NAME,'') != ''
                            ORDER BY ABS(MQ.DISPLAY_ORDER)
                            """.format(
                Tab_Text=tab_name, APP_LABEL=productName
            )
        )
        if section_qstns_visble_obj is not None:
            for section_obj in section_qstns_visble_obj:
                if section_obj.API_NAME not in tabcolumns_list:
                    tabcolumns_list.append(section_obj.API_NAME)
        if question_visible_obj is not None:
            for question_obj in question_visible_obj:
                if question_obj.API_NAME not in tabcolumns_list:
                    tabcolumns_list.append(question_obj.API_NAME)
        return tabcolumns_list

    def UserRoleLoop(self, Role_list, roleId):
        GetChildRoleId = SqlHelper.GetList("SELECT * FROM SYROMA WHERE PAR_ROLE_RECORD_ID = '" + str(roleId) + "' ")
        for GetChild in GetChildRoleId:
            roleId = str(GetChild.ROLE_RECORD_ID)
            Role_list.append(roleId)
            CheckParent = SqlHelper.GetFirst("SELECT * FROM SYROMA WHERE PAR_ROLE_RECORD_ID = '" + str(roleId) + "' ")
            if CheckParent:
                getRolelist = self.UserRoleLoop(Role_list, roleId)
        return Role_list


objcontainer = CONTAINER()
try:
    QuoteId = Quote.CompositeNumber
except:
    QuoteId = ""
try:
    PerPage = Param.PerPage
    PageInform = Param.PageInform
except:
    PerPage = "20"
    PageInform = "1___20___20"
try:
    flag = Param.FLAG
except:
    flag = 5
Trace.Write(str(Param.ACTION))
if Param.ACTION == "FIRST":
    PerPage = ""
    PageInform = ""
    A_Keys = ""
    A_Values = ""
    SortColumn = ""
    SortColumnOrder = ""
    # if QuoteId == "":
    ApiResponse = ApiResponseFactory.JsonResponse(
        objcontainer.ListContainerShow(PerPage, PageInform, A_Keys, A_Values, SortColumn, SortColumnOrder)
    )
    """else:
        QuoteData = Sql.GetFirst(
            "SELECT MASTER_TABLE_QUOTE_RECORD_ID, QUOTE_ID FROM SAQTMT WHERE C4C_QUOTE_ID = '" + str(QuoteId) + "'"
        )
        if QuoteData is not None:
            ScriptExecutor.ExecuteGlobal(
                "SYALLTABOP",
                {
                    "Primary_Data": str(QuoteData.MASTER_TABLE_QUOTE_RECORD_ID),
                    "Primary_Data_rec": str(QuoteData.QUOTE_ID),
                    "TabNAME": "Quotes",
                    "ACTION": "VIEW",
                    "RELATED": "",
                },
            )"""

elif Param.ACTION == "SECOND":
    PerPage = Param.PerPage
    PageInform = Param.PageInform
    A_Keys = Param.A_Keys
    A_Values = Param.A_Values
    SortColumn = Param.SortColumn
    SortColumnOrder = Param.SortColumnOrder
    ApiResponse = ApiResponseFactory.JsonResponse(
        objcontainer.ListContainerShow(PerPage, PageInform, A_Keys, A_Values, SortColumn, SortColumnOrder)
    )
elif Param.ACTION == "SORTING":
    SortColumn = Param.SortColumn
    SortColumnOrder = Param.SortColumnOrder
    A_Keys = Param.A_Keys
    A_Values = Param.A_Values
    ApiResponse = ApiResponseFactory.JsonResponse(
        objcontainer.ListContainerShow(PerPage, PageInform, A_Keys, A_Values, SortColumn, SortColumnOrder)
    )
elif Param.ACTION == "TABLESORTING":
    PerPage = Param.PerPage
    PageInform = Param.PageInform
    PageInform = "1___" + str(PerPage) + "___" + str(PerPage)
    A_Keys = Param.A_Keys
    A_Values = Param.A_Values
    SortColumn = Param.SortColumn
    SortColumnOrder = Param.SortColumnOrder
    ApiResponse = ApiResponseFactory.JsonResponse(
        objcontainer.ListContainerShow(PerPage, PageInform, A_Keys, A_Values, SortColumn, SortColumnOrder)
    )


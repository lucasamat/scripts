# =========================================================================================================================================
#   __script_name : SYLDLKPPUP.PY
#   __script_description : THIS SCRIPT IS USED TO IMPLEMENT THE LOOKUP FIELD POPUP FUNCTIONALITY.
#   __primary_author__ : JOE EBENEZER
#   __create_date :
#   Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import re
import Webcom.Configurator.Scripting.Test.TestProduct
from SYDATABASE import SQL

Sql = SQL()

#####IMPLEMENT POPUP FUNCTIONALITY
def GSCONTLOOKUPPOPUP(TABLEID, objName, RECORD_ID, api_name, where):
    sec_str = ""
    SALESID = ""
    VAL_Obj = ""
    table_list = []
    curr_list = []
    # rec=Product.GetGlobal('segment_rec_id')
    # if rec == '':
    # Product.SetGlobal('inv_curr','')
    # Product.SetGlobal('cat_curr','')
    inv_curr = Product.GetGlobal("inv_curr")
    cat_curr = Product.GetGlobal("cat_curr")
    SALESID = Product.GetGlobal("SALESID")
    Trace.Write(str(cat_curr) + "catalog_currency")
    filter_control_function = ""
    var_str = ""
    pagination_app_total_count=0
    REC_IDS = "LOOKUPTABLE_" + str(RECORD_ID)
    TABLEID = str(TABLEID).strip()
    

    ####GETTING INFORMATION ABOUT TABLE LOOKUP LIST AND HEADER LABEL
    DATA_OBJ = Sql.GetFirst("SELECT COLUMNS FROM SYOBJS WHERE CONTAINER_NAME='" + str(TABLEID) + "' AND NAME='Lookup list'")
    Trace.Write("DATA_OBJ" + str(DATA_OBJ))
    
    OBJD_OBJ = Sql.GetList(
        "SELECT top 1000 API_NAME,FIELD_LABEL,DATA_TYPE FROM  SYOBJD WHERE OBJECT_NAME='" + str(TABLEID) + "'"
    )
    if OBJD_OBJ is not None:
        head_list = [{ins.API_NAME: ins.FIELD_LABEL} for ins in OBJD_OBJ]
    # if LOOKUP_ID != '' and xx_objname != '':
    # WhereStr = "SELECT LOOKUP_SQL_QUERY FROM  SYOBJD (NOLOCK) where OBJECT_NAME = '"+str(xx_objname)+"' and LOOKUP_API_NAME = '"+str(LOOKUP_ID)+"'"
    # where_obj = Sql.GetFirst(WhereStr)
    # where = where_obj.LOOKUP_SQL_QUERY
    if where and where != "":
        if where.find("<") != -1:
            m_where = re.findall("<(.+?)>", where)
            if m_where:
                for found in m_where:
                    where_text = "<" + str(found) + ">"
                    where_parse = Product.ParseString(where_text)
                  
                    where = where.replace(where_text, where_parse)
    
    Header_Obj = Sql.GetFirst("SELECT LABEL FROM SYOBJH WHERE OBJECT_NAME='" + str(TABLEID) + "'")
    if DATA_OBJ is not None:
        Colums_List = DATA_OBJ.COLUMNS
        Colums_final_list1 = eval(Colums_List)
        Colums_final_list = eval(Colums_List)[1:]
        COLUMNS_NAME = ",".join(Colums_final_list1)
        

        SegmentsClickParam = Product.GetGlobal("TreeParam")
        

        if SegmentsClickParam == "" and str(api_name) == "ACCOUNT_RECORD_ID":
            QueryStr = (
                "SELECT top 100 "
                + str(COLUMNS_NAME)
                + " FROM "
                + str(TABLEID)
                + " WHERE ACCOUNT_TYPE = 'SOLD TO PARTY' "
                + OrdersBy
            )
            VAL_Obj = Sql.GetList(QueryStr)

        else:
            QueryCount = Sql.GetFirst("SELECT COUNT(*) AS cnt FROM " + str(TABLEID))
            QueryStr = (
                "SELECT TOP 10 " + str(COLUMNS_NAME) + " FROM " + str(TABLEID) + " " + str(where)
            )
            
            ## A043S001P01-7711 STARTS
            VAL_Obj = Sql.GetList(QueryStr)
            ## A043S001P01-7711 ENDS
            try:

                QueryStr = (
                    "SELECT top 10 " + str(COLUMNS_NAME) + " FROM " + str(TABLEID) + " " + OrdersBy
                )
                VAL_Obj = Sql.GetList(QueryStr)
            except:
                Trace.Write("238----------------" + str(api_name))
                '''if TABLEID=="CACATG":
                    Categoryid=""
                    Categoryid=Product.Attributes.GetByName('QSTN_SYSEFL_MA_00079').GetValue()
                    if Categoryid!="":
                        QueryStr ="SELECT top 100 "+str(COLUMNS_NAME)+" FROM "+str(TABLEID)+" WHERE CATEGORY_ID!="+Categoryid+" "
                    else:
                        QueryStr ="SELECT top 100 "+str(COLUMNS_NAME)+" FROM "+str(TABLEID)+" " + OrdersBy
                else:
                    QueryStr = "SELECT top 100 "+str(COLUMNS_NAME)+" FROM "+str(TABLEID)+" "'''
            # Trace.Write('248----------------------------'+str(QueryStr))

    if VAL_Obj is not None and VAL_Obj != "":
        table_list = []
        for val_api in VAL_Obj:
            data_dict = {}
            objName = str(objName)
            first_col = str(eval("val_api." + str(Colums_final_list1[0])))
            sec_col = str(eval("val_api." + str(Colums_final_list1[1])))
            
            for Colums_final in Colums_final_list:
                try:
                    Colums_final_obj = eval("val_api." + str(Colums_final))
                    data_dict["ids"] = (
                        objName
                        + "|"
                        + str(Colums_final_list1[0])
                        + "|"
                        + first_col
                        + "|"
                        + sec_col
                        + "|"
                        + Colums_final_obj.replace('"', "")
                        + "|"
                        + api_name
                    )
                    #Trace.Write(str(Colums_final) + " " + str(Colums_final))

                    data_dict[str(Colums_final)] = eval("val_api." + str(Colums_final))
                except:
                    data_dict[str(Colums_final)] = (
                        str(eval("val_api." + str(Colums_final))).decode("unicode_escape").encode("utf-8")
                    )
                    Colums_final_obj = str(eval("val_api." + str(Colums_final)))
                    data_dict["ids"] = (
                        objName
                        + "|"
                        + str(Colums_final_list1[0])
                        + "|"
                        + first_col
                        + "|"
                        + sec_col
                        + "|"
                        + str(Colums_final_obj).replace('"', "")
                        + "|"
                        + api_name
                    )
            table_list.append(data_dict)
        if Header_Obj is not None:
            sec_str += (
                '<div   class="row modulebnr brdr">'
                + str(eval("Header_Obj.LABEL")).upper()
                + " LOOKUP LIST"
                + '<button type="button"   class="close fltrt"  data-dismiss="modal">X</button></div>'
            )
        sec_str += '<div   class="row pad-10 bg-lt-wt brdr brdbt0">'
        if RECORD_ID == 'SYSEFL_QT_01124':
            sec_str += '<button type="button" class="btnconfig" data-dismiss="modal">CANCEL</button>'
        else:
            sec_str += '<button type="button" onclick="popupClearall()" class="btnconfig" data-dismiss="modal">CLEAR SELECTION</button>'
        sec_str += "</div>"
        sec_str += '<div id="container" class="g4 pad-10 brdr except_sec">'
        sec_str += (
            '<table id="'
            + str(REC_IDS)
            + '" data-pagination="true" data-page-list="[5, 10, 20, 50, 100]" data-filter-control="true"><thead><tr>'
        )
        values_list = ""
        # lookup_data= Product.Attributes.GetByName('QSTN_SYSEFL_CM_00095').GetValue()
        # if lookup_data == '1':
        for invs in list(Colums_final_list):
            filter_clas = ".bootstrap-table-filter-control-" + str(invs)
            values_list += "var " + str(invs) + ' = $("' + str(filter_clas) + '").val(); '
            values_list += "ATTRIBUTE_VALUEList.push(" + str(invs) + "); "
        for key, col in enumerate(Colums_final_list):
            api_name_dict_list = [dicts for dicts in head_list if dicts.get(col)]
            api_name_header = ""
            if len(api_name_dict_list) > 0:
                api_name_header = api_name_dict_list[0].get(str(col))
                filter_class = ".bootstrap-table-filter-control-" + str(col)

                filter_control_function += (
                    '$("'
                    + filter_class
                    + '").change( function(){ var table_id = $(this).closest("table").attr("id"); ATTRIBUTE_VALUEList = []; '
                    + str(values_list)
                    + ' var attribute_value = $(this).val(); cpq.server.executeScript("SYLDLKPPUP", {"REC_ID":"'
                    + str(Param.REC_ID)
                    + '","LOOKUP":"LOOKUP_ONCHANGE", "ELEMENT" : "", "ATTRIBUTE_NAME": '
                    + str(list(Colums_final_list))
                    + ', "ATTRIBUTE_VALUE": ATTRIBUTE_VALUEList }, function(data) { if (data.length > 0){ $("#'
                    + str(REC_IDS)
                    + '").bootstrapTable("load", data );Pagination_GS_ADD_NEW_POPUP(attribute_value,data.length); $(".fixed-table-pagination").css("display","block"); }else{$("#'
                    + str(REC_IDS)
                    + '").bootstrapTable("load", data );  $("#'
                    + str(REC_IDS)
                    + ' tbody").html("<tr class=\'noRecDisp\'><td colspan=2 class=\'txtltimp\'>No Records to Display</td></tr>");$("#popup_footer").hide(); $(".fixed-table-pagination").css("cssText","display:none !important"); }  }); });'
                )

                if key == 0:
                    sec_str += (
                        '<th data-filter-control="input" data-sortable="true" data-field="'
                        + str(col)
                        + '"  data-formatter="LOOKTABLENameFormatter">'
                        + str(api_name_header)
                        + "</th>"
                    )
                else:
                    sec_str += (
                        '<th data-filter-control="input" data-sortable="true" data-field="'
                        + str(col)
                        + '">'
                        + str(api_name_header)
                        + "</th>"
                    )
        sec_str += "</tr></thead><tbody></tbody></table><div id=\'popup_footer\'></div></div>"
    
    try:
        pagination_app_total_count=QueryCount.cnt
    except:
        pagination_app_total_count=0
    if pagination_app_total_count>0:
        var_str += """<div class="col-md-12 brdr listContStyle padbthgt30">
                            <div class="col-md-4 pager-numberofitem  clear-padding">
                                <span class="pager-number-of-items-item flt_lt_pad2_mar2022" id="Rec_App_Start_End">{Records_App_Start_And_End}</span>
                                <span class="pager-number-of-items-item flt_lt_pad2_mar" id="TotalRecAppCount">{Pagination_TotalApp_Count}</span>
                                    <div class="clear-padding fltltmrgtp3">
                                        <div class="pull-right vralign">
                                            <select onchange="ShowResultCountFunction_GS_ADD_NEW_POPUP(this,'SYLDLKPPUP')" id="ShowResultCountsApp" class="form-control selcwdt">
                                                <option value="10" selected>10</option>
                                                <option value="20">20</option>
                                                <option value="50">50</option>
                                                <option value="100">100</option>
                                                <option value="200">200</option>
                                            </select>
                                        </div>
                                    </div>
                            </div>
                                <div class="col-xs-8 col-md-4  clear-padding inpadtex" data-bind="visible: totalItemCount">
                                    <div class="clear-padding col-xs-12 col-sm-6 col-md-12 brd0">
                                        <ul class="pagination pagination">
                                            <li class="disabled"><a onclick="GetFirstResultFunction_GS_ADD_NEW_POPUP('SYLDLKPPUP')" ><i class="fa fa-caret-left fnt14bold"></i><i class="fa fa-caret-left fnt14"></i></a></li>
                                            <li class="disabled"><a onclick="GetPreviuosResultFunction_GS_ADD_NEW_POPUP('SYLDLKPPUP')"><i class="fa fa-caret-left fnt14"></i>PREVIOUS</a></li>
                                            <li class="disabled"><a onclick="GetNextResultFunction_GS_ADD_NEW_POPUP('SYLDLKPPUP')">NEXT<i class="fa fa-caret-right fnt14"></i></a></li>
                                            <li class="disabled"><a onclick="GetLastResultFunction_GS_ADD_NEW_POPUP('SYLDLKPPUP')"><i class="fa fa-caret-right fnt14"></i><i class="fa fa-caret-right fnt14bold"></i></a></li>
                                        </ul>
                                    </div>
                                </div>
                                <div class="col-md-4 pad3">
                                <span id="page_count" class="currentPage page_right_content">{Current_Page}</span>
                                    <span class="page_right_content padrt2">Page </span>
                                </div>
                        </div></div>""".format(
                        Records_App_Start_And_End="1 - 10 of " if pagination_app_total_count>10 else "1 - "+str(pagination_app_total_count)+" of",
                        Pagination_TotalApp_Count=pagination_app_total_count,
                        Current_Page=1,
                    )
    return sec_str, table_list, REC_IDS, filter_control_function, var_str


####SEARCH FUNCTIONALITY IN LOOKUP POPUP
def GSCONTLOOKUPPOPUPFILTER(TABLEID, objName, RECORD_ID, ATTRIBUTE_NAME, ATTRIBUTE_VALUE, api_name, where,OFFSET_SKIP_COUNT,FETCH_COUNT):
    VAL_Obj = ""
    sec_str = ""
    filter_control_function = ""
    ATTRIBUTE_VALUE_STR = ""
    REC_IDS = "LOOKUPTABLE_" + str(RECORD_ID)
    TABLEID = str(TABLEID).strip()
    DATA_OBJ = Sql.GetFirst("SELECT COLUMNS FROM SYOBJS WHERE CONTAINER_NAME='" + str(TABLEID) + "' AND NAME='Lookup list'")
    
    Header_Obj = Sql.GetFirst("SELECT LABEL FROM SYOBJH WHERE OBJECT_NAME='" + str(TABLEID) + "'")
    
    if DATA_OBJ is not None:
        Colums_List = DATA_OBJ.COLUMNS
        OBJD_OBJ = Sql.GetList(
            "SELECT top 1000 API_NAME,FIELD_LABEL,DATA_TYPE FROM  SYOBJD WHERE OBJECT_NAME='" + str(TABLEID) + "'"
        )
        Colums_final_list1 = eval(Colums_List)
        
        Colums_final_list = eval(Colums_List)[1:]
        
        head_list = [{ins.API_NAME: ins.FIELD_LABEL} for ins in OBJD_OBJ]
        COLUMNS_NAME = ",".join(Colums_final_list1)
        
        Dict_formation = dict(zip(ATTRIBUTE_NAME, ATTRIBUTE_VALUE))
        ATTRIBUTE_VALUE_List = []
        for quer_key, quer_value in enumerate(Dict_formation):
            if Dict_formation.get(quer_value) != "":
                quer_values = str(Dict_formation.get(quer_value)).strip()
                ATTRIBUTE_VALUE_List.append(str(quer_value) + " like '%" + str(quer_values) + "%'")
                
        ATTRIBUTE_VALUE_STR = " AND ".join(ATTRIBUTE_VALUE_List)
        
        if where and where != "":
            if where.find("<") != -1:
                m_where = re.findall("<(.+?)>", where)
                if m_where:
                    for found in m_where:
                        where_text = "<" + str(found) + ">"
                        where_parse = Product.ParseString(where_text)
                        #Trace.Write("DDDDDDDDDDDDDDDD" + str(where_parse))
                        where = where.replace(where_text, where_parse)
        if ATTRIBUTE_VALUE_STR != "":
            VAL_Obj = Sql.GetList(
                "SELECT top 100 " + str(COLUMNS_NAME) + " FROM " + str(TABLEID) + " where " + str(ATTRIBUTE_VALUE_STR) + " "
            )
        else:
            VAL_Obj = Sql.GetList("SELECT " + str(COLUMNS_NAME) + " FROM " + str(TABLEID) + " order by (SELECT NULL) OFFSET {offset_skip_count} ROWS FETCH NEXT {per_page} ROWS ONLY".format(offset_skip_count=OFFSET_SKIP_COUNT,per_page=FETCH_COUNT))
           
        table_list = []
        for val_api in VAL_Obj:
            data_dict = {}
            objName = str(objName)
            first_col = str(eval("val_api." + str(Colums_final_list1[0])))
            sec_col = str(eval("val_api." + str(Colums_final_list1[1])))
            for Colums_final in Colums_final_list:
                try:
                    Colums_final_obj = eval("val_api." + str(Colums_final))
                    data_dict["ids"] = (
                        objName
                        + "|"
                        + str(Colums_final_list1[0])
                        + "|"
                        + first_col
                        + "|"
                        + sec_col
                        + "|"
                        + Colums_final_obj.replace('"', "")
                        + "|"
                        + api_name
                    )
                    data_dict[str(Colums_final)] = eval("val_api." + str(Colums_final))
                except:
                    data_dict[str(Colums_final)] = (
                        str(eval("val_api." + str(Colums_final))).decode("unicode_escape").encode("utf-8")
                    )
                    Colums_final_obj = str(eval("val_api." + str(Colums_final)))
                    data_dict["ids"] = (
                        objName
                        + "|"
                        + str(Colums_final_list1[0])
                        + "|"
                        + first_col
                        + "|"
                        + sec_col
                        + "|"
                        + str(Colums_final_obj).replace('"', "")
                        + "|"
                        + str(api_name)
                    )
            table_list.append(data_dict)
    return table_list


###to clear the data in popup fields
def GSCONTLOOKUPPOPUPCLEAR(VALUE, QSTN_LKP_ID):
    val_list = []
    val_dict = {}
    api_name = ""
    TABLEID = ""
    SQLOBJ = Sql.GetFirst("SELECT API_NAME,API_FIELD_NAME FROM SYSEFL WHERE SAPCPQ_ATTRIBUTE_NAME='" + str(VALUE) + "'")
    if SQLOBJ is not None:
        obj = str(eval("SQLOBJ.API_NAME"))
        TABLE_OBJ = Sql.GetFirst(
            "SELECT API_NAME,LOOKUP_OBJECT, LOOKUP_SQL_QUERY FROM  SYOBJD WHERE OBJECT_NAME='"
            + str(SQLOBJ.API_NAME)
            + "' AND DATA_TYPE='LOOKUP' AND LOOKUP_API_NAME='"
            + str(SQLOBJ.API_FIELD_NAME)
            + "'"
        )
        if TABLE_OBJ is not None:
            TABLEID = str(eval("TABLE_OBJ.LOOKUP_OBJECT"))
            api_name = str(eval("TABLE_OBJ.API_NAME"))
            LOOKUP_SQL_QUERY = str(eval("TABLE_OBJ.LOOKUP_SQL_QUERY"))
           
        TABLE_OBJS = Sql.GetList(
            "select OBJECT_NAME,API_NAME,DATA_TYPE,LOOKUP_OBJECT,FORMULA_LOGIC FROM  SYOBJD where OBJECT_NAME ='"
            + str(obj).strip()
            + "' and FORMULA_LOGIC like '%"
            + str(api_name)
            + "%'"
        )
        if TABLE_OBJS is not None:
            for TABLE_OBJ in TABLE_OBJS:
                val_dict = {}
               
                if TABLE_OBJ.DATA_TYPE != "":
                    DATA_TYPE = str(TABLE_OBJ.DATA_TYPE)

                    if api_name in str(TABLE_OBJ.FORMULA_LOGIC):
                        val_dict["API_NAME"] = str(TABLE_OBJ.API_NAME)
                        val_list.append(val_dict)

    for values in list(val_list):
        test_obj = Sql.GetFirst(
            "SELECT FIELD_LABEL,API_NAME FROM  SYOBJD WHERE API_NAME='"
            + str(values["API_NAME"])
            + "' and OBJECT_NAME='"
            + str(obj)
            + "'"
        )
       
        Trace.Write("testtettetetetet" + str(values["API_NAME"]))
        if test_obj is not None:
            for tab in Product.Tabs:
                if tab.IsSelected == True:
                    name = tab.Name
                    prod = Product.Name
                    tab_obj = Sql.GetFirst(
                        "select TAB_LABEL,APP_LABEL from SYTABS where SAPCPQ_ALTTAB_NAME='"
                        + str(name)
                        + "' AND LTRIM(RTRIM(APP_LABEL))='"
                        + str(prod).strip()
                        + "'"
                    )
                    if tab_obj is not None:
                        testobj = Sql.GetFirst(
                            "select APP_ID from SYAPPS where APP_LABEL='" + str(tab_obj.APP_LABEL).strip() + "'"
                        )
                        sec_obj = Sql.GetList(
                            "select SE.RECORD_ID from SYSECT(nolock) SE inner join SYPAGE(nolock)PG on SE.PAGE_RECORD_ID = PG.RECORD_ID where PG.TAB_NAME='"
                            + str(tab_obj.TAB_LABEL).strip()
                            + "'"
                        )

                        if testobj is not None:
                            for data in sec_obj:
                                result_obj = Sql.GetFirst(
                                    "SELECT SAPCPQ_ATTRIBUTE_NAME as RECORD_ID FROM SYSEFL WHERE (FIELD_LABEL='"
                                    + str(test_obj.FIELD_LABEL).strip()
                                    + "' or API_NAME='"
                                    + str(test_obj.API_NAME).strip()
                                    + "') AND SAPCPQ_ATTRIBUTE_NAME LIKE '%SYSEFL-"
                                    + str(testobj.APP_ID).strip()
                                    + "%' and SECTION_RECORD_ID='"
                                    + str(data.RECORD_ID).strip()
                                    + "'"
                                )
                                
                                if result_obj is not None:
                                    #Trace.Write("QSTNQSTNQSTNQSTN" + "QSTN_" + str(result_obj.RECORD_ID).replace("-", "_"))
                                    qstnid = str("QSTN_" + str(result_obj.RECORD_ID).replace("-", "_"))
                                    Product.ResetAttr(str(qstnid))
                                    Product.Attributes.GetByName(str(qstnid)).AssignValue("")
                                    
        Product.Attributes.GetByName(str(QSTN_LKP_ID)).HintFormula = ""
        Trace.Write("QSTN_LKP_ID---------" + str(Product.Attributes.GetByName(str(QSTN_LKP_ID)).GetValue))

    return ""

def GSCONTLOOKUPPOPUPPAGINATION(QSTN_LKP_ID,VALUE):
    Trace.Write('Inside pagination function')




REC_ID = Param.REC_ID
LOOKUP = Param.LOOKUP
ELEMENT = Param.ELEMENT

Trace.Write(ELEMENT)
Trace.Write("LOOKUP_SCRIPT_EXECUTION _STARTS" + str(LOOKUP))
Product.SetGlobal("lookup", "")
LOOKUP_SQL_QUERY = ""

warning = False
try:
    Offset_Skip_Count=Param.Offset_Skip_Count
    Fetch_Count=Param.Fetch_Count
except:
    Offset_Skip_Count=0
    Fetch_Count=10

if LOOKUP == "FIRST":
    VALUE = REC_ID.replace("_", "-")
    sqlStr = "SELECT API_NAME,API_FIELD_NAME FROM SYSEFL WHERE SAPCPQ_ATTRIBUTE_NAME='" + str(VALUE) + "'"
    SQLOBJ = Sql.GetFirst(sqlStr)
    
    if SQLOBJ is not None:
        obj = str(eval("SQLOBJ.API_NAME"))
        Qstr = (
            "SELECT API_NAME,LOOKUP_OBJECT, LOOKUP_SQL_QUERY FROM  SYOBJD WHERE OBJECT_NAME='"
            + str(SQLOBJ.API_NAME)
            + "' AND DATA_TYPE='LOOKUP' AND LOOKUP_API_NAME='"
            + str(SQLOBJ.API_FIELD_NAME)
            + "'"
        )
        TABLE_OBJ = Sql.GetFirst(Qstr)
        if TABLE_OBJ is not None:
            TABLEID = str(eval("TABLE_OBJ.LOOKUP_OBJECT"))
            api_name = str(eval("TABLE_OBJ.API_NAME"))
            LOOKUP_SQL_QUERY = str(eval("TABLE_OBJ.LOOKUP_SQL_QUERY"))
           
            ApiResponse = ApiResponseFactory.JsonResponse(
                GSCONTLOOKUPPOPUP(TABLEID, obj, REC_ID, api_name, LOOKUP_SQL_QUERY)
            )

####TO ASSIGN VALUE SELECTED FROM POPUP
elif LOOKUP == "SECOND":
    objname = ELEMENT.split("|")[0]
    id_value = ELEMENT.split("|")[1]
    RecordID = ELEMENT.split("|")[2]
    RecordName = ELEMENT.split("|")[3]
    api_name = ELEMENT.split("|")[5]
    # Product.SetGlobal('inv_curr','')
    # Product.SetGlobal('cat_curr','')
    RecordID_No = RecordID + ", " + RecordName
    
    Product.Attributes.GetByName(str(REC_ID)).HintFormula = RecordID
    RECORD_ID = REC_ID.replace("QSTN_LKP_", "QSTN_")
    
    
    result = ScriptExecutor.ExecuteGlobal("SYPARCEFMA", {"Object": objname, "API_Name": api_name, "API_Value": RecordID})
    Trace.Write("result ===> " + str(result))
    for values in result:
        test_obj = Sql.GetFirst(
            "SELECT FIELD_LABEL,API_NAME FROM  SYOBJD WHERE API_NAME='"
            + str(values["API_NAME"])
            + "' and OBJECT_NAME='"
            + str(objname)
            + "'"
        )
        
        if test_obj is not None:
            for tab in Product.Tabs:
                if tab.IsSelected == True:
                    name = tab.Name
                    prod = Product.Name
                    #Trace.Write("prod" + str(prod))
                    tab_obj = Sql.GetFirst(
                        "select TAB_LABEL,APP_LABEL from SYTABS where SAPCPQ_ALTTAB_NAME='"
                        + str(name)
                        + "' AND LTRIM(RTRIM(APP_LABEL))='"
                        + str(prod).strip()
                        + "'"
                    )
                    if tab_obj is not None:
                        testobj = Sql.GetFirst(
                            "select APP_ID from SYAPPS where APP_LABEL='" + str(tab_obj.APP_LABEL).strip() + "'"
                        )
                       
                        sec_obj = Sql.GetList(
                            "select SE.RECORD_ID from SYSECT(nolock) SE inner join SYPAGE(nolock)PG on SE.PAGE_RECORD_ID = PG.RECORD_ID where PG.TAB_NAME='"
                            + str(tab_obj.TAB_LABEL).strip()
                            + "'"
                        )
                        
                        if testobj is not None:
                            for data in sec_obj:
                                result_obj = Sql.GetFirst(
                                    "SELECT SAPCPQ_ATTRIBUTE_NAME as RECORD_ID FROM SYSEFL WHERE (FIELD_LABEL='"
                                    + str(test_obj.FIELD_LABEL).strip()
                                    + "' or API_NAME='"
                                    + str(test_obj.API_NAME).strip()
                                    + "') AND SAPCPQ_ATTRIBUTE_NAME LIKE '%SYSEFL-"
                                    + str(testobj.APP_ID).strip()
                                    + "%' and SECTION_RECORD_ID='"
                                    + str(data.RECORD_ID).strip()
                                    + "'"
                                )
                                
                                if result_obj is not None:
                                    #Trace.Write("QSTNQSTNQSTNQSTN" + "QSTN_" + str(result_obj.RECORD_ID).replace("-", "_"))
                                    qstnid = str("QSTN_" + str(result_obj.RECORD_ID).replace("-", "_"))
                                    Product.ResetAttr(str(qstnid))
                                    #Trace.Write("The value if values is here " + str(qstnid))
                                   
                                    Product.Attributes.GetByName(str(qstnid)).AssignValue(values["FORMULA_RESULT"])

    ApiResponse = ApiResponseFactory.JsonResponse([warning])


elif LOOKUP == "LOOKUP_ONCHANGE":
    ATTRIBUTE_NAME = list(Param.ATTRIBUTE_NAME)
    ATTRIBUTE_VALUE = list(Param.ATTRIBUTE_VALUE)
    OFFSET_SKIP_COUNT=Offset_Skip_Count
    FETCH_COUNT=Fetch_Count
    
    VALUE = REC_ID.replace("_", "-")
    
    SQLOBJ = Sql.GetFirst("SELECT API_NAME,API_FIELD_NAME FROM SYSEFL WHERE SAPCPQ_ATTRIBUTE_NAME='" + str(VALUE) + "'")
    if SQLOBJ is not None:
        obj = str(eval("SQLOBJ.API_NAME"))
        TABLE_OBJ = Sql.GetFirst(
            "SELECT API_NAME,LOOKUP_OBJECT,LOOKUP_SQL_QUERY FROM  SYOBJD WHERE OBJECT_NAME='"
            + str(SQLOBJ.API_NAME)
            + "' AND DATA_TYPE='LOOKUP' AND LOOKUP_API_NAME='"
            + str(SQLOBJ.API_FIELD_NAME)
            + "'"
        )
        if TABLE_OBJ is not None:
            TABLEID = str(eval("TABLE_OBJ.LOOKUP_OBJECT"))
            api_name = str(eval("TABLE_OBJ.API_NAME"))
            LOOKUP_SQL_QUERY = str(eval("TABLE_OBJ.LOOKUP_SQL_QUERY"))
            
            ApiResponse = ApiResponseFactory.JsonResponse(
                GSCONTLOOKUPPOPUPFILTER(TABLEID, obj, REC_ID, ATTRIBUTE_NAME, ATTRIBUTE_VALUE, api_name, LOOKUP_SQL_QUERY,OFFSET_SKIP_COUNT,FETCH_COUNT)
            )
elif LOOKUP == "PAGINATION":
    QSTN_LKP_ID = str(REC_ID)
    VALUE = REC_ID.replace("_", "-")
    ApiResponse = ApiResponseFactory.JsonResponse(GSCONTLOOKUPPOPUPPAGINATION(QSTN_LKP_ID,VALUE))
elif LOOKUP == "CLEAR":
    QSTN_LKP_ID = str(REC_ID)
    VALUE = str(QSTN_LKP_ID).replace("_", "-").replace("QSTN-LKP-", "")
    Trace.Write(str(REC_ID) + "REC_IDREC_IDREC_ID" + str(VALUE))
    ApiResponse = ApiResponseFactory.JsonResponse(GSCONTLOOKUPPOPUPCLEAR(VALUE, QSTN_LKP_ID))

Trace.Write("LOOKUP_SCRIPT_EXECUTION_ENDS")
ScriptExecutor.ExecuteGlobal("SYRLEXEEND")

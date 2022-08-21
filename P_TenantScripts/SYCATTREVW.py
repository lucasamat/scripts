# =========================================================================================================================================
#   __script_name : SYCATTREVW.PY
#   __script_description : THIS SCRIPT IS USED TO LOAD THE NESTED LIST GRID FOR THE PRICECLASS AND CATEGORY TABS.
#   __primary_author__ :  
#   __create_date :
#   Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
from SYDATABASE import SQL
import Webcom.Configurator.Scripting.Test.TestProduct
Sql = SQL()


def Rolesrecurrsion(ROLE_ID, data_list, Action_str, Select_str):
    Qstr1 = (
        "select top 10000 ROLE_RECORD_ID,ROLE_ID,ROLE_NAME,ROLE_DESCRIPTION,PAR_ROLE_RECORD_ID,PAR_ROLE_ID,START_PAGE from SYROMA (nolock) where PAR_ROLE_ID = '"
        + str(ROLE_ID)
        + "' order by ROLE_ID asc"
    )
   
    child_obj = Sql.GetList(Qstr1)
    if child_obj:
        for chil in child_obj:
            child_dict = {}
            child_dict["ACTION"] = str(Action_str)
            child_dict["SELECT"] = str(Select_str)
            child_dict["ROLE_RECORD_ID"] = str(chil.ROLE_RECORD_ID)
            child_dict["PAR_ROLE_RECORD_ID"] = str(chil.PAR_ROLE_RECORD_ID)
            Role_Id = str(chil.ROLE_ID)
            Role_Id = Role_Id.upper()
            Role_Name = str(chil.ROLE_NAME)
            Role_Name = Role_Name.upper()
            Role_Description = str(chil.ROLE_DESCRIPTION)
            Role_Description = Role_Description.upper()
            child_dict["ROLE_ID"] = (
                '<a href="#" class="cur_sty" onclick="Material_view_obj(this)">' + str(Role_Id) + "</a>"
            )
            
            child_dict["PAR_ROLE_ID"] = str(chil.PAR_ROLE_ID)
            child_dict["ROLE_NAME"] = str(chil.ROLE_NAME)
            child_dict["ROLE_DESCRIPTION"] = str(chil.ROLE_DESCRIPTION)
            child_dict["START_PAGE"] = str(chil.START_PAGE)
            data_list.append(child_dict)
            if str(chil.PAR_ROLE_ID) != "":
                Rolesrecurrsion(chil.ROLE_ID, data_list, Action_str, Select_str)
    return data_list


def GetRolesTreeresult(PerPage, PageInform, A_Keys, A_Values):
    # Variable decliration. And Action button visibility check.
    data_list = []
    A_list = {}
    rec_id = "SYOBJ-00424"
    obj_id = "SYOBJ-00424"
    objh_getid = Sql.GetFirst(
        "SELECT TOP 1  RECORD_ID  FROM SYOBJH (NOLOCK) WHERE SAPCPQ_ATTRIBUTE_NAME='" + str(obj_id) + "'"
    )
    if objh_getid:
        obj_id = objh_getid.RECORD_ID
    objs_obj = Sql.GetFirst(
        "select CAN_ADD,CAN_EDIT,CAN_CLONE,CAN_DELETE from SYOBJS (NOLOCK) where UPPER(NAME)='TAB LIST' and OBJ_REC_ID = '"
        + str(obj_id)
        + "' "
    )
    can_edit = str(objs_obj.CAN_EDIT)
    can_clone = str(objs_obj.CAN_CLONE)
    can_delete = str(objs_obj.CAN_DELETE)
    # if len(A_Keys) < 0 and  len(A_Values) < 0:
    A_list = dict(zip(A_Keys, A_Values))
    if PageInform != "":
        Page_start = PageInform.split("___")[0]
        Page_End = PageInform.split("___")[1]

    where = ""
    for inj in A_list:
        if A_list[inj] != "":
            x_picklistcheckobj = Sql.GetFirst(
                "SELECT PICKLIST FROM SYOBJD (NOLOCK) WHERE OBJECT_NAME ='SYROMA' AND API_NAME = '" + str(inj) + "'"
            )
            x_picklistcheck = str(x_picklistcheckobj.PICKLIST).upper()
            if x_picklistcheck == "TRUE":
                where += str(inj) + " = '" + str(A_list[inj]) + "' and "
            else:
                where += str(inj) + " like '%" + str(A_list[inj]) + "%' and "

    Action_str = '<div class="btn-group dropdown"><div class="dropdown" id="ctr_drop"><i data-toggle="dropdown" id="dropdownMenuButton" class="fa fa-sort-desc dropdown-toggle" aria-expanded="false"></i><ul class="dropdown-menu left" aria-labelledby="dropdownMenuButton"><li><a class="dropdown-item cur_sty" href="#" onclick="Material_view_obj(this)">VIEW</a></li>'
    if can_edit.upper() == "TRUE":
        Action_str += '<li><a class="dropdown-item cur_sty" href="#" onclick="Material_edit_obj(this)">EDIT</a></li>'
    if can_delete.upper() == "TRUE":
        Action_str += '''<li class="delete_list" style="display: block;"><a class="dropdown-item" href="#" id="deletebtn" onclick="CommonDelete(this, 'SYROMA', 'WARNING')" data-target="#cont_CommonModalDelete" data-toggle="modal">DELETE</a></li>'''
    Action_str += "</ul></div></div>"
    OrderBy_obj = Sql.GetFirst("select ORDERS_BY from SYOBJS (NOLOCK) where CONTAINER_NAME = 'SYROMA' and NAME ='Tab list' ")
    if OrderBy_obj is not None:
        if OrderBy_obj.ORDERS_BY != "":
            col = OrderBy_obj.ORDERS_BY
        else:
            col = "ROLE_RECORD_ID DESC"
    else:
        col = "ROLE_RECORD_ID DESC"
    Select_str = '<label class="middle"><input class="custom" type="checkbox"  onclick="get_checkbox_row_list(this)" /><span class="lbl"></span></label>'
    '''Qstr = (
        "select top "
        + str(PerPage)
        + " * from (select ROW_NUMBER() OVER(ORDER BY "
        + str(col)
        + ") AS ROW,ROLE_RECORD_ID,ROLE_ID,ROLE_NAME,ROLE_DESCRIPTION,PAR_ROLE_RECORD_ID,PAR_ROLE_ID,START_PAGE from SYROMA (NOLOCK) ) m where "
        + str(where)
        + " m.ROW BETWEEN "
        + str(Page_start)
        + " and "
        + str(Page_End)
        + ""
    )'''
    Qstr = (
        "select top "
        + str(PerPage)
        + " * from (select ROW_NUMBER() OVER(ORDER BY "
        + str(col)
        + ") AS ROW,ROLE_RECORD_ID,ROLE_ID,ROLE_NAME,ROLE_DESCRIPTION,PAR_ROLE_RECORD_ID,PAR_ROLE_ID,PAR_ROLE_NAME,START_PAGE from SYROMA (NOLOCK) where "
        + str(where)
        + " PAR_ROLE_ID = '') m where m.ROW BETWEEN "
        + str(Page_start)
        + " and "
        + str(Page_End)
        + ""
    )

    
    QCont = "select count(ROLE_RECORD_ID) as cnt from SYROMA (NOLOCK) where " + str(where) + " PAR_ROLE_ID = '' "
    QueryCountObj = Sql.GetFirst(QCont)
    QueryCount = QueryCountObj.cnt
    parent_obj = Sql.GetList(Qstr)
    for par in parent_obj:
        ROLE_ID = par.ROLE_ID
        ROLE_NAME = par.ROLE_NAME
        data_dict = {}
        data_dict["ACTION"] = str(Action_str)
        data_dict["SELECT"] = str(Select_str)
        data_dict["ROLE_RECORD_ID"] = str(par.ROLE_RECORD_ID)
        
        Role_Id = str(par.ROLE_ID)
        Role_Id = Role_Id.upper()
        
        Role_Name = str(par.ROLE_NAME)
        Role_Name = Role_Name.upper()
        Role_Description = str(par.ROLE_DESCRIPTION)
        Role_Description = Role_Description.upper()
        data_dict["ROLE_ID"] = '<a href="#" class="cur_sty" onclick="Material_view_obj(this)">' + str(Role_Id) + "</a>"
        
        if str(par.PAR_ROLE_RECORD_ID):
            data_dict["PAR_ROLE_RECORD_ID"] = str(par.PAR_ROLE_RECORD_ID)
        else:
            data_dict["PAR_ROLE_RECORD_ID"] = ''
        try:
            data_dict["ROLE_NAME"] = str(Role_Name.encode("ASCII", "ignore"))
        except:
            data_dict["ROLE_NAME"] = str(Role_Name)
        if str(par.PAR_ROLE_ID):
            data_dict["PAR_ROLE_ID"] = str(par.PAR_ROLE_ID)
        else:
            data_dict["PAR_ROLE_ID"] =  ''
        data_dict["ROLE_DESCRIPTION"] = str(Role_Description)
        if str(par.START_PAGE):
            data_dict["START_PAGE"] = str(par.START_PAGE)
        else:
            data_dict["START_PAGE"] = ''
        data_list.append(data_dict)
        if str(par.PAR_ROLE_ID != ''):
            Rolesrecurrsion(ROLE_ID, data_list, Action_str, Select_str)
    if QueryCount < int(Page_End):
        PageInformS = str(Page_start) + " - " + str(QueryCount) + " of"
    else:
        PageInformS = str(Page_start) + " - " + str(Page_End) + " of"
    filter_control_function = '$("#ejsearch_btn_cat").click( function(){ RoleSearchFuction(); });'
    Test = (
        '<div class="col-md-12 brdr listContStyle" style="padding-bottom: 0;padding: 2px;height: 30px;"><div class="col-md-4 pager-numberofitem  clear-padding"><span class="pager-number-of-items-item" id="NumberofItem" style="float:left;padding:2px;margin:2px 0px 2px 2px;">'
        + str(PageInformS)
        + ' </span><span class="pager-number-of-items-item" id="totalItemCount" style="float:left;padding:2px;margin:2px 2px 2px 0px;">'
        + str(QueryCount)
        + '</span><div class="clear-padding" style="float:left;margin-top: -3px;"><div style="vertical-align:middle;text-align: right;" class="pull-right"><select onchange="PageFunctestChild(this, \'Roles\')" id="PageCountValue" style="width: 65px; vertical-align:middle; display: inline-block; margin-left: 5px" class="form-control"><option value="10">10</option><option value="20" selected>20</option><option value="50">50</option><option value="100">100</option><option value="200">200</option></select> </div></div></div><div class="col-xs-8 col-md-4  clear-padding" style="display:inline-block;padding-left:10px !important; text-align: center;" data-bind="visible: totalItemCount"><div class="clear-padding col-xs-12 col-sm-6 col-md-12" style="border:0;"><ul class="pagination pagination"><li class="disabled"><a href="#" onclick="FirstPageLoad_paginationChild(\'Roles\')"><i class="fa fa-caret-left" style="font-size: 14px;font-weight: bold;"></i><i class="fa fa-caret-left" style="font-size: 14px;"></i></a></li><li class="disabled"><a href="#" onclick="Previous12334Child(\'Roles\')"><i class="fa fa-caret-left" style="font-size: 14px;"></i>PREVIOUS</a></li><li class="disabled"><a href="#" class="disabledPage" onclick="Next12334Child(\'Roles\')">NEXT<i class="fa fa-caret-right" style="font-size: 14px;"></i></a></li><li class="disabled"><a href="#" onclick="LastPageLoad_paginationChild(\'Roles\')" class="disabledPage"><i class="fa fa-caret-right" style="font-size: 14px;"></i><i class="fa fa-caret-right" style="font-size: 14px;font-weight: bold;"></i></a></li></ul></div> </div> <div class="col-md-4" style="padding: 3px;"> <span id="page_count" class="currentPage page_right_content">1</span><span class="page_right_content" style="padding-right: 2px;">Page </span></div></div>'
    )
    Filter_Sr = '$("#RolesTreeTable_ROLE_NAME_filterbarcell").change(function(){ $("#ejsearch_btn_cat").click(); }); $("#RolesTreeTable_ROLE_ID_filterbarcell").change(function(){ $("#ejsearch_btn_cat").click(); });$("#RolesTreeTable_ROLE_NAME_filterbarcell").change(function(){ $("#ejsearch_btn_cat").click(); }); $("#RolesTreeTable_PAR_ROLE_ID_filterbarcell").change(function(){ $("#ejsearch_btn_cat").click(); }); $("#RolesTreeTable_ROLE_DESCRIPTION_filterbarcell").change(function(){ $("#ejsearch_btn_cat").click(); }); $("#RolesTreeTable_START_PAGE_filterbarcell").change(function(){ $("#ejsearch_btn_cat").click(); });'
    return (
        data_list,
        rec_id,
        filter_control_function,
        Test,
        "RolesTreeTable",
        PageInformS,
        QueryCount,
        Filter_Sr,
    )


def GetRolesTreeResultFilter(ATTRIBUTE_NAME, ATTRIBUTE_VALUE, PerPage): 
    # Variable decliration and Where conduction formation.
    Dict_formation = dict(zip(ATTRIBUTE_NAME, ATTRIBUTE_VALUE))
    ATTRIBUTE_VALUE_STR = ""
    filter_control_function = ""
    data_list = []
    rec_id = "SYOBJ-00424"
    for quer_key, quer_value in enumerate(Dict_formation):
        if Dict_formation.get(quer_value) != "":
            x_picklistcheckobj = Sql.GetFirst(
                "SELECT PICKLIST FROM SYOBJD (NOLOCK) WHERE OBJECT_NAME ='SYROMA' AND API_NAME = '" + str(quer_value) + "'"
            )
            x_picklistcheck = str(x_picklistcheckobj.PICKLIST).upper() if x_picklistcheckobj is not None else "FALSE"
            quer_values = str(Dict_formation.get(quer_value)).strip()
            if str(quer_values).upper() == "TRUE":
                quer_values = "True"
            elif str(quer_values).upper() == "FALSE":
                quer_values = "False"
            if str(quer_values).find(",") == -1:
                if x_picklistcheck == "TRUE":
                    ATTRIBUTE_VALUE_STR += str(quer_value) + " = '" + str(quer_values) + "' and "
                else:
                    ATTRIBUTE_VALUE_STR += str(quer_value) + " like '%" + str(quer_values) + "%' and "
            else:
                quer_values = quer_values.split(",")
                quer_values = tuple(list(quer_values))
                ATTRIBUTE_VALUE_STR += str(quer_value) + " in " + str(quer_values) + " and "
    if ATTRIBUTE_VALUE_STR != "":
        Qury_str = (
            "select top "
            + str(PerPage)
            + " ROLE_RECORD_ID,ROLE_ID,ROLE_NAME,ROLE_DESCRIPTION,PAR_ROLE_RECORD_ID,PAR_ROLE_ID,START_PAGE from SYROMA WHERE "
            + str(ATTRIBUTE_VALUE_STR)
            + " 1=1  order by ROLE_ID asc"
        )
        QueryCountStr = "select count(ROLE_RECORD_ID) as cnt from SYROMA WHERE " + str(ATTRIBUTE_VALUE_STR) + " 1=1"
    else:
        Qury_str = (
            "select top "
            + str(PerPage)
            + " ROLE_RECORD_ID,ROLE_ID,ROLE_NAME,ROLE_DESCRIPTION,PAR_ROLE_RECORD_ID,PAR_ROLE_ID,START_PAGE from SYROMA  where PAR_ROLE_ID = '' order by ROLE_ID asc"
        )
        QueryCountStr = "select count(ROLE_RECORD_ID) as cnt from SYROMA where PAR_ROLE_ID = '' "
    
    try:
        Query_Obj = Sql.GetList(str(Qury_str))
        QueryCount_Obj = Sql.GetFirst(str(QueryCountStr))
        QueryCount = QueryCount_Obj.cnt
    except:
        Qury_str = "select ROLE_RECORD_ID,ROLE_ID,ROLE_NAME,ROLE_DESCRIPTION,PAR_ROLE_RECORD_ID,PAR_ROLE_ID,START_PAGE from SYROMA  where PAR_ROLE_ID = ''"
        QueryCountStr = "select count(ROLE_RECORD_ID) as cnt from SYROMA where PAR_ROLE_ID = ''"
        QueryCount_Obj = Sql.GetFirst(str(QueryCountStr))
        QueryCount = QueryCount_Obj.cnt
        Query_Obj = Sql.GetList(Qury_str)
    # Action button formation
    obj_id = "SYOBJ-00424"
    objh_getid = Sql.GetFirst(
        "SELECT TOP 1  RECORD_ID FROM SYOBJH (NOLOCK) WHERE SAPCPQ_ATTRIBUTE_NAME='" + str(obj_id) + "'"
    )
    if objh_getid:
        obj_id = objh_getid.RECORD_ID
    objs_obj = Sql.GetFirst(
        "select CAN_ADD,CAN_EDIT,CAN_CLONE,CAN_DELETE from SYOBJS where UPPER(NAME)='TAB LIST' and OBJ_REC_ID = '"
        + str(obj_id)
        + "' "
    )
    can_edit = str(objs_obj.CAN_EDIT)
    can_clone = str(objs_obj.CAN_CLONE)
    can_delete = str(objs_obj.CAN_DELETE)

    # Action button formation.
    Action_str = '<div class="btn-group dropdown"><div class="dropdown" id="ctr_drop"><i data-toggle="dropdown" id="dropdownMenuButton" class="fa fa-sort-desc dropdown-toggle" aria-expanded="false"></i><ul class="dropdown-menu left" aria-labelledby="dropdownMenuButton"><li><a class="dropdown-item cur_sty" href="#" onclick="Material_view_obj(this)">VIEW</a></li>'
    if can_edit.upper() == "TRUE":
        Action_str += '<li><a class="dropdown-item cur_sty" href="#" onclick="Material_edit_obj(this)">EDIT</a></li>'
    if can_delete.upper() == "TRUE":
        Action_str += '''<li class="delete_list" style="display: block;"><a class="dropdown-item" href="#" id="deletebtn" onclick="CommonDelete(this, 'SYROMA', 'WARNING')" data-target="#cont_CommonModalDelete" data-toggle="modal">DELETE</a></li>'''
    Action_str += "</ul></div></div>"

    # Values in dictonary formation.
    Select_str = '<label class="middle"><input class="custom" type="checkbox"  onclick="get_checkbox_row_list(this)" /><span class="lbl"></span></label>'
    if Query_Obj is not None:
        for par in Query_Obj:
            data_dict = {}
            try:
                par_name = str(par.ROLE_NAME).encode("ASCII", "ignore")
            except:
                par_name = par.ROLE_NAME
            data_dict["ACTION"] = str(Action_str)
            data_dict["SELECT"] = str(Select_str)
            data_dict["ROLE_RECORD_ID"] = str(par.ROLE_RECORD_ID)
            data_dict["PAR_ROLE_RECORD_ID"] = str(par.PAR_ROLE_RECORD_ID)
            data_dict["ROLE_NAME"] = str(par_name)
            data_dict["ROLE_ID"] = (
                '<a href="#" class="cur_sty" onclick="Material_view_obj(this)">' + str(par.ROLE_ID) + "</a>"
            )
            data_dict["ROLE_DESCRIPTION"] = str(par.ROLE_DESCRIPTION)
            data_dict["START_PAGE"] = str(par.START_PAGE)
            # data_dict['ACTIVE'] = str(par.ACTIVE).lower()
            data_list.append(data_dict)
            Qstr1 = (
                "select top 10000 ROLE_RECORD_ID,ROLE_ID,ROLE_NAME,ROLE_DESCRIPTION,PAR_ROLE_RECORD_ID,PAR_ROLE_ID,START_PAGE from SYROMA where "
                + str(ATTRIBUTE_VALUE_STR)
                + " ROLE_ID = '"
                + str(par.ROLE_ID)
                + "' order by ROLE_ID asc"
            )
            child_obj = Sql.GetList(Qstr1)
            for chil in child_obj:
                child_dict = {}
                child_dict["ACTION"] = str(Action_str)
                child_dict["SELECT"] = str(Select_str)
                child_dict["ROLE_RECORD_ID"] = str(chil.ROLE_RECORD_ID)
                child_dict["PAR_ROLE_RECORD_ID"] = str(chil.PAR_ROLE_RECORD_ID)
                child_dict["ROLE_NAME"] = str(chil.ROLE_NAME.encode("ASCII", "ignore"))
                child_dict["ROLE_ID"] = (
                    '<a href="#" class="cur_sty" onclick="Material_view_obj(this)">' + str(chil.ROLE_ID) + "</a>"
                )
                
                child_dict["ROLE_DESCRIPTION"] = str(chil.ROLE_DESCRIPTION)
                child_dict["START_PAGE"] = str(chil.START_PAGE)
                data_list.append(child_dict)
        filter_control_function += '$("#ejsearch_btn_cat").click( function(){ RoleSearchFuction(); });'
    if QueryCount < int(PerPage):
        PageInformS = "1" + " - " + str(QueryCount) + " of"
    else:
        PageInformS = "1" + " - " + str(PerPage) + " of"
    data_list = [dict(t) for t in {tuple(d.items()) for d in data_list}]
    return data_list, rec_id, filter_control_function, PageInformS, QueryCount



# Param Variable
TABNAME = Param.TABNAME
ACTION = Param.ACTION
try:
    ATTRIBUTE_NAME = Param.ATTRIBUTE_NAME
except:
    ATTRIBUTE_NAME = ""
ATTRIBUTE_VALUE = Param.ATTRIBUTE_VALUE
if ACTION == "LOAD":
    PerPage = "20"
    PageInform = "1___20___20"
    A_Keys = []
    A_Values = []
    if TABNAME == "Roles":
        ApiResponse = ApiResponseFactory.JsonResponse(GetRolesTreeresult(PerPage, PageInform, A_Keys, A_Values))

    elif TABNAME == "RolesFilter":
        A_Keys = list(Param.ATTRIBUTE_NAME)
        A_Values = list(Param.ATTRIBUTE_VALUE)
        PerPage = Param.PerPage
        PageInform = Param.PageInform
        ApiResponse = ApiResponseFactory.JsonResponse(GetRolesTreeresult(PerPage, PageInform, A_Keys, A_Values))
elif ACTION == "PRODUCT_ONLOAD_FILTER":
    if TABNAME == "Roles":
        PerPage = Param.PerPage
        ApiResponse = ApiResponseFactory.JsonResponse(GetRolesTreeResultFilter(ATTRIBUTE_NAME, ATTRIBUTE_VALUE, PerPage))
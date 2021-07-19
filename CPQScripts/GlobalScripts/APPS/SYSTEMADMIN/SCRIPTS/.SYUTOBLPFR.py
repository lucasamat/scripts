# =========================================================================================================================================
#   __script_name : SYUTOBLPFR.PY
#   __script_description : THIS SCRIPT IS USED TO LOAD THE QUERY CONDITION IN SYSTEM ADMIN OBJUCT TAB.
#   __primary_author__ : JOE EBENEZER
#   __create_date :
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================

from SYDATABASE import SQL

Sql = SQL()


def ObjLookupFilters():
    TableName = Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_OBJECT").GetValue()
    MM_OBJ_TBL_NAME = Product.Attributes.GetByName("MM_OBJ_TBL_NAME").GetValue()
    Custom_Api_Name = Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_API_NAME").GetValue()
    if TableName == "":
        TableName = Product.Attributes.GetByName("MM_OBJ_TBL_NAME").GetValue()
    Objd_obj = Sql.GetList("select API_NAME from  SYOBJD (nolock) where OBJECT_NAME = '" + str(TableName).strip() + "'")
    Objd_Where_obj = Sql.GetFirst(
        "select API_NAME, LOOKUP_SQL_QUERY, LOOKUP_SQL_QUERY_LIST from  SYOBJD (nolock) where LOOKUP_API_NAME ='"
        + str(Custom_Api_Name).strip()
        + "' and OBJECT_NAME = '"
        + str(MM_OBJ_TBL_NAME).strip()
        + "'"
    )
    sec_str = ""
    where = ""
    Iswhere = []
    section_str = ""
    Equaity = ["equal", "not_equal", "in", "not_in", "is_null", "is_not_null"]
    Field_Value = ["Field", "Value"]
    wherecondition = ["AND", "OR"]
    if Objd_Where_obj is not None:
        where = Objd_Where_obj.LOOKUP_SQL_QUERY
        if str(Objd_Where_obj.LOOKUP_SQL_QUERY_LIST) is not None and str(Objd_Where_obj.LOOKUP_SQL_QUERY_LIST) != "":
            Iswhere = eval(Objd_Where_obj.LOOKUP_SQL_QUERY_LIST)
    if len(list(Iswhere)) == 0:
        if Objd_obj is not None:
            sec_str += '<select class="form-control lookupcls"><option>..Select</option>'
            for ins in Objd_obj:
                sec_str += "<option>" + str(ins.API_NAME) + "</option>"
            sec_str += "</select>"
        else:
            sec_str += '<div class="col-md-2 left"><input type="text" class="form-control lookupcls"></div>'
        section_str = (
            '<div class="row" style="line-height: 2.0;"><div class="col-md-3 left">Field</div><div class="col-md-3 centre">Operator</div><div class="col-md-3 right">Value/Field</div><div class="col-md-3 right"></div></div><div class="row" style="line-height: 2.0;"><div class="col-md-3 left" id="lookupTest">'
            + str(sec_str)
            + '</div<div class="col-md-3 centre"><select class="form-control lookupcls"><option>equal</option><option>not_equal</option><option>in</option><option>not_in</option><option>is_null</option><option>is_not_null</option></select></div><div class="col-md-3"><select class="form-control lookupcls"><option>Field</option><option>Value</option></select></div><div class="col-md-3 right"><input type="text" class="form-control lookupcls"></div><div id="new_chq" ></div></div><div class="row"><input type="hidden" value="1" id="total_chq"></div>'
        )
    if len(list(Iswhere)) > 0:
        section_str += '<div class="row" style="line-height: 2.0;"><div class="col-md-3 left">Field</div><div class="col-md-3 centre">Operator</div><div class="col-md-3 right">Value/Field</div><div class="col-md-3 right"></div></div>'
        for key, ink in enumerate(list(Iswhere)):
            section_str += '<div class="row" style="line-height: 2.0;">'
            if key != 0:
                section_str += '<div class="col-md-2"><select class="form-control lookupcls">'
                for inf in wherecondition:
                    if str(inf) == str(ink[0]):
                        section_str += "<option selected>" + str(inf) + "</option>"
                    else:
                        section_str += "<option>" + str(inf) + "</option>"
                section_str += "</select></div>"
            if Objd_obj is not None:
                section_str += '<div class="col-md-3 left" id="lookupTest"><select class="form-control lookupcls"><option>..Select</option>'
                for ins in Objd_obj:
                    if str(ins.API_NAME) == ink[1]:
                        section_str += "<option selected>" + str(ins.API_NAME) + "</option>"
                    else:
                        section_str += "<option>" + str(ins.API_NAME) + "</option>"
                section_str += "</select>"
            else:
                section_str += '<div class="col-md-2 left"><input type="text" class="form-control lookupcls"></div>'
            section_str += '</div><div class="col-md-3 centre"><select class="form-control lookupcls">'
            for inj in Equaity:
                if str(inj) == str(ink[2]):
                    section_str += "<option selected>" + str(inj) + "</option>"
                else:
                    section_str += "<option>" + str(inj) + "</option>"
            section_str += '</select></div><div class="col-md-3"><select class="form-control lookupcls">'
            for inm in Field_Value:
                if str(inm) == ink[3]:
                    section_str += "<option selected>" + str(inm) + "</option>"
                else:
                    section_str += "<option>" + str(inm) + "</option>"
            section_str += (
                '</select></div><div class="col-md-3 right"><input type="text" class="form-control lookupcls" value="'
                + str(ink[4])
                + '"></div>'
            )
            section_str += (
                '<div id="new_chq" ></div></div><div class="row"><input type="hidden" value="'
                + str(key + 1)
                + '" id="total_chq"></div>'
            )
    return section_str


def ObjLookupFilter():
    sec_str = (
        '<div class="col-md-2"><select class="form-control lookupcls"><option>AND</option><option>OR</option></select></div>'
    )
    TableName = Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_OBJECT").GetValue()
    Objd_obj = Sql.GetList("select API_NAME from  SYOBJD (nolock) where OBJECT_NAME = '" + str(TableName).strip() + "'")
    if Objd_obj is not None:
        sec_str += '<div class="col-md-2 left"><select class="form-control lookupcls"><option>..Select</option>'
        for ins in Objd_obj:
            sec_str += "<option>" + str(ins.API_NAME) + "</option>"
        sec_str += "</select></div>"
    else:
        sec_str += '<div class="col-md-2 left"><input type="text" class="form-control lookupcls"></div>'
    sec_str += '<div class="col-md-2 centre"><select class="form-control lookupcls"><option>equal</option><option>not_equal</option><option>in</option><option>not_in</option><option>is_null</option><option>is_not_null</option></select></div>'
    sec_str += '<div class="col-md-3"><select class="form-control lookupcls"><option>Field</option><option>Value</option></select> </div>'
    sec_str += '<div class="col-md-2 right"><input type="text" class="form-control lookupcls"></div>'
    sec_str += '<div class="col-md-1"><a onclick="Obj_remove()">Clear</a></div><div class="row"><input type="hidden" value="" id="total_chq"></div>'
    return sec_str


if Param.ACTION == "FIRST":
    ApiResponse = ApiResponseFactory.JsonResponse(ObjLookupFilters())
elif Param.ACTION == "SECOND":
    ApiResponse = ApiResponseFactory.JsonResponse(ObjLookupFilter())


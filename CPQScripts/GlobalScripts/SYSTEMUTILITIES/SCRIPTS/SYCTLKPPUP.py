# =========================================================================================================================================
#   __script_name : SYCTLKPPUP.PY
#   __script_description : THIS SCRIPT IS USED TO DISPLAY THE LOOKUP POPUP WHEN USERS CLICK THE ADD OR EDIT ACTION BUTTONS ON A RELATED LIST RECORD.
#   __primary_author__ : JOE EBENEZER
#   __create_date :
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct
import re
from SYDATABASE import SQL
import SYCNGEGUID as CPQID

Sql = SQL()

def GSCONTLOOKUPPOPUP(
    TABLEID, OPER, TABLENAME, KEYDATA, ARRAYVAL, PRICEMODEL_ID, LOOKUP_ID, MARKET_TYPE, MODEL_TYPE, PRODUCT_TYPE,TESTEDOBJECT,TRACKEDTESTEDOBJECT,MAPPINGSAPPROVALOBJECT
):
    Trace.Write("lookup=------"+str(LOOKUP_ID))
    a_TABLEID = TABLEID
    a_test = ""
    A_value = ""
    if TABLEID != "" and TABLEID.find("___") != -1:
        TABLEID = a_TABLEID.split("___")[0]
        A_value = a_TABLEID.split("___")[1]
        OPER = "Price_class_popup"
        a_test = "attr_not_available"
    ARRAYVALL = {}
    ARRAYVALL = ARRAYVAL
    ATTRIBUTE_NAME_list = []
    att_list = []
    tab_Name = ""
    tableId = ""
    x_objname_list = []
    x_objname = ""
    get_segment_obj = ""
    var_str = ""
    pagination_app_total_count=0
    ContractRecordId = Product.GetGlobal("contract_record_id")
    try:
        quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
    except:
        quote_revision_record_id = ""
    xx_objname = SegmentsClickParam = VAL_Obj = xz_objname = ""
    
    if TABLENAME is not None:
        if TABLENAME.find("_") != -1:
            x_objname_list = TABLENAME.split("_")
            xz_objrid = x_objname_list[2] + "-" + x_objname_list[3]
            x_obJr = Sql.GetFirst("SELECT OBJ_REC_ID FROM SYOBJR WHERE SAPCPQ_ATTRIBUTE_NAME='" + str(xz_objrid) + "'")
            if x_obJr:
                xz_objname = x_obJr.OBJ_REC_ID
            x_obJ = Sql.GetFirst("SELECT OBJECT_NAME FROM SYOBJH WHERE RECORD_ID='" + str(xz_objname) + "'")
            if x_obJ is not None:
                xx_objname = x_obJ.OBJECT_NAME
    # siva--end
    if str(TABLEID).find("|") != -1:
        tableId = TABLEID.split("|")[0]
    try:
        for tab in Product.Tabs:
            if tab.IsSelected == True:
                tab_Name = tab.Name
    except:
        pass
    x_obJ = Sql.GetFirst("SELECT OBJECT_NAME FROM SYOBJH WHERE RECORD_ID='" + str(xz_objname) + "'")
    if x_obJ is not None:
        xx_objname = x_obJ.OBJECT_NAME
    if TESTEDOBJECT in("SOURCE ACCOUNT","BILL TO","SHIP TO","SOLD TO","PAYER","SELLER"):
        TABLEID ="SAACNT"
    elif TESTEDOBJECT =="SALES UNIT":
        TABLEID ="SAQTMT"
    try:
        if Quote.GetGlobal("TreeParam") == "Receiving Equipment":
            TABLEID = "SAQSCO"
            LOOKUP_ID = "FABLOCATION_ID"
    except:
        pass
    if tableId == "":
        Header_Obj = Sql.GetFirst("SELECT LABEL,RECORD_NAME FROM SYOBJH (nolock) WHERE OBJECT_NAME='" + str(TABLEID) + "'")
    DATA_OBJ = Sql.GetFirst(
        "SELECT COLUMNS FROM SYOBJS (nolock) WHERE CONTAINER_NAME='" + str(TABLEID) + "' AND NAME='Lookup list'"
    )

    sec_str = ""
    filter_control_function = ""
    value_dict_list = []
    TABLEIDS = ""
    PRICE_MOD_ID = ""
    PRICE_MODEL_ID = ""
    flag = 0
    idss = []

    # A043S001P01-10888 START
    if OPER == "YES" and TABLEID != "USERS":
        # # A043S001P01-10888 END
        oncli = "namePOPUPFormatternew"
        back_btn = "cont_openaddnew_back()"
        btn_clear = "addnew_clear_selection(this)"
    # A043S001P01-12867 end
    elif OPER == "YES" and TABLEID == "USERS":
        oncli = "namePOPUPFormatternew"
        back_btn = "cont_openaddnew_back()"
        btn_clear = "userRoles_clear(this)"
        # A043S001P01-10888 END
    elif OPER == "NO":
        oncli = "namePOPUPFormatter"
        back_btn = "popup_cont_EDIT()"
        btn_clear = "edit_clear_selection(this)"
    elif OPER == "PASGMT":
        oncli = "SGnamePOPUPFormatter"
        btn_clear = "edit_clear_selection_segment(this)"
        back_btn = "seg_popup_edit(this)"
    elif OPER == "CLONE":
        oncli = "namePOPUPFormatterClone"
        back_btn = "popup_cont_clone()"
        btn_clear = "clone_clear_selection(this)"
    elif OPER == "PIVOT":
        oncli = "namePOPUPFormatterPivot"
        back_btn = "popup_cont_pivot_back()"
        btn_clear = "pivot_clear_selection(this)"
    elif OPER == "PIVOT_CHK":
        oncli = "namePOPUPFormatternew"
        back_btn = "cont_openaddnew_back()"
        btn_clear = "addnew_clear_selection(this)"
    elif OPER == "PIVOT_CHECK":
        oncli = "namePOPUPFormatternew"
        back_btn = "cont_lookup_attr_new(this)"
        btn_clear = "saveAttMaterial(this)"
    elif OPER == "MATERIALATTRPIVOT":
        oncli = "namePOPUPFormattermtrlattrpivot"
        back_btn = "cont_lookup_mtrlattr_new(this)"
        btn_clear = "saveMtrlAttMaterial(this)"
    elif OPER == "PIVOT_CHECK_SET":
        oncli = "namePOPUPFormattersetcheck"
        back_btn = "cont_lookup_set_attrcheck_new(this)"
        btn_clear = "saveAttMaterial(this)"
    elif OPER == "Price_class_popup":
        oncli = "namePrice_class_popup"
        back_btn = "namePrice_class_popupback()"
        btn_clear = "namePrice_class_popupclear(this)"
    elif OPER == "PRICE AGREEMENT":
        oncli = "namePOPUPFormatterSegmt"
        back_btn = "popup_cont_Segmt_back()"
        btn_clear = "segmt_clear_selection(this)"
    elif OPER == "SEGMENTADDNEW":
        oncli = "namePOPUPFormatterSegmtAdd"
        back_btn = "popup_add_cont_Segmt_back()"
        btn_clear = "segmt_addnew_clear_selection(this)"
    elif OPER == "SEGMENTDELPLNT":
        oncli = "namePOPUPFormatterSegmtDP"
        back_btn = "popup_add_cont_SegmtDP_back()"
        btn_clear = "segmtDP_addnew_clear_selection(this)"
    elif OPER == "MATERIALTREE":
        oncli = "MatrlTreeNameFormatter"
        back_btn = "popup_add_cont_mtrlTree_back()"
        btn_clear = "mtrlTree_addnew_clear_selection(this)"
    elif OPER == "SEGMENTTREETREE":
        oncli = "SegmtTreeNameFormatter"
        back_btn = "popup_add_cont_sgmtTree_back()"
        btn_clear = "sgmtTree_addnew_clear_selection(this)"
    elif OPER == "PRIMODELTREE":
        oncli = "PriceModelTreeNameFormatter"
        back_btn = "popup_add_cont_PriceModelTree_back()"
        btn_clear = "PriceModelTree_addnew_clear_selection(this)"
    elif OPER == "CommonTreeView":
        oncli = "CommonTreePlaceHolder"
        back_btn = "CommonTreeBackOnclick()"
        btn_clear = "CommonTree_clear_selection(this)"
    elif OPER == "ProfileTreeView":
        oncli = "ProfileTreePlaceHolder"
        back_btn = "ProfileTreeBackOnclick()"
        btn_clear = "ProfileTree_clear_selection(this)"
    else:
        oncli = "namePOPUPFormatterRelatedList"
        back_btn = "cont_relatedlist_openedit(this)"
        btn_clear = "relatededit_clear_selection(this)"
    val = ""
    if OPER == "PIVOT_CHECK":
        sec_str += (
            '<div   class="row modulebnr brdr">'
            + str(Header_Obj.LABEL).upper()
            + " LOOKUP LIST"
            + '<button type="button"   class="close fltrt" data-dismiss= "modal" >X</button></div>'
        )

        sec_str += '<div class="col-md-12"><div class="row pad-10 bg-lt-wt brdr">'
        sec_str += (
            '<button type="button" class="btnconfig" id="'
            + str(OPER)
            + "|"
            + str(TABLEID)
            + '" data-dismiss= "modal">CANCEL</button>'
        )
        sec_str += (
            '<button type="button" class="btnconfig" id="'
            + str(TABLEID)
            + "|"
            + str(str(Header_Obj.RECORD_NAME))
            + '" onclick="'
            + back_btn
            + '">SAVE</button>'
        )
        sec_str += "</div></div>"
        sec_str += '<div id="container" class="g4 pad-10 brdr except_sec">'
    elif OPER == "PIVOT_CHECK_SET":
        sec_str += (
            '<div class="row modulebnr brdr">'
            + str(Header_Obj.LABEL).upper()
            + " LIST"
            + '<button type="button"   class="close fltrt" data-dismiss= "modal" >X</button></div>'
        )
        sec_str += '<div class="col-md-12"><div class="row pad-10 bg-lt-wt brdr">'
        sec_str += (
            '<button type="button" class="btnconfig" id="'
            + str(OPER)
            + "|"
            + str(TABLEID)
            + '" data-dismiss= "modal">CANCEL</button>'
        )
        sec_str += (
            '<button type="button" class="btnconfig" id="'
            + str(TABLEID)
            + "|"
            + str(str(Header_Obj.RECORD_NAME))
            + '" onclick="'
            + btn_clear
            + '">SAVE</button>'
        )
        sec_str += "</div></div>"
        sec_str += '<div id="container" class="g4 pad-10 brdr except_sec">'
    elif LOOKUP_ID == "PARTY_ID":
        sec_str += (
            '<div style="margin-bottom: -1px;" class="row modulebnr brdr">'
            + str(eval("Header_Obj.LABEL")).upper()
            + " LOOKUP LIST"
            + '<button type="button" style="float:right;" class="close"  data-dismiss= "modal">X</button></div>'
        )
        sec_str += '<div class="col-md-12"><div class="row pad-10 bg-lt-wt brdr"><img style="height: 40px; margin-top: -1px; margin-left: -1px; float: left;" src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/Secondary Icon.svg"><div class="product_txt_div_child secondary_highlight" style="display: block;text-align: left;"><div class="product_txt_child"><abbr title="Key">Acoount ID</abbr></div><div class="product_txt_to_top_child"><abbr title="ALL">ALL</abbr></div></div><div class="product_txt_div_child secondary_highlight" style="display: block;text-align: left;"><div class="product_txt_child"><abbr title="Key">Account Name</abbr></div><div class="product_txt_to_top_child"><abbr title="ALL">ALL</abbr></div></div><button type="button" class="btnconfig" id="' + str(TABLEID) + "|" + str(str(Header_Obj.RECORD_NAME)) + '" onclick="' + btn_clear + '">CLEAR SELECTION</button>'
        # sec_str += (
        #     '<button type="button" class="btnconfig" id="'
        #     + str(TABLEID)
        #     + "|"
        #     + str(str(Header_Obj.RECORD_NAME))
        #     + '" onclick="'
        #     + btn_clear
        #     + '">CLEAR SELECTION</button>'
        # )
        sec_str += "</div></div>"
        sec_str += '<div id="container" class="g4 pad-10 brdr except_sec">'
    else:
        sec_str += (
            '<div style="margin-bottom: -1px;" class="row modulebnr brdr">'
            + str(eval("Header_Obj.LABEL")).upper()
            + " LOOKUP LIST"
            + '<button type="button" style="float:right;" class="close"  data-dismiss= "modal">X</button></div>'
        )
        sec_str += '<div class="col-md-12"><div class="row pad-10 bg-lt-wt brdr">'
        sec_str += (
            '<button type="button" class="btnconfig" id="'
            + str(TABLEID)
            + "|"
            + str(str(Header_Obj.RECORD_NAME))
            + '" onclick="'
            + btn_clear
            + '">CLEAR SELECTION</button>'
        )
        sec_str += "</div></div>"
        sec_str += '<div id="container" class="g4 pad-10 brdr except_sec">'
        
    if DATA_OBJ is not None:
        VAL_Str = ""
        where = ""

        if LOOKUP_ID != "" and xx_objname != "" and str(TABLEID) != "USERS":
            WhereStr = (
                "SELECT LOOKUP_SQL_QUERY FROM  SYOBJD (NOLOCK) where OBJECT_NAME = '"
                + str(xx_objname)
                + "' and LOOKUP_API_NAME = '"
                + str(LOOKUP_ID)
                + "'"
            )
            where_obj = Sql.GetFirst(WhereStr)
            if where_obj is not None:
                where = where_obj.LOOKUP_SQL_QUERY
            if where and where != "":
                if where.find("<") != -1:
                    m_where = re.findall("<(.+?)>", where)
                    if m_where:
                        for found in m_where:
                            where_text = "<" + str(found) + ">"
                            where_parse = Product.ParseString(where_text)
                            where = where.replace(where_text, where_parse)
        if TABLEID == "SVPGAL":
            NAME = str(DATA_OBJ[1:-1])
        else:
            NAME = str(DATA_OBJ.COLUMNS[1:-1]).replace('"', "'").replace("[","").replace("]","")
        if tab_Name == "Set" and str(TABLEID) == "MAATTR":
            RecAttValue = Product.Attributes.GetByName("QSTN_SYSEFL_MA_00263").GetValue()
            Atrribute_Obj = Sql.GetList(
                "select top 1000 ATTRIBUTE_NAME from MASTAT where SET_RECORD_ID = '"
                + str(RecAttValue)
                + "' ORDER BY CpqTableEntryId desc"
            )
            ATTRIBUTE_NAME_list = [str(inc.ATTRIBUTE_NAME).upper() for inc in Atrribute_Obj if inc.ATTRIBUTE_NAME]
        END_OBJ = Sql.GetList(
            "SELECT top 1000 API_NAME,FIELD_LABEL,DATA_TYPE FROM  SYOBJD WHERE OBJECT_NAME='"
            + str(TABLEID)
            + "' AND API_NAME in ("
            + NAME
            + ") ORDER BY DISPLAY_ORDER"
        )

        RelTABEL_NAME = ""
        API_NAME_list = [ins.API_NAME for ins in END_OBJ]
        API_NAME_str = ",".join(API_NAME_list)
        Trace.Write('API_NAME_str==='+str(API_NAME_str))
        FIELD_LABEL_list = [ins.FIELD_LABEL for ins in END_OBJ]
        LABEL_list = [{ins.FIELD_LABEL: ins.API_NAME} for ins in END_OBJ]
        FIELD_LABEL_str = ",".join(FIELD_LABEL_list)
        CHECKBOX_LIST = []
        for ins in END_OBJ:
            if str(ins.DATA_TYPE) == "CHECKBOX":
                CHECKBOX_LIST.append(str(ins.API_NAME))
        RelTABEL_NAME = ""
        Trace.Write('RelTABEL_NAME==='+str(RelTABEL_NAME))
        if RelTABEL_NAME != "QSTN_R_SYOBJR_80011":
            SegmentsClickParam = Product.GetGlobal("TreeParam")
            TreeParentParam = Product.GetGlobal("TreeParentLevel0")
            if str(tab_Name) == "Object" and str(TABLEID) == "SYOBJD":
                # VAL_Str = "SELECT top 1000 "+ str(API_NAME_str)+ " FROM "+ str(TABLEID)+ " WHERE "+ str(where)
                Recvalue = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00701").GetValue()
                if LOOKUP_ID not in ["DEPENDENT_FIELD","OBJECTFIELD_APINAME"]:
                    VAL_Str = (
                        "SELECT top 1000 "
                        + str(API_NAME_str)
                        + " FROM "
                        + str(TABLEID)
                        + " WHERE DATA_TYPE IN ('PICKLIST','CHECKBOX') and PARENT_OBJECT_RECORD_ID = '"
                        + str(Recvalue)
                        + "'"
                    )
                elif LOOKUP_ID == "OBJECTFIELD_APINAME":
                    VAL_Str = (
                        "SELECT top 10 "
                        + str(API_NAME_str)
                        + " FROM "
                        + str(TABLEID)
                        + " WHERE  PARENT_OBJECT_RECORD_ID = '"
                        + str(Recvalue)
                        + "'"
                    )
                    count_query=Sql.GetList("SELECT COUNT(*) as cnt FROM "+ str(TABLEID)+" WHERE  PARENT_OBJECT_RECORD_ID = '"+ str(Recvalue)+ "'")
                else:
                    VAL_Str = (
                        "SELECT top 1000 "
                        + str(API_NAME_str)
                        + " FROM "
                        + str(TABLEID)
                        + " WHERE DATA_TYPE IN ('PICKLIST','CHECKBOX') and PARENT_OBJECT_RECORD_ID = '"
                        + str(Recvalue)
                        + "'"
                    )
                VAL_Obj = Sql.GetList(VAL_Str)

            elif str(tab_Name) == "Approval Chain" and str(TABLEID) == "SYOBJD" and str(SegmentsClickParam) == "Approval Chain Steps":
                Header_Obj = Sql.GetFirst("SELECT OBJECT_NAME FROM SYOBJH WHERE LABEL = '{}'".format(TESTEDOBJECT))
                object_name = Header_Obj.OBJECT_NAME
                if Header_Obj is not None:
                    VAL_Str = (
                        "SELECT top 1000 "
                        + str(API_NAME_str)
                        + " FROM "
                        + str(TABLEID)
                        + " WHERE OBJECT_NAME = '{}'".format(object_name)
                    )
                VAL_Obj = Sql.GetList(VAL_Str)
            # elif str(tab_Name) =="Quote" and TABLEID == 'PRTXCL':
                # classification_obj = Sql.GetFirst("select SRVTAXCAT_ID from SAQITM where QUOTE_RECORD_ID = '{quote_record_id}' and SERVICE_ID = '{service_id}'  AND QTEREV_RECORD_ID = '{quote_revision_record_id}' ".format(quote_record_id = Quote.GetGlobal("contract_quote_record_id"),service_id = '-'.join(SegmentsClickParam.split('-')[1:]).strip(),quote_revision_record_id))
                # TESTEDOBJECT = classification_obj.SRVTAXCAT_ID
                # VAL_Str = ("SELECT top 1000 TAX_CLASSIFICATION_RECORD_ID,TAX_CLASSIFICATION_DESCRIPTION,TAX_CLASSIFICATION_ID FROM PRTXCL WHERE TAXCATEGORY_ID = '{TESTEDOBJECT}' and TAX_CLASSIFICATION_TYPE = 'MATERIAL' ".format(TESTEDOBJECT = TESTEDOBJECT))
                # VAL_Obj = Sql.GetList(VAL_Str)
            elif str(tab_Name) =="Quote" and str(SegmentsClickParam)=="Quote Information" and xx_objname == 'SAQTIP' and TABLEID != "MAFBLC":
                if TESTEDOBJECT in("BILL TO","SHIP TO","SOLD TO","PAYER","SELLER"):
                    VAL_Str = (
                        "SELECT top 1000 ACCOUNT_RECORD_ID,ACCOUNT_ID,ACCOUNT_NAME FROM SAACNT"
                    ) 
                elif TESTEDOBJECT =="SOURCE ACCOUNT":
                    ContractRecordId = str(Quote.GetGlobal("contract_quote_record_id"))
                    VAL_Str = (
                        "SELECT top 1000 ACCOUNT_RECORD_ID,ACCOUNT_ID,ACCOUNT_NAME FROM SAACNT WHERE ACCOUNT_RECORD_ID NOT IN (SELECT ACCOUNT_RECORD_ID FROM SAQTMT (NOLOCK) WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}')".format(ContractRecordId,quote_revision_record_id)
                    )
                elif TESTEDOBJECT =="SALES UNIT":
                    VAL_Str = (
                        "SELECT top 1000 MASTER_TABLE_QUOTE_RECORD_ID,ACCOUNT_NAME FROM SAQTMT"
                    )
                VAL_Obj = Sql.GetList(VAL_Str)
            

            elif str(tab_Name) == "Approval Chain" and str(TABLEID) == "SYOBJD" and str(TreeParentParam) == "Approval Chain Steps":
                Header_Obj = Sql.GetFirst("SELECT OBJECT_NAME FROM SYOBJH WHERE LABEL = '{}'".format(TRACKEDTESTEDOBJECT))
                object_name = Header_Obj.OBJECT_NAME
                if Header_Obj is not None:
                    VAL_Str = (
                        "SELECT top 1000 "
                        + str(API_NAME_str)
                        + " FROM "
                        + str(TABLEID)
                        + " WHERE OBJECT_NAME = '{}'".format(object_name)
                    )
                VAL_Obj = Sql.GetList(VAL_Str)
            elif str(tab_Name) == "Approval Chain" and str(TABLEID) == "SYOBJD" and (str(SegmentsClickParam) == "Approval Chain Status Mappings" or str(TreeParentParam) == "Approval Chain Status Mappings"):
                Header_Obj = Sql.GetFirst("SELECT OBJECT_NAME FROM SYOBJH WHERE LABEL = '{}'".format(MAPPINGSAPPROVALOBJECT))
                object_name = Header_Obj.OBJECT_NAME
                if Header_Obj is not None:
                    VAL_Str = (
                        "SELECT top 1000 "
                        + str(API_NAME_str)
                        + " FROM "
                        + str(TABLEID)
                        + " WHERE OBJECT_NAME = '{}'".format(object_name)
                    )
                VAL_Obj = Sql.GetList(VAL_Str) 
            elif str(TABLEID) == "MAFBLC" and str(tab_Name) =="Quote":
                ContractRecordId = str(Quote.GetGlobal("contract_quote_record_id"))
                quote_obj = Sql.GetFirst("select ACCOUNT_ID from SAQTMT where MASTER_TABLE_QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(ContractRecordId,quote_revision_record_id))
                account_id = quote_obj.ACCOUNT_ID
                VAL_Str = "SELECT top 10000 * FROM MAFBLC WHERE ACCOUNT_ID like '%{account_id}%'".format(account_id = account_id)
                VAL_Obj = Sql.GetList(VAL_Str)
            elif tab_Name=="Role":
                user = Sql.GetList("SELECT USER_NAME FROM SYROUS (NOLOCK)")
                if user:
                    for userss in user:
                        VAL_Str = ("SELECT top 10 ID,NAME,EMAIL FROM USERS WHERE NAME != '{}'".format(userss.USER_NAME))
                        VAL_Obj = Sql.GetList(VAL_Str)
                        count_query=SqlHelper.GetList("SELECT COUNT(*) as cnt FROM USERS WHERE NAME != '{}'".format(userss.USER_NAME))
                else:
                    VAL_Str = "SELECT top 1000 ID,NAME,EMAIL FROM USERS"
                    VAL_Obj = Sql.GetList(VAL_Str)
                    count_query=SqlHelper.GetList("SELECT COUNT(*) as cnt FROM USERS ")
            elif str(TABLEID) == "cpq_permissions":
                VAL_Str = "SELECT top 10 permission_id,SYSTEM_ID,permission_name FROM cpq_permissions where permission_type ='0'"
                VAL_Obj = Sql.GetList(VAL_Str)
                count_query=SqlHelper.GetList("SELECT COUNT(*) as cnt FROM cpq_permissions where permission_type ='0'")
            else:
                Trace.Write('At 437'+str(TABLEID)+"tab_Name"+str(tab_Name))
                if str(where).strip() != "":
                    where = " where " + str(where)
                    VAL_Str = "SELECT top 10 " + str(API_NAME_str) + " FROM " + str(TABLEID) + " " + str(where)
                    count_query=SqlHelper.GetList("SELECT COUNT(*) as cnt FROM " + str(TABLEID) + " " + str(where))
                elif str(TABLEID) == "SYTRND" and tab_Name == "Page":
                    VAL_Str = "SELECT * FROM SYTRND where PARENTNODE_OBJECT = 'TRUE'"
                    VAL_Obj = Sql.GetList(VAL_Str)
                elif str(TABLEID) == "SAQSCO":
                    VAL_Str = "SELECT DISTINCT *  from SAQFBL WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND RELOCATION_FAB_TYPE = 'RECEIVING FAB' ".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id)
                    VAL_Obj = Sql.GetList(VAL_Str)
                # elif str(TABLEID) == "SYOBJR":
                #     VAL_Str = "SELECT top 10 * " + " FROM " + str(TABLEID)
                #     count_query = SqlHelper.GetList("SELECT COUNT(*) as cnt FROM " + str(TABLEID))
                elif str(TABLEID) == "SYOBJR":
                    VAL_Str = "SELECT top 10 " + str(API_NAME_str) + " FROM " + str(TABLEID)
                    count_query = SqlHelper.GetList("SELECT COUNT(*) as cnt FROM " + str(TABLEID))
                elif str(TABLEID) == "SYPFTY":
                    Trace.Write("TABLEID====>>>"+str(TABLEID))
                    ContractRecordId = str(Quote.GetGlobal("contract_quote_record_id"))
                    VAL_Str = (" SELECT top 1000 PARTNERFUNCTION_RECORD_ID,C4C_PARTNER_FUNCTION,CRM_PARTNERFUNCTION FROM SYPFTY WHERE C4C_PARTNER_FUNCTION != '' AND C4C_PARTNER_FUNCTION NOT IN(SELECT C4C_PARTNERFUNCTION_ID FROM SAQDLT WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}')".format(ContractRecordId,quote_revision_record_id))
                    VAL_Obj = Sql.GetList(VAL_Str)
                elif str(TABLEID) == "SAEMPL":
                    Trace.Write("TABLEID====>>>"+str(TABLEID))
                    ContractRecordId = str(Quote.GetGlobal("contract_quote_record_id"))
                    VAL_Str = (" SELECT EMPLOYEE_RECORD_ID,EMPLOYEE_ID,EMPLOYEE_NAME,EMAIL FROM SAEMPL WHERE EMPLOYEE_ID NOT IN(SELECT MEMBER_ID FROM SAQDLT WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}')".format(ContractRecordId,quote_revision_record_id))
                    VAL_Obj = Sql.GetList(VAL_Str) 
                else:
                    VAL_Str = "SELECT top 10 " + str(API_NAME_str) + " FROM " + str(TABLEID)
                    count_query = SqlHelper.GetList("SELECT COUNT(*) as cnt FROM " + str(TABLEID))
                VAL_Obj = Sql.GetList(VAL_Str)
            ##pagiantion format issue fix  
            #Trace.Write("VAL_Obj"+str(VAL_Obj))        
            #if VAL_Obj and pagination_app_total_count == 0:
                #Trace.Write("inside")
            #    pagination_app_total_count = len(VAL_Obj)
            ##pagiantion format issue fix 

        else:
            if str(where).strip() != "":
                where = " where " + str(where)
                #Trace.Write("where-------->" + str(where))
            VAL_Str = "SELECT top 100 " + str(API_NAME_str) + " FROM " + str(TABLEID) + " " + str(where)
            VAL_Obj = Sql.GetList(VAL_Str)
        #Trace.Write("VAL_Str-------------------------------------> " + str(VAL_Str))
        
        ids = API_NAME_list[0]
        Trace.Write('ids==='+str(ids))
        TABLEIDS = "table_" + TABLEID
        sec_str += (
            '<table id="'
            + str(TABLEIDS)
            + '" data-escape="true" data-search-on-enter-key="true" data-pagination="true" data-page-list="[5, 10, 20, 50, 100]"  data-page-size="10" data-show-header="true"  data-filter-control="true"> <thead><tr>'
        )
        values_list = ""
        
        if OPER == "PIVOT_CHK":
            sec_str += '<th data-field="dd" data-checkbox="true"></th>'
        if OPER == "PIVOT_CHECK":
            sec_str += '<th data-field="dd" data-checkbox="true" checked></th>'
        if OPER == "PIVOT_CHECK_SET":
            sec_str += '<th data-field="dd" data-checkbox="true" checked></th>'
        for invs in list(API_NAME_list[1:]):
            filter_clas = "#container .bootstrap-table-filter-control-" + str(invs)
            values_list += "var " + str(invs) + ' = $("' + str(filter_clas) + '").val(); '
            values_list += "ATTRIBUTE_VALUEList.push(" + str(invs) + "); "
        for key, header in enumerate(FIELD_LABEL_list[1:]):
            api_name_dict_list = [dicts for dicts in LABEL_list if dicts.get(header)]
            api_name_header = ""
            if len(api_name_dict_list) > 0:
                api_name_header = api_name_dict_list[0].get(str(header))
                filter_class = "#container .bootstrap-table-filter-control-" + str(api_name_header)
                filter_control_function += (
                    '$("'
                    + filter_class
                    + '").change( function(){ var modal_id = "";  var table_id = $(this).closest("table").attr("id"); if( table_id == "table_PRPRCL") { modal_id = $("input#PRICEMODEL_ID").val(); } var ATTRIBUTE_VALUEList = []; '
                    + str(values_list)
                    + ' var attribute_value = $(this).val(); cpq.server.executeScript("SYCTLKPPUP", {"TABLEID":"'
                    + str(TABLEID)
                    + '","OPER":"'
                    + str(OPER)
                    + '", "ATTRIBUTE_NAME": '
                    + str(list(API_NAME_list[1:]))
                    + ', "ATTRIBUTE_VALUE": ATTRIBUTE_VALUEList,"GSCONTLOOKUP": "GSCONTLOOKUP", "TABLENAME":"'
                    + str(TABLENAME)
                    + '" , "KEYDATA":"'
                    + str(KEYDATA)
                    + '","ARRAYVAL":\''
                    + str(dict(ARRAYVAL)).replace("'", "\\'")
                    + '\', "PRICE_MOD_ID": "'
                    + str(PRICEMODEL_ID)
                    + '", "PRICEMODEL_ID": "", "LOOKUP_ID": "'
                    + str(LOOKUP_ID)
                    + '" , "TESTEDOBJECT": "'
                    + str(TESTEDOBJECT)
                    + '" , "TRACKEDTESTEDOBJECT": "'
                    + str(TRACKEDTESTEDOBJECT)
                    + '" , "MAPPINGSAPPROVALOBJECT": "'
                    + str(MAPPINGSAPPROVALOBJECT)
                    + '" }, function(data) { $("#'
                    + str(TABLEIDS)
                    + '").bootstrapTable("load", data);Pagination_GS_ADD_NEW_POPUP(attribute_value,data.length);if(data==""){ $("#'
                    + str(TABLEIDS)
                    + ' tbody").html("<tr class=\'noRecDisp\'><td colspan=2 class=\'txtltimp\'>No Records to Display</td></tr>");$("#popup_footer").hide();} }); });'
                )
                if key == 0:
                    sec_str += (
                        '<th data-field="'
                        + str(api_name_header)
                        + '" data-sortable="true" data-pagination="true" data-formatter="'
                        + str(oncli)
                        + '"  data-filter-control="input">'
                        + str(header)
                        + "</th>"
                    )
                else:
                    if str(api_name_header) in CHECKBOX_LIST:
                        sec_str += (
                            '<th  data-field="'
                            + str(api_name_header)
                            + '" data-filter-control="input" data-align="center" data-title-tooltip="'
                            + str(header)
                            + '" data-formatter="CheckboxFieldRelatedList" data-sortable="true">'
                            + str(header)
                            + "</th>"
                        )
                    elif str(api_name_header) == "EFFECTIVEDATE_BEG":
                        sec_str += (
                            '<th data-field="'
                            + str(api_name_header)
                            + '" data-sortable="true" data-align="center" data-filter-control="input">'
                            + str(header)
                            + "</th>"
                        )

                    else:
                        sec_str += (
                            '<th data-field="'
                            + str(api_name_header)
                            + '" data-sortable="true" data-filter-control="input">'
                            + str(header)
                            + "</th>"
                        )
        sec_str += "</tr></thead><tbody></tbody></table><div id=\'popup_footer\'></div></div>"
        for obj_name in VAL_Obj:
            value_dict = {}
            if OPER == "PIVOT_CHECK_SET":
                if str(obj_name.ATTRIBUTE_NAME).upper() in ATTRIBUTE_NAME_list:
                    value_dict["dd"] = "true"
                # else:
                # Trace.Write('else')
                # value_dict['dd'] = 'false'

            objsk = "obj_name." + str(ids)
            idss = str(eval(objsk)) + "|" + str(ids)
            for tes in API_NAME_list[1:]:
                value_dict["ids"] = idss
                try:

                    tes = tes.decode("unicode_escape").encode("utf-8")

                    # value_dict[tes] = str(eval("obj_name."+str(tes))).decode('unicode_escape').encode('utf-8')
                    values= str(eval("obj_name." + str(tes)))
                    value_dict[tes] = values.upper()
                except:

                    tes = tes.decode("unicode_escape").encode("utf-8")
                    # value_dict[tes] = eval("obj_name."+str(tes)).decode('unicode_escape').encode('utf-8')
                    #values= str(eval("obj_name." + str(tes)))
                    #value_dict[tes] = values.upper()
            value_dict_list.append(value_dict)
            

    else:
        sec_str += '<div class="txt_center">No matching records found </div>'
    #Trace.Write("sec_str" + str(sec_str)+"value_dict_list" + str(value_dict_list)+"TABLEIDS" + str(TABLEIDS))
    #Trace.Write("filter_control_function" + str(filter_control_function)+str(pagination_app_total_count))
    try:
        pagination_app_total_count=count_query[0].cnt
    except:
        pagination_app_total_count=0
    if pagination_app_total_count>0:
        var_str += """<div class="col-md-12 brdr listContStyle padbthgt30">
                            <div class="col-md-4 pager-numberofitem  clear-padding">
                                <span class="pager-number-of-items-item flt_lt_pad2_mar2022" id="Rec_App_Start_End">{Records_App_Start_And_End}</span>
                                <span class="pager-number-of-items-item flt_lt_pad2_mar" id="TotalRecAppCount">{Pagination_TotalApp_Count}</span>
                                    <div class="clear-padding fltltmrgtp3">
                                        <div class="pull-right vralign">
                                            <select onchange="ShowResultCountFunction_GS_ADD_NEW_POPUP(this,'SYCTLKPPUP')" id="ShowResultCountsApp" class="form-control selcwdt">
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
                                            <li class="disabled"><a onclick="GetFirstResultFunction_GS_ADD_NEW_POPUP('SYCTLKPPUP')" ><i class="fa fa-caret-left fnt14bold"></i><i class="fa fa-caret-left fnt14"></i></a></li>
                                            <li class="disabled"><a onclick="GetPreviuosResultFunction_GS_ADD_NEW_POPUP('SYCTLKPPUP')"><i class="fa fa-caret-left fnt14"></i>PREVIOUS</a></li>
                                            <li class="disabled"><a onclick="GetNextResultFunction_GS_ADD_NEW_POPUP('SYCTLKPPUP')">NEXT<i class="fa fa-caret-right fnt14"></i></a></li>
                                            <li class="disabled"><a onclick="GetLastResultFunction_GS_ADD_NEW_POPUP('SYCTLKPPUP')"><i class="fa fa-caret-right fnt14"></i><i class="fa fa-caret-right fnt14bold"></i></a></li>
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
    Pager = (
        '$("#'
        + str(TABLEIDS)
        + '").on("page-change.bs.table", function (e, size, number) { $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>");var chk = $("table#table_MAATTR th.bs-checkbox .filter-control input.custom").attr(\'checked\');if(chk == \'checked\'){ $("table#table_MAATTR th.bs-checkbox .filter-control input.custom").trigger("click");}});'
    )
    return sec_str, value_dict_list, TABLEIDS, filter_control_function, a_test, Pager, var_str


def GSCONTLOOKUPPOPUPFILTER(
    TABLEID, OPER, ATTRIBUTE_NAME, ATTRIBUTE_VALUE, TABLENAME, KEYDATA, ARRAYVAL, PRICEMODEL_ID, LOOKUP_ID,TESTEDOBJECT,TRACKEDTESTEDOBJECT,MAPPINGSAPPROVALOBJECT,OFFSET_SKIP_COUNT,FETCH_COUNT
):
    Trace.Write('65----')
    tab_Name = ""
    VAL_Obj = ""
    VAL_Str = ""
    API_DICT = {}
    ARRAYVALL = {}
    ARRAYVALL = eval(ARRAYVAL)
    SegmentsClickParam = Product.GetGlobal("TreeParam")
    TreeParentParam = Product.GetGlobal("TreeParentLevel0")
    # API_NAME_str=''
    for tab in Product.Tabs:
        if tab.IsSelected == True:
            tab_Name = tab.Name
    sec_str = ""
    filter_control_function = ""
    ATTRIBUTE_VALUE_STR = ""
    REC_IDS = "table_" + str(TABLEID)
    TABLEID = str(TABLEID).strip()
    x_objname_list = []
    x_objname = ""
    xx_objname = ""
    # siva--start
    if(TABLEID.find("table_")!=-1):
        TABLEID=TABLEID.split("table_")[1]
    if TABLENAME.find("_") != -1:
        x_objname_list = TABLENAME.split("_")[-2:]
        x_objname = "-".join(x_objname_list)
        x_obJ = Sql.GetFirst("SELECT OBJECT_NAME FROM SYOBJH WHERE RECORD_ID = '" + str(x_objname) + "' ")
        if x_obJ is not None:
            xx_objname = x_obJ.OBJECT_NAME
    # siva--end
    DATA_OBJ = Sql.GetFirst("SELECT COLUMNS FROM SYOBJS WHERE CONTAINER_NAME='" + str(TABLEID) + "' AND NAME='Lookup list'")
    Header_Obj = Sql.GetFirst("SELECT LABEL FROM SYOBJH WHERE OBJECT_NAME='" + str(TABLEID) + "'")
    quer_values = ""
    if DATA_OBJ is not None:
        where = ""
        if LOOKUP_ID != "" and xx_objname != "":
            WhereStr = (
                "SELECT LOOKUP_SQL_QUERY FROM  SYOBJD (NOLOCK) where OBJECT_NAME = '"
                + str(xx_objname)
                + "' and LOOKUP_API_NAME = '"
                + str(LOOKUP_ID)
                + "'"
            )
            where_obj = Sql.GetFirst(WhereStr)
            where = where_obj.LOOKUP_SQL_QUERY
            if where and where != "":
                if where.find("<") != -1:
                    m_where = re.findall("<(.+?)>", where)
                    if m_where:
                        for found in m_where:
                            where_text = "<" + str(found) + ">"
                            where_parse = Product.ParseString(where_text)
                            where = where.replace(where_text, where_parse)
        Colums_List = DATA_OBJ.COLUMNS
        #if TABLEID =='USERS':
            #user = Sql.GetList("SELECT USER_NAME FROM SYROUS (NOLOCK)")
            #for userss in user:
                #OBJD_OBJ = Sql.GetList("SELECT top 1000 ID,NAME,EMAIL FROM USERS WHERE NAME != '{}'".format(userss.USER_NAME))
                
        #else:
        OBJD_OBJ = Sql.GetList(
            "SELECT top 1000 API_NAME,FIELD_LABEL,DATA_TYPE FROM  SYOBJD WHERE OBJECT_NAME='" + str(TABLEID) + "'"
        )
        Colums_final_list1 = eval(Colums_List)
        Colums_final_list = eval(Colums_List)[1:]
        head_list = [{ins.API_NAME: ins.FIELD_LABEL} for ins in OBJD_OBJ]
        COLUMNS_NAME = ",".join(Colums_final_list1)
        Dict_formation = dict(zip(ATTRIBUTE_NAME, ATTRIBUTE_VALUE))
        ATTRIBUTE_VALUE_List = []
        RelTABEL_NAME = ""
        ## LOOKUP DATE SEARCH ISSUE FIX
        for API_NAME_LIST in OBJD_OBJ:
            API_DICT[API_NAME_LIST.API_NAME] = str(API_NAME_LIST.DATA_TYPE)

        for quer_key, quer_value in enumerate(Dict_formation):
            if Dict_formation.get(quer_value) != "":
                quer_values = Dict_formation.get(quer_value).strip()
                if str(TABLEID) == "PRPRCL":
                    ATTRIBUTE_VALUE_List.append("A." + str(quer_value) + " like '%" + str(quer_values) + "%'")
                else:
                    if str(API_DICT[quer_value]) != "DATE":
                        ATTRIBUTE_VALUE_List.append(quer_value + " like '%" + quer_values + "%'")
                    else:
                        if quer_values.find("/") != -1:
                            ATTRIBUTE_VALUE_List.append(quer_value + " = " + "'" + str(quer_values) + "'")
                        else:
                            ATTRIBUTE_VALUE_List.append(quer_value + " like '%" + quer_values + "%'")

                    Trace.Write("FINAL_ATTRIBUTE_VALUE_STR_ATTRIBUTE_VALUE_STR" + str(ATTRIBUTE_VALUE_List))
        ## LOOKUP DATE SEARCH ISSUE FIX
        ATTRIBUTE_VALUE_STR = " AND ".join(ATTRIBUTE_VALUE_List)
        
        if str(ATTRIBUTE_VALUE_STR) != "":
            RelTABEL_NAME = ""
            if RelTABEL_NAME != "QSTN_R_SYOBJR_80011":
                if str(tab_Name) == "Object" and str(TABLEID) == "SYOBJD":
                    Recvalue = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00701").GetValue()
                    VAL_Str = (
                        "SELECT top 100 "
                        + str(COLUMNS_NAME)
                        + " FROM "
                        + str(TABLEID)
                        + " WHERE "
                        + str(ATTRIBUTE_VALUE_STR)
                        + " AND PARENT_OBJECT_RECORD_ID = '"
                        + str(Recvalue)
                        + "'" 
                    )

                    VAL_Obj = Sql.GetList(VAL_Str)
                elif str(tab_Name) == "Approval Chain" and str(TABLEID) == "SYOBJD" and str(SegmentsClickParam) == "Approval Chain Steps":
                    Header_Obj = Sql.GetFirst("SELECT OBJECT_NAME FROM SYOBJH WHERE LABEL = '{}'".format(TESTEDOBJECT))
                    object_name = Header_Obj.OBJECT_NAME
                    if Header_Obj is not None:
                        VAL_Str = (
                            "SELECT top 1000 "
                            + str(COLUMNS_NAME)
                            + " FROM "
                            + str(TABLEID)
                            + " WHERE "
                            + str(ATTRIBUTE_VALUE_STR)
                            + "and OBJECT_NAME = '{}'".format(object_name)
                            )
                    VAL_Obj = Sql.GetList(VAL_Str)
                elif str(tab_Name) == "Approval Chain" and str(TABLEID) == "SYOBJD" and str(TreeParentParam) == "Approval Chain Steps":
                    Header_Obj = Sql.GetFirst("SELECT OBJECT_NAME FROM SYOBJH WHERE LABEL = '{}'".format(TRACKEDTESTEDOBJECT))
                    object_name = Header_Obj.OBJECT_NAME
                    if Header_Obj is not None:
                        VAL_Str = (
                            "SELECT top 1000 "
                            + str(COLUMNS_NAME)
                            + " FROM "
                            + str(TABLEID)
                            + " WHERE "
                            + str(ATTRIBUTE_VALUE_STR)
                            + "and OBJECT_NAME = '{}'".format(object_name)
                        )
                    VAL_Obj = Sql.GetList(VAL_Str)
                elif str(TABLEID) == "SYPFTY":
                    ContractRecordId = str(Quote.GetGlobal("contract_quote_record_id"))
                    quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
                    Trace.Write("TABLEID====>>>"+str(TABLEID))
                    
                    VAL_Str = ("SELECT top 1000 "+ str(COLUMNS_NAME)+ " FROM "
                        + str(TABLEID)
                        + " WHERE "
                        + str(ATTRIBUTE_VALUE_STR)
                        + " AND C4C_PARTNER_FUNCTION != '' AND C4C_PARTNER_FUNCTION NOT IN(SELECT C4C_PARTNERFUNCTION_ID FROM SAQDLT(NOLOCK) WHERE QTEREV_RECORD_ID ='"
                        + str(quote_revision_record_id)
                        + "' AND QUOTE_RECORD_ID = '"
                        + str(ContractRecordId)
                        + "'"
                        + ")"
                    )
                    VAL_Obj = Sql.GetList(VAL_Str)
                elif str(TABLEID) == "SAEMPL":
                    Trace.Write("TABLEID====>>>"+str(TABLEID))
                    ContractRecordId = str(Quote.GetGlobal("contract_quote_record_id"))
                    quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
                    
                    VAL_Str = ("SELECT top 1000 "+ str(COLUMNS_NAME)+ " FROM "
                        + str(TABLEID)
                        + " WHERE "
                        + str(ATTRIBUTE_VALUE_STR)
                        + " AND EMPLOYEE_RECORD_ID NOT IN(SELECT MEMBER_RECORD_ID FROM SAQDLT(NOLOCK) WHERE QTEREV_RECORD_ID ='"
                        + str(quote_revision_record_id)
                        + "' AND QUOTE_RECORD_ID = '"
                        + str(ContractRecordId)
                        + "'"
                        + ")"
                    )
                    VAL_Obj = Sql.GetList(VAL_Str) 
                elif str(tab_Name) == "Approval Chain" and str(TABLEID) == "SYOBJD" and str(SegmentsClickParam) == "Approval Chain Status Mappings":
                    Header_Obj = Sql.GetFirst("SELECT OBJECT_NAME FROM SYOBJH WHERE LABEL = '{}'".format(MAPPINGSAPPROVALOBJECT))
                    object_name = Header_Obj.OBJECT_NAME
                    if Header_Obj is not None:
                        VAL_Str = (
                            "SELECT top 1000 "
                            + str(COLUMNS_NAME)
                            + " FROM "
                            + str(TABLEID)
                            + " WHERE "
                            + str(ATTRIBUTE_VALUE_STR)
                            + "and OBJECT_NAME = '{}'".format(object_name)
                        )
                    VAL_Obj = Sql.GetList(VAL_Str)   


                elif str(tab_Name) == "Approval Chain" and str(TABLEID) == "SYOBJD" and str(TreeParentParam) == "Approval Chain Status Mappings":
                    Header_Obj = Sql.GetFirst("SELECT OBJECT_NAME FROM SYOBJH WHERE LABEL = '{}'".format(MAPPINGSAPPROVALOBJECT))
                    object_name = Header_Obj.OBJECT_NAME
                    if Header_Obj is not None:
                        VAL_Str = (
                            "SELECT top 1000 "
                            + str(COLUMNS_NAME)
                            + " FROM "
                            + str(TABLEID)
                            + " WHERE "
                            + str(ATTRIBUTE_VALUE_STR)
                            + "and OBJECT_NAME = '{}'".format(object_name)
                        )
                    VAL_Obj = Sql.GetList(VAL_Str)

                elif str(tab_Name) =="Quote" and str(SegmentsClickParam)=="Quote Information" and TESTEDOBJECT =="SOURCE ACCOUNT" and str(TABLEID) == 'SAACNT':
                    ContractRecordId = str(Quote.GetGlobal("contract_quote_record_id"))
                    VAL_Str = ("SELECT top 1000 "+ str(COLUMNS_NAME)+ " FROM "
                        + str(TABLEID)
                        + " WHERE "
                        + str(ATTRIBUTE_VALUE_STR)
                        + " AND ACCOUNT_RECORD_ID NOT IN (SELECT ACCOUNT_RECORD_ID FROM SAQTMT (NOLOCK) WHERE QTEREV_RECORD_ID ='"
                        + str(quote_revision_record_id)
                        + "' AND MASTER_TABLE_QUOTE_RECORD_ID = '"
                        + str(ContractRecordId)
                        + "'"
                        + ")"
                    )
                    VAL_Obj = Sql.GetList(VAL_Str)                    
                elif str(TABLEID) == "MAFBLC" and str(tab_Name) =="Quote":
                    ContractRecordId = str(Quote.GetGlobal("contract_quote_record_id"))
                    quote_obj = Sql.GetFirst("select ACCOUNT_ID from SAQTMT where MASTER_TABLE_QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' ".format(ContractRecordId,quote_revision_record_id))
                    account_id = quote_obj.ACCOUNT_ID   
                    VAL_Str = ("SELECT top 1000 * FROM MAFBLC WHERE "+ str(ATTRIBUTE_VALUE_STR)+ " AND ACCOUNT_ID like '%{account_id}%'".format(account_id = account_id))
                    VAL_Obj = Sql.GetList(VAL_Str)
                elif str(TABLEID) == "SAQSCO":
                    VAL_Str = ("SELECT DISTINCT *  from SAQFBL WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND {} AND RELOCATION_FAB_TYPE = 'RECEIVING FAB' ".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id,ATTRIBUTE_VALUE_STR))
                    VAL_Obj = Sql.GetList(VAL_Str)   
                elif str(TABLEID) == "cpq_permissions":
                    VAL_Str = "SELECT top 10000 permission_id,SYSTEM_ID,permission_name FROM cpq_permissions where "+ str(ATTRIBUTE_VALUE_STR)+ " and permission_type ='0'"
                    VAL_Obj = Sql.GetList(VAL_Str)                     
                # elif str(tab_Name) =="Quote" and TABLEID == 'PRTXCL':
                #     classification_obj = Sql.GetFirst("select SRVTAXCAT_ID from SAQITM where QUOTE_RECORD_ID = '{quote_record_id}' and SERVICE_ID = '{service_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' ".format(quote_record_id = Quote.GetGlobal("contract_quote_record_id"),service_id = '-'.join(SegmentsClickParam.split('-')[1:]).strip(),quote_revision_record_id))
                #     TESTEDOBJECT = classification_obj.SRVTAXCAT_ID
                #     VAL_Str = ("SELECT top 1000 TAX_CLASSIFICATION_RECORD_ID,TAX_CLASSIFICATION_DESCRIPTION,        TAX_CLASSIFICATION_ID FROM PRTXCL WHERE "
                #     + str(ATTRIBUTE_VALUE_STR)
                #     + " AND TAXCATEGORY_ID = '{TESTEDOBJECT}' and TAX_CLASSIFICATION_TYPE = 'MATERIAL' ".format(TESTEDOBJECT = TESTEDOBJECT))
                #     VAL_Obj = Sql.GetList(VAL_Str)                     
                
                elif TABLEID == 'USERS':
                    #A055S000P01-3282--start
                    #user = Sql.GetList("SELECT USER_NAME FROM SYROUS (NOLOCK)")
                    query_type=str(ATTRIBUTE_VALUE_STR).split()
                    #for userss in user:
                    VAL_Str = ("SELECT top 1000 ID,NAME,EMAIL FROM USERS WHERE {query_type} like '%{}%'".format(quer_values,query_type=query_type[0]))
                    VAL_Obj = Sql.GetList(VAL_Str)
                    #A055S000P01-3282--end
                else:
                    VAL_Str = (
                        "SELECT top 1000 "
                        + str(COLUMNS_NAME)
                        + " FROM "
                        + str(TABLEID)
                        + " WHERE "
                        + str(ATTRIBUTE_VALUE_STR)
                        + ""
                    )
                    VAL_Obj = Sql.GetList(VAL_Str) 
                if str(where).strip() != "" :
                    where = " and " + str(where)
                if str(TABLEID) != "SYOBJD" and str(TABLEID) != "PRTXCL" and str(TABLEID) != "MAFBLC" and str(TABLEID) != "SAQSCO" and str(TABLEID) != "SAEMPL" and str(TABLEID) != "SYPFTY" and (str(TreeParentParam) != "Approval Chain Steps" or str(SegmentsClickParam) == "Approval Chain Steps") and TESTEDOBJECT !="SOURCE ACCOUNT":    
                    VAL_Str = "SELECT top 100 " + COLUMNS_NAME + " FROM " + TABLEID + " where " + ATTRIBUTE_VALUE_STR + where
                    VAL_Obj = Sql.GetList(VAL_Str)
                


        else:
            Trace.Write("cm toelse====")
            RelTABEL_NAME = ""
            if RelTABEL_NAME != "QSTN_R_SYOBJR_80011":
                if str(where).strip() != "" and str(ATTRIBUTE_VALUE_STR).strip() != "":
                    where = " and " + str(where)
                    VAL_Str = (
                        "SELECT top 100 "
                        + str(COLUMNS_NAME)
                        + " FROM "
                        + str(TABLEID)
                        + " where "
                        + str(ATTRIBUTE_VALUE_STR)
                        + str(where)
                    )
                elif str(ATTRIBUTE_VALUE_STR).strip() != "":
                    VAL_Str = (
                        "SELECT top 100 "
                        + str(COLUMNS_NAME)
                        + " FROM "
                        + str(TABLEID)
                        + " where "
                        + str(ATTRIBUTE_VALUE_STR)
                        + str(where)
                    )

                    try:
                        PRICE_MOD_ID = Param.PRICE_MOD_ID or ""

                    except:
                        if A_value != "":
                            PRICE_MOD_ID = A_value
                        else:
                            PRICE_MOD_ID = ""
                    VAL_Str = (
                        "SELECT top 100 "
                        + str(COLUMNS_NAME)
                        + " FROM "
                        + str(TABLEID)
                        + " where PRICEMODEL_ID='"
                        + str(PRICE_MOD_ID)
                        + "' AND ACTIVE = 1 and PROCEDURE_ID !='UNASGN' "
                    )
                elif str(TABLEID) == "SAQSCO":
                    VAL_Str = ("SELECT DISTINCT *  from SAQFBL WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND RELOCATION_FAB_TYPE = 'RECEIVING FAB' ".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id))
                    VAL_Obj = Sql.GetList(VAL_Str)
                elif str(tab_Name) == "Approval Chain" and str(TABLEID) == "SYOBJD" and str(TreeParentParam) == "Approval Chain Status Mappings":
                    Header_Obj = Sql.GetFirst("SELECT OBJECT_NAME FROM SYOBJH WHERE LABEL = '{}'".format(MAPPINGSAPPROVALOBJECT))
                    object_name = Header_Obj.OBJECT_NAME
                    if Header_Obj is not None:
                        VAL_Str = (
                            "SELECT top 1000 "
                            + str(COLUMNS_NAME)
                            + " FROM "
                            + str(TABLEID)
                            + " WHERE  OBJECT_NAME = '{}'".format(object_name)
                        )
                    VAL_Obj = Sql.GetList(VAL_Str)
                elif str(tab_Name) == "Object" and str(TABLEID) == "SYOBJD":
                    Recvalue = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00701").GetValue()
                    if LOOKUP_ID == "OBJECTFIELD_APINAME":
                        VAL_Str = (
                            "SELECT "
                            + str(COLUMNS_NAME)
                            + " FROM "
                            + str(TABLEID)
                            + " WHERE  PARENT_OBJECT_RECORD_ID = '"
                            + str(Recvalue)
                            + "' order by (SELECT NULL) OFFSET {offset_skip_count} ROWS FETCH NEXT {per_page} ROWS ONLY"
                        )
                    else:
                        VAL_Str = (
                            "SELECT "
                            + str(API_NAME_str)
                            + " FROM "
                            + str(TABLEID)
                            + " WHERE DATA_TYPE IN ('PICKLIST','CHECKBOX') and PARENT_OBJECT_RECORD_ID = '"
                            + str(Recvalue)
                            + "' order by (SELECT NULL) OFFSET {offset_skip_count} ROWS FETCH NEXT {per_page} ROWS ONLY"
                        )
                    VAL_Obj = Sql.GetList(VAL_Str.format(offset_skip_count=OFFSET_SKIP_COUNT,per_page=FETCH_COUNT))
                elif str(TABLEID) == "cpq_permissions":
                    VAL_Obj = Sql.GetList("SELECT " + str(COLUMNS_NAME) + " FROM " + str(TABLEID) +" where permission_type ='0' order by (SELECT NULL) OFFSET {offset_skip_count} ROWS FETCH NEXT {per_page} ROWS ONLY".format(offset_skip_count=OFFSET_SKIP_COUNT,per_page=FETCH_COUNT))
                else:
                    VAL_Obj = Sql.GetList("SELECT " + str(COLUMNS_NAME) + " FROM " + str(TABLEID) + " order by (SELECT NULL) OFFSET {offset_skip_count} ROWS FETCH NEXT {per_page} ROWS ONLY".format(offset_skip_count=OFFSET_SKIP_COUNT,per_page=FETCH_COUNT))
            else:
                VAL_Str = "SELECT top 100 " + str(COLUMNS_NAME) + " FROM " + str(TABLEID) + " "
                VAL_Obj = Sql.GetList(VAL_Str)
        table_list = []

        for val_api in VAL_Obj:
            data_dict = {}
            first_col = str(eval("val_api." + str(Colums_final_list1[0])))
            for Colums_final in Colums_final_list:
                data_dict["ids"] = first_col + "|" + str(Colums_final_list1[0])
                if str(Colums_final) != "EFFECTIVEDATE_BEG":
                    data_dict[str(Colums_final)] = eval(
                        "val_api." + str(Colums_final).decode("unicode_escape").encode("utf-8")
                    )
                else:
                    Colums_final = Colums_final.decode("unicode_escape").encode("utf-8")
                    data_dict[str(Colums_final)] = str(eval("val_api." + str(Colums_final)))
            table_list.append(data_dict)
    return table_list


TABLEID = Param.TABLEID
OPER = Param.OPER
GSCONTLOOKUP = Param.GSCONTLOOKUP
TABLENAME = Param.TABLENAME
KEYDATA = Param.KEYDATA
ARRAYVAL = Param.ARRAYVAL
PRICEMODEL_ID = ""
try:
    LOOKUP_ID = Param.LOOKUP_ID
except:
    LOOKUP_ID = ""
try:
    TESTEDOBJECT = Param.TESTEDOBJECT
except:
    TESTEDOBJECT = ""
try:
    TRACKEDTESTEDOBJECT = Param.TRACKEDTESTEDOBJECT
except:
    TRACKEDTESTEDOBJECT = ""
try:
    MAPPINGSAPPROVALOBJECT = Param.MAPPINGSAPPROVALOBJECT
except:
    MAPPINGSAPPROVALOBJECT = ""

try:
    try:
        PRICEMODEL_ID = Param.PRICE_MOD_ID
    except Exception:
        PRICEMODEL_ID = ""
    if PRICEMODEL_ID == "" or PRICEMODEL_ID is None:
        PRICEMODEL_ID = Param.PRICE_MODEL_ID
except:
    PRICEMODEL_ID = ""

try:
    MARKET_TYPE = Param.MARKET_TYPE
    MODEL_TYPE = Param.MODEL_TYPE
    PRODUCT_TYPE = Param.PRODUCT_TYPE
except:
    MARKET_TYPE = ""
    MODEL_TYPE = ""
    PRODUCT_TYPE = ""
try:
    Offset_Skip_Count=Param.Offset_Skip_Count
    Fetch_Count=Param.Fetch_Count
except:
    Offset_Skip_Count=0
    Fetch_Count=10
# jira 8434 end
#### SEGMENT REVISION MIGRATION CODE ENDS...
try:
    LOOKUP_ID = Param.LOOKUP_ID
except:
    LOOKUP_ID = ""
# ------A043S001P01-10888 STARRT ----------
if str(TABLENAME) == "ADDNEW__SYOBJR_94452_SYOBJ_00425":
    TABLEID = "USERS"
# ------A043S001P01-10888 END-----------
if GSCONTLOOKUP == "":
    ApiResponse = ApiResponseFactory.JsonResponse(
        GSCONTLOOKUPPOPUP(
            TABLEID, OPER, TABLENAME, KEYDATA, ARRAYVAL, PRICEMODEL_ID, LOOKUP_ID, MARKET_TYPE, MODEL_TYPE, PRODUCT_TYPE,TESTEDOBJECT,TRACKEDTESTEDOBJECT,MAPPINGSAPPROVALOBJECT
        )
    )
elif GSCONTLOOKUP == "GSCONTLOOKUP":
    ATTRIBUTE_VALUE = Param.ATTRIBUTE_VALUE
    ATTRIBUTE_NAME = Param.ATTRIBUTE_NAME
    OFFSET_SKIP_COUNT=Offset_Skip_Count
    FETCH_COUNT=Fetch_Count
    ApiResponse = ApiResponseFactory.JsonResponse(
        GSCONTLOOKUPPOPUPFILTER(
            TABLEID, OPER, ATTRIBUTE_NAME, ATTRIBUTE_VALUE, TABLENAME, KEYDATA, ARRAYVAL, PRICEMODEL_ID, LOOKUP_ID,TESTEDOBJECT,TRACKEDTESTEDOBJECT,MAPPINGSAPPROVALOBJECT,OFFSET_SKIP_COUNT,FETCH_COUNT
        )
    )


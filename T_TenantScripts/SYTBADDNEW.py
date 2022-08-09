# =========================================================================================================================================
#   __script_name : SYTBADDNEW.PY
#   __script_description :  THIS SCRIPT IS USED TO NAVIGATE THE USER FROM THE OBJECT LIST GRID PAGE TO THE ADD-NEW PAGE. THE SCRIPT IS EECUTED WHEN THE USER CLICKS ON THE ADD-NEW BUTTON IN ALL TABS.
#   __primary_author__ : JOE EBENEZER
#   __create_date :
#   Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct
TestProduct = Webcom.Configurator.Scripting.Test.TestProduct()
Product.Attributes.GetByName("MA_MTR_TAB_ACTION").AssignValue("ADDNEW")
Action = "ADDNEW"
Product_name = Product.Name
from SYDATABASE import SQL

Sql = SQL()
import datetime
from datetime import date
from datetime import timedelta

try:
    TestProduct = Webcom.Configurator.Scripting.Test.TestProduct()
    CurrentTabName = TestProduct.CurrentTab


    sql_obj = Sql.GetFirst(
        "select SAPCPQ_ALTTAB_NAME,PRIMARY_OBJECT_NAME from SYTABS (NOLOCK) where TAB_LABEL = '"
        + str(CurrentTabName)
        + "' and APP_LABEL='"
        + str(Product.Name)
        + "'"
    )

    ## approval chain alert banner starts
    if (str(CurrentTabName) == 'Approval Chains' and str(Product.Name) == 'APPROVAL CENTER') or str(Product.Name) == 'SYSTEM ADMIN' :
        #Trace.Write("sql_obj.PRIMARY_OBJECT_NAME"+ str(sql_obj.PRIMARY_OBJECT_NAME))
        Product.Attributes.GetByName("SEC_N_TAB_PAGE_ALERT").HintFormula = ''
        Product.Attributes.GetByName("SEC_N_TAB_PAGE_ALERT").Allowed = False
    ## approval chain alert banner ends

    Product.Attributes.GetByName("MA_MTR_TAB_ACTION").AssignValue(Action)
    TestProduct.ChangeTab(sql_obj.SAPCPQ_ALTTAB_NAME)

    if Product.Tabs.GetByName(str(TestProduct.CurrentTab)) is not None:
        Datalist = [
            str(attr.Name).replace("SEC_", "").replace("_", "-")
            for attr in Product.Tabs.GetByName(str(TestProduct.CurrentTab)).Attributes
            if str(attr.Name).startswith("SEC_")
        ]
        looKup_list = [
            str(attr.Name)
            for attr in Product.Tabs.GetByName(str(TestProduct.CurrentTab)).Attributes
            if str(attr.Name).startswith("QSTN_LKP_")
        ]
        #Trace.Write(str(Datalist) + "---------datalist" + str(tuple(Datalist)))


        if str(sql_obj.PRIMARY_OBJECT_NAME) == "cpq_permissions":
            Question_Permission_Query = Sql.GetList(
                "Select a.API_NAME, a.RECORD_ID, a.SECTION_NAME,a.SAPCPQ_ATTRIBUTE_NAME, a.FIELD_LABEL, b.permission,b.data_type,b.EDITABLE_ONINSERT from SYSEFL a (nolock) inner join SYOBJD b (nolock) on a.API_NAME=b.object_name and a.API_FIELD_NAME = b.API_NAME where a.API_NAME='"
                + str(sql_obj.PRIMARY_OBJECT_NAME)
                + "'"
            )
        else:
            #Trace.Write("-------else"+str(len(Datalist)))
            if len(Datalist) == 1:

                Question_Permission_Query = Sql.GetList(
                    "Select a.API_NAME, a.RECORD_ID,a.SAPCPQ_ATTRIBUTE_NAME, a.SECTION_NAME, a.FIELD_LABEL, b.permission,b.data_type,b.EDITABLE_ONINSERT from SYSEFL a (nolock) inner join SYOBJD b (nolock) on a.API_NAME=b.OBJECT_NAME and a.API_FIELD_NAME=b.API_NAME inner join sysect (nolock) c on c.RECORD_ID = a.SECTION_RECORD_ID where a.API_NAME='"
                    + str(sql_obj.PRIMARY_OBJECT_NAME)
                    + "'  and c.SAPCPQ_ATTRIBUTE_NAME in ('"
                    + str(Datalist[0])
                    + "') "
                )
            else:
                Question_Permission_Query = Sql.GetList(
                    "Select a.API_NAME, a.RECORD_ID, a.SECTION_NAME, a.FIELD_LABEL,a.SAPCPQ_ATTRIBUTE_NAME, b.permission,b.data_type,b.EDITABLE_ONINSERT from SYSEFL a (nolock) inner join SYOBJD b (nolock) on a.API_NAME=b.OBJECT_NAME and a.API_FIELD_NAME = b.API_NAME inner join sysect (nolock) c on c.RECORD_ID = a.SECTION_RECORD_ID where a.API_NAME='"
                    + str(sql_obj.PRIMARY_OBJECT_NAME)
                    + "'  and c.SAPCPQ_ATTRIBUTE_NAME in "
                    + str(tuple(Datalist))
                    + ""
                )

                
        for Question_Permission in Question_Permission_Query:
            Trace.Write("SECTION_NAME-->" + str(Question_Permission.SECTION_NAME))
            Trace.Write("FIELD_LABEL-->" + str(Question_Permission.FIELD_LABEL))
            if (
                str(Question_Permission.data_type) == "LONG TEXT AREA"
                or str(Question_Permission.data_type) == "RICH TEXT AREA"
            ):
                #Trace.Write("----------------" + str(Question_Permission.data_type))
                AttrName = str("QSTN_" + str(Question_Permission.SAPCPQ_ATTRIBUTE_NAME).replace("-", "_") + "_LONG")
                if str(Question_Permission.EDITABLE_ONINSERT).upper() == "TRUE":
                    Product.Attributes.GetByName(AttrName).Access = AttributeAccess.Editable
            else:
                AttrName = str("QSTN_" + str(Question_Permission.SAPCPQ_ATTRIBUTE_NAME).replace("-", "_"))
                #Trace.Write(str(Question_Permission.permission)+"-----AttrName_AttrName--110--" + str(AttrName))
                if (
                    str(Question_Permission.EDITABLE_ONINSERT).upper() == "TRUE"
                    or str(Question_Permission.permission).upper() == "EDITABLE"
                ):
                    Product.Attributes.GetByName(AttrName).Access = AttributeAccess.Editable
            ScriptExecutor.ExecuteGlobal("SYLDRLADBN")

            if str(AttrName) == "QSTN_SYSEFL_SY_00125":
                if Product.Attributes.GetByName(str(AttrName)) is not None:
                    Product.Attributes.GetByName(str(AttrName)).Allowed = False
            elif str(Question_Permission.SECTION_NAME) == "AUDIT INFORMATION" and Question_Permission.FIELD_LABEL in [
                "Added Date",
                "Added By",
                "Last Modified By",
                "Last Modified Date",
            ]:
                Trace.Write("Audit Information")
                if Product.Attributes.GetByName(str(AttrName)) is not None:
                    Product.Attributes.GetByName(str(AttrName)).Allowed = False
            elif (
                str(Question_Permission.API_NAME) == "SYTABS"
                and str(Question_Permission.SECTION_NAME) == "AUDIT INFORMATION"
                and Question_Permission.FIELD_LABEL in ["Owned By", "Owned Date"]
            ):
                if Product.Attributes.GetByName(str(AttrName)) is not None:
                    Product.Attributes.GetByName(str(AttrName)).Allowed = False
            elif (
                str(Question_Permission.API_NAME) == "SYPAGE"
                and str(Question_Permission.SECTION_NAME) == "AUDIT INFORMATION"
                and Question_Permission.FIELD_LABEL in ["Owned By", "Owned Date"]
            ):
                if Product.Attributes.GetByName(str(AttrName)) is not None:
                    Product.Attributes.GetByName(str(AttrName)).Allowed = False             
            
            elif "QSTN_LKP_SYSEFL_" in looKup_list:
                for data in looKup_list:
                    Product.Attributes.GetByName(str(data)).HintFormula = ""    
            else:
                if Product.Attributes.GetByName(str(AttrName)) is not None:
                    if str(Question_Permission.data_type) == "PICKLIST":
                        Product.Attributes.GetByName(str(AttrName)).SelectDisplayValue("None")
                    # elif str(Question_Permission.data_type) == "PICKLIST" and str(Question_Permission.API_NAME) == "ACAPCH"):
                    #     Trace.Write("ObjectName---> " + str(API_NAME))
                    #     sec_str = (
                    #             '<td><select id="'
                    #             + str(current_obj_api_name)
                    #             + '" value="'
                    #             + str(current_obj_value)
                    #             + '" type="text" class="form-control pop_up_brd_rad related_popup_css hgt32fnt13 light_yellow" onchange = "onFieldChanges(this)" '
                    #             + disable
                    #             + " ><option value='Select'>..Select</option>"
                    #         )     
                    else:
                        Product.ResetAttr(str(AttrName))
                        Product.Attributes.GetByName(str(AttrName)).AssignValue(" ")
                    if (
                        str(Question_Permission.permission) == "READ ONLY"
                        and str(Question_Permission.EDITABLE_ONINSERT).upper() != "TRUE"
                    ):
                        Product.Attributes.GetByName(str(AttrName)).Access = AttributeAccess.ReadOnly

    Product.SetGlobal("ATTR_VAL", "")
    ScriptExecutor.ExecuteGlobal("SYLDRLADBN")
    ScriptExecutor.ExecuteGlobal("SYGETVRCTX")

    current_tab = str(TestProduct.CurrentTab)
 
except Exception, e:
    #Trace.Write("ERROR" + str(e))
    TestProduct = Webcom.Configurator.Scripting.Test.TestProduct()
    CurrentTabName = TestProduct.CurrentTab



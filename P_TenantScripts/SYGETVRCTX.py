# =========================================================================================================================================
#   __script_name : SYGETVRCTX.PY
#   __script_description : THIS SCRIPT IS USED TO GET THE CTX LOGIC FROM VARIABLES AND ITS TRIGGERED DURING THE ONPRODUCTLOADED, AND ONPRODUCTRULEEXECUTIONEND EVENTS IN THE MATERIALS APP.
#   __primary_author__ : LEO JOSEPH
#   __create_date :
#   Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
from SYDATABASE import SQL
import Webcom.Configurator.Scripting.Test.TestProduct
Sql = SQL()

get_user_id = User.Id
TestProduct = Webcom.Configurator.Scripting.Test.TestProduct()
TabName = TestProduct.CurrentTab
if str(TabName) != "Price Models" and str(TabName) != "Profiles" and str(TabName) != "Roles":
    value = Product.Attributes.GetByName("MA_MTR_TAB_ACTION").GetValue()
    sql_obj = Sql.GetFirst(
        "select RECORD_ID,TAB_LABEL,SAPCPQ_ALTTAB_NAME from SYTABS (nolock) where SAPCPQ_ALTTAB_NAME = '" + str(TabName) + "'"
    )
    if sql_obj:
        #section level restrictions start
        #Trace.Write('21---')
        SYSECT_OBJNAME = Sql.GetList(
            "select SE.RECORD_ID,SE.SECTION_NAME,SE.PRIMARY_OBJECT_NAME FROM SYSECT (nolock) SE inner join SYPAGE(nolock)PG on SE.PAGE_RECORD_ID = PG.RECORD_ID and SE.PAGE_NAME = PG.PAGE_NAME  JOIN  SYPRSN (NOLOCk) ON  SYPRSN.SECTION_RECORD_ID = SE.RECORD_ID  JOIN USERS_PERMISSIONS UP (NOLOCK) ON UP.Permission_id = SYPRSN.PROFILE_RECORD_ID where PG.TAB_NAME = '"
            + str(sql_obj.TAB_LABEL).strip()
            + "' and SYPRSN.VISIBLE = 1 AND Up.user_id ='"
            + str(get_user_id)
            + "' and PG.TAB_RECORD_ID='"
            + str(sql_obj.RECORD_ID)
            + "' "
        )
        #section level restrictions end
        '''SYSECT_OBJNAME = Sql.GetList(
            "select SE.RECORD_ID,SE.SECTION_NAME,SE.PRIMARY_OBJECT_NAME FROM SYSECT (nolock) SE inner join SYPAGE(nolock)PG on SE.PAGE_RECORD_ID = PG.RECORD_ID and SE.PAGE_NAME = PG.PAGE_NAME where LTRIM(RTRIM(PG.TAB_NAME)) = '"
            + str(sql_obj.TAB_LABEL).strip()
            + "' and PG.TAB_RECORD_ID='"
            + str(sql_obj.RECORD_ID)
            + "' "
        )'''
        if SYSECT_OBJNAME is not None:
            for SYSECT_Details in SYSECT_OBJNAME:
                if SYSECT_Details.SECTION_NAME != "" and SYSECT_Details.PRIMARY_OBJECT_NAME != "":
                    obj_name = SYSECT_Details.PRIMARY_OBJECT_NAME.strip()
                    SYSEFL_OBJNAME = Sql.GetList(
                        "SELECT q.RECORD_ID,q.SAPCPQ_ATTRIBUTE_NAME,q.FIELD_LABEL, q.API_FIELD_NAME,q.API_NAME,q.SECTION_NAME,q.FLDVIS_VARIABLE_RECORD_ID,q.FLDVIS_VARIABLE_NAME,q.FLDEDT_VARIABLE_RECORD_ID,q.FLDDEF_VARIABLE_RECORD_ID,q.FLDDEF_VARIABLE_NAME,q.FLDEDT_VARIABLE_NAME,o.DATA_TYPE FROM SYSEFL (nolock) q INNER JOIN  SYOBJD (nolock) o ON q.API_FIELD_NAME = o.API_NAME  and o.OBJECT_NAME = q.API_NAME where RTRIM(LTRIM(q.API_NAME)) ='"
                        + str(SYSECT_Details.PRIMARY_OBJECT_NAME).strip()
                        + "' and RTRIM(LTRIM(q.SECTION_NAME))='"
                        + str(SYSECT_Details.SECTION_NAME).strip()
                        + "' and q.SECTION_RECORD_ID='"
                        + str(SYSECT_Details.RECORD_ID)
                        + "' AND ((q.FLDVIS_VARIABLE_RECORD_ID != '' and q.FLDVIS_VARIABLE_RECORD_ID is not null) or (q.FLDEDT_VARIABLE_RECORD_ID != '' and q.FLDEDT_VARIABLE_RECORD_ID is not null) or (q.FLDDEF_VARIABLE_RECORD_ID != '' and q.FLDDEF_VARIABLE_RECORD_ID is not null))"
                    )
                    if SYSEFL_OBJNAME is not None:
                        for SYSEFL_Details in SYSEFL_OBJNAME:
                            SECTIONQSTNRECORDID = (
                                str(SYSEFL_Details.SAPCPQ_ATTRIBUTE_NAME).replace("-", "_").replace(" ", "")
                            )
                            SECQSTNATTRIBUTENAME = (SECTIONQSTNRECORDID).upper()
                            MM_MOD_ATTR_NAME = "QSTN_" + str(SECQSTNATTRIBUTENAME)
                            if (
                                SYSEFL_Details.FLDVIS_VARIABLE_RECORD_ID != ""
                                and SYSEFL_Details.FLDVIS_VARIABLE_NAME != ""
                                and Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)) is not None
                            ):
                                FLDVIS_VARIABLE_RECORD_ID = SYSEFL_Details.FLDVIS_VARIABLE_RECORD_ID
                                CTX_Logic = Sql.GetFirst(
                                    "select CPQ_CALCULATION_LOGIC from SYVABL (nolock) where RECORD_ID = '"
                                    + str(FLDVIS_VARIABLE_RECORD_ID)
                                    + "' "
                                )
                                if CTX_Logic is not None:
                                    result = ScriptExecutor.ExecuteGlobal(
                                        "SYPARVRLLG",
                                        {"CTXLogic": str(CTX_Logic.CPQ_CALCULATION_LOGIC), "Obj_Name": obj_name},
                                    )
                                    if str(result).upper() == "TRUE":
                                        Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).Allowed = True
                                    else:
                                        Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).Allowed = False
                            elif (
                                SYSEFL_Details.FLDEDT_VARIABLE_RECORD_ID != ""
                                and SYSEFL_Details.FLDEDT_VARIABLE_NAME != ""
                                and Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)) is not None
                                and value != "VIEW"
                            ):
                                FLDEDT_VARIABLE_RECORD_ID = SYSEFL_Details.FLDEDT_VARIABLE_RECORD_ID
                                CTX_Logic = Sql.GetFirst(
                                    "select CPQ_CALCULATION_LOGIC from SYVABL (nolock) where RECORD_ID = '"
                                    + str(FLDEDT_VARIABLE_RECORD_ID)
                                    + "' "
                                )
                                if CTX_Logic is not None:
                                    result = ScriptExecutor.ExecuteGlobal(
                                        "SYPARVRLLG",
                                        {"CTXLogic": str(CTX_Logic.CPQ_CALCULATION_LOGIC), "Obj_Name": obj_name},
                                    )
                                    if str(result).upper() == "TRUE":
                                        Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).Access = 0
                                    else:
                                        Product.Attributes.GetByName(
                                            str(MM_MOD_ATTR_NAME)
                                        ).Access = AttributeAccess.ReadOnly
                            elif (
                                SYSEFL_Details.FLDDEF_VARIABLE_RECORD_ID != ""
                                and SYSEFL_Details.FLDDEF_VARIABLE_NAME != ""
                                and Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)) is not None
                                and value != "VIEW"
                            ):
                                FLDDEF_VARIABLE_RECORD_ID = SYSEFL_Details.FLDDEF_VARIABLE_RECORD_ID
                                CTX_Logic = Sql.GetFirst(
                                    "select CPQ_CALCULATION_LOGIC from SYVABL (nolock) where RECORD_ID = '"
                                    + str(FLDDEF_VARIABLE_RECORD_ID)
                                    + "' "
                                )
                                if CTX_Logic is not None:
                                    result = ScriptExecutor.ExecuteGlobal(
                                        "SYPARVRLLG",
                                        {"CTXLogic": str(CTX_Logic.CPQ_CALCULATION_LOGIC), "Obj_Name": obj_name},
                                    )
                                    if str(result) != "":
                                        Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).AssignValue(str(result))
                                    else:
                                        Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).AssignValue("")
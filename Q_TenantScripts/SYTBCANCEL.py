# =========================================================================================================================================
#   __script_name : SYTBCANCEL.PY
#   __script_description :  THIS SCRIPT IS USED TO CANCEL USER CHANGES WHEN ADDING OR EDITING A RECORD.
#   __primary_author__ : JOE EBENZER
#   __create_date :
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct
import SYCNGEGUID as CPQID
from SYDATABASE import SQL

Sql = SQL()

TestProduct = Webcom.Configurator.Scripting.Test.TestProduct()
Product_name = Product.Name
current_tab = str(TestProduct.CurrentTab)

if Product.Tabs.GetByName(str(current_tab)) is not None and Product_name != "":
    sql_obj = Sql.GetFirst(
        "select RECORD_ID,TAB_LABEL from SYTABS where RTRIM(LTRIM(SAPCPQ_ALTTAB_NAME)) = '"
        + str(current_tab)
        + "' and RTRIM(LTRIM(APP_LABEL))='"
        + str(Product_name).strip()
        + "' "
    )
    if sql_obj is not None:
        TABNAME = str(sql_obj.TAB_LABEL).strip()

        SYSECT_OBJNAME = Sql.GetFirst(
            "select SYSECT.PRIMARY_OBJECT_NAME,SYSECT.PRIMARY_OBJECT_RECORD_ID,SYSECT.PAGE_RECORD_ID,SYPAGE.TAB_RECORD_ID FROM SYSECT (NOLOCK) INNER JOIN SYPAGE (NOLOCK) on SYSECT.PAGE_RECORD_ID = SYPAGE.RECORD_ID where  SYPAGE.TAB_RECORD_ID ='"
            + str(sql_obj.RECORD_ID).strip()
            + "' order by DISPLAY_ORDER"
        )

        if SYSECT_OBJNAME is not None:
            TABLE_NAME = str(SYSECT_OBJNAME.PRIMARY_OBJECT_NAME).strip()
            SYSEFL_OBJNAME = Sql.GetList(
                "SELECT q.SAPCPQ_ATTRIBUTE_NAME,q.FIELD_LABEL, q.API_NAME,q.SECTION_NAME,o.DATA_TYPE FROM SYSEFL q INNER JOIN  SYOBJD o ON q.API_FIELD_NAME = o.API_NAME  and o.OBJECT_NAME = q.API_NAME where q.API_NAME ='"
                + str(SYSECT_OBJNAME.PRIMARY_OBJECT_NAME).strip()
                + "' "
            )

            if SYSEFL_OBJNAME is not None:
                for SYSEFL_Details in SYSEFL_OBJNAME:
                    DATA_TYPE = str(SYSEFL_Details.DATA_TYPE).strip()
                    if DATA_TYPE == "AUTO NUMBER":
                        SECTIONQSTNRECORDID = str(SYSEFL_Details.SAPCPQ_ATTRIBUTE_NAME).replace("-", "_").replace(" ", "")

                        SECQSTNATTRIBUTENAME = (SECTIONQSTNRECORDID).upper()

                        MM_MOD_ATTR_NAME = "QSTN_" + str(SECQSTNATTRIBUTENAME)

                        curr = Product.Attributes.GetByName("MA_MTR_TAB_ACTION").GetValue()
                        if curr == "CLONE":
                            clone_id = Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).GetValue()
                            if clone_id != "":
                                ScriptExecutor.ExecuteGlobal(
                                    "SYALLTABOP",
                                    {"Primary_Data": clone_id, "TabNAME": TABNAME, "ACTION": "VIEW", "RELATED": "",},
                                )
                        elif Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)) is not None:
                            RECORD_ID = Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).GetValue()
                            if RECORD_ID != "":
                                ScriptExecutor.ExecuteGlobal(
                                    "SYALLTABOP",
                                    {"Primary_Data": RECORD_ID, "TabNAME": TABNAME, "ACTION": "VIEW", "RELATED": "",},
                                )
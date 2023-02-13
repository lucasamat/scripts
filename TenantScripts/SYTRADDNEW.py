# =========================================================================================================================================
#   __script_name : SYTRADDNEW.PY
#   __script_description : THIS SCRIPT IS USED TO NAVIGATE THE PAGE FROM RELATED LIST GRID TO ADD NEW. IT WILL EXECUTE WHEN THE USER CLICKS THE ADD NEW BUTTON IN ALL RELATED LIST TABS.
#   __primary_author__ : JOE EBENEZER
#   __create_date :
# ==========================================================================================================================================
import SYCNGEGUID as CPQID
import Webcom.Configurator.Scripting.Test.TestProduct
from SYDATABASE import SQL
Sql = SQL()

CurrentTabName = Param.TABNAME
RECORD_ID = Param.RECID
RelatedTab = Param.CURRENTTAB
Trace.Write("CurrentTabName----->" + str(CurrentTabName))
Trace.Write("RECORD_ID----->" + str(RECORD_ID))
Trace.Write("RelatedTab----->" + str(RelatedTab))

Product.Attributes.GetByName("MA_MTR_TAB_ACTION").AssignValue("ADDNEW")
Action = "ADD NEW"
Category_ID = ""
Category_Name = ""
ACCOUNT_ID = ""
ACCOUNT_NAME = ""

try:
    TestProduct = Webcom.Configurator.Scripting.Test.TestProduct()
    sql_obj = Sql.GetFirst(
        "select RECORD_ID,SAPCPQ_ALTTAB_NAME from SYTABS where upper(TAB_NAME) = '" + str(CurrentTabName).upper() + "'"
    )
    Product.Attributes.GetByName("MA_MTR_TAB_ACTION").AssignValue(Action)
    if sql_obj is not None:
        TestProduct.ChangeTab(str(sql_obj.SAPCPQ_ALTTAB_NAME).strip())
        Tab_Recid = sql_obj.RECORD_ID
        Product.Attributes.GetByName("MA_MTR_TAB_ACTION").AssignValue("ADDNEW")
        if Product.Tabs.GetByName(str(TestProduct.CurrentTab)) is not None:
          
            Tab_Name = Product.Tabs.GetByName(str(TestProduct.CurrentTab)).Attributes
            for attr in Tab_Name:
                if Product.Attributes.GetByName(str(attr.Name)) is not None:
                    Product.ResetAttr(str(attr.Name))
                    Product.Attributes.GetByName(str(attr.Name)).AssignValue(" ")
                    Product.Attributes.GetByName(str(attr.Name)).Access = 0

            if Tab_Recid != "":
                OBJECT_NAME = Sql.GetFirst(
                    "select PRIMARY_OBJECT_NAME from SYSECT (NOLOCK) INNER JOIN SYPAGE (NOLOCK) ON SYPAGE.RECORD_ID = SYSECT.PAGE_RECORD_ID where SYPAGE.TAB_RECORD_ID = '"
                    + str(Tab_Recid)
                    + "'"
                )
                if OBJECT_NAME is not None:
                    Table_Name = str(OBJECT_NAME.PRIMARY_OBJECT_NAME).strip()

            if RelatedTab != "":
                REL_TAB = Sql.GetFirst(
                    "select RECORD_ID from SYTABS where upper(SAPCPQ_ALTTAB_NAME) = '" + str(RelatedTab).upper() + "'"
                )
                if REL_TAB is not None:
                    Rel_Tab_Id = str(REL_TAB.RECORD_ID)
                    REL_OBJ = Sql.GetFirst(
                        "select PRIMARY_OBJECT_NAME from SYSECT (NOLOCK) INNER JOIN SYPAGE (NOLOCK) ON SYPAGE.RECORD_ID = SYSECT.PAGE_RECORD_ID where SYPAGE.TAB_RECORD_ID = '"
                        + str(Rel_Tab_Id)
                        + "'"
                    )
                    if REL_OBJ is not None:
                        Related_table = str(REL_OBJ.PRIMARY_OBJECT_NAME)

            if Table_Name != "" and Related_table != "":
                OBJD = Sql.GetFirst(
                    "select API_NAME,LOOKUP_API_NAME from  SYOBJD where OBJECT_NAME = '"
                    + str(Table_Name).strip()
                    + "' and LOOKUP_OBJECT='"
                    + str(Related_table).strip()
                    + "' "
                )
                if OBJD.LOOKUP_API_NAME is not None and OBJD.API_NAME and RECORD_ID != "":
                    Obj_Val = Sql.GetFirst(
                        "select "
                        + str(OBJD.LOOKUP_API_NAME)
                        + " from "
                        + str(Related_table)
                        + " where "
                        + str(OBJD.API_NAME).strip()
                        + " = '"
                        + str(RECORD_ID)
                        + "'"
                    )
                    if Obj_Val is not None:
                        Attr_val = eval(str("Obj_Val." + OBJD.LOOKUP_API_NAME))

                    SYSEFL = Sql.GetFirst(
                        "select RECORD_ID from SYSEFL where LTRIM(RTRIM(API_NAME)) = '"
                        + str(Table_Name)
                        + "' and LTRIM(RTRIM(API_NAME))='"
                        + str(OBJD.LOOKUP_API_NAME).strip()
                        + "' "
                    )
                    if SYSEFL is not None:
                        QSTNRECORDID = str(SYSEFL.RECORD_ID).replace("-", "_").replace(" ", "")
                        QSTNATTRIBUTENAME = (QSTNRECORDID).upper()
                        MM_MOD_ATTR_NAME = "QSTN_" + str(QSTNATTRIBUTENAME)
                        Trace.Write("MM_MOD_ATTR_NAME----->" + str(MM_MOD_ATTR_NAME))
                        LKP_ATTR_NAME = "QSTN_LKP_" + str(QSTNATTRIBUTENAME)

                        if Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)) is not None and Attr_val != "":
                            Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).AssignValue(str(Attr_val))
                            Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).Access = AttributeAccess.ReadOnly

                        if Product.Attributes.GetByName(str(LKP_ATTR_NAME)) is not None:
                            Product.Attributes.GetByName(str(LKP_ATTR_NAME)).HintFormula = str(RECORD_ID)
                            Product.Attributes.GetByName(str(LKP_ATTR_NAME)).Access = AttributeAccess.ReadOnly

 
except Exception, e:
    Trace.Write("ERROR GETTING" + str(e))


def get_value_from_obj(record_obj, column):
    #Trace.Write("vvvvvvvvvvvvvv")
    return getattr(record_obj, column, "")
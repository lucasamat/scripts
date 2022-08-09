# =========================================================================================================================================
#   __script_name : SYTBKTOLST.PY
#   __script_description :  THIS SCRIPT IS USED TO REDIRECT THE USER TO THE OBJECT LIST GRID PAGE FROM AN OBJECT RECORD PAGE.
#   __primary_author__ : JOE EBENEZER
#   __create_date :
#   Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import SYCNGEGUID as CPQID
from SYDATABASE import SQL
import Webcom.Configurator.Scripting.Test.TestProduct

Sql = SQL()

Action = "BACK TO LIST"

TestProduct = Webcom.Configurator.Scripting.Test.TestProduct()
CurrentTabName = TestProduct.CurrentTab
sql_obj = Sql.GetFirst("select TAB_LABEL from SYTABS where LTRIM(RTRIM(SAPCPQ_ALTTAB_NAME)) = '" + str(CurrentTabName) + "'")
# Product.Attributes.GetByName("MA_MTR_ACTIVE_TAB").AssignValue(CurrentTabName+'S')
Product.Attributes.GetByName("MA_MTR_TAB_ACTION").AssignValue(Action)

Product.SetGlobal("SegmentsClickParam", "Setup Information")
TestProduct.ChangeTab(sql_obj.TAB_LABEL)
# Product.SetGlobal("SegmentsClickParam","Setup Information")
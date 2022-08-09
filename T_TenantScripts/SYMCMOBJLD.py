# =========================================================================================================================================
#   __script_name : SYMCMOBJLD.PY
#   __script_description : THIS SCRIPT IS USED TO LOAD THE OBJECT LIST IN THE SYSTEM ADMIN APP
#   __primary_author__ : LEO JOSEPH
#   __create_date : 8/31/2020
#   Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct
from SYDATABASE import SQL

Sql = SQL()

data_typ = ""
if str(Product.Tabs.GetByName("OBJECTS").IsSelected) == "True":
    Log.Info("Object tab loading----")
    Product.Attributes.GetByName("MM_OBJ_DATA_TYPE").Access = AttributeAccess.ReadOnly
    Product.Attributes.GetByName("MM_OBJ_DIS_FORMAT").Access = AttributeAccess.ReadOnly
    Product.Attributes.GetByName("MM_OBJ_DATA_TYPE").SelectDisplayValue("AUTO NUMBER")
    
    Sql_Obj = Sql.GetList("SELECT top 1000 * FROM SYOBJH ORDER BY RECORD_ID")
    Cont = Product.GetContainerByName("MM_OBJ_CTR_OBJ_INFO")
    Cont.Rows.Clear()
    for inv in Sql_Obj:
        row = Cont.AddNewRow(False)
        row.SetColumnValue("RECORD_ID", str(inv.RECORD_ID))
        row.SetColumnValue("OBJECT_NAME", str(inv.OBJECT_NAME))
        row.SetColumnValue("OBJ_DESC", str(inv.OBJ_DESC))
        row.SetColumnValue("LABEL", str(inv.LABEL))
        row.SetColumnValue("OBJECT_STATUS", str(inv.OBJECT_STATUS))

    data_typ = Product.Attributes.GetByName("MM_OBJ_FI_DATA_TYPE").GetValue()
    Product.Attributes.GetByName("MM_OBJ_TAB_ALERT").Allowed = False

    Product.Attributes.GetByName("MM_OBJ_LABEL_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_PL_LABEL_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_TBL_NAME_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_REC_NAME_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_DATA_TYPE_ERR").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_API_NAME_ERR").Allowed = False


if str(data_typ) == "":

    Product.Attributes.GetByName("MM_OBJ_FI_LEN").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_DECIMAL").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_PL_VALUE").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_PERMISSIONS").Allowed = False
    Product.Attributes.GetByName("MM_OBJ_FI_LOOKUP_OBJECT").Allowed = False
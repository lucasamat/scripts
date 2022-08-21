 # =========================================================================================================================================
#   __script_name : SYRLEXEEND.PY
#   __script_description :  THIS SCRIPT IS USED ACROSS ALL THE APPS DURING THE ONPRODUCTRULEEXECUTIONEND EVENT TO EXECUTE ANY ADDITIONAL RULES AS NECESSARY.
#   __primary_author__ : JOE EBENEZER
#   __create_date :
#   Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import re
import Webcom.Configurator.Scripting.Test.TestProduct
from SYDATABASE import SQL

Sql = SQL()
TestProduct = Webcom.Configurator.Scripting.Test.TestProduct()
import datetime

Product_name = Product.Name
current_tab = str(TestProduct.CurrentTab)
Attr_val = ""
# import Utilities

sql_obj = Sql.GetFirst(
    "select SAPCPQ_ALTTAB_NAME,PRIMARY_OBJECT_NAME from SYTABS (NOLOCK) where SAPCPQ_ALTTAB_NAME = '"
    + str(current_tab)
    + "' and APP_LABEL='"
    + str(Product.Name)
    + "'"
)
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
    if sql_obj:
        if str(sql_obj.PRIMARY_OBJECT_NAME) == "cpq_permissions":
            Question_Permission_Query = Sql.GetList(
                "Select b.EDITABLE_ONINSERT from SYSEFL a (nolock) inner join SYOBJD b (nolock) on a.API_NAME=b.object_name and a.API_FIELD_NAME=b.api_name where a.API_NAME='"
                + str(sql_obj.PRIMARY_OBJECT_NAME)
                + "'"
            )
        else:
            if Datalist:
                if len(Datalist) == 1:
                    ### ADDED THIS CONDITION BECAUSE OF ISSUE WHEN THE LEN OF LIST IS 1 AFTER CONVERSION TO TUPLE IT IS CREATING A ADDITIONAL COMMA

                    Question_Permission_Query = Sql.GetList(
                        "Select b.EDITABLE_ONINSERT from SYSEFL (nolock) a inner join SYOBJD (nolock) b on a.API_NAME=b.object_name and a.API_FIELD_NAME=b.api_name inner join sysect (nolock) c on c.RECORD_ID = a.SECTION_RECORD_ID where a.API_NAME='"
                        + str(sql_obj.PRIMARY_OBJECT_NAME)
                        + "'  and c.SAPCPQ_ATTRIBUTE_NAME in ('"
                        + str(Datalist[0])
                        + "') "
                    )

                else:
                    Question_Permission_Query = Sql.GetList(
                        "Select b.EDITABLE_ONINSERT from SYSEFL (nolock) a inner join SYOBJD (nolock) b on a.API_NAME=b.object_name and a.API_FIELD_NAME=b.api_name inner join sysect (nolock) c on c.RECORD_ID = a.SECTION_RECORD_ID where a.API_NAME='"
                        + str(sql_obj.PRIMARY_OBJECT_NAME)
                        + "'  and c.SAPCPQ_ATTRIBUTE_NAME in "
                        + str(tuple(Datalist))
                        + ""
                    )
            else:
                Question_Permission_Query = Sql.GetList(
                        "Select b.EDITABLE_ONINSERT from SYSEFL (nolock) a inner join SYOBJD (nolock) b on a.API_NAME=b.object_name and a.API_FIELD_NAME=b.api_name inner join sysect (nolock) c on c.RECORD_ID = a.SECTION_RECORD_ID where a.API_NAME='"
                        + str(sql_obj.PRIMARY_OBJECT_NAME)
                        + "'"
                    )
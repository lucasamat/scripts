# =========================================================================================================================================
#   __script_name : SYMCMOBJLP.PY
#   __script_description : THIS SCRIPT IS USED TO LOAD DATA IN OBJECTS LOOKUP IN THE SYSTEM ADMIN APP
#   __primary_author__ : LEO JOSEPH
#   __create_date : 8/31/2020
#   Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct
from SYDATABASE import SQL

Sql = SQL()

Lookup_obj = Product.Attributes.GetByName("MM_OBJ_LOOKUP_OBJECT").GetValue()

Lookup_obj_BIND = ""
Scrpnames1 = ""
Sql_lookup = Sql.GetList("SELECT OBJECT_NAME FROM SYOBJS")
for Scrpnames in Sql_lookup:
    Scrpnames1 = Scrpnames.OBJECT_NAME
    Lookup_obj_BIND += '<option value="' + Scrpnames1 + '" >' + Scrpnames1 + "</option>"

ApiResponse = ApiResponseFactory.JsonResponse(Lookup_obj_BIND)
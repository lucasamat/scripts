# =========================================================================================================================================
#   __script_name : SYMCMOBJBL.PY
#   __script_description : THIS SCRIPT IS USED TO NAVIGATE BACK TO THE LIST FROM THE VIEW/EDIT PAGE IN OBJECTS IN SYSTEM ADMIN APP
#   __primary_author__ : 
#   __create_date :
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
Product.Attributes.GetByName("MM_OBJ_TAB_ALERT").Allowed = False

Product.GetContainerByName("MM_OBJ_CTR_OBJ_INFO").Clear()
Product.GetContainerByName("MM_OBJ_CTR_OBJ_INFO").LoadFromDatabase(
    "SELECT top 1000 * FROM SYOBJH ORDER BY RECORD_ID", ""
)

# =========================================================================================================================================
#   __script_name : SYMCMOBJAC.PY
#   __script_description : THIS SCRIPT IS TO ADD FIELDS FOR THE OBJECTS IN SYSTEM ADMIN APP
#   __primary_author__ : 
#   __create_date :
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
if str(Product.Tabs.GetByName("OBJECTS").IsSelected) == "True":
	Cont = Product.GetContainerByName("MM_OBJ_CTR_OBJ_DATA")
	Cont.Rows.Clear()
	row = Cont.AddNewRow(False)
	
	ContIndex = Product.GetContainerByName("MM_OBJ_CTR_REINDEX_DATA")
	ContIndex.Rows.Clear()
	row = ContIndex.AddNewRow(False)
	

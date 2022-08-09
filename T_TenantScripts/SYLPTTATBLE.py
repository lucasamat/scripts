# =========================================================================================================================================
#   __script_name : SYLPTTATBLE.PY
#   __script_description : THIS SCRIPT IS USED TO LOAD THE PIVOT TABLE IN THE APPS
#   __primary_author__ : JOE EBENEZER
#   __create_date : 27/08/2020
#   Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
"""
TestProduct=Webcom.Configurator.Scripting.Test.TestProduct()
CurrentTabName=TestProduct.CurrentTab
Trace.Write("---Tab Name is---" + str(CurrentTabName))"""
from SYDATABASE import SQL
import Webcom.Configurator.Scripting.Test.TestProduct


Sql = SQL()





def AppRelatedTabContainerLoad():
	
	Product.Attributes.GetByName("QSTN_MM_MOD_CTR_REL_LIST").Allowed = True
	AppRelatedTabContainer = Product.GetContainerByName("QSTN_MM_MOD_CTR_REL_LIST")
	Trace.Write("AttributeContainer -- " + str(AppRelatedTabContainer))
	tableInfo = Sql.GetList(
		"select top 1000 * FROM SYTABS where APP_RECORD_ID= '" + str(rec_id_mod) + "' ORDER BY RECORD_ID ASC"
	)
	Trace.Write("select top 1000 * FROM SYTABS where APP_RECORD_ID= '" + str(rec_id_mod) + "' ORDER BY RECORD_ID ASC")
	ModuleContainer = Product.GetContainerByName("QSTN_MM_MOD_CTR_REL_LIST")
	Product.GetContainerByName("QSTN_MM_MOD_CTR_REL_LIST").Clear()
	if tableInfo != "":
		for item in tableInfo:
			row = ModuleContainer.AddNewRow()
			row["Tab Record No"] = item.RECORD_ID
			row["Tab Name"] = item.TAB_NAME
			if len(str(item.APP_RECORD_ID)) > 0:
				Name = str(item.APP_RECORD_ID)
				ModuleName = Name.split(",")
				ModName = ModuleName[0]
				row["Parent Module"] = ModName
				row["Parent Module Name"] = item.APP_LABEL
			row["Attribute Name"] = item.ATTRIBUTE_NAME
	else:
		Product.GetContainerByName("QSTN_MM_MOD_CTR_REL_LIST").Clear()
	return True


TabName = Param.TabName

State = Param.State

if hasattr(Param, "rec_id_mod"):
	rec_id_mod = Param.rec_id_mod

	
	Product.SetGlobal("rec_id_mod", str(rec_id_mod))
else:
	primary_data = ""

# rec_id_mod = Param.rec_id_mod
try:
	if TabName == "App" and State == "True":
		
		Product.Attributes.GetByName("QSTN_MM_MOD_CTR_REL_LIST").Allowed = True

		
		data = AppRelatedTabContainerLoad()
	if data is not None:
		ApiResponse = ApiResponseFactory.JsonResponse(data)
except:
	Trace.Write(str(TabName) + "tab container has not loaded")
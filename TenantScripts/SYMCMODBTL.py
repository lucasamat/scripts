# =========================================================================================================================================
#   __script_name : SYMCMODBTL.PY
#   __script_description : THIS SCRIPT IS USED TO DO BACK TO LIST IN MODULES IN SYSTEM ADMIN
#   __primary_author__ : THIYAGA RAJAN
#   __create_date :
# ==========================================================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct
TestProduct = Webcom.Configurator.Scripting.Test.TestProduct()

tabvalue = Product.Attributes.GetByName("MA_MTR_ACTIVE_TAB").GetValue()
tabName = ''
if tabvalue == 'Profile':
    Product.Attributes.GetByName("MA_MTR_ACTIVE_TAB").AssignValue('Profiles')

for tab in Product.Tabs:
    if tab.IsSelected == True:
        tabName = str(tab.Name)
        if tabName == 'Tab':
            Product.Attributes.GetByName("MA_MTR_ACTIVE_TAB").AssignValue('Tabs')    

if tabvalue == 'App':    
    Product.Attributes.GetByName("MA_MTR_ACTIVE_TAB").AssignValue('Apps')

try:
    if Product is not None and Product.Name == "SYSTEM ADMIN":
        if Product.Tabs.GetByName("APPS").IsSelected == True:
            Product.Attributes.GetByName("QSTN_MM_MOD_ERROR_MSG").Allowed = False
except:
    Trace.Write("Error in MMModuleBTL")
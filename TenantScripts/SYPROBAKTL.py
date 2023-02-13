# ======================================================================================================================================================
#   __script_name : SYPROBAKTL.PY
#   __script_description : This script is used to Return the user from anywhere in the Profiles Tab to List Grid
#   __primary_author__ : JOE EBENEZER
#   __create_date : 31/08/2020
# =======================================================================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct
TestProduct = Webcom.Configurator.Scripting.Test.TestProduct()
Product_name = Product.Name
Related_Tab = 'Profiles'
current_prod = Product.Name
tabs = Product.Tabs

currentTab = Product.Attributes.GetByName("MA_MTR_ACTIVE_TAB").GetValue()

if currentTab == 'Error Log':
    Related_Tab = "Error Logs"
elif currentTab == 'Role':
    Related_Tab = "Roles"  
else:
    Related_Tab = "Profiles"
if str(current_prod) != "" and str(current_prod) == "SYSTEM ADMIN" and str(currentTab) != "Error Log" and str(currentTab) != "Role":
    Product.Attributes.GetByName("MA_MTR_ACTIVE_TAB").AssignValue("Profiles")
    TestProduct.ChangeTab(Related_Tab)
elif str(currentTab) == "Role":
    Product.Attributes.GetByName("MA_MTR_ACTIVE_TAB").AssignValue("Roles")
    TestProduct.ChangeTab(Related_Tab)   
else:
    Product.Attributes.GetByName("MA_MTR_ACTIVE_TAB").AssignValue("Error Logs")
    TestProduct.ChangeTab(Related_Tab)



if Product.Attributes.GetByName('BTN_PROFILE_ADD_NEW'):
	Product.Attributes.GetByName('BTN_PROFILE_ADD_NEW').Allowed = True
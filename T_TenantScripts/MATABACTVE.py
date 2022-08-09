# =========================================================================================================================================
#   __script_name : MATABACTVE.PY
#   __script_description :
#   __primary_author__ :
#   __create_date :
#   Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
#import Webcom.Configurator.Scripting.Test.TestProduct
def set_active_tab_to_attr():
    for tab in Product.Tabs:
        #Log.Info("TNBI : " + str(tab.Name))
        if tab.IsSelected == True:
            Product.Attributes.GetByName("MA_MTR_ACTIVE_TAB").AssignValue(str(tab.Name))
            break
    return True

set_active_tab_to_attr()

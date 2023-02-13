# =========================================================================================================================================
#   __script_name : SYLDMDMENU.PY
#   __script_description : THIS SCRIPT IS USED TO LOAD APPS FROM THE MAIN MENU
#   __primary_author__ : JOE EBENEZER
#   __create_date :
# ====================================================================================================================================
from SYDATABASE import SQL
import Webcom.Configurator.Scripting.Test.TestProduct
Sql = SQL()


def LOAD_MOD_MENU():
    """Load Home Page in OCT CPQ Based on IS_ADMIN Permission in CPQ."""
    login_is_admin = User.IsAdmin
    Session["USERID"] = User.Id if Session["USERID"] is None else Session["USERID"]
    Session["USERNAME"] = str(User.UserName) if Session["USERNAME"] is None else Session["USERNAME"]
    if Session["USERNAME"] == "CONFIGURATION@BOSTONHARBORCONSULTING.COM":
        record_obj = Sql.GetList(
            "SELECT TOP 100 MM.APP_LABEL, P.PRODUCT_ID, MM.APP_RECORD_ID, MM.DISPLAY_ORDER "
            + " FROM SYAPPS (NOLOCK) MM  LEFT JOIN PRODUCTS (NOLOCK) P ON P.PRODUCT_NAME = "
            + " MM.APP_LABEL WHERE (MM.APP_STATUS='DEPLOYED' OR MM.APP_STATUS='OUT OF SYNC') "
            + " AND MM.SAPCPQ_APP_TYPE='CUSTOM' ORDER BY ABS(MM.DISPLAY_ORDER)"
        )
    else:
        
        record_obj = Sql.GetList(
            """SELECT MOD.* FROM (
                SELECT TOP 100  MM.APP_LABEL,MM.APP_NAME, P.PRODUCT_ID, MM.APP_RECORD_ID, MM.DISPLAY_ORDER,
                MM.APP_ID, ROW_NUMBER() OVER(PARTITION BY MM.APP_LABEL ORDER BY MM.APP_LABEL) AS RANK
                FROM SYAPPS (NOLOCK) MM LEFT JOIN PRODUCTS (NOLOCK) P ON P.PRODUCT_NAME =  MM.APP_NAME
                
                 WHERE
                (MM.APP_STATUS='DEPLOYED' OR MM.APP_STATUS='OUT OF SYNC')
                AND  MM.SAPCPQ_APP_TYPE='CUSTOM'  AND MM.APP_LABEL != 'INTEGRATION_MODULE' AND MM.APP_ID != 'CT'
                ORDER BY MM.DISPLAY_ORDER) MOD WHERE MOD.RANK = 1 """
        )
    test = []
    if record_obj is not None and len(record_obj) > 0:
        for item in record_obj:
            if item.APP_ID == "QT":
                Product_Url = "/QUOTATION/LOADQUOTE.ASPX"
            else:
                Product_Url = "/Configurator.aspx?pid=" + str(item.PRODUCT_ID)
            test.append(item.APP_LABEL + "|" + Product_Url)
    #Trace.Write(str(test))
    return test

ApiResponse = ApiResponseFactory.JsonResponse(LOAD_MOD_MENU())
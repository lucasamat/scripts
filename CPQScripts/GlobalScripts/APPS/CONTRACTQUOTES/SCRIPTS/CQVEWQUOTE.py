
# =========================================================================================================================================
#   __script_name : CQVEWQUOTE.PY
#   __script_description : THIS SCRIPT IS USED TO GET THE QUOTE ID FROM CART PAGE.
#   __primary_author__ : ASHA LYSANDAR
#   __create_date :
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct
import clr
import sys
import System.Net
from System.Text.Encoding import UTF8
from System import Convert
from SYDATABASE import SQL

Sql = SQL()
get_user_id = User.Id
class RedirectQuote:
    def __init__(self, Quote):
        self.quote = Quote

    def view_quote(self, ComposId):        
        if ComposId !='':
            GetQuotes = Sql.GetFirst("SELECT * FROM SAQTMT (NOLOCK) WHERE C4C_QUOTE_ID = '" + str(ComposId) + "'")
            
            #Trace.Write("SELECT USER_NAME AS Username,Password,Domain FROM SYCONF (NOLOCK) where Domain='AMAT_TST'")
            LOGIN_CREDENTIALS = Sql.GetFirst(
                "SELECT USER_NAME AS Username,Password,Domain FROM SYCONF (NOLOCK) where Domain='AMAT_TST'"
            )
            if GetQuotes is None:
                if LOGIN_CREDENTIALS is not None:
                    Login_Username = str(LOGIN_CREDENTIALS.Username)
                    Login_Password = str(LOGIN_CREDENTIALS.Password)
                    authorization = Login_Username + ":" + Login_Password
                    binaryAuthorization = UTF8.GetBytes(authorization)
                    authorization = Convert.ToBase64String(binaryAuthorization)
                    authorization = "Basic " + authorization

                    webclient = System.Net.WebClient()
                    webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/json"
                    webclient.Headers[System.Net.HttpRequestHeader.Authorization] = authorization

                    LOGIN_CRE = Sql.GetFirst("SELECT URL FROM SYCONF (NOLOCK) where EXTERNAL_TABLE_NAME  ='C4C_TO_CPQ_QUOTE'")

                    requestdata = '{\n  "quoteid": "' + str(ComposId) + '"\n}'
                    Trace.Write("requestdata: "+str(requestdata))

                    response_SAQTMT = webclient.UploadString(str(LOGIN_CRE.URL), str(requestdata))
                    Trace.Write("response_SAQTMT: "+str(response_SAQTMT))
                    Log.Info("response_SAQTMT: "+str(response_SAQTMT))
        try:
            c4cId = self.quote.CompositeNumber
        except:
            c4cId = ComposId        
        masterQuoteId = ""
        masterQuoteRecId = ""
        if c4cId is not None:            
            GetQuoteId = Sql.GetFirst(
                "SELECT QUOTE_ID,MASTER_TABLE_QUOTE_RECORD_ID FROM SAQTMT (NOLOCK) WHERE C4C_QUOTE_ID = '" + str(c4cId) + "'"
            )
            if GetQuoteId is not None and GetQuoteId != '':
                masterQuoteId = GetQuoteId.QUOTE_ID
                masterQuoteRecId = GetQuoteId.MASTER_TABLE_QUOTE_RECORD_ID                
        record_obj = Sql.GetList(
            """SELECT MOD.* FROM (
                SELECT TOP 100  MM.APP_LABEL, P.PRODUCT_ID, MM.APP_RECORD_ID, MM.DISPLAY_ORDER,
                AP.VISIBLE, AP.APP_ID, ROW_NUMBER() OVER(PARTITION BY MM.APP_LABEL ORDER BY MM.APP_LABEL) AS RANK
                FROM SYAPPS (NOLOCK) MM LEFT JOIN PRODUCTS (NOLOCK) P ON P.PRODUCT_NAME =  MM.APP_LABEL
                INNER JOIN SYPRAP (NOLOCK) AP ON AP.APP_ID = MM.APP_LABEL
                INNER JOIN  CPQ_PERMISSIONS (NOLOCK) CP ON CP.PERMISSION_ID = AP.PROFILE_RECORD_ID
                INNER JOIN USERS_PERMISSIONS (NOLOCK) UP ON CP.PERMISSION_ID = UP.PERMISSION_ID WHERE
                (MM.APP_STATUS='DEPLOYED' OR MM.APP_STATUS='OUT OF SYNC')
                AND  MM.SAPCPQ_APP_TYPE='CUSTOM'  AND AP.VISIBLE = 1 AND MM.APP_LABEL != 'INTEGRATION_MODULE' AND MM.APP_ID != 'CT' AND UP.USER_ID = {user_Id}
                ORDER BY MM.DISPLAY_ORDER) MOD WHERE MOD.RANK = 1 """.format(
                user_Id=get_user_id
            )
        )
        getappdata = ''
        if len(record_obj) == 0:
            getappdata = "No access to app"        
        return masterQuoteId, masterQuoteRecId,getappdata


try:
    ComposId = Param.Id
except:
    ComposId = ''
quoteObj = RedirectQuote(Quote)
ApiResponse = ApiResponseFactory.JsonResponse(quoteObj.view_quote(ComposId))


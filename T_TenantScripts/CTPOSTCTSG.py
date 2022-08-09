# =========================================================================================================================================
#   __script_name : CTPOSTCTSG.PY
#   __script_description : THIS SCRIPT IS USED TO GET CONTRACT ID FROM SSCM AND STORED IN SYINPL
#   __primary_author__ : Baji
#   __create_date :
#   Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import sys
import clr
import System.Net
from System.Text.Encoding import UTF8
from System import Convert

try:

    Contract_Id = [str(param_result.Value) for param_result in Param.CPQ_Columns]
    Parameter=SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME='SELECT' ")
    
    sessionid = SqlHelper.GetFirst("SELECT NEWID() AS A")
    timestamp_sessionid = "'" + str(sessionid.A) + "'"
    
    #Log.Info("CTPOSTCTSG Contract ID --->"+str(Contract_Id))
    
    Flag = 'False'
    
    if len(Contract_Id) >0:
        Flag = "True"
        
        for Cnt_Id in Contract_Id:
            primaryQueryItems = SqlHelper.GetFirst( ""+ str(Parameter.QUERY_CRITERIA_1)+ " SYINPL (INTEGRATION_PAYLOAD,SESSION_ID,INTEGRATION_NAME,CpqTableEntryDateModified)  select ''"+str(Cnt_Id)+ "'','"+ str(timestamp_sessionid)+ "',''CRM_TO_CPQ_CONTRACT_ID'',GETDATE() ' ")
            
            
    if Flag == "True":
        ApiResponse = ApiResponseFactory.JsonResponse(
            {"Response": [{"Status": "200", "Message": "CRM Contract ID has been successfully stored in the CPQ staging table. "}]}
        )
    else:
        ApiResponse = ApiResponseFactory.JsonResponse(
            {"Response": [{"Status": "200", "Message": "No Data available in the input json."}]}
        )
        
except:
    Log.Info("CTPOSTCTSG ERROR---->:" + str(sys.exc_info()[1]))
    Log.Info("CTPOSTCTSG ERROR LINE NO---->:" + str(sys.exc_info()[-1].tb_lineno))
    ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "400", "Message": str(sys.exc_info()[1])}]})

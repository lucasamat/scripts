# =========================================================================================================================================
#   __script_name : QTPOSTACRM.PY
#   __script_description : THIS SCRIPT IS USED TO SEND QUOTE INFROMATION FROM CPQ TO CRM in ASYNC
#   __primary_author__ : BAJI
#   __create_date :
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import clr
import System.Net
from System.Text.Encoding import UTF8
from System import Convert
import sys

#result=ScriptExecutor.ExecuteGlobal('QTPOSTQCRM',{'QUOTE_ID':'MAQ000001-RW000-06012020','Fun_type':'cpq_to_crm'})

try:	

	def cpq_to_crm(Qt_id):
		LOGIN_CREDENTIALS = SqlHelper.GetFirst("SELECT USER_NAME as Username,Password,Domain FROM SYCONF where Domain='AMAT_TST'")
		if LOGIN_CREDENTIALS is not None:
			Login_Username = str(LOGIN_CREDENTIALS.Username)
			Login_Password = str(LOGIN_CREDENTIALS.Password)
			authorization = Login_Username+":"+Login_Password
			binaryAuthorization = UTF8.GetBytes(authorization)
			authorization = Convert.ToBase64String(binaryAuthorization)
			authorization = "Basic " + authorization


			webclient = System.Net.WebClient()
			webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/json"
			webclient.Headers[System.Net.HttpRequestHeader.Authorization] = authorization;
			
			result = '{\"CPQ_Columns\":\r\n{\r\n\"QUOTE_ID\" : \"'+str(Qt_id)+'\"\r\n}\r\n}\r\n'
			
			Log.Info("28-10-2020 result ---->"+str(result))	

			LOGIN_CRE = SqlHelper.GetFirst("SELECT URL FROM SYCONF where EXTERNAL_TABLE_NAME ='CPQ_TO_CRM_QUOTE_ASYNC'")
			response_MAMSOP = webclient.UploadString(str(LOGIN_CRE.URL), str(result))
			#ApiResponse = ApiResponseFactory.JsonResponse({"Response":[{'Status':'200','Message':"Data Completely Uploaded"}]})
			
			
	def cpq_to_sscm(Qt_id):
		LOGIN_CREDENTIALS = SqlHelper.GetFirst("SELECT USER_NAME as Username,Password,Domain FROM SYCONF where Domain='AMAT_TST'")
		if LOGIN_CREDENTIALS is not None:
			Login_Username = str(LOGIN_CREDENTIALS.Username)
			Login_Password = str(LOGIN_CREDENTIALS.Password)
			authorization = Login_Username+":"+Login_Password
			binaryAuthorization = UTF8.GetBytes(authorization)
			authorization = Convert.ToBase64String(binaryAuthorization)
			authorization = "Basic " + authorization


			webclient = System.Net.WebClient()
			webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/json"
			webclient.Headers[System.Net.HttpRequestHeader.Authorization] = authorization;
			
			result = '{\"CPQ_Columns\":\r\n{\r\n\"QUOTE_ID\" : \"'+str(Qt_id)+'\"\r\n}\r\n}\r\n'
			
			Log.Info("28-10-2020 result ---->"+str(result))	

			LOGIN_CRE = SqlHelper.GetFirst("SELECT URL FROM SYCONF where EXTERNAL_TABLE_NAME ='CPQ_TO_SSCM_QUOTE_ASYNC'")
			response_MAMSOP = webclient.UploadString(str(LOGIN_CRE.URL), str(result))
			#ApiResponse = ApiResponseFactory.JsonResponse({"Response":[{'Status':'200','Message':"Data Completely Uploaded"}]})
			
	
	input_data = Param.QUOTE_ID
	Log.Info("20202020 input_data ---->"+str(input_data))
	Fun_type = Param.Fun_type
	Log.Info("20202020 Fun_type ---->"+str(Fun_type))
	if len(Fun_type) > 0:
		if str(Fun_type).upper() == 'CPQ_TO_CRM':
			Funtion_call = cpq_to_crm(input_data)
		elif str(Fun_type).upper() == 'CPQ_TO_SSCM':
			Funtion_call = cpq_to_sscm(input_data)
	
			
except:
	Log.Info("QTPOSTACRM ERROR---->:" + str(sys.exc_info()[1]))
	Log.Info("QTPOSTACRM ERROR LINE NO---->:" + str(sys.exc_info()[-1].tb_lineno))
	#ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "400", "Message": str(sys.exc_info()[1])}]})
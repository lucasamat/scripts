# =========================================================================================================================================
#   __script_name : SAGETCLMUP.PY
#   __script_description : THIS SCRIPT IS USED TO RETRIVE THE CLM AGREEMENT INFO AND UPDATE IN SAQTRV
#   __primary_author__ : BAJI
#   __create_date :
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================

import clr
import sys
import datetime
import System.Net
from System.Text.Encoding import UTF8
from System import Convert
import System
from System.Net import HttpWebRequest, NetworkCredential
from System.Net import *
from System.Net import CookieContainer
from System.Net import Cookie
from System.Net import WebRequest
from System.Net import HttpWebResponse
from System import Uri

try:
	Parameter=SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME='SELECT' ")
	Parameter1 = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'UPD' ")

	Oauth_info = SqlHelper.GetFirst("SELECT  DOMAIN,URL FROM SYCONF where EXTERNAL_TABLE_NAME ='OAUTH'")

	LOGIN_CRE = SqlHelper.GetFirst("SELECT URL FROM SYCONF (nolock) where EXTERNAL_TABLE_NAME ='CLM_DELETE_METHOD'")
	webRequest = str(LOGIN_CRE.URL)

	def GetNewRequest(targetUrl, Btoken):

		newRequest = HttpWebRequest.Create(targetUrl)
		newRequest.AllowAutoRedirect = 0
		newRequest.Headers.Add("AUTHORIZATION", Btoken)
		newRequest.Method = 'DELETE'
		newRequest.ContentLength = 0
		newRequest.ContentType = 'application/json'


		return newRequest



	requestdata =Oauth_info.DOMAIN
	webclient = System.Net.WebClient()
	webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/x-www-form-urlencoded"
	response = webclient.UploadString(Oauth_info.URL,str(requestdata))

	response = eval(response)
	access_token = response['access_token']
	Btoken = "Bearer " + access_token


	rew = GetNewRequest(webRequest, Btoken)
	resp = rew.GetResponse()			

	streamReader = StreamReader(resp.GetResponseStream())
	jsonData = streamReader.ReadToEnd()	

	Log.Info("456 -->"+str(jsonData))
	primaryQueryItems = SqlHelper.GetFirst( ""+ str(Parameter.QUERY_CRITERIA_1)+ " SYINPL (INTEGRATION_PAYLOAD,INTEGRATION_NAME,CPQTABLEENTRYDATEADDED,CPQTABLEENTRYADDEDBY)  select ''"+str(jsonData)+ "'',''CLM_AGREEMENT_INFO'',Getdate(),''"+str(User.UserName)+ "'' ' ")

	jsonData = jsonData.split("'")

	rebuilt_data = eval(str(jsonData[1]))

	if 'CorrelationID' in rebuilt_data:
		Qt_Id = rebuilt_data['CorrelationID']
		
		primaryQueryItems = SqlHelper.GetFirst(
			""
			+ str(Parameter1.QUERY_CRITERIA_1)
			+ "  SAQTRV SET CLM_AGREEMENT_NUM=''"+ str(rebuilt_data['AgreementNumber'])+"'',CLM_AGREEMENT_OWNER = ''"+ str(rebuilt_data['AgreementID'])+"'',CLM_AGREEMENT_STATUS = ''"+ str(rebuilt_data['AgreementStatus'])+"'' FROM SAQTRV (NOLOCK) WHERE QUOTE_ID = ''"+ str(Qt_Id)+"''  ' "
		)

except:
	Log.Info("SAGETCLMUP ERROR---->:" + str(sys.exc_info()[1]))
	Log.Info("SAGETCLMUP ERROR LINE NO---->:" + str(sys.exc_info()[-1].tb_lineno))
	ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "400", "Message": str(sys.exc_info()[1])}]})
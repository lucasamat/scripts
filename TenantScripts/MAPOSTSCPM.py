# =========================================================================================================================================
#   __script_name : MAPOSTSCPM.PY
#   __script_description : THIS SCRIPT IS USED TO INSERT SSCM Tool PM Kit Information DATA TO CPQ(SYINPL) TABLE USING WEB METHOD.
#   __primary_author__ : BAJI
#   __create_date :
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import sys
import datetime 
import clr
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
from SYDATABASE import SQL
Log.Info("MAPOSTSCPM ---->Hitting")

try:
	LOGIN_CRE = SqlHelper.GetFirst("SELECT URL FROM SYCONF (nolock) where EXTERNAL_TABLE_NAME ='PMKIT_GETMETHOD'")
	
	webRequest = str(LOGIN_CRE.URL)
	Check_flag = 1
	
	if Check_flag == 1:

		def GetNewRequest(targetUrl, Btoken):

			newRequest = HttpWebRequest.Create(targetUrl)
			newRequest.AllowAutoRedirect = 0
			newRequest.Headers.Add("AUTHORIZATION", Btoken)
			newRequest.Headers.Add("Environment-Identifier", 'P')
			newRequest.Method = 'GET'
			newRequest.ContentLength = 0
			newRequest.ContentType = 'application/json'

			return newRequest

		Oauth_info = SqlHelper.GetFirst("SELECT  DOMAIN,URL FROM SYCONF where EXTERNAL_TABLE_NAME ='OAUTH'")

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

		conv_data = jsonData.replace("'",'%%')
		l =  conv_data.rindex("%%")
		f = conv_data.index("%%")+2
		
		
		if '[]' not in conv_data[f:l]:	
		
			Parameter = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'SELECT' ")
					
			primaryQueryItems = SqlHelper.GetFirst( ""+ str(Parameter.QUERY_CRITERIA_1)+ " SYINPL (INTEGRATION_PAYLOAD,INTEGRATION_NAME,CpqTableEntryDateModified)  select ''"+conv_data[f:l]+ "'',''SSCM_TO_CPQ_TOOL_PMKIT_DATA'',GETDATE() ' ")
		else:
			Check_flag = 0			
	
	
	Resp_msg = """{"Response": [{"Status": "200","Message": "SSCM_TO_CPQ_TOOL_PMKIT_DATA Data Sucessfully Uploaded ."}]}"""
	Result = Resp_msg

except:		
	Log.Info("MAPOSTSCPM ERROR---->:" + str(sys.exc_info()[1]))
	Log.Info("MAPOSTSCPM ERROR LINE NO---->:" + str(sys.exc_info()[-1].tb_lineno))
	error_info = {"Response": [{"Status": "400", "Message": str(sys.exc_info()[1])}]}
	Result  = str(error_info)
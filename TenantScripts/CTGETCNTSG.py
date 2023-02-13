# =========================================================================================================================================
#   __script_name : CTGETCNTSG.PY
#   __script_description : THIS SCRIPT IS USED TO INSERT CRM TO CPQ DATA IN STAGING TABLE FROM ECC TO CPQ
#   __primary_author__ : BAJI
#   __create_date : 2020-11-26
#   Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
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
from SYDATABASE import SQL

try:
	check_flag = 0	
	Parameter = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'SELECT' ")
	Parameter1 = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'UPD' ")
	
	primaryQueryItems = SqlHelper.GetFirst( ""+ str(Parameter1.QUERY_CRITERIA_1)+ " SYINPL SET STATUS = ''DUPLICATE'' FROM SYINPL (NOLOCK)  JOIN(SELECT MIN(CPQTABLEENTRYID) AS CPQTABLEENTRYID,INTEGRATION_PAYLOAD FROM SYINPL (NOLOCK) WHERE INTEGRATION_NAME = ''CRM_TO_CPQ_CONTRACT_ID'' AND ISNULL(STATUS ,'''')= '''' GROUP BY INTEGRATION_PAYLOAD HAVING COUNT(CPQTABLEENTRYID)>1) SUB_SYINPL ON SYINPL.INTEGRATION_PAYLOAD = SUB_SYINPL.INTEGRATION_PAYLOAD  WHERE SYINPL.CPQTABLEENTRYID <> SUB_SYINPL.CPQTABLEENTRYID  ' ")
	
	LOGIN_CRE = SqlHelper.GetFirst("SELECT URL FROM SYCONF (nolock) where EXTERNAL_TABLE_NAME ='CONTRACT_DATA_GETMETHOD'")
	while check_flag == 0:
		
		ContractIdquery = SqlHelper.GetList("SELECT top 1 INTEGRATION_PAYLOAD from SYINPL(NOLOCK) where INTEGRATION_NAME = 'CRM_TO_CPQ_CONTRACT_ID' and ISNULL(STATUS ,'')= '' ")			
		
		if len(ContractIdquery) > 0:
			for Cnt_Id in ContractIdquery:		

				contract_input = '{ "ContractIDJSON" : "'+str(Cnt_Id.INTEGRATION_PAYLOAD)+'" }'
                

				webRequest = str(LOGIN_CRE.URL).format(contract_input)
				Log.Info("456456 webRequest--->"+str(webRequest))
				
				
				def GetNewRequest(targetUrl, Btoken):

					newRequest = HttpWebRequest.Create(targetUrl)
					newRequest.AllowAutoRedirect = 0
					newRequest.Headers.Add("AUTHORIZATION", Btoken)
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
				sessionid = SqlHelper.GetFirst("SELECT NEWID() AS Guid")
				timestamp_sessionid = "'" + str(sessionid.Guid) + "'"				

				primaryQueryItems = SqlHelper.GetFirst( ""+ str(Parameter.QUERY_CRITERIA_1)+ " SYINPL (INTEGRATION_PAYLOAD,SESSION_ID,INTEGRATION_NAME,CpqTableEntryDateModified,INTEGRATION_KEY)  select N''"+conv_data+ "'','"+ str(timestamp_sessionid)+ "',''CRM_TO_CPQ_CONTRACT_DATA'',GETDATE(),''"+str(Cnt_Id.INTEGRATION_PAYLOAD)+ "'' ' ")
				
				primaryQueryItems = SqlHelper.GetFirst(	""+ str(Parameter1.QUERY_CRITERIA_1)+ "  SYINPL set STATUS = ''PROCESSED'' from SYINPL  (NOLOCK) WHERE INTEGRATION_PAYLOAD  = ''"+str(Cnt_Id.INTEGRATION_PAYLOAD)+ "'' and INTEGRATION_NAME = ''CRM_TO_CPQ_CONTRACT_ID'' AND ISNULL(STATUS ,'''')= '''' ' "	)
					
		else:		
			check_flag = 1
	
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
		
		result = '<?xml version="1.0" encoding="UTF-8"?><soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"><soapenv:Body ></soapenv:Body></soapenv:Envelope>'
		
		LOGIN_CRE = SqlHelper.GetFirst("SELECT URL FROM SYCONF where EXTERNAL_TABLE_NAME ='CPQ_TO_CRM_GETMETHOD_ASYNC'")
		Async = webclient.UploadString(str(LOGIN_CRE.URL), str(result))
	
except:
	Log.Info("CTGETCNTSG ERROR---->:" + str(sys.exc_info()[1]))
	Log.Info("CTGETCNTSG ERROR LINE NO---->:" + str(sys.exc_info()[-1].tb_lineno))
	ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "400", "Message": str(sys.exc_info()[1])}]})
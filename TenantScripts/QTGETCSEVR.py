# =========================================================================================================================================
#   __script_name : QTGETCSEVR.PY
#   __script_description : THIS SCRIPT IS USED TO INSERT CPQ_SSCM_TOOL_VERSION Information DATA TO CPQ(SYINPL) TABLE USING WEB METHOD.
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
 
try:
	LOGIN_CRE = SqlHelper.GetFirst("SELECT URL FROM SYCONF (nolock) where EXTERNAL_TABLE_NAME ='CPQ_TO_SSCM_TOOL_VERSION'") 

	webRequest = str(LOGIN_CRE.URL) 
	Check_flag = 1

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
	

	if '[]' not in conv_data:
		Parameter = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'SELECT' ")
				
		primaryQueryItems = SqlHelper.GetFirst( ""+ str(Parameter.QUERY_CRITERIA_1)+ " SYINPL (INTEGRATION_PAYLOAD,INTEGRATION_NAME,CpqTableEntryDateModified)  select ''"+conv_data+ "'',''CPQ_SSCM_TOOL_VERSION'',GETDATE() ' ")
	else:
		Check_flag = 0
			
		
	Table_Name = 'TOOL_VERSION_INBOUND'

	TempTable = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(Table_Name)+"'' ) BEGIN DROP TABLE "+str(Table_Name)+" END CREATE TABLE "+str(Table_Name)+" (EQUIPMENT_ID VARCHAR(250) ,ASSEMBLY_ID VARCHAR(250) ,PREV_ARCM_MODULE_ID VARCHAR(250) ,PREV_MODULE_VERSION VARCHAR(250) ,NEW_ARCM_MODULE_ID VARCHAR(250) ,NEW_MODULE_VERSION VARCHAR(250) ,	CREATEDBY VARCHAR(250) ,CREATEDDATE VARCHAR(250))'")
	
	jsonData = eval(jsonData.replace("'",'%%'))
	
	for record_dict in jsonData:
		Stagingquery = SqlHelper.GetFirst( ""+ str(Parameter.QUERY_CRITERIA_1)+ " "+str(Table_Name)+" (EQUIPMENT_ID, ASSEMBLY_ID, PREV_ARCM_MODULE_ID, PREV_MODULE_VERSION, NEW_ARCM_MODULE_ID, NEW_MODULE_VERSION, CREATEDBY, CREATEDDATE)  select  N''"+str(record_dict['EQUIPMENT_ID'])+ "'',''"+str(record_dict['ASSEMBLY_ID'])+ "'',''"+str(record_dict['PREV_ARCM_MODULE_ID'])+ "'',''"+str(record_dict['PREV_MODULE_VERSION'])+ "'',''"+str(record_dict['NEW_ARCM_MODULE_ID'])+ "'',''"+str(record_dict['NEW_MODULE_VERSION'])+ "'',''"+str(record_dict['CREATEDBY'])+ "'',''"+str(record_dict['CREATEDDATE'])+ "'' ' ")
	
	S = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE SAQICA SET NEW_MODULE_VERSION_ID = NEW_MODULE_VERSION,NEW_MODULE_ID =NEW_ARCM_MODULE_ID,MODVRS_DIRTY_FLAG = ''TRUE''  FROM TOOL_VERSION_INBOUND(NOLOCK) A JOIN SAQICA (NOLOCK) B ON A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.ASSEMBLY_ID = B.ASSEMBLY_ID JOIN SAQTRV(NOLOCK) D ON B.QUOTE_ID = D.QUOTE_ID AND B.QTEREV_ID = D.QTEREV_ID WHERE NEW_MODULE_VERSION <> ISNULL(B.MODULE_VERSION_ID,'''') AND REVISION_STATUS IN (''CFG-CONFIGURATION'',''CFG-ACQUIRING'',''CFG-ON HOLD - COSTING'',''PRR-ON HOLD PRICING'',''PRI-PRICING''  )  '")
	
	S = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE SAQICO SET MODVRS_DIRTY_FLAG = SAQICA.MODVRS_DIRTY_FLAG  FROM SAQICA (NOLOCK) JOIN SAQICO(NOLOCK) ON SAQICA.QUOTE_ID = SAQICO.QUOTE_ID AND SAQICA.QTEREV_ID = SAQICO.QTEREV_ID AND SAQICA.LINE = SAQICO.LINE AND SAQICA.EQUIPMENT_ID = SAQICO.EQUIPMENT_ID WHERE ISNULL(SAQICA.MODVRS_DIRTY_FLAG,''FALSE'')=''TRUE''  '")
	
	S = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE SAQRIT SET SAQRIT.MODVRS_DIRTY_FLAG = SAQICO.MODVRS_DIRTY_FLAG  FROM SAQRIT (NOLOCK) JOIN SAQICO(NOLOCK) ON SAQRIT.QUOTE_ID = SAQICO.QUOTE_ID AND SAQRIT.QTEREV_ID = SAQICO.QTEREV_ID AND SAQRIT.LINE = SAQICO.LINE WHERE ISNULL(SAQICO.MODVRS_DIRTY_FLAG,''FALSE'')=''TRUE''  '")
	
	S = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE SAQTRV SET MODVRS_DIRTY_FLAG = SAQRIT.MODVRS_DIRTY_FLAG  FROM SAQRIT (NOLOCK) JOIN SAQTRV(NOLOCK) ON SAQRIT.QUOTE_ID = SAQTRV.QUOTE_ID AND SAQRIT.QTEREV_ID = SAQTRV.QTEREV_ID WHERE ISNULL(SAQRIT.MODVRS_DIRTY_FLAG,''FALSE'')=''TRUE''  '")
	
	ApiResponse = ApiResponseFactory.JsonResponse(
		{
			"Response": [
				{
					"Status": "200",
					"Message": "Data Sucessfully Uploaded ."
				}
			]
		}
	)
except:		
	Log.Info("QTGETCSEVR ERROR---->:" + str(sys.exc_info()[1]))
	Log.Info("QTGETCSEVR ERROR LINE NO---->:" + str(sys.exc_info()[-1].tb_lineno))
	ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "400", "Message": str(sys.exc_info()[1])}]})
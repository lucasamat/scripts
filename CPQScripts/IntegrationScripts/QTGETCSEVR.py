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
		newRequest.Headers.Add("Environment-Identifier", 'X')
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

	Table_Name1 = 'TOOL_VERQTE_INBOUND'

	TempTable1 = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(Table_Name1)+"'' ) BEGIN DROP TABLE "+str(Table_Name1)+" END CREATE TABLE "+str(Table_Name1)+" (EQUIPMENT_ID VARCHAR(250) ,ASSEMBLY_ID VARCHAR(250) ,PREV_ARCM_MODULE_ID VARCHAR(250) ,PREV_MODULE_VERSION VARCHAR(250) ,NEW_ARCM_MODULE_ID VARCHAR(250) ,NEW_MODULE_VERSION VARCHAR(250) ,	CREATEDBY VARCHAR(250) ,CREATEDDATE VARCHAR(250),QUOTE_ID VARCHAR(250),QTEREV_ID VARCHAR(250),LINE INT )'")
	
	jsonData = eval(jsonData.replace("'",'%%'))
	
	for record_dict in conv_data:
		Stagingquery = SqlHelper.GetFirst( ""+ str(Parameter.QUERY_CRITERIA_1)+ " "+str(Table_Name)+" (EQUIPMENT_ID, ASSEMBLY_ID, PREV_ARCM_MODULE_ID, PREV_MODULE_VERSION, NEW_ARCM_MODULE_ID, NEW_MODULE_VERSION, CREATEDBY, CREATEDDATE)  select  N''"+str(record_dict['EQUIPMENT_ID'])+ "'',''"+str(record_dict['ASSEMBLY_ID'])+ "'',''"+str(record_dict['PREV_ARCM_MODULE_ID'])+ "'',''"+str(record_dict['PREV_MODULE_VERSION'])+ "'',''"+record_dict['NEW_ARCM_MODULE_ID']+ "'',''"+str(record_dict['NEW_MODULE_VERSION'])+ "'',''"+str(record_dict['CREATEDBY'])+ "'',''"+str(record_dict['CREATEDDATE'])+ "'' ' ")
	
	S = SqlHelper.GetFirst("sp_executesql @T=N'insert TOOL_VERQTE_INBOUND (EQUIPMENT_ID,ASSEMBLY_ID,PREV_ARCM_MODULE_ID,PREV_MODULE_VERSION,NEW_ARCM_MODULE_ID,NEW_MODULE_VERSION,QUOTE_ID,QTEREV_ID,LINE)SELECT DISTINCT A.EQUIPMENT_ID,A.ASSEMBLY_ID,A.PREV_ARCM_MODULE_ID,A.PREV_MODULE_VERSION,A.NEW_ARCM_MODULE_ID,A.NEW_MODULE_VERSION,C.QUOTE_ID,C.QTEREV_ID,C.LINE FROM TOOL_VERSION_INBOUND(NOLOCK) A JOIN SAQICA (NOLOCK) B ON A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.ASSEMBLY_ID = B.ASSEMBLY_ID JOIN SAQICO(NOLOCK) ON B.QUOTE_ID = C.QUOTE_ID AND B.QTEREV_ID = C.QTEREV_ID AND B.EQUIPMENT_ID = C.EQUIPMENT_ID AND B.LINE = C.LINE JOIN SAQTRV(NOLOCK) D ON C.QUOTE_ID = D.QUOTE_ID AND C.QTEREV_ID = D.QTEREV_ID WHERE NEW_MODULE_VERSION <> B.MODULE_VERSION_ID AND REVISION_STATUS IN (''CFG-CONFIGURATION'',''CFG-ACQUIRING'',''CFG-ON HOLD - COSTING'',''PRR-ON HOLD PRICING'',''PRI-PRICING''  )  '")
	
	S = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET STATUS = '''' FROM SAQICO (NOLOCK)A JOIN TOOL_VERQTE_INBOUND (NOLOCK)B ON A.QUOTE_ID = B.QUOTE_ID AND A.QTEREV_ID = B.QTEREV_ID AND A.LINE = B.LINE AND A.EQUIPMENT_ID = B.EQUIPMENT_ID  '")
	
	S = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET STATUS = ''CFG-ACQUIRING'' FROM SAQTRV (NOLOCK)A JOIN TOOL_VERQTE_INBOUND (NOLOCK)B ON A.QUOTE_ID = B.QUOTE_ID AND A.QTEREV_ID = B.QTEREV_ID WHERE REVISION_STATUS IN (''CFG-CONFIGURATION'',''CFG-ACQUIRING'',''CFG-ON HOLD - COSTING'',''PRR-ON HOLD PRICING'',''PRI-PRICING''  )  '")
	
	sqlqueryinfo = SqlHelper.GetList("SELECT DISTINCT QTEREV_ID,QUOTE_ID FROM TOOL_VERQTE_INBOUND(NOLOCK) ")

	if len(sqlqueryinfo) > 0:
		for data in sqlqueryinfo:
			Callingsscmpricing = ScriptExecutor.ExecuteGlobal("QTPOSTACRM",{"QUOTE_ID":data.QUOTE_ID,"REVISION_ID":data.QTEREV_ID,'Fun_type':'CPQ_TO_SSCM'})


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
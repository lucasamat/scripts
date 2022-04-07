
# ======================================================================================================================================================
#   __script_name : SYPRCTRDEL.PY
#   __script_description : This script is used to Delete the Record in Profiles Tab Both View Delete and Grid Delete (In System Admin )
#   __primary_author__ : JOE EBENEZER
#   __create_date : 31/08/2020
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# =======================================================================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct
from SYDATABASE import SQL
Sql = SQL()
import clr
clr.AddReference("System.Net")
import System.Net
from System.Text.Encoding import UTF8
from System import Convert
from System.Net import *

Trace = Trace  # pylint: disable=E0602
SqlHelper = SqlHelper  # pylint: disable=E0602
WebRequest = WebRequest  # pylint: disable=E0602
CookieContainer = CookieContainer  # pylint: disable=E0602
StreamReader = StreamReader  # pylint: disable=E0602

def nativeProfileDelete(PROFILE_RECORD_ID):

	LOGIN_CREDENTIALS = SqlHelper.GetFirst("SELECT Username,Password,Domain FROM SYCONF (nolock)")
	if LOGIN_CREDENTIALS is not None:
		Login_Username = str(LOGIN_CREDENTIALS.Username)
		Login_Password = str(LOGIN_CREDENTIALS.Password)
		Login_Domain = str(LOGIN_CREDENTIALS.Domain)

	rssandboxBaseURL = "https://rssandbox.webcomcpq.com"
	authenticationUrl = rssandboxBaseURL+'/api/rd/v1/Core/Login?username='+Login_Username+'&password='+Login_Password+'&domain='+Login_Domain
	authRequest = WebRequest.Create(str(authenticationUrl))
	authRequest.Method = 'POST'
	authRequest.CookieContainer = CookieContainer()
	authRequest.ContentLength = 0
	authResponse = authRequest.GetResponse()
	cookies = authResponse.Cookies
	authResponseData = StreamReader(authResponse.GetResponseStream()).ReadToEnd()
	xcrf = str(authResponseData).replace('"', '')
	#Trace.Write("X-CSRF-Token : " + str(xcrf))

	#cookies
	coookies = ''
	if cookies is not None:
		for cookie in cookies:
			coookies = coookies + str(cookie) + ";"
	Trace.Write("COOKIES : " + coookies)


	data='grant_type=password&username='+Login_Username+'&password='+Login_Password+'&domain='+Login_Domain+''
	#Trace.Write('53--data-----'+str(data))
	authenticationapitokenUrl = "https://rssandbox.webcomcpq.com/basic/api/token"
	authRequesttoken = WebRequest.Create(str(authenticationapitokenUrl))
	authRequesttoken.Method = 'DELETE'
	webclienttoken = System.Net.WebClient()
	webclienttoken.Headers[System.Net.HttpRequestHeader.Host] = "rssandbox.webcomcpq.com"
	webclienttoken.Headers[System.Net.HttpRequestHeader.ContentType] = "application/json; charset=utf-8"
	webclienttoken.Headers[System.Net.HttpRequestHeader.Cookie]= coookies
	webclienttoken.Headers.Add("X-CSRF-Token", xcrf)
	response = webclienttoken.UploadString(str(authenticationapitokenUrl), data)
	accessToken = 'Bearer ' + str(response).split(":")[1].split(",")[0].replace('"', '')
	#Trace.Write("ACCESS TOKEN : " + accessToken )
	#Trace.Write('60-------PROFILE_RECORD_ID-----'+str(PROFILE_RECORD_ID))
	prf_ID = ''
	datasave='''{
		"Id":%s
		
	}'''%(PROFILE_RECORD_ID)
	#Trace.Write('188-------------datasave----'+str(datasave))
	setPermissionURL = rssandboxBaseURL + '/setup/api/v1/admin/permissionGroups/'+str(int(PROFILE_RECORD_ID))
	webclient = System.Net.WebClient()
	webclient.Headers[System.Net.HttpRequestHeader.Host] = "rssandbox.webcomcpq.com"
	webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/json; charset=utf-8"
	webclient.Headers[System.Net.HttpRequestHeader.Cookie]= coookies
	webclient.Headers.Add("X-CSRF-Token", xcrf)
	webclient.Headers.Add("Authorization", accessToken)
	response = webclient.UploadString(str(setPermissionURL), "DELETE", "")
	#Trace.Write("PERMISSIONS : " + str(response.encode('ascii','ignore')) )
	return 'response'

Product.Attributes.GetByName("MA_MTR_ACTIVE_TAB").AssignValue('')
for tab in Product.Tabs:
	if tab.IsSelected==True:
		if Product.Attributes.GetByName("MA_MTR_ACTIVE_TAB") is not None:
			if str(tab.Name)!="Profiles" and str(tab.Name)!="Profile" and str(tab.Name)!="Roles" and str(tab.Name)!="Role":
				Product.Attributes.GetByName("MA_MTR_ACTIVE_TAB").AssignValue('Profiles')
def Profile_container_Delete(PROFILE_RECORD_ID,Object_Name,MODE):
	tableRelInfo=''
	Profile_AutoNumber_APIS = "SELECT API_NAME,PARENT_OBJECT_RECORD_ID FROM  SYOBJD WHERE DATA_TYPE='AUTO NUMBER' AND OBJECT_NAME='"+str(Object_Name)+"'"
	Profile_AutoNumber_API = Sql.GetFirst(Profile_AutoNumber_APIS)
	nativeProfileDelete(PROFILE_RECORD_ID)
	
	if PROFILE_RECORD_ID is not None:
	
		tableInfo = Sql.GetTable('SYPRAP')
		query_Res =  Sql.GetList("SELECT CpqTableEntryId FROM SYPRAP WHERE PROFILE_RECORD_ID = '"+str(PROFILE_RECORD_ID)+"' ")
		for val in query_Res:
			tableInfo.AddRow(val)
		Sql.Delete(tableInfo)
		tableInfoTB = Sql.GetTable('SYPRTB')
		query_ResTB =  Sql.GetList("SELECT CpqTableEntryId FROM SYPRTB WHERE PROFILE_RECORD_ID = '"+str(PROFILE_RECORD_ID)+"' ")
		for val in query_ResTB:
			tableInfoTB.AddRow(val)
		Sql.Delete(tableInfoTB)
		
		tableInfoSN = Sql.GetTable('SYPRSN')
		query_ResSN =  Sql.GetList("SELECT CpqTableEntryId FROM SYPRSN WHERE PROFILE_RECORD_ID = '"+str(PROFILE_RECORD_ID)+"' ")
		for val in query_ResSN:
			tableInfoSN.AddRow(val)
		Sql.Delete(tableInfoSN)
		
		

		
		

		
		
		
			
	return 0;
		
def Role_container_Delete(ROLE_RECORD_ID,Object_Name,MODE):
	tableRelInfo=''
	Role_AutoNumber_APIS = "SELECT API_NAME,PARENT_OBJECT_RECORD_ID FROM  SYOBJD WHERE DATA_TYPE='AUTO NUMBER' AND OBJECT_NAME='"+str(Object_Name)+"'"
	Role_AutoNumber_API = Sql.GetFirst(Role_AutoNumber_APIS)
	if Role_AutoNumber_API is not None and str(Role_AutoNumber_API)!='':
		Role_AutoNumber_APISE = str(Role_AutoNumber_API.API_NAME)
		Role_Tab_Obj_id = str(Role_AutoNumber_API.PARENT_OBJECT_RECORD_ID)
		
		Role_Recordse = "SELECT * FROM "+str(Object_Name)+" WHERE "+str(Role_AutoNumber_APISE)+" = '"+str(ROLE_RECORD_ID)+"'"
		Role_Records = Sql.GetFirst(Role_Recordse)						
		if Role_Records is not None and str(Role_Records)!='':
			Role_name = Role_Records.ROLE_NAME
			Role_RecId = Role_Records.ROLE_RECORD_ID
			tableRelInfo = Sql.GetTable(Object_Name)
			tableRelInfo.AddRow(Role_Records)
			Sql.Delete(tableRelInfo)
			
	return 0;
Object_Name = Param.Object_Name
MODE = Param.ACTION

if Object_Name == 'SYROMA':
	ROLE_RECORD_ID = Param.Primary_Data
	Product.SetGlobal('ROLE_RECORD_ID', str(ROLE_RECORD_ID))
	ApiResponse = ApiResponseFactory.JsonResponse(Role_container_Delete(ROLE_RECORD_ID,Object_Name,MODE))

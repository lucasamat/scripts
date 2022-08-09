# =========================================================================================================================================
#   __script_name : SYALRELADL.PY
#   __script_description : THIS SCRIPT IS USED TO DELETE THE DATA IN ANY RELATED LIST VIA THE DELETE ACTION BUTTON.
#   __primary_author__ : LEO JOSEPH
#   __create_date :
#   Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import SYTABACTIN as Table
from SYDATABASE import SQL
import Webcom.Configurator.Scripting.Test.TestProduct
Sql = SQL()
# LABLE = Param.LABLE
import SYCNGEGUID as CPQID
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
TestProduct = Webcom.Configurator.Scripting.Test.TestProduct()


def nativeProfileUserDelete(SYSTEM_ID, valID):
	LOGIN_CREDENTIALS = SqlHelper.GetFirst("SELECT Username,Password,Domain,URL FROM SYCONF (nolock)")
	if LOGIN_CREDENTIALS is not None:
		Login_Username = str(LOGIN_CREDENTIALS.Username)
		Login_Password = str(LOGIN_CREDENTIALS.Password)
		Login_Domain = str(LOGIN_CREDENTIALS.Domain)
		URL = str(LOGIN_CREDENTIALS.URL)

	sandboxBaseURL = URL
	authenticationUrl = (
		sandboxBaseURL
		+ "/api/rd/v1/Core/Login?username="
		+ Login_Username
		+ "&password="
		+ Login_Password
		+ "&domain="
		+ Login_Domain
	)
	authRequest = WebRequest.Create(str(authenticationUrl))
	authRequest.Method = "POST"
	authRequest.CookieContainer = CookieContainer()
	authRequest.ContentLength = 0
	authResponse = authRequest.GetResponse()
	cookies = authResponse.Cookies
	authResponseData = StreamReader(authResponse.GetResponseStream()).ReadToEnd()
	xcrf = str(authResponseData).replace('"', "")
	

	# cookies
	coookies = ""
	if cookies is not None:
		for cookie in cookies:
			coookies = coookies + str(cookie) + ";"


	data = "grant_type=password&username=" + Login_Username + "&password=" + Login_Password + "&domain=" + Login_Domain + ""

	authenticationapitokenUrl = "https://sandbox.webcomcpq.com/basic/api/token"
	authRequesttoken = WebRequest.Create(str(authenticationapitokenUrl))
	authRequesttoken.Method = "DELETE"
	webclienttoken = System.Net.WebClient()
	webclienttoken.Headers[System.Net.HttpRequestHeader.Host] = "sandbox.webcomcpq.com"
	webclienttoken.Headers[System.Net.HttpRequestHeader.ContentType] = "application/json; charset=utf-8"
	webclienttoken.Headers[System.Net.HttpRequestHeader.Cookie] = coookies
	webclienttoken.Headers.Add("X-CSRF-Token", xcrf)
	response = webclienttoken.UploadString(str(authenticationapitokenUrl), data)
	accessToken = "Bearer " + str(response).split(":")[1].split(",")[0].replace('"', "")

	datasave = '["%s"]' % (SYSTEM_ID)
	#Trace.Write("188-------------datasave----" + str(datasave))
	setPermissionURL = sandboxBaseURL + "/setup/api/v1/admin/users/" + str(valID) + "/permissionGroup"
	#Trace.Write("188-----------setPermissionURL---" + str(setPermissionURL))
	webclient = System.Net.WebClient()
	webclient.Headers[System.Net.HttpRequestHeader.Host] = "sandbox.webcomcpq.com"
	webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/json; charset=utf-8"
	webclient.Headers[System.Net.HttpRequestHeader.Cookie] = coookies
	webclient.Headers.Add("X-CSRF-Token", xcrf)
	webclient.Headers.Add("Authorization", accessToken)
	response = webclient.UploadString(str(setPermissionURL), "DELETE", datasave)
	
	return "response"


def deleterows(VALUE, ID, OPERATION):
	ID = ID.split("_")
	CustomerRestricted = ""
	table = ID[2] + "-" + ID[3] + "-" + ID[4] + "-" + ID[5] + "-" + ID[6]
	# lable=LABLE.split(',')[1]
	value = VALUE.split(",")[1]
	prfnameVal = ""
	#Trace.Write("sssssssssssssssss" + str(table))
	# A043S001P01-12265 Start
	try:
		prfnameVal = VALUE.split(",")[3]
	except Exception:
		pass
	# A043S001P01-12265 End
	usersval = VALUE.split(",")[1]
	Trace.Write("usersval---------" + str(usersval))
	valID = usersval.split("-")[1]
	Trace.Write("valuevaluevaluevaluevalue" + str(value))
	CurrentTab = TestProduct.CurrentTab
	Trace.Write("CurrentTab" + str(CurrentTab))
	DELETEROWID = ""
	if queryuserId:
		DELETEROWID = queryuserId.Id
	nativeProfileUserDelete(SYSTEM_ID, valID)
	Trace.Write("DELETEROWID----" + str(DELETEROWID))

	SQL_OBJ = Sql.GetFirst(
		"select API_NAME,OBJECT_NAME from SYOBJD where PARENT_OBJECT_RECORD_ID ='"
		+ str(table)
		+ "' and DATA_TYPE ='AUTO NUMBER'"
	)
	Trace.Write(
		"I GOT THE LIST"
		+ "select API_NAME,OBJECT_NAME from SYOBJD where PARENT_OBJECT_RECORD_ID ='"
		+ str(table)
		+ "' and DATA_TYPE ='AUTO NUMBER'"
	)
	data = value1 = data2 = ""
	if SQL_OBJ is not None:
		data = str(SQL_OBJ.OBJECT_NAME).strip()

		value1 = str(value).strip().replace(" ", " ")
		data2 = str(SQL_OBJ.API_NAME).strip()
		GetQuery = Sql.GetList(
			"SELECT " + str(data2) + " FROM " + str(data) + " WHERE " + str(data2) + "='" + str(value1) + "'"
		)
		Trace.Write(
			"Single Delete ============>  "
			+ "SELECT "
			+ str(data2)
			+ " FROM "
			+ str(data)
			+ " WHERE "
			+ str(data2)
			+ "='"
			+ str(value1)
			+ "'"
		)
		Trace.Write("Single Delete ============> 1111111 " + str(data))
		Trace.Write("Single Delete ============> 222222 " + str(data2))
		Trace.Write("Single Delete ============> 33333333 " + str(value1))
		if GetQuery is not None:
			Table.TableActions.Delete(str(data), str(data2), str(value1))
			Log.Info(Table.TableActions.Delete(str(data), str(data2), str(value1)))
			Log.Info("Table Deleted")




VALUE = Param.VALUE
ID = Param.ID
Trace.Write("511--------------" + str(VALUE))
Trace.Write("GOT  ID" + str(ID))

OPERATION = Param.OPERATION
ApiResponse = ApiResponseFactory.JsonResponse(deleterows(VALUE, ID, OPERATION))
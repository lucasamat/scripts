"""This script is used to add user from users table CPQ Native Profiles Table."""
# ====================================================================================================
#   __script_name : SGUSERSAVE.PY
#   __script_description : This script is used to add user from users table CPQ Native Profiles Table
#   __primary_author__ : JOE EBENEZER
#   __create_date : 31/08/2020
#   Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ====================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct
import datetime
import clr
import System.Net
from System.Text.Encoding import UTF8
from System import Convert
from System.Net import *
from SYDATABASE import SQL

clr.AddReference("System.Net")
today = datetime.datetime.now()
Modified_date = today.strftime("%m/%d/%Y %H:%M:%S %p")
Sql = SQL()


def nativeProfileUserUpdate(permissionid, currentprofilename, permission_description, SYSTEM_ID, SELECTROW):

    LOGIN_CREDENTIALS = Sql.GetFirst("SELECT USER_NAME,Password,Domain FROM SYCONF (nolock) where USER_NAME = 'X0125427'")
    if LOGIN_CREDENTIALS is not None:
        Login_Username = str(LOGIN_CREDENTIALS.USER_NAME)
        Login_Password = str(LOGIN_CREDENTIALS.Password)
        Login_Domain = str(LOGIN_CREDENTIALS.Domain)

    sandboxBaseURL = "https://sandbox.webcomcpq.com"
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
    authRequesttoken.Method = "POST"
    webclienttoken = System.Net.WebClient()
    webclienttoken.Headers[System.Net.HttpRequestHeader.Host] = "sandbox.webcomcpq.com"
    webclienttoken.Headers[System.Net.HttpRequestHeader.ContentType] = "application/json; charset=utf-8"
    webclienttoken.Headers[System.Net.HttpRequestHeader.Cookie] = coookies
    webclienttoken.Headers.Add("X-CSRF-Token", xcrf)
    response = webclienttoken.UploadString(str(authenticationapitokenUrl), data)
    accessToken = "Bearer " + str(response).split(":")[1].split(",")[0].replace('"', "")

    SELECTROWId = ""
    for val in SELECTROW:
        datasave = '["%s"]' % (SYSTEM_ID)
        #Trace.Write("188-------------datasave----" + str(datasave))
        setPermissionURL = sandboxBaseURL + "/setup/api/v1/admin/users/" + str(val) + "/permissionGroup"
        #Trace.Write("188-----------setPermissionURL---" + str(setPermissionURL))
        webclient = System.Net.WebClient()
        webclient.Headers[System.Net.HttpRequestHeader.Host] = "sandbox.webcomcpq.com"
        webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/json; charset=utf-8"
        webclient.Headers[System.Net.HttpRequestHeader.Cookie] = coookies
        webclient.Headers.Add("X-CSRF-Token", xcrf)
        webclient.Headers.Add("Authorization", accessToken)
        response = webclient.UploadString(str(setPermissionURL), datasave)
        Trace.Write("PERMISSIONS : " + str(response.encode("ascii", "ignore")))
    return "response"


def assigneduser(CURRREC, SELECTROW, Primary_Data, currentprofilename):
    datas = ""

    today = datetime.datetime.now()
    Modified_date = today.strftime("%m/%d/%Y %H:%M:%S %p")
    PF_REC_ID = Product.GetGlobal("PF_REC_ID")
    proff_id = Product.GetGlobal("Profile_ID")

    RecAttValue = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00128").GetValue()

    permissionid = SYSTEM_ID = permission_description = ""
    cpqNativepermission = Sql.GetFirst(
        "Select permission_id,permission_description,SYSTEM_ID from cpq_permissions where SYSTEM_ID ='"
        + str(RecAttValue)
        + "'"
    )
    if cpqNativepermission:
        permissionid = cpqNativepermission.permission_id
        permission_description = cpqNativepermission.permission_description
        SYSTEM_ID = cpqNativepermission.SYSTEM_ID
    #Trace.Write("permissionid--108----------" + str(permissionid))
    nativeProfileUserUpdate(permissionid, currentprofilename, permission_description, SYSTEM_ID, SELECTROW)


    return datas


if hasattr(Param, "Primary_Data"):
    Primary_Data = Param.Primary_Data


'''def nativeProfileUserUpdate(permissionid, currentprofilename, permission_description, SYSTEM_ID, SELECTROW):
    """Update the Profile User Assignment using CPQ Native User Profiles."""
    LOGIN_CREDENTIALS = SqlHelper.GetFirst("SELECT Username,Password,Domain FROM SYCONF (nolock)")
    if LOGIN_CREDENTIALS is not None:
        Login_Username = str(LOGIN_CREDENTIALS.Username)
        Login_Password = str(LOGIN_CREDENTIALS.Password)
        Login_Domain = str(LOGIN_CREDENTIALS.Domain)

    sandboxBaseURL = "https://sandbox.webcomcpq.com"
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
    coookies = ""
    if cookies is not None:
        for cookie in cookies:
            coookies = coookies + str(cookie) + ";"

    data = "grant_type=password&username=" + Login_Username + "&password=" + Login_Password + "&domain=" + Login_Domain + ""
    authenticationapitokenUrl = "https://sandbox.webcomcpq.com/basic/api/token"
    authRequesttoken = WebRequest.Create(str(authenticationapitokenUrl))
    authRequesttoken.Method = "POST"
    webclienttoken = System.Net.WebClient()
    webclienttoken.Headers[System.Net.HttpRequestHeader.Host] = "sandbox.webcomcpq.com"
    webclienttoken.Headers[System.Net.HttpRequestHeader.ContentType] = "application/json; charset=utf-8"
    webclienttoken.Headers[System.Net.HttpRequestHeader.Cookie] = coookies
    webclienttoken.Headers.Add("X-CSRF-Token", xcrf)
    response = webclienttoken.UploadString(str(authenticationapitokenUrl), data)
    accessToken = "Bearer " + str(response).split(":")[1].split(",")[0].replace('"', "")
    SELECTROWId = ""
    for val in SELECTROW:
        datasave = '["%s"]' % (SYSTEM_ID)
        setPermissionURL = sandboxBaseURL + "/setup/api/v1/admin/users/" + str(val) + "/permissionGroup"
        webclient = System.Net.WebClient()
        webclient.Headers[System.Net.HttpRequestHeader.Host] = "sandbox.webcomcpq.com"
        webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/json; charset=utf-8"
        webclient.Headers[System.Net.HttpRequestHeader.Cookie] = coookies
        webclient.Headers.Add("X-CSRF-Token", xcrf)
        webclient.Headers.Add("Authorization", accessToken)
        response = webclient.UploadString(str(setPermissionURL), datasave)
        Trace.Write("PERMISSIONS : " + str(response.encode("ascii", "ignore")))
    return "response"'''


'''def assigneduser(CURRREC, SELECTROW, Primary_Data, currentprofilename):
    """Get the Selected User assigned to the Current Profile."""
    datas = ""
    today = datetime.datetime.now()
    Modified_date = today.strftime("%m/%d/%Y %H:%M:%S %p")
    PF_REC_ID = Product.GetGlobal("PF_REC_ID")
    proff_id = Product.GetGlobal("Profile_ID")
    Trace.Write("proff_id : " + str(proff_id))
    Trace.Write("PF_REC_ID : " + str(PF_REC_ID))

    RecAttValue = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00128").GetValue()
    Trace.Write("RecAttValue---220--------" + str(RecAttValue))
    permissionid = SYSTEM_ID = permission_description = ""
    cpqNativepermission = Sql.GetFirst(
        "Select permission_id,permission_description,SYSTEM_ID from cpq_permissions where SYSTEM_ID ='"
        + str(RecAttValue)
        + "'"
    )
    if cpqNativepermission:
        permissionid = cpqNativepermission.permission_id
        permission_description = cpqNativepermission.permission_description
        SYSTEM_ID = cpqNativepermission.SYSTEM_ID
    Trace.Write("permissionid---" + str(permissionid))
    nativeProfileUserUpdate(permissionid, currentprofilename, permission_description, SYSTEM_ID, SELECTROW)
    return datas'''


if hasattr(Param, "Primary_Data"):
    Primary_Data = Param.Primary_Data
else:
    Primary_Data = ""

SELECTROW = list(Param.SELECTROW)

if hasattr(Param, "currentprofilename"):
    currentprofilename = Param.currentprofilename
else:
    currentprofilename = ""

if hasattr(Param, "CURRREC"):
    CURRREC = Param.CURRREC
else:
    CURRREC = ""

ApiResponse = ApiResponseFactory.JsonResponse(assigneduser(CURRREC, SELECTROW, Primary_Data, currentprofilename))
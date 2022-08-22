# =========================================================================================================================================
#   __script_name : SYAPROFILES.PY
#   __script_description : THIS SCRIPT IS USED FOR THE PROFILE SAVE FUNCTIONALITY AND ITS CALLING FROM SYATABSAVE SCRIPT.
#   __primary_author__ :AYYAPPAN SUBRAMANIYAN
#   __create_date :
#   Ãƒâ€šÃ‚Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================


import Webcom.Configurator.Scripting.Test.TestProduct
import System.Net
from System.Net import *
from System import Convert
from System.Net import CookieContainer, NetworkCredential, Mail
from System.Net.Mail import SmtpClient, MailAddress, Attachment, MailMessage
from System.Net import WebRequest
from System.Net import HttpWebResponse
import SYTABACTIN as Table
import datetime
import re
from SYDATABASE import SQL

Sql = SQL()   

try:
    row = Param.row
except:
    row = ""
try:
    nativeProfileUpdate = Param.nativeProfileUpdate
except:
    nativeProfileUpdate = ""    
try:
    nativeProfileSave = Param.nativeProfileSave
except:
    nativeProfileSave = ""
Trace.Write("row "+str(row)+"nativeProfileUpdate"+str(nativeProfileUpdate)+"nativeProfileSave"+str(nativeProfileSave))
if nativeProfileUpdate == "Yes":
    LOGIN_CREDENTIALS = SqlHelper.GetFirst("SELECT USER_NAME, PASSWORD, DOMAIN, URL FROM SYCONF (nolock) WHERE USER_NAME = 'X0125427'")
    if LOGIN_CREDENTIALS is not None:
        Login_Username = str(LOGIN_CREDENTIALS.USER_NAME)
        Login_Password = str(LOGIN_CREDENTIALS.PASSWORD)
        Login_Domain = str(LOGIN_CREDENTIALS.DOMAIN)
        sandboxBaseURL = str(LOGIN_CREDENTIALS.URL)
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
        # authentication api token creation start
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

        # setPermissionURL = sandboxBaseURL + '/setup/api/v1/admin/permissionGroups'
        
        prf_ID = ""            
        prfid = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00128").GetValue()
        prfname = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00129").GetValue()
        prfdesc = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00130_LONG").GetValue()
        profile_id_gen = prfid
        permissionQuery = Sql.GetFirst(
            "Select permission_id from cpq_permissions where permission_name ='" + str(prfname) + "'"
        )
        if permissionQuery:
            prf_ID = permissionQuery.permission_id    
        
        prf_ID = newdict.get("permission_id")    
        # setPermissionURL = sandboxBaseURL + '/setup/api/v1/admin/permissionGroups/'+ str(int(prf_ID))
        
        datasave = """{
            "Id":%s,
            "Name": "%s",
            "Description": "%s",
            "SystemId": "%s",
            "Condition": "%s",
            "SelectedPermissions": {
            "ManualPermissions": [],
            "CompanyPermissions": [],
            "MarketPermissions": [],
            "MultiBrandingPermissions": [],
            "UserTypePermissions": [],
            "Users": [136]
            }        
            
        }""" % (
            prf_ID,
            prfname,
            prfdesc,
            prfid,
            prfdesc,
        )    
        setPermissionURL = sandboxBaseURL + "/setup/api/v1/admin/permissionGroups"    
        webclient = System.Net.WebClient()
        webclient.Headers[System.Net.HttpRequestHeader.Host] = "sandbox.webcomcpq.com"
        webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/json; charset=utf-8"
        webclient.Headers[System.Net.HttpRequestHeader.Cookie] = coookies
        webclient.Headers.Add("X-CSRF-Token", xcrf)
        webclient.Headers.Add("Authorization", accessToken)    
        response = webclient.UploadString(str(setPermissionURL), datasave)
        Trace.Write("PERMISSIONS : " + str(response.encode("ascii", "ignore")))
    
elif  nativeProfileSave == "Yes":
    LOGIN_CREDENTIALS = SqlHelper.GetFirst("SELECT USER_NAME, PASSWORD, DOMAIN, URL FROM SYCONF (nolock) WHERE USER_NAME = 'X0125427'")
    if LOGIN_CREDENTIALS is not None:
        Login_Username = str(LOGIN_CREDENTIALS.USER_NAME)
        Login_Password = str(LOGIN_CREDENTIALS.PASSWORD)
        Login_Domain = str(LOGIN_CREDENTIALS.DOMAIN)
        sandboxBaseURL = str(LOGIN_CREDENTIALS.URL)
    
        authenticationUrl = (
            sandboxBaseURL
            + "/api/rd/v1/Core/Login?username="
            + Login_Username
            + "&password="
            + Login_Password
            + "&domain="
            + Login_Domain
        )        
        prfid = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00128").GetValue()
        prfname = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00129").GetValue()
        prfdesc = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00130_LONG").GetValue()
        profile_id_gen = prfid
        Product.SetGlobal("SYSTEM_ID_PRF", str(profile_id_gen))        
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
        # authentication api token creation start
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
        setPermissionURL = sandboxBaseURL + "/setup/api/v1/admin/permissionGroups"    
        
        datasave = """{
            
            "Name": "%s",
            "Description": "%s",
            "SystemId": "%s",
            "Condition": "%s",
            "SelectedPermissions": {
            "ManualPermissions": [],
            "CompanyPermissions": [],
            "MarketPermissions": [],
            "MultiBrandingPermissions": [],
            "UserTypePermissions": [],
            "Users": [136]
            }
            
            
        }""" % (
            prfname,
            prfdesc,
            profile_id_gen,
            prfid,
        )    
        setPermissionURL = sandboxBaseURL + "/setup/api/v1/admin/permissionGroups"    
        webclient = System.Net.WebClient()
        webclient.Headers[System.Net.HttpRequestHeader.Host] = "sandbox.webcomcpq.com"
        webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/json; charset=utf-8"
        webclient.Headers[System.Net.HttpRequestHeader.Cookie] = coookies
        webclient.Headers.Add("X-CSRF-Token", xcrf)
        webclient.Headers.Add("Authorization", accessToken)
        response = webclient.UploadString(str(setPermissionURL), datasave)
        Trace.Write("PERMISSIONS : " + str(response.encode("ascii", "ignore")))
        Product.SetGlobal("Profile_ID_val", str(response.encode("ascii", "ignore")))
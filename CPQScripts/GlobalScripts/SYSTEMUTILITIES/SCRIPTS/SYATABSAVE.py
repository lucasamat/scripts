""" 
SCRIPT NAME : SYATABSAVE
CREATE BY   : JOE EBENEZER
CREATE DATE :
DESCRIPTION : To save the details of all the tabs in all modules


------------------------------------------------------------------------------------------------
"""
###save functionality
import Webcom.Configurator.Scripting.Test.TestProduct
TestProduct = Webcom.Configurator.Scripting.Test.TestProduct()

import System.Net


import clr

clr.AddReference("System.Net")
from System.Net import *
from System.Text.Encoding import UTF8
from System import Convert


import SYTABACTIN as Table
import datetime
import re
import SYCNGEGUID as CPQID


import datetime
from datetime import timedelta
from SYDATABASE import SQL

Sql = SQL()

UserId = str(User.Id)
UserName = str(User.Name)
#now = datetime.now()
#datetime_value = now.strftime("%m/%d/%Y %H:%M:%S")
#Trace = Trace  # pylint: disable=E0602
#SqlHelper = SqlHelper  # pylint: disable=E0602
#WebRequest = WebRequest  # pylint: disable=E0602
#CookieContainer = CookieContainer  # pylint: disable=E0602
#StreamReader = StreamReader  # pylint: disable=E0602
# create Profiles 9517 start
def nativeProfileSave(newdict):
    Login_Username = 'X0116955'
    #Login_Password = 'Joseph@2020'
    Login_Password = 'Welcome@123'
    Login_Domain = 'appliedmaterials_tst'
    #LOGIN_CREDENTIALS = SqlHelper.GetFirst("SELECT Username,Password,Domain,URL FROM SYCONF (nolock)")
    #if LOGIN_CREDENTIALS is not None:
        #Login_Username = str(LOGIN_CREDENTIALS.Username)
        #Login_Password = str(LOGIN_CREDENTIALS.Password)
        #Login_Domain = str(LOGIN_CREDENTIALS.Domain)
    URL = 'https://sandbox.webcomcpq.com'
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
    prfname = profile_id_gen = prfid = ""
    prfid = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00128").GetValue()
    prfname = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00129").GetValue()
    prfdesc = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00130_LONG").GetValue()
    profile_id_gen = prfid
    Product.SetGlobal("SYSTEM_ID_PRF", str(profile_id_gen))
    PROFILE_NAME = prfname
    #Trace.Write('url check----authenticationUrl-76-------------'+str(authenticationUrl))
    authRequest = WebRequest.Create(str(authenticationUrl))
    authRequest.Method = "POST"
    authRequest.CookieContainer = CookieContainer()
    authRequest.ContentLength = 0
    authResponse = authRequest.GetResponse()
    cookies = authResponse.Cookies
    authResponseData = StreamReader(authResponse.GetResponseStream()).ReadToEnd()
    xcrf = str(authResponseData).replace('"', "")
    #Trace.Write("X-CSRF-Token 85--: " + str(xcrf))

    # cookies
    coookies = ""
    if cookies is not None:
        for cookie in cookies:
            coookies = coookies + str(cookie) + ";"
    #Trace.Write("COOKIES : " + coookies)

    data = "grant_type=password&username=" + Login_Username + "&password=" + Login_Password + "&domain=" + Login_Domain + ""
    #Trace.Write("53--data-----" + str(data))
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
    #Trace.Write("68---data----" + str(datasave))
    setPermissionURL = sandboxBaseURL + "/setup/api/v1/admin/permissionGroups"
    #Trace.Write("68---data--setPermissionURL----" + str(setPermissionURL))
    webclient = System.Net.WebClient()
    webclient.Headers[System.Net.HttpRequestHeader.Host] = "sandbox.webcomcpq.com"
    webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/json; charset=utf-8"
    webclient.Headers[System.Net.HttpRequestHeader.Cookie] = coookies
    webclient.Headers.Add("X-CSRF-Token", xcrf)
    webclient.Headers.Add("Authorization", accessToken)
    response = webclient.UploadString(str(setPermissionURL), datasave)
    Trace.Write("PERMISSIONS : " + str(response.encode("ascii", "ignore")))
    Product.SetGlobal("Profile_ID_val", str(response.encode("ascii", "ignore")))
    return "response"


# create Profiles-Native tables-- 9517 End
def nativeProfileUpdate(newdict):
    Login_Username = 'X0116955'
    #Login_Password = 'Joseph@2020'
    Login_Password = 'Welcome@123'
    Login_Domain = 'appliedmaterials_tst'
    
    URL = 'https://sandbox.webcomcpq.com'
    '''LOGIN_CREDENTIALS = SqlHelper.GetFirst("SELECT Username,Password,Domain,URL FROM SYCONF (nolock)")
    if LOGIN_CREDENTIALS is not None:
        Login_Username = str(LOGIN_CREDENTIALS.Username)
        Login_Password = str(LOGIN_CREDENTIALS.Password)
        Login_Domain = str(LOGIN_CREDENTIALS.Domain)
        URL = str(LOGIN_CREDENTIALS.URL)'''

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
    #Trace.Write('url check----authenticationUrl--'+str(authenticationUrl))
    authRequest = WebRequest.Create(str(authenticationUrl))
    authRequest.Method = "POST"
    authRequest.CookieContainer = CookieContainer()
    authRequest.ContentLength = 0
    authResponse = authRequest.GetResponse()
    cookies = authResponse.Cookies
    authResponseData = StreamReader(authResponse.GetResponseStream()).ReadToEnd()
    xcrf = str(authResponseData).replace('"', "")
    #Trace.Write("X-CSRF-Token : " + str(xcrf))
    
    # cookies
    coookies = ""
    if cookies is not None:
        for cookie in cookies:
            coookies = coookies + str(cookie) + ";"
    #Trace.Write("COOKIES : " + coookies)

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

    profile_id_gen = newdict.get("PROFILE_ID")
    #Trace.Write("159----------" + str(profile_id_gen))
    PROFILE_NAME = newdict.get("PROFILE_NAME")
    prf_ID = ""
    prfname = profile_id_gen = prfid = ""
    #Trace.Write('64----nativeProfileSave-------'+str(newdict))
    prfid = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00128").GetValue()
    prfname = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00129").GetValue()
    prfdesc = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00130_LONG").GetValue()
    profile_id_gen = prfid
    permissionQuery = Sql.GetFirst(
        "Select permission_id from cpq_permissions where permission_name ='" + str(prfname) + "'"
    )
    if permissionQuery:
        prf_ID = permissionQuery.permission_id
    
    # Trace.Write("52----PROFILE_NAME--------" + str(PROFILE_NAME))
    # Trace.Write("52--newdict-------" + str(newdict))
    prf_ID = newdict.get("permission_id")
    #Trace.Write("52----prf_ID--------" + str(prf_ID))
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
    #Trace.Write("188-------------datasave----" + str(datasave))
    setPermissionURL = sandboxBaseURL + "/setup/api/v1/admin/permissionGroups"
    #Trace.Write("261----setPermissionURL----" + str(setPermissionURL))
    webclient = System.Net.WebClient()
    webclient.Headers[System.Net.HttpRequestHeader.Host] = "sandbox.webcomcpq.com"
    webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/json; charset=utf-8"
    webclient.Headers[System.Net.HttpRequestHeader.Cookie] = coookies
    webclient.Headers.Add("X-CSRF-Token", xcrf)
    webclient.Headers.Add("Authorization", accessToken)
    #Trace.Write("261----setPermissionURL---272-" + str(setPermissionURL))
    response = webclient.UploadString(str(setPermissionURL), datasave)
    Trace.Write("PERMISSIONS : " + str(response.encode("ascii", "ignore")))
    return "response"


# update profiles 9517 End
# A043S001P01-11419-Profie Explorer-Dhurga-End
####variable declaration
MM_MOD_ATTR_NAME = (
    MM_MOD_CUS_OBJ
) = (
    TABLE_NAME
) = (
    ATTR_Value
) = (
    Rec_Id_Value
) = (
    REC_NO
) = (
    API_Value
) = (
    RESULT
) = Tree = API_NAME = str1 = RecId = Selected_List = CurrentTime = AutoFieldId = Model_Type_letter = Price_Model_ID = ""
Field_Labels = []
row = {}
"""MM_MOD_CUS_OBJ = ""
TABLE_NAME = ""
ATTR_Value = ""
Rec_Id_Value = ""
REC_NO = ""
API_Value = ""
RESULT = ""
Tree = ""
API_NAME = ""
str1 = ""
RecId = ""
Selected_List = CurrentTime = AutoFieldId = Model_Type_letter =Price_Model_ID = "" """
Product_name = Product.Name
flag = "True"
for tab in Product.Tabs:
    tab_name = tab.Name
    #Trace.Write("INSIDE_FOR" + str(tab_name))
    if tab.IsSelected == True:
        CurrentTabName = (tab.Name).strip()
        Product_Type_letter = ""

        sql_obj = Sql.GetFirst(
            "select RECORD_ID,TAB_LABEL from SYTABS (nolock) where SAPCPQ_ALTTAB_NAME = '"
            + str(CurrentTabName)
            + "' and RTRIM(LTRIM(APP_LABEL))='"
            + str(Product_name)
            + "'"
        )
        if sql_obj is not None:
            str1 = sql_obj.TAB_LABEL            
            SYSECT_OBJNAME = Sql.GetList(
                    "select SYSECT.RECORD_ID,SYSECT.PRIMARY_OBJECT_NAME FROM SYSECT (nolock) INNER JOIN SYPAGE ON SYSECT.PAGE_RECORD_ID = SYPAGE.RECORD_ID where SYPAGE.TAB_RECORD_ID ='"
                    + str(sql_obj.RECORD_ID).strip()
                    + "' "
            )            
            #Trace.Write("str1------->" + str(str1.upper()))
            if SYSECT_OBJNAME is not None:
                ##TO GET THE SECTION INFORMATION
                for secobj in SYSECT_OBJNAME:
                    TABLE_NAME = str(secobj.PRIMARY_OBJECT_NAME).strip()
                    REC_ID_OBJ = Sql.GetFirst(
                        "Select RECORD_ID,RECORD_NAME from SYOBJH (nolock) where RTRIM(LTRIM(OBJECT_NAME))='"
                        + str(TABLE_NAME).strip()
                        + "'"
                    )
                    if REC_ID_OBJ is not None:
                        SYOBJH_OBJ = REC_ID_OBJ.RECORD_ID
                        QUE_OBJ = Sql.GetFirst(
                            "Select RECORD_ID,SAPCPQ_ATTRIBUTE_NAME from SYSEFL (nolock) where API_FIELD_NAME='"
                            + str(REC_ID_OBJ.RECORD_NAME).strip()
                            + "' and API_NAME='"
                            + str(TABLE_NAME).strip()
                            + "' and SECTION_RECORD_ID='"
                            + str(secobj.RECORD_ID)
                            + "' "
                        )
                        ###TO GET THE QUESTION INFORMATION
                        if QUE_OBJ is not None:
                            RECORDID = str(QUE_OBJ.SAPCPQ_ATTRIBUTE_NAME).replace("-", "_").replace(" ", "")
                            ATTRIBUTENAME = (RECORDID).upper()
                            RECORD_ID = "QSTN_" + str(ATTRIBUTENAME).strip()
                            RecId = str(REC_ID_OBJ.RECORD_NAME).strip()
                            Trace.Write("str(RecId)" + str(RecId))

                            ####ACTION OF TABS
                            curr = Product.Attributes.GetByName("MA_MTR_TAB_ACTION").GetValue()

                            #####CLONE SAVE ACTION
                            if curr == "CLONE":
                                Product.SetGlobal("clone", "yes")
                                clone_id = Product.GetGlobal("clone_id")
                                SYOBJD_OBJNAME = Sql.GetList(
                                    "SELECT OBJECT_NAME,API_NAME, DATA_TYPE,FORMULA_LOGIC,LOOKUP_API_NAME FROM  SYOBJD where RTRIM(LTRIM(OBJECT_NAME))  ='"
                                    + str(TABLE_NAME).strip()
                                    + "' and PARENT_OBJECT_RECORD_ID='"
                                    + str(SYOBJH_OBJ)
                                    + "'"
                                )

                                if SYOBJD_OBJNAME is not None:
                                    for SYOBJD_Details in SYOBJD_OBJNAME:
                                        # A043S001P01-7458 - Segment Clone - STP Account Editable - Start                                        
                                        SECT_OBJNAME = Sql.GetList(
                                                "select RECORD_ID FROM SYSECT (nolock) where RTRIM(LTRIM(TAB_NAME)) ='"
                                                + str(str1)
                                                + "' and TAB_RECORD_ID ='"
                                                + str(sql_obj.RECORD_ID).strip()
                                                + "'"
                                        )
                                        
                                        # A043S001P01-7458 - Segment Clone - STP Account Editable - End

                                        if SECT_OBJNAME is not None:
                                            for SECT in SECT_OBJNAME:
                                                SYSEFL_OBJNAME = Sql.GetFirst(
                                                    "SELECT RECORD_ID,FIELD_LABEL,SAPCPQ_ATTRIBUTE_NAME, API_NAME,API_NAME,SECTION_NAME,FLDDEF_VARIABLE_RECORD_ID,FLDDEF_VARIABLE_NAME FROM SYSEFL (nolock) where API_NAME ='"
                                                    + str(SYOBJD_Details.OBJECT_NAME).strip()
                                                    + "' and API_FIELD_NAME='"
                                                    + str(SYOBJD_Details.API_NAME).strip()
                                                    + "' and SECTION_RECORD_ID='"
                                                    + str(SECT.RECORD_ID)
                                                    + "'"
                                                )

                                                if SYSEFL_OBJNAME is not None and str(SYSEFL_OBJNAME.API_NAME) != "":
                                                    MM_MOD_CUS_OBJ = (SYSEFL_OBJNAME.API_NAME).strip()
                                                    SECTIONQSTNRECORDID = (
                                                        str(SYSEFL_OBJNAME.SAPCPQ_ATTRIBUTE_NAME)
                                                        .replace("-", "_")
                                                        .replace(" ", "")
                                                    )
                                                    SECQSTNATTRIBUTENAME = SECTIONQSTNRECORDID.upper()
                                                    MM_MOD_ATTR_NAME = "QSTN_" + str(SECQSTNATTRIBUTENAME)
                                                    Trace.Write(
                                                        "MM_MOD_ATTR_NAME____MM_MOD_ATTR_NAME___MM_MOD_ATTR_NAME"
                                                        + str(MM_MOD_ATTR_NAME)
                                                    )
                                                    ###AUTONUMBER DATATYPE QUESTION
                                                    if SYOBJD_Details.DATA_TYPE == "AUTO NUMBER":
                                                        REC_NO = str(Guid.NewGuid()).upper()
                                                        row[RecId] = str(REC_NO)
                                                        Trace.Write("row_row____row" + str(row))
                                                    ###LOOKUP DATATYPE QUESTION
                                                    elif (
                                                        SYOBJD_Details.DATA_TYPE != "LOOKUP"
                                                        and SYOBJD_Details.DATA_TYPE != "FORMULA"
                                                    ):
                                                        if (
                                                            Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)) is not None
                                                            and str(SYSEFL_OBJNAME.FLDDEF_VARIABLE_RECORD_ID) == ""
                                                        ):
                                                            ATTR_Value = (
                                                                Product.Attributes.GetByName(
                                                                    str(MM_MOD_ATTR_NAME)
                                                                ).GetValue()
                                                                or ""
                                                            )
                                                            if str(MM_MOD_CUS_OBJ) == "SETBAR_1PC":
                                                                if (str(ATTR_Value)).upper() == "TRUE" or str(
                                                                    ATTR_Value
                                                                ) == "1":
                                                                    row[MM_MOD_CUS_OBJ] = "001"
                                                                else:
                                                                    row[MM_MOD_CUS_OBJ] = ""
                                                            else:
                                                                row[MM_MOD_CUS_OBJ] = str(ATTR_Value)
                                                        elif (
                                                            Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)) is not None
                                                            and str(SYSEFL_OBJNAME.FLDDEF_VARIABLE_RECORD_ID) != ""
                                                        ):
                                                            FLDDEF_VARIABLE_RECORD_ID = (
                                                                SYSEFL_OBJNAME.FLDDEF_VARIABLE_RECORD_ID
                                                            )

                                                            CTX_Logic = Sql.GetFirst(
                                                                "select CPQ_CALCULATION_LOGIC from SYVABL (nolock) where RECORD_ID = '"
                                                                + str(FLDDEF_VARIABLE_RECORD_ID)
                                                                + "' "
                                                            )
                                                            result = ScriptExecutor.ExecuteGlobal(
                                                                "SYPARVRLLG",
                                                                {
                                                                    "CTXLogic": str(CTX_Logic.CPQ_CALCULATION_LOGIC),
                                                                    "Obj_Name": TABLE_NAME,
                                                                },
                                                            )
                                                            if result != "":
                                                                ATTR_Value = str(result)
                                                                row[MM_MOD_CUS_OBJ] = str(ATTR_Value)
                                                    ###FORMULA DATATYPE QUESTION
                                                    elif SYOBJD_Details.DATA_TYPE == "FORMULA":
                                                        if (
                                                            SYOBJD_Details.FORMULA_LOGIC != ""
                                                            and "select" in str(SYOBJD_Details.FORMULA_LOGIC).lower()
                                                        ):
                                                            SECTIONQSTNRECORDID = (
                                                                str(SYSEFL_OBJNAME.SAPCPQ_ATTRIBUTE_NAME)
                                                                .replace("-", "_")
                                                                .replace(" ", "")
                                                            )
                                                            SECQSTNATTRIBUTENAME = (SECTIONQSTNRECORDID).upper()
                                                            MM_MOD_ATTR_NAME = "QSTN_LKP_" + str(SECQSTNATTRIBUTENAME)
                                                            if (
                                                                Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME))
                                                                is not None
                                                            ):
                                                                API_Value = str(
                                                                    Product.Attributes.GetByName(
                                                                        str(MM_MOD_ATTR_NAME)
                                                                    ).HintFormula
                                                                )
                                                                API_obj = Sql.GetFirst(
                                                                    "select API_NAME from  SYOBJD (nolock) where LOOKUP_API_NAME ='"
                                                                    + str(MM_MOD_CUS_OBJ)
                                                                    + "' "
                                                                )
                                                                if API_obj is not None and API_Value != "":
                                                                    API_Name = str(API_obj.API_NAME).strip()
                                                                    row[API_Name] = str(API_Value)
                                                                    result = ScriptExecutor.ExecuteGlobal(
                                                                        "SYPARCEFMA",
                                                                        {
                                                                            "Object": TABLE_NAME,
                                                                            "API_Name": str(API_Name),
                                                                            "API_Value": API_Value,
                                                                        },
                                                                    )
                                                                    for API_Names in result:
                                                                        API_NAME = str(API_Names["API_NAME"]).strip()
                                                                        RESULT = str(API_Names["FORMULA_RESULT"])
                                                                        row[API_NAME] = str(RESULT)
                                                        elif (
                                                            SYOBJD_Details.FORMULA_LOGIC != ""
                                                            and "select" not in str(SYOBJD_Details.FORMULA_LOGIC).lower()
                                                        ):
                                                            ATTR_Value = str(SYOBJD_Details.FORMULA_LOGIC).strip()
                                                            row[MM_MOD_CUS_OBJ] = str(ATTR_Value)
                                                        elif SYOBJD_Details.FORMULA_LOGIC == "":
                                                            ATTR_Value = Product.Attributes.GetByName(
                                                                str(MM_MOD_ATTR_NAME)
                                                            ).GetValue()
                                                            row[MM_MOD_CUS_OBJ] = str(ATTR_Value)

                                    #Trace.Write("ROW-----" + str(dict(row)))
                                    
                                    Product.Attributes.GetByName(str(RECORD_ID)).AssignValue(str(REC_NO))
                                    Table.TableActions.Create(TABLE_NAME, row)
                                    try:                                        
                                        result = ScriptExecutor.ExecuteGlobal(
                                            "SYPARCEFMA",
                                            {"Object": TABLE_NAME, "API_Name": str(RecId), "API_Value": REC_NO},
                                        )
                                        new_value_dict = {
                                            API_Names["API_NAME"]: API_Names["FORMULA_RESULT"]
                                            for API_Names in result
                                            if API_Names["FORMULA_RESULT"] != ""
                                        }
                                        if new_value_dict is not None:
                                            row = {RecId: str(REC_NO)}
                                            row.update(new_value_dict)
                                            #Trace.Write("Updated 111")
                                            Table.TableActions.Update(TABLE_NAME, RecId, row)
                                    except:
                                        Trace.Write("NOT SELF REFERENCE RECORD")
                                    
                                    #####TO CREATE THE DATA IN THE CUSTOM TABLE
                                    OBJD_OBJ = Sql.GetList(
                                        "Select OBJECT_NAME from  SYOBJD (nolock) where LOOKUP_OBJECT='"
                                        + str(TABLE_NAME).strip()
                                        + "' "
                                    )
                                    if OBJD_OBJ is not None:
                                        for OBJD_Details in OBJD_OBJ:
                                            row = {}
                                            REL_TAB_NAME = str(OBJD_Details.OBJECT_NAME).strip()
                                            REL_OBJ = Sql.GetFirst(
                                                "Select RECORD_NAME from SYOBJH (nolock) where RTRIM(LTRIM(OBJECT_NAME))='"
                                                + str(TABLE_NAME).strip()
                                                + "'"
                                            )
                                            if REL_OBJ is not None:
                                                COL_NAME = str(REL_OBJ.RECORD_NAME).strip()
                                                SQLobj = Sql.GetList(
                                                        "Select * from "
                                                        + str(REL_TAB_NAME)
                                                        + " (nolock) where "
                                                        + str(COL_NAME)
                                                        + "= '"
                                                        + str(clone_id)
                                                        + "'"
                                                    )
                                                if SQLobj is not None:
                                                    for inc in SQLobj:
                                                        SYOBJD_OBJNAME = Sql.GetList(
                                                            "SELECT OBJECT_NAME,API_NAME, DATA_TYPE,FORMULA_LOGIC,LOOKUP_API_NAME FROM  SYOBJD (nolock) where RTRIM(LTRIM(OBJECT_NAME)) ='"
                                                            + str(REL_TAB_NAME).strip()
                                                            + "' "
                                                        )
                                                        if SYOBJD_OBJNAME is not None:
                                                            for SYOBJD_Details in SYOBJD_OBJNAME:
                                                                if str(SYOBJD_Details.API_NAME) != "":
                                                                    MM_MOD_CUS_OBJ = (SYOBJD_Details.API_NAME).strip()
                                                                    #####AUTO NUMBER DATATYPE QUESTION
                                                                    if SYOBJD_Details.DATA_TYPE == "AUTO NUMBER":
                                                                        REL_COL = Sql.GetFirst(
                                                                            "Select RECORD_NAME from SYOBJH (nolock) where RTRIM(LTRIM(OBJECT_NAME))='"
                                                                            + str(REL_TAB_NAME).strip()
                                                                            + "'"
                                                                        )
                                                                        if REL_COL is not None:
                                                                            REC_NO1 = str(Guid.NewGuid()).upper()
                                                                    elif (
                                                                        str(MM_MOD_CUS_OBJ).strip()
                                                                        == str(COL_NAME).strip()
                                                                    ):
                                                                        row[MM_MOD_CUS_OBJ] = str(REC_NO)
                                                                    ####TO OBTAIN RESULT FOR FORMULA LOGIC
                                                                    elif str(COL_NAME).strip() in str(
                                                                        SYOBJD_Details.FORMULA_LOGIC
                                                                    ):
                                                                        result = ScriptExecutor.ExecuteGlobal(
                                                                            "SYPARCEFMA",
                                                                            {
                                                                                "Object": REL_TAB_NAME,
                                                                                "API_Name": str(COL_NAME),
                                                                                "API_Value": str(REC_NO),
                                                                            },
                                                                        )
                                                                        for API_Names in result:
                                                                            API_NAME = str(API_Names["API_NAME"]).strip()
                                                                            RESULT = str(API_Names["FORMULA_RESULT"])
                                                                            row[API_NAME] = str(RESULT)
                                                                    elif not str(COL_NAME).strip() in str(
                                                                        SYOBJD_Details.FORMULA_LOGIC
                                                                    ):
                                                                        
                                                                        if str(MM_MOD_CUS_OBJ) not in (
                                                                            "CPQTABLEENTRYMODIFIEDBY",
                                                                            "CPQTABLEENTRYDATEMODIFIED",
                                                                            "CPQTABLEENTRYADDEDBY",
                                                                            "CPQTABLEENTRYDATEADDED",
                                                                        ):
                                                                            VAL_CUS_OBJ = eval(
                                                                                str("inc." + str(MM_MOD_CUS_OBJ))
                                                                            )
                                                                            row[MM_MOD_CUS_OBJ] = str(VAL_CUS_OBJ)
                                                                        
                                                        Table.TableActions.Create(REL_TAB_NAME, row)
                                                        row1 = {}
                                                        ####TO OBTAIN RESULT FOR FORMULA LOGIC
                                                        try:
                                                            result = ScriptExecutor.ExecuteGlobal(
                                                                "SYPARCEFMA",
                                                                {
                                                                    "Object": REL_TAB_NAME,
                                                                    "API_Name": str(REC_NO1),
                                                                    "API_Value": REC_NO1,
                                                                },
                                                            )
                                                            new_value_dict = {
                                                                API_Names["API_NAME"]: API_Names["FORMULA_RESULT"]
                                                                for API_Names in result
                                                                if API_Names["FORMULA_RESULT"] != ""
                                                            }
                                                            if new_value_dict is not None:
                                                                row1 = {OBJ_COL: str(REC_NO1)}
                                                                row1.update(new_value_dict)
                                                                Trace.Write("Updated 222")
                                                                Table.TableActions.Update(REL_TAB_NAME, OBJ_COL, row1)
                                                        except:
                                                            Trace.Write("NOT SELF REFERENCE RECORD")

                                    ScriptExecutor.ExecuteGlobal(
                                        "SYALLTABOP",
                                        {"Primary_Data": str(REC_NO), "TabNAME": str1, "ACTION": "VIEW", "RELATED": ""},
                                    )
                            #####main SAVE ACTION
                            elif Product.Attributes.GetByName(str(RECORD_ID)) is not None:
                                Rec_Id_Value = Product.Attributes.GetByName(str(RECORD_ID)).GetValue()
                                #Trace.Write("=====Rec_Id_Value"+str(Rec_Id_Value))
                            #####add SAVE ACTION
                            if Rec_Id_Value == "":
                                SYOBJD_OBJNAME = Sql.GetList(
                                    "SELECT OBJECT_NAME,API_NAME, DATA_TYPE,FORMULA_LOGIC,LOOKUP_API_NAME FROM  SYOBJD (nolock) where RTRIM(LTRIM(OBJECT_NAME)) ='"
                                    + str(TABLE_NAME).strip()
                                    + "' and LTRIM(RTRIM(PARENT_OBJECT_RECORD_ID))='"
                                    + str(SYOBJH_OBJ).strip()
                                    + "' "
                                )
                                
                                if SYOBJD_OBJNAME is not None:
                                    for SYOBJD_Details in SYOBJD_OBJNAME:
                                        Trace.Write(
                                            str(SYOBJD_Details.API_NAME)
                                            + " SYOBJD_Details-------476------> "
                                            + str(SYOBJD_Details.DATA_TYPE)
                                        )
                                        SECT_OBJNAME = Sql.GetList(
                                            "select SE.RECORD_ID  FROM SYSECT (nolock)SE inner join SYPAGE(nolock)PG on SE.PAGE_RECORD_ID = PG.RECORD_ID where RTRIM(LTRIM(PG.TAB_NAME)) ='"
                                            + str(str1)
                                            + "' and PG.TAB_RECORD_ID ='"
                                            + str(sql_obj.RECORD_ID).strip()
                                            + "'"
                                        )
                                        if SECT_OBJNAME is not None:
                                            for SECT in SECT_OBJNAME:
                                                SYSEFL_OBJNAME12 = Sql.GetList(
                                                    "SELECT RECORD_ID,FIELD_LABEL, API_NAME,API_FIELD_NAME,SECTION_NAME,FLDDEF_VARIABLE_RECORD_ID,FLDDEF_VARIABLE_NAME,SAPCPQ_ATTRIBUTE_NAME FROM SYSEFL (nolock) where LTRIM(RTRIM(API_NAME)) ='"
                                                    + str(SYOBJD_Details.OBJECT_NAME).strip()
                                                    + "' and LTRIM(RTRIM(API_FIELD_NAME))='"
                                                    + str(SYOBJD_Details.API_NAME)
                                                    + "' and LTRIM(RTRIM(SECTION_RECORD_ID))='"
                                                    + str(SECT.RECORD_ID)
                                                    + "'"
                                                )
                                                if SYSEFL_OBJNAME12 is not None and len(SYSEFL_OBJNAME12) > 0:
                                                    for SYSEFL_OBJNAME in SYSEFL_OBJNAME12:
                                                        Trace.Write("Yes")
                                                        MM_MOD_CUS_OBJ = (SYSEFL_OBJNAME.API_FIELD_NAME).strip()
                                                        SECTIONQSTNRECORDID = (
                                                            str(SYSEFL_OBJNAME.SAPCPQ_ATTRIBUTE_NAME)
                                                            .replace("-", "_")
                                                            .replace(" ", "")
                                                        )
                                                        Trace.Write("MM_MOD_CUS_OBJ__MM_MOD_CUS_OBJ" + str(MM_MOD_CUS_OBJ))
                                                        Trace.Write(
                                                            "str(SYOBJD_Details.DATA_TYPE)" + str(SYOBJD_Details.DATA_TYPE)
                                                        )
                                                        SECQSTNATTRIBUTENAME = SECTIONQSTNRECORDID.upper()                                                    
                                                        if str(SYOBJD_Details.DATA_TYPE) == "LONG TEXT AREA":
                                                            MM_MOD_ATTR_NAME = "QSTN_" + str(SECQSTNATTRIBUTENAME) + "_LONG"
                                                        else:
                                                            MM_MOD_ATTR_NAME = "QSTN_" + str(SECQSTNATTRIBUTENAME)
                                                        Trace.Write(
                                                            "MM_MOD_ATTR_NAME__MM_MOD_ATTR_NAME" + str(MM_MOD_ATTR_NAME)
                                                        )
                                                        
                                                        if SYOBJD_Details.DATA_TYPE == "AUTO NUMBER":
                                                            REC_NO = str(Guid.NewGuid()).upper()
                                                            row[RecId] = str(REC_NO)
                                                        elif (
                                                            SYOBJD_Details.DATA_TYPE != "LOOKUP"
                                                            and SYOBJD_Details.DATA_TYPE != "FORMULA"
                                                            and SYOBJD_Details.DATA_TYPE != "PICKLIST"
                                                            and SYOBJD_Details.DATA_TYPE != "CHECKBOX"
                                                        ):
                                                            if (
                                                                Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME))
                                                                is not None
                                                                and str(SYSEFL_OBJNAME.FLDDEF_VARIABLE_RECORD_ID) == ""
                                                            ):
                                                                Attr_qstn1 = ""
                                                                Attr_qstn2 = ""
                                                                if str(MM_MOD_CUS_OBJ) == "ATTRIBUTE_NAME":
                                                                    row[MM_MOD_CUS_OBJ] = str(Attr_qstn1).title()
                                                                if str(MM_MOD_CUS_OBJ) == "ATTRIBUTE_DESCRIPTION":
                                                                    row[MM_MOD_CUS_OBJ] = str(Attr_qstn2).title()
                                                                else:
                                                                    if MM_MOD_ATTR_NAME == "QSTN_SYSEFL_AC_00067_LONG":
                                                                        msgbody = str(
                                                                            Product.GetGlobal("RichTextVaslue").encode(
                                                                                "ASCII", "ignore"
                                                                            )
                                                                        )
                                                                        # Trace.Write(
                                                                        #     "------------VJ-----------" + str(len(msgbody))
                                                                        # )
                                                                        if len(msgbody) <= 8000:
                                                                            ATTR_Value = str(msgbody)
                                                                            row["MESSAGE_BODY_2"] = ""
                                                                            row["MESSAGE_BODY_3"] = ""
                                                                            row["MESSAGE_BODY_4"] = ""
                                                                            row["MESSAGE_BODY_5"] = ""
                                                                        elif len(msgbody) < 16000:
                                                                            msgsplit = str(msgbody).split("@!#$@!")
                                                                            ATTR_Value = str(msgsplit[0][0:8000])
                                                                            row["MESSAGE_BODY_2"] = str(msgsplit[0][8000:])
                                                                            row["MESSAGE_BODY_3"] = ""
                                                                            row["MESSAGE_BODY_4"] = ""
                                                                            row["MESSAGE_BODY_5"] = ""
                                                                        elif len(msgbody) < 24000:
                                                                            msgsplit = str(msgbody).split("@!#@!")
                                                                            ATTR_Value = str(msgsplit[0][0:8000])
                                                                            row["MESSAGE_BODY_2"] = str(
                                                                                msgsplit[0][8000:16000]
                                                                            )
                                                                            row["MESSAGE_BODY_3"] = str(msgsplit[0][16000:])
                                                                            row["MESSAGE_BODY_4"] = ""
                                                                            row["MESSAGE_BODY_5"] = ""
                                                                        elif len(msgbody) < 32000:
                                                                            msgsplit = str(msgbody).split("@!#@!")
                                                                            ATTR_Value = str(msgsplit[0][0:8000])
                                                                            row["MESSAGE_BODY_2"] = str(
                                                                                msgsplit[0][8000:16000]
                                                                            )
                                                                            row["MESSAGE_BODY_3"] = str(
                                                                                msgsplit[0][16000:24000]
                                                                            )
                                                                            row["MESSAGE_BODY_4"] = str(msgsplit[0][24000:])
                                                                            row["MESSAGE_BODY_5"] = ""
                                                                        elif len(msgbody) < 40000:
                                                                            msgsplit = str(msgbody).split("@!#@!")
                                                                            ATTR_Value = str(msgsplit[0][0:8000])
                                                                            row["MESSAGE_BODY_2"] = str(
                                                                                msgsplit[0][8000:16000]
                                                                            )
                                                                            row["MESSAGE_BODY_3"] = str(
                                                                                msgsplit[0][16000:24000]
                                                                            )
                                                                            row["MESSAGE_BODY_4"] = str(
                                                                                msgsplit[0][24000:32000]
                                                                            )
                                                                            row["MESSAGE_BODY_5"] = str(msgsplit[0][32000:])
                                                                    else:
                                                                        ATTR_Value = (
                                                                            Product.Attributes.GetByName(
                                                                                str(MM_MOD_ATTR_NAME)
                                                                            ).GetValue()
                                                                            or ""
                                                                        )
                                                                row[MM_MOD_CUS_OBJ] = str(ATTR_Value)
                                                                #Trace.Write("rowwe" + str(dict(row)))
                                                            elif (
                                                                Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME))
                                                                is not None
                                                                and str(SYSEFL_OBJNAME.FLDDEF_VARIABLE_RECORD_ID) != ""
                                                            ):
                                                                FLDDEF_VARIABLE_RECORD_ID = (
                                                                    SYSEFL_OBJNAME.FLDDEF_VARIABLE_RECORD_ID
                                                                )
                                                                CTX_Logic = Sql.GetFirst(
                                                                    "select CPQ_CALCULATION_LOGIC from SYVABL (nolock) where RECORD_ID = '"
                                                                    + str(FLDDEF_VARIABLE_RECORD_ID)
                                                                    + "' "
                                                                )
                                                                if CTX_Logic:
                                                                    result = ScriptExecutor.ExecuteGlobal(
                                                                        "SYPARVRLLG",
                                                                        {
                                                                            "CTXLogic": str(CTX_Logic.CPQ_CALCULATION_LOGIC),
                                                                            "Obj_Name": TABLE_NAME,
                                                                        },
                                                                    )
                                                                if result != "":
                                                                    ATTR_Value = str(result)
                                                                    row[MM_MOD_CUS_OBJ] = str(ATTR_Value)
                                                                else:
                                                                    row[MM_MOD_CUS_OBJ] = ""
                                                        elif (SYOBJD_Details.DATA_TYPE).strip() == "PICKLIST (MULTI-SELECT)":
                                                            # if (str(MM_MOD_CUS_OBJ) == "ATTRIBUTE_TYPE"):
                                                            attr_val = Product.GetGlobal("ATTR_VAL")
                                                            #Trace.Write("ATTR_VAL--" + ATTR_VAL)
                                                            if attr_val == "":
                                                                attr_val = "MATERIAL ATTRIBUTE"
                                                            #Trace.Write(
                                                            #     str(MM_MOD_CUS_OBJ) + "is the field which is a picklist!!!"
                                                            # )
                                                            row[MM_MOD_CUS_OBJ] = attr_val
                                                            #Trace.Write(str(attr_val) + "---->multi-select values")
                                                        elif (SYOBJD_Details.DATA_TYPE).strip() == "PICKLIST":
                                                            # if (str("MM_MOD_ATTR_NAME") != "QSTN_SYSEFL_MA_04885"):
                                                            #Trace.Write("str(MM_MOD_ATTR_NAME)" + str(MM_MOD_ATTR_NAME))
                                                            ATTR_Value = Product.Attributes.GetByName(
                                                                str(MM_MOD_ATTR_NAME)
                                                            ).GetValue()
                                                            try:
                                                                row[MM_MOD_CUS_OBJ] = ATTR_Value
                                                            except:
                                                                row[MM_MOD_CUS_OBJ] = str(ATTR_Value)
                                                        elif SYOBJD_Details.DATA_TYPE == "CHECKBOX":
                                                            if (
                                                                Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME))
                                                                is not None
                                                                and str(SYSEFL_OBJNAME.FLDDEF_VARIABLE_RECORD_ID) == ""
                                                            ):
                                                                ATTR_Value = Product.Attributes.GetByName(
                                                                    str(MM_MOD_ATTR_NAME)
                                                                ).GetValue()
                                                                if ATTR_Value == "1":
                                                                    ATTR_Value = "True"
                                                                else:
                                                                    ATTR_Value = "False"
                                                                row[MM_MOD_CUS_OBJ] = str(ATTR_Value)
                                                                '''if str(MM_MOD_CUS_OBJ) == "ALLOW_EX_RT_UPD_SEG_PBK_ENTRY":
                                                                    row[MM_MOD_CUS_OBJ] = "True"'''
                                                            elif (
                                                                Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME))
                                                                is not None
                                                                and str(SYSEFL_OBJNAME.FLDDEF_VARIABLE_RECORD_ID) != ""
                                                            ):
                                                                FLDDEF_VARIABLE_RECORD_ID = (
                                                                    SYSEFL_OBJNAME.FLDDEF_VARIABLE_RECORD_ID
                                                                )
                                                                CTX_Logic = Sql.GetFirst(
                                                                    "select CPQ_CALCULATION_LOGIC from SYVABL (nolock) where RECORD_ID = '"
                                                                    + str(FLDDEF_VARIABLE_RECORD_ID)
                                                                    + "' "
                                                                )
                                                                result = ScriptExecutor.ExecuteGlobal(
                                                                    "SYPARVRLLG",
                                                                    {
                                                                        "CTXLogic": str(CTX_Logic.CPQ_CALCULATION_LOGIC),
                                                                        "Obj_Name": TABLE_NAME,
                                                                    },
                                                                )
                                                                if result != "":
                                                                    ATTR_Value = str(result)
                                                                    if ATTR_Value == "1":
                                                                        ATTR_Value = "True"
                                                                    else:
                                                                        ATTR_Value = "False"
                                                                    row[MM_MOD_CUS_OBJ] = str(ATTR_Value)
                                                            elif (
                                                                Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME))
                                                                is not None
                                                                and str(SYSEFL_OBJNAME.FLDEDT_VARIABLE_RECORD_ID) != ""
                                                            ):
                                                                FLDEDT_VARIABLE_RECORD_ID = (
                                                                    SYSEFL_OBJNAME.FLDEDT_VARIABLE_RECORD_ID
                                                                )
                                                                CTX_Logic = Sql.GetFirst(
                                                                    "select CPQ_CALCULATION_LOGIC from SYVABL (nolock) where RECORD_ID = '"
                                                                    + str(FLDEDT_VARIABLE_RECORD_ID)
                                                                    + "' "
                                                                )
                                                                result = ScriptExecutor.ExecuteGlobal(
                                                                    "SYPARVRLLG",
                                                                    {
                                                                        "CTXLogic": str(CTX_Logic.CPQ_CALCULATION_LOGIC),
                                                                        "Obj_Name": TABLE_NAME,
                                                                    },
                                                                )
                                                                if result != "":
                                                                    ATTR_Value = str(result)
                                                                    row[MM_MOD_CUS_OBJ] = str(ATTR_Value)

                                                        elif SYOBJD_Details.DATA_TYPE == "FORMULA":
                                                            if (
                                                                SYOBJD_Details.FORMULA_LOGIC != ""
                                                                and "select" in str(SYOBJD_Details.FORMULA_LOGIC).lower()
                                                            ):
                                                                if TABLE_NAME != "PRPRCL":
                                                                    SECTIONQSTNRECORDID = (
                                                                        str(SYSEFL_OBJNAME.SAPCPQ_ATTRIBUTE_NAME)
                                                                        .replace("-", "_")
                                                                        .replace(" ", "")
                                                                    )
                                                                    SECQSTNATTRIBUTENAME = (SECTIONQSTNRECORDID).upper()
                                                                    MM_MOD_ATTR_NAME = "QSTN_LKP_" + str(
                                                                        SECQSTNATTRIBUTENAME
                                                                    )
                                                                    Trace.Write(
                                                                        "MM_MOD_ATTR_NAME____MM_MOD_ATTR_NAMEXXXXXXX"
                                                                        + str(MM_MOD_ATTR_NAME)
                                                                    )
                                                                    Trace.Write("API_Value_______API_Value" + str(API_Value))
                                                                    if (
                                                                        Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME))
                                                                        is not None
                                                                    ):
                                                                        API_Value = str(
                                                                            Product.Attributes.GetByName(
                                                                                str(MM_MOD_ATTR_NAME)
                                                                            ).HintFormula
                                                                        )
                                                                        API_obj = Sql.GetFirst(
                                                                            "select API_NAME from  SYOBJD (nolock) where LOOKUP_API_NAME ='"
                                                                            + str(MM_MOD_CUS_OBJ)
                                                                            + "'and OBJECT_NAME='"
                                                                            + str(TABLE_NAME)
                                                                            + "' "
                                                                        )
                                                                        Trace.Write(
                                                                            "LOOKUP CLEAR TEST select API_NAME from  SYOBJD (nolock) where LOOKUP_API_NAME ='"
                                                                            + str(MM_MOD_CUS_OBJ)
                                                                            + "'and OBJECT_NAME='"
                                                                            + str(TABLE_NAME)
                                                                            + "' "
                                                                        )                                                                    
                                                                        # if API_obj is not None and API_Value != "":
                                                                        if API_obj is not None:                                                                    
                                                                            API_Name = str(API_obj.API_NAME).strip()
                                                                            if str(API_Value).upper() == "LOOKUP":
                                                                                OM_ACNT_REC_ID = Product.GetGlobal(
                                                                                    "OM_ACNT_REC_ID"
                                                                                )
                                                                                if OM_ACNT_REC_ID != "":
                                                                                    API_Value = OM_ACNT_REC_ID
                                                                                else:
                                                                                    API_Value = ""
                                                                            row[API_Name] = str(API_Value)
                                                                            result = ScriptExecutor.ExecuteGlobal(
                                                                                "SYPARCEFMA",
                                                                                {
                                                                                    "Object": TABLE_NAME,
                                                                                    "API_Name": str(API_Name),
                                                                                    "API_Value": API_Value,
                                                                                },
                                                                            )
                                                                            for API_Names in result:
                                                                                API_NAME = str(API_Names["API_NAME"]).strip()
                                                                                RESULT = API_Names["FORMULA_RESULT"]
                                                                                row[API_NAME] = RESULT
                                                                elif Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)):
                                                                    ATTR_Value = Product.Attributes.GetByName(
                                                                        str(MM_MOD_ATTR_NAME)
                                                                    ).GetValue()
                                                                    row[MM_MOD_CUS_OBJ] = str(ATTR_Value)
                                                                else:
                                                                    row[MM_MOD_CUS_OBJ] = ""
                                                            elif (
                                                                SYOBJD_Details.FORMULA_LOGIC != ""
                                                                and "select" not in str(SYOBJD_Details.FORMULA_LOGIC).lower()
                                                            ):
                                                                ATTR_Value = str(SYOBJD_Details.FORMULA_LOGIC).strip()
                                                                row[MM_MOD_CUS_OBJ] = str(ATTR_Value)
                                                            elif SYOBJD_Details.FORMULA_LOGIC == "":
                                                                if Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)):
                                                                    ATTR_Value = Product.Attributes.GetByName(
                                                                        str(MM_MOD_ATTR_NAME)
                                                                    ).GetValue()
                                                                row[MM_MOD_CUS_OBJ] = str(ATTR_Value)
                                                            else:
                                                                row[MM_MOD_CUS_OBJ] = ""
                                    #Trace.Write("ROW ADDNEW SAVE-----" + str(dict(row)))
                                    if str(TABLE_NAME) == "ACAPCH":
                                        row["APRCHN_ID"] = row['APRCHN_ID'].upper()
                                        datetime_value = datetime.datetime.now()
                                        Get_UserID = User.Id
                                        UserName = User.Name
                                        ApprovalchainId = row["APRCHN_ID"]
                                        ApprovalchainRecId = row["APPROVAL_CHAIN_RECORD_ID"]
                                        ApprovalObject = row["APROBJ_LABEL"]
                                        ApprovalObjectRecId = row["APROBJ_RECORD_ID"]
                                        StatusLlist = [
                                            "REQUESTED",
                                            "APPROVED",
                                            "REJECTED",
                                            "APPROVAL REQUIRED",
                                            "RECALLED",
                                            "ASSIGNED",
                                            "RESOLVED",
                                            "EXCLUDED",
                                        ]
                                        for status in StatusLlist:
                                            InsertStatus = """INSERT ACACSS (APPROVAL_CHAIN_STATUS_MAPPING_RECORD_ID, APRCHN_ID, APPROVALSTATUS, EXCLUDED_STATUS, APROBJ_LABEL, APROBJ_STATUSFIELD_LABEL, APROBJ_STATUSFIELD_VAL, APROBJ_STATUSFIELD_RECORD_ID, APROBJ_RECORD_ID, APRCHN_RECORD_ID,ADDUSR_RECORD_ID ,CPQTABLEENTRYADDEDBY ,CPQTABLEENTRYDATEADDED , CpqTableEntryModifiedBy ,CpqTableEntryDateModified)SELECT CONVERT(VARCHAR(4000), NEWID()) AS APPROVAL_CHAIN_STATUS_MAPPING_RECORD_ID ,'{ApprovalchainId}' AS APRCHN_ID,'{status}' AS APPROVALSTATUS,'False' AS EXCLUDED_STATUS,'{ApprovalObject}' AS APROBJ_LABEL,'' AS APROBJ_STATUSFIELD_LABEL,'' AS APROBJ_STATUSFIELD_VAL,'' AS APROBJ_STATUSFIELD_RECORD_ID,'{ApprovalObjectRecId}' AS APROBJ_RECORD_ID,'{ApprovalchainRecId}' AS APRCHN_RECORD_ID,'{Get_UserID}' AS ADDUSR_RECORD_ID, '{UserName}' AS CPQTABLEENTRYADDEDBY , convert(VARCHAR(10), '{datetime_value}', 101) AS CPQTABLEENTRYDATEADDED , '{Get_UserID}' AS CpqTableEntryModifiedBy, convert(VARCHAR(10), '{datetime_value}', 101) AS CpqTableEntryDateModified""".format(
                                                datetime_value=datetime_value,
                                                Get_UserID=Get_UserID,
                                                UserName=UserName,
                                                ApprovalchainId=ApprovalchainId,
                                                ApprovalchainRecId=ApprovalchainRecId,
                                                status=status,
                                                ApprovalObject=ApprovalObject,
                                                ApprovalObjectRecId=ApprovalObjectRecId,
                                            )
                                            a = Sql.RunQuery(InsertStatus)
                                    Required_obj = Sql.GetList(
                                        "select top 1000 API_NAME,FIELD_LABEL,DISPLAY_ORDER,REQUIRED from  SYOBJD (nolock) where LTRIM(RTRIM(OBJECT_NAME)) ='"
                                        + str(TABLE_NAME)
                                        + "'and LTRIM(RTRIM(UPPER(REQUIRED)))='1' ORDER BY DISPLAY_ORDER "
                                    )
                            
                                    
                                    #Trace.Write("flag_value" + str(flag))
                                    if Required_obj is not None and Required_obj != "":
                                        for x in Required_obj:
                                            
                                            #Trace.Write("Len_len" + str(len(Required_obj)))
                                            sectalert = x.FIELD_LABEL
                                            #Trace.Write("sectalert_sectalert" + str(sectalert))
                                            #Trace.Write("x.FIELD_LABEL_x.FIELD_LABEL" + str(x.FIELD_LABEL))
                                            if x.API_NAME in row.keys():
                                                API_NAME_val = row[x.API_NAME]
                                                # Trace.Write(
                                                #     "x.API_NAME"
                                                #     + str(x.API_NAME)
                                                #     + " --- API_NAME_val---->"
                                                #     + str(API_NAME_val)
                                                #     + "rows-->"
                                                #     + str(row)
                                                # )
                                                if str(API_NAME_val) == "" or API_NAME_val.upper() == "NONE":
                                                    Trace.Write("row_row_ADD NE1111W")
                                                    flag = "False"
                                                    break
                                                else:
                                                    Trace.Write("row_row_ADD NE1111W2222")
                                                    flag = "True"

                                        for req_add_new in Required_obj:
                                            if req_add_new.API_NAME in row.keys():
                                                API_NAME_val = row[req_add_new.API_NAME]
                                                Trace.Write(
                                                    "API_NAME_val  "
                                                    + str(API_NAME_val)
                                                    + "	row_API_NAME"
                                                    + str(req_add_new.API_NAME)
                                                )
                                                Trace.Write("row_row_ADD NEW" + str(row))
                                                if str(API_NAME_val) == "" or API_NAME_val.upper() == "NONE":
                                                    Field_Labels.append(req_add_new.FIELD_LABEL)
                                        iskey = Sql.GetFirst(
                                            "select API_NAME from  SYOBJD (nolock) where OBJECT_NAME ='"
                                            + str(TABLE_NAME)
                                            + "'and IS_KEY='True' "
                                        )
                                        Trace.Write(
                                            "select API_NAME from  SYOBJD (nolock) where OBJECT_NAME ='"
                                            + str(TABLE_NAME)
                                            + "'and IS_KEY='True' "
                                        )
                                        Trace.Write(str("---is_key---1694---"+str(flag)))
                                        if iskey is not None and flag == "True":
                                            Trace.Write(str("---is_key---1694---"))
                                            Trace.Write(str(iskey.API_NAME) + "---is_key---1695---")
                                            col_name = (iskey.API_NAME).strip()
                                            #Trace.Write(str(col_name) + "---col_name---16996--" + str(row))
                                            unique_val = row[col_name]
                                            Trace.Write("unique_val" + str(unique_val))
                                            if unique_val is not None and unique_val != "":
                                                is_key_table = Sql.GetFirst(
                                                    "select "
                                                    + col_name
                                                    + " from "
                                                    + str(TABLE_NAME)
                                                    + " (nolock)  where "
                                                    + col_name
                                                    + " ='"
                                                    + str(unique_val)
                                                    + "' "
                                                )
                                                if is_key_table is None:
                                                    if (
                                                        "CPQTABLEENTRYMODIFIEDBY" in row.keys()
                                                        and "CPQTABLEENTRYDATEMODIFIED" in row.keys()
                                                    ):
                                                        row.pop("CPQTABLEENTRYMODIFIEDBY")
                                                        row.pop("CPQTABLEENTRYDATEMODIFIED")
                                                        
                                                    Trace.Write(str(CurrentTabName) + "ROW----754------" + str(row))
                                                    if str(CurrentTabName) == "Profile":                                                   
                                                        Trace.Write(
                                                            str(CurrentTabName) + "---CurrentTabName--768---" + str(row)
                                                        )
                                                        
                                                        prfid = Product.Attributes.GetByName(
                                                            "QSTN_SYSEFL_SY_00128"
                                                        ).GetValue()
                                                        prfname = Product.Attributes.GetByName(
                                                            "QSTN_SYSEFL_SY_00129"
                                                        ).GetValue()
                                                        existprofilecheck = SqlHelper.GetList(
                                                            "Select * from cpq_permissions where SYSTEM_ID ='"
                                                            + str(prfid)
                                                            + "'"
                                                        )
                                                        #if existprofilecheck is None:

                                                        nativeProfileSave(row)
                                                        
                                                        # nativeProfileSave(row)
                                                        # permiss_id = Product.GetGlobal('Profile_ID_val')
                                                        # system_id_prf = Product.GetGlobal('SYSTEM_ID_PRF')
                                                        # row['PROFILE_RECORD_ID'] = permiss_id
                                                        # row['PROFILE_ID'] = system_id_prf
                                                        # Table.TableActions.Create(TABLE_NAME,row)
                                                        # to save in SYPRAP Start

                                                        query = Sql.GetList(
                                                            "SELECT APP_LABEL,APP_ID,APP_DESCRIPTION FROM SYAPPS"
                                                        )
                                                        tableInfo = Sql.GetTable("SYPRAP")
                                                        prfid = Product.Attributes.GetByName(
                                                            "QSTN_SYSEFL_SY_00128"
                                                        ).GetValue()
                                                        per_id = Product.GetGlobal("Profile_ID_val")
                                                        prfname = Product.Attributes.GetByName(
                                                            "QSTN_SYSEFL_SY_00129"
                                                        ).GetValue()
                                                        prfname = prfid
                                                        prfdesc = Product.Attributes.GetByName(
                                                            "QSTN_SYSEFL_SY_00130_LONG"
                                                        ).GetValue()
                                                        if query is not None:
                                                            row = {}
                                                            for val in query:

                                                                new_val = str(Guid.NewGuid()).upper()
                                                                row["APP_ID"] = val.APP_LABEL
                                                                row["APP_RECORD_ID"] = val.APP_ID
                                                                
                                                                if row["APP_ID"] == "MATERIALS":
                                                                    row["DEFAULT"] = "True"
                                                                else:
                                                                    row["DEFAULT"] = "False"
                                                                
                                                                row["PROFILE_RECORD_ID"] = per_id
                                                                row["PROFILE_ID"] = prfname
                                                                
                                                                if row["APP_ID"] in [
                                                                    "MATERIALS",
                                                                    "SALES",
                                                                    "SYSTEM ADMIN",
                                                                ]:
                                                                    row["VISIBLE"] = True
                                                                else:
                                                                    row["VISIBLE"] = False
                                                                
                                                                row["PROFILE_APP_RECORD_ID"] = new_val
                                                                tableInfo.AddRow(row)
                                                                
                                                            Sql.Upsert(tableInfo)
                                                            # to save in SYPRAP End
                                                            
                                                            QueryStatementTB = """INSERT INTO SYPRTB ( APP_ID,APP_RECORD_ID,TAB_ID,TAB_RECORD_ID,PROFILE_RECORD_ID,PROFILE_ID,PROFILE_TAB_RECORD_ID,VISIBLE, CPQTABLEENTRYADDEDBY,CpqTableEntryModifiedBy,CPQTABLEENTRYDATEADDED,CpqTableEntryDateModified) SELECT SYTABS.APP_LABEL, SYTABS.APP_RECORD_ID,SYTABS.TAB_LABEL,SYTABS.RECORD_ID,'{}','{}', CONVERT(VARCHAR(4000),NEWID()),'True','{}','{}',convert(VARCHAR(10), '{}', 101),convert(VARCHAR(10), '{}', 101) FROM SYTABS""".format(
                                                                per_id, prfname,UserName,UserId,datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"),datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p")
                                                            )
                                                            Sql.RunQuery(QueryStatementTB)
                                                            
                                                            QueryStatementSN = """INSERT INTO SYPRSN (SECTION_RECORD_ID,SECTION_ID,TAB_ID,TAB_RECORD_ID,PROFILE_RECORD_ID,PROFILE_ID,VISIBLE,PROFILE_SECTION_RECORD_ID,OBJECT_NAME,OBJECT_RECORD_ID,CPQTABLEENTRYADDEDBY,CpqTableEntryModifiedBy) SELECT SYSECT.RECORD_ID, SYSECT.SECTION_NAME,SYPAGE.TAB_NAME,SYPAGE.TAB_RECORD_ID,'{}','{}','True', CONVERT(VARCHAR(4000),NEWID()),SYSECT.PRIMARY_OBJECT_NAME,SYSECT.PRIMARY_OBJECT_RECORD_ID,'{}','{}'  FROM SYSECT INNER JOIN SYPAGE(NOLOCK) ON SYSECT.PAGE_RECORD_ID = SYPAGE.RECORD_ID""".format(
                                                                per_id, prfname,UserName,UserId
                                                            )
                                                            Sql.RunQuery(QueryStatementSN)
                                                            
                                                            QueryStatementAC = """INSERT INTO SYPRAC ( ACTION_RECORD_ID, TAB_RECORD_ID, TAB_NAME, ACTION_TEXT, SECTION_RECORD_ID, SECTION_NAME,PROFILE_RECORD_ID,PROFILE_ID,PROFILE_ACTION_RECORD_ID,VISIBLE,CPQTABLEENTRYADDEDBY,CpqTableEntryModifiedBy) SELECT SYPSAC.RECORD_ID, SYPSAC.TAB_RECORD_ID,SYPSAC.TAB_NAME,SYPSAC.ACTION_NAME,SYPSAC.SECTION_RECORD_ID,SYPSAC.SECTION_NAME,'{}','{}', CONVERT(VARCHAR(4000),NEWID()),'True','{}','{}' FROM SYPSAC""".format(
                                                                per_id, prfname,UserName,UserId
                                                            )
                                                            Sql.RunQuery(QueryStatementAC)
                                                            
                                                           
                                                            QueryStatementQS = """INSERT INTO SYPRSF (SECTIONFIELD_RECORD_ID,SECTION_FIELD_ID,SECTION_RECORD_ID,SECTION_NAME,OBJECT_RECORD_ID,OBJECT_NAME,OBJECTFIELD_API_NAME,PROFILE_RECORD_ID,PROFILE_ID,PROFILE_SECTIONFIELD_RECORD_ID,VISIBLE,CPQTABLEENTRYADDEDBY,CpqTableEntryModifiedBy)SELECT QS.RECORD_ID, QS.FIELD_LABEL,QS.SECTION_RECORD_ID,QS.SECTION_NAME,SC.RECORD_ID,QS.API_NAME,QS.API_NAME,'{}','{}', CONVERT(VARCHAR(4000),NEWID()),1,'{}','{}'  FROM SYSEFL QS inner join SYOBJH SC on  SC.OBJECT_NAME = QS.API_NAME """.format(
                                                                per_id, prfname,UserName,UserId
                                                            )
                                                            Sql.RunQuery(QueryStatementQS)

                                                            QueryStatementOD = """INSERT INTO SYPROD (OBJECTFIELD_RECORD_ID,OBJECT_FIELD_ID,OBJECT_RECORD_ID,OBJECT_NAME,OBJECTFIELD_LABEL,PROFILE_RECORD_ID,PROFILE_ID,PROFILE_OBJECTFIELD_RECORD_ID,VISIBLE,EDITABLE,DEFAULT_EDIT_ACCESS)SELECT SD.RECORD_ID, SD.FIELD_LABEL,SD.PARENT_OBJECT_RECORD_ID,SD.OBJECT_NAME,SD.API_NAME,'{}','{}', CONVERT(VARCHAR(4000),NEWID()),1,1,1 FROM SYOBJD SD  """.format(
                                                                per_id, prfname
                                                            )
                                                            Sql.RunQuery(QueryStatementOD)

                                                            QueryStatementOH = """INSERT INTO SYPROH (OBJECT_RECORD_ID,OBJECT_NAME,CAN_ADD,CAN_EDIT,CAN_DELETE,PROFILE_RECORD_ID,PROFILE_ID,PROFILE_OBJECT_RECORD_ID,VISIBLE)SELECT SH.RECORD_ID, SH.OBJECT_NAME,JS.CAN_ADD,JS.CAN_EDIT,JS.CAN_DELETE,'{}','{}', CONVERT(VARCHAR(4000),NEWID()),1 FROM SYOBJH SH INNER JOIN SYOBJS JS ON JS.CONTAINER_NAME = SH.OBJECT_NAME  """.format(
                                                                per_id, prfname
                                                            )
                                                            Sql.RunQuery(QueryStatementOH)

                                                                                                       
                                                    else:
                                                        ##CPQ Attribute name starts
                                                        Trace.Write('###SAP')
                                                        if ("SAPCPQ_ATTRIBUTE_NAME" in row) and str(TABLE_NAME) == "SYTABS":
                                                            if (str(row["APP_ID"]) != ""):
                                                                APP_ID = str(TABLE_NAME)+"-"+str(row["APP_ID"])+"-"
                                                                cpq_attr_name = Sql.GetFirst("SELECT max(SAPCPQ_ATTRIBUTE_NAME) AS SAPCPQ_ATTRIBUTE_NAME FROM SYTABS (NOLOCK) WHERE SAPCPQ_ATTRIBUTE_NAME like '{}%'".format(str(APP_ID)))
                                                                x = cpq_attr_name.SAPCPQ_ATTRIBUTE_NAME.split("-")
                                                                length = len(x[len(x)-1])
                                                                row["SAPCPQ_ATTRIBUTE_NAME"] = str(APP_ID)+ str(int(x[len(x)-1])+1).zfill(length)
                                                        elif ("SAPCPQ_ATTRIBUTE_NAME" in row) and str(TABLE_NAME) == "SYOBJH":
                                                            cpq_attr_name = Sql.GetFirst("SELECT max(SAPCPQ_ATTRIBUTE_NAME) AS SAPCPQ_ATTRIBUTE_NAME FROM SYOBJH (NOLOCK)")
                                                            x = cpq_attr_name.SAPCPQ_ATTRIBUTE_NAME.split("-")
                                                            length = len(x[len(x)-1])
                                                            row["SAPCPQ_ATTRIBUTE_NAME"] = "SYOBJ-"+ str(int(x[len(x)-1])+1).zfill(length)
                                                        ##CPQ Attribute name ends
                                                        tableInfo = Sql.GetTable(str(TABLE_NAME))
                                                        
                                                        tableInfo.AddRow(row)
                                                        
                                                        Sql.Upsert(tableInfo)
                                                        
                                                        
                                                    Product.Attributes.GetByName(str(RECORD_ID)).Allowed = True
                                                    Product.Attributes.GetByName(str(RECORD_ID)).AssignValue(str(REC_NO))
                                                    try:
                                                        result = ScriptExecutor.ExecuteGlobal(
                                                            "SYPARCEFMA",
                                                            {
                                                                "Object": TABLE_NAME,
                                                                "API_Name": str(RecId),
                                                                "API_Value": str(REC_NO),
                                                            },
                                                        )
                                                        new_value_dict = {
                                                            API_Names["API_NAME"]: API_Names["FORMULA_RESULT"]
                                                            for API_Names in result
                                                            if API_Names["FORMULA_RESULT"] != ""
                                                        }
                                                        if new_value_dict is not None:
                                                            row = {RecId: str(REC_NO)}
                                                            row.update(new_value_dict)
                                                            Table.TableActions.Update(TABLE_NAME, RecId, row)

                                                    except:
                                                        Trace.Write("NOT SELF REFERENCE RECORD")
                                                    if str(SYOBJH_OBJ):
                                                        if str(REC_ID_OBJ.RECORD_NAME) != "permission_id":
                                                            RecId = str(REC_ID_OBJ.RECORD_NAME).strip()
                                                            AutoFieldId = row.get("RecId")
                                                            # Dont Delete the line
                                                            # violationruleInsert.InsertAction(str(SYOBJH_OBJ),str(AutoFieldId),str(TABLE_NAME))
                                                            ScriptExecutor.ExecuteGlobal(
                                                                "SYALLTABOP",
                                                                {
                                                                    "Primary_Data": str(REC_NO),
                                                                    "TabNAME": str(str1),
                                                                    "ACTION": "VIEW",
                                                                    "RELATED": "",
                                                                },
                                                            )

                                                        else:
                                                            per_id = Product.GetGlobal("Profile_ID_val")
                                                            ScriptExecutor.ExecuteGlobal(
                                                                "SYALLTABOP",
                                                                {
                                                                    "Primary_Data": str(per_id),
                                                                    "TabNAME": str(str1),
                                                                    "ACTION": "VIEW",
                                                                    "RELATED": "",
                                                                },
                                                            )
                                                    

                                                else:
                                                    if TABLE_NAME == "cpq_permissions"  and Product.Attributes.GetByName(
                                                        "SEC_N_TAB_PAGE_ALERT"
                                                    ):
                                                        Product.Attributes.GetByName("SEC_N_TAB_PAGE_ALERT").Allowed = True                                                
                                                        Product.Attributes.GetByName(
                                                            "SEC_N_TAB_PAGE_ALERT"
                                                        ).HintFormula = '<div class="col-md-12"   id="PageAlert"  ><div class="row modulesecbnr brdr" data-toggle="collapse" data-target="#Alert11" aria-expanded="true" >NOTIFICATIONS<i class="pull-right fa fa-chevron-down "></i><i class="pull-right fa fa-chevron-up"></i></div><div  id="Alert11" class="col-md-12  alert-notification  brdr collapse in" ><div  class="col-md-12 alert-danger"    ><label ><img src="/mt/OCTANNER_DEV/Additionalfiles/stopicon1.svg" alt="Error">  ERROR : This "PROFILE" Already exists </label></div></div></div>'
                                                                  
                                                    elif Product.Attributes.GetByName("SEC_N_TAB_PAGE_ALERT"):
                                                        Product.Attributes.GetByName("SEC_N_TAB_PAGE_ALERT").Allowed = True
                                                        Product.Attributes.GetByName(
                                                            "SEC_N_TAB_PAGE_ALERT"
                                                        ).HintFormula = '<div class="col-md-12"   id="PageAlert"  ><div class="row modulesecbnr brdr" data-toggle="collapse" data-target="#Alert11" aria-expanded="true" >NOTIFICATIONS<i class="pull-right fa fa-chevron-down "></i><i class="pull-right fa fa-chevron-up"></i></div><div  id="Alert11" class="col-md-12  alert-notification  brdr collapse in" ><div  class="col-md-12 alert-danger"    ><label ><img src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/stopicon1.svg" alt="Error">  ERROR : This "Role Id & Name" Already exists </label></div></div></div>'
                                                                                          
                                            else:
                                                Trace.Write('kkkkk=======')
                                                if (
                                                    Product.Attributes.GetByName("SEC_N_TAB_PAGE_ALERT") is not None
                                                    and flag == "True"
                                                ):
                                                    Product.Attributes.GetByName("SEC_N_TAB_PAGE_ALERT").Allowed = True
                                                    Product.Attributes.GetByName(
                                                        "SEC_N_TAB_PAGE_ALERT"
                                                    ).HintFormula = '<div class="col-md-12"   id="PageAlert"  ><div class="row modulesecbnr brdr" data-toggle="collapse" data-target="#Alert12" aria-expanded="true" >NOTIFICATIONS<i class="pull-right fa fa-chevron-down "></i><i class="pull-right fa fa-chevron-up"></i></div><div  id="Alert12" class="col-md-12  alert-notification  brdr collapse in" ><div  class="col-md-12 alert-danger"    ><label ><img src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/stopicon1.svg" alt="Error">  ERROR : You will not be able to save your data until all required fields are populated </label></div></div></div>'
                                        else:
                                            Trace.Write("sec-alrt===")
                                            col_name = (iskey.API_NAME).strip()
                                            if (
                                                Product.Attributes.GetByName("SEC_N_TAB_PAGE_ALERT") is not None
                                                and flag == "False"
                                            ):
                                                #Trace.Write("insideifflag")
                                                Product.Attributes.GetByName("SEC_N_TAB_PAGE_ALERT").Allowed = True

                                                Product.Attributes.GetByName("SEC_N_TAB_PAGE_ALERT").HintFormula = """<div class='col-md-12' id='PageAlert'  ><div class='row modulesecbnr brdr' data-toggle='collapse' data-target='#Alert13' aria-expanded='true' >NOTIFICATIONS<i class='pull-right fa fa-chevron-down '></i><i class='pull-right fa fa-chevron-up'></i></div><div  id='Alert13' class='col-md-12  alert-notification  brdr collapse in' ><div  class='col-md-12 alert-danger'><label ><img src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/stopicon1.svg" alt="Error">  ERROR : '{}' is a required field </label></div></div></div>""".format(sectalert)
                                                sectalert = ", ".join(Field_Labels)
                                                #Trace.Write("sectalert_sectalert12" + str(sectalert)+str(Product.Attributes.GetByName("SEC_N_TAB_PAGE_ALERT").HintFormula))

                                                if len(Field_Labels) > 1:
                                                    Product.Attributes.GetByName(
                                                        "SEC_N_TAB_PAGE_ALERT"
                                                    ).HintFormula = "<div class='col-md-12' id='PageAlert'  ><div class='row modulesecbnr brdr' data-toggle='collapse' data-target='#Alert13' aria-expanded='true' >NOTIFICATIONS<i class='pull-right fa fa-chevron-down '></i><i class='pull-right fa fa-chevron-up'></i></div><div  id='Alert13' class='col-md-12  alert-notification  brdr collapse in' ><div  class='col-md-12 alert-danger'><label ><img src='/mt/APPLIEDMATERIALS_TST/Additionalfiles/stopicon1.svg' alt='Error'>  ERROR : '{0}' are required fields </label></div></div></div>".format(
                                                        sectalert
                                                    )
                                                if Product.Attributes.GetByName("QSTN_SYSEFL_AC_00006"):
                                                    ApprovalMethod =  Product.Attributes.GetByName("QSTN_SYSEFL_AC_00006")
                                                    if ApprovalMethod == "":
                                                        Product.Attributes.GetByName(
                                                            "SEC_N_TAB_PAGE_ALERT"
                                                        ).HintFormula = "<div class='col-md-12' id='PageAlert'  ><div class='row modulesecbnr brdr' data-toggle='collapse' data-target='#Alert13' aria-expanded='true' >NOTIFICATIONS<i class='pull-right fa fa-chevron-down '></i><i class='pull-right fa fa-chevron-up'></i></div><div  id='Alert13' class='col-md-12  alert-notification  brdr collapse in' ><div  class='col-md-12 alert-danger'><label ><img src='/mt/APPLIEDMATERIALS_TST/Additionalfiles/stopicon1.svg' alt='Error'>  ERROR : Please select an Approval Method from the list for Approval Chain</label></div></div></div>".format(
                                                            sectalert
                                                        )    
                                                if len(Field_Labels) <= 1:
                                                    # Trace.Write("Else Error Message"+str(Product.Attributes.GetByName(
                                                    #     "SEC_N_TAB_PAGE_ALERT"
                                                    # ).Allowed))
                                                    Product.Attributes.GetByName(
                                                        "SEC_N_TAB_PAGE_ALERT"
                                                    ).HintFormula = "<div class='col-md-12' id='PageAlert'  ><div class='row modulesecbnr brdr' data-toggle='collapse' data-target='#Alert13' aria-expanded='true' >NOTIFICATIONS<i class='pull-right fa fa-chevron-down '></i><i class='pull-right fa fa-chevron-up'></i></div><div  id='Alert13' class='col-md-12  alert-notification  brdr collapse in' ><div  class='col-md-12 alert-danger'><label ><img src='/mt/APPLIEDMATERIALS_TST/Additionalfiles/stopicon1.svg' alt='Error'>  ERROR : '{}' is a required field</label></div></div></div>".format(
                                                        sectalert
                                                    )
                                            # commented this code because of not defined flag = 'Falsep'
                                            # if (
                                            #     Product.Attributes.GetByName("SEC_N_TAB_PAGE_ALERT") is not None
                                            #     and flag == "Falsep"
                                            # ):
                                            #     Product.Attributes.GetByName("SEC_N_TAB_PAGE_ALERT").Allowed = True
                                            #     Product.Attributes.GetByName(
                                            #         "SEC_N_TAB_PAGE_ALERT"
                                            #     ).HintFormula = "<div class='col-md-12' id='PageAlert'  ><div class='row modulesecbnr brdr' data-toggle='collapse' data-target='#Alert13' aria-expanded='true' >NOTIFICATIONS<i class='pull-right fa fa-chevron-down '></i><i class='pull-right fa fa-chevron-up'></i></div><div  id='Alert13' class='col-md-12  alert-notification  brdr collapse in' ><div  class='col-md-12 alert-danger'><label ><img src='/mt/APPLIEDMATERIALS_TST/Additionalfiles/stopicon1.svg' alt='Error'> ERROR :  '{}' should be a 6 character alphabet only value</label></div></div></div>".format(
                                            #         sectalert
                                            #     )
                                            elif (
                                                Product.Attributes.GetByName("SEC_N_TAB_PAGE_ALERT") is not None
                                                and flag == "null"
                                            ):
                                                Product.Attributes.GetByName("SEC_N_TAB_PAGE_ALERT").Allowed = True
                                                sectalert = ", ".join(Field_Labels)
                                                #Trace.Write("len____sectalert_sectalert1234" + str(len(Field_Labels)))

                                                if len(Field_Labels) > 1:
                                                    Product.Attributes.GetByName(
                                                        "SEC_N_TAB_PAGE_ALERT"
                                                    ).HintFormula = "<div class='col-md-12' id='PageAlert'  ><div class='row modulesecbnr brdr' data-toggle='collapse' data-target='#Alert13' aria-expanded='true' >NOTIFICATIONS<i class='pull-right fa fa-chevron-down '></i><i class='pull-right fa fa-chevron-up'></i></div><div  id='Alert13' class='col-md-12  alert-notification  brdr collapse in' ><div  class='col-md-12 alert-danger'><label ><img src='/mt/APPLIEDMATERIALS_TST/Additionalfiles/stopicon1.svg' alt='Error'>  ERROR : '{}' are required fields </label></div></div></div>".format(
                                                        sectalert
                                                    )

                                                else:
                                                    Product.Attributes.GetByName(
                                                        "SEC_N_TAB_PAGE_ALERT"
                                                    ).HintFormula = "<div class='col-md-12' id='PageAlert'  ><div class='row modulesecbnr brdr' data-toggle='collapse' data-target='#Alert13' aria-expanded='true' >NOTIFICATIONS<i class='pull-right fa fa-chevron-down '></i><i class='pull-right fa fa-chevron-up'></i></div><div  id='Alert13' class='col-md-12  alert-notification  brdr collapse in' ><div  class='col-md-12 alert-danger'><label ><img src='/mt/APPLIEDMATERIALS_TST/Additionalfiles/stopicon1.svg' alt='Error'>  ERROR : '{}' is a required field</label></div></div></div>".format(
                                                        sectalert
                                                    )

                                                
                                                """Product.Attributes.GetByName("SEC_N_TAB_PAGE_ALERT").Allowed = True
                                                Product.Attributes.GetByName(
                                                    "SEC_N_TAB_PAGE_ALERT"
                                                ).HintFormula = "<div class='col-md-12' id='PageAlert'  ><div class='row modulesecbnr brdr' data-toggle='collapse' data-target='#Alert13' aria-expanded='true' >NOTIFICATIONS<i class='pull-right fa fa-chevron-down '></i><i class='pull-right fa fa-chevron-up'></i></div><div  id='Alert13' class='col-md-12  alert-notification  brdr collapse in' ><div  class='col-md-12 alert-danger'><label ><img src='/mt/APPLIEDMATERIALS_TST/Additionalfiles/stopicon1.svg' alt='Error'> ERROR :  '{}' is a required field</label></div></div></div>".format(
                                                    sectalert
                                                )"""
                                            # A043S001P01-10904 - End
                            #####EDIT SAVE ACTION
                            else:
                                row[RecId] = str(Rec_Id_Value)
                                SYOBJD_OBJNAME = Sql.GetList(
                                    "SELECT OBJECT_NAME,API_NAME, DATA_TYPE,FORMULA_LOGIC, LOOKUP_API_NAME FROM  SYOBJD (nolock) where LTRIM(RTRIM(OBJECT_NAME)) ='"
                                    + str(TABLE_NAME).strip()
                                    + "' and LTRIM(RTRIM(PARENT_OBJECT_RECORD_ID))='"
                                    + str(SYOBJH_OBJ).strip()
                                    + "' "
                                )
                                if SYOBJD_OBJNAME is not None:
                                    for SYOBJD_Details in SYOBJD_OBJNAME:
                                        SECT_OBJNAME = Sql.GetList(
                                            "select SYSECT.RECORD_ID  FROM SYSECT (nolock) INNER JOIN SYPAGE ON SYSECT.PAGE_RECORD_ID = SYPAGE.RECORD_ID where RTRIM(LTRIM(TAB_NAME)) ='"
                                            + str(str1)
                                            + "' and SYPAGE.TAB_RECORD_ID ='"
                                            + str(sql_obj.RECORD_ID).strip()
                                            + "'"
                                        )
                                        if SECT_OBJNAME is not None:
                                            for SECT in SECT_OBJNAME:
                                                SYSEFL_OBJNAME = Sql.GetFirst(
                                                    "SELECT RECORD_ID,FIELD_LABEL,SAPCPQ_ATTRIBUTE_NAME,API_FIELD_NAME, API_NAME,SECTION_NAME,FLDDEF_VARIABLE_RECORD_ID,FLDDEF_VARIABLE_NAME FROM SYSEFL (nolock) where API_NAME ='"
                                                    + str(SYOBJD_Details.OBJECT_NAME).strip()
                                                    + "' and API_FIELD_NAME='"
                                                    + str(SYOBJD_Details.API_NAME).strip()
                                                    + "' and  SECTION_RECORD_ID='"
                                                    + str(SECT.RECORD_ID)
                                                    + "'"
                                                )
                                                if SYSEFL_OBJNAME is not None and str(SYSEFL_OBJNAME.API_NAME) != "":
                                                    MM_MOD_CUS_OBJ = (SYSEFL_OBJNAME.API_FIELD_NAME).strip()
                                                    SECTIONQSTNRECORDID = (
                                                        str(SYSEFL_OBJNAME.SAPCPQ_ATTRIBUTE_NAME)
                                                        .replace("-", "_")
                                                        .replace(" ", "")
                                                    )
                                                    SECQSTNATTRIBUTENAME = SECTIONQSTNRECORDID.upper()
                                                    # A043S001P01-11384 Start
                                                    if str(SYOBJD_Details.DATA_TYPE) == "LONG TEXT AREA":
                                                        MM_MOD_ATTR_NAME = "QSTN_" + str(SECQSTNATTRIBUTENAME) + "_LONG"
                                                    else:
                                                        MM_MOD_ATTR_NAME = "QSTN_" + str(SECQSTNATTRIBUTENAME)
                                                    # A043S001P01-11384 End
                                                    if (
                                                        SYOBJD_Details.DATA_TYPE != "LOOKUP"
                                                        and SYOBJD_Details.DATA_TYPE != "AUTO NUMBER"
                                                        and SYOBJD_Details.DATA_TYPE != "FORMULA"
                                                        and SYOBJD_Details.DATA_TYPE != "PICKLIST"
                                                        and SYOBJD_Details.DATA_TYPE != "CHECKBOX"
                                                        and SYOBJD_Details.DATA_TYPE != "CURRENCY"
                                                    ):
                                                        if (
                                                            Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)) is not None
                                                            and SYSEFL_OBJNAME.FLDDEF_VARIABLE_RECORD_ID == ""
                                                        ):
                                                            if MM_MOD_ATTR_NAME == "QSTN_SYSEFL_AC_00067_LONG":
                                                                msgbody = str(
                                                                    Product.GetGlobal("RichTextVaslue").encode(
                                                                        "ASCII", "ignore"
                                                                    )
                                                                )
                                                                if len(msgbody) <= 8000:
                                                                    ATTR_Value = str(msgbody)
                                                                    row["MESSAGE_BODY_2"] = ""
                                                                    row["MESSAGE_BODY_3"] = ""
                                                                    row["MESSAGE_BODY_4"] = ""
                                                                    row["MESSAGE_BODY_5"] = ""
                                                                elif len(msgbody) < 16000:
                                                                    msgsplit = str(msgbody).split("@!#$@!")
                                                                    ATTR_Value = str(msgsplit[0][0:8000])
                                                                    row["MESSAGE_BODY_2"] = str(msgsplit[0][8000:])
                                                                    row["MESSAGE_BODY_3"] = ""
                                                                    row["MESSAGE_BODY_4"] = ""
                                                                    row["MESSAGE_BODY_5"] = ""
                                                                elif len(msgbody) < 24000:
                                                                    msgsplit = str(msgbody).split("@!#@!")
                                                                    ATTR_Value = str(msgsplit[0][0:8000])
                                                                    row["MESSAGE_BODY_2"] = str(msgsplit[0][8000:16000])
                                                                    row["MESSAGE_BODY_3"] = str(msgsplit[0][16000:])
                                                                    row["MESSAGE_BODY_4"] = ""
                                                                    row["MESSAGE_BODY_5"] = ""
                                                                elif len(msgbody) < 32000:
                                                                    msgsplit = str(msgbody).split("@!#@!")
                                                                    ATTR_Value = str(msgsplit[0][0:8000])
                                                                    row["MESSAGE_BODY_2"] = str(msgsplit[0][8000:16000])
                                                                    row["MESSAGE_BODY_3"] = str(msgsplit[0][16000:24000])
                                                                    row["MESSAGE_BODY_4"] = str(msgsplit[0][24000:])
                                                                    row["MESSAGE_BODY_4"] = ""
                                                                    row["MESSAGE_BODY_5"] = ""
                                                                elif len(msgbody) < 40000:
                                                                    msgsplit = str(msgbody).split("@!#@!")
                                                                    ATTR_Value = str(msgsplit[0][0:8000])
                                                                    row["MESSAGE_BODY_2"] = str(msgsplit[0][8000:16000])
                                                                    row["MESSAGE_BODY_3"] = str(msgsplit[0][16000:24000])
                                                                    row["MESSAGE_BODY_4"] = str(msgsplit[0][24000:32000])
                                                                    row["MESSAGE_BODY_5"] = str(msgsplit[0][32000:])
                                                            else:        
                                                                ATTR_Value = (
                                                                    Product.Attributes.GetByName(
                                                                        str(MM_MOD_ATTR_NAME)
                                                                    ).GetValue()
                                                                    or ""
                                                                )  ## A043S001P01-11384 end
                                                            try:
                                                                row[MM_MOD_CUS_OBJ] = ATTR_Value
                                                            except:
                                                                row[MM_MOD_CUS_OBJ] = str(ATTR_Value)
                                                        elif (
                                                            Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)) is not None
                                                            and SYSEFL_OBJNAME.FLDDEF_VARIABLE_RECORD_ID != ""
                                                        ):
                                                            FLDDEF_VARIABLE_RECORD_ID = str(
                                                                SYSEFL_OBJNAME.FLDDEF_VARIABLE_RECORD_ID
                                                            ).strip()
                                                            CTX_Logic = Sql.GetFirst(
                                                                "select CPQ_CALCULATION_LOGIC from SYVABL (nolock) where RECORD_ID = '"
                                                                + str(FLDDEF_VARIABLE_RECORD_ID)
                                                                + "' "
                                                            )
                                                            result = ScriptExecutor.ExecuteGlobal(
                                                                "SYPARVRLLG",
                                                                {
                                                                    "CTXLogic": str(CTX_Logic.CPQ_CALCULATION_LOGIC),
                                                                    "Obj_Name": str(TABLE_NAME).strip(),
                                                                },
                                                            )
                                                            if result != "":
                                                                ATTR_Value = str(result)
                                                                row[MM_MOD_CUS_OBJ] = str(ATTR_Value)
                                                    elif SYOBJD_Details.DATA_TYPE == "PICKLIST (MULTI-SELECT)":
                                                        
                                                        # if (MM_MOD_CUS_OBJ == "ATTRIBUTE_TYPE"):
                                                        attr_val = Product.GetGlobal("ATTR_VAL")
                                                        row[MM_MOD_CUS_OBJ] = attr_val
                                                    elif SYOBJD_Details.DATA_TYPE == "PICKLIST":               
                                                        sec_attr = []
                                                        Calc_fctr_array = {}
                                                        if str(SECQSTNATTRIBUTENAME) not in sec_attr:
                                                            ATTR_Value = Product.Attributes.GetByName(
                                                                str(MM_MOD_ATTR_NAME)
                                                            ).GetValue()
                                                            try:
                                                                row[MM_MOD_CUS_OBJ] = ATTR_Value
                                                            except:
                                                                row[MM_MOD_CUS_OBJ] = str(ATTR_Value)
                                                        if str(SECQSTNATTRIBUTENAME) in sec_attr:
                                                            row[MM_MOD_CUS_OBJ] = str(
                                                                dict(Calc_fctr_array).get(SECQSTNATTRIBUTENAME)
                                                            )
                                                    elif SYOBJD_Details.DATA_TYPE == "CURRENCY":
                                                        if Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)) is not None:
                                                            ATTR_Value = Product.Attributes.GetByName(
                                                                str(MM_MOD_ATTR_NAME)
                                                            ).GetValue()
                                                            t = ATTR_Value.split(" ")
                                                            if len(t) > 1:
                                                                ATTR_Value = ATTR_Value[2:]
                                                            try:
                                                                row[MM_MOD_CUS_OBJ] = str(ATTR_Value)
                                                            except:
                                                                row[MM_MOD_CUS_OBJ] = ATTR_Value
                                                    elif SYOBJD_Details.DATA_TYPE == "CHECKBOX":

                                                        if (
                                                            Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)) is not None
                                                            and str(SYSEFL_OBJNAME.FLDDEF_VARIABLE_RECORD_ID) == ""
                                                        ):

                                                            ATTR_Value = Product.Attributes.GetByName(
                                                                str(MM_MOD_ATTR_NAME)
                                                            ).GetValue()
                                                            if ATTR_Value == "1":
                                                                ATTR_Value = "True"
                                                            else:
                                                                ATTR_Value = "False"
                                                            # Log.Info("checkbox ATTr"+str(ATTR_Value))
                                                            row[MM_MOD_CUS_OBJ] = str(ATTR_Value)

                                                        elif (
                                                            Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)) is not None
                                                            and str(SYSEFL_OBJNAME.FLDDEF_VARIABLE_RECORD_ID) != ""
                                                        ):

                                                            FLDDEF_VARIABLE_RECORD_ID = (
                                                                SYSEFL_OBJNAME.FLDDEF_VARIABLE_RECORD_ID
                                                            )

                                                            CTX_Logic = Sql.GetFirst(
                                                                "select CPQ_CALCULATION_LOGIC from SYVABL (nolock) where RECORD_ID = '"
                                                                + str(FLDDEF_VARIABLE_RECORD_ID)
                                                                + "' "
                                                            )
                                                            result = ""
                                                            if CTX_Logic:
                                                                result = ScriptExecutor.ExecuteGlobal(
                                                                    "SYPARVRLLG",
                                                                    {
                                                                        "CTXLogic": str(CTX_Logic.CPQ_CALCULATION_LOGIC),
                                                                        "Obj_Name": TABLE_NAME,
                                                                    },
                                                                )
                                                            if result != "":
                                                                ATTR_Value = str(result)
                                                                row[MM_MOD_CUS_OBJ] = str(ATTR_Value)

                                                    elif (
                                                        SYOBJD_Details.DATA_TYPE == "FORMULA"
                                                        and str(MM_MOD_CUS_OBJ) != "EMPLOYEE_STATUS"
                                                    ):
                                                        OBJD_OBJ = Sql.GetFirst(
                                                            "select PERMISSION from  SYOBJD (nolock) where LOOKUP_API_NAME ='"
                                                            + str(MM_MOD_CUS_OBJ)
                                                            + "' and OBJECT_NAME ='"
                                                            + str(TABLE_NAME).strip()
                                                            + "' "
                                                        )
                                                        if OBJD_OBJ is not None and OBJD_OBJ.PERMISSION != "READ ONLY":
                                                            if (
                                                                SYOBJD_Details.FORMULA_LOGIC != ""
                                                                and "select" in str(SYOBJD_Details.FORMULA_LOGIC).lower()
                                                            ):
                                                                SECTIONQSTNRECORDID = (
                                                                    str(SYSEFL_OBJNAME.SAPCPQ_ATTRIBUTE_NAME)
                                                                    .replace("-", "_")
                                                                    .replace(" ", "")
                                                                )

                                                                SECQSTNATTRIBUTENAME = (SECTIONQSTNRECORDID).upper()

                                                                MM_MOD_ATTR_NAME = "QSTN_LKP_" + str(SECQSTNATTRIBUTENAME)

                                                                

                                                                if (
                                                                    Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME))
                                                                    is not None
                                                                ):

                                                                    
                                                                    API_Value = str(
                                                                        Product.Attributes.GetByName(
                                                                            str(MM_MOD_ATTR_NAME)
                                                                        ).HintFormula
                                                                    )

                                                                    API_obj = Sql.GetFirst(
                                                                        "select API_NAME,DATA_TYPE from  SYOBJD (nolock) where LOOKUP_API_NAME ='"
                                                                        + str(MM_MOD_CUS_OBJ)
                                                                        + "' and OBJECT_NAME ='"
                                                                        + str(TABLE_NAME).strip()
                                                                        + "' "
                                                                    )
                                                                    

                                                                    if API_obj is not None:
                                                                        API_Name = str(API_obj.API_NAME).strip()
                                                                        if str(API_Value).upper() == "LOOKUP":
                                                                            API_Value = ""
                                                                        row[API_Name] = str(API_Value)
                                                                        if "DATE" in str(API_obj.DATA_TYPE):
                                                                            API_Name = CONVERT(VARCHAR(10), API_Name, 101,)

                                                                        result = ScriptExecutor.ExecuteGlobal(
                                                                            "SYPARCEFMA",
                                                                            {
                                                                                "Object": TABLE_NAME,
                                                                                "API_Name": str(API_Name),
                                                                                "API_Value": API_Value,
                                                                            },
                                                                        )

                                                                        for API_Names in result:
                                                                            API_NAME = str(API_Names["API_NAME"]).strip()
                                                                            RESULT = str(API_Names["FORMULA_RESULT"])
                                                                            row[API_NAME] = str(RESULT)

                                                                            
                                                            elif (
                                                                SYOBJD_Details.FORMULA_LOGIC != ""
                                                                and "select" not in str(SYOBJD_Details.FORMULA_LOGIC).lower()
                                                            ):
                                                                ATTR_Value = str(SYOBJD_Details.FORMULA_LOGIC).strip()

                                                                

                                                                row[MM_MOD_CUS_OBJ] = str(ATTR_Value)
                                                            elif SYOBJD_Details.FORMULA_LOGIC == "":
                                                                ATTR_Value = Product.Attributes.GetByName(
                                                                    str(MM_MOD_ATTR_NAME)
                                                                ).GetValue()
                                                                row[MM_MOD_CUS_OBJ] = str(ATTR_Value)
                                                        else:
                                                            ATTR_Value = Product.Attributes.GetByName(
                                                                str(MM_MOD_ATTR_NAME)
                                                            ).GetValue()
                                                            row[MM_MOD_CUS_OBJ] = str(ATTR_Value)

                                                    else:                                                      
                                                        ATTR_Value = Product.Attributes.GetByName(
                                                            str(MM_MOD_ATTR_NAME)
                                                        ).GetValue()
                                                        row[MM_MOD_CUS_OBJ] = str(ATTR_Value)
                                                        

                                    Trace.Write("ROW5-----"+str(dict(row)))
                                    if "CPQTABLEENTRYMODIFIEDBY" in row.keys() and "CPQTABLEENTRYDATEMODIFIED" in row.keys():
                                        row.pop("CPQTABLEENTRYMODIFIEDBY")
                                        row.pop("CPQTABLEENTRYDATEMODIFIED")

                                    is_key = Sql.GetFirst(
                                        "select API_NAME from  SYOBJD where OBJECT_NAME ='"
                                        + str(TABLE_NAME)
                                        + "'and IS_KEY='True' "
                                    )
                                    if is_key:
                                        col_name = (is_key.API_NAME).strip()
                                        if str(tab_name) not in  ["Tab","Page","Object","Variable","Script","Email Template","Role","Currency"]:
                                            row[col_name] = str(col_name)
                                        unique_val = row[col_name]
                                        if (
                                                unique_val is not None
                                                and unique_val != ""
                                                or Product.Attributes.GetByName("QSTN_SYSEFL_MA_00387") != ""
                                                and not None
                                            ):

                                                REC_OBJ = Sql.GetFirst(
                                                    "select RECORD_NAME from SYOBJH where OBJECT_NAME ='"
                                                    + str(TABLE_NAME)
                                                    + "' "
                                                )

                                                Required_obj1 = Sql.GetList(
                                                    "select API_NAME,REQUIRED,FIELD_LABEL from  SYOBJD where LTRIM(RTRIM(OBJECT_NAME)) ='"
                                                    + str(TABLE_NAME)
                                                    + "'and REQUIRED='TRUE' "
                                                )

                                                if Required_obj1 :
                                                    for x in Required_obj1:
                                                        API_NAME_val = row[x.API_NAME]
                                                        Trace.Write(
                                                            "API_NAME_val"
                                                            + str(API_NAME_val)
                                                            + "x.API_NAME"
                                                            + str(x.API_NAME)
                                                        )
                                                        if API_NAME_val == "":
                                                            flag = "False"
                                                            break
                                                        else:
                                                            flag = "True"

                                                    for req_fields in Required_obj1:
                                                        API_NAME_val = row[req_fields.API_NAME]
                                                        if API_NAME_val == "":
                                                            Field_Labels.append(req_fields.FIELD_LABEL)

                                                    #Trace.Write("Field_Labels_Field_Labels_Final" + str(Field_Labels))

                                                if REC_OBJ is not None:
                                                    Auto_Col = (REC_OBJ.RECORD_NAME).strip()

                                                    REC_VAL = row[Auto_Col]
                                                    #Trace.Write("REC_VAL_REC_VAL" + str(REC_VAL))
                                                    # REC_VAL=CPQID.KeyCPQId.GetKEYId(str(TABLE_NAME),str(REC_VALUE))

                                                    if REC_VAL != "":
                                                        Trace.Write(
                                                            "selectqwe "
                                                            + col_name
                                                            + " from "
                                                            + str(TABLE_NAME)
                                                            + "  where "
                                                            + col_name
                                                            + " ='"
                                                            + str(unique_val)
                                                            + "' and "
                                                            + Auto_Col
                                                            + "!='"
                                                            + str(REC_VAL)
                                                            + "'"
                                                        )
                                                        is_key_table = Sql.GetFirst(
                                                            "select "
                                                            + col_name
                                                            + " from "
                                                            + str(TABLE_NAME)
                                                            + "  where "
                                                            + col_name
                                                            + " ='"
                                                            + str(unique_val)
                                                            + "' and "
                                                            + Auto_Col
                                                            + "!='"
                                                            + str(REC_VAL)
                                                            + "'"
                                                        )

                                                        if is_key_table and flag == "False":

                                                            if (
                                                                Product.Attributes.GetByName("SEC_N_TAB_PAGE_ALERT")
                                                                is not None
                                                            ):                                                               
                                                                sectalert = ", ".join(Field_Labels)
                                                                Product.Attributes.GetByName(
                                                                    "SEC_N_TAB_PAGE_ALERT"
                                                                ).Allowed = True
                                                                if len(Field_Labels) > 1:
                                                                    Product.Attributes.GetByName(
                                                                        "SEC_N_TAB_PAGE_ALERT"
                                                                    ).HintFormula = "<div class='col-md-12' id='PageAlert'  ><div class='row modulesecbnr brdr' data-toggle='collapse' data-target='#Alert13' aria-expanded='true' >NOTIFICATIONS<i class='pull-right fa fa-chevron-down '></i><i class='pull-right fa fa-chevron-up'></i></div><div  id='Alert13' class='col-md-12  alert-notification  brdr collapse in' ><div  class='col-md-12 alert-danger'><label ><img src='/mt/OCTANNER_DEV/Additionalfiles/stopicon1.svg' alt='Error'>  ERROR : '{0}' are required fields </label></div></div></div>".format(
                                                                        sectalert
                                                                    )

                                                                else:
                                                                    if str(sectalert) != "":
                                                                        Product.Attributes.GetByName(
                                                                            "SEC_N_TAB_PAGE_ALERT"
                                                                        ).HintFormula = '<div class="col-md-12"   id="PageAlert"  ><div class="row modulesecbnr brdr" data-toggle="collapse" data-target="#Alert17" aria-expanded="true" >NOTIFICATIONS<i class="pull-right fa fa-chevron-down "></i><i class="pull-right fa fa-chevron-up"></i></div><div  id="Alert17" class="col-md-12  alert-notification  brdr collapse in" ><div  class="col-md-12 alert-danger"    ><label ><img src="/mt/OCTANNER_DEV/Additionalfiles/stopicon1.svg" alt="Error"> ERROR : "{0}" is a required field </label></div></div></div>'.format(
                                                                            sectalert
                                                                        )
                                                                    else:
                                                                        Product.Attributes.GetByName("SEC_N_TAB_PAGE_ALERT").Allowed =False
                                                                        Table.TableActions.Update(TABLE_NAME, RecId, row)
                                                                        
                                                        elif is_key_table is None:                                                       
                                                            Product.Attributes.GetByName(
                                                                "SEC_N_TAB_PAGE_ALERT"
                                                            ).Allowed = False
                                                            if TABLE_NAME == "cpq_permissions":
                                                                nativeProfileUpdate(row)
                                                            else:
                                                                Trace.Write(str(TABLE_NAME)+"========>>>>> "+str(RecId)+"========>>>>> "+str(row))
                                                                Table.TableActions.Update(
                                                                    TABLE_NAME, RecId, row,
                                                                )
                                                            
                                                            ####TO UPDATE THE EMBLEM TABLE
                                                            '''if Selected_List != "":
                                                                ScriptExecutor.ExecuteGlobal(
                                                                    "MAETEMBTBL",
                                                                    {"Primary_Data": Rec_Id_Value, "List": Selected_List,},
                                                                )'''
                                                            ####TO OBTAIN RESULT FOR FORMULA LOGIC                                      

                                                            if (
                                                                TABLE_NAME != "PASGMT"
                                                                and TABLE_NAME != "PAACSO"
                                                                and TABLE_NAME != "COPART"
                                                            ):
                                                                Trace.Write('1918--------Rec_Id_Value---------------'+str(Rec_Id_Value))
                                                                try:
                                                                    result = ScriptExecutor.ExecuteGlobal(
                                                                        "SYPARCEFMA",
                                                                        {
                                                                            "Object": TABLE_NAME,
                                                                            "API_Name": str(RecId),
                                                                            "API_Value": Rec_Id_Value,
                                                                        },
                                                                    )

                                                                    new_value_dict = {
                                                                        API_Names["API_NAME"]: API_Names["FORMULA_RESULT"]
                                                                        for API_Names in result
                                                                        if API_Names["FORMULA_RESULT"] != ""
                                                                    }

                                                                    if new_value_dict is not None:
                                                                        row = {RecId: str(Rec_Id_Value)}
                                                                        row.update(new_value_dict)
                                                                        #Trace.Write("rowrow------cmcmfma" + str(row))
                                                                        Table.TableActions.Update(
                                                                            TABLE_NAME, RecId, row,
                                                                        )
                                                                        Trace.Write(
                                                                            "oldVal-"
                                                                            + str(oldVal)
                                                                            + " newVal -"
                                                                            + str(newVal)
                                                                        )
                                                                        
                                                                except:
                                                                    Trace.Write("NOT SELF REFERENCE RECORD")

                                                            ###TO SET THE PAGE TO VIEW MODE
                                                            Tree = Product.GetGlobal("SegmentsClickParam")
                                                            TreeParent = Product.GetGlobal("SegmentTreeParentParam")
                                                            RecordId = Product.GetGlobal("segment_rec_id")
                                                            if Tree == "SEG_EDIT" and TreeParent == "Sales Orgs":
                                                                Product.SetGlobal(
                                                                    "SegmentsClickParam", "SEG_VIEW",
                                                                )
                                                                Product.SetGlobal(
                                                                    "SegmentTreeParentParam", "Sales Orgs",
                                                                )
                                                                ScriptExecutor.ExecuteGlobal(
                                                                    "SYALLTABOP",
                                                                    {
                                                                        "Primary_Data": RecordId,
                                                                        "salesorg_data": Rec_Id_Value,
                                                                        "TabNAME": str1,
                                                                        "ACTION": "VIEW",
                                                                        "RELATED": "",
                                                                    },
                                                                )

                                                            else:
                                                                ScriptExecutor.ExecuteGlobal(
                                                                    "SYALLTABOP",
                                                                    {
                                                                        "Primary_Data": Rec_Id_Value,
                                                                        "TabNAME": str1,
                                                                        "ACTION": "VIEW",
                                                                        "RELATED": "",
                                                                    },
                                                                )
                                                            
                                                            if (
                                                                Product.Attributes.GetByName("SEC_N_TAB_PAGE_ALERT")
                                                                is not None
                                                                and flag != "False"
                                                            ):
                                                                Product.Attributes.GetByName(
                                                                    "SEC_N_TAB_PAGE_ALERT"
                                                                ).Allowed = False
                                                                Product.Attributes.GetByName(
                                                                    "SEC_N_TAB_PAGE_ALERT"
                                                                ).HintFormula = ""

                                                        else:
                                                            sectalert = ", ".join(Field_Labels)
                                                            if (
                                                                Product.Attributes.GetByName("SEC_N_TAB_PAGE_ALERT")
                                                                is not None
                                                            ):
                                                               
                                                                if len(Field_Labels) > 1:
                                                                    Product.Attributes.GetByName(
                                                                        "SEC_N_TAB_PAGE_ALERT"
                                                                    ).Allowed = True
                                                                    Product.Attributes.GetByName(
                                                                        "SEC_N_TAB_PAGE_ALERT"
                                                                    ).HintFormula = '<div class="col-md-12"   id="PageAlert"  ><div class="row modulesecbnr brdr" data-toggle="collapse" data-target="#Alert18" aria-expanded="true" >NOTIFICATIONS<i class="pull-right fa fa-chevron-down "></i><i class="pull-right fa fa-chevron-up"></i></div><div  id="Alert18" class="col-md-12  alert-notification  brdr collapse in" ><div  class="col-md-12 alert-danger"    ><label ><img src="/mt/OCTANNER_DEV/Additionalfiles/stopicon1.svg" alt="Error"> ERROR : "{0}" are required fields </label></div></div></div>'.format(
                                                                        sectalert
                                                                    )
                                                                else:
                                                                    result = ScriptExecutor.ExecuteGlobal(
                                                                        "SYPARCEFMA",
                                                                        {
                                                                            "Object": TABLE_NAME,
                                                                            "API_Name": str(RecId),
                                                                            "API_Value": Rec_Id_Value,
                                                                        },
                                                                    )

                                                                    '''new_value_dict = {
                                                                        API_Names["API_NAME"]: API_Names["FORMULA_RESULT"]
                                                                        for API_Names in result
                                                                        if API_Names["FORMULA_RESULT"] != ""
                                                                    }
                                                                    if new_value_dict is not None:
                                                                        row = {RecId: str(Rec_Id_Value)}
                                                                        row.update(new_value_dict)'''
                                                                    Table.TableActions.Update(
                                                                        TABLE_NAME, RecId, row,
                                                                    )
                                                                       
                                                                    ScriptExecutor.ExecuteGlobal(
                                                                        "SYALLTABOP",
                                                                        {
                                                                            "Primary_Data": Rec_Id_Value,
                                                                            "TabNAME": str1,
                                                                            "ACTION": "VIEW",
                                                                            "RELATED": "",
                                                                        },
                                                                    )
                                                                    
                                                                    if Field_Labels:
                                                                        Product.Attributes.GetByName(
                                                                            "SEC_N_TAB_PAGE_ALERT"
                                                                        ).HintFormula = '<div class="col-md-12"   id="PageAlert"  ><div class="row modulesecbnr brdr" data-toggle="collapse" data-target="#Alert18" aria-expanded="true" >NOTIFICATIONS<i class="pull-right fa fa-chevron-down "></i><i class="pull-right fa fa-chevron-up"></i></div><div  id="Alert18" class="col-md-12  alert-notification  brdr collapse in" ><div  class="col-md-12 alert-danger"    ><label ><img src="/mt/OCTANNER_DEV/Additionalfiles/stopicon1.svg" alt="Error"> ERROR : "{0}" are required fields </label></div></div></div>'.format(
                                                                            sectalert
                                                                    )
                                                            
                                                                
                                        else:
                                            if Product.Attributes.GetByName("SEC_N_TAB_PAGE_ALERT") is not None:
                                                Product.Attributes.GetByName("SEC_N_TAB_PAGE_ALERT").Allowed = True
                                                sectalert = ", ".join(Field_Labels)
                                                if len(Field_Labels) > 1:
                                                    Product.Attributes.GetByName(
                                                        "SEC_N_TAB_PAGE_ALERT"
                                                    ).HintFormula = '<div class="col-md-12"   id="PageAlert"  ><div class="row modulesecbnr brdr" data-toggle="collapse" data-target="#Alert19" aria-expanded="true" >NOTIFICATIONS<i class="pull-right fa fa-chevron-down "></i><i class="pull-right fa fa-chevron-up"></i></div><div  id="Alert19" class="col-md-12  alert-notification  brdr collapse in" ><div  class="col-md-12 alert-danger"    ><label ><img src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/stopicon1.svg" alt="Error"> ERROR : "{0}" are required fields </label></div></div></div>'.format(
                                                        sectalert
                                                    )
                                                else:
                                                    Product.Attributes.GetByName(
                                                        "SEC_N_TAB_PAGE_ALERT"
                                                    ).HintFormula = '<div class="col-md-12"   id="PageAlert"  ><div class="row modulesecbnr brdr" data-toggle="collapse" data-target="#Alert19" aria-expanded="true" >NOTIFICATIONS<i class="pull-right fa fa-chevron-down "></i><i class="pull-right fa fa-chevron-up"></i></div><div  id="Alert19" class="col-md-12  alert-notification  brdr collapse in" ><div  class="col-md-12 alert-danger"    ><label ><img src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/stopicon1.svg" alt="Error"> ERROR :"{0}" is a required field  </label></div></div></div>'.format(
                                                        sectalert
                                                    )


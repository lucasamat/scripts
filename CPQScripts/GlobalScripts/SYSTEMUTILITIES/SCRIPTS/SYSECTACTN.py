# =========================================================================================================================================
#   __script_name : SYSECTACTN.PY
#   __script_description :  THIS SCRIPT IS USED TO MANAGE EDITING OF PAGE SECTION.
#   __primary_author__ : JOE EBENEZER
#   __create_date :
#   � BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
#import Webcom
import Webcom.Configurator.Scripting.Test.TestProduct
from datetime import timedelta
from datetime import datetime as date
from SYDATABASE import SQL
import datetime
import re

# import SYPRCALINS as INSERTSYELOG
import SYCNGEGUID as keyid

# import PRIFLWTRGR
import SYERRMSGVL as GetErrorMsg
import math

# import ACVIORULES
# import PRCTPRFPBE

import System.Net


import clr

clr.AddReference("System.Net")
from System.Net import *
from System.Text.Encoding import UTF8
from System import Convert
Trace = Trace  # pylint: disable=E0602
SqlHelper = SqlHelper  # pylint: disable=E0602
User = User  # pylint: disable=E0602
# Product = Product # pylint: disable=E0602
AttributeAccess = AttributeAccess  # pylint: disable=E0602
ScriptExecutor = ScriptExecutor  # pylint: disable=E0602
Log = Log  # pylint: disable=E0602
Param = Param  # pylint: disable=E0602
ApiResponseFactory = ApiResponseFactory  # pylint: disable=E0602
Guid = Guid  # pylint: disable=E0602
#Webcom = Webcom  # pylint: disable=E0602
# pylint: disable = no-name-in-module, import-error, multiple-imports, pointless-string-statement, wrong-import-order
Sql = SQL()
# violationruleInsert = ACVIORULES.ViolationConditions()
flag_return = "FALSE"
today = datetime.datetime.now()
Modified_date = today.strftime("%m/%d/%Y %H:%M:%S %p")


Today_Date = today.strftime("%m/%d/%Y")

TestProduct = Webcom.Configurator.Scripting.Test.TestProduct()
prodName = TestProduct.Name
Trace.Write("prodName!!!!" + str(prodName))
# create Profiles-Native tables-- 9517 End
def nativeProfileUpdate(newdict):
	#Trace.Write('154--newdict--'+str(newdict))
	#Login_Username = 'X0116955'
	#Login_Password = 'Joseph@2020'
	#Login_Password = 'Welcome@123'
	#Login_Domain = 'appliedmaterials_tst'

	#URL = 'https://sandbox.webcomcpq.com'
	#LOGIN_CREDENTIALS = SqlHelper.GetFirst("SELECT Username,Password,Domain,URL FROM SYCONF (nolock)")
	LOGIN_CREDENTIALS = SqlHelper.GetFirst("SELECT USER_NAME, PASSWORD, DOMAIN, URL FROM SYCONF (nolock) WHERE USER_NAME = 'X0117669'")
	if LOGIN_CREDENTIALS is not None:
		Login_Username = str(LOGIN_CREDENTIALS.USER_NAME)
		Login_Password = str(LOGIN_CREDENTIALS.PASSWORD)
		Login_Domain = str(LOGIN_CREDENTIALS.DOMAIN)
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
		Trace.Write('url check----authenticationUrl--'+str(authenticationUrl))
		authRequest = WebRequest.Create(str(authenticationUrl))
		authRequest.Method = "POST"
		authRequest.CookieContainer = CookieContainer()
		authRequest.ContentLength = 0
		authResponse = authRequest.GetResponse()
		cookies = authResponse.Cookies
		authResponseData = StreamReader(authResponse.GetResponseStream()).ReadToEnd()
		xcrf = str(authResponseData).replace('"', "")
		Trace.Write("X-CSRF-Token : " + str(xcrf))

		# cookies
		coookies = ""
		if cookies is not None:
			for cookie in cookies:
				coookies = coookies + str(cookie) + ";"
		#Trace.Write("COOKIES : " + coookies)

		data = "grant_type=password&username=" + Login_Username + "&password=" + Login_Password + "&domain=" + Login_Domain + ""
		Trace.Write("53--data-----" + str(data))
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
		Trace.Write(str(response))
		accessToken = "Bearer " + str(response).split(":")[1].split(",")[0].replace('"', "")
		Trace.Write("ACCESS TOKEN : " + accessToken)
		

		# setPermissionURL = sandboxBaseURL + '/setup/api/v1/admin/permissionGroups'
		# Trace.Write('156-------------------------'+str(setPermissionURL))

		prfname = profile_id_gen = prfid = ""
		Trace.Write('64----nativeProfileSave-------'+str(newdict))
		prfid = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00128").GetValue()
		prf_ID = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00125").GetValue()
		prfname = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00129").GetValue()
		prfdesc = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00130_LONG").GetValue()
		profile_id_gen = prfid
		permissionQuery = Sql.GetFirst(
			"Select permission_id from cpq_permissions where permission_name ='" + str(prfname) + "'"
		)



		


		# setPermissionURL = sandboxBaseURL + '/setup/api/v1/admin/permissionGroups/'+ str(int(prf_ID))
		# Trace.Write('156-------------------------'+str(setPermissionURL))

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
		Trace.Write("188-------------datasave----" + str(datasave))
		setPermissionURL = sandboxBaseURL + "/setup/api/v1/admin/permissionGroups"
		Trace.Write("261----setPermissionURL----" + str(setPermissionURL))
		webclient = System.Net.WebClient()
		webclient.Headers[System.Net.HttpRequestHeader.Host] = "sandbox.webcomcpq.com"
		webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/json; charset=utf-8"
		webclient.Headers[System.Net.HttpRequestHeader.Cookie] = coookies
		webclient.Headers.Add("X-CSRF-Token", xcrf)
		webclient.Headers.Add("Authorization", accessToken)
		response = webclient.UploadString(str(setPermissionURL), datasave)
		#Trace.Write("PERMISSIONS : " + str(response.encode("ascii", "ignore")))
	return "response"

def sec_edit(SEC_REC_ID):
	Product.SetGlobal("SEC_REC_ID", SEC_REC_ID)
	# sec_cancel("")
	Flag_Val = "FALSE"
	Flag25 = ""
	PriceFlag = ""

	
	Product.Attributes.GetByName("MA_MTR_TAB_ACTION").AssignValue("SEG_EDIT")

	SYSEFL_OBJNAME = Sql.GetList(
		" SELECT MQ.SAPCPQ_ATTRIBUTE_NAME, MQ.RECORD_ID, MD.DATA_TYPE, MD.PERMISSION, MD.SOURCE_DATA, MQ.API_NAME, MQ.FIELD_LABEL FROM SYSEFL (NOLOCK) MQ"
		+ " INNER JOIN SYOBJD (NOLOCK) MD ON MQ.API_FIELD_NAME = MD.API_NAME AND MD.OBJECT_NAME = MQ.API_NAME"
		+ " WHERE  MQ.SECTION_RECORD_ID='"
		+ str(SEC_REC_ID)
		+ "'"
	)
	# Trace.Write(
	# 	" SELECT MQ.SAPCPQ_ATTRIBUTE_NAME, MQ.RECORD_ID, MD.DATA_TYPE, MD.PERMISSION, MD.SOURCE_DATA, MQ.API_NAME, MQ.FIELD_LABEL FROM SYSEFL (NOLOCK) MQ"
	# 	+ " INNER JOIN SYOBJD (NOLOCK) MD ON MQ.API_FIELD_NAME = MD.API_NAME AND MD.OBJECT_NAME = MQ.API_NAME"
	# 	+ " WHERE  MQ.SECTION_RECORD_ID='"
	# 	+ str(SEC_REC_ID)
	# 	+ "'"
	# )
	if SYSEFL_OBJNAME:
		for SYSEFL_Details in SYSEFL_OBJNAME:
			SECTIONQSTNRECORDID = str(SYSEFL_Details.SAPCPQ_ATTRIBUTE_NAME).replace("-", "_").replace(" ", "")
			SECQSTNATTRIBUTENAME = (SECTIONQSTNRECORDID).upper()
			Trace.Write("check"+str(SECQSTNATTRIBUTENAME))
			
			MM_MOD_ATTR_NAME = (
				"QSTN_{}_LONG".format(SECQSTNATTRIBUTENAME)
				
				if SYSEFL_Details.DATA_TYPE.upper() == "LONG TEXT AREA" 
				else "QSTN_{}".format(SECQSTNATTRIBUTENAME)
			)
			
			# MM_MOD_ATTR_NAME = "QSTN_" + str(SECQSTNATTRIBUTENAME)
			# cancel_btn = save_btn = ''	
			# sec_html_btn = Sql.GetList("SELECT HTML_CONTENT FROM SYPSAC (NOLOCK) WHERE SECTION_RECORD_ID = '"+str(SEC_REC_ID)+"'")
			# cancelclick = "sec_cancel_tab(this)"
			# saveclick = "sec_save_tab(this)"
			# if sec_html_btn is not None:
			# 	for btn in sec_html_btn:
			# 		Trace.Write("Button")					
			# 		if "CANCEL" in btn.HTML_CONTENT:
			# 			cancel_btn = str(btn.HTML_CONTENT).format(cancel_onclick=cancelclick)
			# 		if "SAVE" in btn.HTML_CONTENT:
			# 			save_btn = str(btn.HTML_CONTENT).format(save_onclick= saveclick)

			# 	cancel_save = '<div  class="g4 sec_' + str(SEC_REC_ID) + ' collapse in except_sec removeHorLine iconhvr sec_edit_sty">'+ str(cancel_btn) + str(save_btn) +'</div>'
			# 	Trace.Write('cancel_save'+str(cancel_save))
			
			if (SEC_REC_ID == "C20DB474-B645-4D91-B733-695D807B9FF0"):
				Trace.Write("CHK_TEST")
			if (SEC_REC_ID == "C20DB474-B645-4D91-B733-695D807B9FF0") or (
				SEC_REC_ID == "6F573442-D205-49C6-8368-039AEF7CC23D"
			):
				queList = [
					"QSTN_SYSEFL_QT_01116",
					"QSTN_SYSEFL_QT_01114",
					"QSTN_SYSEFL_QT_01119",
					"QSTN_SYSEFL_QT_01121",					
					"QSTN_SYSEFL_QT_01138",
					"QSTN_SYSEFL_QT_01139",
					"QSTN_SYSEFL_QT_01141",					
					"QSTN_SYSEFL_QT_01143",
					"QSTN_SYSEFL_QT_01144",
					"QSTN_SYSEFL_QT_01146",
					"QSTN_SYSEFL_QT_01147",
					"QSTN_SYSEFL_QT_01149",
					"QSTN_SYSEFL_QT_01151",
					"QSTN_SYSEFL_QT_01152",
					"QSTN_SYSEFL_QT_01154",
					"QSTN_SYSEFL_QT_01133",
					"QSTN_SYSEFL_QT_01134",
					"QSTN_SYSEFL_QT_01136",
					"QSTN_SYSEFL_QT_01137",                    
				]
				
				if Product.Attributes.GetByName("SYSEFL-QT-01127") is not None:
					Product.Attributes.GetByName("SYSEFL-QT-01127").Access = AttributeAccess.ReadOnly
				for info in queList:
					if Product.Attributes.GetByName(info) is not None:
						Product.DisallowAttr(info)
			if SYSEFL_Details.DATA_TYPE.upper() == "FORMULA":
				MM_LKP_MOD_ATTR_NAME = "QSTN_LKP_" + str(SECQSTNATTRIBUTENAME)
				
				if (
					Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME))
					and SYSEFL_Details.PERMISSION != "READ ONLY"
					and SYSEFL_Details.SOURCE_DATA != "ERP"
				):
					Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).Allowed = True
					Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).Access = 0
					
				elif Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)):					
					Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).Allowed = True
					Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).Access = AttributeAccess.ReadOnly
				if Product.Attributes.GetByName(str(MM_LKP_MOD_ATTR_NAME)):
					Product.Attributes.GetByName(str(MM_LKP_MOD_ATTR_NAME)).Allowed = True
					Product.Attributes.GetByName(str(MM_LKP_MOD_ATTR_NAME)).Access = 0
					Product.Attributes.GetByName(str(MM_LKP_MOD_ATTR_NAME)).Access = AttributeAccess.ReadOnly
					
					if str(MM_LKP_MOD_ATTR_NAME) == "QSTN_LKP_SYSEFL_QT_01124":					
						Product.Attributes.GetByName(str(MM_LKP_MOD_ATTR_NAME)).Allowed = True
					if SYSEFL_Details.PERMISSION == "READ ONLY":
						Product.Attributes.GetByName(str(MM_LKP_MOD_ATTR_NAME)).Access = AttributeAccess.Hidden
						
			elif (
				SYSEFL_Details.PERMISSION == "READ ONLY"
				or SYSEFL_Details.DATA_TYPE == "AUTO NUMBER"
				or SYSEFL_Details.SOURCE_DATA == "ERP"
			):
				Trace.Write("check1")
				if Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)):
					Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).Access = AttributeAccess.ReadOnly
					Trace.Write("check2")
					                 
			else: 				
				Trace.Write("check3")                  
				if Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)):					
					Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).Access = AttributeAccess.Editable
					Trace.Write("check4")
				
				if str(Flag25):
					Trace.Write("Flag25" + str(Flag25))
		cancel_btn = save_btn = ''	
		sec_html_btn = Sql.GetList("SELECT HTML_CONTENT FROM SYPSAC (NOLOCK) WHERE SECTION_RECORD_ID = '"+str(SEC_REC_ID)+"'")
		cancelclick = "sec_cancel_tab(this)"
		saveclick = "sec_save_tab(this)"
		if sec_html_btn is not None:
			for btn in sec_html_btn:
				Trace.Write("Button")					
				if "CANCEL" in btn.HTML_CONTENT:
					cancel_btn = str(btn.HTML_CONTENT).format(cancel_onclick=cancelclick)
				if "SAVE" in btn.HTML_CONTENT:
					save_btn = str(btn.HTML_CONTENT).format(save_onclick= saveclick)

			cancel_save = '<div  class="g4 sec_' + str(SEC_REC_ID) + ' collapse in except_sec removeHorLine iconhvr sec_edit_sty">'+ str(cancel_btn) + str(save_btn) +'</div>'
			Trace.Write('cancel_save'+str(cancel_save))			
				
	Product.Attributes.GetByName("SEC_N_TAB_PAGE_ALERT").Allowed = False
	Product.Attributes.GetByName("SEC_N_TAB_PAGE_ALERT").HintFormula = ""
	return "True", cancel_save


def sec_view(SEC_REC_ID, TABLE_NAME, Auto_col, Rec_Id_Value):
	Product.Attributes.GetByName("MA_MTR_TAB_ACTION").AssignValue("VIEW")
	#Trace.Write(
	#	"sqlobj"
	#	+ str("select * from " + str(TABLE_NAME) + " with (nolock) where " + str(Auto_col) + "='" + str(Rec_Id_Value) + "' ")
	#)
	SQLobj = Sql.GetFirst(
		"select * from " + str(TABLE_NAME) + " with (nolock) where " + str(Auto_col) + "='" + str(Rec_Id_Value) + "'"
	)
	new_dict = {}
	Prod_Name = Product.Name
	CurrentTab = TestProduct.CurrentTab
	AuditSectionRecId = ""
	Trace.Write("Prod_Name" + Prod_Name)
	Trace.Write("CurrentTab" + CurrentTab)
	MOD_OBJ = Sql.GetFirst(
		"select RECORD_ID from SYTABS where APP_LABEL='"
		+ str(Prod_Name)
		+ "' and SAPCPQ_ALTTAB_NAME='"
		+ str(CurrentTab)
		+ "'"
	)
	if MOD_OBJ is not None:		
		SEC_OBJ = Sql.GetFirst(
			"select SYSECT.RECORD_ID from SYSECT (NOLOCK) INNER JOIN SYPAGE (NOLOCK) on SYSECT.PAGE_RECORD_ID = SYPAGE.RECORD_ID where SYPAGE.TAB_RECORD_ID = '"
			+ str(MOD_OBJ.RECORD_ID)
			+ "' and SYSECT.SECTION_NAME='AUDIT INFORMATION' "
		)
		if SEC_OBJ is not None:
			AuditSectionRecId = SEC_OBJ.RECORD_ID
	if str(TABLE_NAME) == "cpq_permissions":
		SYSEFL_OBJNAME = Sql.GetList(
		"SELECT q.SAPCPQ_ATTRIBUTE_NAME as RECORD_ID,o.DATA_TYPE,o.PERMISSION,q.API_FIELD_NAME as API_NAME,o.DECIMALS,o.FORMULA_DATA_TYPE FROM SYSEFL (nolock) q INNER JOIN  SYOBJD (nolock) o ON q.API_FIELD_NAME = o.API_NAME  and o.OBJECT_NAME = q.API_NAME where q.SECTION_RECORD_ID ='"
		+ str(SEC_REC_ID)
		+ "'"
		)
	else:
		SYSEFL_OBJNAME = Sql.GetList(
			"SELECT q.SAPCPQ_ATTRIBUTE_NAME as RECORD_ID,o.DATA_TYPE,o.PERMISSION,q.API_FIELD_NAME as API_NAME,o.DECIMALS,o.FORMULA_DATA_TYPE FROM SYSEFL (nolock) q INNER JOIN  SYOBJD (nolock) o ON q.API_FIELD_NAME = o.API_NAME  and o.OBJECT_NAME = q.API_NAME where q.SECTION_RECORD_ID ='"
			+ str(SEC_REC_ID)
			+ "' OR q.SECTION_RECORD_ID ='"
			+ str(AuditSectionRecId)
			+ "'"
		)
	if SYSEFL_OBJNAME is not None and SQLobj is not None:
		for SYSEFL_Details in SYSEFL_OBJNAME:
			SECTIONQSTNRECORDID = str(SYSEFL_Details.RECORD_ID).replace("-", "_").replace(" ", "")
			SECQSTNATTRIBUTENAME = (SECTIONQSTNRECORDID).upper()
			MM_MOD_ATTR_NAME = "QSTN_" + str(SECQSTNATTRIBUTENAME)
			try:
				MM_MOD_CUS_OBJ = eval(str("SQLobj." + str(SYSEFL_Details.API_NAME)).strip())
			except:
				MM_MOD_CUS_OBJ = ""
			
			DATA_TYPE = str(SYSEFL_Details.DATA_TYPE)
			Decimal_Value = str(SYSEFL_Details.DECIMALS)
			FORMULA_DATA_TYPE_SYOBJD = str(SYSEFL_Details.FORMULA_DATA_TYPE)
			if DATA_TYPE == "AUTO NUMBER" and Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)) is not None:

				Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).DisplayType = "FreeInputNoMatching"
				Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).AssignValue(str(MM_MOD_CUS_OBJ))
				Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).Allowed = True
				Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).Access = AttributeAccess.ReadOnly

			elif DATA_TYPE == "PICKLIST" and Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)) is not None:				
				if str(SEC_REC_ID) != "A7406EB8-0714-4461-97F8-9E04B05698E5":
					try:
						if str(MM_MOD_ATTR_NAME) == "QSTN_SYSEFL_PB_00489":
							Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).SelectDisplayValues(str(MM_MOD_CUS_OBJ))
							Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).Access = AttributeAccess.ReadOnly
						else:
							Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).SelectDisplayValues(MM_MOD_CUS_OBJ)
							Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).Access = AttributeAccess.ReadOnly
					except:
						Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).SelectDisplayValues(str(MM_MOD_CUS_OBJ))
						Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).Access = AttributeAccess.ReadOnly
				else:
					new_dict.update({str(SECQSTNATTRIBUTENAME): str(MM_MOD_CUS_OBJ)})

			elif DATA_TYPE == "NUMBER" or DATA_TYPE == "CURRENCY":
				if MM_MOD_CUS_OBJ:					
					my_format = "{:." + str(Decimal_Value) + "f}"
					MM_MOD_CUS_OBJ = str(my_format.format(round(float(MM_MOD_CUS_OBJ), int(Decimal_Value))))					
				Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).AssignValue(str(MM_MOD_CUS_OBJ))
				Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).Access = AttributeAccess.ReadOnly

			elif FORMULA_DATA_TYPE_SYOBJD == "PERCENT" or DATA_TYPE == "PERCENT":
				if MM_MOD_CUS_OBJ:
					my_format = "{:." + str(Decimal_Value) + "f}"
					MM_MOD_CUS_OBJ = str(my_format.format(round(float(MM_MOD_CUS_OBJ), int(Decimal_Value)))) + " %"
				Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).AssignValue(str(MM_MOD_CUS_OBJ))
				Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).Access = AttributeAccess.ReadOnly

			elif DATA_TYPE == "CHECKBOX" and Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)) is not None:
				if str(MM_MOD_CUS_OBJ).upper() == "TRUE" or str(MM_MOD_CUS_OBJ) == "1":
					Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).SelectDisplayValue("1")
					Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).Access = AttributeAccess.ReadOnly
				else:
					Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).SelectDisplayValue("0")
					Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).Access = AttributeAccess.ReadOnly

			elif DATA_TYPE == "FORMULA" and Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)) is not None:
				# RELEASE NOTES FOR A043S001P01-8996 A043S001P01-7591
				if str(SYSEFL_Details.API_NAME).strip().upper() == "CPQTABLEENTRYMODIFIEDBY":
					if str(MM_MOD_CUS_OBJ) != "":
						MM_MOD_CUS_OBJ = Sql.GetFirst(
							"select USERNAME from users where id = " + str(MM_MOD_CUS_OBJ)
						).USERNAME						
				# RELEASE NOTES FOR A043S001P01-8996 A043S001P01-7591
				Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).AssignValue(str(MM_MOD_CUS_OBJ))
				Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).Access = AttributeAccess.ReadOnly

				RECORDID = str(SYSEFL_Details.RECORD_ID).replace("-", "_").replace(" ", "").upper()
				MOD_ATTR_NAME = "QSTN_LKP_" + str(RECORDID)
				
				try:

					OBJD_OBJ = Sql.GetFirst(
						"select API_NAME from  SYOBJD where LTRIM(RTRIM(DATA_TYPE))='LOOKUP' and LTRIM(RTRIM(OBJECT_NAME))='"
						+ str(TABLE_NAME).strip()
						+ "' and LTRIM(RTRIM(LOOKUP_API_NAME)) = '"
						+ str(SYSEFL_Details.API_NAME).strip()
						+ "' "
					)
					#Trace.Write(
					#	"select API_NAME from  SYOBJD where LTRIM(RTRIM(DATA_TYPE))='LOOKUP' and LTRIM(RTRIM(OBJECT_NAME))='"
					#	+ str(TABLE_NAME).strip()
					#	+ "' and LTRIM(RTRIM(LOOKUP_API_NAME)) = '"
					#	+ str(SYSEFL_Details.API_NAME).strip()
					#	+ "' "
					#)

					if OBJD_OBJ is not None:
						MOD_CUS_OBJ = eval(str("SQLobj." + str(OBJD_OBJ.API_NAME)))					
						if Product.Attributes.GetByName(str(MOD_ATTR_NAME)) is not None and MOD_CUS_OBJ != "":
							Product.Attributes.GetByName(str(MOD_ATTR_NAME)).HintFormula = str(MOD_CUS_OBJ)
						elif Product.Attributes.GetByName(str(MOD_ATTR_NAME)) is not None:
							Product.Attributes.GetByName(str(MOD_ATTR_NAME)).HintFormula = ""

				except:
					Trace.Write("ERROR")

			elif DATA_TYPE == "LOOKUP" and Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)) is not None:
				Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).AssignValue(str(MM_MOD_CUS_OBJ))
				Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).Access = AttributeAccess.ReadOnly

			elif Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)) is not None:			
				try:					
					Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).AssignValue(str(MM_MOD_CUS_OBJ))

					Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).Access = AttributeAccess.ReadOnly
				except:					
					Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).AssignValue(MM_MOD_CUS_OBJ)

					Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).Access = AttributeAccess.ReadOnly

			elif Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)) is not None:
				Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).AssignValue("")
				Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).Access = AttributeAccess.ReadOnly

			elif Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)):
				Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).Access = AttributeAccess.ReadOnly

	return "true"


def sec_save(SEC_REC_ID, ATTR_VAL, Picklist_array):	
	flag_return = "FALSE"
	SalesEmployeePhone = ""
	row = {}
	sec_attr = []
	requiredDict = []	
	if len(Picklist_array) > 0:
		for data, lab in dict(Picklist_array).items():
			sec_attr.append(data)
	# row["CPQTABLEENTRYADDEDBY"] = User.UserName
	# row["CPQTABLEENTRYMODIFIEDBY"] = User.Id
	# row["CPQTABLEENTRYDATEADDED"] = Modified_date
	# row["CPQTABLEENTRYDATEMODIFIED"] = Modified_date
	Auto_col = ""
	Rec_Id_Value = ""
	flag = "TRUE"
	
	SYSECT_OBJID = Sql.GetFirst(
		"SELECT SAPCPQ_ATTRIBUTE_NAME FROM SYSECT (NOLOCK) WHERE RECORD_ID='" + str(SEC_REC_ID) + "' "
	)
	if SYSECT_OBJID:
		Product_code = SYSECT_OBJID.SAPCPQ_ATTRIBUTE_NAME.split("-")
	# current_tab=str(TestProduct.CurrentTab)
	CurrentTab = TestProduct.CurrentTab  # pylint: disable=unused-variable
	Product_code = Product_code[1]
	USGB_VAL = ""
	# USGB_VAL = Product.Attributes.GetByName('QSTN_SYSEFL_SE_00192').GetValue()
	# A043S001P01-6040,A043S001P01-7124 &A043S001P01-7126 START
	
	SYSEFL_OBJNAME = Sql.GetList(
		" SELECT MQ.SAPCPQ_ATTRIBUTE_NAME as RECORD_ID,  MQ.API_FIELD_NAME as API_NAME, MQ.FLDDEF_VARIABLE_RECORD_ID, MD.DATA_TYPE, MD.PERMISSION, MD.REQUIRED,"
		+ " MD.IS_KEY, MD.OBJECT_NAME, MD.FORMULA_LOGIC FROM SYSEFL (NOLOCK) MQ"
		+ " INNER JOIN  SYOBJD (NOLOCK) MD ON MQ.API_FIELD_NAME = MD.API_NAME AND MD.OBJECT_NAME = MQ.API_NAME WHERE  MQ.SECTION_RECORD_ID='"
		+ str(SEC_REC_ID)
		+ "' "
	)
	# A043S001P01-6040,A043S001P01-7124 & A043S001P01-7126 END
	if SYSEFL_OBJNAME is not None:
		TABLE_NAME = ""
		for SYSEFL_Details in SYSEFL_OBJNAME:
			TABLE_NAME = str(SYSEFL_Details.OBJECT_NAME)

			# Auto No field
			# A043S001P01-6040 START
			REC_ID_OBJ = Sql.GetFirst(
				"Select RECORD_ID,RECORD_NAME from SYOBJH (nolock) where RTRIM(LTRIM(OBJECT_NAME))='" + TABLE_NAME + "'"
			)
			if REC_ID_OBJ is not None:
				Auto_col = str(REC_ID_OBJ.RECORD_NAME).strip()

				QUE_OBJ = Sql.GetFirst(
					"SELECT SYSEFL.SAPCPQ_ATTRIBUTE_NAME as RECORD_ID  from SYSEFL (nolock) INNER JOIN SYSECT (NOLOCK) ON SYSECT.RECORD_ID = SYSEFL.SECTION_RECORD_ID INNER JOIN SYPAGE (NOLOCK) on SYSECT.PAGE_RECORD_ID = SYPAGE.RECORD_ID where SYSEFL.API_FIELD_NAME='"
					+ str(Auto_col)
					+ "' and SYSEFL.API_NAME='"
					+ str(TABLE_NAME)
					+ "' and SYSEFL.SAPCPQ_ATTRIBUTE_NAME like '%"
					+ str(Product_code)
					+ "%' AND SYPAGE.TAB_RECORD_ID!='' "
				)
				if QUE_OBJ is not None:					
					RECORDID = str(QUE_OBJ.RECORD_ID).replace("-", "_").replace(" ", "")
					ATTRIBUTENAME = (RECORDID).upper()
					Auto_Field = "QSTN_" + str(ATTRIBUTENAME).strip()					
					if Product.Attributes.GetByName(str(Auto_Field)) is not None:
						Rec_Id_Value = Product.Attributes.GetByName(str(Auto_Field)).GetValue()
					if Rec_Id_Value != "":
						row[Auto_col] = str(Rec_Id_Value)						
						cpq_id = Sql.GetFirst(
							"select CpqTableEntryId from "
							+ str(TABLE_NAME)
							+ " with (nolock) where "
							+ str(Auto_col)
							+ "='"
							+ str(Rec_Id_Value)
							+ "'"
						)
						if cpq_id is not None:
							row["CpqTableEntryId"] = cpq_id.CpqTableEntryId

			# Except Auto Number Field
			SECTIONQSTNRECORDID = str(SYSEFL_Details.RECORD_ID).replace("-", "_").replace(" ", "")
			SECQSTNATTRIBUTENAME = (SECTIONQSTNRECORDID).upper()
			MM_MOD_ATTR_NAME = "QSTN_" + str(SECQSTNATTRIBUTENAME)			
			MM_MOD_CUS_OBJ = str(SYSEFL_Details.API_NAME)
			
			if str(SECQSTNATTRIBUTENAME) not in sec_attr:
				if Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)):
					ATTR_Value = Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).GetValue()

				# COMMENT LINE 557 BECAUSE OF THE UNICODE ERROR - HARINIPRIYA
				

			if SYSEFL_Details.DATA_TYPE == "PICKLIST" and str(MM_MOD_CUS_OBJ) != "ATTRIBUTE_TYPE":
				if str(SECQSTNATTRIBUTENAME) not in sec_attr:
					if Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)):
						ATTR_Value = Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).GetValue()
						if ATTR_Value == "..Select":
							ATTR_Value = ""						
					try:
						row[MM_MOD_CUS_OBJ] = ATTR_Value						
					except:
						row[MM_MOD_CUS_OBJ] = str(ATTR_Value)						
				else:
					row[MM_MOD_CUS_OBJ] = str(dict(Picklist_array).get(SECQSTNATTRIBUTENAME))

			elif SYSEFL_Details.DATA_TYPE == "CHECKBOX":

				if (
					Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)) is not None
					and str(SYSEFL_Details.FLDDEF_VARIABLE_RECORD_ID) == ""
				):

					ATTR_Value = Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).GetValue()
					if ATTR_Value == "1":
						ATTR_Value = "True"
					else:
						ATTR_Value = "False"					
					row[MM_MOD_CUS_OBJ] = str(ATTR_Value)

				elif (
					Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)) is not None
					and str(SYSEFL_Details.FLDDEF_VARIABLE_RECORD_ID) != ""
				):

					FLDDEF_VARIABLE_RECORD_ID = SYSEFL_Details.FLDDEF_VARIABLE_RECORD_ID

					CTX_Logic = Sql.GetFirst(
						"select CPQ_CALCULATION_LOGIC from SYVABL (nolock) where RECORD_ID = '"
						+ str(FLDDEF_VARIABLE_RECORD_ID)
						+ "' "
					)					
					result = ScriptExecutor.ExecuteGlobal(
						"SYPARVRLLG", {"CTXLogic": str(CTX_Logic.CPQ_CALCULATION_LOGIC), "Obj_Name": TABLE_NAME,},
					)
					#Trace.Write("Result 222 " + str(result))
					if result != "":
						ATTR_Value = str(result)
						row[MM_MOD_CUS_OBJ] = str(ATTR_Value)
					# A043S001P01-10678 start

			elif SYSEFL_Details.DATA_TYPE == "FORMULA":				
				OBJD_OBJ = Sql.GetFirst(
					"select PERMISSION from  SYOBJD (nolock) where LOOKUP_API_NAME ='"
					+ str(MM_MOD_CUS_OBJ)
					+ "' and OBJECT_NAME ='"
					+ str(TABLE_NAME).strip()
					+ "' "
				)				
				if OBJD_OBJ is not None and OBJD_OBJ.PERMISSION != "READ ONLY":
					if SYSEFL_Details.FORMULA_LOGIC != "" and "select" in str(SYSEFL_Details.FORMULA_LOGIC).lower():

						SECTIONQSTNRECORDID = str(SYSEFL_Details.RECORD_ID).replace("-", "_").replace(" ", "")
						SECQSTNATTRIBUTENAME = (SECTIONQSTNRECORDID).upper()
						MM_MOD_ATTR_NAME = "QSTN_LKP_" + str(SECQSTNATTRIBUTENAME)
						
						if Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)) is not None:
							API_Value = str(Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).HintFormula)

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
									if str(TABLE_NAME) == 'ACAPCH' and str(row['APPROVAL_CHAIN_RECORD_ID']) and str(API_Name)== 'APROBJ_RECORD_ID':
										API_val_obj = Sql.GetFirst(
											"select APROBJ_RECORD_ID from  ACAPCH (nolock) where APPROVAL_CHAIN_RECORD_ID ='"
											+ str(row['APPROVAL_CHAIN_RECORD_ID'])+ "' "
										)										
										API_Value = str(API_val_obj.APROBJ_RECORD_ID)
								row[API_Name] = str(API_Value)								
								if str(TABLE_NAME) == 'ACAPCH':
									row['APRCHN_ID'] = row['APRCHN_ID'].upper()

								
								if "DATE" in str(API_obj.DATA_TYPE):
									API_Name = "CONVERT(VARCHAR(10)," + API_Name + ", 101)"
									
								result = ScriptExecutor.ExecuteGlobal(
									"SYPARCEFMA", {"Object": TABLE_NAME, "API_Name": str(API_Name), "API_Value": API_Value,},
								)
								
								for API_Names in result:
									API_NAME = str(API_Names["API_NAME"]).strip()
									RESULT = str(API_Names["FORMULA_RESULT"])								
									# A043S001P01-9167 09-04-2020 START
									if str(API_NAME) == "MINIMUM_PRICE":
										currency_Value = Product.Attributes.GetByName(str("QSTN_SYSEFL_PR_00012")).GetValue()
										if str(currency_Value) != "":
											price_decimal_obj = Sql.GetFirst(
												"select SYMBOL,DECIMAL_PLACES,ROUNDING_METHOD from PRCURR (NOLOCK) where CURRENCY='"
												+ str(currency_Value)
												+ "'"
											)
											price_decimal = price_decimal_obj.DECIMAL_PLACES
											if str(price_decimal_obj.ROUNDING_METHOD) == "ROUND":
												
												if RESULT is None or RESULT == "":
													RESULT = 0
												price_decimals = "." + str(price_decimal) + "f"
												decimal_val = format(float(RESULT), price_decimals)
												RESULT = decimal_val
												row[API_NAME] = str(RESULT)
											else:
												multiplier = 10 ** price_decimal
												decimal_val = math.floor(float(RESULT) * multiplier) / multiplier
												RESULT = decimal_val
												row[API_NAME] = str(RESULT)
										else:
											row[API_NAME] = str(RESULT)
									else:
										if str(API_NAME) == str(MM_MOD_CUS_OBJ):
											row[API_NAME] = str(RESULT)

									#Trace.Write("row3:" + str(row))
									# A043S001P01-9167 09-04-2020 END
					elif SYSEFL_Details.FORMULA_LOGIC != "" and "select" not in str(SYSEFL_Details.FORMULA_LOGIC).lower():
						ATTR_Value = str(SYSEFL_Details.FORMULA_LOGIC).strip()	

						row[MM_MOD_CUS_OBJ] = str(ATTR_Value)
					elif SYSEFL_Details.FORMULA_LOGIC == "":						
						ATTR_Value = Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).GetValue()
						row[MM_MOD_CUS_OBJ] = str(ATTR_Value)
				else:					
					ATTR_Value = Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).GetValue()				
					row[MM_MOD_CUS_OBJ] = str(ATTR_Value)					

			elif SYSEFL_Details.DATA_TYPE == "CURRENCY":
				##if the attr Data type is Currency and contains special char,Ignore the Symbol.
				# START---added ignore unicode for PRLPBE----HariniPriya
				if Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)) is not None and TABLE_NAME == "PRLPBE":
					ATTR_Value = Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).GetValue()
					ATTR_Value = ATTR_Value.encode("ASCII", "ignore")
					ATTR_Value = re.sub(r"[A-Za-z ?|$||!|`|~|@|#|%|^|&|*|(|)|_|=|>|<|/]", r"", str(ATTR_Value))

					# A043S001P01-7659 CONVERT TO DECIMAL VALUE RAMESH  STRART
					currency_Value = Product.Attributes.GetByName(str("QSTN_SYSEFL_PB_01467")).GetValue()
					if str(currency_Value) != "":
						price_decimal_obj = Sql.GetFirst(
							"select SYMBOL,DECIMAL_PLACES,ROUNDING_METHOD from PRCURR (NOLOCK) where CURRENCY='"
							+ str(currency_Value)
							+ "'"
						)
						price_decimal = price_decimal_obj.DECIMAL_PLACES
						if str(price_decimal_obj.ROUNDING_METHOD) == "ROUND":						
							if ATTR_Value is None or ATTR_Value == "":
								ATTR_Value = 0
							price_decimals = "." + str(price_decimal) + "f"
							decimal_val = format(float(ATTR_Value), price_decimals)
							ATTR_Value = decimal_val
						else:
							multiplier = 10 ** price_decimal
							decimal_val = math.floor(float(ATTR_Value) * multiplier) / multiplier
							ATTR_Value = decimal_val
					# A043S001P01-7659 CONVERT TO DECIMAL VALUE RAMESH  END
					try:
						row[MM_MOD_CUS_OBJ] = str(ATTR_Value)
					except:
						row[MM_MOD_CUS_OBJ] = str(ATTR_Value)
				elif Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)) is not None and TABLE_NAME != "PRLPBE":
					ATTR_Value = Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).GetValue()
					t = ATTR_Value.split(" ")					
					if len(t) > 1:
						ATTR_Value = ATTR_Value[2:]					
					try:
						row[MM_MOD_CUS_OBJ] = str(ATTR_Value)
					except:
						row[MM_MOD_CUS_OBJ] = str(ATTR_Value)
				# END---added ignore unicode for PRLPBE
			elif str(SYSEFL_Details.DATA_TYPE) == "LONG TEXT AREA":
				MM_MOD_ATTR_NAME = MM_MOD_ATTR_NAME + "_LONG"
				if Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)) is not None:
					ATTR_Value = Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).GetValue()
				try:
					row[MM_MOD_CUS_OBJ] = str(ATTR_Value)
				except:
					row[MM_MOD_CUS_OBJ] = str(ATTR_Value)
			elif (
				SYSEFL_Details.DATA_TYPE != "LOOKUP"
				and SYSEFL_Details.DATA_TYPE != "AUTO NUMBER"
				and SYSEFL_Details.DATA_TYPE != "FORMULA"
				and SYSEFL_Details.DATA_TYPE != "PICKLIST"
				and SYSEFL_Details.DATA_TYPE != "CHECKBOX"
				and SYSEFL_Details.DATA_TYPE != "CURRENCY"
			):
				
				if str(TABLE_NAME) == "MAMTRL" and str(SYSEFL_Details.API_NAME).strip() == "MINIMUM_ORDER_QUANTITY":
					if Product.Attributes.GetByName("QSTN_SYSEFL_MA_05242") is not None:						
						if Product.Attributes.GetByName("QSTN_SYSEFL_MA_05242").GetValue() is not None and ("" or "0"):
							if str(ATTR_Value) == "0" or str(ATTR_Value) == "":
								ATTR_Value = "1"
						try:							
							row[MM_MOD_CUS_OBJ] = str(ATTR_Value)
						except:
							row[MM_MOD_CUS_OBJ] = str(ATTR_Value)

				elif Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)) is not None and (
					SYSEFL_Details.FLDDEF_VARIABLE_RECORD_ID == "" or SYSEFL_Details.FLDDEF_VARIABLE_RECORD_ID is None
				):					
					ATTR_Value = Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).GetValue() or ""
					try:						
						row[MM_MOD_CUS_OBJ] = ATTR_Value
					except:
						row[MM_MOD_CUS_OBJ] = str(ATTR_Value)
				
				elif (
					Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)) is not None
					and SYSEFL_Details.FLDDEF_VARIABLE_RECORD_ID != ""
					and USGB_VAL != 1
				):
					FLDDEF_VARIABLE_RECORD_ID = str(SYSEFL_Details.FLDDEF_VARIABLE_RECORD_ID).strip()

					CTX_Logic = Sql.GetFirst(
						"select CPQ_CALCULATION_LOGIC from SYVABL (nolock) where RECORD_ID = '"
						+ str(FLDDEF_VARIABLE_RECORD_ID)
						+ "' "
					)
					result = ScriptExecutor.ExecuteGlobal(
						"SYPARVRLLG",
						{"CTXLogic": str(CTX_Logic.CPQ_CALCULATION_LOGIC), "Obj_Name": str(TABLE_NAME).strip(),},
					)
					# Trace.Write("Result"+str(result))
					if result != "":
						ATTR_Value = str(result)
						row[MM_MOD_CUS_OBJ] = str(ATTR_Value)
						#Trace.Write("ROW7-----" + str(dict(row)))

		# Changed the logic for A043S001P01-13661 - End
		# Trace.Write("ROW5-----" + str(dict(row)))
		# Trace.Write("TABLE_NAME--" + str(TABLE_NAME))
		# Trace.Write("Auto_col"+str(Auto_col))
		if str(TABLE_NAME) == "cpq_permissions":
			if Product.Attributes.GetByName('QSTN_SYSEFL_SY_00129').GetValue():
				Trace.Write('cpq prpof===')
				nativeProfileUpdate(str(dict(row)))
		is_key_Flag = "FALSE"
		is_required = "FALSE"
		is_Past_Date = "FALSE"
		is_key = Sql.GetFirst(
			"select API_NAME from  SYOBJD where OBJECT_NAME ='" + str(TABLE_NAME) + "'and UPPER(IS_KEY)='TRUE' "
		)		
		if is_key is not None:
			col_name = (is_key.API_NAME).strip()
			if col_name in row:
				unique_val = row[col_name]
				if unique_val is not None and unique_val != "":
					REC_OBJ = Sql.GetFirst("select RECORD_NAME from SYOBJH where OBJECT_NAME ='" + str(TABLE_NAME) + "' ")

					if REC_OBJ :
						Auto_Col = (REC_OBJ.RECORD_NAME).strip()						
						REC_VAL = row[Auto_Col]						
						if REC_VAL != "":
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
							if is_key_table:
								is_key_Flag = "TRUE"								
							else:
								is_key_Flag = "FALSE"
				else:
					is_key_Flag = "TRUE"
		
		if TABLE_NAME == "SYROMA":
			is_key_Flag = "FALSE"
		# Ramesh A043S001P01-6083 START 05-12-11-2019  ADD SEGMENT REQUIRED FIELDS
		SEC_TAB_PAGE_ALERT = ""
		Required_obj = Sql.GetList(
			"select API_NAME,FIELD_LABEL,REQUIRED from  SYOBJD where LTRIM(RTRIM(OBJECT_NAME)) ='"
			+ str(TABLE_NAME)
			+ "'and REQUIRED='TRUE' "
		)
		# Ramesh A043S001P01-6083 END 05-12-11-2019  ADD SEGMENT REQUIRED FIELDS
		Field_Labels = []
		if Required_obj:			
			for x in Required_obj:
				api_name = str(x.API_NAME)
				# Ramesh A043S001P01-6083 START 05-12-11-2019  ADD SEGMENT REQUIRED FIELDS
				SEC_TAB_PAGE_ALERT = str(x.FIELD_LABEL)
				# Ramesh A043S001P01-6083 END 05-12-11-2019  ADD SEGMENT REQUIRED FIELDS			
				if api_name in row and str(api_name) != "":
					API_NAME_val = row[x.API_NAME]					
					if API_NAME_val == "":
						Field_Labels.append(x.FIELD_LABEL)
						is_required = "TRUE"
						# break
					else:
						is_required = "FALSE"

		requiredDict = GetErrorMsg.GetQuestionlevelMessage(TABLE_NAME, row, SEC_REC_ID)
		Trace.Write("Field_Labels" + str(Field_Labels))	
		Trace.Write("requiredDict" + str(requiredDict))		
		Trace.Write(str(is_key_Flag) + "aaaaaaaaa" + str(is_required))
		if is_key_Flag == "TRUE" or is_required == "TRUE" or is_Past_Date == "TRUE":			
			if Product.Attributes.GetByName("SEC_N_TAB_PAGE_ALERT") is not None:
				Product.Attributes.GetByName("SEC_N_TAB_PAGE_ALERT").Allowed = False
				# Ramesh A043S001P01-6083 START 05-12-11-2019  ADD SEGMENT REQUIRED FIELDS
				if len(Field_Labels) == 1:
					Product.Attributes.GetByName("SEC_N_TAB_PAGE_ALERT").HintFormula = ""
					Product.Attributes.GetByName(
						"SEC_N_TAB_PAGE_ALERT"
					).HintFormula = "<div class='col-md-12' id='PageAlert' ><div class='row modulesecbnr brdr' data-toggle='collapse' data-target='#Alert_notifcatio2' aria-expanded='true' >NOTIFICATIONS<i class='pull-right fa fa-chevron-down '></i><i class='pull-right fa fa-chevron-up'></i></div><div  id='Alert_notifcatio2' class='col-md-12  alert-notification  brdr collapse in' ><div  class='col-md-12 alert-danger'  ><label ><img src='/mt/APPLIEDMATERIALS_TST/Additionalfiles/stopicon1.svg' alt='Error'>'{}' is a required field</label></div></div></div>".format(
						str(SEC_TAB_PAGE_ALERT)
					)
					flag = "FALSE"
				elif len(Field_Labels) >1:
					Product.Attributes.GetByName("SEC_N_TAB_PAGE_ALERT").HintFormula = ""
					Product.Attributes.GetByName(
						"SEC_N_TAB_PAGE_ALERT"
					).HintFormula = "<div class='col-md-12' id='PageAlert' ><div class='row modulesecbnr brdr' data-toggle='collapse' data-target='#Alert_notifcatio2' aria-expanded='true' >NOTIFICATIONS<i class='pull-right fa fa-chevron-down '></i><i class='pull-right fa fa-chevron-up'></i></div><div  id='Alert_notifcatio2' class='col-md-12  alert-notification  brdr collapse in' ><div  class='col-md-12 alert-danger'  ><label ><img src='/mt/APPLIEDMATERIALS_TST/Additionalfiles/stopicon1.svg' alt='Error'>ERROR : You will not be able to save your data until all required fields are populated </label></div></div></div>"
					flag = "FALSE"
		elif is_required == "FALSE" and TABLE_NAME == "SYROMA":
			Product.Attributes.GetByName("SEC_N_TAB_PAGE_ALERT").HintFormula = ""
			tableInfo = Sql.GetTable(TABLE_NAME)
			tablerow = row			
			tableInfo.AddRow(tablerow)
			Sql.Upsert(tableInfo)
			sec_view(SEC_REC_ID, TABLE_NAME, Auto_col, Rec_Id_Value)
		else:						
			tableInfo = Sql.GetTable(TABLE_NAME)			
			
			if TABLE_NAME != "COPART":				
				tablerow = row
				tableInfo.AddRow(tablerow)
				Sql.Upsert(tableInfo)
				try:
					if Quote is not None:
						PurchaseOrderNumber = PurchaseOrderDate = CustomerNotes = PaymentTermName = SalesEmployeePhone = ""
						QuoteRecId = Product.Attr('QSTN_SYSEFL_QT_00001').GetValue()	
						SalesPersonValue = Sql.GetFirst("Select PHONE from SAQTIP where QUOTE_RECORD_ID = '"+str(QuoteRecId)+"' and CPQ_PARTNER_FUNCTION = 'SALES EMPLOYEE' AND QTEREV_RECORD_ID = '" + str(quote_revision_record_id) + "'")
						if Product.Attributes.GetByName("QSTN_SYSEFL_QT_01126"):
							PurchaseOrderNumber = Product.Attr('QSTN_SYSEFL_QT_01126').GetValue()
						if Product.Attributes.GetByName("QSTN_SYSEFL_QT_01128"):	
							PurchaseOrderDate = Product.Attr('QSTN_SYSEFL_QT_01128').GetValue()
						if Product.Attributes.GetByName("QSTN_SYSEFL_QT_01392_LONG"):	
							CustomerNotes = Product.Attr('QSTN_SYSEFL_QT_01392_LONG').GetValue()
						if Product.Attributes.GetByName("QSTN_SYSEFL_QT_01124"):	
							PaymentTermName = Product.Attr('QSTN_SYSEFL_QT_01124').GetValue()
						if SalesPersonValue is not None:
							SalesEmployeePhone = SalesPersonValue.PHONE
						Quote.GetCustomField('CustomerPO').Content = str(PurchaseOrderNumber)
						Quote.GetCustomField('CustomerPODate').Content = str(PurchaseOrderDate)
						Quote.GetCustomField('CustomerNotes').Content = str(CustomerNotes)
						Quote.GetCustomField('PaymentTermName').Content = str(PaymentTermName)
						Quote.GetCustomField('SalesEmployeePhone').Content = str(SalesEmployeePhone)
						Quote.Save()
				except:
					pass		

				if TABLE_NAME == "SAQTMT":

					GetquoteID = Sql.GetFirst(
						"SELECT QUOTE_ID,QUOTE_STATUS FROM SAQTMT WHERE MASTER_TABLE_QUOTE_RECORD_ID = '"
						+ str(Rec_Id_Value)
						+ "' AND QTEREV_RECORD_ID = '"
						+ str(quote_revision_record_id)
						+ "'"
					)
					QuoteID = GetquoteID.QUOTE_ID	
					Payment_Term = SqlHelper.GetFirst(" SELECT PAYMENTTERM_NAME FROM SAQTRV (NOLOCK) WHERE QUOTE_RECORD_ID = '"+str(Rec_Id_Value)+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id) + "'")				
					if GetquoteID.QUOTE_STATUS == "APPROVED":						
						result = ScriptExecutor.ExecuteGlobal("QTPOSTACRM", {"QUOTE_ID": QuoteID, 'Fun_type':'cpq_to_crm'})
					Quoteupdate = "UPDATE QT__QTQTMT SET PAYMENTTERM_NAME = '{PaymentTermName}' where MASTER_TABLE_QUOTE_RECORD_ID ='{Rec_Id_Value}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}'".format(PaymentTermName = Payment_Term.PAYMENTTERM_NAME, Rec_Id_Value=Rec_Id_Value,quote_revision_record_id=quote_revision_record_id )
					Sql.RunQuery(Quoteupdate)
					
					# Billing Matrix Notification - Start
					if 'CONTRACT_VALID_FROM' in tablerow and 'CONTRACT_VALID_TO' in tablerow:			
						# Item Covered Object Extendted Price Update - Start
						start_date = datetime.datetime.strptime(tablerow.get('CONTRACT_VALID_FROM'), '%m/%d/%Y')
						end_date = datetime.datetime.strptime(tablerow.get('CONTRACT_VALID_TO'), '%m/%d/%Y')			
						diff1 = end_date - start_date

						avgyear = 365.2425        # pedants definition of a year length with leap years
						avgmonth = 365.2425/12.0  # even leap years have 12 months
						years, remainder = divmod(diff1.days, avgyear)
						years, months = int(years), int(remainder // avgmonth)   
						if months > 0:
							years += 1
						if years:
							extented_price = " + ".join(["CASE WHEN ISNULL(SALES_PRICE, 0) = 0 THEN 100 ELSE ISNULL(YEAR_{Year}, 0) END".format(Year=year) for year in range(1, years+1)])
						else:
							extented_price = "CASE WHEN ISNULL(SALES_PRICE, 0) = 0 THEN 100 ELSE 0 END"	
						items_covered_object_query = "UPDATE SAQICO SET EXTENDED_PRICE = {ExtendedPrice} WHERE QUOTE_RECORD_ID ='{QuoteRecordId}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}'".format(ExtendedPrice=extented_price,QuoteRecordId=Rec_Id_Value,quote_revision_record_id=quote_revision_record_id)
						Sql.RunQuery(items_covered_object_query)
						
						# Sql.RunQuery("""UPDATE SAQITM
						# 				SET EXTENDED_PRICE = SAQICO.EXTENDED_PRICE
						# 				FROM SAQITM
						# 				JOIN (SELECT 											
						# 						ISNULL(SUM(ISNULL(EXTENDED_PRICE, 0)), 0) as EXTENDED_PRICE, QUOTE_RECORD_ID, SERVICE_ID										
						# 						FROM SAQICO (NOLOCK) 
						# 						WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}'
						# 						GROUP BY SERVICE_ID, QUOTE_RECORD_ID) 
						# 				AS SAQICO ON SAQICO.QUOTE_RECORD_ID = SAQITM.QUOTE_RECORD_ID AND SAQICO.SERVICE_ID = SAQITM.SERVICE_ID
						# 				""".format(QuoteRecordId=Rec_Id_Value,quote_revision_record_id=quote_revision_record_id)
						# 			)
						# Sql.RunQuery("""UPDATE QT__QTQITM
						# 				SET EXTENDED_UNIT_PRICE = SAQITM.EXTENDED_PRICE, UNIT_PRICE = SAQITM.EXTENDED_PRICE
						# 				FROM QT__QTQITM
						# 				JOIN SAQITM ON SAQITM.QUOTE_RECORD_ID = QT__QTQITM.QUOTE_RECORD_ID 
						# 								AND SAQITM.SERVICE_ID = QT__QTQITM.SERVICE_ID
						# 								AND SAQITM.LINE_ITEM_ID = QT__QTQITM.ITEM_LINE_ID
						# 				WHERE QT__QTQITM.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQITM.QTEREV_RECORD_ID = '{quote_revision_record_id}'""".format(QuoteRecordId=Rec_Id_Value,quote_revision_record_id=quote_revision_record_id)
						# 			)
						
						#Sql.RunQuery("""UPDATE QT__QTQICO
						#				SET EXTENDED_PRICE = QTQICO.EXTENDED_PRICE
						#				FROM QT__QTQICO
						#				JOIN QTQICO ON QTQICO.QUOTE_RECORD_ID = QT__QTQICO.QUOTE_RECORD_ID 
						#								AND QTQICO.SERVICE_ID = QT__QTQICO.SERVICE_ID
						#								AND QTQICO.EQUIPMENT_ID = QT__QTQITM.EQUIPMENT_ID
						#								AND QTQICO.ITEM_LINE_ID = QT__QTQITM.ITEM_LINE_ID
						#								AND QTQICO.EQUIPMENT_LINE_ID = QT__QTQITM.EQUIPMENT_LINE_ID
						#				WHERE QT__QTQICO.QUOTE_RECORD_ID = '{QuoteRecordId}'""".format(QuoteRecordId=Rec_Id_Value)
						#			)

						# Item Covered Object Extendted Price Update - End			
						date_diff_obj = Sql.GetFirst("""SELECT DATEDIFF(day, SAQTMT.CONTRACT_VALID_FROM, SAQRIB.BILLING_START_DATE) as START_DATE_DIFF, 
										DATEDIFF(day, SAQTMT.CONTRACT_VALID_TO, SAQRIB.BILLING_END_DATE) as END_DATE_DIFF, QUOTE_BILLING_PLAN_RECORD_ID
										FROM SAQRIB (NOLOCK) JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQRIB.QUOTE_RECORD_ID 
										WHERE SAQRIB.QUOTE_RECORD_ID = '{}' AND SAQRIB.QTEREV_RECORD_ID = '{}'""".format(Rec_Id_Value,quote_revision_record_id))
						if date_diff_obj:
							if date_diff_obj.START_DATE_DIFF or date_diff_obj.END_DATE_DIFF:						
								billing_query = "UPDATE SAQRIB SET IS_CHANGED = 1, BILLING_START_DATE = '{}', BILLING_END_DATE = '{}' WHERE QUOTE_BILLING_PLAN_RECORD_ID ='{}'".format(tablerow.get('CONTRACT_VALID_FROM'), tablerow.get('CONTRACT_VALID_TO'), date_diff_obj.QUOTE_BILLING_PLAN_RECORD_ID)
								Sql.RunQuery(billing_query)
					# Billing Matrix Notification - End
					
					# Approval Trigger - Start		
					# if tablerow.get('PAYMENTTERM_NAME'):				
					# 	import ACVIORULES
					# 	violationruleInsert = ACVIORULES.ViolationConditions()
					# 	header_obj = Sql.GetFirst("SELECT RECORD_ID FROM SYOBJH (NOLOCK) WHERE OBJECT_NAME = 'SAQTMT'")
					# 	if header_obj:									
					# 		violationruleInsert.InsertAction(
					# 										header_obj.RECORD_ID, Rec_Id_Value, "SAQTMT"
					# 										)
					# Approval Trigger - End
				Trace.Write("row ================> " + str(row))
				Trace.Write("TABLE_NAME ================> " + str(TABLE_NAME))

				sec_view(SEC_REC_ID, TABLE_NAME, Auto_col, Rec_Id_Value)
	return str(flag), str(flag_return), str(requiredDict), (dict(Picklist_array))


def sec_cancel(SEC_REC_ID):

	current_prod = Product.Name
	Trace.Write("current_prod" + str(current_prod))

	CurrentModuleObj = Sql.GetFirst("select * from SYAPPS (NOLOCK) where APP_LABEL = '" + str(current_prod) + "'")
	crnt_prd_val = str(CurrentModuleObj.APP_ID)
	

	Read_Source = "FALSE"
	Product.Attributes.GetByName("MA_MTR_TAB_ACTION").AssignValue("VIEW")

	# A043S001P01-6040 START
	if str(SEC_REC_ID) == "":
		Read_Source = "TRUE"
		SEC_REC_ID = Product.GetGlobal("SEC_REC_ID")
	# A043S001P01-6040 END
	Data_Val = ""
	Trace.Write("-------" + str(Data_Val))
	Trace.Write("SEC_REC_ID" + str(SEC_REC_ID))
	Rec_Id_Value = ""
	Product_code = SEC_REC_ID.split("-")
	Product_code = crnt_prd_val
	
	# SQL_OBJ = Sql.GetFirst(
	# 	"Select API_NAME from SYSEFL with (nolock)  where RTRIM(LTRIM(SECTION_RECORD_ID))='" + SEC_REC_ID + "'"
	# )
	SQL_OBJ = Sql.GetList(
		" SELECT MQ.SAPCPQ_ATTRIBUTE_NAME as RECORD_ID,  MQ.API_FIELD_NAME as API_NAME, MQ.FLDDEF_VARIABLE_RECORD_ID, MD.DATA_TYPE, MD.PERMISSION, MD.REQUIRED,"
		+ " MD.IS_KEY, MD.OBJECT_NAME, MD.FORMULA_LOGIC FROM SYSEFL (NOLOCK) MQ"
		+ " INNER JOIN  SYOBJD (NOLOCK) MD ON MQ.API_FIELD_NAME = MD.API_NAME AND MD.OBJECT_NAME = MQ.API_NAME WHERE  MQ.SECTION_RECORD_ID='"
		+ str(SEC_REC_ID)
		+ "' "
	)
	if SQL_OBJ is not None:
		for SYSEFL_Details in SQL_OBJ:
			TABLE_NAME = str(SYSEFL_Details.OBJECT_NAME)
		#TABLE_NAME = str(SQL_OBJ.API_NAME)
		# Auto No field
		#TABLE_NAME = ""
			REC_ID_OBJ = Sql.GetFirst(
				"Select RECORD_ID,RECORD_NAME from SYOBJH with (nolock)  where RTRIM(LTRIM(OBJECT_NAME))='" + TABLE_NAME + "'"
			)		
			for SYSEFL_Details in SQL_OBJ:
				TABLE_NAME = str(SYSEFL_Details.OBJECT_NAME)
				if REC_ID_OBJ is not None:
					Auto_col = str(REC_ID_OBJ.RECORD_NAME).strip()
					# Trace.Write(
					# 	"Select SAPCPQ_ATTRIBUTE_NAME,RECORD_ID from SYSEFL where API_NAME='"
					# 	+ Auto_col
					# 	+ "' and API_NAME='"
					# 	+ TABLE_NAME
					# 	+ "' and SAPCPQ_ATTRIBUTE_NAME like '%SYSECT-"
					# 	+ str(crnt_prd_val)
					# 	+ "%'"
					# )
					# QUE_OBJ = Sql.GetFirst(
					# 	"Select SAPCPQ_ATTRIBUTE_NAME,RECORD_ID from SYSEFL  with (nolock)  where API_FIELD_NAME='"
					# 	+ Auto_col
					# 	+ "' and API_NAME='"
					# 	+ TABLE_NAME
					# 	+ "'"
					# )
					QUE_OBJ = Sql.GetFirst(
						"SELECT SYSEFL.SAPCPQ_ATTRIBUTE_NAME from SYSEFL (nolock) INNER JOIN SYSECT (NOLOCK) ON SYSECT.RECORD_ID = SYSEFL.SECTION_RECORD_ID INNER JOIN SYPAGE (NOLOCK) on SYSECT.PAGE_RECORD_ID = SYPAGE.RECORD_ID where SYSEFL.API_FIELD_NAME='"
						+ str(Auto_col)
						+ "' and SYSEFL.API_NAME='"
						+ str(TABLE_NAME)
						+ "' and SYSEFL.SAPCPQ_ATTRIBUTE_NAME like '%"
						+ str(Product_code)
						+ "%' AND SYPAGE.TAB_RECORD_ID!='' "
					)
			# if TABLE_NAME == "SYTABS":
			#     Trace.Write("come ========")
			#     QUE_OBJ = Sql.GetFirst(
			#         "Select SAPCPQ_ATTRIBUTE_NAME,RECORD_ID from SYSEFL  with (nolock)  where API_NAME='"
			#         + TABLE_NAME
			#         + "' and SECTION_RECORD_ID = '"
			#         + str(SEC_REC_ID)
			#         + "'"
			#     )
			#     Trace.Write(
			#         "Select SAPCPQ_ATTRIBUTE_NAME,RECORD_ID from SYSEFL  with (nolock)  where API_NAME='"
			#         + TABLE_NAME
			#         + "' and SECTION_RECORD_ID = '"
			#         + str(SEC_REC_ID)
			#         + "'"
			#     )
			# else:
			#     Trace.Write("else----------00000")
			#     QUE_OBJ = Sql.GetFirst(
			#         "Select SAPCPQ_ATTRIBUTE_NAME,RECORD_ID from SYSEFL  with (nolock)  where API_FIELD_NAME='"
			#         + Auto_col
			#         + "' and API_NAME='"
			#         + TABLE_NAME
			#         + "'"
			#     )

					if QUE_OBJ is not None:						
						RECORDID = str(QUE_OBJ.SAPCPQ_ATTRIBUTE_NAME).replace("-", "_").replace(" ", "")
						ATTRIBUTENAME = (RECORDID).upper()
						Auto_Field = "QSTN_" + str(ATTRIBUTENAME).strip()						
						if Product.Attributes.GetByName(str(Auto_Field)) is not None:					
							Rec_Id_Value = Product.Attributes.GetByName(str(Auto_Field)).GetValue()

						
						if Rec_Id_Value != "":							
							Data_Val = Sql.GetFirst(
								"Select * from "
								+ str(TABLE_NAME)
								+ " with (nolock) where "
								+ str(Auto_col)
								+ "='"
								+ str(Rec_Id_Value)
								+ "'"
							)

							
	if Read_Source == "TRUE":		
		SYSEFL_OBJNAME = Sql.GetList(
			" SELECT  MQ.SAPCPQ_ATTRIBUTE_NAME, MQ.RECORD_ID, MQ.API_FIELD_NAME as API_NAME , MQ.FLDDEF_VARIABLE_RECORD_ID, MD.DATA_TYPE, MD.PERMISSION, MD.REQUIRED,"
			+ " MD.IS_KEY, MD.OBJECT_NAME, MD.FORMULA_LOGIC FROM SYSEFL (NOLOCK) MQ"
			+ " INNER JOIN  SYOBJD (NOLOCK) MD ON MQ.API_FIELD_NAME = MD.API_NAME AND MD.OBJECT_NAME = MQ.API_NAME"
			+ " WHERE  MD.OBJECT_NAME='"
			+ str(TABLE_NAME)
			+ "'"
		)

	else:		
		SYSEFL_OBJNAME = Sql.GetList(
			" SELECT  MQ.SAPCPQ_ATTRIBUTE_NAME, MQ.RECORD_ID, MQ.API_FIELD_NAME as API_NAME, MQ.FLDDEF_VARIABLE_RECORD_ID,MQ.DISPLAY_ORDER, MD.DATA_TYPE, MD.PERMISSION, MD.REQUIRED,"
			+ " MD.IS_KEY, MD.OBJECT_NAME, MD.FORMULA_LOGIC FROM SYSEFL (NOLOCK) MQ"
			+ " INNER JOIN  SYOBJD (NOLOCK) MD ON MQ.API_FIELD_NAME = MD.API_NAME AND MD.OBJECT_NAME = MQ.API_NAME"
			+ " WHERE MQ.SECTION_RECORD_ID='"
			+ str(SEC_REC_ID)
			+ "'"
		)
	if SYSEFL_OBJNAME is not None:
		for SYSEFL_Details in SYSEFL_OBJNAME:
			DATA_TYPE = str(SYSEFL_Details.DATA_TYPE)
			SECTIONQSTNRECORDID = str(SYSEFL_Details.SAPCPQ_ATTRIBUTE_NAME).replace("-", "_").replace(" ", "")
			SECQSTNATTRIBUTENAME = (SECTIONQSTNRECORDID).upper()
			MM_MOD_ATTR_NAME = "QSTN_" + str(SECQSTNATTRIBUTENAME)
			
			MM_MOD_CUS_OBJ = ""			
			if Data_Val is not None:
				
				try:					
					MM_MOD_CUS_OBJ = eval(str("Data_Val." + str(SYSEFL_Details.API_NAME)).strip())
					
				except:					
					MM_MOD_CUS_OBJ = (
						eval("Data_Val." + str(SYSEFL_Details.API_NAME).strip()).decode("unicode_escape").encode("utf-8")
					)
					
			if DATA_TYPE == "AUTO NUMBER" and Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)) is not None:

				Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).DisplayType = "FreeInputNoMatching"
				Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).Allowed = True
				Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).AssignValue(str(MM_MOD_CUS_OBJ))
				Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).Access = AttributeAccess.ReadOnly

			elif DATA_TYPE == "PICKLIST" and Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)) is not None:				
				try:
					Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).SelectDisplayValues(MM_MOD_CUS_OBJ)
					Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).Access = AttributeAccess.ReadOnly					
				except:
					Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).SelectDisplayValues(str(MM_MOD_CUS_OBJ))
					Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).Access = AttributeAccess.ReadOnly					

			elif (
				DATA_TYPE == "CHECKBOX"
				and Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)) is not None
				and Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)) != ""
			):

				if str(MM_MOD_CUS_OBJ).upper() == "TRUE" or str(MM_MOD_CUS_OBJ) == "1":
					Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).SelectDisplayValue("1")
					Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).Access = AttributeAccess.ReadOnly
				else:
					Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).SelectDisplayValue("0")
					Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).Access = AttributeAccess.ReadOnly

			elif DATA_TYPE == "FORMULA" and Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)) is not None:
				Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).AssignValue(str(MM_MOD_CUS_OBJ))
				Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).Access = AttributeAccess.ReadOnly

				RECORDID = str(SYSEFL_Details.SAPCPQ_ATTRIBUTE_NAME).replace("-", "_").replace(" ", "").upper()
				MOD_ATTR_NAME = "QSTN_LKP_" + str(RECORDID)				
				if Product.Attributes.GetByName(str(MOD_ATTR_NAME)):
					Product.Attributes.GetByName(str(MOD_ATTR_NAME)).Allowed = False
					Product.Attributes.GetByName(str(MOD_ATTR_NAME)).Access = 0
					
				try:
					OBJD_OBJ = Sql.GetFirst(
						"select API_NAME from  SYOBJD (nolock) where LTRIM(RTRIM(DATA_TYPE))='LOOKUP' and LTRIM(RTRIM(OBJECT_NAME))='"
						+ str(TABLE_NAME).strip()
						+ "' and LTRIM(RTRIM(LOOKUP_API_NAME)) = '"
						+ str(SYSEFL_Details.API_NAME).strip()
						+ "' "
					)
					if OBJD_OBJ is not None:
						MOD_CUS_OBJ = eval(str("SQLobj." + str(OBJD_OBJ.API_NAME)))					
						if Product.Attributes.GetByName(str(MOD_ATTR_NAME)) is not None and MOD_CUS_OBJ != "":
							Product.Attributes.GetByName(str(MOD_ATTR_NAME)).HintFormula = str(MOD_CUS_OBJ)
						elif Product.Attributes.GetByName(str(MOD_ATTR_NAME)) is not None:
							Product.Attributes.GetByName(str(MOD_ATTR_NAME)).HintFormula = ""
				except:
					Trace.Write("ERROR")

			elif DATA_TYPE == "LOOKUP" and Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)) is not None:
				Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).AssignValue(str(MM_MOD_CUS_OBJ))
				Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).Access = AttributeAccess.ReadOnly

			elif DATA_TYPE == "LONG TEXT AREA":				
				MM_MOD_ATTR_NAME = MM_MOD_ATTR_NAME + "_LONG"
				try:
					Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).AssignValue(MM_MOD_CUS_OBJ)
					Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).Access = AttributeAccess.ReadOnly
				except:
					Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).AssignValue(str(MM_MOD_CUS_OBJ))
					Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).Access = AttributeAccess.ReadOnly

			elif Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)) is not None:			
				try:
					Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).AssignValue(MM_MOD_CUS_OBJ)
					Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).Access = AttributeAccess.ReadOnly
				except:
					Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).AssignValue(str(MM_MOD_CUS_OBJ))
					Product.Attributes.GetByName(str(MM_MOD_ATTR_NAME)).Access = AttributeAccess.ReadOnly

	return "true"


def save(SEC_REC_ID, RECORDS_VAL, TABLE_NAME):
	newdict = {}
	Sql = SQL()
	# newdict["CPQTABLEENTRYADDEDBY"] = User.UserName
	# newdict["CPQTABLEENTRYMODIFIEDBY"] = User.Id
	# newdict["CPQTABLEENTRYDATEADDED"] = Modified_date
	# newdict["CPQTABLEENTRYDATEMODIFIED"] = Modified_date
	RECORD = eval(RECORDS_VAL)
	Trace.Write("record-------------------700" + str(RECORD))
	TABLEID = str(TABLE_NAME).replace("collapse in", "")
	Trace.Write("TABLEID---702" + str(TABLEID))
	flag_return = "FALSE"
	TABLEID = TABLEID[:6]
	# Trace.Write("RECORDS_VAL"+str(dict(RECORDS_VAL)))

	OBJH_OBJ = Sql.GetFirst("select RECORD_NAME from SYOBJH where OBJECT_NAME='" + str(TABLEID) + "' ")	
	# Added by VETRI for #A043S001P01-7065 - Start

	if OBJH_OBJ is not None:
		KEY_ID = keyid.KeyCPQId.GetKEYId(str(TABLEID), str(RECORD[str(OBJH_OBJ.RECORD_NAME)]))
		RECID = KEY_ID		
		RECORD.update({str(OBJH_OBJ.RECORD_NAME): str(RECID)})
		TABLE_OBJ = Sql.GetFirst(
			"SELECT * FROM " + TABLEID + " WHERE " + str(OBJH_OBJ.RECORD_NAME) + " ='" + str(RECID) + "'"
		)
		OBJD_OBJ = Sql.GetList("SELECT API_NAME FROM  SYOBJD WHERE OBJECT_NAME='" + str(TABLEID) + "'")
	if TABLE_OBJ is not None:
		for attr in OBJD_OBJ:
			for KEY in RECORD:
				if str(attr.API_NAME) == KEY:
					newdict[attr.API_NAME] = RECORD[KEY]
		dictc = {"CpqTableEntryId": str(TABLE_OBJ.CpqTableEntryId)}
		newdict.update(dictc)
		#Trace.Write(str(SEC_REC_ID) + "  --------111111111111-------->" + str(newdict))
		tableInfo = Sql.GetTable(TABLEID)
		tablerow = newdict
		tableInfo.AddRow(tablerow)
		Sql.Upsert(tableInfo)

	Trace.Write("flag_return" + str(flag_return))
	return str(flag_return)


x = datetime.datetime.now()

SEC_REC_ID = Param.SECTION_REC_ID
ACTION = Param.ACTION

try:
	Picklist_array = Param.Picklist_array
except:
	Picklist_array = ""
try:
	quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
except:
	quote_revision_record_id = ""

if ACTION.strip() == "EDIT":
	Trace.Write("EDITTTTTTTTTTTTTTTT")
	ApiResponse = ApiResponseFactory.JsonResponse(sec_edit(SEC_REC_ID))
elif ACTION == "SAVE":
	Trace.Write("SAVEEEEEEEEEEEEEEEE")
	ATTR_VAL = Param.ATTR_VAL
	Trace.Write("ATTR_VAL" + str(ATTR_VAL))
	ApiResponse = ApiResponseFactory.JsonResponse(sec_save(SEC_REC_ID, ATTR_VAL, Picklist_array))
elif ACTION == "CANCEL":
	Trace.Write("CANCELLLLLLLLLLLLLL")
	ApiResponse = ApiResponseFactory.JsonResponse(sec_cancel(SEC_REC_ID))
elif ACTION == "SEC_SAVE":
	Trace.Write("SAVEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
	RECORDS_VAL = Param.RECORD
	TABLE_NAME = Param.TABLE_NAME
	Trace.Write("TABLE_NAME-----45680" + str(TABLE_NAME))
	ApiResponse = ApiResponseFactory.JsonResponse(save(SEC_REC_ID, RECORDS_VAL, TABLE_NAME))


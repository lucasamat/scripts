# =========================================================================================================================================
#   __script_name : SYULODTRND.PY
#   __script_description : THIS SCRIPT IS USED TO LOAD THE RIGHT HAND SIDE PAGE CONTENT WHEN CLICKING ON A LEFT HAND SIDE TREE NODE.
#   __primary_author__ : ASHA LYSANDAR
#   __create_date : 26/08/2020
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
# pylint: noqa: E501
# pylint: disable=unused-variable
import Webcom.Configurator.Scripting.Test.TestProduct
Trace = Trace  # pylint: disable=E0602
Webcom = Webcom  # pylint: disable=E0602
Product = Product  # pylint: disable=E0602
# User = User  # pylint: disable=E0602
Session = Session  # pylint: disable=E0602
Param = Param  # pylint: disable=E0602
ScriptExecutor = ScriptExecutor  # pylint: disable=E0602
ApiResponseFactory = ApiResponseFactory  # pylint: disable=E0602
# pylint: disable = no-name-in-module, import-error, multiple-imports, pointless-string-statement, wrong-import-order
#import CQENTIFLOW

import re
import SYTABACTIN as Table
import SYCNGEGUID as CPQID
from SYDATABASE import SQL
#import SYERRMSGVL as GetErrorMsg
import System.Net
import datetime
from datetime import datetime

import time
Sql = SQL()
userId = str(User.Id)
userName = str(User.UserName)
gettodaydate = datetime.now().strftime("%Y-%m-%d")
#gettodaydate = datetime.datetime.now().strftime("%Y-%m-%d")
#datetime_value = datetime.datetime.now()
def CommonTreeViewHTMLDetail(
	MODE, TableId, RECORD_ID, TreeParam, NEWVAL, LOOKUPOBJ, LOOKUPAPI, SECTION_EDIT, Flag, ObjectName, SectionList,LEGALSOW,
):	
	try:
		current_prod = Product.Name
	except:
		current_prod = "Sales"
	Trace.Write("RECORD_ID---->"+str(RECORD_ID))
	TestProduct = Webcom.Configurator.Scripting.Test.TestProduct()
	CurrentModuleObj = Sql.GetFirst("select * from SYAPPS (NOLOCK) where APP_LABEL = '" + str(current_prod) + "'")
	quote_revision_record_id = ""
	if current_prod != 'APPROVAL CENTER':
		quote_record_id = Quote.GetGlobal("contract_quote_record_id")
		quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
	if CurrentModuleObj:
		crnt_prd_val = str(CurrentModuleObj.APP_ID)
	TreeParentParam = Product.GetGlobal("TreeParentLevel0")
	TreeSuperParentParam = Product.GetGlobal("TreeParentLevel1")
	TreeParam = Product.GetGlobal("TreeParam")
	TreeTopSuperParentParam = Product.GetGlobal("TreeParentLevel2")
	sec_str = getyears = ""
	sec_bnr = ""
	Second_Banner_Name = ""
	Chkctry = ""
	canedit = ""

	auto_field = ""
	date_field = []
	primary_value = RECORD_ID

	Product.SetGlobal('get_quote_item_service',primary_value)
	Trace.Write(str(ObjectName)+"---ObjectName-----Recordid"+str(primary_value))
	if str(ObjectName) == "SAQSGB" or str(ObjectName) == "SAQRGG":
		Product.SetGlobal('addon_prd_rec_id',primary_value)
	try:
		CurrentTab = TestProduct.CurrentTab
	except:
		CurrentTab = 'Quotes'    
	#TableName = primary_value.split("-")
	LOOKUPOBJ = LOOKUPOBJ.replace("table_", "")
	objr_obj_id = spare_parts_visibility = ""
	new_value_dict = {}
	api_name = ""
	
	tablistdict = {}
	par_obj_id = ""
	action_visible_str = contract_quote_record_id = ""
	queryStr = ""
	add_style = ""
	if Product.GetGlobal("TreeParentLevel0") == 'Sending Equipment':
		ObjectName = "SAQSSF"
		SectionList = ["CD4AEEE6-54EC-4C7A-8103-F9D76843632B","A88CBAD1-1EC2-43A4-A953-FF100D9D89CF"]
	Account_Id_Query = Sql.GetFirst("SELECT PARTY_ID, PARTY_NAME FROM SAQTIP (NOLOCK) WHERE QUOTE_INVOLVED_PARTY_RECORD_ID = '"+str(primary_value)+"'")
	if Account_Id_Query:
		Account_Id = Account_Id_Query.PARTY_ID
		Account_Name = Account_Id_Query.PARTY_NAME		
		Product.SetGlobal("stp_account_id", str(Account_Id))
		Product.SetGlobal("stp_account_name", str(Account_Name))
	if SectionList is not None and len(SectionList) > 0:		
		sectionId = tuple(SectionList)
		queryStr = " AND SYSECT.RECORD_ID IN " + str(sectionId)		
	# Billing Matrix Details Load - Start
	quote_record_id = None
	if ObjectName == 'SAQRIB':
		quote_record_id = Product.GetGlobal("contract_quote_record_id")
	elif ObjectName == 'SAQSAF':
		sending_fab_object = Sql.GetFirst("SELECT SNDFBL_ID FROM SAQSAF (NOLOCK) WHERE QUOTE_REV_SENDING_ACC_FAB_LOCATION_RECORD_ID = '"+str(primary_value)+"'")
		if sending_fab_object:
			Product.SetGlobal("sending_fab_id", str(sending_fab_object.SNDFBL_ID))
	elif ObjectName == 'SAQFBL':
		receiving_fab_object = Sql.GetFirst("SELECT FABLOCATION_ID FROM SAQFBL (NOLOCK) WHERE QUOTE_FABLOCATION_RECORD_ID = '"+str(primary_value)+"'")
		if receiving_fab_object:
			Product.SetGlobal("receiving_fab_id", str(receiving_fab_object.SNDFBL_ID))
			
	# Billing Matrix Details Load - End
	
	#getyear calculatin start
	try:
		contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
	except:
		pass #to handle error while we are in system admin
	Getyear = Sql.GetFirst("select CONTRACT_VALID_FROM,CONTRACT_VALID_TO from SAQTMT where MASTER_TABLE_QUOTE_RECORD_ID = '"+str(contract_quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' ")
	if Getyear:
		start_date = datetime(Getyear.CONTRACT_VALID_FROM)
		end_date = datetime(Getyear.CONTRACT_VALID_TO)
		mm = (end_date. year - start_date. year) * 12 + (end_date. month - start_date. month)
		quotient, remainder = divmod(mm, 12)
		getyears = quotient + (1 if remainder > 0 else 0)		
		if not getyears:
			getyears = 1

	#getyear end
	#getQuotetype = Product.Attributes.GetByName("QSTN_SYSEFL_QT_00723").GetValue()

	if ObjectName == 'SYPAGE' and CurrentTab == 'Tab':
		#GetRec = Sql.GetFirst("SELECT SYPAGE.RECORD_ID FROM SYPAGE (NOLOCK) INNER JOIN SYTABS (NOLOCK) ON SYPAGE.TAB_NAME = SYTABS.TAB_LABEL WHERE SYTABS.RECORD_ID = '{}' AND SYPAGE.PAGE_NAME = '{}'".format(Product.GetGlobal("TabId"),TreeParam))
		GetRec = Sql.GetFirst("SELECT SYPAGE.RECORD_ID FROM SYPAGE (NOLOCK) INNER JOIN SYTABS (NOLOCK) ON SYPAGE.TAB_NAME = SYTABS.TAB_LABEL WHERE SYTABS.RECORD_ID = '{}'".format(str(Product.Attributes.GetByName("QSTN_SYSEFL_SY_03295").GetValue()) ))
		RECORD_ID = str(GetRec.RECORD_ID)
	if TableId is not None and  (ObjectName is None or str(ObjectName.isdigit()) == 'True'):	

		objr_obj = Sql.GetFirst("select * FROM SYOBJR WITH (NOLOCK) where SAPCPQ_ATTRIBUTE_NAME = '" + str(TableId) + "' ")		
		if objr_obj is not None:
			objr_obj_id = str(objr_obj.OBJ_REC_ID)
			par_obj_id = str(objr_obj.PARENT_LOOKUP_REC_ID)			
			canedit = str(objr_obj.CAN_EDIT)
		if objr_obj_id is not None and str(objr_obj_id) != "":
			objh_obj = Sql.GetFirst("select * FROM SYOBJH WITH (NOLOCK) where RECORD_ID = '" + str(objr_obj_id) + "' ")			

			if objh_obj is not None:
				ObjectName = str(objh_obj.OBJECT_NAME)
				
	if str(ObjectName) in ["ACAPCH","SYPRAP", "SAQIBP","SAQTBP","SAQRIB","SASORG","PREXRT","SYTABS","ACACSS","ACACST","ACACSA","cpq_permissions","SYOBJD","SYPRTB","SYPSAC","SYPRSN","SYAPPS","SYOBJC","SYSECT","USERS","SYSEFL","SYPROH","SAQTMT","PRCURR","SYROMA","SYPGAC","SAQTIP","SYOBJX","SYPRSF","SYROUS","SYOBFD","SYPRAC","SAQSCO","SAQTRV","SAQTSV","SAQSFB","SAQSGB","SAQDOC"]:
			canedit = "TRUE"
	if Product.GetGlobal("TreeParentLevel0") == "Billing":
		ObjectName = "SAQRIB"
	if TableId == "SYOBJR-95824" and str(TreeParentParam == "Fields and Relationships") and (current_prod == "SYSTEM ADMIN"):		
		ObjectName = "SYOBJD"
		if str(CurrentTab == "Object"):
			canedit = "TRUE"
	if Flag == 1 and MODE != "EDIT":		
		if (
					
			str(ObjectName) != "USERS"
			and str(ObjectName) != "SYSECT"
			and str(ObjectName) != "SYOBJD"
			and str(ObjectName) != "SYOBJH"
			and str(ObjectName) != "SYOBJC"
			and str(ObjectName) != "SYOBJX"
			
			and str(ObjectName) != "SYSEFL"
		):
			try:
				if RECORD_ID.startswith(ObjectName):					
					RECORD_ID = CPQID.KeyCPQId.GetKEYId(str(ObjectName), str(RECORD_ID))
			except:
				Trace.Write('check error')	

	if MODE == "EDIT":		
		if str(ObjectName) == "USERS":
			RECORD_ID
		else:
			RECORD_ID = CPQID.KeyCPQId.GetKEYId(str(ObjectName), str(RECORD_ID))
			Trace.Write(str(ObjectName)+"@170---ObjectName-----Recordid"+str(RECORD_ID))

	elif MODE == "EDIT_CLEAR":
		MODE = "EDIT"
	elif MODE == "CANCEL" :
		if str(ObjectName) == "SYTABS":
			if ObjectName in RECORD_ID:
				RECORD_ID = CPQID.KeyCPQId.GetKEYId(str(ObjectName), str(RECORD_ID))
		else:
			try:
				if RECORD_ID.startswith(ObjectName):
					RECORD_ID = CPQID.KeyCPQId.GetKEYId(str(ObjectName), str(RECORD_ID))
			except:
				Trace.Write('check error')
	elif MODE == "BREADCRUMB":		
		try:
			if RECORD_ID.startswith(ObjectName):
				RECORD_ID = CPQID.KeyCPQId.GetKEYId(str(ObjectName), str(RECORD_ID))
		except:
			Trace.Write('check error')
	else:
		MODE = "VIEW"

	
	
	Sqq_obj = Sql.GetList(
		"SELECT top 1000 API_NAME, DATA_TYPE, LOOKUP_OBJECT, PERMISSION, REQUIRED, LOOKUP_API_NAME, FIELD_LABEL,SOURCE_DATA FROM  SYOBJD WITH (NOLOCK) WHERE OBJECT_NAME='"
		+ str(ObjectName)
		+ "' ORDER BY abs(DISPLAY_ORDER)"
	)
	lookup_val = [val.LOOKUP_API_NAME for val in Sqq_obj]
	lookup_list = {ins.LOOKUP_API_NAME: ins.LOOKUP_OBJECT for ins in Sqq_obj}
	lookup_list1 = {ins.LOOKUP_API_NAME: ins.API_NAME for ins in Sqq_obj}
	
	if NEWVAL != "":		
		if str(LOOKUPOBJ) == "CLEAR SELECTION":
			attrval_obj = Sql.GetFirst(
				"SELECT API_NAME FROM  SYOBJD WITH (NOLOCK) WHERE OBJECT_NAME='"
				+ str(ObjectName)
				+ "' AND LOOKUP_OBJECT='"
				+ str(NEWVAL)
				+ "'"
			)
			api_name = attrval_obj.API_NAME.strip()
			TABLE_OBJS = Sql.GetList(
				"select OBJECT_NAME,API_NAME,DATA_TYPE,LOOKUP_OBJECT,FORMULA_LOGIC FROM  SYOBJD WITH (NOLOCK) where OBJECT_NAME ='"
				+ str(ObjectName)
				+ "' and FORMULA_LOGIC like '%"
				+ str(api_name)
				+ "%'"
			)
			if TABLE_OBJS is not None:
				for TABLE_OBJ in TABLE_OBJS:
					if TABLE_OBJ.DATA_TYPE != "":
						DATA_TYPE = str(TABLE_OBJ.DATA_TYPE)
						if api_name in str(TABLE_OBJ.FORMULA_LOGIC):
							new_value_dict[str(TABLE_OBJ.API_NAME)] = ""
							new_value_dict[str(api_name)] = ""
		else:
			attrval_obj = Sql.GetFirst(
				"SELECT API_NAME FROM  SYOBJD WITH (NOLOCK) WHERE OBJECT_NAME='"
				+ str(ObjectName)
				+ "' AND LOOKUP_OBJECT='"
				+ str(LOOKUPOBJ)
				+ "' and  LOOKUP_API_NAME='"
				+ str(LOOKUPAPI)
				+ "'"
			)
			api_name = attrval_obj.API_NAME.strip()
			NEWVAL = NEWVAL.split("|")
			result = ScriptExecutor.ExecuteGlobal(
				"SYPARCEFMA", {"Object": ObjectName, "API_Name": api_name, "API_Value": NEWVAL[0]},
			)
			new_value_dict = {API_Names["API_NAME"]: API_Names["FORMULA_RESULT"] for API_Names in result}

			lookupval = str(LOOKUPOBJ).split("_")
			lookup_ObjName = ""
			if len(lookupval) == 1:
				lookup_ObjName = lookupval[0]
			else:
				lookup_ObjName = lookupval[1]

	
	if ObjectName != 'SAQRIB':
		sec_str += ' <div class="col-md-12"   id="alert_msg" style="display: none;"><div class="row modulesecbnr brdr" data-toggle="collapse" data-target="#Alertmsg8" aria-expanded="true">NOTIFICATIONS<i class="pull-right fa fa-chevron-down "></i><i class="pull-right fa fa-chevron-up"></i></div><div  id="Alertmsg8" class="col-md-12  alert-notification  brdr collapse in" ><div  class="col-md-12 alert-danger"  ><label ><img src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/stopicon1.svg" alt="Error">  </label></div></div></div>'

	if str(ObjectName) == "SAQTRV" or  str(ObjectName) == "ACAPCH":
		editclick = "QuoteinformationEDIT(this)"
		cancelclick = "QuoteinformationCancel()"
		saveclick = "QuoteinformationSave()"
	else:
		editclick = "CommonEDIT(this)"
		cancelclick = "CommontreeCancel(this)"
		saveclick = "CommontreeSAVE()"
	lookup_popup = "CommonTree_lookup_popup(this)"
	cancel_save = ""
	if str(SECTION_EDIT) == "" and str(MODE) == "EDIT":
		section_edit_obj_query = (
			"SELECT TOP 1000 SYSECT.* FROM SYSECT WITH (NOLOCK) INNER JOIN SYSEFL (NOLOCK)"
			+ " ON SYSECT.RECORD_ID = SYSEFL.SECTION_RECORD_ID INNER JOIN SYOBJD (NOLOCK)"
			+ " ON SYSEFL.API_NAME = SYOBJD.OBJECT_NAME AND SYSEFL.API_FIELD_NAME = SYOBJD.API_NAME INNER JOIN SYPAGE (NOLOCK) ON SYPAGE.RECORD_ID = SYSECT.PAGE_RECORD_ID WHERE PRIMARY_OBJECT_NAME='"
			+ str(ObjectName)
			+ "' AND SYPAGE.TAB_RECORD_ID = '' AND SYOBJD.PERMISSION <> 'READ ONLY' "
			+ str(queryStr)
			+ " ORDER BY ABS(SYSECT.DISPLAY_ORDER)"
		)		
		section_edit_obj = Sql.GetFirst(section_edit_obj_query)
		if section_edit_obj is not None:
			SECTION_EDIT = str(section_edit_obj.RECORD_ID)
			api_name = SECTION_EDIT
	get_user_id = userId
	#section level permissions start	
	if ( ObjectName == "SYSECT" or ObjectName == "SYSEFL") and (crnt_prd_val == "SY"):		
		#Below query is in the logic to remove duplicate if the user is in more than one profile
		QStr1 = ("SELECT TOP 1000 SYSECT.* FROM SYSECT WHERE SYSECT.RECORD_ID IN (SELECT DISTINCT SECTION_RECORD_ID FROM SYPRSN (NOLOCK) JOIN USERS_PERMISSIONS (NOLOCK) up ON UP.PERMISSION_ID = SYPRSN.PROFILE_RECORD_ID WHERE SYPRSN.TAB_RECORD_ID = '' AND SYPRSN.VISIBLE = 'True' AND UP.USER_ID = '"
			+ str(get_user_id)
			+ "') AND SYSECT.PRIMARY_OBJECT_NAME = '"
			+ str(ObjectName)
			+ "' ORDER BY ABS(SYSECT.DISPLAY_ORDER)")
		# QStr1 = (
		# 	"SELECT TOP 1000 SYSECT.* FROM SYSECT WITH (NOLOCK)"
		# 	+ " JOIN SYPRSN (NOLOCK) ON SYPRSN.SECTION_RECORD_ID = SYSECT.RECORD_ID"
		# 	+ " JOIN USERS_PERMISSIONS (NOLOCK) up ON UP.PERMISSION_ID = SYPRSN.PROFILE_RECORD_ID WHERE SYSECT.PRIMARY_OBJECT_NAME = '"
		# 	+ str(ObjectName)
		# 	+ "' AND SYPRSN.TAB_RECORD_ID = '' AND SYPRSN.VISIBLE = 1 AND UP.USER_ID = '"
		# 	+ str(get_user_id)
		# 	+ "' "
		# 	+ str(queryStr)
		# 	+ " ORDER BY ABS(SYSECT.DISPLAY_ORDER)"
		# )
		#section level permissions end
		'''QStr1 = (
			"SELECT TOP 1000 SYSECT.* FROM SYSECT WITH (NOLOCK)"
			+ " WHERE SYSECT.PRIMARY_OBJECT_NAME = '"
			+ str(ObjectName)
			+ "' AND SYSECT.PAGE_RECORD_ID = '' "
			+ str(queryStr)
			+ " ORDER BY ABS(SYSECT.DISPLAY_ORDER)"
		)'''
	elif (ObjectName == "ACAPTX" and crnt_prd_val == "QT"):
		QStr1 = ("""SELECT TOP 1000 SYSECT.* FROM SYTABS (NOLOCK) 
					JOIN SYPAGE (NOLOCK) ON SYPAGE.TAB_NAME = SYTABS.TAB_LABEL
					JOIN SYSECT (NOLOCK) ON SYSECT.PAGE_RECORD_ID = SYPAGE.RECORD_ID AND SYSECT.PAGE_LABEL = SYPAGE.PAGE_LABEL
					where SYTABS.APP_ID = '{}' and SYPAGE.OBJECT_APINAME = '{}' ORDER BY ABS(SYSECT.DISPLAY_ORDER)""".format(str(crnt_prd_val),str(ObjectName)))
	## ACAPTX Sect load ends
	
	elif (ObjectName =="SYTABS" and crnt_prd_val == "SY" and (TreeParentParam == "Tabs" or TreeParam == "Tabs")):	
		QStr1 = ("SELECT TOP 1000 SYSECT.* FROM SYSECT (NOLOCK) WHERE SYSECT.PAGE_RECORD_ID = '' AND SYSECT.PRIMARY_OBJECT_NAME = '" + str(ObjectName) + "' " + str(queryStr) + " ORDER BY ABS(SYSECT.DISPLAY_ORDER)")
	elif ObjectName in ("SAQSGB","SAQFBL","SAQFGB","SAQSFB","SAQRIT"):
		QStr1 = ("SELECT TOP 1000 SYSECT.* FROM SYSECT (NOLOCK) WHERE  SYSECT.PRIMARY_OBJECT_NAME = '" + str(ObjectName) + "' ORDER BY ABS(SYSECT.DISPLAY_ORDER)")
	elif (ObjectName == "CTCFGB"):
		QStr1 = ("SELECT TOP 1000 SYSECT.* FROM SYSECT (NOLOCK) WHERE  SYSECT.PRIMARY_OBJECT_NAME = '" + str(ObjectName) + "' ORDER BY ABS(SYSECT.DISPLAY_ORDER)")
	# elif (ObjectName == "CTCSCO"):
	# 	QStr1 = ("SELECT TOP 1000 SYSECT.* FROM SYSECT (NOLOCK) WHERE  SYSECT.PRIMARY_OBJECT_NAME = '" + str(ObjectName) + "' ORDER BY ABS(SYSECT.DISPLAY_ORDER)")
	elif (ObjectName == "SAQTMT") and SubtabName == "Idling Attributes":
		Trace.Write('elee====2')
		QStr1 = ("SELECT TOP 1000 SYSECT.* FROM SYSECT (NOLOCK) WHERE  SYSECT.SECTION_DESC != '' AND SYSECT.PRIMARY_OBJECT_NAME = '" + str(ObjectName) + "' ORDER BY ABS(SYSECT.DISPLAY_ORDER)")
	elif (ObjectName == "SAQDOC") and SubtabName == "Document Generator":
		Trace.Write('elee====23')
		QStr1 = ("SELECT TOP 1000 SYSECT.* FROM SYSECT (NOLOCK) WHERE  SYSECT.PRIMARY_OBJECT_NAME = '" + str(ObjectName) + "' ORDER BY ABS(SYSECT.DISPLAY_ORDER)")	
	else:
		Trace.Write(str(queryStr)+'---eleee===1'+str(LEGALSOW))		
		"""QStr1 = (
			"SELECT TOP 1000 SYSECT.* FROM SYSECT WITH (NOLOCK)"
			+ " JOIN SYPRSN (NOLOCK) ON SYPRSN.SECTION_RECORD_ID = SYSECT.RECORD_ID"
			+ " JOIN USERS_PERMISSIONS (NOLOCK) up ON UP.PERMISSION_ID = SYPRSN.PROFILE_RECORD_ID WHERE SYSECT.PRIMARY_OBJECT_NAME = '"
			+ str(ObjectName)
			+ "' AND SYPRSN.TAB_RECORD_ID = '' AND SYPRSN.VISIBLE = 1 AND UP.USER_ID = '"
			+ str(get_user_id)
			+ "' "
			+ str(queryStr)
			+ " ORDER BY ABS(SYSECT.DISPLAY_ORDER)"
		)"""	
		if LEGALSOW == 'LEGAL_SOW':
			QStr1 = ("SELECT TOP 1000 SYSECT.* FROM SYSECT (NOLOCK) WHERE  SYSECT.PRIMARY_OBJECT_NAME = '" + str(ObjectName) + "' AND RECORD_ID ='AED0A92A-8644-46AE-ACF0-90D6E331E506' " + str(queryStr) + " ORDER BY ABS(SYSECT.DISPLAY_ORDER)")
		elif ObjectName == "SAQRGG":
			QStr1 = ("SELECT TOP 1000 SYSECT.* FROM SYSECT (NOLOCK) WHERE  SYSECT.PRIMARY_OBJECT_NAME = '" + str(ObjectName) + "' AND RECORD_ID !='AED0A92A-8644-46AE-ACF0-90D6E331E506' ORDER BY ABS(SYSECT.DISPLAY_ORDER)")

		else:
			QStr1 = ("SELECT TOP 1000 SYSECT.* FROM SYSECT (NOLOCK) WHERE  SYSECT.PRIMARY_OBJECT_NAME = '" + str(ObjectName) + "' AND RECORD_ID !='AED0A92A-8644-46AE-ACF0-90D6E331E506' " + str(queryStr) + " ORDER BY ABS(SYSECT.DISPLAY_ORDER)")
		#QStr1 = (
			#"SELECT TOP 1000 SYSECT.* FROM SYSECT WITH (NOLOCK)"
			#+ " WHERE SYSECT.PRIMARY_OBJECT_NAME = '"
			#+ str(ObjectName)
			#+ "' "
			#+ str(queryStr)
			#+ " ORDER BY ABS(SYSECT.DISPLAY_ORDER)"
		#)	
		
	section_obj = Sql.GetList(QStr1)	


	for sec in section_obj:
		sec_rec_id = str(sec.RECORD_ID)
		b = "sec_" + str(sec_rec_id)
		a = "g4 " + str(sec_rec_id)
		editable_permission = "FALSE"
		if SECTION_EDIT != "":			
			if str(sec.RECORD_ID) != str(SECTION_EDIT):
				MODE = "SEC_VIEW"
			else:
				MODE = "EDIT"

		'''QuStr = """ SELECT TOP 1000
						SYOBJD.SOURCE_DATA, SYSEFL.FIELD_LABEL AS FIELD_LABEL, SYOBJD.REQUIRED,
						SYOBJD.RECORD_ID, SYOBJD.API_NAME, SYOBJD.DATA_TYPE, SYOBJD.PERMISSION,
						SYOBJD.FORMULA_DATA_TYPE, SYOBJD.LOOKUP_API_NAME, SYOBJD.LOOKUP_OBJECT, SYSEFL.HELP_TEXT_TITLE,SYSEFL.HELP_TEXT_COPY
					FROM SYOBJD (NOLOCK) INNER JOIN SYSEFL (NOLOCK) ON SYOBJD.OBJECT_NAME = SYSEFL.API_NAME AND SYOBJD.API_NAME = SYSEFL.API_FIELD_NAME INNER JOIN SYPRSF (nolock) ON SYSEFL.RECORD_ID = SYPRSF.SECTIONFIELD_RECORD_ID INNER JOIN USERS_PERMISSIONS (NOLOCK) up ON UP.PERMISSION_ID = SYPRSF.PROFILE_RECORD_ID 
					WHERE
						SYSEFL.API_NAME = '{1}' AND
						SYSEFL.SECTION_RECORD_ID='{0}' AND
						SYOBJD.OBJECT_NAME='{1}' AND
						UP.USER_ID = '{2}'
					ORDER BY ABS(SYSEFL.DISPLAY_ORDER) """.format(
			str(sec.RECORD_ID), str(ObjectName), str(get_user_id)
		)'''
		QuStr = """ SELECT TOP 1000
						SYOBJD.SOURCE_DATA, SYSEFL.FIELD_LABEL AS FIELD_LABEL, SYOBJD.REQUIRED,
						SYOBJD.RECORD_ID, SYOBJD.API_NAME, SYOBJD.DATA_TYPE, SYOBJD.PERMISSION,
						SYOBJD.FORMULA_DATA_TYPE, SYOBJD.LOOKUP_API_NAME, SYOBJD.LOOKUP_OBJECT,SYOBJD.LENGTH, SYSEFL.HELP_TEXT_TITLE,SYSEFL.HELP_TEXT_COPY
					FROM SYOBJD (NOLOCK) INNER JOIN SYSEFL (NOLOCK) ON SYOBJD.OBJECT_NAME = SYSEFL.API_NAME AND SYOBJD.API_NAME = SYSEFL.API_FIELD_NAME 
					WHERE
						SYSEFL.API_NAME = '{1}' AND
						SYSEFL.SECTION_RECORD_ID='{0}' AND
						SYOBJD.OBJECT_NAME='{1}' 
					ORDER BY ABS(SYSEFL.DISPLAY_ORDER) """.format(
			str(sec.RECORD_ID), str(ObjectName)
		)
		# Trace.Write(
		# 	""" SELECT TOP 1000
		# 				SYOBJD.SOURCE_DATA, SYSEFL.FIELD_LABEL AS FIELD_LABEL, SYOBJD.REQUIRED,
		# 				SYOBJD.RECORD_ID, SYOBJD.API_NAME, SYOBJD.DATA_TYPE, SYOBJD.PERMISSION,
		# 				SYOBJD.FORMULA_DATA_TYPE, SYOBJD.LOOKUP_API_NAME, SYOBJD.LOOKUP_OBJECT, SYSEFL.HELP_TEXT_TITLE,SYSEFL.HELP_TEXT_COPY
		# 			FROM SYOBJD (NOLOCK) INNER JOIN SYSEFL (NOLOCK) ON SYOBJD.OBJECT_NAME = SYSEFL.API_NAME AND SYOBJD.API_NAME = SYSEFL.API_FIELD_NAME 
		# 			WHERE
		# 				SYSEFL.API_NAME = '{1}' AND
		# 				SYSEFL.SECTION_RECORD_ID='{0}' AND
		# 				SYOBJD.OBJECT_NAME='{1}' 
		# 			ORDER BY ABS(SYSEFL.DISPLAY_ORDER) """.format(
		# 		str(sec.RECORD_ID), str(ObjectName)
		# 	)
		# )
		data_obj = Sql.GetList(QuStr)
		Trace.Write('388-----------')
		#API_NAMES = ",".join(str(data.API_NAME) for data in data_obj if data.DATA_TYPE != "DATE")
		API_NAMES = ",".join(str(data.API_NAME) for data in data_obj)
		for data in data_obj:
			# Trace.Write(
			# 	"PERMISSION : "
			# 	+ str(data.PERMISSION)
			# 	+ "	CANEDIT : "
			# 	+ str(canedit)
			# 	+ "	FIELD_LABEL : "
			# 	+ str(data.FIELD_LABEL)
			# 	+ "	MODE : "
			# 	+ MODE
			# )
			text = ""
			if data.PERMISSION != "READ ONLY" and str(canedit).upper() == "TRUE":
				editable_permission = "TRUE"
			if data.DATA_TYPE == "DATE" or data.FORMULA_DATA_TYPE == "DATE" or str(data.API_NAME) == "EXCHANGE_RATE_DATE":				
				if text == "":	
					Trace.Write('text if--'+str(text))				
					text = "CONVERT(VARCHAR(10),"+'CONVERT(DATE,'+str(data.API_NAME)+')'+" ,101) AS " + str(data.API_NAME)
				else:	    
					Trace.Write('text else--'+str(text))
					text = text + "," + "CONVERT(VARCHAR(10),"+'CONVERT(DATE,'+str(data.API_NAME)+')'+" ,101) AS " + str(data.API_NAME)
				if text.startswith("CONVERT"):
					Trace.Write("API_NAMES- API_NAMES->"+str(API_NAMES))
					API_NAMES = API_NAMES + "," + ",".join(str(data) for data in text.split(","))
					Trace.Write("API_NAMES-->"+str(API_NAMES))
				else:					
					API_NAMES = API_NAMES + "," + ",".join(str(data) for data in text.split(","))
		Trace.Write("main container"+str(a))
		if str(a)=="g4 F43725A0-056D-473B-BC90-0065CCCF9D13" and (TreeParam != 'Z0007' or TreeParam != 'Z0007_AG'):
			sec_str += '<div id="container" class="wdth100 margtop10 ' + str(a) + '" style ="display:none" >'
		else:
			sec_str += '<div id="container" class="wdth100 margtop10 ' + str(a) + '"  >'
		action_visible_obj = ""
		SecEdiApp = ["SYSTEM ADMIN", "SALES"]
		if current_prod not in SecEdiApp:
			action_visible_obj = Sql.GetFirst(
				"""
									SELECT
										SYPRSN.*
									FROM
										SYPRSN (NOLOCK)
									JOIN
										USERS_PERMISSIONS UP (NOLOCK) ON UP.PERMISSION_ID = SYPRSN.PROFILE_RECORD_ID
									WHERE
										SYPRSN.SECTION_RECORD_ID = '{Section_Rec_Id}' AND
										UP.USER_ID = '{User_Record_Id}' AND
										SYPRSN.EDITABLE = 0
									""".format(
					Section_Rec_Id=sec.RECORD_ID, User_Record_Id=get_user_id
				)
			)

		if action_visible_obj:
			if action_visible_obj.OBJECT_RECORD_ID:
				action_visible_str = action_visible_obj.OBJECT_RECORD_ID
		if ObjectName == "SYOBFD":
			editable_permission = "TRUE"
		Trace.Write("editable_permission==="+str(editable_permission))
		if editable_permission == "TRUE":			
			sec_str += (
				'<div class="dyn_main_head master_manufac glyphicon pointer   glyphicon-chevron-down" onclick="dyn_main_sec_collapse_arrow(this)" data-target="#'
				+ str(b)
				+ '"  data-toggle="collapse"><label class="onlytext"><div>'
			)	
			sec_not_list = [
				"SYSECT-MA-00019",
				"SYSECT-MA-00407",
				"SYSECT-MA-00023",
				"SYSECT-MA-00410",
				"SYSECT-MA-00416",
				"SYSECT-MA-00417",
				"SYSECT-MA-00418",
				"SYSECT-MA-00419",
				"SYSECT-MA-00460",
				"SYSECT-MA-00461",
				"SYSECT-MA-00429",
				"SYSECT-MA-00429",
				"SYSECT-TQ-00215",
				"SYSECT-QT-00121",
				"SYSECT-AC-00002",
				"SYSECT-AC-00003",
				"SYSECT-AC-00004",
				"SYSECT-AC-00005",
				"SYSECT-AC-00006",
				"SYSECT-QT-00167",
				"SYSECT-QT-00168"							
				
			]

			if action_visible_str:
				sec_not_list.append(action_visible_str)
			
			if (MODE == "SEC_VIEW" or MODE == "VIEW" or MODE == "CANCEL" or MODE == "EDIT") and str(sec.RECORD_ID) not in sec_not_list:	
				Trace.Write('=====>')	
				Trace.Write("@486")		
				if sec.SECTION_NAME =="BASIC INFORMATION" and Product.GetGlobal("TreeParentLevel0") == "Quote Items":					
					sec_str += ("")
					Trace.Write("@488")
					#quote items edit issue
					'''sec_str += (
						'<div id="ctr_drop" class="btn-group dropdown"><div class="dropdown"><i data-toggle="dropdown" class="fa fa-sort-desc dropdown-toggle"></i><ul class="dropdown-menu left" aria-labelledby="dropdownMenuButton"><li class="edit_list"><a id="'
						+ str(sec.RECORD_ID)
						+ '" class="dropdown-item" href="#" onclick="'
						+ str(editclick)
						+ '">EDIT</a></li></ul></div></div>'
					)'''
				elif sec.SECTION_NAME =="PRICING INFORMATION" and Product.GetGlobal("TreeParentLevel0") == "Quote Items":					
					sec_str += ("")
					Trace.Write("@498")
				
				else:
					cancel_btn = save_btn = ''	
					sec_html_btn = Sql.GetList("SELECT HTML_CONTENT FROM SYPSAC (NOLOCK) WHERE SECTION_RECORD_ID = '"+str(sec.RECORD_ID)+"'")
					if sec_html_btn:
						for btn in sec_html_btn:											
							if "EDIT" in btn.HTML_CONTENT and (MODE == 'VIEW' or MODE == 'CANCEL'):
								section_edit_btn = str(btn.HTML_CONTENT).format(rec_id= sec.RECORD_ID, edit_click= editclick)
								sec_str += (
									section_edit_btn
								)
							if "CANCEL" in btn.HTML_CONTENT:
								cancel_btn = str(btn.HTML_CONTENT).format(cancel_onclick=cancelclick)
							if "SAVE" in btn.HTML_CONTENT:
								save_btn = str(btn.HTML_CONTENT).format(save_onclick= saveclick)

						cancel_save = '<div  class="g4 sec_' + str(SECTION_EDIT) + ' collapse in except_sec removeHorLine iconhvr sec_edit_sty">'+ str(cancel_btn) + str(save_btn) +'</div>'
						Trace.Write("cancel_savecancel_save_J"+str(cancel_save))
						Trace.Write("@540"+str(sec_str))

					

					if Product.GetGlobal("TreeParentLevel0") == 'Quote Items':
						if (' - ' ) in TreeParam: 
							if TreeParam.split('-')[1].strip() == 'Z0100':
								if sec.SECTION_NAME == "PRICING INFORMATION":
									sec.SECTION_NAME = "FPM INFORMATION"	
					# sec_html_btn = Sql.GetFirst("SELECT HTML_CONTENT FROM SYPSAC (NOLOCK) WHERE ACTION_NAME = 'EDIT' AND SECTION_RECORD_ID = '"+str(sec.RECORD_ID)+"'")


					# cancel_html = Sql.GetFirst("SELECT HTML_CONTENT FROM SYPSAC (NOLOCK) WHERE ACTION_NAME = 'CANCEL' AND SECTION_RECORD_ID = '"+str(sec.RECORD_ID)+"'")
					# save_html = Sql.GetFirst("SELECT HTML_CONTENT FROM SYPSAC (NOLOCK) WHERE ACTION_NAME = 'SAVE' AND SECTION_RECORD_ID = '"+str(sec.RECORD_ID)+"'")
					# cancel_save = '<div  class="g4 sec_'+str(sec.RECORD_ID)+' collapse in except_sec removeHorLine iconhvr sec_edit_sty">' +str(cancel_html)+str(save_html)+'</div>'

					# if sec_html_btn is not None:
						# section_edit_btn = str(sec_html_btn.HTML_CONTENT).format(rec_id= sec.RECORD_ID, edit_click= editclick)

						# sec_str += (
						# 	section_edit_btn
						# )
							# '<div id="ctr_drop" class="btn-group dropdown"><div class="dropdown"><i data-toggle="dropdown" class="fa fa-sort-desc dropdown-toggle"></i><ul class="dropdown-menu left" aria-labelledby="dropdownMenuButton"><li class="edit_list"><a id="'
							# + str(sec.RECORD_ID)
							# + '" class="dropdown-item" href="#" onclick="'
							# + str(editclick)
							# + '">EDIT</a></li></ul></div></div>'
					# else:
					# 	sec_str += ""
			# COMMENTED THE CONDITION TO RESTRICT SECTIONAL EDIT BUTTON FOR UNWANTED SECTIONS WHILE CLICKING CANCEL - START			
			# if (MODE == "CANCEL") and str(sec.RECORD_ID) not in sec_not_list:
			# 	Trace.Write("cm to thus SAQITMCANCEL"+str(sec.RECORD_ID))
			# 	sec_str += (
			# 		'<div id="ctr_drop" class="btn-group dropdown"><div class="dropdown"><i data-toggle="dropdown" class="fa fa-sort-desc dropdown-toggle"></i><ul class="dropdown-menu left" aria-labelledby="dropdownMenuButton"><li class="edit_list"><a id="'
			# 		+ str(sec.RECORD_ID)
			# 		+ '" class="dropdown-item" href="#" onclick="'
			# 		+ str(editclick)
			# 		+ '">EDIT</a></li></ul></div></div>'
			# 	)
			# COMMENTED THE CONDITION TO RESTRICT SECTIONAL EDIT BUTTON FOR UNWANTED SECTIONS WHILE CLICKING CANCEL - END
			
			sec_str += str(sec.SECTION_NAME) + "</div> </label> </div>"		
		else:			
			Trace.Write("astrl"+str(TreeParam))
			Trace.Write("astrl2"+str(sec.SECTION_NAME))
			if sec.SECTION_NAME =="BASIC INFORMATION" and Product.GetGlobal("TreeParentLevel0") == "Field Dependencies":
				'''sec_str += (
					'<div id="ctr_drop" class="btn-group dropdown"><div class="dropdown"><i data-toggle="dropdown" class="fa fa-sort-desc dropdown-toggle"></i><ul class="dropdown-menu left" aria-labelledby="dropdownMenuButton"><li class="edit_list"><a id="'
					+ str(sec.RECORD_ID)
					+ '" class="dropdown-item" href="#" onclick="'
					+ str(editclick)
					+ '">EDIT</a></li></ul></div></div>'
				)'''
				
				sec_str += (
					'<div class="dyn_main_head master_manufac glyphicon pointer  glyphicon-chevron-down" onclick="dyn_main_sec_collapse_arrow(this)" data-target="#'
					+ str(b)
					+ '" data-toggle="collapse"><label class="onlytext"><div>'
					+ str(sec.SECTION_NAME)
					+ "</div> </label></div>"
				)
				#sec_str += str(sec.SECTION_NAME) + "</div> </label> </div>"
			elif sec.SECTION_NAME =="RELOCATION INFORMATION" and (TreeParam != 'Z0007' or TreeParam != 'Z0007_AG'):	
				#Trace.Write("astrl2"+str(sec.SECTION_NAME))
				sec_str += ("") 		
			else:				
				sec_str += (
					'<div class="dyn_main_head master_manufac glyphicon pointer  glyphicon-chevron-down" onclick="dyn_main_sec_collapse_arrow(this)" data-target="#'
					+ str(b)
					+ '" data-toggle="collapse"><label class="onlytext"><div>'
					+ str(sec.SECTION_NAME)
					+ "</div> </label></div>"
				)				
				
				'''sec_str += (
					'<div id="ctr_drop" class="btn-group dropdown"><div class="dropdown"><i data-toggle="dropdown" class="fa fa-sort-desc dropdown-toggle"></i><ul class="dropdown-menu left" aria-labelledby="dropdownMenuButton"><li class="edit_list"><a id="'
					+ str(sec.SECTION_NAME)
					+ '" class="dropdown-item" href="#" onclick="'
					+ str(editclick)
					+ '">EDIT</a></li></ul></div></div>'
				)'''
		Trace.Write("astrl3"+str(b))
		if str(b) =="sec_F43725A0-056D-473B-BC90-0065CCCF9D13" and (TreeParam != 'Z0007' or TreeParam != 'Z0007_AG'):
			sec_str += '<div id="' + str(b) + '" class="collapse in" style ="display:none"> <table  class="wth100mrg8">'
		else:
			sec_str += '<div id="' + str(b) + '" class="collapse in"> <table  class="wth100mrg8">'
		sec_str += auto_field
					
		query_value = Sql.GetFirst(
			"SELECT * FROM SYOBJD WITH (NOLOCK) WHERE DATA_TYPE = 'AUTO NUMBER' AND OBJECT_NAME = '" + str(ObjectName) + "'"
		)
		
		if str(ObjectName) != "QT__ACSRPB":
			autoNumber = query_value.API_NAME
		if str(ObjectName) != "SYSECT":
			if "DEFAULT" in str(API_NAMES):
				API_NAMES = str(API_NAMES).replace("DEFAULT", "[DEFAULT]")	
		if "PRIMARY" in str(API_NAMES):
			API_NAMES = str(API_NAMES).replace("PRIMARY", "[PRIMARY]")
		# if str(ObjectName) == "SAQITM":
		# 	autoNumber = "LINE_ITEM_ID"
		if str(ObjectName) == "SYPROH":
			if "SYPRO" in RECORD_ID:
				syprohval = SqlHelper.GetFirst(
					"select PROFILE_OBJECT_RECORD_ID from SYPROH (NOLOCK) where OBJECT_RECORD_ID = '" + str(RECORD_ID) + "'"
				)
				RECORD_ID = syprohval.PROFILE_OBJECT_RECORD_ID
			elif MODE == "SEC_VIEW":				
				RECORD_ID = TreeParam
				autoNumber = "OBJECT_NAME"
			elif MODE == "CANCEL":
				autoNumber = "PROFILE_OBJECT_RECORD_ID"
			elif MODE == "EDIT" and str(TreeParam) == "Object Level Permissions":
				RECORD_ID
				autoNumber = "PROFILE_OBJECT_RECORD_ID"
			else:
				RECORD_ID
				autoNumber = "OBJECT_RECORD_ID"
		
		if str(ObjectName) == "USERS":
			RECORD_ID = re.findall(r"\d+", RECORD_ID)
			RECORD_ID = "".join(RECORD_ID)
			if RECORD_ID =="":
				users_obj = Sql.GetFirst("SELECT ID FROM USERS (NOLOCK) WHERE USERNAME = '"+str(TreeParam)+"' ")
				RECORD_ID = str(users_obj.ID)			
		
		# Billing Matrix Details Load - Start
		if ObjectName == 'SAQRIB':
			billing_plan_obj = SqlHelper.GetFirst(
					"select QUOTE_BILLING_PLAN_RECORD_ID from SAQRIB (NOLOCK) where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' ".format(quote_record_id,quote_revision_record_id)
					
				)
			if billing_plan_obj:
				RECORD_ID = billing_plan_obj.QUOTE_BILLING_PLAN_RECORD_ID
		# Billing Matrix Details Load - End	
		
		# Greenbook details load || Quote item Location Node - Start
		if Product.GetGlobal("TreeParentLevel2") == 'Quote Items':
			quote_record_id = Quote.GetGlobal("contract_quote_record_id")
			TreeSuperParentParam = Product.GetGlobal("TreeParentLevel1")
			TreeParam = Product.GetGlobal("TreeParam")
			TreeParentParam = Product.GetGlobal("TreeParentLevel0")
			try:
				if str(TreeSuperParentParam.split("-")[4]):
					Trace.Write("try if") 
					service_id = TreeSuperParentParam.split('-')[-3].strip()
				else:
					Trace.Write("try else")
					service_id = TreeSuperParentParam.split('-')[1].strip()
			except:
				Trace.Write("except")
				Trace.Write("SuperParentParam-"+str(TreeSuperParentParam))
				service_id = TreeSuperParentParam.split('-')[1].strip()
			# quote_item_gb = Sql.GetFirst(
			# 	"select QUOTE_ITEM_GREENBOOK_RECORD_ID from SAQIGB (NOLOCK) where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND GREENBOOK = '{}' AND FABLOCATION_ID = '{}' AND SERVICE_ID = '{}'".format(quote_record_id,quote_revision_record_id,TreeParam,TreeParentParam,service_id)
			# )
			if quote_item_gb:
				RECORD_ID = quote_item_gb.QUOTE_ITEM_GREENBOOK_RECORD_ID				
		# Greenbook details load || Quote item Location Node - End
			
		# Greenbook details load || Fab Location Node - Start 
		if ObjectName == 'SAQFGB':			
			quote_record_id = Quote.GetGlobal("contract_quote_record_id")
			fab_location_gb = Sql.GetFirst(
				"select QUOTE_FAB_LOC_GB_RECORD_ID from SAQFGB (NOLOCK) where QUOTE_RECORD_ID = '"+str(quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"'  AND GREENBOOK = '"+str(TreeParam)+"' AND FABLOCATION_ID = '"+str(Product.GetGlobal("TreeParentLevel0"))+"'"
			)
			if fab_location_gb:
				RECORD_ID = fab_location_gb.QUOTE_FAB_LOC_GB_RECORD_ID
		# Greenbook details load || Fab Location Node - End	

		# Greenbook details load || Product offering Node - Start 
		if ObjectName == 'SAQSGB':	
			Trace.Write('ObjectName---')		
			quote_record_id = Quote.GetGlobal("contract_quote_record_id")
			prd_location_gb = Sql.GetFirst(
				"""select QUOTE_SERVICE_GREENBOOK_RECORD_ID from SAQSGB (NOLOCK) where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND GREENBOOK = '{}' AND SERVICE_ID = '{}'""".format(quote_record_id,quote_revision_record_id,TreeParam,TreeParentParam)
			)
			''' ## REMOVAL FOR FAB LOCATIONS.
			prd_location_gb = Sql.GetFirst(
				"""select QUOTE_SERVICE_GREENBOOK_RECORD_ID from SAQSGB (NOLOCK) where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'
and GREENBOOK = '{}' AND FABLOCATION_ID = '{}' AND SERVICE_ID = '{}'""".format(quote_record_id,quote_revision_record_id,TreeParam,TreeParentParam,Product.GetGlobal("TreeParentLevel1").split(" ")[0].strip())
			)
			'''
			if prd_location_gb:
				RECORD_ID = prd_location_gb.QUOTE_SERVICE_GREENBOOK_RECORD_ID
		# Greenbook details load || Product offering  Node - End
		if ObjectName == 'SAQSFB':
			quote_record_id = Quote.GetGlobal("contract_quote_record_id")
			if Product.GetGlobal("TreeParentLevel0") == 'Sending Equipment' or Product.GetGlobal("TreeParentLevel0") == 'Receiving Equipment':
				prd_location_fb = Sql.GetFirst(
					"select QUOTE_SERVICE_FAB_LOCATION_RECORD_ID from SAQSFB (NOLOCK) where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID = '{}'".format(quote_record_id,quote_revision_record_id,TreeSuperParentParam)
				)				
			else:
				prd_location_fb = Sql.GetFirst(
					"select QUOTE_SERVICE_FAB_LOCATION_RECORD_ID from SAQSFB (NOLOCK) where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID = '{}' AND FABLOCATION_ID = '{}'".format(quote_record_id,quote_revision_record_id,Product.GetGlobal("TreeParentLevel0").split(" ")[0].strip(),TreeParam)
				)
			if prd_location_fb:
				RECORD_ID = prd_location_fb.QUOTE_SERVICE_FAB_LOCATION_RECORD_ID		
		if ObjectName == 'CTCSCO':
			quote_record_id = Quote.GetGlobal("contract_record_id")
			prd_location_fb = Sql.GetFirst(
				"select * from CTCSCO (NOLOCK) where CONTRACT_RECORD_ID = '{}' AND SERVICE_ID = '{}'".format(quote_record_id,Product.GetGlobal("TreeParentLevel0"))
			)
			if prd_location_fb:
				RECORD_ID = prd_location_fb.CONTRACT_SERVICE_EQUIPMENT_RECORD_ID
		if ObjectName == 'CTCSGB':
			quote_record_id = Quote.GetGlobal("contract_record_id")
			prd_location_fb = Sql.GetFirst(
				"select * from CTCSGB (NOLOCK) where CONTRACT_RECORD_ID = '{}' AND SERVICE_ID = '{}'".format(quote_record_id,TreeParentParam)
			)
			if prd_location_fb:
				RECORD_ID = prd_location_fb.CNTSRVGB_RECORD_ID		


		if ObjectName == 'SAQSRA':
			quote_record_id = Quote.GetGlobal("contract_quote_record_id")
			if TreeParam.startswith("Sending"):
				send_receive_data = Sql.GetFirst(
					"select QUOTE_SENDING_RECEIVING_ACCOUNT from SAQSRA (NOLOCK) where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND RELOCATION_TYPE LIKE '%SENDING%'".format(quote_record_id,quote_revision_record_id)
				)
			if TreeParam.startswith("Receiving"):
				send_receive_data = Sql.GetFirst(
					"select QUOTE_SENDING_RECEIVING_ACCOUNT from SAQSRA (NOLOCK) where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND RELOCATION_TYPE LIKE '%RECEIVING%'".format(quote_record_id,quote_revision_record_id)
				)
			if send_receive_data:
				RECORD_ID = send_receive_data.QUOTE_SENDING_RECEIVING_ACCOUNT
		# if ObjectName == 'SAQIFL':
		# 	quote_record_id = Quote.GetGlobal("contract_quote_record_id")
		# 	qitm_location_fb = Sql.GetFirst(
		# 		"select * from SAQIFL (NOLOCK) where QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}'".format(quote_record_id,TreeParentParam.split("-")[1].strip())
		# 	)
		# 	if qitm_location_fb:
		# 		RECORD_ID = qitm_location_fb.QUOTE_ITEM_FAB_LOCATION_RECORD_ID	
		try:
			if str(ObjectName) == "SYPROH" and TreeParam != "Object Level Permissions":		
				if MODE == "VIEW":
					autoNumber = "PROFILE_OBJECT_RECORD_ID"
				else:
					if '-' in str(RECORD_ID):
						autoNumber = "PROFILE_OBJECT_RECORD_ID"
					else:
						autoNumber = "OBJECT_NAME"
				permissions_id_val = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00128").GetValue()
				script = (
					"SELECT "
					+ str(API_NAMES)
					+ " FROM "
					+ str(ObjectName)
					+ " (NOLOCK) WHERE PROFILE_ID = '"
					+ str(permissions_id_val)
					+ "' AND "
					+ str(autoNumber)
					+ " = '"
					+ str(RECORD_ID)
					+ "'"
				)
			elif str(ObjectName) == "SYPROH" and TreeParam == "Object Level Permissions" and MODE == "VIEW":				
				autoNumber = "PROFILE_OBJECT_RECORD_ID"
				permissions_id_val = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00128").GetValue()
				script = (
					"SELECT "
					+ str(API_NAMES)
					+ " FROM "
					+ str(ObjectName)
					+ " (NOLOCK) WHERE PROFILE_ID = '"
					+ str(permissions_id_val)
					+ "' AND "
					+ str(autoNumber)
					+ " = '"
					+ str(RECORD_ID)
					+ "'"
				)
			elif str(ObjectName) == "SYPROH" and TreeParam == "Object Level Permissions" and MODE == "EDIT":				
				autoNumber = "PROFILE_OBJECT_RECORD_ID"
				permissions_id_val = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00128").GetValue()
				script = (
					"SELECT "
					+ str(API_NAMES)
					+ " FROM "
					+ str(ObjectName)
					+ " (NOLOCK) WHERE PROFILE_ID = '"
					+ str(permissions_id_val)
					+ "' AND "
					+ str(autoNumber)
					+ " = '"
					+ str(RECORD_ID)
					+ "'"
				)
			elif str(ObjectName) == "SAQSRA":
				if TreeParam.startswith("Sending"):
					script = (
						"SELECT "
						+ str(API_NAMES)
						+ " FROM "
						+ str(ObjectName)
						+ " (NOLOCK) WHERE "
						+ str(autoNumber)
						+ " = '"
						+ str(RECORD_ID)
						+ "' AND RELOCATION_TYPE LIKE '%SENDING%'"
					)
				elif TreeParam.startswith("Receiving"):
					script = (
						"SELECT "
						+ str(API_NAMES)
						+ " FROM "
						+ str(ObjectName)
						+ " (NOLOCK) WHERE "
						+ str(autoNumber)
						+ " = '"
						+ str(RECORD_ID)
						+ "' AND RELOCATION_TYPE LIKE '%RECEIVING%'"
					)
			# elif ObjectName == "SAQITM":
			# 	Trace.Write("test74_J "+str(RECORD_ID))
			# 	Trace.Write("Treeparam"+str(TreeParam))
			# 	#RECORD_ID = RECORD_ID.split("|")[0]
			# 	Trace.Write("test746--quote_record_id--00--------"+str(RECORD_ID))
			# 	quote_record_id = Quote.GetGlobal("contract_quote_record_id")
			# 	Trace.Write("test746---quote_record_id-----"+str(quote_record_id))
			# 	RECORD_ID = TreeParam.split("-")[0].strip()
			# 	script = (
			# 		"SELECT "
			# 		+ str(API_NAMES)
			# 		+ " FROM "
			# 		+ str(ObjectName)
			# 		+ " (NOLOCK) WHERE "
			# 		+ str(autoNumber)
			# 		+ " = '"
			# 		+ str(RECORD_ID) 
			# 		+ "' AND  QUOTE_RECORD_ID = '"+str(quote_record_id)+"'"
			# 		+ " AND  QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"'"
			# 	)
			elif ObjectName == "SAQICO":
				RECORD_ID = primary_value
				Trace.Write("line_item--quote_record_id--00--------"+str(RECORD_ID))
				quote_record_id = Quote.GetGlobal("contract_quote_record_id")
				Trace.Write("line_item---quote_record_id-----"+str(quote_record_id))
				# script = (
				# 	"SELECT "
				# 	+ str(API_NAMES)
				# 	+ " FROM "
				# 	+ str(ObjectName)
				# 	+ " (NOLOCK) WHERE "
				# 	+ str(autoNumber)
				# 	+ " = '"
				# 	+ str(RECORD_ID)
				# 	+ "'"
				# )
				script = (
					"SELECT "
					+ str(API_NAMES)
					+ " FROM "
					+ str(ObjectName)
					+ " (NOLOCK) WHERE QUOTE_RECORD_ID "
					+ " = '"
					+ str(quote_record_id)
					+ "' and LINE = '"+str(RECORD_ID)+"'"
					+ ""
				)
			elif ObjectName == "SAQTRV":
				RECORD_ID = RECORD_ID.split("|")[0]
				Trace.Write("test746--quote_record_id--00--------"+str(RECORD_ID))
				quote_record_id = Quote.GetGlobal("contract_quote_record_id")
				Trace.Write("test746---quote_record_id-----"+str(quote_record_id))
				script = (
					"SELECT "
					+ str(API_NAMES)
					+ " FROM "
					+ str(ObjectName)
					+ " (NOLOCK) WHERE "
					+ str(autoNumber)
					+ " = '"
					+ str(RECORD_ID)
					+ "'"
					+ ""
				)
			elif ObjectName == "SAQRIB" and TreeParentParam == "Billing":
				RECORD_ID = RECORD_ID.split("|")[0]
				Trace.Write("test746--867-----TreeParam-----"+str(TreeParam))
				quote_record_id = Quote.GetGlobal("contract_quote_record_id")
				Trace.Write("test746---quote_record_id-----"+str(quote_record_id))
				script = (
					"SELECT "
					+ str(API_NAMES)
					+ " FROM "
					+ str(ObjectName)
					+ " (NOLOCK) WHERE QUOTE_RECORD_ID "
					+ " = '"
					+ str(quote_record_id)
					+ "' and PRDOFR_ID = '"+str(TreeParam)+"'"
					+ ""
				)
			elif ObjectName == "ACAPCH" and TreeParam == "Approval Chain Information":
				RECORD_ID = RECORD_ID.split("|")[0]
				quote_record_id = Quote.GetGlobal("contract_quote_record_id")
				script = (
					"SELECT "
					+ str(API_NAMES)
					+ " FROM "
					+ str(ObjectName)
					+ " (NOLOCK) WHERE "
					+ str(autoNumber)
					+ " = '"
					+ str(RECORD_ID)
					+ "'"
				)
			else:	
				Trace.Write("test746"+str(API_NAMES))		
				RECORD_ID = RECORD_ID.split("|")[0]
				Trace.Write("test746--quote_record_id--00--------"+str(RECORD_ID))
				quote_record_id = Quote.GetGlobal("contract_quote_record_id")
				Trace.Write("test746---quote_record_id-----"+str(quote_record_id))
				if current_prod == "Sales" and ObjectName != "ACAPMA" and ObjectName != "ACAPTX" and ObjectName != "ACACHR":
					if ObjectName == "SAQDOC":
						script = (
							"SELECT "
							+ str(API_NAMES)
							+ " FROM "
							+ str(ObjectName)
							+ " (NOLOCK) WHERE QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"'"
						)
					else:
						script = (
							"SELECT "
							+ str(API_NAMES)
							+ " FROM "
							+ str(ObjectName)
							+ " (NOLOCK) WHERE "
							+ str(autoNumber)
							+ " = '"
							+ str(RECORD_ID)
							+ "'"
							+ " AND  QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"'"
						)
				else:
					script = (
						"SELECT "
						+ str(API_NAMES)
						+ " FROM "
						+ str(ObjectName)
						+ " (NOLOCK) WHERE "
						+ str(autoNumber)
						+ " = '"
						+ str(RECORD_ID)
						+ "'"
					)
			Custom_obj = Sql.GetFirst(script)
			Trace.Write("ObjName"+str(ObjectName))
			Trace.Write("TreeParam"+str(TreeParam))
			
			
		except:
			Trace.Write("Test2")
			script = (
				"SELECT * FROM " + str(ObjectName) + " (NOLOCK) WHERE " + str(autoNumber) + " = '" + str(RECORD_ID) + "'"
			)
			Custom_obj = Sql.GetFirst(script)
		Trace.Write('862-----------')
		if data_obj is not None:
			Trace.Write('862----864-------')			
			for val in data_obj:				
				readonly = "readonly"
				disable = "disabled"
				current_obj_api_name = val.API_NAME.strip()
				current_obj_field_lable = val.FIELD_LABEL.strip()
				readonly_val = val.PERMISSION.strip()
				hint_text = val.HELP_TEXT_TITLE.strip()
				hint_text_Copy = val.HELP_TEXT_COPY.strip()
				data_type = val.DATA_TYPE.strip()
				formula_data_type = ""
				max_length = val.LENGTH
				if str(val.FORMULA_DATA_TYPE) != "" and len(str(val.FORMULA_DATA_TYPE)) > 0:
					formula_data_type = val.FORMULA_DATA_TYPE
				erp_source = str(val.SOURCE_DATA)
				current_obj_value = ""
				header_obj_value = ""
				datepicker = "onclick_datepicker('" + current_obj_api_name + "')"
				ids = ""
				add_style = ""
				idval = ""
				edit_warn_icon = ""
				formula_permission = ""
				formula_obj_permission = ""
				left_float = ""
				id_val = ""
				id_api = ""
				priceclass_val = ""
				keypressval = ""
				onchange = ""
				datepicker_onchange = "onchangedatepicker('" + current_obj_api_name + "')"
				Trace.Write("CURRENTOBJAPINAME===="+str(current_obj_api_name))
				if Custom_obj is not None:
					try:
						current_obj_value = eval(
							str("Custom_obj." + str(current_obj_api_name).encode("ascii", "ignore")).strip()
						)
						current_obj_value = str(current_obj_value)						
					except UnicodeEncodeError:
						current_obj_value = current_obj_value
					except:
						Trace.Write("Error--900")
				if action_visible_str:
					edit_pencil_icon = '<i class="fa fa-lock" aria-hidden="true"></i>'
					
				elif readonly_val.upper() != "READ ONLY" and data_type != "AUTO NUMBER" and erp_source != "ERP":					
					edit_pencil_icon = '<i class="fa fa-pencil" aria-hidden="true"></i>'
				else:					
					edit_pencil_icon = '<i class="fa fa-lock" aria-hidden="true"></i>'
				if len(current_obj_value) > 0:
					current_obj_value = current_obj_value
				else:
					current_obj_value = ""
				if current_obj_api_name.upper() == "CPQTABLEENTRYMODIFIEDBY":				
					if current_obj_value != "":
						current_obj_value = Sql.GetFirst(
							"SELECT USERNAME FROM USERS WHERE ID = " + str(current_obj_value) + ""
						).USERNAME
				if current_obj_api_name in lookup_val:
					for key, value in lookup_list.items():
						if key == current_obj_api_name:
							ids = value.strip()
							
				if current_obj_api_name in lookup_val:
					formula_obj_permission = "true"
					for key, value in lookup_list1.items():
						if key == current_obj_api_name:
							formula_permission_qry = Sql.GetFirst(
								"SELECT * FROM SYOBJD WITH (NOLOCK) WHERE API_NAME = '"
								+ str(value)
								+ "' AND OBJECT_NAME = '"
								+ str(ObjectName)
								+ "' "
							)
							if formula_permission_qry is not None:
								formula_permission = str(formula_permission_qry.PERMISSION).strip()
				if MODE == "VIEW":					
					if (readonly_val == "" or readonly_val.upper() == "EDITABLE") and canedit.upper() == "TRUE":						
						edit_pencil_icon = '<i class="fa fa-pencil" aria-hidden="true"></i>'
					elif readonly_val == "EDITABLE":						
						edit_pencil_icon = '<i class="fa fa-pencil" aria-hidden="true"></i>'
					else:						
						edit_pencil_icon = '<i class="fa fa-lock" aria-hidden="true"></i>'
						disable = "disabled"						
				else:
					if readonly_val == "READ ONLY":
						if (
							formula_obj_permission.upper() == "TRUE"
							and formula_permission != "READ ONLY"
							and canedit.upper() == "TRUE"
						):							
							edit_pencil_icon = '<i class="fa fa-pencil" aria-hidden="true"></i>'
							if MODE == "EDIT":
								readonly = ""
								disable = ""
						else:							
							edit_pencil_icon = '<i class="fa fa-lock" aria-hidden="true"></i>'
							readonly = "readonly"
							disable = "disabled"
					elif MODE == "EDIT":
						if erp_source != "ERP":							
							edit_pencil_icon = '<i class="fa fa-pencil" aria-hidden="true"></i>'
							readonly = ""
							disable = ""
						elif (readonly_val == "" or readonly_val.upper() == "EDITABLE") and canedit.upper() == "TRUE":
							edit_pencil_icon = '<i class="fa fa-pencil" aria-hidden="true"></i>'
							readonly = ""
							disable = ""
						else:							
							edit_pencil_icon = '<i class="fa fa-lock" aria-hidden="true"></i>'
							readonly = "readonly"
							disable = "disabled"
				
				if ObjectName == "SAQIBP" and TreeParam == "Billing Plan":
					notinlist = [
						"QUOTE_ID",											
						"SPLIT_BILLING",						
						"CPQTABLEENTRYADDEDBY",
						"CPQTABLEENTRYDATEADDED",
						"CpqTableEntryModifiedBy",
						"CpqTableEntryDateModified",
					]
					if current_obj_api_name in notinlist:
						add_style = "display: none;"
				
				##suppress PAR_SERVICE_ID and PAR_SERVICE_DESCRIPTION if value is null starts
				if ObjectName == "SAQTSV":
					if current_obj_api_name == 'PAR_SERVICE_ID' and not current_obj_value:
						add_style = "display: none;"
					elif current_obj_api_name == 'PAR_SERVICE_DESCRIPTION' and not current_obj_value:
						add_style = "display: none;"
				##suppress PAR_SERVICE_ID and PAR_SERVICE_DESCRIPTION if value is null ends

				if ObjectName == "SAQTMT" and TreeParam == "Sales":
					noninlist = [
						"SALESORG_CURRENCY",
						"SALESOFFICE_ID",
						"DISTRIBUTIONCHANNEL_ID",
						"DIVISION_ID",
						"PRICINGPROCEDURE_ID",
						"PRICINGPROCEDURE_NAME",
						"REASONFOR_REJECTION",
						"PREDECESSOR_CONTRACT_ID",
						"PREDECESSOR_CONTRACT_NAME",
						"PARENTQUOTE_ID",
						"PARENTQUOTE_NAME",
						"EMPLOYEE_ID",
						"NET_VALUE",
						"OPPORTUNITY_NAME",
						"ACCOUNT_ID",
						"ACCOUNT_NAME"
					]
					if current_obj_api_name in noninlist:						
						add_style = "display: none;"	
				if ObjectName == "SAQRIB" and TreeParam == "Billing":
					noninlist = [						
						"SALESORG_ID",
						"SALESORG_NAME"					
					]
					if current_obj_api_name in noninlist:
						add_style = "display: none;"		
				if ObjectName == "SAQFBL" and TreeParentParam == "Fab Locations":
					notinlist = ["ADDRESS_2"]
					if current_obj_api_name in notinlist:						
						add_style = "display: none;"
				if ObjectName == "PREXRT" and TreeParam == "Exchange Rates":
					notinlistt = ["EXCHANGE_RATE_TYPE"]
					if current_obj_api_name in notinlistt:						
						add_style = "display: none;"			
				if ObjectName == "SAQDOC" and TreeParam == "Quote Documents":
					notinlist = ["QUOTE_ID", "QUOTE_NAME", "DOCUMENT_PATH","QUOTE_DOCUMENT_RECORD_ID"]
					if current_obj_api_name in notinlist:
						add_style = "display: none;"
				if (ObjectName == "ACACST" or ObjectName == "ACAPTF" or ObjectName == "ACACSS" or ObjectName == "ACACSA" or ObjectName == "ACAPMA") and (MODE == "VIEW" or MODE == "EDIT" or MODE == "CANCEL"):	
					hidelist = ["APRCHN_ID", "TSTOBJ_TESTEDFIELD_LABEL", "OWNER_ID", "OWNED_DATE", "ENABLE_SMARTAPPROVAL"]
					if 	current_obj_api_name in hidelist:
						add_style = "display: none;"
				if ObjectName == "ACACSS" and (MODE == "VIEW" or MODE == "EDIT"):	
					hidelist = ["APPROVAL_CHAIN_STATUS_MAPPING_RECORD_ID"]
					if 	current_obj_api_name in hidelist:
						add_style = "display: none;"
				if ObjectName == "ACAPMA" and TreeParentParam == "Approvals":
					notinlist = ["OWNER_ID", "OWNED_DATE"]
					if current_obj_api_name in notinlist:
						add_style = "display: none;"
				if ObjectName == "ACAPTX":
					notinlist = ["ARCHIVED"]
					if current_obj_api_name in notinlist:
						add_style = "display: none;"
				if ObjectName == "":
					notinlist = ["ADDRESS_2"]
					##suppress PAR_SERVICE_ID and PAR_SERVICE_DESCRIPTION if value is null starts
					if current_obj_api_name == 'PAR_SERVICE_ID' and not current_obj_value:
						notinlist.append(current_obj_api_name)
					elif current_obj_api_name == 'PAR_SERVICE_DESCRIPTION' and not current_obj_value:
						notinlist.append(current_obj_api_name)
					##suppress PAR_SERVICE_ID and PAR_SERVICE_DESCRIPTION if value is null ends
					if current_obj_api_name in notinlist:
						add_style = "display: none;"	
				if ObjectName == "SAQFGB":
					notinlist = ["QUOTE_FAB_LOC_GB_RECORD_ID"]
					if current_obj_api_name in notinlist:
						add_style = "display: none;"
				elif ObjectName == "SAQSGB":
					notinlist = ["QUOTE_SERVICE_GREENBOOK_RECORD_ID"]
					##suppress PAR_SERVICE_ID and PAR_SERVICE_DESCRIPTION if value is null starts
					if current_obj_api_name == 'PAR_SERVICE_ID' and not current_obj_value:
						notinlist.append(current_obj_api_name)
					elif current_obj_api_name == 'PAR_SERVICE_DESCRIPTION' and not current_obj_value:
						notinlist.append(current_obj_api_name)
					##suppress PAR_SERVICE_ID and PAR_SERVICE_DESCRIPTION if value is null ends
					if current_obj_api_name in notinlist:
						add_style = "display: none;"
				# elif ObjectName == "SAQIGB":
				# 	notinlist = ["QUOTE_ITEM_GREENBOOK_RECORD_ID"]
				# 	if current_obj_api_name in notinlist:
				# 		add_style = "display: none;"
				# elif ObjectName == "SAQITM":
				# 	notinlist = ["SRVTAXCLA_ID","SALESORG_NAME","SALESORG_ID","REMAINING_QUANTITY","RELEASED_QUANTITY","PO_ITEM","PO_NOTES","PO_NUMBER"]
				# 	if current_obj_api_name in notinlist:
				# 		add_style = "display: none;"
				Quote_Type = Sql.GetFirst("SELECT QUOTE_TYPE FROM SAQTMT (NOLOCK) WHERE MASTER_TABLE_QUOTE_RECORD_ID = '"+str(contract_quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' ")
				if Quote_Type is not None:
					if Quote_Type.QUOTE_TYPE == "ZWK1 - SPARES":
						if ObjectName == "SAQTRV":
							notinlist = [
								"EXCHANGE_RATE_DATE",
								"EXCHANGE_RATE"
							]
							if current_obj_api_name in notinlist:
								add_style = "display: none;"
				if data_type == "LOOKUP":
					add_style = "display: none;"

				displaynoneList = [
					"ACCOUNT_NAME",
					"STP_ACCOUNT_ID",
					"STP_ACCOUNT_NAME",
					"ACCOUNT_ID",
					"CRITERIA_01",
					"CRITERIA_02",
					"CRITERIA_03",
					"CRITERIA_04",
					"CRITERIA_05",
				]

				sec_str += (
					'<tr class="iconhvr brdbt" style="'
					+ str(add_style)
					+ ' "><td class="wth350"><abbr title="'
					+ str(current_obj_field_lable)
					+ '" ><label class="pad5mrgbt0">'
					+ str(current_obj_field_lable)
					+ '</label></abbr></td><td width40><a href="#" title="'
					+ '" data-placement="auto top" data-toggle="popover" data-trigger="focus" data-content="'
					+ str(hint_text_Copy)
					+ '" class="bgcccwth10"><i class="fa fa-info-circle fltlt"></i>'
				)			
				Trace.Write("CHKZ_MODE_J "+str(MODE))
				if (str(val.REQUIRED).upper() == "TRUE" or val.REQUIRED == "1") and (MODE == "VIEW" or MODE == "EDIT" or MODE == "CANCEL") :
					sec_str += ""
					sec_str += '<span class="req-field">*</span>'
				sec_str += "</a></td>"
				if data_type == "AUTO NUMBER":					
					if current_obj_value == "":
						try:
							if RECORD_ID.startswith(ObjectName):							
								if str(ObjectName) != "USERS":

									current_obj_value = CPQID.KeyCPQId.GetKEYId(str(ObjectName), str(RECORD_ID))

								else:
									current_obj_value = RECORD_ID
							else:
								current_obj_value = RECORD_ID
						except:
							Trace.Write('check error')
					if current_obj_api_name == "approve_condition_id" and ObjectName == "approve_condition":
						current_obj_value = current_obj_value
					elif ObjectName == 'SAQRIB' and TreeParam == "Billing":		# Billing Matrix Details Load - Start				
						billing_plan_obj = Sql.GetFirst(
									"SELECT CpqTableEntryId FROM {ObjectName} (NOLOCK) where QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID='{revision_rec_id}'".format(
										ObjectName=ObjectName, QuoteRecordId=quote_record_id,revision_rec_id = quote_revision_record_id)
								)
						if billing_plan_obj:
							billing_cpq_table_entry_id = billing_plan_obj.CpqTableEntryId
							if billing_cpq_table_entry_id:
									KeyId = str(ObjectName) + "-" + str(billing_cpq_table_entry_id).rjust(5, "0")
									current_obj_value = KeyId
									# Billing Matrix Details Load - End
					else:						
						if (
							str(ObjectName) != "USERS"
							and str(ObjectName) != "SYTABS"
							and str(ObjectName) != "SYSECT"
							and str(ObjectName) != "SYPROH"
						):
							current_obj_value = CPQID.KeyCPQId.GetCPQId(str(ObjectName), str(current_obj_value))
							
						elif str(ObjectName) == "SYSECT":
							current_obj_value = CPQID.KeyCPQId.GetCPQId(str(ObjectName), str(current_obj_value))
							
						elif str(ObjectName) == "SYTABS":
							current_obj_value = CPQID.KeyCPQId.GetCPQId(str(ObjectName), str(current_obj_value))
							
						elif str(ObjectName) == "SYPROH" and MODE == "VIEW":				
							permissions_id_val = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00128").GetValue()							
							CPQIDVAL = ""
							if TreeParam != "Object Level Permissions":						
								cpqidquery = Sql.GetFirst(
									"SELECT CpqTableEntryId FROM SYPROH (NOLOCK) where PROFILE_ID = '"
									+ str(permissions_id_val)
									+ "' and PROFILE_OBJECT_RECORD_ID = '"
									+ str(RECORD_ID)
									+ "' "
								)
							else:								
								cpqidquery = Sql.GetFirst(
									"SELECT CpqTableEntryId FROM SYPROH (NOLOCK) where PROFILE_ID = '"
									+ str(permissions_id_val)
									+ "' and PROFILE_OBJECT_RECORD_ID = '"
									+ str(RECORD_ID)
									+ "' "
								)
							if cpqidquery is not None:
								CPQIDVAL = cpqidquery.CpqTableEntryId
								if CPQID != "":
									KeyId = str(ObjectName) + "-" + str(CPQIDVAL).rjust(5, "0")
									current_obj_value = KeyId
							
						elif str(ObjectName) == "SYPROH" and MODE == "EDIT":				
							permissions_id_val = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00128").GetValue()							
							CPQIDVAL = ""
							cpqidquery = Sql.GetFirst(
								"SELECT CpqTableEntryId FROM SYPROH (NOLOCK) where PROFILE_ID = '"
								+ str(permissions_id_val)
								+ "' and PROFILE_OBJECT_RECORD_ID = '"
								+ str(RECORD_ID)
								+ "' "
							)
							if cpqidquery is not None:
								CPQIDVAL = cpqidquery.CpqTableEntryId
								if CPQID != "":
									KeyId = str(ObjectName) + "-" + str(CPQIDVAL).rjust(5, "0")
									current_obj_value = KeyId
							
						elif str(ObjectName) == "SYPROH" and MODE == "CANCEL":				
							permissions_id_val = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00128").GetValue()							
							CPQIDVAL = ""
							cpqidquery = Sql.GetFirst(
								"SELECT CpqTableEntryId FROM SYPROH (NOLOCK) where PROFILE_ID = '"
								+ str(permissions_id_val)
								+ "' and PROFILE_OBJECT_RECORD_ID = '"
								+ str(RECORD_ID)
								+ "' "
							)
							if cpqidquery is not None:
								CPQIDVAL = cpqidquery.CpqTableEntryId
								if CPQID != "":
									KeyId = str(ObjectName) + "-" + str(CPQIDVAL).rjust(5, "0")
									current_obj_value = KeyId							

					sec_str += (
						'<td><input id="'
						+ str(current_obj_api_name)
						+ '" type="text" value="'
						+ current_obj_value
						+ '" title="'
						+ str(current_obj_value)
						+ '" class="form-control related_popup_css" disabled></td>'
					)
					auto_field = (
						'<tr style="display: none;" class="iconhvr brdbt" style=" '
						+ str(add_style)
						+ '"><td class="wth350"><abbr title="'
						+ str(current_obj_field_lable)
						+ '"><label class="pad5mrgbt0">'
						+ str(current_obj_field_lable)
						+ '</label></td></abbr><td class="width40"><a href="#" data-placement="auto top" data-toggle="popover" data-content="'
						+ str(hint_text)
						+ '" class="bgcccwth10"><i  class="fa fa-info-circle fltlt"></i><td><input id="'
						+ str(current_obj_api_name)
						+ '" type="text" value="'
						+ current_obj_value
						+ '" title="'
						+ str(current_obj_value)
						+ '" class="form-control related_popup_css" disabled></td><tr>'
					)
					#Trace.Write("cm to this data-original"+str(auto_field))
				
				elif data_type == "LONG TEXT AREA":
					if str(MODE)=="VIEW" or str(MODE)=="CANCEL":							
						sec_str += (
							'<td><textarea title="'
							+ str(current_obj_value)
							+ '" class="form-control related_popup_css txtArea" id="'
							+ str(current_obj_api_name)
							+ '" rows="1" cols="100" '
							+ disable
							+ ">"
							+ current_obj_value
							+ "</textarea></td>"
						)
					else:																	
						sec_str += (
							'<td><textarea title="'
							+ str(current_obj_value)
							+ '" class="form-control related_popup_css txtArea " id="'
							+ str(current_obj_api_name)
							+ '" rows="1" cols="100" '
							+ disable							
							+ ">"
							+ current_obj_value
							+ "</textarea></td>"
						)						
				elif data_type == "LOOKUP":
					sec_str += (
						'<td><input id="'
						+ str(current_obj_api_name)
						+ '" type="text" value="'
						+ current_obj_value
						+ '" title="'
						+ str(current_obj_value)
						+ '" class="form-control related_popup_css" disabled></td>'
					)
				
				elif data_type == "PERCENT" or formula_data_type == "PERCENT":
					Trace.Write("else 1404"+str(current_obj_api_name)) 
					Coeff_values =""
					symbol = " %"
					if str(ObjectName) == "SAQICO":
						symbol =""
					Decimal_Value = 2 if str(ObjectName) == 'SAQIGB' else 3  ## decimal precision for SAQIGB
					Decimal_Values = 2										
					if current_obj_value and str(ObjectName) == "SAQICO" and str(current_obj_api_name) =="FAB_VALUEDRIVER_COEFFICIENT" or str(current_obj_api_name) == "TOOL_VALUEDRIVER_COEFFICIENT":					
						#my_format = "{:." + str(Decimal_Values) + "f}"
						Coeff_values = str(current_obj_value)
						if Coeff_values !='':
							#Coeff_values = str(current_obj_value)
							
							current_obj_value =str(float(Coeff_values)*float(100))
						else:
							current_obj_value = str(Coeff_values)
					if current_obj_value and str(ObjectName) != "SAQICO":
						Trace.Write("if-----")
						my_format = "{:." + str(Decimal_Value) + "f}"
						current_obj_value = str(my_format.format(round(float(current_obj_value), int(Decimal_Value))))
					if current_obj_value and str(ObjectName) == "SAQICO":
						Trace.Write("if-----111"+str(current_obj_value))
						try:
							my_format = "{:." + str(Decimal_Values) + "f}"
							current_obj_value = str(current_obj_value).replace('%','')
							current_obj_value = str(my_format.format(round(float(current_obj_value), int(Decimal_Values))))
							current_obj_value = str(current_obj_value) + '%'
						except:
							current_obj_value = str(current_obj_value)													
					

						#my_format = "{:." + str(Decimal_Values) + "f}"
						#current_obj_value = str(current_obj_api_name*int(100))				
					if current_obj_value == "":
						symbol = ""
					if current_obj_api_name == "DISCOUNT" and MODE == "EDIT":
						Trace.Write("@1809 inside discount")
						sec_str += (
							'<td><input id="'
							+ str(current_obj_api_name)
							+ '" type="text" value="'
							+ current_obj_value.lstrip()
							+ '" title="'
							+ current_obj_value
							+ '" class="form-control related_popup_css light_yellow" style="'
							+ str(left_float)
							+ ' " '
							+ disable
							+ " maxlength = '"+str(max_length)+"'>"
							+ str(edit_warn_icon)
							+ "</td>"
						)
					else:
						sec_str += (
							'<td><input id="'
							+ str(current_obj_api_name)
							+ '" type="text" value="'
							+ current_obj_value
							+ symbol
							+ '" title="'
							+ current_obj_value
							+ symbol
							+ '" class="form-control related_popup_css" disabled></td>'
						)	
								
						
				elif (
					data_type == "FORMULA"
					and MODE == "EDIT"
					and formula_data_type != "CHECKBOX"
					and formula_data_type != "CURRENCY"
				):	
					Trace.Write(str(lookup_val)+'--lookup_val---'+str(readonly)+'current_obj_api_name--1440---'+str(current_obj_api_name))
					##A055S000P01-10459 code starts...
					# if current_obj_api_name == "EXCHANGE_RATE_TYPE":
					# 	revision_object = SqlHelper.GetFirst("select REGION FROM SAQTRV where QUOTE_RECORD_ID = '{}' and QTEREV_RECORD_ID = '{}'".format(Quote.GetGlobal("contract_quote_record_id"),Quote.GetGlobal("quote_revision_record_id")))
					# 	if revision_object.REGION == "AMC" or revision_object.REGION == "AMK":
					# 		readonly = ""
					# 	else:
					# 		readonly = "readonly"
					##A055S000P01-10459 code ends...
					if current_obj_api_name in lookup_val and str(readonly) != "readonly":
						Trace.Write(str(readonly)+'current_obj_api_name--1443---'+str(current_obj_api_name))	
						sec_str += (
							'<td><input id="'
							+ str(current_obj_api_name)
							+ '" type="text" value="'
							+ current_obj_value
							+ '" title="'
							+ str(current_obj_value)
							+ '" class="form-control lookupBg related_popup_css fltlt" readonly>'
						)
						sec_str += (
							'<input class="popup fltlt" id="'
							+ str(ids)
							+ '|" onclick="'
							+ str(lookup_popup)
							+ '"   type="image" data-toggle="modal" data-target="#cont_viewModalSection"  src="../mt/default/images/customer_lookup.gif"></td>'
						)
					else:
						if str(formula_data_type) == "TEXT" and str(readonly) != "readonly":			
							Trace.Write('api---1398----'+str(current_obj_api_name))
							sec_str += (
								'<td><input id="'
								+ str(current_obj_api_name)
								+ '" type="text" value="'
								+ current_obj_value
								+ '" title="'
								+ current_obj_value
								+ '" class="form-control related_popup_css fltlt" style="'
								+ str(left_float)
								+ ' ">'
								+ str(edit_warn_icon)
								+ "</td>"
							)
						# elif current_obj_api_name in ["CONTRACT_VALID_FROM","CONTRACT_VALID_TO"] and ObjectName == "SAQSCO":
						# 	sec_str += (
						# 		'<td><input id="'
						# 		+ str(current_obj_api_name)
						# 		+ '" value="'
						# 		+ current_obj_value
						# 		+ '" type="text"  onclick="'
						# 		+ str(datepicker)
						# 		+ '"  class="form-control datePickerField wth157fltltbrdbt"   '
						# 		+ disable
						# 		+ " ></td>"
						# 	)
						elif (
							str(current_obj_api_name) == "MESSAGE_HEADERVALUE"
							or str(current_obj_api_name) == "MESSAGE_BODYVALUE"
						):
							GetPrimeKey = Product.Attributes.GetByName("QSTN_SYSEFL_AC_00075").GetValue()
							sec_str += "<td>"
							sec_str += (
								'<div class="col-md-4 pad-0"><div id="div_PICKLISTLOAD_'
								+ str(current_obj_api_name)
								+ '" class="multiselect"><select id="First'
								+ str(current_obj_api_name)
								+ '" multiple="multiple"'
								+ str(onchange)
								+ ' value="'
								+ current_obj_value
								+ '" class="form-control pop_up_brd_rad related_popup_css fltlt options_'
								+ str(current_obj_api_name)
								+ ' "  '
								+ disable
								+ " ><option value='Select'>..Select</option>"
							)
							currectvaluelist = current_obj_value.split(",")
							splitedlist = str(currectvaluelist).replace("[", "").replace("]", "")
							if len(currectvaluelist) == 1 and currectvaluelist[0] == "":
								splitedlist = "'1'"
							if str(current_obj_api_name) == "MESSAGE_HEADERVALUE":
								Tier_List = Sql.GetList(
									"""SELECT SYOBJD.FIELD_LABEL  FROM ACAPCH (NOLOCK) INNER JOIN SYOBJH (NOLOCK)
									ON ACAPCH.APROBJ_RECORD_ID = SYOBJH.RECORD_ID INNER JOIN SYOBJD (NOLOCK)
									ON SYOBJD.OBJECT_NAME = SYOBJH.OBJECT_NAME WHERE
									APPROVAL_CHAIN_RECORD_ID = '{chainrecordId}'
									AND SYOBJD.FIELD_LABEL NOT in ({exceptlist})""".format(
										chainrecordId=str(GetPrimeKey), exceptlist=splitedlist
									)
								)
							else:
								Tier_List = Sql.GetList(
									"""SELECT SYOBJD.FIELD_LABEL FROM ACACST (NOLOCK) INNER JOIN SYOBJH (NOLOCK)
									ON ACACST.TSTOBJ_RECORD_ID = SYOBJH.RECORD_ID
									INNER JOIN SYOBJD (NOLOCK) ON SYOBJD.OBJECT_NAME = SYOBJH.OBJECT_NAME
									WHERE ACACST.APRCHN_RECORD_ID = '{chainrecordId}'
									AND ACACST.APRCHNSTP_NAME = '{TreeParam}'
									AND SYOBJD.FIELD_LABEL NOT in ({exceptlist}) """.format(
										chainrecordId=str(GetPrimeKey), TreeParam=TreeParam.split(': ')[1], exceptlist=splitedlist
									)
								)
							for req1 in Tier_List:
								if current_obj_value == req1:
									sec_str += "<option>" + str(req1.FIELD_LABEL) + "</option>"
								else:
									sec_str += "<option>" + str(req1.FIELD_LABEL) + "</option>"
							sec_str += (
								'</select><div id="button_mvmt1"> <button onclick="unselectedval(this)" '
								+ 'class="leftbutton" id ="'
								+ str(current_obj_api_name)
								+ '"> <i class="glyphicon glyphicon-triangle-left"></i> </button> '
								+ '<button onclick="selectedval(this)" id ="'
								+ str(current_obj_api_name)
								+ '" class="rightbutton"> <i class="glyphicon glyphicon-triangle-right"></i> </button> '
								+ '</div><select multiple="multiple" id="options1_'
								+ str(current_obj_api_name)
								+ '" >'
							)
							for listval in currectvaluelist:
								sec_str += "<option>" + str(listval) + "</option>"
							sec_str += (
								'</select><div id="button_mvmt"> <button class="topbutton" onclick="topselect(this)" id ="'
								+ str(current_obj_api_name)
								+ '"> <i class="glyphicon glyphicon-triangle-top"></i> </button> <button class="btmbutton"'
								+ ' onclick="btmselect(this)"id ="'
								+ str(current_obj_api_name)
								+ '" ><i class="glyphicon glyphicon-triangle-bottom"></i> </button> </div></div></div></td>'
							)
						
						elif current_obj_api_name in ["CONTRACT_VALID_FROM","CONTRACT_VALID_TO"]:
							Trace.Write("Quote_Items_CONTRACT_EDITABILTY")
							sec_str += (
								'<td><input id="'
								+ str(current_obj_api_name)
								+ '" value="'
								+ current_obj_value
								+ '" type="text"  onclick="'
								+ str(datepicker)
								+ '"  class="form-control datePickerField wth157fltltbrdbt light_yellow"   '
								+ disable
								+ " ></td>"
							)
						else:							
							sec_str += (
								'<td><input id="'
								+ str(current_obj_api_name)
								+ '" type="text" value="'
								+ current_obj_value
								+ '" title="'
								+ current_obj_value
								+ '" class="form-control related_popup_css fltlt" style="'
								+ str(left_float)
								+ ' " disabled>'
								+ str(edit_warn_icon)
								+ "</td>"
							)
				elif data_type == "CHECKBOX":
					Trace.Write('1472----------'+str(current_obj_value))					
					if str(current_obj_value).upper() == "TRUE" or current_obj_value == "1":
						sec_str += (
							'<td><input id="'
							+ str(current_obj_api_name)
							+ '" type="'
							+ str(data_type)
							+ '" value="'
							+ current_obj_value
							+ '" class="custom" '
							+ disable
							+ ' checked><span class="lbl"></span></td>'
						)
					elif str(ObjectName) == "USERS":
						Trace.Write('1472----USERSA------'+str(current_obj_value))
						if str(current_obj_value).upper() == "TRUE" or current_obj_value == "1":
							sec_str += (
								'<td><input id="'
								+ str(current_obj_api_name)
								+ '" type="'
								+ str(data_type)
								+ '" value="'
								+ current_obj_value
								+ '" class="custom" '
								+ disable
								+ ' checked><span class="lbl"></span></td>'
							)
						else:
							sec_str += (
								'<td><input id="'
								+ str(current_obj_api_name)
								+ '" type="'
								+ str(data_type)
								+ '" value="'
								+ current_obj_value
								+ '" class="custom" '
								+ disable
								+ '><span class="lbl"></span></td>'
							)
					else:
						sec_str += (
							'<td><input id="'
							+ str(current_obj_api_name)
							+ '" type="'
							+ str(data_type)
							+ '" value="False" class="custom" '
							+ disable
							+ '><span class="lbl"></span></td>'
						)
				elif data_type == "FORMULA" and formula_data_type == "CHECKBOX" and formula_data_type != "CURRENCY":					
					if str(current_obj_value).upper() == "TRUE" or current_obj_value == "1":
						sec_str += (
							'<td><input id="'
							+ str(current_obj_api_name)
							+ '" type="CHECKBOX" value="'
							+ current_obj_value
							+ '" class="custom" '
							+ disable
							+ ' checked><span class="lbl"></span></td>'
						)			
						
					else:
						sec_str += (
							'<td><input id="'
							+ str(current_obj_api_name)
							+ '" type="CHECKBOX" value="False" class="custom" '
							+ disable
							+ '><span class="lbl"></span></td>'
						)

				elif data_type == "PICKLIST" and MODE == "EDIT":
					#Trace.Write("apiname--1574----"+str(current_obj_api_name))
					#Trace.Write("current_obj_value--1574----"+str(current_obj_value))					
					if str(ObjectName) == 'ACACSA' or (str(ObjectName)== "SAQTMT" and SubtabName == "Idling Attributes"):						
						sec_str += "<td>"
						sec_str += (
							'<select id="'
							+ str(current_obj_api_name)
							+ '" '
							+ str(onchange)
							+ ' value="'
							+ current_obj_value
							+ '" type="text" title="'
							+ str(current_obj_value)
							+ '" class="form-control pop_up_brd_rad related_popup_css fltlt" onchange = "onchangeFunction(this)" '
							+ disable
							+ " ><option value='Select'>..Select</option>"
						)
						Sql_Quality_Tier = Sql.GetFirst(
							"select PICKLIST_VALUES FROM  SYOBJD WITH (NOLOCK) where OBJECT_NAME='"
							+ str(ObjectName)
							+ "' and DATA_TYPE='PICKLIST' and API_NAME = '"
							+ str(current_obj_api_name)
							+ "' "
						)
					# elif str(current_obj_api_name) == "APPDTE_EXCH_RATE":
					# 	sec_str += "<td>"
					# 	sec_str += (
					# 		'<select id="'
					# 		+ str(current_obj_api_name)
					# 		+ '" '
					# 		+ str(onchange)
					# 		+ ' value="'
					# 		+ current_obj_value
					# 		+ 'of month" type="text" title="'
					# 		+ str(current_obj_value)
					# 		+ '" class="form-control pop_up_brd_rad related_popup_css fltlt"  '
					# 		+ disable
					# 		+ " style=\'margin-left: -1px\'><option value='Select'>..Select</option>"
					# 	)
					# 	Sql_Quality_Tier = Sql.GetFirst(
					# 		"select PICKLIST_VALUES FROM  SYOBJD WITH (NOLOCK) where OBJECT_NAME='"
					# 		+ str(ObjectName)
					# 		+ "' and DATA_TYPE='PICKLIST' and API_NAME = '"
					# 		+ str(current_obj_api_name)
					# 		+ "' "
					# 	)
					else:						
						sec_str += "<td>"
						sec_str += (
							'<select id="'
							+ str(current_obj_api_name)
							+ '" '
							+ str(onchange)
							+ ' value="'
							+ current_obj_value
							+ '" type="text" title="'
							+ str(current_obj_value)
							+ '" class="form-control pop_up_brd_rad related_popup_css fltlt"  '
							+ disable
							+ " style=\'margin-left: -1px\'><option value='Select'>..Select</option>"
						)
						Sql_Quality_Tier = Sql.GetFirst(
							"select PICKLIST_VALUES FROM  SYOBJD WITH (NOLOCK) where OBJECT_NAME='"
							+ str(ObjectName)
							+ "' and DATA_TYPE='PICKLIST' and API_NAME = '"
							+ str(current_obj_api_name)
							+ "' "
						)

					if (
						str(Sql_Quality_Tier.PICKLIST_VALUES).strip() is not None
						and str(Sql_Quality_Tier.PICKLIST_VALUES).strip() != ""
					):						
						Tier_List = (Sql_Quality_Tier.PICKLIST_VALUES).split(",")		
						for req1 in Tier_List:
							req1 = req1.strip()							
							if current_obj_value == req1:
								sec_str += "<option selected>" + str(req1) + "</option>"
							else:
								sec_str += "<option>" + str(req1) + "</option>"
					else:	
						sec_str += "<option selected>" + str(current_obj_value) + "</option>"
					sec_str += "</select></td>"
				elif data_type == "DATE" and MODE == "EDIT":								
					date_field.append(current_obj_api_name)					
					sec_str += (
						'<td><input id="'
						+ str(current_obj_api_name)
						+ '" value="'
						+ current_obj_value
						+ '" type="text"  onclick="'
						+ str(datepicker)
						+ '"  class="form-control datePickerField wth157fltltbrdbt"   '
						+ disable
						+ " ></td>"
					)
				elif data_type == "NUMBER" and str(ObjectName) == "SAQITM":					
					num_list = ['OBJECT_QUANTITY']
					if current_obj_api_name in num_list :
						string_val = str(current_obj_value)
						#string_val = string_val.replace('0','')
						string_val1 = string_val.split('.')
						str_val = str(string_val1[0])
						#str_val1 = str_val[0]+str_val[1]
						current_obj_value = str_val						
						sec_str += (
							'<td><input id="'
							+ str(current_obj_api_name)
							+ '" type="text" value="'
							+ current_obj_value
							+ '" class="form-control related_popup_css" style="'
							+ str(add_style)
							+ '" '
							+ disable
							+ "></td>"
						)
					else:
						sec_str += (
							'<td><input id="'
							+ str(current_obj_api_name)
							+ '" type="text" value="'
							+ current_obj_value
							+ '" class="form-control related_popup_css" style="'
							+ str(add_style)
							+ '" '
							+ disable
							+ "></td>"
						)											
				elif data_type == "NUMBER" and formula_data_type != "CURRENCY":	
					Trace.Write("@1737 inside discount")			
					precentage_columns = ['BD_DISCOUNT']
					precent_column = ['TARGET_PRICE_MARGIN','BD_PRICE_MARGIN','GREATER_THAN_QTLY_HRS','LESS_THAN_QTLY_HRS','LABOR_HOURS','CHAMBER_PM_HRS', 'MONTHLY_PM_HRS']					
					# if current_obj_api_name in precentage_columns and (str(ObjectName) == "SAQICO" or str(ObjectName) == "SAQITM"):						
					# 	string_val = str(current_obj_value)
					# 	#string_val = string_val.replace('0','')
					# 	string_val1 = string_val.split('.')
					# 	str_val = str(string_val1[0])
					# 	#str_val1 = str_val[0]+str_val[1]
					# 	current_obj_value = str_val
					# 	if current_obj_value != "":							
					# 		sec_str += (
					# 			'<td><input id="'
					# 			+ str(current_obj_api_name)
					# 			+ '" type="text" value="'
					# 			+ current_obj_value +" %"
					# 			+ '" class="form-control related_popup_css" style="'
					# 			+ str(add_style)
					# 			+ '" '
					# 			+ disable
					# 			+ "></td>"
					# 		)
					# 	else:
					# 		sec_str += (
					# 			'<td><input id="'
					# 			+ str(current_obj_api_name)
					# 			+ '" type="text" value="'
					# 			+ current_obj_value
					# 			+ '" class="form-control related_popup_css" style="'
					# 			+ str(add_style)
					# 			+ '" '
					# 			+ disable
					# 			+ "></td>"
					# 		)	
					# elif current_obj_api_name in precent_column and (str(ObjectName) == "SAQICO" or str(ObjectName) == "SAQITM") and str(current_obj_value) !='':					
					# 	string_val = str(current_obj_value)
					# 	#string_val = string_val.replace('0','')
					# 	string_val1 = string_val.split('.')
					# 	#str_val = str(string_val1[1])
					# 	str_vaal = str(string_val1[1])
					# 	str_val2 = str(str_vaal[0]+str_vaal[1])
					# 	strr = str(string_val1[0] +"."+ str_val2)
					# 	current_obj_value = strr
					# 	if current_obj_value != "":
					# 		sec_str += (
					# 			'<td><input id="'
					# 			+ str(current_obj_api_name)
					# 			+ '" type="text" value="'
					# 			+ current_obj_value
					# 			+ '" class="form-control related_popup_css" style="'
					# 			+ str(add_style)
					# 			+ '" '
					# 			+ disable
					# 			+ "></td>"
					# 		)
					# 	else:
					# 		sec_str += (
					# 			'<td><input id="'
					# 			+ str(current_obj_api_name)
					# 			+ '" type="text" value="'
					# 			+ current_obj_value
					# 			+ '" class="form-control related_popup_css" style="'
					# 			+ str(add_style)
					# 			+ '" '
					# 			+ disable
					# 			+ "></td>"
					# 		)								
					# else:
					Trace.Write("else 1812"+str(current_obj_api_name))
					if current_obj_api_name=='CANCELLATION_PERIOD_NOTPER':
						len_restrict= 'oninput="this.value=this.value.slice(0,this.maxLength)" maxlength="3"' 
						Trace.Write('@421'+current_obj_api_name) 
					else :
						len_restrict=""

					# if str(ObjectName) == "SAQIGB" and current_obj_value != "":
					# 	decimal_val = 2
					# 	formatting_string = "{0:." + str(decimal_val) + "f}"
					# 	current_obj_value = formatting_string.format(float(current_obj_value))
												
					sec_str += (
						'<td><input id="'
						+ str(current_obj_api_name)
						+ '" type="number"' 
						+len_restrict
						+'value="'
						+ current_obj_value
						+ '" class="form-control related_popup_css" style="'
						+ str(add_style)
						+ '" '
						+ disable
						+ "></td>"
					)
						
							
				elif data_type == "FORMULA" and formula_data_type == "NUMBER":				
					#precentage_columns = ['SALES_DISCOUNT','BD_DISCOUNT']
					precent_columns = ['BASE_PRICE_MARGIN', 'SALES_PRICE_MARGIN', 'SALES_DISCOUNT', 'BD_PRICE_MARGIN', 'YEAR_OVER_YEAR', 'LIST_PRICE_MARGIN', 'TARGET_PRICE_MARGIN']
					if current_obj_api_name in precent_columns and (str(ObjectName) == "SAQICO" or str(ObjectName) == "SAQITM") and str(current_obj_value) !='':						
						string_val = str(current_obj_value)
						#string_val = string_val.replace('0','')
						string_val1 = string_val.split('.')
						#str_val = str(string_val1[1])
						str_vaal = str(string_val1[1])
						str_val2 = str(str_vaal[0]+str_vaal[1])
						strr = str(string_val1[0] +"."+ str_val2)
						current_obj_value = strr
						if current_obj_value != "":
							sec_str += (
								'<td><input id="'
								+ str(current_obj_api_name)
								+ '" type="text" value="'
								+ current_obj_value +" %"
								+ '" class="form-control related_popup_css" style="'
								+ str(add_style)
								+ '" '
								+ disable
								+ "></td>"
							)
						else:
							
							sec_str += (
								'<td><input id="'
								+ str(current_obj_api_name)
								+ '" type="text" value="'
								+ current_obj_value
								+ '" class="form-control related_popup_css" style="'
								+ str(add_style)
								+ '" '
								+ disable
								+ "></td>"
							)	
					else:
						sec_str += (
							'<td><input id="'
							+ str(current_obj_api_name)
							+ '" type="number" value="'
							+ current_obj_value
							+ '" class="form-control related_popup_css" style="'
							+ str(add_style)
							+ '" '
							+ disable
							+ "></td>"
						)								
				elif (data_type == "CURRENCY" or formula_data_type == "CURRENCY") and MODE == "VIEW":
					curr_symbol = ""
					decimal_val = 3					
					try:
						if str(ObjectName) != "SAQICO":							
							cur_api_name = Sql.GetFirst(
								"select CURRENCY_INDEX from  SYOBJD WITH (NOLOCK) where API_NAME = '"
								+ str(current_obj_api_name)
								+ "' and OBJECT_NAME = '"
								+ str(ObjectName)
								+ "' and (DATA_TYPE = 'CURRENCY' or FORMULA_DATA_TYPE= 'CURRENCY')"
							)
							# Trace.Write(
							# 	"select CURRENCY_INDEX from  SYOBJD WITH (NOLOCK) where API_NAME = '"
							# 	+ str(current_obj_api_name)
							# 	+ "' and OBJECT_NAME = '"
							# 	+ str(ObjectName)
							# 	+ "' and (DATA_TYPE = 'CURRENCY' or FORMULA_DATA_TYPE= 'CURRENCY')"
							# )
							if cur_api_name is not None:
								if current_prod == "Sales":
									if str(ObjectName) != "SAQTMT":
										curr_symbol_obj = Sql.GetFirst(
											"select SYMBOL,CURRENCY,isnull(DISPLAY_DECIMAL_PLACES,3) AS DISPLAY_DECIMAL_PLACES  from PRCURR WITH (NOLOCK) where CURRENCY_RECORD_ID = (select top 1 "
											+ cur_api_name.CURRENCY_INDEX
											+ " from "
											+ str(ObjectName)
											+ " where "
											+ str(autoNumber)
											+ " = '"
											+ str(RECORD_ID)
											+ "'  AND QUOTE_RECORD_ID = '"
											+ str(quote_record_id)
											+ "' AND QTEREV_RECORD_ID = '"
											+ str(quote_revision_record_id)
											+ "'  ) "
											)
									elif str(ObjectName) == "SAQTMT":
										curr_symbol_obj = Sql.GetFirst(
											"select SYMBOL,CURRENCY,isnull(DISPLAY_DECIMAL_PLACES,3) AS DISPLAY_DECIMAL_PLACES  from PRCURR WITH (NOLOCK) where CURRENCY_RECORD_ID = (select top 1 "
											+ cur_api_name.CURRENCY_INDEX
											+ " from "
											+ str(ObjectName)
											+ " where "
											+ str(autoNumber)
											+ " = '"
											+ str(RECORD_ID)
											+ "'  AND MASTER_TABLE_QUOTE_RECORD_ID = '"
											+ str(quote_record_id)
											+ "' AND QTEREV_RECORD_ID = '"
											+ str(quote_revision_record_id)
											+ "'  ) "
											)
								else:
									curr_symbol_obj = Sql.GetFirst(
										"select SYMBOL,CURRENCY,isnull(DISPLAY_DECIMAL_PLACES,3) AS DISPLAY_DECIMAL_PLACES  from PRCURR WITH (NOLOCK) where CURRENCY_RECORD_ID = (select top 1 "
										+ cur_api_name.CURRENCY_INDEX
										+ " from "
										+ str(ObjectName)
										+ " where "
										+ str(autoNumber)
										+ " = '"
										+ str(RECORD_ID)
										+ "' ) "
										)

								# Trace.Write(
								# 	"select SYMBOL,isnull(DISPLAY_DECIMAL_PLACES,3) DISPLAY_DECIMAL_PLACES  from PRCURR WITH (NOLOCK) where CURRENCY_RECORD_ID = (select "
								# 	+ cur_api_name.CURRENCY_INDEX
								# 	+ " from "
								# 	+ str(ObjectName)
								# 	+ " where "
								# 	+ str(autoNumber)
								# 	+ " = '"
								# 	+ str(RECORD_ID)
								# 	+ "' ) "
								# )
								if curr_symbol_obj is not None:
									if curr_symbol_obj != "":
										curr_symbol = curr_symbol_obj.CURRENCY
										decimal_val = curr_symbol_obj.DISPLAY_DECIMAL_PLACES  # modified for A043S001P01-9963							
								if current_obj_value != "" and decimal_val != "":
									formatting_string = "{0:." + str(decimal_val) + "f}"
									current_obj_value = formatting_string.format(float(current_obj_value))
						else:							
							cur_api_name = Sql.GetFirst(
							"select CURRENCY_INDEX from  SYOBJD WITH (NOLOCK) where API_NAME = '"
							+ str(current_obj_api_name)
							+ "' and OBJECT_NAME = '"
							+ str(ObjectName)
							+ "' and (DATA_TYPE = 'CURRENCY' or FORMULA_DATA_TYPE= 'CURRENCY')"
							)
							# Trace.Write(
							# 	"select CURRENCY_INDEX from  SYOBJD WITH (NOLOCK) where API_NAME = '"
							# 	+ str(current_obj_api_name)
							# 	+ "' and OBJECT_NAME = '"
							# 	+ str(ObjectName)
							# 	+ "' and (DATA_TYPE = 'CURRENCY' or FORMULA_DATA_TYPE= 'CURRENCY')"
							# )
							if cur_api_name is not None:
								curr_symbol_obj = Sql.GetFirst(
									"select SYMBOL,CURRENCY,isnull(DISPLAY_DECIMAL_PLACES,3) DISPLAY_DECIMAL_PLACES  from PRCURR WITH (NOLOCK) where CURRENCY = (select "
									+ cur_api_name.CURRENCY_INDEX
									+ " from "
									+ str(ObjectName)
									+ " where "
									+ str(autoNumber)
									+ " = '"
									+ str(RECORD_ID)
									+ "' ) "
								)
								# Trace.Write(
								# 	"select SYMBOL,isnull(DISPLAY_DECIMAL_PLACES,3) DISPLAY_DECIMAL_PLACES  from PRCURR WITH (NOLOCK) where CURRENCY = (select "
								# 	+ cur_api_name.CURRENCY_INDEX
								# 	+ " from "
								# 	+ str(ObjectName)
								# 	+ " where "
								# 	+ str(autoNumber)
								# 	+ " = '"
								# 	+ str(RECORD_ID)
								# 	+ "' ) "
								# )
								if curr_symbol_obj :
									if curr_symbol_obj != "":
										curr_symbol = curr_symbol_obj.CURRENCY
										decimal_val = curr_symbol_obj.DISPLAY_DECIMAL_PLACES  # modified for A043S001P01-9963
										
								else:
									curr_symbol_obj = Sql.GetFirst(
										"select SYMBOL,CURRENCY,isnull(DISPLAY_DECIMAL_PLACES,3) DISPLAY_DECIMAL_PLACES  from PRCURR WITH (NOLOCK) where CURRENCY_RECORD_ID = (select "
										+ cur_api_name.CURRENCY_INDEX
										+ " from "
										+ str(ObjectName)
										+ " where "
										+ str(autoNumber)
										+ " = '"
										+ str(RECORD_ID)
										+ "' ) "
									)
									if curr_symbol_obj != "":
										curr_symbol = curr_symbol_obj.CURRENCY
										decimal_val = curr_symbol_obj.DISPLAY_DECIMAL_PLACES  # modified for A043S001P01-9963							
								if current_obj_value != "" and decimal_val != "":
									formatting_string = "{0:." + str(decimal_val) + "f}"
									current_obj_value = formatting_string.format(float(current_obj_value))
					except:
						Trace.Write("currency symbol details error")
					if current_obj_value is not None:
						if current_obj_value != "":
							current_obj_value = current_obj_value + " " + curr_symbol		
					sec_str += (
						'<td><input id="'
						+ str(current_obj_api_name)
						+ '" type="text" value="'
						+ current_obj_value
						+ '" title="'
						+ current_obj_value
						+ '" class="form-control related_popup_css" style="'
						+ str(left_float)
						+ ' " '
						+ disable
						+ "></td>"
					)
				elif (
					str(current_obj_api_name) == "MESSAGE_HEADERVALUE" or str(current_obj_api_name) == "MESSAGE_BODYVALUE"
				) and MODE == "VIEW":
					GetPrimeKey = Product.Attributes.GetByName("QSTN_SYSEFL_AC_00075").GetValue()
					sec_str += "<td>"
					sec_str += (
						'<div class="row"><div id="div_PICKLISTLOAD_'
						+ str(current_obj_api_name)
						+ '" class="multiselect"><select id="First'
						+ str(current_obj_api_name)
						+ '" multiple="multiple"'
						+ str(onchange)
						+ ' value="'
						+ current_obj_value
						+ '" class="form-control pop_up_brd_rad related_popup_css fltlt options_'
						+ str(current_obj_api_name)
						+ ' "  '
						+ disable
						+ " >"
					)
					currectvaluelist = current_obj_value.split(",")
					splitedlist = str(currectvaluelist).replace("[", "").replace("]", "")
					if len(currectvaluelist) == 1 and currectvaluelist[0] == "":
						splitedlist = "'1'"
					if str(current_obj_api_name) == "MESSAGE_HEADERVALUE":
						Tier_List = Sql.GetList(
							"""SELECT SYOBJD.FIELD_LABEL  FROM ACAPCH (NOLOCK) INNER JOIN SYOBJH (NOLOCK)
							ON ACAPCH.APROBJ_RECORD_ID = SYOBJH.RECORD_ID INNER JOIN SYOBJD (NOLOCK)
							ON SYOBJD.OBJECT_NAME = SYOBJH.OBJECT_NAME WHERE
							APPROVAL_CHAIN_RECORD_ID = '{chainrecordId}'
							AND SYOBJD.FIELD_LABEL NOT in ({exceptlist})""".format(
								chainrecordId=str(GetPrimeKey), exceptlist=splitedlist
							)
						)
					else:
						Tier_List = Sql.GetList(
							"""SELECT SYOBJD.FIELD_LABEL FROM ACACST (NOLOCK) INNER JOIN SYOBJH (NOLOCK)
							ON ACACST.TSTOBJ_RECORD_ID = SYOBJH.RECORD_ID
							INNER JOIN SYOBJD (NOLOCK) ON SYOBJD.OBJECT_NAME = SYOBJH.OBJECT_NAME
							WHERE ACACST.APRCHN_RECORD_ID = '{chainrecordId}'
							AND ACACST.APRCHNSTP_NAME = '{TreeParam}'
							AND SYOBJD.FIELD_LABEL NOT in ({exceptlist})  """.format(
								chainrecordId=str(GetPrimeKey), TreeParam=TreeParam.split(': ')[1], exceptlist=splitedlist
							)
						)
					for req1 in Tier_List:
						if current_obj_value == req1:
							sec_str += "<option>" + str(req1.FIELD_LABEL) + "</option>"
						else:
							sec_str += "<option>" + str(req1.FIELD_LABEL) + "</option>"
					sec_str += (
						'</select><div id="button_mvmt1"> <button onclick="unselectedval(this)" '
						+ 'class="leftbutton" id ="'
						+ str(current_obj_api_name)
						+ '"> <i class="glyphicon glyphicon-triangle-left"></i> </button> '
						+ '<button onclick="selectedval(this)" id ="'
						+ str(current_obj_api_name)
						+ '" class="rightbutton"> <i class="glyphicon glyphicon-triangle-right"></i> </button> '
						+ '</div><select multiple="multiple" id="options1_'
						+ str(current_obj_api_name)
						+ '" >'
					)
					for listval in currectvaluelist:
						sec_str += "<option>" + str(listval) + "</option>"
					sec_str += (
						'</select><div id="button_mvmt"> <button class="topbutton" onclick="topselect(this)" id ="'
						+ str(current_obj_api_name)
						+ '"> <i class="glyphicon glyphicon-triangle-top"></i> </button> <button class="btmbutton"'
						+ ' onclick="btmselect(this)"id ="'
						+ str(current_obj_api_name)
						+ '" > <i class="glyphicon glyphicon-triangle-bottom"></i> </button> </div></div></div></td>'
					)
				elif str(current_obj_api_name) in ("CPQTABLEENTRYDATEADDED","CpqTableEntryDateModified"):
					try:
						current_obj_value = datetime.strptime(str(current_obj_value), '%m/%d/%Y %I:%M:%S %p').strftime('%m/%d/%Y %I:%M:%S %p')
					except:
						pass
					sec_str += (
						'<td><input id="'
						+ str(current_obj_api_name)
						+ '" type="text" value="'
						+ current_obj_value
						+ '" title="'
						+ current_obj_value
						+ '" class="form-control related_popup_css" style="'
						+ str(left_float)
						+ ' " '
						+ disable
						+ " maxlength = '"+str(max_length)+"'>"
						+ str(edit_warn_icon)
						+ "</td>"
					)
				else:	
					Trace.Write('2032---'+ str(current_obj_api_name) +str(MODE))
					if str(MODE) == "EDIT":				
						sec_str += (
							'<td><input id="'
							+ str(current_obj_api_name)
							+ '" type="text" value="'
							+ current_obj_value.lstrip()
							+ '" title="'
							+ current_obj_value
							+ '" class="form-control related_popup_css light_yellow" style="'
							+ str(left_float)
							+ ' " '
							+ disable
							+ " maxlength = '"+str(max_length)+"'>"
							+ str(edit_warn_icon)
							+ "</td>"
						)
					else:
						# if current_obj_api_name == "APPDTE_EXCH_RATE" and str(current_obj_value).lstrip() != "":
						# 	sec_str += (
						# 		'<td><input id="'
						# 		+ str(current_obj_api_name)
						# 		+ '" type="text" value="'
						# 		+ current_obj_value.lstrip()
						# 		+ ' of month" title="'
						# 		+ current_obj_value
						# 		+ '" class="form-control related_popup_css" style="'
						# 		+ str(left_float)
						# 		+ ' " '
						# 		+ disable
						# 		+ " maxlength = '"+str(max_length)+"'>"
						# 		+ str(edit_warn_icon)
						# 		+ "</td>"
						# 	)
						# else:
						sec_str += (
							'<td><input id="'
							+ str(current_obj_api_name)
							+ '" type="text" value="'
							+ current_obj_value.lstrip()
							+ '" title="'
							+ current_obj_value
							+ '" class="form-control related_popup_css" style="'
							+ str(left_float)
							+ ' " '
							+ disable
							+ " maxlength = '"+str(max_length)+"'>"
							+ str(edit_warn_icon)
							+ "</td>"
						)
				sec_str += (
					'<td class="float_r_bor_bot"><div class="col-md-12 editiconright"><a href="#" onclick="editclick_row(this)" class="editclick">'
					+ str(edit_pencil_icon)
					+ "</a></div></td>"
				)
				sec_str += "</tr>"
		sec_str += "</table></div>"
		sec_str += "</div>"

	try:
		returnList = []
		returnList = eval(Product.GetGlobal("CommonTreeList"))
		# Trace.Write("returnList--1687---" + str(returnList))
		# Trace.Write("objectName" + str(ObjectName) + "RECORD_IDRECORD_ID" + str(RECORD_ID))

		if str(ObjectName) == "SYTABS" or str(ObjectName) == "SYSECT":
			if str(ObjectName) != "SYSEFL":
				if RECORD_ID.startswith(ObjectName):					
					if str(ObjectName) != "USERS" and str(ObjectName) != "SYSEFL":
						RECORD_ID = CPQID.KeyCPQId.GetKEYId(str(ObjectName), str(RECORD_ID))
		Trace.Write('Return list-->'+str(returnList))
		Trace.Write('RECORD_ID--->'+str(RECORD_ID))
		recur_func(returnList, RECORD_ID)
	except:
		Trace.Write("errrorr")
	ret_value = str(Product.GetGlobal("CommonTreeListNodeId"))
	'''Trace.Write(
		"sec_str-"
		+ str(sec_str)
		+ " date_field--"
		+ str(date_field)
		+ " new_value_dict--"
		+ str(new_value_dict)
		+ " api_name--"
		+ str(api_name)
		+ " ret_value--"
		+ str(ret_value)
		+ " ObjectName--"
		+ str(ObjectName)
		+ " sec_bnr--"
		+ str(sec_bnr)
	)'''
	if MODE == "EDIT":
		if(str(ObjectName)=="SYPRAP"):		
			SEC_t = Sql.GetFirst("SELECT SYSECT.RECORD_ID FROM SYSECT WHERE  PRIMARY_OBJECT_NAME = '"+ str(ObjectName)+ "' AND  SECTION_NAME = 'APP PROPERTIES' ")
			api_name = SEC_t.RECORD_ID
		else:
			SEC_t = Sql.GetFirst("SELECT SYSECT.RECORD_ID FROM SYSECT WHERE  PRIMARY_OBJECT_NAME = '"+ str(ObjectName)+ "' AND  SECTION_NAME = 'BASIC INFORMATION' ")
			api_name = SEC_t.RECORD_ID
	
	if not RECORD_ID and ObjectName == 'SAQRIB':
		#sec_str = "<div class='noRecDisp'>Billing Matrix is not applicable for this quote configuration.</div>"
		Trace.Write('receiving---1993-------')
		quoteid = Quote.GetGlobal("contract_quote_record_id")
		SAQTSVObj=Sql.GetFirst("Select ENTITLEMENT_XML from SAQTSE (nolock) where QUOTE_RECORD_ID= '"+str(quoteid)+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"'  and SERVICE_ID like '%Z00%'")
		if SAQTSVObj:
			sec_str = "<div class='noRecDisp'>No Record Found.</div>"
		#else:
			#sec_str = "<div class='noRecDisp'>Billing Matrix is not applicable for this quote configuration.</div>"
	# if RECORD_ID and ObjectName == 'SAQRIB':
	# 	date_diff_obj = Sql.GetFirst("""SELECT IS_CHANGED
	# 					FROM SAQRIB (NOLOCK) 
	# 					WHERE QUOTE_BILLING_PLAN_RECORD_ID = '{}'""".format(RECORD_ID))
		# if date_diff_obj:
		# 	if date_diff_obj.IS_CHANGED:
		# 		notification = ' <div class="col-md-12" id="alert_msg" style="display: block;"><div class="row modulesecbnr brdr" data-toggle="collapse" data-target="#Alertmsg8" aria-expanded="true" >NOTIFICATIONS<i class="pull-right fa fa-chevron-down "></i><i class="pull-right fa fa-chevron-up"></i></div><div  id="Alertmsg8" class="col-md-12  alert-notification  brdr collapse in" ><div  class="col-md-12 alert-warning"  ><label ><img src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/warning1.svg" alt="Warning">  Changes have been made to the Quote Configuration. Please refresh the Billing Matrix.</label></div></div></div>'
		# 		sec_str = notification+sec_str
	
	# To Hide Add On Products Subtab
	try:
		quote_record_id = Quote.GetGlobal("contract_quote_record_id")
	except:
		pass #to handle error while we are in system admin
	if Product.GetGlobal("TreeParentLevel0") == "Comprehensive Services" and TreeSuperParentParam == "Product Offerings":		
		quoteid = Quote.GetGlobal("contract_quote_record_id")
		addon_details = Sql.GetList("SELECT SERVICE_ID FROM SAQSAO (NOLOCK) WHERE SERVICE_ID = '"+str(TreeParam)+"'")
		equipment_details = Sql.GetFirst("SELECT * FROM SAQSCO (NOLOCK) WHERE SERVICE_ID = '"+str(TreeParam)+"' AND QUOTE_RECORD_ID ='"+str(quoteid)+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"'  ")
		if addon_details and equipment_details:
			Ad_on_prd = "True"
		else:
			Ad_on_prd = "False"
	else:
		Ad_on_prd = ""
	if	Product.GetGlobal("TreeParentLevel0") == "Complementary Products" and TreeSuperParentParam == "Product Offerings":
		quoteid = Quote.GetGlobal("contract_quote_record_id")
		entitlement_obj=Sql.GetFirst("SELECT ENTITLEMENT_XML FROM SAQTSE (NOLOCK) WHERE SERVICE_ID='Z0092' AND QUOTE_RECORD_ID ='{}' AND QTEREV_RECORD_ID = '{}'".format(quoteid,quote_revision_record_id))
		spare_parts_visibility = 'False'
		if entitlement_obj:
			entitlement_xml = entitlement_obj.ENTITLEMENT_XML
			pattern_tag = re.compile(r'(<QUOTE_ITEM_ENTITLEMENT>[\w\W]*?</QUOTE_ITEM_ENTITLEMENT>)')
			pattern_id = re.compile(r'<ENTITLEMENT_NAME>CONSUMABLE_92</ENTITLEMENT_NAME>')
			pattern_name = re.compile(r'<ENTITLEMENT_DISPLAY_VALUE>(?:INCLUDED|SOME INCLUSIONS)</ENTITLEMENT_DISPLAY_VALUE>')
			for m in re.finditer(pattern_tag, entitlement_xml):
				sub_string = m.group(1)
				get_ent_id =re.findall(pattern_id,sub_string)
				get_ent_name=re.findall(pattern_name,sub_string)
				if get_ent_id and get_ent_name:
					spare_parts_visibility = 'True'
					break
	else:
		spare_parts_visibility = ""				
	
	return sec_str, date_field, new_value_dict, api_name, ret_value, ObjectName, sec_bnr,getyears, Ad_on_prd,spare_parts_visibility,cancel_save


def recur_func(test, key):
	for d_data in test:
		if "nodes" in d_data.keys():
			if str(d_data.get("id")) == str(key):
				Product.SetGlobal("CommonTreeListNodeId", str(d_data.get("nodeId")))
				break
			else:				
				recur_func(d_data.get("nodes"), key)
		else:
			if d_data.get("id"):
				if str(d_data.get("id")) == str(key):
					Product.SetGlobal("CommonTreeListNodeId", str(d_data.get("nodeId")))
					break
	return "true"


def UpdateBreadcrumb(REC_ID):	
	qry = ""
	bc_id = ""
	# QRE = ""
	if TreeParam == "Sales": 
		ObjectName = REC_ID.split('-')[0]		
		RECORD_ID = CPQID.KeyCPQId.GetKEYId(str(ObjectName), str(REC_ID))
		qry = Sql.GetFirst(
			"""SELECT QUOTE_ID FROM SAQTMT (NOLOCK) WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{recid}' AND QTEREV_RECORD_ID='{revision_rec_id}' """.format(recid=RECORD_ID,revision_rec_id = quote_revision_record_id)	)
		if qry:
			bc_id = str(qry.QUOTE_ID)
		else:
			bc_id = "Quotes"
	# elif TreeParam == "Sales Orgs":
	# 	ObjectName = REC_ID.split('-')[0]
	# 	RECORD_ID = CPQID.KeyCPQId.GetKEYId(str(ObjectName), str(REC_ID))
	# 	qry = Sql.GetFirst(
	# 		"SELECT SASORG.SALESORG_ID, SAQTSO.QUOTE_ID FROM SASORG (NOLOCK) INNER JOIN SAQTSO ON SAQTSO.SALESORG_ID = SASORG.SALESORG_ID WHERE SALES_ORG_RECORD_ID = '{recid}'".format(recid=RECORD_ID)
	# 	)
	# 	if qry:
	# 			bc_id = str(qry.SALESORG_ID) + '-' + str(qry.QUOTE_ID)									
	# 	else:
	# 		bc_id = "Sales Orgs"
	elif TreeParentParam == "Sales Orgs":
		ObjectName = REC_ID.split('-')[0]
		RECORD_ID = CPQID.KeyCPQId.GetKEYId(str(ObjectName), str(REC_ID))
		qry = Sql.GetFirst("SELECT QUOTE_ID FROM SAQTSO (NOLOCK) WHERE QUOTE_SALESORG_RECORD_ID ='{recid}'".format(recid=RECORD_ID))
		# ObjectName = "SAQTSO"
		#RECORD_ID = CPQID.KeyCPQId.GetKEYId(str(ObjectName), str(REC_ID))
		# qry = Sql.GetFirst("SELECT QUOTE_ID FROM SAQTSO WHERE SALESORG_ID = '{}' AND DOC_CURRENCY = '{}'".format(str(QRE.SALESORG_ID), str(QRE.SORG_CURRENCY)))
		if qry:
				bc_id = str(qry.QUOTE_ID)
	elif TreeParam == "Exchange Rates":
		ObjectName = REC_ID.split('-')[0]
		RECORD_ID = CPQID.KeyCPQId.GetKEYId(str(ObjectName), str(REC_ID))
		qry = Sql.GetFirst(
			"SELECT FROM_CURRENCY, TO_CURRENCY FROM PREXRT (NOLOCK) WHERE EXCHANGE_RATE_RECORD_ID = '{recid}'".format(recid=RECORD_ID)
		)
		if qry:
				bc_id = str(qry.FROM_CURRENCY) + '-' + str(qry. TO_CURRENCY)
		else:
			bc_id = "Exchange Rates"
	Action_Str = ""
	Action_Str = '<li><a onclick="tree_breadCrumb_redirection(this)">'
	Action_Str += '<abbr title="'+str(bc_id)+'">'
	Action_Str += str(bc_id)
	Action_Str += '</abbr></a><span class="angle_symbol"><img src="/mt/appliedmaterials_tst/images/productimages/BREADCRUMB_ICON_TRANS.PNG"></span></li>'

	return Action_Str

# def EntitlementTreeViewHTMLDetail(
# 	MODE,
# 	TableId,
# 	RECORD_ID,
# 	TreeParam,
# 	NEWVAL,
# 	LOOKUPOBJ,
# 	LOOKUPAPI,
# 	SECTION_EDIT,
# 	Flag,
# 	TreeParentParam,
# 	ObjectName,
# 	SectionList,
# 	EntitlementType,
# ):
# 	quoteid = Quote.GetGlobal("contract_quote_record_id")
# 	TreeParentParam = AllTreeParam["TreeParentLevel0"]
# 	TreeSuperParentParam = AllTreeParam["TreeParentLevel1"]
# 	cpsConfigID = get_last_secid = ''
# 	msg_txt = insertservice  = costlabimp = pricelabimp = costlabimt0t1 = pricelabimptot1 =  costlabimt0t1t = pricelabimptot1t = costlabimt2lt = pricelabimpt2lt = costlabimt2l = pricelabimpt2l = costlabimt3l = pricelabimpt3l = costlabimt3lab = pricelabimpt3lab = ""
# 	sec_str_boot = sec_bnr = imgstr = dbl_clk_function = getprevdicts = sec_str_cf = sec_str1 = getTlab = getregionval = getquote_sales_val = ""
# 	tablistnew =  []
# 	TableObj = ""
# 	attributes_count = 0
# 	ChangedList = totaldisallowlist = section_not_list = []
# 	Trace.Write("EntitlementType"+str(EntitlementType))
	
# 	try:
# 		TreeSuperTopParentParam = AllTreeParam["TreeParentLevel3"]
# 	except:
# 		TreeSuperTopParentParam = ""
# 	Trace.Write('TreeSuperParentParam'+'--'+str(TreeSuperTopParentParam)+'--'+str(TreeTopSuperParentParam))
# 	objname_ent = "" ##add on product entitilement obj declare
# 	if TreeSuperParentParam == "Product Offerings":		
# 		ProductPartnumber = AllTreeParam["TreeParam"]
# 	elif TreeTopSuperParentParam == "Product Offerings":
# 		### add on product entitilement starts
# 		if str(TreeParentParam).upper() == "ADD-ON PRODUCTS":
# 			ProductPartnumber = TreeParam
# 			objname_ent = 'SAQSAO'	
# 			### add on product entitilement starts
# 		else:	
# 			ProductPartnumber = TreeParentParam
# 			###receiving equp entitilement starts
# 			if TreeSuperParentParam == 'Complementary Products' and TreeParam == 'Receiving Equipment':
# 				objname_ent = 'SAQSCO'
# 			###receiving equp entitilement ends
# 	elif TreeSuperTopParentParam == "Product Offerings":
# 		### add on product entitilement starts
# 		if str(TreeParentParam).upper() == "ADD-ON PRODUCTS":
# 			ProductPartnumber = TreeParam
# 			objname_ent = 'SAQSAO'	
# 			### add on product entitilement starts
# 		else:	
# 			ProductPartnumber = TreeSuperParentParam
# 			if (TreeParentParam == 'Receiving Equipment' and TreeTopSuperParentParam == 'Complementary Products'):
# 				TreeParentParam = ProductPartnumber

# 	elif TreeParentParam == "Quote Items":
# 		if "-" in TreeParam:
# 			TreeParam = TreeParam.split("-")[1].strip()
# 		GetItem = Sql.GetFirst("select * from SAQICO (NOLOCK) where QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '" + str(RECORD_ID) + "'")
# 		if GetItem is not None:
# 			ProductPartnumber = GetItem.SERVICE_ID
# 		else:
# 			ProductPartnumber = TreeParam
# 	elif TreeSuperParentParam == "Quote Items":
# 		TreeParentParam = TreeParentParam.split("-")[1].strip()
# 		ProductPartnumber = TreeParentParam
# 	elif TreeTopSuperParentParam == "Quote Items":
# 		##for Quote items for ADDON Product starts
# 		if " - ADDON" in str(TreeSuperParentParam):
# 			tree_temp = TreeSuperParentParam.split(" - ")
# 			try:
# 				if str(TreeSuperParentParam.split("-")[3]):
# 					TreeSuperParentParam = TreeSuperParentParam.split("-")[2].strip()	
# 				else:
# 					TreeSuperParentParam = TreeSuperParentParam.split("-")[1].strip()
# 			except:
# 				TreeSuperParentParam = TreeSuperParentParam.split("-")[1].strip()	
# 			##for Quote items for ADDON Product ends	
# 		else:
# 			TreeSuperParentParam = TreeSuperParentParam.split("-")[1].strip()
# 		ProductPartnumber = TreeSuperParentParam
# 	##addon product fab and greenbook level 
# 	elif (str(TreeSuperTopParentParam).upper() == "COMPREHENSIVE SERVICES" and str(TreeSuperParentParam).upper() == "ADD-ON PRODUCTS"):		
# 		ProductPartnumber = TreeParentParam	
# 	elif str(TreeTopSuperTopParentParam).upper() == "COMPREHENSIVE SERVICES" and str(TreeTopSuperParentParam).upper() == "ADD-ON PRODUCTS":		
# 		ProductPartnumber = TreeSuperParentParam		
# 	##addon product fab and greenbook level 
# 	elif (TreeSuperParentParam in ('Receiving Equipment', 'Sending Equipment') and TreeSuperTopParentParam == 'Complementary Products'):
# 		TreeSuperParentParam = ProductPartnumber = TreeTopSuperParentParam
# 		Trace.Write('comes1'+str(ProductPartnumber))
# 	#A055S000P01-9226 start
# 	getslaes_value  = Sql.GetFirst("SELECT SALESORG_ID FROM SAQTRV WHERE QUOTE_RECORD_ID = '"+str(quoteid)+"'")
# 	if getslaes_value:
# 		getquote_sales_val = getslaes_value.SALESORG_ID
# 	Trace.Write('getquote_sales_val---2421----'+str(getquote_sales_val))
# 	get_il_sales = SqlHelper.GetList("select SALESORG_ID from SASORG where country = 'IL'")
# 	get_il_sales_list = [val.SALESORG_ID for val in get_il_sales]
# 	Trace.Write('get_il_sales_list---2421----'+str(get_il_sales_list))
# 	#A055S000P01-9226 end
# 	if EntitlementType == "EQUIPMENT":
# 		### add on product entitilement starts		
# 		if str(TreeParentParam).upper() == "ADD-ON PRODUCTS" and objname_ent == 'SAQSAO':
# 			TableObj = Sql.GetFirst("select * from SAQTSE (NOLOCK) where QTESRV_RECORD_ID = '" + str(RECORD_ID) + "'")
# 			ParentObj = Sql.GetFirst("select * from SAQSAO (NOLOCK) where QUOTE_SERVICE_ADD_ON_PRODUCT_RECORD_ID = '" + str(RECORD_ID) + "'")
# 			if ParentObj:
# 				QUOTE_ID = ParentObj.QUOTE_ID
# 				QUOTE_NAME = ParentObj.QUOTE_NAME
# 				QUOTE_RECORD_ID = ParentObj.QUOTE_RECORD_ID
# 				QUOTE_SERVICE_RECORD_ID = ParentObj.QUOTE_SERVICE_ADD_ON_PRODUCT_RECORD_ID
# 				SERVICE_RECORD_ID = ParentObj.SERVICE_RECORD_ID
# 				SERVICE_ID = ParentObj.SERVICE_ID
# 				SERVICE_DESCRIPTION = ParentObj.SERVICE_DESCRIPTION
# 				SALESORG_RECORD_ID = ParentObj.SALESORG_RECORD_ID
# 				SALESORG_ID = ParentObj.SALESORG_ID
# 				SALESORG_NAME = ParentObj.SALESORG_NAME
# 				QTEREV_RECORD_ID = ParentObj.QTEREV_RECORD_ID

# 			where = "QUOTE_RECORD_ID = '" + str(QUOTE_RECORD_ID) + "' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' AND QTESRV_RECORD_ID = '" + str(RECORD_ID) + "'"
# 			join = ''
# 			##add on product entitilement ends
# 		###receiving equp entitilement starts
# 		elif str(TreeParam).upper() == "RECEIVING EQUIPMENT" and objname_ent == 'SAQSCO':
# 			Trace.Write('receiving----'+str(quoteid)+'---'+str(ProductPartnumber))
# 			TableObj = Sql.GetFirst("select * from SAQTSE (NOLOCK) where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' and SERVICE_ID = '{}' ".format(quoteid,quote_revision_record_id,ProductPartnumber))
# 			ParentObj = Sql.GetFirst("select * from SAQTSV (NOLOCK) where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' and SERVICE_ID = '{}' ".format(quoteid,quote_revision_record_id,ProductPartnumber))
# 			if ParentObj:
# 				QUOTE_ID = ParentObj.QUOTE_ID
# 				QUOTE_NAME = ParentObj.QUOTE_NAME
# 				QUOTE_RECORD_ID = ParentObj.QUOTE_RECORD_ID
# 				RECORD_ID = QUOTE_SERVICE_RECORD_ID = ParentObj.QUOTE_SERVICE_RECORD_ID
# 				SERVICE_RECORD_ID = ParentObj.SERVICE_RECORD_ID
# 				SERVICE_ID = ParentObj.SERVICE_ID
# 				SERVICE_DESCRIPTION = ParentObj.SERVICE_DESCRIPTION
# 				SALESORG_RECORD_ID = ParentObj.SALESORG_RECORD_ID
# 				SALESORG_ID = ParentObj.SALESORG_ID
# 				SALESORG_NAME = ParentObj.SALESORG_NAME
# 				QTEREV_RECORD_ID = ParentObj.QTEREV_RECORD_ID

# 			where = "QUOTE_RECORD_ID = '" + str(QUOTE_RECORD_ID) + "' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' AND QTESRV_RECORD_ID = '" + str(RECORD_ID) + "'"
# 			join = ''	
# 		###receiving equp entitilement ends
# 		else:
# 			TableObj = Sql.GetFirst("select * from SAQTSE (NOLOCK) where QTESRV_RECORD_ID = '" + str(RECORD_ID) + "'")
# 			ParentObj = Sql.GetFirst("select * from SAQTSV (NOLOCK) where QUOTE_SERVICE_RECORD_ID = '" + str(RECORD_ID) + "'")
# 			if ParentObj:
# 				QUOTE_ID = ParentObj.QUOTE_ID
# 				QUOTE_NAME = ParentObj.QUOTE_NAME
# 				QUOTE_RECORD_ID = ParentObj.QUOTE_RECORD_ID
# 				QUOTE_SERVICE_RECORD_ID = ParentObj.QUOTE_SERVICE_RECORD_ID
# 				SERVICE_RECORD_ID = ParentObj.SERVICE_RECORD_ID
# 				SERVICE_ID = ParentObj.SERVICE_ID
# 				SERVICE_DESCRIPTION = ParentObj.SERVICE_DESCRIPTION
# 				SALESORG_RECORD_ID = ParentObj.SALESORG_RECORD_ID
# 				SALESORG_ID = ParentObj.SALESORG_ID
# 				SALESORG_NAME = ParentObj.SALESORG_NAME
# 				QTEREV_RECORD_ID = ParentObj.QTEREV_RECORD_ID

# 			where = "QUOTE_RECORD_ID = '" + str(QUOTE_RECORD_ID) + "' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' AND QTESRV_RECORD_ID = '" + str(RECORD_ID) + "'"
# 			join = ''		
# 	elif EntitlementType == "TOOLS":
# 		TableObj = Sql.GetFirst("select * from SAQSCE (NOLOCK) where QTESRVCOB_RECORD_ID = '" + str(RECORD_ID) + "'")
# 		ObjectName = "SAQSCE"
# 		where = "QUOTE_RECORD_ID = '" + str(quoteid) + "' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' AND QTESRVCOB_RECORD_ID = '" + str(RECORD_ID) + "'"
# 		join = ''		

# 	elif EntitlementType == "ITEMGREENBOOK":
# 		ObjectName = "SAQSGE"
# 		service = TreeSuperParentParam
# 		TableObj = Sql.GetFirst("select * from SAQSGE (NOLOCK) where QUOTE_RECORD_ID = '" + str(quoteid) + "' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' AND SERVICE_ID = '"+str(service)+"' AND GREENBOOK = '" + str(TreeParam) + "' AND FABLOCATION_ID = '"+ str(TreeParentParam) + "'")		
# 		where = "QUOTE_RECORD_ID = '" + str(quoteid) + "' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' AND SERVICE_ID = '"+str(service)+"' AND GREENBOOK = '" + str(TreeParam) + "' AND FABLOCATION_ID = '"+ str(TreeParentParam) + "'"
# 		join = ''		
# 	elif EntitlementType == "ITEMSPARE":
# 		#TableObj = Sql.GetFirst("select SAQIEN.* from SAQIEN (NOLOCK) JOIN QTQITM ON QTQITM.QUOTE_RECORD_ID = SAQIEN.QUOTE_RECORD_ID where QTQITM.QUOTE_ITEM_RECORD_ID = '" + str(RECORD_ID) + "'")
# 		#TableObj = Sql.GetFirst("select SAQIPE.* from SAQIPE (NOLOCK) JOIN QTQITM ON QTQITM.QUOTE_RECORD_ID = SAQIPE.QUOTE_RECORD_ID AND QTQITM.SERVICE_ID =SAQIPE.SERVICE_ID where SAQIPE.QUOTE_RECORD_ID = '" + str(quoteid) + "'")	
# 		TableObj = Sql.GetFirst("select SAQIPE.* from SAQIPE (NOLOCK) JOIN SAQIFP ON SAQIFP.QUOTE_RECORD_ID = SAQIPE.QUOTE_RECORD_ID AND SAQIFP.QTEREV_RECORD_ID  = SAQIPE.QTEREV_RECORD_ID  where SAQIFP.QUOTE_ITEM_FORECAST_PART_RECORD_ID  = '" + str(RECORD_ID) + "'")		
# 		#where = "QTQITM.QUOTE_ITEM_RECORD_ID = '" + str(RECORD_ID) + "'"
# 		#join = 'JOIN QTQITM ON QTQITM.QUOTE_RECORD_ID = SAQIEN.QUOTE_RECORD_ID'
# 		where = "QUOTE_RECORD_ID = '" + str(quoteid) + "' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' AND SERVICE_ID = '" + str(TreeParam) + "'"
# 		join = 'JOIN SAQIFP ON SAQITM.QUOTE_RECORD_ID = SAQIPE.QUOTE_RECORD_ID AND SAQITM.QTEREV_RECORD_ID  = SAQIPE.QTEREV_RECORD_ID  AND SAQIFP.SERVICE_ID =SAQIPE.SERVICE_ID'
# 	elif EntitlementType == "ITEMS":	
# 		TableObj = Sql.GetFirst("select * from SAQIEN (NOLOCK) where QTEITMCOB_RECORD_ID = '" + str(RECORD_ID) + "'")
# 		where = "QTEITMCOB_RECORD_ID = '" + str(RECORD_ID) + "'"
# 		join = ''
# 	elif EntitlementType == "FABLOCATION":			
# 		TableObj = Sql.GetFirst("select * from SAQSFE (NOLOCK) where  QUOTE_RECORD_ID = '" + str(quoteid) + "' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' AND SERVICE_ID = '" + str(TreeParentParam) + "' AND FABLOCATION_ID = '" + str(TreeParam) + "'")
# 		where = "QUOTE_RECORD_ID = '" + str(quoteid) + "' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' AND SERVICE_ID = '" + str(TreeParentParam) + "' AND FABLOCATION_ID ='"+str(TreeParam)+"'"
# 		join = ''		
# 	elif EntitlementType == "BUSINESSUNIT":
# 		TableObj = Sql.GetFirst("select * from SAQSGE (NOLOCK) where QUOTE_RECORD_ID = '" + str(quoteid) + "' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' AND SERVICE_ID = '" + str(TreeSuperParentParam) + "' AND FABLOCATION_ID = '" + str(TreeParentParam) + "' AND GREENBOOK = '"+str(TreeParam)+"'")
# 		if TableObj is not None:
# 			RECORD_ID = str(TableObj.SERVICE_RECORD_ID)
# 		where = "QUOTE_RECORD_ID = '" + str(quoteid) + "' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' AND SERVICE_ID = '" + str(TreeSuperParentParam) + "' AND GREENBOOK ='"+str(TreeParam)+"' AND FABLOCATION_ID = '"+str(TreeParentParam)+"'"
# 		join = ''
# 	elif EntitlementType == "ASSEMBLY":
# 		TableObj = Sql.GetFirst("select * from SAQSAE (NOLOCK) where QUOTE_RECORD_ID = '" + str(quoteid) + "' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' AND SERVICE_ID = '" + str(TreeSuperParentParam) + "' AND FABLOCATION_ID = '" + str(TreeParentParam) + "' AND GREENBOOK = '"+str(TreeParam)+"' AND EQUIPMENT_ID = '"+str(EquipmentId)+"' AND ASSEMBLY_ID = '"+str(AssemblyId)+"' ")
# 		where = "QUOTE_RECORD_ID = '" + str(quoteid) + "' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' AND SERVICE_ID = '" + str(TreeSuperParentParam) + "' AND GREENBOOK ='"+str(TreeParam)+"' AND FABLOCATION_ID = '"+str(TreeParentParam)+"' AND EQUIPMENT_ID = '"+str(EquipmentId)+"' AND ASSEMBLY_ID = '"+str(AssemblyId)+"'"
# 		join = ''		
# 	if EntitlementType != "SENDING_LEVEL":
# 		if TableObj is None and (EntitlementType == "EQUIPMENT"):
# 			Request_URL = "https://cpservices-product-configuration.cfapps.us10.hana.ondemand.com/api/v2/configurations?autoCleanup=False"
# 			Fullresponse = EntitlementRequest(ProductPartnumber,Request_URL,"New")
# 		else:		
# 			if TableObj:
# 				cpsConfigID = TableObj.CPS_CONFIGURATION_ID
# 			Request_URL = "https://cpservices-product-configuration.cfapps.us10.hana.ondemand.com/api/v2/configurations/"+str(cpsConfigID)
# 			Fullresponse = EntitlementRequest(ProductPartnumber,Request_URL,"Existing")

# 		attributesdisallowedlst = []
# 		attributeReadonlylst = attributes_disallowed_list = []
# 		attributeEditlst = list_of_tabs = []
# 		attributevalues = {}
# 		attributedefaultvalue = []
# 		dropdowndisallowlist = []
# 		dropdownallowlist = []
# 		get_lastsection_val = attrcode = disable_edit = ""
# 		# where = ""
# 		Trace.Write("Fullresponse_J "+str(Fullresponse))
# 		Product.SetGlobal('Fullresponse_load',str(Fullresponse))
# 		#Product.SetGlobal('Fullresponse',str(Fullresponse_load))
# 		for rootattribute, rootvalue in Fullresponse.items():
# 			if rootattribute == "rootItem":
# 				for Productattribute, Productvalue in rootvalue.items():
# 					if Productattribute == "characteristics":
# 						for prdvalue in Productvalue:
# 							if prdvalue["visible"] == "false":
# 								attributesdisallowedlst.append(prdvalue["id"])
# 							if prdvalue["readOnly"] == "true":
# 								attributeReadonlylst.append(prdvalue["id"])
# 							if prdvalue["readOnly"] == "false":
# 								attributeEditlst.append(prdvalue["id"])
# 							if prdvalue["possibleValues"]:
# 								for i in prdvalue["possibleValues"]:
# 									if i['selectable'] == 'false' and 'valueLow' in i.keys():
# 										dropdowndisallowlist.append(str(prdvalue["id"])+'_'+str(i['valueLow'])	)
# 									# else:
# 									# 	dropdownallowlist.append(str(prdvalue["id"])+'_'+str(i['valueLow'])	)
# 							for attribute in prdvalue["values"]:
# 								attributevalues[str(prdvalue["id"])] = attribute["value"]
# 								if attribute["author"] in ('Default','System'):
# 									attributedefaultvalue.append(prdvalue["id"])
# 		#Trace.Write('attributesdisallowedlst--'+str(attributesdisallowedlst))
# 		Trace.Write('attributeReadonlylst--'+str(attributeReadonlylst))
# 		Trace.Write('attributevalues'+str(attributevalues))
# 		Trace.Write('attributedefaultvalue----'+str(attributedefaultvalue))


# 		product_obj = Sql.GetFirst("""SELECT 
# 									MAX(PDS.PRODUCT_ID) AS PRD_ID,PDS.SYSTEM_ID,PDS.PRODUCT_NAME 
# 								FROM PRODUCTS PDS 
# 								INNER JOIN PRODUCT_VERSIONS PRVS ON  PDS.PRODUCT_ID = PRVS.PRODUCT_ID 
# 								WHERE SYSTEM_ID ='{SystemId}' and PRVS.SAPKBVersion = '{kb_version}'
# 								GROUP BY PDS.SYSTEM_ID,PDS.UnitOfMeasure,PDS.CART_DESCRIPTION_BUILDER,PDS.PRODUCT_NAME""".format(SystemId = str(ProductPartnumber),kb_version = Fullresponse['kbKey']['version'] ))
		
# 		product_tabs_obj = Sql.GetList("""SELECT 
# 												TOP 1000 TAB_NAME, TAB_RANK, TAB_PROD_ID, TAB_PRODUCTS.TAB_CODE
# 											FROM TAB_PRODUCTS
# 											JOIN TAB_DEFN ON TAB_DEFN.TAB_CODE = TAB_PRODUCTS.TAB_CODE
# 											WHERE TAB_PRODUCTS.PRODUCT_ID = {ProductId} and TAB_NAME not like '$%'
# 											ORDER BY TAB_PRODUCTS.RANK""".format(ProductId = product_obj.PRD_ID))
		
# 		product_attributes_obj = Sql.GetList("""SELECT TOP 1000 PAT_SCHEMA.STANDARD_ATTRIBUTE_CODE, 
# 													TAB_PRODUCTS.TAB_PROD_ID, TAB_PRODUCTS.TAB_CODE, ATTRIBUTE_DEFN.STANDARD_ATTRIBUTE_NAME,PRODUCT_ATTRIBUTES.LABEL AS LABEL, ATTRIBUTE_DEFN.SYSTEM_ID AS SYSTEM_ID, ATT_DISPLAY_DEFN.ATT_DISPLAY_DESC AS ATT_DISPLAY_DESC
# 												FROM TAB_PRODUCTS
# 												LEFT JOIN PAT_SCHEMA ON PAT_SCHEMA.TAB_PROD_ID=TAB_PRODUCTS.TAB_PROD_ID											
# 												LEFT JOIN PRODUCT_ATTRIBUTES ON PRODUCT_ATTRIBUTES.STANDARD_ATTRIBUTE_CODE = PAT_SCHEMA.STANDARD_ATTRIBUTE_CODE AND PRODUCT_ATTRIBUTES.PRODUCT_ID = TAB_PRODUCTS.PRODUCT_ID
# 												LEFT JOIN ATTRIBUTE_DEFN ON ATTRIBUTE_DEFN.STANDARD_ATTRIBUTE_CODE = PRODUCT_ATTRIBUTES.STANDARD_ATTRIBUTE_CODE
# 												LEFT JOIN ATT_DISPLAY_DEFN ON ATT_DISPLAY_DEFN.ATT_DISPLAY = PRODUCT_ATTRIBUTES.ATT_DISPLAY
												
# 												WHERE TAB_PRODUCTS.PRODUCT_ID = {ProductId}
# 												ORDER BY TAB_PRODUCTS.RANK""".format(ProductId = product_obj.PRD_ID))
# 		tabwise_product_attributes = {}
# 		#overall_attribute_list = []	
# 		if product_attributes_obj:
# 			for product_attribute_obj in product_attributes_obj:
# 				overall_attribute ={}
# 				attr_detail = {'attribute_name':str(product_attribute_obj.STANDARD_ATTRIBUTE_NAME), 
# 							'attribute_label':str(product_attribute_obj.LABEL), 
# 							'attribute_system_id':str(product_attribute_obj.SYSTEM_ID),
# 							'attribute_dtype':str(product_attribute_obj.ATT_DISPLAY_DESC),
# 							'attribute_code':str(product_attribute_obj.STANDARD_ATTRIBUTE_CODE)
							
# 							}
# 				# overall_attribute[str(product_attribute_obj.STANDARD_ATTRIBUTE_CODE)] = str(product_attribute_obj.SYSTEM_ID)
# 				# overall_attribute_list.append(overall_attribute)
# 				if product_attribute_obj.TAB_PROD_ID in tabwise_product_attributes:
# 					tabwise_product_attributes[product_attribute_obj.TAB_PROD_ID].append(attr_detail)
# 				else:
# 					tabwise_product_attributes[product_attribute_obj.TAB_PROD_ID] = [attr_detail]
# 		Trace.Write("tabwise_product_attributes_J "+str(tabwise_product_attributes))
	
# 		#Trace.Write('overall_attribute_list'+str(overall_attribute_list))



# 		# ATTRvalue = Sql.GetList("SELECT Top 100000 ATDF.STANDARD_ATTRIBUTE_NAME,ATDF.SYSTEM_ID,ATDD.ATT_DISPLAY_DESC,PRDAT.LABEL,PRDAT.LINEITEM,PRDAT.STANDARD_ATTRIBUTE_CODE from ATTRIBUTE_DEFN ATDF INNER JOIN PRODUCT_ATTRIBUTES PRDAT ON ATDF.STANDARD_ATTRIBUTE_CODE = PRDAT.STANDARD_ATTRIBUTE_CODE INNER JOIN ATT_DISPLAY_DEFN ATDD on    PRDAT.ATT_DISPLAY = ATDD.ATT_DISPLAY where PRDAT.PRODUCT_ID = '{product_id}'".format(sap_part_no = str(ATTPRD.SYSTEM_ID),product_id = str(ATTPRD.PRD_ID)) )
		
# 		# for attr in ATTRvalue:
# 		# 	STDVALUES =  Sql.GetList("SELECT * from STANDARD_ATTRIBUTE_VALUES where STANDARD_ATTRIBUTE_CODE ='{attr_code}' and SYSTEM_ID like '%{sys_id}%' ".format(attr_code = str(attr.STANDARD_ATTRIBUTE_CODE),sys_id = str(attr.SYSTEM_ID) )  )


# 		# attr_dict = {}
# 		# ServiceContainer = Product.GetContainerByName("Services")
# 		sec_str = getvaludipto = getvaludipt1 = getvaludipt2 = getvaludipt2lt = getvaludipt2lab = getvaludipto_q = getvaludipt2_q = getvaludipt2lt_q = getvaludipt2lab_q = getvaludipt2lab = getvaludipt3lab = getvaludipt3lab_q = getvaludipt3labt = getvaludipt3labt_q= getvaludipt1_q=  getlabortype_calc = gett1labor_calc= gett1labortype_calc =gett2labo_calc = gett2labotype_calc = gett3lab_calc = gett3labtype_calc = ""
# 		multi_select_attr_list = {}
# 		getregion=Sql.GetFirst("SELECT REGION from SAQTRV WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' ".format(quoteid,quote_revision_record_id))
# 		if getregion:
# 			getregionval = getregion.REGION
			
# 		GetCPSVersion = Sql.GetFirst("SELECT KB_VERSION FROM SAQTSE (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND KB_VERSION IS NOT NULL AND KB_VERSION != ''".format(quoteid,quote_revision_record_id))

# 		if GetCPSVersion :
# 			if GetCPSVersion.KB_VERSION is not None and GetCPSVersion.KB_VERSION != Fullresponse["kbKey"]["version"]:
# 				sec_str += '<div id="Headerbnr" class="mart_col_back disp_blk"><div class="col-md-12" id="PageAlert_not"><div class="row modulesecbnr brdr" data-toggle="collapse" data-target="#Alert_notifcatio6" aria-expanded="true">NOTIFICATIONS<i class="pull-right fa fa-chevron-down"></i><i class="pull-right fa fa-chevron-up"></i></div><div id="Alert_notifcatio6" class="col-md-12 alert-notification brdr collapse in"><div class="col-md-12 alert-info"><label title=" Information : The Knowledge Base of the VC Characteristics has been updated in CPS."><img src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/infocircle1.svg" alt="Info"> Information : The Knowledge Base of the VC Characteristics has been updated in CPS.</label></div></div></div></div>'
# 			else:
# 				sec_str += ''
# 		else:
# 			Trace.Write("GETCPS VERSION EMPTY!")	
		
# 		#desc_list = ["APPROVAL","ENTITLEMENT DESCRIPTION","ENTITLEMENT VALUE","DATA TYPE","FACTOR CURRENCY","CALCULATION FACTOR","ENTITLEMENT COST IMPACT","ENTITLEMENT PRICE IMPACT",]
# 		desc_list = ["APPROVAL","ENTITLEMENT DESCRIPTION","ENTITLEMENT VALUE","CALCULATION FACTOR","ENTITLEMENT COST IMPACT","ENTITLEMENT PRICE IMPACT",]

# 		#attr_dict = {"APPROVAL":"APPROVAL","ENTITLEMENT DESCRIPTION": "ENTITLEMENT DESCRIPTION","ENTITLEMENT VALUE": "ENTITLEMENT VALUE","DATA TYPE":"DATA TYPE","FACTOR CURRENCY": "FACTOR CURRENCY","CALCULATION FACTOR": "CALCULATION FACTOR","ENTITLEMENT PRICE IMPACT":"ENTITLEMENT PRICE IMPACT","ENTITLEMENT COST IMPACT":"ENTITLEMENT COST IMPACT",}
# 		attr_dict = {"APPROVAL":"APPROVAL","ENTITLEMENT DESCRIPTION": "ENTITLEMENT DESCRIPTION","ENTITLEMENT VALUE": "ENTITLEMENT VALUE","CALCULATION FACTOR": "CALCULATION FACTOR","ENTITLEMENT PRICE IMPACT":"ENTITLEMENT PRICE IMPACT","ENTITLEMENT COST IMPACT":"ENTITLEMENT COST IMPACT",}
# 		date_field = []
		
# 		insertservice = ""
# 		Trace.Write("TableObj__J"+str(TableObj)+" EntitlementType_J "+str(EntitlementType))
# 	if TableObj is None and (EntitlementType == "EQUIPMENT"): 
# 		Trace.Write('not inserted')
# 		getnameentallowed = []
# 		if product_tabs_obj:
# 			for product_tab_obj in product_tabs_obj:
# 				# section=========================product_tab_obj.TAB_NAME,
# 				product_section =  str(product_tab_obj.TAB_CODE)+'_'+ str(product_tab_obj.TAB_NAME)
# 				Trace.Write("product_tab_obj"+str(product_section))
# 				list_of_tabs.append(product_section)
# 				Trace.Write("list_of_tabs"+str(list_of_tabs))
# 				sysectObj = Sql.GetFirst(
# 					"SELECT RECORD_ID,SECTION_DESC,SECTION_NAME FROM SYSECT (NOLOCK) WHERE SECTION_NAME='"+str(product_section)+"'"
# 				)
# 				date_boot_field=[]
# 				tablistdict = {}
# 				if sysectObj and str(sysectObj.SECTION_NAME) == str(product_section):
# 					Section_id = sysectObj.RECORD_ID
# 					Section_desc = sysectObj.SECTION_DESC.split('_')
# 					Section_desc = sysectObj.SECTION_DESC.split('_')[len(Section_desc) - 1]
# 				else:
# 					get_last_secid = SqlHelper.GetFirst("select max(SAPCPQ_ATTRIBUTE_NAME) as saprec_id from sysect where SAPCPQ_ATTRIBUTE_NAME like '%SYSECT-SA%'")
# 					Trace.Write("product_tab_obj--2683---"+str(product_section))
# 					if get_last_secid:
# 						get_last_secid = get_last_secid.saprec_id.split('-')[2]
# 						get_last_secid = int(int(get_last_secid)) + 1
# 						get_lastsection_val = 'SYSECT-SA-'+ str(get_last_secid)
# 						getsect_tab = SqlHelper.GetTable("SYSECT")
# 						tbrowsect = {}
# 						tbrowsect['RECORD_ID'] = str(Guid.NewGuid()).upper()
# 						tbrowsect['SAPCPQ_ATTRIBUTE_NAME'] = get_lastsection_val
# 						tbrowsect['SECTION_DESC'] =  str(product_section)
# 						tbrowsect['SECTION_NAME'] =  str(product_section)
# 						tbrowsect['SECTION_PARTNUMBER'] =  TreeParam.upper()
# 						getsect_tab.AddRow(tbrowsect)
# 						Sql.Upsert(getsect_tab)
# 						sysectObj = Sql.GetFirst("SELECT RECORD_ID,SECTION_DESC FROM SYSECT (NOLOCK) WHERE SECTION_NAME='" + str(product_section) + "'")
# 						if sysectObj:
# 							Section_id = sysectObj.RECORD_ID
# 							Section_desc = sysectObj.SECTION_DESC.split('_')
# 							Section_desc = sysectObj.SECTION_DESC.split('_')[len(Section_desc) - 1]
# 				add_style =  add_style_color = ""
# 				sec_str_boot += ('<div id="sec_'+str(Section_id)+ '" class="dyn_main_head master_manufac glyphicon pointer   glyphicon-chevron-down margtop10" onclick="dyn_main_sec_collapse_arrow(this)" data-target="#sc_'+ str(Section_id)+ '" data-toggle="collapse" <label class="onlytext"><label class="onlytext"><div>'+ str(Section_desc).upper()+ '</div></label></div><div id="sc_'+str(Section_id)+ '" class="collapse in "><table id="' + str(Section_id)+ '" class= "getentdata" data-filter-control="true" data-maintain-selected="true" data-locale = "en-US" data-escape="true" data-html="true"  data-show-header="true" > <thead><tr class="hovergrey">')
# 				for key, invs in enumerate(list(desc_list)):
# 					invs = str(invs).strip()
# 					qstring = attr_dict.get(str(invs)) or ""
# 					sec_str_boot += (
# 						'<th data-field="'
# 						+ invs
# 						+ '" data-title-tooltip="'
# 						+ str(qstring)
# 						+ '" >'
# 						+ str(qstring)
# 						+ "</th>"
# 					)
# 				sec_str_boot += '</tr></thead><tbody onclick="Table_Onclick_Scroll(this)" ></tbody></table>'
# 				sec_str_boot += ('<div id = "btn_ent" class="g4  except_sec removeHorLine iconhvr sec_edit_sty" style="display: none;"><button id="entcancel" class="btnconfig btnMainBanner sec_edit_sty_btn"  onclick="fabcostlocatecancel(this)" style="display: none;" class="btnconfig">CANCEL</button><button id="entsave" class="btnconfig btnMainBanner sec_edit_sty_btn"  onclick="fabcostlocatesave(this)" style="display: none;" class="btnconfig">SAVE</button></div>')
# 				attribute_Name_list = []
# 				Trace.Write(" tabwise_product_attributes.get(product_tab_obj.TAB_PROD_ID)"+str(tabwise_product_attributes.get(product_tab_obj.TAB_PROD_ID)))
# 				if tabwise_product_attributes.get(product_tab_obj.TAB_PROD_ID):
# 					for attribute in tabwise_product_attributes.get(product_tab_obj.TAB_PROD_ID):
# 						new_value_dicta = {}
# 						attrName = attribute['attribute_name']
# 						attrLabel = attribute['attribute_label']	
# 						attrSysId = attribute['attribute_system_id']
# 						attribute_code = attribute['attribute_code']					
# 						STDVALUES =  Sql.GetFirst("SELECT * FROM STANDARD_ATTRIBUTE_VALUES WHERE SYSTEM_ID like '%{sys_id}%' ".format(sys_id = attrSysId)  )
# 						if STDVALUES:
# 							attrValue = STDVALUES.STANDARD_ATTRIBUTE_VALUE
# 							if attrValue == "DefaultValue":
# 								attrValue = ''
# 						else:
# 							attrValue = ''
						
# 						attribute_Name_list.append(attrSysId)
# 						DType = attribute['attribute_dtype']
# 						Trace.Write(str(DType)+'----'+str(attrName)+'--attrName---attrSysId--'+str(attrSysId))
# 						Trace.Write(str(attrLabel)+'--attrLabel----attrValue--'+str(attrValue))
# 						if attrSysId in attributesdisallowedlst:
# 							if attrSysId in attributedefaultvalue:
# 								add_style = "display:none;color:#1B78D2"
# 							else:
# 								add_style = "display:none;"
# 							attributes_disallowed_list.append(attrSysId)
# 						else:
# 							add_style = ""
# 						Trace.Write(str(attrSysId)+'--attrLabel-2602---attrValue--'+str(add_style))
# 						if attrSysId in attributedefaultvalue:
# 							Trace.Write("add_style----3077----- "+str(attrSysId))
# 							add_style = "color:#1B78D2"
# 						# if attrSysId in attributedefaultvalue:
# 						# 	add_style_color = ";color: red"
# 						# else:
# 						# 	add_style_color = ""
# 						if attrSysId in attributeEditlst :
# 							disable_edit = 'disable_edit'
# 							edit_pencil_icon = '<a href="#" class="editclick"><i title="Double Click to Edit" class="fa fa-pencil"  aria-hidden="true"></i></a>'
							
# 						else:
# 							disable_edit = ''
# 							edit_pencil_icon = '<a href="#" class="editclick"><i title="Double Click to Edit" class="fa fa-lock"  aria-hidden="true"></i></a>'
# 						attrValueSysId = attributevalues.get(attrSysId)
# 						Trace.Write('attrValueSysId'+str(attrValueSysId))
# 						if DType == 'Check Box' and attrValueSysId is None:
# 							attr_value =''
# 							ent_val_code = ''
# 							Trace.Write("attrValueSysId---inside"+str(attrValueSysId))
# 						elif  DType == 'Free Input, no Matching':
# 							if attributevalues.get(attrSysId) is None:
# 								attr_value = ''
# 							else:
# 								attr_value = attributevalues.get(attrSysId)	
# 							Trace.Write('attr_value'+str(attr_value)+'---'+str(attrSysId))
# 							ent_val_code = attrValueSysId
# 						else:
# 							attr_value = attrValue
# 							ent_val_code = attrValueSysId
# 						# Inserting Rows:
# 						Trace.Write('attr_value------1'+str(attr_value)+'---'+str(attrSysId))
# 						insertservice += """<QUOTE_ITEM_ENTITLEMENT>
# 							<ENTITLEMENT_NAME>{ent_name}</ENTITLEMENT_NAME>
# 							<ENTITLEMENT_VALUE_CODE>{ent_val_code}</ENTITLEMENT_VALUE_CODE>
# 							<ENTITLEMENT_TYPE>{ent_type}</ENTITLEMENT_TYPE>							
# 							<ENTITLEMENT_DISPLAY_VALUE>{ent_disp_val}</ENTITLEMENT_DISPLAY_VALUE>
# 							<ENTITLEMENT_DESCRIPTION>{ent_desc}</ENTITLEMENT_DESCRIPTION>
# 							<ENTITLEMENT_COST_IMPACT>{ct}</ENTITLEMENT_COST_IMPACT>
# 							<ENTITLEMENT_PRICE_IMPACT>{pi}</ENTITLEMENT_PRICE_IMPACT>
# 							<IS_DEFAULT>{is_default}</IS_DEFAULT>
# 							<PRICE_METHOD>{pm}</PRICE_METHOD>
# 							<CALCULATION_FACTOR>{cf}</CALCULATION_FACTOR>
# 							</QUOTE_ITEM_ENTITLEMENT>""".format(ent_name = str(attrSysId),ent_val_code =ent_val_code,ent_type = DType,ent_desc = attrName,ent_disp_val = attr_value,ct = '',pi = '',is_default =  '1' if str(attrSysId) in attributedefaultvalue else '0',pm = '',cf = '')
# 						if DType == "Drop Down":
# 							Trace.Write('attrSysId--2324--drop down----'+str(attrSysId))
# 							#STDVALUES =  Sql.GetList("SELECT * from STANDARD_ATTRIBUTE_VALUES where  SYSTEM_ID like '%{sys_id}%' and STANDARD_ATTRIBUTE_CODE = '{attr_code}' ".format(sys_id = str(attrSysId), attr_code = attribute_code )  )
# 							STDVALUES = Sql.GetList("""SELECT TOP 20 A.PA_ID, A.PAV_ID, A.STANDARD_ATTRIBUTE_VALUE_CD, A.STANDARD_ATTRIBUTE_PRICE, A.NON_STANDARD_VALUE, A.NON_STANDARD_DISPLAY_VALUE, 
# 							A.PRODUCT_ATT_IMAGE_OFF_ALT_TEXT, A.SORT_RANK, A.RELATED_PRODUCT_ID

# 							, COALESCE(P.PRODUCT_CATALOG_CODE, A.VALUE_CATALOG_CODE) VALUE_CATALOG_CODE

# 							, PA.STANDARD_ATTRIBUTE_CODE, COALESCE(P.PRODUCT_NAME, V.STANDARD_ATTRIBUTE_DISPLAY_VAL) STANDARD_ATTRIBUTE_DISPLAY_VAL, V.SYSTEM_ID,V.STANDARD_ATTRIBUTE_VALUE, V.SYSTEM_ID AS VALUE_SYSTEM_ID, V.UNIT_ID AS VALUE_UNIT_ID, V.BILLING_PERIOD_ID AS VALUE_BILLING_PERIOD_ID
# 							, PA.USEALTERNATIVEPRICINGFORPRODUCTSINCONTAINER
# 							, COALESCE(P_ML.PRODUCT_NAME, P.PRODUCT_NAME, STDML.STANDARD_ATTRIBUTE_DISPLAY_VAL, V.SYSTEM_ID,V.STANDARD_ATTRIBUTE_DISPLAY_VAL) AS ML_NON_STANDARD_DISPLAY_VALUE
# 							FROM PRODUCT_ATTRIBUTES PA INNER JOIN ATTRIBUTES A ON PA.PA_ID=A.PA_ID 
# 							INNER JOIN STANDARD_ATTRIBUTE_VALUES V ON A.STANDARD_ATTRIBUTE_VALUE_CD = V.STANDARD_ATTRIBUTE_VALUE_CD  
# 							LEFT OUTER JOIN PRODUCTS P ON A.RELATED_PRODUCT_ID=P.PRODUCT_ID 
# 							LEFT OUTER JOIN PRODUCTS_ML P_ML ON P.PRODUCT_ID=P_ML.PRODUCT_ID AND P_ML.ML_ID=0
# 							LEFT JOIN  ATTRIBUTES_ML ML ON A.PAV_ID=ML.PAV_ID AND ML.ML_ID= 0
# 							LEFT JOIN STANDARD_ATTRIBUTE_VALUES_ML STDML ON A.STANDARD_ATTRIBUTE_VALUE_CD=STDML.STANDARD_ATTRIBUTE_VALUE_CD AND STDML.ML_ID=0 LEFT OUTER JOIN test_USD_L1 ON COALESCE(P.PRODUCT_CATALOG_CODE, A.VALUE_CATALOG_CODE) = test_USD_L1.PARTNUMBER AND ISNULL(A.PRICINGCODE, '')=ISNULL(test_USD_L1.PRICECODE, '') 
# 							WHERE PA.PRODUCT_ID ={productId} AND V.STANDARD_ATTRIBUTE_CODE  = {sys_id} ORDER BY A.SORT_RANK""".format(sys_id = attribute_code,productId = str(product_obj.PRD_ID)))
# 							VAR1 = sec_str1 = selected_option = ""
# 							if STDVALUES:
# 								if attributevalues.get(attrSysId) is not None:
# 									select_option = 'selected'
# 									default = ''
# 								else:
# 									select_option = ""
# 									default = 'selected'
# 									selected_option = ' title="Select" '
# 								VAR1 += '<option value="select" ' +str(default)+' style= "display:none;"> </option>'
# 								for value in STDVALUES:
# 									if value.SYSTEM_ID in dropdowndisallowlist:
# 										disallow_style = "style = 'display:none'"
# 									else:	
# 										disallow_style = ""
# 									if str(selected_option)=='selected':
# 										selected_option = ' title="'+str(value.STANDARD_ATTRIBUTE_DISPLAY_VAL)+'" '
# 									VAR1 += (
# 										'<option '+disallow_style+' id="'+value.SYSTEM_ID+'"  value = "'
# 										+ value.STANDARD_ATTRIBUTE_DISPLAY_VAL
# 										+ '"'+select_option+'>'
# 										+ value.STANDARD_ATTRIBUTE_DISPLAY_VAL
# 										+ "</option>"
# 									)
# 							sec_str1 += (
# 								'<select class="form-control remove_yellow '+str(disable_edit)+'" style ="'+str(add_style)+'" id = "'
# 								+ str(attrSysId)
# 								+ '" type="text"  data-content ="'
# 								+ str(attrSysId)
# 								+ '" class="form-control '+str(disable_edit)+'" onchange="editent_bt(this)" '+str(selected_option)+'  disabled>'
# 								+ VAR1
# 								+ "</select>"
# 							)
# 								#sec_str += "<option id='"+str(attrcode)+"' >" + str(optionvalue) + "</option>"
# 							#sec_str += "</select></td>"
# 						elif DType == "Check Box":
# 							multi_select_attr_list[attrSysId] = ""
# 							Trace.Write('attrSysId--2324--checkbox---2624------'+str(attrSysId)+'---'+str(multi_select_attr_list))
# 							#STDVALUES =  Sql.GetList("SELECT * from STANDARD_ATTRIBUTE_VALUES where  SYSTEM_ID like '%{sys_id}%' and STANDARD_ATTRIBUTE_CODE = '{attr_code}' ".format(sys_id = str(attrSysId), attr_code = attribute_code )  )
# 							STDVALUES = Sql.GetList("""SELECT TOP 20 A.PA_ID, A.PAV_ID, A.STANDARD_ATTRIBUTE_VALUE_CD, A.STANDARD_ATTRIBUTE_PRICE, A.NON_STANDARD_VALUE, A.NON_STANDARD_DISPLAY_VALUE, 
# 							A.PRODUCT_ATT_IMAGE_OFF_ALT_TEXT, A.SORT_RANK, A.RELATED_PRODUCT_ID

# 							, COALESCE(P.PRODUCT_CATALOG_CODE, A.VALUE_CATALOG_CODE) VALUE_CATALOG_CODE

# 							, PA.STANDARD_ATTRIBUTE_CODE, COALESCE(P.PRODUCT_NAME, V.STANDARD_ATTRIBUTE_DISPLAY_VAL) STANDARD_ATTRIBUTE_DISPLAY_VAL, V.SYSTEM_ID,V.STANDARD_ATTRIBUTE_VALUE, V.SYSTEM_ID AS VALUE_SYSTEM_ID, V.UNIT_ID AS VALUE_UNIT_ID, V.BILLING_PERIOD_ID AS VALUE_BILLING_PERIOD_ID
# 							, PA.USEALTERNATIVEPRICINGFORPRODUCTSINCONTAINER
# 							, COALESCE(P_ML.PRODUCT_NAME, P.PRODUCT_NAME, STDML.STANDARD_ATTRIBUTE_DISPLAY_VAL, V.SYSTEM_ID,V.STANDARD_ATTRIBUTE_DISPLAY_VAL) AS ML_NON_STANDARD_DISPLAY_VALUE
# 							FROM PRODUCT_ATTRIBUTES PA INNER JOIN ATTRIBUTES A ON PA.PA_ID=A.PA_ID 
# 							INNER JOIN STANDARD_ATTRIBUTE_VALUES V ON A.STANDARD_ATTRIBUTE_VALUE_CD = V.STANDARD_ATTRIBUTE_VALUE_CD  
# 							LEFT OUTER JOIN PRODUCTS P ON A.RELATED_PRODUCT_ID=P.PRODUCT_ID 
# 							LEFT OUTER JOIN PRODUCTS_ML P_ML ON P.PRODUCT_ID=P_ML.PRODUCT_ID AND P_ML.ML_ID=0
# 							LEFT JOIN  ATTRIBUTES_ML ML ON A.PAV_ID=ML.PAV_ID AND ML.ML_ID= 0
# 							LEFT JOIN STANDARD_ATTRIBUTE_VALUES_ML STDML ON A.STANDARD_ATTRIBUTE_VALUE_CD=STDML.STANDARD_ATTRIBUTE_VALUE_CD AND STDML.ML_ID=0 LEFT OUTER JOIN test_USD_L1 ON COALESCE(P.PRODUCT_CATALOG_CODE, A.VALUE_CATALOG_CODE) = test_USD_L1.PARTNUMBER AND ISNULL(A.PRICINGCODE, '')=ISNULL(test_USD_L1.PRICECODE, '') 
# 							WHERE PA.PRODUCT_ID ={productId} AND V.STANDARD_ATTRIBUTE_CODE  = {sys_id} ORDER BY A.SORT_RANK""".format(sys_id = attribute_code,productId = str(product_obj.PRD_ID)))
# 							VAR1 = sec_str1 = ""
# 							if STDVALUES:
# 								for value in STDVALUES:
# 									if value.SYSTEM_ID in dropdowndisallowlist:
# 										disallow_style = "style = 'display:none'"
# 									else:	
# 										disallow_style = ""
# 									#if attrValue == value.STANDARD_ATTRIBUTE_VALUE:
# 										#Trace.Write("SYSTEM_ID"+str(value.SYSTEM_ID))
# 										#get_code = Sql.GetFirst("SELECT * from STANDARD_ATTRIBUTE_VALUES where  SYSTEM_ID like '{sys_id}' ".format(sys_id = str(value.SYSTEM_ID) )  )
# 										#get_id = [ attr[str(get_code.STANDARD_ATTRIBUTE_CODE)] for attr in overall_attribute_list]
# 										#getnameentallowed.append(value.SYSTEM_ID)
# 										#Trace.Write('valueeeee----'+str(getnameentallowed))
# 									VAR1 += (
# 										'<option '+str(disallow_style)+'  id="'+str(value.SYSTEM_ID)+'" value = "'
# 										+ str(value.STANDARD_ATTRIBUTE_DISPLAY_VAL)
# 										+ '">'
# 										+ str(value.STANDARD_ATTRIBUTE_DISPLAY_VAL)
# 										+ "</option>"
# 									)
# 							sec_str1 += (
# 								'<select class="form-control remove_yellow div_multi_checkbox" style ="'+str(add_style)+'" id = "'
# 								+ str(attrSysId)
# 								+ '" type="text"  data-content ="'
# 								+ str(attrSysId)
# 								+ '" class="form-control" onchange="editent_bt(this)" disabled>'
# 								+ str(VAR1)
# 								+ "</select>"
# 							)
# 								#sec_str += "<option id='"+str(attrcode)+"' >" + str(optionvalue) + "</option>"
# 							#sec_str += "</select></td>"
# 						elif DType == "Free Input, no Matching":
# 							if str(attrSysId) == "AGS_REL_STDATE":
# 								datepicker = "onclick_datepicker_locdate('" + attrSysId + "')"
# 								datepicker_onchange = "onchangedatepicker('" + attrSysId + "')"

# 								sec_str1 += (
# 									'<input class="form-control no_border_bg  datePickerField wth157fltltbrdbt '+str(disable_edit)+'" id = "'
# 									+ str(attrSysId)
# 									+ '" type="text"  style ="'+str(add_style)+'"  onclick="'+ str(datepicker)+ '"  data-content ="'
# 									+ str(attr_value)
# 									+ '" value = "'+str(attr_value)+'" title="'+str(attr_value)+'"  disabled>'
# 									+ "</input> "
# 								)
# 							else:
# 								STDVALUES =  Sql.GetFirst("SELECT STANDARD_ATTRIBUTE_VALUE from STANDARD_ATTRIBUTE_VALUES  where  SYSTEM_ID like '%{sys_id}%' ".format(sys_id = str(attrSysId))  )							
# 								sec_str1 = ""
# 								if attr_value == "DefaultValue":
# 									attr_value = ''
# 								sec_str1 += (
# 									'<input class="form-control '+str(disable_edit)+'" id = "'
# 									+ str(attrSysId)
# 									+ '" type="text"  data-content ="'
# 									+ str(attrSysId)
# 									+ '" value = "'+str(attr_value)+'" title = "'+str(attr_value)+'" onchange="editent_bt(this)" disabled>'
# 									+ "</input>"
# 								)
# 						else:
# 							getinval = ''
# 							Trace.Write('attrSysId--input-----'+str(attrSysId))
# 							STDVALUES =  Sql.GetFirst("SELECT STANDARD_ATTRIBUTE_VALUE from STANDARD_ATTRIBUTE_VALUES  where  SYSTEM_ID like '%{sys_id}%' ".format(sys_id = str(attrSysId))  )
# 							if STDVALUES:
# 								getinval = STDVALUES.STANDARD_ATTRIBUTE_VALUE
# 							else:
# 								getinval = ''

# 							sec_str1 += (
# 								'<input class="form-control '+str(disable_edit)+'" id = "'
# 								+ str(attrSysId)
# 								+ '" type="text"  data-content ="'
# 								+ str(attrSysId)
# 								+ '"  disabled>'
# 								+ "</input>"
# 							)
# 						#getnameentallowed.append(attrName)
# 						#totaldisallowlist = [item for item in attributesdisallowedlst if item not in getnameentallowed]
# 						new_value_dicta["APPROVAL"] = ""	
# 						new_value_dicta["ENTITLEMENT DESCRIPTION"] = str(attrName)
# 						Trace.Write('sec_str1---2372---'+str(sec_str1))
# 						if DType == "Drop Down" or DType == "Check Box" or DType =="Free Input, no Matching":
# 							new_value_dicta["ENTITLEMENT VALUE"] =  sec_str1
# 						else:
# 							new_value_dicta["ENTITLEMENT VALUE"] =  attrValue
# 						#new_value_dicta["FACTOR CURRENCY"] = ""
# 						new_value_dicta["ENTITLEMENT COST IMPACT"]= ""
# 						new_value_dicta["ENTITLEMENT PRICE IMPACT"]= str("<abbr class = 'wid90_per' title=''></abbr>")+str(edit_pencil_icon)
# 						#new_value_dicta["DATA TYPE"] = ""
# 						new_value_dicta["CALCULATION FACTOR"] = ""
# 						if new_value_dicta:
# 							date_boot_field.append(new_value_dicta)
# 					sec_str_boot += ('</div>')
# 				if len(date_boot_field) > 0:
# 					tablistdict[Section_id] = date_boot_field
					
# 				if len(tablistdict) > 0:
# 					tablistnew.append(tablistdict)
# 				table_ids = '#'+Section_id
# 				getdivid = '#sc_'+Section_id+' .sec_edit_sty'
# 				getdividbtn = '#sc_'+Section_id+' #btn_ent .sec_edit_sty_btn'
# 				getprevdicts +=   ("try{var dict_new = {};$('"+str(table_ids)+" tbody tr td select').each(function () {dict_new[$(this).attr('id')] = $(this).children(':selected').val();});$('"+str(table_ids)+" tbody tr td input').each(function () {dict_new[$(this).attr('id')] = $(this).val();});console.log('dict_new-2190-2938----',dict_new);}catch{console.log('')}")
# 				#dbl_clk_function +=   ("try{var dict_new = {};$('"+str(table_ids)+"').on('dbl-click-cell.bs.table', function (e, row, $element) { $('"+str(table_ids)+" tbody tr:visible').each(function () {dict_new[$(this).find('td:nth-child(3) select').attr('id')] =$(this).find('td:nth-child(3) select').children(':selected').val() ;});$('"+str(table_ids)+" tbody tr:visible').each(function () {dict_new[$(this).find('td:nth-child(3) input').attr('id')] =  $(this).find('td:nth-child(3) input').val();});console.log('dblclk_dict_new-28001--',dict_new);localStorage.setItem('prventdict', JSON.stringify(dict_new))})}catch{console.log('')}")
# 				#dbl_clk_function +=   ("try{var dict_new = {};$('"+str(table_ids)+"').on('dbl-click-cell.bs.table', function (e, row, $element) { $('"+str(table_ids)+" tbody tr td select').each(function () {dict_new[$(this).attr('id')] = $(this).children(':selected').val();});$('"+str(table_ids)+" tbody tr td input').each(function () {dict_new[$(this).attr('id')] = $(this).val();});console.log('dblclk_dict_new-2800--',dict_new);localStorage.setItem('prventdict', JSON.stringify(dict_new))})}catch{console.log('')}")
# 				dbl_clk_function +=   ("try{var dict_new = {};localStorage.setItem('editfirst','true');$('"+str(table_ids)+"').on('dbl-click-cell.bs.table', function (e, row, $element) { localStorage.setItem('AddNew','false');$('"+str(table_ids)+" tbody tr:visible').each(function () {var getcostimpact =  $(this).find('td:nth-child(7) ').text();var getpriceimpact =  $(this).find('td:nth-child(8) ').text();dict_new[$(this).find('td:nth-child(3) select').attr('id')] =$(this).find('td:nth-child(3) select').children(':selected').val()+'||'+getcostimpact+'||'+getpriceimpact;});var arr = [];$('"+str(table_ids)+" tbody tr:visible').each(function () {if ($(this).find('td:nth-child(3) input') && !($(this).find('td:nth-child(3) input').attr('type') == 'checkbox') ){var getcostimpact =  $(this).find('td:nth-child(7) ').text();var getpriceimpact =  $(this).find('td:nth-child(8) ').text();dict_new[$(this).find('td:nth-child(3) input').attr('id')] =  $(this).find('td:nth-child(3) input').val()+'||'+getcostimpact+'||'+getpriceimpact;}else if ($(this).find('td:nth-child(3) input').attr('type') == 'checkbox') {var getcostimpact =  $(this).find('td:nth-child(7) ').text();var getpriceimpact =  $(this).find('td:nth-child(8) ').text();$(this).find('.mulinput:checked').each(function () {arr.push($(this).val());console.log('arr',arr) });dict_new[$(this).find('td:nth-child(3) select').attr('id')] =  arr+'||'+getcostimpact+'||'+getpriceimpact;};});console.log('dblclk_dict_new-28002--',dict_new,'--',"+str(dropdowndisallowlist)+");localStorage.setItem('prventdict', JSON.stringify(dict_new))})}catch(e){console.log('error---12',e)}")
				
# 				dbl_clk_function += (
# 					"try { console.log('2944 start----');var newentdict =[]; var newentValues =[]; var getentedictip = [];$('"+str(table_ids)+"').on('dbl-click-cell.bs.table', function (e, row, $element) {if(localStorage.getItem('EDITENT_SEC') != 'EDIT'){console.log('tset--prev value-2944---222-----',this.value);localStorage.setItem('EDITENT_SEC','EDIT'); $('"+str(table_ids)+" .disable_edit').prop('disabled', false);$('.sec_edit_sty_btn').css('display','block');$('#sc_'+'"+str(Section_id)+"').addClass('header_section_div header_section_div_pad_bt10');$('"+str(getdivid)+"').css('display','block');$('"+str(table_ids)+" .disable_edit').removeClass('remove_yellow ').addClass('light_yellow');$('#AGS_CON_DAY').removeClass('light_yellow').addClass('remove_yellow');$('#AGS_CON_DAY').prop('disabled', true);$('"+str(getdividbtn)+"').css('display','block');$('#entsave').css('display','block');$('#entcancel').css('display','block');$('"+str(table_ids)+" .MultiCheckBox').css('pointer-events','auto');var getmanualip = $('#ADDL_PERF_GUARANTEE_91_1').find(':selected').text();if(getmanualip.toUpperCase() == 'MANUAL INPUT'){ $('#ADDL_PERF_GUARANTEE_91_1_imt').removeAttr('disabled');$('#ADDL_PERF_GUARANTEE_91_1_imt').removeClass('remove_yellow ').addClass('light_yellow');$('#ADDL_PERF_GUARANTEE_91_1_primp').removeAttr('disabled');$('#ADDL_PERF_GUARANTEE_91_1_primp').removeClass('remove_yellow ').addClass('light_yellow');}$('#ADDL_PERF_GUARANTEE_91_1_imt').attr('disabled', 'disabled');$('"+str(table_ids)+" tbody tr td:nth-child(6) input').removeClass('light_yellow').addClass('remove_yellow');$('"+str(table_ids)+" tbody tr td:nth-child(4) input').removeClass('light_yellow').addClass('remove_yellow');$('#entsave').css('display','block');$('#entcancel').css('display','block');$('input').on('focus', function () {var previnp = $(this).data('val', $(this).val());var getprevid = this.id;var prev_concate_data = getprevid +'='+previnp;}).change(function() {var prev = $(this).data('val');var current = $(this).val();var getseltabledesc = this.id;var getinputtbleid =  $(this).closest('table').attr('id');var concated_data = getinputtbleid+'|'+current+'|'+getseltabledesc;if(!getentedictip.includes(concated_data)){getentedictip.push(concated_data)};getentedictip1 = JSON.stringify(getentedictip);localStorage.setItem('getdictentdata', getentedictip1);});}})}catch {console.log('error---')}"
# 				)
# 				Trace.Write('dbl_clk_function--2946-'+str(dbl_clk_function))
# 				'''dbl_clk_function += (
# 					"try {var getentedict = [];$('"+str(table_ids)+"').on('dbl-click-cell.bs.table', function (e, row, $element) {console.log('tset--prev value---',this.value);$('"+str(table_ids)+"').find(':input(:disabled)').prop('disabled', false);$('"+str(table_ids)+" tbody  tr td select option').css('background-color','lightYellow');$('"+str(table_ids)+" tbody  tr td input').css('background-color','lightYellow');$('"+str(table_ids)+"  tbody tr td select').addClass('light_yellow');$('"+str(table_ids)+" .disable_edit').addClass('light_yellow');$('#fabcostlocate_save').css('display','block');$('#fabcostlocate_cancel').css('display','block');});}catch {console.log('error---')}"
# 				)'''
			
# 				tbrow = {}
# 				tbrow["QUOTE_SERVICE_ENTITLEMENT_RECORD_ID"] = str(Guid.NewGuid()).upper()
# 				tbrow["QUOTE_ID"] = QUOTE_ID
# 				tbrow["QUOTE_NAME"] = QUOTE_NAME
# 				tbrow["QUOTE_RECORD_ID"] = QUOTE_RECORD_ID
# 				tbrow["QTEREV_RECORD_ID"] = QTEREV_RECORD_ID
# 				tbrow["QTEREV_ID"] = Quote.GetGlobal("quote_revision_id")
# 				tbrow["QTESRV_RECORD_ID"] = QUOTE_SERVICE_RECORD_ID
# 				tbrow["SERVICE_RECORD_ID"] = SERVICE_RECORD_ID
# 				tbrow["SERVICE_ID"] = SERVICE_ID
# 				tbrow["SERVICE_DESCRIPTION"] = SERVICE_DESCRIPTION
# 				tbrow["ENTITLEMENT_XML"]=insertservice
# 				tbrow["CPS_CONFIGURATION_ID"] = Fullresponse["id"]
# 				tbrow["SALESORG_RECORD_ID"] = SALESORG_RECORD_ID
# 				tbrow["SALESORG_ID"] = SALESORG_ID
# 				tbrow["SALESORG_NAME"] = SALESORG_NAME
# 				tbrow["CPS_MATCH_ID"] = 11
				
# 				tbrow["KB_VERSION"] = Fullresponse["kbKey"]["version"]
# 				tbrow["CPQTABLEENTRYADDEDBY"] = userId
# 				tbrow["CPQTABLEENTRYDATEADDED"] = datetime.now().strftime("%m/%d/%Y %H:%M:%S %p")

# 				columns = ', '.join("" + str(x) + "" for x in tbrow.keys())
# 				values = ', '.join("'" + str(x) + "'" for x in tbrow.values())
# 				insert_qtqtse_query = "INSERT INTO SAQTSE ( %s ) VALUES ( %s );" % (columns, values)				
# 			Sql.RunQuery(insert_qtqtse_query)
# 			if objname_ent == "SAQSAO":
# 				QueryStatement ="""
# 				MERGE SAQIEN SRC USING (SELECT A.ENTITLEMENT_XML,B.EQUIPMENT_ID,B.EQUIPMENT_RECORD_ID,B.LINE_ITEM_ID,A.QUOTE_ID,B.QUOTE_ITEM_COVERED_OBJECT_RECORD_ID,B.QTEITM_RECORD_ID,A.QUOTE_RECORD_ID,A.QTEREV_RECORD_ID,A.QUOTE_SERVICE_ENTITLEMENT_RECORD_ID,B.SERIAL_NO,A.SERVICE_DESCRIPTION,A.SERVICE_ID,A.SERVICE_RECORD_ID,A.SALESORG_ID,A.SALESORG_NAME,A.SALESORG_RECORD_ID,A.CPS_CONFIGURATION_ID,B.EQUIPMENT_LINE_ID FROM SAQTSE(NOLOCK) A JOIN SAQICO (NOLOCK) B ON A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.QTEREV_RECORD_ID = B.QTEREV_RECORD_ID AND A.SALESORG_ID =B.SALESORG_ID where A.QUOTE_RECORD_ID = '{rec}' AND A.QTEREV_RECORD_ID  = '{revision_rec_id}' )
# 				TGT ON (SRC.QUOTE_RECORD_ID = TGT.QUOTE_RECORD_ID AND SRC.QTEREV_RECORD_ID = TGT.QTEREV_RECORD_ID AND SRC.SERVICE_ID = TGT.SERVICE_ID AND SRC.EQUIPMENT_ID = TGT.EQUIPMENT_ID)
# 				WHEN MATCHED
# 				THEN UPDATE SET SRC.ENTITLEMENT_XML = TGT.ENTITLEMENT_XML
# 				WHEN NOT MATCHED BY TARGET
# 				THEN INSERT(QUOTE_ITEM_COVERED_OBJECT_ENTITLEMENTS_RECORD_ID,ENTITLEMENT_XML,EQUIPMENT_ID,EQUIPMENT_RECORD_ID,LINE_ITEM_ID,QUOTE_ID,QTEITMCOB_RECORD_ID,QTEITM_RECORD_ID,QUOTE_RECORD_ID,QTEREV_RECORD_ID,QTESRVENT_RECORD_ID,SERIAL_NO,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,CPS_CONFIGURATION_ID,EQUIPMENT_LINE_ID,CPQTABLEENTRYDATEADDED, CPQTABLEENTRYADDEDBY, ADDUSR_RECORD_ID, CpqTableEntryModifiedBy,
# 						CpqTableEntryDateModified)
# 				VALUES (NEWID(),ENTITLEMENT_XML,EQUIPMENT_ID,EQUIPMENT_RECORD_ID,LINE_ITEM_ID,QUOTE_ID,QUOTE_ITEM_COVERED_OBJECT_RECORD_ID,QTEITM_RECORD_ID,QUOTE_RECORD_ID,QTEREV_RECORD_ID,QUOTE_SERVICE_ENTITLEMENT_RECORD_ID,SERIAL_NO,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,CPS_CONFIGURATION_ID,EQUIPMENT_LINE_ID,'{datetimenow}', '{username}', {userid}, {userid}, '{datetimenow}' );""".format(rec=quoteid, datetimenow=datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"), userid=userId, username=userName, revision_rec_id = quote_revision_record_id )
			
# 			else:
# 				QueryStatement ="""
# 				MERGE SAQIEN SRC USING (SELECT A.ENTITLEMENT_XML,B.EQUIPMENT_ID,B.EQUIPMENT_RECORD_ID,B.LINE_ITEM_ID,A.QUOTE_ID,B.QUOTE_ITEM_COVERED_OBJECT_RECORD_ID,B.QTEITM_RECORD_ID,A.QUOTE_RECORD_ID,A.QTEREV_RECORD_ID,A.QUOTE_SERVICE_ENTITLEMENT_RECORD_ID,B.SERIAL_NO,A.SERVICE_DESCRIPTION,A.SERVICE_ID,A.SERVICE_RECORD_ID,A.SALESORG_ID,A.SALESORG_NAME,A.SALESORG_RECORD_ID,A.CPS_CONFIGURATION_ID,B.EQUIPMENT_LINE_ID FROM SAQTSE(NOLOCK) A JOIN SAQICO (NOLOCK) B ON A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.QTEREV_RECORD_ID = B.QTEREV_RECORD_ID AND A.SALESORG_ID =B.SALESORG_ID where A.QUOTE_RECORD_ID = '{rec}'  AND A.QTEREV_RECORD_ID  = '{revision_rec_id}' )
# 				TGT ON (SRC.QUOTE_RECORD_ID = TGT.QUOTE_RECORD_ID AND SRC.QTEREV_RECORD_ID = TGT.QTEREV_RECORD_ID AND SRC.SERVICE_ID = TGT.SERVICE_ID)
# 				WHEN MATCHED
# 				THEN UPDATE SET SRC.ENTITLEMENT_XML = TGT.ENTITLEMENT_XML
# 				WHEN NOT MATCHED BY TARGET
# 				THEN INSERT(QUOTE_ITEM_COVERED_OBJECT_ENTITLEMENTS_RECORD_ID,ENTITLEMENT_XML,EQUIPMENT_ID,EQUIPMENT_RECORD_ID,LINE_ITEM_ID,QUOTE_ID,QTEITMCOB_RECORD_ID,QTEITM_RECORD_ID,QUOTE_RECORD_ID,QTEREV_RECORD_ID,QTESRVENT_RECORD_ID,SERIAL_NO,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,CPS_CONFIGURATION_ID,EQUIPMENT_LINE_ID,CPQTABLEENTRYDATEADDED, CPQTABLEENTRYADDEDBY, ADDUSR_RECORD_ID, CpqTableEntryModifiedBy,
# 						CpqTableEntryDateModified)
# 				VALUES (NEWID(),ENTITLEMENT_XML,EQUIPMENT_ID,EQUIPMENT_RECORD_ID,LINE_ITEM_ID,QUOTE_ID,QUOTE_ITEM_COVERED_OBJECT_RECORD_ID,QTEITM_RECORD_ID,QUOTE_RECORD_ID,QTEREV_RECORD_ID,QUOTE_SERVICE_ENTITLEMENT_RECORD_ID,SERIAL_NO,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,CPS_CONFIGURATION_ID,EQUIPMENT_LINE_ID,'{datetimenow}', '{username}', {userid}, {userid}, '{datetimenow}' );""".format(rec=quoteid, datetimenow=datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"), userid=userId, username=userName, revision_rec_id = quote_revision_record_id)
				
# 				Sql.RunQuery(QueryStatement)
# 				QueryStatement =""
# 				MERGE SAQIEN SRC USING (SELECT A.ENTITLEMENT_XML,B.PART_NUMBER,B.PART_RECORD_ID,B.LINE_ITEM_ID,A.QUOTE_ID,B.QUOTE_ITEM_FORECAST_PART_RECORD_ID,B.QTEITM_RECORD_ID,A.QUOTE_RECORD_ID,A.QTEREV_RECORD_ID,A.QUOTE_SERVICE_ENTITLEMENT_RECORD_ID,A.SERVICE_DESCRIPTION,A.SERVICE_ID,A.SERVICE_RECORD_ID,A.SALESORG_ID,A.SALESORG_NAME,A.SALESORG_RECORD_ID,A.CPS_CONFIGURATION_ID,B.PART_LINE_ID FROM SAQTSE(NOLOCK) A JOIN SAQIFP (NOLOCK) B ON A.QUOTE_RECORD_ID  = B.QUOTE_RECORD_ID AND A.QTEREV_RECORD_ID = B.QTEREV_RECORD_ID AND A.SALESORG_ID =B.SALESORG_ID where A.QUOTE_RECORD_ID = '{rec}'  AND A.QTEREV_RECORD_ID  = '{revision_rec_id}' )
# 				TGT ON (SRC.QUOTE_RECORD_ID = TGT.QUOTE_RECORD_ID AND SRC.QTEREV_RECORD_ID = TGT.QTEREV_RECORD_ID AND SRC.SERVICE_ID = TGT.SERVICE_ID AND SRC.EQUIPMENT_ID = TGT.PART_NUMBER) 
# 				WHEN MATCHED THEN UPDATE SET SRC.ENTITLEMENT_XML = TGT.ENTITLEMENT_XML
# 				WHEN NOT MATCHED BY TARGET THEN INSERT(QUOTE_ITEM_COVERED_OBJECT_ENTITLEMENTS_RECORD_ID,ENTITLEMENT_XML,EQUIPMENT_ID,EQUIPMENT_RECORD_ID,LINE_ITEM_ID,QUOTE_ID,QTEITM_RECORD_ID,QUOTE_RECORD_ID,QTEREV_RECORD_ID,QTESRVENT_RECORD_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,CPS_CONFIGURATION_ID,EQUIPMENT_LINE_ID,CPQTABLEENTRYDATEADDED, CPQTABLEENTRYADDEDBY, ADDUSR_RECORD_ID, CpqTableEntryModifiedBy,CpqTableEntryDateModified) VALUES (NEWID(),ENTITLEMENT_XML,PART_NUMBER,PART_RECORD_ID,LINE_ITEM_ID,QUOTE_ID,QTEITM_RECORD_ID,QUOTE_RECORD_ID,QTEREV_RECORD_ID,QUOTE_SERVICE_ENTITLEMENT_RECORD_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,CPS_CONFIGURATION_ID,PART_LINE_ID,'{datetimenow}', '{username}', {userid}, {userid}, '{datetimenow}' );""".format(rec=quoteid, datetimenow=datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"), userid=userId, username=userName, revision_rec_id = quote_revision_record_id)
# 				Sql.RunQuery(QueryStatement)
# 			Trace.Write("getnameentallowed"+str(getnameentallowed))
# 			getnameentallowed = [i.replace('_00','') if '_00' in i else i.replace('_00','_0') if '_0' else i  for i in getnameentallowed ]
# 			totaldisallowlist = [item for item in attributesdisallowedlst if item not in getnameentallowed]	
# 			Trace.Write("totaldisallowlist"+str(totaldisallowlist))	
# 	elif EntitlementType == "SENDING_LEVEL":
# 		sec_str = getvaludipto = getvaludipt1 = getvaludipt2 = getvaludipt2lt = getvaludipt2lab = getvaludipto_q = getvaludipt2_q = getvaludipt2lt_q = getvaludipt2lab_q = getvaludipt2lab = getvaludipt3lab = getvaludipt3lab_q = getvaludipt3labt = getvaludipt3labt_q= getvaludipt1_q=  getlabortype_calc = gett1labor_calc= gett1labortype_calc =gett2labo_calc = gett2labotype_calc = gett3lab_calc = gett3labtype_calc = ""
# 		multi_select_attr_list = {}
# 		getnameentallowed = []
# 		sec_str_cf = sec_str_boot = sec_bnr = sec_str_primp =  ""
# 		#sec_str = "Entitlements are not applicable at this level"
# 		sec_str = "<div class='noRecDisp'>Entitlements are not applicable at this level</div>"
# 	else:
# 		getnameentallowed = []
# 		multi_select_attr_list = {}
# 		attributedefaultvalue = []

# 		Trace.Write('after inserting in table-----')
# 		getinnercon  = Sql.GetFirst("select QUOTE_RECORD_ID,QTEREV_RECORD_ID,convert(xml,replace(replace(ENTITLEMENT_XML,'&',';#38'),'''',';#39')) as ENTITLEMENT_XML from "+str(ObjectName)+" (nolock)  where  "+str(where)+"")
# 		GetXMLsecField = Sql.GetList("SELECT distinct e.QUOTE_RECORD_ID,e.QTEREV_RECORD_ID, replace(X.Y.value('(ENTITLEMENT_NAME)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_NAME,replace(X.Y.value('(IS_DEFAULT)[1]', 'VARCHAR(128)'),';#38','&') as IS_DEFAULT,replace(X.Y.value('(ENTITLEMENT_COST_IMPACT)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_COST_IMPACT,replace(X.Y.value('(CALCULATION_FACTOR)[1]', 'VARCHAR(128)'),';#38','&') as CALCULATION_FACTOR,replace(X.Y.value('(ENTITLEMENT_PRICE_IMPACT)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_PRICE_IMPACT,replace(X.Y.value('(ENTITLEMENT_TYPE)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_TYPE,replace(X.Y.value('(ENTITLEMENT_VALUE_CODE)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_VALUE_CODE,replace(X.Y.value('(ENTITLEMENT_DESCRIPTION)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_DESCRIPTION,replace(replace(X.Y.value('(ENTITLEMENT_DISPLAY_VALUE)[1]', 'VARCHAR(128)'),';#38','&'),';#39','''') as ENTITLEMENT_DISPLAY_VALUE,replace(X.Y.value('(PRICE_METHOD)[1]', 'VARCHAR(128)'),';#38','&') as PRICE_METHOD FROM (select '"+str(getinnercon.QUOTE_RECORD_ID)+"' as QUOTE_RECORD_ID,'"+str(getinnercon.QTEREV_RECORD_ID)+"' as QTEREV_RECORD_ID,convert(xml,'"+str(getinnercon.ENTITLEMENT_XML)+"') as ENTITLEMENT_XML ) e OUTER APPLY e.ENTITLEMENT_XML.nodes('QUOTE_ITEM_ENTITLEMENT') as X(Y) ")
# 		inserted_value_list = [val.ENTITLEMENT_NAME for val in GetXMLsecField if GetXMLsecField]
# 		for val in GetXMLsecField:
# 			#Trace.Write(str(val.ENTITLEMENT_NAME)+'--ENT___NAME---2908----'+str(val.IS_DEFAULT))
# 			if val.IS_DEFAULT == '1':
# 				#Trace.Write(str(val.ENTITLEMENT_NAME)+'--2910------'+str(val.IS_DEFAULT))
# 				attributedefaultvalue.append(val.ENTITLEMENT_NAME)
# 		Trace.Write('attributedefaultvalue--2912----2912---'+str(attributedefaultvalue))
# 		sec_str_cf = sec_str_boot = sec_bnr = sec_str_primp =  ""		
# 		## set entitlement_xml for cancel fn A055S000P01-3157 starts
# 		previous_entitlement_xml  = Sql.GetFirst("select ENTITLEMENT_XML from "+str(ObjectName)+" (nolock)  where  "+str(where)+"")	
# 		#Trace.Write('previous_entitlement_xml----'+str(previous_entitlement_xml))	
# 		Product.SetGlobal("previous_entitlement_xml", previous_entitlement_xml.ENTITLEMENT_XML)
# 		## set entitlement_xml for cancel fn A055S000P01-3157 ends
# 		list_of_tabs = []
# 		getprevdicts +=   ("var dict_new = {};var list_new = [];")	
# 		if str(TreeParentParam).upper() == "ADD-ON PRODUCTS":
# 			TreeSuperParentParam = ""
# 		Trace.Write('TreeParam----'+str(TreeParam)+'--'+str(ProductPartnumber))
# 		if TreeParam.upper() == ProductPartnumber or TreeParentParam.upper() == ProductPartnumber or TreeSuperParentParam == ProductPartnumber:	
# 			Trace.Write("@2756------->"+str(TreeParentParam))
			
# 			for product_tab_obj in product_tabs_obj:
# 				product_section =   str(product_tab_obj.TAB_CODE)+'_'+ str(product_tab_obj.TAB_NAME)
# 				Trace.Write("product_tab_obj"+str(product_section))
# 				tablistdict = {}
# 				date_boot_field = []
# 				list_of_tabs.append(product_section)
# 				if str(TreeParentParam).upper() == "ADD-ON PRODUCTS":
# 					sysectObj = Sql.GetFirst(
# 						"SELECT RECORD_ID,SECTION_DESC,SECTION_NAME FROM SYSECT (NOLOCK) WHERE SECTION_NAME='" + str(product_section) + "' AND SECTION_PARTNUMBER = '" + str(TreeParam.upper()) + "'"
# 					)
# 				else:
# 					sysectObj = Sql.GetFirst(
# 					"SELECT RECORD_ID,SECTION_DESC,SECTION_NAME FROM SYSECT (NOLOCK) WHERE SECTION_NAME='" + str(product_section) + "'"
# 				)
				
# 				if sysectObj and str(sysectObj.SECTION_NAME) == str(product_section):
# 					Section_id = sysectObj.RECORD_ID
# 					Section_desc = sysectObj.SECTION_DESC.split('_')
# 					Section_desc = sysectObj.SECTION_DESC.split('_')[len(Section_desc) - 1]
# 				else:
# 					get_last_secid = Sql.GetFirst("select max(SAPCPQ_ATTRIBUTE_NAME) as saprec_id from sysect where SAPCPQ_ATTRIBUTE_NAME like '%SYSECT-QT%'")
# 					if get_last_secid:
# 						get_last_secid = get_last_secid.saprec_id.split('-')[2]
# 						get_last_secid = int(int(get_last_secid)) + 1
# 						get_lastsection_val = 'SYSECT-QT-'+ str(get_last_secid)
# 						getsect_tab = SqlHelper.GetTable("SYSECT")
# 						tbrowsect = {}
# 						Section_id = tbrowsect['RECORD_ID'] = str(Guid.NewGuid()).upper()
# 						tbrowsect['SAPCPQ_ATTRIBUTE_NAME'] = get_lastsection_val
# 						tbrowsect['SECTION_DESC'] =  str(product_section) 
# 						tbrowsect['SECTION_NAME'] =  str(product_section)
# 						tbrowsect['SECTION_PARTNUMBER'] =  TreeParam.upper()
# 						getsect_tab.AddRow(tbrowsect)
# 						Sql.Upsert(getsect_tab)
# 						Section_desc = product_section.split('_')
# 						Section_desc =product_section.split('_')[len(Section_desc) - 1]

# 				if EntitlementType in ("EQUIPMENT","BUSINESSUNIT","TOOLS"):
# 					#Trace.Write("@@2794")
# 					sec_bnr += (
# 						'<div class="dyn_main_head master_manufac glyphicon pointer  glyphicon-chevron-down " id="'
# 						+ str(Section_id)+ '" onclick="dyn_main_sec_collapse_arrow(this)" data-target="#sec_'
# 						+ str(Section_id)
# 						+ '" data-toggle="collapse"><label class="onlytext"><label class="onlytext"><div><div id="ctr_drop" class="btn-group dropdown"><div class="dropdown"><i data-toggle="dropdown" class="fa fa-sort-desc dropdown-toggle"></i><ul class="dropdown-menu left" aria-labelledby="dropdownMenuButton"><li class="edit_list"><a id="'
# 						+ str(Section_id)
# 						+ '" class="dropdown-item" href="#" onclick="edit_entitlement(this)">EDIT</a></li></ul></div></div>'
# 						+ str(Section_desc)
# 						+ "</div></label></div>"
# 					)
# 				else:					
# 					sec_bnr += (
# 						'<div class="dyn_main_head master_manufac glyphicon pointer  glyphicon-chevron-down" onclick="dyn_main_sec_collapse_arrow(this)" id="'+ str(Section_id)+ '" data-target="#sec_'
# 						+ str(Section_id)
# 						+ '" data-toggle="collapse"><label class="onlytext"><label class="onlytext"><div>'
# 						+ str(Section_desc)
# 						+ "</div></label></div>"
# 					)
				
# 				sec_str_boot += ('<div id="sec_'+str(Section_id)+ '" class="dyn_main_head master_manufac glyphicon pointer   glyphicon-chevron-down margtop10 " onclick="dyn_main_sec_collapse_arrow(this)" data-target="#sc_'+ str(Section_id)+ '" data-toggle="collapse" <label class="onlytext"><label class="onlytext"><div>'+ str(Section_desc).upper()+ '</div></label></div><div id="sc_'+str(Section_id)+ '" class="collapse in entitle_select_out"><table id="' + str(Section_id)+ '" class= "getentdata" data-filter-control="true" data-maintain-selected="true" data-locale = "en-US" data-escape="true" data-html="true"  data-show-header="true" > <thead><tr class="hovergrey">')
# 				for key, invs in enumerate(list(desc_list)):
# 					invs = str(invs).strip()
# 					qstring = attr_dict.get(str(invs)) or ""
# 					sec_str_boot += (
# 						'<th data-field="'
# 						+ invs
# 						+ '" data-title-tooltip="'
# 						+ str(qstring)
# 						+ '" >'
# 						+ str(qstring)
# 						+ "</th>"
# 					)
# 				sec_str_boot += '</tr></thead><tbody onclick="Table_Onclick_Scroll(this)" ></tbody></table>'
# 				sec_str_boot += ('<div id = "btn_ent" class="g4  except_sec removeHorLine iconhvr sec_edit_sty" style="display: none;"><button id="entcancel" class="btnconfig btnMainBanner sec_edit_sty_btn"  onclick="fabcostlocatecancel(this)" style="display: none;" class="btnconfig">CANCEL</button><button id="entsave" class="btnconfig btnMainBanner sec_edit_sty_btn"  onclick="fabcostlocatesave(this)" style="display: none;" class="btnconfig">SAVE</button></div>')

# 				add_style = ""
# 				attributes_disallowed_list = []
# 				attribute_Name_list = []
# 				if tabwise_product_attributes.get(product_tab_obj.TAB_PROD_ID):
# 					#Trace.Write("tabwise_product_attributes.get(product_tab_obj.TAB_PROD_ID)"+str(tabwise_product_attributes.get(product_tab_obj.TAB_PROD_ID)))
# 					for attribute in tabwise_product_attributes.get(product_tab_obj.TAB_PROD_ID):
# 						info_column = get_tooltip = ""
# 						new_value_dicta = {}
# 						attrName = attribute['attribute_name']
# 						attrLabel = attribute['attribute_label']
# 						attrSysId = attribute['attribute_system_id']
# 						attribute_code = attribute['attribute_code']
# 						#Trace.Write('attrSysId---looping0507--'+str(attrSysId))
# 						STDVALUES = Sql.GetFirst("""SELECT TOP 1 A.PA_ID, A.PAV_ID, A.STANDARD_ATTRIBUTE_VALUE_CD, A.STANDARD_ATTRIBUTE_PRICE, A.NON_STANDARD_VALUE, A.NON_STANDARD_DISPLAY_VALUE, 
# 						A.PRODUCT_ATT_IMAGE_OFF_ALT_TEXT, A.SORT_RANK, A.RELATED_PRODUCT_ID

# 						, COALESCE(P.PRODUCT_CATALOG_CODE, A.VALUE_CATALOG_CODE) VALUE_CATALOG_CODE

# 						, PA.STANDARD_ATTRIBUTE_CODE, PA.ATTRDESC,COALESCE(P.PRODUCT_NAME, V.STANDARD_ATTRIBUTE_DISPLAY_VAL) STANDARD_ATTRIBUTE_DISPLAY_VAL,V.SYSTEM_ID , V.STANDARD_ATTRIBUTE_VALUE, V.SYSTEM_ID AS VALUE_SYSTEM_ID, V.UNIT_ID AS VALUE_UNIT_ID, V.BILLING_PERIOD_ID AS VALUE_BILLING_PERIOD_ID
# 						, PA.USEALTERNATIVEPRICINGFORPRODUCTSINCONTAINER
# 						, COALESCE(P_ML.PRODUCT_NAME, P.PRODUCT_NAME, STDML.STANDARD_ATTRIBUTE_DISPLAY_VAL, V.STANDARD_ATTRIBUTE_DISPLAY_VAL) AS ML_NON_STANDARD_DISPLAY_VALUE
# 						FROM PRODUCT_ATTRIBUTES PA INNER JOIN ATTRIBUTES A ON PA.PA_ID=A.PA_ID 
# 						INNER JOIN STANDARD_ATTRIBUTE_VALUES V ON A.STANDARD_ATTRIBUTE_VALUE_CD = V.STANDARD_ATTRIBUTE_VALUE_CD  
# 						LEFT OUTER JOIN PRODUCTS P ON A.RELATED_PRODUCT_ID=P.PRODUCT_ID 
# 						LEFT OUTER JOIN PRODUCTS_ML P_ML ON P.PRODUCT_ID=P_ML.PRODUCT_ID AND P_ML.ML_ID=0
# 						LEFT JOIN  ATTRIBUTES_ML ML ON A.PAV_ID=ML.PAV_ID AND ML.ML_ID= 0
# 						LEFT JOIN STANDARD_ATTRIBUTE_VALUES_ML STDML ON A.STANDARD_ATTRIBUTE_VALUE_CD=STDML.STANDARD_ATTRIBUTE_VALUE_CD AND STDML.ML_ID=0 LEFT OUTER JOIN test_USD_L1 ON COALESCE(P.PRODUCT_CATALOG_CODE, A.VALUE_CATALOG_CODE) = test_USD_L1.PARTNUMBER AND ISNULL(A.PRICINGCODE, '')=ISNULL(test_USD_L1.PRICECODE, '') 
# 						WHERE PA.PRODUCT_ID ={productId} AND V.STANDARD_ATTRIBUTE_CODE  = {sys_id} ORDER BY A.SORT_RANK""".format(sys_id = attribute_code,productId = str(product_obj.PRD_ID)))
# 						#STDVALUES =  Sql.GetFirst("SELECT * from STANDARD_ATTRIBUTE_VALUES  where  STANDARD_ATTRIBUTE_CODE = {sys_id} ".format(sys_id = attribute_code)  )
# 						if STDVALUES:
# 							attrValue = STDVALUES.STANDARD_ATTRIBUTE_DISPLAY_VAL
# 							get_tooltip = STDVALUES.ATTRDESC
# 						else:
# 							attrValue = get_tooltip = ''
# 						Trace.Write('get_tooltip---'+str(get_tooltip))
# 						attribute_Name_list.append(attrSysId)
# 						DType = attribute['attribute_dtype']
# 						Trace.Write("attrSysId --3109---"+str(attrSysId) + " attrName_else_j "+str(attrName)+ " || "+str(attributedefaultvalue)+"attrSysId__else_j "+str(attributesdisallowedlst)+" attributesdisallowedlst_else_j")
# 						if attrSysId in attributesdisallowedlst:
# 							if attrSysId in attributedefaultvalue:
# 								add_style = "display:none;color:#1B78D2"
# 							else:
# 								add_style = ""
# 							attributes_disallowed_list.append(attrSysId)
# 						else:
# 							Trace.Write("attrValue_else_j 2860---attrName_else_j "+str(attrName))
# 							add_style = ""
# 						if attrSysId in attributedefaultvalue:
# 							Trace.Write("add_style----3077----- "+str(attrSysId))
# 							add_style = "color:#1B78D2"
# 						#Trace.Write(str(attrSysId)+'--attrLabel-2602-3076--attrValue--'+str(add_style))
# 						if attrSysId in attributeEditlst :
# 							disable_edit = 'disable_edit'
# 							edit_pencil_icon = '<a href="#" class="editclick"><i title="Double Click to Edit" class="fa fa-pencil"  aria-hidden="true"></i></a>'
							
# 						else:
# 							disable_edit = ''
# 							edit_pencil_icon = '<a href="#" class="editclick"><i title="Double Click to Edit" class="fa fa-lock"  aria-hidden="true"></i></a>'
# 						attrValueSysId = attributevalues.get(attrSysId)
# 						##info tooltip adding in entitlement grid starts..
# 						info_column = '''<a   data-placement="auto top" data-trigger="focus"  class="bgcccwth10"><i title="{value}" class="fa fa-info-circle fltlt"></i></a>'''.format(value= get_tooltip)
# 						##info tooltip adding in entitlement grid ends..
# 						disp_val = ""
# 						userselectedvalue = []
# 						#for val in GetXMLsecField:
						
# 						#userselectedvalue = [val.ENTITLEMENT_DESCRIPTION for val in GetXMLsecField if GetXMLsecField]
# 						sec_str_cf =sec_str_imt =  dataent = factcurreny = decimal_place = value1234 = sec_str_dt = sec_str_faccur = sec_str_faccur = costimpact = sec_str_primp = priceimp =  sec_str_ipp = ""
# 						#Trace.Write("inserted_value_list--"+str(inserted_value_list))
# 						if GetXMLsecField and attrSysId in inserted_value_list:
# 							# entitlement_display_value = [i.ENTITLEMENT_DISPLAY_VALUE for i in GetXMLsecField]
# 							# Trace.Write('entitlement_display_value'+str(entitlement_display_value))
# 							for val in GetXMLsecField:
# 								userselectedvalue.append(val.ENTITLEMENT_DESCRIPTION)
# 								#getnameentallowed.append(val.ENTITLEMENT_NAME)
# 								#Trace.Write("ENTITLEMENT_NAME_else_j "+str(val.ENTITLEMENT_NAME) +" || attrSysId "+str(attrSysId))
# 								# if  str(attrSysId) == val.ENTITLEMENT_NAME:
# 								#disp_val = str(val.ENTITLEMENT_DISPLAY_VALUE)
# 								#Trace.Write("dtype-----before if"+str(DType))
								
# 								if DType == "Drop Down" :
									
# 									#Trace.Write(str(attrName)+'---3152------'+str(val.ENTITLEMENT_NAME))
# 									#STDVALUES =  Sql.GetList("SELECT * from STANDARD_ATTRIBUTE_VALUES where  SYSTEM_ID like '%{sys_id}%' and STANDARD_ATTRIBUTE_CODE = '{attr_code}' ".format(sys_id = str(attrSysId), attr_code = attribute_code )  )
# 									STDVALUES = Sql.GetList("""SELECT TOP 20 A.PA_ID, A.PAV_ID, A.STANDARD_ATTRIBUTE_VALUE_CD, A.STANDARD_ATTRIBUTE_PRICE, A.NON_STANDARD_VALUE, A.NON_STANDARD_DISPLAY_VALUE, 
# 									A.PRODUCT_ATT_IMAGE_OFF_ALT_TEXT, A.SORT_RANK, A.RELATED_PRODUCT_ID

# 									, COALESCE(P.PRODUCT_CATALOG_CODE, A.VALUE_CATALOG_CODE) VALUE_CATALOG_CODE

# 									, PA.STANDARD_ATTRIBUTE_CODE, COALESCE(P.PRODUCT_NAME, V.STANDARD_ATTRIBUTE_DISPLAY_VAL) STANDARD_ATTRIBUTE_DISPLAY_VAL, V.SYSTEM_ID,V.STANDARD_ATTRIBUTE_VALUE, V.SYSTEM_ID AS VALUE_SYSTEM_ID, V.UNIT_ID AS VALUE_UNIT_ID, V.BILLING_PERIOD_ID AS VALUE_BILLING_PERIOD_ID
# 									, PA.USEALTERNATIVEPRICINGFORPRODUCTSINCONTAINER
# 									, COALESCE(P_ML.PRODUCT_NAME, P.PRODUCT_NAME, STDML.STANDARD_ATTRIBUTE_DISPLAY_VAL, V.STANDARD_ATTRIBUTE_DISPLAY_VAL) AS ML_NON_STANDARD_DISPLAY_VALUE
# 									FROM PRODUCT_ATTRIBUTES PA INNER JOIN ATTRIBUTES A ON PA.PA_ID=A.PA_ID 
# 									INNER JOIN STANDARD_ATTRIBUTE_VALUES V ON A.STANDARD_ATTRIBUTE_VALUE_CD = V.STANDARD_ATTRIBUTE_VALUE_CD  
# 									LEFT OUTER JOIN PRODUCTS P ON A.RELATED_PRODUCT_ID=P.PRODUCT_ID 
# 									LEFT OUTER JOIN PRODUCTS_ML P_ML ON P.PRODUCT_ID=P_ML.PRODUCT_ID AND P_ML.ML_ID=0
# 									LEFT JOIN  ATTRIBUTES_ML ML ON A.PAV_ID=ML.PAV_ID AND ML.ML_ID= 0
# 									LEFT JOIN STANDARD_ATTRIBUTE_VALUES_ML STDML ON A.STANDARD_ATTRIBUTE_VALUE_CD=STDML.STANDARD_ATTRIBUTE_VALUE_CD AND STDML.ML_ID=0 LEFT OUTER JOIN test_USD_L1 ON COALESCE(P.PRODUCT_CATALOG_CODE, A.VALUE_CATALOG_CODE) = test_USD_L1.PARTNUMBER AND ISNULL(A.PRICINGCODE, '')=ISNULL(test_USD_L1.PRICECODE, '') 
# 									WHERE PA.PRODUCT_ID ={productId} AND V.STANDARD_ATTRIBUTE_CODE  = {sys_id} ORDER BY A.SORT_RANK""".format(sys_id = attribute_code,productId = str(product_obj.PRD_ID)))
									
									
									
# 									if STDVALUES and val.ENTITLEMENT_NAME == str(attrSysId): 
# 										VAR1 = sec_str1 = ""
# 										selected_option = "Select"
# 										if str(val.ENTITLEMENT_DISPLAY_VALUE).strip() != "":
# 											default = ''
# 										else:
# 											default = 'selected'
# 										# if str(attrName) == "Fab Location":
# 										# 	if getquote_sales_val in get_il_sales_list:
# 										# 		VAR1 += '<option value="select" ' +str(default)+'> </option>'
# 										# 	else:
# 										# else:
# 										VAR1 += '<option value="select" ' +str(default)+' style= "display:none;"> </option>'
# 										for value in STDVALUES:
# 											if value.SYSTEM_ID in dropdowndisallowlist:
# 												#Trace.Write('3179-----'+str(value.SYSTEM_ID)+'-'+str(attribute_code))
# 												disallow_style = "style = 'display:none'"
# 											else:	
# 												disallow_style = ""
# 											try:
												
# 												if str(val.ENTITLEMENT_DISPLAY_VALUE).strip() == str(value.STANDARD_ATTRIBUTE_DISPLAY_VAL).strip():
# 													#Trace.Write('drpppppp---3031-------'+str(val.ENTITLEMENT_DISPLAY_VALUE)+str(value.STANDARD_ATTRIBUTE_DISPLAY_VAL))
													
# 													selected_option = str(val.ENTITLEMENT_DISPLAY_VALUE)
# 													VAR1 += (
# 														'<option  id="'+str(value.SYSTEM_ID)+'" value = "'
# 														+ str(val.ENTITLEMENT_DISPLAY_VALUE)
# 														+ '" selected>'
# 														+ str(val.ENTITLEMENT_DISPLAY_VALUE)
# 														+ "</option>"
# 													)
# 												else:
# 													#Trace.Write('drpppppp---3031----3342-----'+str(val.ENTITLEMENT_DISPLAY_VALUE)+str(value.STANDARD_ATTRIBUTE_DISPLAY_VAL))
# 													VAR1 += (
# 														'<option '
# 														+ str(disallow_style)
# 														+ ' id="'+str(value.SYSTEM_ID)+'" value = "'
# 														+ str(value.STANDARD_ATTRIBUTE_DISPLAY_VAL)
# 														+ '">'
# 														+ str(value.STANDARD_ATTRIBUTE_DISPLAY_VAL)
# 														+ "</option>"
# 													)
# 											except:
# 												Trace.Write('except dropdown {} {}'.format(value.SYSTEM_ID, value.STANDARD_ATTRIBUTE_DISPLAY_VAL))
# 												VAR1 = '<option value="select" ' +str(default)+'  style="display;none;"> </option>'
# 												if val.ENTITLEMENT_DISPLAY_VALUE == value.STANDARD_ATTRIBUTE_DISPLAY_VAL:
# 													selected_option = val.ENTITLEMENT_DISPLAY_VALUE
# 													VAR1 += (
# 														'<option  id="'+str(value.SYSTEM_ID)+'" value = "{value}" selected>{value}</option>'.format(value= value.STANDARD_ATTRIBUTE_DISPLAY_VAL)
# 													)
# 												else:
# 													VAR1 += (
# 														'<option '
# 														+ str(disallow_style)
# 														+ ' id="'+str(value.SYSTEM_ID)+'" value = "{value}">{value}</option>'.format(value= value.STANDARD_ATTRIBUTE_DISPLAY_VAL)
# 													)

# 										try:
# 											if str(attrName) == "Fab Location":
# 												disable_edit =''
# 												sec_str1 += (
# 												'<select class="form-control remove_yellow '+str(disable_edit)+'" style ="'+str(add_style)+'" id = "'
# 												+ str(attrSysId)
# 												+ '" type="text"  data-content ="'
# 												+ str(attrSysId)
# 												+ '" class="form-control" onchange="editent_bt(this)" title="'+str(selected_option)+'" disabled>'
# 												+ str(VAR1)
# 												+ "</select>"
# 												)
# 											else:
# 												sec_str1 += (
# 												'<select class="form-control remove_yellow '+str(disable_edit)+'" style ="'+str(add_style)+'" id = "'
# 												+ str(attrSysId)
# 												+ '" type="text"  data-content ="'
# 												+ str(attrSysId)
# 												+ '" class="form-control" onchange="editent_bt(this)" title="'+str(selected_option)+'" disabled>'
# 												+ str(VAR1)
# 												+ "</select>"
# 												)

# 										except:
# 											sec_str1 += (
# 											'<select class="form-control remove_yellow '+str(disable_edit)+'" style ="'+str(add_style)+'" id = "'
# 											+ str(attrSysId)
# 											+ '" type="text"  data-content ="'
# 											+ str(attrSysId)
# 											+ '" class="form-control" onchange="editent_bt(this)" title="'+str(selected_option)+'" disabled>{}</select>'.format(VAR1)
# 											)
										
# 										if val.ENTITLEMENT_NAME == 'AGS_SFM_DEI_PAC' and "Included" in val.ENTITLEMENT_DISPLAY_VALUE:
# 											sec_str_imt += str(val.ENTITLEMENT_COST_IMPACT)+" "+str(val.PRICE_METHOD)
# 											sec_str_faccur += str(val.PRICE_METHOD)
# 										elif (val.ENTITLEMENT_NAME == 'AGS_RFM_INS_T0' or val.ENTITLEMENT_NAME == 'AGS_RFM_INS_T1') and "Included" in val.ENTITLEMENT_DISPLAY_VALUE:
# 											sec_str_imt += str(val.ENTITLEMENT_COST_IMPACT)+" "+str(val.PRICE_METHOD)
# 											sec_str_faccur += str(val.PRICE_METHOD)
# 										elif (val.ENTITLEMENT_NAME == 'AGS_RFM_INS_T2' or val.ENTITLEMENT_NAME == 'AGS_RFM_INS_T3') and "Included" in val.ENTITLEMENT_DISPLAY_VALUE:
# 											sec_str_imt += str(val.ENTITLEMENT_COST_IMPACT)+" "+str(val.PRICE_METHOD)
# 											sec_str_faccur += str(val.PRICE_METHOD)
# 										else:
# 											sec_str_imt += ""
										
										
# 										""" except Exception, e:
# 											Trace.Write(str(e)+'error1111')
# 											sec_str_imt += str(val.ENTITLEMENT_COST_IMPACT) """
# 										#Trace.Write("CHKNG_STYLE_J "+str(add_style)+" attrSysId "+str(attrSysId))
									

# 								elif DType == "Check Box" :
# 									STDVALUES = Sql.GetList("""SELECT TOP 20 A.PA_ID, A.PAV_ID, A.STANDARD_ATTRIBUTE_VALUE_CD, A.STANDARD_ATTRIBUTE_PRICE, A.NON_STANDARD_VALUE, A.NON_STANDARD_DISPLAY_VALUE, 
# 									A.PRODUCT_ATT_IMAGE_OFF_ALT_TEXT, A.SORT_RANK, A.RELATED_PRODUCT_ID

# 									, COALESCE(P.PRODUCT_CATALOG_CODE, A.VALUE_CATALOG_CODE) VALUE_CATALOG_CODE

# 									, PA.STANDARD_ATTRIBUTE_CODE, COALESCE(P.PRODUCT_NAME, V.STANDARD_ATTRIBUTE_DISPLAY_VAL) STANDARD_ATTRIBUTE_DISPLAY_VAL,V.SYSTEM_ID, V.STANDARD_ATTRIBUTE_VALUE, V.SYSTEM_ID AS VALUE_SYSTEM_ID, V.UNIT_ID AS VALUE_UNIT_ID, V.BILLING_PERIOD_ID AS VALUE_BILLING_PERIOD_ID
# 									, PA.USEALTERNATIVEPRICINGFORPRODUCTSINCONTAINER
# 									, COALESCE(P_ML.PRODUCT_NAME, P.PRODUCT_NAME, STDML.STANDARD_ATTRIBUTE_DISPLAY_VAL, V.STANDARD_ATTRIBUTE_DISPLAY_VAL) AS ML_NON_STANDARD_DISPLAY_VALUE
# 									FROM PRODUCT_ATTRIBUTES PA INNER JOIN ATTRIBUTES A ON PA.PA_ID=A.PA_ID 
# 									INNER JOIN STANDARD_ATTRIBUTE_VALUES V ON A.STANDARD_ATTRIBUTE_VALUE_CD = V.STANDARD_ATTRIBUTE_VALUE_CD  
# 									LEFT OUTER JOIN PRODUCTS P ON A.RELATED_PRODUCT_ID=P.PRODUCT_ID 
# 									LEFT OUTER JOIN PRODUCTS_ML P_ML ON P.PRODUCT_ID=P_ML.PRODUCT_ID AND P_ML.ML_ID=0
# 									LEFT JOIN  ATTRIBUTES_ML ML ON A.PAV_ID=ML.PAV_ID AND ML.ML_ID= 0
# 									LEFT JOIN STANDARD_ATTRIBUTE_VALUES_ML STDML ON A.STANDARD_ATTRIBUTE_VALUE_CD=STDML.STANDARD_ATTRIBUTE_VALUE_CD AND STDML.ML_ID=0 LEFT OUTER JOIN test_USD_L1 ON COALESCE(P.PRODUCT_CATALOG_CODE, A.VALUE_CATALOG_CODE) = test_USD_L1.PARTNUMBER AND ISNULL(A.PRICINGCODE, '')=ISNULL(test_USD_L1.PRICECODE, '') 
# 									WHERE PA.PRODUCT_ID ={productId} AND V.STANDARD_ATTRIBUTE_CODE  = {sys_id} ORDER BY A.SORT_RANK""".format(sys_id = attribute_code,productId = str(product_obj.PRD_ID)))
# 									#STDVALUES =  Sql.GetList("SELECT * from STANDARD_ATTRIBUTE_VALUES where STANDARD_ATTRIBUTE_CODE = '{attr_code}' ".format(attr_code = attribute_code )  )
# 									if STDVALUES and val.ENTITLEMENT_NAME == str(attrSysId):
# 										try:
# 											display_value_arr = eval(val.ENTITLEMENT_DISPLAY_VALUE)
# 										except Exception as e:
# 											Trace.Write('except'+str(e))
# 											try:
# 												display_value_code = str(tuple(eval(val.ENTITLEMENT_VALUE_CODE))).replace(',)',')')
# 												#Trace.Write('display_value_code'+str(display_value_code))
# 												display_value_query = Sql.GetList("SELECT * from STANDARD_ATTRIBUTE_VALUES where STANDARD_ATTRIBUTE_CODE = '{attr_code}' and STANDARD_ATTRIBUTE_VALUE in {code} ".format(attr_code = attribute_code,code = display_value_code )  )
# 												display_value_arr = [i.STANDARD_ATTRIBUTE_DISPLAY_VAL for i in display_value_query]
# 											except Exception as e:
# 												Trace.Write('except1'+str(e))
# 												display_value_arr = str(val.ENTITLEMENT_DISPLAY_VALUE)
										
# 										multi_select_attr_list[attrSysId] = display_value_arr
# 										Trace.Write("multi_select_attr_list"+str(multi_select_attr_list)+'---'+str(display_value_arr))
# 										VAR1 = sec_str1 = selected_option = ""
# 										for value in STDVALUES:
# 											if value.SYSTEM_ID in dropdowndisallowlist:
# 												disallow_style = "style = 'display:none'"
# 											else:	
# 												disallow_style = ""
# 											#Trace.Write("checkkkkkk---"+str(val.ENTITLEMENT_VALUE_CODE)+"----"+str(value.STANDARD_ATTRIBUTE_VALUE)+str(attrSysId))
# 											try:
# 												if not (type(val.ENTITLEMENT_VALUE_CODE) is 'int' or type(val.ENTITLEMENT_VALUE_CODE) is 'float'):
# 													value_code = eval(val.ENTITLEMENT_VALUE_CODE)
# 												else:
# 													value_code = val.ENTITLEMENT_VALUE_CODE	
# 											except:
# 												value_code = val.ENTITLEMENT_VALUE_CODE
# 											#Trace.Write('value_code'+str(value_code))
# 											try:
# 												if value_code and str(value.STANDARD_ATTRIBUTE_VALUE).strip() in value_code:
# 													#Trace.Write('2620-----ch---'+str(value.STANDARD_ATTRIBUTE_VALUE))
# 													# getnameentallowed.append(value.STANDARD_ATTRIBUTE_DISPLAY_VAL)
# 													# Trace.Write("getnameentallowed"+str(getnameentallowed))
# 													selected_option = str(value.STANDARD_ATTRIBUTE_DISPLAY_VAL)
# 													VAR1 += (
# 															'<option  id="'+str(value.SYSTEM_ID)+'" value = "'
# 															+ str(value.STANDARD_ATTRIBUTE_DISPLAY_VAL)
# 															+ '" selected>'
# 															+ str(value.STANDARD_ATTRIBUTE_DISPLAY_VAL)
# 															+ "</option>"
# 													)
# 												elif str(value.STANDARD_ATTRIBUTE_VALUE).strip() not in value_code :
# 													#Trace.Write(str(val.ENTITLEMENT_DISPLAY_VALUE)+'26211111-----'+str(value.STANDARD_ATTRIBUTE_VALUE))
# 													VAR1 += (
# 														'<option '+str(disallow_style)+'  id="'+str(value.SYSTEM_ID)+'" value = "'
# 														+ str(value.STANDARD_ATTRIBUTE_DISPLAY_VAL)
# 														+ '">'
# 														+ str(value.STANDARD_ATTRIBUTE_DISPLAY_VAL)
# 														+ "</option>"
# 													)
# 											except:
# 												if value_code and str(value.STANDARD_ATTRIBUTE_VALUE).strip() == value_code:
# 													#Trace.Write('2620-----ch---'+str(value.STANDARD_ATTRIBUTE_VALUE))
# 													# getnameentallowed.append(value.STANDARD_ATTRIBUTE_DISPLAY_VAL)
# 													# Trace.Write("getnameentallowed"+str(getnameentallowed))
# 													selected_option = str(value.STANDARD_ATTRIBUTE_DISPLAY_VAL)
# 													VAR1 += (
# 															'<option  id="'+str(value.SYSTEM_ID)+'" value = "'
# 															+ str(value.STANDARD_ATTRIBUTE_DISPLAY_VAL)
# 															+ '" selected>'
# 															+ str(value.STANDARD_ATTRIBUTE_DISPLAY_VAL)
# 															+ "</option>"
# 													)
# 												elif str(value.STANDARD_ATTRIBUTE_VALUE).strip() != value_code :
# 													#Trace.Write(str(val.ENTITLEMENT_DISPLAY_VALUE)+'26211111-----'+str(value.STANDARD_ATTRIBUTE_VALUE))
# 													VAR1 += (
# 														'<option '+str(disallow_style)+'  id="'+str(value.SYSTEM_ID)+'" value = "'
# 														+ str(value.STANDARD_ATTRIBUTE_DISPLAY_VAL)
# 														+ '">'
# 														+ str(value.STANDARD_ATTRIBUTE_DISPLAY_VAL)
# 														+ "</option>"
# 													)	
# 											#Trace.Write('VAR1'+str(attrSysId)+str(value.STANDARD_ATTRIBUTE_VALUE))
# 										#Trace.Write("CHKNG_STYLE_J "+str(add_style)+" attrSysId "+str(attrSysId))
# 										#Trace.Write("CHKNG_STYLE_J "+str(VAR1)+" attrSysId "+str(attrSysId))
# 										sec_str1 += (
# 											'<select class="form-control remove_yellow div_multi_checkbox '+str(disable_edit)+'"  style ="'+str(add_style)+'" id = "'
# 											+ str(attrSysId)
# 											+ '" type="text"  data-content ="'
# 											+ str(attrSysId)
# 											+ '" class="form-control" onchange="editent_bt(this)" title="'+str(selected_option)+'" disabled>'
# 											+ str(VAR1)
# 											+ "</select>"
# 										)
# 									#Trace.Write('sec_str1'+str(sec_str1))
								
								
# 								elif DType == "Free Input, no Matching" :
# 									Trace.Write('val.ENTITLEMENT_NAME--'+str(val.ENTITLEMENT_NAME))
# 									if val.ENTITLEMENT_NAME == str(attrSysId):
# 										sec_str1 = ""
# 										sec_str_imt = ""
# 										sec_str_primp =""
# 										sec_str_cf =""
# 										sec_str_faccur = ""
# 										attr_value = val.ENTITLEMENT_DISPLAY_VALUE
# 										Trace.Write("DType free1---"+str(attr_value)+str(attrSysId)+str(add_style))
# 										if str(attrSysId) == "AGS_REL_STDATE":
# 											datepicker = "onclick_datepicker_locdate('" + attrSysId + "')"
# 											datepicker_onchange = "onchangedatepicker('" + attrSysId + "')"

# 											sec_str1 += (
# 												'<input class="form-control no_border_bg  datePickerField wth157fltltbrdbt '+str(disable_edit)+'" id = "'
# 												+ str(attrSysId)
# 												+ '" type="text"  style ="'+str(add_style)+'"  onchange="'+ str(datepicker)+ '"  data-content ="'
# 												+ str(attr_value)
# 												+ '" value = "'+str(attr_value)+'" title="'+str(attr_value)+'"  disabled>'									
# 												+ "</input> "
# 											)
# 											# sec_str1 += (
# 											# 	'<input class="form-control no_border_bg datePickerField wth157fltltbrdbt '+str(disable_edit)+'" id = "'
# 											# 	+ str(attrSysId)
# 											# 	+ '" type="text"   style ="'+str(add_style)+'"  onclick="'+ str(datepicker)+ '" data-content ="'
# 											# 	+ str(attr_value) 
# 											# 	+ '" value = "'+str(attr_value)+'" title="'+str(attr_value)+'" onchange="'+ datepicker_onchange+ +'" disabled>'									
# 											# 	+ "</input> "
# 											# )
# 										else:
# 											if attr_value == "DefaultValue":
# 												attr_value = ''
# 											sec_str1 += (
# 												'<input class="form-control no_border_bg '+str(disable_edit)+'" id = "'
# 												+ str(attrSysId)
# 												+ '" type="text"  style ="'+str(add_style)+'"  data-content ="'
# 												+ str(attr_value)
# 												+ '" value = "'+str(attr_value)+'" title="'+str(attr_value)+'" onchange="editent_bt(this)" disabled>'									
# 												+ "</input> "
# 											)
# 										#cost_impact  = val.ENTITLEMENT_COST_IMPACT
# 										try:
# 											#Trace.Write("@@3087"+str(attrSysId))
# 											if val.ENTITLEMENT_COST_IMPACT:
# 												#Trace.Write("@@3089"+str(val.ENTITLEMENT_COST_IMPACT)+str(val.PRICE_METHOD)+str(attrSysId))
# 												#sec_str_imt += str("{:,.2f}".format(float(val.ENTITLEMENT_COST_IMPACT)))
# 												sec_str_imt += str("{:,.2f}".format(float(val.ENTITLEMENT_COST_IMPACT))) + " "+val.PRICE_METHOD
												
# 											# else:
# 											# 	#Trace.Write("@@3093")
# 											# 	#sec_str_imt += str("{:,.2f}".format(float(val.ENTITLEMENT_COST_IMPACT)))
# 											# 	sec_str_imt += 
												
# 										except Exception as e:
# 											Trace.Write(str(e)+'error1111'+str(attrSysId))
# 											sec_str_imt += str(val.ENTITLEMENT_COST_IMPACT)
# 										#price_impact = val.ENTITLEMENT_PRICE_IMPACT
# 										try:
# 											if val.ENTITLEMENT_PRICE_IMPACT:
# 												#sec_str_primp += str("{:,.2f}".format(float(val.ENTITLEMENT_PRICE_IMPACT)))
# 												sec_str_primp += str("{:,.2f}".format(float(val.ENTITLEMENT_PRICE_IMPACT))) + " "+val.PRICE_METHOD
# 											# else:
# 											# 	Trace.Write("else price")
# 											# 	#sec_str_primp += str("{:,.2f}".format(float(val.ENTITLEMENT_PRICE_IMPACT)))
# 											# 	sec_str_primp += ""
# 										except Exception as e:
# 											sec_str_primp += str(val.ENTITLEMENT_PRICE_IMPACT)
# 											Trace.Write(str(e)+'error2222')
											
# 										#calc_factor = val.CALCULATION_FACTOR
# 										sec_str_cf +=str(val.CALCULATION_FACTOR)
# 										Trace.Write('sec_str_cf chk ## '+str(sec_str_cf))
# 										##FACTOR CURRENCY
# 										sec_str_faccur += str(val.PRICE_METHOD)
									
# 								if (str(val.ENTITLEMENT_DESCRIPTION) == "Addl Perf Guarantee 2" and str(val.ENTITLEMENT_VALUE_CODE).upper()== "MANUAL_INPUT"):
									
# 									imgstr = ('<img title=Acquired src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/clock_exe.svg>')
# 								else:
# 									imgstr  = ""
# 								new_value_dicta["APPROVAL"] = imgstr	
# 								new_value_dicta["ENTITLEMENT DESCRIPTION"] = str("<abbr title='"+str(attrName)+"'>"+str(attrName)+"</abbr>")
								
# 								if DType in( "Drop Down", "Check Box", "Free Input, no Matching"):
# 									new_value_dicta["ENTITLEMENT VALUE"] = str(info_column)+ sec_str1 									
# 								else:
# 									new_value_dicta["ENTITLEMENT VALUE"] = str(info_column) + str(sec_str_ipp)
# 									Trace.Write("@3323-----"+str(attrSysId))
# 								new_value_dicta["ENTITLEMENT COST IMPACT"]= str("<abbr title='"+str(sec_str_imt)+"'>"+str(sec_str_imt)+"</abbr>")
# 								new_value_dicta["ENTITLEMENT PRICE IMPACT"]= str("<abbr class = 'wid90_per' title='"+str(sec_str_primp)+"'>"+str(sec_str_primp)+"</abbr>")+str(edit_pencil_icon)
# 								new_value_dicta["CALCULATION FACTOR"] = str("<abbr title='"+str(sec_str_cf)+"'>"+str(sec_str_cf)+"</abbr>")						
# 						else:
# 							if attrSysId not in attributesdisallowedlst and attrSysId:
# 								attributesdisallowedlst.append(attrSysId)
# 							add_style = "display:none"							
# 							if DType == "Drop Down":
# 								Trace.Write(str(attrName)+'attrSysId--2324--drop down---3491-'+str(attrSysId))
# 								#STDVALUES =  Sql.GetList("SELECT * from STANDARD_ATTRIBUTE_VALUES where  SYSTEM_ID like '%{sys_id}%' and STANDARD_ATTRIBUTE_CODE = '{attr_code}' ".format(sys_id = str(attrSysId), attr_code = attribute_code )  )
# 								STDVALUES = Sql.GetList("""SELECT TOP 20 A.PA_ID, A.PAV_ID, A.STANDARD_ATTRIBUTE_VALUE_CD, A.STANDARD_ATTRIBUTE_PRICE, A.NON_STANDARD_VALUE, A.NON_STANDARD_DISPLAY_VALUE, 
# 									A.PRODUCT_ATT_IMAGE_OFF_ALT_TEXT, A.SORT_RANK, A.RELATED_PRODUCT_ID

# 									, COALESCE(P.PRODUCT_CATALOG_CODE, A.VALUE_CATALOG_CODE) VALUE_CATALOG_CODE

# 									, PA.STANDARD_ATTRIBUTE_CODE, COALESCE(P.PRODUCT_NAME, V.STANDARD_ATTRIBUTE_DISPLAY_VAL) STANDARD_ATTRIBUTE_DISPLAY_VAL, V.SYSTEM_ID,V.STANDARD_ATTRIBUTE_VALUE, V.SYSTEM_ID AS VALUE_SYSTEM_ID, V.UNIT_ID AS VALUE_UNIT_ID, V.BILLING_PERIOD_ID AS VALUE_BILLING_PERIOD_ID
# 									, PA.USEALTERNATIVEPRICINGFORPRODUCTSINCONTAINER
# 									, COALESCE(P_ML.PRODUCT_NAME, P.PRODUCT_NAME, STDML.STANDARD_ATTRIBUTE_DISPLAY_VAL, V.SYSTEM_ID,V.STANDARD_ATTRIBUTE_DISPLAY_VAL) AS ML_NON_STANDARD_DISPLAY_VALUE
# 									FROM PRODUCT_ATTRIBUTES PA INNER JOIN ATTRIBUTES A ON PA.PA_ID=A.PA_ID 
# 									INNER JOIN STANDARD_ATTRIBUTE_VALUES V ON A.STANDARD_ATTRIBUTE_VALUE_CD = V.STANDARD_ATTRIBUTE_VALUE_CD  
# 									LEFT OUTER JOIN PRODUCTS P ON A.RELATED_PRODUCT_ID=P.PRODUCT_ID 
# 									LEFT OUTER JOIN PRODUCTS_ML P_ML ON P.PRODUCT_ID=P_ML.PRODUCT_ID AND P_ML.ML_ID=0
# 									LEFT JOIN  ATTRIBUTES_ML ML ON A.PAV_ID=ML.PAV_ID AND ML.ML_ID= 0
# 									LEFT JOIN STANDARD_ATTRIBUTE_VALUES_ML STDML ON A.STANDARD_ATTRIBUTE_VALUE_CD=STDML.STANDARD_ATTRIBUTE_VALUE_CD AND STDML.ML_ID=0 LEFT OUTER JOIN test_USD_L1 ON COALESCE(P.PRODUCT_CATALOG_CODE, A.VALUE_CATALOG_CODE) = test_USD_L1.PARTNUMBER AND ISNULL(A.PRICINGCODE, '')=ISNULL(test_USD_L1.PRICECODE, '') 
# 									WHERE PA.PRODUCT_ID ={productId} AND V.STANDARD_ATTRIBUTE_CODE  = {sys_id} ORDER BY A.SORT_RANK""".format(sys_id = attribute_code,productId = str(product_obj.PRD_ID)))
# 								VAR1 = sec_str1 =  ""
# 								selected_option = " "
# 								if STDVALUES:
# 									if attributevalues.get(attrSysId) is not None:
# 										#select_option = 'selected'
# 										select_option = ''
# 										default = ''
# 									else:
# 										select_option = ""
# 										default = 'selected'
# 										selected_option = ' title="Select" '
# 									VAR1 += '<option value="select" ' +str(default)+' style= "display:none;"> </option>'
# 									for value in STDVALUES:
# 										if value.SYSTEM_ID in dropdowndisallowlist:
# 											disallow_style = "style = 'display:none'"
# 										else:	
# 											disallow_style = ""
# 										if str(selected_option)=='selected':
# 											selected_option = ' title="'+str(value.STANDARD_ATTRIBUTE_DISPLAY_VAL)+'" '
# 										try:
# 											#Trace.Write('attrSysId-try---3491-'+str(attrSysId))
# 											VAR1 += (
# 												'<option '+str(disallow_style)+' id="'+str(value.SYSTEM_ID)+'"  value = "'
# 												+ str(value.STANDARD_ATTRIBUTE_DISPLAY_VAL) 
# 												+ '"'+str(select_option)+'>'
# 												+ str(value.STANDARD_ATTRIBUTE_DISPLAY_VAL)
# 												+ "</option>"
# 											)
									
# 										except:
# 											#Trace.Write('attrSysId-try-catch--3491-'+str(attrSysId))
# 											VAR1 += (
# 												'<option '
# 												+ str(disallow_style)
# 												+ ' id="'+str(value.SYSTEM_ID)+'" value = "{value}" {select}>{value}</option>'.format(value= value.STANDARD_ATTRIBUTE_DISPLAY_VAL,select = select_option)
# 											)
# 									try:
# 										sec_str1 += (
# 												'<select class="form-control remove_yellow '+str(disable_edit)+'" style ="'+str(add_style)+'" id = "'
# 												+ str(attrSysId)
# 												+ '" type="text"  data-content ="'
# 												+ str(attrSysId)
# 												+ '" onchange="editent_bt(this)" '+str(selected_option)+'  >'
# 												+ str(VAR1)
# 												+ "</select>"
# 											)
# 									except:		
# 										sec_str1 += (
# 											'<select class="form-control remove_yellow '+str(disable_edit)+'" style ="'+str(add_style)+'" id = "'
# 											+ str(attrSysId)
# 											+ '" type="text"  data-content ="'
# 											+ str(attrSysId)
# 											+ '" onchange="editent_bt(this)" '+str(selected_option)+'  >{} </select>'.format(VAR1)
# 										)

								
# 									#sec_str += "<option id='"+str(attrcode)+"' >" + str(optionvalue) + "</option>"
# 								#sec_str += "</select></td>"
						
# 							elif DType == "Check Box":
# 								#Trace.Write('attrSysId--2324---'+str(attrSysId))
# 								#STDVALUES =  Sql.GetList("SELECT * from STANDARD_ATTRIBUTE_VALUES where  SYSTEM_ID like '%{sys_id}%' and STANDARD_ATTRIBUTE_CODE = '{attr_code}' ".format(sys_id = str(attrSysId), attr_code = attribute_code )  )
# 								STDVALUES = Sql.GetList("""SELECT TOP 20 A.PA_ID, A.PAV_ID, A.STANDARD_ATTRIBUTE_VALUE_CD, A.STANDARD_ATTRIBUTE_PRICE, A.NON_STANDARD_VALUE, A.NON_STANDARD_DISPLAY_VALUE, 
# 								A.PRODUCT_ATT_IMAGE_OFF_ALT_TEXT, A.SORT_RANK, A.RELATED_PRODUCT_ID

# 								, COALESCE(P.PRODUCT_CATALOG_CODE, A.VALUE_CATALOG_CODE) VALUE_CATALOG_CODE

# 								, PA.STANDARD_ATTRIBUTE_CODE, COALESCE(P.PRODUCT_NAME, V.STANDARD_ATTRIBUTE_DISPLAY_VAL) STANDARD_ATTRIBUTE_DISPLAY_VAL, V.SYSTEM_ID,V.STANDARD_ATTRIBUTE_VALUE, V.SYSTEM_ID AS VALUE_SYSTEM_ID, V.UNIT_ID AS VALUE_UNIT_ID, V.BILLING_PERIOD_ID AS VALUE_BILLING_PERIOD_ID
# 								, PA.USEALTERNATIVEPRICINGFORPRODUCTSINCONTAINER
# 								, COALESCE(P_ML.PRODUCT_NAME, P.PRODUCT_NAME, STDML.STANDARD_ATTRIBUTE_DISPLAY_VAL, V.STANDARD_ATTRIBUTE_DISPLAY_VAL) AS ML_NON_STANDARD_DISPLAY_VALUE
# 								FROM PRODUCT_ATTRIBUTES PA INNER JOIN ATTRIBUTES A ON PA.PA_ID=A.PA_ID 
# 								INNER JOIN STANDARD_ATTRIBUTE_VALUES V ON A.STANDARD_ATTRIBUTE_VALUE_CD = V.STANDARD_ATTRIBUTE_VALUE_CD  
# 								LEFT OUTER JOIN PRODUCTS P ON A.RELATED_PRODUCT_ID=P.PRODUCT_ID 
# 								LEFT OUTER JOIN PRODUCTS_ML P_ML ON P.PRODUCT_ID=P_ML.PRODUCT_ID AND P_ML.ML_ID=0
# 								LEFT JOIN  ATTRIBUTES_ML ML ON A.PAV_ID=ML.PAV_ID AND ML.ML_ID= 0
# 								LEFT JOIN STANDARD_ATTRIBUTE_VALUES_ML STDML ON A.STANDARD_ATTRIBUTE_VALUE_CD=STDML.STANDARD_ATTRIBUTE_VALUE_CD AND STDML.ML_ID=0 LEFT OUTER JOIN test_USD_L1 ON COALESCE(P.PRODUCT_CATALOG_CODE, A.VALUE_CATALOG_CODE) = test_USD_L1.PARTNUMBER AND ISNULL(A.PRICINGCODE, '')=ISNULL(test_USD_L1.PRICECODE, '') 
# 								WHERE PA.PRODUCT_ID ={productId} AND V.STANDARD_ATTRIBUTE_CODE  = {sys_id} ORDER BY A.SORT_RANK""".format(sys_id = attribute_code,productId = str(product_obj.PRD_ID)))
# 								VAR1 = sec_str1 = ""
# 								if STDVALUES:
# 									for value in STDVALUES:
										
# 										VAR1 += (
# 											'<option  value = "'
# 											+ str(value.STANDARD_ATTRIBUTE_DISPLAY_VAL)
# 											+ '">'
# 											+ str(value.STANDARD_ATTRIBUTE_DISPLAY_VAL)
# 											+ "</option>"
# 										)
# 								sec_str1 += (
# 									'<select class="form-control remove_yellow div_multi_checkbox '+str(disable_edit)+'" style ="'+str(add_style)+'" id = "'
# 									+ str(attrSysId)
# 									+ '" type="text"  data-content ="'
# 									+ str(attrSysId)
# 									+ '" onchange="editent_bt(this)" >'
# 									+ str(VAR1)
# 									+ "</select>"
# 								)
									
# 							elif DType == "Free Input, no Matching":
# 								STDVALUES =  Sql.GetFirst("SELECT STANDARD_ATTRIBUTE_VALUE from STANDARD_ATTRIBUTE_VALUES  where  SYSTEM_ID like '%{sys_id}%' ".format(sys_id = str(attrSysId))  )							
# 								sec_str1 = ""
# 								#Trace.Write(str(attrSysId)+'--attrValue---3594---'+str(attrValue))
# 								if attrValue == "DefaultValue":
# 									attrValue = ''
# 								sec_str1 += (
# 									'<input class="form-control remove_yellow '+str(disable_edit)+'" style ="'+str(add_style)+'"  id = "'
# 									+ str(attrSysId)
# 									+ '" type="text"  data-content ="'
# 									+ str(attrSysId)
# 									+ '" value = "'+str(attrValue)+'" title="'+str(attrValue)+'" onchange="editent_bt(this)" >'
# 									+ "</input>"
# 								)
							
# 							new_value_dicta["APPROVAL"] = ""	
# 							new_value_dicta["ENTITLEMENT DESCRIPTION"] = str(attrName)
# 							if DType == "Drop Down" or DType == "Check Box" or DType =="Free Input, no Matching":
# 								new_value_dicta["ENTITLEMENT VALUE"] = str(info_column)+ sec_str1
# 								#Trace.Write("attrSysIdDType---3623-- "+str(attrSysId)+str(DType))
# 							else:
# 								new_value_dicta["ENTITLEMENT VALUE"] = str(info_column)+ attrValue
# 							#new_value_dicta["FACTOR CURRENCY"] = ""
# 							new_value_dicta["ENTITLEMENT COST IMPACT"]= ""
# 							new_value_dicta["ENTITLEMENT PRICE IMPACT"]= ""
# 							#new_value_dicta["DATA TYPE"] = ""
# 							new_value_dicta["CALCULATION FACTOR"] = ""	
# 						Trace.Write('attributesdisallowedlst'+str(attributesdisallowedlst))
# 						totaldisallowlist = [item for item in attributesdisallowedlst]
						
# 						if new_value_dicta:
# 							date_boot_field.append(new_value_dicta)

# 					tablistdict[Section_id] = date_boot_field					
# 					if len(tablistdict) > 0:
# 						tablistnew.append(tablistdict)
# 				Product.SetGlobal('ent_data_List',str(tablistnew))					
# 				table_ids = '#'+Section_id
# 				getdivid = '#sc_'+Section_id+' .sec_edit_sty'
# 				getdividbtn = '#sc_'+Section_id+' #btn_ent .sec_edit_sty_btn'
				
# 				sec_str_boot += ('</div>')
# 				##section hide starts..
# 				if len(attribute_Name_list) == len(attributes_disallowed_list):
# 					section_not_list.append('sec_'+Section_id)
					
# 				##section hide ends...
# 				#getprevdicts +=   ("try{var dict_new = {};$('"+str(table_ids)+" tbody tr td select').each(function () {dict_new[$(this).find('td:nth-child(3) select').attr('id')] = $(this).children(':selected').val();});$('"+str(table_ids)+" tbody tr td input').each(function () {if($(this).attr('id') != 'T0_T1_LABOR_calc'){dict_new[$(this).find('td:nth-child(3) input').attr('id')] =  $(this).find('td:nth-child(3) input').val();}});console.log('dict_new-2796--',dict_new);localStorage.setItem('prventdict', JSON.stringify(dict_new))}catch{console.log('')}")
# 				#getprevdicts +=   ("try{var dict_new = {};$('"+str(table_ids)+" tbody tr:visible').each(function () {dict_new[$(this).find('td:nth-child(3) select').attr('id')] = $(this).find('td:nth-child(3) select').children(':selected').val() ;});$('"+str(table_ids)+" tbody tr:visible').each(function () {dict_new[$(this).find('td:nth-child(3) input').attr('id')] =  $(this).find('td:nth-child(3) input').val();});console.log('dict_new-2796--',dict_new);localStorage.setItem('prventdict', JSON.stringify(dict_new))}catch{console.log('')}")
# 				if (TreeParentParam == "Quote Items" or TreeSuperParentParam == "Quote Items" or TreeTopSuperParentParam == "Quote Items"):
# 					dbl_clk_function = ""
# 				else:
# 					#dbl_clk_function += ("try{var dict_new = {};$('"+str(table_ids)+" tbody tr:visible').each(function () {dict_new[$(this).find('td:nth-child(3) select').attr('id')] =  $(this).find('td:nth-child(3) select').children(':selected').attr('id');});$('"+str(table_ids)+" tbody tr:visible').each(function () {dict_new[$(this).find('td:nth-child(3) input').attr('id')] =  $(this).find('td:nth-child(3) input').val();});console.log('dict_new-2818--',dict_new);localStorage.setItem('prventdict', JSON.stringify(dict_new))}catch{console.log('')}")
# 					dbl_clk_function +=   ("try{var dict_new = {};localStorage.setItem('editfirst','true');$('"+str(table_ids)+"').on('dbl-click-cell.bs.table', function (e, row, $element) { localStorage.setItem('AddNew','false');$('"+str(table_ids)+" tbody tr:visible').each(function () {var getcostimpact =  $(this).find('td:nth-child(7) ').text();var getpriceimpact =  $(this).find('td:nth-child(8) ').text();dict_new[$(this).find('td:nth-child(3) select').attr('id')] =$(this).find('td:nth-child(3) select').children(':selected').val()+'||'+getcostimpact+'||'+getpriceimpact;});var arr = [];$('"+str(table_ids)+" tbody tr:visible').each(function () {if ($(this).find('td:nth-child(3) input') && !($(this).find('td:nth-child(3) input').attr('type') == 'checkbox') ){var getcostimpact =  $(this).find('td:nth-child(7) ').text();var getpriceimpact =  $(this).find('td:nth-child(8) ').text();dict_new[$(this).find('td:nth-child(3) input').attr('id')] =  $(this).find('td:nth-child(3) input').val()+'||'+getcostimpact+'||'+getpriceimpact;}else if ($(this).find('td:nth-child(3) input').attr('type') == 'checkbox') {var getcostimpact =  $(this).find('td:nth-child(7) ').text();var getpriceimpact =  $(this).find('td:nth-child(8) ').text();$(this).find('.mulinput:checked').each(function () {arr.push($(this).val());console.log('arr',arr) });dict_new[$(this).find('td:nth-child(3) select').attr('id')] =  arr+'||'+getcostimpact+'||'+getpriceimpact;};});console.log('dblclk_dict_new-28002--',dict_new,'--',"+str(dropdowndisallowlist)+");localStorage.setItem('prventdict', JSON.stringify(dict_new))})}catch(e){console.log('error---12',e)}")
# 					#dbl_clk_function +=   ("try{var dict_new = {};$('"+str(table_ids)+"').on('dbl-click-cell.bs.table', function (e, row, $element) { $('"+str(table_ids)+" tbody tr td select').each(function () {dict_new[$(this).attr('id')] = $(this).children(':selected').val();});$('"+str(table_ids)+" tbody tr td input').each(function () {dict_new[$(this).attr('id')] = $(this).val();});console.log('dblclk_dict_new-2800--',dict_new);localStorage.setItem('prventdict', JSON.stringify(dict_new))})}catch{console.log('')}")
# 					dbl_clk_function += (
# 						"try {var newentdict =[]; var newentValues =[]; var getentedictip = [];$('"+str(table_ids)+"').on('dbl-click-cell.bs.table', function (e, row, $element) {localStorage.setItem('AddNew','false');if(localStorage.getItem('EDITENT_SEC') != 'EDIT'){console.log('tset--prev value--2300-',this.value);localStorage.setItem('EDITENT_SEC','EDIT');$('"+str(getdivid)+"').css('display','block');$('"+str(getdividbtn)+"').css('display','block');$('"+str(table_ids)+" .MultiCheckBox').css('pointer-events','auto');$('#entsave').css('display','block');$('#entcancel').css('display','block'); $('"+str(table_ids)+" .disable_edit').prop('disabled', false);$('#sc_'+'"+str(Section_id)+"').addClass('header_section_div header_section_div_pad_bt10');$('"+str(table_ids)+" .disable_edit').removeClass('remove_yellow').addClass('light_yellow');$('"+str(table_ids)+" tbody tr td:nth-child(5) input').removeClass('light_yellow').addClass('remove_yellow');$('"+str(table_ids)+" tbody tr td:nth-child(5) input').attr('disabled', 'disabled');$('"+str(table_ids)+" tbody tr td:nth-child(6) input').removeClass('light_yellow').addClass('remove_yellow');$('"+str(table_ids)+" tbody tr td:nth-child(7) input').removeClass('light_yellow').addClass('remove_yellow');$('#AGS_CON_DAY').removeClass('light_yellow').addClass('remove_yellow');$('#AGS_CON_DAY').prop('disabled', true);$('"+str(table_ids)+"  tbody tr td:nth-child(7) input').attr('disabled', 'disabled');$('"+str(table_ids)+"  tbody tr td:nth-child(8) input').attr('disabled', 'disabled');$('"+str(table_ids)+"  tbody tr td:nth-child(6) input').attr('disabled', 'disabled');$('#T2_LABOR_TYPE_calc').removeAttr('disabled');$('#T3_LABOR_TYPE_calc').removeAttr('disabled');$('#LABOR_TYPE_calc').removeAttr('disabled');$('#T0_T1_LABOR_TYPE_calc').removeAttr('disabled');$('"+str(table_ids)+" tbody tr td:nth-child(8) input').removeClass('light_yellow').addClass('remove_yellow');$('"+str(table_ids)+" tbody tr td:nth-child(4) input').removeClass('light_yellow').addClass('remove_yellow');var testperf = $('#ADDL_PERF_GUARANTEE_91_1').val();console.log('testperf--1---',testperf);if(testperf != undefined && testperf != ''){ if(testperf.toUpperCase() == 'MANUAL INPUT'){console.log('manual input val on donble click---');$('#ADDL_PERF_GUARANTEE_91_1_imt').removeAttr('disabled');$('#ADDL_PERF_GUARANTEE_91_1_imt').parent().css('position', 'relative');$('#ADDL_PERF_GUARANTEE_91_1_primp').parent().css('position', 'relative');$('#ADDL_PERF_GUARANTEE_91_1_primp').removeAttr('disabled');}else{$('#ADDL_PERF_GUARANTEE_91_1_imt').removeClass('light_yellow')};};$('#ADDL_PERF_GUARANTEE_91_1_dt').attr('disabled', 'disabled');$('#ADDL_PERF_GUARANTEE_91_1_calc').attr('disabled', 'disabled');$('input').on('focus', function () {var previnp = $(this).data('val', $(this).val());$('#ADDL_PERF_GUARANTEE_91_1_primp').removeAttr('disabled');console.log('manual input----');var getprevid = this.id;var prev_concate_data = getprevid +'='+previnp;}).change(function() {var prev = $(this).data('val');var current = $(this).val();var getseltabledesc = this.id;var getinputtbleid =  $(this).closest('table').attr('id');var concated_data = getinputtbleid+'|'+current+'|'+getseltabledesc;if(!getentedictip.includes(concated_data)){getentedictip.push(concated_data)};getentedictip1 = JSON.stringify(getentedictip);localStorage.setItem('getdictentdata', getentedictip1);});}})}catch {console.log('error---')}"
# 					)
# 				Trace.Write('dbl_clk_function---'+str(dbl_clk_function))
# 				'''dbl_clk_function += (
# 					"try {var getentedict = [];$('"+str(table_ids)+"').on('click-row.bs.table', function (e, row, $element) {console.log('tset--prev value---',this.value);$('"+str(table_ids)+"').find(':input(:disabled)').prop('disabled', false);$('"+str(table_ids)+" tbody  tr td select option').css('background-color','lightYellow');$('"+str(table_ids)+"  tbody tr td select').addClass('light_yellow');$('#fabcostlocate_save').css('display','block');$('#AGS_CON_DAY').prop('disabled', true);$('select').on('focus', function () { var previousval = this.value;console.log('previous1---',previousval);localStorage.setItem('previousval', previousval);}).change(function() {var entchanged = this.value;console.log('previous--previous-----',entchanged);var getatbleid =  $(this).closest('table').attr('id');localStorage.setItem('getatbleid', getatbleid);console.log('getatbleid----',getatbleid);var getseltabledesc = this.id;console.log('getseltableid---',getseltabledesc);var previousval = localStorage.getItem('previousval');var concate_data = getatbleid +'='+previousval+'='+getseltabledesc+'='+entchanged;if(!getentedict.includes(concate_data)){getentedict.push(concate_data)};console.log('getentedict---',getentedict);getentedict = JSON.stringify(getentedict);localStorage.setItem('getentedict', getentedict);localStorage.setItem('previousval', '');});});}catch {console.log('error---')}"
# 				)'''
			
# 	##Adding Audit information section in Entitlement starts...
# 	if EntitlementType in ("EQUIPMENT","FABLOCATION","BUSINESSUNIT","ASSEMBLY","TOOLS"):
# 		get_sec = Sql.GetFirst("""SELECT * FROM SYSECT WHERE PRIMARY_OBJECT_NAME = '{}' AND SECTION_NAME = 'AUDIT INFORMATION'""".format(ObjectName))
# 		if get_sec :
# 			section_id = get_sec.RECORD_ID
# 			section_desc = get_sec.SECTION_NAME
			
# 			sec_str_boot += ('<div id="container" class="wdth100 margtop10"><div id="sec_'+str(section_id)+ '" class="dyn_main_head master_manufac glyphicon pointer   glyphicon-chevron-down" onclick="dyn_main_sec_collapse_arrow(this)" data-target="#sc_'+ str(section_id)+ '" data-toggle="collapse" <label class="onlytext"><label class="onlytext"><div>'+ str(section_desc).upper()+ '</div></label></div><div id="sc_'+str(section_id)+ '" class="collapse in "><table id="' + str(section_id)+ '" class= "wth100mrg8"  > <tbody>')
# 			get_sefl = Sql.GetList(
# 				"SELECT TOP 1000 FIELD_LABEL, API_FIELD_NAME,RECORD_ID FROM SYSEFL WHERE SECTION_RECORD_ID = '" + str(section_id) + "' ORDER BY DISPLAY_ORDER"
# 			)
# 			col_name = Sql.GetFirst("SELECT * FROM "+str(ObjectName)+" WHERE "+str(where)+" ")
# 			for sefl in get_sefl:
# 				sec_str_boot += (
# 						'<tr class="iconhvr brdbt" style=" "><td class="wth350"><abbr title="'
# 						+ str(sefl.FIELD_LABEL)
# 						+ '" ><label class="pad5mrgbt0">'
# 						+ str(sefl.FIELD_LABEL)
# 						+ '</label></abbr></td><td width40><a  title="'
# 						+ str(sefl.FIELD_LABEL)
# 						+ '"data-content="'
# 						+ str(sefl.FIELD_LABEL)
# 						+ '" class="bgcccwth10"><i class="fa fa-info-circle fltlt"></i></a></td>'
# 					)
# 				sefl_api = sefl.API_FIELD_NAME
				
# 				if col_name:
# 					current_obj_value = str(eval("col_name." + str(sefl_api)))
# 					Trace.Write('current_obj_value---'+str(current_obj_value)+'--'+str(sefl_api))
# 					if sefl_api in ("CPQTABLEENTRYDATEADDED","CpqTableEntryDateModified") and current_obj_value:
# 						try:
# 							current_obj_value = datetime.strptime(str(current_obj_value), '%m/%d/%Y %I:%M:%S %p').strftime('%m/%d/%Y %I:%M:%S %p')
# 						except:
# 							pass
# 					elif sefl_api in ("CpqTableEntryModifiedBy","CPQTABLEENTRYADDEDBY") and current_obj_value:
# 						current_user = Sql.GetFirst(
# 							"SELECT USERNAME FROM USERS WHERE ID = " + str(current_obj_value) + "")
# 						current_obj_value = current_user.USERNAME

# 					sec_str_boot +=(
# 						'<td><input id="'
# 						+ str(sefl_api)
# 						+ '" type="text" value="'
# 						+ current_obj_value
# 						+ '" title="'
# 						+ current_obj_value
# 						+ '" class="form-control related_popup_css" '
# 						+ " disabled></td>"
# 					)
# 					sec_str_boot +=(
# 						'<td class="float_r_bor_bot"><div class="col-md-12 editiconright"><a onclick="" class="editclick"><i class="fa fa-lock" aria-hidden="true"></i></a></div></td>'
# 					)

# 				sec_str_boot +=	('</tr>')
				
# 			sec_str_boot += '</tbody></table>'
		
# 			sec_str_boot += ('</div></div>')
			
		
# 	##Adding Audit information section in Entitlement ends...

# 	quote_status = Sql.GetFirst("SELECT QUOTE_STATUS FROM SAQTMT WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' ".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id ))
# 	if quote_status:
# 		if quote_status.QUOTE_STATUS == "APPROVED":
# 			Trace.Write('dbl_click123====')
# 			dbl_clk_function = ""

		
# 	date_field = ""
# 	new_value_dict = ""
# 	api_name = ""
# 	ret_value = ""
# 	#Trace.Write('multi_select_attr_list'+str(multi_select_attr_list))
# 	return sec_str, date_field, new_value_dict, api_name, ret_value, ObjectName, sec_bnr,sec_str_boot,tablistnew,dbl_clk_function,getprevdicts,totaldisallowlist,msg_txt,ChangedList,getnameentallowed,getvaludipto,getvaludipt1,getvaludipt2,getvaludipt2lt,getvaludipt2lab,getvaludipto_q ,getvaludipt2_q,getvaludipt2lt_q ,getvaludipt2lab_q ,getvaludipt2lab,getvaludipt3lab ,getvaludipt3lab_q , getvaludipt3labt ,getvaludipt3labt_q,getvaludipt1_q,getlabortype_calc,gett1labor_calc,gett1labortype_calc,gett2labo_calc,gett2labotype_calc,gett3lab_calc,gett3labtype_calc,getTlab,section_not_list,multi_select_attr_list

# def ContractEntitlementTreeViewHTMLDetail(
# 	MODE,
# 	TableId,
# 	RECORD_ID,
# 	TreeParam,
# 	NEWVAL,
# 	LOOKUPOBJ,
# 	LOOKUPAPI,
# 	SECTION_EDIT,
# 	Flag,
# 	TreeParentParam,
# 	ObjectName,
# 	SectionList,
# 	EntitlementType,
# ):
# 	quoteid = Product.GetGlobal("contract_record_id")
# 	TreeParentParam = Product.GetGlobal("TreeParentLevel0")
# 	TreeSuperParentParam = Product.GetGlobal("TreeParentLevel1")	
# 	if EntitlementType == "EQUIPMENT":
# 		TableObj = Sql.GetFirst("select * from CTCTSE (NOLOCK) where CNTSRV_RECORD_ID = '" + str(RECORD_ID) + "'")
# 		ParentObj = Sql.GetFirst("select * from CTCTSV (NOLOCK) where CONTRACT_SERVICES_RECORD_ID = '" + str(RECORD_ID) + "'")
# 		if ParentObj:
# 			CONTRACT_ID = ParentObj.CONTRACT_ID
# 			CONTRACT_NAME = ParentObj.CONTRACT_NAME
# 			CONTRACT_RECORD_ID = ParentObj.CONTRACT_RECORD_ID
# 			CONTRACT_SERVICES_RECORD_ID = ParentObj.CONTRACT_SERVICES_RECORD_ID
# 			SERVICE_RECORD_ID = ParentObj.SERVICE_RECORD_ID
# 			SERVICE_ID = ParentObj.SERVICE_ID
# 			SERVICE_DESCRIPTION = ParentObj.SERVICE_DESCRIPTION
# 			SALESORG_RECORD_ID = ParentObj.SALESORG_RECORD_ID
# 			SALESORG_ID = ParentObj.SALESORG_ID
# 			SALESORG_NAME = ParentObj.SALESORG_NAME
# 		where = "CONTRACT_RECORD_ID = '" + str(CONTRACT_RECORD_ID) + "' AND CNTSRV_RECORD_ID = '" + str(RECORD_ID) + "'"
# 		join = ''

# 	elif EntitlementType == "TOOLS":
# 		TableObj = Sql.GetFirst("select * from CTCTSE (NOLOCK) where CNTSRV_RECORD_ID = '" + str(RECORD_ID) + "'")
# 		ObjectName = "CTCSCE"
# 		where = "CONTRACT_RECORD_ID = '" + str(quoteid) + "' AND CNTSRVCOB_RECORD_ID = '" + str(RECORD_ID) + "'"
# 		join = ''
# 	elif EntitlementType == "ITEMGREENBOOK":
# 		TableObj = Sql.GetFirst("select * from CTCIEN (NOLOCK) where CNTITMCOB_RECORD_ID = '" + str(RECORD_ID) + "'")
# 		ObjectName = "CTCIEN"
# 		where = "CONTRACT_RECORD_ID = '" + str(quoteid) + "' AND CNTITMCOB_RECORD_ID = '" + str(RECORD_ID) + "'"
# 		join = ''
# 		#cpsConfigID = TableObj.CPS_CONFIGURATION_ID
# 	elif EntitlementType == "ITEMS":
# 		TableObj = Sql.GetFirst("select * from CTCIEN (NOLOCK) where CTESRVCOE_RECORD_ID = '" + str(RECORD_ID) + "'")
# 		where = "CTCITM.CONTRACT_ITEM_RECORD_ID = '" + str(RECORD_ID) + "'"
# 		join = 'JOIN CTCITM ON CTCITM.CONTRACT_ITEM_RECORD_ID = CTCIEN.CONTRACT_RECORD_ID'
# 	elif EntitlementType == "BUSINESSUNIT":
# 		TableObj = Sql.GetFirst("select * from CTCSGE (NOLOCK) where CONTRACT_RECORD_ID = '" + str(quoteid) + "' AND SERVICE_ID = '" + str(TreeParentParam) + "'")
# 		if TableObj is not None:
# 			RECORD_ID = str(TableObj.SERVICE_RECORD_ID)
# 		where = "CONTRACT_RECORD_ID = '" + str(quoteid) + "' AND SERVICE_RECORD_ID = '" + str(RECORD_ID) + "'"
# 		join = ''

# 	if TreeSuperParentParam == "Product Offerings":
# 		# requestdata= '{"productKey":"'+TreeParam+'","date":"2020-10-14","context":[{"name":"VBAP-MATNR","value":"'+TreeParam+'"}]}'
# 		ProductPartnumber = TreeParam
# 	elif TreeTopSuperParentParam == "Product Offerings":		
# 		# requestdata= '{"productKey":"'+TreeParentParam+'","date":"2020-09-01","context":[{"name":"VBAP-MATNR","value":"'+TreeParentParam+'"}]}'		
# 		ProductPartnumber = TreeParentParam
# 	elif TreeParentParam == "Cart Items":
# 		GetItem = Sql.GetFirst("select * from CTCICO (NOLOCK) where CONTRACT_ITEM_COVERED_OBJECT_RECORD_ID = '" + str(RECORD_ID) + "'")
# 		if GetItem is not None:
# 			ProductPartnumber = GetItem.SERVICE_ID
# 		if "-" in TreeParam:
# 			TreeParam = TreeParam.split("-")[1].strip()
# 	elif TreeSuperParentParam == "Cart Items":
# 		TreeParentParam = TreeParentParam.split("-")[1].strip()
# 		ProductPartnumber = TreeParentParam

# 	'''if TableObj is None and EntitlementType == "EQUIPMENT":
# 		Request_URL = "https://cpservices-product-configuration.cfapps.us10.hana.ondemand.com/api/v2/configurations?autoCleanup=False"
# 		Fullresponse = EntitlementRequest(ProductPartnumber,Request_URL,"New")
# 	else:
# 		Request_URL = "https://cpservices-product-configuration.cfapps.us10.hana.ondemand.com/api/v2/configurations/"+str(cpsConfigID)
# 		Fullresponse = EntitlementRequest(ProductPartnumber,Request_URL,"Existing")'''
# 	'''if TableObj is None and EntitlementType == "EQUIPMENT":
# 		Fullresponse = EntitlementRequest(ProductPartnumber,"False")
# 	else:
# 		Fullresponse = EntitlementRequest(ProductPartnumber,"True")'''

# 	attributesdisallowedlst = []
# 	attributeReadonlylst = []
# 	attributeEditlst =[]
# 	tablistnew = []
# 	attributevalues = {}
# 	# where = ""
# 	# for rootattribute, rootvalue in Fullresponse.items():
# 	# 	if rootattribute == "rootItem":
# 	# 		for Productattribute, Productvalue in rootvalue.items():
# 	# 			if Productattribute == "characteristics":
# 	# 				for prdvalue in Productvalue:
# 	# 					if prdvalue["visible"] == "false":
# 	# 						Trace.Write(prdvalue["id"] + " set here")
# 	# 						attributesdisallowedlst.append(prdvalue["id"])
# 	# 					if prdvalue["readOnly"] == "true":
# 	# 						attributeReadonlylst.append(prdvalue["id"])
# 	# 					if prdvalue["readOnly"] == "false":
# 	# 						attributeEditlst.append(prdvalue["id"])
# 	# 					for attribute in prdvalue["values"]:
# 	# 						# Trace.Write("attribute---"+str(attribute))
# 	# 						attributevalues[str(prdvalue["id"])] = attribute["value"]
# 	product_obj = Sql.GetFirst("""SELECT 
# 								MAX(PDS.PRODUCT_ID) AS PRD_ID,PDS.SYSTEM_ID,PDS.PRODUCT_NAME 
# 							FROM PRODUCTS PDS 
# 							INNER JOIN PRODUCT_VERSIONS PRVS ON  PDS.PRODUCT_ID = PRVS.PRODUCT_ID 
# 							WHERE SYSTEM_ID ='{SystemId}' 
# 							GROUP BY PDS.SYSTEM_ID,PDS.UnitOfMeasure,PDS.CART_DESCRIPTION_BUILDER,PDS.PRODUCT_NAME""".format(SystemId = str(ProductPartnumber)))
	
# 	product_tabs_obj = Sql.GetList("""SELECT 
# 											TOP 1000 TAB_NAME, TAB_RANK, TAB_PROD_ID, TAB_PRODUCTS.TAB_CODE
# 										FROM TAB_PRODUCTS
# 										JOIN TAB_DEFN ON TAB_DEFN.TAB_CODE = TAB_PRODUCTS.TAB_CODE
# 										WHERE TAB_PRODUCTS.PRODUCT_ID = {ProductId}
# 										ORDER BY TAB_PRODUCTS.RANK""".format(ProductId = product_obj.PRD_ID))
	
# 	product_attributes_obj = Sql.GetList("""SELECT TOP 1000 PAT_SCHEMA.STANDARD_ATTRIBUTE_CODE, 
# 												TAB_PRODUCTS.TAB_PROD_ID, TAB_PRODUCTS.TAB_CODE, ATTRIBUTE_DEFN.STANDARD_ATTRIBUTE_NAME,PRODUCT_ATTRIBUTES.LABEL AS LABEL, ATTRIBUTE_DEFN.SYSTEM_ID AS SYSTEM_ID, ATT_DISPLAY_DEFN.ATT_DISPLAY_DESC AS ATT_DISPLAY_DESC
# 											FROM TAB_PRODUCTS
# 											LEFT JOIN PAT_SCHEMA ON PAT_SCHEMA.TAB_PROD_ID=TAB_PRODUCTS.TAB_PROD_ID											
# 											LEFT JOIN PRODUCT_ATTRIBUTES ON PRODUCT_ATTRIBUTES.STANDARD_ATTRIBUTE_CODE = PAT_SCHEMA.STANDARD_ATTRIBUTE_CODE AND PRODUCT_ATTRIBUTES.PRODUCT_ID = TAB_PRODUCTS.PRODUCT_ID
# 											LEFT JOIN ATTRIBUTE_DEFN ON ATTRIBUTE_DEFN.STANDARD_ATTRIBUTE_CODE = PRODUCT_ATTRIBUTES.STANDARD_ATTRIBUTE_CODE
# 											LEFT JOIN ATT_DISPLAY_DEFN ON ATT_DISPLAY_DEFN.ATT_DISPLAY = PRODUCT_ATTRIBUTES.ATT_DISPLAY
											
# 											WHERE TAB_PRODUCTS.PRODUCT_ID = {ProductId}
# 											ORDER BY TAB_PRODUCTS.RANK""".format(ProductId = product_obj.PRD_ID))
# 	tabwise_product_attributes = {}	
# 	if product_attributes_obj:
# 		for product_attribute_obj in product_attributes_obj:
# 			attr_detail = {'attribute_name':str(product_attribute_obj.STANDARD_ATTRIBUTE_NAME), 
# 						'attribute_label':str(product_attribute_obj.LABEL), 
# 						'attribute_system_id':str(product_attribute_obj.SYSTEM_ID),
# 						'attribute_dtype':str(product_attribute_obj.ATT_DISPLAY_DESC)
						
# 						}
# 			if product_attribute_obj.TAB_PROD_ID in tabwise_product_attributes:
# 				tabwise_product_attributes[product_attribute_obj.TAB_PROD_ID].append(attr_detail)
# 			else:
# 				tabwise_product_attributes[product_attribute_obj.TAB_PROD_ID] = [attr_detail]
	
# 	ServiceContainer = Product.GetContainerByName("Services")
# 	sec_str = ""
# 	'''GetCPSVersion = Sql.GetFirst("SELECT KB_VERSION FROM SAQTSE (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND KB_VERSION IS NOT NULL".format(quoteid))
# 	if GetCPSVersion:
# 		if GetCPSVersion.KB_VERSION is not None and GetCPSVersion.KB_VERSION != Fullresponse["kbKey"]["version"]:
# 			sec_str += '<div id="Headerbnr" class="mart_col_back disp_blk"><div class="col-md-12" id="PageAlert"><div class="row modulesecbnr brdr" data-toggle="collapse" data-target="#Alert_notifcatio6" aria-expanded="true">NOTIFICATIONS<i class="pull-right fa fa-chevron-down"></i><i class="pull-right fa fa-chevron-up"></i></div><div id="Alert_notifcatio6" class="col-md-12 alert-notification brdr collapse in"><div class="col-md-12 alert-info"><label title=" Information : The Knowledgebase of the VC Characteristics has been updated in CPS."><img src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/infocircle1.svg" alt="Info"> Information : The Knowledgebase of the VC Characteristics has been updated in CPS.</label></div></div></div></div>'
# 		else:
# 			sec_str = ''
# 	else:
# 		Trace.Write("GETCPS VERSION EMPTY!")'''	

# 	#desc_list = ["APPROVAL","ENTITLEMENT DESCRIPTION","ENTITLEMENT VALUE","DATA TYPE","FACTOR CURRENCY","CALCULATION FACTOR","ENTITLEMENT COST IMPACT","ENTITLEMENT PRICE IMPACT",]
# 	desc_list = ["APPROVAL","ENTITLEMENT DESCRIPTION","ENTITLEMENT VALUE","CALCULATION FACTOR","ENTITLEMENT COST IMPACT","ENTITLEMENT PRICE IMPACT",]
	
# 	#attr_dict = {"APPROVAL":"APPROVAL","ENTITLEMENT DESCRIPTION": "ENTITLEMENT DESCRIPTION","ENTITLEMENT VALUE": "ENTITLEMENT VALUE","DATA TYPE":"DATA TYPE","FACTOR CURRENCY": "FACTOR CURRENCY","CALCULATION FACTOR": "CALCULATION FACTOR","ENTITLEMENT PRICE IMPACT":"ENTITLEMENT PRICE IMPACT","ENTITLEMENT COST IMPACT":"ENTITLEMENT COST IMPACT",}
# 	attr_dict = {"APPROVAL":"APPROVAL","ENTITLEMENT DESCRIPTION": "ENTITLEMENT DESCRIPTION","ENTITLEMENT VALUE": "ENTITLEMENT VALUE","CALCULATION FACTOR": "CALCULATION FACTOR","ENTITLEMENT PRICE IMPACT":"ENTITLEMENT PRICE IMPACT","ENTITLEMENT COST IMPACT":"ENTITLEMENT COST IMPACT",}
# 	date_field = []
# 	getnameentallowed = []
# 	insertservice = ""
	
# 	if TableObj is None and EntitlementType == "EQUIPMENT":  # or len(TableObj)>0:
# 		tableInfo = SqlHelper.GetTable("CTCTSE")
# 		for row in ServiceContainer.Rows:
# 			if TreeParam.upper() == str(row.Product.PartNumber).upper():
# 				ContainerProduct = row.Product
# 				tabs = ContainerProduct.Tabs
# 				list_of_tabs = []
# 				for tab in tabs:
# 					list_of_tabs.append(tab.Name)
# 					sysectObj = Sql.GetFirst(
# 						"SELECT RECORD_ID,SECTION_DESC FROM SYSECT (NOLOCK) WHERE SECTION_NAME='" + str(tab.Name) + "'  "
# 					)
# 					Section_id = sysectObj.RECORD_ID
# 					Section_desc = sysectObj.SECTION_DESC
# 					sec_str += '<div id="container" class="wdth100 margtop10 g4 ' + str(Section_id) + '">'
# 					sec_str += (
# 						'<div class="dyn_main_head master_manufac glyphicon pointer   glyphicon-chevron-down" onclick="dyn_main_sec_collapse_arrow(this)" data-target="#sec_'
# 						+ str(Section_id)
# 						+ '" data-toggle="collapse"><label class="onlytext"><label class="onlytext"><div><div id="ctr_drop" class="btn-group dropdown"><div class="dropdown"><i data-toggle="dropdown" class="fa fa-sort-desc dropdown-toggle"></i><ul class="dropdown-menu left" aria-labelledby="dropdownMenuButton"><li class="edit_list"><a id="'
# 						+ str(Section_id)
# 						+ '" class="dropdown-item" href="#" onclick="edit_entitlement(this)">EDIT</a></li></ul></div></div>'
# 						+ str(Section_desc)
# 						+ "</div></label></div>"
# 					)

# 					sec_str += '<div id="sec_' + str(Section_id) + '" class="collapse in">'
# 					sec_str += '<table class="wth100mrg8"><tbody>'
# 					add_style =  ""
# 					for attr in tab.Attributes:
# 						attrName = attr.Name
# 						attrLabel = attr.Name
# 						attrValue = attr.GetValue()
# 						attrSysId = attr.SystemId
# 						DType = attr.DisplayType						
# 						if attrSysId in attributesdisallowedlst:
# 							add_style = "display:none"
# 						else:
# 							add_style = ""
# 							""
# 						if attrSysId in attributeEditlst :
# 							edit_pencil_icon = '<i class="fa fa-pencil" aria-hidden="true"></i>'
							
# 						else:
# 							edit_pencil_icon = '<i class="fa fa-lock" aria-hidden="true"></i>'
# 						attrValueSysId = attributevalues.get(attrSysId)
# 						if DType in ("DropDown", "CheckBox", "Drop Down", "Check Box"):
# 							Count = 0
# 							for value in attr.Values:
# 								Count += 1
# 								if attrValueSysId == value.ValueCode:
# 									attrValue = value.Display
# 									break
# 								elif "D:" in str(value.Display):
# 									attrValue = value.Display
# 									break
# 								elif Count == 1:
# 									attrValue = value.Display
# 						# Inserting Rows:
# 						tbrow = {}
# 						tbrow["CONTRACT_SERVICE_ENTITLEMENTS_RECORD_ID"] = str(Guid.NewGuid()).upper()
# 						tbrow["CONTRACT_ID"] = CONTRACT_ID
# 						tbrow["CONTRACT_NAME"] = CONTRACT_NAME
# 						tbrow["CONTRACT_RECORD_ID"] = CONTRACT_RECORD_ID
# 						tbrow["CNTSRV_RECORD_ID"] = CNTSRV_RECORD_ID
# 						tbrow["SERVICE_RECORD_ID"] = SERVICE_RECORD_ID
# 						tbrow["SERVICE_ID"] = SERVICE_ID
# 						tbrow["SERVICE_DESCRIPTION"] = SERVICE_DESCRIPTION
# 						tbrow["ENTITLEMENT_NAME"] = attrSysId
# 						tbrow["ENTITLEMENT_DESCRIPTION"] = attrName
# 						tbrow["ENTITLEMENT_VALUE_CODE"] = attrValueSysId
# 						tbrow["ENTITLEMENT_DISPLAY_VALUE"] = attrValue
# 						tbrow["ENTITLEMENT_TYPE"] = DType
# 						tbrow["SALESORG_RECORD_ID"] = SALESORG_RECORD_ID
# 						tbrow["SALESORG_ID"] = SALESORG_ID
# 						tbrow["SALESORG_NAME"] = SALESORG_NAME
# 						# tbrow["ENTITLEMENT_TYPE"]=
# 						tableInfo.AddRow(tbrow)
# 						if DType in ("DropDown", "CheckBox", "Drop Down", "Check Box"):
							
# 							sec_str += (
# 								'<tr class="iconhvr brdbt" style="'
# 								+ str(add_style)
# 								+ '"><td class="wth350"> <abbr title="'
# 								+ str(attrLabel)
# 								+ '"> <label class="pad5mrgbt0">'
# 								+ str(attrLabel)
# 								+ '</label> </abbr> </td> <td width40=""> <a href="#" title="" data-placement="auto top" data-toggle="popover" data-trigger="focus" data-content="'
# 								+ str(attrLabel)
# 								+ '" class="bgcccwth10"> <i class="fa fa-info-circle fltlt"></i> </a> </td><td><select id="'
# 								+ str(attrSysId)
# 								+ '" type="text" value="'
# 								+ attrValue
# 								+ '" title="'
# 								+ str(attrValue)
# 								+ '" data-content ="'
# 								+ str(attrValueSysId)
# 								+ '" class="form-control related_popup_css" disabled>'
# 							)

# 							for value in attr.Values:
# 								if attrValueSysId == value.ValueCode:
# 									optionvalue = value.Display
# 									attrcode = str(value.ValueCode).replace(" ","_")
# 								elif "D:" in str(value.Display):
# 									optionvalue = value.Display
# 								else:
# 									optionvalue=value.Display
# 								if str(optionvalue) == attrValue:
# 									sec_str += (
# 										"<option id="+str(attrcode)+" selected>" + str(attrValue) + "</option>"
# 									)
# 								else:
# 									sec_str += "<option id='"+str(attrcode)+"' >" + str(optionvalue) + "</option>"
# 							sec_str += "</select></td>"
# 						else:
# 							sec_str += (
# 								'<tr class="iconhvr brdbt" style="'
# 								+ str(add_style)
# 								+ '"><td class="wth350"> <abbr title="'
# 								+ str(attrLabel)
# 								+ '"> <label class="pad5mrgbt0">'
# 								+ str(attrLabel)
# 								+ '</label> </abbr> </td> <td width40=""> <a href="#" title="" data-placement="auto top" data-toggle="popover" data-trigger="focus" data-content="'
# 								+ str(attrLabel)
# 								+ '" class="bgcccwth10"> <i class="fa fa-info-circle fltlt"></i> </a> </td><td><input id="'
# 								+ str(attrSysId)
# 								+ '" type="text" style="width: 90% ! important;" value="'
# 								+ attrValue
# 								+ '" title="'
# 								+ str(attrValue)
# 								+ '" data-content ="'
# 								+ str(attrValueSysId)
# 								+ '" class="form-control related_popup_css" disabled></td>'
# 							)
# 						sec_str += (
# 							'<td class="float_r_bor_bot" style ="'+str(add_style)+'"><div class="col-md-12 editiconright"><a href="#" class="editclick">'
# 							+ str(edit_pencil_icon)
# 							+ "</a></div></td></tr>"
# 						)
# 					sec_str += "</tbody></table></div>"
						
# 			#Trace.Write("IFSEC"+sec_str)
# 		Sql.Upsert(tableInfo)
# 		QueryStatement ="""
# 		MERGE CTCIEN SRC USING (SELECT A.ENTITLEMENT_NAME,A.ENTITLEMENT_TYPE,A.ENTITLEMENT_VALUE_CODE,B.EQUIPMENT_ID,B.EQUIPMENT_RECORD_ID,A.CONTRACT_ID,B.CONTRACT_ITEM_COVERED_OBJECT_RECORD_ID,B.CNTITM_RECORD_ID,A.CONTRACT_RECORD_ID,A.CONTRACT_SERVICE_ENTITLEMENTS_RECORD_ID,B.SERIAL_NO,A.SERVICE_DESCRIPTION,A.SERVICE_ID,A.SERVICE_RECORD_ID,A.SALESORG_ID,A.SALESORG_NAME,A.SALESORG_RECORD_ID,A.ENTITLEMENT_DESCRIPTION,A.ENTITLEMENT_DISPLAY_VALUE,B.EQUIPMENT_LINE_ID FROM CTCTSE(NOLOCK) A JOIN CTCICO (NOLOCK) B ON A.CONTRACT_RECORD_ID  = B.CONTRACT_RECORD_ID AND A.SALESORG_ID =B.SALESORG_ID where A.CONTRACT_RECORD_ID = '{rec}' )
# 		TGT ON (SRC.CONTRACT_RECORD_ID = TGT.CONTRACT_RECORD_ID AND SRC.SERVICE_ID = TGT.SERVICE_ID )
# 		WHEN MATCHED
# 		THEN UPDATE SET SRC.ENTITLEMENT_DISPLAY_VALUE = TGT.ENTITLEMENT_DISPLAY_VALUE
# 		WHEN NOT MATCHED BY TARGET
# 		THEN INSERT(CONTRACT_ITEM_COV_OBJ_ENTITLEMENT_RECORD_ID,ENTITLEMENT_NAME,ENTITLEMENT_TYPE,ENTITLEMENT_VALUE_CODE,EQUIPMENT_ID,EQUIPMENT_RECORD_ID,CONTRACT_ID,CNTITMCOB_RECORD_ID,CNTITM_RECORD_ID,CONTRACT_RECORD_ID,CTESRVCOE_RECORD_ID,SERIAL_NUMBER,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,ENTITLEMENT_DESCRIPTION,ENTITLEMENT_DISPLAY_VALUE,EQUIPMENT_LINE_ID,CPQTABLEENTRYDATEADDED, CPQTABLEENTRYADDEDBY, ADDUSR_RECORD_ID, CpqTableEntryModifiedBy,
# 				CpqTableEntryDateModified)
# 		VALUES (NEWID(),ENTITLEMENT_NAME,ENTITLEMENT_TYPE,ENTITLEMENT_VALUE_CODE,EQUIPMENT_ID,EQUIPMENT_RECORD_ID,CONTRACT_ID,CONTRACT_ITEM_COVERED_OBJECT_RECORD_ID,CNTITM_RECORD_ID,CONTRACT_RECORD_ID,CONTRACT_SERVICE_ENTITLEMENTS_RECORD_ID,SERIAL_NO,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,ENTITLEMENT_DESCRIPTION,ENTITLEMENT_DISPLAY_VALUE,EQUIPMENT_LINE_ID,'{datetimenow}', '{username}', {userid}, {userid}, '{datetimenow}' );""".format(rec=quoteid, datetimenow=datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"), userid=userId, username=userName)
# 		Sql.RunQuery(QueryStatement)
# 		QueryStatement ="""
# 		MERGE CTCIEN SRC USING (SELECT A.ENTITLEMENT_NAME,A.ENTITLEMENT_TYPE,A.ENTITLEMENT_VALUE_CODE,B.SAP_PART_NUMBER,A.CONTRACT_ID,B.CONTRACT_ITEM_FORECAST_PART_RECORD_ID,B.CNTITM_RECORD_ID,A.CONTRACT_RECORD_ID,A.CONTRACT_SERVICE_ENTITLEMENTS_RECORD_ID,A.SERVICE_DESCRIPTION,A.SERVICE_ID,A.SERVICE_RECORD_ID,A.SALESORG_ID,A.SALESORG_NAME,A.SALESORG_RECORD_ID,A.ENTITLEMENT_DESCRIPTION,A.ENTITLEMENT_DISPLAY_VALUE FROM CTCTSE(NOLOCK) A JOIN CTCIFP (NOLOCK) B ON A.CONTRACT_RECORD_ID  = B.CONTRACT_RECORD_ID AND A.SALESORG_ID =B.SALESORG_ID where A.CONTRACT_RECORD_ID = '{rec}' )
# 		TGT ON (SRC.CONTRACT_RECORD_ID = TGT.CONTRACT_RECORD_ID AND SRC.SERVICE_ID = TGT.SERVICE_ID ) 
# 		WHEN MATCHED THEN UPDATE SET SRC.ENTITLEMENT_DISPLAY_VALUE = TGT.ENTITLEMENT_DISPLAY_VALUE
# 		WHEN NOT MATCHED BY TARGET THEN INSERT(CONTRACT_ITEM_COV_OBJ_ENTITLEMENT_RECORD_ID,ENTITLEMENT_NAME,ENTITLEMENT_TYPE,ENTITLEMENT_VALUE_CODE,EQUIPMENT_ID,EQUIPMENT_RECORD_ID,CONTRACT_ID,CNTITM_RECORD_ID,CONTRACT_RECORD_ID,CTESRVCOE_RECORD_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,ENTITLEMENT_DESCRIPTION,ENTITLEMENT_DISPLAY_VALUE,EQUIPMENT_LINE_ID,CPQTABLEENTRYDATEADDED, CPQTABLEENTRYADDEDBY, ADDUSR_RECORD_ID, CpqTableEntryModifiedBy,CpqTableEntryDateModified) VALUES (NEWID(),ENTITLEMENT_NAME,ENTITLEMENT_TYPE,ENTITLEMENT_VALUE_CODE,CONTRATC_ID,CNTITM_RECORD_ID,CONTRACT_RECORD_ID,CONTRACT_SERVICE_ENTITLEMENTS_RECORD_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,ENTITLEMENT_DESCRIPTION,ENTITLEMENT_DISPLAY_VALUE,'{datetimenow}', '{username}', {userid}, {userid}, '{datetimenow}' );""".format(rec=quoteid, datetimenow=datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"), userid=userId, username=userName)
# 		Sql.RunQuery(QueryStatement)
# 	else:
# 		getinnercon  = Sql.GetFirst("select CONTRACT_RECORD_ID,convert(xml,replace(replace(ENTITLEMENT_XML,'&',';#38'),'''',';#39')) as ENTITLEMENT_XML from "+str(ObjectName)+" (nolock)  where  "+str(where)+"")
		
# 		GetXMLsecField = Sql.GetList("SELECT distinct e.CONTRACT_RECORD_ID, replace(X.Y.value('(ENTITLEMENT_NAME)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_NAME,replace(X.Y.value('(IS_DEFAULT)[1]', 'VARCHAR(128)'),';#38','&') as IS_DEFAULT,replace(X.Y.value('(ENTITLEMENT_COST_IMPACT)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_COST_IMPACT,replace(X.Y.value('(CALCULATION_FACTOR)[1]', 'VARCHAR(128)'),';#38','&') as CALCULATION_FACTOR,replace(X.Y.value('(ENTITLEMENT_PRICE_IMPACT)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_PRICE_IMPACT,replace(X.Y.value('(ENTITLEMENT_TYPE)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_TYPE,replace(X.Y.value('(ENTITLEMENT_VALUE_CODE)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_VALUE_CODE,replace(X.Y.value('(ENTITLEMENT_DESCRIPTION)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_DESCRIPTION,replace(replace(X.Y.value('(ENTITLEMENT_DISPLAY_VALUE)[1]', 'VARCHAR(128)'),';#38','&'),';#39','''') as ENTITLEMENT_DISPLAY_VALUE FROM (select '"+str(getinnercon.CONTRACT_RECORD_ID)+"' as CONTRACT_RECORD_ID,convert(xml,'"+str(getinnercon.ENTITLEMENT_XML)+"') as ENTITLEMENT_XML ) e OUTER APPLY e.ENTITLEMENT_XML.nodes('QUOTE_ITEM_ENTITLEMENT') as X(Y) ")
		
# 		sec_str_cf = sec_str_boot = sec_bnr = getprevdicts = sec_str_primp = sec_str1 = dbl_clk_function = ""
# 		getnameentallowed = []
# 		## set entitlement_xml for cancel fn A055S000P01-3157 starts
# 		previous_entitlement_xml  = Sql.GetFirst("select ENTITLEMENT_XML from "+str(ObjectName)+" (nolock)  where  "+str(where)+"")		
# 		Product.SetGlobal("previous_entitlement_xml", previous_entitlement_xml.ENTITLEMENT_XML)
# 		## set entitlement_xml for cancel fn A055S000P01-3157 ends
# 		list_of_tabs = []
# 		getprevdicts +=   ("var dict_new = {};var list_new = [];")

# 		for product_tab_obj in product_tabs_obj:
# 			tablistdict = {}
# 			date_boot_field = []
# 			list_of_tabs.append(product_tab_obj.TAB_NAME)

# 			sysectObj = Sql.GetFirst(
# 			"SELECT RECORD_ID,SECTION_DESC,SECTION_NAME FROM SYSECT (NOLOCK) WHERE SECTION_NAME='" + str(product_tab_obj.TAB_NAME) + "'"
# 			)
# 			if sysectObj and str(sysectObj.SECTION_NAME) == str(product_tab_obj.TAB_NAME):
# 				Section_id = sysectObj.RECORD_ID
# 				Section_desc = sysectObj.SECTION_DESC
# 			else:
# 				get_last_secid = Sql.GetFirst("select max(SAPCPQ_ATTRIBUTE_NAME) as saprec_id from sysect where SAPCPQ_ATTRIBUTE_NAME like '%SYSECT-QT%'")
# 				if get_last_secid:
# 					get_last_secid = get_last_secid.saprec_id.split('-')[2]
# 					get_last_secid = int(int(get_last_secid)) + 1
# 					get_lastsection_val = 'SYSECT-QT-'+ str(get_last_secid)
# 					getsect_tab = SqlHelper.GetTable("SYSECT")
# 					tbrowsect = {}
# 					Section_id = tbrowsect['RECORD_ID'] = str(Guid.NewGuid()).upper()
# 					tbrowsect['SAPCPQ_ATTRIBUTE_NAME'] = get_lastsection_val
# 					Section_desc = tbrowsect['SECTION_DESC'] =  str(product_tab_obj.TAB_NAME) 
# 					tbrowsect['SECTION_NAME'] =  str(product_tab_obj.TAB_NAME)
# 					tbrowsect['SECTION_PARTNUMBER'] =  TreeParam.upper()
# 					getsect_tab.AddRow(tbrowsect)
# 					Sql.Upsert(getsect_tab)

# 			if EntitlementType == "EQUIPMENT" or EntitlementType == "BUSINESSUNIT" or EntitlementType == "TOOLS":
					
# 				sec_bnr += (
# 					'<div class="dyn_main_head master_manufac glyphicon pointer  glyphicon-chevron-down" id="'
# 					+ str(Section_id)+ '" onclick="dyn_main_sec_collapse_arrow(this)" data-target="#sec_'
# 					+ str(Section_id)
# 					+ '" data-toggle="collapse"><label class="onlytext"><label class="onlytext"><div><div id="ctr_drop" class="btn-group dropdown"><div class="dropdown"><i data-toggle="dropdown" class="fa fa-sort-desc dropdown-toggle"></i><ul class="dropdown-menu left" aria-labelledby="dropdownMenuButton"><li class="edit_list"><a id="'
# 					+ str(Section_id)
# 					+ '" class="dropdown-item" href="#" onclick="edit_entitlement(this)">EDIT</a></li></ul></div></div>'
# 					+ str(Section_desc)
# 					+ "</div></label></div>"
# 				)
			
				
# 			else:
				
# 				sec_bnr += (
# 					'<div class="dyn_main_head master_manufac glyphicon pointer   glyphicon-chevron-down" onclick="dyn_main_sec_collapse_arrow(this)" id="'+ str(Section_id)+ '" data-target="#sec_'
# 					+ str(Section_id)
# 					+ '" data-toggle="collapse"><label class="onlytext"><label class="onlytext"><div>'
# 					+ str(Section_desc)
# 					+ "</div></label></div>"
# 				)
# 			sec_str_boot += ('<div id="sec_'+str(Section_id)+ '" class="dyn_main_head master_manufac glyphicon pointer   glyphicon-chevron-down margtop10" onclick="dyn_main_sec_collapse_arrow(this)" data-target="#sc_'+ str(Section_id)+ '" data-toggle="collapse" <label class="onlytext"><label class="onlytext"><div>'+ str(Section_desc).upper()+ '</div></label></div><div id="sc_'+str(Section_id)+ '" class="collapse in "><table id="' + str(Section_id)+ '" class= "getentdata" data-filter-control="true" data-maintain-selected="true" data-locale = "en-US" data-escape="true" data-html="true"  data-show-header="true" > <thead><tr class="hovergrey">')
# 			for key, invs in enumerate(list(desc_list)):
# 				invs = str(invs).strip()
# 				qstring = attr_dict.get(str(invs)) or ""
# 				sec_str_boot += (
# 					'<th data-field="'
# 					+ invs
# 					+ '" data-title-tooltip="'
# 					+ str(qstring)
# 					+ '" >'
# 					+ str(qstring)
# 					+ "</th>"
# 				)
# 			sec_str_boot += '</tr></thead><tbody onclick="Table_Onclick_Scroll(this)" ></tbody></table>'
# 			sec_str_boot += ('<div id = "btn_ent" class="g4  except_sec removeHorLine iconhvr sec_edit_sty" style="display: none;"><button id="entcancel" class="btnconfig btnMainBanner sec_edit_sty_btn"  onclick="fabcostlocatecancel(this)" style="display: none;" class="btnconfig">CANCEL</button><button id="entsave" class="btnconfig btnMainBanner sec_edit_sty_btn"  onclick="fabcostlocatesave(this)" style="display: none;" class="btnconfig">SAVE</button></div>')

# 			add_style = ""
# 			attributes_disallowed_list = []
# 			attribute_Name_list = []
# 			attribute_Name_list = []
# 			if tabwise_product_attributes.get(product_tab_obj.TAB_PROD_ID):
# 				for attribute in tabwise_product_attributes.get(product_tab_obj.TAB_PROD_ID):
# 					new_value_dicta = {}
# 					attrName = attribute['attribute_name']
# 					attrLabel = attribute['attribute_label']
# 					attrSysId = attribute['attribute_system_id']
# 					STDVALUES =  Sql.GetFirst("SELECT STANDARD_ATTRIBUTE_VALUE from STANDARD_ATTRIBUTE_VALUES  where  SYSTEM_ID like '%{sys_id}%' ".format(sys_id = attrSysId)  )
# 					if STDVALUES:
# 						attrValue = STDVALUES.STANDARD_ATTRIBUTE_VALUE
# 					else:
# 						attrValue = ''
					
# 					attribute_Name_list.append(attrSysId)
# 					DType = attribute['attribute_dtype']

# 					if attrSysId in attributesdisallowedlst:
# 						add_style = "display:none"
# 						attributes_disallowed_list.append(attrSysId)
# 					else:
# 						add_style = ""	
# 					if attrSysId in attributeEditlst :
# 						edit_pencil_icon = '<i class="fa fa-pencil" aria-hidden="true"></i>'
						
# 					else:
# 						edit_pencil_icon = '<i class="fa fa-lock" aria-hidden="true"></i>'
# 					attrValueSysId = attributevalues.get(attrSysId)
				
# 					disp_val = ""
# 					userselectedvalue = []
# 					#for val in GetXMLsecField:
# 					getnameentallowed = []

# 					sec_str_cf =sec_str_imt =  dataent = factcurreny = decimal_place = value1234 = sec_str_dt = sec_str_faccur = sec_str_faccur = costimpact = sec_str_primp = priceimp =  sec_str_ipp = ""
# 					if GetXMLsecField:
						
# 						for val in GetXMLsecField:
# 							userselectedvalue.append(val.ENTITLEMENT_DESCRIPTION)
# 							getnameentallowed.append(val.ENTITLEMENT_NAME)
# 							if  str(attrSysId) == val.ENTITLEMENT_NAME:
# 								disp_val = str(val.ENTITLEMENT_DISPLAY_VALUE)
# 								if val.ENTITLEMENT_TYPE in ("DropDown", "Drop Down") or val.ENTITLEMENT_TYPE in ("CheckBox", "Check Box"):
# 									VAR1 = sec_str1 = ""
# 									STDVALUES =  Sql.GetList("SELECT STANDARD_ATTRIBUTE_DISPLAY_VAL from STANDARD_ATTRIBUTE_VALUES where  SYSTEM_ID like '%{sys_id}%' ".format(sys_id = str(attrSysId) )  )
# 									if STDVALUES:
# 										for value in STDVALUES:
											
# 											if str(val.ENTITLEMENT_DISPLAY_VALUE).strip() == str(value.STANDARD_ATTRIBUTE_DISPLAY_VAL).strip():
# 												VAR1 += (
# 														'<option  id="'+str(attrSysId)+'" value = "'
# 														+ str(val.ENTITLEMENT_DISPLAY_VALUE)
# 														+ '" selected>'
# 														+ str(val.ENTITLEMENT_DISPLAY_VALUE)
# 														+ "</option>"
# 												)
# 											else:
# 												VAR1 += (
# 													'<option  id="'+str(attrSysId)+'" value = "'
# 													+ str(value.STANDARD_ATTRIBUTE_DISPLAY_VAL)
# 													+ '">'
# 													+ str(value.STANDARD_ATTRIBUTE_DISPLAY_VAL)
# 													+ "</option>"
# 												)
# 									sec_str1 += (
# 										'<select class="form-control remove_yellow" style ="'+str(add_style)+'" id = "'
# 										+ str(attrSysId)
# 										+ '" type="text"  data-content ="'
# 										+ str(attrSysId)
# 										+ '" class="form-control" onchange="editent_bt(this)" disabled>'
# 										+ str(VAR1)
# 										+ "</select>"
# 									)
# 								elif DType == "FreeInputNoMatching":
# 									STDVALUES =  Sql.GetFirst("SELECT STANDARD_ATTRIBUTE_VALUE from STANDARD_ATTRIBUTE_VALUES  where  SYSTEM_ID like '%{sys_id}%' ".format(sys_id = str(attrSysId))  )							
# 									sec_str1 = ""
# 									sec_str1 += (
# 										'<input class="form-control" id = "'
# 										+ str(attrSysId)
# 										+ '" type="text"  data-content ="'
# 										+ str(attrSysId)
# 										+ '"  disabled>'
# 										+ "</input>"
# 									)
								
# 								else:										
# 									sec_str_ipp = ""
# 									sec_str_ipp = ('<input class="form-control no_border_bg" id = "'
# 										+ str(attrSysId)
# 										+ '" type="text"  data-content ="'
# 										+ str(attrValueSysId)
# 										+ '" value = "'+str(val.ENTITLEMENT_DISPLAY_VALUE)+'" style ="'+str(add_style)+'"  onclick="editent_bt(this)" disabled>'									
# 										+ "</input>"
# 									)
							
# 							if (str(val.ENTITLEMENT_DESCRIPTION) == "Addl Perf Guarantee 2" and str(val.ENTITLEMENT_VALUE_CODE).upper()== "MANUAL_INPUT"):
								
# 								imgstr = ('<img title=Acquired src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/clock_exe.svg>')
# 							else:
# 								imgstr  = ""
# 							new_value_dicta["APPROVAL"] = imgstr	
# 							new_value_dicta["ENTITLEMENT DESCRIPTION"] = str(attrName)
# 							#Trace.Write("=============MMMMM "+str(sec_str1))
# 							if DType in ("DropDown", "Drop Down") or DType in ("CheckBox", "Check Box"):
# 								new_value_dicta["ENTITLEMENT VALUE"] =  sec_str1
# 							else:
# 								new_value_dicta["ENTITLEMENT VALUE"] =  sec_str_ipp
# 							#new_value_dicta["FACTOR CURRENCY"] = sec_str_faccur
# 							new_value_dicta["ENTITLEMENT COST IMPACT"]= sec_str_imt
# 							#new_value_dicta["DATA TYPE"] = sec_str_dt
# 							new_value_dicta["ENTITLEMENT PRICE IMPACT"]= sec_str_primp
# 							new_value_dicta["CALCULATION FACTOR"] = sec_str_cf
# 					totaldisallowlist = [item for item in attributesdisallowedlst if item not in getnameentallowed]
				
# 					if  str(attrLabel) not in userselectedvalue and len(userselectedvalue) > 0:							
# 						if attrSysId in attributesdisallowedlst:						
# 							#attributes_disallowed_list.append(attrSysId)
# 							add_style = "display:none"
# 						else:
# 							add_style = ""
# 						if DType == "FreeInputNoMatching":
# 							sec_str1 = ""
							
# 							sec_str1 += (
# 								'<input class="form-control no_border_bg" id = "'
# 								+ str(attrSysId)
# 								+ '" type="text"  style ="'+str(add_style)+'"  data-content ="'
# 								+ str(attrValueSysId)
# 								+ '" value = "" onchange="editent_bt(this)" >'									
# 								+ "</input>"
# 							)
# 						elif DType == "CheckBox":				
# 							VAR1 = sec_str1 = ""
# 							STDVALUES =  Sql.GetList("SELECT STANDARD_ATTRIBUTE_DISPLAY_VAL from STANDARD_ATTRIBUTE_VALUES where  SYSTEM_ID like '%{sys_id}%' ".format(sys_id = str(attrSysId) )  )
# 							if STDVALUES:
# 								for value in STDVALUES:
# 									if str(val.ENTITLEMENT_DISPLAY_VALUE).strip() == str(value.STANDARD_ATTRIBUTE_VALUE).strip():
# 										VAR1 += (
# 												'<option  id='+str(attrSysId)+' value = "'
# 												+ str(val.ENTITLEMENT_DISPLAY_VALUE)
# 												+ '" selected>'
# 												+ str(val.ENTITLEMENT_DISPLAY_VALUE)
# 												+ "</option>"
# 										)
# 									else:
# 										VAR1 += (
# 											'<option  id="'+str(attrSysId)+'" value = "'
# 											+ str(value.STANDARD_ATTRIBUTE_DISPLAY_VAL)
# 											+ '">'
# 											+ str(value.STANDARD_ATTRIBUTE_DISPLAY_VAL)
# 											+ "</option>"
# 										)
# 							sec_str1 += (
# 								'<select class="form-control remove_yellow" style ="'+str(add_style)+'" id = "'
# 								+ str(attrSysId)
# 								+ '" type="text"  data-content ="'
# 								+ str(attrSysId)
# 								+ '" class="form-control" onchange="editent_bt(this)" disabled>'
# 								+ str(VAR1)
# 								+ "</select>"
# 							)
						
# 						new_value_dicta["APPROVAL"] = ""	
# 						new_value_dicta["ENTITLEMENT DESCRIPTION"] = str(attrName)
# 						if DType == "Drop Down" or DType == "CheckBox" or DType == "FreeInputNoMatching":
# 							new_value_dicta["ENTITLEMENT VALUE"] =  sec_str1
# 						else:
# 							new_value_dicta["ENTITLEMENT VALUE"] =  attrValue
# 						#new_value_dicta["FACTOR CURRENCY"] = sec_str_faccur
# 						new_value_dicta["ENTITLEMENT COST IMPACT"]= sec_str_imt
# 						#new_value_dicta["DATA TYPE"] = sec_str_dt
# 						new_value_dicta["ENTITLEMENT PRICE IMPACT"]= ""
# 						new_value_dicta["CALCULATION FACTOR"] = sec_str_cf
# 					if new_value_dicta:
# 						date_boot_field.append(new_value_dicta)
				

# 				tablistdict[Section_id] = date_boot_field					
# 				if len(tablistdict) > 0:
# 					tablistnew.append(tablistdict)
# 			Product.SetGlobal('ent_data_List',str(tablistnew))					
# 			table_ids = '#'+Section_id
# 			getdivid = '#sc_'+Section_id+' .sec_edit_sty'
# 			getdividbtn = '#sc_'+Section_id+' #btn_ent .sec_edit_sty_btn'
			
# 			sec_str_boot += ('</div>')
# 			##section hide starts..					
# 			if len(attribute_Name_list) == len(attributes_disallowed_list):
# 				section_not_list.append('sec_'+Section_id)
				
# 			##section hide ends...
# 			#getprevdicts +=   ("try{var dict_new = {};$('"+str(table_ids)+" tbody tr td select').each(function () {dict_new[$(this).find('td:nth-child(3) select').attr('id')] = $(this).children(':selected').val();});$('"+str(table_ids)+" tbody tr td input').each(function () {if($(this).attr('id') != 'T0_T1_LABOR_calc'){dict_new[$(this).find('td:nth-child(3) input').attr('id')] =  $(this).find('td:nth-child(3) input').val();}});console.log('dict_new-2796--',dict_new);localStorage.setItem('prventdict', JSON.stringify(dict_new))}catch{console.log('')}")
# 			#getprevdicts +=   ("try{var dict_new = {};$('"+str(table_ids)+" tbody tr:visible').each(function () {dict_new[$(this).find('td:nth-child(3) select').attr('id')] = $(this).find('td:nth-child(3) select').children(':selected').val() ;});$('"+str(table_ids)+" tbody tr:visible').each(function () {dict_new[$(this).find('td:nth-child(3) input').attr('id')] =  $(this).find('td:nth-child(3) input').val();});console.log('dict_new-2796--',dict_new);localStorage.setItem('prventdict', JSON.stringify(dict_new))}catch{console.log('')}")
# 			if (TreeParentParam == "Quote Items" or TreeSuperParentParam == "Quote Items" or TreeTopSuperParentParam == "Quote Items"):
# 				dbl_clk_function = ""
# 			else:
# 				#dbl_clk_function += ("try{var dict_new = {};$('"+str(table_ids)+" tbody tr:visible').each(function () {dict_new[$(this).find('td:nth-child(3) select').attr('id')] =  $(this).find('td:nth-child(3) select').children(':selected').attr('id');});$('"+str(table_ids)+" tbody tr:visible').each(function () {dict_new[$(this).find('td:nth-child(3) input').attr('id')] =  $(this).find('td:nth-child(3) input').val();});console.log('dict_new-2818--',dict_new);localStorage.setItem('prventdict', JSON.stringify(dict_new))}catch{console.log('')}")
# 				dbl_clk_function +=   ("try{var dict_new = {};$('"+str(table_ids)+"').on('dbl-click-cell.bs.table', function (e, row, $element) { $('"+str(table_ids)+" tbody tr:visible').each(function () {dict_new[$(this).find('td:nth-child(3) select').attr('id')] =$(this).find('td:nth-child(3) select').children(':selected').val() ;});$('"+str(table_ids)+" tbody tr:visible').each(function () {dict_new[$(this).find('td:nth-child(3) input').attr('id')] =  $(this).find('td:nth-child(3) input').val();});console.log('dblclk_dict_new-28001--',dict_new);localStorage.setItem('prventdict', JSON.stringify(dict_new))})}catch{console.log('')}")
# 				#dbl_clk_function +=   ("try{var dict_new = {};$('"+str(table_ids)+"').on('dbl-click-cell.bs.table', function (e, row, $element) { $('"+str(table_ids)+" tbody tr td select').each(function () {dict_new[$(this).attr('id')] = $(this).children(':selected').val();});$('"+str(table_ids)+" tbody tr td input').each(function () {dict_new[$(this).attr('id')] = $(this).val();});console.log('dblclk_dict_new-2800--',dict_new);localStorage.setItem('prventdict', JSON.stringify(dict_new))})}catch{console.log('')}")
# 				dbl_clk_function += (
# 					"try { var newentdict =[]; var newentValues =[]; var getentedictip = [];$('"+str(table_ids)+"').on('dbl-click-cell.bs.table', function (e, row, $element) {if(localStorage.getItem('EDITENT_SEC') != 'EDIT'){console.log('tset--prev value--23001-',this.value);localStorage.setItem('EDITENT_SEC','EDIT');$('"+str(getdivid)+"').css('display','block');$('"+str(getdividbtn)+"').css('display','block');$('#entsave').css('display','block');$('#entcancel').css('display','block'); $('"+str(table_ids)+"').find(':input(:disabled)').prop('disabled', false);$('#sc_'+'"+str(Section_id)+"').addClass('header_section_div header_section_div_pad_bt10');$('"+str(table_ids)+" tbody tr td:nth-child(5) input').removeClass('light_yellow').addClass('remove_yellow');$('"+str(table_ids)+" tbody tr td:nth-child(5) input').attr('disabled', 'disabled');$('"+str(table_ids)+" tbody tr td:nth-child(4) input').attr('disabled', 'disabled');$('"+str(table_ids)+" tbody tr td:nth-child(6) input').removeClass('light_yellow').addClass('remove_yellow');$('"+str(table_ids)+" tbody tr td:nth-child(7) input').removeClass('light_yellow').addClass('remove_yellow');$('"+str(table_ids)+"  tbody tr td:nth-child(7) input').attr('disabled', 'disabled');$('"+str(table_ids)+"  tbody tr td:nth-child(8) input').attr('disabled', 'disabled');$('"+str(table_ids)+"  tbody tr td:nth-child(6) input').attr('disabled', 'disabled');$('#T2_LABOR_TYPE_calc').removeAttr('disabled');$('#T3_LABOR_TYPE_calc').removeAttr('disabled');$('#LABOR_TYPE_calc').removeAttr('disabled');$('#T0_T1_LABOR_TYPE_calc').removeAttr('disabled');$('"+str(table_ids)+" tbody tr td:nth-child(8) input').removeClass('light_yellow').addClass('remove_yellow');$('"+str(table_ids)+" tbody tr td:nth-child(4) input').removeClass('light_yellow').addClass('remove_yellow');var testperf = $('#ADDL_PERF_GUARANTEE_91_1').val();console.log('testperf-----',testperf);if(testperf.toUpperCase() == 'MANUAL INPUT'){console.log('manual input val on donble click---');$('#ADDL_PERF_GUARANTEE_91_1_imt').removeAttr('disabled');$('#ADDL_PERF_GUARANTEE_91_1_imt').parent().css('position', 'relative');$('#ADDL_PERF_GUARANTEE_91_1_primp').parent().css('position', 'relative');$('#ADDL_PERF_GUARANTEE_91_1_primp').removeAttr('disabled');}else{$('#ADDL_PERF_GUARANTEE_91_1_imt').removeClass('light_yellow')};$('#ADDL_PERF_GUARANTEE_91_1_dt').attr('disabled', 'disabled');$('#ADDL_PERF_GUARANTEE_91_1_calc').attr('disabled', 'disabled');$('input').on('focus', function () {var previnp = $(this).data('val', $(this).val());$('#ADDL_PERF_GUARANTEE_91_1_primp').removeAttr('disabled');console.log('manual input----');var getprevid = this.id;var prev_concate_data = getprevid +'='+previnp;}).change(function() {var prev = $(this).data('val');var current = $(this).val();var getseltabledesc = this.id;var getinputtbleid =  $(this).closest('table').attr('id');var concated_data = getinputtbleid+'|'+current+'|'+getseltabledesc;if(!getentedictip.includes(concated_data)){getentedictip.push(concated_data)};getentedictip1 = JSON.stringify(getentedictip);localStorage.setItem('getdictentdata', getentedictip1);});}})}catch {console.log('error---')}"
# 				)
				
# 	date_field = ""
# 	new_value_dict = ""
# 	api_name = ""
# 	ret_value = ""
# 	# ObjectName="CTCTSE"
# 	sec_bnr = ""
# 	return sec_str, date_field, new_value_dict, api_name, ret_value, ObjectName, sec_bnr,sec_str_boot,tablistnew

if hasattr(Param, "RECORD_ID"):
	RECORD_ID = Param.RECORD_ID
else:
	RECORD_ID =""
#RECORD_ID = Param.RECORD_ID

try:
	AllTreeParam = Param.AllTreeParams
	AllTreeParam = eval(AllTreeParam)
	TreeParam = AllTreeParam["TreeParam"]
	

	try:
		TreeParentParam = AllTreeParam["TreeParentLevel0"]
	except:
		TreeParentParam = ""
	try:
		TreeSuperParentParam = AllTreeParam["TreeParentLevel1"]
	except:
		TreeSuperParentParam = ""
	try:
		TreeTopSuperParentParam = AllTreeParam["TreeParentLevel2"]
	except:
		TreeTopSuperParentParam = ""
	try:
		TreeSuperTopParentParam = AllTreeParam["TreeParentLevel3"]
	except:
		TreeSuperTopParentParam = ""
	try:
		TreeTopSuperTopParentParam = AllTreeParam["TreeParentLevel4"]
	except:
		TreeTopSuperTopParentParam = ""
	
except:
	Trace.Write("inside except")
	try:
		TreeParam = Param.TreeParam
	except:
		TreeParam = ""
	try:
		TreeParentParam = Param.TreeParentParam
	except:
		TreeParentParam = ""
	try:
		TreeSuperParentParam = Param.TreeSuperParentParam
	except:
		TreeSuperParentParam = ""
	try:
		TreeTopSuperParentParam = Param.TreeTopSuperParentParam
	except:
		TreeTopSuperParentParam = ""


NEWVAL = Param.NEWVAL
LOOKUPOBJ = Param.LOOKUPOBJ
LOOKUPAPI = Param.LOOKUPAPI
MODE = Param.MODE
TreeSuperParentParam = Product.GetGlobal("TreeParentLevel1")
TreeParam = Product.GetGlobal("TreeParam")
TreeParentParam = Product.GetGlobal("TreeParentLevel0")
TreeTopSuperParentParam = Product.GetGlobal("TreeParentLevel2")
try:
	quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
except:
	Trace.Write("EXCEPT: quote_revision_record_id ")
	quote_revision_record_id = ""

if hasattr(Param, "TableId"):
	TableId = Param.TableId
	Product.SetGlobal("TableId", str(TableId))    
elif TreeParentParam == "Quote Items":
	TableId = "SYOBJR-00008"
	Product.SetGlobal("TableId", str(TableId)) 	  
else:
	TableId = ""
SECTION_EDIT = ""
Trace.Write(str(TableId))

try:
	TreeSuperTopParentParam = Param.TreeSuperTopParentParam
except:
	TreeSuperTopParentParam = ""

if hasattr(Param, "TreeFirstSuperTopParentParam"):
	TreeFirstSuperTopParentParam = Param.TreeFirstSuperTopParentParam
	Product.SetGlobal("TreeFirstSuperTopParentParam", str(TreeFirstSuperTopParentParam))
else:
	TreeFirstSuperTopParentParam = ""

if MODE == "EDIT":
	SECTION_EDIT = Param.SECTION_EDIT


try:
	Flag = Param.Flag
except:
	Flag = 0

try:
	ObjectName = Param.ObjName
except:
	ObjectName = None
try:
	LEGALSOW= Param.LEGALSOW
except:
	LEGALSOW = ''
try:
	SectionList = Param.DetailList
except:
	SectionList = ""
try:
	SubtabName = Param.SubtabName
	Trace.Write("SubtabName==="+str(SubtabName))
except:
	SubtabName = ""
try:
	EquipmentId = Param.EquipmentId
except:
	EquipmentId = ""
try:
	AssemblyId = Param.AssemblyId
except:
	AssemblyId = ""


if (TreeParam.startswith("Sending") or TreeParam.startswith("Receiving")):
	ObjectName = "SAQSRA"
	
#Trace.Write("OBJ" + str(ObjectName))

# if SectionList is not None and (
# 	"CE171F61-B09E-4E4F-8161-1036A062B205" in SectionList
# 	or "68C30A98-154E-436F-B4E5-73D8186DB68D" in SectionList
# 	or "68855FCB-F4D7-4641-93AB-B515A41F29E2" in SectionList
# 	or "0EF8591C-4B5A-4EC2-863F-F8229B5FA025" in SectionList
# 	or "DF5F6D00-989C-4EDB-BB15-2D350B5F5753" in SectionList
# 	or "9020F322-C390-4CDC-AD77-ADCE87566815" in SectionList
# 	or "1F2C9353-3E51-4D1D-8C99-D88FDCED4838" in SectionList
# 	or "C50B4387-AEBB-4D10-B470-67034C15C44F" in SectionList
# 	or "F8C12B12-6C91-4838-8BE9-015034ED21C8" in SectionList
# 	or "36F74B1C-91FD-44BD-BE72-64D5068F9BDB" in SectionList
# 	or "2D2E0F0C-6013-4073-8F8B-B0D12DE6CECF" in SectionList
# 	or "0EF8591C-4B5A-4EC2-863F-F8229B5FA025" in SectionList
# 	or "484F3029-7844-4DE7-BBB4-535A7BAE476E" in SectionList
# ):
# 	Trace.Write("SectionList111")

# 	sectionId = tuple(SectionList)
# 	sectObj = Sql.GetFirst("SELECT PRIMARY_OBJECT_NAME FROM SYSECT (NOLOCK) WHERE RECORD_ID IN " + str(sectionId) + "")
# 	#result = ScriptExecutor.ExecuteGlobal("CQENTLVIEW", {"action": 'ENT_VIEW','alltreeparam':AllTreeParam})
# 	if sectObj is not None:
# 		SectionObjectName = sectObj.PRIMARY_OBJECT_NAME		
# 		if SectionObjectName in ("SAQTSE"):
# 			# ObjectName=SectionObjectName
# 			EntitlementType = "EQUIPMENT"
# 			ApiResponse = ApiResponseFactory.JsonResponse(
# 				EntitlementTreeViewHTMLDetail(
# 					MODE,
# 					TableId,
# 					RECORD_ID,
# 					TreeParam,
# 					NEWVAL,
# 					LOOKUPOBJ,
# 					LOOKUPAPI,					
# 					SECTION_EDIT,					
# 					Flag,
# 					TreeParentParam,
# 					SectionObjectName,
# 					SectionList,
# 					EntitlementType,
# 				)
# 			)
# 		elif SectionObjectName in ("CTCTSE"):
# 				# ObjectName=SectionObjectName			
# 			EntitlementType = "EQUIPMENT"
# 			ApiResponse = ApiResponseFactory.JsonResponse(
# 				ContractEntitlementTreeViewHTMLDetail(
# 					MODE,
# 					TableId,
# 					RECORD_ID,
# 					TreeParam,
# 					NEWVAL,
# 					LOOKUPOBJ,
# 					LOOKUPAPI,					
# 					SECTION_EDIT,					
# 					Flag,
# 					TreeParentParam,
# 					SectionObjectName,
# 					SectionList,
# 					EntitlementType,
# 				)
# 			)
# 		elif SectionObjectName in ("CTCIEN"):    		
# 			ApiResponse = ApiResponseFactory.JsonResponse(
# 				ContractEntitlementTreeViewHTMLDetail(
# 					MODE,
# 					TableId,
# 					RECORD_ID,
# 					TreeParam,
# 					NEWVAL,
# 					LOOKUPOBJ,
# 					LOOKUPAPI,					
# 					SECTION_EDIT,					
# 					Flag,
# 					TreeParentParam,
# 					SectionObjectName,
# 					SectionList,
# 					"ITEMGREENBOOK"
# 				)
# 			)
# 		elif SectionObjectName in ("SAQIEN"):
# 			TreeParentParam = Product.GetGlobal("TreeParentLevel0")			
# 			if TreeParentParam == 'Quote Items':
# 				EntitlementType = "ITEMSPARE"
# 			elif TreeTopSuperParentParam == 'Quote Items' and SubtabName == 'Equipment Entitlements':
# 				EntitlementType = "ITEMS"
# 			elif TreeTopSuperParentParam == 'Quote Items' and SubtabName == 'Entitlements':
# 				EntitlementType = "ITEMGREENBOOK"				
# 			ApiResponse = ApiResponseFactory.JsonResponse(
# 				EntitlementTreeViewHTMLDetail(
# 					MODE,
# 					TableId,
# 					RECORD_ID,
# 					TreeParam,
# 					NEWVAL,
# 					LOOKUPOBJ,
# 					LOOKUPAPI,
# 					SECTION_EDIT,					
# 					Flag,
# 					TreeParentParam,
# 					SectionObjectName,
# 					SectionList,
# 					EntitlementType,
# 				)
# 			)
# 		elif SectionObjectName in ("SAQSGE"):			
# 			ApiResponse = ApiResponseFactory.JsonResponse(
# 				EntitlementTreeViewHTMLDetail(
# 					MODE,
# 					TableId,
# 					RECORD_ID,
# 					TreeParam,
# 					NEWVAL,
# 					LOOKUPOBJ,
# 					LOOKUPAPI,
# 					SECTION_EDIT,					
# 					Flag,
# 					TreeParentParam,
# 					SectionObjectName,
# 					SectionList,
# 					"BUSINESSUNIT",
# 				)
# 			)
# 		elif SectionObjectName in ("CTCSGE"):			
# 			ApiResponse = ApiResponseFactory.JsonResponse(
# 				ContractEntitlementTreeViewHTMLDetail(
# 					MODE,
# 					TableId,
# 					RECORD_ID,
# 					TreeParam,
# 					NEWVAL,
# 					LOOKUPOBJ,
# 					LOOKUPAPI,
# 					SECTION_EDIT,					
# 					Flag,
# 					TreeParentParam,
# 					SectionObjectName,
# 					SectionList,
# 					"BUSINESSUNIT",
# 				)
# 			)
# 		elif SectionObjectName in ("SAQSFE"):			
# 			ApiResponse = ApiResponseFactory.JsonResponse(
# 				EntitlementTreeViewHTMLDetail(
# 					MODE,
# 					TableId,
# 					RECORD_ID,
# 					TreeParam,
# 					NEWVAL,
# 					LOOKUPOBJ,
# 					LOOKUPAPI,
# 					SECTION_EDIT,					
# 					Flag,
# 					TreeParentParam,
# 					SectionObjectName,
# 					SectionList,
# 					"FABLOCATION",
# 				)
# 			)
# 		elif SectionObjectName in ("SAQSCE"):			
# 			ApiResponse = ApiResponseFactory.JsonResponse(
# 				EntitlementTreeViewHTMLDetail(
# 					MODE,
# 					TableId,
# 					RECORD_ID,
# 					TreeParam,
# 					NEWVAL,
# 					LOOKUPOBJ,
# 					LOOKUPAPI,
# 					SECTION_EDIT,					
# 					Flag,
# 					TreeParentParam,
# 					SectionObjectName,
# 					SectionList,
# 					"TOOLS",
# 				)
# 			)
# 		elif SectionObjectName in ("CTCSCE"):			
# 			ApiResponse = ApiResponseFactory.JsonResponse(
# 				ContractEntitlementTreeViewHTMLDetail(
# 					MODE,
# 					TableId,
# 					RECORD_ID,
# 					TreeParam,
# 					NEWVAL,
# 					LOOKUPOBJ,
# 					LOOKUPAPI,
# 					SECTION_EDIT,					
# 					Flag,
# 					TreeParentParam,
# 					SectionObjectName,
# 					SectionList,
# 					"ITEMGREENBOOK",
# 				)
# 			)
# 		elif SectionObjectName in ("SAQSAE"):			
# 			ApiResponse = ApiResponseFactory.JsonResponse(
# 				EntitlementTreeViewHTMLDetail(
# 					MODE,
# 					TableId,
# 					RECORD_ID,
# 					TreeParam,
# 					NEWVAL,
# 					LOOKUPOBJ,
# 					LOOKUPAPI,
# 					SECTION_EDIT,					
# 					Flag,
# 					TreeParentParam,
# 					SectionObjectName,
# 					SectionList,
# 					"ASSEMBLY",
# 				)
# 			)
# elif ObjectName == "SAQTSE":	
# 	ApiResponse = ApiResponseFactory.JsonResponse(
# 		EntitlementTreeViewHTMLDetail(
# 			MODE,
# 			TableId,
# 			RECORD_ID,
# 			TreeParam,
# 			NEWVAL,
# 			LOOKUPOBJ,
# 			LOOKUPAPI,
# 			SECTION_EDIT,			
# 			Flag,
# 			TreeParentParam,
# 			ObjectName,
# 			SectionList,
# 			"TOOLS",
# 		)
# 	)
# elif ObjectName == "CTCTSE":	
# 	ApiResponse = ApiResponseFactory.JsonResponse(
# 		ContractEntitlementTreeViewHTMLDetail(
# 			MODE,
# 			TableId,
# 			RECORD_ID,
# 			TreeParam,
# 			NEWVAL,
# 			LOOKUPOBJ,
# 			LOOKUPAPI,
# 			SECTION_EDIT,			
# 			Flag,
# 			TreeParentParam,
# 			ObjectName,
# 			SectionList,
# 			"TOOLS",
# 		)
# 	)

if MODE == "BREADCRUMB":
	REC_ID = Param.REC_ID
	ApiResponse = ApiResponseFactory.JsonResponse(UpdateBreadcrumb(REC_ID))
# elif ((SubtabName in ('Entitlements','Equipment Entitlements','Assembly Entitlements') ) and (TreeParam.upper() == "SENDING EQUIPMENT" or TreeSuperParentParam.upper() =="SENDING EQUIPMENT" or TreeParentParam.upper() =="SENDING EQUIPMENT")):
# 		Trace.Write("Entitlements"+str(TreeParam))
# 		#if TreeParam.upper() == "SENDING EQUIPMENT":
# 		EntitlementType = "SENDING_LEVEL"
# 		SectionObjectName = "SAQSRA"
# 		# elif TreeParam.upper() == "RECEIVING EQUIPMENT":
# 		# 	EntitlementType = "EQUIPMENT"
# 		# 	SectionObjectName = "SAQTSE"
# 		ApiResponse = ApiResponseFactory.JsonResponse(
# 				EntitlementTreeViewHTMLDetail(
# 					MODE,
# 					TableId,
# 					RECORD_ID,
# 					TreeParam,
# 					NEWVAL,
# 					LOOKUPOBJ,
# 					LOOKUPAPI,					
# 					SECTION_EDIT,					
# 					Flag,
# 					TreeParentParam,
# 					SectionObjectName,
# 					SectionList,
# 					EntitlementType,
# 				)
# 			)	


else:
	# Trace.Write(
	# 	"COMMON_TREE_VIEW_HTML_DETAIL=====>MODE---->"
	# 	+ str(MODE)
	# 	+ "TableId  --->"
	# 	+ str(TableId)
	# 	+ "RECORD_ID  --->"
	# 	+ str(RECORD_ID)
	# 	+ "TreeParam  --->"
	# 	+ str(TreeParam)
	# 	+ "NEWVAL  --->"
	# 	+ str(NEWVAL)
	# 	+ "LOOKUPOBJ  --->"
	# 	+ str(LOOKUPOBJ)
	# 	+ "LOOKUPAPI  --->"
	# 	+ str(LOOKUPAPI)
	# 	+ "SECTION_EDIT  --->"
	# 	+ str(SECTION_EDIT)
	# 	+ "Flag  --->"
	# 	+ str(Flag)
	# 	+ "ObjectName  --->"
	# 	+ str(ObjectName)
	# 	+ "SectionList  --->"
	# 	+ str(SectionList)
	# )
	Trace.Write('else part---')
	Trace.Write('Section List-->'+str(SectionList))

	ApiResponse = ApiResponseFactory.JsonResponse(
		CommonTreeViewHTMLDetail(
			MODE, TableId, RECORD_ID, TreeParam, NEWVAL, LOOKUPOBJ, LOOKUPAPI, SECTION_EDIT, Flag, ObjectName, SectionList,LEGALSOW
		)
	)
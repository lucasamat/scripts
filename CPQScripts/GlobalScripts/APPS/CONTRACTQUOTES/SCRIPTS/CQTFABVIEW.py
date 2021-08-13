# =========================================================================================================================================
#   __script_name : CQTFABVIEW.PY
#   __script_description : THIS SCRIPT IS USED FOR LOADING FAB DRIVER DYNAMICALLY BASED ON PARAM.
#   __primary_author__ : DHURGA GOPALAKRISHNAN
#   __create_date : 18/12/2020
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct
import math
import SYCNGEGUID as CPQID
from SYDATABASE import SQL
import datetime
import CQVLDRIFLW
import CQTVLDRIFW
Sql = SQL()
TestProduct = Webcom.Configurator.Scripting.Test.TestProduct()
try:
	CurrentTabName = TestProduct.CurrentTab
except:
	CurrentTabName = "Quotes"
Qt_rec_id = Quote.GetGlobal("contract_quote_record_id")
userId = str(User.Id)
userName = str(User.UserName)
TreeParam = Product.GetGlobal("TreeParam")
TreeParentParam = Product.GetGlobal("TreeParentLevel0")
TreeSuperParentParam = Product.GetGlobal("TreeParentLevel1")
TreeTopSuperParentParam = Product.GetGlobal("TreeParentLevel2")


def fabview(ACTION,CurrentRecordId,subtab):	
	Trace.Write("THIS FUNCTION====fabview")
	Trace.Write("THIS FUNCTION====ACTION"+str(ACTION))
	Trace.Write("THIS FUNCTION====subtab"+str(subtab))
	Trace.Write("THIS FUNCTION====CurrentRecordId"+str(CurrentRecordId))
	sec_str1 = sec_str = ""
	dbl_clk_function = ""
	desc_list = ["VALUE DRIVER DESCRIPTION","VALUE DRIVER VALUE","VALUE DRIVER COEFFICIENT",]
	table_id = 'fabvaldrives'
	attr_dict = {"VALUE DRIVER DESCRIPTION": "VALUE DRIVER DESCRIPTION",
					"VALUE DRIVER VALUE": "VALUE DRIVER VALUE",
					"VALUE DRIVER COEFFICIENT": "VALUE DRIVER COEFFICIENT",
				}
	date_field = []
	if str(TreeSuperParentParam).upper() == "FAB LOCATIONS" or str(TreeTopSuperParentParam) == 'Quote Items':
		GetPRVLDR = Sql.GetList("SELECT DISTINCT VALUEDRIVER_ID,VALUEDRIVER_RECORD_ID FROM PRBUVD(NOLOCK) WHERE BUSINESSUNIT_ID ='"+str(TreeParam)+"' AND BUSINESSUNIT_VALUEDRIVER_RECORD_ID != '' ")
		#table_id = 'fabvaldrives'
	else:
		#table_id = 'fabvaluedrives'
		GetPRVLDR = Sql.GetList("SELECT DISTINCT VALUE_DRIVER_ID,VALUE_DRIVER_RECORD_ID,EDITABLE FROM PRVLDR(NOLOCK) WHERE VALUE_DRIVER_TYPE = 'FAB BASED SURVEY'")
	sec_str += ('<div id = "fabnotify">')
	sec_str += ('<table id="' + str(table_id)+ '" data-escape="true" data-html="true"  data-locale = "en-US"  > <thead><tr>')
	
	for key, invs in enumerate(list(desc_list)):
		invs = str(invs).strip()
		qstring = attr_dict.get(str(invs)) or ""
		sec_str += (
			'<th data-field="'
			+ invs
			+ '" data-title-tooltip="'
			+ str(qstring)
			+ '"  >'
			+ str(qstring)
			+ "</th>"
		)
	sec_str += '</tr></thead><tbody class ="app_id" ></tbody></table></div>'
	disable_edit = ''
	get_editable_list = []
	if GetPRVLDR:
		for qstn in GetPRVLDR:
			sec_str1 = sec_str_eff = ""
			VAR1 = coeffval = ""
			userselectedeffi = []
			
			if str(TreeSuperParentParam).upper() == "FAB LOCATIONS" or str(TreeTopSuperParentParam) == 'Quote Items':
				mastername = str(qstn.VALUEDRIVER_RECORD_ID)
				field_name = str(qstn.VALUEDRIVER_ID).replace("'", "''")
			else:
				mastername = str(qstn.VALUE_DRIVER_RECORD_ID)
				field_name = str(qstn.VALUE_DRIVER_ID).replace("'", "''")
			#sec_str += ('')
			new_value_dict = {}
			if str(TreeParam).upper() == "QUOTE INFORMATION":				
				GetDRIVNAME = Sql.GetList(
					"SELECT TOP 1000 VALUEDRIVER_VALUE_DESCRIPTION FROM PRVDVL(NOLOCK) WHERE  VALUEDRIVER_ID = '"
					+ str(field_name)
					+ "' AND VALUEDRIVER_RECORD_ID = '"
					+ str(mastername)
					+ "'"
				)
				selecter = Sql.GetList(
					"SELECT VALUEDRIVER_VALUE_DESCRIPTION,VALUEDRIVER_COEFFICIENT FROM SAQVDV(NOLOCK) WHERE QUOTE_RECORD_ID = '"
					+ str(Qt_rec_id)
					+ "' AND VALUEDRIVER_ID = '"
					+ str(field_name)
					+ "'"
				)
				userselected = []
				if selecter:
					userselected = [Valuedrivervalue.VALUEDRIVER_VALUE_DESCRIPTION for Valuedrivervalue in selecter]
					userselectedeffi = [Valuedrivereff.VALUEDRIVER_COEFFICIENT for Valuedrivereff in selecter if Valuedrivereff.VALUEDRIVER_COEFFICIENT]
				if GetDRIVNAME:
					for qstns in GetDRIVNAME:
						if qstn.EDITABLE:
							Trace.Write(str(qstn.EDITABLE)+'---102---if----'+str(field_name))
							disable_edit = 'disabled'
						else:
							Trace.Write(str(qstn.EDITABLE)+'---102----else---'+str(field_name))
							disable_edit = ''
						if qstns.VALUEDRIVER_VALUE_DESCRIPTION in userselected:
							VAR1 += (
								'<option value = "'
								+ str(qstns.VALUEDRIVER_VALUE_DESCRIPTION)
								+ '" selected>'
								+ str(qstns.VALUEDRIVER_VALUE_DESCRIPTION)
								+ "</option>"
							)
						else:
							VAR1 += (
								'<option value = "'
								+ str(qstns.VALUEDRIVER_VALUE_DESCRIPTION)
								+ '">'
								+ str(qstns.VALUEDRIVER_VALUE_DESCRIPTION)
								+ "</option>"
							)
					sec_str1 += (
						'<select class="form-control '+str(disable_edit)+'" id = "'
						+ str(field_name).replace(" ", "_")
						+ '" disabled><option value="Select">..Select</option>'
						+ str(VAR1)
						+ "</select>"
					)
			elif str(TreeParentParam).upper() == "FAB LOCATIONS" or str(TreeSuperParentParam) == 'Quote Items':
				GetDRIVNAME = SqlHelper.GetList(
						"SELECT TOP 1000 VALUEDRIVER_VALUE_DESCRIPTION,VALUEDRIVER_COEFFICIENT FROM PRVDVL(NOLOCK) WHERE  VALUEDRIVER_ID = '"
						+ str(field_name)
						+ "' AND VALUEDRIVER_RECORD_ID = '"
						+ str(mastername)
						+ "'"
					)
				selecter = Sql.GetList(
					"SELECT VALUEDRIVER_VALUEDESC,VALUEDRIVER_COEFFICIENT FROM SAQFDV(NOLOCK) WHERE QUOTE_RECORD_ID = '"
					+ str(Qt_rec_id)
					+ "' AND VALUEDRIVER_ID = '"
					+ str(field_name)
					+ "' AND FABLOCATION_ID = '"
					+ str(TreeParam)
					+ "'"
				)
				
				userselecteddrive = []
				
				if selecter:
					userselecteddrive = [Valuedrivervalue.VALUEDRIVER_VALUEDESC for Valuedrivervalue in selecter]
					userselectedeffi = [Valuedrivereff.VALUEDRIVER_COEFFICIENT for Valuedrivereff in selecter if Valuedrivereff.VALUEDRIVER_COEFFICIENT]

				
				for qstns in GetDRIVNAME:
					if qstns.VALUEDRIVER_VALUE_DESCRIPTION in userselecteddrive:
						VAR1 += (
							'<option  value = "'
							+ str(qstns.VALUEDRIVER_VALUE_DESCRIPTION)
							+ '" selected>'
							+ str(qstns.VALUEDRIVER_VALUE_DESCRIPTION)
							+ "</option>"
						)
					else:
						VAR1 += (
							'<option  value = "'
							+ str(qstns.VALUEDRIVER_VALUE_DESCRIPTION)
							+ '">'
							+ str(qstns.VALUEDRIVER_VALUE_DESCRIPTION)
							+ "</option>"
						)
					
				sec_str1 += (
					'<select class="form-control" id = "'
					+ str(field_name).replace(" ", "_")
					+ '" disabled><option value="Select">..Select</option>'
					+ str(VAR1)
					+ "</select>"
				)
			elif str(TreeSuperParentParam).upper() == "FAB LOCATIONS" or str(TreeTopSuperParentParam).upper() == "QUOTE ITEMS":				
				GetDRIVNAME = Sql.GetList(
					"SELECT TOP 1000 VALUEDRIVER_VALUE_DESCRIPTION,VALUEDRIVER_COEFFICIENT FROM PRBDVL(NOLOCK) WHERE  VALUEDRIVER_ID = '"
					+ str(field_name)
					+ "' AND VALUEDRIVER_RECORD_ID = '"
					+ str(mastername)
					+ "' AND BUSINESSUNIT_ID = '"
					+ str(TreeParam)
					+ "'"
				)
				selecter = Sql.GetFirst("SELECT VALUEDRIVER_VALUE_DESCRIPTION,VALUEDRIVER_COEFFICIENT FROM SAQFGV(NOLOCK) WHERE QUOTE_RECORD_ID = '"+ str(Qt_rec_id)+ "' AND VALUEDRIVER_ID = '"+ str(field_name)+ "' AND GREENBOOK = '"+str(TreeParam)+"' AND FABLOCATION_ID ='"+str(TreeParentParam)+"' ")
				userselected = []
				userselectedeff =[]
				if selecter:
					userselected.append(selecter.VALUEDRIVER_VALUE_DESCRIPTION)
					#userselected = [Valuedrivervalue.VALUEDRIVER_VALUE_DESCRIPTION for Valuedrivervalue in selecter if Valuedrivervalue.VALUEDRIVER_VALUE_DESCRIPTION]
					#userselectedeff = [str(float(Valuedrivereff.VALUEDRIVER_COEFFICIENT)*float(100))+" %" for Valuedrivereff in selecter if Valuedrivereff.VALUEDRIVER_COEFFICIENT]
					
					if selecter.VALUEDRIVER_COEFFICIENT == '0.00000':
						userselectedeff ='0.0%'
					else:
						userselectedeff.append(str(float(selecter.VALUEDRIVER_COEFFICIENT)*float(100))+" %")	
				else:
					userselectedeff = ''
				for qstns in GetDRIVNAME:					
					if qstns.VALUEDRIVER_VALUE_DESCRIPTION in userselected:
						VAR1 += (
							'<option value = "'
							+ str(qstns.VALUEDRIVER_VALUE_DESCRIPTION)
							+ '" selected>'
							+ str(qstns.VALUEDRIVER_VALUE_DESCRIPTION)
							+ "</option>"
						)
						
					else:
						VAR1 += (
							'<option value = "'
							+ str(qstns.VALUEDRIVER_VALUE_DESCRIPTION)
							+ '">'
							+ str(qstns.VALUEDRIVER_VALUE_DESCRIPTION)
							+ "</option>"
						)
				
				sec_str1 += (
					'<select class="form-control" id = "'
					+ str(field_name).replace(" ", "_")
					+ '" disabled><option value="Select">..Select</option>'
					+ str(VAR1)
					+ "</select>"
				)
			for data in qstn:
				if str(TreeSuperParentParam).upper() == "FAB LOCATIONS" or str(TreeTopSuperParentParam).upper() == "QUOTE ITEMS":
					new_value_dict["VALUE DRIVER DESCRIPTION"] = str(qstn.VALUEDRIVER_ID)
					new_value_dict["VALUE DRIVER COEFFICIENT"] =  userselectedeff
					
				else:
					new_value_dict["VALUE DRIVER DESCRIPTION"] = str(qstn.VALUE_DRIVER_ID)
					if len(userselectedeffi) != 0:
						coeffval = str(userselectedeffi).replace("['","").replace("']","")
						new_value_dict["VALUE DRIVER COEFFICIENT"] = str(float(coeffval)*float(100))+" %"
					else:
						new_value_dict["VALUE DRIVER COEFFICIENT"] =  ""
				new_value_dict["VALUE DRIVER VALUE"] = sec_str1
				
				
			date_field.append(new_value_dict)
		
		if str(TreeSuperParentParam).strip() != 'Quote Items':
			dbl_clk_function += (
				"try {var fablocatedict = [];$('#fabvaldrives').on('dbl-click-cell.bs.table', function (e, row, $element) {console.log('tset---');$('#fabvaldrives').find(':input(:disabled)').prop('disabled', false);$('#fabvaldrives tbody  tr td select option').css('background-color','lightYellow');$('#fabnotify').addClass('header_section_div  header_section_div_pad_bt10');$('#fabvaldrives  tbody tr td select').addClass('light_yellow');$('#fablocate_save').css('display','block');$('#fablocate_cancel').css('display','block');$('select').on('change', function() { console.log( this.value );var valuedrivchage = this.value;var valuedesc = $(this).closest('tr').find('td:nth-child(1)').text();console.log('valuedesc-----',valuedesc);var concate_data = valuedesc+'-'+valuedrivchage;if(!fablocatedict.includes(concate_data)){fablocatedict.push(concate_data)};console.log('fablocatedict---',fablocatedict);getfablocatedict = JSON.stringify(fablocatedict);localStorage.setItem('getfablocatedict', getfablocatedict);});});}catch {console.log('error---')}"
			)
			#Trace.Write('date_field---'+str(date_field))
		if str(CurrentTabName) == "Contract":
			dbl_clk_function = ""	
	
	else:
		if (TreeTopSuperParentParam == "Complementary Products" and subtab == "Fab Value Drivers" and TreeParentParam.startswith("Sending")):
			sec_str += '<div class="noRecDisp">Fab Value Drivers are not applicable at this level</div>'
		elif (TreeSuperTopParentParam == "Complementary Products" and subtab == "Greenbook Fab Value Drivers" and TreeSuperParentParam.startswith("Sending")):
			sec_str += '<div class="noRecDisp">Greenbook Fab Value Drivers are not applicable at this level</div>'
		elif (TreeSuperParentParam == 'Complementary Products' and subtab == 'Service Fab Value Drivers' and TreeParam.startswith("Sending")):
			sec_str += '<div class="noRecDisp">Service Fab Value Drivers are not applicable at this level</div>'	
		else:
			sec_str += '<div class="noRecDisp">No Records to Display</div>'
	return sec_str,table_id,date_field,dbl_clk_function


def nestedfabview(ACTION,CurrentRecordId,subtab):	
	sec_str1 = sec_str = ""
	dbl_clk_function = ""
	desc_list = ["VALUE DRIVER DESCRIPTION","VALUE DRIVER VALUE","VALUE DRIVER COEFFICIENT",]
	table_id = 'nestedfabvaldrives'
	attr_dict = {"VALUE DRIVER DESCRIPTION": "VALUE DRIVER DESCRIPTION",
					"VALUE DRIVER VALUE": "VALUE DRIVER VALUE",
					"VALUE DRIVER COEFFICIENT": "VALUE DRIVER COEFFICIENT",
				}
	date_field = []
	
	GetPRVLDR = Sql.GetList("SELECT DISTINCT VALUEDRIVER_ID,VALUEDRIVER_RECORD_ID FROM PRBUVD(NOLOCK) WHERE BUSINESSUNIT_ID ='"+str(TreeParam)+"' AND BUSINESSUNIT_VALUEDRIVER_RECORD_ID != '' ")
	sec_str += ('<div id = "fabnotify">')
	sec_str += ('<table id="' + str(table_id)+ '" data-escape="true" data-html="true"    data-show-header="true" > <thead><tr>')
	for key, invs in enumerate(list(desc_list)):
		invs = str(invs).strip()
		qstring = attr_dict.get(str(invs)) or ""
		sec_str += (
			'<th data-field="'
			+ invs
			+ '" data-title-tooltip="'
			+ str(qstring)
			+ '"  >'
			+ str(qstring)
			+ "</th>"
		)
	sec_str += '</tr></thead><tbody class ="app_id" ></tbody></table></div>'
	for qstn in GetPRVLDR:
		sec_str1 = sec_str_eff = ""
		VAR1 = coeffval = ""
		userselectedeffi = []
		mastername = str(qstn.VALUEDRIVER_RECORD_ID)
		field_name = str(qstn.VALUEDRIVER_ID).replace("'", "''")
		
		#sec_str += ('')
		new_value_dict = {}
		
		
		
		GetDRIVNAME = Sql.GetList(
			"SELECT TOP 1000 VALUEDRIVER_VALUE_DESCRIPTION FROM PRBDVL(NOLOCK) WHERE  VALUEDRIVER_ID = '"
			+ str(field_name)
			+ "' AND VALUEDRIVER_RECORD_ID = '"
			+ str(mastername)
			+ "' AND BUSINESSUNIT_ID = '"
			+ str(TreeParam)
			+ "'"
		)
		Get_EQUIP = Sql.GetFirst("SELECT EQUIPMENT_ID FROM SAQFEQ(NOLOCK) WHERE QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID ='"+str(CurrentRecordId)+"' AND QUOTE_RECORD_ID = '"+str(Qt_rec_id)+"'")
		if TreeTopSuperParentParam == 'Quote Items':
			Get_EQUIP = Sql.GetFirst("SELECT EQUIPMENT_ID FROM SAQICO(NOLOCK) WHERE QUOTE_ITEM_COVERED_OBJECT_RECORD_ID ='"+str(CurrentRecordId)+"' AND QUOTE_RECORD_ID = '"+str(Qt_rec_id)+"'")
		selecter = Sql.GetFirst("SELECT VALUEDRIVER_VALUE_DESCRIPTION,VALUEDRIVER_COEFFICIENT FROM SAQEDV(NOLOCK) WHERE QUOTE_RECORD_ID = '"+ str(Qt_rec_id)+ "' AND VALUEDRIVER_ID = '"+ str(field_name)+ "' AND EQUIPMENT_ID = '"+str(Get_EQUIP.EQUIPMENT_ID)+"'")
		userselected = []
		userselectedeff =[]
		if selecter:
			#userselected = [Valuedrivervalue.VALUEDRIVER_VALUE_DESCRIPTION for Valuedrivervalue in selecter if Valuedrivervalue.VALUEDRIVER_VALUE_DESCRIPTION]
			#userselectedeff = [str(float(Valuedrivereff.VALUEDRIVER_COEFFICIENT)*float(100))+" %" for Valuedrivereff in selecter if Valuedrivereff.VALUEDRIVER_COEFFICIENT]
			userselected.append(selecter.VALUEDRIVER_VALUE_DESCRIPTION)
			if selecter.VALUEDRIVER_COEFFICIENT == '0.00000':
				userselectedeff ='0.0%'
			else:
				userselectedeff.append(str(float(selecter.VALUEDRIVER_COEFFICIENT)*float(100))+" %")
		else:
			userselectedeff = ''
		for qstns in GetDRIVNAME:			
			if qstns.VALUEDRIVER_VALUE_DESCRIPTION in userselected:
				VAR1 += (
					'<option value = "'
					+ str(qstns.VALUEDRIVER_VALUE_DESCRIPTION)
					+ '" selected>'
					+ str(qstns.VALUEDRIVER_VALUE_DESCRIPTION)
					+ "</option>"
				)
				
			else:
				VAR1 += (
					'<option value = "'
					+ str(qstns.VALUEDRIVER_VALUE_DESCRIPTION)
					+ '">'
					+ str(qstns.VALUEDRIVER_VALUE_DESCRIPTION)
					+ "</option>"
				)
		
		sec_str1 += (
			'<select class="form-control" id = "'
			+ str(field_name).replace(" ", "_")
			+ '" disabled><option value="Select">..Select</option>'
			+ str(VAR1)
			+ "</select>"
		)
		for data in qstn:
			if str(TreeSuperParentParam).upper() == "FAB LOCATIONS" or TreeTopSuperParentParam == 'Quote Items':
				new_value_dict["VALUE DRIVER DESCRIPTION"] = str(qstn.VALUEDRIVER_ID)
				new_value_dict["VALUE DRIVER COEFFICIENT"] =  userselectedeff
			else:
				new_value_dict["VALUE DRIVER DESCRIPTION"] = str(qstn.VALUE_DRIVER_ID)
				if len(userselectedeffi) != 0:
					coeffval = str(userselectedeffi).replace("['","").replace("']","")
					new_value_dict["VALUE DRIVER COEFFICIENT"] = str(float(coeffval)*float(100))+" %"
				else:
					new_value_dict["VALUE DRIVER COEFFICIENT"] =  ""
			new_value_dict["VALUE DRIVER VALUE"] = sec_str1
			
			
		date_field.append(new_value_dict)
	
	if TreeTopSuperParentParam != 'Quote Items':
		dbl_clk_function += (
			"try {var fablocatedict = [];$('#nestedfabvaldrives').on('dbl-click-cell.bs.table', function (e, row, $element) {console.log('tset---');$('#nestedfabvaldrives').find(':input(:disabled)').prop('disabled', false);$('#nestedfabvaldrives tbody  tr td select option').css('background-color','lightYellow');$('#fabnotify').addClass('header_section_div  header_section_div_pad_bt10');$('#nestedfabvaldrives').addClass('header_section_div  header_section_div_pad_bt10');$('#nestedfabvaldrives  tbody tr td select').addClass('light_yellow');$('#fablocate_save').css('display','block');$('#fablocate_cancel').css('display','block');$('select').on('change', function() { console.log( this.value );var valuedrivchage = this.value;var valuedesc = $(this).closest('tr').find('td:nth-child(1)').text();console.log('valuedesc-----',valuedesc);var concate_data = valuedesc+'-'+valuedrivchage;if(!fablocatedict.includes(concate_data)){fablocatedict.push(concate_data)};console.log('fablocatedict---',fablocatedict);getfablocatedict = JSON.stringify(fablocatedict);localStorage.setItem('getfablocatedict', getfablocatedict);});});}catch {console.log('error---')}"
		)
		#Trace.Write('date_field---'+str(date_field))
	if str(CurrentTabName) == "Contract":
		dbl_clk_function = ""	
	
	if len(date_field) == 0:
		if (TreeSuperTopParentParam == "Complementary Products" and subtab == "Equipment Fab Value Drivers" and TreeSuperParentParam.startswith("Sending")):
			sec_str += '<div class="noRecDisp">Equipment Fab Value Drivers are not applicable at this level</div>'
		else:
			sec_str += '<div class="noRecDisp">No Records to Display</div>'
	return sec_str,table_id,date_field,dbl_clk_function


def servicefabview(ACTION,CurrentRecordId):		
	Trace.Write("@@383")
	sec_str1 = sec_str = ""
	dbl_clk_function = ""
	desc_list = ["VALUE DRIVER DESCRIPTION","VALUE DRIVER VALUE","VALUE DRIVER COEFFICIENT",]
	table_id = 'servicefabvaldrives'
	attr_dict = {"VALUE DRIVER DESCRIPTION": "VALUE DRIVER DESCRIPTION",
					"VALUE DRIVER VALUE": "VALUE DRIVER VALUE",
					"VALUE DRIVER COEFFICIENT": "VALUE DRIVER COEFFICIENT",
				}
	date_field = []
	
	GetPRVLDR = Sql.GetList("SELECT DISTINCT VALUE_DRIVER_ID,VALUE_DRIVER_RECORD_ID FROM PRVLDR(NOLOCK) WHERE VALUE_DRIVER_TYPE LIKE '%QUOTE BASED%'")
	Trace.Write("379")
	sec_str += ('<table id="' + str(table_id)+ '" data-escape="true" data-html="true"    data-show-header="true" > <thead><tr>')
	for key, invs in enumerate(list(desc_list)):
		invs = str(invs).strip()
		qstring = attr_dict.get(str(invs)) or ""
		sec_str += (
			'<th data-field="'
			+ invs
			+ '" data-title-tooltip="'
			+ str(qstring)
			+ '"  >'
			+ str(qstring)
			+ "</th>"
		)
	sec_str += '</tr></thead><tbody class ="app_id" ></tbody></table>'
	for qstn in GetPRVLDR:
		sec_str1 = sec_str_eff = ""
		VAR1 = coeffval = ""
		userselectedeffi = []
		mastername = str(qstn.VALUE_DRIVER_RECORD_ID)
		field_name = str(qstn.VALUE_DRIVER_ID).replace("'", "''")
		
		#sec_str += ('')
		new_value_dict = {}
		
		
		GetDRIVNAME = Sql.GetList(
			"SELECT TOP 1000 VALUEDRIVER_VALUE_DESCRIPTION FROM PRVDVL(NOLOCK) WHERE  VALUEDRIVER_ID = '"
			+ str(field_name)
			+ "' AND VALUEDRIVER_RECORD_ID = '"
			+ str(mastername)
			+ "'"
		)
		selecter = Sql.GetList(
			"SELECT VALUEDRIVER_VALUE_DESCRIPTION,VALUEDRIVER_COEFFICIENT FROM SAQVDV(NOLOCK) WHERE QUOTE_RECORD_ID = '"
			+ str(Qt_rec_id)
			+ "' AND VALUEDRIVER_ID = '"
			+ str(field_name)
			+ "'"
		)
		userselected = []
		if selecter:
			userselected = [Valuedrivervalue.VALUEDRIVER_VALUE_DESCRIPTION for Valuedrivervalue in selecter]
			userselectedeffi = [Valuedrivereff.VALUEDRIVER_COEFFICIENT for Valuedrivereff in selecter if Valuedrivereff.VALUEDRIVER_COEFFICIENT]
		
		for qstns in GetDRIVNAME:
			if qstns.VALUEDRIVER_VALUE_DESCRIPTION in userselected:
				VAR1 += (
					'<option value = "'
					+ str(qstns.VALUEDRIVER_VALUE_DESCRIPTION)
					+ '" selected>'
					+ str(qstns.VALUEDRIVER_VALUE_DESCRIPTION)
					+ "</option>"
				)
			else:
				VAR1 += (
					'<option value = "'
					+ str(qstns.VALUEDRIVER_VALUE_DESCRIPTION)
					+ '">'
					+ str(qstns.VALUEDRIVER_VALUE_DESCRIPTION)
					+ "</option>"
				)
		sec_str1 += (
			'<select class="form-control" disabled id = "'
			+ str(field_name).replace(" ", "_")
			+ '" disabled><option value="Select">..Select</option>'
			+ str(VAR1)
			+ "</select>"
		)
		for data in qstn:
			new_value_dict["VALUE DRIVER DESCRIPTION"] = str(qstn.VALUE_DRIVER_ID)
			if len(userselectedeffi) != 0:
				coeffval = str(userselectedeffi).replace("['","").replace("']","")
				new_value_dict["VALUE DRIVER COEFFICIENT"] = str(float(coeffval)*float(100))+" %"
			else:
				new_value_dict["VALUE DRIVER COEFFICIENT"] =  ""
			new_value_dict["VALUE DRIVER VALUE"] = sec_str1
			
			
		date_field.append(new_value_dict)
	
	
	
	#Trace.Write('date_field---'+str(date_field))
	if len(date_field) == 0:
		sec_str += '<div class="noRecDisp">No Records to Display</div>'
	return sec_str,table_id,date_field

def costfabview(ACTION,CurrentRecordId):
	sec_str1 = sec_str = ""
	dbl_clk_function = ""
	desc_list = ["VALUE DRIVER DESCRIPTION","VALUE DRIVER VALUE","VALUE DRIVER COEFFICIENT",]
	table_id = 'servicecostvaldrives'
	attr_dict = {"VALUE DRIVER DESCRIPTION": "VALUE DRIVER DESCRIPTION",
					"VALUE DRIVER VALUE": "VALUE DRIVER VALUE",
					"VALUE DRIVER COEFFICIENT": "VALUE DRIVER COEFFICIENT",
				}
	date_field = []
	TreeParam = Product.GetGlobal("TreeParam")
	if TreeParentParam == "Quote Items":
		TP = str(TreeParam)
		TP1 = TP.split('-')
		TreeParam = TP1[1].strip()
	GetSAQSVD = Sql.GetList("SELECT DISTINCT VALUEDRIVER_ID,VALUEDRIVER_RECORD_ID FROM PRSVDR(NOLOCK) WHERE VALUEDRIVER_TYPE = 'TOOL BASED' AND SERVICE_ID = '"+str(TreeParam)+"'")
	sec_str += ('<div id = "fabnotify">')
	sec_str += ('<table id="' + str(table_id)+ '" data-escape="true" data-html="true"    data-show-header="true" > <thead><tr>')
	for key, invs in enumerate(list(desc_list)):
		invs = str(invs).strip()
		qstring = attr_dict.get(str(invs)) or ""
		sec_str += (
			'<th data-field="'
			+ invs
			+ '" data-title-tooltip="'
			+ str(qstring)
			+ '"  >'
			+ str(qstring)
			+ "</th>"
		)
	sec_str += '</tr></thead><tbody class ="app_id" ></tbody></table></div>'
	for qstn in GetSAQSVD:
		sec_str1 = sec_str_eff = ""
		VAR1 = coeffval = ""
		userselectedeffi = []
		mastername = str(qstn.VALUEDRIVER_RECORD_ID)
		field_name = str(qstn.VALUEDRIVER_ID).replace("'", "''")
		
		#sec_str += ('')
		new_value_dict = {}
		
		
		GetDRIVNAME = Sql.GetList(
			"SELECT TOP 1000 VALUEDRIVER_VALUE_DESCRIPTION FROM PRSDVL(NOLOCK) WHERE  VALUEDRIVER_ID = '"
			+ str(field_name)
			+ "' AND VALUEDRIVER_RECORD_ID = '" 
			+ str(mastername)
			+ "'AND SERVICE_ID = '" 
			+ str(TreeParam)
			+ "'"
		)
		if TreeParentParam != 'Quote Items':
			selecter = Sql.GetList(
				"SELECT TOOL_VALUEDRIVER_VALUE_DESCRIPTION,VALUEDRIVER_COEFFICIENT FROM SAQSDV(NOLOCK) WHERE QUOTE_RECORD_ID = '"
				+ str(Qt_rec_id)
				+ "' AND TOOL_VALUEDRIVER_ID = '"
				+ str(field_name)
				+ "' AND QTESRV_RECORD_ID = '"
				+ str(CurrentRecordId)
				+ "' "
			)
		else:
			selecter = Sql.GetList(
				"SELECT TOOL_VALUEDRIVER_VALUE_DESCRIPTION,VALUEDRIVER_COEFFICIENT FROM SAQSDV(NOLOCK) WHERE QUOTE_RECORD_ID = '"
				+ str(Qt_rec_id)
				+ "' AND TOOL_VALUEDRIVER_ID = '"
				+ str(field_name)
				+ "' AND SERVICE_ID = '"
				+ str(TreeParam)
				+ "' "
			)
		userselected = userselectedeff =  []
		if selecter:
			userselected = [Valuedrivervalue.TOOL_VALUEDRIVER_VALUE_DESCRIPTION for Valuedrivervalue in selecter]
			userselectedeff = [str(float(Valuedrivereff.VALUEDRIVER_COEFFICIENT)*float(100))+" %" for Valuedrivereff in selecter]
			
		for qstns in GetDRIVNAME:
			if qstns.VALUEDRIVER_VALUE_DESCRIPTION in userselected:
				VAR1 += (
					'<option value = "'
					+ str(qstns.VALUEDRIVER_VALUE_DESCRIPTION)
					+ '" selected>'
					+ str(qstns.VALUEDRIVER_VALUE_DESCRIPTION)
					+ "</option>"
				)
			else:
				VAR1 += (
					'<option value = "'
					+ str(qstns.VALUEDRIVER_VALUE_DESCRIPTION)
					+ '">'
					+ str(qstns.VALUEDRIVER_VALUE_DESCRIPTION)
					+ "</option>"
				)
		sec_str1 += (
			'<select class="form-control" disabled id = "'
			+ str(field_name).replace(" ", "_")
			+ '" disabled><option value="Select">..Select</option>'
			+ str(VAR1)
			+ "</select>"
		)
		for data in qstn:
			new_value_dict["VALUE DRIVER DESCRIPTION"] = str(qstn.VALUEDRIVER_ID)
			new_value_dict["VALUE DRIVER COEFFICIENT"] =  userselectedeff
			new_value_dict["VALUE DRIVER VALUE"] = sec_str1
			
			
		date_field.append(new_value_dict)
	if TreeParentParam != "Quote Items":
		dbl_clk_function += (
			"try {var fablocatedict = [];$('#servicecostvaldrives').on('dbl-click-cell.bs.table', function (e, row, $element) {console.log('tset---');$('#servicecostvaldrives').find(':input(:disabled)').prop('disabled', false);$('#servicecostvaldrives tbody  tr td select option').css('background-color','lightYellow');$('#fabnotify').addClass('header_section_div  header_section_div_pad_bt10');$('#servicecostvaldrives').addClass('header_section_div  header_section_div_pad_bt10');$('#servicecostvaldrives  tbody tr td select').addClass('light_yellow');$('#fabcostlocate_save').css('display','block');$('#fabcostlocate_cancel').css('display','block');$('select').on('change', function() { console.log( this.value );var valuedrivchage = this.value;var valuedesc = $(this).closest('tr').find('td:nth-child(1)').text();console.log('valuedesc-----',valuedesc);var concate_data = valuedesc+'='+valuedrivchage;if(!fablocatedict.includes(concate_data)){fablocatedict.push(concate_data)};console.log('fablocatedict---',fablocatedict);getfablocatedict = JSON.stringify(fablocatedict);localStorage.setItem('getfablocatedict', getfablocatedict);});});}catch {console.log('error---')}"
		)
		
	
	if str(CurrentTabName) == "Contract":
		dbl_clk_function = ""	
	#Trace.Write('date_field---'+str(date_field))
	if len(date_field) == 0 and len(GetSAQSVD) == 0:
		if (TreeSuperParentParam == 'Complementary Products' and subtab == 'Service Cost and Value Drivers' and TreeParam.startswith("Sending")):
			sec_str += '<div class="noRecDisp">Service Cost and Value Drivers are not applicable at this level</div>'
		else:
			sec_str += '<div class="noRecDisp">Service Cost and Value Drivers are not applicable for this Product Offering</div>'
	if len(date_field) == 0 and len(GetSAQSVD) != 0:
		sec_str += '<div class="noRecDisp">No Records to Display</div>'	
	

	return sec_str,table_id,date_field,dbl_clk_function

def Comp_fabview(ACTION,CurrentRecordId):	
	Trace.Write("@@@610")
	sec_str1 = sec_str = ""
	dbl_clk_function = ""
	desc_list = ["VALUE DRIVER DESCRIPTION","VALUE DRIVER VALUE","VALUE DRIVER COEFFICIENT",]
	table_id = 'csservicefabvaldrives'
	attr_dict = {"VALUE DRIVER DESCRIPTION": "VALUE DRIVER DESCRIPTION",
					"VALUE DRIVER VALUE": "VALUE DRIVER VALUE",
					"VALUE DRIVER COEFFICIENT": "VALUE DRIVER COEFFICIENT",
				}
	date_field = []
	
	GetPRVLDR = SqlHelper.GetList("SELECT DISTINCT VALUE_DRIVER_ID,VALUE_DRIVER_RECORD_ID FROM PRVLDR(NOLOCK) WHERE VALUE_DRIVER_TYPE = 'QUOTE BASED'")
	sec_str += ('<table id="' + str(table_id)+ '" data-escape="true" data-html="true"    data-show-header="true" > <thead><tr>')
	for key, invs in enumerate(list(desc_list)):
		invs = str(invs).strip()
		qstring = attr_dict.get(str(invs)) or ""
		sec_str += (
			'<th data-field="'
			+ invs
			+ '" data-title-tooltip="'
			+ str(qstring)
			+ '"  >'
			+ str(qstring)
			+ "</th>"
		)
	sec_str += '</tr></thead><tbody class ="app_id" ></tbody></table>'
	for qstn in GetPRVLDR:
		sec_str1 = sec_str_eff = ""
		VAR1 = coeffval = ""
		userselectedeffi = []
		mastername = str(qstn.VALUE_DRIVER_RECORD_ID)
		field_name = str(qstn.VALUE_DRIVER_ID).replace("'", "''")
		
		#sec_str += ('')
		new_value_dict = {}
		
		
		GetDRIVNAME = SqlHelper.GetList(
			"SELECT TOP 1000 VALUEDRIVER_VALUE_DESCRIPTION,VALUEDRIVER_COEFFICIENT FROM PRVDVL(NOLOCK) WHERE  VALUEDRIVER_ID = '"
			+ str(field_name)
			+ "' AND VALUEDRIVER_RECORD_ID = '"
			+ str(mastername)
			+ "'"
		)
		selecter = Sql.GetList(
			"SELECT VALUEDRIVER_VALUEDESC,VALUEDRIVER_COEFFICIENT FROM SAQFDV(NOLOCK) WHERE QUOTE_RECORD_ID = '"
			+ str(Qt_rec_id)
			+ "' AND VALUEDRIVER_ID = '"
			+ str(field_name)
			+ "' AND FABLOCATION_ID = '"
			+ str(TreeParam)
			+ "'"
		)
		
		userselecteddrive = []
		
		if selecter:
			userselecteddrive = [Valuedrivervalue.VALUEDRIVER_VALUEDESC for Valuedrivervalue in selecter]
			userselectedeffi = [Valuedrivereff.VALUEDRIVER_COEFFICIENT for Valuedrivereff in selecter if Valuedrivereff.VALUEDRIVER_COEFFICIENT]

		
		for qstns in GetDRIVNAME:
			if qstns.VALUEDRIVER_VALUE_DESCRIPTION in userselecteddrive:
				VAR1 += (
					'<option  value = "'
					+ str(qstns.VALUEDRIVER_VALUE_DESCRIPTION)
					+ '" selected>'
					+ str(qstns.VALUEDRIVER_VALUE_DESCRIPTION)
					+ "</option>"
				)
			else:
				VAR1 += (
					'<option  value = "'
					+ str(qstns.VALUEDRIVER_VALUE_DESCRIPTION)
					+ '">'
					+ str(qstns.VALUEDRIVER_VALUE_DESCRIPTION)
					+ "</option>"
				)
			
		sec_str1 += (
			'<select class="form-control" id = "'
			+ str(field_name).replace(" ", "_")
			+ '" disabled><option value="Select">..Select</option>'
			+ str(VAR1)
			+ "</select>"
		)
		for data in qstn:
			new_value_dict["VALUE DRIVER DESCRIPTION"] = str(qstn.VALUE_DRIVER_ID)
			if len(userselectedeffi) != 0:
				coeffval = str(userselectedeffi).replace("['","").replace("']","")
				new_value_dict["VALUE DRIVER COEFFICIENT"] = str(float(coeffval)*float(100))+" %"
			else:
				new_value_dict["VALUE DRIVER COEFFICIENT"] =  ""
			new_value_dict["VALUE DRIVER VALUE"] = sec_str1
			
			
		date_field.append(new_value_dict)
	
	
	
	#Trace.Write('date_field---'+str(date_field))
	if len(date_field) == 0:
		sec_str += '<div class="noRecDisp">No Records to Display</div>'
	return sec_str,table_id,date_field

def item_gb_fabview(ACTION,CurrentRecordId):	
	TreeParam = Product.GetGlobal("TreeParam")
	TreeParentParam = Product.GetGlobal("TreeParentLevel0")
	TreeSuperParentParam = Product.GetGlobal("TreeParentLevel1")
	TreeTopSuperParentParam = Product.GetGlobal("TreeParentLevel2")
	
	sec_str1 = sec_str = ""
	dbl_clk_function = ""
	desc_list = ["VALUE DRIVER DESCRIPTION","VALUE DRIVER VALUE","VALUE DRIVER COEFFICIENT",]
	table_id = 'item_gb_fabview'
	attr_dict = {"VALUE DRIVER DESCRIPTION": "VALUE DRIVER DESCRIPTION",
					"VALUE DRIVER VALUE": "VALUE DRIVER VALUE",
					"VALUE DRIVER COEFFICIENT": "VALUE DRIVER COEFFICIENT",
				}
	date_field = []
	if str(TreeTopSuperParentParam).upper() == "QUOTE ITEMS":
		GetPRVLDR = Sql.GetList("SELECT DISTINCT VALUEDRIVER_ID,VALUEDRIVER_RECORD_ID FROM PRBUVD(NOLOCK) WHERE BUSINESSUNIT_ID ='"+str(TreeParam)+"' AND BUSINESSUNIT_VALUEDRIVER_RECORD_ID != '' ")
		#table_id = 'fabvaldrives'
		
	else:
		#table_id = 'fabvaluedrives'
		GetPRVLDR = SqlHelper.GetList("SELECT DISTINCT VALUE_DRIVER_ID,VALUE_DRIVER_RECORD_ID FROM PRVLDR(NOLOCK) WHERE VALUE_DRIVER_TYPE = 'QUOTE BASED'")
	sec_str += ('<table id="' + str(table_id)+ '" data-escape="true" data-html="true"    data-show-header="true" > <thead><tr>')
	
	for key, invs in enumerate(list(desc_list)):
		invs = str(invs).strip()
		qstring = attr_dict.get(str(invs)) or ""
		sec_str += (
			'<th data-field="'
			+ invs
			+ '" data-title-tooltip="'
			+ str(qstring)
			+ '"  >'
			+ str(qstring)
			+ "</th>"
		)
	sec_str += '</tr></thead><tbody class ="app_id" ></tbody></table>'
	if GetPRVLDR:
		for qstn in GetPRVLDR:
			if str(TreeTopSuperParentParam).upper() == "QUOTE ITEMS":				
				GetDRIVNAME = Sql.GetList(
					"SELECT TOP 1000 VALUEDRIVER_VALUE_DESCRIPTION FROM PRBDVL(NOLOCK) WHERE  VALUEDRIVER_ID = '"
					+ str(field_name)
					+ "' AND VALUEDRIVER_RECORD_ID = '"
					+ str(mastername)
					+ "' AND BUSINESSUNIT_ID = '"
					+ str(TreeParam)
					+ "'"
				)
				selecter = Sql.GetList("SELECT VALUEDRIVER_VALUE_DESCRIPTION,VALUEDRIVER_COEFFICIENT FROM SAQFGV(NOLOCK) WHERE QUOTE_RECORD_ID = '"+ str(Qt_rec_id)+ "' AND VALUEDRIVER_ID = '"+ str(field_name)+ "' AND GREENBOOK = '"+str(TreeParam)+"' AND FABLOCATION_ID ='"+str(TreeParentParam)+"' ")
				userselected = []
				if selecter:
					userselected = [Valuedrivervalue.VALUEDRIVER_VALUE_DESCRIPTION for Valuedrivervalue in selecter if Valuedrivervalue.VALUEDRIVER_VALUE_DESCRIPTION]
					userselectedeff = [str(float(Valuedrivereff.VALUEDRIVER_COEFFICIENT)*float(100))+" %" for Valuedrivereff in selecter if Valuedrivereff.VALUEDRIVER_COEFFICIENT]
				else:
					userselectedeff = ''
				for qstns in GetDRIVNAME:					
					if qstns.VALUEDRIVER_VALUE_DESCRIPTION in userselected:
						VAR1 += (
							'<option value = "'
							+ str(qstns.VALUEDRIVER_VALUE_DESCRIPTION)
							+ '" selected>'
							+ str(qstns.VALUEDRIVER_VALUE_DESCRIPTION)
							+ "</option>"
						)
						
					else:
						VAR1 += (
							'<option value = "'
							+ str(qstns.VALUEDRIVER_VALUE_DESCRIPTION)
							+ '">'
							+ str(qstns.VALUEDRIVER_VALUE_DESCRIPTION)
							+ "</option>"
						)
				
				sec_str1 += (
					'<select class="form-control" id = "'
					+ str(field_name).replace(" ", "_")
					+ '"><option value="Select">..Select</option>'
					+ str(VAR1)
					+ "</select>"
				)
			for data in qstn:
				if str(TreeSuperParentParam).upper() == "FAB LOCATIONS":
					new_value_dict["VALUE DRIVER DESCRIPTION"] = str(qstn.VALUEDRIVER_ID)
					new_value_dict["VALUE DRIVER COEFFICIENT"] =  userselectedeff
				else:
					new_value_dict["VALUE DRIVER DESCRIPTION"] = str(qstn.VALUE_DRIVER_ID)
					if len(userselectedeffi) != 0:
						coeffval = str(userselectedeffi).replace("['","").replace("']","")
						new_value_dict["VALUE DRIVER COEFFICIENT"] = str(float(coeffval)*float(100))+" %"
					else:
						new_value_dict["VALUE DRIVER COEFFICIENT"] =  ""
				new_value_dict["VALUE DRIVER VALUE"] = sec_str1
				
				
			date_field.append(new_value_dict)
		

		#Trace.Write('date_field---'+str(date_field))
	else:
		sec_str += '<div class="noRecDisp">No Records to Display</div>'
	return sec_str,table_id,date_field

def Comp_cost_fabview(ACTION,CurrentRecordId,subtab):	
	TreeParam = Product.GetGlobal("TreeParam")
	TreeParentParam = Product.GetGlobal("TreeParentLevel0")
	TreeSuperParentParam = Product.GetGlobal("TreeParentLevel1")
	TreeTopSuperParentParam = Product.GetGlobal("TreeParentLevel2")
	userId = str(User.Id)
	userName = str(User.UserName)
	
	sec_str1 = sec_str = ""
	dbl_clk_function = ""
	desc_list = ["VALUE DRIVER DESCRIPTION","VALUE DRIVER VALUE","VALUE DRIVER COEFFICIENT",]
	table_id = 'csservicecostfabvaldrives'
	attr_dict = {"VALUE DRIVER DESCRIPTION": "VALUE DRIVER DESCRIPTION",
					"VALUE DRIVER VALUE": "VALUE DRIVER VALUE",
					"VALUE DRIVER COEFFICIENT": "VALUE DRIVER COEFFICIENT",
				}
	date_field = []
	if TreeSuperParentParam == "Quote Items":
		TP = str(TreeParentParam)
		TP1 = TP.split('-')
		TreeParentParam = TP1[1].strip()
	GetSAQSVD = Sql.GetList("SELECT DISTINCT VALUEDRIVER_ID,VALUEDRIVER_RECORD_ID FROM PRSVDR(NOLOCK) WHERE VALUEDRIVER_TYPE = 'TOOL BASED' AND SERVICE_ID = '"+str(TreeParentParam)+"'")
	sec_str += ('<div id = "fabnotify">')
	sec_str += ('<table id="' + str(table_id)+ '" data-escape="true" data-html="true"  data-locale = "en-US"  data-show-header="true" > <thead><tr>')
	for key, invs in enumerate(list(desc_list)):
		invs = str(invs).strip()
		qstring = attr_dict.get(str(invs)) or ""
		sec_str += (
			'<th data-field="'
			+ invs
			+ '" data-title-tooltip="'
			+ str(qstring)
			+ '" >'
			+ str(qstring)
			+ "</th>"
		)
	sec_str += '</tr></thead><tbody class ="app_id" ></tbody></table></div>'
	for qstn in GetSAQSVD:
		sec_str1 = sec_str_eff = ""
		VAR1 = coeffval = ""
		userselectedeffi = []
		mastername = str(qstn.VALUEDRIVER_RECORD_ID)
		field_name = str(qstn.VALUEDRIVER_ID).replace("'", "''")
		
		#sec_str += ('')
		new_value_dict = {}
		
		
		GetDRIVNAME = SqlHelper.GetList(
			"SELECT TOP 1000 VALUEDRIVER_VALUE_DESCRIPTION,VALUEDRIVER_COEFFICIENT FROM PRSDVL(NOLOCK) WHERE  VALUEDRIVER_ID = '"
			+ str(field_name)
			+ "' AND VALUEDRIVER_RECORD_ID = '"
			+ str(mastername)
			+ "' AND SERVICE_ID ='"
			+ str(TreeParentParam)
			+ "'"
		)
		selecter = Sql.GetFirst(
			"SELECT VALUEDRIVER_VALUE_DESCRIPTION,VALUEDRIVER_COEFFICIENT FROM SAQSFV(NOLOCK) WHERE QUOTE_RECORD_ID = '"
			+ str(Qt_rec_id)
			+ "' AND VALUEDRIVER_ID = '"
			+ str(field_name)
			+ "' AND FABLOCATION_ID = '"
			+ str(TreeParam)
			+ "' AND SERVICE_ID = '"
			+ str(TreeParentParam)
			+ "'"
		)
		
		userselecteddrive = []
		
		if selecter:
			userselecteddrive.append(selecter.VALUEDRIVER_VALUE_DESCRIPTION)
			userselectedeffi.append(str(float(selecter.VALUEDRIVER_COEFFICIENT)*float(100))+" %")
			""" userselecteddrive = [Valuedrivervalue.VALUEDRIVER_VALUE_DESCRIPTION for Valuedrivervalue in selecter]
			userselectedeffi = [str(float(Valuedrivereff.VALUEDRIVER_COEFFICIENT)*float(100))+" %" for Valuedrivereff in selecter if Valuedrivereff.VALUEDRIVER_COEFFICIENT] """

		
		for qstns in GetDRIVNAME:
			if qstns.VALUEDRIVER_VALUE_DESCRIPTION in userselecteddrive:
				VAR1 += (
					'<option  value = "'
					+ str(qstns.VALUEDRIVER_VALUE_DESCRIPTION)
					+ '" selected>'
					+ str(qstns.VALUEDRIVER_VALUE_DESCRIPTION)
					+ "</option>"
				)
			else:
				VAR1 += (
					'<option  value = "'
					+ str(qstns.VALUEDRIVER_VALUE_DESCRIPTION)
					+ '">'
					+ str(qstns.VALUEDRIVER_VALUE_DESCRIPTION)
					+ "</option>"
				)
			
		sec_str1 += (
			'<select class="form-control" id = "'
			+ str(field_name).replace(" ", "_")
			+ '" disabled><option value="Select">..Select</option>'
			+ str(VAR1)
			+ "</select>"
		)
		for data in qstn:
			new_value_dict["VALUE DRIVER DESCRIPTION"] = str(qstn.VALUEDRIVER_ID)
			new_value_dict["VALUE DRIVER COEFFICIENT"] =  userselectedeffi
			new_value_dict["VALUE DRIVER VALUE"] = sec_str1
			
			
		date_field.append(new_value_dict)
	if TreeSuperParentParam != "Quote Items":
		dbl_clk_function += (
			"try {debugger; var fablocatedict = [];$('#csservicecostfabvaldrives').on('dbl-click-cell.bs.table', function (e, row, $element) {console.log('tset---');$('#csservicecostfabvaldrives').find(':input(:disabled)').prop('disabled', false);$('#csservicecostfabvaldrives tbody  tr td select option').css('background-color','lightYellow');$('#fabnotify').addClass('header_section_div  header_section_div_pad_bt10');$('#csservicecostfabvaldrives').addClass('header_section_div  header_section_div_pad_bt10');$('#csservicecostfabvaldrives  tbody tr td select').addClass('light_yellow');$('#fabcostlocate_save').css('display','block');$('#fabcostlocate_cancel').css('display','block');$('select').on('change', function() { console.log( this.value );var valuedrivchage = this.value;var valuedesc = $(this).closest('tr').find('td:nth-child(1)').text();console.log('valuedesc-----',valuedesc);var concate_data = valuedesc+'='+valuedrivchage;if(!fablocatedict.includes(concate_data)){fablocatedict.push(concate_data)};console.log('fablocatedict---',fablocatedict);getfablocatedict = JSON.stringify(fablocatedict);localStorage.setItem('getfablocatedict', getfablocatedict);});});}catch {console.log('error---')}"
		)
	#Trace.Write('date_field---'+str(date_field))
	if len(date_field) == 0 and len(GetSAQSVD) == 0:
		if (TreeTopSuperParentParam == "Complementary Products" and subtab == "Fab Cost and Value Drivers" and TreeParentParam.startswith("Sending")):
			sec_str += '<div class="noRecDisp">Fab Cost and Value Drivers are not applicable at this level</div>'
		else:
			sec_str += '<div class="noRecDisp">Fab Cost and Value Drivers are not applicable for this Product Offering</div>'
	if len(date_field) == 0 and len(GetSAQSVD) != 0:
		sec_str += '<div class="noRecDisp">No Records to Display</div>'
	return sec_str,table_id,date_field,dbl_clk_function

def Offergreenfab(ACTION,CurrentRecordId):	
	sec_str1 = sec_str = ""
	dbl_clk_function = ""
	desc_list = ["VALUE DRIVER DESCRIPTION","VALUE DRIVER VALUE","VALUE DRIVER COEFFICIENT",]
	table_id = 'csserviceGreenfabvaldrives'
	attr_dict = {"VALUE DRIVER DESCRIPTION": "VALUE DRIVER DESCRIPTION",
					"VALUE DRIVER VALUE": "VALUE DRIVER VALUE",
					"VALUE DRIVER COEFFICIENT": "VALUE DRIVER COEFFICIENT",
				}
	date_field = []
	
	#GetPRVLDR = SqlHelper.GetList("SELECT DISTINCT VALUE_DRIVER_ID,VALUE_DRIVER_RECORD_ID FROM PRVLDR(NOLOCK) WHERE VALUE_DRIVER_TYPE = 'QUOTE BASED'")
	GetPRVLDR = Sql.GetList("SELECT DISTINCT VALUEDRIVER_ID,VALUEDRIVER_RECORD_ID FROM PRBUVD(NOLOCK) WHERE BUSINESSUNIT_ID ='"+str(TreeParam)+"' AND BUSINESSUNIT_VALUEDRIVER_RECORD_ID != '' ")
	sec_str += ('<table id="' + str(table_id)+ '" data-escape="true" data-html="true"    data-show-header="true" > <thead><tr>')
	for key, invs in enumerate(list(desc_list)):
		invs = str(invs).strip()
		qstring = attr_dict.get(str(invs)) or ""
		sec_str += (
			'<th data-field="'
			+ invs
			+ '" data-title-tooltip="'
			+ str(qstring)
			+ '" >'
			+ str(qstring)
			+ "</th>"
		)
	sec_str += '</tr></thead><tbody class ="app_id" ></tbody></table>'
	for qstn in GetPRVLDR:
		sec_str1 = sec_str_eff = ""
		VAR1 = coeffval = ""
		userselectedeffi = []
		mastername = str(qstn.VALUEDRIVER_RECORD_ID)
		field_name = str(qstn.VALUEDRIVER_ID).replace("'", "''")
		
		#sec_str += ('')
		new_value_dict = {}
		
		
		GetDRIVNAME = Sql.GetList(
				"SELECT TOP 1000 VALUEDRIVER_VALUE_DESCRIPTION FROM PRBDVL(NOLOCK) WHERE  VALUEDRIVER_ID = '"
				+ str(field_name)
				+ "' AND VALUEDRIVER_RECORD_ID = '"
				+ str(mastername)
				+ "' AND BUSINESSUNIT_ID = '"
				+ str(TreeParam)
				+ "'"
			)
		selecter = Sql.GetFirst("SELECT VALUEDRIVER_VALUE_DESCRIPTION,VALUEDRIVER_COEFFICIENT FROM SAQFGV(NOLOCK) WHERE QUOTE_RECORD_ID = '"+ str(Qt_rec_id)+ "' AND VALUEDRIVER_ID = '"+ str(field_name)+ "' AND GREENBOOK = '"+str(TreeParam)+"' AND FABLOCATION_ID ='"+str(TreeParentParam)+"' ")
		userselecteddrive = []
		
		if selecter:
			#userselecteddrive = [Valuedrivervalue.VALUEDRIVER_VALUE_DESCRIPTION for Valuedrivervalue in selecter]
			#userselectedeffi = [str(float(Valuedrivereff.VALUEDRIVER_COEFFICIENT)*float(100))+" %" for Valuedrivereff in selecter if Valuedrivereff.VALUEDRIVER_COEFFICIENT]
			userselecteddrive.append(selecter.VALUEDRIVER_VALUE_DESCRIPTION)				
			if selecter.VALUEDRIVER_COEFFICIENT == '0.00000':
				userselectedeffi ='0.0%'
			else:
				userselectedeffi.append(str(float(selecter.VALUEDRIVER_COEFFICIENT)*float(100))+" %")
		
		
		for qstns in GetDRIVNAME:
			if qstns.VALUEDRIVER_VALUE_DESCRIPTION in userselecteddrive:
				VAR1 += (
					'<option  value = "'
					+ str(qstns.VALUEDRIVER_VALUE_DESCRIPTION)
					+ '" selected>'
					+ str(qstns.VALUEDRIVER_VALUE_DESCRIPTION)
					+ "</option>"
				)
			else:
				VAR1 += (
					'<option  value = "'
					+ str(qstns.VALUEDRIVER_VALUE_DESCRIPTION)
					+ '">'
					+ str(qstns.VALUEDRIVER_VALUE_DESCRIPTION)
					+ "</option>"
				)
			
		sec_str1 += (
			'<select class="form-control" id = "'
			+ str(field_name).replace(" ", "_")
			+ '" disabled><option value="Select">..Select</option>'
			+ str(VAR1)
			+ "</select>"
		)
		for data in qstn:
			new_value_dict["VALUE DRIVER DESCRIPTION"] = str(qstn.VALUEDRIVER_ID)
			
			new_value_dict["VALUE DRIVER COEFFICIENT"]  = userselectedeffi
			
			new_value_dict["VALUE DRIVER VALUE"] = sec_str1
			
			
		date_field.append(new_value_dict)
	#Trace.Write('date_field---'+str(date_field))
	if len(date_field) == 0:
		sec_str += '<div class="noRecDisp">No Records to Display</div>'
	return sec_str,table_id,date_field

def Offerequipfab(ACTION,CurrentRecordId):	
	sec_str1 = sec_str = ""
	dbl_clk_function = ""
	desc_list = ["VALUE DRIVER DESCRIPTION","VALUE DRIVER VALUE","VALUE DRIVER COEFFICIENT",]
	table_id = 'csserviceEquipfabvaldrives'
	attr_dict = {"VALUE DRIVER DESCRIPTION": "VALUE DRIVER DESCRIPTION",
					"VALUE DRIVER VALUE": "VALUE DRIVER VALUE",
					"VALUE DRIVER COEFFICIENT": "VALUE DRIVER COEFFICIENT",
				}
	date_field = []
	
	#GetPRVLDR = SqlHelper.GetList("SELECT DISTINCT VALUE_DRIVER_ID,VALUE_DRIVER_RECORD_ID FROM PRVLDR(NOLOCK) WHERE VALUE_DRIVER_TYPE = 'QUOTE BASED'")
	GetPRVLDR = Sql.GetList("SELECT DISTINCT VALUEDRIVER_ID,VALUEDRIVER_RECORD_ID FROM PRBUVD(NOLOCK) WHERE BUSINESSUNIT_ID ='"+str(TreeParam)+"' AND BUSINESSUNIT_VALUEDRIVER_RECORD_ID != '' ")
	sec_str += ('<table id="' + str(table_id)+ '" data-escape="true" data-html="true"    data-show-header="true" > <thead><tr>')
	for key, invs in enumerate(list(desc_list)):
		invs = str(invs).strip()
		qstring = attr_dict.get(str(invs)) or ""
		sec_str += (
			'<th data-field="'
			+ invs
			+ '" data-title-tooltip="'
			+ str(qstring)
			+ '"  >'
			+ str(qstring)
			+ "</th>"
		)
	sec_str += '</tr></thead><tbody class ="app_id" ></tbody></table>'
	for qstn in GetPRVLDR:
		sec_str1 = sec_str_eff = ""
		VAR1 = coeffval = ""
		userselectedeffi = []
		mastername = str(qstn.VALUEDRIVER_RECORD_ID)
		field_name = str(qstn.VALUEDRIVER_ID).replace("'", "''")
		
		#sec_str += ('')
		new_value_dict = {}
		
		
		GetDRIVNAME = Sql.GetList(
				"SELECT TOP 1000 VALUEDRIVER_VALUE_DESCRIPTION FROM PRBDVL(NOLOCK) WHERE  VALUEDRIVER_ID = '"
				+ str(field_name)
				+ "' AND VALUEDRIVER_RECORD_ID = '"
				+ str(mastername)
				+ "' AND BUSINESSUNIT_ID = '"
				+ str(TreeParam)
				+ "'"
			)
		selecter = Sql.GetFirst("SELECT VALUEDRIVER_VALUE_DESCRIPTION,VALUEDRIVER_COEFFICIENT FROM SAQEDV(NOLOCK) WHERE QUOTE_RECORD_ID = '"+ str(Qt_rec_id)+ "' AND VALUEDRIVER_ID = '"+ str(field_name)+ "' AND GREENBOOK = '"+str(TreeParam)+"' AND FABLOCATION_ID ='"+str(TreeParentParam)+"' AND EQUIPMENT_ID = '"+str(CurrentRecordId)+"' ")
		userselecteddrive = []
		
		if selecter:
			#userselecteddrive = [Valuedrivervalue.VALUEDRIVER_VALUE_DESCRIPTION for Valuedrivervalue in selecter]
			#userselectedeffi = [str(float(Valuedrivereff.VALUEDRIVER_COEFFICIENT)*float(100))+" %" for Valuedrivereff in selecter if Valuedrivereff.VALUEDRIVER_COEFFICIENT]
			userselecteddrive.append(selecter.VALUEDRIVER_VALUE_DESCRIPTION)					
			if selecter.VALUEDRIVER_COEFFICIENT == '0.00000':
				userselectedeffi ='0.0%'
			else:
				userselectedeffi.append(str(float(selecter.VALUEDRIVER_COEFFICIENT)*float(100))+" %")
				
		
		
		for qstns in GetDRIVNAME:			
			if qstns.VALUEDRIVER_VALUE_DESCRIPTION in userselecteddrive:
				VAR1 += (
					'<option  value = "'
					+ str(qstns.VALUEDRIVER_VALUE_DESCRIPTION)
					+ '" selected>'
					+ str(qstns.VALUEDRIVER_VALUE_DESCRIPTION)
					+ "</option>"
				)
			else:
				VAR1 += (
					'<option  value = "'
					+ str(qstns.VALUEDRIVER_VALUE_DESCRIPTION)
					+ '">'
					+ str(qstns.VALUEDRIVER_VALUE_DESCRIPTION)
					+ "</option>"
				)
			
		sec_str1 += (
			'<select class="form-control" id = "'
			+ str(field_name).replace(" ", "_")
			+ '" disabled><option value="Select">..Select</option>'
			+ str(VAR1)
			+ "</select>"
		)
		for data in qstn:
			new_value_dict["VALUE DRIVER DESCRIPTION"] = str(qstn.VALUEDRIVER_ID)
			
			new_value_dict["VALUE DRIVER COEFFICIENT"]  = userselectedeffi
			
			new_value_dict["VALUE DRIVER VALUE"] = sec_str1
			
			
		date_field.append(new_value_dict)
	#Trace.Write('date_field---'+str(date_field))
	if len(date_field) == 0:
		sec_str += '<div class="noRecDisp">No Records to Display</div>'
	return sec_str,table_id,date_field

def fabsave(ACTION,CurrentRecordId,FabLocateDT,getfabid,subtab):
	TreeParam = Product.GetGlobal("TreeParam")
	TreeParentParam = Product.GetGlobal("TreeParentLevel0")
	TreeSuperParentParam = Product.GetGlobal("TreeParentLevel1")
	TreeTopSuperParentParam = Product.GetGlobal("TreeParentLevel2")
	userId = str(User.Id)
	userName = str(User.UserName)
	Getmastertable = Sql.GetFirst("SELECT * FROM SAQTMT(NOLOCK) WHERE MASTER_TABLE_QUOTE_RECORD_ID = '" + str(Qt_rec_id) + "'")
	GetSalesOrg = Sql.GetFirst("SELECT * FROM SAQTSO(NOLOCK) WHERE QUOTE_RECORD_ID = '" + str(Qt_rec_id) + "'")
	GETFABLOC = Sql.GetFirst("SELECT * FROM SAQFBL(NOLOCK) WHERE QUOTE_RECORD_ID ='" + str(Qt_rec_id)+ "' and FABLOCATION_ID = '"+ str(TreeParam)+ "'")
	for val in FabLocateDT:
		getval = str(val).replace("('","").replace("',)","")
		getdescription =getval.split('-')[0]		
		#getvaluedriv = getval.split('-')[1]
		getvaluedriv = getval.partition('-')[2]
		if str(TreeParam).upper() == "QUOTE INFORMATION":
			if str(getdescription) == "Quality required by the clients' customers":
				getdescription = "Quality required by the clients'' customers"
			Getchildtable = Sql.GetFirst(
				"SELECT * FROM PRVLDR (NOLOCK) WHERE VALUE_DRIVER_TYPE = 'QUOTE BASED' AND VALUE_DRIVER_ID ='"
				+ str(getdescription)
				+ "' "
			)

			
			tablerow = {}
			SAQTVDENTRY = Sql.GetFirst(
				"Select QUOTE_VALUEDRIVER_RECORD_ID FROM SAQTVD(NOLOCK) WHERE QUOTE_RECORD_ID='{}' AND VALUEDRIVER_RECORD_ID='{}' ".format(
					str(Getmastertable.MASTER_TABLE_QUOTE_RECORD_ID), str(Getchildtable.VALUE_DRIVER_RECORD_ID)
				)
			)
			primarykey = str(Guid.NewGuid()).upper()
			SEConDARYkey = primarykey
			if SAQTVDENTRY is None:
				tableInfo = SqlHelper.GetTable("SAQTVD")
				tablerow = {
					"QUOTE_ID": str(Getmastertable.QUOTE_ID),
					"QUOTE_NAME": str(Getmastertable.QUOTE_NAME),
					"QUOTE_RECORD_ID": str(Getmastertable.MASTER_TABLE_QUOTE_RECORD_ID),
					"VALUEDRIVER_ID": str(Getchildtable.VALUE_DRIVER_ID),
					"VALUEDRIVER_NAME": str(Getchildtable.VALUE_DRIVER_NAME),
					"VALUEDRIVER_RECORD_ID": str(Getchildtable.VALUE_DRIVER_RECORD_ID),
					"QUOTE_VALUEDRIVER_RECORD_ID": SEConDARYkey,
					"VALUEDRIVER_TYPE": str(Getchildtable.VALUE_DRIVER_TYPE),
					"SALESORG_ID":str(GetSalesOrg.SALESORG_ID),
					"SALESORG_NAME":str(GetSalesOrg.SALESORG_NAME),
					"SALESORG_RECORD_ID":str(GetSalesOrg.SALESORG_RECORD_ID),
					"CPQTABLEENTRYDATEADDED": datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"),
					"CPQTABLEENTRYADDEDBY": userName,
					"ADDUSR_RECORD_ID": userId,
				}
				#Trace.Write(str(tablerow))
				tableInfo.AddRow(tablerow)
				Sql.Upsert(tableInfo)
				#Trace.Write("aaaaaaaaaaa" + str(tablerow))

			Getchildtable2 = Sql.GetFirst(
				"SELECT * FROM PRVDVL (NOLOCK) WHERE VALUEDRIVER_VALUE_DESCRIPTION ='" + str(getvaluedriv) + "'"
			)
			if Getchildtable2:
				tablerow2 = {}
				tableInfo2 = SqlHelper.GetTable("SAQVDV")
				Q = Sql.GetFirst(
					"Select QUOTE_VALUEDRIVER_RECORD_ID FROM SAQTVD(NOLOCK) WHERE QUOTE_RECORD_ID='{}' AND VALUEDRIVER_RECORD_ID='{}'".format(
						str(Getmastertable.MASTER_TABLE_QUOTE_RECORD_ID), str(Getchildtable.VALUE_DRIVER_RECORD_ID)
					)
				)
				SAQVDVENTRY = Sql.GetFirst(
					"Select QUOTE_VALUE_DRIVER_VALUE_RECORD_ID,CpqTableEntryId,QTEVDR_RECORD_ID FROM SAQVDV(NOLOCK) WHERE QUOTE_RECORD_ID='{}' AND VALUEDRIVER_RECORD_ID='{}'".format(
						str(Getmastertable.MASTER_TABLE_QUOTE_RECORD_ID), str(Getchildtable.VALUE_DRIVER_RECORD_ID)
					)
				)
				if SAQVDVENTRY:
					tablerow2 = {"CpqTableEntryId": SAQVDVENTRY.CpqTableEntryId}
				else:
					tablerow2 = {"QUOTE_VALUE_DRIVER_VALUE_RECORD_ID": str(Guid.NewGuid()).upper()}
				tablerow2.update(
					{
						"QUOTE_ID": str(Getmastertable.QUOTE_ID),
						"QUOTE_NAME": str(Getmastertable.QUOTE_NAME),
						"QUOTE_RECORD_ID": str(Getmastertable.MASTER_TABLE_QUOTE_RECORD_ID),
						"VALUEDRIVER_ID": str(Getchildtable.VALUE_DRIVER_ID),
						"VALUEDRIVER_NAME": str(Getchildtable.VALUE_DRIVER_NAME),
						"VALUEDRIVER_RECORD_ID": str(Getchildtable.VALUE_DRIVER_RECORD_ID),
						"QTEVDR_RECORD_ID": str(Q.QUOTE_VALUEDRIVER_RECORD_ID),
						"VALUEDRIVER_VALUE_DESCRIPTION": getvaluedriv,
						"VALUEDRIVER_VALUE_RECORD_ID": str(Getchildtable2.VALUE_DRIVER_VALUE_RECORD_ID),
						"VALUEDRIVER_COEFFICIENT":str(Getchildtable2.VALUEDRIVER_COEFFICIENT),
						"VALUEDRIVER_TYPE": str(Getchildtable.VALUE_DRIVER_TYPE),
						#"VALUEDRIVER_VALUE_CODE":str(Getchildtable.VALUEDRIVER_VALUE_CODE),
						"SALESORG_ID":str(GetSalesOrg.SALESORG_ID),
						"SALESORG_NAME":str(GetSalesOrg.SALESORG_NAME),
						"SALESORG_RECORD_ID":str(GetSalesOrg.SALESORG_RECORD_ID),
						"CPQTABLEENTRYDATEADDED": datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"),
						"CPQTABLEENTRYADDEDBY": userName,
						"ADDUSR_RECORD_ID": userId,
					}
				)
				#Trace.Write(str(tablerow2))
				tableInfo2.AddRow(tablerow2)
				Sql.Upsert(tableInfo2)

			try:				
				quote = Qt_rec_id
				level = "QUOTE VALUE DRIVER"
				userId = str(User.Id)
				userName = str(User.UserName)
				TreeParam = Product.GetGlobal("TreeParam")
				TreeParentParam = Product.GetGlobal("TreeParentLevel0")
				TreeSuperParentParam = Product.GetGlobal("TreeParentLevel1")
				TreeTopSuperParentParam = Product.GetGlobal("TreeParentLevel2")
				CQTVLDRIFW.iflow_valuedriver_rolldown(quote,level,TreeParam, TreeParentParam, TreeSuperParentParam, TreeTopSuperParentParam,userId,userName)
			except:
				Trace.Write("EXCEPT----QUOTE VALUE DRIVER LEVEL IFLOW")
		elif str(TreeParentParam).upper() == "FAB LOCATIONS":
			if str(getdescription) == "Quality required by the clients' customers":
				getdescription = "Quality required by the clients'' customers"
			GETFBVD = Sql.GetFirst(
				"SELECT * FROM PRVLDR (NOLOCK) WHERE VALUE_DRIVER_TYPE = 'QUOTE BASED' AND VALUE_DRIVER_ID ='"
				+ str(getdescription)
				+ "' "
			)
			
			SAQFVDENTRY = Sql.GetFirst(
				"Select QUOTE_FABLOCATION_VALUEDRIVER_RECORD_ID FROM SAQFVD(NOLOCK) WHERE QUOTE_RECORD_ID='{}' AND VALUEDRIVER_RECORD_ID='{}' AND QTEFBL_RECORD_ID ='{}' ".format(
					str(GETFABLOC.QUOTE_RECORD_ID), str(GETFBVD.VALUE_DRIVER_RECORD_ID),str(GETFABLOC.QUOTE_FABLOCATION_RECORD_ID)
				)
			)
			primarykey = str(Guid.NewGuid()).upper()
			if SAQFVDENTRY is None:				
				tableInfo = SqlHelper.GetTable("SAQFVD")
				tablerow = {
					"QUOTE_FABLOCATION_VALUEDRIVER_RECORD_ID": primarykey,
					"FABLOCATION_ID": str(GETFABLOC.FABLOCATION_ID),
					"FABLOCATION_NAME": str(GETFABLOC.FABLOCATION_NAME),
					"FABLOCATION_RECORD_ID": str(GETFABLOC.FABLOCATION_RECORD_ID),
					"QUOTE_ID": str(GETFABLOC.QUOTE_ID),
					"QUOTE_NAME": str(GETFABLOC.QUOTE_NAME),
					"QUOTE_RECORD_ID": str(GETFABLOC.QUOTE_RECORD_ID),
					"VALUEDRIVER_ID": str(GETFBVD.VALUE_DRIVER_ID),
					"VALUEDRIVER_NAME": str(GETFBVD.VALUE_DRIVER_NAME),
					"VALUEDRIVER_RECORD_ID": str(GETFBVD.VALUE_DRIVER_RECORD_ID),
					"VALUEDRIVER_TYPE": str(GETFBVD.VALUE_DRIVER_TYPE),
					"QTEFBL_RECORD_ID": str(GETFABLOC.QUOTE_FABLOCATION_RECORD_ID),
					"CPQTABLEENTRYDATEADDED": datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"),
					"CPQTABLEENTRYADDEDBY": userName,
					"ADDUSR_RECORD_ID": userId,
				}
				#Trace.Write('169----'+str(tablerow))
				tableInfo.AddRow(tablerow)
				Sql.Upsert(tableInfo)
			GETVALMAS = Sql.GetFirst(
				"Select VALUE_DRIVER_VALUE_RECORD_ID,VALUEDRIVER_COEFFICIENT from PRVDVL(NOLOCK) where VALUEDRIVER_ID ='"
				+ str(getdescription)
				+ "' and VALUEDRIVER_VALUE_DESCRIPTION ='"
				+ str(getvaluedriv)
				+ "'"
			)
			
			if GETVALMAS:				
				GETFABVAL = Sql.GetFirst(
					"SELECT VALUEDRIVER_VALUEDESC,CpqTableEntryId,VALUEDRIVER_VALUE_RECORD_ID from SAQFDV(NOLOCK) where VALUEDRIVER_ID ='"
					+ str(getdescription)
					+ "' and QUOTE_RECORD_ID = '"+str(Qt_rec_id)+"' and FABLOCATION_ID ='"
					+ str(TreeParam)
					+ "'"
				)
				GETFABDRIVERS = Sql.GetFirst(
					"SELECT * FROM SAQFVD WHERE VALUEDRIVER_ID = '"
					+ str(getdescription)
					+ "' and QUOTE_RECORD_ID = '"+str(Qt_rec_id)+"' and FABLOCATION_ID ='"
					+ str(TreeParam)
					+ "' "
				)
				tablerow = {}
				tableInfos = SqlHelper.GetTable("SAQFDV")
				if GETFABVAL:					
					tablerow = {
						"VALUEDRIVER_VALUEDESC": str(getvaluedriv),
						"CpqTableEntryId": GETFABVAL.CpqTableEntryId,
						"VALUEDRIVER_COEFFICIENT":str(GETVALMAS.VALUEDRIVER_COEFFICIENT),
						"VALUEDRIVER_VALUE_RECORD_ID": str(GETVALMAS.VALUE_DRIVER_VALUE_RECORD_ID),
					}
				else:
					tablerow = {"QUOTE_FAB_VALDRIVER_VALUE_RECORD_ID": str(Guid.NewGuid()).upper()}
				tablerow.update(
					{
						"FABLOCATION_ID": str(GETFABDRIVERS.FABLOCATION_ID),
						"VALUEDRIVER_COEFFICIENT":str(GETVALMAS.VALUEDRIVER_COEFFICIENT),
						"FABLOCATION_NAME": str(GETFABDRIVERS.FABLOCATION_NAME),
						"FABLOCATION_RECORD_ID": str(GETFABDRIVERS.FABLOCATION_RECORD_ID),
						"QUOTE_ID": str(GETFABDRIVERS.QUOTE_ID),
						"QUOTE_NAME": str(GETFABDRIVERS.QUOTE_NAME),
						"QUOTE_RECORD_ID": str(GETFABDRIVERS.QUOTE_RECORD_ID),
						"VALUEDRIVER_ID": str(GETFABDRIVERS.VALUEDRIVER_ID),
						"VALUEDRIVER_NAME": str(GETFABDRIVERS.VALUEDRIVER_NAME),
						"VALUEDRIVER_RECORD_ID": str(GETFABDRIVERS.VALUEDRIVER_RECORD_ID),
						"VALUEDRIVER_VALUEDESC": str(getvaluedriv),
						"VALUEDRIVER_VALUE_RECORD_ID": str(GETVALMAS.VALUE_DRIVER_VALUE_RECORD_ID),
						"QUOTE_FABLOCATION_RECORD_ID": str(GETFABDRIVERS.QTEFBL_RECORD_ID),
						"CPQTABLEENTRYDATEADDED": datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"),
						"CPQTABLEENTRYADDEDBY": userName,
						"ADDUSR_RECORD_ID": userId,
					}
				)
				#Trace.Write('225------------------'+str(tablerow))
				tableInfos.AddRow(tablerow)
				Sql.Upsert(tableInfos)
			try:
				quote = Qt_rec_id
				level = "FAB VALUE DRIVER"
				userId = str(User.Id)
				userName = str(User.UserName)
				TreeParam = Product.GetGlobal("TreeParam")
				TreeParentParam = Product.GetGlobal("TreeParentLevel0")
				TreeSuperParentParam = Product.GetGlobal("TreeParentLevel1")
				TreeTopSuperParentParam = Product.GetGlobal("TreeParentLevel2")
				CQTVLDRIFW.iflow_valuedriver_rolldown(quote,level,TreeParam, TreeParentParam, TreeSuperParentParam, TreeTopSuperParentParam,userId,userName)
			except:
				Trace.Write("EXCEPT----QUOTE VALUE DRIVER LEVEL IFLOW")

		elif str(TreeSuperParentParam).upper() == "FAB LOCATIONS" and subtab == "Greenbook Fab Value Drivers":			
			if str(getdescription) == "Quality required by the clients' customers":
				getdescription = "Quality required by the clients'' customers"
			
			QueryStatement = "DELETE FROM SAQFGB WHERE QUOTE_RECORD_ID ='"+str(Qt_rec_id)+"' AND FABLOCATION_ID ='"+str(TreeParentParam)+"' AND GREENBOOK ='"+str(TreeParam)+"'"
			Sql.RunQuery(QueryStatement)
			Parameter = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'SELECT' ")
			primaryQueryItems = SqlHelper.GetFirst(
			""
			+ str(Parameter.QUERY_CRITERIA_1)
			+ " SAQFGB (FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,GREENBOOK,GREENBOOK_RECORD_ID,QTEFBL_RECORD_ID,QUOTE_ID,QUOTE_NAME,QUOTE_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,CpqTableEntryDateModified,QUOTE_FAB_LOC_GB_RECORD_ID) SELECT A. *,getdate(),CONVERT(VARCHAR(4000),NEWID()) FROM (SELECT DISTINCT A.FABLOCATION_ID,A.FABLOCATION_NAME,A.FABLOCATION_RECORD_ID,A.GREENBOOK,A.GREENBOOK_RECORD_ID,A.QTEFBL_RECORD_ID,A.QUOTE_ID,A.QUOTE_NAME,A.QUOTE_RECORD_ID,A.SALESORG_ID,A.SALESORG_NAME,A.SALESORG_RECORD_ID FROM SAQFEQ A left join SAQFGB b on a.QUOTE_RECORD_ID = ''"+str(Qt_rec_id)+"'' and a.QUOTE_ID =b.QUOTE_ID and a.FABLOCATION_RECORD_ID =b.FABLOCATION_RECORD_ID AND a.GREENBOOK = b.GREENBOOK WHERE b.QUOTE_ID IS NULL AND a.FABLOCATION_ID = ''"+str(TreeParentParam)+"'' AND a.GREENBOOK = ''"+str(TreeParam)+"'')A ' " )
			
			GETFABLOC = Sql.GetFirst("SELECT  * FROM SAQFBL(NOLOCK) WHERE QUOTE_RECORD_ID ='"+ str(Qt_rec_id)+ "' and FABLOCATION_ID = '"+ str(TreeParentParam)+ "'")
			QTFAB = GETFABLOC.FABLOCATION_RECORD_ID
			
			GETFBVD = Sql.GetFirst("SELECT * FROM PRBUVD (NOLOCK) WHERE VALUEDRIVER_ID ='"+ str(getdescription)+ "' AND BUSINESSUNIT_ID ='"+str(TreeParam)+"' ")
			SAQFVDENTRY = Sql.GetFirst("Select QUOTE_FAB_LOC_GB_VAL_DRIVER_RECORD_ID FROM SAQFGD(NOLOCK) WHERE QUOTE_RECORD_ID='{}' AND VALUEDRIVER_RECORD_ID='{}'AND FABLOCATION_ID ='{}' AND GREENBOOK ='{}'".format(str(GETFABLOC.QUOTE_RECORD_ID), str(GETFBVD.VALUEDRIVER_RECORD_ID),str(GETFABLOC.FABLOCATION_ID),str(TreeParam)))
			QTGB = Sql.GetFirst("SELECT * FROM SAQFGB(NOLOCK) WHERE GREENBOOK ='"+str(TreeParam)+"' AND FABLOCATION_RECORD_ID ='"+str(QTFAB)+"' ")
			GETVDVD = Sql.GetFirst("SELECT QUOTE_FABLOCATION_VALUEDRIVER_RECORD_ID FROM SAQFVD(NOLOCK) WHERE FABLOCATION_ID ='"+str(TreeParentParam)+"' AND FABLOCATION_RECORD_ID='"+str(QTFAB)+"'")
			if SAQFVDENTRY is None:
				tableInfo = SqlHelper.GetTable("SAQFGD")
				tablerow = {
					"QUOTE_FAB_LOC_GB_VAL_DRIVER_RECORD_ID": str(Guid.NewGuid()).upper(),
					"FABLOCATION_ID": str(GETFABLOC.FABLOCATION_ID),
					"FABLOCATION_NAME": str(GETFABLOC.FABLOCATION_NAME),
					"FABLOCATION_RECORD_ID": str(GETFABLOC.FABLOCATION_RECORD_ID),
					"QUOTE_ID": str(GETFABLOC.QUOTE_ID),
					"QUOTE_NAME": str(GETFABLOC.QUOTE_NAME),
					"QUOTE_RECORD_ID": str(GETFABLOC.QUOTE_RECORD_ID),
					"VALUEDRIVER_ID": str(GETFBVD.VALUEDRIVER_ID),
					"VALUEDRIVER_NAME": str(GETFBVD.VALUEDRIVER_NAME),
					"VALUEDRIVER_RECORD_ID": str(GETFBVD.VALUEDRIVER_RECORD_ID),
					"VALUEDRIVER_TYPE": str(GETFBVD.VALUEDRIVER_TYPE),
					"QTEFBLVDR_RECORD_ID": str(GETVDVD.QUOTE_FABLOCATION_VALUEDRIVER_RECORD_ID),
					"GREENBOOK":str(QTGB.GREENBOOK),
					"GREENBOOK_RECORD_ID": str(QTGB.GREENBOOK_RECORD_ID),
					"CPQTABLEENTRYDATEADDED": datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"),
					"CPQTABLEENTRYADDEDBY": userName,
					"ADDUSR_RECORD_ID": userId,
				}
				#Trace.Write(str(tablerow))
				tableInfo.AddRow(tablerow)
				Sql.Upsert(tableInfo)
				#Trace.Write("GREENVD ADDED" + str(tablerow))
			GETVALMAS = Sql.GetFirst("Select * from PRBDVL(NOLOCK) where VALUEDRIVER_ID ='"+ str(getdescription)+ "' and VALUEDRIVER_VALUE_DESCRIPTION ='"+ str(getvaluedriv)+ "' AND BUSINESSUNIT_ID = '"+str(TreeParam)+"'  ")
			if GETVALMAS is not None:
				GETFABVAL = Sql.GetFirst("SELECT VALUEDRIVER_VALUE_DESCRIPTION,CpqTableEntryId,VALUEDRIVER_VALUE_RECORD_ID from SAQFGV(NOLOCK) where VALUEDRIVER_ID ='"+ str(getdescription)+ "' and FABLOCATION_ID ='"+ str(TreeParentParam)+ "'and GREENBOOK ='"+ str(TreeParam)+ "' AND QUOTE_RECORD_ID ='"+ str(Qt_rec_id)+ "'")
				GETFABDRIVERS = Sql.GetFirst("SELECT * FROM SAQFGD WHERE VALUEDRIVER_ID = '"+ str(getdescription)+ "' and FABLOCATION_ID ='"+ str(TreeParentParam)+ "' and GREENBOOK ='"+ str(TreeParam)+ "' AND QUOTE_RECORD_ID ='"+ str(Qt_rec_id)+ "'")
				tablerow = {}
				tableInfos = SqlHelper.GetTable("SAQFGV")
				if GETFABVAL:					
					tablerow = {"VALUEDRIVER_VALUE_DESCRIPTION": str(getvaluedriv),"CpqTableEntryId": GETFABVAL.CpqTableEntryId,"VALUEDRIVER_VALUE_RECORD_ID": str(GETVALMAS.VALUEDRIVER_VALUE_RECORD_ID)}
				else:					
					tablerow = {"QUOTE_FAB_LOC_GB_VAL_DRIVER_VAL_RECORD_ID": str(Guid.NewGuid()).upper()}
				tablerow.update(
					{
						"FABLOCATION_ID": str(GETFABDRIVERS.FABLOCATION_ID),
						"FABLOCATION_NAME": str(GETFABDRIVERS.FABLOCATION_NAME),
						"FABLOCATION_RECORD_ID": str(GETFABDRIVERS.FABLOCATION_RECORD_ID),
						"QUOTE_ID": str(GETFABDRIVERS.QUOTE_ID),
						"QUOTE_NAME": str(GETFABDRIVERS.QUOTE_NAME),
						"QUOTE_RECORD_ID": str(GETFABDRIVERS.QUOTE_RECORD_ID),
						"VALUEDRIVER_ID": str(GETFABDRIVERS.VALUEDRIVER_ID),
						"VALUEDRIVER_NAME": str(GETFABDRIVERS.VALUEDRIVER_NAME),
						"VALUEDRIVER_RECORD_ID": str(GETFABDRIVERS.VALUEDRIVER_RECORD_ID),
						"GREENBOOK":str(GETFABDRIVERS.GREENBOOK),
						"GREENBOOK_RECORD_ID":str(GETFABDRIVERS.GREENBOOK_RECORD_ID),
						"VALUEDRIVER_VALUE_DESCRIPTION": str(getvaluedriv),
						"VALUEDRIVER_VALUE_CODE": str(GETVALMAS.VALUEDRIVER_VALUE_CODE),
						"VALUEDRIVER_TYPE": str(GETFABDRIVERS.VALUEDRIVER_TYPE),
						"VALUEDRIVER_COEFFICIENT":str(GETVALMAS.VALUEDRIVER_COEFFICIENT),
						"VALUEDRIVER_COEFFICIENT_RECORD_ID":str(GETVALMAS.BU_VALUEDRIVER_VALUE_RECORD_ID),
						"VALUEDRIVER_VALUE_RECORD_ID": str(GETVALMAS.VALUEDRIVER_VALUE_RECORD_ID),
						"CPQTABLEENTRYDATEADDED": datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"),
						"CPQTABLEENTRYADDEDBY": userName,
						"ADDUSR_RECORD_ID": userId
					}
				)
				#Trace.Write(str(tablerow))
				tableInfos.AddRow(tablerow)
				Sql.Upsert(tableInfos)
				#Trace.Write("GREENDV ADDED" + str(tablerow))
			#COEFFICIENTS
			try:
				quote = Qt_rec_id
				level = "FAB GREENBOOK VALUE DRIVER"
				userId = str(User.Id)
				userName = str(User.UserName)
				TreeParam = Product.GetGlobal("TreeParam")
				TreeParentParam = Product.GetGlobal("TreeParentLevel0")
				TreeSuperParentParam = Product.GetGlobal("TreeParentLevel1")
				TreeTopSuperParentParam = Product.GetGlobal("TreeParentLevel2")
				CQTVLDRIFW.iflow_valuedriver_rolldown(quote,level,TreeParam, TreeParentParam, TreeSuperParentParam, TreeTopSuperParentParam,userId,userName)
			except:
				Trace.Write("EXCEPT----FAB GREENBOOK VALUE DRIVER LEVEL IFLOW")

		elif str(TreeSuperParentParam).upper() == "FAB LOCATIONS" and subtab == "Equipment Fab Value Drivers":
			if str(getdescription) == "Quality required by the clients' customers":
				getdescription = "Quality required by the clients'' customers"
			
			GETEQP = Sql.GetFirst("SELECT * FROM SAQFEQ(NOLOCK) WHERE QUOTE_RECORD_ID ='"+ str(Qt_rec_id)+ "' and QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID = '"+ str(CurrentRecordId)+ "'")
			GETPRVD = Sql.GetFirst("SELECT * FROM PRBUVD (NOLOCK) WHERE VALUEDRIVER_ID ='"+ str(getdescription)+ "' AND BUSINESSUNIT_ID ='"+str(TreeParam)+"' ")
			SAQFEDENTRY = Sql.GetFirst("Select QUOTE_FAB_LOC_EQUIP_VAL_DRIVER_RECORD_ID FROM SAQFED(NOLOCK) WHERE QUOTE_RECORD_ID='{}' AND VALUEDRIVER_RECORD_ID='{}' AND EQUIPMENT_ID ='{}' ".format(str(GETEQP.QUOTE_RECORD_ID), str(GETPRVD.VALUEDRIVER_RECORD_ID), str(GETEQP.EQUIPMENT_ID)))
			GETFABDRIVER = Sql.GetFirst("SELECT QUOTE_FABLOCATION_VALUEDRIVER_RECORD_ID FROM SAQFVD(NOLOCK) WHERE FABLOCATION_ID = '"+str(TreeParentParam)+"' ")
			primarykey = str(Guid.NewGuid()).upper()
			if SAQFEDENTRY is None:
				tableInfo = SqlHelper.GetTable("SAQFED")
				tablerow = {
					"QUOTE_FAB_LOC_EQUIP_VAL_DRIVER_RECORD_ID": primarykey,
					"EQUIPMENT_DESCRIPTION": str(GETEQP.EQUIPMENT_DESCRIPTION),
					"EQUIPMENT_ID": str(GETEQP.EQUIPMENT_ID),
					"EQUIPMENT_RECORD_ID": str(GETEQP.EQUIPMENT_RECORD_ID),
					"FABLOCATION_ID": str(GETEQP.FABLOCATION_ID),
					"FABLOCATION_NAME": str(GETEQP.FABLOCATION_NAME),
					"FABLOCATION_RECORD_ID": str(GETEQP.FABLOCATION_RECORD_ID),
					"QUOTE_ID": str(GETEQP.QUOTE_ID),
					"QUOTE_NAME": str(GETEQP.QUOTE_NAME),
					"QUOTE_RECORD_ID": str(GETEQP.QUOTE_RECORD_ID),
					"VALUEDRIVER_ID": str(GETPRVD.VALUEDRIVER_ID),
					"VALUEDRIVER_NAME": str(GETPRVD.VALUEDRIVER_NAME),
					"VALUEDRIVER_RECORD_ID": str(GETPRVD.VALUEDRIVER_RECORD_ID),
					"VALUEDRIVER_TYPE": str(GETPRVD.VALUEDRIVER_TYPE),
					"SERIAL_NUMBER": str(GETEQP.SERIAL_NUMBER),
					"QTEFBLVDR_RECORD_ID": str(GETFABDRIVER.QUOTE_FABLOCATION_VALUEDRIVER_RECORD_ID),
					"GREENBOOK": str(GETEQP.GREENBOOK),
					"GREENBOOK_RECORD_ID": str(GETEQP.GREENBOOK_RECORD_ID),
					"CPQTABLEENTRYDATEADDED": datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"),
					"CPQTABLEENTRYADDEDBY": userName,
					"ADDUSR_RECORD_ID": userId
				}
				#Trace.Write(str(tablerow))
				tableInfo.AddRow(tablerow)
				Sql.Upsert(tableInfo)
				#Trace.Write("EVD ADDED" + str(tablerow))
			GETVALSDV = Sql.GetFirst("SELECT * from PRBDVL where VALUEDRIVER_ID ='"+ str(getdescription)+ "' and VALUEDRIVER_VALUE_DESCRIPTION = '"+ str(getvaluedriv)+ "' and  BUSINESSUNIT_ID = '"+str(TreeParam)+"'")
			# Trace.Write("drivervalueSELECT * from PRBDVL where VALUEDRIVER_ID ='"+ str(getdescription)+ "' and VALUEDRIVER_VALUE_DESCRIPTION = '"+ str(getvaluedriv)+ "' and  BUSINESSUNIT_ID = '"+str(TreeParam)+"'")
			if GETVALSDV is not None:
				GETDRISVD = Sql.GetFirst("SELECT * FROM SAQFED where QUOTE_RECORD_ID = '"+str(Qt_rec_id)+ "' AND GREENBOOK = '"+str(TreeParam)+"' AND EQUIPMENT_ID ='"+(GETEQP.EQUIPMENT_ID)+"'and VALUEDRIVER_ID = '"+str(getdescription)+"' ")
				QTQSDVUPD = Sql.GetFirst("Select QUOTE_FAB_LOC_EQUIP_DRV_VAL_RECORD_ID,CpqTableEntryId FROM SAQEDV(NOLOCK) WHERE QUOTE_RECORD_ID = '"+str(Qt_rec_id)+ "' AND GREENBOOK = '"+str(TreeParam)+"' AND EQUIPMENT_ID='"+str(GETEQP.EQUIPMENT_ID)+"' AND VALUEDRIVER_ID = '"+str(getdescription)+"' ")
				tablerow = {}
				tableInfos = SqlHelper.GetTable("SAQEDV")
				if QTQSDVUPD:
					tablerow = {"CpqTableEntryId": QTQSDVUPD.CpqTableEntryId}
				else:
					tablerow = {"QUOTE_FAB_LOC_EQUIP_DRV_VAL_RECORD_ID": str(Guid.NewGuid()).upper()}
				tablerow.update(
					{
						"QUOTE_ID": str(GETDRISVD.QUOTE_ID),
						"QUOTE_NAME": str(GETDRISVD.QUOTE_NAME),
						"EQUIPMENT_DESCRIPTION": str(GETDRISVD.EQUIPMENT_DESCRIPTION),
						"EQUIPMENT_ID": str(GETDRISVD.EQUIPMENT_ID),
						"EQUIPMENT_RECORD_ID": str(GETDRISVD.EQUIPMENT_RECORD_ID),
						"QUOTE_RECORD_ID": str(GETDRISVD.QUOTE_RECORD_ID),
						"VALUEDRIVER_ID": str(GETDRISVD.VALUEDRIVER_ID),
						"VALUEDRIVER_NAME": str(GETDRISVD.VALUEDRIVER_NAME),
						"VALUEDRIVER_TYPE": str(GETDRISVD.VALUEDRIVER_TYPE),
						"VALUEDRIVER_RECORD_ID": str(GETDRISVD.VALUEDRIVER_RECORD_ID),
						"VALUEDRIVER_VALUE_DESCRIPTION": str(GETVALSDV.VALUEDRIVER_VALUE_DESCRIPTION),
						"VALUEDRIVER_VALUE_RECORD_ID": str(GETVALSDV.VALUEDRIVER_VALUE_RECORD_ID),
						"VALUEDRIVER_VALUE_CODE": str(GETVALSDV.VALUEDRIVER_VALUE_CODE),
						"GREENBOOK": str(GETDRISVD.GREENBOOK),
						"GREENBOOK_RECORD_ID":str(GETDRISVD.GREENBOOK_RECORD_ID),
						"VALUEDRIVER_COEFFICIENT": str(GETVALSDV.VALUEDRIVER_COEFFICIENT),
						"VALUEDRIVER_COEFFICIENT_RECORD_ID": str(GETVALSDV.BU_VALUEDRIVER_VALUE_RECORD_ID),
						"FABLOCATION_ID": str(GETDRISVD.FABLOCATION_ID),
						"FABLOCATION_RECORD_ID": str(GETDRISVD.FABLOCATION_RECORD_ID),
						"FABLOCATION_NAME": str(GETDRISVD.FABLOCATION_NAME),
						"CPQTABLEENTRYDATEADDED": datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"),
						"CPQTABLEENTRYADDEDBY": userName,
						"ADDUSR_RECORD_ID": userId,
					}
				)
				#Trace.Write(str(tablerow))
				tableInfos.AddRow(tablerow)
				Sql.Upsert(tableInfos)
			#FABCOEFF = Sql.GetList("SELECT VALUEDRIVER_COEFFICIENT=SUM(VALUEDRIVER_COEFFICIENT) from SAQEDV WHERE EQUIPMENT_ID = '"+str(GETEQP.EQUIPMENT_ID)+"' and QUOTE_RECORD_ID = '"+str(Qt_rec_id)+"' ")
			QueryStatement = "UPDATE A  SET FAB_VALUEDRIVER_COEFFICIENT = VALUEDRIVER_COEFFICIENT FROM SAQICO A(NOLOCK) JOIN (SELECT QUOTE_RECORD_ID,EQUIPMENT_ID,SUM(VALUEDRIVER_COEFFICIENT) AS VALUEDRIVER_COEFFICIENT from SAQEDV(NOLOCK) WHERE QUOTE_RECORD_ID = '"+str(Qt_rec_id)+"' AND FABLOCATION_ID ='"+str(TreeParentParam)+"'AND GREENBOOK = '"+str(TreeParam)+"' AND EQUIPMENT_ID = '"+str(GETEQP.EQUIPMENT_ID)+"' GROUP BY QUOTE_RECORD_ID,EQUIPMENT_ID) B ON A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID"
			Sql.RunQuery(QueryStatement)
	return 'data'


def costsave(ACTION,CurrentRecordId,SerLocateDT,getfabid,subtab):	
	TreeParam = Product.GetGlobal("TreeParam")
	TreeParentParam = Product.GetGlobal("TreeParentLevel0")
	TreeSuperParentParam = Product.GetGlobal("TreeParentLevel1")
	TreeTopSuperParentParam = Product.GetGlobal("TreeParentLevel2")
	userId = str(User.Id)
	userName = str(User.UserName)
	#getQuoteId = SqlHelper.GetFirst("SELECT QUOTE_ID FROM SAQTMT WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{}'".format(Qt_rec_id))
	#DELETE_SYELOG = """DELETE FROM SYELOG WHERE ERRORMESSAGE_RECORD_ID = 'EBDD1157-CD03-409E-8257-57A36753360E' AND OBJECT_VALUE_REC_ID = '{}'""".format(getQuoteId.QUOTE_ID)
	#Sql.RunQuery(DELETE_SYELOG)
	if str(TreeParentParam) == 'Comprehensive Services':
		GETSEVC = Sql.GetFirst ("SELECT * from SAQTSV where QUOTE_RECORD_ID = '" + str(Qt_rec_id)+ "' AND SERVICE_ID ='"+ str(TreeParam)+ "'") #SAQSFB
		for val in SerLocateDT:			
			getval = str(val).replace("('","").replace("',)","")
			getdescription =getval.split('=')[0]			
			#getvaluedriv = getval.split('-')[1]
			getvaluedriv = getval.partition('=')[2]
			
			if str(getdescription) == "Customer's ability to self-service":
					getdescription = "Customer''s ability to self-service"
			GETSVD = Sql.GetFirst("SELECT * FROM PRSVDR (NOLOCK) WHERE VALUEDRIVER_TYPE = 'TOOL BASED' AND VALUEDRIVER_ID ='"+ str(getdescription)+ "' ")
			SAQFVDENTRY = Sql.GetFirst(
				"Select QUOTE_SERVICE_TOOL_VALUE_DRIVER_RECORD_ID FROM SAQSVD(NOLOCK) WHERE QUOTE_RECORD_ID='{}' AND TOOL_VALUEDRIVER_RECORD_ID='{}' AND QTESRV_RECORD_ID ='{}'".format(
					str(GETSEVC.QUOTE_RECORD_ID), str(GETSVD.VALUEDRIVER_RECORD_ID),str(GETSEVC.QUOTE_SERVICE_RECORD_ID)
				)
			)
			# Trace.Write("bSelect QUOTE_FABLOCATION_VALUEDRIVER_RECORD_ID FROM SAQFVD(NOLOCK) WHERE QUOTE_RECORD_ID='{}' AND VALUEDRIVER_RECORD_ID='{}' ".format(str(GETFABLOC.QUOTE_RECORD_ID),str(GETFBVD.VALUE_DRIVER_RECORD_ID)))
			primarykey = str(Guid.NewGuid()).upper()
			if SAQFVDENTRY is None:
				tableInfo = SqlHelper.GetTable("SAQSVD") #SAQSFD
				tablerow = {
					"QUOTE_SERVICE_TOOL_VALUE_DRIVER_RECORD_ID": primarykey,
					"SERVICE_DESCRIPTION": str(GETSEVC.SERVICE_DESCRIPTION),
					"SERVICE_ID": str(GETSEVC.SERVICE_ID),
					"SERVICE_RECORD_ID": str(GETSEVC.SERVICE_RECORD_ID),
					"QUOTE_ID": str(GETSEVC.QUOTE_ID),
					"QUOTE_NAME": str(GETSEVC.QUOTE_NAME),
					"QUOTE_RECORD_ID": str(GETSEVC.QUOTE_RECORD_ID),
					"TOOL_VALUEDRIVER_ID": str(GETSVD.VALUEDRIVER_ID),
					"TOOL_VALUEDRIVER_RECORD_ID": str(GETSVD.VALUEDRIVER_RECORD_ID),
					"QTESRV_RECORD_ID": str(GETSEVC.QUOTE_SERVICE_RECORD_ID),
					"SALESORG_ID": str(GETSEVC.SALESORG_ID),
					"SALESORG_NAME": str(GETSEVC.SALESORG_NAME),
					"SALESORG_RECORD_ID": str(GETSEVC.SALESORG_RECORD_ID),
					"CPQTABLEENTRYDATEADDED": datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"),
					"CPQTABLEENTRYADDEDBY": userName,
					"ADDUSR_RECORD_ID": userId,
				}
				
				#Trace.Write(str(tablerow))
				tableInfo.AddRow(tablerow)
				Sql.Upsert(tableInfo)
				#Trace.Write("serVD ADDED" + str(tablerow))
			GETVALSDV = Sql.GetFirst(
				"SELECT * from PRSDVL(NOLOCK) where VALUEDRIVER_ID ='"
				+ str(getdescription)
				+ "' and VALUEDRIVER_VALUE_DESCRIPTION = '"
				+ str(getvaluedriv)
				+ "' and SERVICE_ID = '"
				+ str(TreeParam)
				+ "'"
			)
			# Trace.Write(
			# 	"drivervalueSELECT * from PRSDVL(NOLOCK) where VALUEDRIVER_ID ='"
			# 	+ str(getdescription)
			# 	+ "' and VALUEDRIVER_VALUE_DESCRIPTION = '"
			# 	+ str(getvaluedriv)
			# 	+ "'"
			# 	) 
			if GETVALSDV is not None:
				GETDRISVD = Sql.GetFirst(
					"SELECT * from SAQSVD where TOOL_VALUEDRIVER_ID ='"
					+ str(getdescription)
					+ "' AND QUOTE_RECORD_ID = '"
					+ str(Qt_rec_id)
					+ "' AND QTESRV_RECORD_ID ='"
					+ str(GETSEVC.QUOTE_SERVICE_RECORD_ID)
					+ "'"
				)
				QTQSDVUPD = Sql.GetFirst(
					"Select QUOTE_SERVICE_TOOL_VALUE_DRIVER_VALUES_RECORD_ID,CpqTableEntryId FROM SAQSDV(NOLOCK) WHERE TOOL_VALUEDRIVER_ID ='"
					+ str(getdescription)
					+ "' AND QUOTE_RECORD_ID = '"
					+ str(Qt_rec_id)
					+ "'AND QTESRV_RECORD_ID ='"
					+ str(GETSEVC.QUOTE_SERVICE_RECORD_ID)
					+ "' "
				)
				tablerow = {}
				tableInfos = SqlHelper.GetTable("SAQSDV") #QTQSFV
				if QTQSDVUPD:
					tablerow = {"CpqTableEntryId": QTQSDVUPD.CpqTableEntryId}
				else:
					tablerow = {"QUOTE_SERVICE_TOOL_VALUE_DRIVER_VALUES_RECORD_ID": str(Guid.NewGuid()).upper()}
				tablerow.update(
					{
						"QUOTE_ID": str(GETDRISVD.QUOTE_ID),
						"QUOTE_NAME": str(GETDRISVD.QUOTE_NAME),
						"QTESRV_RECORD_ID": str(GETDRISVD.QTESRV_RECORD_ID),
						"SERVICE_DESCRIPTION": str(GETDRISVD.SERVICE_DESCRIPTION),
						"SERVICE_ID": str(GETDRISVD.SERVICE_ID),
						"SERVICE_RECORD_ID": str(GETDRISVD.SERVICE_RECORD_ID),
						"TOOL_VALUEDRIVER_ID": str(GETDRISVD.TOOL_VALUEDRIVER_ID),
						"TOOL_VALUEDRIVER_RECORD_ID": str(GETDRISVD.TOOL_VALUEDRIVER_RECORD_ID),
						"TOOL_VALUEDRIVER_VALUE_DESCRIPTION": str(getvaluedriv),
						"QTESRVVDR_RECORD_ID": str(GETDRISVD.QUOTE_SERVICE_TOOL_VALUE_DRIVER_RECORD_ID),
						"TOOL_VALUEDRIVER_VALUE_RECORD_ID": str(GETVALSDV.VALUEDRIVER_VALUE_RECORD_ID),
						"QUOTE_RECORD_ID": str(GETDRISVD.QUOTE_RECORD_ID),
						"SALESORG_ID": str(GETDRISVD.SALESORG_ID),
						"SALESORG_NAME": str(GETDRISVD.SALESORG_NAME),
						"TOOL_VALUEDRIVER_VALUE_CODE": str(GETVALSDV.VALUEDRIVER_VALUE_CODE),
						"VALUEDRIVER_COEFFICIENT": str(GETVALSDV.VALUEDRIVER_COEFFICIENT),
						"VALUEDRIVER_COEFFICIENT_RECORD_ID": str(GETVALSDV.SERVICE_VALUEDRIVER_VALUE_RECORD_ID),
						"SALESORG_RECORD_ID": str(GETDRISVD.SALESORG_RECORD_ID),
						"CPQTABLEENTRYDATEADDED": datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"),
						"CPQTABLEENTRYADDEDBY": userName,
						"ADDUSR_RECORD_ID": userId,
					}
				)
				#Trace.Write(str(tablerow))
				tableInfos.AddRow(tablerow)
				Sql.Upsert(tableInfos)
		try:
			quote = Qt_rec_id
			level = "SERVICE COST AND VALUE DRIVERS"
			userId = str(User.Id)
			userName = str(User.UserName)
			TreeParam = Product.GetGlobal("TreeParam")
			
			TreeParentParam = Product.GetGlobal("TreeParentLevel0")
			TreeSuperParentParam = Product.GetGlobal("TreeParentLevel1")
			TreeTopSuperParentParam = Product.GetGlobal("TreeParentLevel2")

			CQTVLDRIFW.iflow_valuedriver_rolldown(quote,level,TreeParam, TreeParentParam, TreeSuperParentParam, TreeTopSuperParentParam,userId,userName)
		except:
			Trace.Write("EXCEPT----SERVICE COST AND VALUE DRIVER LEVEL IFLOW")

				
	elif str(TreeSuperParentParam) == 'Comprehensive Services':
		#QueryStatement = "DELETE FROM SAQSFB WHERE QUOTE_RECORD_ID ='"+str(Qt_rec_id)+"' AND SERVICE_ID = '" + str(TreeParentParam) + "' AND FABLOCATION_ID = '" + str(TreeParam) + "'"
		#Sql.RunQuery(QueryStatement)
		# ADDING GREEN BOOK TO ALREADY AVAILABLE COVERED OBJECTS 1520 
		#Parameter = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'SELECT' ")
		#primaryQueryItems = SqlHelper.GetFirst(
		#""
		# str(Parameter.QUERY_CRITERIA_1)
		#+ " SAQSFB (FABLOCATION_ID,FABLOCATION_NAME, FABLOCATION_RECORD_ID,SERVICE_ID,SERVICE_DESCRIPTION,SERVICE_RECORD_ID,QUOTE_ID,QUOTE_NAME,QUOTE_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,CpqTableEntryDateModified,QUOTE_SERVICE_FAB_LOCATION_RECORD_ID) SELECT A. *,getdate(),CONVERT(VARCHAR(4000),NEWID()) FROM (SELECT DISTINCT A.FABLOCATION_ID,A.FABLOCATION_NAME,A.FABLOCATION_RECORD_ID,A.SERVICE_ID,A.SERVICE_DESCRIPTION,A.SERVICE_RECORD_ID,A.QUOTE_ID,A.QUOTE_NAME,A.QUOTE_RECORD_ID,A.SALESORG_ID,A.SALESORG_NAME,A.SALESORG_RECORD_ID FROM SAQSCO A left join SAQSFB b on a.QUOTE_RECORD_ID = ''"+str(Qt_rec_id)+"'' and a.QUOTE_ID =b.QUOTE_ID and a.SERVICE_RECORD_ID =b.SERVICE_RECORD_ID AND A.FABLOCATION_ID = B.FABLOCATION_ID WHERE b.QUOTE_ID IS NULL )A ' " )
		#""" Trace.Write(""
		#+ str(Parameter.QUERY_CRITERIA_1)
		#+ " SAQSFB (FABLOCATION_ID,FABLOCATION_NAME, FABLOCATION_RECORD_ID,SERVICE_ID,SERVICE_DESCRIPTION,SERVICE_RECORD_ID,QUOTE_ID,QUOTE_NAME,QUOTE_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,CpqTableEntryDateModified,QUOTE_SERVICE_FAB_LOCATION_RECORD_ID) SELECT A. *,getdate(),CONVERT(VARCHAR(4000),NEWID()) FROM (SELECT DISTINCT A.FABLOCATION_ID,A.FABLOCATION_NAME,A.FABLOCATION_RECORD_ID,A.SERVICE_ID,A.SERVICE_DESCRIPTION,A.SERVICE_RECORD_ID,A.QUOTE_ID,A.QUOTE_NAME,A.QUOTE_RECORD_ID,A.SALESORG_ID,A.SALESORG_NAME,A.SALESORG_RECORD_ID FROM SAQSCO A left join SAQSFB b on a.QUOTE_RECORD_ID = ''"+str(Qt_rec_id)+"'' and a.QUOTE_ID =b.QUOTE_ID and a.SERVICE_RECORD_ID =b.SERVICE_RECORD_ID AND A.FABLOCATION_ID = B.FABLOCATION_ID WHERE b.QUOTE_ID IS NULL )A ' ") """
		GETSEVC = Sql.GetFirst ("SELECT * from SAQSFB where QUOTE_RECORD_ID = '" + str(Qt_rec_id)+ "' AND FABLOCATION_ID ='"+ str(TreeParam)+ "' AND SERVICE_ID ='" + str(TreeParentParam)+ "'") #SAQSFB
		for val in SerLocateDT:			
			getval = str(val).replace("('","").replace("',)","")
			getdescription =getval.split('=')[0]			
			#getvaluedriv = getval.split('-')[1]
			getvaluedriv = getval.partition('=')[2]
			
			if str(getdescription) == "Customer's ability to self-service":
					getdescription = "Customer''s ability to self-service"
			GETSVD = Sql.GetFirst("SELECT * FROM PRSVDR (NOLOCK) WHERE VALUEDRIVER_TYPE = 'TOOL BASED' AND VALUEDRIVER_ID ='"+ str(getdescription)+ "' ")
			SAQFVDENTRY = Sql.GetFirst(
				"Select QUOTE_SERVICE_FBL_TOOL_VAL_DRV_RECORD_ID FROM SAQSFD(NOLOCK) WHERE QUOTE_RECORD_ID='{}' AND VALUEDRIVER_RECORD_ID='{}' AND FABLOCATION_ID ='{}' AND SERVICE_ID = '{}'".format(
					str(GETSEVC.QUOTE_RECORD_ID), str(GETSVD.VALUEDRIVER_RECORD_ID),str(TreeParam),str(TreeParentParam)
				)
			)
			# Trace.Write("bSelect QUOTE_FABLOCATION_VALUEDRIVER_RECORD_ID FROM SAQFVD(NOLOCK) WHERE QUOTE_RECORD_ID='{}' AND VALUEDRIVER_RECORD_ID='{}' ".format(str(GETFABLOC.QUOTE_RECORD_ID),str(GETFBVD.VALUE_DRIVER_RECORD_ID)))
			primarykey = str(Guid.NewGuid()).upper()
			if SAQFVDENTRY is None:
				tableInfo = SqlHelper.GetTable("SAQSFD") #SAQSFD
				tablerow = {
					"QUOTE_SERVICE_FBL_TOOL_VAL_DRV_RECORD_ID": primarykey,
					"SERVICE_DESCRIPTION": str(GETSEVC.SERVICE_DESCRIPTION),
					"SERVICE_ID": str(GETSEVC.SERVICE_ID),
					"SERVICE_RECORD_ID": str(GETSEVC.SERVICE_RECORD_ID),
					"FABLOCATION_ID": str(TreeParam),
					"FABLOCATION_NAME":str(GETSEVC.FABLOCATION_NAME),
					"FABLOCATION_RECORD_ID":str(GETSEVC.FABLOCATION_RECORD_ID),
					"QUOTE_ID": str(GETSEVC.QUOTE_ID),
					"QUOTE_NAME": str(GETSEVC.QUOTE_NAME),
					"QUOTE_RECORD_ID": str(GETSEVC.QUOTE_RECORD_ID),
					"VALUEDRIVER_ID": str(GETSVD.VALUEDRIVER_ID),
					"VALUEDRIVER_RECORD_ID": str(GETSVD.VALUEDRIVER_RECORD_ID),
					#"QTESRV_RECORD_ID": str(GETSEVC.QUOTE_SERVICE_RECORD_ID),
					"SALESORG_ID": str(GETSEVC.SALESORG_ID),
					"SALESORG_NAME": str(GETSEVC.SALESORG_NAME),
					"SALESORG_RECORD_ID": str(GETSEVC.SALESORG_RECORD_ID),
					"CPQTABLEENTRYDATEADDED": datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"),
					"CPQTABLEENTRYADDEDBY": userName,
					"ADDUSR_RECORD_ID": userId,
				}
				
				#Trace.Write(str(tablerow))
				tableInfo.AddRow(tablerow)
				Sql.Upsert(tableInfo)
				#Trace.Write("serVD ADDED" + str(tablerow))
			GETVALSDV = Sql.GetFirst(
				"SELECT * from PRSDVL(NOLOCK) where VALUEDRIVER_ID ='"
				+ str(getdescription)
				+ "' and VALUEDRIVER_VALUE_DESCRIPTION = '"
				+ str(getvaluedriv)
				+ "' and SERVICE_ID = '"
				+ str(TreeParentParam)
				+ "'"
			)
			# Trace.Write(
			# 	"drivervalueSELECT * from PRSDVL(NOLOCK) where VALUEDRIVER_ID ='"
			# 	+ str(getdescription)
			# 	+ "' and VALUEDRIVER_VALUE_DESCRIPTION = '"
			# 	+ str(getvaluedriv)
			# 	+ "'"
			# 	) 
			if GETVALSDV is not None:
				GETDRISVD = Sql.GetFirst(
					"SELECT * from SAQSFD where VALUEDRIVER_ID ='"
					+ str(getdescription)
					+ "' AND QUOTE_RECORD_ID = '"
					+ str(Qt_rec_id)
					+ "' AND SERVICE_ID ='"
					+ str(TreeParentParam)
					+ "' AND FABLOCATION_ID ='"
					+ str(TreeParam)
					+ "'"
				)
				QTQSDVUPD = Sql.GetFirst(
					"Select QUOTE_SERVICE_FAB_LOC_DRV_VAL_RECORD_ID,CpqTableEntryId FROM SAQSFV(NOLOCK) WHERE VALUEDRIVER_ID ='"
					+ str(getdescription)
					+ "' AND QUOTE_RECORD_ID = '"
					+ str(Qt_rec_id)
					+ "' AND SERVICE_ID ='"
					+ str(TreeParentParam)
					+ "' AND FABLOCATION_ID ='"
					+ str(TreeParam)
					+ "'"
				)
				tablerow = {}
				tableInfos = SqlHelper.GetTable("SAQSFV") #SAQSFV
				if QTQSDVUPD:
					tablerow = {"CpqTableEntryId": QTQSDVUPD.CpqTableEntryId}
				else:
					tablerow = {"QUOTE_SERVICE_FAB_LOC_DRV_VAL_RECORD_ID": str(Guid.NewGuid()).upper()}
				tablerow.update(
					{
						"QUOTE_ID": str(GETDRISVD.QUOTE_ID),
						"QUOTE_NAME": str(GETDRISVD.QUOTE_NAME),
						#"QTESRV_RECORD_ID": str(GETDRISVD.QTESRV_RECORD_ID),
						"SERVICE_DESCRIPTION": str(GETDRISVD.SERVICE_DESCRIPTION),
						"SERVICE_ID": str(GETDRISVD.SERVICE_ID),
						"SERVICE_RECORD_ID": str(GETDRISVD.SERVICE_RECORD_ID),
						"FABLOCATION_ID": str(GETDRISVD.FABLOCATION_ID),
						"FABLOCATION_NAME":str(GETDRISVD.FABLOCATION_NAME),
						"FABLOCATION_RECORD_ID":str(GETDRISVD.FABLOCATION_RECORD_ID),
						"VALUEDRIVER_ID": str(GETDRISVD.VALUEDRIVER_ID),
						"VALUEDRIVER_RECORD_ID": str(GETDRISVD.VALUEDRIVER_RECORD_ID),
						"VALUEDRIVER_VALUE_DESCRIPTION": str(getvaluedriv),
						#"QTESRVVDR_RECORD_ID": str(GETDRISVD.QUOTE_SERVICE_TOOL_VALUE_DRIVER_RECORD_ID),
						#"TOOL_VALUEDRIVER_VALUE_RECORD_ID": str(GETVALSDV.VALUEDRIVER_VALUE_RECORD_ID),
						"QUOTE_RECORD_ID": str(GETDRISVD.QUOTE_RECORD_ID),
						"SALES_ORG_ID": str(GETDRISVD.SALESORG_ID),
						"SALES_ORG_NAME": str(GETDRISVD.SALESORG_NAME),
						#"TOOL_VALUEDRIVER_VALUE_CODE": str(GETVALSDV.VALUEDRIVER_VALUE_CODE),
						"VALUEDRIVER_COEFFICIENT": str(GETVALSDV.VALUEDRIVER_COEFFICIENT),
						"VALUEDRIVER_COEFFICIENT_RECORD_ID": str(GETVALSDV.SERVICE_VALUEDRIVER_VALUE_RECORD_ID),
						"SALESORG_RECORD_ID": str(GETDRISVD.SALESORG_RECORD_ID),
						"CPQTABLEENTRYDATEADDED": datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"),
						"CPQTABLEENTRYADDEDBY": userName,
						"ADDUSR_RECORD_ID": userId,
					}
				)
				#Trace.Write(str(tablerow))
				tableInfos.AddRow(tablerow)
				Sql.Upsert(tableInfos)
		# COEFFICIENTS SUM at Level 1
		
		try:
			quote = Qt_rec_id
			level = "FAB COST AND VALUE DRIVER"
			userId = str(User.Id)
			userName = str(User.UserName)
			TreeParam = Product.GetGlobal("TreeParam")
			TreeParentParam = Product.GetGlobal("TreeParentLevel0")
			TreeSuperParentParam = Product.GetGlobal("TreeParentLevel1")
			TreeTopSuperParentParam = Product.GetGlobal("TreeParentLevel2")

			CQTVLDRIFW.iflow_valuedriver_rolldown(quote,level,TreeParam, TreeParentParam, TreeSuperParentParam, TreeTopSuperParentParam,userId,userName)
		except:
			Trace.Write("EXCEPT----FAB COST AND VALUE DRIVER LEVEL IFLOW")
				
	elif str(TreeTopSuperParentParam) == 'Comprehensive Services' and subtab == 'Greenbook Cost and Value Drivers':		
		for val in SerLocateDT:			
			getval = str(val).replace("('","").replace("',)","")
			getdescription =getval.split('=')[0]
			getvaluedriv = getval.partition('=')[2]
			
			if str(getdescription) == "Customer's ability to self-service":
					getdescription = "Customer''s ability to self-service"
			QueryStatement = "DELETE FROM SAQSGB WHERE QUOTE_RECORD_ID ='"+str(Qt_rec_id)+"' AND SERVICE_ID ='"+str(TreeSuperParentParam)+"' AND FABLOCATION_ID = '" + str(TreeParentParam) + "' AND GREENBOOK = '" + str(TreeParam) + "'"
			Sql.RunQuery(QueryStatement)
			Parameter = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'SELECT' ")
			primaryQueryItems = SqlHelper.GetFirst(
			""
			+ str(Parameter.QUERY_CRITERIA_1)
			+ " SAQSGB (SERVICE_ID,SERVICE_DESCRIPTION,SERVICE_RECORD_ID,GREENBOOK,GREENBOOK_RECORD_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,QUOTE_ID,QUOTE_NAME,QUOTE_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,CpqTableEntryDateModified,QUOTE_SERVICE_GREENBOOK_RECORD_ID) SELECT A. *,getdate(),CONVERT(VARCHAR(4000),NEWID()) FROM (SELECT DISTINCT A.SERVICE_ID,A.SERVICE_DESCRIPTION,A.SERVICE_RECORD_ID,A.GREENBOOK,A.GREENBOOK_RECORD_ID,A.FABLOCATION_ID,A.FABLOCATION_NAME,A.FABLOCATION_RECORD_ID,A.QUOTE_ID,A.QUOTE_NAME,A.QUOTE_RECORD_ID,A.SALESORG_ID,A.SALESORG_NAME,A.SALESORG_RECORD_ID FROM SAQSCO A left join SAQSGB b on a.QUOTE_RECORD_ID = ''2CA6A7C0-6526-4829-AFEB-767DC9A72CF8'' and a.QUOTE_ID = b.QUOTE_ID and a.SERVICE_RECORD_ID =b.SERVICE_RECORD_ID AND a.FABLOCATION_ID = b.FABLOCATION_ID AND a.GREENBOOK = b.GREENBOOK WHERE b.QUOTE_ID IS NULL AND a.SERVICE_ID = ''{treeSuperParentParam}''AND a.FABLOCATION_ID =''{treeparentparam}'' AND a.GREENBOOK = ''{treeparam}'')A ' ".format(treeparentparam=TreeParentParam,treeparam=TreeParam,treeSuperParentParam=TreeSuperParentParam))
			GETSEVC = Sql.GetFirst ("SELECT * from SAQSGB where QUOTE_RECORD_ID = '"+ str(Qt_rec_id)+ "' AND SERVICE_ID ='"+str(TreeSuperParentParam)+"' AND FABLOCATION_ID = '" + str(TreeParentParam) + "' AND GREENBOOK = '" + str(TreeParam) + "'")
			GETSVD = Sql.GetFirst("SELECT * FROM PRSVDR (NOLOCK) WHERE VALUEDRIVER_TYPE = 'TOOL BASED' AND VALUEDRIVER_ID ='"+ str(getdescription)+ "' ")
			SAQFVDENTRY = Sql.GetFirst(
				"Select QUOTE_SERVICE_GREENBOOK_VAL_DRV_RECORD_ID FROM SAQSGD(NOLOCK) WHERE QUOTE_RECORD_ID='{}' AND TOOL_VALUEDRIVER_RECORD_ID='{}' AND SERVICE_RECORD_ID ='{}' and FABLOCATION_ID ='{}' and GREENBOOK = '{}'".format(
					str(GETSEVC.QUOTE_RECORD_ID), str(GETSVD.VALUEDRIVER_RECORD_ID),str(GETSEVC.SERVICE_RECORD_ID),str(TreeParentParam),str(TreeParam)
				)
			)
			primarykey = str(Guid.NewGuid()).upper()
			if SAQFVDENTRY is None:
				tableInfo = SqlHelper.GetTable("SAQSGD")
				tablerow = {
					"QUOTE_SERVICE_GREENBOOK_VAL_DRV_RECORD_ID": primarykey,
					"SERVICE_DESCRIPTION": str(GETSEVC.SERVICE_DESCRIPTION),
					"SERVICE_ID": str(TreeSuperParentParam),
					"SERVICE_RECORD_ID": str(GETSEVC.SERVICE_RECORD_ID),
					"QUOTE_ID": str(GETSEVC.QUOTE_ID),
					"QUOTE_NAME": str(GETSEVC.QUOTE_NAME),
					"QUOTE_RECORD_ID": str(GETSEVC.QUOTE_RECORD_ID),
					"TOOL_VALUEDRIVER_ID": str(GETSVD.VALUEDRIVER_ID),
					"TOOL_VALUEDRIVER_RECORD_ID": str(GETSVD.VALUEDRIVER_RECORD_ID),
					"GREENBOOK": str(TreeParam),
					"GREENBOOK_RECORD_ID": str(GETSEVC.GREENBOOK_RECORD_ID),
					"SALESORG_ID": str(GETSEVC.SALESORG_ID),
					"SALESORG_NAME": str(GETSEVC.SALESORG_NAME),
					"SALESORG_RECORD_ID": str(GETSEVC.SALESORG_RECORD_ID),
					"CPQTABLEENTRYDATEADDED": datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"),
					"CPQTABLEENTRYADDEDBY": userName,
					"ADDUSR_RECORD_ID": userId,
					"QTESRVFBL_RECORD_ID": str(GETSEVC.QTESRVFBL_RECORD_ID),
					"QTESRVGBK_RECORD_ID":str(GETSEVC.QUOTE_SERVICE_GREENBOOK_RECORD_ID),
					"FABLOCATION_RECORD_ID":str(GETSEVC.FABLOCATION_RECORD_ID),
					"FABLOCATION_ID":str(GETSEVC.FABLOCATION_ID),
					"FABLOCATION_NAME":str(GETSEVC.FABLOCATION_NAME)
					#"QUOTE_SERVICE_GREENBOOK_RECORD_ID":str(GETSEVC.QTESRVGBK_RECORD_ID)
				}
				
				#Trace.Write(str(tablerow))
				tableInfo.AddRow(tablerow)
				Sql.Upsert(tableInfo)
				#Trace.Write("serVD ADDED" + str(tablerow))
			GETVALSDV = Sql.GetFirst("SELECT * from PRSDVL(NOLOCK) where VALUEDRIVER_ID ='"+ str(getdescription)+ "' and VALUEDRIVER_VALUE_DESCRIPTION = '"+ str(getvaluedriv)+ "' and SERVICE_ID = '"+ str(TreeSuperParentParam)+"'")
			if GETVALSDV is not None:
				GETDRISVD = Sql.GetFirst("SELECT * from SAQSGD where TOOL_VALUEDRIVER_ID ='"+ str(getdescription)+ "' AND QUOTE_RECORD_ID = '"+ str(Qt_rec_id)+ "' AND SERVICE_ID ='"+ str(TreeSuperParentParam)+ "' AND FABLOCATION_ID = '" + str(TreeParentParam) + "' AND GREENBOOK = '"+ str(TreeParam)+"'")
				QTQSDVUPD = Sql.GetFirst("Select QUOTE_SERVICE_GBK_VAL_DRV_VAL_RECORD_ID,CpqTableEntryId FROM SAQSGV(NOLOCK) WHERE TOOL_VALUEDRIVER_ID ='"+ str(getdescription)+ "' AND QUOTE_RECORD_ID = '"+ str(Qt_rec_id)+ "'AND SERVICE_ID ='"+ str(TreeSuperParentParam)+ "' AND FABLOCATION_ID = '" + str(TreeParentParam) + "' AND GREENBOOK = '"+str(TreeParam)+"'")
				tablerow = {}
				tableInfos = SqlHelper.GetTable("SAQSGV")
				if QTQSDVUPD:
					tablerow = {"CpqTableEntryId": QTQSDVUPD.CpqTableEntryId}
				else:
					tablerow = {"QUOTE_SERVICE_GBK_VAL_DRV_VAL_RECORD_ID": str(Guid.NewGuid()).upper()}
				tablerow.update(
					{
						"QUOTE_ID": str(GETDRISVD.QUOTE_ID),
						"QUOTE_NAME": str(GETDRISVD.QUOTE_NAME),
						"GREENBOOK": str(GETDRISVD.GREENBOOK),
						"GREENBOOK_RECORD_ID": str(GETDRISVD.GREENBOOK_RECORD_ID),
						"SERVICE_DESCRIPTION": str(GETDRISVD.SERVICE_DESCRIPTION),
						"SERVICE_ID": str(GETDRISVD.SERVICE_ID),
						"SERVICE_RECORD_ID": str(GETDRISVD.SERVICE_RECORD_ID),
						"TOOL_VALUEDRIVER_ID": str(GETDRISVD.TOOL_VALUEDRIVER_ID),
						"TOOL_VALUEDRIVER_RECORD_ID": str(GETDRISVD.TOOL_VALUEDRIVER_RECORD_ID),
						"TOOL_VALUEDRIVER_VALUE_DESCRIPTION": str(getvaluedriv),
						#"QTESRVVDR_RECORD_ID": str(GETDRISVD.QUOTE_SERVICE_TOOL_VALUE_DRIVER_RECORD_ID),
						"QTESRVGBK_RECORD_ID":str(GETSEVC.QUOTE_SERVICE_GREENBOOK_RECORD_ID),
						"TOOL_VALUEDRIVER_VALUE_RECORD_ID": str(GETVALSDV.VALUEDRIVER_VALUE_RECORD_ID),
						"QUOTE_RECORD_ID": str(GETDRISVD.QUOTE_RECORD_ID),
						"SALESORG_ID": str(GETDRISVD.SALESORG_ID),
						"SALESORG_NAME": str(GETDRISVD.SALESORG_NAME),
						"TOOL_VALUEDRIVER_VALUE_CODE": str(GETVALSDV.VALUEDRIVER_VALUE_CODE),
						"VALUEDRIVER_COEFFICIENT": str(GETVALSDV.VALUEDRIVER_COEFFICIENT),
						"VALUEDRIVER_COEFFICIENT_RECORD_ID": str(GETVALSDV.SERVICE_VALUEDRIVER_VALUE_RECORD_ID),
						"SALESORG_RECORD_ID": str(GETDRISVD.SALESORG_RECORD_ID),
						"QTESRVFBL_RECORD_ID": str(GETDRISVD.QTESRVFBL_RECORD_ID),
						"FABLOCATION_RECORD_ID":str(GETDRISVD.FABLOCATION_RECORD_ID),
						"FABLOCATION_ID":str(GETDRISVD.FABLOCATION_ID),
						"FABLOCATION_NAME":str(GETDRISVD.FABLOCATION_NAME),
						#"QUOTE_SERVICE_GREENBOOK_RECORD_ID":str(GETDRISVD.QTESRVGBK_RECORD_ID),
						"CPQTABLEENTRYDATEADDED": datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"),
						"CPQTABLEENTRYADDEDBY": userName,
						"ADDUSR_RECORD_ID": userId
					}
				)
				#Trace.Write(str(tablerow))
				tableInfos.AddRow(tablerow)
				Sql.Upsert(tableInfos)
		
		try:
			quote = Qt_rec_id
			level = "GREENBOOK COST AND VALUE DRIVERS"
			userId = str(User.Id)
			userName = str(User.UserName)
			TreeParam = Product.GetGlobal("TreeParam")
			TreeParentParam = Product.GetGlobal("TreeParentLevel0")
			TreeSuperParentParam = Product.GetGlobal("TreeParentLevel1")
			TreeTopSuperParentParam = Product.GetGlobal("TreeParentLevel2")

			CQTVLDRIFW.iflow_valuedriver_rolldown(quote,level,TreeParam, TreeParentParam, TreeSuperParentParam, TreeTopSuperParentParam,userId,userName)
		except:
			Trace.Write("EXCEPT----GREENBOOK COST AND VALUE DRIVER LEVEL IFLOW")
	elif str(TreeTopSuperParentParam) == 'Comprehensive Services' and subtab == 'Equipment Cost and Value Drivers':
		for val in SerLocateDT:			
			getval = str(val).replace("('","").replace("',)","")
			getdescription =getval.split('=')[0]
			getvaluedriv = getval.partition('=')[2]
			
			if str(getdescription) == "Customer's ability to self-service":
					getdescription = "Customer''s ability to self-service"
		#EQUIPMENT COST AND DRIVER SAVE
			GETSEVC = Sql.GetFirst ("SELECT * from SAQSCO where QUOTE_RECORD_ID = '"
						+ str(Qt_rec_id)
						+ "' AND SERVICE_ID ='"
						+ str(TreeSuperParentParam)
						+ "' AND FABLOCATION_ID = '"
						+ str(TreeParentParam)
						+ "' AND GREENBOOK = '"
						+ str(TreeParam)
						+ "' AND QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID = '"
						+ str(CurrentRecordId)
						+ "'"
					)
			GETSVD = Sql.GetFirst("SELECT * FROM PRSVDR (NOLOCK) WHERE VALUEDRIVER_ID ='"+ str(getdescription).replace("_", " ")+ "' AND SERVICE_ID = '"+str(TreeSuperParentParam)+"'")
			SAQSCDENTRY = Sql.GetFirst(
				"Select QUOTE_SERVICE_COVERED_OBJ_TOOL_DRIVER_RECORD_ID FROM SAQSCD(NOLOCK) WHERE QUOTE_RECORD_ID='{}' AND VALUEDRIVER_RECORD_ID='{}' AND QTESRVCOB_RECORD_ID ='{}'".format(
					str(GETSEVC.QUOTE_RECORD_ID), str(GETSVD.VALUEDRIVER_RECORD_ID),str(GETSEVC.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID)
				)
			)
			# Trace.Write("bSelect QUOTE_FABLOCATION_VALUEDRIVER_RECORD_ID FROM SAQFVD(NOLOCK) WHERE QUOTE_RECORD_ID='{}' AND VALUEDRIVER_RECORD_ID='{}' ".format(str(GETFABLOC.QUOTE_RECORD_ID),str(GETFBVD.VALUE_DRIVER_RECORD_ID)))
			primarykey = str(Guid.NewGuid()).upper()
			if SAQSCDENTRY is None:
				tableInfo = SqlHelper.GetTable("SAQSCD")
				tablerow = {
					"QUOTE_SERVICE_COVERED_OBJ_TOOL_DRIVER_RECORD_ID": primarykey,
					"EQUIPMENT_DESCRIPTION": str(GETSEVC.EQUIPMENT_DESCRIPTION),
					"EQUIPMENT_ID": str(GETSEVC.EQUIPMENT_ID),
					"EQUIPMENT_RECORD_ID": str(GETSEVC.EQUIPMENT_RECORD_ID),
					"SERIAL_NUMBER": str(GETSEVC.SERIAL_NO),
					"SERVICE_DESCRIPTION": str(GETSEVC.SERVICE_DESCRIPTION),
					"FABLOCATION_ID" : str(GETSEVC.FABLOCATION_ID),
					"FABLOCATION_RECORD_ID": str(GETSEVC.FABLOCATION_RECORD_ID),
					"GREENBOOK": str(GETSEVC.GREENBOOK),
					"GREENBOOK_RECORD_ID": str(GETSEVC.GREENBOOK_RECORD_ID),
					"SERVICE_ID": str(GETSEVC.SERVICE_ID),
					"SERVICE_RECORD_ID": str(GETSEVC.SERVICE_RECORD_ID),
					"QUOTE_ID": str(GETSEVC.QUOTE_ID),
					"QUOTE_NAME": str(GETSEVC.QUOTE_NAME),
					"QUOTE_RECORD_ID": str(GETSEVC.QUOTE_RECORD_ID),
					"VALUEDRIVER_ID": str(GETSVD.VALUEDRIVER_ID),
					"VALUEDRIVER_NAME": str(GETSVD.VALUEDRIVER_NAME),
					"VALUEDRIVER_RECORD_ID": str(GETSVD.VALUEDRIVER_RECORD_ID),
					"QTESRVCOB_RECORD_ID": str(GETSEVC.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID),
					"CPQTABLEENTRYDATEADDED": datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"),
					"CPQTABLEENTRYADDEDBY": userName,
					"ADDUSR_RECORD_ID": userId,
				}
				#Trace.Write(str(tablerow))
				tableInfo.AddRow(tablerow)
				Sql.Upsert(tableInfo)
				#Trace.Write("COVVD ADDED" + str(tablerow))
			GETVALSDV = Sql.GetFirst(
				"SELECT * from PRSDVL where VALUEDRIVER_ID ='"
				+ str(getdescription)
				+ "' and VALUEDRIVER_VALUE_DESCRIPTION = '"
				+ str(getvaluedriv)
				+ "' and SERVICE_ID = '"
				+ str(TreeSuperParentParam)
				+ "'"
			)
			# Trace.Write(
			# 	"drivervalueSELECT * from PRSDVL where VALUEDRIVER_ID ='"
			# 	+ str(getdescription)
			# 	+ "' and VALUEDRIVER_VALUE_DESCRIPTION = '"
			# 	+ str(getvaluedriv)
			# 	+ "'"
			# )
			if GETVALSDV is not None:
				GETDRISVD = Sql.GetFirst(
					"SELECT * from SAQSCD(NOLOCK) where VALUEDRIVER_ID ='"
					+ str(getdescription)
					+ "' AND QUOTE_RECORD_ID = '"
					+ str(Qt_rec_id)
					+ "'AND SERVICE_ID = '"
					+ str(TreeSuperParentParam)
					+ "' AND GREENBOOK = '"
					+ str(TreeParam)
					+ "' AND FABLOCATION_ID = '"
					+ str(TreeParentParam)
					+ "'"
				)
				QTQSDVUPD = Sql.GetFirst(
					"Select QUOTE_SERVICE_COVERED_OBJ_TOOL_DRIVER_VALUE_RECORD_ID,CpqTableEntryId FROM SAQSCV(NOLOCK) WHERE TOOL_VALUEDRIVER_ID ='"
					+ str(getdescription)
					+ "' AND QUOTE_RECORD_ID = '"
					+ str(Qt_rec_id)
					+ "' AND SERVICE_ID = '"
					+ str(TreeSuperParentParam)
					+ "' AND GREENBOOK = '"
					+ str(TreeParam)
					+ "' AND FABLOCATION_ID = '"
					+ str(TreeParentParam)
					+ "'"
				)
				tablerow = {}
				tableInfos = SqlHelper.GetTable("SAQSCV")
				if QTQSDVUPD:
					tablerow = {"CpqTableEntryId": QTQSDVUPD.CpqTableEntryId}
				else:
					tablerow = {"QUOTE_SERVICE_COVERED_OBJ_TOOL_DRIVER_VALUE_RECORD_ID": str(Guid.NewGuid()).upper()}
				tablerow.update(
					{
						"QUOTE_ID": str(GETDRISVD.QUOTE_ID),
						"QUOTE_NAME": str(GETDRISVD.QUOTE_NAME),
						#"BUSINESSUNIT_ID": str(GETDRISVD.BUSINESSUNIT_ID),
						#"BUSINESSUNIT_RECORD_ID": str(GETDRISVD.BUSINESSUNIT_RECORD_ID),
						"GREENBOOK": str(GETDRISVD.GREENBOOK),
						"GREENBOOK_RECORD_ID": str(GETDRISVD.GREENBOOK_RECORD_ID),
						"VALUEDRIVER_COEFFICIENT": str(GETVALSDV.VALUEDRIVER_COEFFICIENT),
						"VALUEDRIVER_COEFFICIENT_RECORD_ID": str(GETVALSDV.SERVICE_VALUEDRIVER_VALUE_RECORD_ID),
						"EQUIPMENT_DESCRIPTION": str(GETDRISVD.EQUIPMENT_DESCRIPTION),
						"EQUIPMENT_ID": str(GETDRISVD.EQUIPMENT_ID),
						"EQUIPMENT_RECORD_ID": str(GETDRISVD.EQUIPMENT_RECORD_ID),
						"QUOTE_RECORD_ID": str(GETDRISVD.QUOTE_RECORD_ID),
						"QTESRVCOB_RECORD_ID": str(GETDRISVD.QTESRVCOB_RECORD_ID),
						"QTESRVCOB_VDR_RECORD_ID": str(GETDRISVD.QUOTE_SERVICE_COVERED_OBJ_TOOL_DRIVER_RECORD_ID),
						"TOOL_VALUEDRIVER_ID": str(GETDRISVD.VALUEDRIVER_ID),
						"TOOL_VALUEDRIVER_RECORD_ID": str(GETDRISVD.VALUEDRIVER_RECORD_ID),
						"TOOL_VALUEDRIVER_VALUE_DESCRIPTION": str(GETVALSDV.VALUEDRIVER_VALUE_DESCRIPTION),
						"TOOL_VALUEDRIVER_VALUE_RECORD_ID": str(GETVALSDV.VALUEDRIVER_VALUE_RECORD_ID),
						"TOOL_VALUEDRIVER_VALUE_CODE": str(GETVALSDV.VALUEDRIVER_VALUE_CODE),
						"SERIAL_NUMBER": str(GETDRISVD.SERIAL_NUMBER),
						"SERVICE_DESCRIPTION": str(GETDRISVD.SERVICE_DESCRIPTION),
						"SERVICE_ID": str(GETDRISVD.SERVICE_ID),
						"SERVICE_RECORD_ID": str(GETDRISVD.SERVICE_RECORD_ID),
						"FABLOCATION_ID" : str(GETDRISVD.FABLOCATION_ID),
						"FABLOCATION_RECORD_ID": str(GETDRISVD.FABLOCATION_RECORD_ID),
						"FABLOCATION_NAME":str(GETDRISVD.FABLOCATION_NAME),
						"CPQTABLEENTRYDATEADDED": datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"),
						"CPQTABLEENTRYADDEDBY": userName,
						"ADDUSR_RECORD_ID": userId,
					}
				)
				#Trace.Write(str(tablerow))
				tableInfos.AddRow(tablerow)
				Sql.Upsert(tableInfos)
		# COEFFICIENTS SUM at Level 3
		QueryStatement = "UPDATE A  SET TOOL_VALUEDRIVER_COEFFICIENT = VALUEDRIVER_COEFFICIENT FROM SAQICO A(NOLOCK) JOIN (SELECT QUOTE_RECORD_ID,EQUIPMENT_ID,SUM(VALUEDRIVER_COEFFICIENT) AS VALUEDRIVER_COEFFICIENT from SAQSCV(NOLOCK) WHERE QUOTE_RECORD_ID ='"+str(Qt_rec_id)+"' AND SERVICE_ID ='"+str(TreeSuperParentParam)+"' AND FABLOCATION_ID = '" + str(TreeParentParam) + "' AND GREENBOOK = '" + str(TreeParam) + "' AND EQUIPMENT_ID = '"+str(GETDRISVD.EQUIPMENT_ID)+"' GROUP BY QUOTE_RECORD_ID,EQUIPMENT_ID) B ON A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID"
		Sql.RunQuery(QueryStatement)
		# Trace.Write("CoeffUPDATE A  SET TOOL_VALUEDRIVER_COEFFICIENT = VALUEDRIVER_COEFFICIENT FROM SAQICO A(NOLOCK) JOIN (SELECT QUOTE_RECORD_ID,EQUIPMENT_ID,SUM(VALUEDRIVER_COEFFICIENT) AS VALUEDRIVER_COEFFICIENT from SAQSCV(NOLOCK) WHERE QUOTE_RECORD_ID ='"+str(Qt_rec_id)+"' AND SERVICE_ID ='"+str(TreeSuperParentParam)+"' AND FABLOCATION_ID = '" + str(TreeParentParam) + "' AND GREENBOOK = '" + str(TreeParam) + "' AND EQUIPMENT_ID = '"+str(GETDRISVD.EQUIPMENT_ID)+"' GROUP BY QUOTE_RECORD_ID,EQUIPMENT_ID) B ON A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID")
	return 'data'

def Offergreencost(ACTION,CurrentRecordId,subtab):
	TreeParam = Product.GetGlobal("TreeParam")
	TreeParentParam = Product.GetGlobal("TreeParentLevel0")
	TreeSuperParentParam = Product.GetGlobal("TreeParentLevel1")
	TreeTopSuperParentParam = Product.GetGlobal("TreeParentLevel2")	
	
	sec_str1 = sec_str = ""
	dbl_clk_function = ""
	desc_list = ["VALUE DRIVER DESCRIPTION","VALUE DRIVER VALUE","VALUE DRIVER COEFFICIENT",]
	table_id = 'csserviceGreencostvaldrives'
	attr_dict = {"VALUE DRIVER DESCRIPTION": "VALUE DRIVER DESCRIPTION",
					"VALUE DRIVER VALUE": "VALUE DRIVER VALUE",
					"VALUE DRIVER COEFFICIENT": "VALUE DRIVER COEFFICIENT",
				}
	date_field = []
	if TreeTopSuperParentParam == 'Quote Items':
		TreeSuperParentParam = str(TreeSuperParentParam.split('-')[1]).strip()
	#GetSAQSVD = Sql.GetList("SELECT DISTINCT VALUEDRIVER_ID,VALUEDRIVER_RECORD_ID FROM PRSVDR(NOLOCK) WHERE VALUEDRIVER_TYPE = 'TOOL BASED' AND SERVICE_ID = '"+str(TreeParam)+"'")
	GetSAQSVD = Sql.GetList("SELECT DISTINCT VALUEDRIVER_ID,VALUEDRIVER_RECORD_ID FROM PRSVDR(NOLOCK) WHERE VALUEDRIVER_TYPE = 'TOOL BASED' AND SERVICE_ID = '"+str(TreeSuperParentParam)+"'")
	sec_str += ('<table id="' + str(table_id)+ '" data-escape="true" data-html="true"    data-show-header="true" > <thead><tr>')
	for key, invs in enumerate(list(desc_list)):
		invs = str(invs).strip()
		qstring = attr_dict.get(str(invs)) or ""
		sec_str += (
			'<th data-field="'
			+ invs
			+ '" data-title-tooltip="'
			+ str(qstring)
			+ '" data-sortable="true" >'
			+ str(qstring)
			+ "</th>"
		)
	sec_str += '</tr></thead><tbody class ="app_id" ></tbody></table>'
	for qstn in GetSAQSVD:
		sec_str1 = sec_str_eff = ""
		VAR1 = coeffval = ""
		userselectedeffi = []
		mastername = str(qstn.VALUEDRIVER_RECORD_ID)
		field_name = str(qstn.VALUEDRIVER_ID).replace("'", "''")
		
		#sec_str += ('')
		new_value_dict = {}
		
		
		GetDRIVNAME = Sql.GetList(
			"SELECT TOP 1000 VALUEDRIVER_VALUE_DESCRIPTION FROM PRSDVL(NOLOCK) WHERE  VALUEDRIVER_ID = '"
			+ str(field_name)
			+ "' AND VALUEDRIVER_RECORD_ID = '" 
			+ str(mastername)
			+ "'AND SERVICE_ID = '" 
			+ str(TreeSuperParentParam)
			+ "'"
		)
		selecter = Sql.GetFirst(
			"SELECT TOOL_VALUEDRIVER_VALUE_DESCRIPTION,VALUEDRIVER_COEFFICIENT FROM SAQSGV(NOLOCK) WHERE QUOTE_RECORD_ID = '"
			+ str(Qt_rec_id)
			+ "' AND TOOL_VALUEDRIVER_ID = '"
			+ str(field_name)
			+ "' AND SERVICE_ID = '"
			+ str(TreeSuperParentParam)
			+ "' AND GREENBOOK = '"
			+str(TreeParam)
			+"' AND FABLOCATION_ID ='"
			+ str(TreeParentParam)
			+ "'"
		)
		
		userselecteddrive = []
		
		if selecter:
			userselecteddrive.append(selecter.TOOL_VALUEDRIVER_VALUE_DESCRIPTION)
			userselectedeffi.append(str(float(selecter.VALUEDRIVER_COEFFICIENT)*float(100))+" %")

		
		for qstns in GetDRIVNAME:
			if qstns.VALUEDRIVER_VALUE_DESCRIPTION in userselecteddrive:
				VAR1 += (
					'<option  value = "'
					+ str(qstns.VALUEDRIVER_VALUE_DESCRIPTION)
					+ '" selected>'
					+ str(qstns.VALUEDRIVER_VALUE_DESCRIPTION)
					+ "</option>"
				)
			else:
				VAR1 += (
					'<option  value = "'
					+ str(qstns.VALUEDRIVER_VALUE_DESCRIPTION)
					+ '">'
					+ str(qstns.VALUEDRIVER_VALUE_DESCRIPTION)
					+ "</option>"
				)
			
		sec_str1 += (
			'<select class="form-control" id = "'
			+ str(field_name).replace(" ", "_")
			+ '" disabled><option value="Select">..Select</option>'
			+ str(VAR1)
			+ "</select>"
		)
		for data in qstn:
			new_value_dict["VALUE DRIVER DESCRIPTION"] = str(qstn.VALUEDRIVER_ID)
			new_value_dict["VALUE DRIVER COEFFICIENT"]  = userselectedeffi
			new_value_dict["VALUE DRIVER VALUE"] = sec_str1
			
			
		date_field.append(new_value_dict)
	
	dbl_clk_function += (
		"try {var fablocatedict = [];$('#csserviceGreencostvaldrives').on('click-row.bs.table', function (e, row, $element) {console.log('tset---');$('#csserviceGreencostvaldrives').find(':input(:disabled)').prop('disabled', false);$('#csserviceGreencostvaldrives tbody  tr td select option').css('background-color','lightYellow');$('#csserviceGreencostvaldrives  tbody tr td select').addClass('light_yellow');$('#fabcostlocate_save').css('display','block');$('#fabcostlocate_cancel').css('display','block');$('select').on('change', function() { console.log( this.value );var valuedrivchage = this.value;var valuedesc = $(this).closest('tr').find('td:nth-child(1)').text();console.log('valuedesc-----',valuedesc);var concate_data = valuedesc+'='+valuedrivchage;if(!fablocatedict.includes(concate_data)){fablocatedict.push(concate_data)};console.log('fablocatedict---',fablocatedict);getfablocatedict = JSON.stringify(fablocatedict);localStorage.setItem('getfablocatedict', getfablocatedict);});});}catch {console.log('error---')}"
	)
	
	#Trace.Write('date_field---'+str(date_field))
	if len(date_field) == 0 and len(GetSAQSVD) == 0:
		if (TreeSuperTopParentParam == "Complementary Products" and subtab == "Greenbook Cost and Value Drivers" and TreeSuperParentParam.startswith("Sending")):
			sec_str += '<div class="noRecDisp">Greenbook Cost and Value Drivers are not applicable at this level</div>'
		else:
			sec_str += '<div class="noRecDisp">Greenbook Cost and Value Drivers are not applicable for this Product Offering</div>'
	if len(date_field) == 0 and len(GetSAQSVD) != 0:
		sec_str += '<div class="noRecDisp">No Records to Display</div>'
	return sec_str,table_id,date_field,dbl_clk_function

def Offerequipcost(ACTION,CurrentRecordId,subtab):
	TreeParam = Product.GetGlobal("TreeParam")
	TreeParentParam = Product.GetGlobal("TreeParentLevel0")
	TreeSuperParentParam = Product.GetGlobal("TreeParentLevel1")
	TreeTopSuperParentParam = Product.GetGlobal("TreeParentLevel2")
	
	#In this level im getting Currentrecord as equipment id
	
	sec_str1 = sec_str = ""
	dbl_clk_function = ""
	desc_list = ["VALUE DRIVER DESCRIPTION","VALUE DRIVER VALUE","VALUE DRIVER COEFFICIENT",]
	table_id = 'csserviceEquipcostvaldrives'
	attr_dict = {"VALUE DRIVER DESCRIPTION": "VALUE DRIVER DESCRIPTION",
					"VALUE DRIVER VALUE": "VALUE DRIVER VALUE",
					"VALUE DRIVER COEFFICIENT": "VALUE DRIVER COEFFICIENT",
				}
	date_field = []
	
	#GetSAQSVD = Sql.GetList("SELECT DISTINCT VALUEDRIVER_ID,VALUEDRIVER_RECORD_ID FROM PRSVDR(NOLOCK) WHERE VALUEDRIVER_TYPE = 'TOOL BASED' AND SERVICE_ID = '"+str(TreeParam)+"'")
	if TreeTopSuperParentParam == "Quote Items":
		TP = str(TreeSuperParentParam)
		TP1 = TP.split('-')
		TreeSuperParentParam = TP1[1].strip()
	GetSAQSVD = Sql.GetList("SELECT DISTINCT VALUEDRIVER_ID,VALUEDRIVER_RECORD_ID FROM PRSVDR(NOLOCK) WHERE VALUEDRIVER_TYPE = 'TOOL BASED' AND SERVICE_ID = '"+str(TreeSuperParentParam)+"'")
	sec_str += ('<table id="' + str(table_id)+ '" data-escape="true" data-html="true"    data-show-header="true" > <thead><tr>')
	for key, invs in enumerate(list(desc_list)):
		invs = str(invs).strip()
		qstring = attr_dict.get(str(invs)) or ""
		sec_str += (
			'<th data-field="'
			+ invs
			+ '" data-title-tooltip="'
			+ str(qstring)
			+ '" data-sortable="true" data-filter-control="input">'
			+ str(qstring)
			+ "</th>"
		)
	sec_str += '</tr></thead><tbody class ="app_id" ></tbody></table>'
	for qstn in GetSAQSVD:
		sec_str1 = sec_str_eff = ""
		VAR1 = coeffval = ""
		userselectedeffi = []
		mastername = str(qstn.VALUEDRIVER_RECORD_ID)
		field_name = str(qstn.VALUEDRIVER_ID).replace("'", "''")
		
		#sec_str += ('')
		new_value_dict = {}
		
		
		GetDRIVNAME = Sql.GetList(
			"SELECT TOP 1000 VALUEDRIVER_VALUE_DESCRIPTION FROM PRSDVL(NOLOCK) WHERE  VALUEDRIVER_ID = '"
			+ str(field_name)
			+ "' AND VALUEDRIVER_RECORD_ID = '" 
			+ str(mastername)
			+ "'AND SERVICE_ID = '" 
			+ str(TreeSuperParentParam)
			+ "'"
		)
		selecter = Sql.GetFirst(
			"SELECT TOOL_VALUEDRIVER_VALUE_DESCRIPTION,VALUEDRIVER_COEFFICIENT FROM SAQSCV(NOLOCK) WHERE QUOTE_RECORD_ID = '"
			+ str(Qt_rec_id)
			+ "' AND TOOL_VALUEDRIVER_ID = '"
			+ str(field_name)
			+ "' AND SERVICE_ID = '"
			+ str(TreeSuperParentParam)
			+ "' AND FABLOCATION_ID = '"
			+ str(TreeParentParam)
			+ "' AND GREENBOOK = '"
			+ str(TreeParam)
			+ "' AND EQUIPMENT_ID = '"
			+ str(CurrentRecordId)
			+ "'"
		)
		
		userselecteddrive = []
		if selecter:
			userselecteddrive.append(selecter.TOOL_VALUEDRIVER_VALUE_DESCRIPTION)
			userselectedeffi.append(str(float(selecter.VALUEDRIVER_COEFFICIENT)*float(100))+" %")

		
		for qstns in GetDRIVNAME:
			if qstns.VALUEDRIVER_VALUE_DESCRIPTION in userselecteddrive:
				VAR1 += (
					'<option  value = "'
					+ str(qstns.VALUEDRIVER_VALUE_DESCRIPTION)
					+ '" selected>'
					+ str(qstns.VALUEDRIVER_VALUE_DESCRIPTION)
					+ "</option>"
				)
			else:
				VAR1 += (
					'<option  value = "'
					+ str(qstns.VALUEDRIVER_VALUE_DESCRIPTION)
					+ '">'
					+ str(qstns.VALUEDRIVER_VALUE_DESCRIPTION)
					+ "</option>"
				)
			
		sec_str1 += (
			'<select class="form-control" id = "'
			+ str(field_name).replace(" ", "_")
			+ '" disabled><option value="Select">..Select</option>'
			+ str(VAR1)
			+ "</select>"
		)
		for data in qstn:
			new_value_dict["VALUE DRIVER DESCRIPTION"] = str(qstn.VALUEDRIVER_ID)
			new_value_dict["VALUE DRIVER COEFFICIENT"]  = userselectedeffi
			new_value_dict["VALUE DRIVER VALUE"] = sec_str1
			
			
		date_field.append(new_value_dict)
	if TreeTopSuperParentParam.strip() == "Comprehensive Services":		
		dbl_clk_function += (
			"try {var fablocatedict = [];$('#csserviceEquipcostvaldrives').on('click-row.bs.table', function (e, row, $element) {console.log('tset---');$('#csserviceEquipcostvaldrives').find(':input(:disabled)').prop('disabled', false);$('#csserviceEquipcostvaldrives tbody  tr td select option').css('background-color','lightYellow');$('#csserviceEquipcostvaldrives  tbody tr td select').addClass('light_yellow');$('#fabcostlocate_save').css('display','block');$('#fabcostlocate_cancel').css('display','block');$('select').on('change', function() { console.log( this.value );var valuedrivchage = this.value;var valuedesc = $(this).closest('tr').find('td:nth-child(1)').text();console.log('valuedesc-----',valuedesc);var concate_data = valuedesc+'='+valuedrivchage;if(!fablocatedict.includes(concate_data)){fablocatedict.push(concate_data)};console.log('fablocatedict---',fablocatedict);getfablocatedict = JSON.stringify(fablocatedict);localStorage.setItem('getfablocatedict', getfablocatedict);});});}catch {console.log('error---')}"
		)
	
	#Trace.Write('date_field---'+str(date_field))
	if len(date_field) == 0 and len(GetSAQSVD) == 0:
		if (TreeSuperTopParentParam == "Complementary Products" and subtab == "Equipment Cost and Value Drivers" and TreeSuperParentParam.startswith("Sending")):
			sec_str += '<div class="noRecDisp">Equipment Cost and Value Drivers are not applicable at this level</div>'
		else:	
			sec_str += '<div class="noRecDisp">Equipment Cost and Value Drivers are not applicable for this Product Offering</div>'
	if len(date_field) == 0 and len(GetSAQSVD) != 0:
		sec_str += '<div class="noRecDisp">No Records to Display</div>'
	return sec_str,table_id,date_field,dbl_clk_function

ACTION = Param.ACTION
TreeParam = Product.GetGlobal("TreeParam")
TreeParentParam = Product.GetGlobal("TreeParentLevel0")
TreeSuperParentParam = Product.GetGlobal("TreeParentLevel1")
TreeTopSuperParentParam = Product.GetGlobal("TreeParentLevel2")
TreeSuperTopParentParam = Product.GetGlobal("TreeParentLevel3")
userId = str(User.Id)
userName = str(User.UserName)
if hasattr(Param, "CurrentRecordId"):
	CurrentRecordId = Param.CurrentRecordId
else:
	CurrentRecordId =""
Trace.Write('CurrentRecordId--------------------'+str(CurrentRecordId))
if hasattr(Param, "SerLocateDT"):
	SerLocateDT = Param.SerLocateDT
else:
	SerLocateDT =""
Trace.Write('SerLocateDT--------------------'+str(SerLocateDT))
try:
	FabLocateDT = Param.FabLocateDT
	#SerLocateDT = Param.SerLocateDT
	getfabid = Param.getfabid
except:
	FabLocateDT = getfabid = ""
	#SerLocateDT = getfabid = ""
	#subtab = ""
try:
	subtab= Param.subtab
except:
	subtab = ""
if ACTION == "SAVE":
	ApiResponse = ApiResponseFactory.JsonResponse(fabsave(ACTION,CurrentRecordId,FabLocateDT,getfabid,subtab))
elif ACTION == "SAVECOST":
	ApiResponse = ApiResponseFactory.JsonResponse(costsave(ACTION,CurrentRecordId,SerLocateDT,getfabid,subtab))
elif ACTION == "NESTED_FAB_VIEW":
	ApiResponse = ApiResponseFactory.JsonResponse(nestedfabview(ACTION,CurrentRecordId,subtab))
elif ACTION == "SERVICE_FAB_VIEWS":
	ApiResponse = ApiResponseFactory.JsonResponse(servicefabview(ACTION,CurrentRecordId,))
elif ACTION == "ITEM_GB_FAB_VIEWS":
	ApiResponse = ApiResponseFactory.JsonResponse(itemgreenbookfabview(ACTION,CurrentRecordId,))
elif ACTION == "COST_FAB_VIEWS":
	ApiResponse = ApiResponseFactory.JsonResponse(costfabview(ACTION,CurrentRecordId,))
elif ACTION == "CS_FAB_VIEWS":
	ApiResponse = ApiResponseFactory.JsonResponse(Comp_fabview(ACTION,CurrentRecordId,))
elif ACTION == "CS_CT_FAB_VIEWS":
	ApiResponse = ApiResponseFactory.JsonResponse(Comp_cost_fabview(ACTION,CurrentRecordId,subtab))
elif ACTION == "CS_FABGREEN_VIEWS":
	ApiResponse = ApiResponseFactory.JsonResponse(Offergreenfab(ACTION,CurrentRecordId,))
elif ACTION == "CS_COSTGREEN_VIEWS":
	ApiResponse = ApiResponseFactory.JsonResponse(Offergreencost(ACTION,CurrentRecordId,subtab))	
elif ACTION == "CS_FABEQUIP_VIEWS":
	ApiResponse = ApiResponseFactory.JsonResponse(Offerequipfab(ACTION,CurrentRecordId,))
elif ACTION == "CS_COSTEQUIP_VIEWS":
	ApiResponse = ApiResponseFactory.JsonResponse(Offerequipcost(ACTION,CurrentRecordId,subtab))			
else:
	ApiResponse = ApiResponseFactory.JsonResponse(fabview(ACTION,CurrentRecordId,subtab))
# =========================================================================================================================================
#   __script_name : CQVLDPRDEF.PY
#   __script_description : THIS SCRIPT IS USED FOR PREDEFINED VALUES IN VALUE DRIVER (GETS TRIGGERED AFTER IFLOW SCRIPT - CQTVLDRIFW.py)
#   __primary_author__ : 
#   __create_date :06-09-2021
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct
import clr
import System.Net
import sys
import re
import datetime
from System.Net import CookieContainer, NetworkCredential, Mail
from System.Net.Mail import SmtpClient, MailAddress, Attachment, MailMessage
from SYDATABASE import SQL
Sql = SQL()

try:
	quote_record_id = Param.quote_rec_id
except:
	quote_record_id = ""
try:
	LEVEL = Param.level
except:
	LEVEL = ""
try:
	TreeParam = Param.treeparam
	userId = Param.user_id
	quote_revision_record_id = Param.quote_rev_id
	where_condition =  Param.where_condition
except: 
	TreeParam = ""
	userId = ""
	quote_revision_record_id = ""
	where_condition = ""

Log.Info('predefined script started')	

def equipment_predefined():
	get_valuedriver_ids = Sql.GetList("SELECT PRENTL.ENTITLEMENT_ID,PRENTL.ENTITLEMENT_DESCRIPTION from PRENTL (NOLOCK) INNER JOIN PRENLI (NOLOCK) ON PRENTL.ENTITLEMENT_ID = PRENLI.ENTITLEMENT_ID WHERE SERVICE_ID = '{}' AND VISIBLE_IN_CONFIG = 1 AND ENTITLEMENT_TYPE ='VALUE DRIVER' AND PRENLI.ENTITLEMENTLEVEL_NAME = 'OFFERING FAB GREENBOOK TOOL LEVEL' AND PRENTL.ENTITLEMENT_ID NOT IN (SELECT ENTITLEMENT_ID from PRENLI (NOLOCK) WHERE ENTITLEMENTLEVEL_NAME IN ('OFFERING FAB LEVEL','OFFERING LEVEL','OFFERING FAB GREENBOOK LEVEL')) ".format(TreeParam) )
	getall_recid = Sql.GetList(""" SELECT EQUIPMENT_RECORD_ID,ENTITLEMENT_XML,GREENBOOK_RECORD_ID,FABLOCATION_RECORD_ID FROM SAQSCE {}""".format(str(where_condition) ))
	for rec in getall_recid:
		entxmldict = {}
		pattern_tag = re.compile(r'(<QUOTE_ITEM_ENTITLEMENT>[\w\W]*?</QUOTE_ITEM_ENTITLEMENT>)')
		pattern_name = re.compile(r'<ENTITLEMENT_ID>([^>]*?)</ENTITLEMENT_ID>')
		updateentXML = rec.ENTITLEMENT_XML
		for m in re.finditer(pattern_tag, updateentXML):
			sub_string = m.group(1)
			x=re.findall(pattern_name,sub_string)
			entxmldict[x[0]]=sub_string
		for val in get_valuedriver_ids:
			if 'WAFER NODE' in val.ENTITLEMENT_DESCRIPTION.upper():
				get_val = Sql.GetFirst(""" SELECT M.VALDRV_WAFERNODE as VALDRV_WAFERNODE FROM MAEQUP M JOIN PRENVL P ON M.VALDRV_DEVICETYPE=P.ENTITLEMENT_DISPLAY_VALUE WHERE M.EQUIPMENT_RECORD_ID='{}' """.format(str(rec.EQUIPMENT_RECORD_ID)))
				if get_val.VALDRV_WAFERNODE:
					updateentXML = updating_xml(entxmldict,updateentXML,val.ENTITLEMENT_ID,get_val.VALDRV_WAFERNODE)
			elif 'DEVICE TYPE' in val.ENTITLEMENT_DESCRIPTION.upper():
				get_val = Sql.GetFirst(""" SELECT M.VALDRV_DEVICETYPE as VALDRV_DEVICETYPE FROM MAEQUP M JOIN PRENVL P ON M.VALDRV_DEVICETYPE=P.ENTITLEMENT_DISPLAY_VALUE WHERE M.EQUIPMENT_RECORD_ID='{}' """.format(str(rec.EQUIPMENT_RECORD_ID)))
				if get_val.VALDRV_DEVICETYPE:
					updateentXML = updating_xml(entxmldict,updateentXML,val.ENTITLEMENT_ID,get_val.VALDRV_DEVICETYPE)


		for roll_obj in ['SAQSCE','SAQSAE']:
			Sql.RunQuery( "UPDATE {} SET ENTITLEMENT_XML = '{}' {} AND FABLOCATION_RECORD_ID = '{}' AND GREENBOOK_RECORD_ID ='{}' AND EQUIPMENT_RECORD_ID ='{}' ".format(roll_obj, updateentXML.replace("'","''") ,where_condition,rec.FABLOCATION_RECORD_ID, rec.GREENBOOK_RECORD_ID, rec.EQUIPMENT_RECORD_ID) )

def greenbook_predefined():
	getxml_query = Sql.GetList(""" SELECT GREENBOOK,ENTITLEMENT_XML,GREENBOOK_RECORD_ID,FABLOCATION_RECORD_ID FROM SAQSGE {}""".format(str(where_condition) ))
	
	get_valuedriver_ids = Sql.GetList("SELECT PRENTL.ENTITLEMENT_ID,PRENTL.ENTITLEMENT_DESCRIPTION from PRENTL (NOLOCK) INNER JOIN PRENLI (NOLOCK) ON PRENTL.ENTITLEMENT_ID = PRENLI.ENTITLEMENT_ID WHERE SERVICE_ID = '{}' AND VISIBLE_IN_CONFIG = 1 AND ENTITLEMENT_TYPE ='VALUE DRIVER' AND PRENLI.ENTITLEMENTLEVEL_NAME = 'OFFERING FAB GREENBOOK LEVEL' AND PRENTL.ENTITLEMENT_ID NOT IN (SELECT ENTITLEMENT_ID from PRENLI (NOLOCK) WHERE ENTITLEMENTLEVEL_NAME IN ('OFFERING FAB LEVEL','OFFERING LEVEL')) ".format(TreeParam) )
	for rec in getxml_query:
		entxmldict = {}
		pattern_tag = re.compile(r'(<QUOTE_ITEM_ENTITLEMENT>[\w\W]*?</QUOTE_ITEM_ENTITLEMENT>)')
		pattern_name = re.compile(r'<ENTITLEMENT_ID>([^>]*?)</ENTITLEMENT_ID>')
		updateentXML = rec.ENTITLEMENT_XML
		for m in re.finditer(pattern_tag, updateentXML):
			sub_string = m.group(1)
			x=re.findall(pattern_name,sub_string)
			entxmldict[x[0]]=sub_string
		for val in get_valuedriver_ids:
			if 'GREENBOOK' in val.ENTITLEMENT_DESCRIPTION.upper():
				ent_value = rec.GREENBOOK
				updateentXML = updating_xml(entxmldict,updateentXML,val.ENTITLEMENT_ID,ent_value)
		
		#Sql.RunQuery( "UPDATE SAQSGE SET ENTITLEMENT_XML = '{}' {} AND FABLOCATION_RECORD_ID = '{}' AND GREENBOOK_RECORD_ID ='{}'".format(updateentXML.replace("'","''") ,where_condition,rec.FABLOCATION_RECORD_ID, rec.GREENBOOK_RECORD_ID   ) )

		##rolldown
		for roll_obj in ['SAQSGE','SAQSCE','SAQSAE']:
			Sql.RunQuery( "UPDATE {} SET ENTITLEMENT_XML = '{}' {} AND FABLOCATION_RECORD_ID = '{}' AND GREENBOOK_RECORD_ID ='{}'".format(roll_obj, updateentXML.replace("'","''") ,where_condition,rec.FABLOCATION_RECORD_ID, rec.GREENBOOK_RECORD_ID   ) )
			


def fab_predefined():
	getxml_query = Sql.GetList(""" SELECT ENTITLEMENT_XML,FABLOCATION_RECORD_ID FROM SAQSGE {}""".format(str(where_condition) ))
	
	get_valuedriver_ids = Sql.GetList("SELECT PRENTL.ENTITLEMENT_ID,PRENTL.ENTITLEMENT_DESCRIPTION from PRENTL (NOLOCK) INNER JOIN PRENLI (NOLOCK) ON PRENTL.ENTITLEMENT_ID = PRENLI.ENTITLEMENT_ID WHERE SERVICE_ID = '{}' AND VISIBLE_IN_CONFIG = 1 AND ENTITLEMENT_TYPE ='VALUE DRIVER' AND PRENLI.ENTITLEMENTLEVEL_NAME = 'OFFERING FAB LEVEL' AND PRENTL.ENTITLEMENT_ID NOT IN (SELECT ENTITLEMENT_ID from PRENLI (NOLOCK) WHERE ENTITLEMENTLEVEL_NAME IN ('OFFERING LEVEL')) ".format(TreeParam) )
	for rec in getxml_query:
		entxmldict = {}
		pattern_tag = re.compile(r'(<QUOTE_ITEM_ENTITLEMENT>[\w\W]*?</QUOTE_ITEM_ENTITLEMENT>)')
		pattern_name = re.compile(r'<ENTITLEMENT_ID>([^>]*?)</ENTITLEMENT_ID>')
		updateentXML = rec.ENTITLEMENT_XML
		for m in re.finditer(pattern_tag, updateentXML):
			sub_string = m.group(1)
			x=re.findall(pattern_name,sub_string)
			entxmldict[x[0]]=sub_string
		for val in get_valuedriver_ids:
			if 'CSA TOOLS PER FAB' in val.ENTITLEMENT_DESCRIPTION.upper():
				account_id_query = Sql.GetFirst("SELECT ACCOUNT_ID FROM SAQTMT (NOLOCK) WHERE MASTER_TABLE_QUOTE_RECORD_ID = '"+str(Qt_rec_id)+"'")
				account_bluebook_query = Sql.GetFirst("SELECT BLUEBOOK FROM SAACNT (NOLOCK) WHERE ACCOUNT_ID = '"+str(account_id_query.ACCOUNT_ID)+"'")
				tools_count_query = SqlHelper.GetList("SELECT COUNT(GREENBOOK) AS COUNT FROM SAQSCO (NOLOCK) WHERE QUOTE_RECORD_ID = '"+str(Qt_rec_id)+"' GROUP BY FABLOCATION_NAME")
				#ent_value = rec.GREENBOOK
				updateentXML = updating_xml(entxmldict,updateentXML,val.ENTITLEMENT_ID,ent_value)
		
		Sql.RunQuery( "UPDATE SAQSGE SET ENTITLEMENT_XML = '{}' {} AND FABLOCATION_RECORD_ID = '{}' AND GREENBOOK_RECORD_ID ='{}'".format(updateentXML.replace("'","''") ,where_condition,rec.FABLOCATION_RECORD_ID, rec.GREENBOOK_RECORD_ID   ) )

		##rolldown
		for roll_obj in ['SAQSCE','SAQSAE']:
			Sql.RunQuery( "UPDATE {} SET ENTITLEMENT_XML = '{}' {} AND FABLOCATION_RECORD_ID = '{}' AND GREENBOOK_RECORD_ID ='{}'".format(roll_obj, updateentXML.replace("'","''") ,where_condition,rec.FABLOCATION_RECORD_ID, rec.GREENBOOK_RECORD_ID   ) )
			

##service level
def service_level_predefined(): 
	getxml_query = Sql.GetFirst(""" SELECT ENTITLEMENT_XML FROM SAQTSE {} """.format(str(where_condition)))
	entxmldict = {}
	pattern_tag = re.compile(r'(<QUOTE_ITEM_ENTITLEMENT>[\w\W]*?</QUOTE_ITEM_ENTITLEMENT>)')
	pattern_name = re.compile(r'<ENTITLEMENT_ID>([^>]*?)</ENTITLEMENT_ID>')
	updateentXML = getxml_query.ENTITLEMENT_XML
	for m in re.finditer(pattern_tag, updateentXML):
		sub_string = m.group(1)
		x=re.findall(pattern_name,sub_string)
		entxmldict[x[0]]=sub_string

	get_valuedriver_ids = Sql.GetList("SELECT PRENTL.ENTITLEMENT_ID,PRENTL.ENTITLEMENT_DESCRIPTION from PRENTL (NOLOCK) INNER JOIN PRENLI (NOLOCK) ON PRENTL.ENTITLEMENT_ID = PRENLI.ENTITLEMENT_ID WHERE SERVICE_ID = 'Z0091' AND VISIBLE_IN_CONFIG = 1 AND ENTITLEMENT_TYPE = 'VALUE DRIVER' AND PRENLI.ENTITLEMENTLEVEL_NAME = 'OFFERING LEVEL' ")

	for val in get_valuedriver_ids:
		if 'PRODUCT OFFERING' in val.ENTITLEMENT_DESCRIPTION.upper() or 'INTERCEPT' in val.ENTITLEMENT_DESCRIPTION.upper():
			ent_value = ""
			updateentXML = updating_xml(entxmldict,updateentXML,val.ENTITLEMENT_ID,ent_value )
	#Product.SetGlobal("updateentXML",updateentXML)
	Sql.RunQuery( "UPDATE SAQTSE SET ENTITLEMENT_XML = '{}' WHERE QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}' AND QTEREV_RECORD_ID='{}'".format(updateentXML.replace("'","''") , quote_record_id,TreeParam, quote_revision_record_id) )

	##rolldown
	# for roll_obj in ['SAQSFE','SAQSGE','SAQSCE','SAQSAE']:
	# 	Sql.RunQuery( "UPDATE {} SET ENTITLEMENT_XML = '{}' {} ".format(roll_obj, updateentXML.replace("'","''") ,where_condition   ) )
		
	
	
def updating_xml(entxmldict, input_xml, ent_id, ent_value):
	where =""
	if ent_value:
		get_value_code = Sql.GetFirst("SELECT ENTITLEMENT_VALUE_CODE FROM PRENVL WHERE ENTITLEMENT_ID ='{}' AND SERVICE_ID = '{}' AND ENTITLEMENT_DISPLAY_VALUE = '{}'".format(ent_id, TreeParam, ent_value) )
		entitlement_string = entxmldict[ent_id]
		entitlement_string = re.sub('<ENTITLEMENT_DISPLAY_VALUE>[^>]*?</ENTITLEMENT_DISPLAY_VALUE>','<ENTITLEMENT_DISPLAY_VALUE>'+str(ent_value)+'</ENTITLEMENT_DISPLAY_VALUE>',entitlement_string)

		entitlement_string = re.sub('<ENTITLEMENT_VALUE_CODE>[^>]*?</ENTITLEMENT_VALUE_CODE>','<ENTITLEMENT_VALUE_CODE>'+str(get_value_code.ENTITLEMENT_VALUE_CODE)+'</ENTITLEMENT_VALUE_CODE>',entitlement_string)
		where = " AND PRENVL.ENTITLEMENT_DISPLAY_VALUE = '{}'".format(ent_value)
		updateentXML = re.sub(r'<ENTITLEMENT_ID>'+str(ent_id)+'<[\w\W]*?</CALCULATION_FACTOR>', entitlement_string, input_xml )
		Log.Info("EID11->{}, {} ".format(str(ent_id),str(entitlement_string)) )

	get_coefficient_val = Sql.GetFirst("SELECT ENTITLEMENT_COEFFICIENT, PRENTL.ENTITLEMENT_ID FROM PRENVL (NOLOCK) INNER JOIN PRENTL (NOLOCK) ON PAR_ENPAR_ENTITLEMETITLEMENT_ID = PRENVL.ENTITLEMENT_ID AND PRENVL.SERVICE_ID = PRENTL.SERVICE_ID WHERE PRENVL.ENTITLEMENT_ID = '{}' AND PRENVL.SERVICE_ID = '{}' {}".format(ent_id, TreeParam, where))
	if get_coefficient_val.ENTITLEMENT_ID in entxmldict.keys():
		entitlement_string = entxmldict[get_coefficient_val.ENTITLEMENT_ID]
		entitlement_string = re.sub('<ENTITLEMENT_DISPLAY_VALUE>[^>]*?</ENTITLEMENT_DISPLAY_VALUE>','<ENTITLEMENT_DISPLAY_VALUE>'+str(get_coefficient_val.ENTITLEMENT_COEFFICIENT)+'</ENTITLEMENT_DISPLAY_VALUE>',entitlement_string)

		entitlement_string = re.sub('<ENTITLEMENT_VALUE_CODE>[^>]*?</ENTITLEMENT_VALUE_CODE>','<ENTITLEMENT_VALUE_CODE>'+str(get_coefficient_val.ENTITLEMENT_COEFFICIENT)+'</ENTITLEMENT_VALUE_CODE>',entitlement_string)
		updateentXML = re.sub(r'<ENTITLEMENT_ID>'+str(get_coefficient_val.ENTITLEMENT_ID)+'<[\w\W]*?</CALCULATION_FACTOR>', entitlement_string, updateentXML )
		Log.Info("EID->{}, {} ".format(str(ent_id),str(entitlement_string)) )
	return updateentXML

def tool_uptimetimprovementdriver_update():
	Trace.Write("11"+str(TreeParam))
	Trace.Write("22"+str(where_condition))
	getxml_query = Sql.GetFirst(""" SELECT ENTITLEMENT_XML FROM SAQSCE '{where_condition}' """.format(where_condition =where_condition))
	entxmldict = {}
	querystring =''
	uptime=''
	pattern_tag = re.compile(r'(<QUOTE_ITEM_ENTITLEMENT>[\w\W]*?</QUOTE_ITEM_ENTITLEMENT>)')
	pattern_name = re.compile(r'<ENTITLEMENT_ID>([^>]*?)</ENTITLEMENT_ID>')
	updateentXML = getxml_query.ENTITLEMENT_XML
	for m in re.finditer(pattern_tag, updateentXML):
		sub_string = m.group(1)
		x=re.findall(pattern_name,sub_string)
		entxmldict[x[0]]=sub_string
	if 'AGS_Z0091_KPI_SDUTBP' and 'AGS_Z0091_KPI_SDUTTP' in entxmldict.keys():
		base= entxmldict['AGS_Z0091_KPI_SDUTBP']
		base_price=re.search(r'<ENTITLEMENT_DISPLAY_VALUE>([^>]*?)</ENTITLEMENT_DISPLAY_VALUE>',base)
		base_price_value =str(base_price.group(1))
		#Trace.Write("aaaaaa"+str(base_price.group(1)))
		target= entxmldict['AGS_Z0091_KPI_SDUTTP']
		target_price=re.search(r'<ENTITLEMENT_DISPLAY_VALUE>([^>]*?)</ENTITLEMENT_DISPLAY_VALUE>',target)
		target_price_value=str(target_price.group(1))
		#Trace.Write("bbbb"+str(target_price.group(1)))
		uptime=float(target_price_value)-float(base_price_value)
		Trace.Write("a"+str(uptime))
		if uptime >= 10:
			uptime = 10
		update=Sql.GetFirst("Select ENTITLEMENT_DISPLAY_VALUE,ENTITLEMENT_COEFFICIENT FROM PRENVL WHERE ENTITLEMENT_DISPLAY_VALUE LIKE '%{uptime}%' ".format(uptime=uptime))
		for key in entxmldict.keys():
			if 'AGS_Z0091_VAL_UPIMPV' == key:
				entxmldict['AGS_Z0091_VAL_UPIMPV'] = re.sub('<ENTITLEMENT_DISPLAY_VALUE>[^>]*?</ENTITLEMENT_DISPLAY_VALUE>','<ENTITLEMENT_DISPLAY_VALUE>'+str(update.ENTITLEMENT_DISPLAY_VALUE)+'</ENTITLEMENT_DISPLAY_VALUE>',entxmldict['AGS_Z0091_VAL_UPIMPV'])
				entxmldict['AGS_Z0091_VAL_UPIMPV'] = re.sub('<ENTITLEMENT_VALUE_CODE>[^>]*?</ENTITLEMENT_VALUE_CODE>','<ENTITLEMENT_VALUE_CODE>'+str(update.ENTITLEMENT_COEFFICIENT)+'</ENTITLEMENT_VALUE_CODE>',entxmldict['AGS_Z0091_VAL_UPIMPV'])
			querystring = querystring + entxmldict[key]
			Trace.Write(querystring)
			Update_xml_uptime = ("UPDATE SAQSCE SET ENTITLEMENT_XML = '{querystring}' '{where_condition}' ".format(querystring=querystring,where_condition=where_condition))	
	

try:
	if LEVEL == 'SERVICE_LEVEL':
		service_level_predefined()
	elif LEVEL == 'UPTIME_IMPROVEMENT':
		tool_uptimetimprovementdriver_update()
	else:
		obj_list = ['SAQSFE','SAQSGE','SAQSCE']
		for obj in obj_list:
			if obj == "SAQSFE":
				#fab_predefined()
				pass
			elif obj == "SAQSGE":
				greenbook_predefined()
			elif obj == "SAQSCE":
				equipment_predefined()
except:
	pass

#predefined_logic()
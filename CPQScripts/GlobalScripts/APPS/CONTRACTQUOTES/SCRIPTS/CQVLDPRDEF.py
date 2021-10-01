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
    quote_record_id = Param.CPQ_Columns['Quote'] 
except:
    quote_record_id = ""
try:
    LEVEL = Param.CPQ_Columns['Level']
except:
    LEVEL = ""
try:
    TreeParam = Param.CPQ_Columns['TreeParam']   
    userId = Param.CPQ_Columns['Userid']
    quote_revision_record_id = Param.CPQ_Columns['quote_revision_record_id']
except: 
    TreeParam = ""
    userId = ""
    quote_revision_record_id = ""

Log.Info('predefined script started')	

def wafernode_predefinedlogic(entitlement_string, equipment_record_id):
    getwafernode_logicdetails = Sql.GetFirst(""" SELECT M.VALDRV_WAFERNODE as VALDRV_WAFERNODE , P.ENTITLEMENT_VALUE_CODE as ENTITLEMENT_VALUE_CODE FROM MAEQUP M JOIN PRENVL P ON M.VALDRV_DEVICETYPE=P.ENTITLEMENT_DISPLAY_VALUE WHERE M.EQUIPMENT_RECORD_ID='{}' """.format(str(equipment_record_id)))
    entitlement_string = re.sub('<ENTITLEMENT_DISPLAY_VALUE>[^>]*?</ENTITLEMENT_DISPLAY_VALUE>','<ENTITLEMENT_DISPLAY_VALUE>'+str(getwafernode_logicdetails.VALDRV_WAFERNODE)+'</ENTITLEMENT_DISPLAY_VALUE>',entitlement_string)
    entitlement_string = re.sub('<ENTITLEMENT_VALUE_CODE>[^>]*?</ENTITLEMENT_VALUE_CODE>','<ENTITLEMENT_VALUE_CODE>'+str(getwafernode_logicdetails.ENTITLEMENT_VALUE_CODE)+'</ENTITLEMENT_VALUE_CODE>',entitlement_string)
    return entitlement_string

def devicetype_predefinedlogic(entitlement_string, equipment_record_id):
    getdevicetype_logicdetails = Sql.GetFirst(""" SELECT M.VALDRV_DEVICETYPE as VALDRV_DEVICETYPE, P.ENTITLEMENT_VALUE_CODE as ENTITLEMENT_VALUE_CODE FROM MAEQUP M JOIN PRENVL P ON M.VALDRV_DEVICETYPE=P.ENTITLEMENT_DISPLAY_VALUE WHERE M.EQUIPMENT_RECORD_ID='{}' """.format(str(equipment_record_id)))
    entitlement_string = re.sub('<ENTITLEMENT_DISPLAY_VALUE>[^>]*?</ENTITLEMENT_DISPLAY_VALUE>','<ENTITLEMENT_DISPLAY_VALUE>'+str(getdevicetype_logicdetails.VALDRV_DEVICETYPE)+'</ENTITLEMENT_DISPLAY_VALUE>',entitlement_string)
    entitlement_string = re.sub('<ENTITLEMENT_VALUE_CODE>[^>]*?</ENTITLEMENT_VALUE_CODE>','<ENTITLEMENT_VALUE_CODE>'+str(getdevicetype_logicdetails.ENTITLEMENT_VALUE_CODE)+'</ENTITLEMENT_VALUE_CODE>',entitlement_string)
    return entitlement_string

def equipment_predefined():
	getallequip_recid = Sql.GetList(""" SELECT EQUIPMENT_RECORD_ID FROM SAQSCE WHERE QUOTE_RECORD_ID='{}' AND QTEREV_RECORD_ID='{}' """.format(str(quote_record_id), str(quote_revision_record_id)))

	for equip_id in getallequip_recid:
		getxml_equip_recid = Sql.GetList(""" SELECT ENTITLEMENT_XML FROM SAQSCE WHERE EQUIPMENT_RECORD_ID='{}' QUOTE_RECORD_ID='{}' AND QTEREV_RECORD_ID='{}' """ .format(str(equip_id.EQUIPMENT_RECORD_ID), str(quote_record_id), str(quote_revision_record_id)))
		
		input_xml = getxml_equip_recid.ENTITLEMENT_XML

		#ref_dict = {'AGS_Z0091_VAL_WAFNOD': wafernode_predefinedlogic,'AGS_Z0091_VAL_DEVTYP': devicetype_predefinedlogic}

		entxmldict = {}
		final_xml=''
		pattern_tag = re.compile(r'(<QUOTE_ITEM_ENTITLEMENT>[\w\W]*?</QUOTE_ITEM_ENTITLEMENT>)')
		pattern_name = re.compile(r'<ENTITLEMENT_ID>([^>]*?)</ENTITLEMENT_ID>')

		for m in re.finditer(pattern_tag, input_xml):
			sub_string = m.group(1)
			x=re.findall(pattern_name,sub_string)
			entxmldict[x[0]]=sub_string

		for key in ref_dict:
			if entxmldict[key]:
				entxmldict[key] = ref_dict[key](entxmldict[key],equip_id.EQUIPMENT_RECORD_ID)
				final_xml += entxmldict[key]
			else:
				final_xml += entxmldict[key]

		Sql.RunQuery( "UPDATE SAQSCE SET ENTITLEMENT_XML = ''{}'' WHERE QUOTE_RECORD_ID = '{}' AND EQUIPMENT_RECORD_ID = '{}' AND QTEREV_RECORD_ID='{}'".format(final_xml, quote_record_id, equip_id.EQUIPMENT_RECORD_ID, quote_revision_record_id) )

##service level
def service_level_predefined(): 
	get_attr_list = {}
	
	updateentXML = getxml_query.ENTITLEMENT_XML
	get_valuedriver_ids = Sql.GetList("SELECT PRENTL.ENTITLEMENT_ID,PRENTL.ENTITLEMENT_DESCRIPTION from PRENTL (NOLOCK) INNER JOIN PRENLI (NOLOCK) ON PRENTL.ENTITLEMENT_ID = PRENLI.ENTITLEMENT_ID WHERE SERVICE_ID = 'Z0091' AND VISIBLE_IN_CONFIG = 1 AND ENTITLEMENT_TYPE ='VALUE DRIVER' AND PRENTL.ENTITLEMENT_ID not in ('AGS_Z0091_VAL_CSTSEG','AGS_Z0091_VAL_SVCCMP','AGS_Z0091_VAL_QLYREQ') AND PRENLI.ENTITLEMENTLEVEL_NAME = 'OFFERING LEVEL' ")

	get_attr_list = [val.ENTITLEMENT_ID for val in get_valuedriver_ids ]
	updating_xml(updateentXML,val.ENTITLEMENT_ID )

	for val in get_valuedriver_ids:
		if 'PRODUCT OFFERING' in val.ENTITLEMENT_DESCRIPTION.upper() or 'INTERCEPT' in val.ENTITLEMENT_DESCRIPTION.upper():
			final_xml = updating_xml(updateentXML,val.ENTITLEMENT_ID )

			Sql.RunQuery( "UPDATE SAQTSE SET ENTITLEMENT_XML = ''{}'' WHERE QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}' AND QTEREV_RECORD_ID='{}'".format(final_xml, quote_record_id,TreeParam, quote_revision_record_id) )



		
	
def updating_xml(input_xml, ent_id):
	
	Trace.Write("entxmldict--"+str(entxmldict))	
	if LEVEL != 'SERVICE_LEVEL':
		#call other level
		pass

	get_coefficient_val = Sql.GetFirst("SELECT ENTITLEMENT_COEFFICIENT, PRENTL.ENTITLEMENT_ID FROM PRENVL (NOLOCK) INNER JOIN PRENTL (NOLOCK) ON PAR_ENPAR_ENTITLEMETITLEMENT_ID = PRENVL.ENTITLEMENT_ID AND PRENVL.SERVICE_ID = PRENTL.SERVICE_ID WHERE PRENVL.ENTITLEMENT_ID = '{}' AND PRENVL.SERVICE_ID = '{}' {}".format(ent_id, TreeParam))
	if get_coefficient_val.ENTITLEMENT_ID in entxmldict.keys():
		entitlement_string = entxmldict[get_coefficient_val.ENTITLEMENT_ID]
		entitlement_string = re.sub('<ENTITLEMENT_DISPLAY_VALUE>[^>]*?</ENTITLEMENT_DISPLAY_VALUE>','<ENTITLEMENT_DISPLAY_VALUE>'+str(get_coefficient_val.ENTITLEMENT_COEFFICIENT)+'</ENTITLEMENT_DISPLAY_VALUE>',entitlement_string)

		entitlement_string = re.sub('<ENTITLEMENT_VALUE_CODE>[^>]*?</ENTITLEMENT_VALUE_CODE>','<ENTITLEMENT_VALUE_CODE>'+str(get_coefficient_val.ENTITLEMENT_COEFFICIENT)+'</ENTITLEMENT_VALUE_CODE>',entitlement_string)
		updateentXML = re.sub(r'<ENTITLEMENT_ID>'+str(get_coefficient_val.ENTITLEMENT_ID)+'<[\w\W]*?</CALCULATION_FACTOR>', entitlement_string, input_xml )
	
	return input_xml




	# assign_xml = """<ENTITLEMENT_ID>{ent_name}</ENTITLEMENT_ID>
	# 					<ENTITLEMENT_DESCRIPTION>{tool_desc}</ENTITLEMENT_DESCRIPTION>
	# 					<ENTITLEMENT_VALUE_CODE>{ent_val_code}</ENTITLEMENT_VALUE_CODE>
	# 					<ENTITLEMENT_DISPLAY_VALUE>{ent_disp_val}</ENTITLEMENT_DISPLAY_VALUE>"""
	# get_xml = re.sub(r'<ENTITLEMENT_ID>'+str(xml_val)+'<[\w\W]*?</CALCULATION_FACTOR>', assign_xml, updateentXML )

			
			

	

##fn call
if LEVEL == 'SERVICE_LEVEL':
	getxml_query = Sql.GetFirst(""" SELECT ENTITLEMENT_XML FROM SAQTSE WHERE QUOTE_RECORD_ID='{}' AND QTEREV_RECORD_ID='{}' AND SERVICE_ID = '{}' """.format(str(quote_record_id), str(quote_revision_record_id), str(TreeParam)))
	entxmldict = {}
	pattern_tag = re.compile(r'(<QUOTE_ITEM_ENTITLEMENT>[\w\W]*?</QUOTE_ITEM_ENTITLEMENT>)')
	pattern_name = re.compile(r'<ENTITLEMENT_ID>([^>]*?)</ENTITLEMENT_ID>')
	
	for m in re.finditer(pattern_tag, input_xml):
		sub_string = m.group(1)
		x=re.findall(pattern_name,sub_string)
		entxmldict[x[0]]=sub_string
	
	service_level_predefined(getxml_query,ENTITLEMENT_XML)
#predefined_logic()
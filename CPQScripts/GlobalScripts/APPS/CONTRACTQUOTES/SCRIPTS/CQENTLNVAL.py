# =========================================================================================================================================
#   __script_name : CQENTLNVAL.py
#   __script_description : THIS SCRIPT IS USED TO GET ENTITLEMENT VALUES.
#   __primary_author__ : 
#   __create_date :8/23/2021
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import Webcom
from datetime import datetime
import Webcom.Configurator.Scripting.Test.TestProduct
from SYDATABASE import SQL
import re
import System.Net
import sys

Sql = SQL()

Trace.Write('script called')
def Request_access_token():
	webclient = System.Net.WebClient()
	webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/json"
	webclient.Headers[
		System.Net.HttpRequestHeader.Authorization
	] = "Basic c2ItYzQwYThiMWYtYzU5NS00ZWJjLTkyYzYtYzM4ODg4ODFmMTY0IWIyNTAzfGNwc2VydmljZXMtc2VjdXJlZCFiMzkxOm9zRzgvSC9hOGtkcHVHNzl1L2JVYTJ0V0FiMD0="
	response = webclient.DownloadString(
		"https://cpqprojdevamat.authentication.us10.hana.ondemand.com:443/oauth/token?grant_type=client_credentials"
	)
	return eval(response)

def entitlement_request(partnumber,request_url,request_type):
	gettodaydate = datetime.now().strftime("%Y-%m-%d")
	Trace.Write('request_url---'+str(request_url))
	Trace.Write('request_type---'+str(request_type))
	partnumber = partnumber.strip()
	webclient = System.Net.WebClient()
	response = Request_access_token()
	#response = eval(response)
	Trace.Write(response["access_token"])
	if request_type.upper() == 'NEW':
		request_url = request_url 
		webclient.Headers[System.Net.HttpRequestHeader.Authorization] = "Bearer " + str(response["access_token"])
		requestdata = '{"productKey":"'+ partnumber+ '","date":"'+gettodaydate+'","context":[{"name":"VBAP-MATNR","value":"'+ partnumber+ '"}]}'

		Trace.Write("requestdata-1888---" + str(requestdata))
		response1 = webclient.UploadString(request_url, str(requestdata))
	else:
		try:		
			#Trace.Write("CHKNGTRAZ_J "+str(webclient.Headers[System.Net.HttpRequestHeader.Authorization]))
			webclient.Headers[System.Net.HttpRequestHeader.Authorization] = "Bearer " + str(response["access_token"])			
			response1 = webclient.DownloadString(request_url)
		except Exception as e:
			Trace.Write('1897-----'+str(e))
			response1 = {}
					
	response1 = str(response1).replace(": true", ': "true"').replace(": false", ': "false"')
	Trace.Write("response1_J "+str(response1))
	return eval(response1)

def entitlement_attributes_lvel_request(partnumber,inserted_value_list,ent_level_table,where_cond):
	level_name = get_clicked_greenbook = get_greenbook_value_itemlevel = ''
	if ent_level_table == "SAQTSE":
		level_name = 'OFFERING LEVEL'
	elif ent_level_table == "SAQSFE":
		level_name = 'OFFERING FAB LEVEL'
	elif ent_level_table == "SAQITE":
		get_entitlement_qt_item_sctructure = Sql.GetFirst("select ENTITLEMENT_XML,SERVICE_ID,GREENBOOK from SAQITE where {where_condition}".format(where_condition= where_cond))
		#flag_excluse=0
		get_service_val =get_entitlement_qt_item_sctructure.SERVICE_ID
		get_greenbook_value_itemlevel = get_entitlement_qt_item_sctructure.GREENBOOK
		#condition based on quote item strcuture start
		if get_entitlement_qt_item_sctructure:
			Trace.Write('get_service_val-32----'+str(get_service_val))
			get_ent_val = ''
			updateentXML = get_entitlement_qt_item_sctructure.ENTITLEMENT_XML
			pattern_tag = re.compile(r'(<QUOTE_ITEM_ENTITLEMENT>[\w\W]*?</QUOTE_ITEM_ENTITLEMENT>)')
			pattern_id = re.compile(r'<ENTITLEMENT_ID>(AGS_'+str(get_service_val)+'_PQB_QTITST)</ENTITLEMENT_ID>')
			pattern_name = re.compile(r'<ENTITLEMENT_DISPLAY_VALUE>([^>]*?)</ENTITLEMENT_DISPLAY_VALUE>')
			for m in re.finditer(pattern_tag, updateentXML):
				sub_string = m.group(1)
				get_ent_id = re.findall(pattern_id,sub_string)
				get_ent_val= re.findall(pattern_name,sub_string)
				if get_ent_id:
					Trace.Write(str(sub_string)+'---get_ent_name---'+str(get_ent_val[0]))
					get_ent_val = str(get_ent_val[0])
					#flag_excluse=1
					break
		Trace.Write('get_ent_val---4750--'+str(get_ent_val))
		if str(get_ent_val).upper() == "OFFERING + EQUIPMENT":
			level_name = 'OFFERING FAB GREENBOOK TOOL LEVEL'
		elif str(get_ent_val).upper() == "OFFERING + GREENBOOK + GR EQUI":
			level_name = 'OFFERING FAB GREENBOOK LEVEL'
		else:
			level_name = 'OFFERING LEVEL'
		#condition based on quote item strcuture end
	elif ent_level_table == "SAQSGE":
		if Product.GetGlobal('TreeParam') == 'Add-On Products' and Product.GetGlobal("TreeParentLevel3") == 'Product Offerings':
			get_clicked_greenbook = Product.GetGlobal("TreeParentLevel0")
		else:
			get_clicked_greenbook = Product.GetGlobal('TreeParam')
		level_name = 'OFFERING FAB GREENBOOK LEVEL'
	elif ent_level_table == "SAQSCE":
		get_clicked_greenbook = Product.GetGlobal('TreeParam')
		level_name = 'OFFERING FAB GREENBOOK TOOL LEVEL'
	elif ent_level_table == "SAQGPE":
		get_clicked_greenbook = Product.GetGlobal("TreeParentLevel1")
		level_name = 'OFFERING FAB GREENBOOK TOOL LEVEL'
	else:
		get_clicked_greenbook = Product.GetGlobal('TreeParam')
		level_name = 'OFFERING FAB GREENBOOK TOOL ASSEMBLY LEVEL'
	get_attr_leve_based_list =[]
	if get_clicked_greenbook == "" and ent_level_table == "SAQITE":
		Trace.Write('107----get_greenbook_value_itemlevel----'+str(get_greenbook_value_itemlevel))
		get_clicked_greenbook =get_greenbook_value_itemlevel
	for val in inserted_value_list:
		#Trace.Write(str(level_name)+'--level_name--value---'+str(val))
		if level_name in ["OFFERING FAB LEVEL","OFFERING LEVEL"]:
			get_visible_fields= SqlHelper.GetFirst("select ENTITLEMENTLEVEL_ID from PRENLI where ENTITLEMENT_ID = '"+str(val)+"' and ENTITLEMENTLEVEL_NAME = '"+str(level_name)+"'")
		else:
			get_visible_fields= Sql.GetFirst("select PRENLI.ENTITLEMENTLEVEL_ID from PRENLI JOIN PRENGB on PRENLI.ENTITLEMENT_ID=PRENGB.ENTITLEMENT_ID where PRENLI.ENTITLEMENT_ID = '"+str(val)+"' and PRENLI.ENTITLEMENTLEVEL_NAME = '"+str(level_name)+"' and PRENGB.GREENBOOK = '"+str(get_clicked_greenbook)+"'")
		if get_visible_fields:
			get_attr_leve_based_list.append(str(val))
	#Trace.Write('get_attr_leve_based_list--type return'+str(type(get_attr_leve_based_list)))
	return get_attr_leve_based_list

action= Param.action
#to get the product status
try:
	where_cond= Param.where_cond
	#Trace.Write('where_cond-----try--'+str(where_cond))
except:
	where_cond = ""
	#Trace.Write('where_cond----except--'+str(where_cond))
try:
	ent_level_table= Param.ent_level_table
	#Trace.Write('ent_level_table---try---'+str(ent_level_table))
except:
	ent_level_table = ""
	#Trace.Write('ent_level_table---except---'+str(ent_level_table))
try:	
	partnumber= Param.partnumber
	#Trace.Write('partnumber---try---'+str(partnumber))
except:	
	partnumber = ""
	#Trace.Write('partnumber--except----'+str(partnumber))
try:
	inserted_value_list = list(Param.inserted_value_list)
except:
	inserted_value_list = []
##to get the response
try:
	request_url = Param.request_url
except:
	request_url = ""
try:
	request_type = Param.request_type
except:
	request_type = ""
# if action == 'GET_STATUS':
# 	Result = get_entitlement_status(partnumber,where_cond,ent_level_table)
if action == 'GET_RESPONSE':
	Result = entitlement_request(partnumber,request_url,request_type)
if action == 'get_from_prenli':
	Result = entitlement_attributes_lvel_request(partnumber,inserted_value_list,ent_level_table,where_cond)
	




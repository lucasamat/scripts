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
import time
from SYDATABASE import SQL
Sql = SQL()

import System.Net
import sys


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
			Trace.Write("CHKNGTRAZ_J "+str(webclient.Headers[System.Net.HttpRequestHeader.Authorization]))
			webclient.Headers[System.Net.HttpRequestHeader.Authorization] = "Bearer " + str(response["access_token"])			
			response1 = webclient.DownloadString(request_url)
		except Exception as e:
			Trace.Write('1897-----'+str(e))
			response1 = {}
					
	response1 = str(response1).replace(": true", ': "true"').replace(": false", ': "false"')
	Trace.Write("response1_J "+str(response1))
	return eval(response1)

def entitlement_attributes_lvel_request(partnumber,inserted_value_list,ent_level_table,where_cond):
	Trace.Write('partnumber---61---'+str(partnumber))
	Trace.Write('ent_level_table---61---'+str(ent_level_table))
	Trace.Write('where_cond---61---'+str(where_cond))
	Trace.Write('inserted_value_list---61---'+str(list(inserted_value_list)))
	level_name = get_clicked_greenbook = ''
	if ent_level_table == "SAQTSE":
		level_name = 'OFFERING LEVEL'
	elif ent_level_table == "SAQSFE":
		level_name = 'OFFERING FAB LEVEL'
	elif ent_level_table == "SAQSGE":
		get_clicked_greenbook = Product.GetGlobal('TreeParam')
		Trace.Write('get_clicked_greenbook---'+str(get_clicked_greenbook))
		level_name = 'OFFERING FAB GREENBOOK LEVEL'
	elif ent_level_table == "SAQSCE":
		get_clicked_greenbook = Product.GetGlobal('TreeParam')
		Trace.Write('get_clicked_greenbook---'+str(get_clicked_greenbook))
		level_name = 'OFFERING FAB GREENBOOK TOOL LEVEL'
	else:
		get_clicked_greenbook = Product.GetGlobal('TreeParam')
		Trace.Write('get_clicked_greenbook---'+str(get_clicked_greenbook))
		level_name = 'OFFERING FAB GREENBOOK TOOL ASSEMBLY LEVEL'
	get_attr_leve_based_list =[]
	for val in inserted_value_list:
		#Trace.Write(str(level_name)+'--level_name--value---'+str(val))
		if level_name in ["OFFERING FAB LEVEL","OFFERING LEVEL"]:
			get_visible_fields= SqlHelper.GetFirst("select ENTITLEMENTLEVEL_ID from PRENLI where ENTITLEMENT_ID = '"+str(val)+"' and ENTITLEMENTLEVEL_NAME = '"+str(level_name)+"'")
		else:
			get_visible_fields= Sql.GetFirst("select PRENLI.ENTITLEMENTLEVEL_ID from PRENLI JOIN PRENGB on PRENLI.ENTITLEMENT_ID=PRENGB.ENTITLEMENT_ID where PRENLI.ENTITLEMENT_ID = '"+str(val)+"' and PRENLI.ENTITLEMENTLEVEL_NAME = '"+str(level_name)+"' and PRENGB.GREENBOOK = '"+str(get_clicked_greenbook)+"'")
		if get_visible_fields:
			get_attr_leve_based_list.append(str(val))
	Trace.Write('get_attr_leve_based_list--type return'+str(type(get_attr_leve_based_list)))
	return get_attr_leve_based_list
# def get_entitlement_status(partnumber,where_cond,ent_level_table):
# 	get_cps = Sql.GetFirst("SELECT * FROM {} {}".format(ent_level_table,where_cond) )
# 	if get_cps:
# 		request_url = "https://cpservices-product-configuration.cfapps.us10.hana.ondemand.com/api/v2/configurations/"+str(get_cps.CPS_CONFIGURATION_ID)
# 		fullresponse = entitlement_request(partnumber,request_url,'EXISTING')
# 		if fullresponse:
# 			status = fullresponse['complete']
# 			Trace.Write('status--'+str(status))
# 			return status


action= Param.action

#to get the product status



try:
	where_cond= Param.where_cond
	Trace.Write('where_cond-----try--'+str(where_cond))
except:
	where_cond = ""
	Trace.Write('where_cond----except--'+str(where_cond))
try:
	ent_level_table= Param.ent_level_table
	Trace.Write('ent_level_table---try---'+str(ent_level_table))
except:
	ent_level_table = ""
	Trace.Write('ent_level_table---except---'+str(ent_level_table))
try:
	
	partnumber= Param.partnumber
	Trace.Write('partnumber---try---'+str(partnumber))
except:
	
	partnumber = ""
	Trace.Write('partnumber--except----'+str(partnumber))
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
Trace.Write('ent_level_table------'+str(ent_level_table))
Trace.Write('partnumber------'+str(partnumber))
# if action == 'GET_STATUS':
# 	Result = get_entitlement_status(partnumber,where_cond,ent_level_table)
if action == 'GET_RESPONSE':
	Result = entitlement_request(partnumber,request_url,request_type)
if action == 'get_from_prenli':
	Result = entitlement_attributes_lvel_request(partnumber,inserted_value_list,ent_level_table,where_cond)
	




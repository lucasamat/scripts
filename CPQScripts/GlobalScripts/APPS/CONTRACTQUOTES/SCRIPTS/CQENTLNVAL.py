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

def ChildEntRequest(partnumber,tableName,where):	
	get_c4c_quote_id = Sql.GetFirst("select * from SAQTMT where MASTER_TABLE_QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(quote_record_id,revision_record_id))
	#attribute_id,value_code,attr_type,display_name,config_id,cpsmatchID,isdefault	
	ent_child_temp = "ANC_ENT_BKP_"+str(get_c4c_quote_id.C4C_QUOTE_ID)
	cpsmatchID = 1
	Request_URL="https://cpservices-product-configuration.cfapps.us10.hana.ondemand.com/api/v2/configurations?autoCleanup=False"
	Fullresponse = entitlement_request(partnumber,Request_URL,'NEW')
	config_id = Fullresponse["id"]	
	try:
		if tableName :
			ent_child_temp_drop = Sql.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(ent_child_temp)+"'' ) BEGIN DROP TABLE "+str(ent_child_temp)+" END  ' ")
			where_cond = where.replace("'","''")
			Sql.GetFirst("sp_executesql @T=N'declare @H int; Declare @val Varchar(MAX);DECLARE @XML XML; SELECT @val = FINAL from(select  REPLACE(entitlement_xml,''<QUOTE_ITEM_ENTITLEMENT>'',sml) AS FINAL FROM (select ''  <QUOTE_ITEM_ENTITLEMENT><QUOTE_ID>''+quote_id+''</QUOTE_ID><QUOTE_RECORD_ID>''+QUOTE_RECORD_ID+''</QUOTE_RECORD_ID><QTEREV_RECORD_ID>''+QTEREV_RECORD_ID+''</QTEREV_RECORD_ID><GREENBOOK>''+GREENBOOK+''</GREENBOOK><SERVICE_ID>''+service_id+''</SERVICE_ID>'' AS sml,replace(replace(replace(replace(replace(replace(replace(replace(replace(ENTITLEMENT_XML,''&'','';#38''),'''','';#39''),'' < '','' &lt; '' ),'' > '','' &gt; '' ),''_>'',''_&gt;''),''_<'',''_&lt;''),''&'','';#38''),''<10%'',''&lt;10%''),''<='',''&lt;='')   as entitlement_xml from "+str(tableName)+"(nolock)  WHERE "+str(where_cond)+"  )A )a SELECT @XML = CONVERT(XML,''<ROOT>''+@VAL+''</ROOT>'') exec sys.sp_xml_preparedocument @H output,@XML; select QUOTE_ID,QUOTE_RECORD_ID,QTEREV_RECORD_ID,SERVICE_ID,ENTITLEMENT_ID,ENTITLEMENT_NAME,ENTITLEMENT_COST_IMPACT,ENTITLEMENT_TYPE,ENTITLEMENT_VALUE_CODE,ENTITLEMENT_DISPLAY_VALUE,IS_DEFAULT INTO "+str(ent_child_temp)+"  from openxml(@H, ''ROOT/QUOTE_ITEM_ENTITLEMENT'', 0) with (QUOTE_ID VARCHAR(100) ''QUOTE_ID'',QUOTE_RECORD_ID VARCHAR(100) ''QUOTE_RECORD_ID'',QTEREV_RECORD_ID VARCHAR(100) ''QTEREV_RECORD_ID'',ENTITLEMENT_NAME VARCHAR(100) ''ENTITLEMENT_NAME'',ENTITLEMENT_ID VARCHAR(100) ''ENTITLEMENT_ID'',SERVICE_ID VARCHAR(100) ''SERVICE_ID'',GREENBOOK VARCHAR(100) ''GREENBOOK'',ENTITLEMENT_COST_IMPACT VARCHAR(100) ''ENTITLEMENT_COST_IMPACT'',ENTITLEMENT_TYPE VARCHAR(100) ''ENTITLEMENT_TYPE'',ENTITLEMENT_VALUE_CODE VARCHAR(100) ''ENTITLEMENT_VALUE_CODE'',ENTITLEMENT_DISPLAY_VALUE VARCHAR(100) ''ENTITLEMENT_DISPLAY_VALUE'',IS_DEFAULT VARCHAR(100) ''IS_DEFAULT'') ; exec sys.sp_xml_removedocument @H; '")

			Parentgetdata=Sql.GetList("SELECT * FROM {} ".format(ent_child_temp))
			#Log.Info("where------ "+str(where))
			if Parentgetdata:					
				response = Request_access_token()					
				Request_URL = "https://cpservices-product-configuration.cfapps.us10.hana.ondemand.com/api/v2/configurations/"+str(config_id)+"/items/1"
				#webclient.Headers[System.Net.HttpRequestHeader.Authorization] = "Bearer " + str(response["access_token"])
				cpsmatchID = 1
				
				for row in Parentgetdata:
					webclient = System.Net.WebClient()
					
					webclient.Headers[System.Net.HttpRequestHeader.Authorization] = "Bearer " + str(response["access_token"])
					Trace.Write("enval--end_id --"+str(row.ENTITLEMENT_ID)+'-'+str(row.ENTITLEMENT_VALUE_CODE))
					#webclient.Headers.Add("If-Match", "111")
					webclient.Headers.Add("If-Match", '"'+str(cpsmatchID)+'"')	
					get_ent_type = Sql.GetFirst("select ENTITLEMENT_TYPE from PRENTL where ENTITLEMENT_ID = '"+str(row.ENTITLEMENT_ID)+"' and SERVICE_ID = '"+str(partnumber)+"'")	
					if row.ENTITLEMENT_VALUE_CODE and row.ENTITLEMENT_VALUE_CODE not in ('undefined','None') and   row.ENTITLEMENT_ID !='undefined' and row.ENTITLEMENT_DISPLAY_VALUE !='select' and row.IS_DEFAULT =='0' and str(get_ent_type.ENTITLEMENT_TYPE).upper() not in ["VALUE DRIVER","VALUE DRIVER COEFFICIENT"] and row.ENTITLEMENT_VALUE_CODE != 0:
						try:
							requestdata = '{"characteristics":['
							
							requestdata +='{"id":"'+ str(row.ENTITLEMENT_ID) + '","values":[' 
							if row.ENTITLEMENT_TYPE in ('Check Box','CheckBox'):
								Trace.Write("auto update--val-"+str(row.ENTITLEMENT_VALUE_CODE)+'---'+str( row.ENTITLEMENT_ID))
								for code in row.ENTITLEMENT_VALUE_CODE.split(','):
									requestdata += '{"value":"' + str(code) + '","selected":true}'
									requestdata +=','
								requestdata +=']},'	
								Trace.Write("auto update-val--"+str(requestdata))
							else:
								requestdata+= '{"value":"' +str(row.ENTITLEMENT_VALUE_CODE) + '","selected":true}]},'
							requestdata += ']}'
							requestdata = requestdata.replace('},]','}]')
							Trace.Write("requestdata--child-val- " + str(requestdata))
							response1 = webclient.UploadString(Request_URL, "PATCH", str(requestdata))
							#cpsmatchID = cpsmatchID + 1			
							cpsmatchID = webclient.ResponseHeaders["Etag"]
							cpsmatchID = re.sub('"',"",cpsmatchID)
						except Exception:
							Trace.Write("Patch Error-1-"+str(sys.exc_info()[1]))
							cpsmatchID = cpsmatchID


	except Exception:
		Log.Info("Patch Error-2-"+str(sys.exc_info()[1]))        
	ent_child_temp_drop = Sql.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(ent_child_temp)+"'' ) BEGIN DROP TABLE "+str(ent_child_temp)+" END  ' ")
	return cpsmatchID,config_id



action= Param.action
#to get the product status
try:
	where_cond= Param.where_cond
	#Trace.Write('where_cond-----try--'+str(where_cond))
except:
	where_cond = ""
	#Trace.Write('where_cond----except--'+str(where_cond))
try:
	quote_record_id = Param.quote_record_id
except:
	quote_record_id = ''
try:
	revision_record_id = Param.revision_record_id
except:
	revision_record_id = ''
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
elif action == 'get_from_prenli':
	Result = entitlement_attributes_lvel_request(partnumber,inserted_value_list,ent_level_table,where_cond)
elif action == 'ENTITLEMENT_UPDATE':
	Result = ChildEntRequest(partnumber,ent_level_table,where_cond)






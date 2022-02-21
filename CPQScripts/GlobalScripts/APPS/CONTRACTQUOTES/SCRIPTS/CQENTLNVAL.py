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
	Trace.Write("ent_level_table--"+str(ent_level_table))
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
		Trace.Write('107-gpe---get_greenbook_value_itemlevel----'+str(get_greenbook_value_itemlevel))
		get_clicked_greenbook = Product.GetGlobal("TreeParentLevel1")
		level_name = 'OFFERING FAB GREENBOOK TOOL LEVEL'
	else:
		Trace.Write('107-else---get_greenbook_value_itemlevel----'+str(get_greenbook_value_itemlevel))
		get_clicked_greenbook = Product.GetGlobal('TreeParam')
		level_name = 'OFFERING FAB GREENBOOK TOOL ASSEMBLY LEVEL'
	get_attr_leve_based_list =[]
	if get_clicked_greenbook == "" and ent_level_table == "SAQITE":
		Trace.Write('107----get_greenbook_value_itemlevel----'+str(get_greenbook_value_itemlevel))
		get_clicked_greenbook =get_greenbook_value_itemlevel
	for val in inserted_value_list:
		#Trace.Write(str(level_name)+'--level_name--value---'+str(val))
		if level_name in ["OFFERING FAB LEVEL","OFFERING LEVEL"]:
			get_visible_fields= Sql.GetFirst("select ENTITLEMENTLEVEL_ID from PRENLI where ENTITLEMENT_ID = '"+str(val)+"' and ENTITLEMENTLEVEL_NAME = '"+str(level_name)+"'")
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
					if get_ent_type.ENTITLEMENT_TYPE:
						ent_type = get_ent_type.ENTITLEMENT_TYPE
					else:
						ent_type = 'entitlement'
					if row.ENTITLEMENT_VALUE_CODE and row.ENTITLEMENT_VALUE_CODE not in ('undefined','None') and   row.ENTITLEMENT_ID !='undefined' and row.ENTITLEMENT_DISPLAY_VALUE !='select'  and str(ent_type).upper() not in ["VALUE DRIVER","VALUE DRIVER COEFFICIENT"] and row.ENTITLEMENT_VALUE_CODE != '0':
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

def _construct_dict_xml(updateentXML):
	entxmldict = {}
	pattern_tag = re.compile(r'(<QUOTE_ITEM_ENTITLEMENT>[\w\W]*?</QUOTE_ITEM_ENTITLEMENT>)')
	pattern_name = re.compile(r'<ENTITLEMENT_ID>([^>]*?)</ENTITLEMENT_ID>')
	entitlement_display_value_tag_pattern = re.compile(r'<ENTITLEMENT_DISPLAY_VALUE>([^>]*?)</ENTITLEMENT_DISPLAY_VALUE>')
	display_val_dict = {}
	if updateentXML:
		for m in re.finditer(pattern_tag, updateentXML):
			sub_string = m.group(1)
			x=re.findall(pattern_name,sub_string)
			if x:
				entitlement_display_value_tag_match = re.findall(entitlement_display_value_tag_pattern,sub_string)
				if entitlement_display_value_tag_match:
					display_val_dict[x[0]] = entitlement_display_value_tag_match[0]
			entxmldict[x[0]]=sub_string
	return entxmldict,display_val_dict

def entitlemnt_attr_update(partnumber,entitlement_table, where):
	get_equipment = Sql.GetList("SELECT * FROM {} {}".format(entitlement_table, where))
	entitlement_details = [{
								"field":["INTCPV","Intercept","AGS_{}_VAL_INTCPT".format(partnumber)]						
								},
								{
								"field":["INTCPC","Intercept Coefficient","AGS_{}_VAL_INTCCO".format(partnumber)]
								},
								{
								"field":["OSSVDV","Total Cost W/O Seedstock","AGS_{}_VAL_TBCOCO".format(partnumber)]	
								},
								{
								"field":["POFVDV","Product Offering","AGS_{}_VAL_POFFER".format(partnumber)]	
								},
								{
								"field":["POFVDC","Product Offering Coefficient","AGS_{}_VAL_POFFCO".format(partnumber)]
								},
								{
								"field":["GBKVDV","Greenbook","AGS_{}_VAL_GRNBKV".format(partnumber)]	
								},
								{
								"field":["GBKVDC","Greenbook Coefficient","AGS_{}_VAL_GRNBCO".format(partnumber)]
								},
								{
								"field":["UIMVDV","Uptime Improvement","AGS_{}_VAL_UPIMPV".format(partnumber)]	
								},
								{
								"field":["UIMVDC","Uptime Improvement Coefficient","AGS_{}_VAL_UPIMCO".format(partnumber)]
								},
								{
								"field":["CAVVDV","Capital Avoidance","AGS_{}_VAL_CAPAVD".format(partnumber)]	
								},
								{
								"field":["CAVVDC","Capital Avoidance Coefficient","AGS_{}_VAL_CAPACO".format(partnumber)]
								},
								{
								"field":["WNDVDV","Wafer Node","AGS_{}_VAL_WAFNOD".format(partnumber)]	
								},
								{
								"field":["WNDVDC","Wafer Node Coefficient","AGS_{}_VAL_WAFNCO".format(partnumber)]
								},
								{
								"field":["CCRTMV","Contract Coverage & Response Time","AGS_{}_VAL_CCRTME".format(partnumber)]	
								},
								{
								"field":["CCRTMC","Contract Coverage & Response Time Coefficient","AGS_{}_VAL_CCRTCO".format(partnumber)]
								},
								{
								"field":["SCMVDV","Service Complexity","AGS_{}_VAL_SCCCDF".format(partnumber)]
								},
								{
								"field":["SCMVDC", "Service Complexity Coefficient", "AGS_{}_VAL_SCCCCO".format(partnumber)]
								},
								{
								"field":["CCDFFV","Cleaning Coating Differentiation","AGS_{}_VAL_CCDVAL".format(partnumber)]
								},
								{
								"field":["CCDFFC", "Cleaning Coating Diff coeff.", "AGS_{}_VAL_CCDVCO".format(partnumber)]
								},
								{
								"field":["NPIVDV","NPI","AGS_{}_VAL_NPIREC".format(partnumber)]
								},	
								{
								"field":["NPIVDC", "NPI Coefficient", "AGS_{}_VAL_NPICOF".format(partnumber)]
								},	
								{
								"field":["DTPVDV","Device Type","AGS_{}_VAL_DEVTYP".format(partnumber)]
								},
								{
								"field":["DTPVDC", "Device Type Coefficient", "AGS_{}_VAL_DEVTCO".format(partnumber)]
								},	
								{
								"field":["CSTVDV","# CSA Tools per Fab","AGS_{}_VAL_TLSFAB".format(partnumber)]
								},	
								{
								"field":["CSTVDC", "# CSA Tools per Fab Coefficient", "AGS_{}_VAL_TLSFCO".format(partnumber)]
								},	
								{
								"field":["CSGVDV","Customer Segment","AGS_{}_VAL_CSTSEG".format(partnumber)]
								},
								{
								"field":["CSGVDC", "Customer Segment Coefficent", "AGS_{}_VAL_CSSGCO".format(partnumber)]
								},	
								{
								"field":["QRQVDV","Quality Required","AGS_{}_VAL_QLYREQ".format(partnumber)]
								},
								{
								"field":["QRQVDC", "Quality Required Coefficient", "AGS_{}_VAL_QLYRCO".format(partnumber)]
								},	
								{
								"field":["SVCVDV","Service Competition","AGS_{}_VAL_SVCCMP".format(partnumber)]
								},
								{
								"field":["SVCVDC", "Service Competition Coefficient", "AGS_{}_VAL_SVCCCO".format(partnumber)]
								},
								{
								"field":["RKFVDV","Risk Factor","AGS_{}_VAL_RSKFVD".format(partnumber)]
								},
								{
								"field":["RKFVDC", "Risk Factor Coefficient", "AGS_{}_VAL_RSKFCO".format(partnumber)]
								},
								{
								"field":["PBPVDV","PDC Base Price","AGS_{}_VAL_PDCBCO".format(partnumber)]
								},
								{
								"field":["CMLAB_ENT","Corrective Maintenance Labor","AGS_{}_NET_CRMALB".format(partnumber)]
								},		
								{
								"field":["CNSMBL_ENT","Consumable","AGS_{}_TSC_CONSUM".format(partnumber)]
								},
								{
								"field":["CNTCVG_ENT","Contract Coverage","AGS_{}_CVR_CNTCOV".format(partnumber)]
								},	
								{
								"field":["NCNSMB_ENT","Non-Consumable","AGS_{}_TSC_NONCNS".format(partnumber)]
								},	
								{
								"field":["PMEVNT_ENT","Quote Type","AGS_{}_PQB_QTETYP".format(partnumber)]
								},		
								{
								"field":["PMLAB_ENT","Preventative Maintenance Labor","AGS_{}_NET_PRMALB".format(partnumber)]
								},	
								{
								"field":["PRMKPI_ENT","Primary KPI. Perf Guarantee","AGS_{}_KPI_PRPFGT".format(partnumber)]
								},
								{
								"field":["OFRING","Product Offering","AGS_{}_VAL_POFFER".format(partnumber)]
								},	
								{
								"field":["QTETYP","Quote Type","AGS_{}_PQB_QTETYP".format(partnumber)]
								},	
								{
								"field":["BILTYP","Billing Type","AGS_{}_PQB_BILTYP".format(partnumber)]
								},	
								{
								"field":["BPTKPI","Bonus & Penalty Tied to KPI","AGS_{}_KPI_BPTKPI".format(partnumber)]
								},
								{
								"field":["ATGKEY","Additional Target KPI","AGS_{}_KPI_TGTKPI".format(partnumber)]
								},	
								{
								"field":["ATNKEY","Additional Target KPI(Non-std)","AGS_{}_KPI_TGKPNS".format(partnumber)]
								},
								{
								"field":["NWPTON","New Parts Only","AGS_{}_TSC_RPPNNW".format(partnumber)]
								},
								{
								"field":["HEDBIN","Head break-in","AGS_{}_STT_HDBRIN".format(partnumber)]
								},
						]
			
	if get_equipment:
		for ent_rec in get_equipment:
			addtional_whr = ''
			update_values = ""
			if entitlement_table == 'SAQSCE':
				addtional_whr = " AND GREENBOOK = '{}' AND EQUIPMENT_ID = '{}'".format(ent_rec.GREENBOOK,ent_rec.EQUIPMENT_ID )
			elif entitlement_table == 'SAQGPE':
				addtional_whr = " AND GREENBOOK = '{}' AND GOT_CODE = '{}' AND PM_ID = '{}'".format(ent_rec.GREENBOOK,ent_rec.GOT_CODE,  ent_rec.PM_ID)
			get_xml_dict,dict_val = _construct_dict_xml(ent_rec.ENTITLEMENT_XML)
			Trace.Write("dict_val--"+str(dict_val))
			for entitlement_detail in entitlement_details:
				entitlement_table_col = entitlement_detail['field'][0]
				entitlement_id = entitlement_detail['field'][2]
				if entitlement_id in dict_val.keys():
					entitlement_disp_val = dict_val[entitlement_id]
					if entitlement_disp_val:
						update_values += ", {} = '{}' ".format(entitlement_table_col, entitlement_disp_val  ) 
					else:
						update_values += ", {} = NULL ".format(entitlement_table_col, entitlement_disp_val  )
			if update_values:
				update_query = "UPDATE {entitlement_table} SET {cols}  {where} {addtional_whr}".format(entitlement_table = entitlement_table, cols = update_values, where =where,addtional_whr= addtional_whr )
				update_query = update_query.replace('SET ,','SET ')
				#Log.Info('update_query---'+str(update_query))
				Sql.RunQuery(update_query)							
	return True

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
elif action == 'ENTITLEMENT_COLUMN_UPDATE':
	Result = entitlemnt_attr_update(partnumber,ent_level_table,where_cond)






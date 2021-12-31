# =========================================================================================================================================
#   __script_name : CQASSMEDIT.PY
#   __script_description : THIS SCRIPT IS USED TO EDIT THE ASSEMBLY LEVEL GRID FOR SENDING EQUIPMENT.
#   __primary_author__ : 
#   __create_date :8/17/2021
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import Webcom
from SYDATABASE import SQL
from datetime import datetime
import Webcom.Configurator.Scripting.Test.TestProduct
import time
Sql = SQL()
import SYCNGEGUID as CPQID
import System.Net
import sys
import re



#A055S000P01-6826- Relocation chamber starts...
def update_assembly_level(Values):
	#TreeParentParam = Product.GetGlobal("TreeParentLevel0")
	# TreeSuperParentParam = Product.GetGlobal("TreeParentLevel1")
	# TreeTopSuperParentParam =  Product.GetGlobal("TreeParentLevel2")
	#ContractRecordId = Quote.GetGlobal("contract_quote_record_id")
	record_ids = [
				CPQID.KeyCPQId.GetKEYId('SAQSSA', str(value))
				if value.strip() != "" and 'SAQSSA' in value
				else value
				for value in Values
			]
	#Trace.Write('unselected_values---'+str(unselected_values))
	un_selected_record_ids = [
				CPQID.KeyCPQId.GetKEYId('SAQSSA', str(value))
				if value.strip() != "" and 'SAQSSA' in value
				else value
				for value in unselected_values
			]
	record_ids = str(tuple(record_ids)).replace(",)",")")
	un_selected_record_ids = str(tuple(un_selected_record_ids)).replace(",)",")")
	# Trace.Write('record_ids------inside-'+str(record_ids))
	#Trace.Write('un_selected_record_ids------inside-'+str(un_selected_record_ids))
	try:
		equipment_id = Param.equipment_id
	except:
		equipment_id =""
	##update for selected assembly
	if record_ids != '()':
		Sql.RunQuery("update SAQSSA set INCLUDED = 1 where QUOTE_SERVICE_SENDING_FAB_EQUIP_ASS_ID in {} ".format(record_ids))
		
		get_assembly_query = Sql.GetList("SELECT SND_ASSEMBLY_ID FROM SAQSSA where QUOTE_SERVICE_SENDING_FAB_EQUIP_ASS_ID in {}".format(record_ids))
		get_assembly = [val.SND_ASSEMBLY_ID for val in get_assembly_query]
		get_assembly = str(tuple(get_assembly)).replace(',)',')')
		if equipment_id:
			Sql.RunQuery("update SAQSCA set INCLUDED = 1 where ASSEMBLY_ID in {} and QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' and SERVICE_ID = '{}' and EQUIPMENT_ID = '{}'".format(get_assembly,ContractRecordId, revision_record_id,TreeParentParam,equipment_id))
	##update for un selected assembly
	if un_selected_record_ids != '()':
		#update SAQSSA
		Sql.RunQuery("update SAQSSA set INCLUDED = 0 where QUOTE_SERVICE_SENDING_FAB_EQUIP_ASS_ID in {} ".format(un_selected_record_ids))
		
		#update SAQSCA
		get_assembly_query = Sql.GetList("SELECT SND_ASSEMBLY_ID FROM SAQSSA where QUOTE_SERVICE_SENDING_FAB_EQUIP_ASS_ID in {}".format(un_selected_record_ids))
		get_assembly = [val.SND_ASSEMBLY_ID for val in get_assembly_query]
		get_assembly = str(tuple(get_assembly)).replace(',)',')')
		if equipment_id:
			Sql.RunQuery("update SAQSCA set INCLUDED = 0 where ASSEMBLY_ID in {} and QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' and SERVICE_ID = '{}' and EQUIPMENT_ID = '{}'".format(get_assembly,ContractRecordId,revision_record_id,TreeParentParam,equipment_id))
		
	if equipment_id:
		get_total_count = Sql.GetFirst("""select count(*) as cnt from SAQSSA (NOLOCK) where SND_EQUIPMENT_ID = '{}' and EQUIPMENTTYPE_ID = 'CHAMBER' and QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' and SERVICE_ID = '{}'""".format(equipment_id,ContractRecordId,revision_record_id,TreeParentParam))
		
		included_count = Sql.GetFirst("""select count(*) as cnt from SAQSSA (NOLOCK) where SND_EQUIPMENT_ID = '{}' and EQUIPMENTTYPE_ID = 'CHAMBER' and INCLUDED = 1 and QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' and SERVICE_ID = '{}'""".format(equipment_id,ContractRecordId,revision_record_id,TreeParentParam))
		
		###updating equipment level tables
		if get_total_count.cnt == included_count.cnt:
			#update SAQSSE
			Sql.RunQuery("update SAQSSE set INCLUDED = 'TOOL' where SND_EQUIPMENT_ID ='{}' and QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' and SERVICE_ID = '{}' ".format(equipment_id,ContractRecordId, revision_record_id,TreeParentParam))
			#update SAQSCO
			Sql.RunQuery("update SAQSCO set INCLUDED = 'TOOL' where EQUIPMENT_ID ='{}' and QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' and SERVICE_ID = '{}' ".format(equipment_id,ContractRecordId, revision_record_id,TreeParentParam))
			if 'Z0007' in TreeParentParam:
				whereReq = "QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' and SERVICE_ID = '{}' AND EQUIPMENT_ID = '{}'".format(ContractRecordId, revision_record_id,TreeParentParam,equipment_id)
				add_where = "and INCLUDED = 'TOOL'"
				AttributeID = 'AGS_QUO_QUO_TYP'
				NewValue = 'Tool based' 
				update_flag = entitlement_update(whereReq,add_where,AttributeID,NewValue,TreeParentParam,'SAQSCE')
				if update_flag:
					##Assembly level roll down
					userId = User.Id
					datetimenow = datetime.now().strftime("%m/%d/%Y %H:%M:%S %p")  
					where_cond = "SRC.QUOTE_RECORD_ID = '{}' AND SRC.QTEREV_RECORD_ID = '{}' and SRC.SERVICE_ID = '{}' AND SRC.EQUIPMENT_ID = '{}'".format(ContractRecordId, revision_record_id,TreeParentParam,equipment_id)
					rolldown(where_cond)
		##update chmaber as included for SAQSSE,SAQSCO and assembly rolldown
		else:
			Sql.RunQuery("update SAQSSE set INCLUDED = 'CHAMBER' where SND_EQUIPMENT_ID ='{}' and QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' and SERVICE_ID = '{}' ".format(equipment_id,ContractRecordId, revision_record_id,TreeParentParam))
			Sql.RunQuery("update SAQSCO set INCLUDED = 'CHAMBER' where EQUIPMENT_ID ='{}' and QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' and SERVICE_ID = '{}' ".format(equipment_id,ContractRecordId, revision_record_id,TreeParentParam))
			if 'Z0007' in TreeParentParam:
				whereReq = "QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' and SERVICE_ID = '{}' AND EQUIPMENT_ID = '{}'".format(ContractRecordId, revision_record_id,TreeParentParam,equipment_id)
				add_where = "and INCLUDED = 'CHAMBER'"
				AttributeID = 'AGS_QUO_QUO_TYP'
				NewValue = 'Chamber based'
				update_flag = entitlement_update(whereReq,add_where,AttributeID,NewValue,TreeParentParam,'SAQSCE')
				if update_flag:
					##Assembly level roll down
					userId = User.Id
					datetimenow = datetime.now().strftime("%m/%d/%Y %H:%M:%S %p")  
					where_cond = "SRC.QUOTE_RECORD_ID = '{}' AND SRC.QTEREV_RECORD_ID = '{}' and SRC.SERVICE_ID = '{}' AND SRC.EQUIPMENT_ID = '{}'".format(ContractRecordId, revision_record_id,TreeParentParam,equipment_id)
					rolldown(where_cond)
					

	return True

def edit_assembly_level(Values):
	#TreeParentParam = Product.GetGlobal("TreeParentLevel0")
	# TreeSuperParentParam = Product.GetGlobal("TreeParentLevel1")
	# TreeTopSuperParentParam =  Product.GetGlobal("TreeParentLevel2")
	#ContractRecordId = Quote.GetGlobal("contract_quote_record_id")
	#Trace.Write('Values----'+str(Values))
	get_rec = Sql.GetList("select SND_ASSEMBLY_ID from SAQSSA (NOLOCK) where SND_EQUIPMENT_ID = '{}' and EQUIPMENTTYPE_ID = 'CHAMBER' and QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' and SERVICE_ID = '{}'".format(Values,ContractRecordId, revision_record_id,TreeParentParam))
	chamber_res_list = [i.SND_ASSEMBLY_ID for i in get_rec]
	#Trace.Write('bb--'+str(chamber_res_list))
	return chamber_res_list

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


def child_ent_request(tableName,where,serviceId):		
	response = Request_access_token()
	webclient = System.Net.WebClient()		
	Trace.Write(response["access_token"])
	#Log.Info(str(tableName)+'--serviceId---'+str(serviceId))
	ent_temp =''
	Request_URL="https://cpservices-product-configuration.cfapps.us10.hana.ondemand.com/api/v2/configurations?autoCleanup=False"
	webclient.Headers[System.Net.HttpRequestHeader.Authorization] = "Bearer " + str(response["access_token"])    
	gettodaydate = datetime.now().strftime("%Y-%m-%d")
	ProductPartnumber = serviceId#'Z0035'
	#Log.Info('inside----')
	try:        
		requestdata = '{"productKey":"'+ ProductPartnumber+ '","date":"'+gettodaydate+'","context":[{"name":"VBAP-MATNR","value":"'+ ProductPartnumber+ '"}]}'
		Trace.Write("requestdata" + str(requestdata))
		response1 = webclient.UploadString(Request_URL, str(requestdata))        
		response1 = str(response1).replace(": true", ': "true"').replace(": false", ': "false"')
		Fullresponse = eval(response1)
		Trace.Write("response.."+str(eval(response1)))
		newConfigurationid = Fullresponse["id"]
		Trace.Write("newConfigurationid.."+str(newConfigurationid))
		if tableName!="":
			get_c4c_quote_id = Sql.GetFirst("select * from SAQTMT where MASTER_TABLE_QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(ContractRecordId, revision_record_id))
			#Log.Info('-ContractRecordId-'+str(ContractRecordId))
			#Log.Info('-revision_record_id-'+str(revision_record_id))
			#Log.Info('-ent_temp-160---C4C_QUOTE_ID-'+str(get_c4c_quote_id.C4C_QUOTE_ID))
			ent_temp = "ENT_ASSEM_BKP_"+str(get_c4c_quote_id.C4C_QUOTE_ID)
			#Log.Info('-ent_temp-160----'+str(ent_temp))
			ent_temp_drop = Sql.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(ent_temp)+"'' ) BEGIN DROP TABLE "+str(ent_temp)+" END  ' ")
			#Log.Info('-ent_temp---'+str(ent_temp))
			where_cond = where.replace("'","''")
			#Sql.GetFirst("sp_executesql @T=N'declare @H int; Declare @val Varchar(MAX);DECLARE @XML XML; SELECT @val =  replace(replace(STUFF((SELECT ''''+FINAL from(select  REPLACE(entitlement_xml,''<QUOTE_ITEM_ENTITLEMENT>'',sml) AS FINAL FROM (select ''  <QUOTE_ITEM_ENTITLEMENT><QUOTE_ID>''+quote_id+''</QUOTE_ID><QUOTE_RECORD_ID>''+QUOTE_RECORD_ID+''</QUOTE_RECORD_ID><QTEREV_RECORD_ID>''+QTEREV_RECORD_ID+''</QTEREV_RECORD_ID><SERVICE_ID>''+service_id+''</SERVICE_ID>'' AS sml,replace(replace(replace(replace(entitlement_xml,''&'','';#38''),'''','';#39''),'' < '','' &lt; ''),'' > '','' &gt; '')  as entitlement_xml from "+str(tableName)+"(nolock) WHERE "+str(where_cond)+" )A )a FOR XML PATH ('''')), 1, 1, ''''),''&lt;'',''<''),''&gt;'',''>'')  SELECT @XML = CONVERT(XML,''<ROOT>''+@VAL+''</ROOT>'') exec sys.sp_xml_preparedocument @H output,@XML; select QUOTE_ID,QUOTE_RECORD_ID,QTEREV_RECORD_ID,SERVICE_ID,ENTITLEMENT_ID,ENTITLEMENT_NAME,ENTITLEMENT_COST_IMPACT,ENTITLEMENT_TYPE,ENTITLEMENT_VALUE_CODE,ENTITLEMENT_DISPLAY_VALUE,IS_DEFAULT INTO "+str(ent_temp)+"  from openxml(@H, ''ROOT/QUOTE_ITEM_ENTITLEMENT'', 0) with (QUOTE_ID VARCHAR(100) ''QUOTE_ID'',QUOTE_RECORD_ID VARCHAR(100) ''QUOTE_RECORD_ID'',QTEREV_RECORD_ID VARCHAR(100) ''QTEREV_RECORD_ID'',ENTITLEMENT_NAME VARCHAR(100) ''ENTITLEMENT_NAME'',ENTITLEMENT_ID VARCHAR(100) ''ENTITLEMENT_ID'',SERVICE_ID VARCHAR(100) ''SERVICE_ID'',ENTITLEMENT_COST_IMPACT VARCHAR(100) ''ENTITLEMENT_COST_IMPACT'',ENTITLEMENT_TYPE VARCHAR(100) ''ENTITLEMENT_TYPE'',ENTITLEMENT_VALUE_CODE VARCHAR(100) ''ENTITLEMENT_VALUE_CODE'',ENTITLEMENT_DISPLAY_VALUE VARCHAR(100) ''ENTITLEMENT_DISPLAY_VALUE'',IS_DEFAULT VARCHAR(100) ''IS_DEFAULT'') ; exec sys.sp_xml_removedocument @H; '")

			Sql.GetFirst("sp_executesql @T=N'declare @H int; Declare @val Varchar(MAX);DECLARE @XML XML; SELECT @val = FINAL from(select  REPLACE(entitlement_xml,''<QUOTE_ITEM_ENTITLEMENT>'',sml) AS FINAL FROM (select ''  <QUOTE_ITEM_ENTITLEMENT><QUOTE_ID>''+quote_id+''</QUOTE_ID><QUOTE_RECORD_ID>''+QUOTE_RECORD_ID+''</QUOTE_RECORD_ID><QTEREV_RECORD_ID>''+QTEREV_RECORD_ID+''</QTEREV_RECORD_ID><SERVICE_ID>''+service_id+''</SERVICE_ID>'' AS sml,replace(replace(replace(replace(replace(replace(replace(replace(ENTITLEMENT_XML,''&'','';#38''),'''','';#39''),'' < '','' &lt; '' ),'' > '','' &gt; '' ),''_>'',''_&gt;''),''_<'',''_&lt;''),''&'','';#38''),''<10%'',''&lt;10%'')   as entitlement_xml from "+str(tableName)+"(nolock)  WHERE "+str(where_cond)+"  )A )a SELECT @XML = CONVERT(XML,''<ROOT>''+@VAL+''</ROOT>'') exec sys.sp_xml_preparedocument @H output,@XML; select QUOTE_ID,QUOTE_RECORD_ID,QTEREV_RECORD_ID,SERVICE_ID,ENTITLEMENT_ID,ENTITLEMENT_NAME,ENTITLEMENT_COST_IMPACT,ENTITLEMENT_TYPE,ENTITLEMENT_VALUE_CODE,ENTITLEMENT_DISPLAY_VALUE,IS_DEFAULT INTO "+str(ent_temp)+"  from openxml(@H, ''ROOT/QUOTE_ITEM_ENTITLEMENT'', 0) with (QUOTE_ID VARCHAR(100) ''QUOTE_ID'',QUOTE_RECORD_ID VARCHAR(100) ''QUOTE_RECORD_ID'',QTEREV_RECORD_ID VARCHAR(100) ''QTEREV_RECORD_ID'',ENTITLEMENT_NAME VARCHAR(100) ''ENTITLEMENT_NAME'',ENTITLEMENT_ID VARCHAR(100) ''ENTITLEMENT_ID'',SERVICE_ID VARCHAR(100) ''SERVICE_ID'',ENTITLEMENT_COST_IMPACT VARCHAR(100) ''ENTITLEMENT_COST_IMPACT'',ENTITLEMENT_TYPE VARCHAR(100) ''ENTITLEMENT_TYPE'',ENTITLEMENT_VALUE_CODE VARCHAR(100) ''ENTITLEMENT_VALUE_CODE'',ENTITLEMENT_DISPLAY_VALUE VARCHAR(100) ''ENTITLEMENT_DISPLAY_VALUE'',IS_DEFAULT VARCHAR(100) ''IS_DEFAULT'') ; exec sys.sp_xml_removedocument @H; '")

			Parentgetdata=Sql.GetList("SELECT * FROM {} ".format(ent_temp))
			#Log.Info("where--167------- "+str(where))
			if Parentgetdata:					
				response = Request_access_token()					
				Request_URL = "https://cpservices-product-configuration.cfapps.us10.hana.ondemand.com/api/v2/configurations/"+str(newConfigurationid)+"/items/1"
				cpsmatchID=1
				
				for row in Parentgetdata:
					webclient = System.Net.WebClient()
						
					webclient.Headers[System.Net.HttpRequestHeader.Authorization] = "Bearer " + str(response["access_token"])
						
					webclient.Headers.Add("If-Match", '"'+str(cpsmatchID)+'"')	
						
					if row.ENTITLEMENT_VALUE_CODE and row.ENTITLEMENT_VALUE_CODE not in ('undefined','None') and   row.ENTITLEMENT_ID !='undefined' and row.ENTITLEMENT_DISPLAY_VALUE !='select' and row.IS_DEFAULT =='0':
						Trace.Write('row--'+str(row.ENTITLEMENT_ID))
						try:
							requestdata = '{"characteristics":['
							
							requestdata +='{"id":"'+ str(row.ENTITLEMENT_ID) + '","values":[' 
							if row.ENTITLEMENT_TYPE in ('Check Box','CheckBox'):
								Trace.Write("auto update---"+str(row.ENTITLEMENT_VALUE_CODE)+'---'+str( row.ENTITLEMENT_ID))
								#Log.Info('ENTITLEMENT_VALUE_CODE----'+str(row.ENTITLEMENT_VALUE_CODE)+'---'+str(eval(row.ENTITLEMENT_VALUE_CODE)))
								for code in row.ENTITLEMENT_VALUE_CODE.split(','):
									requestdata += '{"value":"' + str(code) + '","selected":true}'
									requestdata +=','
								requestdata +=']},'	
								#Trace.Write("auto update---"+str(requestdata))
							else:
								requestdata+= '{"value":"' +str(row.ENTITLEMENT_VALUE_CODE) + '","selected":true}]},'
							requestdata += ']}'
							requestdata = requestdata.replace('},]','}]')
							Trace.Write("requestdata--child-- " + str(requestdata))
							response1 = webclient.UploadString(Request_URL, "PATCH", str(requestdata))
							#cpsmatchID = cpsmatchID + 1			
							cpsmatchID = webclient.ResponseHeaders["Etag"]
							cpsmatchID = re.sub('"',"",cpsmatchID)
						except Exception:
							Trace.Write("Patch Error-1-"+str(sys.exc_info()[1]))
							cpsmatchID = cpsmatchID

		getdata=Sql.GetList("SELECT * FROM {} WHERE {}".format(tableName,where))
		#cpsmatc_incr = cpsmatchID + 1
		for data in getdata:
			updateConfiguration = Sql.RunQuery("UPDATE {} SET CPS_CONFIGURATION_ID = '{}',CPS_MATCH_ID={} WHERE {} ".format(tableName,newConfigurationid,cpsmatchID,where))            
	except Exception:
		Log.Info("Patch Error-2-"+str(sys.exc_info()[1]))        
	ent_temp_drop = Sql.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(ent_temp)+"'' ) BEGIN DROP TABLE "+str(ent_temp)+" END  ' ")
	return newConfigurationid,cpsmatchID



def entitlement_update(whereReq=None,add_where=None,AttributeID=None,NewValue=None,service_id=None,table_name=None):
	#whereReq = "QUOTE_RECORD_ID = '{}' and SERVICE_ID = '{}' AND EQUIPMENT_ID = '{}'".format('50243B0C-C53B-4BE5-8923-939BB9DCEB73','Z0007','100000181')
	#add_where = "and INCLUDED = 'CHAMBER'""
	#AttributeID = 'AGS_QUO_QUO_TYP'
	#NewValue = 'Chamber based'
	get_equp_xml = Sql.GetFirst("select distinct CPS_MATCH_ID,ENTITLEMENT_XML,CPS_CONFIGURATION_ID FROM {} where {}".format(table_name,whereReq))
	#get_query = Sql.GetFirst("select EQUIPMENT_ID FROM SAQSCO where {} {}".format(whereReq,add_where))
	if get_equp_xml and NewValue.upper() not in ('SELECT','UNDEFINED'):
		Trace.Write('inside----')
		cpsConfigID,cpsmatchID = child_ent_request(table_name,whereReq,service_id)
		# cpsmatchID = get_equp_xml.CPS_MATCH_ID
		# cpsConfigID = get_equp_xml.CPS_CONFIGURATION_ID
		#try:       
		Trace.Write(str(AttributeID)+"----NewValue-----"+str(NewValue)+"---requestdata--244-cpsConfigID0-----"+str(cpsmatchID)+'--'+str(cpsConfigID))
		# webclient = System.Net.WebClient()
		# webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/json"
		# webclient.Headers[System.Net.HttpRequestHeader.Authorization] = "Basic c2ItYzQwYThiMWYtYzU5NS00ZWJjLTkyYzYtYzM4ODg4ODFmMTY0IWIyNTAzfGNwc2VydmljZXMtc2VjdXJlZCFiMzkxOm9zRzgvSC9hOGtkcHVHNzl1L2JVYTJ0V0FiMD0="
		# response = webclient.DownloadString("https://cpqprojdevamat.authentication.us10.hana.ondemand.com:443/oauth/token?grant_type=client_credentials")
		response = Request_access_token()
		#response = eval(response)
		webclient = System.Net.WebClient()		
		Request_URL = "https://cpservices-product-configuration.cfapps.us10.hana.ondemand.com/api/v2/configurations/"+str(cpsConfigID)+"/items/1"
		webclient.Headers[System.Net.HttpRequestHeader.Authorization] = "Bearer " + str(response["access_token"])

		webclient.Headers.Add("If-Match", '"'+str(cpsmatchID)+'"')
				
		#AttributeID = 'AGS_QUO_QUO_TYP'
		#NewValue = 'Chamber based'
		product_obj = Sql.GetFirst("""SELECT 
								MAX(PDS.PRODUCT_ID) AS PRD_ID,PDS.SYSTEM_ID,PDS.PRODUCT_NAME 
							FROM PRODUCTS PDS 
							INNER JOIN PRODUCT_VERSIONS PRVS ON  PDS.PRODUCT_ID = PRVS.PRODUCT_ID 
							WHERE SYSTEM_ID ='{SystemId}' 
							GROUP BY PDS.SYSTEM_ID,PDS.UnitOfMeasure,PDS.CART_DESCRIPTION_BUILDER,PDS.PRODUCT_NAME""".format(SystemId = str(service_id)))
		get_datatype = Sql.GetFirst("""SELECT ATT_DISPLAY_DEFN.ATT_DISPLAY_DESC AS ATT_DISPLAY_DESC,PRODUCT_ATTRIBUTES.ATTRDESC
												FROM TAB_PRODUCTS
												LEFT JOIN PAT_SCHEMA ON PAT_SCHEMA.TAB_PROD_ID=TAB_PRODUCTS.TAB_PROD_ID											
												LEFT JOIN PRODUCT_ATTRIBUTES ON PRODUCT_ATTRIBUTES.STANDARD_ATTRIBUTE_CODE = PAT_SCHEMA.STANDARD_ATTRIBUTE_CODE AND PRODUCT_ATTRIBUTES.PRODUCT_ID = TAB_PRODUCTS.PRODUCT_ID
												LEFT JOIN ATTRIBUTE_DEFN ON ATTRIBUTE_DEFN.STANDARD_ATTRIBUTE_CODE = PRODUCT_ATTRIBUTES.STANDARD_ATTRIBUTE_CODE
												LEFT JOIN ATT_DISPLAY_DEFN ON ATT_DISPLAY_DEFN.ATT_DISPLAY = PRODUCT_ATTRIBUTES.ATT_DISPLAY
												
												WHERE TAB_PRODUCTS.PRODUCT_ID = {ProductId} AND SYSTEM_ID = '{service_id}'""".format(ProductId = product_obj.PRD_ID,service_id = AttributeID ))
		field_type = ""
		checkbox_dict =""
		if get_datatype:
			if get_datatype.ATT_DISPLAY_DESC:
				field_type = get_datatype.ATT_DISPLAY_DESC
		requestdata = '{"characteristics":[{"id":"' + AttributeID + '","values":['
		if field_type not in ('input','Free Input, no Matching'):
			STANDARD_ATTRIBUTE_VALUES=Sql.GetList("SELECT V.STANDARD_ATTRIBUTE_DISPLAY_VAL, V.STANDARD_ATTRIBUTE_VALUE FROM PRODUCT_ATTRIBUTES PA INNER JOIN ATTRIBUTES A ON PA.PA_ID=A.PA_ID INNER JOIN STANDARD_ATTRIBUTE_VALUES V ON A.STANDARD_ATTRIBUTE_VALUE_CD = V.STANDARD_ATTRIBUTE_VALUE_CD INNER JOIN ATTRIBUTE_DEFN (NOLOCK) AD ON AD.STANDARD_ATTRIBUTE_CODE=V.STANDARD_ATTRIBUTE_CODE WHERE AD.SYSTEM_ID = '{}' AND PA.PRODUCT_ID ={} ".format(AttributeID,product_obj.PRD_ID))
			if STANDARD_ATTRIBUTE_VALUES:
				if field_type == 'Check Box':
					checkbox_dict = NewValue.split(',')
				for val in STANDARD_ATTRIBUTE_VALUES:
					#if str(val.STANDARD_ATTRIBUTE_DISPLAY_VAL).upper() == str(NewValue).upper():
					if (field_type == 'Check Box' and val.STANDARD_ATTRIBUTE_DISPLAY_VAL in checkbox_dict) or (val.STANDARD_ATTRIBUTE_DISPLAY_VAL.upper() == str(NewValue).upper()):
						#if field_type == 'Check Box' and checkbox_dict:
						requestdata += '{"value":"' + val.STANDARD_ATTRIBUTE_VALUE + '","selected":true}'
						requestdata +=','
						
						#NewValue = str(val.STANDARD_ATTRIBUTE_VALUE)
						Trace.Write('NewValue-iff--254----'+str(NewValue))
					elif field_type == 'Check Box':
						Trace.Write("inside_J____checkbox")
						requestdata += '{"value":"' + val.STANDARD_ATTRIBUTE_VALUE + '","selected":false}'
						requestdata +=','
					

					# else:
					# 	Trace.Write('NewValue--'+str(NewValue))
					# 	#requestdata = '{"characteristics":[{"id":"' + AttributeID + '","values":['
					# 	#requestdata += '{"value":"' + NewValue + '","selected":true}'
					# 	requestdata += '{"value":"' + val.STANDARD_ATTRIBUTE_VALUE + '","selected":true}'
			else:
				if AttributeID == "AGS_Z0046_KPI_BPTKPI":
					NewValue ='002'
					Trace.Write('NewValue--'+str(NewValue))
					#requestdata = '{"characteristics":[{"id":"' + AttributeID + '","values":['
					#requestdata += '{"value":"' + NewValue + '","selected":true}'
					requestdata += '{"value":"' + NewValue + '","selected":true}'
		else:
			Trace.Write("elseee----field type--"+str(AttributeID))
			requestdata += '{"value":"' + NewValue + '","selected":true}'
		
		requestdata += ']}]}'
		requestdata = requestdata.replace(',]}]}',']}]}')
		Trace.Write("requestdata----"+str(requestdata))
		response2 = webclient.UploadString(Request_URL, "PATCH", str(requestdata))
		cpsmatc_incr = webclient.ResponseHeaders["Etag"]
		cpsmatc_incr = re.sub('"',"",cpsmatc_incr)
		Request_URL = "https://cpservices-product-configuration.cfapps.us10.hana.ondemand.com/api/v2/configurations/"+str(cpsConfigID)
		webclient.Headers[System.Net.HttpRequestHeader.Authorization] = "Bearer " + str(response["access_token"])
		#Log.Info("requestdata---180--265----" + str(requestdata))
		response2 = webclient.DownloadString(Request_URL)
		#Log.Info('response2--182----267-----'+str(response2))
		response2 = str(response2).replace(": true", ': "true"').replace(": false", ': "false"')
		Fullresponse= eval(response2)
		##getting configuration_status status
		if Fullresponse['complete'] == 'true':
			configuration_status = 'COMPLETE'
		elif Fullresponse['complete'] == 'false':
			configuration_status = 'INCOMPLETE'
		else:
			configuration_status = 'ERROR'
		Trace.Write('configuration_status---'+str(configuration_status))
		attributesdisallowedlst=[]
		attributesallowedlst=[]
		attributedefaultvalue = []
		multi_value = get_tooltip_desc = ""
		overallattributeslist =[]
		attributevalues={}
		for rootattribute, rootvalue in Fullresponse.items():
			if rootattribute=="rootItem":
				for Productattribute, Productvalue in rootvalue.items():
					if Productattribute=="characteristics":
						for prdvalue in Productvalue:
							multi_value = ""
							overallattributeslist.append(prdvalue['id'])
							if prdvalue['visible'] =='false':
								attributesdisallowedlst.append(prdvalue['id'])
							else:
								#Trace.Write(prdvalue['id']+" set here")
								attributesallowedlst.append(prdvalue['id'])
							
							if len(prdvalue["values"]) == 1:
								#Trace.Write('ifffff'+str(prdvalue["id"]))
								attributevalues[str(prdvalue["id"])] = prdvalue['values'][0]['value']
								if prdvalue["values"][0]["author"] in ("Default","System"):
									#Trace.Write('524------'+str(prdvalue["id"]))
									attributedefaultvalue.append(prdvalue["id"])
							elif len(prdvalue["values"]) > 1:
								#Trace.Write('else if'+str(prdvalue["id"])+'--'+str(prdvalue["values"]))
								for attribute in prdvalue["values"]:
									#Trace.Write('iiiii---'+str(attribute)+'-'+str(prdvalue["id"]) )
									value_list = [attribute["value"] for attribute in prdvalue["values"]]
									if attribute["author"] in ("Default","System"):
										attributedefaultvalue.append(prdvalue["id"])
									#value_list = str(value_list)
								attributevalues[str(prdvalue["id"])] = value_list
								#Trace.Write('else if--chkbox--'+str(prdvalue["id"])+'--'+str(attributevalues[str(prdvalue["id"])]))
							# else:
							#     Trace.Write('else'+str(prdvalue["id"]))

		
		attributesallowedlst = list(set(attributesallowedlst))
		overallattributeslist = list(set(overallattributeslist))
		HasDefaultvalue=False
		#Log.Info('response2--182----315---'+str(attributesallowedlst))
		Trace.Write(str(overallattributeslist)+'--attributevalues--182----315---'+str(attributevalues))
		ProductVersionObj=Sql.GetFirst("Select product_id from product_versions(nolock) where SAPKBId = '"+str(Fullresponse['kbId'])+"' AND SAPKBVersion='"+str(Fullresponse['kbKey']['version'])+"'")
		if ProductVersionObj is not None:
			insertservice = ""
			for attrs in overallattributeslist:
				if attrs in attributevalues:
					HasDefaultvalue=True
					STANDARD_ATTRIBUTE_VALUES=Sql.GetFirst("SELECT S.STANDARD_ATTRIBUTE_DISPLAY_VAL,S.STANDARD_ATTRIBUTE_CODE FROM STANDARD_ATTRIBUTE_VALUES (nolock) S INNER JOIN ATTRIBUTE_DEFN (NOLOCK) A ON A.STANDARD_ATTRIBUTE_CODE=S.STANDARD_ATTRIBUTE_CODE WHERE A.SYSTEM_ID = '{}'".format(attrs,attributevalues[attrs]))
					ent_disp_val = attributevalues[attrs]
					ent_val_code = attributevalues[attrs]
				else:
					HasDefaultvalue=False
					ent_disp_val = ""
					ent_val_code = ""
					STANDARD_ATTRIBUTE_VALUES=Sql.GetFirst("SELECT S.STANDARD_ATTRIBUTE_CODE FROM STANDARD_ATTRIBUTE_VALUES (nolock) S INNER JOIN ATTRIBUTE_DEFN (NOLOCK) A ON A.STANDARD_ATTRIBUTE_CODE=S.STANDARD_ATTRIBUTE_CODE WHERE A.SYSTEM_ID = '{}'".format(attrs))
				ATTRIBUTE_DEFN=Sql.GetFirst("SELECT * FROM ATTRIBUTE_DEFN (NOLOCK) WHERE SYSTEM_ID='{}'".format(attrs))
				
				PRODUCT_ATTRIBUTES=Sql.GetFirst("SELECT A.ATT_DISPLAY_DESC,P.ATTRDESC FROM ATT_DISPLAY_DEFN (NOLOCK) A INNER JOIN PRODUCT_ATTRIBUTES (NOLOCK) P ON A.ATT_DISPLAY=P.ATT_DISPLAY WHERE P.PRODUCT_ID={} AND P.STANDARD_ATTRIBUTE_CODE={}".format(ProductVersionObj.product_id,STANDARD_ATTRIBUTE_VALUES.STANDARD_ATTRIBUTE_CODE))
				if PRODUCT_ATTRIBUTES:
					if PRODUCT_ATTRIBUTES.ATTRDESC:
						get_tooltip_desc = PRODUCT_ATTRIBUTES.ATTRDESC
					else:
						get_tooltip_desc = ''
				if PRODUCT_ATTRIBUTES.ATT_DISPLAY_DESC in ('Drop Down','DropDown') and ent_disp_val:
					Trace.Write('ent_val_code--348--'+str(attrs)+'--ent_disp_val---'+str(ent_disp_val))
					get_display_val = Sql.GetFirst("SELECT STANDARD_ATTRIBUTE_DISPLAY_VAL  from STANDARD_ATTRIBUTE_VALUES S INNER JOIN ATTRIBUTE_DEFN (NOLOCK) A ON A.STANDARD_ATTRIBUTE_CODE=S.STANDARD_ATTRIBUTE_CODE WHERE S.STANDARD_ATTRIBUTE_CODE = '{}' AND A.SYSTEM_ID = '{}' AND S.STANDARD_ATTRIBUTE_VALUE = '{}' ".format(STANDARD_ATTRIBUTE_VALUES.STANDARD_ATTRIBUTE_CODE,attrs,  attributevalues[attrs] ) )
					if get_display_val:
						ent_disp_val = get_display_val.STANDARD_ATTRIBUTE_DISPLAY_VAL 
				elif PRODUCT_ATTRIBUTES.ATT_DISPLAY_DESC in ('Check Box') and ent_disp_val and ent_val_code:
					#Trace.Write('ent_val_code--'+str(type(ent_val_code))+'---'+str(ent_val_code))
					if type(eval(str(ent_val_code))) is list:
						ent_val = str(tuple(ent_val_code)).replace(',)',')')
						get_display_val = Sql.GetList("SELECT STANDARD_ATTRIBUTE_DISPLAY_VAL  from STANDARD_ATTRIBUTE_VALUES S INNER JOIN ATTRIBUTE_DEFN (NOLOCK) A ON A.STANDARD_ATTRIBUTE_CODE=S.STANDARD_ATTRIBUTE_CODE WHERE S.STANDARD_ATTRIBUTE_CODE = '{}' AND A.SYSTEM_ID = '{}' AND S.STANDARD_ATTRIBUTE_VALUE in {} ".format(STANDARD_ATTRIBUTE_VALUES.STANDARD_ATTRIBUTE_CODE,attrs,  ent_val ) )
						if get_display_val:
							ent_disp_val = [i.STANDARD_ATTRIBUTE_DISPLAY_VAL for i in get_display_val if i.STANDARD_ATTRIBUTE_DISPLAY_VAL]
							#ent_disp_val = str(ent_disp_val).replace("'", '"')
							#ent_val_code = str(ent_val_code).replace("'", '"')
							ent_disp_val = ','.join(ent_disp_val)
							ent_val_code = ','.join(ent_val_code)
						else:
							ent_disp_val = ent_val_code =''
						#Trace.Write('ent_val_code--'+str(type(ent_val_code))+'---'+str(ent_val_code))
					
					else:
						get_display_val = Sql.GetFirst("SELECT STANDARD_ATTRIBUTE_DISPLAY_VAL  from STANDARD_ATTRIBUTE_VALUES S INNER JOIN ATTRIBUTE_DEFN (NOLOCK) A ON A.STANDARD_ATTRIBUTE_CODE=S.STANDARD_ATTRIBUTE_CODE WHERE S.STANDARD_ATTRIBUTE_CODE = '{}' AND A.SYSTEM_ID = '{}' AND S.STANDARD_ATTRIBUTE_VALUE = '{}' ".format(STANDARD_ATTRIBUTE_VALUES.STANDARD_ATTRIBUTE_CODE,attrs,  attributevalues[attrs] ) )
						if get_display_val:
							ent_disp_val = str(str(get_display_val.STANDARD_ATTRIBUTE_DISPLAY_VAL).split("'") ).replace("'", '"')
							ent_val_code = str(str(ent_val_code).split(',') ).replace("'", '"')
				else:
					Trace.Write(str(AttributeID)+'---369--attrs---'+str(attrs))
					Trace.Write('369-NewValue-370----'+str(attrs)+'-----'+str(NewValue)+str(ent_val_code))
					if attrs == AttributeID:
						Trace.Write(str(NewValue)+'---372--'+str(attrs)+'372---ent_val_code----'+str(ent_val_code))
						ent_disp_val = NewValue
						ent_val_code = NewValue
				if attrs == "AGS_Z0016_NET_PRICNG":
					if type(eval(str(ent_val_code))) is list:
						ent_val = str(tuple(ent_val_code)).replace(',)',')')
						get_display_val = Sql.GetList("SELECT STANDARD_ATTRIBUTE_DISPLAY_VAL  from STANDARD_ATTRIBUTE_VALUES S INNER JOIN ATTRIBUTE_DEFN (NOLOCK) A ON A.STANDARD_ATTRIBUTE_CODE=S.STANDARD_ATTRIBUTE_CODE WHERE S.STANDARD_ATTRIBUTE_CODE = '{}' AND A.SYSTEM_ID = '{}' AND S.STANDARD_ATTRIBUTE_VALUE in {} ".format(STANDARD_ATTRIBUTE_VALUES.STANDARD_ATTRIBUTE_CODE,attrs,  ent_val ) )
						if get_display_val:
							ent_disp_val = [i.STANDARD_ATTRIBUTE_DISPLAY_VAL for i in get_display_val if i.STANDARD_ATTRIBUTE_DISPLAY_VAL]
							ent_disp_val = str(ent_disp_val).replace("'", '"')
							ent_val_code = str(ent_val_code).replace("'", '"')
						else:
							ent_disp_val = ent_val_code =''
					else:
						get_display_val = Sql.GetFirst("SELECT STANDARD_ATTRIBUTE_DISPLAY_VAL  from STANDARD_ATTRIBUTE_VALUES S INNER JOIN ATTRIBUTE_DEFN (NOLOCK) A ON A.STANDARD_ATTRIBUTE_CODE=S.STANDARD_ATTRIBUTE_CODE WHERE S.STANDARD_ATTRIBUTE_CODE = '{}' AND A.SYSTEM_ID = '{}' AND S.STANDARD_ATTRIBUTE_VALUE = '{}' ".format(STANDARD_ATTRIBUTE_VALUES.STANDARD_ATTRIBUTE_CODE,attrs,  attributevalues[attrs] ) )
						if get_display_val:
							ent_disp_val = str(str(get_display_val.STANDARD_ATTRIBUTE_DISPLAY_VAL).split("'") ).replace("'", '"')
							ent_val_code = str(str(ent_val_code).split(',') ).replace("'", '"')
				DTypeset={"Drop Down":"DropDown","Free Input, no Matching":"FreeInputNoMatching","Check Box":"Check Box"}
				#Log.Info('response2--182----342-')
				Trace.Write('--ent_disp_val--value code-'+str(attrs)+'--'+str(ent_val_code)+'--'+str(ent_disp_val))
				
				insertservice += """<QUOTE_ITEM_ENTITLEMENT>
				<ENTITLEMENT_ID>{ent_name}</ENTITLEMENT_ID>
				<ENTITLEMENT_VALUE_CODE>{ent_val_code}</ENTITLEMENT_VALUE_CODE>
				<ENTITLEMENT_DESCRIPTION>{tool_desc}</ENTITLEMENT_DESCRIPTION>
				<ENTITLEMENT_TYPE>{ent_type}</ENTITLEMENT_TYPE>                    
				<ENTITLEMENT_DISPLAY_VALUE>{ent_disp_val}</ENTITLEMENT_DISPLAY_VALUE>
				<ENTITLEMENT_COST_IMPACT>{ct}</ENTITLEMENT_COST_IMPACT>
				<ENTITLEMENT_PRICE_IMPACT>{pi}</ENTITLEMENT_PRICE_IMPACT>
				<IS_DEFAULT>{is_default}</IS_DEFAULT>
				<PRICE_METHOD>{pm}</PRICE_METHOD>
				<CALCULATION_FACTOR>{cf}</CALCULATION_FACTOR>
				<ENTITLEMENT_NAME>{ent_desc}</ENTITLEMENT_NAME>
				</QUOTE_ITEM_ENTITLEMENT>""".format(ent_name = str(attrs),ent_val_code = ent_val_code,ent_type = DTypeset[PRODUCT_ATTRIBUTES.ATT_DISPLAY_DESC] if PRODUCT_ATTRIBUTES else  '',ent_desc = ATTRIBUTE_DEFN.STANDARD_ATTRIBUTE_NAME,ent_disp_val = ent_disp_val if HasDefaultvalue==True else '',ct = '',pi = '',is_default = 1 if str(attrs) in attributedefaultvalue else '0',pm = '',cf = '',tool_desc =get_tooltip_desc.replace("'","''") if "'" in get_tooltip_desc else get_tooltip_desc)
				insertservice = insertservice.encode('ascii', 'ignore').decode('ascii')
				#cpsmatc_incr = int(cpsmatchID) + 1
				#Trace.Write('cpsmatc_incr'+str(cpsmatc_incr))
			Updatecps = "UPDATE {} SET CPS_MATCH_ID ={},CPS_CONFIGURATION_ID = '{}',ENTITLEMENT_XML='{}',CpqTableEntryModifiedBy = {}, CpqTableEntryDateModified = GETDATE(),CONFIGURATION_STATUS = '{}' WHERE {} ".format(table_name, cpsmatc_incr,cpsConfigID,insertservice,User.Id,configuration_status,whereReq)
			Trace.Write(str(whereReq)+'---Updatecps---'+str(Updatecps))
			Sql.RunQuery(Updatecps)
		
		return True
		#except Exception as e:
			#Trace.Write("except---"+str(e))

def rolldown(where_cond):
	userId = User.Id
	datetimenow = datetime.now().strftime("%m/%d/%Y %H:%M:%S %p") 
	update_query = """ UPDATE TGT 
		SET TGT.ENTITLEMENT_XML = SRC.ENTITLEMENT_XML,
		TGT.CPS_MATCH_ID = SRC.CPS_MATCH_ID,
		TGT.CPS_CONFIGURATION_ID = SRC.CPS_CONFIGURATION_ID,
		TGT.CpqTableEntryModifiedBy = {},
		TGT.CpqTableEntryDateModified = '{}'
		FROM SAQSCE (NOLOCK) SRC JOIN SAQSAE (NOLOCK) TGT 
		ON  TGT.QUOTE_RECORD_ID = SRC.QUOTE_RECORD_ID AND TGT.QTEREV_RECORD_ID = SRC.QTEREV_RECORD_ID AND TGT.SERVICE_ID = SRC.SERVICE_ID AND SRC.EQUIPMENT_ID = TGT.EQUIPMENT_ID WHERE {} """.format(userId,datetimenow,where_cond)
	Sql.RunQuery(update_query)


TreeParentParam = Product.GetGlobal("TreeParentLevel0")
try:
	ent_params_list = Param.ent_params_list.split('||')
	Trace.Write('ent_params_list-----'+str(ent_params_list))
except:

	ent_params_list = []
try:
	ContractRecordId = Quote.GetGlobal("contract_quote_record_id")
except:
	Contract_RecordId = ent_params_list[0].split('and')[0].split('=')
	ContractRecordId = Contract_RecordId[1].replace("'", "").strip()
try:
	revision_record_id = Quote.GetGlobal("quote_revision_record_id")
except:
	revisionrecord_id = ent_params_list[0].split('and')[1].split('=')
	revision_record_id = revisionrecord_id[2].replace("'", "").strip()
Trace.Write("check script called")
try:
	ACTION = Param.ACTION
	Trace.Write("check script called"+str(ACTION))
except:
	ACTION = ""

try:
	TABNAME = Param.TABNAME
except:
	TABNAME = ""

try:
	selected_values= eval(Param.Values)
	#Trace.Write('selected_values-----'+str(selected_values))
except:
	selected_values =[]
try:
	unselected_values= eval(Param.unselected_list)
	#Trace.Write('unselected_list-----'+str(unselected_values))
except Exception as e:
	#Trace.Write('unselected_values--error-'+str(e))
	unselected_values =[]

if ACTION == 'UPDATE_ASSEMBLY':
	#selected_values = list(selected_values)
	#Trace.Write('values----'+str(selected_values))
	ApiResponse = ApiResponseFactory.JsonResponse(update_assembly_level(selected_values))
elif ACTION == 'EDIT_ASSEMBLY':
	#Trace.Write('values----'+str(selected_values))
	ApiResponse = ApiResponseFactory.JsonResponse(edit_assembly_level(selected_values))

elif ACTION == 'UPDATE_ENTITLEMENT' and ent_params_list and len(ent_params_list) == 6:
	Trace.Write('inside update')
	#Log.Info('ent_params_lis----------'+str(ent_params_list))
	ent_where = ent_params_list[0]
	#Log.Info('ent_params_lis------ent_where----'+str(ent_where))
	ent_add_where = ent_params_list[1]
	ent_attr_id = ent_params_list[2]
	ent_newval = ent_params_list[3]
	ent_serviceid = ent_params_list[4]
	table_name = ent_params_list[5]
	ApiResponse = entitlement_update(ent_where, ent_add_where, ent_attr_id, ent_newval,ent_serviceid,table_name )

elif ACTION == 'ENT_ROLLDOWN' and ent_params_list and len(ent_params_list) == 1:
	ent_where = ent_params_list[0]  
	ApiResponse =rolldown(ent_where )




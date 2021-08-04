# =========================================================================================================================================
#   __script_name : CQENTLMENT.PY
#   __script_description :
#   __primary_author__ :
#   __create_date : 21/10/2020
#   � BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
#Deployment Test
import Webcom.Configurator.Scripting.Test.TestProduct
Trace = Trace  # pylint: disable=E0602
Webcom = Webcom  # pylint: disable=E0602
Product = Product  # pylint: disable=E0602
Param = Param  # pylint: disable=E0602
ScriptExecutor = ScriptExecutor  # pylint: disable=E0602
ApiResponseFactory = ApiResponseFactory  # pylint: disable=E0602
import clr

clr.AddReference("Webcom.Configurator")
import System.Net
import sys
from SYDATABASE import SQL
import datetime
import CQENTIFLOW
userId = str(User.Id)
userName = str(User.UserName)
Sql = SQL()
import time
gettodaydate = datetime.datetime.now().strftime("%Y-%m-%d")
class Entitlements:
	def __init__(self):
		self.treeparam = Product.GetGlobal("TreeParam")
		self.treeparentparam = Product.GetGlobal("TreeParentLevel0")
		self.treesuperparentparam = Product.GetGlobal("TreeParentLevel1")
		self.treetopsuperparentparam = Product.GetGlobal("TreeParentLevel2")
		self.treesupertopparentparam = Product.GetGlobal("TreeParentLevel3")
		##TreeParentLevel4 added for addon product
		self.treetopsupertopparentparam = Product.GetGlobal("TreeParentLevel4")
		self.ContractRecordId = Quote.GetGlobal("contract_quote_record_id")
		#Trace.Write("treesuperparentparam--25--"+str(self.treesuperparentparam)+"treetopsuperparentparam-"+ str(self.treetopsuperparentparam)+"treetopsupertopparentparam-- "+ str(self.treetopsupertopparentparam)+"--" + str(self.treesupertopparentparam))
		self.attr_code_mapping = {"L3_SLB_S1":"AGS_LAB_OPT1", "L3_SLB_S2":"AGS_LAB_OPT2", "L3_SLA_CWW":"AGS_LAB_OPT3", "L3_SLB_CWW":"AGS_LAB_OPT4", "SER_COO_S1":"AGS_LAB_OPT5", "RAM_SPE_S1":"AGS_LAB_OPT6", "ENG_IN_CHA_S1":"AGS_LAB_OPT7", "APP_ENG_S1":"AGS_LAB_OPT8", "3MON_SLA_CWW":"AGS_LAB_OPT9", "3MON_SLB_CWW":"AGS_LAB_OPT10", "3MON_EIC_RS_S1":"AGS_LAB_OPT11", "6MON_SLA_CWW":"AGS_LAB_OPT12", "6MON_SLB_CWW":"AGS_LAB_OPT13", "6MON_EIC_RS_S1":"AGS_LAB_OPT14"}

	def getcpsID(self,tableName,serviceId,parentObj,whereReq,attId,ParentwhereReq):
		cpsConfiguration = Sql.GetFirst("select CPS_CONFIGURATION_ID,MAX(CPS_MATCH_ID) as CPS_MATCH_ID from {} (NOLOCK) WHERE {} GROUP BY CPS_CONFIGURATION_ID ".format(tableName, whereReq))
		try:
			new_configid_flag = Param.new_configid_flag
		except:
			new_configid_flag = ""	
		cpsmatchID = ''
		cpsConfigID = ''
		oldConfigID =''
		if cpsConfiguration is not None:
			cpsmatchID = cpsConfiguration.CPS_MATCH_ID
			cpsConfigID = cpsConfiguration.CPS_CONFIGURATION_ID
			oldConfigID = cpsConfiguration.CPS_CONFIGURATION_ID
			if parentObj !='':
				parentcpsConfig = Sql.GetFirst("select CPS_CONFIGURATION_ID,MAX(CPS_MATCH_ID) as CPS_MATCH_ID from {} (NOLOCK) WHERE  QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}' GROUP BY CPS_CONFIGURATION_ID ".format(parentObj,self.ContractRecordId, serviceId))
				# if cpsConfigID == parentcpsConfig.CPS_CONFIGURATION_ID and tableName != 'SAQTSE':					
				# 	cpsConfigID,cpsmatchID = self.ChildEntRequest(cpsmatchID,tableName,whereReq,serviceId,parentObj,ParentwhereReq)
			if new_configid_flag == 'true':
				cpsConfigID,cpsmatchID = self.ChildEntRequest(cpsmatchID,tableName,whereReq,serviceId,parentObj,ParentwhereReq)	
		return cpsmatchID,cpsConfigID,oldConfigID
	def Request_access_token(self):
		webclient = System.Net.WebClient()
		webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/json"
		webclient.Headers[
			System.Net.HttpRequestHeader.Authorization
		] = "Basic c2ItYzQwYThiMWYtYzU5NS00ZWJjLTkyYzYtYzM4ODg4ODFmMTY0IWIyNTAzfGNwc2VydmljZXMtc2VjdXJlZCFiMzkxOm9zRzgvSC9hOGtkcHVHNzl1L2JVYTJ0V0FiMD0="
		response = webclient.DownloadString(
			"https://cpqprojdevamat.authentication.us10.hana.ondemand.com:443/oauth/token?grant_type=client_credentials"
		)
		return eval(response)

	def ChildEntRequest(self,cpsmatchID,tableName,where,serviceId,parentObj,ParentwhereReq):		
		response = self.Request_access_token()
		webclient = System.Net.WebClient()		
		Trace.Write(response["access_token"])
		Request_URL="https://cpservices-product-configuration.cfapps.us10.hana.ondemand.com/api/v2/configurations?autoCleanup=False"
		webclient.Headers[System.Net.HttpRequestHeader.Authorization] = "Bearer " + str(response["access_token"])    
		#webclient.Headers.Add("If-Match", "1"+str(cpsmatchID))
		Trace.Write(str(cpsmatchID)+"Request_URL--"+Request_URL)
		ProductPartnumber = serviceId#'Z0035'
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
				get_c4c_quote_id = Sql.GetFirst("select * from SAQTMT where MASTER_TABLE_QUOTE_RECORD_ID = '{}'".format(self.ContractRecordId))
				ent_temp = "ENT_SAVE_BKP_"+str(get_c4c_quote_id.C4C_QUOTE_ID)
				ent_temp_drop = Sql.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(ent_temp)+"'' ) BEGIN DROP TABLE "+str(ent_temp)+" END  ' ")
				where_cond = where.replace("'","''")
				Sql.GetFirst("sp_executesql @T=N'declare @H int; Declare @val Varchar(MAX);DECLARE @XML XML; SELECT @val =  replace(replace(STUFF((SELECT ''''+FINAL from(select  REPLACE(entitlement_xml,''<QUOTE_ITEM_ENTITLEMENT>'',sml) AS FINAL FROM (select ''  <QUOTE_ITEM_ENTITLEMENT><QUOTE_ID>''+quote_id+''</QUOTE_ID><QUOTE_RECORD_ID>''+QUOTE_RECORD_ID+''</QUOTE_RECORD_ID><SERVICE_ID>''+service_id+''</SERVICE_ID>'' AS sml,replace(entitlement_xml,''&'','';#38'')  as entitlement_xml from "+str(tableName)+"(nolock) WHERE "+str(where_cond)+" )A )a FOR XML PATH ('''')), 1, 1, ''''),''&lt;'',''<''),''&gt;'',''>'')  SELECT @XML = CONVERT(XML,''<ROOT>''+@VAL+''</ROOT>'') exec sys.sp_xml_preparedocument @H output,@XML; select QUOTE_ID,QUOTE_RECORD_ID,SERVICE_ID,ENTITLEMENT_NAME,ENTITLEMENT_COST_IMPACT,ENTITLEMENT_TYPE,ENTITLEMENT_VALUE_CODE INTO "+str(ent_temp)+"  from openxml(@H, ''ROOT/QUOTE_ITEM_ENTITLEMENT'', 0) with (QUOTE_ID VARCHAR(100) ''QUOTE_ID'',QUOTE_RECORD_ID VARCHAR(100) ''QUOTE_RECORD_ID'',ENTITLEMENT_NAME VARCHAR(100) ''ENTITLEMENT_NAME'',SERVICE_ID VARCHAR(100) ''SERVICE_ID'',ENTITLEMENT_COST_IMPACT VARCHAR(100) ''ENTITLEMENT_COST_IMPACT'',ENTITLEMENT_TYPE VARCHAR(100) ''ENTITLEMENT_TYPE'',ENTITLEMENT_VALUE_CODE VARCHAR(100) ''ENTITLEMENT_VALUE_CODE'') ; exec sys.sp_xml_removedocument @H; '")
				Parentgetdata=Sql.GetList("SELECT * FROM {} WHERE QUOTE_RECORD_ID = '{}'".format(ent_temp,self.ContractRecordId))
				Trace.Write("where------ "+str(where))
				if Parentgetdata:					
					response = self.Request_access_token()					
					Request_URL = "https://cpservices-product-configuration.cfapps.us10.hana.ondemand.com/api/v2/configurations/"+str(newConfigurationid)+"/items/1"
					#webclient.Headers[System.Net.HttpRequestHeader.Authorization] = "Bearer " + str(response["access_token"])
					cpsmatchID=11
					#response = self.Request_access_token()
					#webclient.Headers[System.Net.HttpRequestHeader.Authorization] = "Bearer " + str(response["access_token"])
					for row in Parentgetdata:
						webclient = System.Net.WebClient()
						webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/json"
						webclient.Headers[
							System.Net.HttpRequestHeader.Authorization
						] = "Basic c2ItYzQwYThiMWYtYzU5NS00ZWJjLTkyYzYtYzM4ODg4ODFmMTY0IWIyNTAzfGNwc2VydmljZXMtc2VjdXJlZCFiMzkxOm9zRzgvSC9hOGtkcHVHNzl1L2JVYTJ0V0FiMD0="
						response = webclient.DownloadString(
							"https://cpqprojdevamat.authentication.us10.hana.ondemand.com:443/oauth/token?grant_type=client_credentials"
						)
						response = eval(response)	
						webclient.Headers[System.Net.HttpRequestHeader.Authorization] = "Bearer " + str(response["access_token"])
							
						#webclient.Headers.Add("If-Match", "111")
						webclient.Headers.Add("If-Match", "1"+str(cpsmatchID))						
						try:
							requestdata = '{"characteristics":['
							
							requestdata +='{"id":"'+ str(row.ENTITLEMENT_NAME) + '","values":[' 
							if row.ENTITLEMENT_TYPE in ('Check Box','CheckBox'):
								for code in eval(row.ENTITLEMENT_VALUE_CODE):
									requestdata += '{"value":"' + code + '","selected":true}'
									requestdata +=','
								requestdata +=']},'	
							else:
								requestdata+= '{"value":"' +str(row.ENTITLEMENT_VALUE_CODE) + '","selected":true}]},'
							requestdata += ']}'
							requestdata = requestdata.replace('},]','}]')
							Trace.Write("requestdata--child-- " + str(requestdata))
							response1 = webclient.UploadString(Request_URL, "PATCH", str(requestdata))
							cpsmatchID = cpsmatchID + 10			
							
						except Exception:
							Trace.Write("Patch Error--"+str(sys.exc_info()[1]))
							cpsmatchID = cpsmatchID

			getdata=Sql.GetList("SELECT * FROM {} WHERE {}".format(tableName,where))
			cpsmatc_incr = cpsmatchID + 10
			for data in getdata:
				updateConfiguration = Sql.RunQuery("UPDATE {} SET CPS_CONFIGURATION_ID = '{}',CPS_MATCH_ID={} WHERE {} ".format(tableName,newConfigurationid,cpsmatchID,where))            
		except Exception:
			Trace.Write("Patch Error--"+str(sys.exc_info()[1]))        
		ent_temp_drop = Sql.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(ent_temp)+"'' ) BEGIN DROP TABLE "+str(ent_temp)+" END  ' ")
		return newConfigurationid,cpsmatchID

	def EntitlementRequest(self,cpsConfigID=None,cpsmatchID=None,AttributeID=None,NewValue=None,field_type=None):
		if type(NewValue) is 'str' and multiselect_flag != 'true':
			NewValue = NewValue.replace("'","''")
			# if NewValue == 'Select':
			# 	NewValue = ''
		#Trace.Write('cpsmatchID--132-----------'+str(cpsmatchID))
		#Trace.Write('AttributeID--132-----------'+str(AttributeID))
		Trace.Write('NewValue--132-----------'+str(NewValue))
		response = self.Request_access_token()
		webclient = System.Net.WebClient()		
		Trace.Write(response["access_token"])
		Request_URL = "https://cpservices-product-configuration.cfapps.us10.hana.ondemand.com/api/v2/configurations/"+str(cpsConfigID)+"/items/1"
		webclient.Headers[System.Net.HttpRequestHeader.Authorization] = "Bearer " + str(response["access_token"])
		#webclient.Headers.Add("If-Match", "111")
		#Trace.Write('cpsmatchID------'+str(cpsmatchID))
		webclient.Headers.Add("If-Match", "1"+str(cpsmatchID))
		Trace.Write(str(cpsmatchID)+"--Request_UR-L--"+Request_URL+"---cpsConfigID---: "+str(cpsConfigID))
		#AttributeValCode = ''
		try:
			#STANDARD_ATTRIBUTE_VALUES=Sql.GetFirst("SELECT STANDARD_ATTRIBUTE_VALUE FROM STANDARD_ATTRIBUTE_VALUES (nolock) where STANDARD_ATTRIBUTE_DISPLAY_VAL='{}' and SYSTEM_ID like '{}%'".format(NewValue,AttributeID))
			requestdata = '{"characteristics":[{"id":"' + AttributeID + '","values":['
			attribute_code = []
			Trace.Write("field_type--"+str(field_type))
			Trace.Write("previous_val "+str(Getprevdict))
			
			
			if field_type != 'input':
				STANDARD_ATTRIBUTE_VALUES=Sql.GetList("SELECT S.STANDARD_ATTRIBUTE_VALUE,S.STANDARD_ATTRIBUTE_DISPLAY_VAL FROM STANDARD_ATTRIBUTE_VALUES (nolock) S INNER JOIN ATTRIBUTE_DEFN (NOLOCK) A ON A.STANDARD_ATTRIBUTE_CODE=S.STANDARD_ATTRIBUTE_CODE WHERE A.SYSTEM_ID = '{}' ".format(AttributeID))
				
				if STANDARD_ATTRIBUTE_VALUES is not None:				
					#AttributeValCode=STANDARD_ATTRIBUTE_VALUES.STANDARD_ATTRIBUTE_VALUE
					ent_total_val = []
					ent_non_selec_value = []
					for val in STANDARD_ATTRIBUTE_VALUES:
						#Trace.Write('val.STANDARD_ATTRIBUTE_DISPLAY_VAL'+str(val.STANDARD_ATTRIBUTE_DISPLAY_VAL)+'---'+str(NewValue))
						#if val.STANDARD_ATTRIBUTE_DISPLAY_VAL == NewValue:
						#Trace.Write('NewValue'+str(NewValue)+'---'+str(val.STANDARD_ATTRIBUTE_DISPLAY_VAL))
						ent_total_val.append(val.STANDARD_ATTRIBUTE_VALUE)
						if (field_type == 'Check Box' and val.STANDARD_ATTRIBUTE_DISPLAY_VAL in NewValue) or (val.STANDARD_ATTRIBUTE_DISPLAY_VAL == NewValue):
							Trace.Write('inside-------')
							requestdata += '{"value":"' + val.STANDARD_ATTRIBUTE_VALUE + '","selected":true}'
							requestdata +=','
							attribute_code.append(val.STANDARD_ATTRIBUTE_VALUE)
						elif field_type == 'Check Box':
							Trace.Write("inside_J____")
							requestdata += '{"value":"' + val.STANDARD_ATTRIBUTE_VALUE + '","selected":false}'
							requestdata +=','
						elif field_type == 'Drop Down':
							Trace.Write("New_VALUE_J "+str(val.STANDARD_ATTRIBUTE_VALUE))
							# list_of_vals = []
							# list_of_vals.append(val.STANDARD_ATTRIBUTE_VALUE)
							# Trace.Write("list_of_vals_J "+str(list_of_vals))
							# try:
							# 	previous_value = Product.GetGlobal("previous_ent_val")
							# except:
							# 	previous_value = ""
							# Trace.Write("previous_Value_J "+str(previous_value))
							
							

							if NewValue != 'select':
								
								ent_non_selec_value.append(val.STANDARD_ATTRIBUTE_VALUE)
								Trace.Write("ent_total_val "+str(ent_total_val))
								Trace.Write("ent_non_selec_value "+str(ent_non_selec_value))
							elif NewValue == 'select':
								Trace.Write("inside_J____DROP_DOWN = "+str(Product.GetGlobal("pre_ent_val")))
								Trace.Write("ent_total_val "+str(ent_total_val))
								Trace.Write("ent_non_selec_value "+str(ent_non_selec_value))
								for prev_val in ent_total_val:
									if prev_val not in ent_non_selec_value:
										requestdata += '{"value":"' + prev_val + '","selected":false}'
										requestdata +=','
			else:
				Product.SetGlobal("pre_ent_val",str(NewValue))
				requestdata += '{"value":"' + NewValue + '","selected":true}'
			requestdata += ']}]}'
			requestdata = requestdata.replace(',]}]}',']}]}')
			Trace.Write(str(Request_URL)+"---requestdata--166---" + str(requestdata))

			response1 = webclient.UploadString(Request_URL, "PATCH", str(requestdata))
			#Trace.Write("patch response1---170---" + str(response1))
			
			cpsmatc_incr = int(cpsmatchID) + 10
			Trace.Write("new cps match Id: "+str(cpsmatc_incr))
					
			
		except Exception:
			Trace.Write("Patch Error---176----"+str(sys.exc_info()[1]))
			cpsmatc_incr = cpsmatchID
		Request_URL = "https://cpservices-product-configuration.cfapps.us10.hana.ondemand.com/api/v2/configurations/"+str(cpsConfigID)
		webclient.Headers[System.Net.HttpRequestHeader.Authorization] = "Bearer " + str(response["access_token"])
		Trace.Write("requestdata---180---" + str(requestdata))
		response2 = webclient.DownloadString(Request_URL)
		Trace.Write('response2--182---------'+str(response2))
		response2 = str(response2).replace(": true", ': "true"').replace(": false", ': "false"')
		return eval(response2),cpsmatc_incr,attribute_code
	
	def get_product_attr_level_cps_pricing(self, characteristics_attr_values=None,serviceId =None):
		webclient = System.Net.WebClient()
		webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/json"
		webclient.Headers[System.Net.HttpRequestHeader.Authorization] = "Basic c2ItYzQwYThiMWYtYzU5NS00ZWJjLTkyYzYtYzM4ODg4ODFmMTY0IWIyNTAzfGNwc2VydmljZXMtc2VjdXJlZCFiMzkxOm9zRzgvSC9hOGtkcHVHNzl1L2JVYTJ0V0FiMD0=";
		response = webclient.DownloadString("https://cpqprojdevamat.authentication.us10.hana.ondemand.com:443/oauth/token?grant_type=client_credentials")
		response = eval(response)
		
		Request_URL="https://cpservices-pricing.cfapps.us10.hana.ondemand.com/api/v1/statelesspricing"
		webclient.Headers[System.Net.HttpRequestHeader.Authorization] ="Bearer "+str(response['access_token'])

		today = str(datetime.datetime.today())		
		today = today.split(" ")		
		variant_condition = ', '.join(['{"factor":'+str(attr_code.get('factor'))+',"key":"'+attr_code.get('key')+'"}' for attr_code in characteristics_attr_values])
		QuoteItemList = Quote.QuoteTables["SAQICD"]
		CrtId = TagParserProduct.ParseString("<*CTX( Quote.CartId )*>")
		account_obj = Sql.GetFirst("SELECT ACCOUNT_ID FROM SAOPQT (NOLOCK) WHERE QUOTE_RECORD_ID ='{QuoteRecordId}'".format(QuoteRecordId=self.ContractRecordId))
		stp_account_id = ""
		if account_obj:
			stp_account_id = str(account_obj.ACCOUNT_ID)
		salesorg_obj = Sql.GetFirst("SELECT EXCHANGE_RATE_TYPE, DIVISION_ID, DISTRIBUTIONCHANNEL_ID, SALESORG_ID, SORG_CURRENCY, PRICINGPROCEDURE_ID, ISNULL(CUSTAXCLA_ID,1) as CUSTAXCLA_ID FROM SAQTSO (NOLOCK) WHERE QUOTE_RECORD_ID ='{QuoteRecordId}'".format(QuoteRecordId=self.ContractRecordId))
		if salesorg_obj:
			Trace.Write("serviceId--22--"+str(serviceId))			
			
			exchange_rate_type = salesorg_obj.EXCHANGE_RATE_TYPE if salesorg_obj.EXCHANGE_RATE_TYPE else 'M'
			pricing_procedure_id = salesorg_obj.PRICINGPROCEDURE_ID if salesorg_obj.PRICINGPROCEDURE_ID else 'ZZNA05'
			item_string = '{"itemId":"1","externalId":null,"quantity":{"value":'+str(1)+',"unit":"EA"},"exchRateType":"'+exchange_rate_type+'","exchRateDate":"'+str(today[0])+'","productDetails":{"productId":"'+str(serviceId)+'","baseUnit":"EA","alternateProductUnits":null},"attributes":[{"name":"KOMK-ALAND","values":["US"]},{"name":"KOMK-REGIO","values":["TX"]},{"name":"KOMK-KUNNR","values":["'+stp_account_id+'"]},{"name":"KOMK-KUNWE","values":["'+stp_account_id+'"]},{"name":"KOMK-SPART","values":["'+str(salesorg_obj.DIVISION_ID)+'"]},{"name":"KOMP-SPART","values":["'+str(salesorg_obj.DIVISION_ID)+'"]},{"name":"KOMP-PMATN","values":["'+str(serviceId)+'"]},{"name":"KOMK-WAERK","values":["'+str(salesorg_obj.SORG_CURRENCY)+'"]},{"name":"KOMK-HWAER","values":["'+str(salesorg_obj.SORG_CURRENCY)+'"]},{"name":"KOMP-PRSFD","values":["X"]},{"name":"KOMK-VTWEG","values":["'+str(salesorg_obj.DISTRIBUTIONCHANNEL_ID)+'"]},{"name":"KOMK-VKORG","values":["'+str(salesorg_obj.SALESORG_ID)+'"]},{"name":"KOMP-KPOSN","values":["0"]},{"name":"KOMP-KZNEP","values":[""]},{"name":"KOMP-ZZEXE","values":["true"]}],"accessDateList":[{"name":"KOMK-PRSDT","value":"'+str(today[0])+'"},{"name":"KOMK-FBUDA","value":"'+str(today[0])+'"}],"variantConditions":['+variant_condition+'],"statistical":true,"subItems":[]}'

			requestdata = '{"docCurrency":"'+salesorg_obj.SORG_CURRENCY+'","locCurrency":"'+salesorg_obj.SORG_CURRENCY+'","pricingProcedure":"'+pricing_procedure_id+'","groupCondition":false,"itemConditionsRequired":true,"items": ['+item_string+']}'
			Trace.Write("requestdata111111111"+str(requestdata))
			response1 = webclient.UploadString(Request_URL,str(requestdata))
			Trace.Write("res111111111"+str(response1))
			response1 = str(response1).replace(": true", ': "true"').replace(": false", ': "false"').replace(": null",': " None"')
			response1 = eval(response1)
			price = []
			for root, value in response1.items():
				if root == "items":
					price = value[:]
					break
			attr_prices = {}
			for data in price[0]['conditions']:
				#Trace.Write("condtiirontype---"+str( data['conditionType'])+'----'+str(data['conditionValue']) )
				if data['conditionType'] == 'VA00':# and data['varcondKey'] in characteristics_attr_values.get('SDCOM_VKOND'):
					total_price_val = "{:,}".format(float(data['conditionValue']))
					price_val = "{:,}".format(float(data['conditionRate']))
					#attr_prices[data['varcondKey']] = {'total_price':total_price_val, 'price':price_val, 'factor':data['varcondFactor'],'currency': data['conditionCurrency']}
					total_price_value = "{} {}".format(total_price_val, data['conditionCurrency'] )
					price_value = "{} {}".format(price_val, data['conditionCurrency'] )
					attr_prices[data['varcondKey']] = {'total_price':total_price_value , 'price':price_value, 'factor':data['varcondFactor'],'currency': data['conditionCurrency']}
				#to update quote table
			Product.SetGlobal('attr_level_pricing',str(attr_prices))	
			#Trace.Write("attr_prices111111111111"+str(attr_prices))
			return attr_prices
					

	def EntitlementSave(self, subtabName, PrevValue, NewValue, AttributeID, AttributeValCode,SectionRecordId,EquipmentId,calc_factor,costimpact,priceimapct,getmaualipval,ENT_IP_DICT):
		#AttributeValCode = AttributeValCode.replace("_"," ")
		Trace.Write(str(type(PrevValue))+'----PrevValue')
		Trace.Write(str(type(NewValue))+'----NewValue')
		if not type(NewValue) is 'str' and multiselect_flag == 'true':
			NewValue = list(NewValue)	
			multiselect_arr = NewValue
			multiselect_arr = Product.SetGlobal('multiselect_arr',str(multiselect_arr))
			Trace.Write('ArrayList-----'+str(NewValue))
		if calc_factor == '':
			calc_factor = 'null'
		if costimpact == '':
			costimpact = 'null'
		if priceimapct == '':
			priceimapct = 'null'
		UpdateEntitlement = ''
		tableName = getregionval = ''
		serviceId = ''
		parentObj = ''
		whereReq = ''
		totalcostent = 0.00
		totalpriceimpact = 0.00
		join = defaultval = ''
		ParentwhereReq=''
		getregion=Sql.GetFirst("SELECT REGION from SAQTSO WHERE QUOTE_RECORD_ID = '{}'".format(self.ContractRecordId))
		if getregion:
			getregionval = getregion.REGION		
		
		### tool relocation receiving entitilement starts
		if (self.treeparam.upper() == 'RECEIVING EQUIPMENT' or self.treeparentparam.upper() == 'RECEIVING EQUIPMENT' or self.treesuperparentparam.upper() == 'RECEIVING EQUIPMENT') and (self.treesuperparentparam == 'Other Products' or self.treetopsuperparentparam == 'Other Products' or self.treesupertopparentparam == 'Other Products' ):
			Trace.Write('inside')
			if self.treeparam.upper() == 'RECEIVING EQUIPMENT'  and subtabName == 'Entitlements':
				tableName = 'SAQTSE'
				serviceId = self.treeparentparam
				whereReq = "QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}' ".format(self.ContractRecordId,serviceId)
			elif self.treeparentparam.upper() == 'RECEIVING EQUIPMENT' and subtabName == 'Entitlements':
				tableName = 'SAQSFE'
				serviceId = self.treesuperparentparam 
				parentObj = 'SAQTSE'
				whereReq = "QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}' AND FABLOCATION_ID ='{}'".format(self.ContractRecordId,serviceId,self.treeparam)
				ParentwhereReq="QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}' ".format(self.ContractRecordId,serviceId)
			elif self.treesuperparentparam.upper() == 'RECEIVING EQUIPMENT'  and subtabName == 'Entitlements':
				tableName = 'SAQSGE'
				serviceId = self.treetopsuperparentparam
				parentObj = 'SAQTSE'
				#join = "JOIN SAQSFE ON SAQSFE.SERVICE_RECORD_ID = SAQSGE.SERVICE_RECORD_ID AND SAQSFE.QUOTE_RECORD_ID = SAQSGE.QUOTE_RECORD_ID AND SAQSFE.QUOTE_SERVICE_FAB_LOC_ENT_RECORD_ID = SAQSGE.QTSFBLENT_RECORD_ID "
				whereReq = "QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}' AND GREENBOOK ='{}' AND FABLOCATION_ID = '{}'".format(self.ContractRecordId,serviceId,self.treeparam,self.treeparentparam)
				ParentwhereReq="QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}' ".format(self.ContractRecordId,serviceId)
			elif self.treesuperparentparam.upper() == 'RECEIVING EQUIPMENT'  and subtabName == 'Equipment Entitlements':
				Trace.Write('331----treesuperparentparam----'+str(self.treesuperparentparam))
				Trace.Write('331----treetopsuperparentparam----'+str(self.treetopsuperparentparam))
				tableName = 'SAQSCE'
				#serviceId = self.treesuperparentparam
				serviceId = self.treetopsuperparentparam
				parentObj = 'SAQSGE'
				whereReq = "QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}' AND EQUIPMENT_ID = '{}' AND GREENBOOK ='{}' AND FABLOCATION_ID = '{}'".format(self.ContractRecordId,serviceId,EquipmentId,self.treeparam,self.treeparentparam)
				ParentwhereReq="QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}' AND GREENBOOK ='{}'".format(self.ContractRecordId,serviceId,self.treeparam)	
		###tool relocation receiving entitilement ends
		else:
			##addon product condition is added
			if ((self.treesuperparentparam == 'Product Offerings' or (self.treeparentparam == 'Add-On Products' and self.treesupertopparentparam == 'Product Offerings')) and subtabName == 'Entitlements'):			
				tableName = 'SAQTSE'
				serviceId = self.treeparam
				whereReq = "QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}' ".format(self.ContractRecordId,serviceId)
			elif ((self.treetopsuperparentparam == 'Product Offerings' or (self.treesuperparentparam == 'Add-On Products' and self.treesupertopparentparam == 'Comprehensive Services' )) and subtabName == 'Entitlements'):
				tableName = 'SAQSFE'
				serviceId = self.treeparentparam
				parentObj = 'SAQTSE'
				whereReq = "QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}' AND FABLOCATION_ID ='{}'".format(self.ContractRecordId,serviceId,self.treeparam)
				ParentwhereReq="QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}' ".format(self.ContractRecordId,serviceId)	
			elif ((self.treesupertopparentparam == 'Product Offerings' or (self.treetopsuperparentparam == 'Add-On Products' and self.treetopsupertopparentparam == 'Comprehensive Services')) and subtabName == 'Entitlements' and self.treeparentparam != 'Add-On Products'):
				tableName = 'SAQSGE'
				serviceId = self.treesuperparentparam
				parentObj = 'SAQTSE'
				#join = "JOIN SAQSFE ON SAQSFE.SERVICE_RECORD_ID = SAQSGE.SERVICE_RECORD_ID AND SAQSFE.QUOTE_RECORD_ID = SAQSGE.QUOTE_RECORD_ID AND SAQSFE.QUOTE_SERVICE_FAB_LOC_ENT_RECORD_ID = SAQSGE.QTSFBLENT_RECORD_ID "
				whereReq = "QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}' AND GREENBOOK ='{}' AND FABLOCATION_ID = '{}'".format(self.ContractRecordId,serviceId,self.treeparam,self.treeparentparam)
				ParentwhereReq="QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}' ".format(self.ContractRecordId,serviceId)
			elif (self.treesupertopparentparam == 'Product Offerings' and subtabName == 'Equipment Entitlements'):
				tableName = 'SAQSCE'
				serviceId = self.treesuperparentparam
				parentObj = 'SAQSGE'
				whereReq = "QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}' AND EQUIPMENT_ID = '{}' AND GREENBOOK ='{}' AND FABLOCATION_ID = '{}'".format(self.ContractRecordId,serviceId,EquipmentId,self.treeparam,self.treeparentparam)
				ParentwhereReq="QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}' AND GREENBOOK ='{}'".format(self.ContractRecordId,serviceId,self.treeparam)
			elif (self.treesupertopparentparam == 'Product Offerings' and subtabName == 'Assembly Entitlements'):
				tableName = 'SAQSAE'
				serviceId = self.treesuperparentparam
				parentObj = 'SAQSCE'
				whereReq = "QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}' AND GREENBOOK ='{}' AND EQUIPMENT_ID = '{}' AND FABLOCATION_ID = '{}' AND ASSEMBLY_ID = '{}' ".format(self.ContractRecordId,serviceId,self.treeparam,EquipmentId,self.treeparentparam,AssemblyId)
				ParentwhereReq="QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}' AND GREENBOOK ='{}'".format(self.ContractRecordId,serviceId,self.treeparam)
			elif (self.treeparentparam == 'Quote Items' and subtabName == 'Entitlements'):
				tableName = 'SAQIEN'
				serviceId = (self.treeparam).split("-")[1].strip()	
		
		
		Trace.Write('tableName'+str(tableName))
		attId = "AND ENTITLEMENT_NAME = '{}' ".format(AttributeID)		
		cpsmatchID,cpsConfigID,oldConfigID = self.getcpsID(tableName,serviceId,parentObj,whereReq,attId,ParentwhereReq)
		
		attributesdisallowedlst = []
		attributesallowedlst = []
		attributeReadonlylst = []
		attributeEditonlylst = []
		attributevalues = {}
		attributedefaultvalue = []
		where = pricemethodupdate = ""
		Gettabledata = Sql.GetFirst("SELECT * FROM {} (NOLOCK) WHERE {} ".format(tableName,whereReq))
		if multiselect_flag != 'true':
			GetDefault = Sql.GetFirst("SELECT * FROM PRENVL WHERE ENTITLEMENT_NAME = '{}' AND ENTITLEMENT_DISPLAY_VALUE = '{}'".format(AttributeID,NewValue.replace("'","''")))
		else:
			GetDefault = ''	
		product_obj = Sql.GetFirst("""SELECT 
								MAX(PDS.PRODUCT_ID) AS PRD_ID,PDS.SYSTEM_ID,PDS.PRODUCT_NAME 
							FROM PRODUCTS PDS 
							INNER JOIN PRODUCT_VERSIONS PRVS ON  PDS.PRODUCT_ID = PRVS.PRODUCT_ID 
							WHERE SYSTEM_ID ='{SystemId}' 
							GROUP BY PDS.SYSTEM_ID,PDS.UnitOfMeasure,PDS.CART_DESCRIPTION_BUILDER,PDS.PRODUCT_NAME""".format(SystemId = str(Gettabledata.SERVICE_ID)))
	
		product_tabs_obj = Sql.GetList("""SELECT 
												TOP 1000 TAB_NAME, TAB_RANK, TAB_PROD_ID, TAB_PRODUCTS.TAB_CODE
											FROM TAB_PRODUCTS
											JOIN TAB_DEFN ON TAB_DEFN.TAB_CODE = TAB_PRODUCTS.TAB_CODE
											WHERE TAB_PRODUCTS.PRODUCT_ID = {ProductId}
											ORDER BY TAB_PRODUCTS.RANK""".format(ProductId = product_obj.PRD_ID))
		
		product_attributes_obj = Sql.GetList("""SELECT TOP 1000 PAT_SCHEMA.STANDARD_ATTRIBUTE_CODE, 
													TAB_PRODUCTS.TAB_PROD_ID, TAB_PRODUCTS.TAB_CODE, ATTRIBUTE_DEFN.STANDARD_ATTRIBUTE_NAME,PRODUCT_ATTRIBUTES.LABEL AS LABEL, ATTRIBUTE_DEFN.SYSTEM_ID AS SYSTEM_ID, ATT_DISPLAY_DEFN.ATT_DISPLAY_DESC AS ATT_DISPLAY_DESC
												FROM TAB_PRODUCTS
												LEFT JOIN PAT_SCHEMA ON PAT_SCHEMA.TAB_PROD_ID=TAB_PRODUCTS.TAB_PROD_ID											
												LEFT JOIN PRODUCT_ATTRIBUTES ON PRODUCT_ATTRIBUTES.STANDARD_ATTRIBUTE_CODE = PAT_SCHEMA.STANDARD_ATTRIBUTE_CODE AND PRODUCT_ATTRIBUTES.PRODUCT_ID = TAB_PRODUCTS.PRODUCT_ID
												LEFT JOIN ATTRIBUTE_DEFN ON ATTRIBUTE_DEFN.STANDARD_ATTRIBUTE_CODE = PRODUCT_ATTRIBUTES.STANDARD_ATTRIBUTE_CODE
												LEFT JOIN ATT_DISPLAY_DEFN ON ATT_DISPLAY_DEFN.ATT_DISPLAY = PRODUCT_ATTRIBUTES.ATT_DISPLAY
												
												WHERE TAB_PRODUCTS.PRODUCT_ID = {ProductId}
												ORDER BY TAB_PRODUCTS.RANK""".format(ProductId = product_obj.PRD_ID))
		tabwise_product_attributes = {}	
		if product_attributes_obj:
			for product_attribute_obj in product_attributes_obj:
				attr_detail = {'attribute_name':str(product_attribute_obj.STANDARD_ATTRIBUTE_NAME), 
							'attribute_label':str(product_attribute_obj.LABEL), 
							'attribute_system_id':str(product_attribute_obj.SYSTEM_ID),
							'attribute_dtype':str(product_attribute_obj.ATT_DISPLAY_DESC)
							
							}
				if product_attribute_obj.TAB_PROD_ID in tabwise_product_attributes:
					tabwise_product_attributes[product_attribute_obj.TAB_PROD_ID].append(attr_detail)
				else:
					tabwise_product_attributes[product_attribute_obj.TAB_PROD_ID] = [attr_detail]
		Trace.Write("tabwise_product_attributes_J "+str(tabwise_product_attributes))
		if GetDefault:
			#Trace.Write("GetDefault------")
			if GetDefault.PRICE_METHOD:
				pricemethodupdate = GetDefault.PRICE_METHOD
			else:
				pricemethodupdate = ''
			if GetDefault.IS_DEFAULT == 0:
				defaultval = '0'
			else:
				defaultval = '1'
		else:
			defaultval = '0'
		attr_level_pricing = []
		dropdownallowlist = []
		dropdowndisallowlist = []
		if EntitlementType == 'Dropdown':
			#attr_mapping_dict, cpsmatc_incr = self.labor_type_entitlement_attr_code_mapping(cpsConfigID,cpsmatchID,AttributeID,NewValue)
			#Updatecps = "UPDATE {} SET CPS_MATCH_ID ={},CPS_CONFIGURATION_ID = '{}' WHERE {} ".format(tableName, cpsmatc_incr,cpsConfigID, whereReq)
			#cpsmatchID,cpsConfigID,oldConfigID = self.getcpsID(tableName,serviceId,parentObj,whereReq,attId,ParentwhereReq)
			get_datatype = Sql.GetFirst("""SELECT ATT_DISPLAY_DEFN.ATT_DISPLAY_DESC AS ATT_DISPLAY_DESC
												FROM TAB_PRODUCTS
												LEFT JOIN PAT_SCHEMA ON PAT_SCHEMA.TAB_PROD_ID=TAB_PRODUCTS.TAB_PROD_ID											
												LEFT JOIN PRODUCT_ATTRIBUTES ON PRODUCT_ATTRIBUTES.STANDARD_ATTRIBUTE_CODE = PAT_SCHEMA.STANDARD_ATTRIBUTE_CODE AND PRODUCT_ATTRIBUTES.PRODUCT_ID = TAB_PRODUCTS.PRODUCT_ID
												LEFT JOIN ATTRIBUTE_DEFN ON ATTRIBUTE_DEFN.STANDARD_ATTRIBUTE_CODE = PRODUCT_ATTRIBUTES.STANDARD_ATTRIBUTE_CODE
												LEFT JOIN ATT_DISPLAY_DEFN ON ATT_DISPLAY_DEFN.ATT_DISPLAY = PRODUCT_ATTRIBUTES.ATT_DISPLAY
												
												WHERE TAB_PRODUCTS.PRODUCT_ID = {ProductId} AND SYSTEM_ID = '{service_id}'""".format(ProductId = product_obj.PRD_ID,service_id = AttributeID ))
			Fullresponse,cpsmatc_incr,attribute_code = self.EntitlementRequest(cpsConfigID,cpsmatchID,AttributeID,NewValue,get_datatype.ATT_DISPLAY_DESC)
			Trace.Write("Fullresponse--"+str(Fullresponse))
			#Product.SetGlobal('Fullresponse',str(Fullresponse))
			Trace.Write("===============>>> attr_mapping_dict"+str(self.attr_code_mapping))
			'''GetDefault = Sql.GetFirst("SELECT * FROM PRENVL WHERE ENTITLEMENT_NAME = '{}' AND ENTITLEMENT_DISPLAY_VALUE = '{}'".format(AttributeID,NewValue.replace("'","''")))
			if GetDefault.PRICE_METHOD:
				pricemethodupdate = GetDefault.PRICE_METHOD
			else:
				pricemethodupdate = ''
			if GetDefault.IS_DEFAULT == 0:
				defaultval = 0
			else:
				defaultval = 1'''
			#UpdateIsdefault = " UPDATE {} SET IS_DEFAULT = '{}' WHERE ENTITLEMENT_NAME = '{}' AND {}  ".format(
			#tableName,defaultval,AttributeID, whereReq)
			Trace.Write('whereReq----'+str(whereReq))
			#Sql.RunQuery(UpdateIsdefault)
			characteristics_attr_values = []
			#dropdownallow = {}
			for rootattribute, rootvalue in Fullresponse.items():
				if rootattribute == "rootItem":
					for Productattribute, Productvalue in rootvalue.items():
						if Productattribute == "characteristics":
							for prdvalue in Productvalue:
								#dropdownallowlist = []
								#Trace.Write('attr_chk----'+str(prdvalue))
								if prdvalue["visible"] == "false":							
									attributesdisallowedlst.append(prdvalue["id"])
								if prdvalue["visible"] == "true":							
									attributesallowedlst.append(prdvalue["id"])
								if prdvalue["readOnly"] == "true":
									attributeReadonlylst.append(prdvalue["id"])
								if prdvalue["readOnly"] == "false":
									attributeEditonlylst.append(prdvalue["id"])
								if prdvalue["possibleValues"]:
									for i in prdvalue["possibleValues"]:

										if i['selectable'] == 'false' and 'valueLow' in i.keys():
											dropdowndisallowlist.append(str(prdvalue["id"])+'_'+str(i['valueLow'])	)
										elif i['selectable'] == 'true' and 'valueLow' in i.keys():
											dropdownallowlist.append(str(prdvalue["id"])+'_'+str(i['valueLow'])	)	
										#dropdownallow[prdvalue["id"]] = dropdownallowlist
								for attribute in prdvalue["values"]:									
									attributevalues[str(prdvalue["id"])] = attribute["value"]
									if attribute["author"] == "Default":
										attributedefaultvalue.append(prdvalue["id"])
								
									# if prdvalue["id"] in characteristics_attr_values:
									# 	characteristics_attr_values[str(prdvalue["id"])].append(attribute["value"])
									# else:
									# 	characteristics_attr_values[str(prdvalue["id"])] = [attribute["value"]]
						if Productattribute == "variantConditions":
							characteristics_attr_values = Productvalue
			Trace.Write("characteristics_attr_values"+str(characteristics_attr_values)+str(AttributeID))
			Trace.Write("attributesallowedlst"+str(attributesallowedlst))
			Trace.Write("dropdownallow---"+str(dropdownallowlist))
			if characteristics_attr_values and 'AGS_LAB_OPT' in AttributeID:
				Trace.Write("serviceId--1--"+str(serviceId))
				attr_prices = self.get_product_attr_level_cps_pricing(characteristics_attr_values,serviceId)
				Trace.Write("attr_prices"+str(attr_prices)+'---')
				if self.attr_code_mapping and attr_prices:
					for attr, attr_value in attr_prices.items():
						data_dict = {'key':attr}
						data_dict.update(attr_value)
						attr_level_pricing.append(data_dict)
				else:
					attr_level_pricing  =[ {'key':i['key'],'total_price':0.00, 'price':0.00, 'factor':0.00,} for i in characteristics_attr_values]
					
			Trace.Write("attr_level_pricing----"+str(attr_level_pricing))
			ServiceContainer = Product.GetContainerByName("Services")
			sec_name = updateentXML = ""
			for tab in product_tabs_obj:
				if tabwise_product_attributes.get(tab.TAB_PROD_ID):
					for attribute in tabwise_product_attributes.get(tab.TAB_PROD_ID):
						new_value_dicta = {}
						attrName = attribute['attribute_name']
						attrLabel = attribute['attribute_label']
						attrValue = attribute['attribute_name']
						attrSysId = attribute['attribute_system_id']
						DType = attribute['attribute_dtype']
						attrValueSysId = attributevalues.get(attrSysId)	
						GetDefault = Sql.GetFirst("SELECT PRICE_METHOD FROM PRENVL WHERE ENTITLEMENT_NAME = '{}' AND ENTITLEMENT_DISPLAY_VALUE = '{}'".format(str(attrSysId),attrValue))
						## replace fn &apos; added for A055S000P01-3158
						if GetDefault:
							pricemethodupdate = GetDefault.PRICE_METHOD
						try:
							if attrSysId == AttributeID:
								ent_disp_val = 	str(NewValue).replace("'", '"')
								
								ent_val_code = str(attribute_code).replace("'", '"')
								Trace.Write('ArrayList-----11'+str(NewValue))
							else:
								ent_disp_val = 	attrValue
								ent_val_code = attrValue
						except Exception as e:
							Trace.Write('except'+str(e))
							ent_disp_val = 	attrValue
							ent_val_code = attrValue
						Trace.Write('ent_disp_val-----11'+str(ent_disp_val)+'--'+str(attrSysId))
						updateentXML  += """<QUOTE_ITEM_ENTITLEMENT>
						<ENTITLEMENT_NAME>{ent_name}</ENTITLEMENT_NAME>
						<ENTITLEMENT_VALUE_CODE>{ent_val_code}</ENTITLEMENT_VALUE_CODE>
						<ENTITLEMENT_DISPLAY_VALUE>{ent_disp_val}</ENTITLEMENT_DISPLAY_VALUE>
						<ENTITLEMENT_COST_IMPACT>{ct}</ENTITLEMENT_COST_IMPACT>
						<ENTITLEMENT_PRICE_IMPACT>{pi}</ENTITLEMENT_PRICE_IMPACT>
						<IS_DEFAULT>{is_default}</IS_DEFAULT>
						<ENTITLEMENT_TYPE>{ent_type}</ENTITLEMENT_TYPE>
						<ENTITLEMENT_DESCRIPTION>{ent_desc}</ENTITLEMENT_DESCRIPTION>
						<PRICE_METHOD>{pm}</PRICE_METHOD>
						<CALCULATION_FACTOR>{cf}</CALCULATION_FACTOR>
						</QUOTE_ITEM_ENTITLEMENT>""".format(ent_name = str(attrSysId),ent_val_code = ent_val_code,ent_disp_val = ent_disp_val,ct = costimpact,pi = priceimapct,is_default = defaultval,ent_type = DType,ent_desc=attrLabel ,pm =  pricemethodupdate if str(attrSysId)==AttributeID else '',cf = '')

						UpdateEntitlement = " UPDATE {} SET ENTITLEMENT_XML= '{}' WHERE  {} ".format(tableName, updateentXML,whereReq)
						Trace.Write("@548----UpdateEntitlement"+str(UpdateEntitlement))	
							
			#Sql.RunQuery(UpdateEntitlement)	
			Updatecps = "UPDATE {} SET CPS_MATCH_ID ={},CPS_CONFIGURATION_ID = '{}' WHERE {} ".format(tableName, cpsmatc_incr,cpsConfigID, whereReq)
			Sql.RunQuery(Updatecps)
		else:
			# to insert new input column value and price factor, cost impact for manual input Start 
			getvalue = ""
			Trace.Write("-----------AttributeID----------------"+str(AttributeID))
			if "calc" in AttributeID:
				updateentXML = getDeinstall = ""
				
				""" if Quote.GetGlobal("TreeParentLevel1") == "Receiving Equipment":
					#whereReq = "QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}' AND EQUIPMENT_ID = '{}' AND GREENBOOK ='{}' AND FABLOCATION_ID = '{}'".format(self.ContractRecordId,serviceId,EquipmentId,self.treeparam,self.treeparentparam)
					quoteid = Quote.GetGlobal("contract_quote_record_id")
					EntCost = EntCost2 = EntCost3 = EntCost4 = 0.00
					getPlatform = Sql.GetFirst("SELECT PLATFORM, WAFER_SIZE FROM SAQSCO WHERE QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}' AND EQUIPMENT_ID = '{}' AND GREENBOOK ='{}' AND FABLOCATION_ID = '{}'".format(self.ContractRecordId,serviceId,EquipmentId,self.treeparam,self.treeparentparam))
					if getPlatform:
						getDeinstall = Sql.GetFirst("SELECT  ISNULL(INSTALL_T0T1_CE_HRS,0) AS INSTALL_T0T1_CE_HRS,ISNULL(INSTALL_T0T1_TECH_HRS,0) AS INSTALL_T0T1_TECH_HRS ,ISNULL(INSTALL_T2_CE_HRS,0) AS INSTALL_T2_CE_HRS,ISNULL(INSTALL_T2_PSE_HRS,0) AS INSTALL_T2_PSE_HRS,ISNULL(INSTALL_T2_SSE_HRS,0) AS INSTALL_T2_SSE_HRS,ISNULL(INSTALL_T3_CE_HRS,0) AS INSTALL_T3_CE_HRS,ISNULL(INSTALL_T3_PSE_HRS,0) AS INSTALL_T3_PSE_HRS,ISNULL(INSTALL_T3_SSE_HRS,0) AS INSTALL_T3_SSE_HRS,DEINSTALL_CE_HRS,DEINSTALL_PRICE,DEINSTALL_TECH_HRS,DEINSTALL_TRDPTY_AMOUNT FROM PRLPBK (NOLOCK) WHERE GREENBOOK = '{TreeParam}' AND SUBSTRATESIZE_ID LIKE '%{sub}%'".format(TreeParam=self.treeparam,sub=getPlatform.WAFER_SIZE,plt=getPlatform.PLATFORM))
						GetRegion = Sql.GetFirst("SELECT REGION,GLOBAL_CURRENCY FROM SAQTMT WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{}'".format(quoteid))
						Region = GetRegion.REGION
						getRegionhrs = Sql.GetFirst("SELECT TECH_RATE,CE_RATE,PSE_RATE,SSE_RATE FROM SAREGN WHERE REGION = '{}'".format(Region))
						
						
						
						
						curr = GetRegion.GLOBAL_CURRENCY if GetRegion else "" """
				AttributeID = AttributeID.replace("_calc","")
				gettechlaborcostimpact = gettechlaborpriceimpact = getpselaborcostimpact = getpselaborpriceimpact = ""
				for key,val in ENT_IP_DICT.items():	
					getcostbaborimpact =""
					getpriceimpact = ""
					calculation_factor =""
					pricemethodupdate = ""
					Trace.Write("val---"+str(val))
					Trace.Write("key---"+str(key))
					#getregionvalq = "AMT"
					getvalue = str((val).split("||")[4]).strip()
										
					totalpriceent = ""					
					decimal_place ="2"
					my_format = "{:." + str(decimal_place) + "f}"
					if getvalue:
						if str((val).split("||")[1]) == "CE":	
							
							getcostbabor = Sql.GetFirst("select CE_COST,CE_PRICE from SAREGN where REGION='{}'".format(getregionval))
							if getcostbabor:
								cecost = str(getcostbabor.CE_COST).strip()
								getcostbaborimpact = str(float(getvalue)*float(cecost))
								#getcostbaborimpact = '{:.2f}'.format(round(float(getcostbaborimpact), 2))
								
								getcostbaborimpact = str(my_format.format(round(float(getcostbaborimpact), int(decimal_place))))
								#value1234 = str(my_format.format(round(float(getcostbaborimpact))))								
								getpriceimpact = str(float(getvalue)*float(getcostbabor.CE_PRICE))
								getpriceimpact = str(my_format.format(round(float(getpriceimpact), int(decimal_place))))
								
						elif str((val).split("||")[1]) == "Technician_or_3rd_Party":			
							gettechlabor = Sql.GetFirst("select TECH_COST,TECH_PRICE from SAREGN where REGION='{}'".format(getregionval))
							if gettechlabor:
								getcostbaborimpact = str(float(getvalue)*float(gettechlabor.TECH_COST))
								getcostbaborimpact = str(my_format.format(round(float(getcostbaborimpact), int(decimal_place))))
								getpriceimpact = str(float(getvalue)*float(gettechlabor.TECH_PRICE))
								getpriceimpact = str(my_format.format(round(float(getpriceimpact), int(decimal_place))))
								
						elif str((val).split("||")[1]) == "PSE":							
							getpselabor = Sql.GetFirst("select PSE_COST,PSE_PRICE from SAREGN where REGION='{}' ".format(getregionval))
							if getpselabor:
								getcostbaborimpact = str(float(getvalue)*float(getpselabor.PSE_COST))
								getcostbaborimpact = str(my_format.format(round(float(getcostbaborimpact), int(decimal_place))))
								getpriceimpact = str(float(getvalue)*float(getpselabor.PSE_PRICE))
								getpriceimpact = str(my_format.format(round(float(getpriceimpact), int(decimal_place))))
					
					##assigning cost impact, price impact, calc factor value  starts
					else:
						getcostbaborimpact = costimpact
						getpriceimpact = priceimapct
					try:
						attr_level_pricing = eval(Product.GetGlobal('attr_level_pricing')) 
						Trace.Write("try----")
						getcostbaborimpact = attr_level_pricing[key]['price']
						Trace.Write("get_cost---"+str(get_cost))

					except:	
						attr_level_pricing = ""
						Trace.Write("")
					Trace.Write("attr_level_pricing"+str(attr_level_pricing))
					if attr_level_pricing:
						getcostbaborimpact = "{0:.2f}".format(float(attr_level_pricing[key]['price'])) 	
						getpriceimpact = attr_level_pricing[key]['total_price']
						calculation_factor =  attr_level_pricing[key]['factor']
						pricemethodupdate =  attr_level_pricing[key]['currency']
					else:	
						if str((val).split("||")[5]).strip() and str((val).split("||")[5]).strip() not in ('undefined','NULL'):
							getcostbaborimpact = str((val).split("||")[5]).replace(',','').strip()
							try:
								getcostbaborimpact = getcostbaborimpact.split(" ")[0].strip()
								#pricemethodupdate = getpriceimpact.split(" ")[1].strip()
							except:
								getcostbaborimpact = getcostbaborimpact	
							Trace.Write("getcostbaborimpact---"+str(getcostbaborimpact))
						if str((val).split("||")[6]).strip() and str((val).split("||")[6]).strip()not in ('undefined','NULL'):
							getpriceimpact = str((val).split("||")[6]).replace(',','').strip()
							try:
								price_split = getpriceimpact.split(" ")
								getpriceimpact = price_split[0].strip()
								pricemethodupdate = price_split[1].strip()
							except:
								getpriceimpact = getpriceimpact	
							Trace.Write("getpriceimpact---"+str(getpriceimpact))
						if str((val).split("||")[4]).strip() and str((val).split("||")[4]).strip() not in ('undefined','NULL'):
							calculation_factor = str((val).split("||")[4]).strip()
							Trace.Write("calculation_factor---"+str(calculation_factor))
						# if (str((val).split("||")[7]).strip() and str((val).split("||")[7]).strip() not in ('undefined','NULL') ) :
						# 	pricemethodupdate = str((val).split("||")[7]).strip()

					##assigning cost impact, price impact, calc factor value ends
					
					if getcostbaborimpact == "" or getcostbaborimpact == 'null':
						getcostbaborimpact = 0.00
					if getpriceimpact == "" or getpriceimpact == 'null':
						getpriceimpact = 0.00
					totalcostent += float(getcostbaborimpact)
					totalpriceimpact += float(getpriceimpact)
					if calculation_factor in ('undefined','NULL', 'null'):
						calculation_factor =""	
					if getcostbaborimpact == 0.00:
						getcostbaborimpact = ""
					if getpriceimpact == 0.00:
						getpriceimpact = ""
					##storing values for multi select  starts
					if str((val).split("||")[2]) == "Check Box":
						display_vals = str((val).split("||")[0])
						if display_vals:
							display_vals = str(tuple(eval(display_vals))).replace(',)',')')
							STANDARD_ATTRIBUTE_VALUES=Sql.GetList("SELECT S.STANDARD_ATTRIBUTE_VALUE,S.STANDARD_ATTRIBUTE_DISPLAY_VAL FROM STANDARD_ATTRIBUTE_VALUES (nolock) S INNER JOIN ATTRIBUTE_DEFN (NOLOCK) A ON A.STANDARD_ATTRIBUTE_CODE=S.STANDARD_ATTRIBUTE_CODE WHERE A.SYSTEM_ID = '{sys_id}' and S.STANDARD_ATTRIBUTE_DISPLAY_VAL in {display_vals} ".format(sys_id = str(key),display_vals = display_vals  ))
							Trace.Write('Check Box--------'+str(val)+'----'+str(type(str((val).split("||")[0]))) +'----'+str(str((val).split("||")[0])) )
							if STANDARD_ATTRIBUTE_VALUES:
								attr_code = [code.STANDARD_ATTRIBUTE_VALUE for code in STANDARD_ATTRIBUTE_VALUES]
								Trace.Write('attr_code--if'+str(attr_code))
								ent_val_code =  str(attr_code).replace("'", '"')
						else:
							attr_code = ""
					else:
						ent_val_code = 	str((val).split("||")[0]).replace("'","&apos;")
					Trace.Write('ent_val_code--'+str(key)+'--'+str(ent_val_code))
					##ends

					##------ commented and assign the default currency ---++
					#GetDefault = Sql.GetFirst("SELECT PRICE_METHOD FROM PRENVL WHERE ENTITLEMENT_NAME = '{}' AND ENTITLEMENT_DISPLAY_VALUE = '{}'".format(str(key),str((val).split("||")[0]).replace("'","&apos;")))
					## replace fn &apos; added for A055S000P01-3158
					#Trace.Write("getcostbaborimpact--1--"+str(getcostbaborimpact))
					#Trace.Write("getpriceimpact--1--"+str(getpriceimpact))
					#if GetDefault:
					#	pricemethodupdate = GetDefault.PRICE_METHOD
					""" get_value = value.ENTITLEMENT_DISPLAY_VALUE
					get_cost_impact = value.ENTITLEMENT_COST_IMPACT
					get_price_impact = value.ENTITLEMENT_PRICE_IMPACT
					get_curr = value.PRICE_METHOD """
					""" if 'AGS_SFM_DEI_PAC' in key and 'Included' in val:
						EntCost =(float(getDeinstall.DEINSTALL_CE_HRS)*float(getRegionhrs.CE_RATE)) + (float(getDeinstall.DEINSTALL_TECH_HRS)*float(getRegionhrs.TECH_RATE))
						Trace.Write("ENTCOST1---------->"+str(EntCost))
						getcostbaborimpact = "{0:.2f}".format(EntCost)
						pricemethodupdate = curr
					if ('AGS_RFM_INS_T0' in key or 'AGS_RFM_INS_T1' in key) and 'Included' in val:
						EntCost2 = (float(getDeinstall.INSTALL_T0T1_CE_HRS)*float(getRegionhrs.CE_RATE)) + (float(getDeinstall.INSTALL_T0T1_TECH_HRS)*float(getRegionhrs.TECH_RATE)) + float(getDeinstall.DEINSTALL_TRDPTY_AMOUNT)
						Trace.Write("ENTCOST2---------->"+str(EntCost2))
						getcostbaborimpact = "{0:.2f}".format(EntCost2)
						pricemethodupdate = curr
						#get_curr = curr
					if 'AGS_RFM_INS_T2' in key and 'Included' in val:
						EntCost3 = (float(getDeinstall.INSTALL_T2_CE_HRS)*float(getRegionhrs.CE_RATE)) + (float(getDeinstall.INSTALL_T2_PSE_HRS)*float(getRegionhrs.PSE_RATE)) + (float(getDeinstall.INSTALL_T2_SSE_HRS)*float(getRegionhrs.SSE_RATE))
						Trace.Write("ENTCOST3---------->"+str(EntCost3))
						getcostbaborimpact = "{0:.2f}".format(EntCost3)
						pricemethodupdate = curr
						#get_curr = curr
					if 'AGS_RFM_INS_T3' in key and 'Included' in val:
						EntCost4 = (float(getDeinstall.INSTALL_T3_CE_HRS)*float(getRegionhrs.CE_RATE)) + (float(getDeinstall.INSTALL_T3_PSE_HRS)*float(getRegionhrs.PSE_RATE)) + (float(getDeinstall.INSTALL_T3_SSE_HRS)*float(getRegionhrs.SSE_RATE))
						Trace.Write("ENTCOST3---------->"+str(EntCost4))
						getcostbaborimpact = "{0:.2f}".format(EntCost4)
						pricemethodupdate = curr """
						#get_curr = curr
					#Trace.Write("Cost---->"+str(getcostbaborimpact))
					#getpriceimpact = str(getpriceimpact)+" "+str(pricemethodupdate)
					#getcostbaborimpact = str(getcostbaborimpact)+" "+str(pricemethodupdate)
					updateentXML  += """<QUOTE_ITEM_ENTITLEMENT>
						<ENTITLEMENT_NAME>{ent_name}</ENTITLEMENT_NAME>
						<ENTITLEMENT_VALUE_CODE>{ent_val_code}</ENTITLEMENT_VALUE_CODE>
						<ENTITLEMENT_DISPLAY_VALUE>{ent_disp_val}</ENTITLEMENT_DISPLAY_VALUE>
						<ENTITLEMENT_COST_IMPACT>{ct}</ENTITLEMENT_COST_IMPACT>
						<ENTITLEMENT_PRICE_IMPACT>{pi}</ENTITLEMENT_PRICE_IMPACT>
						<IS_DEFAULT>{is_default}</IS_DEFAULT>
						<ENTITLEMENT_TYPE>{ent_type}</ENTITLEMENT_TYPE>
						<ENTITLEMENT_DESCRIPTION>{ent_desc}</ENTITLEMENT_DESCRIPTION>
						<PRICE_METHOD>{pm}</PRICE_METHOD>
						<CALCULATION_FACTOR>{cf}</CALCULATION_FACTOR>
						</QUOTE_ITEM_ENTITLEMENT>""".format(ent_name = str(key),ent_val_code = ent_val_code,ent_disp_val = str((val).split("||")[0]).replace("'","&apos;"),ct = getcostbaborimpact,pi = getpriceimpact,is_default = '0' if str(key)==AttributeID else '1',ent_type = str((val).split("||")[2]),ent_desc=str((val).split("||")[3]) ,pm = pricemethodupdate ,cf =calculation_factor )
					#Trace.Write("updateentXML---"+str(updateentXML))
				UpdateEntitlement = " UPDATE {} SET ENTITLEMENT_XML= REPLACE('{}','&apos;','''') WHERE  {} ".format(tableName, updateentXML,whereReq)
				###to update match id at all level while saving starts
				get_match_id = Sql.GetFirst("select CPS_MATCH_ID FROM {} WHERE {}".format(tableName,whereReq))
				ent_tables_list = ['SAQTSE','SAQSFE','SAQSGE','SAQSCE','SAQSAE']
				#ent_tables_list.remove(tableName)
				if get_match_id:
					for table in ent_tables_list:
						Updatecps = "UPDATE {} SET CPS_MATCH_ID ={} WHERE QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}'".format(table, get_match_id.CPS_MATCH_ID, self.ContractRecordId, serviceId)
						Sql.RunQuery(Updatecps)
				##to update match id at all level while saving ends

				Sql.RunQuery(UpdateEntitlement)
				Trace.Write("TEST COMMIT")
				where = " QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}'".format(self.ContractRecordId,self.treeparentparam)
				EntCost = EntCost2 = EntCost3 = EntCost4 = 0.00
				getPlatform = Sql.GetList("SELECT EQUIPMENT_ID,WAFER_SIZE,GREENBOOK,PLATFORM  FROM SAQSCO WHERE {where}".format(where=where))
				GetRegion = Sql.GetFirst("SELECT REGION,GLOBAL_CURRENCY FROM SAQTMT WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{}'".format(self.ContractRecordId))
				Region = GetRegion.REGION
				getRegionhrs = Sql.GetFirst("SELECT TECH_RATE,CE_RATE,PSE_RATE,SSE_RATE FROM SAREGN WHERE REGION = '{}'".format(Region))
				curr = GetRegion.GLOBAL_CURRENCY if GetRegion else ""
				list1 = {}
				list2 = {}
				list3 = {}
				list4 = {}
				if getPlatform and 'Z0007' in serviceId:
					#Log.Info("Entering if")
					for a in getPlatform:
					
						getDeinstall = Sql.GetFirst("SELECT ISNULL(INSTALL_T0T1_CE_HRS,0) AS INSTALL_T0T1_CE_HRS,ISNULL(INSTALL_T0T1_TECH_HRS,0) AS INSTALL_T0T1_TECH_HRS ,ISNULL(INSTALL_T2_CE_HRS,0) AS INSTALL_T2_CE_HRS,ISNULL(INSTALL_T2_PSE_HRS,0) AS INSTALL_T2_PSE_HRS,ISNULL(INSTALL_T2_SSE_HRS,0) AS INSTALL_T2_SSE_HRS,ISNULL(INSTALL_T3_CE_HRS,0) AS INSTALL_T3_CE_HRS,ISNULL(INSTALL_T3_PSE_HRS,0) AS INSTALL_T3_PSE_HRS,ISNULL(INSTALL_T3_SSE_HRS,0) AS INSTALL_T3_SSE_HRS,ISNULL(DEINSTALL_CE_HRS,0) AS DEINSTALL_CE_HRS,DEINSTALL_PRICE,DEINSTALL_TECH_HRS,DEINSTALL_TRDPTY_AMOUNT FROM PRLPBK (NOLOCK) WHERE GREENBOOK = '{Greenbook}' AND SUBSTRATESIZE_ID = '{sub}' AND PLATFORM_ID = '{plt}' AND REGION = '{Region}'".format(Greenbook=a.GREENBOOK,sub=a.WAFER_SIZE,Region=Region,plt=a.PLATFORM))
						if getDeinstall:
							Trace.Write("if---")
							EntCost =str((float(getDeinstall.DEINSTALL_CE_HRS)*float(getRegionhrs.CE_RATE)) + (float(getDeinstall.DEINSTALL_TECH_HRS)*float(getRegionhrs.TECH_RATE)))
							list1[str(a.EQUIPMENT_ID)] = EntCost
							#list1.append(EntCost)
							Trace.Write("LIST1----"+str(list1))
							
							EntCost2 = str((float(getDeinstall.INSTALL_T0T1_CE_HRS)*float(getRegionhrs.CE_RATE)) + (float(getDeinstall.INSTALL_T0T1_TECH_HRS)*float(getRegionhrs.TECH_RATE)) + float(getDeinstall.DEINSTALL_TRDPTY_AMOUNT))
							list2[str(a.EQUIPMENT_ID)] = EntCost2
							#list2.append(EntCost2)
							Trace.Write("LIST2----"+str(list2))
							
							EntCost3 = str((float(getDeinstall.INSTALL_T2_CE_HRS)*float(getRegionhrs.CE_RATE)) + (float(getDeinstall.INSTALL_T2_PSE_HRS)*float(getRegionhrs.PSE_RATE)) + (float(getDeinstall.INSTALL_T2_SSE_HRS)*float(getRegionhrs.SSE_RATE)))
							list3[str(a.EQUIPMENT_ID)] = EntCost3
							#list3.append(EntCost3)
							Trace.Write("LIST3----"+str(list3))
							EntCost4 = str((float(getDeinstall.INSTALL_T3_CE_HRS)*float(getRegionhrs.CE_RATE)) + (float(getDeinstall.INSTALL_T3_PSE_HRS)*float(getRegionhrs.PSE_RATE)) + (float(getDeinstall.INSTALL_T3_SSE_HRS)*float(getRegionhrs.SSE_RATE)))
							list4[str(a.EQUIPMENT_ID)] = EntCost4
							#list4.append(EntCost4)
							Trace.Write("LIST4----"+str(list4))
						else:
							Trace.Write("else---")
							EntCost = 0.00
							EntCost2 = 0.00
							EntCost3 = 0.00
							EntCost4 = 0.00
							list1[str(a.EQUIPMENT_ID)] = str(EntCost)
							list2[str(a.EQUIPMENT_ID)] = str(EntCost2)
							list3[str(a.EQUIPMENT_ID)] = str(EntCost3)
							list4[str(a.EQUIPMENT_ID)] = str(EntCost4)
					objName = tableName
					Trace.Write("objName--"+str(objName)+'----'+str(where))
					getinnercon  = Sql.GetFirst("select CPS_MATCH_ID,CPS_CONFIGURATION_ID,QUOTE_RECORD_ID,convert(xml,replace(replace(ENTITLEMENT_XML,'&',';#38'),'''',';#39')) as ENTITLEMENT_XML from "+str(objName)+" (nolock)  where  "+str(where)+"")
					GetXMLsecField = Sql.GetList("SELECT distinct e.QUOTE_RECORD_ID, replace(X.Y.value('(ENTITLEMENT_NAME)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_NAME,replace(X.Y.value('(IS_DEFAULT)[1]', 'VARCHAR(128)'),';#38','&') as IS_DEFAULT,replace(X.Y.value('(ENTITLEMENT_COST_IMPACT)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_COST_IMPACT,replace(X.Y.value('(CALCULATION_FACTOR)[1]', 'VARCHAR(128)'),';#38','&') as CALCULATION_FACTOR,replace(X.Y.value('(ENTITLEMENT_PRICE_IMPACT)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_PRICE_IMPACT,replace(X.Y.value('(ENTITLEMENT_TYPE)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_TYPE,replace(X.Y.value('(ENTITLEMENT_VALUE_CODE)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_VALUE_CODE,replace(X.Y.value('(ENTITLEMENT_DESCRIPTION)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_DESCRIPTION,replace(replace(X.Y.value('(ENTITLEMENT_DISPLAY_VALUE)[1]', 'VARCHAR(128)'),';#38','&'),';#39','''') as ENTITLEMENT_DISPLAY_VALUE,replace(X.Y.value('(PRICE_METHOD)[1]', 'VARCHAR(128)'),';#38','&') as PRICE_METHOD FROM (select '"+str(getinnercon.QUOTE_RECORD_ID)+"' as QUOTE_RECORD_ID,convert(xml,'"+str(getinnercon.ENTITLEMENT_XML)+"') as ENTITLEMENT_XML ) e OUTER APPLY e.ENTITLEMENT_XML.nodes('QUOTE_ITEM_ENTITLEMENT') as X(Y) ")


					for e in getPlatform:
						updatexml = ""
						updateentXML = ""
						eq = str(e.EQUIPMENT_ID)
						for value in GetXMLsecField:
							
							get_name = value.ENTITLEMENT_NAME
							Trace.Write("VALUE IN XML--------->"+str(get_name))
							get_value = value.ENTITLEMENT_DISPLAY_VALUE
							get_cost_impact = value.ENTITLEMENT_COST_IMPACT
							get_price_impact = value.ENTITLEMENT_PRICE_IMPACT
							get_curr = value.PRICE_METHOD
							if 'AGS_SFM_DEI_PAC' in get_name and 'Included' in get_value:
								#get_cost_impact = "{0:.2f}".format(next(float(x.split("_")[0]) for x in list1 if str(e.EQUIPMENT_ID) in x))
								get_cost_impact = "{0:.2f}".format(float(list1[eq]))
								#get_cost_impact = "{0:.2f}".format(float(list1[0]))
								get_curr = curr
								Trace.Write("ENTCOST1 = "+str(get_cost_impact))
							elif 'AGS_RFM_INS_T1' in get_name and 'Included' in get_value:
								#get_cost_impact = "{0:.2f}".format(next(float(x.split("_")[0]) for x in list2 if str(e.EQUIPMENT_ID) in x))
								Trace.Write("list2="+str(list2))
								get_cost_impact = "{0:.2f}".format(float(list2[eq]))
								get_curr = curr
								Trace.Write("ENTCOST2 = "+str(float(list2[e.EQUIPMENT_ID])))
								Trace.Write("ENTCOST2 = "+str(get_cost_impact))
							elif 'AGS_RFM_INS_T2' in get_name and 'Included' in get_value:
								#get_cost_impact = "{0:.2f}".format(next(float(x.split("_")[0]) for x in list3 if str(e.EQUIPMENT_ID) in x))
								get_cost_impact = "{0:.2f}".format(float(list3[eq]))
								get_curr = curr
								Trace.Write("ENTCOST3 = "+str(get_cost_impact))
							elif 'AGS_RFM_INS_T3' in get_name and 'Included' in get_value:
								#get_cost_impact = "{0:.2f}".format(next(float(x.split("_")[0]) for x in list1 if str(e.EQUIPMENT_ID) in x))
								get_cost_impact = "{0:.2f}".format(float(list4[eq]))
								get_curr = curr
								Trace.Write("ENTCOST4 = "+str(get_cost_impact))
							
							updatexml  = """<QUOTE_ITEM_ENTITLEMENT>
								<ENTITLEMENT_NAME>{ent_name}</ENTITLEMENT_NAME>
								<ENTITLEMENT_VALUE_CODE>{ent_val_code}</ENTITLEMENT_VALUE_CODE>
								<ENTITLEMENT_DISPLAY_VALUE>{ent_disp_val}</ENTITLEMENT_DISPLAY_VALUE>
								<ENTITLEMENT_COST_IMPACT>{ct}</ENTITLEMENT_COST_IMPACT>
								<ENTITLEMENT_PRICE_IMPACT>{pi}</ENTITLEMENT_PRICE_IMPACT>
								<IS_DEFAULT>{is_default}</IS_DEFAULT>
								<ENTITLEMENT_TYPE>{ent_type}</ENTITLEMENT_TYPE>
								<ENTITLEMENT_DESCRIPTION>{ent_desc}</ENTITLEMENT_DESCRIPTION>
								<PRICE_METHOD>{pm}</PRICE_METHOD>
								<CALCULATION_FACTOR>{cf}</CALCULATION_FACTOR>
								</QUOTE_ITEM_ENTITLEMENT>""".format(ent_name = get_name,ent_val_code = value.ENTITLEMENT_VALUE_CODE,ent_disp_val = get_value ,ct = str(get_cost_impact) ,pi = get_price_impact ,is_default = value.IS_DEFAULT ,ent_desc= value.ENTITLEMENT_DESCRIPTION ,pm = get_curr ,cf= value.CALCULATION_FACTOR , ent_type = value.ENTITLEMENT_TYPE)
							updateentXML  += updatexml
							if ('AGS_RFM_INS_T0' in get_name or 'AGS_RFM_INS_T1' in get_name):
						
								Trace.Write("xml--------->"+str(updatexml))
						where = " SAQSCE.QUOTE_RECORD_ID = '{}' AND SAQSCE.SERVICE_ID = '{}'".format(self.ContractRecordId,self.treeparentparam)
						Trace.Write("where condition--"+str(where))
						UpdateEntitlement = "UPDATE SAQSCE SET ENTITLEMENT_XML= '{}',CPS_MATCH_ID ={},CPS_CONFIGURATION_ID = '{}' WHERE {} AND SAQSCE.EQUIPMENT_ID = '{}'".format(updateentXML,getinnercon.CPS_MATCH_ID,getinnercon.CPS_CONFIGURATION_ID,where,e.EQUIPMENT_ID)
						Trace.Write("UPDATE---"+str(UpdateEntitlement))
						# UpdateEntitlement_tst = " UPDATE {} SET ENTITLEMENT_XML= '', {} {} ".format(obj,update_fields,where_condition)
						Sql.RunQuery(UpdateEntitlement)
				#update SAQICO
				#updateSAQICO = " UPDATE {} SET ENTITLEMENT_COST_IMPACT={},ENTITLEMENT_PRICE_IMPACT={} WHERE  PRICING_STATUS IN ('PARTIALLY PRICED','ACQUIRED') AND {}  ".format('SAQICO',costimpact,priceimapct, whereReq)
				getsaletypeloc = Sql.GetFirst("select SALE_TYPE from SAQTMT where MASTER_TABLE_QUOTE_RECORD_ID = '{}'".format(self.ContractRecordId))
				if getsaletypeloc:					
					if getsaletypeloc.SALE_TYPE == "TOOL RELOCATION":
						updateSAQICO = Sql.RunQuery("""UPDATE SAQICO 
										SET ENTITLEMENT_PRICE_IMPACT = CASE
													WHEN EXCHANGE_RATE > 0 THEN ISNULL({priceimp}, 0) * ISNULL(EXCHANGE_RATE,0)
													ELSE {priceimp}
													END,
										ENTITLEMENT_COST_IMPACT = '{costimp}' where {WhereCondition}""".format(costimp=totalcostent,priceimp=totalpriceimpact,WhereCondition=whereReq))
						QueryStatement ="""UPDATE a SET a.TOTAL_COST = b.ENTITLEMENT_COST_IMPACT,a.TARGET_PRICE = b.ENTITLEMENT_PRICE_IMPACT,a.YEAR_1 = b.ENTITLEMENT_PRICE_IMPACT FROM SAQICO a INNER JOIN SAQICO b on a.EQUIPMENT_ID = b.EQUIPMENT_ID and a.QUOTE_ID = b.QUOTE_ID where a.QUOTE_RECORD_ID = '{QuoteRecordId}' """.format(QuoteRecordId= self.ContractRecordId)
						Sql.RunQuery(QueryStatement)
						QueryStatement ="""UPDATE a SET a.TAX = CASE WHEN a.TAX_PERCENTAGE > 0 THEN (a.TARGET_PRICE) * (a.TAX_PERCENTAGE/100) ELSE a.TAX END FROM SAQICO a INNER JOIN SAQICO b on a.EQUIPMENT_ID = b.EQUIPMENT_ID and a.QUOTE_ID = b.QUOTE_ID where a.QUOTE_RECORD_ID = '{QuoteRecordId}'""".format(QuoteRecordId= self.ContractRecordId)
						Sql.RunQuery(QueryStatement)
						QueryStatement ="""UPDATE A SET A.EXTENDED_PRICE = B.TARGET_PRICE + B.TAX FROM SAQICO A INNER JOIN SAQICO B on A.EQUIPMENT_ID = B.EQUIPMENT_ID and A.QUOTE_ID = B.QUOTE_ID where A.QUOTE_RECORD_ID = '{QuoteRecordId}' """.format(QuoteRecordId= self.ContractRecordId)
						Sql.RunQuery(QueryStatement)
						QueryStatement = """UPDATE A  SET A.TOTAL_COST = B.TOTAL_COST FROM SAQITM A(NOLOCK) JOIN (SELECT SUM(TOTAL_COST) AS TOTAL_COST,QUOTE_RECORD_ID,SERVICE_ID from SAQICO(NOLOCK) WHERE QUOTE_RECORD_ID ='{QuoteRecordId}' GROUP BY QUOTE_RECORD_ID,SERVICE_ID) B ON A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.SERVICE_ID=B.SERVICE_ID """.format(QuoteRecordId= self.ContractRecordId)
						Sql.RunQuery(QueryStatement)
						QueryStatement = """UPDATE A  SET A.TARGET_PRICE = B.TARGET_PRICE FROM SAQITM A(NOLOCK) JOIN (SELECT SUM(TARGET_PRICE) AS TARGET_PRICE,QUOTE_RECORD_ID,SERVICE_ID from SAQICO(NOLOCK) WHERE QUOTE_RECORD_ID ='{QuoteRecordId}' GROUP BY QUOTE_RECORD_ID,SERVICE_ID) B ON A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.SERVICE_ID=B.SERVICE_ID """.format(QuoteRecordId= self.ContractRecordId)
						Sql.RunQuery(QueryStatement)
						QueryStatement = """UPDATE A  SET A.EXTENDED_PRICE = B.EXTENDED_PRICE FROM SAQITM A(NOLOCK) JOIN (SELECT SUM(EXTENDED_PRICE) AS EXTENDED_PRICE,QUOTE_RECORD_ID,SERVICE_ID from SAQICO(NOLOCK) WHERE QUOTE_RECORD_ID ='{QuoteRecordId}' GROUP BY QUOTE_RECORD_ID,SERVICE_ID) B ON A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.SERVICE_ID=B.SERVICE_ID """.format(QuoteRecordId= self.ContractRecordId)
						Sql.RunQuery(QueryStatement)
						QueryStatement = """UPDATE A  SET A.YEAR_1 = B.YEAR_1 FROM SAQITM A(NOLOCK) JOIN (SELECT SUM(YEAR_1) AS YEAR_1,QUOTE_RECORD_ID,SERVICE_ID from SAQICO(NOLOCK) WHERE QUOTE_RECORD_ID ='{QuoteRecordId}' GROUP BY QUOTE_RECORD_ID,SERVICE_ID) B ON A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.SERVICE_ID=B.SERVICE_ID """.format(QuoteRecordId= self.ContractRecordId)
						Sql.RunQuery(QueryStatement)
						QueryStatement = """UPDATE A  SET A.TAX = B.TAX FROM SAQITM A(NOLOCK) JOIN (SELECT SUM(TAX) AS TAX,QUOTE_RECORD_ID,SERVICE_ID from SAQICO(NOLOCK) WHERE QUOTE_RECORD_ID ='{QuoteRecordId}' GROUP BY QUOTE_RECORD_ID,SERVICE_ID) B ON A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.SERVICE_ID=B.SERVICE_ID """.format(QuoteRecordId= self.ContractRecordId)
						Sql.RunQuery(QueryStatement)
						QueryStatement ="""UPDATE a SET a.PRICING_STATUS = 'ACQUIRED' FROM SAQICO a INNER JOIN SAQICO b on a.EQUIPMENT_ID = b.EQUIPMENT_ID and a.QUOTE_ID = b.QUOTE_ID where a.QUOTE_RECORD_ID = '{QuoteRecordId}' """.format(QuoteRecordId= self.ContractRecordId)
						Sql.RunQuery(QueryStatement)
						QueryStatement ="""UPDATE a SET a.PRICING_STATUS = 'ACQUIRED' FROM SAQITM a INNER JOIN SAQITM b on a.SERVICE_ID = b.SERVICE_ID and a.QUOTE_ID = b.QUOTE_ID where a.QUOTE_RECORD_ID = '{QuoteRecordId}' """.format(QuoteRecordId= self.ContractRecordId)
						Sql.RunQuery(QueryStatement) 
						QueryStatement ="""UPDATE a SET a.TOTAL_COST = b.TOTAL_COST,a.TARGET_PRICE = b.TARGET_PRICE,a.YEAR_1 = b.YEAR_1,a.TAX = b.TAX,a.EXTENDED_PRICE = b.EXTENDED_PRICE FROM QT__SAQICO a INNER JOIN SAQICO b on a.EQUIPMENT_ID = b.EQUIPMENT_ID and a.QUOTE_ID = b.QUOTE_ID where a.QUOTE_RECORD_ID = '{QuoteRecordId}' """.format(QuoteRecordId= self.ContractRecordId)
						Sql.RunQuery(QueryStatement)
						QueryStatement ="""UPDATE a SET a.TOTAL_COST = b.TOTAL_COST,a.TARGET_PRICE = b.TARGET_PRICE,a.YEAR_1 = b.YEAR_1,a.TAX = b.TAX,a.EXTENDED_PRICE = b.EXTENDED_PRICE FROM QT__SAQITM a INNER JOIN SAQITM b on a.SERVICE_ID = b.SERVICE_ID and a.QUOTE_ID = b.QUOTE_ID where a.QUOTE_RECORD_ID = '{QuoteRecordId}' """.format(QuoteRecordId= self.ContractRecordId)
						Sql.RunQuery(QueryStatement)
					else:						
						updateSAQICO = Sql.RunQuery("""UPDATE SAQICO
								SET ENTITLEMENT_PRICE_IMPACT = CASE
														WHEN EXCHANGE_RATE > 0 THEN ISNULL({price_impact}, 0) * ISNULL(EXCHANGE_RATE,0)
														ELSE {price_impact}
														END,
								ENTITLEMENT_COST_IMPACT = CASE
														WHEN EXCHANGE_RATE > 0 THEN ISNULL({cost_impact}, 0) * ISNULL(EXCHANGE_RATE,0)
														ELSE {cost_impact}
														END,
								TOTAL_COST = CASE  
														WHEN TOTAL_COST > 0 THEN ISNULL({cost_impact}, 0) + ISNULL(TOTAL_COST,0)
														ELSE TOTAL_COST
														END,
								TARGET_PRICE = CASE  
														WHEN TARGET_PRICE > 0 THEN TARGET_PRICE + (ISNULL(EXCHANGE_RATE, 0) * ISNULL({price_impact}, 0))
														ELSE TARGET_PRICE
													END,
								BD_PRICE = CASE  
													WHEN BD_PRICE > 0 THEN BD_PRICE + (ISNULL(EXCHANGE_RATE, 0) * ISNULL({price_impact}, 0))
													ELSE BD_PRICE
												END,  
								SALES_PRICE = CASE  
														WHEN SALES_PRICE > 0 THEN SALES_PRICE + (ISNULL(EXCHANGE_RATE, 0) * ISNULL({price_impact}, 0))
														ELSE SALES_PRICE
													END,
								SALES_DISCOUNT_PRICE = CASE  
														WHEN SALES_DISCOUNT_PRICE > 0 THEN SALES_DISCOUNT_PRICE + (ISNULL(EXCHANGE_RATE, 0) * ISNULL({price_impact}, 0))
														ELSE SALES_DISCOUNT_PRICE
													END,
								YEAR_1 = CASE  
													WHEN YEAR_1 > 0 THEN YEAR_1 + (ISNULL(EXCHANGE_RATE, 0) * ISNULL({price_impact}, 0))
													ELSE ISNULL(YEAR_1, 0)
												END,
								YEAR_2 = CASE  
													WHEN YEAR_2 > 0 THEN YEAR_2 + (ISNULL(EXCHANGE_RATE, 0) * ISNULL({price_impact}, 0))
													ELSE ISNULL(YEAR_2,0)
												END,
								YEAR_3 = CASE  
													WHEN ISNULL(YEAR_3,0) > 0 THEN YEAR_3 + (ISNULL(EXCHANGE_RATE, 0) * ISNULL({price_impact}, 0))
													ELSE ISNULL(YEAR_3,0)
												END,
								YEAR_4 = CASE  
													WHEN ISNULL(YEAR_4,0) > 0 THEN YEAR_4 + (ISNULL(EXCHANGE_RATE, 0) * ISNULL({price_impact}, 0))
													ELSE ISNULL(YEAR_4,0)
												END,
								YEAR_5 = CASE  
													WHEN ISNULL(YEAR_5,0) > 0 THEN YEAR_5 + (ISNULL(EXCHANGE_RATE, 0) * ISNULL({price_impact}, 0))
													ELSE ISNULL(YEAR_5,0)
												END,
								EXTENDED_PRICE = CASE 
															WHEN ISNULL(EXTENDED_PRICE,0) > 0 THEN
																								CASE  
																									WHEN ISNULL(YEAR_1, 0) > 0 THEN YEAR_1 + (ISNULL(EXCHANGE_RATE, 0) * ISNULL({price_impact}, 0))
																									ELSE ISNULL(YEAR_1, 0)
																								END +
																								CASE  
																									WHEN ISNULL(YEAR_2, 0) > 0 THEN YEAR_2 + (ISNULL(EXCHANGE_RATE, 0) * ISNULL({price_impact}, 0))
																									ELSE ISNULL(YEAR_2, 0)
																								END +
																								CASE  
																									WHEN ISNULL(YEAR_3,0) > 0 THEN YEAR_3 + (ISNULL(EXCHANGE_RATE, 0) * ISNULL({price_impact}, 0))
																									ELSE ISNULL(YEAR_3,0)
																								END +
																								CASE  
																									WHEN ISNULL(YEAR_4,0) > 0 THEN YEAR_4 + (ISNULL(EXCHANGE_RATE, 0) * ISNULL({price_impact}, 0))
																									ELSE ISNULL(YEAR_4,0)
																								END +
																								CASE  
																									WHEN ISNULL(YEAR_5,0) > 0 THEN YEAR_5 + (ISNULL(EXCHANGE_RATE, 0) * ISNULL({price_impact}, 0))
																									ELSE ISNULL(YEAR_5,0)
																								END
															ELSE ISNULL(EXTENDED_PRICE,0)
														END,
								PRICING_STATUS = CASE
														WHEN {price_impact} > 0 OR {cost_impact} > 0 THEN 'ACQUIRED'
														ELSE PRICING_STATUS
														END
								FROM SAQICO where
								{WhereCondition}
							AND PRICING_STATUS IN ('PARTIALLY PRICED','ACQUIRED') """.format(WhereCondition=whereReq,price_impact=totalpriceimpact,cost_impact=totalcostent))
						#Sql.RunQuery(updateSAQICO)
				else:					
					updateSAQICO = Sql.RunQuery("""UPDATE SAQICO
							SET ENTITLEMENT_PRICE_IMPACT = CASE
													WHEN EXCHANGE_RATE > 0 THEN ISNULL({price_impact}, 0) * ISNULL(EXCHANGE_RATE,0)
													ELSE {price_impact}
													END,
							ENTITLEMENT_COST_IMPACT = CASE
													WHEN EXCHANGE_RATE > 0 THEN ISNULL({cost_impact}, 0) * ISNULL(EXCHANGE_RATE,0)
													ELSE {cost_impact}
													END,
							TOTAL_COST = CASE  
													WHEN TOTAL_COST > 0 THEN ISNULL({cost_impact}, 0) + ISNULL(TOTAL_COST,0)
													ELSE TOTAL_COST
													END,
							TARGET_PRICE = CASE  
													WHEN TARGET_PRICE > 0 THEN TARGET_PRICE + (ISNULL(EXCHANGE_RATE, 0) * ISNULL({price_impact}, 0))
													ELSE TARGET_PRICE
												END,
							BD_PRICE = CASE  
												WHEN BD_PRICE > 0 THEN BD_PRICE + (ISNULL(EXCHANGE_RATE, 0) * ISNULL({price_impact}, 0))
												ELSE BD_PRICE
											END,  
							SALES_PRICE = CASE  
													WHEN SALES_PRICE > 0 THEN SALES_PRICE + (ISNULL(EXCHANGE_RATE, 0) * ISNULL({price_impact}, 0))
													ELSE SALES_PRICE
												END,
							SALES_DISCOUNT_PRICE = CASE  
													WHEN SALES_DISCOUNT_PRICE > 0 THEN SALES_DISCOUNT_PRICE + (ISNULL(EXCHANGE_RATE, 0) * ISNULL({price_impact}, 0))
													ELSE SALES_DISCOUNT_PRICE
												END,
							YEAR_1 = CASE  
												WHEN YEAR_1 > 0 THEN YEAR_1 + (ISNULL(EXCHANGE_RATE, 0) * ISNULL({price_impact}, 0))
												ELSE ISNULL(YEAR_1, 0)
											END,
							YEAR_2 = CASE  
												WHEN YEAR_2 > 0 THEN YEAR_2 + (ISNULL(EXCHANGE_RATE, 0) * ISNULL({price_impact}, 0))
												ELSE ISNULL(YEAR_2,0)
											END,
							YEAR_3 = CASE  
												WHEN ISNULL(YEAR_3,0) > 0 THEN YEAR_3 + (ISNULL(EXCHANGE_RATE, 0) * ISNULL({price_impact}, 0))
												ELSE ISNULL(YEAR_3,0)
											END,
							YEAR_4 = CASE  
												WHEN ISNULL(YEAR_4,0) > 0 THEN YEAR_4 + (ISNULL(EXCHANGE_RATE, 0) * ISNULL({price_impact}, 0))
												ELSE ISNULL(YEAR_4,0)
											END,
							YEAR_5 = CASE  
												WHEN ISNULL(YEAR_5,0) > 0 THEN YEAR_5 + (ISNULL(EXCHANGE_RATE, 0) * ISNULL({price_impact}, 0))
												ELSE ISNULL(YEAR_5,0)
											END,
							EXTENDED_PRICE = CASE 
														WHEN ISNULL(EXTENDED_PRICE,0) > 0 THEN
																							CASE  
																								WHEN ISNULL(YEAR_1, 0) > 0 THEN YEAR_1 + (ISNULL(EXCHANGE_RATE, 0) * ISNULL({price_impact}, 0))
																								ELSE ISNULL(YEAR_1, 0)
																							END +
																							CASE  
																								WHEN ISNULL(YEAR_2, 0) > 0 THEN YEAR_2 + (ISNULL(EXCHANGE_RATE, 0) * ISNULL({price_impact}, 0))
																								ELSE ISNULL(YEAR_2, 0)
																							END +
																							CASE  
																								WHEN ISNULL(YEAR_3,0) > 0 THEN YEAR_3 + (ISNULL(EXCHANGE_RATE, 0) * ISNULL({price_impact}, 0))
																								ELSE ISNULL(YEAR_3,0)
																							END +
																							CASE  
																								WHEN ISNULL(YEAR_4,0) > 0 THEN YEAR_4 + (ISNULL(EXCHANGE_RATE, 0) * ISNULL({price_impact}, 0))
																								ELSE ISNULL(YEAR_4,0)
																							END +
																							CASE  
																								WHEN ISNULL(YEAR_5,0) > 0 THEN YEAR_5 + (ISNULL(EXCHANGE_RATE, 0) * ISNULL({price_impact}, 0))
																								ELSE ISNULL(YEAR_5,0)
																							END
														ELSE ISNULL(EXTENDED_PRICE,0)
													END,
							PRICING_STATUS = CASE
													WHEN {price_impact} > 0 OR {cost_impact} > 0 THEN 'ACQUIRED'
													ELSE PRICING_STATUS
													END
							FROM SAQICO where
							{WhereCondition}
						AND PRICING_STATUS IN ('PARTIALLY PRICED','ACQUIRED') """.format(WhereCondition=whereReq,price_impact=totalpriceimpact,cost_impact=totalcostent))
					#Sql.RunQuery(updateSAQICO)

				'''UpdateEntitlement = " UPDATE {} SET CALCULATION_FACTOR={},ENTITLEMENT_COST_IMPACT={},ENTITLEMENT_PRICE_IMPACT={} WHERE ENTITLEMENT_NAME = '{}' AND {}  ".format(tableName,calc_factor,costimpact,priceimapct,AttributeID, whereReq)
				Sql.RunQuery(UpdateEntitlement)
				updatePricemethod = " UPDATE TGT SET TGT.PRICE_METHOD = SRC.PRICE_METHOD FROM PRENVL (NOLOCK) SRC JOIN {} (NOLOCK) TGT ON TGT.ENTITLEMENT_NAME = SRC.ENTITLEMENT_NAME WHERE SRC.ENTITLEMENT_NAME = '{}' AND {} ".format(tableName,AttributeID, whereReq)
				Sql.RunQuery(updatePricemethod)'''
				# to insert new input column value and price factor, cost impact for manual input end
			else:
				Trace.Write("---------------------------111111111"+str(ENT_IP_DICT))
				# to insert  input column value  start
				getvalue = ""
				updateentXML = getcostbaborimpact = getpriceimpact = ""
				
				for key,val in ENT_IP_DICT.items():
					if str((val).split("||")[4]).strip():
						getvalue = str((val).split("||")[4]).strip()
					decimal_place ="2"
					my_format = "{:." + str(decimal_place) + "f}"
					if getvalue:
						if str((val).split("||")[1]) == "CE":
							getcostbabor = Sql.GetFirst("select CE_COST,CE_PRICE from SAREGN where REGION='{}'".format(getregionval))
							if getcostbabor:
								getcostbaborimpact = str(float(getvalue)*float(getcostbabor.CE_COST))
								getpriceimpact = str(float(getvalue)*float(getcostbabor.CE_PRICE))
								getcostbaborimpact = str(my_format.format(round(float(getcostbaborimpact), int(decimal_place))))
								getpriceimpact = str(my_format.format(round(float(getpriceimpact), int(decimal_place))))
						elif str((val).split("||")[1]) == "Technician_or_3rd_Party":
							gettechlabor = Sql.GetFirst("select TECH_COST,TECH_PRICE from SAREGN where REGION='{}'".format(getregionval))
							if gettechlabor:
								getcostbaborimpact = str(float(getvalue)*float(gettechlabor.TECH_COST))
								getpriceimpact = str(float(getvalue)*float(gettechlabor.TECH_PRICE))
								getcostbaborimpact = str(my_format.format(round(float(getcostbaborimpact), int(decimal_place))))
								getpriceimpact = str(my_format.format(round(float(getpriceimpact), int(decimal_place))))
						elif str((val).split("||")[1]) == "PSE":
							getpselabor = Sql.GetFirst("select PSE_COST,PSE_PRICE from SAREGN where REGION='{}' ".format(getregionval))
							if getpselabor:
								getcostbaborimpact = str(float(getvalue)*float(getpselabor.PSE_COST))
								getpriceimpact = str(float(getvalue)*float(getpselabor.PSE_PRICE))
								getcostbaborimpact = str(my_format.format(round(float(getcostbaborimpact), int(decimal_place))))
								getpriceimpact = str(my_format.format(round(float(getpriceimpact), int(decimal_place))))
					else:
						getcostbaborimpact = ""
						getpriceimpact = ""
					factor_value = str((val).split("||")[4])
					#if 'AGS_LAB_OPT' in AttributeID and str((val).split("||")[1]).strip() == AttributeID:
					if  AttributeID and str((val).split("||")[1]).strip() == AttributeID:
						Trace.Write("AttributeID---904----"+str(AttributeID))
						Fullresponse,cpsmatc_incr,attribute_code = self.EntitlementRequest(cpsConfigID,cpsmatchID,AttributeID,str(NewValue),'input')
						Trace.Write("Fullresponse"+str(Fullresponse))
						Trace.Write("tableName--894---"+str(tableName))
						Trace.Write("cpsmatc_incr--894---"+str(cpsmatc_incr))
						Trace.Write("cpsConfigID--894---"+str(cpsConfigID))
						Trace.Write("whereReq--894---"+str(whereReq))

						Updatecps = "UPDATE {} SET CPS_MATCH_ID ={},CPS_CONFIGURATION_ID = '{}' WHERE {} ".format(tableName, cpsmatc_incr,cpsConfigID, whereReq)
						Sql.RunQuery(Updatecps)
						characteristics_attr_values = []
						for rootattribute, rootvalue in Fullresponse.items():
							if rootattribute == "rootItem":
								for Productattribute, Productvalue in rootvalue.items():
									if Productattribute == "variantConditions":
										characteristics_attr_values = Productvalue
									# if Productattribute == "characteristics":
									# 	for prdvalue in Productvalue:											
									# 		for attribute in prdvalue["values"]:
									# 			if prdvalue["id"] in characteristics_attr_values:
									# 				characteristics_attr_values[str(prdvalue["id"])].append(attribute["value"])
									# 			else:
									# 				characteristics_attr_values[str(prdvalue["id"])] = [attribute["value"]]
						Trace.Write("characteristics_attr_values"+str(characteristics_attr_values)+str(AttributeID))
						
						if characteristics_attr_values and 'AGS_LAB_OPT' in AttributeID:
							Trace.Write("serviceId---"+str(serviceId))
							attr_prices = self.get_product_attr_level_cps_pricing(characteristics_attr_values,serviceId)
							#Product.SetGlobal('attr_level_pricing',str(attr_prices))
							Trace.Write("attr_prices---908---"+str(attr_prices))
							if attr_prices:
								for attr, attr_value in attr_prices.items():
									data_dict = {'key':attr}
									Trace.Write("attr_prices--912=-----"+str(attr)+str(data_dict))
									data_dict.update(attr_value)
									attr_level_pricing.append(data_dict)
									#Trace.Write("attr_prices----"+str(attr))
									# data_dict = {'key':AttributeID}
									# data_dict.update(attr_value)
									# attr_level_pricing.append(data_dict)
						# if attr_level_pricing:
						# 	getcostbaborimpact = attr_level_pricing[0].get('total_price')
						# 	getpriceimpact = attr_level_pricing[0].get('price')		
						# 	factor_value = 	attr_level_pricing[0].get('factor')	
					updateentXML  += """<QUOTE_ITEM_ENTITLEMENT>
					<ENTITLEMENT_NAME>{ent_name}</ENTITLEMENT_NAME>
					<ENTITLEMENT_VALUE_CODE>{ent_val_code}</ENTITLEMENT_VALUE_CODE>
					<ENTITLEMENT_DISPLAY_VALUE>{ent_disp_val}</ENTITLEMENT_DISPLAY_VALUE>
					<ENTITLEMENT_COST_IMPACT>{ct}</ENTITLEMENT_COST_IMPACT>
					<ENTITLEMENT_PRICE_IMPACT>{pi}</ENTITLEMENT_PRICE_IMPACT>
					<IS_DEFAULT>{is_default}</IS_DEFAULT>
					<ENTITLEMENT_TYPE>{ent_type}</ENTITLEMENT_TYPE>
					<ENTITLEMENT_DESCRIPTION>{ent_desc}</ENTITLEMENT_DESCRIPTION>
					<PRICE_METHOD>{pm}</PRICE_METHOD>
					<CALCULATION_FACTOR>{cf}</CALCULATION_FACTOR>
					</QUOTE_ITEM_ENTITLEMENT>""".format(ent_name = str(key),ent_val_code = str((val).split("||")[0]),ent_disp_val = str((val).split("||")[0]),ct = getcostbaborimpact,pi = getpriceimpact,is_default = '0' if str(key)==AttributeID else '1',ent_type = str((val).split("||")[2]),ent_desc=str((val).split("||")[3]) ,pm = pricemethodupdate if str(key)==AttributeID else '',cf=factor_value)
				Trace.Write("---------------------------222222222222222"+str(updateentXML))
				UpdateEntitlement = " UPDATE {} SET ENTITLEMENT_XML= '{}' WHERE  {} ".format(tableName, updateentXML,whereReq)
				

				#Sql.RunQuery(UpdateEntitlement)	
				'''if getmaualipval:
					AttributeID = inputId
					NewValue = getmaualipval
				Trace.Write('335-------NewValue------------456----------'+str(NewValue))
				Trace.Write('335-------NewValue------------456----------'+str(NewValue))						
				UpdateEntitlement = " UPDATE {} SET ENTITLEMENT_DISPLAY_VALUE = '{}',IS_DEFAULT = '0' WHERE ENTITLEMENT_NAME = '{}' AND {}  ".format(
				tableName,NewValue,AttributeID, whereReq
				)
				Sql.RunQuery(UpdateEntitlement)'''
				# to insert  input column value end
			
		factcurreny = ""
		dataent = ""
		getedit_calc = Sql.GetFirst("SELECT PRICE_METHOD,DATA_TYPE as DT FROM PRENVL (NOLOCK) where ENTITLEMENT_NAME = 'ADDL_PERF_GUARANTEE_91_1' AND ENTITLEMENT_VALUE_CODE = 'MANUAL INPUT' ")
		if getedit_calc:
			if getedit_calc.PRICE_METHOD == "MANUAL PRICE":				
				dataent = getedit_calc.DT				
				# factcurr = Sql.GetFirst("select GLOBAL_CURRENCY as GS from SAQTMT (NOLOCK) where MASTER_TABLE_QUOTE_RECORD_ID = '{}'".format(str(self.ContractRecordId)))
				# if factcurr:
				# 	factcurreny = factcurr.GS
		return attributesdisallowedlst,attributesallowedlst,attributevalues,attributeReadonlylst,attributeEditonlylst,factcurreny, dataent, attr_level_pricing,dropdownallowlist,dropdowndisallowlist,attributedefaultvalue

	def EntitlementCancel(self,SectionRecordId, ENT_CANCEL, Getprevdict,subtabName,EquipmentId):		
		#Trace.Write('Cancel function--Getprevdict-----'+str(dict(Getprevdict)))
		gettotallist = Product.GetGlobal('ent_data_List')	
		## set entitlement_xml for cancel fn A055S000P01-3157
		getprevent_xml = Product.GetGlobal('previous_entitlement_xml')
		## set entitlement_xml for cancel fn A055S000P01-3157
		tableName = ''
		serviceId = ''
		parentObj = ''
		whereReq = ''
		ParentwhereReq = ''
		attributesdisallowedlst = attributesallowedlst =[]
		join =''	
		Trace.Write("getprevent_xml--> "+str(getprevent_xml))
		###tool relocation receiving entitilement starts
		if (self.treeparam.upper() == 'RECEIVING EQUIPMENT' or self.treeparentparam.upper() == 'RECEIVING EQUIPMENT' or self.treesuperparentparam.upper() == 'RECEIVING EQUIPMENT') and (self.treesuperparentparam == 'Other Products' or self.treetopsuperparentparam == 'Other Products' or self.treesupertopparentparam == 'Other Products' ):
			if self.treeparam.upper() == 'RECEIVING EQUIPMENT'  and subtabName == 'Entitlements':
				tableName = 'SAQTSE'
				serviceId = self.treeparentparam
				whereReq = "QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}' ".format(self.ContractRecordId,serviceId)
			elif self.treeparentparam.upper() == 'RECEIVING EQUIPMENT' and subtabName == 'Entitlements':
				tableName = 'SAQSFE'
				serviceId = self.treesuperparentparam 
				parentObj = 'SAQTSE'
				whereReq = "QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}' AND FABLOCATION_ID ='{}'".format(self.ContractRecordId,serviceId,self.treeparam)
				ParentwhereReq="QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}' ".format(self.ContractRecordId,serviceId)
			elif self.treesuperparentparam.upper() == 'RECEIVING EQUIPMENT'  and subtabName == 'Entitlements':
				tableName = 'SAQSGE'
				serviceId = self.treetopsuperparentparam
				parentObj = 'SAQTSE'
				#join = "JOIN SAQSFE ON SAQSFE.SERVICE_RECORD_ID = SAQSGE.SERVICE_RECORD_ID AND SAQSFE.QUOTE_RECORD_ID = SAQSGE.QUOTE_RECORD_ID AND SAQSFE.QUOTE_SERVICE_FAB_LOC_ENT_RECORD_ID = SAQSGE.QTSFBLENT_RECORD_ID "
				whereReq = "QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}' AND GREENBOOK ='{}' AND FABLOCATION_ID = '{}'".format(self.ContractRecordId,serviceId,self.treeparam,self.treeparentparam)
				ParentwhereReq="QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}' ".format(self.ContractRecordId,serviceId)
			elif self.treesuperparentparam.upper() == 'RECEIVING EQUIPMENT'  and subtabName == 'Equipment Entitlements':
				Trace.Write('331----treesuperparentparam----'+str(self.treesuperparentparam))
				Trace.Write('331----treetopsuperparentparam----'+str(self.treetopsuperparentparam))
				tableName = 'SAQSCE'
				#serviceId = self.treesuperparentparam
				serviceId = self.treetopsuperparentparam
				parentObj = 'SAQSGE'
				whereReq = "QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}' AND EQUIPMENT_ID = '{}' AND GREENBOOK ='{}' AND FABLOCATION_ID = '{}'".format(self.ContractRecordId,serviceId,EquipmentId,self.treeparam,self.treeparentparam)
				ParentwhereReq="QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}' AND GREENBOOK ='{}'".format(self.ContractRecordId,serviceId,self.treeparam)
		###tool relocation receiving entitilement ends
		else:
			##addon product condition is added
			if ((self.treesuperparentparam == 'Product Offerings' or (self.treeparentparam == 'Add-On Products' and self.treesupertopparentparam == 'Product Offerings')) and subtabName == 'Entitlements'):
				tableName = 'SAQTSE'
				serviceId = self.treeparam
				whereReq = "QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}' ".format(self.ContractRecordId,serviceId)
			elif ((self.treetopsuperparentparam == 'Product Offerings' or (self.treesuperparentparam == 'Add-On Products' and self.treesupertopparentparam == 'Comprehensive Services' )) and subtabName == 'Entitlements'):
				tableName = 'SAQSFE'
				serviceId = self.treeparentparam
				parentObj = 'SAQTSE'
				whereReq = "QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}' AND FABLOCATION_ID ='{}'".format(self.ContractRecordId,serviceId,self.treeparam)
				ParentwhereReq="QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}' ".format(self.ContractRecordId,serviceId)
			elif ((self.treesupertopparentparam == 'Product Offerings' or (self.treetopsuperparentparam == 'Add-On Products' and self.treetopsupertopparentparam == 'Comprehensive Services')) and subtabName == 'Entitlements' and self.treeparentparam != 'Add-On Products'):
				tableName = 'SAQSGE'
				parentObj = 'SAQTSE'
				serviceId = self.treeparentparam
				#join = "JOIN SAQSFE ON SAQSFE.SERVICE_RECORD_ID = SAQSGE.SERVICE_RECORD_ID AND SAQSFE.QUOTE_RECORD_ID = SAQSGE.QUOTE_RECORD_ID AND SAQSFE.QUOTE_SERVICE_FAB_LOC_ENT_RECORD_ID = SAQSGE.QTSFBLENT_RECORD_ID "
				whereReq = "QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}' AND GREENBOOK ='{}' AND FABLOCATION_ID = '{}'".format(self.ContractRecordId,serviceId,self.treeparam,self.treeparentparam)
				ParentwhereReq="QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}' ".format(self.ContractRecordId,serviceId)
			elif (self.treesupertopparentparam == 'Product Offerings' and subtabName == 'Equipment Entitlements'):
				tableName = 'SAQSCE'
				parentObj = 'SAQSGE'
				serviceId = self.treesuperparentparam
				whereReq = "QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}' AND GREENBOOK ='{}' AND EQUIPMENT_ID = '{}'".format(self.ContractRecordId,serviceId,self.treeparam,EquipmentId)
				ParentwhereReq="QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}' AND GREENBOOK ='{}'".format(self.ContractRecordId,serviceId,self.treeparam)
			elif (self.treesupertopparentparam == 'Product Offerings' and subtabName == 'Assembly Entitlements'):
				tableName = 'SAQSAE'
				serviceId = self.treesuperparentparam
				parentObj = 'SAQSCE'
				whereReq = "QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}' AND GREENBOOK ='{}' AND EQUIPMENT_ID = '{}' AND FABLOCATION_ID = '{}' AND ASSEMBLY_ID = '{}' ".format(self.ContractRecordId,serviceId,self.treeparam,EquipmentId,self.treeparentparam,AssemblyId)
				ParentwhereReq="QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}' AND GREENBOOK ='{}'".format(self.ContractRecordId,serviceId,self.treeparam)
			elif (self.treeparentparam == 'Quote Items' and subtabName == 'Entitlements'):
				tableName = 'SAQIEN'
				serviceId = (self.treeparam).split("-")[1].strip()				
			
		valdisplaycode = []
		Getprevdict = eval(str(Getprevdict))
		Trace.Write('Getprevdict----------'+str(Getprevdict))
		###added  3157
		#attId=AttributeID = valcode=""
		#cpsmatchID,cpsConfigID,oldConfigID = self.getcpsID(tableName,serviceId,parentObj,whereReq,attId,ParentwhereReq)
		#Fullresponse,cpsmatc_incrn = self.EntitlementRequest(cpsConfigID,cpsmatchID,AttributeID,valcode)
		#Trace.Write("Fullresponse-->cancel--"+ str(Fullresponse)+"cpsmatc_incrn"+str(cpsmatc_incrn))
		#Trace.Write("cpsmatchID--"+ str(cpsmatchID)+"cpsConfigID"+str(cpsConfigID)+"oldConfigID-- "+str(oldConfigID))
		## ends
		Gettabledata = Sql.GetFirst("SELECT * FROM {} (NOLOCK) WHERE {} ".format(tableName,whereReq))
		
		product_obj = Sql.GetFirst("""SELECT 
				MAX(PDS.PRODUCT_ID) AS PRD_ID,PDS.SYSTEM_ID,PDS.PRODUCT_NAME 
				FROM PRODUCTS PDS 
				INNER JOIN PRODUCT_VERSIONS PRVS ON  PDS.PRODUCT_ID = PRVS.PRODUCT_ID 
				WHERE SYSTEM_ID ='{SystemId}' 
				GROUP BY PDS.SYSTEM_ID,PDS.UnitOfMeasure,PDS.CART_DESCRIPTION_BUILDER,PDS.PRODUCT_NAME""".format(SystemId = str(Gettabledata.SERVICE_ID)))
		for AttributeID,valcode in dict(Getprevdict).items():
			Trace.Write(str(valcode)+'170-------'+str(AttributeID))
			if AttributeID not in ['T0_T1_LABOR_calc','T0_T1_LABOR_imt','T3_LABOR','T0_T1_LABOR','T3_LABOR_imt','T2_LABOR_calc','LABOR_TYPE_primp','T2_LABOR_TYPE_imt']:
				valdisplaycode.append(str(valcode))
				attId = "AND ENTITLEMENT_NAME = '{}' ".format(AttributeID)
				#Trace.Write("tableName--"+str(tableName)+'---'+str(serviceId)+'---'+str(whereReq))	
				cpsmatchID,cpsConfigID,oldConfigID = self.getcpsID(tableName,serviceId,parentObj,whereReq,attId,ParentwhereReq)
				get_datatype = Sql.GetFirst("""SELECT ATT_DISPLAY_DEFN.ATT_DISPLAY_DESC AS ATT_DISPLAY_DESC
												FROM TAB_PRODUCTS
												LEFT JOIN PAT_SCHEMA ON PAT_SCHEMA.TAB_PROD_ID=TAB_PRODUCTS.TAB_PROD_ID											
												LEFT JOIN PRODUCT_ATTRIBUTES ON PRODUCT_ATTRIBUTES.STANDARD_ATTRIBUTE_CODE = PAT_SCHEMA.STANDARD_ATTRIBUTE_CODE AND PRODUCT_ATTRIBUTES.PRODUCT_ID = TAB_PRODUCTS.PRODUCT_ID
												LEFT JOIN ATTRIBUTE_DEFN ON ATTRIBUTE_DEFN.STANDARD_ATTRIBUTE_CODE = PRODUCT_ATTRIBUTES.STANDARD_ATTRIBUTE_CODE
												LEFT JOIN ATT_DISPLAY_DEFN ON ATT_DISPLAY_DEFN.ATT_DISPLAY = PRODUCT_ATTRIBUTES.ATT_DISPLAY
												
												WHERE TAB_PRODUCTS.PRODUCT_ID = {ProductId} AND SYSTEM_ID = '{service_id}'""".format(ProductId = product_obj.PRD_ID,service_id = AttributeID ))
				if get_datatype:
					Fullresponse,cpsmatc_incr,attribute_code = self.EntitlementRequest(cpsConfigID,cpsmatchID,AttributeID,valcode,get_datatype.ATT_DISPLAY_DESC)
				else:
					Fullresponse,cpsmatc_incr,attribute_code = self.EntitlementRequest(cpsConfigID,cpsmatchID,AttributeID,valcode)
				#Trace.Write("Cancel - new cps match Id: "+str(cpsmatc_incr))
				attributesdisallowedlst = []
				attributesallowedlst = []
				attributeReadonlylst = []
				attributeEditonlylst = []
				attributedefaultvalue = []
				attributevalues = {}			
				for rootattribute, rootvalue in Fullresponse.items():
					if rootattribute == "rootItem":
						for Productattribute, Productvalue in rootvalue.items():
							if Productattribute == "characteristics":
								for prdvalue in Productvalue:
									if prdvalue["visible"] == "false":
										#Trace.Write(prdvalue["id"] + " set here")
										attributesdisallowedlst.append(prdvalue["id"])
									if prdvalue["visible"] == "true":
										#Trace.Write(prdvalue["id"] + " set here")
										attributesallowedlst.append(prdvalue["id"])
									if prdvalue["readOnly"] == "true":
										attributeReadonlylst.append(prdvalue["id"])
									if prdvalue["readOnly"] == "false":
										attributeEditonlylst.append(prdvalue["id"])
									for attribute in prdvalue["values"]:
										#Trace.Write("attribute---"+str(attribute))
										attributevalues[str(prdvalue["id"])] = attribute["value"]
										if attribute["author"] == "Default":
											attributedefaultvalue.append(prdvalue["id"])
				ServiceContainer = Product.GetContainerByName("Services")
				sec_name =""
				# for row in ServiceContainer.Rows:
				# 	#Trace.Write(row.Product.PartNumber)
				# 	#Trace.Write('--------99-----'+str(SectionRecordId))
				# 	if self.treeparam.upper() == str(row.Product.PartNumber).upper() or self.treeparentparam.upper() == str(row.Product.PartNumber).upper() or self.treesuperparentparam.upper() == str(row.Product.PartNumber).upper():
				# 		ContainerProduct = row.Product
				# 		tabs = ContainerProduct.Tabs
				# 		list_of_tabs = []
				# 		for tab in tabs:
				# 			list_of_tabs.append(tab.Name)
				# 			sysectObj = Sql.GetFirst(
				# 				"SELECT SECTION_DESC,SECTION_NAME FROM SYSECT (NOLOCK) WHERE RECORD_ID='" + str(SectionRecordId) + "'"
				# 			)
				# 			if sysectObj:
				# 				sec_name = sysectObj.SECTION_NAME
				# 				if sec_name == str(tab.Name):
				# 					for attr in tab.Attributes:
				# 						#Trace.Write(attr.Name)
				# 						attrName = attr.Name
				# 						attrLabel = attr.Name
				# 						attrValue = attr.GetValue()
				# 						attrSysId = attr.SystemId
				# 						DType = attr.DisplayType
				# 						#Trace.Write("attrSysId-1494-------" + str(attrSysId))
				# 						#Trace.Write("attrValue--1494-------" + str(attrValue))
				# 						#Trace.Write("DType-1494-------------" + str(DType))
				# 						#Trace.Write("attrName-------1659-----" + str(attrName))
				# 						#Trace.Write("attrLabel-------1659-----" + str(attrLabel))
				# 						if attrSysId in attributesdisallowedlst:
				# 							add_style = "display:none"
											
				# 						attrValueSysId = attributevalues.get(attrSysId)
				# 						if DType in ("DropDown", "CheckBox"):
				# 							Count = 0
				# 							for value in attr.Values:
				# 								if attrValueSysId == value.ValueCode:										
				# 									attrValue = value.Display
				# 						attrValue = attrValue.replace("'","''")									
				
				#Trace.Write(str(AttributeID)+"-------attributesallowedlst--------"+str(attributesallowedlst))
				AttributeValCoderes =  attributevalues.get(str(AttributeID))
				#Trace.Write("attributevalues--------"+str(attributevalues))			
				#Trace.Write("AttributeValCoderes--------"+str(AttributeValCoderes))			
				#updated cps response while clicking cancel in UI
				#UpdateEntitlement = " UPDATE {} SET ENTITLEMENT_DISPLAY_VALUE = '{}', ENTITLEMENT_VALUE_CODE = '{}',CPS_MATCH_ID ={} WHERE ENTITLEMENT_NAME = '{}' AND {}  ".format(
				#	tableName,valcode, AttributeValCoderes, cpsmatc_incr,AttributeID, whereReq
				#)
				#Trace.Write("UpdateEntitlement--"+ str(UpdateEntitlement)+"valcode"+str(valcode))
				#Sql.RunQuery(UpdateEntitlement)
				#Updatecps = "UPDATE {} SET CPS_MATCH_ID ={} WHERE QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}'".format(tableName, cpsmatc_incr, self.ContractRecordId, serviceId)
				#Sql.RunQuery(Updatecps)
				## set entitlement_xml for cancel fn A055S000P01-3157 starts
				if getprevent_xml:
					UpdateEntitlement = " UPDATE {} SET ENTITLEMENT_XML = '{}',CPS_MATCH_ID ={} WHERE {}  ".format(
							tableName,getprevent_xml,cpsmatc_incr,whereReq
						)
					#Trace.Write("UpdateEntitlement--"+ str(UpdateEntitlement))
					Sql.RunQuery(UpdateEntitlement)	
				####to update match id at all level while cancelling starts
				ent_tables_list = ['SAQTSE','SAQSFE','SAQSGE','SAQSCE','SAQSAE']
				#ent_tables_list.remove(tableName)
				for table in ent_tables_list:
					Updatecps = "UPDATE {} SET CPS_MATCH_ID ={} WHERE QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}'".format(table, cpsmatc_incr, self.ContractRecordId, serviceId)
					Sql.RunQuery(Updatecps)
				##to update match id at all level while cancelling ends

				## set entitlement_xml for cancel fn A055S000P01-3157 ends	
				GetDefault = Sql.GetFirst("SELECT * FROM PRENVL WHERE ENTITLEMENT_NAME = '{}' AND ENTITLEMENT_DISPLAY_VALUE = '{}'".format(AttributeID,valcode))
				if GetDefault:
					if GetDefault.IS_DEFAULT == 0:
						defaultval = 0
					else:
						defaultval = 1
					UpdateIsdefault = " UPDATE {} SET IS_DEFAULT = '{}' WHERE ENTITLEMENT_NAME = '{}' AND {}  ".format(
					tableName,defaultval,AttributeID, whereReq
					)
					Sql.RunQuery(UpdateIsdefault)
		if tableName == 'SAQTSE':
			where = "WHERE TGT.QUOTE_RECORD_ID = '{}' AND TGT.SERVICE_ID = '{}' ".format(self.ContractRecordId, serviceId)
		elif tableName == 'SAQSFE':
			where = " WHERE TGT.QUOTE_RECORD_ID = '{}' AND TGT.SERVICE_ID = '{}' AND SRC.FABLOCATION_ID ='{}'".format(self.ContractRecordId, serviceId, self.treeparam)
		elif tableName == 'SAQSGE':
			where = "WHERE TGT.QUOTE_RECORD_ID = '{}' AND TGT.SERVICE_ID = '{}' AND TGT.GREENBOOK ='{}'".format(self.ContractRecordId, serviceId, self.treeparam)
		else:
			where = "WHERE TGT.QUOTE_RECORD_ID = '{}' AND TGT.SERVICE_ID = '{}' AND TGT.GREENBOOK ='{}' AND TGT.EQUIPMENT_ID = '{}'".format(self.ContractRecordId, serviceId, self.treeparam,EquipmentId)		
		#self.ent_update(tableName,valcode, AttributeValCoderes, cpsmatc_incr,ConfigurationId,where)
		Trace.Write("Updated Successfully!!")
		#Trace.Write('response2--Fullresponse--------'+str(Fullresponse))
		#Trace.Write("valdisplaycode--------"+str(valdisplaycode))
		'''try:			
			CQENTIFLOW.iflow_entitlement(tableName,where)
		except Exception, e:
			Trace.Write("ENTITLEMENT IFLOW ERROR! "+str(e))
			Log.Info("ENTITLEMENT IFLOW ERROR! "+str(e))'''
		return attributesdisallowedlst,attributesallowedlst,attributevalues,attributeReadonlylst,attributeEditonlylst,valdisplaycode,attributedefaultvalue
	def Rolldown(self):
		#Log.Info("Newdict------523----> "+str(Newdict))
		try:
			Log.Info("Newdict-----745---> "+str(Newdict))
			AttributeList = ','.join(map(str, Newdict))
		except:
			Log.Info("Newdict----748--> "+str(Newdict))
			AttributeList = ','.join(map(int, Newdict))
		Log.Info("Attr List-> "+str(AttributeList))
		try:
			Getprevdict = eval(Param.getprevdict)
		except:
			Getprevdict = {}
		###tool relocation receiving entitilement starts
		if (self.treeparam.upper() == 'RECEIVING EQUIPMENT' or self.treeparentparam.upper() == 'RECEIVING EQUIPMENT' or self.treesuperparentparam.upper() == 'RECEIVING EQUIPMENT') and (self.treesuperparentparam == 'Other Products' or self.treetopsuperparentparam == 'Other Products' or self.treesupertopparentparam == 'Other Products' ):
			if self.treeparam.upper() == 'RECEIVING EQUIPMENT'  and subtabName == 'Entitlements':
				objName = 'SAQTSE'
				serviceId = self.treeparentparam
				where = "WHERE SRC.QUOTE_RECORD_ID = '{}' AND SRC.SERVICE_ID = '{}' ".format(self.ContractRecordId, serviceId)
			elif self.treeparentparam.upper() == 'RECEIVING EQUIPMENT' and subtabName == 'Entitlements':
				objName = 'SAQSFE'
				serviceId = self.treesuperparentparam 
				where = " WHERE SRC.QUOTE_RECORD_ID = '{}' AND SRC.SERVICE_ID = '{}' AND SRC.FABLOCATION_ID ='{}'".format(self.ContractRecordId, serviceId, self.treeparam)
			elif self.treesuperparentparam.upper() == 'RECEIVING EQUIPMENT'  and subtabName == 'Entitlements':
				objName = 'SAQSGE'
				serviceId = self.treetopsuperparentparam
				where = "WHERE SRC.QUOTE_RECORD_ID = '{}' AND SRC.SERVICE_ID = '{}' AND SRC.GREENBOOK ='{}' AND SRC.FABLOCATION_ID = '{}'".format(self.ContractRecordId, serviceId, self.treeparam,self.treeparentparam)
			elif self.treesuperparentparam.upper() == 'RECEIVING EQUIPMENT'  and subtabName == 'Equipment Entitlements':
				Trace.Write('331----treesuperparentparam----'+str(self.treesuperparentparam))
				Trace.Write('331----treetopsuperparentparam----'+str(self.treetopsuperparentparam))
				objName = 'SAQSCE'
				#serviceId = self.treesuperparentparam
				serviceId = self.treetopsuperparentparam
				parentObj = 'SAQSGE'
				where = " WHERE QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}' AND EQUIPMENT_ID = '{}' AND GREENBOOK ='{}' AND FABLOCATION_ID = '{}'".format(self.ContractRecordId,serviceId,EquipmentId,self.treeparam,self.treeparentparam)
				ParentwhereReq="QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}' AND GREENBOOK ='{}'".format(self.ContractRecordId,serviceId,self.treeparam)
		###tool relocation receiving entitilement ends
		else:
			##addon product condition is added
			if ((self.treesuperparentparam == 'Product Offerings' or (self.treeparentparam == 'Add-On Products' and self.treesupertopparentparam == 'Product Offerings')) and subtabName == 'Entitlements'):
				objName = 'SAQTSE'
				serviceId = self.treeparam
				where = "WHERE SRC.QUOTE_RECORD_ID = '{}' AND SRC.SERVICE_ID = '{}' ".format(self.ContractRecordId, serviceId)
			elif ((self.treetopsuperparentparam == 'Product Offerings' or (self.treesuperparentparam == 'Add-On Products' and self.treesupertopparentparam == 'Comprehensive Services' )) and subtabName == 'Entitlements'):
				objName = 'SAQSFE'
				serviceId = self.treeparentparam
				where = " WHERE SRC.QUOTE_RECORD_ID = '{}' AND SRC.SERVICE_ID = '{}' AND SRC.FABLOCATION_ID ='{}'".format(self.ContractRecordId, serviceId, self.treeparam)
			elif ((self.treesupertopparentparam == 'Product Offerings' or (self.treetopsuperparentparam == 'Add-On Products' and self.treetopsupertopparentparam == 'Comprehensive Services')) and subtabName == 'Entitlements' and self.treeparentparam != 'Add-On Products'):
				#Trace.Write("inside---25--"+str(self.treesuperparentparam))
				objName = 'SAQSGE'			
				serviceId = self.treesuperparentparam
				where = "WHERE SRC.QUOTE_RECORD_ID = '{}' AND SRC.SERVICE_ID = '{}' AND SRC.GREENBOOK ='{}' AND SRC.FABLOCATION_ID = '{}'".format(self.ContractRecordId, serviceId, self.treeparam,self.treeparentparam)
			elif (self.treesupertopparentparam == 'Product Offerings' and subtabName == 'Equipment Entitlements'):
				objName = 'SAQSCE'			
				serviceId = self.treesuperparentparam
				where = "WHERE SRC.QUOTE_RECORD_ID = '{}' AND SRC.SERVICE_ID = '{}'  AND SRC.EQUIPMENT_ID = '{}' AND SRC.GREENBOOK ='{}' AND SRC.FABLOCATION_ID = '{}'".format(self.ContractRecordId, serviceId,EquipmentId,self.treeparam,self.treeparentparam)
			elif (self.treesupertopparentparam == 'Product Offerings' and subtabName == 'Assembly Entitlements'):
				tableName = 'SAQSAE'
				serviceId = self.treesuperparentparam
				parentObj = 'SAQSCE'
				whereReq = "WHERE SRC.QUOTE_RECORD_ID = '{}' AND SRC.SERVICE_ID = '{}' AND SRC.GREENBOOK ='{}' AND SRC.EQUIPMENT_ID = '{}' AND SRC.FABLOCATION_ID = '{}' AND SRC.ASSEMBLY_ID = '{}' ".format(self.ContractRecordId,serviceId,self.treeparam,EquipmentId,self.treeparentparam,AssemblyId)
				ParentwhereReq="QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}' AND GREENBOOK ='{}'".format(self.ContractRecordId,serviceId,self.treeparam)
		
		

		Trace.Write("ENT_IP_DICT---"+str(ENT_IP_DICT))
		if ENT_IP_DICT != '':
			Trace.Write("ENT_IP_DICT-inside--"+str(ENT_IP_DICT))
			Log.Info("inside Attr List------> "+str(AttributeList))
			tableName = str(objName) +"="+str(AttributeList)+"="+str(User.Id)+","+str(Quote.GetGlobal("contract_quote_record_id"))
			SAQITMwhere = "WHERE A.QUOTE_RECORD_ID = '{}' AND A.SERVICE_ID = '{}'".format(self.ContractRecordId, serviceId)
			where = str(where)+","+str(SAQITMwhere)+","+str(sectionid)
			Trace.Write("where---"+str(where))
			Trace.Write("Getprevdict---"+str(Getprevdict))
			Trace.Write("tableName---"+str(tableName))
			Getprevdict = str(Getprevdict).replace("&","&#38;")
			try:			
				CQENTIFLOW.iflow_entitlement(tableName,where,Getprevdict)
			except Exception as e:
				#Trace.Write("ENTITLEMENT IFLOW ERROR! "+str(e))
				Log.Info("ENTITLEMENT IFLOW ERROR! "+str(e))
		
		return True

	def popup(self):
		sec_str = ""
		sec_str += """<div id="container_service" class="drop-boxes" style="display: none;">
					<div class="col-md-3 pl-0 rolling_popup">
					<div class="col-md-2 p-0">
						<img src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/info_icon.svg" class="img-responsive center-block">
					</div>
					<div class="col-md-10 p-0">
						<h3>Service Entitlement Updates <button data-dismiss="modal" type="button"
					class="close"
					aria-label="Close" onclick="close_popup()"> 
				<span aria-hidden="true">&times;</span> 
			</button></h3>
					<p>The Entitlement settings are being applied to the Equipment in this quote. You will be notified by email when this background job completes.</p>
					</div>
					</div>
					</div>"""
		return sec_str

	
try:
	AttributeID = Param.attributeId
except:	
	AttributeID = ""	
try:
	NewValue = Param.current
except:
	NewValue = ""
try:
	PrevValue = Param.prev
except:
	PrevValue =""
try:
	AttributeValCode = Param.attvalcode
except:
	AttributeValCode =""
try:
	subtabName = Param.subtabName
except:
	subtabName = ""
try:
	SectionRecordId = Param.SectionRecordId
except:
	SectionRecordId = ""
try:
	sectionid = Param.sectionid
except:
	sectionid =""
try:	
	ENT_CANCEL = Param.ENT_CANCEL
except:
	ENT_CANCEL = ""	
try:
	EntitlementType = Param.EntitlementType
	Trace.Write('EntitlementType---1032----'+str(EntitlementType))
except:
	EntitlementType = ""
	Trace.Write('EntitlementType---1035----'+str(EntitlementType))
try:
	EquipmentId = Param.EquipmentId
except:
	EquipmentId = ""
try:
	AssemblyId = Param.AssemblyId
except:
	AssemblyId = ""
try:
	ACTION = Param.ACTION
except:
	ACTION = ""
try:
	Newdict = Param.newdict
	#Log.Info('852-----------------'+str(Newdict))
except:
	Newdict = ""
	#Log.Info('852---------inside except--------'+str(Newdict))
try:
	Getprevdict = Param.getprevdict
except:
	Getprevdict = {}
try:
	calc_factor = Param.calc_factor
except:
	calc_factor = 'NULL'
try:
	costimpact = Param.costimpact
except:
	costimpact = 'NULL'
try:
	priceimapct = Param.priceimapct
except:
	priceimapct = 'NULL'
try:
	getmaualipval = Param.getmaualipval
except:
	getmaualipval = ''
try:
	inputId = Param.inputId
except:
	inputId = ''
try:
	ENT_IP_DICT = dict(Param.ENT_IP_DICT)
	Trace.Write('ENT_IP_DICT----'+str(ENT_IP_DICT))
except:
	Trace.Write('ENT_IP_DICT--except--')
	ENT_IP_DICT = ''
try:
	multiselect_flag = Param.multiselect_flag
except:
	multiselect_flag =''		
Trace.Write("subtabName : " + str(subtabName)+".. EntitlementType : "+str(EntitlementType)+"Action : "+str(ACTION))
#Trace.Write("calc_factor : " + str(calc_factor) + " costimpact : " + str(costimpact) + " priceimapct "+str(priceimapct))
#Trace.Write("AttributeID : " + str(AttributeID) + " AttributeValCode : " + str(AttributeValCode))
EntObj = Entitlements()
if ENT_CANCEL == 'CANCEL':
	ApiResponse = ApiResponseFactory.JsonResponse(
		EntObj.EntitlementCancel(SectionRecordId, ENT_CANCEL, Getprevdict,subtabName,EquipmentId)
	)
elif ACTION == 'POPUP':
	ApiResponse = ApiResponseFactory.JsonResponse(EntObj.popup())
elif ACTION == 'SAVE':
	Trace.Write("calling save")
	ApiResponse = ApiResponseFactory.JsonResponse(EntObj.Rolldown())
else:
	Trace.Write("calling else save")
	ApiResponse = ApiResponseFactory.JsonResponse(
		EntObj.EntitlementSave(subtabName, PrevValue, NewValue, AttributeID, AttributeValCode,SectionRecordId,EquipmentId,calc_factor,costimpact,priceimapct,getmaualipval,ENT_IP_DICT)
	)

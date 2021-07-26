# =========================================================================================================================================
#   __script_name : SYBLKETRLG.PY
#   __script_description : THIS SCRIPT IS USED FOR BULK EDITING RECORDS IN A RELATED LIST.
#   __primary_author__ : JOE EBENEZER
#   __create_date :
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import datetime
import System.Net
import Webcom.Configurator.Scripting.Test.TestProduct
import SYTABACTIN as Table
import SYCNGEGUID as CPQID
import CQTVLDRIFW
from SYDATABASE import SQL


Sql = SQL()
ContractRecordId = sqlforupdatePT = ""
try:
	ContractRecordId = Quote.GetGlobal("contract_quote_record_id")
except:
	ContractRecordId = ""
try:	
	Qt_rec_id = Quote.GetGlobal("contract_quote_record_id")
except:
	Qt_rec_id = ""

userId = str(User.Id)
userName = str(User.UserName)



def getting_cps_tax(quote_id = None,quote_record_id = None,item_lines_record_ids=None):		
	Log.Info("getting_cps_tax function"+str(item_lines_record_ids))
	webclient = System.Net.WebClient()
	webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/json"
	webclient.Headers[System.Net.HttpRequestHeader.Authorization] = "Basic c2ItYzQwYThiMWYtYzU5NS00ZWJjLTkyYzYtYzM4ODg4ODFmMTY0IWIyNTAzfGNwc2VydmljZXMtc2VjdXJlZCFiMzkxOm9zRzgvSC9hOGtkcHVHNzl1L2JVYTJ0V0FiMD0=";
	response = webclient.DownloadString("https://cpqprojdevamat.authentication.us10.hana.ondemand.com:443/oauth/token?grant_type=client_credentials")
	response = eval(response)
	
	Request_URL="https://cpservices-pricing.cfapps.us10.hana.ondemand.com/api/v1/statelesspricing"
	webclient.Headers[System.Net.HttpRequestHeader.Authorization] ="Bearer "+str(response['access_token'])

	x = datetime.datetime.today()
	x= str(x)
	y = x.split(" ")
	GetPricingProcedure = Sql.GetFirst("SELECT ISNULL(EXCHANGE_RATE_TYPE,'') as EXCHANGE_RATE_TYPE, ISNULL(DIVISION_ID, '') as DIVISION_ID, ISNULL(DISTRIBUTIONCHANNEL_ID, '') as DISTRIBUTIONCHANNEL_ID, ISNULL(SALESORG_ID, '') as SALESORG_ID, ISNULL(SORG_CURRENCY,'') as SORG_CURRENCY, ISNULL(PRICINGPROCEDURE_ID,'') as PRICINGPROCEDURE_ID, QUOTE_RECORD_ID, ISNULL(CUSTAXCLA_ID,1) as CUSTAXCLA_ID FROM SAQTSO (NOLOCK) WHERE QUOTE_ID = '{}'".format(quote_id))
	if GetPricingProcedure is not None:			
		PricingProcedure = GetPricingProcedure.PRICINGPROCEDURE_ID
		curr = GetPricingProcedure.SORG_CURRENCY
		dis = GetPricingProcedure.DISTRIBUTIONCHANNEL_ID
		salesorg = GetPricingProcedure.SALESORG_ID
		div = GetPricingProcedure.DIVISION_ID
		exch = GetPricingProcedure.EXCHANGE_RATE_TYPE
		taxk1 = GetPricingProcedure.CUSTAXCLA_ID

	#update_SAQITM = "UPDATE SAQITM SET PRICINGPROCEDURE_ID = '{prc}' WHERE SAQITM.QUOTE_ID = '{quote}'".format(prc=str(PricingProcedure), quote=self.contract_quote_id)
	#Sql.RunQuery(update_SAQITM)		
	
	STPObj=Sql.GetFirst("SELECT ACCOUNT_ID FROM SAOPQT (NOLOCK) WHERE QUOTE_ID ='{quote}'".format(quote=quote_id))		
	stp_account_id = ""
	if STPObj:
		stp_account_id = str(STPObj.ACCOUNT_ID)
	if item_lines_record_ids:		
		Log.Info("getting_cps_tax function item_lines_record_ids")	
		items_data = []
		item_line_record_ids_str = "','".join([item_line_record_id for item_line_record_id in item_lines_record_ids])
		item_lines_obj = Sql.GetList("SELECT * FROM SAQICO (NOLOCK) WHERE QUOTE_ITEM_COVERED_OBJECT_RECORD_ID IN ('{item_line_record_ids_str}')".format(item_line_record_ids_str = item_line_record_ids_str))
		if item_lines_obj:
			Log.Info("getting_cps_tax function item_lines_obj")	
			for item_line_obj in item_lines_obj:
				itemid = str(item_line_obj.EQUIPMENT_ID)+";"+str(quote_id)+";"+str(1)
				item_string = '{"itemId":"'+str(itemid)+'","externalId":null,"quantity":{"value":'+str(1)+',"unit":"EA"},"exchRateType":"'+str(exch)+'","exchRateDate":"'+str(y[0])+'","productDetails":{"productId":"'+str(item_line_obj.EQUIPMENT_ID)+'","baseUnit":"EA","alternateProductUnits":null},"attributes":[{"name":"KOMK-LAND1","values":["CN"]},{"name":"KOMK-ALAND","values":["CN"]},{"name":"KOMK-REGIO","values":["TX"]},{"name":"KOMK-KUNNR","values":["'+stp_account_id+'"]},{"name":"KOMK-KUNWE","values":["'+stp_account_id+'"]},{"name":"KOMP-TAXM1","values":["'+str(item_line_obj.SRVTAXCLA_ID)+'"]},{"name":"KOMK-TAXK1","values":["'+str(taxk1)+'"]},{"name":"KOMK-SPART","values":["'+str(div)+'"]},{"name":"KOMP-SPART","values":["'+str(div)+'"]},{"name":"KOMP-PMATN","values":["'+str(item_line_obj.EQUIPMENT_ID)+'"]},{"name":"KOMK-WAERK","values":["'+str(curr)+'"]},{"name":"KOMK-HWAER","values":["'+str(curr)+'"]},{"name":"KOMP-PRSFD","values":["X"]},{"name":"KOMK-VTWEG","values":["'+str(dis)+'"]},{"name":"KOMK-VKORG","values":["'+str(salesorg)+'"]},{"name":"KOMP-KPOSN","values":["0"]},{"name":"KOMP-KZNEP","values":[""]},{"name":"KOMP-ZZEXE","values":["true"]}],"accessDateList":[{"name":"KOMK-PRSDT","value":"'+str(y[0])+'"},{"name":"KOMK-FBUDA","value":"'+str(y[0])+'"}],"variantConditions":[],"statistical":true,"subItems":[]}'
				items_data.append(item_string)
			items_string = ','.join(items_data)
			requestdata = '{"docCurrency":"'+curr+'","locCurrency":"'+curr+'","pricingProcedure":"'+PricingProcedure+'","groupCondition":false,"itemConditionsRequired":true,"items": ['+str(items_string)+']}'
			Log.Info("requestdata-----",requestdata)
			response1 = webclient.UploadString(Request_URL,str(requestdata))			
			response1 = str(response1).replace(": true", ': "true"').replace(": false", ': "false"').replace(": null",': " None"')
			response1 = eval(response1)
			price = []
			for root, value in response1.items():
				if root == "items":
					price = value[:]
					break
			update_data = []
			batch_group_record_id = str(Guid.NewGuid()).upper()
			for data in price:
				equipment_id = str(data["itemId"]).split(";")[0]
				tax_percentage = 0
				for condition_obj in data['conditions']:
					if condition_obj['conditionType'] == 'ZWSC' and condition_obj['conditionTypeDescription'] == 'VAT Asia':
						tax_percentage = condition_obj['conditionRate']
						break
				update_data.append((str(Guid.NewGuid()).upper(), equipment_id, 1, 'IN PROGRESS', quote_id, quote_record_id, batch_group_record_id, tax_percentage))
			
			update_data_joined = ', '.join(map(str, update_data))
			Sql.RunQuery("""INSERT INTO SYSPBT(BATCH_RECORD_ID, SAP_PART_NUMBER, QUANTITY, BATCH_STATUS, QUOTE_ID, QUOTE_RECORD_ID, BATCH_GROUP_RECORD_ID, TAX_PERCENTAGE) 
									SELECT * FROM (VALUES {}) QS (BATCH_RECORD_ID, SAP_PART_NUMBER, QUANTITY, BATCH_STATUS, QUOTE_ID, QUOTE_RECORD_ID, BATCH_GROUP_RECORD_ID, TAX_PERCENTAGE)""".format(update_data_joined))											
			Sql.RunQuery("""UPDATE SAQICO
					SET
					SAQICO.TAX_PERCENTAGE = IQ.TAX_PERCENTAGE
					FROM SAQICO
					INNER JOIN (
						SELECT SAQICO.CpqTableEntryId, SYSPBT.TAX_PERCENTAGE
						FROM SYSPBT (NOLOCK) 
						JOIN SAQICO (NOLOCK) ON SAQICO.QUOTE_RECORD_ID = SYSPBT.QUOTE_RECORD_ID AND SAQICO.EQUIPMENT_ID = SYSPBT.SAP_PART_NUMBER						
						WHERE SYSPBT.QUOTE_RECORD_ID ='{QuoteRecordId}' AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}' AND SYSPBT.BATCH_STATUS = 'IN PROGRESS'								
					)AS IQ
					ON SAQICO.CpqTableEntryId = IQ.CpqTableEntryId""".format(BatchGroupRecordId=batch_group_record_id, QuoteRecordId=quote_record_id))

			Sql.RunQuery(
					"""DELETE FROM SYSPBT WHERE SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}' and SYSPBT.BATCH_STATUS = 'IN PROGRESS'""".format(
						BatchGroupRecordId=batch_group_record_id
					)
				)
			#update TAX column  and Extended price for each SAQICO records
			QueryStatement ="""UPDATE a SET a.TAX = CASE WHEN a.TAX_PERCENTAGE > 0 THEN (ISNULL(a.YEAR_1, 0)+ISNULL(a.YEAR_2, 0)+ISNULL(a.YEAR_3, 0)+ISNULL(a.YEAR_4, 0)+ISNULL(a.YEAR_5, 0)) * (a.TAX_PERCENTAGE/100) ELSE a.TAX_PERCENTAGE END FROM SAQICO a INNER JOIN SAQICO b on a.EQUIPMENT_ID = b.EQUIPMENT_ID and a.QUOTE_ID = b.QUOTE_ID where a.QUOTE_RECORD_ID = '{QuoteRecordId}' and a.QUOTE_ITEM_COVERED_OBJECT_RECORD_ID IN ('{item_line_record_ids_str}') """.format(			
			item_line_record_ids_str = item_line_record_ids_str,
			QuoteRecordId=Quote.GetGlobal("contract_quote_record_id"),
			)
			Sql.RunQuery(QueryStatement)
			QueryStatement ="""UPDATE a SET a.EXTENDED_PRICE = CASE WHEN a.TAX > 0 THEN (ISNULL(a.YEAR_1, 0)+ISNULL(a.YEAR_2, 0)+ISNULL(a.YEAR_3, 0)+ISNULL(a.YEAR_4, 0)+ISNULL(a.YEAR_5, 0)) + (a.TAX) ELSE a.TAX END FROM SAQICO a INNER JOIN SAQICO b on a.EQUIPMENT_ID = b.EQUIPMENT_ID and a.QUOTE_ID = b.QUOTE_ID where a.QUOTE_RECORD_ID = '{QuoteRecordId}' and a.QUOTE_ITEM_COVERED_OBJECT_RECORD_ID IN ('{item_line_record_ids_str}')""".format(
			QuoteRecordId=Quote.GetGlobal("contract_quote_record_id"),
			item_line_record_ids_str = item_line_record_ids_str
			)
			Sql.RunQuery(QueryStatement)
			#update SAQITM role up 
			QueryStatement = """UPDATE A  SET A.EXTENDED_PRICE = B.EXTENDED_PRICE FROM SAQITM A(NOLOCK) JOIN (SELECT SUM(EXTENDED_PRICE) AS EXTENDED_PRICE,QUOTE_RECORD_ID,SERVICE_ID from SAQICO(NOLOCK) WHERE QUOTE_RECORD_ID ='{QuoteRecordId}' and QUOTE_ITEM_COVERED_OBJECT_RECORD_ID IN ('{item_line_record_ids_str}') GROUP BY QUOTE_RECORD_ID,SERVICE_ID) B ON A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.SERVICE_ID=B.SERVICE_ID """.format(			
			item_line_record_ids_str = item_line_record_ids_str,
			QuoteRecordId=Quote.GetGlobal("contract_quote_record_id"),
			)
			Sql.RunQuery(QueryStatement)
			QueryStatement = """UPDATE A  SET A.TAX = B.TAX FROM SAQITM A(NOLOCK) JOIN (SELECT SUM(TAX) AS TAX,QUOTE_RECORD_ID,SERVICE_ID from SAQICO(NOLOCK) WHERE QUOTE_RECORD_ID ='{QuoteRecordId}' and QUOTE_ITEM_COVERED_OBJECT_RECORD_ID IN ('{item_line_record_ids_str}') GROUP BY QUOTE_RECORD_ID,SERVICE_ID) B ON A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.SERVICE_ID=B.SERVICE_ID """.format(		
			item_line_record_ids_str = item_line_record_ids_str,
			QuoteRecordId=Quote.GetGlobal("contract_quote_record_id")
			)
			Sql.RunQuery(QueryStatement)
			##Upading the quote tables for quote document
			quote_line_items_covered_obj ="""UPDATE a SET a.TOTAL_COST = b.TOTAL_COST,a.TARGET_PRICE = b.TARGET_PRICE,a.YEAR_1 = b.YEAR_1,a.TAX = b.TAX,a.TAX_PERCENTAGE = b.TAX_PERCENTAGE,a.EXTENDED_PRICE = b.EXTENDED_PRICE FROM QT__SAQICO a INNER JOIN SAQICO b on a.EQUIPMENT_ID = b.EQUIPMENT_ID and a.QUOTE_RECORD_ID = b.QUOTE_RECORD_ID where a.QUOTE_RECORD_ID = '{QuoteRecordId}' """.format(QuoteRecordId= Quote.GetGlobal("contract_quote_record_id"))
			Sql.RunQuery(quote_line_items_covered_obj)
			quote_line_item_obj ="""UPDATE a SET a.TOTAL_COST = b.TOTAL_COST,a.TARGET_PRICE = b.TARGET_PRICE,a.YEAR_1 = b.YEAR_1,a.TAX = b.TAX,a.TAX_PERCENTAGE = b.TAX_PERCENTAGE,a.EXTENDED_PRICE = b.EXTENDED_PRICE FROM QT__SAQITM a INNER JOIN SAQITM b on a.SERVICE_ID = b.SERVICE_ID and a.QUOTE_RECORD_ID = b.QUOTE_RECORD_ID where a.QUOTE_RECORD_ID = '{QuoteRecordId}' """.format(QuoteRecordId= Quote.GetGlobal("contract_quote_record_id"))
			Sql.RunQuery(quote_line_item_obj)
	
			
			
def RELATEDMULTISELECTONEDIT(TITLE, VALUE, CLICKEDID, RECORDID):
	TreeParam = Product.GetGlobal("TreeParam")
	if TreeParam == 'Receiving Equipment':
		CLICKEDID = "SYOBJR_98800_0D035FD5_F0EA_4F11_A0DB_B4E10928B59F"
	clicked = CLICKEDID.split("_")
	Trace.Write("clicked---"+str(clicked))
	obj_id = clicked[2] + "-" + clicked[3] + "-" + clicked[4] + "-" + clicked[5] + "-" + clicked[6]
	objr_id = clicked[0] + "-" + clicked[1]
	edt_str = ""
	checked = ""
	data_type = ""
	pricbkst_lock = "FALSE"
	pricbk_lock = "FALSE"
	date_field = []
	VALUE = remove_html_tags(VALUE)
	rec_ids = ",".join(RECORDID)
	
	Product.SetGlobal("RecordList", str(list(RECORDID)))
	Trace.Write("recordids---"+str(Product.GetGlobal("RecordList")))
	TreeParentParam = Product.GetGlobal("TreeParentLevel0")
	objh_obj = Sql.GetFirst("select OBJECT_NAME from SYOBJH where RECORD_ID = '" + str(obj_id) + "'")
	objr_obj = Sql.GetFirst("select CAN_EDIT from SYOBJR where SAPCPQ_ATTRIBUTE_NAME = '" + str(objr_id) + "'")
	canedit = str(objr_obj.CAN_EDIT)
		
	if str(CLICKEDID) == "SYOBJR_00007_26B8147E_C59C_4010_AA3A_38176869E305":
		TITLE = "BILLING_DATE"
	if str(CLICKEDID) == "SYOBJR_00009_E5504B40_36E7_4EA6_9774_EA686705A63F" and TreeParentParam != 'Quote Items':
		canedit = "FALSE"	
	if objh_obj is not None and str(canedit).upper() == "TRUE":
		obj_obj = str(objh_obj.OBJECT_NAME)
		
		objd_obj = Sql.GetFirst(
			"SELECT DATA_TYPE,PICKLIST_VALUES,API_NAME,FIELD_LABEL,PERMISSION,FORMULA_DATA_TYPE FROM  SYOBJD where OBJECT_NAME='"
			+ str(obj_obj)
			+ "' and API_NAME='"
			+ str(TITLE)
			+ "'"
		)
		if objd_obj is not None and pricbkst_lock.upper() == "FALSE" and pricbk_lock.upper() == "FALSE":
			data_type = str(objd_obj.DATA_TYPE).strip()
			api_name = str(objd_obj.API_NAME).strip()
			Permission = str(objd_obj.PERMISSION).strip()
			formula_data_type = str(objd_obj.FORMULA_DATA_TYPE).strip()
			if(data_type != "LOOKUP" and data_type != "AUTO NUMBER" and data_type != "" and Permission != "READ ONLY"):
				Trace.Write('Working ----->')
				pick_val = str(objd_obj.PICKLIST_VALUES)
				field_lable = str(objd_obj.FIELD_LABEL)
				datepicker = "onclick_datepicker('" + api_name + "')"
				edt_str += (
					'<div   class="row modulebnr brdr">EDIT '
					+ str(field_lable).upper()
					+ ' <button type="button"   class="close fltrt" onclick="multiedit_RL_cancel();">X</button></div>'
				)
				edt_str += '<div id="container" class="g4 pad-10 brdr except_sec">'
				edt_str += '<table class="wdth100" id="bulk_edit">'
				edt_str += (
					'<tbody><tr class="fieldRow"><td   class="wth50txtcein labelCol">'
					+ str(field_lable)
					+ '</td><td class="dataCol"><div id="massEditFieldDiv" class="inlineEditRequiredDiv">'
				)
				if len(list(RECORDID)) > 1:
					if data_type.upper() == "TEXT":
						edt_str += '<input class="form-control light_yellow wth_80"   id="' + str(api_name) + '" type="text">'
					elif data_type.upper() == "NUMBER":
						edt_str += '<input class="form-control light_yellow wth_80"   id="' + str(api_name) + '" type="text">'
					elif data_type.upper() == "CHECKBOX" or formula_data_type.upper() == "CHECKBOX":
						edt_str += (
							'<input class="custom light_yellow wth_80"  id="'
							+ str(api_name)
							+ '" type="checkbox"><span class="lbl"></span>'
						)
					elif data_type.upper() == "FORMULA":
						if  obj_obj == 'SAQSTE':
							edt_str += '<input class="form-control light_yellow fltlt wth_80"   id="' + str(api_name) + '" type="text">'
							edt_str += '<input  id="MAFBLC|SAQSTE" class="popup fltlt"  type="image" onclick = "CommonTree_lookup_popup(this)" data-toggle="modal" data-target="#cont_viewModalSection"  src="../mt/default/images/customer_lookup.gif" id="' + str(api_name) + '" >'
						elif obj_obj == 'SAQICO':
							edt_str += '<input class="form-control light_yellow fltlt wth_80"   id="' + str(api_name) + '" type="text">'
							edt_str += '<input  id="PRTXCL|SAQICO" class="popup fltlt"  type="image" onclick = "CommonTree_lookup_popup(this)" data-toggle="modal" data-target="#cont_viewModalSection"  src="../mt/default/images/customer_lookup.gif" id="' + str(api_name) + '" >'	
						elif obj_obj == 'SAQSCO':
							edt_str += '<input class="form-control light_yellow fltlt wth_80"   id="' + str(api_name) + '" type="text">'
							edt_str += '<input  id="SAQSCO|SAQFEQ" class="popup fltlt"  type="image" onclick = "CommonTree_lookup_popup(this)" data-toggle="modal" data-target="#cont_viewModalSection"  src="../mt/default/images/customer_lookup.gif" id="' + str(api_name) + '" >'	
							Trace.Write("EDITSTR"+str(edt_str))	
					elif data_type.upper() == "PICKLIST":
						edt_str += '<select class="form-control light_yellow wth150"   id="' + str(api_name) + '">'
						pick_val = pick_val.split(",")
						for value in pick_val:
							edt_str += "<option>" + str(value) + "</option>"
						edt_str += "</select>"
					elif data_type.upper() == "DATE":
						date_field.append(api_name)
						edt_str += (
							'<input id="'
							+ str(api_name)
							+ '" type="text" class="form-control light_yellow wth155hit26"  ><span   class="pad4wth0 input-group-addon" onclick="'
							+ str(datepicker)
							+ '"><i class="glyphicon glyphicon-calendar"></i></span>'
						)
					else:
						edt_str += '<input class="form-control light_yellow wth_80"   id="' + str(api_name) + '" type="text">'
					edt_str += '</div></td></tr><tr class="selectionRow">'
					edt_str += (
						'<td   class="labelCol wth50txtcein">Apply changes to</td><td class="dataCol"><div class="radio"><input type="radio" name="massOrSingleEdit" id="singleEditRadio" checked="checked"><label for="singleEditRadio">The record clicked</label></div><div class="radio"><input type="radio" name="massOrSingleEdit" id="massEditRadio"><label for="massEditRadio">All '
						+ str(len(list(RECORDID)))
						+ " selected records</label>"
					)
				else:
					
					if data_type.upper() == "TEXT":
						edt_str += (
							'<input class="form-control light_yellow wth_80"   id="'
							+ str(api_name)
							+ '" type="text" value="'
							+ str(VALUE)
							+ '">'
						)
					elif data_type.upper() == "FORMULA" and obj_obj == 'SAQSTE':
						edt_str += '<input class="form-control light_yellow fltlt wth_80"   id="' + str(api_name) + '" type="text">'
						edt_str += '<input  id="MAFBLC|SAQSTE" class="popup fltlt"  type="image" onclick = "CommonTree_lookup_popup(this)" data-toggle="modal" data-target="#cont_viewModalSection"  src="../mt/default/images/customer_lookup.gif" id="' + str(api_name) + '" >'	
					elif data_type.upper() == "NUMBER":
						edt_str += (
							'<input class="form-control light_yellow wth_80"   id="'
							+ str(api_name)
							+ '" value="'
							+ str(VALUE)
							+ '" type="text">'
						)
					elif data_type.upper() == "FORMULA":
						if  obj_obj == 'SAQSTE':
							edt_str += '<input class="form-control light_yellow fltlt wth_80"   id="' + str(api_name) + '" type="text">'
							edt_str += '<input  id="MAFBLC|SAQSTE" class="popup fltlt"  type="image" onclick = "CommonTree_lookup_popup(this)" data-toggle="modal" data-target="#cont_viewModalSection"  src="../mt/default/images/customer_lookup.gif" id="' + str(api_name) + '" >'
						elif obj_obj == 'SAQICO':
							edt_str += '<input class="form-control light_yellow fltlt wth_80"   id="' + str(api_name) + '" type="text">'
							edt_str += '<input  id="PRTXCL|SAQICO" class="popup fltlt"  type="image" onclick = "CommonTree_lookup_popup(this)" data-toggle="modal" data-target="#cont_viewModalSection"  src="../mt/default/images/customer_lookup.gif" id="' + str(api_name) + '" >'	
						elif obj_obj == 'SAQSCO':
							edt_str += '<input class="form-control light_yellow fltlt wth_80"   id="' + str(api_name) + '" type="text">'
							edt_str += '<input  id="SAQSCO|SAQFEQ" class="popup fltlt"  type="image" onclick = "CommonTree_lookup_popup(this)" data-toggle="modal" data-target="#cont_viewModalSection"  src="../mt/default/images/customer_lookup.gif" id="' + str(api_name) + '" >'	
							Trace.Write("EDITSTR"+str(edt_str))
					elif data_type.upper() == "CHECKBOX" or formula_data_type.upper() == "CHECKBOX":
						if str(VALUE).upper() == "TRUE":
							checked = "checked"
						edt_str += (
							'<input class="custom light_yellow wth_80"   id="'
							+ str(api_name)
							+ '" type="checkbox" '
							+ str(checked)
							+ '><span class="lbl"></span>'
						)
					elif data_type.upper() == "PICKLIST":
						edt_str += '<select class="form-control light_yellow wth150"   id="' + str(api_name) + '">'
						pick_val = pick_val.split(",")
						for value in pick_val:
							edt_str += "<option>" + str(value) + "</option>"
						edt_str += "</select>"
					elif data_type.upper() == "DATE":
						date_field.append(api_name)
						edt_str += (
							'<input id="'
							+ str(api_name)
							+ '" type="text" value="'
							+ str(VALUE)
							+ '" class="form-control light_yellow wth155hit26"  ><span   class="pad4wth0 input-group-addon" onclick="'
							+ str(datepicker)
							+ '"><i class="glyphicon glyphicon-calendar"></i></span>'
						)
					else:
						edt_str += (
							'<input class="form-control light_yellow wth_80"   id="'
							+ str(api_name)
							+ '" type="text" value="'
							+ str(VALUE)
							+ '">'
						)
				edt_str += "</div></td></tr></tbody></table>"
				edt_str += '<div class="row pad-10"><button class="btnconfig" onclick="multiedit_RL_cancel();" type="button" value="Cancel" id="cancelButton">CANCEL</button><button class="btnconfig" type="button" value="Save" onclick="multiedit_save_RL()" id="saveButton">SAVE</button></div></div>'
			else:
				edt_str = "NO"
		else:
			edt_str = "NO"
			Trace.Write("EDITSTR"+str(edt_str))	
	else:
		edt_str = "NO"
	return edt_str, date_field


def remove_html_tags(text):
	"""Remove html tags from a string"""
	import re

	clean = re.compile("<.*?>")
	return re.sub(clean, "", text)


def RELATEDMULTISELECTONSAVE(TITLE, VALUE, CLICKEDID, RECORDID,selectPN):
	TreeParam = Product.GetGlobal("TreeParam")
	if TreeParam == 'Receiving Equipment':
		CLICKEDID = "SYOBJR_98800_0D035FD5_F0EA_4F11_A0DB_B4E10928B59F"
	value_list = []
	VALUE1 = []
	selected_rows = RECORDID.split(",")
	
	clicked = CLICKEDID.split("_")
	obj_id = clicked[2] + "-" + clicked[3] + "-" + clicked[4] + "-" + clicked[5] + "-" + clicked[6]
	
	edt_str = ""
	checked = ""
	date_field = []
	selected_rows_cpqid = []
	objh_obj = Sql.GetFirst("select OBJECT_NAME, RECORD_NAME from SYOBJH where RECORD_ID = '" + str(obj_id) + "'")
	if objh_obj is not None:
		obj_name = str(objh_obj.OBJECT_NAME)
		objh_head = str(objh_obj.RECORD_NAME)
		Trace.Write("selected_rows"+str(selected_rows))
		item_lines_record_ids = []
		for rec in selected_rows:
			row = {}
			row = {TITLE: str(VALUE)}
			
			cpqid = rec.split("-")[1].lstrip("0")
			Trace.Write("cpdid--->"+str(cpqid))
			##to update changed value in related tables in tool relcoation matrix
			selected_rows_cpqid.append(cpqid)
			Get_recidval = Sql.GetFirst(
				"SELECT {}  FROM {} (NOLOCK) WHERE CpqTableEntryId='{}' ".format(objh_head, obj_name, cpqid)
			)
			
			rec = getattr(Get_recidval, objh_head)
			
			row[objh_head] = str(rec)
			

			#Trace.Write("SELECT * FROM " + str(obj_name) + " (NOLOCK) WHERE " + str(objh_head) + " = '" + str(rec) + "'")
			sql_obj = Sql.GetFirst("SELECT * FROM  " + str(obj_name) + "  WHERE " + str(objh_head) + " = '" + str(rec) + "'")
			
			#Trace.Write("111====="+str(sql_obj.QUOTE_ID))
			if obj_name == 'SAQICO':
				quote_id = sql_obj.QUOTE_ID
				item_lines_record_ids.append(sql_obj.QUOTE_ITEM_COVERED_OBJECT_RECORD_ID)
			if obj_name == "SYPRAP":
				
				tableInfo = Sql.GetTable("SYPRAP")
				primaryQueryItems = Sql.GetFirst(
					"SELECT * FROM " + str(obj_name) + " WHERE " + objh_head + " = '" + str(rec) + "'"
				)
				row["CpqTableEntryId"] = primaryQueryItems.CpqTableEntryId
				row["DEFAULT"] = str(row.get("VISIBLE"))
				
				tableInfo.AddRow(row)
				Sql.Upsert(tableInfo)
			##multi select bulk edit..
			elif obj_name == "SAQSCO":
				recordslist = []
				for val in selectPn:
					ObjectName = val.split('-')[0]
					cpqid = val.split('-')[1]
					recid = CPQID.KeyCPQId.GetKEYId(ObjectName,str(cpqid))
					recordslist.append(recid)
				recordslist = str(tuple(recordslist)).replace(',)',')')
			##multi select bulk edit..	
			elif str(obj_name) == "SAQSPT":
				
				getserid = row.get("QUOTE_SERVICE_PART_RECORD_ID")
				getpartno = getQn = getAQ = ""
				getPN = Sql.GetFirst("select  * from SAQSPT where QUOTE_SERVICE_PART_RECORD_ID = '"+str(getserid)+"'")
				if getPN:
					getpartno = getPN.PART_NUMBER
					getQn = getPN.QUOTE_ID
					getAQ = getPN.CUSTOMER_ANNUAL_QUANTITY
				sqlforupdatePT = sqlforupdate = ""
				Table.TableActions.Update(obj_name, objh_head, row)
				#for PN in selectPN:
				#Trace.Write(str(getAQ)+str(getQn)+str(getpartno)+'selected rows-------------------------'+str(len(selected_rows)))
				if len(selected_rows) > 1:
					sqlforupdatePT += "UPDATE SAQIFP SET ANNUAL_QUANTITY = '{AQ}',EXTENDED_PRICE = (UNIT_PRICE*'{AQ}') where QUOTE_RECORD_ID ='{CT}' and  PART_NUMBER in {PN}".format(AQ =str(VALUE) ,CT = str(ContractRecordId),PN=tuple(selectPN))
					#sqlforupdatePT += "UPDATE SAQIFP SET ANNUAL_QUANTITY = '{AQ}',EXTENDED_UNIT_PRICE = '{UP}' where QUOTE_RECORD_ID ='{CT}' and  PART_NUMBER in {PN}".format(AQ =str(VALUE) ,CT = str(ContractRecordId),PN=tuple(selectPN))
					Sql.RunQuery(sqlforupdatePT)
					sqlforupdate += "UPDATE QT__SAQIFP SET  ANNUAL_QUANTITY = {AQ},EXTENDED_UNIT_PRICE = (UNIT_PRICE*{AQ}) where QUOTE_RECORD_ID ='{CT}' and  PART_NUMBER in {PN}".format(AQ =VALUE ,CT = str(ContractRecordId),PN=tuple(selectPN))
					Sql.RunQuery(sqlforupdate)
				else:
					
					sqlforupdatePT += "UPDATE SAQIFP SET ANNUAL_QUANTITY = '{AQ}',EXTENDED_PRICE = (UNIT_PRICE*{AQ}) where QUOTE_RECORD_ID ='{CT}' and  PART_NUMBER = '{PN}'".format(AQ =VALUE ,CT = str(ContractRecordId),PN=getpartno)
					#sqlforupdatePT += "UPDATE SAQIFP SET ANNUAL_QUANTITY = '{AQ}',EXTENDED_UNIT_PRICE = '{UP}' where QUOTE_RECORD_ID ='{CT}' and  PART_NUMBER in {PN}".format(AQ =str(VALUE) ,CT = str(ContractRecordId),PN=tuple(selectPN))
					Sql.RunQuery(sqlforupdatePT)
					sqlforupdate += "UPDATE QT__SAQIFP SET  ANNUAL_QUANTITY = {AQ},EXTENDED_UNIT_PRICE = (UNIT_PRICE*{AQ}) where QUOTE_RECORD_ID ='{CT}' and  PART_NUMBER  = '{PN}'".format(AQ =VALUE ,CT = str(ContractRecordId),PN=getpartno)
					Sql.RunQuery(sqlforupdate)

			else:
				Trace.Write("selected_rows"+str(row))
				Table.TableActions.Update(obj_name, objh_head, row)
				##Updating the fabname and fablocation id in bulk edit scenario starts....
		if obj_name == 'SAQICO':
			prtxcl_obj = Sql.GetFirst("Select TAX_CLASSIFICATION_RECORD_ID,TAX_CLASSIFICATION_DESCRIPTION,TAX_CLASSIFICATION_ID FROM PRTXCL WHERE  TAX_CLASSIFICATION_DESCRIPTION = '{SRVTAXCLA_DESCRIPTION}'".format(SRVTAXCLA_DESCRIPTION = str(VALUE)))
			line_items_obj = """UPDATE SAQICO SET SRVTAXCLA_ID = '{TAX_CLASSIFICATION_ID}', SRVTAXCLA_RECORD_ID = '{SRVTAXCLA_RECORD_ID}' WHERE SRVTAXCLA_DESCRIPTION = '{SRVTAXCLA_DESCRIPTION}' and QUOTE_RECORD_ID = '{quote_record_id}' """.format(TAX_CLASSIFICATION_ID = prtxcl_obj.TAX_CLASSIFICATION_ID,SRVTAXCLA_RECORD_ID = prtxcl_obj.TAX_CLASSIFICATION_RECORD_ID,SRVTAXCLA_DESCRIPTION = str(VALUE),quote_record_id = str(ContractRecordId))
			Sql.RunQuery(line_items_obj)
			quote_id = quote_id
			quote_record_id = str(Qt_rec_id)
			getting_cps_tax(quote_id,quote_record_id,item_lines_record_ids)
		if obj_name == "SAQSCO":
			getfab = Sql.GetFirst("SELECT FABLOCATION_NAME, FABLOCATION_RECORD_ID FROM SAQFBL WHERE QUOTE_RECORD_ID = '{}' AND FABLOCATION_ID = '{}'".format(Quote.GetGlobal("contract_quote_record_id"),VALUE))
			fabname = getfab.FABLOCATION_NAME
			fabrec = getfab.FABLOCATION_RECORD_ID		
			if 	SELECTALL != "no":
				Sql.RunQuery("UPDATE SAQSCO SET FABLOCATION_ID = '{VALUE}',FABLOCATION_NAME = '{name}',FABLOCATION_RECORD_ID = '{rec}' WHERE QUOTE_RECORD_ID = '{Quote}' AND RELOCATION_EQUIPMENT_TYPE = 'RECEIVING EQUIPMENT' AND SERVICE_ID= '{ServiceId}' {SingleRow}".format(VALUE=VALUE,Quote=Quote.GetGlobal("contract_quote_record_id"),SingleRow=" AND CpqTableEntryId = '"+str(cpqid) + "'" if SELECTALL == "no" else "",ServiceId=Quote.GetGlobal("TreeParentLevel0"),name=fabname,rec=fabrec))
			else:
				Sql.RunQuery("UPDATE SAQSCO SET FABLOCATION_ID = '{VALUE}',FABLOCATION_NAME = '{name}',FABLOCATION_RECORD_ID = '{rec}' WHERE QUOTE_RECORD_ID = '{Quote}' AND RELOCATION_EQUIPMENT_TYPE = 'RECEIVING EQUIPMENT' AND SERVICE_ID= '{ServiceId}' AND QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID IN {recordslist}".format(VALUE=VALUE,Quote=Quote.GetGlobal("contract_quote_record_id"),ServiceId=Quote.GetGlobal("TreeParentLevel0"),name=fabname,rec=fabrec))	
			'''Sql.RunQuery("UPDATE SAQSFE SET FABLOCATION_ID = '{VALUE}',FABLOCATION_NAME = '{name}',FABLOCATION_RECORD_ID = '{rec}' WHERE QUOTE_RECORD_ID = '{Quote}' AND SERVICE_ID= '{ServiceId}' {SingleRow}".format(VALUE=VALUE,Quote=Quote.GetGlobal("contract_quote_record_id"),SingleRow=" AND CpqTableEntryId = '"+str(cpqid) + "'" if SELECTALL == "no" else "",ServiceId=Quote.GetGlobal("TreeParentLevel0"),name=fabname,rec=fabrec))
			Sql.RunQuery("UPDATE SAQSGE SET FABLOCATION_ID = '{VALUE}',FABLOCATION_NAME = '{name}',FABLOCATION_RECORD_ID = '{rec}' WHERE QUOTE_RECORD_ID = '{Quote}' AND SERVICE_ID= '{ServiceId}' {SingleRow}".format(VALUE=VALUE,Quote=Quote.GetGlobal("contract_quote_record_id"),SingleRow=" AND CpqTableEntryId = '"+str(cpqid) + "'" if SELECTALL == "no" else "",ServiceId=Quote.GetGlobal("TreeParentLevel0"),name=fabname,rec=fabrec))
			Sql.RunQuery("""UPDATE SAQSCE SET FABLOCATION_ID = '{VALUE}',FABLOCATION_NAME = '{name}',FABLOCATION_RECORD_ID = '{rec}' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND SERVICE_ID= '{ServiceId}' {SingleRow}""".format(
			VALUE=VALUE,
			UserId=User.Id, 
			QuoteRecordId=Quote.GetGlobal("contract_quote_record_id"),
			name=fabname,
			rec=fabrec,
			ServiceId=Quote.GetGlobal("TreeParentLevel0"),SingleRow=" AND SAQSCO.CpqTabl """eEntryId = '"+str(cpqid) + "'" if SELECTALL == "no" else ""))'''
			Sql.RunQuery(
				"""INSERT SAQSFB(
					FABLOCATION_ID,
					FABLOCATION_NAME,
					FABLOCATION_RECORD_ID,
					SERVICE_ID,
					SERVICE_TYPE,
					SERVICE_DESCRIPTION,
					SERVICE_RECORD_ID,
					FABLOCATION_STATUS,
					QUOTE_ID,
					QUOTE_NAME,
					QUOTE_RECORD_ID,
					MNT_PLANT_ID,
					MNT_PLANT_NAME,
					MNT_PLANT_RECORD_ID,
					ADDRESS_1,
					ADDRESS_2,
					CITY,
					COUNTRY,
					COUNTRY_RECORD_ID,
					SALESORG_ID,
					SALESORG_NAME,
					SALESORG_RECORD_ID,
					PAR_SERVICE_DESCRIPTION,
					PAR_SERVICE_ID,
					PAR_SERVICE_RECORD_ID,
					QUOTE_SERVICE_FAB_LOCATION_RECORD_ID,
					CPQTABLEENTRYADDEDBY,
					CPQTABLEENTRYDATEADDED,
					CpqTableEntryModifiedBy,
					CpqTableEntryDateModified
					) SELECT FB.*,CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_FAB_LOCATION_RECORD_ID,
					'{UserName}' AS CPQTABLEENTRYADDEDBY,
					GETDATE() as CPQTABLEENTRYDATEADDED, {UserId} as CpqTableEntryModifiedBy,
					GETDATE() as CpqTableEntryDateModified FROM (
					SELECT DISTINCT
					SAQSCO.FABLOCATION_ID,
					MAFBLC.FAB_LOCATION_NAME,
					MAFBLC.FAB_LOCATION_RECORD_ID,
					SAQSCO.SERVICE_ID,
					SAQSCO.SERVICE_TYPE,
					SAQSCO.SERVICE_DESCRIPTION,
					SAQSCO.SERVICE_RECORD_ID,
					MAFBLC.STATUS,
					SAQSCO.QUOTE_ID,
					SAQSCO.QUOTE_NAME,
					SAQSCO.QUOTE_RECORD_ID,
					SAQSCO.MNT_PLANT_ID,
					SAQSCO.MNT_PLANT_NAME,
					SAQSCO.MNT_PLANT_RECORD_ID,
					MAFBLC.ADDRESS_1,
					MAFBLC.ADDRESS_2,
					MAFBLC.CITY,
					MAFBLC.COUNTRY,
					MAFBLC.COUNTRY_RECORD_ID,
					SAQSCO.SALESORG_ID,
					SAQSCO.SALESORG_NAME,
					SAQSCO.SALESORG_RECORD_ID,
					SAQSCO.PAR_SERVICE_DESCRIPTION,
					SAQSCO.PAR_SERVICE_ID,
					SAQSCO.PAR_SERVICE_RECORD_ID
					FROM SAQSCO (NOLOCK)
					JOIN MAFBLC (NOLOCK) ON SAQSCO.FABLOCATION_ID = MAFBLC.FAB_LOCATION_ID
					WHERE SAQSCO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCO.RELOCATION_EQUIPMENT_TYPE = 'RECEIVING EQUIPMENT' AND FABLOCATION_ID NOT IN(SELECT FABLOCATION_ID FROM SAQSFB WHERE SERVICE_ID = '{TreeParam}' AND QUOTE_RECORD_ID = '{QuoteRecordId}') {SingleRow}
					) FB""".format(
									TreeParam=Quote.GetGlobal("TreeParentLevel0"),
									QuoteRecordId=Quote.GetGlobal("contract_quote_record_id"),
									UserId=User.Id,
									UserName=User.UserName,
									SingleRow=" AND SAQSCO.CpqTableEntryId = '"+str(cpqid) + "'" if SELECTALL == "no" else ""
								))
			Sql.RunQuery("""
						INSERT SAQSFE (ENTITLEMENT_XML,QUOTE_ID,QUOTE_NAME,QUOTE_RECORD_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,	
						CPS_CONFIGURATION_ID, CPS_MATCH_ID,QTESRVENT_RECORD_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,QTESRVFBL_RECORD_ID,PAR_SERVICE_ID,PAR_SERVICE_DESCRIPTION,PAR_SERVICE_RECORD_ID,QUOTE_SERVICE_FAB_LOC_ENT_RECORD_ID,CPQTABLEENTRYDATEADDED, CPQTABLEENTRYADDEDBY)
						SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_FAB_LOC_ENT_RECORD_ID, {UserId} as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM (
						SELECT 
							DISTINCT	
							SAQTSE.ENTITLEMENT_XML,SAQTSE.QUOTE_ID,SAQTSE.QUOTE_NAME,SAQTSE.QUOTE_RECORD_ID,SAQTSE.SERVICE_DESCRIPTION,SAQTSE.SERVICE_ID,SAQTSE.SERVICE_RECORD_ID,SAQTSE.SALESORG_ID,SAQTSE.SALESORG_NAME,SAQTSE.SALESORG_RECORD_ID,SAQTSE.CPS_CONFIGURATION_ID, SAQTSE.CPS_MATCH_ID,SAQTSE.QUOTE_SERVICE_ENTITLEMENT_RECORD_ID as QTESRVENT_RECORD_ID,SAQSFB.FABLOCATION_ID, SAQSFB.FABLOCATION_NAME, SAQSFB.FABLOCATION_RECORD_ID,SAQSFB.QUOTE_SERVICE_FAB_LOCATION_RECORD_ID as QTESRVFBL_RECORD_ID,SAQTSE.PAR_SERVICE_ID,SAQTSE.PAR_SERVICE_DESCRIPTION,SAQTSE.PAR_SERVICE_RECORD_ID
						FROM
						SAQTSE (NOLOCK)
						JOIN SAQSFB ON SAQSFB.SERVICE_RECORD_ID = SAQTSE.SERVICE_RECORD_ID AND SAQSFB.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID
						WHERE SAQTSE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQTSE.SERVICE_ID = '{ServiceId}' AND SAQSFB.FABLOCATION_ID NOT IN (SELECT FABLOCATION_ID FROM SAQSFE WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND SERVICE_ID = '{ServiceId}')) IQ""".format(UserId=User.Id, QuoteRecordId=Quote.GetGlobal("contract_quote_record_id"), ServiceId=Quote.GetGlobal("TreeParentLevel0")))
			
			Sql.RunQuery(""" INSERT SAQSGE (KB_VERSION,QUOTE_ID,QUOTE_NAME,QUOTE_RECORD_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,	
			CPS_CONFIGURATION_ID, CPS_MATCH_ID,GREENBOOK,GREENBOOK_RECORD_ID,QTESRVENT_RECORD_ID,QTSFBLENT_RECORD_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,ENTITLEMENT_XML, QUOTE_SERVICE_GREENBOOK_ENTITLEMENT_RECORD_ID,CPQTABLEENTRYDATEADDED, CPQTABLEENTRYADDEDBY)
			SELECT OQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_GREENBOOK_ENTITLEMENT_RECORD_ID, {UserId} as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM (SELECT IQ.*,M.ENTITLEMENT_XML FROM(
			SELECT 
				DISTINCT	
				SAQTSE.KB_VERSION,SAQTSE.QUOTE_ID,SAQTSE.QUOTE_NAME,SAQTSE.QUOTE_RECORD_ID,SAQTSE.SERVICE_DESCRIPTION,SAQTSE.SERVICE_ID,SAQTSE.SERVICE_RECORD_ID,SAQTSE.SALESORG_ID,SAQTSE.SALESORG_NAME,SAQTSE.SALESORG_RECORD_ID,SAQTSE.CPS_CONFIGURATION_ID, SAQTSE.CPS_MATCH_ID,SAQSCO.GREENBOOK,SAQSCO.GREENBOOK_RECORD_ID,SAQTSE.QUOTE_SERVICE_ENTITLEMENT_RECORD_ID as QTESRVENT_RECORD_ID,SAQSFE.QUOTE_SERVICE_FAB_LOC_ENT_RECORD_ID as QTSFBLENT_RECORD_ID,SAQSFE.FABLOCATION_ID,SAQSFE.FABLOCATION_NAME,SAQSFE.FABLOCATION_RECORD_ID
			FROM
			SAQTSE (NOLOCK)
			JOIN SAQSCO  (NOLOCK) ON SAQSCO.SERVICE_RECORD_ID = SAQTSE.SERVICE_RECORD_ID AND SAQSCO.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID JOIN SAQSFE ON SAQSFE.SERVICE_RECORD_ID = SAQTSE.SERVICE_RECORD_ID AND SAQSFE.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID 
			WHERE SAQTSE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQTSE.SERVICE_ID = '{ServiceId}' AND SAQSCO.RELOCATION_EQUIPMENT_TYPE = 'Receiving Equipment') IQ JOIN SAQSFE (NOLOCK) M ON IQ.QTSFBLENT_RECORD_ID = QUOTE_SERVICE_FAB_LOC_ENT_RECORD_ID )OQ""".format(UserId=User.Id, QuoteRecordId=Quote.GetGlobal("contract_quote_record_id"), ServiceId=Quote.GetGlobal("TreeParentLevel0")))

			
			Sql.RunQuery(
				"""
					INSERT SAQSGB (
						QUOTE_SERVICE_GREENBOOK_RECORD_ID,
						FABLOCATION_ID,
						GREENBOOK,
						GREENBOOK_RECORD_ID,
						QUOTE_ID,
						QUOTE_NAME,
						QUOTE_RECORD_ID,
						SALESORG_ID,
						SALESORG_NAME,
						SALESORG_RECORD_ID,
						SERVICE_DESCRIPTION,
						SERVICE_ID,
						SERVICE_RECORD_ID,
						EQUIPMENT_QUANTITY,
						FABLOCATION_NAME,
						FABLOCATION_RECORD_ID,
						PAR_SERVICE_DESCRIPTION,
						PAR_SERVICE_ID,
						PAR_SERVICE_RECORD_ID,
						CPQTABLEENTRYADDEDBY,
						CPQTABLEENTRYDATEADDED,
						CpqTableEntryModifiedBy,
						CpqTableEntryDateModified
						) SELECT CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_GREENBOOK_RECORD_ID,A.* from (SELECT DISTINCT
							SAQSCO.FABLOCATION_ID,
							SAQSCO.GREENBOOK,
							SAQSCO.GREENBOOK_RECORD_ID,
							SAQSCO.QUOTE_ID,
							SAQSCO.QUOTE_NAME,
							SAQSCO.QUOTE_RECORD_ID,
							SAQSCO.SALESORG_ID,
							SAQSCO.SALESORG_NAME,
							SAQSCO.SALESORG_RECORD_ID,
							SAQSCO.SERVICE_DESCRIPTION,
							SAQSCO.SERVICE_ID,
							SAQSCO.SERVICE_RECORD_ID,
							SAQSCO.EQUIPMENT_QUANTITY,								
							SAQSCO.FABLOCATION_NAME,
							SAQSCO.FABLOCATION_RECORD_ID,
							SAQTSV.PAR_SERVICE_DESCRIPTION,
							SAQTSV.PAR_SERVICE_ID,
							SAQTSV.PAR_SERVICE_RECORD_ID,
							'{UserName}' AS CPQTABLEENTRYADDEDBY,
							GETDATE() as CPQTABLEENTRYDATEADDED,
							{UserId} as CpqTableEntryModifiedBy,
							GETDATE() as CpqTableEntryDateModified
							FROM SAQSCO (NOLOCK) JOIN SAQTSV (NOLOCK) ON
							SAQSCO.QUOTE_ID = SAQTSV.QUOTE_ID AND
							SAQTSV.SERVICE_ID = '{TreeParam}' AND
							SAQTSV.SERVICE_TYPE = '{TreeParentParam}'
							JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID
							WHERE 
							SAQSCO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCO.RELOCATION_EQUIPMENT_TYPE = 'Receiving Equipment' {SingleRow})A""".format(
							TreeParam=Quote.GetGlobal("TreeParentLevel0"),
							TreeParentParam=Quote.GetGlobal("TreeParentLevel1"),
							QuoteRecordId=Quote.GetGlobal("contract_quote_record_id"),
							UserName=User.UserName,
							UserId=User.Id,
							SingleRow=" AND SAQSCO.CpqTableEntryId = '"+str(cpqid) + "'" if SELECTALL == "no" else ""
						)
			)
			# ###SAQSCE and SAQSAE insert for assembly and entitlement 
			qtqsce_query="""
			 	INSERT SAQSCE
				(KB_VERSION,ENTITLEMENT_XML,EQUIPMENT_ID,EQUIPMENT_RECORD_ID,QUOTE_ID,QUOTE_RECORD_ID,QTESRVCOB_RECORD_ID,QTESRVENT_RECORD_ID,SERIAL_NO,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,CPS_CONFIGURATION_ID,CPS_MATCH_ID,GREENBOOK,GREENBOOK_RECORD_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,QUOTE_SERVICE_COVERED_OBJ_ENTITLEMENTS_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED) 
				SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_COVERED_OBJ_ENTITLEMENTS_RECORD_ID, {UserId} as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM (
				SELECT 
			 	DISTINCT
			 	SAQTSE.KB_VERSION,SAQTSE.ENTITLEMENT_XML,SAQSCO.EQUIPMENT_ID,SAQSCO.EQUIPMENT_RECORD_ID,SAQTSE.QUOTE_ID,SAQTSE.QUOTE_RECORD_ID,SAQSCO.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID as QTESRVCOB_RECORD_ID,SAQTSE.QUOTE_SERVICE_ENTITLEMENT_RECORD_ID as QTESRVENT_RECORD_ID,SAQSCO.SERIAL_NO,SAQTSE.SERVICE_DESCRIPTION,SAQTSE.SERVICE_ID,SAQTSE.SERVICE_RECORD_ID,SAQTSE.CPS_CONFIGURATION_ID,SAQTSE.CPS_MATCH_ID,SAQSCO.GREENBOOK,SAQSCO.GREENBOOK_RECORD_ID,SAQSCO.FABLOCATION_ID,SAQSCO.FABLOCATION_NAME,SAQSCO.FABLOCATION_RECORD_ID,SAQTSE.SALESORG_ID,SAQTSE.SALESORG_NAME,SAQTSE.SALESORG_RECORD_ID
				FROM	
			 	SAQTSE (NOLOCK)
				JOIN SAQSCO (NOLOCK) ON SAQSCO.SERVICE_RECORD_ID = SAQTSE.SERVICE_RECORD_ID AND SAQSCO.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID 
				WHERE SAQTSE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQTSE.SERVICE_ID = '{ServiceId}') IQ""".format(
			 	UserId=User.Id, 
				QuoteRecordId=Qt_rec_id, 
			 	ServiceId=Quote.GetGlobal("TreeParentLevel0") )
			 	#Trace.Write('qtqsce_query-renewal----179=---Qt_rec_id--'+str(qtqsce_query))
			Sql.RunQuery(qtqsce_query)
			# SAQSAE_insert = """INSERT SAQSAE (KB_VERSION,EQUIPMENT_ID,EQUIPMENT_RECORD_ID,QUOTE_ID,QUOTE_RECORD_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,CPS_CONFIGURATION_ID,CPS_MATCH_ID,GREENBOOK,GREENBOOK_RECORD_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,ASSEMBLY_DESCRIPTION,ASSEMBLY_ID,ASSEMBLY_RECORD_ID,QTESRVCOA_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,ENTITLEMENT_XML,QTESRVCOE_RECORD_ID,QUOTE_SERVICE_COV_OBJ_ASS_ENT_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED) SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_COV_OBJ_ASS_ENT_RECORD_ID, {UserId} as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM(SELECT IQ.*,M.ENTITLEMENT_XML,M.QUOTE_SERVICE_COVERED_OBJ_ENTITLEMENTS_RECORD_ID as QTESRVCOE_RECORD_ID FROM ( SELECT DISTINCT SAQTSE.KB_VERSION,SAQSCA.EQUIPMENT_ID,SAQSCA.EQUIPMENT_RECORD_ID,SAQTSE.QUOTE_ID,SAQTSE.QUOTE_RECORD_ID,SAQTSE.SERVICE_DESCRIPTION,SAQTSE.SERVICE_ID,SAQTSE.SERVICE_RECORD_ID,SAQTSE.CPS_CONFIGURATION_ID,SAQTSE.CPS_MATCH_ID,SAQSCA.GREENBOOK,SAQSCA.GREENBOOK_RECORD_ID,SAQSCA.FABLOCATION_ID,SAQSCA.FABLOCATION_NAME,SAQSCA.FABLOCATION_RECORD_ID,SAQSCA.ASSEMBLY_DESCRIPTION,SAQSCA.ASSEMBLY_ID,SAQSCA.ASSEMBLY_RECORD_ID,SAQSCA.QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID as QTESRVCOA_RECORD_ID,SAQTSE.SALESORG_ID,SAQTSE.SALESORG_NAME,SAQTSE.SALESORG_RECORD_ID FROM SAQTSE (NOLOCK) JOIN (SELECT * FROM SAQSCA (NOLOCK) WHERE SAQSCA.QUOTE_RECORD_ID = '{ContractId}' ) SAQSCA ON SAQTSE.QUOTE_RECORD_ID = SAQSCA.QUOTE_RECORD_ID AND SAQTSE.SERVICE_RECORD_ID = SAQSCA.SERVICE_RECORD_ID WHERE SAQTSE.QUOTE_RECORD_ID = '{ContractId}' AND SAQTSE.SERVICE_ID = '{serviceId}') IQ JOIN SAQSCE (NOLOCK) M ON M.SERVICE_RECORD_ID = IQ.SERVICE_RECORD_ID AND M.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND M.EQUIPMENT_ID = IQ.EQUIPMENT_ID )IQ""".format(
			# 	UserId=User.Id, 
			# 	ContractId=Qt_rec_id, 
			# 	ServiceId=Quote.GetGlobal("TreeParentLevel0") )
			# Sql.RunQuery(SAQSAE_insert)
			# Trace.Write('SAQSAE_insert--'+str(SAQSAE_insert))
		if obj_name == 'SAQSTE':
			master_fab_object = Sql.GetFirst("Select FAB_LOCATION_NAME,FAB_LOCATION_RECORD_ID from MAFBLC where FAB_LOCATION_ID = '{fab_id}'".format(fab_id = str(VALUE)))
			fab_name = master_fab_object.FAB_LOCATION_NAME
			fab_location_record_id = master_fab_object.FAB_LOCATION_RECORD_ID
			Tool_relocation_object = """UPDATE SAQSTE SET FABLOCATION_NAME = '{fab_name}', FABLOCATION_RECORD_ID = '{fab_location_record_id}' WHERE FABLOCATION_ID = '{fab_id}' and QUOTE_RECORD_ID = '{quote_record_id}' """.format(fab_name = fab_name,fab_location_record_id = fab_location_record_id,fab_id = str(VALUE),quote_record_id = str(ContractRecordId))
			Sql.RunQuery(Tool_relocation_object)
			##Updating the fabname and fablocation id in bulk edit scenario ends.... 
			
			GETSAQFBL = Sql.GetFirst("SELECT QUOTE_FABLOCATION_RECORD_ID FROM SAQFBL(NOLOCK) WHERE QUOTE_RECORD_ID = '"+str(ContractRecordId)+"'and FABLOCATION_ID ='"+str(VALUE)+"' ")
			if GETSAQFBL is None:
				Sql.RunQuery(""" INSERT SAQFBL (FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, QUOTE_ID, QUOTE_RECORD_ID, COUNTRY, COUNTRY_RECORD_ID, MNT_PLANT_ID, MNT_PLANT_NAME, MNT_PLANT_RECORD_ID, SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID, FABLOCATION_STATUS, ADDRESS_1, ADDRESS_2, CITY, STATE, STATE_RECORD_ID,QUOTE_FABLOCATION_RECORD_ID,CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified) SELECT A.*,CONVERT(VARCHAR(4000),NEWID()) as QUOTE_FABLOCATION_RECORD_ID,'{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED,'{UserId}' as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (SELECT DISTINCT MAFBLC.FAB_LOCATION_ID,MAFBLC.FAB_LOCATION_NAME,MAFBLC.FAB_LOCATION_RECORD_ID,SAQSTE.QUOTE_ID,SAQSTE.QUOTE_RECORD_ID,MAFBLC.COUNTRY,MAFBLC.COUNTRY_RECORD_ID,MAFBLC.MNT_PLANT_ID,MAFBLC.MNT_PLANT_NAME,MAFBLC.MNT_PLANT_RECORD_ID,MAFBLC.SALESORG_ID,MAFBLC.SALESORG_NAME,MAFBLC.SALESORG_RECORD_ID,MAFBLC.STATUS AS FABLOCATION_STATUS,MAFBLC.ADDRESS_1,MAFBLC.ADDRESS_2,MAFBLC.CITY,MAFBLC.STATE,MAFBLC.STATE_RECORD_ID FROM MAFBLC INNER JOIN  SAQSTE on MAFBLC.FAB_LOCATION_ID = SAQSTE.FABLOCATION_ID WHERE QUOTE_RECORD_ID = '{QuoteRecId}' AND SAQSTE.FABLOCATION_ID ='{fabid}')A WHERE A.FAB_LOCATION_ID NOT IN (SELECT FABLOCATION_ID FROM SAQFBL WHERE QUOTE_RECORD_ID = '{QuoteRecId}') """.format(UserName=User.UserName,UserId=User.Id,QuoteRecId=ContractRecordId,fabid=VALUE))
			

			###update SAQFEQ starts
			GETSAQFEQ = Sql.GetFirst("""SELECT SAQFBL.QUOTE_FABLOCATION_RECORD_ID from SAQFEQ (NOLOCK) INNER JOIN SAQSTE (NOLOCK) ON SAQFEQ.EQUIPMENT_ID = SAQSTE.EQUIPMENT_ID AND SAQFEQ.QUOTE_RECORD_ID = SAQSTE.QUOTE_RECORD_ID INNER JOIN SAQFBL (NOLOCK) on SAQFBL.FABLOCATION_ID = SAQSTE.FABLOCATION_ID AND  SAQFBL.QUOTE_RECORD_ID = SAQSTE.QUOTE_RECORD_ID where SAQFEQ.QUOTE_RECORD_ID = '{quote_record_id}' AND SAQSTE.CpqTableEntryId in {SAQSTE_cpqid}""".format(quote_record_id = str(ContractRecordId),SAQSTE_cpqid = str(tuple(selected_rows_cpqid)).replace(',)',')')))
			if GETSAQFEQ is not None:
				 
				Sql.RunQuery("""UPDATE SAQFEQ SET FABLOCATION_ID = '{fab_id}',FABLOCATION_NAME = '{fab_name}', FABLOCATION_RECORD_ID = '{fab_location_record_id}', QTEFBL_RECORD_ID = '{quote_fab_rec_id}' FROM SAQFEQ WHERE QUOTE_RECORD_ID = '{quote_record_id}' AND EQUIPMENT_RECORD_ID IN (SELECT SAQFEQ.EQUIPMENT_RECORD_ID from SAQFEQ (NOLOCK) INNER JOIN SAQSTE (NOLOCK) ON SAQFEQ.EQUIPMENT_ID = SAQSTE.EQUIPMENT_ID AND SAQFEQ.QUOTE_RECORD_ID = SAQSTE.QUOTE_RECORD_ID where SAQFEQ.QUOTE_RECORD_ID = '{quote_record_id}' AND SAQSTE.CpqTableEntryId in {SAQSTE_cpqid} )""".format(fab_id = str(VALUE),fab_name = fab_name,fab_location_record_id = fab_location_record_id,quote_record_id = str(ContractRecordId),SAQSTE_cpqid = str(tuple(selected_rows_cpqid)).replace(',)',')') ,quote_fab_rec_id = GETSAQFEQ.QUOTE_FABLOCATION_RECORD_ID ))
			###update SAQFEQ ends
			else:

				Sql.RunQuery(""" INSERT SAQFEQ ( QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID, EQUIPMENT_ID, EQUIPMENT_RECORD_ID, EQUIPMENT_DESCRIPTION, FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, SERIAL_NUMBER, QUOTE_RECORD_ID, QUOTE_ID, QUOTE_NAME, PLATFORM, EQUIPMENTCATEGORY_RECORD_ID, EQUIPMENTCATEGORY_ID, EQUIPMENTCATEGORY_DESCRIPTION, EQUIPMENT_STATUS, PBG, GREENBOOK, GREENBOOK_RECORD_ID, MNT_PLANT_RECORD_ID, MNT_PLANT_ID, MNT_PLANT_NAME, WARRANTY_START_DATE, WARRANTY_END_DATE, SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID, CUSTOMER_TOOL_ID,SRCACC_ID,SRCACC_NAME,SRCACC_RECORD_ID,SRCFBL_ID,SRCFBL_NAME,SRCFBL_RECORD_ID,QTEFBL_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified )SELECT A.* FROM( SELECT CONVERT(VARCHAR(4000),NEWID()) as QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID, SAQSTE.EQUIPMENT_ID, SAQSTE.EQUIPMENT_RECORD_ID, SAQSTE.EQUIPMENT_DESCRIPTION, SAQSTE.FABLOCATION_ID, SAQSTE.FABLOCATION_NAME, SAQSTE.FABLOCATION_RECORD_ID, MAEQUP.SERIAL_NO, SAQSTE.QUOTE_RECORD_ID, SAQSTE.QUOTE_ID, SAQSTE.QUOTE_NAME, MAEQUP.PLATFORM, SAQSTE.EQUIPMENTCATEGORY_RECORD_ID, SAQSTE.EQUIPMENTCATEGORY_ID, SAQSTE.EQUIPMENTCATEGORY_DESCRIPTION, SAQSTE.EQUIPMENT_STATUS, MAEQUP.PBG, SAQSTE.GREENBOOK, SAQSTE.GREENBOOK_RECORD_ID, SAQSTE.MNT_PLANT_RECORD_ID, SAQSTE.MNT_PLANT_ID, SAQSTE.MNT_PLANT_NAME, MAEQUP.WARRANTY_START_DATE, MAEQUP.WARRANTY_END_DATE, MAEQUP.SALESORG_ID, MAEQUP.SALESORG_NAME, MAEQUP.SALESORG_RECORD_ID, MAEQUP.CUSTOMER_TOOL_ID,SAQSTE.SRCACC_ID,SAQSTE.SRCACC_NAME,SAQSTE.SRCACC_RECORD_ID,SAQSTE.SRCFBL_ID,SAQSTE.SRCFBL_NAME,SAQSTE.SRCFBL_RECORD_ID,SAQFBL.QUOTE_FABLOCATION_RECORD_ID as QTEFBL_RECORD_ID,'{UserName}' AS CPQTABLEENTRYADDEDBY,GETDATE() as CPQTABLEENTRYDATEADDED,'{UserId}' as CpqTableEntryModifiedBy,GETDATE() as CpqTableEntryDateModified FROM MAEQUP (NOLOCK)INNER JOIN  SAQSTE on MAEQUP.EQUIPMENT_ID = SAQSTE.EQUIPMENT_ID INNER JOIN SAQFBL on SAQFBL.FABLOCATION_ID = SAQSTE.FABLOCATION_ID AND  SAQFBL.QUOTE_RECORD_ID = SAQSTE.QUOTE_RECORD_ID WHERE SAQSTE.QUOTE_RECORD_ID = '{QuoteRecId}' AND SAQSTE.FABLOCATION_ID ='{fabid}') A LEFT JOIN SAQFEQ M(NOLOCK) ON A.QUOTE_ID = M.QUOTE_ID AND A.EQUIPMENT_ID = M.EQUIPMENT_ID WHERE M.EQUIPMENT_ID IS NULL""".format(UserName=User.UserName,UserId=User.Id,QuoteRecId=ContractRecordId,fabid=VALUE))
			
			###update SAQFEA starts
			GETSAQFEA = Sql.GetFirst("""SELECT count(SAQFEA.EQUIPMENT_RECORD_ID) as cnt from SAQFEA (NOLOCK) INNER JOIN SAQSTE (NOLOCK) ON SAQFEA.EQUIPMENT_ID = SAQSTE.EQUIPMENT_ID AND SAQFEA.QUOTE_RECORD_ID = SAQSTE.QUOTE_RECORD_ID where SAQFEA.QUOTE_RECORD_ID = '{quote_record_id}' AND SAQSTE.CpqTableEntryId in {SAQSTE_cpqid}""".format(quote_record_id = str(ContractRecordId),SAQSTE_cpqid = str(tuple(selected_rows_cpqid)).replace(',)',')'))) 
			if GETSAQFEA.cnt:
				Sql.RunQuery("""UPDATE SAQFEA SET FABLOCATION_ID = '{fab_id}',FABLOCATION_NAME = '{fab_name}', FABLOCATION_RECORD_ID = '{fab_location_record_id}' FROM SAQFEA WHERE QUOTE_RECORD_ID = '{quote_record_id}' AND EQUIPMENT_RECORD_ID IN (SELECT SAQFEA.EQUIPMENT_RECORD_ID from SAQFEA (NOLOCK) INNER JOIN SAQSTE (NOLOCK) ON SAQFEA.EQUIPMENT_ID = SAQSTE.EQUIPMENT_ID AND SAQFEA.QUOTE_RECORD_ID = SAQSTE.QUOTE_RECORD_ID where SAQFEA.QUOTE_RECORD_ID = '{quote_record_id}' AND SAQSTE.CpqTableEntryId in {SAQSTE_cpqid} )""".format(fab_id = str(VALUE),fab_name = fab_name,fab_location_record_id = fab_location_record_id,quote_record_id = str(ContractRecordId),SAQSTE_cpqid = str(tuple(selected_rows_cpqid)).replace(',)',')') ))
			###update SAQFEA ends
			else:
				Sql.RunQuery("""INSERT SAQFEA (QUOTE_FAB_LOC_COV_OBJ_ASSEMBLY_RECORD_ID, EQUIPMENT_ID, EQUIPMENT_RECORD_ID, EQUIPMENT_DESCRIPTION, ASSEMBLY_ID, ASSEMBLY_STATUS, ASSEMBLY_DESCRIPTION, ASSEMBLY_RECORD_ID, FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, SERIAL_NUMBER, QUOTE_RECORD_ID, QUOTE_ID, QUOTE_NAME, EQUIPMENTCATEGORY_RECORD_ID, EQUIPMENTCATEGORY_ID, EQUIPMENTCATEGORY_DESCRIPTION, EQUIPMENTTYPE_DESCRIPTION, EQUIPMENTTYPE_RECORD_ID, GOT_CODE, MNT_PLANT_RECORD_ID, MNT_PLANT_ID, WARRANTY_START_DATE, WARRANTY_END_DATE, SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified ) SELECT A.* FROM (SELECT CONVERT(VARCHAR(4000),NEWID()) as QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID, MAEQUP.PAR_EQUIPMENT_ID, MAEQUP.PAR_EQUIPMENT_RECORD_ID, MAEQUP.PAR_EQUIPMENT_DESCRIPTION, SAQSTE.EQUIPMENT_ID, SAQSTE.EQUIPMENT_STATUS, SAQSTE.EQUIPMENT_DESCRIPTION, SAQSTE.EQUIPMENT_RECORD_ID, SAQSTE.FABLOCATION_ID, SAQSTE.FABLOCATION_NAME, SAQSTE.FABLOCATION_RECORD_ID, MAEQUP.SERIAL_NO,SAQSTE.QUOTE_RECORD_ID, SAQSTE.QUOTE_ID,SAQSTE.QUOTE_NAME, SAQSTE.EQUIPMENTCATEGORY_RECORD_ID, SAQSTE.EQUIPMENTCATEGORY_ID, SAQSTE.EQUIPMENTCATEGORY_DESCRIPTION, '' as EQUIPMENTTYPE_DESCRIPTION, MAEQUP.EQUIPMENTTYPE_RECORD_ID, MAEQUP.GOT_CODE, SAQSTE.MNT_PLANT_RECORD_ID, SAQSTE.MNT_PLANT_ID, MAEQUP.WARRANTY_START_DATE, MAEQUP.WARRANTY_END_DATE, MAEQUP.SALESORG_ID, MAEQUP.SALESORG_NAME, MAEQUP.SALESORG_RECORD_ID,'{UserName}' AS CPQTABLEENTRYADDEDBY,GETDATE() as CPQTABLEENTRYDATEADDED,'{UserId}' as CpqTableEntryModifiedBy,GETDATE() as CpqTableEntryDateModified  FROM MAEQUP (NOLOCK)INNER JOIN  SAQSTE on MAEQUP.PAR_EQUIPMENT_ID = SAQSTE.EQUIPMENT_ID  WHERE QUOTE_RECORD_ID = '{QuoteRecId}'AND SAQSTE.FABLOCATION_ID ='{fabid}' ) A LEFT JOIN SAQFEA M(NOLOCK) ON A.QUOTE_ID = M.QUOTE_ID AND A.EQUIPMENT_ID = M.ASSEMBLY_ID WHERE M.ASSEMBLY_ID IS NULL""".format(UserName=User.UserName,UserId=User.Id,QuoteRecId=ContractRecordId,fabid=VALUE))

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


	return ""



TITLE = Param.TITLE
VALUE = Param.VALUE
ELEMENT = Param.ELEMENT
CLICKEDID = Param.CLICKEDID
RECORDID = Param.RECORDID
if hasattr(Param, "selectPN"):

	selectPN = list(Param.selectPN)
else:
	selectPN = ""
try:
	SELECTALL = Param.SELECTALL
	Trace.Write("SELECTALL = "+str(SELECTALL))
except:
	SELECTALL = None

# Trace.Write("VALUE--------------------------->" + str(VALUE))

# Trace.Write("selectPN--------------------------->" + str(selectPN))
# Trace.Write("TITLE-----------xxx---- " + str(TITLE))
# Trace.Write("VALUE----------xx---------" + str(VALUE))
# Trace.Write("ELEMENT---------" + str(ELEMENT))
# Trace.Write("CLICKEDID-----679--------- " + str(CLICKEDID))
#Trace.Write("RECORDID--------xxx-----" + str(RECORDID))
if ELEMENT == "RELATEDEDIT":
	
	ApiResponse = ApiResponseFactory.JsonResponse(RELATEDMULTISELECTONEDIT(TITLE, VALUE, CLICKEDID, RECORDID))
elif ELEMENT == "SAVE":
	ApiResponse = ApiResponseFactory.JsonResponse(RELATEDMULTISELECTONSAVE(TITLE, VALUE, CLICKEDID, RECORDID,selectPN))
else:
	ApiResponse = ApiResponseFactory.JsonResponse("")


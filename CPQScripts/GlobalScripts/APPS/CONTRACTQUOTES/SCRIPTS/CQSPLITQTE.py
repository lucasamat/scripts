# =========================================================================================================================================
#   __script_name : CQSPLITQTE.PY
#   __script_description : THIS SCRIPT IS USED TO SPLIT THE ITEMS BY PRODUCT OFFERINGS
#   __primary_author__ : WASIM.ABDUL
#   __create_date :12-13-2021
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct
import clr
import System.Net
import sys
import re
from datetime import datetime
from System.Net import CookieContainer, NetworkCredential, Mail
from System.Text.Encoding import UTF8
from System import Convert
from System.Net.Mail import SmtpClient, MailAddress, Attachment, MailMessage
from SYDATABASE import SQL
Sql = SQL()

TestProduct = Webcom.Configurator.Scripting.Test.TestProduct() or "Sales"
try:
	contract_quote_rec_id = Quote.QuoteId
except:
	contract_quote_rec_id = ''

try:
	quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
except:
	quote_revision_record_id = ""

try:
	current_prod = Product.Name
	
except:
	current_prod = "Sales"
try:
	TabName = TestProduct.CurrentTab
except:
	TabName = "Quotes"

contract_quote_rec_id = Quote.GetGlobal("contract_quote_record_id")
quote_revision_rec_id = Quote.GetGlobal("quote_revision_record_id")
user_id = str(User.Id)
user_name = str(User.UserName) 

def _insert_equipment_entitlement():
	qtqsce_anc_query="""
					INSERT SAQSCE
					(KB_VERSION,ENTITLEMENT_XML,CONFIGURATION_STATUS,PAR_SERVICE_ID,PAR_SERVICE_RECORD_ID,PAR_SERVICE_DESCRIPTION,EQUIPMENT_ID,EQUIPMENT_RECORD_ID,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_RECORD_ID,QTEREV_ID,QTESRVCOB_RECORD_ID,QTESRVENT_RECORD_ID,SERIAL_NO,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,CPS_CONFIGURATION_ID,CPS_MATCH_ID,GREENBOOK,GREENBOOK_RECORD_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,QUOTE_SERVICE_COVERED_OBJ_ENTITLEMENTS_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED) 
					SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_COVERED_OBJ_ENTITLEMENTS_RECORD_ID, {UserId} as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM (
					SELECT 
					SAQTSE.KB_VERSION,SAQTSE.ENTITLEMENT_XML,SAQTSE.CONFIGURATION_STATUS,SAQTSE.PAR_SERVICE_ID,SAQTSE.PAR_SERVICE_RECORD_ID,SAQTSE.PAR_SERVICE_DESCRIPTION,SAQSCO.EQUIPMENT_ID,SAQSCO.EQUIPMENT_RECORD_ID,SAQTSE.QUOTE_ID,SAQTSE.QUOTE_RECORD_ID,SAQTSE.QTEREV_RECORD_ID,SAQTSE.QTEREV_ID,SAQSCO.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID as QTESRVCOB_RECORD_ID,SAQTSE.QUOTE_SERVICE_ENTITLEMENT_RECORD_ID as QTESRVENT_RECORD_ID,SAQSCO.SERIAL_NO,SAQTSE.SERVICE_DESCRIPTION,SAQTSE.SERVICE_ID,SAQTSE.SERVICE_RECORD_ID,SAQTSE.CPS_CONFIGURATION_ID,SAQTSE.CPS_MATCH_ID,SAQSCO.GREENBOOK,SAQSCO.GREENBOOK_RECORD_ID,SAQSCO.FABLOCATION_ID,SAQSCO.FABLOCATION_NAME,SAQSCO.FABLOCATION_RECORD_ID,SAQTSE.SALESORG_ID,SAQTSE.SALESORG_NAME,SAQTSE.SALESORG_RECORD_ID FROM
					SAQTSE (NOLOCK)
					JOIN SAQSCO (NOLOCK) ON SAQSCO.PAR_SERVICE_ID = SAQTSE.PAR_SERVICE_ID AND SAQSCO.SERVICE_ID = SAQTSE.SERVICE_ID AND SAQSCO.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID  AND SAQSCO.QTEREV_RECORD_ID = SAQTSE.QTEREV_RECORD_ID 
					
					WHERE SAQTSE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND ISNULL(SAQTSE.CONFIGURATION_STATUS,'') = 'COMPLETE' AND SAQTSE.QTEREV_RECORD_ID = '{revision_rec_id}' AND SAQTSE.SERVICE_ID = 'Z0105' AND SAQSCO.EQUIPMENT_ID not in (SELECT EQUIPMENT_ID FROM SAQSCE (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}'   AND QTEREV_RECORD_ID = '{revision_rec_id}'  AND SAQSCE.SERVICE_ID = 'Z0105')) IQ""".format(UserId=user_id, QuoteRecordId=contract_quote_rec_id, revision_rec_id = quote_revision_rec_id)
	Log.Info('@qtqsce_anc_query-renewal----179=---Qt_rec_id--'+str(qtqsce_anc_query))
	Sql.RunQuery(qtqsce_anc_query)

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
					display_val_dict[x[0]] = entitlement_display_value_tag_match[0].upper()
			entxmldict[x[0]]=sub_string
	return entxmldict

def _update_entitlement_values(par_service = ''):
	get_parent_xml = Sql.GetFirst("SELECT * FROM SAQTSE WHERE QUOTE_RECORD_ID ='{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID ='{}'".format(contract_quote_rec_id, quote_revision_rec_id ,par_service) )
	getall_recid = Sql.GetFirst("SELECT * FROM SAQTSE WHERE QUOTE_RECORD_ID ='{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID ='Z0105' AND PAR_SERVICE_ID = '{}' ".format(contract_quote_rec_id, quote_revision_rec_id ,par_service) )
	get_parent_dict = {}
	get_service_xml_dict = {}
	assign_xml = ""
	if get_parent_xml:
		get_parent_dict = _construct_dict_xml(get_parent_xml.ENTITLEMENT_XML)
	if getall_recid:
		get_service_xml_dict =  _construct_dict_xml(getall_recid.ENTITLEMENT_XML)
	if get_parent_dict and get_service_xml_dict:
		for key,value in get_service_xml_dict.items():
			temp_val = value
			if key in get_parent_dict.keys() or key == 'AGS_Z0105_PQB_SVSPPC' :
				Trace.Write("keyiffff- "+str(key)+" valueiffff- "+str(value))
				if key == 'AGS_Z0105_PQB_SVSPPC':
					#temp_val = get_parent_dict['AGS_Z0105_SPS_SPLIT_PER']
					pass
				else:
					temp_val = get_parent_dict[key]
			assign_xml += temp_val
		Sql.RunQuery("UPDATE SAQTSE SET ENTITLEMENT_XML = '{}' WHERE QUOTE_RECORD_ID ='{}' AND QTEREV_RECORD_ID = '{}' AND PAR_SERVICE_ID ='{}' AND SERVICE_ID ='Z0105'".format(assign_xml,contract_quote_rec_id, quote_revision_rec_id ,par_service) )
	

def _insert_service_level_entitlement(par_service=''):
	splitservice_object = 'Z0105'
	ent_disp_val = ent_val_code = ''
	get_tooltip = ''
	tbrow = {}
	request_url="https://cpservices-product-configuration.cfapps.us10.hana.ondemand.com/api/v2/configurations?autoCleanup=False"
	fullresponse = ScriptExecutor.ExecuteGlobal("CQENTLNVAL", {'action':'GET_RESPONSE','partnumber':splitservice_object,'request_url':request_url,'request_type':"New"})
	fullresponse=str(fullresponse).replace(": true",": \"true\"").replace(": false",": \"false\"")
	fullresponse= eval(fullresponse)
	##getting configuration_status status
	if fullresponse['complete'] == 'true':
		configuration_status = 'COMPLETE'
	elif fullresponse['complete'] == 'false':
		configuration_status = 'INCOMPLETE'
	else:
		configuration_status = 'ERROR'
	attributesdisallowedlst=[]
	attributeReadonlylst=[]
	attributesallowedlst=[]
	attributedefaultvalue = []
	overallattributeslist =[]
	attributevalues={}
	ProductVersionObj=Sql.GetFirst("Select product_id AS PRD_ID from product_versions(nolock) where SAPKBId = '"+str(fullresponse['kbId'])+"' AND SAPKBVersion='"+str(fullresponse['kbKey']['version'])+"'")
	if par_service :		
		get_existing_record = Sql.GetFirst("SELECT count(CpqTableEntryId) as cnt FROM SAQTSE WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND PAR_SERVICE_ID = '{}' AND SERVICE_ID ='Z0105'".format(contract_quote_rec_id, quote_revision_rec_id ,par_service))

		HasDefaultvalue=False
		for rootattribute, rootvalue in fullresponse.items():
			if rootattribute=="rootItem":
				for Productattribute, Productvalue in rootvalue.items():
					if Productattribute=="characteristics":
						for prdvalue in Productvalue:
							overallattributeslist.append(prdvalue['id'])

							if prdvalue['visible'] =='false':
								attributesdisallowedlst.append(prdvalue['id'])
							else:								
								attributesallowedlst.append(prdvalue['id'])
							if prdvalue['readOnly'] =='true':
								attributeReadonlylst.append(prdvalue['id'])
							for attribute in prdvalue['values']:								
								attributevalues[str(prdvalue['id'])]=attribute['value']
								if attribute["author"] in ('Default','System'):
									attributedefaultvalue.append(prdvalue["id"])
		attributesallowedlst = list(set(attributesallowedlst))
		overallattributeslist = list(set(overallattributeslist))
		if ProductVersionObj and get_existing_record.cnt == 0:
			get_service_values = Sql.GetFirst("SELECT * FROM SAQTSV WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND PAR_SERVICE_ID = '{}' AND SERVICE_ID ='Z0105'".format(contract_quote_rec_id, quote_revision_rec_id ,par_service))
			insertservice = ""
			for attrs in overallattributeslist:
				if attrs in attributevalues:
					HasDefaultvalue=True					
					STANDARD_ATTRIBUTE_VALUES=Sql.GetFirst("SELECT S.STANDARD_ATTRIBUTE_DISPLAY_VAL,S.STANDARD_ATTRIBUTE_CODE FROM STANDARD_ATTRIBUTE_VALUES (nolock) S INNER JOIN ATTRIBUTE_DEFN (NOLOCK) A ON A.STANDARD_ATTRIBUTE_CODE=S.STANDARD_ATTRIBUTE_CODE WHERE A.SYSTEM_ID = '{}' ".format(attrs))
					ent_disp_val = attributevalues[attrs]
					ent_val_code = attributevalues[attrs]
					#Log.Info("ent_disp_val----"+str(ent_disp_val))
				else:					
					HasDefaultvalue=False
					ent_disp_val = ""
					ent_val_code = ""
					STANDARD_ATTRIBUTE_VALUES=Sql.GetFirst("SELECT S.STANDARD_ATTRIBUTE_CODE FROM STANDARD_ATTRIBUTE_VALUES (nolock) S INNER JOIN ATTRIBUTE_DEFN (NOLOCK) A ON A.STANDARD_ATTRIBUTE_CODE=S.STANDARD_ATTRIBUTE_CODE WHERE A.SYSTEM_ID = '{}'".format(attrs))
				ATTRIBUTE_DEFN=Sql.GetFirst("SELECT * FROM ATTRIBUTE_DEFN (NOLOCK) WHERE SYSTEM_ID='{}'".format(attrs))
				PRODUCT_ATTRIBUTES=Sql.GetFirst("SELECT A.ATT_DISPLAY_DESC,P.ATTRDESC FROM ATT_DISPLAY_DEFN (NOLOCK) A INNER JOIN PRODUCT_ATTRIBUTES (NOLOCK) P ON A.ATT_DISPLAY=P.ATT_DISPLAY WHERE P.PRODUCT_ID={} AND P.STANDARD_ATTRIBUTE_CODE={}".format(ProductVersionObj.PRD_ID,STANDARD_ATTRIBUTE_VALUES.STANDARD_ATTRIBUTE_CODE))
				if PRODUCT_ATTRIBUTES:
					if PRODUCT_ATTRIBUTES.ATTRDESC:
						get_tooltip = PRODUCT_ATTRIBUTES.ATTRDESC
					if PRODUCT_ATTRIBUTES.ATT_DISPLAY_DESC in ('Drop Down','Check Box') and ent_disp_val:
						get_display_val = Sql.GetFirst("SELECT STANDARD_ATTRIBUTE_DISPLAY_VAL  from STANDARD_ATTRIBUTE_VALUES S INNER JOIN ATTRIBUTE_DEFN (NOLOCK) A ON A.STANDARD_ATTRIBUTE_CODE=S.STANDARD_ATTRIBUTE_CODE WHERE S.STANDARD_ATTRIBUTE_CODE = '{}' AND A.SYSTEM_ID = '{}' AND S.STANDARD_ATTRIBUTE_VALUE = '{}' ".format(STANDARD_ATTRIBUTE_VALUES.STANDARD_ATTRIBUTE_CODE,attrs,  attributevalues[attrs] ) )
						ent_disp_val = get_display_val.STANDARD_ATTRIBUTE_DISPLAY_VAL 
						
						getslaes_value  = Sql.GetFirst("SELECT SALESORG_ID FROM SAQTRV WHERE QUOTE_RECORD_ID = '"+str(contract_quote_rec_id)+"'")
						if getslaes_value:
							getquote_sales_val = getslaes_value.SALESORG_ID
						get_il_sales = Sql.GetList("select SALESORG_ID from SASORG where country = 'IL'")
						get_il_sales_list = [value.SALESORG_ID for value in get_il_sales]
				DTypeset={"Drop Down":"DropDown","Free Input, no Matching":"FreeInputNoMatching","Check Box":"CheckBox"}
				if ATTRIBUTE_DEFN.STANDARD_ATTRIBUTE_NAME:
					ent_desc = ATTRIBUTE_DEFN.STANDARD_ATTRIBUTE_NAME
				else:
					ent_desc = ''
				
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
				</QUOTE_ITEM_ENTITLEMENT>
				""".format(ent_name = str(attrs),ent_val_code = ent_val_code,ent_type = DTypeset[PRODUCT_ATTRIBUTES.ATT_DISPLAY_DESC] if PRODUCT_ATTRIBUTES else  '',ent_desc = ent_desc, tool_desc = get_tooltip.replace("'","''") if "'" in get_tooltip else get_tooltip,ent_disp_val = ent_disp_val if HasDefaultvalue==True else '',ct = '',pi = '',is_default = '1' if str(attrs) in attributedefaultvalue else '0',pm = '',cf = '')

			insertservice = insertservice.encode('ascii', 'ignore').decode('ascii')
			tbrow["QUOTE_SERVICE_ENTITLEMENT_RECORD_ID"]=str(Guid.NewGuid()).upper()
			tbrow["QUOTE_ID"]= get_service_values.QUOTE_ID
			tbrow["ENTITLEMENT_XML"]= insertservice
			tbrow["QUOTE_NAME"]=get_service_values.QUOTE_NAME
			tbrow["QUOTE_RECORD_ID"]=contract_quote_rec_id
			tbrow["QTESRV_RECORD_ID"]=get_service_values.SERVICE_RECORD_ID
			tbrow["SERVICE_RECORD_ID"]=get_service_values.SERVICE_RECORD_ID
			tbrow["SERVICE_ID"]= get_service_values.SERVICE_ID
			tbrow["SERVICE_DESCRIPTION"]=get_service_values.SERVICE_DESCRIPTION
			tbrow["CPS_CONFIGURATION_ID"]= fullresponse['id']
			tbrow["SALESORG_RECORD_ID"]=get_service_values.SALESORG_RECORD_ID
			tbrow["SALESORG_ID"]=get_service_values.SALESORG_ID
			tbrow["SALESORG_NAME"]=get_service_values.SALESORG_NAME
			tbrow["CPS_MATCH_ID"] = 1
			tbrow["CPQTABLEENTRYADDEDBY"] = user_id
			tbrow["CPQTABLEENTRYDATEADDED"] = datetime.now().strftime("%m/%d/%Y %H:%M:%S %p")
			tbrow["QTEREV_RECORD_ID"] = quote_revision_rec_id 
			tbrow["QTEREV_ID"] = get_service_values.QTEREV_ID
			tbrow["CONFIGURATION_STATUS"] = configuration_status
			tbrow["PAR_SERVICE_ID"] = get_service_values.PAR_SERVICE_ID
			tbrow["PAR_SERVICE_RECORD_ID"] = get_service_values.PAR_SERVICE_RECORD_ID
			tbrow["PAR_SERVICE_DESCRIPTION"] = get_service_values.PAR_SERVICE_DESCRIPTION
			columns = ', '.join("" + str(x) + "" for x in tbrow.keys())
			values = ', '.join("'" + str(x) + "'" for x in tbrow.values())
			insert_qtqtse_query = "INSERT INTO SAQTSE ( %s ) VALUES ( %s );" % (columns, values)
			Sql.RunQuery(insert_qtqtse_query)			
		
			try:
				_update_entitlement_values(par_service)
			except:
				pass

def _quote_items_entitlement_insert():
	Trace.Write("Insert saqite")
	service_id = 'Z0105'
	source_object_name = 'SAQSCE'
	join_condition_string = ''
	dynamic_group_id_value = 'null as ENTITLEMENT_GROUP_ID'
	dynamic_is_changed_value = 'null as IS_CHANGED'
	join_condition_string = ' AND SAQRIT.FABLOCATION_RECORD_ID = {ObjectName}.FABLOCATION_RECORD_ID AND SAQRIT.OBJECT_ID = {ObjectName}.EQUIPMENT_ID'.format(ObjectName=source_object_name)
	dynamic_group_id_value = '{ObjectName}.ENTITLEMENT_GROUP_ID'.format(ObjectName=source_object_name)
	dynamic_is_changed_value = '{ObjectName}.IS_CHANGED'.format(ObjectName=source_object_name)
	#if update: # need to verify one more time
	Sql.RunQuery("DELETE SAQITE FROM SAQITE WHERE SAQITE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQITE.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQITE.SERVICE_ID = '{ServiceId}'".format(QuoteRecordId=contract_quote_rec_id, QuoteRevisionRecordId=quote_revision_rec_id, ServiceId=service_id))
	
	Sql.RunQuery("""INSERT SAQITE (QUOTE_REV_ITEM_ENTITLEMENT_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified, CPS_CONFIGURATION_ID, CPS_MATCH_ID, ENTITLEMENT_COST_IMPACT, ENTITLEMENT_GROUP_ID, ENTITLEMENT_GROUP_XML, ENTITLEMENT_PRICE_IMPACT, ENTITLEMENT_XML, IS_CHANGED, LINE, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, QTEITM_RECORD_ID, QUOTE_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID)
				SELECT
					CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REV_ITEM_ENTITLEMENT_RECORD_ID,
					'{UserName}' AS CPQTABLEENTRYADDEDBY,
					GETDATE() as CPQTABLEENTRYDATEADDED,
					{UserId} as CpqTableEntryModifiedBy,
					GETDATE() as CpqTableEntryDateModified,
					{ObjectName}.CPS_CONFIGURATION_ID,
					{ObjectName}.CPS_MATCH_ID,
					null as ENTITLEMENT_COST_IMPACT,
					{dynamic_group_id_value},
					null as ENTITLEMENT_GROUP_XML,
					null as ENTITLEMENT_PRICE_IMPACT,
					{ObjectName}.ENTITLEMENT_XML,
					{dynamic_is_changed_value},
					SAQRIT.LINE,						
					SAQRIT.SERVICE_DESCRIPTION,
					SAQRIT.SERVICE_ID,
					SAQRIT.SERVICE_RECORD_ID,
					SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID,						
					SAQRIT.QUOTE_ID,
					SAQRIT.QUOTE_RECORD_ID,
					SAQRIT.QTEREV_ID,
					SAQRIT.QTEREV_RECORD_ID,						
					SAQRIT.GREENBOOK,
					SAQRIT.GREENBOOK_RECORD_ID
				FROM {ObjectName} (NOLOCK) 
				JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = {ObjectName}.QUOTE_RECORD_ID
											AND SAQRIT.SERVICE_RECORD_ID = {ObjectName}.SERVICE_RECORD_ID
											AND SAQRIT.QTEREV_RECORD_ID = {ObjectName}.QTEREV_RECORD_ID	
											AND ISNULL(SAQRIT.GREENBOOK_RECORD_ID,'') = ISNULL({ObjectName}.GREENBOOK_RECORD_ID,'')
											{JoinConditionString}			
				WHERE {ObjectName}.QUOTE_RECORD_ID = '{QuoteRecordId}' AND {ObjectName}.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND {ObjectName}.SERVICE_ID = '{ServiceId}' AND ISNULL({ObjectName}.CONFIGURATION_STATUS,'') = 'COMPLETE'			
			""".format(UserId=user_id, UserName=user_name, ObjectName=source_object_name, QuoteRecordId=contract_quote_rec_id, QuoteRevisionRecordId=quote_revision_rec_id, ServiceId=service_id, JoinConditionString=join_condition_string, dynamic_is_changed_value = dynamic_is_changed_value, dynamic_group_id_value = dynamic_group_id_value))
	return True
	
def splitserviceinsert():
	splitservice_object = 'Z0105'
	material_obj = Sql.GetFirst("SELECT MATERIAL_RECORD_ID,SAP_DESCRIPTION,MATERIALCONFIG_TYPE FROM MAMTRL WHERE SAP_PART_NUMBER = '{}'".format(splitservice_object))
	#delete Z0105
	Sql.RunQuery("DELETE FROM SAQTSV WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_rec_id}' AND SERVICE_ID LIKE '{ServiceId}%'".format(
			contract_quote_rec_id=contract_quote_rec_id,quote_revision_rec_id=quote_revision_rec_id,ServiceId=splitservice_object))
	service_list=[]
	#NEED TO change Query for SAQRIT
	get_existing_record = Sql.GetList("SELECT SERVICE_ID FROM SAQTSV WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_rec_id}'".format(contract_quote_rec_id = contract_quote_rec_id,quote_revision_rec_id =quote_revision_rec_id))
	for i in get_existing_record:
		service_list.append(i.SERVICE_ID)
	parservice_values=tuple(service_list)
	parservice_values=re.sub('\,\)',')',str(parservice_values))
	if get_existing_record:
		description = material_obj.SAP_DESCRIPTION
		material_record_id = material_obj.MATERIAL_RECORD_ID

		Sql.RunQuery("""INSERT SAQTSV (QTEREV_RECORD_ID,QTEREV_ID,QUOTE_ID, QUOTE_NAME,UOM_ID,UOM_RECORD_ID, QUOTE_RECORD_ID, SERVICE_DESCRIPTION, SERVICE_ID, PAR_SERVICE_ID,PAR_SERVICE_DESCRIPTION,PAR_SERVICE_RECORD_ID,SERVICE_RECORD_ID, SERVICE_TYPE, CONTRACT_VALID_FROM, CONTRACT_VALID_TO, SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID, QUOTE_SERVICE_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified)
						SELECT A.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED, {UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
						SELECT DISTINCT QTEREV_RECORD_ID, QTEREV_ID,QUOTE_ID, QUOTE_NAME,UOM_ID,UOM_RECORD_ID, QUOTE_RECORD_ID, '{description}' AS SERVICE_DESCRIPTION, '{splitservice_object}' AS SERVICE_ID,SERVICE_ID as PAR_SERVICE_ID,SERVICE_DESCRIPTION AS PAR_SERVICE_DESCRIPTION,QUOTE_SERVICE_RECORD_ID as PAR_SERVICE_RECORD_ID, '{material_record_id}' AS SERVICE_RECORD_ID, '' AS SERVICE_TYPE, CONTRACT_VALID_FROM, CONTRACT_VALID_TO, SALESORG_ID, SALESORG_NAME,SALESORG_RECORD_ID FROM SAQTSV (NOLOCK)
						WHERE SERVICE_ID IN {service_id} AND QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_rec_id}'
						) A""".format(description=description, service_id = parservice_values, material_record_id = material_record_id,contract_quote_rec_id = contract_quote_rec_id , quote_revision_rec_id = quote_revision_rec_id ,UserName = user_name, UserId = user_id,splitservice_object = splitservice_object ))
		
		##entitlement insert for service level 
		if service_list:
			Trace.Write("service_list---"+str(service_list))
			for par_service in service_list:
				_insert_service_level_entitlement(par_service)
	
	###split the items with new insert and updation:
	split_service =Sql.GetFirst("Select * FROM SAQTSV WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID ='Z0105'".format(contract_quote_rec_id,quote_revision_rec_id))
	splitservice_id = split_service.SERVICE_ID
	splitservice_name = split_service.SERVICE_DESCRIPTION
	splitservice_recid = split_service.SERVICE_RECORD_ID
	# SPLIT SAQRIS 
	equipmentservice_count = 0
	item_number_saqris_start = 0
	item_number_saqris_inc = 0
	quote_item_obj_service = Sql.GetFirst("SELECT TOP 1 LINE FROM SAQRIS (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' ORDER BY LINE DESC".format(QuoteRecordId=contract_quote_rec_id,RevisionRecordId=quote_revision_rec_id))
	if quote_item_obj_service:
		equipmentservice_count = int(quote_item_obj_service.LINE)
	doctype_service_obj = Sql.GetFirst("SELECT ITEM_NUMBER_START, ITEM_NUMBER_INCREMENT FROM SAQTRV LEFT JOIN SADOTY ON SADOTY.DOCTYPE_ID=SAQTRV.DOCTYP_ID WHERE SAQTRV.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQTRV.QTEREV_RECORD_ID = '{RevisionRecordId}'".format(QuoteRecordId=contract_quote_rec_id,RevisionRecordId=quote_revision_rec_id))
	if doctype_service_obj:
		item_number_saqris_start = int(doctype_service_obj.ITEM_NUMBER_START)
		item_number_saqris_inc = int(doctype_service_obj.ITEM_NUMBER_INCREMENT)
	
	get_split_service_object = Sql.GetFirst("SELECT SERVICE_ID FROM SAQRIS WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID = 'Z0105'".format(QuoteRecordId=contract_quote_rec_id,RevisionRecordId=quote_revision_rec_id))
	if not get_split_service_object:
		get_subtotal_off_details = Sql.GetFirst("SELECT DISTINCT COMMITTED_VALUE,CONTRACT_VALID_FROM,CONTRACT_VALID_TO,DIVISION_ID,DIVISION_RECORD_ID,DOC_CURRENCY,DOCCURR_RECORD_ID,ESTIMATED_VALUE,GLOBAL_CURRENCY,GLOBAL_CURRENCY_RECORD_ID,(({equipmentservice_count} + ROW_NUMBER()OVER(ORDER BY(SAQRIS.CpqTableEntryId))) * {item_number_saqris_inc}) as LINE,NET_PRICE,NET_PRICE_INGL_CURR,NET_VALUE,NET_VALUE_INGL_CURR,PLANT_ID,PLANT_RECORD_ID,SERVICE_ID,SERVICE_RECORD_ID,QUANTITY,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,TAX_PERCENTAGE,TAX_AMOUNT,TAX_AMOUNT_INGL_CURR,UNIT_PRICE,UNIT_PRICE_INGL_CURR FROM SAQRIS WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_rec_id}' ".format(contract_quote_rec_id=contract_quote_rec_id,quote_revision_rec_id = quote_revision_rec_id,equipmentservice_count =equipmentservice_count,item_number_saqris_inc =item_number_saqris_inc))
		
		

		primarykey = str(Guid.NewGuid()).upper()
		tableInfo = Sql.GetTable("SAQRIS")
		tablerow = {
			"QUOTE_REV_ITEM_SUMMARY_RECORD_ID": primarykey,
			"COMMITTED_VALUE": str(get_subtotal_off_details.COMMITTED_VALUE),
			"CONTRACT_VALID_FROM": str(get_subtotal_off_details.CONTRACT_VALID_FROM),
			"CONTRACT_VALID_TO": str(get_subtotal_off_details.CONTRACT_VALID_TO),
			"DIVISION_ID": str(get_subtotal_off_details.DIVISION_ID),
			"DIVISION_RECORD_ID": str(get_subtotal_off_details.DIVISION_RECORD_ID),
			"DOC_CURRENCY" : str(get_subtotal_off_details.DOC_CURRENCY),
			"DOCCURR_RECORD_ID": str(get_subtotal_off_details.DOCCURR_RECORD_ID),
			"ESTIMATED_VALUE": str(get_subtotal_off_details.ESTIMATED_VALUE),
			"GLOBAL_CURRENCY": str(get_subtotal_off_details.GLOBAL_CURRENCY),
			"GLOBAL_CURRENCY_RECORD_ID": str(get_subtotal_off_details.GLOBAL_CURRENCY_RECORD_ID),
			"LINE": str(get_subtotal_off_details.LINE),
			"NET_PRICE": str(get_subtotal_off_details.NET_PRICE),
			"NET_PRICE_INGL_CURR": str(get_subtotal_off_details.NET_PRICE_INGL_CURR),
			"NET_VALUE": str(get_subtotal_off_details.NET_VALUE),
			"NET_VALUE_INGL_CURR": str(get_subtotal_off_details.NET_VALUE_INGL_CURR),
			"PLANT_ID": str(get_subtotal_off_details.PLANT_ID),
			"PLANT_RECORD_ID": str(get_subtotal_off_details.PLANT_RECORD_ID),
			"SERVICE_ID": str(splitservice_id),
			"SERVICE_RECORD_ID": str(splitservice_recid),
			"SERVICE_DESCRIPTION": str(splitservice_name),
			"QUANTITY": str(get_subtotal_off_details.QUANTITY),
			"QUOTE_ID":str(get_subtotal_off_details.QUOTE_ID),
			"QUOTE_RECORD_ID": str(get_subtotal_off_details.QUOTE_RECORD_ID),
			"TAX_PERCENTAGE": str(get_subtotal_off_details.TAX_PERCENTAGE),
			"TAX_AMOUNT": str(get_subtotal_off_details.TAX_AMOUNT),
			"TAX_AMOUNT_INGL_CURR": str(get_subtotal_off_details.TAX_AMOUNT_INGL_CURR),
			"UNIT_PRICE": str(get_subtotal_off_details.UNIT_PRICE),
			"UNIT_PRICE_INGL_CURR": str(get_subtotal_off_details.UNIT_PRICE_INGL_CURR),
			"CPQTABLEENTRYDATEADDED":datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"),
			"CPQTABLEENTRYADDEDBY":user_name,
			"ADDUSR_RECORD_ID":user_id,
			"QTEREV_RECORD_ID":str(get_subtotal_off_details.QTEREV_RECORD_ID),
			"QTEREV_ID":str(get_subtotal_off_details.QTEREV_ID)
		}
		#Trace.Write(str(tablerow))
		tableInfo.AddRow(tablerow)
		Sql.Upsert(tableInfo)
		
	QueryStatement ="""MERGE SAQSCO SRC USING (SELECT 	
	QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,SERVICE_ID,SERVICE_DESCRIPTION,EQUIPMENT_DESCRIPTION,EQUIPMENT_RECORD_ID,FABLOCATION_RECORD_ID,FABLOCATION_ID,FABLOCATION_NAME,PARENTEQUIPMENT_ID,QUOTE_ID,QUOTE_NAME,QUOTE_RECORD_ID,QTESRV_RECORD_ID,SERVICE_TYPE,SERVICE_RECORD_ID,EQUIPMENTCATEGORY_ID,EQUIPMENTCATEGORY_RECORD_ID,EQUIPMENT_STATUS,GREENBOOK,EQUIPMENT_ID,SERIAL_NO,GREENBOOK_RECORD_ID,MNT_PLANT_ID,MNT_PLANT_NAME,PAR_SERVICE_DESCRIPTION,PAR_SERVICE_ID,MNT_PLANT_RECORD_ID,PLATFORM,PAR_SERVICE_RECORD_ID,PBG,WARRANTY_END_DATE, MATERIAL_RECORD_ID,SAP_PART_NUMBER,WARRANTY_START_DATE,CUSTOMER_TOOL_ID,TECHNOLOGY,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,EQUIPMENTCATEGORY_DESCRIPTION,EQUIPMENT_QUANTITY,ACCOUNT_ID,ACCOUNT_NAME,ACCOUNT_RECORD_ID,RELOCATION_EQUIPMENT_TYPE,SNDACC_ID,SNDACC_NAME,SNDACC_RECORD_ID,SNDFBL_ID,SNDFBL_NAME,SNDFBL_RECORD_ID,QTESRVFBL_RECORD_ID,QTESRVGBK_RECORD_ID,WARRANTY_END_DATE_ALERT,QTEREV_ID,QTEREV_RECORD_ID,INCLUDED,CONTRACT_VALID_FROM,CONTRACT_VALID_TO,KPU,SNDSOR_ID,SNDSOR_NAME,SNDSOR_RECORD_ID,WAFER_SIZE,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified FROM SAQSCO where QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID  = '{quote_revision_rec_id}'  )
	TGT ON (SRC.QUOTE_RECORD_ID = TGT.QUOTE_RECORD_ID AND SRC.QTEREV_RECORD_ID = TGT.QTEREV_RECORD_ID AND SRC.SERVICE_ID = 'Z0105')
	WHEN NOT MATCHED BY TARGET
	THEN INSERT(QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,SERVICE_ID,SERVICE_DESCRIPTION,EQUIPMENT_DESCRIPTION,EQUIPMENT_RECORD_ID,FABLOCATION_RECORD_ID,FABLOCATION_ID,FABLOCATION_NAME,PARENTEQUIPMENT_ID,QUOTE_ID,QUOTE_NAME,QUOTE_RECORD_ID,QTESRV_RECORD_ID,SERVICE_TYPE,SERVICE_RECORD_ID,EQUIPMENTCATEGORY_ID,EQUIPMENTCATEGORY_RECORD_ID,EQUIPMENT_STATUS,GREENBOOK,EQUIPMENT_ID,SERIAL_NO,GREENBOOK_RECORD_ID,MNT_PLANT_ID,MNT_PLANT_NAME,PAR_SERVICE_DESCRIPTION,PAR_SERVICE_ID,MNT_PLANT_RECORD_ID,PLATFORM,PAR_SERVICE_RECORD_ID,PBG,WARRANTY_END_DATE, MATERIAL_RECORD_ID,SAP_PART_NUMBER,WARRANTY_START_DATE,CUSTOMER_TOOL_ID,TECHNOLOGY,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,EQUIPMENTCATEGORY_DESCRIPTION,EQUIPMENT_QUANTITY,ACCOUNT_ID,ACCOUNT_NAME,ACCOUNT_RECORD_ID,RELOCATION_EQUIPMENT_TYPE,SNDACC_ID,SNDACC_NAME,SNDACC_RECORD_ID,SNDFBL_ID,SNDFBL_NAME,SNDFBL_RECORD_ID,QTESRVFBL_RECORD_ID,QTESRVGBK_RECORD_ID,WARRANTY_END_DATE_ALERT,QTEREV_ID,QTEREV_RECORD_ID,INCLUDED,CONTRACT_VALID_FROM,CONTRACT_VALID_TO,KPU,SNDSOR_ID,SNDSOR_NAME,SNDSOR_RECORD_ID,WAFER_SIZE,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified)
	VALUES (NEWID(),'{splitservice_id}','{splitservice_name}',EQUIPMENT_DESCRIPTION,EQUIPMENT_RECORD_ID,FABLOCATION_RECORD_ID,FABLOCATION_ID,FABLOCATION_NAME,PARENTEQUIPMENT_ID,QUOTE_ID,QUOTE_NAME,QUOTE_RECORD_ID,QTESRV_RECORD_ID,SERVICE_TYPE,'{splitservice_recid}',EQUIPMENTCATEGORY_ID,EQUIPMENTCATEGORY_RECORD_ID,EQUIPMENT_STATUS,GREENBOOK,EQUIPMENT_ID,SERIAL_NO,GREENBOOK_RECORD_ID,MNT_PLANT_ID,MNT_PLANT_NAME,SERVICE_DESCRIPTION,SERVICE_ID,MNT_PLANT_RECORD_ID,PLATFORM,SERVICE_RECORD_ID,PBG,WARRANTY_END_DATE, MATERIAL_RECORD_ID,SAP_PART_NUMBER,WARRANTY_START_DATE,CUSTOMER_TOOL_ID,TECHNOLOGY,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,EQUIPMENTCATEGORY_DESCRIPTION,EQUIPMENT_QUANTITY,ACCOUNT_ID,ACCOUNT_NAME,ACCOUNT_RECORD_ID,RELOCATION_EQUIPMENT_TYPE,SNDACC_ID,SNDACC_NAME,SNDACC_RECORD_ID,SNDFBL_ID,SNDFBL_NAME,SNDFBL_RECORD_ID,QTESRVFBL_RECORD_ID,QTESRVGBK_RECORD_ID,WARRANTY_END_DATE_ALERT,QTEREV_ID,QTEREV_RECORD_ID,INCLUDED,CONTRACT_VALID_FROM,CONTRACT_VALID_TO,KPU,SNDSOR_ID,SNDSOR_NAME,SNDSOR_RECORD_ID,WAFER_SIZE,'{UserName}','{datetimenow}','{UserId}','{datetimenow}');""".format(contract_quote_rec_id=contract_quote_rec_id,quote_revision_rec_id = quote_revision_rec_id,splitservice_recid = splitservice_recid,splitservice_id=splitservice_id,splitservice_name = splitservice_name,UserId=user_id,UserName=user_name,datetimenow=datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"))
	Sql.RunQuery(QueryStatement)

	##equipment level entitlement insert
	_insert_equipment_entitlement()

	
	##INSERT FOR SAQRIT
	service_entitlement_objs = Sql.GetList("""SELECT SERVICE_ID, ENTITLEMENT_XML FROM  SAQTSE (NOLOCK) WHERE QUOTE_RECORD_ID ='{contract_quote_rec_id}' AND QTEREV_RECORD_ID ='{quote_revision_rec_id}'""".format(contract_quote_rec_id=contract_quote_rec_id,quote_revision_rec_id=quote_revision_rec_id) )
	for service_entitlement_obj in service_entitlement_objs:
		entitlement_display_value_tag_match = ''
		split_entitlement_display_value = ''
		quote_item_tag_pattern = re.compile(r'(<QUOTE_ITEM_ENTITLEMENT>[\w\W]*?</QUOTE_ITEM_ENTITLEMENT>)')
		entitlement_id_tag_pattern = re.compile(r'<ENTITLEMENT_ID>AGS_'+str(service_entitlement_obj.SERVICE_ID)+'_PQB_QTITST</ENTITLEMENT_ID>')
		##getting billing type
		billing_type_pattern = re.compile(r'<ENTITLEMENT_ID>AGS_'+str(service_entitlement_obj.SERVICE_ID)+'_PQB_BILTYP</ENTITLEMENT_ID>')
		entitlement_display_value_tag_pattern = re.compile(r'<ENTITLEMENT_DISPLAY_VALUE>([^>]*?)</ENTITLEMENT_DISPLAY_VALUE>')
		entitlement_split_id = re.compile(r'<ENTITLEMENT_ID>AGS_'+str(service_entitlement_obj.SERVICE_ID)+'_PQB_SPLQTE</ENTITLEMENT_ID>')
		for quote_item_tag in re.finditer(quote_item_tag_pattern, service_entitlement_obj.ENTITLEMENT_XML):
			quote_item_tag_content = quote_item_tag.group(1)
			entitlement_id_tag_match = re.findall(entitlement_id_tag_pattern,quote_item_tag_content)	
			entitlement_billing_id_tag_match = re.findall(billing_type_pattern,quote_item_tag_content)
			entitlement_split_match_id = re.findall(entitlement_split_id,quote_item_tag_content)
			if entitlement_id_tag_match:
				entitlement_display_value_tag_match = re.findall(entitlement_display_value_tag_pattern,quote_item_tag_content)
			if entitlement_split_match_id:
				split_entitlement_display_value = re.findall(entitlement_display_value_tag_pattern,quote_item_tag_content)
			if entitlement_display_value_tag_match and split_entitlement_display_value:
				quote_service_entitlement_type = entitlement_display_value_tag_match[0].upper()
				if quote_service_entitlement_type == 'OFFERING + EQUIPMENT' and split_entitlement_display_value == ["Yes"]:
					Trace.Write("1")
					servicelevel_split_equip(service_entitlement_obj.SERVICE_ID)
					break
				elif quote_service_entitlement_type in ('OFFERING + FAB + GREENBOOK + GROUP OF EQUIPMENT', 'OFFERING + GREENBOOK + GR EQUI', 'OFFERING + CHILD GROUP OF PART') and split_entitlement_display_value == ["Yes"]:
					Trace.Write("2")
					servicelevel_split_green(service_entitlement_obj.SERVICE_ID)
					break
		##saqite insert
		_quote_items_entitlement_insert()
	LOGIN_CREDENTIALS = SqlHelper.GetFirst("SELECT USER_NAME as Username,Password,Domain FROM SYCONF where Domain='AMAT_TST'")
	if LOGIN_CREDENTIALS is not None:
		Login_Username = str(LOGIN_CREDENTIALS.Username)
		Login_Password = str(LOGIN_CREDENTIALS.Password)
		authorization = Login_Username+":"+Login_Password
		binaryAuthorization = UTF8.GetBytes(authorization)
		authorization = Convert.ToBase64String(binaryAuthorization)
		authorization = "Basic " + authorization


		webclient = System.Net.WebClient()
		webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/json"
		webclient.Headers[System.Net.HttpRequestHeader.Authorization] = authorization;
		
		result = '''<?xml version="1.0" encoding="UTF-8"?><soapenv:Envelope	xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">	<soapenv:Body><CPQ_Columns>	<QUOTE_ID>{Qt_Id}</QUOTE_ID><REVISION_ID>{Rev_Id}</REVISION_ID></CPQ_Columns></soapenv:Body></soapenv:Envelope>'''.format( Qt_Id= contract_quote_rec_id,Rev_Id = quote_revision_rec_id)
		
		LOGIN_CRE = SqlHelper.GetFirst("SELECT URL FROM SYCONF where EXTERNAL_TABLE_NAME ='BILLING_MATRIX_ASYNC'")
		Async = webclient.UploadString(str(LOGIN_CRE.URL), str(result))


def servicelevel_split_equip(seid):
	Trace.Write("SAQSCE_SPLIT"+str(seid))
	#seid ="Z0091"
	where_condition = "WHERE SERVICE_ID = ''"+str(seid)+"'' AND QUOTE_RECORD_ID = ''"+str(contract_quote_rec_id)+"'' and QTEREV_RECORD_ID = ''"+str(quote_revision_rec_id)+"''  "
	get_c4c_quote_id = Sql.GetFirst("select * from SAQTMT where MASTER_TABLE_QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_rec_id}'".format(contract_quote_rec_id =contract_quote_rec_id,quote_revision_rec_id = quote_revision_rec_id))
	ent_temp = "ENT_SPLIT_BKP_"+str(get_c4c_quote_id.C4C_QUOTE_ID)

	Trace.Write("aaaaaaa"+str(ent_temp))
	ent_child_temp_drop = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(ent_temp)+"'' ) BEGIN DROP TABLE "+str(ent_temp)+" END  ' ")

	SqlHelper.GetFirst("sp_executesql @T=N'declare @H int; Declare @val Varchar(MAX);DECLARE @XML XML; SELECT @val =  replace(replace(STUFF((SELECT ''''+FINAL from(select  REPLACE(entitlement_xml,''<QUOTE_ITEM_ENTITLEMENT>'',sml) AS FINAL FROM (select ''  <QUOTE_ITEM_ENTITLEMENT><QUOTE_ID>''+quote_id+''</QUOTE_ID><QUOTE_RECORD_ID>''+QUOTE_RECORD_ID+''</QUOTE_RECORD_ID><QTEREV_RECORD_ID>''+QTEREV_RECORD_ID+''</QTEREV_RECORD_ID><SERVICE_ID>''+service_id+''</SERVICE_ID><FABLOCATION_ID>''+FABLOCATION_ID+''</FABLOCATION_ID><GREENBOOK>''+GREENBOOK+''</GREENBOOK><EQUIPMENT_ID>''+equipment_id+''</EQUIPMENT_ID>'' AS sml,replace(replace(replace(replace(replace(replace(replace(replace(ENTITLEMENT_XML,''&'','';#38''),'''','';#39''),'' < '','' &lt; '' ),'' > '','' &gt; '' ),''_>'',''_&gt;''),''_<'',''_&lt;''),''&'','';#38''),''<10%'',''&lt;10%'')  as entitlement_xml from SAQSCE(nolock) "+str(where_condition)+" )A )a FOR XML PATH ('''')), 1, 1, ''''),''&lt;'',''<''),''&gt;'',''>'')  SELECT @XML = CONVERT(XML,''<ROOT>''+@VAL+''</ROOT>'') exec sys.sp_xml_preparedocument @H output,@XML; select QUOTE_ID,QUOTE_RECORD_ID,QTEREV_RECORD_ID,EQUIPMENT_ID,SERVICE_ID,ENTITLEMENT_ID,ENTITLEMENT_NAME,ENTITLEMENT_COST_IMPACT,FABLOCATION_ID,GREENBOOK,ENTITLEMENT_VALUE_CODE,ENTITLEMENT_DISPLAY_VALUE,ENTITLEMENT_PRICE_IMPACT,IS_DEFAULT,ENTITLEMENT_TYPE,ENTITLEMENT_DESCRIPTION,PRICE_METHOD,CALCULATION_FACTOR INTO "+str(ent_temp)+"  from openxml(@H, ''ROOT/QUOTE_ITEM_ENTITLEMENT'', 0) with (QUOTE_ID VARCHAR(100) ''QUOTE_ID'',QUOTE_RECORD_ID VARCHAR(100) ''QUOTE_RECORD_ID'',QTEREV_RECORD_ID VARCHAR(100) ''QTEREV_RECORD_ID'',EQUIPMENT_ID VARCHAR(100) ''EQUIPMENT_ID'',ENTITLEMENT_NAME VARCHAR(100) ''ENTITLEMENT_NAME'',ENTITLEMENT_ID VARCHAR(100) ''ENTITLEMENT_ID'',SERVICE_ID VARCHAR(100) ''SERVICE_ID'',ENTITLEMENT_COST_IMPACT VARCHAR(100) ''ENTITLEMENT_COST_IMPACT'',FABLOCATION_ID VARCHAR(100) ''FABLOCATION_ID'',GREENBOOK VARCHAR(100) ''GREENBOOK'',ENTITLEMENT_VALUE_CODE VARCHAR(100) ''ENTITLEMENT_VALUE_CODE'',ENTITLEMENT_DISPLAY_VALUE VARCHAR(100) ''ENTITLEMENT_DISPLAY_VALUE'',ENTITLEMENT_PRICE_IMPACT VARCHAR(100) ''ENTITLEMENT_PRICE_IMPACT'',IS_DEFAULT VARCHAR(100) ''IS_DEFAULT'',ENTITLEMENT_TYPE VARCHAR(100) ''ENTITLEMENT_TYPE'',ENTITLEMENT_DESCRIPTION VARCHAR(100) ''ENTITLEMENT_DESCRIPTION'',PRICE_METHOD VARCHAR(100) ''PRICE_METHOD'',CALCULATION_FACTOR VARCHAR(100) ''CALCULATION_FACTOR'') ; exec sys.sp_xml_removedocument @H; '")

	#a = SqlHelper.GetList("select * from ENT_SPLIT_BKP_3050008527 where ENTITLEMENT_ID  ='AGS_Z0091_SER_SPLIT_PER'")
	#updating the split percent from Xml
	entitlement_service_id = 'AGS_'+str(seid)+'_SER_SPLIT_PER'
	updatesaqritchild ="""UPDATE A SET A.SPLIT_PERCENT =  replace(B.ENTITLEMENT_DISPLAY_VALUE,'%','')  FROM SAQRIT A JOIN {ent_temp} B ON A.QUOTE_RECORD_ID =B.QUOTE_RECORD_ID  AND A.QTEREV_RECORD_ID  =B.QTEREV_RECORD_ID AND A.SERVICE_ID =B.SERVICE_ID AND A.FABLOCATION_ID  = B.FABLOCATION_ID AND A.GREENBOOK  = B.GREENBOOK AND A.OBJECT_ID = B.EQUIPMENT_ID WHERE  A.QUOTE_RECORD_ID ='{contract_quote_rec_id}' AND A.QTEREV_RECORD_ID='{quote_revision_rec_id}' AND A.SERVICE_ID ='{seid}' AND B.ENTITLEMENT_ID  ='{entitlement_service_id}'""".format(contract_quote_rec_id =contract_quote_rec_id,quote_revision_rec_id =quote_revision_rec_id,ent_temp = ent_temp,entitlement_service_id =entitlement_service_id,seid =seid)
	Sql.RunQuery(updatesaqritchild)
	ent_child_temp_drop = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(ent_temp)+"'' ) BEGIN DROP TABLE "+str(ent_temp)+" END  ' ")
	##INSERTING CHILD TO PARENT SERVICE.
	split_service =Sql.GetFirst("Select * FROM SAQTSV WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID ='Z0105'".format(contract_quote_rec_id,quote_revision_rec_id,seid))
	splitservice_id = split_service.SERVICE_ID
	splitservice_name = split_service.SERVICE_DESCRIPTION
	splitservice_recid = split_service.SERVICE_RECORD_ID
	equipments_count = 0
	item_number_saqrit_start = 0
	item_number_saqrit_inc = 0
	quote_item_obj = Sql.GetFirst("SELECT TOP 1 LINE FROM SAQRIT (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' ORDER BY LINE DESC".format(QuoteRecordId=contract_quote_rec_id,RevisionRecordId=quote_revision_rec_id))
	if quote_item_obj:
		equipments_count = int(quote_item_obj.LINE)
	doctype_obj = Sql.GetFirst("SELECT ITEM_NUMBER_START, ITEM_NUMBER_INCREMENT FROM SAQTRV LEFT JOIN SADOTY ON SADOTY.DOCTYPE_ID=SAQTRV.DOCTYP_ID WHERE SAQTRV.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQTRV.QTEREV_RECORD_ID = '{RevisionRecordId}'".format(QuoteRecordId=contract_quote_rec_id,RevisionRecordId=quote_revision_rec_id))
	if doctype_obj:
		item_number_saqrit_start = int(doctype_obj.ITEM_NUMBER_START)
		item_number_saqrit_inc = int(doctype_obj.ITEM_NUMBER_INCREMENT)
	
	Sql.RunQuery("""INSERT SAQRIT (CONTRACT_VALID_FROM,CONTRACT_VALID_TO,DOC_CURRENCY,DOCURR_RECORD_ID,EXCHANGE_RATE,EXCHANGE_RATE_DATE,EXCHANGE_RATE_RECORD_ID,GL_ACCOUNT_NO,GLOBAL_CURRENCY,GLOBAL_CURRENCY_RECORD_ID,LINE,OBJECT_ID,OBJECT_TYPE,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,PROFIT_CENTER,QUANTITY,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,REF_SALESORDER,TAX_PERCENTAGE,TAX_AMOUNT,TAX_AMOUNT_INGL_CURR,TAXCLASSIFICATION_DESCRIPTION,TAXCLASSIFICATION_ID,TAXCLASSIFICATION_RECORD_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,GREENBOOK,GREENBOOK_RECORD_ID,NET_PRICE,NET_PRICE_INGL_CURR,PLANT_ID,PLANT_NAME,PLANT_RECORD_ID,COMVAL_INGL_CURR,ESTVAL_INGL_CURR,NET_VALUE,NET_VALUE_INGL_CURR,UNIT_PRICE,UNIT_PRICE_INGL_CURR,QTEITMSUM_RECORD_ID,MODULE_ID,MODULE_NAME,MODULE_RECORD_ID,PARQTEITM_LINE,PARQTEITM_LINE_RECORD_ID,BILLING_TYPE,COMMITTED_VALUE,ESTIMATED_VALUE,SPLIT_PERCENT,SPLIT,STATUS,QUOTE_REVISION_CONTRACT_ITEM_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified) 
	SELECT A.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REVISION_CONTRACT_ITEM_ID,'{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED, {UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
	SELECT DISTINCT CONTRACT_VALID_FROM,CONTRACT_VALID_TO,DOC_CURRENCY,DOCURR_RECORD_ID,EXCHANGE_RATE,EXCHANGE_RATE_DATE,EXCHANGE_RATE_RECORD_ID,GL_ACCOUNT_NO,GLOBAL_CURRENCY,GLOBAL_CURRENCY_RECORD_ID,(({equipments_count} + ROW_NUMBER()OVER(ORDER BY(SAQRIT.CpqTableEntryId))) * {item_number_saqrit_inc}) AS LINE,OBJECT_ID,OBJECT_TYPE,'{splitservice_name}' as SERVICE_DESCRIPTION,'{splitservice_id}' as SERVICE_ID,'{splitservice_recid}' as SERVICE_RECORD_ID,PROFIT_CENTER,QUANTITY,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,REF_SALESORDER,TAX_PERCENTAGE,TAX_AMOUNT,TAX_AMOUNT_INGL_CURR,TAXCLASSIFICATION_DESCRIPTION,TAXCLASSIFICATION_ID,TAXCLASSIFICATION_RECORD_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,GREENBOOK,GREENBOOK_RECORD_ID,NET_PRICE ,NET_PRICE_INGL_CURR,PLANT_ID,PLANT_NAME,PLANT_RECORD_ID,COMVAL_INGL_CURR,ESTVAL_INGL_CURR,NET_VALUE ,NET_VALUE_INGL_CURR,UNIT_PRICE,UNIT_PRICE_INGL_CURR,QTEITMSUM_RECORD_ID,MODULE_ID,MODULE_NAME,MODULE_RECORD_ID,LINE AS PARQTEITM_LINE,QUOTE_REVISION_CONTRACT_ITEM_ID AS PARQTEITM_LINE_RECORD_ID,BILLING_TYPE,COMMITTED_VALUE,ESTIMATED_VALUE,SPLIT_PERCENT,SPLIT,'ACQUIRED' AS STATUS FROM SAQRIT WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_rec_id}' AND SERVICE_ID = '{seid}' AND ISNULL(SPLIT,'')='')A""".format(contract_quote_rec_id = contract_quote_rec_id , quote_revision_rec_id = quote_revision_rec_id,item_number_saqrit_inc =item_number_saqrit_inc,equipments_count =equipments_count,splitservice_recid = splitservice_recid,splitservice_id=splitservice_id,splitservice_name = splitservice_name,seid = seid,UserId=user_id,UserName=user_name))
	
	#UPDATE PRICING TO CLONE RECORD AS WELL AS MASTER
	update_pricing = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET A.NET_PRICE = (CASE WHEN ISNULL(A.PARQTEITM_LINE_RECORD_ID,'''')='''' AND ISNULL(A.PARQTEITM_LINE,'''') = '''' THEN NET_PRICE * XY.SPLIT_PERCENT/100 WHEN A.PARQTEITM_LINE_RECORD_ID <> A.QUOTE_REVISION_CONTRACT_ITEM_ID AND ISNULL(A.PARQTEITM_LINE,'''') <> ''''  and ISNULL(A.PARQTEITM_LINE_RECORD_ID,'''') <> '''' THEN NET_PRICE * (100-XY.SPLIT_PERCENT)/100 END),A.NET_PRICE_INGL_CURR = (CASE WHEN ISNULL(A.PARQTEITM_LINE_RECORD_ID,'''')='''' AND ISNULL(A.PARQTEITM_LINE,'''') = '''' THEN NET_PRICE_INGL_CURR * XY.SPLIT_PERCENT/100 WHEN A.PARQTEITM_LINE_RECORD_ID <> A.QUOTE_REVISION_CONTRACT_ITEM_ID AND ISNULL(A.PARQTEITM_LINE,'''') <> ''''  and ISNULL(A.PARQTEITM_LINE_RECORD_ID,'''') <> '''' THEN NET_PRICE_INGL_CURR * (100-XY.SPLIT_PERCENT)/100 END),A.NET_VALUE = (CASE WHEN ISNULL(A.PARQTEITM_LINE_RECORD_ID,'''')='''' AND ISNULL(A.PARQTEITM_LINE,'''') = '''' THEN NET_PRICE * XY.SPLIT_PERCENT/100 WHEN A.PARQTEITM_LINE_RECORD_ID <> A.QUOTE_REVISION_CONTRACT_ITEM_ID AND ISNULL(A.PARQTEITM_LINE,'''') <> ''''  and ISNULL(A.PARQTEITM_LINE_RECORD_ID,'''') <> '''' THEN NET_PRICE * (100-XY.SPLIT_PERCENT)/100 END) + TAX_AMOUNT,A.NET_VALUE_INGL_CURR = (CASE WHEN ISNULL(A.PARQTEITM_LINE_RECORD_ID,'''')='''' AND ISNULL(A.PARQTEITM_LINE,'''') = '''' THEN NET_PRICE_INGL_CURR * XY.SPLIT_PERCENT/100 WHEN A.PARQTEITM_LINE_RECORD_ID <> A.QUOTE_REVISION_CONTRACT_ITEM_ID AND ISNULL(A.PARQTEITM_LINE,'''') <> ''''  and ISNULL(A.PARQTEITM_LINE_RECORD_ID,'''') <> '''' THEN NET_PRICE_INGL_CURR * (100-XY.SPLIT_PERCENT)/100 END) + TAX_AMOUNT,A.SPLIT = ''YES'',A.SPLIT_PERCENT = (CASE WHEN ISNULL(A.PARQTEITM_LINE_RECORD_ID,'''')='''' AND ISNULL(A.PARQTEITM_LINE,'''') = '''' THEN XY.SPLIT_PERCENT WHEN A.PARQTEITM_LINE_RECORD_ID <> A.QUOTE_REVISION_CONTRACT_ITEM_ID AND ISNULL(A.PARQTEITM_LINE,'''') <> ''''  and ISNULL(A.PARQTEITM_LINE_RECORD_ID,'''') <> '''' THEN 100-XY.SPLIT_PERCENT END),A.UNIT_PRICE_INGL_CURR = (CASE WHEN A.PARQTEITM_LINE_RECORD_ID <> A.QUOTE_REVISION_CONTRACT_ITEM_ID AND ISNULL(A.PARQTEITM_LINE,'''') <> ''''  and ISNULL(A.PARQTEITM_LINE_RECORD_ID,'''') <> '''' THEN NET_PRICE_INGL_CURR * (100-XY.SPLIT_PERCENT)/100 END),A.UNIT_PRICE = (CASE WHEN A.PARQTEITM_LINE_RECORD_ID <> A.QUOTE_REVISION_CONTRACT_ITEM_ID AND ISNULL(A.PARQTEITM_LINE,'''') <> ''''  and ISNULL(A.PARQTEITM_LINE_RECORD_ID,'''') <> '''' THEN NET_PRICE * (100-XY.SPLIT_PERCENT)/100 END) FROM SAQRIT(NOLOCK)A INNER JOIN(SELECT DISTINCT B.SPLIT_PERCENT,B.QUOTE_RECORD_ID,B.QTEREV_RECORD_ID,B.OBJECT_ID FROM SAQRIT B(NOLOCK) WHERE B.QUOTE_RECORD_ID = ''"+str(contract_quote_rec_id)+"'' AND B.SERVICE_ID = ''"+str(seid)+"'') AS XY ON A.QUOTE_RECORD_ID = XY.QUOTE_RECORD_ID AND A.QTEREV_RECORD_ID = XY.QTEREV_RECORD_ID AND A.OBJECT_ID = XY.OBJECT_ID  WHERE A.QUOTE_RECORD_ID = ''"+str(contract_quote_rec_id)+"'' AND ISNULL(A.SPLIT,'''')<>''YES'' AND A.SERVICE_ID IN( ''"+str(seid)+"'' ,''"+str(splitservice_id)+"'')'".format(contract_quote_rec_id =contract_quote_rec_id,seid =seid,splitservice_id = splitservice_id))
	#SUM UPTO SAQRIS:
	update_service_parent_summary = """UPDATE A  SET A.NET_PRICE = B.NET_PRICE,A.NET_PRICE_INGL_CURR = B.NET_PRICE_INGL_CURR,A.NET_VALUE = B.NET_VALUE,A.NET_VALUE_INGL_CURR = B.NET_VALUE_INGL_CURR,A.UNIT_PRICE = B.UNIT_PRICE,A.UNIT_PRICE_INGL_CURR = B.UNIT_PRICE_INGL_CURR FROM SAQRIS A(NOLOCK) JOIN (SELECT SUM(NET_PRICE) AS NET_PRICE,SUM(NET_PRICE_INGL_CURR) AS NET_PRICE_INGL_CURR,SUM(NET_VALUE) AS NET_VALUE,SUM(NET_VALUE_INGL_CURR) AS NET_VALUE_INGL_CURR,SUM(UNIT_PRICE) AS UNIT_PRICE,SUM(UNIT_PRICE_INGL_CURR) AS UNIT_PRICE_INGL_CURR,QUOTE_RECORD_ID,QTEREV_RECORD_ID,SERVICE_ID from SAQRIT(NOLOCK) WHERE QUOTE_RECORD_ID ='{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_rec_id}'  AND SERVICE_ID = '{seid}' GROUP BY QUOTE_RECORD_ID,QTEREV_RECORD_ID,SERVICE_ID) B ON A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.SERVICE_ID=B.SERVICE_ID AND A.QTEREV_RECORD_ID = B.QTEREV_RECORD_ID """.format(contract_quote_rec_id= contract_quote_rec_id,quote_revision_rec_id = quote_revision_rec_id,seid =seid)
	Sql.RunQuery(update_service_parent_summary)
	update_service_child_summary = """UPDATE A  SET A.NET_PRICE = B.NET_PRICE,A.NET_PRICE_INGL_CURR = B.NET_PRICE_INGL_CURR,A.NET_VALUE = B.NET_VALUE,A.NET_VALUE_INGL_CURR = B.NET_VALUE_INGL_CURR,A.UNIT_PRICE = B.UNIT_PRICE,A.UNIT_PRICE_INGL_CURR = B.UNIT_PRICE_INGL_CURR FROM SAQRIS A(NOLOCK) JOIN (SELECT SUM(NET_PRICE) AS NET_PRICE,SUM(NET_PRICE_INGL_CURR) AS NET_PRICE_INGL_CURR,SUM(NET_VALUE) AS NET_VALUE,SUM(NET_VALUE_INGL_CURR) AS NET_VALUE_INGL_CURR,SUM(UNIT_PRICE) AS UNIT_PRICE,SUM(UNIT_PRICE_INGL_CURR) AS UNIT_PRICE_INGL_CURR,QUOTE_RECORD_ID,QTEREV_RECORD_ID,SERVICE_ID from SAQRIT(NOLOCK) WHERE QUOTE_RECORD_ID ='{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_rec_id}'  AND SERVICE_ID = '{splitservice_id}' GROUP BY QUOTE_RECORD_ID,QTEREV_RECORD_ID,SERVICE_ID) B ON A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.SERVICE_ID=B.SERVICE_ID AND A.QTEREV_RECORD_ID = B.QTEREV_RECORD_ID """.format(contract_quote_rec_id= contract_quote_rec_id,quote_revision_rec_id = quote_revision_rec_id,seid =seid,splitservice_id =splitservice_id)
	Sql.RunQuery(update_service_child_summary)
	#Object list grid
	saqrioinsert ="""MERGE SAQRIO SRC USING (SELECT A.QUOTE_REVISION_ITEM_OBJECT_RECORD_ID,A.CUSTOMER_TOOL_ID,A.EQUIPMENT_DESCRIPTION,A.EQUIPMENT_ID,A.EQUIPMENT_RECORD_ID,A.GREENBOOK,A.GREENBOOK_RECORD_ID,A.KPU,B.LINE,B.SERVICE_DESCRIPTION,B.SERVICE_ID,B.SERVICE_RECORD_ID,A.QUOTE_ID,A.QTEITM_RECORD_ID,A.QUOTE_RECORD_ID,A.QTEREV_ID,A.QTEREV_RECORD_ID,A.SERIAL_NUMBER,A.TECHNOLOGY,A.TOOL_CONFIGURATION,A.WAFER_SIZE,B.QUOTE_REVISION_CONTRACT_ITEM_ID,B.CPQTABLEENTRYADDEDBY,B.CPQTABLEENTRYDATEADDED,B.CpqTableEntryModifiedBy,B.CpqTableEntryDateModified FROM SAQRIO(NOLOCK) A JOIN SAQRIT (NOLOCK) B ON A.QUOTE_RECORD_ID  = B.QUOTE_RECORD_ID AND A.LINE = B.PARQTEITM_LINE where B.QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND B.QTEREV_RECORD_ID  = '{quote_revision_rec_id}' AND B.SERVICE_ID = '{splitservice_id}')
	TGT ON (SRC.QUOTE_RECORD_ID = TGT.QUOTE_RECORD_ID AND SRC.QTEREV_RECORD_ID = TGT.QTEREV_RECORD_ID AND SRC.SERVICE_ID = '{splitservice_id}')
	WHEN NOT MATCHED BY TARGET
	THEN INSERT(QUOTE_REVISION_ITEM_OBJECT_RECORD_ID,CUSTOMER_TOOL_ID,EQUIPMENT_DESCRIPTION,EQUIPMENT_ID,EQUIPMENT_RECORD_ID,GREENBOOK,GREENBOOK_RECORD_ID,KPU,LINE,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,QUOTE_ID,QTEITM_RECORD_ID,QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,SERIAL_NUMBER,TECHNOLOGY,TOOL_CONFIGURATION,WAFER_SIZE,CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified)
	VALUES (NEWID(),CUSTOMER_TOOL_ID,EQUIPMENT_DESCRIPTION,EQUIPMENT_ID,EQUIPMENT_RECORD_ID,GREENBOOK,GREENBOOK_RECORD_ID,KPU,LINE,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,QUOTE_ID,QUOTE_REVISION_CONTRACT_ITEM_ID,QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,SERIAL_NUMBER,TECHNOLOGY,TOOL_CONFIGURATION,WAFER_SIZE,'{UserName}','{datetimenow}','{UserId}','{datetimenow}');""".format(contract_quote_rec_id=contract_quote_rec_id,quote_revision_rec_id = quote_revision_rec_id,splitservice_id =splitservice_id,UserId=user_id,UserName=user_name,datetimenow=datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"))
	Sql.RunQuery(saqrioinsert)
	annaul_line_insert = ScriptExecutor.ExecuteGlobal("CQINSQTITM",{"ContractQuoteRecordId":contract_quote_rec_id, "ContractQuoteRevisionRecordId":quote_revision_rec_id, "ServiceId":splitservice_id, "ActionType":'INSERT_LINE_ITEMS'})
	#Updating net price for Annualised grid
	update_annual_grid_split_service = """UPDATE SAQICO SET SAQICO.NET_PRICE_INGL_CURR = CAST(CAST(A.NET_PRICE_INGL_CURR AS DECIMAL(13,5))/(SELECT count(*) FROM SAQICO Y(NOLOCK)WHERE Y.QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND Y.QTEREV_RECORD_ID ='{quote_revision_rec_id}' AND SERVICE_ID='{splitservice_id}')AS DECIMAL(13,5)) FROM SAQICO X(NOLOCK) INNER JOIN (SELECT NET_PRICE_INGL_CURR,SERVICE_ID,QUOTE_REVISION_CONTRACT_ITEM_ID FROM SAQRIT (NOLOCK) WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID ='{quote_revision_rec_id}' AND SERVICE_ID='{splitservice_id}' Group By NET_PRICE_INGL_CURR,SERVICE_ID,QUOTE_REVISION_CONTRACT_ITEM_ID )A ON X.QTEITM_RECORD_ID = A.QUOTE_REVISION_CONTRACT_ITEM_ID AND X.SERVICE_ID = A.SERVICE_ID WHERE X.QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND X.QTEREV_RECORD_ID ='{quote_revision_rec_id}' """.format(contract_quote_rec_id= contract_quote_rec_id,quote_revision_rec_id = quote_revision_rec_id,splitservice_id =splitservice_id)
	Sql.RunQuery(update_annual_grid_split_service)
	update_annual_grid_split_service_adjustment ="""Update XY SET XY.NET_PRICE_INGL_CURR = XY.NET_PRICE_INGL_CURR + (SELECT CAST(A.NET_PRICE_INGL_CURR AS DECIMAL(13,5))- CAST(sum(B.NET_PRICE_INGL_CURR)AS DECIMAL(13,5)) from SAQRIT A(NOLOCK) JOIN SAQICO B(NOLOCK) ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID WHERE A.QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND A.QTEREV_RECORD_ID ='{quote_revision_rec_id}' AND A.SERVICE_ID='{splitservice_id}' GROUP BY B.NET_PRICE_INGL_CURR,A.NET_PRICE_INGL_CURR) FROM SAQICO XY(NOLOCK) WHERE XY.QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND XY.QTEREV_RECORD_ID ='{quote_revision_rec_id}'AND XY.SERVICE_ID='{splitservice_id}' AND XY.CpqTableEntryId = (SELECT MAX(Y.CpqTableEntryId) FROM SAQICO Y(NOLOCK) WHERE Y.QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND Y.QTEREV_RECORD_ID ='{quote_revision_rec_id}' AND Y.SERVICE_ID='{splitservice_id}')""".format(contract_quote_rec_id= contract_quote_rec_id,quote_revision_rec_id = quote_revision_rec_id,splitservice_id =splitservice_id)
	Sql.RunQuery(update_annual_grid_split_service_adjustment)
	global_year_1 ="""UPDATE X SET X.YEAR_1_INGL_CURR = CASE A.[YEAR] WHEN 'YEAR 1' THEN CAST(A.NET_PRICE_INGL_CURR AS DECIMAL(13,5)) ELSE NULL END FROM SAQRIT X(NOLOCK) INNER JOIN (SELECT DISTINCT NET_PRICE_INGL_CURR,SERVICE_ID,QTEITM_RECORD_ID,[YEAR] FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID ='{quote_revision_rec_id}' AND SERVICE_ID='{splitservice_id}' AND ISNULL([YEAR],'') = 'YEAR 1' GROUP BY NET_PRICE_INGL_CURR,SERVICE_ID,QUOTE_ITEM_COVERED_OBJECT_RECORD_ID,[YEAR] ,QTEITM_RECORD_ID)A ON X.QUOTE_REVISION_CONTRACT_ITEM_ID = A.QTEITM_RECORD_ID AND X.SERVICE_ID = A.SERVICE_ID""".format(contract_quote_rec_id= contract_quote_rec_id,quote_revision_rec_id = quote_revision_rec_id,splitservice_id =splitservice_id)
	Sql.RunQuery(global_year_1)
	global_year_2 ="""UPDATE X SET X.YEAR_2_INGL_CURR = CASE A.[YEAR] WHEN 'YEAR 2' THEN CAST(A.NET_PRICE_INGL_CURR AS DECIMAL(13,5)) ELSE NULL END FROM SAQRIT X(NOLOCK) INNER JOIN (SELECT DISTINCT NET_PRICE_INGL_CURR,SERVICE_ID,QTEITM_RECORD_ID,[YEAR] FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID ='{quote_revision_rec_id}' AND SERVICE_ID='{splitservice_id}' AND ISNULL([YEAR],'') = 'YEAR 2' GROUP BY NET_PRICE_INGL_CURR,SERVICE_ID,QUOTE_ITEM_COVERED_OBJECT_RECORD_ID,[YEAR] ,QTEITM_RECORD_ID)A ON X.QUOTE_REVISION_CONTRACT_ITEM_ID = A.QTEITM_RECORD_ID AND X.SERVICE_ID = A.SERVICE_ID""".format(contract_quote_rec_id= contract_quote_rec_id,quote_revision_rec_id = quote_revision_rec_id,splitservice_id =splitservice_id)
	Sql.RunQuery(global_year_2)
	global_year_3 ="""UPDATE X SET X.YEAR_3_INGL_CURR = CASE A.[YEAR] WHEN 'YEAR 3' THEN CAST(A.NET_PRICE_INGL_CURR AS DECIMAL(13,5)) ELSE NULL END FROM SAQRIT X(NOLOCK) INNER JOIN (SELECT DISTINCT NET_PRICE_INGL_CURR,SERVICE_ID,QTEITM_RECORD_ID,[YEAR] FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID ='{quote_revision_rec_id}' AND SERVICE_ID='{splitservice_id}' AND ISNULL([YEAR],'') = 'YEAR 3' GROUP BY NET_PRICE_INGL_CURR,SERVICE_ID,QUOTE_ITEM_COVERED_OBJECT_RECORD_ID,[YEAR] ,QTEITM_RECORD_ID)A ON X.QUOTE_REVISION_CONTRACT_ITEM_ID = A.QTEITM_RECORD_ID AND X.SERVICE_ID = A.SERVICE_ID""".format(contract_quote_rec_id= contract_quote_rec_id,quote_revision_rec_id = quote_revision_rec_id,splitservice_id =splitservice_id)
	Sql.RunQuery(global_year_3)
	global_year_4 ="""UPDATE X SET X.YEAR_4_INGL_CURR = CASE A.[YEAR] WHEN 'YEAR 4' THEN CAST(A.NET_PRICE_INGL_CURR AS DECIMAL(13,5)) ELSE NULL END FROM SAQRIT X(NOLOCK) INNER JOIN (SELECT DISTINCT NET_PRICE_INGL_CURR,SERVICE_ID,QTEITM_RECORD_ID,[YEAR] FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID ='{quote_revision_rec_id}' AND SERVICE_ID='{splitservice_id}' AND ISNULL([YEAR],'') = 'YEAR 4' GROUP BY NET_PRICE_INGL_CURR,SERVICE_ID,QUOTE_ITEM_COVERED_OBJECT_RECORD_ID,[YEAR] ,QTEITM_RECORD_ID)A ON X.QUOTE_REVISION_CONTRACT_ITEM_ID = A.QTEITM_RECORD_ID AND X.SERVICE_ID = A.SERVICE_ID""".format(contract_quote_rec_id= contract_quote_rec_id,quote_revision_rec_id = quote_revision_rec_id,splitservice_id =splitservice_id)
	Sql.RunQuery(global_year_4)
	global_year_5 ="""UPDATE X SET X.YEAR_5_INGL_CURR = CASE A.[YEAR] WHEN 'YEAR 5' THEN CAST(A.NET_PRICE_INGL_CURR AS DECIMAL(13,5)) ELSE NULL END FROM SAQRIT X(NOLOCK) INNER JOIN (SELECT DISTINCT NET_PRICE_INGL_CURR,SERVICE_ID,QTEITM_RECORD_ID,[YEAR] FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID ='{quote_revision_rec_id}' AND SERVICE_ID='{splitservice_id}' AND ISNULL([YEAR],'') = 'YEAR 5' GROUP BY NET_PRICE_INGL_CURR,SERVICE_ID,QUOTE_ITEM_COVERED_OBJECT_RECORD_ID,[YEAR] ,QTEITM_RECORD_ID)A ON X.QUOTE_REVISION_CONTRACT_ITEM_ID = A.QTEITM_RECORD_ID AND X.SERVICE_ID = A.SERVICE_ID""".format(contract_quote_rec_id= contract_quote_rec_id,quote_revision_rec_id = quote_revision_rec_id,splitservice_id =splitservice_id)
	Sql.RunQuery(global_year_5)
	document_years="""UPDATE SAQRIT SET 
		SAQRIT.YEAR_1 = CASE WHEN YEAR_1_INGL_CURR IS NULL THEN NULL ELSE
		CAST(CAST(NET_PRICE AS DECIMAL(13,5))/(SELECT count(*) FROM SAQICO Y(NOLOCK)WHERE Y.QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND Y.QTEREV_RECORD_ID ='{quote_revision_rec_id}' AND SERVICE_ID='{splitservice_id}')AS DECIMAL(13,5)) END,
		SAQRIT.YEAR_2 = CASE WHEN YEAR_2_INGL_CURR IS NULL THEN  NULL ELSE 
		CAST(CAST(NET_PRICE AS DECIMAL(13,5))/(SELECT count(*) FROM SAQICO Y(NOLOCK)WHERE Y.QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND Y.QTEREV_RECORD_ID ='{quote_revision_rec_id}' AND SERVICE_ID='{splitservice_id}')AS DECIMAL(13,5)) END,
		SAQRIT.YEAR_3 = CASE WHEN YEAR_3_INGL_CURR IS NULL THEN  NULL ELSE 
		CAST(CAST(NET_PRICE AS DECIMAL(13,5))/(SELECT count(*) FROM SAQICO Y(NOLOCK)WHERE Y.QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND Y.QTEREV_RECORD_ID ='{quote_revision_rec_id}' AND SERVICE_ID='{splitservice_id}')AS DECIMAL(13,5)) END,
		SAQRIT.YEAR_4 = CASE WHEN YEAR_4_INGL_CURR IS NULL THEN  NULL ELSE
		CAST(CAST(NET_PRICE AS DECIMAL(13,5))/(SELECT count(*) FROM SAQICO Y(NOLOCK)WHERE Y.QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND Y.QTEREV_RECORD_ID ='{quote_revision_rec_id}' AND SERVICE_ID='{splitservice_id}')AS DECIMAL(13,5)) END,
		SAQRIT.YEAR_5 = CASE WHEN YEAR_5_INGL_CURR IS NULL THEN  NULL ELSE
		CAST(CAST(NET_PRICE AS DECIMAL(13,5))/(SELECT count(*) FROM SAQICO Y(NOLOCK)WHERE Y.QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND Y.QTEREV_RECORD_ID ='{quote_revision_rec_id}' AND SERVICE_ID='{splitservice_id}')AS DECIMAL(13,5)) END
		FROM SAQRIT X(NOLOCK)
		WHERE X.QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND X.QTEREV_RECORD_ID ='{quote_revision_rec_id}' AND SERVICE_ID ='{splitservice_id}' """.format(contract_quote_rec_id= contract_quote_rec_id,quote_revision_rec_id = quote_revision_rec_id,splitservice_id =splitservice_id)
	Sql.RunQuery(document_years)
	document_years_adjustments ="UPDATE SAQRIT SET YEAR_1 = YEAR_1 + (NET_PRICE - (ISNULL(YEAR_1,0)+ISNULL(YEAR_2,0)+ISNULL(YEAR_3,0)+ISNULL(YEAR_4,0)+ISNULL(YEAR_5,0))) FROM SAQRIT WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID ='{quote_revision_rec_id}' AND SERVICE_ID='{splitservice_id}')""".format(contract_quote_rec_id= contract_quote_rec_id,quote_revision_rec_id = quote_revision_rec_id,splitservice_id =splitservice_id)
	Sql.RunQuery(document_years_adjustments)

	
	#CQIFWUDQTM = ScriptExecutor.ExecuteGlobal("CQIFWUDQTM",{"QT_REC_ID":get_c4c_quote_id.QUOTE_ID})


def servicelevel_split_green(seid):
	Trace.Write("thisgreen service"+str(seid))
	where_condition = "WHERE SERVICE_ID = ''"+str(seid)+"'' AND QUOTE_RECORD_ID = ''"+str(contract_quote_rec_id)+"'' and QTEREV_RECORD_ID = ''"+str(quote_revision_rec_id)+"''  "
	get_c4c_quote_id = Sql.GetFirst("select * from SAQTMT where MASTER_TABLE_QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_rec_id}'".format(contract_quote_rec_id =contract_quote_rec_id,quote_revision_rec_id = quote_revision_rec_id))
	ent_temp = "ENT_SPLIT_BKP_"+str(get_c4c_quote_id.C4C_QUOTE_ID)

	Trace.Write("aaaaaaa"+str(ent_temp))
	ent_child_temp_drop = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(ent_temp)+"'' ) BEGIN DROP TABLE "+str(ent_temp)+" END  ' ")

	SqlHelper.GetFirst("sp_executesql @T=N'declare @H int; Declare @val Varchar(MAX);DECLARE @XML XML; SELECT @val =  replace(replace(STUFF((SELECT ''''+FINAL from(select  REPLACE(entitlement_xml,''<QUOTE_ITEM_ENTITLEMENT>'',sml) AS FINAL FROM (select ''  <QUOTE_ITEM_ENTITLEMENT><QUOTE_ID>''+quote_id+''</QUOTE_ID><QUOTE_RECORD_ID>''+QUOTE_RECORD_ID+''</QUOTE_RECORD_ID><QTEREV_RECORD_ID>''+QTEREV_RECORD_ID+''</QTEREV_RECORD_ID><SERVICE_ID>''+service_id+''</SERVICE_ID><FABLOCATION_ID>''+FABLOCATION_ID+''</FABLOCATION_ID><GREENBOOK>''+GREENBOOK+''</GREENBOOK><EQUIPMENT_ID>''+equipment_id+''</EQUIPMENT_ID>'' AS sml,replace(replace(replace(replace(replace(replace(replace(replace(ENTITLEMENT_XML,''&'','';#38''),'''','';#39''),'' < '','' &lt; '' ),'' > '','' &gt; '' ),''_>'',''_&gt;''),''_<'',''_&lt;''),''&'','';#38''),''<10%'',''&lt;10%'')  as entitlement_xml from SAQSCE(nolock) "+str(where_condition)+" )A )a FOR XML PATH ('''')), 1, 1, ''''),''&lt;'',''<''),''&gt;'',''>'')  SELECT @XML = CONVERT(XML,''<ROOT>''+@VAL+''</ROOT>'') exec sys.sp_xml_preparedocument @H output,@XML; select QUOTE_ID,QUOTE_RECORD_ID,QTEREV_RECORD_ID,EQUIPMENT_ID,SERVICE_ID,ENTITLEMENT_ID,ENTITLEMENT_NAME,ENTITLEMENT_COST_IMPACT,FABLOCATION_ID,GREENBOOK,ENTITLEMENT_VALUE_CODE,ENTITLEMENT_DISPLAY_VALUE,ENTITLEMENT_PRICE_IMPACT,IS_DEFAULT,ENTITLEMENT_TYPE,ENTITLEMENT_DESCRIPTION,PRICE_METHOD,CALCULATION_FACTOR INTO "+str(ent_temp)+"  from openxml(@H, ''ROOT/QUOTE_ITEM_ENTITLEMENT'', 0) with (QUOTE_ID VARCHAR(100) ''QUOTE_ID'',QUOTE_RECORD_ID VARCHAR(100) ''QUOTE_RECORD_ID'',QTEREV_RECORD_ID VARCHAR(100) ''QTEREV_RECORD_ID'',EQUIPMENT_ID VARCHAR(100) ''EQUIPMENT_ID'',ENTITLEMENT_NAME VARCHAR(100) ''ENTITLEMENT_NAME'',ENTITLEMENT_ID VARCHAR(100) ''ENTITLEMENT_ID'',SERVICE_ID VARCHAR(100) ''SERVICE_ID'',ENTITLEMENT_COST_IMPACT VARCHAR(100) ''ENTITLEMENT_COST_IMPACT'',FABLOCATION_ID VARCHAR(100) ''FABLOCATION_ID'',GREENBOOK VARCHAR(100) ''GREENBOOK'',ENTITLEMENT_VALUE_CODE VARCHAR(100) ''ENTITLEMENT_VALUE_CODE'',ENTITLEMENT_DISPLAY_VALUE VARCHAR(100) ''ENTITLEMENT_DISPLAY_VALUE'',ENTITLEMENT_PRICE_IMPACT VARCHAR(100) ''ENTITLEMENT_PRICE_IMPACT'',IS_DEFAULT VARCHAR(100) ''IS_DEFAULT'',ENTITLEMENT_TYPE VARCHAR(100) ''ENTITLEMENT_TYPE'',ENTITLEMENT_DESCRIPTION VARCHAR(100) ''ENTITLEMENT_DESCRIPTION'',PRICE_METHOD VARCHAR(100) ''PRICE_METHOD'',CALCULATION_FACTOR VARCHAR(100) ''CALCULATION_FACTOR'') ; exec sys.sp_xml_removedocument @H; '")

	#a = SqlHelper.GetList("select * from ENT_SPLIT_BKP_3050008527 where ENTITLEMENT_ID  ='AGS_Z0091_SER_SPLIT_PER'")
	#updating the split percent from Xml
	entitlement_service_id = 'AGS_'+str(seid)+'_SER_SPLIT_PER'
	updatesaqritchild ="""UPDATE A SET A.SPLIT_PERCENT =  replace(B.ENTITLEMENT_DISPLAY_VALUE,'%','')  FROM SAQRIT A JOIN {ent_temp} B ON A.QUOTE_RECORD_ID =B.QUOTE_RECORD_ID  AND A.QTEREV_RECORD_ID  =B.QTEREV_RECORD_ID AND A.SERVICE_ID =B.SERVICE_ID AND A.FABLOCATION_ID  = B.FABLOCATION_ID AND A.GREENBOOK  = B.GREENBOOK WHERE  A.QUOTE_RECORD_ID ='{contract_quote_rec_id}' AND A.QTEREV_RECORD_ID='{quote_revision_rec_id}' AND A.SERVICE_ID ='{seid}' AND B.ENTITLEMENT_ID  ='{entitlement_service_id}'""".format(contract_quote_rec_id =contract_quote_rec_id,quote_revision_rec_id =quote_revision_rec_id,ent_temp = ent_temp,entitlement_service_id =entitlement_service_id,seid =seid)
	Sql.RunQuery(updatesaqritchild)
	ent_child_temp_drop = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(ent_temp)+"'' ) BEGIN DROP TABLE "+str(ent_temp)+" END  ' ")
	##INSERTING CHILD TO PARENT SERVICE.
	split_service =Sql.GetFirst("Select * FROM SAQTSV WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID ='Z0105'".format(contract_quote_rec_id,quote_revision_rec_id))
	splitservice_id = split_service.SERVICE_ID
	splitservice_name = split_service.SERVICE_DESCRIPTION
	splitservice_recid = split_service.SERVICE_RECORD_ID
	equipments_count = 0
	item_number_saqrit_start = 0
	item_number_saqrit_inc = 0
	quote_item_obj = Sql.GetFirst("SELECT TOP 1 LINE FROM SAQRIT (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' ORDER BY LINE DESC".format(QuoteRecordId=contract_quote_rec_id,RevisionRecordId=quote_revision_rec_id))
	if quote_item_obj:
		equipments_count = int(quote_item_obj.LINE)
	doctype_obj = Sql.GetFirst("SELECT ITEM_NUMBER_START, ITEM_NUMBER_INCREMENT FROM SAQTRV LEFT JOIN SADOTY ON SADOTY.DOCTYPE_ID=SAQTRV.DOCTYP_ID WHERE SAQTRV.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQTRV.QTEREV_RECORD_ID = '{RevisionRecordId}'".format(QuoteRecordId=contract_quote_rec_id,RevisionRecordId=quote_revision_rec_id))
	if doctype_obj:
		item_number_saqrit_start = int(doctype_obj.ITEM_NUMBER_START)
		item_number_saqrit_inc = int(doctype_obj.ITEM_NUMBER_INCREMENT)
	
	Sql.RunQuery("""INSERT SAQRIT (CONTRACT_VALID_FROM,CONTRACT_VALID_TO,DOC_CURRENCY,DOCURR_RECORD_ID,EXCHANGE_RATE,EXCHANGE_RATE_DATE,EXCHANGE_RATE_RECORD_ID,GL_ACCOUNT_NO,GLOBAL_CURRENCY,GLOBAL_CURRENCY_RECORD_ID,LINE,OBJECT_ID,OBJECT_TYPE,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,PROFIT_CENTER,QUANTITY,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,REF_SALESORDER,TAX_PERCENTAGE,TAX_AMOUNT,TAX_AMOUNT_INGL_CURR,TAXCLASSIFICATION_DESCRIPTION,TAXCLASSIFICATION_ID,TAXCLASSIFICATION_RECORD_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,GREENBOOK,GREENBOOK_RECORD_ID,NET_PRICE,NET_PRICE_INGL_CURR,PLANT_ID,PLANT_NAME,PLANT_RECORD_ID,COMVAL_INGL_CURR,ESTVAL_INGL_CURR,NET_VALUE,NET_VALUE_INGL_CURR,UNIT_PRICE,UNIT_PRICE_INGL_CURR,QTEITMSUM_RECORD_ID,MODULE_ID,MODULE_NAME,MODULE_RECORD_ID,PARQTEITM_LINE,PARQTEITM_LINE_RECORD_ID,BILLING_TYPE,COMMITTED_VALUE,ESTIMATED_VALUE,SPLIT_PERCENT,SPLIT,STATUS,QUOTE_REVISION_CONTRACT_ITEM_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified) 
		SELECT A.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REVISION_CONTRACT_ITEM_ID,'{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED, {UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
	SELECT DISTINCT CONTRACT_VALID_FROM,CONTRACT_VALID_TO,DOC_CURRENCY,DOCURR_RECORD_ID,EXCHANGE_RATE,EXCHANGE_RATE_DATE,EXCHANGE_RATE_RECORD_ID,GL_ACCOUNT_NO,GLOBAL_CURRENCY,GLOBAL_CURRENCY_RECORD_ID,(({equipments_count} + ROW_NUMBER()OVER(ORDER BY(SAQRIT.CpqTableEntryId))) * {item_number_saqrit_inc}) AS LINE,OBJECT_ID,OBJECT_TYPE,'{splitservice_name}' as SERVICE_DESCRIPTION,'{splitservice_id}' as SERVICE_ID,'{splitservice_recid}' as SERVICE_RECORD_ID,PROFIT_CENTER,QUANTITY,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,REF_SALESORDER,TAX_PERCENTAGE,TAX_AMOUNT,TAX_AMOUNT_INGL_CURR,TAXCLASSIFICATION_DESCRIPTION,TAXCLASSIFICATION_ID,TAXCLASSIFICATION_RECORD_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,GREENBOOK,GREENBOOK_RECORD_ID,NET_PRICE ,NET_PRICE_INGL_CURR,PLANT_ID,PLANT_NAME,PLANT_RECORD_ID,COMVAL_INGL_CURR,ESTVAL_INGL_CURR,NET_VALUE ,NET_VALUE_INGL_CURR,UNIT_PRICE,UNIT_PRICE_INGL_CURR,QTEITMSUM_RECORD_ID,MODULE_ID,MODULE_NAME,MODULE_RECORD_ID,LINE AS PARQTEITM_LINE,QUOTE_REVISION_CONTRACT_ITEM_ID AS PARQTEITM_LINE_RECORD_ID,BILLING_TYPE,COMMITTED_VALUE,ESTIMATED_VALUE,SPLIT_PERCENT,SPLIT, 'ACQUIRED' as STATUS FROM SAQRIT WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_rec_id}' AND SERVICE_ID = '{seid}' AND ISNULL(SPLIT,'')='')A""".format(contract_quote_rec_id = contract_quote_rec_id , quote_revision_rec_id = quote_revision_rec_id,item_number_saqrit_inc =item_number_saqrit_inc,equipments_count =equipments_count,splitservice_recid = splitservice_recid,splitservice_id=splitservice_id,splitservice_name = splitservice_name,seid = seid,UserId=user_id,UserName=user_name))
	
	update_pricing = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET A.NET_PRICE = (CASE WHEN ISNULL(A.PARQTEITM_LINE_RECORD_ID,'''')='''' AND ISNULL(A.PARQTEITM_LINE,'''') = '''' THEN NET_PRICE * XY.SPLIT_PERCENT/100 WHEN A.PARQTEITM_LINE_RECORD_ID <> A.QUOTE_REVISION_CONTRACT_ITEM_ID AND ISNULL(A.PARQTEITM_LINE,'''') <> ''''  and ISNULL(A.PARQTEITM_LINE_RECORD_ID,'''') <> '''' THEN NET_PRICE * (100-XY.SPLIT_PERCENT)/100 END),A.NET_PRICE_INGL_CURR = (CASE WHEN ISNULL(A.PARQTEITM_LINE_RECORD_ID,'''')='''' AND ISNULL(A.PARQTEITM_LINE,'''') = '''' THEN NET_PRICE_INGL_CURR * XY.SPLIT_PERCENT/100 WHEN A.PARQTEITM_LINE_RECORD_ID <> A.QUOTE_REVISION_CONTRACT_ITEM_ID AND ISNULL(A.PARQTEITM_LINE,'''') <> ''''  and ISNULL(A.PARQTEITM_LINE_RECORD_ID,'''') <> '''' THEN NET_PRICE_INGL_CURR * (100-XY.SPLIT_PERCENT)/100 END),A.NET_VALUE = (CASE WHEN ISNULL(A.PARQTEITM_LINE_RECORD_ID,'''')='''' AND ISNULL(A.PARQTEITM_LINE,'''') = '''' THEN NET_PRICE * XY.SPLIT_PERCENT/100 WHEN A.PARQTEITM_LINE_RECORD_ID <> A.QUOTE_REVISION_CONTRACT_ITEM_ID AND ISNULL(A.PARQTEITM_LINE,'''') <> ''''  and ISNULL(A.PARQTEITM_LINE_RECORD_ID,'''') <> '''' THEN NET_PRICE * (100-XY.SPLIT_PERCENT)/100 END) + TAX_AMOUNT,A.NET_VALUE_INGL_CURR = (CASE WHEN ISNULL(A.PARQTEITM_LINE_RECORD_ID,'''')='''' AND ISNULL(A.PARQTEITM_LINE,'''') = '''' THEN NET_PRICE_INGL_CURR * XY.SPLIT_PERCENT/100 WHEN A.PARQTEITM_LINE_RECORD_ID <> A.QUOTE_REVISION_CONTRACT_ITEM_ID AND ISNULL(A.PARQTEITM_LINE,'''') <> ''''  and ISNULL(A.PARQTEITM_LINE_RECORD_ID,'''') <> '''' THEN NET_PRICE_INGL_CURR * (100-XY.SPLIT_PERCENT)/100 END) + TAX_AMOUNT,A.SPLIT = ''YES'',A.SPLIT_PERCENT = (CASE WHEN ISNULL(A.PARQTEITM_LINE_RECORD_ID,'''')='''' AND ISNULL(A.PARQTEITM_LINE,'''') = '''' THEN XY.SPLIT_PERCENT WHEN A.PARQTEITM_LINE_RECORD_ID <> A.QUOTE_REVISION_CONTRACT_ITEM_ID AND ISNULL(A.PARQTEITM_LINE,'''') <> ''''  and ISNULL(A.PARQTEITM_LINE_RECORD_ID,'''') <> '''' THEN 100-XY.SPLIT_PERCENT END),A.UNIT_PRICE_INGL_CURR = (CASE WHEN A.PARQTEITM_LINE_RECORD_ID <> A.QUOTE_REVISION_CONTRACT_ITEM_ID AND ISNULL(A.PARQTEITM_LINE,'''') <> ''''  and ISNULL(A.PARQTEITM_LINE_RECORD_ID,'''') <> '''' THEN NET_PRICE_INGL_CURR * (100-XY.SPLIT_PERCENT)/100 END),A.UNIT_PRICE = (CASE WHEN A.PARQTEITM_LINE_RECORD_ID <> A.QUOTE_REVISION_CONTRACT_ITEM_ID AND ISNULL(A.PARQTEITM_LINE,'''') <> ''''  and ISNULL(A.PARQTEITM_LINE_RECORD_ID,'''') <> '''' THEN NET_PRICE * (100-XY.SPLIT_PERCENT)/100 END) FROM SAQRIT(NOLOCK)A INNER JOIN(SELECT DISTINCT B.SPLIT_PERCENT,B.QUOTE_RECORD_ID,B.QTEREV_RECORD_ID,B.GREENBOOK FROM SAQRIT B(NOLOCK) WHERE B.QUOTE_RECORD_ID = ''"+str(contract_quote_rec_id)+"'' AND B.SERVICE_ID = ''"+str(seid)+"'') AS XY ON A.QUOTE_RECORD_ID = XY.QUOTE_RECORD_ID AND A.QTEREV_RECORD_ID = XY.QTEREV_RECORD_ID AND A.GREENBOOK = XY.GREENBOOK WHERE A.QUOTE_RECORD_ID = ''"+str(contract_quote_rec_id)+"'' AND ISNULL(A.SPLIT,'''')<>''YES'' AND  A.SERVICE_ID IN( ''"+str(seid)+"'' ,''"+str(splitservice_id)+"'')'".format(contract_quote_rec_id =contract_quote_rec_id,seid =seid,splitservice_id = splitservice_id))
	#summary update
	update_service_parent_summary = """UPDATE A  SET A.NET_PRICE = B.NET_PRICE,A.NET_PRICE_INGL_CURR = B.NET_PRICE_INGL_CURR,A.NET_VALUE = B.NET_VALUE,A.NET_VALUE_INGL_CURR = B.NET_VALUE_INGL_CURR,A.UNIT_PRICE = B.UNIT_PRICE,A.UNIT_PRICE_INGL_CURR = B.UNIT_PRICE_INGL_CURR FROM SAQRIS A(NOLOCK) JOIN (SELECT SUM(NET_PRICE) AS NET_PRICE,SUM(NET_PRICE_INGL_CURR) AS NET_PRICE_INGL_CURR,SUM(NET_VALUE) AS NET_VALUE,SUM(NET_VALUE_INGL_CURR) AS NET_VALUE_INGL_CURR,SUM(UNIT_PRICE) AS UNIT_PRICE,SUM(UNIT_PRICE_INGL_CURR) AS UNIT_PRICE_INGL_CURR,QUOTE_RECORD_ID,QTEREV_RECORD_ID,SERVICE_ID from SAQRIT(NOLOCK) WHERE QUOTE_RECORD_ID ='{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_rec_id}'  AND SERVICE_ID = '{seid}' GROUP BY QUOTE_RECORD_ID,QTEREV_RECORD_ID,SERVICE_ID) B ON A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.SERVICE_ID=B.SERVICE_ID AND A.QTEREV_RECORD_ID = B.QTEREV_RECORD_ID """.format(contract_quote_rec_id= contract_quote_rec_id,quote_revision_rec_id = quote_revision_rec_id,seid =seid)
	Sql.RunQuery(update_service_parent_summary)
	update_service_child_summary = """UPDATE A  SET A.NET_PRICE = B.NET_PRICE,A.NET_PRICE_INGL_CURR = B.NET_PRICE_INGL_CURR,A.NET_VALUE = B.NET_VALUE,A.NET_VALUE_INGL_CURR = B.NET_VALUE_INGL_CURR,A.UNIT_PRICE = B.UNIT_PRICE,A.UNIT_PRICE_INGL_CURR = B.UNIT_PRICE_INGL_CURR FROM SAQRIS A(NOLOCK) JOIN (SELECT SUM(NET_PRICE) AS NET_PRICE,SUM(NET_PRICE_INGL_CURR) AS NET_PRICE_INGL_CURR,SUM(NET_VALUE) AS NET_VALUE,SUM(NET_VALUE_INGL_CURR) AS NET_VALUE_INGL_CURR,SUM(UNIT_PRICE) AS UNIT_PRICE,SUM(UNIT_PRICE_INGL_CURR) AS UNIT_PRICE_INGL_CURR,QUOTE_RECORD_ID,QTEREV_RECORD_ID,SERVICE_ID from SAQRIT(NOLOCK) WHERE QUOTE_RECORD_ID ='{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_rec_id}'  AND SERVICE_ID = '{splitservice_id}' GROUP BY QUOTE_RECORD_ID,QTEREV_RECORD_ID,SERVICE_ID) B ON A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.SERVICE_ID=B.SERVICE_ID AND A.QTEREV_RECORD_ID = B.QTEREV_RECORD_ID """.format(contract_quote_rec_id= contract_quote_rec_id,quote_revision_rec_id = quote_revision_rec_id,seid =seid,splitservice_id =splitservice_id)
	Sql.RunQuery(update_service_child_summary)
	saqrioinsert ="""MERGE SAQRIO SRC USING (SELECT A.QUOTE_REVISION_ITEM_OBJECT_RECORD_ID,A.CUSTOMER_TOOL_ID,A.EQUIPMENT_DESCRIPTION,A.EQUIPMENT_ID,A.EQUIPMENT_RECORD_ID,A.GREENBOOK,A.GREENBOOK_RECORD_ID,A.KPU,B.LINE,B.SERVICE_DESCRIPTION,B.SERVICE_ID,B.SERVICE_RECORD_ID,A.QUOTE_ID,A.QTEITM_RECORD_ID,A.QUOTE_RECORD_ID,A.QTEREV_ID,A.QTEREV_RECORD_ID,A.SERIAL_NUMBER,A.TECHNOLOGY,A.TOOL_CONFIGURATION,A.WAFER_SIZE,B.QUOTE_REVISION_CONTRACT_ITEM_ID,B.CPQTABLEENTRYADDEDBY,B.CPQTABLEENTRYDATEADDED,B.CpqTableEntryModifiedBy,B.CpqTableEntryDateModified FROM SAQRIO(NOLOCK) A JOIN SAQRIT (NOLOCK) B ON A.QUOTE_RECORD_ID  = B.QUOTE_RECORD_ID AND A.LINE = B.PARQTEITM_LINE where B.QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND B.QTEREV_RECORD_ID  = '{quote_revision_rec_id}' AND B.SERVICE_ID = '{splitservice_id}')
	TGT ON (SRC.QUOTE_RECORD_ID = TGT.QUOTE_RECORD_ID AND SRC.QTEREV_RECORD_ID = TGT.QTEREV_RECORD_ID AND SRC.SERVICE_ID = '{splitservice_id}')
	WHEN NOT MATCHED BY TARGET
	THEN INSERT(QUOTE_REVISION_ITEM_OBJECT_RECORD_ID,CUSTOMER_TOOL_ID,EQUIPMENT_DESCRIPTION,EQUIPMENT_ID,EQUIPMENT_RECORD_ID,GREENBOOK,GREENBOOK_RECORD_ID,KPU,LINE,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,QUOTE_ID,QTEITM_RECORD_ID,QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,SERIAL_NUMBER,TECHNOLOGY,TOOL_CONFIGURATION,WAFER_SIZE,CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified)
	VALUES (NEWID(),CUSTOMER_TOOL_ID,EQUIPMENT_DESCRIPTION,EQUIPMENT_ID,EQUIPMENT_RECORD_ID,GREENBOOK,GREENBOOK_RECORD_ID,KPU,LINE,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,QUOTE_ID,QUOTE_REVISION_CONTRACT_ITEM_ID,QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,SERIAL_NUMBER,TECHNOLOGY,TOOL_CONFIGURATION,WAFER_SIZE,'{UserName}','{datetimenow}','{UserId}','{datetimenow}');""".format(contract_quote_rec_id=contract_quote_rec_id,quote_revision_rec_id = quote_revision_rec_id,splitservice_id =splitservice_id,UserId=user_id,UserName=user_name,datetimenow=datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"))
	Sql.RunQuery(saqrioinsert)
	annaul_line_insert = ScriptExecutor.ExecuteGlobal("CQINSQTITM",{"ContractQuoteRecordId":contract_quote_rec_id, "ContractQuoteRevisionRecordId":quote_revision_rec_id, "ServiceId":splitservice_id, "ActionType":'INSERT_LINE_ITEMS'})
	#Updating net price for Annualised grid
	update_annual_grid_split_service = """UPDATE SAQICO SET SAQICO.NET_PRICE_INGL_CURR = CAST(CAST(A.NET_PRICE_INGL_CURR AS DECIMAL(13,5))/(SELECT count(*) FROM SAQICO Y(NOLOCK)WHERE Y.QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND Y.QTEREV_RECORD_ID ='{quote_revision_rec_id}' AND SERVICE_ID='{splitservice_id}')AS DECIMAL(13,5)) FROM SAQICO X(NOLOCK) INNER JOIN (SELECT NET_PRICE_INGL_CURR,SERVICE_ID,QUOTE_REVISION_CONTRACT_ITEM_ID FROM SAQRIT (NOLOCK) WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID ='{quote_revision_rec_id}' AND SERVICE_ID='{splitservice_id}' Group By NET_PRICE_INGL_CURR,SERVICE_ID,QUOTE_REVISION_CONTRACT_ITEM_ID )A ON X.QTEITM_RECORD_ID = A.QUOTE_REVISION_CONTRACT_ITEM_ID AND X.SERVICE_ID = A.SERVICE_ID WHERE X.QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND X.QTEREV_RECORD_ID ='{quote_revision_rec_id}' """.format(contract_quote_rec_id= contract_quote_rec_id,quote_revision_rec_id = quote_revision_rec_id,splitservice_id =splitservice_id)
	Sql.RunQuery(update_annual_grid_split_service)
	update_annual_grid_split_service_adjustment ="""Update XY SET XY.NET_PRICE_INGL_CURR = XY.NET_PRICE_INGL_CURR + (SELECT CAST(A.NET_PRICE_INGL_CURR AS DECIMAL(13,5))- CAST(sum(B.NET_PRICE_INGL_CURR)AS DECIMAL(13,5)) from SAQRIT A(NOLOCK) JOIN SAQICO B(NOLOCK) ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID WHERE A.QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND A.QTEREV_RECORD_ID ='{quote_revision_rec_id}' AND A.SERVICE_ID='{splitservice_id}' GROUP BY B.NET_PRICE_INGL_CURR,A.NET_PRICE_INGL_CURR) FROM SAQICO XY(NOLOCK) WHERE XY.QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND XY.QTEREV_RECORD_ID ='{quote_revision_rec_id}'AND XY.SERVICE_ID='{splitservice_id}' AND XY.CpqTableEntryId = (SELECT MAX(Y.CpqTableEntryId) FROM SAQICO Y(NOLOCK) WHERE Y.QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND Y.QTEREV_RECORD_ID ='{quote_revision_rec_id}' AND Y.SERVICE_ID='{splitservice_id}')""".format(contract_quote_rec_id= contract_quote_rec_id,quote_revision_rec_id = quote_revision_rec_id,splitservice_id =splitservice_id)
	Sql.RunQuery(update_annual_grid_split_service_adjustment)
	global_year_1 ="""UPDATE X SET X.YEAR_1_INGL_CURR = CASE A.[YEAR] WHEN 'YEAR 1' THEN CAST(A.NET_PRICE_INGL_CURR AS DECIMAL(13,5)) ELSE NULL END FROM SAQRIT X(NOLOCK) INNER JOIN (SELECT DISTINCT NET_PRICE_INGL_CURR,SERVICE_ID,QTEITM_RECORD_ID,[YEAR] FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID ='{quote_revision_rec_id}' AND SERVICE_ID='{splitservice_id}' AND ISNULL([YEAR],'') = 'YEAR 1' GROUP BY NET_PRICE_INGL_CURR,SERVICE_ID,QUOTE_ITEM_COVERED_OBJECT_RECORD_ID,[YEAR] ,QTEITM_RECORD_ID)A ON X.QUOTE_REVISION_CONTRACT_ITEM_ID = A.QTEITM_RECORD_ID AND X.SERVICE_ID = A.SERVICE_ID""".format(contract_quote_rec_id= contract_quote_rec_id,quote_revision_rec_id = quote_revision_rec_id,splitservice_id =splitservice_id)
	Sql.RunQuery(global_year_1)
	global_year_2 ="""UPDATE X SET X.YEAR_2_INGL_CURR = CASE A.[YEAR] WHEN 'YEAR 2' THEN CAST(A.NET_PRICE_INGL_CURR AS DECIMAL(13,5)) ELSE NULL END FROM SAQRIT X(NOLOCK) INNER JOIN (SELECT DISTINCT NET_PRICE_INGL_CURR,SERVICE_ID,QTEITM_RECORD_ID,[YEAR] FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID ='{quote_revision_rec_id}' AND SERVICE_ID='{splitservice_id}' AND ISNULL([YEAR],'') = 'YEAR 2' GROUP BY NET_PRICE_INGL_CURR,SERVICE_ID,QUOTE_ITEM_COVERED_OBJECT_RECORD_ID,[YEAR] ,QTEITM_RECORD_ID)A ON X.QUOTE_REVISION_CONTRACT_ITEM_ID = A.QTEITM_RECORD_ID AND X.SERVICE_ID = A.SERVICE_ID""".format(contract_quote_rec_id= contract_quote_rec_id,quote_revision_rec_id = quote_revision_rec_id,splitservice_id =splitservice_id)
	Sql.RunQuery(global_year_2)
	global_year_3 ="""UPDATE X SET X.YEAR_3_INGL_CURR = CASE A.[YEAR] WHEN 'YEAR 3' THEN CAST(A.NET_PRICE_INGL_CURR AS DECIMAL(13,5)) ELSE NULL END FROM SAQRIT X(NOLOCK) INNER JOIN (SELECT DISTINCT NET_PRICE_INGL_CURR,SERVICE_ID,QTEITM_RECORD_ID,[YEAR] FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID ='{quote_revision_rec_id}' AND SERVICE_ID='{splitservice_id}' AND ISNULL([YEAR],'') = 'YEAR 3' GROUP BY NET_PRICE_INGL_CURR,SERVICE_ID,QUOTE_ITEM_COVERED_OBJECT_RECORD_ID,[YEAR] ,QTEITM_RECORD_ID)A ON X.QUOTE_REVISION_CONTRACT_ITEM_ID = A.QTEITM_RECORD_ID AND X.SERVICE_ID = A.SERVICE_ID""".format(contract_quote_rec_id= contract_quote_rec_id,quote_revision_rec_id = quote_revision_rec_id,splitservice_id =splitservice_id)
	Sql.RunQuery(global_year_3)
	global_year_4 ="""UPDATE X SET X.YEAR_4_INGL_CURR = CASE A.[YEAR] WHEN 'YEAR 4' THEN CAST(A.NET_PRICE_INGL_CURR AS DECIMAL(13,5)) ELSE NULL END FROM SAQRIT X(NOLOCK) INNER JOIN (SELECT DISTINCT NET_PRICE_INGL_CURR,SERVICE_ID,QTEITM_RECORD_ID,[YEAR] FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID ='{quote_revision_rec_id}' AND SERVICE_ID='{splitservice_id}' AND ISNULL([YEAR],'') = 'YEAR 4' GROUP BY NET_PRICE_INGL_CURR,SERVICE_ID,QUOTE_ITEM_COVERED_OBJECT_RECORD_ID,[YEAR] ,QTEITM_RECORD_ID)A ON X.QUOTE_REVISION_CONTRACT_ITEM_ID = A.QTEITM_RECORD_ID AND X.SERVICE_ID = A.SERVICE_ID""".format(contract_quote_rec_id= contract_quote_rec_id,quote_revision_rec_id = quote_revision_rec_id,splitservice_id =splitservice_id)
	Sql.RunQuery(global_year_4)
	global_year_5 ="""UPDATE X SET X.YEAR_5_INGL_CURR = CASE A.[YEAR] WHEN 'YEAR 5' THEN CAST(A.NET_PRICE_INGL_CURR AS DECIMAL(13,5)) ELSE NULL END FROM SAQRIT X(NOLOCK) INNER JOIN (SELECT DISTINCT NET_PRICE_INGL_CURR,SERVICE_ID,QTEITM_RECORD_ID,[YEAR] FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID ='{quote_revision_rec_id}' AND SERVICE_ID='{splitservice_id}' AND ISNULL([YEAR],'') = 'YEAR 5' GROUP BY NET_PRICE_INGL_CURR,SERVICE_ID,QUOTE_ITEM_COVERED_OBJECT_RECORD_ID,[YEAR] ,QTEITM_RECORD_ID)A ON X.QUOTE_REVISION_CONTRACT_ITEM_ID = A.QTEITM_RECORD_ID AND X.SERVICE_ID = A.SERVICE_ID""".format(contract_quote_rec_id= contract_quote_rec_id,quote_revision_rec_id = quote_revision_rec_id,splitservice_id =splitservice_id)
	Sql.RunQuery(global_year_5)
	document_years="""UPDATE SAQRIT SET 
		SAQRIT.YEAR_1 = CASE WHEN YEAR_1_INGL_CURR IS NULL THEN NULL ELSE
		CAST(CAST(NET_PRICE AS DECIMAL(13,5))/(SELECT count(*) FROM SAQICO Y(NOLOCK)WHERE Y.QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND Y.QTEREV_RECORD_ID ='{quote_revision_rec_id}' AND SERVICE_ID='{splitservice_id}')AS DECIMAL(13,5)) END,
		SAQRIT.YEAR_2 = CASE WHEN YEAR_2_INGL_CURR IS NULL THEN  NULL ELSE 
		CAST(CAST(NET_PRICE AS DECIMAL(13,5))/(SELECT count(*) FROM SAQICO Y(NOLOCK)WHERE Y.QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND Y.QTEREV_RECORD_ID ='{quote_revision_rec_id}' AND SERVICE_ID='{splitservice_id}')AS DECIMAL(13,5)) END,
		SAQRIT.YEAR_3 = CASE WHEN YEAR_3_INGL_CURR IS NULL THEN  NULL ELSE 
		CAST(CAST(NET_PRICE AS DECIMAL(13,5))/(SELECT count(*) FROM SAQICO Y(NOLOCK)WHERE Y.QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND Y.QTEREV_RECORD_ID ='{quote_revision_rec_id}' AND SERVICE_ID='{splitservice_id}')AS DECIMAL(13,5)) END,
		SAQRIT.YEAR_4 = CASE WHEN YEAR_4_INGL_CURR IS NULL THEN  NULL ELSE
		CAST(CAST(NET_PRICE AS DECIMAL(13,5))/(SELECT count(*) FROM SAQICO Y(NOLOCK)WHERE Y.QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND Y.QTEREV_RECORD_ID ='{quote_revision_rec_id}' AND SERVICE_ID='{splitservice_id}')AS DECIMAL(13,5)) END,
		SAQRIT.YEAR_5 = CASE WHEN YEAR_5_INGL_CURR IS NULL THEN  NULL ELSE
		CAST(CAST(NET_PRICE AS DECIMAL(13,5))/(SELECT count(*) FROM SAQICO Y(NOLOCK)WHERE Y.QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND Y.QTEREV_RECORD_ID ='{quote_revision_rec_id}' AND SERVICE_ID='{splitservice_id}')AS DECIMAL(13,5)) END
		FROM SAQRIT X(NOLOCK)
		WHERE X.QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND X.QTEREV_RECORD_ID ='{quote_revision_rec_id}' AND SERVICE_ID ='{splitservice_id}' """.format(contract_quote_rec_id= contract_quote_rec_id,quote_revision_rec_id = quote_revision_rec_id,splitservice_id =splitservice_id)
	Sql.RunQuery(document_years)
	document_years_adjustments ="UPDATE SAQRIT SET YEAR_1 = YEAR_1 + (NET_PRICE - (ISNULL(YEAR_1,0)+ISNULL(YEAR_2,0)+ISNULL(YEAR_3,0)+ISNULL(YEAR_4,0)+ISNULL(YEAR_5,0))) FROM SAQRIT WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID ='{quote_revision_rec_id}' AND SERVICE_ID='{splitservice_id}')""".format(contract_quote_rec_id= contract_quote_rec_id,quote_revision_rec_id = quote_revision_rec_id,splitservice_id =splitservice_id)
	Sql.RunQuery(document_years_adjustments)
	#CQIFWUDQTM = ScriptExecutor.ExecuteGlobal("CQIFWUDQTM",{"QT_REC_ID":get_c4c_quote_id.QUOTE_ID}) 


##To update the SAQTRV table after clicking the split button..
##adding the pricing column  values from SAQRIS table...
Sql.RunQuery("""UPDATE SAQTRV
						SET
						SAQTRV.NET_PRICE_INGL_CURR = IQ.NET_PRICE_INGL_CURR,
						SAQTRV.NET_VALUE_INGL_CURR = IQ.NET_VALUE_INGL_CURR
						FROM SAQTRV (NOLOCK)
						INNER JOIN (SELECT SAQRIS.QUOTE_RECORD_ID, SAQRIS.QTEREV_RECORD_ID,
									SUM(ISNULL(SAQRIS.NET_PRICE, 0)) as NET_PRICE,
									SUM(ISNULL(SAQRIS.NET_PRICE_INGL_CURR, 0)) as NET_PRICE_INGL_CURR,
									SUM(ISNULL(SAQRIS.NET_VALUE, 0)) as NET_VALUE,
									SUM(ISNULL(SAQRIS.NET_VALUE_INGL_CURR, 0)) as NET_VALUE_INGL_CURR
									FROM SAQRIS (NOLOCK) WHERE SAQRIS.QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND SAQRIS.QTEREV_RECORD_ID = '{quote_revision_rec_id}' GROUP BY SAQRIS.QUOTE_RECORD_ID,SAQRIS.QTEREV_RECORD_ID) IQ ON SAQTRV.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND SAQTRV.QUOTE_REVISION_RECORD_ID = IQ.QTEREV_RECORD_ID
						WHERE SAQTRV.QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND SAQTRV.QUOTE_REVISION_RECORD_ID = '{quote_revision_rec_id}' """.format(contract_quote_rec_id = contract_quote_rec_id,quote_revision_rec_id = quote_revision_rec_id) )




splitserviceinsert()









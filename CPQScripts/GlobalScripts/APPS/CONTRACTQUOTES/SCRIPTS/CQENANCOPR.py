# =========================================================================================================================================
#   __script_name : CQENANCOPR.py
#   __script_description : THIS SCRIPT IS USED FOR ANCILLARY PRODUCT OPERATIONS
#   __primary_author__ : 
#   __create_date :8/23/2021
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import System.Net
import re
import time
import datetime
from SYDATABASE import SQL
Sql = SQL()

class AncillaryProductOperation:
	def __init__(self):		
		self.user_id = str(User.Id)
		self.user_name = str(User.UserName)		
		self.datetime_value = datetime.datetime.now()
		self.contract_quote_record_id = str(quote_record_id)
		self.contract_quote_revision_record_id = str(revision_rec_id)
		self.action_type = str(action_type)
		self.service_id = str(service_id)
		self.ancillary_obj = str(ancillary_obj)
		self.where_string = where_string
	
	def _do_opertion(self):
		if self.action_type == "INSERT_SERVICE":
			self._insert_service_offering()
		elif self.action_type == "DELETE_SERVICE":
			self._delete_operation()
	
	def _insert_service_offering(self):
		material_obj = Sql.GetFirst("SELECT MATERIAL_RECORD_ID,SAP_DESCRIPTION FROM MAMTRL WHERE SAP_PART_NUMBER = '{}'".format(self.ancillary_obj))
		if material_obj:
			description = material_obj.SAP_DESCRIPTION
			material_record_id = material_obj.MATERIAL_RECORD_ID
			Sql.RunQuery("""INSERT SAQTSV (QTEREV_RECORD_ID,QTEREV_ID,QUOTE_ID, QUOTE_NAME,UOM_ID,UOM_RECORD_ID, QUOTE_RECORD_ID, SERVICE_DESCRIPTION, SERVICE_ID, PAR_SERVICE_ID,PAR_SERVICE_DESCRIPTION,PAR_SERVICE_RECORD_ID,SERVICE_RECORD_ID, SERVICE_TYPE, CONTRACT_VALID_FROM, CONTRACT_VALID_TO, SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID, QUOTE_SERVICE_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified)
							SELECT A.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED, {UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
							SELECT DISTINCT QTEREV_RECORD_ID, QTEREV_ID,QUOTE_ID, QUOTE_NAME,UOM_ID,UOM_RECORD_ID, QUOTE_RECORD_ID, '{description}' AS SERVICE_DESCRIPTION, '{ancillary_object}' AS SERVICE_ID,SERVICE_ID as PAR_SERVICE_ID,SERVICE_DESCRIPTION AS PAR_SERVICE_DESCRIPTION,QUOTE_SERVICE_RECORD_ID as PAR_SERVICE_RECORD_ID, '{material_record_id}' AS SERVICE_RECORD_ID, '' AS SERVICE_TYPE, CONTRACT_VALID_FROM, CONTRACT_VALID_TO, SALESORG_ID, SALESORG_NAME,SALESORG_RECORD_ID FROM SAQTSV (NOLOCK)
							WHERE SERVICE_ID = '{service_id}' AND QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'
							) A""".format(description=description, service_id = self.service_id, material_record_id = material_record_id,QuoteRecordId = self.contract_quote_record_id, RevisionRecordId = self.contract_quote_revision_record_id ,UserName = self.user_name, UserId = self.user_id, ancillary_object = self.ancillary_obj ))
			
			##calling service insert
			self._insert_service_ent()
			
	def _insert_service_ent(self):
		ent_disp_val = ent_val_code = ''
		get_tooltip = ''
		tbrow = {}
		anc_request_url="https://cpservices-product-configuration.cfapps.us10.hana.ondemand.com/api/v2/configurations?autoCleanup=False"

		anc_fullresponse = ScriptExecutor.ExecuteGlobal("CQENTLNVAL", {'action':'GET_RESPONSE','partnumber':self.ancillary_obj,'request_url':anc_request_url,'request_type':"New"})
		anc_fullresponse=str(anc_fullresponse).replace(": true",": \"true\"").replace(": false",": \"false\"")
		anc_fullresponse= eval(anc_fullresponse)
		##getting configuration_status status
		if anc_fullresponse['complete'] == 'true':
			anc_configuration_status = 'COMPLETE'
		elif anc_fullresponse['complete'] == 'false':
			anc_configuration_status = 'INCOMPLETE'
		else:
			anc_configuration_status = 'ERROR'
		attributesdisallowedlst=[]
		attributeReadonlylst=[]
		attributesallowedlst=[]
		attributedefaultvalue = []
		overallattributeslist =[]
		attributevalues={}
		get_service_details = Sql.GetFirst("SELECT * FROM SAQTSV WHERE {}".format(self.where_string))
		ProductVersionObj=Sql.GetFirst("Select product_id AS PRD_ID from product_versions(nolock) where SAPKBId = '"+str(anc_fullresponse['kbId'])+"' AND SAPKBVersion='"+str(anc_fullresponse['kbKey']['version'])+"'")
		HasDefaultvalue=False
		for rootattribute, rootvalue in anc_fullresponse.items():
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
							
		ProductVersionObj=Sql.GetFirst("Select product_id AS PRD_ID from product_versions(nolock) where SAPKBId = '"+str(anc_fullresponse['kbId'])+"' AND SAPKBVersion='"+str(anc_fullresponse['kbKey']['version'])+"'")
		HasDefaultvalue=False
		if ProductVersionObj:
			insertservice = ""
			for attrs in overallattributeslist:
				if attrs in attributevalues:
					HasDefaultvalue=True					
					STANDARD_ATTRIBUTE_VALUES=Sql.GetFirst("SELECT S.STANDARD_ATTRIBUTE_DISPLAY_VAL,S.STANDARD_ATTRIBUTE_CODE FROM STANDARD_ATTRIBUTE_VALUES (nolock) S INNER JOIN ATTRIBUTE_DEFN (NOLOCK) A ON A.STANDARD_ATTRIBUTE_CODE=S.STANDARD_ATTRIBUTE_CODE WHERE A.SYSTEM_ID = '{}' ".format(attrs))
					ent_disp_val = attributevalues[attrs]
					ent_val_code = attributevalues[attrs]
					#Trace.Write("ent_disp_val----"+str(ent_disp_val))
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
						
						getslaes_value  = Sql.GetFirst("SELECT SALESORG_ID FROM SAQTRV WHERE QUOTE_RECORD_ID = '"+str(self.ContractRecordId)+"'")
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

			
			tbrow["QUOTE_SERVICE_ENTITLEMENT_RECORD_ID"]=str(Guid.NewGuid()).upper()
			tbrow["QUOTE_ID"]=get_service_details.QUOTE_ID
			tbrow["ENTITLEMENT_XML"]=insertservice
			tbrow["QUOTE_NAME"]=get_service_details.QUOTE_NAME
			tbrow["QUOTE_RECORD_ID"]=get_service_details.QUOTE_RECORD_ID
			tbrow["QTESRV_RECORD_ID"]=get_service_details.SERVICE_RECORD_ID
			tbrow["SERVICE_RECORD_ID"]=get_service_details.SERVICE_RECORD_ID
			tbrow["SERVICE_ID"]= self.ancillary_obj
			tbrow["SERVICE_DESCRIPTION"]=get_service_details.SERVICE_DESCRIPTION
			tbrow["CPS_CONFIGURATION_ID"]= anc_fullresponse['id']
			tbrow["SALESORG_RECORD_ID"]=get_service_details.SALESORG_RECORD_ID
			tbrow["SALESORG_ID"]=get_service_details.SALESORG_ID
			tbrow["SALESORG_NAME"]=get_service_details.SALESORG_NAME
			tbrow["CPS_MATCH_ID"] = 1
			tbrow["CPQTABLEENTRYADDEDBY"] = self.user_id
			tbrow["CPQTABLEENTRYDATEADDED"] = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p")
			tbrow["QTEREV_RECORD_ID"] = get_service_details.QTEREV_ID
			tbrow["QTEREV_ID"] = self.contract_quote_revision_record_id
			tbrow["CONFIGURATION_STATUS"] = anc_configuration_status
			columns = ', '.join("" + str(x) + "" for x in tbrow.keys())
			values = ', '.join("'" + str(x) + "'" for x in tbrow.values())
			insert_qtqtse_query = "INSERT INTO SAQTSE ( %s ) VALUES ( %s );" % (columns, values)
			Sql.RunQuery(insert_qtqtse_query)
					




	def _delete_operation(self):
		delete_obj_list = ["SAQTSV","SAQTSE"]
		if self.action_type == "DELETE_EQUIPMENT":
			delete_obj_list = delete_obj_list.extend(["SAQSCO","SAQSFE","SAQSGE","SAQSCE","SAQSAE"])
		for obj in delete_obj_list:
			Sql.RunQuery("DELETE FROM {} WHERE {}".format(obj,self.where_string))
	def _entitlement_rolldown(self):
		pass
	def _equipment_insert(self):
		pass

ancillary_obj = Param.ancillary_obj
action_type = Param.ActionType
quote_record_id = Param.quote_record_id
revision_rec_id = Param.revision_rec_id
service_id  = Param.service_id
where_string = Param.where_string

auto_ancillary_obj = AncillaryProductOperation()
auto_ancillary_obj._do_opertion()
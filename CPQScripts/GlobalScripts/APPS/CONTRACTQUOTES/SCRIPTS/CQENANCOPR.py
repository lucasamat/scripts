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
import sys
from SYDATABASE import SQL
Sql = SQL()

class AncillaryProductOperation:
	def __init__(self):		
		self.fab = ""
		self.greenbook = ""
		self.equipment_id = ""
		self.assembly = ""
		self.user_id = str(User.Id)
		self.user_name = str(User.UserName)		
		self.datetime_value = datetime.datetime.now()
		self.contract_quote_record_id = str(quote_record_id)
		self.contract_quote_revision_record_id = str(revision_rec_id)
		self.action_type = str(action_type)
		self.service_id = str(service_id)
		self.ancillary_obj = str(ancillary_obj)
		self.where_string = where_string
		self.tablename = tablename
		if self.tablename in ("SAQSFE","SAQSGE","SAQSCE","SAQSAE"):
			pattern = re.compile(r''+str('FABLOCATION_ID')+'\s*\=\s*\'([^>]*?)\'')
			self.fab = re.search(pattern, self.where_string).group(1)
		if self.tablename in ("SAQSGE","SAQSCE","SAQSAE"):
			pattern = re.compile(r''+str('GREENBOOK')+'\s*\=\s*\'([^>]*?)\'')
			self.greenbook = re.search(pattern, self.where_string).group(1)
		if self.tablename in ("SAQSCE","SAQSAE"):
			pattern = re.compile(r''+str('EQUIPMENT_ID')+'\s*\=\s*\'([^>]*?)\'')
			self.equipment_id = re.search(pattern, self.where_string).group(1)
		if self.tablename in ("SAQSAE"):
			pattern = re.compile(r''+str('ASSEMBLY_ID')+'\s*\=\s*\'([^>]*?)\'')
			self.assembly = re.search(pattern, self.where_string).group(1)

	
	def _do_opertion(self):
		if self.action_type == "INSERT_SERVICE":
			self._insert_service_offering()
		elif self.action_type == "DELETE_SERVICE":
			self._delete_operation()
		elif  self.action_type == "INSERT_ENT_EQUIPMENT":
			self._entitlement_rolldown()
		elif self.action_type == "DELETE_ENT_EQUIPMENT":
			self._delete_operation()
	
	def _insert_service_offering(self):
		material_obj = Sql.GetFirst("SELECT MATERIAL_RECORD_ID,SAP_DESCRIPTION,MATERIALCONFIG_TYPE FROM MAMTRL WHERE SAP_PART_NUMBER = '{}'".format(self.ancillary_obj))
		if material_obj:
			description = material_obj.SAP_DESCRIPTION
			material_record_id = material_obj.MATERIAL_RECORD_ID
			Sql.RunQuery("""INSERT SAQTSV (QTEREV_RECORD_ID,QTEREV_ID,QUOTE_ID, QUOTE_NAME,UOM_ID,UOM_RECORD_ID, QUOTE_RECORD_ID, SERVICE_DESCRIPTION, SERVICE_ID, PAR_SERVICE_ID,PAR_SERVICE_DESCRIPTION,PAR_SERVICE_RECORD_ID,SERVICE_RECORD_ID, SERVICE_TYPE, CONTRACT_VALID_FROM, CONTRACT_VALID_TO, SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID, QUOTE_SERVICE_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified)
							SELECT A.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED, {UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
							SELECT DISTINCT QTEREV_RECORD_ID, QTEREV_ID,QUOTE_ID, QUOTE_NAME,UOM_ID,UOM_RECORD_ID, QUOTE_RECORD_ID, '{description}' AS SERVICE_DESCRIPTION, '{ancillary_object}' AS SERVICE_ID,SERVICE_ID as PAR_SERVICE_ID,SERVICE_DESCRIPTION AS PAR_SERVICE_DESCRIPTION,QUOTE_SERVICE_RECORD_ID as PAR_SERVICE_RECORD_ID, '{material_record_id}' AS SERVICE_RECORD_ID, '' AS SERVICE_TYPE, CONTRACT_VALID_FROM, CONTRACT_VALID_TO, SALESORG_ID, SALESORG_NAME,SALESORG_RECORD_ID FROM SAQTSV (NOLOCK)
							WHERE SERVICE_ID = '{service_id}' AND QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'
							) A""".format(description=description, service_id = self.service_id, material_record_id = material_record_id,QuoteRecordId = self.contract_quote_record_id, RevisionRecordId = self.contract_quote_revision_record_id ,UserName = self.user_name, UserId = self.user_id, ancillary_object = self.ancillary_obj ))
			
			##calling fn for service insert MATERIALCONFIG_TYPE
			if material_obj.MATERIALCONFIG_TYPE != "SIMPLE MATERIAL":
				self._insert_service_ent()

			##calling fn for equipment insert
			#self._equipment_insert()


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
		get_service_details = Sql.GetFirst("SELECT * FROM SAQTSV WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID ='{}' AND PAR_SERVICE_ID = '{}'".format(self.contract_quote_record_id, self.contract_quote_revision_record_id ,self.ancillary_obj, self.service_id))
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
						
						getslaes_value  = Sql.GetFirst("SELECT SALESORG_ID FROM SAQTRV WHERE QUOTE_RECORD_ID = '"+str(self.contract_quote_record_id)+"'")
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
			tbrow["PAR_SERVICE_ID"] = get_service_details.PAR_SERVICE_ID
			tbrow["PAR_SERVICE_RECORD_ID"] = get_service_details.PAR_SERVICE_RECORD_ID
			tbrow["PAR_SERVICE_DESCRIPTION"] = get_service_details.PAR_SERVICE_DESCRIPTION
			columns = ', '.join("" + str(x) + "" for x in tbrow.keys())
			values = ', '.join("'" + str(x) + "'" for x in tbrow.values())
			insert_qtqtse_query = "INSERT INTO SAQTSE ( %s ) VALUES ( %s );" % (columns, values)
			Sql.RunQuery(insert_qtqtse_query)
					
	def _insert_fab(self):
		get_service_details = Sql.GetFirst("SELECT * FROM SAQTSV WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID ='{}' AND PAR_SERVICE_ID = '{}'".format(self.contract_quote_record_id, self.contract_quote_revision_record_id ,self.ancillary_obj, self.service_id))
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
					QTEREV_ID,
					QTEREV_RECORD_ID,
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
					CONTRACT_VALID_FROM,
					CONTRACT_VALID_TO,
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
					FABLOCATION_ID,
					FABLOCATION_NAME,
					FABLOCATION_RECORD_ID,
					'{serviceid}',
					'{service_type}',
					'{desc}',
					'{rec}',
					STATUS,
					QUOTE_ID,
					QUOTE_NAME,
					QUOTE_RECORD_ID,
					QTEREV_ID,
					QTEREV_RECORD_ID,
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
					CONTRACT_VALID_FROM,
					CONTRACT_VALID_TO,
					SERVICE_DESCRIPTION,
					SERVICE_ID,
					SERVICE_RECORD_ID
					FROM SAQSFB (NOLOCK)
					
					WHERE QUOTE_RECORD_ID = '{QuoteRecordId}'  AND QTEREV_RECORD_ID = '{RevisionRecordId}'  AND SERVICE_ID ='{par_service_id}' {addtional_where} AND SAQSFB.FABLOCATION_ID not in (SELECT FABLOCATION_ID FROM SAQSFB (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}'  AND QTEREV_RECORD_ID = '{RevisionRecordId}'  AND PAR_SERVICE_ID ='{par_service_id}' AND SERVICE_ID ='{serviceid}')
					) FB""".format(
									par_service_id = self.service_id,
									QuoteRecordId=self.contract_quote_record_id,
									RevisionRecordId=self.contract_quote_revision_record_id,
									UserId=self.user_id,
									UserName=self.user_name,
									serviceid = self.ancillary_obj ,
									desc = get_service_details.SERVICE_DESCRIPTION,
									rec = get_service_details.SERVICE_RECORD_ID,
									addtional_where = " AND FABLOCATION_ID = '{}'".format(self.fab) if self.fab else ""
								)
				)
				
		
	def _insert_grn(self):
		addtional_where = ""
		get_service_details = Sql.GetFirst("SELECT * FROM SAQTSV WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID ='{}' AND PAR_SERVICE_ID = '{}'".format(self.contract_quote_record_id, self.contract_quote_revision_record_id ,self.ancillary_obj, self.service_id))
		if self.fab:
			addtional_where = " AND FABLOCATION_ID = '{}' ".format(self.fab)
		if self.greenbook:
			addtional_where += " AND GREENBOOK = '{}'".format(self.greenbook)
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
						QTEREV_ID,
						QTEREV_RECORD_ID,
						SALESORG_ID,
						SALESORG_NAME,
						SALESORG_RECORD_ID,
						SERVICE_DESCRIPTION,
						SERVICE_ID,
						SERVICE_RECORD_ID,
						EQUIPMENT_QUANTITY,
						FABLOCATION_NAME,
						FABLOCATION_RECORD_ID,
						CONTRACT_VALID_FROM,
						CONTRACT_VALID_TO,
						PAR_SERVICE_DESCRIPTION,
						PAR_SERVICE_ID,
						PAR_SERVICE_RECORD_ID,
						CPQTABLEENTRYADDEDBY,
						CPQTABLEENTRYDATEADDED,
						CpqTableEntryModifiedBy,
						CpqTableEntryDateModified
						) SELECT CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_GREENBOOK_RECORD_ID,A.* from (SELECT DISTINCT
							FABLOCATION_ID,
							GREENBOOK,
							GREENBOOK_RECORD_ID,
							QUOTE_ID,
							QUOTE_NAME,
							QUOTE_RECORD_ID,
							QTEREV_ID,
							QTEREV_RECORD_ID,
							SALESORG_ID,
							SALESORG_NAME,
							SALESORG_RECORD_ID,
							'{desc}',
							'{serviceid}',
							'{rec}',
							EQUIPMENT_QUANTITY,								
							FABLOCATION_NAME,
							FABLOCATION_RECORD_ID,
							CONTRACT_VALID_FROM,
							CONTRACT_VALID_TO,
							SERVICE_DESCRIPTION,
							SERVICE_ID,
							SERVICE_RECORD_ID,
							'{UserName}' AS CPQTABLEENTRYADDEDBY,
							GETDATE() as CPQTABLEENTRYDATEADDED,
							{UserId} as CpqTableEntryModifiedBy,
							GETDATE() as CpqTableEntryDateModified
							FROM SAQSGB (NOLOCK) 
							 
							WHERE QUOTE_RECORD_ID = '{QuoteRecordId}'  AND QTEREV_RECORD_ID = '{RevisionRecordId}'  AND SERVICE_ID ='{par_service_id}' {addtional_where} AND GREENBOOK NOT IN (SELECT M.GREENBOOK FROM SAQSGB M (NOLOCK) WHERE M.QUOTE_RECORD_ID = '{QuoteRecordId}' AND M.QTEREV_RECORD_ID = '{RevisionRecordId}' AND PAR_SERVICE_ID ='{par_service_id}' AND SERVICE_ID ='{serviceid}' )               
					
					
					""".format(
							par_service_id = self.service_id,
							QuoteRecordId=self.contract_quote_record_id,
							RevisionRecordId=self.contract_quote_revision_record_id,
							UserId=self.user_id,
							UserName=self.user_name,
							serviceid = self.ancillary_obj ,
							desc = get_service_details.SERVICE_DESCRIPTION,
							rec = get_service_details.SERVICE_RECORD_ID,
							addtional_where = addtional_where 
						)
			)
		
	
	def _insert_assembly(self):
		addtional_where = ""
		get_service_details = Sql.GetFirst("SELECT * FROM SAQTSV WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID ='{}' AND PAR_SERVICE_ID = '{}'".format(self.contract_quote_record_id, self.contract_quote_revision_record_id ,self.ancillary_obj, self.service_id))
		if self.fab:
			addtional_where = " AND FABLOCATION_ID = '{}' ".format(self.fab)
		if self.greenbook:
			addtional_where += " AND GREENBOOK = '{}'".format(self.greenbook)
		if self.equipment_id:
			addtional_where += " AND EQUIPMENT_ID = '{}'".format(self.equipment_id)
		if self.assembly:
			addtional_where += " AND ASSEMBLY_ID = '{}'".format(self.assembly)
		Sql.RunQuery(
			"""
				INSERT (
					QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID,
					CPQTABLEENTRYADDEDBY,
					CPQTABLEENTRYDATEADDED,
					CpqTableEntryModifiedBy,
					CpqTableEntryDateModified,
					ASSEMBLY_ID,
					ASSEMBLY_DESCRIPTION,
					ASSEMBLY_RECORD_ID,
					EQUIPMENT_ID,
					EQUIPMENT_DESCRIPTION,
					EQUIPMENT_RECORD_ID,
					SERIAL_NUMBER,
					GOT_CODE,
					EQUIPMENTCATEGORY_ID,
					EQUIPMENTCATEGORY_DESCRIPTION,
					EQUIPMENTCATEGORY_RECORD_ID,
					ASSEMBLY_STATUS,
					WARRANTY_START_DATE,
					WARRANTY_END_DATE,
					EQUIPMENTTYPE_ID,
					EQUIPMENTTYPE_DESCRIPTION,
					EQUIPMENTTYPE_RECORD_ID,
					QUOTE_ID,
					QUOTE_NAME,
					QUOTE_RECORD_ID,
					QTEREV_ID,
					QTEREV_RECORD_ID,
					SERVICE_ID,
					SERVICE_DESCRIPTION,
					SERVICE_RECORD_ID,
					FABLOCATION_ID,
					FABLOCATION_RECORD_ID,
					FABLOCATION_NAME,
					SALESORG_ID,
					SALESORG_NAME,
					SALESORG_RECORD_ID,
					MNT_PLANT_ID,
					MNT_PLANT_RECORD_ID,
					GREENBOOK,
					GREENBOOK_RECORD_ID,
					PAR_SERVICE_DESCRIPTION,
					PAR_SERVICE_ID,
					PAR_SERVICE_RECORD_ID,
					INCLUDED
					) SELECT
					CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID,
					'{UserName}' AS CPQTABLEENTRYADDEDBY,
					GETDATE() as CPQTABLEENTRYDATEADDED,
					{UserId} as CpqTableEntryModifiedBy,
					GETDATE() as CpqTableEntryDateModified,
					ASSEMBLY_ID,
					ASSEMBLY_DESCRIPTION,
					ASSEMBLY_RECORD_ID,
					EQUIPMENT_ID,
					EQUIPMENT_DESCRIPTION,
					EQUIPMENT_RECORD_ID,
					SERIAL_NUMBER,
					GOT_CODE,
					EQUIPMENTCATEGORY_ID,
					EQUIPMENTCATEGORY_DESCRIPTION,
					EQUIPMENTCATEGORY_RECORD_ID,
					ASSEMBLY_STATUS,
					WARRANTY_START_DATE,
					WARRANTY_END_DATE,
					EQUIPMENTTYPE_ID,
					EQUIPMENTTYPE_DESCRIPTION,
					EQUIPMENTTYPE_RECORD_ID,
					QUOTE_ID,
					QUOTE_NAME,
					QUOTE_RECORD_ID,
					QTEREV_ID,
					QTEREV_RECORD_ID,
					'{serviceid}',
					'{desc}',
					'{rec}',
					FABLOCATION_ID,
					FABLOCATION_RECORD_ID,
					FABLOCATION_NAME,
					SALESORG_ID,
					SALESORG_NAME,
					SALESORG_RECORD_ID,
					MNT_PLANT_ID,
					MNT_PLANT_RECORD_ID,
					GREENBOOK,
					GREENBOOK_RECORD_ID,
					SERVICE_DESCRIPTION,
					SERVICE_ID,
					SERVICE_RECORD_ID,
					INCLUDED 
					FROM SAQSCA (NOLOCK)
					WHERE QUOTE_RECORD_ID = '{QuoteRecordId}'  AND QTEREV_RECORD_ID = '{RevisionRecordId}'  AND SERVICE_ID ='{par_service_id}' {addtional_where}  AND ASSEMBLY_ID NOT IN (SELECT ASSEMBLY_ID FROM SAQSCA WHERE QUOTE_RECORD_ID = '{QuoteRecordId}'  AND QTEREV_RECORD_ID = '{RevisionRecordId}'  AND PAR_SERVICE_ID ='{par_service_id}' AND SERVICE_ID ='{serviceid}' )
				""".format(
						par_service_id = self.service_id,
						serviceid = self.ancillary_obj ,
						QuoteRecordId = self.contract_quote_record_id,
						RevisionRecordId = self.contract_quote_revision_record_id,
						desc = get_service_details.SERVICE_DESCRIPTION,
						rec = get_service_details.SERVICE_RECORD_ID,
						UserName = self.user_name,
						UserId = self.user_id,
						where= self.where_string,
						addtional_where = addtional_where 
			)
		) 
		


	def _equipment_insert(self):
		addtional_where = ""
		get_service_details = Sql.GetFirst("SELECT * FROM SAQTSV WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID ='{}' AND PAR_SERVICE_ID = '{}'".format(self.contract_quote_record_id, self.contract_quote_revision_record_id ,self.ancillary_obj, self.service_id))
		if self.fab:
			addtional_where = " AND FABLOCATION_ID = '{}' ".format(self.fab)
		if self.greenbook:
			addtional_where += " AND GREENBOOK = '{}'".format(self.greenbook)
		if self.equipment_id:
			addtional_where += " AND EQUIPMENT_ID = '{}'".format(self.equipment_id)
		Sql.RunQuery(
				"""
				INSERT SAQSCO (
					QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,
					EQUIPMENT_ID,
					EQUIPMENT_RECORD_ID,
					EQUIPMENT_DESCRIPTION,                            
					FABLOCATION_ID,
					FABLOCATION_NAME,
					FABLOCATION_RECORD_ID,
					WAFER_SIZE,
					SALESORG_ID,
					SALESORG_NAME,
					SALESORG_RECORD_ID,
					SERIAL_NO,
					QUOTE_RECORD_ID,
					QUOTE_ID,
					QUOTE_NAME,
					RELOCATION_EQUIPMENT_TYPE,
					SERVICE_ID,
					SERVICE_TYPE,
					SERVICE_DESCRIPTION,
					SERVICE_RECORD_ID,
					EQUIPMENT_STATUS,
					EQUIPMENTCATEGORY_ID,
					EQUIPMENTCATEGORY_DESCRIPTION,
					EQUIPMENTCATEGORY_RECORD_ID,
					PLATFORM,
					GREENBOOK,
					GREENBOOK_RECORD_ID,
					MNT_PLANT_RECORD_ID,
					MNT_PLANT_NAME,
					MNT_PLANT_ID,
					WARRANTY_START_DATE,
					WARRANTY_END_DATE,
					CUSTOMER_TOOL_ID,
					PAR_SERVICE_DESCRIPTION,
					PAR_SERVICE_ID,
					PAR_SERVICE_RECORD_ID,
					TECHNOLOGY,
					CPQTABLEENTRYADDEDBY,
					CPQTABLEENTRYDATEADDED,
					CpqTableEntryModifiedBy,
					CpqTableEntryDateModified,
					QTEREV_RECORD_ID,
					KPU,
					QTEREV_ID
											
					) SELECT
						CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,
						EQUIPMENT_ID,
						EQUIPMENT_RECORD_ID,
						EQUIPMENT_DESCRIPTION,                                
						FABLOCATION_ID,
						FABLOCATION_NAME,
						FABLOCATION_RECORD_ID,
						WAFER_SIZE,
						SALESORG_ID,
						SALESORG_NAME,
						SALESORG_RECORD_ID,
						SERIAL_NO,
						QUOTE_RECORD_ID,
						QUOTE_ID,
						QUOTE_NAME,
						RELOCATION_EQUIPMENT_TYPE,
						'{serviceid}',
						'{service_type}',
						'{desc}',
						'{rec}',
						EQUIPMENT_STATUS,
						EQUIPMENTCATEGORY_ID,
						EQUIPMENTCATEGORY_DESCRIPTION,
						EQUIPMENTCATEGORY_RECORD_ID,
						PLATFORM,
						GREENBOOK,
						GREENBOOK_RECORD_ID,
						MNT_PLANT_RECORD_ID,
						MNT_PLANT_NAME,
						MNT_PLANT_ID,
						WARRANTY_START_DATE,
						WARRANTY_END_DATE,
						CUSTOMER_TOOL_ID,
						SERVICE_DESCRIPTION,
						SERVICE_ID,
						SERVICE_RECORD_ID,
						TECHNOLOGY,
						'{UserName}',
						GETDATE(),
						{UserId},
						GETDATE(),
						QTEREV_RECORD_ID,
						KPU,
						QTEREV_ID
						FROM SAQSCO (NOLOCK)
						WHERE QUOTE_RECORD_ID = '{QuoteRecordId}'  AND QTEREV_RECORD_ID = '{RevisionRecordId}'  AND SERVICE_ID ='{par_service_id}' {addtional_where} AND SAQSCO.EQUIPMENT_ID not in (SELECT EQUIPMENT_ID FROM SAQSCO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}'  AND QTEREV_RECORD_ID = '{RevisionRecordId}'  AND PAR_SERVICE_ID ='{par_service_id}' AND SERVICE_ID ='{serviceid}')
												
					""".format(
						par_service_id = self.service_id,
						serviceid = self.ancillary_obj ,
						service_type ="Add-On Products",
						QuoteRecordId = self.contract_quote_record_id,
						RevisionRecordId = self.contract_quote_revision_record_id,
						desc = get_service_details.SERVICE_DESCRIPTION,
						rec = get_service_details.SERVICE_RECORD_ID,
						UserName = self.user_name,
						UserId = self.user_id,
						where= self.where_string,
						addtional_where = addtional_where 
					)
					)
	
	
	def _entitlement_rolldown(self):
		try:
			ancillary_where = re.sub("SERVICE_ID","PAR_SERVICE_ID",self.where_string)
			ancillary_where += " AND SERVICE_ID = '{}'".format(self.ancillary_obj)
			
			get_ancillaryservice = Sql.GetFirst("select * from SAQTSE WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID ='{}' AND PAR_SERVICE_ID = '{}'".format(self.contract_quote_record_id, self.contract_quote_revision_record_id ,self.ancillary_obj, self.service_id))
			if get_ancillaryservice :
				 
				get_ancillary_fab = Sql.GetFirst("select count(CpqTableEntryId) as cnt from SAQSFE WHERE {}".format(ancillary_where))
				if get_ancillary_fab:
					if get_ancillary_fab.cnt == 0:
						
						SAQSFE_ancillary_query="""
							INSERT SAQSFE (ENTITLEMENT_XML,QUOTE_ID,QUOTE_NAME,QUOTE_RECORD_ID,QTEREV_RECORD_ID,QTEREV_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,	
							CPS_CONFIGURATION_ID, CPS_MATCH_ID,QTESRVENT_RECORD_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,QTESRVFBL_RECORD_ID,CONFIGURATION_STATUS,PAR_SERVICE_ID,PAR_SERVICE_RECORD_ID,PAR_SERVICE_DESCRIPTION,QUOTE_SERVICE_FAB_LOC_ENT_RECORD_ID, CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED)
							SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_FAB_LOC_ENT_RECORD_ID, {UserId} as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM (
							SELECT 
								DISTINCT	
								SAQTSE.ENTITLEMENT_XML,SAQTSE.QUOTE_ID,SAQTSE.QUOTE_NAME,SAQTSE.QUOTE_RECORD_ID,SAQTSE.QTEREV_RECORD_ID,SAQTSE.QTEREV_ID,SAQTSE.SERVICE_DESCRIPTION,SAQTSE.SERVICE_ID,SAQTSE.SERVICE_RECORD_ID,SAQTSE.SALESORG_ID,SAQTSE.SALESORG_NAME,SAQTSE.SALESORG_RECORD_ID,SAQTSE.CPS_CONFIGURATION_ID, SAQTSE.CPS_MATCH_ID,SAQTSE.QUOTE_SERVICE_ENTITLEMENT_RECORD_ID as QTESRVENT_RECORD_ID,SAQSFB.FABLOCATION_ID, SAQSFB.FABLOCATION_NAME, SAQSFB.FABLOCATION_RECORD_ID, SAQSFB.QUOTE_SERVICE_FAB_LOCATION_RECORD_ID as QTESRVFBL_RECORD_ID,SAQTSE.CONFIGURATION_STATUS,SAQTSE.PAR_SERVICE_ID,SAQTSE.PAR_SERVICE_RECORD_ID,SAQTSE.PAR_SERVICE_DESCRIPTION
							FROM
							SAQTSE (NOLOCK)
							JOIN SAQSFB ON SAQSFB.SERVICE_ID = '{par_service_id}' AND SAQSFB.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID AND SAQSFB.QTEREV_RECORD_ID = SAQTSE.QTEREV_RECORD_ID
							WHERE SAQTSE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQTSE.QTEREV_RECORD_ID = '{revision_rec_id}' AND SAQTSE.SERVICE_ID = '{ServiceId}') IQ""".format(UserId=self.user_id, QuoteRecordId=self.contract_quote_record_id, ServiceId=self.ancillary_obj, revision_rec_id = self.contract_quote_revision_record_id, par_service_id = self.service_id)
						Log.Info('SAQSFE_ancillary_query--148----ROLL DOWN----'+str(SAQSFE_ancillary_query))
						Sql.RunQuery(SAQSFE_ancillary_query)
						
				
				get_ancillary_grn = Sql.GetFirst("select count(CpqTableEntryId) as cnt from SAQSGE WHERE {}".format(ancillary_where))
				if get_ancillary_grn:
					if get_ancillary_grn.cnt == 0: 
						qtqtse_query_anc="""
							INSERT SAQSGE (KB_VERSION,QUOTE_ID,QUOTE_NAME,QUOTE_RECORD_ID,QTEREV_RECORD_ID,QTEREV_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,	
							CPS_CONFIGURATION_ID, CPS_MATCH_ID,GREENBOOK,GREENBOOK_RECORD_ID,QTESRVENT_RECORD_ID,QTSFBLENT_RECORD_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,ENTITLEMENT_XML,CONFIGURATION_STATUS,PAR_SERVICE_ID,PAR_SERVICE_RECORD_ID,PAR_SERVICE_DESCRIPTION, QUOTE_SERVICE_GREENBOOK_ENTITLEMENT_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED )
							SELECT OQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_GREENBOOK_ENTITLEMENT_RECORD_ID, {UserId} as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM (SELECT IQ.*,M.ENTITLEMENT_XML,M.CONFIGURATION_STATUS,M.PAR_SERVICE_ID,M.PAR_SERVICE_RECORD_ID,M.PAR_SERVICE_DESCRIPTION FROM(
							SELECT 
								DISTINCT	
								SAQTSE.KB_VERSION,SAQTSE.QUOTE_ID,SAQTSE.QUOTE_NAME,SAQTSE.QUOTE_RECORD_ID,SAQTSE.QTEREV_RECORD_ID,SAQTSE.QTEREV_ID,SAQTSE.SERVICE_DESCRIPTION,SAQTSE.SERVICE_ID,SAQTSE.SERVICE_RECORD_ID,SAQTSE.SALESORG_ID,SAQTSE.SALESORG_NAME,SAQTSE.SALESORG_RECORD_ID,SAQTSE.CPS_CONFIGURATION_ID, SAQTSE.CPS_MATCH_ID,SAQSCO.GREENBOOK,SAQSCO.GREENBOOK_RECORD_ID,SAQTSE.QUOTE_SERVICE_ENTITLEMENT_RECORD_ID as QTESRVENT_RECORD_ID,SAQSFE.QUOTE_SERVICE_FAB_LOC_ENT_RECORD_ID as QTSFBLENT_RECORD_ID,SAQSFE.FABLOCATION_ID,SAQSFE.FABLOCATION_NAME,SAQSFE.FABLOCATION_RECORD_ID
							FROM
							SAQTSE (NOLOCK)
							JOIN SAQSCO  (NOLOCK) ON SAQSCO.SERVICE_ID = '{par_service_id}' AND SAQSCO.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID  AND SAQSCO.QTEREV_RECORD_ID = SAQTSE.QTEREV_RECORD_ID JOIN SAQSFE ON SAQSFE.SERVICE_RECORD_ID = SAQTSE.SERVICE_RECORD_ID AND SAQSFE.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID AND SAQSFE.QTEREV_RECORD_ID = SAQTSE.QTEREV_RECORD_ID 
							WHERE SAQTSE.QUOTE_RECORD_ID = '{QuoteRecordId}'  AND SAQTSE.QTEREV_RECORD_ID = '{revision_rec_id}' AND SAQTSE.PAR_SERVICE_ID = '{par_service_id}') IQ JOIN SAQSFE (NOLOCK) M ON IQ.QTSFBLENT_RECORD_ID = QUOTE_SERVICE_FAB_LOC_ENT_RECORD_ID )OQ""".format(UserId=self.user_id, QuoteRecordId=self.contract_quote_record_id, revision_rec_id = self.contract_quote_revision_record_id,par_service_id = self.service_id)
						Log.Info("qtqtse_query_anc---163------"+str(qtqtse_query_anc))
						Sql.RunQuery(qtqtse_query_anc)
				
				get_ancillary_equp = Sql.GetFirst("select count(CpqTableEntryId) as cnt from SAQSCE WHERE {}".format(ancillary_where))
				if get_ancillary_equp:
					if get_ancillary_equp.cnt == 0: 
						qtqsce_anc_query="""
							INSERT SAQSCE
							(KB_VERSION,ENTITLEMENT_XML,CONFIGURATION_STATUS,PAR_SERVICE_ID,PAR_SERVICE_RECORD_ID,PAR_SERVICE_DESCRIPTION,EQUIPMENT_ID,EQUIPMENT_RECORD_ID,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_RECORD_ID,QTEREV_ID,QTESRVCOB_RECORD_ID,QTESRVENT_RECORD_ID,SERIAL_NO,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,CPS_CONFIGURATION_ID,CPS_MATCH_ID,GREENBOOK,GREENBOOK_RECORD_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,QUOTE_SERVICE_COVERED_OBJ_ENTITLEMENTS_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED) 
							SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_COVERED_OBJ_ENTITLEMENTS_RECORD_ID, {UserId} as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM (
							SELECT 
							SAQTSE.KB_VERSION,SAQTSE.ENTITLEMENT_XML,SAQTSE.CONFIGURATION_STATUS,SAQTSE.PAR_SERVICE_ID,SAQTSE.PAR_SERVICE_RECORD_ID,SAQTSE.PAR_SERVICE_DESCRIPTION,SAQSCO.EQUIPMENT_ID,SAQSCO.EQUIPMENT_RECORD_ID,SAQTSE.QUOTE_ID,SAQTSE.QUOTE_RECORD_ID,SAQTSE.QTEREV_RECORD_ID,SAQTSE.QTEREV_ID,SAQSCO.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID as QTESRVCOB_RECORD_ID,SAQTSE.QUOTE_SERVICE_ENTITLEMENT_RECORD_ID as QTESRVENT_RECORD_ID,SAQSCO.SERIAL_NO,SAQTSE.SERVICE_DESCRIPTION,SAQTSE.SERVICE_ID,SAQTSE.SERVICE_RECORD_ID,SAQTSE.CPS_CONFIGURATION_ID,SAQTSE.CPS_MATCH_ID,SAQSCO.GREENBOOK,SAQSCO.GREENBOOK_RECORD_ID,SAQSCO.FABLOCATION_ID,SAQSCO.FABLOCATION_NAME,SAQSCO.FABLOCATION_RECORD_ID,SAQTSE.SALESORG_ID,SAQTSE.SALESORG_NAME,SAQTSE.SALESORG_RECORD_ID
							FROM	
							SAQTSE (NOLOCK)
							JOIN SAQSCO (NOLOCK) ON SAQSCO.SERVICE_ID = '{par_service_id}' AND SAQSCO.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID  AND SAQSCO.QTEREV_RECORD_ID = SAQTSE.QTEREV_RECORD_ID 
							WHERE SAQTSE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQTSE.QTEREV_RECORD_ID = '{revision_rec_id}' AND SAQTSE.SERVICE_ID = '{ServiceId}' AND SAQSCO.EQUIPMENT_ID not in (SELECT EQUIPMENT_ID FROM SAQSCE (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}'   AND QTEREV_RECORD_ID = '{revision_rec_id}' AND SERVICE_ID = '{ServiceId}')) IQ""".format(UserId=self.user_id, QuoteRecordId=self.contract_quote_record_id, ServiceId=self.ancillary_obj, revision_rec_id = self.contract_quote_revision_record_id,par_service_id = self.service_id)
						Log.Info('@qtqsce_anc_query-renewal----179=---Qt_rec_id--'+str(qtqsce_anc_query))
						Sql.RunQuery(qtqsce_anc_query)
				
			

				# Duplicate records removed from assembly level entitlement in offering - Start
				Sql.RunQuery("""DELETE FROM SAQSAE WHERE {}""".format(ancillary_where))
				# Duplicate records removed from assembly level entitlement in offering - End
				SAQSAE_ent_anc_renewal = """INSERT SAQSAE (KB_VERSION,EQUIPMENT_ID,EQUIPMENT_RECORD_ID,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_RECORD_ID,QTEREV_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,CPS_CONFIGURATION_ID,CPS_MATCH_ID,GREENBOOK,GREENBOOK_RECORD_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,ASSEMBLY_DESCRIPTION,ASSEMBLY_ID,ASSEMBLY_RECORD_ID,QTESRVCOA_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,ENTITLEMENT_XML,CONFIGURATION_STATUS,PAR_SERVICE_ID,PAR_SERVICE_RECORD_ID,PAR_SERVICE_DESCRIPTION,QTESRVCOE_RECORD_ID,QUOTE_SERVICE_COV_OBJ_ASS_ENT_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED) SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_COV_OBJ_ASS_ENT_RECORD_ID, {UserId} as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM(SELECT IQ.*,M.ENTITLEMENT_XML,M.CONFIGURATION_STATUS,M.PAR_SERVICE_ID,M.PAR_SERVICE_RECORD_ID,M.PAR_SERVICE_DESCRIPTION,M.QUOTE_SERVICE_COVERED_OBJ_ENTITLEMENTS_RECORD_ID as QTESRVCOE_RECORD_ID FROM ( SELECT DISTINCT SAQTSE.KB_VERSION,SAQSCA.EQUIPMENT_ID,SAQSCA.EQUIPMENT_RECORD_ID,SAQTSE.QUOTE_ID,SAQTSE.QUOTE_RECORD_ID,SAQTSE.QTEREV_RECORD_ID,SAQTSE.QTEREV_ID,SAQTSE.SERVICE_DESCRIPTION,SAQTSE.SERVICE_ID,SAQTSE.SERVICE_RECORD_ID,SAQTSE.CPS_CONFIGURATION_ID,SAQTSE.CPS_MATCH_ID,SAQSCA.GREENBOOK,SAQSCA.GREENBOOK_RECORD_ID,SAQSCA.FABLOCATION_ID,SAQSCA.FABLOCATION_NAME,SAQSCA.FABLOCATION_RECORD_ID,SAQSCA.ASSEMBLY_DESCRIPTION,SAQSCA.ASSEMBLY_ID,SAQSCA.ASSEMBLY_RECORD_ID,SAQSCA.QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID as QTESRVCOA_RECORD_ID,SAQTSE.SALESORG_ID,SAQTSE.SALESORG_NAME,SAQTSE.SALESORG_RECORD_ID FROM SAQTSE (NOLOCK) JOIN (SELECT * FROM SAQSCA (NOLOCK) WHERE SAQSCA.QUOTE_RECORD_ID = '{ContractId}' AND SAQSCA.QTEREV_RECORD_ID = '{revision_rec_id}' ) SAQSCA ON SAQTSE.QUOTE_RECORD_ID = SAQSCA.QUOTE_RECORD_ID AND SAQTSE.QTEREV_RECORD_ID = SAQSCA.QTEREV_RECORD_ID AND SAQTSE.SERVICE_RECORD_ID = SAQSCA.SERVICE_RECORD_ID WHERE SAQTSE.QUOTE_RECORD_ID = '{ContractId}' AND SAQTSE.QTEREV_RECORD_ID = '{revision_rec_id}' AND SAQTSE.SERVICE_ID = '{serviceId}') IQ JOIN SAQSCE (NOLOCK) M ON M.SERVICE_RECORD_ID = IQ.SERVICE_RECORD_ID AND M.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND M.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND M.EQUIPMENT_ID = IQ.EQUIPMENT_ID )IQ""".format(UserId=self.user_id, QuoteRecordId=self.contract_quote_record_id, serviceId=self.ancillary_obj, revision_rec_id = self.contract_quote_revision_record_id)
				Log.Info('SAQSAE_ent_anc_renewal--393--renewal-1881-----'+str(SAQSAE_ent_anc_renewal))

		except Exception as e:
			Log.Info("error on ancillary--"+str(e)+'--'+str(str(sys.exc_info()[-1].tb_lineno)))

	def _delete_operation(self):
		delete_obj_list = []
		if self.tablename == "SAQTSE": 
			delete_obj_list = ["SAQTSV","SAQSFB","SAQSGB","SAQSCO","SAQSCA","SAQTSE","SAQSFE","SAQSGE","SAQSCE","SAQSAE"]
		elif self.tablename == "SAQSFE":
			delete_obj_list = ["SAQSFB","SAQSGB","SAQSCO","SAQSCA","SAQSFE","SAQSGE","SAQSCE","SAQSAE"]
		elif self.tablename == "SAQSGE":
			delete_obj_list = ["SAQSGB","SAQSCO","SAQSCA","SAQSGE","SAQSCE","SAQSAE"] 
		elif self.tablename == "SAQSCE":
			delete_obj_list = ["SAQSCO","SAQSCA","SAQSCE","SAQSAE"] 
		elif self.tablename == "SAQSAE":
			delete_obj_list = ["SAQSCA","SAQSAE"]
		
		if self.action_type == "DELETE_ENT_EQUIPMENT":
			delete_obj_list = ["SAQSFE","SAQSGE","SAQSCE","SAQSAE"]
		for obj in delete_obj_list:
			#Sql.RunQuery("DELETE FROM {} WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID ='{}' AND PAR_SERVICE_ID = '{}'".format(obj, self.contract_quote_record_id, self.contract_quote_revision_record_id ,self.ancillary_obj, self.service_id))
			ancillary_where = re.sub("SERVICE_ID","PAR_SERVICE_ID",self.where_string)
			Sql.RunQuery("DELETE FROM {} WHERE {} AND SERVICE_ID = '{}'".format(obj,ancillary_where,self.ancillary_obj))

	
	
try:			
	ancillary_obj = Param.ancillary_obj
except :
	ancillary_obj ='' 
action_type = Param.ActionType
quote_record_id = Param.quote_record_id
revision_rec_id = Param.revision_rec_id
service_id  = Param.service_id
try:
	where_string = Param.where_string
except:
	where_string = '' 
try:
	tablename = Param.tablename
except:
	tablename = ""
auto_ancillary_obj = AncillaryProductOperation()
auto_ancillary_obj._do_opertion()
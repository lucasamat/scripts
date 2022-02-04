# =========================================================================================================================================
#   __script_name : CQENANCOPR.py
#   __script_description : THIS SCRIPT IS USED FOR ANCILLARY PRODUCT OPERATIONS(insert,roll down)
#   __primary_author__ : SELVI
#   __create_date :8/23/2021
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import System.Net
import re
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
		self.where_string = where_string.replace("WHERE","")
		self.tablename = tablename
		self.attributeList = attributeList
		# if self.tablename in ("SAQSGE","SAQSCE","SAQSAE"):
		# 	pattern = re.compile(r''+str('FABLOCATION_ID')+'\s*\=\s*\'([^>]*?)\'')
		# 	self.fab = re.search(pattern, self.where_string).group(1)
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
			#self._insert_fab()
			self._insert_grn()
			self._equipment_insert()
			self._insert_assembly()

		elif self.action_type == "DELETE_SERVICE":
			self._delete_operation()
		elif  self.action_type == "INSERT_ENT_EQUIPMENT":
			self._delete_entitlement_tables()
			self._insert_service_ent()
			#if self.service_id in ('Z0091','Z0035'):
			self._update_entitlement()
			self._entitlement_rolldown()
		# elif self.action_type == "DELETE_ENT_EQUIPMENT":
		# 	self._delete_entitlement_tables()

	def _insert_service_offering(self):
		material_obj = Sql.GetFirst("SELECT MATERIAL_RECORD_ID,SAP_DESCRIPTION,MATERIALCONFIG_TYPE FROM MAMTRL WHERE SAP_PART_NUMBER = '{}'".format(self.ancillary_obj))
		get_existing_record = Sql.GetFirst("SELECT count(CpqTableEntryId) as cnt FROM SAQTSV WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID ='{}' AND PAR_SERVICE_ID = '{}'".format(self.contract_quote_record_id, self.contract_quote_revision_record_id ,self.ancillary_obj, self.service_id))
		if material_obj and get_existing_record.cnt == 0:
			description = material_obj.SAP_DESCRIPTION
			material_record_id = material_obj.MATERIAL_RECORD_ID

			Sql.RunQuery("""INSERT SAQTSV (QTEREV_RECORD_ID,QTEREV_ID,QUOTE_ID, QUOTE_NAME,UOM_ID,UOM_RECORD_ID, QUOTE_RECORD_ID, SERVICE_DESCRIPTION, SERVICE_ID, PAR_SERVICE_ID,PAR_SERVICE_DESCRIPTION,PAR_SERVICE_RECORD_ID,SERVICE_RECORD_ID, SERVICE_TYPE, CONTRACT_VALID_FROM, CONTRACT_VALID_TO, SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID,QUOTE_SERVICE_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified)
							SELECT A.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED, {UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
							SELECT DISTINCT QTEREV_RECORD_ID, QTEREV_ID,QUOTE_ID, QUOTE_NAME,UOM_ID,UOM_RECORD_ID, QUOTE_RECORD_ID, '{description}' AS SERVICE_DESCRIPTION, '{ancillary_object}' AS SERVICE_ID,SERVICE_ID as PAR_SERVICE_ID,SERVICE_DESCRIPTION AS PAR_SERVICE_DESCRIPTION,QUOTE_SERVICE_RECORD_ID as PAR_SERVICE_RECORD_ID, '{material_record_id}' AS SERVICE_RECORD_ID, '' AS SERVICE_TYPE, CONTRACT_VALID_FROM, CONTRACT_VALID_TO, SALESORG_ID, SALESORG_NAME,SALESORG_RECORD_ID FROM SAQTSV (NOLOCK)
							WHERE SERVICE_ID = '{service_id}' AND QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' 
							) A""".format(description=description, service_id = self.service_id, material_record_id = material_record_id,QuoteRecordId = self.contract_quote_record_id, RevisionRecordId = self.contract_quote_revision_record_id ,UserName = self.user_name, UserId = self.user_id, ancillary_object = self.ancillary_obj ))
	
	# def _insert_fab(self):
	# 	get_service_details = Sql.GetFirst("SELECT * FROM SAQTSV WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID ='{}' AND PAR_SERVICE_ID = '{}'".format(self.contract_quote_record_id, self.contract_quote_revision_record_id ,self.ancillary_obj, self.service_id))
	# 	Sql.RunQuery(
	# 			"""INSERT SAQSFB(
	# 				FABLOCATION_ID,
	# 				FABLOCATION_NAME,
	# 				FABLOCATION_RECORD_ID,
	# 				SERVICE_ID,
	# 				SERVICE_TYPE,
	# 				SERVICE_DESCRIPTION,
	# 				SERVICE_RECORD_ID,
	# 				FABLOCATION_STATUS,
	# 				QUOTE_ID,
	# 				QUOTE_NAME,
	# 				QUOTE_RECORD_ID,
	# 				QTEREV_ID,
	# 				QTEREV_RECORD_ID,
	# 				MNT_PLANT_ID,
	# 				MNT_PLANT_NAME,
	# 				MNT_PLANT_RECORD_ID,
	# 				ADDRESS_1,
	# 				ADDRESS_2,
	# 				CITY,
	# 				COUNTRY,
	# 				COUNTRY_RECORD_ID,
	# 				SALESORG_ID,
	# 				SALESORG_NAME,
	# 				SALESORG_RECORD_ID,
	# 				CONTRACT_VALID_FROM,
	# 				CONTRACT_VALID_TO,
	# 				PAR_SERVICE_DESCRIPTION,
	# 				PAR_SERVICE_ID,
	# 				PAR_SERVICE_RECORD_ID,
	# 				QUOTE_SERVICE_FAB_LOCATION_RECORD_ID,
	# 				CPQTABLEENTRYADDEDBY,
	# 				CPQTABLEENTRYDATEADDED,
	# 				CpqTableEntryModifiedBy,
	# 				CpqTableEntryDateModified
	# 				) SELECT FB.*,CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_FAB_LOCATION_RECORD_ID,
	# 				'{UserName}' AS CPQTABLEENTRYADDEDBY,
	# 				GETDATE() as CPQTABLEENTRYDATEADDED, {UserId} as CpqTableEntryModifiedBy,
	# 				GETDATE() as CpqTableEntryDateModified FROM (
	# 				SELECT DISTINCT
	# 				FABLOCATION_ID,
	# 				FABLOCATION_NAME,
	# 				FABLOCATION_RECORD_ID,
	# 				'{serviceid}' as SERVICE_ID,
	# 				'{service_type}' as SERVICE_TYPE,
	# 				'{desc}' as SERVICE_DESCRIPTION,
	# 				'{rec}' as SERVICE_RECORD_ID,
	# 				FABLOCATION_STATUS,
	# 				QUOTE_ID,
	# 				QUOTE_NAME,
	# 				QUOTE_RECORD_ID,
	# 				QTEREV_ID,
	# 				QTEREV_RECORD_ID,
	# 				MNT_PLANT_ID,
	# 				MNT_PLANT_NAME,
	# 				MNT_PLANT_RECORD_ID,
	# 				ADDRESS_1,
	# 				ADDRESS_2,
	# 				CITY,
	# 				COUNTRY,
	# 				COUNTRY_RECORD_ID,
	# 				SALESORG_ID,
	# 				SALESORG_NAME,
	# 				SALESORG_RECORD_ID,
	# 				CONTRACT_VALID_FROM,
	# 				CONTRACT_VALID_TO,
	# 				SERVICE_DESCRIPTION as PAR_SERVICE_DESCRIPTION,
	# 				SERVICE_ID as PAR_SERVICE_ID,
	# 				SERVICE_RECORD_ID as PAR_SERVICE_RECORD_ID
	# 				FROM SAQSFB (NOLOCK)
					
	# 				WHERE QUOTE_RECORD_ID = '{QuoteRecordId}'  AND QTEREV_RECORD_ID = '{RevisionRecordId}'  AND SERVICE_ID ='{par_service_id}' {addtional_where} AND SAQSFB.FABLOCATION_ID not in (SELECT FABLOCATION_ID FROM SAQSFB (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}'  AND QTEREV_RECORD_ID = '{RevisionRecordId}'  AND PAR_SERVICE_ID ='{par_service_id}' AND SERVICE_ID ='{serviceid}')
	# 				) FB""".format(
	# 								par_service_id = self.service_id,
	# 								QuoteRecordId=self.contract_quote_record_id,
	# 								RevisionRecordId=self.contract_quote_revision_record_id,
	# 								UserId=self.user_id,
	# 								UserName=self.user_name,
	# 								serviceid = self.ancillary_obj ,
	# 								desc = get_service_details.SERVICE_DESCRIPTION,
	# 								rec = get_service_details.SERVICE_RECORD_ID,
	# 								addtional_where = " AND FABLOCATION_ID = '{}'".format(self.fab) if self.fab else "",
	# 								service_type = ""
	# 							)
	# 			)				
		
	def _insert_grn(self):
		addtional_where = ""
		get_service_details = Sql.GetFirst("SELECT * FROM SAQTSV WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID ='{}' AND PAR_SERVICE_ID = '{}'".format(self.contract_quote_record_id, self.contract_quote_revision_record_id ,self.ancillary_obj, self.service_id))
		#if self.fab:
		#	addtional_where = " AND FABLOCATION_ID = '{}' ".format(self.fab)
		if self.greenbook:
			addtional_where += " AND GREENBOOK = '{}'".format(self.greenbook)
		Sql.RunQuery(
				"""
					INSERT SAQSGB (
						QUOTE_SERVICE_GREENBOOK_RECORD_ID,
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
							'{desc}' as SERVICE_DESCRIPTION,
							'{serviceid}' as SERVICE_ID,
							'{rec}' as SERVICE_RECORD_ID,
							EQUIPMENT_QUANTITY,								
							CONTRACT_VALID_FROM,
							CONTRACT_VALID_TO,
							SERVICE_DESCRIPTION as PAR_SERVICE_DESCRIPTION,
							SERVICE_ID as PAR_SERVICE_ID,
							SERVICE_RECORD_ID as PAR_SERVICE_RECORD_ID,
							'{UserName}' AS CPQTABLEENTRYADDEDBY,
							GETDATE() as CPQTABLEENTRYDATEADDED,
							{UserId} as CpqTableEntryModifiedBy,
							GETDATE() as CpqTableEntryDateModified
							FROM SAQSGB (NOLOCK) 
							 
							WHERE QUOTE_RECORD_ID = '{QuoteRecordId}'  AND QTEREV_RECORD_ID = '{RevisionRecordId}'  AND SERVICE_ID ='{par_service_id}' {addtional_where} AND GREENBOOK NOT IN (SELECT M.GREENBOOK FROM SAQSGB M (NOLOCK) WHERE M.QUOTE_RECORD_ID = '{QuoteRecordId}' AND M.QTEREV_RECORD_ID = '{RevisionRecordId}' AND PAR_SERVICE_ID ='{par_service_id}' AND SERVICE_ID ='{serviceid}' )   )A             
					
					
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
				INSERT SAQSCA (
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
					CONTRACT_VALID_FROM,
					CONTRACT_VALID_TO,
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
					CONTRACT_VALID_FROM,
					CONTRACT_VALID_TO,
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
						
						addtional_where = addtional_where 
			)
		) 		

	def _insert_service_ent(self):
		get_service_details = Sql.GetList("SELECT SAQTSV.* FROM SAQTSV INNER JOIN MAMTRL ON SAP_PART_NUMBER = SERVICE_ID WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'  AND PAR_SERVICE_ID = '{}' AND MATERIALCONFIG_TYPE != 'SIMPLE MATERIAL'".format(self.contract_quote_record_id, self.contract_quote_revision_record_id , self.service_id))
		# anc_insert_dict ={}
		for addon in get_service_details:
			ent_disp_val = ent_val_code = AttributeID_Pass = NewValue = ''
			get_tooltip = ''
			tbrow = {}
			anc_request_url="https://cpservices-product-configuration.cfapps.us10.hana.ondemand.com/api/v2/configurations?autoCleanup=False"

			anc_fullresponse = ScriptExecutor.ExecuteGlobal("CQENTLNVAL", {'action':'GET_RESPONSE','partnumber':addon.SERVICE_ID,'request_url':anc_request_url,'request_type':"New"})
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
			#if get_service_details : 
			ProductVersionObj=Sql.GetFirst("Select product_id AS PRD_ID from product_versions(nolock) where SAPKBId = '"+str(anc_fullresponse['kbId'])+"' AND SAPKBVersion='"+str(anc_fullresponse['kbKey']['version'])+"'")
			get_existing_record = Sql.GetFirst("SELECT count(CpqTableEntryId) as cnt FROM SAQTSE WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID ='{}' AND PAR_SERVICE_ID = '{}'".format(self.contract_quote_record_id, self.contract_quote_revision_record_id ,addon.SERVICE_ID, self.service_id))
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
								
			Trace.Write("attributevalues----"+str(attributevalues))
			if ProductVersionObj and get_existing_record.cnt == 0:
				insertservice = ""
				for attrs in overallattributeslist:
					if attrs in attributevalues:
						HasDefaultvalue=True					
						STANDARD_ATTRIBUTE_VALUES=Sql.GetFirst("SELECT S.STANDARD_ATTRIBUTE_DISPLAY_VAL,S.STANDARD_ATTRIBUTE_CODE FROM STANDARD_ATTRIBUTE_VALUES (nolock) S INNER JOIN ATTRIBUTE_DEFN (NOLOCK) A ON A.STANDARD_ATTRIBUTE_CODE=S.STANDARD_ATTRIBUTE_CODE WHERE A.SYSTEM_ID = '{}' ".format(attrs))
						ent_disp_val = attributevalues[attrs]
						ent_val_code = attributevalues[attrs]
						#Log.Info("ent_disp_val----"+str(ent_disp_val))
					else:	
						#Trace.Write("else----"+str(attributevalues[attrs]))				
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
							Trace.Write("else------"+str(attrs)+"-"+str(attributevalues[attrs]))
							get_display_val = Sql.GetFirst("SELECT STANDARD_ATTRIBUTE_DISPLAY_VAL  from STANDARD_ATTRIBUTE_VALUES S INNER JOIN ATTRIBUTE_DEFN (NOLOCK) A ON A.STANDARD_ATTRIBUTE_CODE=S.STANDARD_ATTRIBUTE_CODE WHERE S.STANDARD_ATTRIBUTE_CODE = '{}' AND A.SYSTEM_ID = '{}' AND S.STANDARD_ATTRIBUTE_VALUE = '{}' ".format(STANDARD_ATTRIBUTE_VALUES.STANDARD_ATTRIBUTE_CODE,attrs,  attributevalues[attrs] ) )
							ent_disp_val = get_display_val.STANDARD_ATTRIBUTE_DISPLAY_VAL 
							
							# getslaes_value  = Sql.GetFirst("SELECT SALESORG_ID FROM SAQTRV WHERE QUOTE_RECORD_ID = '"+str(self.contract_quote_record_id)+"'")
							# if getslaes_value:
							# 	getquote_sales_val = getslaes_value.SALESORG_ID
							# get_il_sales = Sql.GetList("select SALESORG_ID from SASORG where country = 'IL'")
							# get_il_sales_list = [value.SALESORG_ID for value in get_il_sales]
					DTypeset={"Drop Down":"DropDown","Free Input, no Matching":"FreeInputNoMatching","Check Box":"CheckBox"}
					if ATTRIBUTE_DEFN.STANDARD_ATTRIBUTE_NAME:
						ent_desc = ATTRIBUTE_DEFN.STANDARD_ATTRIBUTE_NAME
					else:
						ent_desc = ''
					
					#ancillary insert based on aprent insert end
					# entitlement_obj = Sql.GetFirst("select ENTITLEMENT_ID,ENTITLEMENT_VALUE_CODE,ENTITLEMENT_DISPLAY_VALUE from (SELECT distinct e.QUOTE_RECORD_ID,e.QTEREV_RECORD_ID, replace(X.Y.value('(ENTITLEMENT_ID)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_ID,replace(X.Y.value('(ENTITLEMENT_VALUE_CODE)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_VALUE_CODE,replace(X.Y.value('(ENTITLEMENT_DISPLAY_VALUE)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_DISPLAY_VALUE FROM (select QUOTE_RECORD_ID,QTEREV_RECORD_ID,convert(xml,replace(ENTITLEMENT_XML,'&',';#38')) as ENTITLEMENT_XML from {table_name} (nolock) where QUOTE_RECORD_ID = '{contract_quote_record_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' and SERVICE_ID = '{service_id}' ) e OUTER APPLY e.ENTITLEMENT_XML.nodes('QUOTE_ITEM_ENTITLEMENT') as X(Y) ) as m where  ( ENTITLEMENT_ID like '{att_id}')".format(table_name = 'SAQTSE' ,contract_quote_record_id = self.contract_quote_record_id,quote_revision_record_id = self.contract_quote_revision_record_id,service_id = 'Z0091',att_id = 'AGS_'+str(addon.PAR_SERVICE_ID)+'_KPI_BPTKPI'))
					
					if str(ATTRIBUTE_DEFN.STANDARD_ATTRIBUTE_NAME).upper() == "BONUS & PENALTY TIED TO KPI":
						if str(addon.PAR_SERVICE_ID) == "Z0091":
							AttributeID_Pass = 'AGS_Z0035_KPI_BPTKPI'						
							NewValue = 'Yes'
					# entitlement_obj = Sql.GetFirst("select ENTITLEMENT_ID,ENTITLEMENT_VALUE_CODE,ENTITLEMENT_DISPLAY_VALUE from (SELECT distinct e.QUOTE_RECORD_ID,e.QTEREV_RECORD_ID, replace(X.Y.value('(ENTITLEMENT_ID)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_ID,replace(X.Y.value('(ENTITLEMENT_VALUE_CODE)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_VALUE_CODE,replace(X.Y.value('(ENTITLEMENT_DISPLAY_VALUE)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_DISPLAY_VALUE FROM (select QUOTE_RECORD_ID,QTEREV_RECORD_ID,convert(xml,replace(ENTITLEMENT_XML,'&',';#38')) as ENTITLEMENT_XML from {table_name} (nolock) where QUOTE_RECORD_ID = '{contract_quote_record_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' and SERVICE_ID = '{service_id}' ) e OUTER APPLY e.ENTITLEMENT_XML.nodes('QUOTE_ITEM_ENTITLEMENT') as X(Y) ) as m where  ( ENTITLEMENT_ID like '{att_id}')".format(table_name = 'SAQTSE' ,contract_quote_record_id = self.contract_quote_record_id,quote_revision_record_id = self.contract_quote_revision_record_id,service_id = 'Z0091',att_id = 'AGS_'+str(addon.PAR_SERVICE_ID)+'_PQB_PPCPRM'))
					#if str(ATTRIBUTE_DEFN.STANDARD_ATTRIBUTE_NAME).upper() == "PRICE PER CRITICAL PARAMETER":
						#AttributeID_Pass = 'AGS_'+str(addon.PAR_SERVICE_ID)+'_PQB_PPCPRM'
						# if entitlement_obj:
						# 	ent_disp = entitlement_obj.ENTITLEMENT_DISPLAY_VALUE
						# 	if str(ent_disp).upper() == 'YES':
						#NewValue = 'Yes'
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
				tbrow["QUOTE_ID"]=addon.QUOTE_ID
				tbrow["ENTITLEMENT_XML"]=insertservice
				tbrow["QUOTE_NAME"]=addon.QUOTE_NAME
				tbrow["QUOTE_RECORD_ID"]=addon.QUOTE_RECORD_ID
				tbrow["QTESRV_RECORD_ID"]=addon.SERVICE_RECORD_ID
				tbrow["SERVICE_RECORD_ID"]=addon.SERVICE_RECORD_ID
				tbrow["SERVICE_ID"]= addon.SERVICE_ID
				tbrow["SERVICE_DESCRIPTION"]=addon.SERVICE_DESCRIPTION
				tbrow["CPS_CONFIGURATION_ID"]= anc_fullresponse['id']
				tbrow["SALESORG_RECORD_ID"]=addon.SALESORG_RECORD_ID
				tbrow["SALESORG_ID"]=addon.SALESORG_ID
				tbrow["SALESORG_NAME"]=addon.SALESORG_NAME
				tbrow["CPS_MATCH_ID"] = 1
				tbrow["CPQTABLEENTRYADDEDBY"] = self.user_id
				tbrow["CPQTABLEENTRYDATEADDED"] = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p")
				tbrow["QTEREV_RECORD_ID"] = self.contract_quote_revision_record_id 
				tbrow["QTEREV_ID"] = addon.QTEREV_ID
				tbrow["CONFIGURATION_STATUS"] = anc_configuration_status
				tbrow["PAR_SERVICE_ID"] = addon.PAR_SERVICE_ID
				tbrow["PAR_SERVICE_RECORD_ID"] = addon.PAR_SERVICE_RECORD_ID
				tbrow["PAR_SERVICE_DESCRIPTION"] = addon.PAR_SERVICE_DESCRIPTION
				columns = ', '.join("" + str(x) + "" for x in tbrow.keys())
				values = ', '.join("'" + str(x) + "'" for x in tbrow.values())
				insert_qtqtse_query = "INSERT INTO SAQTSE ( %s ) VALUES ( %s );" % (columns, values)
				Sql.RunQuery(insert_qtqtse_query)
				if addon.PAR_SERVICE_ID and NewValue == "Yes":
					#ancillary insert based on aprent insert start
					try:						
						add_where =''
						ServiceId = addon.SERVICE_ID
						whereReq = "QUOTE_RECORD_ID = '{}' and SERVICE_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(addon.QUOTE_RECORD_ID,addon.SERVICE_ID,self.contract_quote_revision_record_id)
						ent_params_list = str(whereReq)+"||"+str(add_where)+"||"+str(AttributeID_Pass)+"||"+str(NewValue)+"||"+str(ServiceId) + "||" + 'SAQTSE'
						result = ScriptExecutor.ExecuteGlobal("CQASSMEDIT", {"ACTION": 'UPDATE_ENTITLEMENT', 'ent_params_list':ent_params_list})
					except:
						Log.Info('656--661---eroror--')
						Trace.Write('error--296')
				# else:
				# 	try:
				# 		Log.Info('636--646----'+str(contract_quote_record_id))
				# 		get_c4c_quote_id = Sql.GetFirst("select * from SAQTMT where MASTER_TABLE_QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(contract_quote_record_id,self.contract_quote_revision_record_id))
				# 		ent_temp = "ENT_BKP_"+str(get_c4c_quote_id.C4C_QUOTE_ID)
				# 		ent_temp_drop = Sql.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(ent_temp)+"'' ) BEGIN DROP TABLE "+str(ent_temp)+" END  ' ")
				# 		where_cond = "QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID = '{}'".format(self.contract_quote_record_id, self.contract_quote_revision_record_id , self.service_id)
				# 		where_cond = where_cond.replace("'","''")
				# 		Log.Info('636--646---where_cond-'+str(where_cond))
				# 		Sql.GetFirst("sp_executesql @T=N'declare @H int; Declare @val Varchar(MAX);DECLARE @XML XML; SELECT @val = FINAL from(select  REPLACE(entitlement_xml,''<QUOTE_ITEM_ENTITLEMENT>'',sml) AS FINAL FROM (select ''  <QUOTE_ITEM_ENTITLEMENT><QUOTE_ID>''+quote_id+''</QUOTE_ID><QUOTE_RECORD_ID>''+QUOTE_RECORD_ID+''</QUOTE_RECORD_ID><QTEREV_RECORD_ID>''+QTEREV_RECORD_ID+''</QTEREV_RECORD_ID><SERVICE_ID>''+service_id+''</SERVICE_ID>'' AS sml,replace(replace(replace(replace(replace(replace(replace(ENTITLEMENT_XML,''&'','';#38''),'''','';#39''),'' < '','' &lt; '' ),'' > '','' &gt; '' ),''_>'',''_&gt;''),''_<'',''_&lt;''),''&'','';#38'')   as entitlement_xml from SAQTSE (nolock)  WHERE "+str(where_cond)+"  )A )a SELECT @XML = CONVERT(XML,''<ROOT>''+@VAL+''</ROOT>'') exec sys.sp_xml_preparedocument @H output,@XML; select QUOTE_ID,QUOTE_RECORD_ID,QTEREV_RECORD_ID,SERVICE_ID,ENTITLEMENT_ID,ENTITLEMENT_NAME,ENTITLEMENT_COST_IMPACT,ENTITLEMENT_PRICE_IMPACT,CALCULATION_FACTOR,ENTITLEMENT_TYPE,ENTITLEMENT_VALUE_CODE,ENTITLEMENT_DISPLAY_VALUE,IS_DEFAULT INTO "+str(ent_temp)+"  from openxml(@H, ''ROOT/QUOTE_ITEM_ENTITLEMENT'', 0) with (QUOTE_ID VARCHAR(100) ''QUOTE_ID'',QUOTE_RECORD_ID VARCHAR(100) ''QUOTE_RECORD_ID'',QTEREV_RECORD_ID VARCHAR(100) ''QTEREV_RECORD_ID'',ENTITLEMENT_NAME VARCHAR(100) ''ENTITLEMENT_NAME'',ENTITLEMENT_ID VARCHAR(100) ''ENTITLEMENT_ID'',SERVICE_ID VARCHAR(100) ''SERVICE_ID'',ENTITLEMENT_COST_IMPACT VARCHAR(100) ''ENTITLEMENT_COST_IMPACT'',ENTITLEMENT_PRICE_IMPACT VARCHAR(100) ''ENTITLEMENT_PRICE_IMPACT'',CALCULATION_FACTOR VARCHAR(100) ''CALCULATION_FACTOR'',ENTITLEMENT_TYPE VARCHAR(100) ''ENTITLEMENT_TYPE'',ENTITLEMENT_VALUE_CODE VARCHAR(100) ''ENTITLEMENT_VALUE_CODE'',ENTITLEMENT_DISPLAY_VALUE VARCHAR(100) ''ENTITLEMENT_DISPLAY_VALUE'',IS_DEFAULT VARCHAR(100) ''IS_DEFAULT'') ; exec sys.sp_xml_removedocument @H; '")

				# 		GetXMLsecField=Sql.GetList("SELECT * FROM {} ".format(ent_temp))
				# 		Log.Info('GetXMLsecField-655--'+str(ent_temp))
				# 		for val in GetXMLsecField:
				# 			Log.Info('GetXMLsecField-inside loop--'+str(ent_temp))
				# 			if str(addon.SERVICE_ID) in val.ENTITLEMENT_ID:
				# 				Log.Info('647--'+str(val.ENTITLEMENT_ID))
				# 				if val.ENTITLEMENT_DISPLAY_VALUE:
				# 					try:						
				# 						add_where =''
										
				# 						NewValue = val.ENTITLEMENT_DISPLAY_VALUE
				# 						AttributeID_Pass = val.ENTITLEMENT_ID
				# 						#ServiceId = serviceId
				# 						whereReq = "QUOTE_RECORD_ID = '{}' and SERVICE_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(addon.QUOTE_RECORD_ID,addon.SERVICE_ID,self.contract_quote_revision_record_id)
				# 						ent_params_list = str(whereReq)+"||"+str(add_where)+"||"+str(AttributeID_Pass)+"||"+str(NewValue)+"||"+str(ServiceId) + "||" + 'SAQTSE'
										
				# 						result = ScriptExecutor.ExecuteGlobal("CQASSMEDIT", {"ACTION": 'UPDATE_ENTITLEMENT', 'ent_params_list':ent_params_list})
				# 					except:
				# 						Trace.Write('error--296')
				# 				#anc_insert_dict[val.ENTITLEMENT_ID] = val.ENTITLEMENT_DISPLAY_VALUE
				# 		ent_temp_drop = Sql.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(ent_temp)+"'' ) BEGIN DROP TABLE "+str(ent_temp)+" END  ' ")

				# except:
				# 	Trace.Write('592----------')

	def _construct_dict_xml(self,updateentXML):
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

	def _update_entitlement_values(self,anc_service = '',ent_table = ''):
		try:
			where_cond = self.where_string.replace('SERVICE_ID','PAR_SERVICE_ID')
			where_cond += " AND SERVICE_ID = '{}'".format(anc_service)
			check_ancillary = Sql.GetFirst("SELECT COUNT(SERVICE_ID) AS CNT FROM SAQTSE WHERE QUOTE_RECORD_ID ='{}' AND QTEREV_RECORD_ID = '{}' AND PAR_SERVICE_ID ='{}' AND SERVICE_ID ='{}'".format(self.contract_quote_record_id, self.contract_quote_revision_record_id ,self.service_id, anc_service) )
			if check_ancillary.CNT > 0 and self.tablename == 'SAQSGE':
				get_parent_xml = Sql.GetList("SELECT * FROM {} WHERE {}".format(ent_table, self.where_string) )
				get_anc_xml_dict = {}
				for parent in get_parent_xml:
					joinstr = ''
					assign_xml = {}
					if ent_table == 'SAQSCE':
						joinstr = " AND EQUIPEMNT_ID = '{}'".format(parent.EQUIPMENT_ID)
					getall_recid = Sql.GetFirst("SELECT * FROM {} WHERE QUOTE_RECORD_ID ='{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID ='{}' AND PAR_SERVICE_ID = '{}' AND GREENBOOK = '{}' {}".format(ent_table,self.contract_quote_record_id, self.contract_quote_revision_record_id, anc_service ,self.service_id, parent.GREENBOOK, joinstr) )
					if getall_recid:
						get_parent_dict = self._construct_dict_xml(parent.ENTITLEMENT_XML)
						get_anc_xml_dict = self._construct_dict_xml(getall_recid.ENTITLEMENT_XML)
						if get_parent_dict and get_anc_xml_dict:
							for key,value in get_anc_xml_dict.items():
								if key in get_parent_dict.keys()  :
									value = get_parent_dict[key]
								assign_xml += value
							where_cond += joinstr
							Sql.RunQuery("UPDATE {} SET ENTITLEMENT_XML = '{}' WHERE {} ".format(ent_table, assign_xml, where_cond) )
							if ent_table == 'SAQSGE':
								cpsmatchID,Configurationid = ScriptExecutor.ExecuteGlobal("CQENTLNVAL", {'action':'ENTITLEMENT_UPDATE',
												'partnumber':anc_service,
												'where_cond' :where_cond, 
												'ent_level_table': ent_table, 
												'quote_record_id':self.contract_quote_record_id,
												'revision_record_id':self.contract_quote_revision_record_id})
								Trace.Write("value--"+str(cpsmatchID)+'-'+str(Configurationid))
								#Sql.RunQuery("UPDATE {} SET CPS_CONFIGURATION_ID = '{}',CPS_MATCH_ID={}  {} ".format(obj,newConfigurationid,cpsmatchID,where_condition))
		except Exception as e:
			Trace.Write("error on ancillary--"+str(e)+'--'+str(str(sys.exc_info()[-1].tb_lineno)))


	def _update_entitlement(self):
		#Log.Info('attr--685--ttributeList----'+str(self.attributeList))
		# attr_id = value_application = ''
		try:
			#Log.Info('636--646--700--'+str(self.contract_quote_record_id))
			get_c4c_quote_id = Sql.GetFirst("select * from SAQTMT where MASTER_TABLE_QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(self.contract_quote_record_id,self.contract_quote_revision_record_id))
			ent_temp = "ENT_BKP_"+str(get_c4c_quote_id.C4C_QUOTE_ID)
			ent_temp_drop = Sql.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(ent_temp)+"'' ) BEGIN DROP TABLE "+str(ent_temp)+" END  ' ")
			where_cond = "QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID = '{}'".format(self.contract_quote_record_id,self.contract_quote_revision_record_id , self.service_id)
			where_cond = where_cond.replace("'","''")
			#Log.Info('636--646---706---where_cond-'+str(where_cond))
			Sql.GetFirst("sp_executesql @T=N'declare @H int; Declare @val Varchar(MAX);DECLARE @XML XML; SELECT @val = FINAL from(select  REPLACE(entitlement_xml,''<QUOTE_ITEM_ENTITLEMENT>'',sml) AS FINAL FROM (select ''  <QUOTE_ITEM_ENTITLEMENT><QUOTE_ID>''+quote_id+''</QUOTE_ID><QUOTE_RECORD_ID>''+QUOTE_RECORD_ID+''</QUOTE_RECORD_ID><QTEREV_RECORD_ID>''+QTEREV_RECORD_ID+''</QTEREV_RECORD_ID><SERVICE_ID>''+service_id+''</SERVICE_ID>'' AS sml,replace(replace(replace(replace(replace(replace(replace(replace(replace(ENTITLEMENT_XML,''&'','';#38''),'''','';#39''),'' < '','' &lt; '' ),'' > '','' &gt; '' ),''_>'',''_&gt;''),''_<'',''_&lt;''),''&'','';#38''),''<10%'',''&lt;10%''),''<='',''&lt;='')  as entitlement_xml from SAQTSE (nolock)  WHERE "+str(where_cond)+"  )A )a SELECT @XML = CONVERT(XML,''<ROOT>''+@VAL+''</ROOT>'') exec sys.sp_xml_preparedocument @H output,@XML; select QUOTE_ID,QUOTE_RECORD_ID,QTEREV_RECORD_ID,SERVICE_ID,ENTITLEMENT_ID,ENTITLEMENT_NAME,ENTITLEMENT_COST_IMPACT,ENTITLEMENT_PRICE_IMPACT,CALCULATION_FACTOR,ENTITLEMENT_TYPE,ENTITLEMENT_VALUE_CODE,ENTITLEMENT_DISPLAY_VALUE,IS_DEFAULT INTO "+str(ent_temp)+"  from openxml(@H, ''ROOT/QUOTE_ITEM_ENTITLEMENT'', 0) with (QUOTE_ID VARCHAR(100) ''QUOTE_ID'',QUOTE_RECORD_ID VARCHAR(100) ''QUOTE_RECORD_ID'',QTEREV_RECORD_ID VARCHAR(100) ''QTEREV_RECORD_ID'',ENTITLEMENT_NAME VARCHAR(100) ''ENTITLEMENT_NAME'',ENTITLEMENT_ID VARCHAR(100) ''ENTITLEMENT_ID'',SERVICE_ID VARCHAR(100) ''SERVICE_ID'',ENTITLEMENT_COST_IMPACT VARCHAR(100) ''ENTITLEMENT_COST_IMPACT'',ENTITLEMENT_PRICE_IMPACT VARCHAR(100) ''ENTITLEMENT_PRICE_IMPACT'',CALCULATION_FACTOR VARCHAR(100) ''CALCULATION_FACTOR'',ENTITLEMENT_TYPE VARCHAR(100) ''ENTITLEMENT_TYPE'',ENTITLEMENT_VALUE_CODE VARCHAR(100) ''ENTITLEMENT_VALUE_CODE'',ENTITLEMENT_DISPLAY_VALUE VARCHAR(100) ''ENTITLEMENT_DISPLAY_VALUE'',IS_DEFAULT VARCHAR(100) ''IS_DEFAULT'') ; exec sys.sp_xml_removedocument @H; '")

			GetXMLsecField=Sql.GetList("SELECT * FROM {} ".format(ent_temp))
			#Log.Info('GetXMLsecField-655-710------'+str(ent_temp))
			for val in GetXMLsecField:
				#Log.Info('GetXMLsecField-inside loop--'+str(ent_temp))
				if val.ENTITLEMENT_ID:
					Trace.Write('647--'+str(val.ENTITLEMENT_ID))
					if val.ENTITLEMENT_DISPLAY_VALUE:
						try:
							AttributeID_Pass =""						
							add_where =''
							NewValue = val.ENTITLEMENT_DISPLAY_VALUE
							# if str(val.ENTITLEMENT_ID) == "AGS_{}_KPI_BPTKPI".format(self.service_id) and NewValue == "Yes":
							# 	AttributeID_Pass = 'AGS_Z0035_KPI_BPTKPI'
							if str(val.ENTITLEMENT_ID) == "AGS_{}_PQB_PPCPRM".format(self.service_id) and NewValue == "Yes":
								AttributeID_Pass = 'AGS_Z0046_PQB_PPCPRM'
								# value_application = 'YES'
							else:
								if 'AGS_Z0046' in val.ENTITLEMENT_ID:
									ServiceId = 'Z0046'
									AttributeID_Pass = val.ENTITLEMENT_ID
								elif 'AGS_Z0101' in val.ENTITLEMENT_ID:
									ServiceId = 'Z0101'
									AttributeID_Pass = val.ENTITLEMENT_ID
								elif 'AGS_Z0100' in val.ENTITLEMENT_ID:
									ServiceId = 'Z0100'
									AttributeID_Pass = val.ENTITLEMENT_ID
								elif 'AGS_Z0048' in val.ENTITLEMENT_ID:
									ServiceId = 'Z0048'
									AttributeID_Pass = val.ENTITLEMENT_ID
								# if 'AGS_Z0091_PRODUCT_TYPE' in val.ENTITLEMENT_ID:
								# 	AttributeID_Pass = val.ENTITLEMENT_ID
								# 	ServiceId = 'Z0101'
							if AttributeID_Pass:
								#ServiceId = 'Z0046'
							
								whereReq = "QUOTE_RECORD_ID = '{}' and SERVICE_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(self.contract_quote_record_id,ServiceId,self.contract_quote_revision_record_id)
								ent_params_list = str(whereReq)+"||"+str(add_where)+"||"+str(AttributeID_Pass)+"||"+str(NewValue)+"||"+str(ServiceId) + "||" + 'SAQTSE'
								
								result = ScriptExecutor.ExecuteGlobal("CQASSMEDIT", {"ACTION": 'UPDATE_ENTITLEMENT', 'ent_params_list':ent_params_list})
						except Exception as e:
							Log.Info('error--296'+str(e))
							Trace.Write('erroe on update'+str(e))
			
			ent_temp_drop = Sql.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(ent_temp)+"'' ) BEGIN DROP TABLE "+str(ent_temp)+" END  ' ")
		except:
			Log.Info('728-----')

		
		self._delete_entitlement_tables_anc()

	def _delete_entitlement_tables_anc(self):
		if self.tablename == "SAQTSE": 
			delete_obj_list = ["SAQSGE","SAQSCE","SAQSAE"]
		# elif self.tablename == "SAQSFE": 
		# 	delete_obj_list = ["SAQSGE","SAQSCE","SAQSAE"]
		elif self.tablename == "SAQSGE": 
			delete_obj_list = ["SAQSCE","SAQSAE"]
		elif self.tablename == "SAQSCE": 
			delete_obj_list = ["SAQSAE"]

		ancillary_where = re.sub(r'AND SERVICE_ID\s*\=\s*\'[^>]*?\'', '', self.where_string )
		for obj in delete_obj_list:
			Sql.RunQuery("DELETE FROM {obj} WHERE {where} AND PAR_SERVICE_ID IN (SELECT SERVICE_ID FROM {obj}  WHERE {par_where}) AND SERVICE_ID NOT IN (SELECT ADNPRD_ID FROM SAQSAO WHERE QUOTE_RECORD_ID='{quote_rec_id}' and SERVICE_ID = '{service_id}' AND QTEREV_RECORD_ID = '{revision_rec_id}' )".format(obj = obj, where=  ancillary_where, par_where = self.where_string ,quote_rec_id= self.contract_quote_record_id,revision_rec_id = self.contract_quote_revision_record_id,service_id = self.service_id ))

	def _entitlement_rolldown(self):
		try:
			addtional_where = ""
			if self.fab:
				addtional_where = " AND FABLOCATION_ID = '{}' ".format(self.fab)
			if self.greenbook:
				addtional_where += " AND GREENBOOK = '{}'".format(self.greenbook)
			if self.equipment_id:
				addtional_where += " AND EQUIPMENT_ID = '{}'".format(self.equipment_id)
			if self.assembly:
				addtional_where += " AND ASSEMBLY_ID = '{}'".format(self.assembly)

			# ancillary_where = re.sub("SERVICE_ID","PAR_SERVICE_ID",self.where_string)
			# ancillary_where += " AND SERVICE_ID = '{}'".format(self.ancillary_obj)
			
			get_ancillaryservice = Sql.GetFirst("select * from SAQTSE WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND PAR_SERVICE_ID = '{}'".format(self.contract_quote_record_id, self.contract_quote_revision_record_id , self.service_id))
			#QUOTE_RECORD_ID = '{QuoteRecordId}'  AND QTEREV_RECORD_ID = '{RevisionRecordId}'  AND SERVICE_ID ='{par_service_id}' {addtional_where}
		
			if get_ancillaryservice :				
				# get_ancillary_fab = Sql.GetFirst("select count(CpqTableEntryId) as cnt from SAQSFE WHERE QUOTE_RECORD_ID = '{}'  AND QTEREV_RECORD_ID = '{}' AND PAR_SERVICE_ID ='{}' {}".format(self.contract_quote_record_id, self.contract_quote_revision_record_id, self.service_id, addtional_where))
				# if get_ancillary_fab:
				# 	if get_ancillary_fab.cnt == 0:
						
				# saqsfe_ancillary_query="""
				# 	INSERT SAQSFE (ENTITLEMENT_XML,QUOTE_ID,QUOTE_NAME,QUOTE_RECORD_ID,QTEREV_RECORD_ID,QTEREV_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,	
				# 	CPS_CONFIGURATION_ID, CPS_MATCH_ID,QTESRVENT_RECORD_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,QTESRVFBL_RECORD_ID,CONFIGURATION_STATUS,PAR_SERVICE_ID,PAR_SERVICE_RECORD_ID,PAR_SERVICE_DESCRIPTION,QUOTE_SERVICE_FAB_LOC_ENT_RECORD_ID, CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED)
				# 	SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_FAB_LOC_ENT_RECORD_ID, {UserId} as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM (SELECT 
				# 		DISTINCT	
				# 		SAQTSE.ENTITLEMENT_XML,SAQTSE.QUOTE_ID,SAQTSE.QUOTE_NAME,SAQTSE.QUOTE_RECORD_ID,SAQTSE.QTEREV_RECORD_ID,SAQTSE.QTEREV_ID,SAQTSE.SERVICE_DESCRIPTION,SAQTSE.SERVICE_ID,SAQTSE.SERVICE_RECORD_ID,SAQTSE.SALESORG_ID,SAQTSE.SALESORG_NAME,SAQTSE.SALESORG_RECORD_ID,SAQTSE.CPS_CONFIGURATION_ID, SAQTSE.CPS_MATCH_ID,SAQTSE.QUOTE_SERVICE_ENTITLEMENT_RECORD_ID as QTESRVENT_RECORD_ID,SAQSFB.FABLOCATION_ID, SAQSFB.FABLOCATION_NAME, SAQSFB.FABLOCATION_RECORD_ID, SAQSFB.QUOTE_SERVICE_FAB_LOCATION_RECORD_ID as QTESRVFBL_RECORD_ID,SAQTSE.CONFIGURATION_STATUS,SAQTSE.PAR_SERVICE_ID,SAQTSE.PAR_SERVICE_RECORD_ID,SAQTSE.PAR_SERVICE_DESCRIPTION
				# 	FROM SAQTSE (NOLOCK)
				# 	JOIN SAQSFB ON SAQSFB.PAR_SERVICE_ID = SAQTSE.PAR_SERVICE_ID AND SAQSFB.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID AND SAQSFB.QTEREV_RECORD_ID = SAQTSE.QTEREV_RECORD_ID AND SAQSFB.SERVICE_ID = SAQTSE.SERVICE_ID
				# 	JOIN SAQSFE ON SAQSFB.PAR_SERVICE_ID = SAQSFE.SERVICE_ID AND SAQSFB.QUOTE_RECORD_ID = SAQSFE.QUOTE_RECORD_ID AND SAQSFB.QTEREV_RECORD_ID = SAQSFE.QTEREV_RECORD_ID 
					
				# 	WHERE SAQTSE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQTSE.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQTSE.PAR_SERVICE_ID ='{par_service_id}' AND ISNULL(SAQSFE.CONFIGURATION_STATUS,'') = 'COMPLETE'  AND SAQSFB.FABLOCATION_ID not in (SELECT FABLOCATION_ID FROM SAQSFE M WHERE M.QUOTE_RECORD_ID = '{QuoteRecordId}' AND M.QTEREV_RECORD_ID = '{RevisionRecordId}' AND M.SERVICE_ID = SAQTSE.SERVICE_ID AND PAR_SERVICE_ID = '{par_service_id}')) IQ""".format(UserId=self.user_id, QuoteRecordId=self.contract_quote_record_id, RevisionRecordId = self.contract_quote_revision_record_id, par_service_id = self.service_id)
				# Sql.RunQuery(saqsfe_ancillary_query)
						
				
				# get_ancillary_grn = Sql.GetFirst("select count(CpqTableEntryId) as cnt from SAQSGE WHERE QUOTE_RECORD_ID = '{}'  AND QTEREV_RECORD_ID = '{}' AND PAR_SERVICE_ID ='{}' {}".format(self.contract_quote_record_id, self.contract_quote_revision_record_id, self.service_id, addtional_where))
				# if get_ancillary_grn:
				# 	if get_ancillary_grn.cnt == 0:
				# qtqsge_query_anc= """INSERT SAQSGE (KB_VERSION,QUOTE_ID,QUOTE_NAME,QUOTE_RECORD_ID,QTEREV_RECORD_ID,QTEREV_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,	
				# 	CPS_CONFIGURATION_ID, CPS_MATCH_ID,GREENBOOK,GREENBOOK_RECORD_ID,QTESRVENT_RECORD_ID,PAR_SERVICE_ID,PAR_SERVICE_DESCRIPTION,PAR_SERVICE_RECORD_ID,ENTITLEMENT_XML,CONFIGURATION_STATUS, QUOTE_SERVICE_GREENBOOK_ENTITLEMENT_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED )
				# 	SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_GREENBOOK_ENTITLEMENT_RECORD_ID, {UserId} as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM (SELECT DISTINCT SAQTSE.KB_VERSION,SAQTSE.QUOTE_ID,SAQTSE.QUOTE_NAME,SAQTSE.QUOTE_RECORD_ID,SAQTSE.QTEREV_RECORD_ID,SAQTSE.QTEREV_ID,SAQTSE.SERVICE_DESCRIPTION,SAQTSE.SERVICE_ID,SAQTSE.SERVICE_RECORD_ID,SAQTSE.SALESORG_ID,SAQTSE.SALESORG_NAME,SAQTSE.SALESORG_RECORD_ID,	
				# 	SAQTSE.CPS_CONFIGURATION_ID, SAQTSE.CPS_MATCH_ID,SAQSCO.GREENBOOK,SAQSCO.GREENBOOK_RECORD_ID,SAQTSE.QUOTE_SERVICE_ENTITLEMENT_RECORD_ID as QTESRVENT_RECORD_ID,SAQTSE.PAR_SERVICE_ID,SAQTSE.PAR_SERVICE_DESCRIPTION,SAQTSE.PAR_SERVICE_RECORD_ID,SAQTSE.ENTITLEMENT_XML,SAQTSE.CONFIGURATION_STATUS FROM
				# 	SAQTSE (NOLOCK) JOIN SAQSGB ON SAQTSE.SERVICE_ID = SAQSGB.PAR_SERVICE_ID  AND SAQTSE.QUOTE_RECORD_ID = SAQSGB.QUOTE_RECORD_ID AND SAQSGB.QTEREV_RECORD_ID = SAQTSE.QTEREV_RECORD_ID JOIN SAQSCO  (NOLOCK) ON SAQSCO.PAR_SERVICE_ID = SAQTSE.PAR_SERVICE_ID AND SAQSCO.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID  AND SAQSCO.QTEREV_RECORD_ID = SAQTSE.QTEREV_RECORD_ID and SAQSCO.FABLOCATION_RECORD_ID = SAQSGB.FABLOCATION_RECORD_ID and SAQSGB.GREENBOOK_RECORD_ID = SAQSCO.GREENBOOK_RECORD_ID

				# 	JOIN SAQSGE ON SAQSGE.SERVICE_ID = SAQSCO.PAR_SERVICE_ID AND SAQSCO.QUOTE_RECORD_ID = SAQSGE.QUOTE_RECORD_ID AND SAQSCO.QTEREV_RECORD_ID = SAQSGE.QTEREV_RECORD_ID AND SAQSGB.GREENBOOK_RECORD_ID = SAQSGE.GREENBOOK_RECORD_ID  
				# 	WHERE SAQTSE.QUOTE_RECORD_ID ='{QuoteRecordId}'  AND SAQTSE.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQTSE.SERVICE_ID = '{ServiceId}')IQ""".format(UserId=self.user_id, QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id, ServiceId=OfferingRow_detail.ADNPRD_ID)
				#commented for favb changes-start
				# 
				#end-
				qtqsge_query_anc= """INSERT SAQSGE (KB_VERSION,QUOTE_ID,QUOTE_NAME,QUOTE_RECORD_ID,QTEREV_RECORD_ID,QTEREV_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,	
					CPS_CONFIGURATION_ID, CPS_MATCH_ID,GREENBOOK,GREENBOOK_RECORD_ID,QTESRVENT_RECORD_ID,ENTITLEMENT_XML,CONFIGURATION_STATUS,PAR_SERVICE_ID,PAR_SERVICE_RECORD_ID,PAR_SERVICE_DESCRIPTION, QUOTE_SERVICE_GREENBOOK_ENTITLEMENT_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED )
					
					
					SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_GREENBOOK_ENTITLEMENT_RECORD_ID,{UserId} as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM (SELECT DISTINCT
					SAQTSE.KB_VERSION,SAQTSE.QUOTE_ID,SAQTSE.QUOTE_NAME,SAQTSE.QUOTE_RECORD_ID,SAQTSE.QTEREV_RECORD_ID,SAQTSE.QTEREV_ID,SAQTSE.SERVICE_DESCRIPTION,SAQTSE.SERVICE_ID,SAQTSE.SERVICE_RECORD_ID,SAQTSE.SALESORG_ID,SAQTSE.SALESORG_NAME,SAQTSE.SALESORG_RECORD_ID,	
					SAQTSE.CPS_CONFIGURATION_ID, SAQTSE.CPS_MATCH_ID,SAQSCO.GREENBOOK,SAQSCO.GREENBOOK_RECORD_ID,SAQTSE.QUOTE_SERVICE_ENTITLEMENT_RECORD_ID as QTESRVENT_RECORD_ID,SAQTSE.ENTITLEMENT_XML,SAQTSE.CONFIGURATION_STATUS,SAQTSE.PAR_SERVICE_ID,SAQTSE.PAR_SERVICE_RECORD_ID,SAQTSE.PAR_SERVICE_DESCRIPTION
					FROM
					SAQTSE (NOLOCK) 
					
					JOIN SAQSGB ON SAQTSE.PAR_SERVICE_ID = SAQSGB.PAR_SERVICE_ID  AND SAQTSE.QUOTE_RECORD_ID = SAQSGB.QUOTE_RECORD_ID AND SAQSGB.QTEREV_RECORD_ID = SAQTSE.QTEREV_RECORD_ID AND SAQTSE.SERVICE_ID = SAQSGB.SERVICE_ID

					JOIN SAQSCO  (NOLOCK) ON SAQSCO.PAR_SERVICE_ID = SAQTSE.PAR_SERVICE_ID AND SAQTSE.SERVICE_ID = SAQSCO.SERVICE_ID AND SAQSCO.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID  AND SAQSCO.QTEREV_RECORD_ID = SAQTSE.QTEREV_RECORD_ID and SAQSGB.GREENBOOK_RECORD_ID = SAQSCO.GREENBOOK_RECORD_ID

					JOIN SAQSGE ON SAQSGE.SERVICE_ID = SAQSCO.PAR_SERVICE_ID AND SAQSCO.QUOTE_RECORD_ID = SAQSGE.QUOTE_RECORD_ID AND SAQSCO.QTEREV_RECORD_ID = SAQSGE.QTEREV_RECORD_ID AND SAQSGB.GREENBOOK_RECORD_ID = SAQSGE.GREENBOOK_RECORD_ID
					
					WHERE SAQTSE.QUOTE_RECORD_ID = '{QuoteRecordId}'  AND SAQTSE.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQTSE.PAR_SERVICE_ID = '{ServiceId}'  AND ISNULL(SAQSGE.CONFIGURATION_STATUS,'') = 'COMPLETE' AND SAQSCO.GREENBOOK not in (SELECT GREENBOOK FROM SAQSGE M WHERE M.QUOTE_RECORD_ID = '{QuoteRecordId}' AND M.QTEREV_RECORD_ID = '{RevisionRecordId}' AND M.SERVICE_ID = SAQTSE.SERVICE_ID AND PAR_SERVICE_ID = '{ServiceId}') ) IQ""".format(UserId=self.user_id, QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id) 
				
				Sql.RunQuery(qtqsge_query_anc)
				self._update_entitlement_values('Z0046','SAQSGE')
				# get_ancillary_equp = Sql.GetFirst("select count(CpqTableEntryId) as cnt from SAQSCE WHERE QUOTE_RECORD_ID = '{}'  AND QTEREV_RECORD_ID = '{}' AND PAR_SERVICE_ID ='{}' {}".format(self.contract_quote_record_id, self.contract_quote_revision_record_id, self.service_id, addtional_where))
				# if get_ancillary_equp:
				# 	#if get_ancillary_equp.cnt == 0: 
				qtqsce_anc_query="""
					INSERT SAQSCE
					(KB_VERSION,ENTITLEMENT_XML,CONFIGURATION_STATUS,PAR_SERVICE_ID,PAR_SERVICE_RECORD_ID,PAR_SERVICE_DESCRIPTION,EQUIPMENT_ID,EQUIPMENT_RECORD_ID,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_RECORD_ID,QTEREV_ID,QTESRVCOB_RECORD_ID,QTESRVENT_RECORD_ID,SERIAL_NO,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,CPS_CONFIGURATION_ID,CPS_MATCH_ID,GREENBOOK,GREENBOOK_RECORD_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,QUOTE_SERVICE_COVERED_OBJ_ENTITLEMENTS_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED) 
					SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_COVERED_OBJ_ENTITLEMENTS_RECORD_ID, {UserId} as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM (
					SELECT 
					SAQTSE.KB_VERSION,SAQTSE.ENTITLEMENT_XML,SAQTSE.CONFIGURATION_STATUS,SAQTSE.PAR_SERVICE_ID,SAQTSE.PAR_SERVICE_RECORD_ID,SAQTSE.PAR_SERVICE_DESCRIPTION,SAQSCO.EQUIPMENT_ID,SAQSCO.EQUIPMENT_RECORD_ID,SAQTSE.QUOTE_ID,SAQTSE.QUOTE_RECORD_ID,SAQTSE.QTEREV_RECORD_ID,SAQTSE.QTEREV_ID,SAQSCO.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID as QTESRVCOB_RECORD_ID,SAQTSE.QUOTE_SERVICE_ENTITLEMENT_RECORD_ID as QTESRVENT_RECORD_ID,SAQSCO.SERIAL_NO,SAQTSE.SERVICE_DESCRIPTION,SAQTSE.SERVICE_ID,SAQTSE.SERVICE_RECORD_ID,SAQTSE.CPS_CONFIGURATION_ID,SAQTSE.CPS_MATCH_ID,SAQSCO.GREENBOOK,SAQSCO.GREENBOOK_RECORD_ID,SAQSCO.FABLOCATION_ID,SAQSCO.FABLOCATION_NAME,SAQSCO.FABLOCATION_RECORD_ID,SAQTSE.SALESORG_ID,SAQTSE.SALESORG_NAME,SAQTSE.SALESORG_RECORD_ID FROM
					SAQTSE (NOLOCK)
					JOIN SAQSCO (NOLOCK) ON SAQSCO.PAR_SERVICE_ID = SAQTSE.PAR_SERVICE_ID AND SAQSCO.SERVICE_ID = SAQTSE.SERVICE_ID AND SAQSCO.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID  AND SAQSCO.QTEREV_RECORD_ID = SAQTSE.QTEREV_RECORD_ID 
					
					JOIN SAQSCE ON SAQTSE.PAR_SERVICE_ID = SAQSCE.SERVICE_ID AND SAQSCO.QUOTE_RECORD_ID = SAQSCE.QUOTE_RECORD_ID AND SAQSCO.QTEREV_RECORD_ID = SAQSCE.QTEREV_RECORD_ID  AND SAQSCO.EQUIPMENT_ID = SAQSCE.EQUIPMENT_ID

					WHERE SAQTSE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND ISNULL(SAQSCE.CONFIGURATION_STATUS,'') = 'COMPLETE' AND SAQTSE.QTEREV_RECORD_ID = '{revision_rec_id}' AND SAQTSE.PAR_SERVICE_ID = '{par_service_id}' AND SAQSCO.EQUIPMENT_ID not in (SELECT EQUIPMENT_ID FROM SAQSCE (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}'   AND QTEREV_RECORD_ID = '{revision_rec_id}' AND SERVICE_ID = SAQTSE.SERVICE_ID AND PAR_SERVICE_ID = '{par_service_id}')) IQ""".format(UserId=self.user_id, QuoteRecordId=self.contract_quote_record_id, ServiceId=self.ancillary_obj, revision_rec_id = self.contract_quote_revision_record_id,par_service_id = self.service_id)
				
				Sql.RunQuery(qtqsce_anc_query)
				self._update_entitlement_values('Z0046','SAQSCE')
				# Sql.RunQuery("""UPDATE SAQSCE
				# 				SET
				# 				ENTITLEMENT_GROUP_ID = OQ.RowNo
				# 				FROM SAQSCE (NOLOCK)
				# 				INNER JOIN (
				# 					SELECT *, ROW_NUMBER()OVER(ORDER BY IQ.QUOTE_RECORD_ID) AS RowNo  FROM (
				# 					SELECT DISTINCT SRC.QUOTE_RECORD_ID,SRC.QTEREV_RECORD_ID, SRC.SERVICE_ID, SRC.ENTITLEMENT_XML
				# 					FROM SAQSCE (NOLOCK) SRC
				# 					JOIN MAMTRL ON MAMTRL.SAP_PART_NUMBER = SRC.SERVICE_ID AND MAMTRL.SERVICE_TYPE = 'NON TOOL BASED'
				# 					WHERE SRC.QUOTE_RECORD_ID = '{QuoteRecordId}'   AND SRC.QTEREV_RECORD_ID = '{revision_rec_id}' AND SRC.PAR_SERVICE_ID = '{service_id}' )AS IQ
				# 				)AS OQ
				# 				ON OQ.QUOTE_RECORD_ID = SAQSCE.QUOTE_RECORD_ID AND OQ.SERVICE_ID = SAQSCE.SERVICE_ID AND OQ.ENTITLEMENT_XML = SAQSCE.ENTITLEMENT_XML AND OQ.QTEREV_RECORD_ID = SAQSCE.QTEREV_RECORD_ID""".format(QuoteRecordId=self.contract_quote_record_id , revision_rec_id = self.contract_quote_revision_record_id ,service_id = self.service_id ))
				# Duplicate records removed from assembly level entitlement in offering - Start
				Sql.RunQuery("""DELETE FROM SAQSAE  WHERE QUOTE_RECORD_ID = '{}'  AND QTEREV_RECORD_ID = '{}' AND PAR_SERVICE_ID ='{}' {}""".format(self.contract_quote_record_id, self.contract_quote_revision_record_id, self.service_id, addtional_where))
				# Duplicate records removed from assembly level entitlement in offering - End
				saqsae_insert = """INSERT SAQSAE (KB_VERSION,EQUIPMENT_ID,EQUIPMENT_RECORD_ID,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_RECORD_ID,QTEREV_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,CPS_CONFIGURATION_ID,CPS_MATCH_ID,GREENBOOK,GREENBOOK_RECORD_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,ASSEMBLY_DESCRIPTION,ASSEMBLY_ID,ASSEMBLY_RECORD_ID,QTESRVCOA_RECORD_ID,PAR_SERVICE_ID,PAR_SERVICE_RECORD_ID,PAR_SERVICE_DESCRIPTION,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,ENTITLEMENT_XML,CONFIGURATION_STATUS,QTESRVCOE_RECORD_ID,QUOTE_SERVICE_COV_OBJ_ASS_ENT_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED) SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_COV_OBJ_ASS_ENT_RECORD_ID, {UserId} as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM(SELECT IQ.*,M.ENTITLEMENT_XML,M.CONFIGURATION_STATUS,M.QUOTE_SERVICE_COVERED_OBJ_ENTITLEMENTS_RECORD_ID as QTESRVCOE_RECORD_ID FROM ( SELECT DISTINCT SAQTSE.KB_VERSION,SAQSCA.EQUIPMENT_ID,SAQSCA.EQUIPMENT_RECORD_ID,SAQTSE.QUOTE_ID,SAQTSE.QUOTE_RECORD_ID,SAQTSE.QTEREV_RECORD_ID,SAQTSE.QTEREV_ID,SAQTSE.SERVICE_DESCRIPTION,SAQTSE.SERVICE_ID,SAQTSE.SERVICE_RECORD_ID,SAQTSE.CPS_CONFIGURATION_ID,SAQTSE.CPS_MATCH_ID,SAQSCA.GREENBOOK,SAQSCA.GREENBOOK_RECORD_ID,SAQSCA.FABLOCATION_ID,SAQSCA.FABLOCATION_NAME,SAQSCA.FABLOCATION_RECORD_ID,SAQSCA.ASSEMBLY_DESCRIPTION,SAQSCA.ASSEMBLY_ID,SAQSCA.ASSEMBLY_RECORD_ID,SAQSCA.QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID as QTESRVCOA_RECORD_ID,SAQSCA.PAR_SERVICE_ID,SAQSCA.PAR_SERVICE_RECORD_ID,SAQSCA.PAR_SERVICE_DESCRIPTION ,SAQTSE.SALESORG_ID,SAQTSE.SALESORG_NAME,SAQTSE.SALESORG_RECORD_ID FROM SAQTSE (NOLOCK) JOIN (SELECT * FROM SAQSCA (NOLOCK) WHERE SAQSCA.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCA.QTEREV_RECORD_ID = '{revision_rec_id}' AND SAQSCA.PAR_SERVICE_ID = '{par_service_id}' ) SAQSCA ON SAQTSE.QUOTE_RECORD_ID = SAQSCA.QUOTE_RECORD_ID AND SAQTSE.QTEREV_RECORD_ID = SAQSCA.QTEREV_RECORD_ID  AND SAQTSE.PAR_SERVICE_ID = SAQSCA.PAR_SERVICE_ID AND SAQTSE.SERVICE_ID = SAQSCA.SERVICE_ID JOIN SAQSAE ON SAQSAE.SERVICE_ID = SAQSCA.PAR_SERVICE_ID AND SAQSCA.QUOTE_RECORD_ID = SAQSAE.QUOTE_RECORD_ID AND SAQSCA.QTEREV_RECORD_ID = SAQSAE.QTEREV_RECORD_ID AND SAQSAE.EQUIPMENT_ID = SAQSCA.EQUIPMENT_ID  WHERE  SAQTSE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQTSE.QTEREV_RECORD_ID = '{revision_rec_id}' AND SAQSCA.PAR_SERVICE_ID = '{par_service_id}' AND ISNULL(SAQSAE.CONFIGURATION_STATUS,'') = 'COMPLETE' ) IQ JOIN SAQSCE (NOLOCK) M ON M.SERVICE_RECORD_ID = IQ.SERVICE_RECORD_ID AND M.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND M.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND M.EQUIPMENT_ID = IQ.EQUIPMENT_ID AND M.PAR_SERVICE_ID = IQ.PAR_SERVICE_ID )IQ""".format(UserId=self.user_id, QuoteRecordId=self.contract_quote_record_id, par_service_id=self.service_id, revision_rec_id = self.contract_quote_revision_record_id)				
				Sql.RunQuery(saqsae_insert)

		except Exception as e:
			Log.Info("error on ancillary--"+str(e)+'--'+str(str(sys.exc_info()[-1].tb_lineno)))

	def _delete_entitlement_tables(self):
		if self.tablename == "SAQTSE": 
			delete_obj_list = ["SAQTSE","SAQSGE","SAQSCE","SAQSAE"]
		# elif self.tablename == "SAQSFE":
		# 	delete_obj_list = ["SAQSFE","SAQSGE","SAQSCE","SAQSAE"]
		elif self.tablename == "SAQSGE":
			delete_obj_list = ["SAQSGE","SAQSCE","SAQSAE"] 
		elif self.tablename == "SAQSCE":
			delete_obj_list = ["SAQSCE","SAQSAE"] 
		elif self.tablename == "SAQSAE":
			delete_obj_list = ["SAQSAE"]
		
		ancillary_where = re.sub(r'AND SERVICE_ID\s*\=\s*\'[^>]*?\'', '', self.where_string )
		for obj in delete_obj_list:
			Sql.RunQuery("DELETE FROM {obj} WHERE {where} AND PAR_SERVICE_ID IN (SELECT SERVICE_ID FROM {obj}  WHERE {par_where} AND CONFIGURATION_STATUS ='INCOMPLETE') AND SERVICE_ID NOT IN (SELECT ADNPRD_ID FROM SAQSAO WHERE QUOTE_RECORD_ID='{quote_rec_id}' and SERVICE_ID = '{service_id}' AND QTEREV_RECORD_ID = '{revision_rec_id}' )".format(obj = obj, where=  ancillary_where, par_where = self.where_string, quote_rec_id=self.contract_quote_record_id,revision_rec_id = self.contract_quote_revision_record_id, service_id = self.service_id ))
		
	def _delete_operation(self):
		self._set_quote_service_entitlement_type()
		delete_obj_list = []

		if self.tablename == "SAQTSE": 
			delete_obj_list = ["SAQTSV","SAQSFB","SAQSGB","SAQSCO","SAQSCA","SAQTSE","SAQSGE","SAQSCE","SAQSAE","SAQICO","SAQRIT","SAQRIO","SAQRIS"]
		# elif self.tablename == "SAQSFE":
		# 	delete_obj_list = ["SAQSFB","SAQSGB","SAQSCO","SAQSCA","SAQSFE","SAQSGE","SAQSCE","SAQSAE","SAQICO","SAQRIT","SAQRIO"]
		elif self.tablename == "SAQSGE":
			delete_obj_list = ["SAQSGB","SAQSCO","SAQSCA","SAQSGE","SAQSCE","SAQSAE","SAQICO","SAQRIT","SAQRIO","SAQRIS"] 
		elif self.tablename == "SAQSCE":
			delete_obj_list = ["SAQSCO","SAQSCA","SAQSCE","SAQSAE","SAQICO","SAQRIT","SAQRIO","SAQRIS"] 
		elif self.tablename == "SAQSAE":
			delete_obj_list = ["SAQSCA","SAQSAE","SAQICO","SAQRIT","SAQRIO","SAQRIS"]
		
		# if self.action_type == "DELETE_ENT_EQUIPMENT":
		# 	delete_obj_list = ["SAQTSE","SAQSFE","SAQSGE","SAQSCE","SAQSAE"]
		addtional_where = ""
		if self.fab:
			addtional_where = " AND FABLOCATION_ID = '{}' ".format(self.fab)
		if self.greenbook:
			addtional_where += " AND GREENBOOK = '{}'".format(self.greenbook)
		if self.equipment_id:
			addtional_where += " AND EQUIPMENT_ID = '{}'".format(self.equipment_id)
		if self.assembly:
			addtional_where += " AND ASSEMBLY_ID = '{}'".format(self.assembly)
		if self.ancillary_obj in ('Z0101','Z0100'):
			delete_obj_list.append('SAQRIP')
		for obj in delete_obj_list:
			#Sql.RunQuery("DELETE FROM {} WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID ='{}' AND PAR_SERVICE_ID = '{}'".format(obj, self.contract_quote_record_id, self.contract_quote_revision_record_id ,self.ancillary_obj, self.service_id))
			
			ancillary_where = re.sub("SERVICE_ID","PAR_SERVICE_ID",self.where_string)
			if obj in ('SAQICO','SAQRIT','SAQRIO','SAQRIS'):
				ancillary_where = re.sub(r'AND SERVICE_ID\s*\=\s*\'[^>]*?\'', '', self.where_string )
			if obj == 'SAQRIO':
				ancillary_where = re.sub(r'AND FABLOCATION_ID\s*\=\s*\'[^>]*?\'', '', ancillary_where )
			# if obj in ('SAQICO','SAQRIT','SAQRIO'):
			# 	ancillary_where = re.sub(r'AND SERVICE_ID\s*\=\s*\'[^>]*?\'', '', self.where_string )
			if obj == 'SAQRIT' and 'EQUIPMENT_ID' in ancillary_where:
				if self.quote_service_entitlement_type != "OFFERING + EQUIPMENT":
					ancillary_where = re.sub(r'AND EQUIPMENT_ID\s*\=\s*\'[^>]*?\'', '', ancillary_where )
				else:
					ancillary_where = re.sub('EQUIPMENT_ID', 'OBJECT_ID', ancillary_where )
			Sql.RunQuery("DELETE FROM {} WHERE {} AND SERVICE_ID = '{}' AND SERVICE_ID NOT IN (SELECT ADNPRD_ID FROM SAQSAO WHERE QUOTE_RECORD_ID='{}' and SERVICE_ID = '{}' AND QTEREV_RECORD_ID = '{}' )".format(obj,ancillary_where,self.ancillary_obj, self.contract_quote_record_id, self.service_id,self.contract_quote_revision_record_id ))
		
		##deleting higher table records based on below level 
		if self.tablename != "SAQTSE":
			obj_list = ["SAQSCA","SAQSCO","SAQSGB"]
			for rec in obj_list:
				if rec == "SAQSCA":
					addtional_where = re.sub(r'AND ASSEMBLY_ID\s*\=\s*\'[^>]*?\'', '',addtional_where )
				elif rec == "SAQSCO":
					addtional_where = re.sub(r'AND EQUIPMENT_ID\s*\=\s*\'[^>]*?\'', '',addtional_where )
					addtional_where = re.sub(r'AND ASSEMBLY_ID\s*\=\s*\'[^>]*?\'', '',addtional_where )
				elif rec == "SAQSGB":
					addtional_where =''
				get_count = Sql.GetFirst("select count(CpqTableEntryId) as cnt from {} (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID ='{}' AND PAR_SERVICE_ID = '{}' {}".format(rec,self.contract_quote_record_id, self.contract_quote_revision_record_id ,self.ancillary_obj, self.service_id,addtional_where ))
				if rec == "SAQSCA" and get_count.cnt == 0:
					for del_obj in ['SAQSCO','SAQSCE']:
						Sql.RunQuery("DELETE FROM {} WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID ='{}' AND PAR_SERVICE_ID = '{}' {}".format(del_obj,self.contract_quote_record_id, self.contract_quote_revision_record_id ,self.ancillary_obj, self.service_id,addtional_where ))
				elif rec == "SAQSCO" and get_count.cnt == 0:
					
					for del_obj in ['SAQSGB','SAQSGE']:
						Sql.RunQuery("DELETE FROM {} WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID ='{}' AND PAR_SERVICE_ID = '{}' {}".format(del_obj,self.contract_quote_record_id, self.contract_quote_revision_record_id ,self.ancillary_obj, self.service_id,addtional_where ))
				elif rec == "SAQSGB" and get_count.cnt == 0:
					for del_obj in ['SAQTSE','SAQTSV']:
						Sql.RunQuery("DELETE FROM {} WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID ='{}' AND PAR_SERVICE_ID = '{}' ".format(del_obj,self.contract_quote_record_id, self.contract_quote_revision_record_id ,self.ancillary_obj, self.service_id ))

	def _set_quote_service_entitlement_type(self):
		self.quote_service_entitlement_type = ""
		##chk ancillary offering
		
		if self.tablename != 'SAQTSE' :			
			where_str = self.where_string.replace('SRC.','').replace('WHERE','')
		else:
			where_str = " QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' and SERVICE_ID = '{ServiceId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.ancillary_obj)
		service_entitlement_obj = Sql.GetFirst("""SELECT SERVICE_ID, ENTITLEMENT_XML FROM  {obj_name} (NOLOCK) WHERE {where_str}""".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id, obj_name = self.tablename, where_str = where_str))
		if service_entitlement_obj:
			quote_item_tag_pattern = re.compile(r'(<QUOTE_ITEM_ENTITLEMENT>[\w\W]*?</QUOTE_ITEM_ENTITLEMENT>)')
			entitlement_id_tag_pattern = re.compile(r'<ENTITLEMENT_ID>AGS_'+str(self.ancillary_obj)+'_PQB_QTITST</ENTITLEMENT_ID>')
			entitlement_display_value_tag_pattern = re.compile(r'<ENTITLEMENT_DISPLAY_VALUE>([^>]*?)</ENTITLEMENT_DISPLAY_VALUE>')
			for quote_item_tag in re.finditer(quote_item_tag_pattern, service_entitlement_obj.ENTITLEMENT_XML):
				quote_item_tag_content = quote_item_tag.group(1)
				entitlement_id_tag_match = re.findall(entitlement_id_tag_pattern,quote_item_tag_content)				
				if entitlement_id_tag_match:
					entitlement_display_value_tag_match = re.findall(entitlement_display_value_tag_pattern,quote_item_tag_content)
					if entitlement_display_value_tag_match:
						self.quote_service_entitlement_type = entitlement_display_value_tag_match[0].upper()
						break
				else:
					continue
			
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
try:
	attributeList = eval(Param.attributeList)
except:
	attributeList = ""
auto_ancillary_obj = AncillaryProductOperation()
auto_ancillary_obj._do_opertion()
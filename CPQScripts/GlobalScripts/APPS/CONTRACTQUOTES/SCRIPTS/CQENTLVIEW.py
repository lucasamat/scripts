# =========================================================================================================================================
#   __script_name : CQENTLVIEW.PY
#   __script_description :
#   __primary_author__ :Dhurga,Selvi
#   __create_date : 21/09/2021
#   ï¿½ BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct

import System.Net
from datetime import datetime
from SYDATABASE import SQL
import re
Sql = SQL()
userId = str(User.Id)
#userName = str(User.UserName)

class EntitlementView():
	def __init__(self):
		self.treeparam = TreeParam
		self.treeparentparam = TreeParentParam
		self.treesuperparentparam = TreeSuperParentParam
		self.treetopsuperparentparam = TreeTopSuperParentParam
		self.treesupertopparentparam = TreeSuperTopParentParam
		##TreeParentLevel4 added for addon product
		self.treetopsupertopparentparam = TreeTopSuperTopParentParam
		self.contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
		self.quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
	
	def entitlement_view(
		self,
		RECORD_ID,
		ObjectName,
		EntitlementType
	):
		quoteid = self.contract_quote_record_id
		cpsConfigID = get_last_secid = get_tooltip = get_conflict_message = get_conflict_message_id = ''
		msg_txt = insertservice  = sec_str_boot = sec_bnr = imgstr = dbl_clk_function = getprevdicts = sec_str_cf = sec_str1 = getTlab = getquote_sales_val = ent_temp = ""
		tablistnew =  []
		TableObj = ""
		ChangedList = totaldisallowlist = section_not_list = []
		Trace.Write("EntitlementType"+str(EntitlementType))

		#Trace.Write('TreeSuperParentParam'+'--'+str(self.treesupertopparentparam)+'--'+str(self.treetopsuperparentparam))
		objname_ent = "" ##add on product entitilement obj declare
		if self.treesuperparentparam == "Product Offerings":		
			ProductPartnumber = self.treeparam
		elif self.treetopsuperparentparam == "Product Offerings":
			### add on product entitilement starts
			if str(self.treeparentparam).upper() == "ADD-ON PRODUCTS":
				ProductPartnumber = self.treeparam
				objname_ent = 'SAQSAO'	
				### add on product entitilement starts
			else:	
				ProductPartnumber = self.treeparentparam
				###receiving equp entitilement starts
				if self.treesuperparentparam == 'Complementary Products' and self.treeparam == 'Receiving Equipment':
					objname_ent = 'SAQSCO'
				###receiving equp entitilement ends
		elif self.treesupertopparentparam == "Product Offerings":
			### add on product entitilement starts
			if str(self.treeparentparam).upper() == "ADD-ON PRODUCTS":
				ProductPartnumber = self.treeparam
				objname_ent = 'SAQSAO'	
				### add on product entitilement starts
			else:	
				ProductPartnumber = self.treesuperparentparam
				if (self.treeparentparam == 'Receiving Equipment' and self.treetopsuperparentparam == 'Complementary Products'):
					self.treeparentparam = ProductPartnumber

		elif self.treeparentparam == "Quote Items":
			if "-" in self.treeparam:
				self.treeparam = self.treeparam.split("-")[1].strip()
			GetItem = Sql.GetFirst("select * from SAQICO (NOLOCK) where QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '" + str(RECORD_ID) + "'")
			if GetItem is not None:
				ProductPartnumber = GetItem.SERVICE_ID
			else:
				ProductPartnumber = self.treeparam
		elif self.treesuperparentparam == "Quote Items":
			self.treeparentparam = self.treeparentparam.split("-")[1].strip()
			ProductPartnumber = self.treeparentparam
		elif self.treetopsuperparentparam == "Quote Items":
			##for Quote items for ADDON Product starts
			if " - ADDON" in str(self.treesuperparentparam):
				tree_temp = self.treesuperparentparam.split(" - ")
				try:
					if str(self.treesuperparentparam.split("-")[3]):
						self.treesuperparentparam = self.treesuperparentparam.split("-")[2].strip()	
					else:
						self.treesuperparentparam = self.treesuperparentparam.split("-")[1].strip()
				except:
					self.treesuperparentparam = self.treesuperparentparam.split("-")[1].strip()	
				##for Quote items for ADDON Product ends	
			else:
				self.treesuperparentparam = self.treesuperparentparam.split("-")[1].strip()
			ProductPartnumber = self.treesuperparentparam
		##addon product fab and greenbook level 
		elif (str(self.treesupertopparentparam).upper() == "COMPREHENSIVE SERVICES" and str(self.treesuperparentparam).upper() == "ADD-ON PRODUCTS"):		
			ProductPartnumber = self.treeparentparam	
		elif str(self.treesupertopparentparam).upper() == "COMPREHENSIVE SERVICES" and str(self.treetopsuperparentparam).upper() == "ADD-ON PRODUCTS":		
			ProductPartnumber = self.treesuperparentparam		
		##addon product fab and greenbook level 
		elif (self.treesuperparentparam in ('Receiving Equipment', 'Sending Equipment') and self.treesupertopparentparam == 'Complementary Products'):
			self.treesuperparentparam = ProductPartnumber = self.treetopsuperparentparam
			#Trace.Write('comes1'+str(ProductPartnumber))
		#A055S000P01-9226 start
		getslaes_value  = Sql.GetFirst("SELECT SALESORG_ID FROM SAQTRV WHERE QUOTE_RECORD_ID = '"+str(quoteid)+"'")
		if getslaes_value:
			getquote_sales_val = getslaes_value.SALESORG_ID
		#Trace.Write(str(EntitlementType)+'----getquote_sales_val---2421----'+str(getquote_sales_val))
		get_il_sales = Sql.GetList("select SALESORG_ID from SASORG where country = 'IL'")
		get_il_sales_list = [val.SALESORG_ID for val in get_il_sales]
		if 'Z0101' in TreeParam and TreeParentParam == "Quote Items":
			EntitlementType = ""
			TableObj = Sql.GetFirst("select * from SAQTSE (NOLOCK) where QUOTE_RECORD_ID = '" + str(self.contract_quote_record_id) + "' AND QTEREV_RECORD_ID = '" + str(self.quote_revision_record_id) + "' AND SERVICE_ID = 'Z0101'")
			ObjectName = "SAQTSE"
			where = "QUOTE_RECORD_ID = '" + str(self.contract_quote_record_id) + "' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"' AND SERVICE_ID = 'Z0101'"

		#A055S000P01-9226 end
		if EntitlementType == "EQUIPMENT":
			### add on product entitilement starts		
			if str(self.treeparentparam).upper() == "ADD-ON PRODUCTS" and objname_ent == 'SAQSAO':
				#Trace.Write('126----126----')
				TableObj = Sql.GetFirst("select * from SAQTSE (NOLOCK) where QTESRV_RECORD_ID = '" + str(RECORD_ID) + "'")
				ParentObj = Sql.GetFirst("select * from SAQSAO (NOLOCK) where QUOTE_SERVICE_ADD_ON_PRODUCT_RECORD_ID = '" + str(RECORD_ID) + "'")
				if ParentObj:
					QUOTE_ID = ParentObj.QUOTE_ID
					QUOTE_NAME = ParentObj.QUOTE_NAME
					QUOTE_RECORD_ID = ParentObj.QUOTE_RECORD_ID
					QUOTE_SERVICE_RECORD_ID = ParentObj.QUOTE_SERVICE_ADD_ON_PRODUCT_RECORD_ID
					SERVICE_RECORD_ID = ParentObj.SERVICE_RECORD_ID
					SERVICE_ID = ParentObj.SERVICE_ID
					SERVICE_DESCRIPTION = ParentObj.SERVICE_DESCRIPTION
					SALESORG_RECORD_ID = ParentObj.SALESORG_RECORD_ID
					SALESORG_ID = ParentObj.SALESORG_ID
					SALESORG_NAME = ParentObj.SALESORG_NAME
					QTEREV_RECORD_ID = ParentObj.QTEREV_RECORD_ID

				where = "QUOTE_RECORD_ID = '" + str(QUOTE_RECORD_ID) + "' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"' AND QTESRV_RECORD_ID = '" + str(RECORD_ID) + "'"
				
				##add on product entitilement ends
			###receiving equp entitilement starts
			elif str(self.treeparam).upper() == "RECEIVING EQUIPMENT" and objname_ent == 'SAQSCO':
				#Trace.Write('receiving----'+str(quoteid)+'---'+str(ProductPartnumber))
				TableObj = Sql.GetFirst("select * from SAQTSE (NOLOCK) where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' and SERVICE_ID = '{}' ".format(quoteid,self.quote_revision_record_id,ProductPartnumber))
				ParentObj = Sql.GetFirst("select * from SAQTSV (NOLOCK) where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' and SERVICE_ID = '{}' ".format(quoteid,self.quote_revision_record_id,ProductPartnumber))
				if ParentObj:
					QUOTE_ID = ParentObj.QUOTE_ID
					QUOTE_NAME = ParentObj.QUOTE_NAME
					QUOTE_RECORD_ID = ParentObj.QUOTE_RECORD_ID
					RECORD_ID = QUOTE_SERVICE_RECORD_ID = ParentObj.QUOTE_SERVICE_RECORD_ID
					SERVICE_RECORD_ID = ParentObj.SERVICE_RECORD_ID
					SERVICE_ID = ParentObj.SERVICE_ID
					SERVICE_DESCRIPTION = ParentObj.SERVICE_DESCRIPTION
					SALESORG_RECORD_ID = ParentObj.SALESORG_RECORD_ID
					SALESORG_ID = ParentObj.SALESORG_ID
					SALESORG_NAME = ParentObj.SALESORG_NAME
					QTEREV_RECORD_ID = ParentObj.QTEREV_RECORD_ID

				where = "QUOTE_RECORD_ID = '" + str(QUOTE_RECORD_ID) + "' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"' AND QTESRV_RECORD_ID = '" + str(RECORD_ID) + "'"
					
			###receiving equp entitilement ends
			else:
				TableObj = Sql.GetFirst("select * from SAQTSE (NOLOCK) where QTESRV_RECORD_ID = '" + str(RECORD_ID) + "'")
				ParentObj = Sql.GetFirst("select * from SAQTSV (NOLOCK) where QUOTE_SERVICE_RECORD_ID = '" + str(RECORD_ID) + "'")
				if ParentObj:
					QUOTE_ID = ParentObj.QUOTE_ID
					QUOTE_NAME = ParentObj.QUOTE_NAME
					QUOTE_RECORD_ID = ParentObj.QUOTE_RECORD_ID
					QUOTE_SERVICE_RECORD_ID = ParentObj.QUOTE_SERVICE_RECORD_ID
					SERVICE_RECORD_ID = ParentObj.SERVICE_RECORD_ID
					SERVICE_ID = ParentObj.SERVICE_ID
					SERVICE_DESCRIPTION = ParentObj.SERVICE_DESCRIPTION
					SALESORG_RECORD_ID = ParentObj.SALESORG_RECORD_ID
					SALESORG_ID = ParentObj.SALESORG_ID
					SALESORG_NAME = ParentObj.SALESORG_NAME
					QTEREV_RECORD_ID = ParentObj.QTEREV_RECORD_ID
				where = "QUOTE_RECORD_ID = '" + str(QUOTE_RECORD_ID) + "' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"' AND QTESRV_RECORD_ID = '" + str(RECORD_ID) + "'"
						
		elif EntitlementType == "TOOLS":
			TableObj = Sql.GetFirst("select * from SAQSCE (NOLOCK) where QTESRVCOB_RECORD_ID = '" + str(RECORD_ID) + "'")
			ObjectName = "SAQSCE"
			where = "QUOTE_RECORD_ID = '" + str(quoteid) + "' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"' AND QTESRVCOB_RECORD_ID = '" + str(RECORD_ID) + "'"
					

		elif EntitlementType == "ITEMGREENBOOK":
			ObjectName = "SAQSGE"
			#service = self.treesuperparentparam
			service = self.treeparentparam
			# TableObj = Sql.GetFirst("select * from SAQSGE (NOLOCK) where QUOTE_RECORD_ID = '" + str(quoteid) + "' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"' AND SERVICE_ID = '"+str(service)+"' AND GREENBOOK = '" + str(self.treeparam) + "' AND FABLOCATION_ID = '"+ str(self.treeparentparam) + "'")		
			# where = "QUOTE_RECORD_ID = '" + str(quoteid) + "' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"' AND SERVICE_ID = '"+str(service)+"' AND GREENBOOK = '" + str(self.treeparam) + "' AND FABLOCATION_ID = '"+ str(self.treeparentparam) + "'"
			TableObj = Sql.GetFirst("select * from SAQSGE (NOLOCK) where QUOTE_RECORD_ID = '" + str(quoteid) + "' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"' AND SERVICE_ID = '"+str(service)+"' AND GREENBOOK = '" + str(self.treeparam) + "' ")		
			where = "QUOTE_RECORD_ID = '" + str(quoteid) + "' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"' AND SERVICE_ID = '"+str(service)+"' AND GREENBOOK = '" + str(self.treeparam) + "' "
					
		elif EntitlementType == "ITEMSPARE":
			#TableObj = Sql.GetFirst("select SAQIEN.* from SAQIEN (NOLOCK) JOIN QTQITM ON QTQITM.QUOTE_RECORD_ID = SAQIEN.QUOTE_RECORD_ID where QTQITM.QUOTE_ITEM_RECORD_ID = '" + str(RECORD_ID) + "'")
			#TableObj = Sql.GetFirst("select SAQIPE.* from SAQIPE (NOLOCK) JOIN QTQITM ON QTQITM.QUOTE_RECORD_ID = SAQIPE.QUOTE_RECORD_ID AND QTQITM.SERVICE_ID =SAQIPE.SERVICE_ID where SAQIPE.QUOTE_RECORD_ID = '" + str(quoteid) + "'")	
			TableObj = Sql.GetFirst("select SAQIPE.* from SAQIPE (NOLOCK) JOIN SAQIFP ON SAQIFP.QUOTE_RECORD_ID = SAQIPE.QUOTE_RECORD_ID AND SAQIFP.QTEREV_RECORD_ID  = SAQIPE.QTEREV_RECORD_ID  where SAQIFP.QUOTE_ITEM_FORECAST_PART_RECORD_ID  = '" + str(RECORD_ID) + "'")		
			#where = "QTQITM.QUOTE_ITEM_RECORD_ID = '" + str(RECORD_ID) + "'"
			#join = 'JOIN QTQITM ON QTQITM.QUOTE_RECORD_ID = SAQIEN.QUOTE_RECORD_ID'
			where = "QUOTE_RECORD_ID = '" + str(quoteid) + "' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"' AND SERVICE_ID = '" + str(self.treeparam) + "'"
			# join = 'JOIN SAQIFP ON SAQITM.QUOTE_RECORD_ID = SAQIPE.QUOTE_RECORD_ID AND SAQITM.QTEREV_RECORD_ID  = SAQIPE.QTEREV_RECORD_ID  AND SAQIFP.SERVICE_ID =SAQIPE.SERVICE_ID'
			join = ''
		elif EntitlementType == "ITEMS":	
			TableObj = Sql.GetFirst("select * from SAQIEN (NOLOCK) where QTEITMCOB_RECORD_ID = '" + str(RECORD_ID) + "'")
			where = "QTEITMCOB_RECORD_ID = '" + str(RECORD_ID) + "'"
			
		# elif EntitlementType == "FABLOCATION":			
		# 	TableObj = Sql.GetFirst("select * from SAQSFE (NOLOCK) where  QUOTE_RECORD_ID = '" + str(quoteid) + "' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"' AND SERVICE_ID = '" + str(self.treeparentparam) + "' AND FABLOCATION_ID = '" + str(self.treeparam) + "'")
		# 	where = "QUOTE_RECORD_ID = '" + str(quoteid) + "' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"' AND SERVICE_ID = '" + str(self.treeparentparam) + "' AND FABLOCATION_ID ='"+str(self.treeparam)+"'"
					
		elif EntitlementType == "BUSINESSUNIT":
			#TableObj = Sql.GetFirst("select * from SAQSGE (NOLOCK) where QUOTE_RECORD_ID = '" + str(quoteid) + "' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"' AND SERVICE_ID = '" + str(self.treesuperparentparam) + "' AND FABLOCATION_ID = '" + str(self.treeparentparam) + "' AND GREENBOOK = '"+str(self.treeparam)+"'")
			greenbook_val = self.treeparam
			service_val = self.treeparentparam
			if self.treeparam == 'Add-On Products' and self.treesupertopparentparam == 'Product Offerings':
				greenbook_val = self.treeparentparam
				par_service_val = self.treesuperparentparam
				TableObj = Sql.GetFirst("select * from SAQSGE (NOLOCK) where QUOTE_RECORD_ID = '" + str(quoteid) + "' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"' AND QTESRVGBK_RECORD_ID = '" + str(RECORD_ID) + "' AND PAR_SERVICE_ID = '" + str(par_service_val) + "'  AND GREENBOOK = '"+str(greenbook_val)+"'")
				where = " QUOTE_RECORD_ID = '" + str(quoteid) + "' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"' AND QTESRVGBK_RECORD_ID = '" + str(RECORD_ID) + "' AND PAR_SERVICE_ID = '" + str(par_service_val) + "'  AND GREENBOOK = '"+str(greenbook_val)+"'"
				ProductPartnumber = TableObj.SERVICE_ID
			else:
				TableObj = Sql.GetFirst("select * from SAQSGE (NOLOCK) where QUOTE_RECORD_ID = '" + str(quoteid) + "' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"' AND SERVICE_ID = '" + str(service_val) + "'  AND GREENBOOK = '"+str(greenbook_val)+"'")
				where = "QUOTE_RECORD_ID = '" + str(quoteid) + "' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"' AND SERVICE_ID = '" + str(service_val) + "' AND GREENBOOK ='"+str(greenbook_val)+"'"
			if TableObj is not None:
				RECORD_ID = str(TableObj.SERVICE_RECORD_ID)
			#where = "QUOTE_RECORD_ID = '" + str(quoteid) + "' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"' AND SERVICE_ID = '" + str(self.treesuperparentparam) + "' AND GREENBOOK ='"+str(self.treeparam)+"' AND FABLOCATION_ID = '"+str(self.treeparentparam)+"'"
			#where = "QUOTE_RECORD_ID = '" + str(quoteid) + "' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"' AND SERVICE_ID = '" + str(service_val) + "' AND GREENBOOK ='"+str(greenbook_val)+"'"
			
		elif EntitlementType == "ASSEMBLY":
			# TableObj = Sql.GetFirst("select * from SAQSAE (NOLOCK) where QUOTE_RECORD_ID = '" + str(quoteid) + "' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"' AND SERVICE_ID = '" + str(self.treesuperparentparam) + "' AND FABLOCATION_ID = '" + str(self.treeparentparam) + "' AND GREENBOOK = '"+str(self.treeparam)+"' AND EQUIPMENT_ID = '"+str(EquipmentId)+"' AND ASSEMBLY_ID = '"+str(AssemblyId)+"' ")
			# where = "QUOTE_RECORD_ID = '" + str(quoteid) + "' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"' AND SERVICE_ID = '" + str(self.treesuperparentparam) + "' AND GREENBOOK ='"+str(self.treeparam)+"' AND FABLOCATION_ID = '"+str(self.treeparentparam)+"' AND EQUIPMENT_ID = '"+str(EquipmentId)+"' AND ASSEMBLY_ID = '"+str(AssemblyId)+"'"
			TableObj = Sql.GetFirst("select * from SAQSAE (NOLOCK) where QUOTE_RECORD_ID = '" + str(quoteid) + "' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"' AND SERVICE_ID = '" + str(self.treeparentparam) + "'  AND GREENBOOK = '"+str(self.treeparam)+"' AND EQUIPMENT_ID = '"+str(EquipmentId)+"' AND ASSEMBLY_ID = '"+str(AssemblyId)+"' ")
			where = "QUOTE_RECORD_ID = '" + str(quoteid) + "' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"' AND SERVICE_ID = '" + str(self.treeparentparam) + "' AND GREENBOOK ='"+str(self.treeparam)+"'  AND EQUIPMENT_ID = '"+str(EquipmentId)+"' AND ASSEMBLY_ID = '"+str(AssemblyId)+"'"
		#Trace.Write('Treeparam--'+str(self.treeparam))
		#Trace.Write('treeparentparam----'+str(self.treeparentparam))
		if self.treeparam == "Quote Items":
			quote_item_revision_rec_id = Product.GetGlobal('get_quote_item_service')
			Trace.Write('quote_item_revision_rec_id--'+str(quote_item_revision_rec_id))
			if quote_item_revision_rec_id:
				get_quite_item_service= Sql.GetFirst("select SERVICE_ID from SAQRIT where QUOTE_REVISION_CONTRACT_ITEM_ID ='"+str(quote_item_revision_rec_id)+"'")
				ProductPartnumber = get_quite_item_service.SERVICE_ID
				Trace.Write('ProductPartnumber-224-'+str(ProductPartnumber))
				TableObj = Sql.GetFirst("select * from SAQITE (NOLOCK) where QUOTE_RECORD_ID = '" + str(quoteid) + "' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"' AND SERVICE_ID = '" + str(ProductPartnumber) + "'AND QTEITM_RECORD_ID ='"+str(quote_item_revision_rec_id)+"' ")
				where = "QUOTE_RECORD_ID = '" + str(quoteid) + "' AND QTEREV_RECORD_ID = '"+str(self.quote_revision_record_id)+"' AND SERVICE_ID = '" + str(ProductPartnumber) + "' AND QTEITM_RECORD_ID ='"+str(quote_item_revision_rec_id)+"'"
				EntitlementType == "ITEM_ENTITLEMENT"
				ObjectName = "SAQITE"
		try:
			get_configuration_status = Sql.GetFirst("SELECT MATERIALCONFIG_TYPE FROM MAMTRL WHERE SAP_PART_NUMBER = '{}'".format(ProductPartnumber))
			if get_configuration_status:
				if get_configuration_status.MATERIALCONFIG_TYPE == 'SIMPLE MATERIAL' or ProductPartnumber == 'Z0101':
					EntitlementType = "NO_ENTITLEMENT"
		except:
			Trace.Write('Treeparam--'+str(self.treeparam))
		

		if EntitlementType != "NO_ENTITLEMENT":
			if TableObj is None and (EntitlementType == "EQUIPMENT"):
				Trace.Write('223----durga---')
				Request_URL = "https://cpservices-product-configuration.cfapps.us10.hana.ondemand.com/api/v2/configurations?autoCleanup=False"
				Fullresponse = ScriptExecutor.ExecuteGlobal("CQENTLNVAL", {'action':'GET_RESPONSE','partnumber':ProductPartnumber,'request_url':Request_URL,'request_type':"New"})
				#self.EntitlementRequest(ProductPartnumber,Request_URL,)
			else:		
				if TableObj :
					cpsConfigID = TableObj.CPS_CONFIGURATION_ID
				Request_URL = "https://cpservices-product-configuration.cfapps.us10.hana.ondemand.com/api/v2/configurations/"+str(cpsConfigID)
				Fullresponse = ScriptExecutor.ExecuteGlobal("CQENTLNVAL", {'action':'GET_RESPONSE','partnumber':ProductPartnumber,'request_url':Request_URL,'request_type':"Existing"})
				#self.EntitlementRequest(ProductPartnumber,Request_URL,"Existing")

			attributesdisallowedlst = []
			attributeReadonlylst = attributes_disallowed_list =  []
			attriburesrequired_list = []
			attributeEditlst = list_of_tabs = []
			attributevalues = {}
			attributedefaultvalue = []
			overallattributeslist_visible =[]
			dropdowndisallowlist = attr_tab_list_allow = attr_tab_list_disallow = total_tablist = []
			validation_dict = {}
			get_lastsection_val = attrcode = disable_edit = get_requiredicon = ""
			# where = ""
			Product.SetGlobal('Fullresponse_load',str(Fullresponse))
			for rootattribute, rootvalue in Fullresponse.items():
				if rootattribute == "conflicts":
					for conflict in rootvalue:
						Trace.Write('88---2191-'+str(conflict))
						for val,key in conflict.items():
							if str(val) == "explanation":
								Trace.Write(str(key)+'-2195---'+str(val))
								get_conflict_message = str(key)
								try:
									get_conflict_message_id = re.findall(r'\(ID\s*([^>]*?)\)', get_conflict_message)[0]
								except:
									get_conflict_message_id = ''
				if rootattribute == "rootItem":
					for Productattribute, Productvalue in rootvalue.items():
						if Productattribute == "characteristicGroups":
							for prdvalue in Productvalue:
								if prdvalue["visible"]:
									total_tablist.append(prdvalue["id"])
								if prdvalue["visible"] == "true":							
									attr_tab_list_allow.append(prdvalue["id"])
								if prdvalue["visible"] == "false":
									attr_tab_list_disallow.append(prdvalue["id"])
						if Productattribute == "characteristics":
							for prdvalue in Productvalue:
								if prdvalue["visible"] == "true":
									overallattributeslist_visible.append(prdvalue["id"])
								if prdvalue["visible"] == "false":
									attributesdisallowedlst.append(prdvalue["id"])
								if prdvalue["readOnly"] == "true":
									attributeReadonlylst.append(prdvalue["id"])
								if prdvalue["readOnly"] == "false":
									attributeEditlst.append(prdvalue["id"])
								if prdvalue["required"] == "true":
									attriburesrequired_list.append(prdvalue["id"])
								if prdvalue["possibleValues"]:
									for i in prdvalue["possibleValues"]:
										if i['selectable'] == 'false' and 'valueLow' in i.keys():
											dropdowndisallowlist.append(str(prdvalue["id"])+'_'+str(i['valueLow'])	)
										if i['selectable'] == 'true' and 'valueHigh' in i.keys():
											validation_dict[prdvalue["id"] ] = i['valueHigh']
										# else:
										# 	dropdownallowlist.append(str(prdvalue["id"])+'_'+str(i['valueLow'])	)
								for attribute in prdvalue["values"]:
									attributevalues[str(prdvalue["id"])] = attribute["value"]
									if attribute["author"] in ('Default','System'):
										attributedefaultvalue.append(prdvalue["id"])
			#Trace.Write('attributesdisallowedlst--'+str(attributesdisallowedlst))
			#Trace.Write('total_tablist--'+str(total_tablist))
			#Trace.Write('attr_tab_list_disallow--'+str(attr_tab_list_disallow))
			Trace.Write('attriburesrequired_list----'+str(attriburesrequired_list))
			#Trace.Write("validation_dict---"+str(validation_dict))

			product_obj = Sql.GetFirst("""SELECT 
										MAX(PDS.PRODUCT_ID) AS PRD_ID,PDS.SYSTEM_ID,PDS.PRODUCT_NAME 
									FROM PRODUCTS PDS 
									INNER JOIN PRODUCT_VERSIONS PRVS ON  PDS.PRODUCT_ID = PRVS.PRODUCT_ID 
									WHERE SYSTEM_ID ='{SystemId}' and PRVS.SAPKBVersion = '{kb_version}'
									GROUP BY PDS.SYSTEM_ID,PDS.UnitOfMeasure,PDS.CART_DESCRIPTION_BUILDER,PDS.PRODUCT_NAME""".format(SystemId = str(ProductPartnumber),kb_version = Fullresponse['kbKey']['version'] ))
			
			product_tabs_obj = Sql.GetList("""SELECT 
													TOP 1000 TAB_NAME,TAB_DEFN.SYSTEM_ID, TAB_RANK, TAB_PROD_ID, TAB_PRODUCTS.TAB_CODE
												FROM TAB_PRODUCTS
												JOIN TAB_DEFN ON TAB_DEFN.TAB_CODE = TAB_PRODUCTS.TAB_CODE
												WHERE TAB_PRODUCTS.PRODUCT_ID = {ProductId} and TAB_NAME not like '$%'
												ORDER BY TAB_PRODUCTS.RANK""".format(ProductId = product_obj.PRD_ID))
			
			product_attributes_obj = Sql.GetList("""SELECT TOP 1000 PAT_SCHEMA.STANDARD_ATTRIBUTE_CODE, 
														TAB_PRODUCTS.TAB_PROD_ID, TAB_PRODUCTS.TAB_CODE, ATTRIBUTE_DEFN.STANDARD_ATTRIBUTE_NAME,PRODUCT_ATTRIBUTES.LABEL AS LABEL, ATTRIBUTE_DEFN.SYSTEM_ID AS SYSTEM_ID, ATT_DISPLAY_DEFN.ATT_DISPLAY_DESC AS ATT_DISPLAY_DESC
													FROM TAB_PRODUCTS
													LEFT JOIN PAT_SCHEMA ON PAT_SCHEMA.TAB_PROD_ID=TAB_PRODUCTS.TAB_PROD_ID											
													LEFT JOIN PRODUCT_ATTRIBUTES ON PRODUCT_ATTRIBUTES.STANDARD_ATTRIBUTE_CODE = PAT_SCHEMA.STANDARD_ATTRIBUTE_CODE AND PRODUCT_ATTRIBUTES.PRODUCT_ID = TAB_PRODUCTS.PRODUCT_ID
													LEFT JOIN ATTRIBUTE_DEFN ON ATTRIBUTE_DEFN.STANDARD_ATTRIBUTE_CODE = PRODUCT_ATTRIBUTES.STANDARD_ATTRIBUTE_CODE
													LEFT JOIN ATT_DISPLAY_DEFN ON ATT_DISPLAY_DEFN.ATT_DISPLAY = PRODUCT_ATTRIBUTES.ATT_DISPLAY
													
													WHERE TAB_PRODUCTS.PRODUCT_ID = {ProductId}
													ORDER BY TAB_PRODUCTS.RANK,PRODUCT_ATTRIBUTES.ATT_SUBRANK""".format(ProductId = product_obj.PRD_ID))
			tabwise_product_attributes = {}
			#overall_attribute_list = []	
			if product_attributes_obj:
				for product_attribute_obj in product_attributes_obj:
					overall_attribute ={}
					attr_detail = {'attribute_name':product_attribute_obj.STANDARD_ATTRIBUTE_NAME, 
								'attribute_label':str(product_attribute_obj.LABEL), 
								'attribute_system_id':str(product_attribute_obj.SYSTEM_ID),
								'attribute_dtype':str(product_attribute_obj.ATT_DISPLAY_DESC),
								'attribute_code':str(product_attribute_obj.STANDARD_ATTRIBUTE_CODE)
								
								}
					# overall_attribute[str(product_attribute_obj.STANDARD_ATTRIBUTE_CODE)] = str(product_attribute_obj.SYSTEM_ID)
					# overall_attribute_list.append(overall_attribute)
					if product_attribute_obj.TAB_PROD_ID in tabwise_product_attributes:
						tabwise_product_attributes[product_attribute_obj.TAB_PROD_ID].append(attr_detail)
					else:
						tabwise_product_attributes[product_attribute_obj.TAB_PROD_ID] = [attr_detail]
			Trace.Write("tabwise_product_attributes_J "+str(tabwise_product_attributes))
		
			#Trace.Write('overall_attribute_list-----'+str(overall_attribute_list))



			# ATTRvalue = Sql.GetList("SELECT Top 100000 ATDF.STANDARD_ATTRIBUTE_NAME,ATDF.SYSTEM_ID,ATDD.ATT_DISPLAY_DESC,PRDAT.LABEL,PRDAT.LINEITEM,PRDAT.STANDARD_ATTRIBUTE_CODE from ATTRIBUTE_DEFN ATDF INNER JOIN PRODUCT_ATTRIBUTES PRDAT ON ATDF.STANDARD_ATTRIBUTE_CODE = PRDAT.STANDARD_ATTRIBUTE_CODE INNER JOIN ATT_DISPLAY_DEFN ATDD on    PRDAT.ATT_DISPLAY = ATDD.ATT_DISPLAY where PRDAT.PRODUCT_ID = '{product_id}'".format(sap_part_no = str(ATTPRD.SYSTEM_ID),product_id = str(ATTPRD.PRD_ID)) )
			
			# for attr in ATTRvalue:
			# 	STDVALUES =  Sql.GetList("SELECT * from STANDARD_ATTRIBUTE_VALUES where STANDARD_ATTRIBUTE_CODE ='{attr_code}' and SYSTEM_ID like '%{sys_id}%' ".format(attr_code = str(attr.STANDARD_ATTRIBUTE_CODE),sys_id = str(attr.SYSTEM_ID) )  )


			# attr_dict = {}
			# ServiceContainer = Product.GetContainerByName("Services")
			sec_str = getvaludipto = getvaludipt1 = getvaludipt2 = getvaludipt2lt = getvaludipt2lab = getvaludipto_q = getvaludipt2_q = getvaludipt2lt_q = getvaludipt2lab_q = getvaludipt2lab = getvaludipt3lab = getvaludipt3lab_q = getvaludipt3labt = getvaludipt3labt_q= getvaludipt1_q=  getlabortype_calc = gett1labor_calc= gett1labortype_calc =gett2labo_calc = gett2labotype_calc = gett3lab_calc = gett3labtype_calc = ""
			multi_select_attr_list = {}
			getregion=Sql.GetFirst("SELECT REGION from SAQTRV WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' ".format(quoteid,self.quote_revision_record_id))
			if getregion:
				getregionval = getregion.REGION
				
			GetCPSVersion = Sql.GetFirst("SELECT KB_VERSION FROM SAQTSE (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND KB_VERSION IS NOT NULL AND KB_VERSION != ''".format(quoteid,self.quote_revision_record_id))

			if GetCPSVersion :
				if GetCPSVersion.KB_VERSION is not None and GetCPSVersion.KB_VERSION != Fullresponse["kbKey"]["version"]:
					sec_str += '<div id="Headerbnr" class="mart_col_back disp_blk"><div class="col-md-12" id="PageAlert_not"><div class="row modulesecbnr brdr" data-toggle="collapse" data-target="#Alert_notifcatio6" aria-expanded="true">NOTIFICATIONS<i class="pull-right fa fa-chevron-down"></i><i class="pull-right fa fa-chevron-up"></i></div><div id="Alert_notifcatio6" class="col-md-12 alert-notification brdr collapse in"><div class="col-md-12 alert-info"><label title=" Information : The Knowledge Base of the VC Characteristics has been updated in CPS."><img src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/infocircle1.svg" alt="Info"> Information : The Knowledge Base of the VC Characteristics has been updated in CPS.</label></div></div></div></div>'
				else:
					sec_str += ''
			else:
				Trace.Write("GETCPS VERSION EMPTY!")	
			
		
			desc_list = ["APPROVAL","ENTITLEMENT","DESCRIPTION","REQUIRED","VALUE","VALIDATION","CALCULATION FACTOR","ENTITLEMENT COST IMPACT","ENTITLEMENT PRICE IMPACT"]

			#attr_dict = {"APPROVAL":"APPROVAL","ENTITLEMENT DESCRIPTION": "ENTITLEMENT DESCRIPTION","ENTITLEMENT VALUE": "ENTITLEMENT VALUE","DATA TYPE":"DATA TYPE","FACTOR CURRENCY": "FACTOR CURRENCY","CALCULATION FACTOR": "CALCULATION FACTOR","ENTITLEMENT PRICE IMPACT":"ENTITLEMENT PRICE IMPACT","ENTITLEMENT COST IMPACT":"ENTITLEMENT COST IMPACT",}
			
			attr_dict = {"APPROVAL":"APPROVAL","ENTITLEMENT":"ENTITLEMENT","DESCRIPTION": "DESCRIPTION","REQUIRED":"*","VALUE": "VALUE","VALIDATION":"VALIDATION","CALCULATION FACTOR": "CALCULATION FACTOR","ENTITLEMENT PRICE IMPACT":"ENTITLEMENT PRICE IMPACT","ENTITLEMENT COST IMPACT":"ENTITLEMENT COST IMPACT"}
			date_field = []
			
			insertservice = ""
			#Trace.Write("TableObj__J"+str(TableObj)+" EntitlementType_J "+str(EntitlementType))		
		if TableObj is None and (EntitlementType == "EQUIPMENT"): 
			Trace.Write('not inserted')
			getnameentallowed = []
			if product_tabs_obj:
				for product_tab_obj in product_tabs_obj:
					# section=========================product_tab_obj.TAB_NAME,
					product_section =  str(product_tab_obj.TAB_CODE)+'_'+ str(product_tab_obj.TAB_NAME)
					#Trace.Write("product_tab_obj---"+str(product_section))
					list_of_tabs.append(product_section)
					#Trace.Write("list_of_tabs---"+str(list_of_tabs))
					sysectObj = Sql.GetFirst(
						"SELECT RECORD_ID,SECTION_DESC,SECTION_NAME FROM SYSECT (NOLOCK) WHERE SECTION_NAME='"+str(product_section)+"'"
					)
					date_boot_field=[]
					tablistdict = {}
					if sysectObj and str(sysectObj.SECTION_NAME) == str(product_section):
						Section_id = sysectObj.RECORD_ID
						Section_desc = sysectObj.SECTION_DESC.split('_')
						Section_desc = sysectObj.SECTION_DESC.split('_')[len(Section_desc) - 1]
					else:
						get_last_secid = Sql.GetFirst("select max(SAPCPQ_ATTRIBUTE_NAME) as saprec_id from sysect where SAPCPQ_ATTRIBUTE_NAME like '%SYSECT-SA%'")
						if get_last_secid:
							get_last_secid = get_last_secid.saprec_id.split('-')[2]
							get_last_secid = int(int(get_last_secid)) + 1
							get_lastsection_val = 'SYSECT-SA-'+ str(get_last_secid)
							getsect_tab = Sql.GetTable("SYSECT")
							tbrowsect = {}
							tbrowsect['RECORD_ID'] = str(Guid.NewGuid()).upper()
							tbrowsect['SAPCPQ_ATTRIBUTE_NAME'] = get_lastsection_val
							tbrowsect['SECTION_DESC'] =  str(product_section)
							tbrowsect['SECTION_NAME'] =  str(product_section)
							tbrowsect['SECTION_PARTNUMBER'] =  self.treeparam.upper()
							tbrowsect['PARENT_SECTION_TEXT'] = product_tab_obj.SYSTEM_ID
							getsect_tab.AddRow(tbrowsect)
							Sql.Upsert(getsect_tab)
							sysectObj = Sql.GetFirst("SELECT RECORD_ID,SECTION_DESC,PARENT_SECTION_TEXT FROM SYSECT (NOLOCK) WHERE SECTION_NAME='" + str(product_section) + "'")
							if sysectObj:
								Section_id = sysectObj.RECORD_ID
								Section_desc = sysectObj.SECTION_DESC.split('_')
								Section_desc = sysectObj.SECTION_DESC.split('_')[len(Section_desc) - 1]
					add_style =  add_style_color = ""
					sec_str_boot += ('<div id="sec_'+str(Section_id)+ '" class="dyn_main_head master_manufac glyphicon pointer   glyphicon-chevron-down margtop10" onclick="dyn_main_sec_collapse_arrow(this)" data-target="#sc_'+ str(Section_id)+ '" data-toggle="collapse" <label class="onlytext"><label class="onlytext"><div>'+ str(Section_desc).upper()+ '</div></label></div><div id="sc_'+str(Section_id)+ '" class="collapse in "><table id="' + str(Section_id)+ '" class= "getentdata" data-filter-control="true" data-maintain-selected="true" data-locale = "en-US" data-escape="true" data-html="true"  data-show-header="true" > <thead><tr class="hovergrey">')
					
					for key, invs in enumerate(list(desc_list)):
						invs = str(invs).strip()
						qstring = attr_dict.get(str(invs)) or ""
						sec_str_boot += (
							'<th data-field="'
							+ invs
							+ '" data-title-tooltip="'
							+ str(qstring)
							+ '" >'
							+ str(qstring)
							+ "</th>"
						)
					sec_str_boot += '</tr></thead><tbody onclick="Table_Onclick_Scroll(this)" ></tbody></table>'
					sec_str_boot += ('<div id = "btn_ent" class="g4  except_sec removeHorLine iconhvr sec_edit_sty" style="display: none;"><button id="entcancel" class="btnconfig btnMainBanner sec_edit_sty_btn"  onclick="fabcostlocatecancel(this)" style="display: none;" class="btnconfig">CANCEL</button><button id="entsave" class="btnconfig btnMainBanner sec_edit_sty_btn"  onclick="fabcostlocatesave(this)" style="display: none;" class="btnconfig">SAVE</button></div>')
					attribute_Name_list = []
					#Trace.Write(" tabwise_product_attributes.get(product_tab_obj.TAB_PROD_ID)"+str(tabwise_product_attributes.get(product_tab_obj.TAB_PROD_ID)))
					if tabwise_product_attributes.get(product_tab_obj.TAB_PROD_ID):
						for attribute in tabwise_product_attributes.get(product_tab_obj.TAB_PROD_ID):

							new_value_dicta = {}
							attrName = attribute['attribute_name']
							attrLabel = attribute['attribute_label']	
							attrSysId = attribute['attribute_system_id']
							attribute_code = attribute['attribute_code']					
							STDVALUES =  Sql.GetFirst("SELECT * FROM STANDARD_ATTRIBUTE_VALUES WHERE SYSTEM_ID like '%{sys_id}%' ".format(sys_id = attrSysId)  )
							if STDVALUES:
								attrValue = STDVALUES.STANDARD_ATTRIBUTE_VALUE
								if attrValue == "DefaultValue":
									attrValue = ''
							else:
								attrValue = ''
							
							attribute_Name_list.append(attrSysId)
							DType = attribute['attribute_dtype']
							#Trace.Write(str(DType)+'----'+str(attrName)+'--attrName---attrSysId--'+str(attrSysId))
							#Trace.Write(str(attrLabel)+'--attrLabel----attrValue--'+str(attrValue))
							if attrSysId in attributesdisallowedlst:
								if attrSysId in attributedefaultvalue:
									add_style = "display:none;"
								else:
									add_style = "display:none;color:#1B78D2"
								attributes_disallowed_list.append(attrSysId)
							else:
								add_style = ""
							Trace.Write('---attributeEditlst--'+str(attributeEditlst))
							if attrSysId not in attributedefaultvalue:
								#Trace.Write("add_style----3077----- "+str(attrSysId))
								add_style = "color:#1B78D2"
							# if attrSysId in attributedefaultvalue:
							# 	add_style_color = ";color: red"
							# else:
							# 	add_style_color = ""
							
							if attrSysId in attributeEditlst :
								disable_edit = 'disable_edit'
								edit_pencil_icon = '<a href="#" class="editclick"><i title="Double Click to Edit" class="fa fa-pencil"  aria-hidden="true"></i></a>'
								
							else:
								disable_edit = ''
								edit_pencil_icon = '<a href="#" class="editclick"><i title="Double Click to Edit" class="fa fa-lock"  aria-hidden="true"></i></a>'
							attrValueSysId = attributevalues.get(attrSysId)
							#Trace.Write('attrValueSysId'+str(attrValueSysId))
							if DType == 'Check Box' and attrValueSysId is None:
								attr_value =''
								ent_val_code = ''
								#Trace.Write("attrValueSysId---inside"+str(attrValueSysId))
							elif  DType == 'Free Input, no Matching':
								if attributevalues.get(attrSysId) is None:
									attr_value = ''
								else:
									attr_value = attributevalues.get(attrSysId)	
								#Trace.Write('attr_value'+str(attr_value)+'---'+str(attrSysId))
								ent_val_code = attrValueSysId
							else:
								attr_value = attrValue
								ent_val_code = attrValueSysId
							# Inserting Rows:
							#Trace.Write('attr_value------1'+str(attr_value)+'---'+str(attrSysId))
							insertservice += """<QUOTE_ITEM_ENTITLEMENT>
								<ENTITLEMENT_ID>{ent_name}</ENTITLEMENT_ID>
								<ENTITLEMENT_VALUE_CODE>{ent_val_code}</ENTITLEMENT_VALUE_CODE>
								<ENTITLEMENT_DESCRIPTION>{ent_desc}</ENTITLEMENT_DESCRIPTION>
								<ENTITLEMENT_TYPE>{ent_type}</ENTITLEMENT_TYPE>							
								<ENTITLEMENT_DISPLAY_VALUE>{ent_disp_val}</ENTITLEMENT_DISPLAY_VALUE>
								<ENTITLEMENT_COST_IMPACT>{ct}</ENTITLEMENT_COST_IMPACT>
								<ENTITLEMENT_PRICE_IMPACT>{pi}</ENTITLEMENT_PRICE_IMPACT>
								<IS_DEFAULT>{is_default}</IS_DEFAULT>
								<PRICE_METHOD>{pm}</PRICE_METHOD>
								<CALCULATION_FACTOR>{cf}</CALCULATION_FACTOR>
								<ENTITLEMENT_NAME>{ent_desc}</ENTITLEMENT_NAME>
								</QUOTE_ITEM_ENTITLEMENT>""".format(ent_name = str(attrSysId),ent_val_code =ent_val_code,ent_type = DType,ent_desc = attrName,ent_disp_val = attr_value,ct = '',pi = '',is_default =  '1' if str(attrSysId) in attributedefaultvalue else '0',pm = '',cf = '')
							if DType == "Drop Down":
								Trace.Write('attrSysId--2324-500------------drop down----'+str(attrSysId))
								#STDVALUES =  Sql.GetList("SELECT * from STANDARD_ATTRIBUTE_VALUES where  SYSTEM_ID like '%{sys_id}%' and STANDARD_ATTRIBUTE_CODE = '{attr_code}' ".format(sys_id = str(attrSysId), attr_code = attribute_code )  )
								STDVALUES = Sql.GetList("""SELECT TOP 100 A.PA_ID, A.PAV_ID, A.STANDARD_ATTRIBUTE_VALUE_CD, A.STANDARD_ATTRIBUTE_PRICE, A.NON_STANDARD_VALUE, A.NON_STANDARD_DISPLAY_VALUE, 
								A.PRODUCT_ATT_IMAGE_OFF_ALT_TEXT, A.SORT_RANK, A.RELATED_PRODUCT_ID

								, COALESCE(P.PRODUCT_CATALOG_CODE, A.VALUE_CATALOG_CODE) VALUE_CATALOG_CODE

								, PA.STANDARD_ATTRIBUTE_CODE, COALESCE(P.PRODUCT_NAME, V.STANDARD_ATTRIBUTE_DISPLAY_VAL) STANDARD_ATTRIBUTE_DISPLAY_VAL, V.SYSTEM_ID,V.STANDARD_ATTRIBUTE_VALUE, V.SYSTEM_ID AS VALUE_SYSTEM_ID, V.UNIT_ID AS VALUE_UNIT_ID, V.BILLING_PERIOD_ID AS VALUE_BILLING_PERIOD_ID
								, PA.USEALTERNATIVEPRICINGFORPRODUCTSINCONTAINER
								, COALESCE(P_ML.PRODUCT_NAME, P.PRODUCT_NAME, STDML.STANDARD_ATTRIBUTE_DISPLAY_VAL, V.SYSTEM_ID,V.STANDARD_ATTRIBUTE_DISPLAY_VAL) AS ML_NON_STANDARD_DISPLAY_VALUE
								FROM PRODUCT_ATTRIBUTES PA INNER JOIN ATTRIBUTES A ON PA.PA_ID=A.PA_ID 
								INNER JOIN STANDARD_ATTRIBUTE_VALUES V ON A.STANDARD_ATTRIBUTE_VALUE_CD = V.STANDARD_ATTRIBUTE_VALUE_CD  
								LEFT OUTER JOIN PRODUCTS P ON A.RELATED_PRODUCT_ID=P.PRODUCT_ID 
								LEFT OUTER JOIN PRODUCTS_ML P_ML ON P.PRODUCT_ID=P_ML.PRODUCT_ID AND P_ML.ML_ID=0
								LEFT JOIN  ATTRIBUTES_ML ML ON A.PAV_ID=ML.PAV_ID AND ML.ML_ID= 0
								LEFT JOIN STANDARD_ATTRIBUTE_VALUES_ML STDML ON A.STANDARD_ATTRIBUTE_VALUE_CD=STDML.STANDARD_ATTRIBUTE_VALUE_CD AND STDML.ML_ID=0 LEFT OUTER JOIN test_USD_L1 ON COALESCE(P.PRODUCT_CATALOG_CODE, A.VALUE_CATALOG_CODE) = test_USD_L1.PARTNUMBER AND ISNULL(A.PRICINGCODE, '')=ISNULL(test_USD_L1.PRICECODE, '') 
								WHERE PA.PRODUCT_ID ={productId} AND V.STANDARD_ATTRIBUTE_CODE  = {sys_id} ORDER BY A.SORT_RANK""".format(sys_id = attribute_code,productId = str(product_obj.PRD_ID)))
								VAR1 = sec_str1 = selected_option = ""
								if STDVALUES:
									if attributevalues.get(attrSysId) is not None:
										select_option = 'selected'
										default = ''
									else:
										select_option = ""
										default = 'selected'
										selected_option = ' title="Select" '
									VAR1 += '<option value="select" ' +str(default)+' style= "display:none;"> </option>'
									for value in STDVALUES:
										if value.SYSTEM_ID in dropdowndisallowlist:
											disallow_style = "style = 'display:none'"
										else:	
											disallow_style = ""
										if str(selected_option)=='selected':
											selected_option = ' title="'+str(value.STANDARD_ATTRIBUTE_DISPLAY_VAL)+'" '
										VAR1 += (
											'<option '+disallow_style+' id="'+value.SYSTEM_ID+'"  value = "'
											+ value.STANDARD_ATTRIBUTE_DISPLAY_VAL
											+ '"'+select_option+'>'
											+ value.STANDARD_ATTRIBUTE_DISPLAY_VAL
											+ "</option>"
										)
								sec_str1 += (
									'<select class="form-control remove_yellow '+str(disable_edit)+'" style ="'+str(add_style)+'" id = "'
									+ str(attrSysId)
									+ '" type="text"  data-content ="'
									+ str(attrSysId)
									+ '" class="form-control '+str(disable_edit)+'" onchange="editent_bt(this)" '+str(selected_option)+'  disabled>'
									+ VAR1
									+ "</select>"
								)
									#sec_str += "<option id='"+str(attrcode)+"' >" + str(optionvalue) + "</option>"
								#sec_str += "</select></td>"
							elif DType == "Check Box":
								multi_select_attr_list[attrSysId] = ""
								#Trace.Write('attrSysId--2324--checkbox---2624------'+str(attrSysId)+'---'+str(multi_select_attr_list))
								#STDVALUES =  Sql.GetList("SELECT * from STANDARD_ATTRIBUTE_VALUES where  SYSTEM_ID like '%{sys_id}%' and STANDARD_ATTRIBUTE_CODE = '{attr_code}' ".format(sys_id = str(attrSysId), attr_code = attribute_code )  )
								STDVALUES = Sql.GetList("""SELECT TOP 100 A.PA_ID, A.PAV_ID, A.STANDARD_ATTRIBUTE_VALUE_CD, A.STANDARD_ATTRIBUTE_PRICE, A.NON_STANDARD_VALUE, A.NON_STANDARD_DISPLAY_VALUE, 
								A.PRODUCT_ATT_IMAGE_OFF_ALT_TEXT, A.SORT_RANK, A.RELATED_PRODUCT_ID

								, COALESCE(P.PRODUCT_CATALOG_CODE, A.VALUE_CATALOG_CODE) VALUE_CATALOG_CODE

								, PA.STANDARD_ATTRIBUTE_CODE, COALESCE(P.PRODUCT_NAME, V.STANDARD_ATTRIBUTE_DISPLAY_VAL) STANDARD_ATTRIBUTE_DISPLAY_VAL, V.SYSTEM_ID,V.STANDARD_ATTRIBUTE_VALUE, V.SYSTEM_ID AS VALUE_SYSTEM_ID, V.UNIT_ID AS VALUE_UNIT_ID, V.BILLING_PERIOD_ID AS VALUE_BILLING_PERIOD_ID
								, PA.USEALTERNATIVEPRICINGFORPRODUCTSINCONTAINER
								, COALESCE(P_ML.PRODUCT_NAME, P.PRODUCT_NAME, STDML.STANDARD_ATTRIBUTE_DISPLAY_VAL, V.SYSTEM_ID,V.STANDARD_ATTRIBUTE_DISPLAY_VAL) AS ML_NON_STANDARD_DISPLAY_VALUE
								FROM PRODUCT_ATTRIBUTES PA INNER JOIN ATTRIBUTES A ON PA.PA_ID=A.PA_ID 
								INNER JOIN STANDARD_ATTRIBUTE_VALUES V ON A.STANDARD_ATTRIBUTE_VALUE_CD = V.STANDARD_ATTRIBUTE_VALUE_CD  
								LEFT OUTER JOIN PRODUCTS P ON A.RELATED_PRODUCT_ID=P.PRODUCT_ID 
								LEFT OUTER JOIN PRODUCTS_ML P_ML ON P.PRODUCT_ID=P_ML.PRODUCT_ID AND P_ML.ML_ID=0
								LEFT JOIN  ATTRIBUTES_ML ML ON A.PAV_ID=ML.PAV_ID AND ML.ML_ID= 0
								LEFT JOIN STANDARD_ATTRIBUTE_VALUES_ML STDML ON A.STANDARD_ATTRIBUTE_VALUE_CD=STDML.STANDARD_ATTRIBUTE_VALUE_CD AND STDML.ML_ID=0 LEFT OUTER JOIN test_USD_L1 ON COALESCE(P.PRODUCT_CATALOG_CODE, A.VALUE_CATALOG_CODE) = test_USD_L1.PARTNUMBER AND ISNULL(A.PRICINGCODE, '')=ISNULL(test_USD_L1.PRICECODE, '') 
								WHERE PA.PRODUCT_ID ={productId} AND V.STANDARD_ATTRIBUTE_CODE  = {sys_id} ORDER BY A.SORT_RANK""".format(sys_id = attribute_code,productId = str(product_obj.PRD_ID)))
								VAR1 = sec_str1 = ""
								if STDVALUES:
									for value in STDVALUES:
										if value.SYSTEM_ID in dropdowndisallowlist:
											disallow_style = "style = 'display:none'"
										else:	
											disallow_style = ""
										#if attrValue == value.STANDARD_ATTRIBUTE_VALUE:
											#Trace.Write("SYSTEM_ID"+str(value.SYSTEM_ID))
											#get_code = Sql.GetFirst("SELECT * from STANDARD_ATTRIBUTE_VALUES where  SYSTEM_ID like '{sys_id}' ".format(sys_id = str(value.SYSTEM_ID) )  )
											#get_id = [ attr[str(get_code.STANDARD_ATTRIBUTE_CODE)] for attr in overall_attribute_list]
											#getnameentallowed.append(value.SYSTEM_ID)
											#Trace.Write('valueeeee----'+str(getnameentallowed))
										VAR1 += (
											'<option '+str(disallow_style)+'  id="'+str(value.SYSTEM_ID)+'" value = "'
											+ str(value.STANDARD_ATTRIBUTE_DISPLAY_VAL)
											+ '">'
											+ str(value.STANDARD_ATTRIBUTE_DISPLAY_VAL)
											+ "</option>"
										)
								sec_str1 += (
									'<select class="form-control remove_yellow div_multi_checkbox" style ="'+str(add_style)+'" id = "'
									+ str(attrSysId)
									+ '" type="text"  data-content ="'
									+ str(attrSysId)
									+ '" class="form-control" onchange="editent_bt(this)" disabled>'
									+ str(VAR1)
									+ "</select>"
								)
									#sec_str += "<option id='"+str(attrcode)+"' >" + str(optionvalue) + "</option>"
								#sec_str += "</select></td>"
							elif DType == "Free Input, no Matching":
								if str(attrSysId) in ("AGS_REL_STDATE",'AGS_Z0007_GEN_RELDAT'):
									datepicker = "onclick_datepicker_locdate('" + attrSysId + "')"
									datepicker_onchange = "onchangedatepicker('" + attrSysId + "')"

									sec_str1 += (
										'<input class="form-control no_border_bg  datePickerField wth157fltltbrdbt '+str(disable_edit)+'" id = "'
										+ str(attrSysId)
										+ '" type="text"  style ="'+str(add_style)+'"  onclick="'+ str(datepicker)+ '"  data-content ="'
										+ str(attr_value)
										+ '" value = "'+str(attr_value)+'" title="'+str(attr_value)+'"  disabled>'
										+ "</input> "
									)
								else:
									#Trace.Write('617----attrSysId----'+str(attrSysId))
									STDVALUES =  Sql.GetFirst("SELECT STANDARD_ATTRIBUTE_VALUE from STANDARD_ATTRIBUTE_VALUES  where  SYSTEM_ID like '%{sys_id}%' ".format(sys_id = str(attrSysId))  )							
									sec_str1 = ""
									if attr_value == "DefaultValue":
										attr_value = ''
									sec_str1 += (
										'<input maxlength="255" class="form-control '+str(disable_edit)+'" id = "'
										+ str(attrSysId)
										+ '" type="text"  data-content ="'
										+ str(attrSysId)
										+ '" value = "'+str(attr_value)+'" title = "'+str(attr_value)+'" onchange="editent_bt(this)" disabled>'
										+ "</input>"
									)
							else:
								getinval = ''
								#Trace.Write('attrSysId--input-----'+str(attrSysId))
								STDVALUES =  Sql.GetFirst("SELECT STANDARD_ATTRIBUTE_VALUE from STANDARD_ATTRIBUTE_VALUES  where  SYSTEM_ID like '%{sys_id}%' ".format(sys_id = str(attrSysId))  )
								if STDVALUES:
									getinval = STDVALUES.STANDARD_ATTRIBUTE_VALUE
								else:
									getinval = ''

								sec_str1 += (
									'<input maxlength="255" class="form-control '+str(disable_edit)+'" id = "'
									+ str(attrSysId)
									+ '" type="text"  data-content ="'
									+ str(attrSysId)
									+ '"  disabled>'
									+ "</input>"
								)
							#getnameentallowed.append(attrName)
							#totaldisallowlist = [item for item in attributesdisallowedlst if item not in getnameentallowed]
							new_value_dicta["APPROVAL"] = ""	
							new_value_dicta["ENTITLEMENT"] = attrName
							new_value_dicta["DESCRIPTION"] = ""
							new_value_dicta["REQUIRED"] = ""
							#Trace.Write('sec_str1---2372---'+str(sec_str1))
							if DType == "Drop Down" or DType == "Check Box" or DType =="Free Input, no Matching":
								new_value_dicta["VALUE"] =  sec_str1
							else:
								new_value_dicta["VALUE"] =  attrValue
							#new_value_dicta["FACTOR CURRENCY"] = ""
							new_value_dicta["ENTITLEMENT COST IMPACT"]= ""
							new_value_dicta["ENTITLEMENT PRICE IMPACT"]= str("<abbr class = 'wid90_per' title=''></abbr>")+str(edit_pencil_icon)
							#new_value_dicta["DATA TYPE"] = ""
							new_value_dicta["CALCULATION FACTOR"] = ""
							new_value_dicta["VALIDATION"]= ""
							

							if new_value_dicta:
								date_boot_field.append(new_value_dicta)
						sec_str_boot += ('</div>')
					if len(date_boot_field) > 0:
						tablistdict[Section_id] = date_boot_field
						
					if len(tablistdict) > 0:
						tablistnew.append(tablistdict)
					table_ids = '#'+Section_id
					getdivid = '#sc_'+Section_id+' .sec_edit_sty'
					getdividbtn = '#sc_'+Section_id+' #btn_ent .sec_edit_sty_btn'
					getprevdicts +=   ("try{var dict_new = {};$('"+str(table_ids)+" tbody tr td select').each(function () {dict_new[$(this).attr('id')] = $(this).children(':selected').val();});$('"+str(table_ids)+" tbody tr td input').each(function () {dict_new[$(this).attr('id')] = $(this).val();});console.log('dict_new-2190-2938----',dict_new);}catch{console.log('')}")
					#dbl_clk_function +=   ("try{var dict_new = {};$('"+str(table_ids)+"').on('dbl-click-cell.bs.table', function (e, row, $element) { $('"+str(table_ids)+" tbody tr:visible').each(function () {dict_new[$(this).find('td:nth-child(3) select').attr('id')] =$(this).find('td:nth-child(3) select').children(':selected').val() ;});$('"+str(table_ids)+" tbody tr:visible').each(function () {dict_new[$(this).find('td:nth-child(3) input').attr('id')] =  $(this).find('td:nth-child(3) input').val();});console.log('dblclk_dict_new-28001--',dict_new);localStorage.setItem('prventdict', JSON.stringify(dict_new))})}catch{console.log('')}")
					#dbl_clk_function +=   ("try{var dict_new = {};$('"+str(table_ids)+"').on('dbl-click-cell.bs.table', function (e, row, $element) { $('"+str(table_ids)+" tbody tr td select').each(function () {dict_new[$(this).attr('id')] = $(this).children(':selected').val();});$('"+str(table_ids)+" tbody tr td input').each(function () {dict_new[$(this).attr('id')] = $(this).val();});console.log('dblclk_dict_new-2800--',dict_new);localStorage.setItem('prventdict', JSON.stringify(dict_new))})}catch{console.log('')}")
					dbl_clk_function +=   ("try{var dict_new = {};localStorage.setItem('editfirst','true');$('"+str(table_ids)+"').on('dbl-click-cell.bs.table', function (e, row, $element) { localStorage.setItem('AddNew','false');$('"+str(table_ids)+" tbody tr:visible').each(function () {var getcostimpact =  $(this).find('td:nth-child(7) ').text();var getpriceimpact =  $(this).find('td:nth-child(8) ').text();dict_new[$(this).find('td:nth-child(3) select').attr('id')] =$(this).find('td:nth-child(3) select').children(':selected').val()+'||'+getcostimpact+'||'+getpriceimpact;});var arr = [];$('"+str(table_ids)+" tbody tr:visible').each(function () {if ($(this).find('td:nth-child(3) input') && !($(this).find('td:nth-child(3) input').attr('type') == 'checkbox') ){var getcostimpact =  $(this).find('td:nth-child(7) ').text();var getpriceimpact =  $(this).find('td:nth-child(8) ').text();dict_new[$(this).find('td:nth-child(3) input').attr('id')] =  $(this).find('td:nth-child(3) input').val()+'||'+getcostimpact+'||'+getpriceimpact;}else if ($(this).find('td:nth-child(3) input').attr('type') == 'checkbox') {var getcostimpact =  $(this).find('td:nth-child(7) ').text();var getpriceimpact =  $(this).find('td:nth-child(8) ').text();$(this).find('.mulinput:checked').each(function () {arr.push($(this).val());console.log('arr',arr) });dict_new[$(this).find('td:nth-child(3) select').attr('id')] =  arr+'||'+getcostimpact+'||'+getpriceimpact;};});console.log('dblclk_dict_new-28002--',dict_new,'--',"+str(dropdowndisallowlist)+");localStorage.setItem('prventdict', JSON.stringify(dict_new))})}catch(e){console.log('error---12',e)}")
					
					dbl_clk_function += (
						"try { console.log('2944 start----');var newentdict =[]; var newentValues =[]; var getentedictip = [];$('"+str(table_ids)+"').on('dbl-click-cell.bs.table', function (e, row, $element) {if(localStorage.getItem('EDITENT_SEC') != 'EDIT'){console.log('tset--prev value-2944---222-----',this.value);localStorage.setItem('EDITENT_SEC','EDIT'); $('"+str(table_ids)+" .disable_edit').prop('disabled', false);$('.sec_edit_sty_btn').css('display','block');$('#sc_'+'"+str(Section_id)+"').addClass('header_section_div header_section_div_pad_bt10');$('"+str(getdivid)+"').css('display','block');$('"+str(table_ids)+" .disable_edit').removeClass('remove_yellow ').addClass('light_yellow');$('#AGS_CON_DAY').removeClass('light_yellow').addClass('remove_yellow');$('#AGS_CON_DAY').prop('disabled', true);$('"+str(getdividbtn)+"').css('display','block');$('#entsave').css('display','block');$('#entcancel').css('display','block');$('"+str(table_ids)+" .MultiCheckBox').css('pointer-events','auto');var getmanualip = $('#ADDL_PERF_GUARANTEE_91_1').find(':selected').text();if(getmanualip.toUpperCase() == 'MANUAL INPUT'){ $('#ADDL_PERF_GUARANTEE_91_1_imt').removeAttr('disabled');$('#ADDL_PERF_GUARANTEE_91_1_imt').removeClass('remove_yellow ').addClass('light_yellow');$('#ADDL_PERF_GUARANTEE_91_1_primp').removeAttr('disabled');$('#ADDL_PERF_GUARANTEE_91_1_primp').removeClass('remove_yellow ').addClass('light_yellow');}$('#ADDL_PERF_GUARANTEE_91_1_imt').attr('disabled', 'disabled');$('"+str(table_ids)+" tbody tr td:nth-child(6) input').removeClass('light_yellow').addClass('remove_yellow');$('"+str(table_ids)+" tbody tr td:nth-child(4) input').removeClass('light_yellow').addClass('remove_yellow');$('#entsave').css('display','block');$('#entcancel').css('display','block');$('input').on('focus', function () {var previnp = $(this).data('val', $(this).val());var getprevid = this.id;var prev_concate_data = getprevid +'='+previnp;}).change(function() {var prev = $(this).data('val');var current = $(this).val();var getseltabledesc = this.id;var getinputtbleid =  $(this).closest('table').attr('id');var concated_data = getinputtbleid+'|'+current+'|'+getseltabledesc;if(!getentedictip.includes(concated_data)){getentedictip.push(concated_data)};getentedictip1 = JSON.stringify(getentedictip);localStorage.setItem('getdictentdata', getentedictip1);});}})}catch {console.log('error---')}"
					)
					#Trace.Write('dbl_clk_function--2946-'+str(dbl_clk_function))
					'''dbl_clk_function += (
						"try {var getentedict = [];$('"+str(table_ids)+"').on('dbl-click-cell.bs.table', function (e, row, $element) {console.log('tset--prev value---',this.value);$('"+str(table_ids)+"').find(':input(:disabled)').prop('disabled', false);$('"+str(table_ids)+" tbody  tr td select option').css('background-color','lightYellow');$('"+str(table_ids)+" tbody  tr td input').css('background-color','lightYellow');$('"+str(table_ids)+"  tbody tr td select').addClass('light_yellow');$('"+str(table_ids)+" .disable_edit').addClass('light_yellow');$('#fabcostlocate_save').css('display','block');$('#fabcostlocate_cancel').css('display','block');});}catch {console.log('error---')}"
					)'''
				
					tbrow = {}
					tbrow["QUOTE_SERVICE_ENTITLEMENT_RECORD_ID"] = str(Guid.NewGuid()).upper()
					tbrow["QUOTE_ID"] = QUOTE_ID
					tbrow["QUOTE_NAME"] = QUOTE_NAME
					tbrow["QUOTE_RECORD_ID"] = QUOTE_RECORD_ID
					tbrow["QTEREV_RECORD_ID"] = QTEREV_RECORD_ID
					tbrow["QTEREV_ID"] = Quote.GetGlobal("quote_revision_id")
					tbrow["QTESRV_RECORD_ID"] = QUOTE_SERVICE_RECORD_ID
					tbrow["SERVICE_RECORD_ID"] = SERVICE_RECORD_ID
					tbrow["SERVICE_ID"] = SERVICE_ID
					tbrow["SERVICE_DESCRIPTION"] = SERVICE_DESCRIPTION
					tbrow["ENTITLEMENT_XML"]=insertservice
					tbrow["CPS_CONFIGURATION_ID"] = Fullresponse["id"]
					tbrow["SALESORG_RECORD_ID"] = SALESORG_RECORD_ID
					tbrow["SALESORG_ID"] = SALESORG_ID
					tbrow["SALESORG_NAME"] = SALESORG_NAME
					tbrow["CPS_MATCH_ID"] = 1
					
					tbrow["KB_VERSION"] = Fullresponse["kbKey"]["version"]
					tbrow["CPQTABLEENTRYADDEDBY"] = userId
					tbrow["CPQTABLEENTRYDATEADDED"] = datetime.now().strftime("%m/%d/%Y %H:%M:%S %p")

					columns = ', '.join("" + str(x) + "" for x in tbrow.keys())
					values = ', '.join("'" + str(x) + "'" for x in tbrow.values())
					insert_qtqtse_query = "INSERT INTO SAQTSE ( %s ) VALUES ( %s );" % (columns, values)				
				Sql.RunQuery(insert_qtqtse_query)
				# if objname_ent == "SAQSAO":
				#     QueryStatement ="""
				#     MERGE SAQIEN SRC USING (SELECT A.ENTITLEMENT_XML,B.EQUIPMENT_ID,B.EQUIPMENT_RECORD_ID,B.LINE_ITEM_ID,A.QUOTE_ID,B.QUOTE_ITEM_COVERED_OBJECT_RECORD_ID,B.QTEITM_RECORD_ID,A.QUOTE_RECORD_ID,A.QTEREV_RECORD_ID,A.QUOTE_SERVICE_ENTITLEMENT_RECORD_ID,B.SERIAL_NO,A.SERVICE_DESCRIPTION,A.SERVICE_ID,A.SERVICE_RECORD_ID,A.SALESORG_ID,A.SALESORG_NAME,A.SALESORG_RECORD_ID,A.CPS_CONFIGURATION_ID,B.EQUIPMENT_LINE_ID FROM SAQTSE(NOLOCK) A JOIN SAQICO (NOLOCK) B ON A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.QTEREV_RECORD_ID = B.QTEREV_RECORD_ID AND A.SALESORG_ID =B.SALESORG_ID where A.QUOTE_RECORD_ID = '{rec}' AND A.QTEREV_RECORD_ID  = '{revision_rec_id}' )
				#     TGT ON (SRC.QUOTE_RECORD_ID = TGT.QUOTE_RECORD_ID AND SRC.QTEREV_RECORD_ID = TGT.QTEREV_RECORD_ID AND SRC.SERVICE_ID = TGT.SERVICE_ID AND SRC.EQUIPMENT_ID = TGT.EQUIPMENT_ID)
				#     WHEN MATCHED
				#     THEN UPDATE SET SRC.ENTITLEMENT_XML = TGT.ENTITLEMENT_XML
				#     WHEN NOT MATCHED BY TARGET
				#     THEN INSERT(QUOTE_ITEM_COVERED_OBJECT_ENTITLEMENTS_RECORD_ID,ENTITLEMENT_XML,EQUIPMENT_ID,EQUIPMENT_RECORD_ID,LINE_ITEM_ID,QUOTE_ID,QTEITMCOB_RECORD_ID,QTEITM_RECORD_ID,QUOTE_RECORD_ID,QTEREV_RECORD_ID,QTESRVENT_RECORD_ID,SERIAL_NO,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,CPS_CONFIGURATION_ID,EQUIPMENT_LINE_ID,CPQTABLEENTRYDATEADDED, CPQTABLEENTRYADDEDBY, ADDUSR_RECORD_ID, CpqTableEntryModifiedBy,
				#             CpqTableEntryDateModified)
				#     VALUES (NEWID(),ENTITLEMENT_XML,EQUIPMENT_ID,EQUIPMENT_RECORD_ID,LINE_ITEM_ID,QUOTE_ID,QUOTE_ITEM_COVERED_OBJECT_RECORD_ID,QTEITM_RECORD_ID,QUOTE_RECORD_ID,QTEREV_RECORD_ID,QUOTE_SERVICE_ENTITLEMENT_RECORD_ID,SERIAL_NO,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,CPS_CONFIGURATION_ID,EQUIPMENT_LINE_ID,'{datetimenow}', '{username}', {userid}, {userid}, '{datetimenow}' );""".format(rec=quoteid, datetimenow=datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"), userid=userId, username=userName, revision_rec_id = self.quote_revision_record_id )
				
				# else:
				#     QueryStatement ="""
				#     MERGE SAQIEN SRC USING (SELECT A.ENTITLEMENT_XML,B.EQUIPMENT_ID,B.EQUIPMENT_RECORD_ID,B.LINE_ITEM_ID,A.QUOTE_ID,B.QUOTE_ITEM_COVERED_OBJECT_RECORD_ID,B.QTEITM_RECORD_ID,A.QUOTE_RECORD_ID,A.QTEREV_RECORD_ID,A.QUOTE_SERVICE_ENTITLEMENT_RECORD_ID,B.SERIAL_NO,A.SERVICE_DESCRIPTION,A.SERVICE_ID,A.SERVICE_RECORD_ID,A.SALESORG_ID,A.SALESORG_NAME,A.SALESORG_RECORD_ID,A.CPS_CONFIGURATION_ID,B.EQUIPMENT_LINE_ID FROM SAQTSE(NOLOCK) A JOIN SAQICO (NOLOCK) B ON A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.QTEREV_RECORD_ID = B.QTEREV_RECORD_ID AND A.SALESORG_ID =B.SALESORG_ID where A.QUOTE_RECORD_ID = '{rec}'  AND A.QTEREV_RECORD_ID  = '{revision_rec_id}' )
				#     TGT ON (SRC.QUOTE_RECORD_ID = TGT.QUOTE_RECORD_ID AND SRC.QTEREV_RECORD_ID = TGT.QTEREV_RECORD_ID AND SRC.SERVICE_ID = TGT.SERVICE_ID)
				#     WHEN MATCHED
				#     THEN UPDATE SET SRC.ENTITLEMENT_XML = TGT.ENTITLEMENT_XML
				#     WHEN NOT MATCHED BY TARGET
				#     THEN INSERT(QUOTE_ITEM_COVERED_OBJECT_ENTITLEMENTS_RECORD_ID,ENTITLEMENT_XML,EQUIPMENT_ID,EQUIPMENT_RECORD_ID,LINE_ITEM_ID,QUOTE_ID,QTEITMCOB_RECORD_ID,QTEITM_RECORD_ID,QUOTE_RECORD_ID,QTEREV_RECORD_ID,QTESRVENT_RECORD_ID,SERIAL_NO,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,CPS_CONFIGURATION_ID,EQUIPMENT_LINE_ID,CPQTABLEENTRYDATEADDED, CPQTABLEENTRYADDEDBY, ADDUSR_RECORD_ID, CpqTableEntryModifiedBy,
				#             CpqTableEntryDateModified)
				#     VALUES (NEWID(),ENTITLEMENT_XML,EQUIPMENT_ID,EQUIPMENT_RECORD_ID,LINE_ITEM_ID,QUOTE_ID,QUOTE_ITEM_COVERED_OBJECT_RECORD_ID,QTEITM_RECORD_ID,QUOTE_RECORD_ID,QTEREV_RECORD_ID,QUOTE_SERVICE_ENTITLEMENT_RECORD_ID,SERIAL_NO,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,CPS_CONFIGURATION_ID,EQUIPMENT_LINE_ID,'{datetimenow}', '{username}', {userid}, {userid}, '{datetimenow}' );""".format(rec=quoteid, datetimenow=datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"), userid=userId, username=userName, revision_rec_id = self.quote_revision_record_id)
					
				#     Sql.RunQuery(QueryStatement)
				#     QueryStatement ="""
				#     MERGE SAQIEN SRC USING (SELECT A.ENTITLEMENT_XML,B.PART_NUMBER,B.PART_RECORD_ID,B.LINE_ITEM_ID,A.QUOTE_ID,B.QUOTE_ITEM_FORECAST_PART_RECORD_ID,B.QTEITM_RECORD_ID,A.QUOTE_RECORD_ID,A.QTEREV_RECORD_ID,A.QUOTE_SERVICE_ENTITLEMENT_RECORD_ID,A.SERVICE_DESCRIPTION,A.SERVICE_ID,A.SERVICE_RECORD_ID,A.SALESORG_ID,A.SALESORG_NAME,A.SALESORG_RECORD_ID,A.CPS_CONFIGURATION_ID,B.PART_LINE_ID FROM SAQTSE(NOLOCK) A JOIN SAQIFP (NOLOCK) B ON A.QUOTE_RECORD_ID  = B.QUOTE_RECORD_ID AND A.QTEREV_RECORD_ID = B.QTEREV_RECORD_ID AND A.SALESORG_ID =B.SALESORG_ID where A.QUOTE_RECORD_ID = '{rec}'  AND A.QTEREV_RECORD_ID  = '{revision_rec_id}' )
				#     TGT ON (SRC.QUOTE_RECORD_ID = TGT.QUOTE_RECORD_ID AND SRC.QTEREV_RECORD_ID = TGT.QTEREV_RECORD_ID AND SRC.SERVICE_ID = TGT.SERVICE_ID AND SRC.EQUIPMENT_ID = TGT.PART_NUMBER) 
				#     WHEN MATCHED THEN UPDATE SET SRC.ENTITLEMENT_XML = TGT.ENTITLEMENT_XML
				#     WHEN NOT MATCHED BY TARGET THEN INSERT(QUOTE_ITEM_COVERED_OBJECT_ENTITLEMENTS_RECORD_ID,ENTITLEMENT_XML,EQUIPMENT_ID,EQUIPMENT_RECORD_ID,LINE_ITEM_ID,QUOTE_ID,QTEITM_RECORD_ID,QUOTE_RECORD_ID,QTEREV_RECORD_ID,QTESRVENT_RECORD_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,CPS_CONFIGURATION_ID,EQUIPMENT_LINE_ID,CPQTABLEENTRYDATEADDED, CPQTABLEENTRYADDEDBY, ADDUSR_RECORD_ID, CpqTableEntryModifiedBy,CpqTableEntryDateModified) VALUES (NEWID(),ENTITLEMENT_XML,PART_NUMBER,PART_RECORD_ID,LINE_ITEM_ID,QUOTE_ID,QTEITM_RECORD_ID,QUOTE_RECORD_ID,QTEREV_RECORD_ID,QUOTE_SERVICE_ENTITLEMENT_RECORD_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,CPS_CONFIGURATION_ID,PART_LINE_ID,'{datetimenow}', '{username}', {userid}, {userid}, '{datetimenow}' );""".format(rec=quoteid, datetimenow=datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"), userid=userId, username=userName, revision_rec_id = self.quote_revision_record_id)
				#     Sql.RunQuery(QueryStatement)
				
				#Trace.Write("getnameentallowed"+str(getnameentallowed))
				getnameentallowed = [i.replace('_00','') if '_00' in i else i.replace('_00','_0') if '_0' else i  for i in getnameentallowed ]
				totaldisallowlist = [item for item in attributesdisallowedlst if item not in getnameentallowed]	
				#Trace.Write("totaldisallowlist"+str(totaldisallowlist))	
		elif EntitlementType == "NO_ENTITLEMENT":
			ent_temp = ''
			sec_str = getvaludipto = getvaludipt1 = getvaludipt2 = getvaludipt2lt = getvaludipt2lab = getvaludipto_q = getvaludipt2_q = getvaludipt2lt_q = getvaludipt2lab_q = getvaludipt2lab = getvaludipt3lab = getvaludipt3lab_q = getvaludipt3labt = getvaludipt3labt_q= getvaludipt1_q=  getlabortype_calc = gett1labor_calc= gett1labortype_calc =gett2labo_calc = gett2labotype_calc = gett3lab_calc = gett3labtype_calc = ""
			multi_select_attr_list = {}
			getnameentallowed = []
			sec_str_cf = sec_str_boot = sec_bnr = sec_str_primp =  ""
			#sec_str = "Entitlements are not applicable at this level"
			sec_str = "<div class='noRecDisp'>Entitlements are not applicable at this level</div>"
		else:
			getnameentallowed = []
			multi_select_attr_list = {}
			attributedefaultvalue = []
			Trace.Write("after inserting in table")
			#Trace.Write('after inserting in table---ObjectName-----'+str(ObjectName))
			#Trace.Write('after inserting in table---where-----'+str(where))
			inserted_value_dict = {}
			#temp_table_dyn = Sql.GetFirst("sp_executesql @T=N' create table entl_tmp (entitlement_id varchar(100))'")
			get_c4c_quote_id = Sql.GetFirst("select * from SAQTMT where MASTER_TABLE_QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(quoteid,self.quote_revision_record_id))
			ent_temp = "ENT_BKP_"+str(get_c4c_quote_id.C4C_QUOTE_ID)
			ent_temp_drop = Sql.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(ent_temp)+"'' ) BEGIN DROP TABLE "+str(ent_temp)+" END  ' ")
			where_cond = where.replace("'","''")
			Trace.Write('where_cond---787--'+str(where_cond))
			Sql.GetFirst("sp_executesql @T=N'declare @H int; Declare @val Varchar(MAX);DECLARE @XML XML; SELECT @val = FINAL from(select  REPLACE(entitlement_xml,''<QUOTE_ITEM_ENTITLEMENT>'',sml) AS FINAL FROM (select ''  <QUOTE_ITEM_ENTITLEMENT><QUOTE_ID>''+quote_id+''</QUOTE_ID><QUOTE_RECORD_ID>''+QUOTE_RECORD_ID+''</QUOTE_RECORD_ID><QTEREV_RECORD_ID>''+QTEREV_RECORD_ID+''</QTEREV_RECORD_ID><SERVICE_ID>''+service_id+''</SERVICE_ID>'' AS sml,replace(replace(replace(replace(replace(replace(replace(replace(ENTITLEMENT_XML,''&'','';#38''),'''','';#39''),'' < '','' &lt; '' ),'' > '','' &gt; '' ),''_>'',''_&gt;''),''_<'',''_&lt;''),''&'','';#38''),''<10%'',''&lt;10%'')  as entitlement_xml from "+str(ObjectName)+"(nolock)  WHERE "+str(where_cond)+"  )A )a SELECT @XML = CONVERT(XML,''<ROOT>''+@VAL+''</ROOT>'') exec sys.sp_xml_preparedocument @H output,@XML; select QUOTE_ID,QUOTE_RECORD_ID,QTEREV_RECORD_ID,SERVICE_ID,ENTITLEMENT_ID,ENTITLEMENT_NAME,ENTITLEMENT_COST_IMPACT,ENTITLEMENT_PRICE_IMPACT,CALCULATION_FACTOR,ENTITLEMENT_TYPE,ENTITLEMENT_VALUE_CODE,ENTITLEMENT_DISPLAY_VALUE,IS_DEFAULT INTO "+str(ent_temp)+"  from openxml(@H, ''ROOT/QUOTE_ITEM_ENTITLEMENT'', 0) with (QUOTE_ID VARCHAR(100) ''QUOTE_ID'',QUOTE_RECORD_ID VARCHAR(100) ''QUOTE_RECORD_ID'',QTEREV_RECORD_ID VARCHAR(100) ''QTEREV_RECORD_ID'',ENTITLEMENT_NAME VARCHAR(100) ''ENTITLEMENT_NAME'',ENTITLEMENT_ID VARCHAR(100) ''ENTITLEMENT_ID'',SERVICE_ID VARCHAR(100) ''SERVICE_ID'',ENTITLEMENT_COST_IMPACT VARCHAR(100) ''ENTITLEMENT_COST_IMPACT'',ENTITLEMENT_PRICE_IMPACT VARCHAR(100) ''ENTITLEMENT_PRICE_IMPACT'',CALCULATION_FACTOR VARCHAR(100) ''CALCULATION_FACTOR'',ENTITLEMENT_TYPE VARCHAR(100) ''ENTITLEMENT_TYPE'',ENTITLEMENT_VALUE_CODE VARCHAR(100) ''ENTITLEMENT_VALUE_CODE'',ENTITLEMENT_DISPLAY_VALUE VARCHAR(100) ''ENTITLEMENT_DISPLAY_VALUE'',IS_DEFAULT VARCHAR(100) ''IS_DEFAULT'') ; exec sys.sp_xml_removedocument @H; '")

			GetXMLsecField=Sql.GetList("SELECT * FROM {} ".format(ent_temp))
			#getinnercon  = Sql.GetFirst("select QUOTE_RECORD_ID,QTEREV_RECORD_ID,convert(xml,replace(replace(replace(replace(replace(replace(ENTITLEMENT_XML,'&',';#38'),'''',';#39'),' < ',' &lt; ' ),' > ',' &gt; ' ),'_>','_&gt;'),'_<','_&lt;')) as ENTITLEMENT_XML from "+str(ObjectName)+" (nolock)  where  "+str(where)+"")
			#GetXMLsecField = Sql.GetList("SELECT distinct e.QUOTE_RECORD_ID,e.QTEREV_RECORD_ID, replace(X.Y.value('(ENTITLEMENT_NAME)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_NAME,replace(X.Y.value('(ENTITLEMENT_ID)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_ID,replace(X.Y.value('(IS_DEFAULT)[1]', 'VARCHAR(128)'),';#38','&') as IS_DEFAULT,replace(X.Y.value('(ENTITLEMENT_COST_IMPACT)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_COST_IMPACT,replace(X.Y.value('(CALCULATION_FACTOR)[1]', 'VARCHAR(128)'),';#38','&') as CALCULATION_FACTOR,replace(X.Y.value('(ENTITLEMENT_PRICE_IMPACT)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_PRICE_IMPACT,replace(X.Y.value('(ENTITLEMENT_TYPE)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_TYPE,replace(X.Y.value('(ENTITLEMENT_VALUE_CODE)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_VALUE_CODE,replace(replace(replace(replace(X.Y.value('(ENTITLEMENT_DESCRIPTION)[1]', 'VARCHAR(128)'),';#38','&'),';#39',''''),'&lt;','<' ),'&gt;','>') as ENTITLEMENT_DESCRIPTION,replace(replace(replace(replace(X.Y.value('(ENTITLEMENT_DISPLAY_VALUE)[1]', 'VARCHAR(128)'),';#38','&'),';#39',''''),'_&lt;','_<' ),'_&gt;','_>') as ENTITLEMENT_DISPLAY_VALUE FROM (select '"+str(getinnercon.QUOTE_RECORD_ID)+"' as QUOTE_RECORD_ID,'"+str(getinnercon.QTEREV_RECORD_ID)+"' as QTEREV_RECORD_ID,convert(xml,'"+str(getinnercon.ENTITLEMENT_XML)+"') as ENTITLEMENT_XML ) e OUTER APPLY e.ENTITLEMENT_XML.nodes('QUOTE_ITEM_ENTITLEMENT') as X(Y) ")
			for val in GetXMLsecField:
				inserted_value_dict[val.ENTITLEMENT_ID] = val.ENTITLEMENT_VALUE_CODE
			inserted_value_list = [val.ENTITLEMENT_ID for val in GetXMLsecField if GetXMLsecField]
			Trace.Write(str(ProductPartnumber)+'----766---ObjectName-----'+str(overallattributeslist_visible))
			#if ProductPartnumber == 'Z0046':
				#inserted_value_list.append('AGS_Z0046_PQB_APPLCN')
			Trace.Write(str(inserted_value_list)+'----802-----overallattributeslist_visible----'+str(overallattributeslist_visible))
			#if self.treeparam == "Quote Items":
				#get_attr_leve_based_list = overallattributeslist_visible
			#else:
			get_attr_leve_based_list = ScriptExecutor.ExecuteGlobal("CQENTLNVAL", {'where_cond':where,'partnumber':ProductPartnumber,'ent_level_table':ObjectName,'inserted_value_list':inserted_value_list,'action':'get_from_prenli'})
			
			Trace.Write('---766---get_attr_leve_based_list-----'+str(list(get_attr_leve_based_list)))
			for val in GetXMLsecField:
				#Trace.Write(str(val.ENTITLEMENT_NAME)+'--ENT___NAME---2908----'+str(val.IS_DEFAULT))
				if val.IS_DEFAULT == '1':
					#Trace.Write(str(val.ENTITLEMENT_NAME)+'--2910------'+str(val.IS_DEFAULT))
					attributedefaultvalue.append(val.ENTITLEMENT_ID)
			#Trace.Write('attributedefaultvalue--2912----2912---'+str(attributedefaultvalue))
			sec_str_cf = sec_str_boot = sec_bnr = sec_str_primp =  ""		
			## set entitlement_xml for cancel fn A055S000P01-3157 starts
			previous_entitlement_xml  = Sql.GetFirst("select ENTITLEMENT_XML from "+str(ObjectName)+" (nolock)  where  "+str(where)+"")	
			#Trace.Write('previous_entitlement_xml----'+str(previous_entitlement_xml))	
			Product.SetGlobal("previous_entitlement_xml", previous_entitlement_xml.ENTITLEMENT_XML)
			## set entitlement_xml for cancel fn A055S000P01-3157 ends
			list_of_tabs = []
			getprevdicts +=   ("var dict_new = {};var list_new = [];")	
			if str(self.treeparentparam).upper() == "ADD-ON PRODUCTS":
				self.treesuperparentparam = ""
			Trace.Write('self.treeparam----'+str(self.treeparam)+'--'+str(ProductPartnumber))
			if self.treeparam.upper() == ProductPartnumber or self.treeparentparam.upper() == ProductPartnumber or self.treesuperparentparam == ProductPartnumber or self.treeparam in ("Quote Items",'Add-On Products' ) :	
				#Trace.Write("@2756------->"+str(self.treeparentparam))
				
				for product_tab_obj in product_tabs_obj:
					product_section =   str(product_tab_obj.TAB_CODE)+'_'+ str(product_tab_obj.TAB_NAME)
					#Trace.Write("product_tab_obj"+str(product_section))
					tablistdict = {}
					date_boot_field = []
					list_of_tabs.append(product_section)
					if str(self.treeparentparam).upper() == "ADD-ON PRODUCTS":
						sysectObj = Sql.GetFirst(
							"SELECT RECORD_ID,SECTION_DESC,SECTION_NAME FROM SYSECT (NOLOCK) WHERE SECTION_NAME='" + str(product_section) + "' AND SECTION_PARTNUMBER = '" + str(self.treeparam.upper()) + "'"
						)
					else:
						sysectObj = Sql.GetFirst(
						"SELECT RECORD_ID,SECTION_DESC,SECTION_NAME FROM SYSECT (NOLOCK) WHERE SECTION_NAME='" + str(product_section) + "'"
					)
					
					if sysectObj and str(sysectObj.SECTION_NAME) == str(product_section):
						Section_id = sysectObj.RECORD_ID
						Section_desc = sysectObj.SECTION_DESC.split('_')
						Section_desc = sysectObj.SECTION_DESC.split('_')[len(Section_desc) - 1]
					else:
						get_last_secid = Sql.GetFirst("select max(SAPCPQ_ATTRIBUTE_NAME) as saprec_id from sysect where SAPCPQ_ATTRIBUTE_NAME like '%SYSECT-QT%'")
						if get_last_secid:
							get_last_secid = get_last_secid.saprec_id.split('-')[2]
							get_last_secid = int(int(get_last_secid)) + 1
							get_lastsection_val = 'SYSECT-QT-'+ str(get_last_secid)
							getsect_tab = Sql.GetTable("SYSECT")
							tbrowsect = {}
							Section_id = tbrowsect['RECORD_ID'] = str(Guid.NewGuid()).upper()
							tbrowsect['SAPCPQ_ATTRIBUTE_NAME'] = get_lastsection_val
							tbrowsect['SECTION_DESC'] =  str(product_section) 
							tbrowsect['SECTION_NAME'] =  str(product_section)
							tbrowsect['SECTION_PARTNUMBER'] =  self.treeparam.upper()
							tbrowsect['PARENT_SECTION_TEXT'] = product_tab_obj.SYSTEM_ID
							getsect_tab.AddRow(tbrowsect)
							Sql.Upsert(getsect_tab)
							Section_desc = product_section.split('_')
							Section_desc =product_section.split('_')[len(Section_desc) - 1]

					if EntitlementType in ("EQUIPMENT","BUSINESSUNIT","TOOLS"):
						#Trace.Write("@@2794")
						sec_bnr += (
							'<div class="dyn_main_head master_manufac glyphicon pointer  glyphicon-chevron-down " id="'
							+ str(Section_id)+ '" onclick="dyn_main_sec_collapse_arrow(this)" data-target="#sec_'
							+ str(Section_id)
							+ '" data-toggle="collapse"><label class="onlytext"><label class="onlytext"><div><div id="ctr_drop" class="btn-group dropdown"><div class="dropdown"><i data-toggle="dropdown" class="fa fa-sort-desc dropdown-toggle"></i><ul class="dropdown-menu left" aria-labelledby="dropdownMenuButton"><li class="edit_list"><a id="'
							+ str(Section_id)
							+ '" class="dropdown-item" href="#" onclick="edit_entitlement(this)">EDIT</a></li></ul></div></div>'
							+ str(Section_desc)
							+ "</div></label></div>"
						)
					else:					
						sec_bnr += (
							'<div class="dyn_main_head master_manufac glyphicon pointer  glyphicon-chevron-down" onclick="dyn_main_sec_collapse_arrow(this)" id="'+ str(Section_id)+ '" data-target="#sec_'
							+ str(Section_id)
							+ '" data-toggle="collapse"><label class="onlytext"><label class="onlytext"><div>'
							+ str(Section_desc)
							+ "</div></label></div>"
						)
					
					sec_str_boot += ('<div id="sec_'+str(Section_id)+ '" class="dyn_main_head master_manufac glyphicon pointer   glyphicon-chevron-down margtop10 " onclick="dyn_main_sec_collapse_arrow(this)" data-target="#sc_'+ str(Section_id)+ '" data-toggle="collapse" <label class="onlytext"><label class="onlytext"><div>'+ str(Section_desc).upper()+ '</div></label></div><div id="sc_'+str(Section_id)+ '" class="collapse in entitle_select_out"><table id="' + str(Section_id)+ '" class= "getentdata" data-filter-control="true" data-maintain-selected="true" data-locale = "en-US" data-escape="true" data-html="true"  data-show-header="true" > <thead><tr class="hovergrey">')
					for key, invs in enumerate(list(desc_list)):
						invs = str(invs).strip()
						qstring = attr_dict.get(str(invs)) or ""
						if invs == 'REQUIRED':
							required_symbol_class = 'class ="required_symbol"'
						else:
							required_symbol_class = ""
						sec_str_boot += (
							'<th '+str(required_symbol_class)+' data-field="'
							+ invs
							+ '" data-title-tooltip="'
							+ str(qstring)
							+ '" >'
							+ str(qstring)
							+ "</th>"
						)
					sec_str_boot += '</tr></thead><tbody onclick="Table_Onclick_Scroll(this)" ></tbody></table>'
					sec_str_boot += ('<div id = "btn_ent" class="g4  except_sec removeHorLine iconhvr sec_edit_sty" style="display: none;"><button id="entcancel" class="btnconfig btnMainBanner sec_edit_sty_btn"  onclick="fabcostlocatecancel(this)" style="display: none;" class="btnconfig">CANCEL</button><button id="entsave" class="btnconfig btnMainBanner sec_edit_sty_btn"  onclick="fabcostlocatesave(this)" style="display: none;" class="btnconfig">SAVE</button></div>')

					add_style = ""
					attributes_disallowed_list = []
					attribute_Name_list = []
					get_tab_attr_length =""
					tab_get_disallow_list =[]
					if tabwise_product_attributes.get(product_tab_obj.TAB_PROD_ID):
						Trace.Write("tabwise_product_attributes.get(product_tab_obj.TAB_PROD_ID)"+str(tabwise_product_attributes.get(product_tab_obj.TAB_PROD_ID)))
						get_tab_attr_length = len(tabwise_product_attributes.get(product_tab_obj.TAB_PROD_ID))
						for attribute in tabwise_product_attributes.get(product_tab_obj.TAB_PROD_ID):
							get_tooltip = ""
							sec_validation = ""
							new_value_dicta = {}
							attrName = attribute['attribute_name']
							attrLabel = attribute['attribute_label']
							attrSysId = attribute['attribute_system_id']
							attribute_code = attribute['attribute_code']

							#Trace.Write('attrSysId---looping0507--'+str(attrSysId))
							STDVALUES = Sql.GetFirst("""SELECT TOP 100 A.PA_ID, A.PAV_ID, A.STANDARD_ATTRIBUTE_VALUE_CD, A.STANDARD_ATTRIBUTE_PRICE, A.NON_STANDARD_VALUE, A.NON_STANDARD_DISPLAY_VALUE, 
							A.PRODUCT_ATT_IMAGE_OFF_ALT_TEXT, A.SORT_RANK, A.RELATED_PRODUCT_ID

							, COALESCE(P.PRODUCT_CATALOG_CODE, A.VALUE_CATALOG_CODE) VALUE_CATALOG_CODE

							, PA.STANDARD_ATTRIBUTE_CODE, PA.ATTRDESC,COALESCE(P.PRODUCT_NAME, V.STANDARD_ATTRIBUTE_DISPLAY_VAL) STANDARD_ATTRIBUTE_DISPLAY_VAL,V.SYSTEM_ID , V.STANDARD_ATTRIBUTE_VALUE, V.SYSTEM_ID AS VALUE_SYSTEM_ID, V.UNIT_ID AS VALUE_UNIT_ID, V.BILLING_PERIOD_ID AS VALUE_BILLING_PERIOD_ID
							, PA.USEALTERNATIVEPRICINGFORPRODUCTSINCONTAINER
							, COALESCE(P_ML.PRODUCT_NAME, P.PRODUCT_NAME, STDML.STANDARD_ATTRIBUTE_DISPLAY_VAL, V.STANDARD_ATTRIBUTE_DISPLAY_VAL) AS ML_NON_STANDARD_DISPLAY_VALUE
							FROM PRODUCT_ATTRIBUTES PA INNER JOIN ATTRIBUTES A ON PA.PA_ID=A.PA_ID 
							INNER JOIN STANDARD_ATTRIBUTE_VALUES V ON A.STANDARD_ATTRIBUTE_VALUE_CD = V.STANDARD_ATTRIBUTE_VALUE_CD  
							LEFT OUTER JOIN PRODUCTS P ON A.RELATED_PRODUCT_ID=P.PRODUCT_ID 
							LEFT OUTER JOIN PRODUCTS_ML P_ML ON P.PRODUCT_ID=P_ML.PRODUCT_ID AND P_ML.ML_ID=0
							LEFT JOIN  ATTRIBUTES_ML ML ON A.PAV_ID=ML.PAV_ID AND ML.ML_ID= 0
							LEFT JOIN STANDARD_ATTRIBUTE_VALUES_ML STDML ON A.STANDARD_ATTRIBUTE_VALUE_CD=STDML.STANDARD_ATTRIBUTE_VALUE_CD AND STDML.ML_ID=0 LEFT OUTER JOIN test_USD_L1 ON COALESCE(P.PRODUCT_CATALOG_CODE, A.VALUE_CATALOG_CODE) = test_USD_L1.PARTNUMBER AND ISNULL(A.PRICINGCODE, '')=ISNULL(test_USD_L1.PRICECODE, '') 
							WHERE PA.PRODUCT_ID ={productId} AND V.STANDARD_ATTRIBUTE_CODE  = {sys_id} ORDER BY A.SORT_RANK""".format(sys_id = attribute_code,productId = str(product_obj.PRD_ID)))
							#STDVALUES =  Sql.GetFirst("SELECT * from STANDARD_ATTRIBUTE_VALUES  where  STANDARD_ATTRIBUTE_CODE = {sys_id} ".format(sys_id = attribute_code)  )
							if STDVALUES:
								attrValue = STDVALUES.STANDARD_ATTRIBUTE_DISPLAY_VAL
								get_tooltip = STDVALUES.ATTRDESC
								#get_tooltip = get_tooltip.encode('ascii', 'ignore').decode('ascii')
							else:
								attrValue = get_tooltip = ''
							#Trace.Write('get_tooltip----'+str(get_tooltip))
							attribute_Name_list.append(attrSysId)
							DType = attribute['attribute_dtype']
							#Trace.Write("attrSysId --3109---"+str(attrSysId) + " attrName_else_j "+str(attrName)+ " || "+str(attributedefaultvalue)+"attrSysId__else_j "+str(attributesdisallowedlst)+" attributesdisallowedlst_else_j")
							if attrSysId in attributesdisallowedlst:
								if attrSysId in attributedefaultvalue:
									add_style = "display:none;"
								else:
									add_style = "color:#1B78D2"
								attributes_disallowed_list.append(attrSysId)
							else:
								#Trace.Write("attrValue_else_j 2860---attrName_else_j "+str(attrName))
								add_style = ""
							##validation msg
							if attrSysId in validation_dict.keys():
								sec_validation = "Only enter the values in the following range: "+str(validation_dict[attrSysId])+"-0"

							if attrSysId not in attributedefaultvalue:
								#Trace.Write("add_style----3077----- "+str(attrSysId))
								add_style = "color:#1B78D2"
							#Trace.Write('--attributeEditlst-930----'+str(attributeEditlst))
							if attrSysId in attributeEditlst :
								disable_edit = 'disable_edit'
								edit_pencil_icon = '<a href="#" class="editclick"><i title="Double Click to Edit" class="fa fa-pencil"  aria-hidden="true"></i></a>'
								
							else:
								disable_edit = ''
								edit_pencil_icon = '<a href="#" class="editclick"><i title="Double Click to Edit" class="fa fa-lock"  aria-hidden="true"></i></a>'
							attrValueSysId = attributevalues.get(attrSysId)
							##info tooltip adding in entitlement grid starts..
							# info_column = '''<a   data-placement="auto top" data-trigger="focus"  class="bgcccwth10"><i title="{value}" class="fa fa-info-circle fltlt"></i></a>'''.format(value= get_tooltip)
							##info tooltip adding in entitlement grid ends..
							disp_val = ""
							userselectedvalue = []
							#for val in GetXMLsecField:
							
							#userselectedvalue = [val.ENTITLEMENT_DESCRIPTION for val in GetXMLsecField if GetXMLsecField]
							sec_str_cf =sec_str_imt =  dataent = factcurreny = decimal_place = value1234 = sec_str_dt = sec_str_faccur = sec_str_faccur = costimpact = sec_str_primp = priceimp =  sec_str_ipp = ""
							imgstr =""
							#Trace.Write("inserted_value_list--"+str(inserted_value_list))
							standard_attr_values = Sql.GetList("""SELECT TOP 50 A.PA_ID, A.PAV_ID, A.STANDARD_ATTRIBUTE_VALUE_CD, A.STANDARD_ATTRIBUTE_PRICE, A.NON_STANDARD_VALUE, A.NON_STANDARD_DISPLAY_VALUE, 
										A.PRODUCT_ATT_IMAGE_OFF_ALT_TEXT, A.SORT_RANK, A.RELATED_PRODUCT_ID

										, COALESCE(P.PRODUCT_CATALOG_CODE, A.VALUE_CATALOG_CODE) VALUE_CATALOG_CODE

										, PA.STANDARD_ATTRIBUTE_CODE, COALESCE(P.PRODUCT_NAME, V.STANDARD_ATTRIBUTE_DISPLAY_VAL) STANDARD_ATTRIBUTE_DISPLAY_VAL, V.SYSTEM_ID,V.STANDARD_ATTRIBUTE_VALUE, V.SYSTEM_ID AS VALUE_SYSTEM_ID, V.UNIT_ID AS VALUE_UNIT_ID, V.BILLING_PERIOD_ID AS VALUE_BILLING_PERIOD_ID
										, PA.USEALTERNATIVEPRICINGFORPRODUCTSINCONTAINER
										, COALESCE(P_ML.PRODUCT_NAME, P.PRODUCT_NAME, STDML.STANDARD_ATTRIBUTE_DISPLAY_VAL, V.STANDARD_ATTRIBUTE_DISPLAY_VAL) AS ML_NON_STANDARD_DISPLAY_VALUE
										FROM PRODUCT_ATTRIBUTES PA INNER JOIN ATTRIBUTES A ON PA.PA_ID=A.PA_ID 
										INNER JOIN STANDARD_ATTRIBUTE_VALUES V ON A.STANDARD_ATTRIBUTE_VALUE_CD = V.STANDARD_ATTRIBUTE_VALUE_CD  
										LEFT OUTER JOIN PRODUCTS P ON A.RELATED_PRODUCT_ID=P.PRODUCT_ID 
										LEFT OUTER JOIN PRODUCTS_ML P_ML ON P.PRODUCT_ID=P_ML.PRODUCT_ID AND P_ML.ML_ID=0
										LEFT JOIN  ATTRIBUTES_ML ML ON A.PAV_ID=ML.PAV_ID AND ML.ML_ID= 0
										LEFT JOIN STANDARD_ATTRIBUTE_VALUES_ML STDML ON A.STANDARD_ATTRIBUTE_VALUE_CD=STDML.STANDARD_ATTRIBUTE_VALUE_CD AND STDML.ML_ID=0 LEFT OUTER JOIN test_USD_L1 ON COALESCE(P.PRODUCT_CATALOG_CODE, A.VALUE_CATALOG_CODE) = test_USD_L1.PARTNUMBER AND ISNULL(A.PRICINGCODE, '')=ISNULL(test_USD_L1.PRICECODE, '') 
										WHERE PA.PRODUCT_ID ={productId} AND V.STANDARD_ATTRIBUTE_CODE  = {sys_id} ORDER BY A.SORT_RANK""".format(sys_id = attribute_code,productId = str(product_obj.PRD_ID)))
							if GetXMLsecField and attrSysId in get_attr_leve_based_list:
								# entitlement_display_value = [i.ENTITLEMENT_DISPLAY_VALUE for i in GetXMLsecField]
								# Trace.Write('entitlement_display_value'+str(entitlement_display_value))
								for val in GetXMLsecField:
									try:
										val.ENTITLEMENT_DISPLAY_VALUE = val.ENTITLEMENT_DISPLAY_VALUE.replace(';#38','&').replace("_&lt;","_<").replace("_&gt;","_>").replace(" &gt; "," > ").replace(" &lt; "," < ").replace(';#39',"'").replace('&lt;10%',"<10%")
									except:
										pass
									try:
										val.ENTITLEMENT_DESCRIPTION = val.ENTITLEMENT_DESCRIPTION.replace(';#38','&').replace("_&lt;","_<").replace("_&gt;","_>").replace(" &gt; "," > ").replace(" &lt; "," < ").replace(';#39',"'").replace('&lt;10%',"<10%")
									except:
										pass
									val.ENTITLEMENT_NAME = val.ENTITLEMENT_NAME.replace(';#38','&').replace("_&lt;","_<").replace("_&gt;","_>").replace(" &gt; "," > ").replace(" &lt; "," < ").replace(';#39',"'").replace('&lt;10%',"<10%")
									try:
										val.ENTITLEMENT_VALUE_CODE = val.ENTITLEMENT_VALUE_CODE.replace(';#38','&').replace("_&lt;","_<").replace("_&gt;","_>").replace(" &gt; "," > ").replace(" &lt; "," < ").replace(';#39',"'").replace('&lt;10%',"<10%")
									except:
										pass
									#imgstr = ""
									userselectedvalue.append(val.ENTITLEMENT_NAME)
									#getnameentallowed.append(val.ENTITLEMENT_NAME)
									#Trace.Write("ENTITLEMENT_NAME_else_j "+str(val.ENTITLEMENT_NAME) +" || attrSysId "+str(attrSysId))
									# if  str(attrSysId) == val.ENTITLEMENT_NAME:
									#disp_val = str(val.ENTITLEMENT_DISPLAY_VALUE)
									#Trace.Write(str(attrName)+"dtype--959-----before if"+str(DType))
									
									if DType == "Drop Down":
										
										#Trace.Write(str(attrName)+'------963--'+str(val.ENTITLEMENT_NAME))
										#STDVALUES =  Sql.GetList("SELECT * from STANDARD_ATTRIBUTE_VALUES where  SYSTEM_ID like '%{sys_id}%' and STANDARD_ATTRIBUTE_CODE = '{attr_code}' ".format(sys_id = str(attrSysId), attr_code = attribute_code )  )
										
										
										
										
										if standard_attr_values and val.ENTITLEMENT_ID == str(attrSysId): 
											VAR1 = sec_str1 = ""
											selected_option = "Select"
											if str(val.ENTITLEMENT_DISPLAY_VALUE).strip() != "":
												default = ''
											else:
												default = 'selected'

											Trace.Write(str(attrSysId)+'--attrSysId----'+str(val.ENTITLEMENT_ID)+'-----982------>'+str(val.ENTITLEMENT_DISPLAY_VALUE))
											
											Trace.Write(str(attributes_disallowed_list)+'---dropdowndisallowlist----'+str(dropdowndisallowlist))
											VAR1 += '<option value="select" ' +str(default)+' style= "display:none;"> </option>'
											for value in standard_attr_values:
												if value.SYSTEM_ID in dropdowndisallowlist:
													
													disallow_style = "style = 'display:none'"
												else:	
													disallow_style = ""
												try:
													
													if str(val.ENTITLEMENT_DISPLAY_VALUE).strip().upper() == str(value.STANDARD_ATTRIBUTE_DISPLAY_VAL).strip().upper():
														Trace.Write('drpppppp---3031-------'+str(val.ENTITLEMENT_DISPLAY_VALUE)+'--1028--'+str(value.STANDARD_ATTRIBUTE_DISPLAY_VAL))
														approval_status = Sql.GetFirst("SELECT APPROVAL_REQUIRED FROM PRENVL WHERE ENTITLEMENT_ID = '{}' AND ENTITLEMENT_DISPLAY_VALUE = '{}'".format(str(attrSysId),str(val.ENTITLEMENT_DISPLAY_VALUE).replace("'","''")) )
														if approval_status:
															#Trace.Write("imgstr--1-"+str(approval_status.APPROVAL_REQUIRED))
															if approval_status.APPROVAL_REQUIRED == True:
																imgstr = '<img title=Acquired src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/clock_exe.svg>'
															
														
														selected_option = str(val.ENTITLEMENT_DISPLAY_VALUE)
														VAR1 += (
															'<option  id="'+str(value.SYSTEM_ID)+'" value = "'
															+ str(val.ENTITLEMENT_DISPLAY_VALUE)
															+ '" selected>'
															+ str(val.ENTITLEMENT_DISPLAY_VALUE)
															+ "</option>"
														)
														Trace.Write('selected_option--'+str(selected_option))
													else:
														Trace.Write(str(disallow_style)+'--disallow_style----'+'-----default----'+str(default)+'----1032---'+str(disallow_style)+'---disallow_style--1025--'+str(value.STANDARD_ATTRIBUTE_DISPLAY_VAL)+'drpppppp---3031---3342-----'+str(attrName))
														VAR1 += (
															'<option '
															+ str(disallow_style)
															+ ' id="'+str(value.SYSTEM_ID)+'" value = "'
															+ str(value.STANDARD_ATTRIBUTE_DISPLAY_VAL)
															+ '">'
															+ str(value.STANDARD_ATTRIBUTE_DISPLAY_VAL)
															+ "</option>"
														)
												except:
													#Trace.Write(str(default)+'----except dropdown ----'+str(attrName)+'--1043--')
													#VAR1 = '<option value="select" ' +str(default)+'  style="display;none;"> </option>'
													if val.ENTITLEMENT_DISPLAY_VALUE == value.STANDARD_ATTRIBUTE_DISPLAY_VAL:
														selected_option = val.ENTITLEMENT_DISPLAY_VALUE
														#Trace.Write(str(selected_option)+'---selected_option---except dropdown ----'+str(attrName))
														approval_status = Sql.GetFirst("SELECT APPROVAL_REQUIRED FROM PRENVL WHERE ENTITLEMENT_ID = '{}' AND ENTITLEMENT_DISPLAY_VALUE = '{}'".format(str(attrSysId),str(val.ENTITLEMENT_DISPLAY_VALUE).replace("'","''")) )
														if approval_status:
															if approval_status.APPROVAL_REQUIRED == True:
																imgstr = ('<img title=Acquired src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/clock_exe.svg>')
														VAR1 += (
															'<option  id="'+str(value.SYSTEM_ID)+'" value = "{value}" selected>{value}</option>'.format(value= val.ENTITLEMENT_DISPLAY_VALUE)
														)
														#Trace.Write(str(selected_option)+'---selected_option---except dropdown ----'+str(attrName))
													else:
														VAR1 += (
															'<option '
															+ str(disallow_style)
															+ ' id="'+str(value.SYSTEM_ID)+'" value = "{value}">{value}</option>'.format(value= value.STANDARD_ATTRIBUTE_DISPLAY_VAL)
														)

											try:
												if str(attrName) == "Fab Location":
													disable_edit =''
													sec_str1 += (
													'<select class="form-control remove_yellow '+str(disable_edit)+'" style ="'+str(add_style)+'" id = "'
													+ str(attrSysId)
													+ '" type="text"  data-content ="'
													+ str(attrSysId)
													+ '" class="form-control" onchange="editent_bt(this)" title="'+str(selected_option)+'" disabled>'
													+ str(VAR1)
													+ "</select>"
													)
												else:
													sec_str1 += (
													'<select class="form-control remove_yellow '+str(disable_edit)+'" style ="'+str(add_style)+'" id = "'
													+ str(attrSysId)
													+ '" type="text"  data-content ="'
													+ str(attrSysId)
													+ '" class="form-control" onchange="editent_bt(this)" title="'+str(selected_option)+'" disabled>'
													+ str(VAR1)
													+ "</select>"
													)

											except:
												sec_str1 += (
												'<select class="form-control remove_yellow '+str(disable_edit)+'" style ="'+str(add_style)+'" id = "'
												+ str(attrSysId)
												+ '" type="text"  data-content ="'
												+ str(attrSysId)
												+ '" class="form-control" onchange="editent_bt(this)" title="'+str(selected_option)+'" disabled>{}</select>'.format(VAR1)
												)
											
											# if val.ENTITLEMENT_ID == 'AGS_SFM_DEI_PAC' and "Included" in val.ENTITLEMENT_DISPLAY_VALUE:
											# 	sec_str_imt += str(val.ENTITLEMENT_COST_IMPACT)+" "+str(val.PRICE_METHOD)
											# 	sec_str_faccur += ''
											# elif (val.ENTITLEMENT_ID == 'AGS_RFM_INS_T0' or val.ENTITLEMENT_ID == 'AGS_RFM_INS_T1') and "Included" in val.ENTITLEMENT_DISPLAY_VALUE:
											# 	sec_str_imt += str(val.ENTITLEMENT_COST_IMPACT)+" "+str(val.PRICE_METHOD)
											# 	sec_str_faccur += ''
											# elif (val.ENTITLEMENT_ID == 'AGS_RFM_INS_T2' or val.ENTITLEMENT_ID == 'AGS_RFM_INS_T3') and "Included" in val.ENTITLEMENT_DISPLAY_VALUE:
											# 	sec_str_imt += str(val.ENTITLEMENT_COST_IMPACT)+" "+str(val.PRICE_METHOD)
											# 	sec_str_faccur += ''
											#else:
											sec_str_imt += ""
											
											
											""" except Exception, e:
												Trace.Write(str(e)+'error1111')
												sec_str_imt += str(val.ENTITLEMENT_COST_IMPACT) """
											#Trace.Write("CHKNG_STYLE_J "+str(add_style)+" attrSysId "+str(attrSysId))
										

									elif DType == "Check Box" :
										#Trace.Write(str(attrSysId)+'CheckApproval'+str(attrValue))
										
										#STDVALUES =  Sql.GetList("SELECT * from STANDARD_ATTRIBUTE_VALUES where STANDARD_ATTRIBUTE_CODE = '{attr_code}' ".format(attr_code = attribute_code )  )
										if standard_attr_values and val.ENTITLEMENT_ID == str(attrSysId):
											try:
												Trace.Write("ENTITLEMENT_DISPLAY_VALUE--chkbox-"+str(val.ENTITLEMENT_DISPLAY_VALUE))
												display_value_arr = eval(val.ENTITLEMENT_DISPLAY_VALUE)
											except Exception as e:
												Trace.Write('except checkbox'+str(e))
												try:
													display_value_code = str(tuple(eval(val.ENTITLEMENT_VALUE_CODE))).replace(',)',')')
													#Trace.Write('display_value_code'+str(display_value_code))
													display_value_query = Sql.GetList("SELECT * from STANDARD_ATTRIBUTE_VALUES where STANDARD_ATTRIBUTE_CODE = '{attr_code}' and STANDARD_ATTRIBUTE_VALUE in {code} ".format(attr_code = attribute_code,code = display_value_code )  )
													display_value_arr = [i.STANDARD_ATTRIBUTE_DISPLAY_VAL for i in display_value_query]
												except Exception as e:
													Trace.Write('except1'+str(e))
													display_value_arr = str(val.ENTITLEMENT_DISPLAY_VALUE)
											
											multi_select_attr_list[attrSysId] = display_value_arr
											#Trace.Write("multi_select_attr_list"+str(multi_select_attr_list)+'---'+str(display_value_arr))
											VAR1 = sec_str1 = selected_option = ""
											for value in standard_attr_values:
												if value.SYSTEM_ID in dropdowndisallowlist:
													disallow_style = "style = 'display:none'"
												else:	
													disallow_style = ""
												Trace.Write("checkkkkkk---"+str(val.ENTITLEMENT_VALUE_CODE)+"----"+str(value.STANDARD_ATTRIBUTE_VALUE)+str(attrSysId))
												try:
													if not (type(val.ENTITLEMENT_VALUE_CODE) is 'int' or type(val.ENTITLEMENT_VALUE_CODE) is 'float'):
														# value_code = eval(val.ENTITLEMENT_VALUE_CODE)
														value_code = val.ENTITLEMENT_VALUE_CODE.split(',')
													else:
														value_code = val.ENTITLEMENT_VALUE_CODE	
												except:
													value_code = val.ENTITLEMENT_VALUE_CODE
												Trace.Write('value_code'+str(value_code))
												try:
													if value_code and str(value.STANDARD_ATTRIBUTE_VALUE).strip() in value_code:
														#Trace.Write('2620-----ch---'+str(value.STANDARD_ATTRIBUTE_VALUE))
														# getnameentallowed.append(value.STANDARD_ATTRIBUTE_DISPLAY_VAL)
														# Trace.Write("getnameentallowed"+str(getnameentallowed))
														selected_option = str(value.STANDARD_ATTRIBUTE_DISPLAY_VAL)
														VAR1 += (
																'<option  id="'+str(value.SYSTEM_ID)+'" value = "'
																+ str(value.STANDARD_ATTRIBUTE_DISPLAY_VAL)
																+ '" selected>'
																+ str(value.STANDARD_ATTRIBUTE_DISPLAY_VAL)
																+ "</option>"
														)
													elif str(value.STANDARD_ATTRIBUTE_VALUE).strip() not in value_code :
														#Trace.Write(str(val.ENTITLEMENT_DISPLAY_VALUE)+'26211111-----'+str(value.STANDARD_ATTRIBUTE_VALUE))
														VAR1 += (
															'<option '+str(disallow_style)+'  id="'+str(value.SYSTEM_ID)+'" value = "'
															+ str(value.STANDARD_ATTRIBUTE_DISPLAY_VAL)
															+ '">'
															+ str(value.STANDARD_ATTRIBUTE_DISPLAY_VAL)
															+ "</option>"
														)
												except:
													if value_code and str(value.STANDARD_ATTRIBUTE_VALUE).strip() == value_code:
														#Trace.Write('2620-----ch---'+str(value.STANDARD_ATTRIBUTE_VALUE))
														# getnameentallowed.append(value.STANDARD_ATTRIBUTE_DISPLAY_VAL)
														# Trace.Write("getnameentallowed"+str(getnameentallowed))
														selected_option = str(value.STANDARD_ATTRIBUTE_DISPLAY_VAL)
														VAR1 += (
																'<option  id="'+str(value.SYSTEM_ID)+'" value = "'
																+ str(value.STANDARD_ATTRIBUTE_DISPLAY_VAL)
																+ '" selected>'
																+ str(value.STANDARD_ATTRIBUTE_DISPLAY_VAL)
																+ "</option>"
														)
													elif str(value.STANDARD_ATTRIBUTE_VALUE).strip() != value_code :
														#Trace.Write(str(val.ENTITLEMENT_DISPLAY_VALUE)+'26211111-----'+str(value.STANDARD_ATTRIBUTE_VALUE))
														VAR1 += (
															'<option '+str(disallow_style)+'  id="'+str(value.SYSTEM_ID)+'" value = "'
															+ str(value.STANDARD_ATTRIBUTE_DISPLAY_VAL)
															+ '">'
															+ str(value.STANDARD_ATTRIBUTE_DISPLAY_VAL)
															+ "</option>"
														)	
												#Trace.Write('VAR1'+str(attrSysId)+str(value.STANDARD_ATTRIBUTE_VALUE))
											Trace.Write("CHKNG_STYLE_J--- "+str(add_style)+" attrSysId --"+str(attrSysId))
											#Trace.Write("CHKNG_STYLE_J "+str(VAR1)+" attrSysId "+str(attrSysId))
											sec_str1 += (
												'<select class="form-control remove_yellow div_multi_checkbox '+str(disable_edit)+'"  style ="'+str(add_style)+'" id = "'
												+ str(attrSysId)
												+ '" type="text"  data-content ="'
												+ str(attrSysId)
												+ '" class="form-control" onchange="editent_bt(this)" title="'+str(selected_option)+'" disabled>'
												+ str(VAR1)
												+ "</select>"
											)
											#Trace.Write('sec_str1'+str(sec_str1))
									
									
									elif DType == "Free Input, no Matching" :
										#Trace.Write('val.ENTITLEMENT_NAME------'+str(val.ENTITLEMENT_NAME))
										if val.ENTITLEMENT_ID == str(attrSysId):
											sec_str1 = ""
											sec_str_imt = ""
											sec_str_primp =""
											sec_str_cf =""
											sec_str_faccur = ""
											attr_value = val.ENTITLEMENT_DISPLAY_VALUE
											#Trace.Write("DType free1---"+str(attr_value)+str(attrSysId)+str(add_style))
											# Status = Sql.GetFirst("SELECT APPROVAL_REQUIRED FROM PRENVL WHERE ENTITLEMENT_ID = '{}' AND ENTITLEMENT_DISPLAY_VALUE = '{}'".format(str(attrSysId),attrValue))
											# if Status :
											# 	if Status.APPROVAL_REQUIRED == True:
											
											# 		imgstr = ('<img title=Acquired src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/clock_exe.svg>')
											# 	else:
											# 		imgstr  = ""
											# else:
											# 	imgstr  = ""

											if str(attrSysId) in ("AGS_REL_STDATE",'AGS_Z0007_GEN_RELDAT'):
												datepicker = "onclick_datepicker_locdate('" + attrSysId + "')"
												if attrSysId == 'AGS_Z0007_GEN_RELDAT':

													datepicker = "onclick_datepicker('" + attrSysId + "')"
												
												sec_str1 += (
													'<input maxlength="255" class="form-control no_border_bg  datePickerField wth157fltltbrdbt '+str(disable_edit)+'" id = "'
													+ str(attrSysId)
													+ '" type="text"  style ="'+str(add_style)+'"  onclick="'+ str(datepicker)+ '"  data-content ="'
													+ str(attr_value)
													+ '" value = "'+str(attr_value)+'" title="'+str(attr_value)+'"  disabled>'									
													+ "</input> "
												)
												# sec_str1 += (
												# 	'<input class="form-control no_border_bg datePickerField wth157fltltbrdbt '+str(disable_edit)+'" id = "'
												# 	+ str(attrSysId)
												# 	+ '" type="text"   style ="'+str(add_style)+'"  onclick="'+ str(datepicker)+ '" data-content ="'
												# 	+ str(attr_value) 
												# 	+ '" value = "'+str(attr_value)+'" title="'+str(attr_value)+'" onchange="'+ datepicker_onchange+ +'" disabled>'									
												# 	+ "</input> "
												# )
											else:
												if attr_value == "DefaultValue":
													attr_value = ''
												sec_str1 += (
													'<input maxlength="255" class="form-control no_border_bg '+str(disable_edit)+'" id = "'
													+ str(attrSysId)
													+ '" type="text"  style ="'+str(add_style)+'"  data-content ="'
													+ str(attr_value)
													+ '" value = "'+str(attr_value)+'" title="'+str(attr_value)+'" onchange="editent_bt(this)" disabled>'									
													+ "</input> "
												)
											#cost_impact  = val.ENTITLEMENT_COST_IMPACT
											try:
												#Trace.Write("@@3087"+str(attrSysId))
												if val.ENTITLEMENT_COST_IMPACT:
													#Trace.Write("@@3089"+str(val.ENTITLEMENT_COST_IMPACT)+str(val.PRICE_METHOD)+str(attrSysId))
													#sec_str_imt += str("{:,.2f}".format(float(val.ENTITLEMENT_COST_IMPACT)))
													sec_str_imt += str("{:,.2f}".format(float(val.ENTITLEMENT_COST_IMPACT)))
													#sec_str_imt += str("{:,.2f}".format(float(val.ENTITLEMENT_COST_IMPACT))) + " "+val.PRICE_METHOD
													
												# else:
												# 	#Trace.Write("@@3093")
												# 	#sec_str_imt += str("{:,.2f}".format(float(val.ENTITLEMENT_COST_IMPACT)))
												# 	sec_str_imt += 
													
											except Exception as e:
												#Trace.Write(str(e)+'error1111'+str(attrSysId))
												sec_str_imt += str(val.ENTITLEMENT_COST_IMPACT)
											#price_impact = val.ENTITLEMENT_PRICE_IMPACT
											try:
												if val.ENTITLEMENT_PRICE_IMPACT:
													#sec_str_primp += str("{:,.2f}".format(float(val.ENTITLEMENT_PRICE_IMPACT)))
													sec_str_primp += str("{:,.2f}".format(float(val.ENTITLEMENT_PRICE_IMPACT)))
													#sec_str_primp += str("{:,.2f}".format(float(val.ENTITLEMENT_PRICE_IMPACT))) + " "+val.PRICE_METHOD
												# else:
												# 	Trace.Write("else price")
												# 	#sec_str_primp += str("{:,.2f}".format(float(val.ENTITLEMENT_PRICE_IMPACT)))
												# 	sec_str_primp += ""
											except Exception as e: 
												sec_str_primp += str(val.ENTITLEMENT_PRICE_IMPACT)
												#Trace.Write(str(e)+'error2222')
												
											#calc_factor = val.CALCULATION_FACTOR
											sec_str_cf +=str(val.CALCULATION_FACTOR)
											#Trace.Write('sec_str_cf chk ## '+str(sec_str_cf))
											##FACTOR CURRENCY
											sec_str_faccur += ''
											#sec_str_faccur += str(val.PRICE_METHOD)
																			
									if attrSysId in attriburesrequired_list:
										required_symbol_class = str(attrSysId)+' required_symbol'
										get_requiredicon = str("<abbr class='"+str(required_symbol_class)+"' title='"+str(attrName)+"'>*</abbr>")
									else:
										required_symbol_class = get_requiredicon = ""
									new_value_dicta["APPROVAL"] = imgstr
									try:
										new_value_dicta["ENTITLEMENT"] = str("<abbr title='"+str(attrName)+"'>"+str(attrName)+"</abbr>")
									except:
										new_value_dicta["ENTITLEMENT"] = "<abbr title='{entitlement_name}'>{entitlement_name}</abbr>".format(entitlement_name=attrName)
									try:
										new_value_dicta["DESCRIPTION"] = str('<abbr title="'+str(get_tooltip)+'">'+str(get_tooltip)+'</abbr>')
									except:
										new_value_dicta["DESCRIPTION"] = '<abbr title="{get_tooltip}">{get_tooltip}</abbr>'.format(get_tooltip=get_tooltip)
									new_value_dicta["REQUIRED"] = get_requiredicon
									if DType in( "Drop Down", "Check Box", "Free Input, no Matching"):
										new_value_dicta["VALUE"] = sec_str1 									
									else:
										new_value_dicta["VALUE"] = str(sec_str_ipp)
										#Trace.Write("@3323-----"+str(attrSysId))
									new_value_dicta["VALIDATION"]=str("<abbr id ='"+ str(attrSysId)+"'  class = 'wid90_per requ_validation' title='"+str(sec_validation)+"'>"+str(sec_validation)+"</abbr>")+str(edit_pencil_icon)
									new_value_dicta["ENTITLEMENT COST IMPACT"]= str("<abbr title='"+str(sec_str_imt)+"'>"+str(sec_str_imt)+"</abbr>") 
									new_value_dicta["ENTITLEMENT PRICE IMPACT"]= str(sec_str_primp)
									new_value_dicta["CALCULATION FACTOR"] = str("<abbr title='"+str(sec_str_cf)+"'>"+str(sec_str_cf)+"</abbr>")						
							else:
								tab_get_disallow_list.append(attrSysId)
								if attrSysId not in attributesdisallowedlst and attrSysId:
									attributesdisallowedlst.append(attrSysId)
								add_style = "display:none"							
								if DType == "Drop Down":
									#Trace.Write(str(attrName)+'attrSysId--2324--drop down---3491-'+str(attrSysId))
									#STDVALUES =  Sql.GetList("SELECT * from STANDARD_ATTRIBUTE_VALUES where  SYSTEM_ID like '%{sys_id}%' and STANDARD_ATTRIBUTE_CODE = '{attr_code}' ".format(sys_id = str(attrSysId), attr_code = attribute_code )  )
									
									VAR1 = sec_str1 =  ""
									selected_option = " "
									if standard_attr_values:
										if attributevalues.get(attrSysId) is not None:
											#select_option = 'selected'
											select_option = ''
											default = ''
										else:
											select_option = ""
											default = 'selected'
											selected_option = ' title="Select" '
										VAR1 += '<option value="select" ' +str(default)+' style= "display:none;"> </option>'
										for value in standard_attr_values:
											selected = ""
											if value.SYSTEM_ID in dropdowndisallowlist:
												disallow_style = "style = 'display:none'"
											else:	
												disallow_style = ""
											if str(selected_option)=='selected':
												selected_option = ' title="'+str(value.STANDARD_ATTRIBUTE_DISPLAY_VAL)+'" '
											try:
												#Trace.Write('attrSysId-try---3491-'+str(attrSysId))
												if inserted_value_dict[str(attrSysId)] == value.STANDARD_ATTRIBUTE_VALUE :
													selected = "selected"
												VAR1 += (
													'<option '+str(disallow_style)+' id="'+str(value.SYSTEM_ID)+'"  value = "'
													+ str(value.STANDARD_ATTRIBUTE_DISPLAY_VAL) 
													+ '"'+str(select_option)+str(selected)+'>'
													+ str(value.STANDARD_ATTRIBUTE_DISPLAY_VAL)
													+ "</option>"
												)
										
											except:
												#Trace.Write('attrSysId-try-catch--3491-'+str(attrSysId))
												VAR1 += (
													'<option '
													+ str(disallow_style)
													+ ' id="'+str(value.SYSTEM_ID)+'" value = "{value}" {select}>{value}</option>'.format(value= value.STANDARD_ATTRIBUTE_DISPLAY_VAL,select = select_option)
												)
										try:
											sec_str1 += (
													'<select class="form-control remove_yellow '+str(disable_edit)+'" style ="'+str(add_style)+'" id = "'
													+ str(attrSysId)
													+ '" type="text"  data-content ="'
													+ str(attrSysId)
													+ '" onchange="editent_bt(this)" '+str(selected_option)+'  >'
													+ str(VAR1)
													+ "</select>"
												)
										except:		
											sec_str1 += (
												'<select class="form-control remove_yellow '+str(disable_edit)+'" style ="'+str(add_style)+'" id = "'
												+ str(attrSysId)
												+ '" type="text"  data-content ="'
												+ str(attrSysId)
												+ '" onchange="editent_bt(this)" '+str(selected_option)+'  >{} </select>'.format(VAR1)
											)

									
										#sec_str += "<option id='"+str(attrcode)+"' >" + str(optionvalue) + "</option>"
									#sec_str += "</select></td>"
							
								elif DType == "Check Box":
									#STDVALUES =  Sql.GetList("SELECT * from STANDARD_ATTRIBUTE_VALUES where  SYSTEM_ID like '%{sys_id}%' and STANDARD_ATTRIBUTE_CODE = '{attr_code}' ".format(sys_id = str(attrSysId), attr_code = attribute_code )  )
									
									VAR1 = sec_str1 = ""
									if standard_attr_values:
										for value in standard_attr_values:
											
											VAR1 += (
												'<option  value = "'
												+ str(value.STANDARD_ATTRIBUTE_DISPLAY_VAL)
												+ '">'
												+ str(value.STANDARD_ATTRIBUTE_DISPLAY_VAL)
												+ "</option>"
											)
									sec_str1 += (
										'<select class="form-control remove_yellow div_multi_checkbox '+str(disable_edit)+'" style ="'+str(add_style)+'" id = "'
										+ str(attrSysId)
										+ '" type="text"  data-content ="'
										+ str(attrSysId)
										+ '" onchange="editent_bt(this)" >'
										+ str(VAR1)
										+ "</select>"
									)
										
								elif DType == "Free Input, no Matching":
									STDVALUES =  Sql.GetFirst("SELECT STANDARD_ATTRIBUTE_VALUE from STANDARD_ATTRIBUTE_VALUES  where  SYSTEM_ID like '%{sys_id}%' ".format(sys_id = str(attrSysId))  )							
									sec_str1 = ""
									
									if attrValue == "DefaultValue":
										attrValue = ''
									attr_value = ""
									if attrSysId in inserted_value_dict.keys():
										attr_value = inserted_value_dict[attrSysId]
									sec_str1 += (
										'<input maxlength="255" class="form-control remove_yellow '+str(disable_edit)+'" style ="'+str(add_style)+'"  id = "'
										+ str(attrSysId)
										+ '" type="text"  data-content ="'
										+ str(attrSysId)
										+ '" value = "'+str(attr_value)+'" title="'+str(attr_value)+'" onchange="editent_bt(this)" >'
										+ "</input>"
									)
								Trace.Write(str(attrSysId)+'attriburesrequired_list-1436---1288---'+str(attriburesrequired_list))
								if attrSysId in attriburesrequired_list:
									required_symbol_class = str(attrSysId)+' required_symbol'
									get_requiredicon = str("<abbr class='"+str(required_symbol_class)+"' title=''>*</abbr>")
								else:
									required_symbol_class = ""
									get_required_icon = ""
								new_value_dicta["APPROVAL"] = ""	
								new_value_dicta["ENTITLEMENT"] = str(attrName)
								new_value_dicta["DESCRIPTION"] = get_tooltip
								new_value_dicta["REQUIRED"] = ""
								if DType == "Drop Down" or DType == "Check Box" or DType =="Free Input, no Matching":
									new_value_dicta["VALUE"] =sec_str1
									#Trace.Write("attrSysIdDType---3623-- "+str(attrSysId)+str(DType))
								else:
									new_value_dicta["VALUE"] = attrValue
								#new_value_dicta["FACTOR CURRENCY"] = ""
								new_value_dicta["ENTITLEMENT COST IMPACT"]= ""
								new_value_dicta["ENTITLEMENT PRICE IMPACT"]= ""
								new_value_dicta["VALIDATION"] = ""
								new_value_dicta["CALCULATION FACTOR"] = ""	
							#Trace.Write('attributesdisallowedlst'+str(attributesdisallowedlst))
							totaldisallowlist = [item for item in attributesdisallowedlst]
							
							if new_value_dicta:
								date_boot_field.append(new_value_dicta)

						tablistdict[Section_id] = date_boot_field					
						if len(tablistdict) > 0:
							tablistnew.append(tablistdict)
					Product.SetGlobal('ent_data_List',str(tablistnew))					
					table_ids = '#'+Section_id
					getdivid = '#sc_'+Section_id+' .sec_edit_sty'
					getdividbtn = '#sc_'+Section_id+' #btn_ent .sec_edit_sty_btn'
					
					sec_str_boot += ('</div>')
					##section hide starts..
					Trace.Write('nott section--'+str(get_tab_attr_length)+'--'+str(tab_get_disallow_list))
					if len(tab_get_disallow_list) == get_tab_attr_length :
						Trace.Write("yess----"+str(Section_id))
						section_not_list.append(Section_id)
						
					##section hide ends...
					#getprevdicts +=   ("try{var dict_new = {};$('"+str(table_ids)+" tbody tr td select').each(function () {dict_new[$(this).find('td:nth-child(3) select').attr('id')] = $(this).children(':selected').val();});$('"+str(table_ids)+" tbody tr td input').each(function () {if($(this).attr('id') != 'T0_T1_LABOR_calc'){dict_new[$(this).find('td:nth-child(3) input').attr('id')] =  $(this).find('td:nth-child(3) input').val();}});console.log('dict_new-2796--',dict_new);localStorage.setItem('prventdict', JSON.stringify(dict_new))}catch{console.log('')}")
					#getprevdicts +=   ("try{var dict_new = {};$('"+str(table_ids)+" tbody tr:visible').each(function () {dict_new[$(this).find('td:nth-child(3) select').attr('id')] = $(this).find('td:nth-child(3) select').children(':selected').val() ;});$('"+str(table_ids)+" tbody tr:visible').each(function () {dict_new[$(this).find('td:nth-child(3) input').attr('id')] =  $(this).find('td:nth-child(3) input').val();});console.log('dict_new-2796--',dict_new);localStorage.setItem('prventdict', JSON.stringify(dict_new))}catch{console.log('')}")
					if (self.treeparentparam == "Quote Items" or self.treeparam == "Quote Items" or self.treesuperparentparam == "Quote Items" or self.treetopsuperparentparam == "Quote Items"):
						dbl_clk_function = ""
					else:
						#dbl_clk_function += ("try{var dict_new = {};$('"+str(table_ids)+" tbody tr:visible').each(function () {dict_new[$(this).find('td:nth-child(3) select').attr('id')] =  $(this).find('td:nth-child(3) select').children(':selected').attr('id');});$('"+str(table_ids)+" tbody tr:visible').each(function () {dict_new[$(this).find('td:nth-child(3) input').attr('id')] =  $(this).find('td:nth-child(3) input').val();});console.log('dict_new-2818--',dict_new);localStorage.setItem('prventdict', JSON.stringify(dict_new))}catch{console.log('')}")
						dbl_clk_function +=   ("try{var dict_new = {};localStorage.setItem('editfirst','true');$('"+str(table_ids)+"').on('dbl-click-cell.bs.table', function (e, row, $element) { localStorage.setItem('AddNew','false');$('"+str(table_ids)+" tbody tr:visible').each(function () {var getcostimpact =  $(this).find('td:nth-child(7) ').text();var getpriceimpact =  $(this).find('td:nth-child(8) ').text();dict_new[$(this).find('td:nth-child(3) select').attr('id')] =$(this).find('td:nth-child(3) select').children(':selected').val()+'||'+getcostimpact+'||'+getpriceimpact;});var arr = [];$('"+str(table_ids)+" tbody tr:visible').each(function () {if ($(this).find('td:nth-child(3) input') && !($(this).find('td:nth-child(3) input').attr('type') == 'checkbox') ){var getcostimpact =  $(this).find('td:nth-child(7) ').text();var getpriceimpact =  $(this).find('td:nth-child(8) ').text();dict_new[$(this).find('td:nth-child(3) input').attr('id')] =  $(this).find('td:nth-child(3) input').val()+'||'+getcostimpact+'||'+getpriceimpact;}else if ($(this).find('td:nth-child(3) input').attr('type') == 'checkbox') {var getcostimpact =  $(this).find('td:nth-child(7) ').text();var getpriceimpact =  $(this).find('td:nth-child(8) ').text();$(this).find('.mulinput:checked').each(function () {arr.push($(this).val());console.log('arr',arr) });dict_new[$(this).find('td:nth-child(3) select').attr('id')] =  arr+'||'+getcostimpact+'||'+getpriceimpact;};});console.log('dblclk_dict_new-28002--',dict_new,'--',"+str(dropdowndisallowlist)+");localStorage.setItem('prventdict', JSON.stringify(dict_new))})}catch(e){console.log('error---12',e)}")
						#dbl_clk_function +=   ("try{var dict_new = {};$('"+str(table_ids)+"').on('dbl-click-cell.bs.table', function (e, row, $element) { $('"+str(table_ids)+" tbody tr td select').each(function () {dict_new[$(this).attr('id')] = $(this).children(':selected').val();});$('"+str(table_ids)+" tbody tr td input').each(function () {dict_new[$(this).attr('id')] = $(this).val();});console.log('dblclk_dict_new-2800--',dict_new);localStorage.setItem('prventdict', JSON.stringify(dict_new))})}catch{console.log('')}")
						dbl_clk_function += (
							"try {var newentdict =[]; var newentValues =[]; var getentedictip = [];$('"+str(table_ids)+"').on('dbl-click-cell.bs.table', function (e, row, $element) {localStorage.setItem('AddNew','false');if(localStorage.getItem('EDITENT_SEC') != 'EDIT'){console.log('tset--prev value--2300-',this.value);localStorage.setItem('EDITENT_SEC','EDIT');$('"+str(getdivid)+"').css('display','block');$('"+str(getdividbtn)+"').css('display','block');$('"+str(table_ids)+" .MultiCheckBox').css('pointer-events','auto');$('#entsave').css('display','block');$('#entcancel').css('display','block'); $('"+str(table_ids)+" .disable_edit').prop('disabled', false);$('#sc_'+'"+str(Section_id)+"').addClass('header_section_div header_section_div_pad_bt10');$('"+str(table_ids)+" .disable_edit').removeClass('remove_yellow').addClass('light_yellow');$('"+str(table_ids)+" tbody tr td:nth-child(5) input').removeClass('light_yellow').addClass('remove_yellow');$('"+str(table_ids)+" tbody tr td:nth-child(6) input').removeClass('light_yellow').addClass('remove_yellow');$('"+str(table_ids)+" tbody tr td:nth-child(7) input').removeClass('light_yellow').addClass('remove_yellow');$('#AGS_CON_DAY').removeClass('light_yellow').addClass('remove_yellow');$('#AGS_CON_DAY').prop('disabled', true);$('"+str(table_ids)+"  tbody tr td:nth-child(7) input').attr('disabled', 'disabled');$('"+str(table_ids)+"  tbody tr td:nth-child(8) input').attr('disabled', 'disabled');$('"+str(table_ids)+"  tbody tr td:nth-child(6) input').attr('disabled', 'disabled');$('"+str(table_ids)+" tbody tr td:nth-child(8) input').removeClass('light_yellow').addClass('remove_yellow');$('"+str(table_ids)+" .disable_edit').removeClass('remove_yellow').addClass('light_yellow');var testperf = $('#ADDL_PERF_GUARANTEE_91_1').val();console.log('testperf--1---',testperf);if(testperf != undefined && testperf != ''){ if(testperf.toUpperCase() == 'MANUAL INPUT'){console.log('manual input val on donble click---');$('#ADDL_PERF_GUARANTEE_91_1_imt').removeAttr('disabled');$('#ADDL_PERF_GUARANTEE_91_1_primp').parent().css('position', 'relative');$('#ADDL_PERF_GUARANTEE_91_1_primp').removeAttr('disabled');}else{$('#ADDL_PERF_GUARANTEE_91_1_imt').removeClass('light_yellow')};};$('#ADDL_PERF_GUARANTEE_91_1_dt').attr('disabled', 'disabled');$('#ADDL_PERF_GUARANTEE_91_1_calc').attr('disabled', 'disabled');$('input').on('focus', function () {var previnp = $(this).data('val', $(this).val());$('#ADDL_PERF_GUARANTEE_91_1_primp').removeAttr('disabled');console.log('manual input----');var getprevid = this.id;var prev_concate_data = getprevid +'='+previnp;}).change(function() {var prev = $(this).data('val');var current = $(this).val();var getseltabledesc = this.id;var getinputtbleid =  $(this).closest('table').attr('id');var concated_data = getinputtbleid+'|'+current+'|'+getseltabledesc;if(!getentedictip.includes(concated_data)){getentedictip.push(concated_data)};getentedictip1 = JSON.stringify(getentedictip);localStorage.setItem('getdictentdata', getentedictip1);});}})}catch {console.log('error---')}"
						)
					#Trace.Write('dbl_clk_function---'+str(dbl_clk_function))
					'''dbl_clk_function += (
						"try {var getentedict = [];$('"+str(table_ids)+"').on('click-row.bs.table', function (e, row, $element) {console.log('tset--prev value---',this.value);$('"+str(table_ids)+"').find(':input(:disabled)').prop('disabled', false);$('"+str(table_ids)+" tbody  tr td select option').css('background-color','lightYellow');$('"+str(table_ids)+"  tbody tr td select').addClass('light_yellow');$('#fabcostlocate_save').css('display','block');$('#AGS_CON_DAY').prop('disabled', true);$('select').on('focus', function () { var previousval = this.value;console.log('previous1---',previousval);localStorage.setItem('previousval', previousval);}).change(function() {var entchanged = this.value;console.log('previous--previous-----',entchanged);var getatbleid =  $(this).closest('table').attr('id');localStorage.setItem('getatbleid', getatbleid);console.log('getatbleid----',getatbleid);var getseltabledesc = this.id;console.log('getseltableid---',getseltabledesc);var previousval = localStorage.getItem('previousval');var concate_data = getatbleid +'='+previousval+'='+getseltabledesc+'='+entchanged;if(!getentedict.includes(concate_data)){getentedict.push(concate_data)};console.log('getentedict---',getentedict);getentedict = JSON.stringify(getentedict);localStorage.setItem('getentedict', getentedict);localStorage.setItem('previousval', '');});});}catch {console.log('error---')}"
					)'''
				
		##Adding Audit information section in Entitlement starts...
		if ent_temp:
			ent_temp_drop = Sql.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(ent_temp)+"'' ) BEGIN DROP TABLE "+str(ent_temp)+" END  ' ")
		if EntitlementType in ("EQUIPMENT","FABLOCATION","BUSINESSUNIT","ASSEMBLY","TOOLS","ITEM_ENTITLEMENT"):
			get_sec = Sql.GetFirst("""SELECT * FROM SYSECT WHERE PRIMARY_OBJECT_NAME = '{}' AND SECTION_NAME = 'AUDIT INFORMATION'""".format(ObjectName))
			if get_sec :
				section_id = get_sec.RECORD_ID
				section_desc = get_sec.SECTION_NAME
				
				sec_str_boot += ('<div id="container" class="wdth100 margtop10"><div id="sec_'+str(section_id)+ '" class="dyn_main_head master_manufac glyphicon pointer   glyphicon-chevron-down" onclick="dyn_main_sec_collapse_arrow(this)" data-target="#sc_'+ str(section_id)+ '" data-toggle="collapse" <label class="onlytext"><label class="onlytext"><div>'+ str(section_desc).upper()+ '</div></label></div><div id="sc_'+str(section_id)+ '" class="collapse in "><table id="' + str(section_id)+ '" class= "wth100mrg8"  > <tbody>')
				get_sefl = Sql.GetList(
					"SELECT TOP 1000 FIELD_LABEL, API_FIELD_NAME,RECORD_ID FROM SYSEFL WHERE SECTION_RECORD_ID = '" + str(section_id) + "' ORDER BY DISPLAY_ORDER"
				)
				col_name = Sql.GetFirst("SELECT * FROM "+str(ObjectName)+" WHERE "+str(where)+" ")
				for sefl in get_sefl:
					sec_str_boot += (
							'<tr class="iconhvr brdbt" style=" "><td class="wth350"><abbr title="'
							+ str(sefl.FIELD_LABEL)
							+ '" ><label class="pad5mrgbt0">'
							+ str(sefl.FIELD_LABEL)
							+ '</label></abbr></td><td width40><a  title="'
							+ str(sefl.FIELD_LABEL)
							+ '"data-content="'
							+ str(sefl.FIELD_LABEL)
							+ '" class="bgcccwth10"><i class="fa fa-info-circle fltlt"></i></a></td>'
						)
					sefl_api = sefl.API_FIELD_NAME
					
					if col_name:
						current_obj_value = str(eval("col_name." + str(sefl_api)))
						#Trace.Write('current_obj_value---'+str(current_obj_value)+'--'+str(sefl_api))
						if sefl_api in ("CPQTABLEENTRYDATEADDED","CpqTableEntryDateModified") and current_obj_value:
							try:
								current_obj_value = datetime.strptime(str(current_obj_value), '%m/%d/%Y %I:%M:%S %p').strftime('%m/%d/%Y %I:%M:%S %p')
							except:
								pass
						elif sefl_api in ("CpqTableEntryModifiedBy","CPQTABLEENTRYADDEDBY") and current_obj_value:
							current_user = Sql.GetFirst(
								"SELECT USERNAME FROM USERS WHERE ID = " + str(current_obj_value) + "")
							current_obj_value = current_user.USERNAME

						sec_str_boot +=(
							'<td><input id="'
							+ str(sefl_api)
							+ '" type="text" value="'
							+ current_obj_value
							+ '" title="'
							+ current_obj_value
							+ '" class="form-control related_popup_css" '
							+ " disabled></td>"
						)
						sec_str_boot +=(
							'<td class="float_r_bor_bot"><div class="col-md-12 editiconright"><a onclick="" class="editclick"><i class="fa fa-lock" aria-hidden="true"></i></a></div></td>'
						)

					sec_str_boot +=	('</tr>')
					
				sec_str_boot += '</tbody></table>'
			
				sec_str_boot += ('</div></div>')			
		##Adding Audit information section in Entitlement ends...
		quote_status = Sql.GetFirst("SELECT QUOTE_STATUS FROM SAQTMT WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' ".format(self.contract_quote_record_id,self.quote_revision_record_id ))
		if quote_status:
			if quote_status.QUOTE_STATUS == "APPROVED":
				dbl_clk_function = ""
		date_field = ""
		new_value_dict = ""
		api_name = ""
		ret_value = ""
		#Trace.Write('sec_str---'+str(sec_str))
		return sec_str, date_field, new_value_dict, api_name, ret_value, ObjectName, sec_bnr,sec_str_boot,tablistnew,dbl_clk_function,getprevdicts,totaldisallowlist,msg_txt,ChangedList,getnameentallowed,getvaludipto,getvaludipt1,getvaludipt2,getvaludipt2lt,getvaludipt2lab,getvaludipto_q ,getvaludipt2_q,getvaludipt2lt_q ,getvaludipt2lab_q ,getvaludipt2lab,getvaludipt3lab ,getvaludipt3lab_q , getvaludipt3labt ,getvaludipt3labt_q,getvaludipt1_q,getlabortype_calc,gett1labor_calc,gett1labortype_calc,gett2labo_calc,gett2labotype_calc,gett3lab_calc,gett3labtype_calc,getTlab,section_not_list,multi_select_attr_list

##Getting Tree params
try:
	alltreeparam =eval(Param.alltreeparam)
	TreeParam = alltreeparam["TreeParam"]  
	if 'TreeParentLevel0' in  alltreeparam.keys():
		TreeParentParam = alltreeparam["TreeParentLevel0"]
	else:
		TreeParentParam = ""
	if 'TreeParentLevel1' in  alltreeparam.keys():
		TreeSuperParentParam = alltreeparam["TreeParentLevel1"]
	else:
		TreeSuperParentParam = ""
	if 'TreeParentLevel2' in  alltreeparam.keys():
		TreeTopSuperParentParam = alltreeparam["TreeParentLevel2"]
	else:
		TreeTopSuperParentParam = ""
	if 'TreeParentLevel3' in  alltreeparam.keys():
		TreeSuperTopParentParam = alltreeparam["TreeParentLevel3"]
	else:
		TreeSuperTopParentParam = ""
	if 'TreeParentLevel4' in  alltreeparam.keys():
		TreeTopSuperTopParentParam = alltreeparam["TreeParentLevel4"]
	else:
		TreeTopSuperTopParentParam = ""

except:
	#Trace.Write("inside except")
	TreeParam = Product.GetGlobal("TreeParam")
	TreeParentParam = Product.GetGlobal("TreeParentLevel0")
	TreeSuperParentParam = Product.GetGlobal("TreeParentLevel1")
	TreeTopSuperParentParam = Product.GetGlobal("TreeParentLevel2")
	TreeSuperTopParentParam = Product.GetGlobal("TreeParentLevel3")
	TreeTopSuperTopParentParam = Product.GetGlobal("TreeParentLevel4")
	
##getting params
SubtabName = Param.SubtabName
action = Param.action
#Trace.Write("SubtabName==="+str(SubtabName))
try:
	RECORD_ID = Param.RECORD_ID
except:
	RECORD_ID = ""
try:
	ObjectName = Param.ObjectName
	#Trace.Write("ObjectName--"+str(ObjectName))
except Exception as e:
	ObjectName = ""
	#Trace.Write("ObjectName-err--"+str(e))
try:
	SectionList = Param.DetailList
except:
	SectionList = ""
try:
	EquipmentId = Param.EquipmentId
except:
	EquipmentId = ""
try:
	AssemblyId = Param.AssemblyId
except:
	AssemblyId = ""





EntitlementType = ""
SectionObjectName = ""
mode = ""
if SectionList is not None and (
	"CE171F61-B09E-4E4F-8161-1036A062B205" in SectionList
	or "68C30A98-154E-436F-B4E5-73D8186DB68D" in SectionList
	or "68855FCB-F4D7-4641-93AB-B515A41F29E2" in SectionList
	or "0EF8591C-4B5A-4EC2-863F-F8229B5FA025" in SectionList
	or "DF5F6D00-989C-4EDB-BB15-2D350B5F5753" in SectionList
	or "9020F322-C390-4CDC-AD77-ADCE87566815" in SectionList
	or "1F2C9353-3E51-4D1D-8C99-D88FDCED4838" in SectionList
	or "C50B4387-AEBB-4D10-B470-67034C15C44F" in SectionList
	or "F8C12B12-6C91-4838-8BE9-015034ED21C8" in SectionList
	or "36F74B1C-91FD-44BD-BE72-64D5068F9BDB" in SectionList
	or "2D2E0F0C-6013-4073-8F8B-B0D12DE6CECF" in SectionList
	or "0EF8591C-4B5A-4EC2-863F-F8229B5FA025" in SectionList
	or "484F3029-7844-4DE7-BBB4-535A7BAE476E" in SectionList
):

	sectionId = tuple(SectionList)
	sectObj = Sql.GetFirst("SELECT PRIMARY_OBJECT_NAME FROM SYSECT (NOLOCK) WHERE RECORD_ID IN " + str(sectionId) + "")
	if sectObj is not None:
		SectionObjectName = sectObj.PRIMARY_OBJECT_NAME	
		##service level	
		if SectionObjectName == "SAQTSE":
			mode = "Quote"
			EntitlementType = "EQUIPMENT"
		##fab level
		# elif SectionObjectName == "SAQSFE":	
		# 	mode = "Quote"
		# 	EntitlementType = "FABLOCATION"		
		##greenbook level
		elif SectionObjectName == "SAQSGE":	
			mode = "Quote"
			EntitlementType = "BUSINESSUNIT"
		##equipment level
		elif SectionObjectName == "SAQSCE":
			mode = "Quote"
			EntitlementType = "TOOLS"				
		##assembly level
		elif SectionObjectName == "SAQSAE":
			mode = "Quote"
			EntitlementType = "ASSEMBLY"				
		##Quote items     
		elif SectionObjectName == "SAQIEN":
			mode = "Quote"
			TreeParentParam = Product.GetGlobal("TreeParentLevel0")			
			if TreeParentParam == 'Quote Items':
				EntitlementType = "ITEMSPARE"
			elif TreeTopSuperParentParam == 'Quote Items' and SubtabName == 'Equipment Entitlements':
				EntitlementType = "ITEMS"
			elif TreeTopSuperParentParam == 'Quote Items' and SubtabName == 'Entitlements':
				EntitlementType = "ITEMGREENBOOK"				
		
		elif SectionObjectName == ("CTCTSE"):
			mode = "Contracts"
			EntitlementType = "EQUIPMENT"
			
		elif SectionObjectName == ("CTCIEN"):  
			mode = "Contracts" 
			EntitlementType = "ITEMGREENBOOK" 		  		
		
		elif SectionObjectName == ("CTCSGE"):
			mode = "Contracts"
			EntitlementType = "BUSINESSUNIT"			
			
		elif SectionObjectName == ("CTCSCE"):
			mode = "Contracts"
			EntitlementType = "ITEMGREENBOOK"				
			
elif ((SubtabName in ('Entitlements','Equipment Entitlements','Assembly Entitlements') ) and (TreeParam.upper() == "SENDING EQUIPMENT" or TreeSuperParentParam.upper() =="SENDING EQUIPMENT" or TreeParentParam.upper() =="SENDING EQUIPMENT")):
	#Trace.Write("Entitlements"+str(TreeParam))
	EntitlementType = "NO_ENTITLEMENT"
	SectionObjectName = "SAQSRA"

elif ObjectName == "SAQTSE":	
	#Trace.Write("TOOLS")
	SectionObjectName = ObjectName
	EntitlementType = "TOOLS"
	
# elif ObjectName == "CTCTSE":	
# 	SectionObjectName = ObjectName
# 	EntitlementType = "TOOLS"
# else:
# 	Trace.Write("ObjectName-else--"+str(ObjectName))

##calling class


entview_class = EntitlementView()
if action == "VIEW":
	# if mode == 'Contracts':
	# 	ApiResponse = ApiResponseFactory.JsonResponse(entview_class.contract_entitlement_view(RECORD_ID,SectionObjectName,EntitlementType) )
	# else:
	ApiResponse = ApiResponseFactory.JsonResponse(entview_class.entitlement_view(RECORD_ID,SectionObjectName,EntitlementType) )
	
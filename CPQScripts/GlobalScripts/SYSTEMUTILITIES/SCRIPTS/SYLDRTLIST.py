# ==========================================================================================================================================
#   __script_name : SYLDRTLIST.PY
#   __script_description : THIS SCRIPT IS USED TO LOAD RELATED LISTS FOR A GIVEN OBJECT.
#   __primary_author__ : JOE EBENEZER 
#   __create_date :
#   Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import re
import Webcom.Configurator.Scripting.Test.TestProduct
from datetime import datetime

from SYDATABASE import SQL
import time

Sql = SQL()
get_user_id = User.Id
current_date = datetime.now()
productAttributesGetByName = lambda productAttribute: Product.Attributes.GetByName(productAttribute) or ""
try:
	GetActiveRevision = Sql.GetFirst("SELECT QUOTE_REVISION_RECORD_ID,QTEREV_ID FROM SAQTRV (NOLOCK) WHERE QUOTE_ID ='{}' AND ACTIVE = 1".format(Quote.CompositeNumber))
except:
	Trace.Write("EXCEPT: GetActiveRevision ")
	GetActiveRevision = ""
if GetActiveRevision:
	Quote.SetGlobal("quote_revision_record_id",str(GetActiveRevision.QUOTE_REVISION_RECORD_ID))
class SYLDRTLIST:
	def MDYNMICSQLOBJECT(self, RECORD_ID, PerPage, PageInform, SubTab, PR_CURR, TP, equipment_id,line_item):         
		TestProduct = Webcom.Configurator.Scripting.Test.TestProduct() or ""
		getyears = col_year = footer_tot = ""
		getQuotetype = exclamation=""
		
		Page_start = (
			QueryCount
		) = (
			Page_End
		) = (
			Wh_API_NAMEs
		) = (
			TreeParam
		) = (
			TreeParentParam
		) = (
			TreeSuperParentParam
		)  = (
			current_rec_id
		) = (
			Query_Obj
		) = (
			TreeParam
		) = (
			TreeParentParam
		) = (
			TreeSuperParentParam
		) = (
			TopTreeSuperParentParam
		) = (
			TreeTopSuperParentParam
		) = (
			Columns
		) = (
			Obj_Name
		) = (
			table_id
		) = (
			COLUMN_REC_ID
		) = (
			Qstn_REC_ID
		) = (
			CurrentObj_Recordno
		) = (
			CurrentObj_Name
		) = (
			Wh_API_NAME
		) = (
			Wh_OBJECT_NAME
		) = (
			Query_Obj
		) = (
			ObjectName
		) = dbl_clk_function = col = text = texts = Qury_str = QuryCount_str = table_ids = lookup_str = curr_symbol_obj = curr_symbol = decimal_place = SAQICO_dbl_clk_function =  ""

		Action_permission, related_list_permissions, attr_list, attrs_datatype_dict = ({} for i in range(4))

		(
			list_of_tabs,
			cell_api,
			table_list,            
			lookup_rl_popup,
			primary_link_popup,
			lookup_link_popup,
			dblclick_ele,
			checkbox_list,
			name,
			lookup_disply_list,
			edit_field,
		) = ([] for i in range(11))
		#Trace.Write("@96----"+str(primary_link_popup))
		Qustr = ""
		table_header = ""
		TreeParam = Product.GetGlobal("TreeParam")
		TreeParentParam = Product.GetGlobal("TreeParentLevel0")
		
		if str(PerPage) == "" and str(PageInform) == "":
			Page_start = 1
			Page_End = PerPage = 10
			PageInform = "1___10___10"
		else:
			Page_start = int(PageInform.split("___")[0])
			
			Page_End = int(PageInform.split("___")[1])
			
			PerPage = PerPage
		try:
			current_prod = Product.Name
		except:
			current_prod = "Sales"
		
		try:        
			contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
		except:
			contract_quote_record_id = ''    
		if current_prod == "vc_config":
			current_prod = "Sales"
		Trace.Write('139---'+str(RECORD_ID))
		
		#object level permissions
		obj_obj = Sql.GetFirst(
			"""SELECT   SYOBJR.RECORD_ID, SYOBJR.SAPCPQ_ATTRIBUTE_NAME,SYOBJR.PARENT_LOOKUP_REC_ID, SYOBJR.OBJ_REC_ID,
										SYOBJR.NAME, SYOBJR.COLUMN_REC_ID, SYOBJR.COLUMNS,
										SYPROH.CAN_ADD, SYPROH.CAN_EDIT, SYPROH.CAN_DELETE, SYOBJR.RELATED_LIST_SINGULAR_NAME,
										SYOBJR.DISPLAY_ORDER, SYOBJR.ORDERS_BY
									FROM
										SYOBJR (NOLOCK) inner join SYPROH (NOLOCK) on SYPROH.OBJECT_RECORD_ID = SYOBJR.OBJ_REC_ID INNER JOIN USERS_PERMISSIONS (NOLOCK) UP ON UP.PERMISSION_ID = SYPROH.PROFILE_RECORD_ID

									WHERE
										SYOBJR.SAPCPQ_ATTRIBUTE_NAME = '{RECORD_ID}'  AND SYPROH.VISIBLE= 1 AND UP.USER_ID = '{get_user_id}'
									""".format(
				RECORD_ID=str(RECORD_ID), get_user_id=str(get_user_id)
			)
		)
		CurrentModuleObj = Sql.GetFirst("select * from SYAPPS (NOLOCK) where APP_LABEL = '" + str(current_prod) + "'")
		#TestProduct = Webcom.Configurator.Scripting.Test.TestProduct()
		
		crnt_prd_val = str(CurrentModuleObj.APP_ID) or ""
		Product_Name = ""
		tabs = Product.Tabs or "Quotes"       
		for tab in tabs:
			list_of_tabs.append(tab.Name)
		try:
			TestProduct = Webcom.Configurator.Scripting.Test.TestProduct()
			Product_Name = TestProduct.Name
			#Trace.Write('TestProduct--'+str(TestProduct))
		except:            
			Product_Name = "Sales"

		try:
			current_tab = str(TestProduct.CurrentTab)            
		except:            
			current_tab = "Quote"                         
		
		Tree_Enable = Sql.GetFirst(
			"select ENABLE_TREE FROM SYTABS (NOLOCK) where UPPER(SAPCPQ_ALTTAB_NAME) ='"
			+ str(current_tab).upper()
			+ "' AND APP_RECORD_ID = '"
			+ str(str(CurrentModuleObj.APP_RECORD_ID))
			+ "'"
		)
		
		if Tree_Enable is not None or len(Tree_Enable) > 0:
			if str(Tree_Enable.ENABLE_TREE).upper() == "TRUE":
				if Product_Name.upper() == "SYSTEM ADMIN" or Product_Name.upper() == "SALES":
					(
						TreeParam,
						TreeParentParam,
						TreeSuperParentParam,
						TopTreeSuperParentParam,
						TreeFirstSuperTopParentParam,
						TreeSecondSuperTopParentParam,
					) = (
						Product.GetGlobal("TreeParam"),
						Product.GetGlobal("TreeParentLevel0"),
						Product.GetGlobal("TreeParentLevel1"),
						Product.GetGlobal("TreeParentLevel2"),
						Product.GetGlobal("TreeParentLevel3"),
						Product.GetGlobal("TreeParentLevel4"),
					)
				else:
					(
						TreeParam,
						TreeParentParam,
						TreeSuperParentParam,
						TopTreeSuperParentParam,
						TreeTopSuperParentParam,
						TreeFirstSuperTopParentParam,
					) = (
						Product.GetGlobal("CommonTreeParam"),
						Product.GetGlobal("CommonTreeParentParam"),
						Product.GetGlobal("CommonTreeSuperParentParam"),
						Product.GetGlobal("CommonTreeTopSuperParentParam"),
						Product.GetGlobal("CommonTopTreeSuperParentParam"),
						Product.GetGlobal("CommonTreeFirstSuperTopParentParam"),
					)
	
		if obj_obj is None:
			return "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""
		# Billing Matrix - Pivot - Start
		billing_date_column = getQuotetype = delivery_date_column =  ''
		delivery_date_column_joined = ''
		delivery_list = []    
		# Billing Matrix - Pivot - End
		if obj_obj is not None:
			##A055S000P01-4401            
			# if str(TreeParam) == "Quote Items" and RECORD_ID == "SYOBJR-00009" and pricing_picklist_value == 'Pricing':
			# 	##column for pricing view
			# 	Columns = "['STATUS','QUOTE_ITEM_COVERED_OBJECT_RECORD_ID','EQUIPMENT_LINE_ID','SERVICE_ID','EQUIPMENT_ID','SERIAL_NO','ASSEMBLY_ID','GREENBOOK','FABLOCATION_ID','KPU','TECHNOLOGY','YEAR_OVER_YEAR','YEAR_1','YEAR_2','YEAR_3','YEAR_4','YEAR_5','ENTITLEMENT_CATEGORY','TOTAL_COST_WOSEEDSTOCK','TOTAL_COST_WSEEDSTOCK','MODEL_PRICE','TARGET_PRICE','CEILING_PRICE','SALES_DISCOUNT_PRICE','NET_PRICE','BD_PRICE_MARGIN','DISCOUNT','SRVTAXCLA_DESCRIPTION','TAX_PERCENTAGE','NET_VALUE','PRICE_BENCHMARK_TYPE','TOOL_CONFIGURATION','ANNUAL_BENCHMARK_BOOKING_PRICE','CONTRACT_ID','CONTRACT_VALID_FROM','CONTRACT_VALID_TO','BENCHMARKING_THRESHOLD']"
			# else:
			Columns = obj_obj.COLUMNS 
			#Hide columns in Related list based on Quote type start
			if Currenttab == 'Quotes':
				quote_rec_id = Product.GetGlobal("contract_quote_record_id")
				quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
				if  quote_rec_id:                  
					getQuote = Sql.GetFirst("SELECT QUOTE_TYPE,QUOTE_STATUS FROM SAQTMT (NOLOCK) WHERE MASTER_TABLE_QUOTE_RECORD_ID = '"+str(quote_rec_id)+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"'  ")
					getRevision = Sql.GetFirst("SELECT REVISION_STATUS FROM SAQTRV (NOLOCK) WHERE QUOTE_RECORD_ID = '"+str(quote_rec_id)+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"'  ")
					if getQuote:
						getQuotetype = getQuote.QUOTE_TYPE
						getQuotestatus = getQuote.QUOTE_STATUS
					else:
						getQuotetype =''
										
					if str(getQuotetype).upper() == "ZWK1 - SPARES" and  str(TreeParam) in ['Quote Items','Quote Preview','Cart Items','Contract Preview']:
						if RECORD_ID == "SYOBJR-00006" and str(TreeParam) == "Quote Preview":
							rem_list_sp = ["QUOTE_ITEM_FORECAST_PART_RECORD_ID","ITEM_LINE_SEQUENCE","SCHEDULE_MODE","DELIVERY_MODE"]
							Columns = str([ele for ele in  eval(Columns) if ele not in rem_list_sp])                            
						elif RECORD_ID == "SYOBJR-98837" and str(TreeParam) == "Contract Preview":
							rem_list_sp = ["CONTRACT_ITEM_FORECAST_PART_RECORD_ID","MATPRIGRP_ID","SCHEDULE_MODE","DELIVERY_MODE"]
							Columns = str([ele for ele in  eval(Columns) if ele not in rem_list_sp])                            
						elif RECORD_ID == "SYOBJR-00008" and str(TreeParam) == "Quote Items":
							rem_list_sp = ['TARGET_PRICE','CEILING_PRICE','SALES_DISCOUNT_PRICE','BD_PRICE','BD_PRICE_MARGIN','DISCOUNT','NET_PRICE','YEAR_OVER_YEAR','YEAR_1','YEAR_2','YEAR_3','YEAR_4','YEAR_5','SERVICE_DESCRIPTION','QUANTITY']
							Columns = str([ele for ele in  eval(Columns) if ele not in rem_list_sp])  
						if RECORD_ID == "SYOBJR-98792" and str(TreeParam) == "Quote Preview":                    
							rem_list_sp = ["QUOTE_ITEM_RECORD_ID","PO_NOTES","QUANTITY","EQUIPMENT_QUANTITY","TARGET_PRICE","CEILING_PRICE","SALES_DISCOUNT_PRICE","BD_PRICE","BD_PRICE_MARGIN","DISCOUNT","NET_PRICE","YEAR_OVER_YEAR","YEAR_1","YEAR_2",]
							Columns = str([ele for ele in  eval(Columns) if ele not in rem_list_sp])                            
						elif RECORD_ID == "SYOBJR-98819" and str(TreeParam) == "Contract Preview":                    
							rem_list_sp = ["CONTRACT_ITEM_RECORD_ID","PO_NOTES","QUANTITY","DISCOUNT"]
							Columns = str([ele for ele in  eval(Columns) if ele not in rem_list_sp])                            
						else:
							rem_list_sp = ['ITEM_TYPE','ITEM_STATUS','EQUIPMENT_QUANTITY','SALES_DISCOUNT_PRICE','DISCOUNT','UOM_ID']
							Columns = str([ele for ele in  eval(Columns) if ele not in rem_list_sp])
					elif str(getQuotetype).upper() == "ZTBC - TOOL BASED" and  str(TreeParam) in ['Quote Items','Quote Preview','Cart Items','Contract Preview']:
						if RECORD_ID == "SYOBJR-98795" and str(TreeParam) == "Quote Preview":
							rem_list_sp = ["QUOTE_ITEM_COVERED_OBJECT_RECORD_ID","EQUIPMENT_STATUS","BD_DISCOUNT","DISCOUNT","BASE_PRICE","LIST_PRICE","BD_PRICE_MARGIN"]
							Columns = str([ele for ele in  eval(Columns) if ele not in rem_list_sp])                                                 
						elif RECORD_ID == "SYOBJR-98822" and str(TreeParam) == "Contract Preview":
							rem_list_sp = ["CONTRACT_ITEM_COVERED_OBJECT_RECORD_ID","EQUIPMENT_STATUS"]
							Columns = str([ele for ele in  eval(Columns) if ele not in rem_list_sp])                            
						if RECORD_ID == "SYOBJR-98792" and str(TreeParam) == "Quote Preview":                    
							rem_list_sp = ["QUOTE_ITEM_RECORD_ID","PO_NOTES","ONSITE_PURCHASE_COMMIT","DISCOUNT"]
							Columns = str([ele for ele in  eval(Columns) if ele not in rem_list_sp])                            
						elif RECORD_ID == "SYOBJR-98819" and str(TreeParam) == "Contract Preview":                    
							rem_list_sp = ["CONTRACT_ITEM_RECORD_ID","PO_NOTES","ONSITE_PURCHASE_COMMIT"]
							Columns = str([ele for ele in  eval(Columns) if ele not in rem_list_sp])                            
						else:     
							rem_list_sp = ['ITEM_TYPE','ITEM_STATUS','ONSITE_PURCHASE_COMMIT','UOM_ID']
							#rem_list_sp = ['ONSITE_PURCHASE_COMMIT']
							Columns = str([ele for ele in  eval(Columns) if ele not in rem_list_sp])
					elif str(getQuotetype).upper() == "ZTBC - TOOL BASED" and  (str(TreeParentParam) =='Quote Items' or str(TreeSuperParentParam) == "Quote Items" or str(TopTreeSuperParentParam) == "Quote Items" or str(TreeParam) == "Quote Items"):
						if RECORD_ID == "SYOBJR-00009" and (str(TreeParentParam) == "Quote Items" or str(TreeSuperParentParam) == "Quote Items" or str(TopTreeSuperParentParam) == "Quote Items" or str(TreeParam) == "Quote Items") :
							if TreeParam == 'Quote Items':                                  
								rem_list_sp = ["BASE_PRICE"]
							else:
								rem_list_sp = ["SERVICE_ID","BASE_PRICE"]    
							Columns = str([ele for ele in  eval(Columns) if ele not in rem_list_sp])                                                         
					else:         
						##A055S000P01-4401
						##column for pricing view
						# if str(TreeParam) == "Quote Items" and RECORD_ID == "SYOBJR-00009" and pricing_picklist_value == 'Pricing':                            
						# 	Columns = "['STATUS','QUOTE_ITEM_COVERED_OBJECT_RECORD_ID','EQUIPMENT_LINE_ID','SERVICE_ID','EQUIPMENT_ID','SERIAL_NO','ASSEMBLY_ID','GREENBOOK','FABLOCATION_ID','KPU','TECHNOLOGY','YEAR_OVER_YEAR','YEAR_1','YEAR_2','YEAR_3','YEAR_4','YEAR_5','ENTITLEMENT_CATEGORY','TOTAL_COST_WOSEEDSTOCK','TOTAL_COST_WSEEDSTOCK','MODEL_PRICE','TARGET_PRICE','CEILING_PRICE','SALES_DISCOUNT_PRICE','NET_PRICE','BD_PRICE_MARGIN','DISCOUNT','SRVTAXCLA_DESCRIPTION','TAX_PERCENTAGE','NET_VALUE','PRICE_BENCHMARK_TYPE','TOOL_CONFIGURATION','ANNUAL_BENCHMARK_BOOKING_PRICE','CONTRACT_ID','CONTRACT_VALID_FROM','CONTRACT_VALID_TO','BENCHMARKING_THRESHOLD']"  
						# else:        
						Columns = obj_obj.COLUMNS
						if RECORD_ID == "SYOBJR-98869":                                
							rem_list_sp = ["QUOTE_REVISION_RECORD_ID"]
							Columns = str([ele for ele in  eval(Columns) if ele not in rem_list_sp])						
						if RECORD_ID == "SYOBJR-00029" and SubTab.upper() =='INCLUSIONS':							
							rem_list_sp = ["NEW_PART",'FABLOCATION_ID','GREENBOOK']
							Columns = [ele for ele in  eval(Columns) if ele not in rem_list_sp]
							Columns.extend(['UNIT_PRICE','EXTENDED_PRICE'])
							Columns = str(Columns)
			
			#Hide columns in Related list based on Quote type End
			Obj_Name = obj_obj.OBJ_REC_ID            
			COLUMN_REC_ID = obj_obj.COLUMN_REC_ID            
			objsk_permiss = Sql.GetFirst(
				"SELECT CAN_ADD, CAN_EDIT, CAN_DELETE FROM SYOBJR  WHERE SAPCPQ_ATTRIBUTE_NAME = '" + str(RECORD_ID) + "'"
			)
			PARENT_LOOKUP_REC_ID = obj_obj.PARENT_LOOKUP_REC_ID			
			if objsk_permiss:
				if str(objsk_permiss.CAN_EDIT).upper() == "TRUE":
					Action_permission["Edit"] = obj_obj.CAN_EDIT                    
				else:
					Action_permission["Edit"] = objsk_permiss.CAN_EDIT                    
				if str(objsk_permiss.CAN_DELETE).upper() == "TRUE":
					Action_permission["Delete"] = obj_obj.CAN_DELETE                    
				else:
					Action_permission["Delete"] = objsk_permiss.CAN_DELETE			
			objd_where_obj = Sql.GetFirst("select * from  SYOBJD (NOLOCK) where RECORD_ID = '" + str(COLUMN_REC_ID) + "'")
			
			if objd_where_obj is not None:
				Wh_API_NAME = objd_where_obj.API_NAME
				Wh_OBJECT_NAME = objd_where_obj.OBJECT_NAME
			#Contract valid start date & End date Calculation--START
			if Currenttab == 'Quotes':
				Getyear = Sql.GetFirst("select CONTRACT_VALID_FROM,CONTRACT_VALID_TO from SAQTMT where MASTER_TABLE_QUOTE_RECORD_ID = '"+str(contract_quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"'  ")
				if Getyear:
					start_date = datetime(Getyear.CONTRACT_VALID_FROM)
					end_date = datetime(Getyear.CONTRACT_VALID_TO)
					mm = (end_date. year - start_date. year) * 12 + (end_date. month - start_date. month)
					quotient, remainder = divmod(mm, 12)
					getyears = quotient + (1 if remainder > 0 else 0)
					
					if not getyears:
						getyears = 1
					if Quote is not None:
						Quote.GetCustomField('GetBillingMatrix_Year').Content = str(getyears)
					if getyears == 1:
						rem_list_sp = ["YEAR_2","YEAR_3","YEAR_4","YEAR_5","YEAR_2_INGL_CURR","YEAR_3_INGL_CURR","YEAR_4_INGL_CURR","YEAR_5_INGL_CURR"]
						Columns = str([ele for ele in  eval(Columns) if ele not in rem_list_sp]) 
					elif getyears == 2:
						rem_list_sp = ["YEAR_3","YEAR_4","YEAR_5","YEAR_3_INGL_CURR","YEAR_4_INGL_CURR","YEAR_5_INGL_CURR"]
						Columns = str([ele for ele in  eval(Columns) if ele not in rem_list_sp])
					elif getyears == 3:
						rem_list_sp = ["YEAR_4","YEAR_5","YEAR_4_INGL_CURR","YEAR_5_INGL_CURR"]
						Columns = str([ele for ele in  eval(Columns) if ele not in rem_list_sp])
					elif getyears == 4:
						rem_list_sp = ["YEAR_5","YEAR_5_INGL_CURR"]
						Columns = str([ele for ele in  eval(Columns) if ele not in rem_list_sp])
					else:
						Columns
			#Contract valid start date & End date Calculation--END
			#Quote items column based on pricing picklist strts A055S000P01-4578
			# if str(TreeParam) == "Quote Items" and RECORD_ID == "SYOBJR-00009" and pricing_picklist_value == 'Global Currency':
			# 	Columns = Columns.replace('CEILING_PRICE','CEILING_PRICE_INGL_CURR').replace('MODEL_PRICE','MODEL_PRICE_INGL_CURR').replace('NET_PRICE','NET_PRICE_INGL_CURR').replace('NET_VALUE','NET_VALUE_INGL_CURR').replace('TARGET_PRICE','TARGET_PRICE_INGL_CURR').replace('YEAR_1','YEAR_1_INGL_CURR').replace('YEAR_2','YEAR_2_INGL_CURR').replace('YEAR_3','YEAR_3_INGL_CURR').replace('YEAR_4','YEAR_4_INGL_CURR').replace('YEAR_5','YEAR_5_INGL_CURR').replace('SALES_DISCOUNT_PRICE','SLSDIS_PRICE_INGL_CURR').replace('TAX_AMOUNT','TAX_AMOUNT_INGL_CURR')
			#Quote items column based on pricing picklist ends A055S000P01-4578
			#A055S000P01-4401
			Trace.Write('inside--343---'+str(type(Columns)))
			# if RECORD_ID == "SYOBJR-00009" and not (pricing_picklist_value == 'Pricing' and str(TreeParam) == "Quote Items"):
			# 	Trace.Write('inside')
			# 	#backup for SYOBJR-00009
			# 	# ['STATUS','EQUIPMENT_LINE_ID','SERVICE_ID','EQUIPMENT_ID','SERIAL_NO','ASSEMBLY_ID','GREENBOOK','FABLOCATION_ID','KPU','TECHNOLOGY','TOTAL_COST_WOSEEDSTOCK','TOTAL_COST_WSEEDSTOCK','MODEL_PRICE','TARGET_PRICE','CEILING_PRICE','SALES_DISCOUNT_PRICE','BD_PRICE_MARGIN','DISCOUNT','NET_PRICE','YEAR_OVER_YEAR','YEAR_1','YEAR_2','YEAR_3','YEAR_4','YEAR_5','SRVTAXCLA_DESCRIPTION','TAX_PERCENTAGE','NET_VALUE','ENTITLEMENT_CATEGORY','PRICE_BENCHMARK_TYPE','TOOL_CONFIGURATION','ANNUAL_BENCHMARK_BOOKING_PRICE','CONTRACT_ID','CONTRACT_VALID_FROM','CONTRACT_VALID_TO','BENCHMARKING_THRESHOLD']
			# 	rem_list_sp = ["ENTITLEMENT_CATEGORY"]
			# 	Columns = str([ele for ele in  eval(Columns) if ele not in rem_list_sp])
				
			# Billing Matrix - Pivot - Start
			#delivery pivot start
			#A055S000P01-14047 start
			if  Wh_OBJECT_NAME == 'SAQSPD':
				item_delivery_plans_obj = Sql.GetList("""SELECT FORMAT(DELIVERY_SCHED_DATE, 'MM-dd-yyyy') as DELIVERY_SCHED_DATE FROM (SELECT ROW_NUMBER() OVER(ORDER BY DELIVERY_SCHED_DATE)
									AS ROW, * FROM (SELECT DISTINCT DELIVERY_SCHED_DATE
														FROM SAQSPD (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' 
														GROUP BY DELIVERY_SCHED_DATE,QTEREVSPT_RECORD_ID) IQ) OQ WHERE OQ.ROW BETWEEN {} AND {}""".format(
															contract_quote_record_id, quote_revision_record_id, 1, 52))
				count = 0
				if item_delivery_plans_obj:
					delivery_date_column = [item_delivery_plans_obj.DELIVERY_SCHED_DATE for item_delivery_plans_obj in item_delivery_plans_obj]
					for delivery_data in delivery_date_column:
						count += 1
						Delivery = 'Delivery {}'.format(count)
						delivery_date_column_joined = ",".join(["'{}'".format(Delivery)])
						delivery_list.append('{}'.format(Delivery))
						delivery_date_joined =",".join(["'{}'".format(delivery_data)])
						#deliverydata_concatenate  = delivery_date_column_joined + delivery_date_joined
						#delivery_date_joined = ",".join(["'{}','{}'".format('Delivery {}'.format(count),delivery_data) for delivery_data in delivery_date_column])
						#Columns = Columns.replace(']', ','+delivery_date_joined+']')
						Columns = Columns.replace(']', ','+delivery_date_joined+']')
			#A055S000P01-14047 end
			#delivery pivot end
			if Wh_OBJECT_NAME == 'SAQIBP' and SubTab != 'Billing Plan':				
				try:
					if SubTab:
						# item_billing_plan_obj = Sql.GetFirst("""SELECT count(CpqTableEntryId) as cnt FROM SAQIBP (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'GROUP BY EQUIPMENT_ID,SERVICE_ID""".format(contract_quote_record_id,quote_revision_record_id))
						# if item_billing_plan_obj is not None:
						# 	quotient, remainder = divmod(item_billing_plan_obj.cnt, 12)
						# 	years = quotient + (1 if remainder > 0 else 0)
						# 	if not years:
						# 		years = 1
						# 	for index in range(1, years+1):
						# 		YearCount = "Year {}".format(index)
						# 		no_of_year = index
						# 		#YearCount1 = index
						# 		if YearCount:
						# 			end = int(YearCount.split(' ')[-1]) * 12
						# 			start = end - 12 + 1
						#commented for loading grid in billing plan 						
						end = int(SubTab.split(' ')[-1]) * 12
						start = end - 12 + 1
				except:
					end = ""
					start = ""					
				if str(TreeParam) == "Billing":
					item_billing_plans_obj = Sql.GetList("""SELECT FORMAT(BILLING_DATE, 'MM-dd-yyyy') as BILLING_DATE FROM (SELECT ROW_NUMBER() OVER(ORDER BY BILLING_DATE)
									AS ROW, * FROM (SELECT DISTINCT BILLING_DATE
														FROM SAQIBP (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'
														GROUP BY EQUIPMENT_ID, BILLING_DATE,SERVICE_ID) IQ) OQ WHERE OQ.ROW BETWEEN {} AND {}""".format(
															contract_quote_record_id, quote_revision_record_id, start, end))
				else:
					item_billing_plans_obj = Sql.GetList("""SELECT FORMAT(BILLING_DATE, 'MM-dd-yyyy') as BILLING_DATE FROM (SELECT ROW_NUMBER() OVER(ORDER BY BILLING_DATE)
									AS ROW, * FROM (SELECT DISTINCT BILLING_DATE
														FROM SAQIBP (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}' AND QTEREV_RECORD_ID = '{}'
														GROUP BY EQUIPMENT_ID, BILLING_DATE,SERVICE_ID) IQ) OQ WHERE OQ.ROW BETWEEN {} AND {}""".format(
															contract_quote_record_id,TreeParam, quote_revision_record_id, start, end))
				if item_billing_plans_obj:
					billing_date_column = [item_billing_plan_obj.BILLING_DATE for item_billing_plan_obj in item_billing_plans_obj]
					billing_date_column_joined = ",".join(["'{}'".format(billing_data) for billing_data in billing_date_column])
					Columns = Columns.replace(']', ','+billing_date_column_joined+']')   
			# Billing Matrix - Pivot - End
			CurrentObj = Sql.GetFirst(
				"select API_NAME, OBJECT_NAME from  SYOBJD (NOLOCK) where PARENT_OBJECT_RECORD_ID = '"
				+ str(PARENT_LOOKUP_REC_ID)
				+ "' and DATA_TYPE ='AUTO NUMBER'"
			)
			
			if CurrentObj is not None:
				CurrentObj_Recordno = CurrentObj.API_NAME
				CurrentObj_Name = CurrentObj.OBJECT_NAME
			
			Qstn_where_obj = Sql.GetFirst(
				"select QN.* from SYSEFL (NOLOCK) QN INNER JOIN SYSECT (nolock) SE on SE.RECORD_ID = QN.SECTION_RECORD_ID INNER JOIN SYPAGE (nolock) PG on SE.PAGE_RECORD_ID = PG.RECORD_ID where QN.API_NAME = '"
				+ str(CurrentObj_Name)
				+ "' and QN.API_FIELD_NAME = '"
				+ str(CurrentObj_Recordno).strip()
				+ "' and QN.SAPCPQ_ATTRIBUTE_NAME like '%"
				+ str(crnt_prd_val)
				+ "%' and PG.TAB_RECORD_ID != '' "
			)
			RecAttValue = ""
			
			if Qstn_where_obj is not None:
				Qstn_REC_ID = Qstn_where_obj.SAPCPQ_ATTRIBUTE_NAME                
				if Qstn_REC_ID != "":
					wh_Qstn_REC_ID = "QSTN_" + Qstn_REC_ID.replace("-", "_")                    
					RecAttValue = ""
					try:                        
						RecAtt = productAttributesGetByName(str(wh_Qstn_REC_ID))                        
						if RecAtt is not None:                            
							RecAttValue = RecAtt.GetValue()
					except:
						RecAttValue = ""
			table_id = obj_obj.SAPCPQ_ATTRIBUTE_NAME.replace("-", "_") + "_" + str(Obj_Name).replace("-", "_")
			table_ids = "#" + str(table_id)
		
		if 'SYOBJR_98797' in table_id:
			table_header = (
				'<table id="'
				+ table_id
				+ '" data-pagination="false" data-filter-control="true" data-detail-view="true" data-maintain-selected="true" data-locale = "en-US"><thead>'
			)
		elif 'SYOBJR_98872' in table_id or 'SYOBJR_98873' in table_id:
			table_header = (
				'<table id="'
				+ table_id
				+ '" data-pagination="false" data-filter-control="true" class = "items_grid"  data-maintain-selected="true" data-locale = "en-US"><thead>'
			)
		else:
			table_header = (
				'<table id="'
				+ table_id
				+ '" data-pagination="false" data-filter-control="true"  data-maintain-selected="true" data-locale = "en-US"><thead>'
			)
		"""
		elif 'SYOBJR_00005' in table_id:			
			table_header = (
				'<table id="'
				+ table_id
				+ '" data-pagination="false" data-filter-control="true" data-show-export="true" data-maintain-selected="true" data-locale = "en-US"><thead>'
			)
		"""		
		related_list_edit_permission = False
		related_list_delete_permission = False
		#Realted list permissions start
		related_list_permission_obj = Sql.GetFirst(
			"""
									SELECT
							SYOBJR.RELATED_LIST_SINGULAR_NAME,SYPROH.CAN_ADD,SYPROH.CAN_DELETE,SYPROH.CAN_EDIT,SYOBJR.COLUMN_REC_ID ,SYOBJR.COLUMNS,SYOBJR.DISPLAY_ORDER, SYOBJR.NAME,SYOBJR.OBJ_REC_ID,SYOBJR.PARENT_LOOKUP_REC_ID,SYOBJR.RECORD_ID,SYOBJR.SAPCPQ_ATTRIBUTE_NAME,SYOBJR.VISIBLE
						FROM
							SYOBJR (NOLOCK)
						JOIN SYPROH (NOLOCK) ON SYPROH.OBJECT_RECORD_ID = SYOBJR.OBJ_REC_ID
						JOIN USERS_PERMISSIONS (NOLOCK) UP ON UP.PERMISSION_ID = SYPROH.PROFILE_RECORD_ID
						WHERE
							SYOBJR.SAPCPQ_ATTRIBUTE_NAME = '{RECORD_ID}' AND
							SYPROH.VISIBLE = 1 AND
							UP.USER_ID = '{get_user_id}'
							""".format(
				RECORD_ID=str(RECORD_ID), get_user_id=str(get_user_id)
			)
		)
		#Realted list permissions end
		'''related_list_permission_obj = Sql.GetFirst(
			"""
									SELECT
										SYOBJR.RECORD_ID,SYOBJR.SAPCPQ_ATTRIBUTE_NAME, SYOBJR.PARENT_LOOKUP_REC_ID, SYOBJR.OBJ_REC_ID,
										SYOBJR.NAME, SYOBJR.COLUMN_REC_ID, SYOBJR.COLUMNS,
										SYOBJR.CAN_ADD, SYOBJR.CAN_EDIT, SYOBJR.CAN_DELETE, SYOBJR.RELATED_LIST_SINGULAR_NAME,
										SYOBJR.DISPLAY_ORDER, SYOBJR.ORDERS_BY, SYOBJR.VISIBLE
									FROM
										SYOBJR (NOLOCK)

									WHERE

										SYOBJR.SAPCPQ_ATTRIBUTE_NAME = '{RECORD_ID}'
									""".format(
				RECORD_ID=str(RECORD_ID)
			)
		)'''       

		if related_list_permission_obj is not None:
			related_list_edit_permission = related_list_permission_obj.CAN_EDIT
			related_list_delete_permission = related_list_permission_obj.CAN_DELETE
			related_list_permissions.update(
				{"canAdd": related_list_permission_obj.CAN_ADD, "canDelete": related_list_delete_permission}
			)

		objRecName = ""
		# Billing Matrix - Pivot - Start
		column_before_pivot_change = column_before_delivery_pivot_change = ""
		# Billing Matrix - Pivot - End
		if Columns != "" and Obj_Name != "":
			
			objh_obj = Sql.GetFirst("select * from SYOBJH (NOLOCK) where RECORD_ID = '" + str(Obj_Name) + "' ")
			if objh_obj is not None:
				ObjectName = objh_obj.OBJECT_NAME.strip()
				objRecName = objh_obj.RECORD_NAME.strip()
			Objd_Obj = Sql.GetList(
				"select FIELD_LABEL,API_NAME,LOOKUP_OBJECT,LOOKUP_API_NAME,DATA_TYPE,FORMULA_DATA_TYPE,FIELD_SHORT_LABEL from  SYOBJD (NOLOCK) where OBJECT_NAME = '"
				+ str(ObjectName)
				+ "' "
			)

			if Objd_Obj is not None:
				for attr in Objd_Obj:

					attrs_datatype_dict[str(attr.API_NAME)] = str(attr.DATA_TYPE)
					if attr.FIELD_SHORT_LABEL is not None and str(attr.FIELD_SHORT_LABEL) != "":
						attr_list[str(attr.API_NAME)] = str(attr.FIELD_SHORT_LABEL)
					else:
						attr_list[str(attr.API_NAME)] = str(attr.FIELD_LABEL)
					#Trace.Write("attr_list_j"+str(attr_list))
					if (
						str(attr.LOOKUP_API_NAME) != ""
						and str(attr.LOOKUP_API_NAME) is not None
						and str(attr.LOOKUP_API_NAME) not in ["CONTROLLING_FIELD", "DEPENDENT_FIELD"]
					):
						lookup_disply_list.append(str(attr.API_NAME))
						
				checkbox_list = [
					inn.API_NAME for inn in Objd_Obj if (inn.DATA_TYPE == "CHECKBOX" or inn.FORMULA_DATA_TYPE == "CHECKBOX")
				]
				
				right_align_list = [
					inn.API_NAME
					for inn in Objd_Obj
					if (
						inn.DATA_TYPE == "CURRENCY"
						or inn.API_NAME == "SALE_DISCOUNT" or inn.API_NAME == "ANNUAL_QUANTITY" or inn.API_NAME == "ONSITE_PURCHASE_COMMIT"   or (inn.DATA_TYPE == "FORMULA" and inn.FORMULA_DATA_TYPE == "NUMBER")
						or inn.FORMULA_DATA_TYPE == "CURRENCY"
						or inn.DATA_TYPE == "PERCENT"
						or inn.FORMULA_DATA_TYPE == "PERCENT"
						or inn.DATA_TYPE == "NUMBER"
					)
				]
				
				center_align_list = [
					inn.API_NAME
					for inn in Objd_Obj
					if (
						inn.DATA_TYPE == "DATE" or inn.API_NAME == "EFFECTIVEDATE_BEG" or inn.API_NAME == "EFFECTIVEDATE_END" or inn.API_NAME == "ITEM_LINE_SEQUENCE" or inn.API_NAME == "WARRANTY_END_DATE" and  inn.FORMULA_DATA_TYPE == "DATE"
					)
				]
				
				lookup_list = {
					ins.LOOKUP_API_NAME: ins.API_NAME
					for ins in Objd_Obj
					if str(ins.LOOKUP_API_NAME) != "" and str(ins.LOOKUP_API_NAME) is not None
				}
			
			lookup_disply_list123 = ""
			lookup_str = ",".join(list(lookup_disply_list))
			if len(list(lookup_disply_list)) > 1:
				lookup_disply_list123 = list(lookup_disply_list)[0]
			else:
				if len(list(eval(Columns))) > 1:
					lookup_disply_list123 = list(eval(Columns))[0]
			obj_str = ",".join(list(eval(Columns)))
			if lookup_str != "":
				select_obj_str = str(obj_str) + "," + str(lookup_str)
			else:
				select_obj_str = str(obj_str)
			#select_obj_str = select_obj_str.replace("PRIMARY","[PRIMARY]")
			Trace.Write('obj_str-->'+str(obj_str))
			Trace.Write('select_obj_str-->'+str(select_obj_str))
			name = select_obj_str.split(",")
			for text in name:                
				s = Sql.GetList(
					"select DATA_TYPE,LENGTH,API_NAME,DECIMALS,FORMULA_DATA_TYPE from  SYOBJD (NOLOCK) WHERE LTRIM(RTRIM(API_NAME))='"
					+ str(text).strip()
					+ "' and OBJECT_NAME='"
					+ str(ObjectName).strip()
					+ "'"
				)                
				for ins in s:                    
					if (ins.DATA_TYPE == "DATE" or ins.FORMULA_DATA_TYPE == "DATE") or (
						ins.API_NAME
						in [
							"EFFECTIVEDATE_BEG",
							"EFFECTIVEDATE_END",
							"PROMOTION_START_DATE",
							"PROMOTION_END_DATE",
							"EXCHANGE_RATE_DATE",
						]
					):  
						if str(RECORD_ID) == "SYOBJR-00007" and ins.API_NAME == 'BILLING_DATE':
							text = "CONVERT(VARCHAR(10),FORMAT(" + str(text) + ",'MM-dd-yyyy'),101) AS [" + str(text) + "]"
							texts = texts + "," + str(text)                  
						elif texts != "":
							text = "CONVERT(VARCHAR(10)," + str(text) + ",101) AS [" + str(text) + "]"
							texts = texts + "," + str(text)
						else:
							text = "CONVERT(VARCHAR(10)," + str(text) + ",101) AS [" + str(text) + "]"
							texts = str(text)
							
					else:
						if col != "":
							col = col + "," + text                            
						else:
							col = str(text)                            
			if texts != "":
				col = col + "," + texts
			# Billing Matrix - Pivot - Start            
			if billing_date_column:
				column_before_pivot_change = col
				col += ","+ ",".join(billing_date_column)
			if delivery_date_column:
				column_before_delivery_pivot_change = col
				col += ","+ ",".join(delivery_date_column)
		
			Trace.Write('col--642----'+str(col))
			# Billing Matrix - Pivot - End
			col = col.replace("PRIMARY","[PRIMARY]") # CODE COMMON FOR ALL PRIMARY CHECK BOC API NAME
			select_obj_str = col
			
			orderStr = """
									SELECT
										SYOBJR.RECORD_ID,SYOBJR.SAPCPQ_ATTRIBUTE_NAME, SYOBJR.PARENT_LOOKUP_REC_ID, SYOBJR.OBJ_REC_ID,
										SYOBJR.NAME, SYOBJR.COLUMN_REC_ID, SYOBJR.COLUMNS,
										SYOBJR.CAN_ADD, SYOBJR.CAN_EDIT, SYOBJR.CAN_DELETE, SYOBJR.RELATED_LIST_SINGULAR_NAME,
										SYOBJR.DISPLAY_ORDER, SYOBJR.ORDERS_BY
									FROM
										SYOBJR (NOLOCK)

									WHERE

										SYOBJR.SAPCPQ_ATTRIBUTE_NAME = '{RECORD_ID}'
									""".format(
				RECORD_ID=str(RECORD_ID)
			)
			OrderBy_obj = Sql.GetFirst(orderStr)
			
			if Qstn_REC_ID != "" and Wh_API_NAME != "":                
				if OrderBy_obj is not None:
					if OrderBy_obj.ORDERS_BY:
						Wh_API_NAMEs = OrderBy_obj.ORDERS_BY
					else:
						Wh_API_NAMEs = Wh_API_NAME
				else:
					Wh_API_NAMEs = Wh_API_NAME
				
				TreeTopSuperParentParam = Product.GetGlobal("CommonTreeTopSuperParentParam")                

				if RECORD_ID == "SYOBJR-95868":
					
					Qury_str = (
						"select top "
						+ str(PerPage)
						+ " "
						+ "SYSEFL."
						+ str(select_obj_str)
						+ ",SYSEFL.CpqTableEntryId from "
						+ str(ObjectName)
						+ " (nolock) INNER JOIN SYSECT (nolock) ON SYSEFL.SECTION_RECORD_ID = SYSECT.RECORD_ID  AND "
						+ str(Wh_API_NAME)
						+ " = '"
						+ str(RecAttValue)
						+ "' "
						+ "where SYSEFL.SECTION_NAME = '"
						+ str(TreeParentParam)
						+ "' ORDER BY abs(SYSEFL.DISPLAY_ORDER)"
					)
					QuryCount_str = (
						"select count(*) as cnt from "
						+ str(ObjectName)
						+ " (nolock) INNER JOIN SYSECT (nolock) ON SYSEFL.SECTION_RECORD_ID = SYSECT.RECORD_ID and "
						+ str(Wh_API_NAME)
						+ " = '"
						+ str(RecAttValue)
						+ "' where SYSEFL.SECTION_NAME = '"
						+ str(TreeParentParam)
						+ "'"
					)                    
				elif RECORD_ID == "SYOBJR-95843" and TreeParentParam != "" :
					RecAttValue = Product.Attributes.GetByName("QSTN_SYSEFL_SY_03295").GetValue()
					
					Qury_str = (
						"select top "
						+ str(PerPage)
						+ " * "
						+ " from "
						+ str(ObjectName)
						+ " (nolock) WHERE "
						+ str(Wh_API_NAME)
						+ " = '"
						+ str(RecAttValue)
						+ "' AND PAGE_NAME = '"
						+ str(TreeParentParam)
						+ "'"
					)
					QuryCount_str = (
						"select count(*) as cnt from "
						+ str(ObjectName)
						+ " (nolock) WHERE "
						+ str(Wh_API_NAME)
						+ " = '"
						+ str(RecAttValue)
						+ "' AND PAGE_NAME = '"
						+ str(TreeParentParam)
						+ "'"
					)
					
				
				elif RECORD_ID == "SYOBJR-94441":					            
					RecAttValue = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00152").GetValue()
					Qustr = " where " + str(Wh_API_NAME) + " = '" + str(RecAttValue) + "'"
				
				elif RECORD_ID == "SYOBJR-94587" and TreeParam =="Section Actions" :					
					RecAttValue = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00154").GetValue()					
					tabRecord = ""
					gettabres = Sql.GetFirst(
						"Select TB.RECORD_ID,TB.PAGE_NAME,SE.SECTION_NAME from SYTABS (NOLOCK)TB INNER JOIN SYPAGE (NOLOCK) PG ON PG.TAB_RECORD_ID = TB.RECORD_ID INNER JOIN SYSECT (NOLOCK) SE ON SE.PAGE_RECORD_ID = PG.RECORD_ID where TB.TAB_LABEL = '" + str(TreeSecondSuperTopParentParam) + "'AND SE.SECTION_NAME = '"+str(TreeParentParam)+"'"
					)
					if gettabres:                        
						tabRecord = str(gettabres.SECTION_NAME)
					Qustr = " where SECTION_NAME = '" + str(tabRecord) + "'"
					# Qustr = " where " + str(Wh_API_NAME) + " = '" + str(gettabidval) + "'"
				
				elif RECORD_ID == "SYOBJR-94489":                    
					GetappValue = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00154").GetValue()                   

					Qury_str = (
						"select DISTINCT top 10 RECORD_ID,SECTION_NAME,DISPLAY_ORDER,PARENT_SECTION_RECORD_ID,OWNER_RECORD_ID,PRIMARY_OBJECT_RECORD_ID,PAGE_LABEL,PAGE_RECORD_ID,CpqTableEntryId from ( select TOP 10 ROW_NUMBER() OVER(order by DISPLAY_ORDER) AS ROW,* from SYSECT where PAGE_LABEL = '"
						+ str(TreeParentParam)
						+ "') m where m.ROW BETWEEN 1 and 10"
					)
					
					QuryCount_str = (
						"select count(*) as cnt from SYSECT (nolock) where PAGE_LABEL = '" + str(TreeParentParam) + "'"
					)
				elif RECORD_ID == "SYOBJR-97459":
					getrecordpage = ""
					
					gettabval = Sql.GetFirst(
						"Select RECORD_ID,PAGE_NAME from SYPAGE where PAGE_LABEL = '" + str(TreeParentParam) + "'"
					)
					if gettabval:
						getrecordpage = gettabval.PAGE_NAME
				
					Qustr = " where PAGE_NAME = '" + str(getrecordpage) + "'"
				elif RECORD_ID == "SYOBJR-94490":
					tabRecord = ""
				
					GetappValue = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00154").GetValue()                   
					gettabres = Sql.GetFirst(
						"Select RECORD_ID from SYSECT where PAGE_LABEL = '"
						+ str(TopTreeSuperParentParam)
						+ "' and SECTION_NAME = '"
						+ str(TreeParentParam)
						+ "'"
					)
					if gettabres:                        
						tabRecord = str(gettabres.RECORD_ID)
					
					Qustr = " where SECTION_RECORD_ID = '" + str(tabRecord) + "'"                    
				elif RECORD_ID == "SYOBJR-98782":
					GetappValue = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00154").GetValue()
					
					gettabval = Sql.GetFirst(
						"Select RECORD_ID,PAGE_NAME,TAB_LABEL from SYTABS where TAB_LABEL = '" + str(TreeParentParam) + "'"
					)
					if gettabval:
						getpagename = gettabval.TAB_LABEL
					Qustr = " where TAB_LABEL = '" + str(getpagename) + "'"
					
				elif RECORD_ID == "SYOBJR-98784" and TreeParam !="Section Actions":
					gettabval = getptabname = ""
					CommonTreeTopSuperParentParam = Product.GetGlobal("CommonTreeTopSuperParentParam")
					GetappValue = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00154").GetValue()
					gettabval = Sql.GetFirst(
						"Select RECORD_ID,PAGE_NAME,TAB_LABEL from SYTABS where PAGE_NAME = '"
						+ str(TreeParentParam)
						+ "' and TAB_LABEL = '"
						+ str(TopTreeSuperParentParam)
						+ "'"
					)                    
					if gettabval:
						getptabname = gettabval.RECORD_ID
					Qustr = " where TAB_RECORD_ID = '" + str(getptabname) + "'"                    
				elif RECORD_ID == "SYOBJR-98784" and TreeParam =="Section Actions":
					gettabval= Sql.GetFirst(
						"Select RECORD_ID,ACTION_NAME from SYPSAC where SECTION_NAME = '" + str(TreeParentParam) + "'"
					)
					
				
				elif RECORD_ID == "SYOBJR-94587" and TreeParam =="Section Actions":					
					gettabval = ""

					GetappValue = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00154").GetValue()
					gettabval = Sql.GetFirst(
						"Select RECORD_ID,PAGE_NAME from SYTABS where TAB_LABEL = '" + str(TreeFirstSuperTopParentParam) + "'"
					)
					if gettabval:
						getpagename = gettabval.PAGE_NAME
					Qustr = " where PAGE_NAME = '" + str(getpagename) + "'"                    
			
				else:               
					PLN_ID = Product.GetGlobal("PLN_ID")
					if PLN_ID != "":
						PLN_ID = PLN_ID.split("-")[1]
					SORG_ID = Product.GetGlobal("SORG_ID")
					if SORG_ID != "":
						SORG_ID = SORG_ID.split("-")[1]

					elif RECORD_ID == "SYOBJR-93121":
						RecAttValue = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00128").GetValue()
						Qury_str = (
							"select DISTINCT top "
							+ str(PerPage)
							+ " PROFILE_APP_RECORD_ID,APP_ID,VISIBLE,[DEFAULT],PROFILE_RECORD_ID,CpqTableEntryId from ( select TOP 10 ROW_NUMBER() OVER(order by APP_ID) AS ROW, * from SYPRAP (nolock)  where PROFILE_ID = '"
							+ str(RecAttValue)
							+ "' ) m where m.ROW BETWEEN "
							+ str(Page_start)
							+ " and "
							+ str(Page_End)
							+ " order by APP_ID"
						)
						QuryCount_str = (
							"select count(*) as cnt from SYPRAP (nolock)  where PROFILE_ID = '" + str(RecAttValue) + "'"
						)

					elif RECORD_ID == "SYOBJR-93122":
						RecAttValue = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00128").GetValue()
						Qury_str = (
							"select  top "
							+ str(PerPage)
							+ " PROFILE_OBJECT_RECORD_ID,OBJECT_RECORD_ID,OBJECT_NAME, VISIBLE,CpqTableEntryId from ( select ROW_NUMBER() OVER( order by PROFILE_OBJECT_RECORD_ID) AS ROW, PROFILE_OBJECT_RECORD_ID,OBJECT_RECORD_ID,OBJECT_NAME, VISIBLE,CpqTableEntryId from SYPROH (nolock) where PROFILE_ID = '"
							+ str(RecAttValue)
							+ "' ) m where m.ROW BETWEEN "
							+ str(Page_start)
							+ " and "
							+ str(Page_End)
							+ "  order by OBJECT_NAME"
						)
						QuryCount_str = (
							"select count(*) as cnt from SYPROH (nolock) where  PROFILE_ID = '" + str(RecAttValue) + "'"
						)
					
					elif RECORD_ID == "SYOBJR-93169":
						CommonTreeParentParam = Product.GetGlobal("CommonTreeParentParam")
						CommonTreeTopSuperParentParam = Product.GetGlobal("CommonTreeTopSuperParentParam")
						RecAttValue = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00128").GetValue()
						objrecid = ""
						QueryTest = Sql.GetFirst(
							"select TAB_RECORD_ID from SYPRTB (NOLOCK) where TAB_ID='"
							+ str(CommonTreeParentParam)
							+ "' and APP_ID = '"
							+ str(CommonTreeTopSuperParentParam)
							+ "' and PROFILE_ID = '"
							+ str(RecAttValue)
							+ "'"
						)
						if QueryTest is not None:
							objrecid = str(QueryTest.TAB_RECORD_ID)
						

						Qury_str = (
							"select top "
							+ str(PerPage)
							+ " PROFILE_ACTION_RECORD_ID,ACTION_ID,VISIBLE,CpqTableEntryId from ( select ROW_NUMBER() OVER( order by ACTION_ID) AS ROW,PROFILE_ACTION_RECORD_ID,ACTION_ID,VISIBLE,CpqTableEntryId from SYPRAC (nolock) where PROFILE_ID = '"
							+ str(RecAttValue)
							+ "'  and TAB_RECORD_ID='"
							+ str(objrecid)
							+ "') m where m.ROW BETWEEN "
							+ str(Page_start)
							+ " and "
							+ str(Page_End)
							+ " order by ACTION_ID"
						)
						QuryCount_str = (
							"select count(*) as cnt from SYPRAC (nolock)  where PROFILE_ID = '"
							+ str(RecAttValue)
							+ "' and TAB_RECORD_ID='"
							+ str(objrecid)
							+ "'"
						)

					elif RECORD_ID == "SYOBJR-93160":
						RecAttValue = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00128").GetValue()
						GetAppname_query = ""
						if TreeTopSuperParentParam == "App Level Permissions":
							CommonTreeSuperParentParam = Product.GetGlobal("CommonTreeSuperParentParam")
							
							GetAppname_query = Sql.GetFirst(
								"SELECT TAB_RECORD_ID FROM SYPRTB where APP_ID = '"
								+ str(CommonTreeSuperParentParam)
								+ "' and TAB_ID = '"
								+ str(TreeParam)
								+ "'"
							)
						else:
							TreeParam = Product.GetGlobal("CommonTreeParentParam")
							GetAppname_query = Sql.GetFirst(
								"SELECT TAB_RECORD_ID FROM SYPRTB where APP_ID = '"
								+ str(TreeTopSuperParentParam)
								+ "' and TAB_ID = '"
								+ str(TreeParam)
								+ "'"
							)

						Qury_str = (
							"select top "
							+ str(PerPage)
							+ " *  from ( select ROW_NUMBER() OVER(order by P.PROFILE_RECORD_ID) AS ROW, P.PROFILE_SECTION_RECORD_ID,P.SECTION_RECORD_ID,P.SECTION_ID,P.TAB_ID,P.VISIBLE,P.PROFILE_RECORD_ID,P.CpqTableEntryId,s.DISPLAY_ORDER from SYPRSN P (nolock) inner join SYSECT s on s.RECORD_ID = P.SECTION_RECORD_ID where P.PROFILE_ID = '"
							+ str(RecAttValue)
							+ "' and P.TAB_ID = '"
							+ str(TreeParam)
							+ "' and P.TAB_RECORD_ID ='"
							+ str(GetAppname_query.TAB_RECORD_ID)
							+ "' ) m where m.ROW BETWEEN "
							+ str(Page_start)
							+ " and "
							+ str(Page_End)
							+ "  order by m.DISPLAY_ORDER"
						)
						
						QuryCount_str = (
							"select count(*) as cnt from SYPRSN (nolock)  where PROFILE_ID = '"
							+ str(RecAttValue)
							+ "' and TAB_ID = '"
							+ str(TreeParam)
							+ "' and TAB_RECORD_ID ='"
							+ str(GetAppname_query.TAB_RECORD_ID)
							+ "'"
						)

					elif RECORD_ID == "SYOBJR-93188":
						CommonTreeTopSuperParentParam = Product.GetGlobal("CommonTreeTopSuperParentParam")
						TreeFirstSuperTopParentParam = Product.GetGlobal("CommonTreeFirstSuperTopParentParam")
						CommonTreeParentParam = Product.GetGlobal("CommonTreeParentParam")
						CommonTreeTopSuperParentParam = Product.GetGlobal("CommonTreeTopSuperParentParam")
						RecAttValue = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00128").GetValue()
						GetAppname_query = ""
						
						QueryTest = SqlHelper.GetFirst(
							"select TAB_RECORD_ID from SYPRTB (NOLOCK) where TAB_ID='"
							+ str(CommonTreeTopSuperParentParam)
							+ "' and APP_ID = '"
							+ str(TreeFirstSuperTopParentParam)
							+ "' and PROFILE_ID = '"
							+ str(RecAttValue)
							+ "'"
						)
						if QueryTest is not None:
							objrecid = str(QueryTest.TAB_RECORD_ID)
							
							GetAppname_query = SqlHelper.GetFirst(
								"SELECT SECTION_RECORD_ID FROM SYPRSN where TAB_RECORD_ID = '"
								+ str(objrecid)
								+ "' and TAB_ID = '"
								+ str(CommonTreeTopSuperParentParam)
								+ "' and SECTION_ID = '"
								+ str(CommonTreeParentParam)
								+ "' and PROFILE_ID = '"
								+ str(RecAttValue)
								+ "'"
							)
							Qury_str = (
								"select top "
								+ str(PerPage)
								+ " PROFILE_ACTION_RECORD_ID,ACTION_ID,VISIBLE,PROFILE_RECORD_ID,CpqTableEntryId from ( select ROW_NUMBER() OVER(order by PROFILE_RECORD_ID) AS ROW, * from SYPRAC (nolock)  where PROFILE_ID = '"
								+ str(RecAttValue)
								+ "'  and SECTION_RECORD_ID ='"
								+ str(GetAppname_query.SECTION_RECORD_ID)
								+ "' and  SECTION_ID = '"
								+ str(CommonTreeParentParam)
								+ "') m where m.ROW BETWEEN "
								+ str(Page_start)
								+ " and "
								+ str(Page_End)
								+ " "
							)
							
							QuryCount_str = (
								"select count(*) as cnt from SYPRAC (nolock)  where PROFILE_ID = '"
								+ str(RecAttValue)
								+ "'   and SECTION_RECORD_ID ='"
								+ str(GetAppname_query.SECTION_RECORD_ID)
								+ "' and  SECTION_ID = '"
								+ str(CommonTreeParentParam)
								+ "'"
							)

					elif RECORD_ID == "SYOBJR-93162":

						CommonTreeSuperParentParam = Product.GetGlobal("CommonTreeSuperParentParam")
						CommonTreeParentParam = Product.GetGlobal("CommonTreeParentParam")
						CommonTopTreeSuperParentParam = Product.GetGlobal("CommonTopTreeSuperParentParam")
						CommonTreeTopSuperParentParam = Product.GetGlobal("CommonTreeTopSuperParentParam")
						
						RecAttValue = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00128").GetValue()
						TreeFirstSuperTopParentParam = Product.GetGlobal("CommonTreeFirstSuperTopParentParam")
						if TreeFirstSuperTopParentParam == "App Level Permissions":
							getTabrec = Sql.GetFirst(
								"SELECT TAB_RECORD_ID from SYPRTB where APP_ID = '"
								+ str(CommonTopTreeSuperParentParam)
								+ "' and PROFILE_ID = '"
								+ str(RecAttValue)
								+ "' and TAB_ID = '"
								+ str(CommonTreeSuperParentParam)
								+ "'"
							)
							sectrecid = Tabrecordid = ""
							if getTabrec is not None:
								Tabrecordid = str(getTabrec.TAB_RECORD_ID)
								
								getsectrec = Sql.GetFirst(
									"SELECT SECTION_RECORD_ID from SYPRSN where TAB_RECORD_ID = '"
									+ str(Tabrecordid)
									+ "' and SECTION_ID ='"
									+ str(TreeParam)
									+ "'"
								)
								if getsectrec is not None:
									sectrecid = str(getsectrec.SECTION_RECORD_ID)

						else:
							getTabrec = Sql.GetFirst(
								"SELECT TAB_RECORD_ID from SYPRTB where APP_ID = '"
								+ str(TreeFirstSuperTopParentParam)
								+ "' and PROFILE_ID = '"
								+ str(RecAttValue)
								+ "' and TAB_ID = '"
								+ str(CommonTreeTopSuperParentParam)
								+ "'"
							)
							sectrecid = Tabrecordid = ""
							if getTabrec is not None:
								Tabrecordid = str(getTabrec.TAB_RECORD_ID)
								
								getsectrec = Sql.GetFirst(
									"SELECT SECTION_RECORD_ID from SYPRSN where TAB_RECORD_ID = '"
									+ str(Tabrecordid)
									+ "' and SECTION_ID ='"
									+ str(CommonTreeParentParam)
									+ "'"
								)
								if getsectrec is not None:
									sectrecid = str(getsectrec.SECTION_RECORD_ID)
						Qury_str = (
							"select top "
							+ str(PerPage)
							+ " * from ( select ROW_NUMBER() OVER(order by P.SECTION_FIELD_ID ) AS ROW,P.PROFILE_SECTIONFIELD_RECORD_ID,P.SECTIONFIELD_RECORD_ID,P.SECTION_FIELD_ID ,P.VISIBLE,P.EDITABLE,P.PROFILE_RECORD_ID,P.CpqTableEntryId,s.DISPLAY_ORDER from SYPRSF P (nolock)  inner join SYSEFL s on s.RECORD_ID = P.SECTIONFIELD_RECORD_ID where P.PROFILE_ID = '"
							+ str(RecAttValue)
							+ "' and P.SECTION_RECORD_ID = '"
							+ str(sectrecid)
							+ "' ) m where m.ROW BETWEEN "
							+ str(Page_start)
							+ " and "
							+ str(Page_End)
							+ "  order by m.DISPLAY_ORDER"
						)
						QuryCount_str = (
							"select count(*) as cnt from SYPRSF (nolock)  where PROFILE_ID = '"
							+ str(RecAttValue)
							+ "' and SECTION_RECORD_ID = '"
							+ str(sectrecid)
							+ "'"
						)
					elif RECORD_ID == "SYOBJR-94441":						
						RECORD_ID = Product.GetGlobal("RecordNo")                        
						if RECORD_ID != "":
							Qury_str = (
								"select top "
								+ str(PerPage)
								+ " RECORD_ID,TAB_LABEL,TAB_TYPE,APP_RECORD_ID,APP_LABEL,ATTRIBUTE_NAME,CpqTableEntryId from ( select TOP 10 ROW_NUMBER() OVER(order by RECORD_ID) AS ROW, * from SYTABS (nolock)  where "
								+ str(ATTRIBUTE_VALUE_STR)
								+ " APP_RECORD_ID = '"
								+ str(RECORD_ID)
								+ "' ) m where m.ROW BETWEEN "
								+ str(Page_start)
								+ " and "
								+ str(Page_End)
								+ ""
							)
							QuryCount_str = (
								"select count(*) as cnt from "
								+ str(ObjectName)
								+ " (nolock) where APP_RECORD_ID = '"
								+ str(RECORD_ID)
								+ "' "
							)
					#elif RECORD_ID == "SYOBJR-95843":     
						
						#RecAttValue = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00200").GetValue()

					elif RECORD_ID == "SYOBJR-93123":
						Wh_API_NAME = "PROFILE_ID"
						RecAttValue = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00128").GetValue()

						Qustr = " where " + str(Wh_API_NAME) + " = '" + str(RecAttValue) + "'" 
					elif RECORD_ID == "SYOBJR-94452":
						Wh_API_NAME = "ROLE_RECORD_ID"
						RecAttValue = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00001").GetValue()

						Qustr = " where " + str(Wh_API_NAME) + " = '" + str(RecAttValue) + "'"                        
					elif RECORD_ID == "SYOBJR-95800":                        
						RecAttValue = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00128").GetValue()
						permiss_id = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00125").GetValue()
						
						Qury_str = (
							"select DISTINCT TOP "
							+ str(PerPage)
							+ " ID,USERNAME,NAME,ACTIVE from ( select ROW_NUMBER() OVER(order by ID) AS ROW, ID,USERNAME,NAME,ACTIVE from USERS U (nolock) inner join users_permissions up on U.id = up.user_id   where up.permission_id = '"
							+ str(permiss_id)
							+ "'  ) m where m.ROW BETWEEN "
							+ str(Page_start)
							+ " and "
							+ str(Page_End)
							+ ""
						)
						QuryCount_str = (
							"select count(U.ID) as cnt from USERS U (nolock)  inner join users_permissions up on U.id = up.user_id  where  up.permission_id = '"
							+ str(permiss_id)
							+ "'  "
						)
					elif RECORD_ID == "SYOBJR-98784" and TreeParam =="Section Actions":
						gettabval= Sql.GetFirst(
							"Select RECORD_ID,ACTION_NAME from SYPSAC where SECTION_NAME = '" + str(TreeParentParam) + "'"
						)
					elif RECORD_ID == "SYOBJR-98869":						
						RecAttValue = contract_quote_record_id
						#Trace.Write('1196---RecAttValue--RecAttValue-----'+str(RecAttValue))
						Qury_str = ("select DISTINCT TOP "
							+ str(PerPage)
							+ " QUOTE_REVISION_RECORD_ID,CONCAT(QUOTE_ID, '-', QTEREV_ID) AS QTEREV_ID,REVISION_DESCRIPTION,REV_CREATE_DATE,REV_EXPIRE_DATE,REVISION_STATUS,ACTIVE,CONTRACT_VALID_FROM,CONTRACT_VALID_TO,SALESORG_RECORD_ID,QUOTE_RECORD_ID,CpqTableEntryId from ( select TOP 10 ROW_NUMBER() OVER(order by QUOTE_RECORD_ID) AS ROW, * from SAQTRV (nolock)  where QUOTE_RECORD_ID = '" 
							+ str(contract_quote_record_id) + "' ) m where m.ROW BETWEEN "
							+ str(Page_start)
							+ " and "
							+ str(Page_End)
							+ ""
						)
						QuryCount_str = (
							"select count(U.QUOTE_REVISION_RECORD_ID) as cnt from SAQTRV U (nolock) where  U.QUOTE_RECORD_ID = '"
							+ str(contract_quote_record_id)
							+ "'  "
						)
						# Qury_str = (
						# 	"SELECT DISTINCT TOP "
						# 	+ str(PerPage)
						# 	+ "QUOTE_REVISION_RECORD_ID, CONCAT(QUOTE_ID, '-', QTEREV_ID) AS QTEREV_ID,REVISION_DESCRIPTION,REV_CREATE_DATE,REV_EXPIRE_DATE,REVISION_STATUS,ACTIVE FROM ( SELECT TOP "+ str(PerPage)+" ROW_NUMBER() OVER(order by "+ str(Wh_API_NAMEs) +") AS ROW, * FROM SAQTRV (nolock) WHERE QUOTE_RECORD_ID ='"+str(RecAttValue)
						# 	+"') m WHERE m.ROW BETWEEN "
						# 	+ str(Page_start)
						# 	+ " AND "
						# 	+ str(Page_End)+" "
						# )
						Qustr =  " where QUOTE_RECORD_ID = '" + str(contract_quote_record_id) + "'"           
					elif RECORD_ID == "SYOBJR-93130":
						CommonTreeSuperParentParam = Product.GetGlobal("CommonTreeSuperParentParam")
						CommonTreeParentParam = Product.GetGlobal("CommonTreeParentParam")
						CommonTopTreeSuperParentParam = Product.GetGlobal("CommonTopTreeSuperParentParam")
						CommonTreeTopSuperParentParam = Product.GetGlobal("CommonTreeTopSuperParentParam")
						RecAttValue = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00128").GetValue()
						if CommonTreeParentParam == "Object Level Permissions":
							Qury_str = (
								"select top "
								+ str(PerPage)
								+ " * from ( select ROW_NUMBER() OVER(order by PROFILE_RECORD_ID ASC) AS ROW,p.PROFILE_OBJECTFIELD_RECORD_ID,p.OBJECTFIELD_RECORD_ID,s.DISPLAY_ORDER,p.OBJECT_FIELD_ID,p.OBJECT_RECORD_ID,p.OBJECT_NAME,p.VISIBLE,p.EDITABLE,p.CpqTableEntryId from SYPROD p (nolock)  inner join  SYOBJD s on s.RECORD_ID = p.OBJECTFIELD_RECORD_ID where  p.PROFILE_ID = '"
								+ str(RecAttValue)
								+ "' and p.OBJECT_NAME='"
								+ str(TreeParam)
								+ "') m where m.ROW BETWEEN "
								+ str(Page_start)
								+ " and "
								+ str(Page_End)
								+ " order by m.DISPLAY_ORDER"
							)

							QuryCount_str = (
								"select count(*) as cnt from SYPROD (nolock) where PROFILE_ID = '"
								+ str(RecAttValue)
								+ "' and OBJECT_NAME='"
								+ str(TreeParam)
								+ "'"
							)
						else:
							Qury_str = (
								"select top "
								+ str(PerPage)
								+ " * from ( select ROW_NUMBER() OVER(order by PROFILE_RECORD_ID ASC) AS ROW,p.PROFILE_OBJECTFIELD_RECORD_ID,p.OBJECTFIELD_RECORD_ID,s.DISPLAY_ORDER,p.OBJECT_FIELD_ID,p.OBJECT_RECORD_ID,p.OBJECT_NAME,p.VISIBLE,p.EDITABLE,p.CpqTableEntryId from SYPROD p (nolock)  inner join  SYOBJD s on s.RECORD_ID = p.OBJECTFIELD_RECORD_ID where  p.PROFILE_ID = '"
								+ str(RecAttValue)
								+ "' and p.OBJECT_NAME='"
								+ str(CommonTreeParentParam)
								+ "') m where m.ROW BETWEEN "
								+ str(Page_start)
								+ " and "
								+ str(Page_End)
								+ " order by m.DISPLAY_ORDER"
							)

							QuryCount_str = (
								"select count(*) as cnt from SYPROD (nolock) where PROFILE_ID = '"
								+ str(RecAttValue)
								+ "' and OBJECT_NAME='"
								+ str(CommonTreeParentParam)
								+ "'"
							)					
					else:						
						if Wh_API_NAME == "FACTOR_ID":
							dataobjPRICEFACTOR = Sql.GetFirst(
								"SELECT FACTOR_ID FROM PRCAFC WHERE CALCULATION_FACTORS_RECORD_ID='" + str(RecAttValue) + "'"
							)
							if dataobjPRICEFACTOR:
								Qustr = " where " + str(Wh_API_NAME) + " = '" + str(dataobjPRICEFACTOR.FACTOR_ID) + "'"
						elif Wh_API_NAME == "APPROVAL_RECORD_ID":
							dataobjAPHISTORY = Sql.GetFirst(
								"SELECT APPROVAL_RECORD_ID FROM ACAPTX WHERE APPROVAL_TRANSACTION_RECORD_ID='" + str(RecAttValue) + "'"
							)
							if dataobjAPHISTORY:
								Qustr = " where " + str(Wh_API_NAME) + " = '" + str(dataobjAPHISTORY.APPROVAL_RECORD_ID) + "'"
						else:
							CommonTreeParam = Product.GetGlobal("CommonTreeParam")
							CommonTreeSuperParentParam = Product.GetGlobal("CommonTreeSuperParentParam")
							CommonTreeParentParam = Product.GetGlobal("CommonTreeParentParam")
							CommonTopTreeSuperParentParam = Product.GetGlobal("CommonTopTreeSuperParentParam")
							CommonTreeTopSuperParentParam = Product.GetGlobal("CommonTreeTopSuperParentParam")
							if current_prod.upper() == "SALES" or  current_prod.upper() == "APPROVAL CENTER":
								if Currenttab == "Contracts":
									RecAttValue = Quote.GetGlobal("contract_record_id")     
								else:
									if current_prod.upper() == "SALES":
										RecAttValue = Quote.GetGlobal("contract_quote_record_id")
									elif current_prod.upper() == "APPROVAL CENTER":
										if str(current_tab).upper() == "APPROVAL CHAIN":
											RecAttValue = Product.Attributes.GetByName("QSTN_SYSEFL_AC_00001").GetValue()
										else:
											RecAttValue = ""
								Qustr = " where " + str(Wh_API_NAME) + " = '" + str(RecAttValue) + "'"
							elif current_prod.upper() == "PRICE MODELS" and TP == "Sales":                                
								Qustr = " where QUOTE_CURRENCY = '"+str(PR_CURR)+"'"
							elif current_prod.upper() == "PRICE MODELS" and TP == "Sales Orgs":
								Qustr = " where DEF_CURRENCY = '"+str(PR_CURR)+"'"
							elif current_prod.upper() == "PRICE MODELS" and TP == "Exchange Rates":
								Qustr = " where FROM_CURRENCY = '"+str(PR_CURR)+"'"
							elif str(RECORD_ID) == "SYOBJR-98815":
								splitTP = TP.split('-')
								TP = splitTP[1]
								Qustr = "where SALESORG_ID = '"+str(TP)+"' and DOC_CURRENCY='"+str(PR_CURR)+"'"
							elif str(RECORD_ID) == "SYOBJR-95824":
								Qustr = " where " + str(Wh_API_NAME) + " = '" + str(RecAttValue) + "'"                                   
							# elif str(RECORD_ID) == "SYOBJR-93123":
							#     Qustr = " where PROFILE_RECORD_ID = '" + str(RecAttValue) + "'"
							# 
							elif str(RECORD_ID) == "SYOBJR-95840": 
								Wh_API_NAMEs = "PAGEACTION_RECORD_ID"                       
								RecAttValue = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00723").GetValue()
								Qustr =  " where SCRIPT_RECORD_ID = '" + str(RecAttValue) + "'"
							elif str(RECORD_ID) == "SYOBJR-98867":
								TreeParentParam = Product.GetGlobal("TreeParentLevel0") 
								Wh_API_NAMEs = "PAGE_NAME"                       
								Qustr =  " where PAGE_NAME = '" + str(TreeParentParam) + "'"         
							else:    								                  
								Qustr = " where " + str(Wh_API_NAME) + " = '" + str(RecAttValue) + "'"

				if str(Qury_str) == "" and str(QuryCount_str) == "":
					TreeParam = Product.GetGlobal("TreeParam")
					TreeParentParam = Product.GetGlobal("TreeParentLevel0")
					TreeSuperParentParam = Product.GetGlobal("TreeParentLevel1")
					try:
						CurrentTabName = TestProduct.CurrentTab
					except:
						CurrentTabName = "Quotes"
					if str(RECORD_ID) == "SYOBJR-98795":                                           
						qt_rec_id = Sql.GetFirst("SELECT QUOTE_ID FROM SAQTSV WHERE QUOTE_RECORD_ID ='" + str(
							contract_quote_record_id) + "' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"'  ")						  
						LineAndEquipIDList = TreeParam.split(' - ')
						
						if getyears == 1:
							col_year =  'YEAR_1'
						elif getyears == 2:
							col_year =  'YEAR_1,YEAR_2'
						elif getyears == 3:
							col_year =  'YEAR_1,YEAR_2,YEAR_3'
						elif getyears == 4:
							col_year =  'YEAR_1,YEAR_2,YEAR_3,YEAR_4'
						else:
							col_year = 'YEAR_1,YEAR_2,YEAR_3,YEAR_4,YEAR_5'
						if TreeParam == "Quote Preview":                            
							Qury_str = (
							"select top "
								+ str(PerPage)
								+ " QUOTE_ITEM_COVERED_OBJECT_RECORD_ID, EQUIPMENT_ID,SERVICE_ID,BD_DISCOUNT,BD_PRICE_MARGIN,DISCOUNT,YEAR_OVER_YEAR,"+col_year+",SERIAL_NO, GREENBOOK,FABLOCATION_ID, TARGET_PRICE_MARGIN, SALES_DISCOUNT_PRICE, SALDIS_PERCENT,LINE,PRICE_BENCHMARK_TYPE,TOOL_CONFIGURATION,ANNUAL_BENCHMARK_BOOKING_PRICE,CONTRACT_ID,CONVERT(VARCHAR(10),CONTRACT_VALID_FROM,101) AS [CONTRACT_VALID_FROM],CONVERT(VARCHAR(10),CONTRACT_VALID_TO,101) AS [CONTRACT_VALID_TO],BENCHMARKING_THRESHOLD,CpqTableEntryId from ( select  * from SAQICO (NOLOCK) where QUOTE_ID = '"
								+ str(qt_rec_id.QUOTE_ID)
								+ "' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"') m where m.ROW BETWEEN "
								+ str(Page_start)
								+ " and "
								+ str(Page_End)
							)
							QuryCount_str = (
									"select count(*) as cnt FROM SAQICO where QUOTE_ID = '{}'".format(str(qt_rec_id.QUOTE_ID))
							)
					elif str(RECORD_ID) == "SYOBJR-00009":
						# if Quote.GetCustomField('PRICING_PICKLIST').Content == '':
						#     Quote.GetCustomField('PRICING_PICKLIST').Content = 'Document Currency'
						if getyears == 1:
							col_year =  'YEAR_1'
						elif getyears == 2:
							col_year =  'YEAR_1,YEAR_2'
						elif getyears == 3:
							col_year =  'YEAR_1,YEAR_2,YEAR_3'
						elif getyears == 4:
							col_year =  'YEAR_1,YEAR_2,YEAR_3,YEAR_4'
						else:
							col_year = 'YEAR_1,YEAR_2,YEAR_3,YEAR_4,YEAR_5'
						if Product.GetGlobal("TreeParentLevel2") == "Quote Items":                            
							imgstr = '<img title="Acquired" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Green_Tick.svg>'
							acquiring_img_str = '<img title="Acquiring" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Cloud_Icon.svg>'
							exclamation = '<img title="Approval Required" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/clock_exe.svg>'
							error = '<img title="Error" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/exclamation_icon.svg>'
							partially_priced = '<img title="Partially Priced" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Red1_Circle.svg>'
							assembly_missing = '<img title="Assembly Missing" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Orange1_Circle.svg>'
							TreeParentParam = Product.GetGlobal("TreeParentLevel1")							
							try:
								if str(TreeParentParam.split("-")[4]):
									ServiceId = TreeParentParam.split("-")[-3].strip()
								else:
									ServiceId = TreeParentParam.split("-")[1].strip() 
							except:
								ServiceId = TreeParentParam.split("-")[1].strip()
							fab_location_id = Product.GetGlobal("TreeParentLevel0")
							Qury_str = (
									"SELECT DISTINCT TOP "
									+ str(PerPage)
									+ " CASE WHEN STATUS = 'ACQUIRED' THEN '"+ imgstr +"' WHEN STATUS = 'APPROVAL REQUIRED' THEN '"+ exclamation +"' WHEN STATUS = 'ON HOLD - COSTING' THEN '"+ error +"' WHEN STATUS = 'ERROR' THEN '"+ error +"' WHEN STATUS = 'PARTIALLY PRICED' THEN '"+ partially_priced +"' WHEN STATUS = 'ASSEMBLY IS MISSING' THEN '"+ assembly_missing +"' ELSE '"+ acquiring_img_str +"' END AS STATUS, QUOTE_ITEM_COVERED_OBJECT_RECORD_ID,LINE,EQUIPMENT_ID,SERVICE_ID,SERIAL_NO,GREENBOOK,FABLOCATION_ID,TECHNOLOGY,KPU,TARGET_PRICE_MARGIN,TARGET_PRICE,BD_DISCOUNT,BD_PRICE_MARGIN,DISCOUNT,NET_PRICE,YEAR_OVER_YEAR,"+col_year+",SALDIS_PERCENT,EQUIPMENT_RECORD_ID,SERVICE_RECORD_ID,FABLOCATION_RECORD_ID,BD_DISCOUNT_RECORD_ID,EQUIPMENTCATEGORY_RECORD_ID,QUOTE_RECORD_ID,MNT_PLANT_RECORD_ID,SALES_DISCOUNT_PRICE,SALESORG_RECORD_ID,GREENBOOK_RECORD_ID,PRICE_BENCHMARK_TYPE,TOOL_CONFIGURATION,ANNUAL_BENCHMARK_BOOKING_PRICE,CONTRACT_ID,CONVERT(VARCHAR(10),CONTRACT_VALID_FROM,101) AS [CONTRACT_VALID_FROM],CONVERT(VARCHAR(10),CONTRACT_VALID_TO,101) AS [CONTRACT_VALID_TO],BENCHMARKING_THRESHOLD,CpqTableEntryId,ASSEMBLY_ID from ( select ROW_NUMBER() OVER(order by LINE,"+ str(Wh_API_NAMEs) +") AS ROW, * from SAQICO (nolock)  where QUOTE_RECORD_ID ='"+str(RecAttValue)
									+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"'  and GREENBOOK = '"+str(TreeParam)+"' and FABLOCATION_ID = '"+str(fab_location_id)+"' and SERVICE_ID = '"+str(ServiceId)+"') m where m.ROW BETWEEN "
									+ str(Page_start)
									+ " AND "
									+ str(Page_End)
								)

							QuryCount_str = (
								"SELECT COUNT(CpqTableEntryId) AS cnt FROM SAQICO (nolock) WHERE QUOTE_RECORD_ID = '"
									+ str(RecAttValue)
									+ "' AND QTEREV_RECORD_ID = '"
									+ str(quote_revision_record_id)
									+ "' and GREENBOOK = '"+str(TreeParam)+"' and FABLOCATION_ID = '"+str(fab_location_id)+"' and SERVICE_ID = '"+str(ServiceId)+"'"
							)                                
						else:    
							imgstr = '<img title="Acquired" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Green_Tick.svg>'
							acquiring_img_str = '<img title="Acquiring" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Cloud_Icon.svg>'
							exclamation = '<img title="Approval Required" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/clock_exe.svg>'
							error = '<img title="Error" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/exclamation_icon.svg>'
							partially_priced = '<img title="Partially Priced" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Red1_Circle.svg>'
							assembly_missing = '<img title="Assembly Missing" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Orange1_Circle.svg>'
							qt_rec_id = SqlHelper.GetFirst("SELECT QUOTE_ID FROM SAQTSV WHERE QUOTE_RECORD_ID ='" + str(
							contract_quote_record_id) + "' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"'  ")
							if TreeParentParam == "Quote Items": 
								try:
									if str(TreeParam.split("-")[3]):
										LineAndEquipIDList = TreeParam.split(' - ')[1].strip()
									else:
										LineAndEquipIDList = TreeParam.split(' - ')[1].strip() 
								except:
									LineAndEquipIDList = TreeParam.split('-')[1].strip()
							# elif TreeSuperParentParam == "Quote Items":
							#     try:
							#         if str(TreeParentParam.split("-")[3]):
							#             LineAndEquipIDList = TreeParentParam.split(' - ')[-2].strip()
							#         else:
							#             LineAndEquipIDList = TreeParentParam.split(' - ')[1].strip() 
							#     except:
							#         LineAndEquipIDList = TreeParentParam.split(' - ')[1].strip()
							
							if TreeParentParam == "Quote Items":
								Qury_str = (
									"select top "
										+ str(PerPage)
										+ " CASE  WHEN STATUS = 'ACQUIRED' THEN '"+ imgstr +"' WHEN STATUS = 'APPROVAL REQUIRED' THEN '" +exclamation+ "' WHEN STATUS = 'ON HOLD - COSTING' THEN '"+ error +"' WHEN STATUS = 'ERROR' THEN '"+ error +"' WHEN STATUS = 'PARTIALLY PRICED' THEN '"+ partially_priced +"' WHEN STATUS = 'ASSEMBLY IS MISSING' THEN '"+ assembly_missing +"' ELSE '"+ acquiring_img_str +"' END AS STATUS, QUOTE_ITEM_COVERED_OBJECT_RECORD_ID, EQUIPMENT_ID,SERVICE_ID,BD_DISCOUNT,BD_PRICE_MARGIN,DISCOUNT,YEAR_OVER_YEAR,"+col_year+",SERIAL_NO, GREENBOOK,FABLOCATION_ID,TECHNOLOGY,KPU,TARGET_PRICE_MARGIN SALES_DISCOUNT_PRICE, SALDIS_PERCENT,PRICE_BENCHMARK_TYPE,TOOL_CONFIGURATION,ANNUAL_BENCHMARK_BOOKING_PRICE,CONTRACT_ID,CONVERT(VARCHAR(10),CONTRACT_VALID_FROM,101) AS [CONTRACT_VALID_FROM],CONVERT(VARCHAR(10),CONTRACT_VALID_TO,101) AS [CONTRACT_VALID_TO],BENCHMARKING_THRESHOLD,CpqTableEntryId,ASSEMBLY_ID from ( select * from SAQICO (NOLOCK) where QUOTE_ID = '"
										+ str(qt_rec_id.QUOTE_ID)
										+ "' AND SERVICE_ID = '"
										+ str(LineAndEquipIDList)
										+ "' and LINE_ITEM_ID = '"+str(TreeParam.split(' -')[0])+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"') m where m.ROW BETWEEN "
										+ str(Page_start)
										+ " and "
										+ str(Page_End)
								)
								QuryCount_str = (
										"select count(*) as cnt FROM SAQICO where SERVICE_ID = '"+str(LineAndEquipIDList)+"' and QUOTE_ID = '"+str(qt_rec_id.QUOTE_ID)+"'  AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' and LINE_ITEM_ID = '"+str(TreeParam.split(' -')[0])+"'"
								)
							#A055S000P01-4578 starts
							elif TreeParam == "Quote Items":
								Trace.Write("b1")
								#saqico_cols =""								
								#pricing_curr = pricing_picklist_value
									
								# if pricing_picklist_value == 'Document Currency':
								#     saqico_cols ="CEILING_PRICE, MODEL_PRICE, NET_PRICE, NET_VALUE, TARGET_PRICE, SALES_DISCOUNT_PRICE,TAX_AMOUNT, "+col_year
								#     Trace.Write('DocumentCurr----'+str(saqico_cols)) 
								# else:
								#     ##Global Currency
								#     gl_str = "_INGL_CURR"
								#     col_year = col_year.split(',')
								#     col_year = ','.join([i+gl_str for i in col_year])
								#     saqico_cols ="CEILING_PRICE_INGL_CURR, MODEL_PRICE_INGL_CURR, NET_PRICE_INGL_CURR, NET_VALUE_INGL_CURR, TARGET_PRICE_INGL_CURR, SLSDIS_PRICE_INGL_CURR,TAX_AMOUNT_INGL_CURR, "+col_year
								#     Trace.Write('GlobalCurr----'+str(saqico_cols))

								
								# Qury_str = (
								#     "select top "
								#         + str(PerPage)
								#         + " CASE WHEN STATUS = 'ACQUIRED' THEN '"+ imgstr +"' WHEN STATUS = 'APPROVAL REQUIRED' THEN '" +exclamation+ "' WHEN STATUS = 'ON HOLD - COSTING' THEN '"+ error +"' WHEN STATUS = 'ERROR' THEN '"+ error +"' WHEN STATUS = 'PARTIALLY PRICED' THEN '"+ partially_priced +"' WHEN STATUS = 'ASSEMBLY MISSING' THEN '"+ assembly_missing +"'  ELSE '"+ acquiring_img_str +"' END AS STATUS, QUOTE_ITEM_COVERED_OBJECT_RECORD_ID, EQUIPMENT_LINE_ID, EQUIPMENT_ID,SERVICE_ID,LINE_ITEM_ID,BD_DISCOUNT, "+saqico_cols+", BD_PRICE_MARGIN,DISCOUNT,YEAR_OVER_YEAR,SERIAL_NO, GREENBOOK,FABLOCATION_ID,TECHNOLOGY,KPU, TARGET_PRICE_MARGIN, SALDIS_PERCENT, SRVTAXCLA_DESCRIPTION,TAX_PERCENTAGE, PRICE_BENCHMARK_TYPE,TOOL_CONFIGURATION,ANNUAL_BENCHMARK_BOOKING_PRICE,CONTRACT_ID,CONVERT(VARCHAR(10),CONTRACT_VALID_FROM,101) AS [CONTRACT_VALID_FROM],CONVERT(VARCHAR(10),CONTRACT_VALID_TO,101) AS [CONTRACT_VALID_TO],BENCHMARKING_THRESHOLD,CpqTableEntryId,ASSEMBLY_ID,TOTAL_COST_WOSEEDSTOCK,TOTAL_COST_WSEEDSTOCK from ( select  ROW_NUMBER() OVER( ORDER BY EQUIPMENT_LINE_ID) AS ROW, * from SAQICO (NOLOCK) where QUOTE_ID = '"
								#         + str(qt_rec_id.QUOTE_ID)
								#         + "'  AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"') m where m.ROW BETWEEN "
								#         + str(Page_start)
								#         + " and "
								#         + str(Page_End)
								# )
								Qury_str = (
									"select top "
										+ str(PerPage)
										+ " CASE WHEN STATUS = 'ACQUIRED' THEN '"+ imgstr +"' WHEN STATUS = 'APPROVAL REQUIRED' THEN '" +exclamation+ "' WHEN STATUS = 'ON HOLD - COSTING' THEN '"+ error +"' WHEN STATUS = 'ERROR' THEN '"+ error +"' WHEN STATUS = 'PARTIALLY PRICED' THEN '"+ partially_priced +"' WHEN STATUS = 'ASSEMBLY IS MISSING' THEN '"+ assembly_missing +"'  ELSE '"+ acquiring_img_str +"' END AS STATUS, QUOTE_ITEM_COVERED_OBJECT_RECORD_ID,SERVICE_ID,FABLOCATION_ID,GREENBOOK,OBJECT_ID,OBJECT_TYPE,QUANTITY,EQUIPMENT_ID,GOT_CODE,ASSEMBLY_ID,PM_ID,PM_LABOR_LEVEL,KIT_NAME,KIT_NUMBER,KPU,TOOL_CONFIGURATION,SSCM_PM_FREQUENCY,ADJ_PM_FREQUENCY,CEILING_PRICE_INGL_CURR,TARGET_PRICE_INGL_CURR,SLSDIS_PRICE_INGL_CURR,BD_PRICE_INGL_CURR,DISCOUNT,SALES_PRICE_INGL_CURR,YEAR_OVER_YEAR,YEAR,CONVERT(VARCHAR(10),CONTRACT_VALID_FROM,101) AS [CONTRACT_VALID_FROM],CONVERT(VARCHAR(10),CONTRACT_VALID_TO,101) AS [CONTRACT_VALID_TO],CONVERT(VARCHAR(10),WARRANTY_START_DATE,101) AS [WARRANTY_START_DATE],CONVERT(VARCHAR(10),WARRANTY_END_DATE,101) AS [WARRANTY_END_DATE],CNTCST_INGL_CURR,CNTPRI_INGL_CURR,CpqTableEntryId from ( select  ROW_NUMBER() OVER( ORDER BY CpqTableEntryId) AS ROW, * from SAQICO (NOLOCK) where QUOTE_ID = '"
										+ str(qt_rec_id.QUOTE_ID)
										+ "'  AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"') m where m.ROW BETWEEN "
										+ str(Page_start)
										+ " and "
										+ str(Page_End)
								)
								QuryCount_str = (
										"select count(*) as cnt FROM SAQICO where QUOTE_ID = '{}' AND QTEREV_RECORD_ID ='{}'".format(
											str(qt_rec_id.QUOTE_ID),quote_revision_record_id)
								)
							#A055S000P01-4578 ends
							elif Product.GetGlobal("TreeParentLevel1") == 'Quote Items': 
								try:                               
									if str(TreeParentParam.split("-")[4]):
										ServiceId = TreeParentParam.split("-")[-3].strip()
									else:
										ServiceId = TreeParentParam.split("-")[1].strip()
								except:
									ServiceId = TreeParentParam.split("-")[1].strip()
								Qury_str = (
									"SELECT DISTINCT TOP "
									+ str(PerPage)
									+ " CASE WHEN STATUS = 'ACQUIRED' THEN '"+ imgstr +"' WHEN STATUS = 'APPROVAL REQUIRED' THEN '"+ exclamation +"' WHEN STATUS = 'ON HOLD - COSTING' THEN '"+ error +"' WHEN STATUS = 'ERROR' THEN '"+ error +"' WHEN STATUS = 'PARTIALLY PRICED' THEN '"+ partially_priced +"' WHEN STATUS = 'ASSEMBLY IS MISSING' THEN '"+ assembly_missing +"' ELSE '"+ acquiring_img_str +"' END AS STATUS, QUOTE_ITEM_COVERED_OBJECT_RECORD_ID,EQUIPMENT_ID,SERVICE_ID,SERIAL_NO,GREENBOOK,FABLOCATION_ID,TARGET_PRICE_MARGIN,BD_DISCOUNT,BD_PRICE_MARGIN,DISCOUNT,YEAR_OVER_YEAR,"+col_year+",SALDIS_PERCENT,EQUIPMENT_RECORD_ID,SERVICE_RECORD_ID,FABLOCATION_RECORD_ID,TECHNOLOGY,KPU,BD_DISCOUNT_RECORD_ID,EQUIPMENTCATEGORY_RECORD_ID,QUOTE_RECORD_ID,QTEREV_RECORD_ID,MNT_PLANT_RECORD_ID,SALES_DISCOUNT_PRICE,SALESORG_RECORD_ID,GREENBOOK_RECORD_ID,PRICE_BENCHMARK_TYPE,TOOL_CONFIGURATION,ANNUAL_BENCHMARK_BOOKING_PRICE,CONTRACT_ID,CONVERT(VARCHAR(10),CONTRACT_VALID_FROM,101) AS [CONTRACT_VALID_FROM],CONVERT(VARCHAR(10),CONTRACT_VALID_TO,101) AS [CONTRACT_VALID_TO],BENCHMARKING_THRESHOLD,CpqTableEntryId,ASSEMBLY_ID from ( select ROW_NUMBER() OVER(order by "+ str(Wh_API_NAMEs) +") AS ROW, * from SAQICO (nolock)  where QUOTE_RECORD_ID ='"+str(RecAttValue)
									+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"'  and FABLOCATION_ID = '"+str(TreeParam)+"' and SERVICE_ID = '"+str(ServiceId)+"' and LINE_ITEM_ID = '"+str(TreeParentParam.split(' -')[0])+"') m where m.ROW BETWEEN "
									+ str(Page_start)
									+ " AND "
									+ str(Page_End)
								)

								QuryCount_str = (
									"SELECT COUNT(CpqTableEntryId) AS cnt FROM SAQICO (nolock) WHERE QUOTE_RECORD_ID = '"
										+ str(RecAttValue)
										+ "' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' and FABLOCATION_ID = '"+str(TreeParam)+"'and SERVICE_ID = '"+str(ServiceId)+"' and LINE_ITEM_ID = '"+str(TreeParentParam.split(' -')[0])+"'"
								)          
							else:
								Qury_str = (
									"select top "
										+ str(PerPage)
										+ " * from ( select  * from SAQICO (NOLOCK) where QUOTE_ID = '"
										+ str(qt_rec_id.QUOTE_ID)
										+ "' AND SERVICE_ID = '"
										+ str(LineAndEquipIDList[1])
										+ "' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"') m where m.ROW BETWEEN "
										+ str(Page_start)
										+ " and "
										+ str(Page_End)
								)
								QuryCount_str = (
										"select count(*) as cnt FROM SAQICO where SERVICE_ID = '{}' and QUOTE_ID = '{}'  AND QTEREV_RECORD_ID = '{}'".format(
											LineAndEquipIDList[1], str(qt_rec_id.QUOTE_ID),quote_revision_record_id)
								)
					elif str(RECORD_ID) == "SYOBJR-91822":
						contractrecid = Product.GetGlobal("contract_record_id")						
						if Product.GetGlobal("TreeParentLevel1") == "Cart Items":                                                     
							imgstr = '<img title="Acquired" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Green_Tick.svg>'
							acquiring_img_str = '<img title="Acquiring" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Cloud_Icon.svg>'
							TreeParentParam = Product.GetGlobal("TreeParentLevel0")
							ServiceId = TreeParentParam.split("-")[1].strip()                           
							Qury_str = (
									"SELECT DISTINCT TOP "
									+ str(PerPage)
									+ " CASE WHEN DISCOUNT = 'ACQUIRED' THEN '"+ imgstr +"' ELSE '"+ imgstr +"' END AS EQUIPMENT_STATUS, CONTRACT_ITEM_COVERED_OBJECT_RECORD_ID,SERVICE_ID,EQUIPMENT_ID,SERIAL_NO,GREENBOOK,TOTAL_COST,LINE_ITEM_ID,DISCOUNT,TAX,NET_VALUE,EQUIPMENT_RECORD_ID,SERVICE_RECORD_ID,FABLOCATION_RECORD_ID,EQUIPMENTCATEGORY_RECORD_ID,CONTRACT_RECORD_ID,MNT_PLANT_RECORD_ID,SALESORG_RECORD_ID,GREENBOOK_RECORD_ID,CONTRACT_CURRENCY,CONTRACT_CURRENCY_RECORD_ID,CpqTableEntryId from ( select ROW_NUMBER() OVER(order by "+ str(Wh_API_NAMEs) +") AS ROW, * from CTCICO (nolock)  where CONTRACT_RECORD_ID ='"+str(RecAttValue)
									+"' and GREENBOOK = '"+str(TreeParam)+"' and SERVICE_ID = '"+str(ServiceId)+"') m where m.ROW BETWEEN "
									+ str(Page_start)
									+ " AND "
									+ str(Page_End)
								)

							QuryCount_str = (
								"SELECT COUNT(CpqTableEntryId) AS cnt FROM CTCICO (nolock) WHERE CONTRACT_RECORD_ID = '"
									+ str(RecAttValue)
									+ "'and GREENBOOK = '"+str(TreeParam)+"'and SERVICE_ID = '"+str(ServiceId)+"'"
							)                                
						else:							                 
							imgstr = '<img title="Acquired" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Green_Tick.svg>'
							acquiring_img_str = '<img title="Acquiring" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Cloud_Icon.svg>'
							qt_rec_id = Sql.GetFirst("SELECT CONTRACT_ID FROM CTCTSV (NOLOCK) WHERE CONTRACT_RECORD_ID='" + str(
							contractrecid) + "'")
							LineAndEquipIDList = TreeParam.split(' - ')
							if TreeParentParam == "Cart Items":
								Qury_str = (
									"select top "
										+ str(PerPage)
										+ " CASE WHEN DISCOUNT = 'ACQUIRED' THEN '"+ imgstr +"' ELSE '"+ imgstr +"' END AS EQUIPMENT_STATUS, CONTRACT_ITEM_COVERED_OBJECT_RECORD_ID,EQUIPMENT_LINE_ID,SERVICE_ID,EQUIPMENT_ID,SERIAL_NO,GREENBOOK,TOTAL_COST,LINE_ITEM_ID,DISCOUNT,TAX,NET_VALUE,EQUIPMENT_RECORD_ID,SERVICE_RECORD_ID,FABLOCATION_RECORD_ID,EQUIPMENTCATEGORY_RECORD_ID,CONTRACT_RECORD_ID,MNT_PLANT_RECORD_ID,SALESORG_RECORD_ID,GREENBOOK_RECORD_ID,CpqTableEntryId from ( select  ROW_NUMBER() OVER( ORDER BY EQUIPMENT_LINE_ID) AS ROW, * from CTCICO (NOLOCK) where CONTRACT_ID = '"
										+ str(qt_rec_id.CONTRACT_ID)
										+ "' AND SERVICE_ID = '"
										+ str(LineAndEquipIDList[1])
										+ "') m where m.ROW BETWEEN "
										+ str(Page_start)
										+ " and "
										+ str(Page_End)
								)
								QuryCount_str = (
										"select count(*) as cnt FROM CTCICO where SERVICE_ID = '{}' and CONTRACT_ID = '{}'".format(
											LineAndEquipIDList[1], str(qt_rec_id.CONTRACT_ID))
								)
							elif TreeParam == "Cart Items":
								Qury_str = (
									"select top "
										+ str(PerPage)
										+ " CASE WHEN DISCOUNT = 'ACQUIRED' THEN '"+ imgstr +"' ELSE '"+ imgstr +"' END AS EQUIPMENT_STATUS, CONTRACT_ITEM_COVERED_OBJECT_RECORD_ID,EQUIPMENT_LINE_ID,SERVICE_ID,EQUIPMENT_ID,SERIAL_NO,GREENBOOK,TOTAL_COST,LINE_ITEM_ID,DISCOUNT,TAX,NET_VALUE,EQUIPMENT_RECORD_ID,SERVICE_RECORD_ID,FABLOCATION_RECORD_ID,EQUIPMENTCATEGORY_RECORD_ID,CONTRACT_RECORD_ID,MNT_PLANT_RECORD_ID,SALESORG_RECORD_ID,GREENBOOK_RECORD_ID,CpqTableEntryId from ( select  ROW_NUMBER() OVER( ORDER BY EQUIPMENT_LINE_ID) AS ROW, * from CTCICO (NOLOCK) where CONTRACT_ID = '"
										+ str(qt_rec_id.CONTRACT_ID)
										+ "') m where m.ROW BETWEEN "
										+ str(Page_start)
										+ " and "
										+ str(Page_End)
								)
								QuryCount_str = (
										"select count(*) as cnt FROM CTCICO where CONTRACT_ID = '{}'".format(     str(qt_rec_id.CONTRACT_ID))
								)
							else:                                   
								Qury_str = (
									"select top "
										+ str(PerPage)
										+ " * from ( select  ROW_NUMBER() OVER( ORDER BY EQUIPMENT_LINE_ID) AS ROW, * from CTCICO (NOLOCK) where CONTRACT_ID = '"
										+ str(qt_rec_id.CONTRACT_ID)
										+ "' AND SERVICE_ID = '"
										+ str(LineAndEquipIDList[1])
										+ "') m where m.ROW BETWEEN "
										+ str(Page_start)
										+ " and "
										+ str(Page_End)
								)
								QuryCount_str = (
										"select count(*) as cnt FROM CTCICO where SERVICE_ID = '{}' and CONTRACT_ID = '{}'".format(
											LineAndEquipIDList[1], str(qt_rec_id.CONTRACT_ID))
								)
					elif str(RECORD_ID) == 'SYOBJR-98799':
						contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
						qt_rec_id = Sql.GetFirst("SELECT QUOTE_ID FROM SAQTSV WHERE QUOTE_RECORD_ID ='" + str(
						contract_quote_record_id) + "' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' ")
						try:
							quote_id = qt_rec_id.QUOTE_ID
						except:
							quote_id = ""
						imgstr = '<img title="Acquired" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Green_Tick.svg>'
						acquiring_img_str = '<img title="Acquiring" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Cloud_Icon.svg>'
						Qury_str = (
									"select top "
										+ str(PerPage)
										+ " CASE WHEN STATUS = 'ACQUIRED' THEN '"+ imgstr +"' ELSE '"+ acquiring_img_str +"' END AS STATUS, QUOTE_DOCUMENT_RECORD_ID, DOCUMENT_ID,DOCUMENT_NAME,LANGUAGE_ID,LANGUAGE_NAME,CPQTABLEENTRYDATEADDED,QUOTE_RECORD_ID,QTEREV_RECORD_ID,CpqTableEntryId from ( select  ROW_NUMBER() OVER( ORDER BY STATUS) AS ROW, * from SAQDOC (NOLOCK) where QUOTE_ID = '"
										+ str(quote_id)
										+ "' AND QTEREV_RECORD_ID = '"
										+ str(quote_revision_record_id)
										+ "' ) m where m.ROW BETWEEN "
										+ str(Page_start)
										+ " and "
										+ str(Page_End)
								)
						QuryCount_str = (
								"select count(*) as cnt FROM SAQDOC where QUOTE_ID = '{}'".format(
									str(quote_id))
						)
					elif str(RECORD_ID) == "SYOBJR-00015" and str(TreeParentParam) == "Approval Chain Steps":
						Qury_str = (
							" SELECT TOP "
							+ str(PerPage)
							+ " * FROM (SELECT ROW_NUMBER() OVER(ORDER BY APPROVAL_TRACKED_FIELD_RECORD_ID) AS ROW,APPROVAL_TRACKED_FIELD_RECORD_ID,TRKOBJ_TRACKEDFIELD_LABEL,TRKOBJ_NAME,TRACKING_TYPE,ACAPTF.CpqTableEntryId FROM ACAPTF (NOLOCK) INNER JOIN ACACST (NOLOCK) ON ACAPTF.APRCHNSTP_RECORD_ID = ACACST.APPROVAL_CHAIN_STEP_RECORD_ID WHERE ACACST.APRCHN_RECORD_ID = '"
							+ str(RecAttValue)
							+ "' AND ACACST.APRCHNSTP_NAME = '"
							+ str(TreeParam).split(': ')[1]
							+ "' )m where m.ROW BETWEEN "
							+ str(Page_start)
							+ " and "
							+ str(Page_End)
							+ " "
						)

						QuryCount_str = (
							"SELECT COUNT(APPROVAL_TRACKED_FIELD_RECORD_ID) AS cnt FROM ACAPTF (NOLOCK) INNER JOIN ACACST (NOLOCK) ON ACAPTF.APRCHNSTP_RECORD_ID = ACACST.APPROVAL_CHAIN_STEP_RECORD_ID WHERE ACACST.APRCHN_RECORD_ID = '"
							+ str(RecAttValue)
							+ "' AND ACACST.APRCHNSTP_NAME = '"
							+ str(TreeParam).split(': ')[1]
							+ "' "
						)    
					elif str(RECORD_ID) == "SYOBJR-00014":                        
						step_name = TreeParam.split(':')[1].strip()
						Qury_str = (
							"select top "
							+ str(PerPage)
							+ " * from ( select ROW_NUMBER() OVER( order by APPROVAL_CHAIN_STEP_APPROVER_RECORD_ID) AS ROW,ACACSA.APPROVAL_CHAIN_STEP_APPROVER_RECORD_ID,ACACSA.APRCHN_ID,ACACSA.APRCHNSTP_APPROVER_ID,ACACSA.APPROVER_SELECTION_METHOD,ACACSA.USERNAME,ACACSA.PROFILE_ID,ACACSA.ROLE_ID,ACACSA.NOTIFICATION_ONLY,ACACSA.CpqTableEntryId from ACACSA (nolock) INNER JOIN ACACST (NOLOCK) ON ACACST.APPROVAL_CHAIN_STEP_RECORD_ID = ACACSA.APRCHNSTP_RECORD_ID WHERE  ACACSA."
							+ str(Wh_API_NAME)
							+ " = '"
							+ str(RecAttValue)
							+ "' AND ACACST.APRCHNSTP_NAME = '"
							+ str(step_name)
							+ "') m where m.ROW BETWEEN "
							+ str(Page_start)
							+ " AND "
							+ str(Page_End)
							+ ""
						)
						QuryCount_str = (
							"select count(ACACSA.CpqTableEntryId) as cnt from ACACSA (nolock) INNER JOIN ACACST (NOLOCK) ON ACACST.APPROVAL_CHAIN_STEP_RECORD_ID = ACACSA.APRCHNSTP_RECORD_ID WHERE ACACSA."
							+ str(Wh_API_NAME)
							+ " = '"
							+ str(RecAttValue)
							+ "' AND ACACST.APRCHNSTP_NAME = '"
							+ str(step_name)
							+ "'"
						)
					elif str(RECORD_ID) == "SYOBJR-98822":     
						if Product.GetGlobal("TreeParentLevel1") == "Cart Items":                            
							imgstr = '<img title="Acquired" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Green_Tick.svg>'
							acquiring_img_str = '<img title="Acquiring" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Cloud_Icon.svg>'
							
							Qury_str = (
									"SELECT DISTINCT TOP "
									+ str(PerPage)
									+ " CASE WHEN DISCOUNT = 'ACQUIRED' THEN '"+ imgstr +"' ELSE '"+ imgstr +"' END AS EQUIPMENT_STATUS, CONTRACT_ITEM_COVERED_OBJECT_RECORD_ID,EQUIPMENT_LINE_ID,SERVICE_ID,EQUIPMENT_ID,SERIAL_NO,GREENBOOK,TOTAL_COST,LINE_ITEM_ID,DISCOUNT,TAX,NET_VALUE,EQUIPMENT_RECORD_ID,SERVICE_RECORD_ID,FABLOCATION_RECORD_ID,EQUIPMENTCATEGORY_RECORD_ID,CONTRACT_RECORD_ID,MNT_PLANT_RECORD_ID,SALESORG_RECORD_ID,GREENBOOK_RECORD_ID,CpqTableEntryId from ( select ROW_NUMBER() OVER(order by "+ str(Wh_API_NAMEs) +") AS ROW, * from CTCICO (nolock)  where CONTRACT_RECORD_ID ='"+str(RecAttValue)
									+"' and GREENBOOK = '"+str(TreeParam)+"') m where m.ROW BETWEEN "
									+ str(Page_start)
									+ " AND "
									+ str(Page_End)
								)

							QuryCount_str = (
								"SELECT COUNT(CpqTableEntryId) AS cnt FROM CTCICO (nolock) WHERE CONTRACT_RECORD_ID = '"
									+ str(RecAttValue)
									+ "'and GREENBOOK = '"+str(TreeParam)+"'"
							)  
						else:    
							imgstr = '<img title="Acquired" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Green_Tick.svg>'
							acquiring_img_str = '<img title="Acquiring" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Cloud_Icon.svg>'
							contract_record_id = Product.GetGlobal("contract_record_id")
							qt_rec_id = Sql.GetFirst("SELECT CONTRACT_ID, SERVICE_ID FROM CTCTSV (NOLOCK) WHERE CONTRACT_RECORD_ID ='" + str(
							contract_record_id) + "'")
							LineAndEquipIDList = TreeParam.split(' - ')
							if qt_rec_id.CONTRACT_ID == '70011556':
								SERV_DESC = "Z0091"
							else:
								SERV_DESC = qt_rec_id.SERVICE_ID
							if TreeParentParam == "Cart Items":
								Qury_str = (
									"select top "
										+ str(PerPage)
										+ " CASE WHEN DISCOUNT = 'ACQUIRED' THEN '"+ imgstr +"' ELSE '"+ imgstr +"' END AS EQUIPMENT_STATUS, CONTRACT_ITEM_COVERED_OBJECT_RECORD_ID, EQUIPMENT_LINE_ID, SERVICE_ID, EQUIPMENT_ID,LINE_ITEM_ID,DISCOUNT,SERIAL_NO, GREENBOOK, TOTAL_COST, TAX, NET_VALUE, CONTRACT_CURRENCY, CONTRACT_CURRENCY_RECORD_ID,CpqTableEntryId from ( select  ROW_NUMBER() OVER( ORDER BY EQUIPMENT_LINE_ID) AS ROW, * from CTCICO (NOLOCK) where CONTRACT_ID = '"
										+ str(qt_rec_id.CONTRACT_ID)
										+ "' AND SERVICE_ID = '"
										+ str(LineAndEquipIDList[1])
										+ "') m where m.ROW BETWEEN "
										+ str(Page_start)
										+ " and "
										+ str(Page_End)
								)
								QuryCount_str = (
										"select count(*) as cnt FROM CTCICO where SERVICE_ID = '{}' and CONTRACT_ID = '{}'".format(
											LineAndEquipIDList[1], str(qt_rec_id.CONTRACT_ID))
								)
							else:
								Qury_str = (
									"select top "
										+ str(PerPage)
										+ " * from ( select  ROW_NUMBER() OVER( ORDER BY EQUIPMENT_LINE_ID) AS ROW, * from CTCICO (NOLOCK) where CONTRACT_ID = '"
										+ str(qt_rec_id.CONTRACT_ID)
										+ "' AND SERVICE_ID = '"
										+ str(SERV_DESC)
										+ "') m where m.ROW BETWEEN "
										+ str(Page_start)
										+ " and "
										+ str(Page_End)
								)
								QuryCount_str = (
										"select count(*) as cnt FROM CTCICO where SERVICE_ID = '{}' and CONTRACT_ID = '{}'".format(
											SERV_DESC, str(qt_rec_id.CONTRACT_ID))
								)
					elif str(RECORD_ID) == "SYOBJR-98788":
						#contract_quote_record_id = Quote.CompositeNumber						
						contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")                        
						qt_rec_id= Sql.GetFirst("SELECT QUOTE_ID FROM SAQTSV WHERE QUOTE_RECORD_ID ='"+str(contract_quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' ")
						if qt_rec_id is not None:
							if TreeParentParam:
								Qustr = "where QUOTE_ID = '"+str(qt_rec_id.QUOTE_ID)+"' and SERVICE_TYPE = '{}'".format(TreeParam) +" AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' "
							else:
								Qustr = "where QUOTE_ID = '"+str(qt_rec_id.QUOTE_ID)+"'" +" AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' "
							
							doc_type = Sql.GetList("SELECT DOCTYP_ID FROM SAQTSV (NOLOCK) "+ str(Qustr))
							for document_type in doc_type:
								if document_type.DOCTYP_ID == "ZWK1":
									Qury_str = (
										"select DISTINCT top "
										+ str(PerPage)
										+ " "
										+ str(select_obj_str)
										+ ",CpqTableEntryId from ( select TOP 10 ROW_NUMBER() OVER(order by "
										+ str(Wh_API_NAMEs)
										+ ") AS ROW, S.QUOTE_SERVICE_RECORD_ID,S.SERVICE_ID,S.SERVICE_DESCRIPTION,S.PAR_SERVICE_ID,S.SERVICE_TYPE,S.QUOTE_RECORD_ID,S.SALESORG_RECORD_ID,S.UOM_RECORD_ID,S.PAR_SERVICE_RECORD_ID,S.QTEREV_RECORD_ID,S.SERVICE_RECORD_ID,CONVERT(VARCHAR(10),CONTRACT_VALID_FROM,101) AS [CONTRACT_VALID_FROM],CONVERT(VARCHAR(10),CONTRACT_VALID_TO,101) AS [CONTRACT_VALID_TO],S.CpqTableEntryId  from SAQTSV S "
										+ str(Qustr)
										+ ") m where m.ROW BETWEEN "
										+ str(Page_start)
										+ " and "
										+ str(Page_End)
										+ ""
									)
								else:
									Qury_str = (
										"select DISTINCT top "
										+ str(PerPage)
										+ " "
										+ str(select_obj_str)
										+ ",CpqTableEntryId from ( select TOP 10 ROW_NUMBER() OVER(order by "
										+ str(Wh_API_NAMEs)
										+ ") AS ROW, S.QUOTE_SERVICE_RECORD_ID,S.SERVICE_ID,S.SERVICE_DESCRIPTION,S.PAR_SERVICE_ID,S.SERVICE_TYPE,S.QUOTE_RECORD_ID,S.SALESORG_RECORD_ID,S.UOM_RECORD_ID,S.PAR_SERVICE_RECORD_ID,S.QTEREV_RECORD_ID,S.SERVICE_RECORD_ID,CONVERT(VARCHAR(10),CONTRACT_VALID_FROM,101) AS [CONTRACT_VALID_FROM],CONVERT(VARCHAR(10),CONTRACT_VALID_TO,101) AS [CONTRACT_VALID_TO],S.CpqTableEntryId  from SAQTSV S JOIN (SELECT distinct PRDOFR_ID FROM MAADPR WHERE VISIBLE_INCONFIG = 'TRUE' )M ON S.SERVICE_ID = M.PRDOFR_ID "
										+ str(Qustr)
										+ ") m where m.ROW BETWEEN "
										+ str(Page_start)
										+ " and "
										+ str(Page_End)
										+ ""
									)
							QuryCount_str = "select count(*) as cnt from " + str(ObjectName) + " S (nolock)  JOIN (SELECT distinct PRDOFR_ID FROM MAADPR WHERE VISIBLE_INCONFIG = 'TRUE' )M ON S.SERVICE_ID = M.PRDOFR_ID " + str(Qustr) 
						else: 							
							#Qustr = "where QUOTE_ID = '"+str(contract_quote_record_id)+"'"                          
							Qury_str = (
								"select DISTINCT top "
								+ str(PerPage)
								+ " "
								+ str(select_obj_str)
								+ ",CpqTableEntryId from ( select TOP 10 ROW_NUMBER() OVER(order by "
								+ str(Wh_API_NAMEs)
								+ ") AS ROW, * from "
								+ str(ObjectName)
								+ " (nolock) "
								+ str(Qustr)
								+ " ) m where m.ROW BETWEEN "
								+ str(Page_start)
								+ " and "
								+ str(Page_End)
								+ ""
							)
							
							QuryCount_str = "select count(*) as cnt from " + str(ObjectName) + " (nolock)  JOIN MAADPR M ON S.SERVICE_ID = M.PRDOFR_ID " + str(Qustr) + " and M.VISIBLE_INCONFIG = 'TRUE'"
					elif str(RECORD_ID) == "SYOBJR-98853" and str(TreeParam) == "Tracked Objects":
						RecAttValue = Product.Attributes.GetByName("QSTN_SYSEFL_AC_00063").GetValue()
						Qury_str = (
							"select DISTINCT top "
							+ str(PerPage)
							+ " APPROVAL_TRACKED_FIELD_RECORD_ID,APRCHN_ID,APRCHNSTP,TRKOBJ_TRACKEDFIELD_LABEL,TRKOBJ_NAME,TRACKING_TYPE,CpqTableEntryId from (SELECT ROW_NUMBER() OVER(order by APPROVAL_TRACKED_FIELD_RECORD_ID) AS ROW,ACAPTF.APPROVAL_TRACKED_FIELD_RECORD_ID,ACAPTF.APRCHN_ID,ACAPTF.APRCHNSTP,ACAPTF.TRKOBJ_TRACKEDFIELD_LABEL,ACAPTF.TRKOBJ_NAME,ACAPTF.TRACKING_TYPE,ACAPTF.CpqTableEntryId FROM ACAPTF (NOLOCK) INNER JOIN ACAPTX ON ACAPTF.APRCHN_ID = ACAPTX.APRCHN_ID WHERE ACAPTX.APPROVAL_TRANSACTION_RECORD_ID = '"
							+ str(RecAttValue)
							+ "') S where S.ROW BETWEEN "
							+ str(Page_start)
							+ " and "
							+ str(Page_End)
							+ " "
						)
						QuryCount_str = (
							"SELECT count(DISTINCT ACAPTF.APPROVAL_TRACKED_FIELD_RECORD_ID) as cnt FROM ACAPTF (NOLOCK) INNER JOIN ACAPTX ON ACAPTF.APRCHN_ID = ACAPTX.APRCHN_ID WHERE ACAPTX.APPROVAL_TRANSACTION_RECORD_ID = '"
							+ str(RecAttValue)                            
							+ "' "
						)
					elif str(RECORD_ID) == "SYOBJR-00026" and str(TreeParentParam) == "Tracked Objects":
						RecAttValue = Product.Attributes.GetByName("QSTN_SYSEFL_AC_00063").GetValue()
						Qury_str = (
							"select DISTINCT top "
							+ str(PerPage)
							+ " APPROVAL_TRACKED_VALUE_RECORD_ID,APRCHN_ID,APRCHNSTP,TRKOBJ_TRACKEDFIELD_LABEL,TRKOBJ_NAME,TRKOBJ_TRACKEDFIELD_OLDVALUE,TRKOBJ_TRACKEDFIELD_NEWVALUE,TRKOBJ_CPQTABLEENTRYID,CpqTableEntryId from (SELECT ROW_NUMBER() OVER(order by APPROVAL_TRACKED_VALUE_RECORD_ID) AS ROW,ACAPFV.TRKOBJ_TRACKEDFIELD_OLDVALUE,ACAPFV.APPROVAL_TRACKED_VALUE_RECORD_ID,ACAPFV.APRCHN_ID,ACAPFV.APRCHNSTP,ACAPFV.TRKOBJ_TRACKEDFIELD_LABEL,ACAPFV.TRKOBJ_NAME,ACAPFV.TRKOBJ_TRACKEDFIELD_NEWVALUE, ACAPFV.CpqTableEntryId,ACAPFV.TRKOBJ_CPQTABLEENTRYID FROM ACAPFV (NOLOCK) INNER JOIN ACAPTX ON ACAPFV.APRCHN_ID = ACAPTX.APRCHN_ID AND ACAPFV.APPROVAL_ID = ACAPTX.APPROVAL_ID WHERE ACAPTX.APPROVAL_TRANSACTION_RECORD_ID = '"
							+ str(RecAttValue)
							+ "' AND ACAPFV.TRKOBJ_TRACKEDFIELD_LABEL= '"
							+ str(TreeParam)                            
							+ "') S where S.ROW BETWEEN "
							+ str(Page_start)
							+ " and "
							+ str(Page_End)
							+ " "
						)
						QuryCount_str = (
							"SELECT count(DISTINCT ACAPFV.APPROVAL_TRACKED_VALUE_RECORD_ID) as cnt FROM ACAPFV (NOLOCK) INNER JOIN ACAPTX ON ACAPFV.APRCHN_ID = ACAPTX.APRCHN_ID WHERE ACAPTX.APPROVAL_TRANSACTION_RECORD_ID = '"
							+ str(RecAttValue) 
							+ "' AND ACAPFV.TRKOBJ_TRACKEDFIELD_LABEL= '"
							+ str(TreeParam)                           
							+ "' "
						)
					elif str(RECORD_ID) == "SYOBJR-98816":
						contract_quote_record_id = Quote.GetGlobal("contract_record_id")                        
						ct_rec_id= SqlHelper.GetFirst("SELECT CONTRACT_ID FROM CTCTSV (NOLOCK) WHERE CONTRACT_RECORD_ID ='"+str(contract_quote_record_id)+"'")
						try:
							if TreeParentParam:
								Qustr = "where  CONTRACT_ID = '"+str(ct_rec_id.CONTRACT_ID)+"' and PRODUCT_TYPE = '{}'".format(TreeParam)
							else:
								Qustr = "where  CONTRACT_ID = '"+str(ct_rec_id.CONTRACT_ID)+"'"
						except:
							Qustr=" where  CONTRACT_ID = '' "
						Qury_str = (
							"select DISTINCT top "
							+ str(PerPage)
							+ " "
							+ str(select_obj_str)
							+ ",CpqTableEntryId from ( select TOP 10 ROW_NUMBER() OVER(order by "
							+ str(Wh_API_NAMEs)
							+ ") AS ROW, * from "
							+ str(ObjectName)
							+ " (nolock) "
							+ str(Qustr)
							+ " ) m where m.ROW BETWEEN "
							+ str(Page_start)
							+ " and "
							+ str(Page_End)
							+ ""
						)
						
						QuryCount_str = "select count(*) as cnt from " + str(ObjectName) + " (nolock) " + str(Qustr)
									
					## involved parties equipmemt starts
					elif  str(RECORD_ID) == "SYOBJR-34575":
						if delivery_date_column:                        
							pivot_columns = ",".join(['[{}]'.format(delivery_date) for delivery_date in delivery_date_column])							
							if Qustr:
								
								Qustr += " AND DELIVERY_SCHED_DATE  BETWEEN '{}' AND '{}'".format(delivery_date_column[0], delivery_date_column[-1])
							pivot_query_str = """
										SELECT ROW_NUMBER() OVER(ORDER BY QTEREVSPT_RECORD_ID )
										AS ROW, *
											FROM (
												SELECT 
													{Columns}                                         
												FROM {ObjectName}
												{WhereString}
											) AS IQ
											PIVOT
											(
												SUM(QUANTITY)
												FOR DELIVERY_SCHED_DATE  IN ({PivotColumns})
											)AS PVT
										""".format(OrderByColumn=Wh_API_NAMEs,Columns=column_before_delivery_pivot_change, ObjectName=ObjectName,
													WhereString=Qustr, PivotColumns=pivot_columns)                        
							Qury_str = """
										SELECT DISTINCT TOP {PerPage} * FROM ( SELECT * FROM ({InnerQuery}) OQ WHERE ROW BETWEEN {Start} AND {End} ) AS FQ ORDER BY QTEREVSPT_RECORD_ID 
										""".format(PerPage=PerPage, OrderByColumn=Wh_API_NAMEs, InnerQuery=pivot_query_str, Start=Page_start, End=Page_End)
							QuryCount_str = "SELECT COUNT(*) AS cnt FROM ({InnerQuery}) OQ ".format(InnerQuery=pivot_query_str)
					elif str(RECORD_ID) == "SYOBJR-00007": # Billing Matrix - Pivot - Start						
						if billing_date_column:                        
							pivot_columns = ",".join(['[{}]'.format(billing_date) for billing_date in billing_date_column])							
							if Qustr:
								if str(TreeParentParam)== "Billing":
									Qustr += " AND SERVICE_ID = '{}' AND BILLING_DATE BETWEEN '{}' AND '{}'".format(TreeParam,billing_date_column[0], billing_date_column[-1])
								else:
									Qustr += " AND BILLING_DATE BETWEEN '{}' AND '{}'".format(billing_date_column[0], billing_date_column[-1])
							pivot_query_str = """
										SELECT ROW_NUMBER() OVER(ORDER BY EQUIPMENT_ID)
										AS ROW, *
											FROM (
												SELECT 
													{Columns}                                           
												FROM {ObjectName}
												{WhereString}
											) AS IQ
											PIVOT
											(
												SUM(BILLING_VALUE)
												FOR BILLING_DATE IN ({PivotColumns})
											)AS PVT
										""".format(OrderByColumn=Wh_API_NAMEs, Columns=column_before_pivot_change, ObjectName=ObjectName,
													WhereString=Qustr, PivotColumns=pivot_columns)                        
							Qury_str = """
										SELECT DISTINCT TOP {PerPage} * FROM ( SELECT * FROM ({InnerQuery}) OQ WHERE ROW BETWEEN {Start} AND {End} ) AS FQ ORDER BY EQUIPMENT_ID
										""".format(PerPage=PerPage, OrderByColumn=Wh_API_NAMEs, InnerQuery=pivot_query_str, Start=Page_start, End=Page_End)
							QuryCount_str = "SELECT COUNT(*) AS cnt FROM ({InnerQuery}) OQ ".format(InnerQuery=pivot_query_str)
						
						# Billing Matrix - Pivot - End 
					##involved parties equipmemt starts
					elif (str(RECORD_ID) == "SYOBJR-98858" or str(RECORD_ID) == "SYOBJR-00028") and str(TreeParam) == "Quote Information":
						account_id = Product.GetGlobal("stp_account_id")                        
						Qury_str = ("""select DISTINCT top {PerPage} * from (select ROW_NUMBER() OVER( ORDER BY SAQSTE.FABLOCATION_ID DESC) AS ROW,SAQSTE.* from SAQSTE  inner join SAQSCF(nolock)  on SAQSTE.QUOTE_RECORD_ID = SAQSCF.QUOTE_RECORD_ID and SAQSTE.QTEREV_RECORD_ID = SAQSCF.QTEREV_RECORD_ID and SAQSTE.SRCFBL_ID = SAQSCF.SRCFBL_ID where SAQSTE.QUOTE_RECORD_ID = '{contract_quote_record_id}' and SAQSTE.QTEREV_RECORD_ID = '{revision_rec_id}' and SAQSTE.SRCACC_ID = '{account_id}')m where m.ROW BETWEEN """.format(PerPage = PerPage,account_id = account_id,revision_rec_id = quote_revision_record_id, contract_quote_record_id = str(RecAttValue))+ str(Page_start) + " and " + str(Page_End))
						
						QuryCount_str = "select count(SAQSTE.CpqTableEntryId) as cnt from SAQSTE  inner join SAQSCF(nolock) on SAQSTE.QUOTE_RECORD_ID = SAQSCF.QUOTE_RECORD_ID and SAQSTE.QTEREV_RECORD_ID = SAQSCF.QTEREV_RECORD_ID and SAQSTE.SRCFBL_ID= SAQSCF.SRCFBL_ID where SAQSTE.QUOTE_RECORD_ID = '{contract_quote_record_id}' and SAQSTE.QTEREV_RECORD_ID = '{revision_rec_id}' and SAQSTE.SRCACC_ID = '{account_id}'".format(account_id = account_id,revision_rec_id = quote_revision_record_id,contract_quote_record_id=str(RecAttValue))
					##involved parties equipmemt ends
					
					##involved parties source fab starts
					elif (str(RECORD_ID) == "SYOBJR-98857") and str(TreeParam) == "Quote Information":
						account_id = Product.GetGlobal("stp_account_id")                        
						Qustr += " AND SRCACC_ID = '{}'".format(account_id)
						Qury_str = (
							"select DISTINCT top "
							+ str(PerPage)
							+ " "
							+ str(select_obj_str)
							+ ",CpqTableEntryId from ( select TOP 10 ROW_NUMBER() OVER(order by "
							+ str(Wh_API_NAMEs)
							+ ") AS ROW, * from "
							+ str(ObjectName)
							+ " (nolock) "
							+ str(Qustr)
							+ " ) m where m.ROW BETWEEN "
							+ str(Page_start)
							+ " and "
							+ str(Page_End)
							+ ""
						)
						QuryCount_str = "select count(*) as cnt from " + str(ObjectName) + " (nolock) " + str(Qustr)
					##involved parties source fab ends
					elif str(RECORD_ID) == "SYOBJR-98859":                        
						Qustr += " AND PAR_SERVICE_ID = '"+str(TreeSuperParentParam)+"' AND GREENBOOK = '"+str(TreeParentParam)+"' "
						Qury_str = (
							"select DISTINCT top "
							+ str(PerPage)
							+ " "
							+ str(select_obj_str)
							+ ",CpqTableEntryId from ( select TOP 10 ROW_NUMBER() OVER(order by "
							+ str(Wh_API_NAMEs)
							+ ") AS ROW, * from "
							+ str(ObjectName)
							+ " (nolock) "
							+ str(Qustr)
							+ " ) m where m.ROW BETWEEN "
							+ str(Page_start)
							+ " and "
							+ str(Page_End)
							+ ""
						)                        
						QuryCount_str = "select count(*) as cnt from " + str(ObjectName) + " (nolock) " + str(Qustr)
					elif str(RECORD_ID) == "SYOBJR-98862":
						Qustr = " WHERE APP_ID = '"+str(TreeParentParam)+"' AND PROFILE_RECORD_ID ='"+str(RecAttValue)+"'"
						Qury_str = (
							"select DISTINCT top "
							+ str(PerPage)
							+ " "
							+ str(select_obj_str)
							+ ",CpqTableEntryId from ( select TOP 10 ROW_NUMBER() OVER(order by "
							+ str(Wh_API_NAMEs)
							+ ") AS ROW, * from "
							+ str(ObjectName)
							+ " (nolock) "
							+ str(Qustr)
							+ " ) m where m.ROW BETWEEN "
							+ str(Page_start)
							+ " and "
							+ str(Page_End)
							+ ""
						)                        
						QuryCount_str = "select count(*) as cnt from " + str(ObjectName) + " (nolock) " + str(Qustr)
					elif str(RECORD_ID) == "SYOBJR-98863":
						Qustr = " WHERE TAB_ID = '"+str(TreeParentParam)+"' AND PROFILE_RECORD_ID ='"+str(RecAttValue)+"'"
						Qury_str = (
							"select DISTINCT top "
							+ str(PerPage)
							+ " "
							+ str(select_obj_str)
							+ ",CpqTableEntryId from ( select TOP 10 ROW_NUMBER() OVER(order by "
							+ str(Wh_API_NAMEs)
							+ ") AS ROW, * from "
							+ str(ObjectName)
							+ " (nolock) "
							+ str(Qustr)
							+ " ) m where m.ROW BETWEEN "
							+ str(Page_start)
							+ " and "
							+ str(Page_End)
							+ ""
						)                        
						QuryCount_str = "select count(*) as cnt from " + str(ObjectName) + " (nolock) " + str(Qustr)
					elif str(RECORD_ID) == "SYOBJR-98864":
						Qustr = " WHERE TAB_NAME = '"+str(TreeParentParam)+"' AND PROFILE_RECORD_ID ='"+str(RecAttValue)+"'"
						Qury_str = (
							"select DISTINCT top "
							+ str(PerPage)
							+ " "
							+ str(select_obj_str)
							+ ",CpqTableEntryId from ( select TOP 10 ROW_NUMBER() OVER(order by "
							+ str(Wh_API_NAMEs)
							+ ") AS ROW, * from "
							+ str(ObjectName)
							+ " (nolock) "
							+ str(Qustr)
							+ " ) m where m.ROW BETWEEN "
							+ str(Page_start)
							+ " and "
							+ str(Page_End)
							+ ""
						)
						
						QuryCount_str = "select count(*) as cnt from " + str(ObjectName) + " (nolock) " + str(Qustr)
					elif str(RECORD_ID) == "SYOBJR-93123":
						app_ObjectName = Sql.GetFirst("select PRIMARY_OBJECT_NAME FROM SYTABS INNER JOIN SYAPPS ON SYTABS.APP_LABEL = SYAPPS.APP_LABEL WHERE SYTABS.TAB_LABEL = '"+str(TopTreeSuperParentParam)+"' AND SYAPPS.APP_LABEL = '"+str(TreeSecondSuperTopParentParam)+"'")
						Qustr = " WHERE SECTION_NAME = '"+str(TreeParentParam)+"' AND PROFILE_RECORD_ID ='"+str(RecAttValue)+"' "
						Qury_str = (
							"select DISTINCT top "
							+ str(PerPage)
							+ " "
							+ str(select_obj_str)
							+ ",CpqTableEntryId from ( select TOP 10 ROW_NUMBER() OVER(order by "
							+ str(Wh_API_NAMEs)
							+ ") AS ROW, * from "
							+ str(ObjectName)
							+ " (nolock) "
							+ str(Qustr)
							+ " ORDER BY SECTION_FIELD_ID ASC ) m where m.ROW BETWEEN "
							+ str(Page_start)
							+ " and "
							+ str(Page_End)
							+ ""
						)
						
						QuryCount_str = "select count(*) as cnt from " + str(ObjectName) + " (nolock) " + str(Qustr)    
					elif str(RECORD_ID) == "SYOBJR-98784" and TreeFirstSuperTopParentParam == "Pages":
						Qustr = " WHERE SECTION_NAME = '"+str(TreeParentParam)+"' AND TAB_NAME = '"+str(TreeSecondSuperTopParentParam)+"'"
						Qury_str = (
							"select DISTINCT top "
							+ str(PerPage)
							+ " "
							+ str(select_obj_str)
							+ ",CpqTableEntryId from ( select TOP 10 ROW_NUMBER() OVER(order by "
							+ str(Wh_API_NAMEs)
							+ ") AS ROW, * from "
							+ str(ObjectName)
							+ " (nolock) "
							+ str(Qustr)
							+ " ) m where m.ROW BETWEEN "
							+ str(Page_start)
							+ " and "
							+ str(Page_End)
							+ ""
						)
						
						QuryCount_str = "select count(*) as cnt from " + str(ObjectName) + " (nolock) " + str(Qustr)
					elif str(RECORD_ID) == "SYOBJR-93188":						
						RecAttValue = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00128").GetValue()
						GetAppname_query = ""
						Qustr = " WHERE TAB_NAME = '"+str(TreeParentParam)+"' AND PROFILE_ID ='"+str(RecAttValue)+"'"
						Qury_str = (
							"select DISTINCT top "
							+ str(PerPage)
							+ " "
							+ str(select_obj_str)
							+ ",CpqTableEntryId from ( select TOP 10 ROW_NUMBER() OVER(order by "
							+ str(Wh_API_NAMEs)
							+ ") AS ROW, * from "
							+ str(ObjectName)
							+ " (nolock) "
							+ str(Qustr)
							+ " ) m where m.ROW BETWEEN "
							+ str(Page_start)
							+ " and "
							+ str(Page_End)
							+ ""
						)
						
						QuryCount_str = "select count(*) as cnt from " + str(ObjectName) + " (nolock) " + str(Qustr)
					elif str(RECORD_ID) == "SYOBJR-95825" and str(TreeParentParam) == 'Constraints':
						Qustr = "WHERE CONSTRAINT_TYPE = '"+str(TreeParam)+"' AND OBJECT_RECORD_ID='"+str(RecAttValue)+"'" 
						Qury_str = (
							"select DISTINCT top "
							+ str(PerPage)
							+ " "
							+ str(select_obj_str)
							+ ",CpqTableEntryId from ( select TOP 10 ROW_NUMBER() OVER(order by "
							+ str(Wh_API_NAMEs)
							+ ") AS ROW, * from "
							+ str(ObjectName)
							+ " (nolock) "
							+ str(Qustr)
							+ " ) m where m.ROW BETWEEN "
							+ str(Page_start)
							+ " and "
							+ str(Page_End)
							+ ""
						)
						
						QuryCount_str = "select count(*) as cnt from " + str(ObjectName) + " (nolock) " + str(Qustr)
					elif str(RECORD_ID) == "SYOBJR-98834":
						#contract_quote_record_id = Product.GetGlobal("contract_quote_record_id")
						contract_quote_record_id = Quote.GetGlobal("contract_record_id")						
						Qustr = "where  CONTRACT_RECORD_ID = '"+str(contract_quote_record_id)+"'"
						Qury_str = (
							"select DISTINCT top "
							+ str(PerPage)
							+ " "
							+ str(select_obj_str)
							+ ",CpqTableEntryId from ( select TOP 10 ROW_NUMBER() OVER(order by "
							+ str(Wh_API_NAMEs)
							+ ") AS ROW, * from "
							+ str(ObjectName)
							+ " (nolock) "
							+ str(Qustr)
							+ " ) m where m.ROW BETWEEN "
							+ str(Page_start)
							+ " and "
							+ str(Page_End)
							+ ""
						)						
						QuryCount_str = "select count(*) as cnt from " + str(ObjectName) + " (nolock) " + str(Qustr)
					elif str(RECORD_ID) == "SYOBJR-98817":											
						#contract_quote_record_id = Product.GetGlobal("contract_quote_record_id")
						contract_quote_record_id = Quote.GetGlobal("contract_record_id")						
						ct_rec_id= Sql.GetList("SELECT CONTRACT_ID FROM CTCFBL (NOLOCK) WHERE CONTRACT_RECORD_ID ='"+str(contract_quote_record_id)+"'")						
						Qustr = "where  CONTRACT_RECORD_ID = '"+str(contract_quote_record_id)+"'"
						Qury_str = (
							"select DISTINCT top "
							+ str(PerPage)
							+ " "
							+ str(select_obj_str)
							+ ",CpqTableEntryId from ( select TOP 10 ROW_NUMBER() OVER(order by "
							+ str(Wh_API_NAMEs)
							+ ") AS ROW, * from "
							+ str(ObjectName)
							+ " (nolock) "
							+ str(Qustr)
							+ " ) m where m.ROW BETWEEN "
							+ str(Page_start)
							+ " and "
							+ str(Page_End)
							+ ""
						)						
						QuryCount_str = "select count(*) as cnt from " + str(ObjectName) + " (nolock) " + str(Qustr)
					else:
						if  str(RECORD_ID) == "SYOBJR-98789" and "Sending Account -" in TreeParam :
							Qustr += " AND RELOCATION_FAB_TYPE = 'SENDING FAB'"
						elif  str(RECORD_ID) == "SYOBJR-98789" and "Receiving Account -" in TreeParam :
							Qustr += " AND RELOCATION_FAB_TYPE = 'RECEIVING FAB'"
						elif str(RECORD_ID) == "SYOBJR-98868":
							Qustr += "AND EQUIPMENT_ID = '"+str(equipment_id)+"'"
							Qustr += "AND SERVICE_ID = '"+str(TreeParentParam)+"'"
						elif str(RECORD_ID) == "SYOBJR-00029":
							quote_rec_id = Product.GetGlobal("contract_quote_record_id")
							quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
							if TreeSuperParentParam == "Product Offerings":
								service_id = TreeParam.split('-')[0]	
								if subTab == "New Parts":	
									Qustr += " AND PAR_SERVICE_ID = '"+str(service_id)+"' AND NEW_PART = 'True'"
								elif subTab == "Inclusions":
									Qustr += " AND PAR_SERVICE_ID = '"+str(service_id)+"' AND NEW_PART = 'False' AND INCLUDED = 1"	
								elif subTab == "Exclusions":
									Qustr += " AND PAR_SERVICE_ID = '"+str(service_id)+"' AND NEW_PART = 'False' AND INCLUDED = 0"	
							elif TopTreeSuperParentParam == "Product Offerings":
								service_id = TreeParentParam.split('-')[0]
								if subTab == "New Parts":
									Qustr += " AND PAR_SERVICE_ID = '"+str(service_id)+"' AND GREENBOOK = '"+str(TreeParam)+"' AND NEW_PART = 'True'"	
								elif subTab == "Inclusions":
									Qustr += " AND PAR_SERVICE_ID = '"+str(service_id)+"' AND GREENBOOK = '"+str(TreeParam)+"' AND NEW_PART = 0 AND INCLUDED = 1"
								elif subTab == "Exclusions":
									Qustr += " AND PAR_SERVICE_ID = '"+str(service_id)+"' AND GREENBOOK = '"+str(TreeParam)+"' AND NEW_PART = 'False' AND INCLUDED = 0"														
										
						if str(RECORD_ID) == "SYOBJR-98874" or str(RECORD_ID) == "SYOBJR-98873":
							Qustr += " AND LINE = '"+str(line_item)+"'"
						if str(RECORD_ID) == "SYOBJR-98880":
							Qustr += " AND GREENBOOK = '"+str(TreeParentParam)+"'"
						if str(RECORD_ID) == "SYOBJR-98875":
							quote_item_revision_rec_id = Product.GetGlobal('get_quote_item_service')							
							get_gb_val = Sql.GetFirst("SELECT GREENBOOK FROM SAQRIT where QUOTE_REVISION_CONTRACT_ITEM_ID= '"+str(quote_item_revision_rec_id)+"'")
							if get_gb_val:
								Qustr += "AND QTEITM_RECORD_ID = '"+str(quote_item_revision_rec_id)+"' AND GREENBOOK = '"+str(get_gb_val.GREENBOOK)+"'"
						if str(RECORD_ID) == "SYOBJR-98872":
							Wh_API_NAMEs +=",LINE"
						if str(RECORD_ID) not in("SYOBJR-98869","SYOBJR-00643","SYOBJR-00013","SYOBJR-98825","SYOBJR-00016"):
							Qustr += " AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"'"
						
						Qury_str = (
							"select DISTINCT top "
							+ str(PerPage)
							+ " "
							+ str(select_obj_str)
							+ ",CpqTableEntryId from ( select TOP 10 ROW_NUMBER() OVER(order by "
							+ str(Wh_API_NAMEs)
							+ ") AS ROW, * from "
							+ str(ObjectName)
							+ " (nolock) "
							+ str(Qustr)
							+ " ) m where m.ROW BETWEEN "
							+ str(Page_start)
							+ " and "
							+ str(Page_End)
							+ ""
						)
						
						QuryCount_str = "select count(*) as cnt from " + str(ObjectName) + " (nolock) " + str(Qustr)

				if RECORD_ID == "SYOBJR-94442" and str(current_tab) == "Tab":                    
					Qury_str = (
						"SELECT TOP "
						+ str(PerPage)
						+ " * FROM (SELECT ROW_NUMBER() OVER (ORDER BY RECORD_ID DESC) AS ROW,RECORD_ID,ACTION_NAME,TAB_NAME,ATTRIBUTE_NAME,ACTVIS_VARIABLE_RECORD_ID,SCRIPT_RECORD_ID,TAB_RECORD_ID,CpqTableEntryId FROM SYPSAC WHERE TAB_RECORD_ID = '"
						+ str(RecAttValue)
						+ "' GROUP BY RECORD_ID,ACTION_NAME,TAB_NAME,ATTRIBUTE_NAME,ACTVIS_VARIABLE_RECORD_ID,SCRIPT_RECORD_ID,TAB_RECORD_ID,CpqTableEntryId) m WHERE m.ROW BETWEEN "
						+ str(Page_start)
						+ " AND "
						+ str(Page_End)
					)
					QuryCount_str = "SELECT COUNT(*) AS cnt FROM SYPSAC WHERE TAB_RECORD_ID = '" + str(RecAttValue) + "'"
				if RECORD_ID == "SYOBJR-94443" and str(current_tab) == "Tab":                    
					Qury_str = (
						"SELECT TOP "
						+ str(PerPage)
						+ " * FROM (SELECT ROW_NUMBER() OVER (ORDER BY SE.RECORD_ID DESC) AS ROW,SE.RECORD_ID,SE.SECTION_NAME,PG.TAB_NAME,SE.ATTRIBUTE_NAME,PG.TAB_RECORD_ID,SE.CpqTableEntryId FROM SYSECT (nolock) SE INNER JOIN SYPAGE (nolock) PG on SE.PAGE_RECORD_ID = PG.RECORD_ID WHERE PG.TAB_RECORD_ID = '"
						+ str(RecAttValue)
						+ "' GROUP BY SE.RECORD_ID,SE.SECTION_NAME,PG.TAB_NAME,SE.ATTRIBUTE_NAME,PG.TAB_RECORD_ID,SE.CpqTableEntryId) m WHERE m.ROW BETWEEN "
						+ str(Page_start)
						+ " AND "
						+ str(Page_End)
					)
					QuryCount_str = (
						"SELECT COUNT(SE.CpqTableEntryId) AS cnt FROM SYSECT (nolock) SE INNER JOIN SYPAGE (nolock) PG on SE.PAGE_RECORD_ID = PG.RECORD_ID WHERE PG.TAB_RECORD_ID = '"
						+ str(RecAttValue)
						+ "'"
					)
				elif RECORD_ID == 'SYOBJR-00006' and TreeParam == "Quote Preview":
					
					Qury_str = (
					"SELECT DISTINCT TOP "
					+ str(PerPage)
					+ " QUOTE_ITEM_FORECAST_PART_RECORD_ID,PART_NUMBER,MATPRIGRP_ID,PART_DESCRIPTION,BASEUOM_ID,SCHEDULE_MODE,DELIVERY_MODE,UNIT_PRICE,EXTENDED_PRICE,ANNUAL_QUANTITY,PRICING_STATUS,CUSTOMER_PART_NUMBER_RECORD_ID,BASEUOM_RECORD_ID,MATPRIGRP_RECORD_ID,QTEITM_RECORD_ID,QUOTE_RECORD_ID,QTEREV_RECORD_ID,SALESORG_RECORD_ID,SERVICE_RECORD_ID,PART_RECORD_ID,SALESUOM_RECORD_ID,CpqTableEntryId,TAX,TAX_PERCENTAGE,SERVICE_ID,SRVTAXCLA_DESCRIPTION from ( select TOP "+ str(PerPage)+" ROW_NUMBER() OVER(order by "+ str(Wh_API_NAMEs) +") AS ROW, * from SAQIFP (nolock)  where QUOTE_RECORD_ID ='"+str(RecAttValue)
					+"' AND QTEREV_RECORD_ID = '"
					+str(quote_revision_record_id)
					+"') m where m.ROW BETWEEN "
					+ str(Page_start)
					+ " AND "
					+ str(Page_End)+" "
					)
					QuryCount_str = (
						"SELECT COUNT(CpqTableEntryId) AS cnt FROM SAQIFP (nolock) WHERE QUOTE_RECORD_ID = '"
						+ str(RecAttValue)
						+ "' AND QTEREV_RECORD_ID = '"
						+ str(quote_revision_record_id)+"' "
					)
				elif RECORD_ID == 'SYOBJR-98869' and TreeParam == "Revisions":
					Qury_str = ("select DISTINCT TOP "
						+ str(PerPage)
						+ " QUOTE_REVISION_RECORD_ID,CONCAT(QUOTE_ID, '-', QTEREV_ID) AS QTEREV_ID,REVISION_DESCRIPTION,REV_CREATE_DATE,REV_EXPIRE_DATE,REVISION_STATUS,ACTIVE,CONTRACT_VALID_FROM,CONTRACT_VALID_TO,SALESORG_RECORD_ID,QUOTE_RECORD_ID,CpqTableEntryId from ( select TOP "+ str(PerPage)+" ROW_NUMBER() OVER(order by QUOTE_RECORD_ID) AS ROW, * from SAQTRV (nolock)  where QUOTE_RECORD_ID = '" 
						+ str(contract_quote_record_id) + "' ) m where m.ROW BETWEEN "
						+ str(Page_start)
						+ " and "
						+ str(Page_End)
						+ ""
					)
					QuryCount_str = (
						"select count(U.QUOTE_REVISION_RECORD_ID) as cnt from SAQTRV U (nolock) where  U.QUOTE_RECORD_ID = '"
						+ str(contract_quote_record_id)
						+ "'  "
					)
				elif RECORD_ID == 'SYOBJR-00010':
					imgstr = '<img title="Acquired" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Green_Tick.svg>'
					acquiring_img_str = '<img title="Acquiring" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Cloud_Icon.svg>'
					cps_pricing_img = ""
					#cps_pricing_img ="<a href=''#'' onclick=''cps_pricing_call(this)''><img src=''/mt/APPLIEDMATERIALS_TST/Additionalfiles/info.png''  style=''height: 15px; width: 15px; background-size: 20px 20px;''> </a>" 
					error = '<img title="Error" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/exclamation_icon.svg>'
					Qury_str = (
						"SELECT DISTINCT TOP "
						+ str(PerPage)
						+ " QUOTE_ITEM_FORECAST_PART_RECORD_ID, CASE WHEN PRICING_STATUS = 'ACQUIRED' THEN '"+ imgstr +"'  WHEN PRICING_STATUS = 'ERROR' THEN '" +error+ "' ELSE '"+ acquiring_img_str +"' END AS PRICING_STATUS,SERVICE_ID,CONCAT('"+cps_pricing_img+ "',PART_NUMBER) AS PART_NUMBER,MATPRIGRP_ID,PART_DESCRIPTION,BASEUOM_ID,SCHEDULE_MODE,DELIVERY_MODE,UNIT_PRICE,UNIT_PRICE_INGL_CURR,EXTENDED_PRICE,EXTPRI_INGL_CURR,ANNUAL_QUANTITY,CUSTOMER_PART_NUMBER_RECORD_ID,BASEUOM_RECORD_ID,MATPRIGRP_RECORD_ID,QTEITM_RECORD_ID,QUOTE_RECORD_ID,QTEREV_RECORD_ID,SALESORG_RECORD_ID,SERVICE_RECORD_ID,PART_RECORD_ID,SALESUOM_RECORD_ID,CpqTableEntryId,TAX,SRVTAXCLA_DESCRIPTION,TAX_PERCENTAGE from ( select TOP "+ str(PerPage)+" ROW_NUMBER() OVER(order by "+ str(Wh_API_NAMEs) +") AS ROW, * from SAQIFP (nolock)  where QUOTE_RECORD_ID ='"+str(RecAttValue)
						+"' AND QTEREV_RECORD_ID = '"
						+str(quote_revision_record_id)
						+"') m where m.ROW BETWEEN "
						+ str(Page_start)
						+ " AND "
						+ str(Page_End)+" ORDER BY PRICING_STATUS ASC"
					)
					QuryCount_str = (
						"SELECT COUNT(CpqTableEntryId) AS cnt FROM SAQIFP (nolock) WHERE QUOTE_RECORD_ID = '"
						+ str(RecAttValue)
						+ "' AND QTEREV_RECORD_ID = '"
						+ str(quote_revision_record_id)
						+"'"
					)

				elif RECORD_ID == 'SYOBJR-00008':
					imgstr = '<img title="Acquired" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Green_Tick.svg>'
					acquiring_img_str = '<img title="Acquiring" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Cloud_Icon.svg>'
					exclamation = '<img title="Approval Required" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/clock_exe.svg>'

					if getyears == 1:
						col_year =  'YEAR_1'
					elif getyears == 2:
						col_year =  'YEAR_1,YEAR_2'
					elif getyears == 3:
						col_year =  'YEAR_1,YEAR_2,YEAR_3'
					elif getyears == 4:
						col_year =  'YEAR_1,YEAR_2,YEAR_3,YEAR_4'
					else:
						col_year = 'YEAR_1,YEAR_2,YEAR_3,YEAR_4,YEAR_5'
					price_status = []
					# quote_itm_rec = Sql.GetFirst("SELECT QUOTE_ITEM_RECORD_ID FROM SAQITM (NOLOCK) "+str(Qustr)+"")
					# if str(getQuotetype).upper() == "ZWK1 - SPARES":
					# 	quote_item_obj = Sql.GetFirst("SELECT PRICING_STATUS FROM SAQITM (NOLOCK) "+str(Qustr)+"")
					# 	if quote_item_obj:
					# 		if quote_item_obj.PRICING_STATUS == 'ACQUIRED':
					# 			icon = '<img title="Acquired" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Green_Tick.svg>'
					# 		else:
					# 			icon = '<img title="Acquiring" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Cloud_Icon.svg>'
					# else:
					SAQICO_status = Sql.GetList("SELECT DISTINCT STATUS FROM SAQICO (NOLOCK) "+str(Qustr)+"")
					for pricing_status in SAQICO_status:
						price_status.append(pricing_status.STATUS)


						
						all_acquired = ["ACQUIRING","APPROVAL REQUIRED","ERROR"]
						all_error = ["APPROVAL REQUIRED","ACQUIRING","ACQUIERD"]
						all_required = ["ACQUIERD","ACQUIRING","ERROR"]
						all_acquiring = ["ACQUIERD","ERROR","APPROVAL REQUIRED"]
						acq_error = ["ACQUIERD","ERROR"]
						acq_req = ["ACQUIERD","APPROVAL REQUIRED"]
						not_acq_req = ["ACQUIRING","ERROR"]
						acq_error_approval = ["ACQUIERD","ERROR","APPROVAL"]
						not_acq_error = ["ACQUIRING","APPROVAL REQUIRED"]

						if "ACQUIRED" in price_status and ('ACQUIRING' not in price_status and 'APPROVAL REQUIRED' not in price_status and 'ERROR' not in price_status):
							icon = '<img title="Acquired" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Green_Tick.svg>'
						elif "ERROR" in price_status and ('ACQUIRED' not in price_status and 'APPROVAL REQUIRED' not in price_status and 'ACQUIRING' not in price_status):
							icon = '<img title="Error" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/exclamation_icon.svg>'
						elif "APPROVAL REQUIRED" in price_status and ('ACQUIRED' not in price_status and 'ERROR' not in price_status and 'ACQUIRING' not in price_status):
							icon = '<img title="Approval Required" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/clock_exe.svg>'
						elif "ACQUIRING" in price_status and 'ACQUIRED' not in price_status and 'ERROR' not in price_status and 'APPROVAL REQUIRED' not in price_status:
							icon = '<img title="Acquiring" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Cloud_Icon.svg>'
						elif ("ACQUIRED" in price_status and "ERROR" in price_status) and ('ACQUIRING' not in price_status and 'APPROVAL REQUIRED' not in price_status):
							icon = '<img title="Error" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/exclamation_icon.svg>'
						elif ("ACQUIRED" in price_status and "ACQUIRING" in price_status) and ('ERROR' not in price_status and 'APPROVAL REQUIRED' not in price_status):
							icon = '<img title="Acquiring" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Cloud_Icon.svg>'
						elif ("ACQUIRED" in price_status and "APPROVAL REQUIRED" in price_status) and ('ERROR' not in price_status and 'ACQUIRING' not in price_status):
							icon = '<img title="Approval Required" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/clock_exe.svg>'
						elif ("ACQUIRED" in price_status and 'ERROR' in price_status and 'APPROVAL REQUIRED' in price_status) and "ACQUIRING" not in price_status :
							icon = '<img title="Error" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/exclamation_icon.svg>'
						elif ("ACQUIRING" in price_status and 'APPROVAL REQUIRED' in price_status) and ('ACQUIRED' not in price_status and "ERROR" not in price_status) :
							icon = '<img title="Acquiring" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/clock_exe.svg>'
						else:
							icon = '<img title="Error" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/exclamation_icon.svg>'
					

					if TreeParam == "Quote Items":                        
						
						Qury_str = (
							"select DISTINCT top "
							+ str(PerPage)
							+ " '"+ icon +"' AS PO_NOTES, QUOTE_ITEM_RECORD_ID, LINE_ITEM_ID, SERVICE_ID, SERVICE_DESCRIPTION, OBJECT_QUANTITY, QUANTITY,TOTAL_COST, ONSITE_PURCHASE_COMMIT, SALES_DISCOUNT_PRICE,SRVTAXCLA_DESCRIPTION,TAX_PERCENTAGE,TAX, NET_VALUE, TARGET_PRICE, CEILING_PRICE, BD_PRICE, BD_PRICE_MARGIN, DISCOUNT, NET_PRICE, YEAR_OVER_YEAR, "+col_year+" "
							+ ",CpqTableEntryId from ( select TOP 10 ROW_NUMBER() OVER(order by "
							+ str(Wh_API_NAMEs)
							+ ") AS ROW, * from "
							+ str(ObjectName)
							+ " (nolock) "
							+ str(Qustr)
							+ " ) m where m.ROW BETWEEN "
							+ str(Page_start)
							+ " and "
							+ str(Page_End)
							+ ""
						)
						QuryCount_str = "select count(*) as cnt from " + str(ObjectName) + " (nolock) " + str(Qustr)
					
				elif RECORD_ID == 'SYOBJR-00024':                    
					quote_obj = Sql.GetFirst("select QUOTE_ID,MASTER_TABLE_QUOTE_RECORD_ID from SAQTMT where MASTER_TABLE_QUOTE_RECORD_ID = '{contract_quote_record_id}' AND QTEREV_RECORD_ID='{revision_rec_id}'".format(contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id"), revision_rec_id = quote_revision_record_id))
					quote_id = quote_obj.QUOTE_ID
					TreeParam = Product.GetGlobal("TreeParam")
					TreeParentParam = Product.GetGlobal("TreeParentLevel0")
					try:
						chain_step_name = subTab.split(':')[1].strip()
						
						step_id = chain_step_name.split(' ')[1]
						
					except:
						step_id=""
						
					dynamic_condtn=""
					round_value=""
					if TreeSuperParentParam == 'Approvals':
						round_value = TreeParam.split()[1]
						dynamic_condtn=" and ACAPTX.APRCHNSTP_ID = '{chain_step_name}' and ACAPTX.APPROVAL_ROUND = '{step_value}'".format(chain_step_name = step_id,step_value = round_value)
					Qury_str = ("""select DISTINCT top {PerPage} * from (select ROW_NUMBER() OVER( ORDER BY ACAPTX.APRCHNSTP_ID) AS ROW,ACAPTX.APPROVAL_TRANSACTION_RECORD_ID, ACAPTX.APPROVAL_ID,ACAPTX.APRCHNSTP_ID,ACAPTX.APRCHNSTP_APPROVER_ID,ACAPTX.APPROVAL_ROUND,ACAPTX.APPROVALSTATUS,ACAPTX.RECIPIENT_COMMENTS,ACAPTX.APRCHNSTP_RECORD_ID,ACAPTX.APPROVAL_RECIPIENT,ACAPTX.CpqTableEntryId FROM ACAPTX (nolock) inner join ACACST (nolock) on ACAPTX.APRCHNSTP_RECORD_ID = ACACST.APPROVAL_CHAIN_STEP_RECORD_ID  and ACAPTX.APRTRXOBJ_ID = '{Quote_id}' and ACAPTX.APRCHNSTPTRX_ID like '%{Quote_id}%' and ACAPTX.APRCHN_ID = '{chain_id}' {dynamic_condtn})m where m.ROW BETWEEN """.format(PerPage = PerPage,contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id"),Quote_id = quote_id,dynamic_condtn=dynamic_condtn,chain_id=TreeParentParam if TreeSuperParentParam == 'Approvals' else TreeParam) + str(Page_start) + " and " + str(Page_End))
					QuryCount_str = """select count(ACAPTX.CpqTableEntryId) as cnt FROM ACAPTX (nolock) inner join ACACST (nolock) on ACAPTX.APRCHNSTP_RECORD_ID = ACACST.APPROVAL_CHAIN_STEP_RECORD_ID and  ACAPTX.APRTRXOBJ_ID = '{Quote_id}' and ACAPTX.APRCHNSTPTRX_ID like '%{Quote_id}%' and ACAPTX.APRCHN_ID = '{chain_id}' {dynamic_condtn}""".format(contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id"),Quote_id = quote_id,dynamic_condtn=dynamic_condtn,chain_id=TreeParentParam if TreeSuperParentParam == 'Approvals' else TreeParam)
			
				##involved parties source fab starts
				elif (str(RECORD_ID) == "SYOBJR-98857") and str(TreeParam) == "Quote Information":
					account_id = Product.GetGlobal("stp_account_id")                    
					Qustr += " AND SRCACC_ID = '{}'".format(account_id)
					Qury_str = (
						"select DISTINCT top "
						+ str(PerPage)
						+ " "
						+ str(select_obj_str)
						+ ",CpqTableEntryId from ( select TOP 10 ROW_NUMBER() OVER(order by "
						+ str(Wh_API_NAMEs)
						+ ") AS ROW, * from "
						+ str(ObjectName)
						+ " (nolock) "
						+ str(Qustr)
						+ " ) m where m.ROW BETWEEN "
						+ str(Page_start)
						+ " and "
						+ str(Page_End)
						+ ""
					)
					
					
					
					QuryCount_str = "select count(*) as cnt from " + str(ObjectName) + " (nolock) " + str(Qustr)
				##involved parties source fab ends
				elif str(RECORD_ID) == "SYOBJR-98859":
					Qury_str = (
						"select DISTINCT top "
						+ str(PerPage)
						+ " "
						+ str(select_obj_str)
						+ ",CpqTableEntryId from ( select TOP 10 ROW_NUMBER() OVER(order by "
						+ str(Wh_API_NAMEs)
						+ ") AS ROW, * from "
						+ str(ObjectName)
						+ " (nolock) "
						+ str(Qustr)
						+ " ) m where m.ROW BETWEEN "
						+ str(Page_start)
						+ " and "
						+ str(Page_End)
						+ ""
					)
					
					QuryCount_str = "select count(*) as cnt from " + str(ObjectName) + " (nolock) " + str(Qustr)
				elif str(RECORD_ID) == "SYOBJR-98862":
					Qustr = " WHERE APP_ID = '"+str(TreeParentParam)+"' AND PROFILE_RECORD_ID ='"+str(RecAttValue)+"'"
					Qury_str = (
						"select DISTINCT top "
						+ str(PerPage)
						+ " "
						+ str(select_obj_str)
						+ ",CpqTableEntryId from ( select TOP 10 ROW_NUMBER() OVER(order by "
						+ str(Wh_API_NAMEs)
						+ ") AS ROW, * from "
						+ str(ObjectName)
						+ " (nolock) "
						+ str(Qustr)
						+ " ) m where m.ROW BETWEEN "
						+ str(Page_start)
						+ " and "
						+ str(Page_End)
						+ ""
					)
					
					QuryCount_str = "select count(*) as cnt from " + str(ObjectName) + " (nolock) " + str(Qustr)
				elif str(RECORD_ID) == "SYOBJR-98863":
					Qustr = " WHERE TAB_ID = '"+str(TreeParentParam)+"' AND PROFILE_RECORD_ID ='"+str(RecAttValue)+"'"
					Qury_str = (
						"select DISTINCT top "
						+ str(PerPage)
						+ " "
						+ str(select_obj_str)
						+ ",CpqTableEntryId from ( select TOP 10 ROW_NUMBER() OVER(order by "
						+ str(Wh_API_NAMEs)
						+ ") AS ROW, * from "
						+ str(ObjectName)
						+ " (nolock) "
						+ str(Qustr)
						+ " ) m where m.ROW BETWEEN "
						+ str(Page_start)
						+ " and "
						+ str(Page_End)
						+ ""
					)
					
					QuryCount_str = "select count(*) as cnt from " + str(ObjectName) + " (nolock) " + str(Qustr)
				
				elif str(RECORD_ID) == "SYOBJR-98864":
					Qustr = " WHERE TAB_NAME = '"+str(TreeParentParam)+"' AND PROFILE_RECORD_ID ='"+str(RecAttValue)+"'"
					Qury_str = (
						"select DISTINCT top "
						+ str(PerPage)
						+ " "
						+ str(select_obj_str)
						+ ",CpqTableEntryId from ( select TOP 10 ROW_NUMBER() OVER(order by "
						+ str(Wh_API_NAMEs)
						+ ") AS ROW, * from "
						+ str(ObjectName)
						+ " (nolock) "
						+ str(Qustr)
						+ " ) m where m.ROW BETWEEN "
						+ str(Page_start)
						+ " and "
						+ str(Page_End)
						+ ""
					)
					
					QuryCount_str = "select count(*) as cnt from " + str(ObjectName) + " (nolock) " + str(Qustr)
				elif str(RECORD_ID) == "SYOBJR-93123":
					TreeParentParam = Product.GetGlobal("TreeParentLevel0") 
					
					app_ObjectName = Sql.GetFirst("select PRIMARY_OBJECT_NAME FROM SYTABS INNER JOIN SYAPPS ON SYTABS.APP_LABEL = SYAPPS.APP_LABEL WHERE SYTABS.TAB_LABEL = '"+str(TopTreeSuperParentParam)+"' AND SYAPPS.APP_LABEL = '"+str(TreeSecondSuperTopParentParam)+"'")
					Qustr = " WHERE SECTION_NAME = '"+str(TreeParentParam)+"' AND PROFILE_ID ='"+str(RecAttValue)+"' AND OBJECT_NAME = '"+str(app_ObjectName.PRIMARY_OBJECT_NAME)+"' "
					Qury_str = (
						"select DISTINCT top "
						+ str(PerPage)
						+ " "
						+ str(select_obj_str)
						+ ",CpqTableEntryId from ( select TOP 10 ROW_NUMBER() OVER(order by "
						+ str(Wh_API_NAMEs)
						+ ") AS ROW, * from "
						+ str(ObjectName)
						+ " (nolock) "
						+ str(Qustr)
						+ " ORDER BY SECTION_FIELD_ID ASC ) m where m.ROW BETWEEN "
						+ str(Page_start)
						+ " and "
						+ str(Page_End)
						+ ""
						)
					QuryCount_str = "select count(*) as cnt from " + str(ObjectName) + " (nolock) " + str(Qustr)    
				elif str(RECORD_ID) == "SYOBJR-98784" and TreeFirstSuperTopParentParam == "Pages":
					Qustr = " WHERE SECTION_NAME = '"+str(TreeParentParam)+"' AND TAB_NAME = '"+str(TreeSecondSuperTopParentParam)+"'"
					Qury_str = (
						"select DISTINCT top "
						+ str(PerPage)
						+ " "
						+ str(select_obj_str)
						+ ",CpqTableEntryId from ( select TOP 10 ROW_NUMBER() OVER(order by "
						+ str(Wh_API_NAMEs)
						+ ") AS ROW, * from "
						+ str(ObjectName)
						+ " (nolock) "
						+ str(Qustr)
						+ " ) m where m.ROW BETWEEN "
						+ str(Page_start)
						+ " and "
						+ str(Page_End)
						+ ""
					)
					
					QuryCount_str = "select count(*) as cnt from " + str(ObjectName) + " (nolock) " + str(Qustr)
				elif str(RECORD_ID) == "SYOBJR-95985" and str(current_tab) == "Page":
					#tree_var = Sql.GetFirst("SELECT * FROM SYTREE WHERE PAGE_RECORD_ID = '"+str(RecAttValue)+"'") 
					
					Qustr = "WHERE TREE_NAME = '"+str(TreeParentParam)+"' "
					Qury_str = (
						"select DISTINCT top "
						+ str(PerPage)
						+ " "
						+ str(select_obj_str)
						+ ",CpqTableEntryId from ( select TOP 10 ROW_NUMBER() OVER(order by "
						+ str(Wh_API_NAMEs)
						+ ") AS ROW, * from "
						+ str(ObjectName)
						+ " (nolock) "
						+ str(Qustr)
						+ " ) m where m.ROW BETWEEN "
						+ str(Page_start)
						+ " and "
						+ str(Page_End)
						+ ""
					)
					
					QuryCount_str = "select count(*) as cnt from " + str(ObjectName) + " (nolock) " + str(Qustr)
				elif str(RECORD_ID) == "SYOBJR-93188":					
					RecAttValue = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00128").GetValue()
					GetAppname_query = ""
					Qustr = " WHERE TAB_NAME = '"+str(TreeParentParam)+"' AND PROFILE_ID ='"+str(RecAttValue)+"'"
					Qury_str = (
						"select DISTINCT top "
						+ str(PerPage)
						+ " "
						+ str(select_obj_str)
						+ ",CpqTableEntryId from ( select TOP 10 ROW_NUMBER() OVER(order by "
						+ str(Wh_API_NAMEs)
						+ ") AS ROW, * from "
						+ str(ObjectName)
						+ " (nolock) "
						+ str(Qustr)
						+ " ) m where m.ROW BETWEEN "
						+ str(Page_start)
						+ " and "
						+ str(Page_End)
						+ ""
					)
					
					QuryCount_str = "select count(*) as cnt from " + str(ObjectName) + " (nolock) " + str(Qustr)
				elif str(RECORD_ID) == "SYOBJR-95825" and str(TreeParentParam) == 'Constraints':
						Qustr = "WHERE CONSTRAINT_TYPE = '"+str(TreeParam)+"' AND OBJECT_RECORD_ID ='"+str(RecAttValue)+"'" 
						Qury_str = (
							"select DISTINCT top "
							+ str(PerPage)
							+ " "
							+ str(select_obj_str)
							+ ",CpqTableEntryId from ( select TOP 10 ROW_NUMBER() OVER(order by "
							+ str(Wh_API_NAMEs)
							+ ") AS ROW, * from "
							+ str(ObjectName)
							+ " (nolock) "
							+ str(Qustr)
							+ " ) m where m.ROW BETWEEN "
							+ str(Page_start)
							+ " and "
							+ str(Page_End)
							+ ""
						)
						
						QuryCount_str = "select count(*) as cnt from " + str(ObjectName) + " (nolock) " + str(Qustr)
				elif RECORD_ID == 'SYOBJR-98841':
					imgstr = '<img title="Acquired" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Green_Tick.svg>'
					acquiring_img_str = '<img title="Acquiring" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Cloud_Icon.svg>'

					
					if TreeParam == "Cart Items":                       
						
						Qury_str = (
							"select DISTINCT top "
							+ str(PerPage)
							+ "  CASE WHEN ITEM_STATUS = 'ACQUIRED' THEN '"+ imgstr +"' ELSE '"+ imgstr +"' END AS PO_NOTES, CONTRACT_ITEM_RECORD_ID, LINE_ITEM_ID, SERVICE_ID, SERVICE_DESCRIPTION, QUANTITY, TAX, DISCOUNT, EXTENDED_PRICE"
							+ ",CpqTableEntryId from ( select TOP 10 ROW_NUMBER() OVER(order by "
							+ str(Wh_API_NAMEs)
							+ ") AS ROW, * from "
							+ str(ObjectName)
							+ " (nolock) "
							+ str(Qustr)
							+ " ) m where m.ROW BETWEEN "
							+ str(Page_start)
							+ " and "
							+ str(Page_End)
							+ ""
						)
						QuryCount_str = "select count(*) as cnt from " + str(ObjectName) + " (nolock) " + str(Qustr)

				elif RECORD_ID == 'SYOBJR-98792' and str(TreeParam) == "Quote Preview":
					
					if getyears == 1:
						col_year =  'YEAR_1'
					elif getyears == 2:
						col_year =  'YEAR_1,YEAR_2'
					elif getyears == 3:
						col_year =  'YEAR_1,YEAR_2,YEAR_3'
					elif getyears == 4:
						col_year =  'YEAR_1,YEAR_2,YEAR_3,YEAR_4'
					else:
						col_year = 'YEAR_1,YEAR_2,YEAR_3,YEAR_4,YEAR_5'
					Qury_str = (
						"select DISTINCT top "
						+ str(PerPage)
						+ " QUOTE_ITEM_RECORD_ID, LINE_ITEM_ID, SERVICE_ID, SERVICE_DESCRIPTION, ONSITE_PURCHASE_COMMIT, OBJECT_QUANTITY, TOTAL_COST, SALES_DISCOUNT_PRICE, TAX, NET_VALUE, QUANTITY, TARGET_PRICE, CEILING_PRICE, BD_PRICE, BD_PRICE_MARGIN, DISCOUNT, NET_PRICE, YEAR_OVER_YEAR, "+col_year+" , SRVTAXCLA_DESCRIPTION, TAX_PERCENTAGE, CpqTableEntryId from ( select TOP 10 ROW_NUMBER() OVER(order by "          
						
						+ str(Wh_API_NAMEs)
						+ ") AS ROW, * from "
						+ str(ObjectName)
						+ " (nolock) "
						+ str(Qustr)
						+ "  AND SERVICE_ID NOT LIKE '%BUNDLE%') m where m.ROW BETWEEN "
						+ str(Page_start)
						+ " and "
						+ str(Page_End)
						+ ""
					)
					
					QuryCount_str = "select count(*) as cnt from " + str(ObjectName) + " (nolock) " + str(Qustr) + " AND SERVICE_ID NOT LIKE '%BUNDLE%' "
				elif RECORD_ID == "SYOBJR-95555":
					Qury_str = (
						"select DISTINCT top "
						+ str(PerPage)
						+ " * from ( select TOP 10 ROW_NUMBER() OVER(order by CpqTableEntryId"
						+ ") AS ROW, * from "
						+ str(ObjectName)
						+ " (nolock) "
						+ str(Qustr)
						+ " AND GOT_CODE = '"+str(TreeParam)+"' ) m where m.ROW BETWEEN "
						+ str(Page_start)
						+ " and "
						+ str(Page_End)
						+ ""
					)
					
					QuryCount_str = "select count(*) as cnt from " + str(ObjectName) + " (nolock) " + str(Qustr) + " AND GOT_CODE = '"+str(TreeParam)+"' "
				elif RECORD_ID == "SYOBJR-95556":
					Qury_str = (
						"select DISTINCT top "
						+ str(PerPage)
						+ " * from ( select TOP 10 ROW_NUMBER() OVER(order by CpqTableEntryId"
						+ ") AS ROW, * from "
						+ str(ObjectName)
						+ " (nolock) "
						+ str(Qustr)
						+ " AND PM_ID = '"+str(TreeParam)+"' ) m where m.ROW BETWEEN "
						+ str(Page_start)
						+ " and "
						+ str(Page_End)
						+ ""
					)
					
					QuryCount_str = "select count(*) as cnt from " + str(ObjectName) + " (nolock) " + str(Qustr) + " AND PM_ID = '"+str(TreeParam)+"' "
				
				try:
					Query_Obj = Sql.GetList(str(Qury_str))
					
					
					QueryCount_Obj = Sql.GetFirst(str(QuryCount_str))
					
					if QueryCount_Obj is not None:
						QueryCount = QueryCount_Obj.cnt
						
				except:
					
					if OrderBy_obj is not None:
						if OrderBy_obj.ORDERS_BY:
							Wh_API_NAMEs = OrderBy_obj.ORDERS_BY
						else:
							Wh_API_NAMEs = lookup_disply_list123
					else:
						Wh_API_NAMEs = lookup_disply_list123
					Qury_str = (
						"select * from ( select ROW_NUMBER() OVER( order by "
						+ str(lookup_disply_list123)
						+ " ) AS ROW, * from "
						+ str(ObjectName)
						+ " (nolock) where 1=1 ) m where m.ROW BETWEEN "
						+ str(Page_start)
						+ " and "
						+ str(Page_End)
						+ ""
					)
					# Trace.Write(
					#     "LLLLL"
					#     + str(
					#         "select * from ( select ROW_NUMBER() OVER( order by "
					#         + str(lookup_disply_list123)
					#         + " ) AS ROW, * from "
					#         + str(ObjectName)
					#         + " (nolock) where 1=1 ) m where m.ROW BETWEEN "
					#         + str(Page_start)
					#         + " and "
					#         + str(Page_End)
					#         + ""
					#     )
					# )
					QuryCount_str = "select count(*) as cnt  from " + str(ObjectName) + " (nolock) where 1=1 "
					Query_Obj = Sql.GetList(Qury_str)
					
					QueryCount_Obj = Sql.GetFirst(str(QuryCount_str))
					if QueryCount_Obj is not None:
						QueryCount = QueryCount_Obj.cnt
			
			Trace.Write("CHKNG_QUERY_J "+str(Qury_str))
			if Query_Obj is not None:
				for ik in Query_Obj:					                  
					new_dict = {}
					ids = {}
					seg_pric = {}
					primary = ""
					primary_view = ""
					product_id = ""
					product_name = ""
					other_tab = ""
					key_value = ""
					decimal_place = 3                    
					product_id_val = ""
					editvalue = {}
					red_color = ""
					pop_val = {}
					list_lineup = []
					list_lineup1 = []
					
					if ObjectName != 'SAQIBP' and ObjectName != 'SAQDOC':
						Trace.Write("dropdown11==="+str(ObjectName))
						Action_str = '<div class="btn-group dropdown"><div class="dropdown" id="ctr_drop"><i data-toggle="dropdown" id="dropdownMenuButton" class="fa fa-sort-desc dropdown-toggle" aria-expanded="false"></i><ul class="dropdown-menu left empty_ctrdrop_ul" aria-labelledby="dropdownMenuButton">'
					elif ObjectName == "SAQDOC":
						Trace.Write("dropdown11==="+str(ObjectName))
						Action_str = '<div class="btn-group dropdown"><div class="dropdown" id="ctr_drop"><i data-toggle="dropdown" id="dropdownMenuButton" class="fa fa-sort-desc dropdown-toggle" aria-expanded="false"></i><ul class="dropdown-menu left empty_ctrdrop_ul" aria-labelledby="dropdownMenuButton">'
					
					else:
						Trace.Write("dropdown===")
						Action_str = '<div class="btn-group dropdown"><div class="dropdown" id="ctr_drop"><i data-toggle="dropdown" id="dropdownMenuButton" class="fa fa-sort-desc dropdown-toggle" aria-expanded="false"></i><ul class="dropdown-menu left empty_ctrdrop_ul" style="display: none;" aria-labelledby="dropdownMenuButton">'
					#Action_str = '<div class="btn-group dropdown"><div class="dropdown" id="ctr_drop"><i data-toggle="dropdown" id="dropdownMenuButton" class="fa fa-sort-desc dropdown-toggle" aria-expanded="false"></i><ul class="dropdown-menu left" aria-labelledby="dropdownMenuButton">'
					
					for inm in ik:
						value123 = str(inm).split(",")[0].replace("[", "").lstrip()
						value1234 = str(inm).split(",")[1].replace("]", "").lstrip()
						if (
							str(obj_obj.SAPCPQ_ATTRIBUTE_NAME) == "SYOBJR-30114"
							or str(obj_obj.SAPCPQ_ATTRIBUTE_NAME) == "SYOBJR-60052"
							or str(obj_obj.SAPCPQ_ATTRIBUTE_NAME) == "SYOBJR-70085"
						):
							if value123 == objRecName:
								other_tab = "0"
								primary_view = value1234

						else:
							if value123 == objRecName:
								tab_obj1 = Sql.GetFirst(
									"SELECT PG.TAB_NAME,PG.TAB_RECORD_ID FROM SYSECT (nolock) SE INNER JOIN SYPAGE (nolock) PG on SE.PAGE_RECORD_ID = PG.RECORD_ID WHERE SE.PRIMARY_OBJECT_NAME='"
									+ str(ObjectName)
									+ "' and SE.SECTION_NAME ='BASIC INFORMATION'"
								)
						
					if primary_view != "":                        
						if str(current_tab).upper() == "PROFILE" and (ObjectName != "SYPROD"):
							Action_str += (
								'<li><a class="dropdown-item" href="#" onclick="Commonteree_view_RL(this)">VIEW</a></li>'
							)
						elif str(current_tab).upper() == "PROFILE" and (ObjectName == "SYPROF"):
							Action_str += '<li><a class="dropdown-item" href="#" onclick="profileObjSet(this)" data-target="#viewProfileRelatedList" data-toggle="modal">VIEW<a><li>'
						elif ObjectName == "SAQTRV":
							quote_contract_recordId = Quote.GetGlobal("contract_quote_record_id")
							get_activerev = Sql.GetFirst("select * from SAQTRV where QUOTE_RECORD_ID = '"+str(quote_contract_recordId)+"' and ACTIVE =1 and CpqTableEntryId = '"+str(value1234)+"'")
							if get_activerev:
								Action_str += '<li><a id = "" class="dropdown-item" href="#" " onclick="edit_desc(this)">EDIT DESC</a></li>'
							else:
								Action_str += ''    

					else:                        
						if str(current_tab).upper() == "PROFILE" and (ObjectName == "SYPROF"):
							Action_str += '<li><a class="dropdown-item" href="#" onclick="profileObjSet(this)" data-target="#viewProfileRelatedList" data-toggle="modal">VIEW<a><li>'
						elif str(current_tab).upper() == "PROFILE" and (ObjectName != "SYPROF"):
							
							Action_str += (
								'<li><a class="dropdown-item" href="#" onclick="Commonteree_view_RL(this)"  >VIEW<a><li>'
							)
						elif ObjectName == "SAQTRV":							
							quote_contract_recordId = Quote.GetGlobal("contract_quote_record_id")
							get_activerev = Sql.GetFirst("select * from SAQTRV where QUOTE_RECORD_ID = '"+str(quote_contract_recordId)+"' and ACTIVE =1 and CpqTableEntryId = '"+str(value1234)+"'")
							if get_activerev:
								Action_str += '<li><a id = "" class="dropdown-item" href="#" " onclick="edit_desc(this)">EDIT DESC</a></li>'
							else:
								Action_str += '' 

						elif ObjectName == "SAQDOC":
							contract_quote_rec_id = Quote.GetGlobal("contract_quote_record_id")
							quote_revision_rec_id = Quote.GetGlobal("quote_revision_record_id")
							docnode_action_btn = Sql.GetFirst("SELECT DOCUMENT_DESCRIPTION FROM SAQDOC WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND QUOTE_DOCUMENT_RECORD_ID = '{}'".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_rec_id,ik.QUOTE_DOCUMENT_RECORD_ID))
							if docnode_action_btn:
								if str(docnode_action_btn.DOCUMENT_DESCRIPTION) == "" or docnode_action_btn.DOCUMENT_DESCRIPTION == "":
									Trace.Write("edit=====")
									Action_str += '<li><a id = "" class="dropdown-item" href="#" " onclick="doc_edit_desc(this)">EDIT DESC</a></li>'													
																	
						
						# elif str(current_tab).upper() == "APP" and str(ObjectName)=="SYTABS":                    
						#     Action_str += '<li><a class="dropdown-item" href="#" onclick="Move_to_parent_obj(this)">VIEW<a><li>'  
						# elif str(current_tab).upper() == "ROLE":
							# Action_str += '<li><a class="dropdown-item" href="#" onclick="Commonteree_view_RL(this)"  >VIEW<a><li>'
							
						else:
							#if ObjectName == "SAQSAO":
							#Action_str += '<li><a class="dropdown-item" href="#" onclick="Commonteree_view_RL(this)">VIEW</a></li>'
							if ObjectName== "SAQICT" :
								Action_str += '<li><a class="dropdown-item" href="#" onclick="Commonteree_view_RL(this)">VIEW CONTACT</a></li>'
							elif ObjectName== "SAQTIP":
								Action_str += '<li><a class="dropdown-item" href="#" onclick="Commonteree_view_RL(this)">VIEW ACCOUNT</a></li>'
							elif ObjectName == "SAQSPT":
								pass
							elif ObjectName != "SAQIBP":								
								Action_str += '<li><a class="dropdown-item" href="#" onclick="Commonteree_view_RL(this)">VIEW</a></li>'
							elif ObjectName == "SAQSAO":
								Action_str += '<li><a id = '' class="dropdown-item" href="#" onclick="Commonteree_view_RL(this)">VIEW</a></li>'
							elif ObjectName == "SAQRAT":
								Action_str += '<li><a id = '' class="dropdown-item" href="#" onclick="download_file(this)">DOWNLOAD</a></li>'
								
							


					
					if str(Action_permission.get("Edit")).upper() == "TRUE":
						if related_list_edit_permission:							
							if primary_view != "":								
								if other_tab == "1":
									Action_str += (
										'<li><a class="dropdown-item curptr"  href="../Configurator.aspx?pid='
										+ str(product_id_val)
										+ '" id = "'
										+ primary_view
										+ '"   onclick="Move_to_parent_obj_edit(this)">EDIT</a></li>'
									)
								elif other_tab != "0":
									Action_str += (
										'<li><a class="dropdown-item curptr" href="#" id = "'
										+ primary_view
										+ '"  onclick="Move_to_parent_obj_edit(this)">EDIT</a></li>'
									)

								elif str(current_tab).upper() == "PROFILE":
									Action_str += (
										'<li><a class="dropdown-item" href="#" onclick="Commontree_edit_RL(this)">EDIT</a></li>'
									)
								else:
									if str(current_tab).upper() == "PROFILE":
										Action_str += '<li><a class="dropdown-item" href="#" onclick="Commontree_edit_RL(this)">EDIT</a></li>'
									elif str(current_tab).upper() == "SYPROF":
										Action_str += '<li><a class="dropdown-item" href="#" data-toggle="modal" data-target="#viewProfileRelatedList" onclick="profileObjSetEdit(this)">EDIT</a></li>'
									else:
										Action_str += '<li><a class="dropdown-item" href="#" onclick="cont_openedit(this)" data-target="#cont_viewModalSection" data-toggle="modal">EDIT</a></li>'

							elif (
								ObjectName == "SYPRAP"
								or ObjectName == "SYPRTB"
								or ObjectName == "SYPRSN"
								or ObjectName == "SYPRAC"
							):
								Action_str += (
									'<li><a class="dropdown-item" href="#" onclick="Commontree_edit_RL(this)">EDIT</a></li>'
								)
							elif ObjectName == "SYPROF":
								Action_str += '<li><a class="dropdown-item" href="#" data-toggle="modal" data-target="#viewProfileRelatedList" onclick="profileObjSetEdit(this)">EDIT</a></li>'
							elif ObjectName == "SAQTRV":
								quote_contract_recordId = Quote.GetGlobal("contract_quote_record_id")
								get_activerev = Sql.GetFirst("select * from SAQTRV where QUOTE_RECORD_ID = '"+str(quote_contract_recordId)+"' and ACTIVE =1 and CpqTableEntryId = '"+str(value1234)+"'")
								get_expire_rev = Sql.GetFirst("select * from SAQTRV where QUOTE_RECORD_ID = '"+str(quote_contract_recordId)+"' and ACTIVE =0  AND (REV_EXPIRE_DATE = '"+str(current_date)+"' or REV_EXPIRE_DATE <= '"+str(current_date)+"' ) and CpqTableEntryId = '"+str(value1234)+"'")
								if get_activerev:
									Action_str += '<li><a class="dropdown-item" href="#" data-toggle="modal" data-target="" style="display: none;" onclick="set_as_active(this)">SET AS ACTIVE</a></li>'
								elif get_expire_rev:
									Action_str += ''	
								else:
									Action_str += '<li><a class="dropdown-item" href="#" data-toggle="modal" data-target="" onclick="set_as_active(this)">SET AS ACTIVE</a></li>'

							elif ObjectName == "SAQDOC":
								contract_quote_rec_id = Quote.GetGlobal("contract_quote_record_id")
								quote_revision_rec_id = Quote.GetGlobal("quote_revision_record_id")
								docnode_action_btn = Sql.GetFirst("SELECT * FROM SAQDOC WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND QUOTE_DOCUMENT_RECORD_ID = '{}' ".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_rec_id,ik.QUOTE_DOCUMENT_RECORD_ID))								
								#for date_value in docnode_action_btn:
								if docnode_action_btn:
									Trace.Write("act_btn=="+str(docnode_action_btn.DATE_SUBMITTED))						
									if str(docnode_action_btn.DATE_SUBMITTED) != "":
										Trace.Write("docnode=====")
										if str(docnode_action_btn.DATE_ACCEPTED) == "" and str(docnode_action_btn.DATE_REJECTED) == "":
											Trace.Write("2222222222222")
											Action_str += '<li><a id = "" class="dropdown-item" href="#" " onclick="customer_accepted(this)">CUSTOMER ACCEPTED</a></li>'									
											Action_str += '<li><a id = "" class="dropdown-item" href="#" " onclick="customer_rejected(this)">CUSTOMER REJECTED</a></li>'
									else:
										Trace.Write("docnode111=====")									
										Action_str += '<li><a id = "" class="dropdown-item" href="#" " onclick="submit_to_customer(this)">SUBMITTED TO CUSTOMER</a></li>'     
							elif ObjectName == "SAQDLT":
								Action_str += (
									'<li><a class="dropdown-item" href="#" onclick="replace_cont_manager(this)">REPLACE</a></li>'
								) 
							else:
								if str(current_tab).upper() == "PROFILE":
									Action_str += (
										'<li><a class="dropdown-item" href="#" onclick="Commontree_edit_RL(this)">EDIT</a></li>'
									)
								elif Tree_Enable is not None and str(Tree_Enable.ENABLE_TREE).upper() == "TRUE":
									if ObjectName =='SAQICT':										
										if str(ik.PRIMARY).upper() != "TRUE":											
											Action_str += ('<li><a class="dropdown-item" href="#" onclick="mark_primary_contact(this)">MARK PRIMARY</a></li>')
										#Action_str += ('<li><a class="dropdown-item" href="#" onclick="cont_openaddnew(this,'')" id ="ADDNEW__SYOBJR_98871_SYOBJ_002649">MARK PRIMARY</a></li>')
									elif str(ObjectName) =='SAQSPT':
										pass
									else:
										Action_str += ('<li><a class="dropdown-item" href="#" onclick="Commontree_edit_RL(this)">EDIT</a></li>')
								elif str(current_tab).upper() == "PROFILE":
									Action_str += (
										'<li><a class="dropdown-item" href="#" onclick="Commontree_edit_RL(this)">EDIT</a></li>'
									)
								elif str(current_tab).upper() == "SYPROF":
									Action_str += '<li><a class="dropdown-item" href="#" data-toggle="modal" data-target="#viewProfileRelatedList" onclick="profileObjSetEdit(this)">EDIT</a></li>'
								else:
									Action_str += '<li><a class="dropdown-item" href="#" onclick="cont_openedit(this)" data-target="#cont_viewModalSection" data-toggle="modal">EDIT</a></li>'
					if str(Action_permission.get("Delete")).upper() == "TRUE":
						#Trace.Write("ooooooooo"+str(ik.PARTY_ROLE))
						if related_list_delete_permission:
							onclick = "CommonDelete(this, '" + str(ObjectName) + "', 'WARNING')"
							if str(ObjectName) == "SYOBJC":
								Action_str += (
									'<li><a class="dropdown-item" href="#" id="deletebtn" onclick="'
									+ str(onclick)
									+ '" data-target="#cont_CommonModalDelete" data-toggle="modal">DROP</a></li>'
								)
							##A055S000P01-10136
							elif str(ObjectName)=="SAQTIP":
								if ik.PARTY_ROLE == "SHIP TO":
									quote_contract_recordId = Quote.GetGlobal("contract_quote_record_id")
									quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
									get_role_name = Sql.GetFirst("Select count(CpqTableEntryId) as COUNT FROM SAQTIP where QUOTE_RECORD_ID = '"+str(quote_contract_recordId)+"' and QTEREV_RECORD_ID ='"+str(quote_revision_record_id)+"' and PARTY_ROLE = 'SHIP TO' ")
									if get_role_name.COUNT >1:										
										Action_str += ('<li><a class="dropdown-item" href="#" id="deletebtn" onclick="'+ str(onclick)+ '" data-target="#cont_CommonModalDelete" data-toggle="modal">DELETE ACCOUNT</a></li>')
									else:										
										Action_str += ('<li style="display: none;"><a class="dropdown-item" href="#" id="deletebtn" onclick="'+ str(onclick)+ '" data-target="#cont_CommonModalDelete" data-toggle="modal">DELETE ACCOUNT</a></li>')
							##A055S000P01-10136
							elif str(ObjectName)=="SAQICT":								
								Action_str += (
									'<li><a class="dropdown-item" href="#" id="deletebtn" onclick="'
									+ str(onclick)
									+ '" data-target="#cont_CommonModalDelete" data-toggle="modal">DELETE</a></li>'
								)  
								
							else:
								Action_str += (
									'<li><a class="dropdown-item" href="#" id="deletebtn" onclick="'
									+ str(onclick)
									+ '" data-target="#cont_CommonModalDelete" data-toggle="modal">DELETE</a></li>'
								)
					Action_str += "</ul></div></div>"
					
					list_lineup1.append(("ACTIONS", Action_str))
					OBJ_CpqTableEntryId = ""
					try:
						if str(ik.CpqTableEntryId) is not None and str(ik.CpqTableEntryId) != "":
							OBJ_CpqTableEntryId = str(ik.CpqTableEntryId)
							
					except:
						pass
					getdate_indication = ''
					for inm in ik:
						a = str(inm).split(",")
						value123 = a[0].replace("[", "").lstrip()
						valu = ",".join(a[1:])
						value1234 = valu.replace("]", "").lstrip()
						if value1234 == "ACQUIRED" or value1234 == "PRICED":
							value1234 = value1234.replace(value1234,"<img title='"+str(value1234).title()+"' src=/mt/APPLIEDMATERIALS_SIT/Additionalfiles/Green_Tick.svg> "+str(value1234))
						if value1234 == "APPROVAL REQUIRED":
							value1234 = value1234.replace("APPROVAL REQUIRED","<img title='Approval Required' src=/mt/APPLIEDMATERIALS_SIT/Additionalfiles/clock_exe.svg> APPROVAL REQUIRED")
						if value1234 == "ACQUIRING":                        
							value1234 = value1234.replace("ACQUIRING","<img title='Acquiring' src=/mt/APPLIEDMATERIALS_SIT/Additionalfiles/Cloud_Icon.svg> ACQUIRING")
						if value1234 == "ERROR":
							value1234 = value1234.replace("ERROR","<img title='Error' src=/mt/APPLIEDMATERIALS_SIT/Additionalfiles/exclamation_icon.svg> ERROR")
						if value1234 == "ASSEMBLY IS MISSING":
							value1234 = value1234.replace("ASSEMBLY IS MISSING","<img title='Assembly Missing' src=/mt/APPLIEDMATERIALS_SIT/Additionalfiles/Orange1_Circle.svg> ASSEMBLY IS MISSING")
						if value1234 == "PARTIALLY PRICED":
							value1234 = value1234.replace("PARTIALLY PRICED","<img title='Partially Priced' src=/mt/APPLIEDMATERIALS_SIT/Additionalfiles/Red1_Circle.svg> PARTIALLY PRICED")
						if value1234 != "ACQUIRED" and value1234 != "APPROVAL REQUIRED" and value1234 != "ERROR" and value1234 != "ASSEMBLY IS MISSING" and value1234 != "PARTIALLY PRICED" and value1234 != "ACQUIRING" and value1234 != "PRICED":                        
							value1234 = value1234
						if value123 == objRecName:
							current_rec_id = value1234
						if value123 == objRecName:
							current_rec_id = value1234
						curr_symbol = ""
						cur_api_name = Sql.GetFirst(
							"select API_NAME,DATA_TYPE,FORMULA_DATA_TYPE from  SYOBJD (nolock) where API_NAME = '"
							+ str(value123)
							+ "' and OBJECT_NAME = '"
							+ str(ObjectName)
							+ "' "
						)
						
						data_type_val = ""
						formu_data_type_val = ""
						if cur_api_name is not None:
							data_type_val = cur_api_name.DATA_TYPE
							formu_data_type_val = cur_api_name.FORMULA_DATA_TYPE
						
						if str(cur_api_name) is not None and (
							str(data_type_val) == "CURRENCY" or str(formu_data_type_val) == "CURRENCY"
						):
							
							cur_api_name_obj = Sql.GetFirst(
								"select CURRENCY_INDEX from  SYOBJD (nolock) where API_NAME = '"
								+ str(value123)
								+ "' and OBJECT_NAME = '"
								+ str(ObjectName)
								+ "' "
							)
							curr_symbol_obj = ""
							try:
								if cur_api_name_obj.CURRENCY_INDEX != "":
									if str(ObjectName) == "SAQIBP":
										contract_quote_record_id = Product.GetGlobal("contract_quote_record_id")
										curr_symbol_obj = Sql.GetFirst(
											"select SYMBOL,CURRENCY,DISPLAY_DECIMAL_PLACES from PRCURR (nolock) where CURRENCY_RECORD_ID = (select "
											+ str(cur_api_name_obj.CURRENCY_INDEX)
											+ " from SAQTMT"
											+ " where MASTER_TABLE_QUOTE_RECORD_ID  "
											+ " = '"
											+ str(contract_quote_record_id)
											+ "' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"') "
										)
									else:
										if str(cur_api_name_obj.CURRENCY_INDEX) =="GLOBAL_CURRENCY":
											Globalcurrency=Sql.GetFirst("SELECT CURRENCY_RECORD_ID FROM PRCURR(NOLOCK) WHERE CURRENCY = 'USD' ")
											curr_symbol_obj = Sql.GetFirst(
												"select SYMBOL,CURRENCY,DISPLAY_DECIMAL_PLACES from PRCURR (nolock) where CURRENCY_RECORD_ID = '"+str(Globalcurrency.CURRENCY_RECORD_ID)+"'"
											)
										
										else:
											curr_symbol_obj = Sql.GetFirst(
												"select SYMBOL,CURRENCY,DISPLAY_DECIMAL_PLACES from PRCURR (nolock) where CURRENCY_RECORD_ID = (select "
												+ str(cur_api_name_obj.CURRENCY_INDEX)
												+ " from "
												+ str(ObjectName)
												+ " where  "
												+ str(objRecName)
												+ " = '"
												+ str(current_rec_id)
												+ "' ) "
											)
											
								cur_api_name_obj = ""
							except:
								curr_symbol_obj = ""
							curr_symbol = ""
							decimal_place = 3
							if curr_symbol_obj is not None and len(curr_symbol_obj) > 0 and curr_symbol_obj != "":
								
								curr_symbol = curr_symbol_obj.CURRENCY
								decimal_place = curr_symbol_obj.DISPLAY_DECIMAL_PLACES
								
							if value1234 is not None:
								if value1234 != "":
									if "-" in value1234:										
										##A055S000P01-12021
										if (str(value123) in ("NET_PRICE_INGL_CURR","NET_PRICE")) :
											my_format = "{:,." + str(decimal_place) + "f}"
											value1234 = str(my_format.format(round(float(value1234), int(decimal_place))))
											value1234 = value1234 + " " + curr_symbol
										##A055S000P01-12021
										else:
											ccc = value1234.split("-")
											value1234 = value1234[0] + "" + ccc[1] + curr_symbol
									else:
										my_format = "{:,." + str(decimal_place) + "f}"
										value1234 = str(my_format.format(round(float(value1234), int(decimal_place))))
										if str(value123) == "ANNUAL_BILLING_AMOUNT" and str(ObjectName) == "SAQIBP":
											value1234 = value1234
										else:											
											value1234 = value1234 + " " + curr_symbol
						if str(cur_api_name) is not None and (
							str(data_type_val) == "PERCENT" or str(formu_data_type_val) == "PERCENT"
						):
							decimal_place = 2
							percentSymbol = "%"
							
							if value1234 is not None and value1234 != '':
								my_format = "{:." + str(decimal_place) + "f}"
								value1234 = str(my_format.format(round(float(value1234), int(decimal_place)))) + " %"

						if value123 in lookup_disply_list:
							for key, value in lookup_list.items():
								if value == value123:
									if value123 == "ATTRIBUTE_UOM":
										key = ""
									lookup_obj = Sql.GetFirst(
										"SELECT LOOKUP_OBJECT FROM  SYOBJD (nolock) WHERE OBJECT_NAME = '"
										+ str(ObjectName)
										+ "' AND LOOKUP_API_NAME ='"
										+ str(key)
										+ "' AND DATA_TYPE = 'LOOKUP'"
									)                                    
									lookup_val = str(lookup_obj.LOOKUP_OBJECT)
									tab_obj = Sql.GetFirst(
										"SELECT TOP 10 PG.TAB_NAME,PG.TAB_RECORD_ID FROM SYSECT (nolock) SE INNER JOIN SYPAGE (nolock) PG on SE.PAGE_RECORD_ID = PG.RECORD_ID WHERE SE.PRIMARY_OBJECT_NAME='"
										+ str(lookup_val)
										+ "' and SE.SECTION_NAME ='BASIC INFORMATION' ORDER BY SE.CpqTableEntryId asc"
									)
									if tab_obj is not None:
										tab_val = str(tab_obj.TAB_NAME).strip()
										if tab_val in list_of_tabs:
											ids[key] = value1234 + "|" + tab_val
											lookup_link_popup.append(key)
										else:
											product_name = Sql.GetFirst(
												"select APP_LABEL from SYTABS (nolock) where RECORD_ID='"
												+ str(tab_obj.TAB_RECORD_ID)
												+ "'"
											)
											if product_name is not None:
												module_txt = str(product_name.APP_LABEL).strip()
												product_id = Sql.GetFirst(
													"select PRODUCT_ID from products (nolock) where PRODUCT_NAME='"
													+ str(module_txt)
													+ "'"
												)											
											if product_id != "" and product_id is not None:
												if key:
													pop_val[key] = value1234 + "|" + tab_val + "," + str(product_id.PRODUCT_ID)
											else:
												lookup_obj = Sql.GetFirst(
													"SELECT LOOKUP_OBJECT FROM  SYOBJD (nolock) WHERE OBJECT_NAME = '"
													+ str(ObjectName)
													+ "' AND LOOKUP_API_NAME ='"
													+ str(key)
													+ "' AND DATA_TYPE = 'LOOKUP'"
												)												
												lookup_val = str(lookup_obj.LOOKUP_OBJECT)
												if key:
													pop_val[key] = value1234 + "|" + lookup_val
											lookup_rl_popup.append(key)
									else:
										lookup_obj = Sql.GetFirst(
											"SELECT LOOKUP_OBJECT FROM  SYOBJD (nolock) WHERE OBJECT_NAME = '"
											+ str(ObjectName)
											+ "' AND LOOKUP_API_NAME ='"
											+ str(key)
											+ "' AND DATA_TYPE = 'LOOKUP'"
										)										
										lookup_val = str(lookup_obj.LOOKUP_OBJECT)
										if key:
											pop_val[key] = value1234 + "|" + lookup_val
										lookup_rl_popup.append(key)
						elif value123 == objRecName:
							key_value = str(value1234)
							if str(ObjectName) == "USERS":
								value1234 = str(ObjectName) + "-" + str(key_value).rjust(6, "0")
							elif str(ObjectName) == 'SAQDOC' and key_value == 'Pending':
								value1234 = 'Pending'
							else:
								value1234 = str(ObjectName) + "-" + str(OBJ_CpqTableEntryId).rjust(6, "0")
							tab_obj1 = Sql.GetFirst(
								"SELECT PG.TAB_NAME,PG.TAB_RECORD_ID FROM SYSECT (nolock) SE INNER JOIN SYPAGE (nolock) PG on SE.PAGE_RECORD_ID = PG.RECORD_ID WHERE SE.PRIMARY_OBJECT_NAME='"
								+ str(ObjectName)
								+ "' and SE.SECTION_NAME ='BASIC INFORMATION'"
							)
						else:							
							imgValue = ''
							if str(ObjectName) == "SAQRIT":
								if value1234 != "":
									imgValue = str(value1234).split(">")[0]
									imgValue = str(imgValue)+">"
								else:
									imgValue = ""
							elif str(ObjectName) == "SAQDOC":
								if value1234 != "":
									imgValue = str(value1234).split(">")[0]
									imgValue = str(imgValue)+">"
								else:
									imgValue = ""
							elif value1234.startswith("<img"):
								# value1234 = value1234.replace('"', "&quot;")
								value1234 = value1234.replace("<p>", " ")
								value1234 = value1234.replace("</p>", " ")
								imgValue = value1234
								value1234 = value1234.split('"')
								try:
									value1234 = value1234[1]
								except:
									value1234 = value1234								
							else:
								value1234 = value1234.replace('"', "&quot;")
								value1234 = value1234.replace("<p>", " ")
								value1234 = value1234.replace("</p>", " ")
							
							#value1234 = value1234.split("&quot;")
							#value1234 = value1234[1]
							
							img_list = ['PO_NOTES','PRICING_STATUS','STATUS','EQUIPMENT_STATUS']
							if str(ObjectName) == "SAQIFP":
								img_list.append('PRICING_STATUS')
							if str(ObjectName) == "SAQDOC":
								img_list.append('STATUS')
							if value123 in img_list:
								new_dict[value123] = ('<abbr id ="' + key_value + '" title="' + value1234 + '">' + imgValue + "</abbr>")
							else:
								if not re.match(r'[A-Za-z0-9]',str(value1234)):
									Trace.Write("encode character")
									Trace.Write("key_value ---"+str(key_value))
									# Trace.Write(value1234.encode('utf-8'))
									# Trace.Write(value1234.decode('utf-8'))
									#Trace.Write(value1234.encode('utf-8').decode('utf-8'))
									value1234 = str(value1234).encode('utf-8').decode('utf-8')
									new_dict[str(value123)] = ('<abbr id ="' + key_value + '" title="' + value1234 + '">' + value1234 + "</abbr>")
								else:
									new_dict[value123] = ('<abbr id ="' + str(key_value) + '" title="' + str(value1234) + '">' + str(value1234) + "</abbr>")  
								#new_dict[value123] = value1234                           
						## addon product hyperlink starts
						if str(RECORD_ID) == "SYOBJR-98859" and value123 == 'SERVICE_ID':
							contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
							get_key_value = Sql.GetFirst("SELECT {} AS VAL from {} (nolock) where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID='{}' and SERVICE_ID = '{}' AND GREENBOOK = '{}' and PAR_SERVICE_ID = '{}'".format(str(objRecName),str(ObjectName),contract_quote_record_id,quote_revision_record_id,str(value1234),str(TreeParentParam), str(TreeSuperParentParam)))
							key_value = get_key_value.VAL
						## addon product hyperlink ends
						if value123 in edit_field:
							value1234 = value1234.replace('"', "&quot;")
							value1234 = value1234.replace("<p>", " ")
							value1234 = value1234.replace("</p>", " ")
							
							new_dict[value123] = (
								'<abbr id ="' + value1234 + '" title="' + value1234 + '">' + value1234 + "</abbr>"
							)   
						else:
							if value123 in checkbox_list:
								new_dict[value123] = value1234
							else:
								if (value123 == "SET_NAME" or value123 == "SETMAT_NAME") and (
									RECORD_ID == "SYOBJR-90016" or RECORD_ID == "SYOBJR-30101"
								):
									new_dict[value123] = (
										"<a id='"
										+ str(primary_view)
										+ "' onclick='Move_to_parent_obj(this)'>"
										+ value1234
										+ "</a>"
									)
								else:
									if not re.match(r'[A-Za-z0-9]',value1234):
										value1234 = value1234.replace('"', "&quot;")
										value1234 = value1234.replace("<p>", " ")
										value1234 = value1234.replace("</p>", " ")
									else:
										value1234 = str(value1234).replace('"', "&quot;")
										value1234 = str(value1234).replace("<p>", " ")
										value1234 = str(value1234).replace("</p>", " ")
									#Trace.Write(str(value123)+'3107--3051---'+str(value1234))
									if value123 in [
										"ERROR",
										"MINIMUM_PRICE",
										"CATCLC_PRICE_INSORG_CURR",
										"INVCLC_UNITPRICE_INSORG_CURR",
									]:
										new_dict[value123] = value1234
										seg_pric[value123] = value1234.replace(curr_symbol, "").replace(" ", "")
										seg_pric["PRICE_FACTOR"] = PriceFactor
									else:										
										#Trace.Write(str(value1234)+'---3067---'+str(value123))
										if str(RECORD_ID) == "SYOBJR-00009" and str(value123) == 'NET_PRICE':							
											new_dict[value123] = (
												'<input id ="' + key_value + '" value="' + value1234 + '" style="border: 0px solid;" disabled> </input>'
											)										
										#the Billing Matrix based on the Warranty Date  start
										if str(value123) == "WARRANTY_END_DATE" and RECORD_ID != "SYOBJR-00009":
											#Trace.Write('getindication--3075---'+str(getindication))
											getdate_indication = str(value1234)
											if getdate_indication:
												getdate_indication = datetime.strptime(str(getdate_indication), '%m/%d/%Y')												
										elif str(value123) in billing_date_column:											
											getdate_indication_billing = datetime.strptime(str(value123), '%m-%d-%Y')											
											contract_quote_record_id = Product.GetGlobal("contract_quote_record_id")
											curr_symbol_obj = Sql.GetFirst(
												"select SYMBOL,CURRENCY,DISPLAY_DECIMAL_PLACES from PRCURR (nolock) where CURRENCY_RECORD_ID = (select QUOTE_CURRENCY_RECORD_ID"
												+ " from SAQTMT"
												+ " where MASTER_TABLE_QUOTE_RECORD_ID  "
												+ " = '"
												+ str(contract_quote_record_id)
												+ "' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' ) "
											)											
											if curr_symbol_obj:
												curr_symbol = curr_symbol_obj.CURRENCY												
												try:
													decimal_place = curr_symbol_obj.DISPLAY_DECIMAL_PLACES								
													my_format = "{:,." + str(decimal_place) + "f}"
													value1234 = str(my_format.format(round(float(value1234), int(decimal_place))))
												except:
													value1234											
											if getdate_indication:												
												if getdate_indication > getdate_indication_billing:
													new_dict[value123] = (
														'<input  type= "text" id ="' + key_value + '" class= "billclassedit billclassedit_bg"  value="' + value1234 + '" style="border: 0px solid;"  disabled>'
													)
												else:													
													if str(value1234) == "0.00":
														
														new_dict[value123] = (
															'<input  type= "text" id ="billeditval_disable"   value="' + value1234 + '" style="border: 0px solid;"  disabled>'
														)
													else:
														new_dict[value123] = (
															'<input  type= "text" id ="' + key_value + '" class= "billclassedit"  value="' + value1234 + '" style="border: 0px solid;"  disabled>'
														)
											else:												
												new_dict[value123] = (
													'<input  type= "text" id ="' + key_value + '" class= "billclassedit"  value="' + value1234 + '" style="border: 0px solid;"  disabled>'
												)
											#the Billing Matrix based on the Warranty Date  start
										elif str(value123) in delivery_date_column:
											new_dict[value123] = (
												'<input  type= "text" id ="' + key_value + '" class= "deliveryclassedit"  value="' + value1234 + '" style="border: 0px solid;"  disabled>'
											)
										else:                                            
											if str(value123) != "CUSTOMER_ANNUAL_QUANTITY":
												precentage_columns = ['SALES_DISCOUNT','BD_DISCOUNT','TARGET_PRICE_MARGIN','BD_PRICE_MARGIN','YEAR_OVER_YEAR']
												if value123 in precentage_columns:
													# perc = Sql.GetList("SELECT DISCOUNT FROM SAQICO WHERE "+str(value123)+" = '"+str(value1234)+"'")
													string_val = str(value1234)
													#string_val = string_val.replace('0','')
													string_val1 = string_val.split('.')
													str_val = string_val1[0]
													value1234 = str_val
													#Trace.Write(str(value123)+'3107-----'+str(value1234))
													if value1234 is not None and value1234 != '':
														new_dict[value123] = (
															'<abbr id ="' + key_value + '" title="' + str(value1234).upper() +'">' + str(value1234).upper() +  ' %' +  "</abbr>"
														)														
													else:
														new_dict[value123] = (
														'<abbr id ="' + key_value + '" title="' + str(value1234).upper() + '">' + str(value1234).upper() + "</abbr>"
													)	
												else:													
													img_list = ['PO_NOTES','PRICING_STATUS','STATUS','EQUIPMENT_STATUS']
													if str(ObjectName) == "SAQIFP":
														img_list.append('PRICING_STATUS')
													if str(ObjectName) == "SAQDOC":
														img_list.append('STATUS')
													if value123 in img_list:
														
														new_dict[value123] = ('<abbr id ="' + key_value + '" title="' + value1234 + '">' + imgValue + "</abbr>")
													elif value123 in ["REV_EXPIRE_DATE","REV_CREATE_DATE"]:								
														value1234 = str(value1234).upper().split(" ")[0].strip()
														value1234 = new_dict[value123] = ('<abbr title="' + str(value1234).upper() + '">' +str(value1234).upper() + "</abbr>")
													# for redirecting the left tree node while viewing record from listgrid - start    
													elif ObjectName in value1234: 
														new_dict[value123] = ('<abbr id ="' + key_value + '" title="' + str(value1234).upper() + '">' + str(value1234).upper() + "</abbr>") 							
													# for redirecting the left tree node while viewing record from listgrid - end       
													elif ObjectName == "SAQSAO" or ObjectName == "SAQSGB":
														new_dict[value123] = ('<abbr id ="' + key_value + '" title="' + str(value1234).upper() + '">' + value1234 + "</abbr>") 
													else:														
														try:
															if RECORD_ID == 'SYOBJR-00009' and value123 == 'DISCOUNT':
																new_dict[value123] = ('<abbr id ="discount_' + key_value + '"  title="' + str(value1234).upper() + '">' +str(value1234).upper() + "</abbr>")
															elif RECORD_ID == 'SYOBJR-98872' and value123 == 'LINE':
																new_dict[value123] = ('<abbr id ="' + key_value + '"  title="' + str(value1234).upper() + '">' +str(value1234).upper() + "</abbr>")
															elif RECORD_ID == 'SYOBJR-98873' and value123 == 'SERVICE_ID':
																new_dict[value123] = ('<abbr id ="' + key_value + '"  title="' + str(value1234).upper() + '">' +str(value1234).upper() + "</abbr>")
															else:
																new_dict[value123] = ('<abbr  title="' + str(value1234).upper() + '">' +str(value1234).upper() + "</abbr>")
														except:
															new_dict[value123] = ('<abbr title="{value}">{value}</abbr>'.format(value= value1234))
														#new_dict[value123] = value1234
												
						new_dict["ACTIONS"] = Action_str   
						new_dict["ids"] = ids
						new_dict["seg_pric"] = seg_pric
						new_dict["pop_val"] = pop_val
						new_dict["primary"] = primary
						list_lineup.append(value123)
					table_list.append(new_dict)
				table_header += "<tr id='getbannername' >"
			#A055S000P01-682 start to hide the Actions column for related list
			rowspan = ''
			#A055S000P01-4401
			if RECORD_ID == 'SYOBJR-00009':
				# if pricing_picklist_value == 'Pricing' and str(TreeParam) == "Quote Items":
				# 	rowspan = 'rowspan="3"' 
				# else:
				rowspan = 'rowspan="2"' 
				
				#table_header += '<th colspan="23" data-align="right"><div><label class="onlytext"><div>QUOTE ITEMS</div></label></div></th>'
			# if RECORD_ID == 'SYOBJR-34575':
			# 	# if pricing_picklist_value == 'Pricing' and str(TreeParam) == "Quote Items":
			# 	# 	rowspan = 'rowspan="3"' 
			# 	# else:
			# 	rowspan = 'rowspan="3"'
			if TreeParam == "Quote Preview" or TreeParam == "Contract Preview":
				table_header += ''            
			else:
				# A055S000P01-682 end to hide the Actions column for related list                 
				table_header += (
					'<th data-field="ACTIONS" '
					+ rowspan
					+'><div class="action_col">ACTIONS</div><button class="searched_button" id="Act_'
					+ str(table_id)
					+ '">Search</button></th>'
				)
				#A055S000P01-682 start to hide the Select column for related list    
			if TreeParam == "Quote Preview" or TreeParam == "Contract Preview":
				table_header += ''
			else:
				#A055S000P01-682 end to hide the Select column for related list                
				table_header += '<th data-field="SELECT"  class="wth45" data-checkbox="true" '+rowspan+'> <div class="pad0brdbt">SELECT</div></th>'
				Trace.Write("table_header=="+str(table_header))
			# if RECORD_ID == 'SYOBJR-00006':
			#     table_header += (
			#         '<th data-field="emp"  data-filter-control="input" data-title-tooltip="emp" data-formatter="" data-sortable="true"></th>'
			#     )
			# if TreeParam == "Items":
			#     table_header += (
			#         '<th data-field="ACTIONS"><div class="action_col">STATUS</div><button class="searched_button" id="STAT_'
			#         + str(table_id)
			#         + '"></button></th>'
			#     )
				# table_header += '<th data-field="STATUS"  class="wth45" ></th>'
				# table_header += (
				#     '<th data-field="emp"  data-filter-control="input" data-title-tooltip="emp" data-formatter="" data-sortable="true"></th>'
				# )

			filter_control_function = ""
			values_list = ""
			dict_form = {}			
			cv_list = []
			ignorecol = ['BILLING_DATE', 'BILLING_AMOUNT', 'BILLING_VALUE','DELIVERY_SCHED_DATE']
			Trace.Write("Columns_chk_J"+str(Columns))
			Trace.Write("billing_date_column--"+str(billing_date_column))
			Trace.Write("delivery_date_column--"+str(delivery_date_column))
			for invs in list(eval(Columns)):
				table_ids = "#" + str(table_id)
				if invs in billing_date_column: # Billing Matrix - Pivot - Start
					filter_clas = ("#" + str(table_id) + " .bootstrap-table-filter-control-" + str(invs).replace('-','_'))
					Trace.Write('filter_clas--billing--'+str(filter_clas))
					values_list += "var x_" + str(invs).replace('-','_') + ' = $("' + str(filter_clas) + '").val(); '
					values_list += "ATTRIBUTE_VALUEList.push(x_" + str(invs).replace('/','_').replace('-','_') + "); "
				elif  invs in delivery_date_column: # Billing Matrix - Pivot - Start
					filter_clas = ("#" + str(table_id) + " .bootstrap-table-filter-control-" + str(invs).replace('-','_'))
					Trace.Write('filter_clas--delivery--'+str(filter_clas))
					values_list += "var x_" + str(invs).replace('-','_') + ' = $("' + str(filter_clas) + '").val(); '
					values_list += "ATTRIBUTE_VALUEList.push(x_" + str(invs).replace('/','_').replace('-','_') + "); "              
				else:# Billing Matrix - Pivot - End
					if invs not in ignorecol:
						filter_clas = ("#" + str(table_id) + " .bootstrap-table-filter-control-" + str(invs))
						values_list += "var " + str(invs) + ' = $("' + str(filter_clas) + '").val(); '
						values_list += "ATTRIBUTE_VALUEList.push(" + str(invs) + "); "
						

			Currentcol = Sql.GetFirst(
				"select COLUMNS from  SYOBJR (NOLOCK) where SAPCPQ_ATTRIBUTE_NAME ='" + str(RECORD_ID) + "'"
			)
			CountCol = eval(Currentcol.COLUMNS)
			
			# Billing Matrix - Pivot - Start			
			Colcount = 0
			#Trace.Write('Colcount--ObjectName-----'+str(ObjectName))			
			if ObjectName == 'SAQIBP':
				Colcount += len(billing_date_column)
			#if ObjectName == 'SAQSPD':
				#Colcount += len(delivery_date_column)
			# Billing Matrix - Pivot - End
			Colcount = len(CountCol) + 2
			

			filter_class = "#Act_" + str(table_id)
			filter_control_function += (
				'$("'
				+ filter_class
				+ '").click( function(){ var table_id = $(this).closest("table").attr("id"); ATTRIBUTE_VALUEList = []; '
				+ str(values_list)
				+ " var attribute_value = $(this).val(); SortColumn = localStorage.getItem('"
				+ str(table_id)
				+ "_SortColumn'); if (SortColumn === null){ SortColumn = \"\"; } SortColumnOrder = localStorage.getItem('"
				+ str(table_id)
				+ '_SortColumnOrder\'); if (SortColumnOrder === null){ SortColumnOrder = ""; } PerPage = $("#'
				+ str(table_id)
				+ '_PageCountValue").val(); PageInform = "1___" + PerPage + "___" + PerPage; cpq.server.executeScript("SYLDRTLIST", {"REC_ID":table_id, "ATTRIBUTE_NAME": '
				+ str(list(eval(Columns)))
				+ ', "ATTRIBUTE_VALUE": ATTRIBUTE_VALUEList, "ACTION" : "PRODUCT_ONLOAD_FILTER",  "SortColumn":SortColumn, "SortColumnOrder": SortColumnOrder, "PerPage": PerPage, "PageInform": PageInform, "PR_CURR": PR_CURR, "TP": TP ,"SUBTAB":"'
				+ str(SubTab)
				+'"}, function(data) { debugger; console.log(data);$("'
				+ str(table_ids)
				+ '").bootstrapTable("load", data[0] );if (document.getElementById(\''
				+ str(table_id)
				+ "_totalItemCount')) { document.getElementById('"
				+ str(table_id)
				+ "_totalItemCount').innerHTML = data[1]; if ($('#"
				+ str(table_id)
				+ "_totalItemCount').text() == '0') { $('#"
				+ str(table_id)
				+ " > tbody').html('<tr class=\"noRecDisp\"><td colspan="
				+ str(Colcount)
				+ " class=\"txtltimp\">No Records to Display</td></tr>'); document.getElementById('"
				+ str(table_id)+"').deleteTFoot();} }if (document.getElementById('"
				+ str(table_id)
				+ "_NumberofItem')) { document.getElementById('"
				+ str(table_id)
				+ "_NumberofItem').innerHTML = data[2];; } if(document.getElementById('"
				+ str(table_id)
				+ "_page_count')) { document.getElementById('"
				+ str(table_id)
				+ "_page_count').innerHTML = '1'; } $(\"#"
				+ str(table_id)
				+ '_PageCountValue").val(10); }); });'
			)
			Trace.Write('filter_control_function----'+str(filter_control_function))
			filter_control_function +=("$('#SYOBJR_00009_E5504B40_36E7_4EA6_9774_EA686705A63F_RelatedMutipleCheckBoxDrop_0').on('checkChange', function (event){ setTimeout(function () { try{ var GetValInput = $('#dropdownlistContentSYOBJR_00009_E5504B40_36E7_4EA6_9774_EA686705A63F_RelatedMutipleCheckBoxDrop_0 span').text(); gevalSplit = GetValInput.split(','); if(gevalSplit[0].indexOf('>') != -1){ var RemoveImg = (GetValInput).split('>'); if(gevalSplit[1] != undefined) imgtext = RemoveImg[1]+','+gevalSplit[1]; else imgtext = RemoveImg[1]; } else if(gevalSplit[1].indexOf('>') != -1){ var RemoveImg = (GetValInput).split('>'); if(gevalSplit[0] != undefined) imgtext = gevalSplit[0]+','+RemoveImg[1]; else imgtext = RemoveImg[1]; } else{ imgtext = GetValInput; } $('#dropdownlistContentSYOBJR_00009_E5504B40_36E7_4EA6_9774_EA686705A63F_RelatedMutipleCheckBoxDrop_0 span').text(imgtext); } catch(err){ console.log('wrong---'); } }, 600); });")                                      
					
		
			# Item Covered Object Column Grouping - Start
			table_group_columns = ''
			table_group_columns_delivery = ''
			#table_group_columns1 = ''
			table_group_columns2 = ''
			table_group_columns_delivery2 =''
			#table_group_columns3 = ''
			#table_group_columns4 = ''
			#table_group_columns5 = ''
			#A055S000P01-4401 pricing view
			##cost grouping
			# ##price grouping
			# table_group_columns3 =''
			# ##Line summary grouping
			# table_group_columns4 =''
			# ##Entitlement category grouping
			# header1 = ''
			# header3 = ''
			# header2 = ''
			# if RECORD_ID == 'SYOBJR-00009' and pricing_picklist_value == 'Pricing' and str(TreeParam) == "Quote Items":
			# 	ent_cat_list = ['KPI','MISC TERMS']
			# 	if ent_cat_list:
			# 		header1 = '<th class = "ent_header1" colspan="{}" data-align="right"><div><button style="border:none;" class="glyphicon glyphicon-minus-sign header1" id="entitlement-header-category-toggle" onclick="entitlement_category_toggle(this)"></button>CATEGORY 4 ENTITLEMENTS</div></th>'.format(len(ent_cat_list)*3)
			# 		for i in ent_cat_list:
			# 			category_val = str(i).replace(' ','_')
			# 			header2 += (									
			# 						'<th id ='+category_val+' class = "ent_header2" data-field='+category_val+' colspan=3 data-align="right"><div><button data-field='+category_val+' style="border:none;" class="glyphicon glyphicon-minus-sign" id="entitlement-category-toggle" onclick="entitlement_category_toggle(this)"></button>'+str(i)+'</div></th>'
			# 						) 
			# 			#'<th colspan=3 data-toggle="bootstrap-table" data-field="'
			# 							# + str(i)
			# 							# + '" data-filter-control="input" data-align="right" data-title-tooltsip="'
			# 							# + str(i)
			# 							# + '" data-sortable="true">'
			# 							# + str(i)
			# 							# + "</th>" 
			# 			header3 += (
			# 						'<th class = "entitlement_category_header entitlement_category_{val}" data-toggle="bootstrap-table" data-field="ENTITLEMENT_NAME_{val}" data-filter-control="input" data-align="left" data-title-tooltsip="ENTITLEMENT_NAME_{val}" data-sortable="true">ENTITLEMENT NAME</th><th class = "entitlement_category_header entitlement_category_{val}" data-toggle="bootstrap-table" data-field="ENTITLEMENT_COST_{val}" data-filter-control="input" data-align="left" data-title-tooltsip="ENTITLEMENT_COST_{val}" data-sortable="true">COST IMPACT</th><th class = "entitlement_category_header entitlement_category_{val}" data-toggle="bootstrap-table" data-field="ENTITLEMENT_PRICE_{val}" data-filter-control="input" data-align="left" data-title-tooltsip="ENTITLEMENT_PRICE_{val}" data-sortable="true">PRICE IMPACT</th>'.format(val = category_val)
			# 						)    
			# Trace.Write("@Columns---"+str(Columns))
			
			for key, invs in enumerate(list(eval(Columns))):
				table_ids = "#" + str(table_id)
				invs = str(invs).strip()
				Trace.Write("keyval---"+str(key)+ "--"+str(invs))
				qstring = attr_list.get(str(invs)) or ""
				if qstring == "":
					qstring = invs.replace("_", " ")
			
				rowspan = ''
				#Trace.Write("@3394--"+str(qstring))
				#A055S000P01-4401
				if RECORD_ID == 'SYOBJR-00009':
					# if pricing_picklist_value == 'Pricing' and str(TreeParam) == "Quote Items":
					# 	rowspan = 'rowspan="3"'
					# else:
					rowspan = 'rowspan="2"'
					#table_header += '<th colspan="5" data-align="right"><div><label class="onlytext"><label class="onlytext"><div>QUOTE ITEMS</div></label></div></th>'
				# if RECORD_ID == 'SYOBJR-34575':
				# 	rowspan = 'rowspan="3"'
				if key == 0:
					if invs in primary_link_popup:
						
						if str(current_tab).upper() == "APP" and current_prod.upper() == "SYSTEM ADMIN":
							
							table_header += (
								'<th  data-field="'
								+ str(invs)
								+ '" data-filter-control="input" data-title-tooltip="'
								+ str(qstring)
								+ '" data-formatter="primaryListHyperLink" data-sortable="true" '
								+ rowspan
								+'>'
								+ str(qstring)
								+ "</th>"
							)         
						else:  							
							if str(TreeParam) != 'Quote Preview' and  str(TreeParam) != 'Billing Matrix' and RECORD_ID != "SYOBJR-00010":
								Trace.Write("CHKNG_J_04 "+str(qstring))
								table_header += (
									'<th  data-field="'
									+ str(invs)
									+ '" data-filter-control="input" data-title-tooltip="'
									+ str(qstring)
									+ '" data-formatter="commonrealtedhyperlink" data-sortable="true" '
									+ rowspan
									+'>'
									+ str(qstring)
									+ "</th>"
								)       
							elif RECORD_ID == "SYOBJR-00010":
								Trace.Write("CHKNG_EMPTY HYPERLINK")
								table_header += (
									'<th  data-field="'
									+ str(invs)
									+ '" data-filter-control="input" data-title-tooltip="'
									+ str(qstring)
									+ '" data-formatter="emptyHyperLink" data-sortable="true" '
									+ rowspan
									+'>'
									+ str(qstring)
									+ "</th>"
								)
							else:								
								table_header += (
									'<th  data-field="'
									+ str(invs)
									+ '" data-filter-control="input" data-title-tooltip="'
									+ str(qstring)
									+ '" data-sortable="true" '
									+ rowspan
									+'>'
									+ str(qstring)
									+ "</th>"
								)                         
					else:        						
						if str(qstring) == "Purchase Order Notes" or str(qstring) == "Equipment Status":
							table_header += (
								'<th class="wth60" data-field="'
								+ str(invs)
								+ '" data-filter-control="input" data-align="center" data-title-tooltip="'
								+ str("STATUS")
								+ '" data-sortable="false" '
								+ rowspan
								+'>'
								+ str("STATUS")
								+ "</th>"
							)
						elif RECORD_ID == 'SYOBJR-00010' and str(invs) == 'SERVICE_ID' and TreeParam != "Quote Preview":
							table_header += (
								'<th class="wth60" data-field="'
								+ str(invs)
								+ '" data-filter-control="input" data-align="center" data-title-tooltip="'
								+ str("STATUS")
								+ '" data-sortable="false" '
								+ rowspan
								+'>'
								+ str("STATUS")
								+ "</th>"
							)
						else:							
							if (str(TreeParam) != 'Quote Preview' and str(TreeParam) != 'Contract Preview' and  str(TreeParam) != 'Billing Matrix' and str(current_tab).upper() != "APP" and RECORD_ID != "SYOBJR-98872") and RECORD_ID != "SYOBJR-98875" and RECORD_ID !="SYOBJR-98873" and RECORD_ID!="SYOBJR-00005" and RECORD_ID != "SYOBJR-00010":
								Trace.Write("CHKNG_J_05 "+str(qstring))
								table_header += (
									'<th  data-field="'
									+ str(invs)
									+ '" data-filter-control="input" data-title-tooltip="'
									+ str(qstring)
									+ '" data-formatter="commonrealtedhyperlink" data-sortable="true" '
									+ rowspan
									+'>'
									+ str(qstring)
									+ "</th>"
								)
							elif RECORD_ID == "SYOBJR-00010":
								Trace.Write("CHKNG_EMPTY HYPERLINK")
								table_header += (
									'<th  data-field="'
									+ str(invs)
									+ '" data-filter-control="input" data-title-tooltip="'
									+ str(qstring)
									+ '" data-formatter="emptyHyperLink" data-sortable="true" '
									+ rowspan
									+'>'
									+ str(qstring)
									+ "</th>"
								)
							elif str(current_tab).upper() == "APP":
								if (str(TreeParam) == "Tabs" or str(TreeParam) == "Pages"):
									table_header += (
										'<th  data-field="'
										+ str(invs)
										+ '" data-filter-control="input" data-title-tooltip="'
										+ str(qstring)
										+ '" data-formatter="ParentListHyperLink" data-sortable="true" '
										+ rowspan
										+'>'
										+ str(qstring)
										+ "</th>"
									)    
								else:	
									Trace.Write("CHKNG_J_01 "+str(qstring))									
									table_header += (
										'<th  data-field="'
										+ str(invs)
										+ '" data-filter-control="input" data-title-tooltip="'
										+ str(qstring)
										+ '" data-formatter="commonrealtedhyperlink" data-sortable="true" '
										+ rowspan
										+'>'
										+ str(qstring)
										+ "</th>"
									)  
							# elif RECORD_ID == "SYOBJR-98872":
							# 	table_header += ""
							# elif RECORD_ID == "SYOBJR-98873":
							# 	table_header += ""	
							else:								
								table_header += (
									'<th  data-field="'
									+ str(invs)
									+ '" data-filter-control="input" data-title-tooltip="'
									+ str(qstring)
									+ '" data-sortable="true" '
									+ rowspan
									+'>'
									+ str(qstring)
									+ "</th>"
								)    
								
				# elif RECORD_ID == 'SYOBJR-00009' and invs in ('PRICE_BENCHMARK_TYPE','TOOL_CONFIGURATION','ANNUAL_BENCHMARK_BOOKING_PRICE','CONTRACT_ID','CONTRACT_VALID_FROM','CONTRACT_VALID_TO','BENCHMARKING_THRESHOLD'):
					
				# 	align = ''
				# 	#A055S000P01-4401
				# 	# if pricing_picklist_value == 'Pricing' and str(TreeParam) == "Quote Items":
				# 	# 	rowspan_level1 = 'rowspan="2"'
				# 	# else:
				# 	rowspan_level1 = ""
				# 	if not table_group_columns:
				# 		table_header += '<th colspan="7" '+rowspan_level1+'  data-align="center"><div><button style="border:none;" class="glyphicon glyphicon-minus-sign" id="price-benchmark-column-toggle" onclick="price_benchmark_column_toggle(this)"></button>PRICE BENCHMARKING</div></th>'
				# 	if str(invs) in right_align_list:
				# 		align = 'right'
				# 	elif str(invs) in center_align_list:
				# 		align = 'center'
				# 	table_group_columns += (
				# 				'<th data-toggle="bootstrap-table" data-field="'
				# 				+ str(invs)
				# 				+ '" data-filter-control="input" data-align="'
				# 				+ str(align)
				# 				+'" data-title-tooltsip="'
				# 				+ str(qstring)
				# 				+ '" data-sortable="true">'
				# 				+ str(qstring)
				# 				+ "</th>"
				# 			)           
				# 	continue
				# elif RECORD_ID == 'SYOBJR-00009' and invs in ('EQUIPMENT_ID','PM_ID','PM_LABOR_LEVEL','KIT_NAME','KIT_NUMBER','TOOL_CONFIGURATION'):
				# 	align = ''
				# 	rowspan_level1 = ""
				# 	if not table_group_columns:
				# 		table_header += '<th colspan="6" '+rowspan_level1+'  data-align="center"><div>OBJECT INFORMATION<button style="border:none;" class="glyphicon glyphicon-minus-sign" id="object_info_column_toggle" onclick="quote_items_column_toggle(this)"></button></div></th>'
				# 	if str(invs) in right_align_list:
				# 		align = 'right'
				# 	elif str(invs) in center_align_list:
				# 		align = 'center'
				# 	table_group_columns += (
				# 				'<th data-toggle="bootstrap-table" data-field="'
				# 				+ str(invs)
				# 				+ '" data-filter-control="input" data-align="'
				# 				+ str(align)
				# 				+'" data-title-tooltsip="'
				# 				+ str(qstring)
				# 				+ '" data-sortable="true">'
				# 				+ str(qstring)
				# 				+ "</th>"
				# 			)           
				# 	continue
				# elif RECORD_ID == 'SYOBJR-00009' and invs in ('SSCM_PM_FREQUENCY','ADJ_PM_FREQUENCY','PM_COUNT_YEAR','PER_EVENT_PMSA_COST','ANNUAL_PMSA_COST'):
				# 	align = ''
				# 	rowspan_level1 = ""
				# 	if not table_group_columns2:
				# 		table_header += '<th colspan="5" '+rowspan_level1+'  data-align="center"><div>EVENT INFORMATION<button style="border:none;" class="glyphicon glyphicon-minus-sign" id="event_info_column_toggle" onclick="quote_items_column_toggle(this)"></button></div></th>'
				# 	if str(invs) in right_align_list:
				# 		align = 'right'
				# 	elif str(invs) in center_align_list:
				# 		align = 'center'
				# 	table_group_columns2 += (
				# 				'<th data-toggle="bootstrap-table" data-field="'
				# 				+ str(invs)
				# 				+ '" data-filter-control="input" data-align="'
				# 				+ str(align)
				# 				+'" data-title-tooltsip="'
				# 				+ str(qstring)
				# 				+ '" data-sortable="true">'
				# 				+ str(qstring)
				# 				+ "</th>"
				# 			)           
				# 	continue
				# ##annulaized cost
				# elif RECORD_ID == 'SYOBJR-00009' and invs in ('LABOR_COST','GREATER_THAN_QTLY_PM_COST','LESS_THAN_QTLY_PM_COST','CM_PART_COST','PM_PART_COST','REPLACE_COST','REFURB_COST','CLEANING_COST','METROLOGY_COST','KPI_COST','SEEDSTOCK_COST','FAILURE_COST','LOGISTICS_COST','OUTSOURCE_COST','TOTAL_COST_WOSEEDSTOCK','TOTAL_COST_WSEEDSTOCK','ENTITLEMENT_COST_IMPACT','ADD_COST_IMPACT'):	
				# 	align = ''
				# 	rowspan_level1 = ""
				# 	if not table_group_columns3:
				# 		table_header += '<th colspan="18" '+rowspan_level1+'  data-align="center"><div>ANNUALIZED COSTS<button style="border:none;" class="glyphicon glyphicon-minus-sign" id="cost_info_column_toggle" onclick="quote_items_column_toggle(this)"></button></div></th>'
				# 	if str(invs) in right_align_list:
				# 		align = 'right'
				# 	elif str(invs) in center_align_list:
				# 		align = 'center'
				# 	if str(invs) == 'ADD_COST_IMPACT':
				# 		table_group_columns3 += (
				# 					'<th data-toggle="bootstrap-table" data-field="'
				# 					+ str(invs)
				# 					+ '" data-filter-control="input" data-align="'
				# 					+ str(align)
				# 					+'" data-title-tooltsip="'
				# 					+ str(qstring)
				# 					+ '" data-formatter="cost_impact_edit_link" data-sortable="true">'
				# 					+ str(qstring)
				# 					+ "</th>"
				# 				)
				# 	else:
				# 		table_group_columns3 += (
				# 				'<th data-toggle="bootstrap-table" data-field="'
				# 				+ str(invs)
				# 				+ '" data-filter-control="input" data-align="'
				# 				+ str(align)
				# 				+'" data-title-tooltsip="'
				# 				+ str(qstring)
				# 				+ '" data-sortable="true">'
				# 				+ str(qstring)
				# 				+ "</th>"
				# 			)		           
				# 	continue
				
				# ##annulaized price
				# elif RECORD_ID == 'SYOBJR-00009' and invs in ('ENTPRCIMP_INGL_CURR','ADD_PRICE_IMPACT','PER_EVENT_PMSA_PRICE','ANNUAL_PMSA_PRICE','CEILING_PRICE_MARGIN','TARGET_PRICE_MARGIN','BD_PRICE_MARGIN','DISCOUNT','SALES_PRICE_INGL_CURR'):
				# 	align = ''
				# 	rowspan_level1 = ""
				# 	if not table_group_columns4:
				# 		table_header += '<th colspan="9" '+rowspan_level1+'  data-align="center"><div>ANNUALIZED PRICES<button style="border:none;" class="glyphicon glyphicon-minus-sign" id="price_info_column_toggle" onclick="quote_items_column_toggle(this)"></button></div></th>'
				# 	if str(invs) in right_align_list:
				# 		align = 'right'
				# 	elif str(invs) in center_align_list:
				# 		align = 'center'
				# 	if str(invs) == 'ADD_PRICE_IMPACT':
				# 		table_group_columns4 += (
				# 					'<th data-toggle="bootstrap-table" data-field="'
				# 					+ str(invs)
				# 					+ '" data-filter-control="input" data-align="'
				# 					+ str(align)
				# 					+'" data-title-tooltsip="'
				# 					+ str(qstring)
				# 					+ '" data-formatter="price_impact_edit_link" data-sortable="true">'
				# 					+ str(qstring)
				# 					+ "</th>"
				# 				)
				# 	elif str(invs) == 'DISCOUNT':
				# 		table_group_columns4 += (
				# 					'<th data-toggle="bootstrap-table" data-field="'
				# 					+ str(invs)
				# 					+ '" data-filter-control="input" data-align="'
				# 					+ str(align)
				# 					+'" data-title-tooltsip="'
				# 					+ str(qstring)
				# 					+ '" data-formatter="discount_edit_link" data-sortable="true">'
				# 					+ str(qstring)
				# 					+ "</th>"
				# 				)   
				# 	else:
				# 		table_group_columns4 += (
				# 					'<th data-toggle="bootstrap-table" data-field="'
				# 					+ str(invs)
				# 					+ '" data-filter-control="input" data-align="'
				# 					+ str(align)
				# 					+'" data-title-tooltsip="'
				# 					+ str(qstring)
				# 					+ '" data-sortable="true">'
				# 					+ str(qstring)
				# 					+ "</th>"
				# 				)
				# 	continue
				
				# ##contractual cost and price
				# elif RECORD_ID == 'SYOBJR-00009' and invs in ('YEAR','YEAR_OVER_YEAR','CONTRACT_VALID_FROM','CONTRACT_VALID_TO','WARRANTY_START_DATE','WARRANTY_END_DATE','CNTCST_INGL_CURR','CNTPRI_INGL_CURR'):
				# 	align = ''
				# 	rowspan_level1 = ""
				# 	if not table_group_columns5:
				# 		table_header += '<th colspan="8" '+rowspan_level1+'  data-align="center"><div>CONTRACTUAL COSTS AND PRICES<button style="border:none;" class="glyphicon glyphicon-minus-sign" id="contractual_info_column_toggle" onclick="quote_items_column_toggle(this)"></button></div></th>'
				# 	if str(invs) in right_align_list:
				# 		align = 'right'
				# 	elif str(invs) in center_align_list:
				# 		align = 'center'
				# 	if str(invs) == 'YEAR_OVER_YEAR':
				# 		table_group_columns5 += (
				# 					'<th data-toggle="bootstrap-table" data-field="'
				# 					+ str(invs)
				# 					+ '" data-filter-control="input" data-align="'
				# 					+ str(align)
				# 					+'" data-title-tooltsip="'
				# 					+ str(qstring)
				# 					+ '" data-formatter="yoy_edit_link" data-sortable="true">'
				# 					+ str(qstring)
				# 					+ "</th>"
				# 				)
				# 	else:	
				# 		table_group_columns5 += (
				# 					'<th data-toggle="bootstrap-table" data-field="'
				# 					+ str(invs)
				# 					+ '" data-filter-control="input" data-align="'
				# 					+ str(align)
				# 					+'" data-title-tooltsip="'
				# 					+ str(qstring)
				# 					+ '" data-sortable="true">'
				# 					+ str(qstring)
				# 					+ "</th>"
				# 				)
				# 	continue
				
				#normal+Collapsaible+normal
				
				elif RECORD_ID == 'SYOBJR-00009' and invs in ('EQUIPMENT_ID','GOT_CODE','ASSEMBLY_ID','PM_ID','PM_LABOR_LEVEL','KIT_NAME','KIT_NUMBER','KPU','TOOL_CONFIGURATION','SSCM_PM_FREQUENCY','ADJ_PM_FREQUENCY','CEILING_PRICE_INGL_CURR'):
					align = ''
					rowspan_level1 = ""
					if not table_group_columns:
						table_header += '<th colspan="12" '+rowspan_level1+'  data-align="center"><div>CEILING PRICE<button style="border:none;" class="glyphicon glyphicon-minus-sign" id="celing_info_column_toggle" onclick="quote_items_column_toggle(this)"></button></div></th>'
					if str(invs) in right_align_list:
						align = 'right'
					elif str(invs) in center_align_list:
						align = 'center'
					table_group_columns += (
								'<th data-toggle="bootstrap-table" data-field="'
								+ str(invs)
								+ '" data-filter-control="input" data-align="'
								+ str(align)
								+'" data-title-tooltsip="'
								+ str(qstring)
								+ '" data-sortable="true">'
								+ str(qstring)
								+ "</th>"
							)           
					continue
						
					
				# elif RECORD_ID == 'SYOBJR-34575' and delivery_date_column_joined:
				# 	Trace.Write('3991-')
				# 	align = ''
				# 	rowspan_level1 = ""
				# 	if str(invs) in right_align_list:
				# 		align = 'right'
				# 	elif str(invs) in center_align_list:
				# 		align = 'center'
				# 	if not table_group_columns_delivery2:
				# 		#table_header += '<th colspan="12" '+rowspan_level1+'  data-align="center"><div>CEILING PRICE<button style="border:none;" class="glyphicon glyphicon-minus-sign" id="celing_info_column_toggle" onclick="quote_items_column_toggle(this)"></button></div></th>'
				# 		for invs in delivery_date_column_joined:
				# 			table_header += (
				# 						'<th data-toggle="bootstrap-table" data-field="'
				# 						+ str(invs)
				# 						+ '" data-filter-control="input" '+rowspan_level1+' data-align="'
				# 						+ str(align)
				# 						+'" data-title-tooltsip="'
				# 						+ str(invs)
				# 						+ '" data-sortable="true">'
				# 						+ str(invs)
				# 						+ "</th>"
				# 					)           
				# 	continue
				# elif RECORD_ID == 'SYOBJR-00009' and invs in ('TARGET_PRICE_INGL_CURR','SLSDIS_PRICE_INGL_CURR','BD_PRICE_INGL_CURR','DISCOUNT','SALES_PRICE_INGL_CURR','YEAR_OVER_YEAR'):
				# 	align = ''
				# 	rowspan_level1 = ""
				# 	if not table_group_columns1:
				# 		table_header += '<th colspan="6" '+rowspan_level1+'  data-align="center"><div>PRICE<button style="border:none;" class="glyphicon glyphicon-minus-sign" id="price_column_toggle" onclick="quote_items_column_toggle(this)"></button></div></th>'
				# 	if str(invs) in right_align_list:
				# 		align = 'right'
				# 	elif str(invs) in center_align_list:
				# 		align = 'center'
				# 	table_group_columns1 += (
				# 				'<th data-toggle="bootstrap-table" data-field="'
				# 				+ str(invs)
				# 				+ '" data-filter-control="input" data-align="'
				# 				+ str(align)
				# 				+'" data-title-tooltsip="'
				# 				+ str(qstring)
				# 				+ '" data-sortable="true">'
				# 				+ str(qstring)
				# 				+ "</th>"
				# 			)           
				# 	continue
				elif RECORD_ID == 'SYOBJR-00009' and invs in ('YEAR','CONTRACT_VALID_FROM','CONTRACT_VALID_TO','WARRANTY_START_DATE','WARRANTY_END_DATE','CNTCST_INGL_CURR','CNTPRI_INGL_CURR'):
					align = ''
					rowspan_level1 = ""
					if not table_group_columns2:
						table_header += '<th colspan="7" '+rowspan_level1+'  data-align="center"><div>CONTRACTUAL PRICES<button style="border:none;" class="glyphicon glyphicon-minus-sign" id="contractual_info_column_toggle" onclick="quote_items_column_toggle(this)"></button></div></th>'
					if str(invs) in right_align_list:
						align = 'right'
					elif str(invs) in center_align_list:
						align = 'center'
					table_group_columns2 += (
								'<th data-toggle="bootstrap-table" data-field="'
								+ str(invs)
								+ '" data-filter-control="input" data-align="'
								+ str(align)
								+'" data-title-tooltsip="'
								+ str(qstring)
								+ '" data-sortable="true">'
								+ str(qstring)
								+ "</th>"
							)           
					continue

				elif len(cell_api) > 0 and invs in cell_api:
					table_header += (
						'<th  data-field="'
						+ str(invs)
						+ '" data-filter-control="input" data-cell-style="SgpbenrowStyle" data-title-tooltip="'
						+ str(qstring)
						+ '" data-sortable="true" '
						+ rowspan
						+'>'
						+ str(qstring)
						+ "</th>"
					)					
				elif lookup_link_popup is not None and invs in lookup_link_popup and (str(invs) != "TAB_NAME" and str(ObjectName) != "SYPSAC"):                 
					table_header += (
						'<th  data-field="'
						+ str(invs)
						+ '" data-filter-control="input" data-title-tooltip="'
						+ str(qstring)
						+ '" data-formatter="ParentListHyperLink" data-sortable="true" '
						+ rowspan
						+'>'
						+ str(qstring)
						+ "</th>"
					)
					
				elif lookup_rl_popup is not None and invs in lookup_rl_popup:
					footer_text_formatter = ''

					if RECORD_ID == 'SYOBJR-00024' and invs == 'APRCHNSTP_ID':                        
						table_header += (
							'<th  data-field="'
							+ str(invs)
							+ '" data-filter-control="input" data-align="right" data-title-tooltip="'
							+ str(qstring)
							+ '" data-sortable="true" '                            
							+ rowspan
							+'>'
							+ str(qstring)
							+ "</th>"
						)
					if invs == "SERVICE_ID"and RECORD_ID == 'SYOBJR-98873' :	
						Trace.Write("CHKNG_J_06 "+str(qstring))					
						table_header += (
							'<th  data-field="'
							+ str(invs)
							+ '" data-filter-control="input" data-title-tooltip="'
							+ str(qstring)
							+ '" data-formatter="commonrealtedhyperlink" data-sortable="true" '
							+ rowspan
							+'>'
							+ str(qstring)
							+ "</th>"
						) 
					else:
						Trace.Write('invs-50--'+str(invs))   
						table_header += (
							'<th  data-field="'
							+ str(invs)
							+ '" data-filter-control="input" data-title-tooltip="'
							+ str(qstring)
							+ '" data-sortable="true" '
							+ str(footer_text_formatter)
							+ ' '
							+ rowspan
							+'>'
							+ str(qstring)
							+ "</th>"
						)                    
					
				elif checkbox_list is not None and invs in checkbox_list:				
					table_header += (
						'<th  data-field="'
						+ str(invs)
						+ '" data-filter-control="input" data-align="center" data-title-tooltip="'
						+ str(qstring)
						+ '" data-formatter="CheckboxFieldRelatedList" data-sortable="true" '
						+ rowspan
						+'>'
						+ str(qstring)
						+ "</th>"
					)
					
				elif edit_field is not None and invs in edit_field:       
					table_header += (
						'<th  data-field="'
						+ str(invs)
						+ '" data-filter-control="input" data-title-tooltip="'
						+ str(qstring)
						+ '" data-formatter="editIconIfValueChanged" data-sortable="true" '
						+ rowspan
						+'>'
						+ str(qstring)
						+ "</th>"
					)
										
				else:								
					dblclick_ele.append(invs)

					if str(invs) in right_align_list:
						visible = ""
						if RECORD_ID == 'SYOBJR-00007' and str(invs) == 'BILLING_AMOUNT':                            
							visible = 'data-visible="false"'  
						if RECORD_ID == 'SYOBJR-34575' and str(invs) == 'QTEREVSPT_RECORD_ID':
							visible = 'data-visible="false"'
						
						if (str(RECORD_ID) == "SYOBJR-00029" and str(invs)=="QUANTITY" and str(Product.GetGlobal("TreeParentLevel2"))=="Product Offerings") or (str(RECORD_ID)=="SYOBJR-00005" and str(invs) == "CUSTOMER_ANNUAL_QUANTITY" and str(TreeParentParam)=="Complementary Products") or (SubTab.upper() =='INCLUSIONS' and str(RECORD_ID) == "SYOBJR-00029" and str(invs)=="QUANTITY"  and str(Product.GetGlobal("TreeParentLevel1"))=="Product Offerings") and TreeParam in ('Z0092','Z0006','Z0009'):
							data_formatter = "partsListEditLink" if getRevision.REVISION_STATUS!='APPROVED' else ''
							table_header += (
								'<th  data-field="'
								+ str(invs)
								+ '" data-filter-control="input" data-align="right" data-title-tooltip="'
								+ str(qstring)
								+ '" data-formatter="'+str(data_formatter)+'" data-sortable="true" '
								+ rowspan
								+'>'
								+ str(qstring)
								+ "</th>"
								)
						elif invs != "EQUIPMENT_LINE_ID" and invs != "LINE":             
							table_header += (
								'<th  data-field="'
								+ str(invs)
								+ '" data-filter-control="input" data-align="right" data-title-tooltip="'
								+ str(qstring)
								+ '" data-sortable="true" '
								+ str(visible)
								+ ' '
								+ rowspan
								+ '>'
								+ str(qstring)
								+ "</th>"
							)  
						if invs == "LINE"and RECORD_ID != 'SYOBJR-98873' :
							Trace.Write("CHKNG_J_07 "+str(qstring))
							if RECORD_ID == "SYOBJR-98877":
								table_header += (
									'<th  data-field="'
									+ str(invs)
									+ '" data-filter-control="input" data-title-tooltip="'
									+ str(qstring)
									+ '" data-sortable="true" '
									+ rowspan
									+'>'
									+ str(qstring)
									+ "</th>"
								)    
							else:
								table_header += (
									'<th  data-field="'
									+ str(invs)
									+ '" data-filter-control="input" data-title-tooltip="'
									+ str(qstring)
									+ '" data-formatter="commonrealtedhyperlink" data-sortable="true" '
									+ rowspan
									+'>'
									+ str(qstring)
									+ "</th>"
								)   
		
						# if invs == "EQUIPMENT_LINE_ID":
						# 	Trace.Write("@3817"+str(qstring))
						# 	table_header += (
						# 			'<th  data-field="'
						# 			+ str(invs)
						# 			+ '" data-filter-control="input" data-title-tooltip="'
						# 			+ str("Equipment Line ID")
						# 			+ '" data-formatter="commonrealtedhyperlink" data-sortable="true" '
						# 			+ rowspan
						# 			+'>'
						# 			+ str("Equipment Line ID")
						# 			+ "</th>"
						# 		)                      
					elif str(invs) in center_align_list:
						if RECORD_ID == 'SYOBJR-00010' and str(invs) == 'SERVICE_ID' and TreeParam != "Quote Preview":
							table_header += (
								'<th class="wth60" data-field="'
								+ str(invs)
								+ '" data-filter-control="input" data-align="center" data-title-tooltip="'
								+ str("STATUS")
								+ '" data-sortable="false" '
								+ rowspan
								+'>'
								+ str("STATUS")
								+ "</th>"
							)
						else:                     
							visible = ""
							if RECORD_ID == 'SYOBJR-00007' and str(invs) == 'BILLING_DATE':
								visible = 'data-visible="false"'                   
							table_header += (
								'<th  data-field="'
								+ str(invs)
								+ '" data-filter-control="input" data-align="center" data-title-tooltip="'
								+ str(qstring)
								+ '" data-sortable="true" '
								+ str(visible)
								+ ' '
								+ rowspan
								+'>'
								+ str(qstring)
								+ "</th>"
							)
					else:                       
						if str(qstring) == "Key": 							
							if ObjectName == "CTCICO":
								table_header += (
									'<th  data-field="'
									+ str(invs)
									+ '" data-filter-control="input" data-title-tooltip="'
									+ str(qstring)
									+ '" data-formatter="" data-sortable="true" '
									+ rowspan
									+'>'
									+ str(qstring)
									+ "</th>"
								)
							elif ObjectName == "SAQDOC":
								table_header += (
									'<th  data-field="'
									+ str(invs)
									+ '" data-filter-control="input" data-title-tooltip="'
									+ str(qstring)
									+ '" data-formatter="" data-sortable="true" '
									+ rowspan
									+'>'
									+ str(qstring)
									+ "</th>"
								)
							elif RECORD_ID == "SYOBJR-00010":
								Trace.Write("CHKNG_EMPTY HYPERLINK")
								table_header += (
									'<th  data-field="'
									+ str(invs)
									+ '" data-filter-control="input" data-title-tooltip="'
									+ str(qstring)
									+ '" data-formatter="emptyHyperLink" data-sortable="true" '
									+ rowspan
									+'>'
									+ str(qstring)
									+ "</th>"
								)
							else:
								Trace.Write("CHKNG_J_02 "+str(qstring))
								table_header += (
									'<th  data-field="'
									+ str(invs)
									+ '" data-filter-control="input" data-title-tooltip="'
									+ str(qstring)
									+ '" data-formatter="commonrealtedhyperlink" data-sortable="true" '
									+ rowspan
									+'>'
									+ str(qstring)
									+ "</th>"
								)
						
						elif ObjectName == "SAQDOC" and str(qstring) == "Document Name":
							table_header += (
								'<th  data-field="'
								+ str(invs)
								+ '" data-filter-control="input" class="cust_billing_name" data-title-tooltip="'
								+ str(qstring)
								+ '" data-formatter="documentrealtedhyperlink" data-sortable="true" '
								+ rowspan
								+'>'
								+ str(qstring)
								+ "</th>"
							)
						elif RECORD_ID == 'SYOBJR-00007' and str(invs) in billing_date_column: # Billing Matrix Date Change Model and Footer - Start
							
							footer_formatter = ''
							#'data-footer-formatter="priceSumFormatter"'
							tooltip = qstring
							qstring = '<a onclick="openBillingMatrixDateChangeModal(\'{Value}\')" href="#">{Value}</a>'.format(Value=qstring.replace('-','/'))
							#data_field = invs.replace('/','-')
							Trace.Write('2780-------month-------'+ str(invs))
							table_header += (
								'<th  data-field="'
								+ str(invs)
								+ '" data-filter-control="input" class="text-right cust_billing_date" data-title-tooltip="'
								+ str(tooltip)
								+ '" data-sortable="true" '
								+ str(footer_formatter)
								+ ' '
								+ rowspan
								+'>'
								+ str(qstring)
								+ "</th>"
							) # Billing Matrix Date Change Model and Footer - Start
						elif RECORD_ID == 'SYOBJR-34575' and str(invs) in delivery_date_column: 
							
							footer_formatter = ''
							#rowspan = 'rowspan="1"'
							#'data-footer-formatter="priceSumFormatter"'
							tooltip = qstring
							
							qstring = '<a onclick="openBillingMatrixDateChangeModal(\'{Value}\')" href="#">{Value}</a>'.format(Value=qstring.replace('-','/'))
							#data_field = invs.replace('/','-')
							Trace.Write('2780-----rowspan----'+ str(rowspan))
							table_header += (
								'<th  data-field="'
								+ str(invs)
								+ '" data-filter-control="input"  class="text-right cust_billing_date" data-title-tooltip="'
								+ str(tooltip)
								+ '" data-sortable="true" '
								+ str(footer_formatter)
								+ ' '
								+ rowspan
								+'>'
								+ str(qstring)
								+ "</th>"
							)
						
						
						else:                    
							table_header += (
								'<th  data-field="'
								+ str(invs)
								+ '" data-filter-control="input" class="cust_billing_name" data-title-tooltip="'
								+ str(qstring)
								+ '" data-sortable="true" '
								+ rowspan
								+'>'
								+ str(qstring)
								+ "</th>"
							)
			table_header += "</tr>"
		if RECORD_ID == 'SYOBJR-00009':
			grouping_columns = ""
			if table_group_columns:
				grouping_columns += table_group_columns
			# if table_group_columns1:
			# 	grouping_columns += table_group_columns1
			if table_group_columns2:
				grouping_columns += table_group_columns2
			# if table_group_columns3:
			# 	grouping_columns += table_group_columns3
			# if table_group_columns4:
			# 	grouping_columns += table_group_columns4
			# if table_group_columns5:
			# 	grouping_columns += table_group_columns5 
			table_header += "<tr >{}</tr>".format(grouping_columns)
		# if RECORD_ID == 'SYOBJR-34575':
		# 	grouping_columns_delivery = ""
		# 	#if table_group_columns:
		# 	#Trace.Write('table_group_columns_delivery---'+str(table_group_columns_delivery))
			
			
		# 	grouping_columns_delivery += table_group_columns_delivery2
			
		# 	Trace.Write('table_group_columns_delivery2---'+str(table_group_columns_delivery2))

				
		# 	Trace.Write('grouping_columns_delivery---'+str(grouping_columns_delivery))
		# 	table_header += "<tr >{}</tr>".format(grouping_columns_delivery)
		if RECORD_ID == 'SYOBJR-00009':
			cls = "eq(3)"
			table_header += '</thead><tbody onclick="Table_Onclick_Scroll(this)"></tbody></table>'
	
		else:
			table_header += '</thead><tbody onclick="Table_Onclick_Scroll(this)"></tbody></table>'
		
		cls = "eq(2)"
		CHL_STS_OBJ = None

		if CHL_STS_OBJ is not None: # Not Needed
			Trace.Write('4512---4439------')
			dbl_clk_function += (
				'$("debugger;'
				+ str(table_ids)
				+ '").on("all.bs.table", function (e, name, args) { $(".bs-checkbox input").addClass("custom");if ($("input[name=\'btSelectAll\']:checkbox").is(":checked")) {$("button#delete_parts").removeAttr("disabled");} $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); }); $("'
				+ str(table_ids)
				+ '\ th.bs-checkbox div.th-inner").before("<div class=\'pad0brdbt\'>SELECT</div>"); $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); function onClickCell(event, field, value, row, $element) {if(localStorage.getItem("InlineEdit")=="YES"){ return ;} var reco_id=""; var reco = []; reco = localStorage.getItem("multiedit_checkbox_clicked"); if (reco === null || reco === undefined ){ reco = []; } if (reco.length > 0){reco = reco.split(",");} if (reco.length > 0){ reco.push($element.closest("tr").find("td:'
				+ str(cls)
				+ '").text());  data1 = $element.closest("tr").find("td:'
				+ str(cls)
				+ '").text(); localStorage.setItem("multiedit_save_date", data1); reco_id = removeDuplicates(reco); }else{reco_id=$element.closest("tr").find("td:'
				+ str(cls)
				+ '").text(); reco_id=reco_id.split(","); localStorage.setItem("multiedit_save_date", reco_id); } localStorage.setItem("multiedit_data_clicked", reco_id); localStorage.setItem("table_id_RL_edit", "'
				+ str(table_id)
				+ '"); cpq.server.executeScript("SYBLKETRLG", {"TITLE":field, "VALUE":value, "CLICKEDID":"'
				+ str(table_id)
				+ '", "RECORDID":reco_id, "ELEMENT":"RELATEDEDIT"}, function(data) { data1=data[0]; data2=data[1]; if(data1 != "NO"){ if(document.getElementById("RL_EDIT_DIV_ID") ) { document.getElementById("RL_EDIT_DIV_ID").innerHTML = data1; document.getElementById("cont_multiEditModalSection").style.display = "block"; $("#cont_multiEditModalSection").prepend("<div class=\'modal-backdrop fade in\'></div>"); var divHeight = $("#cont_multiEditModalSection").height(); $("#cont_multiEditModalSection .modal-backdrop").css("min-height", divHeight+"px"); $("#cont_multiEditModalSection .modal-dialog").css("width","550px"); $(".modal-dialog").css("margin-top","100px"); } if (data2.length !== 0){ $.each( data2, function( key, values ) { onclick_datepicker(values) }); } } }); }                   $("'
				+ str(table_ids)
				+ "\").on('sort.bs.table', function (e, name, order) {  currenttab = $(\"ul#carttabs_head .active\").text().trim(); localStorage.setItem('"
				+ str(table_id)
				+ "_SortColumn', name); localStorage.setItem('"
				+ str(table_id)
				+ "_SortColumnOrder', order); RelatedContainerSorting(name, order, '"
				+ str(table_id)
				+ "'); }); "
			)

		else:
			if RECORD_ID != "SYOBJR-00009":
				dbl_clk_function += (
					'var checkedRows=[]; localStorage.setItem("multiedit_checkbox_clicked", []); $("'
					+ str(table_ids)
					+ '").on("check.bs.table", function (e, row, $element) { console.log("checked00009==");checkedRows.push($element.closest("tr").find("td:'
					+ str(cls)
					+ '").text()); localStorage.setItem("multiedit_checkbox_clicked", checkedRows); }); $("'
					+ str(table_ids)
					+ '").on("check-all.bs.table", function (e) { var table = $("'
					+ str(table_ids)
					+ '").closest("table"); table.find("tbody tr").each(function() { checkedRows.push($(this).find("td:nth-child(3)").text()); }); localStorage.setItem("multiedit_checkbox_clicked", checkedRows); }); $("'
					+ str(table_ids)
					+ '").on("uncheck-all.bs.table", function (e) { localStorage.setItem("multiedit_checkbox_clicked", []); checkedRows=[]; }); $("'
					+ str(table_ids)
					+ '").on("uncheck.bs.table", function (e, row, $element) { var rec_ids=$element.closest("tr").find("td:'
					+ str(cls)
					+ '").text(); $.each(checkedRows, function(index, value) { if (value === rec_ids) { checkedRows.splice(index,1); }}); localStorage.setItem("multiedit_checkbox_clicked", checkedRows); });'
				)
				dbl_clk_function += (
					'debugger; localStorage.setItem("cont_table_id","'+str(table_id)+'");$("'
					+ str(table_ids)
					+ '").on("dbl-click-cell.bs.table", onClickCell); $("'
					+ str(table_ids)
					+ '").on("all.bs.table", function (e, name, args) { $(".bs-checkbox input").addClass("custom");if ($("'+str(table_ids)+' input[name=\'btSelectAll\']:checkbox").is(":checked")) { if(localStorage.getItem("CommonNodeTreeSuperParentParam") == "Comprehensive Services" || localStorage.getItem("CommonTreeParentParam") == "Complementary Products"){$("button#delete_parts").css("display","block"); }localStorage.setItem("selectall","yes");}if (!$("'+str(table_ids)+' input[name=\'btSelectAll\']:checkbox").is(":checked")){$("button#delete_parts").css("display","none");localStorage.setItem("selectall","no");} if($("'+str(table_ids)+' input[name=\'btSelectItem\']:checked").length > 1){ if(localStorage.getItem("CommonNodeTreeSuperParentParam") == "Comprehensive Services" || localStorage.getItem("CommonTreeParentParam") == "Complementary Products"){$("button#delete_parts").css("display","block");}localStorage.setItem("selectall","no");} if(!$("'+str(table_ids)+' input[name=\'btSelectItem\']:checked").length > 1){$("button#delete_parts").css("display","none");}$(".bs-checkbox input").after("<span class=\'lbl\'></span>"); }); $("'
					+ str(table_ids)
					+ '\ th.bs-checkbox div.th-inner").before("<div class=\'pad0brdbt\' >SELECT</div>"); $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); function onClickCell(event, field, value, row, $element) { if(localStorage.getItem("InlineEdit")=="YES"){ return ;}var reco_id=""; var reco = []; reco = localStorage.getItem("multiedit_checkbox_clicked"); if (reco === null || reco === undefined ){ reco = []; } if (reco.length > 0){reco = reco.split(",");} if (reco.length > 0){ reco.push($element.closest("tr").find("td:'
					+ str(cls)
					+ '").text());  data1 = $element.closest("tr").find("td:'
					+ str(cls)
					+ '").text(); localStorage.setItem("multiedit_save_date", data1);localStorage.setItem("PartsSelectedId",data1); reco_id = removeDuplicates(reco); }else{reco_id=$element.closest("tr").find("td:'
					+ str(cls)
					+ '").text(); reco_id=reco_id.split(","); localStorage.setItem("multiedit_save_date", reco_id);localStorage.setItem("PartsSelectedId",reco_id); } localStorage.setItem("multiedit_data_clicked", reco_id); localStorage.setItem("table_id_RL_edit", "'
					+ str(table_id)
					+ '"); cpq.server.executeScript("SYBLKETRLG", {"TITLE":field, "VALUE":value, "CLICKEDID":"'
					+ str(table_id)
					+ '", "RECORDID":reco_id, "ELEMENT":"RELATEDEDIT"}, function(data) { data1=data[0]; data2=data[1]; if(data1 != "NO"){ if(document.getElementById("RL_EDIT_DIV_ID") ) { document.getElementById("RL_EDIT_DIV_ID").innerHTML = data1;localStorage.setItem("PartsListBulkedit","yes");  document.getElementById("cont_multiEditModalSection").style.display = "block"; $("#cont_multiEditModalSection").prepend("<div class=\'modal-backdrop fade in\'></div>"); var divHeight = $("#cont_multiEditModalSection").height(); $("#cont_multiEditModalSection .modal-backdrop").css("min-height", divHeight+"px"); $("#cont_multiEditModalSection .modal-dialog").css("width","550px"); $(".modal-dialog").css("margin-top","100px"); }TreeParentParam = localStorage.getItem("CommonTreeParentParam");TreeParam = localStorage.getItem("CommonTreeParam");var sparePartsBulkSAVEBtn = $(".secondary_highlight_panel").find("button#spare-parts-bulk-save-btn");var sparePartsBulkEDITBtn = $(".secondary_highlight_panel").find("button#spare-parts-bulk-edit-btn");var sparePartsBulkAddBtn = $(".secondary_highlight_panel").find("button#spare-parts-bulk-add-modal-btn");if (data2.length !== 0){ $.each( data2, function( key, values ) { onclick_datepicker(values) }); } } }); }                   $("'
					+ str(table_ids)
					+ "\").on('sort.bs.table', function (e, name, order) {  currenttab = $(\"ul#carttabs_head .active\").text().trim(); localStorage.setItem('"
					+ str(table_id)
					+ "_SortColumn', name); localStorage.setItem('"
					+ str(table_id)
					+ "_SortColumnOrder', order); RelatedContainerSorting(name, order, '"
					+ str(table_id)
					+ "'); }); "
				)  
			else:
				Trace.Write('4512----')
				dbl_clk_function += (
					'var checkedRows=[]; localStorage.setItem("multiedit_checkbox_clicked", []); $("'
					+ str(table_ids)
					+ '").on("check.bs.table", function (e, row, $element) { console.log("checked00009==");checkedRows.push($element.closest("tr").find("td:'
					+ str(cls)
					+ '").text()); localStorage.setItem("multiedit_checkbox_clicked", checkedRows); }); $("'
					+ str(table_ids)
					+ '").on("check-all.bs.table", function (e) { var table = $("'
					+ str(table_ids)
					+ '").closest("table"); table.find("tbody tr").each(function() { checkedRows.push($(this).find("td:nth-child(3)").text()); }); localStorage.setItem("multiedit_checkbox_clicked", checkedRows); }); $("'
					+ str(table_ids)
					+ '").on("uncheck-all.bs.table", function (e) { localStorage.setItem("multiedit_checkbox_clicked", []); checkedRows=[]; }); $("'
					+ str(table_ids)
					+ '").on("uncheck.bs.table", function (e, row, $element) { var rec_ids=$element.closest("tr").find("td:'
					+ str(cls)
					+ '").text(); $.each(checkedRows, function(index, value) { if (value === rec_ids) { checkedRows.splice(index,1); }}); localStorage.setItem("multiedit_checkbox_clicked", checkedRows); });'
				)
				dbl_clk_function += (
					'debugger; console.log("checking--selectedvol");$("'
					+ str(table_ids)
					+ '").on("dbl-click-cell.bs.table", onClickCell); $("'
					+ str(table_ids)
					+ '").on("all.bs.table", function (e, name, args) { $(".bs-checkbox input").addClass("custom"); if ($("input[name=\'btSelectAll\']:checkbox").is(":checked")) {$("button#delete_parts").removeAttr("disabled");}$(".bs-checkbox input").after("<span class=\'lbl\'></span>"); }); $("'
					+ str(table_ids)
					+ '\ th.bs-checkbox div.th-inner").before("<div class=\'pad0brdbt\' >SELECT</div>"); $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); function onClickCell(event, field, value, row, $element) { if(localStorage.getItem("InlineEdit")=="YES"){ return ;}var reco_id=""; var reco = []; reco = localStorage.getItem("multiedit_checkbox_clicked"); if (reco === null || reco === undefined ){ reco = []; } if (reco.length > 0){reco = reco.split(",");} if (reco.length > 0){ reco.push($element.closest("tr").find("td:'
					+ str(cls)
					+ '").text());  data1 = $element.closest("tr").find("td:'
					+ str(cls)
					+ '").text(); localStorage.setItem("multiedit_save_date", data1); reco_id = removeDuplicates(reco); }else{reco_id=$element.closest("tr").find("td:'
					+ str(cls)
					+ '").text(); reco_id=reco_id.split(","); localStorage.setItem("multiedit_save_date", reco_id); } localStorage.setItem("multiedit_data_clicked", reco_id); localStorage.setItem("table_id_RL_edit", "'
					+ str(table_id)
					+ '"); cpq.server.executeScript("SYBLKETRLG", {"TITLE":field, "VALUE":value, "CLICKEDID":"'
					+ str(table_id)
					+ '", "RECORDID":reco_id, "ELEMENT":"RELATEDEDIT"}, function(data) { data1=data[0]; data2=data[1]; if(data1 != "NO"){ if(document.getElementById("RL_EDIT_DIV_ID") ) { document.getElementById("RL_EDIT_DIV_ID").innerHTML = "";$("input").prop("readonly",false); document.getElementById("cont_multiEditModalSection").style.display = "none"; var divHeight = $("#cont_multiEditModalSection").height(); $("#cont_multiEditModalSection .modal-backdrop").css("min-height", divHeight+"px"); $("#cont_multiEditModalSection .modal-dialog").css("width","550px"); $(".modal-dialog").css("margin-top","100px"); }TreeParentParam = localStorage.getItem("CommonTreeParentParam");TreeParam = localStorage.getItem("CommonTreeParam");var sparePartsBulkSAVEBtn = $(".secondary_highlight_panel").find("button#spare-parts-bulk-save-btn");var sparePartsBulkEDITBtn = $(".secondary_highlight_panel").find("button#spare-parts-bulk-edit-btn");var sparePartsBulkAddBtn = $(".secondary_highlight_panel").find("button#spare-parts-bulk-add-modal-btn");if (data2.length !== 0){ $.each( data2, function( key, values ) { onclick_datepicker(values) }); } } }); }                   $("'
					+ str(table_id)
					+ "_SortColumn', name); localStorage.setItem('"
					+ str(table_id)
					+ "_SortColumnOrder', order); RelatedContainerSorting(name, order, '"
					+ str(table_id)
					+ "'); }); "
				)
		

		NORECORDS = ""
		if len(table_list) == 0:
			NORECORDS = "NORECORDS"
		DropDownList = []
		filter_level_list = []
		filter_clas_name = ""
		cv_list = []		
		footer_str, footer = "", ""
		gettotalamt = ""
		if ObjectName == "SAQIBP":
			ContractRecordId = Product.GetGlobal("contract_quote_record_id")
			gettotaldateamt = Sql.GetList("SELECT BILLING_VALUE=SUM(BILLING_VALUE),ANNUAL_BILLING_AMOUNT = SUM(ANNUAL_BILLING_AMOUNT),BILLING_DATE FROM SAQIBP WHERE BILLING_DATE in {billing_date_column} and QUOTE_RECORD_ID ='{cq}' AND QTEREV_RECORD_ID='{revision_rec_id}' AND SERVICE_ID = '{service_id}' group by BILLING_DATE ".format(cq=str(ContractRecordId),revision_rec_id = quote_revision_record_id,billing_date_column=str(tuple(billing_date_column)),service_id = TreeParam))
			if gettotaldateamt:
				my_format = "{:,." + str(decimal_place) + "f}"
				for val in gettotaldateamt:
					if val.ANNUAL_BILLING_AMOUNT:
						gettotalamt = str(my_format.format(round(float(val.ANNUAL_BILLING_AMOUNT), int(decimal_place))))  
					
			if gettotaldateamt:
				my_format = "{:,." + str(decimal_place) + "f}"
			
				
				footer_tot += '<th colspan="1" class="text-left">{}</th>'.format(curr_symbol)
				footer_tot += '<th colspan="1" class="text-right">{}</th>'.format(gettotalamt)
				for val in gettotaldateamt:
					getamt = str(my_format.format(round(float(val.BILLING_VALUE), int(decimal_place))))
					footer_tot += '<th class="text-right">{}</th>'.format(getamt)
		# if  RECORD_ID == 'SYOBJR-00009' and str(TreeParam) == "Quote Items":
				#Columns = "['STATUS','EQUIPMENT_LINE_ID','SERVICE_ID','EQUIPMENT_ID','EQUIPMENT_DESCRIPTION','YEAR_OVER_YEAR','CONTRACT_VALID_FROM','CONTRACT_VALID_TO','SERIAL_NO','CUSTOMER_TOOL_ID','ASSEMBLY_ID','GREENBOOK','FABLOCATION_ID','KPU','TECHNOLOGY','TOOL_CONFIGURATION','TARGET_PRICE_INGL_CURR','SLSDIS_PRICE_INGL_CURR','BD_PRICE_INGL_CURR','CEILING_PRICE_INGL_CURR','NET_VALUE_INGL_CURR','DISCOUNT','TOTAL_AMOUNT_INGL_CURR','TAX_PERCENTAGE','NET_PRICE_INGL_CURR']"
		for key, col_name in enumerate(list(eval(Columns))):            
			StringValue_list = []
			filter_level_data = ""
			objss_obj = Sql.GetFirst(
				"SELECT API_NAME, DATA_TYPE, FORMULA_LOGIC, PICKLIST FROM  SYOBJD (nolock) WHERE OBJECT_NAME='"
				+ str(ObjectName)
				+ "' and API_NAME = '"
				+ str(col_name)
				+ "'"
			)           
			if objss_obj:				
				try:
					if str(objss_obj.PICKLIST).upper() == "TRUE":		                                          
						filter_level_data = "select"                        
						filter_clas_name = (
							'<div dropDownWidth="true" id = "'
							+ str(table_id)
							+ "_RelatedMutipleCheckBoxDrop_"
							+ str(key)
							+ '" class="form-control bootstrap-table-filter-control-'
							+ str(col_name)
							+ " RelatedMutipleCheckBoxDrop_"
							+ str(key)
							+ ' "></div>'
						)
						filter_level_list.append(filter_level_data)
					else:                     
						filter_level_data = "input"
						if str(col_name) == "QUOTE_REVISION_CONTRACT_ITEM_ID":
							# filter_level_data = "select"                        
							# filter_clas_name = (
							# 	'<div dropDownWidth="true" id = "'
							# 	+ str(table_id)
							# 	+ "_RelatedMutipleCheckBoxDrop_"
							# 	+ str(key)
							# 	+ '" class="form-control bootstrap-table-filter-control-'
							# 	+ str(col_name)
							# 	+ " RelatedMutipleCheckBoxDrop_"
							# 	+ str(key)
							# 	+ ' "></div>'
							# )
							# filter_level_list.append(filter_level_data)
							# filter_clas_name = ""
							filter_clas_name = (
								'<input type="text"  class="width100_vis form-control bootstrap-table-filter-control-'
								+ str(col_name)
								+ '">'
							)
						else:
							filter_clas_name = (
								'<input type="text"   class="width100_vis form-control bootstrap-table-filter-control-'
								+ str(col_name)
								+ '">'
							)
						filter_level_list.append(filter_level_data)
				except:
					if str(objss_obj.PICKLIST).upper() == "TRUE":		
						filter_level_data = "select"
						filter_clas_name = (
							'<div  id = "'
							+ str(table_id)
							+ "_RelatedMutipleCheckBoxDrop_"
							+ str(key)
							+ '" class="form-control bootstrap-table-filter-control-'
							+ str(col_name)
							+ " RelatedMutipleCheckBoxDrop_"
							+ str(key)
							+ ' "></div>'
						)
						filter_level_list.append(filter_level_data)
					else:                        
						filter_level_data = "input"
						if str(col_name) == "QUOTE_REVISION_CONTRACT_ITEM_ID":
							filter_clas_name = (
								'<input type="text"   class="width100_vis form-control bootstrap-table-filter-control-'
								+ str(col_name)
								+ '">'
							)
						else:
							filter_clas_name = (
									'<input type="text"  class="width100_vis form-control bootstrap-table-filter-control-'
									+ str(col_name)
									+ '">'
								)
						filter_level_list.append(filter_level_data)
				cv_list.append(filter_clas_name)
			
			#A055S000P01-4401
			##filter control for entitlement category for pricing view
			# if col_name == 'ENTITLEMENT_CATEGORY' and RECORD_ID == 'SYOBJR-00009' and pricing_picklist_value == 'Pricing' and str(TreeParam) == "Quote Items":
			# 	Trace.Write('ENTITLEMENT_CATEGORY')
			# 	ent_cat_list = ['KPI','MISC TERMS']
			# 	header3_list = ['ENTITLEMENT_NAME','ENTITLEMENT_COST','ENTITLEMENT_PRICE']
			# 	for i in ent_cat_list:
			# 		filter_level_data = ["input","input",'input']
			# 		temp_list = ['<input type="text"  class="width100_vis form-control bootstrap-table-filter-control-'+str(j)+'_'+ str(i).replace(' ','_')+ '">' for j in header3_list]

					
			# 		filter_level_list.extend(filter_level_data)
			# 		cv_list.extend(temp_list)

			if filter_level_data == "select" and col_name not in checkbox_list:                
				try:
					if str(col_name) == "EXCHANGE_RATE_DATE":						
						xcdStr = (
							"SELECT  Top 1000 CONVERT(VARCHAR(10),"
							+ str(col_name)
							+ ",101) as EXCHANGE_RATE_DATE  from "
							+ str(ObjectName)
							+ " (nolock) where "
							+ str(Wh_API_NAME)
							+ " = '"
							+ str(RecAttValue)
							+ "' ORDER BY CONVERT(DateTime,"
							+ str(col_name)
							+ ",101) DESC"
						)						
					else:
						if str(col_name) == 'TRACKING_TYPE':
							RecAttValue = Product.Attributes.GetByName("QSTN_SYSEFL_AC_00159").GetValue()
							Wh_API_NAME = "APPROVAL_TRACKED_FIELD_RECORD_ID"
						if str(RECORD_ID) == "SYOBJR-98788":
							doc_type = Sql.GetList("SELECT DOCTYP_ID FROM SAQTSV (NOLOCK) WHERE "+str(Wh_API_NAME)+" = '"+str(RecAttValue)+"' AND QTEREV_RECORD_ID = '"+ str(quote_revision_record_id)+"' ")

							for document_type in doc_type:
								if document_type.DOCTYP_ID == "ZWK1":
									xcdStr = (
										"SELECT DISTINCT TOP 10000000 "
										+ col_name
										+ " FROM "
										+ str(ObjectName)
										+ " (nolock)  where "
										+ str(Wh_API_NAME)
										+ " = '"
										+ str(RecAttValue) 
										+ "'"
										+ " AND QTEREV_RECORD_ID = '"
										+ str(quote_revision_record_id)
										+ "'" 
										+ "ORDER BY "
										+ str(col_name)
									)
								else:
									xcdStr = (
										"SELECT DISTINCT TOP 10000000 "
										+ col_name
										+ " FROM "
										+ str(ObjectName)
										+ " (nolock) JOIN (SELECT distinct PRDOFR_ID FROM MAADPR WHERE VISIBLE_INCONFIG = 'TRUE' )M ON SERVICE_ID = M.PRDOFR_ID  where "
										+ str(Wh_API_NAME)
										+ " = '"
										+ str(RecAttValue) 
										+ "'"
										+ " AND QTEREV_RECORD_ID = '"
										+ str(quote_revision_record_id)
										+ "'" 
										+ "ORDER BY "
										+ str(col_name)
									)
						else:	
							xcdStr = (
								"SELECT DISTINCT TOP 10000000 "
								+ col_name
								+ " FROM "
								+ str(ObjectName)
								+ " (nolock) where "
								+ str(Wh_API_NAME)
								+ " = '"
								+ str(RecAttValue)
								+ "'"
								+ " ORDER BY "
								+ str(col_name)
							)
					xcd = Sql.GetList(xcdStr)
				except:					
					if str(col_name) != "EXCHANGE_RATE_DATE":						
						xcdStr = (
							"SELECT "
							+ str(col_name)
							+ "  from "
							+ str(ObjectName)
							+ " (nolock) where "
							+ str(Wh_API_NAME)
							+ " = '"
							+ str(RecAttValue)
							+ "'"
						)
						xcd = Sql.GetList(xcdStr)

				try:
					if xcd is not None:
						StringValue_list = [
							str(eval("ins." + str(col_name))) for ins in xcd if eval("ins." + str(col_name)) != ""
						]						
						StringValue_list = filter(None, list(set(StringValue_list)))
						if len(StringValue_list) == 0:
							StringValue_list = [""]
					else:
						StringValue_list = [""]
					if str(col_name) == "EXCHANGE_RATE_DATE":
						StringValue_list.sort(key=lambda x: time.mktime(time.strptime(x, "%d/%m/%Y")), reverse=True)
					elif str(col_name) == 'TRACKING_TYPE':
						StringValue_list = ["ALL VALUES","ANY CHANGE"]
					else:
						StringValue_list.sort()
				except:
					StringValue_list = [""]
				StringValue_lists=[]
				
				for string in StringValue_list:
					string_value =""
					Trace.Write("string--"+str(string))
					if string == "ACQUIRED" or string == "PRICED":
						Trace.Write("priced status--"+str(string))
						string_value = string.replace(string,"<img title='"+str(string).title()+"' src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Green_Tick.svg> "+str(string))
						Trace.Write("string_value--"+str(string_value))
					if string == "APPROVAL REQUIRED":
						string_value = string.replace("APPROVAL REQUIRED","<img title='Approval Required' src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/clock_exe.svg> APPROVAL REQUIRED")
					if string == "ACQUIRING":                        
						string_value = string.replace("ACQUIRING","<img title='Acquiring' src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Cloud_Icon.svg> ACQUIRING")
					if string == "ERROR":
						string_value = string.replace("ERROR","<img title='Error' src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/exclamation_icon.svg> ERROR")
					if string == "ASSEMBLY IS MISSING":
						string_value = string.replace("ASSEMBLY IS MISSING","<img title='Assembly Missing' src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Orange1_Circle.svg> ASSEMBLY IS MISSING")
					if string == "PARTIALLY PRICED":
						string_value = string.replace("PARTIALLY PRICED","<img title='Partially Priced' src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Red1_Circle.svg> PARTIALLY PRICED")
					if string != "ACQUIRED" and string != "APPROVAL REQUIRED" and string != "ERROR" and string != "ASSEMBLY IS MISSING" and string != "PARTIALLY PRICED" and string != "ACQUIRING" and string != "PRICED":                        
						string_value = string
					StringValue_lists.append(string_value)
				DropDownList.append(StringValue_lists)
				Trace.Write("DropDownList--"+str(DropDownList))
				
			elif col_name in checkbox_list:
				DropDownList.append(["True", "False"])
			elif ObjectName == 'SAQIBP' and (col_name in billing_date_column or col_name == 'BILLING_CURRENCY'):# Billing Matrix - Pivot - Start
				try:
					gettotaldateamt =""
					if col_name in billing_date_column:                    
						my_format = "{:,." + str(decimal_place) + "f}"
						tovalue = 0.00
						getamt = ""                        
						#footer += '<th>{}{}</th>'.format(my_format.(sum([float(re.findall(r'value=["](.*?)["]',data.get(col_name))[0].split(" ")[0].replace(",","")) for data in table_list])) ,curr_symbol)
						for data in table_list:
							#Trace.Write('getval ---------'+str(float(re.findall(r'value=["](.*?)["]',data.get(col_name))[0].replace(",",""))))
							tovalue += float(re.findall(r'value=["](.*?)["]',data.get(col_name))[0].replace(",",""))
							getamt = str(my_format.format(round(float(tovalue), int(decimal_place))))
						footer += '<th class="text-right">{}</th>'.format(getamt)
					else:
						if table_list:
							currency_obj = re.search(r'>(.+?)<', table_list[0].get(col_name))
							if currency_obj:
								footer += '<th colspan="2" class="text-left">{}</th>'.format(currency_obj.group(1))
							else:
								footer += '<th colspan="2" class="text-left"></th>'
					
					#footer += '<th>{}{}</th>'.format(sum([float(re.findall(r'value=["](.*?)["]',data.get(col_name))[0].split(" ")[0].replace(",","")) for data in table_list]),curr_symbol)
					#footer += '<th>{}</th>'.format(sum([float(re.findall(r'value=["](.*?)["]',data.get(col_name))[0]) for data in table_list]))
				except Exception:                    
					footer += '<th>0.00</th>'
					footer_tot += '<th>0.00</th>'
				filter_level_data = "input"
				col_name = col_name.replace('/','-')
				col_name = col_name.replace('-','_')                
				filter_clas_name = (
					'<input type="text" class="width100_vis form-control bootstrap-table-filter-control-'
					+ str(col_name)
					+ '">'
				)
				filter_level_list.append(filter_level_data)
				cv_list.append(filter_clas_name)
			elif ObjectName == 'SAQSPD' and (col_name in delivery_date_column):
				Trace.Write('4831---col_name-'+str(col_name))
				filter_level_data = "input"
				col_name = col_name.replace('/','-')
				col_name = col_name.replace('-','_')                
				filter_clas_name = (
					'<input type="text" class="width100_vis form-control bootstrap-table-filter-control-'
					+ str(col_name)
					+ '">'
				)
				filter_level_list.append(filter_level_data)
				cv_list.append(filter_clas_name)
			else:
				DropDownList.append("")
		if ObjectName == 'SAQIBP' and TreeParam != 'Quote Items':
			#footer_str = '<tfoot><tr><th colspan="7" id= "getbill1year" class="text-left">{}</th>{}</tr><tr><th colspan="7" id= "getbillyear" class="text-left">{}</th>{}</tr></tfoot>'.format("SUBTOTAL", footer,str(SubTab)+" Total",footer_tot)
			footer_str = '<tfoot><tr><th colspan="7" id= "getbill1year" class="text-left">{}</th>{}</tr><tr></tr></tfoot>'.format("GRAND TOTAL", footer_tot)
		RelatedDrop_str = (
			"try { if( document.getElementById('"
			+ str(table_id)
			+ "') ) { var listws = document.getElementById('"
			+ str(table_id)
			+ "').getElementsByClassName('filter-control');  for (i = 0; i < listws.length; i++) { document.getElementById('"
			+ str(table_id)
			+ "').getElementsByClassName('filter-control')[i].innerHTML = data6[i];  } for (j = 0; j < listws.length; j++) { if (data7[j] == 'select') { var dataAdapter = new $.jqx.dataAdapter(data8[j]); if(data8[j].length>5){ $('#"
			+ str(table_id)
			+ "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter, dropDownWidth:200}); }else{$('#"
			+ str(table_id)
			+ "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter ,width: 200, autoDropDownHeight: true, dropDownWidth:200});} } } } }  catch(err) { setTimeout(function() { var listws = document.getElementById('"
			+ str(table_id)
			+ "').getElementsByClassName('filter-control');  for (i = 0; i < listws.length; i++) { document.getElementById('"
			+ str(table_id)
			+ "').getElementsByClassName('filter-control')[i].innerHTML = data6[i];  } for (j = 0; j < listws.length; j++) { if (data7[j] == 'select') { var dataAdapter = new $.jqx.dataAdapter(data8[j]); $('#"
			+ str(table_id)
			+ "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter, width: 200, dropDownWidth:200, scrollBarSize :10 }); } } }, 10); }"
		)
		
		try:
			get_Param_Val = Product.GetGlobal("CurrTreeParamVal")
			Selected_Node = Product.GetGlobal("SEL_NODE_LIST")
			#EXECUTION_TIME = Product.GetGlobal("EXECUTION")
			if get_Param_Val != "" and Selected_Node != "":
				Selected_Node = eval(Selected_Node)
				if get_Param_Val in Selected_Node:
					if Selected_Node.get(str(get_Param_Val)) == "1":
						
						filter_control_function += (
							'try { $("#'
							+ str(table_id)
							+ '").colResizable({ resizeMode:"overflow", onResize: function(){ $("div[id^=\''
							+ str(table_id)
							+ '_RelatedMutipleCheckBoxDrop\']").jqxDropDownList("close"); } }); } catch (err) { setTimeout(function(){ $("#'
							+ str(table_id)
							+ '").colResizable({ resizeMode:"overflow", onResize: function(){ $("div[id^=\''
							+ str(table_id)
							+ '_RelatedMutipleCheckBoxDrop\']").jqxDropDownList("close"); }}); }, 3000); } finally { setTimeout(function(){ $("#'
							+ str(table_id)
							+ '").colResizable({ resizeMode:"overflow" }); }, 5000); }'
						)
			else:				
				filter_control_function += (
					'try { $("#'
					+ str(table_id)
					+ '").colResizable({ resizeMode:"overflow", onResize: function(){ $("div[id^=\''
					+ str(table_id)
					+ '_RelatedMutipleCheckBoxDrop\']").jqxDropDownList("close"); } }); } catch (err) { setTimeout(function(){ $("#'
					+ str(table_id)
					+ '").colResizable({ resizeMode:"overflow", onResize: function(){ $("div[id^=\''
					+ str(table_id)
					+ '_RelatedMutipleCheckBoxDrop\']").jqxDropDownList("close"); } }); }, 3000); }  finally { setTimeout(function(){ $("#'
					+ str(table_id)
					+ '").colResizable({ resizeMode:"overflow" }); }, 5000); }'
				)				
		except:			
			filter_control_function += (
				'try { $("#'
				+ str(table_id)
				+ '").colResizable({ resizeMode:"overflow", onResize: function(){ $("div[id^=\''
				+ str(table_id)
				+ '_RelatedMutipleCheckBoxDrop\']").jqxDropDownList("close"); } }); } catch (err) { setTimeout(function(){ $("#'
				+ str(table_id)
				+ '").colResizable({ resizeMode:"overflow", onResize: function(){ $("div[id^=\''
				+ str(table_id)
				+ '_RelatedMutipleCheckBoxDrop\']").jqxDropDownList("close"); } }); }, 3000); } finally { setTimeout(function(){ $("#'
				+ str(table_id)
				+ '").colResizable({ resizeMode:"overflow"}); }, 5000); }'
			)
			
		filter_control_function += (
			"try {$('#SYOBJR_00005_7EAA11B4_82C9_400B_8E48_65497373A578').on('check-all.bs.table', function (e, row) {console.log('spare test edit----');$('#spare-parts-bulk-edit-btn').css('display','block') ;var selectedspares = []; var selectAll = false; $('#SYOBJR_00005_7EAA11B4_82C9_400B_8E48_65497373A578').find('[type =\"checkbox\"]:checked').map(function () { console.log('checked checkbox select------');if ($(this).attr('name') == 'btSelectAll'){ selectAll = true; } var sel_val = $(this).closest('tr').find('td:nth-child(3)').text(); if (sel_val != '') { selectedspares.push(sel_val);$('#spare-parts-bulk-edit-btn').css('display','block'); }else{$('#spare-parts-bulk-edit-btn').css('display','none');} }); console.log('selectedspares---',selectedspares); localStorage.setItem('selectedspares', selectedspares);if(selectedspares){console.log('indide spares--selectAll---',selectAll);}$('#SYOBJR_00005_7EAA11B4_82C9_400B_8E48_65497373A578').find('[type =\"checkbox\"]:not(:checked)').map(function () {console.log('indide spares--selectAll---',selectAll); if ($(this).attr('name') == 'btSelectAll'){$('#spare-parts-bulk-edit-btn').css('display','none');} })}) }catch (err){console.log('catch-----')}"
		)
		filter_control_function += ("try {$('#SYOBJR_95825_CD53CDDF_4575_493A_AFEF_BE4811E922FA').on('check-all.bs.table', function (e, row) {console.log('spare test edit----');var selectedconstriants= []; var selectAll = false; $('#SYOBJR_95825_CD53CDDF_4575_493A_AFEF_BE4811E922FA').find('[type =\"checkbox\"]:checked').map(function () { console.log('checked checkbox select------');if ($(this).attr('name') == 'btSelectAll'){ selectAll = true; } var sel_val = $(this).closest('tr').find('td:nth-child(3)').text(); if (sel_val != '') { $('#DROP_CONSTRAINT_BTN').css('display','block');$('#RECREATE_CONSTRAINT_BTN').css('display','none');$('#ADDNEW__SYOBJR_95825_SYOBJ_00426').css('display','none'); }else{$('#spare-parts-bulk-edit-btn').css('display','none');} }); console.log('selectedspares---',selectedspares); $('#SYOBJR_95825_CD53CDDF_4575_493A_AFEF_BE4811E922FA').find('[type =\"checkbox\"]:not(:checked)').map(function () {console.log('indide spares--selectAll---',selectAll); if ($(this).attr('name') == 'btSelectAll'){$('#DROP_CONSTRAINT_BTN').css('display','none');$('#RECREATE_CONSTRAINT_BTN').css('display','none');$('#ADDNEW__SYOBJR_95825_SYOBJ_00426').css('display','block');} })}) }catch (err){console.log('catch-----')}")
		
		if str(TreeParentParam) == "Billing":
			dbl_clk_function += (
				"try {var bildict = [];$('#SYOBJR_00007_26B8147E_C59C_4010_AA3A_38176869E305').on('click-row.bs.table', function (e, row, $element) { $('#SYOBJR_00007_26B8147E_C59C_4010_AA3A_38176869E305').find(':input(:disabled)').prop('disabled', false);$('#billingmatrix_save').css('display','block');$('#billingmatrix_cancel').css('display','block');$('#generatingbillingmatrix').css('display','none'); $('.billclassedit').parent().css('background-color','lightyellow');$('#SYOBJR_00007_26B8147E_C59C_4010_AA3A_38176869E305  tbody  tr td input').css('background-color','lightyellow');$('#billingmatrix_save').css('display','block');$('#billingmatrix_cancel').css('display','block'); var BillingmatrixBtn = $('.secondary_highlight_panel').find('button#REFRESH_MATRIX'); var billsave = $('.secondary_highlight_panel').find('button#billingmatrix_save'); var billcan = $('.secondary_highlight_panel').find('button#billingmatrix_cancel'); if (BillingmatrixBtn.length == 1){ BillingmatrixBtn.remove() } $('#billingmatrix_save').css('display','block'); $('#billingmatrix_cancel').css('display','block');$('#input#billeditval_disable').attr('disabled', true);$('#SYOBJR_00007_26B8147E_C59C_4010_AA3A_38176869E305 tbody tr td input').change(function () {console.log('on change function--');var getbillamt = $(this).val();console.log('getbillamt-------',getbillamt);localStorage.setItem('getbillamt', getbillamt);var equipid = $(this).closest('tr').find('td:nth-child(4)').text();var annualamt_total = $(this).closest('tr').find('td:nth-child(9)').text();console.log('eduip-----',equipid);var test = $(this).closest('td').index();var getindex = test+1;var getheaderdate = $('#SYOBJR_00007_26B8147E_C59C_4010_AA3A_38176869E305 thead th:nth-child('+getindex+')').text();var getannualtotal = $('#SYOBJR_00007_26B8147E_C59C_4010_AA3A_38176869E305 thead th:nth-child('+getindex+')').text();console.log('getannualtotal----',getannualtotal);console.log('annualamt_total----',annualamt_total);var concate_data = equipid+ ' - '+getheaderdate+ '- '+getbillamt+' - '+annualamt_total;if(!bildict.includes(concate_data)){bildict.push(concate_data)};getbilldictdata = JSON.stringify(bildict);localStorage.setItem('getbilldictdata', getbilldictdata);}); })}catch (err){console.log('catch-----')}"
			)
		if str(TreeParam) == "Delivery Schedule":
			dbl_clk_function += ("try{var deliverydict = [];$('#SYOBJR_34575_A67DBF63_1974_433F_A9BE_421D8D34C0C0 tbody tr td input').change(function () {console.log('on change function--');var getdeliveryamt = $(this).val();console.log('getdeliveryamt-------',getdeliveryamt);localStorage.setItem('getdeliveryamt', getdeliveryamt);var equipid = $(this).closest('tr').find('td:nth-child(4)').text();var annualamt_total = $(this).closest('tr').find('td:nth-child(9)').text();console.log('eduip-----',equipid);var test = $(this).closest('td').index();var getindex = test+1;var getheaderdate = $('#SYOBJR_34575_A67DBF63_1974_433F_A9BE_421D8D34C0C0 thead th:nth-child('+getindex+')').text();var getannualtotal = $('#SYOBJR_34575_A67DBF63_1974_433F_A9BE_421D8D34C0C0 thead th:nth-child('+getindex+')').text();console.log('getannualtotal----',getannualtotal);console.log('annualamt_total----',annualamt_total);var concate_data = equipid+ ' - '+getheaderdate+ '- '+getdeliveryamt+' - '+annualamt_total;if(!deliverydict.includes(concate_data)){deliverydict.push(concate_data)};getdeliverydictdata = JSON.stringify(deliverydict);localStorage.setItem('getdeliverydictdata', getdeliverydictdata);})}catch(err){console.log('catch-----')}")		
		if ObjectName == 'SAQICO':
			cls = "eq(3)"
			SAQICO_dbl_clk_function += (
				'var checkedRows=[]; localStorage.setItem("multiedit_checkbox_clicked", []); $("'
				+ str(table_ids)
				+ '").on("check.bs.table", function (e, row, $element) { console.log("checked00009==");checkedRows.push($element.closest("tr").find("td:'
				+ str(cls)
				+ '").text()); localStorage.setItem("multiedit_checkbox_clicked", checkedRows); }); $("'
				+ str(table_ids)
				+ '").on("check-all.bs.table", function (e) { var table = $("'
				+ str(table_ids)
				+ '").closest("table"); table.find("tbody tr").each(function() { checkedRows.push($(this).find("td:nth-child(4)").text()); }); localStorage.setItem("multiedit_checkbox_clicked", checkedRows); }); $("'
				+ str(table_ids)
				+ '").on("uncheck-all.bs.table", function (e) { localStorage.setItem("multiedit_checkbox_clicked", []); checkedRows=[]; }); $("'
				+ str(table_ids)
				+ '").on("uncheck.bs.table", function (e, row, $element) { var rec_ids=$element.closest("tr").find("td:'
				+ str(cls)
				+ '").text(); $.each(checkedRows, function(index, value) { if (value === rec_ids) { checkedRows.splice(index,1); }}); localStorage.setItem("multiedit_checkbox_clicked", checkedRows); });'
			)
			# buttons = "<button class=\'btnconfig\' onclick=\'multiedit_RL_cancel();\' type=\'button\' value=\'Cancel\' id=\'cancelButton\'>CANCEL</button><button class=\'btnconfig\' type=\'button\' value=\'Save\' onclick=\'multiedit_save_RL()\' id=\'saveButton\'>SAVE</button>" 
			SAQICO_dbl_clk_function += (    
				'$("'   
				+ str(table_ids)    
				+ '").on("dbl-click-cell.bs.table", onClickCell); $("'  
				+ str(table_ids)    
				+ '").on("all.bs.table", function (e, name, args) { $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); }); $("'  
				+ str(table_ids)    
				+ '\ th.bs-checkbox div.th-inner").before(""); $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); function onClickCell(event, field, value, row, $element) { if(localStorage.getItem("InlineEdit")=="YES"){ return ;} var reco_id=""; var reco = []; reco = localStorage.getItem("multiedit_checkbox_clicked"); if (reco === null || reco === undefined ){ reco = []; } if (reco.length > 0){reco = reco.split(",");} if (reco.length > 0){ reco.push($element.closest("tr").find("td:'   
				+ str(cls)  
				+ '").text());  data1 = $element.closest("tr").find("td:'   
				+ str(cls)  
				+ '").text(); localStorage.setItem("multiedit_save_date", data1); reco_id = removeDuplicates(reco); }else{reco_id=$element.closest("tr").find("td:' 
				+ str(cls)  
				+ '").text(); reco_id=reco_id.split(","); localStorage.setItem("multiedit_save_date", reco_id); } localStorage.setItem("multiedit_data_clicked", reco_id); localStorage.setItem("table_id_RL_edit", "'  
				+ str(table_id) 
				+ '");edit_index = $("'+str(table_ids)+'").find("[data-field="+ field +"]").index()+1;localStorage.setItem("edit_index",edit_index); cpq.server.executeScript("SYBLKETRLG", {"TITLE":field, "VALUE":value, "CLICKEDID":"'   
				+ str(table_id) 
				+ '", "RECORDID":reco_id, "ELEMENT":"RELATEDEDIT"}, function(data) { debugger; data1=data[0]; data2=data[1]; data3 = data[2];if(data1 != "NO"){ if(document.getElementById("RL_EDIT_DIV_ID") ) { localStorage.setItem("saqico_title", field); if(field == "DISCOUNT"){inp = "discount_" + data3; localStorage.setItem("saqico_value", inp); }else{inp = "#"+data3;} $("#SYOBJR_00009_E5504B40_36E7_4EA6_9774_EA686705A63F").find(inp).prop("disabled", false);localStorage.setItem("value_tag", "'+ str(table_id)+' "+inp); if (field == "DISCOUNT"){ $("'+str(table_ids)+' ").find("abbr[id="+inp+"]").parent().attr("contenteditable", true);} else{ $("'+str(table_ids)+' "+inp).closest("tr").find("td:nth-child("+edit_index+")").attr("contenteditable", true);}   var buttonlen = $("#seginnerbnr").find("button#saveButton"); if (buttonlen.length == 0){  RecId = "SYOBJR-00009";RecName = "div_CTR_Assemblies";$("#seginnerbnr").append("<button class=\'btnconfig\' type=\'button\' value=\'Save\' onclick=\'multiedit_save_RL()\' id=\'saveButton\'>SAVE</button><button class=\'btnconfig\' onclick=\'loadRelatedList(RecId,RecName);\' type=\'button\' value=\'Cancel\' id=\'cancelButton\'>CANCEL</button>");} else{$("#cancelButton").css("display", "block");$("#saveButton").css("display", "block");} if (field == "DISCOUNT"){ $("'+str(table_ids)+' ").find("abbr[id="+inp+"]").parent().addClass("light_yellow");}else{$("'+str(table_ids)+' " +inp).closest("tr").find("td:nth-child("+edit_index+")").addClass("light_yellow");} document.getElementById("cont_multiEditModalSection").style.display = "none";  var divHeight = $("#cont_multiEditModalSection").height(); $("#cont_multiEditModalSection .modal-backdrop").css("min-height", divHeight+"px"); $("#cont_multiEditModalSection .modal-dialog").css("width","550px"); $(".modal-dialog").css("margin-top","100px"); } if (data2.length !== 0){ $.each( data2, function( key, values ) { onclick_datepicker(values) }); } } }); }                   $("' 
				+ str(table_ids)    
				+ "\").on('sort.bs.table', function (e, name, order) {  currenttab = $(\"ul#carttabs_head .active\").text().trim(); localStorage.setItem('" 
				+ str(table_id) 
				+ "_SortColumn', name); localStorage.setItem('" 
				+ str(table_id) 
				+ "_SortColumnOrder', order); }); " 
			)

			SAQICO_dbl_clk_function += (
					'console.log("checking--select");$("'
					+ str(table_ids)
					+ '").on("all.bs.table", function (e, name, args) { console.log("sort.bs.table ============>11");$(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); }); $("'
					+ str(table_ids)
					+ '\ th.bs-checkbox div.th-inner").before("<div class=\'pad0brdbt\'>SELECT</div>"); $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); $("'
					+ str(table_ids)
					+ "\").on('sort.bs.table', function (e, name, order) { console.log('sort.bs.table ============>', e); e.stopPropagation(); currenttab = $(\"ul#carttabs_head .active\").text().trim(); localStorage.setItem('"
					+ str(table_id)
					+ "_SortColumn', name); localStorage.setItem('"
					+ str(table_id)
					+ "_SortColumnOrder', order); ATTRIBUTE_VALUEList = []; "+str(values_list)+"  QuoteitemContainerSorting(name, order, '"
					+ str(table_id)
					+ "',"+ str(list(eval(Columns)))+", ATTRIBUTE_VALUEList,'"+str(PR_CURR)+"','"+str(TP)+"','"+str(SubTab)+"'); }); "
					)	        

			
			dbl_clk_function = SAQICO_dbl_clk_function		 
		if RECORD_ID == "SYOBJR-98872":
			dbl_clk_function = ""
			dbl_clk_function += (
				'var checkedRows=[]; localStorage.setItem("multiedit_checkbox_clicked", []); $("'
				+ str(table_ids)
				+ '").on("check.bs.table", function (e, row, $element) { console.log("checked00009==");checkedRows.push($element.closest("tr").find("td:'
				+ str(cls)
				+ '").text()); localStorage.setItem("multiedit_checkbox_clicked", checkedRows); }); $("'
				+ str(table_ids)
				+ '").on("check-all.bs.table", function (e) { var table = $("'
				+ str(table_ids)
				+ '").closest("table"); table.find("tbody tr").each(function() { checkedRows.push($(this).find("td:nth-child(3)").text()); }); localStorage.setItem("multiedit_checkbox_clicked", checkedRows); }); $("'
				+ str(table_ids)
				+ '").on("uncheck-all.bs.table", function (e) { localStorage.setItem("multiedit_checkbox_clicked", []); checkedRows=[]; }); $("'
				+ str(table_ids)
				+ '").on("uncheck.bs.table", function (e, row, $element) { var rec_ids=$element.closest("tr").find("td:'
				+ str(cls)
				+ '").text(); $.each(checkedRows, function(index, value) { if (value === rec_ids) { checkedRows.splice(index,1); }}); localStorage.setItem("multiedit_checkbox_clicked", checkedRows); });'
			)
			dbl_clk_function += (
				'debugger; localStorage.setItem("cont_table_id","'+str(table_id)+'");$("'
				+ str(table_ids)
				+ '").on("dbl-click-cell.bs.table", onClickCell); $("'
				+ str(table_ids)
				+ '").on("all.bs.table", function (e, name, args) { $(".bs-checkbox input").addClass("custom");if ($("'+str(table_ids)+' input[name=\'btSelectAll\']:checkbox").is(":checked")) { if(localStorage.getItem("CommonNodeTreeSuperParentParam") == "Comprehensive Services" || localStorage.getItem("CommonTreeParentParam") == "Complementary Products"){$("button#delete_parts").css("display","block"); }localStorage.setItem("selectall","yes");}if (!$("'+str(table_ids)+' input[name=\'btSelectAll\']:checkbox").is(":checked")){$("button#delete_parts").css("display","none");localStorage.setItem("selectall","no");} if($("'+str(table_ids)+' input[name=\'btSelectItem\']:checked").length > 1){ if(localStorage.getItem("CommonNodeTreeSuperParentParam") == "Comprehensive Services" || localStorage.getItem("CommonTreeParentParam") == "Complementary Products"){$("button#delete_parts").css("display","block");}localStorage.setItem("selectall","no");} if(!$("'+str(table_ids)+' input[name=\'btSelectItem\']:checked").length > 1){$("button#delete_parts").css("display","none");}$(".bs-checkbox input").after("<span class=\'lbl\'></span>"); }); $("'
				+ str(table_ids)
				+ '\ th.bs-checkbox div.th-inner").before("<div class=\'pad0brdbt\' >SELECT</div>"); $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); function onClickCell(event, field, value, row, $element) { if(localStorage.getItem("InlineEdit")=="YES"){ return ;}var reco_id=""; var reco = []; reco = localStorage.getItem("multiedit_checkbox_clicked"); if (reco === null || reco === undefined ){ reco = []; } if (reco.length > 0){reco = reco.split(",");} if (reco.length > 0){ reco.push($element.closest("tr").find("td:'
				+ str(cls)
				+ '").text());  data1 = $element.closest("tr").find("td:'
				+ str(cls)
				+ '").text(); localStorage.setItem("multiedit_save_date", data1);localStorage.setItem("PartsSelectedId",data1); reco_id = removeDuplicates(reco); }else{reco_id=$element.closest("tr").find("td:'
				+ str(cls)
				+ '").text(); reco_id=reco_id.split(","); localStorage.setItem("multiedit_save_date", reco_id);localStorage.setItem("PartsSelectedId",reco_id); } localStorage.setItem("multiedit_data_clicked", reco_id); localStorage.setItem("table_id_RL_edit", "'
				+ str(table_id)
				+ '"); cpq.server.executeScript("SYBLKETRLG", {"TITLE":field, "VALUE":value, "CLICKEDID":"'
				+ str(table_id)
				+ '", "RECORDID":reco_id, "ELEMENT":"RELATEDEDIT"}, function(data) { data1=data[0]; data2=data[1]; if(data1 != "NO"){ if(document.getElementById("RL_EDIT_DIV_ID") ) { document.getElementById("RL_EDIT_DIV_ID").innerHTML = data1;localStorage.setItem("PartsListBulkedit","yes");  document.getElementById("cont_multiEditModalSection").style.display = "block"; $("#cont_multiEditModalSection").prepend("<div class=\'modal-backdrop fade in\'></div>"); var divHeight = $("#cont_multiEditModalSection").height(); $("#cont_multiEditModalSection .modal-backdrop").css("min-height", divHeight+"px"); $("#cont_multiEditModalSection .modal-dialog").css("width","550px"); $(".modal-dialog").css("margin-top","100px"); }TreeParentParam = localStorage.getItem("CommonTreeParentParam");TreeParam = localStorage.getItem("CommonTreeParam");var sparePartsBulkSAVEBtn = $(".secondary_highlight_panel").find("button#spare-parts-bulk-save-btn");var sparePartsBulkEDITBtn = $(".secondary_highlight_panel").find("button#spare-parts-bulk-edit-btn");var sparePartsBulkAddBtn = $(".secondary_highlight_panel").find("button#spare-parts-bulk-add-modal-btn");if (data2.length !== 0){ $.each( data2, function( key, values ) { onclick_datepicker(values) }); } } }); }                   $("'
				+ str(table_ids)
				+ "\").on('sort.bs.table', function (e, name, order) {  currenttab = $(\"ul#carttabs_head .active\").text().trim(); localStorage.setItem('"
				+ str(table_id)
				+ "_SortColumn', name); localStorage.setItem('"
				+ str(table_id)
				+ "_SortColumnOrder', order); RelatedContainerSorting(name, order, '"
				+ str(table_id)
				+ "'); }); "
			)         
		if QueryCount < int(Page_End):
			PageInformS = str(Page_start) + " - " + str(QueryCount) + " of"
		else:
			PageInformS = str(Page_start) + " - " + str(Page_End) + " of"
		Test = (
			'<div class="col-md-12 brdr listContStyle padbthgt30"  ><div class="col-md-4 pager-numberofitem  clear-padding"><span class="pager-number-of-items-item noofitem" id="'
			+ str(table_id)
			+ '_NumberofItem"  >'
			+ str(PageInformS)
			+ ' </span><span class="pager-number-of-items-item fltltpad2mrg0" id="'
			+ str(table_id)
			+ '_totalItemCount"  >'
			+ str(QueryCount)
			+ '</span><div class="clear-padding fltltmrgtp3" ><div  class="pull-right veralmert"><select onchange="PageFunctestChild(this, \'RelatedList\',\''
			+ str(RECORD_ID)
			+ "','"
			+ str(table_id)
			+ '\')" id="'
			+ str(table_id)
			+ '_PageCountValue"  class="form-control pagecunt"><option value="10" selected>10</option><option value="20">20</option><option value="50">50</option><option value="100">100</option><option value="200">200</option></select> </div></div></div><div class="col-xs-8 col-md-4  clear-padding totcnt"   data-bind="visible: totalItemCount"><div class="clear-padding col-xs-12 col-sm-6 col-md-12 brdr0"  ><ul class="pagination pagination"><li class="disabled"  ><a href="javascript:void(0)"  onclick="FirstPageLoad_paginationChild(\'RelatedList\', \''
			+ str(RECORD_ID)
			+ "','"
			+ str(table_id)
			+ '\')"><i class="fa fa-caret-left fnt14bold"  ></i><i class="fa fa-caret-left fnt14"  ></i></a></li><li class="disabled"><a href="javascript:void(0)" onclick="Previous12334Child(\'RelatedList\', \''
			+ str(RECORD_ID)
			+ "','"
			+ str(table_id)
			+ '\')" ><i class="fa fa-caret-left fnt14"  "></i>PREVIOUS</a></li><li class="disabled"><a href="javascript:void(0)" class="disabledPage"  onclick="Next12334Child(\'RelatedList\', \''
			+ str(RECORD_ID)
			+ "','"
			+ str(table_id)
			+ '\')">NEXT<i class="fa fa-caret-right fnt14"  ></i></a></li><li class="disabled"><a href="javascript:void(0)" onclick="LastPageLoad_paginationChild(\'RelatedList\', \''
			+ str(RECORD_ID)
			+ "','"
			+ str(table_id)
			+ '\')" class="disabledPage" ><i class="fa fa-caret-right fnt14"  ></i><i class="fa fa-caret-right fnt14bold"  ></i></a></li></ul></div> </div> <div class="col-md-4 pr_page_pad"  > <span id="'
			+ str(table_id)
			+ '_page_count" class="currentPage page_right_content">1</span><span class="page_right_content pad_rt_2"  >Page </span></div></div>'
		)
		return (
			table_header,
			table_list,
			table_id,
			filter_control_function,
			NORECORDS,
			dbl_clk_function,
			cv_list,
			filter_level_list,
			DropDownList,
			RelatedDrop_str,
			ObjectName,
			RECORD_ID,
			Test,
			PageInformS,
			PageInform,
			QueryCount,
			related_list_permissions,
			footer_str
		)

	def MDYNMICSQLOBJECTFILTER(
		self, RECORD_ID, ATTRIBUTE_NAME, ATTRIBUTE_VALUE, PerPage, PageInform, SortColumn, SortColumnOrder,  PR_CURR, TP ,SubTab,line_item
	):
		obj_obj1 = ""
		price_status = []
		obj_obj12 = getyears = col_year =exclamation= ""
		PageInformS = ""
		Page_start = ""
		QueryCount = key_value = ""
		Page_End = ""
		try:
			current_prod = Product.Name
		except:
			current_prod = "Sales"
		TreeParam = ""
		TreeParentParam = ""
		TreeSuperParentParam = ""
		TreeTopSuperParentParam = ""
		Qustr = ""
		imgValue = ""
		
		TreeParam = Product.GetGlobal("TreeParam")
		TreeParentParam = Product.GetGlobal("TreeParentLevel0") 
		TreeSuperParentParam = Product.GetGlobal("TreeParentLevel1") 
		TopTreeSuperParentParam = Product.GetGlobal("TreeParentLevel2") 
		TreeFirstSuperTopParentParam = Product.GetGlobal("TreeParentLevel3") 
		
		if str(PerPage) == "" and str(PageInform) == "":
			Page_start = 1
			Page_End = 10
			PerPage = 10
			PageInform = "1___10___10"
		else:
			Page_start = int(PageInform.split("___")[0])
			Page_End = int(PageInform.split("___")[1])
			PerPage = PerPage
		
		obj_obj = Sql.GetFirst(
			"""SELECT
										SYOBJR.RECORD_ID,SYOBJR.SAPCPQ_ATTRIBUTE_NAME, SYOBJR.PARENT_LOOKUP_REC_ID, SYOBJR.OBJ_REC_ID,
										SYOBJR.NAME, SYOBJR.COLUMN_REC_ID, SYOBJR.COLUMNS, SYOBJR.VISIBLE,
										SYOBJR.CAN_ADD, SYOBJR.CAN_EDIT, SYOBJR.CAN_DELETE, SYOBJR.RELATED_LIST_SINGULAR_NAME,
										SYOBJR.DISPLAY_ORDER, SYOBJR.ORDERS_BY
									FROM
										SYOBJR (NOLOCK)

									WHERE
										SYOBJR.SAPCPQ_ATTRIBUTE_NAME = '{RECORD_ID}'
									""".format(
				RECORD_ID=str(RECORD_ID)
			)
		)
		Columns = ""
		Obj_Name = ""
		table_id = ""
		COLUMN_REC_ID = ""
		col = ""
		text = ""
		texts = ""
		name = []
		related_list_edit_permission = False
		if current_prod == "SYSTEM ADMIN":
			current_prod = "SYSTEM ADMIN"

		CurrentModuleObj = Sql.GetFirst("select * from SYAPPS (NOLOCK) where APP_LABEL = '" + str(current_prod) + "'")
		crnt_prd_val = str(CurrentModuleObj.APP_ID)
		
		Qstn_REC_ID = ""
		CurrentObj_Recordno = ""
		CurrentObj_Name = ""
		Product_Name = ""
		tabs = Product.Tabs or "Quotes"
		list_of_tabs = []
		for tab in tabs:
			list_of_tabs.append(tab.Name)
		try:    
			TestProduct = Webcom.Configurator.Scripting.Test.TestProduct()
			Product_Name = TestProduct.Name
		except:
			Product_Name = "Sales"
		try:        
			current_tab = str(TestProduct.CurrentTab)
		except:
			current_tab = "Quotes"    
		Tree_Enable = ""
		Tree_Enable = Sql.GetFirst(
			"select ENABLE_TREE FROM SYTABS (NOLOCK) where UPPER(SAPCPQ_ALTTAB_NAME) ='"
			+ str(current_tab).upper()
			+ "' AND APP_RECORD_ID = '"
			+ str(str(CurrentModuleObj.APP_RECORD_ID))
			+ "'"
		)
		
		if Tree_Enable is not None:
			if str(Tree_Enable.ENABLE_TREE).upper() == "TRUE":
				(
					TreeParam,
					TreeParentParam,
					TreeSuperParentParam,
					TopTreeSuperParentParam,
					TreeTopSuperParentParam,
					TreeFirstSuperTopParentParam,
				) = (
					Product.GetGlobal("TreeParam"),
					Product.GetGlobal("TreeParentLevel0"),
					Product.GetGlobal("TreeParentLevel1"),
					Product.GetGlobal("TreeParentLevel2"),
					Product.GetGlobal("TreeParentLevel3"),
					Product.GetGlobal("TreeParentLevel4"),
				)
		if obj_obj is None:
			return "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""
		Action_permission = {}
		Wh_API_NAME = ""
		Wh_OBJECT_NAME = ""
		Query_Obj =  ""
		billing_date_column = ''
		if obj_obj is not None:
			Columns = obj_obj.COLUMNS
			Obj_Name = obj_obj.OBJ_REC_ID
			Obj_Name = obj_obj.OBJ_REC_ID
			COLUMN_REC_ID = obj_obj.COLUMN_REC_ID            
			PARENT_LOOKUP_REC_ID = obj_obj.PARENT_LOOKUP_REC_ID
			Action_permission["Edit"] = obj_obj.CAN_EDIT
			Action_permission["Delete"] = obj_obj.CAN_DELETE
			related_list_edit_permission = str(obj_obj.CAN_EDIT)            
			objd_where_obj = Sql.GetFirst("select * from  SYOBJD where RECORD_ID = '" + str(COLUMN_REC_ID) + "'")
			if objd_where_obj is not None:
				Wh_API_NAME = objd_where_obj.API_NAME
				Wh_OBJECT_NAME = objd_where_obj.OBJECT_NAME   
			try:                 
				contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
			except:
				contract_quote_record_id = ''    
			
			if Wh_OBJECT_NAME == 'SAQIBP':
				try:
					if SubTab:
						end = int(SubTab.split(' ')[-1]) * 12
						start = end - 12 + 1
						if TreeParam == "Billing":
							item_billing_plans_obj = Sql.GetList("""SELECT FORMAT(BILLING_DATE, 'MM-dd-yyyy') as BILLING_DATE FROM (SELECT ROW_NUMBER() OVER(ORDER BY BILLING_DATE)
										AS ROW, * FROM (SELECT DISTINCT BILLING_DATE
															FROM SAQIBP (NOLOCK) WHERE QUOTE_RECORD_ID = '{}'  AND QTEREV_RECORD_ID='{}'
															GROUP BY EQUIPMENT_ID, BILLING_DATE,SERVICE_ID) IQ) OQ WHERE OQ.ROW BETWEEN {} AND {}""".format(
																contract_quote_record_id, Quote.GetGlobal("quote_revision_record_id"), start, end))
						else:
							item_billing_plans_obj = Sql.GetList("""SELECT FORMAT(BILLING_DATE, 'MM-dd-yyyy') as BILLING_DATE FROM (SELECT ROW_NUMBER() OVER(ORDER BY BILLING_DATE)
										AS ROW, * FROM (SELECT DISTINCT BILLING_DATE
															FROM SAQIBP (NOLOCK) WHERE QUOTE_RECORD_ID = '{}'  AND SERVICE_ID = '{}' AND QTEREV_RECORD_ID='{}'
															GROUP BY EQUIPMENT_ID, BILLING_DATE,SERVICE_ID) IQ) OQ WHERE OQ.ROW BETWEEN {} AND {}""".format(
																contract_quote_record_id,TreeParam, Quote.GetGlobal("quote_revision_record_id"), start, end))

					
					if item_billing_plans_obj:
						billing_date_column = [item_billing_plan_obj.BILLING_DATE for item_billing_plan_obj in item_billing_plans_obj]                    
						billing_date_column_joined = ",".join(["'{}'".format(billing_data) for billing_data in billing_date_column])                    
						Columns = Columns.replace(']', ','+billing_date_column_joined+']')                     
				except:
					pass
			CurrentObj = Sql.GetFirst(
				"select API_NAME, OBJECT_NAME from  SYOBJD (nolock) where PARENT_OBJECT_RECORD_ID = '"
				+ str(PARENT_LOOKUP_REC_ID)
				+ "' and DATA_TYPE ='AUTO NUMBER'"
			)
			if CurrentObj is not None:
				CurrentObj_Recordno = CurrentObj.API_NAME                
				CurrentObj_Name = CurrentObj.OBJECT_NAME
			try:
				CurrentTabName = TestProduct.CurrentTab
			except:
				CurrentTabName = "Quotes"
			crnt_prd_val = str(CurrentModuleObj.APP_ID)
			Qstn_where_obj = Sql.GetFirst(
				"select * from SYSEFL (nolock) where API_NAME = '"
				+ str(CurrentObj_Name)
				+ "' and API_FIELD_NAME = '"
				+ str(CurrentObj_Recordno).strip()
				+ "' and SAPCPQ_ATTRIBUTE_NAME like '%"
				+ str(crnt_prd_val)
				+ "%' "
			)

			if Qstn_where_obj is not None:
				Qstn_REC_ID = Qstn_where_obj.SAPCPQ_ATTRIBUTE_NAME
				if Qstn_REC_ID != "":
					wh_Qstn_REC_ID = "QSTN_" + Qstn_REC_ID.replace("-", "_")  
									
					RecAttValue = ""
					try:
						RecAtt = productAttributesGetByName(str(wh_Qstn_REC_ID))
						

						if RecAtt is not None:
							RecAttValue = RecAtt.GetValue()
						#A055S000P01-3414 - start related list sort issue    
						if str(current_tab) == "Tab" and str(current_prod) == "SYSTEM ADMIN":
							
							RecAttValue = productAttributesGetByName("QSTN_SYSEFL_SY_03295").GetValue()
						#A055S000P01-3414 - end related list sort issue     
						if str(current_tab) == "Account" and str(current_prod) == "QUOTAS":
							RecAttValue = productAttributesGetByName("QSTN_SYSEFL_TQ_00084").GetValue()
							
					except:
						RecAttValue = ""
			table_id = obj_obj.SAPCPQ_ATTRIBUTE_NAME.replace("-", "_") + "_" + str(Obj_Name).replace("-", "_")
		
		table_list = []
		Qury_str = ""

		QuryCount_str = ""
		footer_str = ""
		footer_tot = ""
		if Columns != "" and Obj_Name != "":
			objh_obj = Sql.GetFirst("select * from SYOBJH (nolock) where RECORD_ID = '" + str(Obj_Name) + "'")
			
			ObjectName = objh_obj.OBJECT_NAME
			objRecName = objh_obj.RECORD_NAME.strip()
			Objd_Obj = Sql.GetList(
				"select FIELD_LABEL,FORMULA_DATA_TYPE,DATA_TYPE,API_NAME,LOOKUP_API_NAME,FIELD_SHORT_LABEL from  SYOBJD (nolock) where OBJECT_NAME = '"
				+ str(ObjectName)
				+ "'"
			)
			
			attr_list = []
			lookup_disply_list = []
			if Objd_Obj is not None:
				attr_list = {}
				for attr in Objd_Obj:
					if attr.FIELD_SHORT_LABEL is not None or attr.FIELD_SHORT_LABEL != "":
						attr_list[str(attr.API_NAME)] = str(attr.FIELD_SHORT_LABEL)
					else:
						attr_list[str(attr.API_NAME)] = str(attr.FIELD_LABEL)

					attr_list[str(attr.API_NAME)] = str(attr.FIELD_LABEL)
					if attr is not None:
						if (
							attr.LOOKUP_API_NAME is not None
							and attr.LOOKUP_API_NAME != ""
							and str(attr.LOOKUP_API_NAME) not in ["CONTROLLING_FIELD", "DEPENDENT_FIELD"]
						):
							lookup_disply_list.append(str(attr.API_NAME))
						checkbox_list = [
							inn.API_NAME
							for inn in Objd_Obj
							if (inn.DATA_TYPE == "CHECKBOX" or inn.FORMULA_DATA_TYPE == "CHECKBOX")
						]
				lookup_list = {ins.LOOKUP_API_NAME: ins.API_NAME for ins in Objd_Obj}
				if "QUOTE_REV_PO_PRODUCT_LIST_ID" in lookup_disply_list and ObjectName == "SAQRSP":
					try:
						lookup_disply_list.remove("QUOTE_REV_PO_PRODUCT_LIST_ID")
						lookup_disply_list.remove("PART_DESCRIPTION")
						lookup_disply_list.remove("PART_NUMBER")
						lookup_disply_list.remove("SERVICE_ID")
						lookup_disply_list.remove("FABLOCATION_ID")
						lookup_disply_list.remove("GREENBOOK")
					except:
						pass
				elif "QUOTE_REVISION_CONTRACT_ITEM_ID" in lookup_disply_list and ObjectName == "SAQRIT":
					try:
						lookup_disply_list.remove("QUOTE_REVISION_CONTRACT_ITEM_ID")
					except:
						pass
				elif "QUOTE_REV_ITEM_GREENBK_SUMRY_RECORD_ID" in lookup_disply_list and ObjectName == "SAQIGS":
					try:
						lookup_disply_list.remove("QUOTE_REV_ITEM_GREENBK_SUMRY_RECORD_ID")
						lookup_disply_list.remove("CONTRACT_VALID_FROM")
						lookup_disply_list.remove("CONTRACT_VALID_TO")
						lookup_disply_list.remove("GREENBOOK")
					except:
						pass
				
				elif "QUOTE_REV_DEAL_TEAM_MEMBER_ID" in lookup_disply_list and ObjectName == "SAQDLT":
					try:
						lookup_disply_list.remove("QUOTE_REV_DEAL_TEAM_MEMBER_ID")
						lookup_disply_list.remove("C4C_PARTNERFUNCTION_ID")
						lookup_disply_list.remove("CRM_PARTNERFUNCTION_ID")
						
					except:
						pass
			lookup_str = ",".join(list(lookup_disply_list))
			obj_str = ",".join(list(eval(Columns)))
			if lookup_str != "":
				select_obj_str = str(obj_str) + "," + str(lookup_str)
			else:
				select_obj_str = str(obj_str)
			Trace.Write("obj_str---- "+str(obj_str))
			Trace.Write("select_obj_str---- "+str(select_obj_str))
			lookup_disply_list123 = ""
			lookup_str = ",".join(list(lookup_disply_list))
			if len(list(lookup_disply_list)) > 1:
				lookup_disply_list123 = list(lookup_disply_list)[0]
			else:
				if len(list(eval(Columns))) > 1:
					lookup_disply_list123 = list(eval(Columns))[0]
			name = select_obj_str.split(",")
			
			for text in name:
				s = Sql.GetList(
					"select DATA_TYPE,API_NAME,LENGTH,DECIMALS,FORMULA_DATA_TYPE from  SYOBJD (nolock) WHERE API_NAME='"
					+ str(text)
					+ "' and OBJECT_NAME='"
					+ str(ObjectName).strip()
					+ "'"
				)
				for ins in s:
					if (ins.DATA_TYPE == "DATE" or ins.FORMULA_DATA_TYPE == "DATE") or (
						ins.API_NAME
						in [
							"EFFECTIVEDATE_BEG",
							"EFFECTIVEDATE_END",
							"PROMOTION_START_DATE",
							"PROMOTION_END_DATE",
							"EXCHANGE_RATE_DATE",
						]
					):
						if str(RECORD_ID) == "SYOBJR-00007" and ins.API_NAME == 'BILLING_DATE':
							text = "CONVERT(VARCHAR(10),FORMAT(" + str(text) + ",'MM-dd-yyyy'),101) AS [" + str(text) + "]"
							texts = texts + "," + str(text)
						elif texts != "":
							text = "CONVERT(VARCHAR(10)," + str(text) + ",101) AS [" + str(text) + "]"
							texts = texts + "," + str(text)
						else:
							text = "CONVERT(VARCHAR(10)," + str(text) + ",101) AS [" + str(text) + "]"
							texts = str(text)
					else:
						if col != "":
							col = col + "," + text
						else:
							col = str(text)
			if texts != "":
				col = col + "," + texts
			if billing_date_column:
				column_before_pivot_change = col
				col += ","+ ",".join(billing_date_column)
			select_obj_str = col
			Trace.Write('@5221, Select obj str-->'+str(select_obj_str))
			edit_field = []
			OrderBy_obj = Sql.GetFirst("select ORDERS_BY from SYOBJR (NOLOCK) where RECORD_ID = '" + str(RECORD_ID) + "'")
			
			if Qstn_REC_ID != "" and Wh_API_NAME != "":
				if OrderBy_obj is not None:
					if OrderBy_obj.ORDERS_BY:
						Wh_API_NAMEs = OrderBy_obj.ORDERS_BY
					else:
						Wh_API_NAMEs = Wh_API_NAME
				else:
					Wh_API_NAMEs = Wh_API_NAME

				if (
					RECORD_ID != "SYOBJR-92121"
					and RECORD_ID != "SYOBJR-92122"
					and RECORD_ID != "SYOBJR-93171"
					and RECORD_ID != "SYOBJR-93164"
					and RECORD_ID != "SYOBJR-93155"
					and RECORD_ID != "SYOBJR-93163"
				):                    
					if SortColumn == "" and SortColumnOrder == "":                        
						Wh_API_NAMEs = Wh_API_NAMEs
					elif SortColumn in billing_date_column:
						Wh_API_NAMEs = " CONVERT(VARCHAR(10),FORMAT("+str(SortColumn)+",'MM-dd-yyyy'),101) " + str(SortColumnOrder).upper()
					else:                        
						Wh_API_NAMEs = str(SortColumn) + " " + str(SortColumnOrder).upper()                                              
				else:                    
					if SortColumn == "" and SortColumnOrder == "":
						if not "DESC" in Wh_API_NAMEs and "ASC" in Wh_API_NAMEs:
							Wh_API_NAMEs = Wh_API_NAMEs + " ASC"
					else:                        
						Wh_API_NAMEs = str(SortColumn) + " " + str(SortColumnOrder).upper()
				ATTRIBUTE_VALUE_STR = ""
				Dict_formation = dict(zip(ATTRIBUTE_NAME, ATTRIBUTE_VALUE))
							

				if ATTRIBUTE_NAME:
					if ObjectName == 'SAQICO' and RECORD_ID == 'SYOBJR-00009': #added the code for pricing status image filters
						xa = list(ATTRIBUTE_NAME)[1]
					else:
						xa = list(ATTRIBUTE_NAME)[0] 
								
					if Dict_formation.get(str(xa)) != "":

						if str(Dict_formation.get(str(xa))).find(",") == -1:
							if str(Dict_formation.get(str(xa))).find("-") == -1:
								try:
									J_str = (
										"select "
										+ str(xa)
										+ " from "
										+ str(ObjectName)
										+ " (nolock) where CpqTableEntryId = '"
										+ str(Dict_formation.get(str(xa)))
										+ "' "
									)

								except:
									J_str = (
										"select "
										+ str(xa)
										+ " from "
										+ str(ObjectName)
										+ " (nolock) where CpqTableEntryId = '"
										+ str(Dict_formation.get(str(xa)))
										+ "' "
									)
							else:
								xa_str = Dict_formation.get(str(xa)).split("-")[1]
								
								J_str = (
									"select "
									+ str(xa)
									+ " from "
									+ str(ObjectName)
									+ " (nolock) where CpqTableEntryId = '"
									+ str(int(xa_str))
									+ "' "
								)
						else:
							xa_str = []                        
							for data in Dict_formation.get(str(xa)).split(","):
								xa_str.append(
									int(data.split("-")[1]) if str(Dict_formation.get(str(xa))).find("-") != -1 else int(data)
								)
							xa_str = tuple(xa_str)                        
							J_str = (
								"select "
								+ str(xa)
								+ " from "
								+ str(ObjectName)
								+ " (nolock) where CpqTableEntryId in "
								+ str(xa_str)
								+ ""
							)
						J_obj = Sql.GetList(J_str)

						if J_obj is not None and str(J_obj) != "" and len(J_obj) > 0:
							xa_list = [eval("kn." + str(xa)) for kn in J_obj]
							Dict_formation[str(xa)] = ",".join(xa_list)
						else:
							xa_list = [""]
							Dict_formation[str(xa)]

				for quer_key, quer_value in enumerate(Dict_formation):                    
					if Dict_formation.get(quer_value) != "" and Dict_formation.get(quer_value) is not None:
						quer_values = str(Dict_formation.get(quer_value)).strip()
						SYOBJD_obj = Sql.GetFirst(
							"select DATA_TYPE, PICKLIST, FORMULA_DATA_TYPE from SYOBJD (nolock) where API_NAME = '"
							+ str(quer_value)
							+ "' and OBJECT_NAME ='"
							+ str(ObjectName)
							+ "' "
						)

						picklist_data = ""
						api_data_type = ""

						if SYOBJD_obj is not None:
							api_data_type = (
								str(SYOBJD_obj.DATA_TYPE)
								if str(SYOBJD_obj.DATA_TYPE) != "FORMULA"
								else str(SYOBJD_obj.FORMULA_DATA_TYPE)
							)
							picklist_data = str(SYOBJD_obj.PICKLIST)
													
						if str(quer_values).find(",") == -1:
							
							if str(picklist_data).upper() == "TRUE":
								if str(quer_values).upper() == "TRUE":
									quer_values = ["1", "true"]
									##removed additional braces for checkbox column at first and last in ATTRIBUTE_VALUE_STR 
									ATTRIBUTE_VALUE_STR += (
										str(quer_value) + " in " + str(tuple(quer_values)) + " and "
									)                                    
								elif str(quer_values).upper() == "FALSE":
									if RECORD_ID == "SYOBJR-30330":
										quer_values = ["0", "false"]
										ATTRIBUTE_VALUE_STR += (
											"(" + str(quer_value) + " in " + str(tuple(quer_values)) + ") and "
										)
									else:
										quer_values = ["0", "false", " ", ""]

										quer_values = str(tuple(quer_values)) + " OR " + str(quer_value) + " IS NULL "
										ATTRIBUTE_VALUE_STR += "(" + str(quer_value) + " in " + str(quer_values) + ") AND "  
								elif str(quer_values).upper() == "TRUE" and str(quer_values).upper() == "FALSE":                                    
									quer_values = ["0", "false", " ", "", "1", "true"]
									quer_values = str(tuple(quer_values)) + " OR " + str(quer_value) + " IS NULL "
									trueFalseCondition = True
									Falsecondition = True
									if str(quer_value) == "EXCLUSIVE_MATERIAL":
										ATTRIBUTE_VALUE_STR += (
											"(EXCLUSIVE_MATERIAL is NULL or "
											+ str(quer_value)
											+ " in "
											+ str(tuple(quer_values))
											+ ") and "
										)
									elif str(quer_value) == "ACTIVE":
										ATTRIBUTE_VALUE_STR += (
											"(ACTIVE is NULL or "
											+ str(quer_value)
											+ " in "
											+ str(tuple(quer_values))
											+ ") and "
										)
									elif str(quer_value) == "FULFILLMENT_EXCLUDED":
										ATTRIBUTE_VALUE_STR += (
											"(FULFILLMENT_EXCLUDED is NULL or "
											+ str(quer_value)
											+ " in "
											+ str(tuple(quer_values))
											+ ") and "
										)
									else:
										if Falsecondition:
											ATTRIBUTE_VALUE_STR += (
												"(" + str(quer_value) + " in " + str(quer_values) + ") and "
											)
										else:
											ATTRIBUTE_VALUE_STR += (
												str(quer_value) + " in " + str(tuple(quer_values)) + " and "
											) 
								elif str(quer_value) == 'STATUS' and str(RECORD_ID) == 'SYOBJR-00009':
									if 'ACQUIRING' in quer_values:
										quer_values = "ACQUIRING"
									elif 'MISSING' in quer_values:
										quer_values = "ASSEMBLY IS MISSING"
									elif 'ACQUIRED' in quer_values:
										quer_values = "ACQUIRED"
									elif 'PARTIALLY PRICED' in quer_values:
										quer_values = "PARTIALLY PRICED"
									elif 'APPROVAL REQUIRED' in quer_values:
										quer_values = "APPROVAL REQUIRED"
									elif 'ERROR' in quer_values:
										quer_values = "ERROR"
									ATTRIBUTE_VALUE_STR += str(quer_value) + " = '" + str(quer_values) + "' and "   
								elif str(quer_value) == 'STATUS' and str(RECORD_ID) == 'SYOBJR-98872':
									remove_tag =re.compile(r'<[^>]+>')
									quer_values=remove_tag.sub('',quer_values)
									quer_values = quer_values.strip()
									ATTRIBUTE_VALUE_STR += str(quer_value) + " = '" + str(quer_values) + "' and "
									Trace.Write(str(ATTRIBUTE_VALUE_STR))
								else:
									ATTRIBUTE_VALUE_STR += str(quer_value) + " = '" + str(quer_values) + "' and "
							else:
															
								if re.search(r"(\d+/\d+/\d+)", quer_values) and api_data_type in ("DATE"):
									if api_data_type == "DATE":
										re_format = r"^(((0)[0-9])|((1)[0-2]))(\/)([0-2][0-9]|(3)[0-1])(\/)\d{4}$"
										result = re.match(re_format, quer_values)
										if result is None:
											quer_values = ""
									ATTRIBUTE_VALUE_STR += " " + str(quer_value) + " = '" + str(quer_values) + "' and "                                    

								elif api_data_type == "AUTO NUMBER":
									if len(quer_values) >= 1:
										if "," not in str(quer_values):
											quer_values = quer_values
										else:
											quer_values = tuple(quer_values)
										quer_values = quer_values
										if str(quer_values) != "":
											ATTRIBUTE_VALUE_STR += (
												str(quer_value) + " = '" + str(quer_values) + "' and "
												if str(quer_values) != ""
												else " 1=1 and "
											)
								elif ObjectName == 'SAQIBP' and (str(quer_value) in 'BILLING_VALUE' or 'BILLING_DATE' in str(quer_value) or '20' in str(quer_value)):                                    
									ATTRIBUTE_VALUE_STR += "BILLING_DATE = '" + str(SortColumn) + "' and BILLING_VALUE like '%" + str(quer_values) + "%' and "                                  
								else:
																		
									ATTRIBUTE_VALUE_STR += str(quer_value) + " like '%" + str(quer_values) + "%' and "
						else:                            
							quer_values = quer_values.split(",")
							quer_values = tuple(list(quer_values)) if len(quer_values) > 1 else "('" + quer_values[0] + "')"
							
							if "TRUE" in str(quer_values).upper() and "FALSE" in str(quer_values).upper():
								quer_values_list = ["0", "false", " ", "", "1", "true"]
								quer_values = str(tuple(quer_values_list)) + " OR " + str(quer_value) + " IS NULL "
								trueFalseCondition = True                                

							if str(quer_value) == "EXCLUSIVE_MATERIAL":
								ATTRIBUTE_VALUE_STR += str(quer_value) + " in " + str(tuple(quer_values)) + " and "
							elif str(quer_value) == "FULFILLMENT_EXCLUDED":
								quer_values = ["0", "false", " ", "", "1", "true"]
								ATTRIBUTE_VALUE_STR += (
									"(FULFILLMENT_EXCLUDED is NULL or "
									+ str(quer_value)
									+ " in "
									+ str(tuple(quer_values))
									+ ") and "
								)
							elif str(quer_value) == "STD_FULFILL_TO_CTY":
								quer_values = ["0", "false", " ", "", "1", "true"]
								ATTRIBUTE_VALUE_STR += (
									"(STD_FULFILL_TO_CTY is NULL or "
									+ str(quer_value)
									+ " in "
									+ str(tuple(quer_values))
									+ ") and "
								)

							elif str(quer_value) == "XFR_FULFILL_TO_CTY":
								quer_values = ["0", "false", " ", "", "1", "true"]
								ATTRIBUTE_VALUE_STR += (
									"(XFR_FULFILL_TO_CTY is NULL or "
									+ str(quer_value)
									+ " in "
									+ str(tuple(quer_values))
									+ ") and "
								)
							elif str(quer_value) == "EXP_FULFILL_TO_CTY":
								quer_values = ["0", "false", " ", "", "1", "true"]
								ATTRIBUTE_VALUE_STR += (
									"(EXP_FULFILL_TO_CTY is NULL or "
									+ str(quer_value)
									+ " in "
									+ str(tuple(quer_values))
									+ ") and "
								)

							elif str(quer_value) == "VISIBLEINCATALOG":                                
								quer_values = ["0", "false", " ", "", "1", "true"]
								ATTRIBUTE_VALUE_STR += (
									"(VISIBLEINCATALOG is NULL or "
									+ str(quer_value)
									+ " in "
									+ str(tuple(quer_values))
									+ ") and "
								)
							elif str(quer_value) == 'STATUS' and str(RECORD_ID) == 'SYOBJR-00009':
								quer_values = list(quer_values)
								
								for i in range(0,len(quer_values)):

									if 'ACQUIRING' in quer_values[i]:
										quer_values[i] = "ACQUIRING"
									elif 'MISSING' in quer_values[i]:
										quer_values[i] = "ASSEMBLY IS MISSING"
									elif 'ACQUIRED' in quer_values[i]:
										quer_values[i] = "ACQUIRED"
									elif 'PARTIALLY PRICED' in quer_values[i]:
										quer_values[i] = "PARTIALLY PRICED"
									elif 'APPROVAL REQUIRED' in quer_values[i]:
										quer_values[i] = "APPROVAL REQUIRED"
									elif 'ERROR' in quer_values[i]:
										quer_values[i] = "ERROR"
								quer_values = tuple(quer_values)
								
								ATTRIBUTE_VALUE_STR += "(" + str(quer_value) + " in " + str(quer_values) + ") and "                                          
							elif str(quer_value) == 'STATUS' and str(RECORD_ID) == 'SYOBJR-98872':
								remove_tag =re.compile(r'<[^>]+>')
								status_list = []
								for value in quer_values:
									quer_values=remove_tag.sub('',value)
									quer_values = quer_values.strip()
									status_list.append(quer_values)
								ATTRIBUTE_VALUE_STR += "(" + str(quer_value) + " in " + str(tuple(status_list)) + ") and "                                          
							else:
								if api_data_type == "AUTO NUMBER":
									ATTRIBUTE_VALUE_STR += (
										str(quer_value) + " in " + str(quer_values) + " and "
										if str(quer_values) != ""
										else " 1=1 and "
									)
								elif (
									re.search(r"(\d+/\d+/\d+)", quer) for quer in str(quer_values).split(",")
								) and api_data_type in ("DATE"):
									ATTRIBUTE_VALUE_STR += " " + str(quer_value) + " in " + str(quer_values) + " and "
								else:
									trueFalseCondition = True
									if trueFalseCondition:
										ATTRIBUTE_VALUE_STR += "(" + str(quer_value) + " in " + str(quer_values) + ") and "
									else:
										ATTRIBUTE_VALUE_STR += str(quer_value) + " in " + str(quer_values) + " and "
				
				#Contract valid start date & End date Calculation--START
				try:
					contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
					quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
				except:
					contract_quote_record_id = '' 
					quote_revision_record_id = ''   
				Getyear = Sql.GetFirst("select CONTRACT_VALID_FROM,CONTRACT_VALID_TO from SAQTMT where MASTER_TABLE_QUOTE_RECORD_ID = '"+str(contract_quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' ")
				
				if Getyear:
					start_date = datetime(Getyear.CONTRACT_VALID_FROM)
					end_date = datetime(Getyear.CONTRACT_VALID_TO)
					mm = (end_date. year - start_date. year) * 12 + (end_date. month - start_date. month)
					quotient, remainder = divmod(mm, 12)
					getyears = quotient + (1 if remainder > 0 else 0)                   
					if not getyears:
						getyears = 1
					
				#Contract valid start date & End date Calculation--END
				if ATTRIBUTE_VALUE_STR != "":
					
					TreeParam = Product.GetGlobal("TreeParam")
					TreeParentParam = Product.GetGlobal("TreeParentLevel0")  
					TreeSuperParentParam =  Product.GetGlobal("TreeParentLevel1")               
					TreeTopSuperParentParam = Product.GetGlobal("CommonTreeTopSuperParentParam")
					try:
						RecAttValue = Quote.GetGlobal("contract_quote_record_id")
					except:
						RecAttValue = ''    
					if RECORD_ID == "SYOBJR-95868":                        
						Qury_str = (
							"select top "
							+ str(PerPage)
							+ " "
							+ "SYSEFL."
							+ str(select_obj_str)
							+ ",SYSEFL.CpqTableEntryId from "
							+ str(ObjectName)
							+ " (nolock) INNER JOIN SYSECT (nolock) ON SYSEFL.SECTION_RECORD_ID = SYSECT.RECORD_ID  AND "
							+ str(Wh_API_NAME)
							+ " = '"
							+ str(RecAttValue)
							+ "' "
							+ "where SYSEFL.SECTION_NAME = '"
							+ str(TreeParentParam)
							+ "'"
						)
						QuryCount_str = (
							"select count(*) as cnt from "
							+ str(ObjectName)
							+ " (nolock) INNER JOIN SYSECT (nolock) ON SYSEFL.SECTION_RECORD_ID = SYSECT.RECORD_ID and "
							+ str(Wh_API_NAME)
							+ " = '"
							+ str(RecAttValue)
							+ "' where SYSEFL.SECTION_NAME = '"
							+ str(TreeParentParam)
							+ "'"
						)                        
					elif RECORD_ID == "SYOBJR-95843" and TreeParentParam != "" :  
						RecAttValue = Product.Attributes.GetByName("QSTN_SYSEFL_SY_03295").GetValue()
						Qury_str = (
						"select top "
						+ str(PerPage)
						+ " * "
						+ " from "
						+ str(ObjectName)
						+ " (nolock) WHERE "
						+str(ATTRIBUTE_VALUE_STR)
						+""
						+ str(Wh_API_NAME)
						+ " = '"
						+ str(RecAttValue)
						+ "' AND PAGE_NAME = '"
						+ str(TreeParentParam)
						+ "'"
						
						)
						QuryCount_str = (
							"select count(*) as cnt from "
							+ str(ObjectName)
							+ " (nolock) WHERE "
							+str(ATTRIBUTE_VALUE_STR)
							+""
							+ str(Wh_API_NAME)
							+ " = '"
							+ str(RecAttValue)
							+ "' AND PAGE_NAME = '"
							+ str(TreeParentParam)
							+ "'"
						)

					elif RECORD_ID == "SYOBJR-94489":                        
						GetappValue = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00154").GetValue()
						GetappValue = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00154").GetValue()
						Qury_str = (
							"select DISTINCT top 10 RECORD_ID,SECTION_NAME,DISPLAY_ORDER,PARENT_SECTION_RECORD_ID,OWNER_RECORD_ID,PRIMARY_OBJECT_RECORD_ID,PAGE_LABEL,PAGE_RECORD_ID,CpqTableEntryId from ( select TOP 10 ROW_NUMBER() OVER(order by DISPLAY_ORDER) AS ROW,* from SYSECT where "+str(ATTRIBUTE_VALUE_STR)+" PAGE_LABEL = '"
							+ str(TreeParentParam)
							+ "') m where m.ROW BETWEEN 1 and 10"
						)
						
						QuryCount_str = (
							"select count(*) as cnt from SYSECT (nolock) where "+str(ATTRIBUTE_VALUE_STR)+"  PAGE_LABEL = '" + str(TreeParentParam) + "'"
						)

					elif RECORD_ID == "SYOBJR-94490":
						GetappValue = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00154").GetValue()                        
						gettabres = Sql.GetFirst(
							"Select RECORD_ID from SYSECT where PAGE_NAME = '"
							+ str(TopTreeSuperParentParam)
							+ "' and SECTION_NAME = '"
							+ str(TreeParentParam)
							+ "'"
						)
						if gettabres:                            
							tabRecord = str(gettabres.RECORD_ID)

						Qustr = " where "+str(ATTRIBUTE_VALUE_STR)+" SECTION_RECORD_ID = '" + str(tabRecord) + "'"
					elif RECORD_ID == "SYOBJR-93121":
						proff_per_id = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00125").GetValue()
						Profile_ID_PERMISSION = Product.GetGlobal("Profile_ID_PERMISSION")                        
						if proff_per_id != "":
							Qury_str = (
								"select top "
								+ str(PerPage)
								+ " PROFILE_APP_RECORD_ID,APP_ID,VISIBLE,[DEFAULT],PROFILE_RECORD_ID, CpqTableEntryId from ( select ROW_NUMBER() OVER( order by APP_ID) AS ROW, PROFILE_APP_RECORD_ID,APP_ID,VISIBLE,[DEFAULT],PROFILE_RECORD_ID, CpqTableEntryId  from SYPRAP (nolock) where "+str(ATTRIBUTE_VALUE_STR)+" PROFILE_RECORD_ID = '"
								+ str(proff_per_id)
								+ "') m where m.ROW BETWEEN "
								+ str(Page_start)
								+ " and "
								+ str(Page_End)
							)
							QuryCount_str = (
								"select count(*) as cnt from "
								+ str(ObjectName)
								+ " (nolock) where  "+str(ATTRIBUTE_VALUE_STR)+" PROFILE_RECORD_ID = '"
								+ str(proff_per_id)
								+ "' "
							)
						else:
							proff_id = Product.GetGlobal("Profile_ID")
							Qury_str = (
								"select top "
								+ str(PerPage)
								+ " PROFILE_APP_RECORD_ID,APP_ID,VISIBLE,[DEFAULT],PROFILE_RECORD_ID, CpqTableEntryId from ( select ROW_NUMBER() OVER( order by APP_ID) AS ROW, PROFILE_APP_RECORD_ID,APP_ID,VISIBLE,[DEFAULT],PROFILE_RECORD_ID, CpqTableEntryId  from SYPRAP (nolock) where "+str(ATTRIBUTE_VALUE_STR)+" PROFILE_RECORD_ID = '"
								+ str(Profile_ID_PERMISSION)
								+ "') m where m.ROW BETWEEN "
								+ str(Page_start)
								+ " and "
								+ str(Page_End)
							)
							QuryCount_str = (
								"select count(*) as cnt from "
								+ str(ObjectName)
								+ " (nolock) where  "+str(ATTRIBUTE_VALUE_STR)+" PROFILE_RECORD_ID = '"
								+ str(Profile_ID_PERMISSION)
								+ "' "
							)
					elif RECORD_ID == "SYOBJR-95800":                        
						RecAttValue = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00128").GetValue()
						permiss_id = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00125").GetValue()
						
						Qury_str = (
							"select DISTINCT TOP "
							+ str(PerPage)
							+ " ID,USERNAME,NAME,ACTIVE from ( select ROW_NUMBER() OVER(order by ID) AS ROW, ID,USERNAME,NAME,ACTIVE from USERS U (nolock) inner join users_permissions up on U.id = up.user_id   where "
							+ str(ATTRIBUTE_VALUE_STR)
							+ " up.permission_id = '"
							+ str(permiss_id)
							+ "'  ) m where m.ROW BETWEEN "
							+ str(Page_start)
							+ " and "
							+ str(Page_End)
							+ ""
						)
						QuryCount_str = (
							"select count(U.ID) as cnt from USERS U (nolock)  inner join users_permissions up on U.id = up.user_id  where "
							+ str(ATTRIBUTE_VALUE_STR)
							+ " up.permission_id = '"
							+ str(permiss_id)
							+ "'  "
						)
					elif RECORD_ID == "SYOBJR-93159":
						Wh_API_NAME = "PROFILE_ID"
						RecAttValue = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00128").GetValue()
						CommonTreeSuperParentParam = Product.GetGlobal("CommonTreeSuperParentParam")
						appId = Product.GetGlobal("CommonTreeParentParam")
						if appId == "App Level Permissions":
							Qury_str = (
								"select top "
								+ str(PerPage)
								+ " *  from ( select ROW_NUMBER() OVER(order by S.DISPLAY_ORDER) AS ROW, p.PROFILE_TAB_RECORD_ID,p.TAB_ID,p.VISIBLE,p.PROFILE_RECORD_ID,p.CpqTableEntryId,S.DISPLAY_ORDER from SYPRTB p (nolock) inner join SYTABS S on S.RECORD_ID = p.TAB_RECORD_ID where "
								+ str(ATTRIBUTE_VALUE_STR)
								+ " p.PROFILE_ID = '"
								+ str(RecAttValue)
								+ "' and p.APP_ID = '"
								+ str(TreeParam)
								+ "' ) m where m.ROW BETWEEN "
								+ str(Page_start)
								+ " and "
								+ str(Page_End)
								+ " order by m.DISPLAY_ORDER"
							)                            
							QuryCount_str = (
								"select count(*) as cnt from SYPRTB (nolock)  where PROFILE_ID = '"
								+ str(RecAttValue)
								+ "' and APP_ID = '"
								+ str(TreeParam)
								+ "'"
							)
						else:
							Qury_str = (
								"select top "
								+ str(PerPage)
								+ " *  from ( select ROW_NUMBER() OVER(order by S.DISPLAY_ORDER) AS ROW, p.PROFILE_TAB_RECORD_ID,p.TAB_ID,p.VISIBLE,p.PROFILE_RECORD_ID,p.CpqTableEntryId,S.DISPLAY_ORDER from SYPRTB p (nolock) inner join SYTABS S on S.RECORD_ID = p.TAB_RECORD_ID where "
								+ str(ATTRIBUTE_VALUE_STR)
								+ " p.PROFILE_ID = '"
								+ str(RecAttValue)
								+ "' and p.APP_ID = '"
								+ str(appId)
								+ "' ) m where m.ROW BETWEEN "
								+ str(Page_start)
								+ " and "
								+ str(Page_End)
								+ " order by m.DISPLAY_ORDER"
							)
							QuryCount_str = (
								"select count(*) as cnt from SYPRTB (nolock)  where PROFILE_ID = '"
								+ str(RecAttValue)
								+ "' and APP_ID = '"
								+ str(appId)
								+ "'"
							)
					elif RECORD_ID == "SYOBJR-93160":
						RecAttValue = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00128").GetValue()
						GetAppname_query = ""
						if TreeTopSuperParentParam == "App Level Permissions":
							CommonTreeSuperParentParam = Product.GetGlobal("CommonTreeSuperParentParam")                            
							GetAppname_query = Sql.GetFirst(
								"SELECT TAB_RECORD_ID FROM SYPRTB where APP_ID = '"
								+ str(CommonTreeSuperParentParam)
								+ "' and TAB_ID = '"
								+ str(TreeParam)
								+ "'"
							)
						else:
							TreeParam = Product.GetGlobal("CommonTreeParentParam")
							GetAppname_query = Sql.GetFirst(
								"SELECT TAB_RECORD_ID FROM SYPRTB where APP_ID = '"
								+ str(TreeTopSuperParentParam)
								+ "' and TAB_ID = '"
								+ str(TreeParam)
								+ "'"
							)
						Qury_str = (
							"select top "
							+ str(PerPage)
							+ " *  from ( select ROW_NUMBER() OVER(order by P.PROFILE_RECORD_ID) AS ROW, P.PROFILE_SECTION_RECORD_ID,P.SECTION_RECORD_ID,P.SECTION_ID,P.TAB_ID,P.VISIBLE,P.PROFILE_RECORD_ID,P.CpqTableEntryId,s.DISPLAY_ORDER from SYPRSN P (nolock) inner join SYSECT s on s.RECORD_ID = P.SECTION_RECORD_ID where "
							+ str(ATTRIBUTE_VALUE_STR)
							+ " P.PROFILE_ID = '"
							+ str(RecAttValue)
							+ "' and P.TAB_ID = '"
							+ str(TreeParam)
							+ "' and P.TAB_RECORD_ID ='"
							+ str(GetAppname_query.TAB_RECORD_ID)
							+ "' ) m where m.ROW BETWEEN "
							+ str(Page_start)
							+ " and "
							+ str(Page_End)
							+ "  order by m.DISPLAY_ORDER"
						)

						QuryCount_str = (
							"select count(*) as cnt from SYPRSN (nolock)  where PROFILE_ID = '"
							+ str(RecAttValue)
							+ "' and TAB_ID = '"
							+ str(TreeParam)
							+ "' and TAB_RECORD_ID ='"
							+ str(GetAppname_query.TAB_RECORD_ID)
							+ "'"
						)
					elif RECORD_ID == "SYOBJR-93162":
						CommonTreeTopSuperParentParam = Product.GetGlobal("CommonTreeTopSuperParentParam")
						TreeFirstSuperTopParentParam = Product.GetGlobal("CommonTreeFirstSuperTopParentParam")
						CommonTreeParentParam = Product.GetGlobal("CommonTreeParentParam")
						RecAttValue = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00128").GetValue()
						getTabrec = Sql.GetFirst(
							"SELECT TAB_RECORD_ID from SYPRTB where APP_ID = '"
							+ str(TreeFirstSuperTopParentParam)
							+ "' and PROFILE_ID = '"
							+ str(RecAttValue)
							+ "' and TAB_ID = '"
							+ str(CommonTreeTopSuperParentParam)
							+ "'"
						)
						sectrecid = Tabrecordid = ""
						if getTabrec is not None:
							Tabrecordid = str(getTabrec.TAB_RECORD_ID)                            
							getsectrec = Sql.GetFirst(
								"SELECT SECTION_RECORD_ID from SYPRSN where TAB_RECORD_ID = '"
								+ str(Tabrecordid)
								+ "' and SECTION_ID ='"
								+ str(CommonTreeParentParam)
								+ "'"
							)
							if getsectrec is not None:
								sectrecid = str(getsectrec.SECTION_RECORD_ID)
						Qury_str = (
							"select top "
							+ str(PerPage)
							+ " * from ( select ROW_NUMBER() OVER(order by P.SECTION_FIELD_ID ) AS ROW,P.PROFILE_SECTIONFIELD_RECORD_ID,P.SECTIONFIELD_RECORD_ID,P.SECTION_FIELD_ID ,P.VISIBLE,P.EDITABLE,P.PROFILE_RECORD_ID,P.CpqTableEntryId,s.DISPLAY_ORDER from SYPRSF P (nolock)  inner join SYSEFL s on s.RECORD_ID = P.SECTIONFIELD_RECORD_ID where "
							+ str(ATTRIBUTE_VALUE_STR)
							+ " P.PROFILE_ID = '"
							+ str(RecAttValue)
							+ "' and P.SECTION_RECORD_ID = '"
							+ str(sectrecid)
							+ "' ) m where m.ROW BETWEEN "
							+ str(Page_start)
							+ " and "
							+ str(Page_End)
							+ "  order by m.DISPLAY_ORDER"
						)

						QuryCount_str = (
							"select count(*) as cnt from SYPRSF (nolock)  where PROFILE_ID = '"
							+ str(RecAttValue)
							+ "' and SECTION_RECORD_ID = '"
							+ str(sectrecid)
							+ "'"
						)
					elif RECORD_ID == "SYOBJR-93122":
						RecAttValue = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00128").GetValue()

						Qury_str = (
							"select  top "
							+ str(PerPage)
							+ " PROFILE_OBJECT_RECORD_ID,OBJECT_RECORD_ID, OBJECT_NAME, VISIBLE,CpqTableEntryId from ( select ROW_NUMBER() OVER( order by PROFILE_RECORD_ID) AS ROW, PROFILE_OBJECT_RECORD_ID,OBJECT_RECORD_ID, OBJECT_NAME, VISIBLE,CpqTableEntryId from SYPROH (nolock) where  "
							+ str(ATTRIBUTE_VALUE_STR)
							+ " PROFILE_ID = '"
							+ str(RecAttValue)
							+ "') m where m.ROW BETWEEN "
							+ str(Page_start)
							+ " and "
							+ str(Page_End)
							+ " order by OBJECT_NAME"
						)
						QuryCount_str = (
							"select count(*) as cnt from SYPROH (nolock) where  PROFILE_ID = '" + str(RecAttValue) + "'"
						)

					elif RECORD_ID == "SYOBJR-93130":
						CommonTreeSuperParentParam = Product.GetGlobal("CommonTreeSuperParentParam")
						CommonTreeParentParam = Product.GetGlobal("CommonTreeParentParam")
						CommonTopTreeSuperParentParam = Product.GetGlobal("CommonTopTreeSuperParentParam")
						CommonTreeTopSuperParentParam = Product.GetGlobal("CommonTreeTopSuperParentParam")
						RecAttValue = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00128").GetValue()
						if CommonTreeParentParam == "Object Level Permissions":
							Qury_str = (
								"select top "
								+ str(PerPage)
								+ " * from ( select ROW_NUMBER() OVER(order by PROFILE_RECORD_ID ASC) AS ROW,p.PROFILE_OBJECTFIELD_RECORD_ID,p.OBJECTFIELD_RECORD_ID,s.DISPLAY_ORDER,p.OBJECT_FIELD_ID,p.OBJECT_RECORD_ID,p.OBJECT_NAME,p.VISIBLE,p.EDITABLE,p.CpqTableEntryId from SYPROD p (nolock)  inner join  SYOBJD s on s.RECORD_ID = p.OBJECTFIELD_RECORD_ID where  p.PROFILE_ID = '"
								+ str(RecAttValue)
								+ "' and p.OBJECT_NAME='"
								+ str(TreeParam)
								+ "') m where m.ROW BETWEEN "
								+ str(Page_start)
								+ " and "
								+ str(Page_End)
								+ " order by m.DISPLAY_ORDER"
							)
							QuryCount_str = (
								"select count(*) as cnt from SYPROD (nolock) where PROFILE_ID = '"
								+ str(RecAttValue)
								+ "' and OBJECT_NAME='"
								+ str(TreeParam)
								+ "'"
							)
						else:
							Qury_str = (
								"select top "
								+ str(PerPage)
								+ " * from ( select ROW_NUMBER() OVER(order by PROFILE_RECORD_ID ASC) AS ROW,p.PROFILE_OBJECTFIELD_RECORD_ID,p.OBJECTFIELD_RECORD_ID,s.DISPLAY_ORDER,p.OBJECT_FIELD_ID,p.OBJECT_RECORD_ID,p.OBJECT_NAME,p.VISIBLE,p.EDITABLE,p.CpqTableEntryId from SYPROD p (nolock)  inner join  SYOBJD s on s.RECORD_ID = p.OBJECTFIELD_RECORD_ID where  p.PROFILE_ID = '"
								+ str(RecAttValue)
								+ "' and p.OBJECT_NAME='"
								+ str(CommonTreeParentParam)
								+ "') m where m.ROW BETWEEN "
								+ str(Page_start)
								+ " and "
								+ str(Page_End)
								+ " order by m.DISPLAY_ORDER"
							)
							QuryCount_str = (
								"select count(*) as cnt from SYPROD (nolock) where PROFILE_ID = '"
								+ str(RecAttValue)
								+ "' and OBJECT_NAME='"
								+ str(CommonTreeParentParam)
								+ "'"
							)
					elif RECORD_ID == "SYOBJR-93130":
						CommonTreeSuperParentParam = Product.GetGlobal("CommonTreeSuperParentParam")
						CommonTreeParentParam = Product.GetGlobal("CommonTreeParentParam")
						CommonTopTreeSuperParentParam = Product.GetGlobal("CommonTopTreeSuperParentParam")
						CommonTreeTopSuperParentParam = Product.GetGlobal("CommonTreeTopSuperParentParam")
						RecAttValue = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00128").GetValue()
						if CommonTreeParentParam == "Object Level Permissions":
							Qury_str = (
								"select top "
								+ str(PerPage)
								+ " * from ( select ROW_NUMBER() OVER(order by PROFILE_RECORD_ID ASC) AS ROW,p.PROFILE_OBJECTFIELD_RECORD_ID,p.OBJECTFIELD_RECORD_ID,s.DISPLAY_ORDER,p.OBJECT_FIELD_ID,p.OBJECT_RECORD_ID,p.OBJECT_NAME,p.VISIBLE,p.EDITABLE,p.CpqTableEntryId from SYPROD p (nolock)  inner join  SYOBJD s on s.RECORD_ID = p.OBJECTFIELD_RECORD_ID where  p.PROFILE_ID = '"
								+ str(RecAttValue)
								+ "' and p.OBJECT_NAME='"
								+ str(TreeParam)
								+ "') m where m.ROW BETWEEN "
								+ str(Page_start)
								+ " and "
								+ str(Page_End)
								+ " order by m.DISPLAY_ORDER"
							)
							QuryCount_str = (
								"select count(*) as cnt from SYPROD (nolock) where PROFILE_ID = '"
								+ str(RecAttValue)
								+ "' and OBJECT_NAME='"
								+ str(TreeParam)
								+ "'"
							)
						else:
							Qury_str = (
								"select top "
								+ str(PerPage)
								+ " * from ( select ROW_NUMBER() OVER(order by PROFILE_RECORD_ID ASC) AS ROW,p.PROFILE_OBJECTFIELD_RECORD_ID,p.OBJECTFIELD_RECORD_ID,s.DISPLAY_ORDER,p.OBJECT_FIELD_ID,p.OBJECT_RECORD_ID,p.OBJECT_NAME,p.VISIBLE,p.EDITABLE,p.CpqTableEntryId from SYPROD p (nolock)  inner join  SYOBJD s on s.RECORD_ID = p.OBJECTFIELD_RECORD_ID where  p.PROFILE_ID = '"
								+ str(RecAttValue)
								+ "' and p.OBJECT_NAME='"
								+ str(CommonTreeParentParam)
								+ "') m where m.ROW BETWEEN "
								+ str(Page_start)
								+ " and "
								+ str(Page_End)
								+ " order by m.DISPLAY_ORDER"
							)
							QuryCount_str = (
								"select count(*) as cnt from SYPROD (nolock) where PROFILE_ID = '"
								+ str(RecAttValue)
								+ "' and OBJECT_NAME='"
								+ str(CommonTreeParentParam)
								+ "'"
							)
					elif str(RECORD_ID) == "SYOBJR-94454" or str(RECORD_ID) == "SYOBJR-94455":
						Qury_str = (
							"select DISTINCT top "
							+ str(PerPage)
							+ " "
							+ str(select_obj_str)
							+ " from ( select ROW_NUMBER() OVER(order by "
							+ str(Wh_API_NAMEs)
							+ ") AS ROW, * from "
							+ str(ObjectName)
							+ " (nolock)  where  "
							+ str(ATTRIBUTE_VALUE_STR)
							+ " "
							+ str(Wh_API_NAME)
							+ " = '"
							+ str(RecAttValue)
							+ "' ) m where m.ROW BETWEEN "
							+ str(Page_start)
							+ " and "
							+ str(Page_End)
							+ ""
						)
						QuryCount_str = (
							"select count(*) as cnt from "
							+ str(ObjectName)
							+ " (nolock) where  "
							+ str(ATTRIBUTE_VALUE_STR)
							+ " "
							+ str(Wh_API_NAME)
							+ " = '"
							+ str(RecAttValue)
							+ "' "
						) 
					elif str(RECORD_ID) == "SYOBJR-91822":
						contractrecid = Product.GetGlobal("contract_record_id")
						
						if Product.GetGlobal("TreeParentLevel1") == "Cart Items": 
												
							imgstr = '<img title="Acquired" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Green_Tick.svg>'
							acquiring_img_str = '<img title="Acquiring" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Cloud_Icon.svg>'
							TreeParentParam = Product.GetGlobal("TreeParentLevel0")
							ServiceId = TreeParentParam.split("-")[1].strip()                           
							Qury_str = (
									"SELECT DISTINCT TOP "
									+ str(PerPage)
									+ " CASE WHEN DISCOUNT = 'ACQUIRED' THEN '"+ imgstr +"' ELSE '"+ imgstr +"' END AS EQUIPMENT_STATUS, CONTRACT_ITEM_COVERED_OBJECT_RECORD_ID,EQUIPMENT_LINE_ID,SERVICE_ID,EQUIPMENT_ID,SERIAL_NO,GREENBOOK,TOTAL_COST,LINE_ITEM_ID,DISCOUNT,TAX,NET_VALUE,EQUIPMENT_RECORD_ID,SERVICE_RECORD_ID,FABLOCATION_RECORD_ID,EQUIPMENTCATEGORY_RECORD_ID,CONTRACT_RECORD_ID,MNT_PLANT_RECORD_ID,SALESORG_RECORD_ID,GREENBOOK_RECORD_ID,CpqTableEntryId from ( select ROW_NUMBER() OVER(order by "+ str(Wh_API_NAMEs) +") AS ROW, * from CTCICO (nolock)  where "+ str(ATTRIBUTE_VALUE_STR)+" CONTRACT_RECORD_ID ='"+str(RecAttValue)
									+"' and GREENBOOK = '"+str(TreeParam)+"' and SERVICE_ID = '"+str(ServiceId)+"') m where m.ROW BETWEEN "
									+ str(Page_start)
									+ " AND "
									+ str(Page_End)
								)

							QuryCount_str = (
								"SELECT COUNT(CpqTableEntryId) AS cnt FROM CTCICO (nolock) WHERE "+ str(ATTRIBUTE_VALUE_STR)+" CONTRACT_RECORD_ID = '"
									+ str(RecAttValue)
									+ "'and GREENBOOK = '"+str(TreeParam)+"'and SERVICE_ID = '"+str(ServiceId)+"'"
							)                                
						else:
							
							imgstr = '<img title="Acquired" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Green_Tick.svg>'
							acquiring_img_str = '<img title="Acquiring" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Cloud_Icon.svg>'
							qt_rec_id = SqlHelper.GetFirst("SELECT CONTRACT_ID FROM CTCTSV WHERE CONTRACT_RECORD_ID='" + str(
							contractrecid) + "'")
							LineAndEquipIDList = TreeParam.split(' - ')
							if TreeParentParam == "Cart Items":
								Qury_str = (
									"select top "
										+ str(PerPage)
										+ " CASE WHEN DISCOUNT = 'ACQUIRED' THEN '"+ imgstr +"' ELSE '"+ imgstr +"' END AS EQUIPMENT_STATUS, CONTRACT_ITEM_COVERED_OBJECT_RECORD_ID,EQUIPMENT_LINE_ID,SERVICE_ID,EQUIPMENT_ID,SERIAL_NO,GREENBOOK,TOTAL_COST,LINE_ITEM_ID,DISCOUNT,TAX,EXTENDED_PRICE,EQUIPMENT_RECORD_ID,SERVICE_RECORD_ID,FABLOCATION_RECORD_ID,EQUIPMENTCATEGORY_RECORD_ID,CONTRACT_RECORD_ID,MNT_PLANT_RECORD_ID,SALESORG_RECORD_ID,GREENBOOK_RECORD_ID,CpqTableEntryId from ( select  ROW_NUMBER() OVER( ORDER BY EQUIPMENT_LINE_ID) AS ROW, * from CTCICO (NOLOCK) where "+ str(ATTRIBUTE_VALUE_STR)+" CONTRACT_ID = '"
										+ str(qt_rec_id.CONTRACT_ID)
										+ "' AND SERVICE_ID = '"
										+ str(LineAndEquipIDList[1])
										+ "') m where m.ROW BETWEEN "
										+ str(Page_start)
										+ " and "
										+ str(Page_End)
								)
								QuryCount_str = (
										"select count(*) as cnt FROM CTCICO where "+ str(ATTRIBUTE_VALUE_STR)+" SERVICE_ID = '{}' and CONTRACT_ID = '{}'".format(
											LineAndEquipIDList[1], str(qt_rec_id.CONTRACT_ID))
								)
							else:
							
								Qury_str = (
									"select top "
										+ str(PerPage)
										+ " * from ( select  ROW_NUMBER() OVER( ORDER BY EQUIPMENT_LINE_ID) AS ROW, * from CTCICO (NOLOCK) where "+ str(ATTRIBUTE_VALUE_STR)+" CONTRACT_ID = '"
										+ str(qt_rec_id.CONTRACT_ID)
										+ "' AND SERVICE_ID = '"
										+ str(LineAndEquipIDList[1])
										+ "') m where m.ROW BETWEEN "
										+ str(Page_start)
										+ " and "
										+ str(Page_End)
								)
								QuryCount_str = (
										"select count(*) as cnt FROM CTCICO where "+ str(ATTRIBUTE_VALUE_STR)+" SERVICE_ID = '{}' and CONTRACT_ID = '{}'".format(
											LineAndEquipIDList[1], str(qt_rec_id.CONTRACT_ID))
								)                              
					elif str(RECORD_ID) == "SYOBJR-98795":                        
						TreeParam = Product.GetGlobal("TreeParam")
						TreeParentParam = Product.GetGlobal("TreeParentLevel0")
						contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
						qt_rec_id = Sql.GetFirst("SELECT QUOTE_ID FROM SAQTSV WHERE QUOTE_RECORD_ID ='" + str(
							contract_quote_record_id) + "' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' ")						
						LineAndEquipIDList = TreeParam.split(' - ')                        
						if getyears == 1:
							col_year =  'YEAR_1'
						elif getyears == 2:
							col_year =  'YEAR_1,YEAR_2'
						elif getyears == 3:
							col_year =  'YEAR_1,YEAR_2,YEAR_3'
						elif getyears == 4:
							col_year =  'YEAR_1,YEAR_2,YEAR_3,YEAR_4'
						else:
							col_year = 'YEAR_1,YEAR_2,YEAR_3,YEAR_4,YEAR_5'
						if TreeParam == "Quote Preview":                            
							Qury_str = (
							"select top "
								+ str(PerPage)
								+ " QUOTE_ITEM_COVERED_OBJECT_RECORD_ID, EQUIPMENT_LINE_ID, EQUIPMENT_ID,SERVICE_ID,BD_DISCOUNT,BD_PRICE_MARGIN,DISCOUNT,YEAR_OVER_YEAR,"+col_year+",SERIAL_NO, GREENBOOK,FABLOCATION_ID, TARGET_PRICE_MARGIN, SALES_DISCOUNT_PRICE, SALDIS_PERCENT,LINE,NET_VALUE,PRICE_BENCHMARK_TYPE,TOOL_CONFIGURATION,ANNUAL_BENCHMARK_BOOKING_PRICE,CONTRACT_ID,CONVERT(VARCHAR(10),CONTRACT_VALID_FROM,101) AS [CONTRACT_VALID_FROM],CONVERT(VARCHAR(10),CONTRACT_VALID_TO,101) AS [CONTRACT_VALID_TO],BENCHMARKING_THRESHOLD,CpqTableEntryId from ( select  ROW_NUMBER() OVER( ORDER BY EQUIPMENT_LINE_ID) AS ROW, * from SAQICO (NOLOCK) where QUOTE_ID = '"
								+ str(qt_rec_id.QUOTE_ID)
								+ "' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"') m where m.ROW BETWEEN "
								+ str(Page_start)
								+ " and "
								+ str(Page_End)
							)
							QuryCount_str = (
									"select count(*) as cnt FROM SAQICO where " + str(ATTRIBUTE_VALUE_STR) +" QUOTE_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(
										str(qt_rec_id.QUOTE_ID),quote_revision_record_id)
							)
					elif str(RECORD_ID) == "SYOBJR-00009":
						# if Quote.GetCustomField('PRICING_PICKLIST').Content == '':
						# 	Quote.GetCustomField('PRICING_PICKLIST').Content = 'Document Currency'
						if Product.GetGlobal("TreeParentLevel2") == "Quote Items":  
							imgstr = '<img title="Acquired" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Green_Tick.svg>'
							acquiring_img_str = '<img title="Acquiring" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Cloud_Icon.svg>'
							exclamation = '<img title="Approval Required" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/clock_exe.svg>'
							error = '<img title="Error" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/exclamation_icon.svg>'
							partially_priced = '<img title="Partially Priced" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Red1_Circle.svg>'
							assembly_missing = '<img title="Assembly Missing" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Orange1_Circle.svg>'
							if getyears == 1:
								col_year =  'YEAR_1'
							elif getyears == 2:
								col_year =  'YEAR_1,YEAR_2'
							elif getyears == 3:
								col_year =  'YEAR_1,YEAR_2,YEAR_3'
							elif getyears == 4:
								col_year =  'YEAR_1,YEAR_2,YEAR_3,YEAR_4'
							else:
								col_year = 'YEAR_1,YEAR_2,YEAR_3,YEAR_4,YEAR_5' 
							TreeParentParam = Product.GetGlobal("TreeParentLevel1")
							
							try:
								if str(TreeParentParam.split("-")[4]):
									ServiceId = TreeParentParam.split("-")[-3].strip()
								else:
									ServiceId = TreeParentParam.split("-")[1].strip() 
							except:
								ServiceId = TreeParentParam.split("-")[1].strip()
							fab_location_id = Product.GetGlobal("TreeParentLevel0")
							Qury_str = (
									"SELECT DISTINCT TOP "
									+ str(PerPage)
									+ " CASE WHEN STATUS = 'ACQUIRED' THEN '"+ imgstr +"' WHEN STATUS = 'APPROVAL REQUIRED' THEN '"+ exclamation +"' WHEN STATUS = 'ON HOLD - COSTING' THEN '"+ error +"' WHEN STATUS = 'ERROR' THEN '"+ error +"' WHEN STATUS = 'PARTIALLY PRICED' THEN '"+ partially_priced +"' WHEN STATUS = 'ASSEMBLY IS MISSING' THEN '"+ assembly_missing +"' ELSE '"+ acquiring_img_str +"' END AS STATUS, QUOTE_ITEM_COVERED_OBJECT_RECORD_ID,TARGET_PRICE_MARGIN,SERVICE_ID,EQUIPMENT_ID,SERIAL_NO,GREENBOOK,FABLOCATION_ID,TARGET_PRICE,SALDIS_PERCENT,NET_VALUE,EQUIPMENT_RECORD_ID,BD_DISCOUNT,BD_PRICE_MARGIN,DISCOUNT,YEAR_OVER_YEAR,"+col_year+",SERVICE_RECORD_ID,FABLOCATION_RECORD_ID,TECHNOLOGY,KPU,BD_DISCOUNT_RECORD_ID,EQUIPMENTCATEGORY_RECORD_ID,QUOTE_RECORD_ID,QTEREV_RECORD_ID,MNT_PLANT_RECORD_ID,SALES_DISCOUNT_PRICE,SALESORG_RECORD_ID,GREENBOOK_RECORD_ID,PRICE_BENCHMARK_TYPE,TOOL_CONFIGURATION,ANNUAL_BENCHMARK_BOOKING_PRICE,CONTRACT_ID,CONVERT(VARCHAR(10),CONTRACT_VALID_FROM,101) AS [CONTRACT_VALID_FROM],CONVERT(VARCHAR(10),CONTRACT_VALID_TO,101) AS [CONTRACT_VALID_TO],BENCHMARKING_THRESHOLD,CpqTableEntryId,ASSEMBLY_ID,TOTAL_COST_WOSEEDSTOCK,TOTAL_COST_WSEEDSTOCK from ( select ROW_NUMBER() OVER(order by "+ str(Wh_API_NAMEs) +") AS ROW, * from SAQICO (nolock)  where "+ str(ATTRIBUTE_VALUE_STR)+" QUOTE_RECORD_ID ='"+str(RecAttValue)
									+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"'  and GREENBOOK = '"+str(TreeParam)+"' and FABLOCATION_ID = '"+str(fab_location_id)+"' and SERVICE_ID = '"+str(ServiceId)+"') m where m.ROW BETWEEN "
									+ str(Page_start)
									+ " AND "
									+ str(Page_End)
								)
							
							QuryCount_str = (
								"SELECT COUNT(CpqTableEntryId) AS cnt FROM SAQICO (nolock) WHERE " + str(ATTRIBUTE_VALUE_STR) +" QUOTE_RECORD_ID = '"
									+ str(RecAttValue)
									+ "' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' and GREENBOOK = '"+str(TreeParam)+"' and FABLOCATION_ID = '"+str(fab_location_id)+"' and SERVICE_ID = '"+str(ServiceId)+"'"
							)    
						else:
							if getyears == 1:
								col_year =  'YEAR_1'
							elif getyears == 2:
								col_year =  'YEAR_1,YEAR_2'
							elif getyears == 3:
								col_year =  'YEAR_1,YEAR_2,YEAR_3'
							elif getyears == 4:
								col_year =  'YEAR_1,YEAR_2,YEAR_3,YEAR_4'
							else:
								col_year = 'YEAR_1,YEAR_2,YEAR_3,YEAR_4,YEAR_5'   
							imgstr = '<img title="Acquired" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Green_Tick.svg>'
							acquiring_img_str = '<img title="Acquiring" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Cloud_Icon.svg>'
							exclamation = '<img title="Approval Required" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/clock_exe.svg>'
							error = '<img title="Error" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/exclamation_icon.svg>'
							partially_priced = '<img title="Partially Priced" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Red1_Circle.svg>'
							assembly_missing = '<img title="Assembly Missing" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Orange1_Circle.svg>'
							qt_rec_id = SqlHelper.GetFirst("SELECT QUOTE_ID FROM SAQTSV WHERE QUOTE_RECORD_ID ='" + str(
							contract_quote_record_id) + "' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' ")                            
							

							if TreeParam == "Quote Items":
								Trace.Write("a1")
								# Qury_str = (
								# 	"select top "
								# 		+ str(PerPage)
								# 		+ " CASE WHEN STATUS = 'ACQUIRED' THEN '"+ imgstr +"' WHEN STATUS = 'APPROVAL REQUIRED' THEN '" +exclamation+ "' WHEN STATUS = 'ON HOLD - COSTING' THEN '"+ error +"' WHEN STATUS = 'ERROR' THEN '"+ error +"' WHEN STATUS = 'PARTIALLY PRICED' THEN '"+ partially_priced +"' WHEN STATUS = 'ASSEMBLY MISSING' THEN '"+ assembly_missing +"'  ELSE '"+ acquiring_img_str +"' END AS STATUS, QUOTE_ITEM_COVERED_OBJECT_RECORD_ID, EQUIPMENT_LINE_ID, EQUIPMENT_ID,SERVICE_ID,LINE_ITEM_ID,BD_DISCOUNT,BD_PRICE_MARGIN,DISCOUNT,NET_PRICE,YEAR_OVER_YEAR,"+col_year+",SERIAL_NO, GREENBOOK,FABLOCATION_ID,TECHNOLOGY,KPU,MODEL_PRICE, TARGET_PRICE_MARGIN, TARGET_PRICE, SALES_DISCOUNT_PRICE, CEILING_PRICE, SALDIS_PERCENT,SRVTAXCLA_DESCRIPTION,TAX_PERCENTAGE, NET_VALUE,PRICE_BENCHMARK_TYPE,TOOL_CONFIGURATION,ANNUAL_BENCHMARK_BOOKING_PRICE,CONTRACT_ID,CONVERT(VARCHAR(10),CONTRACT_VALID_FROM,101) AS [CONTRACT_VALID_FROM],CONVERT(VARCHAR(10),CONTRACT_VALID_TO,101) AS [CONTRACT_VALID_TO],BENCHMARKING_THRESHOLD,CpqTableEntryId,ASSEMBLY_ID,TOTAL_COST_WOSEEDSTOCK,TOTAL_COST_WSEEDSTOCK from ( select  ROW_NUMBER() OVER( ORDER BY "+ str(Wh_API_NAMEs)
								# 		+") AS ROW, * from SAQICO (NOLOCK) where "+ str(ATTRIBUTE_VALUE_STR)+" QUOTE_ID = '"
								# 		+ str(qt_rec_id.QUOTE_ID)
								# 		+ "') m where m.ROW BETWEEN "
								# 		+ str(Page_start)
								# 		+ " and "
								# 		+ str(Page_End)+" ORDER BY "+ str(Wh_API_NAMEs)
								# )

								Qury_str = (
									
									"select top "
										+ str(PerPage)
										+ " CASE WHEN STATUS = 'ACQUIRED' THEN '"+ imgstr +"' WHEN STATUS = 'APPROVAL REQUIRED' THEN '" +exclamation+ "' WHEN STATUS = 'ON HOLD - COSTING' THEN '"+ error +"' WHEN STATUS = 'ERROR' THEN '"+ error +"' WHEN STATUS = 'PARTIALLY PRICED' THEN '"+ partially_priced +"' WHEN STATUS = 'ASSEMBLY IS MISSING' THEN '"+ assembly_missing +"'  ELSE '"+ acquiring_img_str +"' END AS STATUS, QUOTE_ITEM_COVERED_OBJECT_RECORD_ID,SERVICE_ID,FABLOCATION_ID,GREENBOOK,OBJECT_ID,OBJECT_TYPE,QUANTITY,EQUIPMENT_ID,GOT_CODE,ASSEMBLY_ID,PM_ID,PM_LABOR_LEVEL,KIT_NAME,KIT_NUMBER,KPU,TOOL_CONFIGURATION,SSCM_PM_FREQUENCY,ADJ_PM_FREQUENCY,CEILING_PRICE_INGL_CURR,TARGET_PRICE_INGL_CURR,SLSDIS_PRICE_INGL_CURR,BD_PRICE_INGL_CURR,DISCOUNT,SALES_PRICE_INGL_CURR,YEAR_OVER_YEAR,YEAR,CONVERT(VARCHAR(10),CONTRACT_VALID_FROM,101) AS [CONTRACT_VALID_FROM],CONVERT(VARCHAR(10),CONTRACT_VALID_TO,101) AS [CONTRACT_VALID_TO],CONVERT(VARCHAR(10),WARRANTY_START_DATE,101) AS [WARRANTY_START_DATE],CONVERT(VARCHAR(10),WARRANTY_END_DATE,101) AS [WARRANTY_END_DATE],CNTCST_INGL_CURR,CNTPRI_INGL_CURR,CpqTableEntryId from ( select  ROW_NUMBER() OVER( ORDER BY LINE,"+ str(Wh_API_NAMEs)
										+") AS ROW, * from SAQICO (NOLOCK) where "+ str(ATTRIBUTE_VALUE_STR)+" QUOTE_ID = '"
										+ str(qt_rec_id.QUOTE_ID)
										+ "') m where m.ROW BETWEEN "
										+ str(Page_start)
										+ " and "
										+ str(Page_End)+" ORDER BY "+ str(Wh_API_NAMEs)
								)
								QuryCount_str = (
										"select count(*) as cnt FROM SAQICO where "+ str(ATTRIBUTE_VALUE_STR)+"  QUOTE_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(
											str(qt_rec_id.QUOTE_ID),quote_revision_record_id)
								)


							elif TreeParentParam == "Quote Items": 
								try:
									if str(TreeParam.split("-")[3]):
										LineAndEquipIDList = TreeParam.split(' - ')[-2].strip()
									else:
										LineAndEquipIDList = TreeParam.split(' - ')[1].strip() 
								except:
									LineAndEquipIDList = TreeParam.split('-')[1].strip()
								Qury_str = (
									"select top "
										+ str(PerPage)
										+ " CASE  WHEN STATUS = 'ACQUIRED' THEN '"+ imgstr +"' WHEN STATUS = 'APPROVAL REQUIRED' THEN '" +exclamation+ "' WHEN STATUS = 'ON HOLD - COSTING' THEN '"+ error +"'  WHEN STATUS = 'ERROR' THEN '"+ error +"' WHEN STATUS = 'PARTIALLY PRICED' THEN '"+ partially_priced +"' WHEN STATUS = 'ASSEMBLY IS MISSING' THEN '"+ assembly_missing +"' ELSE '"+ acquiring_img_str +"' END AS STATUS, QUOTE_ITEM_COVERED_OBJECT_RECORD_ID, SERVICE_ID, EQUIPMENT_ID,LINE_ITEM_ID,BD_DISCOUNT,BD_PRICE_MARGIN,DISCOUNT,YEAR_OVER_YEAR,YEAR_1, SERIAL_NO,GREENBOOK,FABLOCATION_ID,TECHNOLOGY,KPU,SALES_DISCOUNT_PRICE, TARGET_PRICE_MARGIN,  SALDIS_PERCENT,NET_VALUE,PRICE_BENCHMARK_TYPE,TOOL_CONFIGURATION,ANNUAL_BENCHMARK_BOOKING_PRICE,CONTRACT_ID,CONVERT(VARCHAR(10),CONTRACT_VALID_FROM,101) AS [CONTRACT_VALID_FROM],CONVERT(VARCHAR(10),CONTRACT_VALID_TO,101) AS [CONTRACT_VALID_TO],BENCHMARKING_THRESHOLD,CpqTableEntryId,ASSEMBLY_ID,TOTAL_COST_WOSEEDSTOCK,TOTAL_COST_WSEEDSTOCK from ( select  ROW_NUMBER() OVER( ORDER BY "+ str(Wh_API_NAMEs)
										+") AS ROW, * from SAQICO (NOLOCK) where "+ str(ATTRIBUTE_VALUE_STR)+" QUOTE_ID = '"
										+ str(qt_rec_id.QUOTE_ID)
										+ "' AND SERVICE_ID = '"
										+ str(LineAndEquipIDList)
										+ "' and LINE_ITEM_ID = '"+str(TreeParam.split(' -')[0])+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"') m where m.ROW BETWEEN "
										+ str(Page_start)
										+ " and "
										+ str(Page_End)
								)
								QuryCount_str = (
										"select count(*) as cnt FROM SAQICO where "+ str(ATTRIBUTE_VALUE_STR)+" SERVICE_ID = '"+ str(LineAndEquipIDList) + "' and QUOTE_ID = '"+str(qt_rec_id.QUOTE_ID)+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' and LINE_ITEM_ID = '"+str(TreeParam.split(' -')[0])+"'"
								)
							
								
							## code is not using anywhere    TreeSuperParentParam
							elif TreeSuperParentParam == "Quote Items":
								
								LineAndEquipIDList = TreeParentParam.split('-')[1].strip()
								Qury_str = (
									"select top "
										+ str(PerPage)
										+ " CASE  WHEN STATUS = 'ACQUIRED' THEN '"+ imgstr +"' WHEN STATUS = 'APPROVAL REQUIRED' THEN '" +exclamation+ "' WHEN STATUS = 'ON HOLD - COSTING' THEN '"+ error +"' WHEN STATUS = 'ERROR' THEN '"+ error +"' WHEN STATUS = 'PARTIALLY PRICED' THEN '"+ partially_priced +"' WHEN STATUS = 'ASSEMBLY IS MISSING' THEN '"+ assembly_missing +"' ELSE '"+ acquiring_img_str +"' END AS STATUS, QUOTE_ITEM_COVERED_OBJECT_RECORD_ID, SERVICE_ID, EQUIPMENT_ID,LINE_ITEM_ID,BD_DISCOUNT,BD_PRICE_MARGIN,DISCOUNT,YEAR_OVER_YEAR,YEAR_1, SERIAL_NO,GREENBOOK,FABLOCATION_ID,TECHNOLOGY,KPU,TARGET_PRICE, SALES_DISCOUNT_PRICE, TARGET_PRICE_MARGIN, SALDIS_PERCENT,NET_VALUE,PRICE_BENCHMARK_TYPE,TOOL_CONFIGURATION,ANNUAL_BENCHMARK_BOOKING_PRICE,CONTRACT_ID,CONVERT(VARCHAR(10),CONTRACT_VALID_FROM,101) AS [CONTRACT_VALID_FROM],CONVERT(VARCHAR(10),CONTRACT_VALID_TO,101) AS [CONTRACT_VALID_TO],BENCHMARKING_THRESHOLD,CpqTableEntryId,ASSEMBLY_ID,TOTAL_COST_WOSEEDSTOCK,TOTAL_COST_WSEEDSTOCK from ( select  ROW_NUMBER() OVER( ORDER BY "+ str(Wh_API_NAMEs)
										+") AS ROW, * from SAQICO (NOLOCK) where "+ str(ATTRIBUTE_VALUE_STR)+" QUOTE_ID = '"
										+ str(qt_rec_id.QUOTE_ID)
										+ "' AND SERVICE_ID = '"
										+ str(LineAndEquipIDList)
										+ "' AND FABLOCATION_ID = '"+str(TreeParam)+"' and LINE_ITEM_ID = '"+str(TreeParentParam.split(' -')[0])+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"') m where m.ROW BETWEEN "
										+ str(Page_start)
										+ " and "
										+ str(Page_End)
								)
								QuryCount_str = (
										"select count(*) as cnt FROM SAQICO where "+ str(ATTRIBUTE_VALUE_STR)+" SERVICE_ID = '"+ str(LineAndEquipIDList)+"' and FABLOCATION_ID = '"+str(TreeParam)+"'  and QUOTE_ID = '"+str(qt_rec_id.QUOTE_ID)+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' and LINE_ITEM_ID = '"+str(TreeParentParam.split(' -')[0])+"'"
								)
							

					elif str(RECORD_ID) == 'SYOBJR-98799':     
						contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")                
						qt_rec_id = Sql.GetFirst("SELECT QUOTE_ID FROM SAQTSV WHERE QUOTE_RECORD_ID ='" + str(
						contract_quote_record_id) + "' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' ")
						try:
							quote_id = qt_rec_id.QUOTE_ID
						except:
							quote_id = ""
						imgstr = '<img title="Acquired" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Green_Tick.svg>'
						acquiring_img_str = '<img title="Acquiring" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Cloud_Icon.svg>'
						Qury_str = (
									"select top "
										+ str(PerPage)
										+ " CASE WHEN STATUS = 'ACQUIRED' THEN '"+ imgstr +"' ELSE '"+ acquiring_img_str +"' END AS STATUS, QUOTE_DOCUMENT_RECORD_ID, DOCUMENT_ID,DOCUMENT_NAME,LANGUAGE_ID,LANGUAGE_NAME,CPQTABLEENTRYDATEADDED,QUOTE_RECORD_ID,QTEREV_RECORD_ID,CpqTableEntryId from ( select  ROW_NUMBER() OVER( ORDER BY STATUS) AS ROW, * from SAQDOC (NOLOCK) where " + str(ATTRIBUTE_VALUE_STR)+" QUOTE_ID = '"
										+ str(qt_rec_id.QUOTE_ID)
										+ "' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' ) m where m.ROW BETWEEN "
										+ str(Page_start)
										+ " and "
										+ str(Page_End)
								)
						QuryCount_str = (
								"select count(*) as cnt FROM SAQDOC where " + str(ATTRIBUTE_VALUE_STR)+" QUOTE_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(
									str(qt_rec_id.QUOTE_ID),quote_revision_record_id)
						)
					elif str(RECORD_ID) == "SYOBJR-00007": # Billing Matrix - Pivot - Start                        
						pivot_columns = ",".join(['[{}]'.format(billing_date) for billing_date in billing_date_column])
						Qustr = " where " + str(ATTRIBUTE_VALUE_STR)+" "+ str(Wh_API_NAME) + " = '" + str(RecAttValue) + "'"
						if Qustr:
							if str(TreeParentParam)== "Billing":
								Qustr += " AND SERVICE_ID = '{}' AND BILLING_DATE BETWEEN '{}' AND '{}'".format(TreeParam,billing_date_column[0], billing_date_column[-1])
							else:
								Qustr += " AND BILLING_DATE BETWEEN '{}' AND '{}'".format(billing_date_column[0], billing_date_column[-1])
						pivot_query_str = """
									SELECT ROW_NUMBER() OVER(ORDER BY EQUIPMENT_ID)
									AS ROW, *
										FROM (
											SELECT 
												{Columns}                                           
											FROM {ObjectName}
											{WhereString}
										) AS IQ
										PIVOT
										(
											SUM(BILLING_VALUE)
											FOR BILLING_DATE IN ({PivotColumns})
										)AS PVT
									""".format(OrderByColumn=Wh_API_NAMEs, Columns=column_before_pivot_change, ObjectName=ObjectName,
												WhereString=Qustr, PivotColumns=pivot_columns)
						Qury_str = """
									SELECT DISTINCT TOP {PerPage} * FROM ( SELECT * FROM ({InnerQuery}) OQ WHERE ROW BETWEEN {Start} AND {End} ) AS FQ ORDER BY EQUIPMENT_ID
									""".format(PerPage=PerPage, OrderByColumn=Wh_API_NAMEs, InnerQuery=pivot_query_str, Start=Page_start, End=Page_End)
						QuryCount_str = "SELECT COUNT(*) AS cnt FROM ({InnerQuery}) OQ".format(InnerQuery=pivot_query_str)
						# Billing Matrix - Pivot - End
					elif str(RECORD_ID) == "SYOBJR-00015" and str(TreeParentParam) == "Approval Chain Steps":
						Qury_str = (
							" SELECT TOP "
							+ str(PerPage)
							+ " * FROM (SELECT ROW_NUMBER() OVER(ORDER BY APPROVAL_TRACKED_FIELD_RECORD_ID) AS ROW,APPROVAL_TRACKED_FIELD_RECORD_ID,TRKOBJ_TRACKEDFIELD_LABEL,TRKOBJ_NAME,TRACKING_TYPE,ACAPTF.CpqTableEntryId FROM ACAPTF (NOLOCK) INNER JOIN ACACST (NOLOCK) ON ACAPTF.APRCHNSTP_RECORD_ID = ACACST.APPROVAL_CHAIN_STEP_RECORD_ID WHERE "
							+ str(ATTRIBUTE_VALUE_STR)
							+ " ACACST.APRCHNSTP_NAME = '"
							+ str(TreeParam).split(': ')[1]
							+ "' AND ACACST.APRCHN_RECORD_ID = '"
							+ str(RecAttValue)
							+ "')m where m.ROW BETWEEN "
							+ str(Page_start)
							+ " and "
							+ str(Page_End)
							+ " "
						)

						QuryCount_str = (
							"SELECT COUNT(APPROVAL_TRACKED_FIELD_RECORD_ID) AS cnt FROM ACAPTF (NOLOCK) INNER JOIN ACACST (NOLOCK) ON ACAPTF.APRCHNSTP_RECORD_ID = ACACST.APPROVAL_CHAIN_STEP_RECORD_ID WHERE "
							+ str(ATTRIBUTE_VALUE_STR)
							+ " ACACST.APRCHNSTP_NAME = '"
							+ str(TreeParam).split(': ')[1]
							+ "' AND ACACST.APRCHN_RECORD_ID = '"
							+ str(RecAttValue)
							+ "' "
						)
					elif str(RECORD_ID) == "SYOBJR-00014":
						step_name = TreeParam.split(':')[1].strip()
						
						Qury_str = (
							"select top "
							+ str(PerPage)
							+ " * from ( select ROW_NUMBER() OVER( order by APPROVAL_CHAIN_STEP_APPROVER_RECORD_ID) AS ROW,ACACSA.APPROVAL_CHAIN_STEP_APPROVER_RECORD_ID,ACACSA.APRCHN_ID,ACACSA.APRCHNSTP_APPROVER_ID,ACACSA.APPROVER_SELECTION_METHOD,ACACSA.USERNAME,ACACSA.PROFILE_ID,ACACSA.ROLE_ID,ACACSA.NOTIFICATION_ONLY,ACACSA.CpqTableEntryId from ACACSA (nolock) INNER JOIN ACACST (NOLOCK) ON ACACST.APPROVAL_CHAIN_STEP_RECORD_ID = ACACSA.APRCHNSTP_RECORD_ID WHERE  "
							+ str(ATTRIBUTE_VALUE_STR)
							+ " ACACSA."
							+ str(Wh_API_NAME)
							+ " = '"
							+ str(RecAttValue)
							+ "' AND ACACST.APRCHNSTP_NAME = '"
							+ str(step_name)
							+ "') m where m.ROW BETWEEN "
							+ str(Page_start)
							+ " AND "
							+ str(Page_End)
							+ ""
						)
						QuryCount_str = (
							"select count(ACACSA.CpqTableEntryId) as cnt from ACACSA (nolock) INNER JOIN ACACST (NOLOCK) ON ACACST.APPROVAL_CHAIN_STEP_RECORD_ID = ACACSA.APRCHNSTP_RECORD_ID WHERE ACACSA."
							+ str(ATTRIBUTE_VALUE_STR)
							+ " ACACSA."
							+ str(Wh_API_NAME)
							+ " = '"
							+ str(RecAttValue)
							+ "' AND ACACST.APRCHNSTP_NAME = '"
							+ str(step_name)
							+ "'"
						)  
					elif str(RECORD_ID) == "SYOBJR-98822":     
						if Product.GetGlobal("TreeParentLevel1") == "Cart Items":                            
							imgstr = '<img title="Acquired" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Green_Tick.svg>'
							acquiring_img_str = '<img title="Acquiring" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Cloud_Icon.svg>'
							
							Qury_str = (
									"SELECT DISTINCT TOP "
									+ str(PerPage)
									+ " CASE WHEN DISCOUNT = 'ACQUIRED' THEN '"+ imgstr +"' ELSE '"+ imgstr +"' END AS EQUIPMENT_STATUS, CONTRACT_ITEM_COVERED_OBJECT_RECORD_ID,EQUIPMENT_LINE_ID,SERVICE_ID,EQUIPMENT_ID,SERIAL_NO,GREENBOOK,TOTAL_COST,LINE_ITEM_ID,DISCOUNT,TAX,EXTENDED_PRICE,EQUIPMENT_RECORD_ID,SERVICE_RECORD_ID,FABLOCATION_RECORD_ID,EQUIPMENTCATEGORY_RECORD_ID,CONTRACT_RECORD_ID,MNT_PLANT_RECORD_ID,SALESORG_RECORD_ID,GREENBOOK_RECORD_ID,CONTRACT_CURRENCY,CONTRACT_CURRENCY_RECORD_ID,CpqTableEntryId from ( select ROW_NUMBER() OVER(order by "+ str(Wh_API_NAMEs) +") AS ROW, * from CTCICO (nolock)  where CONTRACT_RECORD_ID ='"+str(RecAttValue)
									+"' and GREENBOOK = '"+str(TreeParam)+"') m where m.ROW BETWEEN "
									+ str(Page_start)
									+ " AND "
									+ str(Page_End)
								)

							QuryCount_str = (
								"SELECT COUNT(CpqTableEntryId) AS cnt FROM CTCICO (nolock) WHERE CONTRACT_RECORD_ID = '"
									+ str(RecAttValue)
									+ "'and GREENBOOK = '"+str(TreeParam)+"'"
							)  
						else:    
							imgstr = '<img title="Acquired" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Green_Tick.svg>'
							acquiring_img_str = '<img title="Acquiring" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Cloud_Icon.svg>'
							qt_rec_id = SqlHelper.GetFirst("SELECT CONTRACT_ID, SERVICE_ID FROM CTCTSV WHERE CONTRACT_RECORD_ID ='" + str(
							contract_quote_record_id) + "'")
							LineAndEquipIDList = TreeParam.split(' - ')
							if qt_rec_id.CONTRACT_ID == '70011556':
								SERV_DESC = "Z0091"
							else:
								SERV_DESC = qt_rec_id.SERVICE_ID                            
							if TreeParentParam == "Cart Items":                                
								Qury_str = (
									"select top "
										+ str(PerPage)
										+ " CASE WHEN DISCOUNT = 'ACQUIRED' THEN '"+ imgstr +"' ELSE '"+ imgstr +"' END AS EQUIPMENT_STATUS, CONTRACT_ITEM_COVERED_OBJECT_RECORD_ID, EQUIPMENT_LINE_ID, SERVICE_ID, EQUIPMENT_ID,LINE_ITEM_ID,DISCOUNT,SERIAL_NO, GREENBOOK, TOTAL_COST, TAX, EXTENDED_PRICE,CpqTableEntryId from ( select  ROW_NUMBER() OVER( ORDER BY EQUIPMENT_LINE_ID) AS ROW, * from CTCICO (NOLOCK) where CONTRACT_ID = '"
										+ str(qt_rec_id.CONTRACT_ID)
										+ "' AND SERVICE_ID = '"
										+ str(LineAndEquipIDList[1])
										+ "') m where m.ROW BETWEEN "
										+ str(Page_start)
										+ " and "
										+ str(Page_End)
								)
								QuryCount_str = (
										"select count(*) as cnt FROM CTCICO where SERVICE_ID = '{}' and CONTRACT_ID = '{}'".format(
											LineAndEquipIDList[1], str(qt_rec_id.CONTRACT_ID))
								)
							else:
								Qury_str = (
									"select top "
										+ str(PerPage)
										+ " * from ( select  ROW_NUMBER() OVER( ORDER BY EQUIPMENT_LINE_ID) AS ROW, * from CTCICO (NOLOCK) where CONTRACT_ID = '"
										+ str(qt_rec_id.CONTRACT_ID)
										+ "' AND SERVICE_ID = '"
										+ str(SERV_DESC)
										+ "') m where m.ROW BETWEEN "
										+ str(Page_start)
										+ " and "
										+ str(Page_End)
								)
								QuryCount_str = (
										"select count(*) as cnt FROM CTCICO where SERVICE_ID = '{}' and CONTRACT_ID = '{}'".format(
											SERV_DESC, str(qt_rec_id.CONTRACT_ID))
								)
					elif str(RECORD_ID) == "SYOBJR-98788":       
						contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
						qt_rec_id= Sql.GetFirst("SELECT QUOTE_ID FROM SAQTSV WHERE QUOTE_RECORD_ID ='"+str(contract_quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' ")
						
						if TreeParentParam:
							Qustr = "where "+ str(ATTRIBUTE_VALUE_STR)+" QUOTE_ID = '"+str(qt_rec_id.QUOTE_ID)+"' and SERVICE_TYPE = '{}' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"'".format(TreeParam)
						else:
							Qustr = "where "+ str(ATTRIBUTE_VALUE_STR)+" QUOTE_ID = '"+str(qt_rec_id.QUOTE_ID)+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"'"
						
						doc_type = Sql.GetList("SELECT DOCTYP_ID FROM SAQTSV (NOLOCK) "+ str(Qustr))

						for document_type in doc_type:
							if document_type.DOCTYP_ID == "ZWK1":
								Qury_str = (
									"select DISTINCT top "
									+ str(PerPage)
									+ " "
									+ str(select_obj_str)
									+ ",CpqTableEntryId from ( select TOP 10 ROW_NUMBER() OVER(order by "
									+ str(Wh_API_NAMEs)
									+ ") AS ROW, S.QUOTE_SERVICE_RECORD_ID,S.SERVICE_ID,S.SERVICE_DESCRIPTION,S.PAR_SERVICE_ID,S.SERVICE_TYPE,S.QUOTE_RECORD_ID,S.SALESORG_RECORD_ID,S.UOM_RECORD_ID,S.PAR_SERVICE_RECORD_ID,S.QTEREV_RECORD_ID,S.SERVICE_RECORD_ID,CONVERT(VARCHAR(10),CONTRACT_VALID_FROM,101) AS [CONTRACT_VALID_FROM],CONVERT(VARCHAR(10),CONTRACT_VALID_TO,101) AS [CONTRACT_VALID_TO],S.CpqTableEntryId  from SAQTSV S "
									+ str(Qustr)
									+ ") m where m.ROW BETWEEN "
									+ str(Page_start)
									+ " and "
									+ str(Page_End)
									+ ""
								)
							else:
								Qury_str = (
									"select DISTINCT top "
									+ str(PerPage)
									+ " "
									+ str(select_obj_str)
									+ ",CpqTableEntryId from ( select TOP 10 ROW_NUMBER() OVER(order by "
									+ str(Wh_API_NAMEs)
									+ ") AS ROW, S.QUOTE_SERVICE_RECORD_ID,S.SERVICE_ID,S.SERVICE_DESCRIPTION,S.PAR_SERVICE_ID,S.SERVICE_TYPE,S.QUOTE_RECORD_ID,S.SALESORG_RECORD_ID,S.UOM_RECORD_ID,S.PAR_SERVICE_RECORD_ID,S.QTEREV_RECORD_ID,S.SERVICE_RECORD_ID,CONVERT(VARCHAR(10),CONTRACT_VALID_FROM,101) AS [CONTRACT_VALID_FROM],CONVERT(VARCHAR(10),CONTRACT_VALID_TO,101) AS [CONTRACT_VALID_TO],S.CpqTableEntryId  from SAQTSV S JOIN (SELECT distinct PRDOFR_ID FROM MAADPR WHERE VISIBLE_INCONFIG = 'TRUE' )M ON S.SERVICE_ID = M.PRDOFR_ID "
									+ str(Qustr)
									+ ") m where m.ROW BETWEEN "
									+ str(Page_start)
									+ " and "
									+ str(Page_End)
									+ ""
								)                      
						QuryCount_str = "select count(*) as cnt from " + str(ObjectName) + " S (nolock) JOIN (SELECT distinct PRDOFR_ID FROM MAADPR WHERE VISIBLE_INCONFIG = 'TRUE' ) M ON S.SERVICE_ID = M.PRDOFR_ID " + str(Qustr) 
					elif str(RECORD_ID) == "SYOBJR-98853" and str(TreeParam) == "Tracked Objects":
						RecAttValue = Product.Attributes.GetByName("QSTN_SYSEFL_AC_00063").GetValue()
						Qury_str = (
							"select DISTINCT top "
							+ str(PerPage)
							+ " APPROVAL_TRACKED_FIELD_RECORD_ID,APRCHN_ID,APRCHNSTP,TRKOBJ_TRACKEDFIELD_LABEL,TRKOBJ_NAME,TRACKING_TYPE,CpqTableEntryId from (SELECT ROW_NUMBER() OVER(order by APPROVAL_TRACKED_FIELD_RECORD_ID) AS ROW,ACAPTF.APPROVAL_TRACKED_FIELD_RECORD_ID,ACAPTF.APRCHN_ID,ACAPTF.APRCHNSTP,ACAPTF.TRKOBJ_TRACKEDFIELD_LABEL,ACAPTF.TRKOBJ_NAME,ACAPTF.TRACKING_TYPE,ACAPTF.CpqTableEntryId FROM ACAPTF (NOLOCK) INNER JOIN ACAPTX ON ACAPTF.APRCHN_ID = ACAPTX.APRCHN_ID WHERE "+str(ATTRIBUTE_VALUE_STR)+" ACAPTX.APPROVAL_TRANSACTION_RECORD_ID = '"
							+ str(RecAttValue)
							+ "') S where S.ROW BETWEEN "
							+ str(Page_start)
							+ " and "
							+ str(Page_End)
							+ " "
						)
						QuryCount_str = (
							"SELECT count(DISTINCT ACAPTF.APPROVAL_TRACKED_FIELD_RECORD_ID) as cnt FROM ACAPTF (NOLOCK) INNER JOIN ACAPTX ON ACAPTF.APRCHN_ID = ACAPTX.APRCHN_ID WHERE "+str(ATTRIBUTE_VALUE_STR)+" ACAPTX.APPROVAL_TRANSACTION_RECORD_ID = '"
							+ str(RecAttValue)                            
							+ "' "
						)
					elif str(RECORD_ID) == "SYOBJR-00026" and str(TreeParentParam) == "Tracked Objects":
						RecAttValue = Product.Attributes.GetByName("QSTN_SYSEFL_AC_00063").GetValue()
						Qury_str = (
							"select DISTINCT top "
							+ str(PerPage)
							+ " APPROVAL_TRACKED_VALUE_RECORD_ID,APRCHN_ID,APRCHNSTP,TRKOBJ_TRACKEDFIELD_LABEL,TRKOBJ_NAME,TRKOBJ_TRACKEDFIELD_OLDVALUE,TRKOBJ_TRACKEDFIELD_NEWVALUE,TRKOBJ_CPQTABLEENTRYID,CpqTableEntryId from (SELECT ROW_NUMBER() OVER(order by APPROVAL_TRACKED_VALUE_RECORD_ID) AS ROW,ACAPFV.TRKOBJ_TRACKEDFIELD_OLDVALUE,ACAPFV.APPROVAL_TRACKED_VALUE_RECORD_ID,ACAPFV.APRCHN_ID,ACAPFV.APRCHNSTP,ACAPFV.TRKOBJ_TRACKEDFIELD_LABEL,ACAPFV.TRKOBJ_NAME,ACAPFV.TRKOBJ_TRACKEDFIELD_NEWVALUE, ACAPFV.CpqTableEntryId,ACAPFV.TRKOBJ_CPQTABLEENTRYID FROM ACAPFV (NOLOCK) INNER JOIN ACAPTX ON ACAPFV.APRCHN_ID = ACAPTX.APRCHN_ID AND ACAPFV.APPROVAL_ID = ACAPTX.APPROVAL_ID WHERE "+str(ATTRIBUTE_VALUE_STR)+" ACAPTX.APPROVAL_TRANSACTION_RECORD_ID = '"
							+ str(RecAttValue)
							+ "' AND ACAPFV.TRKOBJ_TRACKEDFIELD_LABEL= '"
							+ str(TreeParam)                            
							+ "') S where S.ROW BETWEEN "
							+ str(Page_start)
							+ " and "
							+ str(Page_End)
							+ " "
						)
						QuryCount_str = (
							"SELECT count(DISTINCT ACAPFV.APPROVAL_TRACKED_VALUE_RECORD_ID) as cnt FROM ACAPFV (NOLOCK) INNER JOIN ACAPTX ON ACAPFV.APRCHN_ID = ACAPTX.APRCHN_ID WHERE "+str(ATTRIBUTE_VALUE_STR)+" ACAPTX.APPROVAL_TRANSACTION_RECORD_ID = '"
							+ str(RecAttValue)
							+ "' AND ACAPFV.TRKOBJ_TRACKEDFIELD_LABEL= '"
							+ str(TreeParam)                            
							+ "' "
						)
					elif str(RECORD_ID) == "SYOBJR-98816":                        
						contract_quote_record_id = Quote.GetGlobal("contract_record_id")
						ct_rec_id= SqlHelper.GetFirst("SELECT CONTRACT_ID FROM CTCTSV WHERE CONTRACT_RECORD_ID ='"+str(contract_quote_record_id)+"'")
						if TreeParentParam:
							Qustr = "where "+str(ATTRIBUTE_VALUE_STR)+" CONTRACT_ID = '"+str(ct_rec_id.CONTRACT_ID)+"' and PRODUCT_TYPE = '{}'".format(TreeParam)
						else:
							Qustr = "where "+str(ATTRIBUTE_VALUE_STR)+ " CONTRACT_ID = '"+str(ct_rec_id.CONTRACT_ID)+"'"
						Qury_str = (
							"select DISTINCT top "
							+ str(PerPage)
							+ " "
							+ str(select_obj_str)
							+ ",CpqTableEntryId from ( select TOP 10 ROW_NUMBER() OVER(order by "
							+ str(Wh_API_NAMEs)
							+ ") AS ROW, * from "
							+ str(ObjectName)
							+ " (nolock) "
							+ str(Qustr)
							+ " ) m where m.ROW BETWEEN "
							+ str(Page_start)
							+ " and "
							+ str(Page_End)
							+ ""
						)                        
						QuryCount_str = "select count(*) as cnt from " + str(ObjectName) + " (nolock) " + str(Qustr)
					elif RECORD_ID == 'SYOBJR-00006' and TreeParam == "Quote Preview":                        
						Qury_str = (
						"SELECT DISTINCT TOP "
						+ str(PerPage)
						+ " QUOTE_ITEM_FORECAST_PART_RECORD_ID,PART_NUMBER,MATPRIGRP_ID,PART_DESCRIPTION,BASEUOM_ID,SCHEDULE_MODE,DELIVERY_MODE,UNIT_PRICE,EXTENDED_PRICE,ANNUAL_QUANTITY,PRICING_STATUS,CUSTOMER_PART_NUMBER_RECORD_ID,BASEUOM_RECORD_ID,MATPRIGRP_RECORD_ID,QTEITM_RECORD_ID,QUOTE_RECORD_ID,SALESORG_RECORD_ID,SERVICE_RECORD_ID,PART_RECORD_ID,SALESUOM_RECORD_ID,CpqTableEntryId,TAX,TAX_PERCENTAGE,SERVICE_ID,SRVTAXCLA_DESCRIPTION from ( select TOP "+ str(PerPage)+" ROW_NUMBER() OVER(order by "+ str(Wh_API_NAMEs) +") AS ROW, * from SAQIFP (nolock)  where "+ str(ATTRIBUTE_VALUE_STR)+" QUOTE_RECORD_ID ='"+str(RecAttValue)
						+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' ) m where m.ROW BETWEEN "
						+ str(Page_start)
						+ " AND "
						+ str(Page_End)+" "
						)
						QuryCount_str = (
							"SELECT COUNT(CpqTableEntryId) AS cnt FROM SAQIFP (nolock) WHERE "+ str(ATTRIBUTE_VALUE_STR)+" QUOTE_RECORD_ID = '"
							+ str(RecAttValue)
							+ "' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' "
						)
					elif RECORD_ID == 'SYOBJR-98869' and TreeParam == "Revisions":
						Qury_str = ("select DISTINCT TOP "
							+ str(PerPage)
							+ " QUOTE_REVISION_RECORD_ID,CONCAT(QUOTE_ID, '-', QTEREV_ID) AS QTEREV_ID,REVISION_DESCRIPTION,REV_CREATE_DATE,REV_EXPIRE_DATE,REVISION_STATUS,ACTIVE,CONTRACT_VALID_FROM,CONTRACT_VALID_TO,SALESORG_RECORD_ID,QUOTE_RECORD_ID,CpqTableEntryId from ( select ROW_NUMBER() OVER(order by QUOTE_RECORD_ID) AS ROW, * from SAQTRV (nolock)  where "+str(ATTRIBUTE_VALUE_STR)+ " QUOTE_RECORD_ID = '" 
							+ str(contract_quote_record_id) + "' ) m where m.ROW BETWEEN "
							+ str(Page_start)
							+ " and "
							+ str(Page_End)
							+ ""
						)
						# Qury_str = ("select DISTINCT TOP "
						#     + str(PerPage)
						#     + " QUOTE_REVISION_RECORD_ID,CONCAT(QUOTE_ID, '-', QTEREV_ID) AS QTEREV_ID,REVISION_DESCRIPTION,REV_CREATE_DATE,REV_EXPIRE_DATE,REVISION_STATUS,ACTIVE,CONTRACT_VALID_FROM,CONTRACT_VALID_TO,SALESORG_RECORD_ID,QUOTE_RECORD_ID,CpqTableEntryId from ( select TOP 10 ROW_NUMBER() OVER(order by QUOTE_RECORD_ID) AS ROW, * from SAQTRV (nolock)  where QUOTE_RECORD_ID = '" 
						#     + str(contract_quote_record_id) + "' ) m where m.ROW BETWEEN "
						#     + str(Page_start)
						#     + " and "
						#     + str(Page_End)
						#     + ""
						# )
						QuryCount_str = (
							"SELECT COUNT(QUOTE_REVISION_RECORD_ID) AS cnt FROM SAQTRV (nolock) WHERE QUOTE_RECORD_ID = '"
							+ str(contract_quote_record_id)
							+ "'"
						)
					elif RECORD_ID == 'SYOBJR-00010':
						imgstr = '<img title="Acquired" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Green_Tick.svg>'
						acquiring_img_str = '<img title="Acquiring" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Cloud_Icon.svg>'
						error = '<img title="Error" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/exclamation_icon.svg>'
						cps_pricing_img = ""                     
						#cps_pricing_img ='<a href="#" onclick=""><img src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/info.png"></a>' 
						Qury_str = (
							"SELECT DISTINCT TOP "
							+ str(PerPage)
							+ "QUOTE_ITEM_FORECAST_PART_RECORD_ID, CASE WHEN PRICING_STATUS = 'ACQUIRED' THEN '"+ imgstr +"' WHEN PRICING_STATUS = 'APPROVAL REQUIRED' THEN '" +exclamation+ "' WHEN PRICING_STATUS = 'ERROR' THEN '" +error+ "' ELSE '"+ acquiring_img_str +"' END AS PRICING_STATUS,SERVICE_ID,CONCAT('"+cps_pricing_img+ "',PART_NUMBER) AS PART_NUMBER,PART_DESCRIPTION,MATPRIGRP_ID,BASEUOM_ID,SCHEDULE_MODE,DELIVERY_MODE,UNIT_PRICE,UNIT_PRICE_INGL_CURR,EXTENDED_PRICE,EXTPRI_INGL_CURR,ANNUAL_QUANTITY,CUSTOMER_PART_NUMBER_RECORD_ID,BASEUOM_RECORD_ID,MATPRIGRP_RECORD_ID,QTEITM_RECORD_ID,QUOTE_RECORD_ID,QTEREV_RECORD_ID,SALESORG_RECORD_ID,SERVICE_RECORD_ID,PART_RECORD_ID,SALESUOM_RECORD_ID,CpqTableEntryId,TAX,SRVTAXCLA_DESCRIPTION,TAX_PERCENTAGE from ( select TOP 10 ROW_NUMBER() OVER(order by "+ str(Wh_API_NAMEs) +") AS ROW, * from SAQIFP (nolock)  where "+ str(ATTRIBUTE_VALUE_STR)+" QUOTE_RECORD_ID ='"+str(RecAttValue)
							+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' ) m where m.ROW BETWEEN "
							+ str(Page_start)
							+ " AND "
							+ str(Page_End)+" ORDER BY PRICING_STATUS ASC"
						)
						QuryCount_str = (
							"SELECT COUNT(CpqTableEntryId) AS cnt FROM SAQIFP (nolock) WHERE "+ str(ATTRIBUTE_VALUE_STR)+" QUOTE_RECORD_ID = '"
							+ str(RecAttValue)
							+ "' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' "
						)
					elif RECORD_ID == 'SYOBJR-00008':
						imgstr = '<img title="Acquired" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Green_Tick.svg>'
						acquiring_img_str = '<img title="Acquiring" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Cloud_Icon.svg>'
						exclamation = '<img title="Approval Required" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/clock_exe.svg>'

						if getyears == 1:
							col_year =  'YEAR_1'
						elif getyears == 2:
							col_year =  'YEAR_1,YEAR_2'
						elif getyears == 3:
							col_year =  'YEAR_1,YEAR_2,YEAR_3'
						elif getyears == 4:
							col_year =  'YEAR_1,YEAR_2,YEAR_3,YEAR_4'
						else:
							col_year = 'YEAR_1,YEAR_2,YEAR_3,YEAR_4,YEAR_5'

						price_status = []
						# quote_itm_rec = Sql.GetFirst("SELECT QUOTE_ITEM_RECORD_ID FROM SAQITM (NOLOCK) "+str(Qustr)+"")
						SAQICO_status = Sql.GetList("SELECT DISTINCT STATUS FROM SAQICO (NOLOCK) "+str(Qustr)+"")
						for pricing_status in SAQICO_status:
							price_status.append(pricing_status.STATUS)
						
						all_acquired = ["ACQUIRING","APPROVAL REQUIRED","ERROR"]
						all_error = ["APPROVAL REQUIRED","ACQUIRING","ACQUIERD"]
						all_required = ["ACQUIERD","ACQUIRING","ERROR"]
						all_acquiring = ["ACQUIERD","ERROR","APPROVAL REQUIRED"]
						acq_error = ["ACQUIERD","ERROR"]
						acq_req = ["ACQUIERD","APPROVAL REQUIRED"]
						not_acq_req = ["ACQUIRING","ERROR"]
						acq_error_approval = ["ACQUIERD","ERROR","APPROVAL"]
						not_acq_error = ["ACQUIRING","APPROVAL REQUIRED"]

						if "ACQUIRED" in price_status and ('ACQUIRING' not in price_status and 'APPROVAL REQUIRED' not in price_status and 'ERROR' not in price_status):
							icon = '<img title="Acquired" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Green_Tick.svg>'
						elif "ERROR" in price_status and ('ACQUIRED' not in price_status and 'APPROVAL REQUIRED' not in price_status and 'ACQUIRING' not in price_status):
							icon = '<img title="Error" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/exclamation_icon.svg>'
						elif "APPROVAL REQUIRED" in price_status and ('ACQUIRED' not in price_status and 'ERROR' not in price_status and 'ACQUIRING' not in price_status):
							icon = '<img title="Approval Required" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/clock_exe.svg>'
						elif "ACQUIRING" in price_status and 'ACQUIRED' not in price_status and 'ERROR' not in price_status and 'APPROVAL REQUIRED' not in price_status:
							icon = '<img title="Acquiring" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Cloud_Icon.svg>'
						elif ("ACQUIRED" in price_status and "ERROR" in price_status) and ('ACQUIRING' not in price_status and 'APPROVAL REQUIRED' not in price_status):
							icon = '<img title="Error" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/exclamation_icon.svg>'
						elif ("ACQUIRED" in price_status and "ACQUIRING" in price_status) and ('ERROR' not in price_status and 'APPROVAL REQUIRED' not in price_status):
							icon = '<img title="Acquiring" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Cloud_Icon.svg>'
						elif ("ACQUIRED" in price_status and "APPROVAL REQUIRED" in price_status) and ('ERROR' not in price_status and 'ACQUIRING' not in price_status):
							icon = '<img title="Approval Required" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/clock_exe.svg>'
						elif ("ACQUIRED" in price_status and 'ERROR' in price_status and 'APPROVAL REQUIRED' in price_status) and "ACQUIRING" not in price_status :
							icon = '<img title="Error" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/exclamation_icon.svg>'
						elif ("ACQUIRING" in price_status and 'APPROVAL REQUIRED' in price_status) and ('ACQUIRED' not in price_status and "ERROR" not in price_status) :
							icon = '<img title="Approval Required" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/clock_exe.svg>'
						else:
							icon = '<img title="Error" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/exclamation_icon.svg>'
						


						if TreeParam == "Quote Items":                            
							Qustr = "where "+ str(ATTRIBUTE_VALUE_STR)+" QUOTE_RECORD_ID ='"+str(RecAttValue)+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' "
							Qury_str = (
								"select DISTINCT top "
								+ str(PerPage)
								+ " '"+ icon +"' AS PO_NOTES, QUOTE_ITEM_RECORD_ID, LINE_ITEM_ID, SERVICE_ID, SERVICE_DESCRIPTION, OBJECT_QUANTITY,QUANTITY, TOTAL_COST, SALES_DISCOUNT_PRICE,SRVTAXCLA_DESCRIPTION,TAX_PERCENTAGE,TAX, NET_VALUE, TARGET_PRICE, CEILING_PRICE, BD_PRICE, BD_PRICE_MARGIN, DISCOUNT, NET_PRICE, YEAR_OVER_YEAR, "+col_year+" "
								+ ",CpqTableEntryId from ( select TOP 10 ROW_NUMBER() OVER(order by "
								+ str(Wh_API_NAMEs)
								+ ") AS ROW, * from "
								+ str(ObjectName)
								+ " (nolock) "
								+ str(Qustr)
								+ " ) m where m.ROW BETWEEN "
								+ str(Page_start)
								+ " and "
								+ str(Page_End)
								+ ""
							)
							QuryCount_str = "select count(*) as cnt from " + str(ObjectName) + " (nolock) " + str(Qustr)
					elif RECORD_ID == 'SYOBJR-00024':
						dynamic_condtn = ""
						quote_obj = Sql.GetFirst("select QUOTE_ID,MASTER_TABLE_QUOTE_RECORD_ID from SAQTMT where MASTER_TABLE_QUOTE_RECORD_ID = '{contract_quote_record_id}' AND QTEREV_RECORD_ID='{revision_rec_id}'".format(contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id"), revision_rec_id = quote_revision_record_id))
						quote_id = quote_obj.QUOTE_ID
						TreeParam = Product.GetGlobal("TreeParam")
						if TreeSuperParentParam == 'Approvals':
							chain_step_name = SubTab.split(':')[1].strip()
							step_id = chain_step_name.split(' ')[1]
							round_value = TreeParam.split()[1]
							TreeParam = Product.GetGlobal("TreeParam")
							Qury_str = ("""select DISTINCT top {PerPage} * from (select ROW_NUMBER() OVER( ORDER BY ACAPTX.APRCHNSTP_ID) AS ROW,ACAPTX.APPROVAL_TRANSACTION_RECORD_ID, ACAPTX.APPROVAL_ID,ACAPTX.APRCHNSTP_ID,ACAPTX.APRCHNSTP_APPROVER_ID,ACAPTX.APPROVAL_ROUND,ACAPTX.APPROVALSTATUS,ACAPTX.RECIPIENT_COMMENTS,ACAPTX.APRCHNSTP_RECORD_ID,ACAPTX.APPROVAL_RECIPIENT,ACAPTX.CpqTableEntryId FROM ACAPTX (nolock) inner join ACACST (nolock) on ACAPTX.APRCHNSTP_RECORD_ID = ACACST.APPROVAL_CHAIN_STEP_RECORD_ID  and ACAPTX.APRTRXOBJ_ID = '{Quote_id}' and {ATTRIBUTE_VALUE_STR} ACAPTX.APRCHNSTPTRX_ID like '%{Quote_id}%' and ACAPTX.APRCHN_ID = '{chain_id}' {dynamic_condtn})m where m.ROW BETWEEN """.format(PerPage = PerPage,contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id"),Quote_id = quote_id,dynamic_condtn=dynamic_condtn,ATTRIBUTE_VALUE_STR = ATTRIBUTE_VALUE_STR,chain_id=TreeParentParam if TreeSuperParentParam == 'Approvals' else TreeParam) + str(Page_start) + " and " + str(Page_End))
							QuryCount_str = """select count(ACAPTX.CpqTableEntryId) as cnt FROM ACAPTX (nolock) inner join ACACST (nolock) on ACAPTX.APRCHNSTP_RECORD_ID = ACACST.APPROVAL_CHAIN_STEP_RECORD_ID and  ACAPTX.APRTRXOBJ_ID = '{Quote_id}' and {ATTRIBUTE_VALUE_STR} ACAPTX.APRCHNSTPTRX_ID like '%{Quote_id}%' and ACAPTX.APRCHN_ID = '{chain_id}' {dynamic_condtn}""".format(contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id"),Quote_id = quote_id,dynamic_condtn=dynamic_condtn,ATTRIBUTE_VALUE_STR = ATTRIBUTE_VALUE_STR,chain_id=TreeParentParam if TreeSuperParentParam == 'Approvals' else TreeParam)
						else:
							
							Qury_str = ("""select DISTINCT top {PerPage} * from (select ROW_NUMBER() OVER( ORDER BY ACAPTX.APPROVAL_TRANSACTION_RECORD_ID) AS ROW,ACAPTX.APPROVAL_TRANSACTION_RECORD_ID, ACAPTX.APPROVAL_ID,ACAPTX.APRCHNSTP_ID,ACAPTX.APRCHNSTP_APPROVER_ID,ACAPTX.APPROVAL_ROUND,ACAPTX.APPROVALSTATUS,ACAPTX.RECIPIENT_COMMENTS,ACAPTX.APRCHNSTP_RECORD_ID,ACAPTX.APPROVAL_RECIPIENT,ACAPTX.CpqTableEntryId FROM ACAPTX (nolock) inner join ACACST (nolock) on ACAPTX.APRCHNSTP_RECORD_ID = ACACST.APPROVAL_CHAIN_STEP_RECORD_ID  and ACAPTX.APRTRXOBJ_ID = '{Quote_id}' and  {ATTRIBUTE_VALUE_STR} ACAPTX.APRCHNSTPTRX_ID like '%{Quote_id}%' and ACAPTX.APRCHN_ID = '{Chain}')m where m.ROW BETWEEN """.format(PerPage = PerPage,contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id"),Quote_id = quote_id,Chain = TreeParam,ATTRIBUTE_VALUE_STR = ATTRIBUTE_VALUE_STR) + str(Page_start) + " and " + str(Page_End))
							QuryCount_str = """select count(ACAPTX.CpqTableEntryId) as cnt FROM ACAPTX (nolock) inner join ACACST (nolock) on ACAPTX.APRCHNSTP_RECORD_ID = ACACST.APPROVAL_CHAIN_STEP_RECORD_ID and  ACAPTX.APRTRXOBJ_ID = '{Quote_id}' and ACAPTX.APRCHNSTPTRX_ID like '%{Quote_id}%' and {ATTRIBUTE_VALUE_STR}  ACAPTX.APRCHN_ID = '{Chain}' """.format(contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id"),Quote_id = quote_id,Chain = TreeParam, ATTRIBUTE_VALUE_STR = ATTRIBUTE_VALUE_STR)
					
					##involved parties equipmemt and tool relocation matrix starts
					elif (str(RECORD_ID) == "SYOBJR-98858" or str(RECORD_ID) == "SYOBJR-00028") and str(TreeParam) == "Quote Information":
						account_id = Product.GetGlobal("stp_account_id")
						
						Qury_str = ("""select DISTINCT top {PerPage} * from (select ROW_NUMBER() OVER( ORDER BY SAQSTE.FABLOCATION_ID DESC) AS ROW,SAQSTE.* from SAQSTE  inner join SAQSCF(nolock)  on SAQSTE.QUOTE_RECORD_ID = SAQSCF.QUOTE_RECORD_ID and SAQSTE.QTEREV_RECORD_ID = SAQSCF.QTEREV_RECORD_ID and SAQSTE.SRCFBL_ID = SAQSCF.SRCFBL_ID where SAQSTE.QUOTE_RECORD_ID = '{contract_quote_record_id}' AND QTEREV_RECORD_ID='{revision_rec_id}' and SAQSTE.{ATTRIBUTE_VALUE_STR} SAQSTE.SRCACC_ID = '{account_id}')m where m.ROW BETWEEN """.format(PerPage = PerPage,account_id = account_id,revision_rec_id = quote_revision_record_id,
						contract_quote_record_id = str(RecAttValue),ATTRIBUTE_VALUE_STR = ATTRIBUTE_VALUE_STR)+ str(Page_start) + " and " + str(Page_End))
						
						
						
						QuryCount_str = "select count(SAQSTE.CpqTableEntryId) as cnt from SAQSTE  inner join SAQSCF(nolock) on SAQSTE.QUOTE_RECORD_ID = SAQSCF.QUOTE_RECORD_ID  and SAQSTE.QTEREV_RECORD_ID = SAQSCF.QTEREV_RECORD_ID and SAQSTE.SRCFBL_ID= SAQSCF.SRCFBL_ID where SAQSTE.QUOTE_RECORD_ID = '{contract_quote_record_id}' AND QTEREV_RECORD_ID='{revision_rec_id}' and SAQSTE.{ATTRIBUTE_VALUE_STR} SAQSTE.SRCACC_ID = '{account_id}'".format(account_id = account_id,contract_quote_record_id=str(RecAttValue),ATTRIBUTE_VALUE_STR = ATTRIBUTE_VALUE_STR,revision_rec_id = quote_revision_record_id)
					##involved parties equipmemt ends
					elif str(RECORD_ID) == "SYOBJR-98859":
						#"where "+ str(ATTRIBUTE_VALUE_STR)+" QUOTE_RECORD_ID ='"+str(RecAttValue)+"'"
						Qustr += " where "+ str(ATTRIBUTE_VALUE_STR)+" QUOTE_RECORD_ID ='"+str(RecAttValue)+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' AND PAR_SERVICE_ID = '"+str(TreeSuperParentParam)+"' AND GREENBOOK = '"+str(TreeParentParam)+"' "
						Qury_str = (
							"select DISTINCT top "
							+ str(PerPage)
							+ " "
							+ str(select_obj_str)
							+ ",CpqTableEntryId from ( select TOP 10 ROW_NUMBER() OVER(order by "
							+ str(Wh_API_NAMEs)
							+ ") AS ROW, * from "
							+ str(ObjectName)
							+ " (nolock) "
							+ str(Qustr)
							+ " ) m where m.ROW BETWEEN "
							+ str(Page_start)
							+ " and "
							+ str(Page_End)
							+ ""
						)
						
						QuryCount_str = "select count(*) as cnt from " + str(ObjectName) + " (nolock) " + str(Qustr)

					##involved parties source fab starts
					elif str(RECORD_ID) == "SYOBJR-98862":
						RecAttValue=Product.Attributes.GetByName("QSTN_SYSEFL_SY_00125").GetValue()
						Qustr = " WHERE "+str(ATTRIBUTE_VALUE_STR) +" APP_ID = '"+str(TreeParentParam)+"' AND PROFILE_RECORD_ID ='"+str(RecAttValue)+"'"
						Qury_str = (
							"select DISTINCT top "
							+ str(PerPage)
							+ " "
							+ str(select_obj_str)
							+ ",CpqTableEntryId from ( select TOP 10 ROW_NUMBER() OVER(order by "
							+ str(Wh_API_NAMEs)
							+ ") AS ROW, * from "
							+ str(ObjectName)
							+ " (nolock) "
							+ str(Qustr)
							+" ) m where m.ROW BETWEEN "
							+ str(Page_start)
							+ " and "
							+ str(Page_End)
							+ ""
						)
						
						QuryCount_str = "select count(*) as cnt from " + str(ObjectName) + " (nolock) " + str(Qustr)
					elif str(RECORD_ID) == "SYOBJR-98863":
						RecAttValue=Product.Attributes.GetByName("QSTN_SYSEFL_SY_00125").GetValue()
						Qustr = " WHERE "+str(ATTRIBUTE_VALUE_STR) +" TAB_ID = '"+str(TreeParentParam)+"' AND PROFILE_RECORD_ID ='"+str(RecAttValue)+"'"
						Qury_str = (
							"select DISTINCT top "
							+ str(PerPage)
							+ " "
							+ str(select_obj_str)
							+ ",CpqTableEntryId from ( select TOP 10 ROW_NUMBER() OVER(order by "
							+ str(Wh_API_NAMEs)
							+ ") AS ROW, * from "
							+ str(ObjectName)
							+ " (nolock) "
							+ str(Qustr)
							+ " ) m where m.ROW BETWEEN "
							+ str(Page_start)
							+ " and "
							+ str(Page_End)
							+ ""
						)
					
						QuryCount_str = "select count(*) as cnt from " + str(ObjectName) + " (nolock) " + str(Qustr)
					
					elif str(RECORD_ID) == "SYOBJR-98864":
						Qustr = " WHERE "+str(ATTRIBUTE_VALUE_STR) +" TAB_NAME = '"+str(TreeParentParam)+"' AND PROFILE_RECORD_ID ='"+str(RecAttValue)+"'"
						Qury_str = (
							"select DISTINCT top "
							+ str(PerPage)
							+ " "
							+ str(select_obj_str)
							+ ",CpqTableEntryId from ( select TOP 10 ROW_NUMBER() OVER(order by "
							+ str(Wh_API_NAMEs)
							+ ") AS ROW, * from "
							+ str(ObjectName)
							+ " (nolock) "
							+ str(Qustr)
							+ " ) m where m.ROW BETWEEN "
							+ str(Page_start)
							+ " and "
							+ str(Page_End)
							+ ""
						)
						
						QuryCount_str = "select count(*) as cnt from " + str(ObjectName) + " (nolock) " + str(Qustr)
					elif str(RECORD_ID) == "SYOBJR-93123":
						app_ObjectName = Sql.GetFirst("select PRIMARY_OBJECT_NAME FROM SYTABS INNER JOIN SYAPPS ON SYTABS.APP_LABEL = SYAPPS.APP_LABEL WHERE SYTABS.TAB_LABEL = '"+str(TopTreeSuperParentParam)+"' AND SYAPPS.APP_LABEL = '"+str(TreeFirstSuperTopParentParam)+"'")
						RecAttValue = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00128").GetValue()
						Qustr = " WHERE "+str(ATTRIBUTE_VALUE_STR) +" SECTION_NAME = '"+str(TreeParentParam)+"' AND PROFILE_ID ='"+str(RecAttValue)+"' AND OBJECT_NAME = '"+str(app_ObjectName.PRIMARY_OBJECT_NAME)+"' "
						Qury_str = (
							"select DISTINCT top "
							+ str(PerPage)
							+ " "
							+ str(select_obj_str)
							+ ",CpqTableEntryId from ( select TOP 10 ROW_NUMBER() OVER(order by "
							+ str(Wh_API_NAMEs)
							+ ") AS ROW, * from "
							+ str(ObjectName)
							+ " (nolock) "
							+ str(Qustr)
							+ " ORDER BY SECTION_FIELD_ID ASC ) m where m.ROW BETWEEN "
							+ str(Page_start)
							+ " and "
							+ str(Page_End)
							+ ""
						)
						
						QuryCount_str = "select count(*) as cnt from " + str(ObjectName) + " (nolock) " + str(Qustr)    
					elif str(RECORD_ID) == "SYOBJR-98784" and TreeFirstSuperTopParentParam == "Pages":
						Qustr = " WHERE SECTION_NAME = '"+str(TreeParentParam)+"' AND TAB_NAME = '"+str(TreeSecondSuperTopParentParam)+"'"
						Qury_str = (
							"select DISTINCT top "
							+ str(PerPage)
							+ " "
							+ str(select_obj_str)
							+ ",CpqTableEntryId from ( select TOP 10 ROW_NUMBER() OVER(order by "
							+ str(Wh_API_NAMEs)
							+ ") AS ROW, * from "
							+ str(ObjectName)
							+ " (nolock) "
							+ str(Qustr)
							+ " ) m where m.ROW BETWEEN "
							+ str(Page_start)
							+ " and "
							+ str(Page_End)
							+ ""
						)
						
						QuryCount_str = "select count(*) as cnt from " + str(ObjectName) + " (nolock) " + str(Qustr)
					elif str(RECORD_ID) == "SYOBJR-93188":
						RecAttValue = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00128").GetValue()
						GetAppname_query = ""
						Qustr = " WHERE TAB_NAME = '"+str(TreeParentParam)+"'and "+str(ATTRIBUTE_VALUE_STR)+" PROFILE_ID ='"+str(RecAttValue)+"'"
						Qury_str = (
							"select DISTINCT top "
							+ str(PerPage)
							+ " "
							+ str(select_obj_str)
							+ ",CpqTableEntryId from ( select TOP 10 ROW_NUMBER() OVER(order by "
							+ str(Wh_API_NAMEs)
							+ ") AS ROW, * from "
							+ str(ObjectName)
							+ " (nolock) "
							+ str(Qustr)
							+ " ) m where m.ROW BETWEEN "
							+ str(Page_start)
							+ " and "
							+ str(Page_End)
							+ ""
						)
						
						QuryCount_str = "select count(*) as cnt from " + str(ObjectName) + " (nolock) " + str(Qustr)
					elif str(RECORD_ID) == "SYOBJR-95825" and str(TreeParentParam) == 'Constraints':
						Qustr = "WHERE CONSTRAINT_TYPE = '"+str(TreeParam)+"' AND OBJECT_RECORD_ID ='"+str(RecAttValue)+"'" 
						Qury_str = (
							"select DISTINCT top "
							+ str(PerPage)
							+ " "
							+ str(select_obj_str)
							+ ",CpqTableEntryId from ( select TOP 10 ROW_NUMBER() OVER(order by "
							+ str(Wh_API_NAMEs)
							+ ") AS ROW, * from "
							+ str(ObjectName)
							+ " (nolock) "
							+ str(Qustr)
							+ " ) m where m.ROW BETWEEN "
							+ str(Page_start)
							+ " and "
							+ str(Page_End)
							+ ""
						)
						
						QuryCount_str = "select count(*) as cnt from " + str(ObjectName) + " (nolock) " + str(Qustr)
					elif (str(RECORD_ID) == "SYOBJR-98857") and str(TreeParam) == "Quote Information":
						account_id = Product.GetGlobal("stp_account_id")
						quote_rec_id = Product.GetGlobal("contract_quote_record_id")
						Qustr = " WHERE QUOTE_RECORD_ID = '"+str(quote_rec_id)+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' and  "+str(ATTRIBUTE_VALUE_STR) +" SRCACC_ID = '{}'".format(account_id)
						Qury_str = (
							"select DISTINCT top "
							+ str(PerPage)
							+ " "
							+ str(select_obj_str)
							+ ",CpqTableEntryId from ( select TOP 10 ROW_NUMBER() OVER(order by "
							+ str(Wh_API_NAMEs)
							+ ") AS ROW, * from "
							+ str(ObjectName)
							+ " (nolock) "
							+ str(Qustr)
							+ " ) m where m.ROW BETWEEN "
							+ str(Page_start)
							+ " and "
							+ str(Page_End)
							+ ""
						)
						
						
						
						QuryCount_str = "select count(*) as cnt from " + str(ObjectName) + " (nolock) " + str(Qustr)
					##involved parties source fab ends
					elif RECORD_ID == 'SYOBJR-98841':
						imgstr = '<img title="Acquired" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Green_Tick.svg>'
						acquiring_img_str = '<img title="Acquiring" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Cloud_Icon.svg>'
						
						if TreeParam == "Cart Items":
							Qury_str = (
								"select DISTINCT top "
								+ str(PerPage)
								+ "  CASE WHEN ITEM_STATUS = 'ACQUIRED' THEN '"+ imgstr +"' ELSE '"+ imgstr +"' END AS PO_NOTES, CONTRACT_ITEM_RECORD_ID, LINE_ITEM_ID, SERVICE_ID, SERVICE_DESCRIPTION, QUANTITY, TAX, DISCOUNT, EXTENDED_PRICE"
								+ ",CpqTableEntryId from ( select TOP 10 ROW_NUMBER() OVER(order by "
								+ str(Wh_API_NAMEs)
								+ ") AS ROW, * from "
								+ str(ObjectName)
								+ " (nolock) "
								+ str(Qustr)
								+ " ) m where m.ROW BETWEEN "
								+ str(Page_start)
								+ " and "
								+ str(Page_End)
								+ ""
							)
							QuryCount_str = "select count(*) as cnt from " + str(ObjectName) + " (nolock) " + str(Qustr)
					elif RECORD_ID == 'SYOBJR-98792' and str(TreeParam) == "Quote Preview":                        
						contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
						# Qustr_id = Sql.GetFirst("SELECT QUOTE_ID FROM SAQITM WHERE QUOTE_RECORD_ID ='" + str(
						#contract_quote_record_id) + "' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"'")
						if getyears == 1:
							col_year =  'YEAR_1'
						elif getyears == 2:
							col_year =  'YEAR_1,YEAR_2'
						elif getyears == 3:
							col_year =  'YEAR_1,YEAR_2,YEAR_3'
						elif getyears == 4:
							col_year =  'YEAR_1,YEAR_2,YEAR_3,YEAR_4'
						else:
							col_year = 'YEAR_1,YEAR_2,YEAR_3,YEAR_4,YEAR_5'
						# if TreeParam:
						# 	Qustr = "where QUOTE_ID = '"+str(Qustr_id.QUOTE_ID)+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' "
						Qury_str = (
							"select DISTINCT top "
							+ str(PerPage)
							+ " QUOTE_ITEM_RECORD_ID, LINE_ITEM_ID, SERVICE_ID, SERVICE_DESCRIPTION, ONSITE_PURCHASE_COMMIT,OBJECT_QUANTITY, TOTAL_COST, SALES_DISCOUNT_PRICE, TAX, NET_VALUE, QUANTITY, TARGET_PRICE, CEILING_PRICE, BD_PRICE, BD_PRICE_MARGIN, DISCOUNT, NET_PRICE, YEAR_OVER_YEAR, "+col_year+" , SRVTAXCLA_DESCRIPTION, TAX_PERCENTAGE, CpqTableEntryId from ( select TOP 10 ROW_NUMBER() OVER(order by "
							+ str(Wh_API_NAMEs)
							+ ") AS ROW, * from "
							+ str(ObjectName)
							+ " (nolock) "
							+ str(Qustr)
							+ " AND SERVICE_ID NOT LIKE '%BUNDLE%') m where m.ROW BETWEEN "
							+ str(Page_start)
							+ " and "
							+ str(Page_End)
							+ ""
						)
						QuryCount_str = "select count(*) as cnt from " + str(ObjectName) + " (nolock) " + str(Qustr)+ " AND SERVICE_ID NOT LIKE '%BUNDLE%' "

					elif str(RECORD_ID) == "SYOBJR-98815":                        
						#Qustr = "where SALESORG_ID = '"+str(TP)+"' and DOC_CURRENCY='"+str(PR_CURR)+"'"
						splitTP = TP.split('-')
						TP = splitTP[1]
						Qury_str = (
							"SELECT DISTINCT TOP "
							+ str(PerPage)
							+ "QUOTE_SALESORG_RECORD_ID,QUOTE_ID,SALESORG_ID,SALESORG_NAME,DISTRIBUTIONCHANNEL_ID,DIVISION_ID,SALESOFFICE_ID,SALESOFFICE_NAME,CpqTableEntryId from ( select TOP 10 ROW_NUMBER() OVER(order by "+ str(Wh_API_NAMEs) +") AS ROW, * from SAQTRV (nolock)  where "+ str(ATTRIBUTE_VALUE_STR)+" SALESORG_ID = '"+str(TP)+"' and DOC_CURRENCY='"+str(PR_CURR)+"') m where m.ROW BETWEEN "
							+ str(Page_start)
							+ " AND "
							+ str(Page_End)
							+ ""
						)
						QuryCount_str = (
							"SELECT COUNT(CpqTableEntryId) AS cnt FROM SAQTRV (nolock) WHERE "+ str(ATTRIBUTE_VALUE_STR)+" SALESORG_ID = '"+str(TP)+"' and DOC_CURRENCY='"+str(PR_CURR)+"'"
						)

					elif RECORD_ID == "SYOBJR-95866":                        
						Qustr = (
							" where "
							+ str(Wh_API_NAME)
							+ " = '"
							+ str(RecAttValue)
							+ "' AND "
							+ str(ATTRIBUTE_VALUE_STR)
							+ " CFGMATCLS_PAGE_TYPE in ('PRODUCT LANDING PAGE') "
						)
					elif RECORD_ID == "SYOBJR-95867":                        
						Qustr = (
							" where "
							+ str(Wh_API_NAME)
							+ " = '"
							+ str(RecAttValue)
							+ "' AND "
							+ str(ATTRIBUTE_VALUE_STR)
							+ " CFGMATCLS_PAGE_TYPE in ('PRODUCT CONFIGURATION LANDING PAGE') "
						)
					elif RECORD_ID == "SYOBJR-95987":                        
						Qustr = (
							" where "
							+ str(Wh_API_NAME)
							+ " = '"
							+ str(RecAttValue)
							+ "' AND PRODUCT_SPECIFICATION = 0 AND "
							+ str(ATTRIBUTE_VALUE_STR)
						)
					elif RECORD_ID == "SYOBJR-98784":
						gettabval = getptabname = ""
						CommonTreeTopSuperParentParam = Product.GetGlobal("CommonTreeTopSuperParentParam")
						GetappValue = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00154").GetValue()
						gettabval = Sql.GetFirst(
							"Select RECORD_ID,PAGE_NAME,TAB_LABEL from SYTABS where PAGE_NAME = '"
							+ str(TreeParentParam)
							+ "' and TAB_LABEL = '"
							+ str(TopTreeSuperParentParam)
							+ "'"
						)
						
						if gettabval:
							getptabname = gettabval.RECORD_ID
						Qustr = " where "+ str(ATTRIBUTE_VALUE_STR)+" TAB_RECORD_ID = '" + str(getptabname) + "'"
					elif RECORD_ID == "SYOBJR-94452":                        
						Wh_API_NAME = "ROLE_RECORD_ID"
						RecAttValue = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00001").GetValue()
						
						Qustr = " where "+str(ATTRIBUTE_VALUE_STR)+" "+ str(Wh_API_NAME) + " = '" + str(RecAttValue) + "'"                             
					elif RECORD_ID == "SYOBJR-98782":
						Qustr = " where "+str(ATTRIBUTE_VALUE_STR)+" TAB_LABEL = '" + str(TreeParentParam) + "'"
					elif RECORD_ID == "SYOBJR-94441":                        
						RecAttValue = productAttributesGetByName("QSTN_SYSEFL_SY_00152").GetValue()
						Qustr = " where "+str(ATTRIBUTE_VALUE_STR)+" "+ str(Wh_API_NAME) + " = '" + str(RecAttValue) + "'"
					elif str(RECORD_ID) == "SYOBJR-95824":
						#Qustr = " where " + str(Wh_API_NAME) + " = '" + str(RecAttValue) + "'" 
						RecAttValue = productAttributesGetByName("QSTN_SYSEFL_SY_00701").GetValue()
						Qustr = " where "+str(ATTRIBUTE_VALUE_STR)+" "+ str(Wh_API_NAME) + " = '" + str(RecAttValue) + "'" 
					elif str(RECORD_ID) == "SYOBJR-95840": 
						Wh_API_NAMEs = "PAGEACTION_RECORD_ID"                       
						RecAttValue = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00723").GetValue()
						Qustr =  " where "+str(ATTRIBUTE_VALUE_STR)+" SCRIPT_RECORD_ID = '" + str(RecAttValue) + "'"         
					elif str(RECORD_ID) == "SYOBJR-95890": 
						RecAttValue = Product.Attributes.GetByName("QSTN_SYSEFL_SY_03295").GetValue()
						Qustr = " where "+str(ATTRIBUTE_VALUE_STR)+" "+ str(Wh_API_NAME) + " = '" + str(RecAttValue) + "'"
					elif str(RECORD_ID) == "SYOBJR-95826":
						RecAttValue = productAttributesGetByName("QSTN_SYSEFL_SY_00701").GetValue()
						Qustr = " where "+str(ATTRIBUTE_VALUE_STR)+" "+ str(Wh_API_NAME) + " = '" + str(RecAttValue) + "'"                  
					elif str(RECORD_ID) == "SYOBJR-95976":
						RecAttValue = productAttributesGetByName("QSTN_SYSEFL_SY_00701").GetValue()
						Qustr = " where "+str(ATTRIBUTE_VALUE_STR)+" "+ str(Wh_API_NAME) + " = '" + str(RecAttValue) + "'"
					elif str(RECORD_ID) == "SYOBJR-95985":
						Qustr = " WHERE "+str(ATTRIBUTE_VALUE_STR)+" TREE_NAME = '"+str(TreeParentParam)+"'"
					elif str(RECORD_ID) == "SYOBJR-95981" or str(RECORD_ID)=="SYOBJR-98459":
						RecAttValue = Product.Attributes.GetByName("QSTN_SYSEFL_SY_01110").GetValue()
						Qustr = " where "+str(ATTRIBUTE_VALUE_STR)+" "+ str(Wh_API_NAME) + " = '" + str(RecAttValue) + "'"
					elif str(RECORD_ID) == "SYOBJR-95980":
						RecAttValue = Product.Attributes.GetByName("QSTN_SYSEFL_SY_01110").GetValue()
						Qustr = " where "+str(ATTRIBUTE_VALUE_STR)+" "+ str(Wh_API_NAME) + " = '" + str(RecAttValue) + "'"
					elif str(RECORD_ID) == "SYOBJR-98785":
						RecAttValue = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00811").GetValue()
						Qustr = " where "+str(ATTRIBUTE_VALUE_STR)+" "+ str(Wh_API_NAME) + " = '" + str(RecAttValue) + "'"
					elif str(RECORD_ID) == "SYOBJR-00029":
						quote_rec_id = Product.GetGlobal("contract_quote_record_id")
						quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
						
						if TreeSuperParentParam == "Product Offerings":
							service_id = TreeParam.split('-')[0]		
							Qustr = " where "+str(ATTRIBUTE_VALUE_STR)+" "+ str(Wh_API_NAME) + " = '" + str(RecAttValue) + "' AND PAR_SERVICE_ID = '"+str(service_id)+"' "	
						elif TopTreeSuperParentParam == "Product Offerings":
							service_id = TreeParentParam.split('-')[0]
							Qustr = " where "+str(ATTRIBUTE_VALUE_STR)+" "+ str(Wh_API_NAME) + " = '" + str(RecAttValue) + "' AND PAR_SERVICE_ID = '"+str(service_id)+"' AND GREENBOOK = '"+str(TreeParam)+"' "
						#Qustr = " where "+str(ATTRIBUTE_VALUE_STR)+" "+ str(Wh_API_NAME) + " = '" + str(RecAttValue) + "' AND PAR_SERVICE_ID = '"+str(service_id)+"' AND FABLOCATION_ID = '"+str(fab_id)+"' AND GREENBOOK = '"+str(TreeParam)+"' "
					else:                                        
						Qustr = " where "+str(ATTRIBUTE_VALUE_STR)+" "+ str(Wh_API_NAME) + " = '" + str(RecAttValue) + "'"

				else:  
					try:     
						RecAttValue = Quote.GetGlobal("contract_quote_record_id")
					except:
						RecAttValue = ''                 
					TreeTopSuperParentParam = Product.GetGlobal("CommonTreeTopSuperParentParam")
					if RECORD_ID == "SYOBJR-95868":                        
						Qury_str = (
							"select top "
							+ str(PerPage)
							+ " "
							+ "SYSEFL."
							+ str(select_obj_str)
							+ ",SYSEFL.CpqTableEntryId from "
							+ str(ObjectName)
							+ " (nolock) INNER JOIN SYSECT (nolock) ON SYSEFL.SECTION_RECORD_ID = SYSECT.RECORD_ID  AND "
							+ str(Wh_API_NAME)
							+ " = '"
							+ str(RecAttValue)
							+ "' "
							+ "where SYSEFL.SECTION_NAME = '"
							+ str(TreeParentParam)
							+ "' "
							+ "where SYSEFL.SECTION_NAME = '"
							+ str(TreeParentParam)
							+ "' ORDER BY abs(SYSEFL.DISPLAY_ORDER)"
						)
						QuryCount_str = (
							"select count(*) as cnt from "
							+ str(ObjectName)
							+ " (nolock) INNER JOIN SYSECT (nolock) ON SYSEFL.SECTION_RECORD_ID = SYSECT.RECORD_ID and "
							+ str(Wh_API_NAME)
							+ " = '"
							+ str(RecAttValue)
							+ "' where SYSEFL.SECTION_NAME = '"
							+ str(TreeParentParam)
							+ "'"
						)                        
					elif RECORD_ID == "SYOBJR-95843" and TreeParentParam != "" :  
						RecAttValue = Product.Attributes.GetByName("QSTN_SYSEFL_SY_03295").GetValue()      
						Qury_str = (
						"select top "
						+ str(PerPage)
						+ " * "
						+ " from "
						+ str(ObjectName)
						+ " (nolock) WHERE "
						+ str(Wh_API_NAME)
						+ " = '"
						+ str(RecAttValue)
						+ "' AND PAGE_NAME = '"
						+ str(TreeParentParam)
						+ "'"
						
						)
						QuryCount_str = (
							"select count(*) as cnt from "
							+ str(ObjectName)
							+ " (nolock) WHERE "
							+ str(Wh_API_NAME)
							+ " = '"
							+ str(RecAttValue)
							+ "' AND PAGE_NAME = '"
							+ str(TreeParentParam)
							+ "'"
						)
					elif RECORD_ID == "SYOBJR-94452":                        
						Wh_API_NAME = "ROLE_RECORD_ID"
						RecAttValue = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00001").GetValue()

						Qustr = " where " + str(Wh_API_NAME) + " = '" + str(RecAttValue) + "'"   
					elif RECORD_ID == "SYOBJR-94489":                        
						GetappValue = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00154").GetValue()
						Qury_str = (
						"select DISTINCT top 10 RECORD_ID,SECTION_NAME,DISPLAY_ORDER,PARENT_SECTION_RECORD_ID,OWNER_RECORD_ID,PRIMARY_OBJECT_RECORD_ID,PAGE_LABEL,PAGE_RECORD_ID,CpqTableEntryId from ( select TOP 10 ROW_NUMBER() OVER(order by DISPLAY_ORDER) AS ROW,* from SYSECT where PAGE_LABEL = '"
						+ str(TreeParentParam)
						+ "') m where m.ROW BETWEEN 1 and 10"
						)
					
						QuryCount_str = (
							"select count(*) as cnt from SYSECT (nolock) where PAGE_LABEL = '" + str(TreeParentParam) + "'"
						)

					elif RECORD_ID == "SYOBJR-93162":
						CommonTreeTopSuperParentParam = Product.GetGlobal("CommonTreeTopSuperParentParam")
						TreeFirstSuperTopParentParam = Product.GetGlobal("CommonTreeFirstSuperTopParentParam")
						CommonTreeParentParam = Product.GetGlobal("CommonTreeParentParam")
						RecAttValue = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00128").GetValue()
						getTabrec = Sql.GetFirst(
							"SELECT TAB_RECORD_ID from SYPRTB where APP_ID = '"
							+ str(TreeFirstSuperTopParentParam)
							+ "' and PROFILE_ID = '"
							+ str(RecAttValue)
							+ "' and TAB_ID = '"
							+ str(CommonTreeTopSuperParentParam)
							+ "'"
						)
						sectrecid = Tabrecordid = ""
						if getTabrec is not None:
							Tabrecordid = str(getTabrec.TAB_RECORD_ID)                            
							getsectrec = Sql.GetFirst(
								"SELECT SECTION_RECORD_ID from SYPRSN where TAB_RECORD_ID = '"
								+ str(Tabrecordid)
								+ "' and SECTION_ID ='"
								+ str(CommonTreeParentParam)
								+ "'"
							)
							if getsectrec is not None:
								sectrecid = str(getsectrec.SECTION_RECORD_ID)
						Qury_str = (
							"select top "
							+ str(PerPage)
							+ " * from ( select ROW_NUMBER() OVER(order by P.SECTION_FIELD_ID ) AS ROW,P.PROFILE_SECTIONFIELD_RECORD_ID,P.SECTIONFIELD_RECORD_ID,P.SECTION_FIELD_ID ,P.VISIBLE,P.EDITABLE,P.PROFILE_RECORD_ID,P.CpqTableEntryId,s.DISPLAY_ORDER from SYPRSF P (nolock)  inner join SYSEFL s on s.RECORD_ID = P.SECTIONFIELD_RECORD_ID where "
							+ str(ATTRIBUTE_VALUE_STR)
							+ " P.PROFILE_ID = '"
							+ str(RecAttValue)
							+ "' and P.SECTION_RECORD_ID = '"
							+ str(sectrecid)
							+ "' ) m where m.ROW BETWEEN "
							+ str(Page_start)
							+ " and "
							+ str(Page_End)
							+ "  order by m.DISPLAY_ORDER"
						)
						QuryCount_str = (
							"select count(*) as cnt from SYPRSF (nolock)  where PROFILE_ID = '"
							+ str(RecAttValue)
							+ "' and SECTION_RECORD_ID = '"
							+ str(sectrecid)
							+ "'"
						)
					elif RECORD_ID == "SYOBJR-95864":
						Qustr1 = (
							" where "
							+ str(Wh_API_NAME)
							+ " = '"
							+ str(RecAttValue)
							+ "' AND ACTIVE = '"
							+ str(TreeParam)
							+ "' "
						)
						Qustr = Qustr1.replace("Active", "True").replace("Inactive", "False")

					elif RECORD_ID == "SYOBJR-94441":                       
						RecAttValue = productAttributesGetByName("QSTN_SYSEFL_SY_00152").GetValue()
						Qustr = " where " + str(Wh_API_NAME) + " = '" + str(RecAttValue) + "'"

					elif RECORD_ID == "SYOBJR-98782":                        
						#RecAttValue = productAttributesGetByName("QSTN_SYSEFL_SY_01110").GetValue()
						#Qustr = " where " + str(Wh_API_NAME) + " = '" + str(RecAttValue) + "'" 
						Qury_str = (
							"select DISTINCT top "
							+ str(PerPage)
							+ " "
							+ str(select_obj_str)
							+ " from ( select ROW_NUMBER() OVER(order by "
							+ str(Wh_API_NAMEs)
							+ ") AS ROW, * from "
							+ str(ObjectName)
							+ " (nolock) where TAB_LABEL = '" + str(TreeParentParam) + "'"
							" ) m where m.ROW BETWEEN " + str(Page_start) + " and " + str(Page_End) + ""
						)
						QuryCount_str = (
							"select count(*) as cnt from "
							+ str(ObjectName)
							+ " (nolock) where TAB_LABEL = '" + str(TreeParentParam) + "'"
						)               
					
					elif RECORD_ID == "SYOBJR-94489":

						GetappValue = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00154").GetValue()

						gettabres = Sql.GetFirst(
							"Select RECORD_ID from SYTABS where APP_LABEL = '"
							+ str(GetappValue)
							+ "' and TAB_LABEL = '"
							+ str(TreeParentParam)
							+ "'"
						)
						if gettabres:

							tabRecord = str(gettabres.RECORD_ID)
						Qustr = " where TAB_RECORD_ID = '" + str(tabRecord) + "'"

					elif RECORD_ID == "SYOBJR-95800":
						RecAttValue = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00128").GetValue()
						permiss_id = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00125").GetValue()
						

						Qury_str = (
							"select DISTINCT TOP "
							+ str(PerPage)
							+ " ID,USERNAME,NAME,ACTIVE from ( select ROW_NUMBER() OVER(order by ID) AS ROW, ID,USERNAME,NAME,ACTIVE from USERS U (nolock) inner join users_permissions up on U.id = up.user_id   where "
							+ str(ATTRIBUTE_VALUE_STR)
							+ " up.permission_id = '"
							+ str(permiss_id)
							+ "'  ) m where m.ROW BETWEEN "
							+ str(Page_start)
							+ " and "
							+ str(Page_End)
							+ ""
						)
						QuryCount_str = (
							"select count(U.ID) as cnt from USERS U (nolock)  inner join users_permissions up on U.id = up.user_id  where  up.permission_id = '"
							+ str(permiss_id)
							+ "'  "
						)
					elif RECORD_ID == "SYOBJR-93121":
						proff_per_id = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00125").GetValue()
						Profile_ID_PERMISSION = Product.GetGlobal("Profile_ID_PERMISSION")                        
						if proff_per_id != "":
							Qury_str = (
								"select top "
								+ str(PerPage)
								+ " PROFILE_APP_RECORD_ID,APP_ID,VISIBLE,[DEFAULT],PROFILE_RECORD_ID, CpqTableEntryId from ( select ROW_NUMBER() OVER( order by APP_ID) AS ROW, PROFILE_APP_RECORD_ID,APP_ID,VISIBLE,[DEFAULT],PROFILE_RECORD_ID, CpqTableEntryId  from SYPRAP (nolock) where PROFILE_RECORD_ID = '"
								+ str(proff_per_id)
								+ "') m where m.ROW BETWEEN "
								+ str(Page_start)
								+ " and "
								+ str(Page_End)
							)
							QuryCount_str = (
								"select count(*) as cnt from "
								+ str(ObjectName)
								+ " (nolock) where  PROFILE_RECORD_ID = '"
								+ str(proff_per_id)
								+ "' "
							)
						else:
							proff_id = Product.GetGlobal("Profile_ID")
							Qury_str = (
								"select top "
								+ str(PerPage)
								+ " PROFILE_APP_RECORD_ID,APP_ID,VISIBLE,[DEFAULT],PROFILE_RECORD_ID, CpqTableEntryId from ( select ROW_NUMBER() OVER( order by APP_ID) AS ROW, PROFILE_APP_RECORD_ID,APP_ID,VISIBLE,[DEFAULT],PROFILE_RECORD_ID, CpqTableEntryId  from SYPRAP (nolock) where PROFILE_RECORD_ID = '"
								+ str(Profile_ID_PERMISSION)
								+ "') m where m.ROW BETWEEN "
								+ str(Page_start)
								+ " and "
								+ str(Page_End)
							)
							QuryCount_str = (
								"select count(*) as cnt from "
								+ str(ObjectName)
								+ " (nolock) where  PROFILE_RECORD_ID = '"
								+ str(Profile_ID_PERMISSION)
								+ "' "
							)
					elif RECORD_ID == "SYOBJR-93159":
						Wh_API_NAME = "PROFILE_ID"
						RecAttValue = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00128").GetValue()
						CommonTreeSuperParentParam = Product.GetGlobal("CommonTreeSuperParentParam")
						appId = Product.GetGlobal("CommonTreeParentParam")                        
						if appId == "App Level Permissions":
							Qury_str = (
								"select top "
								+ str(PerPage)
								+ " *  from ( select ROW_NUMBER() OVER(order by S.DISPLAY_ORDER) AS ROW, p.PROFILE_TAB_RECORD_ID,p.TAB_ID,p.VISIBLE,p.PROFILE_RECORD_ID,p.CpqTableEntryId,S.DISPLAY_ORDER from SYPRTB p (nolock) inner join SYTABS S on S.RECORD_ID = p.TAB_RECORD_ID where "
								+ str(ATTRIBUTE_VALUE_STR)
								+ " p.PROFILE_ID = '"
								+ str(RecAttValue)
								+ "' and p.APP_ID = '"
								+ str(TreeParam)
								+ "' ) m where m.ROW BETWEEN "
								+ str(Page_start)
								+ " and "
								+ str(Page_End)
								+ " order by m.DISPLAY_ORDER"
							)                            
							QuryCount_str = (
								"select count(*) as cnt from SYPRTB (nolock)  where PROFILE_ID = '"
								+ str(RecAttValue)
								+ "' and APP_ID = '"
								+ str(TreeParam)
								+ "'"
							)
						else:
							Qury_str = (
								"select top "
								+ str(PerPage)
								+ " *  from ( select ROW_NUMBER() OVER(order by S.DISPLAY_ORDER) AS ROW, p.PROFILE_TAB_RECORD_ID,p.TAB_ID,p.VISIBLE,p.PROFILE_RECORD_ID,p.CpqTableEntryId,S.DISPLAY_ORDER from SYPRTB p (nolock) inner join SYTABS S on S.RECORD_ID = p.TAB_RECORD_ID where "
								+ str(ATTRIBUTE_VALUE_STR)
								+ " p.PROFILE_ID = '"
								+ str(RecAttValue)
								+ "' and p.APP_ID = '"
								+ str(appId)
								+ "' ) m where m.ROW BETWEEN "
								+ str(Page_start)
								+ " and "
								+ str(Page_End)
								+ " order by m.DISPLAY_ORDER"
							)
							QuryCount_str = (
								"select count(*) as cnt from SYPRTB (nolock)  where PROFILE_ID = '"
								+ str(RecAttValue)
								+ "' and APP_ID = '"
								+ str(appId)
								+ "'"
							)

					elif RECORD_ID == "SYOBJR-93160":
						RecAttValue = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00128").GetValue()
						GetAppname_query = ""
						if TreeTopSuperParentParam == "App Level Permissions":
							CommonTreeSuperParentParam = Product.GetGlobal("CommonTreeSuperParentParam")                            
							GetAppname_query = Sql.GetFirst(
								"SELECT TAB_RECORD_ID FROM SYPRTB where APP_ID = '"
								+ str(CommonTreeSuperParentParam)
								+ "' and TAB_ID = '"
								+ str(TreeParam)
								+ "'"
							)
						else:
							TreeParam = Product.GetGlobal("CommonTreeParentParam")
							GetAppname_query = Sql.GetFirst(
								"SELECT TAB_RECORD_ID FROM SYPRTB where APP_ID = '"
								+ str(TreeTopSuperParentParam)
								+ "' and TAB_ID = '"
								+ str(TreeParam)
								+ "'"
							)
						Qury_str = (
							"select top "
							+ str(PerPage)
							+ " *  from ( select ROW_NUMBER() OVER(order by P.PROFILE_RECORD_ID) AS ROW, P.PROFILE_SECTION_RECORD_ID,P.SECTION_RECORD_ID,P.SECTION_ID,P.TAB_ID,P.VISIBLE,P.PROFILE_RECORD_ID,P.CpqTableEntryId,s.DISPLAY_ORDER from SYPRSN P (nolock) inner join SYSECT s on s.RECORD_ID = P.SECTION_RECORD_ID where "
							+ str(ATTRIBUTE_VALUE_STR)
							+ " P.PROFILE_ID = '"
							+ str(RecAttValue)
							+ "' and P.TAB_ID = '"
							+ str(TreeParam)
							+ "' and P.TAB_RECORD_ID ='"
							+ str(GetAppname_query.TAB_RECORD_ID)
							+ "' ) m where m.ROW BETWEEN "
							+ str(Page_start)
							+ " and "
							+ str(Page_End)
							+ "  order by m.DISPLAY_ORDER"
						)

						QuryCount_str = (
							"select count(*) as cnt from SYPRSN (nolock)  where PROFILE_ID = '"
							+ str(RecAttValue)
							+ "' and TAB_ID = '"
							+ str(TreeParam)
							+ "' and TAB_RECORD_ID ='"
							+ str(GetAppname_query.TAB_RECORD_ID)
							+ "'"
						)                    
					elif RECORD_ID == "SYOBJR-98784":
						gettabval = getptabname = ""
						CommonTreeTopSuperParentParam = Product.GetGlobal("CommonTreeTopSuperParentParam")
						GetappValue = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00154").GetValue()
						gettabval = Sql.GetFirst(
							"Select RECORD_ID,PAGE_NAME,TAB_LABEL from SYTABS where PAGE_NAME = '"
							+ str(TreeParentParam)
							+ "' and TAB_LABEL = '"
							+ str(TopTreeSuperParentParam)
							+ "'"
						)                        
						if gettabval:
							getptabname = gettabval.RECORD_ID
						Qustr = " where TAB_RECORD_ID = '" + str(getptabname) + "'"
					elif RECORD_ID == "SYOBJR-94490":
						GetappValue = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00154").GetValue()                        
						gettabres = Sql.GetFirst(
							"Select RECORD_ID from SYSECT where PAGE_NAME = '"
							+ str(TopTreeSuperParentParam)
							+ "' and SECTION_NAME = '"
							+ str(TreeParentParam)
							+ "'"
						)
						if gettabres:                            
							tabRecord = str(gettabres.RECORD_ID)

						Qustr = " where SECTION_RECORD_ID = '" + str(tabRecord) + "'"

					else:
						TreeParam = Product.GetGlobal("TreeParam")
						TreeParentParam = Product.GetGlobal("TreeParentLevel0") 
						TreeSuperParentParam = Product.GetGlobal("TreeParentLevel1")                                               
						PLN_ID = Product.GetGlobal("PLN_ID")
						if PLN_ID != "":
							PLN_ID = PLN_ID.split("-")[1]
						SORG_ID = Product.GetGlobal("SORG_ID")
						if SORG_ID != "":
							SORG_ID = SORG_ID.split("-")[1]                        
						if RECORD_ID == "SYOBJR-93122":
							RecAttValue = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00128").GetValue()

							Qury_str = (
								"select  top "
								+ str(PerPage)
								+ "  PROFILE_OBJECT_RECORD_ID,OBJECT_RECORD_ID, OBJECT_NAME, VISIBLE,CpqTableEntryId from ( select ROW_NUMBER() OVER( order by OBJECT_NAME) AS ROW,  PROFILE_OBJECT_RECORD_ID,OBJECT_RECORD_ID, OBJECT_NAME, VISIBLE,CpqTableEntryId from SYPROH (nolock) where "
								+ str(ATTRIBUTE_VALUE_STR)
								+ " PROFILE_ID = '"
								+ str(RecAttValue)
								+ "') m where m.ROW BETWEEN "
								+ str(Page_start)
								+ " and "
								+ str(Page_End)
								+ " order by OBJECT_NAME"
							)
							QuryCount_str = (
								"select count(*) as cnt from SYPROH (nolock) where  PROFILE_ID = '" + str(RecAttValue) + "' "
							)

						elif str(RECORD_ID) == "SYOBJR-94454" or str(RECORD_ID) == "SYOBJR-94455":
							Qury_str = (
								"select DISTINCT top "
								+ str(PerPage)
								+ " "
								+ str(select_obj_str)
								+ " from ( select ROW_NUMBER() OVER(order by "
								+ str(Wh_API_NAMEs)
								+ ") AS ROW, * from "
								+ str(ObjectName)
								+ " (nolock) where "
								+ str(Wh_API_NAME)
								+ " = '"
								+ str(RecAttValue)
								+ "' "
								" ) m where m.ROW BETWEEN " + str(Page_start) + " and " + str(Page_End) + ""
							)
							QuryCount_str = (
								"select count(*) as cnt from "
								+ str(ObjectName)
								+ " (nolock) where "
								+ str(Wh_API_NAME)
								+ " = '"
								+ str(RecAttValue)
								+ "' "
							)                        
						elif str(RECORD_ID) == "SYOBJR-98795":                            
							TreeParam = Product.GetGlobal("TreeParam")
							TreeParentParam = Product.GetGlobal("TreeParentLevel0")
							contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
							qt_rec_id = Sql.GetFirst("SELECT QUOTE_ID FROM SAQTSV WHERE QUOTE_RECORD_ID ='" + str(
								contract_quote_record_id) + "' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"'")							  
							LineAndEquipIDList = TreeParam.split(' - ')
							
							if getyears == 1:
								col_year =  'YEAR_1'
							elif getyears == 2:
								col_year =  'YEAR_1,YEAR_2'
							elif getyears == 3:
								col_year =  'YEAR_1,YEAR_2,YEAR_3'
							elif getyears == 4:
								col_year =  'YEAR_1,YEAR_2,YEAR_3,YEAR_4'
							else:
								col_year = 'YEAR_1,YEAR_2,YEAR_3,YEAR_4,YEAR_5'
							if TreeParam == "Quote Preview":                                
								Qury_str = (
								"select top "
									+ str(PerPage)
									+ " QUOTE_ITEM_COVERED_OBJECT_RECORD_ID, EQUIPMENT_LINE_ID, EQUIPMENT_ID,SERVICE_ID,LINE_ITEM_ID,BD_DISCOUNT,BD_PRICE_MARGIN,DISCOUNT,YEAR_OVER_YEAR,"+col_year+",SERIAL_NO, GREENBOOK,FABLOCATION_ID, LINE,TARGET_PRICE_MARGIN, SALES_DISCOUNT_PRICE, SALDIS_PERCENT, NET_VALUE,PRICE_BENCHMARK_TYPE,TOOL_CONFIGURATION,ANNUAL_BENCHMARK_BOOKING_PRICE,CONTRACT_ID,CONVERT(VARCHAR(10),CONTRACT_VALID_FROM,101) AS [CONTRACT_VALID_FROM],CONVERT(VARCHAR(10),CONTRACT_VALID_TO,101) AS [CONTRACT_VALID_TO],BENCHMARKING_THRESHOLD,CpqTableEntryId from ( select  ROW_NUMBER() OVER( ORDER BY EQUIPMENT_LINE_ID) AS ROW, * from SAQICO (NOLOCK) where QUOTE_ID = '"
									+ str(qt_rec_id.QUOTE_ID)
									+ "' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"') m where m.ROW BETWEEN "
									+ str(Page_start)
									+ " and "
									+ str(Page_End)
								)
								QuryCount_str = (
										"select count(*) as cnt FROM SAQICO where QUOTE_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(
											str(qt_rec_id.QUOTE_ID),quote_revision_record_id)
								)
						elif str(RECORD_ID) == "SYOBJR-91822":
							contractrecid = Product.GetGlobal("contract_record_id")
							
							if Product.GetGlobal("TreeParentLevel1") == "Cart Items":
								imgstr = '<img title="Acquired" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Green_Tick.svg>'
								acquiring_img_str = '<img title="Acquiring" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Cloud_Icon.svg>'
								TreeParentParam = Product.GetGlobal("TreeParentLevel0")
								ServiceId = TreeParentParam.split("-")[1].strip()                           
								Qury_str = (
										"SELECT DISTINCT TOP "
										+ str(PerPage)
										+ " CASE WHEN DISCOUNT = 'ACQUIRED' THEN '"+ imgstr +"' ELSE '"+ imgstr +"' END AS EQUIPMENT_STATUS, CONTRACT_ITEM_COVERED_OBJECT_RECORD_ID,EQUIPMENT_LINE_ID,SERVICE_ID,EQUIPMENT_ID,SERIAL_NO,GREENBOOK,TOTAL_COST,LINE_ITEM_ID,DISCOUNT,TAX,EXTENDED_PRICE,EQUIPMENT_RECORD_ID,SERVICE_RECORD_ID,FABLOCATION_RECORD_ID,EQUIPMENTCATEGORY_RECORD_ID,CONTRACT_RECORD_ID,MNT_PLANT_RECORD_ID,SALESORG_RECORD_ID,GREENBOOK_RECORD_ID,CpqTableEntryId from ( select ROW_NUMBER() OVER(order by "+ str(Wh_API_NAMEs) +") AS ROW, * from CTCICO (nolock)  where "+ str(ATTRIBUTE_VALUE_STR)+" CONTRACT_RECORD_ID ='"+str(RecAttValue)
										+"' and GREENBOOK = '"+str(TreeParam)+"' and SERVICE_ID = '"+str(ServiceId)+"') m where m.ROW BETWEEN "
										+ str(Page_start)
										+ " AND "
										+ str(Page_End)
									)

								QuryCount_str = (
									"SELECT COUNT(CpqTableEntryId) AS cnt FROM CTCICO (nolock) WHERE "+ str(ATTRIBUTE_VALUE_STR)+" CONTRACT_RECORD_ID = '"
										+ str(RecAttValue)
										+ "'and GREENBOOK = '"+str(TreeParam)+"'and SERVICE_ID = '"+str(ServiceId)+"'"
								)                                
							else:
								imgstr = '<img title="Acquired" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Green_Tick.svg>'
								acquiring_img_str = '<img title="Acquiring" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Cloud_Icon.svg>'
								qt_rec_id = SqlHelper.GetFirst("SELECT CONTRACT_ID FROM CTCTSV WHERE CONTRACT_RECORD_ID='" + str(
								contractrecid) + "'")
								LineAndEquipIDList = TreeParam.split(' - ')
								if TreeParentParam == "Cart Items":
									Qury_str = (
										"select top "
											+ str(PerPage)
											+ " CASE WHEN DISCOUNT = 'ACQUIRED' THEN '"+ imgstr +"' ELSE '"+ imgstr +"' END AS EQUIPMENT_STATUS, CONTRACT_ITEM_COVERED_OBJECT_RECORD_ID,EQUIPMENT_LINE_ID,SERVICE_ID,EQUIPMENT_ID,SERIAL_NO,GREENBOOK,TOTAL_COST,LINE_ITEM_ID,DISCOUNT,TAX,EXTENDED_PRICE,EQUIPMENT_RECORD_ID,SERVICE_RECORD_ID,FABLOCATION_RECORD_ID,EQUIPMENTCATEGORY_RECORD_ID,CONTRACT_RECORD_ID,MNT_PLANT_RECORD_ID,SALESORG_RECORD_ID,GREENBOOK_RECORD_ID,CpqTableEntryId from ( select  ROW_NUMBER() OVER( ORDER BY EQUIPMENT_LINE_ID) AS ROW, * from CTCICO (NOLOCK) where "+ str(ATTRIBUTE_VALUE_STR)+" CONTRACT_ID = '"
											+ str(qt_rec_id.CONTRACT_ID)
											+ "' AND SERVICE_ID = '"
											+ str(LineAndEquipIDList[1])
											+ "') m where m.ROW BETWEEN "
											+ str(Page_start)
											+ " and "
											+ str(Page_End)
									)
									QuryCount_str = (
											"select count(*) as cnt FROM CTCICO where "+ str(ATTRIBUTE_VALUE_STR)+" SERVICE_ID = '{}' and CONTRACT_ID = '{}'".format(
												LineAndEquipIDList[1], str(qt_rec_id.CONTRACT_ID))
									)
								else:
									Qury_str = (
										"select top "
											+ str(PerPage)
											+ " * from ( select  ROW_NUMBER() OVER( ORDER BY EQUIPMENT_LINE_ID) AS ROW, * from CTCICO (NOLOCK) where "+ str(ATTRIBUTE_VALUE_STR)+" CONTRACT_ID = '"
											+ str(qt_rec_id.CONTRACT_ID)
											+ "' AND SERVICE_ID = '"
											+ str(LineAndEquipIDList[1])
											+ "') m where m.ROW BETWEEN "
											+ str(Page_start)
											+ " and "
											+ str(Page_End)
									)
									QuryCount_str = (
											"select count(*) as cnt FROM CTCICO where "+ str(ATTRIBUTE_VALUE_STR)+" SERVICE_ID = '{}' and CONTRACT_ID = '{}'".format(
												LineAndEquipIDList[1], str(qt_rec_id.CONTRACT_ID))
									)  
						elif str(RECORD_ID) == "SYOBJR-00009":
							if Quote.GetCustomField('PRICING_PICKLIST').Content == '':
								Quote.GetCustomField('PRICING_PICKLIST').Content = 'Document Currency'
							if getyears == 1:
								col_year =  'YEAR_1'
							elif getyears == 2:
								col_year =  'YEAR_1,YEAR_2'
							elif getyears == 3:
								col_year =  'YEAR_1,YEAR_2,YEAR_3'
							elif getyears == 4:
								col_year =  'YEAR_1,YEAR_2,YEAR_3,YEAR_4'
							else:
								col_year = 'YEAR_1,YEAR_2,YEAR_3,YEAR_4,YEAR_5'        
							if Product.GetGlobal("TreeParentLevel2") == "Quote Items":
								imgstr = '<img title="Acquired" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Green_Tick.svg>'
								acquiring_img_str = '<img title="Acquiring" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Cloud_Icon.svg>'
								exclamation = '<img title="Approval Required" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/clock_exe.svg>'
								error = '<img title="Error" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/exclamation_icon.svg>'
								partially_priced = '<img title="Partially Priced" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Red1_Circle.svg>'
								assembly_missing = '<img title="Assembly Missing" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Orange1_Circle.svg>'
								TreeParentParam = Product.GetGlobal("TreeParentLevel1")
								
								try:
									if str(TreeParentParam.split("-")[4]):
										ServiceId = TreeParentParam.split("-")[-3].strip()
								except:
									ServiceId = TreeParentParam.split("-")[1].strip()                            
								Qury_str = ("SELECT DISTINCT TOP " + str(PerPage) + " CASE WHEN STATUS = 'ACQUIRED' THEN '"+ imgstr +"' WHEN STATUS = 'APPROVAL REQUIRED' THEN '"+ exclamation +"' WHEN STATUS = 'ON HOLD - COSTING' THEN '"+ error +"' WHEN STATUS = 'ERROR' THEN '"+ error +"' WHEN STATUS = 'PARTIALLY PRICED' THEN '"+ partially_priced +"' WHEN STATUS = 'ASSEMBLY IS MISSING' THEN '"+ assembly_missing +"' ELSE '"+ acquiring_img_str +"' END AS STATUS, QUOTE_ITEM_COVERED_OBJECT_RECORD_ID,SERVICE_ID,EQUIPMENT_ID,SERIAL_NO,TARGET_PRICE_MARGIN,GREENBOOK,FABLOCATION_ID,TECHNOLOGY,KPU,TARGET_PRICE,SALDIS_PERCENT,NET_VALUE,EQUIPMENT_RECORD_ID,SERVICE_RECORD_ID,FABLOCATION_RECORD_ID,LINE_ITEM_ID,BD_DISCOUNT,BD_PRICE_MARGIN,DISCOUNT,YEAR_OVER_YEAR,YEAR_1,YEAR_2,BD_DISCOUNT_RECORD_ID,EQUIPMENTCATEGORY_RECORD_ID,QUOTE_RECORD_ID,QTEREV_RECORD_ID,MNT_PLANT_RECORD_ID,SALESORG_RECORD_ID,SALES_DISCOUNT_PRICE,GREENBOOK_RECORD_ID,PRICE_BENCHMARK_TYPE,TOOL_CONFIGURATION,ANNUAL_BENCHMARK_BOOKING_PRICE,CONTRACT_ID,CONVERT(VARCHAR(10),CONTRACT_VALID_FROM,101) AS [CONTRACT_VALID_FROM],CONVERT(VARCHAR(10),CONTRACT_VALID_TO,101) AS [CONTRACT_VALID_TO],BENCHMARKING_THRESHOLD,CpqTableEntryId from ( select ROW_NUMBER() OVER(order by EQUIPMENT_LINE_ID) AS ROW, * from SAQICO (nolock)  where QUOTE_RECORD_ID ='"+str(RecAttValue) +"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' and GREENBOOK = '"+str(TreeParam)+"' and SERVICE_ID = '"+str(ServiceId)+"' and FABLOCATION_ID = '"+str(Product.GetGlobal("TreeParentLevel0"))+"') m where m.ROW BETWEEN " + str(Page_start) + " AND " + str(Page_End) )
								
								QuryCount_str = (
									"SELECT COUNT(CpqTableEntryId) AS cnt FROM SAQICO (nolock) WHERE QUOTE_RECORD_ID = '"
										+ str(RecAttValue)
										+ "' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' and GREENBOOK = '"+str(TreeParam)+"' and SERVICE_ID = '"+str(ServiceId)+"' and FABLOCATION_ID = '"+str(Product.GetGlobal("TreeParentLevel0"))+"' "
								)    
							else:
								imgstr = '<img title="Acquired" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Green_Tick.svg>'
								acquiring_img_str = '<img title="Acquiring" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Cloud_Icon.svg>'
								exclamation = '<img title="Approval Required" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/clock_exe.svg>'
								error = '<img title="Error" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/exclamation_icon.svg>'
								partially_priced = '<img title="Partially Priced" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Red1_Circle.svg>'
								assembly_missing = '<img title="Assembly Missing" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Orange1_Circle.svg>'
								qt_rec_id = Sql.GetFirst("SELECT QUOTE_ID FROM SAQTSV (NOLOCK) WHERE QUOTE_RECORD_ID ='" + str(
								contract_quote_record_id) + "' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' ")
								if TreeParam == "Quote Items":
									Trace.Write("c1")
									##A055S000P01-4578 strts
									#Trace.Write('xchk--')
									saqico_cols =""
									#pricing_curr = pricing_picklist_value
										
									# if pricing_picklist_value == 'Document Currency':
									# 	saqico_cols ="CEILING_PRICE, MODEL_PRICE, NET_PRICE, NET_VALUE, TARGET_PRICE, SALES_DISCOUNT_PRICE,TAX_AMOUNT, "+col_year
									# 	Trace.Write('DocumentCurr----'+str(saqico_cols)) 
									# else:
									# 	##Global Currency
									# 	gl_str = "_INGL_CURR"
									# 	col_year = col_year.split(',')
									# 	col_year = ','.join([i+gl_str for i in col_year])
									# 	saqico_cols ="CEILING_PRICE_INGL_CURR, MODEL_PRICE_INGL_CURR, NET_PRICE_INGL_CURR, NET_VALUE_INGL_CURR, TARGET_PRICE_INGL_CURR, SLSDIS_PRICE_INGL_CURR,TAX_AMOUNT_INGL_CURR, "+col_year
									# 	Trace.Write('GlobalCurr----'+str(saqico_cols))
									# Qury_str = (
									# 	"select top "
									# 		+ str(PerPage)
									# 		+ " CASE WHEN STATUS = 'ACQUIRED' THEN '"+ imgstr +"' WHEN STATUS = 'APPROVAL REQUIRED' THEN '" +exclamation+ "' WHEN STATUS = 'ON HOLD - COSTING' THEN '"+ error +"' WHEN STATUS = 'ERROR' THEN '"+ error +"'  WHEN STATUS = 'PARTIALLY PRICED' THEN '"+ partially_priced +"' WHEN STATUS = 'ASSEMBLY MISSING' THEN '"+ assembly_missing +"'  ELSE '"+ acquiring_img_str +"' END AS STATUS, QUOTE_ITEM_COVERED_OBJECT_RECORD_ID, EQUIPMENT_LINE_ID, EQUIPMENT_ID,SERVICE_ID,LINE_ITEM_ID,BD_DISCOUNT,BD_PRICE_MARGIN,DISCOUNT,YEAR_OVER_YEAR,SERIAL_NO, "+saqico_cols+", GREENBOOK,FABLOCATION_ID,TECHNOLOGY,KPU, TARGET_PRICE_MARGIN,++ SALDIS_PERCENT,SRVTAXCLA_DESCRIPTION,TAX_PERCENTAGE, PRICE_BENCHMARK_TYPE,TOOL_CONFIGURATION,ANNUAL_BENCHMARK_BOOKING_PRICE,CONTRACT_ID,CONVERT(VARCHAR(10),CONTRACT_VALID_FROM,101) AS [CONTRACT_VALID_FROM],CONVERT(VARCHAR(10),CONTRACT_VALID_TO,101) AS [CONTRACT_VALID_TO],BENCHMARKING_THRESHOLD,CpqTableEntryId,ASSEMBLY_ID,TOTAL_COST_WOSEEDSTOCK,TOTAL_COST_WSEEDSTOCK from ( select  ROW_NUMBER() OVER( ORDER BY "+ str(Wh_API_NAMEs)
									# 		+") AS ROW, * from SAQICO (NOLOCK) where  QUOTE_ID = '"
									# 		+ str(qt_rec_id.QUOTE_ID)
									# 		+ "' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"') m where m.ROW BETWEEN "
									# 		+ str(Page_start)
									# 		+ " and "
									# 		+ str(Page_End)+" ORDER BY "+ str(Wh_API_NAMEs)
									# )
									Qury_str = (
										"select top "
											+ str(PerPage)
											+ " CASE WHEN STATUS = 'ACQUIRED' THEN '"+ imgstr +"' WHEN STATUS = 'APPROVAL REQUIRED' THEN '" +exclamation+ "' WHEN STATUS = 'ON HOLD - COSTING' THEN '"+ error +"' WHEN STATUS = 'ERROR' THEN '"+ error +"'  WHEN STATUS = 'PARTIALLY PRICED' THEN '"+ partially_priced +"' WHEN STATUS = 'ASSEMBLY IS MISSING' THEN '"+ assembly_missing +"'  ELSE '"+ acquiring_img_str +"' END AS STATUS, QUOTE_ITEM_COVERED_OBJECT_RECORD_ID,SERVICE_ID,FABLOCATION_ID,GREENBOOK,OBJECT_ID,OBJECT_TYPE,QUANTITY,EQUIPMENT_ID,GOT_CODE,ASSEMBLY_ID,PM_ID,PM_LABOR_LEVEL,KIT_NAME,KIT_NUMBER,KPU,TOOL_CONFIGURATION,SSCM_PM_FREQUENCY,ADJ_PM_FREQUENCY,CEILING_PRICE_INGL_CURR,TARGET_PRICE_INGL_CURR,SLSDIS_PRICE_INGL_CURR,BD_PRICE_INGL_CURR,DISCOUNT,SALES_PRICE_INGL_CURR,YEAR_OVER_YEAR,YEAR,CONVERT(VARCHAR(10),CONTRACT_VALID_FROM,101) AS [CONTRACT_VALID_FROM],CONVERT(VARCHAR(10),CONTRACT_VALID_TO,101) AS [CONTRACT_VALID_TO],CONVERT(VARCHAR(10),WARRANTY_START_DATE,101) AS [WARRANTY_START_DATE],CONVERT(VARCHAR(10),WARRANTY_END_DATE,101) AS [WARRANTY_END_DATE],CNTCST_INGL_CURR,CNTPRI_INGL_CURR,CpqTableEntryId from ( select  ROW_NUMBER() OVER( ORDER BY "+ str(Wh_API_NAMEs)
											+") AS ROW, * from SAQICO (NOLOCK) where  QUOTE_ID = '"
											+ str(qt_rec_id.QUOTE_ID)
											+ "' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"') m where m.ROW BETWEEN "
											+ str(Page_start)
											+ " and "
											+ str(Page_End)+" ORDER BY "+ str(Wh_API_NAMEs)
									)
									##A055S000P01-4578 ends
									QuryCount_str = (
											"select count(*) as cnt FROM SAQICO (NOLOCK) where  QUOTE_ID = '"+str(qt_rec_id.QUOTE_ID)+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"'")
								elif TreeParentParam == "Quote Items": 
									try:
										if str(TreeParam.split("-")[3]):
											LineAndEquipIDList = TreeParam.split(' - ')[-2].strip()
										else:
											LineAndEquipIDList = TreeParam.split(' - ')[1].strip() 
									except:
										LineAndEquipIDList = TreeParam.split('-')[1].strip()
									Qury_str = (
										"select top "
											+ str(PerPage)
											+ " CASE  WHEN STATUS = 'ACQUIRED' THEN '"+ imgstr +"' WHEN STATUS = 'APPROVAL REQUIRED' THEN '" +exclamation+ "' WHEN STATUS = 'ON HOLD - COSTING' THEN '"+ error +"' WHEN STATUS = 'ERROR' THEN '"+ error +"' WHEN STATUS = 'PARTIALLY PRICED' THEN '"+ partially_priced +"' WHEN STATUS = 'ASSEMBLY IS MISSING' THEN '"+ assembly_missing +"' ELSE '"+ acquiring_img_str +"' END AS STATUS, QUOTE_ITEM_COVERED_OBJECT_RECORD_ID, EQUIPMENT_LINE_ID, SERVICE_ID, EQUIPMENT_ID,LINE_ITEM_ID,BD_DISCOUNT,BD_PRICE_MARGIN,DISCOUNT,YEAR_OVER_YEAR,YEAR_1, SERIAL_NO,GREENBOOK,FABLOCATION_ID,TECHNOLOGY,KPU,MODEL_PRICE, SALES_DISCOUNT_PRICE, TARGET_PRICE_MARGIN, SALDIS_PERCENT,NET_VALUE,PRICE_BENCHMARK_TYPE,TOOL_CONFIGURATION,ANNUAL_BENCHMARK_BOOKING_PRICE,CONTRACT_ID,CONVERT(VARCHAR(10),CONTRACT_VALID_FROM,101) AS [CONTRACT_VALID_FROM],CONVERT(VARCHAR(10),CONTRACT_VALID_TO,101) AS [CONTRACT_VALID_TO],BENCHMARKING_THRESHOLD,CpqTableEntryId from ( select  ROW_NUMBER() OVER( ORDER BY "+ str(Wh_API_NAMEs)
											+") AS ROW, * from SAQICO (NOLOCK) where  QUOTE_ID = '"
											+ str(qt_rec_id.QUOTE_ID)
											+ "' AND SERVICE_ID = '"
											+ str(LineAndEquipIDList)
											+ "' and LINE_ITEM_ID = '"+str(TreeParam.split(' -')[0])+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"') m where m.ROW BETWEEN "
											+ str(Page_start)
											+ " and "
											+ str(Page_End)
									)
									QuryCount_str = (
											"select count(*) as cnt FROM SAQICO (NOLOCK) where SERVICE_ID = '"+ str(LineAndEquipIDList) + "' and QUOTE_ID = '"+str(qt_rec_id.QUOTE_ID)+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' and LINE_ITEM_ID = '"+str(TreeParam.split(' -')[0])+"'"
									)
								elif TreeSuperParentParam == "Quote Items":                                    
									LineAndEquipIDList = TreeParentParam.split('-')[1].strip()
									Qury_str = (
										"select top "
											+ str(PerPage)
											+ " CASE  WHEN STATUS = 'ACQUIRED' THEN '"+ imgstr +"' WHEN STATUS = 'APPROVAL REQUIRED' THEN '" +exclamation+ "' WHEN STATUS = 'ON HOLD - COSTING' THEN '"+ error +"' WHEN STATUS = 'ERROR' THEN '"+ error +"' WHEN STATUS = 'PARTIALLY PRICED' THEN '"+ partially_priced +"' WHEN STATUS = 'ASSEMBLY IS MISSING' THEN '"+ assembly_missing +"' ELSE '"+ acquiring_img_str +"' END AS STATUS, QUOTE_ITEM_COVERED_OBJECT_RECORD_ID, EQUIPMENT_LINE_ID, SERVICE_ID, EQUIPMENT_ID,LINE_ITEM_ID,BD_DISCOUNT,BD_PRICE_MARGIN,DISCOUNT,YEAR_OVER_YEAR,YEAR_1, SERIAL_NO,GREENBOOK,FABLOCATION_ID,TECHNOLOGY,KPU, TARGET_PRICE, SALES_DISCOUNT_PRICE, TARGET_PRICE_MARGIN, CEILING_PRICE, SALDIS_PERCENT, NET_VALUE,PRICE_BENCHMARK_TYPE,TOOL_CONFIGURATION,ANNUAL_BENCHMARK_BOOKING_PRICE,CONTRACT_ID,CONVERT(VARCHAR(10),CONTRACT_VALID_FROM,101) AS [CONTRACT_VALID_FROM],CONVERT(VARCHAR(10),CONTRACT_VALID_TO,101) AS [CONTRACT_VALID_TO],BENCHMARKING_THRESHOLD,CpqTableEntryId from ( select  ROW_NUMBER() OVER( ORDER BY "+ str(Wh_API_NAMEs)
											+") AS ROW, * from SAQICO (NOLOCK) where  QUOTE_ID = '"
											+ str(qt_rec_id.QUOTE_ID)
											+ "' AND SERVICE_ID = '"
											+ str(LineAndEquipIDList)
											+ "' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' AND FABLOCATION_ID = '"+str(TreeParam)+"' and LINE_ITEM_ID = '"+str(TreeParentParam.split(' -')[0])+"') m where m.ROW BETWEEN "
											+ str(Page_start)
											+ " and "
											+ str(Page_End)
									)
									QuryCount_str = (
											"select count(*) as cnt FROM SAQICO (NOLOCK) where SERVICE_ID = '"+ str(LineAndEquipIDList)+"' and FABLOCATION_ID = '"+str(TreeParam)+"'  and QUOTE_ID = '"+ str(qt_rec_id.QUOTE_ID)+ "' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' and LINE_ITEM_ID = '"+str(TreeParentParam.split(' -')[0])+"'".format(
												LineAndEquipIDList[1],str(TreeParam) ,str(qt_rec_id.QUOTE_ID)))
						elif str(RECORD_ID) == 'SYOBJR-98799':
							contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
							qt_rec_id = Sql.GetFirst("SELECT QUOTE_ID FROM SAQTSV WHERE QUOTE_RECORD_ID ='" + str(
							contract_quote_record_id) + "' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' ")
							try:
								quote_id = qt_rec_id.QUOTE_ID
							except:
								quote_id = ""
							imgstr = '<img title="Acquired" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Green_Tick.svg>'
							acquiring_img_str = '<img title="Acquiring" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Cloud_Icon.svg>'
							Qury_str = (
										"select top "
											+ str(PerPage)
											+ " CASE WHEN STATUS = 'ACQUIRED' THEN '"+ imgstr +"' ELSE '"+ acquiring_img_str +"' END AS STATUS, QUOTE_DOCUMENT_RECORD_ID, DOCUMENT_ID,DOCUMENT_NAME,LANGUAGE_ID,LANGUAGE_NAME,CPQTABLEENTRYDATEADDED,QUOTE_RECORD_ID,QTEREV_RECORD_ID,CpqTableEntryId from ( select  ROW_NUMBER() OVER( ORDER BY STATUS) AS ROW, * from SAQDOC (NOLOCK) where QUOTE_ID = '"
											+ str(qt_rec_id.QUOTE_ID)
											+ "' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"') m where m.ROW BETWEEN "
											+ str(Page_start)
											+ " and "
											+ str(Page_End)
									)
							QuryCount_str = (
									"select count(*) as cnt FROM SAQDOC (NOLOCK) where QUOTE_ID = '{}' AND QTEREV_RECORD_ID='{}'".format(
										str(qt_rec_id.QUOTE_ID),quote_revision_record_id)
							)                        
						elif str(RECORD_ID) == "SYOBJR-00015" and str(TreeParentParam) == "Approval Chain Steps":
							Qury_str = (
								" SELECT TOP "
								+ str(PerPage)
								+ " * FROM (SELECT ROW_NUMBER() OVER(ORDER BY APPROVAL_TRACKED_FIELD_RECORD_ID) AS ROW,APPROVAL_TRACKED_FIELD_RECORD_ID,TRKOBJ_TRACKEDFIELD_LABEL,TRKOBJ_NAME,TRACKING_TYPE,ACAPTF.CpqTableEntryId FROM ACAPTF (NOLOCK) INNER JOIN ACACST (NOLOCK) ON ACAPTF.APRCHNSTP_RECORD_ID = ACACST.APPROVAL_CHAIN_STEP_RECORD_ID WHERE ACACST.APRCHN_RECORD_ID = '"
								+ str(RecAttValue)
								+ "' AND ACACST.APRCHNSTP_NAME = '"
								+ str(TreeParam).split(': ')[1]
								+ "' )m where m.ROW BETWEEN "
								+ str(Page_start)
								+ " and "
								+ str(Page_End)
								+ " "
							)

							QuryCount_str = (
								"SELECT COUNT(APPROVAL_TRACKED_FIELD_RECORD_ID) AS cnt FROM ACAPTF (NOLOCK) INNER JOIN ACACST (NOLOCK) ON ACAPTF.APRCHNSTP_RECORD_ID = ACACST.APPROVAL_CHAIN_STEP_RECORD_ID WHERE ACACST.APRCHN_RECORD_ID = '"
								+ str(RecAttValue)
								+ "' AND ACACST.APRCHNSTP_NAME = '"
								+ str(TreeParam).split(': ')[1]
								+ "' "
							)    
						elif str(RECORD_ID) == "SYOBJR-00014":
							step_name = TreeParam.split(':')[1].strip()
							Qury_str = (
								"select top "
								+ str(PerPage)
								+ " * from ( select ROW_NUMBER() OVER( order by APPROVAL_CHAIN_STEP_APPROVER_RECORD_ID) AS ROW,ACACSA.APPROVAL_CHAIN_STEP_APPROVER_RECORD_ID,ACACSA.APRCHN_ID,ACACSA.APRCHNSTP_APPROVER_ID,ACACSA.APPROVER_SELECTION_METHOD,ACACSA.USERNAME,ACACSA.PROFILE_ID,ACACSA.ROLE_ID,ACACSA.NOTIFICATION_ONLY,ACACSA.CpqTableEntryId from ACACSA (nolock) INNER JOIN ACACST (NOLOCK) ON ACACST.APPROVAL_CHAIN_STEP_RECORD_ID = ACACSA.APRCHNSTP_RECORD_ID WHERE  ACACSA."
								+ str(Wh_API_NAME)
								+ " = '"
								+ str(RecAttValue)
								+ "' AND ACACST.APRCHNSTP_NAME = '"
								+ str(step_name)
								+ "') m where m.ROW BETWEEN "
								+ str(Page_start)
								+ " AND "
								+ str(Page_End)
								+ ""
							)
							QuryCount_str = (
								"select count(ACACSA.CpqTableEntryId) as cnt from ACACSA (nolock) INNER JOIN ACACST (NOLOCK) ON ACACST.APPROVAL_CHAIN_STEP_RECORD_ID = ACACSA.APRCHNSTP_RECORD_ID WHERE ACACSA."
								+ str(Wh_API_NAME)
								+ " = '"
								+ str(RecAttValue)
								+ "' AND ACACST.APRCHNSTP_NAME = '"
								+ str(step_name)
								+ "'"
							)    
						elif str(RECORD_ID) == "SYOBJR-98822":     
							if Product.GetGlobal("TreeParentLevel1") == "Cart Items":                                
								imgstr = '<img title="Acquired" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Green_Tick.svg>'
								acquiring_img_str = '<img title="Acquiring" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Cloud_Icon.svg>'
								
								Qury_str = (
										"SELECT DISTINCT TOP "
										+ str(PerPage)
										+ " CASE WHEN DISCOUNT = 'ACQUIRED' THEN '"+ imgstr +"' ELSE '"+ imgstr +"' END AS EQUIPMENT_STATUS, CONTRACT_ITEM_COVERED_OBJECT_RECORD_ID,EQUIPMENT_LINE_ID,SERVICE_ID,EQUIPMENT_ID,SERIAL_NO,GREENBOOK,TOTAL_COST,LINE_ITEM_ID,DISCOUNT,TAX,EXTENDED_PRICE,EQUIPMENT_RECORD_ID,SERVICE_RECORD_ID,FABLOCATION_RECORD_ID,EQUIPMENTCATEGORY_RECORD_ID,CONTRACT_RECORD_ID,MNT_PLANT_RECORD_ID,SALESORG_RECORD_ID,GREENBOOK_RECORD_ID,CONTRACT_CURRENCY,CONTRACT_CURRENCY_RECORD_ID,CpqTableEntryId from ( select ROW_NUMBER() OVER(order by "+ str(Wh_API_NAMEs) +") AS ROW, * from CTCICO (nolock)  where CONTRACT_RECORD_ID ='"+str(RecAttValue)
										+"' and GREENBOOK = '"+str(TreeParam)+"') m where m.ROW BETWEEN "
										+ str(Page_start)
										+ " AND "
										+ str(Page_End)
									)

								QuryCount_str = (
									"SELECT COUNT(CpqTableEntryId) AS cnt FROM CTCICO (nolock) WHERE CONTRACT_RECORD_ID = '"
										+ str(RecAttValue)
										+ "'and GREENBOOK = '"+str(TreeParam)+"'"
								)  
							else:    
								imgstr = '<img title="Acquired" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Green_Tick.svg>'
								acquiring_img_str = '<img title="Acquiring" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Cloud_Icon.svg>'
								qt_rec_id = SqlHelper.GetFirst("SELECT CONTRACT_ID, SERVICE_ID FROM CTCTSV (NOLOCK) WHERE CONTRACT_RECORD_ID ='" + str(
								contract_quote_record_id) + "'")
								LineAndEquipIDList = TreeParam.split(' - ')
								if qt_rec_id.CONTRACT_ID == '70011556':
									SERV_DESC = "Z0091"
								else:
									SERV_DESC = qt_rec_id.SERVICE_ID
								if TreeParentParam == "Cart Items":                                    
									Qury_str = (
										"select top "
											+ str(PerPage)
											+ " CASE WHEN DISCOUNT = 'ACQUIRED' THEN '"+ imgstr +"' ELSE '"+ imgstr +"' END AS EQUIPMENT_STATUS, CONTRACT_ITEM_COVERED_OBJECT_RECORD_ID, EQUIPMENT_LINE_ID, SERVICE_ID, EQUIPMENT_ID,LINE_ITEM_ID,DISCOUNT,SERIAL_NO, GREENBOOK, TOTAL_COST, TAX, EXTENDED_PRICE,CpqTableEntryId from ( select  ROW_NUMBER() OVER( ORDER BY EQUIPMENT_LINE_ID) AS ROW, * from CTCICO (NOLOCK) where CONTRACT_ID = '"
											+ str(qt_rec_id.CONTRACT_ID)
											+ "' AND SERVICE_ID = '"
											+ str(LineAndEquipIDList[1])
											+ "') m where m.ROW BETWEEN "
											+ str(Page_start)
											+ " and "
											+ str(Page_End)
									)
									QuryCount_str = (
											"select count(*) as cnt FROM CTCICO (NOLOCK) where SERVICE_ID = '{}' and CONTRACT_ID = '{}'".format(
												LineAndEquipIDList[1], str(qt_rec_id.CONTRACT_ID))
									)
								else:
									Qury_str = (
										"select top "
											+ str(PerPage)
											+ " * from ( select  ROW_NUMBER() OVER( ORDER BY EQUIPMENT_LINE_ID) AS ROW, * from CTCICO (NOLOCK) where CONTRACT_ID = '"
											+ str(qt_rec_id.CONTRACT_ID)
											+ "' AND SERVICE_ID = '"
											+ str(SERV_DESC)
											+ "') m where m.ROW BETWEEN "
											+ str(Page_start)
											+ " and "
											+ str(Page_End)
									)
									QuryCount_str = (
											"select count(*) as cnt FROM CTCICO (NOLOCK) where SERVICE_ID = '{}' and CONTRACT_ID = '{}'".format(
												SERV_DESC, str(qt_rec_id.CONTRACT_ID))
									)
						elif str(RECORD_ID) == "SYOBJR-98788":
							contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
							qt_rec_id= Sql.GetFirst("SELECT QUOTE_ID FROM SAQTSV WHERE QUOTE_RECORD_ID ='"+str(contract_quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' ")
							
							if TreeParentParam:
								Qustr = "where QUOTE_ID = '"+str(qt_rec_id.QUOTE_ID)+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' and SERVICE_TYPE = '{}'".format(TreeParam)
							else:
								Qustr = "where QUOTE_ID = '"+str(qt_rec_id.QUOTE_ID)+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"'"
							##aa = SqlHelper.GetList(" select DISTINCT top 10 QUOTE_SERVICE_RECORD_ID,SERVICE_ID,SERVICE_DESCRIPTION,SERVICE_TYPE,QUOTE_RECORD_ID,SALESORG_RECORD_ID,UOM_RECORD_ID,PAR_SERVICE_RECORD_ID,QTEREV_RECORD_ID,SERVICE_RECORD_ID,CONVERT(VARCHAR(10),CONTRACT_VALID_FROM,101) AS [CONTRACT_VALID_FROM],CONVERT(VARCHAR(10),CONTRACT_VALID_TO,101) AS [CONTRACT_VALID_TO],CpqTableEntryId from ( select TOP 10 ROW_NUMBER() OVER(order by QUOTE_RECORD_ID) AS ROW,S.QUOTE_SERVICE_RECORD_ID,S.SERVICE_ID,S.SERVICE_DESCRIPTION,S.PAR_SERVICE_ID,S.SERVICE_TYPE,S.QUOTE_RECORD_ID,S.SALESORG_RECORD_ID,S.UOM_RECORD_ID,S.PAR_SERVICE_RECORD_ID,S.QTEREV_RECORD_ID,S.SERVICE_RECORD_ID,CONVERT(VARCHAR(10),CONTRACT_VALID_FROM,101) AS [CONTRACT_VALID_FROM],CONVERT(VARCHAR(10),CONTRACT_VALID_TO,101) AS [CONTRACT_VALID_TO],S.CpqTableEntryId  from SAQTSV S JOIN MAADPR M ON S.SERVICE_ID = M.PRDOFR_ID  where S.QUOTE_ID = '3050006088' AND S.QTEREV_RECORD_ID = '545092F3-0315-41C6-A7FD-71F9079DE8C0'  and M.VISIBLE_INCONFIG = 'True' ) m where m.ROW BETWEEN 1 and 10")
							doc_type = Sql.GetList("SELECT DOCTYP_ID FROM SAQTSV (NOLOCK) "+ str(Qustr))

							for document_type in doc_type:
								if document_type.DOCTYP_ID == "ZWK1":
									Qury_str = (
										"select DISTINCT top "
										+ str(PerPage)
										+ " "
										+ str(select_obj_str)
										+ ",CpqTableEntryId from ( select TOP 10 ROW_NUMBER() OVER(order by "
										+ str(Wh_API_NAMEs)
										+ ") AS ROW, S.QUOTE_SERVICE_RECORD_ID,S.SERVICE_ID,S.SERVICE_DESCRIPTION,S.PAR_SERVICE_ID,S.SERVICE_TYPE,S.QUOTE_RECORD_ID,S.SALESORG_RECORD_ID,S.UOM_RECORD_ID,S.PAR_SERVICE_RECORD_ID,S.QTEREV_RECORD_ID,S.SERVICE_RECORD_ID,CONVERT(VARCHAR(10),CONTRACT_VALID_FROM,101) AS [CONTRACT_VALID_FROM],CONVERT(VARCHAR(10),CONTRACT_VALID_TO,101) AS [CONTRACT_VALID_TO],S.CpqTableEntryId  from SAQTSV S "
										+ str(Qustr)
										+ ") m where m.ROW BETWEEN "
										+ str(Page_start)
										+ " and "
										+ str(Page_End)
										+ ""
									)
								else:
									Qury_str = (
										"select DISTINCT top "
										+ str(PerPage)
										+ " "
										+ str(select_obj_str)
										+ ",CpqTableEntryId from ( select TOP 10 ROW_NUMBER() OVER(order by "
										+ str(Wh_API_NAMEs)
										+ ") AS ROW, S.QUOTE_SERVICE_RECORD_ID,S.SERVICE_ID,S.SERVICE_DESCRIPTION,S.PAR_SERVICE_ID,S.SERVICE_TYPE,S.QUOTE_RECORD_ID,S.SALESORG_RECORD_ID,S.UOM_RECORD_ID,S.PAR_SERVICE_RECORD_ID,S.QTEREV_RECORD_ID,S.SERVICE_RECORD_ID,CONVERT(VARCHAR(10),CONTRACT_VALID_FROM,101) AS [CONTRACT_VALID_FROM],CONVERT(VARCHAR(10),CONTRACT_VALID_TO,101) AS [CONTRACT_VALID_TO],S.CpqTableEntryId  from SAQTSV S JOIN (SELECT distinct PRDOFR_ID FROM MAADPR WHERE VISIBLE_INCONFIG = 'TRUE' )M ON S.SERVICE_ID = M.PRDOFR_ID "
										+ str(Qustr)
										+ ") m where m.ROW BETWEEN "
										+ str(Page_start)
										+ " and "
										+ str(Page_End)
										+ ""
									)                           
							
							QuryCount_str = "select count(*) as cnt from " + str(ObjectName) + " S (nolock) JOIN (SELECT distinct PRDOFR_ID FROM MAADPR WHERE VISIBLE_INCONFIG = 'TRUE' ) M ON S.SERVICE_ID = M.PRDOFR_ID " + str(Qustr)
						elif str(RECORD_ID) == "SYOBJR-98853" and str(TreeParam) == "Tracked Objects":
							RecAttValue = Product.Attributes.GetByName("QSTN_SYSEFL_AC_00063").GetValue()
							Qury_str = (
								"select DISTINCT top "
								+ str(PerPage)
								+ " APPROVAL_TRACKED_FIELD_RECORD_ID,APRCHN_ID,APRCHNSTP,TRKOBJ_TRACKEDFIELD_LABEL,TRKOBJ_NAME,TRACKING_TYPE,CpqTableEntryId from (SELECT ROW_NUMBER() OVER(order by APPROVAL_TRACKED_FIELD_RECORD_ID) AS ROW,ACAPTF.APPROVAL_TRACKED_FIELD_RECORD_ID,ACAPTF.APRCHN_ID,ACAPTF.APRCHNSTP,ACAPTF.TRKOBJ_TRACKEDFIELD_LABEL,ACAPTF.TRKOBJ_NAME,ACAPTF.TRACKING_TYPE,ACAPTF.CpqTableEntryId FROM ACAPTF (NOLOCK) INNER JOIN ACAPTX ON ACAPTF.APRCHN_ID = ACAPTX.APRCHN_ID WHERE ACAPTX.APPROVAL_TRANSACTION_RECORD_ID = '"
								+ str(RecAttValue)
								+ "') S where S.ROW BETWEEN "
								+ str(Page_start)
								+ " and "
								+ str(Page_End)
								+ " "
							)
							QuryCount_str = (
								"SELECT count(DISTINCT ACAPTF.APPROVAL_TRACKED_FIELD_RECORD_ID) as cnt FROM ACAPTF (NOLOCK) INNER JOIN ACAPTX ON ACAPTF.APRCHN_ID = ACAPTX.APRCHN_ID WHERE ACAPTX.APPROVAL_TRANSACTION_RECORD_ID = '"
								+ str(RecAttValue)                                
								+ "' "
							)
						elif str(RECORD_ID) == "SYOBJR-00026" and str(TreeParentParam) == "Tracked Objects":
							RecAttValue = Product.Attributes.GetByName("QSTN_SYSEFL_AC_00063").GetValue()
							Qury_str = (
								"select DISTINCT top "
								+ str(PerPage)
								+ " APPROVAL_TRACKED_VALUE_RECORD_ID,APRCHN_ID,APRCHNSTP,TRKOBJ_TRACKEDFIELD_LABEL,TRKOBJ_NAME,TRKOBJ_TRACKEDFIELD_OLDVALUE,TRKOBJ_TRACKEDFIELD_NEWVALUE,TRKOBJ_CPQTABLEENTRYID,CpqTableEntryId from (SELECT ROW_NUMBER() OVER(order by APPROVAL_TRACKED_VALUE_RECORD_ID) AS ROW,ACAPFV.TRKOBJ_TRACKEDFIELD_OLDVALUE,ACAPFV.APPROVAL_TRACKED_VALUE_RECORD_ID,ACAPFV.APRCHN_ID,ACAPFV.APRCHNSTP,ACAPFV.TRKOBJ_TRACKEDFIELD_LABEL,ACAPFV.TRKOBJ_NAME,ACAPFV.TRKOBJ_TRACKEDFIELD_NEWVALUE, ACAPFV.CpqTableEntryId,ACAPFV.TRKOBJ_CPQTABLEENTRYID FROM ACAPFV (NOLOCK) INNER JOIN ACAPTX ON ACAPFV.APRCHN_ID = ACAPTX.APRCHN_ID AND ACAPFV.APPROVAL_ID = ACAPTX.APPROVAL_ID WHERE ACAPTX.APPROVAL_TRANSACTION_RECORD_ID = '"
								+ str(RecAttValue)
								+ "' AND ACAPFV.TRKOBJ_TRACKEDFIELD_LABEL= '"
								+ str(TreeParam)                            
								+ "') S where S.ROW BETWEEN "
								+ str(Page_start)
								+ " and "
								+ str(Page_End)
								+ " "
							)
							QuryCount_str = (
								"SELECT count(DISTINCT ACAPFV.APPROVAL_TRACKED_VALUE_RECORD_ID) as cnt FROM ACAPFV (NOLOCK) INNER JOIN ACAPTX ON ACAPFV.APRCHN_ID = ACAPTX.APRCHN_ID WHERE ACAPTX.APPROVAL_TRANSACTION_RECORD_ID = '"
								+ str(RecAttValue)
								+ "' AND ACAPFV.TRKOBJ_TRACKEDFIELD_LABEL= '"
								+ str(TreeParam)                            
								+ "' "
							)
						elif str(RECORD_ID) == "SYOBJR-98816":                            
							contract_quote_record_id = Quote.GetGlobal("contract_record_id")
							ct_rec_id= SqlHelper.GetFirst("SELECT CONTRACT_ID FROM CTCTSV WHERE CONTRACT_RECORD_ID ='"+str(contract_quote_record_id)+"'")
							if TreeParentParam:
								Qustr = "where  CONTRACT_ID = '"+str(ct_rec_id.CONTRACT_ID)+"' and PRODUCT_TYPE = '{}'".format(TreeParam)
							else:
								Qustr = "where  CONTRACT_ID = '"+str(ct_rec_id.CONTRACT_ID)+"'"
							Qury_str = (
								"select DISTINCT top "
								+ str(PerPage)
								+ " "
								+ str(select_obj_str)
								+ ",CpqTableEntryId from ( select TOP 10 ROW_NUMBER() OVER(order by "
								+ str(Wh_API_NAMEs)
								+ ") AS ROW, * from "
								+ str(ObjectName)
								+ " (nolock) "
								+ str(Qustr)
								+ " ) m where m.ROW BETWEEN "
								+ str(Page_start)
								+ " and "
								+ str(Page_End)
								+ ""
							)                            
							QuryCount_str = "select count(*) as cnt from " + str(ObjectName) + " (nolock) " + str(Qustr)
						elif RECORD_ID == 'SYOBJR-00006' and TreeParam == "Quote Preview":                            
							Qury_str = (
							"SELECT DISTINCT TOP "
							+ str(PerPage)
							+ "QUOTE_ITEM_FORECAST_PART_RECORD_ID,PART_NUMBER,PART_DESCRIPTION,BASEUOM_ID,SCHEDULE_MODE,DELIVERY_MODE,MATPRIGRP_ID,UNIT_PRICE,EXTENDED_PRICE,ANNUAL_QUANTITY,PRICING_STATUS,CUSTOMER_PART_NUMBER_RECORD_ID,BASEUOM_RECORD_ID,MATPRIGRP_RECORD_ID,QTEITM_RECORD_ID,QUOTE_RECORD_ID,QTEREV_RECORD_ID,SALESORG_RECORD_ID,SERVICE_RECORD_ID,PART_RECORD_ID,SALESUOM_RECORD_ID,CpqTableEntryId,TAX,TAX_PERCENTAGE,SERVICE_ID,SRVTAXCLA_DESCRIPTION from ( select ROW_NUMBER() OVER(order by "+ str(Wh_API_NAMEs) +") AS ROW, * from SAQIFP (nolock)  where QUOTE_RECORD_ID ='"+str(RecAttValue)
							+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' ) m where m.ROW BETWEEN "
							+ str(Page_start)
							+ " AND "
							+ str(Page_End)+" "
							)
							QuryCount_str = (
								"SELECT COUNT(CpqTableEntryId) AS cnt FROM SAQIFP (nolock) WHERE QUOTE_RECORD_ID = '"
								+ str(RecAttValue)
								+ "' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' "
							)
						elif RECORD_ID == 'SYOBJR-98869' and TreeParam == "Revisions":
							Qury_str = ("select DISTINCT TOP "
								+ str(PerPage)
								+ " QUOTE_REVISION_RECORD_ID,CONCAT(QUOTE_ID, '-', QTEREV_ID) AS QTEREV_ID,REVISION_DESCRIPTION,REV_CREATE_DATE,REV_EXPIRE_DATE,REVISION_STATUS,ACTIVE,CONTRACT_VALID_FROM,CONTRACT_VALID_TO,SALESORG_RECORD_ID,QUOTE_RECORD_ID,CpqTableEntryId from ( select  ROW_NUMBER() OVER(order by QUOTE_RECORD_ID) AS ROW, * from SAQTRV (nolock)  where QUOTE_RECORD_ID = '" 
								+ str(contract_quote_record_id) + "' ) m where m.ROW BETWEEN "
								+ str(Page_start)
								+ " and "
								+ str(Page_End)
								+ ""
							)
							QuryCount_str = (
								"SELECT COUNT(QUOTE_REVISION_RECORD_ID) AS cnt FROM SAQTRV (nolock) WHERE QUOTE_RECORD_ID = '"
								+ str(contract_quote_record_id)
								+ "'"
							)
						elif RECORD_ID == 'SYOBJR-00010':    
							imgstr = '<img title="Acquired" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Green_Tick.svg>'
							acquiring_img_str = '<img title="Acquiring" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Cloud_Icon.svg>'
							error = '<img title="Error" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/exclamation_icon.svg>'
							cps_pricing_img = ""
							#cps_pricing_img ='<a href="#" onclick=""><img src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/info.png"></a>'
							Qury_str = (
								"SELECT DISTINCT TOP "
								+ str(PerPage)
								+ "QUOTE_ITEM_FORECAST_PART_RECORD_ID, CASE WHEN PRICING_STATUS = 'ACQUIRED' THEN '"+ imgstr +"' WHEN PRICING_STATUS = 'APPROVAL REQUIRED' THEN '" +exclamation+ "' WHEN PRICING_STATUS = 'ERROR' THEN '" +error+ "' ELSE '"+ acquiring_img_str +"' END AS PRICING_STATUS,SERVICE_ID,CONCAT('"+cps_pricing_img+ "',PART_NUMBER) AS PART_NUMBER,PART_DESCRIPTION,MATPRIGRP_ID,BASEUOM_ID,SCHEDULE_MODE,DELIVERY_MODE,UNIT_PRICE,UNIT_PRICE_INGL_CURR,EXTENDED_PRICE,EXTPRI_INGL_CURR,ANNUAL_QUANTITY,CUSTOMER_PART_NUMBER_RECORD_ID,BASEUOM_RECORD_ID,MATPRIGRP_RECORD_ID,QTEITM_RECORD_ID,QUOTE_RECORD_ID,QTEREV_RECORD_ID,SALESORG_RECORD_ID,SERVICE_RECORD_ID,PART_RECORD_ID,SALESUOM_RECORD_ID,CpqTableEntryId,TAX,SRVTAXCLA_DESCRIPTION,TAX_PERCENTAGE from ( select ROW_NUMBER() OVER(order by "+ str(Wh_API_NAMEs) +") AS ROW, * from SAQIFP (nolock)  where QUOTE_RECORD_ID ='"+str(RecAttValue)
								+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' ) m where m.ROW BETWEEN "
								+ str(Page_start)
								+ " AND "
								+ str(Page_End)+" ORDER BY PRICING_STATUS ASC"
							)
							QuryCount_str = (
								"SELECT COUNT(CpqTableEntryId) AS cnt FROM SAQIFP (nolock) WHERE QUOTE_RECORD_ID = '"
								+ str(RecAttValue)
								+ "' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' "
							)
							all_acquired = ["ACQUIRING","APPROVAL REQUIRED","ERROR"]
							all_error = ["APPROVAL REQUIRED","ACQUIRING","ACQUIERD"]
							all_required = ["ACQUIERD","ACQUIRING","ERROR"]
							all_acquiring = ["ACQUIERD","ERROR","APPROVAL REQUIRED"]
							acq_error = ["ACQUIERD","ERROR"]
							acq_req = ["ACQUIERD","APPROVAL REQUIRED"]
							not_acq_req = ["ACQUIRING","ERROR"]
							acq_error_approval = ["ACQUIERD","ERROR","APPROVAL"]
							not_acq_error = ["ACQUIRING","APPROVAL REQUIRED"]

							if "ACQUIRED" in price_status and ('ACQUIRING' not in price_status and 'APPROVAL REQUIRED' not in price_status and 'ERROR' not in price_status):
								icon = '<img title="Acquired" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Green_Tick.svg>'
							elif "ERROR" in price_status and ('ACQUIRED' not in price_status and 'APPROVAL REQUIRED' not in price_status and 'ACQUIRING' not in price_status):
								icon = '<img title="Acquiring" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/exclamation_icon.svg'
							elif "APPROVAL REQUIRED" in price_status and ('ACQUIRED' not in price_status and 'ERROR' not in price_status and 'ACQUIRING' not in price_status):
								icon = '<img title="Acquiring" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/clock_exe.svg>'
							elif "ACQUIRING" in price_status and 'ACQUIRED' not in price_status and 'ERROR' not in price_status and 'APPROVAL REQUIRED' not in price_status:
								icon = '<img title="Acquiring" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Cloud_Icon.svg>'
							elif ("ACQUIRED" in price_status and "ERROR" in price_status) and ('ACQUIRING' not in price_status and 'APPROVAL REQUIRED' not in price_status):
								icon = '<img title="Acquiring" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/exclamation_icon.svg'
							elif ("ACQUIRED" in price_status and 'ERROR' in price_status and 'APPROVAL REQUIRED' in price_status) and "ACQUIRING" not in price_status :
								icon = '<img title="Acquiring" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/exclamation_icon.svg'
							elif ("ACQUIRING" in price_status and 'APPROVAL REQUIRED' in price_status) and ('ACQUIRED' not in price_status and "ERROR" not in price_status) :
								icon = '<img title="Acquiring" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/clock_exe.svg>'
							else:
								icon = '<img title="Acquiring" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/exclamation_icon.svg'


						elif RECORD_ID == 'SYOBJR-00008':
							imgstr = '<img title="Acquired" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Green_Tick.svg>'
							acquiring_img_str = '<img title="Acquiring" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Cloud_Icon.svg>'
							exclamation = '<img title="Approval Required" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/clock_exe.svg>'

							if getyears == 1:
								col_year =  'YEAR_1'
							elif getyears == 2:
								col_year =  'YEAR_1,YEAR_2'
							elif getyears == 3:
								col_year =  'YEAR_1,YEAR_2,YEAR_3'
							elif getyears == 4:
								col_year =  'YEAR_1,YEAR_2,YEAR_3,YEAR_4'
							else:
								col_year = 'YEAR_1,YEAR_2,YEAR_3,YEAR_4,YEAR_5'

							price_status = []
							# quote_itm_rec = Sql.GetFirst("SELECT QUOTE_ITEM_RECORD_ID FROM SAQITM (NOLOCK) "+str(Qustr)+"")
							SAQICO_status = Sql.GetList("SELECT DISTINCT STATUS FROM SAQICO (NOLOCK) "+str(Qustr)+"")
							for pricing_status in SAQICO_status:
								price_status.append(pricing_status.STATUS)
								
							
							all_acquired = ["ACQUIRING","APPROVAL REQUIRED","ERROR"]
							all_error = ["APPROVAL REQUIRED","ACQUIRING","ACQUIERD"]
							all_required = ["ACQUIERD","ACQUIRING","ERROR"]
							all_acquiring = ["ACQUIERD","ERROR","APPROVAL REQUIRED"]
							acq_error = ["ACQUIERD","ERROR"]
							acq_req = ["ACQUIERD","APPROVAL REQUIRED"]
							not_acq_req = ["ACQUIRING","ERROR"]
							acq_error_approval = ["ACQUIERD","ERROR","APPROVAL"]
							not_acq_error = ["ACQUIRING","APPROVAL REQUIRED"]

							if "ACQUIRED" in price_status and ('ACQUIRING' not in price_status and 'APPROVAL REQUIRED' not in price_status and 'ERROR' not in price_status):
								icon = '<img title="Acquired" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Green_Tick.svg>'
							elif "ERROR" in price_status and ('ACQUIRED' not in price_status and 'APPROVAL REQUIRED' not in price_status and 'ACQUIRING' not in price_status):
								icon = '<img title="Error" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/exclamation_icon.svg'
							elif "APPROVAL REQUIRED" in price_status and ('ACQUIRED' not in price_status and 'ERROR' not in price_status and 'ACQUIRING' not in price_status):
								icon = '<img title="Approval Required" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/clock_exe.svg>'
							elif "ACQUIRING" in price_status and 'ACQUIRED' not in price_status and 'ERROR' not in price_status and 'APPROVAL REQUIRED' not in price_status:
								icon = '<img title="Acquiring" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Cloud_Icon.svg>'
							elif ("ACQUIRED" in price_status and "ERROR" in price_status) and ('ACQUIRING' not in price_status and 'APPROVAL REQUIRED' not in price_status):
								icon = '<img title="Error" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/exclamation_icon.svg'
							elif ("ACQUIRED" in price_status and "ACQUIRING" in price_status) and ('ERROR' not in price_status and 'APPROVAL REQUIRED' not in price_status):
								icon = '<img title="Acquiring" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Cloud_Icon.svg>'
							elif ("ACQUIRED" in price_status and "APPROVAL REQUIRED" in price_status) and ('ERROR' not in price_status and 'ACQUIRING' not in price_status):
								icon = '<img title="Approval Required" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/clock_exe.svg>'
							elif ("ACQUIRED" in price_status and 'ERROR' in price_status and 'APPROVAL REQUIRED' in price_status) and "ACQUIRING" not in price_status :
								icon = '<img title="Error" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/exclamation_icon.svg'
							elif ("ACQUIRING" in price_status and 'APPROVAL REQUIRED' in price_status) and ('ACQUIRED' not in price_status and "ERROR" not in price_status) :
								icon = '<img title="Approval Required" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/clock_exe.svg>'
							else:
								icon = '<img title="Error" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/exclamation_icon.svg'

							if TreeParam == "Quote Items":                                
								Qustr = "where QUOTE_RECORD_ID ='"+str(RecAttValue)+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' "
								Qury_str = (
									"select DISTINCT top "
									+ str(PerPage)
									+ " '"+ icon +"' AS PO_NOTES, QUOTE_ITEM_RECORD_ID, LINE_ITEM_ID, SERVICE_ID, SERVICE_DESCRIPTION, OBJECT_QUANTITY,QUANTITY, TOTAL_COST, SALES_DISCOUNT_PRICE,SRVTAXCLA_DESCRIPTION,TAX_PERCENTAGE,TAX, NET_VALUE, TARGET_PRICE, CEILING_PRICE, BD_PRICE, BD_PRICE_MARGIN, DISCOUNT, NET_PRICE, YEAR_OVER_YEAR, "+col_year+" "
									+ ",CpqTableEntryId from ( select TOP 10 ROW_NUMBER() OVER(order by "
									+ str(Wh_API_NAMEs)
									+ ") AS ROW, * from "
									+ str(ObjectName)
									+ " (nolock) "
									+ str(Qustr)
									+ " ) m where m.ROW BETWEEN "
									+ str(Page_start)
									+ " and "
									+ str(Page_End)
									+ ""
								)
								QuryCount_str = "select count(*) as cnt from " + str(ObjectName) + " (nolock) " + str(Qustr)
						elif RECORD_ID == 'SYOBJR-00024':                            
							quote_obj = Sql.GetFirst("select QUOTE_ID,MASTER_TABLE_QUOTE_RECORD_ID from SAQTMT (NOLOCK) where MASTER_TABLE_QUOTE_RECORD_ID = '{contract_quote_record_id}' AND QTEREV_RECORD_ID='{revision_rec_id}' ".format(contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id"), revision_rec_id = quote_revision_record_id))
							quote_id = quote_obj.QUOTE_ID
							TreeParam = Product.GetGlobal("TreeParam")
							dynamic_condtn = ""
							if TreeSuperParentParam == 'Approvals':
								chain_step_name = SubTab.split(':')[1].strip()
								step_id = chain_step_name.split(' ')[1]
								round_value = TreeParam.split()[1]
								TreeParam = Product.GetGlobal("TreeParam")
								Qury_str = ("""select DISTINCT top {PerPage} * from (select ROW_NUMBER() OVER( ORDER BY ACAPTX.APRCHNSTP_ID) AS ROW,ACAPTX.APPROVAL_TRANSACTION_RECORD_ID, ACAPTX.APPROVAL_ID,ACAPTX.APRCHNSTP_ID,ACAPTX.APRCHNSTP_APPROVER_ID,ACAPTX.APPROVAL_ROUND,ACAPTX.APPROVALSTATUS,ACAPTX.RECIPIENT_COMMENTS,ACAPTX.APRCHNSTP_RECORD_ID,ACAPTX.APPROVAL_RECIPIENT,ACAPTX.CpqTableEntryId FROM ACAPTX (nolock) inner join ACACST (nolock) on ACAPTX.APRCHNSTP_RECORD_ID = ACACST.APPROVAL_CHAIN_STEP_RECORD_ID  and ACAPTX.APRTRXOBJ_ID = '{Quote_id}' and ACAPTX.APRCHNSTPTRX_ID like '%{Quote_id}%' and ACAPTX.APRCHN_ID = '{chain_id}' {dynamic_condtn})m where m.ROW BETWEEN """.format(PerPage = PerPage,contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id"),Quote_id = quote_id,dynamic_condtn=dynamic_condtn,chain_id=TreeParentParam if TreeSuperParentParam == 'Approvals' else TreeParam) + str(Page_start) + " and " + str(Page_End))
								QuryCount_str = """select count(ACAPTX.CpqTableEntryId) as cnt FROM ACAPTX (nolock) inner join ACACST (nolock) on ACAPTX.APRCHNSTP_RECORD_ID = ACACST.APPROVAL_CHAIN_STEP_RECORD_ID and  ACAPTX.APRTRXOBJ_ID = '{Quote_id}' and ACAPTX.APRCHNSTPTRX_ID like '%{Quote_id}%' and ACAPTX.APRCHN_ID = '{chain_id}' {dynamic_condtn}""".format(contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id"),Quote_id = quote_id,dynamic_condtn=dynamic_condtn,chain_id=TreeParentParam if TreeSuperParentParam == 'Approvals' else TreeParam)
							else:                            
								Qury_str = ("""select DISTINCT top {PerPage} * from (select ROW_NUMBER() OVER( ORDER BY {Wh_API_NAMEs}) AS ROW,ACAPTX.APPROVAL_TRANSACTION_RECORD_ID, ACAPTX.APPROVAL_ID,ACAPTX.APRCHNSTP_ID,ACAPTX.APRCHNSTP_APPROVER_ID,ACAPTX.APPROVAL_ROUND,ACAPTX.APPROVALSTATUS,ACAPTX.RECIPIENT_COMMENTS,ACAPTX.APRCHNSTP_RECORD_ID,ACAPTX.APPROVAL_RECIPIENT,ACAPTX.CpqTableEntryId FROM ACAPTX (nolock) inner join ACACST (nolock) on ACAPTX.APRCHNSTP_RECORD_ID = ACACST.APPROVAL_CHAIN_STEP_RECORD_ID  and ACAPTX.APRTRXOBJ_ID = '{Quote_id}' and ACAPTX.APRCHNSTPTRX_ID like '%{Quote_id}%' and ACAPTX.APRCHN_ID = '{Chain}')m where m.ROW BETWEEN """.format(PerPage = PerPage,contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id"),Quote_id = quote_id,Chain = TreeParam,Wh_API_NAMEs = Wh_API_NAMEs ) + str(Page_start) + " and " + str(Page_End))
								QuryCount_str = """select count(ACAPTX.CpqTableEntryId) as cnt FROM ACAPTX (nolock) inner join ACACST (nolock) on ACAPTX.APRCHNSTP_RECORD_ID = ACACST.APPROVAL_CHAIN_STEP_RECORD_ID and  ACAPTX.APRTRXOBJ_ID = '{Quote_id}' and ACAPTX.APRCHNSTPTRX_ID like '%{Quote_id}%' and ACAPTX.APRCHN_ID = '{Chain}' """.format(contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id"),Quote_id = quote_id,Chain = TreeParam)
						elif RECORD_ID == 'SYOBJR-98841':
							imgstr = '<img title="Acquired" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Green_Tick.svg>'
							acquiring_img_str = '<img title="Acquiring" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Cloud_Icon.svg>'
							
							if TreeParam == "Cart Items":                                
								Qury_str = (
									"select DISTINCT top "
									+ str(PerPage)
									+ "  CASE WHEN ITEM_STATUS = 'ACQUIRED' THEN '"+ imgstr +"' ELSE '"+ imgstr +"' END AS PO_NOTES, CONTRACT_ITEM_RECORD_ID, LINE_ITEM_ID, SERVICE_ID, SERVICE_DESCRIPTION, QUANTITY, TAX, DISCOUNT, EXTENDED_PRICE"
									+ ",CpqTableEntryId from ( select TOP 10 ROW_NUMBER() OVER(order by "
									+ str(Wh_API_NAMEs)
									+ ") AS ROW, * from "
									+ str(ObjectName)
									+ " (nolock) "
									+ str(Qustr)
									+ " ) m where m.ROW BETWEEN "
									+ str(Page_start)
									+ " and "
									+ str(Page_End)
									+ ""
								)
								QuryCount_str = "select count(*) as cnt from " + str(ObjectName) + " (nolock) " + str(Qustr)
						##involved parties equipmemt and tool equipment matrix starts
						elif (str(RECORD_ID) == "SYOBJR-98858" or str(RECORD_ID) == "SYOBJR-00028") and str(TreeParam) == "Quote Information":
							account_id = Product.GetGlobal("stp_account_id")
							
							Qury_str = ("""select DISTINCT top {PerPage} * from (select ROW_NUMBER() OVER( ORDER BY SAQSTE.{Wh_API_NAMEs}) AS ROW,SAQSTE.* from SAQSTE  inner join SAQSCF(nolock)  on SAQSTE.QUOTE_RECORD_ID = SAQSCF.QUOTE_RECORD_ID and SAQSTE.SRCFBL_ID = SAQSCF.SRCFBL_ID where SAQSTE.QUOTE_RECORD_ID = '{contract_quote_record_id}' AND SAQSTE.QTEREV_RECORD_ID='{revision_rec_id}' and SAQSTE.SRCACC_ID = '{account_id}')m where m.ROW BETWEEN """.format(PerPage = PerPage,account_id = account_id,revision_rec_id = quote_revision_record_id,
							contract_quote_record_id = str(RecAttValue), Wh_API_NAMEs= str(Wh_API_NAMEs))+ str(Page_start) + " and " + str(Page_End))
							
							
							
							QuryCount_str = "select count(SAQSTE.CpqTableEntryId) as cnt from SAQSTE  inner join SAQSCF(nolock) on SAQSTE.QUOTE_RECORD_ID = SAQSCF.QUOTE_RECORD_ID and SAQSTE.QTEREV_RECORD_ID = SAQSCF.QTEREV_RECORD_ID and SAQSTE.SRCFBL_ID= SAQSCF.SRCFBL_ID where SAQSTE.QUOTE_RECORD_ID = '{contract_quote_record_id}' and  SAQSTE.QTEREV_RECORD_ID = '{revision_rec_id}' and SAQSTE.SRCACC_ID = '{account_id}'".format(account_id = account_id,revision_rec_id = quote_revision_record_id,contract_quote_record_id=str(RecAttValue))
						##involved parties equipmemt ends
						elif RECORD_ID == 'SYOBJR-98792' and str(TreeParam) == "Quote Preview":
							
							contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
							# Qustr_id = Sql.GetFirst("SELECT QUOTE_ID FROM SAQITM WHERE QUOTE_RECORD_ID ='" + str(
							#contract_quote_record_id) + "' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"'")
							if getyears == 1:
								col_year =  'YEAR_1'
							elif getyears == 2:
								col_year =  'YEAR_1,YEAR_2'
							elif getyears == 3:
								col_year =  'YEAR_1,YEAR_2,YEAR_3'
							elif getyears == 4:
								col_year =  'YEAR_1,YEAR_2,YEAR_3,YEAR_4'
							else:
								col_year = 'YEAR_1,YEAR_2,YEAR_3,YEAR_4,YEAR_5'
							# if TreeParam:
							# 	Qustr = "where QUOTE_ID = '"+str(Qustr_id.QUOTE_ID)+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"'"
							Qury_str = (
								"select DISTINCT top "
								+ str(PerPage)
								+ " QUOTE_ITEM_RECORD_ID, LINE_ITEM_ID, SERVICE_ID, SERVICE_DESCRIPTION, ONSITE_PURCHASE_COMMIT, OBJECT_QUANTITY, TOTAL_COST, SALES_DISCOUNT_PRICE, TAX, NET_VALUE, QUANTITY, TARGET_PRICE, CEILING_PRICE, BD_PRICE, BD_PRICE_MARGIN, DISCOUNT, NET_PRICE, YEAR_OVER_YEAR, "+col_year+", SRVTAXCLA_DESCRIPTION, TAX_PERCENTAGE, CpqTableEntryId from ( select TOP 10 ROW_NUMBER() OVER(order by "
								+ str(Wh_API_NAMEs)
								+ ") AS ROW, * from "
								+ str(ObjectName)
								+ " (nolock) "
								+ str(Qustr)
								+ " AND SERVICE_ID NOT LIKE '%BUNDLE%') m where m.ROW BETWEEN "
								+ str(Page_start)
								+ " and "
								+ str(Page_End)
								+ ""
							)
							QuryCount_str = "select count(*) as cnt from " + str(ObjectName) + " (nolock) " + str(Qustr)+ " AND SERVICE_ID NOT LIKE '%BUNDLE%' "

						elif str(RECORD_ID) == "SYOBJR-98815":                            
							splitTP = TP.split('-')
							TP = splitTP[1]
							Qustr = "where SALESORG_ID = '"+str(TP)+"' and DOC_CURRENCY='"+str(PR_CURR)+"'"
						elif str(RECORD_ID) == "SYOBJR-98862":
							RecAttValue=Product.Attributes.GetByName("QSTN_SYSEFL_SY_00125").GetValue()
							Qustr = " WHERE "+str(ATTRIBUTE_VALUE_STR)+" APP_ID = '"+str(TreeParentParam)+"' AND PROFILE_RECORD_ID ='"+str(RecAttValue)+"'"
						elif str(RECORD_ID) == "SYOBJR-98863":
							RecAttValue=Product.Attributes.GetByName("QSTN_SYSEFL_SY_00125").GetValue()
							Qustr = " WHERE "+str(ATTRIBUTE_VALUE_STR) +" TAB_ID = '"+str(TreeParentParam)+"' AND PROFILE_RECORD_ID ='"+str(RecAttValue)+"'"
						elif str(RECORD_ID) == "SYOBJR-93123":
							RecAttValue = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00128").GetValue()
							Qustr = " WHERE "+str(ATTRIBUTE_VALUE_STR) +" SECTION_NAME = '"+str(TreeParentParam)+"' AND PROFILE_ID ='"+str(RecAttValue)+"' AND OBJECT_NAME = '"+str(ObjectName)+"' "
						elif str(RECORD_ID) == "SYOBJR-98864":
							Qustr = " WHERE "+str(ATTRIBUTE_VALUE_STR) +" TAB_NAME = '"+str(TreeParentParam)+"' AND PROFILE_RECORD_ID ='"+str(RecAttValue)+"'"
						elif str(RECORD_ID) == "SYOBJR-95824" or (str(RECORD_ID) == "SYOBJR-95825" and str(TreeParam)=="Constraints") or str(RECORD_ID) == "SYOBJR-95826" or str(RECORD_ID) == "SYOBJR-95976":
							RecAttValue = productAttributesGetByName("QSTN_SYSEFL_SY_00701").GetValue()
							Qustr = " where " + str(Wh_API_NAME) + " = '" + str(RecAttValue) + "'"
						elif str(RECORD_ID) == "SYOBJR-95825" and str(TreeParentParam) == 'Constraints':
							RecAttValue = productAttributesGetByName("QSTN_SYSEFL_SY_00701").GetValue()
							Qustr = "WHERE CONSTRAINT_TYPE = '"+str(TreeParam)+"' AND OBJECT_RECORD_ID='"+str(RecAttValue)+"'"
						elif str(RECORD_ID) == "SYOBJR-95840": 
							Wh_API_NAMEs = "PAGEACTION_RECORD_ID"                
							RecAttValue = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00723").GetValue()       
							Qustr =  " where SCRIPT_RECORD_ID = '" + str(RecAttValue) + "'"
						elif str(RECORD_ID) == "SYOBJR-95890": 
							RecAttValue = Product.Attributes.GetByName("QSTN_SYSEFL_SY_03295").GetValue()
							Qustr = " where "+str(ATTRIBUTE_VALUE_STR)+" "+ str(Wh_API_NAME) + " = '" + str(RecAttValue) + "'"
						elif str(RECORD_ID) == "SYOBJR-93188":
							RecAttValue = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00128").GetValue()
							GetAppname_query = ""
							Qustr = " WHERE TAB_NAME = '"+str(TreeParentParam)+"' AND PROFILE_ID ='"+str(RecAttValue)+"'" 
						elif str(RECORD_ID)== "SYOBJR-98857":
							Qustr = " where " + str(Wh_API_NAME) + " = '" + str(RecAttValue) + "'"   
							if "SRCFBL_ID" in Wh_API_NAMEs:
								Wh_API_NAMEs=Wh_API_NAMEs.replace("SRCFBL_ID", "CAST(SRCFBL_ID AS int)")
						elif  str(RECORD_ID) == "SYOBJR-98789" and "Sending Account -" in TreeParam :
							Qustr += " where " + str(Wh_API_NAME) + " = '" + str(RecAttValue) + "' AND RELOCATION_FAB_TYPE = 'SENDING FAB'"
						elif  str(RECORD_ID) == "SYOBJR-98789" and "Receiving Account -" in TreeParam :
							Qustr += " where " + str(Wh_API_NAME) + " = '" + str(RecAttValue) + "' AND RELOCATION_FAB_TYPE = 'RECEIVING FAB'"   
						elif str(RECORD_ID) == "SYOBJR-95985":
							Qustr += " WHERE TREE_NAME = '"+str(TreeParentParam)+"'"
						elif str(RECORD_ID) == "SYOBJR-98869":
							RecAttValue = contract_quote_record_id
							#Trace.Write('1196---RecAttValue--RecAttValue-----'+str(RecAttValue))
							Qustr =  " where QUOTE_RECORD_ID = '" + str(contract_quote_record_id) + "'" 
						elif str(RECORD_ID) == "SYOBJR-95981" or str(RECORD_ID)=="SYOBJR-98459":
							RecAttValue = Product.Attributes.GetByName("QSTN_SYSEFL_SY_01110").GetValue()
							Qustr +=" where "+str(Wh_API_NAME) + " = '"+str(RecAttValue)+"'"
						elif str(RECORD_ID) == "SYOBJR-95980":
							RecAttValue = Product.Attributes.GetByName("QSTN_SYSEFL_SY_01110").GetValue()
							Qustr = " where "+str(ATTRIBUTE_VALUE_STR)+" "+ str(Wh_API_NAME) + " = '" + str(RecAttValue) + "'"
						elif str(RECORD_ID) == "SYOBJR-98785":
							RecAttValue = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00811").GetValue()
							Qustr = " where " + str(Wh_API_NAME) + " = '" + str(RecAttValue) + "'"
						elif str(RECORD_ID) == "SYOBJR-00029":
							quote_rec_id = Product.GetGlobal("contract_quote_record_id")
							quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")					
							if TreeSuperParentParam == "Product Offerings":
								service_id = TreeParam.split('-')[0]		
								Qustr = " where "+ str(Wh_API_NAME) + " = '" +str(RecAttValue)+ "' AND PAR_SERVICE_ID = '"+str(service_id)+"' "	
							elif TopTreeSuperParentParam == "Product Offerings":
								service_id = TreeParentParam.split('-')[0]
								Qustr = " where "+ str(Wh_API_NAME) + " = '" +str(RecAttValue)+ "' AND PAR_SERVICE_ID = '"+str(service_id)+"' AND GREENBOOK = '"+str(TreeParam)+"' "
							#Qustr = " where "+ str(Wh_API_NAME) + " = '" +str(RecAttValue)+ "' AND PAR_SERVICE_ID = '"+str(service_id)+"' AND FABLOCATION_ID = '"+str(fab_id)+"' AND GREENBOOK = '"+str(TreeParam)+"' "
						elif str(RECORD_ID) == "SYOBJR-00013":
							RecAttValue = Product.Attributes.GetByName("QSTN_SYSEFL_AC_00001").GetValue()
							Qustr = " where " + str(Wh_API_NAME) + " = '" + str(RecAttValue) + "'"
						elif str(RECORD_ID) == "SYOBJR-98875":
							quote_item_revision_rec_id = Product.GetGlobal('get_quote_item_service')
							get_gb_val = Sql.GetFirst("SELECT GREENBOOK FROM SAQRIT where QUOTE_REVISION_CONTRACT_ITEM_ID= '"+str(quote_item_revision_rec_id)+"'")
							if get_gb_val:
								Qustr += "  where "+ str(Wh_API_NAME) + " = '" +str(RecAttValue)+ "'  AND QTEITM_RECORD_ID = '"+str(quote_item_revision_rec_id)+"' AND GREENBOOK = '"+str(get_gb_val.GREENBOOK)+"'"
						else:
							Qustr = " where " + str(Wh_API_NAME) + " = '" + str(RecAttValue) + "'"
				
				if str(Qury_str) == "" and str(QuryCount_str) == "":  
					select_obj_str = select_obj_str.replace("DEFAULT","[DEFAULT]") 
					select_obj_str = select_obj_str.replace("PRIMARY","[PRIMARY]")
					if str(RECORD_ID) == "SYOBJR-00007":
						pivot_columns = ",".join(['[{}]'.format(billing_date) for billing_date in billing_date_column])
						if Qustr:
							if str(TreeParentParam)== "Billing":
								Qustr += " AND SERVICE_ID = '{}' AND BILLING_DATE BETWEEN '{}' AND '{}'".format(TreeParam,billing_date_column[0], billing_date_column[-1])
							else:
								Qustr += " AND BILLING_DATE BETWEEN '{}' AND '{}'".format(billing_date_column[0], billing_date_column[-1])
						pivot_query_str = """
										SELECT ROW_NUMBER() OVER(ORDER BY EQUIPMENT_ID)
										AS ROW, *
											FROM (
												SELECT 
													{Columns}                                           
												FROM {ObjectName}
												{WhereString}
											) AS IQ
											PIVOT
											(
												SUM(BILLING_VALUE)
												FOR BILLING_DATE IN ({PivotColumns})
											)AS PVT
										""".format(OrderByColumn=Wh_API_NAMEs, Columns=column_before_pivot_change, ObjectName=ObjectName,
													WhereString=Qustr, PivotColumns=pivot_columns)                        
						Qury_str = """SELECT DISTINCT TOP {PerPage} * FROM ( SELECT * FROM ({InnerQuery}) OQ WHERE ROW BETWEEN {Start} AND {End} ) AS FQ ORDER BY EQUIPMENT_ID
										""".format(PerPage=PerPage, OrderByColumn=Wh_API_NAMEs, InnerQuery=pivot_query_str, Start=Page_start, End=Page_End)
						QuryCount_str = "SELECT COUNT(*) AS cnt FROM ({InnerQuery}) OQ ".format(InnerQuery=pivot_query_str) 
					else:
						Qury_str = (
							"select top "
							+ str(PerPage)
							+ " "
							+ str(select_obj_str)
							+ ",CpqTableEntryId from ( select ROW_NUMBER() OVER(order by "
							+ str(Wh_API_NAMEs)
							+ ") AS ROW, * from "
							+ str(ObjectName)
							+ " (nolock) "
							+ str(Qustr)
							+ " ) m where m.ROW BETWEEN "
							+ str(Page_start)
							+ " and "
							+ str(Page_End)
							+ " "
						)
						QuryCount_str = "select count(*) as cnt from " + str(ObjectName) + " (nolock) " + str(Qustr)
					
				try:
					Query_Obj = Sql.GetList(Qury_str)
					Query_CountObj = Sql.GetFirst(QuryCount_str)                
				except:                                    
					Query_Obj = Sql.GetList(
						"select top "
						+ str(PerPage)
						+ "  "
						+ str(obj_str)
						+ ",CpqTableEntryId from "
						+ str(ObjectName)
						+ " (nolock) where 1=1"
					)                    
					QuryCount_str = (
						"select count(" + str(Wh_API_NAME) + ") as cnt from " + str(ObjectName) + " (nolock) where 1=1"
					)
					Query_CountObj = Sql.GetFirst(QuryCount_str)                    
				if Query_CountObj is not None:
					QueryCount = Query_CountObj.cnt
			OBJ_CpqTableEntryId_New = ""
		
			for ik in Query_Obj:				                  
				primary_view = ""
				product_id = ""
				product_name = ""
				other_tab = ""
				product_id_val = ""                
				module_txt = ""
				tab_val = ""
				try:
					OBJ_CpqTableEntryId_New = str(ik.CpqTableEntryId)
				except:
					pass
				
				Action_str = '<div class="btn-group dropdown"><div class="dropdown" id="ctr_drop"><i data-toggle="dropdown" id="dropdownMenuButton" class="fa fa-sort-desc dropdown-toggle" aria-expanded="false"></i><ul class="dropdown-menu left empty_ctrdrop_ul" aria-labelledby="dropdownMenuButton">'
				
				for inm in ik:                
					value123 = str(inm).split(",")[0].replace("[", "").lstrip()
					value1234 = str(inm).split(",")[1].replace("]", "").lstrip()
					if (
						str(obj_obj.SAPCPQ_ATTRIBUTE_NAME) == "SYOBJR-30114"
						or str(obj_obj.SAPCPQ_ATTRIBUTE_NAME) == "SYOBJR-60052"
						or str(obj_obj.SAPCPQ_ATTRIBUTE_NAME) == "SYOBJR-70085"
					):
						if value123 == objRecName:
							other_tab = "0"
							primary_view = value1234                    
					else:
						if value123 == objRecName:
							tab_obj1 = Sql.GetFirst(
								"SELECT PG.TAB_NAME,PG.TAB_RECORD_ID FROM SYSECT (nolock) SE INNER JOIN SYPAGE (nolock) PG on SE.PAGE_RECORD_ID = PG.RECORD_ID WHERE SE.PRIMARY_OBJECT_NAME='"
								+ str(ObjectName)
								+ "' and SE.SECTION_NAME ='BASIC INFORMATION'"
							)
							if tab_obj1 is not None:
								tab_val = str(tab_obj1.TAB_NAME)
								if tab_val in list_of_tabs:
									primary_view = value1234 + "|" + tab_val
								else:
									product_name = Sql.GetFirst(
										"select APP_LABEL from SYTABS (nolock) where RECORD_ID='"
										+ str(tab_obj1.TAB_RECORD_ID)
										+ "'"
									)
									if product_name is not None:
										module_txt = str(product_name.APP_LABEL).strip()
										product_id = Sql.GetFirst(
											"select PRODUCT_ID from products (nolock) where PRODUCT_NAME='"
											+ str(module_txt)
											+ "'"
										)
									if product_id != "" and product_id is not None:
										primary_view = value1234 + "|" + tab_val
										product_id_val = str(product_id.PRODUCT_ID)
										other_tab = "1"
									else:
										primary_view = ""

				if str(current_tab).upper() == "PROFILE" and (ObjectName == "SYPROF"):
					Action_str += '<li><a class="dropdown-item" href="#" onclick="profileObjSet(this)" data-target="#viewProfileRelatedList" data-toggle="modal">VIEW<a><li>'
				elif str(current_tab).upper() == "PROFILE" and (ObjectName != "SYPROD"):                    
					Action_str += '<li><a class="dropdown-item" href="#" onclick="Commonteree_view_RL(this)">VIEW<a><li><li><a class="dropdown-item" href="#" onclick="Commontree_edit_RL(this)">EDIT</a></li>'

				elif str(current_tab).upper() == "ROLE":                    
					Action_str += '<li><a class="dropdown-item" href="#" onclick="Commonteree_view_RL(this)">VIEW<a><li>'  
				else: 
								
					if ObjectName != "SAQIBP" and ObjectName != "SAQTRV" and ObjectName != "SAQDOC":
						Action_str += '<li><a class="dropdown-item" href="#" onclick="Commonteree_view_RL(this)">VIEW</a></li>'

					elif ObjectName == "SAQTRV" :
						quote_contract_recordId = Quote.GetGlobal("contract_quote_record_id")
						get_activerev = Sql.GetFirst("select * from SAQTRV where QUOTE_RECORD_ID = '"+str(quote_contract_recordId)+"' and ACTIVE =1 and CpqTableEntryId = '"+str(value1234)+"'")
						if get_activerev:
							Action_str += '<li><a class="dropdown-item" href="#"  onclick="edit_desc(this)">EDIT DESC</a></li>'
						else:
							Action_str += ''

					elif ObjectName == "SAQDOC":
						contract_quote_rec_id = Quote.GetGlobal("contract_quote_record_id")
						quote_revision_rec_id = Quote.GetGlobal("quote_revision_record_id")
						docnode_action_btn = Sql.GetFirst("SELECT DOCUMENT_DESCRIPTION FROM SAQDOC WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND QUOTE_DOCUMENT_RECORD_ID = '{}'".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_rec_id,ik.QUOTE_DOCUMENT_RECORD_ID))
						if str(docnode_action_btn.DOCUMENT_DESCRIPTION) == "":
							Action_str += '<li><a id = "" class="dropdown-item" href="#" " onclick="doc_edit_desc(this)">EDIT DESC</a></li>'						    

				if str(Action_permission.get("Edit")).upper() == "TRUE":
					if ObjectName == "SAQTRV":
						get_activerev = Sql.GetFirst("select * from SAQTRV where QUOTE_RECORD_ID = '"+str(quote_contract_recordId)+"' and ACTIVE =1 and CpqTableEntryId = '"+str(value1234)+"'")
						get_expire_rev = Sql.GetFirst("select * from SAQTRV where QUOTE_RECORD_ID = '"+str(quote_contract_recordId)+"' and ACTIVE =0  AND (REV_EXPIRE_DATE = '"+str(current_date)+"' or REV_EXPIRE_DATE <= '"+str(current_date)+"' ) and CpqTableEntryId = '"+str(value1234)+"'")
						if get_activerev:
							Action_str += '<li><a class="dropdown-item" href="#" data-toggle="modal" data-target="" style="display: none;" onclick="set_as_active(this)">SET AS ACTIVE</a></li>'
						elif get_expire_rev:
							Action_str += ''
						else:
							Action_str += '<li><a class="dropdown-item" href="#" onclick="set_as_active(this)" >SET AS ACTIVE</a></li>'
					elif ObjectName == "SAQDOC":
						contract_quote_rec_id = Quote.GetGlobal("contract_quote_record_id")
						quote_revision_rec_id = Quote.GetGlobal("quote_revision_record_id")
						docnode_action_btn = Sql.GetFirst("SELECT * FROM SAQDOC WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND QUOTE_DOCUMENT_RECORD_ID = '{}'".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_rec_id,ik.QUOTE_DOCUMENT_RECORD_ID))								
						#for date_value in docnode_action_btn:
						if docnode_action_btn:
							Trace.Write("act_btn=="+str(docnode_action_btn.DATE_SUBMITTED))						
							if str(docnode_action_btn.DATE_SUBMITTED) != "":
								Trace.Write("docnode=====")
								if str(docnode_action_btn.DATE_ACCEPTED) == "" and str(docnode_action_btn.DATE_REJECTED) == "":
									Trace.Write("2222222222222")
									Action_str += '<li><a id = "" class="dropdown-item" href="#" " onclick="customer_accepted(this)">CUSTOMER ACCEPTED</a></li>'
									Action_str += '<li><a id = "" class="dropdown-item" href="#" " onclick="customer_rejected(this)">CUSTOMER REJECTED</a></li>'
							else:
								Trace.Write("docnode111=====")									
								Action_str += '<li><a id = "" class="dropdown-item" href="#" " onclick="submit_to_customer(this)">SUBMITTED TO CUSTOMER</a></li>'
					elif ObjectName == "SAQDLT":
						Action_str += (
							'<li><a class="dropdown-item" href="#" onclick="replace_cont_manager(this)">REPLACE</a></li>'
						) 
					else:
						Action_str += '<li><a class="dropdown-item" href="#" onclick="Commontree_edit_RL(this)">EDIT</a></li>'    
				if str(Action_permission.get("Delete")).upper() == "TRUE":
					onclick = "CommonDelete(this, '" + str(ObjectName) + "', 'WARNING')"
					if ObjectName == "SAQDLT":
						Action_str += (
									'<li><a class="dropdown-item" href="#" id="deletebtn" onclick="'
									+ str(onclick)
									+ '" data-target="#cont_CommonModalDelete" data-toggle="modal">DELETE</a></li>'
								)
					else:
						Action_str += '<li><a class="dropdown-item" data-target="#cont_viewModalDelete" data-toggle="modal" onclick="cont_delete(this)" href="#">DELETE</a></li>'
				Action_str += "</ul></div></div>"
				new_dict = {}
				seg_pric = {}
				ids = {}
				product_id = ""
				product_name = ""
				lookup_rl_popup = []
				pop_val = {}
				editvalue = {}
				primary = ""
				red_color = ""
				decimal_place = 3
				list_lineup = []
				current_rec_id = ""
				for inm in ik:
					#value123 = str(inm).split(",")[0].replace("[", "").lstrip()
					#value1234 = str(inm).split(",")[1].replace("]", "").lstrip()
					Trace.Write("search_after_img"+str(inm))
					a = str(inm).split(",")
					value123 = a[0].replace("[", "").lstrip()
					valu = ",".join(a[1:])
					value1234 = valu.replace("]", "").lstrip()
					if value1234 == "ACQUIRED" or value1234 == "PRICED":
						value1234 = value1234.replace(value1234,"<img title='"+str(value1234).title()+"' src=/mt/APPLIEDMATERIALS_SIT/Additionalfiles/Green_Tick.svg> "+str(value1234))
					if value1234 == "APPROVAL REQUIRED":
						value1234 = value1234.replace("APPROVAL REQUIRED","<img title='Approval Required' src=/mt/APPLIEDMATERIALS_SIT/Additionalfiles/clock_exe.svg> APPROVAL REQUIRED")
					if value1234 == "ACQUIRING":                        
						value1234 = value1234.replace("ACQUIRING","<img title='Acquiring' src=/mt/APPLIEDMATERIALS_SIT/Additionalfiles/Cloud_Icon.svg> ACQUIRING")
					if value1234 == "ERROR":
						value1234 = value1234.replace("ERROR","<img title='Error' src=/mt/APPLIEDMATERIALS_SIT/Additionalfiles/exclamation_icon.svg> ERROR")
					if value1234 == "ASSEMBLY IS MISSING":
						value1234 = value1234.replace("ASSEMBLY IS MISSING","<img title='Assembly Missing' src=/mt/APPLIEDMATERIALS_SIT/Additionalfiles/Orange1_Circle.svg> ASSEMBLY IS MISSING")
					if value1234 == "PARTIALLY PRICED":
						value1234 = value1234.replace("PARTIALLY PRICED","<img title='Partially Priced' src=/mt/APPLIEDMATERIALS_SIT/Additionalfiles/Red1_Circle.svg> PARTIALLY PRICED")
					if value1234 != "ACQUIRED" and value1234 != "APPROVAL REQUIRED" and value1234 != "ERROR" and value1234 != "ASSEMBLY IS MISSING" and value1234 != "PARTIALLY PRICED" and value1234 != "ACQUIRING" and value1234 != "PRICED":                        
						value1234 = value1234
					if value123 == objRecName:
						current_rec_id = value1234
						
					curr_symbol = ""
					cur_api_name=Sql.GetFirst(
							"select API_NAME,DATA_TYPE,FORMULA_DATA_TYPE from  SYOBJD (nolock) where API_NAME = '"
							+ str(value123)
							+ "' and OBJECT_NAME = '"
							+ str(ObjectName)
							+ "' "
						)
					data_type_val = ""
					formu_data_type_val = ""
					if cur_api_name is not None:
						data_type_val = cur_api_name.DATA_TYPE
						formu_data_type_val = cur_api_name.FORMULA_DATA_TYPE

					if str(cur_api_name) is not None and (
						str(data_type_val) == "CURRENCY" or str(formu_data_type_val) == "CURRENCY"
					):                        
						cur_api_name_obj = Sql.GetFirst(
							"select CURRENCY_INDEX from  SYOBJD (nolock) where API_NAME = '"
							+ str(value123)
							+ "' and OBJECT_NAME = '"
							+ str(ObjectName)
							+ "' "
						)                        
						if str(ObjectName) == "SAQIBP":
							contract_quote_record_id = Product.GetGlobal("contract_quote_record_id")
							curr_symbol_obj = Sql.GetFirst(
								"select SYMBOL,CURRENCY,DISPLAY_DECIMAL_PLACES from PRCURR (nolock) where CURRENCY_RECORD_ID = (select "
								+ str(cur_api_name_obj.CURRENCY_INDEX)
								+ " from SAQTMT"
								+ " where MASTER_TABLE_QUOTE_RECORD_ID  "
								+ " = '"
								+ str(contract_quote_record_id)
								+ "' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"') "
							)
						else:
							#Trace.Write("value123-"+str(value123))
							curr_symbol_obj = Sql.GetFirst(
								"select SYMBOL,CURRENCY,DISPLAY_DECIMAL_PLACES from PRCURR (nolock) where CURRENCY_RECORD_ID = (select "
								+ str(cur_api_name_obj.CURRENCY_INDEX)
								+ " from "
								+ str(ObjectName)
								+ " where  "
								+ str(objRecName)
								+ " = '"
								+ str(current_rec_id)
								+ "' ) "
							)
						if curr_symbol_obj is not None:
							#Trace.Write("value123-"+str(value123)+'--'+str(curr_symbol_obj.DISPLAY_DECIMAL_PLACES))
							curr_symbol = curr_symbol_obj.CURRENCY
							decimal_place = curr_symbol_obj.DISPLAY_DECIMAL_PLACES
						if value1234 is not None:
							if value1234 != "":
								my_format = "{:,." + str(decimal_place) + "f}"                                
								value1234 = str(my_format.format(round(float(value1234), int(decimal_place))))
								if str(value123) == "ANNUAL_BILLING_AMOUNT" and str(ObjectName) == "SAQIBP":
									value1234 = value1234
								else:
									value1234 = value1234 + " " + curr_symbol

					if str(cur_api_name) is not None and (
						str(data_type_val) == "PERCENT" or str(formu_data_type_val) == "PERCENT"
					):
						decimal_place = 3
						percentSymbol = "%"
					
						if value1234 is not None and value1234 != '':
							my_format = "{:." + str(decimal_place) + "f}"
							value1234 = str(my_format.format(round(float(value1234), int(decimal_place)))) + " %"
					if value123 in lookup_disply_list:
						for key, value in lookup_list.items():
							if value == value123:
								lookup_val = ""
								lookup_obj = Sql.GetFirst(
									"SELECT LOOKUP_OBJECT FROM  SYOBJD (nolock) WHERE OBJECT_NAME = '"
									+ str(ObjectName)
									+ "' AND LOOKUP_API_NAME ='"
									+ str(key)
									+ "' AND DATA_TYPE = 'LOOKUP'"
								)
								if lookup_obj is not None:
									lookup_val = str(lookup_obj.LOOKUP_OBJECT)
								tab_obj = Sql.GetFirst(
									"SELECT PG.TAB_NAME,PG.TAB_RECORD_ID FROM SYSECT (nolock) SE INNER JOIN SYPAGE (nolock) PG on SE.PAGE_RECORD_ID = PG.RECORD_ID WHERE SE.PRIMARY_OBJECT_NAME='"
									+ str(lookup_val)
									+ "' and SE.SECTION_NAME ='BASIC INFORMATION'"
								)
								if tab_obj is not None:
									tab_val = str(tab_obj.TAB_NAME)
									if tab_val in list_of_tabs:
										ids[key] = value1234 + "|" + tab_val
										
									else:
										product_name = Sql.GetFirst(
											"select APP_LABEL from SYTABS (nolock) where RECORD_ID='"
											+ str(tab_obj.TAB_RECORD_ID)
											+ "'"
										)
										if product_name is not None:
											module_txt = str(product_name.APP_LABEL).strip()
											product_id = Sql.GetFirst(
												"select PRODUCT_ID from products (nolock) where PRODUCT_NAME='"
												+ str(module_txt)
												+ "'"
											)
										if not value1234:
											value1234 = ""

										if product_id != "" and product_id is not None:
											if key:
												pop_val[key] = str(value1234) + "|" + tab_val + "," + str(product_id.PRODUCT_ID)                                            
										else:
											lookup_obj = Sql.GetFirst(
												"SELECT LOOKUP_OBJECT FROM  SYOBJD (nolock) WHERE OBJECT_NAME = '"
												+ str(ObjectName)
												+ "' AND LOOKUP_API_NAME ='"
												+ str(key)
												+ "' AND DATA_TYPE = 'LOOKUP'"
											)
											if not value1234:
												value1234 = ""
											
											lookup_val = str(lookup_obj.LOOKUP_OBJECT)
											if key:
												pop_val[key] = str(value1234) + "|" + lookup_val
								else:
									lookup_obj = Sql.GetFirst(
										"SELECT LOOKUP_OBJECT FROM  SYOBJD (nolock) WHERE OBJECT_NAME = '"
										+ str(ObjectName)
										+ "' AND LOOKUP_API_NAME ='"
										+ str(key)
										+ "' AND DATA_TYPE = 'LOOKUP'"
									)
									if not value1234:
										value1234 = ""
									
									lookup_val = str(lookup_obj.LOOKUP_OBJECT)
									if key:
										pop_val[key] = str(value1234) + "|" + lookup_val
					elif value123 == objRecName:
						key_value = str(value1234)
						if str(ObjectName) == "USERS":                            
							value1234 = str(ObjectName) + "-" + str(key_value).rjust(6, "0")
						elif str(ObjectName) == 'SAQDOC' and key_value == 'Pending':
							value1234 = 'Pending'
						else:
							value1234 = str(ObjectName) + "-" + str(OBJ_CpqTableEntryId_New).rjust(6, "0")
							
						tab_obj1 = Sql.GetFirst(
							"SELECT PG.TAB_NAME,PG.TAB_RECORD_ID FROM SYSECT (nolock) SE INNER JOIN SYPAGE (nolock) PG on SE.PAGE_RECORD_ID = PG.RECORD_ID WHERE SE.PRIMARY_OBJECT_NAME='"
							+ str(ObjectName)
							+ "' and SE.SECTION_NAME ='BASIC INFORMATION'"
						)
						if tab_obj1 is not None:
							tab_val = str(tab_obj1.TAB_NAME)
							if tab_val in list_of_tabs:
								primary = value1234 + "|" + tab_val 
														
								new_dict[value123] = (
									'<abbr id ="' + key_value + '" title="' + value1234 + '">' + value1234 + "</abbr>"
								)                                
							else:
								product_name = Sql.GetFirst(
									"select APP_LABEL from SYTABS (NOLOCK) where RECORD_ID='"
									+ str(tab_obj1.TAB_RECORD_ID)
									+ "'"
								)
								if product_name is not None:
									module_txt = str(product_name.APP_LABEL).strip()
									product_id = Sql.GetFirst(
										"select PRODUCT_ID from products (NOLOCK) where PRODUCT_NAME='"
										+ str(module_txt)
										+ "'"
									)
								if product_id != "" and product_id is not None:                                    
									primary = value1234 + "|" + tab_val + "," + str(product_id.PRODUCT_ID)
									value1234 = value1234.replace('"', "&quot;")
									value1234 = value1234.replace("<p>", " ")
									value1234 = value1234.replace("</p>", " ")                                                                     
									new_dict[value123] = (
										'<abbr id ="' + key_value + '" title="' + value1234 + '">' + value1234 + "</abbr>"
									)
								else:                                                                                                                                             
									new_dict[value123] = (
										'<abbr id ="' + key_value + '" title="' + value1234 + '">' + value1234 + "</abbr>"
									)					
					else:                 
						imgValue = ''
						if str(ObjectName) == "SAQRIT":
							if value1234 != "":
								imgValue = str(value1234).split(">")[0]
								imgValue = str(imgValue)+">"
							else:
								imgValue = ""
						elif str(ObjectName) == "SAQDOC":
							if value1234 != "":
								imgValue = str(value1234).split(">")[0]
								imgValue = str(imgValue)+">"
							else:
								imgValue = ""
						elif value1234.startswith("<img"):
							# value1234 = value1234.replace('"', "&quot;")
							value1234 = value1234.replace("<p>", " ")
							value1234 = value1234.replace("</p>", " ")
							imgValue = value1234
							value1234 = value1234.split('"')
							try:
								value1234 = value1234[1]
							except:
								value1234 = value1234								
						else:
							value1234 = value1234.replace('"', "&quot;")
							value1234 = value1234.replace("<p>", " ")
							value1234 = value1234.replace("</p>", " ")
						img_list = ['PO_NOTES','PRICING_STATUS','STATUS','EQUIPMENT_STATUS']
						if str(ObjectName) == "SAQIFP":
							img_list.append('PRICING_STATUS')
						
						if value123 in img_list:
							Trace.Write("8883"+str(imgValue))
							
							new_dict[value123] = ('<abbr id ="' + key_value + '" title="' + value1234 + '">' + imgValue + "</abbr>")
						else:
							Trace.Write("8886")
							Trace.Write("8886"+str(value1234))
							new_dict[value123] = value1234.upper() 
					if value123 in edit_field:                      
						value1234 = value1234.replace('"', "&quot;")
						value1234 = value1234.replace("<p>", " ")
						value1234 = value1234.replace("</p>", " ")
						new_dict[value123] = value1234
					else:               
						if value123 in checkbox_list:
							new_dict[value123] = value1234
						else:
							Trace.Write("elseval"+str(value1234))
							value1234 = str(value1234).replace('"', "&quot;")
							value1234 = str(value1234).replace("<p>", " ")
							value1234 = str(value1234).replace("</p>", " ")

							if value123 in [
								"ERROR",
								"MINIMUM_PRICE",
								"CATCLC_PRICE_INSORG_CURR",
								"INVCLC_UNITPRICE_INSORG_CURR",
							]:
								new_dict[value123] = value1234
								seg_pric[value123] = value1234.replace(curr_symbol, "").replace(" ", "")
								seg_pric["PRICE_FACTOR"] = PriceFactor
							else:                                    
								if str(RECORD_ID) == "SYOBJR-00009" and str(value123) == 'NET_PRICE':
									new_dict[value123] = (
										'<input id ="' + key_value + '"   value="' + value1234 + '" style="border: 0px solid;" disabled>' + str(value1234).upper() + "</input>"
									)
								if str(value123) == "WARRANTY_END_DATE":
									#Trace.Write('getindication--3075---'+str(getindication))
									getdate_indication = str(value1234)
									if getdate_indication:
										getdate_indication = datetime.strptime(str(getdate_indication), '%m/%d/%Y')                                            
								elif str(value123) in billing_date_column:                                        
									getdate_indication_billing = datetime.strptime(str(value123), '%m-%d-%Y')                                        
									contract_quote_record_id = Product.GetGlobal("contract_quote_record_id")
									curr_symbol_obj = Sql.GetFirst(
										"select SYMBOL,CURRENCY,DISPLAY_DECIMAL_PLACES from PRCURR (nolock) where CURRENCY_RECORD_ID = (select QUOTE_CURRENCY_RECORD_ID"
										+ " from SAQTMT"
										+ " where MASTER_TABLE_QUOTE_RECORD_ID  "
										+ " = '"
										+ str(contract_quote_record_id)
										+ "' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"') "
									)									
									if curr_symbol_obj:
										curr_symbol = curr_symbol_obj.CURRENCY                                            
										try:
											decimal_place = curr_symbol_obj.DISPLAY_DECIMAL_PLACES                                                
											my_format = "{:,." + str(decimal_place) + "f}"
											value1234 = str(my_format.format(round(float(value1234), int(decimal_place))))
										except:
											value1234
									if getdate_indication:                                            
										if getdate_indication > getdate_indication_billing:
											new_dict[value123] = (
												'<input  type= "text" id ="' + key_value + '" class= "billclassedit billclassedit_bg"  value="' + value1234 + '" style="border: 0px solid;"  disabled>'
											)
										else:
											new_dict[value123] = (
												'<input  type= "text" id ="' + key_value + '" class= "billclassedit"  value="' + value1234 + '" style="border: 0px solid;"  disabled>'
											)
									else:                                            
										new_dict[value123] = (
											'<input  type= "text" id ="' + key_value + '" class= "billclassedit"  value="' + value1234 + '" style="border: 0px solid;"  disabled>'
										)
								else:
									if str(value123) != "CUSTOMER_ANNUAL_QUANTITY":                                                
											precentage_columns = ['SALES_DISCOUNT','BD_DISCOUNT']
											if value123 in precentage_columns:                                                    
												string_val = str(value1234)
												#string_val = string_val.replace('0','')
												string_val1 = string_val.split('.')
												str_val = string_val1[0]
												value1234 = str_val
												if value1234 is not None and value1234 != '':
													new_dict[value123] = (
														'<abbr id ="' + key_value + '" title="' + value1234 +'">' + value1234 +  ' %' +  "</abbr>"
													)
												else:
													new_dict[value123] = (
													'<abbr id ="' + key_value + '" title="' + value1234 + '">' + value1234 + "</abbr>"
												)    
											else:
												img_list = ['PO_NOTES','PRICING_STATUS','EQUIPMENT_STATUS','STATUS']
												if str(ObjectName) == "SAQIFP":
													img_list.append('PRICING_STATUS')
												if value123 in img_list:
													#A055S000P01-15028									#imgValue =imgValue.split(">")[0]
													#imgvalue =str(imgValue)+">"
													Trace.Write("9067"+str(value123))
													imgValue = re.sub(r'>\s+([^>]*?)$','>',imgValue)
													Trace.Write("8981"+str(imgValue))
													new_dict[value123] = ('<abbr id ="' + key_value + '">' + imgValue + "</abbr>")  
												elif RECORD_ID == 'SYOBJR-98872' and value123 == 'LINE':
													Trace.Write("8976")
													new_dict[value123] = ('<abbr id ="' + key_value + '"  title="' + str(value1234).upper() + '">' +str(value1234).upper() + "</abbr>")
												elif RECORD_ID == 'SYOBJR-98873' and value123 == 'SERVICE_ID':
													new_dict[value123] = ('<abbr id ="' + key_value + '"  title="' + str(value1234).upper() + '">' +str(value1234).upper() + "</abbr>")
												else:     
													if RECORD_ID == 'SYOBJR-00009' and value123 == 'DISCOUNT':
														new_dict[value123] = ('<abbr id="discount_'+key_value+'" title="'+str(value1234).upper()+'">'+str(value1234).upper()+'</abbr>')
													elif value123 == "QUOTE_REV_DEAL_TEAM_MEMBER_ID":
														new_dict[value123] = ('<abbr id ="' + key_value + '"  title="' + str(value1234).upper() + '">' +str(value1234).upper() + "</abbr>")
													else:
														Trace.Write("8985")
														#Trace.Write("value1234"+str(value1234)+"key_value"+str(key_value)+"value123"+str(value123))
														new_dict[value123] = value1234
					
					new_dict["ACTIONS"] = Action_str       
					new_dict["ids"] = ids
					new_dict["seg_pric"] = seg_pric
					new_dict["pop_val"] = pop_val
					new_dict["primary"] = primary

				table_list.append(new_dict)
				
				footer_str, footer = "", ""
				footer_tot = ""
				if ObjectName == "SAQIBP" and TreeParam != 'Quote Items':
					ContractRecordId = Product.GetGlobal("contract_quote_record_id")
					gettotaldateamt = Sql.GetList("SELECT BILLING_VALUE=SUM(BILLING_VALUE),ANNUAL_BILLING_AMOUNT = SUM(ANNUAL_BILLING_AMOUNT),BILLING_DATE FROM SAQIBP WHERE BILLING_DATE in {billing_date_column} and QUOTE_RECORD_ID ='{cq}' AND QTEREV_RECORD_ID='{revision_rec_id}' AND SERVICE_ID = '{service_id}' group by BILLING_DATE ".format(cq=str(ContractRecordId),revision_rec_id = quote_revision_record_id,billing_date_column=str(tuple(billing_date_column)),service_id = TreeParam))
					if gettotaldateamt:
						my_format = "{:,." + str(decimal_place) + "f}"
						for val in gettotaldateamt: 
							gettotalamt = str(my_format.format(round(float(val.ANNUAL_BILLING_AMOUNT), int(decimal_place))))  
							
					if gettotaldateamt:
						my_format = "{:,." + str(decimal_place) + "f}"
						footer_tot += '<th colspan="1" class="text-left">{}</th>'.format(curr_symbol)
						footer_tot += '<th colspan="1" class="text-right">{}</th>'.format(gettotalamt)
						for val in gettotaldateamt:
							getamt = str(my_format.format(round(float(val.BILLING_VALUE), int(decimal_place))))
							footer_tot += '<th class="text-right">{}</th>'.format(getamt)					
					
				for key, col_name in enumerate(list(eval(Columns))):                    
					if ObjectName == 'SAQIBP' and TreeParam != 'Quote Items' and (col_name in billing_date_column or col_name == 'QUOTE_CURRENCY'):                        
						try:                            
							if col_name in billing_date_column:                                                
								my_format = "{:,." + str(decimal_place) + "f}"
								tovalue = 0.00
								getamt = ""                        
								#footer += '<th>{}{}</th>'.format(my_format.(sum([float(re.findall(r'value=["](.*?)["]',data.get(col_name))[0].split(" ")[0].replace(",","")) for data in table_list])) ,curr_symbol)
								for data in table_list:                                    
									tovalue += float(re.findall(r'value=["](.*?)["]',data.get(col_name))[0].replace(",",""))
									getamt = str(my_format.format(round(float(tovalue), int(decimal_place))))                               
								footer += '<th class="text-right">{}</th>'.format(getamt)							
							else:
								if table_list:
									currency_obj = re.search(r'>(.+?)<', table_list[0].get(col_name))
									if currency_obj:
										footer += '<th colspan="2" class="text-left">{}</th>'.format(currency_obj.group(1))
									else:
										footer += '<th colspan="2" class="text-left"></th>'
							#footer += '<th>{}{}</th>'.format(sum([float(re.findall(r'value=["](.*?)["]',data.get(col_name))[0].split(" ")[0].replace(",","")) for data in table_list]),curr_symbol)
							#footer += '<th>{}</th>'.format(sum([float(re.findall(r'value=["](.*?)["]',data.get(col_name))[0]) for data in table_list]))
						except Exception:                    
							footer += '<th>0.00</th>'
		if ObjectName == 'SAQIBP' and TreeParam != 'Quote Items':
			#footer_str = '<tfoot><tr><th colspan="7" id= "getbillyear" class="text-left">{}</th>{}</tr></tfoot>'.format(str(SubTab)+" Total", footer)
			footer_str = '<tfoot><tr><th colspan="7" id= "getbill1year" class="text-left">{}</th>{}</tr><tr></tr></tfoot>'.format("GRAND TOTAL", footer_tot)
			#footer_str = '<tfoot><tr><th colspan="7" id= "getbill1year" class="text-left">{}</th>{}</tr><tr><th colspan="9" id= "getbillyear" class="text-left">{}</th>{}</tr></tfoot>'.format("GRAND TOTAL", footer_tot,str(SubTab)+" Total",footer_tot)
			
		if QueryCount==0:
			Page_start=0
		if QueryCount < int(Page_End):
			PageInformS = str(Page_start) + " - " + str(QueryCount) + " of"
		else:
			PageInformS = str(Page_start) + " - " + str(Page_End) + " of"
		dbl_clk_function = ""
		SAQICO_dbl_clk_function = ""
		if ObjectName == 'SAQICO':
			table_ids = "#SYOBJR_00009_E5504B40_36E7_4EA6_9774_EA686705A63F"
			cls = "eq(3)"
			SAQICO_dbl_clk_function += (
				'var checkedRows=[]; localStorage.setItem("multiedit_checkbox_clicked", []); $("'
				+ str(table_ids)
				+ '").on("check.bs.table", function (e, row, $element) { console.log("checked00009==");checkedRows.push($element.closest("tr").find("td:'
				+ str(cls)
				+ '").text()); localStorage.setItem("multiedit_checkbox_clicked", checkedRows); }); $("'
				+ str(table_ids)
				+ '").on("check-all.bs.table", function (e) { var table = $("'
				+ str(table_ids)
				+ '").closest("table"); table.find("tbody tr").each(function() { checkedRows.push($(this).find("td:nth-child(4)").text()); }); localStorage.setItem("multiedit_checkbox_clicked", checkedRows); }); $("'
				+ str(table_ids)
				+ '").on("uncheck-all.bs.table", function (e) { localStorage.setItem("multiedit_checkbox_clicked", []); checkedRows=[]; }); $("'
				+ str(table_ids)
				+ '").on("uncheck.bs.table", function (e, row, $element) { var rec_ids=$element.closest("tr").find("td:'
				+ str(cls)
				+ '").text(); $.each(checkedRows, function(index, value) { if (value === rec_ids) { checkedRows.splice(index,1); }}); localStorage.setItem("multiedit_checkbox_clicked", checkedRows); });'
			)
			# buttons = "<button class=\'btnconfig\' onclick=\'multiedit_RL_cancel();\' type=\'button\' value=\'Cancel\' id=\'cancelButton\'>CANCEL</button><button class=\'btnconfig\' type=\'button\' value=\'Save\' onclick=\'multiedit_save_RL()\' id=\'saveButton\'>SAVE</button>" 

			SAQICO_dbl_clk_function += (    
				'$("'   
				+ str(table_ids)    
				+ '").on("dbl-click-cell.bs.table", onClickCell); $("'  
				+ str(table_ids)    
				+ '").on("all.bs.table", function (e, name, args) { $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); }); $("'  
				+ str(table_ids)    
				+ '\ th.bs-checkbox div.th-inner").before(""); $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); function onClickCell(event, field, value, row, $element) { if(localStorage.getItem("InlineEdit")=="YES"){ return ;} var reco_id=""; var reco = []; reco = localStorage.getItem("multiedit_checkbox_clicked"); if (reco === null || reco === undefined ){ reco = []; } if (reco.length > 0){reco = reco.split(",");} if (reco.length > 0){ reco.push($element.closest("tr").find("td:'   
				+ str(cls)  
				+ '").text());  data1 = $element.closest("tr").find("td:'   
				+ str(cls)  
				+ '").text(); localStorage.setItem("multiedit_save_date", data1); reco_id = removeDuplicates(reco); }else{reco_id=$element.closest("tr").find("td:' 
				+ str(cls)  
				+ '").text(); reco_id=reco_id.split(","); localStorage.setItem("multiedit_save_date", reco_id); } localStorage.setItem("multiedit_data_clicked", reco_id); localStorage.setItem("table_id_RL_edit", "'  
				+ str(table_id) 
				+ '");edit_index = $("'+str(table_ids)+'").find("[data-field="+ field +"]").index()+1;localStorage.setItem("edit_index",edit_index); cpq.server.executeScript("SYBLKETRLG", {"TITLE":field, "VALUE":value, "CLICKEDID":"'   
				+ str(table_id) 
				+ '", "RECORDID":reco_id, "ELEMENT":"RELATEDEDIT"}, function(data) { debugger; data1=data[0]; data2=data[1]; data3 = data[2];if(data1 != "NO"){ if(document.getElementById("RL_EDIT_DIV_ID") ) { localStorage.setItem("saqico_title", field); inp = "#"+data3; $("#SYOBJR_00009_E5504B40_36E7_4EA6_9774_EA686705A63F").find(inp).prop("disabled", false);localStorage.setItem("value_tag", "'+ str(table_id)+' "+inp);$("'+str(table_ids)+'").find("td:nth-child("+edit_index+")").attr("contenteditable", true);  var buttonlen = $("#seginnerbnr").find("button#saveButton"); if (buttonlen.length == 0){  RecId = "SYOBJR-00009";RecName = "div_CTR_Assemblies";$("#seginnerbnr").append("<button class=\'btnconfig\' onclick=\'loadRelatedList(RecId,RecName);\' type=\'button\' value=\'Cancel\' id=\'cancelButton\'>CANCEL</button><button class=\'btnconfig\' type=\'button\' value=\'Save\' onclick=\'multiedit_save_RL()\' id=\'saveButton\'>SAVE</button>");}else{$("#cancelButton").css("display", "block");$("#saveButton").css("display", "block");}$("'+str(table_ids)+' ").find("td:nth-child("+edit_index+")").addClass("light_yellow"); document.getElementById("cont_multiEditModalSection").style.display = "none";  var divHeight = $("#cont_multiEditModalSection").height(); $("#cont_multiEditModalSection .modal-backdrop").css("min-height", divHeight+"px"); $("#cont_multiEditModalSection .modal-dialog").css("width","550px"); $(".modal-dialog").css("margin-top","100px"); } if (data2.length !== 0){ $.each( data2, function( key, values ) { onclick_datepicker(values) }); } } }); }                   $("' 
				+ str(table_ids)    
				+ "\").on('sort.bs.table', function (e, name, order) {  currenttab = $(\"ul#carttabs_head .active\").text().trim(); localStorage.setItem('" 
				+ str(table_id) 
				+ "_SortColumn', name); localStorage.setItem('" 
				+ str(table_id) 
				+ "_SortColumnOrder', order); }); " 
			)   
						
			dbl_clk_function = SAQICO_dbl_clk_function
		return table_list, QueryCount, PageInformS,dbl_clk_function,footer_str


ObjSYLDRTLIST = SYLDRTLIST()
if hasattr(Param, "REC_ID"):
	RECORD_ID = Param.REC_ID

	Product.SetGlobal("REC_ID", str(RECORD_ID))
else:
	RECORD_ID = ""
	
ACTION = Param.ACTION
try:
	PerPage = Param.PerPage
	PageInform = Param.PageInform
except:
	PerPage = ""
	PageInform = ""

try:
	SortColumn = Param.SortColumn
	SortColumnOrder = Param.SortColumnOrder
except:
	SortColumn = ""
	SortColumnOrder = ""

try:
	subTab = Param.SUBTAB

except Exception:
	subTab = "Year 1"

try:
	PR_CURR = Param.PR_CURR
	TP = Param.TP
except:
	PR_CURR = ""
	TP= ""
try:
	equipment_id = Param.equipment_id
except:
	equipment_id = ""

try:
	Currenttab = Param.Currenttab    
except:
	Currenttab = ""
		
try:
	quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
except:
	quote_revision_record_id = None
	
try:
	pricing_picklist_value = Quote.GetCustomField('PRICING_PICKLIST').Content
except:
	pricing_picklist_value = 'Pricing'

try:
	line_item = Param.line_item
except:
	line_item = ""

if ACTION == "PRODUCT_ONLOAD": 
	ApiResponse = ApiResponseFactory.JsonResponse(ObjSYLDRTLIST.MDYNMICSQLOBJECT(RECORD_ID, PerPage, PageInform, subTab, PR_CURR, TP, equipment_id,line_item))
elif ACTION == "PRODUCT_ONLOAD_FILTER":

	ATTRIBUTE_NAME = Param.ATTRIBUTE_NAME
	
	ATTRIBUTE_VALUE = Param.ATTRIBUTE_VALUE
	if RECORD_ID:
		RECORD_ID = "-".join(RECORD_ID.split("_")[:2])
		ApiResponse = ApiResponseFactory.JsonResponse(
			ObjSYLDRTLIST.MDYNMICSQLOBJECTFILTER(
				RECORD_ID, ATTRIBUTE_NAME, ATTRIBUTE_VALUE, PerPage, PageInform, SortColumn, SortColumnOrder, PR_CURR, TP,subTab,line_item
			)
		)

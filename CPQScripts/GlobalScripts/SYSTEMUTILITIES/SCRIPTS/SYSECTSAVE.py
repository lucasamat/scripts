# =========================================================================================================================================
#   __script_name : SYSECTSAVE.PY
#   __script_description :  THIS SCRIPT IS USED TO SAVE THE SEGMENT DATA AND MATERIAL DATA IN CUSTOM TABLES DURING ADD NEW OR EDIT
#   __primary_author__ : JOE EBENEZER
#   __create_date :
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import SYTABACTIN as Table
import Webcom.Configurator.Scripting.Test.TestProduct
import SYCNGEGUID as CPQID
import System.Net
#import PRIFLWTRGR
from datetime import datetime,date
#import datetime
from SYDATABASE import SQL
import CQCPQC4CWB
import CQREVSTSCH
import re

Sql = SQL()
#from PAUPDDRYFG import DirtyFlag

import re
#from datetime import datetime


login_is_admin = User.IsAdmin

def insert_items_billing_plan(contract_quote_record_id=None, total_months=1, billing_date=''):     
	Sql.RunQuery("""INSERT SAQIBP (
					QUOTE_ITEM_BILLING_PLAN_RECORD_ID, BILLING_END_DATE, BILLING_START_DATE, BILLING_TYPE, 
					LINE, QUOTE_ID, QTEITM_RECORD_ID, 
					QUOTE_RECORD_ID,QTEREV_RECORD_ID,QTEREV_ID,
					BILLING_DATE, BILLING_YEAR,
					EQUIPMENT_DESCRIPTION, EQUIPMENT_ID, EQUIPMENT_RECORD_ID, QTEITMCOB_RECORD_ID, 
					SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID,
					SERIAL_NUMBER,
					CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED
				) 
				SELECT 
					CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_BILLING_PLAN_RECORD_ID,  
					SAQICO.WARRANTY_END_DATE as BILLING_END_DATE,
					SAQICO.WARRANTY_START_DATE as BILLING_START_DATE,
					SAQTSE.ENTITLEMENT_VALUE_CODE as BILLING_TYPE,
					SAQICO.LINE AS LINE,                                       
					SAQICO.QUOTE_ID,
					SAQICO.QTEITM_RECORD_ID,					
					SAQICO.QUOTE_RECORD_ID,
					SAQICO.QTEREV_RECORD_ID,
					SAQICO.QTEREV_ID,	
					{BillingDate} as BILLING_DATE,					
					0 as BILLING_YEAR,
					SAQICO.EQUIPMENT_DESCRIPTION,
					SAQICO.EQUIPMENT_ID,					
					SAQICO.EQUIPMENT_RECORD_ID,					
					SAQICO.QUOTE_ITEM_COVERED_OBJECT_RECORD_ID as QTEITMCOB_RECORD_ID,
					SAQICO.SERVICE_DESCRIPTION,
					SAQICO.SERVICE_ID,
					SAQICO.SERVICE_RECORD_ID,
					SAQICO.GREENBOOK,
					SAQICO.GREENBOOK_RECORD_ID,
					SAQICO.SERIAL_NO AS SERIAL_NUMBER,                     
					{UserId} as CPQTABLEENTRYADDEDBY, 
					GETDATE() as CPQTABLEENTRYDATEADDED
				FROM SAQICO (NOLOCK)     
				JOIN SAQTSE (NOLOCK) ON SAQTSE.QUOTE_RECORD_ID = SAQICO.QUOTE_RECORD_ID AND  SAQTSE.QTEREV_RECORD_ID = SAQICO.QTEREV_RECORD_ID AND SAQTSE.ENTITLEMENT_ID = 'FIXED_PRICE_PER_RESOU_EVENT_91'                    
				WHERE SAQICO.QUOTE_RECORD_ID='{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID='{revision_rec_id}'""".format(
					UserId=User.Id, QuoteRecordId=contract_quote_record_id,
					Months=total_months,
					BillingDate=billing_date,
					revision_rec_id = quote_revision_record_id
					))
	return True

def generate_year_based_billing_matrix(billing_plan_data=None):
	if billing_plan_data.get("BILLING_START_DATE") and billing_plan_data.get("BILLING_END_DATE"):
		start_date = datetime.strptime(billing_plan_data.get("BILLING_START_DATE"), '%m/%d/%Y')
		end_date = datetime.strptime(billing_plan_data.get("BILLING_END_DATE"), '%m/%d/%Y')

		diff1 = end_date - start_date

		avgyear = 365.2425        # pedants definition of a year length with leap years
		avgmonth = 365.2425/12.0  # even leap years have 12 months
		years, remainder = divmod(diff1.days, avgyear)
		years, months = int(years), int(remainder // avgmonth)
		""" subtab_details = {}
		subtab_obj = Sql.GetFirst('''
					SELECT SYSTAB.* FROM SYSTAB (NOLOCK)
					JOIN SYOBJH (NOLOCK) SYOBJH.RECORD_ID = SYSTAB.OBJECT_RECORD_ID
					WHERE SYSTAB.SUBTAB_NAME = 'Detail' AND SYOBJH.OBJECT_NAME = 'SAQRIB'
					''')
		if subtab_obj:
			subtab_details.update({
				'TREE_NODE_RECORD_ID':subtab_obj.TREE_NODE_RECORD_ID,
				'SUBTAB_TYPE':'OBJECT RELATED LAYOUT',
				'OBJECT_RECORD_ID':Sql.GetGirst("SELECT RECORD_ID FROM SYOBJH (NOLOCK) WHERE OBJECT_NAME = 'SAQIBP'").RECORD_ID
				'DISPLAY_ORDER':subtab_obj.DISPLAY_ORDER                
			})
		tableInfo = Sql.GetTable("SYSTAB")
			
		for year in range(1, years+1):
			data = {'SUBTAB_RECORD_ID':str(Guid.NewGuid()).upper(), 'SUBTAB_NAME':'Year {}'.format(year)}
			subtab_details['DISPLAY_ORDER'] = subtab_details.get('DISPLAY_ORDER') + 10
			data.update(subtab_details)
			tableInfo.AddRow(newdict)
				Sql.Upsert(tableInfo) """
		contract_quote_record_id = Product.GetGlobal("contract_quote_record_id")
		total_months = years * 12 + months
		Sql.RunQuery("""DELETE FROM SAQIBP WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID='{revision_rec_id}'""".format(QuoteRecordId=contract_quote_record_id,revision_rec_id = quote_revision_record_id))
		for index in range(0, total_months+1):
			insert_items_billing_plan(contract_quote_record_id=contract_quote_record_id, total_months=total_months, 
									billing_date="DATEADD(month, {Month}, '{BillingDate}')".format(
										Month=index, BillingDate=billing_plan_data.get("BILLING_START_DATE")
										))     
			#billing_date = '{}/{}/{}'.format(start_date.month + index, start_date.day, start_date.year)
			#Sql.RunQuery("""UPDATE SAQIBP
			#                        SET BILLING_DATE = DATEADD(month, {Month}, '{BillingDate}')                   
			#                        WHERE QUOTE_RECORD_ID = '{QuoteRecordId}'
			#                        AND ISNULL(BILLING_DATE,'') = ''""".format(
			#            Month=index, BillingDate=billing_plan_data.get("BILLING_START_DATE"), QuoteRecordId=contract_quote_record_id
			#        ))   


	return True




def MaterialSave(ObjectName, RECORD, warning_msg, SectionRecId=None,subtab_name=None):
	row = ""
	result = ""
	RecordId = ""
	disc = []
	newdict = {}
	next_val = ""
	cp_con_factor_result = notification = notificationinterval = ""
	cp_con_factor = ""
	SecRecId = ""
	pricing_sap_prt_num = ""
	RECORD = eval(RECORD)
	billstart = ""
	constartdt = ""
	conenddt = ""
	contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
	quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
	TreeParam = Product.GetGlobal("TreeParam")
	if subtab_name =="Legal SoW":
		Trace.Write("legalsowwwwwwwww")
		get_revesion_values =Sql.GetFirst("Select * FROM SAQTRV WHERE QUOTE_REVISION_RECORD_ID = '{quote_revision_record_id}'".format(quote_revision_record_id = quote_revision_record_id))
		record_value_update = {"QUOTE_REVISION_RECORD_ID":quote_revision_record_id,"QTEREV_ID":get_revesion_values.QTEREV_ID,"REVISION_STATUS":get_revesion_values.REVISION_STATUS,"REV_APPROVE_DATE":get_revesion_values.REV_APPROVE_DATE}
		RECORD.update(record_value_update)

		##Calling the iflow script to update the details in c4c..(cpq to c4c write back...)
		CQCPQC4CWB.writeback_to_c4c("quote_header",Quote.GetGlobal("contract_quote_record_id"),Quote.GetGlobal("quote_revision_record_id"))
		CQCPQC4CWB.writeback_to_c4c("opportunity_header",Quote.GetGlobal("contract_quote_record_id"),Quote.GetGlobal("quote_revision_record_id"))
	 
	if Product.GetGlobal("TreeParentLevel2") == "Quote Items":
		ObjectName = "SAQIGB"
	elif Product.GetGlobal("TreeParentLevel1") == "Quote Items":
		ObjectName = "SAQIFL"
	# elif Product.GetGlobal("TreeParentLevel0") == "Quote Items":
	# 	ObjectName = "SAQITM"
	# 	sect_name = RECORD.get("SECTION_ID")
	# 	Trace.Write("section name = "+str(sect_name))
	elif Product.GetGlobal("TreeParentLevel1") == "Product Offerings":
		ObjectName = "SAQTSV"
	elif Product.GetGlobal("TreeParentLevel2") == "Product Offerings":
		ObjectName = "SAQSFB"
	elif Product.GetGlobal("TreeParentLevel3") == "Product Offerings" and subtab_name == "Details":
		ObjectName = "SAQSGB"
	elif Product.GetGlobal("TreeParentLevel3") == "Product Offerings" and subtab_name == "Equipment Details":
		ObjectName = "SAQSCO"
	Trace.Write("SubTab_Name "+str(subtab_name))
	Trace.Write("RECORD_RECORD "+str(RECORD))
	if str(ObjectName) == "SYPRSN":
		
		permissions_id_val = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00128").GetValue()
		sect_edit = RECORD.get("EDITABLE")
		
		VISIBLEval = RECORD.get("VISIBLE")
		sect_name = RECORD.get("SECTION_ID")
		Trace.Write("section name = "+str(sect_name))
		sect_rec_id = RECORD.get("PROFILE_SECTION_RECORD_ID")
		tableInfosf = Sql.GetTable("SYPRSF")
		newdictSF = {}
		getsection_record = CPQID.KeyCPQId.GetKEYId('SYPRSN', sect_rec_id)
		querySYPRsn = Sql.GetFirst(
			"Select SECTION_RECORD_ID,CpqTableEntryId from SYPRSN where PROFILE_ID = '"
			+ str(permissions_id_val)
			+ "' and PROFILE_SECTION_RECORD_ID = '"
			+ str(getsection_record)
			+ "'"
		)
		newdictsn = {}

		if querySYPRsn:
			TableName = 'SYPRSN'
			tableInfo = Sql.GetTable(TableName)
			newdictsn.update({"CpqTableEntryId": str(querySYPRsn.CpqTableEntryId),"VISIBLE": str(VISIBLEval),"EDITABLE": str(sect_edit)})                
			tableInfo.AddRow(newdictsn)
			Sql.Upsert(tableInfo)
			querySYPRsf = Sql.GetList(
				"Select * from SYPRSF where PROFILE_ID = '"
				+ str(permissions_id_val)
				+ "' and SECTION_RECORD_ID = '"
				+ str(querySYPRsn.SECTION_RECORD_ID)
				+ "'"
			)
			for val in querySYPRsf:
				
				newdictSF["VISIBLE"] = str(VISIBLEval)
				newdictSF["EDITABLE"] = str(sect_edit)
				newdictSF["CpqTableEntryId"] = val.CpqTableEntryId
				
				
				tablerow = newdictSF
				tableInfosf.AddRow(tablerow)
				Sql.Upsert(tableInfosf)
	if str(ObjectName) == "SYPROH":
		
		permissions_id_val = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00128").GetValue()
		objName = RECORD.get("OBJECT_NAME")
		# permissions_id_val = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00128").GetValue()
		
		VISIBLEval = RECORD.get("VISIBLE")
		ObjectNameSection = RECORD.get("OBJECT_NAME")
		CAN_EDIT_VAL = RECORD.get("CAN_EDIT")
		Trace.Write("permissions_id_val--->" + str(permissions_id_val))
		Trace.Write("ObjectNameSection--->" + str(ObjectNameSection))
		CAN_DELETE_VAL = RECORD.get("CAN_DELETE")
		CAN_ADD_VAL = RECORD.get("CAN_ADD")
		Trace.Write(str(CAN_DELETE_VAL) + "40----CAN_EDIT_VAL-----" + str(CAN_EDIT_VAL))
		tableInfo = Sql.GetTable("SYPROD")
		newdict = {}
		newdictH = {}
		newdictF = {}
		tableInfoH = Sql.GetTable("SYPROH")
		querySYPROH = Sql.GetList(
			"Select * from SYPROH where PROFILE_ID = '"
			+ str(permissions_id_val)
			+ "' and OBJECT_NAME = '"
			+ str(objName)
			+ "'"
		)
		if querySYPROH:
			
			for val in querySYPROH:
				if VISIBLEval == "true":
					
					newdictH["VISIBLE"] = VISIBLEval
					newdictH["CAN_EDIT"] = CAN_EDIT_VAL
					newdictH["CAN_ADD"] = CAN_ADD_VAL
					newdictH["CAN_DELETE"] = CAN_DELETE_VAL
					newdictH["CpqTableEntryId"] = val.CpqTableEntryId
				else:
					
					newdictH["VISIBLE"] = VISIBLEval
					newdictH["CAN_EDIT"] = VISIBLEval
					newdictH["CAN_ADD"] = VISIBLEval
					newdictH["CAN_DELETE"] = VISIBLEval
					newdictH["CpqTableEntryId"] = val.CpqTableEntryId
				tablerow = newdictH
				tableInfoH.AddRow(tablerow)
			Sql.Upsert(tableInfoH)
		tableInfoSF = Sql.GetTable("SYPRSF")
		
		querySYPRSF = Sql.GetList(
			"Select * from SYPRSF where PROFILE_ID = '"
			+ str(permissions_id_val)
			+ "' and OBJECT_NAME = '"
			+ str(objName)
			+ "'"
		)
		if querySYPRSF:
			for val in querySYPRSF:
				if VISIBLEval == 1:
					newdictF["VISIBLE"] = VISIBLEval
					newdictF["EDITABLE"] = CAN_EDIT_VAL
					newdictF["CpqTableEntryId"] = val.CpqTableEntryId
				else:
					newdictF["VISIBLE"] = VISIBLEval
					newdictF["EDITABLE"] = VISIBLEval
					newdictF["CpqTableEntryId"] = val.CpqTableEntryId
				# Trace.Write("newdictF--" + str(newdictF))
				tablerow = newdictF
				tableInfoSF.AddRow(tablerow)
			Sql.Upsert(tableInfoSF)
		tableInfoSN = Sql.GetTable("SYPRSN")
		querySYPRSN = Sql.GetList(
			"Select * from SYPRSN where PROFILE_ID = '"
			+ str(permissions_id_val)
			+ "' and OBJECT_NAME = '"
			+ str(objName)
			+ "'"
		)
		if querySYPRSN:
			for val in querySYPRSN:
				
				if VISIBLEval == 1:
					newdictF["VISIBLE"] = VISIBLEval
					newdictF["EDITABLE"] = CAN_EDIT_VAL
					newdictF["CpqTableEntryId"] = val.CpqTableEntryId
				else:
					newdictF["VISIBLE"] = VISIBLEval
					newdictF["EDITABLE"] = VISIBLEval
					newdictF["CpqTableEntryId"] = val.CpqTableEntryId
				tablerow = newdictF
				tableInfoSN.AddRow(tablerow)
			Sql.Upsert(tableInfoSN)

		querySYPROD = Sql.GetList(
			"Select * from SYPROD where PROFILE_ID = '"
			+ str(permissions_id_val)
			+ "' and OBJECT_NAME = '"
			+ str(objName)
			+ "'"
		)
		if querySYPROD:
			
			for val in querySYPROD:
				if VISIBLEval == 1:
					newdict["VISIBLE"] = VISIBLEval
					newdict["EDITABLE"] = CAN_EDIT_VAL

					newdict["CpqTableEntryId"] = val.CpqTableEntryId
				else:
					newdict["VISIBLE"] = VISIBLEval
					newdict["EDITABLE"] = VISIBLEval

					newdict["CpqTableEntryId"] = val.CpqTableEntryId
				tablerow = newdict
				tableInfo.AddRow(tablerow)
			Sql.Upsert(tableInfo)
		tableInfTB = Sql.GetTable("SYPRTB")
		get_tab_rec = Sql.GetList(
			"Select SYPAGE.TAB_RECORD_ID from SYSECT (NOLOCK) INNER JOIN SYPAGE (NOLOCK) on SYSECT.PAGE_RECORD_ID = SYPAGE.RECORD_ID where PRIMARY_OBJECT_NAME = '"
			+ str(ObjectNameSection)
			+ "'"
		)
		newdictTB = {}

		
		if get_tab_rec:
			for val in get_tab_rec:
				if str(val.TAB_RECORD_ID):
					
					permissions_id_val = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00128").GetValue()
					querytab = Sql.GetList(
						"SELECT CpqTableEntryId from SYPRTB WHERE TAB_RECORD_ID='"
						+ str(val.TAB_RECORD_ID)
						+ "' and PROFILE_ID = '"
						+ str(permissions_id_val)
						+ "'"
					)
					if querytab:
						
						for val in querytab:
							
							newdictTB["VISIBLE"] = VISIBLEval

							newdictTB["CpqTableEntryId"] = val.CpqTableEntryId
						tablerow = newdictTB
						tableInfTB.AddRow(tablerow)
					Sql.Upsert(tableInfTB)

	

	ACCOUNT_ID = ""
	ACCOUNT_NAME = ""
	ACCOUNT_RECORD_ID = ""
	cp_con_factor = Metal = CustomValue = ""
	cp_con_factor_result = (
		ErrorequiredDict
	) = (
		ErrorequiredtabDictMSg
	) = (
		ErrorequiredDictMSg
	) = (
		nSpotPriceSpa
	) = (
		nCustomSPAUnits
	) = nAdjSPAUnits = nSpotPriceGpa = nCustomGPAUnits = nAdjGPAUnits = Points_curr_ex_rate_date = Points_curr_ex_rate = ""
	TableName = ObjectName
	Trace.Write("TableName" + str(TableName))
	CURRENCY_SYMBOL = Sql.GetFirst("SELECT CURRENCY_RECORD_ID FROM PRCURR(NOLOCK) WHERE CURRENCY = 'USD'")
	#CURRENCY_SYMBOL_VALUE = CURRENCY_SYMBOL.CURRENCY_RECORD_ID


	
	if TableName != "":
		Trace.Write("SELECT API_NAME FROM SYOBJD WHERE DATA_TYPE = 'AUTO NUMBER' AND OBJECT_NAME = '" + str(TableName) + "'")
		TABLE_OBJS = Sql.GetFirst(
			"SELECT API_NAME FROM SYOBJD WHERE DATA_TYPE = 'AUTO NUMBER' AND OBJECT_NAME = '" + str(TableName) + "'"
		)
		AutoNumb = TABLE_OBJS.API_NAME
		RECID_OBJ = RECORD[str(AutoNumb)]
		RECID_OBJ_SLICE = RECID_OBJ[slice(0, 6)]
		if RECID_OBJ_SLICE == str(TableName):
			RECID = CPQID.KeyCPQId.GetKEYId(str(TableName), str(RECID_OBJ))
		else:
			RECID = RECID_OBJ
		

		RECORD.update({str(AutoNumb): str(RECID)})
		if str(ObjectName) == "ACACSS":
			RECORD.update({"APROBJ_STATUSFIELD_VAL" : RECORD.get("APROBJ_STATUSFIELD_VAL").upper()})
			Trace.Write("Testing ACACSS----" + RECORD.get("APROBJ_STATUSFIELD_VAL"))
		elif str(ObjectName) == "ACACST":
			Trace.Write("Table name------" + str(ObjectName))
			RECORD["APRCHNSTP_NAME"] = str(RECORD.get("APRCHNSTP_NAME").upper())
			if RECORD["REQUIRE_EXPLICIT_APPROVAL"] =='false':
				RECORD["ENABLE_SMARTAPPROVAL"] ='true'
			elif RECORD["REQUIRE_EXPLICIT_APPROVAL"] =='true':
				RECORD["ENABLE_SMARTAPPROVAL"] = 'false'
			Trace.Write("APRCHNSTP_NAME-----"+ str(RECORD["APRCHNSTP_NAME"]))

		
		if str(TableName) == "USERS":
			
			RECORD.pop("RECORDID")
			
		Trace.Write("SELECT * FROM " + str(TableName) + " WHERE " + str(AutoNumb) + "='" + str(RECID) + "'")
		sql_cpq = Sql.GetFirst("SELECT * FROM " + str(TableName) + " WHERE " + str(AutoNumb) + "='" + str(RECID) + "'")
		Trace.Write("SELECT * FROM " + str(TableName) + " WHERE " + str(AutoNumb) + "='" + str(RECID) + "'")
		sql_sgs = Sql.GetList("SELECT API_NAME FROM SYOBJD WHERE OBJECT_NAME='" + str(TableName) + "'")
		if sql_cpq is not None:
			for attr in sql_sgs:
				for KEY in RECORD:
					if str(attr.API_NAME) == KEY:
						newdict[attr.API_NAME] = RECORD[KEY]
					else:
						if str(attr.API_NAME) == "PRICEMODEL_ID":
							KEY = "PRICEMODEL_ID"
							newdict[attr.API_NAME] = RECORD[KEY] if str(TableName) != "PRPBMA" else RECORD[KEY + "_VALUE"]
			
			if str(TableName) != "USERS":
				old_billing_matrix_obj = None
				if TableName == 'SAQRIB':
					billenddate = RECORD.get('BILLING_END_DATE')
					billstartdt = RECORD.get('BILLING_START_DATE')
					billingdateinterval = RECORD.get('BILLING_DAY')
					billstart = datetime.datetime.strptime(billstartdt, '%m/%d/%Y ')
					constart = Product.Attributes.GetByName("QSTN_SYSEFL_QT_00006").GetValue()
					conend = Product.Attributes.GetByName("QSTN_SYSEFL_QT_00007").GetValue()
					billend = datetime.datetime.strptime(billenddate, '%m/%d/%Y ')
					constartdt = datetime.datetime.strptime(constart, '%m/%d/%Y ')
					conenddt = datetime.datetime.strptime(conend, '%m/%d/%Y ')
					old_billing_matrix_obj = Sql.GetFirst("""SELECT BILLING_START_DATE, 
									BILLING_END_DATE, QUOTE_BILLING_PLAN_RECORD_ID, BILLING_DAY
									FROM SAQRIB (NOLOCK) 
									WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'""".format(Product.GetGlobal("contract_quote_record_id"),quote_revision_record_id))
				if billstart >= constartdt and billstart < conenddt :
					if billend > billstart:
						if str(billingdateinterval) <= "31":
							tableInfo = Sql.GetTable(TableName)
							newdict.update({"CpqTableEntryId": str(sql_cpq.CpqTableEntryId)})                
							tableInfo.AddRow(newdict)
							Sql.Upsert(tableInfo)
						else:
							notificationinterval = 'Enter valid Billing Interval '
					else:
						notification = 'Billing Start Date should be less than Billing End Date'
				else:
					# if TableName == "SAQITM":
					# 	if (newdict.has_key("TAX_PERCENTAGE") or newdict.has_key("BD_PRICE_MARGIN") or newdict.has_key("TARGET_PRICE_MARGIN")) and (newdict.get("DISCOUNT") is None or newdict.get("DISCOUNT") == ''):
					# 		newdict["TAX_PERCENTAGE"] = (newdict.get("TAX_PERCENTAGE").replace("%", "").strip())
					# 		newdict["BD_PRICE_MARGIN"] = (newdict.get("BD_PRICE_MARGIN").replace("%", "").strip())
					# 		newdict["TARGET_PRICE_MARGIN"] = (newdict.get("BD_PRICE_MARGIN").replace("%", "").strip())
					# 		dictc = {"CpqTableEntryId": str(sql_cpq.CpqTableEntryId)}
					# 		newdict.update(dictc)
					# 		tableInfo = Sql.GetTable(str(TableName))
					# 		tablerow = newdict
					# 		tableInfo.AddRow(tablerow)
					# 		#Sql.Upsert(tableInfo)
					# 		item_obj = Sql.GetFirst("select SRVTAXCAT_RECORD_ID,SRVTAXCAT_DESCRIPTION,SRVTAXCAT_ID,SRVTAXCLA_DESCRIPTION,SRVTAXCLA_ID,SRVTAXCLA_RECORD_ID from SAQITM where SERVICE_ID = '{Service_id}' and QUOTE_RECORD_ID = '{contract_quote_record_id}' AND QTEREV_RECORD_ID = '{revision_rec_id}'".format(Service_id = '-'.join(TreeParam.split('-')[1:]).strip(),contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id"),revision_rec_id = quote_revision_record_id))
					# 		quote_item_covered_obj = """UPDATE SAQICO SET SRVTAXCAT_ID = '{}',SRVTAXCAT_DESCRIPTION = '{}',SRVTAXCAT_RECORD_ID = '{}',SRVTAXCLA_ID = '{}',SRVTAXCLA_DESCRIPTION = '{}',SRVTAXCLA_RECORD_ID = '{}' where SERVICE_ID = '{}' and QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' """.format(item_obj.SRVTAXCAT_ID,item_obj.SRVTAXCAT_DESCRIPTION,item_obj.SRVTAXCAT_RECORD_ID,item_obj.SRVTAXCLA_ID,item_obj.SRVTAXCLA_DESCRIPTION,item_obj.SRVTAXCLA_RECORD_ID,'-'.join(TreeParam.split('-')[1:]).strip(),Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id )
					# 		Sql.RunQuery(quote_item_covered_obj)
					# 		check_itm_obj = Sql.GetFirst("""SELECT
					# 								QUOTE_ITEM_RECORD_ID,
					# 								CONVERT(int, OBJECT_QUANTITY) as OBJECT_QUANTITY,
					# 								ISNULL(SRVTAXCLA_ID,1) as SRVTAXCLA_ID
					# 								FROM SAQITM (NOLOCK) WHERE QUOTE_RECORD_ID = '{QUOTE_RECORD_ID}' AND QTEREV_RECORD_ID = '{revision_rec_id}' AND SERVICE_ID LIKE '%{SERVICE_ID}%'
					# 								""".format(
					# 		QUOTE_RECORD_ID=Quote.GetGlobal("contract_quote_record_id"), SERVICE_ID=TreeParam.split('-')[1].strip() +" - "+TreeParam.split('-')[2].strip(), revision_rec_id = quote_revision_record_id
					# 		))
					# 		getting_cps_tax(check_itm_obj,'tool')
					# 	elif newdict.has_key("DISCOUNT") and (newdict.get("DISCOUNT") is not None or newdict.get("DISCOUNT") != ''):
					# 		dictc = {"CpqTableEntryId": str(sql_cpq.CpqTableEntryId)}
					# 		newdict["SERVICE_ID"] = TreeParam
					# 		newdict.update(dictc)
					# 		tableInfo = Sql.GetTable(str(TableName))
					# 		tablerow = newdict
					# 		#tableInfo.AddRow(tablerow)
					# 		#Sql.Upsert(tableInfo)
					# 		VALUE = float(newdict.get("DISCOUNT"))
					# 		Trace.Write("Discount = "+str(newdict.get("DISCOUNT")))
					# 		contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
					# 		quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
					# 		ServiceId = TreeParam.split("-")[1].strip()
							
					# 		decimal_discount = VALUE / 100.0
					# 		Sql.RunQuery("""UPDATE SAQICO SET 
					# 										NET_PRICE = ISNULL(TARGET_PRICE,0) - (ISNULL(TARGET_PRICE,0) * {DecimalDiscount}),
					# 										YEAR_1 = ISNULL(TARGET_PRICE,0) - (ISNULL(TARGET_PRICE,0) * {DecimalDiscount}),
					# 										NET_PRICE_INGL_CURR = ISNULL(TARGET_PRICE_INGL_CURR,0) - (ISNULL(TARGET_PRICE_INGL_CURR,0) * {DecimalDiscount}),
					# 										YEAR_1_INGL_CURR = ISNULL(TARGET_PRICE_INGL_CURR,0) - (ISNULL(TARGET_PRICE_INGL_CURR,0) * {DecimalDiscount}),
					# 										DISCOUNT = '{Discount}'
					# 									FROM SAQICO (NOLOCK)                                     
					# 									WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID = '{TreeParam}'""".format(
					# 										QuoteRecordId=contract_quote_record_id,
					# 										RevisionRecordId=quote_revision_record_id,
					# 										DecimalDiscount=decimal_discount if decimal_discount > 0 else 1,
					# 										Discount=VALUE,
					# 										plus="+",
					# 										TreeParam=ServiceId))
					# 		#self._update_year()
					# 		for count in range(2, 6):
					# 			Sql.RunQuery("""UPDATE SAQICO SET
					# 											SAQICO.YEAR_{Year} = CASE  
					# 												WHEN CAST(DATEDIFF(day,SAQTMT.CONTRACT_VALID_FROM,SAQTMT.CONTRACT_VALID_TO) / 365.2425 AS INT) >= {Count} 
					# 													THEN ISNULL(SAQICO.YEAR_{Count}, 0) - (ISNULL(SAQICO.YEAR_{Count}, 0) * ISNULL(SAQICO.YEAR_OVER_YEAR, 0))/100.0                                                   
					# 												ELSE 0
					# 											END,
					# 											SAQICO.YEAR_{Year}_INGL_CURR = CASE  
					# 												WHEN CAST(DATEDIFF(day,SAQTMT.CONTRACT_VALID_FROM,SAQTMT.CONTRACT_VALID_TO) / 365.2425 AS INT) >= {Count} 
					# 													THEN ISNULL(SAQICO.YEAR_{Count}_INGL_CURR, 0) - (ISNULL(SAQICO.YEAR_{Count}_INGL_CURR, 0) * ISNULL(SAQICO.YEAR_OVER_YEAR, 0))/100.0                                                   
					# 												ELSE 0
					# 											END
					# 										FROM SAQICO (NOLOCK) 
					# 										JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQICO.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = SAQICO.QTEREV_RECORD_ID
					# 										WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQICO.SERVICE_ID = '{TreeParam}'""".format(
					# 											QuoteRecordId=contract_quote_record_id,
					# 											RevisionRecordId=quote_revision_record_id,
					# 											Year=count,
					# 											Count=count - 1,
					# 											TreeParam=ServiceId
					# 											)
					# 						)    
					# 		Sql.RunQuery("""UPDATE SAQICO SET 
					# 										NET_VALUE = ISNULL(YEAR_1,0) + ISNULL(YEAR_2,0) + ISNULL(YEAR_3,0) + ISNULL(YEAR_4,0) + ISNULL(YEAR_5,0),
					# 										NET_VALUE_INGL_CURR = ISNULL(YEAR_1_INGL_CURR,0) + ISNULL(YEAR_2_INGL_CURR,0) + ISNULL(YEAR_3_INGL_CURR,0) + ISNULL(YEAR_4_INGL_CURR,0) + ISNULL(YEAR_5_INGL_CURR,0),
					# 										DISCOUNT_AMOUNT_INGL_CURR = TARGET_PRICE_INGL_CURR - NET_PRICE_INGL_CURR 
					# 									FROM SAQICO (NOLOCK)                                     
					# 									WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID = '{TreeParam}'""".format(
					# 										QuoteRecordId=contract_quote_record_id,
					# 										RevisionRecordId=quote_revision_record_id,
					# 										TreeParam=ServiceId
					# 										))
					# 		c = Sql.GetFirst("SELECT SUM(DISCOUNT_AMOUNT_INGL_CURR) AS DISCOUNT_AMOUNT_INGL_CURR,SUM(NET_PRICE) AS SUM_PRICE, SUM(YEAR_1) AS YEAR1, SUM(YEAR_2) AS YEAR2, SUM(YEAR_3) AS YEAR3, SUM(YEAR_4) AS YEAR4, SUM(YEAR_5) AS YEAR5, SUM(NET_PRICE_INGL_CURR) AS SUM_PRICE_INGL_CURR, SUM(YEAR_1_INGL_CURR) AS YEAR1_INGL_CURR, SUM(YEAR_2_INGL_CURR) AS YEAR2_INGL_CURR, SUM(YEAR_3_INGL_CURR) AS YEAR3_INGL_CURR, SUM(YEAR_4_INGL_CURR) AS YEAR4_INGL_CURR, SUM(YEAR_5_INGL_CURR) AS YEAR5_INGL_CURR FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(contract_quote_record_id,ServiceId,quote_revision_record_id))

					# 		FabNetValue = c.YEAR1 + c.YEAR2 + c.YEAR3 + c.YEAR4 + c.YEAR5

					# 		# Sql.RunQuery("UPDATE SAQITM SET DISCOUNT_AMOUNT_INGL_CURR = {DiscountAmt},NET_VALUE = {netvalue},DISCOUNT = {discount},NET_PRICE = '{net_price}',YEAR_1 = {y1},YEAR_2 = {y2},YEAR_3={y3},YEAR_4={y4},YEAR_5 = {y5},NET_PRICE_INGL_CURR = '{net_price_in_gl}',YEAR_1_INGL_CURR = {y1_gl},YEAR_2_INGL_CURR = {y2_gl},YEAR_3_INGL_CURR={y3_gl},YEAR_4_INGL_CURR={y4_gl},YEAR_5_INGL_CURR = {y5_gl}  WHERE QUOTE_RECORD_ID = '{quote_record_id}' AND SERVICE_ID LIKE '%{service_id}%' AND FABLOCATION_ID = '{fab_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}'".format(discount = float(VALUE),net_price = float(c.SUM_PRICE),net_price_in_gl = float(c.SUM_PRICE_INGL_CURR),quote_record_id = contract_quote_record_id,service_id = TreeParentParam.split("-")[1].strip(),fab_id = TreeParam,y1=c.YEAR1,y2=c.YEAR2,y3=c.YEAR3,y4=c.YEAR4,y5=c.YEAR5,y1_gl=c.YEAR1_INGL_CURR,y2_gl=c.YEAR2_INGL_CURR,y3_gl=c.YEAR3_INGL_CURR,y4_gl=c.YEAR4_INGL_CURR,y5_gl=c.YEAR5_INGL_CURR,quote_revision_record_id=quote_revision_record_id,netvalue=FabNetValue,DiscountAmt=c.DISCOUNT_AMOUNT_INGL_CURR))
					# 		Sql.RunQuery("""UPDATE SAQITM
					# 							SET 
					# 							NET_VALUE = IQ.NET_VALUE,
					# 							NET_PRICE = IQ.NET_PRICE,
					# 							YEAR_1 = IQ.YEAR_1,
					# 							YEAR_2 = IQ.YEAR_2,
					# 							YEAR_3 = IQ.YEAR_3,
					# 							YEAR_4 = IQ.YEAR_4,
					# 							YEAR_5 = IQ.YEAR_5,
					# 							NET_VALUE_INGL_CURR = IQ.NET_VALUE_INGL_CURR,
					# 							NET_PRICE_INGL_CURR = IQ.NET_PRICE_INGL_CURR,
					# 							YEAR_1_INGL_CURR = IQ.YEAR_1_INGL_CURR,
					# 							YEAR_2_INGL_CURR = IQ.YEAR_2_INGL_CURR,
					# 							YEAR_3_INGL_CURR = IQ.YEAR_3_INGL_CURR,
					# 							YEAR_4_INGL_CURR = IQ.YEAR_4_INGL_CURR,
					# 							YEAR_5_INGL_CURR = IQ.YEAR_5_INGL_CURR,
					# 							DISCOUNT = '{Discount}'			
					# 							FROM SAQITM (NOLOCK)
					# 							INNER JOIN (SELECT SAQITM.CpqTableEntryId,
					# 										CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.NET_VALUE, 0)), 0), 0) as decimal(18,2)) as NET_VALUE,
					# 										CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.NET_PRICE, 0)), 0), 0) as decimal(18,2)) as NET_PRICE,
					# 										CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_1, 0)), 0), 0) as decimal(18,2)) as YEAR_1,
					# 										CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_2, 0)), 0), 0) as decimal(18,2)) as YEAR_2,
					# 										CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_3, 0)), 0), 0) as decimal(18,2)) as YEAR_3,
					# 										CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_4, 0)), 0), 0) as decimal(18,2)) as YEAR_4,
					# 										CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_5, 0)), 0), 0) as decimal(18,2)) as YEAR_5,
					# 										CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.NET_VALUE_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as NET_VALUE_INGL_CURR,
					# 										CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.NET_PRICE_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as NET_PRICE_INGL_CURR,
					# 										CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_1_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as YEAR_1_INGL_CURR,
					# 										CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_2_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as YEAR_2_INGL_CURR,
					# 										CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_3_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as YEAR_3_INGL_CURR,
					# 										CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_4_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as YEAR_4_INGL_CURR,
					# 										CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_5_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as YEAR_5_INGL_CURR
					# 										FROM SAQITM (NOLOCK) 
					# 										JOIN SAQICO (NOLOCK) ON SAQICO.QUOTE_RECORD_ID = SAQITM.QUOTE_RECORD_ID AND SAQICO.LINE_ITEM_ID = SAQITM.LINE_ITEM_ID
					# 										WHERE SAQITM.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQITM.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQICO.SERVICE_ID LIKE '%{TreeParam}%'
					# 										GROUP BY SAQITM.LINE_ITEM_ID, SAQITM.QUOTE_RECORD_ID, SAQITM.CpqTableEntryId,SAQITM.QTEREV_RECORD_ID)IQ
					# 							ON SAQITM.CpqTableEntryId = IQ.CpqTableEntryId 
					# 							WHERE SAQITM.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQITM.QTEREV_RECORD_ID = '{RevisionRecordId}' """.format(QuoteRecordId=contract_quote_record_id,RevisionRecordId=quote_revision_record_id,
					# 							Discount=VALUE,plus="+",TreeParam=ServiceId))
					# 		Sql.RunQuery("""UPDATE SAQIFL
					# 		SET 
					# 		NET_VALUE = IQ.NET_VALUE,
					# 		NET_PRICE = IQ.NET_PRICE,
					# 		YEAR_1 = IQ.YEAR_1,
					# 		YEAR_2 = IQ.YEAR_2,
					# 		YEAR_3 = IQ.YEAR_3,
					# 		YEAR_4 = IQ.YEAR_4,
					# 		YEAR_5 = IQ.YEAR_5,
					# 		NET_VALUE_INGL_CURR = IQ.NET_VALUE_INGL_CURR,
					# 		NET_PRICE_INGL_CURR = IQ.NET_PRICE_INGL_CURR,
					# 		YEAR_1_INGL_CURR = IQ.YEAR_1_INGL_CURR,
					# 		YEAR_2_INGL_CURR = IQ.YEAR_2_INGL_CURR,
					# 		YEAR_3_INGL_CURR = IQ.YEAR_3_INGL_CURR,
					# 		YEAR_4_INGL_CURR = IQ.YEAR_4_INGL_CURR,
					# 		YEAR_5_INGL_CURR = IQ.YEAR_5_INGL_CURR,
					# 		DISCOUNT_AMOUNT_INGL_CURR = IQ.DISCOUNT_AMOUNT_INGL_CURR,
					# 		DISCOUNT = '{Discount}'					
					# 		FROM  SAQIFL SAQICO (NOLOCK)
					# 		INNER JOIN (SELECT FABLOCATION_ID, SERVICE_ID,QTEREV_RECORD_ID,QUOTE_RECORD_ID,
					# 					CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.NET_VALUE, 0)), 0), 0) as decimal(18,2)) as NET_VALUE,
					# 					CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.NET_PRICE, 0)), 0), 0) as decimal(18,2)) as NET_PRICE,
					# 					CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_1, 0)), 0), 0) as decimal(18,2)) as YEAR_1,
					# 					CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_2, 0)), 0), 0) as decimal(18,2)) as YEAR_2,
					# 					CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_3, 0)), 0), 0) as decimal(18,2)) as YEAR_3,
					# 					CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_4, 0)), 0), 0) as decimal(18,2)) as YEAR_4,
					# 					CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_5, 0)), 0), 0) as decimal(18,2)) as YEAR_5,
					# 					CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.DISCOUNT_AMOUNT_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as DISCOUNT_AMOUNT_INGL_CURR,
					# 					CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.NET_VALUE_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as NET_VALUE_INGL_CURR,
					# 					CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.NET_PRICE_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as NET_PRICE_INGL_CURR,
					# 					CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_1_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as YEAR_1_INGL_CURR,
					# 					CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_2_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as YEAR_2_INGL_CURR,
					# 					CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_3_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as YEAR_3_INGL_CURR,
					# 					CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_4_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as YEAR_4_INGL_CURR,
					# 					CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_5_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as YEAR_5_INGL_CURR
					# 					FROM SAQICO (NOLOCK) 
					# 					WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'
					# 					GROUP BY FABLOCATION_ID, QUOTE_RECORD_ID,QTEREV_RECORD_ID,LINE_ITEM_ID,SERVICE_ID)IQ
					# 		ON SAQICO.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND SAQICO.SERVICE_ID = IQ.SERVICE_ID AND SAQICO.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND SAQICO.FABLOCATION_ID = IQ.FABLOCATION_ID 
					# 		WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{RevisionRecordId}' """.format(QuoteRecordId=contract_quote_record_id,RevisionRecordId=quote_revision_record_id,
					# 		Discount=VALUE))
					# 		Sql.RunQuery("""UPDATE SAQIGB
					# 		SET
					# 		NET_VALUE = IQ.NET_VALUE,
					# 		NET_PRICE = IQ.NET_PRICE,
					# 		YEAR_1 = IQ.YEAR_1,
					# 		YEAR_2 = IQ.YEAR_2,
					# 		YEAR_3 = IQ.YEAR_3,
					# 		YEAR_4 = IQ.YEAR_4,
					# 		YEAR_5 = IQ.YEAR_5,
					# 		DISCOUNT_AMOUNT_INGL_CURR = IQ.DISCOUNT_AMOUNT_INGL_CURR,
					# 		NET_VALUE_INGL_CURR = IQ.NET_VALUE_INGL_CURR,
					# 		NET_PRICE_INGL_CURR = IQ.NET_PRICE_INGL_CURR,
					# 		YEAR_1_INGL_CURR = IQ.YEAR_1_INGL_CURR,
					# 		YEAR_2_INGL_CURR = IQ.YEAR_2_INGL_CURR,
					# 		YEAR_3_INGL_CURR = IQ.YEAR_3_INGL_CURR,
					# 		YEAR_4_INGL_CURR = IQ.YEAR_4_INGL_CURR,
					# 		YEAR_5_INGL_CURR = IQ.YEAR_5_INGL_CURR,
					# 		DISCOUNT = '{Discount}'
					# 		FROM SAQIGB (NOLOCK)
					# 		INNER JOIN (SELECT 
					# 		GREENBOOK_RECORD_ID,
					# 		QUOTE_RECORD_ID,
					# 		SERVICE_ID,
					# 		FABLOCATION_RECORD_ID,
					# 		QTEREV_RECORD_ID,
					# 		CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.NET_VALUE, 0)), 0), 0) as decimal(18,2)) as NET_VALUE,
					# 		CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.NET_PRICE, 0)), 0), 0) as decimal(18,2)) as NET_PRICE,
					# 		CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_1, 0)), 0), 0) as decimal(18,2)) as YEAR_1,
					# 		CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_2, 0)), 0), 0) as decimal(18,2)) as YEAR_2,
					# 		CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_3, 0)), 0), 0) as decimal(18,2)) as YEAR_3,
					# 		CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_4, 0)), 0), 0) as decimal(18,2)) as YEAR_4,
					# 		CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_5, 0)), 0), 0) as decimal(18,2)) as YEAR_5,
					# 		CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.DISCOUNT_AMOUNT_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as DISCOUNT_AMOUNT_INGL_CURR,
					# 		CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.NET_VALUE_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as NET_VALUE_INGL_CURR,
					# 		CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.NET_PRICE_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as NET_PRICE_INGL_CURR,
					# 		CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_1_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as YEAR_1_INGL_CURR,
					# 		CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_2_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as YEAR_2_INGL_CURR,
					# 		CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_3_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as YEAR_3_INGL_CURR,
					# 		CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_4_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as YEAR_4_INGL_CURR,
					# 		CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_5_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as YEAR_5_INGL_CURR
					# 		FROM SAQICO (NOLOCK)
					# 		WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'
					# 		GROUP BY LINE_ITEM_ID, QUOTE_RECORD_ID,QTEREV_RECORD_ID,GREENBOOK_RECORD_ID,SERVICE_ID,FABLOCATION_RECORD_ID)IQ
					# 		ON SAQIGB.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID  AND SAQIGB.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND SAQIGB.SERVICE_ID = IQ.SERVICE_ID AND SAQIGB.FABLOCATION_RECORD_ID = IQ.FABLOCATION_RECORD_ID AND SAQIGB.GREENBOOK_RECORD_ID = IQ.GREENBOOK_RECORD_ID
					# 		WHERE SAQIGB.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQIGB.QTEREV_RECORD_ID = '{RevisionRecordId}' """.format(QuoteRecordId=contract_quote_record_id,RevisionRecordId=quote_revision_record_id,Discount=VALUE))

					# 		quote_currency = str(Quote.GetCustomField('Currency').Content)		
					# 		total_net_price = 0.00		
					# 		total_year_1 = 0.00
					# 		total_year_2 = 0.00
					# 		total_year_3 = 0.00
					# 		total_year_4 = 0.00
					# 		total_year_5 = 0.00
					# 		total_net_value = 0.00
					# 		items_data = {}

					# 		items_obj = Sql.GetList("SELECT SERVICE_ID, LINE_ITEM_ID, ISNULL(YEAR_1, 0) as YEAR_1 ,ISNULL(YEAR_2, 0) as YEAR_2 ,ISNULL(YEAR_3, 0) as YEAR_3 ,ISNULL(YEAR_4, 0) as YEAR_4 ,ISNULL(YEAR_5, 0) as YEAR_5 , ISNULL(NET_VALUE,0) AS NET_VALUE, ISNULL(NET_PRICE, 0) as NET_PRICE FROM SAQITM (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID LIKE '%{}%'".format(contract_quote_record_id,quote_revision_record_id,ServiceId))
					# 		if items_obj:
					# 			for item_obj in items_obj:
					# 				Trace.Write("1---SERVICE ID -->"+str(item_obj.SERVICE_ID))
					# 				items_data[int(float(item_obj.LINE_ITEM_ID))] = {'NET_VALUE':item_obj.NET_VALUE, 'SERVICE_ID':(item_obj.SERVICE_ID.replace('- BASE', '')).strip(), 'YEAR_1':item_obj.YEAR_1, 'YEAR_2':item_obj.YEAR_2, 'NET_PRICE':item_obj.NET_PRICE}
					# 				Trace.Write("2---SERVICE ID -->"+str(item_obj.SERVICE_ID))
					# 		for item in Quote.MainItems:
					# 			item_number = int(item.RolledUpQuoteItem)
					# 			if item_number in items_data.keys():
					# 				if items_data.get(item_number).get('SERVICE_ID') == item.PartNumber:
					# 					item_data = items_data.get(item_number)
					# 					item.NET_PRICE.Value = float(item_data.get('NET_PRICE'))
					# 					total_net_price += item.NET_PRICE.Value
					# 					item.NET_VALUE.Value = item_data.get('NET_VALUE')
					# 					total_net_value += item.NET_VALUE.Value	
					# 					item.YEAR_1.Value = item_data.get('YEAR_1')
					# 					total_year_1 += item.YEAR_1.Value
					# 					item.YEAR_2.Value = item_data.get('YEAR_2')
					# 					total_year_2 += item.YEAR_2.Value
					# 					item.YEAR_3.Value = item_data.get('YEAR_3')
					# 					total_year_3 += item.YEAR_3.Value
					# 					item.YEAR_4.Value = item_data.get('YEAR_4')
					# 					total_year_4 += item.YEAR_4.Value
					# 					item.YEAR_5.Value = item_data.get('YEAR_5')
					# 					total_year_5 += item.YEAR_5.Value
					# 					item.DISCOUNT.Value = "+"+str(VALUE)
					# 		##Added the percentage symbol for discount custom field...
					# 		Percentage = '%'
					# 		# Quote.GetCustomField('DISCOUNT').Content = str(VALUE)+ " " + Percentage
					# 		#discount_value = Quote.GetCustomField('DISCOUNT').Content
					# 		#Trace.Write("discount"+str(discount_value))
					# 		# Quote.GetCustomField('TOTAL_NET_PRICE').Content =str(total_net_price) + " " + quote_currency
					# 		# Quote.GetCustomField('YEAR_1').Content = str(total_year_1) + " " + quote_currency
					# 		# Quote.GetCustomField('YEAR_2').Content = str(total_year_2) + " " + quote_currency
					# 		# Quote.GetCustomField('YEAR_3').Content = str(total_year_3) + " " + quote_currency
					# 		# Quote.GetCustomField('TOTAL_NET_VALUE').Content = str(total_net_value) + " " + quote_currency
					# 		Quote.Save()

					# 		Sql.RunQuery("""UPDATE SAQTRV
					# 						SET 									
					# 						SAQTRV.NET_PRICE_INGL_CURR = IQ.NET_PRICE_INGL_CURR,
					# 						SAQTRV.TOTAL_AMOUNT_INGL_CURR = IQ.NET_VALUE,
											
					# 						SAQTRV.DISCOUNT_PERCENT = '{discount}'
											
					# 						FROM SAQTRV (NOLOCK)
					# 						INNER JOIN (SELECT SAQRIT.QUOTE_RECORD_ID, SAQRIT.QTEREV_RECORD_ID,
					# 									SUM(ISNULL(SAQRIT.NET_PRICE_INGL_CURR, 0)) as NET_PRICE_INGL_CURR,
					# 									SUM(ISNULL(SAQRIT.TOTAL_AMOUNT_INGL_CURR, 0)) as NET_VALUE
														
					# 									FROM SAQRIT (NOLOCK) WHERE SAQRIT.QUOTE_RECORD_ID = '{quote_rec_id}' AND SAQRIT.QTEREV_RECORD_ID = '{quote_revision_rec_id}' GROUP BY SAQRIT.QTEREV_RECORD_ID, SAQRIT.QUOTE_RECORD_ID) IQ ON SAQTRV.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND SAQTRV.QUOTE_REVISION_RECORD_ID = IQ.QTEREV_RECORD_ID
					# 						WHERE SAQTRV.QUOTE_RECORD_ID = '{quote_rec_id}' AND SAQTRV.QUOTE_REVISION_RECORD_ID = '{quote_revision_rec_id}' """.format(discount = str(VALUE),quote_rec_id = contract_quote_record_id,quote_revision_rec_id = quote_revision_record_id))



					# #A055S000P01-4288 start
					if TableName == "SAQTRV":
						dictc = {"CpqTableEntryId": str(sql_cpq.CpqTableEntryId)}
						newdict.update(dictc)
						tableInfo = Sql.GetTable(str(TableName))
						if subtab_name != "Legal SoW":
							newdict["SLSDIS_PRICE_INGL_CURR"] = re.sub('USD','',newdict["SLSDIS_PRICE_INGL_CURR"])
							newdict["BD_PRICE_INGL_CURR"] = re.sub('USD','',newdict["BD_PRICE_INGL_CURR"])
							newdict["CEILING_PRICE_INGL_CURR"] = re.sub('USD','',newdict["CEILING_PRICE_INGL_CURR"])
							newdict["NET_PRICE_INGL_CURR"] = re.sub('USD','',newdict["NET_PRICE_INGL_CURR"])
							newdict["TAX_AMOUNT_INGL_CURR"] = re.sub('USD','',newdict["TAX_AMOUNT_INGL_CURR"])
							newdict["TARGET_PRICE_INGL_CURR"] = re.sub('USD','',newdict["TARGET_PRICE_INGL_CURR"])
							newdict["NET_VALUE_INGL_CURR"] = re.sub('USD','',newdict["NET_VALUE_INGL_CURR"])
							newdict["DISCOUNT_AMOUNT_INGL_CURR"] = re.sub('USD','',newdict["DISCOUNT_AMOUNT_INGL_CURR"])
							newdict["CANCELLATION_PERIOD_EXCEPTION"] = "" if newdict["CANCELLATION_PERIOD"]!="EXCEPTION" else newdict["CANCELLATION_PERIOD_EXCEPTION"]
							exchange_rate_type = newdict.get("EXCHANGE_RATE_TYPE")
							exchange_rate_object = Sql.GetFirst("SELECT  EXCHANGE_RATE,EXCHANGE_RATE_BEGIN_DATE,EXCHANGE_RATE_RECORD_ID FROM PREXRT(NOLOCK) WHERE FROM_CURRENCY = '{}' AND TO_CURRENCY = '{}' AND EXCHANGE_RATE_TYPE = '{}' ".format(newdict.get("GLOBAL_CURRENCY"),newdict.get("DOC_CURRENCY"),newdict.get("EXCHANGE_RATE_TYPE")))
							if exchange_rate_object:
								newdict["EXCHANGE_RATE"] = exchange_rate_object.EXCHANGE_RATE or ""
								newdict["EXCHANGE_RATE_DATE"] = exchange_rate_object.EXCHANGE_RATE_BEGIN_DATE or ""
								newdict["EXCHANGERATE_RECORD_ID"] = exchange_rate_object.EXCHANGE_RATE_RECORD_ID or ""
						tablerow = newdict
						tableInfo.AddRow(tablerow)
						Trace.Write("TEZTZ--475---"+str(tablerow))
						Sql.Upsert(tableInfo)				
						getactive = newdict.get("ACTIVE")
						get_record_val =  newdict.get("QUOTE_REVISION_RECORD_ID")
						get_rev_val =  newdict.get("QTEREV_ID")
						get_approved_date = newdict.get("REV_APPROVE_DATE")
						get_status = newdict.get("REVISION_STATUS")
						if sql_cpq.REVISION_STATUS !="APPROVED" and get_status == "APPROVED":
							Trace.Write('Mail Triggering for Contract Manager')
							result = ScriptExecutor.ExecuteGlobal("ACSECTACTN", {"ACTION": "CBC_MAIL_TRIGGER"})
						if getactive == 'false':
							getactive = 0
						else:
							getactive = 1
						contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
						quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
						if getactive == 1:
							update_quote_rev = Sql.RunQuery("""UPDATE SAQTRV SET ACTIVE = {active_rev} WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' and  QUOTE_REVISION_RECORD_ID != '{get_record_val}'""".format(QuoteRecordId=contract_quote_record_id,active_rev = 0,get_record_val =get_record_val))
							Sql.RunQuery("""UPDATE SAQTMT SET QTEREV_ID = {newrev_inc},QTEREV_RECORD_ID = '{quote_revision_id}',ACTIVE_REV={active_rev} WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{QuoteRecordId}'""".format(quote_revision_id=get_record_val,newrev_inc= get_rev_val,QuoteRecordId=contract_quote_record_id,active_rev = 1))
						
						productdesc = SqlHelper.GetFirst("sp_executesql @t=N'update CART_REVISIONS set DESCRIPTION =''"+str(newdict.get("REVISION_DESCRIPTION"))+"'' where CART_ID = ''"+str(Quote.QuoteId)+"'' and VISITOR_ID =''"+str(Quote.UserId)+"''  '")
						get_quote_info_details = Sql.GetFirst("select * from SAQTMT where QUOTE_ID = '"+str(Quote.CompositeNumber)+"'")
						Quote.SetGlobal("contract_quote_record_id",get_quote_info_details.MASTER_TABLE_QUOTE_RECORD_ID)
						Quote.SetGlobal("quote_revision_record_id",str(get_quote_info_details.QTEREV_RECORD_ID))
						##Calling the iflow script to update the details in c4c..(cpq to c4c write back...)
						CQCPQC4CWB.writeback_to_c4c("quote_header",contract_quote_record_id,quote_revision_record_id)
						CQCPQC4CWB.writeback_to_c4c("opportunity_header",contract_quote_record_id,quote_revision_record_id)
						if get_status.upper() == "APPROVED":
							##Updating the Revision Approved Date while changing the status to Approved...
							if get_approved_date == "":
								RevisionApprovedDate = datetime.now().date()
								Sql.RunQuery("UPDATE SAQTRV SET REV_APPROVE_DATE = '{RevisionApprovedDate}' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' ".format(RevisionApprovedDate = RevisionApprovedDate,QuoteRecordId = Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id")))
							##Updating the Revision Approved Date while changing the status to Approved...
							#crm_result = ScriptExecutor.ExecuteGlobal('QTPOSTACRM',{'QUOTE_ID':str(newdict.get("QUOTE_ID")),'REVISION_ID':str(get_rev_val),'Fun_type':'cpq_to_crm'})
					#A055S000P01-4288 end

					if TreeParam == "Quote Information":

						contract_quote_record_id = Product.GetGlobal("contract_quote_record_id")
						quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")

						product_offering_contract_validity = Sql.GetFirst("SELECT CONTRACT_VALID_FROM, CONTRACT_VALID_TO FROM SAQTRV (NOLOCK) WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}'".format(Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id)))

						# max_validity_date = Sql.GetFirst("SELECT MAX(CONTRACT_VALID_FROM) AS CONTRACT_VALID_FROM FROM SAQSFB (NOLOCK) WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}'".format(Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id)))

						# min_validity_date = Sql.GetFirst("SELECT MIN(CONTRACT_VALID_FROM) AS CONTRACT_VALID_TO FROM SAQSFB (NOLOCK) WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}'".format(Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id)))

						service_contract_update = "UPDATE SAQTSV SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}'".format(valid_from= product_offering_contract_validity.CONTRACT_VALID_FROM, valid_to =   product_offering_contract_validity.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id))


						fab_contract_update = "UPDATE SAQSFB SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}'".format(valid_from= product_offering_contract_validity.CONTRACT_VALID_FROM, valid_to =   product_offering_contract_validity.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id))

						greenbook_contract_update = "UPDATE SAQSGB SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}'".format(valid_from= product_offering_contract_validity.CONTRACT_VALID_FROM, valid_to =   product_offering_contract_validity.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id))


						equipment_contract_update = "UPDATE SAQSCO SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}'".format(valid_from= product_offering_contract_validity.CONTRACT_VALID_FROM, valid_to =   product_offering_contract_validity.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id))

						assembly_contract_update = "UPDATE SAQSCA SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}'".format(valid_from= product_offering_contract_validity.CONTRACT_VALID_FROM, valid_to =   product_offering_contract_validity.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id))

						# saqitm_contract_update = "UPDATE SAQITM SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}'".format(valid_from= product_offering_contract_validity.CONTRACT_VALID_FROM, valid_to =   product_offering_contract_validity.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id))

						# saqifl_contract_update = "UPDATE SAQIFL SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}'".format(valid_from= product_offering_contract_validity.CONTRACT_VALID_FROM, valid_to =   product_offering_contract_validity.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id))

						# saqigb_contract_update = "UPDATE SAQIGB SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}'".format(valid_from= product_offering_contract_validity.CONTRACT_VALID_FROM, valid_to =   product_offering_contract_validity.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id))

						saqico_contract_update = "UPDATE SAQICO SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}'".format(valid_from= product_offering_contract_validity.CONTRACT_VALID_FROM, valid_to =   product_offering_contract_validity.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id))

						# saqtrv_contract_update = "UPDATE SAQTRV SET CONTRACT_VALID_FROM = '{min_validity_date}' , CONTRACT_VALID_TO = '{max_validity_date}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}'".format(max_validity_date= max_validity_date.CONTRACT_VALID_FROM, min_validity_date =   min_validity_date.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id))

						Sql.RunQuery(service_contract_update)
						Sql.RunQuery(fab_contract_update)
						Sql.RunQuery(greenbook_contract_update)
						Sql.RunQuery(equipment_contract_update)
						Sql.RunQuery(assembly_contract_update)
						# Sql.RunQuery(saqitm_contract_update)
						# Sql.RunQuery(saqifl_contract_update)
						# Sql.RunQuery(saqigb_contract_update)
						Sql.RunQuery(saqico_contract_update)
						# Sql.RunQuery(saqtrv_contract_update)

					# elif TableName == "SAQIGB":
					# 	dictc = {"CpqTableEntryId": str(sql_cpq.CpqTableEntryId)}
					# 	newdict.update(dictc)
					# 	tableInfo = Sql.GetTable(str(TableName))
					# 	tablerow = newdict
					# 	tableInfo.AddRow(tablerow)
					# 	Sql.Upsert(tableInfo)
					# 	VALUE = float(newdict.get("DISCOUNT"))
					# 	Trace.Write("Discount = "+str(newdict.get("DISCOUNT")))
					# 	contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
					# 	quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
					# 	decimal_discount = VALUE / 100.0
					# 	Sql.RunQuery("""UPDATE SAQICO SET 
					# 									NET_PRICE = ISNULL(TARGET_PRICE,0) - (ISNULL(TARGET_PRICE,0) * {DecimalDiscount}),NET_PRICE_INGL_CURR =ISNULL(TARGET_PRICE_INGL_CURR,0) + (ISNULL(TARGET_PRICE_INGL_CURR,0) * {DecimalDiscount}),
					# 									YEAR_1 = ISNULL(TARGET_PRICE,0) - (ISNULL(TARGET_PRICE,0) * {DecimalDiscount}),
					# 									DISCOUNT = '{Discount}',YEAR_1_INGL_CURR = ISNULL(TARGET_PRICE_INGL_CURR,0) + (ISNULL(TARGET_PRICE_INGL_CURR,0) * {DecimalDiscount})
					# 								FROM SAQICO (NOLOCK)                                     
					# 								WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND GREENBOOK = '{TreeParam}' AND FABLOCATION_ID = '{TreeParentParam}'""".format(
					# 									QuoteRecordId=contract_quote_record_id,
					# 									RevisionRecordId=quote_revision_record_id,
					# 									DecimalDiscount=decimal_discount if decimal_discount > 0 else 1,
					# 									Discount=VALUE,
					# 									plus="+",
					# 									TreeParam=TreeParam,TreeParentParam=TreeParentParam))
					# 	#self._update_year()
					# 	for count in range(2, 6):
					# 		Sql.RunQuery("""UPDATE SAQICO SET
					# 										SAQICO.YEAR_{Year} = CASE  
					# 											WHEN CAST(DATEDIFF(day,SAQTMT.CONTRACT_VALID_FROM,SAQTMT.CONTRACT_VALID_TO) / 365.2425 AS INT) >= {Count} 
					# 												THEN ISNULL(SAQICO.YEAR_{Count}, 0) - (ISNULL(SAQICO.YEAR_{Count}, 0) * ISNULL(SAQICO.YEAR_OVER_YEAR, 0))/100.0                                                   
					# 											ELSE 0
					# 										END, SAQICO.YEAR_{Year}_INGL_CURR = CASE  
					# 											WHEN CAST(DATEDIFF(day,SAQTMT.CONTRACT_VALID_FROM,SAQTMT.CONTRACT_VALID_TO) / 365.2425 AS INT) >= {Count} 
					# 												THEN ISNULL(SAQICO.YEAR_{Count}_INGL_CURR, 0) - (ISNULL(SAQICO.YEAR_{Count}_INGL_CURR, 0) * ISNULL(SAQICO.YEAR_OVER_YEAR, 0))/100.0                                                   
					# 											ELSE 0
					# 										END
					# 									FROM SAQICO (NOLOCK) 
					# 									JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQICO.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = SAQICO.QTEREV_RECORD_ID
					# 									WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQICO.GREENBOOK = '{TreeParam}' AND SAQICO.FABLOCATION_ID = '{TreeParentParam}'""".format(
					# 										QuoteRecordId=contract_quote_record_id,
					# 										RevisionRecordId=quote_revision_record_id,
					# 										Year=count,
					# 										Count=count - 1,
					# 										TreeParam=TreeParam,
					# 										TreeParentParam=TreeParentParam
					# 										)
					# 					)    
					# 	Sql.RunQuery("""UPDATE SAQICO SET 
					# 									NET_VALUE = ISNULL(YEAR_1,0) + ISNULL(YEAR_2,0) + ISNULL(YEAR_3,0) + ISNULL(YEAR_4,0) + ISNULL(YEAR_5,0),
					# 									NET_VALUE_INGL_CURR = ISNULL(YEAR_1_INGL_CURR,0) + ISNULL(YEAR_2_INGL_CURR,0) + ISNULL(YEAR_3_INGL_CURR,0) + ISNULL(YEAR_4_INGL_CURR,0) + ISNULL(YEAR_5_INGL_CURR,0),
					# 									DISCOUNT_AMOUNT_INGL_CURR = TARGET_PRICE_INGL_CURR - NET_PRICE_INGL_CURR 
					# 								FROM SAQICO (NOLOCK)                                     
					# 								WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND GREENBOOK = '{TreeParam}' AND FABLOCATION_ID = '{TreeParentParam}'""".format(
					# 									QuoteRecordId=contract_quote_record_id,
					# 									RevisionRecordId=quote_revision_record_id,
					# 									TreeParam=TreeParam,
					# 									TreeParentParam=TreeParentParam
					# 									))
					# 	c = Sql.GetFirst("SELECT SUM(DISCOUNT_AMOUNT_INGL_CURR) AS DISCOUNT_AMOUNT_INGL_CURR,SUM(NET_PRICE) AS SUM_PRICE,SUM(NET_PRICE_INGL_CURR) AS SUM_PRICE_INGL_CURR, SUM(YEAR_1) AS YEAR1, SUM(YEAR_1_INGL_CURR) AS YEAR1_INGL_CURR, SUM(YEAR_2) AS YEAR2,SUM(YEAR_2_INGL_CURR) AS YEAR2_INGL_CURR, SUM(YEAR_3) AS YEAR3, SUM(YEAR_3_INGL_CURR) AS YEAR3_INGL_CURR, SUM(YEAR_4) AS YEAR4, SUM(YEAR_4_INGL_CURR) AS YEAR4_INGL_CURR, SUM(YEAR_5) AS YEAR5, SUM(YEAR_5_INGL_CURR) AS YEAR5_INGL_CURR FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}' AND GREENBOOK = '{}'  AND FABLOCATION_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(contract_quote_record_id,TreeSuperParentParam.split("-")[1].strip(),TreeParam,TreeParentParam,quote_revision_record_id))

					# 	GreenbookNetValue = c.YEAR1 + c.YEAR2 + c.YEAR3 + c.YEAR4 + c.YEAR5
						
					# 	Sql.RunQuery("UPDATE SAQIGB SET DISCOUNT_AMOUNT_INGL_CURR = {DiscountAmt},NET_VALUE = {netvalue},NET_PRICE = '{}',YEAR_1 = {y1},YEAR_2 = {y2},YEAR_3={y3},YEAR_4={y4},YEAR_5 = {y5},NET_PRICE_INGL_CURR = '{}',YEAR_1_INGL_CURR = {y1_gl},YEAR_2_INGL_CURR = {y2_gl},YEAR_3_INGL_CURR={y3_gl},YEAR_4_INGL_CURR={y4_gl},YEAR_5_INGL_CURR = {y5_gl}  WHERE QUOTE_RECORD_ID = '{}' AND SERVICE_ID LIKE '%{}%' AND GREENBOOK = '{}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND FABLOCATION_ID = '{TreeParentParam}'".format(float(c.SUM_PRICE),float(c.SUM_PRICE_INGL_CURR),contract_quote_record_id,TreeSuperParentParam.split("-")[1].strip(),TreeParam,y1=c.YEAR1,y2=c.YEAR2,y3=c.YEAR3,y4=c.YEAR4,y5=c.YEAR5,y1_gl=c.YEAR1_INGL_CURR,y2_gl=c.YEAR2_INGL_CURR,y3_gl=c.YEAR3_INGL_CURR,y4_gl=c.YEAR4_INGL_CURR,y5_gl=c.YEAR5_INGL_CURR,quote_revision_record_id=quote_revision_record_id,TreeParentParam=TreeParentParam,netvalue=GreenbookNetValue,DiscountAmt=c.DISCOUNT_AMOUNT_INGL_CURR))
						
					# 	# Sql.RunQuery("""UPDATE SAQITM
					# 	# 					SET 
					# 	# 					NET_VALUE = IQ.NET_VALUE,
					# 	# 					NET_PRICE = IQ.NET_PRICE,
					# 	# 					YEAR_1 = IQ.YEAR_1,
					# 	# 					YEAR_2 = IQ.YEAR_2,
					# 	# 					YEAR_3 = IQ.YEAR_3,
					# 	# 					YEAR_4 = IQ.YEAR_4,
					# 	# 					YEAR_5 = IQ.YEAR_5,
					# 	# 					NET_VALUE_INGL_CURR = IQ.NET_VALUE_INGL_CURR,
					# 	# 					NET_PRICE_INGL_CURR = IQ.NET_PRICE_INGL_CURR,
					# 	# 					YEAR_1_INGL_CURR = IQ.YEAR_1_INGL_CURR,
					# 	# 					YEAR_2_INGL_CURR = IQ.YEAR_2_INGL_CURR,
					# 	# 					YEAR_3_INGL_CURR = IQ.YEAR_3_INGL_CURR,
					# 	# 					YEAR_4_INGL_CURR = IQ.YEAR_4_INGL_CURR,
					# 	# 					YEAR_5_INGL_CURR = IQ.YEAR_5_INGL_CURR,
					# 	# 					DISCOUNT = '{Discount}'					
					# 	# 					FROM SAQITM (NOLOCK)
					# 	# 					INNER JOIN (SELECT SAQITM.CpqTableEntryId,
					# 	# 								CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.NET_VALUE, 0)), 0), 0) as decimal(18,2)) as NET_VALUE,
					# 	# 								CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.NET_PRICE, 0)), 0), 0) as decimal(18,2)) as NET_PRICE,
					# 	# 								CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_1, 0)), 0), 0) as decimal(18,2)) as YEAR_1,
					# 	# 								CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_2, 0)), 0), 0) as decimal(18,2)) as YEAR_2,
					# 	# 								CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_3, 0)), 0), 0) as decimal(18,2)) as YEAR_3,
					# 	# 								CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_4, 0)), 0), 0) as decimal(18,2)) as YEAR_4,
					# 	# 								CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_5, 0)), 0), 0) as decimal(18,2)) as YEAR_5,
					# 	# 								CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.NET_VALUE_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as NET_VALUE_INGL_CURR,
					# 	# 								CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.NET_PRICE_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as NET_PRICE_INGL_CURR,
					# 	# 								CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_1_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as YEAR_1_INGL_CURR,
					# 	# 								CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_2_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as YEAR_2_INGL_CURR,
					# 	# 								CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_3_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as YEAR_3_INGL_CURR,
					# 	# 								CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_4_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as YEAR_4_INGL_CURR,
					# 	# 								CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_5_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as YEAR_5_INGL_CURR
					# 	# 								FROM SAQITM (NOLOCK) 
					# 	# 								JOIN SAQICO (NOLOCK) ON SAQICO.QUOTE_RECORD_ID = SAQITM.QUOTE_RECORD_ID AND SAQICO.LINE_ITEM_ID = SAQITM.LINE_ITEM_ID
					# 	# 								WHERE SAQITM.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQITM.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQICO.GREENBOOK = '{TreeParam}' AND SAQICO.FABLOCATION_ID = '{TreeParentParam}'
					# 	# 								GROUP BY SAQITM.LINE_ITEM_ID, SAQITM.QUOTE_RECORD_ID, SAQITM.CpqTableEntryId,SAQITM.QTEREV_RECORD_ID)IQ
					# 	# 					ON SAQITM.CpqTableEntryId = IQ.CpqTableEntryId 
					# 	# 					WHERE SAQITM.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQITM.QTEREV_RECORD_ID = '{RevisionRecordId}' """.format(QuoteRecordId=contract_quote_record_id,RevisionRecordId=quote_revision_record_id,
					# 	# 					Discount=VALUE,plus="+",TreeParam=TreeParam,TreeParentParam=TreeParentParam))
						
					# 	quote_currency = str(Quote.GetCustomField('Currency').Content)		
					# 	total_net_price = 0.00		
					# 	total_year_1 = 0.00
					# 	total_year_2 = 0.00
					# 	total_year_3 = 0.00
					# 	total_year_4 = 0.00
					# 	total_year_5 = 0.00
					# 	total_net_value = 0.00
					# 	items_data = {}

					# 	# items_obj = Sql.GetList("SELECT SERVICE_ID, LINE_ITEM_ID, ISNULL(YEAR_1, 0) as YEAR_1 ,ISNULL(YEAR_2, 0) as YEAR_2 ,ISNULL(YEAR_3, 0) as YEAR_3,ISNULL(YEAR_4, 0) as YEAR_4,ISNULL(YEAR_5, 0) as YEAR_5, ISNULL(NET_VALUE,0) AS NET_VALUE, ISNULL(NET_PRICE, 0) as NET_PRICE FROM SAQITM (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(contract_quote_record_id,quote_revision_record_id,TreeParam))
						
					# 	# if items_obj:
					# 	# 	for item_obj in items_obj:
					# 	# 		items_data[int(float(item_obj.LINE_ITEM_ID))] = {'NET_VALUE':item_obj.NET_VALUE, 'SERVICE_ID':(item_obj.SERVICE_ID.replace('- BASE', '')).strip(), 'YEAR_1':item_obj.YEAR_1, 'YEAR_2':item_obj.YEAR_2,'YEAR_3':item_obj.YEAR_3,'YEAR_4':item_obj.YEAR_4,'YEAR_5':item_obj.YEAR_5, 'NET_PRICE':item_obj.NET_PRICE}
						
					# 	for item in Quote.MainItems:
					# 		item_number = int(item.RolledUpQuoteItem)
					# 		if item_number in items_data.keys():
					# 			if items_data.get(item_number).get('SERVICE_ID') == item.PartNumber:
					# 				item_data = items_data.get(item_number)
					# 				item.NET_PRICE.Value = float(item_data.get('NET_PRICE'))
					# 				total_net_price += item.NET_PRICE.Value
					# 				item.NET_VALUE.Value = item_data.get('NET_VALUE')
					# 				total_net_value += item.NET_VALUE.Value	
					# 				item.YEAR_1.Value = item_data.get('YEAR_1')
					# 				total_year_1 += item.YEAR_1.Value
					# 				item.YEAR_2.Value = item_data.get('YEAR_2')
					# 				total_year_2 += item.YEAR_2.Value
					# 				item.YEAR_3.Value = item_data.get('YEAR_3')
					# 				total_year_3 += item.YEAR_2.Value
					# 				item.YEAR_4.Value = item_data.get('YEAR_4')
					# 				total_year_4 += item.YEAR_4.Value
					# 				item.YEAR_5.Value = item_data.get('YEAR_5')
					# 				total_year_5 += item.YEAR_5.Value
					# 				item.DISCOUNT.Value = str(VALUE)
					# 	##Added the percentage symbol for discount custom field...
					# 	Percentage = '%'
					# 	# Quote.GetCustomField('DISCOUNT').Content = str(VALUE)+ " " + Percentage
					# 	#discount_value = Quote.GetCustomField('DISCOUNT').Content
					# 	#Trace.Write("discount"+str(discount_value))
					# 	# Quote.GetCustomField('TOTAL_NET_PRICE').Content =str(total_net_price) + " " + quote_currency
					# 	# Quote.GetCustomField('YEAR_1').Content = str(total_year_1) + " " + quote_currency
					# 	# Quote.GetCustomField('YEAR_2').Content = str(total_year_2) + " " + quote_currency
					# 	# Quote.GetCustomField('YEAR_3').Content = str(total_year_3) + " " + quote_currency
					# 	# Quote.GetCustomField('TOTAL_NET_VALUE').Content = str(total_net_value) + " " + quote_currency
					# 	Sql.RunQuery("""UPDATE SAQTRV
					# 						SET 									
					# 						SAQTRV.NET_PRICE_INGL_CURR = IQ.NET_PRICE_INGL_CURR,
					# 						SAQTRV.TOTAL_AMOUNT_INGL_CURR = IQ.NET_VALUE,
											
					# 						SAQTRV.DISCOUNT_PERCENT = '{discount}'
											
					# 						FROM SAQTRV (NOLOCK)
					# 						INNER JOIN (SELECT SAQRIT.QUOTE_RECORD_ID, SAQRIT.QTEREV_RECORD_ID,
					# 									SUM(ISNULL(SAQRIT.NET_PRICE_INGL_CURR, 0)) as NET_PRICE_INGL_CURR,
					# 									SUM(ISNULL(SAQRIT.TOTAL_AMOUNT_INGL_CURR, 0)) as NET_VALUE
														
					# 									FROM SAQRIT (NOLOCK) WHERE SAQRIT.QUOTE_RECORD_ID = '{quote_rec_id}' AND SAQRIT.QTEREV_RECORD_ID = '{quote_revision_rec_id}' GROUP BY SAQRIT.QTEREV_RECORD_ID, SAQRIT.QUOTE_RECORD_ID) IQ ON SAQTRV.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND SAQTRV.QUOTE_REVISION_RECORD_ID = IQ.QTEREV_RECORD_ID
					# 						WHERE SAQTRV.QUOTE_RECORD_ID = '{quote_rec_id}' AND SAQTRV.QUOTE_REVISION_RECORD_ID = '{quote_revision_rec_id}' """.format(discount = str(VALUE),quote_rec_id = contract_quote_record_id,quote_revision_rec_id = quote_revision_record_id))

					# 	Quote.Save()
					# elif TableName == "SAQIFL":
					# 	dictc = {"CpqTableEntryId": str(sql_cpq.CpqTableEntryId)}
					# 	newdict.update(dictc)
					# 	tableInfo = Sql.GetTable(str(TableName))
					# 	tablerow = newdict
					# 	tableInfo.AddRow(tablerow)
					# 	Sql.Upsert(tableInfo)
					# 	VALUE = float(newdict.get("DISCOUNT"))
					# 	Trace.Write("Discount = "+str(newdict.get("DISCOUNT")))
					# 	contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
					# 	quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
					# 	decimal_discount = VALUE / 100.0
					# 	Sql.RunQuery("""UPDATE SAQICO SET 
					# 									NET_PRICE = ISNULL(TARGET_PRICE,0) - (ISNULL(TARGET_PRICE,0) * {DecimalDiscount}),
					# 									YEAR_1 = ISNULL(TARGET_PRICE,0) - (ISNULL(TARGET_PRICE,0) * {DecimalDiscount}),
					# 									NET_PRICE_INGL_CURR = ISNULL(TARGET_PRICE_INGL_CURR,0) - (ISNULL(TARGET_PRICE_INGL_CURR,0) * {DecimalDiscount}),
					# 									YEAR_1_INGL_CURR = ISNULL(TARGET_PRICE_INGL_CURR,0) - (ISNULL(TARGET_PRICE_INGL_CURR,0) * {DecimalDiscount}),
					# 									DISCOUNT = '{Discount}'
					# 								FROM SAQICO (NOLOCK)                                     
					# 								WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND FABLOCATION_ID = '{TreeParam}'""".format(
					# 									QuoteRecordId=contract_quote_record_id,
					# 									RevisionRecordId=quote_revision_record_id,
					# 									DecimalDiscount=decimal_discount if decimal_discount > 0 else 1,
					# 									Discount=VALUE,
					# 									plus="+",
					# 									TreeParam=TreeParam))
					# 	#self._update_year()
					# 	for count in range(2, 6):
					# 		Sql.RunQuery("""UPDATE SAQICO SET
					# 										SAQICO.YEAR_{Year} = CASE  
					# 											WHEN CAST(DATEDIFF(day,SAQTMT.CONTRACT_VALID_FROM,SAQTMT.CONTRACT_VALID_TO) / 365.2425 AS INT) >= {Count} 
					# 												THEN ISNULL(SAQICO.YEAR_{Count}, 0) - (ISNULL(SAQICO.YEAR_{Count}, 0) * ISNULL(SAQICO.YEAR_OVER_YEAR, 0))/100.0                                                   
					# 											ELSE 0
					# 										END,
					# 										SAQICO.YEAR_{Year}_INGL_CURR = CASE  
					# 											WHEN CAST(DATEDIFF(day,SAQTMT.CONTRACT_VALID_FROM,SAQTMT.CONTRACT_VALID_TO) / 365.2425 AS INT) >= {Count} 
					# 												THEN ISNULL(SAQICO.YEAR_{Count}_INGL_CURR, 0) - (ISNULL(SAQICO.YEAR_{Count}_INGL_CURR, 0) * ISNULL(SAQICO.YEAR_OVER_YEAR, 0))/100.0                                                   
					# 											ELSE 0
					# 										END
					# 									FROM SAQICO (NOLOCK) 
					# 									JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQICO.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = SAQICO.QTEREV_RECORD_ID
					# 									WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQICO.FABLOCATION_ID = '{TreeParam}'""".format(
					# 										QuoteRecordId=contract_quote_record_id,
					# 										RevisionRecordId=quote_revision_record_id,
					# 										Year=count,
					# 										Count=count - 1,
					# 										TreeParam=TreeParam
					# 										)
					# 					)    
					# 	Sql.RunQuery("""UPDATE SAQICO SET 
					# 									NET_VALUE = ISNULL(YEAR_1,0) + ISNULL(YEAR_2,0) + ISNULL(YEAR_3,0) + ISNULL(YEAR_4,0) + ISNULL(YEAR_5,0),
					# 									NET_VALUE_INGL_CURR = ISNULL(YEAR_1_INGL_CURR,0) + ISNULL(YEAR_2_INGL_CURR,0) + ISNULL(YEAR_3_INGL_CURR,0) + ISNULL(YEAR_4_INGL_CURR,0) + ISNULL(YEAR_5_INGL_CURR,0),
					# 									DISCOUNT_AMOUNT_INGL_CURR = TARGET_PRICE_INGL_CURR - NET_PRICE_INGL_CURR 
					# 								FROM SAQICO (NOLOCK)                                     
					# 								WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND FABLOCATION_ID = '{TreeParam}'""".format(
					# 									QuoteRecordId=contract_quote_record_id,
					# 									RevisionRecordId=quote_revision_record_id,
					# 									TreeParam=TreeParam
					# 									))
					# 	c = Sql.GetFirst("SELECT SUM(DISCOUNT_AMOUNT_INGL_CURR) AS DISCOUNT_AMOUNT_INGL_CURR,SUM(NET_PRICE) AS SUM_PRICE, SUM(YEAR_1) AS YEAR1, SUM(YEAR_2) AS YEAR2, SUM(YEAR_3) AS YEAR3, SUM(YEAR_4) AS YEAR4, SUM(YEAR_5) AS YEAR5, SUM(NET_PRICE_INGL_CURR) AS SUM_PRICE_INGL_CURR, SUM(YEAR_1_INGL_CURR) AS YEAR1_INGL_CURR, SUM(YEAR_2_INGL_CURR) AS YEAR2_INGL_CURR, SUM(YEAR_3_INGL_CURR) AS YEAR3_INGL_CURR, SUM(YEAR_4_INGL_CURR) AS YEAR4_INGL_CURR, SUM(YEAR_5_INGL_CURR) AS YEAR5_INGL_CURR FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}' AND FABLOCATION_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(contract_quote_record_id,TreeParentParam.split("-")[1].strip(),TreeParam,quote_revision_record_id))

					# 	FabNetValue = c.YEAR1 + c.YEAR2 + c.YEAR3 + c.YEAR4 + c.YEAR5

					# 	Sql.RunQuery("UPDATE SAQIFL SET DISCOUNT_AMOUNT_INGL_CURR = {DiscountAmt},NET_VALUE = {netvalue},DISCOUNT = {discount},NET_PRICE = '{net_price}',YEAR_1 = {y1},YEAR_2 = {y2},YEAR_3={y3},YEAR_4={y4},YEAR_5 = {y5},NET_PRICE_INGL_CURR = '{net_price_in_gl}',YEAR_1_INGL_CURR = {y1_gl},YEAR_2_INGL_CURR = {y2_gl},YEAR_3_INGL_CURR={y3_gl},YEAR_4_INGL_CURR={y4_gl},YEAR_5_INGL_CURR = {y5_gl}  WHERE QUOTE_RECORD_ID = '{quote_record_id}' AND SERVICE_ID LIKE '%{service_id}%' AND FABLOCATION_ID = '{fab_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}'".format(discount = float(VALUE),net_price = float(c.SUM_PRICE),net_price_in_gl = float(c.SUM_PRICE_INGL_CURR),quote_record_id = contract_quote_record_id,service_id = TreeParentParam.split("-")[1].strip(),fab_id = TreeParam,y1=c.YEAR1,y2=c.YEAR2,y3=c.YEAR3,y4=c.YEAR4,y5=c.YEAR5,y1_gl=c.YEAR1_INGL_CURR,y2_gl=c.YEAR2_INGL_CURR,y3_gl=c.YEAR3_INGL_CURR,y4_gl=c.YEAR4_INGL_CURR,y5_gl=c.YEAR5_INGL_CURR,quote_revision_record_id=quote_revision_record_id,netvalue=FabNetValue,DiscountAmt=c.DISCOUNT_AMOUNT_INGL_CURR))
					# 	# Sql.RunQuery("""UPDATE SAQITM
					# 	# 					SET 
					# 	# 					NET_VALUE = IQ.NET_VALUE,
					# 	# 					NET_PRICE = IQ.NET_PRICE,
					# 	# 					YEAR_1 = IQ.YEAR_1,
					# 	# 					YEAR_2 = IQ.YEAR_2,
					# 	# 					YEAR_3 = IQ.YEAR_3,
					# 	# 					YEAR_4 = IQ.YEAR_4,
					# 	# 					YEAR_5 = IQ.YEAR_5,
					# 	# 					NET_VALUE_INGL_CURR = IQ.NET_VALUE_INGL_CURR,
					# 	# 					NET_PRICE_INGL_CURR = IQ.NET_PRICE_INGL_CURR,
					# 	# 					YEAR_1_INGL_CURR = IQ.YEAR_1_INGL_CURR,
					# 	# 					YEAR_2_INGL_CURR = IQ.YEAR_2_INGL_CURR,
					# 	# 					YEAR_3_INGL_CURR = IQ.YEAR_3_INGL_CURR,
					# 	# 					YEAR_4_INGL_CURR = IQ.YEAR_4_INGL_CURR,
					# 	# 					YEAR_5_INGL_CURR = IQ.YEAR_5_INGL_CURR,
					# 	# 					DISCOUNT = '{Discount}'					
					# 	# 					FROM SAQITM (NOLOCK)
					# 	# 					INNER JOIN (SELECT SAQITM.CpqTableEntryId,
					# 	# 								CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.NET_VALUE, 0)), 0), 0) as decimal(18,2)) as NET_VALUE,
					# 	# 								CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.NET_PRICE, 0)), 0), 0) as decimal(18,2)) as NET_PRICE,
					# 	# 								CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_1, 0)), 0), 0) as decimal(18,2)) as YEAR_1,
					# 	# 								CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_2, 0)), 0), 0) as decimal(18,2)) as YEAR_2,
					# 	# 								CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_3, 0)), 0), 0) as decimal(18,2)) as YEAR_3,
					# 	# 								CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_4, 0)), 0), 0) as decimal(18,2)) as YEAR_4,
					# 	# 								CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_5, 0)), 0), 0) as decimal(18,2)) as YEAR_5,
					# 	# 								CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.NET_VALUE_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as NET_VALUE_INGL_CURR,
					# 	# 								CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.NET_PRICE_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as NET_PRICE_INGL_CURR,
					# 	# 								CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_1_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as YEAR_1_INGL_CURR,
					# 	# 								CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_2_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as YEAR_2_INGL_CURR,
					# 	# 								CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_3_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as YEAR_3_INGL_CURR,
					# 	# 								CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_4_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as YEAR_4_INGL_CURR,
					# 	# 								CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_5_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as YEAR_5_INGL_CURR
					# 	# 								FROM SAQITM (NOLOCK) 
					# 	# 								JOIN SAQICO (NOLOCK) ON SAQICO.QUOTE_RECORD_ID = SAQITM.QUOTE_RECORD_ID AND SAQICO.LINE_ITEM_ID = SAQITM.LINE_ITEM_ID
					# 	# 								WHERE SAQITM.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQITM.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQICO.FABLOCATION_ID = '{TreeParam}'
					# 	# 								GROUP BY SAQITM.LINE_ITEM_ID, SAQITM.QUOTE_RECORD_ID, SAQITM.CpqTableEntryId,SAQITM.QTEREV_RECORD_ID)IQ
					# 	# 					ON SAQITM.CpqTableEntryId = IQ.CpqTableEntryId 
					# 	# 					WHERE SAQITM.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQITM.QTEREV_RECORD_ID = '{RevisionRecordId}' """.format(QuoteRecordId=contract_quote_record_id,RevisionRecordId=quote_revision_record_id,
					# 	# 					Discount=VALUE,plus="+",TreeParam=TreeParam))
					# 	quote_currency = str(Quote.GetCustomField('Currency').Content)		
					# 	total_net_price = 0.00		
					# 	total_year_1 = 0.00
					# 	total_year_2 = 0.00
					# 	total_year_3 = 0.00
					# 	total_year_4 = 0.00
					# 	total_year_5 = 0.00
					# 	total_net_value = 0.00
					# 	items_data = {}

					# 	# items_obj = Sql.GetList("SELECT SERVICE_ID, LINE_ITEM_ID, ISNULL(YEAR_1, 0) as YEAR_1 ,ISNULL(YEAR_2, 0) as YEAR_2 ,ISNULL(YEAR_3, 0) as YEAR_3 ,ISNULL(YEAR_4, 0) as YEAR_4 ,ISNULL(YEAR_5, 0) as YEAR_5 , ISNULL(NET_VALUE,0) AS NET_VALUE, ISNULL(NET_PRICE, 0) as NET_PRICE FROM SAQITM (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(contract_quote_record_id,quote_revision_record_id,TreeParam))
					# 	# if items_obj:
					# 	# 	for item_obj in items_obj:
					# 	# 		items_data[int(float(item_obj.LINE_ITEM_ID))] = {'NET_VALUE':item_obj.NET_VALUE, 'SERVICE_ID':(item_obj.SERVICE_ID.replace('- BASE', '')).strip(), 'YEAR_1':item_obj.YEAR_1, 'YEAR_2':item_obj.YEAR_2, 'NET_PRICE':item_obj.NET_PRICE}
					# 	for item in Quote.MainItems:
					# 		item_number = int(item.RolledUpQuoteItem)
					# 		if item_number in items_data.keys():
					# 			if items_data.get(item_number).get('SERVICE_ID') == item.PartNumber:
					# 				item_data = items_data.get(item_number)
					# 				item.NET_PRICE.Value = float(item_data.get('NET_PRICE'))
					# 				total_net_price += item.NET_PRICE.Value
					# 				item.NET_VALUE.Value = item_data.get('NET_VALUE')
					# 				total_net_value += item.NET_VALUE.Value	
					# 				item.YEAR_1.Value = item_data.get('YEAR_1')
					# 				total_year_1 += item.YEAR_1.Value
					# 				item.YEAR_2.Value = item_data.get('YEAR_2')
					# 				total_year_2 += item.YEAR_2.Value
					# 				item.YEAR_3.Value = item_data.get('YEAR_3')
					# 				total_year_3 += item.YEAR_3.Value
					# 				item.YEAR_4.Value = item_data.get('YEAR_4')
					# 				total_year_4 += item.YEAR_4.Value
					# 				item.YEAR_5.Value = item_data.get('YEAR_5')
					# 				total_year_5 += item.YEAR_5.Value
					# 				item.DISCOUNT.Value = "+"+str(VALUE)
					# 	##Added the percentage symbol for discount custom field...
					# 	Percentage = '%'
					# 	Quote.GetCustomField('DISCOUNT').Content = str(VALUE)+ " " + Percentage
					# 	#discount_value = Quote.GetCustomField('DISCOUNT').Content
					# 	#Trace.Write("discount"+str(discount_value))
					# 	# Quote.GetCustomField('TOTAL_NET_PRICE').Content =str(total_net_price) + " " + quote_currency
					# 	# Quote.GetCustomField('YEAR_1').Content = str(total_year_1) + " " + quote_currency
					# 	# Quote.GetCustomField('YEAR_2').Content = str(total_year_2) + " " + quote_currency
					# 	# Quote.GetCustomField('YEAR_3').Content = str(total_year_3) + " " + quote_currency
					# 	# Quote.GetCustomField('TOTAL_NET_VALUE').Content = str(total_net_value) + " " + quote_currency
					# 	Quote.Save()

					# 	Sql.RunQuery("""UPDATE SAQTRV
					# 						SET 									
					# 						SAQTRV.NET_PRICE_INGL_CURR = IQ.NET_PRICE_INGL_CURR,
					# 						SAQTRV.TOTAL_AMOUNT_INGL_CURR = IQ.NET_VALUE,
											
					# 						SAQTRV.DISCOUNT_PERCENT = '{discount}'
											
					# 						FROM SAQTRV (NOLOCK)
					# 						INNER JOIN (SELECT SAQRIT.QUOTE_RECORD_ID, SAQRIT.QTEREV_RECORD_ID,
					# 									SUM(ISNULL(SAQRIT.NET_PRICE_INGL_CURR, 0)) as NET_PRICE_INGL_CURR,
					# 									SUM(ISNULL(SAQRIT.TOTAL_AMOUNT_INGL_CURR, 0)) as NET_VALUE
														
					# 									FROM SAQRIT (NOLOCK) WHERE SAQRIT.QUOTE_RECORD_ID = '{quote_rec_id}' AND SAQRIT.QTEREV_RECORD_ID = '{quote_revision_rec_id}' GROUP BY SAQRIT.QTEREV_RECORD_ID, SAQRIT.QUOTE_RECORD_ID) IQ ON SAQTRV.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND SAQTRV.QUOTE_REVISION_RECORD_ID = IQ.QTEREV_RECORD_ID
					# 						WHERE SAQTRV.QUOTE_RECORD_ID = '{quote_rec_id}' AND SAQTRV.QUOTE_REVISION_RECORD_ID = '{quote_revision_rec_id}' """.format(discount = str(VALUE),quote_rec_id = contract_quote_record_id,quote_revision_rec_id = quote_revision_record_id))


					else:
						
						notification = 'Billing Start Date should be less than Billing End Date'
						dictc = {"CpqTableEntryId": str(sql_cpq.CpqTableEntryId)}
						newdict.update(dictc)
						tableInfo = Sql.GetTable(str(TableName))
						tablerow = newdict
						tableInfo.AddRow(tablerow)
						Trace.Write("TEZTZ--475---"+str(tablerow))
						# sectional edit error message - starts
						req_obj = Sql.GetList(
							"select API_NAME from  SYOBJD(NOLOCK) where OBJECT_NAME = '" + str(TableName) + "' and REQUIRED = 1 "
						)
						Trace.Write("select API_NAME from  SYOBJD(NOLOCK) where OBJECT_NAME = '" + str(TableName) + "' and REQUIRED = 1 ")

						if req_obj is not None and len(req_obj) > 0:
							
							required_val = [str(i.API_NAME) for i in req_obj]
							
							for data, datas in tablerow.items():
								Trace.Write("data_chk_j---"+str(data)+" datas_chk_j---"+str(datas))
								if data in required_val:
									for req in required_val:
										Trace.Write("req_chk_j---"+str(req)+" tablerow_chk_j---"+str(tablerow))
										if tablerow[req] == "":
											Trace.Write(
												"955---------------------------"
												+ str(datas)
												+ "--required_val--"
												+ str(required_val)
												+ "--data--"
												+ str(data)
											)
											Req_Flag = 1

											# Product.Attributes.GetByName("SEC_N_TAB_PAGE_ALERT").HintFormula = """<div class='col-md-12' id='PageAlert'  ><div class='row modulesecbnr brdr' data-toggle='collapse' data-target='#Alert13' aria-expanded='true' >NOTIFICATIONS<i class='pull-right fa fa-chevron-down '></i><i class='pull-right fa fa-chevron-up'></i></div><div  id='Alert13' class='col-md-12  alert-notification  brdr collapse in' ><div  class='col-md-12 alert-danger'><label ><img src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/stopicon1.svg" alt="Error">  ERROR : '{}' is a required field </label></div></div></div>""".format(data)
											field_label = Sql.GetFirst("select FIELD_LABEL from  SYOBJD(NOLOCK) where OBJECT_NAME = '" + str(TableName) + "' AND API_NAME = '"+str(data)+"' ")
											warning_msg = ' ERROR : "{}" is a required field'.format(field_label.FIELD_LABEL)
											# break
										else:
											Trace.Write("else_chk_j---")
											Req_Flag = 0
											warning_msg = ""
											
											Sql.Upsert(tableInfo)
								# if data in required_val and datas == "":
								#     Trace.Write(
								#         "955---------------------------"
								#         + str(datas)
								#         + "--required_val--"
								#         + str(required_val)
								#         + "--data--"
								#         + str(data)
								#     )
								#     Req_Flag = 1

								#     # Product.Attributes.GetByName("SEC_N_TAB_PAGE_ALERT").HintFormula = """<div class='col-md-12' id='PageAlert'  ><div class='row modulesecbnr brdr' data-toggle='collapse' data-target='#Alert13' aria-expanded='true' >NOTIFICATIONS<i class='pull-right fa fa-chevron-down '></i><i class='pull-right fa fa-chevron-up'></i></div><div  id='Alert13' class='col-md-12  alert-notification  brdr collapse in' ><div  class='col-md-12 alert-danger'><label ><img src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/stopicon1.svg" alt="Error">  ERROR : '{}' is a required field </label></div></div></div>""".format(data)
								#     field_label = Sql.GetFirst("select FIELD_LABEL from  SYOBJD(NOLOCK) where OBJECT_NAME = '" + str(TableName) + "' AND API_NAME = '"+str(data)+"' ")
								#     warning_msg = ' ERROR : "{}" is a required field'.format(field_label.FIELD_LABEL)
								#     # break
								# else:
								#     Req_Flag = 0
								#     warning_msg = ""
									
								#     Sql.Upsert(tableInfo)
						else:
							Trace.Write('533-----------'+str(TableName))
							Sql.Upsert(tableInfo)
						# sectional edit error message - ends

						
						if Product.GetGlobal("TreeParentLevel1") == "Product Offerings":
							contract_quote_record_id = Product.GetGlobal("contract_quote_record_id")
							quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")

							product_offering_contract_validity = Sql.GetFirst("SELECT CONTRACT_VALID_FROM, CONTRACT_VALID_TO,SERVICE_ID FROM SAQTSV (NOLOCK) WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND SERVICE_ID = '{service_id}'".format(Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(TreeParam)))

							validity_from_date = Sql.GetFirst("SELECT MIN(CONTRACT_VALID_FROM) AS CONTRACT_VALID_FROM FROM SAQTSV (NOLOCK) WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}'".format(Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id)))

							validity_to_date = Sql.GetFirst("SELECT MAX(CONTRACT_VALID_TO) AS CONTRACT_VALID_TO FROM SAQTSV (NOLOCK) WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}'".format(Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id)))

							fab_contract_update = "UPDATE SAQSFB SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND SERVICE_ID = '{service_id}'".format(valid_from= product_offering_contract_validity.CONTRACT_VALID_FROM, valid_to =   product_offering_contract_validity.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID))

							greenbook_contract_update = "UPDATE SAQSGB SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND SERVICE_ID = '{service_id}'".format(valid_from= product_offering_contract_validity.CONTRACT_VALID_FROM, valid_to =   product_offering_contract_validity.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID))


							equipment_contract_update = "UPDATE SAQSCO SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND SERVICE_ID = '{service_id}'".format(valid_from= product_offering_contract_validity.CONTRACT_VALID_FROM, valid_to =   product_offering_contract_validity.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID))

							assembly_contract_update = "UPDATE SAQSCA SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND SERVICE_ID = '{service_id}'".format(valid_from= product_offering_contract_validity.CONTRACT_VALID_FROM, valid_to =   product_offering_contract_validity.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID))

							item_contract_update = "UPDATE SAQRIT SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND SERVICE_ID = '{service_id}'".format(valid_from= product_offering_contract_validity.CONTRACT_VALID_FROM, valid_to =   product_offering_contract_validity.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID))

							# saqitm_contract_update = "UPDATE SAQITM SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND SERVICE_ID LIKE '%{service_id}%'".format(valid_from= product_offering_contract_validity.CONTRACT_VALID_FROM, valid_to =   product_offering_contract_validity.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID))

							# saqifl_contract_update = "UPDATE SAQIFL SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND SERVICE_ID = '{service_id}'".format(valid_from= product_offering_contract_validity.CONTRACT_VALID_FROM, valid_to =   product_offering_contract_validity.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID))

							# saqigb_contract_update = "UPDATE SAQIGB SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND SERVICE_ID = '{service_id}'".format(valid_from= product_offering_contract_validity.CONTRACT_VALID_FROM, valid_to =   product_offering_contract_validity.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID))

							saqico_contract_update = "UPDATE SAQICO SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND SERVICE_ID = '{service_id}'".format(valid_from= product_offering_contract_validity.CONTRACT_VALID_FROM, valid_to =   product_offering_contract_validity.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID))
							Trace.Write("QUOTE_REC_CHK_J"+str(contract_quote_record_id))
							saqtrv_contract_update = "UPDATE SAQTRV SET CONTRACT_VALID_FROM = '{validity_from_date}' , CONTRACT_VALID_TO = '{validity_to_date}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}'".format(validity_from_date= validity_from_date.CONTRACT_VALID_FROM, validity_to_date =   validity_to_date.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id))


							Sql.RunQuery(fab_contract_update)
							Sql.RunQuery(greenbook_contract_update)
							Sql.RunQuery(equipment_contract_update)
							Sql.RunQuery(assembly_contract_update)
							# Sql.RunQuery(saqitm_contract_update)
							# Sql.RunQuery(saqifl_contract_update)
							# Sql.RunQuery(saqigb_contract_update)
							Sql.RunQuery(saqico_contract_update)
							Sql.RunQuery(saqtrv_contract_update)
							Sql.RunQuery(item_contract_update)

						elif Product.GetGlobal("TreeParentLevel2") == "Product Offerings":
							contract_quote_record_id = Product.GetGlobal("contract_quote_record_id")
							quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")

							product_offering_contract_validity = Sql.GetFirst("SELECT CONTRACT_VALID_FROM, CONTRACT_VALID_TO,SERVICE_ID FROM SAQSFB (NOLOCK) WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND SERVICE_ID = '{service_id}'".format(Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= Product.GetGlobal("TreeParentLevel0")))

							validity_from_date = Sql.GetFirst("SELECT MIN(CONTRACT_VALID_FROM) AS CONTRACT_VALID_FROM FROM SAQSFB (NOLOCK) WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}'".format(Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id)))

							validity_to_date = Sql.GetFirst("SELECT MAX(CONTRACT_VALID_TO) AS CONTRACT_VALID_TO FROM SAQSFB (NOLOCK) WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}'".format(Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id)))


							service_contract_update = "UPDATE SAQTSV SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND SERVICE_ID = '{service_id}'".format(valid_from= product_offering_contract_validity.CONTRACT_VALID_FROM, valid_to =   product_offering_contract_validity.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID))

							greenbook_contract_update = "UPDATE SAQSGB SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND SERVICE_ID = '{service_id}'".format(valid_from= product_offering_contract_validity.CONTRACT_VALID_FROM, valid_to =   product_offering_contract_validity.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID))

							item_contract_update = "UPDATE SAQRIT SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND SERVICE_ID = '{service_id}'".format(valid_from= product_offering_contract_validity.CONTRACT_VALID_FROM, valid_to =   product_offering_contract_validity.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID))

							equipment_contract_update = "UPDATE SAQSCO SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND SERVICE_ID = '{service_id}'".format(valid_from= product_offering_contract_validity.CONTRACT_VALID_FROM, valid_to =   product_offering_contract_validity.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID))

							assembly_contract_update = "UPDATE SAQSCA SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND SERVICE_ID = '{service_id}'".format(valid_from= product_offering_contract_validity.CONTRACT_VALID_FROM, valid_to =   product_offering_contract_validity.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID))

							# saqitm_contract_update = "UPDATE SAQITM SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND SERVICE_ID LIKE '%{service_id}%".format(valid_from= product_offering_contract_validity.CONTRACT_VALID_FROM, valid_to =   product_offering_contract_validity.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID))

							# saqifl_contract_update = "UPDATE SAQIFL SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND SERVICE_ID = '{service_id}'".format(valid_from= product_offering_contract_validity.CONTRACT_VALID_FROM, valid_to =   product_offering_contract_validity.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID))

							# saqigb_contract_update = "UPDATE SAQIGB SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND SERVICE_ID = '{service_id}'".format(valid_from= product_offering_contract_validity.CONTRACT_VALID_FROM, valid_to =   product_offering_contract_validity.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID))

							saqico_contract_update = "UPDATE SAQICO SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND SERVICE_ID = '{service_id}'".format(valid_from= product_offering_contract_validity.CONTRACT_VALID_FROM, valid_to =   product_offering_contract_validity.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID))

							saqtrv_contract_update = "UPDATE SAQTRV SET CONTRACT_VALID_FROM = '{validity_from_date}' , CONTRACT_VALID_TO = '{validity_to_date}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}'".format(validity_from_date= validity_from_date.CONTRACT_VALID_FROM, validity_to_date =   validity_to_date.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id))

							Sql.RunQuery(service_contract_update)
							Sql.RunQuery(greenbook_contract_update)
							Sql.RunQuery(equipment_contract_update)
							Sql.RunQuery(assembly_contract_update)
							# Sql.RunQuery(saqitm_contract_update)
							# Sql.RunQuery(saqifl_contract_update)
							# Sql.RunQuery(saqigb_contract_update)
							Sql.RunQuery(saqico_contract_update)
							Sql.RunQuery(saqtrv_contract_update)
							Sql.RunQuery(item_contract_update)

						elif Product.GetGlobal("TreeParentLevel3") == "Product Offerings" and subtab_name == "Details":
							contract_quote_record_id = Product.GetGlobal("contract_quote_record_id")
							quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")

							product_offering_contract_validity = Sql.GetFirst("SELECT CONTRACT_VALID_FROM, CONTRACT_VALID_TO,SERVICE_ID FROM SAQSGB (NOLOCK) WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND SERVICE_ID = '{service_id}' AND GREENBOOK = '{Treeparam}'".format(Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= Product.GetGlobal("TreeParentLevel1"),Treeparam= Product.GetGlobal("Treeparam")))

							validity_from_date = Sql.GetFirst("SELECT MIN(CONTRACT_VALID_FROM) AS CONTRACT_VALID_FROM FROM SAQSGB (NOLOCK) WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}'".format(Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id)))

							validity_to_date = Sql.GetFirst("SELECT MAX(CONTRACT_VALID_TO) AS CONTRACT_VALID_TO FROM SAQSGB (NOLOCK) WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}'".format(Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id)))


							service_contract_update = "UPDATE SAQTSV SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND SERVICE_ID = '{service_id}'".format(valid_from= product_offering_contract_validity.CONTRACT_VALID_FROM, valid_to =   product_offering_contract_validity.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID))

							fab_contract_update = "UPDATE SAQSFB SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND SERVICE_ID = '{service_id}'".format(valid_from= product_offering_contract_validity.CONTRACT_VALID_FROM, valid_to =   product_offering_contract_validity.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID))


							equipment_contract_update = "UPDATE SAQSCO SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND SERVICE_ID = '{service_id}'".format(valid_from= product_offering_contract_validity.CONTRACT_VALID_FROM, valid_to =   product_offering_contract_validity.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID))

							assembly_contract_update = "UPDATE SAQSCA SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND SERVICE_ID = '{service_id}'".format(valid_from= product_offering_contract_validity.CONTRACT_VALID_FROM, valid_to =   product_offering_contract_validity.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID))

							# saqitm_contract_update = "UPDATE SAQITM SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND SERVICE_ID LIKE '%{service_id}%".format(valid_from= product_offering_contract_validity.CONTRACT_VALID_FROM, valid_to =   product_offering_contract_validity.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID))

							# saqifl_contract_update = "UPDATE SAQIFL SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND SERVICE_ID = '{service_id}'".format(valid_from= product_offering_contract_validity.CONTRACT_VALID_FROM, valid_to =   product_offering_contract_validity.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID))

							# saqigb_contract_update = "UPDATE SAQIGB SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND SERVICE_ID = '{service_id}' AND GREENBOOK = '{Treeparam}'".format(valid_from= product_offering_contract_validity.CONTRACT_VALID_FROM, valid_to =   product_offering_contract_validity.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID),Treeparam=Product.GetGlobal("Treeparam"))

							saqico_contract_update = "UPDATE SAQICO SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND SERVICE_ID = '{service_id}'".format(valid_from= product_offering_contract_validity.CONTRACT_VALID_FROM, valid_to =   product_offering_contract_validity.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID))

							saqtrv_contract_update = "UPDATE SAQTRV SET CONTRACT_VALID_FROM = '{validity_from_date}' , CONTRACT_VALID_TO = '{validity_to_date}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}'".format(validity_from_date= validity_from_date.CONTRACT_VALID_FROM, validity_to_date =   validity_to_date.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id))

							item_contract_update = "UPDATE SAQRIT SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND SERVICE_ID = '{service_id}'".format(valid_from= product_offering_contract_validity.CONTRACT_VALID_FROM, valid_to =   product_offering_contract_validity.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID))

							Sql.RunQuery(service_contract_update)
							Sql.RunQuery(fab_contract_update)
							Sql.RunQuery(equipment_contract_update)
							Sql.RunQuery(assembly_contract_update)
							# Sql.RunQuery(saqitm_contract_update)
							# Sql.RunQuery(saqifl_contract_update)
							# Sql.RunQuery(saqigb_contract_update)
							Sql.RunQuery(saqico_contract_update)
							Sql.RunQuery(saqtrv_contract_update)
							Sql.RunQuery(item_contract_update)


						elif Product.GetGlobal("TreeParentLevel3") == "Product Offerings" and subtab_name == "Equipment Details":
							contract_quote_record_id = Product.GetGlobal("contract_quote_record_id")
							quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")

							product_offering_contract_validity = Sql.GetFirst("SELECT CONTRACT_VALID_FROM, CONTRACT_VALID_TO,SERVICE_ID FROM SAQSCO (NOLOCK) WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND CpqTableEntryId = '{Equipment}'".format(Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),Equipment=tablerow['CpqTableEntryId']))

							validity_from_date = Sql.GetFirst("SELECT MIN(CONTRACT_VALID_FROM) AS CONTRACT_VALID_FROM FROM SAQSCO (NOLOCK) WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}'".format(Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id)))

							validity_to_date = Sql.GetFirst("SELECT MAX(CONTRACT_VALID_TO) AS CONTRACT_VALID_TO FROM SAQSCO (NOLOCK) WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}'".format(Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id)))


							service_contract_update = "UPDATE SAQTSV SET CONTRACT_VALID_FROM = '{validity_from_date}' , CONTRACT_VALID_TO = '{validity_to_date}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND SERVICE_ID = '{service_id}'".format(validity_from_date= validity_from_date.CONTRACT_VALID_FROM, validity_to_date =   validity_to_date.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(Product.GetGlobal("TreeParentLevel1")))

							fab_contract_update = "UPDATE SAQSFB SET CONTRACT_VALID_FROM = '{validity_from_date}' , CONTRACT_VALID_TO = '{validity_to_date}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND SERVICE_ID = '{service_id}'".format(validity_from_date= validity_from_date.CONTRACT_VALID_FROM, validity_to_date =   validity_to_date.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(Product.GetGlobal("TreeParentLevel1")))

							greenbook_contract_update = "UPDATE SAQSGB SET CONTRACT_VALID_FROM = '{validity_from_date}' , CONTRACT_VALID_TO = '{validity_to_date}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND SERVICE_ID = '{service_id}'".format(validity_from_date= validity_from_date.CONTRACT_VALID_FROM, validity_to_date =   validity_to_date.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(Product.GetGlobal("TreeParentLevel1")))

							# equipment_contract_update = "UPDATE SAQSCO SET CONTRACT_VALID_FROM = '{validity_from_date}' , CONTRACT_VALID_TO = '{validity_to_date}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND SERVICE_ID = '{service_id}'".format(validity_from_date= validity_from_date.CONTRACT_VALID_FROM, validity_to_date =   validity_to_date.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(Product.GetGlobal("TreeParentLevel1")))

							assembly_contract_update = "UPDATE SAQSCA SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND SERVICE_ID = '{service_id}'".format(valid_from= product_offering_contract_validity.CONTRACT_VALID_FROM, valid_to =   product_offering_contract_validity.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID))

							# saqitm_contract_update = "UPDATE SAQITM SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND SERVICE_ID LIKE '%{service_id}%".format(valid_from= product_offering_contract_validity.CONTRACT_VALID_FROM, valid_to =   product_offering_contract_validity.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID))

							# saqifl_contract_update = "UPDATE SAQIFL SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND SERVICE_ID = '{service_id}'".format(valid_from= product_offering_contract_validity.CONTRACT_VALID_FROM, valid_to =   product_offering_contract_validity.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID))

							# saqigb_contract_update = "UPDATE SAQIGB SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND SERVICE_ID = '{service_id}'".format(valid_from= product_offering_contract_validity.CONTRACT_VALID_FROM, valid_to =   product_offering_contract_validity.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID))

							saqico_contract_update = "UPDATE SAQICO SET CONTRACT_VALID_FROM = '{validity_from_date}' , CONTRACT_VALID_TO = '{validity_to_date}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND SERVICE_ID = '{service_id}'".format(validity_from_date= validity_from_date.CONTRACT_VALID_FROM, validity_to_date =   validity_to_date.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(Product.GetGlobal("TreeParentLevel1")))

							saqtrv_contract_update = "UPDATE SAQTRV SET CONTRACT_VALID_FROM = '{validity_from_date}' , CONTRACT_VALID_TO = '{validity_to_date}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}'".format(validity_from_date= validity_from_date.CONTRACT_VALID_FROM, validity_to_date =   validity_to_date.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id))

							item_contract_update = "UPDATE SAQRIT SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND SERVICE_ID = '{service_id}'".format(valid_from= product_offering_contract_validity.CONTRACT_VALID_FROM, valid_to =   product_offering_contract_validity.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID))

							Sql.RunQuery(service_contract_update)
							Sql.RunQuery(fab_contract_update)
							Sql.RunQuery(item_contract_update)
							Sql.RunQuery(assembly_contract_update)
							# Sql.RunQuery(saqitm_contract_update)
							# Sql.RunQuery(saqifl_contract_update)
							# Sql.RunQuery(saqigb_contract_update)
							Sql.RunQuery(saqico_contract_update)
							Sql.RunQuery(saqtrv_contract_update)
							Sql.RunQuery(greenbook_contract_update)
							

							




				if TableName == 'SAQRIB' and old_billing_matrix_obj:                    
					billing_matrix_obj = Sql.GetFirst("""SELECT BILLING_START_DATE, 
									BILLING_END_DATE, QUOTE_BILLING_PLAN_RECORD_ID, BILLING_DAY
									FROM SAQRIB (NOLOCK)
									WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' """.format(Product.GetGlobal("contract_quote_record_id"), quote_revision_record_id ))
					if billing_matrix_obj:
						if billing_matrix_obj.BILLING_START_DATE != old_billing_matrix_obj.BILLING_START_DATE or billing_matrix_obj.BILLING_END_DATE != old_billing_matrix_obj.BILLING_END_DATE or billing_matrix_obj.BILLING_DAY != old_billing_matrix_obj.BILLING_DAY:                        						
							billing_query = "UPDATE SAQRIB SET IS_CHANGED = 1 WHERE QUOTE_BILLING_PLAN_RECORD_ID ='{}'".format(billing_matrix_obj.QUOTE_BILLING_PLAN_RECORD_ID)
							Sql.RunQuery(billing_query)
					#generate_year_based_billing_matrix(newdict)
				if TableName == 'SAQTIP':
					Trace.Write('SAQTIP_CHK_J '+str(RECORD['PARTY_ROLE']))

					saqtip_ship_to_update_query = "UPDATE SAQTIP SET PARTY_ID = {party_id}, [PRIMARY] = '{primary}' WHERE QUOTE_INVOLVED_PARTY_RECORD_ID = '{ship_to_id}'".format(party_id=RECORD['PARTY_ID'],primary=RECORD['PRIMARY'],ship_to_id=RECORD['QUOTE_INVOLVED_PARTY_RECORD_ID'])

					saqtip_ship_to_false = "UPDATE SAQTIP SET [PRIMARY] = 'false' WHERE QUOTE_INVOLVED_PARTY_RECORD_ID != '{ship_to_id}' AND PARTY_ID = 'SHIP TO'".format(ship_to_id=RECORD['QUOTE_INVOLVED_PARTY_RECORD_ID'])

					Sql.RunQuery(saqtip_ship_to_update_query)
					Sql.RunQuery(saqtip_ship_to_false)
					account_details = Sql.GetFirst("SELECT * FROM SAACNT (NOLOCK) WHERE ACCOUNT_ID = '"+str(RECORD['PARTY_ID'])+"'")
					send_n_receive_acunt = "UPDATE SAQSRA SET ACCOUNT_ID = '{}', ACCOUNT_NAME = '{}', ACCOUNT_RECORD_ID = '{}', ADDRESS_1 = '{}', CITY = '{}', COUNTRY = '{}', COUNTRY_RECORD_ID = '{}', PHONE = '{}', STATE = '{}', STATE_RECORD_ID = '{}', POSTAL_CODE = '{}' WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND RELOCATION_TYPE = '{}'".format(str(account_details.ACCOUNT_ID), str(account_details.ACCOUNT_NAME), str(account_details.ACCOUNT_RECORD_ID), str(account_details.ADDRESS_1), str(account_details.CITY), str(account_details.COUNTRY), str(account_details.COUNTRY_RECORD_ID), str(account_details.PHONE), str(account_details.STATE), str(account_details.STATE_RECORD_ID), str(account_details.POSTAL_CODE), Product.GetGlobal("contract_quote_record_id"), quote_revision_record_id, str(RECORD['PARTY_ROLE']))
					Sql.RunQuery(send_n_receive_acunt)
				# A055S000P01-3324 start 
				if TableName == 'SAQTMT':
					#A055S000P01-4393 start 
					WARRANTY_val =''
					#getdate = Sql.GetFirst("""SELECT CONTRACT_VALID_FROM, CONTRACT_VALID_TO FROM SAQTMT WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' """.format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id))
					#get_warrent_dates= SqlHelper.GetList("select QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,WARRANTY_END_DATE_ALERT,WARRANTY_START_DATE,WARRANTY_END_DATE from SAQSCO where QUOTE_RECORD_ID = '"+str(Quote.GetGlobal("contract_quote_record_id"))+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' ")
					warrant_enddat_alert_update = SqlHelper.GetFirst("sp_executesql @T=N'update B SET B.WARRANTY_END_DATE_ALERT = (CASE WHEN B.WARRANTY_END_DATE >= A.CONTRACT_VALID_FROM AND B.WARRANTY_END_DATE <=A.CONTRACT_VALID_TO THEN 1 ELSE 0 END) FROM SAQTMT A JOIN SAQSCO B ON A.MASTER_TABLE_QUOTE_RECORD_ID=B.QUOTE_RECORD_ID AND A.QTEREV_RECORD_ID=B.QTEREV_RECORD_ID WHERE A.MASTER_TABLE_QUOTE_RECORD_ID = ''"+str(Quote.GetGlobal("contract_quote_record_id"))+"'' AND A.QTEREV_RECORD_ID = ''"+str(quote_revision_record_id)+"'' AND B.WARRANTY_END_DATE >= A.CONTRACT_VALID_FROM and B.WARRANTY_END_DATE <=A.CONTRACT_VALID_TO '")
					# update_warranty_enddate_alert = ''
					# for val in get_warrent_dates:
						
					# 	if val.WARRANTY_END_DATE:
					# 		WARRANTY_val = datetime.strptime(str(val.WARRANTY_END_DATE), "%Y-%m-%d")
					# 		get_con_date = str(getdate.CONTRACT_VALID_FROM).split(" ")[0]
					# 		get_con_date = datetime.strptime(str(get_con_date), "%m/%d/%Y")
					# 		if WARRANTY_val > get_con_date:
					# 			update_warranty_enddate_alert = "UPDATE SAQSCO SET WARRANTY_END_DATE_ALERT = 1 where QUOTE_RECORD_ID = '"+str(Quote.GetGlobal("contract_quote_record_id"))+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"'  and QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID = '"+str(val.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID)+"'"
					# 		else:
					# 			update_warranty_enddate_alert = "UPDATE SAQSCO SET WARRANTY_END_DATE_ALERT = 0 where QUOTE_RECORD_ID = '"+str(Quote.GetGlobal("contract_quote_record_id"))+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"'  and QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID = '"+str(val.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID)+"'"
					# 			Trace.Write('no end date--')
					# 		Sql.RunQuery(update_warranty_enddate_alert)
					# 	else:
					# 		Trace.Write('WARRANTY_val--600-'+str(val.WARRANTY_END_DATE))
					# 		update_warranty_enddate_alert = "UPDATE SAQSCO SET WARRANTY_END_DATE_ALERT = 0 where QUOTE_RECORD_ID = '"+str(Quote.GetGlobal("contract_quote_record_id"))+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"'  and QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID = '"+str(val.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID)+"'"
					# 		Trace.Write('no end date--')
					# 		Sql.RunQuery(update_warranty_enddate_alert)
					#A055S000P01-4393 end
					getdate = Sql.GetFirst("""SELECT CONTRACT_VALID_FROM, CONTRACT_VALID_TO FROM SAQTRV WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'""".format(Quote.GetGlobal("contract_quote_record_id"), quote_revision_record_id))
					if getdate:
						Log.Info("SYSECTSAVE - SAQSGB")
						billing_query = "UPDATE SAQRIB SET IS_CHANGED = 1, BILLING_START_DATE = '{}', BILLING_END_DATE = '{}'  WHERE QUOTE_RECORD_ID ='{}' AND QTEREV_RECORD_ID = '{}'".format(getdate.CONTRACT_VALID_FROM, getdate.CONTRACT_VALID_TO, Product.GetGlobal('contract_quote_record_id'),quote_revision_record_id)
						Sql.RunQuery(billing_query)

						quoteinfo_query = "UPDATE SAQTMT SET CONTRACT_VALID_FROM = '{}', CONTRACT_VALID_TO = '{}'  WHERE MASTER_TABLE_QUOTE_RECORD_ID ='{}' AND QTEREV_RECORD_ID = '{}'".format(getdate.CONTRACT_VALID_FROM, getdate.CONTRACT_VALID_TO, Product.GetGlobal('contract_quote_record_id'),quote_revision_record_id)
						Sql.RunQuery(quoteinfo_query)
						
						update_contract_date = "UPDATE SAQTSV SET CONTRACT_VALID_FROM = '{}', CONTRACT_VALID_TO = '{}'  WHERE QUOTE_RECORD_ID ='{}' AND QTEREV_RECORD_ID = '{}'".format(getdate.CONTRACT_VALID_FROM, getdate.CONTRACT_VALID_TO, Product.GetGlobal('contract_quote_record_id'),quote_revision_record_id)
						Sql.RunQuery(update_contract_date)

						update_contract_date_fab_level = "UPDATE SAQSFB SET CONTRACT_VALID_FROM = '{}', CONTRACT_VALID_TO = '{}'  WHERE QUOTE_RECORD_ID ='{}' AND QTEREV_RECORD_ID = '{}'".format(getdate.CONTRACT_VALID_FROM, getdate.CONTRACT_VALID_TO, Product.GetGlobal('contract_quote_record_id'),quote_revision_record_id)
						Sql.RunQuery(update_contract_date_fab_level)

						update_contract_date_greenbook_level = "UPDATE SAQSGB SET CONTRACT_VALID_FROM = '{}', CONTRACT_VALID_TO = '{}'  WHERE QUOTE_RECORD_ID ='{}' AND QTEREV_RECORD_ID = '{}'".format(getdate.CONTRACT_VALID_FROM, getdate.CONTRACT_VALID_TO, Product.GetGlobal('contract_quote_record_id'),quote_revision_record_id)
						Sql.RunQuery(update_contract_date_greenbook_level)

						update_contract_date_cov_obj_level = "UPDATE SAQSCO SET CONTRACT_VALID_FROM = '{}', CONTRACT_VALID_TO = '{}'  WHERE QUOTE_RECORD_ID ='{}' AND QTEREV_RECORD_ID = '{}'".format(getdate.CONTRACT_VALID_FROM, getdate.CONTRACT_VALID_TO, Product.GetGlobal('contract_quote_record_id'),quote_revision_record_id)
						Sql.RunQuery(update_contract_date_cov_obj_level)
					import ACVIORULES
					violationruleInsert = ACVIORULES.ViolationConditions()
					header_obj = Sql.GetFirst("SELECT RECORD_ID FROM SYOBJH (NOLOCK) WHERE OBJECT_NAME = 'SAQTMT'")
					if header_obj:
						violationruleInsert.InsertAction(header_obj.RECORD_ID, Product.GetGlobal("contract_quote_record_id"), "SAQTMT")
					# import ACVIORULES
					# violationruleInsert = ACVIORULES.ViolationConditions()
					# header_obj = Sql.GetFirst("SELECT RECORD_ID FROM SYOBJH (NOLOCK) WHERE OBJECT_NAME = 'SAQTMT'")
					# if header_obj:
					#     Trace.Write(Quote.GetGlobal("contract_quote_record_id"))
					#     violationruleInsert.InsertAction(header_obj.RECORD_ID, Quote.GetGlobal("contract_quote_record_id"), "SAQTMT")
				# A055S000P01-3324 end
			else:
				Trace.Write("1237------5444------------" + str(newdict))
				newdict.update(RECORD)
				Trace.Write("1237------5444------------" + str(newdict))
				activeval = newdict.get("Active")
				idval = newdict.get("ID")
				UPDATE_USERS = "UPDATE USERS SET Active = '{}' WHERE ID = '{}'".format(activeval,idval)
				Sql.RunQuery(UPDATE_USERS)
				#tableInfo = SqlHelper.GetTable("USERS")
				#tableInfo.AddRow(newdict)
				#SqlHelper.Upsert(tableInfo)
		else:            
			new_val = str(Guid.NewGuid()).upper()
			RECID = {str(AutoNumb): new_val}
			RECORD.update(RECID)
			sql_sgs = Sql.GetList("SELECT API_NAME FROM SYOBJD WHERE OBJECT_NAME='" + str(TableName) + "'")
			for attr in sql_sgs:
				for KEY in RECORD:

					if str(attr.API_NAME) == KEY:
						newdict[attr.API_NAME] = RECORD[KEY]
					else:
						if str(attr.API_NAME) == "PRICEMODEL_ID":
							KEY = "PRICEMODEL_ID"
							newdict[attr.API_NAME] = RECORD[KEY] if str(TableName) != "PRPBMA" else RECORD[KEY + "_VALUE"]
					tableInfo = Sql.GetTable(str(TableName))
					tablerow = newdict
					tableInfo.AddRow(tablerow)
					Trace.Write("else1469")
					Sql.Upsert(tableInfo)
		##calling QTPOSTACRM script for CRM Contract idoc
		try:
			if TableName == 'SAQTMT' and 'QUOTE_STATUS' in RECORD.keys() and section_text == " EDITBASIC INFORMATION":
				Trace.Write('QUOTE_STATUS -- inside')
				if RECORD.get("QUOTE_STATUS") ==  'APPROVED':
					quote_id = Sql.GetFirst(
						"""SELECT QUOTE_ID,QTEREV_ID FROM SAQTMT (NOLOCK) WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID='{revision_rec_id}' """.format(
						QuoteRecordId= Quote.GetGlobal("contract_quote_record_id"),
						revision_rec_id = quote_revision_record_id
						)
					)
					
					Trace.Write('inside---'+str({'QUOTE_ID':str(quote_id.QUOTE_ID),'Fun_type':'cpq_to_crm'}))
					crm_result = ScriptExecutor.ExecuteGlobal('QTPOSTACRM',{'QUOTE_ID':str(quote_id.QUOTE_ID),'REVISION_ID':str(quote_id.QTEREV_ID),'Fun_type':'cpq_to_crm'})
					Trace.Write("ends--"+str(crm_result))
		except Exception:
			Trace.Write("except---")
		##ends

		##entitlement contract date update for z0016
		try:
			if Quote is not None:
				quote_record_id = Quote.GetGlobal("contract_quote_record_id")
			else:
				quote_record_id = ''
		except:
			quote_record_id = ''
		

		try:
			get_service_id = Sql.GetList("Select * from SAQTSV (nolock) where QUOTE_RECORD_ID ='"+str(quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' AND SERVICE_ID LIKE '%Z0016%' ")
			if get_service_id:
				for service in get_service_id:
					if TableName == 'SAQTMT' and 'CONTRACT_VALID_TO' in RECORD.keys() and 'CONTRACT_VALID_FROM' in RECORD.keys() and section_text == " EDITQUOTE TIMELINE INFORMATION" :
						Trace.Write('CONTRACT_VALID_TO -- inside')
						try:
							
							get_value = Sql.GetFirst("Select * from SAQTMT (nolock) where MASTER_TABLE_QUOTE_RECORD_ID ='"+str(quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' ")
							Trace.Write('get_value.CONTRACT_VALID_TO--'+str(get_value.CONTRACT_VALID_TO))
							QuoteEndDate = datetime.datetime(get_value.CONTRACT_VALID_TO)
							QuoteStartDate = datetime.datetime(get_value.CONTRACT_VALID_FROM)
							contract_days = (QuoteEndDate - QuoteStartDate).days
							Trace.Write('contract_days-----'+str(contract_days))
							ent_disp_val = 	str(contract_days)
						except:
							Trace.Write('except--1---')
							ent_disp_val = ""
						
						if int(ent_disp_val) > 364:
							try:
								quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
								AttributeID = 'AGS_CON_DAY'
								add_where =''
								ServiceId = service.SERVICE_ID
								whereReq =  """QUOTE_RECORD_ID ='"+str(quote_record_id)+"'  AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' AND SERVICE_ID = '{}' """.format(service.SERVICE_ID)
								ent_params_list = str(whereReq)+"||"+str(add_where)+"||"+str(AttributeID)+"||"+str(ent_disp_val)+"||"+str(ServiceId) + "||" + 'SAQTSE'
								result = ScriptExecutor.ExecuteGlobal("CQASSMEDIT", {"ACTION": 'UPDATE_ENTITLEMENT', 'ent_params_list':ent_params_list})
							except:
									pass
				
		except Exception:
			Trace.Write("except---")
			pass



	return "", warning_msg, str(ErrorequiredDict), ErrorequiredDictMSg, SecRecId, ErrorequiredtabDictMSg,notification,notificationinterval


def UpdateBurdenSettings(Column):

	UpdateBurdenSet = (
		"update PASACS set DEF_MERCH_BURDEN_FACTOR = '0.00' where PRICEAGREEMENT_RECORD_ID = '"
		+ str(Product.GetGlobal("segment_rec_id"))
		+ "' and AGMREV_ID = '"
		+ str(Product.GetGlobal("segmentRevisionId"))
		+ "'"
	)
	Trace.Write("UpdateBurdenSet---->" + str(UpdateBurdenSet))
	Sql.RunQuery(UpdateBurdenSet)


def getting_cps_tax(item_obj,quote_type):
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
	
	GetPricingProcedure = Sql.GetFirst("SELECT ISNULL(DIVISION_ID, '') as DIVISION_ID,ISNULL(COUNTRY, '') as COUNTRY, ISNULL(DISTRIBUTIONCHANNEL_ID, '') as DISTRIBUTIONCHANNEL_ID, ISNULL(SALESORG_ID, '') as SALESORG_ID, ISNULL(DOC_CURRENCY,'') as DOC_CURRENCY, ISNULL(PRICINGPROCEDURE_ID,'') as PRICINGPROCEDURE_ID, QUOTE_RECORD_ID FROM SAQTRV (NOLOCK) WHERE QUOTE_ID = '{}'".format(contract_quote_obj.QUOTE_ID))
	if GetPricingProcedure is not None:			
		PricingProcedure = GetPricingProcedure.PRICINGPROCEDURE_ID
		curr = GetPricingProcedure.DOC_CURRENCY
		dis = GetPricingProcedure.DISTRIBUTIONCHANNEL_ID
		salesorg = GetPricingProcedure.SALESORG_ID
		div = GetPricingProcedure.DIVISION_ID
		#exch = GetPricingProcedure.EXCHANGE_RATE_TYPE
		#taxk1 = GetPricingProcedure.CUSTAXCLA_ID
		country = GetPricingProcedure.COUNTRY
	#update_SAQITM = "UPDATE SAQITM SET PRICINGPROCEDURE_ID = '{prc}' WHERE SAQITM.QUOTE_ID = '{quote}'".format(prc=str(PricingProcedure), quote=self.contract_quote_id)
	#Sql.RunQuery(update_SAQITM)
	STPObj=Sql.GetFirst("SELECT ACCOUNT_ID FROM SAOPQT (NOLOCK) WHERE QUOTE_ID ='{quote}'".format(quote=contract_quote_obj.QUOTE_ID))		
	stp_account_id = ""
	if STPObj:
		stp_account_id = str(STPObj.ACCOUNT_ID)		
		
	itemid = 1	
	TreeParam = Product.GetGlobal("TreeParam")	
	Service_id = TreeParam.split('-')[1].strip()
	if item_obj:			
		item_string = '{"itemId":"'+str(itemid)+'","externalId":null,"quantity":{"value":'+str(1)+',"unit":"EA"},"exchRateType":"'+str(exch)+'","exchRateDate":"'+str(y[0])+'","productDetails":{"productId":"'+str(Service_id)+'","baseUnit":"EA","alternateProductUnits":null},"attributes":[{"name":"KOMK-LAND1","values":["'+country+'"]},{"name":"KOMK-ALAND","values":["'+country+'"]},{"name":"KOMK-REGIO","values":["TX"]},{"name":"KOMK-KUNNR","values":["'+stp_account_id+'"]},{"name":"KOMK-KUNWE","values":["'+stp_account_id+'"]},{"name":"KOMP-TAXM1","values":["'+str(item_obj.SRVTAXCLA_ID)+'"]},{"name":"KOMK-TAXK1","values":["'+str(taxk1)+'"]},{"name":"KOMK-SPART","values":["'+str(div)+'"]},{"name":"KOMP-SPART","values":["'+str(div)+'"]},{"name":"KOMP-PMATN","values":["'+str(Service_id)+'"]},{"name":"KOMK-WAERK","values":["'+str(curr)+'"]},{"name":"KOMK-HWAER","values":["'+str(curr)+'"]},{"name":"KOMP-PRSFD","values":["X"]},{"name":"KOMK-VTWEG","values":["'+str(dis)+'"]},{"name":"KOMK-VKORG","values":["'+str(salesorg)+'"]},{"name":"KOMP-KPOSN","values":["0"]},{"name":"KOMP-KZNEP","values":[""]},{"name":"KOMP-ZZEXE","values":["true"]}],"accessDateList":[{"name":"KOMK-PRSDT","value":"'+str(y[0])+'"},{"name":"KOMK-FBUDA","value":"'+str(y[0])+'"}],"variantConditions":[],"statistical":true,"subItems":[]}'
		requestdata = '{"docCurrency":"'+curr+'","locCurrency":"'+curr+'","pricingProcedure":"'+PricingProcedure+'","groupCondition":false,"itemConditionsRequired":true,"items": ['+str(item_string)+']}'
		Trace.Write("requestdata======>>>> "+str(requestdata))
		response1 = webclient.UploadString(Request_URL,str(requestdata))			
		response1 = str(response1).replace(": true", ': "true"').replace(": false", ': "false"').replace(": null",': " None"')
		response1 = eval(response1)
		Trace.Write("response1 ===> "+str(response1))
		price = []
		for root, value in response1.items():
			if root == "items":
				price = value[:]
				break
		tax_percentage = 0
		for data in price[0]['conditions']:
			if data['conditionType'] == 'ZWSC' and data['conditionTypeDescription'] == 'VAT Asia':
				tax_percentage = data['conditionRate']
				break
		# update_tax = "UPDATE SAQITM SET TAX_PERCENTAGE = {TaxPercentage} WHERE SAQITM.QUOTE_ITEM_RECORD_ID = '{ItemRecordId}'".format(
		# TaxPercentage=tax_percentage,			
		# ItemRecordId=item_obj.QUOTE_ITEM_RECORD_ID
		# )
		# Sql.RunQuery(update_tax)
		if quote_type == 'tool':
			Trace.Write("update saqico---")
			#commented the query because of removing the api_name TAX_PERCENTAGE from SAQICO - start
			# update_tax_item_covered_obj = "UPDATE SAQICO SET TAX_PERCENTAGE = {TaxPercentage} WHERE SAQICO.SERVICE_ID = '{ServiceId}' and QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID='{revision_rec_id}' ".format(
			# TaxPercentage=tax_percentage,			
			# ServiceId=TreeParam.split('-')[1].strip(),
			# QuoteRecordId=Quote.GetGlobal("contract_quote_record_id"),
			# revision_rec_id = quote_revision_record_id
			# )
			# Sql.RunQuery(update_tax_item_covered_obj)
			#commented the query because of removing the api_name TAX_PERCENTAGE from SAQICO - end	
			#update TAX column  and Extended price for each SAQICO records
			'''QueryStatement ="""UPDATE a SET a.TAX = CASE WHEN a.TAX_PERCENTAGE > 0 THEN (ISNULL(a.YEAR_1, 0)+ISNULL(a.YEAR_2, 0)+ISNULL(a.YEAR_3, 0)+ISNULL(a.YEAR_4, 0)+ISNULL(a.YEAR_5, 0)) * (a.TAX_PERCENTAGE/100) ELSE a.TAX_PERCENTAGE END FROM SAQICO a INNER JOIN SAQICO b on a.EQUIPMENT_ID = b.EQUIPMENT_ID and a.QUOTE_RECORD_ID = b.QUOTE_RECORD_ID and  a.QTEREV_RECORD_ID = b.QTEREV_RECORD_ID where a.QUOTE_RECORD_ID = '{QuoteRecordId}' and a.SERVICE_ID = '{ServiceId}' AND a.QTEREV_RECORD_ID='{revision_rec_id}'""".format(			
			ServiceId=TreeParam.split('-')[1].strip(),
			QuoteRecordId=Quote.GetGlobal("contract_quote_record_id"),
			revision_rec_id = quote_revision_record_id
			)
			Sql.RunQuery(QueryStatement)'''
			'''QueryStatement ="""UPDATE a SET a.EXTENDED_PRICE = CASE WHEN a.TAX > 0 THEN (ISNULL(a.YEAR_1, 0)+ISNULL(a.YEAR_2, 0)+ISNULL(a.YEAR_3, 0)+ISNULL(a.YEAR_4, 0)+ISNULL(a.YEAR_5, 0)) + (a.TAX) ELSE a.TAX END FROM SAQICO a INNER JOIN SAQICO b on a.EQUIPMENT_ID = b.EQUIPMENT_ID and a.QUOTE_RECORD_ID = b.QUOTE_RECORD_ID and  a.QTEREV_RECORD_ID = b.QTEREV_RECORD_ID where a.QUOTE_RECORD_ID = '{QuoteRecordId}' and a.SERVICE_ID = '{ServiceId}' AND a.QTEREV_RECORD_ID='{revision_rec_id}' """.format(			
			ServiceId=TreeParam.split('-')[1].strip(),
			QuoteRecordId=Quote.GetGlobal("contract_quote_record_id"),
			revision_rec_id = quote_revision_record_id
			)
			Sql.RunQuery(QueryStatement)'''
			#update SAQITM role up 
			# QueryStatement = """UPDATE A  SET A.EXTENDED_PRICE = B.EXTENDED_PRICE FROM SAQITM A(NOLOCK) JOIN (SELECT SUM(EXTENDED_PRICE) AS EXTENDED_PRICE,QUOTE_RECORD_ID,QTEREV_RECORD_ID,SERVICE_RECORD_ID from SAQICO(NOLOCK) WHERE QUOTE_RECORD_ID ='{QuoteRecordId}' and SERVICE_ID = '{ServiceId}' AND QTEREV_RECORD_ID='{revision_rec_id}' GROUP BY QUOTE_RECORD_ID,SERVICE_RECORD_ID,QTEREV_RECORD_ID) B ON A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.SERVICE_RECORD_ID=B.SERVICE_RECORD_ID AND A.QTEREV_RECORD_ID = B.QTEREV_RECORD_ID """.format(			
			# ServiceId=TreeParam.split('-')[1].strip(),
			# QuoteRecordId=Quote.GetGlobal("contract_quote_record_id"),
			# revision_rec_id = quote_revision_record_id
			# )
			# Sql.RunQuery(QueryStatement)
			'''QueryStatement = """UPDATE A  SET A.TAX = B.TAX FROM SAQITM A(NOLOCK) JOIN (SELECT SUM(TAX) AS TAX,QUOTE_RECORD_ID,QTEREV_RECORD_ID, SERVICE_RECORD_ID from SAQICO(NOLOCK) WHERE QUOTE_RECORD_ID ='{QuoteRecordId}' and SERVICE_ID = '{ServiceId}' AND QTEREV_RECORD_ID='{revision_rec_id}' GROUP BY QUOTE_RECORD_ID,SERVICE_RECORD_ID,QTEREV_RECORD_ID) B ON A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.SERVICE_RECORD_ID=B.SERVICE_RECORD_ID  AND A.QTEREV_RECORD_ID = B.QTEREV_RECORD_ID""".format(			
			ServiceId=TreeParam.split('-')[1].strip(),
			QuoteRecordId=Quote.GetGlobal("contract_quote_record_id"),
			revision_rec_id = quote_revision_record_id
			)
			Sql.RunQuery(QueryStatement)'''


RECORD = Param.RECORD
try:
	SecRecId = Param.SecRecId
except:
	SecRecId = ""
try:
	section_text = Param.SECTION_TEXT
except:
	section_text = ""
TreeParam = Param.TreeParam
TreeParentParam = Param.TreeParentParam
TreeSuperParentParam = Param.TreeSuperParentParam

TopSuperParentParam = Param.TopSuperParentParam
try:
	quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
except:
	quote_revision_record_id = ""

try:
	subtab_name = Param.subtab_name
except:
	subtab_name = ""

TableId = Param.TableId
Trace.Write(RECORD)
ObjectName = ""
warning_msg = ""
Trace.Write("TableId-" + str(TableId))
#Trace.Write("RECORD" + str(RECORD))
Trace.Write("TreeParam" + str(TreeParam))
Trace.Write("TreeParentParam" + str(TreeParentParam))
Trace.Write("TreeSuperParentParam" + str(TreeSuperParentParam))
Trace.Write("TopSuperParentParam" + str(TopSuperParentParam))

if (
	str(TreeParentParam) == "Tabs"
	and str(TopSuperParentParam) == "App Level Permissions"
	and str(TreeParam) != ""
	and "SYPRTB" in RECORD
):
	ObjectName = "SYPRTB"
	TableId = "SYOBJR-93159"
if TreeParam == 'Billing Matrix':    
	ObjectName = "SAQRIB"
elif TreeParentParam == "Questions" and TopSuperParentParam == "Sections":
	ObjectName = "SYPRQN"
	TableId = "SYOBJR-93188"
elif TreeParentParam == "App Level Permissions":
	ObjectName = "SYPRAP"
	TableId = "SYOBJR-93121"
elif TreeParam == "Quote Documents":
	ObjectName = "SAQDOC"
	TableId = " "
elif TreeParentParam == "Actions" and TopSuperParentParam == "Sections":
	ObjectName = "SYPRSN"
	TableId = "SYOBJR-93160"
elif TopSuperParentParam == "Tabs" and TreeParentParam == "Actions":
	ObjectName = "SYPRSN"
	TableId = "SYOBJR-93160"
elif TreeParentParam == "Actions" and TopSuperParentParam == "Sections":
	ObjectName = "SYPRAC"
	TableId = "SYOBJR-93188"
elif TreeParentParam == "Questions" and TopSuperParentParam == "Sections" and TableId == "SYOBJR-93159":
	ObjectName = "SYPRTB"
elif TreeParam == "Quote Information" and TableId == "SYOBJR-98798":
	ObjectName = "SAQTIP"    
elif TreeParam == "Quote Information":
	ObjectName = "SAQTRV"
	
elif TreeParam == "Approval Chain Information":
	ObjectName = "ACAPCH"
	
elif TreeSuperParentParam == "Constraints":
	ObjectName = "SYOBJC"
	
elif TableId is not None:
	objr_obj = Sql.GetFirst("select * FROM SYOBJR where SAPCPQ_ATTRIBUTE_NAME = '" + str(TableId) + "' ")
	Trace.Write("select * FROM SYOBJR where SAPCPQ_ATTRIBUTE_NAME = '" + str(TableId) + "' ")
	if objr_obj is not None:
		objr_obj_id = str(objr_obj.OBJ_REC_ID)
		Trace.Write("objr_obj_id" + str(objr_obj_id))
		if objr_obj_id is not None:
			objh_obj = Sql.GetFirst("select * FROM SYOBJH where RECORD_ID = '" + str(objr_obj_id) + "' ")
			Trace.Write("select * FROM SYOBJH where RECORD_ID = '" + str(objr_obj_id) + "' ")
			if objh_obj is not None:
				ObjectName = str(objh_obj.OBJECT_NAME)



ApiResponse = ApiResponseFactory.JsonResponse(MaterialSave(ObjectName, RECORD, warning_msg, SecRecId,subtab_name))


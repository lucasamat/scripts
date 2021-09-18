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

Sql = SQL()
#from PAUPDDRYFG import DirtyFlag

import re
#from datetime import datetime


login_is_admin = User.IsAdmin

def insert_items_billing_plan(contract_quote_record_id=None, total_months=1, billing_date=''):     
	Sql.RunQuery("""INSERT SAQIBP (
					QUOTE_ITEM_BILLING_PLAN_RECORD_ID, BILLING_END_DATE, BILLING_START_DATE, BILLING_TYPE, 
					LINE_ITEM_ID, QUOTE_ID, QTEITM_RECORD_ID, QUOTE_NAME, 
					QUOTE_RECORD_ID,QTEREV_RECORD_ID,QTEREV_ID, SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID,
					BILLING_AMOUNT, BILLING_DATE, BILLING_INTERVAL, BILLING_YEAR,
					EQUIPMENT_DESCRIPTION, EQUIPMENT_ID, EQUIPMENT_LINE_ID, EQUIPMENT_RECORD_ID, PO_ITEM, PO_NUMBER, QTEITMCOB_RECORD_ID, 
					SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, ANNUAL_BILLING_AMOUNT, GREENBOOK, GREENBOOK_RECORD_ID,
					BILLING_CURRENCY, BILLING_CURRENCY_RECORD_ID, SERIAL_NUMBER,
					CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED
				) 
				SELECT 
					CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_BILLING_PLAN_RECORD_ID,  
					SAQICO.WARRANTY_END_DATE as BILLING_END_DATE,
					SAQICO.WARRANTY_START_DATE as BILLING_START_DATE,
					SAQTSE.ENTITLEMENT_VALUE_CODE as BILLING_TYPE,
					SAQICO.LINE_ITEM_ID AS LINE_ITEM_ID,                                       
					SAQICO.QUOTE_ID,
					SAQICO.QTEITM_RECORD_ID,
					SAQICO.QUOTE_NAME,
					SAQICO.QUOTE_RECORD_ID,
					SAQICO.QTEREV_RECORD_ID,
					SAQICO.QTEREV_ID,
					SAQICO.SALESORG_ID,
					SAQICO.SALESORG_NAME,
					SAQICO.SALESORG_RECORD_ID,
					ISNULL(YEAR_1, 0) / {Months} BILLING_AMOUNT,	
					{BillingDate} as BILLING_DATE,				
					'MONTHLY' as BILLING_INTERVAL,
					0 as BILLING_YEAR,
					SAQICO.EQUIPMENT_DESCRIPTION,
					SAQICO.EQUIPMENT_ID,
					SAQICO.EQUIPMENT_LINE_ID,
					SAQICO.EQUIPMENT_RECORD_ID,
					'' as PO_ITEM,
					'' as PO_NUMBER,
					SAQICO.QUOTE_ITEM_COVERED_OBJECT_RECORD_ID as QTEITMCOB_RECORD_ID,
					SAQICO.SERVICE_DESCRIPTION,
					SAQICO.SERVICE_ID,
					SAQICO.SERVICE_RECORD_ID,
					ISNULL(SAQICO.YEAR_1, 0) AS ANNUAL_BILLING_AMOUNT,
					SAQICO.GREENBOOK,
					SAQICO.GREENBOOK_RECORD_ID,
					'' AS BILLING_CURRENCY,
					'' AS BILLING_CURRENCY_RECORD_ID,
					SAQICO.SERIAL_NO AS SERIAL_NUMBER,                     
					{UserId} as CPQTABLEENTRYADDEDBY, 
					GETDATE() as CPQTABLEENTRYDATEADDED
				FROM SAQICO (NOLOCK)     
				JOIN SAQTSE (NOLOCK) ON SAQTSE.QUOTE_RECORD_ID = SAQICO.QUOTE_RECORD_ID AND  SAQTSE.QTEREV_RECORD_ID = SAQICO.QTEREV_RECORD_ID AND QTQTSE.ENTITLEMENT_NAME = 'FIXED_PRICE_PER_RESOU_EVENT_91'                    
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
					WHERE SYSTAB.SUBTAB_NAME = 'Detail' AND SYOBJH.OBJECT_NAME = 'SAQTBP'
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




def MaterialSave(ObjectName, RECORD, warning_msg, SectionRecId=None):
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
		
	TreeParam = Product.GetGlobal("TreeParam")
	if Product.GetGlobal("TreeParentLevel2") == "Quote Items":
		ObjectName = "SAQIGB"
	elif Product.GetGlobal("TreeParentLevel1") == "Quote Items":
		ObjectName = "SAQIFL"
	if str(ObjectName) == "SYPRSN":
		
		permissions_id_val = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00128").GetValue()
		sect_edit = RECORD.get("EDITABLE")
		
		VISIBLEval = RECORD.get("VISIBLE")
		sect_name = RECORD.get("SECTION_ID")
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
				if TableName == 'SAQTBP':
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
									FROM SAQTBP (NOLOCK) 
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
					if TableName == "SAQITM":
						if newdict.has_key("TAX_PERCENTAGE") or newdict.has_key("BD_PRICE_MARGIN") or newdict.has_key("TARGET_PRICE_MARGIN") :
							newdict["TAX_PERCENTAGE"] = (newdict.get("TAX_PERCENTAGE").replace("%", "").strip())
							newdict["BD_PRICE_MARGIN"] = (newdict.get("BD_PRICE_MARGIN").replace("%", "").strip())
							newdict["TARGET_PRICE_MARGIN"] = (newdict.get("BD_PRICE_MARGIN").replace("%", "").strip())
							dictc = {"CpqTableEntryId": str(sql_cpq.CpqTableEntryId)}
							newdict.update(dictc)
							tableInfo = Sql.GetTable(str(TableName))
							tablerow = newdict
							tableInfo.AddRow(tablerow)
							Sql.Upsert(tableInfo)
							item_obj = Sql.GetFirst("select SRVTAXCAT_RECORD_ID,SRVTAXCAT_DESCRIPTION,SRVTAXCAT_ID,SRVTAXCLA_DESCRIPTION,SRVTAXCLA_ID,SRVTAXCLA_RECORD_ID from SAQITM where SERVICE_ID = '{Service_id}' and QUOTE_RECORD_ID = '{contract_quote_record_id}' AND QTEREV_RECORD_ID = '{revision_rec_id}'".format(Service_id = '-'.join(TreeParam.split('-')[1:]).strip(),contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id"),revision_rec_id = quote_revision_record_id))
							quote_item_covered_obj = """UPDATE SAQICO SET SRVTAXCAT_ID = '{}',SRVTAXCAT_DESCRIPTION = '{}',SRVTAXCAT_RECORD_ID = '{}',SRVTAXCLA_ID = '{}',SRVTAXCLA_DESCRIPTION = '{}',SRVTAXCLA_RECORD_ID = '{}' where SERVICE_ID = '{}' and QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' """.format(item_obj.SRVTAXCAT_ID,item_obj.SRVTAXCAT_DESCRIPTION,item_obj.SRVTAXCAT_RECORD_ID,item_obj.SRVTAXCLA_ID,item_obj.SRVTAXCLA_DESCRIPTION,item_obj.SRVTAXCLA_RECORD_ID,'-'.join(TreeParam.split('-')[1:]).strip(),Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id )
							Sql.RunQuery(quote_item_covered_obj)
							check_itm_obj = Sql.GetFirst("""SELECT
													QUOTE_ITEM_RECORD_ID,
													CONVERT(int, OBJECT_QUANTITY) as OBJECT_QUANTITY,
													ISNULL(SRVTAXCLA_ID,1) as SRVTAXCLA_ID
													FROM SAQITM (NOLOCK) WHERE QUOTE_RECORD_ID = '{QUOTE_RECORD_ID}' AND QTEREV_RECORD_ID = '{revision_rec_id}' AND SERVICE_ID LIKE '%{SERVICE_ID}%'
													""".format(
							QUOTE_RECORD_ID=Quote.GetGlobal("contract_quote_record_id"), SERVICE_ID=TreeParam.split('-')[1].strip() +" - "+TreeParam.split('-')[2].strip(), revision_rec_id = quote_revision_record_id
							))
							getting_cps_tax(check_itm_obj,'tool')
					#A055S000P01-4288 start
					elif TableName == "SAQTRV":
						dictc = {"CpqTableEntryId": str(sql_cpq.CpqTableEntryId)}
						newdict.update(dictc)
						tableInfo = Sql.GetTable(str(TableName))
						tablerow = newdict
						tableInfo.AddRow(tablerow)
						Sql.Upsert(tableInfo)
						getactive = newdict.get("ACTIVE")
						get_record_val =  newdict.get("QUOTE_REVISION_RECORD_ID")
						get_rev_val =  newdict.get("QTEREV_ID")
						get_status = newdict.get("REVISION_STATUS")
						get_approved_date = newdict.get("REV_APPROVE_DATE")
						if getactive == 'false':
							getactive = 0
						else:
							getactive = 1
						if getactive == 1:
							update_quote_rev = Sql.RunQuery("""UPDATE SAQTRV SET ACTIVE = {active_rev} WHERE QUOTE_ID = '{QuoteRecordId}' and  QUOTE_REVISION_RECORD_ID != '{get_record_val}'""".format(QuoteRecordId=newdict.get("QUOTE_ID"),active_rev = 0,get_record_val =get_record_val))
							Sql.RunQuery("""UPDATE SAQTMT SET QTEREV_ID = {newrev_inc},QTEREV_RECORD_ID = '{quote_revision_id}',ACTIVE_REV={active_rev} WHERE QUOTE_ID = '{QuoteRecordId}'""".format(quote_revision_id=get_record_val,newrev_inc= get_rev_val,QuoteRecordId=newdict.get("QUOTE_ID"),active_rev = 1))
						
						productdesc = SqlHelper.GetFirst("sp_executesql @t=N'update CART_REVISIONS set DESCRIPTION =''"+str(newdict.get("REVISION_DESCRIPTION"))+"'' where CART_ID = ''"+str(Quote.QuoteId)+"'' and VISITOR_ID =''"+str(Quote.UserId)+"''  '")
						get_quote_info_details = Sql.GetFirst("select * from SAQTMT where QUOTE_ID = '"+str(Quote.CompositeNumber)+"'")
						Quote.SetGlobal("contract_quote_record_id",get_quote_info_details.MASTER_TABLE_QUOTE_RECORD_ID)
						Quote.SetGlobal("quote_revision_record_id",str(get_quote_info_details.QTEREV_RECORD_ID))
						if get_status.upper() == "APPROVED":
							##Updating the Revision Approved Date while changing the status to Approved...
							if get_approved_date == "":
								RevisionApprovedDate = datetime.now().date()
								Sql.RunQuery("UPDATE SAQTRV SET REV_APPROVE_DATE = '{RevisionApprovedDate}' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' ".format(RevisionApprovedDate = RevisionApprovedDate,QuoteRecordId = Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id")))
							##Updating the Revision Approved Date while changing the status to Approved...
							crm_result = ScriptExecutor.ExecuteGlobal('QTPOSTACRM',{'QUOTE_ID':str(newdict.get("QUOTE_ID")),'REVISION_ID':str(get_rev_val),'Fun_type':'cpq_to_crm'})
					#A055S000P01-4288 end
					elif TableName == "SAQIGB":
						dictc = {"CpqTableEntryId": str(sql_cpq.CpqTableEntryId)}
						newdict.update(dictc)
						tableInfo = Sql.GetTable(str(TableName))
						tablerow = newdict
						tableInfo.AddRow(tablerow)
						Sql.Upsert(tableInfo)
						VALUE = float(newdict.get("DISCOUNT"))
						Trace.Write("Discount = "+str(newdict.get("DISCOUNT")))
						contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
						quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
						decimal_discount = VALUE / 100.0
						Sql.RunQuery("""UPDATE SAQICO SET 
														NET_PRICE = ISNULL(TARGET_PRICE,0) - (ISNULL(TARGET_PRICE,0) * {DecimalDiscount}),NET_PRICE_INGL_CURR =ISNULL(TARGET_PRICE_INGL_CURR,0) + (ISNULL(TARGET_PRICE_INGL_CURR,0) * {DecimalDiscount}),
														YEAR_1 = ISNULL(TARGET_PRICE,0) - (ISNULL(TARGET_PRICE,0) * {DecimalDiscount}),
														DISCOUNT = '{plus}{Discount}',YEAR_1_INGL_CURR = ISNULL(TARGET_PRICE_INGL_CURR,0) + (ISNULL(TARGET_PRICE_INGL_CURR,0) * {DecimalDiscount})
													FROM SAQICO (NOLOCK)                                     
													WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND GREENBOOK = '{TreeParam}' AND FABLOCATION_ID = '{TreeParentParam}'""".format(
														QuoteRecordId=contract_quote_record_id,
														RevisionRecordId=quote_revision_record_id,
														DecimalDiscount=decimal_discount if decimal_discount > 0 else 1,
														Discount=VALUE,
														plus="+",
														TreeParam=TreeParam,TreeParentParam=TreeParentParam))
						#self._update_year()
						for count in range(2, 6):
							Sql.RunQuery("""UPDATE SAQICO SET
															SAQICO.YEAR_{Year} = CASE  
																WHEN CAST(DATEDIFF(day,SAQTMT.CONTRACT_VALID_FROM,SAQTMT.CONTRACT_VALID_TO) / 365.2425 AS INT) >= {Count} 
																	THEN ISNULL(SAQICO.YEAR_{Count}, 0) - (ISNULL(SAQICO.YEAR_{Count}, 0) * ISNULL(SAQICO.YEAR_OVER_YEAR, 0))/100.0                                                   
																ELSE 0
															END, SAQICO.YEAR_{Year}_INGL_CURR = CASE  
																WHEN CAST(DATEDIFF(day,SAQTMT.CONTRACT_VALID_FROM,SAQTMT.CONTRACT_VALID_TO) / 365.2425 AS INT) >= {Count} 
																	THEN ISNULL(SAQICO.YEAR_{Count}_INGL_CURR, 0) - (ISNULL(SAQICO.YEAR_{Count}_INGL_CURR, 0) * ISNULL(SAQICO.YEAR_OVER_YEAR, 0))/100.0                                                   
																ELSE 0
															END
														FROM SAQICO (NOLOCK) 
														JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQICO.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = SAQICO.QTEREV_RECORD_ID
														WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQICO.GREENBOOK = '{TreeParam}' AND SAQICO.FABLOCATION_ID = '{TreeParentParam}'""".format(
															QuoteRecordId=contract_quote_record_id,
															RevisionRecordId=quote_revision_record_id,
															Year=count,
															Count=count - 1,
															TreeParam=TreeParam,
															TreeParentParam=TreeParentParam
															)
										)    
						Sql.RunQuery("""UPDATE SAQICO SET 
														NET_VALUE = ISNULL(YEAR_1,0) + ISNULL(YEAR_2,0) + ISNULL(YEAR_3,0) + ISNULL(YEAR_4,0) + ISNULL(YEAR_5,0),
														NET_VALUE_INGL_CURR = ISNULL(YEAR_1_INGL_CURR,0) + ISNULL(YEAR_2_INGL_CURR,0) + ISNULL(YEAR_3_INGL_CURR,0) + ISNULL(YEAR_4_INGL_CURR,0) + ISNULL(YEAR_5_INGL_CURR,0)
													FROM SAQICO (NOLOCK)                                     
													WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND GREENBOOK = '{TreeParam}' AND FABLOCATION_ID = '{TreeParentParam}'""".format(
														QuoteRecordId=contract_quote_record_id,
														RevisionRecordId=quote_revision_record_id,
														TreeParam=TreeParam,
														TreeParentParam=TreeParentParam
														))
						c = Sql.GetFirst("SELECT SUM(NET_PRICE) AS SUM_PRICE,SUM(NET_PRICE_INGL_CURR) AS SUM_PRICE_INGL_CURR, SUM(YEAR_1) AS YEAR1, SUM(YEAR_1_INGL_CURR) AS YEAR1_INGL_CURR, SUM(YEAR_2) AS YEAR2,SUM(YEAR_2_INGL_CURR) AS YEAR2_INGL_CURR, SUM(YEAR_3) AS YEAR3, SUM(YEAR_3_INGL_CURR) AS YEAR3_INGL_CURR, SUM(YEAR_4) AS YEAR4, SUM(YEAR_4_INGL_CURR) AS YEAR4_INGL_CURR, SUM(YEAR_5) AS YEAR5, SUM(YEAR_5_INGL_CURR) AS YEAR5_INGL_CURR FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}' AND GREENBOOK = '{}'  AND FABLOCATION_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(contract_quote_record_id,TreeSuperParentParam.split("-")[1].strip(),TreeParam,TreeParentParam,quote_revision_record_id))
						Sql.RunQuery("UPDATE SAQIGB SET NET_PRICE = '{}',YEAR_1 = {y1},YEAR_2 = {y2},YEAR_3={y3},YEAR_4={y4},YEAR_5 = {y5},NET_PRICE_INGL_CURR = '{}',YEAR_1_INGL_CURR = {y1_gl},YEAR_2_INGL_CURR = {y2_gl},YEAR_3_INGL_CURR={y3_gl},YEAR_4_INGL_CURR={y4_gl},YEAR_5_INGL_CURR = {y5_gl}  WHERE QUOTE_RECORD_ID = '{}' AND SERVICE_ID LIKE '%{}%' AND GREENBOOK = '{}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND FABLOCATION_ID = '{TreeParentParam}'".format(float(c.SUM_PRICE),float(c.NET_PRICE_INGL_CURR),contract_quote_record_id,TreeSuperParentParam.split("-")[1].strip(),TreeParam,y1=c.YEAR1,y2=c.YEAR2,y3=c.YEAR3,y4=c.YEAR4,y5=c.YEAR5,y1_gl=c.YEAR1_INGL_CURR,y2_gl=c.YEAR2_INGL_CURR,y3_gl=c.YEAR3_INGL_CURR,y4_gl=c.YEAR4_INGL_CURR,y5_gl=c.YEAR5_INGL_CURR,quote_revision_record_id=quote_revision_record_id,TreeParentParam=TreeParentParam))
						Sql.RunQuery("""UPDATE SAQITM
											SET 
											NET_VALUE = IQ.NET_VALUE,
											NET_PRICE = IQ.NET_PRICE,
											YEAR_1 = IQ.YEAR_1,
											YEAR_2 = IQ.YEAR_2,
											NET_VALUE_INGL_CURR = IQ.NET_VALUE_INGL_CURR,
											NET_PRICE_INGL_CURR = IQ.NET_PRICE_INGL_CURR,
											YEAR_1_INGL_CURR = IQ.YEAR_1_INGL_CURR,
											YEAR_2_INGL_CURR = IQ.YEAR_2_INGL_CURR,
											DISCOUNT = '{plus}{Discount}'					
											FROM SAQITM (NOLOCK)
											INNER JOIN (SELECT SAQITM.CpqTableEntryId,
														CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.NET_VALUE, 0)), 0), 0) as decimal(18,2)) as NET_VALUE,
														CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.NET_PRICE, 0)), 0), 0) as decimal(18,2)) as NET_PRICE,
														CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_1, 0)), 0), 0) as decimal(18,2)) as YEAR_1,
														CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_2, 0)), 0), 0) as decimal(18,2)) as YEAR_2,
														CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.NET_VALUE_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as NET_VALUE_INGL_CURR,
														CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.NET_PRICE_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as NET_PRICE_INGL_CURR,
														CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_1_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as YEAR_1_INGL_CURR,
														CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_2_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as YEAR_2_INGL_CURR
														FROM SAQITM (NOLOCK) 
														JOIN SAQICO (NOLOCK) ON SAQICO.QUOTE_RECORD_ID = SAQITM.QUOTE_RECORD_ID AND SAQICO.LINE_ITEM_ID = SAQITM.LINE_ITEM_ID
														WHERE SAQITM.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQITM.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQICO.GREENBOOK = '{TreeParam}' AND SAQICO.FABLOCATION_ID = '{TreeParentParam}'
														GROUP BY SAQITM.LINE_ITEM_ID, SAQITM.QUOTE_RECORD_ID, SAQITM.CpqTableEntryId,SAQITM.QTEREV_RECORD_ID)IQ
											ON SAQITM.CpqTableEntryId = IQ.CpqTableEntryId 
											WHERE SAQITM.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQITM.QTEREV_RECORD_ID = '{RevisionRecordId}' """.format(QuoteRecordId=contract_quote_record_id,RevisionRecordId=quote_revision_record_id,
											Discount=VALUE,plus="+",TreeParam=TreeParam,TreeParentParam=TreeParentParam))
						quote_currency = str(Quote.GetCustomField('Currency').Content)		
						total_net_price = 0.00		
						total_year_1 = 0.00
						total_year_2 = 0.00        
						total_net_value = 0.00
						items_data = {}

						items_obj = Sql.GetList("SELECT SERVICE_ID, LINE_ITEM_ID, ISNULL(YEAR_1, 0) as YEAR_1 ,ISNULL(YEAR_2, 0) as YEAR_2 , ISNULL(NET_VALUE,0) AS NET_VALUE, ISNULL(NET_PRICE, 0) as NET_PRICE FROM SAQITM (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(contract_quote_record_id,quote_revision_record_id,TreeParam))
						if items_obj:
							for item_obj in items_obj:
								items_data[int(float(item_obj.LINE_ITEM_ID))] = {'NET_VALUE':item_obj.NET_VALUE, 'SERVICE_ID':(item_obj.SERVICE_ID.replace('- BASE', '')).strip(), 'YEAR_1':item_obj.YEAR_1, 'YEAR_2':item_obj.YEAR_2, 'NET_PRICE':item_obj.NET_PRICE}
						for item in Quote.MainItems:
							item_number = int(item.RolledUpQuoteItem)
							if item_number in items_data.keys():
								if items_data.get(item_number).get('SERVICE_ID') == item.PartNumber:
									item_data = items_data.get(item_number)
									item.NET_PRICE.Value = float(item_data.get('NET_PRICE'))
									total_net_price += item.NET_PRICE.Value
									item.NET_VALUE.Value = item_data.get('NET_VALUE')
									total_net_value += item.NET_VALUE.Value	
									item.YEAR_1.Value = item_data.get('YEAR_1')
									total_year_1 += item.YEAR_1.Value
									item.YEAR_2.Value = item_data.get('YEAR_2')
									total_year_2 += item.YEAR_2.Value        
									item.DISCOUNT.Value = "+"+str(VALUE)
						##Added the percentage symbol for discount custom field...
						Percentage = '%'
						Quote.GetCustomField('DISCOUNT').Content = "+"+str(VALUE)+ " " + Percentage
						#discount_value = Quote.GetCustomField('DISCOUNT').Content
						#Trace.Write("discount"+str(discount_value))
						Quote.GetCustomField('TOTAL_NET_PRICE').Content =str(total_net_price) + " " + quote_currency
						Quote.GetCustomField('YEAR_1').Content = str(total_year_1) + " " + quote_currency
						Quote.GetCustomField('YEAR_2').Content = str(total_year_2) + " " + quote_currency      
						Quote.GetCustomField('TOTAL_NET_VALUE').Content = str(total_net_value) + " " + quote_currency
						Quote.Save()
					elif TableName == "SAQIFL":
						dictc = {"CpqTableEntryId": str(sql_cpq.CpqTableEntryId)}
						newdict.update(dictc)
						tableInfo = Sql.GetTable(str(TableName))
						tablerow = newdict
						tableInfo.AddRow(tablerow)
						Sql.Upsert(tableInfo)
						VALUE = float(newdict.get("DISCOUNT"))
						Trace.Write("Discount = "+str(newdict.get("DISCOUNT")))
						contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
						quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
						decimal_discount = VALUE / 100.0
						Sql.RunQuery("""UPDATE SAQICO SET 
														NET_PRICE = ISNULL(TARGET_PRICE,0) - (ISNULL(TARGET_PRICE,0) * {DecimalDiscount}),
														YEAR_1 = ISNULL(TARGET_PRICE,0) - (ISNULL(TARGET_PRICE,0) * {DecimalDiscount}),
														NET_PRICE_INGL_CURR = ISNULL(TARGET_PRICE_INGL_CURR,0) - (ISNULL(TARGET_PRICE_INGL_CURR,0) * {DecimalDiscount}),
														YEAR_1_INGL_CURR = ISNULL(TARGET_PRICE_INGL_CURR,0) - (ISNULL(TARGET_PRICE_INGL_CURR,0) * {DecimalDiscount}),
														DISCOUNT = '{plus}{Discount}'
													FROM SAQICO (NOLOCK)                                     
													WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND FABLOCATION_ID = '{TreeParam}'""".format(
														QuoteRecordId=contract_quote_record_id,
														RevisionRecordId=quote_revision_record_id,
														DecimalDiscount=decimal_discount if decimal_discount > 0 else 1,
														Discount=VALUE,
														plus="+",
														TreeParam=TreeParam))
						#self._update_year()
						for count in range(2, 6):
							Sql.RunQuery("""UPDATE SAQICO SET
															SAQICO.YEAR_{Year} = CASE  
																WHEN CAST(DATEDIFF(day,SAQTMT.CONTRACT_VALID_FROM,SAQTMT.CONTRACT_VALID_TO) / 365.2425 AS INT) >= {Count} 
																	THEN ISNULL(SAQICO.YEAR_{Count}, 0) - (ISNULL(SAQICO.YEAR_{Count}, 0) * ISNULL(SAQICO.YEAR_OVER_YEAR, 0))/100.0                                                   
																ELSE 0
															END,
															SAQICO.YEAR_{Year}_INGL_CURR = CASE  
																WHEN CAST(DATEDIFF(day,SAQTMT.CONTRACT_VALID_FROM,SAQTMT.CONTRACT_VALID_TO) / 365.2425 AS INT) >= {Count} 
																	THEN ISNULL(SAQICO.YEAR_{Count}_INGL_CURR, 0) - (ISNULL(SAQICO.YEAR_{Count}_INGL_CURR, 0) * ISNULL(SAQICO.YEAR_OVER_YEAR, 0))/100.0                                                   
																ELSE 0
															END
														FROM SAQICO (NOLOCK) 
														JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQICO.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = SAQICO.QTEREV_RECORD_ID
														WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQICO.FABLOCATION_ID = '{TreeParam}'""".format(
															QuoteRecordId=contract_quote_record_id,
															RevisionRecordId=quote_revision_record_id,
															Year=count,
															Count=count - 1,
															TreeParam=TreeParam
															)
										)    
						Sql.RunQuery("""UPDATE SAQICO SET 
														NET_VALUE = ISNULL(YEAR_1,0) + ISNULL(YEAR_2,0) + ISNULL(YEAR_3,0) + ISNULL(YEAR_4,0) + ISNULL(YEAR_5,0),
														NET_VALUE_INGL_CURR = ISNULL(YEAR_1_INGL_CURR,0) + ISNULL(YEAR_2_INGL_CURR,0) + ISNULL(YEAR_3_INGL_CURR,0) + ISNULL(YEAR_4_INGL_CURR,0) + ISNULL(YEAR_5_INGL_CURR,0)
													FROM SAQICO (NOLOCK)                                     
													WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND FABLOCATION_ID = '{TreeParam}'""".format(
														QuoteRecordId=contract_quote_record_id,
														RevisionRecordId=quote_revision_record_id,
														TreeParam=TreeParam
														))
						c = Sql.GetFirst("SELECT SUM(NET_PRICE) AS SUM_PRICE, SUM(YEAR_1) AS YEAR1, SUM(YEAR_2) AS YEAR2, SUM(YEAR_3) AS YEAR3, SUM(YEAR_4) AS YEAR4, SUM(YEAR_5) AS YEAR5, SUM(NET_PRICE_INGL_CURR) AS SUM_PRICE_INGL_CURR, SUM(YEAR_1_INGL_CURR) AS YEAR1_INGL_CURR, SUM(YEAR_2_INGL_CURR) AS YEAR2_INGL_CURR, SUM(YEAR_3_INGL_CURR) AS YEAR3_INGL_CURR, SUM(YEAR_4_INGL_CURR) AS YEAR4_INGL_CURR, SUM(YEAR_5_INGL_CURR) AS YEAR5_INGL_CURR FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}' AND FABLOCATION_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(contract_quote_record_id,TreeParentParam.split("-")[1].strip(),TreeParam,quote_revision_record_id))
						Sql.RunQuery("UPDATE SAQIFL SET DISCOUNT = {},NET_PRICE = '{}',YEAR_1 = {y1},YEAR_2 = {y2},YEAR_3={y3},YEAR_4={y4},YEAR_5 = {y5},NET_PRICE = '{}',YEAR_1 = {y1_gl},YEAR_2 = {y2_gl},YEAR_3={y3_gl},YEAR_4={y4_gl},YEAR_5 = {y5_gl}  WHERE QUOTE_RECORD_ID = '{}' AND SERVICE_ID LIKE '%{}%' AND FABLOCATION_ID = '{}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}'".format(float(VALUE),float(c.SUM_PRICE),float(VALUE),float(c.SUM_PRICE_INGL_CURR),contract_quote_record_id,TreeParentParam.split("-")[1].strip(),TreeParam,y1=c.YEAR1,y2=c.YEAR2,y3=c.YEAR3,y4=c.YEAR4,y5=c.YEAR5,y1_gl=c.YEAR1_INGL_CURR,y2_gl=c.YEAR2_INGL_CURR,y3_gl=c.YEAR3_INGL_CURR,y4_gl=c.YEAR4_INGL_CURR,y5_gl=c.YEAR5_INGL_CURR,quote_revision_record_id=quote_revision_record_id))
						Sql.RunQuery("""UPDATE SAQITM
											SET 
											NET_VALUE = IQ.NET_VALUE,
											NET_PRICE = IQ.NET_PRICE,
											YEAR_1 = IQ.YEAR_1,
											YEAR_2 = IQ.YEAR_2,
											NET_VALUE_INGL_CURR = IQ.NET_VALUE_INGL_CURR,
											NET_PRICE_INGL_CURR = IQ.NET_PRICE_INGL_CURR,
											YEAR_1_INGL_CURR = IQ.YEAR_1_INGL_CURR,
											YEAR_2_INGL_CURR = IQ.YEAR_2_INGL_CURR,
											DISCOUNT = '{plus}{Discount}'					
											FROM SAQITM (NOLOCK)
											INNER JOIN (SELECT SAQITM.CpqTableEntryId,
														CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.NET_VALUE, 0)), 0), 0) as decimal(18,2)) as NET_VALUE,
														CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.NET_PRICE, 0)), 0), 0) as decimal(18,2)) as NET_PRICE,
														CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_1, 0)), 0), 0) as decimal(18,2)) as YEAR_1,
														CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_2, 0)), 0), 0) as decimal(18,2)) as YEAR_2,
														CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.NET_VALUE_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as NET_VALUE_INGL_CURR,
														CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.NET_PRICE_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as NET_PRICE_INGL_CURR,
														CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_1_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as YEAR_1_INGL_CURR,
														CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_2_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as YEAR_2_INGL_CURR
														FROM SAQITM (NOLOCK) 
														JOIN SAQICO (NOLOCK) ON SAQICO.QUOTE_RECORD_ID = SAQITM.QUOTE_RECORD_ID AND SAQICO.LINE_ITEM_ID = SAQITM.LINE_ITEM_ID
														WHERE SAQITM.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQITM.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQICO.FABLOCATION_ID = '{TreeParam}'
														GROUP BY SAQITM.LINE_ITEM_ID, SAQITM.QUOTE_RECORD_ID, SAQITM.CpqTableEntryId,SAQITM.QTEREV_RECORD_ID)IQ
											ON SAQITM.CpqTableEntryId = IQ.CpqTableEntryId 
											WHERE SAQITM.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQITM.QTEREV_RECORD_ID = '{RevisionRecordId}' """.format(QuoteRecordId=contract_quote_record_id,RevisionRecordId=quote_revision_record_id,
											Discount=VALUE,plus="+",TreeParam=TreeParam))
						quote_currency = str(Quote.GetCustomField('Currency').Content)		
						total_net_price = 0.00		
						total_year_1 = 0.00
						total_year_2 = 0.00        
						total_net_value = 0.00
						items_data = {}

						items_obj = Sql.GetList("SELECT SERVICE_ID, LINE_ITEM_ID, ISNULL(YEAR_1, 0) as YEAR_1 ,ISNULL(YEAR_2, 0) as YEAR_2 , ISNULL(NET_VALUE,0) AS NET_VALUE, ISNULL(NET_PRICE, 0) as NET_PRICE FROM SAQITM (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(contract_quote_record_id,quote_revision_record_id,TreeParam))
						if items_obj:
							for item_obj in items_obj:
								items_data[int(float(item_obj.LINE_ITEM_ID))] = {'NET_VALUE':item_obj.NET_VALUE, 'SERVICE_ID':(item_obj.SERVICE_ID.replace('- BASE', '')).strip(), 'YEAR_1':item_obj.YEAR_1, 'YEAR_2':item_obj.YEAR_2, 'NET_PRICE':item_obj.NET_PRICE}
						for item in Quote.MainItems:
							item_number = int(item.RolledUpQuoteItem)
							if item_number in items_data.keys():
								if items_data.get(item_number).get('SERVICE_ID') == item.PartNumber:
									item_data = items_data.get(item_number)
									item.NET_PRICE.Value = float(item_data.get('NET_PRICE'))
									total_net_price += item.NET_PRICE.Value
									item.NET_VALUE.Value = item_data.get('NET_VALUE')
									total_net_value += item.NET_VALUE.Value	
									item.YEAR_1.Value = item_data.get('YEAR_1')
									total_year_1 += item.YEAR_1.Value
									item.YEAR_2.Value = item_data.get('YEAR_2')
									total_year_2 += item.YEAR_2.Value        
									item.DISCOUNT.Value = "+"+str(VALUE)
						##Added the percentage symbol for discount custom field...
						Percentage = '%'
						Quote.GetCustomField('DISCOUNT').Content = "+"+str(VALUE)+ " " + Percentage
						#discount_value = Quote.GetCustomField('DISCOUNT').Content
						#Trace.Write("discount"+str(discount_value))
						Quote.GetCustomField('TOTAL_NET_PRICE').Content =str(total_net_price) + " " + quote_currency
						Quote.GetCustomField('YEAR_1').Content = str(total_year_1) + " " + quote_currency
						Quote.GetCustomField('YEAR_2').Content = str(total_year_2) + " " + quote_currency      
						Quote.GetCustomField('TOTAL_NET_VALUE').Content = str(total_net_value) + " " + quote_currency
						Quote.Save()

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
				
				if TableName == 'SAQTBP' and old_billing_matrix_obj:                    
					billing_matrix_obj = Sql.GetFirst("""SELECT BILLING_START_DATE, 
									BILLING_END_DATE, QUOTE_BILLING_PLAN_RECORD_ID, BILLING_DAY
									FROM SAQTBP (NOLOCK)
									WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' """.format(Product.GetGlobal("contract_quote_record_id"), quote_revision_record_id ))
					if billing_matrix_obj:
						if billing_matrix_obj.BILLING_START_DATE != old_billing_matrix_obj.BILLING_START_DATE or billing_matrix_obj.BILLING_END_DATE != old_billing_matrix_obj.BILLING_END_DATE or billing_matrix_obj.BILLING_DAY != old_billing_matrix_obj.BILLING_DAY:                        						
							billing_query = "UPDATE SAQTBP SET IS_CHANGED = 1 WHERE QUOTE_BILLING_PLAN_RECORD_ID ='{}'".format(billing_matrix_obj.QUOTE_BILLING_PLAN_RECORD_ID)
							Sql.RunQuery(billing_query)
					#generate_year_based_billing_matrix(newdict)
				if TableName == 'SAQTIP':
					Trace.Write('SAQTIP_CHK_J '+str(RECORD['PARTY_ROLE']))
					account_details = Sql.GetFirst("SELECT * FROM SAACNT (NOLOCK) WHERE ACCOUNT_ID = '"+str(RECORD['PARTY_ID'])+"'")
					send_n_receive_acunt = "UPDATE SAQSRA SET ACCOUNT_ID = '{}', ACCOUNT_NAME = '{}', ACCOUNT_RECORD_ID = '{}', ADDRESS_1 = '{}', CITY = '{}', COUNTRY = '{}', COUNTRY_RECORD_ID = '{}', PHONE = '{}', STATE = '{}', STATE_RECORD_ID = '{}', POSTAL_CODE = '{}' WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND RELOCATION_TYPE = '{}'".format(str(account_details.ACCOUNT_ID), str(account_details.ACCOUNT_NAME), str(account_details.ACCOUNT_RECORD_ID), str(account_details.ADDRESS_1), str(account_details.CITY), str(account_details.COUNTRY), str(account_details.COUNTRY_RECORD_ID), str(account_details.PHONE), str(account_details.STATE), str(account_details.STATE_RECORD_ID), str(account_details.POSTAL_CODE), Product.GetGlobal("contract_quote_record_id"), quote_revision_record_id, str(RECORD['PARTY_ROLE']))
					Sql.RunQuery(send_n_receive_acunt)
				# A055S000P01-3324 start 
				if TableName == 'SAQTMT':
					#A055S000P01-4393 start 
					WARRANTY_val =''
					getdate = Sql.GetFirst("""SELECT CONTRACT_VALID_FROM, CONTRACT_VALID_TO FROM SAQTMT WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' """.format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id))
					get_warrent_dates= SqlHelper.GetList("select QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,WARRANTY_END_DATE_ALERT,WARRANTY_START_DATE,WARRANTY_END_DATE from SAQSCO where QUOTE_RECORD_ID = '"+str(Quote.GetGlobal("contract_quote_record_id"))+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' ")
					update_warranty_enddate_alert = ''
					for val in get_warrent_dates:
						
						if val.WARRANTY_END_DATE:
							WARRANTY_val = datetime.strptime(str(val.WARRANTY_END_DATE), "%Y-%m-%d")
							get_con_date = str(getdate.CONTRACT_VALID_FROM).split(" ")[0]
							get_con_date = datetime.strptime(str(get_con_date), "%m/%d/%Y")
							Trace.Write('get_con_date---562--'+str(type(get_con_date)))
							Trace.Write('WARRANTY_val---562--'+str(type(WARRANTY_val)))
							if WARRANTY_val > get_con_date:
								Trace.Write('get_con_date--564---'+str(get_con_date))
								Trace.Write('WARRANTY_END_DATE--564-'+str(val.WARRANTY_END_DATE))
								update_warranty_enddate_alert = "UPDATE SAQSCO SET WARRANTY_END_DATE_ALERT = 1 where QUOTE_RECORD_ID = '"+str(Quote.GetGlobal("contract_quote_record_id"))+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"'  and QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID = '"+str(val.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID)+"'"
							else:
								Trace.Write('WARRANTY_val---568--'+str(val.WARRANTY_END_DATE))
								update_warranty_enddate_alert = "UPDATE SAQSCO SET WARRANTY_END_DATE_ALERT = 0 where QUOTE_RECORD_ID = '"+str(Quote.GetGlobal("contract_quote_record_id"))+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"'  and QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID = '"+str(val.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID)+"'"
								Trace.Write('no end date--')
							Sql.RunQuery(update_warranty_enddate_alert)
						else:
							Trace.Write('WARRANTY_val--600-'+str(val.WARRANTY_END_DATE))
							update_warranty_enddate_alert = "UPDATE SAQSCO SET WARRANTY_END_DATE_ALERT = 0 where QUOTE_RECORD_ID = '"+str(Quote.GetGlobal("contract_quote_record_id"))+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"'  and QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID = '"+str(val.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID)+"'"
							Trace.Write('no end date--')
							Sql.RunQuery(update_warranty_enddate_alert)
					#A055S000P01-4393 end
					getdate = Sql.GetFirst("""SELECT CONTRACT_VALID_FROM, CONTRACT_VALID_TO FROM SAQTRV WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'""".format(Quote.GetGlobal("contract_quote_record_id"), quote_revision_record_id))
					if getdate:
						Log.Info("SYSECTSAVE - SAQSGB")
						billing_query = "UPDATE SAQTBP SET IS_CHANGED = 1, BILLING_START_DATE = '{}', BILLING_END_DATE = '{}'  WHERE QUOTE_RECORD_ID ='{}' AND QTEREV_RECORD_ID = '{}'".format(getdate.CONTRACT_VALID_FROM, getdate.CONTRACT_VALID_TO, Product.GetGlobal('contract_quote_record_id'),quote_revision_record_id)
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
						get_config_ids = Sql.GetFirst("Select * from SAQTSE (nolock) where QUOTE_RECORD_ID ='"+str(quote_record_id)+"'  AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' AND SERVICE_ID = '{}' ".format(service.SERVICE_ID))
						cpsmatchID = get_config_ids.CPS_MATCH_ID
						cpsConfigID = get_config_ids.CPS_CONFIGURATION_ID
						if int(ent_disp_val) > 364:
									
							Trace.Write("---requestdata--244-cpsConfigID0-----"+str(cpsmatchID)+'--'+str(cpsConfigID))
							webclient = System.Net.WebClient()
							webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/json"
							webclient.Headers[System.Net.HttpRequestHeader.Authorization] = "Basic c2ItYzQwYThiMWYtYzU5NS00ZWJjLTkyYzYtYzM4ODg4ODFmMTY0IWIyNTAzfGNwc2VydmljZXMtc2VjdXJlZCFiMzkxOm9zRzgvSC9hOGtkcHVHNzl1L2JVYTJ0V0FiMD0="
							response = webclient.DownloadString("https://cpqprojdevamat.authentication.us10.hana.ondemand.com:443/oauth/token?grant_type=client_credentials")
							response = eval(response)
							webclient = System.Net.WebClient()		
							#Log.Info("---requestdata--252--")
							Request_URL = "https://cpservices-product-configuration.cfapps.us10.hana.ondemand.com/api/v2/configurations/"+str(cpsConfigID)+"/items/1"
							webclient.Headers[System.Net.HttpRequestHeader.Authorization] = "Bearer " + str(response["access_token"])
							#webclient.Headers.Add("If-Match", "111")

							webclient.Headers.Add("If-Match", "1"+str(cpsmatchID))
									
							AttributeID = 'AGS_CON_DAY'
							NewValue = ent_disp_val
							#Trace.Write("---requestdata--252-NewValue-----"+str(NewValue))
							whereReq = "QUOTE_RECORD_ID = '"+str(quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' and SERVICE_ID = '{}'".format(service.SERVICE_ID)
							#Trace.Write('whereReq---'+str(whereReq))
							requestdata = '{"characteristics":[{"id":"'+AttributeID+'","values":[{"value":"'+NewValue+'","selected":true}]}]}'
							#Trace.Write("---eqruestdata---requestdata----"+str(requestdata))
							response2 = webclient.UploadString(Request_URL, "PATCH", str(requestdata))
							#requestdata = {"characteristics":[{"id":"' + AttributeID + '":[{"value":"' +NewValue+'","selected":true}]}]}

							#Log.Info(str(Request_URL)+"---requestdata--166---" + str(response2))


							#Log.Info("patch response1---170---" + str(response2))
							Request_URL = "https://cpservices-product-configuration.cfapps.us10.hana.ondemand.com/api/v2/configurations/"+str(cpsConfigID)
							webclient.Headers[System.Net.HttpRequestHeader.Authorization] = "Bearer " + str(response["access_token"])
							#Log.Info("requestdata---180--265----" + str(requestdata))
							response2 = webclient.DownloadString(Request_URL)
							Trace.Write('response2--182----267-----'+str(response2))
							response2 = str(response2).replace(": true", ': "true"').replace(": false", ': "false"')
							Fullresponse= eval(response2)
							attributesdisallowedlst=[]
							attributeReadonlylst=[]
							attributesallowedlst=[]
							attributedefaultvalue = []
							multi_value = ""
							#overallattributeslist =[]
							attributevalues={}
							for rootattribute, rootvalue in Fullresponse.items():
								if rootattribute=="rootItem":
									for Productattribute, Productvalue in rootvalue.items():
										if Productattribute=="characteristics":
											for prdvalue in Productvalue:
												multi_value = ""
												#overallattributeslist.append(prdvalue['id'])
												if prdvalue['visible'] =='false':
													attributesdisallowedlst.append(prdvalue['id'])
												else:
													#Trace.Write(prdvalue['id']+" set here")
													attributesallowedlst.append(prdvalue['id'])
												if prdvalue['readOnly'] =='true':
													attributeReadonlylst.append(prdvalue['id'])
												#for attribute in prdvalue['values']:
												# attributevalues[str(prdvalue['id'])]=attribute['value']
												# for attribute in prdvalue['values']:
												if len(prdvalue["values"]) == 1:
													#Trace.Write('ifffff'+str(prdvalue["id"]))
													attributevalues[str(prdvalue["id"])] = prdvalue['values'][0]['value']
												elif len(prdvalue["values"]) > 1:
													#Trace.Write('else if'+str(prdvalue["id"]))
													for attribute in prdvalue["values"]:
														#Trace.Write('iiiii---'+str(attribute["value"])+'-'+str(prdvalue["id"]) )
														value_list = [attribute["value"] for attribute in prdvalue["values"]]
														if attribute["author"] in ("Default","System"):
															#Trace.Write('524------'+str(prdvalue["id"]))
															attributedefaultvalue.append(prdvalue["id"])
														#value_list = str(value_list)
													attributevalues[str(prdvalue["id"])] = value_list
												# else:
												#     Trace.Write('else'+str(prdvalue["id"]))

							
							attributesallowedlst = list(set(attributesallowedlst))
							#overallattributeslist = list(set(overallattributeslist))
							HasDefaultvalue=False
							Trace.Write('response2--182----315---'+str(attributesallowedlst))
							Trace.Write('attributevalues--182----315---'+str(attributevalues))
							ProductVersionObj=Sql.GetFirst("Select product_id from product_versions(nolock) where SAPKBId = '"+str(Fullresponse['kbId'])+"' AND SAPKBVersion='"+str(Fullresponse['kbKey']['version'])+"'")
							if ProductVersionObj is not None:
								#tbrow={}
								insertservice = ""
								tblist = []
								#Log.Info('response2--182----321-')
								for attrs in attributesallowedlst:
									Trace.Write('value code---'+str(attrs))
									#tbrow1 = {}
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
									
									PRODUCT_ATTRIBUTES=Sql.GetFirst("SELECT A.ATT_DISPLAY_DESC FROM ATT_DISPLAY_DEFN (NOLOCK) A INNER JOIN PRODUCT_ATTRIBUTES (NOLOCK) P ON A.ATT_DISPLAY=P.ATT_DISPLAY WHERE P.PRODUCT_ID={} AND P.STANDARD_ATTRIBUTE_CODE={}".format(ProductVersionObj.product_id,STANDARD_ATTRIBUTE_VALUES.STANDARD_ATTRIBUTE_CODE))
									
									if PRODUCT_ATTRIBUTES.ATT_DISPLAY_DESC in ('Drop Down','DropDown') and ent_disp_val:
										get_display_val = Sql.GetFirst("SELECT STANDARD_ATTRIBUTE_DISPLAY_VAL  from STANDARD_ATTRIBUTE_VALUES S INNER JOIN ATTRIBUTE_DEFN (NOLOCK) A ON A.STANDARD_ATTRIBUTE_CODE=S.STANDARD_ATTRIBUTE_CODE WHERE S.STANDARD_ATTRIBUTE_CODE = '{}' AND A.SYSTEM_ID = '{}' AND S.STANDARD_ATTRIBUTE_VALUE = '{}' ".format(STANDARD_ATTRIBUTE_VALUES.STANDARD_ATTRIBUTE_CODE,attrs,  attributevalues[attrs] ) )
										ent_disp_val = get_display_val.STANDARD_ATTRIBUTE_DISPLAY_VAL 
									elif PRODUCT_ATTRIBUTES.ATT_DISPLAY_DESC in ('Check Box') and ent_disp_val and ent_val_code:
										Trace.Write('ent_val_code--'+str(type(ent_val_code))+'---'+str(ent_val_code))
										if type(eval(str(ent_val_code))) is list:
											ent_val = str(tuple(ent_val_code)).replace(',)',')')
											get_display_val = Sql.GetList("SELECT STANDARD_ATTRIBUTE_DISPLAY_VAL  from STANDARD_ATTRIBUTE_VALUES S INNER JOIN ATTRIBUTE_DEFN (NOLOCK) A ON A.STANDARD_ATTRIBUTE_CODE=S.STANDARD_ATTRIBUTE_CODE WHERE S.STANDARD_ATTRIBUTE_CODE = '{}' AND A.SYSTEM_ID = '{}' AND S.STANDARD_ATTRIBUTE_VALUE in {} ".format(STANDARD_ATTRIBUTE_VALUES.STANDARD_ATTRIBUTE_CODE,attrs,  ent_val ) )
											ent_disp_val = [i.STANDARD_ATTRIBUTE_DISPLAY_VAL for i in get_display_val ]
											ent_disp_val = str(ent_disp_val).replace("'", '"')
											ent_val_code = str(ent_val_code).replace("'", '"')
										else:
											get_display_val = Sql.GetFirst("SELECT STANDARD_ATTRIBUTE_DISPLAY_VAL  from STANDARD_ATTRIBUTE_VALUES S INNER JOIN ATTRIBUTE_DEFN (NOLOCK) A ON A.STANDARD_ATTRIBUTE_CODE=S.STANDARD_ATTRIBUTE_CODE WHERE S.STANDARD_ATTRIBUTE_CODE = '{}' AND A.SYSTEM_ID = '{}' AND S.STANDARD_ATTRIBUTE_VALUE = '{}' ".format(STANDARD_ATTRIBUTE_VALUES.STANDARD_ATTRIBUTE_CODE,attrs,  attributevalues[attrs] ) )
											ent_disp_val = str(str(get_display_val.STANDARD_ATTRIBUTE_DISPLAY_VAL).split("'") ).replace("'", '"')
											ent_val_code = str(str(ent_val_code).split(',') ).replace("'", '"')

									
									DTypeset={"Drop Down":"DropDown","Free Input, no Matching":"FreeInputNoMatching","Check Box":"Check Box"}
									#Log.Info('response2--182----342-')
									#Trace.Write('value code---'+str(attributevalues[attrs])+'--'+str(attrs))
									insertservice += """<QUOTE_ITEM_ENTITLEMENT>
									<ENTITLEMENT_NAME>{ent_name}</ENTITLEMENT_NAME>
									<ENTITLEMENT_VALUE_CODE>{ent_val_code}</ENTITLEMENT_VALUE_CODE>
									<ENTITLEMENT_TYPE>{ent_type}</ENTITLEMENT_TYPE>									
									<ENTITLEMENT_DISPLAY_VALUE>{ent_disp_val}</ENTITLEMENT_DISPLAY_VALUE>
									<ENTITLEMENT_DESCRIPTION>{ent_desc}</ENTITLEMENT_DESCRIPTION>
									<ENTITLEMENT_COST_IMPACT>{ct}</ENTITLEMENT_COST_IMPACT>
									<ENTITLEMENT_PRICE_IMPACT>{pi}</ENTITLEMENT_PRICE_IMPACT>
									<IS_DEFAULT>{is_default}</IS_DEFAULT>
									<PRICE_METHOD>{pm}</PRICE_METHOD>
									<CALCULATION_FACTOR>{cf}</CALCULATION_FACTOR>
									</QUOTE_ITEM_ENTITLEMENT>""".format(ent_name = str(attrs),ent_val_code = ent_val_code,ent_type = DTypeset[PRODUCT_ATTRIBUTES.ATT_DISPLAY_DESC] if PRODUCT_ATTRIBUTES else  '',ent_desc = ATTRIBUTE_DEFN.STANDARD_ATTRIBUTE_NAME,ent_disp_val = ent_disp_val if HasDefaultvalue==True else '',ct = '',pi = '', is_default = 1 if str(attrs) in attributedefaultvalue else '0',pm = '',cf = '')
									cpsmatc_incr = int(cpsmatchID) + 10
									Trace.Write('cpsmatc_incr'+str(cpsmatc_incr))
								Updatecps = "UPDATE {} SET CPS_MATCH_ID ={},CPS_CONFIGURATION_ID = '{}',ENTITLEMENT_XML='{}',CpqTableEntryModifiedBy = {}, CpqTableEntryDateModified = GETDATE() WHERE {} ".format('SAQTSE', cpsmatc_incr,cpsConfigID,insertservice, User.Id, whereReq)
								Trace.Write('Updatecps'+str(Updatecps))
								Sql.RunQuery(Updatecps)
								

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
		update_tax = "UPDATE SAQITM SET TAX_PERCENTAGE = {TaxPercentage} WHERE SAQITM.QUOTE_ITEM_RECORD_ID = '{ItemRecordId}'".format(
		TaxPercentage=tax_percentage,			
		ItemRecordId=item_obj.QUOTE_ITEM_RECORD_ID
		)
		Sql.RunQuery(update_tax)
		if quote_type == 'tool':
			update_tax_item_covered_obj = "UPDATE SAQICO SET TAX_PERCENTAGE = {TaxPercentage} WHERE SAQICO.SERVICE_ID = '{ServiceId}' and QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID='{revision_rec_id}' ".format(
			TaxPercentage=tax_percentage,			
			ServiceId=TreeParam.split('-')[1].strip(),
			QuoteRecordId=Quote.GetGlobal("contract_quote_record_id"),
			revision_rec_id = quote_revision_record_id
			)
			Sql.RunQuery(update_tax_item_covered_obj)
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
			QueryStatement = """UPDATE A  SET A.EXTENDED_PRICE = B.EXTENDED_PRICE FROM SAQITM A(NOLOCK) JOIN (SELECT SUM(EXTENDED_PRICE) AS EXTENDED_PRICE,QUOTE_RECORD_ID,QTEREV_RECORD_ID,SERVICE_RECORD_ID from SAQICO(NOLOCK) WHERE QUOTE_RECORD_ID ='{QuoteRecordId}' and SERVICE_ID = '{ServiceId}' AND QTEREV_RECORD_ID='{revision_rec_id}' GROUP BY QUOTE_RECORD_ID,SERVICE_RECORD_ID,QTEREV_RECORD_ID) B ON A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.SERVICE_RECORD_ID=B.SERVICE_RECORD_ID AND A.QTEREV_RECORD_ID = B.QTEREV_RECORD_ID """.format(			
			ServiceId=TreeParam.split('-')[1].strip(),
			QuoteRecordId=Quote.GetGlobal("contract_quote_record_id"),
			revision_rec_id = quote_revision_record_id
			)
			Sql.RunQuery(QueryStatement)
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

TableId = Param.TableId
Trace.Write(RECORD)
ObjectName = ""
warning_msg = ""
Trace.Write("TableId-" + str(TableId))
Trace.Write("RECORD" + str(RECORD))
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
	ObjectName = "SAQTBP"
elif TreeParentParam == "Questions" and TopSuperParentParam == "Sections":
	ObjectName = "SYPRQN"
	TableId = "SYOBJR-93188"
elif TreeParentParam == "App Level Permissions":
	ObjectName = "SYPRAP"
	TableId = "SYOBJR-93121"
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



ApiResponse = ApiResponseFactory.JsonResponse(MaterialSave(ObjectName, RECORD, warning_msg, SecRecId))


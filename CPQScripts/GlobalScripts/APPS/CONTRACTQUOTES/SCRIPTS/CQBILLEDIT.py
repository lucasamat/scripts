#   __script_name : CQBILLEDIT.PY
#   __script_description : THIS SCRIPT IS USED TO EDIT A RECORD WHEN THE USER CLICKS ON THE GRID.
#   __primary_author__ : DHURGA
#   __create_date : 17/11/2020
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================

import Webcom.Configurator.Scripting.Test.TestProduct
from SYDATABASE import SQL
import re

#gettotalannualamt = ""
SubTab = getdatestart = getmonthavle = getmonthavl = ""
Sql = SQL()
ContractRecordId = Quote.GetGlobal("contract_quote_record_id")
quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
get_total_qty =0
def remove_list(t):
	return t[3:]

def BILLEDIT_SAVE(GET_DICT,totalyear,getedited_amt,):
	Trace.Write(str(totalyear)+'---BULK EDIT SAVE BILLING MATRIX--inside function---GET_DICT----'+str(GET_DICT))
	for val in GET_DICT:
		value = val.split('-')
		getmonthavl = value[1].replace("/",'-').strip()		
		getamtval = re.findall(r"\d",str(totalyear))
		SubTab = getamtval[0]
		getannual_amt = value[3]
		Trace.Write('gettotalamount-----'+str(type(getannual_amt)))
		#Trace.Write('edited value-----'+str(BT= value[2].replace(",","")))
		getannual_amt = getannual_amt.replace(',','')
		Trace.Write('getannual_amt---32----'+str(getannual_amt))
		gettotalamt_beforeupdate = Sql.GetFirst("SELECT SUM(BILLING_VALUE) as ANNUAL_BILLING_AMOUNT FROM SAQIBP WHERE  QUOTE_RECORD_ID ='{cq}' AND QTEREV_RECORD_ID ='{revision_rec_id}' and EQUIPMENT_ID = '{EID}' and BILLING_DATE NOT IN '{BD}'".format(cq=str(ContractRecordId),EID=value[0], revision_rec_id = quote_revision_record_id ,BD= str(tuple( value[1]))))
		gettotalamt =0
		gettotalamt_update =0
		gettotalamt = gettotalamt_beforeupdate.ANNUAL_BILLING_AMOUNT
		if gettotalamt_beforeupdate:
			gettotalamt_update = float(gettotalamt_beforeupdate.ANNUAL_BILLING_AMOUNT)+float(value[2].replace(",",""))
		Trace.Write('gettotalamt_update---'+str(float(gettotalamt_update)))
		if float(gettotalamt_update) < float(getannual_amt):
			sqlforupdatePT = "UPDATE SAQIBP SET BILLING_VALUE = {BT} where QUOTE_RECORD_ID ='{CT}' AND QTEREV_RECORD_ID ='{revision_rec_id}' and  EQUIPMENT_ID ='{EID}' and BILLING_DATE = '{BD}'".format(BT= value[2].replace(",",""),CT = str(ContractRecordId),EID=value[0],BD = value[1], revision_rec_id = quote_revision_record_id)
			# getmonthvalue = Sql.GetFirst("select * from QT__Billing_Matrix_Header where QUOTE_RECORD_ID ='{CT}' and YEAR  = {BL}".format(BL =int(SubTab),CT = str(ContractRecordId)))
			# if getmonthvalue:
			# 	if getmonthvalue.MONTH_1 == getmonthavl:
			# 		getmonthavle = "MONTH_1"
			# 	elif getmonthvalue.MONTH_2 == getmonthavl:
			# 		getmonthavle = "MONTH_2"
			# 	elif getmonthvalue.MONTH_3 == getmonthavl:
			# 		getmonthavle = "MONTH_3"
			# 	elif getmonthvalue.MONTH_4 == getmonthavl:
			# 		getmonthavle = "MONTH_4"
			# 	elif getmonthvalue.MONTH_5 == getmonthavl:
			# 		getmonthavle = "MONTH_5"
			# 	elif getmonthvalue.MONTH_6 == getmonthavl:
			# 		getmonthavle = "MONTH_6"
			# 	elif getmonthvalue.MONTH_7 == getmonthavl:
			# 		getmonthavle = "MONTH_7"
			# 	elif getmonthvalue.MONTH_8 == getmonthavl:
			# 		getmonthavle = "MONTH_8"
			# 	elif getmonthvalue.MONTH_9 == getmonthavl:
			# 		getmonthavle = "MONTH_9"
			# 	elif getmonthvalue.MONTH_10 == getmonthavl:
			# 		getmonthavle = "MONTH_10"
			# 	elif getmonthvalue.MONTH_11 == getmonthavl:
			# 		getmonthavle = "MONTH_11"
			# 	else:
			# 		getmonthavle = "MONTH_12"
			#sqlforupdate = "UPDATE QT__BM_YEAR_1 SET {gmon} = {BT} where QUOTE_RECORD_ID ='{CT}' AND QTEREV_RECORD_ID ='{revision_rec_id}' and  EQUIPMENT_ID ='{EID}' and BILLING_YEAR = {BL}".format(BL =int(SubTab) ,gmon = getmonthavle,BT= value[2].replace(",",""),CT = str(ContractRecordId),EID=value[0],BD = value[1], revision_rec_id = quote_revision_record_id)
			Sql.RunQuery(sqlforupdatePT)
			#Sql.RunQuery(sqlforupdate)
			
			#to update total amount
			
			end = int(SubTab.split(' ')[-1]) * 12
			start = end - 12 + 1
			billing_date_column = ""
			item_billing_plans_obj = Sql.GetList("""SELECT FORMAT(BILLING_DATE, 'MM-dd-yyyy') as BILLING_DATE,BILLDATE=CONVERT(VARCHAR(11),BILLING_DATE,121) FROM (SELECT ROW_NUMBER() OVER(ORDER BY BILLING_DATE)
												AS ROW, * FROM (SELECT DISTINCT BILLING_DATE
																	FROM SAQIBP (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID ='{}' GROUP BY EQUIPMENT_ID, BILLING_DATE) IQ) OQ WHERE OQ.ROW BETWEEN {} AND {}""".format(
																		ContractRecordId,quote_revision_record_id, start, end))
			if item_billing_plans_obj:
				billing_date_column = [item_billing_plan_obj.BILLDATE for item_billing_plan_obj in item_billing_plans_obj]
				Trace.Write(str(tuple(billing_date_column))+'billing_date_column---'+str(billing_date_column))
			pivot_columns = ",".join(['{}'.format(billing_date) for billing_date in billing_date_column])
			Trace.Write(str(tuple(billing_date_column))+'billing_date_column---'+str(pivot_columns))
			gettotalamt = Sql.GetFirst("SELECT BILLING_VALUE=SUM(BILLING_VALUE) FROM SAQIBP WHERE CONVERT(VARCHAR(11),BILLING_DATE,121) in {pn} and QUOTE_RECORD_ID ='{cq}' AND QTEREV_RECORD_ID ='{revision_rec_id}' and EQUIPMENT_ID = '{EID}'".format(pn=tuple(billing_date_column),cq=str(ContractRecordId),EID=value[0], revision_rec_id = quote_revision_record_id ))
			if gettotalamt:
				gettotalannualamt = gettotalamt.BILLING_VALUE
			Trace.Write('gettotalannualamt---'+str(gettotalannualamt))
			sqlforupdatePTA = "UPDATE SAQIBP SET ANNUAL_BILLING_AMOUNT = {BTN} where QUOTE_RECORD_ID ='{CT}' AND QTEREV_RECORD_ID ='{revision_rec_id}' and  EQUIPMENT_ID ='{EID}' and BILLING_DATE in {BD}".format(BTN= gettotalannualamt,CT = str(ContractRecordId),EID=value[0],BD = tuple(billing_date_column), revision_rec_id = quote_revision_record_id)
			sqlforupdate = "UPDATE QT__BM_YEAR_1 SET ANNUAL_BILLING_AMOUNT = {BTN} where QUOTE_RECORD_ID ='{CT}' AND QTEREV_RECORD_ID ='{revision_rec_id}' and  EQUIPMENT_ID ='{EID}' and BILLING_YEAR = {BL}".format(BL=int(SubTab),BTN= gettotalannualamt,CT = str(ContractRecordId),EID=value[0], revision_rec_id = quote_revision_record_id)
			Sql.RunQuery(sqlforupdatePTA)
			Sql.RunQuery(sqlforupdate)
			savebill =''
			#return 'save',savebill
		else:
			savebill = 'NOTSAVE'
	return 'not saved',savebill

def DELIVERYEDIT_SAVE(deliverydict,totalyear,getedited_amt,deliveryEdit):
	#Trace.Write('98-----deliverydict-'+str(deliverydict))
	delivery_quantity_add =0
	get_delivery_date_list =[]
	get_delivery_qty_list = []
	get_spare_rec_list= []
	savebill = ''
	partrec ={}
	saqspd_total_qty = 0
	saqspt_total_qty =0
	for val in deliverydict:
		spare_rc = val.split('#')[0]
		get_spare_rec_list.append(spare_rc)
		delivery_date = val.split('#')[1]
		delivery_quantity = val.split('#')[2]
		get_delivery_qty_list.append(delivery_quantity)
		#Trace.Write('delivery_quantity--'+str(delivery_quantity))
		get_delivery_date_list.append(delivery_date)
		delivery_quantity_add += float(delivery_quantity)
		get_delivery_recs = str(tuple(get_delivery_date_list)).replace(',)',')')
	join_all_list = zip(get_delivery_qty_list,get_delivery_date_list,get_spare_rec_list)
	Trace.Write('join_all_list---'+str(join_all_list))
	for qty,deldate,sp_rec in join_all_list:
		Trace.Write('124----115----'+str(qty))
		get_totalqty =0
		if sp_rec in partrec.keys():
			partrec[sp_rec] = partrec[sp_rec]+int(qty)
		else:
			partrec[sp_rec] = int(qty)
		get_spare_qty = Sql.GetFirst("SELECT CUSTOMER_ANNUAL_QUANTITY from SAQSPT where QUOTE_RECORD_ID ='{qt_rec_id}' AND QTEREV_RECORD_ID ='{revision_rec_id}' and QUOTE_SERVICE_PART_RECORD_ID='{rev_spare_rec_id}'".format(revision_rec_id = quote_revision_record_id,rev_spare_rec_id=sp_rec,qt_rec_id = str(ContractRecordId)))
		if get_spare_qty:
			saqspt_total_qty = get_spare_qty.CUSTOMER_ANNUAL_QUANTITY
		get_current_details = Sql.GetFirst("SELECT SUM(QUANTITY) as total FROM SAQSPD where QUOTE_RECORD_ID ='{ContractRecordId}' AND QTEREV_RECORD_ID ='{quote_revision_record_id}' and  QTEREVSPT_RECORD_ID ='{rev_spare_rec_id}' and DELIVERY_SCHED_DATE not in {deliverydates}".format(ContractRecordId=ContractRecordId,quote_revision_record_id=quote_revision_record_id,rev_spare_rec_id=sp_rec,deliverydates=str(tuple(get_delivery_date_list)).replace(',)',')')))
		if get_current_details:
			saqspd_total_qty = get_current_details.total
		get_totalqty = partrec[sp_rec]
		Trace.Write('get_totalqty---'+str(get_totalqty))
		get_delivery_total = float(saqspd_total_qty)+float(get_totalqty)
		Trace.Write('get_delivery_total---'+str(get_delivery_total)+'---saqspt_total_qty--'+str(saqspt_total_qty))
		if get_delivery_total <= saqspt_total_qty:
			Trace.Write('124-----')
			Update_delivery_details = "UPDATE SAQSPD SET QUANTITY={qty} where QUOTE_RECORD_ID ='{qt_rec_id}' AND QTEREV_RECORD_ID ='{revision_rec_id}' and  QTEREVSPT_RECORD_ID ='{rev_spare_rec_id}' and DELIVERY_SCHED_DATE = '{del_sch_date}'".format(qty= qty,qt_rec_id = str(ContractRecordId),rev_spare_rec_id=sp_rec,del_sch_date = deldate, revision_rec_id = quote_revision_record_id)
			Update_delivery_details_query = Sql.RunQuery(Update_delivery_details)
			savebill =''
			#return 'save',savebill
		else:
			Trace.Write('118-126-----')
			#Update_delivery_details = "UPDATE SAQSPD SET QUANTITY={qty} where QUOTE_RECORD_ID ='{qt_rec_id}' AND QTEREV_RECORD_ID ='{revision_rec_id}' and  QTEREVSPT_RECORD_ID ='{rev_spare_rec_id}' and DELIVERY_SCHED_DATE = '{del_sch_date}'".format(qty= val.split('#')[2],qt_rec_id = str(ContractRecordId),rev_spare_rec_id=spare_rc,del_sch_date = val.split('#')[1], revision_rec_id = quote_revision_record_id)
			#Update_delivery_details_query = Sql.RunQuery(Update_delivery_details)
			savebill = 'NOTSAVE'
			#return 'not saved',savebill
	return 'save',savebill
try:
	GET_DICT =list(Param.billdict)
	
	#getedited_amt = Param.getedited_amt
except:
	Trace.Write('131---')
	GET_DICT = []
	#totalyear = "" 
	#getedited_amt = ""
try:
	totalyear = Param.totalyear
except:
	totalyear = ""
try:
	getedited_amt = Param.getedited_amt
except:
	getedited_amt = ""
try:
	deliverydict =list(Param.deliverydict)
	#totalyear = Param.totalyear
	#getedited_amt = Param.getedited_amt
	deliveryEdit = Param.deliveryEdit
except:
	deliverydict = []
	#totalyear = "" 
	deliveryEdit = ""
#GET_DICT =list(Param.billdict)
#totalyear = Param.totalyear
#getedited_amt = Param.getedited_amt
#Trace.Write(str(totalyear)+"--GET_DICT--------------"+str(GET_DICT))
if deliveryEdit == "DELIVERYEDIT":
	ApiResponse = ApiResponseFactory.JsonResponse(DELIVERYEDIT_SAVE(deliverydict,totalyear,getedited_amt,deliveryEdit))
else:
	ApiResponse = ApiResponseFactory.JsonResponse(BILLEDIT_SAVE(GET_DICT,totalyear,getedited_amt,))
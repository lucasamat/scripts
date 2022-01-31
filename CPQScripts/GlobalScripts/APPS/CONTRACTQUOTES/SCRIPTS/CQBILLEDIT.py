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
		Trace.Write('gettotalamount-----'+str(getannual_amt))
		
		if float(getannual_amt.replace(',','')) > float(getedited_amt):
			sqlforupdatePT = "UPDATE SAQIBP SET BILLING_VALUE = {BT} where QUOTE_RECORD_ID ='{CT}' AND QTEREV_RECORD_ID ='{revision_rec_id}' and  EQUIPMENT_ID ='{EID}' and BILLING_DATE = '{BD}'".format(BT= value[2].replace(",",""),CT = str(ContractRecordId),EID=value[0],BD = value[1], revision_rec_id = quote_revision_record_id)
			getmonthvalue = Sql.GetFirst("select * from QT__Billing_Matrix_Header where QUOTE_RECORD_ID ='{CT}' and YEAR  = {BL}".format(BL =int(SubTab),CT = str(ContractRecordId)))
			if getmonthvalue:
				if getmonthvalue.MONTH_1 == getmonthavl:
					getmonthavle = "MONTH_1"
				elif getmonthvalue.MONTH_2 == getmonthavl:
					getmonthavle = "MONTH_2"
				elif getmonthvalue.MONTH_3 == getmonthavl:
					getmonthavle = "MONTH_3"
				elif getmonthvalue.MONTH_4 == getmonthavl:
					getmonthavle = "MONTH_4"
				elif getmonthvalue.MONTH_5 == getmonthavl:
					getmonthavle = "MONTH_5"
				elif getmonthvalue.MONTH_6 == getmonthavl:
					getmonthavle = "MONTH_6"
				elif getmonthvalue.MONTH_7 == getmonthavl:
					getmonthavle = "MONTH_7"
				elif getmonthvalue.MONTH_8 == getmonthavl:
					getmonthavle = "MONTH_8"
				elif getmonthvalue.MONTH_9 == getmonthavl:
					getmonthavle = "MONTH_9"
				elif getmonthvalue.MONTH_10 == getmonthavl:
					getmonthavle = "MONTH_10"
				elif getmonthvalue.MONTH_11 == getmonthavl:
					getmonthavle = "MONTH_11"
				else:
					getmonthavle = "MONTH_12"
			sqlforupdate = "UPDATE QT__BM_YEAR_1 SET {gmon} = {BT} where QUOTE_RECORD_ID ='{CT}' AND QTEREV_RECORD_ID ='{revision_rec_id}' and  EQUIPMENT_ID ='{EID}' and BILLING_YEAR = {BL}".format(BL =int(SubTab) ,gmon = getmonthavle,BT= value[2].replace(",",""),CT = str(ContractRecordId),EID=value[0],BD = value[1], revision_rec_id = quote_revision_record_id)
			Sql.RunQuery(sqlforupdatePT)
			Sql.RunQuery(sqlforupdate)
			
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
			return 'save',savebill
		else:
			savebill = 'NOTSAVE'
			return 'not saved',savebill

def DELIVERYEDIT_SAVE(deliverydict,totalyear,getedited_amt,deliveryEdit):
	Trace.Write('98-----deliverydict-'+str(deliverydict))
	get_delivery_list =[]
	saqspd_total_qty = 0
	saqspt_total_qty =0
	for val in deliverydict:
		spare_rc = val.split('#')[0]
		delivery_date = val.split('#')[1]
		delivery_quantity = val.split('#')[2]
		get_delivery_list.append(delivery_date)
		 
		get_delivery_recs = str(tuple(get_delivery_list)).replace(',)',')')
		#SubTab = getamtval[0]
		#getannual_amt = value[3]
		Trace.Write('---delivery_date--'+str(delivery_date)+'--spare_rc---'+str(spare_rc))
		Trace.Write('---get_delivery_recs--'+str(get_delivery_recs))
		get_current_details = Sql.GetFirst("SELECT SUM(QUANTITY) as total FROM SAQSPD where QUOTE_RECORD_ID ='{ContractRecordId}' AND QTEREV_RECORD_ID ='{quote_revision_record_id}' and  QTEREVSPT_RECORD_ID ='{rev_spare_rec_id}' and DELIVERY_SCHED_DATE not in {deliverydates}".format(ContractRecordId=ContractRecordId,quote_revision_record_id=quote_revision_record_id,rev_spare_rec_id=spare_rc,deliverydates=get_delivery_recs))
		if get_current_details:
			saqspd_total_qty = get_current_details.total
		get_spare_qty = Sql.GetFirst("SELECT CUSTOMER_ANNUAL_QUANTITY from SAQSPT where QUOTE_RECORD_ID ='{qt_rec_id}' AND QTEREV_RECORD_ID ='{revision_rec_id}' and QUOTE_SERVICE_PART_RECORD_ID='{rev_spare_rec_id}'".format(revision_rec_id = quote_revision_record_id,rev_spare_rec_id=spare_rc,qt_rec_id = str(ContractRecordId)))
		if get_spare_qty:
			saqspt_total_qty = get_spare_qty.CUSTOMER_ANNUAL_QUANTITY
		Trace.Write('---saqspd_total_qty--'+str(type(saqspd_total_qty)))
		Trace.Write('---saqspt_total_qty--'+str(saqspt_total_qty))
		if saqspt_total_qty:
			if int(saqspd_total_qty) > int(saqspt_total_qty):
				Trace.Write('---saqspd_total_qty--'+str(type(saqspd_total_qty)))
				Update_delivery_details = "UPDATE SAQSPD SET QUANTITY={qty} where QUOTE_RECORD_ID ='{qt_rec_id}' AND QTEREV_RECORD_ID ='{revision_rec_id}' and  QTEREVSPT_RECORD_ID ='{rev_spare_rec_id}' and DELIVERY_SCHED_DATE = '{del_sch_date}'".format(qty= val.split('#')[2],qt_rec_id = str(ContractRecordId),rev_spare_rec_id=spare_rc,del_sch_date = val.split('#')[1], revision_rec_id = quote_revision_record_id)
				Update_delivery_details_query = Sql.RunQuery(Update_delivery_details)
				savebill =''
				return 'save',savebill
		else:
			savebill = 'NOTSAVE'
			return 'not saved',savebill
	#return 'save','savebill'
try:
	GET_DICT =list(Param.billdict)
	
	getedited_amt = Param.getedited_amt
except:
	Trace.Write('131---')
	GET_DICT = []
	#totalyear = "" 
	getedited_amt = ""
try:
	totalyear = Param.totalyear
except:
	totalyear = ""
try:
	deliverydict =list(Param.deliverydict)
	#totalyear = Param.totalyear
	getedited_amt = Param.getedited_amt
	deliveryEdit = Param.deliveryEdit
except:
	deliverydict = []
	#totalyear = "" 
	getedited_amt = deliveryEdit = ""
#GET_DICT =list(Param.billdict)
#totalyear = Param.totalyear
#getedited_amt = Param.getedited_amt
#Trace.Write(str(totalyear)+"--GET_DICT--------------"+str(GET_DICT))
if deliveryEdit == "DELIVERYEDIT":
	ApiResponse = ApiResponseFactory.JsonResponse(DELIVERYEDIT_SAVE(deliverydict,totalyear,getedited_amt,deliveryEdit))
else:
	ApiResponse = ApiResponseFactory.JsonResponse(BILLEDIT_SAVE(GET_DICT,totalyear,getedited_amt,))
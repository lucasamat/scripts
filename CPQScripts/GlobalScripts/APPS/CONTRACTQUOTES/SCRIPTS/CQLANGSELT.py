



import clr
#clr.AddReference("System.Net")
clr.AddReference("IronPython")
clr.AddReference("Microsoft.Scripting")
from System.Net import WebRequest
from System.Net import HttpWebResponse
from Microsoft.Scripting import SourceCodeKind
from IronPython.Hosting import Python
from IronPython import Compiler
import Webcom.Configurator.Scripting.Test.TestProduct

from SYDATABASE import SQL
import datetime
Sql = SQL()
import SYCNGEGUID as CPQID

UserId = str(User.Id)
UserName = str(User.UserName)
INCLUDESPARE =add_style =  ""

#quoteid = Product.GetGlobal("contract_quote_record_id")
contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
#get_spare=Sql.GetFirst("select * from QTQIFP where QUOTE_RECORD_ID='"+str(quoteid)+"'")
gettoolquote=Sql.GetFirst("select QUOTE_TYPE,QUOTE_ID from SAQTMT where MASTER_TABLE_QUOTE_RECORD_ID='"+str(contract_quote_record_id)+"'")
#if get_spare and gettoolquote.QUOTE_TYPE =="ZTBC - TOOL BASED":
	#INCLUDESPARE = 'INCLUDESPARES'
	#add_style = "display:block"
#else:
	#Trace.Write('succes--NO--')
	#INCLUDESPARE = ''
	#add_style = "display:none"

#Document XML

#A055S000P01-10549- start
update_rev_expire_date  = "UPDATE SAQTRV SET REV_EXPIRE_DATE = CONVERT(date,DATEADD(DAY, 90, GETDATE())) where QUOTE_RECORD_ID ='{quote_record_id}'".format(quote_record_id=contract_quote_record_id)
Sql.RunQuery(update_rev_expire_date)

def _insert_item_level_delivery_schedule():
	insert_item_level_delivery_schedule = "INSERT SAQIPD (QUOTE_REV_ITEM_PART_DELIVERY_RECORD_ID,DELIVERY_SCHED_CAT,DELIVERY_SCHED_DATE,LINE,PART_DESCRIPTION,PART_NUMBER,PART_RECORD_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,QUANTITY,QUOTE_ID,QTEITMPRT_RECORD_ID,QTEITM_RECORD_ID,QUOTE_RECORD_ID,QTEREV_ID,QTEREVSPT_RECORD_ID,QTEREV_RECORD_ID) select QUOTE_REV_ITEM_PART_DELIVERY_RECORD_ID,DELIVERY_SCHED_CAT,DELIVERY_SCHED_DATE,LINE,PART_DESCRIPTION,PART_NUMBER,PART_RECORD_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,QUANTITY,QUOTE_ID,QTEITMPRT_RECORD_ID,QTEITM_RECORD_ID,QUOTE_RECORD_ID,QTEREV_ID,QTEREVSPT_RECORD_ID,QTEREV_RECORD_ID FROM SAQIPD where QUOTE_RECORD_ID = '{QuoteRecordId}' and QTEREV_RECORD_ID= '{rev_rec_id}'".format(QuoteRecordId=contract_quote_record_id,rev_rec_id=quote_revision_record_id)
	Log.Info('insert_item_level_delivery_schedule==='+str(insert_item_level_delivery_schedule))
	Sql.RunQuery(insert_item_level_delivery_schedule)

#quote table insert for billing matrix
def insert_quote_billing_plan():
	services_obj = Sql.GetList("SELECT SERVICE_ID FROM SAQTSV (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' ".format(contract_quote_record_id,quote_revision_record_id))
	item_billing_plan_obj = Sql.GetFirst("SELECT count(CpqTableEntryId) as cnt FROM SAQIBP (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'GROUP BY EQUIPMENT_ID,SERVICE_ID".format(contract_quote_record_id,quote_revision_record_id))
	if item_billing_plan_obj is not None and services_obj:
		quotient, remainder = divmod(item_billing_plan_obj.cnt, 12)
		years = quotient + (1 if remainder > 0 else 0)
		if not years:
			years = 1
		for index in range(1, years+1):
			YearCount = "Year {}".format(index)
			no_of_year = index
			#YearCount1 = index
			if YearCount:
				end = int(YearCount.split(' ')[-1]) * 12
				start = end - 12 + 1
				item_billing_plans_obj = Sql.GetList("""SELECT FORMAT(BILLING_DATE, 'MM-dd-yyyy') as BILLING_DATE FROM (SELECT ROW_NUMBER() OVER(ORDER BY BILLING_DATE)
															AS ROW, * FROM (SELECT DISTINCT BILLING_DATE
															FROM SAQIBP (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' 
															AND QTEREV_RECORD_ID = '{}' GROUP BY EQUIPMENT_ID, BILLING_DATE) IQ) OQ WHERE OQ.ROW BETWEEN {} AND {}""".format(
															contract_quote_record_id,quote_revision_record_id, start, end))
				if item_billing_plans_obj:
					billing_date_column = [item_billing_plan_obj.BILLING_DATE for item_billing_plan_obj in item_billing_plans_obj]
					date_columns = " ,".join(['MONTH_{}'.format(index) for index in range(1, len(billing_date_column)+1)])
					header_select_date_columns = ",".join(["'{}' AS MONTH_{}".format(date_column, index) for index, date_column in enumerate(billing_date_column, 1)])
					select_date_columns = ",".join(['[{}] AS MONTH_{}'.format(date_column, index) for index, date_column in enumerate(billing_date_column, 1)])
					sum_select_date_columns = ",".join(['SUM([{}]) AS MONTH_{}'.format(date_column, index) for index, date_column in enumerate(billing_date_column, 1)])
					Sql.RunQuery("""INSERT QT__Billing_Matrix_Header (
										QUOTE_ID,QUOTE_RECORD_ID,{DateColumn},YEAR,ownerId
									)
									SELECT TOP 1
										QUOTE_ID,										
										QUOTE_RECORD_ID,
										{SelectDateColoumn},
										{Year} as YEAR,
										{UserId} as ownerId
									FROM SAQIBP (NOLOCK)
									WHERE QUOTE_RECORD_ID='{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'""".format(
										QuoteRecordId=contract_quote_record_id,RevisionRecordId=quote_revision_record_id,DateColumn=date_columns,Year=no_of_year,SelectDateColoumn=header_select_date_columns, UserId=User.Id
										))
					pivot_columns = ",".join(['[{}]'.format(billing_date) for billing_date in billing_date_column])
					
					for service_obj in services_obj:
						Qustr = "WHERE QUOTE_RECORD_ID='{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID = '{}' AND BILLING_DATE BETWEEN '{}' AND '{}'".format(contract_quote_record_id,quote_revision_record_id,
																						service_obj.SERVICE_ID, billing_date_column[0], billing_date_column[-1])				
						
						Sql.RunQuery("""INSERT QT__BM_YEAR_1 (
										ANNUAL_BILLING_AMOUNT,BILLING_START_DATE,BILLING_END_DATE,
										BILLING_TYPE,BILLING_YEAR,EQUIPMENT_DESCRIPTION,EQUIPMENT_ID,
										GREENBOOK,GREENBOOK_RECORD_ID,ITEM_LINE_ID,
										QUOTE_ID,QUOTE_RECORD_ID,QTEITMCOB_RECORD_ID,
										QTEITM_RECORD_ID,SERIAL_NUMBER,SERVICE_DESCRIPTION,
										SERVICE_ID,SERVICE_RECORD_ID,YEAR,EQUIPMENT_QUANTITY,
										{DateColumn},ownerId
									)
									SELECT  ANNUAL_BILLING_AMOUNT,BILLING_START_DATE,
												BILLING_END_DATE,BILLING_TYPE,{BillingYear} as BILLING_YEAR,
												EQUIPMENT_DESCRIPTION,EQUIPMENT_ID,GREENBOOK,GREENBOOK_RECORD_ID,
												ITEM_LINE_ID,QUOTE_ID,QUOTE_RECORD_ID,QTEITMCOB_RECORD_ID,
												QTEITM_RECORD_ID,SERIAL_NUMBER,
												SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,
												YEAR,EQUIPMENT_QUANTITY,{SelectDateColoumn},{UserId} as ownerId
										FROM (
											SELECT 
												ANNUAL_BILLING_AMOUNT,BILLING_VALUE,BILLING_DATE,BILLING_START_DATE,
												BILLING_END_DATE,BILLING_TYPE,{BillingYear} as BILLING_YEAR,
												EQUIPMENT_DESCRIPTION,EQUIPMENT_ID,GREENBOOK,GREENBOOK_RECORD_ID,
												LINE as ITEM_LINE_ID,QUOTE_ID,QUOTE_RECORD_ID,QTEITMCOB_RECORD_ID,
												QTEITM_RECORD_ID,SERIAL_NUMBER,
												SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,{BillingYear} as YEAR,EQUIPMENT_QUANTITY
											FROM SAQIBP 
											{WhereString}
										) AS IQ
										PIVOT
										(
											SUM(BILLING_VALUE)
											FOR BILLING_DATE IN ({PivotColumns})
										)AS PVT ORDER BY GREENBOOK,SERVICE_ID
									""".format(BillingYear=no_of_year,WhereString=Qustr, PivotColumns=pivot_columns, 
											DateColumn=date_columns, SelectDateColoumn=select_date_columns,UserId=User.Id,)								
									)
							
						# Total based on service - start
						'''Sql.RunQuery("""INSERT QT__BM_YEAR_1 (
										ANNUAL_BILLING_AMOUNT,BILLING_YEAR,
										QUOTE_ID,QUOTE_RECORD_ID,SERVICE_DESCRIPTION,
										SERVICE_ID,SERVICE_RECORD_ID,YEAR,EQUIPMENT_QUANTITY,
										{DateColumn},ownerId
									)
									SELECT SUM(CONVERT(BIGINT, ANNUAL_BILLING_AMOUNT)) AS ANNUAL_BILLING_AMOUNT,{BillingYear} as BILLING_YEAR,QUOTE_ID,QUOTE_RECORD_ID,
												SERVICE_DESCRIPTION,CONCAT(SERVICE_ID, ' TOTAL') as SERVICE_ID,SERVICE_RECORD_ID,
												YEAR,SUM(EQUIPMENT_QUANTITY) AS EQUIPMENT_QUANTITY,{SumSelectDateColoumn},{UserId} as ownerId
										FROM (
											SELECT 
												ANNUAL_BILLING_AMOUNT,BILLING_AMOUNT,BILLING_DATE,{BillingYear} as BILLING_YEAR,													
												QUOTE_ID,QUOTE_RECORD_ID,													SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,
												{BillingYear} as YEAR, EQUIPMENT_QUANTITY
											FROM SAQIBP 
											{WhereString}
										) AS IQ
										PIVOT
										(
											SUM(BILLING_AMOUNT)
											FOR BILLING_DATE IN ({PivotColumns})
										)AS PVT GROUP BY QUOTE_ID,QUOTE_NAME,QUOTE_RECORD_ID,
												SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,YEAR, EQUIPMENT_QUANTITY
									""".format(BillingYear=no_of_year,WhereString=Qustr, PivotColumns=pivot_columns, 
											DateColumn=date_columns, SumSelectDateColoumn=sum_select_date_columns, UserId=User.Id,)								
									)'''
						# Total based on service - end
	return True
#A055S000P01-10549-end
def _insert_subtotal_by_offerring_quote_table():
	
	c4c_quote_id = gettoolquote.QUOTE_ID
	cartobj = Sql.GetFirst("select CART_ID, USERID from CART where ExternalId = '{}'".format(c4c_quote_id))
	try:
		delete_offerings = "DELETE FROM QT__QT_SAQRIS where cartId = {CartId} AND QUOTE_RECORD_ID ='{c4c_quote_id}' and  QTEREV_RECORD_ID= '{rev_rec_id}'".format(CartId = cartobj.CART_ID,UserId= cartobj.USERID,c4c_quote_id = contract_quote_record_id,rev_rec_id = quote_revision_record_id)
		Sql.RunQuery(delete_offerings)
		delete_items = "DELETE FROM QT__QT_SAQRIT where cartId = {CartId} AND QUOTE_RECORD_ID ='{c4c_quote_id}' and  QTEREV_RECORD_ID= '{rev_rec_id}'".format(CartId = cartobj.CART_ID,c4c_quote_id = contract_quote_record_id,rev_rec_id = quote_revision_record_id)
		Sql.RunQuery(delete_offerings)
		Sql.RunQuery(delete_items)
	except:
		Trace.Write("NO REC FOUND ")


	Quoteofferings = Quote.QuoteTables["QT_SAQRIS"]

	getoffer_details_obj = Sql.GetList("select SAQRIS.COMMITTED_VALUE,SAQRIS.CONTRACT_VALID_FROM,SAQRIS.CONTRACT_VALID_TO,SAQRIS.DIVISION_ID,SAQRIS.DIVISION_RECORD_ID,SAQRIS.DOC_CURRENCY,SAQRIS.DOCCURR_RECORD_ID,SAQRIS.ESTIMATED_VALUE,SAQRIS.GLOBAL_CURRENCY,SAQRIS.GLOBAL_CURRENCY_RECORD_ID,SAQRIS.LINE,SAQRIS.NET_PRICE,SAQRIS.NET_PRICE_INGL_CURR,SAQRIS.NET_VALUE,SAQRIS.NET_VALUE_INGL_CURR,SAQRIS.PLANT_ID,SAQRIS.PLANT_RECORD_ID,SAQRIS.SERVICE_DESCRIPTION,SAQRIS.SERVICE_ID,SAQRIS.SERVICE_RECORD_ID,SAQRIS.QUANTITY,SAQRIS.QUOTE_ID,SAQRIS.QUOTE_RECORD_ID,SAQRIS.QTEREV_ID,SAQRIS.QTEREV_RECORD_ID,SAQRIS.TAX_PERCENTAGE,SAQRIS.TAX_AMOUNT,SAQRIS.TAX_AMOUNT_INGL_CURR,SAQRIS.UNIT_PRICE,SAQRIS.UNIT_PRICE_INGL_CURR,{UserId} as ownerId,{CartId} as cartId from SAQRIS (NOLOCK)  where SAQRIS.QUOTE_RECORD_ID ='{c4c_quote_id}' and  SAQRIS.QTEREV_RECORD_ID= '{rev_rec_id}'".format(CartId = cartobj.CART_ID,UserId= cartobj.USERID,c4c_quote_id = contract_quote_record_id,rev_rec_id = quote_revision_record_id))

	quote_subtotalofferings = Quote.QuoteTables["QT_SAQRIS"]
	quote_subtotalofferings.Rows.Clear()
	if getoffer_details_obj:
		for val in getoffer_details_obj:
			newRow = Quoteofferings.AddNewRow()
			if val.COMMITTED_VALUE:
				newRow['COMMITTED_VALUE'] = val.COMMITTED_VALUE
			else:
				newRow['COMMITTED_VALUE'] =0
			newRow['CONTRACT_VALID_FROM'] = val.CONTRACT_VALID_FROM
			newRow['CONTRACT_VALID_TO'] = val.CONTRACT_VALID_TO
			newRow['DIVISION_ID'] = val.DIVISION_ID
			newRow['DIVISION_RECORD_ID'] = val.DIVISION_RECORD_ID
			newRow['DOC_CURRENCY'] =  val.DOC_CURRENCY
			newRow['DOCCURR_RECORD_ID'] = val.DOCCURR_RECORD_ID
			if val.ESTIMATED_VALUE:
				newRow['ESTIMATED_VALUE'] = val.ESTIMATED_VALUE
			else:
				newRow['ESTIMATED_VALUE'] = 0
			newRow['GLOBAL_CURRENCY'] = val.GLOBAL_CURRENCY
			newRow['GLOBAL_CURRENCY_RECORD_ID'] = val.GLOBAL_CURRENCY_RECORD_ID
			newRow['LINE'] = val.LINE
			if val.NET_PRICE:
				newRow['NET_PRICE'] = val.NET_PRICE
			else:
				newRow['NET_PRICE'] = 0
			if val.NET_PRICE_INGL_CURR:
				newRow['NET_PRICE_INGL_CURR'] = val.NET_PRICE_INGL_CURR
			else:
				newRow['NET_PRICE_INGL_CURR'] = 0
			newRow['SERVICE_ID'] = val.SERVICE_ID
			if val.NET_VALUE:
				newRow['NET_VALUE'] = val.NET_VALUE
			else:
				newRow['NET_VALUE'] = 0
			newRow['SERVICE_RECORD_ID'] = val.SERVICE_RECORD_ID
			newRow['SERVICE_DESCRIPTION'] = val.SERVICE_DESCRIPTION
			newRow['QUANTITY'] = val.QUANTITY
			newRow['QUOTE_RECORD_ID'] = val.QUOTE_RECORD_ID
			newRow['QUOTE_ID'] = val.QUOTE_ID
			newRow['QTEREV_ID'] = val.QTEREV_ID
			newRow['QTEREV_RECORD_ID'] = val.QTEREV_RECORD_ID
			if val.TAX_PERCENTAGE:
				newRow['TAX_PERCENTAGE'] = val.TAX_PERCENTAGE
			else:
				newRow['TAX_PERCENTAGE'] = 0
			newRow['TAX_AMOUNT'] = val.TAX_AMOUNT
			if val.UNIT_PRICE:
				newRow['UNIT_PRICE'] = val.UNIT_PRICE
			else:
				newRow['UNIT_PRICE'] = 0
			if val.UNIT_PRICE_INGL_CURR:
				newRow['UNIT_PRICE_INGL_CURR'] = val.UNIT_PRICE_INGL_CURR
			else:
				newRow['UNIT_PRICE_INGL_CURR'] = 0


		Quoteofferings.Save()
	#insrt_subtotal_offering = ("""INSERT QT__QT_SAQRIS (COMMITTED_VALUE,CONTRACT_VALID_FROM,CONTRACT_VALID_TO,DIVISION_ID,DIVISION_RECORD_ID,DOC_CURRENCY,DOCCURR_RECORD_ID,ESTIMATED_VALUE,GLOBAL_CURRENCY,GLOBAL_CURRENCY_RECORD_ID,LINE,NET_PRICE,NET_PRICE_INGL_CURR,NET_VALUE,NET_VALUE_INGL_CURR,PLANT_ID,PLANT_RECORD_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,QUANTITY,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,TAX_PERCENTAGE,TAX_AMOUNT,TAX_AMOUNT_INGL_CURR,UNIT_PRICE,UNIT_PRICE_INGL_CURR,ownerId, cartId) select SAQRIS.COMMITTED_VALUE,SAQRIS.CONTRACT_VALID_FROM,SAQRIS.CONTRACT_VALID_TO,SAQRIS.DIVISION_ID,SAQRIS.DIVISION_RECORD_ID,SAQRIS.DOC_CURRENCY,SAQRIS.DOCCURR_RECORD_ID,SAQRIS.ESTIMATED_VALUE,SAQRIS.GLOBAL_CURRENCY,SAQRIS.GLOBAL_CURRENCY_RECORD_ID,SAQRIS.LINE,SAQRIS.NET_PRICE,SAQRIS.NET_PRICE_INGL_CURR,SAQRIS.NET_VALUE,SAQRIS.NET_VALUE_INGL_CURR,SAQRIS.PLANT_ID,SAQRIS.PLANT_RECORD_ID,SAQRIS.SERVICE_DESCRIPTION,SAQRIS.SERVICE_ID,SAQRIS.SERVICE_RECORD_ID,SAQRIS.QUANTITY,SAQRIS.QUOTE_ID,SAQRIS.QUOTE_RECORD_ID,SAQRIS.QTEREV_ID,SAQRIS.QTEREV_RECORD_ID,SAQRIS.TAX_PERCENTAGE,SAQRIS.TAX_AMOUNT,SAQRIS.TAX_AMOUNT_INGL_CURR,SAQRIS.UNIT_PRICE,SAQRIS.UNIT_PRICE_INGL_CURR,{UserId} as ownerId,{CartId} as cartId from SAQRIS (NOLOCK)  where SAQRIS.QUOTE_RECORD_ID ='{c4c_quote_id}' and  SAQRIS.QTEREV_RECORD_ID= '{rev_rec_id}'""".format(CartId = cartobj.CART_ID,UserId= cartobj.USERID,c4c_quote_id = contract_quote_record_id,rev_rec_id = quote_revision_record_id))
	#Sql.RunQuery(insrt_subtotal_offering)


	insrt_item_details = ("""INSERT QT__QT_SAQRIT (LINE,SERVICE_DESCRIPTION,SERVICE_RECORD_ID,SERVICE_ID,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,ownerId, cartId) select SAQRIT.LINE,SAQRIT.SERVICE_DESCRIPTION,SAQRIT.SERVICE_RECORD_ID,SAQRIT.SERVICE_ID,SAQRIT.QUOTE_ID,SAQRIT.QUOTE_RECORD_ID,SAQRIT.QTEREV_ID,SAQRIT.QTEREV_RECORD_ID,{UserId} as ownerId,{CartId} as cartId from SAQRIT (NOLOCK)  where SAQRIT.QUOTE_RECORD_ID ='{c4c_quote_id}' and  SAQRIT.QTEREV_RECORD_ID= '{rev_rec_id}'""".format(CartId = cartobj.CART_ID,UserId= cartobj.USERID,c4c_quote_id = contract_quote_record_id,rev_rec_id = quote_revision_record_id))
	Sql.RunQuery(insrt_item_details)

	get_revision_details = Sql.GetFirst("SELECT REVISION_DESCRIPTION,REV_EXPIRE_DATE,EXCHANGE_RATE,CONTRACT_VALID_FROM,CONTRACT_VALID_TO,CUSTOMER_NOTES,PAYMENTTERM_NAME from SAQTRV where QUOTE_RECORD_ID = '{qt_rec_id}'".format(qt_rec_id = contract_quote_record_id))
	if get_revision_details:
		Quote.SetGlobal('REV_DESC', str(get_revision_details.REVISION_DESCRIPTION)) 
		Quote.SetGlobal('REV_EXPIRE', str(get_revision_details.REV_EXPIRE_DATE).split()[0])
		Quote.SetGlobal('EXC_RATE', str(get_revision_details.EXCHANGE_RATE))
		Quote.SetGlobal('QT_CVF', str(get_revision_details.CONTRACT_VALID_FROM).split()[0])
		Quote.SetGlobal('QT_CVT', str(get_revision_details.CONTRACT_VALID_TO).split()[0])
		if str(get_revision_details.CUSTOMER_NOTES):
			Quote.SetGlobal('QT_CN', str(get_revision_details.CUSTOMER_NOTES))
			Quote.GetCustomField('customer_notes').Content = str(get_revision_details.CUSTOMER_NOTES)
		if str(get_revision_details.PAYMENTTERM_NAME):
			Quote.SetGlobal('QT_PAYMENT_TERM', str(get_revision_details.PAYMENTTERM_NAME))
	#set  total net price, total net value start
	total_net_price = total_net_value = total_tax_amt = 0.00
	
	
	quote_subtotalofferings = Quote.QuoteTables["QT_SAQRIS"]

	'''for i in quote_subtotalofferings.Rows:
		Trace.Write('QT_SAQRIS---'+str(i['NET_PRICE']))
		#exts_price += float(i['EXTENDED_PRICE'])
		total_net_price += float(i['NET_PRICE'])
		total_net_value += float(i['NET_VALUE'])
		total_tax_amt += float(i['TAX_AMOUNT'])
		Trace.Write('QT_SAQRIS---total_net_price----'+str(total_net_price))
		Trace.Write('QT_SAQRIS---total_net_value----'+str(total_net_value))
		Quote.SetGlobal('NP', str(total_net_price))
		Quote.SetGlobal('NEV', str(total_net_value))
		Quote.SetGlobal('TX', str(total_tax_amt))'''
	get_quotetotal = Sql.GetFirst("SELECT SUM(NET_PRICE_INGL_CURR) as netprice,SUM(ESTIMATED_VALUE) as est_val from QT__QT_SAQRIS where QUOTE_RECORD_ID = '{contract_quote_record_id}' and QTEREV_RECORD_ID ='{quote_revision_record_id}' ".format(contract_quote_record_id=contract_quote_record_id,quote_revision_record_id=quote_revision_record_id))
	if get_quotetotal:
		Quote.GetCustomField('doc_net_price').Content = str(get_quotetotal.netprice)
		Quote.GetCustomField('tot_est').Content = str(get_quotetotal.est_val)

	return True
#Document XML end


#generate documnet start

get_quote_details = Sql.GetFirst("SELECT QUOTE_ID,QTEREV_ID,QUOTE_NAME,C4C_QUOTE_ID, QUOTE_TYPE FROM SAQTMT(NOLOCK) WHERE MASTER_TABLE_QUOTE_RECORD_ID =  '"+str(contract_quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id) + "'")
def insert_spare_doc(parts_list):
	if Quote.GetCustomField('INCLUDE_ITEMS').Content == 'YES' and Quote.GetCustomField('Billing_Matrix').Content == 'YES':
		Trace.Write('285----')
		_insert_subtotal_by_offerring_quote_table()
		insert_quote_billing_plan()
	elif Quote.GetCustomField('ITEM_DELIVERY_SCHEDULE').Content == 'YES':
		_insert_item_level_delivery_schedule()
	elif Quote.GetCustomField('Billing_Matrix').Content == 'YES':
		Trace.Write('285----')
		insert_quote_billing_plan()
	if str(parts_list) == 'True':
		Trace.Write('93------')
		Log.Info('SAQDOC---documents-')
		saqdoc_output_insert="""INSERT SAQDOC (
							QUOTE_DOCUMENT_RECORD_ID,
							DOCUMENT_ID,
							DOCUMENT_NAME,
							DOCUMENT_PATH,
							QUOTE_ID,
							QUOTE_NAME,
							QUOTE_RECORD_ID,
							LANGUAGE_ID,
							LANGUAGE_NAME,
							LANGUAGE_RECORD_ID,
							CPQTABLEENTRYADDEDBY,
							CPQTABLEENTRYDATEADDED,
							CpqTableEntryModifiedBy,
							CpqTableEntryDateModified,
							STATUS,
							QTEREV_ID,
							QTEREV_RECORD_ID
							)SELECT
							CONVERT(VARCHAR(4000),NEWID()) as QUOTE_DOCUMENT_RECORD_ID,
							'{doc_id}' AS DOCUMENT_ID,
							'{doc_name}' AS DOCUMENT_NAME,
							'' AS DOCUMENT_PATH,
							'{quoteid}' AS QUOTE_ID,
							'{quotename}' AS QUOTE_NAME,
							'{quoterecid}' AS QUOTE_RECORD_ID,
							'EN' AS LANGUAGE_ID,
							'English' AS LANGUAGE_NAME,
							MALANG.LANGUAGE_RECORD_ID AS LANGUAGE_RECORD_ID,
							'{UserName}' as CPQTABLEENTRYADDEDBY,
							'{dateadded}' as CPQTABLEENTRYDATEADDED,
							'{UserId}' as CpqTableEntryModifiedBy,
							'{date}' as CpqTableEntryDateModified,
							'PENDING' as STATUS,
							'{qt_revid}' as QTEREV_ID,
							'{qt_rev_rec_id}' as QTEREV_RECORD_ID
							FROM MALANG (NOLOCK) WHERE MALANG.LANGUAGE_NAME = 'English'""".format(doc_id='Pending',doc_name='',quoteid=get_quote_details.QUOTE_ID,quotename=get_quote_details.QUOTE_NAME,quoterecid=contract_quote_record_id,qt_revid= get_quote_details.QTEREV_ID,qt_rev_rec_id = quote_revision_record_id,UserName=UserName,dateadded=datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"),UserId=UserId,date=datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"))
			#Log.Info(qtqdoc)
		Sql.RunQuery(saqdoc_output_insert)
		
		gen_doc = Quote.GenerateDocument('AMAT_SUBTOTAL_OFFERING', GenDocFormat.PDF)
		fileName = Quote.GetLatestGeneratedDocumentFileName()
		GDB = Quote.GetLatestGeneratedDocumentInBytes()
		List = Quote.GetGeneratedDocumentList('AMAT_SUBTOTAL_OFFERING')
		for doc in List:
			doc_id = doc.Id
			doc_name = doc.FileName
			if fileName==doc_name:
				quote_id = gettoolquote.QUOTE_ID
				#added_by = audit_fields.USERNAME
				#modified_by = audit_fields.CpqTableEntryModifiedBy
				#modified_date = audit_fields.CpqTableEntryDateModified
				guid = str(Guid.NewGuid()).upper()
				qt_rec_id = contract_quote_record_id
				date_added = doc.DateCreated
				update_query = """UPDATE SAQDOC SET DOCUMENT_ID = '{docid}', DOCUMENT_NAME = '{docname}', STATUS = 'ACQUIRED' WHERE DOCUMENT_ID = 'Pending' AND SAQDOC.LANGUAGE_ID = 'EN' AND STATUS = 'PENDING' AND QUOTE_RECORD_ID = '{recid}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}'""".format(recid=contract_quote_record_id,docid=doc_id,docname=doc_name,quote_revision_record_id=quote_revision_record_id)
				Sql.RunQuery(update_query)
	return True


def language_select():
	Trace.Write("Inside language select")
	sec_str =  ''
	get_quote_status = Sql.GetFirst("SELECT REVISION_STATUS FROM SAQTRV WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(contract_quote_record_id,quote_revision_record_id))
	if get_quote_status:
		if str(get_quote_status.REVISION_STATUS).upper() == "APPROVED":
			Trace.Write("If")
			sec_str += ('<div id="container">')
			sec_str += (
					'<div class="dyn_main_head master_manufac glyphicon pointer   glyphicon-chevron-down" onclick="dyn_main_sec_collapse_arrow(this)" data-target=".sec_" data-toggle="collapse"><label class="onlytext"><label class="onlytext"><div>GENERAL SETTINGS</div></label></div>')

		
			sec_str += ('<div id="sec_LANG" class= sec_LANG>')
			#dropdown
			sec_str += (
			'<div style="height: 30px; border-left: 0px; border-right: 0px; border-bottom: 1px solid rgb(204, 204, 204); padding-bottom: 10px;" data-bind="attr: {"id":"drop_cont"+stdAttrCode(),"class": isWholeRow() ? "g4 except_sec dropDownHeight iconhvr" : "g1 except_sec dropDownHeight iconhvr" }" id="drop_cont11744" class="g4 except_sec dropDownHeight iconhvr">')
			sec_str += (
			'<div class="col-md-5">	<abbr data-bind="attr:{"title":label}" title="doc_lang"><label class="col-md-11" data-bind="html: label" style="padding: 5px 5px;margin: 0;" title="doc_lang">Document Language</label></abbr><a href="#" class="col-md-1" style="text-align:right;padding: 7px 5px;color:green">	<i class="fa fa-info-circle autoClosePopover" data-bind="popover: { templateId: "HintTemplate", container: "body", placement: "top", autoClose: true, html: true}" data-original-title="doc_lang" title=""></i></a></div><!--ko if: $data.template() === "DropDownTemplate" && $data.name().toString().indexOf("") === -1 && $data.name().toString().indexOf("") === -1 && $data.name().toString().indexOf("") === -1--><div class="col-md-3 pad-0"><select class="form-control light_yellow" id="Lang"><option value="Select">Select</option><option value="English">English</option><option value="Chinese">Chinese</option></select></div><!-- /ko --><!-- ko if: $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1--><!-- /ko --><div class="col-md-3 " style="display:none;"> <span class="" data-bind="attr:{"id": $data.name()}" id=""></span></div><div class="col-md-1" style="float: right;"><div class="col-md-12 editiconright"><a href="#" onclick="editclick_row(this)" class="editclick">	<i class="fa fa-pencil" aria-hidden="true"></i></a></div></div><div class="col-md-3 pad-0 mrg-bt-5"></div></div>')


			#dropdown
			sec_str += (
			'<div style="height: 30px; border-left: 0px; border-right: 0px; border-bottom: 1px solid rgb(204, 204, 204); padding-bottom: 10px;" data-bind="attr: {"id":"drop_cont"+stdAttrCode(),"class": isWholeRow() ? "g4 except_sec dropDownHeight iconhvr" : "g1 except_sec dropDownHeight iconhvr" }" id="drop_cont11744" class="g4 except_sec dropDownHeight iconhvr">')
			sec_str += (
			'<div class="col-md-5">	<abbr data-bind="attr:{"title":label}" title="doc_Cur"><label class="col-md-11" data-bind="html: label" style="padding: 5px 5px;margin: 0;" title="doc_lang">Document  Currency</label></abbr><a href="#" class="col-md-1" style="text-align:right;padding: 7px 5px;color:green">	<i class="fa fa-info-circle autoClosePopover" data-bind="popover: { templateId: "HintTemplate", container: "body", placement: "top", autoClose: true, html: true}" data-original-title="doc_lang" title=""></i></a></div><!--ko if: $data.template() === "DropDownTemplate" && $data.name().toString().indexOf("") === -1 && $data.name().toString().indexOf("") === -1 && $data.name().toString().indexOf("") === -1--><div class="col-md-3 pad-0"><select class="form-control light_yellow" id="Lang" ><option value="Select">Select</option><option value="Japan">YEN</option><option value="Dollar">USD</option><option value="Chinese">YUAN</option></select></div><!-- /ko --><!-- ko if: $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1--><!-- /ko --><div class="col-md-3 " style="display:none;"> <span class="" data-bind="attr:{"id": $data.name()}" id=""></span></div><div class="col-md-1" style="float: right;"><div class="col-md-12 editiconright"><a href="#" onclick="editclick_row(this)" class="editclick">	<i class="fa fa-pencil" aria-hidden="true"></i></a></div></div><div class="col-md-3 pad-0 mrg-bt-5"></div></div>')
		
			#Checkbox 1
			sec_str += (
			'<div style="height: 30px; border-left: 0px; border-right: 0px; border-bottom: 1px solid rgb(204, 204, 204); padding-bottom: 10px;" data-bind="attr: {"id":"drop_cont"+stdAttrCode(),"class": isWholeRow() ? "g4 except_sec dropDownHeight iconhvr" : "g1 except_sec dropDownHeight iconhvr" }" id="drop_cont11744" class="g4 except_sec dropDownHeight iconhvr">')
			sec_str += ('<div class="col-md-5">	<abbr data-bind="attr:{"title":label}" title="doc_lang"><label class="col-md-11" data-bind="html: label" style="padding: 5px 5px;margin: 0;" title="doc_lang">Include Expected Date of Fx Rate</label></abbr><a href="#" class="col-md-1" style="text-align:right;padding: 7px 5px;color:green">	<i class="fa fa-info-circle autoClosePopover" data-bind="popover: { templateId: "HintTemplate", container: "body", placement: "top", autoClose: true, html: true}" data-original-title="doc_lang" title=""></i></a></div><div class="col-md-3 pad-0 padt_7"><input id="include_expected_date" class="custom custom_gen_doc" type="checkbox" ><span class="lbl"></span></div><!-- /ko --><div class="col-md-3 " style="display:none;"> <span class="" data-bind="attr:{"id": $data.name()}" id=""></span></div><div class="col-md-1" style="float: right;"><div class="col-md-12 editiconright"><a href="#" onclick="editclick_row(this)" class="editclick">	<i class="fa fa-pencil" aria-hidden="true"></i></a></div></div><div class="col-md-3 pad-0 mrg-bt-5"></div></div><!-- /ko --><!-- ko if: $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1--><!-- /ko -->')
		
		
			#Checkbox 2
			sec_str += (
			'<div style="height: 30px; border-left: 0px; border-right: 0px; border-bottom: 1px solid rgb(204, 204, 204); padding-bottom: 10px;" data-bind="attr: {"id":"drop_cont"+stdAttrCode(),"class": isWholeRow() ? "g4 except_sec dropDownHeight iconhvr" : "g1 except_sec dropDownHeight iconhvr" }" id="drop_cont11744" class="g4 except_sec dropDownHeight iconhvr">')
			sec_str += ('<div class="col-md-5">	<abbr data-bind="attr:{"title":label}" title="doc_lang"><label class="col-md-11" data-bind="html: label" style="padding: 5px 5px;margin: 0;" title="doc_lang">Include Items</label></abbr><a href="#" class="col-md-1" style="text-align:right;padding: 7px 5px;color:green">	<i class="fa fa-info-circle autoClosePopover" data-bind="popover: { templateId: "HintTemplate", container: "body", placement: "top", autoClose: true, html: true}" data-original-title="doc_lang" title=""></i></a></div><div class="col-md-3 pad-0 padt_7"><input id="include_items" class="custom custom_gen_doc" type="checkbox" ><span class="lbl"></span></div><!-- /ko --><div class="col-md-3 " style="display:none;"> <span class="" data-bind="attr:{"id": $data.name()}" id=""></span></div><div class="col-md-1" style="float: right;"><div class="col-md-12 editiconright"><a href="#" onclick="editclick_row(this)" class="editclick">	<i class="fa fa-pencil" aria-hidden="true"></i></a></div></div><div class="col-md-3 pad-0 mrg-bt-5"></div></div><!-- /ko --><!-- ko if: $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1--><!-- /ko -->')
		
		
		
			#Checkbox 3
			sec_str += (
			'<div style="height: 30px; border-left: 0px; border-right: 0px; border-bottom: 1px solid rgb(204, 204, 204); padding-bottom: 10px;" data-bind="attr: {"id":"drop_cont"+stdAttrCode(),"class": isWholeRow() ? "g4 except_sec dropDownHeight iconhvr" : "g1 except_sec dropDownHeight iconhvr" }" id="drop_cont11744" class="g4 except_sec dropDownHeight iconhvr">')
			sec_str += ('<div class="col-md-5">	<abbr data-bind="attr:{"title":label}" title="doc_lang"><label class="col-md-11" data-bind="html: label" style="padding: 5px 5px;margin: 0;" title="doc_lang">Include Signature Line</label></abbr><a href="#" class="col-md-1" style="text-align:right;padding: 7px 5px;color:green">	<i class="fa fa-info-circle autoClosePopover" data-bind="popover: { templateId: "HintTemplate", container: "body", placement: "top", autoClose: true, html: true}" data-original-title="doc_lang" title=""></i></a></div><div class="col-md-3 pad-0 padt_7"><input id="include_signature" class="custom custom_gen_doc" type="checkbox" ><span class="lbl"></span></div><!-- /ko --><div class="col-md-3 " style="display:none;"> <span class="" data-bind="attr:{"id": $data.name()}" id=""></span></div><div class="col-md-1" style="float: right;"><div class="col-md-12 editiconright"><a href="#" onclick="editclick_row(this)" class="editclick">	<i class="fa fa-pencil" aria-hidden="true"></i></a></div></div><div class="col-md-3 pad-0 mrg-bt-5"></div></div><!-- /ko --><!-- ko if: $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1--><!-- /ko -->')
		
			#Appendixes
			sec_str += ('<div id="container">')
			sec_str += (
					'<div class="dyn_main_head master_manufac glyphicon pointer   glyphicon-chevron-down" onclick="dyn_main_sec_collapse_arrow(this)" data-target=".sec_" data-toggle="collapse"><label class="onlytext"><label class="onlytext"><div>APPENDIXES</div></label></div>')

			sec_str += ('<div id="sec_LANG" class= sec_LANG>')
			#Checkbox 4
			sec_str += (
			'<div style="height: 30px; border-left: 0px; border-right: 0px; border-bottom: 1px solid rgb(204, 204, 204); padding-bottom: 10px;" data-bind="attr: {"id":"drop_cont"+stdAttrCode(),"class": isWholeRow() ? "g4 except_sec dropDownHeight iconhvr" : "g1 except_sec dropDownHeight iconhvr" }" id="drop_cont11744" class="g4 except_sec dropDownHeight iconhvr">')
			sec_str += ('<div class="col-md-5">	<abbr data-bind="attr:{"title":label}" title="doc_lang"><label class="col-md-11" data-bind="html: label" style="padding: 5px 5px;margin: 0;" title="doc_lang">Include Parts List</label></abbr><a href="#" class="col-md-1" style="text-align:right;padding: 7px 5px;color:green">	<i class="fa fa-info-circle autoClosePopover" data-bind="popover: { templateId: "HintTemplate", container: "body", placement: "top", autoClose: true, html: true}" data-original-title="doc_lang" title=""></i></a></div><div class="col-md-3 pad-0 padt_7"><input id="include_parts_list" class="custom custom_gen_doc" type="checkbox" ><span class="lbl"></span></div><!-- /ko --><div class="col-md-3 " style="display:none;"> <span class="" data-bind="attr:{"id": $data.name()}" id=""></span></div><div class="col-md-1" style="float: right;"><div class="col-md-12 editiconright"><a href="#" onclick="editclick_row(this)" class="editclick">	<i class="fa fa-pencil" aria-hidden="true"></i></a></div></div><div class="col-md-3 pad-0 mrg-bt-5"></div></div><!-- /ko --><!-- ko if: $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1--><!-- /ko -->')
			#checkbox 5
			sec_str += (
			'<div style="height: 30px; border-left: 0px; border-right: 0px; border-bottom: 1px solid rgb(204, 204, 204); padding-bottom: 10px;" data-bind="attr: {"id":"drop_cont"+stdAttrCode(),"class": isWholeRow() ? "g4 except_sec dropDownHeight iconhvr" : "g1 except_sec dropDownHeight iconhvr" }" id="drop_cont11744" class="g4 except_sec dropDownHeight iconhvr">')
			sec_str += ('<div class="col-md-5">	<abbr data-bind="attr:{"title":label}" title="doc_lang"><label class="col-md-11" data-bind="html: label" style="padding: 5px 5px;margin: 0;" title="doc_lang">Include Part Delivery schedule(FPM only)</label></abbr><a href="#" class="col-md-1" style="text-align:right;padding: 7px 5px;color:green">	<i class="fa fa-info-circle autoClosePopover" data-bind="popover: { templateId: "HintTemplate", container: "body", placement: "top", autoClose: true, html: true}" data-original-title="doc_lang" title=""></i></a></div><div class="col-md-3 pad-0 padt_7"><input id="include_part_delivery" class="custom custom_gen_doc" type="checkbox" ><span class="lbl"></span></div><!-- /ko --><div class="col-md-3 " style="display:none;"> <span class="" data-bind="attr:{"id": $data.name()}" id=""></span></div><div class="col-md-1" style="float: right;"><div class="col-md-12 editiconright"><a href="#" onclick="editclick_row(this)" class="editclick">	<i class="fa fa-pencil" aria-hidden="true"></i></a></div></div><div class="col-md-3 pad-0 mrg-bt-5"></div></div><!-- /ko --><!-- ko if: $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1--><!-- /ko -->')	
			#checkbox 5
			sec_str += (
			'<div style="height: 30px; border-left: 0px; border-right: 0px; border-bottom: 1px solid rgb(204, 204, 204); padding-bottom: 10px;" data-bind="attr: {"id":"drop_cont"+stdAttrCode(),"class": isWholeRow() ? "g4 except_sec dropDownHeight iconhvr" : "g1 except_sec dropDownHeight iconhvr" }" id="drop_cont11744" class="g4 except_sec dropDownHeight iconhvr">')
			sec_str += ('<div class="col-md-5">	<abbr data-bind="attr:{"title":label}" title="doc_lang"><label class="col-md-11" data-bind="html: label" style="padding: 5px 5px;margin: 0;" title="doc_lang">Include Detailed Billing Matrix by Offering</label></abbr><a href="#" class="col-md-1" style="text-align:right;padding: 7px 5px;color:green">	<i class="fa fa-info-circle autoClosePopover" data-bind="popover: { templateId: "HintTemplate", container: "body", placement: "top", autoClose: true, html: true}" data-original-title="doc_lang" title=""></i></a></div><div class="col-md-3 pad-0 padt_7"><input id="billmat" class="custom custom_gen_doc" type="checkbox" ><span class="lbl"></span></div><!-- /ko --><div class="col-md-3 " style="display:none;"> <span class="" data-bind="attr:{"id": $data.name()}" id=""></span></div><div class="col-md-1" style="float: right;"><div class="col-md-12 editiconright"><a href="#" onclick="editclick_row(this)" class="editclick">	<i class="fa fa-pencil" aria-hidden="true"></i></a></div></div><div class="col-md-3 pad-0 mrg-bt-5"></div></div><!-- /ko --><!-- ko if: $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1--><!-- /ko -->')

			#dropdown
			sec_str += (
			'<div style="height: 30px; border-left: 0px; border-right: 0px; border-bottom: 1px solid rgb(204, 204, 204); padding-bottom: 10px;" data-bind="attr: {"id":"drop_cont"+stdAttrCode(),"class": isWholeRow() ? "g4 except_sec dropDownHeight iconhvr" : "g1 except_sec dropDownHeight iconhvr" }" id="drop_cont11744" class="g4 except_sec dropDownHeight iconhvr">')
			sec_str += (
			'<div class="col-md-5">	<abbr data-bind="attr:{"title":label}" title="doc_lang"><label class="col-md-11" data-bind="html: label" style="padding: 5px 5px;margin: 0;" title="doc_lang">Include Critical parameter</label></abbr><a href="#" class="col-md-1" style="text-align:right;padding: 7px 5px;color:green">	<i class="fa fa-info-circle autoClosePopover" data-bind="popover: { templateId: "HintTemplate", container: "body", placement: "top", autoClose: true, html: true}" data-original-title="doc_lang" title=""></i></a></div><!--ko if: $data.template() === "DropDownTemplate" && $data.name().toString().indexOf("") === -1 && $data.name().toString().indexOf("") === -1 && $data.name().toString().indexOf("") === -1--><div class="col-md-3 pad-0"><select id="doc" class="form-control light_yellow" id="Lang"><option value="Select">Select</option><option value="Critical Parameters by Greenbook">Critical Parameters by Greenbook</option><option value="Critical Parameters by Fab and Greenbook">Critical Parameters by Fab and Greenbook</option></select></div><!-- /ko --><!-- ko if: $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1--><!-- /ko --><div class="col-md-3 " style="display:none;"> <span class="" data-bind="attr:{"id": $data.name()}" id=""></span></div><div class="col-md-1" style="float: right;"><div class="col-md-12 editiconright"><a href="#" onclick="editclick_row(this)" class="editclick">	<i class="fa fa-pencil" aria-hidden="true"></i></a></div></div><div class="col-md-3 pad-0 mrg-bt-5"></div></div>')


			#sec_str += (
			#	'<div class="g4  except_sec removeHorLine iconhvr sec_edit_sty"><button id="SEC_DIS_CLOSE" style="display: none;"></button><button id="Lang_cancel" class="btnconfig btnMainBanner #sec_edit_sty_btn" onclick="lang_cancel()" name="SECT_CANCEL">CANCEL</button><button id="Lang_Select" class="btnconfig btnMainBanner sec_edit_sty_btn_inh" onclick="lang_save()" #name="SECT_SAVE">SAVE</button></div>')

			sec_str += (
			"</div>")

			sec_str += '<table class="wth100mrg8"><tbody>'
		else:
			Trace.Write("Else")
			sec_str += ('<div id="container">')
			sec_str += (
					'<div class="dyn_main_head master_manufac glyphicon pointer   glyphicon-chevron-down" onclick="dyn_main_sec_collapse_arrow(this)" data-target=".sec_" data-toggle="collapse"><label class="onlytext"><label class="onlytext"><div>GENERAL SETTINGS</div></label></div>')

		
			sec_str += ('<div id="sec_LANG" class= sec_LANG>')
			#dropdown
			sec_str += (
			'<div style="height: 30px; border-left: 0px; border-right: 0px; border-bottom: 1px solid rgb(204, 204, 204); padding-bottom: 10px;" data-bind="attr: {"id":"drop_cont"+stdAttrCode(),"class": isWholeRow() ? "g4 except_sec dropDownHeight iconhvr" : "g1 except_sec dropDownHeight iconhvr" }" id="drop_cont11744" class="g4 except_sec dropDownHeight iconhvr">')
			sec_str += (
			'<div class="col-md-5">	<abbr data-bind="attr:{"title":label}" title="doc_lang"><label class="col-md-11" data-bind="html: label" style="padding: 5px 5px;margin: 0;" title="doc_lang">Document Language</label></abbr><a href="#" class="col-md-1" style="text-align:right;padding: 7px 5px;color:green">	<i class="fa fa-info-circle autoClosePopover" data-bind="popover: { templateId: "HintTemplate", container: "body", placement: "top", autoClose: true, html: true}" data-original-title="doc_lang" title=""></i></a></div><!--ko if: $data.template() === "DropDownTemplate" && $data.name().toString().indexOf("") === -1 && $data.name().toString().indexOf("") === -1 && $data.name().toString().indexOf("") === -1--><div class="col-md-3 pad-0"><select class="form-control" id="Lang" disabled><option value="Select">Select</option><option value="English">English</option><option value="Chinese">Chinese</option></select></div><!-- /ko --><!-- ko if: $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1--><!-- /ko --><div class="col-md-3 " style="display:none;"> <span class="" data-bind="attr:{"id": $data.name()}" id=""></span></div><div class="col-md-1" style="float: right;"><div class="col-md-12 editiconright"><a href="#" onclick="editclick_row(this)" class="editclick">	<i class="fa fa-lock" aria-hidden="true"></i></a></div></div><div class="col-md-3 pad-0 mrg-bt-5"></div></div>')


			#dropdown
			sec_str += (
			'<div style="height: 30px; border-left: 0px; border-right: 0px; border-bottom: 1px solid rgb(204, 204, 204); padding-bottom: 10px;" data-bind="attr: {"id":"drop_cont"+stdAttrCode(),"class": isWholeRow() ? "g4 except_sec dropDownHeight iconhvr" : "g1 except_sec dropDownHeight iconhvr" }" id="drop_cont11744" class="g4 except_sec dropDownHeight iconhvr">')
			sec_str += (
			'<div class="col-md-5">	<abbr data-bind="attr:{"title":label}" title="doc_Cur"><label class="col-md-11" data-bind="html: label" style="padding: 5px 5px;margin: 0;" title="doc_lang">Document  Currency</label></abbr><a href="#" class="col-md-1" style="text-align:right;padding: 7px 5px;color:green">	<i class="fa fa-info-circle autoClosePopover" data-bind="popover: { templateId: "HintTemplate", container: "body", placement: "top", autoClose: true, html: true}" data-original-title="doc_lang" title=""></i></a></div><!--ko if: $data.template() === "DropDownTemplate" && $data.name().toString().indexOf("") === -1 && $data.name().toString().indexOf("") === -1 && $data.name().toString().indexOf("") === -1--><div class="col-md-3 pad-0"><select class="form-control" id="Lang" disabled><option value="Select">Select</option><option value="Japan">YEN</option><option value="Dollar">USD</option><option value="Chinese">YUAN</option></select></div><!-- /ko --><!-- ko if: $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1--><!-- /ko --><div class="col-md-3 " style="display:none;"> <span class="" data-bind="attr:{"id": $data.name()}" id=""></span></div><div class="col-md-1" style="float: right;"><div class="col-md-12 editiconright"><a href="#" onclick="editclick_row(this)" class="editclick">	<i class="fa fa-lock" aria-hidden="true"></i></a></div></div><div class="col-md-3 pad-0 mrg-bt-5"></div></div>')
		
			#Checkbox 1
			sec_str += (
			'<div style="height: 30px; border-left: 0px; border-right: 0px; border-bottom: 1px solid rgb(204, 204, 204); padding-bottom: 10px;" data-bind="attr: {"id":"drop_cont"+stdAttrCode(),"class": isWholeRow() ? "g4 except_sec dropDownHeight iconhvr" : "g1 except_sec dropDownHeight iconhvr" }" id="drop_cont11744" class="g4 except_sec dropDownHeight iconhvr">')
			sec_str += ('<div class="col-md-5">	<abbr data-bind="attr:{"title":label}" title="doc_lang"><label class="col-md-11" data-bind="html: label" style="padding: 5px 5px;margin: 0;" title="doc_lang">Include Expected Date of Fx Rate</label></abbr><a href="#" class="col-md-1" style="text-align:right;padding: 7px 5px;color:green">	<i class="fa fa-info-circle autoClosePopover" data-bind="popover: { templateId: "HintTemplate", container: "body", placement: "top", autoClose: true, html: true}" data-original-title="doc_lang" title=""></i></a></div><div class="col-md-3 pad-0 padt_7"><input id="fxrate" class="custom custom_gen_doc" type="checkbox" disabled><span class="lbl"></span></div><!-- /ko --><div class="col-md-3 " style="display:none;"> <span class="" data-bind="attr:{"id": $data.name()}" id=""></span></div><div class="col-md-1" style="float: right;"><div class="col-md-12 editiconright"><a href="#" onclick="editclick_row(this)" class="editclick">	<i class="fa fa-lock" aria-hidden="true"></i></a></div></div><div class="col-md-3 pad-0 mrg-bt-5"></div></div><!-- /ko --><!-- ko if: $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1--><!-- /ko -->')
		
		
			#Checkbox 2
			sec_str += (
			'<div style="height: 30px; border-left: 0px; border-right: 0px; border-bottom: 1px solid rgb(204, 204, 204); padding-bottom: 10px;" data-bind="attr: {"id":"drop_cont"+stdAttrCode(),"class": isWholeRow() ? "g4 except_sec dropDownHeight iconhvr" : "g1 except_sec dropDownHeight iconhvr" }" id="drop_cont11744" class="g4 except_sec dropDownHeight iconhvr">')
			sec_str += ('<div class="col-md-5">	<abbr data-bind="attr:{"title":label}" title="doc_lang"><label class="col-md-11" data-bind="html: label" style="padding: 5px 5px;margin: 0;" title="doc_lang">Include Items</label></abbr><a href="#" class="col-md-1" style="text-align:right;padding: 7px 5px;color:green">	<i class="fa fa-info-circle autoClosePopover" data-bind="popover: { templateId: "HintTemplate", container: "body", placement: "top", autoClose: true, html: true}" data-original-title="doc_lang" title=""></i></a></div><div class="col-md-3 pad-0 padt_7"><input id="bm" class="custom custom_gen_doc" type="checkbox" disabled><span class="lbl"></span></div><!-- /ko --><div class="col-md-3 " style="display:none;"> <span class="" data-bind="attr:{"id": $data.name()}" id=""></span></div><div class="col-md-1" style="float: right;"><div class="col-md-12 editiconright"><a href="#" onclick="editclick_row(this)" class="editclick">	<i class="fa fa-lock" aria-hidden="true"></i></a></div></div><div class="col-md-3 pad-0 mrg-bt-5"></div></div><!-- /ko --><!-- ko if: $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1--><!-- /ko -->')
		
		
		
			#Checkbox 3
			sec_str += (
			'<div style="height: 30px; border-left: 0px; border-right: 0px; border-bottom: 1px solid rgb(204, 204, 204); padding-bottom: 10px;" data-bind="attr: {"id":"drop_cont"+stdAttrCode(),"class": isWholeRow() ? "g4 except_sec dropDownHeight iconhvr" : "g1 except_sec dropDownHeight iconhvr" }" id="drop_cont11744" class="g4 except_sec dropDownHeight iconhvr">')
			sec_str += ('<div class="col-md-5">	<abbr data-bind="attr:{"title":label}" title="doc_lang"><label class="col-md-11" data-bind="html: label" style="padding: 5px 5px;margin: 0;" title="doc_lang">Include Signature Line</label></abbr><a href="#" class="col-md-1" style="text-align:right;padding: 7px 5px;color:green">	<i class="fa fa-info-circle autoClosePopover" data-bind="popover: { templateId: "HintTemplate", container: "body", placement: "top", autoClose: true, html: true}" data-original-title="doc_lang" title=""></i></a></div><div class="col-md-3 pad-0 padt_7"><input id="include_sign" class="custom custom_gen_doc" type="checkbox" disabled><span class="lbl"></span></div><!-- /ko --><div class="col-md-3 " style="display:none;"> <span class="" data-bind="attr:{"id": $data.name()}" id=""></span></div><div class="col-md-1" style="float: right;"><div class="col-md-12 editiconright"><a href="#" onclick="editclick_row(this)" class="editclick">	<i class="fa fa-lock" aria-hidden="true"></i></a></div></div><div class="col-md-3 pad-0 mrg-bt-5"></div></div><!-- /ko --><!-- ko if: $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1--><!-- /ko -->')
		
			#Appendixes
			sec_str += ('<div id="container">')
			sec_str += (
					'<div class="dyn_main_head master_manufac glyphicon pointer   glyphicon-chevron-down" onclick="dyn_main_sec_collapse_arrow(this)" data-target=".sec_" data-toggle="collapse"><label class="onlytext"><label class="onlytext"><div>APPENDIXES</div></label></div>')

			sec_str += ('<div id="sec_LANG" class= sec_LANG>')
			#Checkbox 4
			sec_str += (
			'<div style="height: 30px; border-left: 0px; border-right: 0px; border-bottom: 1px solid rgb(204, 204, 204); padding-bottom: 10px;" data-bind="attr: {"id":"drop_cont"+stdAttrCode(),"class": isWholeRow() ? "g4 except_sec dropDownHeight iconhvr" : "g1 except_sec dropDownHeight iconhvr" }" id="drop_cont11744" class="g4 except_sec dropDownHeight iconhvr">')
			sec_str += ('<div class="col-md-5">	<abbr data-bind="attr:{"title":label}" title="doc_lang"><label class="col-md-11" data-bind="html: label" style="padding: 5px 5px;margin: 0;" title="doc_lang">Include Parts List</label></abbr><a href="#" class="col-md-1" style="text-align:right;padding: 7px 5px;color:green">	<i class="fa fa-info-circle autoClosePopover" data-bind="popover: { templateId: "HintTemplate", container: "body", placement: "top", autoClose: true, html: true}" data-original-title="doc_lang" title=""></i></a></div><div class="col-md-3 pad-0 padt_7"><input id="include_parts_list" class="custom custom_gen_doc" type="checkbox" disabled><span class="lbl"></span></div><!-- /ko --><div class="col-md-3 " style="display:none;"> <span class="" data-bind="attr:{"id": $data.name()}" id=""></span></div><div class="col-md-1" style="float: right;"><div class="col-md-12 editiconright"><a href="#" onclick="editclick_row(this)" class="editclick">	<i class="fa fa-lock" aria-hidden="true"></i></a></div></div><div class="col-md-3 pad-0 mrg-bt-5"></div></div><!-- /ko --><!-- ko if: $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1--><!-- /ko -->')
			#checkbox 5
			sec_str += (
			'<div style="height: 30px; border-left: 0px; border-right: 0px; border-bottom: 1px solid rgb(204, 204, 204); padding-bottom: 10px;" data-bind="attr: {"id":"drop_cont"+stdAttrCode(),"class": isWholeRow() ? "g4 except_sec dropDownHeight iconhvr" : "g1 except_sec dropDownHeight iconhvr" }" id="drop_cont11744" class="g4 except_sec dropDownHeight iconhvr">')
			sec_str += ('<div class="col-md-5">	<abbr data-bind="attr:{"title":label}" title="doc_lang"><label class="col-md-11" data-bind="html: label" style="padding: 5px 5px;margin: 0;" title="doc_lang">Include Part Delivery schedule(FPM only)</label></abbr><a href="#" class="col-md-1" style="text-align:right;padding: 7px 5px;color:green">	<i class="fa fa-info-circle autoClosePopover" data-bind="popover: { templateId: "HintTemplate", container: "body", placement: "top", autoClose: true, html: true}" data-original-title="doc_lang" title=""></i></a></div><div class="col-md-3 pad-0 padt_7"><input id="part_delivery_schedule" class="custom custom_gen_doc" type="checkbox" disabled><span class="lbl"></span></div><!-- /ko --><div class="col-md-3 " style="display:none;"> <span class="" data-bind="attr:{"id": $data.name()}" id=""></span></div><div class="col-md-1" style="float: right;"><div class="col-md-12 editiconright"><a href="#" onclick="editclick_row(this)" class="editclick">	<i class="fa fa-lock" aria-hidden="true"></i></a></div></div><div class="col-md-3 pad-0 mrg-bt-5"></div></div><!-- /ko --><!-- ko if: $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1--><!-- /ko -->')	
			#checkbox 5
			sec_str += (
			'<div style="height: 30px; border-left: 0px; border-right: 0px; border-bottom: 1px solid rgb(204, 204, 204); padding-bottom: 10px;" data-bind="attr: {"id":"drop_cont"+stdAttrCode(),"class": isWholeRow() ? "g4 except_sec dropDownHeight iconhvr" : "g1 except_sec dropDownHeight iconhvr" }" id="drop_cont11744" class="g4 except_sec dropDownHeight iconhvr">')
			sec_str += ('<div class="col-md-5">	<abbr data-bind="attr:{"title":label}" title="doc_lang"><label class="col-md-11" data-bind="html: label" style="padding: 5px 5px;margin: 0;" title="doc_lang">Include Detailed Billing Matrix by Offering</label></abbr><a href="#" class="col-md-1" style="text-align:right;padding: 7px 5px;color:green">	<i class="fa fa-info-circle autoClosePopover" data-bind="popover: { templateId: "HintTemplate", container: "body", placement: "top", autoClose: true, html: true}" data-original-title="doc_lang" title=""></i></a></div><div class="col-md-3 pad-0 padt_7"><input id="billmat" class="custom custom_gen_doc" type="checkbox" disabled><span class="lbl"></span></div><!-- /ko --><div class="col-md-3 " style="display:none;"> <span class="" data-bind="attr:{"id": $data.name()}" id=""></span></div><div class="col-md-1" style="float: right;"><div class="col-md-12 editiconright"><a href="#" onclick="editclick_row(this)" class="editclick">	<i class="fa fa-lock" aria-hidden="true"></i></a></div></div><div class="col-md-3 pad-0 mrg-bt-5"></div></div><!-- /ko --><!-- ko if: $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1--><!-- /ko -->')

			#dropdown
			sec_str += (
			'<div style="height: 30px; border-left: 0px; border-right: 0px; border-bottom: 1px solid rgb(204, 204, 204); padding-bottom: 10px;" data-bind="attr: {"id":"drop_cont"+stdAttrCode(),"class": isWholeRow() ? "g4 except_sec dropDownHeight iconhvr" : "g1 except_sec dropDownHeight iconhvr" }" id="drop_cont11744" class="g4 except_sec dropDownHeight iconhvr">')
			sec_str += (
			'<div class="col-md-5">	<abbr data-bind="attr:{"title":label}" title="doc_lang"><label class="col-md-11" data-bind="html: label" style="padding: 5px 5px;margin: 0;" title="doc_lang">Include Critical parameter</label></abbr><a href="#" class="col-md-1" style="text-align:right;padding: 7px 5px;color:green">	<i class="fa fa-info-circle autoClosePopover" data-bind="popover: { templateId: "HintTemplate", container: "body", placement: "top", autoClose: true, html: true}" data-original-title="doc_lang" title=""></i></a></div><!--ko if: $data.template() === "DropDownTemplate" && $data.name().toString().indexOf("") === -1 && $data.name().toString().indexOf("") === -1 && $data.name().toString().indexOf("") === -1--><div class="col-md-3 pad-0"><select id="doc" class="form-control" id="Lang" disabled><option value="Select">Select</option><option value="Critical Parameters by Greenbook">Critical Parameters by Greenbook</option><option value="Critical Parameters by Fab and Greenbook">Critical Parameters by Fab and Greenbook</option></select></div><!-- /ko --><!-- ko if: $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1--><!-- /ko --><div class="col-md-3 " style="display:none;"> <span class="" data-bind="attr:{"id": $data.name()}" id=""></span></div><div class="col-md-1" style="float: right;"><div class="col-md-12 editiconright"><a href="#" onclick="editclick_row(this)" class="editclick">	<i class="fa fa-lock" aria-hidden="true"></i></a></div></div><div class="col-md-3 pad-0 mrg-bt-5"></div></div>')


			#sec_str += (
			#	'<div class="g4  except_sec removeHorLine iconhvr sec_edit_sty"><button id="SEC_DIS_CLOSE" style="display: none;"></button><button id="Lang_cancel" class="btnconfig btnMainBanner sec_edit_sty_btn" onclick="lang_cancel()" name="SECT_CANCEL">CANCEL</button><button id="Lang_Select" class="btnconfig btnMainBanner sec_edit_sty_btn_inh" onclick="lang_save()" name="SECT_SAVE">SAVE</button></div>'
			#)

			sec_str += (
			"</div>")

			sec_str += '<table class="wth100mrg8"><tbody>'
	return sec_str

try:
	action_type = Param.LOAD
except:
	action_type = ''



try:
	parts_list = Param.parts_list
except:
	parts_list = ''
try:
	billing_matrix = Param.billing_matrix
except:
	billing_matrix = ''
try:
	delivery_schedule = Param.delivery_schedule
except:
	delivery_schedule = ''
try:
	parts_list_include = Param.parts_list_include
except:
	parts_list_include = ''
Trace.Write("parts_list---"+str(parts_list)+"--billing_matrix---inside--"+str(billing_matrix))

if str(parts_list) == 'True' and str(billing_matrix) == 'True':
	Quote.GetCustomField('INCLUDE_ITEMS').Content = 'YES'
	Trace.Write('531------')
	Quote.GetCustomField('Billing_Matrix').Content = 'YES'
	ApiResponse = ApiResponseFactory.JsonResponse(insert_spare_doc(parts_list))
elif str(billing_matrix) == 'True':
	Trace.Write('531------')
	Quote.GetCustomField('Billing_Matrix').Content = 'YES'
	ApiResponse = ApiResponseFactory.JsonResponse(insert_spare_doc(parts_list))
elif str(parts_list_include) == 'True':
	Quote.GetCustomField('ITEM_DELIVERY_SCHEDULE').Content = 'YES'
if action_type == "DOCUMENT":
	Trace.Write("inside"+str(action_type))
	ApiResponse = ApiResponseFactory.JsonResponse(language_select())
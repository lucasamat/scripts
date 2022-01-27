#========================================================================================================#================================
#   __script_name : CQIFWUDQTM.PY
#   __script_description : THIS SCRIPT USED TO UPDATE QUOTE ITEMS AND QUOTE LINE ITEMS 
#   __primary_author__ : WASIM
#   __create_date :24-08-2021
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================

import datetime
import Webcom.Configurator.Scripting.Test.TestProduct
import sys
import re
import System.Net
import SYCNGEGUID as CPQID
from SYDATABASE import SQL
from System import Convert
import re

Sql = SQL()
ScriptExecutor = ScriptExecutor
from System.Text.Encoding import UTF8
#Log.Info('quote_revision_record_id- '+str(quote_revision_record_id))
def quoteiteminsert(Qt_id):
	#quote_number = Qt_id[2:12]
	Log.Info('quote_id---'+str(Qt_id))
	
	
	get_rev_rec_id = Sql.GetFirst("SELECT QTEREV_RECORD_ID,QUOTE_CURRENCY,MASTER_TABLE_QUOTE_RECORD_ID FROM SAQTMT where QUOTE_ID = '{}'".format(Qt_id))
	get_exch_rate = Sql.GetFirst("SELECT * FROM SAQTRV where QUOTE_ID = '{}' AND QUOTE_REVISION_RECORD_ID = '{}'".format(Qt_id,get_rev_rec_id.QTEREV_RECORD_ID))
	
	get_exch_rate = get_exch_rate.EXCHANGE_RATE

	##updating saqris
	Sql.RunQuery("""UPDATE SAQRIS 
							SET UNIT_PRICE_INGL_CURR = IQ.UNIT_PRICE_INGL_CURR, 
							NET_PRICE_INGL_CURR=IQ.NET_PRICE_INGL_CURR,
							UNIT_PRICE = IQ.UNIT_PRICE, 
							NET_PRICE=IQ.NET_PRICE, 
							NET_VALUE = IQ.NET_VALUE,
							NET_VALUE_INGL_CURR = IQ.NET_VALUE_INGL_CURR,
							ESTIMATED_VALUE = IQ.ESTIMATED_VALUE,
							COMMITTED_VALUE = IQ.COMMITTED_VALUE,
							TAX_AMOUNT_INGL_CURR = IQ.TAX_AMOUNT_INGL_CURR,
							TAX_AMOUNT = IQ.TAX_AMOUNT

							FROM SAQRIS 
								INNER JOIN (SELECT SAQRIT.QUOTE_RECORD_ID, SAQRIT.QTEREV_RECORD_ID,SAQRIT.SERVICE_ID,
								SUM(ISNULL(SAQRIT.UNIT_PRICE_INGL_CURR, 0)) as UNIT_PRICE_INGL_CURR,
								SUM(ISNULL(SAQRIT.NET_PRICE_INGL_CURR, 0)) as NET_PRICE_INGL_CURR,
								SUM(ISNULL(SAQRIT.UNIT_PRICE, 0)) as UNIT_PRICE,
								SUM(ISNULL(SAQRIT.NET_PRICE, 0)) as NET_PRICE,
								SUM(ISNULL(SAQRIT.NET_VALUE, 0)) as NET_VALUE,
								SUM(ISNULL(SAQRIT.NET_VALUE_INGL_CURR, 0)) as NET_VALUE_INGL_CURR,
								SUM(ISNULL(SAQRIT.ESTIMATED_VALUE, 0)) as ESTIMATED_VALUE,
								SUM(ISNULL(SAQRIT.COMMITTED_VALUE, 0)) as COMMITTED_VALUE,
								SUM(ISNULL(SAQRIT.TAX_AMOUNT_INGL_CURR, 0)) as TAX_AMOUNT_INGL_CURR,
								SUM(ISNULL(SAQRIT.TAX_AMOUNT, 0)) as TAX_AMOUNT

								FROM SAQRIT 
								WHERE SAQRIT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID = '{rev}'  GROUP BY SAQRIT.QUOTE_RECORD_ID, SAQRIT.QTEREV_RECORD_ID,SAQRIT.SERVICE_ID) IQ ON SAQRIS.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND SAQRIS.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND SAQRIS.SERVICE_ID = IQ.SERVICE_ID
						WHERE SAQRIS.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRIS.QTEREV_RECORD_ID='{rev}' """.format( QuoteRecordId= get_rev_rec_id.MASTER_TABLE_QUOTE_RECORD_ID ,rev =get_rev_rec_id.QTEREV_RECORD_ID))
						
	##updating quote summary values in saqtrv
	total_credit = 0
	get_credit_val = Sql.GetFirst("""SELECT * FROM SAQRIS WHERE QUOTE_RECORD_ID = '{quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_rec_id}' AND SERVICE_ID='Z0116' """.format(quote_rec_id = get_rev_rec_id.MASTER_TABLE_QUOTE_RECORD_ID ,quote_revision_rec_id = get_rev_rec_id.QTEREV_RECORD_ID ))
	if get_credit_val:
		if get_credit_val.NET_PRICE_INGL_CURR:
			total_credit = get_credit_val.NET_PRICE_INGL_CURR
	##A055S000P01-13894
	update_revision_status = Sql.GetFirst("SELECT PRICING_STATUS FROM SAQIFP WHERE QUOTE_RECORD_ID = '{quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_rec_id}' AND PRICING_STATUS = 'ERROR'""".format(quote_rec_id = get_rev_rec_id.MASTER_TABLE_QUOTE_RECORD_ID ,quote_revision_rec_id = get_rev_rec_id.QTEREV_RECORD_ID))
	rev_status =""
	if update_revision_status:
		rev_status ="ON HOLD - COSTING"
	else:
		rev_status ="PRICED"
	Sql.RunQuery("""UPDATE SAQTRV
						SET 
						SAQTRV.TAX_AMOUNT_INGL_CURR = IQ.TAX_AMOUNT_INGL_CURR,						
						SAQTRV.NET_PRICE_INGL_CURR = IQ.NET_PRICE_INGL_CURR,
						SAQTRV.NET_VALUE_INGL_CURR = IQ.NET_VALUE_INGL_CURR,
						SAQTRV.CREDIT_INGL_CURR	= """+str(total_credit)+""",
						SAQTRV.REVISION_STATUS	= '"""+str(rev_status)+"""'		
						FROM SAQTRV (NOLOCK)
						INNER JOIN (SELECT SAQRIS.QUOTE_RECORD_ID, SAQRIS.QTEREV_RECORD_ID,
									SUM(ISNULL(SAQRIS.TAX_AMOUNT_INGL_CURR, 0)) as TAX_AMOUNT_INGL_CURR,
									SUM(ISNULL(SAQRIS.NET_PRICE_INGL_CURR, 0)) as NET_PRICE_INGL_CURR,
									SUM(ISNULL(SAQRIS.NET_PRICE, 0)) as NET_PRICE,
									SUM(ISNULL(SAQRIS.NET_VALUE, 0)) as NET_VALUE,
									SUM(ISNULL(SAQRIS.NET_VALUE_INGL_CURR, 0)) as NET_VALUE_INGL_CURR,
									SUM(ISNULL(SAQRIS.TAX_AMOUNT, 0)) as TAX_AMOUNT
									FROM SAQRIS (NOLOCK) WHERE SAQRIS.QUOTE_RECORD_ID = '{quote_rec_id}' AND SAQRIS.QTEREV_RECORD_ID = '{quote_revision_rec_id}' AND SERVICE_ID !='Z0117' GROUP BY SAQRIS.QTEREV_RECORD_ID, SAQRIS.QUOTE_RECORD_ID) IQ ON SAQTRV.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND SAQTRV.QUOTE_REVISION_RECORD_ID = IQ.QTEREV_RECORD_ID
						WHERE SAQTRV.QUOTE_RECORD_ID = '{quote_rec_id}' AND SAQTRV.QUOTE_REVISION_RECORD_ID = '{quote_revision_rec_id}' 	""".format(quote_rec_id = get_rev_rec_id.MASTER_TABLE_QUOTE_RECORD_ID ,quote_revision_rec_id = get_rev_rec_id.QTEREV_RECORD_ID ) )

	# SUM(ISNULL(SAQITM.YEAR_1_INGL_CURR, 0)) as YEAR_1_INGL_CURR,
	# SUM(ISNULL(SAQITM.YEAR_2_INGL_CURR, 0)) as YEAR_2_INGL_CURR,
	# SUM(ISNULL(SAQITM.YEAR_3_INGL_CURR, 0)) as YEAR_3_INGL_CURR,
	# SUM(ISNULL(SAQITM.YEAR_4_INGL_CURR, 0)) as YEAR_4_INGL_CURR,
	# SUM(ISNULL(SAQITM.YEAR_5_INGL_CURR, 0)) as YEAR_5_INGL_CURR
	#updating value to quote summary ends
	try:
		get_services = Sql.GetList("SELECT SERVICE_ID from SAQTSE WHERE QUOTE_RECORD_ID = '{quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_rec_id}'".format(quote_rec_id = get_rev_rec_id.MASTER_TABLE_QUOTE_RECORD_ID ,quote_revision_rec_id = get_rev_rec_id.QTEREV_RECORD_ID ))
		get_services_list = []
		for val in get_services:
			if val.SERVICE_ID:
				get_services_list.append(val.SERVICE_ID)
		LOGIN_CREDENTIALS = SqlHelper.GetFirst("SELECT USER_NAME as Username,Password,Domain FROM SYCONF where Domain='AMAT_TST'")
		if LOGIN_CREDENTIALS is not None:
			Login_Username = str(LOGIN_CREDENTIALS.Username)
			Login_Password = str(LOGIN_CREDENTIALS.Password)
			authorization = Login_Username+":"+Login_Password
			binaryAuthorization = UTF8.GetBytes(authorization)
			authorization = Convert.ToBase64String(binaryAuthorization)
			authorization = "Basic " + authorization


			webclient = System.Net.WebClient()
			webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/json"
			webclient.Headers[System.Net.HttpRequestHeader.Authorization] = authorization;
			
			result = '''<?xml version="1.0" encoding="UTF-8"?><soapenv:Envelope	xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">	<soapenv:Body><CPQ_Columns>	<QUOTE_ID>{Qt_Id}</QUOTE_ID><REVISION_ID>{Rev_Id}</REVISION_ID></CPQ_Columns></soapenv:Body></soapenv:Envelope>'''.format( Qt_Id= contract_quote_record_id,Rev_Id = revision)
			
			LOGIN_CRE = SqlHelper.GetFirst("SELECT URL FROM SYCONF where EXTERNAL_TABLE_NAME ='BILLING_MATRIX_ASYNC'")
			Async = webclient.UploadString(str(LOGIN_CRE.URL), str(result))
	except:
		Log.Info('error in Billing')	
	return "True"

def voucher_amt_update(Qt_id):
	get_rev_rec_id = Sql.GetFirst("SELECT QTEREV_RECORD_ID,QUOTE_CURRENCY,MASTER_TABLE_QUOTE_RECORD_ID FROM SAQTMT where QUOTE_ID = '{}'".format(Qt_id))
	try:
		##updating price for z0117
		check_record = Sql.GetFirst("SELECT count(*) as cnt FROM SAQRIT WHERE QUOTE_RECORD_ID = '{quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_rec_id}' AND SERVICE_ID = 'Z0117' AND ISNULL(STATUS,'') = 'ACQUIRING' or ISNULL(STATUS,'') = ''".format(quote_rec_id = get_rev_rec_id.MASTER_TABLE_QUOTE_RECORD_ID ,quote_revision_rec_id = get_rev_rec_id.QTEREV_RECORD_ID) )
		if check_record.cnt > 0:
			get_greenbook_record = Sql.GetList("SELECT DISTINCT GREENBOOK,ENTITLEMENT_XML,SERVICE_ID,PAR_SERVICE_ID FROM SAQSGE WHERE QUOTE_RECORD_ID = '{quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_rec_id}' AND SERVICE_ID = 'Z0117' ".format(quote_rec_id = get_rev_rec_id.MASTER_TABLE_QUOTE_RECORD_ID ,quote_revision_rec_id = get_rev_rec_id.QTEREV_RECORD_ID))
			tag_pattern = re.compile(r'(<QUOTE_ITEM_ENTITLEMENT>[\w\W]*?</QUOTE_ITEM_ENTITLEMENT>)')
			entitlement_id_tag_pattern = re.compile(r'<ENTITLEMENT_ID>AGS_Z0117_PQB_VCRAMT</ENTITLEMENT_ID>')
			entitlement_display_value_tag_pattern = re.compile(r'<ENTITLEMENT_DISPLAY_VALUE>([^>]*?)</ENTITLEMENT_DISPLAY_VALUE>')
			if get_greenbook_record:
				for record in get_greenbook_record:
					get_voucher_value = ''
					for quote_item_tag in re.finditer(tag_pattern, record.ENTITLEMENT_XML):
						quote_item_tag_content = quote_item_tag.group(1)
						entitlement_id_tag_match = re.findall(entitlement_id_tag_pattern,quote_item_tag_content)	
						if entitlement_id_tag_match:
							entitlement_display_value_tag_match = re.findall(entitlement_display_value_tag_pattern,quote_item_tag_content)
							if entitlement_display_value_tag_match:
								get_voucher_value = entitlement_display_value_tag_match[0].upper()
								break
					Trace.Write("get_voucher_value-"+str(record.GREENBOOK)+"-"+str(get_voucher_value))
					Sql.RunQuery("UPDATE SAQICO SET STATUS = 'ACQUIRED', CNTPRI_INGL_CURR = '{voucher_amt}' FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_rec_id}' AND SERVICE_ID = 'Z0117' AND GREENBOOK = '{grnbok}' ".format(quote_rec_id = get_rev_rec_id.MASTER_TABLE_QUOTE_RECORD_ID ,quote_revision_rec_id = get_rev_rec_id.QTEREV_RECORD_ID,voucher_amt = get_voucher_value,grnbok = record.GREENBOOK  ))
			
					Sql.RunQuery("""UPDATE SAQRIT 
						SET 
						YEAR_1 = '{voucher_amt}',
						YEAR_1_INGL_CURR = '{voucher_amt}'
					FROM SAQRIT (NOLOCK) WHERE QUOTE_RECORD_ID = '{quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_rec_id}' AND SERVICE_ID = 'Z0117' AND GREENBOOK = '{grnbok}' """.format(quote_rec_id = get_rev_rec_id.MASTER_TABLE_QUOTE_RECORD_ID ,quote_revision_rec_id = get_rev_rec_id.QTEREV_RECORD_ID,voucher_amt = get_voucher_value,grnbok = record.GREENBOOK  ))
					
			Sql.RunQuery("""UPDATE SAQRIT SET YEAR_2 = CNTPRI_INGL_CURR ,YEAR_2_INGL_CURR = CNTPRI_INGL_CURR FROM SAQRIT (NOLOCK) INNER JOIN SAQICO ON SAQRIT.QUOTE_RECORD_ID = SAQICO.QUOTE_RECORD_ID AND SAQRIT.QTEREV_RECORD_ID = SAQICO.QTEREV_RECORD_ID AND  SAQRIT.SERVICE_ID = SAQICO.SERVICE_ID AND SAQRIT.GREENBOOK = SAQICO.GREENBOOK AND YEAR = 'YEAR 2' WHERE  SAQRIT.QUOTE_RECORD_ID = '{quote_rec_id}' AND SAQRIT.QTEREV_RECORD_ID = '{quote_revision_rec_id}' AND SAQRIT.SERVICE_ID = 'Z0117' AND YEAR = 'YEAR 2' """.format(quote_rec_id = get_rev_rec_id.MASTER_TABLE_QUOTE_RECORD_ID ,quote_revision_rec_id = get_rev_rec_id.QTEREV_RECORD_ID,voucher_amt = get_voucher_value  ))

			Sql.RunQuery("""UPDATE SAQRIT SET YEAR_3 = CNTPRI_INGL_CURR ,YEAR_3_INGL_CURR = CNTPRI_INGL_CURR FROM SAQRIT (NOLOCK) INNER JOIN SAQICO ON SAQRIT.QUOTE_RECORD_ID = SAQICO.QUOTE_RECORD_ID AND SAQRIT.QTEREV_RECORD_ID = SAQICO.QTEREV_RECORD_ID AND  SAQRIT.SERVICE_ID = SAQICO.SERVICE_ID AND SAQRIT.GREENBOOK = SAQICO.GREENBOOK AND YEAR = 'YEAR 3' WHERE  SAQRIT.QUOTE_RECORD_ID = '{quote_rec_id}' AND SAQRIT.QTEREV_RECORD_ID = '{quote_revision_rec_id}' AND SAQRIT.SERVICE_ID = 'Z0117'  AND YEAR = 'YEAR 3' """.format(quote_rec_id = get_rev_rec_id.MASTER_TABLE_QUOTE_RECORD_ID ,quote_revision_rec_id = get_rev_rec_id.QTEREV_RECORD_ID,voucher_amt = get_voucher_value  ))

			Sql.RunQuery("""UPDATE SAQRIT SET YEAR_4 = CNTPRI_INGL_CURR ,YEAR_4_INGL_CURR = CNTPRI_INGL_CURR FROM SAQRIT (NOLOCK) INNER JOIN SAQICO ON SAQRIT.QUOTE_RECORD_ID = SAQICO.QUOTE_RECORD_ID AND SAQRIT.QTEREV_RECORD_ID = SAQICO.QTEREV_RECORD_ID AND  SAQRIT.SERVICE_ID = SAQICO.SERVICE_ID AND SAQRIT.GREENBOOK = SAQICO.GREENBOOK AND YEAR = 'YEAR 4' WHERE  SAQRIT.QUOTE_RECORD_ID = '{quote_rec_id}' AND SAQRIT.QTEREV_RECORD_ID = '{quote_revision_rec_id}' AND SAQRIT.SERVICE_ID = 'Z0117'  AND YEAR = 'YEAR 4' """.format(quote_rec_id = get_rev_rec_id.MASTER_TABLE_QUOTE_RECORD_ID ,quote_revision_rec_id = get_rev_rec_id.QTEREV_RECORD_ID,voucher_amt = get_voucher_value  ))

			Sql.RunQuery("""UPDATE SAQRIT SET YEAR_5 = CNTPRI_INGL_CURR ,YEAR_5_INGL_CURR = CNTPRI_INGL_CURR FROM SAQRIT (NOLOCK) INNER JOIN SAQICO ON SAQRIT.QUOTE_RECORD_ID = SAQICO.QUOTE_RECORD_ID AND SAQRIT.QTEREV_RECORD_ID = SAQICO.QTEREV_RECORD_ID AND  SAQRIT.SERVICE_ID = SAQICO.SERVICE_ID AND SAQRIT.GREENBOOK = SAQICO.GREENBOOK AND YEAR = 'YEAR 5' WHERE  SAQRIT.QUOTE_RECORD_ID = '{quote_rec_id}' AND SAQRIT.QTEREV_RECORD_ID = '{quote_revision_rec_id}' AND SAQRIT.SERVICE_ID = 'Z0117'  AND YEAR = 'YEAR 5' """.format(quote_rec_id = get_rev_rec_id.MASTER_TABLE_QUOTE_RECORD_ID ,quote_revision_rec_id = get_rev_rec_id.QTEREV_RECORD_ID,voucher_amt = get_voucher_value ))

			Sql.RunQuery("""UPDATE SAQRIT SET
						NET_PRICE = ISNULL(YEAR_1,0) + ISNULL(YEAR_2,0) + ISNULL(YEAR_3,0) + ISNULL(YEAR_4,0) + ISNULL(YEAR_5,0), 
						NET_PRICE_INGL_CURR = ISNULL(YEAR_1_INGL_CURR,0) + ISNULL(YEAR_2_INGL_CURR,0) + ISNULL(YEAR_3_INGL_CURR,0) + ISNULL(YEAR_4_INGL_CURR,0) + ISNULL(YEAR_5_INGL_CURR,0)
					FROM SAQRIT (NOLOCK) WHERE QUOTE_RECORD_ID = '{quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_rec_id}' AND SERVICE_ID = 'Z0117'  """.format(quote_rec_id = get_rev_rec_id.MASTER_TABLE_QUOTE_RECORD_ID ,quote_revision_rec_id = get_rev_rec_id.QTEREV_RECORD_ID,voucher_amt = get_voucher_value  ))
			
			Sql.RunQuery("""UPDATE SAQRIT 
						SET STATUS = 'ACQUIRED', 
						NET_VALUE = ISNULL(NET_PRICE, 0) + ISNULL(TAX_AMOUNT,0), 
						NET_VALUE_INGL_CURR =ISNULL(NET_PRICE_INGL_CURR, 0) + ISNULL(TAX_AMOUNT, 0)
					FROM SAQRIT (NOLOCK) WHERE QUOTE_RECORD_ID = '{quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_rec_id}' AND SERVICE_ID = 'Z0117'  """.format(quote_rec_id = get_rev_rec_id.MASTER_TABLE_QUOTE_RECORD_ID ,quote_revision_rec_id = get_rev_rec_id.QTEREV_RECORD_ID,voucher_amt = get_voucher_value ))



	except:
		Log.Info("error in voucher")

def quoteitemupdate(Qt_id):
    delete_saqris = Sql.RunQuery("DELETE FROM SAQRIS WHERE QUOTE_ID = '{}'".format(Qt_id))
    delete_saqrit = Sql.RunQuery("DELETE FROM SAQRIT WHERE QUOTE_ID = '{}'".format(Qt_id))
    delete_saqico = Sql.RunQuery("DELETE FROM SAQICO WHERE QUOTE_ID = '{}'".format(Qt_id))
    update_saqtrv = Sql.RunQuery("UPDATE SAQTRV SET NET_PRICE_INGL_CURR=NULL, NET_VALUE_INGL_CURR=NULL WHERE QUOTE_ID = '{}'".format(Qt_id))
    
try: 
	Qt_id = Param.QT_REC_ID
except:
	Qt_id = ""
try:
   	Action = Param.Operation
except:
	Action= ""

try:
	if Action == 'Delete':
		calling_function = quoteitemupdate(Qt_id)
	elif  Action == 'VOUCHER_UPDATE':
		voucher_amt_update(Qt_id)
	else:    
		voucher_amt_update(Qt_id)
		calling_function = quoteiteminsert(Qt_id)
	
except Exception as e:
	Log.Info('pricing error-'+str(e))

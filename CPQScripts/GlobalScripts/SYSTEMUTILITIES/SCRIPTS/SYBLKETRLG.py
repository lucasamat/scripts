# =========================================================================================================================================
#   __script_name : SYBLKETRLG.PY
#   __script_description : THIS SCRIPT IS USED FOR BULK EDITING RECORDS IN A RELATED LIST.
#   __primary_author__ : JOE EBENEZER
#   __create_date :
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import datetime
import System.Net
import Webcom.Configurator.Scripting.Test.TestProduct
import SYTABACTIN as Table
import SYCNGEGUID as CPQID
from SYDATABASE import SQL
import re

Sql = SQL()
ContractRecordId = sqlforupdatePT = ""
try:
	ContractRecordId = Quote.GetGlobal("contract_quote_record_id")
except:
	ContractRecordId = ""
try:	
	Qt_rec_id = Quote.GetGlobal("contract_quote_record_id")
except:
	Qt_rec_id = ""

userId = str(User.Id)
userName = str(User.UserName)

try:
	GetActiveRevision = Sql.GetFirst("SELECT QUOTE_REVISION_RECORD_ID,QTEREV_ID FROM SAQTRV (NOLOCK) WHERE QUOTE_ID ='{}' AND ACTIVE = 1".format(Quote.CompositeNumber))
except:
	Trace.Write("EXCEPT: GetActiveRevision ")
	GetActiveRevision = ""
if GetActiveRevision:
	qt_rev_id = str(GetActiveRevision.QUOTE_REVISION_RECORD_ID)


def insert_items_billing_plan(total_months=1, billing_date='',billing_end_date ='', amount_column='YEAR_1', entitlement_obj=None,service_id=None,get_ent_val_type =None,get_ent_billing_type_value=None,get_billling_data_dict=None):
	contract_quote_rec_id = ContractRecordId
	quote_revision_rec_id = qt_rev_id
	user_id = str(User.Id)
	userName = str(User.UserName)	
	Trace.Write('104----')
	get_val =get_billing_cycle = get_billing_type = ''
	#Trace.Write(str(service_id)+'--get_billling_data_dict--'+str(get_billling_data_dict))
	Trace.Write(str(service_id)+'get_ent_val_type--'+str(get_ent_val_type))
	for data,val in get_billling_data_dict.items():
		if 'AGS_'+str(service_id)+'_PQB_BILCYC' in data:
			get_billing_cycle = val
		elif 'AGS_'+str(service_id)+'_PQB_BILTYP' in data:
			get_billing_type =val
	#Trace.Write('get_billing_cycle---'+str(get_billing_cycle))
	Trace.Write(str(service_id)+'----billing_type---'+str(get_billing_type)+'--CYCLE---'+str(get_billing_cycle))
	if get_billing_cycle == "Monthly":
		year = int(amount_column.split('_')[-1])
		remaining_months = (total_months + 1) - (year*12)		
		divide_by = 12
		
		if remaining_months < 0:
			divide_by = 12 + remaining_months
		get_val =12
	elif str(get_billing_cycle).upper() == "QUARTERLY":
		year = int(amount_column.split('_')[-1])
		remaining_months = (total_months) - (year*12)		
		divide_by = 12
		
		if remaining_months < 0:
			divide_by = 12 + remaining_months
		get_val = 4
	elif str(get_billing_cycle).upper() == "ANNUALLY":
		year = int(amount_column.split('_')[-1])
		remaining_months = (total_months + 1) - (year*12)		
		divide_by = 12
		
		if remaining_months < 0:
			divide_by = 12 + remaining_months
		get_val = 1
	else:
		year = int(amount_column.split('_')[-1])
		remaining_months = (total_months + 1) - (year*12)		
		divide_by = 12
		
		if remaining_months < 0:
			divide_by = 12 + remaining_months
		get_val =12
	#amount_column = 'TOTAL_AMOUNT_INGL_CURR' # Hard Coded for Sprint 5
	object_name = join_condition = ''
	if str(get_billing_type).upper() == "FIXED":
		#join_condition = "JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID and SAQRIT.QTEREV_RECORD_ID=SAQSCO.QTEREV_RECORD_ID  and SAQRIT.SERVICE_ID = SAQSCO.SERVICE_ID and SAQRIT.OBJECT_ID = SAQSCO.EQUIPMENT_ID and SAQSCO.GREENBOOK = SAQRIT.GREENBOOK"
		#object_name = 'SAQSCO'
		#divide_amt = 'SAQRIT.NET_PRICE_INGL_CURR'
		#annaul_bill_amt = 'SAQRIT.NET_PRICE_INGL_CURR'
		Trace.Write(str(service_id)+'------billing_type_value-----'+str(get_ent_billing_type_value))
		Sql.RunQuery(""" INSERT SAQIBP (

					QUOTE_ITEM_BILLING_PLAN_RECORD_ID, BILLING_END_DATE, BILLING_START_DATE,ANNUAL_BILLING_AMOUNT,BILLING_VALUE, BILLING_VALUE_INGL_CURR,BILLING_TYPE,LINE, QUOTE_ID, QTEITM_RECORD_ID,COMMITTED_VALUE_INGL_CURR,ESTVAL_INGL_CURR,
					QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,
					BILLING_DATE, BILLING_YEAR,
					EQUIPMENT_DESCRIPTION, EQUIPMENT_ID, EQUIPMENT_RECORD_ID, QTEITMCOB_RECORD_ID,
					SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID, SERIAL_NUMBER, WARRANTY_START_DATE, WARRANTY_END_DATE,CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED
					)
					SELECT
					CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_BILLING_PLAN_RECORD_ID,A.* from (SELECT DISTINCT  
					{billing_end_date} as BILLING_END_DATE,
					{BillingDate} as BILLING_START_DATE,
					ISNULL(SAQRIT.NET_PRICE_INGL_CURR, 0)  AS ANNUAL_BILLING_AMOUNT,
					ISNULL(SAQRIT.NET_PRICE, 0) / {get_val}  as BILLING_VALUE,
					ISNULL(SAQRIT.ESTVAL_INGL_CURR, 0) / {get_val}  as  BILLING_VALUE_INGL_CURR,
					'{billing_type}' as BILLING_TYPE,
					SAQRIT.LINE AS LINE,
					SAQSCO.QUOTE_ID,
					SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID,
					SAQRIT.COMVAL_INGL_CURR as COMMITTED_VALUE_INGL_CURR,
					SAQRIT.ESTVAL_INGL_CURR as ESTVAL_INGL_CURR,
					SAQSCO.QUOTE_RECORD_ID,
					SAQSCO.QTEREV_ID,
					SAQSCO.QTEREV_RECORD_ID,
					{BillingDate} as BILLING_DATE,
					0 as BILLING_YEAR,
					SAQSCO.EQUIPMENT_DESCRIPTION,
					SAQSCO.EQUIPMENT_ID,
					SAQSCO.EQUIPMENT_RECORD_ID,
					'' as QTEITMCOB_RECORD_ID,
					SAQSCO.SERVICE_DESCRIPTION,
					SAQSCO.SERVICE_ID,
					SAQSCO.SERVICE_RECORD_ID,
					SAQSCO.GREENBOOK,
					SAQSCO.GREENBOOK_RECORD_ID,
					SAQSCO.SERIAL_NO AS SERIAL_NUMBER,
					SAQSCO.WARRANTY_START_DATE,
					SAQSCO.WARRANTY_END_DATE,    
					{UserId} as CPQTABLEENTRYADDEDBY,
					GETDATE() as CPQTABLEENTRYDATEADDED
					FROM SAQSCO (NOLOCK) JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID and SAQRIT.QTEREV_RECORD_ID=SAQSCO.QTEREV_RECORD_ID  and SAQRIT.SERVICE_ID = SAQSCO.SERVICE_ID and SAQRIT.OBJECT_ID = SAQSCO.EQUIPMENT_ID and SAQSCO.GREENBOOK = SAQRIT.GREENBOOK LEFT JOIN SAQIBP (NOLOCK) on SAQRIT.QUOTE_RECORD_ID = SAQIBP.QUOTE_RECORD_ID and SAQRIT.QTEREV_RECORD_ID=SAQIBP.QTEREV_RECORD_ID  and SAQRIT.SERVICE_ID = SAQIBP.SERVICE_ID AND
					EXISTS (SELECT * FROM  SAQIBP (NOLOCK) WHERE SAQIBP.ANNUAL_BILLING_AMOUNT <> SAQRIT.NET_PRICE AND SAQRIT.QUOTE_RECORD_ID = SAQIBP.QUOTE_RECORD_ID and SAQRIT.QTEREV_RECORD_ID=SAQIBP.QTEREV_RECORD_ID  and SAQRIT.SERVICE_ID = SAQIBP.SERVICE_ID)
					WHERE SAQSCO.QUOTE_RECORD_ID='{QuoteRecordId}' AND SAQSCO.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQSCO.SERVICE_ID ='{service_id}'  and SAQRIT.NET_PRICE > 0 and ISNULL(SAQRIT.OBJECT_ID,'') <> 0 )A """.format(
					UserId=user_id, QuoteRecordId=ContractRecordId,
					RevisionRecordId=quote_revision_rec_id,
					BillingDate=billing_date,billing_end_date=billing_end_date,
					get_val=get_val,
					service_id = service_id,billing_type =get_billing_type))
		Sql.RunQuery(""" INSERT SAQIBP (

					QUOTE_ITEM_BILLING_PLAN_RECORD_ID, BILLING_END_DATE, BILLING_START_DATE,ANNUAL_BILLING_AMOUNT,BILLING_VALUE, BILLING_VALUE_INGL_CURR,BILLING_TYPE,LINE, QUOTE_ID, QTEITM_RECORD_ID,COMMITTED_VALUE_INGL_CURR,ESTVAL_INGL_CURR,
					QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,
					BILLING_DATE, BILLING_YEAR,
					EQUIPMENT_DESCRIPTION, EQUIPMENT_ID, EQUIPMENT_RECORD_ID, QTEITMCOB_RECORD_ID,
					SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID, SERIAL_NUMBER, WARRANTY_START_DATE, WARRANTY_END_DATE,CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED
					)
					SELECT
					CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_BILLING_PLAN_RECORD_ID,A.* from (SELECT DISTINCT  
					{billing_end_date} as BILLING_END_DATE,
					{BillingDate} as BILLING_START_DATE,
					SAQRIT.NET_PRICE_INGL_CURR AS ANNUAL_BILLING_AMOUNT,
					ISNULL(SAQRIT.NET_PRICE, 0) / {get_val}  as BILLING_VALUE,
					ISNULL(SAQRIT.ESTVAL_INGL_CURR, 0) / {get_val}  as  BILLING_VALUE_INGL_CURR,
					'{billing_type}' as BILLING_TYPE,
					SAQRIT.LINE AS LINE,
					SAQRIT.QUOTE_ID,
					SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID,
					SAQRIT.COMVAL_INGL_CURR as COMMITTED_VALUE_INGL_CURR,
					SAQRIT.ESTVAL_INGL_CURR as ESTVAL_INGL_CURR,
					SAQRIT.QUOTE_RECORD_ID,
					SAQRIT.QTEREV_ID,
					SAQRIT.QTEREV_RECORD_ID,
					{BillingDate} as BILLING_DATE,
					0 as BILLING_YEAR,
					'' as EQUIPMENT_DESCRIPTION,
					SAQRIT.OBJECT_ID as EQUIPMENT_ID,
					'' as EQUIPMENT_RECORD_ID,
					'' as QTEITMCOB_RECORD_ID,
					SAQRIT.SERVICE_DESCRIPTION,
					SAQRIT.SERVICE_ID,
					SAQRIT.SERVICE_RECORD_ID,
					SAQRIT.GREENBOOK,
					SAQRIT.GREENBOOK_RECORD_ID,
					'' AS SERIAL_NUMBER,
					'' as WARRANTY_START_DATE,
					'' as WARRANTY_END_DATE,    
					{UserId} as CPQTABLEENTRYADDEDBY,
					GETDATE() as CPQTABLEENTRYDATEADDED
					FROM SAQRIT (NOLOCK)  LEFT JOIN SAQIBP (NOLOCK) on SAQRIT.QUOTE_RECORD_ID = SAQIBP.QUOTE_RECORD_ID and SAQRIT.QTEREV_RECORD_ID=SAQIBP.QTEREV_RECORD_ID  and SAQRIT.SERVICE_ID = SAQIBP.SERVICE_ID AND
					EXISTS (SELECT * FROM  SAQIBP (NOLOCK) WHERE SAQIBP.ANNUAL_BILLING_AMOUNT <> SAQRIT.NET_PRICE AND SAQRIT.QUOTE_RECORD_ID = SAQIBP.QUOTE_RECORD_ID and SAQRIT.QTEREV_RECORD_ID=SAQIBP.QTEREV_RECORD_ID  and SAQRIT.SERVICE_ID = SAQIBP.SERVICE_ID)
					WHERE SAQRIT.QUOTE_RECORD_ID='{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQRIT.SERVICE_ID ='{service_id}'  and SAQRIT.NET_PRICE > 0   and ISNULL(SAQRIT.OBJECT_ID,'') = '' )A """.format(
					UserId=user_id, QuoteRecordId=ContractRecordId,
					RevisionRecordId=quote_revision_rec_id,billing_end_date=billing_end_date,
					BillingDate=billing_date,
					get_val=get_val,
					service_id = service_id,billing_type =get_billing_type))
	else:
		
		Sql.RunQuery("""INSERT SAQIBP (
					
					QUOTE_ITEM_BILLING_PLAN_RECORD_ID, BILLING_END_DATE, BILLING_START_DATE,ANNUAL_BILLING_AMOUNT,BILLING_VALUE, BILLING_VALUE_INGL_CURR,BILLING_TYPE,LINE, QUOTE_ID, QTEITM_RECORD_ID,COMMITTED_VALUE_INGL_CURR,ESTVAL_INGL_CURR,
					QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,
					BILLING_DATE, BILLING_YEAR,
					EQUIPMENT_DESCRIPTION, EQUIPMENT_ID, EQUIPMENT_RECORD_ID, QTEITMCOB_RECORD_ID, 
					SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID, SERIAL_NUMBER, WARRANTY_START_DATE, WARRANTY_END_DATE,CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED
				) 
				SELECT 
					CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_BILLING_PLAN_RECORD_ID,A.* from (SELECT DISTINCT  
					{billing_end_date} as BILLING_END_DATE,
					{BillingDate} as BILLING_START_DATE,
					SAQRIT.NET_PRICE_INGL_CURR AS ANNUAL_BILLING_AMOUNT,
					ISNULL(SAQRIT.NET_PRICE, 0) / {get_val}  as BILLING_VALUE,
					ISNULL(SAQRIT.ESTVAL_INGL_CURR, 0) / {get_val}  as  BILLING_VALUE_INGL_CURR,
					'{billing_type}' as BILLING_TYPE,
					SAQRIT.LINE AS LINE,
					SAQSCO.QUOTE_ID,
					SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID,	
					SAQRIT.COMVAL_INGL_CURR	 as COMMITTED_VALUE_INGL_CURR,
					SAQRIT.ESTVAL_INGL_CURR	as 	ESTVAL_INGL_CURR,		
					SAQSCO.QUOTE_RECORD_ID,
					SAQSCO.QTEREV_ID,
					SAQSCO.QTEREV_RECORD_ID,
					{BillingDate} as BILLING_DATE,						
					0 as BILLING_YEAR,
					SAQSCO.EQUIPMENT_DESCRIPTION,
					SAQSCO.EQUIPMENT_ID,									
					SAQSCO.EQUIPMENT_RECORD_ID,						
					'' as QTEITMCOB_RECORD_ID,
					SAQSCO.SERVICE_DESCRIPTION,
					SAQSCO.SERVICE_ID,
					SAQSCO.SERVICE_RECORD_ID, 
					SAQSCO.GREENBOOK,
					SAQSCO.GREENBOOK_RECORD_ID,
					SAQSCO.SERIAL_NO AS SERIAL_NUMBER,
					SAQSCO.WARRANTY_START_DATE,
					SAQSCO.WARRANTY_END_DATE,    
					{UserId} as CPQTABLEENTRYADDEDBY, 
					GETDATE() as CPQTABLEENTRYDATEADDED
					FROM SAQSCO (NOLOCK) JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID and SAQRIT.QTEREV_RECORD_ID=SAQSCO.QTEREV_RECORD_ID  and SAQRIT.SERVICE_ID = SAQSCO.SERVICE_ID and SAQRIT.OBJECT_ID = SAQSCO.EQUIPMENT_ID and SAQSCO.GREENBOOK = SAQRIT.GREENBOOK LEFT JOIN SAQIBP (NOLOCK) on SAQRIT.QUOTE_RECORD_ID = SAQIBP.QUOTE_RECORD_ID and SAQRIT.QTEREV_RECORD_ID=SAQIBP.QTEREV_RECORD_ID  and SAQRIT.SERVICE_ID = SAQIBP.SERVICE_ID AND
					EXISTS (SELECT * FROM  SAQIBP (NOLOCK) WHERE SAQIBP.ANNUAL_BILLING_AMOUNT <> SAQRIT.NET_PRICE AND SAQRIT.QUOTE_RECORD_ID = SAQIBP.QUOTE_RECORD_ID and SAQRIT.QTEREV_RECORD_ID=SAQIBP.QTEREV_RECORD_ID  and SAQRIT.SERVICE_ID = SAQIBP.SERVICE_ID)
					WHERE SAQSCO.QUOTE_RECORD_ID='{QuoteRecordId}' AND SAQSCO.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQSCO.SERVICE_ID ='{service_id}'   and SAQRIT.NET_PRICE > 0  and ISNULL(SAQRIT.OBJECT_ID,'') <> 0 )A """.format(
					UserId=user_id, QuoteRecordId=contract_quote_rec_id,
					RevisionRecordId=quote_revision_rec_id,billing_end_date=billing_end_date,
					BillingDate=billing_date,
					get_val=get_val,
					service_id = service_id,billing_type =get_billing_type))
		Sql.RunQuery("""INSERT SAQIBP (
					
					QUOTE_ITEM_BILLING_PLAN_RECORD_ID, BILLING_END_DATE, BILLING_START_DATE,ANNUAL_BILLING_AMOUNT,BILLING_VALUE, BILLING_VALUE_INGL_CURR,BILLING_TYPE,LINE, QUOTE_ID, QTEITM_RECORD_ID, COMMITTED_VALUE_INGL_CURR,ESTVAL_INGL_CURR,
					QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,
					BILLING_DATE, BILLING_YEAR,
					EQUIPMENT_DESCRIPTION, EQUIPMENT_ID, EQUIPMENT_RECORD_ID, QTEITMCOB_RECORD_ID, 
					SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID, SERIAL_NUMBER, WARRANTY_START_DATE, WARRANTY_END_DATE,CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED
				) 
				SELECT 
					CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_BILLING_PLAN_RECORD_ID,  
					{billing_end_date} as BILLING_END_DATE,
					{BillingDate} as BILLING_START_DATE,
					NET_PRICE_INGL_CURR AS ANNUAL_BILLING_AMOUNT,
					ISNULL(NET_PRICE, 0) / {get_val}  as BILLING_VALUE,
					ISNULL(NET_PRICE_INGL_CURR, 0) / {get_val}  as  BILLING_VALUE_INGL_CURR,
					'{billing_type}' as BILLING_TYPE,
					LINE,
					QUOTE_ID,
					QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID,
					
					COMVAL_INGL_CURR	 as COMMITTED_VALUE_INGL_CURR,
					ESTVAL_INGL_CURR	as 	ESTVAL_INGL_CURR,								
					QUOTE_RECORD_ID,
					QTEREV_ID,
					QTEREV_RECORD_ID,
					{BillingDate} as BILLING_DATE,						
					0 as BILLING_YEAR,
					'' as EQUIPMENT_DESCRIPTION,
					'' as EQUIPMENT_ID,									
					'' as EQUIPMENT_RECORD_ID,						
					'' as QTEITMCOB_RECORD_ID,
					SERVICE_DESCRIPTION,
					SERVICE_ID,
					SERVICE_RECORD_ID, 
					GREENBOOK,
					GREENBOOK_RECORD_ID,
					'' AS SERIAL_NUMBER,
					'' as WARRANTY_START_DATE,
					'' as WARRANTY_END_DATE,    
					{UserId} as CPQTABLEENTRYADDEDBY, 
					GETDATE() as CPQTABLEENTRYDATEADDED
				FROM  SAQRIT (NOLOCK) 
				WHERE QUOTE_RECORD_ID='{QuoteRecordId}' AND  NET_PRICE > 0 AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID ='{service_id}' AND (OBJECT_ID  IS NULL OR OBJECT_ID = '')""".format(
					UserId=user_id, QuoteRecordId=contract_quote_rec_id,
					RevisionRecordId=quote_revision_rec_id,
					BillingDate=billing_date,billing_end_date=billing_end_date,
					get_val=get_val,
					service_id = service_id,billing_type =get_billing_type))
	
	return True



def getting_cps_tax(quote_id = None,quote_record_id = None,item_lines_record_ids=None):		
	Log.Info("getting_cps_tax function"+str(item_lines_record_ids))
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
	GetPricingProcedure = Sql.GetFirst("SELECT ISNULL(DIVISION_ID, '') as DIVISION_ID, ISNULL(DISTRIBUTIONCHANNEL_ID, '') as DISTRIBUTIONCHANNEL_ID, ISNULL(SALESORG_ID, '') as SALESORG_ID, ISNULL(DOC_CURRENCY,'') as DOC_CURRENCY, ISNULL(PRICINGPROCEDURE_ID,'') as PRICINGPROCEDURE_ID, QUOTE_RECORD_ID FROM SAQTRV (NOLOCK) WHERE QUOTE_ID = '{}'".format(quote_id))
	if GetPricingProcedure is not None:			
		PricingProcedure = GetPricingProcedure.PRICINGPROCEDURE_ID
		curr = GetPricingProcedure.DOC_CURRENCY
		dis = GetPricingProcedure.DISTRIBUTIONCHANNEL_ID
		salesorg = GetPricingProcedure.SALESORG_ID
		div = GetPricingProcedure.DIVISION_ID
		exch = GetPricingProcedure.EXCHANGE_RATE_TYPE
		taxk1 = GetPricingProcedure.CUSTAXCLA_ID

	#update_SAQITM = "UPDATE SAQITM SET PRICINGPROCEDURE_ID = '{prc}' WHERE SAQITM.QUOTE_ID = '{quote}'".format(prc=str(PricingProcedure), quote=self.contract_quote_id)
	#Sql.RunQuery(update_SAQITM)		
	
	STPObj=Sql.GetFirst("SELECT ACCOUNT_ID FROM SAOPQT (NOLOCK) WHERE QUOTE_ID ='{quote}'".format(quote=quote_id))		
	stp_account_id = ""
	if STPObj:
		stp_account_id = str(STPObj.ACCOUNT_ID)
	if item_lines_record_ids:		
		Log.Info("getting_cps_tax function item_lines_record_ids")	
		items_data = []
		item_line_record_ids_str = "','".join([item_line_record_id for item_line_record_id in item_lines_record_ids])
		item_lines_obj = Sql.GetList("SELECT * FROM SAQICO (NOLOCK) WHERE QUOTE_ITEM_COVERED_OBJECT_RECORD_ID IN ('{item_line_record_ids_str}')".format(item_line_record_ids_str = item_line_record_ids_str))
		if item_lines_obj:
			Log.Info("getting_cps_tax function item_lines_obj")	
			for item_line_obj in item_lines_obj:
				itemid = str(item_line_obj.EQUIPMENT_ID)+";"+str(quote_id)+";"+str(1)
				item_string = '{"itemId":"'+str(itemid)+'","externalId":null,"quantity":{"value":'+str(1)+',"unit":"EA"},"exchRateType":"'+str(exch)+'","exchRateDate":"'+str(y[0])+'","productDetails":{"productId":"'+str(item_line_obj.EQUIPMENT_ID)+'","baseUnit":"EA","alternateProductUnits":null},"attributes":[{"name":"KOMK-LAND1","values":["CN"]},{"name":"KOMK-ALAND","values":["CN"]},{"name":"KOMK-REGIO","values":["TX"]},{"name":"KOMK-KUNNR","values":["'+stp_account_id+'"]},{"name":"KOMK-KUNWE","values":["'+stp_account_id+'"]},{"name":"KOMP-TAXM1","values":["'+str(item_line_obj.SRVTAXCLA_ID)+'"]},{"name":"KOMK-TAXK1","values":["'+str(taxk1)+'"]},{"name":"KOMK-SPART","values":["'+str(div)+'"]},{"name":"KOMP-SPART","values":["'+str(div)+'"]},{"name":"KOMP-PMATN","values":["'+str(item_line_obj.EQUIPMENT_ID)+'"]},{"name":"KOMK-WAERK","values":["'+str(curr)+'"]},{"name":"KOMK-HWAER","values":["'+str(curr)+'"]},{"name":"KOMP-PRSFD","values":["X"]},{"name":"KOMK-VTWEG","values":["'+str(dis)+'"]},{"name":"KOMK-VKORG","values":["'+str(salesorg)+'"]},{"name":"KOMP-KPOSN","values":["0"]},{"name":"KOMP-KZNEP","values":[""]},{"name":"KOMP-ZZEXE","values":["true"]}],"accessDateList":[{"name":"KOMK-PRSDT","value":"'+str(y[0])+'"},{"name":"KOMK-FBUDA","value":"'+str(y[0])+'"}],"variantConditions":[],"statistical":true,"subItems":[]}'
				items_data.append(item_string)
			items_string = ','.join(items_data)
			requestdata = '{"docCurrency":"'+curr+'","locCurrency":"'+curr+'","pricingProcedure":"'+PricingProcedure+'","groupCondition":false,"itemConditionsRequired":true,"items": ['+str(items_string)+']}'
			Log.Info("requestdata-----",requestdata)
			response1 = webclient.UploadString(Request_URL,str(requestdata))			
			response1 = str(response1).replace(": true", ': "true"').replace(": false", ': "false"').replace(": null",': " None"')
			response1 = eval(response1)
			price = []
			for root, value in response1.items():
				if root == "items":
					price = value[:]
					break
			update_data = []
			batch_group_record_id = str(Guid.NewGuid()).upper()
			for data in price:
				equipment_id = str(data["itemId"]).split(";")[0]
				tax_percentage = 0
				for condition_obj in data['conditions']:
					if condition_obj['conditionType'] == 'ZWSC' and condition_obj['conditionTypeDescription'] == 'VAT Asia':
						tax_percentage = condition_obj['conditionRate']
						break
				update_data.append((str(Guid.NewGuid()).upper(), equipment_id, 1, 'IN PROGRESS', quote_id, quote_record_id, batch_group_record_id, tax_percentage))
			
			update_data_joined = ', '.join(map(str, update_data))
			Sql.RunQuery("""INSERT INTO SYSPBT(BATCH_RECORD_ID, SAP_PART_NUMBER, QUANTITY, BATCH_STATUS, QUOTE_ID, QUOTE_RECORD_ID, BATCH_GROUP_RECORD_ID, TAX_PERCENTAGE) 
									SELECT * FROM (VALUES {}) QS (BATCH_RECORD_ID, SAP_PART_NUMBER, QUANTITY, BATCH_STATUS, QUOTE_ID, QUOTE_RECORD_ID, BATCH_GROUP_RECORD_ID, TAX_PERCENTAGE)""".format(update_data_joined))
			#commented the query because of removing the api_name TAX_PERCENTAGE from SAQICO - start																
			# Sql.RunQuery("""UPDATE SAQICO
			# 		SET
			# 		SAQICO.TAX_PERCENTAGE = IQ.TAX_PERCENTAGE
			# 		FROM SAQICO
			# 		INNER JOIN (
			# 			SELECT SAQICO.CpqTableEntryId, SYSPBT.TAX_PERCENTAGE
			# 			FROM SYSPBT (NOLOCK) 
			# 			JOIN SAQICO (NOLOCK) ON SAQICO.QUOTE_RECORD_ID = SYSPBT.QUOTE_RECORD_ID AND SAQICO.EQUIPMENT_ID = SYSPBT.SAP_PART_NUMBER						
			# 			WHERE SYSPBT.QUOTE_RECORD_ID ='{QuoteRecordId}' AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}' AND SYSPBT.BATCH_STATUS = 'IN PROGRESS'								
			# 		)AS IQ
			# 		ON SAQICO.CpqTableEntryId = IQ.CpqTableEntryId""".format(BatchGroupRecordId=batch_group_record_id, QuoteRecordId=quote_record_id))

			# Sql.RunQuery(
			# 		"""DELETE FROM SYSPBT WHERE SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}' and SYSPBT.BATCH_STATUS = 'IN PROGRESS'""".format(
			# 			BatchGroupRecordId=batch_group_record_id
			# 		)
			# 	)
			#commented the query because of removing the api_name TAX_PERCENTAGE from SAQICO - end	
			#update TAX column  and Extended price for each SAQICO records
			'''QueryStatement ="""UPDATE a SET a.TAX = CASE WHEN a.TAX_PERCENTAGE > 0 THEN (ISNULL(a.YEAR_1, 0)+ISNULL(a.YEAR_2, 0)+ISNULL(a.YEAR_3, 0)+ISNULL(a.YEAR_4, 0)+ISNULL(a.YEAR_5, 0)) * (a.TAX_PERCENTAGE/100) ELSE a.TAX_PERCENTAGE END FROM SAQICO a INNER JOIN SAQICO b on a.EQUIPMENT_ID = b.EQUIPMENT_ID and a.QUOTE_ID = b.QUOTE_ID where a.QUOTE_RECORD_ID = '{QuoteRecordId}' and a.QUOTE_ITEM_COVERED_OBJECT_RECORD_ID IN ('{item_line_record_ids_str}') """.format(			
			item_line_record_ids_str = item_line_record_ids_str,
			QuoteRecordId=Quote.GetGlobal("contract_quote_record_id"),
			)
			Sql.RunQuery(QueryStatement)
			QueryStatement ="""UPDATE a SET a.EXTENDED_PRICE = CASE WHEN a.TAX > 0 THEN (ISNULL(a.YEAR_1, 0)+ISNULL(a.YEAR_2, 0)+ISNULL(a.YEAR_3, 0)+ISNULL(a.YEAR_4, 0)+ISNULL(a.YEAR_5, 0)) + (a.TAX) ELSE a.TAX END FROM SAQICO a INNER JOIN SAQICO b on a.EQUIPMENT_ID = b.EQUIPMENT_ID and a.QUOTE_ID = b.QUOTE_ID where a.QUOTE_RECORD_ID = '{QuoteRecordId}' and a.QUOTE_ITEM_COVERED_OBJECT_RECORD_ID IN ('{item_line_record_ids_str}')""".format(
			QuoteRecordId=Quote.GetGlobal("contract_quote_record_id"),
			item_line_record_ids_str = item_line_record_ids_str
			)
			Sql.RunQuery(QueryStatement)'''
			#update SAQITM role up 
			# QueryStatement = """UPDATE A  SET A.EXTENDED_PRICE = B.EXTENDED_PRICE FROM SAQITM A(NOLOCK) JOIN (SELECT SUM(EXTENDED_PRICE) AS EXTENDED_PRICE,QUOTE_RECORD_ID,SERVICE_ID from SAQICO(NOLOCK) WHERE QUOTE_RECORD_ID ='{QuoteRecordId}' and QUOTE_ITEM_COVERED_OBJECT_RECORD_ID IN ('{item_line_record_ids_str}') GROUP BY QUOTE_RECORD_ID,SERVICE_ID) B ON A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.SERVICE_ID=B.SERVICE_ID """.format(			
			# item_line_record_ids_str = item_line_record_ids_str,
			# QuoteRecordId=Quote.GetGlobal("contract_quote_record_id"),
			# )
			# Sql.RunQuery(QueryStatement)
			# '''QueryStatement = """UPDATE A  SET A.TAX = B.TAX FROM SAQITM A(NOLOCK) JOIN (SELECT SUM(TAX) AS TAX,QUOTE_RECORD_ID,SERVICE_ID from SAQICO(NOLOCK) WHERE QUOTE_RECORD_ID ='{QuoteRecordId}' and QUOTE_ITEM_COVERED_OBJECT_RECORD_ID IN ('{item_line_record_ids_str}') GROUP BY QUOTE_RECORD_ID,SERVICE_ID) B ON A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.SERVICE_ID=B.SERVICE_ID """.format(		
			# item_line_record_ids_str = item_line_record_ids_str,
			# QuoteRecordId=Quote.GetGlobal("contract_quote_record_id")
			# )
			# Sql.RunQuery(QueryStatement)'''
			##Upading the quote tables for quote document
			# quote_line_items_covered_obj ="""UPDATE a SET a.TARGET_PRICE = b.TARGET_PRICE,a.YEAR_1 = b.YEAR_1,a.TAX_PERCENTAGE = b.TAX_PERCENTAGE,a.EXTENDED_PRICE = b.EXTENDED_PRICE FROM QT__SAQICO a INNER JOIN SAQICO b on a.EQUIPMENT_ID = b.EQUIPMENT_ID and a.QUOTE_RECORD_ID = b.QUOTE_RECORD_ID where a.QUOTE_RECORD_ID = '{QuoteRecordId}' """.format(QuoteRecordId= Quote.GetGlobal("contract_quote_record_id"))
			# Sql.RunQuery(quote_line_items_covered_obj)
			# quote_line_item_obj ="""UPDATE a SET aTOTAL_COST.TOTAL_COST = b.,a.TARGET_PRICE = b.TARGET_PRICE,a.YEAR_1 = b.YEAR_1,a.TAX = b.TAX,a.TAX_PERCENTAGE = b.TAX_PERCENTAGE,a.EXTENDED_PRICE = b.EXTENDED_PRICE FROM QT__SAQITM a INNER JOIN SAQITM b on a.SERVICE_ID = b.SERVICE_ID and a.QUOTE_RECORD_ID = b.QUOTE_RECORD_ID where a.QUOTE_RECORD_ID = '{QuoteRecordId}' """.format(QuoteRecordId= Quote.GetGlobal("contract_quote_record_id"))
			# Sql.RunQuery(quote_line_item_obj)
def _insert_billing_matrix():

	Sql.RunQuery("""
			INSERT SAQRIB (
			QUOTE_BILLING_PLAN_RECORD_ID,
			BILLING_END_DATE,
			BILLING_DAY,
			BILLING_START_DATE,
			QUOTE_ID,
			QUOTE_NAME,
			QUOTE_RECORD_ID,
			QTEREV_ID,
			QTEREV_RECORD_ID,
			CPQTABLEENTRYADDEDBY,
			CPQTABLEENTRYDATEADDED,
			CpqTableEntryModifiedBy,
			CpqTableEntryDateModified,
			SALESORG_ID,
			SALESORG_NAME,
			SALESORG_RECORD_ID,
			PRDOFR_ID,
			PRDOFR_RECORD_ID
			) 
			SELECT 
			CONVERT(VARCHAR(4000),NEWID()) as QUOTE_BILLING_PLAN_RECORD_ID,
			SAQTMT.CONTRACT_VALID_TO as BILLING_END_DATE,
			30 as BILLING_DAY,
			SAQTMT.CONTRACT_VALID_FROM as BILLING_START_DATE,
			SAQTMT.QUOTE_ID,
			SAQTMT.QUOTE_NAME,
			SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID as QUOTE_RECORD_ID,
			SAQTMT.QTEREV_ID as QTEREV_ID,
			SAQTMT.QTEREV_RECORD_ID as QTEREV_RECORD_ID,
			'{UserName}' AS CPQTABLEENTRYADDEDBY,
			GETDATE() as CPQTABLEENTRYDATEADDED,
			{UserId} as CpqTableEntryModifiedBy,
			GETDATE() as CpqTableEntryDateModified,
			SAQTSV.SALESORG_ID,
			SAQTSV.SALESORG_NAME,
			SAQTSV.SALESORG_RECORD_ID,
			SAQTSV.SERVICE_ID,
			SAQTSV.SERVICE_RECORD_ID                   
			FROM SAQTMT (NOLOCK) JOIN SAQTSV on SAQTSV.QUOTE_ID = SAQTMT.QUOTE_ID
			
			WHERE SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQTMT.QTEREV_RECORD_ID = '{RevisionRecordId}'
			AND SAQTSV.SERVICE_ID NOT IN ('Z0101','A6200') AND SAQTSV.SERVICE_ID NOT IN (SELECT PRDOFR_ID FROM SAQRIB (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}')
													
	""".format(                        
		QuoteRecordId= ContractRecordId,
		RevisionRecordId=qt_rev_id,
		UserId=userId,
		UserName=userName
	))
	#Not required right now for SAQTBP.
	#AND JQ.ENTITLEMENT_NAME IN ('FIXED_PRICE_PER_RESOU_EVENT_91','FIXED_PRICE_PER_RESOU_EVENT_92') 
	#AND JQ.ENTITLEMENT_VALUE_CODE = 'FIXED PRICE'
	#BM_line_item_start_time = time.time()
	billingmatrix_create()
	#BM_line_item_end_time = time.time()		
	return True	

def billingmatrix_create():
	#Trace.Write('4739---------------')
	#_quote_items_greenbook_summary_insert()
	billing_plan_obj = Sql.GetList("SELECT DISTINCT PRDOFR_ID,BILLING_START_DATE,BILLING_END_DATE,BILLING_DAY FROM SAQRIB (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(ContractRecordId,qt_rev_id))
	quotedetails = Sql.GetFirst("SELECT CONTRACT_VALID_FROM,CONTRACT_VALID_TO FROM SAQTMT (NOLOCK) WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(ContractRecordId,qt_rev_id))
	get_billling_data_dict = {}
	contract_start_date = quotedetails.CONTRACT_VALID_FROM
	contract_end_date = quotedetails.CONTRACT_VALID_TO
	get_ent_val = get_ent_bill_type = get_ent_billing_type_value = get_ent_bill_cycle = ''
	if contract_start_date and contract_end_date and billing_plan_obj:
		Sql.RunQuery("""DELETE FROM SAQIBP WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'""".format(QuoteRecordId=ContractRecordId,RevisionRecordId=qt_rev_id))
		#Trace.Write('4739---------4744------')
		for val in billing_plan_obj:
			if billing_plan_obj:				
				contract_start_date = val.BILLING_START_DATE
				contract_end_date = val.BILLING_END_DATE				
				start_date = datetime.datetime.strptime(UserPersonalizationHelper.ToUserFormat(contract_start_date), '%m/%d/%Y')
				#start_date = str(contract_start_date).split(' ')[0]
				billing_day = int(val.BILLING_DAY)
				get_service_val = val.PRDOFR_ID
				get_billing_cycle = Sql.GetFirst("select ENTITLEMENT_XML from SAQITE where QUOTE_RECORD_ID = '{qtid}' AND QTEREV_RECORD_ID = '{qt_rev_id}' and SERVICE_ID = '{get_service}'".format(qtid =ContractRecordId,qt_rev_id=qt_rev_id,get_service = str(get_service_val).strip()))
				if get_billing_cycle:
					Trace.Write('get_service_val-32--')
					updateentXML = get_billing_cycle.ENTITLEMENT_XML
					pattern_tag = re.compile(r'(<QUOTE_ITEM_ENTITLEMENT>[\w\W]*?</QUOTE_ITEM_ENTITLEMENT>)')
					pattern_id = re.compile(r'<ENTITLEMENT_ID>(AGS_'+str(get_service_val)+'_PQB_BILCYC|AGS_'+str(get_service_val)+'_PQB_BILTYP)</ENTITLEMENT_ID>')
					#pattern_id_billing_type = re.compile(r'<ENTITLEMENT_ID>(AGS_'+str(get_service_val)+'_PQB_BILTYP|AGS_'+str(get_service_val)+'_PQB_BILTYP)</ENTITLEMENT_ID>')
					pattern_name = re.compile(r'<ENTITLEMENT_DISPLAY_VALUE>([^>]*?)</ENTITLEMENT_DISPLAY_VALUE>')
					for m in re.finditer(pattern_tag, updateentXML):
						sub_string = m.group(1)
						get_ent_id = re.findall(pattern_id,sub_string)
						#get_ent_bill_type = re.findall(pattern_id_billing_type,sub_string)
						get_ent_val= re.findall(pattern_name,sub_string)
						if get_ent_id:
							get_ent_val = str(get_ent_val[0])
							get_billling_data_dict[get_ent_id[0]] = str(get_ent_val)
							#get_ent_bill_cycle = str(get_ent_val)
							for data,val in get_billling_data_dict.items():
								if 'AGS_'+str(get_service_val)+'_PQB_BILCYC' in data:
									get_ent_bill_cycle = val
								elif 'AGS_'+str(get_service_val)+'_PQB_BILTYP' in data:
									get_billing_type =val
							# if 	'AGS_'+str(get_service_val)+'_PQB_BILCYC' == str(get_ent_id[0]):
							# 	get_ent_val = str(get_ent_val)
							# 	Trace.Write(str(get_ent_val)+'---get_ent_name---'+str(get_ent_id[0]))
							# 	#get_ent_bill_cycle = get_ent_val
							# else:
							# 	get_ent_billing_type_value = str(get_ent_val)
				Trace.Write(str(get_billling_data_dict)+'--dict----get_ent_billing_type_value--get_ent_bill_cycle--4750--'+str(get_ent_bill_cycle))
				billing_month_end = 0
				entitlement_obj = Sql.GetFirst("select convert(xml,replace(replace(replace(replace(replace(replace(ENTITLEMENT_XML,'&',';#38'),'''',';#39'),' < ',' &lt; ' ),' > ',' &gt; ' ),'_>','_&gt;'),'_<','_&lt;')) as ENTITLEMENT_XML,QUOTE_RECORD_ID,SERVICE_ID from SAQTSE (nolock) where QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'".format(QuoteRecordId =ContractRecordId,RevisionRecordId=qt_rev_id))
				if str(get_ent_bill_cycle).upper() == "MONTHLY":
					Trace.Write('billing_day----'+str(billing_day))
					Trace.Write('start_date----'+str(start_date))
					if billing_day in (29,30,31):
						if start_date.month == 2:
							isLeap = lambda x: x % 4 == 0 and (x % 100 != 0 or x % 400 == 0)
							end_day = 29 if isLeap(start_date.year) else 28
							start_date = start_date.replace(day=end_day)
						elif start_date.month in (4, 6, 9, 11) and billing_day == 31:
							start_date = start_date.replace(day=30)
						else:
							start_date = start_date.replace(day=billing_day)
					else:
						start_date = start_date.replace(day=billing_day)
					end_date = datetime.datetime.strptime(UserPersonalizationHelper.ToUserFormat(contract_end_date), '%m/%d/%Y')
					#end_date = str(contract_end_date).split(' ')[0]
					diff1 = end_date - start_date

					avgyear = 365.2425        # pedants definition of a year length with leap years
					avgmonth = 365.2425/12.0  # even leap years have 12 months
					years, remainder = divmod(diff1.days, avgyear)
					years, months = int(years), int(remainder // avgmonth)            
					
					total_months = years * 12 + months
					Trace.Write('total_months--458-----'+str(type(total_months)))
					for index in range(0, total_months+1):
						Trace.Write('billing_month_end--460-----')
						billing_month_end += 1
						Trace.Write('billing_month_end----')
						insert_items_billing_plan(total_months=total_months, 
												billing_date="DATEADD(month, {Month}, '{BillingDate}')".format(
													Month=index, BillingDate=start_date.strftime('%m/%d/%Y')
													),billing_end_date="DATEADD(month, {Month_add}, '{BillingDate}')".format(
													Month_add=billing_month_end, BillingDate=start_date.strftime('%m/%d/%Y')
													), amount_column="YEAR_"+str((index/12) + 1),
													entitlement_obj=entitlement_obj,service_id = get_service_val,get_ent_val_type = get_ent_bill_cycle,get_ent_billing_type_value = get_ent_billing_type_value,get_billling_data_dict=get_billling_data_dict)
					Trace.Write('total_months-470-----'+str(total_months))
				elif str(get_ent_bill_cycle).upper() == "QUARTELY":
					Trace.Write('get_ent_val-billicycle--'+str(get_ent_bill_cycle))
					ct_start_date =contract_start_date
					ct_end_date =contract_end_date
					if ct_start_date>ct_end_date:
						ct_start_date,ct_end_date=ct_end_date,ct_start_date
					m1=ct_start_date.Year*12+ct_start_date.Month  
					m2=ct_end_date.Year*12+ct_end_date.Month  
					months=m2-m1
					Trace.Write('months---'+str(months))
					months=months/3
					Trace.Write('months-646----'+str(months))
					for index in range(0, months):
						billing_month_end += 1
						insert_items_billing_plan(total_months=months, 
												billing_date="DATEADD(month, {Month}, '{BillingDate}')".format(
													Month=index, BillingDate=start_date.strftime('%m/%d/%Y')
													),billing_end_date="DATEADD(month, {Month_add}, '{BillingDate}')".format(
													Month_add=billing_month_end, BillingDate=start_date.strftime('%m/%d/%Y')
													),amount_column="YEAR_"+str((index/4) + 1),
													entitlement_obj=entitlement_obj,service_id = get_service_val,get_ent_val_type = get_ent_val,get_ent_billing_type_value=get_ent_billing_type_value,get_billling_data_dict=get_billling_data_dict)
				else:
					Trace.Write('get_ent_val---'+str(get_ent_bill_cycle))
					if billing_day in (29,30,31):
						if start_date.month == 2:
							isLeap = lambda x: x % 4 == 0 and (x % 100 != 0 or x % 400 == 0)
							end_day = 29 if isLeap(start_date.year) else 28
							start_date = start_date.replace(day=end_day)
						elif start_date.month in (4, 6, 9, 11) and billing_day == 31:
							start_date = start_date.replace(day=30)
						else:
							start_date = start_date.replace(day=billing_day)
					else:
						start_date = start_date.replace(day=billing_day)
					end_date = datetime.datetime.strptime(UserPersonalizationHelper.ToUserFormat(contract_end_date), '%m/%d/%Y')			
					diff1 = end_date - start_date

					avgyear = 365.2425        # pedants definition of a year length with leap years
					avgmonth = 365.2425/12.0  # even leap years have 12 months
					years, remainder = divmod(diff1.days, avgyear)
					years, months = int(years), int(remainder // avgmonth)
					for index in range(0, years+1):
						billing_month_end += 1
						insert_items_billing_plan(total_months=years, 
												billing_date="DATEADD(month, {Month}, '{BillingDate}')".format(
													Month=index, BillingDate=start_date.strftime('%m/%d/%Y')
													),billing_end_date="DATEADD(month, {Month_add}, '{BillingDate}')".format(
													Month_add=billing_month_end, BillingDate=start_date.strftime('%m/%d/%Y')
													),amount_column="YEAR_"+str((index) + 1),
													entitlement_obj=entitlement_obj,service_id = get_service_val,get_ent_val_type = get_ent_val,get_ent_billing_type_value = get_ent_billing_type_value,get_billling_data_dict=get_billling_data_dict)			
			
def RELATEDMULTISELECTONEDIT(TITLE, VALUE, CLICKEDID, RECORDID,SELECTALL):
	TreeParam = Product.GetGlobal("TreeParam")
	if TreeParam == 'Receiving Equipment':
		CLICKEDID = "SYOBJR_98800_0D035FD5_F0EA_4F11_A0DB_B4E10928B59F"
	clicked = CLICKEDID.split("_")
	Trace.Write("clicked---"+str(clicked))
	obj_id = clicked[2] + "-" + clicked[3] + "-" + clicked[4] + "-" + clicked[5] + "-" + clicked[6]
	objr_id = clicked[0] + "-" + clicked[1]
	edt_str = ""
	checked = ""
	data_type = ""
	pricbkst_lock = "FALSE"
	pricbk_lock = "FALSE"
	date_field = []
	key = ""
	VALUE = remove_html_tags(VALUE)
	rec_ids = ",".join(RECORDID)
	
	Product.SetGlobal("RecordList", str(list(RECORDID)))
	Trace.Write("recordids---"+str(Product.GetGlobal("RecordList")))
	TreeSuperParentParam = Product.GetGlobal("TreeParentLevel1")
	objh_obj = Sql.GetFirst("select OBJECT_NAME from SYOBJH where RECORD_ID = '" + str(obj_id) + "'")
	objr_obj = Sql.GetFirst("select CAN_EDIT from SYOBJR where SAPCPQ_ATTRIBUTE_NAME = '" + str(objr_id) + "'")
	quote_status = Sql.GetFirst("SELECT REVISION_STATUS FROM SAQTRV WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(ContractRecordId,quote_revision_record_id))
	canedit = str(objr_obj.CAN_EDIT)
		
	if str(CLICKEDID) == "SYOBJR_00007_26B8147E_C59C_4010_AA3A_38176869E305":
		TITLE = "BILLING_DATE"
	#if str(CLICKEDID) == "SYOBJR_00009_E5504B40_36E7_4EA6_9774_EA686705A63F" and (TreeParentParam != 'Quote Items' and TreeParentParam != ''):
	#canedit = "FALSE"	
	Trace.Write("@175----canedit-------->"+str(canedit))
	if objh_obj is not None and str(canedit).upper() == "TRUE":
		obj_obj = str(objh_obj.OBJECT_NAME)
		Trace.Write("object name--"+str(obj_obj))
		
		objd_obj = Sql.GetFirst(
			"SELECT DATA_TYPE,PICKLIST_VALUES,API_NAME,FIELD_LABEL,PERMISSION,FORMULA_DATA_TYPE FROM  SYOBJD where OBJECT_NAME='"
			+ str(obj_obj)
			+ "' and API_NAME='"
			+ str(TITLE)
			+ "'"
		)
		if objd_obj is not None and pricbkst_lock.upper() == "FALSE" and pricbk_lock.upper() == "FALSE":
			data_type = str(objd_obj.DATA_TYPE).strip()
			api_name = str(objd_obj.API_NAME).strip()
			Permission = str(objd_obj.PERMISSION).strip()
			formula_data_type = str(objd_obj.FORMULA_DATA_TYPE).strip()
			if(data_type != "LOOKUP" and data_type != "AUTO NUMBER" and data_type != "" and Permission != "READ ONLY"):
				Trace.Write('Working ----->')
				pick_val = str(objd_obj.PICKLIST_VALUES)
				field_lable = str(objd_obj.FIELD_LABEL)
				datepicker = "onclick_datepicker('" + api_name + "')"
				if SELECTALL != "noselection":
					if TITLE != 'NET_PRICE' and TITLE != "PM_FREQUENCY" and TITLE != "QUANTITY" and TITLE!="CUSTOMER_ANNUAL_QUANTITY":
						edt_str += (
							'<div   class="row modulebnr brdr">EDIT '
							+ str(field_lable).upper()
							+ ' <button type="button"   class="close fltrt" onclick="multiedit_RL_cancel();">X</button></div>'
						)
						edt_str += '<div id="container" class="g4 pad-10 brdr except_sec">'
						edt_str += '<table class="wdth100" id="bulk_edit">'
						edt_str += (
							'<tbody><tr class="fieldRow"><td   class="wth50txtcein labelCol">'
							+ str(field_lable)
							+ '</td><td class="dataCol"><div id="massEditFieldDiv" class="inlineEditRequiredDiv">'
						)
						Trace.Write("list(RECORDID)_CHECK__J "+str(len(list(RECORDID))))
					if len(list(RECORDID)) > 1:
						Trace.Write("data_type_CHECK__J "+str(data_type))
						if data_type.upper() == "TEXT":
							edt_str += '<input class="form-control light_yellow wth_80"   id="' + str(api_name) + '" type="text">'
						elif data_type.upper() == "NUMBER":
							Trace.Write("@215 inside number")
							edt_str += '<input class="form-control light_yellow wth_80"   id="' + str(api_name) + '" type="text">'
						elif data_type.upper() == "CHECKBOX" or formula_data_type.upper() == "CHECKBOX":
							edt_str += (
								'<input class="custom light_yellow wth_80"  id="'
								+ str(api_name)
								+ '" type="checkbox"><span class="lbl"></span>'
							)
						elif data_type.upper() == "FORMULA":
							if  obj_obj == 'SAQSTE':
								edt_str += '<input class="form-control light_yellow fltlt wth_80"   id="' + str(api_name) + '" type="text">'
								edt_str += '<input  id="MAFBLC|SAQSTE" class="popup fltlt"  type="image" onclick = "CommonTree_lookup_popup(this)" data-toggle="modal" data-target="#cont_viewModalSection"  src="../mt/default/images/customer_lookup.gif" id="' + str(api_name) + '" >'
							elif obj_obj == 'SAQICO':
								edt_str += '<input class="form-control light_yellow fltlt wth_80"   id="' + str(api_name) + '" type="text">'
								edt_str += '<input  id="PRTXCL|SAQICO" class="popup fltlt"  type="image" onclick = "CommonTree_lookup_popup(this)" data-toggle="modal" data-target="#cont_viewModalSection"  src="../mt/default/images/customer_lookup.gif" id="' + str(api_name) + '" >'	
							elif obj_obj == 'SAQSCO':
								edt_str += '<input class="form-control light_yellow fltlt wth_80"   id="' + str(api_name) + '" type="text">'
								edt_str += '<input  id="SAQSCO|SAQFEQ" class="popup fltlt"  type="image" onclick = "CommonTree_lookup_popup(this)" data-toggle="modal" data-target="#cont_viewModalSection"  src="../mt/default/images/customer_lookup.gif" id="' + str(api_name) + '" >'	
								Trace.Write("EDITSTR"+str(edt_str))	
							elif obj_obj == 'SYROUS':
								edt_str += '<input class="form-control light_yellow fltlt wth_80"   id="' + str(api_name) + '" type="text">'
								edt_str += '<input  id="SYROMA|SYROUS" class="popup fltlt"  type="image" onclick = "CommonTree_lookup_popup(this)" data-toggle="modal" data-target="#cont_viewModalSection"  src="../mt/default/images/customer_lookup.gif" id="' + str(api_name) + '" >'	
								Trace.Write("EDITSTR"+str(edt_str))	
						elif data_type.upper() == "PICKLIST":
							edt_str += '<select class="form-control light_yellow wth150"   id="' + str(api_name) + '">'
							pick_val = pick_val.split(",")
							for value in pick_val:
								edt_str += "<option>" + str(value) + "</option>"
							edt_str += "</select>"
						elif data_type.upper() == "DATE":
							date_field.append(api_name)
							edt_str += (
								'<input id="'
								+ str(api_name)
								+ '" type="text" class="form-control light_yellow wth155hit26"  ><span   class="pad4wth0 input-group-addon" onclick="'
								+ str(datepicker)
								+ '"><i class="glyphicon glyphicon-calendar"></i></span>'
							)
						else:
							edt_str += '<input class="form-control light_yellow wth_80"   id="' + str(api_name) + '" type="text">'
						edt_str += '</div></td></tr><tr class="selectionRow">'
						edt_str += (
							'<td   class="labelCol wth50txtcein">Apply changes to</td><td class="dataCol"><div class="radio"><input type="radio" name="massOrSingleEdit" id="singleEditRadio" checked="checked"><label for="singleEditRadio">The record clicked</label></div><div class="radio"><input type="radio" name="massOrSingleEdit" id="massEditRadio"><label for="massEditRadio">All '
							+ str(len(list(RECORDID)))
							+ " selected records</label>"
						)
					else:
						
						if data_type.upper() == "TEXT":
							edt_str += (
								'<input class="form-control light_yellow wth_80"   id="'
								+ str(api_name)
								+ '" type="text" value="'
								+ str(VALUE)
								+ '">'
							)
						elif data_type.upper() == "FORMULA" and obj_obj == 'SAQSTE':
							edt_str += '<input class="form-control light_yellow fltlt wth_80"   id="' + str(api_name) + '" type="text">'
							edt_str += '<input  id="MAFBLC|SAQSTE" class="popup fltlt"  type="image" onclick = "CommonTree_lookup_popup(this)" data-toggle="modal" data-target="#cont_viewModalSection"  src="../mt/default/images/customer_lookup.gif" id="' + str(api_name) + '" >'	
						elif data_type.upper() == "NUMBER":
							if TITLE not in ('NET_PRICE','PM_FREQUENCY','QUANTITY','CUSTOMER_ANNUAL_QUANTITY'):
								Trace.Write("inside number")
								edt_str += (
									'<input class="form-control light_yellow wth_80"   id="'
									+ str(api_name)
									+ '" value="'
									+ str(VALUE)
									+ '" type="text">'
								)
						elif data_type.upper() == "FORMULA":
							if obj_obj == 'SAQSTE':
								edt_str += '<input class="form-control light_yellow fltlt wth_80"   id="' + str(api_name) + '" type="text">'
								edt_str += '<input  id="MAFBLC|SAQSTE" class="popup fltlt"  type="image" onclick = "CommonTree_lookup_popup(this)" data-toggle="modal" data-target="#cont_viewModalSection"  src="../mt/default/images/customer_lookup.gif" id="' + str(api_name) + '" >'
							elif obj_obj == 'SAQICO':
								edt_str += '<input class="form-control light_yellow fltlt wth_80"   id="' + str(api_name) + '" type="text">'
								edt_str += '<input  id="PRTXCL|SAQICO" class="popup fltlt"  type="image" onclick = "CommonTree_lookup_popup(this)" data-toggle="modal" data-target="#cont_viewModalSection"  src="../mt/default/images/customer_lookup.gif" id="' + str(api_name) + '" >'	
							elif obj_obj == 'SAQSCO':
								edt_str += '<input class="form-control light_yellow fltlt wth_80"   id="' + str(api_name) + '" type="text">'
								edt_str += '<input  id="SAQSCO|SAQFEQ" class="popup fltlt"  type="image" onclick = "CommonTree_lookup_popup(this)" data-toggle="modal" data-target="#cont_viewModalSection"  src="../mt/default/images/customer_lookup.gif" id="' + str(api_name) + '" >'	
								Trace.Write("EDITSTR"+str(edt_str))
						elif data_type.upper() == "CHECKBOX" or formula_data_type.upper() == "CHECKBOX":
							if str(VALUE).upper() == "TRUE":
								checked = "checked"
							edt_str += (
								'<input class="custom light_yellow wth_80"   id="'
								+ str(api_name)
								+ '" type="checkbox" '
								+ str(checked)
								+ '><span class="lbl"></span>'
							)
						elif data_type.upper() == "PICKLIST":
							edt_str += '<select class="form-control light_yellow wth150"   id="' + str(api_name) + '">'
							pick_val = pick_val.split(",")
							for value in pick_val:
								edt_str += "<option>" + str(value) + "</option>"
							edt_str += "</select>"
						elif data_type.upper() == "DATE":
							date_field.append(api_name)
							edt_str += (
								'<input id="'
								+ str(api_name)
								+ '" type="text" value="'
								+ str(VALUE)
								+ '" class="form-control light_yellow wth155hit26"  ><span   class="pad4wth0 input-group-addon" onclick="'
								+ str(datepicker)
								+ '"><i class="glyphicon glyphicon-calendar"></i></span>'
							)
						else:
							edt_str += (
								'<input class="form-control light_yellow wth_80"   id="'
								+ str(api_name)
								+ '" type="text" value="'
								+ str(VALUE)
								+ '">'
							)
					if TITLE not in ('NET_PRICE','DISCOUNT','PM_FREQUENCY','QUANTITY','CUSTOMER_ANNUAL_QUANTITY','NEW_PART') :
						edt_str += "</div></td></tr></tbody></table>"
						edt_str += '<div class="row pad-10"><button class="btnconfig" onclick="multiedit_RL_cancel();" type="button" value="Cancel" id="cancelButton">CANCEL</button><button class="btnconfig" type="button" value="Save" onclick="multiedit_save_RL()" id="saveButton">SAVE</button></div></div>'
					else:
						if quote_status.REVISION_STATUS=='APPROVED':
							edt_str = "NO"
						elif obj_obj == 'SAQSAP':
							k = Sql.GetFirst("SELECT QUOTE_SERVICE_COV_OBJ_ASS_PM_KIT_RECORD_ID FROM SAQSAP WHERE CpqTableEntryId = {}".format(str(RECORDID[0]).split("-")[1]))
							Trace.Write("query---->"+str(k))
							apply_all = ''
							if len(list(RECORDID)) > 1:
								apply_all = '<div class="col-md-12 pt-0 pb-0 d-flex align-items-center"><div class="partno-lbl col-md-6 text-right">Apply changes to</div><div class="txt-col-sec col-md-6 pl-0"><div class="radio"><input type="radio" name="massOrSingleEdit" id="singleEditRadio" checked="checked"><label for="singleEditRadio">The record clicked</label></div><div class="radio"><input type="radio" name="massOrSingleEdit" id="massEditRadio"><label for="massEditRadio">All selected records</label></div></div></div>'
							edt_str = '<div class="modal-dialog bg-white" id="edit_decrip"><div class="modal-content"><div class="modal-header revision_edit_decripheader"><span class="modal-title">BULK EDIT</span><button type="button" class="close" data-dismiss="modal" aria-label="Close" onclick="multiedit_RL_cancel();"><span aria-hidden="true">x</span></button></div><div class="fixed-table-body"><div class="col-md-12"><div class="row pad-10 bg-lt-wt brdr" id="seginnerbnr"><img style="height: 40px; margin-top: -1px; margin-left: -1px; float: left;" src="/mt/appliedmaterials_tst/Additionalfiles/Secondary Icon.svg"><div class="product_txt_div_child secondary_highlight text-left wid75" style="display: block;"><div class="product_txt_child"><abbr title="Bulk Edit">Bulk Edit</abbr></div><div class="product_txt_to_top_child help_text" style="float: left;"><abbr title="Enter Updated PM Frequency to add to your PM events...">Enter Updated PM Frequency to add to your PM events...</abbr></div></div></div></div><div class="col-md-12 pt-0 d-flex align-items-center"><div class="partno-lbl col-md-6 text-right">Updated PM Frequency</div><div class="txt-col-sec col-md-6 pl-0"><input id="updated_PM" class="light_yellow" value="'+str(VALUE)+'"></div></div>'+str(apply_all)+'</div><div class="modal-footer"><button id="popupcancel" class="btn btn-list-cust" data-dismiss="modal" aria-hidden="true" onclick="multiedit_RL_cancel();">CANCEL</button><button onclick="multiedit_save_RL()" id="bulkEditPM_Frequency" data-dismiss="modal" class="btn btn-list-cust">SAVE</button></div> </div></div>'
							if k:
								key = str(k.QUOTE_SERVICE_COV_OBJ_ASS_PM_KIT_RECORD_ID)
						elif obj_obj == 'SAQRSP':
							#if (str(TreeSuperParentParam)!="Product Offerings" and TreeParam !='Z0092')or (str(TreeSuperParentParam)=="Product Offerings" and TreeParam =='Z0092') :
							if TITLE=="QUANTITY":
								field = "Enter Updated Target Quantity to add to your Parts List..."
								label = "UPDATED TARGET QUANTITY" 
								input_id = "updatedQuantity"
								input_type = ""
								checked = ""
							else: 
								field = "Select New Part to Update Parts List..."
								label = "UPDATED NEW PART"
								input_id = "updatedNewPart"
								input_type = "type = \'checkbox\' "
								checked = "checked" if VALUE == 1 or str(VALUE).upper() =="TRUE" else ""
							k = Sql.GetFirst("SELECT QUOTE_REV_PO_PRODUCT_LIST_ID FROM SAQRSP WHERE CpqTableEntryId = {}".format(str(RECORDID[0]).split("-")[1]))
							apply_all = ''
							if len(list(RECORDID)) > 1:
								apply_all = '<div class="col-md-12 pt-0 pb-0 d-flex align-items-center"><div class="partno-lbl col-md-6 text-right">Apply changes to</div><div class="txt-col-sec col-md-6 pl-0"><div class="radio"><input type="radio" name="massOrSingleEdit" id="singleEditRadio" checked="checked"><label for="singleEditRadio">The record clicked</label></div><div class="radio"><input type="radio" name="massOrSingleEdit" id="massEditRadio"><label for="massEditRadio">All selected records</label></div></div></div>'
							edt_str = '<div class="modal-dialog bg-white" id="edit_decrip"><div class="modal-content"><div class="modal-header revision_edit_decripheader"><span class="modal-title">BULK EDIT</span><button type="button" class="close" data-dismiss="modal" aria-label="Close" onclick="multiedit_RL_cancel();"><span aria-hidden="true">x</span></button></div><div class="fixed-table-body"><div class="col-md-12"><div class="row pad-10 bg-lt-wt brdr" id="seginnerbnr"><img style="height: 40px; margin-top: -1px; margin-left: -1px; float: left;" src="/mt/appliedmaterials_tst/Additionalfiles/Secondary Icon.svg"><div class="product_txt_div_child secondary_highlight text-left wid75" style="display: block;"><div class="product_txt_child"><abbr title="Bulk Edit">Bulk Edit</abbr></div><div class="product_txt_to_top_child help_text" style="float: left;"><abbr title="'+str(field)+'">'+str(field)+'</abbr></div></div></div></div><div class="col-md-12 pt-0 d-flex align-items-center"><div class="partno-lbl col-md-6 text-right">'+str(label)+'</div><div class="txt-col-sec col-md-6 pl-0"><input id="'+str(input_id)+'" class="light_yellow" '+str(input_type)+' value="'+str(VALUE)+'" '+str(checked)+'><span class="lbl"></span></div></div>'+str(apply_all)+'</div><div class="modal-footer"><button id="popupcancel" class="btn btn-list-cust" data-dismiss="modal" aria-hidden="true" onclick="multiedit_RL_cancel();">CANCEL</button><button onclick="PartsListMultiEdit(this)" id="'+str(input_id)+'_save" data-dismiss="modal" class="btn btn-list-cust">SAVE</button></div> </div></div>'
							if k:
								key = str(k.QUOTE_REV_PO_PRODUCT_LIST_ID)
							# else:
							# 	edt_str = "NO"
						elif obj_obj == 'SAQSPT':
							k = Sql.GetFirst("SELECT QUOTE_SERVICE_PART_RECORD_ID FROM SAQSPT WHERE CpqTableEntryId = {}".format(str(RECORDID[0]).split("-")[1]))
							apply_all = ''
							if len(list(RECORDID)) > 1:
								apply_all = '<div class="col-md-12 pt-0 pb-0 d-flex align-items-center"><div class="partno-lbl col-md-6 text-right">Apply changes to</div><div class="txt-col-sec col-md-6 pl-0"><div class="radio"><input type="radio" name="massOrSingleEdit" id="singleEditRadio" checked="checked"><label for="singleEditRadio">The record clicked</label></div><div class="radio"><input type="radio" name="massOrSingleEdit" id="massEditRadio"><label for="massEditRadio">All selected records</label></div></div></div>'
							disabled = "disabled" if VALUE=="" else ""
							edt_str = '<div class="modal-dialog bg-white" id="edit_decrip"><div class="modal-content"><div class="modal-header revision_edit_decripheader"><span class="modal-title">BULK EDIT</span><button type="button" class="close" data-dismiss="modal" aria-label="Close" onclick="multiedit_RL_cancel();"><span aria-hidden="true">x</span></button></div><div class="fixed-table-body"><div class="col-md-12"><div class="row pad-10 bg-lt-wt brdr" id="seginnerbnr"><img style="height: 40px; margin-top: -1px; margin-left: -1px; float: left;" src="/mt/appliedmaterials_tst/Additionalfiles/Secondary Icon.svg"><div class="product_txt_div_child secondary_highlight text-left wid75" style="display: block;"><div class="product_txt_child"><abbr title="Bulk Edit">Bulk Edit</abbr></div><div class="product_txt_to_top_child help_text" style="float: left;"><abbr title="Enter Updated Customer Annual Quantity to add to your Spare Parts...">Enter Updated Customer Annual Quantity to add to your Spare Parts...</abbr></div></div></div></div><div class="col-md-12 pt-0 d-flex align-items-center"><div class="partno-lbl col-md-6 text-right">Updated Quantity</div><div class="txt-col-sec col-md-6 pl-0"><input id="updatedCustomerAnnualQuantity" type="number" class="light_yellow" value="'+str(VALUE)+'" onkeyup="validateInput()"><div id="alertMessage" style="font-size:12px;color:red;"></div></div></div>'+str(apply_all)+'</div><div class="modal-footer"><button id="popupcancel" class="btn btn-list-cust" data-dismiss="modal" aria-hidden="true" onclick="multiedit_RL_cancel();">CANCEL</button><button onclick="PartsListMultiEdit(this)" id="updatedCustomerAnnualQuantity_save" data-dismiss="modal" class="btn btn-list-cust" '+str(disabled)+'>SAVE</button></div> </div></div>'
							if k:
								key = str(k.QUOTE_SERVICE_PART_RECORD_ID)
						else:
							k = Sql.GetFirst("SELECT QUOTE_ITEM_COVERED_OBJECT_RECORD_ID FROM SAQICO WHERE CpqTableEntryId = {}".format(str(RECORDID[0]).split("-")[1]))
							Trace.Write("query---->"+str(k))
							key = str(k.QUOTE_ITEM_COVERED_OBJECT_RECORD_ID)
				if SELECTALL == "noselection":
					edt_str = "NO"
			else:
				edt_str = "NO"
		else:
			edt_str = "NO"
			Trace.Write("EDITSTR"+str(edt_str))	
	else:
		edt_str = "NO"
	Trace.Write('datalist--'+str(edt_str)+'--'+str(date_field)+'--'+str(key))
	return edt_str, date_field,key


def remove_html_tags(text):
	"""Remove html tags from a string"""
	import re

	clean = re.compile("<.*?>")
	return re.sub(clean, "", text)


def RELATEDMULTISELECTONSAVE(TITLE, VALUE, CLICKEDID, RECORDID,selectPN,ALLVALUES,ALLVALUES1,ALLVALUES2,SELECTALL):
	Sql = SQL()
	TreeParam = Product.GetGlobal("TreeParam")
	TreeParentParam = Product.GetGlobal("TreeParentLevel0")
	TreeSuperParentParam = Product.GetGlobal("TreeParentLevel1")
	TreeTopSuperParentParam = Product.GetGlobal("TreeParentLevel2")
	if TreeParam == 'Receiving Equipment':
		CLICKEDID = "SYOBJR_98800_0D035FD5_F0EA_4F11_A0DB_B4E10928B59F"
	value_list = []
	VALUE1 = []
	selected_rows = RECORDID.split(",")
	
	clicked = CLICKEDID.split("_")
	obj_id = clicked[2] + "-" + clicked[3] + "-" + clicked[4] + "-" + clicked[5] + "-" + clicked[6]
	
	edt_str = ""
	checked = ""
	date_field = []
	selected_rows_cpqid = []
	objh_obj = SqlHelper.GetFirst("select OBJECT_NAME, RECORD_NAME from SYOBJH where RECORD_ID = '" + str(obj_id) + "'")
	if objh_obj is not None:
		obj_name = str(objh_obj.OBJECT_NAME)
		objh_head = str(objh_obj.RECORD_NAME)
		item_lines_record_ids = []
		if (obj_name == "SAQSAP" or obj_name == "SAQRSP" or obj_name == "SAQSPT") and (TreeParentParam in ('Comprehensive Services','Complementary Products') or TreeSuperParentParam in ('Comprehensive Services','Complementary Products')):
			selected_rows = selectPN if selectPN else selected_rows
			qury_str = ""
			Trace.Write(str(CLICKEDID)+'--Values-->'+str(A_Values))
			if A_Keys!="" and A_Values!="":
				for key,val in zip(A_Keys,A_Values):
					if(val!=""):
						if key=="QUOTE_SERVICE_COV_OBJ_ASS_PM_KIT_RECORD_ID" or key=="QUOTE_REV_PO_PRODUCT_LIST_ID" or key =="QUOTE_SERVICE_PART_RECORD_ID":
							key="CpqTableEntryId"
							val = ''.join(re.findall(r'\d+', val)) if not val.isdigit() else val
						qury_str+=" "+key+" LIKE '%"+val+"%' AND "
			if(SELECTALL=="PM_BULKEDIT_ALL" and obj_name == "SAQSAP" and TITLE == "PM_FREQUENCY"):
				Sql.RunQuery("""UPDATE SAQSAP SET {column} = {value} WHERE {qury_str} QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{rev_rec_id}' AND SERVICE_ID = '{service_id}' """.format(column=TITLE,value=ALLVALUES,QuoteRecordId = Qt_rec_id,rev_rec_id = Quote.GetGlobal("quote_revision_record_id"),service_id=TreeParam,qury_str=qury_str))
				return ""
			elif(SELECTALL=="PARTS_BULKEDIT_ALL" and obj_name == "SAQRSP" and (TITLE == "QUANTITY" or TITLE=="NEW_PART")):
				Sql.RunQuery("""UPDATE SAQRSP SET {column} = '{value}' WHERE {qury_str} QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{rev_rec_id}' AND PAR_SERVICE_ID = '{service_id}' AND GREENBOOK = '{greenbook}' """.format(column=TITLE,value = ALLVALUES,QuoteRecordId = Qt_rec_id,rev_rec_id = Quote.GetGlobal("quote_revision_record_id"),service_id=TreeParentParam,greenbook=TreeParam,qury_str=qury_str))
				return ""
			elif(SELECTALL=="PARTS_BULKEDIT_ALL" and obj_name == "SAQSPT" and TITLE == "CUSTOMER_ANNUAL_QUANTITY"):
				Sql.RunQuery("""UPDATE SAQSPT SET {column} = {value} WHERE {qury_str} QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{rev_rec_id}' AND SERVICE_ID = '{service_id}' """.format(column=TITLE,value = 'NULL' if int(ALLVALUES)==0 else ALLVALUES,QuoteRecordId = Qt_rec_id,rev_rec_id = Quote.GetGlobal("quote_revision_record_id"),service_id=TreeParam,qury_str=qury_str))
				count=Sql.GetFirst("SELECT COUNT(*) AS CNT FROM SAQSPT WHERE QUOTE_RECORD_ID= '"+str(Qt_rec_id)+"' and CUSTOMER_ANNUAL_QUANTITY IS NOT NULL ")      
				if count.CNT==0:
					delete_saqris = Sql.RunQuery("DELETE FROM SAQRIS WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID = '{}'".format(Qt_rec_id,Quote.GetGlobal("quote_revision_record_id"),TreeParam))
					delete_saqrit = Sql.RunQuery("DELETE FROM SAQRIT WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID = '{}'".format(Qt_rec_id,Quote.GetGlobal("quote_revision_record_id"),TreeParam))
					delete_saqico = Sql.RunQuery("DELETE FROM SAQICO WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID = '{}'".format(Qt_rec_id,Quote.GetGlobal("quote_revision_record_id"),TreeParam))
					update_saqtrv = Sql.RunQuery("UPDATE SAQTRV SET NET_PRICE_INGL_CURR=NULL, NET_VALUE_INGL_CURR=NULL WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(Qt_rec_id,Quote.GetGlobal("quote_revision_record_id")))
				return ""
		for index,rec in enumerate(selected_rows):
			row = {}
			if TITLE == 'DISCOUNT' and '%' in VALUE:
				VALUE = VALUE.replace('%','')
			TITLE_NAME = TITLE.split(',')[0]
			row = {TITLE_NAME: str(VALUE)}
			
			cpqid = rec.split("-")[1].lstrip("0")
			##to update changed value in related tables in tool relcoation matrix
			selected_rows_cpqid.append(cpqid)
			Get_recidval = SqlHelper.GetFirst(
				"SELECT {}  FROM {} (NOLOCK) WHERE CpqTableEntryId='{}' ".format(objh_head, obj_name, cpqid)
			)
			
			rec = getattr(Get_recidval, objh_head)
			
			row[objh_head] = str(rec)
			

			#Trace.Write("SELECT * FROM " + str(obj_name) + " (NOLOCK) WHERE " + str(objh_head) + " = '" + str(rec) + "'")
			sql_obj = SqlHelper.GetFirst("SELECT * FROM  " + str(obj_name) + "  WHERE " + str(objh_head) + " = '" + str(rec) + "'")
			
			#Trace.Write("111====="+str(sql_obj.QUOTE_ID))
			if obj_name == 'SAQICO':
				quote_id = sql_obj.QUOTE_ID
				item_lines_record_ids.append(sql_obj.QUOTE_ITEM_COVERED_OBJECT_RECORD_ID)
			if obj_name == "SYPRAP":
				
				tableInfo = Sql.GetTable("SYPRAP")
				primaryQueryItems = SqlHelper.GetFirst(
					"SELECT * FROM " + str(obj_name) + " WHERE " + objh_head + " = '" + str(rec) + "'"
				)
				row["CpqTableEntryId"] = primaryQueryItems.CpqTableEntryId
				row["DEFAULT"] = str(row.get("VISIBLE"))
				
				tableInfo.AddRow(row)
				Sql.Upsert(tableInfo)
			##multi select bulk edit..
			elif obj_name == "SAQSCO":
				recordslist = []
				for val in selectPN:
					ObjectName = val.split('-')[0].strip()
					cpqid = val.split('-')[1].strip()
					recid = CPQID.KeyCPQId.GetKEYId(ObjectName,str(cpqid))
					recordslist.append(recid)
				Trace.Write("recccccccc"+str(recordslist))	
				recordslist = str(tuple(recordslist)).replace(',)',')')
				Trace.Write("recordslist--->"+str(recordslist))
			##multi select bulk edit..	
			elif (TreeParentParam == 'Complementary Products' and obj_name == "SAQSPT"):
				Sql = SQL()
				if TITLE == "CUSTOMER_ANNUAL_QUANTITY":
					value = ALLVALUES[index] if str(type(ALLVALUES))=="<type 'ArrayList'>" else ALLVALUES
					if int(value)==0:
						Sql.RunQuery("""UPDATE SAQSPT SET {column} = NULL WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{rev_rec_id}' AND {rec_name} = '{rec_id}' """.format(column=TITLE,QuoteRecordId = Qt_rec_id,rev_rec_id = Quote.GetGlobal("quote_revision_record_id"),rec_name = objh_head,rec_id = sql_obj.QUOTE_SERVICE_PART_RECORD_ID))
					else:
						Sql.RunQuery("""UPDATE SAQSPT SET {column} = '{value}' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{rev_rec_id}' AND {rec_name} = '{rec_id}' """.format(column=TITLE,value = ALLVALUES[index] if str(type(ALLVALUES))=="<type 'ArrayList'>" else ALLVALUES,QuoteRecordId = Qt_rec_id,rev_rec_id = Quote.GetGlobal("quote_revision_record_id"),rec_name = objh_head,rec_id = sql_obj.QUOTE_SERVICE_PART_RECORD_ID))
				elif TITLE.split(',') == ["CUSTOMER_PARTICIPATE","CUSTOMER_ACCEPT_PART","CUSTOMER_ANNUAL_QUANTITY"]:
					if int(ALLVALUES2[index])==0:
						Sql.RunQuery("""UPDATE SAQSPT SET {column} = '{value}',{column1} = '{value1}',{column2} = NULL WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{rev_rec_id}' AND {rec_name} = '{rec_id}' """.format(column=TITLE.split(',')[0],value = ALLVALUES[index],column1=TITLE.split(',')[1],value1 = ALLVALUES1[index],column2=TITLE.split(',')[2],value2 = ALLVALUES2[index],QuoteRecordId = Qt_rec_id,rev_rec_id = Quote.GetGlobal("quote_revision_record_id"),rec_name = objh_head,rec_id = sql_obj.QUOTE_SERVICE_PART_RECORD_ID))
					else:
						Sql.RunQuery("""UPDATE SAQSPT SET {column} = '{value}',{column1} = '{value1}',{column2} = '{value2}' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{rev_rec_id}' AND {rec_name} = '{rec_id}' """.format(column=TITLE.split(',')[0],value = ALLVALUES[index],column1=TITLE.split(',')[1],value1 = ALLVALUES1[index],column2=TITLE.split(',')[2],value2 = ALLVALUES2[index],QuoteRecordId = Qt_rec_id,rev_rec_id = Quote.GetGlobal("quote_revision_record_id"),rec_name = objh_head,rec_id = sql_obj.QUOTE_SERVICE_PART_RECORD_ID))
				elif TITLE=="DELIVERY_MODE":
					Sql.RunQuery("""UPDATE SAQSPT SET DELIVERY_MODE = '{value}' {schedule_mode} WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{rev_rec_id}' AND {rec_name} = '{rec_id}' """.format(value=VALUE,schedule_mode= ",SCHEDULE_MODE = 'ON REQUEST'" if str(VALUE)=="OFFSITE" else "",QuoteRecordId = Qt_rec_id,rev_rec_id = Quote.GetGlobal("quote_revision_record_id"),rec_name = objh_head,rec_id = sql_obj.QUOTE_SERVICE_PART_RECORD_ID))
				elif TITLE=="SCHEDULE_MODE":
					Sql.RunQuery("""UPDATE SAQSPT SET SCHEDULE_MODE = '{value}' {delivery_mode} WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{rev_rec_id}' AND {rec_name} = '{rec_id}' """.format(value=VALUE,delivery_mode= ",DELIVERY_MODE = 'ONSITE' " if str(VALUE)=="LOW QUANTITY ONSITE" else "",QuoteRecordId = Qt_rec_id,rev_rec_id = Quote.GetGlobal("quote_revision_record_id"),rec_name = objh_head,rec_id = sql_obj.QUOTE_SERVICE_PART_RECORD_ID))

				count=Sql.GetFirst("SELECT COUNT(*) AS CNT FROM SAQSPT WHERE QUOTE_RECORD_ID= '"+str(Qt_rec_id)+"' and CUSTOMER_ANNUAL_QUANTITY IS NOT NULL ")  
				cust_annual_qty = Sql.GetList("SELECT CUSTOMER_ANNUAL_QUANTITY FROM SAQSPT (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID= '{rev_rec_id}' AND SERVICE_ID = '{service_id}'".format(QuoteRecordId = Qt_rec_id,rev_rec_id = Quote.GetGlobal("quote_revision_record_id"),service_id=TreeParam))
				
				for annual_qty in cust_annual_qty:
					Trace.Write("Annual_Qty "+str(annual_qty))
					if annual_qty.CUSTOMER_ANNUAL_QUANTITY < 10:
						Trace.Write("Less Than 10")
						Sql.RunQuery("UPDATE SAQSPT SET SCHEDULE_MODE = 'UNSCHEDULED' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID= '{rev_rec_id}' AND SERVICE_ID = '{service_id}' AND CUSTOMER_ANNUAL_QUANTITY < 10".format(QuoteRecordId = Qt_rec_id,rev_rec_id = Quote.GetGlobal("quote_revision_record_id"),service_id=TreeParam))
					elif annual_qty.CUSTOMER_ANNUAL_QUANTITY >= 10:
						Trace.Write("Greater Than 10")
						Sql.RunQuery("UPDATE SAQSPT SET SCHEDULE_MODE = 'SCHEDULED' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID= '{rev_rec_id}' AND SERVICE_ID = '{service_id}' AND CUSTOMER_ANNUAL_QUANTITY >= 10".format(QuoteRecordId = Qt_rec_id,rev_rec_id = Quote.GetGlobal("quote_revision_record_id"),service_id=TreeParam))
				if count.CNT==0:
					delete_saqris = Sql.RunQuery("DELETE FROM SAQRIS WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID = '{}'".format(Qt_rec_id,Quote.GetGlobal("quote_revision_record_id"),TreeParam))
					delete_saqrit = Sql.RunQuery("DELETE FROM SAQRIT WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID = '{}'".format(Qt_rec_id,Quote.GetGlobal("quote_revision_record_id"),TreeParam))
					delete_saqico = Sql.RunQuery("DELETE FROM SAQICO WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID = '{}'".format(Qt_rec_id,Quote.GetGlobal("quote_revision_record_id"),TreeParam))
					update_saqtrv = Sql.RunQuery("UPDATE SAQTRV SET NET_PRICE_INGL_CURR=NULL, NET_VALUE_INGL_CURR=NULL WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(Qt_rec_id,Quote.GetGlobal("quote_revision_record_id")))
				
			elif str(obj_name) == "SAQSPT":
				getserid = row.get("QUOTE_SERVICE_PART_RECORD_ID")
				getpartno = getQn = getAQ = ""
				getPN = Sql.GetFirst("select  * from SAQSPT where QUOTE_SERVICE_PART_RECORD_ID = '"+str(getserid)+"'")
				if getPN:
					getpartno = getPN.PART_NUMBER
					getQn = getPN.QUOTE_ID
					getAQ = getPN.CUSTOMER_ANNUAL_QUANTITY
				sqlforupdatePT = sqlforupdate = ""
				Table.TableActions.Update(obj_name, objh_head, row)
				#for PN in selectPN:
				#Trace.Write(str(getAQ)+str(getQn)+str(getpartno)+'selected rows-------------------------'+str(len(selected_rows)))
				if len(selected_rows) > 1:
					sqlforupdatePT += "UPDATE SAQIFP SET ANNUAL_QUANTITY = '{AQ}',EXTENDED_PRICE = (UNIT_PRICE*'{AQ}') where QUOTE_RECORD_ID ='{CT}' and  PART_NUMBER in {PN} AND QTEREV_RECORD_ID = '{quote_revision_record_id}'".format(AQ =str(VALUE) ,CT = str(ContractRecordId),PN=tuple(selectPN),quote_revision_record_id=quote_revision_record_id)
					#sqlforupdatePT += "UPDATE SAQIFP SET ANNUAL_QUANTITY = '{AQ}',EXTENDED_UNIT_PRICE = '{UP}' where QUOTE_RECORD_ID ='{CT}' and  PART_NUMBER in {PN}".format(AQ =str(VALUE) ,CT = str(ContractRecordId),PN=tuple(selectPN))
					Sql.RunQuery(sqlforupdatePT)
					sqlforupdate += "UPDATE QT__SAQIFP SET  ANNUAL_QUANTITY = {AQ},EXTENDED_UNIT_PRICE = (UNIT_PRICE*{AQ}) where QUOTE_RECORD_ID ='{CT}' and  PART_NUMBER in {PN}".format(AQ =VALUE ,CT = str(ContractRecordId),PN=tuple(selectPN))
					Sql.RunQuery(sqlforupdate)
				else:
					
					sqlforupdatePT += "UPDATE SAQIFP SET ANNUAL_QUANTITY = '{AQ}',EXTENDED_PRICE = (UNIT_PRICE*{AQ}) where QUOTE_RECORD_ID ='{CT}' and  PART_NUMBER = '{PN}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}'".format(AQ =VALUE ,CT = str(ContractRecordId),PN=getpartno,quote_revision_record_id=quote_revision_record_id)
					#sqlforupdatePT += "UPDATE SAQIFP SET ANNUAL_QUANTITY = '{AQ}',EXTENDED_UNIT_PRICE = '{UP}' where QUOTE_RECORD_ID ='{CT}' and  PART_NUMBER in {PN}".format(AQ =str(VALUE) ,CT = str(ContractRecordId),PN=tuple(selectPN))
					Sql.RunQuery(sqlforupdatePT)
					sqlforupdate += "UPDATE QT__SAQIFP SET  ANNUAL_QUANTITY = {AQ},EXTENDED_UNIT_PRICE = (UNIT_PRICE*{AQ}) where QUOTE_RECORD_ID ='{CT}' and  PART_NUMBER  = '{PN}'".format(AQ =VALUE ,CT = str(ContractRecordId),PN=getpartno)
					Sql.RunQuery(sqlforupdate)
			
			elif (TreeParentParam in ('Comprehensive Services','Complementary Products') or TreeTopSuperParentParam in ('Comprehensive Services','Complementary Products')) and obj_name == "SAQSAP":
				Sql.RunQuery("""UPDATE SAQSAP SET {column} = {value} WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{rev_rec_id}' AND {rec_name} = '{rec_id}' """.format(column=TITLE,value = ALLVALUES[index] if str(type(ALLVALUES))=="<type 'ArrayList'>" else ALLVALUES,QuoteRecordId = Qt_rec_id,rev_rec_id = Quote.GetGlobal("quote_revision_record_id"),rec_name = objh_head,rec_id = sql_obj.QUOTE_SERVICE_COV_OBJ_ASS_PM_KIT_RECORD_ID))
			else:
				Trace.Write("selected_rows---463----"+str(row)+'--'+str(obj_name))
				#A055S000P01-8729 start
				if obj_name == "SAQTRV":
					contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
					update_quote_rev = Sql.RunQuery("""UPDATE SAQTRV SET ACTIVE = {active_rev} WHERE QUOTE_RECORD_ID = '{QuoteRecordId}'""".format(QuoteRecordId=contract_quote_record_id,active_rev = 0))
					quote_revision_id = row.get("QUOTE_REVISION_RECORD_ID")
					active_rev = row.get("ACTIVE")
					Table.TableActions.Update(obj_name, objh_head, row)
					get_rev_detail = Sql.GetFirst("SELECT * FROM SAQTRV WHERE QUOTE_REVISION_RECORD_ID ='"+str(quote_revision_id)+"'")
					if active_rev == 'True':
						active_rev = 1
					else:
						active_rev = 0
					Trace.Write("cactive_rev----"+str(active_rev))

					Sql.RunQuery("""UPDATE SAQTMT SET QTEREV_ID = {newrev_inc},QTEREV_RECORD_ID = '{quote_revision_id}',ACTIVE_REV={active_rev} WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{QuoteRecordId}'""".format(quote_revision_id=quote_revision_id,newrev_inc= get_rev_detail.QTEREV_ID,QuoteRecordId=contract_quote_record_id,active_rev = int(active_rev)))
				elif obj_name =="SAQRSP":
					Sql = SQL()
					if len(TITLE.split(','))==1:
						Sql.RunQuery("""UPDATE SAQRSP SET {column} = '{value}' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{rev_rec_id}' AND {rec_name} = '{rec_id}' """.format(column=TITLE.split(',')[0],value = ALLVALUES[index] if str(type(ALLVALUES))=="<type 'ArrayList'>" else ALLVALUES,QuoteRecordId = Qt_rec_id,rev_rec_id = Quote.GetGlobal("quote_revision_record_id"),rec_name = objh_head,rec_id = sql_obj.QUOTE_REV_PO_PRODUCT_LIST_ID))
					else:
						Sql.RunQuery("""UPDATE SAQRSP SET {column} = {value} , {column1} = '{value1}' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{rev_rec_id}' AND {rec_name} = '{rec_id}' """.format(column=TITLE.split(',')[0],value = ALLVALUES[index] if str(type(ALLVALUES))=="<type 'ArrayList'>" else ALLVALUES,column1=TITLE.split(',')[1],value1 = ALLVALUES1[index] if str(type(ALLVALUES1))=="<type 'ArrayList'>" else ALLVALUES1,QuoteRecordId = Qt_rec_id,rev_rec_id = Quote.GetGlobal("quote_revision_record_id"),rec_name = objh_head,rec_id = sql_obj.QUOTE_REV_PO_PRODUCT_LIST_ID))
				else:
					Table.TableActions.Update(obj_name, objh_head, row)
				#A055S000P01-8729 end
				#Table.TableActions.Update(obj_name, objh_head, row)
				##Updating the fabname and fablocation id in bulk edit scenario starts....
		if obj_name == 'SAQICO':
			if TITLE != 'NET_PRICE' and TITLE != 'DISCOUNT':
				prtxcl_obj = Sql.GetFirst("Select TAX_CLASSIFICATION_RECORD_ID,TAX_CLASSIFICATION_DESCRIPTION,TAX_CLASSIFICATION_ID FROM PRTXCL WHERE  TAX_CLASSIFICATION_DESCRIPTION = '{SRVTAXCLA_DESCRIPTION}'".format(SRVTAXCLA_DESCRIPTION = str(VALUE)))
				#line_items_obj = """UPDATE SAQICO SET SRVTAXCLA_ID = '{TAX_CLASSIFICATION_ID}', SRVTAXCLA_RECORD_ID = '{SRVTAXCLA_RECORD_ID}' WHERE SRVTAXCLA_DESCRIPTION = '{SRVTAXCLA_DESCRIPTION}' and QUOTE_RECORD_ID = '{quote_record_id}' """.format(TAX_CLASSIFICATION_ID = prtxcl_obj.TAX_CLASSIFICATION_ID,SRVTAXCLA_RECORD_ID = prtxcl_obj.TAX_CLASSIFICATION_RECORD_ID,SRVTAXCLA_DESCRIPTION = str(VALUE),quote_record_id = str(ContractRecordId))
				#Sql.RunQuery(line_items_obj)
				quote_id = quote_id
				quote_record_id = str(Qt_rec_id)
				getting_cps_tax(quote_id,quote_record_id,item_lines_record_ids)
			elif TITLE == 'NET_PRICE':
				
				a = Sql.GetFirst("SELECT ISNULL(TARGET_PRICE,0) AS  TARGET_PRICE, SERVICE_ID,QUOTE_RECORD_ID,GREENBOOK,ISNULL(YEAR_OVER_YEAR,0) AS YEAR_OVER_YEAR,CONTRACT_VALID_FROM,CONTRACT_VALID_TO  FROM SAQICO (NOLOCK) WHERE CpqTableEntryId = {}".format(cpqid))
				
				if float(a.TARGET_PRICE) != 0.0 or float(a.TARGET_PRICE) != 0.00:
					discount =(float(a.TARGET_PRICE)-float(VALUE))/float(a.TARGET_PRICE)
					#Trace.Write("discount1="+str(discount))
					discount = discount*100.00
					#Trace.Write("discount2="+str(discount))
				else:
					discount = 0.00
				
				getdates = Sql.GetFirst("SELECT CONTRACT_VALID_FROM,CONTRACT_VALID_TO FROM SAQTMT WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{}'".format(a.QUOTE_RECORD_ID))
				
				
				import datetime as dt
				fmt = '%m/%d/%Y'
				d1 = dt.datetime.strptime(str(getdates.CONTRACT_VALID_FROM).split(" ")[0], fmt)
				d2 = dt.datetime.strptime(str(getdates.CONTRACT_VALID_TO).split(" ")[0], fmt)
				days = (d2 - d1).days
				Trace.Write("number of days---------------->"+str((d2 - d1).days))
				
				
				yoy = float(a.YEAR_OVER_YEAR)
				#VALUE = float(a.SALES_DISCOUNT_PRICE)-amt
				year1 = float(VALUE)
				year2 = 0.00
				year3 = 0.00
				year4 = 0.00
				year5 = 0.00
				dec1 = (float(VALUE)*yoy)/100
				Trace.Write("dec1---"+str(dec1))

				if days > 365:
					year2 = float(VALUE) - dec1
					dec2 = (year2*yoy)/100
					Trace.Write("dec2---"+str(dec2))
				if days > 730:
					year3 = year2 - dec2
					dec3 = (year3*yoy)/100
					Trace.Write("dec3---"+str(dec3))
				if days > 1095:
					year4 = year3 - dec3
					dec4 = (year4*yoy)/100
				if days > 1460:
					year5 = year4 - dec4
				
				ext_price = year1 + year2 + year3 + year4 + year5

				#Sql.RunQuery("UPDATE SAQICO SET NET_PRICE = '{VALUE}',NET_PRICE_INGL_CURR = {VALUE}, DISCOUNT = '{discount}',YEAR_1 = {y1},YEAR_2 = {y2},YEAR_3={y3},YEAR_4={y4},YEAR_5 = {y5},NET_VALUE = {ext},TOTAL_AMOUNT_INGL_CURR = {ext} WHERE CpqTableEntryId = {cpqid}".format(VALUE=VALUE,cpqid=cpqid,discount=discount,y1=year1,y2=year2,y3=year3,y4=year4,y5=year5,ext=ext_price))

				b = Sql.GetFirst("SELECT  SUM(TARGET_PRICE) AS TARGET_PRICE FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(a.QUOTE_RECORD_ID,a.SERVICE_ID,quote_revision_record_id))
				#(float(a.TARGET_PRICE)-float(VALUE))/float(a.TARGET_PRICE)
				
				TotalDiscount = ((float(b.TARGET_PRICE)-float(b.SUM_PRICE))/float(b.TARGET_PRICE)) * 100.00
				Trace.Write("Total Discount = "+str(TotalDiscount))

				c = Sql.GetFirst("SELECT SUM(NET_PRICE) AS SUM_PRICE, SUM(YEAR_1) AS YEAR1, SUM(YEAR_2) AS YEAR2, SUM(YEAR_3) AS YEAR3, SUM(YEAR_4) AS YEAR4, SUM(YEAR_5) AS YEAR5 FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}' AND GREENBOOK = '{}' AND QTEREV_RECORD_ID = '{}'".format(a.QUOTE_RECORD_ID,a.SERVICE_ID,a.GREENBOOK,quote_revision_record_id))
				
				saqitm_extprice = b.YEAR1 + b.YEAR2 + b.YEAR3 + b.YEAR4 + b.YEAR5

				# Sql.RunQuery("UPDATE SAQITM SET NET_PRICE = '{}',YEAR_1 = {y1},YEAR_2 = {y2},YEAR_3={y3},YEAR_4={y4},YEAR_5 = {y5}, NET_VALUE = {ext}  WHERE QUOTE_RECORD_ID = '{}' AND SERVICE_ID LIKE '%{}%' AND QTEREV_RECORD_ID = '{quote_revision_record_id}'".format(float(b.SUM_PRICE),Quote.GetGlobal("contract_quote_record_id"),a.SERVICE_ID,y1=b.YEAR1,y2=b.YEAR2,y3=b.YEAR3,y4=b.YEAR4,y5=b.YEAR5,ext=saqitm_extprice,quote_revision_record_id=quote_revision_record_id))

				
				# Sql.RunQuery("UPDATE SAQIGB SET NET_PRICE = '{}',YEAR_1 = {y1},YEAR_2 = {y2},YEAR_3={y3},YEAR_4={y4},YEAR_5 = {y5}  WHERE QUOTE_RECORD_ID = '{}' AND SERVICE_ID LIKE '%{}%' AND GREENBOOK = '{}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}'".format(float(b.SUM_PRICE),Quote.GetGlobal("contract_quote_record_id"),a.SERVICE_ID,a.GREENBOOK,y1=c.YEAR1,y2=c.YEAR2,y3=c.YEAR3,y4=c.YEAR4,y5=c.YEAR5,quote_revision_record_id=quote_revision_record_id))

				getServiceSum = Sql.GetFirst("SELECT SUM(NET_PRICE) AS SUM_PRICE,SUM(TARGET_PRICE) AS TARGET_PRICE FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(a.QUOTE_RECORD_ID,quote_revision_record_id))
				
				TotalServiceDiscount = ((float(getServiceSum.TARGET_PRICE)-float(getServiceSum.SUM_PRICE))/float(getServiceSum.TARGET_PRICE)) *100.00
				Trace.Write("Total Service Discount = "+str(TotalServiceDiscount))
				get_curr = str(Quote.GetCustomField('Currency').Content)

				# Quote.GetCustomField('TOTAL_NET_VALUE').Content =str(getServiceSum.NET_VALUE) + " " + get_curr
				# Quote.GetCustomField('TOTAL_NET_PRICE').Content =str(getServiceSum.SUM_PRICE) + " " + get_curr
				# Quote.GetCustomField('YEAR_1').Content =str(getServiceSum.YEAR1) + " " + get_curr
				# Quote.GetCustomField('YEAR_2').Content =str(getServiceSum.YEAR2) + " " + get_curr
				# Quote.GetCustomField('YEAR_3').Content =str(getServiceSum.YEAR3) + " " + get_curr
				# Quote.GetCustomField('DISCOUNT').Content =str(TotalServiceDiscount)
				for item in Quote.MainItems:
					if item.PartNumber == a.SERVICE_ID:
						item.NET_PRICE.Value = str(b.SUM_PRICE)
						item.YEAR_1.Value = str(b.YEAR1)
						item.YEAR_2.Value = str(b.YEAR2)
						item.YEAR_3.Value = str(b.YEAR3)
						item.YEAR_4.Value = str(b.YEAR4)
						item.YEAR_5.Value = str(b.YEAR5)
						item.EXTENDED_PRICE.Value = str(b.NET_VALUE)
						item.DISCOUNT.Value = str(TotalDiscount)
				Quote.Save()
				Sql.RunQuery("""UPDATE SAQTRV
						SET 									
						SAQTRV.NET_PRICE_INGL_CURR = IQ.NET_PRICE_INGL_CURR,						
						SAQTRV.DISCOUNT_PERCENT = '{discount}'
						
						FROM SAQTRV (NOLOCK)
						INNER JOIN (SELECT SAQICO.QUOTE_RECORD_ID, SAQICO.QTEREV_RECORD_ID,
									SUM(ISNULL(SAQICO.NET_PRICE_INGL_CURR, 0)) as NET_PRICE_INGL_CURR			
									
									FROM SAQICO (NOLOCK) WHERE SAQICO.QUOTE_RECORD_ID = '{quote_rec_id}' AND SAQICO.QTEREV_RECORD_ID = '{quote_revision_rec_id}' GROUP BY SAQICO.QTEREV_RECORD_ID, SAQICO.QUOTE_RECORD_ID) IQ ON SAQTRV.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND SAQTRV.QUOTE_REVISION_RECORD_ID = IQ.QTEREV_RECORD_ID
						WHERE SAQTRV.QUOTE_RECORD_ID = '{quote_rec_id}' AND SAQTRV.QUOTE_REVISION_RECORD_ID = '{quote_revision_rec_id}' 	""".format(discount = str(TotalServiceDiscount), quote_rec_id = Quote.GetGlobal("contract_quote_record_id"), quote_revision_rec_id = quote_revision_record_id ) )

				getPRCFVA = Sql.GetFirst("SELECT FACTOR_PCTVAR FROM PRCFVA (NOLOCK) WHERE FACTOR_VARIABLE_ID = '{}' AND FACTOR_ID = 'SLDISC' ".format(a.SERVICE_ID))
				try:
					if float(getPRCFVA.FACTOR_PCTVAR) < discount:
						Sql.RunQuery("UPDATE SAQICO SET STATUS = 'APPROVAL REQUIRED' WHERE CpqTableEntryId = {}".format(cpqid))
						# Sql.RunQuery("UPDATE SAQITM SET PRICING_STATUS = 'APPROVAL REQUIRED' WHERE QUOTE_RECORD_ID = '{}'  AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID LIKE '%{}%'".format(Quote.GetGlobal("contract_quote_record_id"),a.SERVICE_ID,quote_revision_record_id))
				except:
					Trace.Write("NO STATUS UPDATE")
			elif TITLE == 'DISCOUNT':
				if '%' in VALUE:
					VALUE = VALUE.replace('%','')
				a = Sql.GetFirst("SELECT ISNULL(TARGET_PRICE,0) AS  TARGET_PRICE, SERVICE_ID,QUOTE_RECORD_ID,GREENBOOK,FABLOCATION_ID,ISNULL(YEAR_OVER_YEAR,0) AS YEAR_OVER_YEAR,CONTRACT_VALID_FROM,CONTRACT_VALID_TO  FROM SAQICO (NOLOCK) WHERE CpqTableEntryId = {}".format(cpqid))
				amt = 0.00
				if float(a.TARGET_PRICE) != 0.0 or float(a.TARGET_PRICE) != 0.00:
					if "+" not in VALUE and "-" not in VALUE:
						#discount =(float(VALUE)/float(a.SALES_DISCOUNT_PRICE))*100.00
						amt = float(a.TARGET_PRICE) - ((float(VALUE)*float(a.TARGET_PRICE))/100)
					elif "-" in VALUE:
						VALUE = VALUE.replace("-","").replace("%","").strip()
						amt = float(a.TARGET_PRICE) + ((float(VALUE)*float(a.TARGET_PRICE))/100)
						VALUE = "-"+str(VALUE)
					else:
						amt = 0.00
				
				Sql.RunQuery("UPDATE SAQICO SET NET_PRICE = '{VALUE}', DISCOUNT = {discount} WHERE CpqTableEntryId = {cpqid}".format(VALUE=float(amt),cpqid=cpqid,discount=float(VALUE)))

				b = Sql.GetFirst("SELECT SUM(NET_PRICE) AS SUM_PRICE FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(a.QUOTE_RECORD_ID,a.SERVICE_ID,quote_revision_record_id))

				#Sql.RunQuery("UPDATE SAQITM SET NET_PRICE = '{}' WHERE QUOTE_RECORD_ID = '{}' AND SERVICE_ID LIKE '%{}%'".format(float(b.SUM_PRICE),Quote.GetGlobal("contract_quote_record_id"),a.SERVICE_ID))
				getdates = Sql.GetFirst("SELECT CONTRACT_VALID_FROM,CONTRACT_VALID_TO FROM SAQTMT WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(a.QUOTE_RECORD_ID,quote_revision_record_id))
				
				
				import datetime as dt
				fmt = '%m/%d/%Y'
				d1 = dt.datetime.strptime(str(getdates.CONTRACT_VALID_FROM).split(" ")[0], fmt)
				d2 = dt.datetime.strptime(str(getdates.CONTRACT_VALID_TO).split(" ")[0], fmt)
				days = (d2 - d1).days
				Trace.Write("number of days---------------->"+str((d2 - d1).days))
				
				
				yoy = float(a.YEAR_OVER_YEAR)
				#VALUE = amt
				year1 = float(amt)
				year2 = 0.00
				year3 = 0.00
				year4 = 0.00
				year5 = 0.00
				dec1 = (float(amt)*yoy)/100
				Trace.Write("dec1---"+str(dec1))

				if days > 365:
					year2 = float(amt) - dec1
					dec2 = (year2*yoy)/100
					Trace.Write("dec2---"+str(dec2))
				if days > 730:
					year3 = year2 - dec2
					dec3 = (year3*yoy)/100
					Trace.Write("dec3---"+str(dec3))
				if days > 1095:
					year4 = year3 - dec3
					dec4 = (year4*yoy)/100
				if days > 1460:
					year5 = year4 - dec4
				
				ext_price = year1 + year2 + year3 + year4 + year5

				#Sql.RunQuery("UPDATE SAQICO SET NET_PRICE = '{VALUE}',NET_PRICE_INGL_CURR = '{VALUE}', DISCOUNT = '{discount}',YEAR_1 = {y1},YEAR_2 = {y2},YEAR_3={y3},YEAR_4={y4},YEAR_5 = {y5},NET_VALUE = {ext} WHERE CpqTableEntryId = {cpqid}".format(VALUE=amt,cpqid=cpqid,discount=VALUE,y1=year1,y2=year2,y3=year3,y4=year4,y5=year5,ext=ext_price))

				b = Sql.GetFirst("SELECT SUM(NET_PRICE) AS SUM_PRICE, SUM(TARGET_PRICE) AS TARGET_PRICE FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(a.QUOTE_RECORD_ID,a.SERVICE_ID,quote_revision_record_id))
				
				TotalDiscount = ((float(b.TARGET_PRICE)-float(b.SUM_PRICE))/float(b.TARGET_PRICE)) * 100.00
				Trace.Write("Total Discount = "+str(TotalDiscount))

				c = Sql.GetFirst("SELECT SUM(NET_PRICE) AS SUM_PRICE,SUM(TARGET_PRICE) AS TARGET_PRICE FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}' AND GREENBOOK = '{}' AND QTEREV_RECORD_ID = '{}'".format(a.QUOTE_RECORD_ID,a.SERVICE_ID,a.GREENBOOK,quote_revision_record_id))
				greenbook_discount = (float(c.TARGET_PRICE) - float(c.SUM_PRICE))*100/float(c.TARGET_PRICE)
				fab = Sql.GetFirst("SELECT SUM(NET_PRICE) AS SUM_PRICE, SUM(TARGET_PRICE) AS TARGET_PRICE FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}' AND FABLOCATION_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(a.QUOTE_RECORD_ID,a.SERVICE_ID,a.FABLOCATION_ID,quote_revision_record_id))
				
				fab_discount = (float(fab.TARGET_PRICE) - float(fab.SUM_PRICE))*100/float(fab.TARGET_PRICE)
				fab_net_value = fab.YEAR1 + fab.YEAR2 + fab.YEAR3 + fab.YEAR4 + fab.YEAR5
				greenbook_net_value = c.YEAR1 + c.YEAR2 + c.YEAR3 + c.YEAR4 + c.YEAR5
				saqitm_extprice = b.YEAR1 + b.YEAR2 + b.YEAR3 + b.YEAR4 + b.YEAR5

				# Sql.RunQuery("UPDATE SAQITM SET NET_PRICE = '{}',YEAR_1 = {y1},YEAR_2 = {y2},YEAR_3={y3},YEAR_4={y4},YEAR_5 = {y5}, NET_VALUE = {ext}  WHERE QUOTE_RECORD_ID = '{}' AND SERVICE_ID LIKE '%{}%' AND QTEREV_RECORD_ID = '{quote_revision_record_id}'".format(float(b.SUM_PRICE),Quote.GetGlobal("contract_quote_record_id"),a.SERVICE_ID,y1=b.YEAR1,y2=b.YEAR2,y3=b.YEAR3,y4=b.YEAR4,y5=b.YEAR5,ext=saqitm_extprice,quote_revision_record_id=quote_revision_record_id))

				
				# Sql.RunQuery("UPDATE SAQIGB SET NET_VALUE = {},DISCOUNT = '{}',NET_PRICE = '{}',YEAR_1 = {y1},YEAR_2 = {y2},YEAR_3={y3},YEAR_4={y4},YEAR_5 = {y5}  WHERE QUOTE_RECORD_ID = '{}' AND SERVICE_ID LIKE '%{}%' AND GREENBOOK = '{}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}'".format(greenbook_net_value,greenbook_discount,float(b.SUM_PRICE),Quote.GetGlobal("contract_quote_record_id"),a.SERVICE_ID,a.GREENBOOK,y1=c.YEAR1,y2=c.YEAR2,y3=c.YEAR3,y4=c.YEAR4,y5=c.YEAR5,quote_revision_record_id=quote_revision_record_id))

				# Sql.RunQuery("UPDATE SAQIFL SET NET_VALUE = {},DISCOUNT = '{}',NET_PRICE = '{}',YEAR_1 = {y1},YEAR_2 = {y2},YEAR_3={y3},YEAR_4={y4},YEAR_5 = {y5}  WHERE QUOTE_RECORD_ID = '{}' AND SERVICE_ID LIKE '%{}%' AND FABLOCATION_ID = '{}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}'".format(fab_net_value,fab_discount,float(b.SUM_PRICE),Quote.GetGlobal("contract_quote_record_id"),a.SERVICE_ID,a.FABLOCATION_ID,y1=c.YEAR1,y2=c.YEAR2,y3=c.YEAR3,y4=c.YEAR4,y5=c.YEAR5,quote_revision_record_id=quote_revision_record_id))

				getServiceSum = Sql.GetFirst("SELECT SUM(NET_PRICE) AS SUM_PRICE,SUM(TARGET_PRICE) AS TARGET_PRICE FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(a.QUOTE_RECORD_ID,quote_revision_record_id))
				
				TotalServiceDiscount = ((float(getServiceSum.TARGET_PRICE)-float(getServiceSum.SUM_PRICE))/float(getServiceSum.TARGET_PRICE)) *100.00
				Trace.Write("Total Service Discount = "+str(TotalServiceDiscount))
				get_curr = str(Quote.GetCustomField('Currency').Content)

				# Quote.GetCustomField('TOTAL_NET_VALUE').Content =str(getServiceSum.NET_VALUE) + " " + get_curr
				# Quote.GetCustomField('TOTAL_NET_PRICE').Content =str(getServiceSum.SUM_PRICE) + " " + get_curr
				# Quote.GetCustomField('YEAR_1').Content =str(getServiceSum.YEAR1) + " " + get_curr
				# Quote.GetCustomField('YEAR_2').Content =str(getServiceSum.YEAR2) + " " + get_curr
				# Quote.GetCustomField('YEAR_3').Content =str(getServiceSum.YEAR3) + " " + get_curr
				# Quote.GetCustomField('DISCOUNT').Content =str(TotalServiceDiscount) + "%"
				for item in Quote.MainItems:
					if item.PartNumber == a.SERVICE_ID:
						item.NET_PRICE.Value = str(b.SUM_PRICE)
						item.YEAR_1.Value = str(b.YEAR1)
						item.YEAR_2.Value = str(b.YEAR2)
						item.YEAR_3.Value = str(b.YEAR3)
						item.YEAR_4.Value = str(b.YEAR4)
						item.YEAR_5.Value = str(b.YEAR5)
						item.NET_VALUE.Value = str(b.NET_VALUE)
						item.DISCOUNT.Value = str(TotalDiscount)
				Quote.Save()

				Sql.RunQuery("""UPDATE SAQTRV
						SET 									
						SAQTRV.NET_PRICE_INGL_CURR = IQ.NET_PRICE_INGL_CURR,						
						
						SAQTRV.DISCOUNT_PERCENT = '{discount}'
						
						FROM SAQTRV (NOLOCK)
						INNER JOIN (SELECT SAQICO.QUOTE_RECORD_ID, SAQICO.QTEREV_RECORD_ID,
									SUM(ISNULL(SAQICO.NET_PRICE_INGL_CURR, 0)) as NET_PRICE_INGL_CURR,									
									FROM SAQICO (NOLOCK) WHERE SAQICO.QUOTE_RECORD_ID = '{quote_rec_id}' AND SAQICO.QTEREV_RECORD_ID = '{quote_revision_rec_id}' GROUP BY SAQICO.QTEREV_RECORD_ID, SAQICO.QUOTE_RECORD_ID) IQ ON SAQTRV.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND SAQTRV.QUOTE_REVISION_RECORD_ID = IQ.QTEREV_RECORD_ID
						WHERE SAQTRV.QUOTE_RECORD_ID = '{quote_rec_id}' AND SAQTRV.QUOTE_REVISION_RECORD_ID = '{quote_revision_rec_id}' 	""".format(discount = str(TotalServiceDiscount), quote_rec_id = Quote.GetGlobal("contract_quote_record_id"), quote_revision_rec_id = quote_revision_record_id ) )

				getPRCFVA = Sql.GetFirst("SELECT FACTOR_PCTVAR FROM PRCFVA (NOLOCK) WHERE FACTOR_VARIABLE_ID = '{}' AND FACTOR_ID = 'SLDISC' ".format(a.SERVICE_ID))
				try:
					if float(getPRCFVA.FACTOR_PCTVAR) < float(VALUE):
						Sql.RunQuery("UPDATE SAQICO SET STATUS = 'APPROVAL REQUIRED' WHERE CpqTableEntryId = {}".format(cpqid))
						# Sql.RunQuery("UPDATE SAQITM SET PRICING_STATUS = 'APPROVAL REQUIRED' WHERE QUOTE_RECORD_ID = '{}'  AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID LIKE '%{}%'".format(Quote.GetGlobal("contract_quote_record_id"),a.SERVICE_ID,quote_revision_record_id))
				except:
					Trace.Write("NO STATUS UPDATE")
				#getPRCFVA = Sql.GetFirst("SELECT FACTOR_PCTVAR FROM PRCFVA (NOLOCK) WHERE FACTOR_VARIABLE_ID = '{}' AND FACTOR_ID = 'SLDISC' ".format(a.SERVICE_ID))

				#if float(getPRCFVA.FACTOR_PCTVAR) < discount:
				#Sql.RunQuery("UPDATE SAQITM SET PRICING_STATUS = 'APPROVAL REQUIRED' WHERE QUOTE_RECORD_ID = '{}' AND SERVICE_ID LIKE '%{}%'".format(Quote.GetGlobal("contract_quote_record_id"),a.SERVICE_ID))
		if obj_name == "SAQRIT":
			Trace.Write("@802")
			Sql = SQL()
			ALLVALUES1 = str(Param.ALLVALUES1).replace("[","").replace("]","").split(",")
			ALLVALUES = str(Param.ALLVALUES).replace("[","").replace("]","").split(",")
			#ALLVALUES = list(ALLVALUES)
			#ALLVALUES1 = list(ALLVALUES1)
			count = 0
			Trace.Write('ALLVALUES--'+str(ALLVALUES))
			Trace.Write('ALLVALUES1--'+str(ALLVALUES1))
			for x,y in zip(ALLVALUES,ALLVALUES1):
				Trace.Write("x="+str(x))
				Trace.Write("y="+str(y))
				#Sql.RunQuery("UPDATE SAQRIT SET COMVAL_INGL_CURR='{}' WHERE CpqTableEntryId = '{}'".format(x,selected_rows_cpqid[count]))
				#count += 1
				Sql.RunQuery("UPDATE SAQRIT SET ESTVAL_INGL_CURR = '{}',COMVAL_INGL_CURR='{}' WHERE CpqTableEntryId = '{}'".format(float(str(x).replace("USD","").replace(" ","").replace("'","").replace('"','')),float(str(y).replace("USD","").replace(" ","").replace("'","").replace('"','').replace("''","").replace('""','')),selected_rows_cpqid[count]))
				count += 1
			#A055S000P01-12656 start
			tax_percent_amt = commitval = exc_rate = 0
			net_value_tax  = ''
			Sql = SQL()
			get_quote_item_details = Sql.GetList("select * from SAQRIT where QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{rev_rec_id}'".format(QuoteRecordId = Qt_rec_id,rev_rec_id = Quote.GetGlobal("quote_revision_record_id")))
			if get_quote_item_details:
				for val in get_quote_item_details:
					item_rec = val.QUOTE_REVISION_CONTRACT_ITEM_ID
					if val.TAX_PERCENTAGE:
						tax_percent_amt = val.TAX_PERCENTAGE
					if val.EXCHANGE_RATE:
						exc_rate = val.EXCHANGE_RATE
					if val.COMVAL_INGL_CURR:
						commitval = val.COMVAL_INGL_CURR
						net_price_with_exc_rate= float(commitval) * float(exc_rate)
						tax_amt_update  = float(commitval) * float(tax_percent_amt)
						net_value_tax = tax_amt_update + commitval
						net_price_update = "UPDATE SAQRIT SET NET_PRICE = '{net_pr_exc}',NET_PRICE_INGL_CURR= '{commitvalue}',TAX_AMOUNT ={tax_amt_update},TAX_AMOUNT_INGL_CURR = {tax_amt_update},NET_VALUE = {net_value_tax},NET_VALUE_INGL_CURR={net_value_tax} where QUOTE_RECORD_ID = '{qt_rec}' and QUOTE_REVISION_CONTRACT_ITEM_ID = '{item_rec}' AND QTEREV_RECORD_ID = '{rev_rec_id}'".format(net_pr_exc = net_price_with_exc_rate,commitvalue = val.COMVAL_INGL_CURR,tax_amt_update=tax_amt_update,qt_rec= Qt_rec_id,item_rec=item_rec,net_value_tax=net_value_tax,rev_rec_id =  Quote.GetGlobal("quote_revision_record_id"))
						Sql.RunQuery(net_price_update)

			#update SAQTRV based on commit changes--start
			Sql.RunQuery("""UPDATE SAQTRV
						SET 
						SAQTRV.TAX_AMOUNT_INGL_CURR = IQ.TAX_AMOUNT_INGL_CURR,						
						SAQTRV.NET_PRICE_INGL_CURR = IQ.NET_PRICE_INGL_CURR,
						SAQTRV.NET_VALUE_INGL_CURR = IQ.NET_VALUE_INGL_CURR
												
						FROM SAQTRV (NOLOCK)
						INNER JOIN (SELECT SAQRIT.QUOTE_RECORD_ID, SAQRIT.QTEREV_RECORD_ID,
									SUM(ISNULL(SAQRIT.TAX_AMOUNT_INGL_CURR, 0)) as TAX_AMOUNT_INGL_CURR,
									SUM(ISNULL(SAQRIT.NET_PRICE_INGL_CURR, 0)) as NET_PRICE_INGL_CURR,
									SUM(ISNULL(SAQRIT.NET_VALUE_INGL_CURR, 0)) as NET_VALUE_INGL_CURR
									FROM SAQRIT (NOLOCK) WHERE SAQRIT.QUOTE_RECORD_ID = '{quote_rec_id}' AND SAQRIT.QTEREV_RECORD_ID = '{quote_revision_rec_id}' GROUP BY SAQRIT.QTEREV_RECORD_ID, SAQRIT.QUOTE_RECORD_ID) IQ ON SAQTRV.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND SAQTRV.QUOTE_REVISION_RECORD_ID = IQ.QTEREV_RECORD_ID
						WHERE SAQTRV.QUOTE_RECORD_ID = '{quote_rec_id}' AND SAQTRV.QUOTE_REVISION_RECORD_ID = '{quote_revision_rec_id}' 	""".format(quote_rec_id = Qt_rec_id ,quote_revision_rec_id = Quote.GetGlobal("quote_revision_record_id") ) )
			#update SAQTRV based on commit changes--end

			#update SAQRIS -start
			Sql.RunQuery("""UPDATE SAQRIS
						SET 
						SAQRIS.TAX_AMOUNT_INGL_CURR = IQ.TAX_AMOUNT_INGL_CURR,						
						SAQRIS.NET_PRICE_INGL_CURR = IQ.NET_PRICE_INGL_CURR,
						SAQRIS.NET_PRICE = IQ.NET_PRICE,
						SAQRIS.NET_VALUE = IQ.NET_VALUE,
						SAQRIS.NET_VALUE_INGL_CURR = IQ.NET_VALUE_INGL_CURR,
						SAQRIS.TAX_AMOUNT = IQ.TAX_AMOUNT
												
						FROM SAQRIS (NOLOCK)
						INNER JOIN (SELECT SAQRIT.QUOTE_RECORD_ID, SAQRIT.QTEREV_RECORD_ID,SAQRIT.SERVICE_ID,
									SUM(ISNULL(SAQRIT.TAX_AMOUNT_INGL_CURR, 0)) as TAX_AMOUNT_INGL_CURR,
									SUM(ISNULL(SAQRIT.NET_PRICE_INGL_CURR, 0)) as NET_PRICE_INGL_CURR,
									SUM(ISNULL(SAQRIT.NET_PRICE, 0)) as NET_PRICE,
									SUM(ISNULL(SAQRIT.NET_VALUE, 0)) as NET_VALUE,
									SUM(ISNULL(SAQRIT.NET_VALUE_INGL_CURR, 0)) as NET_VALUE_INGL_CURR,
									SUM(ISNULL(SAQRIT.TAX_AMOUNT, 0)) as TAX_AMOUNT
									FROM SAQRIT (NOLOCK) WHERE SAQRIT.QUOTE_RECORD_ID = '{quote_rec_id}' AND SAQRIT.QTEREV_RECORD_ID = '{quote_revision_rec_id}' GROUP BY SAQRIT.QTEREV_RECORD_ID, SAQRIT.QUOTE_RECORD_ID,SAQRIT.SERVICE_ID) IQ ON SAQRIS.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND SAQRIS.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID
						WHERE SAQRIS.QUOTE_RECORD_ID = '{quote_rec_id}' AND SAQRIS.QTEREV_RECORD_ID = '{quote_revision_rec_id}' 	""".format(quote_rec_id = Qt_rec_id ,quote_revision_rec_id = Quote.GetGlobal("quote_revision_record_id") ) )
			_insert_billing_matrix()
			#update SAQRIS end
			#A055S000P01-12656 end

		if obj_name == "SAQSCO":
			getfab = Sql.GetFirst("SELECT FABLOCATION_NAME, FABLOCATION_RECORD_ID FROM SAQFBL WHERE QUOTE_RECORD_ID = '{}' AND FABLOCATION_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(Quote.GetGlobal("contract_quote_record_id"),VALUE,quote_revision_record_id))
			fabname = getfab.FABLOCATION_NAME
			fabrec = getfab.FABLOCATION_RECORD_ID		
			if 	SELECTALL != "no":
				Sql.RunQuery("UPDATE SAQSCO SET FABLOCATION_ID = '{VALUE}',FABLOCATION_NAME = '{name}',FABLOCATION_RECORD_ID = '{rec}' WHERE QUOTE_RECORD_ID = '{Quote}' AND RELOCATION_EQUIPMENT_TYPE = 'RECEIVING EQUIPMENT' AND SERVICE_ID= '{ServiceId}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}'".format(VALUE=VALUE,Quote=Quote.GetGlobal("contract_quote_record_id"),ServiceId=Quote.GetGlobal("TreeParentLevel0"),name=fabname,rec=fabrec,quote_revision_record_id=quote_revision_record_id))

				geteqp = Sql.GetList("SELECT * FROM SAQSCO WHERE QUOTE_RECORD_ID = '{Quote}' AND RELOCATION_EQUIPMENT_TYPE = 'RECEIVING EQUIPMENT' AND SERVICE_ID= '{ServiceId}' AND QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID IN {recordslist} AND QTEREV_RECORD_ID = '{quote_revision_record_id}'".format(Quote=Quote.GetGlobal("contract_quote_record_id"),ServiceId=Quote.GetGlobal("TreeParentLevel0"),name=fabname,rec=fabrec,recordslist=recordslist,quote_revision_record_id=quote_revision_record_id))
				if geteqp:
					recordslist = str(tuple([fab.EQUIPMENT_ID for fab in geteqp])).replace(",)",')')

					Sql.RunQuery("UPDATE SAQSCA SET FABLOCATION_ID = '{VALUE}',FABLOCATION_NAME = '{name}',FABLOCATION_RECORD_ID = '{rec}' WHERE QUOTE_RECORD_ID = '{Quote}' AND SERVICE_ID= '{ServiceId}' AND EQUIPMENT_ID IN {recordslist} AND QTEREV_RECORD_ID = '{quote_revision_record_id}'".format(VALUE=VALUE,Quote=Quote.GetGlobal("contract_quote_record_id"),ServiceId=Quote.GetGlobal("TreeParentLevel0"),name=fabname,rec=fabrec,recordslist=recordslist,quote_revision_record_id=quote_revision_record_id))
			else:
				Sql.RunQuery("UPDATE SAQSCO SET FABLOCATION_ID = '{VALUE}',FABLOCATION_NAME = '{name}',FABLOCATION_RECORD_ID = '{rec}' WHERE QUOTE_RECORD_ID = '{Quote}' AND RELOCATION_EQUIPMENT_TYPE = 'RECEIVING EQUIPMENT' AND SERVICE_ID= '{ServiceId}' AND QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID IN {recordslist} AND QTEREV_RECORD_ID = '{quote_revision_record_id}'".format(VALUE=VALUE,Quote=Quote.GetGlobal("contract_quote_record_id"),ServiceId=Quote.GetGlobal("TreeParentLevel0"),name=fabname,rec=fabrec,recordslist=recordslist,quote_revision_record_id=quote_revision_record_id))

				geteqp = Sql.GetList("SELECT * FROM SAQSCO WHERE QUOTE_RECORD_ID = '{Quote}' AND RELOCATION_EQUIPMENT_TYPE = 'RECEIVING EQUIPMENT' AND SERVICE_ID= '{ServiceId}' AND QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID IN {recordslist}  AND QTEREV_RECORD_ID = '{quote_revision_record_id}'".format(Quote=Quote.GetGlobal("contract_quote_record_id"),ServiceId=Quote.GetGlobal("TreeParentLevel0"),name=fabname,rec=fabrec,recordslist=recordslist,quote_revision_record_id=quote_revision_record_id))
				if geteqp:
					recordslist = str(tuple([fab.EQUIPMENT_ID for fab in geteqp])).replace(",)",')')

					Sql.RunQuery("UPDATE SAQSCA SET FABLOCATION_ID = '{VALUE}',FABLOCATION_NAME = '{name}',FABLOCATION_RECORD_ID = '{rec}' WHERE QUOTE_RECORD_ID = '{Quote}'  AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND SERVICE_ID= '{ServiceId}' AND EQUIPMENT_ID IN {recordslist}".format(VALUE=VALUE,Quote=Quote.GetGlobal("contract_quote_record_id"),ServiceId=Quote.GetGlobal("TreeParentLevel0"),name=fabname,rec=fabrec,recordslist=recordslist,quote_revision_record_id=quote_revision_record_id))
					
			'''Sql.RunQuery("UPDATE SAQSFE SET FABLOCATION_ID = '{VALUE}',FABLOCATION_NAME = '{name}',FABLOCATION_RECORD_ID = '{rec}' WHERE QUOTE_RECORD_ID = '{Quote}' AND SERVICE_ID= '{ServiceId}' {SingleRow}".format(VALUE=VALUE,Quote=Quote.GetGlobal("contract_quote_record_id"),SingleRow=" AND CpqTableEntryId = '"+str(cpqid) + "'" if SELECTALL == "no" else "",ServiceId=Quote.GetGlobal("TreeParentLevel0"),name=fabname,rec=fabrec))
			Sql.RunQuery("UPDATE SAQSGE SET FABLOCATION_ID = '{VALUE}',FABLOCATION_NAME = '{name}',FABLOCATION_RECORD_ID = '{rec}' WHERE QUOTE_RECORD_ID = '{Quote}' AND SERVICE_ID= '{ServiceId}' {SingleRow}".format(VALUE=VALUE,Quote=Quote.GetGlobal("contract_quote_record_id"),SingleRow=" AND CpqTableEntryId = '"+str(cpqid) + "'" if SELECTALL == "no" else "",ServiceId=Quote.GetGlobal("TreeParentLevel0"),name=fabname,rec=fabrec))
			Sql.RunQuery("""UPDATE SAQSCE SET FABLOCATION_ID = '{VALUE}',FABLOCATION_NAME = '{name}',FABLOCATION_RECORD_ID = '{rec}' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND SERVICE_ID= '{ServiceId}' {SingleRow}""".format(
			VALUE=VALUE,
			UserId=User.Id, 
			QuoteRecordId=Quote.GetGlobal("contract_quote_record_id"),
			name=fabname,
			rec=fabrec,
			ServiceId=Quote.GetGlobal("TreeParentLevel0"),SingleRow=" AND SAQSCO.CpqTabl """eEntryId = '"+str(cpqid) + "'" if SELECTALL == "no" else ""))'''
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
					QTEREV_RECORD_ID,
					QTEREV_ID,
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
					SAQSCO.FABLOCATION_ID,
					MAFBLC.FAB_LOCATION_NAME,
					MAFBLC.FAB_LOCATION_RECORD_ID,
					SAQSCO.SERVICE_ID,
					SAQSCO.SERVICE_TYPE,
					SAQSCO.SERVICE_DESCRIPTION,
					SAQSCO.SERVICE_RECORD_ID,
					MAFBLC.STATUS,
					SAQSCO.QUOTE_ID,
					SAQSCO.QUOTE_NAME,
					SAQSCO.QUOTE_RECORD_ID,
					SAQSCO.MNT_PLANT_ID,
					SAQSCO.MNT_PLANT_NAME,
					SAQSCO.MNT_PLANT_RECORD_ID,
					MAFBLC.ADDRESS_1,
					MAFBLC.ADDRESS_2,
					MAFBLC.CITY,
					MAFBLC.COUNTRY,
					MAFBLC.COUNTRY_RECORD_ID,
					SAQSCO.SALESORG_ID,
					SAQSCO.SALESORG_NAME,
					SAQSCO.SALESORG_RECORD_ID,
					SAQSCO.CONTRACT_VALID_FROM,
					SAQSCO.CONTRACT_VALID_TO,
					SAQSCO.PAR_SERVICE_DESCRIPTION,
					SAQSCO.PAR_SERVICE_ID,
					SAQSCO.PAR_SERVICE_RECORD_ID,
					SAQSCO.QTEREV_RECORD_ID,
					SAQSCO.QTEREV_ID
					FROM SAQSCO (NOLOCK)
					JOIN MAFBLC (NOLOCK) ON SAQSCO.FABLOCATION_ID = MAFBLC.FAB_LOCATION_ID
					WHERE SAQSCO.QUOTE_RECORD_ID = '{QuoteRecordId}'  AND SAQSCO.QTEREV_RECORD_ID = '{quote_revision_record_id}' AND SAQSCO.RELOCATION_EQUIPMENT_TYPE = 'RECEIVING EQUIPMENT' AND FABLOCATION_ID NOT IN(SELECT FABLOCATION_ID FROM SAQSFB WHERE SERVICE_ID = '{TreeParam}' AND QUOTE_RECORD_ID = '{QuoteRecordId}') {SingleRow}
					) FB""".format(
									TreeParam=Quote.GetGlobal("TreeParentLevel0"),
									QuoteRecordId=Quote.GetGlobal("contract_quote_record_id"),
									UserId=User.Id,
									UserName=User.UserName,
									SingleRow=" AND SAQSCO.CpqTableEntryId = '"+str(cpqid) + "'" if SELECTALL == "no" else "",
									quote_revision_record_id=quote_revision_record_id
								))
			# Sql.RunQuery("""
			# 			INSERT SAQSFE (ENTITLEMENT_XML,QUOTE_ID,QUOTE_NAME,QUOTE_RECORD_ID,QTEREV_RECORD_ID,QTEREV_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,	
			# 			CPS_CONFIGURATION_ID, CPS_MATCH_ID,QTESRVENT_RECORD_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,QTESRVFBL_RECORD_ID,PAR_SERVICE_ID,PAR_SERVICE_DESCRIPTION,PAR_SERVICE_RECORD_ID,QUOTE_SERVICE_FAB_LOC_ENT_RECORD_ID, CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED)
			# 			SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_FAB_LOC_ENT_RECORD_ID, {UserId} as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM (
			# 			SELECT 
			# 				DISTINCT	
			# 				SAQTSE.ENTITLEMENT_XML,SAQTSE.QUOTE_ID,SAQTSE.QUOTE_NAME,SAQTSE.QUOTE_RECORD_ID,SAQTSE.QTEREV_RECORD_ID,SAQTSE.QTEREV_ID,SAQTSE.SERVICE_DESCRIPTION,SAQTSE.SERVICE_ID,SAQTSE.SERVICE_RECORD_ID,SAQTSE.SALESORG_ID,SAQTSE.SALESORG_NAME,SAQTSE.SALESORG_RECORD_ID,SAQTSE.CPS_CONFIGURATION_ID, SAQTSE.CPS_MATCH_ID,SAQTSE.QUOTE_SERVICE_ENTITLEMENT_RECORD_ID as QTESRVENT_RECORD_ID,SAQSFB.FABLOCATION_ID, SAQSFB.FABLOCATION_NAME, SAQSFB.FABLOCATION_RECORD_ID,SAQSFB.QUOTE_SERVICE_FAB_LOCATION_RECORD_ID as QTESRVFBL_RECORD_ID,SAQTSE.PAR_SERVICE_ID,SAQTSE.PAR_SERVICE_DESCRIPTION,SAQTSE.PAR_SERVICE_RECORD_ID
			# 			FROM
			# 			SAQTSE (NOLOCK)
			# 			JOIN SAQSFB ON SAQSFB.SERVICE_RECORD_ID = SAQTSE.SERVICE_RECORD_ID AND SAQSFB.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID AND SAQSFB.QTEREV_RECORD_ID = SAQTSE.QTEREV_RECORD_ID
			# 			WHERE SAQTSE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQTSE.SERVICE_ID = '{ServiceId}'   AND SAQTSE.QTEREV_RECORD_ID = '{quote_revision_record_id}' AND SAQSFB.FABLOCATION_ID NOT IN (SELECT FABLOCATION_ID FROM SAQSFE WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND SERVICE_ID = '{ServiceId}')) IQ""".format(UserId=User.Id, QuoteRecordId=Quote.GetGlobal("contract_quote_record_id"), ServiceId=Quote.GetGlobal("TreeParentLevel0"),quote_revision_record_id=quote_revision_record_id))
			
			# Sql.RunQuery(""" INSERT SAQSGE (KB_VERSION,QUOTE_ID,QUOTE_NAME,QUOTE_RECORD_ID,QTEREV_RECORD_ID,QTEREV_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,	
			# CPS_CONFIGURATION_ID, CPS_MATCH_ID,GREENBOOK,GREENBOOK_RECORD_ID,QTESRVENT_RECORD_ID,QTSFBLENT_RECORD_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,ENTITLEMENT_XML, QUOTE_SERVICE_GREENBOOK_ENTITLEMENT_RECORD_ID, CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED)
			# SELECT OQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_GREENBOOK_ENTITLEMENT_RECORD_ID, {UserId} as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM (SELECT IQ.*,M.ENTITLEMENT_XML FROM(
			# SELECT 
			# 	DISTINCT	
			# 	SAQTSE.KB_VERSION,SAQTSE.QUOTE_ID,SAQTSE.QUOTE_NAME,SAQTSE.QUOTE_RECORD_ID,SAQTSE.QTEREV_RECORD_ID,SAQTSE.QTEREV_ID,SAQTSE.SERVICE_DESCRIPTION,SAQTSE.SERVICE_ID,SAQTSE.SERVICE_RECORD_ID,SAQTSE.SALESORG_ID,SAQTSE.SALESORG_NAME,SAQTSE.SALESORG_RECORD_ID,SAQTSE.CPS_CONFIGURATION_ID, SAQTSE.CPS_MATCH_ID,SAQSCO.GREENBOOK,SAQSCO.GREENBOOK_RECORD_ID,SAQTSE.QUOTE_SERVICE_ENTITLEMENT_RECORD_ID as QTESRVENT_RECORD_ID,SAQSFE.QUOTE_SERVICE_FAB_LOC_ENT_RECORD_ID as QTSFBLENT_RECORD_ID,SAQSFE.FABLOCATION_ID,SAQSFE.FABLOCATION_NAME,SAQSFE.FABLOCATION_RECORD_ID
			# FROM
			# SAQTSE (NOLOCK)
			# JOIN SAQSCO  (NOLOCK) ON SAQSCO.SERVICE_RECORD_ID = SAQTSE.SERVICE_RECORD_ID AND SAQSCO.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID AND SAQSCO.QTEREV_RECORD_ID = SAQTSE.QTEREV_RECORD_ID JOIN SAQSFE ON SAQSFE.SERVICE_RECORD_ID = SAQTSE.SERVICE_RECORD_ID AND SAQSFE.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID  AND SAQSFE.QTEREV_RECORD_ID = SAQTSE.QTEREV_RECORD_ID
			# WHERE SAQTSE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQTSE.QTEREV_RECORD_ID = '{quote_revision_record_id}' AND SAQTSE.SERVICE_ID = '{ServiceId}' AND SAQSCO.RELOCATION_EQUIPMENT_TYPE = 'Receiving Equipment' ) IQ JOIN SAQSFE (NOLOCK) M ON IQ.QTSFBLENT_RECORD_ID = QUOTE_SERVICE_FAB_LOC_ENT_RECORD_ID )OQ""".format(UserId=User.Id, QuoteRecordId=Quote.GetGlobal("contract_quote_record_id"), ServiceId=Quote.GetGlobal("TreeParentLevel0"),quote_revision_record_id=quote_revision_record_id))
			# Sql.RunQuery(""" INSERT SAQSGE (KB_VERSION,QUOTE_ID,QUOTE_NAME,QUOTE_RECORD_ID,QTEREV_RECORD_ID,QTEREV_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,	
			# CPS_CONFIGURATION_ID, CPS_MATCH_ID,GREENBOOK,GREENBOOK_RECORD_ID,QTESRVENT_RECORD_ID,ENTITLEMENT_XML, QUOTE_SERVICE_GREENBOOK_ENTITLEMENT_RECORD_ID, CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED)
			# SELECT OQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_GREENBOOK_ENTITLEMENT_RECORD_ID, {UserId} as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM (SELECT IQ.*,M.ENTITLEMENT_XML FROM(
			# SELECT 
			# 	DISTINCT	
			# 	SAQTSE.KB_VERSION,SAQTSE.QUOTE_ID,SAQTSE.QUOTE_NAME,SAQTSE.QUOTE_RECORD_ID,SAQTSE.QTEREV_RECORD_ID,SAQTSE.QTEREV_ID,SAQTSE.SERVICE_DESCRIPTION,SAQTSE.SERVICE_ID,SAQTSE.SERVICE_RECORD_ID,SAQTSE.SALESORG_ID,SAQTSE.SALESORG_NAME,SAQTSE.SALESORG_RECORD_ID,SAQTSE.CPS_CONFIGURATION_ID, SAQTSE.CPS_MATCH_ID,SAQSCO.GREENBOOK,SAQSCO.GREENBOOK_RECORD_ID,SAQTSE.QUOTE_SERVICE_ENTITLEMENT_RECORD_ID as QTESRVENT_RECORD_ID
			# FROM
			# SAQTSE (NOLOCK)
			# JOIN SAQSCO  (NOLOCK) ON SAQSCO.SERVICE_RECORD_ID = SAQTSE.SERVICE_RECORD_ID AND SAQSCO.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID AND SAQSCO.QTEREV_RECORD_ID = SAQTSE.QTEREV_RECORD_ID 
			# WHERE SAQTSE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQTSE.QTEREV_RECORD_ID = '{quote_revision_record_id}' AND SAQTSE.SERVICE_ID = '{ServiceId}' AND SAQSCO.RELOCATION_EQUIPMENT_TYPE = 'Receiving Equipment' ) IQ )OQ""".format(UserId=User.Id, QuoteRecordId=Quote.GetGlobal("contract_quote_record_id"), ServiceId=Quote.GetGlobal("TreeParentLevel0"),quote_revision_record_id=quote_revision_record_id))

			Sql.RunQuery("""INSERT SAQSGE (KB_VERSION,QUOTE_ID,QUOTE_NAME,QUOTE_RECORD_ID,QTEREV_RECORD_ID,QTEREV_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,	
			CPS_CONFIGURATION_ID, CPS_MATCH_ID,GREENBOOK,GREENBOOK_RECORD_ID,QTESRVENT_RECORD_ID,ENTITLEMENT_XML,CONFIGURATION_STATUS, QUOTE_SERVICE_GREENBOOK_ENTITLEMENT_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED )
			SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_GREENBOOK_ENTITLEMENT_RECORD_ID, {UserId} as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM (SELECT DISTINCT SAQTSE.KB_VERSION,SAQTSE.QUOTE_ID,SAQTSE.QUOTE_NAME,SAQTSE.QUOTE_RECORD_ID,SAQTSE.QTEREV_RECORD_ID,SAQTSE.QTEREV_ID,SAQTSE.SERVICE_DESCRIPTION,SAQTSE.SERVICE_ID,SAQTSE.SERVICE_RECORD_ID,SAQTSE.SALESORG_ID,SAQTSE.SALESORG_NAME,SAQTSE.SALESORG_RECORD_ID,	
			SAQTSE.CPS_CONFIGURATION_ID, SAQTSE.CPS_MATCH_ID,SAQSCO.GREENBOOK,SAQSCO.GREENBOOK_RECORD_ID,SAQTSE.QUOTE_SERVICE_ENTITLEMENT_RECORD_ID as QTESRVENT_RECORD_ID,SAQTSE.ENTITLEMENT_XML,SAQTSE.CONFIGURATION_STATUS FROM
			SAQTSE (NOLOCK) JOIN SAQSCO  (NOLOCK) ON SAQSCO.SERVICE_RECORD_ID = SAQTSE.SERVICE_RECORD_ID AND SAQSCO.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID  AND SAQSCO.QTEREV_RECORD_ID = SAQTSE.QTEREV_RECORD_ID  
			WHERE SAQTSE.QUOTE_RECORD_ID ='{QuoteRecordId}'  AND SAQTSE.QTEREV_RECORD_ID = '{revision_rec_id}' AND SAQTSE.SERVICE_ID = '{ServiceId}')IQ""".format(UserId=User.Id, QuoteRecordId=Quote.GetGlobal("contract_quote_record_id"), ServiceId=Quote.GetGlobal("TreeParentLevel0"), revision_rec_id = quote_revision_record_id) )

			Trace.Write("SAQSGB INSERT FROM SYBLKETRLG")
			Log.Info("SYBLKETRLG - SAQSGB")
			Sql.RunQuery(
				"""
					INSERT SAQSGB (
						QUOTE_SERVICE_GREENBOOK_RECORD_ID,
						GREENBOOK,
						GREENBOOK_RECORD_ID,
						QUOTE_ID,
						QUOTE_NAME,
						QUOTE_RECORD_ID,
						QTEREV_RECORD_ID,
						QTEREV_ID,
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
							SAQSCO.GREENBOOK,
							SAQSCO.GREENBOOK_RECORD_ID,
							SAQSCO.QUOTE_ID,
							SAQSCO.QUOTE_NAME,
							SAQSCO.QUOTE_RECORD_ID,
							SAQSCO.QTEREV_RECORD_ID,
							SAQSCO.QTEREV_ID,
							SAQSCO.SALESORG_ID,
							SAQSCO.SALESORG_NAME,
							SAQSCO.SALESORG_RECORD_ID,
							SAQSCO.SERVICE_DESCRIPTION,
							SAQSCO.SERVICE_ID,
							SAQSCO.SERVICE_RECORD_ID,
							SAQSCO.EQUIPMENT_QUANTITY,								
							SAQTMT.CONTRACT_VALID_FROM,
							SAQTMT.CONTRACT_VALID_TO,
							SAQTSV.PAR_SERVICE_DESCRIPTION,
							SAQTSV.PAR_SERVICE_ID,
							SAQTSV.PAR_SERVICE_RECORD_ID,
							'{UserName}' AS CPQTABLEENTRYADDEDBY,
							GETDATE() as CPQTABLEENTRYDATEADDED,
							{UserId} as CpqTableEntryModifiedBy,
							GETDATE() as CpqTableEntryDateModified
							FROM SAQSCO (NOLOCK) JOIN SAQTSV (NOLOCK) ON
							SAQSCO.QUOTE_ID = SAQTSV.QUOTE_ID AND
							SAQTSV.SERVICE_ID = '{TreeParam}' AND
							SAQTSV.SERVICE_TYPE = '{TreeParentParam}'
							JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID
							WHERE 
							SAQSCO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCO.QTEREV_RECORD_ID = '{quote_revision_record_id}' AND SAQSCO.RELOCATION_EQUIPMENT_TYPE = 'Receiving Equipment' {SingleRow})A""".format(
							TreeParam=Quote.GetGlobal("TreeParentLevel0"),
							TreeParentParam=Quote.GetGlobal("TreeParentLevel1"),
							QuoteRecordId=Quote.GetGlobal("contract_quote_record_id"),
							UserName=User.UserName,
							UserId=User.Id,
							SingleRow=" AND SAQSCO.CpqTableEntryId = '"+str(cpqid) + "'" if SELECTALL == "no" else "",
							quote_revision_record_id=quote_revision_record_id
						)
			)
			# ###SAQSCE and SAQSAE insert for assembly and entitlement 
			qtqsce_query="""
				INSERT SAQSCE
				(KB_VERSION,ENTITLEMENT_XML,EQUIPMENT_ID,EQUIPMENT_RECORD_ID,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_RECORD_ID,QTEREV_ID,QTESRVCOB_RECORD_ID,QTESRVENT_RECORD_ID,SERIAL_NO,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,CPS_CONFIGURATION_ID,CPS_MATCH_ID,GREENBOOK,GREENBOOK_RECORD_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,QUOTE_SERVICE_COVERED_OBJ_ENTITLEMENTS_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED) 
				SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_COVERED_OBJ_ENTITLEMENTS_RECORD_ID, {UserId} as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM (
				SELECT 
				DISTINCT
				SAQTSE.KB_VERSION,SAQTSE.ENTITLEMENT_XML,SAQSCO.EQUIPMENT_ID,SAQSCO.EQUIPMENT_RECORD_ID,SAQTSE.QUOTE_ID,SAQTSE.QUOTE_RECORD_ID,SAQTSE.QTEREV_RECORD_ID,SAQTSE.QTEREV_ID,SAQSCO.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID as QTESRVCOB_RECORD_ID,SAQTSE.QUOTE_SERVICE_ENTITLEMENT_RECORD_ID as QTESRVENT_RECORD_ID,SAQSCO.SERIAL_NO,SAQTSE.SERVICE_DESCRIPTION,SAQTSE.SERVICE_ID,SAQTSE.SERVICE_RECORD_ID,SAQTSE.CPS_CONFIGURATION_ID,SAQTSE.CPS_MATCH_ID,SAQSCO.GREENBOOK,SAQSCO.GREENBOOK_RECORD_ID,SAQSCO.FABLOCATION_ID,SAQSCO.FABLOCATION_NAME,SAQSCO.FABLOCATION_RECORD_ID,SAQTSE.SALESORG_ID,SAQTSE.SALESORG_NAME,SAQTSE.SALESORG_RECORD_ID
				FROM	
				SAQTSE (NOLOCK)
				JOIN SAQSCO (NOLOCK) ON SAQSCO.SERVICE_RECORD_ID = SAQTSE.SERVICE_RECORD_ID AND SAQSCO.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID AND SAQSCO.QTEREV_RECORD_ID = SAQTSE.QTEREV_RECORD_ID 
				WHERE SAQTSE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQTSE.QTEREV_RECORD_ID = '{quote_revision_record_id}' AND SAQTSE.SERVICE_ID = '{ServiceId}' AND SAQSCO.EQUIPMENT_ID NOT IN (SELECT EQUIPMENT_ID FROM SAQSCE WHERE QUOTE_RECORD_ID  = '{QuoteRecordId}' AND SERVICE_ID = '{ServiceId}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}')) IQ""".format(
				UserId=User.Id, 
				QuoteRecordId=Qt_rec_id, 
				ServiceId=Quote.GetGlobal("TreeParentLevel0"),
				quote_revision_record_id=quote_revision_record_id )
				#Trace.Write('qtqsce_query-renewal----179=---Qt_rec_id--'+str(qtqsce_query))
			Sql.RunQuery(qtqsce_query)
			SAQSAE_insert = """INSERT SAQSAE (KB_VERSION,EQUIPMENT_ID,EQUIPMENT_RECORD_ID,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_RECORD_ID,QTEREV_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,CPS_CONFIGURATION_ID,CPS_MATCH_ID,GREENBOOK,GREENBOOK_RECORD_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,ASSEMBLY_DESCRIPTION,ASSEMBLY_ID,ASSEMBLY_RECORD_ID,QTESRVCOA_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,ENTITLEMENT_XML,QTESRVCOE_RECORD_ID,QUOTE_SERVICE_COV_OBJ_ASS_ENT_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED) SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_COV_OBJ_ASS_ENT_RECORD_ID, {UserId} as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM(SELECT IQ.*,M.ENTITLEMENT_XML,M.QUOTE_SERVICE_COVERED_OBJ_ENTITLEMENTS_RECORD_ID as QTESRVCOE_RECORD_ID FROM ( SELECT DISTINCT SAQTSE.KB_VERSION,SAQSCA.EQUIPMENT_ID,SAQSCA.EQUIPMENT_RECORD_ID,SAQTSE.QUOTE_ID,SAQTSE.QUOTE_RECORD_ID,SAQTSE.QTEREV_RECORD_ID,SAQTSE.QTEREV_ID,SAQTSE.SERVICE_DESCRIPTION,SAQTSE.SERVICE_ID,SAQTSE.SERVICE_RECORD_ID,SAQTSE.CPS_CONFIGURATION_ID,SAQTSE.CPS_MATCH_ID,SAQSCA.GREENBOOK,SAQSCA.GREENBOOK_RECORD_ID,SAQSCA.FABLOCATION_ID,SAQSCA.FABLOCATION_NAME,SAQSCA.FABLOCATION_RECORD_ID,SAQSCA.ASSEMBLY_DESCRIPTION,SAQSCA.ASSEMBLY_ID,SAQSCA.ASSEMBLY_RECORD_ID,SAQSCA.QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID as QTESRVCOA_RECORD_ID,SAQTSE.SALESORG_ID,SAQTSE.SALESORG_NAME,SAQTSE.SALESORG_RECORD_ID FROM SAQTSE (NOLOCK) JOIN (SELECT * FROM SAQSCA (NOLOCK) WHERE SAQSCA.QUOTE_RECORD_ID = '{ContractId}' ) SAQSCA ON SAQTSE.QUOTE_RECORD_ID = SAQSCA.QUOTE_RECORD_ID AND SAQTSE.QTEREV_RECORD_ID = SAQSCA.QTEREV_RECORD_ID AND SAQTSE.SERVICE_RECORD_ID = SAQSCA.SERVICE_RECORD_ID WHERE SAQTSE.QUOTE_RECORD_ID = '{ContractId}' AND SAQTSE.SERVICE_ID = '{serviceId}' AND SAQTSE.QTEREV_RECORD_ID = '{quote_revision_record_id}') IQ JOIN SAQSCE (NOLOCK) M ON M.SERVICE_RECORD_ID = IQ.SERVICE_RECORD_ID AND M.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND M.EQUIPMENT_ID = IQ.EQUIPMENT_ID )IQ""".format(
				UserId=User.Id, 
				ContractId=Qt_rec_id, 
				serviceId=Quote.GetGlobal("TreeParentLevel0"),
				quote_revision_record_id=quote_revision_record_id )
			Sql.RunQuery(SAQSAE_insert)
			#Trace.Write('SAQSAE_insert--'+str(SAQSAE_insert))

			##A055S000P01-6826 --update SAQSCE and SAQSAE table as quote type 'chmaber based' starts....
			ServiceId=Quote.GetGlobal("TreeParentLevel0")
			ContractId = Quote.GetGlobal("contract_quote_record_id")
			Trace.Write('cpqid---'+str(cpqid)+'--'+str(SELECTALL)+'---'+str(recordslist)+str(ServiceId))
			get_chamber_equp = Sql.GetList("SELECT EQUIPMENT_ID,INCLUDED FROM SAQSCO WHERE QUOTE_RECORD_ID = '{Quote}' AND SERVICE_ID= '{ServiceId}' AND EQUIPMENT_ID IN {recordslist} AND INCLUDED= 'CHAMBER' AND QTEREV_RECORD_ID = '{quote_revision_record_id}'".format(Quote = ContractId,ServiceId = ServiceId,recordslist = recordslist,quote_revision_record_id=quote_revision_record_id)  )
			if get_chamber_equp:
				recordslst = str(tuple([cham.EQUIPMENT_ID for cham in get_chamber_equp])).replace(",)",')')

				if recordslst and 'Z0007' in ServiceId:
					whereReq = " QUOTE_RECORD_ID = '{}' and SERVICE_ID = '{}' AND EQUIPMENT_ID IN {} AND QTEREV_RECORD_ID = '{}'".format(ContractId,ServiceId,recordslst,quote_revision_record_id)
					add_where = " and INCLUDED = 'CHAMBER'"
					AttributeID = 'AGS_QUO_QUO_TYP'
					NewValue = 'Chamber based'
					table_name = 'SAQSCE'
					ent_params_list = str(whereReq)+"||"+str(add_where)+"||"+str(AttributeID)+"||"+str(NewValue)+"||"+str(ServiceId)+'||'+str(table_name)
					result = ScriptExecutor.ExecuteGlobal("CQASSMEDIT", {"ACTION": 'UPDATE_ENTITLEMENT', 'ent_params_list':ent_params_list})
					if result:
						Trace.Write('rolldown-'+str(result))
						whereReq = " SRC.QUOTE_RECORD_ID = '{}' and SRC.SERVICE_ID = '{}' AND SRC.EQUIPMENT_ID IN {}  AND SRC.QTEREV_RECORD_ID = '{}'".format(ContractId,ServiceId,recordslst,quote_revision_record_id)
						result1 = ScriptExecutor.ExecuteGlobal("CQASSMEDIT", {"ACTION": 'ENT_ROLLDOWN', 'ent_params_list':whereReq})

			##A055S000P01-6826 --update SAQSCE and SAQSAE table as quote type 'chmaber based' ends....

		
		
		if obj_name == 'SAQSTE':
			master_fab_object = Sql.GetFirst("Select FAB_LOCATION_NAME,FAB_LOCATION_RECORD_ID from MAFBLC where FAB_LOCATION_ID = '{fab_id}'".format(fab_id = str(VALUE)))
			fab_name = master_fab_object.FAB_LOCATION_NAME
			fab_location_record_id = master_fab_object.FAB_LOCATION_RECORD_ID
			Tool_relocation_object = """UPDATE SAQSTE SET FABLOCATION_NAME = '{fab_name}', FABLOCATION_RECORD_ID = '{fab_location_record_id}' WHERE FABLOCATION_ID = '{fab_id}' and QUOTE_RECORD_ID = '{quote_record_id}'  AND QTEREV_RECORD_ID = '{quote_revision_record_id}'""".format(fab_name = fab_name,fab_location_record_id = fab_location_record_id,fab_id = str(VALUE),quote_record_id = str(ContractRecordId,quote_revision_record_id=quote_revision_record_id))
			Sql.RunQuery(Tool_relocation_object)
			##Updating the fabname and fablocation id in bulk edit scenario ends.... 
			
			GETSAQFBL = Sql.GetFirst("SELECT QUOTE_FABLOCATION_RECORD_ID FROM SAQFBL(NOLOCK) WHERE QUOTE_RECORD_ID = '"+str(ContractRecordId)+"'and FABLOCATION_ID ='"+str(VALUE)+"'  AND QTEREV_RECORD_ID = '" + str(quote_revision_record_id) + "'")
			if GETSAQFBL is None:
				Sql.RunQuery(""" INSERT SAQFBL (FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, QUOTE_ID, QUOTE_RECORD_ID,QTEREV_RECORD_ID, QTEREV_ID, COUNTRY, COUNTRY_RECORD_ID, MNT_PLANT_ID, MNT_PLANT_NAME, MNT_PLANT_RECORD_ID, SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID, FABLOCATION_STATUS, ADDRESS_1, ADDRESS_2, CITY, STATE, STATE_RECORD_ID,QUOTE_FABLOCATION_RECORD_ID,CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified) SELECT A.*,CONVERT(VARCHAR(4000),NEWID()) as QUOTE_FABLOCATION_RECORD_ID,'{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED,'{UserId}' as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (SELECT DISTINCT MAFBLC.FAB_LOCATION_ID,MAFBLC.FAB_LOCATION_NAME,MAFBLC.FAB_LOCATION_RECORD_ID,SAQSTE.QUOTE_ID,SAQSTE.QUOTE_RECORD_ID,SAQSTE.QTEREV_RECORD_ID,SAQSTE.QTEREV_ID,MAFBLC.COUNTRY,MAFBLC.COUNTRY_RECORD_ID,MAFBLC.MNT_PLANT_ID,MAFBLC.MNT_PLANT_NAME,MAFBLC.MNT_PLANT_RECORD_ID,MAFBLC.SALESORG_ID,MAFBLC.SALESORG_NAME,MAFBLC.SALESORG_RECORD_ID,MAFBLC.STATUS AS FABLOCATION_STATUS,MAFBLC.ADDRESS_1,MAFBLC.ADDRESS_2,MAFBLC.CITY,MAFBLC.STATE,MAFBLC.STATE_RECORD_ID FROM MAFBLC INNER JOIN  SAQSTE on MAFBLC.FAB_LOCATION_ID = SAQSTE.FABLOCATION_ID WHERE QUOTE_RECORD_ID = '{QuoteRecId}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND SAQSTE.FABLOCATION_ID ='{fabid}')A WHERE A.FAB_LOCATION_ID NOT IN (SELECT FABLOCATION_ID FROM SAQFBL WHERE QUOTE_RECORD_ID = '{QuoteRecId}'  AND QTEREV_RECORD_ID = '{quote_revision_record_id}') """.format(UserName=User.UserName,UserId=User.Id,QuoteRecId=ContractRecordId,fabid=VALUE,quote_revision_record_id=quote_revision_record_id))
			

			###update SAQFEQ starts
			GETSAQFEQ = Sql.GetFirst("""SELECT SAQFBL.QUOTE_FABLOCATION_RECORD_ID from SAQFEQ (NOLOCK) INNER JOIN SAQSTE (NOLOCK) ON SAQFEQ.EQUIPMENT_ID = SAQSTE.EQUIPMENT_ID AND SAQFEQ.QUOTE_RECORD_ID = SAQSTE.QUOTE_RECORD_ID AND SAQFEQ.QTEREV_RECORD_ID = SAQSTE.QTEREV_RECORD_ID INNER JOIN SAQFBL (NOLOCK) on SAQFBL.FABLOCATION_ID = SAQSTE.FABLOCATION_ID AND  SAQFBL.QUOTE_RECORD_ID = SAQSTE.QUOTE_RECORD_ID AND SAQFBL.QTEREV_RECORD_ID = SAQSTE.QTEREV_RECORD_ID where SAQFEQ.QUOTE_RECORD_ID = '{quote_record_id}' AND SAQSTE.QTEREV_RECORD_ID = '{quote_revision_record_id}' AND SAQSTE.CpqTableEntryId in {SAQSTE_cpqid}""".format(quote_record_id = str(ContractRecordId),SAQSTE_cpqid = str(tuple(selected_rows_cpqid)).replace(',)',')'),quote_revision_record_id=quote_revision_record_id))
			if GETSAQFEQ is not None:
				
				Sql.RunQuery("""UPDATE SAQFEQ SET FABLOCATION_ID = '{fab_id}',FABLOCATION_NAME = '{fab_name}', FABLOCATION_RECORD_ID = '{fab_location_record_id}', QTEFBL_RECORD_ID = '{quote_fab_rec_id}' FROM SAQFEQ WHERE QUOTE_RECORD_ID = '{quote_record_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND EQUIPMENT_RECORD_ID IN (SELECT SAQFEQ.EQUIPMENT_RECORD_ID from SAQFEQ (NOLOCK) INNER JOIN SAQSTE (NOLOCK) ON SAQFEQ.EQUIPMENT_ID = SAQSTE.EQUIPMENT_ID AND SAQFEQ.QUOTE_RECORD_ID = SAQSTE.QUOTE_RECORD_ID where SAQFEQ.QUOTE_RECORD_ID = '{quote_record_id}' AND SAQFEQ.QTEREV_RECORD_ID = '{quote_revision_record_id}' AND SAQSTE.CpqTableEntryId in {SAQSTE_cpqid} )""".format(fab_id = str(VALUE),fab_name = fab_name,fab_location_record_id = fab_location_record_id,quote_record_id = str(ContractRecordId),SAQSTE_cpqid = str(tuple(selected_rows_cpqid)).replace(',)',')') ,quote_fab_rec_id = GETSAQFEQ.QUOTE_FABLOCATION_RECORD_ID,quote_revision_record_id=quote_revision_record_id ))
			###update SAQFEQ ends
			else:

				Sql.RunQuery(""" INSERT SAQFEQ ( QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID, EQUIPMENT_ID, EQUIPMENT_RECORD_ID, EQUIPMENT_DESCRIPTION, FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, SERIAL_NUMBER, QUOTE_RECORD_ID, QUOTE_ID, QUOTE_NAME, PLATFORM, EQUIPMENTCATEGORY_RECORD_ID, EQUIPMENTCATEGORY_ID, EQUIPMENTCATEGORY_DESCRIPTION, EQUIPMENT_STATUS, PBG, GREENBOOK, GREENBOOK_RECORD_ID, MNT_PLANT_RECORD_ID, MNT_PLANT_ID, MNT_PLANT_NAME, WARRANTY_START_DATE, WARRANTY_END_DATE, SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID, CUSTOMER_TOOL_ID,QTEFBL_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified )SELECT A.* FROM( SELECT CONVERT(VARCHAR(4000),NEWID()) as QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID, SAQSTE.EQUIPMENT_ID, SAQSTE.EQUIPMENT_RECORD_ID, SAQSTE.EQUIPMENT_DESCRIPTION, SAQSTE.FABLOCATION_ID, SAQSTE.FABLOCATION_NAME, SAQSTE.FABLOCATION_RECORD_ID, MAEQUP.SERIAL_NO, SAQSTE.QUOTE_RECORD_ID, SAQSTE.QUOTE_ID, SAQSTE.QUOTE_NAME, MAEQUP.PLATFORM, SAQSTE.EQUIPMENTCATEGORY_RECORD_ID, SAQSTE.EQUIPMENTCATEGORY_ID, SAQSTE.EQUIPMENTCATEGORY_DESCRIPTION, SAQSTE.EQUIPMENT_STATUS, MAEQUP.PBG, SAQSTE.GREENBOOK, SAQSTE.GREENBOOK_RECORD_ID, SAQSTE.MNT_PLANT_RECORD_ID, SAQSTE.MNT_PLANT_ID, SAQSTE.MNT_PLANT_NAME, MAEQUP.WARRANTY_START_DATE, MAEQUP.WARRANTY_END_DATE, MAEQUP.SALESORG_ID, MAEQUP.SALESORG_NAME, MAEQUP.SALESORG_RECORD_ID, MAEQUP.CUSTOMER_TOOL_ID,SAQFBL.QUOTE_FABLOCATION_RECORD_ID as QTEFBL_RECORD_ID,'{UserName}' AS CPQTABLEENTRYADDEDBY,GETDATE() as CPQTABLEENTRYDATEADDED,'{UserId}' as CpqTableEntryModifiedBy,GETDATE() as CpqTableEntryDateModified FROM MAEQUP (NOLOCK)INNER JOIN  SAQSTE on MAEQUP.EQUIPMENT_ID = SAQSTE.EQUIPMENT_ID INNER JOIN SAQFBL on SAQFBL.FABLOCATION_ID = SAQSTE.FABLOCATION_ID AND  SAQFBL.QUOTE_RECORD_ID = SAQSTE.QUOTE_RECORD_ID WHERE SAQSTE.QUOTE_RECORD_ID = '{QuoteRecId}' AND SAQSTE.QTEREV_RECORD_ID = '{quote_revision_record_id}' AND SAQSTE.FABLOCATION_ID ='{fabid}') A LEFT JOIN SAQFEQ M(NOLOCK) ON A.QUOTE_ID = M.QUOTE_ID AND A.EQUIPMENT_ID = M.EQUIPMENT_ID WHERE M.EQUIPMENT_ID IS NULL""".format(UserName=User.UserName,UserId=User.Id,QuoteRecId=ContractRecordId,fabid=VALUE,quote_revision_record_id=quote_revision_record_id))
			
			###update SAQFEA starts
			GETSAQFEA = Sql.GetFirst("""SELECT count(SAQFEA.EQUIPMENT_RECORD_ID) as cnt from SAQFEA (NOLOCK) INNER JOIN SAQSTE (NOLOCK) ON SAQFEA.EQUIPMENT_ID = SAQSTE.EQUIPMENT_ID AND SAQFEA.QUOTE_RECORD_ID = SAQSTE.QUOTE_RECORD_ID where SAQFEA.QUOTE_RECORD_ID = '{quote_record_id}' AND SAQFEA.QTEREV_RECORD_ID = '{quote_revision_record_id}' AND SAQSTE.CpqTableEntryId in {SAQSTE_cpqid}""".format(quote_record_id = str(ContractRecordId),SAQSTE_cpqid = str(tuple(selected_rows_cpqid)).replace(',)',')'),quote_revision_record_id=quote_revision_record_id)) 
			if GETSAQFEA.cnt:
				Sql.RunQuery("""UPDATE SAQFEA SET FABLOCATION_ID = '{fab_id}',FABLOCATION_NAME = '{fab_name}', FABLOCATION_RECORD_ID = '{fab_location_record_id}' FROM SAQFEA WHERE QUOTE_RECORD_ID = '{quote_record_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND EQUIPMENT_RECORD_ID IN (SELECT SAQFEA.EQUIPMENT_RECORD_ID from SAQFEA (NOLOCK) INNER JOIN SAQSTE (NOLOCK) ON SAQFEA.EQUIPMENT_ID = SAQSTE.EQUIPMENT_ID AND SAQFEA.QUOTE_RECORD_ID = SAQSTE.QUOTE_RECORD_ID where SAQFEA.QUOTE_RECORD_ID = '{quote_record_id}' AND SAQSTE.QTEREV_RECORD_ID = '{quote_revision_record_id}' AND SAQSTE.CpqTableEntryId in {SAQSTE_cpqid} )""".format(fab_id = str(VALUE),fab_name = fab_name,fab_location_record_id = fab_location_record_id,quote_record_id = str(ContractRecordId),SAQSTE_cpqid = str(tuple(selected_rows_cpqid)).replace(',)',')'),quote_revision_record_id=quote_revision_record_id ))
			###update SAQFEA ends
			else:
				Sql.RunQuery("""INSERT SAQFEA (QUOTE_FAB_LOC_COV_OBJ_ASSEMBLY_RECORD_ID, EQUIPMENT_ID, EQUIPMENT_RECORD_ID, EQUIPMENT_DESCRIPTION, ASSEMBLY_ID, ASSEMBLY_STATUS, ASSEMBLY_DESCRIPTION, ASSEMBLY_RECORD_ID, FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, SERIAL_NUMBER, QUOTE_RECORD_ID,QTEREV_RECORD_ID,QTEREV_ID, QUOTE_ID, QUOTE_NAME, EQUIPMENTCATEGORY_RECORD_ID, EQUIPMENTCATEGORY_ID, EQUIPMENTCATEGORY_DESCRIPTION, EQUIPMENTTYPE_DESCRIPTION, EQUIPMENTTYPE_RECORD_ID, GOT_CODE, MNT_PLANT_RECORD_ID, MNT_PLANT_ID, WARRANTY_START_DATE, WARRANTY_END_DATE, SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified ) SELECT A.* FROM (SELECT CONVERT(VARCHAR(4000),NEWID()) as QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID, MAEQUP.PAR_EQUIPMENT_ID, MAEQUP.PAR_EQUIPMENT_RECORD_ID, MAEQUP.PAR_EQUIPMENT_DESCRIPTION, SAQSTE.EQUIPMENT_ID, SAQSTE.EQUIPMENT_STATUS, SAQSTE.EQUIPMENT_DESCRIPTION, SAQSTE.EQUIPMENT_RECORD_ID, SAQSTE.FABLOCATION_ID, SAQSTE.FABLOCATION_NAME, SAQSTE.FABLOCATION_RECORD_ID, MAEQUP.SERIAL_NO,SAQSTE.QUOTE_RECORD_ID,SAQSTE.QTEREV_RECORD_ID,SAQSTE.QTEREV_ID, SAQSTE.QUOTE_ID,SAQSTE.QUOTE_NAME, SAQSTE.EQUIPMENTCATEGORY_RECORD_ID, SAQSTE.EQUIPMENTCATEGORY_ID, SAQSTE.EQUIPMENTCATEGORY_DESCRIPTION, '' as EQUIPMENTTYPE_DESCRIPTION, MAEQUP.EQUIPMENTTYPE_RECORD_ID, MAEQUP.GOT_CODE, SAQSTE.MNT_PLANT_RECORD_ID, SAQSTE.MNT_PLANT_ID, MAEQUP.WARRANTY_START_DATE, MAEQUP.WARRANTY_END_DATE, MAEQUP.SALESORG_ID, MAEQUP.SALESORG_NAME, MAEQUP.SALESORG_RECORD_ID,'{UserName}' AS CPQTABLEENTRYADDEDBY,GETDATE() as CPQTABLEENTRYDATEADDED,'{UserId}' as CpqTableEntryModifiedBy,GETDATE() as CpqTableEntryDateModified  FROM MAEQUP (NOLOCK)INNER JOIN  SAQSTE on MAEQUP.PAR_EQUIPMENT_ID = SAQSTE.EQUIPMENT_ID  WHERE QUOTE_RECORD_ID = '{QuoteRecId}' AND SAQSTE.QTEREV_RECORD_ID = '{quote_revision_record_id}' AND SAQSTE.FABLOCATION_ID ='{fabid}' ) A LEFT JOIN SAQFEA M(NOLOCK) ON A.QUOTE_ID = M.QUOTE_ID AND A.EQUIPMENT_ID = M.ASSEMBLY_ID WHERE M.ASSEMBLY_ID IS NULL""".format(UserName=User.UserName,UserId=User.Id,QuoteRecId=ContractRecordId,fabid=VALUE,quote_revision_record_id=quote_revision_record_id))


	return ""



TITLE = Param.TITLE
ELEMENT = Param.ELEMENT
CLICKEDID = Param.CLICKEDID
RECORDID = Param.RECORDID
try:
	VALUE = Param.VALUE
except:
	VALUE= None
try:
	VALUE1 = Param.VALUE1
except:
	VALUE1= None
try:
	quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
except:
	quote_revision_record_id = ""
if hasattr(Param, "selectPN"):

	selectPN = list(Param.selectPN)
else:
	selectPN = ""
try:
	SELECTALL = Param.SELECTALL
	Trace.Write("SELECTALL = "+str(SELECTALL))
except:
	SELECTALL = None
try:
	ALLVALUES = Param.ALLVALUES
	Trace.Write("allvalues--"+str(list(ALLVALUES)))
except:
	ALLVALUES = None
try:
	ALLVALUES1 = Param.ALLVALUES1
	Trace.Write("allvalues1--"+str(list(ALLVALUES1)))
except:
	ALLVALUES1 = None
try:
	ALLVALUES2 = Param.ALLVALUES2
	Trace.Write("allvalues2--"+str(list(ALLVALUES2)))
except:
	ALLVALUES2 = None
try:
	A_Keys = Param.A_Keys
except:
	A_Keys = ""
try:
	A_Values = Param.A_Values
except:
	A_Values = ""
Trace.Write("VALUE--------------------------->" + str(VALUE))

# Trace.Write("selectPN--------------------------->" + str(selectPN))
# Trace.Write("TITLE-----------xxx---- " + str(TITLE))
# Trace.Write("VALUE----------xx---------" + str(VALUE))
# Trace.Write("ELEMENT---------" + str(ELEMENT))
# Trace.Write("CLICKEDID-----679--------- " + str(CLICKEDID))
#Trace.Write("RECORDID--------xxx-----" + str(RECORDID))
if ELEMENT == "RELATEDEDIT":
	
	ApiResponse = ApiResponseFactory.JsonResponse(RELATEDMULTISELECTONEDIT(TITLE, VALUE, CLICKEDID, RECORDID,SELECTALL))
elif ELEMENT == "SAVE":
	ApiResponse = ApiResponseFactory.JsonResponse(RELATEDMULTISELECTONSAVE(TITLE, VALUE, CLICKEDID, RECORDID,selectPN,ALLVALUES,ALLVALUES1,ALLVALUES2,SELECTALL))
else:
	ApiResponse = ApiResponseFactory.JsonResponse("")


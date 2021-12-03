# =========================================================================================================================================
#   __script_name : CQRPLACTCT.PY
#   __script_description : THIS SCRIPT IS USED TO REPLACE ACCOUNT AND CONTACT WHEN USER CLICKS ON REPLACE BUTTON ON A RELATED LIST RECORD.
#   __primary_author__ : WASIM ABDUL
#   __create_date : 19/10/2021
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct
from SYDATABASE import SQL
import datetime
from datetime import datetime
Sql = SQL()
import SYCNGEGUID as CPQID


Sql = SQL()
ScriptExecutor = ScriptExecutor
contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
#def replace_contact(repalce_values,cont_rec_id,table_name):
    #Trace.Write("repalce_values===="+str(repalce_values))
    #Trace.Write("cont_rec_id===="+str(cont_rec_id))
    #Trace.Write("table_name===="+str(table_name)) 
    #con_data_chk = Sql.GetFirst("Select * from SAQICT(NOLOCK) WHERE QUOTE_RECORD_ID ='{}' AND QTEREV_RECORD_ID = '{}' AND QUOTE_REV_INVOLVED_PARTY_CONTACT_ID ='{}'".format(contract_quote_record_id,quote_revision_record_id,cont_rec_id))
    #rpl_con_data_chk =Sql.GetFirst("Select * FROM SACONT(NOLOCK) WHERE CONTACT_RECORD_ID = '{}'".format(repalce_values))
    #if con_data_chk:
     #   delete_saqict = ("DELETE SAQICT WHERE QUOTE_REV_INVOLVED_PARTY_CONTACT_ID ='{}'".format(cont_rec_id))
      #  Sql.RunQuery(delete_saqict)
       # tableInfo = Sql.GetTable("SAQICT")
        #row = {}	
        #row['CITY'] = rpl_con_data_chk.CITY
        #row['CONTACT_ID'] = rpl_con_data_chk.CONTACT_ID
        #row['CONTACT_NAME'] = rpl_con_data_chk.CONTACT_NAME
        #row['CONTACT_RECORD_ID'] = rpl_con_data_chk.CONTACT_RECORD_ID
        #row['COUNTRY'] = rpl_con_data_chk.COUNTRY
        #row['COUNTRY_RECORD_ID'] = rpl_con_data_chk.COUNTRY_RECORD_ID
        #row['EMAIL'] = rpl_con_data_chk.EMAIL
        #row['PHONE'] = rpl_con_data_chk.PHONE
        #row['POSTAL_CODE'] = rpl_con_data_chk.POSTAL_CODE
        #row['QUOTE_RECORD_ID'] = contract_quote_record_id
        #row['QTEREV_RECORD_ID'] = quote_revision_record_id
        #row['QUOTE_REV_INVOLVED_PARTY_CONTACT_ID'] = cont_rec_id
        #tableInfo.AddRow(row)
        #SqlHelper.Upsert(tableInfo)
        #update_saqict="UPDATE SAQICT SET CITY = '{city}',CONTACT_ID = '{contact_id}',CONTACT_NAME = '{contact_name}',CONTACT_RECORD_ID = '{contact_rec_id}',COUNTRY ='{country}',COUNTRY_RECORD_ID ='{country_rec_id}',EMAIL = '{email}',PHONE ='{phone}',POSTAL_CODE ='{postalcode}' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' and QUOTE_REV_INVOLVED_PARTY_CONTACT_ID ='{cont_rec_id}'".format(city = rpl_con_data_chk.CITY,contact_id = rpl_con_data_chk.CONTACT_ID,contact_name = rpl_con_data_chk.CONTACT_NAME,contact_rec_id = rpl_con_data_chk.CONTACT_RECORD_ID,country =rpl_con_data_chk.COUNTRY,country_rec_id =rpl_con_data_chk.COUNTRY_RECORD_ID,email=rpl_con_data_chk.EMAIL,phone= rpl_con_data_chk.PHONE,postalcode =rpl_con_data_chk.POSTAL_CODE,QuoteRecordId = contract_quote_record_id,RevisionRecordId = quote_revision_record_id,cont_rec_id = cont_rec_id)
        #update_saqict = update_saqict.encode('ascii', 'ignore').decode('ascii')
        #Sql.RunQuery(update_saqict)

def add_contact(values,allvalues):
	Trace.Write("inside"+str(action_type))	
	record_ids= []
	master_object_name='SACONT'
	record_ids = [
					CPQID.KeyCPQId.GetKEYId(master_object_name, str(value))
					if value.strip() != "" and master_object_name in value
					else value
					for value in values
				]
	#record_ids = str(str(record_ids)[1:-1].replace("'",""))
	getquotedetails = SqlHelper.GetFirst("SELECT * FROM SAQTMT  (NOLOCK) WHERE MASTER_TABLE_QUOTE_RECORD_ID ='{contract_quote_record_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}'".format(contract_quote_record_id=contract_quote_record_id,quote_revision_record_id =quote_revision_record_id))
	Sql.RunQuery ("""
	INSERT SAQICT (
	QUOTE_REV_INVOLVED_PARTY_CONTACT_ID,
	QUOTE_ID,
	QUOTE_RECORD_ID,
	QTEREV_ID,
	QTEREV_RECORD_ID,
	CPQTABLEENTRYADDEDBY,
	CPQTABLEENTRYDATEADDED,
	CpqTableEntryDateModified,
	CONTACT_NAME,
	CONTACT_RECORD_ID,
	CITY,
	COUNTRY,
	COUNTRY_RECORD_ID,
	STATE,
	STATE_RECORD_ID,
	EMAIL,
	PHONE,
	POSTAL_CODE

	) SELECT
	CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REV_INVOLVED_PARTY_CONTACT_ID,
	'{quoteid}' as QUOTE_ID,
	'{quotrecid}' as QUOTE_RECORD_ID,
	'{quoterevid}' as QTEREV_ID,
	'{quoterevrecid}' as QTEREV_RECORD_ID,
	'TEST' AS CPQTABLEENTRYADDEDBY,
	GETDATE() as CPQTABLEENTRYDATEADDED,
	GETDATE() as CpqTableEntryDateModified,
	SACONT.CONTACT_NAME,
	SACONT.CONTACT_RECORD_ID,
	SACONT.CITY,
	SACONT.COUNTRY,
	SACONT.COUNTRY_RECORD_ID,
	SACONT.STATE,
	SACONT.STATE_RECORD_ID,
	SACONT.EMAIL,
	SACONT.PHONE,
	SACONT.POSTAL_CODE
	FROM SACONT (NOLOCK)
	WHERE
	SACONT.CONTACT_RECORD_ID IN ({record_ids})
	""".format(record_ids = record_ids,quoteid =getquotedetails.QUOTE_ID,quotrecid=getquotedetails.MASTER_TABLE_QUOTE_RECORD_ID,quoterevid = getquotedetails.QTEREV_ID,quoterevrecid =getquotedetails.QTEREV_RECORD_ID))

def mark_primary_contact(mark_primary_contact):
	
	updatefalsesaqict = """ UPDATE SAQICT SET [PRIMARY] = '0' WHERE QUOTE_RECORD_ID='{contract_quote_record_id}' and QTEREV_RECORD_ID = '{quote_revision_record_id}'  """.format(contract_quote_record_id=contract_quote_record_id,quote_revision_record_id =quote_revision_record_id)
	Sql.RunQuery(updatefalsesaqict)

	updatetruesaqict = """ UPDATE SAQICT SET [PRIMARY] = '1' WHERE QUOTE_RECORD_ID='{contract_quote_record_id}' and QTEREV_RECORD_ID = '{quote_revision_record_id}' and QUOTE_REV_INVOLVED_PARTY_CONTACT_ID ='{primaryprimary}'  """.format(contract_quote_record_id=contract_quote_record_id,quote_revision_record_id =quote_revision_record_id,primaryprimary = primaryprimary)
	Sql.RunQuery(updatetruesaqict)

	return True





try:
	allvalues = Param.AllValues
except:
	allvalues = ''

try:
	values = Param.Values
except:
	values= ''

try:
	action_type = Param.ActionType
except:
	action_type = ''
try:
	cont_rec_id = Param.cont_rec_id
except:
	cont_rec_id = ''
try:
	table_name = Param.table_name
except:
	table_name =''
try:
	repalce_values = Param.repalce_values
except:
	repalce_values = ''
try:
	primary_value = Param.primary_value
except:
	primary_value = ''
	

if action_type == "ADD_CONTACT":
	Trace.Write("inside"+str(action_type))
	ApiResponse = ApiResponseFactory.JsonResponse(add_contact(values,allvalues))
elif action_type == "MARK_PRIMARY"
	ApiResponse = ApiResponseFactory.JsonResponse(mark_primary_contact(primary_value))
# =========================================================================================================================================
#   __script_name : CQRPLACTCT.PY
#   __script_description : THIS SCRIPT IS USED TO REPLACE ACCOUNT AND CONTACT WHEN USER CLICKS ON REPLACE BUTTON ON A RELATED LIST RECORD.
#   __primary_author__ : WASIM ABDUL
#   __create_date : 19/10/2021
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import datetime
import Webcom.Configurator.Scripting.Test.TestProduct
import sys
import re
import System.Net
import SYCNGEGUID as CPQID
from SYDATABASE import SQL

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



class QuoteContactModel:
	
	def __init__(self, **kwargs):


		self.contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
		self.quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
		self.opertion = kwargs.get('opertion')
		self.action_type = kwargs.get('action_type')
		self.values = kwargs.get('values')
		self.table_name = kwargs.get('table_name')
		self.all_values = kwargs.get('all_values')		
		self.node_id = ""
	
	def _create(self):
		if self.action_type == "ADD_CONTACT" :
			Trace.Write('@@Contact'+str(list(values)))
			master_object_name = "SACONT"
			if self.values:
				record_ids = []
				record_ids = [
					CPQID.KeyCPQId.GetKEYId(master_object_name, str(value))
					if value.strip() != "" and master_object_name in value
					else value
					for value in self.values
				]
			record_ids = str(str(record_ids)[1:-1].replace("'",""))
			Trace.Write('@@Contact'+str(list(record_ids))

			
			self._process_query(
					"""
						INSERT SAQICT (
							QUOTE_REV_INVOLVED_PARTY_RECORD_ID,
							QUOTE_ID,
							QTEREV_ID,
							QTEREV_RECORD_ID,
							CPQTABLEENTRYADDEDBY,
							CPQTABLEENTRYDATEADDED,
							CpqTableEntryModifiedBy,
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
								CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REV_INVOLVED_PARTY_RECORD_ID,
								'{QuoteId}' as QUOTE_ID,
								'{RevisionId}' as QTEREV_ID,
								'{RevisionRecordId}' as QTEREV_RECORD_ID,
								'{UserName}' AS CPQTABLEENTRYADDEDBY,
								GETDATE() as CPQTABLEENTRYDATEADDED,
								{UserId} as CpqTableEntryModifiedBy,
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
								SACONT.CONTACT_RECORD_ID in ({})                        
						""".format(
						QuoteId=self.contract_quote_id,
						UserName=self.user_name,
						UserId=self.user_id,
						QuoteRecId=self.contract_quote_record_id,
						RevisionId=self.quote_revision_id,
						RevisionRecordId=self.quote_revision_record_id,
					)
				)
		else:
			""	

	



try:
    repalce_values = Param.repalce_values
    cont_rec_id = Param.cont_rec_id
    table_name = Param.table_name

except:
    repalce_values ='' 
    cont_rec_id = '' 
    table_name = '' 

#replace_contact(repalce_values,cont_rec_id,table_name)

def Factory(node=None):
	"""Factory Method"""
	models = {
		"CONTACT MODEL":QuoteContactModel
	}
	return models[node]

node_object = Factory(node_type)(
	opertion=opertion, action_type=action_type, table_name=table_name, values=values, 
	all_values=all_values, trigger_from=trigger_from, contract_quote_record_id=contract_quote_record_id, 
	apr_current_record_id= apr_current_record_id,
)




try:
		opertion = Param.Opertion
		node_type = Param.NodeType
		try:
			values = Param.Values
		except Exception:
			values = []
		try:
			A_Keys = Param.A_Keys
			A_Values = Param.A_Values
		except:
			A_Keys = ""
			A_Values = ""
		try:
			all_values = Param.AllValues
		except Exception:
			all_values = False
		try:
			table_name = Param.ObjectName
		except Exception:
			table_name = None
		try:
			action_type = Param.ActionType
		except Exception:
			action_type = None
		try:
			contract_quote_record_id = Param.ContractQuoteRecordId	
		except Exception:
			contract_quote_record_id = False
		
	except Exception as e:
		Trace.Write('error-'+str(e))
		pass	
 


if opertion == "ADD":
	node_object._create()








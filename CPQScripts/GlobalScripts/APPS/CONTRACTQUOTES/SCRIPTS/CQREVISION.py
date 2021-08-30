#===================================================================================================================#======================
#   __script_name : CQREVISION.PY
#   __script_description : THIS SCRIPT IS USED TO CREATE NEW REVISIONS AND UPDATE CUSTOM TABLES
#   __primary_author__ : SRIJAYDHURGA
#   __create_date :08/30/2021
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# #====================================================================================================================#======================
import Webcom.Configurator.Scripting.Test.TestProduct
import datetime
import time
from SYDATABASE import SQL
import clr
import sys
import System.Net
from System.Text.Encoding import UTF8
from System import Convert
import re
from datetime import timedelta , date

Sql = SQL()
ScriptExecutor = ScriptExecutor
quote_contract_recordId = Quote.GetGlobal("contract_quote_record_id")
Trace.Write('23----')
#create new revision start
def create_new_revision(Opertion):
	if Quote is not None:
		
		edit_new_rev_quote = QuoteHelper.Edit(Quote.CompositeNumber)
		create_new_rev = Quote.CreateNewRevision(True)
		composite_number = Quote.CompositeNumber
		current_revison = Quote.RevisionNumber

		quote_revision_table_info = Sql.GetTable("SAQTRV")
		quote_revision_id = str(Guid.NewGuid()).upper()
		#Quote.SetGlobal("quote_revision_record_id",str(quote_revision_id))
		quote_rev_data = {"QUOTE_REVISION_RECORD_ID": str(quote_revision_id),"QUOTE_ID": composite_number,"QUOTE_NAME": '',"QUOTE_RECORD_ID": quote_contract_recordId,"ACTIVE":0,"REV_CREATE_DATE":'',"REV_EXPIRE_DATE":'',"REVISION_STATUS":"IN-PROGRESS","QTEREV_ID":current_revison,"REV_APPROVE_DATE":''}
		quote_revision_table_info.AddRow(quote_rev_data)
		#Quote.GetCustomField('QUOTE_REVISION_ID').Content = quote_revision_id
		Log.Info('quote_revision_table_info---443--quote_rev_data--'+str(quote_rev_data))
		Sql.Upsert(quote_revision_table_info)

	return True
#craete new revision ends

Opertion = Param.Opertion
#Trace.Write(str(totalyear)+"--GET_DICT--------------"+str(GET_DICT))
ApiResponse = ApiResponseFactory.JsonResponse(create_new_revision(Opertion,))
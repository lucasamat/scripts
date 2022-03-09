# =========================================================================================================================================
#   __script_name : CQANULEDIT.PY
#   __script_description : THIS SCRIPT IS USED TO EDIT THE ANNUAL GRID BASED ON ENTITLEMENT PRICING
#   __primary_author__ : WASIM ABDUL 
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct
from SYDATABASE import SQL
import datetime
from datetime import datetime
Sql = SQL()
import SYCNGEGUID as CPQID

contract_quote_rec_id = Quote.GetGlobal("contract_quote_record_id")
quote_revision_rec_id = Quote.GetGlobal("quote_revision_record_id")
user_id = str(User.Id)
user_name = str(User.UserName) 
def constructcat4editablity(Quote_rec_id,MODE,values):
	#Trace.Write("Quote_rec_id"+str(Quote_rec_id))
	get_all_lines =Sql.GetList("Select * from SAQICO(NOLOCK) WHERE QUOTE_RECORD_ID ='{contract_quote_rec_id}' and QTEREV_RECORD_ID = '{quote_revision_rec_id}' AND LINE IN ({values})".format(contract_quote_rec_id = contract_quote_rec_id,quote_revision_rec_id = quote_revision_rec_id,values=",".join(values)))
	annaul_dict={}
	for line_values in get_all_lines:
		record_list=[]
		if line_values:
			if(line_values.NWPTON == 'Yes'):
				editvalue1 ='NWPTOP'
				editvalue2 ='NWPTOC'
				record_list.append(editvalue1)
				record_list.append(editvalue2)
			if(line_values.DEVICE_NODE == 'YES'):
				editvalue3 = 'CONSCP'
				editvalue4 = 'CONSPI'
				record_list.append(editvalue3)
				record_list.append(editvalue4)
		annaul_dict[line_values.LINE] = record_list
	Trace.Write("dictdictdict"+str(annaul_dict))
	return annaul_dict
	
	
	# record_dict={}
	# for inlines in values:
	# 	get_annual_values =Sql.GetFirst("Select * from SAQICO(NOLOCK) WHERE QUOTE_RECORD_ID ='{}' and QTEREV_RECORD_ID = '{}' AND LINE = '{}' and NWPTON ='yes'".format(contract_quote_rec_id,quote_revision_rec_id,inlines))
	# 	record_list=[]
	# 	if get_annual_values:
	# 		for editapi in get_annual_values:
	# 			if(editapi == 'NWPTON'):
	# 				record_list+= ['NWPTOP','NWPTOC']	
	# 		record_dict[inlines] = record_list	
		
	return True


ACTION = Param.ACTION
try:
	values = Param.values
except:
	values = ""


if ACTION == 'CAT4_ENTITLMENT':
    MODE="EDIT"
    Quote_rec_id = Quote.GetGlobal("contract_quote_record_id")
    ApiResponse = ApiResponseFactory.JsonResponse(constructcat4editablity(Quote_rec_id,MODE,values))

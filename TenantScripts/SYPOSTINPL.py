# =========================================================================================================================================
#   __script_name : SYPOSTINPL.PY
#   __script_description : THIS SCRIPT IS USED TO INSERT/UPDATE  DATA IN STAGING TABLES
#   __primary_author__ : BAJI
#   __create_date :
#   © BOSTON HARBOR TECHNOLOGY LLC 
# ==========================================================================================================================================
import sys
import datetime 
import sys
import clr
import System.Net
import System
from System.Text.Encoding import UTF8
from System import Convert
clr.AddReference("System.Net")
from System.Net import CookieContainer, NetworkCredential, Mail
from System.Net.Mail import SmtpClient, MailAddress, Attachment, MailMessage
from System.Net import HttpWebRequest, NetworkCredential
from System.Net import *
from System.Net import CookieContainer
from System.Net import Cookie
from System.Net import WebRequest
from System.Net import HttpWebResponse
from System import Uri



try:
	if 'Param' in globals(): 	
		if hasattr(Param, 'CPQ_Columns'): 
			rebuilt_data = ''
			quote_id = ''
			tbl_name = ''
			primaryQueryItems = SqlHelper.GetFirst("SELECT NEWID() AS A")
			for table_dict in Param.CPQ_Columns: 				
				tbl = str(table_dict.Key)
				tbl_name = tbl				
				Single_Record = {}
				Multiple_Record  = []    
				Dirct_record = {}
				for record_dict in table_dict.Value:
					tyty = str(type(record_dict))
					if str(tyty) == "<type 'KeyValuePair[str, object]'>":    
						
						Single_Record[str(record_dict.Key)] = record_dict.Value
					elif str(tyty) == "<type 'Dictionary[str, object]'>":
						colu_Info1 = {}
						for j in record_dict:								
												
							colu_Info1[str(j.Key)] = j.Value         
						Multiple_Record.append(colu_Info1)	
					else:
						Dirct_record[tbl] = str(table_dict.Value)
						if str(tbl).upper() == "QUOTE_ID":
							quote_id = str(table_dict.Value)
							
				
				if len(Dirct_record) > 0:
					for ins in Dirct_record:
						rebuilt_data = rebuilt_data+'"'+(str(ins)+'"'+":"+'"'+str(Dirct_record[ins]))+'"'+','
							
						
				if len(Single_Record) !=  0: 
					tbl = '"'+tbl+'"'
					rebuilt_data = rebuilt_data+(str(tbl)+":"+str(Single_Record))+','
						
				if len(Multiple_Record) !=  0: 
					tbl = '"'+tbl+'"'
					rebuilt_data = rebuilt_data+(str(tbl)+':'+str(Multiple_Record))+','
					
			rebuilt_data = str(rebuilt_data)[:-1]
			Final_data = "{ \"Param\" :''''{ \"CPQ_Columns\": {" + str(rebuilt_data).replace("'",'"') +"}}	''''}"
			#Native_data = "{ \"CPQ_Columns\": {" + str(rebuilt_data).replace("'",'"') +"}}"
			#Log.Info("Native_data --->"+str(Native_data))
			sessionid = SqlHelper.GetFirst("SELECT NEWID() AS A")
			timestamp_sessionid = "'" + str(sessionid.A) + "'"
			addby = User.UserName			
			#Log.Info("66666 Final_data --->"+str(Final_data))
			Parameter = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'SELECT' ")
			if str(tbl_name).upper() == "PREXRT":
				primaryQueryItems = SqlHelper.GetFirst( ""+ str(Parameter.QUERY_CRITERIA_1)+ " SYINPL (INTEGRATION_PAYLOAD,SESSION_ID,INTEGRATION_NAME)  select ''"+str(Final_data)+ "'','"+ str(timestamp_sessionid)+ "',''EXCHANGERATE_DATA'' ' ")

				result = ScriptExecutor.ExecuteGlobal("PRPOSTEXRT")

				ApiResponse = ApiResponseFactory.JsonResponse(
					{
						"Response": [
							{
								"Status": "200",
								"Message": "Data Sucessfully Uploaded ."
							}
						]
					}
				)
			
			else:
				primaryQueryItems = SqlHelper.GetFirst( ""+ str(Parameter.QUERY_CRITERIA_1)+ " SYINPL (INTEGRATION_PAYLOAD,INTEGRATION_NAME,SESSION_ID,CPQTABLEENTRYDATEADDED,CPQTABLEENTRYADDEDBY)  select ''"+str(Final_data)+ "'',''MATMAS'','"+ str(timestamp_sessionid)+ "',Getdate(),''"+str(addby)+ "'' ' ")

				

				ApiResponse = ApiResponseFactory.JsonResponse(
					{
						"Response": [
							{
								"Status": "200",
								"Message": "Data Sucessfully Uploaded ."
							}
						]
					}
				)
	


except:		
	Log.Info("SYPOSTINPL ERROR---->:" + str(sys.exc_info()[1]))
	Log.Info("SYPOSTINPL ERROR LINE NO---->:" + str(sys.exc_info()[-1].tb_lineno))
	ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "400", "Message": str(sys.exc_info()[1])}]})
# =========================================================================================================================================
#   __script_name : SYPOSTACPL.PY
#   __script_description : THIS SCRIPT IS USED TO INSERT/UPDATE  DATA IN STAGING TABLES
#   __primary_author__ : BAJI
#   __create_date :
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import sys
import datetime 
Log.Info("SYPOSTINPL TRIGERED---->")
try:
	if 'Param' in globals(): 	
		if hasattr(Param, 'CPQ_Columns'): 
			rebuilt_data = ''
			tbl_name = ''
			for table_dict in Param.CPQ_Columns: 				
				tbl = str(table_dict.Key)
				tbl_name = tbl				
				Single_Record = {}				
				Multiple_Record  = []				
				for record_dict in table_dict.Value:
					tyty = str(type(record_dict))
					if str(tyty) == "<type 'KeyValuePair[str, object]'>":
						Single_Record[str(record_dict.Key)] = (record_dict.Value).replace('"','\\"')
						
						
					elif str(tyty) == "<type 'Dictionary[str, object]'>":
						colu_Info1 = {}
						for j in record_dict:												
							colu_Info1[str(j.Key)] = (j.Value).replace('"','\\"')         
						Multiple_Record.append(colu_Info1)	
						
							
						
				if len(Single_Record) !=  0: 
					tbl = '"'+tbl+'"'
					rebuilt_data = rebuilt_data+(str(tbl)+":"+str(Single_Record))+','
						
				if len(Multiple_Record) !=  0: 
					tbl = '"'+tbl+'"'
					rebuilt_data = rebuilt_data+(str(tbl)+':'+str(Multiple_Record))+','				
				
					
			rebuilt_data = str(rebuilt_data)[:-1]
			
			Final_data = "{ \"CPQ_Columns\": {" + str(rebuilt_data).replace("'",'"') +"}}"
			sessionid = SqlHelper.GetFirst("SELECT NEWID() AS A")
			timestamp_sessionid = "'" + str(sessionid.A) + "'"
			
			
			primaryQueryItems = SqlHelper.GetFirst( "sp_executesql @statement = N'insert SYINPL (INTEGRATION_PAYLOAD,SESSION_ID,INTEGRATION_NAME,CPQTABLEENTRYDATEADDED)  select ''"+str(Final_data)+ "'','"+ str(timestamp_sessionid)+ "',''DEBMAS'',GetDate()' ")		
		
		
		
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
	Log.Info("SYPOSTACPL ERROR---->:" + str(sys.exc_info()[1]))
	Log.Info("SYPOSTACPL ERROR LINE NO---->:" + str(sys.exc_info()[-1].tb_lineno))
	ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "400", "Message": str(sys.exc_info()[1])}]})	
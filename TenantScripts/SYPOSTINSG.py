# =========================================================================================================================================
#   __script_name : SYPOSTINSG.PY
#   __script_description : THIS SCRIPT IS USED TO INSERT/UPDATE  DATA IN STAGING TABLES
#   __primary_author__ : BAJI
#   __create_date :
#   Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import sys
import datetime 
#Log.Info("SYPOSTINSG ---->Hitting")

try:
	if 'Param' in globals(): 	
		if hasattr(Param, 'CPQ_Columns'): 
			rebuilt_data = ''
			quote_id = ''
			primaryQueryItems = SqlHelper.GetFirst("SELECT NEWID() AS A")		
			for table_dict in Param.CPQ_Columns: 
				tbl = str(table_dict.Key)
				#Log.Info("6666 tbl---->"+str(tbl))
				
				Single_Record = {}
				Multiple_Record  = []    
				Dirct_record = {}
				for record_dict in table_dict.Value:
					#Log.Info("99999 record_dict ---->"+str(table_dict.Value))
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
							#Log.Info("quote id empty==>"+str(table_dict.Value))
							quote_id = str(table_dict.Value)
							
				
				if len(Dirct_record) > 0:
					for ins in Dirct_record:
						rebuilt_data = rebuilt_data+'"'+(str(ins)+'"'+":"+'"'+str(Dirct_record[ins]))+'"'+','
							
						
				if len(Single_Record) !=  0: 
					tbl = '"'+tbl+'"'
					rebuilt_data = rebuilt_data+(str(tbl)+":"+str(Single_Record))+','
					#rebuilt_data.append(sig_dict)
						
				if len(Multiple_Record) !=  0: 
					tbl = '"'+tbl+'"'
					rebuilt_data = rebuilt_data+(str(tbl)+':'+str(Multiple_Record))+','
					#rebuilt_data.append(mul_dict)
					
			#Log.Info("959595---->"+str(rebuilt_data))
			rebuilt_data = str(rebuilt_data)[:-1]
			Final_data = "{ \"Param\" :''''{ \"CPQ_Columns\": {" + str(rebuilt_data).replace("'",'"') +"}}	''''}"
			sessionid = SqlHelper.GetFirst("SELECT NEWID() AS A")
			timestamp_sessionid = "'" + str(sessionid.A) + "'"

			Parameter = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'SELECT' ")
			
			Parameter2 = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'DEL' ")

			primaryQueryItems = SqlHelper.GetFirst(
			""
			+ str(Parameter2.QUERY_CRITERIA_1)
			+ " SYINPL FROM SYINPL(NOLOCK) WHERE INTEGRATION_KEY = ''"+str(quote_id)+"'' and ISNULL(STATUS,'''') = '''' '"
			)
			#Log.Info("Final_data----"+str(Final_data))
			primaryQueryItems = SqlHelper.GetFirst( ""+ str(Parameter.QUERY_CRITERIA_1)+ " SYINPL (INTEGRATION_PAYLOAD,SESSION_ID,INTEGRATION_KEY)  select ''"+str(Final_data)+ "'','"+ str(timestamp_sessionid)+ "',''"+str(quote_id)+"'' ' ")
			
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
	Log.Info("SYPOSTINSG ERROR---->:" + str(sys.exc_info()[1]))
	Log.Info("SYPOSTINSG ERROR LINE NO---->:" + str(sys.exc_info()[-1].tb_lineno))
	ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "400", "Message": str(sys.exc_info()[1])}]})
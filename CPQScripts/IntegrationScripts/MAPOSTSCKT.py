# =========================================================================================================================================
#   __script_name : MAPOSTSCKT.PY
#   __script_description : THIS SCRIPT IS USED TO INSERT SSCM Kit BOM DATA TO CPQ(SYINPL) TABLE.
#   __primary_author__ : BAJI
#   __create_date :
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import sys
import datetime 
Log.Info("MAPOSTSCKT ---->Hitting")

try:
	if 'Param' in globals(): 	
		if hasattr(Param, 'CPQ_Columns'): 
			rebuilt_data = ''
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
			
			primaryQueryItems = SqlHelper.GetFirst( ""+ str(Parameter.QUERY_CRITERIA_1)+ " SYINPL (INTEGRATION_PAYLOAD,SESSION_ID,INTEGRATION_NAME)  select ''"+str(Final_data)+ "'','"+ str(timestamp_sessionid)+ "',''SSCM_TO_CPQ_KITBOM_DATA'' ' ")
			
			
			'''LOGIN_CREDENTIALS = SqlHelper.GetFirst("SELECT USER_NAME as Username,Password,Domain FROM SYCONF where Domain='AMAT_TST'")
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
				
				result = '<?xml version="1.0" encoding="UTF-8"?><soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"><soapenv:Body ></soapenv:Body></soapenv:Envelope>'
				
				#LOGIN_CRE = SqlHelper.GetFirst("SELECT URL FROM SYCONF where EXTERNAL_TABLE_NAME ='CPQ_TO_CRM_KITBOM_ASYNC'")
				Async = webclient.UploadString(str(LOGIN_CRE.URL), str(result))'''
			
			
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
	Log.Info("MAPOSTSCKT ERROR---->:" + str(sys.exc_info()[1]))
	Log.Info("MAPOSTSCKT ERROR LINE NO---->:" + str(sys.exc_info()[-1].tb_lineno))
	ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "400", "Message": str(sys.exc_info()[1])}]})	
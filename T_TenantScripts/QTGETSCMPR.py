# =========================================================================================================================================
#   __script_name : QTGETSCMPR.PY
#   __script_description : THIS SCRIPT IS USED TO INSERT SSCM PRICING DATA IN SYINPL TABLES
#   __primary_author__ : BAJI
#   __create_date :
#   Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import sys
import datetime 
import clr
import System.Net
from System.Text.Encoding import UTF8
from System import Convert
from System.Net import HttpWebRequest, NetworkCredential
from System.Net import *
clr.AddReference("System.Net")
from System.Net import CookieContainer, NetworkCredential, Mail
from System.Net.Mail import SmtpClient, MailAddress, Attachment, MailMessage

Log.Info("QTGETSCMPR Starts ---->Hitting")

try:
	if 'Param' in globals():    
		if hasattr(Param, 'CPQ_Columns'): 
			rebuilt_data = ''
			quote_id = ''
			Sesion_id = ''
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
						if str(record_dict.Key).upper() == "SESSION_ID":
							Sesion_id = record_dict.Value
						if str(record_dict.Key).upper() == "QUOTE_ID":
							quote_id = record_dict.Value
						
						
					elif str(tyty) == "<type 'Dictionary[str, object]'>":
						colu_Info1 = {}
						for j in record_dict:                               
												
							colu_Info1[str(j.Key)] = j.Value
							if str(j.Key).upper() == "SESSION_ID":
								Sesion_id = j.Value
							if str(j.Key).upper() == "QUOTE_ID":
								quote_id = j.Value

							
						Multiple_Record.append(colu_Info1)  
					else:
						Dirct_record[tbl] = str(table_dict.Value)
						if str(tbl).upper() == "QUOTE_ID":
							quote_id = str(table_dict.Value)
						if str(tbl).upper() == "SESSION_ID":
							Sesion_id = str(table_dict.Value)
							
				
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
			Final_data = "{ \"Param\" :''''{ \"CPQ_Columns\": {" + str(rebuilt_data).replace("'",'"') +"}}  ''''}"
			sessionid = SqlHelper.GetFirst("SELECT NEWID() AS A")
			timestamp_sessionid = "'" + str(sessionid.A) + "'"

			Parameter = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'SELECT' ")
			Parameter2 = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'DEL' ")

			LOGIN_CRE = SqlHelper.GetFirst("SELECT URL FROM SYCONF (nolock) where EXTERNAL_TABLE_NAME ='SSCM_DATA_GETMETHOD'")
			PSMA_CRE = SqlHelper.GetFirst("SELECT URL FROM SYCONF (nolock) where EXTERNAL_TABLE_NAME ='SSCM_DATA_GETMETHOD_PMSA'")
			TKM_CRE = SqlHelper.GetFirst("SELECT URL FROM SYCONF (nolock) where EXTERNAL_TABLE_NAME ='SSCM_DATA_GETMETHOD_TKM'")
			
			duplicatechecking = SqlHelper.GetFirst(
                "select 'x' as a from syinpl(nolock)  where integration_name='sscm_to_cpq_pricing_data1' and integration_payload like '%"+str(Sesion_id)+"%' "
            )
			
			if str(duplicatechecking) == "None":
				primaryQueryItems = SqlHelper.GetFirst( ""+ str(Parameter.QUERY_CRITERIA_1)+ " SYINPL (INTEGRATION_PAYLOAD,SESSION_ID,INTEGRATION_NAME,INTEGRATION_KEY,CpqTableEntryDateModified)  select ''"+str(Final_data)+ "'','"+ str(timestamp_sessionid)+ "',''SSCM_TO_CPQ_PRICING_DATA1'',''"+str(quote_id)+ "'',GETDATE() ' ")
				
				#CPI Iflow input
				result= '''<?xml version="1.0" encoding="UTF-8"?>
								<CPQ_Columns>
									<QUOTE_ID>{Qt_Id}</QUOTE_ID>
									<SESSION_ID>{Ses_Id}</SESSION_ID>
								</CPQ_Columns>'''.format(Qt_Id= quote_id,Ses_Id = Sesion_id)
				
				#CPI Iflow calling
				LOGIN_CREDENTIALS = SqlHelper.GetFirst("SELECT USER_NAME as Username,Password,Domain FROM SYCONF where Domain='AMAT_TST'")
				if LOGIN_CREDENTIALS is not None:
					Login_Username = str(LOGIN_CREDENTIALS.Username)
					Login_Password = str(LOGIN_CREDENTIALS.Password)
					authorization = Login_Username+":"+Login_Password
					binaryAuthorization = UTF8.GetBytes(authorization)
					authorization = Convert.ToBase64String(binaryAuthorization)
					authorization = "Basic " + authorization
				
				#PSMA CALL
				if 'Flex' in Sesion_id:
					#OAUTH token
					Oauth_info = SqlHelper.GetFirst("SELECT  DOMAIN,URL FROM SYCONF where EXTERNAL_TABLE_NAME ='OAUTH'")

					requestdata =Oauth_info.DOMAIN
					webclient = System.Net.WebClient()
					webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/x-www-form-urlencoded"
					response = webclient.UploadString(Oauth_info.URL,str(requestdata))
					response = eval(response)
					access_token = response['access_token']		


					webclient = System.Net.WebClient()
					webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/json"
					webclient.Headers[System.Net.HttpRequestHeader.Authorization] = authorization;
					webclient.Headers.Add("BearerToken", str(access_token))					
						

					LOGIN_CRE = SqlHelper.GetFirst("SELECT URL FROM SYCONF where EXTERNAL_TABLE_NAME ='SSCM_DATA_GETMETHOD_PMSA'")
					PSMA_response = webclient.UploadString(str(LOGIN_CRE.URL), str(result))
					PSMA_response = PSMA_response.replace("'",'%%')
					
					#Storing response in syinpl table
					primaryQueryItems = SqlHelper.GetFirst( ""+ str(Parameter.QUERY_CRITERIA_1)+ " SYINPL (INTEGRATION_PAYLOAD,SESSION_ID,INTEGRATION_NAME,INTEGRATION_KEY,CpqTableEntryDateModified)  select REPLACE(''"+str(PSMA_response)+ "'',''CM_LABOR_COST'',''LABOR_COST''),'"+ str(timestamp_sessionid)+ "',''SSCM_TO_CPQ_PRICING_DATA'',''"+str(quote_id)+ "'',GETDATE() ' ")
				#TKM CALL
				elif 'TKMKIT' in Sesion_id:
					#OAUTH token
					Oauth_info = SqlHelper.GetFirst("SELECT  DOMAIN,URL FROM SYCONF where EXTERNAL_TABLE_NAME ='OAUTH'")

					requestdata =Oauth_info.DOMAIN
					webclient = System.Net.WebClient()
					webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/x-www-form-urlencoded"
					response = webclient.UploadString(Oauth_info.URL,str(requestdata))
					response = eval(response)
					access_token = response['access_token']		


					webclient = System.Net.WebClient()
					webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/json"
					webclient.Headers[System.Net.HttpRequestHeader.Authorization] = authorization;
					webclient.Headers.Add("BearerToken", str(access_token))					
						

					LOGIN_CRE = SqlHelper.GetFirst("SELECT URL FROM SYCONF where EXTERNAL_TABLE_NAME ='SSCM_DATA_GETMETHOD_TKM'")
					TKM_response = webclient.UploadString(str(LOGIN_CRE.URL), str(result))
					TKM_response = TKM_response.replace("'",'%%')
					
					#Storing response in syinpl table
					primaryQueryItems = SqlHelper.GetFirst( ""+ str(Parameter.QUERY_CRITERIA_1)+ " SYINPL (INTEGRATION_PAYLOAD,SESSION_ID,INTEGRATION_NAME,INTEGRATION_KEY,CpqTableEntryDateModified)  select REPLACE(''"+str(TKM_response)+ "'',''CM_LABOR_COST'',''LABOR_COST'') ,'"+ str(timestamp_sessionid)+ "',''SSCM_TO_CPQ_PRICING_DATA'',''"+str(quote_id)+ "'',GETDATE() ' ")
				
				else:			
						
					#OAUTH token
					Oauth_info = SqlHelper.GetFirst("SELECT  DOMAIN,URL FROM SYCONF where EXTERNAL_TABLE_NAME ='OAUTH'")

					requestdata =Oauth_info.DOMAIN
					webclient = System.Net.WebClient()
					webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/x-www-form-urlencoded"
					response = webclient.UploadString(Oauth_info.URL,str(requestdata))
					response = eval(response)
					access_token = response['access_token']		


					webclient = System.Net.WebClient()
					webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/json"
					webclient.Headers[System.Net.HttpRequestHeader.Authorization] = authorization;
					webclient.Headers.Add("BearerToken", str(access_token))					
						

					LOGIN_CRE = SqlHelper.GetFirst("SELECT URL FROM SYCONF where EXTERNAL_TABLE_NAME ='SSCM_DATA_GETMETHOD'")
					response = webclient.UploadString(str(LOGIN_CRE.URL), str(result))
					response = response.replace("'",'%%')
					
					#Storing response in syinpl table
					primaryQueryItems = SqlHelper.GetFirst( ""+ str(Parameter.QUERY_CRITERIA_1)+ " SYINPL (INTEGRATION_PAYLOAD,SESSION_ID,INTEGRATION_NAME,INTEGRATION_KEY,CpqTableEntryDateModified)  select ''"+str(response)+ "'','"+ str(timestamp_sessionid)+ "',''SSCM_TO_CPQ_PRICING_DATA'',''"+str(quote_id)+ "'',GETDATE() ' ")			
				
				#Async call

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
					
					result = '<?xml version="1.0" encoding="UTF-8"?><soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"><soapenv:Body ></soapenv:Body></soapenv:Envelope>'
					
					LOGIN_CRE = SqlHelper.GetFirst("SELECT URL FROM SYCONF where EXTERNAL_TABLE_NAME ='CPQ_TO_SSCM_PRICING_ASYNC'")
					Async = webclient.UploadString(str(LOGIN_CRE.URL), str(result))
			
			
			
			rsp_msg = {
							"Status": "200",
							"Message": "Data Sucessfully Uploaded ."
						}
			rsp_msg['SESSION_ID'] = Sesion_id
			
			ApiResponse = ApiResponseFactory.JsonResponse(
				{
					"Response": [rsp_msg
						
					]
				}
			)
	
except:     
	Log.Info("QTGETSCMPR ERROR---->:" + str(sys.exc_info()[1]))
	Log.Info("QTGETSCMPR ERROR LINE NO---->:" + str(sys.exc_info()[-1].tb_lineno))
	ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "400", "Message": str(sys.exc_info()[1])}]})
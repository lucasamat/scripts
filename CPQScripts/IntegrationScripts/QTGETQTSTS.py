# =========================================================================================================================================
#   __script_name : QTGETQTSTS.PY
#   __script_description : THIS SCRIPT IS USED TO UPDATE  STATUS IN SAQTMT TABLES
#   __primary_author__ : BAJI
#   __create_date :
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import sys
import datetime 
Log.Info("QTGETQTSTS ---->Hitting")

import sys
import clr
import System.Net
from System.Text.Encoding import UTF8
from System import Convert
clr.AddReference("System.Net")
from System.Net import CookieContainer, NetworkCredential, Mail
from System.Net.Mail import SmtpClient, MailAddress, Attachment, MailMessage

try:
	if 'Param' in globals(): 	
		if hasattr(Param, 'CPQ_Columns'): 
			rebuilt_data = ''
			quote_id = ''
			Single_Record = {}
			Multiple_Record  = []    
			Dirct_record = {}
			primaryQueryItems = SqlHelper.GetFirst("SELECT NEWID() AS A")
			for table_dict in Param.CPQ_Columns: 
				
				tbl = str(table_dict.Key)				
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
						
			Log.Info("7575 Dirct_record --->"+str(Dirct_record))
			if len(Dirct_record) != 0:

				sessionid = SqlHelper.GetFirst("SELECT NEWID() AS A")
				timestamp_sessionid = "'" + str(sessionid.A) + "'"

				for ins in Dirct_record:
					rebuilt_data = rebuilt_data+'"'+(str(ins)+'"'+":"+'"'+str(Dirct_record[ins]))+'"'+','

				rebuilt_data = str(rebuilt_data)[:-1]
				Final_data = "{ \"Param\" :''''{ \"CPQ_Columns\": {" + str(rebuilt_data).replace("'",'"') +"}}	''''}"

				Parameter = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'SELECT' ")
				Parameter1 = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'UPD' ")
			
				primaryQueryItems = SqlHelper.GetFirst( ""+ str(Parameter.QUERY_CRITERIA_1)+ " SYINPL (INTEGRATION_PAYLOAD,SESSION_ID,INTEGRATION_NAME)  select ''"+str(Final_data)+ "'','"+ str(timestamp_sessionid)+ "',''QUOTE_STATUS_UPDATE'' ' ")



				today = datetime.datetime.now()
				Modi_date = today.strftime("%m/%d/%Y %H:%M:%S %p")
				if Dirct_record['STATUS_DESCRIPTION'].upper() == "SUCCESS":
					Parameter1 = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'UPD' ")
					primaryQueryItems = SqlHelper.GetFirst(""+ str(Parameter1.QUERY_CRITERIA_1)	+ "  SAQTRV SET REVISION_STATUS = ''SUBMITTED FOR BOOKING'' FROM SAQTRV(NOLOCK)  WHERE QUOTE_ID = ''"+str(Dirct_record['QUOTE_ID'])+"'' AND QTEREV_ID IN (SELECT QTEREV_ID FROM SAQTMT WHERE QUOTE_ID = ''"+str(Dirct_record['QUOTE_ID'])+"'' ) '")
					
					if 'CONTRACT_ID'  in Dirct_record:
						primaryQueryItems = SqlHelper.GetFirst(""+ str(Parameter1.QUERY_CRITERIA_1)	+ "  SAQTMT SET QUOTE_STATUS = ''CONVERTED CONTRACT'',CRM_CONTRACT_ID = ''"+str(Dirct_record['CONTRACT_ID'])+"'' FROM SAQTMT(NOLOCK)  WHERE C4C_QUOTE_ID = ''"+str(Dirct_record['QUOTE_ID'])+"'' '")
					
				if 'ERROR1'  in Dirct_record:
					primaryQueryItems = SqlHelper.GetFirst(""+ str(Parameter1.QUERY_CRITERIA_1)	+ "  SAQTRV SET IDOC_STATUS = ISNULL(IDOC_STATUS,'''')+ ''"+str(Dirct_record['ERROR1'])+"'' FROM SAQTRV(NOLOCK)  WHERE QUOTE_ID = ''"+str(Dirct_record['QUOTE_ID'])+"'' AND QTEREV_ID IN (SELECT QTEREV_ID FROM SAQTMT WHERE QUOTE_ID = ''"+str(Dirct_record['QUOTE_ID'])+"'' ) '")
				
				if 'ERROR2'  in Dirct_record:
					primaryQueryItems = SqlHelper.GetFirst(""+ str(Parameter1.QUERY_CRITERIA_1)	+ "  SAQTRV SET IDOC_STATUS = ISNULL(IDOC_STATUS,'''')+'' ; '' + ''"+str(Dirct_record['ERROR2'])+"'' FROM SAQTRV(NOLOCK)  WHERE QUOTE_ID = ''"+str(Dirct_record['QUOTE_ID'])+"'' AND QTEREV_ID IN (SELECT QTEREV_ID FROM SAQTMT WHERE QUOTE_ID = ''"+str(Dirct_record['QUOTE_ID'])+"'' ) '")
				
				if 'ERROR3'  in Dirct_record:
					primaryQueryItems = SqlHelper.GetFirst(""+ str(Parameter1.QUERY_CRITERIA_1)	+ "  SAQTRV SET IDOC_STATUS = ISNULL(IDOC_STATUS,'''')+'' ; '' +  ''"+str(Dirct_record['ERROR3'])+"'' FROM SAQTRV(NOLOCK)  WHERE QUOTE_ID = ''"+str(Dirct_record['QUOTE_ID'])+"'' AND QTEREV_ID IN (SELECT QTEREV_ID FROM SAQTMT WHERE QUOTE_ID = ''"+str(Dirct_record['QUOTE_ID'])+"'' ) '")
					
				if 'ERROR4'  in Dirct_record:
					primaryQueryItems = SqlHelper.GetFirst(""+ str(Parameter1.QUERY_CRITERIA_1)	+ "  SAQTRV SET IDOC_STATUS = ISNULL(IDOC_STATUS,'''')+'' ; '' +  ''"+str(Dirct_record['ERROR4'])+"'' FROM SAQTRV(NOLOCK)  WHERE QUOTE_ID = ''"+str(Dirct_record['QUOTE_ID'])+"'' AND QTEREV_ID IN (SELECT QTEREV_ID FROM SAQTMT WHERE QUOTE_ID = ''"+str(Dirct_record['QUOTE_ID'])+"'' ) '")
					
				if 'ERROR5'  in Dirct_record:
					primaryQueryItems = SqlHelper.GetFirst(""+ str(Parameter1.QUERY_CRITERIA_1)	+ "  SAQTRV SET IDOC_STATUS = ISNULL(IDOC_STATUS,'''')+'' ; '' + ''"+str(Dirct_record['ERROR5'])+"'' FROM SAQTRV(NOLOCK)  WHERE QUOTE_ID = ''"+str(Dirct_record['QUOTE_ID'])+"'' AND QTEREV_ID IN (SELECT QTEREV_ID FROM SAQTMT WHERE QUOTE_ID = ''"+str(Dirct_record['QUOTE_ID'])+"'' ) '")
				
				ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "200", "Message": "Data successfully updated"}]})

				if Dirct_record['STATUS_DESCRIPTION'].upper() == "ERROR":
					Header = "<!DOCTYPE html><html><head><style>table {font-family: Calibri, sans-serif; border-collapse: collapse; width: 75%}td, th {  border: 1px solid #dddddd;  text-align: left; padding: 8px;}.im {color: #222;}tr:nth-child(even) {background-color: #dddddd;} #grey{background: rgb(245,245,245);} #bd{color : 'black'} </style></head><body id = 'bd'>"


					Table_start = "<p>Hi Team,<br><br>The following Quote id having Error status description</p><table class='table table-bordered'><tr><th id ='grey'>QUOTE ID</th><th id = 'grey'>STATUS CODE</th><th id = 'grey'>STATUS DESCRIPTION</th></tr><tr><td >"+str(Dirct_record['QUOTE_ID'])+"</td><td >"+str(Dirct_record['STATUS_CODE'])+"</td ><td >"+str(Dirct_record['STATUS_DESCRIPTION'])+"</td></tr>"

					Table_info = ""
					Table_End = "</table><p><strong>Note : </strong>Please do not reply to this email.</p></body></html>"

					Error_Info = Header + Table_start + Table_info + Table_End

					LOGIN_CRE = SqlHelper.GetFirst("SELECT USER_NAME as Username,Password FROM SYCONF where Domain ='SUPPORT_MAIL'")

					# Create new SmtpClient object
					mailClient = SmtpClient()

					# Set the host and port (eg. smtp.gmail.com)
					mailClient.Host = "smtp.gmail.com"
					mailClient.Port = 587
					mailClient.EnableSsl = "true"

					# Setup NetworkCredential
					mailCred = NetworkCredential()
					mailCred.UserName = str(LOGIN_CRE.Username)
					mailCred.Password = str(LOGIN_CRE.Password)
					mailClient.Credentials = mailCred

					# Create two mail adresses, one for send from and the another for recipient
					toEmail = MailAddress("suresh.muniyandi@bostonharborconsulting.com")
					fromEmail = MailAddress("INTEGRATION.SUPPORT@BOSTONHARBORCONSULTING.COM")

					# Create new MailMessage object
					msg = MailMessage(fromEmail, toEmail)

					# Set message subject and body
					msg.Subject = "Quote Error Status - Notification(X-Tenant)"
					msg.IsBodyHtml = True
					msg.Body = Error_Info

					# Bcc Emails	
					copyEmail4 = MailAddress("baji.baba@bostonharborconsulting.com")
					msg.Bcc.Add(copyEmail4)

					# Send the message
					mailClient.Send(msg)

					ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "400", "Message": "Error Notification sended"}]})

			else:
				ApiResponse = ApiResponseFactory.JsonResponse(
					{"Response": [{"Status": "200", "Message": "NO DATA AVAILABLE FOR SYNCHRONIZATION"}]}
				) 

		else:
			if "ApiResponseFactory" in globals():
				ApiResponse = ApiResponseFactory.JsonResponse(
					{
						"Response": [
							{
								"Status": "400",
								"Message": "Invalid format.Param not available",
							}
						]
					}
				)

except:		
	Log.Info("QTGETQTSTS ERROR---->:" + str(sys.exc_info()[1]))
	Log.Info("QTGETQTSTS ERROR LINE NO---->:" + str(sys.exc_info()[-1].tb_lineno))
	ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "400", "Message": str(sys.exc_info()[1])}]})
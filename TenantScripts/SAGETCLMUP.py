 # =========================================================================================================================================
#   __script_name : SAGETCLMUP.PY
#   __script_description : THIS SCRIPT IS USED TO RETRIVE THE CLM AGREEMENT INFO AND UPDATE IN SAQTRV
#   __primary_author__ : BAJI
#   __create_date :
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================

import clr
import sys
import datetime
import System.Net
from System.Text.Encoding import UTF8
from System import Convert
import System
from System.Net import HttpWebRequest, NetworkCredential
from System.Net import *
from System.Net import CookieContainer
from System.Net import Cookie
from System.Net import WebRequest
from System.Net import HttpWebResponse
from System import Uri
clr.AddReference("System.Net")
from System.Net import CookieContainer, NetworkCredential, Mail
from System.Net.Mail import SmtpClient, MailAddress, Attachment, MailMessage
import time


try:
	Parameter=SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME='SELECT' ")
	Parameter1 = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'UPD' ")

	Oauth_info = SqlHelper.GetFirst("SELECT  DOMAIN,URL FROM SYCONF where EXTERNAL_TABLE_NAME ='OAUTH'")

	LOGIN_CRE = SqlHelper.GetFirst("SELECT URL FROM SYCONF (nolock) where EXTERNAL_TABLE_NAME ='CLM_DELETE_METHOD'")
	webRequest = str(LOGIN_CRE.URL)

	Check_Flag = 0

	while  Check_Flag == 0:


		def GetNewRequest(targetUrl, Btoken):

			newRequest = HttpWebRequest.Create(targetUrl)
			newRequest.AllowAutoRedirect = 0
			newRequest.Headers.Add("AUTHORIZATION", Btoken)
			newRequest.Method = 'DELETE'
			newRequest.ContentLength = 0
			newRequest.Headers.Add("Environment-Identifier", 'P')
			newRequest.ContentType = 'application/json'


			return newRequest


		try:
			requestdata =Oauth_info.DOMAIN
			webclient = System.Net.WebClient()
			webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/x-www-form-urlencoded"
			response = webclient.UploadString(Oauth_info.URL,str(requestdata))
		except:
			Log.Info("except exicuted--->")
			time.sleep(5)
			requestdata =Oauth_info.DOMAIN
			webclient = System.Net.WebClient()
			webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/x-www-form-urlencoded"
			response = webclient.UploadString(Oauth_info.URL,str(requestdata))
			
		response = eval(response)
		access_token = response['access_token']
		Btoken = "Bearer " + access_token


		rew = GetNewRequest(webRequest, Btoken)
		resp = rew.GetResponse()			

		streamReader = StreamReader(resp.GetResponseStream())
		jsonData = streamReader.ReadToEnd()	

		#Log.Info("456 -->"+str(jsonData))

		if jsonData != '' and len(jsonData) > 0:

			jsonData = jsonData.split("'")

			primaryQueryItems = SqlHelper.GetFirst( ""+ str(Parameter.QUERY_CRITERIA_1)+ " SYINPL (INTEGRATION_PAYLOAD,INTEGRATION_NAME,CPQTABLEENTRYDATEADDED,CPQTABLEENTRYADDEDBY)  select REPLACE(''"+str(jsonData[1])+ "'',''\\'',''''),''CLM_AGREEMENT_INFO'',Getdate(),''"+str(User.UserName)+ "'' ' ")

			rebuilt_data = eval(jsonData[1].replace('\\',''))
			
			if 'ErrorCode' in rebuilt_data['CPQ_Columns']:
				Qt_Id = rebuilt_data['CPQ_Columns']['CorrelationID']
				Error_Msg =rebuilt_data['CPQ_Columns']['ErrorMessage']

				ToEml = SqlHelper.GetFirst("SELECT ISNULL(OWNER_ID,'X0116954') as OWNER_ID FROM SAQTMT (NOLOCK) WHERE QUOTE_ID +'-'+CONVERT(VARCHAR,QTEREV_ID) = '"+str(Qt_Id)+"'  ")  

				if ToEml is None:
					OWNER_ID = 'X0116954'
				else:
					OWNER_ID = str(ToEml.OWNER_ID)



				# Mail system				
				Header = "<!DOCTYPE html><html><head><style>table {font-family: Calibri, sans-serif; border-collapse: collapse; width: 75%}td, th {  border: 1px solid #dddddd;  text-align: left; padding: 8px;}.im {color: #222;}tr:nth-child(even) {background-color: #dddddd;} #grey{background: rgb(245,245,245);} #bd{color : 'black';} </style></head><body id = 'bd'>"

				Table_start = "<p>Hi Team,<br><br>CLM Aggrement response getting follwing error message.</p><table class='table table-bordered'><tr><th id = 'grey'>Quote ID</th><th id = 'grey'>Error Message</th></tr><tr><td >"+str(Qt_Id)+"</td><td>"+str(Error_Msg)+"</td ></tr>"

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

				UserEmail = SqlHelper.GetFirst("SELECT isnull(email,'"+str(LOGIN_CRE.Username)+"') as email FROM saempl (nolock) where employee_id  = '"+str(OWNER_ID)+"'")

				# Create two mail adresses, one for send from and the another for recipient
				if UserEmail is None:
					toEmail = MailAddress("suresh.muniyandi@bostonharborconsulting.com")
				else:
					toEmail = MailAddress(UserEmail.email)
				fromEmail = MailAddress(str(LOGIN_CRE.Username))

				# Create new MailMessage object
				msg = MailMessage(fromEmail, toEmail)

				# Set message subject and body
				msg.Subject = "CLM Agrement Error Message - AMAT CPQ(P-Tenant)"
				msg.IsBodyHtml = True
				msg.Body = Error_Info

				# Bcc Emails	
				copyEmail4 = MailAddress("baji.baba@bostonharborconsulting.com")
				msg.Bcc.Add(copyEmail4)

				copyEmail6 = MailAddress("suresh.muniyandi@bostonharborconsulting.com")
				msg.Bcc.Add(copyEmail6) 

				# Send the message
				mailClient.Send(msg)

				ApiResponse = ApiResponseFactory.JsonResponse({	"Response": [{"Status": "400",
							"Message": "Error mail sent."}]}	)



			else:

				if 'CorrelationID' in rebuilt_data['CPQ_Columns']:
					Qt_Id = rebuilt_data['CPQ_Columns']['CorrelationID']
					AgreementNumber = rebuilt_data['CPQ_Columns']['AgreementNumber']
					
					primaryQueryItems = SqlHelper.GetFirst(
						""
						+ str(Parameter1.QUERY_CRITERIA_1)
						+ "  SAQTRV SET CLM_AGREEMENT_NUM=''"+ str(rebuilt_data['CPQ_Columns']['AgreementNumber'])+"'',CLM_AGREEMENT_ID = ''"+ str(rebuilt_data['CPQ_Columns']['AgreementID'])+"'',CLM_AGREEMENT_STATUS = UPPER(''"+ str(rebuilt_data['CPQ_Columns']['AgreementStatus'])+"''),CLM_AGREEMENT_URL = ''"+ str(rebuilt_data ['CPQ_Columns']['AgreementURL'])+"'' FROM SAQTRV (NOLOCK) WHERE SAQTRV.QUOTE_ID +''-''+CONVERT(VARCHAR,SAQTRV.QTEREV_ID) = ''"+ str(Qt_Id)+"''  ' "
					)										
										
					ToEml = SqlHelper.GetFirst("SELECT ISNULL(OWNER_ID,'X0116954') as OWNER_ID FROM SAQTMT (NOLOCK) WHERE QUOTE_ID +'-'+CONVERT(VARCHAR,QTEREV_ID) = '"+str(Qt_Id)+"'  ")  

					if ToEml is None:
						OWNER_ID = 'X0116954'
					else:
						OWNER_ID = str(ToEml.OWNER_ID)



					# Mail system				
					Header = "<!DOCTYPE html><html><head><style>table {font-family: Calibri, sans-serif; border-collapse: collapse; width: 75%}td, th {  border: 1px solid #dddddd;  text-align: left; padding: 8px;}.im {color: #222;}tr:nth-child(even) {background-color: #dddddd;} #grey{background: rgb(245,245,245);} #bd{color : 'black';} </style></head><body id = 'bd'>"

					Table_start = "<p>Hi Team,<br><br>CLM Aggrement has been successfully created.</p><table class='table table-bordered'><tr><th id = 'grey'>Quote ID</th><th id = 'grey'>Agreement Number</th></tr><tr><td >"+str(Qt_Id)+"</td><td>"+str(AgreementNumber)+"</td ></tr>"

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

					UserEmail = SqlHelper.GetFirst("SELECT isnull(email,'"+str(LOGIN_CRE.Username)+"') as email FROM saempl (nolock) where employee_id  = '"+str(OWNER_ID)+"'")
					
					# Create new SmtpClient object
					mailClient = SmtpClient("10.150.65.7")
				
					# Create two mail adresses, one for send from and the another for recipient
					if UserEmail is None:
						toEmail = MailAddress("suresh.muniyandi@bostonharborconsulting.com")
					else:
						toEmail = MailAddress(UserEmail.email)
					#fromEmail = MailAddress(str(LOGIN_CRE.Username))
					fromEmail = "noreply@calliduscloud.com"

					# Create new MailMessage object
					msg = MailMessage(fromEmail, toEmail)

					# Set message subject and body
					msg.Subject = "CLM Agrement Created - AMAT CPQ(P-Tenant)"
					msg.IsBodyHtml = True
					msg.Body = Error_Info

					# Bcc Emails	
					copyEmail4 = MailAddress("baji.baba@bostonharborconsulting.com")
					msg.Bcc.Add(copyEmail4)

					copyEmail6 = MailAddress("suresh.muniyandi@bostonharborconsulting.com")
					msg.Bcc.Add(copyEmail6) 

					# Send the message
					mailClient.Send(msg)
					
					ApiResponse = ApiResponseFactory.JsonResponse({	"Response": [{"Status": "200",
							"Message": "Data Sucessfully Uploaded ."}]}	)

					

		else:
			Check_Flag = 1
except:
	Log.Info("SAGETCLMUP ERROR---->:" + str(sys.exc_info()[1]))
	Log.Info("SAGETCLMUP ERROR LINE NO---->:" + str(sys.exc_info()[-1].tb_lineno))
	ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "400", "Message": str(sys.exc_info()[1])}]}) 
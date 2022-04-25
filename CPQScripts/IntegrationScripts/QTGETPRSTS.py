# =========================================================================================================================================
#   __script_name : QTGETPRSTS.PY
#   __script_description : THIS SCRIPT IS USED TO SEND PRICING STATUS OF SSCM
#   __primary_author__ : BAJI
#   __create_date :
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import sys
import clr
import System.Net
from System.Text.Encoding import UTF8
from System import Convert
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
			Final_data =  "{" + str(rebuilt_data) +"}"
			
			Log.Info("757575 Final_data --->"+str(Final_data))
			
			if "Successfully" in Final_data:
			
				Json_data = eval(Final_data)
				Qt_info = '' #3050013626-0
				
				for data in Json_data['QTQICA']:
					Qt_info = data['QUOTE_ID']
					
					
				Qt_info = Qt_info.split('-')		

				Qt_id = Qt_info[0]
				Revision_id = Qt_info[-1]

				Log.Info("757575 Qt_id --->"+str(Qt_id))
				Log.Info("757575 Revision_id --->"+str(Revision_id))			
			
			
				'''ToEml = SqlHelper.GetFirst("SELECT ISNULL(OWNER_ID,'X0116959') AS OWNER_ID FROM SAQTMT (NOLOCK) WHERE SAQTMT.QUOTE_ID = '"+str(Qt_id)+"'  ") 
				Header = "<!DOCTYPE html><html><head><style>table {font-family: Calibri, sans-serif; border-collapse: collapse; width: 75%}td, th {  border: 1px solid #dddddd;  text-align: left; padding: 8px;}.im {color: #222;}tr:nth-child(even) {background-color: #dddddd;} #grey{background: rgb(245,245,245);} #bd{color : 'black'} </style></head><body id = 'bd'>"
				Table_start = "<p>Hi Team,<br><br>The Tools and Assembly information has been successfully sent to retrieve the cost information from SSCM for the below Quote</p><table class='table table-bordered'><tr><th id ='grey'>QUOTE ID</th><th id = 'grey'>TOTAL TOOLS (CPQ)</th><th id = 'grey'>TOOLS SENT (SSCM)</th><th id = 'grey'>TOOLS NOT SENT TO SSCM (NO ASSEMBLY MAPPED)</th><th id = 'grey'>PRICING STATUS</th></tr><tr><td >"+str(Qt_id)+"</td><td >"+str(Emailinfo.CPQ)+"</td ><td >"+str(Emailinfo.SSCM)+"</td><td >"+str(Emailinfo.REMANING)+"</td><td>Acquiring</td></tr>"
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
				#Current user email(ToEmail)
				#UserId = User.Id
				#Log.Info("123 UserId.UserId --->"+str(UserId))
				UserEmail = SqlHelper.GetFirst("SELECT isnull(email,'"+str(LOGIN_CRE.Username)+"') as email FROM saempl (nolock) where employee_id  = '"+str(ToEml.OWNER_ID)+"'")
				#Log.Info("123 UserEmail.email --->"+str(UserEmail.email))
				# Create two mail adresses, one for send from and the another for recipient
				if UserEmail is None:
					toEmail = MailAddress("suresh.muniyandi@bostonharborconsulting.com")
				else:
					toEmail = MailAddress(UserEmail.email)
				fromEmail = MailAddress(str(LOGIN_CRE.Username))
				# Create new MailMessage object
				msg = MailMessage(fromEmail, toEmail)
				# Set message subject and body
				msg.Subject = "Quote Successfully Sent to SSCM(X-Tenant)"
				msg.IsBodyHtml = True
				msg.Body = Error_Info
				# Bcc Emails			
				copyEmail4 = MailAddress("baji.baba@bostonharborconsulting.com")
				msg.Bcc.Add(copyEmail4)
				copyEmail5 = MailAddress("suresh.muniyandi@bostonharborconsulting.com")
				msg.Bcc.Add(copyEmail5)
				copyEmail7 = MailAddress("christoper.aravinth@bostonharborconsulting.com")
				msg.Bcc.Add(copyEmail7)
				# Send the message
				mailClient.Send(msg)
				ApiResponse = ApiResponseFactory.JsonResponse(
				{"Response": [{"Status": "200", "Message": "Success mail sent"}]})
				
			else:
				indx_start = str(Final_data).find('[')
				indx_end = str(Final_data).find(']')+1
				Header = "<!DOCTYPE html><html><head><style>table {font-family: Calibri, sans-serif; border-collapse: collapse; width: 75%}td, th {  border: 1px solid #dddddd;  text-align: left; padding: 8px;}.im {color: #222;}tr:nth-child(even) {background-color: #dddddd;} #bd{color : 'black';} </style></head><body id = 'bd'>"
				Table_start = "<p>Hi Team,<br><br>The Quote Id "+Qt_id+" is not triggered for SSCM Pricing for below error.<br><br>"+str(Final_data[indx_start:indx_end])+"</p><br>"
				
				Table_End = "</table><p><strong>Note : </strong>Please do not reply to this email.</p></body></html>"
				Table_info = ""     
				Error_Info = Header + Table_start + Table_info + Table_End
				LOGIN_CRE = SqlHelper.GetFirst("SELECT USER_NAME as Username,Password FROM SYCONF where Domain ='SUPPORT_MAIL'")
				ToEml = SqlHelper.GetFirst("SELECT ISNULL(OWNER_ID,'X0116959') AS OWNER_ID FROM SAQTMT (NOLOCK) WHERE SAQTMT.QUOTE_ID = '"+str(Qt_id)+"'  ") 
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
				UserEmail = SqlHelper.GetFirst("SELECT isnull(email,'"+str(LOGIN_CRE.Username)+"') as email FROM saempl (nolock) where employee_id  = '"+str(ToEml.OWNER_ID)+"'")
				#Log.Info("123 UserEmail.email --->"+str(UserEmail.email))
				# Create two mail adresses, one for send from and the another for recipient
				if UserEmail is None:
					toEmail = MailAddress("suresh.muniyandi@bostonharborconsulting.com")
				else:
					toEmail = MailAddress(UserEmail.email)			
				
				fromEmail = MailAddress(str(LOGIN_CRE.Username))
				# Create new MailMessage object
				msg = MailMessage(fromEmail, toEmail)
				# Set message subject and body
				msg.Subject = "CPQ to SSCM - Triggering Error Notification(X-Tenant)"
				msg.IsBodyHtml = True
				msg.Body = Error_Info
				# CC Emails 		
				copyEmail3 = MailAddress("suresh.muniyandi@bostonharborconsulting.com")
				msg.Bcc.Add(copyEmail3)	
				copyEmail4 = MailAddress("baji.baba@bostonharborconsulting.com")
				msg.CC.Add(copyEmail4)
				copyEmail7 = MailAddress("christoper.aravinth@bostonharborconsulting.com")
				msg.Bcc.Add(copyEmail7)
				
				# Send the message
				mailClient.Send(msg)
				ApiResponse = ApiResponseFactory.JsonResponse(
				{"Response": [{"Status": "200", "Message": "Error mail sent"}]})'''
				
except:		
	Log.Info("QTGETPRSTS ERROR---->:" + str(sys.exc_info()[1]))
	Log.Info("QTGETPRSTS ERROR LINE NO---->:" + str(sys.exc_info()[-1].tb_lineno))
	ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "400", "Message": str(sys.exc_info()[1])}]})
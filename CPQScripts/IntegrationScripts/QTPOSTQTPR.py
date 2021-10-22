import sys
import datetime
import clr
import System.Net
from System.Text.Encoding import UTF8
from System import Convert
from SYDATABASE import SQL
import CQVLDRIFLW

clr.AddReference("System.Net")
from System.Net import CookieContainer, NetworkCredential, Mail
from System.Net.Mail import SmtpClient, MailAddress, Attachment, MailMessage

Parameter = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'SELECT' ")
Parameter1 = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'UPD' ")
Parameter2 = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'DEL' ")

SYINPL_SESSION = SqlHelper.GetFirst("SELECT NEWID() AS A")

exceptinfo = ''

try:

	Stausquery = SqlHelper.GetFirst("SELECT count(*) as cnt from SYINPL(NOLOCK) WHERE INTEGRATION_NAME = 'SSCM_TO_CPQ_PRICING_DATA' AND ISNULL(STATUS,'') = 'INPROGRESS' ")	
	
	if Stausquery.cnt == 0:

		#Status Inprogress SYINPL by CPQ Table Entry ID
		
		StatusUpdateQuery = SqlHelper.GetFirst(""+ str(Parameter1.QUERY_CRITERIA_1)+ "  SYINPL SET STATUS = ''ERROR'',SESSION_ID=''"+str(SYINPL_SESSION.A)+"'' FROM SYINPL (NOLOCK)  WHERE isnull(status,'''')='''' AND INTEGRATION_NAME = ''SSCM_TO_CPQ_PRICING_DATA'' AND INTEGRATION_PAYLOAD NOT LIKE ''%QUOTE_ID%'' ' ")

		StatusUpdateQuery = SqlHelper.GetFirst(""+ str(Parameter1.QUERY_CRITERIA_1)+ "  SYINPL SET STATUS = ''INPROGRESS'',SESSION_ID=''"+str(SYINPL_SESSION.A)+"'' FROM SYINPL (NOLOCK)  WHERE isnull(status,'''')='''' AND INTEGRATION_NAME = ''SSCM_TO_CPQ_PRICING_DATA''  ' ")

		#Status Empty
		Jsonquery = SqlHelper.GetList("SELECT replace(INTEGRATION_PAYLOAD,'null','\"\"') as INTEGRATION_PAYLOAD,CpqTableEntryId from SYINPL(NOLOCK) WHERE INTEGRATION_NAME = 'SSCM_TO_CPQ_PRICING_DATA' AND ISNULL(STATUS,'') = 'INPROGRESS' AND SESSION_ID = '"+str(SYINPL_SESSION.A)+"' ")
		
		for json_data in Jsonquery:
				
			exceptinfo = str(json_data.CpqTableEntryId)
			sessiondetail = SqlHelper.GetFirst("SELECT NEWID() AS A")
			
			if "Param" in str(json_data.INTEGRATION_PAYLOAD):
				splited_list = str(json_data.INTEGRATION_PAYLOAD).split("%%")
				rebuilt_data = eval(str(splited_list[1]))
			else:
				splited_list = str(json_data.INTEGRATION_PAYLOAD)
				rebuilt_data = eval(splited_list)		
			
			primaryQuerysession =  SqlHelper.GetFirst("SELECT NEWID() AS A")
			today = datetime.datetime.now()
			Modi_date = today.strftime("%m/%d/%Y %H:%M:%S %p")


			if len(rebuilt_data) != 0:      

				rebuilt_data = rebuilt_data["CPQ_Columns"]
				Table_Names = rebuilt_data.keys()
				Check_flag = 0
				Qt_Id = ''
				Saqico_Flag = 0
				
				for tn in Table_Names:
					if tn in rebuilt_data:	
						if 1:
							if str(type(rebuilt_data[tn])) == "<type 'dict'>":
								Tbl_data = [rebuilt_data[tn]]
							else:
								Tbl_data = rebuilt_data[tn]
								
							for record_dict in Tbl_data:

								if 'HEADBUILD_QTY' not in record_dict:
									record_dict['HEADBUILD_QTY'] = ''

								primaryQueryItems = SqlHelper.GetFirst( ""+ str(Parameter.QUERY_CRITERIA_1)+ " SAQICO_INBOUND (SESSION_ID,QUOTE_ID,EQUIPMENT_ID,ASSEMBLY_ID,SERVICE_ID,COST_MODULE_AVAILABLE,ASSEMBLY_NOT_REQUIRED_FLAG,GREATER_THAN_QTLY_COST,LESS_THAN_QTLY_COST,CLEAN_COST,SEEDSTOCK_COST,METROLOGY_COST,REFURB_COST,RECOATING_COST,CM_PART_COST,PM_PART_COST,LABOUR_COST,KPI_COST,TOTAL_COST_WISEEDSTOCK,TOTAL_COST_WOSEEDSTOCK,COST_CALCULATION_STATUS,NPI,SERVICE_COMPLEXITY,HEADREBUILD_QTY)  select ''"+str(sessiondetail.A)+ "'',''"+str(record_dict['QUOTE_ID'])+ "'',''"+str(record_dict['EQUIPMENT_ID'])+ "'',''"+str(record_dict['ASSEMBLY_ID'])+ "'',''"+ str(record_dict['SERVICE_ID'])+ "'',''"+ str(record_dict['COST_MODULE_AVAILABLE'])+ "'',''"+ str(record_dict['ASSEMBLY_NOT_REQUIRED_FLAG'])+ "'',''"+ str(record_dict['GREATER_THAN_QTLY_COST'])+ "'',''"+ str(record_dict['LESS_THAN_QTLY_COST'])+ "'',''"+str(record_dict['CLEAN_COST'])+ "'',''"+str(record_dict['SEEDSTOCK_COST'])+ "'',''"+str(record_dict['METROLOGY_COST'])+ "'',''"+str(record_dict['REFURB_COST'])+ "'',''"+str(record_dict['RECOATING_COST'])+ "'',''"+str(record_dict['CM_PART_COST'])+ "'',''"+str(record_dict['PM_PART_COST'])+ "'',''"+str(record_dict['LABOR_COST'])+ "'',''"+str(record_dict['KPI_COST'])+ "'',''"+str(record_dict['TOTAL_COST_WISEEDSTOCK'])+ "'',''"+str(record_dict['TOTAL_COST_WOSEEDSTOCK'])+ "'',''"+str(record_dict['COST_CALCULATION_STATUS'])+ "'',''"+str(record_dict['NPI'])+ "'',''"+str(record_dict['SERVICE_COMPLEXITY'])+ "'',CASE WHEN ISNULL(''"+str(record_dict['HEADBUILD_QTY'])+ "'','''')='''' THEN NULL ELSE ''"+str(record_dict['HEADBUILD_QTY'])+ "'' END ' ")
								
								
								Check_flag = 1
				
				primaryQueryItems = SqlHelper.GetFirst(
									""
									+ str(Parameter1.QUERY_CRITERIA_1)
									+ "  SAQICO_INBOUND SET QUOTE_ID = B.QUOTE_ID,REVISION_ID = B.QTEREV_ID FROM SAQICO_INBOUND (NOLOCK) A JOIN SAQTRV B(NOLOCK) ON A.QUOTE_ID = B.QUOTE_ID+''-''+CONVERT(VARCHAR,QTEREV_ID)  WHERE ISNULL(PROCESS_STATUS,'''')='''' AND ISNULL(SESSION_ID,'''')=''"+str(sessiondetail.A)+ "'' '")
								
				Qt_Id = SqlHelper.GetFirst("select QUOTE_ID,REVISION_ID from SAQICO_INBOUND(Nolock) where ISNULL(SESSION_ID,'')='"+str(sessiondetail.A)+ "' ")
				
				Saqicoquery = SqlHelper.GetFirst("select count(*) as cnt from SAQICO(Nolock) where QUOTE_ID = '"+str(Qt_Id.QUOTE_ID)+"' AND SAQICO.QTEREV_ID = '"+str(Qt_Id.REVISION_ID)+"' ")
				
				if Saqicoquery.cnt >0:
					Saqico_Flag = 1
				
				if Check_flag == 1 and Saqico_Flag == 1:  

					Emailinfo = SqlHelper.GetFirst("SELECT QUOTE_ID,SSCM,0 as REMANING,QUOTE_RECORD_ID FROM (SELECT SAQICO.QUOTE_ID,COUNT(DISTINCT SAQICO.EQUIPMENT_ID) AS SSCM,SAQICO.QUOTE_RECORD_ID  FROM SAQICO (NOLOCK) WHERE SAQICO.QUOTE_ID = '"+str(Qt_Id.QUOTE_ID)+"' AND SAQICO.QTEREV_ID = '"+str(Qt_Id.REVISION_ID)+"' AND ISNULL(STATUS,'')<> '' group by SAQICO.Quote_ID,SAQICO.QUOTE_RECORD_ID )SUB_SAQICO ")  
					
					ToEml = SqlHelper.GetFirst("SELECT ISNULL(OWNER_ID,'X0116959') as OWNER_ID FROM SAQTMT (NOLOCK) WHERE SAQTMT.QUOTE_ID = '"+str(Qt_Id.QUOTE_ID)+"'  ")  
					
					Emailinfo1 = SqlHelper.GetFirst("SELECT QUOTE_ID,CPQ FROM (SELECT SAQICO_INBOUND.QUOTE_ID,COUNT(DISTINCT SAQICO_INBOUND.EQUIPMENT_ID) AS CPQ FROM SAQICO_INBOUND (NOLOCK) WHERE SAQICO_INBOUND.QUOTE_ID = '"+str(Qt_Id.QUOTE_ID)+"' AND SAQICO_INBOUND.REVISION_ID = '"+str(Qt_Id.REVISION_ID)+"' AND ISNULL(SESSION_ID,'')='"+str(sessiondetail.A)+ "' group by SAQICO_INBOUND.Quote_ID )SUB_SAQICO ")  
				
					# Mail system				
					Header = "<!DOCTYPE html><html><head><style>table {font-family: Calibri, sans-serif; border-collapse: collapse; width: 75%}td, th {  border: 1px solid #dddddd;  text-align: left; padding: 8px;}.im {color: #222;}tr:nth-child(even) {background-color: #dddddd;} #grey{background: rgb(245,245,245);} #bd{color : 'black';} </style></head><body id = 'bd'>"

					Table_start = "<p>Hi Team,<br><br>Cost data has been received from SSCM for the below Quote ID and the CPQ price calculation has been initiated. Will let you know shortly about the pricing status.</p><table class='table table-bordered'><tr><th id = 'grey'>Quote ID</th><th id = 'grey'>Tools sent (CPQ-SSCM)</th><th id = 'grey'>Tools received (SSCM-CPQ)</th><th id = 'grey'>Price Calculation Status</th></tr><tr><td >"+str(Qt_Id.QUOTE_ID)+"</td><td>"+str(Emailinfo.SSCM)+"</td ><td>"+str(Emailinfo1.CPQ)+"</td><td>Initiated</td></tr>"

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

					UserEmail = SqlHelper.GetFirst("SELECT isnull(email,'INTEGRATION.SUPPORT@BOSTONHARBORCONSULTING.COM') as email FROM saempl (nolock) where employee_id  = '"+str(ToEml.OWNER_ID)+"'")

					# Create two mail adresses, one for send from and the another for recipient
					if UserEmail is None:
						toEmail = MailAddress("suresh.muniyandi@bostonharborconsulting.com")
					else:
						toEmail = MailAddress(UserEmail.email)
					fromEmail = MailAddress("INTEGRATION.SUPPORT@BOSTONHARBORCONSULTING.COM")

					# Create new MailMessage object
					msg = MailMessage(fromEmail, toEmail)

					# Set message subject and body
					msg.Subject = "Pricing Initiated - AMAT CPQ(X-Tenant)"
					msg.IsBodyHtml = True
					msg.Body = Error_Info

					# Bcc Emails	
					copyEmail4 = MailAddress("baji.baba@bostonharborconsulting.com")
					msg.Bcc.Add(copyEmail4)

					copyEmail1 = MailAddress("ranjani.parkavi@bostonharborconsulting.com")
					msg.Bcc.Add(copyEmail1) 

					copyEmail3 = MailAddress("sathyabama.akhala@bostonharborconsulting.com")
					msg.Bcc.Add(copyEmail3)

					#copyEmail5 = MailAddress("ashish.gandotra@bostonharborconsulting.com")
					#msg.Bcc.Add(copyEmail5)
					
					copyEmail6 = MailAddress("suresh.muniyandi@bostonharborconsulting.com")
					msg.Bcc.Add(copyEmail6) 

					copyEmail7 = MailAddress("arivazhagan.natarajan@bostonharborconsulting.com")
					msg.Bcc.Add(copyEmail7)

					copyEmail8 = MailAddress("indira.priyadarsini@bostonharborconsulting.com")
					msg.Bcc.Add(copyEmail8)

					copyEmail2 = MailAddress("zeeshan.ahamed@bostonharborconsulting.com")
					msg.Bcc.Add(copyEmail2)

					copyEmail9 = MailAddress("siva.subramani@bostonharborconsulting.com")
					msg.Bcc.Add(copyEmail9)

					# Send the message
					mailClient.Send(msg)

					#Calculation code started	
					sessionid = SqlHelper.GetFirst("SELECT NEWID() AS A")
					timestamp_sessionid = "'" + str(sessionid.A) + "'"	
					
					CRMQT = SqlHelper.GetFirst("select convert(varchar(100),c4c_quote_id) as c4c_quote_id from SAQTMT(nolock) WHERE QUOTE_ID = '"+str(Qt_Id.QUOTE_ID)+"' ") 
					
					primaryQueryItems = SqlHelper.GetFirst(
						""
						+ str(Parameter1.QUERY_CRITERIA_1)
						+ "  SAQICO_INBOUND SET TIMESTAMP = '"+str(timestamp_sessionid)+"',PROCESS_STATUS = ''INPROGRESS'' FROM SAQICO_INBOUND (NOLOCK)  WHERE ISNULL(PROCESS_STATUS,'''')='''' AND ISNULL(SESSION_ID,'''')=''"+str(sessiondetail.A)+ "'' '")
					
					#Entitlement Temp					
					SAQIEN = "SAQIEN_BKP_"+str(CRMQT.c4c_quote_id)
					CRMTMP = "CRMTMP_BKP_"+str(CRMQT.c4c_quote_id)
					
					#Exchange Rate
					roundcurr1 = SqlHelper.GetFirst("select distinct CASE WHEN ROUNDING_DECIMAL_PLACES = '' THEN 0  ELSE ROUNDING_DECIMAL_PLACES END  AS DECIMAL_PLACES,CASE WHEN ROUNDING_METHOD='ROUND DOWN' THEN 1 ELSE 0 END AS ROUNDING_METHOD from prcurr (nolock) where currency= 'USD' ")
					
					roundcurr = SqlHelper.GetFirst("select distinct CASE WHEN ROUNDING_DECIMAL_PLACES = '' THEN 0  ELSE ROUNDING_DECIMAL_PLACES END  AS DECIMAL_PLACES,CASE WHEN ROUNDING_METHOD='ROUND DOWN' THEN 1 ELSE 0 END AS ROUNDING_METHOD from SAQICO(nolock) a join prcurr (nolock) on a.DOC_CURRENCY = prcurr.currency where QUOTE_ID = '"+str(Qt_Id.QUOTE_ID)+"' AND QTEREV_ID = '"+str(Qt_Id.REVISION_ID)+"' ")
						
					primaryQueryItems = SqlHelper.GetFirst(
						""
						+ str(Parameter1.QUERY_CRITERIA_1)
						+ "  SAQICO_INBOUND SET EXCHANGE_RATE = SAQICO.EXCHANGE_RATE FROM SAQICO_INBOUND (NOLOCK) JOIN SAQICO (NOLOCK) ON SAQICO_INBOUND.QUOTE_ID = SAQICO.QUOTE_ID AND SAQICO_INBOUND.EQUIPMENT_ID = SAQICO.EQUIPMENT_ID AND SAQICO_INBOUND.SERVICE_ID = SAQICO.SERVICE_ID AND SAQICO_INBOUND.REVISION_ID = SAQICO.QTEREV_ID WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'   ' ")
					
					#Quote Item Covered Object Assembly Update 
					primaryQueryItems = SqlHelper.GetFirst(
						""
						+ str(Parameter1.QUERY_CRITERIA_1)
						+ "  A SET CM_PART_COST=CONVERT(FLOAT,B.CM_PART_COST),PM_PART_COST = CONVERT(FLOAT,B.PM_PART_COST),ASSEMBLY_NOT_MAPPED = B.ASSEMBLY_NOT_REQUIRED_FLAG,CLEANING_COST = CONVERT(FLOAT,B.CLEAN_COST),COST_MODULE_AVAILABLE = B.COST_MODULE_AVAILABLE,COST_MODULE_STATUS = B.COST_CALCULATION_STATUS,GREATER_THAN_QTLY_PM_COST = CONVERT(FLOAT,B.GREATER_THAN_QTLY_COST),KPI_COST = CONVERT(FLOAT,B.KPI_COST),LABOR_COST = CONVERT(FLOAT,B.LABOUR_COST),LESS_THAN_QTLY_PM_COST= CONVERT(FLOAT,B.LESS_THAN_QTLY_COST),METROLOGY_COST=CONVERT(FLOAT, B.METROLOGY_COST),RECOATING_COST = CONVERT(FLOAT,B.RECOATING_COST),REFURB_COST = CONVERT(FLOAT,B.REFURB_COST),SEEDSTOCK_COST = CONVERT(FLOAT,B.SEEDSTOCK_COST),TOTAL_COST_WOSEEDSTOCK = CONVERT(FLOAT,B.TOTAL_COST_WOSEEDSTOCK),TOTAL_COST_WSEEDSTOCK = CONVERT(FLOAT,TOTAL_COST_WISEEDSTOCK),NPI = B.NPI,SERVICE_COMPLEXITY = B.SERVICE_COMPLEXITY FROM SAQICA A(NOLOCK) JOIN SAQICO_INBOUND B(NOLOCK) ON A.QUOTE_ID = B.QUOTE_ID AND A.QTEREV_ID = B.REVISION_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.ASSEMBLY_ID = B.ASSEMBLY_ID WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  ' ")
					
					#Quote Item Covered Object Roll Up Cost
					primaryQueryItems = SqlHelper.GetFirst(
						""
						+ str(Parameter1.QUERY_CRITERIA_1)
						+ "  A SET CM_PART_COST=B.CM_PART_COST,PM_PART_COST = B.PM_PART_COST,CLEANING_COST = B.CLEAN_COST,GREATER_THAN_QTLY_PM_COST = B.GREATER_THAN_QTLY_COST,KPI_COST = B.KPI_COST,LABOR_COST = B.LABOUR_COST,LESS_THAN_QTLY_PM_COST= B.LESS_THAN_QTLY_COST,METROLOGY_COST= B.METROLOGY_COST,RECOATING_COST = B.RECOATING_COST,REFURB_COST = B.REFURB_COST,SEEDSTOCK_COST = B.SEEDSTOCK_COST,TOTAL_COST_WOSEEDSTOCK = B.TOTAL_COST_WOSEEDSTOCK,TOTAL_COST_WSEEDSTOCK = TOTAL_COST_WISEEDSTOCK,HEAD_REBUILD_QTY= B.HEADREBUILD_QTY FROM SAQICO A(NOLOCK) JOIN (SELECT QUOTE_ID,SERVICE_ID,EQUIPMENT_ID,SUM(CONVERT(FLOAT,CM_PART_COST)) AS CM_PART_COST,SUM(CONVERT(FLOAT,PM_PART_COST)) AS PM_PART_COST,SUM(CONVERT(FLOAT,CLEAN_COST)) AS CLEAN_COST, SUM(CONVERT(FLOAT,GREATER_THAN_QTLY_COST)) AS GREATER_THAN_QTLY_COST,SUM(CONVERT(FLOAT,KPI_COST)) AS KPI_COST,SUM(CONVERT(FLOAT,LABOUR_COST)) AS LABOUR_COST,SUM(CONVERT(FLOAT,LESS_THAN_QTLY_COST)) AS LESS_THAN_QTLY_COST,SUM(CONVERT(FLOAT,METROLOGY_COST)) AS METROLOGY_COST,SUM(CONVERT(FLOAT,RECOATING_COST)) AS RECOATING_COST,SUM(CONVERT(FLOAT,REFURB_COST)) AS REFURB_COST, SUM(CONVERT(FLOAT,SEEDSTOCK_COST)) AS SEEDSTOCK_COST,SUM(CONVERT(FLOAT,TOTAL_COST_WOSEEDSTOCK)) AS TOTAL_COST_WOSEEDSTOCK,SUM(CONVERT(FLOAT,TOTAL_COST_WISEEDSTOCK)) AS TOTAL_COST_WISEEDSTOCK,REVISION_ID,MIN(HEADREBUILD_QTY) AS HEADREBUILD_QTY  FROM SAQICO_INBOUND B(NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' GROUP BY QUOTE_ID,SERVICE_ID,EQUIPMENT_ID,REVISION_ID  )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.QTEREV_ID = B.REVISION_ID ' ")
					
					#NPI
					
					primaryQueryItems = SqlHelper.GetFirst(
						""
						+ str(Parameter1.QUERY_CRITERIA_1)
						+ "  A SET TOOL_NPI = ''Yes'' FROM SAQICO_INBOUND A(NOLOCK) JOIN (SELECT QUOTE_ID,SERVICE_ID,EQUIPMENT_ID,TIMESTAMP,SESSION_ID FROM SAQICO_INBOUND (NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND NPI = ''TRUE'' )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.TIMESTAMP = B.TIMESTAMP AND A.SESSION_ID = B.SESSION_ID  ' ")

					primaryQueryItems = SqlHelper.GetFirst(
											""
											+ str(Parameter1.QUERY_CRITERIA_1)
											+ "  SAQICO_INBOUND SET TOOL_NPI = ''No'' FROM SAQICO_INBOUND (NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND ISNULL(TOOL_NPI,'''') = ''''  ' ")
					
					#Z0091
					primaryQueryItems = SqlHelper.GetFirst(
												""
												+ str(Parameter1.QUERY_CRITERIA_1)
												+ "  A SET NPI_COEFFICIENT = CONVERT(VARCHAR,ENTITLEMENT_COEFFICIENT) FROM SAQICO_INBOUND (NOLOCK) A JOIN PRENVL B(NOLOCK) ON A.TOOL_NPI = B.ENTITLEMENT_DISPLAY_VALUE WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND ISNULL(TOOL_NPI,'''') <> '''' AND ENTITLEMENT_ID = ''AGS_Z0091_VAL_NPIREC'' AND A.SERVICE_ID = ''Z0091'' ' ")
					
					#Z0092
					primaryQueryItems = SqlHelper.GetFirst(
					""
					+ str(Parameter1.QUERY_CRITERIA_1)
					+ "  A SET NPI_COEFFICIENT = CONVERT(VARCHAR,ENTITLEMENT_COEFFICIENT) FROM SAQICO_INBOUND (NOLOCK) A JOIN PRENVL B(NOLOCK) ON A.TOOL_NPI = B.ENTITLEMENT_DISPLAY_VALUE WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND ISNULL(TOOL_NPI,'''') <> '''' AND ENTITLEMENT_ID = ''AGS_Z0092_VAL_NPIREC'' AND A.SERVICE_ID = ''Z0092'' ' ")
					
					#Z0004
					primaryQueryItems = SqlHelper.GetFirst(
					""
					+ str(Parameter1.QUERY_CRITERIA_1)
					+ "  A SET NPI_COEFFICIENT = CONVERT(VARCHAR,ENTITLEMENT_COEFFICIENT) FROM SAQICO_INBOUND (NOLOCK) A JOIN PRENVL B(NOLOCK) ON A.TOOL_NPI = B.ENTITLEMENT_DISPLAY_VALUE WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND ISNULL(TOOL_NPI,'''') <> '''' AND ENTITLEMENT_ID = ''AGS_Z0004_VAL_NPIREC'' AND A.SERVICE_ID = ''Z0004'' ' ")
					
					#Z0099
					primaryQueryItems = SqlHelper.GetFirst(
					""
					+ str(Parameter1.QUERY_CRITERIA_1)
					+ "  A SET NPI_COEFFICIENT = CONVERT(VARCHAR,ENTITLEMENT_COEFFICIENT) FROM SAQICO_INBOUND (NOLOCK) A JOIN PRENVL B(NOLOCK) ON A.TOOL_NPI = B.ENTITLEMENT_DISPLAY_VALUE WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND ISNULL(TOOL_NPI,'''') <> '''' AND ENTITLEMENT_ID = ''AGS_Z0099_VAL_NPIREC'' AND A.SERVICE_ID = ''Z0099'' ' ")

					#Service Complexity									
					primaryQueryItems = SqlHelper.GetFirst(
						""
						+ str(Parameter1.QUERY_CRITERIA_1)
						+ " A SET GREENBOOK = B.GREENBOOK FROM SAQICO_INBOUND (NOLOCK) A JOIN SAQICO (NOLOCK) B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.REVISION_ID = B.QTEREV_ID WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' '")
						
					primaryQueryItems = SqlHelper.GetFirst(
											""
											+ str(Parameter1.QUERY_CRITERIA_1)
											+ " A SET TOOL_SERVICE_COMPLEXITY = B.SERVICE_COMPLEXITY FROM SAQICO_INBOUND A(NOLOCK) JOIN (SELECT A.QUOTE_ID,A.SERVICE_ID,A.EQUIPMENT_ID,A.REVISION_ID AS QTEREV_ID,CASE WHEN A.SERVICE_COMPLEXITY = ''DIFFICULT'' THEN ''Difficult'' ELSE A.SERVICE_COMPLEXITY END AS SERVICE_COMPLEXITY FROM SAQICO_INBOUND (NOLOCK) A JOIN SAQICA (NOLOCK) B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.REVISION_ID = B.QTEREV_ID AND A.ASSEMBLY_ID = B.ASSEMBLY_ID WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND A.SERVICE_COMPLEXITY = ''Difficult'' AND B.EQUIPMENTTYPE_ID=''MAINFRAME'' AND A.GREENBOOK IN (''CMP'',''PDC'',''MPS'',''IMPLANT'') )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.REVISION_ID = B.QTEREV_ID   '")

					primaryQueryItems = SqlHelper.GetFirst(
																""
																+ str(Parameter1.QUERY_CRITERIA_1)
																+ " A SET TOOL_SERVICE_COMPLEXITY = ''Difficult'' FROM SAQICO_INBOUND A(NOLOCK) JOIN (SELECT A.QUOTE_ID,A.SERVICE_ID,A.EQUIPMENT_ID,A.REVISION_ID AS QTEREV_ID,COUNT(*) AS SERVICE_COMPLEXITY FROM SAQICO_INBOUND (NOLOCK) A WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND A.SERVICE_COMPLEXITY = ''Difficult'' AND A.GREENBOOK NOT IN (''CMP'',''PDC'',''MPS'',''IMPLANT'') GROUP BY A.QUOTE_ID,A.SERVICE_ID,A.EQUIPMENT_ID,A.REVISION_ID )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.REVISION_ID = B.QTEREV_ID WHERE B.SERVICE_COMPLEXITY >= 2  '")

					primaryQueryItems = SqlHelper.GetFirst( ""+ str(Parameter1.QUERY_CRITERIA_1)+ " A SET TOOL_SERVICE_COMPLEXITY = CASE WHEN WA>=75 THEN ''Difficult'' WHEN WA>=25 AND WA<75 THEN ''MEDIUM'' WHEN WA<25 THEN ''EASY'' ELSE NULL END  FROM SAQICO_INBOUND A(NOLOCK) JOIN (SELECT QUOTE_ID,SERVICE_ID,EQUIPMENT_ID,QTEREV_ID,SCORE/SERVICE_COMPLEXITY AS WA FROM (SELECT A.QUOTE_ID,A.SERVICE_ID,A.EQUIPMENT_ID,A.REVISION_ID AS QTEREV_ID,COUNT(CASE WHEN ISNULL(SERVICE_COMPLEXITY,'''')='''' THEN NULL ELSE 1 END) AS SERVICE_COMPLEXITY,SUM(CASE WHEN ISNULL(SERVICE_COMPLEXITY,'''')=''DIFFICULT'' THEN 100 WHEN ISNULL(SERVICE_COMPLEXITY,'''')=''MEDIUM'' THEN 50 ELSE 0 END) AS SCORE FROM SAQICO_INBOUND (NOLOCK) A JOIN SAQICO (NOLOCK) B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.REVISION_ID = B.QTEREV_ID  WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND B.GREENBOOK NOT IN (''CMP'',''PDC'',''MPS'',''IMPLANT'') GROUP BY A.QUOTE_ID,A.SERVICE_ID,A.EQUIPMENT_ID,A.REVISION_ID)B WHERE EQUIPMENT_ID IN (SELECT DISTINCT EQUIPMENT_ID FROM (SELECT A.QUOTE_ID,A.SERVICE_ID,A.EQUIPMENT_ID,A.REVISION_ID AS QTEREV_ID,COUNT(CASE WHEN ISNULL(SERVICE_COMPLEXITY,'''')=''DIFFICULT'' THEN 1 ELSE NULL END) AS SERV_COMP  FROM SAQICO_INBOUND (NOLOCK) A JOIN SAQICO (NOLOCK)B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.REVISION_ID = B.QTEREV_ID  WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND ISNULL(TOOL_SERVICE_COMPLEXITY,'''')='''' AND B.GREENBOOK NOT IN (''CMP'',''PDC'',''MPS'',''IMPLANT'') GROUP BY A.QUOTE_ID,A.SERVICE_ID,A.EQUIPMENT_ID,A.REVISION_ID ) A WHERE SERV_COMP<2) AND ISNULL(SERVICE_COMPLEXITY,0)>0 )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.REVISION_ID = B.QTEREV_ID    '")
					
					#Z0091
					primaryQueryItems = SqlHelper.GetFirst(
																	""
																	+ str(Parameter1.QUERY_CRITERIA_1)
																	+ "  A SET SERVICECOMPLEXITY_COEFFICIENT = CONVERT(VARCHAR,ENTITLEMENT_COEFFICIENT) FROM SAQICO_INBOUND (NOLOCK) A JOIN PRENVL B(NOLOCK) ON A.TOOL_SERVICE_COMPLEXITY = B.ENTITLEMENT_DISPLAY_VALUE WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND ISNULL(TOOL_SERVICE_COMPLEXITY,'''') <> '''' AND ENTITLEMENT_ID = ''AGS_Z0091_VAL_SCCCDF'' AND A.SERVICE_ID = ''Z0091'' ' ")
					
					#Z0092					
					primaryQueryItems = SqlHelper.GetFirst(
										""
										+ str(Parameter1.QUERY_CRITERIA_1)
										+ "  A SET SERVICECOMPLEXITY_COEFFICIENT = CONVERT(VARCHAR,ENTITLEMENT_COEFFICIENT) FROM SAQICO_INBOUND (NOLOCK) A JOIN PRENVL B(NOLOCK) ON A.TOOL_SERVICE_COMPLEXITY = B.ENTITLEMENT_DISPLAY_VALUE WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND ISNULL(TOOL_SERVICE_COMPLEXITY,'''') <> '''' AND ENTITLEMENT_ID = ''AGS_Z0092_VAL_SCCCDF'' AND A.SERVICE_ID = ''Z0092'' ' ")
					
					#Z0004					
					primaryQueryItems = SqlHelper.GetFirst(
										""
										+ str(Parameter1.QUERY_CRITERIA_1)
										+ "  A SET SERVICECOMPLEXITY_COEFFICIENT = CONVERT(VARCHAR,ENTITLEMENT_COEFFICIENT) FROM SAQICO_INBOUND (NOLOCK) A JOIN PRENVL B(NOLOCK) ON A.TOOL_SERVICE_COMPLEXITY = B.ENTITLEMENT_DISPLAY_VALUE WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND ISNULL(TOOL_SERVICE_COMPLEXITY,'''') <> '''' AND ENTITLEMENT_ID = ''AGS_Z0004_VAL_SCCCDF'' AND A.SERVICE_ID = ''Z0004'' ' ")
					
					#Z0099					
					primaryQueryItems = SqlHelper.GetFirst(
										""
										+ str(Parameter1.QUERY_CRITERIA_1)
										+ "  A SET SERVICECOMPLEXITY_COEFFICIENT = CONVERT(VARCHAR,ENTITLEMENT_COEFFICIENT) FROM SAQICO_INBOUND (NOLOCK) A JOIN PRENVL B(NOLOCK) ON A.TOOL_SERVICE_COMPLEXITY = B.ENTITLEMENT_DISPLAY_VALUE WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND ISNULL(TOOL_SERVICE_COMPLEXITY,'''') <> '''' AND ENTITLEMENT_ID = ''AGS_Z0099_VAL_SCCCDF'' AND A.SERVICE_ID = ''Z0099'' ' ")
						
					
					start12 = 1
					end12 = 500

					Check_flag12 = 1
					while Check_flag12 == 1:

						table12 = SqlHelper.GetFirst(
									"SELECT DISTINCT equipment_id FROM (SELECT DISTINCT equipment_id, ROW_NUMBER()OVER(ORDER BY equipment_id) AS SNO FROM (SELECT DISTINCT equipment_id FROM SAQICO_INBOUND (NOLOCK) WHERE ISNULL(PROCESS_STATUS,'')='INPROGRESS' AND TIMESTAMP = "+str(timestamp_sessionid)+" )A ) A WHERE SNO>= "+str(start12)+" AND SNO<="+str(end12)+""
								)
								
						CRMTMP12 = SqlHelper.GetFirst("sp_executesql @T=N'IF NOT EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(CRMTMP)+"'' ) BEGIN CREATE TABLE "+str(CRMTMP)+" (EQUIPMENT_IDD VARCHAR(100)) END  ' ")
						
						table_ins = SqlHelper.GetFirst(
							"sp_executesql @T=N'INSERT "+str(CRMTMP)+" SELECT DISTINCT equipment_id FROM (SELECT DISTINCT equipment_id, ROW_NUMBER()OVER(ORDER BY equipment_id) AS SNO FROM (SELECT DISTINCT equipment_id FROM SAQICO_INBOUND (NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' )A ) A WHERE SNO>= "+str(start12)+" AND SNO<="+str(end12)+"  '")
						
						start12 = start12 + 500
						end12 = end12 + 500

						if str(table12) != "None":
						
							#SAQSCE
							"""primaryQueryItems = SqlHelper.GetFirst("sp_executesql @t=N'UPDATE A SET ENTITLEMENT_XML = replace(replace(entitlement_xml,''	'',''''),''\n'','''')  FROM SAQSCE(NOLOCK) A JOIN (SELECT DISTINCT QUOTE_ID ,SERVICE_ID,EQUIPMENT_ID,REVISION_ID FROM SAQICO_INBOUND B(NOLOCK) JOIN "+str(CRMTMP)+" C ON B.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' ) B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID  = B.EQUIPMENT_ID AND A.QTEREV_ID = B.REVISION_ID  WHERE A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' '")"""
							
							#SAQIEN
							primaryQueryItems = SqlHelper.GetFirst("sp_executesql @t=N'UPDATE A SET ENTITLEMENT_XML = replace(replace(entitlement_xml,''	'',''''),''\n'','''')  FROM SAQIEN(NOLOCK) A JOIN "+str(CRMTMP)+" C ON A.EQUIPMENT_ID = C.EQUIPMENT_IDD  WHERE A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' '")
							
							#SAQSCE NPI
							#Z0091
							"""primaryQueryItems = SqlHelper.GetFirst("sp_executesql @t=N'UPDATE A SET ENTITLEMENT_XML = REPLACE(entitlement_xml ,  substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0091_VAL_NPIREC</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml),charindex(''</ENTITLEMENT_VALUE_CODE>''  ,substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0091_VAL_NPIREC</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml) , 1000 ))-1  ), ''<ENTITLEMENT_ID>AGS_Z0091_VAL_NPIREC</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>''+TOOL_NPI ) FROM SAQSCE(NOLOCK) A JOIN (SELECT DISTINCT QUOTE_ID ,SERVICE_ID,EQUIPMENT_ID,REVISION_ID,TOOL_NPI FROM SAQICO_INBOUND B(NOLOCK) JOIN "+str(CRMTMP)+" C ON B.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND SERVICE_ID = ''Z0091'' ) B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID  = B.EQUIPMENT_ID AND A.QTEREV_ID = B.REVISION_ID  WHERE A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND ISNULL(TOOL_NPI,'''')<>'''' '")
							
							#Z0092
							primaryQueryItems = SqlHelper.GetFirst("sp_executesql @t=N'UPDATE A SET ENTITLEMENT_XML = REPLACE(entitlement_xml ,  substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0092_VAL_NPIREC</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml),charindex(''</ENTITLEMENT_VALUE_CODE>''  ,substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0092_VAL_NPIREC</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml) , 1000 ))-1  ), ''<ENTITLEMENT_ID>AGS_Z0092_VAL_NPIREC</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>''+TOOL_NPI ) FROM SAQSCE(NOLOCK) A JOIN (SELECT DISTINCT QUOTE_ID ,SERVICE_ID,EQUIPMENT_ID,REVISION_ID,TOOL_NPI FROM SAQICO_INBOUND B(NOLOCK) JOIN "+str(CRMTMP)+" C ON B.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND SERVICE_ID = ''Z0092'' ) B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID  = B.EQUIPMENT_ID AND A.QTEREV_ID = B.REVISION_ID  WHERE A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND ISNULL(TOOL_NPI,'''')<>'''' '")"""
							
							#SAQIEN NPI
							#Z0091
							primaryQueryItems = SqlHelper.GetFirst("sp_executesql @t=N'UPDATE A SET ENTITLEMENT_XML = REPLACE(entitlement_xml ,  substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0091_VAL_NPIREC</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml),charindex(''</ENTITLEMENT_VALUE_CODE>''  ,substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0091_VAL_NPIREC</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml) , 1000 ))-1  ), ''<ENTITLEMENT_ID>AGS_Z0091_VAL_NPIREC</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>''+TOOL_NPI ) FROM SAQIEN(NOLOCK) A JOIN (SELECT DISTINCT QUOTE_ID ,SERVICE_ID,EQUIPMENT_ID,REVISION_ID,TOOL_NPI FROM SAQICO_INBOUND B(NOLOCK) JOIN "+str(CRMTMP)+" C ON B.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND SERVICE_ID = ''Z0091'' ) B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID  = B.EQUIPMENT_ID AND A.QTEREV_ID = B.REVISION_ID  WHERE A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND ISNULL(TOOL_NPI,'''')<>'''' '")
							
							#Z0092
							primaryQueryItems = SqlHelper.GetFirst("sp_executesql @t=N'UPDATE A SET ENTITLEMENT_XML = REPLACE(entitlement_xml ,  substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0092_VAL_NPIREC</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml),charindex(''</ENTITLEMENT_VALUE_CODE>''  ,substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0092_VAL_NPIREC</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml) , 1000 ))-1  ), ''<ENTITLEMENT_ID>AGS_Z0092_VAL_NPIREC</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>''+TOOL_NPI ) FROM SAQIEN(NOLOCK) A JOIN (SELECT DISTINCT QUOTE_ID ,SERVICE_ID,EQUIPMENT_ID,REVISION_ID,TOOL_NPI FROM SAQICO_INBOUND B(NOLOCK) JOIN "+str(CRMTMP)+" C ON B.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND SERVICE_ID = ''Z0092'' ) B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID  = B.EQUIPMENT_ID AND A.QTEREV_ID = B.REVISION_ID  WHERE A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND ISNULL(TOOL_NPI,'''')<>'''' '")
							
							#Z0004
							primaryQueryItems = SqlHelper.GetFirst("sp_executesql @t=N'UPDATE A SET ENTITLEMENT_XML = REPLACE(entitlement_xml ,  substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0004_VAL_NPIREC</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml),charindex(''</ENTITLEMENT_VALUE_CODE>''  ,substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0004_VAL_NPIREC</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml) , 1000 ))-1  ), ''<ENTITLEMENT_ID>AGS_Z0004_VAL_NPIREC</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>''+TOOL_NPI ) FROM SAQIEN(NOLOCK) A JOIN (SELECT DISTINCT QUOTE_ID ,SERVICE_ID,EQUIPMENT_ID,REVISION_ID,TOOL_NPI FROM SAQICO_INBOUND B(NOLOCK) JOIN "+str(CRMTMP)+" C ON B.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND SERVICE_ID = ''Z0004'' ) B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID  = B.EQUIPMENT_ID AND A.QTEREV_ID = B.REVISION_ID  WHERE A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND ISNULL(TOOL_NPI,'''')<>'''' '")
							
							#Z0099
							primaryQueryItems = SqlHelper.GetFirst("sp_executesql @t=N'UPDATE A SET ENTITLEMENT_XML = REPLACE(entitlement_xml ,  substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0099_VAL_NPIREC</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml),charindex(''</ENTITLEMENT_VALUE_CODE>''  ,substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0099_VAL_NPIREC</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml) , 1000 ))-1  ), ''<ENTITLEMENT_ID>AGS_Z0099_VAL_NPIREC</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>''+TOOL_NPI ) FROM SAQIEN(NOLOCK) A JOIN (SELECT DISTINCT QUOTE_ID ,SERVICE_ID,EQUIPMENT_ID,REVISION_ID,TOOL_NPI FROM SAQICO_INBOUND B(NOLOCK) JOIN "+str(CRMTMP)+" C ON B.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND SERVICE_ID = ''Z0099'' ) B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID  = B.EQUIPMENT_ID AND A.QTEREV_ID = B.REVISION_ID  WHERE A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND ISNULL(TOOL_NPI,'''')<>'''' '")
		
							#SAQSCE NPI Coefficent
							#Z0091
							"""primaryQueryItems = SqlHelper.GetFirst("sp_executesql @t=N'UPDATE A SET ENTITLEMENT_XML = REPLACE(entitlement_xml ,  substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0091_VAL_NPICOF</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml),charindex(''</ENTITLEMENT_VALUE_CODE>''  ,substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0091_VAL_NPICOF</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml) , 1000 ))-1  ), ''<ENTITLEMENT_ID>AGS_Z0091_VAL_NPICOF</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>''+NPI_COEFFICIENT ) FROM SAQSCE(NOLOCK) A JOIN (SELECT DISTINCT QUOTE_ID ,SERVICE_ID,EQUIPMENT_ID,REVISION_ID,NPI_COEFFICIENT FROM SAQICO_INBOUND B(NOLOCK) JOIN "+str(CRMTMP)+" C ON B.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND SERVICE_ID = ''Z0091'' )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID  = B.EQUIPMENT_ID AND A.QTEREV_ID = B.REVISION_ID  WHERE A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"''   '")
							
							#Z0092
							primaryQueryItems = SqlHelper.GetFirst("sp_executesql @t=N'UPDATE A SET ENTITLEMENT_XML = REPLACE(entitlement_xml ,  substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0092_VAL_NPICOF</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml),charindex(''</ENTITLEMENT_VALUE_CODE>''  ,substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0092_VAL_NPICOF</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml) , 1000 ))-1  ), ''<ENTITLEMENT_ID>AGS_Z0092_VAL_NPICOF</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>''+NPI_COEFFICIENT ) FROM SAQSCE(NOLOCK) A JOIN (SELECT DISTINCT QUOTE_ID ,SERVICE_ID,EQUIPMENT_ID,REVISION_ID,NPI_COEFFICIENT FROM SAQICO_INBOUND B(NOLOCK) JOIN "+str(CRMTMP)+" C ON B.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND SERVICE_ID = ''Z0092'' )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID  = B.EQUIPMENT_ID AND A.QTEREV_ID = B.REVISION_ID  WHERE A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"''  '")"""
							
							#SAQIEN NPI Coefficent
							#Z0091
							primaryQueryItems = SqlHelper.GetFirst("sp_executesql @t=N'UPDATE A SET ENTITLEMENT_XML = REPLACE(entitlement_xml ,  substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0091_VAL_NPICOF</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml),charindex(''</ENTITLEMENT_VALUE_CODE>''  ,substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0091_VAL_NPICOF</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml) , 1000 ))-1  ), ''<ENTITLEMENT_ID>AGS_Z0091_VAL_NPICOF</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>''+CONVERT(VARCHAR,NPI_COEFFICIENT) ) FROM SAQIEN(NOLOCK) A JOIN (SELECT DISTINCT QUOTE_ID ,SERVICE_ID,EQUIPMENT_ID,REVISION_ID,NPI_COEFFICIENT FROM SAQICO_INBOUND B(NOLOCK) JOIN "+str(CRMTMP)+" C ON B.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND SERVICE_ID = ''Z0091'')B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID  = B.EQUIPMENT_ID AND A.QTEREV_ID = B.REVISION_ID  WHERE A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"''   '")
							
							#Z0092 
							primaryQueryItems = SqlHelper.GetFirst("sp_executesql @t=N'UPDATE A SET ENTITLEMENT_XML = REPLACE(entitlement_xml ,  substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0092_VAL_NPICOF</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml),charindex(''</ENTITLEMENT_VALUE_CODE>''  ,substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0092_VAL_NPICOF</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml) , 1000 ))-1  ), ''<ENTITLEMENT_ID>AGS_Z0092_VAL_NPICOF</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>''+CONVERT(VARCHAR,NPI_COEFFICIENT) ) FROM SAQIEN(NOLOCK) A JOIN (SELECT DISTINCT QUOTE_ID ,SERVICE_ID,EQUIPMENT_ID,REVISION_ID,NPI_COEFFICIENT FROM SAQICO_INBOUND B(NOLOCK) JOIN "+str(CRMTMP)+" C ON B.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND SERVICE_ID = ''Z0092'')B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID  = B.EQUIPMENT_ID AND A.QTEREV_ID = B.REVISION_ID  WHERE A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"''   '")
							
							#Z0004
							primaryQueryItems = SqlHelper.GetFirst("sp_executesql @t=N'UPDATE A SET ENTITLEMENT_XML = REPLACE(entitlement_xml ,  substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0004_VAL_NPICOF</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml),charindex(''</ENTITLEMENT_VALUE_CODE>''  ,substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0004_VAL_NPICOF</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml) , 1000 ))-1  ), ''<ENTITLEMENT_ID>AGS_Z0004_VAL_NPICOF</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>''+CONVERT(VARCHAR,NPI_COEFFICIENT) ) FROM SAQIEN(NOLOCK) A JOIN (SELECT DISTINCT QUOTE_ID ,SERVICE_ID,EQUIPMENT_ID,REVISION_ID,NPI_COEFFICIENT FROM SAQICO_INBOUND B(NOLOCK) JOIN "+str(CRMTMP)+" C ON B.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND SERVICE_ID = ''Z0004'')B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID  = B.EQUIPMENT_ID AND A.QTEREV_ID = B.REVISION_ID  WHERE A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"''   '")
							
							#Z0099
							primaryQueryItems = SqlHelper.GetFirst("sp_executesql @t=N'UPDATE A SET ENTITLEMENT_XML = REPLACE(entitlement_xml ,  substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0009_VAL_NPICOF</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml),charindex(''</ENTITLEMENT_VALUE_CODE>''  ,substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0009_VAL_NPICOF</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml) , 1000 ))-1  ), ''<ENTITLEMENT_ID>AGS_Z0009_VAL_NPICOF</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>''+CONVERT(VARCHAR,NPI_COEFFICIENT) ) FROM SAQIEN(NOLOCK) A JOIN (SELECT DISTINCT QUOTE_ID ,SERVICE_ID,EQUIPMENT_ID,REVISION_ID,NPI_COEFFICIENT FROM SAQICO_INBOUND B(NOLOCK) JOIN "+str(CRMTMP)+" C ON B.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND SERVICE_ID = ''Z0099'')B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID  = B.EQUIPMENT_ID AND A.QTEREV_ID = B.REVISION_ID  WHERE A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"''   '")
							
							#SAQSCE Service Complexity
							#Z0091
							"""primaryQueryItems = SqlHelper.GetFirst("sp_executesql @t=N'UPDATE A SET ENTITLEMENT_XML = REPLACE(entitlement_xml ,  substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0091_VAL_SCCCDF</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml),charindex(''</ENTITLEMENT_VALUE_CODE>''  ,substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0091_VAL_SCCCDF</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml) , 1000 ))-1  ), ''<ENTITLEMENT_ID>AGS_Z0091_VAL_SCCCDF</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>''+TOOL_SERVICE_COMPLEXITY ) FROM SAQSCE(NOLOCK) A JOIN (SELECT DISTINCT QUOTE_ID ,SERVICE_ID,EQUIPMENT_ID,REVISION_ID,TOOL_SERVICE_COMPLEXITY FROM SAQICO_INBOUND B(NOLOCK)  JOIN "+str(CRMTMP)+" C ON B.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND SERVICE_ID = ''Z0091''  )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID  = B.EQUIPMENT_ID AND A.QTEREV_ID = B.REVISION_ID  WHERE A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND ISNULL(TOOL_SERVICE_COMPLEXITY,'''')<>'''' '")
							
							#Z0092
							primaryQueryItems = SqlHelper.GetFirst("sp_executesql @t=N'UPDATE A SET ENTITLEMENT_XML = REPLACE(entitlement_xml ,  substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0092_VAL_SCCCDF</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml),charindex(''</ENTITLEMENT_VALUE_CODE>''  ,substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0092_VAL_SCCCDF</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml) , 1000 ))-1  ), ''<ENTITLEMENT_ID>AGS_Z0092_VAL_SCCCDF</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>''+TOOL_SERVICE_COMPLEXITY ) FROM SAQSCE(NOLOCK) A JOIN (SELECT DISTINCT QUOTE_ID ,SERVICE_ID,EQUIPMENT_ID,REVISION_ID,TOOL_SERVICE_COMPLEXITY FROM SAQICO_INBOUND B(NOLOCK) JOIN "+str(CRMTMP)+" C ON B.EQUIPMENT_ID = C.EQUIPMENT_IDD  WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND SERVICE_ID = ''Z0092''  )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID  = B.EQUIPMENT_ID AND A.QTEREV_ID = B.REVISION_ID  WHERE A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND ISNULL(TOOL_SERVICE_COMPLEXITY,'''')<>'''' '")"""
							
							#SAQIEN Service Complexity
							#Z0091
							primaryQueryItems = SqlHelper.GetFirst("sp_executesql @t=N'UPDATE A SET ENTITLEMENT_XML = REPLACE(entitlement_xml ,  substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0091_VAL_SCCCDF</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml),charindex(''</ENTITLEMENT_VALUE_CODE>''  ,substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0091_VAL_SCCCDF</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml) , 1000 ))-1  ), ''<ENTITLEMENT_ID>AGS_Z0091_VAL_SCCCDF</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>''+TOOL_SERVICE_COMPLEXITY ) FROM SAQIEN(NOLOCK) A JOIN (SELECT DISTINCT QUOTE_ID ,SERVICE_ID,EQUIPMENT_ID,REVISION_ID,TOOL_SERVICE_COMPLEXITY FROM SAQICO_INBOUND B(NOLOCK) JOIN "+str(CRMTMP)+" C ON B.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND SERVICE_ID = ''Z0091'' )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID  = B.EQUIPMENT_ID AND A.QTEREV_ID = B.REVISION_ID  WHERE A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND ISNULL(TOOL_SERVICE_COMPLEXITY,'''')<>'''' '")
							
							#Z0092
							primaryQueryItems = SqlHelper.GetFirst("sp_executesql @t=N'UPDATE A SET ENTITLEMENT_XML = REPLACE(entitlement_xml ,  substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0092_VAL_SCCCDF</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml),charindex(''</ENTITLEMENT_VALUE_CODE>''  ,substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0092_VAL_SCCCDF</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml) , 1000 ))-1  ), ''<ENTITLEMENT_ID>AGS_Z0092_VAL_SCCCDF</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>''+TOOL_SERVICE_COMPLEXITY ) FROM SAQIEN(NOLOCK) A JOIN (SELECT DISTINCT QUOTE_ID ,SERVICE_ID,EQUIPMENT_ID,REVISION_ID,TOOL_SERVICE_COMPLEXITY FROM SAQICO_INBOUND B(NOLOCK) JOIN "+str(CRMTMP)+" C ON B.EQUIPMENT_ID = C.EQUIPMENT_IDD  WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND SERVICE_ID = ''Z0092'' )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID  = B.EQUIPMENT_ID AND A.QTEREV_ID = B.REVISION_ID  WHERE A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND ISNULL(TOOL_SERVICE_COMPLEXITY,'''')<>'''' '")
							
							#Z0004
							primaryQueryItems = SqlHelper.GetFirst("sp_executesql @t=N'UPDATE A SET ENTITLEMENT_XML = REPLACE(entitlement_xml ,  substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0004_VAL_SCCCDF</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml),charindex(''</ENTITLEMENT_VALUE_CODE>''  ,substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0004_VAL_SCCCDF</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml) , 1000 ))-1  ), ''<ENTITLEMENT_ID>AGS_Z0004_VAL_SCCCDF</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>''+TOOL_SERVICE_COMPLEXITY ) FROM SAQIEN(NOLOCK) A JOIN (SELECT DISTINCT QUOTE_ID ,SERVICE_ID,EQUIPMENT_ID,REVISION_ID,TOOL_SERVICE_COMPLEXITY FROM SAQICO_INBOUND B(NOLOCK) JOIN "+str(CRMTMP)+" C ON B.EQUIPMENT_ID = C.EQUIPMENT_IDD  WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND SERVICE_ID = ''Z0004'' )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID  = B.EQUIPMENT_ID AND A.QTEREV_ID = B.REVISION_ID  WHERE A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND ISNULL(TOOL_SERVICE_COMPLEXITY,'''')<>'''' '")
							
							#Z0099
							primaryQueryItems = SqlHelper.GetFirst("sp_executesql @t=N'UPDATE A SET ENTITLEMENT_XML = REPLACE(entitlement_xml ,  substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0099_VAL_SCCCDF</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml),charindex(''</ENTITLEMENT_VALUE_CODE>''  ,substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0099_VAL_SCCCDF</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml) , 1000 ))-1  ), ''<ENTITLEMENT_ID>AGS_Z0099_VAL_SCCCDF</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>''+TOOL_SERVICE_COMPLEXITY ) FROM SAQIEN(NOLOCK) A JOIN (SELECT DISTINCT QUOTE_ID ,SERVICE_ID,EQUIPMENT_ID,REVISION_ID,TOOL_SERVICE_COMPLEXITY FROM SAQICO_INBOUND B(NOLOCK) JOIN "+str(CRMTMP)+" C ON B.EQUIPMENT_ID = C.EQUIPMENT_IDD  WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND SERVICE_ID = ''Z0099'' )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID  = B.EQUIPMENT_ID AND A.QTEREV_ID = B.REVISION_ID  WHERE A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND ISNULL(TOOL_SERVICE_COMPLEXITY,'''')<>'''' '")

							#SAQSCE Service Complexity Coefficent
							#Z0091
							"""primaryQueryItems = SqlHelper.GetFirst("sp_executesql @t=N'UPDATE A SET ENTITLEMENT_XML = REPLACE(entitlement_xml ,  substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0091_VAL_SCCCCO</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml),charindex(''</ENTITLEMENT_VALUE_CODE>''  ,substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0091_VAL_SCCCCO</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml) , 1000 ))-1  ), ''<ENTITLEMENT_ID>AGS_Z0091_VAL_SCCCCO</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>''+SERVICECOMPLEXITY_COEFFICIENT ) FROM SAQSCE(NOLOCK) A JOIN (SELECT DISTINCT QUOTE_ID ,SERVICE_ID,EQUIPMENT_ID,REVISION_ID,SERVICECOMPLEXITY_COEFFICIENT FROM SAQICO_INBOUND B(NOLOCK) JOIN "+str(CRMTMP)+" C ON B.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND SERVICE_ID=''Z0091''  )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID  = B.EQUIPMENT_ID AND A.QTEREV_ID = B.REVISION_ID  WHERE A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND ISNULL(SERVICECOMPLEXITY_COEFFICIENT,'''')<>'''' '")
							
							#Z0092
							primaryQueryItems = SqlHelper.GetFirst("sp_executesql @t=N'UPDATE A SET ENTITLEMENT_XML = REPLACE(entitlement_xml ,  substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0092_VAL_SCCCCO</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml),charindex(''</ENTITLEMENT_VALUE_CODE>''  ,substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0092_VAL_SCCCCO</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml) , 1000 ))-1  ), ''<ENTITLEMENT_ID>AGS_Z0092_VAL_SCCCCO</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>''+SERVICECOMPLEXITY_COEFFICIENT ) FROM SAQSCE(NOLOCK) A JOIN (SELECT DISTINCT QUOTE_ID ,SERVICE_ID,EQUIPMENT_ID,REVISION_ID,SERVICECOMPLEXITY_COEFFICIENT FROM SAQICO_INBOUND B(NOLOCK) JOIN "+str(CRMTMP)+" C ON B.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND SERVICE_ID=''Z0092''  )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID  = B.EQUIPMENT_ID AND A.QTEREV_ID = B.REVISION_ID  WHERE A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND ISNULL(SERVICECOMPLEXITY_COEFFICIENT,'''')<>'''' '")"""
							
							#SAQIEN Service Complexity Coefficent
							#Z0091
							primaryQueryItems = SqlHelper.GetFirst("sp_executesql @t=N'UPDATE A SET ENTITLEMENT_XML = REPLACE(entitlement_xml ,  substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0091_VAL_SCCCCO</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml),charindex(''</ENTITLEMENT_VALUE_CODE>''  ,substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0091_VAL_SCCCCO</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml) , 1000 ))-1  ), ''<ENTITLEMENT_ID>AGS_Z0091_VAL_SCCCCO</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>''+SERVICECOMPLEXITY_COEFFICIENT ) FROM SAQIEN(NOLOCK) A JOIN (SELECT DISTINCT QUOTE_ID ,SERVICE_ID,EQUIPMENT_ID,REVISION_ID,SERVICECOMPLEXITY_COEFFICIENT FROM SAQICO_INBOUND B(NOLOCK) JOIN "+str(CRMTMP)+" C ON B.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND SERVICE_ID=''Z0091''  )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID  = B.EQUIPMENT_ID AND A.QTEREV_ID = B.REVISION_ID  WHERE A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND ISNULL(SERVICECOMPLEXITY_COEFFICIENT,'''')<>'''' '")
							
							#Z0092
							primaryQueryItems = SqlHelper.GetFirst("sp_executesql @t=N'UPDATE A SET ENTITLEMENT_XML = REPLACE(entitlement_xml ,  substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0092_VAL_SCCCCO</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml),charindex(''</ENTITLEMENT_VALUE_CODE>''  ,substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0092_VAL_SCCCCO</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml) , 1000 ))-1  ), ''<ENTITLEMENT_ID>AGS_Z0092_VAL_SCCCCO</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>''+SERVICECOMPLEXITY_COEFFICIENT ) FROM SAQIEN(NOLOCK) A JOIN (SELECT DISTINCT QUOTE_ID ,SERVICE_ID,EQUIPMENT_ID,REVISION_ID,SERVICECOMPLEXITY_COEFFICIENT FROM SAQICO_INBOUND B(NOLOCK) JOIN "+str(CRMTMP)+" C ON B.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND SERVICE_ID=''Z0092'' )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID  = B.EQUIPMENT_ID AND A.QTEREV_ID = B.REVISION_ID  WHERE A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND ISNULL(SERVICECOMPLEXITY_COEFFICIENT,'''')<>'''' '")
							
							#Z0004
							primaryQueryItems = SqlHelper.GetFirst("sp_executesql @t=N'UPDATE A SET ENTITLEMENT_XML = REPLACE(entitlement_xml ,  substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0004_VAL_SCCCCO</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml),charindex(''</ENTITLEMENT_VALUE_CODE>''  ,substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0004_VAL_SCCCCO</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml) , 1000 ))-1  ), ''<ENTITLEMENT_ID>AGS_Z0004_VAL_SCCCCO</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>''+SERVICECOMPLEXITY_COEFFICIENT ) FROM SAQIEN(NOLOCK) A JOIN (SELECT DISTINCT QUOTE_ID ,SERVICE_ID,EQUIPMENT_ID,REVISION_ID,SERVICECOMPLEXITY_COEFFICIENT FROM SAQICO_INBOUND B(NOLOCK) JOIN "+str(CRMTMP)+" C ON B.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND SERVICE_ID=''Z0004'' )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID  = B.EQUIPMENT_ID AND A.QTEREV_ID = B.REVISION_ID  WHERE A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND ISNULL(SERVICECOMPLEXITY_COEFFICIENT,'''')<>'''' '")
							
							#Z0099
							primaryQueryItems = SqlHelper.GetFirst("sp_executesql @t=N'UPDATE A SET ENTITLEMENT_XML = REPLACE(entitlement_xml ,  substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0099_VAL_SCCCCO</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml),charindex(''</ENTITLEMENT_VALUE_CODE>''  ,substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0099_VAL_SCCCCO</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml) , 1000 ))-1  ), ''<ENTITLEMENT_ID>AGS_Z0099_VAL_SCCCCO</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>''+SERVICECOMPLEXITY_COEFFICIENT ) FROM SAQIEN(NOLOCK) A JOIN (SELECT DISTINCT QUOTE_ID ,SERVICE_ID,EQUIPMENT_ID,REVISION_ID,SERVICECOMPLEXITY_COEFFICIENT FROM SAQICO_INBOUND B(NOLOCK) JOIN "+str(CRMTMP)+" C ON B.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND SERVICE_ID=''Z0099'' )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID  = B.EQUIPMENT_ID AND A.QTEREV_ID = B.REVISION_ID  WHERE A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND ISNULL(SERVICECOMPLEXITY_COEFFICIENT,'''')<>'''' '")

							#Swap Kit AMAT Provided
							S3 = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET SWAP_KIT=ENTITLEMENT_DISPLAY_VALUE FROM SAQICO_INBOUND A(NOLOCK) JOIN (SELECT distinct quote_ID,equipment_id,service_id, replace(X.Y.value(''(ENTITLEMENT_DISPLAY_VALUE)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_DISPLAY_VALUE,replace(X.Y.value(''(ENTITLEMENT_NAME)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_NAME FROM (SELECT quote_ID,equipment_id,service_id,CONVERT(XML,''<QUOTE_ENTITLEMENT>''+substring(entitlement_xml,charindex (''<ENTITLEMENT_ID>AGS_Z0004_STT_SWKTAP'',entitlement_xml),charindex (''Swap Kits (Applied provided)</ENTITLEMENT_NAME>'',entitlement_xml)-charindex (''<ENTITLEMENT_ID>AGS_Z0004_STT_SWKTAP'',entitlement_xml)+len(''Swap Kits (Applied provided)</ENTITLEMENT_NAME>''))+''</QUOTE_ENTITLEMENT>'') as entitlement_xml FROM SAQSCE (nolock)a JOIN "+str(CRMTMP)+" C ON a.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND SERVICE_ID = ''Z0004'') e OUTER APPLY e.ENTITLEMENT_XML.nodes(''QUOTE_ENTITLEMENT'') as X(Y) )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID  WHERE B.ENTITLEMENT_NAME=''Swap Kits (Applied provided)''  '")
							
							S3 = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET SWAP_KIT=ENTITLEMENT_DISPLAY_VALUE FROM SAQICO_INBOUND A(NOLOCK) JOIN (SELECT distinct quote_ID,equipment_id,service_id, replace(X.Y.value(''(ENTITLEMENT_DISPLAY_VALUE)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_DISPLAY_VALUE,replace(X.Y.value(''(ENTITLEMENT_NAME)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_NAME FROM (SELECT quote_ID,equipment_id,service_id,CONVERT(XML,''<QUOTE_ENTITLEMENT>''+substring(entitlement_xml,charindex (''<ENTITLEMENT_ID>AGS_Z0091_STT_SWKTAP'',entitlement_xml),charindex (''Swap Kits (Applied provided)</ENTITLEMENT_NAME>'',entitlement_xml)-charindex (''<ENTITLEMENT_ID>AGS_Z0091_STT_SWKTAP'',entitlement_xml)+len(''Swap Kits (Applied provided)</ENTITLEMENT_NAME>''))+''</QUOTE_ENTITLEMENT>'') as entitlement_xml FROM SAQSCE (nolock)a JOIN "+str(CRMTMP)+" C ON A.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND SERVICE_ID =''Z0091'') e OUTER APPLY e.ENTITLEMENT_XML.nodes(''QUOTE_ENTITLEMENT'') as X(Y) )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID  WHERE B.ENTITLEMENT_NAME=''Swap Kits (Applied provided)''  '")
							
							S3 = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET SWAP_KIT=ENTITLEMENT_DISPLAY_VALUE FROM SAQICO_INBOUND A(NOLOCK) JOIN (SELECT distinct quote_ID,equipment_id,service_id, replace(X.Y.value(''(ENTITLEMENT_DISPLAY_VALUE)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_DISPLAY_VALUE,replace(X.Y.value(''(ENTITLEMENT_NAME)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_NAME FROM (SELECT quote_ID,equipment_id,service_id,CONVERT(XML,''<QUOTE_ENTITLEMENT>''+substring(entitlement_xml,charindex (''<ENTITLEMENT_ID>AGS_Z0035_STT_SWKTAP'',entitlement_xml),charindex (''Swap Kits (Applied provided)</ENTITLEMENT_NAME>'',entitlement_xml)-charindex (''<ENTITLEMENT_ID>AGS_Z0035_STT_SWKTAP'',entitlement_xml)+len(''Swap Kits (Applied provided)</ENTITLEMENT_NAME>''))+''</QUOTE_ENTITLEMENT>'') as entitlement_xml FROM SAQSCE (nolock)a JOIN "+str(CRMTMP)+" C ON A.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND SERVICE_ID =''Z0035'') e OUTER APPLY e.ENTITLEMENT_XML.nodes(''QUOTE_ENTITLEMENT'') as X(Y) )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID  WHERE B.ENTITLEMENT_NAME=''Swap Kits (Applied provided)''  '")
							
							"""#Subfab like SS
							S3 = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET SUBFAB_SS=ENTITLEMENT_DISPLAY_VALUE FROM SAQICO_INBOUND A(NOLOCK) JOIN (SELECT distinct quote_ID,equipment_id,service_id, replace(X.Y.value(''(ENTITLEMENT_DISPLAY_VALUE)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_DISPLAY_VALUE,replace(X.Y.value(''(ENTITLEMENT_NAME)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_NAME FROM (SELECT quote_ID,equipment_id,service_id,CONVERT(XML,''<QUOTE_ENTITLEMENT>''+substring(entitlement_xml,charindex (''<ENTITLEMENT_ID>AGS_Z0004_KPI_PRPFGT'',entitlement_xml),charindex (''Primary KPI. Perf Guarantee</ENTITLEMENT_NAME>'',entitlement_xml)-charindex (''<ENTITLEMENT_ID>AGS_Z0004_KPI_PRPFGT'',entitlement_xml)+len(''Primary KPI. Perf Guarantee</ENTITLEMENT_NAME>''))+''</QUOTE_ENTITLEMENT>'') as entitlement_xml FROM SAQSCE (nolock)a JOIN "+str(CRMTMP)+" C ON B.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND SERVICE_ID =''Z0004'') e OUTER APPLY e.ENTITLEMENT_XML.nodes(''QUOTE_ENTITLEMENT'') as X(Y) )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID  WHERE B.ENTITLEMENT_NAME=''Primary KPI. Perf Guarantee''  '")"""
							
							#Capital Avoidance					
							primaryQueryItems = SqlHelper.GetFirst(
													""
													+ str(Parameter1.QUERY_CRITERIA_1)
													+ " A SET TOOL_CAPITAL_AVOIDANCE =  CASE WHEN WA > 30 THEN ''HIGH'' WHEN WA >15 AND WA<=30 THEN ''MEDIUM'' WHEN WA<=15 AND WA>0 THEN ''LOW'' ELSE ''NO'' END FROM SAQICO_INBOUND A(NOLOCK) JOIN (SELECT QUOTE_ID,SERVICE_ID,EQUIPMENT_ID,QTEREV_ID,((B.SEEDSTOCK_COST/CASE WHEN TOTAL_COST_WISEEDSTOCK<=0 THEN 1 ELSE TOTAL_COST_WISEEDSTOCK END))*100 AS WA FROM (SELECT A.QUOTE_ID,A.SERVICE_ID,A.EQUIPMENT_ID,A.REVISION_ID AS QTEREV_ID,SUM(CONVERT(FLOAT,A.SEEDSTOCK_COST)) AS SEEDSTOCK_COST,SUM(CONVERT(FLOAT,TOTAL_COST_WISEEDSTOCK)) AS TOTAL_COST_WISEEDSTOCK FROM SAQICO_INBOUND (NOLOCK) A JOIN "+str(CRMTMP)+" C ON A.EQUIPMENT_ID = C.EQUIPMENT_IDD JOIN SAQICO (NOLOCK) B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.REVISION_ID = B.QTEREV_ID  WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND SWAP_KIT=''INCLUDED'' AND A.SERVICE_ID IN (''Z0004'',''Z0091'',''Z0099'',''Z0035'',''Z0092'' ) GROUP BY A.QUOTE_ID,A.SERVICE_ID,A.EQUIPMENT_ID,A.REVISION_ID)B )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.REVISION_ID = B.QTEREV_ID    '")
							
							primaryQueryItems = SqlHelper.GetFirst(
													""
													+ str(Parameter1.QUERY_CRITERIA_1)
													+ " A SET TOOL_CAPITAL_AVOIDANCE =  ''NO'' FROM SAQICO_INBOUND A(NOLOCK) JOIN (SELECT QUOTE_ID,SERVICE_ID,EQUIPMENT_ID,QTEREV_ID,((B.SEEDSTOCK_COST/CASE WHEN TOTAL_COST_WISEEDSTOCK<=0 THEN 1 ELSE TOTAL_COST_WISEEDSTOCK END))*100 AS WA FROM (SELECT A.QUOTE_ID,A.SERVICE_ID,A.EQUIPMENT_ID,A.REVISION_ID AS QTEREV_ID,SUM(CONVERT(FLOAT,A.SEEDSTOCK_COST)) AS SEEDSTOCK_COST,SUM(CONVERT(FLOAT,TOTAL_COST_WISEEDSTOCK)) AS TOTAL_COST_WISEEDSTOCK FROM SAQICO_INBOUND (NOLOCK) A JOIN "+str(CRMTMP)+" C ON A.EQUIPMENT_ID = C.EQUIPMENT_IDD JOIN SAQICO (NOLOCK) B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.REVISION_ID = B.QTEREV_ID  WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND SWAP_KIT=''EXCLUDED'' AND A.SERVICE_ID IN (''Z0004'',''Z0091'',''Z0099'',''Z0035'',''Z0092'' ) GROUP BY A.QUOTE_ID,A.SERVICE_ID,A.EQUIPMENT_ID,A.REVISION_ID)B )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.REVISION_ID = B.QTEREV_ID    '")
							#Z0091
							primaryQueryItems = SqlHelper.GetFirst(
												""
												+ str(Parameter1.QUERY_CRITERIA_1)
												+ "  SAQICO_INBOUND SET CAPITALAVOIDANCE_COEFFICIENT = CONVERT(VARCHAR,ENTITLEMENT_COEFFICIENT) FROM SAQICO_INBOUND (NOLOCK) A JOIN "+str(CRMTMP)+" C ON A.EQUIPMENT_ID = C.EQUIPMENT_IDD JOIN PRENVL B(NOLOCK) ON A.TOOL_CAPITAL_AVOIDANCE = B.ENTITLEMENT_DISPLAY_VALUE WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND ISNULL(TOOL_CAPITAL_AVOIDANCE,'''') <> '''' AND ENTITLEMENT_ID = ''AGS_Z0091_VAL_CAPAVD'' ' ")
							
							#Z0092
							primaryQueryItems = SqlHelper.GetFirst(
												""
												+ str(Parameter1.QUERY_CRITERIA_1)
												+ "  SAQICO_INBOUND SET CAPITALAVOIDANCE_COEFFICIENT = CONVERT(VARCHAR,ENTITLEMENT_COEFFICIENT) FROM SAQICO_INBOUND (NOLOCK) A JOIN "+str(CRMTMP)+" C ON A.EQUIPMENT_ID = C.EQUIPMENT_IDD JOIN PRENVL B(NOLOCK) ON A.TOOL_CAPITAL_AVOIDANCE = B.ENTITLEMENT_DISPLAY_VALUE WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND ISNULL(TOOL_CAPITAL_AVOIDANCE,'''') <> '''' AND ENTITLEMENT_ID = ''AGS_Z0092_VAL_CAPAVD'' ' ")
							
							#Z0004
							primaryQueryItems = SqlHelper.GetFirst(
												""
												+ str(Parameter1.QUERY_CRITERIA_1)
												+ "  SAQICO_INBOUND SET CAPITALAVOIDANCE_COEFFICIENT = CONVERT(VARCHAR,ENTITLEMENT_COEFFICIENT) FROM SAQICO_INBOUND (NOLOCK) A JOIN "+str(CRMTMP)+" C ON A.EQUIPMENT_ID = C.EQUIPMENT_IDD JOIN PRENVL B(NOLOCK) ON A.TOOL_CAPITAL_AVOIDANCE = B.ENTITLEMENT_DISPLAY_VALUE WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND ISNULL(TOOL_CAPITAL_AVOIDANCE,'''') <> '''' AND ENTITLEMENT_ID = ''AGS_Z0004_VAL_CAPAVD'' ' ")
							
							#Z0099
							primaryQueryItems = SqlHelper.GetFirst(
												""
												+ str(Parameter1.QUERY_CRITERIA_1)
												+ "  SAQICO_INBOUND SET CAPITALAVOIDANCE_COEFFICIENT = CONVERT(VARCHAR,ENTITLEMENT_COEFFICIENT) FROM SAQICO_INBOUND (NOLOCK) A JOIN "+str(CRMTMP)+" C ON A.EQUIPMENT_ID = C.EQUIPMENT_IDD JOIN PRENVL B(NOLOCK) ON A.TOOL_CAPITAL_AVOIDANCE = B.ENTITLEMENT_DISPLAY_VALUE WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND ISNULL(TOOL_CAPITAL_AVOIDANCE,'''') <> '''' AND ENTITLEMENT_ID = ''AGS_Z0099_VAL_CAPAVD'' ' ")
							
							#SAQSCE Captial Avoidance
							#Z0091
							"""primaryQueryItems = SqlHelper.GetFirst("sp_executesql @t=N'UPDATE A SET ENTITLEMENT_XML = REPLACE(entitlement_xml ,  substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0091_VAL_CAPAVD</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml),charindex(''</ENTITLEMENT_VALUE_CODE>''  ,substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0091_VAL_CAPAVD</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml) , 1000 ))-1  ), ''<ENTITLEMENT_ID>AGS_Z0091_VAL_CAPAVD</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>''+TOOL_CAPITAL_AVOIDANCE ) FROM SAQSCE(NOLOCK) A JOIN (SELECT DISTINCT QUOTE_ID ,SERVICE_ID,EQUIPMENT_ID,REVISION_ID,TOOL_CAPITAL_AVOIDANCE FROM SAQICO_INBOUND B(NOLOCK) JOIN "+str(CRMTMP)+" C ON B.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND B.SERVICE_ID = ''Z0091'' ) B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID  = B.EQUIPMENT_ID AND A.QTEREV_ID = B.REVISION_ID  WHERE A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND ISNULL(TOOL_CAPITAL_AVOIDANCE,'''')<>'''' '")
							
							#Z0092
							primaryQueryItems = SqlHelper.GetFirst("sp_executesql @t=N'UPDATE A SET ENTITLEMENT_XML = REPLACE(entitlement_xml ,  substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0091_VAL_CAPAVD</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml),charindex(''</ENTITLEMENT_VALUE_CODE>''  ,substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0091_VAL_CAPAVD</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml) , 1000 ))-1  ), ''<ENTITLEMENT_ID>AGS_Z0091_VAL_CAPAVD</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>''+TOOL_CAPITAL_AVOIDANCE ) FROM SAQSCE(NOLOCK) A JOIN (SELECT DISTINCT QUOTE_ID ,SERVICE_ID,EQUIPMENT_ID,REVISION_ID,TOOL_CAPITAL_AVOIDANCE FROM SAQICO_INBOUND B(NOLOCK) JOIN "+str(CRMTMP)+" C ON B.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND B.SERVICE_ID = ''Z0092'' ) B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID  = B.EQUIPMENT_ID AND A.QTEREV_ID = B.REVISION_ID  WHERE A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND ISNULL(TOOL_CAPITAL_AVOIDANCE,'''')<>'''' '")"""
							
							#SAQIEN Capital Avoidance
							#Z0091
							primaryQueryItems = SqlHelper.GetFirst("sp_executesql @t=N'UPDATE A SET ENTITLEMENT_XML = REPLACE(entitlement_xml ,  substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0091_VAL_CAPAVD</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml),charindex(''</ENTITLEMENT_VALUE_CODE>''  ,substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0091_VAL_CAPAVD</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml) , 1000 ))-1  ), ''<ENTITLEMENT_ID>AGS_Z0091_VAL_CAPAVD</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>''+TOOL_CAPITAL_AVOIDANCE ) FROM SAQIEN(NOLOCK) A JOIN (SELECT DISTINCT QUOTE_ID ,SERVICE_ID,EQUIPMENT_ID,REVISION_ID,TOOL_CAPITAL_AVOIDANCE FROM SAQICO_INBOUND B(NOLOCK) JOIN "+str(CRMTMP)+" C ON B.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND B.SERVICE_ID = ''Z0091'') B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID  = B.EQUIPMENT_ID AND A.QTEREV_ID = B.REVISION_ID  WHERE A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND ISNULL(TOOL_CAPITAL_AVOIDANCE,'''')<>'''' '")
							
							#Z0092
							primaryQueryItems = SqlHelper.GetFirst("sp_executesql @t=N'UPDATE A SET ENTITLEMENT_XML = REPLACE(entitlement_xml ,  substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0092_VAL_CAPAVD</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml),charindex(''</ENTITLEMENT_VALUE_CODE>''  ,substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0092_VAL_CAPAVD</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml) , 1000 ))-1  ), ''<ENTITLEMENT_ID>AGS_Z0092_VAL_CAPAVD</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>''+TOOL_CAPITAL_AVOIDANCE ) FROM SAQIEN(NOLOCK) A JOIN (SELECT DISTINCT QUOTE_ID ,SERVICE_ID,EQUIPMENT_ID,REVISION_ID,TOOL_CAPITAL_AVOIDANCE FROM SAQICO_INBOUND B(NOLOCK) JOIN "+str(CRMTMP)+" C ON B.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND B.SERVICE_ID = ''Z0092'') B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID  = B.EQUIPMENT_ID AND A.QTEREV_ID = B.REVISION_ID  WHERE A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND ISNULL(TOOL_CAPITAL_AVOIDANCE,'''')<>'''' '")
							
							#Z0004
							primaryQueryItems = SqlHelper.GetFirst("sp_executesql @t=N'UPDATE A SET ENTITLEMENT_XML = REPLACE(entitlement_xml ,  substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0004_VAL_CAPAVD</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml),charindex(''</ENTITLEMENT_VALUE_CODE>''  ,substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0004_VAL_CAPAVD</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml) , 1000 ))-1  ), ''<ENTITLEMENT_ID>AGS_Z0004_VAL_CAPAVD</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>''+TOOL_CAPITAL_AVOIDANCE ) FROM SAQIEN(NOLOCK) A JOIN (SELECT DISTINCT QUOTE_ID ,SERVICE_ID,EQUIPMENT_ID,REVISION_ID,TOOL_CAPITAL_AVOIDANCE FROM SAQICO_INBOUND B(NOLOCK) JOIN "+str(CRMTMP)+" C ON B.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND B.SERVICE_ID = ''Z0004'') B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID  = B.EQUIPMENT_ID AND A.QTEREV_ID = B.REVISION_ID  WHERE A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND ISNULL(TOOL_CAPITAL_AVOIDANCE,'''')<>'''' '")
							
							#Z0099
							primaryQueryItems = SqlHelper.GetFirst("sp_executesql @t=N'UPDATE A SET ENTITLEMENT_XML = REPLACE(entitlement_xml ,  substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0099_VAL_CAPAVD</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml),charindex(''</ENTITLEMENT_VALUE_CODE>''  ,substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0099_VAL_CAPAVD</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml) , 1000 ))-1  ), ''<ENTITLEMENT_ID>AGS_Z0099_VAL_CAPAVD</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>''+TOOL_CAPITAL_AVOIDANCE ) FROM SAQIEN(NOLOCK) A JOIN (SELECT DISTINCT QUOTE_ID ,SERVICE_ID,EQUIPMENT_ID,REVISION_ID,TOOL_CAPITAL_AVOIDANCE FROM SAQICO_INBOUND B(NOLOCK) JOIN "+str(CRMTMP)+" C ON B.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND B.SERVICE_ID = ''Z0099'') B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID  = B.EQUIPMENT_ID AND A.QTEREV_ID = B.REVISION_ID  WHERE A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND ISNULL(TOOL_CAPITAL_AVOIDANCE,'''')<>'''' '")
							
							#SAQSCE Captial Avoidance Coefficent
							#Z0091
							"""primaryQueryItems = SqlHelper.GetFirst("sp_executesql @t=N'UPDATE A SET ENTITLEMENT_XML = REPLACE(entitlement_xml ,  substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0091_VAL_CAPACO</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml),charindex(''</ENTITLEMENT_VALUE_CODE>''  ,substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0091_VAL_CAPACO</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml) , 1000 ))-1  ), ''<ENTITLEMENT_ID>AGS_Z0091_VAL_CAPACO</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>''+CAPITALAVOIDANCE_COEFFICIENT ) FROM SAQSCE(NOLOCK) A JOIN (SELECT DISTINCT QUOTE_ID ,SERVICE_ID,EQUIPMENT_ID,REVISION_ID,CAPITALAVOIDANCE_COEFFICIENT FROM SAQICO_INBOUND B(NOLOCK) JOIN "+str(CRMTMP)+" C ON B.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND B.SERVICE_ID = ''Z0091'' )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID  = B.EQUIPMENT_ID AND A.QTEREV_ID = B.REVISION_ID  WHERE A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"''  AND ISNULL(CAPITALAVOIDANCE_COEFFICIENT,'''')<>'''' '")
							
							#Z0092
							primaryQueryItems = SqlHelper.GetFirst("sp_executesql @t=N'UPDATE A SET ENTITLEMENT_XML = REPLACE(entitlement_xml ,  substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0091_VAL_CAPACO</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml),charindex(''</ENTITLEMENT_VALUE_CODE>''  ,substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0091_VAL_CAPACO</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml) , 1000 ))-1  ), ''<ENTITLEMENT_ID>AGS_Z0091_VAL_CAPACO</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>''+CAPITALAVOIDANCE_COEFFICIENT ) FROM SAQSCE(NOLOCK) A JOIN (SELECT DISTINCT QUOTE_ID ,SERVICE_ID,EQUIPMENT_ID,REVISION_ID,CAPITALAVOIDANCE_COEFFICIENT FROM SAQICO_INBOUND B(NOLOCK) JOIN "+str(CRMTMP)+" C ON B.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND B.SERVICE_ID = ''Z0092'' )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID  = B.EQUIPMENT_ID AND A.QTEREV_ID = B.REVISION_ID  WHERE A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"''  AND ISNULL(CAPITALAVOIDANCE_COEFFICIENT,'''')<>'''' '")"""
							
							#SAQIEN Capital Avoidance Coefficent
							#Z0091
							primaryQueryItems = SqlHelper.GetFirst("sp_executesql @t=N'UPDATE A SET ENTITLEMENT_XML = REPLACE(entitlement_xml ,  substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0091_VAL_CAPACO</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml),charindex(''</ENTITLEMENT_VALUE_CODE>''  ,substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0091_VAL_CAPACO</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml) , 1000 ))-1  ), ''<ENTITLEMENT_ID>AGS_Z0091_VAL_CAPACO</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>''+CAPITALAVOIDANCE_COEFFICIENT ) FROM SAQIEN(NOLOCK) A JOIN (SELECT DISTINCT QUOTE_ID ,SERVICE_ID,EQUIPMENT_ID,REVISION_ID,CAPITALAVOIDANCE_COEFFICIENT FROM SAQICO_INBOUND B(NOLOCK) JOIN "+str(CRMTMP)+" C ON B.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND B.SERVICE_ID = ''Z0091'' )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID  = B.EQUIPMENT_ID AND A.QTEREV_ID = B.REVISION_ID  WHERE A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"''  AND ISNULL(CAPITALAVOIDANCE_COEFFICIENT,'''')<>'''' '")
							
							#Z0092
							primaryQueryItems = SqlHelper.GetFirst("sp_executesql @t=N'UPDATE A SET ENTITLEMENT_XML = REPLACE(entitlement_xml ,  substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0092_VAL_CAPACO</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml),charindex(''</ENTITLEMENT_VALUE_CODE>''  ,substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0092_VAL_CAPACO</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml) , 1000 ))-1  ), ''<ENTITLEMENT_ID>AGS_Z0092_VAL_CAPACO</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>''+CAPITALAVOIDANCE_COEFFICIENT ) FROM SAQIEN(NOLOCK) A JOIN (SELECT DISTINCT QUOTE_ID ,SERVICE_ID,EQUIPMENT_ID,REVISION_ID,CAPITALAVOIDANCE_COEFFICIENT FROM SAQICO_INBOUND B(NOLOCK) JOIN "+str(CRMTMP)+" C ON B.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND B.SERVICE_ID = ''Z0092'')B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID  = B.EQUIPMENT_ID AND A.QTEREV_ID = B.REVISION_ID  WHERE A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"''  AND ISNULL(CAPITALAVOIDANCE_COEFFICIENT,'''')<>'''' '")
							
							#Z0004
							primaryQueryItems = SqlHelper.GetFirst("sp_executesql @t=N'UPDATE A SET ENTITLEMENT_XML = REPLACE(entitlement_xml ,  substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0004_VAL_CAPACO</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml),charindex(''</ENTITLEMENT_VALUE_CODE>''  ,substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0004_VAL_CAPACO</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml) , 1000 ))-1  ), ''<ENTITLEMENT_ID>AGS_Z0004_VAL_CAPACO</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>''+CAPITALAVOIDANCE_COEFFICIENT ) FROM SAQIEN(NOLOCK) A JOIN (SELECT DISTINCT QUOTE_ID ,SERVICE_ID,EQUIPMENT_ID,REVISION_ID,CAPITALAVOIDANCE_COEFFICIENT FROM SAQICO_INBOUND B(NOLOCK) JOIN "+str(CRMTMP)+" C ON B.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND B.SERVICE_ID = ''Z0004'')B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID  = B.EQUIPMENT_ID AND A.QTEREV_ID = B.REVISION_ID  WHERE A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"''  AND ISNULL(CAPITALAVOIDANCE_COEFFICIENT,'''')<>'''' '")
							
							#Z0099
							primaryQueryItems = SqlHelper.GetFirst("sp_executesql @t=N'UPDATE A SET ENTITLEMENT_XML = REPLACE(entitlement_xml ,  substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0099_VAL_CAPACO</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml),charindex(''</ENTITLEMENT_VALUE_CODE>''  ,substring(entitlement_xml,charindex(''<ENTITLEMENT_ID>AGS_Z0099_VAL_CAPACO</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>'' ,entitlement_xml) , 1000 ))-1  ), ''<ENTITLEMENT_ID>AGS_Z0099_VAL_CAPACO</ENTITLEMENT_ID><ENTITLEMENT_VALUE_CODE>''+CAPITALAVOIDANCE_COEFFICIENT ) FROM SAQIEN(NOLOCK) A JOIN (SELECT DISTINCT QUOTE_ID ,SERVICE_ID,EQUIPMENT_ID,REVISION_ID,CAPITALAVOIDANCE_COEFFICIENT FROM SAQICO_INBOUND B(NOLOCK) JOIN "+str(CRMTMP)+" C ON B.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND B.SERVICE_ID = ''Z0099'')B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID  = B.EQUIPMENT_ID AND A.QTEREV_ID = B.REVISION_ID  WHERE A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"''  AND ISNULL(CAPITALAVOIDANCE_COEFFICIENT,'''')<>'''' '")
							
							#Customer Segment
							#Z0091
							S3 = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET TOTAL_COEFFICIENT= ISNULL(TOTAL_COEFFICIENT,0) + ISNULL(CONVERT(FLOAT,ENTITLEMENT_VALUE_CODE),0) FROM SAQICO_INBOUND A(NOLOCK) JOIN (SELECT distinct quote_ID,equipment_id,service_id, replace(X.Y.value(''(ENTITLEMENT_VALUE_CODE)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_VALUE_CODE,replace(X.Y.value(''(ENTITLEMENT_NAME)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_NAME FROM (SELECT quote_ID,equipment_id,service_id,CONVERT(XML,''<QUOTE_ENTITLEMENT>''+substring(entitlement_xml,charindex (''<ENTITLEMENT_ID>AGS_Z0091_VAL_CSSGCO'',entitlement_xml),charindex (''Customer Segment Coefficent</ENTITLEMENT_NAME>'',entitlement_xml)-charindex (''<ENTITLEMENT_ID>AGS_Z0091_VAL_CSSGCO'',entitlement_xml)+len(''Customer Segment Coefficent</ENTITLEMENT_NAME>''))+''</QUOTE_ENTITLEMENT>'') as entitlement_xml FROM SAQSCE (nolock)a JOIN "+str(CRMTMP)+" C ON A.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND SERVICE_ID = ''Z0091'') e OUTER APPLY e.ENTITLEMENT_XML.nodes(''QUOTE_ENTITLEMENT'') as X(Y) )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID  WHERE B.ENTITLEMENT_NAME=''Customer Segment Coefficent'' AND ISNULL(ENTITLEMENT_VALUE_CODE,'''') <>''''  '")
							
							#Z0092
							S3 = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET TOTAL_COEFFICIENT= ISNULL(TOTAL_COEFFICIENT,0) + ISNULL(CONVERT(FLOAT,ENTITLEMENT_VALUE_CODE),0) FROM SAQICO_INBOUND A(NOLOCK) JOIN (SELECT distinct quote_ID,equipment_id,service_id, replace(X.Y.value(''(ENTITLEMENT_VALUE_CODE)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_VALUE_CODE,replace(X.Y.value(''(ENTITLEMENT_NAME)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_NAME FROM (SELECT quote_ID,equipment_id,service_id,CONVERT(XML,''<QUOTE_ENTITLEMENT>''+substring(entitlement_xml,charindex (''<ENTITLEMENT_ID>AGS_Z0092_VAL_CSSGCO'',entitlement_xml),charindex (''Customer Segment Coefficent</ENTITLEMENT_NAME>'',entitlement_xml)-charindex (''<ENTITLEMENT_ID>AGS_Z0092_VAL_CSSGCO'',entitlement_xml)+len(''Customer Segment Coefficent</ENTITLEMENT_NAME>''))+''</QUOTE_ENTITLEMENT>'') as entitlement_xml FROM SAQSCE (nolock)a JOIN "+str(CRMTMP)+" C ON A.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND SERVICE_ID = ''Z0092'') e OUTER APPLY e.ENTITLEMENT_XML.nodes(''QUOTE_ENTITLEMENT'') as X(Y) )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID  WHERE B.ENTITLEMENT_NAME=''Customer Segment Coefficent'' AND ISNULL(ENTITLEMENT_VALUE_CODE,'''') <>''''  '")
							
							#Z0004
							S3 = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET TOTAL_COEFFICIENT= ISNULL(TOTAL_COEFFICIENT,0) + ISNULL(CONVERT(FLOAT,ENTITLEMENT_VALUE_CODE),0) FROM SAQICO_INBOUND A(NOLOCK) JOIN (SELECT distinct quote_ID,equipment_id,service_id, replace(X.Y.value(''(ENTITLEMENT_VALUE_CODE)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_VALUE_CODE,replace(X.Y.value(''(ENTITLEMENT_NAME)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_NAME FROM (SELECT quote_ID,equipment_id,service_id,CONVERT(XML,''<QUOTE_ENTITLEMENT>''+substring(entitlement_xml,charindex (''<ENTITLEMENT_ID>AGS_Z0004_VAL_CSSGCO'',entitlement_xml),charindex (''Customer Segment Coefficent</ENTITLEMENT_NAME>'',entitlement_xml)-charindex (''<ENTITLEMENT_ID>AGS_Z0004_VAL_CSSGCO'',entitlement_xml)+len(''Customer Segment Coefficent</ENTITLEMENT_NAME>''))+''</QUOTE_ENTITLEMENT>'') as entitlement_xml FROM SAQSCE (nolock)a JOIN "+str(CRMTMP)+" C ON A.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND SERVICE_ID = ''Z0004'') e OUTER APPLY e.ENTITLEMENT_XML.nodes(''QUOTE_ENTITLEMENT'') as X(Y) )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID  WHERE B.ENTITLEMENT_NAME=''Customer Segment Coefficent'' AND ISNULL(ENTITLEMENT_VALUE_CODE,'''') <>''''  '")
							
							#Z0099
							S3 = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET TOTAL_COEFFICIENT= ISNULL(TOTAL_COEFFICIENT,0) + ISNULL(CONVERT(FLOAT,ENTITLEMENT_VALUE_CODE),0) FROM SAQICO_INBOUND A(NOLOCK) JOIN (SELECT distinct quote_ID,equipment_id,service_id, replace(X.Y.value(''(ENTITLEMENT_VALUE_CODE)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_VALUE_CODE,replace(X.Y.value(''(ENTITLEMENT_NAME)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_NAME FROM (SELECT quote_ID,equipment_id,service_id,CONVERT(XML,''<QUOTE_ENTITLEMENT>''+substring(entitlement_xml,charindex (''<ENTITLEMENT_ID>AGS_Z0099_VAL_CSSGCO'',entitlement_xml),charindex (''Customer Segment Coefficent</ENTITLEMENT_NAME>'',entitlement_xml)-charindex (''<ENTITLEMENT_ID>AGS_Z0099_VAL_CSSGCO'',entitlement_xml)+len(''Customer Segment Coefficent</ENTITLEMENT_NAME>''))+''</QUOTE_ENTITLEMENT>'') as entitlement_xml FROM SAQSCE (nolock)a JOIN "+str(CRMTMP)+" C ON A.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND SERVICE_ID = ''Z0099'') e OUTER APPLY e.ENTITLEMENT_XML.nodes(''QUOTE_ENTITLEMENT'') as X(Y) )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID  WHERE B.ENTITLEMENT_NAME=''Customer Segment Coefficent'' AND ISNULL(ENTITLEMENT_VALUE_CODE,'''') <>''''  '")
							
							#Service Competition
							#Z0091
							S3 = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET TOTAL_COEFFICIENT= ISNULL(TOTAL_COEFFICIENT,0) + ISNULL(CONVERT(FLOAT,ENTITLEMENT_VALUE_CODE),0) FROM SAQICO_INBOUND A(NOLOCK) JOIN (SELECT distinct quote_ID,equipment_id,service_id, replace(X.Y.value(''(ENTITLEMENT_VALUE_CODE)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_VALUE_CODE,replace(X.Y.value(''(ENTITLEMENT_NAME)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_NAME FROM (SELECT quote_ID,equipment_id,service_id,CONVERT(XML,''<QUOTE_ENTITLEMENT>''+substring(entitlement_xml,charindex (''<ENTITLEMENT_ID>AGS_Z0091_VAL_SVCCCO'',entitlement_xml),charindex (''Service Competition Coefficien</ENTITLEMENT_NAME>'',entitlement_xml)-charindex (''<ENTITLEMENT_ID>AGS_Z0091_VAL_SVCCCO'',entitlement_xml)+len(''Service Competition Coefficien</ENTITLEMENT_NAME>''))+''</QUOTE_ENTITLEMENT>'') as entitlement_xml FROM SAQSCE (nolock)a JOIN "+str(CRMTMP)+" C ON A.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND SERVICE_ID = ''Z0091'') e OUTER APPLY e.ENTITLEMENT_XML.nodes(''QUOTE_ENTITLEMENT'') as X(Y) )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID  WHERE B.ENTITLEMENT_NAME=''Service Competition Coefficien'' AND ISNULL(ENTITLEMENT_VALUE_CODE,'''') <>''''  '")
							
							#Z0092
							S3 = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET TOTAL_COEFFICIENT= ISNULL(TOTAL_COEFFICIENT,0) + ISNULL(CONVERT(FLOAT,ENTITLEMENT_VALUE_CODE),0) FROM SAQICO_INBOUND A(NOLOCK) JOIN (SELECT distinct quote_ID,equipment_id,service_id, replace(X.Y.value(''(ENTITLEMENT_VALUE_CODE)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_VALUE_CODE,replace(X.Y.value(''(ENTITLEMENT_NAME)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_NAME FROM (SELECT quote_ID,equipment_id,service_id,CONVERT(XML,''<QUOTE_ENTITLEMENT>''+substring(entitlement_xml,charindex (''<ENTITLEMENT_ID>AGS_Z0092_VAL_SVCCCO'',entitlement_xml),charindex (''Service Competition Coefficien</ENTITLEMENT_NAME>'',entitlement_xml)-charindex (''<ENTITLEMENT_ID>AGS_Z0092_VAL_SVCCCO'',entitlement_xml)+len(''Service Competition Coefficien</ENTITLEMENT_NAME>''))+''</QUOTE_ENTITLEMENT>'') as entitlement_xml FROM SAQSCE (nolock)a JOIN "+str(CRMTMP)+" C ON A.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND SERVICE_ID = ''Z0092'') e OUTER APPLY e.ENTITLEMENT_XML.nodes(''QUOTE_ENTITLEMENT'') as X(Y) )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID  WHERE B.ENTITLEMENT_NAME=''Service Competition Coefficien'' AND ISNULL(ENTITLEMENT_VALUE_CODE,'''') <>''''  '")
							
							#Z0004
							S3 = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET TOTAL_COEFFICIENT= ISNULL(TOTAL_COEFFICIENT,0) + ISNULL(CONVERT(FLOAT,ENTITLEMENT_VALUE_CODE),0) FROM SAQICO_INBOUND A(NOLOCK) JOIN (SELECT distinct quote_ID,equipment_id,service_id, replace(X.Y.value(''(ENTITLEMENT_VALUE_CODE)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_VALUE_CODE,replace(X.Y.value(''(ENTITLEMENT_NAME)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_NAME FROM (SELECT quote_ID,equipment_id,service_id,CONVERT(XML,''<QUOTE_ENTITLEMENT>''+substring(entitlement_xml,charindex (''<ENTITLEMENT_ID>AGS_Z0004_VAL_SVCCCO'',entitlement_xml),charindex (''Service Competition Coefficien</ENTITLEMENT_NAME>'',entitlement_xml)-charindex (''<ENTITLEMENT_ID>AGS_Z0004_VAL_SVCCCO'',entitlement_xml)+len(''Service Competition Coefficien</ENTITLEMENT_NAME>''))+''</QUOTE_ENTITLEMENT>'') as entitlement_xml FROM SAQSCE (nolock)a JOIN "+str(CRMTMP)+" C ON A.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND SERVICE_ID = ''Z0004'') e OUTER APPLY e.ENTITLEMENT_XML.nodes(''QUOTE_ENTITLEMENT'') as X(Y) )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID  WHERE B.ENTITLEMENT_NAME=''Service Competition Coefficien'' AND ISNULL(ENTITLEMENT_VALUE_CODE,'''') <>''''  '")
							
							#Z0099
							S3 = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET TOTAL_COEFFICIENT= ISNULL(TOTAL_COEFFICIENT,0) + ISNULL(CONVERT(FLOAT,ENTITLEMENT_VALUE_CODE),0) FROM SAQICO_INBOUND A(NOLOCK) JOIN (SELECT distinct quote_ID,equipment_id,service_id, replace(X.Y.value(''(ENTITLEMENT_VALUE_CODE)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_VALUE_CODE,replace(X.Y.value(''(ENTITLEMENT_NAME)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_NAME FROM (SELECT quote_ID,equipment_id,service_id,CONVERT(XML,''<QUOTE_ENTITLEMENT>''+substring(entitlement_xml,charindex (''<ENTITLEMENT_ID>AGS_Z0099_VAL_SVCCCO'',entitlement_xml),charindex (''Service Competition Coefficien</ENTITLEMENT_NAME>'',entitlement_xml)-charindex (''<ENTITLEMENT_ID>AGS_Z0099_VAL_SVCCCO'',entitlement_xml)+len(''Service Competition Coefficien</ENTITLEMENT_NAME>''))+''</QUOTE_ENTITLEMENT>'') as entitlement_xml FROM SAQSCE (nolock)a JOIN "+str(CRMTMP)+" C ON A.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND SERVICE_ID = ''Z0099'') e OUTER APPLY e.ENTITLEMENT_XML.nodes(''QUOTE_ENTITLEMENT'') as X(Y) )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID  WHERE B.ENTITLEMENT_NAME=''Service Competition Coefficien'' AND ISNULL(ENTITLEMENT_VALUE_CODE,'''') <>''''  '")

							#Quality Required 
							#Z0091
							S3 = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET TOTAL_COEFFICIENT= ISNULL(TOTAL_COEFFICIENT,0) + ISNULL(CONVERT(FLOAT,ENTITLEMENT_VALUE_CODE),0) FROM SAQICO_INBOUND A(NOLOCK) JOIN (SELECT distinct quote_ID,equipment_id,service_id, replace(X.Y.value(''(ENTITLEMENT_VALUE_CODE)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_VALUE_CODE,replace(X.Y.value(''(ENTITLEMENT_NAME)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_NAME FROM (SELECT quote_ID,equipment_id,service_id,CONVERT(XML,''<QUOTE_ENTITLEMENT>''+substring(entitlement_xml,charindex (''<ENTITLEMENT_ID>AGS_Z0091_VAL_QLYRCO'',entitlement_xml),charindex (''Quality Required Coefficient</ENTITLEMENT_NAME>'',entitlement_xml)-charindex (''<ENTITLEMENT_ID>AGS_Z0091_VAL_QLYRCO'',entitlement_xml)+len(''Quality Required Coefficient</ENTITLEMENT_NAME>''))+''</QUOTE_ENTITLEMENT>'') as entitlement_xml FROM SAQSCE (nolock)a JOIN "+str(CRMTMP)+" C ON A.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND SERVICE_ID = ''Z0091'') e OUTER APPLY e.ENTITLEMENT_XML.nodes(''QUOTE_ENTITLEMENT'') as X(Y) )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID  WHERE B.ENTITLEMENT_NAME=''Quality Required Coefficient'' AND ISNULL(ENTITLEMENT_VALUE_CODE,'''') <>''''  '")
							
							#Z0092
							S3 = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET TOTAL_COEFFICIENT= ISNULL(TOTAL_COEFFICIENT,0) + ISNULL(CONVERT(FLOAT,ENTITLEMENT_VALUE_CODE),0) FROM SAQICO_INBOUND A(NOLOCK) JOIN (SELECT distinct quote_ID,equipment_id,service_id, replace(X.Y.value(''(ENTITLEMENT_VALUE_CODE)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_VALUE_CODE,replace(X.Y.value(''(ENTITLEMENT_NAME)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_NAME FROM (SELECT quote_ID,equipment_id,service_id,CONVERT(XML,''<QUOTE_ENTITLEMENT>''+substring(entitlement_xml,charindex (''<ENTITLEMENT_ID>AGS_Z0092_VAL_QLYRCO'',entitlement_xml),charindex (''Quality Required Coefficient</ENTITLEMENT_NAME>'',entitlement_xml)-charindex (''<ENTITLEMENT_ID>AGS_Z0092_VAL_QLYRCO'',entitlement_xml)+len(''Quality Required Coefficient</ENTITLEMENT_NAME>''))+''</QUOTE_ENTITLEMENT>'') as entitlement_xml FROM SAQSCE (nolock)a JOIN "+str(CRMTMP)+" C ON A.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND SERVICE_ID = ''Z0092'') e OUTER APPLY e.ENTITLEMENT_XML.nodes(''QUOTE_ENTITLEMENT'') as X(Y) )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID  WHERE B.ENTITLEMENT_NAME=''Quality Required Coefficient'' AND ISNULL(ENTITLEMENT_VALUE_CODE,'''') <>''''  '")
							
							#Z0004
							S3 = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET TOTAL_COEFFICIENT= ISNULL(TOTAL_COEFFICIENT,0) + ISNULL(CONVERT(FLOAT,ENTITLEMENT_VALUE_CODE),0) FROM SAQICO_INBOUND A(NOLOCK) JOIN (SELECT distinct quote_ID,equipment_id,service_id, replace(X.Y.value(''(ENTITLEMENT_VALUE_CODE)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_VALUE_CODE,replace(X.Y.value(''(ENTITLEMENT_NAME)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_NAME FROM (SELECT quote_ID,equipment_id,service_id,CONVERT(XML,''<QUOTE_ENTITLEMENT>''+substring(entitlement_xml,charindex (''<ENTITLEMENT_ID>AGS_Z0004_VAL_QLYRCO'',entitlement_xml),charindex (''Quality Required Coefficient</ENTITLEMENT_NAME>'',entitlement_xml)-charindex (''<ENTITLEMENT_ID>AGS_Z0004_VAL_QLYRCO'',entitlement_xml)+len(''Quality Required Coefficient</ENTITLEMENT_NAME>''))+''</QUOTE_ENTITLEMENT>'') as entitlement_xml FROM SAQSCE (nolock)a JOIN "+str(CRMTMP)+" C ON A.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND SERVICE_ID = ''Z0004'') e OUTER APPLY e.ENTITLEMENT_XML.nodes(''QUOTE_ENTITLEMENT'') as X(Y) )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID  WHERE B.ENTITLEMENT_NAME=''Quality Required Coefficient'' AND ISNULL(ENTITLEMENT_VALUE_CODE,'''') <>''''  '")
							
							#Z0099
							S3 = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET TOTAL_COEFFICIENT= ISNULL(TOTAL_COEFFICIENT,0) + ISNULL(CONVERT(FLOAT,ENTITLEMENT_VALUE_CODE),0) FROM SAQICO_INBOUND A(NOLOCK) JOIN (SELECT distinct quote_ID,equipment_id,service_id, replace(X.Y.value(''(ENTITLEMENT_VALUE_CODE)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_VALUE_CODE,replace(X.Y.value(''(ENTITLEMENT_NAME)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_NAME FROM (SELECT quote_ID,equipment_id,service_id,CONVERT(XML,''<QUOTE_ENTITLEMENT>''+substring(entitlement_xml,charindex (''<ENTITLEMENT_ID>AGS_Z0099_VAL_QLYRCO'',entitlement_xml),charindex (''Quality Required Coefficient</ENTITLEMENT_NAME>'',entitlement_xml)-charindex (''<ENTITLEMENT_ID>AGS_Z0099_VAL_QLYRCO'',entitlement_xml)+len(''Quality Required Coefficient</ENTITLEMENT_NAME>''))+''</QUOTE_ENTITLEMENT>'') as entitlement_xml FROM SAQSCE (nolock)a JOIN "+str(CRMTMP)+" C ON A.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND SERVICE_ID = ''Z0099'') e OUTER APPLY e.ENTITLEMENT_XML.nodes(''QUOTE_ENTITLEMENT'') as X(Y) )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID  WHERE B.ENTITLEMENT_NAME=''Quality Required Coefficient'' AND ISNULL(ENTITLEMENT_VALUE_CODE,'''') <>''''  '")

							#Intercept
							#Z0091
							S3 = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET INTERCEPT=  ISNULL(CONVERT(FLOAT,ENTITLEMENT_VALUE_CODE),0) FROM SAQICO_INBOUND A(NOLOCK) JOIN (SELECT distinct quote_ID,equipment_id,service_id, replace(X.Y.value(''(ENTITLEMENT_VALUE_CODE)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_VALUE_CODE,replace(X.Y.value(''(ENTITLEMENT_NAME)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_NAME FROM (SELECT quote_ID,equipment_id,service_id,CONVERT(XML,''<QUOTE_ENTITLEMENT>''+substring(entitlement_xml,charindex (''<ENTITLEMENT_ID>AGS_Z0091_VAL_INTCCO'',entitlement_xml),charindex (''Intercept Coefficient</ENTITLEMENT_NAME>'',entitlement_xml)-charindex (''<ENTITLEMENT_ID>AGS_Z0091_VAL_INTCCO'',entitlement_xml)+len(''Intercept Coefficient</ENTITLEMENT_NAME>''))+''</QUOTE_ENTITLEMENT>'') as entitlement_xml FROM SAQSCE (nolock)a JOIN "+str(CRMTMP)+" C ON A.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND SERVICE_ID = ''Z0091'') e OUTER APPLY e.ENTITLEMENT_XML.nodes(''QUOTE_ENTITLEMENT'') as X(Y) )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID  WHERE B.ENTITLEMENT_NAME=''Intercept Coefficient'' AND ISNULL(ENTITLEMENT_VALUE_CODE,'''') <>'''' '")
							
							#Z0092
							S3 = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET INTERCEPT=  ISNULL(CONVERT(FLOAT,ENTITLEMENT_VALUE_CODE),0) FROM SAQICO_INBOUND A(NOLOCK) JOIN (SELECT distinct quote_ID,equipment_id,service_id, replace(X.Y.value(''(ENTITLEMENT_VALUE_CODE)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_VALUE_CODE,replace(X.Y.value(''(ENTITLEMENT_NAME)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_NAME FROM (SELECT quote_ID,equipment_id,service_id,CONVERT(XML,''<QUOTE_ENTITLEMENT>''+substring(entitlement_xml,charindex (''<ENTITLEMENT_ID>AGS_Z0092_VAL_INTCCO'',entitlement_xml),charindex (''Intercept Coefficient</ENTITLEMENT_NAME>'',entitlement_xml)-charindex (''<ENTITLEMENT_ID>AGS_Z0092_VAL_INTCCO'',entitlement_xml)+len(''Intercept Coefficient</ENTITLEMENT_NAME>''))+''</QUOTE_ENTITLEMENT>'') as entitlement_xml FROM SAQSCE (nolock)a JOIN "+str(CRMTMP)+" C ON A.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND SERVICE_ID = ''Z0092'') e OUTER APPLY e.ENTITLEMENT_XML.nodes(''QUOTE_ENTITLEMENT'') as X(Y) )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID  WHERE B.ENTITLEMENT_NAME=''Intercept Coefficient'' AND ISNULL(ENTITLEMENT_VALUE_CODE,'''') <>'''' '")
							
							#Z0004
							S3 = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET INTERCEPT=  ISNULL(CONVERT(FLOAT,ENTITLEMENT_VALUE_CODE),0) FROM SAQICO_INBOUND A(NOLOCK) JOIN (SELECT distinct quote_ID,equipment_id,service_id, replace(X.Y.value(''(ENTITLEMENT_VALUE_CODE)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_VALUE_CODE,replace(X.Y.value(''(ENTITLEMENT_NAME)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_NAME FROM (SELECT quote_ID,equipment_id,service_id,CONVERT(XML,''<QUOTE_ENTITLEMENT>''+substring(entitlement_xml,charindex (''<ENTITLEMENT_ID>AGS_Z0004_VAL_INTCCO'',entitlement_xml),charindex (''Intercept Coefficient</ENTITLEMENT_NAME>'',entitlement_xml)-charindex (''<ENTITLEMENT_ID>AGS_Z0004_VAL_INTCCO'',entitlement_xml)+len(''Intercept Coefficient</ENTITLEMENT_NAME>''))+''</QUOTE_ENTITLEMENT>'') as entitlement_xml FROM SAQSCE (nolock)a JOIN "+str(CRMTMP)+" C ON A.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND SERVICE_ID = ''Z0004'') e OUTER APPLY e.ENTITLEMENT_XML.nodes(''QUOTE_ENTITLEMENT'') as X(Y) )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID  WHERE B.ENTITLEMENT_NAME=''Intercept Coefficient'' AND ISNULL(ENTITLEMENT_VALUE_CODE,'''') <>'''' '")
							
							#Z0099
							S3 = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET INTERCEPT=  ISNULL(CONVERT(FLOAT,ENTITLEMENT_VALUE_CODE),0) FROM SAQICO_INBOUND A(NOLOCK) JOIN (SELECT distinct quote_ID,equipment_id,service_id, replace(X.Y.value(''(ENTITLEMENT_VALUE_CODE)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_VALUE_CODE,replace(X.Y.value(''(ENTITLEMENT_NAME)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_NAME FROM (SELECT quote_ID,equipment_id,service_id,CONVERT(XML,''<QUOTE_ENTITLEMENT>''+substring(entitlement_xml,charindex (''<ENTITLEMENT_ID>AGS_Z0099_VAL_INTCCO'',entitlement_xml),charindex (''Intercept Coefficient</ENTITLEMENT_NAME>'',entitlement_xml)-charindex (''<ENTITLEMENT_ID>AGS_Z0099_VAL_INTCCO'',entitlement_xml)+len(''Intercept Coefficient</ENTITLEMENT_NAME>''))+''</QUOTE_ENTITLEMENT>'') as entitlement_xml FROM SAQSCE (nolock)a JOIN "+str(CRMTMP)+" C ON A.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND SERVICE_ID = ''Z0099'') e OUTER APPLY e.ENTITLEMENT_XML.nodes(''QUOTE_ENTITLEMENT'') as X(Y) )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID  WHERE B.ENTITLEMENT_NAME=''Intercept Coefficient'' AND ISNULL(ENTITLEMENT_VALUE_CODE,'''') <>'''' '")

							#Tool Base Coefficient
							S3 = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET LOG_FACTOR =  0.94 FROM SAQICO_INBOUND A(NOLOCK) WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND REVISION_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND SERVICE_ID = ''Z0091'' AND A.GREENBOOK <> ''PDC'' '")
							
							S3 = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET LOG_FACTOR =  0.94 FROM SAQICO_INBOUND A(NOLOCK) WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND REVISION_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND SERVICE_ID = ''Z0092'' AND A.GREENBOOK <> ''PDC'' '")
							
							S3 = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET LOG_FACTOR =  0.94 FROM SAQICO_INBOUND A(NOLOCK) WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND REVISION_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND SERVICE_ID = ''Z0004'' AND A.GREENBOOK <> ''PDC'' '")
							
							S3 = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET LOG_FACTOR =  0.94 FROM SAQICO_INBOUND A(NOLOCK) WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND REVISION_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND SERVICE_ID = ''Z0099'' AND A.GREENBOOK <> ''PDC'' '")

							#PDC Base Price Coefficient
							S3 = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET LOG_FACTOR =  0.92 FROM SAQICO_INBOUND A(NOLOCK) WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND REVISION_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND SERVICE_ID = ''Z0091'' AND A.GREENBOOK = ''PDC'' '")
							
							S3 = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET LOG_FACTOR =  0.92 FROM SAQICO_INBOUND A(NOLOCK) WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND REVISION_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND SERVICE_ID = ''Z0092'' AND A.GREENBOOK = ''PDC'' '")
							
							S3 = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET LOG_FACTOR =  0.92 FROM SAQICO_INBOUND A(NOLOCK) WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND REVISION_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND SERVICE_ID = ''Z0004'' AND A.GREENBOOK = ''PDC'' '")
							
							S3 = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET LOG_FACTOR =  0.92 FROM SAQICO_INBOUND A(NOLOCK) WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND REVISION_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND SERVICE_ID = ''Z0099'' AND A.GREENBOOK = ''PDC'' '")

							#Product Offering Coefficient
							#Z0091
							S3 = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET TOTAL_COEFFICIENT= ISNULL(TOTAL_COEFFICIENT,0) + ISNULL(CONVERT(FLOAT,ENTITLEMENT_VALUE_CODE),0) FROM SAQICO_INBOUND A(NOLOCK) JOIN (SELECT distinct quote_ID,equipment_id,service_id, replace(X.Y.value(''(ENTITLEMENT_VALUE_CODE)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_VALUE_CODE,replace(X.Y.value(''(ENTITLEMENT_NAME)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_NAME FROM (SELECT quote_ID,equipment_id,service_id,CONVERT(XML,''<QUOTE_ENTITLEMENT>''+substring(entitlement_xml,charindex (''<ENTITLEMENT_ID>AGS_Z0091_VAL_POFFCO'',entitlement_xml),charindex (''Product Offering Coefficient</ENTITLEMENT_NAME>'',entitlement_xml)-charindex (''<ENTITLEMENT_ID>AGS_Z0091_VAL_POFFCO'',entitlement_xml)+len(''Product Offering Coefficient</ENTITLEMENT_NAME>''))+''</QUOTE_ENTITLEMENT>'') as entitlement_xml FROM SAQSCE (nolock)a JOIN "+str(CRMTMP)+" C ON A.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND SERVICE_ID = ''Z0091'') e OUTER APPLY e.ENTITLEMENT_XML.nodes(''QUOTE_ENTITLEMENT'') as X(Y) )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID  WHERE B.ENTITLEMENT_NAME=''Product Offering Coefficient'' AND ISNULL(ENTITLEMENT_VALUE_CODE,'''') <>''''  '")
							
							#Z0092
							S3 = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET TOTAL_COEFFICIENT= ISNULL(TOTAL_COEFFICIENT,0) + ISNULL(CONVERT(FLOAT,ENTITLEMENT_VALUE_CODE),0) FROM SAQICO_INBOUND A(NOLOCK) JOIN (SELECT distinct quote_ID,equipment_id,service_id, replace(X.Y.value(''(ENTITLEMENT_VALUE_CODE)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_VALUE_CODE,replace(X.Y.value(''(ENTITLEMENT_NAME)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_NAME FROM (SELECT quote_ID,equipment_id,service_id,CONVERT(XML,''<QUOTE_ENTITLEMENT>''+substring(entitlement_xml,charindex (''<ENTITLEMENT_ID>AGS_Z0092_VAL_POFFCO'',entitlement_xml),charindex (''Product Offering Coefficient</ENTITLEMENT_NAME>'',entitlement_xml)-charindex (''<ENTITLEMENT_ID>AGS_Z0092_VAL_POFFCO'',entitlement_xml)+len(''Product Offering Coefficient</ENTITLEMENT_NAME>''))+''</QUOTE_ENTITLEMENT>'') as entitlement_xml FROM SAQSCE (nolock)a JOIN "+str(CRMTMP)+" C ON A.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND SERVICE_ID = ''Z0092'') e OUTER APPLY e.ENTITLEMENT_XML.nodes(''QUOTE_ENTITLEMENT'') as X(Y) )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID  WHERE B.ENTITLEMENT_NAME=''Product Offering Coefficient'' AND ISNULL(ENTITLEMENT_VALUE_CODE,'''') <>''''  '")
							
							#Z0004
							S3 = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET TOTAL_COEFFICIENT= ISNULL(TOTAL_COEFFICIENT,0) + ISNULL(CONVERT(FLOAT,ENTITLEMENT_VALUE_CODE),0) FROM SAQICO_INBOUND A(NOLOCK) JOIN (SELECT distinct quote_ID,equipment_id,service_id, replace(X.Y.value(''(ENTITLEMENT_VALUE_CODE)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_VALUE_CODE,replace(X.Y.value(''(ENTITLEMENT_NAME)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_NAME FROM (SELECT quote_ID,equipment_id,service_id,CONVERT(XML,''<QUOTE_ENTITLEMENT>''+substring(entitlement_xml,charindex (''<ENTITLEMENT_ID>AGS_Z0004_VAL_POFFCO'',entitlement_xml),charindex (''Product Offering Coefficient</ENTITLEMENT_NAME>'',entitlement_xml)-charindex (''<ENTITLEMENT_ID>AGS_Z0004_VAL_POFFCO'',entitlement_xml)+len(''Product Offering Coefficient</ENTITLEMENT_NAME>''))+''</QUOTE_ENTITLEMENT>'') as entitlement_xml FROM SAQSCE (nolock)a JOIN "+str(CRMTMP)+" C ON A.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND SERVICE_ID = ''Z0004'') e OUTER APPLY e.ENTITLEMENT_XML.nodes(''QUOTE_ENTITLEMENT'') as X(Y) )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID  WHERE B.ENTITLEMENT_NAME=''Product Offering Coefficient'' AND ISNULL(ENTITLEMENT_VALUE_CODE,'''') <>''''  '")
							
							#Z0099
							S3 = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET TOTAL_COEFFICIENT= ISNULL(TOTAL_COEFFICIENT,0) + ISNULL(CONVERT(FLOAT,ENTITLEMENT_VALUE_CODE),0) FROM SAQICO_INBOUND A(NOLOCK) JOIN (SELECT distinct quote_ID,equipment_id,service_id, replace(X.Y.value(''(ENTITLEMENT_VALUE_CODE)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_VALUE_CODE,replace(X.Y.value(''(ENTITLEMENT_NAME)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_NAME FROM (SELECT quote_ID,equipment_id,service_id,CONVERT(XML,''<QUOTE_ENTITLEMENT>''+substring(entitlement_xml,charindex (''<ENTITLEMENT_ID>AGS_Z0099_VAL_POFFCO'',entitlement_xml),charindex (''Product Offering Coefficient</ENTITLEMENT_NAME>'',entitlement_xml)-charindex (''<ENTITLEMENT_ID>AGS_Z0099_VAL_POFFCO'',entitlement_xml)+len(''Product Offering Coefficient</ENTITLEMENT_NAME>''))+''</QUOTE_ENTITLEMENT>'') as entitlement_xml FROM SAQSCE (nolock)a JOIN "+str(CRMTMP)+" C ON A.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND SERVICE_ID = ''Z0099'') e OUTER APPLY e.ENTITLEMENT_XML.nodes(''QUOTE_ENTITLEMENT'') as X(Y) )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID  WHERE B.ENTITLEMENT_NAME=''Product Offering Coefficient'' AND ISNULL(ENTITLEMENT_VALUE_CODE,'''') <>''''  '")

							#Greenbook Coefficient
							#Z0091
							S3 = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET TOTAL_COEFFICIENT= ISNULL(TOTAL_COEFFICIENT,0) + ISNULL(CONVERT(FLOAT,ENTITLEMENT_VALUE_CODE),0) FROM SAQICO_INBOUND A(NOLOCK) JOIN (SELECT distinct quote_ID,equipment_id,service_id, replace(X.Y.value(''(ENTITLEMENT_VALUE_CODE)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_VALUE_CODE,replace(X.Y.value(''(ENTITLEMENT_NAME)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_NAME FROM (SELECT quote_ID,equipment_id,service_id,CONVERT(XML,''<QUOTE_ENTITLEMENT>''+substring(entitlement_xml,charindex (''<ENTITLEMENT_ID>AGS_Z0091_VAL_GRNBCO'',entitlement_xml),charindex (''Greenbook Coefficient</ENTITLEMENT_NAME>'',entitlement_xml)-charindex (''<ENTITLEMENT_ID>AGS_Z0091_VAL_GRNBCO'',entitlement_xml)+len(''Greenbook Coefficient</ENTITLEMENT_NAME>''))+''</QUOTE_ENTITLEMENT>'') as entitlement_xml FROM SAQSCE (nolock)a JOIN "+str(CRMTMP)+" C ON A.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND SERVICE_ID = ''Z0091'') e OUTER APPLY e.ENTITLEMENT_XML.nodes(''QUOTE_ENTITLEMENT'') as X(Y) )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID  WHERE B.ENTITLEMENT_NAME=''Greenbook Coefficient'' AND ISNULL(ENTITLEMENT_VALUE_CODE,'''') <>''''  '")
							
							#Z0092
							S3 = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET TOTAL_COEFFICIENT= ISNULL(TOTAL_COEFFICIENT,0) + ISNULL(CONVERT(FLOAT,ENTITLEMENT_VALUE_CODE),0) FROM SAQICO_INBOUND A(NOLOCK) JOIN (SELECT distinct quote_ID,equipment_id,service_id, replace(X.Y.value(''(ENTITLEMENT_VALUE_CODE)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_VALUE_CODE,replace(X.Y.value(''(ENTITLEMENT_NAME)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_NAME FROM (SELECT quote_ID,equipment_id,service_id,CONVERT(XML,''<QUOTE_ENTITLEMENT>''+substring(entitlement_xml,charindex (''<ENTITLEMENT_ID>AGS_Z0092_VAL_GRNBCO'',entitlement_xml),charindex (''Greenbook Coefficient</ENTITLEMENT_NAME>'',entitlement_xml)-charindex (''<ENTITLEMENT_ID>AGS_Z0092_VAL_GRNBCO'',entitlement_xml)+len(''Greenbook Coefficient</ENTITLEMENT_NAME>''))+''</QUOTE_ENTITLEMENT>'') as entitlement_xml FROM SAQSCE (nolock)a JOIN "+str(CRMTMP)+" C ON A.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND SERVICE_ID = ''Z0092'') e OUTER APPLY e.ENTITLEMENT_XML.nodes(''QUOTE_ENTITLEMENT'') as X(Y) )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID  WHERE B.ENTITLEMENT_NAME=''Greenbook Coefficient'' AND ISNULL(ENTITLEMENT_VALUE_CODE,'''') <>''''  '")
							
							#Z0004
							S3 = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET TOTAL_COEFFICIENT= ISNULL(TOTAL_COEFFICIENT,0) + ISNULL(CONVERT(FLOAT,ENTITLEMENT_VALUE_CODE),0) FROM SAQICO_INBOUND A(NOLOCK) JOIN (SELECT distinct quote_ID,equipment_id,service_id, replace(X.Y.value(''(ENTITLEMENT_VALUE_CODE)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_VALUE_CODE,replace(X.Y.value(''(ENTITLEMENT_NAME)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_NAME FROM (SELECT quote_ID,equipment_id,service_id,CONVERT(XML,''<QUOTE_ENTITLEMENT>''+substring(entitlement_xml,charindex (''<ENTITLEMENT_ID>AGS_Z0004_VAL_GRNBCO'',entitlement_xml),charindex (''Greenbook Coefficient</ENTITLEMENT_NAME>'',entitlement_xml)-charindex (''<ENTITLEMENT_ID>AGS_Z0004_VAL_GRNBCO'',entitlement_xml)+len(''Greenbook Coefficient</ENTITLEMENT_NAME>''))+''</QUOTE_ENTITLEMENT>'') as entitlement_xml FROM SAQSCE (nolock)a JOIN "+str(CRMTMP)+" C ON A.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND SERVICE_ID = ''Z0004'') e OUTER APPLY e.ENTITLEMENT_XML.nodes(''QUOTE_ENTITLEMENT'') as X(Y) )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID  WHERE B.ENTITLEMENT_NAME=''Greenbook Coefficient'' AND ISNULL(ENTITLEMENT_VALUE_CODE,'''') <>''''  '")
							
							#Z0099
							S3 = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET TOTAL_COEFFICIENT= ISNULL(TOTAL_COEFFICIENT,0) + ISNULL(CONVERT(FLOAT,ENTITLEMENT_VALUE_CODE),0) FROM SAQICO_INBOUND A(NOLOCK) JOIN (SELECT distinct quote_ID,equipment_id,service_id, replace(X.Y.value(''(ENTITLEMENT_VALUE_CODE)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_VALUE_CODE,replace(X.Y.value(''(ENTITLEMENT_NAME)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_NAME FROM (SELECT quote_ID,equipment_id,service_id,CONVERT(XML,''<QUOTE_ENTITLEMENT>''+substring(entitlement_xml,charindex (''<ENTITLEMENT_ID>AGS_Z0099_VAL_GRNBCO'',entitlement_xml),charindex (''Greenbook Coefficient</ENTITLEMENT_NAME>'',entitlement_xml)-charindex (''<ENTITLEMENT_ID>AGS_Z0099_VAL_GRNBCO'',entitlement_xml)+len(''Greenbook Coefficient</ENTITLEMENT_NAME>''))+''</QUOTE_ENTITLEMENT>'') as entitlement_xml FROM SAQSCE (nolock)a JOIN "+str(CRMTMP)+" C ON A.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND SERVICE_ID = ''Z0099'') e OUTER APPLY e.ENTITLEMENT_XML.nodes(''QUOTE_ENTITLEMENT'') as X(Y) )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID  WHERE B.ENTITLEMENT_NAME=''Greenbook Coefficient'' AND ISNULL(ENTITLEMENT_VALUE_CODE,'''') <>''''  '")

							#Uptime Improvement Coefficient
							#Z0091
							S3 = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET TOTAL_COEFFICIENT= ISNULL(TOTAL_COEFFICIENT,0) + ISNULL(CONVERT(FLOAT,ENTITLEMENT_VALUE_CODE),0) FROM SAQICO_INBOUND A(NOLOCK) JOIN (SELECT distinct quote_ID,equipment_id,service_id, replace(X.Y.value(''(ENTITLEMENT_VALUE_CODE)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_VALUE_CODE,replace(X.Y.value(''(ENTITLEMENT_NAME)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_NAME FROM (SELECT quote_ID,equipment_id,service_id,CONVERT(XML,''<QUOTE_ENTITLEMENT>''+substring(entitlement_xml,charindex (''<ENTITLEMENT_ID>AGS_Z0091_VAL_UPIMCO'',entitlement_xml),charindex (''Uptime Improvement Coefficient</ENTITLEMENT_NAME>'',entitlement_xml)-charindex (''<ENTITLEMENT_ID>AGS_Z0091_VAL_UPIMCO'',entitlement_xml)+len(''Uptime Improvement Coefficient</ENTITLEMENT_NAME>''))+''</QUOTE_ENTITLEMENT>'') as entitlement_xml FROM SAQSCE (nolock)a JOIN "+str(CRMTMP)+" C ON A.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND SERVICE_ID = ''Z0091'') e OUTER APPLY e.ENTITLEMENT_XML.nodes(''QUOTE_ENTITLEMENT'') as X(Y) )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID  WHERE B.ENTITLEMENT_NAME=''Uptime Improvement Coefficient'' AND ISNULL(ENTITLEMENT_VALUE_CODE,'''') <>''''  '")
							
							#Z0092
							S3 = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET TOTAL_COEFFICIENT= ISNULL(TOTAL_COEFFICIENT,0) + ISNULL(CONVERT(FLOAT,ENTITLEMENT_VALUE_CODE),0) FROM SAQICO_INBOUND A(NOLOCK) JOIN (SELECT distinct quote_ID,equipment_id,service_id, replace(X.Y.value(''(ENTITLEMENT_VALUE_CODE)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_VALUE_CODE,replace(X.Y.value(''(ENTITLEMENT_NAME)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_NAME FROM (SELECT quote_ID,equipment_id,service_id,CONVERT(XML,''<QUOTE_ENTITLEMENT>''+substring(entitlement_xml,charindex (''<ENTITLEMENT_ID>AGS_Z0092_VAL_UPIMCO'',entitlement_xml),charindex (''Uptime Improvement Coefficient</ENTITLEMENT_NAME>'',entitlement_xml)-charindex (''<ENTITLEMENT_ID>AGS_Z0092_VAL_UPIMCO'',entitlement_xml)+len(''Uptime Improvement Coefficient</ENTITLEMENT_NAME>''))+''</QUOTE_ENTITLEMENT>'') as entitlement_xml FROM SAQSCE (nolock)a JOIN "+str(CRMTMP)+" C ON A.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND SERVICE_ID = ''Z0092'') e OUTER APPLY e.ENTITLEMENT_XML.nodes(''QUOTE_ENTITLEMENT'') as X(Y) )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID  WHERE B.ENTITLEMENT_NAME=''Uptime Improvement Coefficient'' AND ISNULL(ENTITLEMENT_VALUE_CODE,'''') <>''''  '")
							
							#Z0004
							S3 = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET TOTAL_COEFFICIENT= ISNULL(TOTAL_COEFFICIENT,0) + ISNULL(CONVERT(FLOAT,ENTITLEMENT_VALUE_CODE),0) FROM SAQICO_INBOUND A(NOLOCK) JOIN (SELECT distinct quote_ID,equipment_id,service_id, replace(X.Y.value(''(ENTITLEMENT_VALUE_CODE)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_VALUE_CODE,replace(X.Y.value(''(ENTITLEMENT_NAME)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_NAME FROM (SELECT quote_ID,equipment_id,service_id,CONVERT(XML,''<QUOTE_ENTITLEMENT>''+substring(entitlement_xml,charindex (''<ENTITLEMENT_ID>AGS_Z0004_VAL_UPIMCO'',entitlement_xml),charindex (''Uptime Improvement Coefficient</ENTITLEMENT_NAME>'',entitlement_xml)-charindex (''<ENTITLEMENT_ID>AGS_Z0004_VAL_UPIMCO'',entitlement_xml)+len(''Uptime Improvement Coefficient</ENTITLEMENT_NAME>''))+''</QUOTE_ENTITLEMENT>'') as entitlement_xml FROM SAQSCE (nolock)a JOIN "+str(CRMTMP)+" C ON A.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND SERVICE_ID = ''Z0004'') e OUTER APPLY e.ENTITLEMENT_XML.nodes(''QUOTE_ENTITLEMENT'') as X(Y) )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID  WHERE B.ENTITLEMENT_NAME=''Uptime Improvement Coefficient'' AND ISNULL(ENTITLEMENT_VALUE_CODE,'''') <>''''  '")
							
							#Z0099
							S3 = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET TOTAL_COEFFICIENT= ISNULL(TOTAL_COEFFICIENT,0) + ISNULL(CONVERT(FLOAT,ENTITLEMENT_VALUE_CODE),0) FROM SAQICO_INBOUND A(NOLOCK) JOIN (SELECT distinct quote_ID,equipment_id,service_id, replace(X.Y.value(''(ENTITLEMENT_VALUE_CODE)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_VALUE_CODE,replace(X.Y.value(''(ENTITLEMENT_NAME)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_NAME FROM (SELECT quote_ID,equipment_id,service_id,CONVERT(XML,''<QUOTE_ENTITLEMENT>''+substring(entitlement_xml,charindex (''<ENTITLEMENT_ID>AGS_Z0099_VAL_UPIMCO'',entitlement_xml),charindex (''Uptime Improvement Coefficient</ENTITLEMENT_NAME>'',entitlement_xml)-charindex (''<ENTITLEMENT_ID>AGS_Z0099_VAL_UPIMCO'',entitlement_xml)+len(''Uptime Improvement Coefficient</ENTITLEMENT_NAME>''))+''</QUOTE_ENTITLEMENT>'') as entitlement_xml FROM SAQSCE (nolock)a JOIN "+str(CRMTMP)+" C ON A.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND SERVICE_ID = ''Z0099'') e OUTER APPLY e.ENTITLEMENT_XML.nodes(''QUOTE_ENTITLEMENT'') as X(Y) )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID  WHERE B.ENTITLEMENT_NAME=''Uptime Improvement Coefficient'' AND ISNULL(ENTITLEMENT_VALUE_CODE,'''') <>''''  '")

							#Wafer Node Coefficient
							#Z0091
							S3 = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET TOTAL_COEFFICIENT= ISNULL(TOTAL_COEFFICIENT,0) + ISNULL(CONVERT(FLOAT,ENTITLEMENT_VALUE_CODE),0) FROM SAQICO_INBOUND A(NOLOCK) JOIN (SELECT distinct quote_ID,equipment_id,service_id, replace(X.Y.value(''(ENTITLEMENT_VALUE_CODE)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_VALUE_CODE,replace(X.Y.value(''(ENTITLEMENT_NAME)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_NAME FROM (SELECT quote_ID,equipment_id,service_id,CONVERT(XML,''<QUOTE_ENTITLEMENT>''+substring(entitlement_xml,charindex (''<ENTITLEMENT_ID>AGS_Z0091_VAL_WAFNCO'',entitlement_xml),charindex (''Wafer Node Coefficient</ENTITLEMENT_NAME>'',entitlement_xml)-charindex (''<ENTITLEMENT_ID>AGS_Z0091_VAL_WAFNCO'',entitlement_xml)+len(''Wafer Node Coefficient</ENTITLEMENT_NAME>''))+''</QUOTE_ENTITLEMENT>'') as entitlement_xml FROM SAQSCE (nolock)a JOIN "+str(CRMTMP)+" C ON A.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND SERVICE_ID = ''Z0091'') e OUTER APPLY e.ENTITLEMENT_XML.nodes(''QUOTE_ENTITLEMENT'') as X(Y) )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID  WHERE B.ENTITLEMENT_NAME=''Wafer Node Coefficient'' AND ISNULL(ENTITLEMENT_VALUE_CODE,'''') <>''''  '")
							
							#Z0092
							S3 = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET TOTAL_COEFFICIENT= ISNULL(TOTAL_COEFFICIENT,0) + ISNULL(CONVERT(FLOAT,ENTITLEMENT_VALUE_CODE),0) FROM SAQICO_INBOUND A(NOLOCK) JOIN (SELECT distinct quote_ID,equipment_id,service_id, replace(X.Y.value(''(ENTITLEMENT_VALUE_CODE)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_VALUE_CODE,replace(X.Y.value(''(ENTITLEMENT_NAME)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_NAME FROM (SELECT quote_ID,equipment_id,service_id,CONVERT(XML,''<QUOTE_ENTITLEMENT>''+substring(entitlement_xml,charindex (''<ENTITLEMENT_ID>AGS_Z0092_VAL_WAFNCO'',entitlement_xml),charindex (''Wafer Node Coefficient</ENTITLEMENT_NAME>'',entitlement_xml)-charindex (''<ENTITLEMENT_ID>AGS_Z0092_VAL_WAFNCO'',entitlement_xml)+len(''Wafer Node Coefficient</ENTITLEMENT_NAME>''))+''</QUOTE_ENTITLEMENT>'') as entitlement_xml FROM SAQSCE (nolock)a JOIN "+str(CRMTMP)+" C ON A.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND SERVICE_ID = ''Z0092'') e OUTER APPLY e.ENTITLEMENT_XML.nodes(''QUOTE_ENTITLEMENT'') as X(Y) )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID  WHERE B.ENTITLEMENT_NAME=''Wafer Node Coefficient'' AND ISNULL(ENTITLEMENT_VALUE_CODE,'''') <>''''  '")
							
							#Z0004
							S3 = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET TOTAL_COEFFICIENT= ISNULL(TOTAL_COEFFICIENT,0) + ISNULL(CONVERT(FLOAT,ENTITLEMENT_VALUE_CODE),0) FROM SAQICO_INBOUND A(NOLOCK) JOIN (SELECT distinct quote_ID,equipment_id,service_id, replace(X.Y.value(''(ENTITLEMENT_VALUE_CODE)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_VALUE_CODE,replace(X.Y.value(''(ENTITLEMENT_NAME)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_NAME FROM (SELECT quote_ID,equipment_id,service_id,CONVERT(XML,''<QUOTE_ENTITLEMENT>''+substring(entitlement_xml,charindex (''<ENTITLEMENT_ID>AGS_Z0004_VAL_WAFNCO'',entitlement_xml),charindex (''Wafer Node Coefficient</ENTITLEMENT_NAME>'',entitlement_xml)-charindex (''<ENTITLEMENT_ID>AGS_Z0004_VAL_WAFNCO'',entitlement_xml)+len(''Wafer Node Coefficient</ENTITLEMENT_NAME>''))+''</QUOTE_ENTITLEMENT>'') as entitlement_xml FROM SAQSCE (nolock)a JOIN "+str(CRMTMP)+" C ON A.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND SERVICE_ID = ''Z0004'') e OUTER APPLY e.ENTITLEMENT_XML.nodes(''QUOTE_ENTITLEMENT'') as X(Y) )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID  WHERE B.ENTITLEMENT_NAME=''Wafer Node Coefficient'' AND ISNULL(ENTITLEMENT_VALUE_CODE,'''') <>''''  '")
							
							#Z0099
							S3 = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET TOTAL_COEFFICIENT= ISNULL(TOTAL_COEFFICIENT,0) + ISNULL(CONVERT(FLOAT,ENTITLEMENT_VALUE_CODE),0) FROM SAQICO_INBOUND A(NOLOCK) JOIN (SELECT distinct quote_ID,equipment_id,service_id, replace(X.Y.value(''(ENTITLEMENT_VALUE_CODE)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_VALUE_CODE,replace(X.Y.value(''(ENTITLEMENT_NAME)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_NAME FROM (SELECT quote_ID,equipment_id,service_id,CONVERT(XML,''<QUOTE_ENTITLEMENT>''+substring(entitlement_xml,charindex (''<ENTITLEMENT_ID>AGS_Z0099_VAL_WAFNCO'',entitlement_xml),charindex (''Wafer Node Coefficient</ENTITLEMENT_NAME>'',entitlement_xml)-charindex (''<ENTITLEMENT_ID>AGS_Z0099_VAL_WAFNCO'',entitlement_xml)+len(''Wafer Node Coefficient</ENTITLEMENT_NAME>''))+''</QUOTE_ENTITLEMENT>'') as entitlement_xml FROM SAQSCE (nolock)a JOIN "+str(CRMTMP)+" C ON A.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND SERVICE_ID = ''Z0099'') e OUTER APPLY e.ENTITLEMENT_XML.nodes(''QUOTE_ENTITLEMENT'') as X(Y) )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID  WHERE B.ENTITLEMENT_NAME=''Wafer Node Coefficient'' AND ISNULL(ENTITLEMENT_VALUE_CODE,'''') <>''''  '")

							#Device Type Coefficient
							#Z0091
							S3 = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET TOTAL_COEFFICIENT= ISNULL(TOTAL_COEFFICIENT,0) + ISNULL(CONVERT(FLOAT,ENTITLEMENT_VALUE_CODE),0) FROM SAQICO_INBOUND A(NOLOCK) JOIN (SELECT distinct quote_ID,equipment_id,service_id, replace(X.Y.value(''(ENTITLEMENT_VALUE_CODE)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_VALUE_CODE,replace(X.Y.value(''(ENTITLEMENT_NAME)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_NAME FROM (SELECT quote_ID,equipment_id,service_id,CONVERT(XML,''<QUOTE_ENTITLEMENT>''+substring(entitlement_xml,charindex (''<ENTITLEMENT_ID>AGS_Z0091_VAL_DEVTCO'',entitlement_xml),charindex (''Device Type Coefficient</ENTITLEMENT_NAME>'',entitlement_xml)-charindex (''<ENTITLEMENT_ID>AGS_Z0091_VAL_DEVTCO'',entitlement_xml)+len(''Device Type Coefficient</ENTITLEMENT_NAME>''))+''</QUOTE_ENTITLEMENT>'') as entitlement_xml FROM SAQSCE (nolock)a JOIN "+str(CRMTMP)+" C ON A.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND SERVICE_ID = ''Z0091'') e OUTER APPLY e.ENTITLEMENT_XML.nodes(''QUOTE_ENTITLEMENT'') as X(Y) )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID  WHERE B.ENTITLEMENT_NAME=''Device Type Coefficient'' AND ISNULL(ENTITLEMENT_VALUE_CODE,'''') <>''''  '")
							
							#Z0092
							S3 = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET TOTAL_COEFFICIENT= ISNULL(TOTAL_COEFFICIENT,0) + ISNULL(CONVERT(FLOAT,ENTITLEMENT_VALUE_CODE),0) FROM SAQICO_INBOUND A(NOLOCK) JOIN (SELECT distinct quote_ID,equipment_id,service_id, replace(X.Y.value(''(ENTITLEMENT_VALUE_CODE)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_VALUE_CODE,replace(X.Y.value(''(ENTITLEMENT_NAME)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_NAME FROM (SELECT quote_ID,equipment_id,service_id,CONVERT(XML,''<QUOTE_ENTITLEMENT>''+substring(entitlement_xml,charindex (''<ENTITLEMENT_ID>AGS_Z0092_VAL_DEVTCO'',entitlement_xml),charindex (''Device Type Coefficient</ENTITLEMENT_NAME>'',entitlement_xml)-charindex (''<ENTITLEMENT_ID>AGS_Z0092_VAL_DEVTCO'',entitlement_xml)+len(''Device Type Coefficient</ENTITLEMENT_NAME>''))+''</QUOTE_ENTITLEMENT>'') as entitlement_xml FROM SAQSCE (nolock)a JOIN "+str(CRMTMP)+" C ON A.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND SERVICE_ID = ''Z0092'') e OUTER APPLY e.ENTITLEMENT_XML.nodes(''QUOTE_ENTITLEMENT'') as X(Y) )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID  WHERE B.ENTITLEMENT_NAME=''Device Type Coefficient'' AND ISNULL(ENTITLEMENT_VALUE_CODE,'''') <>''''  '")
							
							#Z0004
							S3 = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET TOTAL_COEFFICIENT= ISNULL(TOTAL_COEFFICIENT,0) + ISNULL(CONVERT(FLOAT,ENTITLEMENT_VALUE_CODE),0) FROM SAQICO_INBOUND A(NOLOCK) JOIN (SELECT distinct quote_ID,equipment_id,service_id, replace(X.Y.value(''(ENTITLEMENT_VALUE_CODE)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_VALUE_CODE,replace(X.Y.value(''(ENTITLEMENT_NAME)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_NAME FROM (SELECT quote_ID,equipment_id,service_id,CONVERT(XML,''<QUOTE_ENTITLEMENT>''+substring(entitlement_xml,charindex (''<ENTITLEMENT_ID>AGS_Z0004_VAL_DEVTCO'',entitlement_xml),charindex (''Device Type Coefficient</ENTITLEMENT_NAME>'',entitlement_xml)-charindex (''<ENTITLEMENT_ID>AGS_Z0004_VAL_DEVTCO'',entitlement_xml)+len(''Device Type Coefficient</ENTITLEMENT_NAME>''))+''</QUOTE_ENTITLEMENT>'') as entitlement_xml FROM SAQSCE (nolock)a JOIN "+str(CRMTMP)+" C ON A.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND SERVICE_ID = ''Z0004'') e OUTER APPLY e.ENTITLEMENT_XML.nodes(''QUOTE_ENTITLEMENT'') as X(Y) )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID  WHERE B.ENTITLEMENT_NAME=''Device Type Coefficient'' AND ISNULL(ENTITLEMENT_VALUE_CODE,'''') <>''''  '")
							
							#Z0099
							S3 = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET TOTAL_COEFFICIENT= ISNULL(TOTAL_COEFFICIENT,0) + ISNULL(CONVERT(FLOAT,ENTITLEMENT_VALUE_CODE),0) FROM SAQICO_INBOUND A(NOLOCK) JOIN (SELECT distinct quote_ID,equipment_id,service_id, replace(X.Y.value(''(ENTITLEMENT_VALUE_CODE)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_VALUE_CODE,replace(X.Y.value(''(ENTITLEMENT_NAME)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_NAME FROM (SELECT quote_ID,equipment_id,service_id,CONVERT(XML,''<QUOTE_ENTITLEMENT>''+substring(entitlement_xml,charindex (''<ENTITLEMENT_ID>AGS_Z0099_VAL_DEVTCO'',entitlement_xml),charindex (''Device Type Coefficient</ENTITLEMENT_NAME>'',entitlement_xml)-charindex (''<ENTITLEMENT_ID>AGS_Z0099_VAL_DEVTCO'',entitlement_xml)+len(''Device Type Coefficient</ENTITLEMENT_NAME>''))+''</QUOTE_ENTITLEMENT>'') as entitlement_xml FROM SAQSCE (nolock)a JOIN "+str(CRMTMP)+" C ON A.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND SERVICE_ID = ''Z0099'') e OUTER APPLY e.ENTITLEMENT_XML.nodes(''QUOTE_ENTITLEMENT'') as X(Y) )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID  WHERE B.ENTITLEMENT_NAME=''Device Type Coefficient'' AND ISNULL(ENTITLEMENT_VALUE_CODE,'''') <>''''  '")

							#CSA Tools per Fab Coefficient
							#Z0091
							S3 = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET TOTAL_COEFFICIENT= ISNULL(TOTAL_COEFFICIENT,0) + ISNULL(CONVERT(FLOAT,ENTITLEMENT_VALUE_CODE),0) FROM SAQICO_INBOUND A(NOLOCK) JOIN (SELECT distinct quote_ID,equipment_id,service_id, replace(X.Y.value(''(ENTITLEMENT_VALUE_CODE)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_VALUE_CODE,replace(X.Y.value(''(ENTITLEMENT_NAME)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_NAME FROM (SELECT quote_ID,equipment_id,service_id,CONVERT(XML,''<QUOTE_ENTITLEMENT>''+substring(entitlement_xml,charindex (''<ENTITLEMENT_ID>AGS_Z0091_VAL_TLSFCO'',entitlement_xml),charindex (''#CSA Tools per Fab Coefficient</ENTITLEMENT_NAME>'',entitlement_xml)-charindex (''<ENTITLEMENT_ID>AGS_Z0091_VAL_TLSFCO'',entitlement_xml)+len(''#CSA Tools per Fab Coefficient</ENTITLEMENT_NAME>''))+''</QUOTE_ENTITLEMENT>'') as entitlement_xml FROM SAQSCE (nolock)a JOIN "+str(CRMTMP)+" C ON A.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND SERVICE_ID = ''Z0091'') e OUTER APPLY e.ENTITLEMENT_XML.nodes(''QUOTE_ENTITLEMENT'') as X(Y) )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID  WHERE B.ENTITLEMENT_NAME=''#CSA Tools per Fab Coefficient'' AND ISNULL(ENTITLEMENT_VALUE_CODE,'''') <>''''  '")
							
							#Z0092
							S3 = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET TOTAL_COEFFICIENT= ISNULL(TOTAL_COEFFICIENT,0) + ISNULL(CONVERT(FLOAT,ENTITLEMENT_VALUE_CODE),0) FROM SAQICO_INBOUND A(NOLOCK) JOIN (SELECT distinct quote_ID,equipment_id,service_id, replace(X.Y.value(''(ENTITLEMENT_VALUE_CODE)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_VALUE_CODE,replace(X.Y.value(''(ENTITLEMENT_NAME)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_NAME FROM (SELECT quote_ID,equipment_id,service_id,CONVERT(XML,''<QUOTE_ENTITLEMENT>''+substring(entitlement_xml,charindex (''<ENTITLEMENT_ID>AGS_Z0092_VAL_TLSFCO'',entitlement_xml),charindex (''#CSA Tools per Fab Coefficient</ENTITLEMENT_NAME>'',entitlement_xml)-charindex (''<ENTITLEMENT_ID>AGS_Z0092_VAL_TLSFCO'',entitlement_xml)+len(''#CSA Tools per Fab Coefficient</ENTITLEMENT_NAME>''))+''</QUOTE_ENTITLEMENT>'') as entitlement_xml FROM SAQSCE (nolock)a JOIN "+str(CRMTMP)+" C ON A.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND SERVICE_ID = ''Z0092'') e OUTER APPLY e.ENTITLEMENT_XML.nodes(''QUOTE_ENTITLEMENT'') as X(Y) )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID  WHERE B.ENTITLEMENT_NAME=''#CSA Tools per Fab Coefficient'' AND ISNULL(ENTITLEMENT_VALUE_CODE,'''') <>''''  '")
							
							#Z0004
							S3 = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET TOTAL_COEFFICIENT= ISNULL(TOTAL_COEFFICIENT,0) + ISNULL(CONVERT(FLOAT,ENTITLEMENT_VALUE_CODE),0) FROM SAQICO_INBOUND A(NOLOCK) JOIN (SELECT distinct quote_ID,equipment_id,service_id, replace(X.Y.value(''(ENTITLEMENT_VALUE_CODE)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_VALUE_CODE,replace(X.Y.value(''(ENTITLEMENT_NAME)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_NAME FROM (SELECT quote_ID,equipment_id,service_id,CONVERT(XML,''<QUOTE_ENTITLEMENT>''+substring(entitlement_xml,charindex (''<ENTITLEMENT_ID>AGS_Z0004_VAL_TLSFCO'',entitlement_xml),charindex (''#CSA Tools per Fab Coefficient</ENTITLEMENT_NAME>'',entitlement_xml)-charindex (''<ENTITLEMENT_ID>AGS_Z0004_VAL_TLSFCO'',entitlement_xml)+len(''#CSA Tools per Fab Coefficient</ENTITLEMENT_NAME>''))+''</QUOTE_ENTITLEMENT>'') as entitlement_xml FROM SAQSCE (nolock)a JOIN "+str(CRMTMP)+" C ON A.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND SERVICE_ID = ''Z0004'') e OUTER APPLY e.ENTITLEMENT_XML.nodes(''QUOTE_ENTITLEMENT'') as X(Y) )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID  WHERE B.ENTITLEMENT_NAME=''#CSA Tools per Fab Coefficient'' AND ISNULL(ENTITLEMENT_VALUE_CODE,'''') <>''''  '")
							
							#Z0099
							S3 = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET TOTAL_COEFFICIENT= ISNULL(TOTAL_COEFFICIENT,0) + ISNULL(CONVERT(FLOAT,ENTITLEMENT_VALUE_CODE),0) FROM SAQICO_INBOUND A(NOLOCK) JOIN (SELECT distinct quote_ID,equipment_id,service_id, replace(X.Y.value(''(ENTITLEMENT_VALUE_CODE)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_VALUE_CODE,replace(X.Y.value(''(ENTITLEMENT_NAME)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_NAME FROM (SELECT quote_ID,equipment_id,service_id,CONVERT(XML,''<QUOTE_ENTITLEMENT>''+substring(entitlement_xml,charindex (''<ENTITLEMENT_ID>AGS_Z0099_VAL_TLSFCO'',entitlement_xml),charindex (''#CSA Tools per Fab Coefficient</ENTITLEMENT_NAME>'',entitlement_xml)-charindex (''<ENTITLEMENT_ID>AGS_Z0099_VAL_TLSFCO'',entitlement_xml)+len(''#CSA Tools per Fab Coefficient</ENTITLEMENT_NAME>''))+''</QUOTE_ENTITLEMENT>'') as entitlement_xml FROM SAQSCE (nolock)a JOIN "+str(CRMTMP)+" C ON A.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND SERVICE_ID = ''Z0099'') e OUTER APPLY e.ENTITLEMENT_XML.nodes(''QUOTE_ENTITLEMENT'') as X(Y) )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID  WHERE B.ENTITLEMENT_NAME=''#CSA Tools per Fab Coefficient'' AND ISNULL(ENTITLEMENT_VALUE_CODE,'''') <>''''  '")
							
							CRMTMP21 = SqlHelper.GetFirst("sp_executesql @T=N'DELETE FROM "+str(CRMTMP)+" ' ")	
						else:
							Check_flag12=0
					
					#Entitlement Roll Up
					S3 = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET ENTITLEMENT_XML= B.ENTITLEMENT_XML FROM SAQSCE A(NOLOCK) JOIN SAQIEN B(NOLOCK) ON A.QUOTE_ID = B.QUOTE_ID AND A.QTEREV_ID = B.QTEREV_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID WHERE A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"''   '")
					
					#SSCM Coefficient
					S3 = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET TOTAL_COEFFICIENT= ISNULL(TOTAL_COEFFICIENT,0) + ISNULL(CONVERT(FLOAT,NPI_COEFFICIENT),0)+ ISNULL(CONVERT(FLOAT,SERVICECOMPLEXITY_COEFFICIENT),0) + ISNULL(CONVERT(FLOAT,CAPITALAVOIDANCE_COEFFICIENT),0) FROM SAQICO_INBOUND A(NOLOCK) WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND REVISION_ID = ''"+str(Qt_Id.REVISION_ID)+"''   '")
					
					#Total Cost Entitlement Impact
					primaryQueryItems = SqlHelper.GetFirst(
						""
						+ str(Parameter1.QUERY_CRITERIA_1)
						+ "  SAQICO SET TOTAL_COST_WSEEDSTOCK = TOTAL_COST_WSEEDSTOCK + ISNULL(ENTITLEMENT_COST_IMPACT,0) FROM SAQICO A(NOLOCK) JOIN (SELECT DISTINCT QUOTE_ID,SERVICE_ID,EQUIPMENT_ID,REVISION_ID FROM SAQICO_INBOUND(NOLOCK)  WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND QTEREV_ID = REVISION_ID  ' ")
											
					#Model Price
					primaryQueryItems = SqlHelper.GetFirst(
						""
						+ str(Parameter1.QUERY_CRITERIA_1)
						+ "  SAQICO SET MODEL_PRICE = EXP(ISNULL(INTERCEPT,0) + (LOG(TOTAL_COST_WOSEEDSTOCK)) * ISNULL(LOG_FACTOR,1) + ISNULL(TOTAL_COEFFICIENT,0) )  FROM SAQICO (NOLOCK)A JOIN (SELECT DISTINCT QUOTE_ID,SERVICE_ID,EQUIPMENT_ID,TOTAL_COEFFICIENT,INTERCEPT,LOG_FACTOR,REVISION_ID FROM SAQICO_INBOUND(NOLOCK)  WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND QTEREV_ID = REVISION_ID WHERE A.GREENBOOK<>''PDC'' AND ISNULL(TOTAL_COST_WOSEEDSTOCK,0)>0  ' ")
						
					#Contract Coverage + Model Price 
					#Z0091
					S3 = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET MODEL_PRICE = MODEL_PRICE * (1 + ISNULL(CONVERT(FLOAT,ENTITLEMENT_VALUE_CODE),0) ) FROM SAQICO A(NOLOCK) JOIN (SELECT distinct quote_ID,equipment_id,service_id,QTEREV_ID, replace(X.Y.value(''(ENTITLEMENT_VALUE_CODE)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_VALUE_CODE,replace(X.Y.value(''(ENTITLEMENT_DESCRIPTION)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_DESCRIPTION FROM (SELECT quote_ID,equipment_id,service_id,QTEREV_ID,CONVERT(XML,REPLACE(''<QUOTE_ENTITLEMENT>''+substring(entitlement_xml,charindex (''<ENTITLEMENT_ID>AGS_Z0091_VAL_CCRTCO'',entitlement_xml),charindex (''Contract Coverage & Response Time Coefficient</ENTITLEMENT_DESCRIPTION>'',entitlement_xml)-charindex (''<ENTITLEMENT_ID>AGS_Z0091_VAL_CCRTCO'',entitlement_xml)+len(''Contract Coverage & Response Time Coefficient</ENTITLEMENT_DESCRIPTION>''))+''</QUOTE_ENTITLEMENT>'',''Contract Coverage & Response Time Coefficient'',''Contract Cov'')) as entitlement_xml FROM SAQSCE (nolock)a WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND SERVICE_ID = ''Z0091'' AND ENTITLEMENT_XML LIKE ''%%Contract Coverage & Response Time Coefficient%%'' ) e OUTER APPLY e.ENTITLEMENT_XML.nodes(''QUOTE_ENTITLEMENT'') as X(Y) )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.QTEREV_ID = B.QTEREV_ID  WHERE B.ENTITLEMENT_DESCRIPTION=''Contract Cov'' AND ISNULL(ENTITLEMENT_VALUE_CODE,'''') <>''''  '")
					
					#Z0092
					S3 = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET MODEL_PRICE = MODEL_PRICE * (1 + ISNULL(CONVERT(FLOAT,ENTITLEMENT_VALUE_CODE),0) ) FROM SAQICO A(NOLOCK) JOIN (SELECT distinct quote_ID,equipment_id,service_id,QTEREV_ID, replace(X.Y.value(''(ENTITLEMENT_VALUE_CODE)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_VALUE_CODE,replace(X.Y.value(''(ENTITLEMENT_DESCRIPTION)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_DESCRIPTION FROM (SELECT quote_ID,equipment_id,service_id,QTEREV_ID,CONVERT(XML,REPLACE(''<QUOTE_ENTITLEMENT>''+substring(entitlement_xml,charindex (''<ENTITLEMENT_ID>AGS_Z0092_VAL_CCRTCO'',entitlement_xml),charindex (''Contract Coverage & Response Time Coefficient</ENTITLEMENT_DESCRIPTION>'',entitlement_xml)-charindex (''<ENTITLEMENT_ID>AGS_Z0092_VAL_CCRTCO'',entitlement_xml)+len(''Contract Coverage & Response Time Coefficient</ENTITLEMENT_DESCRIPTION>''))+''</QUOTE_ENTITLEMENT>'',''Contract Coverage & Response Time Coefficient'',''Contract Cov'')) as entitlement_xml FROM SAQSCE (nolock)a WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND SERVICE_ID = ''Z0092'' AND ENTITLEMENT_XML LIKE ''%%Contract Coverage & Response Time Coefficient%%'' ) e OUTER APPLY e.ENTITLEMENT_XML.nodes(''QUOTE_ENTITLEMENT'') as X(Y) )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.QTEREV_ID = B.QTEREV_ID  WHERE B.ENTITLEMENT_DESCRIPTION=''Contract Cov'' AND ISNULL(ENTITLEMENT_VALUE_CODE,'''') <>''''  '")
					
					#Z0004
					S3 = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET MODEL_PRICE = MODEL_PRICE * (1 + ISNULL(CONVERT(FLOAT,ENTITLEMENT_VALUE_CODE),0) ) FROM SAQICO A(NOLOCK) JOIN (SELECT distinct quote_ID,equipment_id,service_id,QTEREV_ID, replace(X.Y.value(''(ENTITLEMENT_VALUE_CODE)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_VALUE_CODE,replace(X.Y.value(''(ENTITLEMENT_DESCRIPTION)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_DESCRIPTION FROM (SELECT quote_ID,equipment_id,service_id,QTEREV_ID,CONVERT(XML,REPLACE(''<QUOTE_ENTITLEMENT>''+substring(entitlement_xml,charindex (''<ENTITLEMENT_ID>AGS_Z0004_VAL_CCRTCO'',entitlement_xml),charindex (''Contract Coverage & Response Time Coefficient</ENTITLEMENT_DESCRIPTION>'',entitlement_xml)-charindex (''<ENTITLEMENT_ID>AGS_Z0004_VAL_CCRTCO'',entitlement_xml)+len(''Contract Coverage & Response Time Coefficient</ENTITLEMENT_DESCRIPTION>''))+''</QUOTE_ENTITLEMENT>'',''Contract Coverage & Response Time Coefficient'',''Contract Cov'')) as entitlement_xml FROM SAQSCE (nolock)a WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND SERVICE_ID = ''Z0004'' AND ENTITLEMENT_XML LIKE ''%%Contract Coverage & Response Time Coefficient%%'' ) e OUTER APPLY e.ENTITLEMENT_XML.nodes(''QUOTE_ENTITLEMENT'') as X(Y) )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.QTEREV_ID = B.QTEREV_ID  WHERE B.ENTITLEMENT_DESCRIPTION=''Contract Cov'' AND ISNULL(ENTITLEMENT_VALUE_CODE,'''') <>''''  '")
					
					#Z0099
					S3 = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET MODEL_PRICE = MODEL_PRICE * (1 + ISNULL(CONVERT(FLOAT,ENTITLEMENT_VALUE_CODE),0) ) FROM SAQICO A(NOLOCK) JOIN (SELECT distinct quote_ID,equipment_id,service_id,QTEREV_ID, replace(X.Y.value(''(ENTITLEMENT_VALUE_CODE)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_VALUE_CODE,replace(X.Y.value(''(ENTITLEMENT_DESCRIPTION)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_DESCRIPTION FROM (SELECT quote_ID,equipment_id,service_id,QTEREV_ID,CONVERT(XML,REPLACE(''<QUOTE_ENTITLEMENT>''+substring(entitlement_xml,charindex (''<ENTITLEMENT_ID>AGS_Z0099_VAL_CCRTCO'',entitlement_xml),charindex (''Contract Coverage & Response Time Coefficient</ENTITLEMENT_DESCRIPTION>'',entitlement_xml)-charindex (''<ENTITLEMENT_ID>AGS_Z0099_VAL_CCRTCO'',entitlement_xml)+len(''Contract Coverage & Response Time Coefficient</ENTITLEMENT_DESCRIPTION>''))+''</QUOTE_ENTITLEMENT>'',''Contract Coverage & Response Time Coefficient'',''Contract Cov'')) as entitlement_xml FROM SAQSCE (nolock)a WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND SERVICE_ID = ''Z0099'' AND ENTITLEMENT_XML LIKE ''%%Contract Coverage & Response Time Coefficient%%'' ) e OUTER APPLY e.ENTITLEMENT_XML.nodes(''QUOTE_ENTITLEMENT'') as X(Y) )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.QTEREV_ID = B.QTEREV_ID  WHERE B.ENTITLEMENT_DESCRIPTION=''Contract Cov'' AND ISNULL(ENTITLEMENT_VALUE_CODE,'''') <>''''  '")
					
					#Model Price Entitlement Price Impact
					primaryQueryItems = SqlHelper.GetFirst(
						""
						+ str(Parameter1.QUERY_CRITERIA_1)
						+ "  A SET MODEL_PRICE = MODEL_PRICE + ISNULL(ENTPRCIMP_INGL_CURR,0) FROM SAQICO A(NOLOCK) JOIN (SELECT DISTINCT QUOTE_ID,SERVICE_ID,EQUIPMENT_ID,REVISION_ID FROM SAQICO_INBOUND(NOLOCK)  WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND QTEREV_ID = REVISION_ID ' ")
										
					
					start13 = 1
					end13 = 500

					Check_flag13 = 1
					while Check_flag13 == 1:

						table13 = SqlHelper.GetFirst(
									"SELECT DISTINCT equipment_id FROM (SELECT DISTINCT equipment_id, ROW_NUMBER()OVER(ORDER BY equipment_id) AS SNO FROM (SELECT DISTINCT equipment_id FROM SAQICO_INBOUND (NOLOCK) WHERE ISNULL(PROCESS_STATUS,'')='INPROGRESS' AND TIMESTAMP = "+str(timestamp_sessionid)+" )A) A WHERE SNO>= "+str(start13)+" AND SNO<="+str(end13)+""
								)
								
						CRMTMP13 = SqlHelper.GetFirst("sp_executesql @T=N'IF NOT EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(CRMTMP)+"'' ) BEGIN CREATE TABLE "+str(CRMTMP)+" (EQUIPMENT_IDD VARCHAR(100)) END  ' ")
						
						table_insert = SqlHelper.GetFirst(
							"sp_executesql @T=N'INSERT "+str(CRMTMP)+" SELECT DISTINCT equipment_id FROM (SELECT DISTINCT equipment_id, ROW_NUMBER()OVER(ORDER BY equipment_id) AS SNO FROM (SELECT DISTINCT equipment_id FROM SAQICO_INBOUND (NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' )A ) A WHERE SNO>= "+str(start13)+" AND SNO<="+str(end13)+"  '")
						
						start13 = start13 + 500
						end13 = end13 + 500

						if str(table13) != "None":
						
							#Head Break In
							S3 = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET TOTAL_COST_WSEEDSTOCK = TOTAL_COST_WSEEDSTOCK + (ISNULL(CONVERT(FLOAT,C.FACTOR_TXTVAR),0) * ISNULL(HEAD_REBUILD_QTY,0) )  FROM SAQICO A(NOLOCK) JOIN (SELECT distinct quote_ID,equipment_id,service_id,QTEREV_ID, replace(X.Y.value(''(ENTITLEMENT_VALUE_CODE)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_VALUE_CODE,replace(X.Y.value(''(ENTITLEMENT_NAME)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_NAME FROM (SELECT A.quote_ID,A.equipment_id,A.service_id,A.QTEREV_ID,CONVERT(XML,''<QUOTE_ENTITLEMENT>''+substring(entitlement_xml,charindex (''<ENTITLEMENT_ID>AGS_Z0091_STT_HDBRIN'',entitlement_xml),charindex (''Head break-in</ENTITLEMENT_NAME>'',entitlement_xml)-charindex (''<ENTITLEMENT_ID>AGS_Z0091_STT_HDBRIN'',entitlement_xml)+len(''Head break-in</ENTITLEMENT_NAME>''))+''</QUOTE_ENTITLEMENT>'') as entitlement_xml FROM SAQSCE  (nolock)A JOIN "+str(CRMTMP)+" C ON A.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND A.SERVICE_ID = ''Z0091'' ) e OUTER APPLY e.ENTITLEMENT_XML.nodes(''QUOTE_ENTITLEMENT'') as X(Y) )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.QTEREV_ID = B.QTEREV_ID JOIN MAEQUP (NOLOCK) ON A.EQUIPMENT_ID  = MAEQUP.EQUIPMENT_ID JOIN PRCFVA C(NOLOCK) ON MAEQUP.SUBSTRATE_SIZE_GROUP = C.FACTOR_VARIABLE_ID WHERE B.ENTITLEMENT_NAME=''Head break-in'' AND ISNULL(B.ENTITLEMENT_VALUE_CODE,'''') = ''002'' AND C.FACTOR_ID  = ''HBWFCT''  '")
							
							S3 = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET MODEL_PRICE = MODEL_PRICE + (ISNULL(CONVERT(FLOAT,C.FACTOR_TXTVAR),0) * ISNULL(HEAD_REBUILD_QTY,0))   FROM SAQICO A(NOLOCK) JOIN (SELECT distinct quote_ID,equipment_id,service_id,QTEREV_ID, replace(X.Y.value(''(ENTITLEMENT_VALUE_CODE)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_VALUE_CODE,replace(X.Y.value(''(ENTITLEMENT_NAME)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_NAME FROM (SELECT A.quote_ID,A.equipment_id,A.service_id,A.QTEREV_ID,CONVERT(XML,''<QUOTE_ENTITLEMENT>''+substring(entitlement_xml,charindex (''<ENTITLEMENT_ID>AGS_Z0091_STT_HDBRIN'',entitlement_xml),charindex (''Head break-in</ENTITLEMENT_NAME>'',entitlement_xml)-charindex (''<ENTITLEMENT_ID>AGS_Z0091_STT_HDBRIN'',entitlement_xml)+len(''Head break-in</ENTITLEMENT_NAME>''))+''</QUOTE_ENTITLEMENT>'') as entitlement_xml FROM SAQSCE (nolock)A JOIN "+str(CRMTMP)+" C ON A.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND A.SERVICE_ID = ''Z0091'' ) e OUTER APPLY e.ENTITLEMENT_XML.nodes(''QUOTE_ENTITLEMENT'') as X(Y) )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.QTEREV_ID = B.QTEREV_ID JOIN MAEQUP (NOLOCK) ON A.EQUIPMENT_ID  = MAEQUP.EQUIPMENT_ID JOIN PRCFVA C(NOLOCK) ON MAEQUP.SUBSTRATE_SIZE_GROUP = C.FACTOR_VARIABLE_ID WHERE B.ENTITLEMENT_NAME=''Head break-in'' AND ISNULL(B.ENTITLEMENT_VALUE_CODE,'''') = ''002'' AND C.FACTOR_ID  = ''HBWFPR''  '")
							
							#Application Engineering
							S3 = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET MODEL_PRICE = MODEL_PRICE + ISNULL(CONVERT(FLOAT,C.ENTITLEMENT_PRICE_IMPACT),0) , TOTAL_COST_WSEEDSTOCK = TOTAL_COST_WSEEDSTOCK + ISNULL(CONVERT(FLOAT,C.ENTITLEMENT_COST_IMPACT),0)  FROM SAQICO A(NOLOCK) JOIN (SELECT distinct quote_ID,equipment_id,service_id,QTEREV_ID, replace(X.Y.value(''(ENTITLEMENT_VALUE_CODE)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_VALUE_CODE,replace(X.Y.value(''(ENTITLEMENT_NAME)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_NAME FROM (SELECT A.quote_ID,A.equipment_id,A.service_id,A.QTEREV_ID,CONVERT(XML,''<QUOTE_ENTITLEMENT>''+substring(entitlement_xml,charindex (''<ENTITLEMENT_ID>AGS_Z0091_NET_NUMLAY'',entitlement_xml),charindex (''Number of Layers</ENTITLEMENT_NAME>'',entitlement_xml)-charindex (''<ENTITLEMENT_ID>AGS_Z0091_NET_NUMLAY'',entitlement_xml)+len(''Number of Layers</ENTITLEMENT_NAME>''))+''</QUOTE_ENTITLEMENT>'') as entitlement_xml FROM SAQSCE (nolock)A JOIN "+str(CRMTMP)+" C ON A.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND A.SERVICE_ID = ''Z0091'' ) e OUTER APPLY e.ENTITLEMENT_XML.nodes(''QUOTE_ENTITLEMENT'') as X(Y) )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.QTEREV_ID = B.QTEREV_ID JOIN PREGBV C(NOLOCK) ON B.ENTITLEMENT_NAME = C.ENTITLEMENT_NAME AND B.ENTITLEMENT_VALUE_CODE = C.ENTITLEMENT_VALUE_CODE WHERE B.ENTITLEMENT_NAME=''Number of Layers'' AND ISNULL(B.ENTITLEMENT_VALUE_CODE,'''') <>''''  '")
							
							#Specialized Coating
							S3 = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET TOTAL_COST_WSEEDSTOCK = TOTAL_COST_WSEEDSTOCK +  ( ISNULL(CONVERT(FLOAT,C.ENTITLEMENT_COST_IMPACT),0) * ISNULL(HEAD_REBUILD_QTY,0) ), MODEL_PRICE = MODEL_PRICE + (ISNULL(CONVERT(FLOAT,C.ENTITLEMENT_PRICE_IMPACT),0)  * ISNULL(HEAD_REBUILD_QTY,0) )   FROM SAQICO A(NOLOCK) JOIN (SELECT distinct quote_ID,equipment_id,service_id,QTEREV_ID, replace(X.Y.value(''(ENTITLEMENT_VALUE_CODE)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_VALUE_CODE,replace(X.Y.value(''(ENTITLEMENT_NAME)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_NAME FROM (SELECT A.quote_ID,A.equipment_id,A.service_id,A.QTEREV_ID,CONVERT(XML,''<QUOTE_ENTITLEMENT>''+substring(entitlement_xml,charindex (''<ENTITLEMENT_ID>AGS_Z0091_STT_SPCCOT'',entitlement_xml),charindex (''Specialized Coating</ENTITLEMENT_NAME>'',entitlement_xml)-charindex (''<ENTITLEMENT_ID>AGS_Z0091_STT_SPCCOT'',entitlement_xml)+len(''Specialized Coating</ENTITLEMENT_NAME>''))+''</QUOTE_ENTITLEMENT>'') as entitlement_xml FROM SAQSCE (nolock)A JOIN "+str(CRMTMP)+" C ON A.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND A.SERVICE_ID = ''Z0091'' ) e OUTER APPLY e.ENTITLEMENT_XML.nodes(''QUOTE_ENTITLEMENT'') as X(Y) )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.QTEREV_ID = B.QTEREV_ID JOIN PREGBV C(NOLOCK) ON B.ENTITLEMENT_NAME = C.ENTITLEMENT_NAME AND B.ENTITLEMENT_VALUE_CODE = C.ENTITLEMENT_VALUE_CODE WHERE B.ENTITLEMENT_NAME=''Specialized Coating'' AND ISNULL(C.ENTITLEMENT_DISPLAY_VALUE,'''') = ''Included''  '")
							
							#Specialized Cleaning					
							S3 = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET TOTAL_COST_WSEEDSTOCK = TOTAL_COST_WSEEDSTOCK + (ISNULL(CONVERT(FLOAT,C.ENTITLEMENT_COST_IMPACT),0) * ISNULL(HEAD_REBUILD_QTY,0)), MODEL_PRICE = MODEL_PRICE + (ISNULL(CONVERT(FLOAT,C.ENTITLEMENT_PRICE_IMPACT),0)  * ISNULL(HEAD_REBUILD_QTY,0) )   FROM SAQICO A(NOLOCK) JOIN (SELECT distinct quote_ID,equipment_id,service_id,QTEREV_ID, replace(X.Y.value(''(ENTITLEMENT_VALUE_CODE)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_VALUE_CODE,replace(X.Y.value(''(ENTITLEMENT_NAME)[1]'', ''VARCHAR(128)''),'';#38'',''&'') as ENTITLEMENT_NAME FROM (SELECT A.quote_ID,A.equipment_id,A.service_id,A.QTEREV_ID,CONVERT(XML,''<QUOTE_ENTITLEMENT>''+substring(entitlement_xml,charindex (''<ENTITLEMENT_ID>AGS_Z0091_STT_SPCCLN'',entitlement_xml),charindex (''Specialized Cleaning</ENTITLEMENT_NAME>'',entitlement_xml)-charindex (''<ENTITLEMENT_ID>AGS_Z0091_STT_SPCCLN'',entitlement_xml)+len(''Specialized Cleaning</ENTITLEMENT_NAME>''))+''</QUOTE_ENTITLEMENT>'') as entitlement_xml FROM SAQSCE  (nolock)A JOIN "+str(CRMTMP)+" C ON A.EQUIPMENT_ID = C.EQUIPMENT_IDD WHERE A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND A.SERVICE_ID = ''Z0091'' ) e OUTER APPLY e.ENTITLEMENT_XML.nodes(''QUOTE_ENTITLEMENT'') as X(Y) )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.QTEREV_ID = B.QTEREV_ID JOIN PREGBV C(NOLOCK) ON B.ENTITLEMENT_NAME = C.ENTITLEMENT_NAME AND B.ENTITLEMENT_VALUE_CODE = C.ENTITLEMENT_VALUE_CODE WHERE B.ENTITLEMENT_NAME=''Specialized Cleaning'' AND ISNULL(C.ENTITLEMENT_DISPLAY_VALUE,'''') = ''Included''  '")
							
							CRMTMP31 = SqlHelper.GetFirst("sp_executesql @T=N'DELETE FROM "+str(CRMTMP)+" ' ")
						
						else:
							Check_flag13 = 0

					#Price Margin 
					primaryQueryItems = SqlHelper.GetFirst(
						""
						+ str(Parameter1.QUERY_CRITERIA_1)
						+ "  A SET TARGET_PRICE_MARGIN= FACTOR_TXTVAR,TARGET_PRICE_MARGIN_RECORD_ID = CALCULATION_VARIABLE_RECORD_ID FROM SAQICO (NOLOCK)A JOIN PRCFVA B(NOLOCK) ON A.SERVICE_ID = B.FACTOR_VARIABLE_ID WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND FACTOR_ID=''TGMRGN'' AND TARGET_PRICE_MARGIN IS NULL ' ")
					
					primaryQueryItems = SqlHelper.GetFirst(
						""
						+ str(Parameter1.QUERY_CRITERIA_1)
						+ "  A SET SLSDIS_PRICE_MARGIN= FACTOR_TXTVAR,SLSDIS_PRICE_MARGIN_RECORD_ID=CALCULATION_VARIABLE_RECORD_ID FROM SAQICO (NOLOCK)A JOIN PRCFVA B(NOLOCK) ON A.SERVICE_ID = B.FACTOR_VARIABLE_ID WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND FACTOR_ID=''SLMRGN'' AND SLSDIS_PRICE_MARGIN IS NULL ' ")
					
					primaryQueryItems = SqlHelper.GetFirst(
						""
						+ str(Parameter1.QUERY_CRITERIA_1)
						+ "  A SET BD_PRICE_MARGIN= FACTOR_TXTVAR,BD_PRICE_MARGIN_RECORD_ID=CALCULATION_VARIABLE_RECORD_ID FROM SAQICO (NOLOCK)A JOIN PRCFVA B(NOLOCK) ON A.SERVICE_ID = B.FACTOR_VARIABLE_ID WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND FACTOR_ID=''BDMRGN'' AND BD_PRICE_MARGIN IS NULL ' ")
					
					primaryQueryItems = SqlHelper.GetFirst(
						""
						+ str(Parameter1.QUERY_CRITERIA_1)
						+ "  A SET CEILING_PRICE_MARGIN= FACTOR_TXTVAR,CEILING_PRICE_MARGIN_RECORD_ID=CALCULATION_VARIABLE_RECORD_ID FROM SAQICO (NOLOCK)A JOIN PRCFVA B(NOLOCK) ON A.SERVICE_ID = B.FACTOR_VARIABLE_ID WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND FACTOR_ID=''CEMRGN'' AND CEILING_PRICE_MARGIN IS NULL ' ")
					
					primaryQueryItems = SqlHelper.GetFirst(
						""
						+ str(Parameter1.QUERY_CRITERIA_1)
						+ "  A SET SALDIS_PERCENT= FACTOR_TXTVAR FROM SAQICO (NOLOCK)A JOIN PRCFVA B(NOLOCK) ON A.SERVICE_ID = B.FACTOR_VARIABLE_ID WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND FACTOR_ID=''SLDISC'' AND SALDIS_PERCENT IS NULL ' ")
					
					primaryQueryItems = SqlHelper.GetFirst(
						""
						+ str(Parameter1.QUERY_CRITERIA_1)
						+ "  A SET BD_DISCOUNT= FACTOR_TXTVAR,BD_DISCOUNT_RECORD_ID=CALCULATION_VARIABLE_RECORD_ID FROM SAQICO (NOLOCK)A JOIN PRCFVA B(NOLOCK) ON A.SERVICE_ID = B.FACTOR_VARIABLE_ID WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND FACTOR_ID=''BDDISC'' AND BD_DISCOUNT IS NULL ' ")

					#Target Price
					primaryQueryItems = SqlHelper.GetFirst(
						""
						+ str(Parameter1.QUERY_CRITERIA_1)
						+ "  A SET TARGET_PRICE = CASE WHEN ISNULL(MODEL_PRICE/(1-(CONVERT(FLOAT,SALDIS_PERCENT)/100)),0) > ISNULL(TOTAL_COST_WSEEDSTOCK / (1-(TARGET_PRICE_MARGIN/100)),0) THEN ISNULL(MODEL_PRICE/(1-(CONVERT(FLOAT,SALDIS_PERCENT)/100)),0) ELSE ISNULL(TOTAL_COST_WSEEDSTOCK / (1-(TARGET_PRICE_MARGIN/100)),0) END FROM SAQICO (NOLOCK)A JOIN (SELECT DISTINCT QUOTE_ID,REVISION_ID,SERVICE_ID,EQUIPMENT_ID FROM SAQICO_INBOUND(NOLOCK)  WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"')B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND QTEREV_ID = REVISION_ID ' ")
					
					#Sale Discounted Price
					primaryQueryItems = SqlHelper.GetFirst(
						""
						+ str(Parameter1.QUERY_CRITERIA_1)
						+ "  A SET SALES_DISCOUNT_PRICE = CASE WHEN ISNULL(MODEL_PRICE,0) > ISNULL(TOTAL_COST_WSEEDSTOCK / (1-(CONVERT(FLOAT,SLSDIS_PRICE_MARGIN)/100)),0) THEN ISNULL(MODEL_PRICE,0) ELSE ISNULL(TOTAL_COST_WSEEDSTOCK / (1-(CONVERT(FLOAT,SLSDIS_PRICE_MARGIN)/100)),0) END FROM SAQICO (NOLOCK)A JOIN (SELECT DISTINCT QUOTE_ID,REVISION_ID,SERVICE_ID,EQUIPMENT_ID FROM SAQICO_INBOUND(NOLOCK)  WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"')B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND QTEREV_ID = REVISION_ID ' ")
					
					#BD Price
					primaryQueryItems = SqlHelper.GetFirst(
						""
						+ str(Parameter1.QUERY_CRITERIA_1)
						+ "  A SET BD_PRICE = CASE WHEN ISNULL(MODEL_PRICE * (1-(CONVERT(FLOAT,BD_DISCOUNT)/100)) ,0) > ISNULL(TOTAL_COST_WSEEDSTOCK / (1-(CONVERT(FLOAT,BD_PRICE_MARGIN)/100)),0) THEN ISNULL(MODEL_PRICE * (1-(CONVERT(FLOAT,BD_DISCOUNT)/100)) ,0) ELSE ISNULL(TOTAL_COST_WSEEDSTOCK / (1-(CONVERT(FLOAT,BD_PRICE_MARGIN)/100)),0) END FROM SAQICO (NOLOCK)A JOIN (SELECT DISTINCT QUOTE_ID,SERVICE_ID,EQUIPMENT_ID,REVISION_ID FROM SAQICO_INBOUND(NOLOCK)  WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"')B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND QTEREV_ID = REVISION_ID ' ")
					
					#Ceiling Price
					primaryQueryItems = SqlHelper.GetFirst(
						""
						+ str(Parameter1.QUERY_CRITERIA_1)
						+ "  A SET CEILING_PRICE = TARGET_PRICE * (1 + (CONVERT(FLOAT,CEILING_PRICE_MARGIN)/100)) FROM SAQICO (NOLOCK)A JOIN (SELECT DISTINCT  QUOTE_ID,SERVICE_ID,EQUIPMENT_ID,REVISION_ID FROM SAQICO_INBOUND(NOLOCK)  WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"')B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND QTEREV_ID = REVISION_ID ' ")
					
					#Global Currency
					primaryQueryItems = SqlHelper.GetFirst(
						""
						+ str(Parameter1.QUERY_CRITERIA_1)
						+ "  A SET BD_PRICE_INGL_CURR = BD_PRICE,CEILING_PRICE_INGL_CURR  = CEILING_PRICE,MODEL_PRICE_INGL_CURR = MODEL_PRICE,SLSDIS_PRICE_INGL_CURR = SALES_DISCOUNT_PRICE,TARGET_PRICE_INGL_CURR = TARGET_PRICE FROM SAQICO (NOLOCK)A JOIN (SELECT DISTINCT  QUOTE_ID,SERVICE_ID,EQUIPMENT_ID,REVISION_ID FROM SAQICO_INBOUND(NOLOCK)  WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"')B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND QTEREV_ID = REVISION_ID ' ")
						
					#Exchange Rate
					primaryQueryItems = SqlHelper.GetFirst(
						""
						+ str(Parameter1.QUERY_CRITERIA_1)
						+ "  A SET TARGET_PRICE = ROUND( (TARGET_PRICE * ISNULL(EXCHANGE_RATE,1)) ,CONVERT(INT,"+str(roundcurr.DECIMAL_PLACES)+"),CONVERT(INT,"+str(roundcurr.ROUNDING_METHOD)+")), SALES_DISCOUNT_PRICE = ROUND( (SALES_DISCOUNT_PRICE * ISNULL(EXCHANGE_RATE,1)) ,CONVERT(INT,"+str(roundcurr.DECIMAL_PLACES)+"),CONVERT(INT,"+str(roundcurr.ROUNDING_METHOD)+")), BD_PRICE = ROUND( (BD_PRICE * ISNULL(EXCHANGE_RATE,1)) ,CONVERT(INT,"+str(roundcurr.DECIMAL_PLACES)+"),CONVERT(INT,"+str(roundcurr.ROUNDING_METHOD)+")), CEILING_PRICE = ROUND( (CEILING_PRICE * ISNULL(EXCHANGE_RATE,1)) ,CONVERT(INT,"+str(roundcurr.DECIMAL_PLACES)+"),CONVERT(INT,"+str(roundcurr.ROUNDING_METHOD)+")),MODEL_PRICE = ROUND( (MODEL_PRICE * ISNULL(EXCHANGE_RATE,1)) ,CONVERT(INT,"+str(roundcurr.DECIMAL_PLACES)+"),CONVERT(INT,"+str(roundcurr.ROUNDING_METHOD)+"))  FROM SAQICO (NOLOCK)A JOIN (SELECT DISTINCT QUOTE_ID,SERVICE_ID,EQUIPMENT_ID,REVISION_ID FROM SAQICO_INBOUND(NOLOCK)  WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"')B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND QTEREV_ID = REVISION_ID ' ")
					
					
					#Sales Price
					primaryQueryItems = SqlHelper.GetFirst(
						""
						+ str(Parameter1.QUERY_CRITERIA_1)
						+ "  A SET NET_PRICE = TARGET_PRICE - (TARGET_PRICE * (ISNULL(DISCOUNT,0)/100)),NET_PRICE_INGL_CURR = TARGET_PRICE_INGL_CURR  FROM SAQICO (NOLOCK)A JOIN (SELECT DISTINCT QUOTE_ID,SERVICE_ID,EQUIPMENT_ID,REVISION_ID FROM SAQICO_INBOUND(NOLOCK)  WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"')B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID  AND QTEREV_ID = REVISION_ID ' ")
					
					#Contract Year
					primaryQueryItems = SqlHelper.GetFirst(
						""
						+ str(Parameter1.QUERY_CRITERIA_1)
						+ "  SAQICO_INBOUND SET YEAR_PERIOD = datediff(yy,contract_valid_from,contract_valid_to)  FROM SAQICO_INBOUND (NOLOCK)  JOIN SAQTMT (NOLOCK) ON SAQICO_INBOUND.QUOTE_ID = SAQTMT.QUOTE_ID WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  ' ")
						
					#Year 1
					primaryQueryItems = SqlHelper.GetFirst(
						""
						+ str(Parameter1.QUERY_CRITERIA_1)
						+ "  A SET YEAR_1 = NET_PRICE,YEAR_1_INGL_CURR = NET_PRICE_INGL_CURR   FROM SAQICO (NOLOCK)A JOIN (SELECT DISTINCT QUOTE_ID,SERVICE_ID,EQUIPMENT_ID,REVISION_ID FROM SAQICO_INBOUND(NOLOCK)  WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"')B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID  AND QTEREV_ID = REVISION_ID ' ")
					
					#Year 2
					primaryQueryItems = SqlHelper.GetFirst(
						""
						+ str(Parameter1.QUERY_CRITERIA_1)
						+ "  A SET YEAR_2 =YEAR_1 - ( YEAR_1 * (YEAR_OVER_YEAR/100) ) , YEAR_2_INGL_CURR = YEAR_1_INGL_CURR - ( YEAR_1_INGL_CURR * (YEAR_OVER_YEAR/100) )  FROM SAQICO (NOLOCK)A JOIN (SELECT DISTINCT QUOTE_ID,SERVICE_ID,EQUIPMENT_ID,YEAR_PERIOD,REVISION_ID FROM SAQICO_INBOUND(NOLOCK)  WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"')B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND QTEREV_ID = REVISION_ID WHERE YEAR_PERIOD>=2  ' ")
					
					#Year 3
					primaryQueryItems = SqlHelper.GetFirst(
						""
						+ str(Parameter1.QUERY_CRITERIA_1)
						+ "  A SET YEAR_3 = YEAR_2 - (YEAR_2 * (YEAR_OVER_YEAR/100) ) , YEAR_3_INGL_CURR = YEAR_2_INGL_CURR - ( YEAR_2_INGL_CURR * (YEAR_OVER_YEAR/100) )  FROM SAQICO (NOLOCK)A JOIN (SELECT DISTINCT QUOTE_ID,SERVICE_ID,EQUIPMENT_ID,YEAR_PERIOD,REVISION_ID FROM SAQICO_INBOUND(NOLOCK)  WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"')B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND QTEREV_ID = REVISION_ID WHERE YEAR_PERIOD>=3  ' ")
					
					#Year 4
					primaryQueryItems = SqlHelper.GetFirst(
						""
						+ str(Parameter1.QUERY_CRITERIA_1)
						+ "  A SET YEAR_4 = YEAR_3 - (YEAR_3 * (YEAR_OVER_YEAR/100)) ,YEAR_4_INGL_CURR = YEAR_3_INGL_CURR - ( YEAR_3_INGL_CURR * (YEAR_OVER_YEAR/100) )  FROM SAQICO (NOLOCK)A JOIN (SELECT DISTINCT QUOTE_ID,SERVICE_ID,EQUIPMENT_ID,YEAR_PERIOD,REVISION_ID FROM SAQICO_INBOUND(NOLOCK)  WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"')B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND QTEREV_ID = REVISION_ID WHERE YEAR_PERIOD>=4  ' ")
					
					#Year 5
					primaryQueryItems = SqlHelper.GetFirst(
						""
						+ str(Parameter1.QUERY_CRITERIA_1)
						+ "  A SET YEAR_5 = YEAR_4 - (YEAR_4 * (YEAR_OVER_YEAR/100)) ,YEAR_5_INGL_CURR = YEAR_4_INGL_CURR - ( YEAR_4_INGL_CURR * (YEAR_OVER_YEAR/100) ) FROM SAQICO (NOLOCK)A JOIN (SELECT DISTINCT QUOTE_ID,SERVICE_ID,EQUIPMENT_ID,YEAR_PERIOD,REVISION_ID FROM SAQICO_INBOUND(NOLOCK)  WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"')B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND QTEREV_ID = REVISION_ID WHERE YEAR_PERIOD>=5  ' ")
					
					#Tax
					primaryQueryItems = SqlHelper.GetFirst(
						""
						+ str(Parameter1.QUERY_CRITERIA_1)
						+ "  A SET TAX_AMOUNT = ( (ISNULL(YEAR_1,0) + ISNULL(YEAR_2,0) + ISNULL(YEAR_3,0) + ISNULL(YEAR_5,0) + ISNULL(YEAR_4,0) ) * (TAX_PERCENTAGE/100)) , TAX_AMOUNT_INGL_CURR = ( (ISNULL(YEAR_1_INGL_CURR,0) + ISNULL(YEAR_2_INGL_CURR,0) + ISNULL(YEAR_3_INGL_CURR,0) + ISNULL(YEAR_5_INGL_CURR,0) + ISNULL(YEAR_4_INGL_CURR,0) ) * (TAX_PERCENTAGE/100))  FROM SAQICO (NOLOCK)A JOIN (SELECT  DISTINCT QUOTE_ID,SERVICE_ID,EQUIPMENT_ID,REVISION_ID FROM SAQICO_INBOUND(NOLOCK)  WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"')B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND QTEREV_ID = REVISION_ID WHERE TAX_AMOUNT IS NULL  ' ")
					
					#Extended Price
					primaryQueryItems = SqlHelper.GetFirst(
						""
						+ str(Parameter1.QUERY_CRITERIA_1)
						+ "  A SET NET_VALUE = ISNULL(YEAR_1,0) + ISNULL(YEAR_2,0) + ISNULL(YEAR_3,0) + ISNULL(YEAR_5,0) + ISNULL(YEAR_4,0) , NET_VALUE_INGL_CURR = ISNULL(YEAR_1_INGL_CURR,0) + ISNULL(YEAR_2_INGL_CURR,0) + ISNULL(YEAR_3_INGL_CURR,0) + ISNULL(YEAR_5_INGL_CURR,0) + ISNULL(YEAR_4_INGL_CURR,0)  FROM SAQICO (NOLOCK)A JOIN (SELECT  DISTINCT QUOTE_ID,SERVICE_ID,EQUIPMENT_ID,REVISION_ID FROM SAQICO_INBOUND(NOLOCK)  WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"')B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND QTEREV_ID = REVISION_ID WHERE TAX_AMOUNT IS NULL  ' ")

					#Greenbook Roll Up
					primaryQueryItems = SqlHelper.GetFirst(
					""
					+ str(Parameter1.QUERY_CRITERIA_1)
					+ "  SAQIGB SET BD_PRICE = SUB_GRNBOK.BD_PRICE,CEILING_PRICE = SUB_GRNBOK.CEILING_PRICE,NET_VALUE = SUB_GRNBOK.NET_VALUE,SALES_DISCOUNT_PRICE = SUB_GRNBOK.SALES_DISCOUNT_PRICE,NET_PRICE = SUB_GRNBOK.NET_PRICE,TARGET_PRICE = SUB_GRNBOK.TARGET_PRICE,TAX_AMOUNT = SUB_GRNBOK.TAX_AMOUNT,TOTAL_COST_WOSEEDSTOCK = SUB_GRNBOK.TOTAL_COST_WOSEEDSTOCK,TOTAL_COST_WSEEDSTOCK = SUB_GRNBOK.TOTAL_COST_WSEEDSTOCK,MODEL_PRICE = SUB_GRNBOK.MODEL_PRICE,YEAR_1 = SUB_GRNBOK.YEAR_1,YEAR_2 = SUB_GRNBOK.YEAR_2,YEAR_3 = SUB_GRNBOK.YEAR_3,YEAR_4 = SUB_GRNBOK.YEAR_4,YEAR_5 = SUB_GRNBOK.YEAR_5,BD_PRICE_INGL_CURR = SUB_GRNBOK.BD_PRICE_INGL_CURR,TARGET_PRICE_INGL_CURR = SUB_GRNBOK.TARGET_PRICE_INGL_CURR,SLSDIS_PRICE_INGL_CURR = SUB_GRNBOK.SLSDIS_PRICE_INGL_CURR,CEILING_PRICE_INGL_CURR = SUB_GRNBOK.CEILING_PRICE_INGL_CURR,NET_PRICE_INGL_CURR = SUB_GRNBOK.NET_PRICE_INGL_CURR,YEAR_1_INGL_CURR = SUB_GRNBOK.YEAR_1_INGL_CURR,YEAR_2_INGL_CURR = SUB_GRNBOK.YEAR_2_INGL_CURR,YEAR_3_INGL_CURR = SUB_GRNBOK.YEAR_3_INGL_CURR, YEAR_4_INGL_CURR = SUB_GRNBOK.YEAR_4_INGL_CURR, YEAR_5_INGL_CURR = SUB_GRNBOK.YEAR_5_INGL_CURR,TAX_AMOUNT_INGL_CURR = SUB_GRNBOK.TAX_AMOUNT_INGL_CURR,MODEL_PRICE_INGL_CURR = SUB_GRNBOK.MODEL_PRICE_INGL_CURR,NET_VALUE_INGL_CURR = SUB_GRNBOK.NET_VALUE_INGL_CURR FROM SAQIGB (NOLOCK) JOIN(SELECT SUM(SAQICO.BD_PRICE) AS BD_PRICE,SUM(SAQICO.CEILING_PRICE) AS CEILING_PRICE,SUM(SAQICO.NET_VALUE) AS NET_VALUE,SUM(SAQICO.SALES_DISCOUNT_PRICE) AS SALES_DISCOUNT_PRICE,SUM(SAQICO.NET_PRICE) AS NET_PRICE,SUM(SAQICO.TARGET_PRICE) AS TARGET_PRICE,SUM(SAQICO.TAX_AMOUNT) AS TAX_AMOUNT,SUM(SAQICO.TOTAL_COST_WOSEEDSTOCK) AS TOTAL_COST_WOSEEDSTOCK,SUM(SAQICO.TOTAL_COST_WSEEDSTOCK) AS TOTAL_COST_WSEEDSTOCK,SUM(SAQICO.YEAR_1) AS YEAR_1,SUM(SAQICO.YEAR_2) AS YEAR_2,SUM(SAQICO.YEAR_3) AS YEAR_3,SUM(SAQICO.YEAR_4) AS YEAR_4,SUM(SAQICO.YEAR_5) AS YEAR_5,SUM(SAQICO.MODEL_PRICE) AS MODEL_PRICE,SAQICO.QUOTE_ID,SAQICO.GREENBOOK,SAQICO.SERVICE_ID,SAQICO.FABLOCATION_ID,SUM(BD_PRICE_INGL_CURR) AS BD_PRICE_INGL_CURR,SUM(TARGET_PRICE_INGL_CURR) AS TARGET_PRICE_INGL_CURR,SUM(SLSDIS_PRICE_INGL_CURR) AS SLSDIS_PRICE_INGL_CURR,SUM(CEILING_PRICE_INGL_CURR) AS CEILING_PRICE_INGL_CURR,SUM(MODEL_PRICE_INGL_CURR) AS MODEL_PRICE_INGL_CURR,SUM(NET_PRICE_INGL_CURR) AS NET_PRICE_INGL_CURR,SUM(YEAR_1_INGL_CURR) AS YEAR_1_INGL_CURR,SUM(YEAR_2_INGL_CURR) AS YEAR_2_INGL_CURR,SUM(YEAR_3_INGL_CURR) AS YEAR_3_INGL_CURR,SUM(YEAR_4_INGL_CURR) AS YEAR_4_INGL_CURR, SUM(YEAR_5_INGL_CURR) AS YEAR_5_INGL_CURR,SUM(TAX_AMOUNT_INGL_CURR) AS TAX_AMOUNT_INGL_CURR,SUM(NET_VALUE_INGL_CURR) AS NET_VALUE_INGL_CURR,SAQICO.QTEREV_ID FROM SAQICO (NOLOCK) WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' GROUP BY SAQICO.QUOTE_ID,SAQICO.GREENBOOK,SAQICO.SERVICE_ID, SAQICO.FABLOCATION_ID,SAQICO.QTEREV_ID ) SUB_GRNBOK ON SAQIGB.QUOTE_ID = SUB_GRNBOK.QUOTE_ID AND SUB_GRNBOK.QTEREV_ID = SAQIGB.QTEREV_ID AND SAQIGB.GREENBOOK = SUB_GRNBOK.GREENBOOK AND SAQIGB.SERVICE_ID = SUB_GRNBOK.SERVICE_ID AND SAQIGB.FABLOCATION_ID = SUB_GRNBOK.FABLOCATION_ID ' ")
					
					#Fab Location Roll Up
					primaryQueryItems = SqlHelper.GetFirst(
					""
					+ str(Parameter1.QUERY_CRITERIA_1)
					+ "  SAQIFL SET BD_PRICE = SUB_FBL.BD_PRICE,NET_VALUE = SUB_FBL.NET_VALUE,SALES_DISCOUNT_PRICE = SUB_FBL.SALES_DISCOUNT_PRICE,NET_PRICE = SUB_FBL.NET_PRICE,TARGET_PRICE = SUB_FBL.TARGET_PRICE,TAX_AMOUNT = SUB_FBL.TAX_AMOUNT,TOTAL_COST_WOSEEDSTOCK = SUB_FBL.TOTAL_COST_WOSEEDSTOCK,TOTAL_COST_WSEEDSTOCK = SUB_FBL.TOTAL_COST_WSEEDSTOCK,MODEL_PRICE = SUB_FBL.MODEL_PRICE,YEAR_1 = SUB_FBL.YEAR_1,YEAR_2 = SUB_FBL.YEAR_2,YEAR_3 = SUB_FBL.YEAR_3,YEAR_4 = SUB_FBL.YEAR_4,YEAR_5 = SUB_FBL.YEAR_5, BD_PRICE_INGL_CURR = SUB_FBL.BD_PRICE_INGL_CURR,TARGET_PRICE_INGL_CURR = SUB_FBL.TARGET_PRICE_INGL_CURR,SLSDIS_PRICE_INGL_CURR = SUB_FBL.SLSDIS_PRICE_INGL_CURR,CEILING_PRICE_INGL_CURR = SUB_FBL.CEILING_PRICE_INGL_CURR,NET_PRICE_INGL_CURR = SUB_FBL.NET_PRICE_INGL_CURR,YEAR_1_INGL_CURR = SUB_FBL.YEAR_1_INGL_CURR,YEAR_2_INGL_CURR = SUB_FBL.YEAR_2_INGL_CURR,YEAR_3_INGL_CURR = SUB_FBL.YEAR_3_INGL_CURR, YEAR_4_INGL_CURR = SUB_FBL.YEAR_4_INGL_CURR, YEAR_5_INGL_CURR = SUB_FBL.YEAR_5_INGL_CURR,TAX_AMOUNT_INGL_CURR = SUB_FBL.TAX_AMOUNT_INGL_CURR,MODEL_PRICE_INGL_CURR = SUB_FBL.MODEL_PRICE_INGL_CURR,NET_VALUE_INGL_CURR = SUB_FBL.NET_VALUE_INGL_CURR FROM SAQIFL (NOLOCK) JOIN(SELECT SUM(SAQICO.BD_PRICE) AS BD_PRICE,SUM(SAQICO.CEILING_PRICE) AS CEILING_PRICE,SUM(SAQICO.NET_VALUE) AS NET_VALUE,SUM(SAQICO.SALES_DISCOUNT_PRICE) AS SALES_DISCOUNT_PRICE,SUM(SAQICO.NET_PRICE) AS NET_PRICE,SUM(SAQICO.TARGET_PRICE) AS TARGET_PRICE,SUM(SAQICO.TAX_AMOUNT) AS TAX_AMOUNT,SUM(SAQICO.TOTAL_COST_WOSEEDSTOCK) AS TOTAL_COST_WOSEEDSTOCK,SUM(SAQICO.TOTAL_COST_WSEEDSTOCK) AS TOTAL_COST_WSEEDSTOCK,SUM(SAQICO.YEAR_1) AS YEAR_1,SUM(SAQICO.YEAR_2) AS YEAR_2,SUM(SAQICO.YEAR_3) AS YEAR_3,SUM(SAQICO.YEAR_4) AS YEAR_4,SUM(SAQICO.YEAR_5) AS YEAR_5,SUM(SAQICO.MODEL_PRICE) AS MODEL_PRICE,SAQICO.QUOTE_ID,SAQICO.SERVICE_ID,SAQICO.FABLOCATION_ID,SUM(BD_PRICE_INGL_CURR) AS BD_PRICE_INGL_CURR,SUM(TARGET_PRICE_INGL_CURR) AS TARGET_PRICE_INGL_CURR,SUM(SLSDIS_PRICE_INGL_CURR) AS SLSDIS_PRICE_INGL_CURR,SUM(CEILING_PRICE_INGL_CURR) AS CEILING_PRICE_INGL_CURR,SUM(MODEL_PRICE_INGL_CURR) AS MODEL_PRICE_INGL_CURR,SUM(NET_PRICE_INGL_CURR) AS NET_PRICE_INGL_CURR,SUM(YEAR_1_INGL_CURR) AS YEAR_1_INGL_CURR,SUM(YEAR_2_INGL_CURR) AS YEAR_2_INGL_CURR,SUM(YEAR_3_INGL_CURR) AS YEAR_3_INGL_CURR,SUM(YEAR_4_INGL_CURR) AS YEAR_4_INGL_CURR, SUM(YEAR_5_INGL_CURR) AS YEAR_5_INGL_CURR,SUM(TAX_AMOUNT_INGL_CURR) AS TAX_AMOUNT_INGL_CURR,SUM(NET_VALUE_INGL_CURR) AS NET_VALUE_INGL_CURR,SAQICO.QTEREV_ID FROM SAQICO (NOLOCK) WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' GROUP BY SAQICO.QUOTE_ID,SAQICO.SERVICE_ID, SAQICO.FABLOCATION_ID,SAQICO.QTEREV_ID ) SUB_FBL ON SAQIFL.QUOTE_ID = SUB_FBL.QUOTE_ID AND SAQIFL.SERVICE_ID = SUB_FBL.SERVICE_ID AND SAQIFL.FABLOCATION_ID = SUB_FBL.FABLOCATION_ID AND SUB_FBL.QTEREV_ID  = SAQIFL.QTEREV_ID ' ")

					#Item Roll Up
					primaryQueryItems = SqlHelper.GetFirst(
					""
					+ str(Parameter1.QUERY_CRITERIA_1)
					+ "  SAQITM SET BD_PRICE = SUB_SAQITM.BD_PRICE,CEILING_PRICE = SUB_SAQITM.CEILING_PRICE,NET_VALUE = SUB_SAQITM.NET_VALUE,SALES_DISCOUNT_PRICE = SUB_SAQITM.SALES_DISCOUNT_PRICE,NET_PRICE = SUB_SAQITM.NET_PRICE,TARGET_PRICE = SUB_SAQITM.TARGET_PRICE,TOTAL_COST_WOSEEDSTOCK = SUB_SAQITM.TOTAL_COST_WOSEEDSTOCK,TOTAL_COST_WSEEDSTOCK = SUB_SAQITM.TOTAL_COST_WSEEDSTOCK,MODEL_PRICE = SUB_SAQITM.MODEL_PRICE,YEAR_1 = SUB_SAQITM.YEAR_1,YEAR_2 = SUB_SAQITM.YEAR_2,YEAR_3 = SUB_SAQITM.YEAR_3,YEAR_4 = SUB_SAQITM.YEAR_4,YEAR_5 = SUB_SAQITM.YEAR_5,TAX_AMOUNT = ROUND((SUB_SAQITM.NET_VALUE * (ISNULL(SAQITM.TAX_PERCENTAGE,0)/100)),CONVERT(INT,"+str(roundcurr.DECIMAL_PLACES)+"),CONVERT(INT,"+str(roundcurr.ROUNDING_METHOD)+")) , TAX_AMOUNT_INGL_CURR = ROUND((SUB_SAQITM.NET_VALUE_INGL_CURR * (ISNULL(SAQITM.TAX_PERCENTAGE,0)/100)),CONVERT(INT,"+str(roundcurr.DECIMAL_PLACES)+"),CONVERT(INT,"+str(roundcurr.ROUNDING_METHOD)+")) , BD_PRICE_INGL_CURR = SUB_SAQITM.BD_PRICE_INGL_CURR,TARGET_PRICE_INGL_CURR = SUB_SAQITM.TARGET_PRICE_INGL_CURR,SLSDIS_PRICE_INGL_CURR = SUB_SAQITM.SLSDIS_PRICE_INGL_CURR,CEILING_PRICE_INGL_CURR = SUB_SAQITM.CEILING_PRICE_INGL_CURR,NET_PRICE_INGL_CURR = SUB_SAQITM.NET_PRICE_INGL_CURR,NET_VALUE_INGL_CURR=SUB_SAQITM.NET_VALUE_INGL_CURR,YEAR_1_INGL_CURR = SUB_SAQITM.YEAR_1_INGL_CURR,YEAR_2_INGL_CURR = SUB_SAQITM.YEAR_2_INGL_CURR,YEAR_3_INGL_CURR = SUB_SAQITM.YEAR_3_INGL_CURR, YEAR_4_INGL_CURR = SUB_SAQITM.YEAR_4_INGL_CURR, YEAR_5_INGL_CURR = SUB_SAQITM.YEAR_5_INGL_CURR,MODEL_PRICE_INGL_CURR = SUB_SAQITM.MODEL_PRICE_INGL_CURR  FROM SAQITM (NOLOCK) JOIN(SELECT SUM(SAQICO.BD_PRICE) AS BD_PRICE,SUM(SAQICO.CEILING_PRICE) AS CEILING_PRICE,SUM(SAQICO.NET_VALUE) AS NET_VALUE,SUM(SAQICO.SALES_DISCOUNT_PRICE) AS SALES_DISCOUNT_PRICE,SUM(SAQICO.NET_PRICE) AS NET_PRICE,SUM(SAQICO.TARGET_PRICE) AS TARGET_PRICE,SUM(SAQICO.TAX_AMOUNT) AS TAX_AMOUNT,SUM(SAQICO.TOTAL_COST_WOSEEDSTOCK) AS TOTAL_COST_WOSEEDSTOCK,SUM(SAQICO.TOTAL_COST_WSEEDSTOCK) AS TOTAL_COST_WSEEDSTOCK,SUM(SAQICO.YEAR_1) AS YEAR_1,SUM(SAQICO.YEAR_2) AS YEAR_2,SUM(SAQICO.YEAR_3) AS YEAR_3,SUM(SAQICO.YEAR_4) AS YEAR_4,SUM(SAQICO.YEAR_5) AS YEAR_5,SUM(SAQICO.MODEL_PRICE) AS MODEL_PRICE,SAQICO.QUOTE_ID,SAQICO.SERVICE_RECORD_ID,SUM(BD_PRICE_INGL_CURR) AS BD_PRICE_INGL_CURR,SUM(TARGET_PRICE_INGL_CURR) AS TARGET_PRICE_INGL_CURR,SUM(SLSDIS_PRICE_INGL_CURR) AS SLSDIS_PRICE_INGL_CURR,SUM(CEILING_PRICE_INGL_CURR) AS CEILING_PRICE_INGL_CURR,SUM(MODEL_PRICE_INGL_CURR) AS MODEL_PRICE_INGL_CURR,SUM(NET_PRICE_INGL_CURR) AS NET_PRICE_INGL_CURR,SUM(NET_VALUE_INGL_CURR) AS NET_VALUE_INGL_CURR,SUM(YEAR_1_INGL_CURR) AS YEAR_1_INGL_CURR,SUM(YEAR_2_INGL_CURR) AS YEAR_2_INGL_CURR,SUM(YEAR_3_INGL_CURR) AS YEAR_3_INGL_CURR,SUM(YEAR_4_INGL_CURR) AS YEAR_4_INGL_CURR, SUM(YEAR_5_INGL_CURR) AS YEAR_5_INGL_CURR,SUM(TAX_AMOUNT_INGL_CURR) AS TAX_AMOUNT_INGL_CURR,SAQICO.QTEREV_ID FROM SAQICO (NOLOCK) WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' GROUP BY SAQICO.QUOTE_ID,SAQICO.SERVICE_RECORD_ID,SAQICO.QTEREV_ID) SUB_SAQITM  ON SAQITM.QUOTE_ID = SUB_SAQITM.QUOTE_ID AND SAQITM.SERVICE_RECORD_ID = SUB_SAQITM.SERVICE_RECORD_ID AND SUB_SAQITM.QTEREV_ID = SAQITM.QTEREV_ID  ' ")

					primaryQueryItems = SqlHelper.GetFirst(
					""
					+ str(Parameter1.QUERY_CRITERIA_1)
					+ "  SAQITM SET BD_PRICE_MARGIN = SUB_SAQITM.BD_PRICE_MARGIN,BD_PRICE_MARGIN_RECORD_ID = SUB_SAQITM.BD_PRICE_MARGIN_RECORD_ID,DISCOUNT = SUB_SAQITM.DISCOUNT,SALDIS_PRICE_MARGIN_RECORD_ID = SUB_SAQITM.SLSDIS_PRICE_MARGIN_RECORD_ID,TARGET_PRICE_MARGIN_RECORD_ID = SUB_SAQITM.TARGET_PRICE_MARGIN_RECORD_ID,TARGET_PRICE_MARGIN = SUB_SAQITM.TARGET_PRICE_MARGIN,SALDIS_PRICE_MARGIN= SLSDIS_PRICE_MARGIN FROM SAQITM (NOLOCK) JOIN(SELECT DISTINCT SAQICO.QUOTE_ID,SAQICO.SERVICE_RECORD_ID,BD_PRICE_MARGIN,BD_PRICE_MARGIN_RECORD_ID,CEILING_PRICE_MARGIN,DISCOUNT,SLSDIS_PRICE_MARGIN,SLSDIS_PRICE_MARGIN_RECORD_ID,TARGET_PRICE_MARGIN_RECORD_ID,TARGET_PRICE_MARGIN,SAQICO.QTEREV_ID FROM SAQICO (NOLOCK) WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' ) SUB_SAQITM ON SAQITM.QUOTE_ID = SUB_SAQITM.QUOTE_ID AND SAQITM.SERVICE_RECORD_ID = SUB_SAQITM.SERVICE_RECORD_ID AND SUB_SAQITM.QTEREV_ID = SAQITM.QTEREV_ID ' ")
					
					primaryQueryItems = SqlHelper.GetFirst(
						""
					+ str(Parameter1.QUERY_CRITERIA_1)
					+ "  SAQICO SET STATUS=''PARTIALLY PRICED'' FROM SAQICO (NOLOCK) JOIN (SELECT DISTINCT QUOTE_ID,SERVICE_ID,EQUIPMENT_ID,REVISION_ID FROM SAQICO_INBOUND(NOLOCK)  WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND ISNULL(COST_MODULE_AVAILABLE,'''')=''UNAVAILABLE'' AND ISNULL(COST_CALCULATION_STATUS,'''') <> ''Chamber map not required'' )SAQICO_INBOUND ON SAQICO.QUOTE_ID = SAQICO_INBOUND.QUOTE_ID AND SAQICO.SERVICE_ID = SAQICO_INBOUND.SERVICE_ID AND SAQICO.EQUIPMENT_ID = SAQICO_INBOUND.EQUIPMENT_ID AND SAQICO.QTEREV_ID = SAQICO_INBOUND.REVISION_ID  '")
					
					primaryQueryItems = SqlHelper.GetFirst(
						""
					+ str(Parameter1.QUERY_CRITERIA_1)
					+ "  SAQICO SET STATUS=''ERROR'' FROM SAQICO (NOLOCK) JOIN (SELECT DISTINCT QUOTE_ID,SERVICE_ID,EQUIPMENT_ID,REVISION_ID FROM SAQICO_INBOUND(NOLOCK)  WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND ISNULL(COST_MODULE_AVAILABLE,'''')=''UNAVAILABLE'' AND ISNULL(COST_CALCULATION_STATUS,'''') = ''Tool Not Available'' )SAQICO_INBOUND ON SAQICO.QUOTE_ID = SAQICO_INBOUND.QUOTE_ID AND SAQICO.SERVICE_ID = SAQICO_INBOUND.SERVICE_ID AND SAQICO.EQUIPMENT_ID = SAQICO_INBOUND.EQUIPMENT_ID AND SAQICO.QTEREV_ID = SAQICO_INBOUND.REVISION_ID  '")
					
					primaryQueryItems = SqlHelper.GetFirst(
						""
					+ str(Parameter1.QUERY_CRITERIA_1)
					+ "  SAQITM SET PRICING_STATUS=''PARTIALLY PRICED'' FROM SAQITM (NOLOCK) WHERE QUOTE_ITEM_RECORD_ID IN (SELECT DISTINCT QTEITM_RECORD_ID FROM SAQICO_INBOUND(NOLOCK)A JOIN SAQICO B(NOLOCK) ON A.QUOTE_ID= B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID  WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND ISNULL(COST_MODULE_AVAILABLE,'''')=''UNAVAILABLE'' AND B.STATUS=''PARTIALLY PRICED'') '")
					
					primaryQueryItems = SqlHelper.GetFirst(
						""
					+ str(Parameter1.QUERY_CRITERIA_1)
					+ "  SAQITM SET PRICING_STATUS=''ERROR'' FROM SAQITM (NOLOCK) WHERE QUOTE_ITEM_RECORD_ID IN (SELECT DISTINCT QTEITM_RECORD_ID FROM SAQICO(NOLOCK)  WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND STATUS IN (''ERROR'',''ASSEMBLY IS MISSING'')) '")
					
					primaryQueryItems = SqlHelper.GetFirst(
						""
					+ str(Parameter1.QUERY_CRITERIA_1)
					+ "  SAQTRV SET REVISION_STATUS=''ON HOLD - COSTING'' FROM SAQTRV A(NOLOCK) JOIN (SELECT DISTINCT QUOTE_ID,QTEREV_ID FROM SAQICO B(NOLOCK)  WHERE  STATUS  IN (''PARTIALLY PRICED'',''ERROR'',''ASSEMBLY IS MISSING'') AND QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'')B ON A.QUOTE_ID = B.QUOTE_ID AND A.QTEREV_ID = B.QTEREV_ID '")
					
					primaryQueryItems = SqlHelper.GetFirst(
						""
					+ str(Parameter1.QUERY_CRITERIA_1)
					+ "  SAQTRV SET REVISION_STATUS=''APPROVAL PENDING'' FROM SAQTRV A(NOLOCK) WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND NOT EXISTS (SELECT ''X'' FROM SAQICO B(NOLOCK)  WHERE  STATUS IN(''PARTIALLY PRICED'',''ERROR'',''ASSEMBLY IS MISSING'') AND QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'') '")
					
					"""primaryQueryItems = SqlHelper.GetFirst(
						""
					+ str(Parameter1.QUERY_CRITERIA_1)
					+ "  SAQICO SET STATUS=''ON HOLD - PRICING'' FROM SAQICO (NOLOCK) JOIN (SELECT DISTINCT QUOTE_ID,SERVICE_ID,EQUIPMENT_ID,REVISION_ID FROM SAQICO_INBOUND(NOLOCK)  WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND ISNULL(COST_MODULE_AVAILABLE,'''')=''AVAILABLE'' AND EQUIPMENT_ID NOT IN (SELECT EQUIPMENT_ID FROM SAQICO_INBOUND(NOLOCK)  WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND ISNULL(COST_MODULE_AVAILABLE,'''')=''UNAVAILABLE'' ) )SAQICO_INBOUND ON SAQICO.QUOTE_ID = SAQICO_INBOUND.QUOTE_ID AND SAQICO.SERVICE_ID = SAQICO_INBOUND.SERVICE_ID AND SAQICO.EQUIPMENT_ID = SQICO_INBOUND.EQUIPMENT_ID AND SAQICO.QTEREV_ID = SAQICO_INBOUND.REVISION_ID '")
					
					primaryQueryItems = SqlHelper.GetFirst(
						""
					+ str(Parameter1.QUERY_CRITERIA_1)
					+ "  SAQITM SET PRICING_STATUS=''ON HOLD - PRICING'' FROM SAQITM (NOLOCK) WHERE QUOTE_ITEM_RECORD_ID IN (SELECT DISTINCT QTEITM_RECORD_ID FROM SAQICO_INBOUND(NOLOCK)A JOIN SAQICO B(NOLOCK) ON A.QUOTE_ID= B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID  WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND ISNULL(COST_MODULE_AVAILABLE,'''')=''UNAVAILABLE'' AND PRICING_STATUS=''ON HOLD - PRICING'') AND PRICING_STATUS <> ''ON HOLD - COSTING'' '")"""
					
					primaryQueryItems = SqlHelper.GetFirst(
						""
					+ str(Parameter1.QUERY_CRITERIA_1)
					+ "  SAQICO SET STATUS=''ACQUIRED'' FROM SAQICO (NOLOCK) JOIN SAQICA(NOLOCK) ON SAQICO.QUOTE_ID = SAQICA.QUOTE_ID AND SAQICO.SERVICE_ID = SAQICA.SERVICE_ID AND SAQICO.QTEREV_ID = SAQICA.QTEREV_ID AND SAQICO.EQUIPMENT_ID = SAQICA.EQUIPMENT_ID JOIN SAQICO_INBOUND C(NOLOCK)ON SAQICO.QUOTE_ID = C.QUOTE_ID AND SAQICO.QTEREV_ID = C.REVISION_ID  AND SAQICO.SERVICE_ID = C.SERVICE_ID AND SAQICO.EQUIPMENT_ID = C.EQUIPMENT_ID WHERE TIMESTAMP = '"+str(timestamp_sessionid)+"' AND STATUS NOT IN (''PARTIAL PRICE'',''ERROR'',''ASSEMBLY IS MISSING'',''ACQUIRING'') '")
					
					primaryQueryItems = SqlHelper.GetFirst(
						""
					+ str(Parameter1.QUERY_CRITERIA_1)
					+ "  SAQITM SET PRICING_STATUS=''ACQUIRED'' FROM SAQITM (NOLOCK) WHERE QUOTE_ITEM_RECORD_ID NOT IN (SELECT QTEITM_RECORD_ID FROM SAQICO B(NOLOCK) WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND STATUS IN (''PARTIAL PRICE'',''ERROR'',''ASSEMBLY IS MISSING'',''ACQUIRING'')) AND PRICING_STATUS NOT IN (''ON HOLD - COSTING'',''ON HOLD - PRICING'',''ACQUIRING'',''PARTIAL PRICE'',''ERROR'',''ASSEMBLY IS MISSING'') '")

					"""primaryQueryItems = SqlHelper.GetFirst(
						""
					+ str(Parameter1.QUERY_CRITERIA_1)
					+ "  SAQICO SET PRICING_STATUS=''APPROVAL REQUIRED'',BENCHMARKING_THRESHOLD  = (((ANNUAL_BENCHMARK_BOOKING_PRICE-TARGET_PRICE)/ANNUAL_BENCHMARK_BOOKING_PRICE) * 100) * -1 FROM SAQICO  (NOLOCK) JOIN (SELECT QUOTE_ID,EQUIPMENT_LINE_ID,SERVICE_ID FROM (SELECT QUOTE_ID,EQUIPMENT_LINE_ID,SERVICE_ID,ANNUAL_BENCHMARK_BOOKING_PRICE + (ANNUAL_BENCHMARK_BOOKING_PRICE * 0.25) AS HIGHTARGET,ANNUAL_BENCHMARK_BOOKING_PRICE - (ANNUAL_BENCHMARK_BOOKING_PRICE * 0.25) AS LOWTARGET,TARGET_PRICE FROM SAQICO (NOLOCK) WHERE QUOTE_ID=''"+str(Qt_Id)+"'' AND ISNULL(ANNUAL_BENCHMARK_BOOKING_PRICE,0)>0 AND ISNULL(TARGET_PRICE,0) >0)B WHERE (B.TARGET_PRICE < B.LOWTARGET OR B.TARGET_PRICE > B.HIGHTARGET ) )SUB_SAQICO ON SAQICO.QUOTE_ID = SUB_SAQICO.QUOTE_ID AND SAQICO.SERVICE_ID = SUB_SAQICO.SERVICE_ID AND SAQICO.EQUIPMENT_LINE_ID = SUB_SAQICO.EQUIPMENT_LINE_ID  '")"""

					#Status Completed in SYINPL by CPQ Table Entry ID
					StatusUpdateQuery = SqlHelper.GetFirst(""+ str(Parameter1.QUERY_CRITERIA_1)+ "  SYINPL SET STATUS = ''COMPLETED'' FROM SYINPL (NOLOCK) A WHERE CpqTableEntryId = ''"+str(json_data.CpqTableEntryId)+"'' AND SESSION_ID =''"+str(SYINPL_SESSION.A)+"'' ' ")

					StatusUpdateQuery = SqlHelper.GetFirst(""+ str(Parameter2.QUERY_CRITERIA_1)+ " FROM SAQICO_INBOUND  WHERE ISNULL(SESSION_ID,'''')=''"+str(sessiondetail.A)+ "'' ' ")

					SAQIEN_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQIEN)+"'' ) BEGIN DROP TABLE "+str(SAQIEN)+" END  ' ")
					
					CRMTMP_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(CRMTMP)+"'' ) BEGIN DROP TABLE "+str(CRMTMP)+" END  ' ")
					
					Log.Info("QTPOSTQTPR pricing async call End --->"+str(Qt_Id.QUOTE_ID))
					# Mail system				
					Header = "<!DOCTYPE html><html><head><style>table {font-family: Calibri, sans-serif; border-collapse: collapse; width: 75%}td, th {  border: 1px solid #dddddd;  text-align: left; padding: 8px;}.im {color: #222;}tr:nth-child(even) {background-color: #dddddd;} #grey{background: rgb(245,245,245);} #bd{color : 'black';} </style></head><body id = 'bd'>"

					Table_start = "<p>Hi Team,<br><br>Pricing has been completed in CPQ, for the equipment's in below Quote ID.</p><table class='table table-bordered'><tr><th id = 'grey'>Quote ID</th><th id = 'grey'>Tools sent (CPQ-SSCM)</th><th id = 'grey'>Tools received (SSCM-CPQ)</th><th id = 'grey'>Price Calculation Status</th></tr><tr><td >"+str(Emailinfo.QUOTE_ID)+"</td><td>"+str(Emailinfo.SSCM)+"</td ><td>"+str(Emailinfo1.CPQ)+"</td><td>Completed</td></tr>"

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

					#Current user email(Toemail)
					#UserId = User.Id
					#Log.Info("123 UserId.UserId --->"+str(UserId))
					UserEmail = SqlHelper.GetFirst("SELECT isnull(email,'INTEGRATION.SUPPORT@BOSTONHARBORCONSULTING.COM') as email FROM saempl (nolock) where employee_id  = '"+str(ToEml.OWNER_ID)+"'")
					#Log.Info("123 UserEmail.email --->"+str(UserEmail.email))

					# Create two mail adresses, one for send from and the another for recipient
					if UserEmail is None:
						toEmail = MailAddress("suresh.muniyandi@bostonharborconsulting.com")
					else:
						toEmail = MailAddress(UserEmail.email)
					fromEmail = MailAddress("INTEGRATION.SUPPORT@BOSTONHARBORCONSULTING.COM")

					# Create new MailMessage object
					msg = MailMessage(fromEmail, toEmail)

					# Set message subject and body
					msg.Subject = "Pricing Completed - AMAT CPQ(X-Tenant)"
					msg.IsBodyHtml = True
					msg.Body = Error_Info

					# Bcc Emails	
					copyEmail4 = MailAddress("baji.baba@bostonharborconsulting.com")
					msg.Bcc.Add(copyEmail4)

					copyEmail1 = MailAddress("ranjani.parkavi@bostonharborconsulting.com")
					msg.Bcc.Add(copyEmail1) 

					copyEmail2 = MailAddress("arivazhagan.natarajan@bostonharborconsulting.com")
					msg.Bcc.Add(copyEmail2)

					copyEmail3 = MailAddress("sathyabama.akhala@bostonharborconsulting.com")
					msg.Bcc.Add(copyEmail3)

					copyEmail5 = MailAddress("ashish.gandotra@bostonharborconsulting.com")
					msg.Bcc.Add(copyEmail5)
					
					copyEmail6 = MailAddress("suresh.muniyandi@bostonharborconsulting.com")
					msg.Bcc.Add(copyEmail6)

					copyEmail8 = MailAddress("indira.priyadarsini@bostonharborconsulting.com")
					msg.Bcc.Add(copyEmail8)

					copyEmail7 = MailAddress("zeeshan.ahamed@bostonharborconsulting.com")
					msg.Bcc.Add(copyEmail7)

					copyEmail9 = MailAddress("siva.subramani@bostonharborconsulting.com")
					msg.Bcc.Add(copyEmail9)

					# Send the message
					mailClient.Send(msg)


					Greenbkquery=SqlHelper.GetList("SELECT DISTINCT SAQICO.GREENBOOK,ISNULL(SABUUN.DISTRIBUTION_EMAIL,'') AS DISTRIBUTION_EMAIL  FROM SAQICO(NOLOCK) JOIN SABUUN (NOLOCK) ON SAQICO.GREENBOOK = SABUUN.BUSINESSUNIT_ID WHERE SAQICO.STATUS IN ('ERROR','PARTIALLY PRICED','ASSEMBLY IS MISSING') AND SAQICO.QUOTE_ID = '"+str(Qt_Id.QUOTE_ID)+"' AND SAQICO.QTEREV_ID = '"+str(Qt_Id.REVISION_ID)+"' ")

					for Gbk in Greenbkquery:


						Grnbkdataquery=SqlHelper.GetList("SELECT SAQICO.GREENBOOK,SAQICO.QUOTE_ID,SAQICO.SERVICE_ID,SAQICO.EQUIPMENT_ID,SAQICA.ASSEMBLY_ID,SAQICA.COST_MODULE_AVAILABLE,ISNULL(SAQICA.COST_MODULE_STATUS,'ASSEMBLY IS MISSING') AS COST_MODULE_STATUS FROM SAQICO (NOLOCK) JOIN SAQICA (NOLOCK) ON SAQICO.QUOTE_ID = SAQICA.QUOTE_ID AND SAQICO.QTEREV_ID = SAQICA.QTEREV_ID AND SAQICO.SERVICE_ID = SAQICA.SERVICE_ID AND SAQICO.EQUIPMENT_ID = SAQICA.EQUIPMENT_ID WHERE SAQICO.STATUS IN ('ERROR','PARTIALLY PRICED' ) AND SAQICO.GREENBOOK= '"+str(Gbk.GREENBOOK)+"' AND SAQICO.QUOTE_ID = '"+str(Qt_Id.QUOTE_ID)+"' AND SAQICO.QTEREV_ID = '"+str(Qt_Id.REVISION_ID)+"' AND  SAQICA.COST_MODULE_AVAILABLE= 'UNAVAILABLE' AND SAQICA.COST_MODULE_STATUS <>'Chamber map not required' UNION ALL SELECT SAQICO.GREENBOOK,SAQICO.QUOTE_ID,SAQICO.SERVICE_ID,SAQICO.EQUIPMENT_ID,'' AS ASSEMBLY_ID,'' AS COST_MODULE_AVAILABLE,'ASSEMBLY IS MISSING' AS COST_MODULE_STATUS FROM SAQICO (NOLOCK)  WHERE SAQICO.STATUS IN ('ASSEMBLY IS MISSING' ) AND SAQICO.GREENBOOK= '"+str(Gbk.GREENBOOK)+"' AND SAQICO.QUOTE_ID = '"+str(Qt_Id.QUOTE_ID)+"' AND SAQICO.QTEREV_ID = '"+str(Qt_Id.REVISION_ID)+"' ")

						tbl_info = ''
						for gbkinfo in Grnbkdataquery:
							tbl_info = tbl_info+"<tr><td>"+str(gbkinfo.SERVICE_ID)+"</td><td>"+str(gbkinfo.GREENBOOK)+"</td ><td>"+str(gbkinfo.EQUIPMENT_ID)+"</td><td>"+str(gbkinfo.ASSEMBLY_ID)+"</td><td>"+str(gbkinfo.COST_MODULE_AVAILABLE)+"</td><td>"+str(gbkinfo.COST_MODULE_STATUS)+"</td></tr>"
						if len(tbl_info) > 0:
							Header = "<!DOCTYPE html><html><head><style>table {font-family: Calibri, sans-serif; border-collapse: collapse; width: 75%}td, th {  border: 1px solid #dddddd;  text-align: left; padding: 8px;}.im {color: #222;}tr:nth-child(even) {background-color: #dddddd;} #grey{background: rgb(245,245,245);} #bd{color : 'black';} </style></head><body id = 'bd'>"

							Table_start = "<p>Hi Team,<br><br>This Quote "+str(Qt_Id.QUOTE_ID)+"  is placed on ON HOLD COSTING status for the below cost information pending from SSCM system or Assembly missing in CPQ from IBASE.</p><table class='table table-bordered'><tr><th id = 'grey'>Service ID</th><th id = 'grey'>Green Book</th><th id = 'grey'>Equipment ID</th><th id = 'grey'>Assembly ID</th><th id = 'grey'>Cost Module Available</th><th id = 'grey'>Cost Module Status</th></tr>"+str(tbl_info)

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

							UserEmail = []
							if len(Gbk.DISTRIBUTION_EMAIL) > 0:
								UserEmail = str(Gbk.DISTRIBUTION_EMAIL).split(';')
							

							# Create two mail adresses, one for send from and the another for recipient
							toEmail = MailAddress("suresh.muniyandi@bostonharborconsulting.com")
							
							fromEmail = MailAddress("INTEGRATION.SUPPORT@BOSTONHARBORCONSULTING.COM")	

							# Create new MailMessage object
							msg = MailMessage(fromEmail, toEmail)							

							# Set message subject and body
							sub = "On Hold - Costing Quote("+str(Gbk.GREENBOOK)+")- AMAT CPQ (X-Tenant)"
							msg.Subject = sub
							msg.IsBodyHtml = True
							msg.Body = Error_Info

							#Comon CC mails
							copyEmail = MailAddress("arivazhagan.natarajan@bostonharborconsulting.com")
							msg.CC.Add(copyEmail)					

							copyEmail2 = MailAddress("indira.priyadarsini@bostonharborconsulting.com")
							msg.CC.Add(copyEmail2)

							copyEmail3 = MailAddress("ranjani.parkavi@bostonharborconsulting.com")
							msg.CC.Add(copyEmail3) 						

							copyEmail4 = MailAddress("sathyabama.akhala@bostonharborconsulting.com")
							msg.CC.Add(copyEmail4) 

							copyEmail5 = MailAddress("baji.baba@bostonharborconsulting.com")
							msg.CC.Add(copyEmail5) 

							copyEmail7 = MailAddress("zeeshan.ahamed@bostonharborconsulting.com")
							msg.CC.Add(copyEmail7)

							copyEmail8 = MailAddress("siva.subramani@bostonharborconsulting.com")
							msg.CC.Add(copyEmail8)
							
							copyEmail9 = MailAddress("deepa.ganesh@bostonharborconsulting.com")
							msg.CC.Add(copyEmail9)

							# Bcc Emails	
							if len(UserEmail) > 0:
								for emalinfo in  UserEmail:
									copyEmail = MailAddress(emalinfo)
									msg.Bcc.Add(copyEmail)

							# Send the message QT_REC_ID
							mailClient.Send(msg)
					#opening quote for update quote items
					try:
						quote_Edit = QuoteHelper.Edit(Qt_Id.QUOTE_ID)
					except:
						Log.Info("quote error")
					CallingCQIFWUDQTM = ScriptExecutor.ExecuteGlobal("CQIFWUDQTM",{"QT_REC_ID":Qt_Id.QUOTE_ID})	
					# Billing matrix async call
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
						
						result = '{\r\n\"ContractQuoteRecordId\" : \"'+str(Emailinfo.QUOTE_RECORD_ID)+'\"\r\n}'
						
						LOGIN_CRE = SqlHelper.GetFirst("SELECT URL FROM SYCONF where EXTERNAL_TABLE_NAME ='BILLING_MATRIX_ASYNC'")
						Async = webclient.UploadString(str(LOGIN_CRE.URL), str(result))

						level = "QT_QTQICO LEVEL"
						try:
							CQVLDRIFLW.iflow_valuedriver_rolldown(str(Emailinfo.QUOTE_RECORD_ID),level)
						except:
							Log.Info('Quote error')
					
					
					Unprocsseddataquery = SqlHelper.GetFirst("SELECT count(*) as cnt from SYINPL(NOLOCK) WHERE INTEGRATION_NAME = 'SSCM_TO_CPQ_PRICING_DATA' AND ISNULL(STATUS,'') = '' ")	

					if Unprocsseddataquery.cnt > 0 :
						#Async call for SSCM TO CPQ Unprocessed data 
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
					else: 
						ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "200", "Message": "Data Successfully Uploaded"}]})
				else:
					if Saqico_Flag == 0:
						Header = "<!DOCTYPE html><html><head><style>table {font-family: Calibri, sans-serif; border-collapse: collapse; width: 75%}td, th {  border: 1px solid #dddddd;  text-align: left; padding: 8px;}.im {color: #222;}tr:nth-child(even) {background-color: #dddddd;} #bd{color : 'black';} </style></head><body id = 'bd'>"

						Table_start = "<p>Hi Team,<br><br>SSCM Pricing script having follwing SAQICO data error for following Quote Id ---  "+str(Qt_Id.QUOTE_ID)+".<br><br></p><br>"
						
						Table_End = "</table><p><strong>Note : </strong>Please do not reply to this email.</p></body></html>"
						Table_info = ""     

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
						msg.Subject = "SSCM to CPQ - SAQICO Error Notification(X-Tenant)"
						msg.IsBodyHtml = True
						msg.Body = Error_Info

						# CC Emails 	
						copyEmail4 = MailAddress("baji.baba@bostonharborconsulting.com")
						msg.CC.Add(copyEmail4)
						
						copyEmail5 = MailAddress("arivazhagan.natarajan@bostonharborconsulting.com")
						msg.CC.Add(copyEmail5) 

						copyEmail6 = MailAddress("indira.priyadarsini@bostonharborconsulting.com")
						msg.CC.Add(copyEmail6) 

						copyEmail7 = MailAddress("indira.priyadarsini@bostonharborconsulting.com")
						msg.CC.Add(copyEmail7) 

						copyEmail1 = MailAddress("ranjani.parkavi@bostonharborconsulting.com")
						msg.CC.Add(copyEmail1) 						

						copyEmail3 = MailAddress("sathyabama.akhala@bostonharborconsulting.com")
						msg.CC.Add(copyEmail3) 

						copyEmail8 = MailAddress("zeeshan.ahamed@bostonharborconsulting.com")
						msg.CC.Add(copyEmail8)

						copyEmail2 = MailAddress("siva.subramani@bostonharborconsulting.com")
						msg.CC.Add(copyEmail2)
						
						copyEmail9 = MailAddress("deepa.ganesh@bostonharborconsulting.com")
						msg.CC.Add(copyEmail9)

						# Send the message
						mailClient.Send(msg)
					if Check_flag == 1:
						#Status Empty in SYINPL
						StatusUpdateQuery = SqlHelper.GetFirst(""+ str(Parameter1.QUERY_CRITERIA_1)+ "  A SET STATUS = ''Hold'' FROM SYINPL (NOLOCK) A WHERE SESSION_ID=''"+str(SYINPL_SESSION.A)+"''   AND  STATUS = ''INPROGRESS'' '")
	else:
		ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "200", "Message": "Session is running.Status is Inprogress"}]})
		

except:
	#Status Empty in SYINPL
	StatusUpdateQuery = SqlHelper.GetFirst(""+ str(Parameter1.QUERY_CRITERIA_1)+ "  A SET STATUS = '''' FROM SYINPL (NOLOCK) A WHERE SESSION_ID=''"+str(SYINPL_SESSION.A)+"''  ' ")
				
	Header = "<!DOCTYPE html><html><head><style>table {font-family: Calibri, sans-serif; border-collapse: collapse; width: 75%}td, th {  border: 1px solid #dddddd;  text-align: left; padding: 8px;}.im {color: #222;}tr:nth-child(even) {background-color: #dddddd;} #bd{color : 'black';} </style></head><body id = 'bd'>"

	Table_start = "<p>Hi Team,<br><br>SSCM Pricing script having follwing Error in Line number "+str(sys.exc_info()[-1].tb_lineno)+".<br><br>"+str(sys.exc_info()[1])+"</p><br>"
	
	Table_End = "</table><p><strong>Note : </strong>Please do not reply to this email.</p></body></html>"
	Table_info = ""     

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
	msg.Subject = "SSCM to CPQ - Pricing Error Notification(X-Tenant)"
	msg.IsBodyHtml = True
	msg.Body = Error_Info

	# CC Emails 	
	copyEmail4 = MailAddress("baji.baba@bostonharborconsulting.com")
	msg.CC.Add(copyEmail4)

	copyEmail5 = MailAddress("arivazhagan.natarajan@bostonharborconsulting.com")
	msg.CC.Add(copyEmail5)

	copyEmail6 = MailAddress("indira.priyadarsini@bostonharborconsulting.com")
	msg.CC.Add(copyEmail6)

	copyEmail8 = MailAddress("zeeshan.ahamed@bostonharborconsulting.com")
	msg.CC.Add(copyEmail8)

	copyEmail2 = MailAddress("siva.subramani@bostonharborconsulting.com")
	msg.CC.Add(copyEmail2)
	
	copyEmail9 = MailAddress("deepa.ganesh@bostonharborconsulting.com")
	msg.CC.Add(copyEmail9)
	
	# Send the message
	mailClient.Send(msg) 
	
	Log.Info("QTPOSTQTPR ERROR---->:" + str(sys.exc_info()[1]))
	Log.Info("QTPOSTQTPR ERROR LINE NO---->:" + str(sys.exc_info()[-1].tb_lineno))
	ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "400", "Message": str(sys.exc_info()[1])}]})
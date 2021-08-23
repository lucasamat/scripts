# =========================================================================================================================================
#   __script_name : QTPOSTQTPR.PY
#   __script_description : THIS SCRIPT IS USED TO INSERT PRICING DATA IN SAQICO_INBOUND FROM SYINPL
#   __primary_author__ : SURESH MUNIYANDI, BAJI
#   __create_date : 2020-11-16
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
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

		StatusUpdateQuery = SqlHelper.GetFirst(""+ str(Parameter1.QUERY_CRITERIA_1)+ "  SYINPL SET STATUS = ''DUPLICATE'' FROM SYINPL (NOLOCK)  WHERE isnull(status,'''')='''' AND INTEGRATION_NAME = ''SSCM_TO_CPQ_PRICING_DATA'' AND integration_key IN (SELECT integration_key FROM SYINPL(NOLOCK) WHERE isnull(status,'''')=''INPROGRESS'' AND INTEGRATION_NAME = ''SSCM_TO_CPQ_PRICING_DATA'') ' ")

		StatusUpdateQuery = SqlHelper.GetFirst(""+ str(Parameter1.QUERY_CRITERIA_1)+ "  SYINPL SET STATUS = ''INPROGRESS'',SESSION_ID=''"+str(SYINPL_SESSION.A)+"'' FROM SYINPL (NOLOCK)  WHERE isnull(status,'''')='''' AND INTEGRATION_NAME = ''SSCM_TO_CPQ_PRICING_DATA''  ' ")

		#Status Empty
		Jsonquery = SqlHelper.GetList("SELECT INTEGRATION_PAYLOAD,CpqTableEntryId from SYINPL(NOLOCK) WHERE INTEGRATION_NAME = 'SSCM_TO_CPQ_PRICING_DATA' AND ISNULL(STATUS,'') = 'INPROGRESS' AND SESSION_ID = '"+str(SYINPL_SESSION.A)+"' ")
		
		for json_data in Jsonquery:			
			
			exceptinfo = str(json_data.CpqTableEntryId)
			sessiondetail = SqlHelper.GetFirst("SELECT NEWID() AS A")
			
			if "Param" in str(json_data.INTEGRATION_PAYLOAD):
				splited_list = str(json_data.INTEGRATION_PAYLOAD).split("'")
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

				
				for tn in Table_Names:
					if tn in rebuilt_data:	
						if 1:#str(tn).upper() == "SAQICO":
							if str(type(rebuilt_data[tn])) == "<type 'dict'>":
								Tbl_data = [rebuilt_data[tn]]
							else:
								Tbl_data = rebuilt_data[tn]
								
							for record_dict in Tbl_data:

								primaryQueryItems = SqlHelper.GetFirst( ""+ str(Parameter.QUERY_CRITERIA_1)+ " SAQICO_INBOUND (SESSION_ID,QUOTE_ID,EQUIPMENT_ID,COST_CALCULATION_STATUS,GREATER_THAN_QTLY_HOURS,LESS_THAN_QTLY_HOURS,LESS_THAN_QTLY_LAB_CST_WETCLEAN,PM_PART_COST,CM_PART_COST,CLEAN_COST,METROLOGY_COST,RECOATING_COST,LABOUR_HRS,CONSUMABLE_COST,CPQTABLEENTRYDATEADDED,SERVICE_ID,MONTHLY_PM_HOURS)  select ''"+str(sessiondetail.A)+ "'',''"+str(record_dict['QUOTE_ID'])+ "'',''"+str(record_dict['EQUIPMENT_ID'])+ "'',''"+str(record_dict['COST_CALCULATION_STATUS'])+ "'',''"+str(record_dict['GREATER_THAN_QTLY_HOURS'])+ "'',''"+str(record_dict['LESS_THAN_QTLY_HOURS'])+ "'',''"+str(record_dict['LESS_THAN_QTLY_LAB_CST_WETCLEAN'])+ "'',''"+str(record_dict['PM_PART_COST'])+ "'',''"+str(record_dict['CM_PART_COST'])+ "'',''"+str(record_dict['CLEAN_COST'])+ "'',''"+str(record_dict['METROLOGY_COST'])+ "'',''"+str(record_dict['RECOATING_COST'])+ "'',''"+str(record_dict['LABOUR_HRS'])+ "'',''"+str(record_dict['CONSUMABLE_COST'])+ "'',''"+ str(Modi_date)+ "'',''"+ str(record_dict['SERVICE_ID'])+ "'',''"+ str(record_dict['MONTHLY_PM_HOURS'])+ "'' ' ")
								
								Qt_Id = str(record_dict['QUOTE_ID'])
								#Log.Info("QTPOSTQTPR pricing async call is hitting1 --->")
								Check_flag = 1
								
				if Check_flag == 1:  

					Emailinfo = SqlHelper.GetFirst("SELECT QUOTE_ID,SSCM,0 as REMANING,QUOTE_RECORD_ID FROM (SELECT SAQICO.QUOTE_ID,COUNT(DISTINCT SAQICO.EQUIPMENT_ID) AS SSCM,SAQICO.QUOTE_RECORD_ID  FROM SAQICO (NOLOCK) WHERE SAQICO.QUOTE_ID = '"+str(Qt_Id)+"' AND ISNULL(PRICING_STATUS,'')<> '' group by SAQICO.Quote_ID,SAQICO.QUOTE_RECORD_ID )SUB_SAQICO ")  
					
					ToEml = SqlHelper.GetFirst("SELECT ISNULL(OWNER_ID,'X0116959') as OWNER_ID FROM SAQTMT (NOLOCK) WHERE SAQTMT.QUOTE_ID = '"+str(Qt_Id)+"'  ")  
					
					Emailinfo1 = SqlHelper.GetFirst("SELECT QUOTE_ID,CPQ FROM (SELECT SAQICO_INBOUND.QUOTE_ID,COUNT(DISTINCT SAQICO_INBOUND.EQUIPMENT_ID) AS CPQ FROM SAQICO_INBOUND (NOLOCK) WHERE SAQICO_INBOUND.QUOTE_ID = '"+str(Qt_Id)+"' AND ISNULL(SESSION_ID,'')='"+str(sessiondetail.A)+ "' group by SAQICO_INBOUND.Quote_ID )SUB_SAQICO ")  
				
					# Mail system				
					Header = "<!DOCTYPE html><html><head><style>table {font-family: Calibri, sans-serif; border-collapse: collapse; width: 75%}td, th {  border: 1px solid #dddddd;  text-align: left; padding: 8px;}.im {color: #222;}tr:nth-child(even) {background-color: #dddddd;} #grey{background: rgb(245,245,245);} #bd{color : 'black';} </style></head><body id = 'bd'>"

					Table_start = "<p>Hi Team,<br><br>Cost data has been received from SSCM for the below Quote ID and the CPQ price calculation has been initiated. Will let you know shortly about the pricing status.</p><table class='table table-bordered'><tr><th id = 'grey'>Quote ID</th><th id = 'grey'>Tools sent (CPQ-SSCM)</th><th id = 'grey'>Tools received (SSCM-CPQ)</th><th id = 'grey'>Price Calculation Status</th></tr><tr><td >"+str(Qt_Id)+"</td><td>"+str(Emailinfo.SSCM)+"</td ><td>"+str(Emailinfo1.CPQ)+"</td><td>Initiated</td></tr>"

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

					#Current user email(tomail)
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
					msg.Subject = "Pricing Initiated - AMAT CPQ QA"
					msg.IsBodyHtml = True
					msg.Body = Error_Info

					# Bcc Emails	
					copyEmail4 = MailAddress("baji.baba@bostonharborconsulting.com")
					msg.Bcc.Add(copyEmail4)

					copyEmail1 = MailAddress("ranjani.parkavi@bostonharborconsulting.com")
					msg.Bcc.Add(copyEmail1) 

					#copyEmail2 = MailAddress("aditya.shivkumar@bostonharborconsulting.com")
					#msg.Bcc.Add(copyEmail2)

					copyEmail3 = MailAddress("sathyabama.akhala@bostonharborconsulting.com")
					msg.Bcc.Add(copyEmail3)

					copyEmail5 = MailAddress("ashish.gandotra@bostonharborconsulting.com")
					msg.Bcc.Add(copyEmail5)
					
					copyEmail6 = MailAddress("suresh.muniyandi@bostonharborconsulting.com")
					msg.Bcc.Add(copyEmail6)

					# Send the message
					mailClient.Send(msg)
					
					Log.Info("QTPOSTQTPR pricing async call starting --->"+str(Qt_Id))
					#Calculation code started	
					sessionid = SqlHelper.GetFirst("SELECT NEWID() AS A")
					timestamp_sessionid = "'" + str(sessionid.A) + "'"	
					
					CRMQT = SqlHelper.GetFirst("select convert(varchar(100),c4c_quote_id) as c4c_quote_id from SAQTMT(nolock) WHERE QUOTE_ID = '"+str(Qt_Id)+"' ") 
					
					#SAQICO = "SAQICO_BKP_"+str(CRMQT.c4c_quote_id)
					
					#SAQICO_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''SAQICO_INBOUND'' ) BEGIN DROP TABLE SAQICO_INBOUND END  ' ")
					
					#SAQICO_SEL = SqlHelper.GetFirst("sp_executesql @T=N'SELECT * INTO SAQICO_INBOUND from SAQICO_INBOUND(NOLOCK) WHERE QUOTE_ID = ''"+str(Qt_Id)+"'' AND ISNULL(SESSION_ID,'''')=''"+str(sessiondetail.A)+ "''  ' ")
					
					primaryQueryItems = SqlHelper.GetFirst(
						""
						+ str(Parameter1.QUERY_CRITERIA_1)
						+ "  SAQICO_INBOUND SET TIMESTAMP = '"+str(timestamp_sessionid)+"',PROCESS_STATUS = ''INPROGRESS'' FROM SAQICO_INBOUND (NOLOCK)  WHERE ISNULL(PROCESS_STATUS,'''')='''' AND ISNULL(SESSION_ID,'''')=''"+str(sessiondetail.A)+ "'' '")
					
					#Managed Service	
					#Sales Org ID
					primaryQueryItems = SqlHelper.GetFirst(
						""
						+ str(Parameter1.QUERY_CRITERIA_1)
						+ "  SAQICO_INBOUND SET SALESORG_ID = SAQTSO.SALESORG_ID FROM SAQICO_INBOUND (NOLOCK) JOIN SAQTSO (NOLOCK) ON SAQICO_INBOUND.QUOTE_ID = SAQTSO.QUOTE_ID WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' ' ")				

					SAQIEN = "SAQIEN_BKP_"+str(CRMQT.c4c_quote_id)
					SAQIEN_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQIEN)+"'' ) BEGIN DROP TABLE "+str(SAQIEN)+" END  ' ")
					
					start = 1
					end = 1

					Check_flag = 1
					while Check_flag == 1:

						ent_query = SqlHelper.GetFirst("SELECT DISTINCT QUOTE_ID,cpqtableentryid FROM (SELECT DISTINCT quote_id,cpqtableentryid, ROW_NUMBER()OVER(ORDER BY cpqtableentryid) AS SNO FROM SAQSCE (NOLOCK) where quote_id='"+str(Qt_Id)+"' ) A WHERE SNO>= "+str(start)+" AND SNO<="+str(end)+" ")

						if str(ent_query) != "None":
							
							start = start + 1
							end = end + 1
													
							if start == 2:
								
								SAQIEN_SEL = SqlHelper.GetFirst("sp_executesql @T=N'declare @H int; Declare @val Varchar(MAX);DECLARE @XML XML; SELECT @val = FINAL from(select  REPLACE(entitlement_xml,''<QUOTE_ITEM_ENTITLEMENT>'',sml) AS FINAL FROM (select ''<QUOTE_ITEM_ENTITLEMENT><QUOTE_ID>''+quote_id+''</QUOTE_ID><SERVICE_ID>''+service_id+''</SERVICE_ID><EQUIPMENT_ID>''+equipment_id+''</EQUIPMENT_ID>'' AS sml,replace(entitlement_xml,''&'','';#38'')  as entitlement_xml from SAQSCE(nolock) where quote_id=''"+str(Qt_Id)+"'' AND cpqtableentryid = "+str(ent_query.cpqtableentryid)+" )A )a SELECT @XML = CONVERT(XML,''<ROOT>''+@VAL+''</ROOT>'') exec sys.sp_xml_preparedocument @H output,@XML; select QUOTE_ID,EQUIPMENT_ID,SERVICE_ID,ENTITLEMENT_NAME,ENTITLEMENT_DESCRIPTION,ENTITLEMENT_VALUE_CODE,PRICE_METHOD,ENTITLEMENT_COST_IMPACT,ENTITLEMENT_PRICE_IMPACT INTO "+str(SAQIEN)+"  from openxml(@H, ''ROOT/QUOTE_ITEM_ENTITLEMENT'', 0) with (QUOTE_ID VARCHAR(100) ''QUOTE_ID'',EQUIPMENT_ID VARCHAR(100) ''EQUIPMENT_ID'',ENTITLEMENT_NAME VARCHAR(100) ''ENTITLEMENT_NAME'',SERVICE_ID VARCHAR(100) ''SERVICE_ID'',ENTITLEMENT_VALUE_CODE VARCHAR(100) ''ENTITLEMENT_VALUE_CODE'',ENTITLEMENT_DESCRIPTION VARCHAR(100) ''ENTITLEMENT_DESCRIPTION'',PRICE_METHOD VARCHAR(100) ''PRICE_METHOD'',ENTITLEMENT_COST_IMPACT VARCHAR(100) ''ENTITLEMENT_COST_IMPACT'',ENTITLEMENT_PRICE_IMPACT VARCHAR(100) ''ENTITLEMENT_PRICE_IMPACT'') ; exec sys.sp_xml_removedocument @H; '")
							
							else:
								SAQIEN_SEL = SqlHelper.GetFirst("sp_executesql @T=N'declare @H int; Declare @val Varchar(MAX);DECLARE @XML XML; SELECT @val = FINAL from(select  REPLACE(entitlement_xml,''<QUOTE_ITEM_ENTITLEMENT>'',sml) AS FINAL FROM (select ''<QUOTE_ITEM_ENTITLEMENT><QUOTE_ID>''+quote_id+''</QUOTE_ID><SERVICE_ID>''+service_id+''</SERVICE_ID><EQUIPMENT_ID>''+equipment_id+''</EQUIPMENT_ID>'' AS sml,replace(entitlement_xml,''&'','';#38'')  as entitlement_xml from SAQSCE(nolock) where quote_id=''"+str(Qt_Id)+"'' AND cpqtableentryid = "+str(ent_query.cpqtableentryid)+" )A )a SELECT @XML = CONVERT(XML,''<ROOT>''+@VAL+''</ROOT>'') exec sys.sp_xml_preparedocument @H output,@XML; insert "+str(SAQIEN)+" (QUOTE_ID,EQUIPMENT_ID,SERVICE_ID,ENTITLEMENT_NAME,ENTITLEMENT_DESCRIPTION,ENTITLEMENT_VALUE_CODE,PRICE_METHOD,ENTITLEMENT_COST_IMPACT,ENTITLEMENT_PRICE_IMPACT) select QUOTE_ID,EQUIPMENT_ID,SERVICE_ID,ENTITLEMENT_NAME,ENTITLEMENT_DESCRIPTION,ENTITLEMENT_VALUE_CODE,PRICE_METHOD,ENTITLEMENT_COST_IMPACT,ENTITLEMENT_PRICE_IMPACT from openxml(@H, ''ROOT/QUOTE_ITEM_ENTITLEMENT'', 0) with (QUOTE_ID VARCHAR(100) ''QUOTE_ID'',EQUIPMENT_ID VARCHAR(100) ''EQUIPMENT_ID'',ENTITLEMENT_NAME VARCHAR(100) ''ENTITLEMENT_NAME'',SERVICE_ID VARCHAR(100) ''SERVICE_ID'',ENTITLEMENT_VALUE_CODE VARCHAR(100) ''ENTITLEMENT_VALUE_CODE'',ENTITLEMENT_DESCRIPTION VARCHAR(100) ''ENTITLEMENT_DESCRIPTION'',PRICE_METHOD VARCHAR(100) ''PRICE_METHOD'',ENTITLEMENT_COST_IMPACT VARCHAR(100) ''ENTITLEMENT_COST_IMPACT'',ENTITLEMENT_PRICE_IMPACT VARCHAR(100) ''ENTITLEMENT_PRICE_IMPACT'') ; exec sys.sp_xml_removedocument @H; '")
						
						else:
							Check_flag=0
					
					#Labor/Tech Labor Rate
					primaryQueryItems = SqlHelper.GetFirst(
						""
						+ str(Parameter1.QUERY_CRITERIA_1)
						+ "  SAQICO_INBOUND SET LABOR_RATE = SASORG.LABOR_RATE,TECH_LABOR_RATE = PM_TECH_LABOR_RATE FROM SAQICO_INBOUND (NOLOCK) JOIN SASORG (NOLOCK) ON SAQICO_INBOUND.SALESORG_ID = SASORG.SALESORG_ID WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' ' ")
					
					#Exchange Rate
					roundcurr1 = SqlHelper.GetFirst("select distinct CASE WHEN ROUNDING_DECIMAL_PLACES = '' THEN 0  ELSE ROUNDING_DECIMAL_PLACES END  AS DECIMAL_PLACES,CASE WHEN ROUNDING_METHOD='ROUND DOWN' THEN 1 ELSE 0 END AS ROUNDING_METHOD from prcurr (nolock) where currency= 'USD' ")
					
					roundcurr = SqlHelper.GetFirst("select distinct CASE WHEN ROUNDING_DECIMAL_PLACES = '' THEN 0  ELSE ROUNDING_DECIMAL_PLACES END  AS DECIMAL_PLACES,CASE WHEN ROUNDING_METHOD='ROUND DOWN' THEN 1 ELSE 0 END AS ROUNDING_METHOD from SAQICO(nolock) a join prcurr (nolock) on a.SORG_CURRENCY = prcurr.currency where quote_Id= '"+str(Qt_Id)+"' ")
						
					primaryQueryItems = SqlHelper.GetFirst(
						""
						+ str(Parameter1.QUERY_CRITERIA_1)
						+ "  SAQICO_INBOUND SET EXCHANGE_RATE = SAQICO.EXCHANGE_RATE FROM SAQICO_INBOUND (NOLOCK) JOIN SAQICO (NOLOCK) ON SAQICO_INBOUND.QUOTE_ID = SAQICO.QUOTE_ID AND SAQICO_INBOUND.EQUIPMENT_ID = SAQICO.EQUIPMENT_ID AND SAQICO_INBOUND.SERVICE_ID = SAQICO.SERVICE_ID WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'   ' ")
					
					#Labor Cost
					Log.Info("5656 -->"+str(""
						+ str(Parameter1.QUERY_CRITERIA_1)
						+ "  SAQICO_INBOUND SET LABOR_COST = ROUND( (LABOUR_HRS * LABOR_RATE ) ,CONVERT(INT,"+str(roundcurr.DECIMAL_PLACES)+"),CONVERT(INT,"+str(roundcurr.ROUNDING_METHOD)+")) FROM SAQICO_INBOUND (NOLOCK)   WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' '"))
					primaryQueryItems = SqlHelper.GetFirst(
						""
						+ str(Parameter1.QUERY_CRITERIA_1)
						+ "  SAQICO_INBOUND SET LABOR_COST = ROUND( (LABOUR_HRS * LABOR_RATE ) ,CONVERT(INT,"+str(roundcurr.DECIMAL_PLACES)+"),CONVERT(INT,"+str(roundcurr.ROUNDING_METHOD)+")) FROM SAQICO_INBOUND (NOLOCK)   WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' '")
					
					#PM Labor Update
					primaryQueryItems = SqlHelper.GetFirst(
						""
						+ str(Parameter1.QUERY_CRITERIA_1)
						+ "  SAQICO_INBOUND SET PM_LABOR = ENTITLEMENT_VALUE_CODE  FROM SAQICO_INBOUND (NOLOCK)  JOIN "+str(SAQIEN)+"  B(NOLOCK) ON SAQICO_INBOUND.QUOTE_ID = B.QUOTE_ID AND SAQICO_INBOUND.EQUIPMENT_ID = B.EQUIPMENT_ID AND SAQICO_INBOUND.SERVICE_ID = B.SERVICE_ID WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND ENTITLEMENT_DESCRIPTION=''Preventive Maintenance Labor''  ' ")

					#TechForce Update
					primaryQueryItems = SqlHelper.GetFirst(
						""
						+ str(Parameter1.QUERY_CRITERIA_1)
						+ "  SAQICO_INBOUND SET TECHFORCE = ENTITLEMENT_VALUE_CODE  FROM SAQICO_INBOUND (NOLOCK) JOIN "+str(SAQIEN)+" B(NOLOCK) ON SAQICO_INBOUND.QUOTE_ID = B.QUOTE_ID AND SAQICO_INBOUND.EQUIPMENT_ID = B.EQUIPMENT_ID AND SAQICO_INBOUND.SERVICE_ID = B.SERVICE_ID WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND ENTITLEMENT_DESCRIPTION=''Tech Force''   ' ")

					#Wet Clean Cost
					primaryQueryItems = SqlHelper.GetFirst(
						""
						+ str(Parameter1.QUERY_CRITERIA_1)
						+ "  SAQICO_INBOUND SET WETCLEAN_COST = ROUND( (ISNULL(LESS_THAN_QTLY_HOURS,0) * (CASE WHEN ISNULL(TECHFORCE,'''')=''INCLUDED'' THEN TECH_LABOR_RATE ELSE LABOR_RATE END) ) ,CONVERT(INT,"+str(roundcurr.DECIMAL_PLACES)+"),CONVERT(INT,"+str(roundcurr.ROUNDING_METHOD)+")) FROM SAQICO_INBOUND (NOLOCK)  WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'   ' ")
					
					#Preventive Maintenance Cost
					primaryQueryItems = SqlHelper.GetFirst(
					""
					+ str(Parameter1.QUERY_CRITERIA_1)
					+ "  SAQICO_INBOUND SET PM_COST = ROUND( (CASE WHEN TECHFORCE=''EXCLUDED'' AND PM_LABOR=''INCLUDED - QUARTERLY AND ABOVE'' THEN (GREATER_THAN_QTLY_HOURS  * LABOR_RATE) WHEN TECHFORCE=''EXCLUDED'' AND PM_LABOR=''INCLUDED - ALL PM'' THEN (GREATER_THAN_QTLY_HOURS + LESS_THAN_QTLY_LAB_CST_WETCLEAN) * LABOR_RATE  WHEN TECHFORCE=''EXCLUDED'' AND PM_LABOR=''INCLUDED - MONTHLY AND ABOVE'' THEN (GREATER_THAN_QTLY_HOURS + MONTHLY_PM_HOURS) * LABOR_RATE WHEN TECHFORCE=''INCLUDED'' AND PM_LABOR=''INCLUDED - QUARTERLY AND ABOVE'' THEN (GREATER_THAN_QTLY_HOURS  * TECH_LABOR_RATE) WHEN TECHFORCE=''INCLUDED'' AND PM_LABOR=''INCLUDED - ALL PM'' THEN ((GREATER_THAN_QTLY_HOURS * LABOR_RATE ) + LESS_THAN_QTLY_LAB_CST_WETCLEAN) * TECH_LABOR_RATE  WHEN TECHFORCE=''INCLUDED'' AND PM_LABOR=''INCLUDED - MONTHLY AND ABOVE'' THEN ((GREATER_THAN_QTLY_HOURS * LABOR_RATE ) + MONTHLY_PM_HOURS) * TECH_LABOR_RATE ELSE NULL END ),CONVERT(INT,"+str(roundcurr.DECIMAL_PLACES)+"),CONVERT(INT,"+str(roundcurr.ROUNDING_METHOD)+")) FROM SAQICO_INBOUND (NOLOCK)   WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  ' ")
					
					#KPI Cost
					primaryQueryItems = SqlHelper.GetFirst(
					""
					+ str(Parameter1.QUERY_CRITERIA_1)
					+ "  SAQICO_INBOUND SET KPI_COST = ROUND( ((ISNULL(PM_COST,0) + ISNULL(LABOR_COST,0) + ISNULL(WETCLEAN_COST,0)) * 0.10 ),CONVERT(INT,"+str(roundcurr.DECIMAL_PLACES)+"),CONVERT(INT,"+str(roundcurr.ROUNDING_METHOD)+"))  FROM SAQICO_INBOUND (NOLOCK) JOIN "+str(SAQIEN)+" B(NOLOCK) ON SAQICO_INBOUND.QUOTE_ID = B.QUOTE_ID AND SAQICO_INBOUND.EQUIPMENT_ID = B.EQUIPMENT_ID AND SAQICO_INBOUND.SERVICE_ID = B.SERVICE_ID WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND ENTITLEMENT_DESCRIPTION=''Performance Guarantee'' AND ISNULL(ENTITLEMENT_VALUE_CODE,'''') = ''UPTIME''  ' ")

					#Coverage Update
					primaryQueryItems = SqlHelper.GetFirst(
						""
						+ str(Parameter1.QUERY_CRITERIA_1)
						+ "  SAQICO_INBOUND SET COVERAGE = ENTITLEMENT_VALUE_CODE  FROM SAQICO_INBOUND (NOLOCK) JOIN "+str(SAQIEN)+" B(NOLOCK) ON SAQICO_INBOUND.QUOTE_ID = B.QUOTE_ID AND SAQICO_INBOUND.EQUIPMENT_ID = B.EQUIPMENT_ID AND SAQICO_INBOUND.SERVICE_ID = B.SERVICE_ID WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND ENTITLEMENT_DESCRIPTION=''CONTRACT COVERAGE''  ' ")
					
					#WetClean Update
					primaryQueryItems = SqlHelper.GetFirst(
					""
					+ str(Parameter1.QUERY_CRITERIA_1)
					+ "  SAQICO_INBOUND SET WETCLEAN_ENT = ENTITLEMENT_VALUE_CODE  FROM SAQICO_INBOUND (NOLOCK)  JOIN "+str(SAQIEN)+" B(NOLOCK) ON SAQICO_INBOUND.QUOTE_ID = B.QUOTE_ID AND SAQICO_INBOUND.EQUIPMENT_ID = B.EQUIPMENT_ID AND SAQICO_INBOUND.SERVICE_ID = B.SERVICE_ID WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND ENTITLEMENT_DESCRIPTION=''Wet Cleans labor''   ' ")
					
						
					#Consumable Update
					primaryQueryItems = SqlHelper.GetFirst(
						""
						+ str(Parameter1.QUERY_CRITERIA_1)
						+ "  SAQICO_INBOUND SET CONSUMABLE_ENT = ENTITLEMENT_VALUE_CODE  FROM SAQICO_INBOUND (NOLOCK)  JOIN "+str(SAQIEN)+" B(NOLOCK) ON SAQICO_INBOUND.QUOTE_ID = B.QUOTE_ID AND SAQICO_INBOUND.EQUIPMENT_ID = B.EQUIPMENT_ID AND SAQICO_INBOUND.SERVICE_ID = B.SERVICE_ID WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND ENTITLEMENT_DESCRIPTION=''Consumable''  ' ")
						
					#Non Consumable Update
					primaryQueryItems = SqlHelper.GetFirst(
						""
						+ str(Parameter1.QUERY_CRITERIA_1)
						+ "  SAQICO_INBOUND SET NONCONSUMABLE_ENT = ENTITLEMENT_VALUE_CODE  FROM SAQICO_INBOUND (NOLOCK) JOIN "+str(SAQIEN)+" B(NOLOCK) ON SAQICO_INBOUND.QUOTE_ID = B.QUOTE_ID AND SAQICO_INBOUND.EQUIPMENT_ID = B.EQUIPMENT_ID AND SAQICO_INBOUND.SERVICE_ID = B.SERVICE_ID WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND ENTITLEMENT_DESCRIPTION=''Non-Consumable''   ' ")
					
					#Total Cost
					primaryQueryItems = SqlHelper.GetFirst(
						""
						+ str(Parameter1.QUERY_CRITERIA_1)
						+ "  SAQICO_INBOUND SET TOTAL_COST = (CASE WHEN ISNULL(COVERAGE,'''')<>'''' THEN ISNULL(LABOR_COST,0) ELSE 0 END) + (CASE WHEN ISNULL(WETCLEAN_ENT,'''')<>'''' THEN ISNULL(WETCLEAN_COST,0) ELSE 0 END) + (CASE WHEN ISNULL(PM_LABOR,'''')<>'''' THEN ISNULL(PM_COST,0) ELSE 0 END) + (CASE WHEN ISNULL(CONSUMABLE_ENT,'''')=''INCLUDED'' THEN ISNULL(PM_PART_COST,0) ELSE 0 END) + (CASE WHEN ISNULL(NONCONSUMABLE_ENT,'''')=''INCLUDED'' THEN ISNULL(CM_PART_COST,0) ELSE 0 END) + ISNULL(CLEAN_COST,0) + ISNULL(KPI_COST,0)  FROM SAQICO_INBOUND (NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'   ' ")
						
					primaryQueryItems = SqlHelper.GetFirst(
						""
						+ str(Parameter1.QUERY_CRITERIA_1)
						+ "  SAQICO_INBOUND SET TOTAL_COST = ROUND(SAQICO_INBOUND.TOTAL_COST + ISNULL(SAQICO.ENTITLEMENT_COST_IMPACT,0),CONVERT(INT,"+str(roundcurr1.DECIMAL_PLACES)+"),CONVERT(INT,"+str(roundcurr1.ROUNDING_METHOD)+")) FROM SAQICO_INBOUND (NOLOCK)  JOIN SAQICO (NOLOCK) ON SAQICO_INBOUND.QUOTE_ID = SAQICO.QUOTE_ID AND SAQICO_INBOUND.SERVICE_ID = SAQICO.SERVICE_ID AND SAQICO_INBOUND.EQUIPMENT_ID = SAQICO.EQUIPMENT_ID WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' ' ")
					
					

					#Base Price
					primaryQueryItems = SqlHelper.GetFirst(
						""
						+ str(Parameter1.QUERY_CRITERIA_1)
						+ "  SAQICO_INBOUND SET BASE_PRICE = ROUND( ((SAQICO_INBOUND.TOTAL_COST /(1 - (PRBAMN.BASE_MARGIN/100))) * ISNULL(SAQICO_INBOUND.EXCHANGE_RATE,1)),CONVERT(INT,"+str(roundcurr.DECIMAL_PLACES)+"),CONVERT(INT,"+str(roundcurr.ROUNDING_METHOD)+"))  FROM SAQICO_INBOUND (NOLOCK) JOIN SAQICO (NOLOCK) ON SAQICO_INBOUND.QUOTE_ID = SAQICO.QUOTE_ID AND SAQICO_INBOUND.EQUIPMENT_ID = SAQICO.EQUIPMENT_ID AND SAQICO_INBOUND.SERVICE_ID = SAQICO.SERVICE_ID LEFT JOIN PRBAMN (NOLOCK) ON SAQICO_INBOUND.SERVICE_ID = PRBAMN.PRODUCT_ID AND SAQICO.GREENBOOK = PRBAMN.GREENBOOK WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'   ' ")
						
					#Target Price 
					primaryQueryItems = SqlHelper.GetFirst(
						""
						+ str(Parameter1.QUERY_CRITERIA_1)
						+ "  SAQICO_INBOUND SET TARGET_PRICE = CASE WHEN (SAQICO_INBOUND.BASE_PRICE * (1 + ISNULL(FAB_VALUEDRIVER_COEFFICIENT,0) + ISNULL(TOOL_VALUEDRIVER_COEFFICIENT,0) )) > (SAQICO_INBOUND.TOTAL_COST/(1-(SELECT MARGIN_DISCOUNT/100 FROM PRMDIT(NOLOCK) WHERE PRICING_TYPE=''TARGET'' AND THRESHOLD_TYPE=''MARGIN'' ))) THEN (SAQICO_INBOUND.BASE_PRICE * (1 + ISNULL(FAB_VALUEDRIVER_COEFFICIENT,0) + ISNULL(TOOL_VALUEDRIVER_COEFFICIENT,0) )) ELSE (SAQICO_INBOUND.TOTAL_COST/(1-(SELECT MARGIN_DISCOUNT/100 FROM PRMDIT(NOLOCK) WHERE PRICING_TYPE=''TARGET'' AND THRESHOLD_TYPE=''MARGIN'' ))) END FROM SAQICO_INBOUND (NOLOCK) JOIN SAQICO (NOLOCK) ON SAQICO_INBOUND.QUOTE_ID = SAQICO.QUOTE_ID AND SAQICO_INBOUND.EQUIPMENT_ID = SAQICO.EQUIPMENT_ID AND SAQICO_INBOUND.SERVICE_ID = SAQICO.SERVICE_ID  WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'   ' ")

					#On Call Outside
					primaryQueryItems = SqlHelper.GetFirst(
						""
						+ str(Parameter1.QUERY_CRITERIA_1)
						+ "  SAQICO_INBOUND SET ONCALL_ENT = ENTITLEMENT_VALUE_CODE  FROM SAQICO_INBOUND (NOLOCK)  JOIN "+str(SAQIEN)+"  B(NOLOCK) ON SAQICO_INBOUND.QUOTE_ID = B.QUOTE_ID AND SAQICO_INBOUND.EQUIPMENT_ID = B.EQUIPMENT_ID AND SAQICO_INBOUND.SERVICE_ID = B.SERVICE_ID WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND ENTITLEMENT_DESCRIPTION=''On call outside Contr Coverage'' ' ")

					#Target Price + On Call Outside
					primaryQueryItems = SqlHelper.GetFirst(
						""
						+ str(Parameter1.QUERY_CRITERIA_1)
						+ "  SAQICO_INBOUND SET TARGET_PRICE = ROUND( ((ISNULL(SAQICO_INBOUND.TARGET_PRICE,0) + (CASE WHEN COVERAGE=''5X8'' THEN 4000 WHEN COVERAGE=''7X12'' THEN 3500 ELSE 0 END)) * ISNULL(SAQICO_INBOUND.EXCHANGE_RATE,1) ),CONVERT(INT,"+str(roundcurr.DECIMAL_PLACES)+"),CONVERT(INT,"+str(roundcurr.ROUNDING_METHOD)+")) FROM SAQICO_INBOUND(NOLOCK) JOIN SAQICO (NOLOCK) ON SAQICO_INBOUND.QUOTE_ID = SAQICO.QUOTE_ID AND SAQICO_INBOUND.EQUIPMENT_ID = SAQICO.EQUIPMENT_ID AND SAQICO_INBOUND.SERVICE_ID = SAQICO.SERVICE_ID WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND ISNULL(ONCALL_ENT,'''')<>''''  ' ")
						
					#Ceiling Price
					primaryQueryItems = SqlHelper.GetFirst(
						""
						+ str(Parameter1.QUERY_CRITERIA_1)
						+ "  SAQICO_INBOUND SET CEILING_PRICE = ROUND( (TARGET_PRICE + (TARGET_PRICE * 0.3)),CONVERT(INT,"+str(roundcurr.DECIMAL_PLACES)+"),CONVERT(INT,"+str(roundcurr.ROUNDING_METHOD)+")) FROM SAQICO_INBOUND(NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  ' ")
						
					#Sales Price
					primaryQueryItems = SqlHelper.GetFirst(
						""
						+ str(Parameter1.QUERY_CRITERIA_1)
						+ "  SAQICO_INBOUND SET SALES_PRICE = ROUND( (CASE WHEN (TARGET_PRICE * (1- ISNULL((SELECT MARGIN_DISCOUNT/100 FROM PRMDIT WHERE PRICING_TYPE=''SALE'' AND THRESHOLD_TYPE=''DISCOUNT''),0))) > (TOTAL_COST/(1-(SELECT MARGIN_DISCOUNT/100 FROM PRMDIT(NOLOCK) WHERE PRICING_TYPE=''SALE'' AND THRESHOLD_TYPE=''MARGIN'' ))) THEN  (TARGET_PRICE * (1- ISNULL((SELECT MARGIN_DISCOUNT/100 FROM PRMDIT WHERE PRICING_TYPE=''SALE'' AND THRESHOLD_TYPE=''DISCOUNT''),0))) ELSE ((TOTAL_COST/(1-(SELECT MARGIN_DISCOUNT/100 FROM PRMDIT(NOLOCK) WHERE PRICING_TYPE=''SALE'' AND THRESHOLD_TYPE=''MARGIN'' ))) * ISNULL(SAQICO_INBOUND.EXCHANGE_RATE,1)) END) ,CONVERT(INT,"+str(roundcurr.DECIMAL_PLACES)+"),CONVERT(INT,"+str(roundcurr.ROUNDING_METHOD)+")) FROM SAQICO_INBOUND (NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  ' ")
						
					#BD Price
					primaryQueryItems = SqlHelper.GetFirst(
						""
						+ str(Parameter1.QUERY_CRITERIA_1)
						+ "  SAQICO_INBOUND SET BD_PRICE = ROUND( (CASE WHEN (TARGET_PRICE * (1- ISNULL((SELECT MARGIN_DISCOUNT/100 FROM PRMDIT WHERE PRICING_TYPE=''BD'' AND THRESHOLD_TYPE=''DISCOUNT''),0))) > (TOTAL_COST/(1-(SELECT MARGIN_DISCOUNT/100 FROM PRMDIT(NOLOCK) WHERE PRICING_TYPE=''BD'' AND THRESHOLD_TYPE=''MARGIN'' ))) THEN  (TARGET_PRICE * (1- ISNULL((SELECT MARGIN_DISCOUNT/100 FROM PRMDIT WHERE PRICING_TYPE=''BD'' AND THRESHOLD_TYPE=''DISCOUNT''),0))) ELSE ((TOTAL_COST/(1-(SELECT MARGIN_DISCOUNT/100 FROM PRMDIT(NOLOCK) WHERE PRICING_TYPE=''BD'' AND THRESHOLD_TYPE=''MARGIN'' )))* ISNULL(SAQICO_INBOUND.EXCHANGE_RATE,1)) END) ,CONVERT(INT,"+str(roundcurr.DECIMAL_PLACES)+"),CONVERT(INT,"+str(roundcurr.ROUNDING_METHOD)+"))  FROM SAQICO_INBOUND (NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  ' ")
					
					#Contract Year
					primaryQueryItems = SqlHelper.GetFirst(
						""
						+ str(Parameter1.QUERY_CRITERIA_1)
						+ "  SAQICO_INBOUND SET YEAR_PERIOD = datediff(yy,contract_valid_from,contract_valid_to)  FROM SAQICO_INBOUND (NOLOCK)  JOIN SAQTMT (NOLOCK) ON SAQICO_INBOUND.QUOTE_ID = SAQTMT.QUOTE_ID WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  ' ")
					
					
					
					#Main Table Update
					primaryQueryItems = SqlHelper.GetFirst(
						""
						+ str(Parameter1.QUERY_CRITERIA_1)
						+ "  SAQICO SET BASE_PRICE = SAQICO_INBOUND.BASE_PRICE , BD_PRICE = SAQICO_INBOUND.BD_PRICE ,CEILING_PRICE = SAQICO_INBOUND.CEILING_PRICE  ,CLEANING_COST = SAQICO_INBOUND.CLEAN_COST ,GREATER_THAN_QTLY_HRS =SAQICO_INBOUND.GREATER_THAN_QTLY_HOURS,LESS_THAN_QTLY_HRS =SAQICO_INBOUND.LESS_THAN_QTLY_LAB_CST_WETCLEAN,CONSUMABLE_COST = SAQICO_INBOUND.CONSUMABLE_COST,CM_PART_COST = SAQICO_INBOUND.CM_PART_COST,COST_CALCULATION_STATUS = SAQICO_INBOUND.COST_CALCULATION_STATUS,KPI_COST = SAQICO_INBOUND.KPI_COST ,LABOR_COST = SAQICO_INBOUND.LABOR_COST,LABOR_RATE = SAQICO_INBOUND.LABOR_RATE,PM_COST = SAQICO_INBOUND.PM_COST,LIST_PRICE = SAQICO_INBOUND.LIST_PRICE * ISNULL(SAQICO_INBOUND.EXCHANGE_RATE,1),PM_PART_COST = SAQICO_INBOUND.PM_PART_COST,PM_TECH_LABOR_RATE = SAQICO_INBOUND.TECH_LABOR_RATE,SALES_DISCOUNT_PRICE = (SAQICO_INBOUND.SALES_PRICE/(1-ISNULL(DISCOUNT,0))) ,SALES_PRICE = SAQICO_INBOUND.SALES_PRICE ,TARGET_PRICE = SAQICO_INBOUND.TARGET_PRICE ,TOTAL_COST =SAQICO_INBOUND.TOTAL_COST ,DISCOUNT=ISNULL(SAQICO.DISCOUNT,''0''),LABOR_HOURS =LABOUR_HRS ,CHAMBER_PM_HRS=LESS_THAN_QTLY_HOURS,WET_CLEAN_COST = WETCLEAN_COST,MONTHLY_PM_HRS =SAQICO_INBOUND.MONTHLY_PM_HOURS FROM SAQICO_INBOUND (NOLOCK)  JOIN SAQICO (NOLOCK) ON SAQICO_INBOUND.QUOTE_ID = SAQICO.QUOTE_ID AND SAQICO_INBOUND.EQUIPMENT_ID = SAQICO.EQUIPMENT_ID AND SAQICO_INBOUND.SERVICE_ID = SAQICO.SERVICE_ID WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  ' ")
					
					
					primaryQueryItems = SqlHelper.GetFirst(
						""
						+ str(Parameter1.QUERY_CRITERIA_1)
						+ "  SAQICO_INBOUND SET ENTITLEMENT_COST_IMPACT = ISNULL(ENTITLEMENT_PRICE_IMPACT,0) FROM SAQICO_INBOUND (NOLOCK) JOIN SAQICO (NOLOCK) ON SAQICO_INBOUND.QUOTE_ID = SAQICO.QUOTE_ID AND SAQICO_INBOUND.SERVICE_ID = SAQICO.SERVICE_ID AND SAQICO_INBOUND.EQUIPMENT_ID = SAQICO.EQUIPMENT_ID WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS''   ' ")
					
					#Targe Price + Entitlement Price Impact
					primaryQueryItems = SqlHelper.GetFirst(
						""
						+ str(Parameter1.QUERY_CRITERIA_1)
						+ "  SAQICO SET TARGET_PRICE = SAQICO.TARGET_PRICE + ISNULL(SAQICO.ENTITLEMENT_PRICE_IMPACT,0),BD_PRICE = SAQICO.BD_PRICE + ISNULL(SAQICO.ENTITLEMENT_PRICE_IMPACT,0),SALES_PRICE = SAQICO.SALES_PRICE + ISNULL(SAQICO.ENTITLEMENT_PRICE_IMPACT,0),SALES_DISCOUNT_PRICE = ((SAQICO.SALES_PRICE + ISNULL(SAQICO.ENTITLEMENT_PRICE_IMPACT,0) )/(1-ISNULL(DISCOUNT,0))) ,CEILING_PRICE = (SAQICO.TARGET_PRICE + ISNULL(SAQICO.ENTITLEMENT_PRICE_IMPACT,0)) + ((SAQICO.TARGET_PRICE + ISNULL(SAQICO.ENTITLEMENT_PRICE_IMPACT,0)) * 0.3) FROM SAQICO_INBOUND (NOLOCK)  JOIN SAQICO(NOLOCK) ON SAQICO_INBOUND.QUOTE_ID = SAQICO.QUOTE_ID AND SAQICO_INBOUND.EQUIPMENT_ID = SAQICO.EQUIPMENT_ID AND SAQICO_INBOUND.SERVICE_ID = SAQICO.SERVICE_ID  WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND  ISNULL(SAQICO.ENTITLEMENT_PRICE_IMPACT,0) >0  ' ")

					primaryQueryItems = SqlHelper.GetFirst(
						""
						+ str(Parameter1.QUERY_CRITERIA_1)
						+ "  SAQICO_INBOUND SET YEAR_1 = (SAQICO.SALES_DISCOUNT_PRICE) ,YEAR_OVER_YEAR = SAQICO.YEAR_OVER_YEAR FROM SAQICO_INBOUND (NOLOCK) JOIN SAQICO (NOLOCK) ON SAQICO_INBOUND.QUOTE_ID = SAQICO.QUOTE_ID AND SAQICO_INBOUND.EQUIPMENT_ID = SAQICO.EQUIPMENT_ID AND SAQICO_INBOUND.SERVICE_ID = SAQICO.SERVICE_ID  WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' ' ")

					primaryQueryItems = SqlHelper.GetFirst(
						""
						+ str(Parameter1.QUERY_CRITERIA_1)
						+ "  SAQICO_INBOUND SET YEAR_2 = ROUND ( (CASE WHEN CONVERT(INT,YEAR_PERIOD)>=2 THEN (((YEAR_1)/(1-(ISNULL(YEAR_OVER_YEAR,0)/100))))  ELSE NULL END),CONVERT(INT,"+str(roundcurr.DECIMAL_PLACES)+"),CONVERT(INT,"+str(roundcurr.ROUNDING_METHOD)+")) FROM SAQICO_INBOUND (NOLOCK)   WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  ' ")
						
					primaryQueryItems = SqlHelper.GetFirst(
						""
						+ str(Parameter1.QUERY_CRITERIA_1)
						+ "  SAQICO_INBOUND SET YEAR_3 = ROUND( (CASE WHEN CONVERT(INT,YEAR_PERIOD)>=3 THEN (YEAR_2 /(1-(ISNULL(YEAR_OVER_YEAR,0)/100))) ELSE NULL END ),CONVERT(INT,"+str(roundcurr.DECIMAL_PLACES)+"),CONVERT(INT,"+str(roundcurr.ROUNDING_METHOD)+")) FROM SAQICO_INBOUND (NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  ' ")
					
					primaryQueryItems = SqlHelper.GetFirst(
						""
						+ str(Parameter1.QUERY_CRITERIA_1)
						+ "  SAQICO_INBOUND SET YEAR_4 =  ROUND( (CASE WHEN CONVERT(INT,YEAR_PERIOD)>=4 THEN YEAR_3 /(1-(ISNULL(YEAR_OVER_YEAR,0)/100)) ELSE NULL END) ,CONVERT(INT,"+str(roundcurr.DECIMAL_PLACES)+"),CONVERT(INT,"+str(roundcurr.ROUNDING_METHOD)+")) FROM SAQICO_INBOUND (NOLOCK)  WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  ' ")
					
					primaryQueryItems = SqlHelper.GetFirst(
						""
						+ str(Parameter1.QUERY_CRITERIA_1)
						+ "  SAQICO_INBOUND SET YEAR_5 =  ROUND( (CASE WHEN CONVERT(INT,YEAR_PERIOD)>=5 THEN YEAR_4 /(1-(ISNULL(YEAR_OVER_YEAR,0)/100)) ELSE NULL END),CONVERT(INT,"+str(roundcurr.DECIMAL_PLACES)+"),CONVERT(INT,"+str(roundcurr.ROUNDING_METHOD)+")) FROM SAQICO_INBOUND (NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  ' ")
					
					

					#Margin Update
					primaryQueryItems = SqlHelper.GetFirst(
						""
						+ str(Parameter1.QUERY_CRITERIA_1)
						+ "  SAQICO SET EXTENDED_PRICE = ISNULL(SAQICO_INBOUND.YEAR_1,0)+ISNULL(SAQICO_INBOUND.YEAR_2,0)+ISNULL(SAQICO_INBOUND.YEAR_3,0)+ISNULL(SAQICO_INBOUND.YEAR_4,0)+ISNULL(SAQICO_INBOUND.YEAR_5,0),YEAR_1 = SAQICO_INBOUND.YEAR_1,YEAR_2 = SAQICO_INBOUND.YEAR_2,YEAR_3 = SAQICO_INBOUND.YEAR_3,YEAR_4 = SAQICO_INBOUND.YEAR_4,YEAR_5 = SAQICO_INBOUND.YEAR_5,BD_DISCOUNT =  (SELECT MARGIN_DISCOUNT FROM PRMDIT(NOLOCK) WHERE PRICING_TYPE=''BD'' AND THRESHOLD_TYPE=''DISCOUNT'' ),BD_DISCOUNT_RECORD_ID = (SELECT MARGIN_DISCOUNT_THRESHOLD_RECORD_ID FROM PRMDIT(NOLOCK) WHERE PRICING_TYPE=''BD'' AND THRESHOLD_TYPE=''DISCOUNT'' ),BD_PRICE_MARGIN =  (SELECT MARGIN_DISCOUNT FROM PRMDIT(NOLOCK) WHERE PRICING_TYPE=''BD'' AND THRESHOLD_TYPE=''MARGIN'' ),BD_PRICE_MARGIN_RECORD_ID = (SELECT MARGIN_DISCOUNT_THRESHOLD_RECORD_ID FROM PRMDIT(NOLOCK) WHERE PRICING_TYPE=''BD'' AND THRESHOLD_TYPE=''MARGIN'' ) ,SALES_DISCOUNT =  (SELECT MARGIN_DISCOUNT FROM PRMDIT(NOLOCK) WHERE PRICING_TYPE=''SALE'' AND THRESHOLD_TYPE=''DISCOUNT'' ),SALE_DISCOUNT_RECORD_ID = (SELECT MARGIN_DISCOUNT_THRESHOLD_RECORD_ID FROM PRMDIT(NOLOCK) WHERE PRICING_TYPE=''SALE'' AND THRESHOLD_TYPE=''DISCOUNT'' ),SALES_PRICE_MARGIN =  (SELECT MARGIN_DISCOUNT FROM PRMDIT(NOLOCK) WHERE PRICING_TYPE=''SALE'' AND THRESHOLD_TYPE=''MARGIN'' ),SALES_DISCOUNT_PRICE_MARGIN_RECORD_ID = (SELECT MARGIN_DISCOUNT_THRESHOLD_RECORD_ID FROM PRMDIT(NOLOCK) WHERE PRICING_TYPE=''SALE'' AND THRESHOLD_TYPE=''MARGIN'' ),TARGET_PRICE_MARGIN =  (SELECT MARGIN_DISCOUNT FROM PRMDIT(NOLOCK) WHERE PRICING_TYPE=''SALE'' AND THRESHOLD_TYPE=''MARGIN'' ),TARGET_PRICE_MARGIN_RECORD_ID = (SELECT MARGIN_DISCOUNT_THRESHOLD_RECORD_ID FROM PRMDIT(NOLOCK) WHERE PRICING_TYPE=''SALE'' AND THRESHOLD_TYPE=''MARGIN'' ),CEILING_PRICE_MARGIN=''30'' FROM SAQICO_INBOUND (NOLOCK) JOIN SAQICO (NOLOCK) ON SAQICO_INBOUND.QUOTE_ID = SAQICO.QUOTE_ID AND SAQICO_INBOUND.EQUIPMENT_ID = SAQICO.EQUIPMENT_ID AND SAQICO_INBOUND.SERVICE_ID = SAQICO.SERVICE_ID WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  ' ")
									
					primaryQueryItems = SqlHelper.GetFirst(
							""
							+ str(Parameter1.QUERY_CRITERIA_1)
							+ "  SAQICO SET LIST_PRICE_MARGIN =  SERVICE_PRODUCT_COEFFICIENT ,LSTPRIMRG_RECORD_ID = SERVICE_PRODUCT_COEFFICIENT_RECORD_ID,LIST_PRICE = ROUND( ( SAQICO.BASE_PRICE * (1 + (SERVICE_PRODUCT_COEFFICIENT/100)) ),CONVERT(INT,"+str(roundcurr.DECIMAL_PLACES)+"),CONVERT(INT,"+str(roundcurr.ROUNDING_METHOD)+")) FROM SAQICO_INBOUND (NOLOCK) JOIN SAQICO (NOLOCK) ON SAQICO_INBOUND.QUOTE_ID = SAQICO.QUOTE_ID AND SAQICO_INBOUND.EQUIPMENT_ID = SAQICO.EQUIPMENT_ID AND SAQICO_INBOUND.SERVICE_ID = SAQICO.SERVICE_ID JOIN PRSPCF (NOLOCK) ON SAQICO.SERVICE_ID = PRSPCF.SERVICE_ID WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  ' ")

					primaryQueryItems = SqlHelper.GetFirst(
							""
							+ str(Parameter1.QUERY_CRITERIA_1)
							+ "  SAQICO SET BASE_PRICE_MARGIN =  PRBAMN.BASE_MARGIN ,BASE_PRICE_MARGIN_RECORD_ID = BASE_MARGIN_RECORD_ID FROM SAQICO_INBOUND (NOLOCK) JOIN SAQICO (NOLOCK) ON SAQICO_INBOUND.QUOTE_ID = SAQICO.QUOTE_ID AND SAQICO_INBOUND.EQUIPMENT_ID = SAQICO.EQUIPMENT_ID AND SAQICO_INBOUND.SERVICE_ID = SAQICO.SERVICE_ID JOIN PRBAMN (NOLOCK) ON SAQICO.SERVICE_ID = PRBAMN.PRODUCT_ID AND SAQICO.GREENBOOK = PRBAMN.GREENBOOK WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  ' ")
					
									
					primaryQueryItems = SqlHelper.GetFirst(
						""
						+ str(Parameter1.QUERY_CRITERIA_1)
						+ "  SAQICO SET PRICING_STATUS=''ACQUIRED'' FROM SAQICO_INBOUND (NOLOCK) JOIN SAQICO (NOLOCK) ON SAQICO_INBOUND.QUOTE_ID = SAQICO.QUOTE_ID AND SAQICO_INBOUND.EQUIPMENT_ID = SAQICO.EQUIPMENT_ID AND SAQICO_INBOUND.SERVICE_ID = SAQICO.SERVICE_ID WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  ' ")
					
					primaryQueryItems = SqlHelper.GetFirst(
						""
						+ str(Parameter1.QUERY_CRITERIA_1)
						+ "  SAQICO SET PRICING_STATUS=''ERROR'' FROM SAQICO_INBOUND (NOLOCK) JOIN SAQICO (NOLOCK) ON SAQICO_INBOUND.QUOTE_ID = SAQICO.QUOTE_ID AND SAQICO_INBOUND.EQUIPMENT_ID = SAQICO.EQUIPMENT_ID AND SAQICO_INBOUND.SERVICE_ID = SAQICO.SERVICE_ID WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND (SAQICO_INBOUND.COST_CALCULATION_STATUS <> ''MAPPED'' OR ISNULL(SAQICO.TARGET_PRICE,0)<=0 ) ' ")
					
					primaryQueryItems = SqlHelper.GetFirst(
						""
						+ str(Parameter1.QUERY_CRITERIA_1)
						+ "  SAQICO SET PRICING_STATUS=''PARTIALLY PRICED'',COST_CALCULATION_STATUS=''Mapped'' FROM SAQICO (NOLOCK)  JOIN "+str(SAQIEN)+"  B(NOLOCK) ON SAQICO.QUOTE_ID = B.QUOTE_ID AND SAQICO.EQUIPMENT_ID = B.EQUIPMENT_ID AND SAQICO.SERVICE_ID = B.SERVICE_ID WHERE SAQICO.QUOTE_ID=''"+str(Qt_Id)+"'' AND ISNULL(PRICE_METHOD,'''')=''MANUAL PRICE'' AND ISNULL(B.ENTITLEMENT_COST_IMPACT,''0'')=''0'' AND ISNULL(B.ENTITLEMENT_PRICE_IMPACT,''0'')=''0'' ' ")
					
					primaryQueryItems = SqlHelper.GetFirst(
						""
						+ str(Parameter1.QUERY_CRITERIA_1)
						+ "  SAQICO SET EXTENDED_PRICE = ROUND((EXTENDED_PRICE + (EXTENDED_PRICE * (ISNULL(TAX_PERCENTAGE,0)/100))),CONVERT(INT,"+str(roundcurr.DECIMAL_PLACES)+"),CONVERT(INT,"+str(roundcurr.ROUNDING_METHOD)+")),TAX = ROUND((EXTENDED_PRICE * (ISNULL(TAX_PERCENTAGE,0)/100)),CONVERT(INT,"+str(roundcurr.DECIMAL_PLACES)+"),CONVERT(INT,"+str(roundcurr.ROUNDING_METHOD)+")) FROM SAQICO (NOLOCK) WHERE QUOTE_ID= ''"+str(Qt_Id)+"''  ' ")

					#Greenbook Roll Up
					primaryQueryItems = SqlHelper.GetFirst(
					""
					+ str(Parameter1.QUERY_CRITERIA_1)
					+ "  SAQIGB SET BD_PRICE = SUB_GRNBOK.BD_PRICE,CEILING_PRICE = SUB_GRNBOK.CEILING_PRICE,EXTENDED_PRICE = SUB_GRNBOK.EXTENDED_PRICE,SALES_DISCOUNT_PRICE = SUB_GRNBOK.SALES_DISCOUNT_PRICE,SALES_PRICE = SUB_GRNBOK.SALES_PRICE,TARGET_PRICE = SUB_GRNBOK.TARGET_PRICE,TAX = SUB_GRNBOK.TAX,TOTAL_COST = SUB_GRNBOK.TOTAL_COST,YEAR_1 = SUB_GRNBOK.YEAR_1,YEAR_2 = SUB_GRNBOK.YEAR_2,YEAR_3 = SUB_GRNBOK.YEAR_3,YEAR_4 = SUB_GRNBOK.YEAR_4,YEAR_5 = SUB_GRNBOK.YEAR_5 FROM SAQIGB (NOLOCK) JOIN(SELECT SUM(SAQICO.BD_PRICE) AS BD_PRICE,SUM(SAQICO.CEILING_PRICE) AS CEILING_PRICE,SUM(SAQICO.EXTENDED_PRICE) AS EXTENDED_PRICE,SUM(SAQICO.SALES_DISCOUNT_PRICE) AS SALES_DISCOUNT_PRICE,SUM(SAQICO.SALES_PRICE) AS SALES_PRICE,SUM(SAQICO.TARGET_PRICE) AS TARGET_PRICE,SUM(SAQICO.TAX) AS TAX,SUM(SAQICO.TOTAL_COST) AS TOTAL_COST,SUM(SAQICO.YEAR_1) AS YEAR_1,SUM(SAQICO.YEAR_2) AS YEAR_2,SUM(SAQICO.YEAR_3) AS YEAR_3,SUM(SAQICO.YEAR_4) AS YEAR_4,SUM(SAQICO.YEAR_5) AS YEAR_5,SAQICO.QUOTE_ID,SAQICO.GREENBOOK,SAQICO.SERVICE_ID,SAQICO.FABLOCATION_ID FROM SAQICO_INBOUND (NOLOCK)  JOIN SAQICO (NOLOCK) ON SAQICO_INBOUND.QUOTE_ID = SAQICO.QUOTE_ID AND SAQICO_INBOUND.EQUIPMENT_ID = SAQICO.EQUIPMENT_ID AND SAQICO_INBOUND.SERVICE_ID = SAQICO.SERVICE_ID WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' GROUP BY SAQICO.QUOTE_ID,SAQICO.GREENBOOK,SAQICO.SERVICE_ID, SAQICO.FABLOCATION_ID ) SUB_GRNBOK ON SAQIGB.QUOTE_ID = SUB_GRNBOK.QUOTE_ID AND SAQIGB.GREENBOOK = SUB_GRNBOK.GREENBOOK AND SAQIGB.SERVICE_ID = SUB_GRNBOK.SERVICE_ID AND SAQIGB.FABLOCATION_ID = SUB_GRNBOK.FABLOCATION_ID ' ")

					primaryQueryItems = SqlHelper.GetFirst(
					""
					+ str(Parameter1.QUERY_CRITERIA_1)
					+ "  SAQIGB SET BD_PRICE_MARGIN = SUB_QTQOGB.BD_PRICE_MARGIN,BD_PRICE_MARGIN_RECORD_ID = SUB_QTQOGB.BD_PRICE_MARGIN_RECORD_ID,CEILING_PRICE_MARGIN = SUB_QTQOGB.CEILING_PRICE_MARGIN,SALES_PRICE_MARGIN = SUB_QTQOGB.SALES_PRICE_MARGIN,SALES_DISCOUNT_PRICE_MARGIN_RECORD_ID = SUB_QTQOGB.SALES_DISCOUNT_PRICE_MARGIN_RECORD_ID,TARGET_PRICE_MARGIN_RECORD_ID = SUB_QTQOGB.TARGET_PRICE_MARGIN_RECORD_ID,TARGET_PRICE_MARGIN = SUB_QTQOGB.TARGET_PRICE_MARGIN FROM SAQIGB (NOLOCK) JOIN(SELECT DISTINCT SAQICO.QUOTE_ID,SAQICO.GREENBOOK,SAQICO.SERVICE_ID,BD_PRICE_MARGIN,BD_PRICE_MARGIN_RECORD_ID,CEILING_PRICE_MARGIN,SALES_PRICE_MARGIN,SALES_DISCOUNT_PRICE_MARGIN_RECORD_ID,TARGET_PRICE_MARGIN_RECORD_ID,TARGET_PRICE_MARGIN,SAQICO.FABLOCATION_ID FROM SAQICO_INBOUND (NOLOCK)  JOIN SAQICO (NOLOCK) ON SAQICO_INBOUND.QUOTE_ID = SAQICO.QUOTE_ID AND SAQICO_INBOUND.EQUIPMENT_ID = SAQICO.EQUIPMENT_ID AND SAQICO_INBOUND.SERVICE_ID = SAQICO.SERVICE_ID WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' ) SUB_QTQOGB ON SAQIGB.QUOTE_ID = SUB_QTQOGB.QUOTE_ID AND SAQIGB.GREENBOOK = SUB_QTQOGB.GREENBOOK AND SAQIGB.SERVICE_ID = SUB_QTQOGB.SERVICE_ID AND SAQIGB.FABLOCATION_ID = SUB_QTQOGB.FABLOCATION_ID ' ")


					#Item Roll Up
					primaryQueryItems = SqlHelper.GetFirst(
					""
					+ str(Parameter1.QUERY_CRITERIA_1)
					+ "  SAQITM SET BD_PRICE = SUB_SAQITM.BD_PRICE,CEILING_PRICE = SUB_SAQITM.CEILING_PRICE,EXTENDED_PRICE = SUB_SAQITM.EXTENDED_PRICE,SALES_DISCOUNT_PRICE = SUB_SAQITM.SALES_DISCOUNT_PRICE,SALES_PRICE = SUB_SAQITM.SALES_PRICE,TARGET_PRICE = SUB_SAQITM.TARGET_PRICE,TOTAL_COST = SUB_SAQITM.TOTAL_COST,YEAR_1 = SUB_SAQITM.YEAR_1,YEAR_2 = SUB_SAQITM.YEAR_2,YEAR_3 = SUB_SAQITM.YEAR_3,YEAR_4 = SUB_SAQITM.YEAR_4,YEAR_5 = SUB_SAQITM.YEAR_5,TAX = ROUND((SUB_SAQITM.EXTENDED_PRICE * (ISNULL(SAQITM.TAX_PERCENTAGE,0)/100)),CONVERT(INT,"+str(roundcurr.DECIMAL_PLACES)+"),CONVERT(INT,"+str(roundcurr.ROUNDING_METHOD)+")) FROM SAQITM (NOLOCK) JOIN(SELECT SUM(SAQICO.BD_PRICE) AS BD_PRICE,SUM(SAQICO.CEILING_PRICE) AS CEILING_PRICE,SUM(SAQICO.EXTENDED_PRICE) AS EXTENDED_PRICE,SUM(SAQICO.SALES_DISCOUNT_PRICE) AS SALES_DISCOUNT_PRICE,SUM(SAQICO.SALES_PRICE) AS SALES_PRICE,SUM(SAQICO.TARGET_PRICE) AS TARGET_PRICE,SUM(SAQICO.TAX) AS TAX,SUM(SAQICO.TOTAL_COST) AS TOTAL_COST,SUM(SAQICO.YEAR_1) AS YEAR_1,SUM(SAQICO.YEAR_2) AS YEAR_2,SUM(SAQICO.YEAR_3) AS YEAR_3,SUM(SAQICO.YEAR_4) AS YEAR_4,SUM(SAQICO.YEAR_5) AS YEAR_5,SAQICO.QUOTE_ID,SAQICO.SERVICE_ID FROM SAQICO_INBOUND (NOLOCK) JOIN SAQICO (NOLOCK) ON SAQICO_INBOUND.QUOTE_ID = SAQICO.QUOTE_ID AND SAQICO_INBOUND.EQUIPMENT_ID = SAQICO.EQUIPMENT_ID AND SAQICO_INBOUND.SERVICE_ID = SAQICO.SERVICE_ID WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' GROUP BY SAQICO.QUOTE_ID,SAQICO.SERVICE_ID) SUB_SAQITM  ON SAQITM.QUOTE_ID = SUB_SAQITM.QUOTE_ID AND SAQITM.SERVICE_ID = SUB_SAQITM.SERVICE_ID  ' ")

					primaryQueryItems = SqlHelper.GetFirst(
					""
					+ str(Parameter1.QUERY_CRITERIA_1)
					+ "  SAQITM SET BD_PRICE_MARGIN = SUB_SAQITM.BD_PRICE_MARGIN,BD_PRICE_MARGIN_RECORD_ID = SUB_SAQITM.BD_PRICE_MARGIN_RECORD_ID,DISCOUNT = SUB_SAQITM.DISCOUNT,SALES_DISCOUNT_PRICE_MARGIN_RECORD_ID = SUB_SAQITM.SALES_DISCOUNT_PRICE_MARGIN_RECORD_ID,TARGET_PRICE_MARGIN_RECORD_ID = SUB_SAQITM.TARGET_PRICE_MARGIN_RECORD_ID,TARGET_PRICE_MARGIN = SUB_SAQITM.TARGET_PRICE_MARGIN FROM SAQITM (NOLOCK) JOIN(SELECT DISTINCT SAQICO.QUOTE_ID,SAQICO.SERVICE_ID,BD_PRICE_MARGIN,BD_PRICE_MARGIN_RECORD_ID,CEILING_PRICE_MARGIN,DISCOUNT,SALES_PRICE_MARGIN,SALES_DISCOUNT_PRICE_MARGIN_RECORD_ID,TARGET_PRICE_MARGIN_RECORD_ID,TARGET_PRICE_MARGIN FROM SAQICO_INBOUND (NOLOCK) JOIN SAQICO (NOLOCK) ON SAQICO_INBOUND.QUOTE_ID = SAQICO.QUOTE_ID AND SAQICO_INBOUND.EQUIPMENT_ID = SAQICO.EQUIPMENT_ID AND SAQICO_INBOUND.SERVICE_ID = SAQICO.SERVICE_ID WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' ) SUB_SAQITM ON SAQITM.QUOTE_ID = SUB_SAQITM.QUOTE_ID AND SAQITM.SERVICE_ID = SUB_SAQITM.SERVICE_ID  ' ")

					primaryQueryItems = SqlHelper.GetFirst(
						""
					+ str(Parameter1.QUERY_CRITERIA_1)
					+ "  SAQICO SET PRICING_STATUS=''APPROVAL REQUIRED'',BENCHMARKING_THRESHOLD  = (((ANNUAL_BENCHMARK_BOOKING_PRICE-TARGET_PRICE)/ANNUAL_BENCHMARK_BOOKING_PRICE) * 100) * -1 FROM SAQICO  (NOLOCK) JOIN (SELECT QUOTE_ID,EQUIPMENT_LINE_ID,SERVICE_ID FROM (SELECT QUOTE_ID,EQUIPMENT_LINE_ID,SERVICE_ID,ANNUAL_BENCHMARK_BOOKING_PRICE + (ANNUAL_BENCHMARK_BOOKING_PRICE * 0.25) AS HIGHTARGET,ANNUAL_BENCHMARK_BOOKING_PRICE - (ANNUAL_BENCHMARK_BOOKING_PRICE * 0.25) AS LOWTARGET,TARGET_PRICE FROM SAQICO (NOLOCK) WHERE QUOTE_ID=''"+str(Qt_Id)+"'' AND ISNULL(ANNUAL_BENCHMARK_BOOKING_PRICE,0)>0 AND ISNULL(TARGET_PRICE,0) >0)B WHERE (B.TARGET_PRICE < B.LOWTARGET OR B.TARGET_PRICE > B.HIGHTARGET ) )SUB_SAQICO ON SAQICO.QUOTE_ID = SUB_SAQICO.QUOTE_ID AND SAQICO.SERVICE_ID = SUB_SAQICO.SERVICE_ID AND SAQICO.EQUIPMENT_LINE_ID = SUB_SAQICO.EQUIPMENT_LINE_ID  '")

					#StatusUpdateQuery = SqlHelper.GetFirst(""+ str(Parameter1.QUERY_CRITERIA_1)+ "  A SET PROCESS_STATUS = ''COMPLETED'' FROM SAQICO_INBOUND (NOLOCK) A WHERE TIMESTAMP = '"+str(timestamp_sessionid)+"' ' ")

					#SAQICO_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''SAQICO_INBOUND'' ) BEGIN DROP TABLE SAQICO_INBOUND END  ' ")

					#Status Completed in SYINPL by CPQ Table Entry ID
					StatusUpdateQuery = SqlHelper.GetFirst(""+ str(Parameter1.QUERY_CRITERIA_1)+ "  SYINPL SET STATUS = ''COMPLETED'' FROM SYINPL (NOLOCK) A WHERE CpqTableEntryId = ''"+str(json_data.CpqTableEntryId)+"'' AND SESSION_ID =''"+str(SYINPL_SESSION.A)+"'' ' ")

					StatusUpdateQuery = SqlHelper.GetFirst(""+ str(Parameter2.QUERY_CRITERIA_1)+ " FROM SAQICO_INBOUND  WHERE ISNULL(SESSION_ID,'''')=''"+str(sessiondetail.A)+ "'' ' ")

					SAQIEN_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQIEN)+"'' ) BEGIN DROP TABLE "+str(SAQIEN)+" END  ' ")
			
					Log.Info("QTPOSTQTPR pricing async call End --->"+str(Qt_Id))
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
					msg.Subject = "Pricing Completed - AMAT CPQ QA"
					msg.IsBodyHtml = True
					msg.Body = Error_Info

					# Bcc Emails	
					copyEmail4 = MailAddress("baji.baba@bostonharborconsulting.com")
					msg.Bcc.Add(copyEmail4)

					copyEmail1 = MailAddress("ranjani.parkavi@bostonharborconsulting.com")
					msg.Bcc.Add(copyEmail1) 

					#copyEmail2 = MailAddress("aditya.shivkumar@bostonharborconsulting.com")
					#msg.Bcc.Add(copyEmail2)

					copyEmail3 = MailAddress("sathyabama.akhala@bostonharborconsulting.com")
					msg.Bcc.Add(copyEmail3)

					copyEmail5 = MailAddress("ashish.gandotra@bostonharborconsulting.com")
					msg.Bcc.Add(copyEmail5)
					
					copyEmail6 = MailAddress("suresh.muniyandi@bostonharborconsulting.com")
					msg.Bcc.Add(copyEmail6)

					# Send the message
					mailClient.Send(msg)

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
						CQVLDRIFLW.iflow_valuedriver_rolldown(str(Emailinfo.QUOTE_RECORD_ID),level)
					
					
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
		ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "200", "Message": "Session is running.Status is Inprogress"}]})
		

except:
	#Status Empty in SYINPL
	StatusUpdateQuery = SqlHelper.GetFirst(""+ str(Parameter1.QUERY_CRITERIA_1)+ "  A SET STATUS = '''' FROM SYINPL (NOLOCK) A WHERE SESSION_ID=''"+str(SYINPL_SESSION.A)+"''  ' ")

	CRMQT = SqlHelper.GetFirst("select convert(varchar(100),c4c_quote_id) as c4c_quote_id from SAQTMT(nolock) WHERE QUOTE_ID = '"+str(Qt_Id)+"' ")

	SAQIEN = "SAQIEN_BKP_"+str(CRMQT.c4c_quote_id)
	SAQIEN_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQIEN)+"'' ) BEGIN DROP TABLE "+str(SAQIEN)+" END  ' ")
	
	#SAQICO = "SAQICO_BKP_"+str(CRMQT.c4c_quote_id)
				
	#SAQICO_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''SAQICO_INBOUND'' ) BEGIN DROP TABLE SAQICO_INBOUND END  ' ")
				
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
	msg.Subject = "SSCM to CPQ - Pricing Error Notification"
	msg.IsBodyHtml = True
	msg.Body = Error_Info

	# CC Emails 	
	copyEmail4 = MailAddress("baji.baba@bostonharborconsulting.com")
	msg.CC.Add(copyEmail4)
	
	# Send the message
	mailClient.Send(msg) 
	
	Log.Info("QTPOSTQTPR ERROR---->:" + str(sys.exc_info()[1]))
	Log.Info("QTPOSTQTPR ERROR LINE NO---->:" + str(sys.exc_info()[-1].tb_lineno))
	ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "400", "Message": str(sys.exc_info()[1])}]})
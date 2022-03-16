## =========================================================================================================================================
#   __script_name : PRPOSTEXRT.PY
#   __script_description : THIS SCRIPT IS USED TO INSERT/UPDATE EXCHANGE RATE FROM ECC TO CPQ
#   __primary_author__ : SURESH MUNIYANDI
#   __create_date : 
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
# CPQExchangeRateInbound
import SYTABACTIN as Table
import sys 
import datetime 

Parameter = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'SELECT' ")
Parameter1 = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'UPD' ")
Parameter2 = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'DEL' ")

TempTable_Seq = SqlHelper.GetFirst("SELECT cpqtableentryid From SYINPL(NOLOCK) WHERE INTEGRATION_NAME = 'EXCHANGERATE_DATA' AND ISNULL(STATUS,'')=''  ")

if str(TempTable_Seq) != 'None':

	Table_Name = "PREXRT_INBOUND"+str(TempTable_Seq.cpqtableentryid)

	try:
		Jsonquery = SqlHelper.GetList("SELECT  INTEGRATION_PAYLOAD,cpqtableentryid From SYINPL(NOLOCK) WHERE INTEGRATION_NAME = 'EXCHANGERATE_DATA' AND ISNULL(STATUS,'')='' ")
		Check_flag = 0
		primaryQueryItems = SqlHelper.GetFirst("SELECT NEWID() AS A")	
		timestamp_sessionid = "\'"+str(primaryQueryItems.A)+"\'"
		Error_Msg_lst = []
		Error_Msg_final = ''
		
		TempTable = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(Table_Name)+"'' ) BEGIN DROP TABLE "+str(Table_Name)+" END CREATE TABLE "+str(Table_Name)+" (SESSION_ID VARCHAR(100),FROM_CURRENCY VARCHAR(100) ,TO_CURRENCY VARCHAR(100) ,EXCHANGE_RATE VARCHAR(100),EXCHANGE_RATE_DATE VARCHAR(100),EXCHANGE_RATE_TYPE VARCHAR(100),RATIO_FROM VARCHAR(100),RATIO_TO VARCHAR(100),TIMESTAMP VARCHAR(100),PROCESS_STATUS VARCHAR(100),INTEGRATION_STATUS VARCHAR(MAX))'")
		
		for json_data in Jsonquery:
			if "Param" in str(json_data.INTEGRATION_PAYLOAD):
				splited_list = str(json_data.INTEGRATION_PAYLOAD).split("'")
				rebuilt_data = eval(str(splited_list[1]))
			else:
				splited_list = str(json_data.INTEGRATION_PAYLOAD)
				rebuilt_data = eval(splited_list)
			
			primaryQuerysession =  SqlHelper.GetFirst("SELECT NEWID() AS A")
			today = datetime.datetime.now()
			Modi_date = today.strftime("%m/%d/%Y %H:%M:%S %p")
			Parameter=SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME='SELECT' ")
			Parameter1 = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'UPD' ")

			if len(rebuilt_data) != 0:      

				rebuilt_data = rebuilt_data["CPQ_Columns"]
				Table_Names = rebuilt_data.keys()
				
				for tn in Table_Names:
					if tn in rebuilt_data:
						Check_flag = 1
						if str(tn).upper() == "PREXRT":
							if str(type(rebuilt_data[tn])) == "<type 'dict'>":
								Tbl_data = [rebuilt_data[tn]]
							else:
								Tbl_data = rebuilt_data[tn]
							
							#Dynamic table creation 
							for record_dict in Tbl_data:
								Stagingquery = SqlHelper.GetFirst( ""+ str(Parameter.QUERY_CRITERIA_1)+ " "+str(Table_Name)+" (SESSION_ID ,FROM_CURRENCY  ,TO_CURRENCY  ,EXCHANGE_RATE ,EXCHANGE_RATE_DATE ,EXCHANGE_RATE_TYPE ,RATIO_FROM ,RATIO_TO  )  select  ''"+ str(primaryQuerysession.A)+ "'',''"+str(record_dict['FROM_CURRENCY'])+ "'',''"+str(record_dict['TO_CURRENCY'])+ "'',''"+str(record_dict['EXCHANGE_RATE'])+ "'',''"+str(record_dict['EXCHANGE_RATE_DATE'])+ "'',''"+str(record_dict['EXCHANGE_RATE_TYPE'])+ "'',''"+str(record_dict['RATIO_FROM'])+ "'',''"+str(record_dict['RATIO_TO'])+ "'' ' ")
		
				primaryItems = SqlHelper.GetFirst(  ""+ str(Parameter1.QUERY_CRITERIA_1)+ "  SYINPL set STATUS = ''PROCESSED'' from SYINPL  (NOLOCK) WHERE cpqtableentryid  = ''"+str(json_data.cpqtableentryid)+ "'' AND ISNULL(STATUS ,'''')= '''' ' "    )
		
		
		if Check_flag == 1:
		
			#Timestamp Update
			primaryQueryItems = SqlHelper.GetFirst(	""+ str(Parameter1.QUERY_CRITERIA_1)+ " "+str(Table_Name)+" SET TIMESTAMP = '"+ str(timestamp_sessionid)+ "' ,PROCESS_STATUS = ''INPROGRESS'' WHERE ISNULL(TIMESTAMP,'''')='''' AND ISNULL(PROCESS_STATUS,'''')=''''  '")
		
			#PREXRT Does not Exist validations
			primaryQueryItems = SqlHelper.GetFirst(	""+ str(Parameter1.QUERY_CRITERIA_1)+ "  A SET A.INTEGRATION_STATUS = A.INTEGRATION_STATUS + ''||''+convert(nvarchar,SYMSGS.MESSAGE_CODE)+''-''+convert(nvarchar,A.FROM_CURRENCY),A.PROCESS_STATUS=''ERROR'' FROM "+str(Table_Name)+"(NOLOCK) A LEFT JOIN PRCURR (NOLOCK) ON A.FROM_CURRENCY = PRCURR.CURRENCY LEFT JOIN SYMSGS(NOLOCK) ON SYMSGS.MESSAGE_CODE = ''200101'' WHERE A.PROCESS_STATUS IN (''Inprogress'',''ERROR'') AND SYMSGS.OBJECT_APINAME = ''PREXRT'' AND a.TIMESTAMP='"+ str(timestamp_sessionid)+ "'  AND PRCURR.CURRENCY IS NULL AND A.FROM_CURRENCY <> '''' '")

			primaryQueryItems = SqlHelper.GetFirst(	""+ str(Parameter1.QUERY_CRITERIA_1)+ "  A SET A.INTEGRATION_STATUS = A.INTEGRATION_STATUS + ''||''+convert(nvarchar,SYMSGS.MESSAGE_CODE)+''-''+convert(nvarchar,A.TO_CURRENCY),A.PROCESS_STATUS=''ERROR'' FROM "+str(Table_Name)+"(NOLOCK) A LEFT JOIN PRCURR (NOLOCK) ON A.TO_CURRENCY = PRCURR.CURRENCY LEFT JOIN SYMSGS(NOLOCK) ON SYMSGS.MESSAGE_CODE = ''200102'' WHERE A.PROCESS_STATUS IN (''Inprogress'',''ERROR'') AND SYMSGS.OBJECT_APINAME = ''PREXRT'' AND a.TIMESTAMP='"+ str(timestamp_sessionid)+ "'  AND PRCURR.CURRENCY IS NULL AND A.TO_CURRENCY <> '''' '")

			#PREXRT Mandatory  validations
			primaryQueryItems = SqlHelper.GetFirst(	""+ str(Parameter1.QUERY_CRITERIA_1)+ "  A SET A.INTEGRATION_STATUS = A.INTEGRATION_STATUS + ''||''+convert(nvarchar,SYMSGS.MESSAGE_CODE),A.PROCESS_STATUS=''ERROR'' FROM "+str(Table_Name)+"(NOLOCK) A LEFT JOIN SYMSGS(NOLOCK) ON SYMSGS.MESSAGE_CODE = ''200103'' WHERE A.PROCESS_STATUS IN (''Inprogress'',''ERROR'') AND SYMSGS.OBJECT_APINAME = ''PREXRT'' AND a.TIMESTAMP='"	+ str(timestamp_sessionid)+ "'  AND ISNULL(EXCHANGE_RATE_DATE,'''') = '''''")

			primaryQueryItems = SqlHelper.GetFirst(	""+ str(Parameter1.QUERY_CRITERIA_1)+ "  A SET A.INTEGRATION_STATUS = A.INTEGRATION_STATUS + ''||''+convert(nvarchar,SYMSGS.MESSAGE_CODE),A.PROCESS_STATUS=''ERROR'' FROM "+str(Table_Name)+"(NOLOCK) A LEFT JOIN SYMSGS(NOLOCK) ON SYMSGS.MESSAGE_CODE = ''200104'' WHERE A.PROCESS_STATUS IN (''Inprogress'',''ERROR'') AND SYMSGS.OBJECT_APINAME = ''PREXRT'' AND a.TIMESTAMP='"	+ str(timestamp_sessionid)+ "'  AND ISNULL(FROM_CURRENCY,'''') = '''''")

			primaryQueryItems = SqlHelper.GetFirst(	""+ str(Parameter1.QUERY_CRITERIA_1)+ "  A SET A.INTEGRATION_STATUS = A.INTEGRATION_STATUS + ''||''+convert(nvarchar,SYMSGS.MESSAGE_CODE),A.PROCESS_STATUS=''ERROR'' FROM "+str(Table_Name)+"(NOLOCK) A LEFT JOIN SYMSGS(NOLOCK) ON SYMSGS.MESSAGE_CODE = ''200105'' WHERE A.PROCESS_STATUS IN (''Inprogress'',''ERROR'') AND SYMSGS.OBJECT_APINAME = ''PREXRT'' AND a.TIMESTAMP='"	+ str(timestamp_sessionid)+ "'  AND ISNULL(TO_CURRENCY,'''') = '''''")		

			#Status Change to READY FOR UPLOAD
			primaryQueryItems = SqlHelper.GetFirst(  
			""
			+ str(Parameter1.QUERY_CRITERIA_1)
			+ "  A SET PROCESS_STATUS = ''READY FOR UPLOAD'' FROM "+str(Table_Name)+" (NOLOCK) A WHERE ISNULL(PROCESS_STATUS,'''')IN (''INPROGRESS'') AND TIMESTAMP = '"+str(timestamp_sessionid)+"' '")
			
			#Update query of PREXRT
			primaryQueryItems = SqlHelper.GetFirst(	""+ str(Parameter1.QUERY_CRITERIA_1)+ "  PREXRT SET PREXRT.CpqTableEntryModifiedBy = ''"	+ str(User.Id)	+ "'',PREXRT.CpqTableEntryDateModified = GetDate(),PREXRT.EXCHANGE_RATE = A.EXCHANGE_RATE,PREXRT.RATIO_FROM = A.RATIO_FROM, PREXRT.RATIO_TO = A.RATIO_TO FROM "+str(Table_Name)+"(NOLOCK) A JOIN PREXRT(NOLOCK)  ON A.TO_CURRENCY = PREXRT.TO_CURRENCY AND A.FROM_CURRENCY = PREXRT.FROM_CURRENCY AND CONVERT(DATE,A.EXCHANGE_RATE_DATE) = CONVERT(DATE,PREXRT.EXCHANGE_RATE_BEGIN_DATE) AND A.EXCHANGE_RATE_TYPE = PREXRT.EXCHANGE_RATE_TYPE WHERE A.PROCESS_STATUS = ''READY FOR UPLOAD''  AND ISNULL(A.INTEGRATION_STATUS,'''') = '''' AND A.TIMESTAMP='"+ str(timestamp_sessionid)+ "'  ' ")
			
			#Insert query of PREXRT
			primaryQueryItems = SqlHelper.GetFirst(	""+ str(Parameter.QUERY_CRITERIA_1)	+ " PREXRT (ACTIVE,EXCHANGE_RATE,EXCHANGE_RATE_TYPE,FROM_CURRENCY,FROM_CURRENCY_RECORD_ID,RATIO_FROM,RATIO_TO,TO_CURRENCY,TO_CURRENCY_RECORD_ID,EXCHANGE_RATE_BEGIN_DATE,EXCHANGE_RATE_END_DATE,EXCHANGE_RATE_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED)SELECT SUB_PREXRT.*, CONVERT(VARCHAR(4000),NEWID()),''"+ str(User.UserName)+ "'',GETDATE() FROM (SELECT DISTINCT ''TRUE'' AS ACTIVE,CONVERT(DECIMAL(13,5),A.EXCHANGE_RATE) AS EXCHANGE_RATE,A.EXCHANGE_RATE_TYPE,A.FROM_CURRENCY,PRCURR1.CURRENCY_RECORD_ID AS FROM_CURRENCY_RECORD_ID,A.RATIO_FROM,A.RATIO_TO,A.TO_CURRENCY,PRCURR.CURRENCY_RECORD_ID AS TO_CURRENCY_RECORD_ID,CONVERT(DATE,A.EXCHANGE_RATE_DATE) AS EXCHANGE_RATE_BEGIN_DATE,CONVERT(DATE,A.EXCHANGE_RATE_DATE) AS EXCHANGE_RATE_END_DATE FROM "+str(Table_Name)+"(NOLOCK) A JOIN PRCURR(NOLOCK) on A.TO_CURRENCY = PRCURR.CURRENCY JOIN PRCURR(NOLOCK) PRCURR1 ON A.FROM_CURRENCY = PRCURR1.CURRENCY WHERE A.PROCESS_STATUS = ''READY FOR UPLOAD''  AND ISNULL(A.INTEGRATION_STATUS,'''') = '''' AND a.TIMESTAMP='"+ str(timestamp_sessionid)+ "')SUB_PREXRT LEFT JOIN PREXRT(NOLOCK) ON SUB_PREXRT.TO_CURRENCY = PREXRT.TO_CURRENCY AND PREXRT.FROM_CURRENCY = SUB_PREXRT.FROM_CURRENCY AND CONVERT(DATE,SUB_PREXRT.EXCHANGE_RATE_BEGIN_DATE) = CONVERT(DATE,PREXRT.EXCHANGE_RATE_BEGIN_DATE) AND SUB_PREXRT.EXCHANGE_RATE_TYPE = PREXRT.EXCHANGE_RATE_TYPE WHERE PREXRT.EXCHANGE_RATE_BEGIN_DATE IS NULL '")

			
			
			#Exchage Rate Errors mail system 
			Error_list = []
			Resp_msg = {}
			Lst_resp = []
			
			primaryQueryItems = SqlHelper.GetList("select distinct EXCHANGE_RATE_DATE AS sap_part_number,INTEGRATION_STATUS from "+str(Table_Name)+" (nolock) where isnull(INTEGRATION_STATUS,'')<>'' AND INTEGRATION_NAME = 'EXCHANGERATE_DATA' AND   timestamp = "+str(timestamp_sessionid)+" ")

			S=SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET ACTIVE=''TRUE'' FROM PREXRT A(NOLOCK) JOIN (SELECT FROM_CURRENCY,TO_CURRENCY,EXCHANGE_RATE_TYPE,MAX(EXCHANGE_RATE_BEGIN_DATE) AS EXCHANGE_RATE_BEGIN_DATE FROM PREXRT(NOLOCK) GROUP BY FROM_CURRENCY,TO_CURRENCY,EXCHANGE_RATE_TYPE)B ON A.FROM_CURRENCY = B.FROM_CURRENCY AND A.TO_CURRENCY = B.TO_CURRENCY AND A.EXCHANGE_RATE_TYPE = B.EXCHANGE_RATE_TYPE AND CONVERT(VARCHAR(11),A.EXCHANGE_RATE_BEGIN_DATE,121) = CONVERT(VARCHAR(11),B.EXCHANGE_RATE_BEGIN_DATE,121) ' ")

			S=SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET ACTIVE=''FALSE'' FROM PREXRT A(NOLOCK) JOIN (SELECT FROM_CURRENCY,TO_CURRENCY,EXCHANGE_RATE_TYPE,MAX(EXCHANGE_RATE_BEGIN_DATE) AS EXCHANGE_RATE_BEGIN_DATE FROM PREXRT(NOLOCK) GROUP BY FROM_CURRENCY,TO_CURRENCY,EXCHANGE_RATE_TYPE)B ON A.FROM_CURRENCY = B.FROM_CURRENCY AND A.TO_CURRENCY = B.TO_CURRENCY AND A.EXCHANGE_RATE_TYPE = B.EXCHANGE_RATE_TYPE AND CONVERT(VARCHAR(11),A.EXCHANGE_RATE_BEGIN_DATE,121) <> CONVERT(VARCHAR(11),B.EXCHANGE_RATE_BEGIN_DATE,121) ' ")

			#Remove Temp Table
			TempTable = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(Table_Name)+"'' ) BEGIN DROP TABLE "+str(Table_Name)+" END'")
		
			ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "200", "Message": "Exchange Rate Data successfully uploaded"}]})
		
			'''Dt = {}
			if len(primaryQueryItems) > 0:
				for ins in primaryQueryItems:
					Modi_integration_status = []
					inte_status = str(ins.ERROR).split("||")
					ERROR = set(inte_status)
					ERROR = list(ERROR)
					if "" in ERROR:
						ERROR.remove("")
					
					for uu in ERROR:
						split_data = uu.split("-", 1)
						SYMSGS_MSG_TEXT = SqlHelper.GetFirst(
							"SELECT MESSAGE_TEXT,RECORD_ID AS REC_ID,OBJECT_APINAME,OBJECT_RECORD_ID,MESSAGE_TYPE FROM SYMSGS(NOLOCK) WHERE MESSAGE_CODE = '"
							+ str(split_data[0])
							+ "'"
						)
						if len(split_data) > 1:
							CONVERTED_MSG = SYMSGS_MSG_TEXT.MESSAGE_TEXT + " - " + split_data[-1]
						else:
							CONVERTED_MSG = SYMSGS_MSG_TEXT.MESSAGE_TEXT
						Modi_integration_status.append(CONVERTED_MSG)
						
						
					if str(ins.sap_part_number) in Dt:
						for data in Modi_integration_status:
							if data not in Dt[ins.sap_part_number]:
								Dt[ins.sap_part_number].append(data)
					else:
						Dt[ins.sap_part_number] = Modi_integration_status
						
					for sap_part_number in Dt:
						inte_status_info = ""
						# Log.Info("232323 sap_part_number--->"+str(sap_part_number))
						for data in Dt[sap_part_number]:
							inte_status_info = inte_status_info + data + "||"
						Error_list.append(sap_part_number + "--" + inte_status_info[:-2])
				#Mail system
				if len(Error_list) > 0:
					Header = "<!DOCTYPE html><html><head><style>table {font-family: Calibri, sans-serif; border-collapse: collapse; width: 75%}td, th {  border: 1px solid #dddddd;  text-align: left; padding: 8px;}.im {color: #222;}tr:nth-child(even) {background-color: #dddddd;}</style></head><body>"
					Table_start = "<p>Hi Team,<br>Please find the below exceptions for your reference</p><table class='table table-bordered'><tr><th>SNO</th><th>EXCHANGE_RATE_DATE</th><th>ERROR MESSAGE</th></tr>"
					Table_End = "</table><p><strong>Note : </strong>Please do not reply to this email.</p></body></html>"
					Table_info = ""
					unique_Error_list = set(Error_list)
					for indx, data in enumerate(unique_Error_list, 1):
						data = data.split("--")
						Table_record = (
							"<tr>"
							+ "<td>"
							+ str(indx)
							+ "</td>"
							+ "<td>"
							+ str(data[0])
							+ "</td>"
							+ "<td>"
							+ str(data[-1])
							+ "</td>"
							+ "</tr>"
						)
						Table_info = Table_info + Table_record
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
					msg.Subject = "AMAT INTEGRATION MATMAS EXCEPTIONS - CPQ(X-Tenant)"
					msg.IsBodyHtml = True
					msg.Body = Error_Info
					# CC Emails	
					copyEmail5 = MailAddress("suresh.muniyandi@bostonharborconsulting.com")
					msg.CC.Add(copyEmail5)
					
					copyEmail4 = MailAddress("baji.baba@bostonharborconsulting.com")
					msg.CC.Add(copyEmail4)
					
					# Send the message
					mailClient.Send(msg)
			
			else:
				ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "200", "Message": "Exchange Rate Data successfully uploaded"}]})'''
				
		
		else:
			ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "200", "Message": "Data not available for syncronization"}]})
		
	except:
		
		TempTable = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(Table_Name)+"'' ) BEGIN DROP TABLE "+str(Table_Name)+" END CREATE TABLE "+str(Table_Name)+" (SESSION_ID VARCHAR(100),FROM_CURRENCY VARCHAR(100) ,TO_CURRENCY VARCHAR(100) ,EXCHANGE_RATE VARCHAR(100),EXCHANGE_RATE_DATE VARCHAR(100),EXCHANGE_RATE_TYPE VARCHAR(100),RATIO_FROM VARCHAR(100),RATIO_TO VARCHAR(100),TIMESTAMP VARCHAR(100),PROCESS_STATUS VARCHAR(100),INTEGRATION_STATUS VARCHAR(MAX))'")
		
		Log.Info("PRPOSTEXRT ERROR---->:" + str(sys.exc_info()[1]))
		Log.Info("PRPOSTEXRT ERROR LINE NO---->:" + str(sys.exc_info()[-1].tb_lineno))
		ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "400", "Message": str(sys.exc_info()[1])}]})
else:
	ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "200", "Message": "NO DATA AVAILABLE FOR SYNCHRONIZATION"}]})
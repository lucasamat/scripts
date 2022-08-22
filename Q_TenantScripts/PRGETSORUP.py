## =========================================================================================================================================
#   __script_name : PRGETSORUP.PY
#   __script_description : THIS SCRIPT IS USED TO INSERT Labor Activity DATA FROM SYINPL TO PRLSOR TABLE
#   __primary_author__ : SURESH MUNIYANDI
#   __create_date : 29-07-2021
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
# CPQExchangeRateInbound
import SYTABACTIN as Table
import sys 
import datetime 

Parameter = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'SELECT' ")
Parameter1 = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'UPD' ")
Parameter2 = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'DEL' ")

try:
	Data_Flag = 0
	while Data_Flag == 0:
		Jsonquery = SqlHelper.GetList("SELECT  replace(integration_payload,'\\\\','\\') as INTEGRATION_PAYLOAD,cpqtableentryid From SYINPL(NOLOCK) WHERE INTEGRATION_NAME = 'Labor Activity' AND ISNULL(STATUS,'')='' ")
		Check_flag = 0
		primaryQueryItems = SqlHelper.GetFirst("SELECT NEWID() AS A")	
		timestamp_sessionid = "\'"+str(primaryQueryItems.A)+"\'"
		Error_Msg_lst = []
		Error_Msg_final = ''
		Table_Name = 'PRLSOR_INBOUND'

		if len(Jsonquery) > 0:
		
			TempTable = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(Table_Name)+"'' ) BEGIN DROP TABLE "+str(Table_Name)+" END CREATE TABLE "+str(Table_Name)+" (COST_CENTER VARCHAR(100) ,SALESORG_ID VARCHAR(10) ,LABORACTIVITY_ID VARCHAR(100),LABORACTIVITY_RATE VARCHAR(100),LABORACTIVITY_CURRENCY VARCHAR(100),SALESORG_RATE VARCHAR(100),SALESORG_CURRENCY VARCHAR(100),PRICING_INDICATOR VARCHAR(100),ACTIVITY_UNIT VARCHAR(100),PERIOD VARCHAR(100),YEAR VARCHAR(100),VALID_FROM VARCHAR(100),VALID_TO VARCHAR(100),TIMESTAMP VARCHAR(100),PROCESS_STATUS VARCHAR(100),INTEGRATION_STATUS VARCHAR(MAX),SESSION_ID VARCHAR(100))'")
			
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
							if str(tn).upper() == "PRLSOR":
								if str(type(rebuilt_data[tn])) == "<type 'dict'>":
									Tbl_data = [rebuilt_data[tn]]
								else:
									Tbl_data = rebuilt_data[tn]
								
								#Dynamic table creation of PRLSOR_INBOUND
								for record_dict in Tbl_data:
									Stagingquery = SqlHelper.GetFirst( ""+ str(Parameter.QUERY_CRITERIA_1)+ " "+str(Table_Name)+" (SESSION_ID ,COST_CENTER  ,SALESORG_ID  ,LABORACTIVITY_ID ,LABORACTIVITY_RATE ,LABORACTIVITY_CURRENCY ,SALESORG_RATE ,SALESORG_CURRENCY,PRICING_INDICATOR,ACTIVITY_UNIT,PERIOD,YEAR,VALID_FROM,VALID_TO  )  select  ''"+ str(primaryQuerysession.A)+ "'',''"+str(record_dict['COST_CENTER'])+ "'',''"+str(record_dict['SALESORG_ID'])+ "'',''"+str(record_dict['LABORACTIVITY_ID'])+ "'',''"+str(record_dict['LABORACTIVITY_RATE'])+ "'',''"+str(record_dict['LABORACTIVITY_CURRENCY'])+ "'',''"+str(record_dict['SALESORG_RATE'])+ "'',''"+str(record_dict['SALESORG_CURRENCY'])+ "'',''"+str(record_dict['PRICING_INDICATOR'])+ "'',''"+str(record_dict['ACTIVITY_UNIT'])+ "'',''"+str(record_dict['PERIOD'])+ "'',''"+str(record_dict['YEAR'])+ "'',''"+str(record_dict['VALID_FROM'])+ "'',''"+str(record_dict['VALID_TO'])+ "'' ' ")
			
					primaryItems = SqlHelper.GetFirst(  ""+ str(Parameter1.QUERY_CRITERIA_1)+ "  SYINPL set STATUS = ''PROCESSED'' from SYINPL  (NOLOCK) WHERE cpqtableentryid  = ''"+str(json_data.cpqtableentryid)+ "'' AND ISNULL(STATUS ,'''')= '''' ' "    )
			
			
			if Check_flag == 1:
			
				#Timestamp Update
				primaryQueryItems = SqlHelper.GetFirst(	""+ str(Parameter1.QUERY_CRITERIA_1)+ " "+str(Table_Name)+" SET TIMESTAMP = '"+ str(timestamp_sessionid)+ "' ,PROCESS_STATUS = ''INPROGRESS'' WHERE ISNULL(TIMESTAMP,'''')='''' AND ISNULL(PROCESS_STATUS,'''')=''''  '")
			
				#PRLSOR Does not Exist validations
				primaryQueryItems = SqlHelper.GetFirst(	""+ str(Parameter1.QUERY_CRITERIA_1)+ "  A SET A.INTEGRATION_STATUS = A.INTEGRATION_STATUS + ''||''+convert(nvarchar,SYMSGS.MESSAGE_CODE)+''-''+convert(nvarchar,A.SALESORG_ID),A.PROCESS_STATUS=''ERROR'' FROM "+str(Table_Name)+"(NOLOCK) A LEFT JOIN SASORG (NOLOCK) ON A.SALESORG_ID = SASORG.SALESORG_ID LEFT JOIN SYMSGS(NOLOCK) ON SYMSGS.MESSAGE_CODE = ''200107'' WHERE A.PROCESS_STATUS IN (''Inprogress'',''ERROR'') AND SYMSGS.OBJECT_APINAME = ''PRLSOR'' AND a.TIMESTAMP='"+ str(timestamp_sessionid)+ "'  AND SASORG.SALESORG_ID IS NULL AND A.SALESORG_ID <> '''' '")

				primaryQueryItems = SqlHelper.GetFirst(	""+ str(Parameter1.QUERY_CRITERIA_1)+ "  A SET A.INTEGRATION_STATUS = A.INTEGRATION_STATUS + ''||''+convert(nvarchar,SYMSGS.MESSAGE_CODE)+''-''+convert(nvarchar,A.SALESORG_CURRENCY),A.PROCESS_STATUS=''ERROR'' FROM "+str(Table_Name)+"(NOLOCK) A LEFT JOIN PRCURR (NOLOCK) ON A.SALESORG_CURRENCY = PRCURR.CURRENCY LEFT JOIN SYMSGS(NOLOCK) ON SYMSGS.MESSAGE_CODE = ''200108'' WHERE A.PROCESS_STATUS IN (''Inprogress'',''ERROR'') AND SYMSGS.OBJECT_APINAME = ''PRLSOR'' AND a.TIMESTAMP='"+ str(timestamp_sessionid)+ "'  AND PRCURR.CURRENCY IS NULL AND A.SALESORG_CURRENCY <> '''' '")

				#PRLSOR Mandatory  validations
				primaryQueryItems = SqlHelper.GetFirst(	""+ str(Parameter1.QUERY_CRITERIA_1)+ "  A SET A.INTEGRATION_STATUS = A.INTEGRATION_STATUS + ''||''+convert(nvarchar,SYMSGS.MESSAGE_CODE),A.PROCESS_STATUS=''ERROR'' FROM "+str(Table_Name)+"(NOLOCK) A LEFT JOIN SYMSGS(NOLOCK) ON SYMSGS.MESSAGE_CODE = ''200109'' WHERE A.PROCESS_STATUS IN (''Inprogress'',''ERROR'') AND SYMSGS.OBJECT_APINAME = ''PRLSOR'' AND a.TIMESTAMP='"	+ str(timestamp_sessionid)+ "'  AND ISNULL(SALESORG_ID,'''') = '''''")

				primaryQueryItems = SqlHelper.GetFirst(	""+ str(Parameter1.QUERY_CRITERIA_1)+ "  A SET A.INTEGRATION_STATUS = A.INTEGRATION_STATUS + ''||''+convert(nvarchar,SYMSGS.MESSAGE_CODE),A.PROCESS_STATUS=''ERROR'' FROM "+str(Table_Name)+"(NOLOCK) A LEFT JOIN SYMSGS(NOLOCK) ON SYMSGS.MESSAGE_CODE = ''200110'' WHERE A.PROCESS_STATUS IN (''Inprogress'',''ERROR'') AND SYMSGS.OBJECT_APINAME = ''PRLSOR'' AND a.TIMESTAMP='"	+ str(timestamp_sessionid)+ "'  AND ISNULL(SALESORG_CURRENCY,'''') = '''''")

					

				#Status Change to READY FOR UPLOAD
				primaryQueryItems = SqlHelper.GetFirst(  
				""
				+ str(Parameter1.QUERY_CRITERIA_1)
				+ "  A SET PROCESS_STATUS = ''READY FOR UPLOAD'' FROM "+str(Table_Name)+" (NOLOCK) A WHERE ISNULL(PROCESS_STATUS,'''')IN (''INPROGRESS'') AND TIMESTAMP = '"+str(timestamp_sessionid)+"' '")
				
				#PRLBAT INSERT IF DATA NOT THERE
				
				InsertQueryItems = SqlHelper.GetFirst(
		        ""
		        + str(Parameter.QUERY_CRITERIA_1)
		        + " PRLBAT (LABORACTIVITY_ID,CPQTABLEENTRYDATEADDED,LABORACTIVITY_RECORD_ID,LABORACTIVITY_NAME)SELECT A.*,GetDate() ,CONVERT(VARCHAR(4000),NEWID()),A.LABORACTIVITY_ID FROM (SELECT DISTINCT A.LABORACTIVITY_ID FROM "+str(Table_Name)+"(NOLOCK) A WHERE  A.PROCESS_STATUS = ''READY FOR UPLOAD'' AND ISNULL(A.INTEGRATION_STATUS,'''') = '''' AND A.TIMESTAMP='"+ str(timestamp_sessionid)+ "'   )A LEFT JOIN PRLBAT (NOLOCK) M ON A.LABORACTIVITY_ID=M.LABORACTIVITY_ID WHERE  M.LABORACTIVITY_ID IS NULL'"
		        )
				
				
				#Update query of PRLSOR
				primaryQueryItems = SqlHelper.GetFirst(	""+ str(Parameter1.QUERY_CRITERIA_1)+ "  PRLSOR SET PRLSOR.CpqTableEntryModifiedBy = ''"	+ str(User.Id)	+ "'',PRLSOR.CpqTableEntryDateModified = GetDate(), PRLSOR.LABOR_RATE_GLCURR= A.LABORACTIVITY_RATE,LABOR_RATE_SOCURR = A.SALESORG_RATE FROM "+str(Table_Name)+"(NOLOCK) A JOIN SASORG(NOLOCK) ON A.SALESORG_ID = SASORG.SALESORG_ID JOIN PRLSOR(NOLOCK)  ON A.LABORACTIVITY_ID = PRLSOR.LABORACTIVITY_ID AND A.SALESORG_ID = PRLSOR.SALESORG_ID AND A.PERIOD = PRLSOR.PERIOD AND A.YEAR = PRLSOR.YEAR AND CONVERT(VARCHAR(11),A.VALID_FROM,121) = CONVERT(VARCHAR(11),PRLSOR.VALID_FROM_DATE,121) AND CONVERT(VARCHAR(11),A.VALID_TO,121) = CONVERT(VARCHAR(11),PRLSOR.VALID_TO_DATE,121) AND A.COST_CENTER = PRLSOR.COST_CENTER WHERE A.PROCESS_STATUS = ''READY FOR UPLOAD''  AND ISNULL(A.INTEGRATION_STATUS,'''') = '''' AND A.TIMESTAMP='"+ str(timestamp_sessionid)+ "'  ' ")
				
				#Insert query of PRLSOR
				primaryQueryItems = SqlHelper.GetFirst(	""+ str(Parameter.QUERY_CRITERIA_1)	+ " PRLSOR (COST_CENTER,LABORACTIVITY_ID,LABORACTIVITY_NAME,LABORACTIVITY_RECORD_ID,LABOR_RATE_GLCURR,GLOBAL_CURRENCY,GLOBAL_CURRENCY_RECORD_ID,LABOR_RATE_SOCURR,SORG_CURRENCY,SORGCURRENCY_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,VALID_FROM_DATE,VALID_TO_DATE,YEAR,PERIOD,LBRACTSOR_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED)SELECT SUB_PRLSOR.*, CONVERT(VARCHAR(4000),NEWID()),''"+ str(User.UserName)+ "'',GETDATE() FROM (SELECT DISTINCT A.COST_CENTER,A.LABORACTIVITY_ID,PRLBAT.LABORACTIVITY_NAME,PRLBAT.LABORACTIVITY_RECORD_ID,A.LABORACTIVITY_RATE,PRCURR1.CURRENCY,PRCURR1.CURRENCY_RECORD_ID AS LABORCURRENCY,A.SALESORG_RATE,A.SALESORG_CURRENCY ,PRCURR.CURRENCY_RECORD_ID,A.SALESORG_ID,SASORG.SALESORG_NAME,SASORG.SALES_ORG_RECORD_ID,A.VALID_FROM,A.VALID_TO,A.YEAR,A.PERIOD FROM "+str(Table_Name)+"(NOLOCK) A JOIN PRCURR(NOLOCK) on A.SALESORG_CURRENCY = PRCURR.CURRENCY JOIN PRCURR PRCURR1(NOLOCK) on A.LABORACTIVITY_CURRENCY = PRCURR1.CURRENCY JOIN SASORG(NOLOCK)  ON A.SALESORG_ID = SASORG.SALESORG_ID JOIN PRLBAT(NOLOCK) ON A.LABORACTIVITY_ID = PRLBAT.LABORACTIVITY_ID WHERE A.PROCESS_STATUS = ''READY FOR UPLOAD''  AND ISNULL(A.INTEGRATION_STATUS,'''') = '''' AND a.TIMESTAMP='"+ str(timestamp_sessionid)+ "')SUB_PRLSOR LEFT JOIN PRLSOR(NOLOCK) ON SUB_PRLSOR.LABORACTIVITY_ID = PRLSOR.LABORACTIVITY_ID AND SUB_PRLSOR.SALESORG_ID = PRLSOR.SALESORG_ID AND SUB_PRLSOR.PERIOD = PRLSOR.PERIOD AND SUB_PRLSOR.YEAR = PRLSOR.YEAR AND CONVERT(VARCHAR(11),SUB_PRLSOR.VALID_FROM,121) = CONVERT(VARCHAR(11),PRLSOR.VALID_FROM_DATE,121) AND CONVERT(VARCHAR(11),SUB_PRLSOR.VALID_TO,121) = CONVERT(VARCHAR(11),PRLSOR.VALID_TO_DATE,121) AND SUB_PRLSOR.COST_CENTER = PRLSOR.COST_CENTER WHERE PRLSOR.LABORACTIVITY_ID IS NULL '")

				
				#Remove Temp Table
				TempTable = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(Table_Name)+"'' ) BEGIN DROP TABLE "+str(Table_Name)+" END'")
			
				ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "200", "Message": "Labor Activity Data successfully uploaded"}]})

			else:
				ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "200", "Message": "Data not available for syncronization"}]})
				
		else:
			Data_Flag = 1	
		
	
except:
	Table_Name = 'PRLSOR_INBOUND'
	#Remove Temp Table
	TempTable = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(Table_Name)+"'' ) BEGIN DROP TABLE "+str(Table_Name)+" END'")
	
	Log.Info("PRGETSORUP ERROR---->:" + str(sys.exc_info()[1]))
	Log.Info("PRGETSORUP ERROR LINE NO---->:" + str(sys.exc_info()[-1].tb_lineno))
	ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "400", "Message": str(sys.exc_info()[1])}]})
	
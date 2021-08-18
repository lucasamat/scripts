#=============================================================================================================================
#   __script_name : SAGETEMPUP.PY
#   __script_description : THIS SCRIPT IS USED TO INSERT/UPDATE EMPLOYEE DATA FROM WORKDAY
#   __primary_author__ : SURESH MUNIYANDI,BAJI
#   __create_date : 12-08-2021
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==============================================================================================================================
import sys 
import datetime 

Parameter = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'SELECT' ")
Parameter1 = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'UPD' ")
Parameter2 = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'DEL' ")

try:
	While_flag = 1
	while While_flag == 1:
		Jsonquery = SqlHelper.GetList("SELECT  replace(integration_payload,'\\\\','\\') as INTEGRATION_PAYLOAD,CpqTableEntryId from SYINPL(NOLOCK) WHERE INTEGRATION_NAME = 'EMPLOYEE_DATA' AND ISNULL(STATUS,'')='' ")
	
		if len(Jsonquery) > 0:
		
			Check_flag = 0
			primaryQuerysession = SqlHelper.GetFirst("SELECT NEWID() AS A")	
			timestamp_sessionid = "\'"+str(primaryQuerysession.A)+"\'"
			
			Table_Name = 'SAEMPL_INBOUND'
			
			#Dynamic table creation 			
			TempTable = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(Table_Name)+"'' ) BEGIN DROP TABLE "+str(Table_Name)+" END CREATE TABLE "+str(Table_Name)+" (SESSION_ID VARCHAR(100),EMPLOYEE_ID VARCHAR(100) ,EMPLOYEE_NAME VARCHAR(MAX),FIRST_NAME VARCHAR(100),LAST_NAME VARCHAR(100),ADDRESS_1 VARCHAR(MAX),CITY VARCHAR(100),	COUNTRY VARCHAR(100),EMAIL VARCHAR(100),STATE VARCHAR(100),PHONE VARCHAR(100),POSTAL_CODE VARCHAR(100),CRM_EMPLOYEE_ID VARCHAR(100),TIMESTAMP VARCHAR(100),PROCESS_STATUS VARCHAR(100),INTEGRATION_STATUS VARCHAR(MAX))'")
			
			for json_data in Jsonquery:
				if "Param" in str(json_data.INTEGRATION_PAYLOAD):
					splited_list = str(json_data.INTEGRATION_PAYLOAD).split("'")
					rebuilt_data = eval(str(splited_list[1]))
				else:
					splited_list = str(json_data.INTEGRATION_PAYLOAD)
					rebuilt_data = eval(splited_list)				

				if len(rebuilt_data) != 0:      

					rebuilt_data = rebuilt_data["CPQ_Columns"]
					Table_Names = rebuilt_data.keys()
					
					for tn in Table_Names:
						if tn in rebuilt_data:
							Check_flag = 1
							if str(tn).upper() == "SAEMPL":
								if str(type(rebuilt_data[tn])) == "<type 'dict'>":
									Tbl_data = [rebuilt_data[tn]]
								else:
									Tbl_data = rebuilt_data[tn]
								
								SessionQuery =  SqlHelper.GetFirst("SELECT NEWID() AS Guid")
								
								#Storing data in staging table SAEMPL_INBOUND
								for record_dict in Tbl_data:
									Stagingquery = SqlHelper.GetFirst( ""+ str(Parameter.QUERY_CRITERIA_1)+ " "+str(Table_Name)+" (SESSION_ID,EMPLOYEE_ID ,EMPLOYEE_NAME ,FIRST_NAME ,LAST_NAME,ADDRESS_1,CITY,COUNTRY,EMAIL,STATE,PHONE,POSTAL_CODE,CRM_EMPLOYEE_ID )  select  ''"+ str(SessionQuery.Guid)+ "'',''"+str(record_dict['EMPLOYEE_ID'])+ "'',''"+str(record_dict['EMPLOYEE_NAME'])+ "'',''"+str(record_dict['FIRST_NAME'])+ "'',''"+str(record_dict['LAST_NAME'])+ "'',''"+str(record_dict['ADDRESS_1'])+ "'',''"+str(record_dict['CITY'])+ "'',''"+str(record_dict['COUNTRY'])+ "'' ,''"+str(record_dict['EMAIL'])+ "''',''"+str(record_dict['STATE'])+ "'',''"+str(record_dict['PHONE'])+ "'',''"+str(record_dict['POSTAL_CODE'])+ "'',''"+str(record_dict['CRM_EMPLOYEE_ID'])+ "'' ")
			
					primaryItems = SqlHelper.GetFirst(  ""+ str(Parameter1.QUERY_CRITERIA_1)+ "  SYINPL set STATUS = ''PROCESSED'' from SYINPL  (NOLOCK) WHERE cpqtableentryid  = ''"+str(json_data.cpqtableentryid)+ "'' AND ISNULL(STATUS ,'''')= '''' ' "    )
			
			
			if Check_flag == 1:
			
				#Timestamp Update
				primaryQueryItems = SqlHelper.GetFirst(	""+ str(Parameter1.QUERY_CRITERIA_1)+ " "+str(Table_Name)+" SET TIMESTAMP = '"+ str(timestamp_sessionid)+ "' ,PROCESS_STATUS = ''INPROGRESS'' WHERE ISNULL(TIMESTAMP,'''')='''' AND ISNULL(PROCESS_STATUS,'''')=''''  '")
			
				#SAEMPL Does not Exist validations
				primaryQueryItems = SqlHelper.GetFirst(	""+ str(Parameter1.QUERY_CRITERIA_1)+ "  A SET A.INTEGRATION_STATUS = A.INTEGRATION_STATUS + ''||''+convert(nvarchar,SYMSGS.MESSAGE_CODE)+''-''+convert(nvarchar,A.COUNTRY),A.PROCESS_STATUS=''ERROR'' FROM "+str(Table_Name)+"(NOLOCK) A LEFT JOIN SACTRY (NOLOCK) ON A.COUNTRY = SACTRY.COUNTRY LEFT JOIN SYMSGS(NOLOCK) ON SYMSGS.MESSAGE_CODE = ''200113'' WHERE A.PROCESS_STATUS IN (''Inprogress'',''ERROR'') AND SYMSGS.OBJECT_APINAME = ''SAEMPL'' AND a.TIMESTAMP='"+ str(timestamp_sessionid)+ "'  AND SACTRY.COUNTRY IS NULL AND A.COUNTRY <> '''' '")

				primaryQueryItems = SqlHelper.GetFirst(	""+ str(Parameter1.QUERY_CRITERIA_1)+ "  A SET A.INTEGRATION_STATUS = A.INTEGRATION_STATUS + ''||''+convert(nvarchar,SYMSGS.MESSAGE_CODE)+''-''+convert(nvarchar,A.STATE),A.PROCESS_STATUS=''ERROR'' FROM "+str(Table_Name)+"(NOLOCK) A LEFT JOIN SACYST (NOLOCK) ON A.STATE = SACYST.STATE LEFT JOIN SYMSGS(NOLOCK) ON SYMSGS.MESSAGE_CODE = ''200114'' WHERE A.PROCESS_STATUS IN (''Inprogress'',''ERROR'') AND SYMSGS.OBJECT_APINAME = ''SAEMPL'' AND a.TIMESTAMP='"+ str(timestamp_sessionid)+ "'  AND SACYST.STATE IS NULL AND A.STATE <> '''' '")

				#SAEMPL Mandatory  validations
				primaryQueryItems = SqlHelper.GetFirst(	""+ str(Parameter1.QUERY_CRITERIA_1)+ "  A SET A.INTEGRATION_STATUS = A.INTEGRATION_STATUS + ''||''+convert(nvarchar,SYMSGS.MESSAGE_CODE),A.PROCESS_STATUS=''ERROR'' FROM "+str(Table_Name)+"(NOLOCK) A LEFT JOIN SYMSGS(NOLOCK) ON SYMSGS.MESSAGE_CODE = ''200117'' WHERE A.PROCESS_STATUS IN (''Inprogress'',''ERROR'') AND SYMSGS.OBJECT_APINAME = ''SAEMPL'' AND a.TIMESTAMP='"	+ str(timestamp_sessionid)+ "'  AND ISNULL(EMPLOYEE_ID,'''') = '''''")		

				#Status Change to READY FOR UPLOAD
				primaryQueryItems = SqlHelper.GetFirst(  
				""
				+ str(Parameter1.QUERY_CRITERIA_1)
				+ "  A SET PROCESS_STATUS = ''READY FOR UPLOAD'' FROM "+str(Table_Name)+" (NOLOCK) A WHERE ISNULL(PROCESS_STATUS,'''')IN (''INPROGRESS'') AND TIMESTAMP = '"+str(timestamp_sessionid)+"' '")
				
				#Update query of SAEMPL
				primaryQueryItems = SqlHelper.GetFirst(	""+ str(Parameter1.QUERY_CRITERIA_1)+ "  SAEMPL SET SAEMPL.CpqTableEntryModifiedBy = ''"+ str(User.Id)+ "'',SAEMPL.CpqTableEntryDateModified = GetDate(),SAEMPL.ADDRESS_1 = A.ADDRESS_1,SAEMPL.CITY = A.CITY, SAEMPL.COUNTRY = A.COUNTRY,SAEMPL.COUNTRY_RECORD_ID = SACTRY.COUNTRY_RECORD_ID,SAEMPL.EMAIL = A.EMAIL, SAEMPL.EMPLOYEE_NAME = A.EMPLOYEE_NAME,SAEMPL.FIRST_NAME = A.FIRST_NAME, SAEMPL.LAST_NAME = A.LAST_NAME,SAEMPL.PHONE = A.PHONE,SAEMPL.POSTAL_CODE = A.POSTAL_CODE, SAEMPL.STATE = A.STATE, SAEMPL.STATE_RECORD_ID = SACYST.STATE_RECORD_ID,SAEMPL.CRM_EMPLOYEE_ID = A.CRM_EMPLOYEE_ID FROM "+str(Table_Name)+"(NOLOCK) A LEFT JOIN SACTRY(NOLOCK)  ON A.COUNTRY = SACTRY.COUNTRY LEFT JOIN SACYST(NOLOCK) ON A.COUNTRY = SACYST.COUNTRY AND A.STATE = SACYST.STATE JOIN SAEMPL (NOLOCK) ON A.EMPLOYEE_ID = SAEMPL.EMPLOYEE_ID WHERE A.PROCESS_STATUS = ''READY FOR UPLOAD''  AND ISNULL(A.INTEGRATION_STATUS,'''') = '''' AND A.TIMESTAMP='"+ str(timestamp_sessionid)+ "'  ' ")
				
				#Insert query of SAEMPL
				primaryQueryItems = SqlHelper.GetFirst(	""+ str(Parameter.QUERY_CRITERIA_1)	+ " SAEMPL (ADDRESS_1,CITY,COUNTRY,COUNTRY_RECORD_ID,EMAIL,EMPLOYEE_ID,EMPLOYEE_NAME,FIRST_NAME,LAST_NAME,PHONE,POSTAL_CODE,STATE,STATE_RECORD_ID,CRM_EMPLOYEE_ID,EMPLOYEE_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED)SELECT SUB_SAEMPL.*, CONVERT(VARCHAR(4000),NEWID()),''"+ str(User.UserName)+ "'',GETDATE() FROM (SELECT DISTINCT A.ADDRESS_1,A.CITY,A.COUNTRY,SACTRY.COUNTRY_RECORD_ID,A.EMAIL,A.EMPLOYEE_ID,A.EMPLOYEE_NAME,A.FIRST_NAME,A.LAST_NAME,A.PHONE,A.POSTAL_CODE,A.STATE,SACYST.STATE_RECORD_ID,A.CRM_EMPLOYEE_ID FROM "+str(Table_Name)+"(NOLOCK) A LEFT JOIN SACTRY(NOLOCK) on A.COUNTRY = SACTRY.COUNTRY LEFT JOIN SACYST(NOLOCK)  ON A.COUNTRY = SACYST.COUNTRY AND A.STATE = SACYST.STATE WHERE A.PROCESS_STATUS = ''READY FOR UPLOAD''  AND ISNULL(A.INTEGRATION_STATUS,'''') = '''' AND a.TIMESTAMP='"+ str(timestamp_sessionid)+ "')SUB_SAEMPL LEFT JOIN SAEMPL(NOLOCK) ON SUB_SAEMPL.EMPLOYEE_ID = SAEMPL.EMPLOYEE_ID WHERE SAEMPL.EMPLOYEE_ID IS NULL '")	
				
				#Remove Temp Table
				TempTable = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(Table_Name)+"'' ) BEGIN DROP TABLE "+str(Table_Name)+" END'")
			
				ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "200", "Message": "Employee Data successfully uploaded"}]})					
			
			else:
				ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "200", "Message": "Data not available for syncronization"}]})
		else:
			While_flag = 0
except:
	
	Table_Name = 'SAEMPL_INBOUND'
	
	TempTable = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(Table_Name)+"'' ) BEGIN DROP TABLE "+str(Table_Name)+" END'")
	
	Log.Info("SAGETEMPUP ERROR---->:" + str(sys.exc_info()[1]))
	Log.Info("SAGETEMPUP ERROR LINE NO---->:" + str(sys.exc_info()[-1].tb_lineno))
	ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "400", "Message": str(sys.exc_info()[1])}]})
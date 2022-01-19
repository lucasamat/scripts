# =========================================================================================================================================
#   __script_name : SAGETCVHUP.PY
#   __script_description : THIS SCRIPT IS USED TO CONNECTING HANA DB AND FETCHING DATA
#   __primary_author__ : BAJI
#   __create_date :
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================

try:
	import clr
	import System.Net
	from System.Text.Encoding import UTF8
	from System import Convert
	import sys
	
	Parameter = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'SELECT' ")
	Parameter1 = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'UPD' ")
	Parameter2 = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'DEL' ")

	LOGIN_CREDENTIALS = SqlHelper.GetFirst("SELECT USER_NAME,Password,URL FROM SYCONF where EXTERNAL_TABLE_NAME='HANA_CONNECTION'")
	if LOGIN_CREDENTIALS is not None:

		Login_Username = str(LOGIN_CREDENTIALS.USER_NAME)
		Login_Password = str(LOGIN_CREDENTIALS.Password)
		authorization = Login_Username+":"+Login_Password
		binaryAuthorization = UTF8.GetBytes(authorization)
		authorization = Convert.ToBase64String(binaryAuthorization)
		authorization = "Basic " + authorization


		webclient = System.Net.WebClient()
		webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/json"
		webclient.Headers[System.Net.HttpRequestHeader.Authorization] = authorization;

		#SACRVC

		Table_Name = 'SACRVC_INBOUND'

		TempTable = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(Table_Name)+"'' ) BEGIN DROP TABLE "+str(Table_Name)+" END CREATE TABLE "+str(Table_Name)+" (MANDT VARCHAR(250) ,BUKRS VARCHAR(250) ,HKONT VARCHAR(250) ,ZUONR VARCHAR(250) ,GJAHR VARCHAR(250) ,BELNR VARCHAR(250) ,	BUZEI VARCHAR(250) ,BUDAT VARCHAR(250) ,ZAFTYPE VARCHAR(250) ,ZAFSP VARCHAR(250) ,KUNAG	VARCHAR(250) ,SPART VARCHAR(250) ,	WRBTR VARCHAR(250) ,WAERS VARCHAR(250) ,ZAFGBOOK VARCHAR(250) ,	ZAFKPU	VARCHAR(250) ,ZAFPLATFORM VARCHAR(250) ,ZAFTECHNO VARCHAR(250) ,ZAFWAFER VARCHAR(250) ,	ZAFTOOL_ID VARCHAR(250) ,ZAFSHIP_DATE VARCHAR(250) ,ZAFEXPIRY_DATE VARCHAR(250) ,	ZAF_UDATE VARCHAR(250) ,ZAF_UTIME VARCHAR(250) )'")	

		start =1
		end = 10000
		check_flag1 = 1
		while check_flag1 == 1:

			req_input = '{"query":"select * from (select *,row_number () over (order by hkont) as sno from zaf0470)a where sno>='+str(start)+' and sno<='+str(end)+'"}'

			response2 = webclient.UploadString(str(LOGIN_CREDENTIALS.URL), str(req_input))

			response = eval(response2)
			if str(type(response)) == "<type 'dict'>":
				response = [response]

			if len(response) > 0:			

				for record_dict in response:

					Stagingquery = SqlHelper.GetFirst( ""+ str(Parameter.QUERY_CRITERIA_1)+ " "+str(Table_Name)+" (HKONT, ZAFPLATFORM, ZAF_UDATE, ZAFTOOL_ID, ZAFWAFER, ZAFSHIP_DATE, GJAHR, ZAFKPU, ZAFTYPE, ZAF_UTIME, BUDAT, ZAFSP, ZAFTECHNO, BUZEI, ZAFEXPIRY_DATE, WRBTR, BELNR, BUKRS, ZAFGBOOK, SPART, ZUONR, KUNAG, MANDT, WAERS )  select  N''"+str(record_dict['HKONT'])+ "'',''"+str(record_dict['ZAFPLATFORM'])+ "'',''"+str(record_dict['ZAF_UDATE'])+ "'',''"+str(record_dict['ZAFTOOL_ID'])+ "'',''"+str(record_dict['ZAFWAFER'])+ "'',''"+str(record_dict['ZAFSHIP_DATE'])+ "'',''"+str(record_dict['GJAHR'])+ "'',''"+str(record_dict['ZAFKPU'])+ "'',''"+str(record_dict['ZAFTYPE'])+ "'',''"+str(record_dict['ZAF_UTIME'])+ "'',''"+str(record_dict['BUDAT'])+ "'',''"+str(record_dict['ZAFSP'])+ "'',''"+str(record_dict['ZAFTECHNO'])+ "'',''"+str(record_dict['BUZEI'])+ "'',''"+str(record_dict['ZAFEXPIRY_DATE'])+ "'',''"+str(record_dict['WRBTR'])+ "'',''"+str(record_dict['BELNR'])+ "'',''"+str(record_dict['BUKRS'])+ "'',''"+str(record_dict['ZAFGBOOK'])+ "'',''"+str(record_dict['SPART'])+ "'',''"+str(record_dict['ZUONR'])+ "'',''"+str(record_dict['KUNAG'])+ "'',''"+str(record_dict['MANDT'])+ "'' ,''"+str(record_dict['WAERS'])+ "''  ' ")

				start = start + 10000
				end = end + 10000

			else:
				check_flag1 = 0


		#SACVNT

		Table_Name = 'SACVNT_INBOUND' 

		TempTable = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(Table_Name)+"'' ) BEGIN DROP TABLE "+str(Table_Name)+" END CREATE TABLE "+str(Table_Name)+" (HKONT VARCHAR(250), ZAF_UDATE VARCHAR(250), MANDT VARCHAR(250), ZAF_UTIME VARCHAR(250), ZAFNOTE VARCHAR(250), ZUONR VARCHAR(250), GJAHR VARCHAR(250), BUZEI VARCHAR(250), ZAFNOTE_ID VARCHAR(250), BELNR VARCHAR(250), BUKRS VARCHAR(250))'")	


		start =1
		end = 10000
		check_flag2 = 1
		while check_flag2 == 1:
			req_input = '{"query":"select * from (select *,row_number () over (order by hkont) as sno from zaf0471)a where sno>='+str(start)+' and sno<='+str(end)+'"}'

			response2 = webclient.UploadString(str(LOGIN_CREDENTIALS.URL), str(req_input))

			response = eval(response2)
			if str(type(response)) == "<type 'dict'>":
				response = [response]

			if len(response) > 0:			

				for record_dict in response:

					Stagingquery = SqlHelper.GetFirst( ""+ str(Parameter.QUERY_CRITERIA_1)+ " "+str(Table_Name)+" (HKONT, ZAF_UDATE, MANDT, ZAF_UTIME, ZAFNOTE, ZUONR, GJAHR, BUZEI, ZAFNOTE_ID, BELNR, BUKRS)  select  N''"+str(record_dict['HKONT'])+ "'',''"+str(record_dict['ZAF_UDATE'])+ "'',''"+str(record_dict['MANDT'])+ "'',''"+str(record_dict['ZAF_UTIME'])+ "'',''"+record_dict['ZAFNOTE']+ "'',''"+str(record_dict['ZUONR'])+ "'',''"+str(record_dict['GJAHR'])+ "'',''"+str(record_dict['BUZEI'])+ "'',''"+str(record_dict['ZAFNOTE_ID'])+ "'',''"+str(record_dict['BELNR'])+ "'',''"+str(record_dict['BUKRS'])+ "''  ' ")

				start = start + 10000
				end = end + 10000

			else:

				check_flag2 = 0
		
		
		#SACRVC Insert Query  
		
		primaryQueryItems = SqlHelper.GetFirst(""+ str(Parameter1.QUERY_CRITERIA_1)+ "  SACRVC_INBOUND SET ZAFSHIP_DATE = null FROM SACRVC_INBOUND(NOLOCK) where ZAFSHIP_DATE = ''00000000''    '") 
		
		primaryQueryItems = SqlHelper.GetFirst(
			""
			+ str(Parameter.QUERY_CRITERIA_1)
			+ " SACRVC (SPART,ZAF_UTIME ,HKONT, ZAFPLATFORM, ZAFTOOL_ID, ZAFWAFER, GJAHR, ZAFKPU, ZAFTYPE, ZAFSP, ZAFTECHNO, BUZEI,  WRBTR, BELNR, BUKRS, ZAFGBOOK,ZUONR, KUNAG,ZAF_UDATE,ZAFSHIP_DATE ,BUDAT,ZAFEXPIRY_DATE,MANDT, WAERS ,CREDITVOUCHER_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED)SELECT SUB_SACRVC.*, CONVERT(VARCHAR(4000),NEWID()),''"+ str(User.UserName)+ "'',GETDATE() FROM (SELECT DISTINCT SPART,ZAF_UTIME,HKONT, ZAFPLATFORM,  ZAFTOOL_ID, ZAFWAFER,  CONVERT(VARCHAR,GJAHR) AS GJAHR , ZAFKPU, ZAFTYPE, ZAFSP, ZAFTECHNO, CONVERT(VARCHAR,BUZEI) AS BUZEI , CONVERT(VARCHAR,WRBTR) AS WRBTR , BELNR, BUKRS, ZAFGBOOK, ZUONR, KUNAG, convert(date,ZAF_UDATE) as ZAF_UDATE,convert(date,ZAFSHIP_DATE) as ZAFSHIP_DATE,convert(date,BUDAT) as BUDAT,convert(date,ZAFEXPIRY_DATE) as ZAFEXPIRY_DATE,MANDT, CONVERT(VARCHAR,WAERS) AS WAERS FROM SACRVC_INBOUND(NOLOCK) )SUB_SACRVC LEFT JOIN SACRVC(NOLOCK)  ON SUB_SACRVC.SPART = SACRVC.SPART WHERE SACRVC.SPART IS NULL '"	)
		
		primaryQueryItems = SqlHelper.GetFirst(
			""
			+ str(Parameter1.QUERY_CRITERIA_1)
			+ " SACRVC SET CREDIT_APPLIED = CREDIT_APPLIED_INVC_CURR FROM SACRVC (NOLOCK) JOIN (SELECT CREDITVOUCHER_RECORD_ID,SUM(CREDIT_APPLIED_INVC_CURR) AS CREDIT_APPLIED_INVC_CURR FROM SAQRCV (NOLOCK) GROUP BY CREDITVOUCHER_RECORD_ID)SAQRCV ON SACRVC.CREDITVOUCHER_RECORD_ID = SAQRCV.CREDITVOUCHER_RECORD_ID '"	)
		
		primaryQueryItems = SqlHelper.GetFirst(
			""
			+ str(Parameter1.QUERY_CRITERIA_1)
			+ " SACRVC SET UNAPPLIED_BALANCE = ISNULL(WRBTR,0) - ISNULL(CREDIT_APPLIED,0) FROM SACRVC (NOLOCK)  '"	)
			
		#SACVNT Insert Query		
		
		primaryQueryItems = SqlHelper.GetFirst(
			""
			+ str(Parameter.QUERY_CRITERIA_1)
			+ " SACVNT (HKONT, ZAF_UDATE, MANDT, ZAF_UTIME, ZAFNOTE, ZUONR, GJAHR, BUZEI, ZAFNOTE_ID, BELNR, BUKRS ,CRDVCH_NOTE_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED)SELECT SUB_SACVNT.*,CONVERT(VARCHAR(4000),NEWID()),''"+ str(User.UserName)+ "'',GETDATE() FROM (SELECT DISTINCT HKONT, ZAF_UDATE, MANDT, ZAF_UTIME, ZAFNOTE, ZUONR, GJAHR, BUZEI, ZAFNOTE_ID, BELNR, BUKRS FROM SACVNT_INBOUND(NOLOCK))SUB_SACVNT LEFT JOIN SACVNT(NOLOCK)  ON SUB_SACVNT.BUKRS = SACVNT.BUKRS WHERE SACVNT.BUKRS IS NULL '"	)
		
		
		
		Tbl = 'SACRVC_INBOUND'
		TempTable = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(Tbl)+"'' ) BEGIN DROP TABLE "+str(Tbl)+" END'")

		Tbl = 'SACVNT_INBOUND'
		TempTable = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(Tbl)+"'' ) BEGIN DROP TABLE "+str(Tbl)+" END'")

		ApiResponse = ApiResponseFactory.JsonResponse(
			{
				"Response": [
					{
						"Status": "200",
						"Message": "Data Successfully Uploaded ."
					}
				]
			}
		)

except:     
	Log.Info("SAGETCVHUP ERROR---->:" + str(sys.exc_info()[1]))
	Log.Info("SAGETCVHUP ERROR LINE NO---->:" + str(sys.exc_info()[-1].tb_lineno))
	ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "400", "Message": str(sys.exc_info()[1])}]})
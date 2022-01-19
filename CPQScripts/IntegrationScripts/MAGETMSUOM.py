# =========================================================================================================================================
#   __script_name : MAGETMSUOM.PY
#   __script_description : THIS SCRIPT IS USED TO CONNECTING HANA DB AND FETCHING DATA OF MAMUOC.
#   __primary_author__ : BAJI
#   __create_date :01/06/2022
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

		#MAMSAC

		Table_Name = 'MAMUOC_INBOUND'

		TempTable = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(Table_Name)+"'' ) BEGIN DROP TABLE "+str(Table_Name)+" END CREATE TABLE "+str(Table_Name)+" (BASE_QUANTITY VARCHAR(250) ,BASEUOM_ID VARCHAR(250) ,CONVERSION_QUANTITY VARCHAR(250) ,CONVERSIONUOM_ID VARCHAR(250) ,SAP_PART_NUMBER VARCHAR(250),BASEUOM_RECORD_ID VARCHAR(250),CONVERSIONUOM_RECORD_ID VARCHAR(250),MATERIAL_NAME VARCHAR(250),MATERIAL_RECORD_ID VARCHAR(250) )'")	

		start =1
		end = 10000
		check_flag1 = 1
		while check_flag1 == 1:	
		

			req_input = '{"query":"select * from (select  MATNR as SAP_PART_NUMBER,MEINH as CONVERSIONUOM_ID,UMREZ as BASE_QUANTITY,UMREN AS CONVERSION_QUANTITY,row_number () over (order by MEINH) as sno from MARM )a where sno>='+str(start)+' and sno<='+str(end)+'"}'

			response2 = webclient.UploadString(str(LOGIN_CREDENTIALS.URL), str(req_input))

			response = eval(response2)
			if str(type(response)) == "<type 'dict'>":
				response = [response]

			if len(response) > 0:			

				for record_dict in response:
					

					Stagingquery = SqlHelper.GetFirst( ""+ str(Parameter.QUERY_CRITERIA_1)+ " "+str(Table_Name)+" (SAP_PART_NUMBER,CONVERSIONUOM_ID,BASE_QUANTITY,CONVERSION_QUANTITY)  select  N''"+record_dict['SAP_PART_NUMBER']+ "'',N''"+record_dict['CONVERSIONUOM_ID']+ "'',N''"+record_dict['BASE_QUANTITY']+ "'',N''"+record_dict['CONVERSION_QUANTITY']+ "'' ' ")

				start = start + 10000
				end = end + 10000

			else:
				check_flag1 = 0
		
		
		
		MaterialupdateQuery = SqlHelper.GetFirst(""+ str(Parameter1.QUERY_CRITERIA_1)+ "  MAMUOC_INBOUND set MAMUOC_INBOUND.SAP_PART_NUMBER= CONVERT(INT,SAP_PART_NUMBER)  FROM MAMUOC_INBOUND (NOLOCK) WHERE ISNUMERIC(SAP_PART_NUMBER)=1  ' ")
		
		MaterialupdateQuery = SqlHelper.GetFirst(""+ str(Parameter1.QUERY_CRITERIA_1)+ "  MAMUOC_INBOUND set MAMUOC_INBOUND.MATERIAL_NAME= MAMTRL.SAP_DESCRIPTION,MAMUOC_INBOUND.MATERIAL_RECORD_ID= MAMTRL.MATERIAL_RECORD_ID,BASEUOM_RECORD_ID=UOM_RECORD_ID,BASEUOM_ID = UOM_ID FROM MAMUOC_INBOUND(NOLOCK)  JOIN MAMTRL(NOLOCK) ON MAMUOC_INBOUND.SAP_PART_NUMBER= MAMTRL.SAP_PART_NUMBER  ' ")
		
		UomupdateQuery = SqlHelper.GetFirst(""+ str(Parameter1.QUERY_CRITERIA_1)+ "  MAMUOC_INBOUND set MAMUOC_INBOUND.CONVERSIONUOM_RECORD_ID= Y.UNIT_OF_MEASURE_RECORD_ID FROM MAMUOC_INBOUND(NOLOCK) JOIN MAMUOM(NOLOCK) Y ON  MAMUOC_INBOUND.CONVERSIONUOM_ID	= Y.UOM ' ")
		
		#MAMUOC Update
		primaryQueryItems = SqlHelper.GetFirst(
			""
			+ str(Parameter.QUERY_CRITERIA_1)
			+ " MAMUOC BASE_QUANTITY = SUB_MAMUOC.BASE_QUANTITY,CONVERSION_QUANTITY = SUB_MAMUOC.CONVERSION_QUANTITY FROM MAMUOC JOIN (SELECT DISTINCT BASEUOM_ID,BASE_QUANTITY,BASEUOM_RECORD_ID,CONVERSIONUOM_ID,CONVERSION_QUANTITY,CONVERSIONUOM_RECORD_ID,SAP_PART_NUMBER,MATERIAL_NAME,MATERIAL_RECORD_ID FROM MAMUOC_INBOUND(NOLOCK) )SUB_MAMUOC ON SUB_MAMUOC.BASEUOM_ID = MAMUOC.BASEUOM_ID AND SUB_MAMUOC.SAP_PART_NUMBER = MAMUOC.SAP_PART_NUMBER AND SUB_MAMUOC.CONVERSIONUOM_ID = MAMUOC.CONVERSIONUOM_ID '"	)
		
		#MAMUOC Insert  
		primaryQueryItems = SqlHelper.GetFirst(
			""
			+ str(Parameter.QUERY_CRITERIA_1)
			+ " MAMUOC (BASEUOM_ID,BASE_QUANTITY,BASEUOM_RECORD_ID,CONVERSIONUOM_ID,CONVERSION_QUANTITY,CONVERSIONUOM_RECORD_ID,SAP_PART_NUMBER,MATERIAL_NAME,MATERIAL_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED)SELECT SUB_MAMUOC.*,''"+ str(User.UserName)+ "'',GETDATE() FROM (SELECT DISTINCT BASEUOM_ID,BASE_QUANTITY,BASEUOM_RECORD_ID,CONVERSIONUOM_ID,CONVERSION_QUANTITY,CONVERSIONUOM_RECORD_ID,SAP_PART_NUMBER,MATERIAL_NAME,MATERIAL_RECORD_ID FROM MAMUOC_INBOUND(NOLOCK) )SUB_MAMUOC LEFT JOIN MAMUOC(NOLOCK)  ON SUB_MAMUOC.BASEUOM_ID = MAMUOC.BASEUOM_ID AND SUB_MAMUOC.SAP_PART_NUMBER = MAMUOC.SAP_PART_NUMBER AND SUB_MAMUOC.CONVERSIONUOM_ID = MAMUOC.CONVERSIONUOM_ID  WHERE MAMUOC.BASEUOM_ID IS NULL '"	)
		
		Tbl = 'MAMUOC_INBOUND'
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
	Log.Info("MAGETMSUOM ERROR---->:" + str(sys.exc_info()[1]))
	Log.Info("MAGETMSUOM ERROR LINE NO---->:" + str(sys.exc_info()[-1].tb_lineno))
	ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "400", "Message": str(sys.exc_info()[1])}]})
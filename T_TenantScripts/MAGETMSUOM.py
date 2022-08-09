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
		
		Table_Name1 = 'MATERIAL_INBOUND'

		TempTable1 = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(Table_Name1)+"'' ) BEGIN DROP TABLE "+str(Table_Name1)+" END CREATE TABLE "+str(Table_Name1)+" (MATERIAL_RECORD_ID VARCHAR(250) )'")	
		
		TempTable2 = SqlHelper.GetFirst("sp_executesql @T=N'INSERT MATERIAL_INBOUND (MATERIAL_RECORD_ID)select DISTINCT A.SAP_PART_NUMBER  from MAMTRL(NOLOCK) A WHERE CONVERT(VARCHAR(11),CPQTABLEENTRYDATEMODIFIED,121)>= CONVERT(VARCHAR(11),GETDATE(),121)  '")	

		start =1
		end = 1
		check_flag1 = 1
		while check_flag1 == 1:
			
			Partquery=SqlHelper.GetFirst("SELECT SAP_PART_NUMBER FROM (SELECT SAP_PART_NUMBER,ROW_NUMBER()OVER(ORDER BY SAP_PART_NUMBER) AS SNO FROM ( select DISTINCT A.MATERIAL_RECORD_ID AS SAP_PART_NUMBER  from MATERIAL_INBOUND(NOLOCK) A )A)a where sno>='"+str(start)+"' and sno<='"+str(end)+"'  ")


			if str(Partquery).upper() != "NONE":
				
				start = start + 1
				end = end + 1

				part = "'"+str(Partquery.SAP_PART_NUMBER)+"'"
		

				req_input = '{"query":"select  MATNR as SAP_PART_NUMBER,MEINH as CONVERSIONUOM_ID,UMREZ as BASE_QUANTITY,UMREN AS CONVERSION_QUANTITY from MARM  where MATNR='+str(part)+'"}'

				response2 = webclient.UploadString(str(LOGIN_CREDENTIALS.URL), str(req_input))

				response = eval(response2)
				if str(type(response)) == "<type 'dict'>":
					response = [response]

				for record_dict in response:
					
					Stagingquery = SqlHelper.GetFirst( ""+ str(Parameter.QUERY_CRITERIA_1)+ " "+str(Table_Name)+" (SAP_PART_NUMBER,CONVERSIONUOM_ID,BASE_QUANTITY,CONVERSION_QUANTITY)  select  N''"+record_dict['SAP_PART_NUMBER']+ "'',N''"+record_dict['CONVERSIONUOM_ID']+ "'',N''"+record_dict['BASE_QUANTITY']+ "'',N''"+record_dict['CONVERSION_QUANTITY']+ "'' ' ")

			else:
				check_flag1 = 0		
		
		MaterialupdateQuery = SqlHelper.GetFirst(""+ str(Parameter1.QUERY_CRITERIA_1)+ "  MAMUOC_INBOUND set MAMUOC_INBOUND.SAP_PART_NUMBER= CONVERT(BIGINT,SAP_PART_NUMBER)  FROM MAMUOC_INBOUND (NOLOCK) WHERE ISNUMERIC(SAP_PART_NUMBER)=1 AND SAP_PART_NUMBER NOT LIKE ''%.%'' AND SAP_PART_NUMBER NOT LIKE ''%D%'' AND SAP_PART_NUMBER NOT LIKE ''%E%''  ' ")
		
		MaterialupdateQuery = SqlHelper.GetFirst(""+ str(Parameter1.QUERY_CRITERIA_1)+ "  MAMUOC_INBOUND set MAMUOC_INBOUND.MATERIAL_NAME= MAMTRL.SAP_DESCRIPTION,MAMUOC_INBOUND.MATERIAL_RECORD_ID= MAMTRL.MATERIAL_RECORD_ID,BASEUOM_RECORD_ID=UOM_RECORD_ID,BASEUOM_ID = UNIT_OF_MEASURE FROM MAMUOC_INBOUND(NOLOCK)  JOIN MAMTRL(NOLOCK) ON MAMUOC_INBOUND.SAP_PART_NUMBER= MAMTRL.SAP_PART_NUMBER  ' ")
		
		UomupdateQuery = SqlHelper.GetFirst(""+ str(Parameter1.QUERY_CRITERIA_1)+ "  MAMUOC_INBOUND set MAMUOC_INBOUND.CONVERSIONUOM_RECORD_ID= Y.UNIT_OF_MEASURE_RECORD_ID FROM MAMUOC_INBOUND(NOLOCK) JOIN MAMUOM(NOLOCK) Y ON  MAMUOC_INBOUND.CONVERSIONUOM_ID	= Y.UOM ' ")
		
		#MAMUOC Update
		primaryQueryItems = SqlHelper.GetFirst(
			""
			+ str(Parameter1.QUERY_CRITERIA_1)
			+ " MAMUOC SET BASE_QUANTITY = SUB_MAMUOC.BASE_QUANTITY,CONVERSION_QUANTITY = SUB_MAMUOC.CONVERSION_QUANTITY FROM MAMUOC JOIN (SELECT DISTINCT BASEUOM_ID,BASE_QUANTITY,BASEUOM_RECORD_ID,CONVERSIONUOM_ID,CONVERSION_QUANTITY,CONVERSIONUOM_RECORD_ID,SAP_PART_NUMBER,MATERIAL_NAME,MATERIAL_RECORD_ID FROM MAMUOC_INBOUND(NOLOCK) )SUB_MAMUOC ON SUB_MAMUOC.BASEUOM_ID = MAMUOC.BASEUOM_ID AND SUB_MAMUOC.SAP_PART_NUMBER = MAMUOC.SAP_PART_NUMBER AND SUB_MAMUOC.CONVERSIONUOM_ID = MAMUOC.CONVERSIONUOM_ID '"	)
		
		#MAMUOC Insert  
		primaryQueryItems = SqlHelper.GetFirst(
			""
			+ str(Parameter.QUERY_CRITERIA_1)
			+ " MAMUOC (BASEUOM_ID,BASE_QUANTITY,BASEUOM_RECORD_ID,CONVERSIONUOM_ID,CONVERSION_QUANTITY,CONVERSIONUOM_RECORD_ID,SAP_PART_NUMBER,MATERIAL_NAME,MATERIAL_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED)SELECT SUB_MAMUOC.*,''"+ str(User.UserName)+ "'',GETDATE() FROM (SELECT DISTINCT BASEUOM_ID,BASE_QUANTITY,BASEUOM_RECORD_ID,CONVERSIONUOM_ID,CONVERSION_QUANTITY,CONVERSIONUOM_RECORD_ID,SAP_PART_NUMBER,MATERIAL_NAME,MATERIAL_RECORD_ID FROM MAMUOC_INBOUND(NOLOCK) )SUB_MAMUOC LEFT JOIN MAMUOC(NOLOCK)  ON SUB_MAMUOC.BASEUOM_ID = MAMUOC.BASEUOM_ID AND SUB_MAMUOC.SAP_PART_NUMBER = MAMUOC.SAP_PART_NUMBER AND SUB_MAMUOC.CONVERSIONUOM_ID = MAMUOC.CONVERSIONUOM_ID  WHERE MAMUOC.BASEUOM_ID IS NULL '"	)
		
		Tbl = 'MAMUOC_INBOUND'
		TempTable = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(Tbl)+"'' ) BEGIN DROP TABLE "+str(Tbl)+" END'")
		
		Tbl1 = 'MATERIAL_INBOUND_INBOUND'
		TempTable1 = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(Tbl1)+"'' ) BEGIN DROP TABLE "+str(Tbl1)+" END'")

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
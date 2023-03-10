# =========================================================================================================================================
#   __script_name : MAGETCUSPT.PY
#   __script_description : THIS SCRIPT IS USED TO CONNECTING HANA DB AND FETCHING DATA OF MAMSAC.
#   __primary_author__ : BAJI
#   __create_date :12/17/2021
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================

try:
	import clr
	import System.Net
	from System.Text.Encoding import UTF8
	from System import Convert
	import sys
	import time
	
	Parameter = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'SELECT' ")
	Parameter1 = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'UPD' ")
	Parameter2 = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'DEL' ")

	LOGIN_CREDENTIALS = SqlHelper.GetFirst("SELECT URL FROM SYCONF where EXTERNAL_TABLE_NAME='HANA_CONNECTION'")
	
	OAUTH_CREDENTIALS = SqlHelper.GetFirst("SELECT DOMAIN,URL FROM SYCONF where EXTERNAL_TABLE_NAME='HANA_OAUTH'")
	
	if LOGIN_CREDENTIALS is not None:
		
		try:
			oauthURL = str(OAUTH_CREDENTIALS.URL)
			requestdata = str(OAUTH_CREDENTIALS.DOMAIN)
			webclient = System.Net.WebClient()
			webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/x-www-form-urlencoded"
			response = webclient.UploadString(str(oauthURL),str(requestdata))
			response = eval(response)     
		except:
			Log.Info("except exicuted--->")
			time.sleep(5)
			oauthURL = str(OAUTH_CREDENTIALS.URL)
			requestdata = str(OAUTH_CREDENTIALS.DOMAIN)
			webclient = System.Net.WebClient()
			webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/x-www-form-urlencoded"
			response = webclient.UploadString(str(oauthURL),str(requestdata))
			response = eval(response)
		
		
		webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/json"
		webclient.Headers[System.Net.HttpRequestHeader.Authorization] ="Bearer "+str(response['access_token'])

		#MAMSAC

		Table_Name = 'MAMSAC_INBOUND'

		TempTable = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(Table_Name)+"'' ) BEGIN DROP TABLE "+str(Table_Name)+" END CREATE TABLE "+str(Table_Name)+" (ACCOUNT_ID VARCHAR(250) ,CUSTOMER_PART_DESC VARCHAR(250) ,CUSTOMER_PART_NUMBER VARCHAR(250) ,DISTRIBUTIONCHANNEL_ID VARCHAR(250) ,SALESORG_ID VARCHAR(250) ,SAP_PART_NUMBER VARCHAR(250) ,ACCOUNT_NAME VARCHAR(250),ACCOUNT_RECORD_ID VARCHAR(250),DISTRIBUTIONCHANNEL_RECORD_ID VARCHAR(250),MATERIAL_NAME VARCHAR(250),MATERIAL_RECORD_ID VARCHAR(250),MATSOR_RECORD_ID VARCHAR(250),SORACC_RECORD_ID VARCHAR(250),SALESORG_NAME VARCHAR(250),SALESORG_RECORD_ID VARCHAR(250))'")	

		start =1
		end = 1
		check_flag1 = 1
		while check_flag1 == 1:

			Partquery=SqlHelper.GetFirst("SELECT SAP_PART_NUMBER FROM (SELECT SAP_PART_NUMBER,ROW_NUMBER()OVER(ORDER BY SAP_PART_NUMBER) AS SNO FROM ( select DISTINCT A.SAP_PART_NUMBER  from MAMTRL(NOLOCK) A WHERE CONVERT(VARCHAR(11),CPQTABLEENTRYDATEMODIFIED,121)= CONVERT(VARCHAR(11),GETDATE(),121) )A)a where sno>='"+str(start)+"' and sno<='"+str(end)+"'  ")

			if str(Partquery).upper() != "NONE":
			
				start = start + 1
				end = end + 1

				part = "'"+str(Partquery.SAP_PART_NUMBER)+"'"

				req_input = '{"query":"select  KUNNR as ACCOUNT_ID,POSTX as CUSTOMER_PART_DESC,KDMAT as CUSTOMER_PART_NUMBER,VTWEG as DISTRIBUTIONCHANNEL_ID,VKORG as SALESORG_ID,MATNR as SAP_PART_NUMBER from KNMT where MATNR='+str(part)+'"}' 

				response2 = webclient.UploadString(str(LOGIN_CREDENTIALS.URL), str(req_input))

				response = eval(response2)
				if str(type(response)) == "<type 'dict'>":
					response = [response]

				if len(response) > 0:			

					for record_dict in response:

						if 'CUSTOMER_PART_DESC' in record_dict:
							record_dict['CUSTOMER_PART_DESC'] = record_dict['CUSTOMER_PART_DESC'].replace("'",'&#39;').replace('"','&#34;')
						if 'CUSTOMER_PART_NUMBER' in record_dict:
							record_dict['CUSTOMER_PART_NUMBER'] = record_dict['CUSTOMER_PART_NUMBER'].replace("'",'&#39;').replace('"','&#34;')

						Stagingquery = SqlHelper.GetFirst( ""+ str(Parameter.QUERY_CRITERIA_1)+ " "+str(Table_Name)+" (ACCOUNT_ID,CUSTOMER_PART_DESC,CUSTOMER_PART_NUMBER ,DISTRIBUTIONCHANNEL_ID,SALESORG_ID,SAP_PART_NUMBER)  select  N''"+record_dict['ACCOUNT_ID']+ "'',N''"+record_dict['CUSTOMER_PART_DESC']+ "'',N''"+record_dict['CUSTOMER_PART_NUMBER']+ "'',N''"+record_dict['DISTRIBUTIONCHANNEL_ID']+ "'',N''"+record_dict['SALESORG_ID']+ "'',N''"+record_dict['SAP_PART_NUMBER']+ "'' ' ")

			else:
				check_flag1 = 0

		
		S = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE MAMSAC_INBOUND set ACCOUNT_ID = convert(bigint,ACCOUNT_ID)  where isnumeric(ACCOUNT_ID)=1  ' ")
		
		S = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE MAMSAC_INBOUND set SAP_PART_NUMBER = convert(bigint,SAP_PART_NUMBER)  where isnumeric(SAP_PART_NUMBER)=1  ' ")
		
		AccountupdateQuery = SqlHelper.GetFirst(""+ str(Parameter1.QUERY_CRITERIA_1)+ "  MAMSAC_INBOUND set MAMSAC_INBOUND.ACCOUNT_NAME= SAACNT.ACCOUNT_NAME,MAMSAC_INBOUND.ACCOUNT_RECORD_ID= SAACNT.ACCOUNT_RECORD_ID FROM MAMSAC_INBOUND(NOLOCK)  JOIN SAACNT(NOLOCK) ON MAMSAC_INBOUND.ACCOUNT_ID= SAACNT.ACCOUNT_ID  ' ")
		
		MaterialupdateQuery = SqlHelper.GetFirst(""+ str(Parameter1.QUERY_CRITERIA_1)+ "  MAMSAC_INBOUND set MAMSAC_INBOUND.MATERIAL_NAME= MAMTRL.SAP_DESCRIPTION,MAMSAC_INBOUND.MATERIAL_RECORD_ID= MAMTRL.MATERIAL_RECORD_ID FROM MAMSAC_INBOUND(NOLOCK)  JOIN MAMTRL(NOLOCK) ON MAMSAC_INBOUND.SAP_PART_NUMBER= MAMTRL.SAP_PART_NUMBER  ' ")
		
		AccountupdateQuery = SqlHelper.GetFirst(""+ str(Parameter1.QUERY_CRITERIA_1)+ "  MAMSAC_INBOUND set MAMSAC_INBOUND.SALESORG_NAME= SASORG.SALESORG_NAME,MAMSAC_INBOUND.SALESORG_RECORD_ID= SASORG.SALES_ORG_RECORD_ID,MAMSAC_INBOUND.DISTRIBUTIONCHANNEL_RECORD_ID = SADSCH.DISTRIBUTION_CHANNEL_RECORD_ID,MAMSAC_INBOUND.SORACC_RECORD_ID = SASOAC.SALESORG_ACCOUNTS_RECORD_ID FROM MAMSAC_INBOUND(NOLOCK) JOIN SASORG(NOLOCK) ON MAMSAC_INBOUND.SALESORG_ID= SASORG.SALESORG_ID LEFT JOIN SADSCH(NOLOCK) ON  MAMSAC_INBOUND.DISTRIBUTIONCHANNEL_ID	= SADSCH.DISTRIBUTIONCHANNEL_ID LEFT JOIN SASOAC(NOLOCK) ON MAMSAC_INBOUND.ACCOUNT_ID = SASOAC.ACCOUNT_ID AND MAMSAC_INBOUND.SALESORG_ID = SASOAC.SALESORG_ID' ")
		
		AccountupdateQuery = SqlHelper.GetFirst(""+ str(Parameter2.QUERY_CRITERIA_1)+ "  FROM MAMSAC_INBOUND WHERE ISNULL(ACCOUNT_RECORD_ID,'''')='''' OR ISNULL(MATERIAL_RECORD_ID,'''')='''' OR ISNULL(SALESORG_RECORD_ID,'''')='''' OR ISNULL(DISTRIBUTIONCHANNEL_RECORD_ID,'''')='''' ' ")
		
		#MAMSAC Update
		primaryQueryItems = SqlHelper.GetFirst(
			""
			+ str(Parameter1.QUERY_CRITERIA_1)
			+ " MAMSAC SET CUSTOMER_PART_NUMBER = SUB_MAMSAC.CUSTOMER_PART_NUMBER, CUSTOMER_PART_DESC = SUB_MAMSAC.CUSTOMER_PART_DESC  FROM MAMSAC JOIN (SELECT DISTINCT ACCOUNT_ID,ACCOUNT_NAME,ACCOUNT_RECORD_ID,CUSTOMER_PART_DESC,CUSTOMER_PART_NUMBER,DISTRIBUTIONCHANNEL_ID,DISTRIBUTIONCHANNEL_RECORD_ID,MATERIAL_NAME,MATERIAL_RECORD_ID,MATSOR_RECORD_ID,SORACC_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,SAP_PART_NUMBER FROM MAMSAC_INBOUND(NOLOCK) )SUB_MAMSAC ON SUB_MAMSAC.ACCOUNT_ID = MAMSAC.ACCOUNT_ID AND SUB_MAMSAC.SAP_PART_NUMBER = MAMSAC.SAP_PART_NUMBER AND SUB_MAMSAC.SALESORG_ID = MAMSAC.SALESORG_ID '"	)	
			
		#MAMSAC Insert  
		primaryQueryItems = SqlHelper.GetFirst(
			""
			+ str(Parameter.QUERY_CRITERIA_1)
			+ " MAMSAC (ACCOUNT_ID,ACCOUNT_NAME,ACCOUNT_RECORD_ID,CUSTOMER_PART_DESC,CUSTOMER_PART_NUMBER,DISTRIBUTIONCHANNEL_ID,DISTRIBUTIONCHANNEL_RECORD_ID,MATERIAL_NAME,MATERIAL_RECORD_ID,MATSOR_RECORD_ID,SORACC_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,SAP_PART_NUMBER ,MATERIAL_SALES_ORG_ACCOUNT_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED)SELECT SUB_MAMSAC.*, CONVERT(VARCHAR(4000),NEWID()),''"+ str(User.UserName)+ "'',GETDATE() FROM (SELECT DISTINCT ACCOUNT_ID,ACCOUNT_NAME,ACCOUNT_RECORD_ID,CUSTOMER_PART_DESC,CUSTOMER_PART_NUMBER,DISTRIBUTIONCHANNEL_ID,DISTRIBUTIONCHANNEL_RECORD_ID,MATERIAL_NAME,MATERIAL_RECORD_ID,MATSOR_RECORD_ID,SORACC_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,SAP_PART_NUMBER FROM MAMSAC_INBOUND(NOLOCK) )SUB_MAMSAC LEFT JOIN MAMSAC(NOLOCK)  ON SUB_MAMSAC.ACCOUNT_ID = MAMSAC.ACCOUNT_ID AND SUB_MAMSAC.SAP_PART_NUMBER = MAMSAC.SAP_PART_NUMBER AND SUB_MAMSAC.SALESORG_ID = MAMSAC.SALESORG_ID WHERE MAMSAC.ACCOUNT_ID IS NULL '"	)	
		
		Tbl = 'MAMSAC_INBOUND'
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
	Log.Info("MAGETCUSPT ERROR---->:" + str(sys.exc_info()[1]))
	Log.Info("MAGETCUSPT ERROR LINE NO---->:" + str(sys.exc_info()[-1].tb_lineno))
	ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "400", "Message": str(sys.exc_info()[1])}]})
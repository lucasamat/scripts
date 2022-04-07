# =========================================================================================================================================
#   __script_name : PRGETPRBMK.PY
#   __script_description : THIS SCRIPT IS USED TO CONNECTING HANA DB ,FETCHING PRICEBENCHMARK DATA AND STORED IN PRPRBM.
#   __primary_author__ : BAJI
#   __create_date :02/03/2021
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
		
		staging_tableInfo = SqlHelper.GetTable("PRPRBM_INBOUND")
		PRPRBM_tableInfoData = SqlHelper.GetTable("PRPRBM")

		#PRPRBM
		start =1
		end = 500
		check_flag = 1
		start_flag = 1
		while check_flag == 1:

			req_input = '{"query":"select * from (select  *,row_number () over (order by GEN_ROW_NUM) as sno from cds_pl_pricebenchmark_vw  )a where sno>='+str(start)+' and sno<='+str(end)+'"}'

			response2 = webclient.UploadString(str(LOGIN_CREDENTIALS.URL), str(req_input)) 

			response = eval(response2)
			if str(type(response)) == "<type 'dict'>":
				response = [response]

			if len(response) > 0:			

				for record_dict in response:						
							
					del record_dict['SNO']
					staging_tableInfo.AddRow(record_dict)
				sqlInfo = SqlHelper.Upsert(staging_tableInfo)					

				start = start + 500
				end = end + 500

			else:
				check_flag = 0	
		
		start1 = 1
		end1 = 1000
		
		while start_flag == 1:			

			benchmarkquery = SqlHelper.GetList("select CONVERT(VARCHAR(4000),NEWID()) as BENCHMARK_RECORD_ID,* from (SELECT a.*,row_number () over (order by a.GEN_ROW_NUM) as sno,b.cpqtableentryid as updateid FROM PRPRBM_INBOUND a left join prprbm b(nolock) on a.GEN_ROW_NUM = b.GEN_ROW_NUM and b.GEN_ROW_NUM IS NULL )a where sno>='"+str(start1)+"' and sno<='"+str(end1)+"'  ")				

			if len(benchmarkquery) > 0:

				for data in benchmarkquery:
					dt = {}
					dt["EQUIPMENT_NUMBER"]= data.EQUIPMENT_NUMBER
					dt["FNCNLLOC"]= data.FNCNLLOC
					dt["CONTRACT_END_FISCAL_MONTH"]= data.CONTRACT_END_FISCAL_MONTH
					dt["SIMILARTOOL"]= data.SIMILARTOOL
					dt["PROCESSPARTSKITSCLEANRECY"]= data.PROCESSPARTSKITSCLEANRECY
					dt["TOTALNEWORDERS"]= data.TOTALNEWORDERS
					dt["PROCESSAPPENGINEERING"]= data.PROCESSAPPENGINEERING
					dt["SERVICE_PRODUCT_NAME"]= data.SERVICE_PRODUCT_NAME
					dt["CONTRACT_END_FISCAL_QUARTER"]= data.CONTRACT_END_FISCAL_QUARTER
					dt["CONTRACT_END_DATE"]= data.CONTRACT_END_DATE
					dt["TECHFORCE"]= data.TECHFORCE
					dt["WETCLEANSLABOR"]= data.WETCLEANSLABOR
					dt["CONTRACT_BOOKING_FISCAL_QURT"]= data.CONTRACT_BOOKING_FISCAL_QURT
					dt["FABVANTAGE"]= data.FABVANTAGE
					dt["CONTRACT_BOOKING_DATE"]= data.CONTRACT_BOOKING_DATE
					dt["ANNUALIZED_BOOKING_PRICE"]= data.ANNUALIZED_BOOKING_PRICE
					dt["CONTRACT_END_FISCAL_YEAR"]= data.CONTRACT_END_FISCAL_YEAR
					dt["TOTAL_COST"]= data.TOTAL_COST
					dt["SALES_DOCUMENT_ITEM"]= data.SALES_DOCUMENT_ITEM
					dt["FNCNLLOCDESC"]= data.FNCNLLOCDESC
					dt["CMLABOR"]= data.CMLABOR
					dt["GLOBALMAXCNTRENDDATE"]= data.GLOBALMAXCNTRENDDATE
					dt["CONSUMABLE"]= data.CONSUMABLE
					dt["TOTALSTDCOSPARTS"]= data.TOTALSTDCOSPARTS
					dt["CUSTMAXANNUAL_BKNG_PRICE"]= data.CUSTMAXANNUAL_BKNG_PRICE
					dt["CUSTMAXCNTRENDDATE"]= data.CUSTMAXCNTRENDDATE
					dt["TOTALGROSSREVENUE"]= data.TOTALGROSSREVENUE
					dt["CONTRACT_CONTRACTCOVERAGE"]= data.CONTRACT_CONTRACTCOVERAGE
					dt["ONCALLOUTSIDECONTRCOVERAGE"]= data.ONCALLOUTSIDECONTRCOVERAGE
					dt["CONTRACT"]= data.CONTRACT
					dt["RENEWALFLAG"]= data.RENEWALFLAG
					dt["PLATFORM"]= data.PLATFORM
					dt["GLBLMAXANNUAL_BKNG_PRICE"]= data.GLBLMAXANNUAL_BKNG_PRICE
					dt["TOOLCONFG"]= data.TOOLCONFG
					dt["RESPONSETIME"]= data.RESPONSETIME
					dt["TOTALGROSSMARGINDLR"]= data.TOTALGROSSMARGINDLR
					dt["TOTALSTDCOST"]= data.TOTALSTDCOST
					dt["STDCOSPARTS"]= data.STDCOSPARTS
					dt["DIFF_MONTHS"]= data.DIFF_MONTHS
					dt["NODE"]= data.NODE
					dt["GEN_ROW_NUM"]= data.GEN_ROW_NUM
					dt["BLUEBOOK"]= data.BLUEBOOK
					dt["CUSTMINANNUAL_BKNG_PRICE"]= data.CUSTMINANNUAL_BKNG_PRICE
					dt["WAFERSIZE"]= data.WAFERSIZE
					dt["SRVCTECHVITA"]= data.SRVCTECHVITA
					dt["GLOBALMAXFAB"]= data.GLOBALMAXFAB
					dt["BOOKING_PER_TOOL"]= data.BOOKING_PER_TOOL
					dt["TOTALNETBOOKINGS"]= data.TOTALNETBOOKINGS
					dt["SWAPKITSAMATPROVIDED"]= data.SWAPKITSAMATPROVIDED
					dt["STDGROSSMARGINDLR"]= data.STDGROSSMARGINDLR
					dt["CNTRDESC"]= data.CNTRDESC
					dt["BLACKBOOK"]= data.BLACKBOOK
					dt["CONTRACT_BOOKING_FISCAL_YEAR"]= data.CONTRACT_BOOKING_FISCAL_YEAR
					dt["DAYSCOUNT"]= data.DAYSCOUNT
					dt["CONTRACT_START_FISCAL_MONTH"]= data.CONTRACT_START_FISCAL_MONTH
					dt["SRVCTECHPDCSERVER"]= data.SRVCTECHPDCSERVER
					dt["CONTRACT_START_FISCAL_YEAR"]= data.CONTRACT_START_FISCAL_YEAR
					dt["PMLABOR"]= data.PMLABOR
					dt["CONTRACT_START_FISCAL_QUARTER"]= data.CONTRACT_START_FISCAL_QUARTER
					dt["CUSTMAXFAB"]= data.CUSTMAXFAB
					dt["CUSTMINFAB"]= data.CUSTMINFAB
					dt["CUSTMINCNTRENDDATE"]= data.CUSTMINCNTRENDDATE
					dt["TOTALSTDCOSLABOR"]= data.TOTALSTDCOSLABOR
					dt["STDCOSLABOR"]= data.STDCOSLABOR
					dt["GLOBALMAXCUSTSHRTNAME"]= data.GLOBALMAXCUSTSHRTNAME
					dt["CUSTSHRTNAMEMKTG"]= data.CUSTSHRTNAMEMKTG
					dt["GLOBALMINCUSTSHRTNAME"]= data.GLOBALMINCUSTSHRTNAME
					dt["SERVICE_PRODUCT_DESC"]= data.SERVICE_PRODUCT_DESC
					dt["CUSTNAME"]= data.CUSTNAME
					dt["RFPCONTRACTMATCH"]= data.RFPCONTRACTMATCH
					dt["GLOBALMINFAB"]= data.GLOBALMINFAB
					dt["GREENBOOK"]= data.GREENBOOK
					dt["CONTRACT_START_DATE"]= data.CONTRACT_START_DATE
					dt["RFPNUM"]= data.RFPNUM
					dt["NONCONSUMABLE"]= data.NONCONSUMABLE
					dt["SERIAL_NUMBER"]= data.SERIAL_NUMBER
					dt["STD_COS_PO_ITEM"]= data.STD_COS_PO_ITEM
					dt["RFPSYSID"]= data.RFPSYSID
					dt["GLOBALMINCNTRENDDATE"]= data.GLOBALMINCNTRENDDATE
					dt["TOTALNETREVENUE"]= data.TOTALNETREVENUE
					dt["GLBLMINANNUAL_BKNG_PRICE"]= data.GLBLMINANNUAL_BKNG_PRICE
					dt["cpqtableentryid"]= data.updateid
					dt["PRICE_BENCHMARK_RECORD_ID"] = data.BENCHMARK_RECORD_ID

					PRPRBM_tableInfoData.AddRow(dt)
				sqlInfo = SqlHelper.Upsert(PRPRBM_tableInfoData)
				
			else:
				start_flag = 0
							
		

		ApiResponse = ApiResponseFactory.JsonResponse(
			{
				"Response": [
					{
						"Status": "200",
						"Message": "Pricebenchmark Data Successfully Uploaded ."
					}
				]
			}
		)
				
except:     
	Log.Info("PRGETPRBMK ERROR---->:" + str(sys.exc_info()[1]))
	Log.Info("PRGETPRBMK ERROR LINE NO---->:" + str(sys.exc_info()[-1].tb_lineno))
	ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "400", "Message": str(sys.exc_info()[1])}]})
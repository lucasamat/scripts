# =========================================================================================================================================
#   __script_name : SYGETINTLG.PY
#   __script_description : THIS SCRIPT IS USED TO STORE RESPONSE BACK IN CPQ SYELOG TABLE FROM OTHER SYSTEMS
#   __primary_author__ : BAJI BABA
#   __create_date :
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import sys
import datetime

try:
    if "Param" in globals():
        Lst_resp = []
        Resp_msg = {}
        Sucess = ""
        Error = ""
        if hasattr(Param, "CPQ_Columns"):
            rebuilt_data = {}
            sessionid = SqlHelper.GetFirst("SELECT NEWID() AS A")
            for table_dict in Param.CPQ_Columns:
                tbl = str(table_dict.Key)
                colu_Info = {}
                uu = []
                for record_dict in table_dict.Value:
                    tyty = str(type(record_dict))
                    if str(tyty) == "<type 'KeyValuePair[str, object]'>":
                        j = record_dict
                        j_Valu = j.Value

                        if "&#34;" in j_Valu:
                            j_Valu = j_Valu.replace("&#34;", '"')
                        if "&#39;" in j_Valu:
                            j_Valu = j_Valu.replace("&#39;", "'")
                        if "&#92;" in j_Valu:
                            j_Valu = j_Valu.replace("&#92;", "\\")

                        colu_Info[str(j.Key)] = j_Valu
                    else:
                        colu_Info1 = {}
                        for j in record_dict:
                            j_Valu = j.Value

                            j_key = str(j.Key)

                            if "&#34;" in j_Valu:
                                j_Valu = j_Valu.replace("&#34;", '"')
                            if "&#39;" in j_Valu:
                                j_Valu = j_Valu.replace("&#39;", "'")
                            if "&#92;" in j_Valu:
                                j_Valu = j_Valu.replace("&#92;", "\\")

                            colu_Info1[str(j.Key)] = j_Valu                        

                        else:
                            uu.append(colu_Info1)
                if len(colu_Info) != 0:
                    rebuilt_data[tbl] = [colu_Info]

                if len(uu) != 0:
                    rebuilt_data[tbl] = uu

            if len(rebuilt_data) != 0:
                today = datetime.datetime.now()
                Modi_date = today.strftime("%m/%d/%Y %H:%M:%S %p")
				Parameter = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'SELECT' ")
				primaryQueryItems = SqlHelper.GetFirst( ""+ str(Parameter.QUERY_CRITERIA_1)+ " SYELOG (ERRORMESSAGE_DESCRIPTION,ERROR_LOGS_RECORD_ID,CPQTABLEENTRYDATEADDED)  select ''"+str(rebuilt_data)+ "'',CONVERT(VARCHAR(4000),NEWID()),''"+ str(Modi_date)+ "'' ' ")
				
				ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "200", "Message": "Data successfully updated"}]})
            else:
				ApiResponse = ApiResponseFactory.JsonResponse(
					{"Response": [{"Status": "200", "Message": "NO DATA AVAILABLE FOR SYNCHRONIZATION"}]}
				)    
				

        else:
            if "ApiResponseFactory" in globals():
                ApiResponse = ApiResponseFactory.JsonResponse(
                    {
                        "Response": [
                            {
                                "Status": "400",
                                "Message": "Invalid format.Param not available",
                            }
                        ]
                    }
                )
except:
    Log.Info("SYGETINTLG ERROR---->:" + str(sys.exc_info()[1]))
    Log.Info("SYGETINTLG ERROR LINE NO---->:" + str(sys.exc_info()[-1].tb_lineno))
    ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "400", "Message": str(sys.exc_info()[1])}]})

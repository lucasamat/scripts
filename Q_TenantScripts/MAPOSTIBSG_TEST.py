# =========================================================================================================================================
#   __script_name : MAPOSTIBSG.PY
#   __script_description : THIS SCRIPT IS USED TO INSERT EQUIPMENT AND FAB DATA FROM SYINPL TO STAGING TABLES.
#   __primary_author__ : BAJI
#   __create_date : 2021-06-16
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import sys
import datetime

cpqentry_id = ''

try :
	While_flag = 1
	Trigger_flag = 0
	while While_flag == 1:
		Jsonquery = SqlHelper.GetList("SELECT integration_payload as INTEGRATION_PAYLOAD,CpqTableEntryId from SYINPL_bkp_installedbase(NOLOCK) WHERE INTEGRATION_NAME = 'INSTALLED BASE' AND ISNULL(STATUS,'')='' ")
		if len(Jsonquery) > 0:

			for json_data in Jsonquery:
				cpqentry_id = str(json_data.CpqTableEntryId)
				splited_list = str(json_data.INTEGRATION_PAYLOAD)
				rebuilt_data = eval(str(splited_list))
				
				primaryQuerysession =  SqlHelper.GetFirst("SELECT NEWID() AS Guid")
				today = datetime.datetime.now()
				Modi_date = today.strftime("%m/%d/%Y %H:%M:%S %p")
				

				if len(rebuilt_data) != 0:      

					rebuilt_data = rebuilt_data["CPQ_Columns"]
					Table_Names = rebuilt_data.keys()
					
					format_error = []
					
					for tn in Table_Names:
						if tn in rebuilt_data:
							Trigger_flag  = 1
							
							MAEQUP_tableInfoData = SqlHelper.GetTable("MAEQUP_INBOUND")
							MAFBLC_tableInfoData = SqlHelper.GetTable("MAFBLC_INBOUND")
							
							
							if str(tn).upper() == "MAEQUP":
								if str(type(rebuilt_data[tn])) == "<type 'dict'>":
									Tbl_data = [rebuilt_data[tn]]
								else:
									Tbl_data = rebuilt_data[tn]
									
								for record_dict in Tbl_data:
									
									record_dict["SESSION_ID"] = primaryQuerysession.Guid
									record_dict["cpqtableentrydatemodified"] = Modi_date
									MAEQUP_tableInfoData.AddRow(record_dict)
															   
									
							elif str(tn).upper() == "MAFBLC":
								if str(type(rebuilt_data[tn])) == "<type 'dict'>":
									Tbl_data = [rebuilt_data[tn]]
								else:
									Tbl_data = rebuilt_data[tn]
									
								for record_dict in Tbl_data:
									
									if "STATUS" not in record_dict:
										record_dict['STATUS'] = ""
									
									record_dict["SESSION_ID"] = primaryQuerysession.Guid
									record_dict["cpqtableentrydatemodified"] = Modi_date
									if str(record_dict['STATUS']).upper()  == 'CRTE':
										record_dict['STATUS'] = 1
									else:
										record_dict['STATUS'] = 0
									MAFBLC_tableInfoData.AddRow(record_dict)							
							

							if str(tn).upper() == "MAEQUP":
								sqlInfo = SqlHelper.Upsert(MAEQUP_tableInfoData)
								if str(sqlInfo.Message) != "None":
									eff_tab = "Affected table : " + str(tn) + " : " + str(sqlInfo.Message)
									format_error.append(eff_tab)

							elif str(tn).upper() == "MAFBLC":
								sqlInfo = SqlHelper.Upsert(MAFBLC_tableInfoData)
								if str(sqlInfo.Message) != "None":
									eff_tab = "Affected table : " + str(tn) + " : " + str(sqlInfo.Message)
									format_error.append(eff_tab)
									
							
					Parameter1 = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'UPD' ")			
					primaryItems = SqlHelper.GetFirst(  ""+ str(Parameter1.QUERY_CRITERIA_1)+ "  SYINPL_bkp_installedbase set STATUS = ''PROCESSED'' from SYINPL_bkp_installedbase  (NOLOCK) WHERE CpqTableEntryId  = ''"+str(json_data.CpqTableEntryId)+ "'' AND ISNULL(STATUS ,'''')= '''' ' "    )
					if len(format_error) > 0:
						ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "400", "Message": str(format_error)}]})

		
		else:
			While_flag = 0
	
	"""if Trigger_flag == 1:
		#resp = ScriptExecutor.ExecuteGlobal("MAPOSTEQBK")              
		ApiResponse = ApiResponseFactory.JsonResponse(resp)		
	else:
		ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "200", "Message": "NO DATA AVAILABLE FOR SYNCHRONIZATION"}]}) """
except:
	Parameter1 = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'UPD' ")			
	primaryItems = SqlHelper.GetFirst(  ""+ str(Parameter1.QUERY_CRITERIA_1)+ "  SYINPL_bkp_installedbase set STATUS = ''ERROR'' from SYINPL_bkp_installedbase  (NOLOCK) WHERE CpqTableEntryId  = ''"+str(cpqentry_id)+ "'' AND ISNULL(STATUS ,'''')= '''' ' "    )
	#result = ScriptExecutor.ExecuteGlobal("MAPOSTIBSG")	
	Log.Info("MAPOSTIBSG ERROR---->:" + str(sys.exc_info()[1]))
	Log.Info("MAPOSTIBSG ERROR LINE NO---->:" + str(sys.exc_info()[-1].tb_lineno))
	ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "400", "Message": str(sys.exc_info()[1])}]})
# =========================================================================================================================================
#   __script_name : QTPOSTCPQUP.PY
#   __script_description : THIS SCRIPT IS USED TO UPDATE STATU IN SAQICO AND CALL SSCM PRICING
#   __primary_author__ : BAJI
#   __create_date :
#   Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import clr
import System.Net
from System.Text.Encoding import UTF8
from System import Convert
import sys

#input_data = [str(param_result.Value) for param_result in Param.CPQ_Columns]
#input_data = [input_data]#[['CPQQUOTEONHOLDTEST01', '100']]

try:
	if 'Param' in globals(): 	
		if hasattr(Param, 'CPQ_Columns'): 
			rebuilt_data = ''
			tbl_name = ''
			for table_dict in Param.CPQ_Columns: 				
				tbl = str(table_dict.Key)
				tbl_name = tbl				
				Single_Record = {}				
				Multiple_Record  = []				
				for record_dict in table_dict.Value:
					tyty = str(type(record_dict))
					if str(tyty) == "<type 'KeyValuePair[str, object]'>":
						Single_Record[str(record_dict.Key)] = (record_dict.Value).replace('"','\\"')
						
						
					elif str(tyty) == "<type 'Dictionary[str, object]'>":
						colu_Info1 = {}
						for j in record_dict:												
							colu_Info1[str(j.Key)] = (j.Value).replace('"','\\"')         
						Multiple_Record.append(colu_Info1)	
						
							
						
				if len(Single_Record) !=  0: 
					tbl = '"'+tbl+'"'
					rebuilt_data = rebuilt_data+(str(tbl)+":"+str(Single_Record))+','
						
				if len(Multiple_Record) !=  0: 
					tbl = '"'+tbl+'"'
					rebuilt_data = rebuilt_data+(str(tbl)+':'+str(Multiple_Record))+','		

			Parameter = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'SELECT' ")
			sessionid = SqlHelper.GetFirst("SELECT NEWID() AS A")
			timestamp_sessionid = "'" + str(sessionid.A) + "'"

			syinpl_data = "{"+str(rebuilt_data)[:-1].replace("'",'"')+"}"

			#Log.Info("4444 syinpl_data --->"+str(syinpl_data))
			#Log.Info("55555 syinpl_data --->"+str(""+ str(Parameter.QUERY_CRITERIA_1)+ " SYINPL (INTEGRATION_PAYLOAD,SESSION_ID,INTEGRATION_NAME)  select ''"+str(syinpl_data)+ "'','"+ str(timestamp_sessionid)+ "',''UPDATECPQ'' ' "))



			primaryQueryItems = SqlHelper.GetFirst( ""+ str(Parameter.QUERY_CRITERIA_1)+ " SYINPL (INTEGRATION_PAYLOAD,SESSION_ID,INTEGRATION_NAME)  select ''"+str(syinpl_data)+ "'','"+ str(timestamp_sessionid)+ "',''UPDATECPQ'' ' ")		
				
					
			rebuilt_data = eval('{'+str(rebuilt_data)[:-1]+'}')
			#Log.Info("4545 rebuilt_data--->"+str(rebuilt_data))
			#Log.Info("4545 type--->"+str(type(rebuilt_data)))
			input_data = rebuilt_data['QTQICO']

			for crmifno in input_data:	
				#Log.Info("4545 type--->"+str(crmifno))
				QUOTE_ID = crmifno['QUOTE_ID']
				EQUIPMENT_ID = crmifno['EQUIPMENT_ID']	
						
				UpdateTable1=SqlHelper.GetFirst("sp_executesql @T=N'update SAQICO set STATUS =  '''' FROM SAQICO (NOLOCK) JOIN SAQRIO (NOLOCK) ON SAQICO.QUOTE_ID = SAQRIO.QUOTE_ID AND SAQICO.QTEREV_ID = SAQRIO.QTEREV_ID where SAQICO.QUOTE_ID+''-''+ CONVERT(VARCHAR,SAQICO.QTEREV_ID)=''"+ str(QUOTE_ID)+ "'' and SAQRIO.EQUIPMENT_ID = ''"+ str(EQUIPMENT_ID)+ "'' '")
				
				UpdateTable1=SqlHelper.GetFirst("sp_executesql @T=N'update SAQRIT set STATUS =  '''' FROM SAQRIT (NOLOCK) JOIN SAQRIO (NOLOCK) ON SAQRIT.QUOTE_ID = SAQRIO.QUOTE_ID AND SAQRIT.QTEREV_ID = SAQRIO.QTEREV_ID where SAQRIT.QUOTE_ID+''-''+ CONVERT(VARCHAR,SAQRIT.QTEREV_ID)=''"+ str(QUOTE_ID)+ "'' and SAQRIO.EQUIPMENT_ID = ''"+ str(EQUIPMENT_ID)+ "'' '")
                
				UpdateTable1=SqlHelper.GetFirst("sp_executesql @T=N'update SAQTRV set REVISION_STATUS =  ''CFG-ACQUIRING'',WORKFLOW_STATUS=''ACQUIRING'' FROM SAQTRV (NOLOCK) where SAQTRV.QUOTE_ID+''-''+ CONVERT(VARCHAR,SAQTRV.QTEREV_ID)=''"+ str(QUOTE_ID)+ "'' '")

				
				sqlqueryinfo = SqlHelper.GetList("SELECT QTEREV_ID,QUOTE_ID FROM SAQICO(NOLOCK) WHERE QUOTE_ID+'-'+ CONVERT(VARCHAR,QTEREV_ID)='"+ str(QUOTE_ID)+ "' ")

				if len(sqlqueryinfo) > 0:
				
					for data in sqlqueryinfo:
					
						Callingsscmpricing = ScriptExecutor.ExecuteGlobal("QTPOSTACRM",{"QUOTE_ID":data.QUOTE_ID,"REVISION_ID":data.QTEREV_ID,'Fun_type':'CPQ_TO_SSCM'})

					ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "200", "Message": "SSCM CALL HITTED SUCCESSULLY"}]})
				else:
					ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "200", "Message": "NO DATA AVAILABLE FOR SYNCHRONIZATION"}]})

except:
	Log.Info("QTPOSTCPQUP ERROR---->:" + str(sys.exc_info()[1]))
	Log.Info("QTPOSTCPQUP ERROR LINE NO---->:" + str(sys.exc_info()[-1].tb_lineno))
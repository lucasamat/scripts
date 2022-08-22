# =========================================================================================================================================
#   __script_name : PRPOSTLSOR.PY
#   __script_description : THIS SCRIPT IS USED TO INSERT LABOUR SALESORG DATA IN SYINPL
#   __primary_author__ : BAJI
#   __create_date :29-07-2021
#   Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import sys
import datetime 
import sys
import clr
import System.Net
import System
from System.Text.Encoding import UTF8
from System import Convert

try:
    if 'Param' in globals():    
        if hasattr(Param, 'CPQ_Columns'): 
            rebuilt_data = ''
            quote_id = ''
            tbl_name = ''
            primaryQueryItems = SqlHelper.GetFirst("SELECT NEWID() AS A")
            for table_dict in Param.CPQ_Columns:                
                tbl = str(table_dict.Key)
                tbl_name = tbl              
                Single_Record = {}
                Multiple_Record  = []    
                Dirct_record = {}
                for record_dict in table_dict.Value:
                    tyty = str(type(record_dict))
                    if str(tyty) == "<type 'KeyValuePair[str, object]'>":    
                        
                        Single_Record[str(record_dict.Key)] = (record_dict.Value).replace('"','\\"')
                    elif str(tyty) == "<type 'Dictionary[str, object]'>":
                        colu_Info1 = {}
                        for j in record_dict:                               
                                                
                            colu_Info1[str(j.Key)] = (j.Value).replace('"','\\"')         
                        Multiple_Record.append(colu_Info1)  
                    else:
                        Dirct_record[tbl] = str(table_dict.Value)                  
                            
                
                if len(Dirct_record) > 0:
                    for ins in Dirct_record:
                        rebuilt_data = rebuilt_data+'"'+(str(ins)+'"'+":"+'"'+str(Dirct_record[ins]))+'"'+','
                            
                        
                if len(Single_Record) !=  0: 
                    tbl = '"'+tbl+'"'
                    rebuilt_data = rebuilt_data+(str(tbl)+":"+str(Single_Record))+','
                        
                if len(Multiple_Record) !=  0: 
                    tbl = '"'+tbl+'"'
                    rebuilt_data = rebuilt_data+(str(tbl)+':'+str(Multiple_Record))+','
                    
            rebuilt_data = str(rebuilt_data)[:-1]
            #Log.Info("66666 Final_data --->"+str(rebuilt_data))
            Final_data = "{ \"CPQ_Columns\": {" + str(rebuilt_data).replace("'",'"') +"}}"

            sessionid = SqlHelper.GetFirst("SELECT NEWID() AS A")
            timestamp_sessionid = "'" + str(sessionid.A) + "'"
            addby = User.UserName           
            #Log.Info("66666 Final_data --->"+str(Final_data))
            Parameter = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'SELECT' ")         
            
            primaryQueryItems = SqlHelper.GetFirst( ""+ str(Parameter.QUERY_CRITERIA_1)+ " SYINPL (INTEGRATION_PAYLOAD,INTEGRATION_NAME,SESSION_ID,CPQTABLEENTRYDATEADDED,CPQTABLEENTRYADDEDBY)  select ''"+str(Final_data)+ "'',''Labor Activity'','"+ str(timestamp_sessionid)+ "',Getdate(),''"+str(addby)+ "'' ' ")

            

            ApiResponse = ApiResponseFactory.JsonResponse(
                {
                    "Response": [
                        {
                            "Status": "200",
                            "Message": "Data Sucessfully Uploaded."
                        }
                    ]
                }
            )

except:     
    Log.Info("PRPOSTLSOR ERROR---->:" + str(sys.exc_info()[1]))
    Log.Info("PRPOSTLSOR ERROR LINE NO---->:" + str(sys.exc_info()[-1].tb_lineno))
    ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "400", "Message": str(sys.exc_info()[1])}]})
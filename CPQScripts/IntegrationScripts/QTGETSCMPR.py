# =========================================================================================================================================
#   __script_name : QTGETSCMPR.PY
#   __script_description : THIS SCRIPT IS USED TO INSERT SSCM PRICING DATA IN SYINPL TABLES
#   __primary_author__ : BAJI
#   __create_date :
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import sys
import datetime 
import clr
import System.Net
from System.Text.Encoding import UTF8
from System import Convert
from System.Net import HttpWebRequest, NetworkCredential
from System.Net import *
clr.AddReference("System.Net")
from System.Net import CookieContainer, NetworkCredential, Mail
from System.Net.Mail import SmtpClient, MailAddress, Attachment, MailMessage

Log.Info("QTGETSCMPR Starts ---->Hitting")

try:
    if 'Param' in globals():    
        if hasattr(Param, 'CPQ_Columns'): 
            rebuilt_data = ''
            quote_id = ''
            Sesion_id = ''
            primaryQueryItems = SqlHelper.GetFirst("SELECT NEWID() AS A")       
            for table_dict in Param.CPQ_Columns: 
                tbl = str(table_dict.Key)
                #Log.Info("6666 tbl---->"+str(tbl))
                
                Single_Record = {}
                Multiple_Record  = []    
                Dirct_record = {}
                for record_dict in table_dict.Value:
                    #Log.Info("99999 record_dict ---->"+str(table_dict.Value))
                    tyty = str(type(record_dict))
                    if str(tyty) == "<type 'KeyValuePair[str, object]'>": 
                    
                        Single_Record[str(record_dict.Key)] = record_dict.Value
                        if str(record_dict.Key).upper() == "SESSION_ID":
                            Sesion_id = record_dict.Value
                        if str(record_dict.Key).upper() == "QUOTE_ID":
                            quote_id = record_dict.Value
                        
                        
                    elif str(tyty) == "<type 'Dictionary[str, object]'>":
                        colu_Info1 = {}
                        for j in record_dict:                               
                                                
                            colu_Info1[str(j.Key)] = j.Value
                            if str(j.Key).upper() == "SESSION_ID":
                                Sesion_id = j.Value
                            if str(j.Key).upper() == "QUOTE_ID":
                                quote_id = j.Value

                            
                        Multiple_Record.append(colu_Info1)  
                    else:
                        Dirct_record[tbl] = str(table_dict.Value)
                        if str(tbl).upper() == "QUOTE_ID":
                            quote_id = str(table_dict.Value)
                        if str(tbl).upper() == "SESSION_ID":
                            Sesion_id = str(table_dict.Value)
                            
                
                if len(Dirct_record) > 0:
                    for ins in Dirct_record:
                        rebuilt_data = rebuilt_data+'"'+(str(ins)+'"'+":"+'"'+str(Dirct_record[ins]))+'"'+','
                            
                        
                if len(Single_Record) !=  0: 
                    tbl = '"'+tbl+'"'
                    rebuilt_data = rebuilt_data+(str(tbl)+":"+str(Single_Record))+','
                    #rebuilt_data.append(sig_dict)
                        
                if len(Multiple_Record) !=  0: 
                    tbl = '"'+tbl+'"'
                    rebuilt_data = rebuilt_data+(str(tbl)+':'+str(Multiple_Record))+','
                    #rebuilt_data.append(mul_dict)
                    
            #Log.Info("959595---->"+str(rebuilt_data))
            rebuilt_data = str(rebuilt_data)[:-1]
            Final_data = "{ \"Param\" :''''{ \"CPQ_Columns\": {" + str(rebuilt_data).replace("'",'"') +"}}  ''''}"
            sessionid = SqlHelper.GetFirst("SELECT NEWID() AS A")
            timestamp_sessionid = "'" + str(sessionid.A) + "'"

            Parameter = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'SELECT' ")
            Parameter2 = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'DEL' ")

            LOGIN_CRE = SqlHelper.GetFirst("SELECT URL FROM SYCONF (nolock) where EXTERNAL_TABLE_NAME ='SSCM_DATA_GETMETHOD'")
            PSMA_CRE = SqlHelper.GetFirst("SELECT URL FROM SYCONF (nolock) where EXTERNAL_TABLE_NAME ='SSCM_DATA_GETMETHOD_PMSA'")
            TKM_CRE = SqlHelper.GetFirst("SELECT URL FROM SYCONF (nolock) where EXTERNAL_TABLE_NAME ='SSCM_DATA_GETMETHOD_TKM'")
            
            primaryQueryItems = SqlHelper.GetFirst( ""+ str(Parameter.QUERY_CRITERIA_1)+ " SYINPL (INTEGRATION_PAYLOAD,SESSION_ID,INTEGRATION_NAME,INTEGRATION_KEY,CpqTableEntryDateModified)  select ''"+str(Final_data)+ "'','"+ str(timestamp_sessionid)+ "',''SSCM_TO_CPQ_PRICING_DATA1'',''"+str(quote_id)+ "'',GETDATE() ' ")

            Log.Info("QTGETSCMPR Ends---->Hitting2")
            
            #SSCM_DATA_GETMETHOD call
            webRequest = str(LOGIN_CRE.URL).format(Sesion_id = Sesion_id,quote_id =quote_id )
            def GetNewRequest(targetUrl, Btoken):

                newRequest = HttpWebRequest.Create(targetUrl)
                newRequest.AllowAutoRedirect = 0
                newRequest.Headers.Add("AUTHORIZATION", Btoken)
                newRequest.Headers.Add("Environment-Identifier", 'X')
                newRequest.Method = 'GET'
                newRequest.ContentLength = 0
                newRequest.ContentType = 'application/json'
                #Log.Info("6666 ---->"+str(newRequest.Headers))

                return newRequest

            Oauth_info = SqlHelper.GetFirst("SELECT  DOMAIN,URL FROM SYCONF where EXTERNAL_TABLE_NAME ='OAUTH'")

            requestdata =Oauth_info.DOMAIN
            webclient = System.Net.WebClient()
            webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/x-www-form-urlencoded"
            response = webclient.UploadString(Oauth_info.URL,str(requestdata))

            response = eval(response)
            access_token = response['access_token']
            Btoken = "Bearer " + access_token

            rew = GetNewRequest(webRequest, Btoken)
            resp = rew.GetResponse()                                        

            streamReader = StreamReader(resp.GetResponseStream())
            jsonData = streamReader.ReadToEnd()
            conv_data = jsonData.replace("'",'%%')
            
            primaryQueryItems = SqlHelper.GetFirst( ""+ str(Parameter.QUERY_CRITERIA_1)+ " SYINPL (INTEGRATION_PAYLOAD,SESSION_ID,INTEGRATION_NAME,INTEGRATION_KEY,CpqTableEntryDateModified)  select ''"+str(conv_data)+ "'','"+ str(timestamp_sessionid)+ "',''SSCM_TO_CPQ_PRICING_DATA'',''"+str(quote_id)+ "'',GETDATE() ' ")
            
            primaryQueryItems = SqlHelper.GetFirst( ""+ str(Parameter2.QUERY_CRITERIA_1)+ " FROM SYINPL WHERE SESSION_ID = '"+ str(timestamp_sessionid)+ "' AND INTEGRATION_PAYLOAD LIKE ''%FLEX%'' AND INTEGRATION_NAME = ''SSCM_TO_CPQ_PRICING_DATA'' AND INTEGRATION_KEY =  ''"+str(quote_id)+ "'' ' ")
            
            primaryQueryItems = SqlHelper.GetFirst( ""+ str(Parameter2.QUERY_CRITERIA_1)+ " FROM SYINPL WHERE SESSION_ID = '"+ str(timestamp_sessionid)+ "' AND INTEGRATION_PAYLOAD LIKE ''%TKMKIT%'' AND INTEGRATION_NAME = ''SSCM_TO_CPQ_PRICING_DATA'' AND INTEGRATION_KEY =  ''"+str(quote_id)+ "'' ' ")
            
            #SSCM_DATA_GETMETHOD_PMSA call
            psma_webRequest = str(PSMA_CRE.URL).format(Sesion_id = Sesion_id,quote_id =quote_id )
            def GetNewRequest(targetUrl, Btoken):

                newRequest = HttpWebRequest.Create(targetUrl)
                newRequest.AllowAutoRedirect = 0
                newRequest.Headers.Add("AUTHORIZATION", Btoken)
                newRequest.Headers.Add("Environment-Identifier", 'X')
                newRequest.Method = 'GET'
                newRequest.ContentLength = 0
                newRequest.ContentType = 'application/json'

                return newRequest

            Oauth_info = SqlHelper.GetFirst("SELECT  DOMAIN,URL FROM SYCONF where EXTERNAL_TABLE_NAME ='OAUTH'")

            requestdata =Oauth_info.DOMAIN
            webclient = System.Net.WebClient()
            webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/x-www-form-urlencoded"
            response = webclient.UploadString(Oauth_info.URL,str(requestdata))

            response = eval(response)
            access_token = response['access_token']
            Btoken = "Bearer " + access_token

            rew = GetNewRequest(psma_webRequest, Btoken)
            resp = rew.GetResponse()                                        

            streamReader = StreamReader(resp.GetResponseStream())
            jsonData = streamReader.ReadToEnd()
            PSMA_conv_data = jsonData.replace("'",'%%')
            
            primaryQueryItems = SqlHelper.GetFirst( ""+ str(Parameter.QUERY_CRITERIA_1)+ " SYINPL (INTEGRATION_PAYLOAD,SESSION_ID,INTEGRATION_NAME,INTEGRATION_KEY,CpqTableEntryDateModified)  select REPLACE(''"+str(PSMA_conv_data)+ "'',''CM_LABOR_COST'',''LABOR_COST''),'"+ str(timestamp_sessionid)+ "',''SSCM_TO_CPQ_PRICING_DATA_FLEX'',''"+str(quote_id)+ "'',GETDATE() ' ")
            
            primaryQueryItems = SqlHelper.GetFirst( ""+ str(Parameter2.QUERY_CRITERIA_1)+ " FROM SYINPL WHERE SESSION_ID = '"+ str(timestamp_sessionid)+ "' AND INTEGRATION_PAYLOAD NOT LIKE ''%FLEX%'' AND INTEGRATION_NAME=''SSCM_TO_CPQ_PRICING_DATA_FLEX'' ' ")
            
            primaryQueryItems = SqlHelper.GetFirst( "sp_executesql @T=N' UPDATE SYINPL SET INTEGRATION_NAME =''SSCM_TO_CPQ_PRICING_DATA'' WHERE SESSION_ID = '"+ str(timestamp_sessionid)+ "' AND INTEGRATION_PAYLOAD LIKE ''%FLEX%'' AND INTEGRATION_NAME=''SSCM_TO_CPQ_PRICING_DATA_FLEX'' ' ")
            
            #SSCM_DATA_GETMETHOD_PMSA call
            tkm_webRequest = str(TKM_CRE.URL).format(Sesion_id = Sesion_id,quote_id =quote_id )
            def GetNewRequest(targetUrl, Btoken):

                newRequest = HttpWebRequest.Create(targetUrl)
                newRequest.AllowAutoRedirect = 0
                newRequest.Headers.Add("AUTHORIZATION", Btoken)
                newRequest.Headers.Add("Environment-Identifier", 'X')
                newRequest.Method = 'GET'
                newRequest.ContentLength = 0
                newRequest.ContentType = 'application/json'

                return newRequest

            Oauth_info = SqlHelper.GetFirst("SELECT  DOMAIN,URL FROM SYCONF where EXTERNAL_TABLE_NAME ='OAUTH'")

            requestdata =Oauth_info.DOMAIN
            webclient = System.Net.WebClient()
            webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/x-www-form-urlencoded"
            response = webclient.UploadString(Oauth_info.URL,str(requestdata))

            response = eval(response)
            access_token = response['access_token']
            Btoken = "Bearer " + access_token

            rew = GetNewRequest(tkm_webRequest, Btoken)
            resp = rew.GetResponse()                                        

            streamReader = StreamReader(resp.GetResponseStream())
            jsonData = streamReader.ReadToEnd()
            PSMA_conv_data = jsonData.replace("'",'%%')
            
            primaryQueryItems = SqlHelper.GetFirst( ""+ str(Parameter.QUERY_CRITERIA_1)+ " SYINPL (INTEGRATION_PAYLOAD,SESSION_ID,INTEGRATION_NAME,INTEGRATION_KEY,CpqTableEntryDateModified)  select REPLACE(''"+str(PSMA_conv_data)+ "'',''CM_LABOR_COST'',''LABOR_COST''),'"+ str(timestamp_sessionid)+ "',''SSCM_TO_CPQ_PRICING_DATA_TKM'',''"+str(quote_id)+ "'',GETDATE() ' ")
            
            primaryQueryItems = SqlHelper.GetFirst( ""+ str(Parameter2.QUERY_CRITERIA_1)+ " FROM SYINPL WHERE SESSION_ID = '"+ str(timestamp_sessionid)+ "' AND INTEGRATION_PAYLOAD NOT LIKE ''%TKMKIT%'' AND INTEGRATION_NAME=''SSCM_TO_CPQ_PRICING_DATA_TKM'' ' ")

            primaryQueryItems = SqlHelper.GetFirst( "sp_executesql @T=N' UPDATE SYINPL SET INTEGRATION_NAME =''SSCM_TO_CPQ_PRICING_DATA'' WHERE SESSION_ID = '"+ str(timestamp_sessionid)+ "' AND INTEGRATION_PAYLOAD LIKE ''%TKMKIT%'' AND INTEGRATION_NAME=''SSCM_TO_CPQ_PRICING_DATA_TKM'' ' ")
            
            
            #Async call

            LOGIN_CREDENTIALS = SqlHelper.GetFirst("SELECT USER_NAME as Username,Password,Domain FROM SYCONF where Domain='AMAT_TST'")
            if LOGIN_CREDENTIALS is not None:
                Login_Username = str(LOGIN_CREDENTIALS.Username)
                Login_Password = str(LOGIN_CREDENTIALS.Password)
                authorization = Login_Username+":"+Login_Password
                binaryAuthorization = UTF8.GetBytes(authorization)
                authorization = Convert.ToBase64String(binaryAuthorization)
                authorization = "Basic " + authorization


                webclient = System.Net.WebClient()
                webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/json"
                webclient.Headers[System.Net.HttpRequestHeader.Authorization] = authorization;
                
                result = '<?xml version="1.0" encoding="UTF-8"?><soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"><soapenv:Body ></soapenv:Body></soapenv:Envelope>'
                
                LOGIN_CRE = SqlHelper.GetFirst("SELECT URL FROM SYCONF where EXTERNAL_TABLE_NAME ='CPQ_TO_SSCM_PRICING_ASYNC'")
                Async = webclient.UploadString(str(LOGIN_CRE.URL), str(result))
            
            
            
            rsp_msg = {
                            "Status": "200",
                            "Message": "Data Sucessfully Uploaded ."
                        }
            rsp_msg['SESSION_ID'] = Sesion_id
            
            ApiResponse = ApiResponseFactory.JsonResponse(
                {
                    "Response": [rsp_msg
                        
                    ]
                }
            )
    
except:     
    Log.Info("QTGETSCMPR ERROR---->:" + str(sys.exc_info()[1]))
    Log.Info("QTGETSCMPR ERROR LINE NO---->:" + str(sys.exc_info()[-1].tb_lineno))
    ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "400", "Message": str(sys.exc_info()[1])}]})
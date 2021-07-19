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
            
            primaryQueryItems = SqlHelper.GetFirst( ""+ str(Parameter.QUERY_CRITERIA_1)+ " SYINPL (INTEGRATION_PAYLOAD,SESSION_ID,INTEGRATION_NAME,INTEGRATION_KEY,CpqTableEntryDateModified)  select ''"+str(Final_data)+ "'','"+ str(timestamp_sessionid)+ "',''SSCM_TO_CPQ_PRICING_DATA'',''"+str(quote_id)+ "'',GETDATE() ' ")

            Log.Info("QTGETSCMPR Ends---->Hitting2")
            
            """
            Header = "<!DOCTYPE html><html><head><style>table {font-family: Calibri, sans-serif; border-collapse: collapse; width: 75%}td, th {  border: 1px solid #dddddd;  text-align: left; padding: 8px;}.im {color: #222;}tr:nth-child(even) {background-color: #dddddd;}</style></head><body>"

            Table_start = "<p>Hi Team,<br>SSCM Pricing data successfully stored in SYINPL.</p><br>"
            
            Table_End = "</table><p><strong>Note : </strong>Please do not reply to this email.</p></body></html>"
            Table_info = ""     

            Error_Info = Header + Table_start + Table_info + Table_End

            LOGIN_CRE = SqlHelper.GetFirst("SELECT USER_NAME as Username,Password FROM SYCONF where Domain ='SUPPORT_MAIL'")

            # Create new SmtpClient object
            mailClient = SmtpClient()

            # Set the host and port (eg. smtp.gmail.com)
            mailClient.Host = "smtp.gmail.com"
            mailClient.Port = 587
            mailClient.EnableSsl = "true"

            # Setup NetworkCredential
            mailCred = NetworkCredential()
            mailCred.UserName = str(LOGIN_CRE.Username)
            mailCred.Password = str(LOGIN_CRE.Password)
            mailClient.Credentials = mailCred

            # Create two mail adresses, one for send from and the another for recipient
            toEmail = MailAddress("suresh.muniyandi@bostonharborconsulting.com")
            fromEmail = MailAddress("INTEGRATION.SUPPORT@BOSTONHARBORCONSULTING.COM")

            # Create new MailMessage object
            msg = MailMessage(fromEmail, toEmail)

            # Set message subject and body
            msg.Subject = "SSCM to CPQ - Pricing Status Notification"
            msg.IsBodyHtml = True
            msg.Body = Error_Info

            # CC Emails 
            copyEmail5 = MailAddress("aditya.shivkumar@bostonharborconsulting.com")
            msg.CC.Add(copyEmail5)
            
            copyEmail4 = MailAddress("baji.baba@bostonharborconsulting.com")
            msg.CC.Add(copyEmail4)
            
            # Send the message
            mailClient.Send(msg)        
            """
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
import sys
import datetime
import clr
import System.Net
from System.Text.Encoding import UTF8
from System import Convert
from SYDATABASE import SQL
import CQVLDRIFLW
import CQCPQC4CWB

clr.AddReference("System.Net")
from System.Net import CookieContainer, NetworkCredential, Mail
from System.Net.Mail import SmtpClient, MailAddress, Attachment, MailMessage

Parameter = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'SELECT' ")
Parameter1 = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'UPD' ")
Parameter2 = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'DEL' ")

SYINPL_SESSION = SqlHelper.GetFirst("SELECT NEWID() AS A")

exceptinfo = ''
Glb_Quote_Id = ''

try:

    Stausquery = SqlHelper.GetFirst("SELECT count(*) as cnt from SYINPL(NOLOCK) WHERE INTEGRATION_NAME = 'SSCM_TO_CPQ_PRICING_DATA' AND ISNULL(STATUS,'') = 'INPROGRESS111' ")  
    
    if Stausquery.cnt == 0:

        #Status Inprogress SYINPL by CPQ Table Entry ID
        
        StatusUpdateQuery = SqlHelper.GetFirst(""+ str(Parameter1.QUERY_CRITERIA_1)+ "  SYINPL SET STATUS = ''ERROR'',SESSION_ID=''"+str(SYINPL_SESSION.A)+"'' FROM SYINPL (NOLOCK)  WHERE isnull(status,'''')='''' AND INTEGRATION_NAME = ''SSCM_TO_CPQ_PRICING_DATA'' AND INTEGRATION_PAYLOAD NOT LIKE ''%QUOTE_ID%'' ' ")
        
        StatusUpdateQuery = SqlHelper.GetFirst(""+ str(Parameter1.QUERY_CRITERIA_1)+ "  SYINPL SET STATUS = '''',SESSION_ID=''"+str(SYINPL_SESSION.A)+"'' FROM SYINPL (NOLOCK)  WHERE INTEGRATION_NAME = ''SSCM_TO_CPQ_PRICING_DATA'' AND ISNULL(STATUS,'''')=''INPROGRESS'' AND datediff(mi,CPQTABLEENTRYDATEMODIFIED,getdate())>15  ' ")

        StatusUpdateQuery = SqlHelper.GetFirst(""+ str(Parameter1.QUERY_CRITERIA_1)+ "  SYINPL SET STATUS = ''INPROGRESS'',SESSION_ID=''"+str(SYINPL_SESSION.A)+"'' FROM SYINPL (NOLOCK)  WHERE isnull(status,'''')='''' AND INTEGRATION_NAME = ''SSCM_TO_CPQ_PRICING_DATA''  ' ")
        
        #Status Empty
        Jsonquery = SqlHelper.GetList("SELECT replace(INTEGRATION_PAYLOAD,'null','\"\"') as INTEGRATION_PAYLOAD,CpqTableEntryId from SYINPL(NOLOCK) WHERE INTEGRATION_NAME = 'SSCM_TO_CPQ_PRICING_DATA' AND ISNULL(STATUS,'') = 'INPROGRESS' AND SESSION_ID = '"+str(SYINPL_SESSION.A)+"' ")
        
        for json_data in Jsonquery:
                
            exceptinfo = str(json_data.CpqTableEntryId)
            sessiondetail = SqlHelper.GetFirst("SELECT NEWID() AS A")
            
            if "Param" in str(json_data.INTEGRATION_PAYLOAD):
                splited_list = str(json_data.INTEGRATION_PAYLOAD).split("%%")
                rebuilt_data = eval(str(splited_list[1]))
            else:
                splited_list = str(json_data.INTEGRATION_PAYLOAD)
                rebuilt_data = eval(splited_list)       
            
            primaryQuerysession =  SqlHelper.GetFirst("SELECT NEWID() AS A")
            today = datetime.datetime.now()
            Modi_date = today.strftime("%m/%d/%Y %H:%M:%S %p")


            if len(rebuilt_data) != 0:      

                rebuilt_data = rebuilt_data["CPQ_Columns"]
                Table_Names = rebuilt_data.keys()
                Check_flag = 0
                Qt_Id = ''
                Saqico_Flag = 0
                
                for tn in Table_Names:
                    if tn in rebuilt_data:  
                        if 1:
                            if str(type(rebuilt_data[tn])) == "<type 'dict'>":
                                Tbl_data = [rebuilt_data[tn]]
                            else:
                                Tbl_data = rebuilt_data[tn]
                                
                            for record_dict in Tbl_data:

                                if 'HEADBUILD_QTY' not in record_dict:
                                    record_dict['HEADBUILD_QTY'] = ''
                                
                                if 'PER_EVENT_COST_WISEEDSTOCK' not in record_dict:
                                    record_dict['PER_EVENT_COST_WISEEDSTOCK'] = '0'
                                
                                if 'PER_EVENT_COST_WOSEEDSTOCK' not in record_dict:
                                    record_dict['PER_EVENT_COST_WOSEEDSTOCK'] = '0'
                                
                                if 'MODULE_ID' not in record_dict:
                                    record_dict['MODULE_ID'] = '0'
                                
                                if 'MODULE_NAME' not in record_dict:
                                    record_dict['MODULE_NAME'] = '0'
                                
                                if 'MODULE_VERSION_ID' not in record_dict:
                                    record_dict['MODULE_VERSION_ID'] = '0'
                                
                                if 'CONTRACT_YEAR' not in record_dict:
                                    record_dict['CONTRACT_YEAR'] = 'YEAR 1'
                                
                                if 'LOGISTICS_COST' not in record_dict:
                                    record_dict['LOGISTICS_COST'] = '0'
                                
                                if 'OUTSOURCE_COST' not in record_dict:
                                    record_dict['OUTSOURCE_COST'] = '0'
                                
                                if 'FAILURE_COST' not in record_dict:
                                    record_dict['FAILURE_COST'] = '0'
                                
                                if 'WETCLEAN_LABOR_COST' not in record_dict:
                                    record_dict['WETCLEAN_LABOR_COST'] = '0'
                                
                                if 'WETCLEAN_LABOR_HRS' not in record_dict:
                                    record_dict['WETCLEAN_LABOR_HRS'] = '0'
                                    
                                if 'CM_REFURB_COST' not in record_dict:
                                    record_dict['CM_REFURB_COST'] = '0'
                                    
                                if 'CM_REPLACE_COST' not in record_dict:
                                    record_dict['CM_REPLACE_COST'] = '0'
                                    
                                if 'PM_REFURB_COST' not in record_dict:
                                    record_dict['PM_REFURB_COST'] = '0'
                                    
                                if 'PM_REPLACE_COST' not in record_dict:
                                    record_dict['PM_REPLACE_COST'] = '0'
                                    
                                if 'REPLACE_COST' not in record_dict:
                                    record_dict['REPLACE_COST'] = '0'
                                    
                                if 'REFURB_COST' not in record_dict:
                                    record_dict['REFURB_COST'] = '0'

                                for col in ['PM_TECH_LABOR_RATE','LESS_THAN_QTLY_HRS','LABOR_RATE','GREATER_THAN_QTLY_HRS','CM_LABOR_HRS','CM_HOURS_7_24','CM_HOURS_7_12','CM_HOURS_5_8']:
                                    if col not in record_dict:
                                        record_dict[col] = ''

                                splt_info = """ ''{SESSION_ID}'',''{QUOTE_ID}'',''{EQUIPMENT_ID}'',''{ASSEMBLY_ID}'',''{SERVICE_ID}'',''{COST_MODULE_AVAILABLE}'',''{ASSEMBLY_NOT_REQUIRED_FLAG}'',''{GREATER_THAN_QTLY_COST}'',''{LESS_THAN_QTLY_COST}'',''{CLEAN_COST}'',''{SEEDSTOCK_COST}'',''{METROLOGY_COST}'',''{REFURB_COST}'',''{RECOATING_COST}'',''{CM_PART_COST}'',''{PM_PART_COST}'',''{LABOUR_COST}'',''{KPI_COST}'',''{TOTAL_COST_WISEEDSTOCK}'',''{TOTAL_COST_WOSEEDSTOCK}'',''{COST_CALCULATION_STATUS}'',''{MODULE_ID}'',''{MODULE_NAME}'',''{MODULE_VERSION_ID}'',''{NPI}'',''{SERVICE_COMPLEXITY}'',''{PM_TECH_LABOR_RATE}'',''{LESS_THAN_QTLY_HRS}'',''{LABOR_RATE}'',''{GREATER_THAN_QTLY_HRS}'',''{CM_LABOR_HRS}'',''{CM_HOURS_7_24}'',''{LINE}'',''{PER_EVENT_COST_WISEEDSTOCK}'',''{PER_EVENT_COST_WOSEEDSTOCK}'',''{CM_HOURS_7_12}'',''{CONTRACT_YEAR}'',''{CM_HOURS_5_8}'',''{LOGISTICS_COST}'',''{OUTSOURCE_COST}'',''{WETCLEAN_LABOR_COST}'',''{WETCLEAN_LABOR_HRS}'',''{CM_REFURB_COST}'',''{CM_REPLACE_COST}'',''{PM_REFURB_COST}'',''{PM_REPLACE_COST}'',''{FAILURE_COST}'' """.format(SESSION_ID= str(sessiondetail.A),QUOTE_ID = str(record_dict['QUOTE_ID']),EQUIPMENT_ID = str(record_dict['EQUIPMENT_ID']),ASSEMBLY_ID = str(record_dict['ASSEMBLY_ID']),SERVICE_ID = str(record_dict['SERVICE_ID']),COST_MODULE_AVAILABLE= str(record_dict['COST_MODULE_AVAILABLE']),ASSEMBLY_NOT_REQUIRED_FLAG = str(record_dict['ASSEMBLY_NOT_REQUIRED_FLAG']),GREATER_THAN_QTLY_COST = str(record_dict['GREATER_THAN_QTLY_COST']),LESS_THAN_QTLY_COST = str(record_dict['LESS_THAN_QTLY_COST']),CLEAN_COST = str(record_dict['CLEAN_COST']),SEEDSTOCK_COST = str(record_dict['SEEDSTOCK_COST']),METROLOGY_COST= str(record_dict['METROLOGY_COST']),REFURB_COST = str(record_dict['REFURB_COST']),RECOATING_COST = str(record_dict['RECOATING_COST']),CM_PART_COST = str(record_dict['CM_PART_COST']),PM_PART_COST = str(record_dict['PM_PART_COST']),LABOUR_COST= str(record_dict['LABOR_COST']),KPI_COST = str(record_dict['KPI_COST']),TOTAL_COST_WISEEDSTOCK = str(record_dict['TOTAL_COST_WISEEDSTOCK']),TOTAL_COST_WOSEEDSTOCK = str(record_dict['TOTAL_COST_WOSEEDSTOCK']),COST_CALCULATION_STATUS = str(record_dict['COST_CALCULATION_STATUS']),MODULE_ID = str(record_dict['MODULE_ID']), MODULE_NAME= str(record_dict['MODULE_NAME']),MODULE_VERSION_ID= str(record_dict['MODULE_VERSION_ID']),NPI = str(record_dict['NPI']),SERVICE_COMPLEXITY = str(record_dict['SERVICE_COMPLEXITY']),PM_TECH_LABOR_RATE = str(record_dict['PM_TECH_LABOR_RATE']),LESS_THAN_QTLY_HRS = str(record_dict['LESS_THAN_QTLY_HRS']),LABOR_RATE= str(record_dict['LABOR_RATE']),GREATER_THAN_QTLY_HRS = str(record_dict['GREATER_THAN_QTLY_HRS']),CM_LABOR_HRS = str(record_dict['CM_LABOR_HRS']),CM_HOURS_7_24 = str(record_dict['CM_HOURS_7_24']),LINE = str(record_dict['LINE']),PER_EVENT_COST_WISEEDSTOCK = str(record_dict['PER_EVENT_COST_WISEEDSTOCK']) ,PER_EVENT_COST_WOSEEDSTOCK = str(record_dict['PER_EVENT_COST_WOSEEDSTOCK']),CM_HOURS_7_12 = str(record_dict['CM_HOURS_7_12']),CONTRACT_YEAR = str(record_dict['CONTRACT_YEAR']),CM_HOURS_5_8 = str(record_dict['CM_HOURS_5_8']),LOGISTICS_COST = str(record_dict['LOGISTICS_COST']),OUTSOURCE_COST = str(record_dict['OUTSOURCE_COST']),WETCLEAN_LABOR_COST = str(record_dict['WETCLEAN_LABOR_COST']),WETCLEAN_LABOR_HRS = str(record_dict['WETCLEAN_LABOR_HRS']),CM_REFURB_COST = str(record_dict['CM_REFURB_COST']),CM_REPLACE_COST = str(record_dict['CM_REPLACE_COST']),PM_REFURB_COST = str(record_dict['PM_REFURB_COST']),PM_REPLACE_COST = str(record_dict['PM_REPLACE_COST']),FAILURE_COST = str(record_dict['FAILURE_COST'])  )

                                primaryQueryItems = SqlHelper.GetFirst( ""+ str(Parameter.QUERY_CRITERIA_1)+ " SAQICO_INBOUND (HEADREBUILD_QTY,SESSION_ID,QUOTE_ID,EQUIPMENT_ID,ASSEMBLY_ID,SERVICE_ID,COST_MODULE_AVAILABLE,ASSEMBLY_NOT_REQUIRED_FLAG,GREATER_THAN_QTLY_COST,LESS_THAN_QTLY_COST,CLEAN_COST,SEEDSTOCK_COST,METROLOGY_COST,REFURB_COST,RECOATING_COST,CM_PART_COST,PM_PART_COST,LABOUR_COST,KPI_COST,TOTAL_COST_WISEEDSTOCK,TOTAL_COST_WOSEEDSTOCK,COST_CALCULATION_STATUS,MODULE_ID,MODULE_NAME,MODULE_VERSION_ID,NPI,SERVICE_COMPLEXITY,PM_TECH_LABOR_RATE,LESS_THAN_QTLY_HRS,LABOR_RATE,GREATER_THAN_QTLY_HRS,CM_LABOR_HRS,CM_HOURS_7_24,LINE,PER_EVENT_COST_WISEEDSTOCK,PER_EVENT_COST_WOSEEDSTOCK,CM_HOURS_7_12,CONTRACT_YEAR,CM_HOURS_5_8,LOGISTICS_COST,OUTSOURCE_COST,WETCLEAN_LABOR_COST,WETCLEAN_LABOR_HRS,CM_REFURB_COST,CM_REPLACE_COST,PM_REFURB_COST,PM_REPLACE_COST,FAILURE_COST)  select CASE WHEN ISNULL(''"+str(record_dict['HEADBUILD_QTY'])+ "'','''')='''' THEN NULL ELSE ''"+str(record_dict['HEADBUILD_QTY'])+ "'' END ,"+str(splt_info)+ " ' ")
                                
                                
                                Check_flag = 1
                
                primaryQueryItems = SqlHelper.GetFirst(
                                    ""
                                    + str(Parameter1.QUERY_CRITERIA_1)
                                    + "  A SET QUOTE_ID = B.QUOTE_ID,REVISION_ID = B.QTEREV_ID FROM SAQICO_INBOUND (NOLOCK) A JOIN SAQTRV B(NOLOCK) ON A.QUOTE_ID = B.QUOTE_ID+''-''+CONVERT(VARCHAR,QTEREV_ID)  WHERE ISNULL(PROCESS_STATUS,'''')='''' AND ISNULL(SESSION_ID,'''')=''"+str(sessiondetail.A)+ "'' '")
                                                    
                primaryQueryItems = SqlHelper.GetFirst(
                                    ""
                                    + str(Parameter1.QUERY_CRITERIA_1)
                                    + "  A SET TOTAL_COST_WISEEDSTOCK = TOTAL_COST_WOSEEDSTOCK FROM SAQICO_INBOUND (NOLOCK) A WHERE ISNULL(PROCESS_STATUS,'''')='''' AND ISNULL(SESSION_ID,'''')=''"+str(sessiondetail.A)+ "'' AND ISNULL(CONVERT(FLOAT,TOTAL_COST_WISEEDSTOCK),0)<=0 '")
                                
                Qt_Id = SqlHelper.GetFirst("select QUOTE_ID,REVISION_ID from SAQICO_INBOUND(Nolock) where ISNULL(SESSION_ID,'')='"+str(sessiondetail.A)+ "' ")
                
                #Annualized Item Record ID
                primaryQueryItems = SqlHelper.GetFirst(
                                    ""
                                    + str(Parameter1.QUERY_CRITERIA_1)
                                    + "  A SET SERVICE_ID = B.SERVICE_ID,TOTWO = TOTAL_COST_WOSEEDSTOCK ,TOTWI = TOTAL_COST_WISEEDSTOCK  FROM SAQICO_INBOUND (NOLOCK) A JOIN SAQICO B(NOLOCK) ON A.QUOTE_ID = B.QUOTE_ID AND A.REVISION_ID = B.QTEREV_ID AND A.LINE = B.LINE AND A.EQUIPMENT_ID = B.EQUIPMENT_ID WHERE ISNULL(PROCESS_STATUS,'''')='''' AND ISNULL(SESSION_ID,'''')=''"+str(sessiondetail.A)+ "'' AND B.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND B.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' '") 
                                    
                Saqicoquery = SqlHelper.GetFirst("select count(*) as cnt from SAQICO(Nolock) A JOIN SAQRIO B ON A.QUOTE_ID = B.QUOTE_ID where A.QUOTE_ID = '"+str(Qt_Id.QUOTE_ID)+"' AND A.QTEREV_ID = '"+str(Qt_Id.REVISION_ID)+"' ")
                
                #Owner ID patch to avoid errors.
                primaryQueryItems = SqlHelper.GetFirst(
                                    ""
                                    + str(Parameter1.QUERY_CRITERIA_1)
                                    + "  A SET OWNER_ID = CPQTABLEENTRYADDEDBY FROM SAQTMT (NOLOCK)A WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND ISNULL(OWNER_ID,'''')='''' '")
                
                
                if Saqicoquery.cnt >0:
                    Saqico_Flag = 1
                
                ToEml = SqlHelper.GetFirst("SELECT ISNULL(OWNER_ID,'X0116954') as OWNER_ID FROM SAQTMT (NOLOCK) WHERE SAQTMT.QUOTE_ID = '"+str(Qt_Id.QUOTE_ID)+"'  ")
                Glb_Quote_Id = str(Qt_Id.QUOTE_ID)

                if Check_flag == 1 and Saqico_Flag == 1:
                    
                    Emailinfo = SqlHelper.GetFirst("SELECT QUOTE_ID,SSCM,0 as REMANING,QUOTE_RECORD_ID FROM (SELECT A.QUOTE_ID,COUNT(DISTINCT B.EQUIPMENT_ID) AS SSCM,A.QUOTE_RECORD_ID  FROM SAQICO (NOLOCK) A JOIN SAQRIO (NOLOCK) B ON A.QUOTE_ID = B.QUOTE_ID AND A.QTEREV_ID = B.QTEREV_ID WHERE A.QUOTE_ID = '"+str(Qt_Id.QUOTE_ID)+"' AND A.QTEREV_ID = '"+str(Qt_Id.REVISION_ID)+"'  group by A.Quote_ID,A.QUOTE_RECORD_ID )SUB_SAQICO ")  
                    
                      
                    
                    Emailinfo1 = SqlHelper.GetFirst("SELECT QUOTE_ID,CPQ FROM (SELECT SAQICO_INBOUND.QUOTE_ID,COUNT(DISTINCT SAQICO_INBOUND.EQUIPMENT_ID) AS CPQ FROM SAQICO_INBOUND (NOLOCK) WHERE SAQICO_INBOUND.QUOTE_ID = '"+str(Qt_Id.QUOTE_ID)+"' AND SAQICO_INBOUND.REVISION_ID = '"+str(Qt_Id.REVISION_ID)+"' AND ISNULL(SESSION_ID,'')='"+str(sessiondetail.A)+ "' group by SAQICO_INBOUND.Quote_ID )SUB_SAQICO ")  
                
                    # Mail system               
                    Header = "<!DOCTYPE html><html><head><style>table {font-family: Calibri, sans-serif; border-collapse: collapse; width: 75%}td, th {  border: 1px solid #dddddd;  text-align: left; padding: 8px;}.im {color: #222;}tr:nth-child(even) {background-color: #dddddd;} #grey{background: rgb(245,245,245);} #bd{color : 'black';} </style></head><body id = 'bd'>"

                    Table_start = "<p>Hi Team,<br><br>Cost data has been received from SSCM for the below Quote ID and the CPQ price calculation has been initiated. Will let you know shortly about the pricing status.</p><table class='table table-bordered'><tr><th id = 'grey'>Quote ID</th><th id = 'grey'>Tools sent (CPQ-SSCM)</th><th id = 'grey'>Tools received (SSCM-CPQ)</th><th id = 'grey'>Price Calculation Status</th></tr><tr><td >"+str(Qt_Id.QUOTE_ID)+"</td><td>"+str(Emailinfo.SSCM)+"</td ><td>"+str(Emailinfo1.CPQ)+"</td><td>Initiated</td></tr>"

                    Table_info = ""
                    Table_End = "</table><p><strong>Note : </strong>Please do not reply to this email.</p></body></html>"

                    Error_Info = Header + Table_start + Table_info + Table_End

                    LOGIN_CRE = SqlHelper.GetFirst("SELECT USER_NAME as Username,Password FROM SYCONF where Domain ='SUPPORT_MAIL'")

                    # Create new SmtpClient object
                    mailClient = SmtpClient("10.150.65.7")

                    if ToEml is None:

                        UserEmail = SqlHelper.GetFirst("SELECT isnull(email,'"+str(LOGIN_CRE.Username)+"') as email FROM saempl (nolock) where employee_id  = 'X0116954'")

                    else:

                        UserEmail = SqlHelper.GetFirst("SELECT isnull(email,'"+str(LOGIN_CRE.Username)+"') as email FROM saempl (nolock) where employee_id  = '"+str(ToEml.OWNER_ID)+"'")

                    # Create two mail adresses, one for send from and the another for recipient
                    if UserEmail is None:
                        toEmail = MailAddress("suresh.muniyandi@bostonharborconsulting.com")
                    else:
                        toEmail = MailAddress(UserEmail.email)
                    fromEmail = 'noreply@calliduscloud.com'

                    # Create new MailMessage object
                    msg = MailMessage()
            
                    msg.From = MailAddress(fromEmail)
                    msg.To.Add(toEmail)

                    # Set message subject and body
                    msg.Subject = "Pricing Initiated - AMAT CPQ(P-Tenant)"
                    msg.IsBodyHtml = True
                    msg.Body = Error_Info

                    # Bcc Emails    
                    copyEmail4 = MailAddress("baji.baba@bostonharborconsulting.com")
                    msg.Bcc.Add(copyEmail4)

                    copyEmail6 = MailAddress("suresh.muniyandi@bostonharborconsulting.com")
                    msg.Bcc.Add(copyEmail6) 

                    copyEmail7 = MailAddress("christoper.aravinth@bostonharborconsulting.com")
                    msg.Bcc.Add(copyEmail7)


                    # Send the message
                    mailClient.Send(msg)

                    #Calculation code started   
                    sessionid = SqlHelper.GetFirst("SELECT NEWID() AS A")
                    timestamp_sessionid = "'" + str(sessionid.A) + "'"  
                    
                    CRMQT = SqlHelper.GetFirst("select convert(varchar(100),c4c_quote_id) as c4c_quote_id from SAQTMT(nolock) WHERE QUOTE_ID = '"+str(Qt_Id.QUOTE_ID)+"' ") 
                    
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                        + str(Parameter1.QUERY_CRITERIA_1)
                        + "  SAQICO_INBOUND SET TIMESTAMP = '"+str(timestamp_sessionid)+"',PROCESS_STATUS = ''INPROGRESS'' FROM SAQICO_INBOUND (NOLOCK)  WHERE ISNULL(PROCESS_STATUS,'''')='''' AND ISNULL(SESSION_ID,'''')=''"+str(sessiondetail.A)+ "'' '")
                    
                    #Entitlement Temp       
                    sess = SqlHelper.GetFirst("select left(convert(varchar(100),newid()),5) as sess  ")

                    SAQIEN = "SAQIEN_BKP_"+str(CRMQT.c4c_quote_id)+str(sess.sess)
                    CRMTMP = "CRMTMP_BKP_"+str(CRMQT.c4c_quote_id)+str(sess.sess)
                    SAQSCE = "SAQSCE_BKP_"+str(CRMQT.c4c_quote_id)+str(sess.sess)
                    
                    SAQIEN_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQIEN)+"'' ) BEGIN DROP TABLE "+str(SAQIEN)+" END  ' ")
                    
                    CRMTMP_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(CRMTMP)+"'' ) BEGIN DROP TABLE "+str(CRMTMP)+" END  ' ")
                    
                    SAQSCE_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQSCE)+"'' ) BEGIN DROP TABLE "+str(SAQSCE)+" END  ' ")
                    
                    #Exchange Rate
                    roundcurr1 = SqlHelper.GetFirst("select distinct CASE WHEN ROUNDING_DECIMAL_PLACES = '' THEN 0  ELSE ROUNDING_DECIMAL_PLACES END  AS DECIMAL_PLACES,CASE WHEN ROUNDING_METHOD='ROUND DOWN' THEN 1 ELSE 0 END AS ROUNDING_METHOD from prcurr (nolock) where currency= 'USD' ")
                    
                    roundcurr = SqlHelper.GetFirst("select distinct CASE WHEN ROUNDING_DECIMAL_PLACES = '' THEN 0  ELSE ROUNDING_DECIMAL_PLACES END  AS DECIMAL_PLACES,CASE WHEN ROUNDING_METHOD='ROUND DOWN' THEN 1 ELSE 0 END AS ROUNDING_METHOD from SAQRIT(nolock) a join prcurr (nolock) on a.DOC_CURRENCY = prcurr.currency where QUOTE_ID = '"+str(Qt_Id.QUOTE_ID)+"' AND QTEREV_ID = '"+str(Qt_Id.REVISION_ID)+"' ")
                    
                    #Quote Item Covered Object Assembly Update 
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                        + str(Parameter1.QUERY_CRITERIA_1)
                        + "  A SET CM_PART_COST=CONVERT(FLOAT,B.CM_PART_COST),PM_PART_COST = CONVERT(FLOAT,B.PM_PART_COST),ASSEMBLY_NOT_MAPPED = B.ASSEMBLY_NOT_REQUIRED_FLAG,CLEANING_COST = CONVERT(FLOAT,B.CLEAN_COST),COST_MODULE_AVAILABLE = B.COST_MODULE_AVAILABLE,COST_MODULE_STATUS = B.COST_CALCULATION_STATUS,GREATER_THAN_QTLY_PM_COST = CONVERT(FLOAT,B.GREATER_THAN_QTLY_COST),KPI_COST = CONVERT(FLOAT,B.KPI_COST),LABOR_COST = CONVERT(FLOAT,B.LABOUR_COST),LESS_THAN_QTLY_PM_COST= CONVERT(FLOAT,B.LESS_THAN_QTLY_COST),METROLOGY_COST=CONVERT(FLOAT, B.METROLOGY_COST),RECOATING_COST = CONVERT(FLOAT,B.RECOATING_COST),REFURB_COST = CONVERT(FLOAT,B.CM_REFURB_COST),REPLACE_COST = CONVERT(FLOAT,B.CM_REPLACE_COST),PM_REFURB_COST = CONVERT(FLOAT,B.PM_REFURB_COST),PM_REPLACE_COST = CONVERT(FLOAT,B.PM_REPLACE_COST),WETCLN_LBRCST = CONVERT(FLOAT,B.WETCLEAN_LABOR_COST),WETCLN_LBRHRS = CONVERT(FLOAT,B.WETCLEAN_LABOR_HRS),SEEDSTOCK_COST = CONVERT(FLOAT,B.SEEDSTOCK_COST),TOTAL_COST_WOSEEDSTOCK = CONVERT(FLOAT,B.TOTAL_COST_WOSEEDSTOCK),TOTAL_COST_WSEEDSTOCK = CONVERT(FLOAT,TOTAL_COST_WISEEDSTOCK),NPI = B.NPI,SERVICE_COMPLEXITY = B.SERVICE_COMPLEXITY,LESS_THAN_QTLY_HRS = CONVERT(FLOAT,B.LESS_THAN_QTLY_HRS),GREATER_THAN_QTLY_HRS = CONVERT(FLOAT,B.GREATER_THAN_QTLY_HRS),CM_LABOR_HRS = CONVERT(FLOAT,B.CM_LABOR_HRS),CM_HOURS_5_8 = CONVERT(FLOAT,B.CM_HOURS_5_8),CM_HOURS_7_12 = CONVERT(FLOAT,B.CM_HOURS_7_12),CM_HOURS_7_24 = CONVERT(FLOAT,B.CM_HOURS_7_24),LABOR_RATE = CONVERT(FLOAT,B.LABOR_RATE),PM_TECH_LABOR_RATE = CONVERT(FLOAT,B.PM_TECH_LABOR_RATE) FROM SAQICA A(NOLOCK) JOIN SAQICO_INBOUND B(NOLOCK) ON A.QUOTE_ID = B.QUOTE_ID AND A.QTEREV_ID = B.REVISION_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.ASSEMBLY_ID = B.ASSEMBLY_ID AND A.CNTYEAR = B.CONTRACT_YEAR AND A.LINE = B.LINE WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND A.QUOTE_ID =''"+str(Qt_Id.QUOTE_ID)+"'' ' ")
                    
                    #Quote Item Covered Object Roll Up Cost
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                        + str(Parameter1.QUERY_CRITERIA_1)
                    
                        + "  A SET CMLBRC = B.LABOUR_COST, CMPREC = REPLACE_COST, CMPRFC = REFURB_COST, GQPLBC = GREATER_THAN_QTLY_COST, LQPLBC = LESS_THAN_QTLY_COST, PMPCLC = CLEAN_COST, PMPMEC  = METROLOGY_COST, PMPRCC = RECOATING_COST, SDSTKC =  SEEDSTOCK_COST, KPINDC = KPI_COST, FAILRC = FAILURE_COST, OUTSRC = OUTSOURCE_COST, LGSTCC = LOGISTICS_COST , TNHRPT = HEADREBUILD_QTY, TCWOSS = B.TOTAL_COST_WOSEEDSTOCK,TCWISS = TOTAL_COST_WISEEDSTOCK,PMPREC = PM_REPLACE_COST , PMPRFC=  PM_REFURB_COST FROM SAQICO A(NOLOCK) JOIN (SELECT QUOTE_ID,SERVICE_ID,SUM(CONVERT(FLOAT,PM_REPLACE_COST)) AS PM_REPLACE_COST,SUM(CONVERT(FLOAT,PM_REFURB_COST)) AS PM_REFURB_COST,SUM(CONVERT(FLOAT,CM_PART_COST)) AS CM_PART_COST,SUM(CONVERT(FLOAT,PM_PART_COST)) AS PM_PART_COST,SUM(CONVERT(FLOAT,CLEAN_COST)) AS CLEAN_COST, SUM(CONVERT(FLOAT,GREATER_THAN_QTLY_COST)) AS GREATER_THAN_QTLY_COST,SUM(CONVERT(FLOAT,KPI_COST)) AS KPI_COST,SUM(CONVERT(FLOAT,LABOUR_COST)) AS LABOUR_COST,SUM(CONVERT(FLOAT,LESS_THAN_QTLY_COST)) AS LESS_THAN_QTLY_COST,SUM(CONVERT(FLOAT,METROLOGY_COST)) AS METROLOGY_COST,SUM(CONVERT(FLOAT,RECOATING_COST)) AS RECOATING_COST,SUM(CONVERT(FLOAT,CM_REFURB_COST)) AS REFURB_COST, SUM(CONVERT(FLOAT,SEEDSTOCK_COST)) AS SEEDSTOCK_COST,SUM(CONVERT(FLOAT,TOTAL_COST_WOSEEDSTOCK)) AS TOTAL_COST_WOSEEDSTOCK,SUM(CONVERT(FLOAT,TOTAL_COST_WISEEDSTOCK)) AS TOTAL_COST_WISEEDSTOCK,REVISION_ID,MIN(HEADREBUILD_QTY) AS HEADREBUILD_QTY,SUM(CONVERT(FLOAT,CM_REPLACE_COST)) AS REPLACE_COST,SUM(CONVERT(FLOAT,FAILURE_COST)) AS FAILURE_COST, SUM(CONVERT(FLOAT,OUTSOURCE_COST)) AS OUTSOURCE_COST, SUM(CONVERT(FLOAT,LOGISTICS_COST)) AS LOGISTICS_COST,LINE,SUM(CONVERT(FLOAT,PER_EVENT_COST_WISEEDSTOCK)) AS PER_EVENT_COST_WISEEDSTOCK,EQUIPMENT_ID,CONTRACT_YEAR FROM SAQICO_INBOUND B(NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' GROUP BY QUOTE_ID,SERVICE_ID,REVISION_ID,LINE,EQUIPMENT_ID,CONTRACT_YEAR )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID  AND A.QTEREV_ID = B.REVISION_ID AND A.LINE = B.LINE AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.CNTYER = B.CONTRACT_YEAR WHERE QTETYP = ''TOOL BASED'' AND A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' ' ")
                    #PMSA
                    #Quote Item Covered Object Roll Up Cost
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                        + str(Parameter1.QUERY_CRITERIA_1)
                        + "  A SET CMLBRC = B.LABOUR_COST, CMPREC = REPLACE_COST, CMPRFC =   REFURB_COST, GQPLBC = GREATER_THAN_QTLY_COST, LQPLBC = LESS_THAN_QTLY_COST, PMPCLC = CLEAN_COST, PMPMEC    = METROLOGY_COST, PMPRCC = RECOATING_COST, SDSTKC =  SEEDSTOCK_COST, KPINDC = KPI_COST, FAILRC = FAILURE_COST, OUTSRC = OUTSOURCE_COST, LGSTCC = LOGISTICS_COST , TNHRPT = HEADREBUILD_QTY, TCWOSS = B.TOTAL_COST_WOSEEDSTOCK,TCWISS = B.TOTAL_COST_WISEEDSTOCK,AIPEOS=B.PER_EVENT_COST_WOSEEDSTOCK,AIPEWS = B.PER_EVENT_COST_WISEEDSTOCK,PMPREC = PM_REPLACE_COST , PMPRFC=  PM_REFURB_COST FROM SAQICO A(NOLOCK) JOIN (SELECT QUOTE_ID,SERVICE_ID,SUM(CONVERT(FLOAT,CM_PART_COST)) AS CM_PART_COST,SUM(CONVERT(FLOAT,PM_PART_COST)) AS PM_PART_COST,SUM(CONVERT(FLOAT,CLEAN_COST)) AS CLEAN_COST, SUM(CONVERT(FLOAT,GREATER_THAN_QTLY_COST)) AS GREATER_THAN_QTLY_COST,SUM(CONVERT(FLOAT,KPI_COST)) AS KPI_COST,SUM(CONVERT(FLOAT,LABOUR_COST)) AS LABOUR_COST,SUM(CONVERT(FLOAT,LESS_THAN_QTLY_COST)) AS LESS_THAN_QTLY_COST,SUM(CONVERT(FLOAT,METROLOGY_COST)) AS METROLOGY_COST,SUM(CONVERT(FLOAT,RECOATING_COST)) AS RECOATING_COST,SUM(CONVERT(FLOAT,CM_REFURB_COST)) AS REFURB_COST, SUM(CONVERT(FLOAT,SEEDSTOCK_COST)) AS SEEDSTOCK_COST,SUM(CONVERT(FLOAT,TOTAL_COST_WOSEEDSTOCK)) AS TOTAL_COST_WOSEEDSTOCK,SUM(CONVERT(FLOAT,TOTAL_COST_WISEEDSTOCK)) AS TOTAL_COST_WISEEDSTOCK,REVISION_ID,MIN(HEADREBUILD_QTY) AS HEADREBUILD_QTY,SUM(CONVERT(FLOAT,CM_REPLACE_COST)) AS REPLACE_COST,SUM(CONVERT(FLOAT,FAILURE_COST)) AS FAILURE_COST, SUM(CONVERT(FLOAT,OUTSOURCE_COST)) AS OUTSOURCE_COST, SUM(CONVERT(FLOAT,LOGISTICS_COST)) AS LOGISTICS_COST,LINE,SUM(CONVERT(FLOAT,PER_EVENT_COST_WISEEDSTOCK)) AS PER_EVENT_COST_WISEEDSTOCK,SUM(CONVERT(FLOAT,PER_EVENT_COST_WOSEEDSTOCK)) AS PER_EVENT_COST_WOSEEDSTOCK,EQUIPMENT_ID,CONTRACT_YEAR,SUM(CONVERT(FLOAT,PM_REPLACE_COST)) AS PM_REPLACE_COST,SUM(CONVERT(FLOAT,PM_REFURB_COST)) AS PM_REFURB_COST FROM SAQICO_INBOUND B(NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' GROUP BY QUOTE_ID,SERVICE_ID,REVISION_ID,LINE,EQUIPMENT_ID,CONTRACT_YEAR )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID  AND A.QTEREV_ID = B.REVISION_ID AND A.LINE = B.LINE AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.CNTYER = B.CONTRACT_YEAR WHERE QTETYP <> ''TOOL BASED'' AND A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' ' ")
                        
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                        + str(Parameter1.QUERY_CRITERIA_1)
                        + "  A SET MODULE_ID=B.MODULE_ID,MODULE_NAME = B.MODULE_NAME,MODULE_VERSION_ID = B.MODULE_VERSION_ID FROM SAQICA A(NOLOCK) JOIN (SELECT  DISTINCT QUOTE_ID,SERVICE_ID,REVISION_ID,MODULE_ID,MODULE_NAME,LINE,EQUIPMENT_ID,ASSEMBLY_ID,MODULE_VERSION_ID,CONTRACT_YEAR  FROM SAQICO_INBOUND B(NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID  AND A.QTEREV_ID = B.REVISION_ID AND A.LINE = B.LINE AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.ASSEMBLY_ID = B.ASSEMBLY_ID AND CNTYEAR = CONTRACT_YEAR WHERE A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"''  '")
                    
                    #Cost Module Version
                    
                    S = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE SAQICA SET MODVRS_DIRTY_FLAG = ''FALSE'' FROM SAQICA (NOLOCK) WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"''  '")

                    S = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE SAQICO SET MODVRS_DIRTY_FLAG = ''FALSE'' FROM SAQICO (NOLOCK) WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"''  '")

                    S = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE SAQRIT SET MODVRS_DIRTY_FLAG = ''FALSE'' FROM SAQRIT (NOLOCK) WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"''  '")

                    S = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE SAQTRV SET MODVRS_DIRTY_FLAG = ''FALSE'' FROM SAQTRV (NOLOCK) WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"''  '")

                    S = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE SAQICA SET MODVRS_DIRTY_FLAG = ''TRUE'' FROM SAQICA (NOLOCK) WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND ISNULL(MODULE_VERSION_ID,'''') <> ISNULL(NEW_MODULE_VERSION_ID,'''') AND ISNULL(NEW_MODULE_VERSION_ID,'''')<>''''  '")

                    S = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE SAQICO SET MODVRS_DIRTY_FLAG = SAQICA.MODVRS_DIRTY_FLAG  FROM SAQICA (NOLOCK) JOIN SAQICO(NOLOCK) ON SAQICA.QUOTE_ID = SAQICO.QUOTE_ID AND SAQICA.QTEREV_ID = SAQICO.QTEREV_ID AND SAQICA.LINE = SAQICO.LINE AND SAQICA.EQUIPMENT_ID = SAQICO.EQUIPMENT_ID AND SAQICA.CNTYEAR = SAQICO.CNTYER WHERE ISNULL(SAQICA.MODVRS_DIRTY_FLAG,''FALSE'')=''TRUE'' AND SAQICO.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND SAQICO.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"''  '")

                    S = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE SAQRIT SET SAQRIT.MODVRS_DIRTY_FLAG = SAQICO.MODVRS_DIRTY_FLAG  FROM SAQRIT (NOLOCK) JOIN SAQICO(NOLOCK) ON SAQRIT.QUOTE_ID = SAQICO.QUOTE_ID AND SAQRIT.QTEREV_ID = SAQICO.QTEREV_ID AND SAQRIT.LINE = SAQICO.LINE WHERE ISNULL(SAQICO.MODVRS_DIRTY_FLAG,''FALSE'')=''TRUE''  AND SAQRIT.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND SAQRIT.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"''  '")

                    S = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE SAQTRV SET MODVRS_DIRTY_FLAG = SAQRIT.MODVRS_DIRTY_FLAG  FROM SAQRIT (NOLOCK) JOIN SAQTRV(NOLOCK) ON SAQRIT.QUOTE_ID = SAQTRV.QUOTE_ID AND SAQRIT.QTEREV_ID = SAQTRV.QTEREV_ID WHERE ISNULL(SAQRIT.MODVRS_DIRTY_FLAG,''FALSE'')=''TRUE'' AND SAQTRV.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND SAQTRV.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' '")
                    
                                                
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                        + str(Parameter1.QUERY_CRITERIA_1)
                        + " A SET GREENBOOK = B.GRNBOK, BLUEBOOK = B.BLUBOK, REGION = B.REGION FROM SAQICO_INBOUND (NOLOCK) A JOIN SAQICO (NOLOCK) B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.LINE = B.LINE AND A.REVISION_ID = B.QTEREV_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND B.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND B.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' '")
                        
                    #NPI Starts
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                        + str(Parameter1.QUERY_CRITERIA_1)
                        + "  A SET TOOL_NPI = ''Yes'' FROM SAQICO_INBOUND A(NOLOCK) JOIN (SELECT QUOTE_ID,SERVICE_ID,EQUIPMENT_ID,TIMESTAMP,SESSION_ID FROM SAQICO_INBOUND (NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND NPI = ''TRUE'' )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.TIMESTAMP = B.TIMESTAMP AND A.SESSION_ID = B.SESSION_ID WHERE A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.TIMESTAMP = '"+str(timestamp_sessionid)+"' ' ")

                    primaryQueryItems = SqlHelper.GetFirst(
                                            ""
                                            + str(Parameter1.QUERY_CRITERIA_1)
                                            + "  SAQICO_INBOUND SET TOOL_NPI = ''No'' FROM SAQICO_INBOUND (NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND ISNULL(TOOL_NPI,''FALSE'') = ''FALSE''  ' ")
                    
                    #Z0091 NPI
                    primaryQueryItems = SqlHelper.GetFirst(
                                                ""
                                                + str(Parameter1.QUERY_CRITERIA_1)
                                                + "  A SET NPI_COEFFICIENT = CONVERT(VARCHAR,ENTITLEMENT_COEFFICIENT),NPI_CODE = ENTITLEMENT_DISPLAY_VALUE FROM SAQICO_INBOUND (NOLOCK) A JOIN PREGBV B(NOLOCK) ON A.TOOL_NPI = B.ENTITLEMENT_DISPLAY_VALUE AND A.GREENBOOK = B.GREENBOOK WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND ISNULL(TOOL_NPI,'''') <> '''' AND ENTITLEMENT_ID = ''AGS_Z0091_VAL_NPIREC'' AND A.SERVICE_ID = ''Z0091'' AND A.GREENBOOK <> ''PDC'' AND A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"''  ' ")
                    
                    #Z0092 NPI
                    primaryQueryItems = SqlHelper.GetFirst(
                    ""
                    + str(Parameter1.QUERY_CRITERIA_1)
                    + "  A SET NPI_COEFFICIENT = CONVERT(VARCHAR,ENTITLEMENT_COEFFICIENT),NPI_CODE = ENTITLEMENT_DISPLAY_VALUE FROM SAQICO_INBOUND (NOLOCK) A JOIN PREGBV B(NOLOCK) ON A.TOOL_NPI = B.ENTITLEMENT_DISPLAY_VALUE AND A.GREENBOOK = B.GREENBOOK WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND ISNULL(TOOL_NPI,'''') <> '''' AND ENTITLEMENT_ID = ''AGS_Z0092_VAL_NPIREC'' AND A.SERVICE_ID = ''Z0092'' AND A.GREENBOOK <> ''PDC'' AND A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' ' ")
                    
                    #Z0004 NPI
                    primaryQueryItems = SqlHelper.GetFirst(
                    ""
                    + str(Parameter1.QUERY_CRITERIA_1)
                    + "  A SET NPI_COEFFICIENT = CONVERT(VARCHAR,ENTITLEMENT_COEFFICIENT),NPI_CODE = ENTITLEMENT_DISPLAY_VALUE FROM SAQICO_INBOUND (NOLOCK) A JOIN PREGBV B(NOLOCK) ON A.TOOL_NPI = B.ENTITLEMENT_DISPLAY_VALUE AND A.GREENBOOK = B.GREENBOOK WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND ISNULL(TOOL_NPI,'''') <> '''' AND ENTITLEMENT_ID = ''AGS_Z0004_VAL_NPIREC'' AND A.SERVICE_ID = ''Z0004'' AND A.GREENBOOK <> ''PDC'' AND A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' ' ")
                    
                    #Z0099 NPI
                    primaryQueryItems = SqlHelper.GetFirst(
                    ""
                    + str(Parameter1.QUERY_CRITERIA_1)
                    + "  A SET NPI_COEFFICIENT = CONVERT(VARCHAR,ENTITLEMENT_COEFFICIENT),NPI_CODE = ENTITLEMENT_DISPLAY_VALUE FROM SAQICO_INBOUND (NOLOCK) A JOIN PREGBV B(NOLOCK) ON A.TOOL_NPI = B.ENTITLEMENT_DISPLAY_VALUE AND A.GREENBOOK = B.GREENBOOK WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND ISNULL(TOOL_NPI,'''') <> '''' AND ENTITLEMENT_ID = ''AGS_Z0099_VAL_NPIREC'' AND A.SERVICE_ID = ''Z0099'' AND A.GREENBOOK <> ''PDC'' AND A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' ' ")
                    
                    #Z0035 NPI
                    primaryQueryItems = SqlHelper.GetFirst(
                    ""
                    + str(Parameter1.QUERY_CRITERIA_1)
                    + "  A SET NPI_COEFFICIENT = CONVERT(VARCHAR,ENTITLEMENT_COEFFICIENT),NPI_CODE = ENTITLEMENT_DISPLAY_VALUE FROM SAQICO_INBOUND (NOLOCK) A JOIN PREGBV B(NOLOCK) ON A.TOOL_NPI = B.ENTITLEMENT_DISPLAY_VALUE AND A.GREENBOOK = B.GREENBOOK WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND ISNULL(TOOL_NPI,'''') <> '''' AND ENTITLEMENT_ID = ''AGS_Z0035_VAL_NPIREC'' AND A.SERVICE_ID = ''Z0035'' AND A.GREENBOOK <> ''PDC'' AND A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' ' ")
                    
                    #Z0009 NPI
                    primaryQueryItems = SqlHelper.GetFirst(
                    ""
                    + str(Parameter1.QUERY_CRITERIA_1)
                    + "  A SET NPI_COEFFICIENT = CONVERT(VARCHAR,ENTITLEMENT_COEFFICIENT),NPI_CODE = ENTITLEMENT_DISPLAY_VALUE FROM SAQICO_INBOUND (NOLOCK) A JOIN PREGBV B(NOLOCK) ON A.TOOL_NPI = B.ENTITLEMENT_DISPLAY_VALUE AND A.GREENBOOK = B.GREENBOOK WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND ISNULL(TOOL_NPI,'''') <> '''' AND ENTITLEMENT_ID = ''AGS_Z0009_VAL_NPIREC'' AND A.SERVICE_ID = ''Z0009'' AND A.GREENBOOK <> ''PDC'' AND A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' ' ")
                    
                    #Z0010 NPI
                    primaryQueryItems = SqlHelper.GetFirst(
                    ""
                    + str(Parameter1.QUERY_CRITERIA_1)
                    + "  A SET NPI_COEFFICIENT = CONVERT(VARCHAR,ENTITLEMENT_COEFFICIENT),NPI_CODE = ENTITLEMENT_DISPLAY_VALUE FROM SAQICO_INBOUND (NOLOCK) A JOIN PREGBV B(NOLOCK) ON A.TOOL_NPI = B.ENTITLEMENT_DISPLAY_VALUE AND A.GREENBOOK = B.GREENBOOK WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND ISNULL(TOOL_NPI,'''') <> '''' AND ENTITLEMENT_ID = ''AGS_Z0010_VAL_NPIREC'' AND A.SERVICE_ID IN( ''Z0010'') AND A.GREENBOOK <> ''PDC'' AND A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' ' ")
                    
                    #Z0128 NPI
                    primaryQueryItems = SqlHelper.GetFirst(
                    ""
                    + str(Parameter1.QUERY_CRITERIA_1)
                    + "  A SET NPI_COEFFICIENT = CONVERT(VARCHAR,ENTITLEMENT_COEFFICIENT),NPI_CODE = ENTITLEMENT_DISPLAY_VALUE FROM SAQICO_INBOUND (NOLOCK) A JOIN PREGBV B(NOLOCK) ON A.TOOL_NPI = B.ENTITLEMENT_DISPLAY_VALUE AND A.GREENBOOK = B.GREENBOOK WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND ISNULL(TOOL_NPI,'''') <> '''' AND ENTITLEMENT_ID = ''AGS_Z0128_VAL_NPIREC'' AND A.SERVICE_ID IN( ''Z0128'') AND A.GREENBOOK <> ''PDC'' AND A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' ' ")
                        
                    primaryQueryItems = SqlHelper.GetFirst(
                                            ""
                                            + str(Parameter1.QUERY_CRITERIA_1)
                                            + " A SET TOOL_SERVICE_COMPLEXITY = B.SERVICE_COMPLEXITY FROM SAQICO_INBOUND A(NOLOCK) JOIN (SELECT A.QUOTE_ID,A.SERVICE_ID,A.EQUIPMENT_ID,A.REVISION_ID AS QTEREV_ID,CASE WHEN A.SERVICE_COMPLEXITY = ''DIFFICULT'' THEN ''Difficult'' ELSE A.SERVICE_COMPLEXITY END AS SERVICE_COMPLEXITY FROM SAQICO_INBOUND (NOLOCK) A JOIN SAQICA (NOLOCK) B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.REVISION_ID = B.QTEREV_ID AND A.ASSEMBLY_ID = B.ASSEMBLY_ID WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND B.EQUIPMENTTYPE_ID=''MAINFRAME'' AND A.GREENBOOK IN (''CMP'') )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.REVISION_ID = B.QTEREV_ID  WHERE A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.REVISION_ID = ''"+str(Qt_Id.REVISION_ID)+"''  '")

                    primaryQueryItems = SqlHelper.GetFirst(
                                                                ""
                                                                + str(Parameter1.QUERY_CRITERIA_1)
                                                                + " A SET TOOL_SERVICE_COMPLEXITY = ''Difficult'' FROM SAQICO_INBOUND A(NOLOCK) JOIN (SELECT A.QUOTE_ID,A.SERVICE_ID,A.EQUIPMENT_ID,A.REVISION_ID AS QTEREV_ID,COUNT(*) AS SERVICE_COMPLEXITY FROM SAQICO_INBOUND (NOLOCK) A WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND A.SERVICE_COMPLEXITY = ''Difficult'' AND A.GREENBOOK NOT IN (''CMP'') GROUP BY A.QUOTE_ID,A.SERVICE_ID,A.EQUIPMENT_ID,A.REVISION_ID )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.REVISION_ID = B.QTEREV_ID WHERE B.SERVICE_COMPLEXITY >= 2 AND A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.REVISION_ID = ''"+str(Qt_Id.REVISION_ID)+"''  '")

                    primaryQueryItems = SqlHelper.GetFirst( ""+ str(Parameter1.QUERY_CRITERIA_1)+ " A SET TOOL_SERVICE_COMPLEXITY = CASE WHEN WA>=75 THEN ''Difficult'' WHEN WA>=25 AND WA<75 THEN ''MEDIUM'' WHEN WA<25 THEN ''EASY'' ELSE NULL END  FROM SAQICO_INBOUND A(NOLOCK) JOIN (SELECT QUOTE_ID,SERVICE_ID,EQUIPMENT_ID,QTEREV_ID,SCORE/SERVICE_COMPLEXITY AS WA FROM (SELECT A.QUOTE_ID,A.SERVICE_ID,A.EQUIPMENT_ID,A.REVISION_ID AS QTEREV_ID,COUNT(CASE WHEN ISNULL(SERVICE_COMPLEXITY,'''')='''' THEN NULL ELSE 1 END) AS SERVICE_COMPLEXITY,SUM(CASE WHEN ISNULL(SERVICE_COMPLEXITY,'''')=''DIFFICULT'' THEN 100 WHEN ISNULL(SERVICE_COMPLEXITY,'''')=''MEDIUM'' THEN 50 ELSE 0 END) AS SCORE FROM SAQICO_INBOUND (NOLOCK) A WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND A.GREENBOOK NOT IN (''CMP'') GROUP BY A.QUOTE_ID,A.SERVICE_ID,A.EQUIPMENT_ID,A.REVISION_ID)B WHERE EQUIPMENT_ID IN (SELECT DISTINCT EQUIPMENT_ID FROM (SELECT A.QUOTE_ID,A.SERVICE_ID,A.EQUIPMENT_ID,A.REVISION_ID AS QTEREV_ID,COUNT(CASE WHEN ISNULL(SERVICE_COMPLEXITY,'''')=''DIFFICULT'' THEN 1 ELSE NULL END) AS SERV_COMP  FROM SAQICO_INBOUND (NOLOCK) A  WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND ISNULL(TOOL_SERVICE_COMPLEXITY,'''')='''' AND A.GREENBOOK NOT IN (''CMP'') GROUP BY A.QUOTE_ID,A.SERVICE_ID,A.EQUIPMENT_ID,A.REVISION_ID ) A WHERE SERV_COMP<2) AND ISNULL(SERVICE_COMPLEXITY,0)>0 )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.REVISION_ID = B.QTEREV_ID  '")
                    
                    #Z0091 Service Complexity
                    primaryQueryItems = SqlHelper.GetFirst(
                                                                    ""
                                                                    + str(Parameter1.QUERY_CRITERIA_1)
                                                                    + "  A SET SERVICECOMPLEXITY_COEFFICIENT = CONVERT(VARCHAR,ENTITLEMENT_COEFFICIENT),SERVICE_COMPLEXITY_CODE = ENTITLEMENT_VALUE_CODE FROM SAQICO_INBOUND (NOLOCK) A JOIN PREGBV B(NOLOCK) ON A.TOOL_SERVICE_COMPLEXITY = B.ENTITLEMENT_DISPLAY_VALUE AND A.GREENBOOK = B.GREENBOOK WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND ISNULL(TOOL_SERVICE_COMPLEXITY,'''') <> '''' AND ENTITLEMENT_ID = ''AGS_Z0091_VAL_SVCCOM'' AND A.SERVICE_ID = ''Z0091'' ' ")
                    
                    #Z0092  Service Complexity              
                    primaryQueryItems = SqlHelper.GetFirst(
                                        ""
                                        + str(Parameter1.QUERY_CRITERIA_1)
                                        + "  A SET SERVICECOMPLEXITY_COEFFICIENT = CONVERT(VARCHAR,ENTITLEMENT_COEFFICIENT),SERVICE_COMPLEXITY_CODE = ENTITLEMENT_VALUE_CODE FROM SAQICO_INBOUND (NOLOCK) A JOIN PREGBV B(NOLOCK) ON A.TOOL_SERVICE_COMPLEXITY = B.ENTITLEMENT_DISPLAY_VALUE AND A.GREENBOOK = B.GREENBOOK WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND ISNULL(TOOL_SERVICE_COMPLEXITY,'''') <> '''' AND ENTITLEMENT_ID = ''AGS_Z0092_VAL_SVCCOM'' AND A.SERVICE_ID = ''Z0092'' ' ")
                    
                    #Z0004  Service Complexity              
                    primaryQueryItems = SqlHelper.GetFirst(
                                        ""
                                        + str(Parameter1.QUERY_CRITERIA_1)
                                        + "  A SET SERVICECOMPLEXITY_COEFFICIENT = CONVERT(VARCHAR,ENTITLEMENT_COEFFICIENT),SERVICE_COMPLEXITY_CODE = ENTITLEMENT_VALUE_CODE FROM SAQICO_INBOUND (NOLOCK) A JOIN PREGBV B(NOLOCK) ON A.TOOL_SERVICE_COMPLEXITY = B.ENTITLEMENT_DISPLAY_VALUE AND A.GREENBOOK = B.GREENBOOK WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND ISNULL(TOOL_SERVICE_COMPLEXITY,'''') <> '''' AND ENTITLEMENT_ID = ''AGS_Z0004_VAL_SVCCOM'' AND A.SERVICE_ID = ''Z0004'' ' ")
                    
                    #Z0099 Service Complexity                   
                    primaryQueryItems = SqlHelper.GetFirst(
                                        ""
                                        + str(Parameter1.QUERY_CRITERIA_1)
                                        + "  A SET SERVICECOMPLEXITY_COEFFICIENT = CONVERT(VARCHAR,ENTITLEMENT_COEFFICIENT),SERVICE_COMPLEXITY_CODE = ENTITLEMENT_VALUE_CODE FROM SAQICO_INBOUND (NOLOCK) A JOIN PREGBV B(NOLOCK) ON A.TOOL_SERVICE_COMPLEXITY = B.ENTITLEMENT_DISPLAY_VALUE AND A.GREENBOOK = B.GREENBOOK WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND ISNULL(TOOL_SERVICE_COMPLEXITY,'''') <> '''' AND ENTITLEMENT_ID = ''AGS_Z0099_VAL_SVCCOM'' AND A.SERVICE_ID = ''Z0099'' ' ")
                    
                    #Z0035 Service Complexity                   
                    primaryQueryItems = SqlHelper.GetFirst(
                                        ""
                                        + str(Parameter1.QUERY_CRITERIA_1)
                                        + "  A SET SERVICECOMPLEXITY_COEFFICIENT = CONVERT(VARCHAR,ENTITLEMENT_COEFFICIENT),SERVICE_COMPLEXITY_CODE = ENTITLEMENT_VALUE_CODE FROM SAQICO_INBOUND (NOLOCK) A JOIN PREGBV B(NOLOCK) ON A.TOOL_SERVICE_COMPLEXITY = B.ENTITLEMENT_DISPLAY_VALUE AND A.GREENBOOK = B.GREENBOOK WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND ISNULL(TOOL_SERVICE_COMPLEXITY,'''') <> '''' AND ENTITLEMENT_ID = ''AGS_Z0035_VAL_SVCCOM'' AND A.SERVICE_ID = ''Z0035'' ' ")
                    
                    #Z0009  Service Complexity              
                    primaryQueryItems = SqlHelper.GetFirst(
                                        ""
                                        + str(Parameter1.QUERY_CRITERIA_1)
                                        + "  A SET SERVICECOMPLEXITY_COEFFICIENT = CONVERT(VARCHAR,ENTITLEMENT_COEFFICIENT),SERVICE_COMPLEXITY_CODE = ENTITLEMENT_VALUE_CODE FROM SAQICO_INBOUND (NOLOCK) A JOIN PREGBV B(NOLOCK) ON A.TOOL_SERVICE_COMPLEXITY = B.ENTITLEMENT_DISPLAY_VALUE AND A.GREENBOOK = B.GREENBOOK WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND ISNULL(TOOL_SERVICE_COMPLEXITY,'''') <> '''' AND ENTITLEMENT_ID = ''AGS_Z0009_VAL_SVCCOM'' AND A.SERVICE_ID = ''Z0009'' ' ")
                    
                    #LTCOSS - Total Cost without Seedstock Coefficient
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                        + str(Parameter1.QUERY_CRITERIA_1)
                        + "  A SET LTCOSS = LOG(TCWOSS) * OSSVDV FROM SAQICO A(NOLOCK) JOIN (SELECT  DISTINCT QUOTE_ID,SERVICE_ID,REVISION_ID,LINE,EQUIPMENT_ID,CONTRACT_YEAR  FROM SAQICO_INBOUND B(NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID  AND A.QTEREV_ID = B.REVISION_ID AND A.LINE = B.LINE AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.CNTYER = B.CONTRACT_YEAR WHERE ISNULL(TCWOSS,0)>0 AND ISNULL(GRNBOK,'''')+''-''+ISNULL(EQUIPMENTCATEGORY_ID,'''') NOT IN(''PDC-S'',''PDC-C'') AND A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"''  ' ")
                    
                    #CAVVDC - Capital Avoidance Coefficient
                    primaryQueryItems = SqlHelper.GetFirst(
                                                ""
                                                + str(Parameter1.QUERY_CRITERIA_1)
                                                + "  A SET CAVVDC = (B.SEEDSTOCK_COST / B.TOTAL_COST_WISEEDSTOCK) * ISNULL(CONVERT(FLOAT,CAVVDV),0) FROM SAQICO (NOLOCK) A JOIN (SELECT DISTINCT QUOTE_ID,REVISION_ID,SERVICE_ID,SUM(CONVERT(FLOAT,SEEDSTOCK_COST)) AS SEEDSTOCK_COST,SUM(CONVERT(FLOAT,TOTAL_COST_WISEEDSTOCK)) AS TOTAL_COST_WISEEDSTOCK,LINE,EQUIPMENT_ID,CONTRACT_YEAR FROM SAQICO_INBOUND(NOLOCK)B  WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' GROUP BY QUOTE_ID,REVISION_ID,SERVICE_ID,LINE,EQUIPMENT_ID,CONTRACT_YEAR)B ON A.QUOTE_ID = B.QUOTE_ID AND A.QTEREV_ID = B.REVISION_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.LINE = B.LINE AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.CNTYER = B.CONTRACT_YEAR JOIN PRENTL D(NOLOCK) ON A.SERVICE_ID = D.SERVICE_ID WHERE ISNULL(B.TOTAL_COST_WISEEDSTOCK,0)>0 AND A.GRNBOK<> ''PDC'' AND ENTITLEMENT_NAME=''Capital Avoidance'' AND ISNULL(CAVVDV,'''')<>'''' AND A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' ' ")
                    
                    #SCMVDV - Service Complexity Value Driver
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                        + str(Parameter1.QUERY_CRITERIA_1)
                        + "  A SET SCMVDV = TOOL_SERVICE_COMPLEXITY FROM SAQICO A(NOLOCK) JOIN (SELECT  DISTINCT QUOTE_ID,SERVICE_ID,REVISION_ID,LINE,TOOL_SERVICE_COMPLEXITY,EQUIPMENT_ID,CONTRACT_YEAR FROM SAQICO_INBOUND B(NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.QTEREV_ID = B.REVISION_ID AND A.LINE = B.LINE AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.CNTYER = B.CONTRACT_YEAR WHERE A.SERVICE_ID NOT IN (''Z0010'',''Z0128'') AND A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' ' ")
                        
                    #SCMVDC - Service Complexity Coefficient
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                        + str(Parameter1.QUERY_CRITERIA_1)
                        + "  A SET SCMVDC = SERVICECOMPLEXITY_COEFFICIENT FROM SAQICO A(NOLOCK) JOIN (SELECT  DISTINCT QUOTE_ID,SERVICE_ID,REVISION_ID,LINE,SERVICECOMPLEXITY_COEFFICIENT,EQUIPMENT_ID,CONTRACT_YEAR FROM SAQICO_INBOUND B(NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.QTEREV_ID = B.REVISION_ID AND A.LINE = B.LINE AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.CNTYER = B.CONTRACT_YEAR WHERE A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' ' ")
                    
                    #NPIVDV - NPI Tool Value Driver
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                        + str(Parameter1.QUERY_CRITERIA_1)
                        + "  A SET NPIVDV = NPI_CODE FROM SAQICO A(NOLOCK) JOIN (SELECT  DISTINCT QUOTE_ID,SERVICE_ID,REVISION_ID,LINE,NPI_CODE,EQUIPMENT_ID,CONTRACT_YEAR  FROM SAQICO_INBOUND B(NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID  AND A.QTEREV_ID = B.REVISION_ID AND A.LINE = B.LINE AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.CNTYER = B.CONTRACT_YEAR WHERE A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' ' ")
                        
                    #NPIVDC - NPI Tool Coefficient
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                        + str(Parameter1.QUERY_CRITERIA_1)
                        + "  A SET NPIVDC = NPI_COEFFICIENT FROM SAQICO A(NOLOCK) JOIN (SELECT  DISTINCT QUOTE_ID,SERVICE_ID,REVISION_ID,LINE,NPI_COEFFICIENT,EQUIPMENT_ID,CONTRACT_YEAR  FROM SAQICO_INBOUND B(NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.QTEREV_ID = B.REVISION_ID AND A.LINE = B.LINE AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.CNTYER = B.CONTRACT_YEAR WHERE A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' ' ")
                    
                    #PBPVDC - PDC Coefficent
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                        + str(Parameter1.QUERY_CRITERIA_1)
                        + "  A SET PBPVDC = LOG(PDCBPR) * PBPVDV FROM SAQICO A(NOLOCK) JOIN (SELECT  DISTINCT QUOTE_ID,SERVICE_ID,REVISION_ID,LINE,NPI_COEFFICIENT,EQUIPMENT_ID,CONTRACT_YEAR  FROM SAQICO_INBOUND B(NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.QTEREV_ID = B.REVISION_ID AND A.LINE = B.LINE AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.CNTYER = B.CONTRACT_YEAR WHERE GRNBOK = ''PDC'' AND EQUIPMENTCATEGORY_ID IN (''S'',''C'') AND A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' ' ")
                        
                    #AISSPC - Annualized Item Seedstock Percent
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                        + str(Parameter1.QUERY_CRITERIA_1)
                        + "  A SET AISSPC = SDSTKC / TCWISS FROM SAQICO A(NOLOCK) JOIN (SELECT  DISTINCT QUOTE_ID,SERVICE_ID,REVISION_ID,LINE,EQUIPMENT_ID,CONTRACT_YEAR FROM SAQICO_INBOUND B(NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.QTEREV_ID = B.REVISION_ID AND A.LINE = B.LINE AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.CNTYER = B.CONTRACT_YEAR WHERE ISNULL(TCWISS,0)>0 AND A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' ' ")
                    
                    #RKFVDV/RKFVDC - Risk Factor Value Driver / Coefficent
                    primaryQueryItems = SqlHelper.GetFirst(
                                                ""
                                                + str(Parameter1.QUERY_CRITERIA_1)
                                                + "  A SET RKFVDV = CASE WHEN CNTYEARITEM <=1 THEN ''FIRST - 1 YEAR CONTRACT'' WHEN CNTYEARITEM =2 THEN ''FIRST - 2 YEAR CONTRACT'' ELSE ''NO RISK'' END, RKFVDC = CASE WHEN CNTYEARITEM <=1 THEN (SDSTKC / TCWISS) WHEN CNTYEARITEM =2 THEN (SDSTKC / TCWISS)/2 ELSE 0 END FROM SAQICO (NOLOCK) A JOIN (SELECT DISTINCT QUOTE_ID,REVISION_ID,SERVICE_ID,LINE,EQUIPMENT_ID,CONTRACT_YEAR FROM SAQICO_INBOUND(NOLOCK)B  WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' )B ON A.QUOTE_ID = B.QUOTE_ID AND A.QTEREV_ID = B.REVISION_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.LINE = B.LINE AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.CNTYER = B.CONTRACT_YEAR JOIN SAQTRV (NOLOCK) ON A.QUOTE_ID = SAQTRV.QUOTE_ID AND A.QTEREV_ID = SAQTRV.QTEREV_ID JOIN (SELECT DISTINCT QUOTE_ID,QTEREV_ID,LINE,datediff(yy,CONTRACT_VALID_FROM,dateadd(dd,1,CONTRACT_VALID_TO)) AS CNTYEARITEM FROM SAQRIT (NOLOCK) WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' )C ON A.QUOTE_ID = C.QUOTE_ID AND A.QTEREV_ID = C.QTEREV_ID AND A.LINE = C.LINE WHERE A.SERVICE_ID IN (''Z0009'',''Z0010'',''Z0128'') AND A.SWPKTA = ''INCLUDED'' AND ISNULL(TCWISS,0)>0 AND CASE WHEN ISNULL(QTTXTP,'''')='''' THEN SAQTRV.TRANSACTION_TYPE ELSE QTTXTP END =''O-QUOTE''  ' ")
                        
                    #SUMCOF - Sum of All Coefficient
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                        + str(Parameter1.QUERY_CRITERIA_1)
                        + "  A SET SUMCOF = ISNULL(INTCPC,0) + ISNULL(LTCOSS,0) + ISNULL(POFVDC,0) + ISNULL(GBKVDC,0) + ISNULL(UIMVDC,0) + ISNULL(CAVVDC,0) + ISNULL(WNDVDC,0) + ISNULL(SCMVDC,0) + ISNULL(CCDFFC,0) + ISNULL(NPIVDC,0) + ISNULL(DTPVDC,0) + ISNULL(CSTVDC,0) + ISNULL(CSGVDC,0) + ISNULL(QRQVDC,0) + ISNULL(SVCVDC,0) + ISNULL(PBPVDC,0) + ISNULL(ADDCOF,0) + ISNULL(ITTNBC,0) FROM SAQICO A(NOLOCK) JOIN (SELECT  DISTINCT QUOTE_ID,SERVICE_ID,REVISION_ID,LINE,EQUIPMENT_ID,CONTRACT_YEAR  FROM SAQICO_INBOUND B(NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.QTEREV_ID = B.REVISION_ID AND A.LINE = B.LINE AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.CNTYER = B.CONTRACT_YEAR WHERE A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' ' ")
                    
                    #INMP01 - Intermediate Model Price 1
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                        + str(Parameter1.QUERY_CRITERIA_1)
                        + "  A SET INMP01 = EXP(SUMCOF) FROM SAQICO A(NOLOCK) JOIN (SELECT  DISTINCT QUOTE_ID,SERVICE_ID,REVISION_ID,LINE,EQUIPMENT_ID,CONTRACT_YEAR  FROM SAQICO_INBOUND B(NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.QTEREV_ID = B.REVISION_ID AND A.LINE = B.LINE AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.CNTYER = B.CONTRACT_YEAR WHERE (ISNULL(LTCOSS,0)>0 OR ISNULL(PBPVDC,0)>0) AND A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' ' ")
                        
                    #INMP02 / FNMDPR - Intermediate Model Price 2 /  Final Model Price
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                        + str(Parameter1.QUERY_CRITERIA_1)
                        + "  A SET INMP02 = INMP01 * (1 + ISNULL(CCRTMC,0)), FNMDPR = INMP01 * (1 + ISNULL(CCRTMC,0)) FROM SAQICO A(NOLOCK) JOIN (SELECT  DISTINCT QUOTE_ID,SERVICE_ID,REVISION_ID,LINE,EQUIPMENT_ID,CONTRACT_YEAR FROM SAQICO_INBOUND B(NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID  AND A.QTEREV_ID = B.REVISION_ID AND A.LINE = B.LINE AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.CNTYER = B.CONTRACT_YEAR WHERE A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' ' ")
                    
                    #FNMDPR - Final Model Price (Z0100 / Z0101)
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                        + str(Parameter1.QUERY_CRITERIA_1)
                        + "  A SET CNSM_MARGIN_PERCENT = D.CNSM_MARGIN_PERCENT FROM SAQICO_INBOUND(NOLOCK)A JOIN SABGMR D(NOLOCK) ON A.GREENBOOK = D.GREENBOOK AND A.BLUEBOOK = D.BLUEBOOK WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  ' ")
                    
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                        + str(Parameter1.QUERY_CRITERIA_1)
                        + "  A SET CNSM_MARGIN_PERCENT = D.CNSM_MARGIN_PERCENT FROM SAQICO_INBOUND(NOLOCK)A JOIN SABGMR D(NOLOCK) ON A.GREENBOOK = D.GREENBOOK AND A.REGION = D.REGION WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND A.CNSM_MARGIN_PERCENT IS NULL ' ")
                    
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                        + str(Parameter1.QUERY_CRITERIA_1)
                        + "  A SET FNMDPR =  TCWISS / (1 - (B.CNSM_MARGIN_PERCENT/100)), MTGPRC =  TCWISS / (1 - (B.CNSM_MARGIN_PERCENT/100)), MSLPRC =  TCWISS / (1 - (B.CNSM_MARGIN_PERCENT/100)), MBDPRC =  TCWISS / (1 - (B.CNSM_MARGIN_PERCENT/100)), MCLPRC =  TCWISS / (1 - (B.CNSM_MARGIN_PERCENT/100)) ,CNTCST = TCWISS, CNTPRC = TCWISS / (1 - (B.CNSM_MARGIN_PERCENT/100))  FROM SAQICO (NOLOCK)A JOIN (SELECT DISTINCT QUOTE_ID,SERVICE_ID,REVISION_ID,LINE,CNSM_MARGIN_PERCENT,EQUIPMENT_ID,CONTRACT_YEAR FROM SAQICO_INBOUND(NOLOCK)  WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' )B ON A.QUOTE_ID = B.QUOTE_ID AND A.LINE = B.LINE  AND QTEREV_ID = REVISION_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.CNTYER = B.CONTRACT_YEAR WHERE ISNULL(TCWISS,0)>0 AND A.SERVICE_ID IN (''Z0100'',''Z0101'') AND A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' ' ")
                    
                    #MTGPRC - Target Model Price
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                        + str(Parameter1.QUERY_CRITERIA_1)
                        + "  A SET MTGPRC = ( CASE WHEN ISNULL(FNMDPR/(1-(CONVERT(FLOAT,SADSPC)/100)),0) > ISNULL(TCWISS / (1-(TAPMMP/100)),0) THEN ISNULL(FNMDPR/(1-(CONVERT(FLOAT,SADSPC)/100)),0) ELSE ISNULL(TCWISS / (1-(TAPMMP/100)),0) END )  * (1 + ISNULL(RKFVDC,0)) FROM SAQICO A(NOLOCK) JOIN (SELECT  DISTINCT QUOTE_ID,SERVICE_ID,REVISION_ID,LINE,EQUIPMENT_ID,CONTRACT_YEAR  FROM SAQICO_INBOUND B(NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID  AND A.QTEREV_ID = B.REVISION_ID AND A.LINE = B.LINE AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.CNTYER = B.CONTRACT_YEAR WHERE A.SERVICE_ID NOT IN (''Z0100'',''Z0101'') AND A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' ' ")
                    
                    #MSLPRC - Sales Model Price
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                        + str(Parameter1.QUERY_CRITERIA_1)
                        + "  A SET MSLPRC = ( CASE WHEN ISNULL(FNMDPR,0) > ISNULL(TCWISS / (1-(CONVERT(FLOAT,SAPMMP)/100)),0) THEN ISNULL(FNMDPR,0) ELSE ISNULL(TCWISS / (1-(CONVERT(FLOAT,SAPMMP)/100)),0) END ) * (1 + ISNULL(RKFVDC,0))  FROM SAQICO A(NOLOCK) JOIN (SELECT  DISTINCT QUOTE_ID,SERVICE_ID,REVISION_ID,LINE,EQUIPMENT_ID,CONTRACT_YEAR FROM SAQICO_INBOUND B(NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.QTEREV_ID = B.REVISION_ID AND A.LINE = B.LINE AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.CNTYER = B.CONTRACT_YEAR WHERE A.SERVICE_ID NOT IN (''Z0100'',''Z0101'') AND A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' ' ")
                    
                    #MBDPRC - BD Model Price
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                        + str(Parameter1.QUERY_CRITERIA_1)
                        + "  A SET MBDPRC = ( CASE WHEN ISNULL(FNMDPR * (1-(CONVERT(FLOAT,BDDSPC)/100)) ,0) > ISNULL(TCWISS / (1-(CONVERT(FLOAT,BDPMMP)/100)),0) THEN ISNULL(FNMDPR * (1-(CONVERT(FLOAT,BDDSPC)/100)) ,0) ELSE ISNULL(TCWISS / (1-(CONVERT(FLOAT,BDPMMP)/100)),0) END )  * (1 + ISNULL(RKFVDC,0)) FROM SAQICO A(NOLOCK) JOIN (SELECT  DISTINCT QUOTE_ID,SERVICE_ID,REVISION_ID,LINE,EQUIPMENT_ID,CONTRACT_YEAR FROM SAQICO_INBOUND B(NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.QTEREV_ID = B.REVISION_ID AND A.LINE = B.LINE AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.CNTYER = B.CONTRACT_YEAR WHERE A.SERVICE_ID NOT IN (''Z0100'',''Z0101'') AND A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' ' ")
                    
                    #MCLPRC - Ceiling Model Price
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                        + str(Parameter1.QUERY_CRITERIA_1)
                        + "  A SET MCLPRC = MTGPRC * (1 + ISNULL(CEPRUP/100,0)) FROM SAQICO A(NOLOCK) JOIN (SELECT  DISTINCT QUOTE_ID,SERVICE_ID,REVISION_ID,LINE,EQUIPMENT_ID,CONTRACT_YEAR FROM SAQICO_INBOUND B(NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.QTEREV_ID = B.REVISION_ID AND A.LINE = B.LINE AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.CNTYER = B.CONTRACT_YEAR WHERE A.SERVICE_ID NOT IN (''Z0100'',''Z0101'') AND A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' ' ")
                    
                    #TOTLCI - Total Cost Impact
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                        + str(Parameter1.QUERY_CRITERIA_1)
                        + "  A SET TOTLCI = ISNULL(CAVVCI,0) + ISNULL(UIMVCI,0) + ISNULL(ATGKEC,0) + ISNULL(AMNCCI,0) + (ISNULL(TNHRPT,1) * ISNULL(HEDBIC,0)) + ISNULL(NWPTOC,0) + ISNULL(NUMLCI,0) + ( ISNULL(TNHRPT,1) * ISNULL(SPCCLC,0)) + ( ISNULL(TNHRPT,1) * ISNULL(SPCCCI,0) ) FROM SAQICO A(NOLOCK) JOIN (SELECT  DISTINCT QUOTE_ID,SERVICE_ID,REVISION_ID,LINE,EQUIPMENT_ID,CONTRACT_YEAR FROM SAQICO_INBOUND B(NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.QTEREV_ID = B.REVISION_ID AND A.LINE = B.LINE  AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.CNTYER = B.CONTRACT_YEAR WHERE A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' ' ")
                    
                    #TOTLPI - Total Price Impact
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                        + str(Parameter1.QUERY_CRITERIA_1)
                        + "  A SET TOTLPI = ISNULL(ATGKEP,0) + ISNULL(AMNPPI,0) + ISNULL(CAVVPI,0) + ( ISNULL(TNHRPT,1) * ISNULL(HEDBIP,0)) + ISNULL(NWPTOP,0) + ISNULL(NUMLPI,0) + (ISNULL(TNHRPT,1) * ISNULL(SPCCLP,0)) + (ISNULL(TNHRPT,1) * ISNULL(SPCCPI,0)) + ISNULL(UIMVPI,0) FROM SAQICO A(NOLOCK) JOIN (SELECT  DISTINCT QUOTE_ID,SERVICE_ID,REVISION_ID,LINE,EQUIPMENT_ID,CONTRACT_YEAR FROM SAQICO_INBOUND B(NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.QTEREV_ID = B.REVISION_ID AND A.LINE = B.LINE AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.CNTYER = B.CONTRACT_YEAR WHERE A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' ' ")
                    
                    #FCWOSS - Final Total Cost without Seedstock
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                        + str(Parameter1.QUERY_CRITERIA_1)
                        + "  A SET FCWOSS = ISNULL(TCWOSS,0) + ISNULL(TOTLCI,0) FROM SAQICO A(NOLOCK) JOIN (SELECT  DISTINCT QUOTE_ID,SERVICE_ID,REVISION_ID,LINE,EQUIPMENT_ID,CONTRACT_YEAR FROM SAQICO_INBOUND B(NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.QTEREV_ID = B.REVISION_ID AND A.LINE = B.LINE AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.CNTYER = B.CONTRACT_YEAR WHERE A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"''' ")
                    
                    #FCWISS - Final Total Cost with Seedstock
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                        + str(Parameter1.QUERY_CRITERIA_1)
                        + "  A SET FCWISS = ISNULL(TCWISS,0) + ISNULL(TOTLCI,0), SBTCST = ISNULL(TCWISS,0) FROM SAQICO A(NOLOCK) JOIN (SELECT  DISTINCT QUOTE_ID,SERVICE_ID,REVISION_ID,LINE,EQUIPMENT_ID,CONTRACT_YEAR FROM SAQICO_INBOUND B(NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.QTEREV_ID = B.REVISION_ID AND A.LINE = B.LINE AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.CNTYER = B.CONTRACT_YEAR WHERE A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' ' ")
                    
                    #AIFCPE - Final Total Cost Per Event
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                        + str(Parameter1.QUERY_CRITERIA_1)
                        + "  A SET AIFCPE = FCWISS / ISNULL(ADJ_PM_FREQUENCY,0) FROM SAQICO A(NOLOCK) JOIN (SELECT  DISTINCT QUOTE_ID,SERVICE_ID,REVISION_ID,LINE,EQUIPMENT_ID,CONTRACT_YEAR FROM SAQICO_INBOUND B(NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.QTEREV_ID = B.REVISION_ID AND A.LINE = B.LINE AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.CNTYER = B.CONTRACT_YEAR WHERE ISNULL(A.ADJ_PM_FREQUENCY,0)>0 AND A.QTETYP <> ''TOOL BASED'' AND A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' ' ")
                    
                    #TRGPRC /SLSPRC / BDVPRC /CELPRC - Target / Sales / BD / Ceiling Price
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                        + str(Parameter1.QUERY_CRITERIA_1)
                        + "  A SET TRGPRC = ISNULL(MTGPRC,0) + ISNULL(TOTLPI,0), SLSPRC = ISNULL(MSLPRC,0) + ISNULL(TOTLPI,0), BDVPRC = ISNULL(MBDPRC,0) + ISNULL(TOTLPI,0), CELPRC = ISNULL(MCLPRC,0) + ISNULL(TOTLPI,0),FINPRC = ISNULL(MTGPRC,0) + ISNULL(TOTLPI,0)   FROM SAQICO A(NOLOCK) JOIN (SELECT  DISTINCT QUOTE_ID,SERVICE_ID,REVISION_ID,LINE,EQUIPMENT_ID,CONTRACT_YEAR FROM SAQICO_INBOUND B(NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.QTEREV_ID = B.REVISION_ID AND A.LINE = B.LINE AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.CNTYER = B.CONTRACT_YEAR WHERE A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' ' ")
                        
                    #SBTPRC - Sub Total Price
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                        + str(Parameter1.QUERY_CRITERIA_1)
                        + "  A SET  SBTPRC = ISNULL(MTGPRC,0) FROM SAQICO A(NOLOCK) JOIN (SELECT  DISTINCT QUOTE_ID,SERVICE_ID,REVISION_ID,LINE,EQUIPMENT_ID,CONTRACT_YEAR FROM SAQICO_INBOUND B(NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.QTEREV_ID = B.REVISION_ID AND A.LINE = B.LINE AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.CNTYER = B.CONTRACT_YEAR WHERE A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' ' ")
                    
                    #USRPRC / TGADJP - User Price / Target User Price Adjustment
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                        + str(Parameter1.QUERY_CRITERIA_1)
                        + "  A SET USRPRC = TRGPRC,TGADJP = ''0.00'' FROM SAQICO A(NOLOCK) JOIN (SELECT  DISTINCT QUOTE_ID,SERVICE_ID,REVISION_ID,LINE,EQUIPMENT_ID,CONTRACT_YEAR FROM SAQICO_INBOUND B(NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.QTEREV_ID = B.REVISION_ID AND A.LINE = B.LINE AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.CNTYER = B.CONTRACT_YEAR WHERE A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' ' ")
                    
                    #AIUPPE - User Price Per Event Kit
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                        + str(Parameter1.QUERY_CRITERIA_1)
                        + "  A SET AIUPPE = TRGPRC / ADJ_PM_FREQUENCY FROM SAQICO A(NOLOCK) JOIN (SELECT  DISTINCT QUOTE_ID,SERVICE_ID,REVISION_ID,LINE,EQUIPMENT_ID,CONTRACT_YEAR FROM SAQICO_INBOUND B(NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.QTEREV_ID = B.REVISION_ID AND A.LINE = B.LINE AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.CNTYER = B.CONTRACT_YEAR WHERE A.QTETYP <> ''TOOL BASED'' AND ISNULL(ADJ_PM_FREQUENCY,0)>0 AND A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' ' ")
                    
                    #CNTPRC - Contractual Price
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                        + str(Parameter1.QUERY_CRITERIA_1)
                        + "  A SET CNTPRC = ((USRPRC / 365) * CNTDAY * ISNULL(CTPDFP ,1) ) * (1 - (ISNULL(YOYPCT,0)/100))  FROM SAQICO A(NOLOCK) JOIN (SELECT  DISTINCT QUOTE_ID,SERVICE_ID,REVISION_ID,LINE,EQUIPMENT_ID,CONTRACT_YEAR FROM SAQICO_INBOUND B(NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID  AND A.QTEREV_ID = B.REVISION_ID AND A.LINE = B.LINE AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.CNTYER = B.CONTRACT_YEAR WHERE A.SERVICE_ID NOT IN (''Z0100'',''Z0101'') AND A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' ' ")
                    
                    #CNTCST - Contractual Cost
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                        + str(Parameter1.QUERY_CRITERIA_1)
                        + "  A SET CNTCST = ((FCWISS / 365) * CNTDAY )  FROM SAQICO A(NOLOCK) JOIN (SELECT  DISTINCT QUOTE_ID,SERVICE_ID,REVISION_ID,LINE,EQUIPMENT_ID,CONTRACT_YEAR  FROM SAQICO_INBOUND B(NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.QTEREV_ID = B.REVISION_ID AND A.LINE = B.LINE AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.CNTYER = B.CONTRACT_YEAR WHERE A.SERVICE_ID NOT IN (''Z0100'',''Z0101'') AND A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' ' ")
                    
                    #AICPPE / AICCPE - Contract Cost / Price Per Event Kit
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                        + str(Parameter1.QUERY_CRITERIA_1)
                        + "  A SET AICPPE = CNTPRC / ADJ_PM_FREQUENCY, AICCPE = CNTCST / ADJ_PM_FREQUENCY FROM SAQICO A(NOLOCK) JOIN (SELECT  DISTINCT QUOTE_ID,SERVICE_ID,REVISION_ID,LINE,EQUIPMENT_ID,CONTRACT_YEAR FROM SAQICO_INBOUND B(NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.QTEREV_ID = B.REVISION_ID AND A.LINE = B.LINE AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.CNTYER = B.CONTRACT_YEAR WHERE A.QTETYP <> ''TOOL BASED'' AND ISNULL(ADJ_PM_FREQUENCY,0)>0 AND A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' ' ")
                    
                    #CNTMGN - Contractual Margin
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                        + str(Parameter1.QUERY_CRITERIA_1)
                        + "  A SET CNTMGN = CNTPRC - CNTCST FROM SAQICO A(NOLOCK) JOIN (SELECT  DISTINCT QUOTE_ID,SERVICE_ID,REVISION_ID,LINE,EQUIPMENT_ID,CONTRACT_YEAR FROM SAQICO_INBOUND B(NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.QTEREV_ID = B.REVISION_ID AND A.LINE = B.LINE AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.CNTYER = B.CONTRACT_YEAR WHERE A.SERVICE_ID NOT IN (''Z0100'',''Z0101'') AND A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' ' ")
                    
                    #SPCTPR /SPCTCS - Spares Contractual Price / Cost
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                        + str(Parameter1.QUERY_CRITERIA_1)
                        + "  A SET SPCTPR = CNTPRC * SPSPCT, SPCTCS = CNTCST * SPSPCT FROM SAQICO A(NOLOCK) JOIN (SELECT  DISTINCT QUOTE_ID,SERVICE_ID,REVISION_ID,LINE,EQUIPMENT_ID,CONTRACT_YEAR FROM SAQICO_INBOUND B(NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.QTEREV_ID = B.REVISION_ID AND A.LINE = B.LINE AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.CNTYER = B.CONTRACT_YEAR  WHERE A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' ' ")
                        
                    #SPCTMG - Spares Contractual Margin
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                        + str(Parameter1.QUERY_CRITERIA_1)
                        + "  A SET SPCTMG = (SPCTPR - SPCTCS) / SPCTPR FROM SAQICO A(NOLOCK) JOIN (SELECT  DISTINCT QUOTE_ID,SERVICE_ID,REVISION_ID,LINE,EQUIPMENT_ID,CONTRACT_YEAR FROM SAQICO_INBOUND B(NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.QTEREV_ID = B.REVISION_ID AND A.LINE = B.LINE AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.CNTYER = B.CONTRACT_YEAR AND ISNULL(SPCTPR,0)>0 WHERE A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' ' ")
                    
                    #SVCTPR /SVCTCS - Service Contractual Price / Cost
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                        + str(Parameter1.QUERY_CRITERIA_1)
                        + "  A SET SVCTPR = CNTPRC * SVSPCT, SVCTCS = CNTCST * SVSPCT FROM SAQICO A(NOLOCK) JOIN (SELECT  DISTINCT QUOTE_ID,SERVICE_ID,REVISION_ID,LINE,EQUIPMENT_ID,CONTRACT_YEAR FROM SAQICO_INBOUND B(NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID  AND A.QTEREV_ID = B.REVISION_ID AND A.LINE = B.LINE AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.CNTYER = B.CONTRACT_YEAR WHERE A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' ' ")
                    
                    #SVCTMG - Service Contractual Margin
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                        + str(Parameter1.QUERY_CRITERIA_1)
                        + "  A SET SVCTMG = (SVCTPR - SVCTCS) / SVCTPR FROM SAQICO A(NOLOCK) JOIN (SELECT  DISTINCT QUOTE_ID,SERVICE_ID,REVISION_ID,LINE,EQUIPMENT_ID,CONTRACT_YEAR FROM SAQICO_INBOUND B(NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.QTEREV_ID = B.REVISION_ID AND A.LINE = B.LINE AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.CNTYER = B.CONTRACT_YEAR AND ISNULL(SVCTPR,0)>0 WHERE A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' ' ")
                    
                    #TNTVGC / TNTMGC / TNTMPC - Total Net Value / Total Net Value in Margin / Margin % (Global Currency) 
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                        + str(Parameter1.QUERY_CRITERIA_1)
                        + "  A SET TNTVGC = CNTPRC , TNTMGC = CNTPRC - CNTCST, TNTMPC = (CNTPRC - CNTCST) / CNTPRC FROM SAQICO A(NOLOCK) JOIN (SELECT  DISTINCT QUOTE_ID,SERVICE_ID,REVISION_ID,LINE,EQUIPMENT_ID,CONTRACT_YEAR FROM SAQICO_INBOUND B(NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.QTEREV_ID = B.REVISION_ID AND A.LINE = B.LINE AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.CNTYER = B.CONTRACT_YEAR WHERE A.BILTYP <> ''VARIABLE'' AND ISNULL(CNTPRC,0)>0 AND A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' ' ")
                    
                    #TENVGC - Estimated Value (Global Currency)
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                        + str(Parameter1.QUERY_CRITERIA_1)
                        + "  A SET TENVGC = CNTPRC , TNTMGC = CNTPRC - CNTCST FROM SAQICO A(NOLOCK) JOIN (SELECT  DISTINCT QUOTE_ID,SERVICE_ID,REVISION_ID,LINE,EQUIPMENT_ID,CONTRACT_YEAR FROM SAQICO_INBOUND B(NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID  AND A.QTEREV_ID = B.REVISION_ID AND A.LINE = B.LINE AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.CNTYER = B.CONTRACT_YEAR WHERE A.BILTYP = ''VARIABLE'' AND A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' ' ")
                        
                    #TAXVGC - Tax Amount (Global Currency) 
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                        + str(Parameter1.QUERY_CRITERIA_1)
                        + "  A SET TAXVGC = TNTVGC * (ISNULL(TAXVTP,0)/100) FROM SAQICO A(NOLOCK) JOIN (SELECT  DISTINCT QUOTE_ID,SERVICE_ID,REVISION_ID,LINE,EQUIPMENT_ID,CONTRACT_YEAR FROM SAQICO_INBOUND B(NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.QTEREV_ID = B.REVISION_ID AND A.LINE = B.LINE AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.CNTYER = B.CONTRACT_YEAR WHERE A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' ' ")
                    
                    #TAMTGC - Total Amount (Global Currency) 
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                        + str(Parameter1.QUERY_CRITERIA_1)
                        + "  A SET TAMTGC = ISNULL(TENVGC,0) + ISNULL(TNTVGC,0) + ISNULL(TAXVGC,0) FROM SAQICO A(NOLOCK) JOIN (SELECT  DISTINCT QUOTE_ID,SERVICE_ID,REVISION_ID,LINE,EQUIPMENT_ID,CONTRACT_YEAR FROM SAQICO_INBOUND B(NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.QTEREV_ID = B.REVISION_ID AND A.LINE = B.LINE AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.CNTYER = B.CONTRACT_YEAR WHERE A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' ' ")
                    
                    #PDC price blank
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                        + str(Parameter1.QUERY_CRITERIA_1)
                        + "  A SET INMP01 = NULL,INMP02 = NULL,FNMDPR = NULL,MTGPRC = NULL,MSLPRC = NULL,MBDPRC = NULL,MCLPRC = NULL,CNTPRC = NULL,TRGPRC = NULL,SLSPRC = NULL,BDVPRC = NULL,CELPRC = NULL,FINPRC = NULL,SBTPRC = NULL,USRPRC = NULL,AIUPPE = NULL,AICPPE = NULL,SPCTPR = NULL,SVCTPR = NULL,TNTVGC = NULL,TNTMGC = NULL,TNTMPC = NULL,TENVGC = NULL,TAXVGC = NULL,TAMTGC = NULL FROM SAQICO A(NOLOCK) JOIN (SELECT  DISTINCT QUOTE_ID,SERVICE_ID,REVISION_ID,LINE,EQUIPMENT_ID,CONTRACT_YEAR FROM SAQICO_INBOUND B(NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.QTEREV_ID = B.REVISION_ID AND A.LINE = B.LINE AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.CNTYER = B.CONTRACT_YEAR WHERE A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND A.SERVICE_ID IN (''Z0091'',''Z0035'',''Z0099'') AND A.GRNBOK = ''PDC''  ' ")
                    
                    #Round Off
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                        + str(Parameter1.QUERY_CRITERIA_1)
                        + "  A SET TAMTGC = ROUND(TAMTGC ,CONVERT(FLOAT,"+str(roundcurr1.DECIMAL_PLACES)+"),CONVERT(FLOAT,"+str(roundcurr1.ROUNDING_METHOD)+")), TAXVGC = ROUND(TAXVGC ,CONVERT(FLOAT,"+str(roundcurr1.DECIMAL_PLACES)+"),CONVERT(FLOAT,"+str(roundcurr1.ROUNDING_METHOD)+")), TNTVGC = ROUND(TNTVGC ,CONVERT(FLOAT,"+str(roundcurr1.DECIMAL_PLACES)+"),CONVERT(FLOAT,"+str(roundcurr1.ROUNDING_METHOD)+")),MTGPRC = ROUND(MTGPRC ,CONVERT(FLOAT,"+str(roundcurr1.DECIMAL_PLACES)+"),CONVERT(FLOAT,"+str(roundcurr1.ROUNDING_METHOD)+")),MSLPRC = ROUND(MSLPRC ,CONVERT(FLOAT,"+str(roundcurr1.DECIMAL_PLACES)+"),CONVERT(FLOAT,"+str(roundcurr1.ROUNDING_METHOD)+")),MBDPRC = ROUND(MBDPRC ,CONVERT(FLOAT,"+str(roundcurr1.DECIMAL_PLACES)+"),CONVERT(FLOAT,"+str(roundcurr1.ROUNDING_METHOD)+")),MCLPRC = ROUND(MCLPRC ,CONVERT(FLOAT,"+str(roundcurr1.DECIMAL_PLACES)+"),CONVERT(FLOAT,"+str(roundcurr1.ROUNDING_METHOD)+")),INMP01 = ROUND(INMP01 ,CONVERT(FLOAT,"+str(roundcurr1.DECIMAL_PLACES)+"),CONVERT(FLOAT,"+str(roundcurr1.ROUNDING_METHOD)+")),INMP02 = ROUND(INMP02 ,CONVERT(FLOAT,"+str(roundcurr1.DECIMAL_PLACES)+"),CONVERT(FLOAT,"+str(roundcurr1.ROUNDING_METHOD)+")),FNMDPR = ROUND(FNMDPR ,CONVERT(FLOAT,"+str(roundcurr1.DECIMAL_PLACES)+"),CONVERT(FLOAT,"+str(roundcurr1.ROUNDING_METHOD)+")),CELPRC = ROUND(CELPRC ,CONVERT(FLOAT,"+str(roundcurr1.DECIMAL_PLACES)+"),CONVERT(FLOAT,"+str(roundcurr1.ROUNDING_METHOD)+"))   FROM SAQICO A(NOLOCK) JOIN (SELECT  DISTINCT QUOTE_ID,SERVICE_ID,REVISION_ID,LINE,EQUIPMENT_ID,CONTRACT_YEAR  FROM SAQICO_INBOUND B(NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.QTEREV_ID = B.REVISION_ID AND A.LINE = B.LINE AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.CNTYER = B.CONTRACT_YEAR WHERE A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"''  ' ")
                    
                    #TNTVDC / TAXVDC / TAMTDC /TENVDC - Total Net Value / Tax / Total Amount/ Estimated (Document Currency) 
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                        + str(Parameter1.QUERY_CRITERIA_1)
                        + "  A SET TNTVDC = ROUND( (TNTVGC * ISNULL(DCCRFX,1)) ,CONVERT(FLOAT,"+str(roundcurr.DECIMAL_PLACES)+"),CONVERT(FLOAT,"+str(roundcurr.ROUNDING_METHOD)+")), TAXVDC = ROUND( (TAXVGC * ISNULL(DCCRFX,1)) ,CONVERT(FLOAT,"+str(roundcurr.DECIMAL_PLACES)+"),CONVERT(FLOAT,"+str(roundcurr.ROUNDING_METHOD)+")), TAMTDC = ROUND( (TAMTGC * ISNULL(DCCRFX,1)) ,CONVERT(FLOAT,"+str(roundcurr.DECIMAL_PLACES)+"),CONVERT(FLOAT,"+str(roundcurr.ROUNDING_METHOD)+")), TENVDC = ROUND( (TENVGC * ISNULL(DCCRFX,1)) ,CONVERT(FLOAT,"+str(roundcurr.DECIMAL_PLACES)+"),CONVERT(FLOAT,"+str(roundcurr.ROUNDING_METHOD)+")),TRGPRC = ROUND(TRGPRC ,CONVERT(FLOAT,"+str(roundcurr.DECIMAL_PLACES)+"),CONVERT(FLOAT,"+str(roundcurr.ROUNDING_METHOD)+")),USRPRC = ROUND(USRPRC ,CONVERT(FLOAT,"+str(roundcurr.DECIMAL_PLACES)+"),CONVERT(FLOAT,"+str(roundcurr.ROUNDING_METHOD)+")),SLSPRC = ROUND(SLSPRC ,CONVERT(FLOAT,"+str(roundcurr.DECIMAL_PLACES)+"),CONVERT(FLOAT,"+str(roundcurr.ROUNDING_METHOD)+")),BDVPRC = ROUND(BDVPRC ,CONVERT(FLOAT,"+str(roundcurr.DECIMAL_PLACES)+"),CONVERT(FLOAT,"+str(roundcurr.ROUNDING_METHOD)+")),CNTPRC = ROUND(CNTPRC ,CONVERT(FLOAT,"+str(roundcurr.DECIMAL_PLACES)+"),CONVERT(FLOAT,"+str(roundcurr.ROUNDING_METHOD)+")),CNTCST = ROUND(CNTCST ,CONVERT(FLOAT,"+str(roundcurr.DECIMAL_PLACES)+"),CONVERT(FLOAT,"+str(roundcurr.ROUNDING_METHOD)+"))  FROM SAQICO A(NOLOCK) JOIN (SELECT  DISTINCT QUOTE_ID,SERVICE_ID,REVISION_ID,LINE,EQUIPMENT_ID,CONTRACT_YEAR FROM SAQICO_INBOUND B(NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.QTEREV_ID = B.REVISION_ID AND A.LINE = B.LINE AND A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.CNTYER = B.CONTRACT_YEAR WHERE A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' ' ")
                        
                    #Item Roll Up
                    primaryQueryItems = SqlHelper.GetFirst(
                    ""
                    + str(Parameter1.QUERY_CRITERIA_1)
                    + "  SAQITM SET TAX_AMOUNT_INGL_CURR = ROUND(ISNULL(TAXVGC,0),CONVERT(FLOAT,"+str(roundcurr1.DECIMAL_PLACES)+"),CONVERT(FLOAT,"+str(roundcurr1.ROUNDING_METHOD)+")) ,NET_VALUE_INGL_CURR =  ROUND(ISNULL(TNTVGC,0),CONVERT(FLOAT,"+str(roundcurr1.DECIMAL_PLACES)+"),CONVERT(FLOAT,"+str(roundcurr1.ROUNDING_METHOD)+")),UNIT_PRICE_INGL_CURR = ROUND(ISNULL(USRPRC,0),CONVERT(FLOAT,"+str(roundcurr1.DECIMAL_PLACES)+"),CONVERT(FLOAT,"+str(roundcurr1.ROUNDING_METHOD)+")),TAX_AMOUNT = ROUND(ISNULL(TAXVDC,0),CONVERT(FLOAT,"+str(roundcurr.DECIMAL_PLACES)+"),CONVERT(FLOAT,"+str(roundcurr.ROUNDING_METHOD)+")) ,NET_VALUE =  ROUND(ISNULL(TNTVDC,0),CONVERT(FLOAT,"+str(roundcurr.DECIMAL_PLACES)+"),CONVERT(FLOAT,"+str(roundcurr.ROUNDING_METHOD)+")),UNIT_PRICE = ROUND(ISNULL(USRPRC,0),CONVERT(FLOAT,"+str(roundcurr.DECIMAL_PLACES)+"),CONVERT(FLOAT,"+str(roundcurr.ROUNDING_METHOD)+")),TOTAL_AMOUNT = ROUND(ISNULL(TAMTDC,0),CONVERT(FLOAT,"+str(roundcurr.DECIMAL_PLACES)+"),CONVERT(FLOAT,"+str(roundcurr.ROUNDING_METHOD)+")),TOTAL_AMOUNT_INGL_CURR = ROUND(ISNULL(TAMTGC,0),CONVERT(FLOAT,"+str(roundcurr1.DECIMAL_PLACES)+"),CONVERT(FLOAT,"+str(roundcurr.ROUNDING_METHOD)+")),ESTIMATED_VALUE = ROUND(ISNULL(TENVDC,0),CONVERT(FLOAT,"+str(roundcurr.DECIMAL_PLACES)+"),CONVERT(FLOAT,"+str(roundcurr.ROUNDING_METHOD)+"))  FROM SAQRIT SAQITM(NOLOCK) JOIN(SELECT SAQICO.QTEREV_ID,LINE,SAQICO.QUOTE_ID,SAQICO.SERVICE_ID,SUM(TAXVGC) AS TAXVGC, SUM(TNTVGC) AS TNTVGC,SUM(USRPRC) AS USRPRC,SUM(TAXVDC) AS TAXVDC, SUM(TAMTDC) AS TAMTDC,SUM(TAMTGC) AS TAMTGC, SUM(TNTVDC) AS TNTVDC,SUM(TENVDC) AS TENVDC, SUM(TENVGC) AS TENVGC,SUM(CNTCST) AS CNTCST FROM SAQICO (NOLOCK) WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND LINE IN(SELECT DISTINCT LINE FROM SAQICO_INBOUND (NOLOCK) WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND REVISION_ID = ''"+str(Qt_Id.REVISION_ID)+"'') GROUP BY SAQICO.QUOTE_ID,SAQICO.SERVICE_ID,SAQICO.QTEREV_ID,SAQICO.LINE) SUB_SAQITM  ON SAQITM.QUOTE_ID = SUB_SAQITM.QUOTE_ID AND SUB_SAQITM.QTEREV_ID = SAQITM.QTEREV_ID  AND SAQITM.LINE = SUB_SAQITM.LINE WHERE SAQITM.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND SAQITM.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND SAQITM.SERVICE_ID <> ''Z0116'' ' ")
                    
                    primaryQueryItems = SqlHelper.GetFirst(
                    ""
                    + str(Parameter1.QUERY_CRITERIA_1)
                    + "  SAQITM SET PEREVTCST_INGL_CURR= ROUND(ISNULL(CNTCST,0)/QUANTITY,CONVERT(FLOAT,"+str(roundcurr1.DECIMAL_PLACES)+"),CONVERT(FLOAT,"+str(roundcurr1.ROUNDING_METHOD)+")) ,PEREVTPRC_INDT_CURR = ROUND(ISNULL( (CASE WHEN BILTYP=''VARIABLE'' THEN TENVDC ELSE TNTVDC END)/QUANTITY,0),CONVERT(FLOAT,"+str(roundcurr.DECIMAL_PLACES)+"),CONVERT(FLOAT,"+str(roundcurr.ROUNDING_METHOD)+")),PEREVTPRC_INGL_CURR = ROUND(ISNULL((CASE WHEN BILTYP=''VARIABLE'' THEN TENVGC ELSE TNTVGC END)/QUANTITY,0),CONVERT(FLOAT,"+str(roundcurr1.DECIMAL_PLACES)+"),CONVERT(FLOAT,"+str(roundcurr1.ROUNDING_METHOD)+")) ,PEREVTCST_INDT_CURR= ROUND((ISNULL(CNTCST,0) * ISNULL((SELECT EXCHANGE_RATE FROM SAQTRV(NOLOCK) WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"''),1) )/QUANTITY ,CONVERT(FLOAT,"+str(roundcurr.DECIMAL_PLACES)+"),CONVERT(FLOAT,"+str(roundcurr.ROUNDING_METHOD)+")),ESTVAL_INGL_CURR = ROUND(ISNULL(TENVGC,0),CONVERT(FLOAT,"+str(roundcurr1.DECIMAL_PLACES)+"),CONVERT(FLOAT,"+str(roundcurr1.ROUNDING_METHOD)+")) FROM SAQRIT SAQITM(NOLOCK) JOIN(SELECT SAQICO.QTEREV_ID,LINE,SAQICO.QUOTE_ID,SAQICO.SERVICE_ID,SUM(TAXVGC) AS TAXVGC, SUM(TNTVGC) AS TNTVGC,SUM(USRPRC) AS USRPRC,SUM(TAXVDC) AS TAXVDC, SUM(TAMTDC) AS TAMTDC,SUM(TAMTGC) AS TAMTGC, SUM(TNTVDC) AS TNTVDC,SUM(TENVDC) AS TENVDC, SUM(TENVGC) AS TENVGC,SUM(CNTCST) AS CNTCST,BILTYP FROM SAQICO (NOLOCK) WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"''  AND LINE IN(SELECT DISTINCT LINE FROM SAQICO_INBOUND (NOLOCK) WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND REVISION_ID = ''"+str(Qt_Id.REVISION_ID)+"'') AND SERVICE_ID IN( ''Z0009'',''Z0010'',''Z0128'') AND QTETYP NOT IN (''TOOL BASED'')  GROUP BY SAQICO.QUOTE_ID,SAQICO.SERVICE_ID,SAQICO.QTEREV_ID,SAQICO.LINE,BILTYP) SUB_SAQITM  ON SAQITM.QUOTE_ID = SUB_SAQITM.QUOTE_ID AND SUB_SAQITM.QTEREV_ID = SAQITM.QTEREV_ID  AND SAQITM.LINE = SUB_SAQITM.LINE WHERE QUANTITY > 0 ' ")

                    #Item Roll Up Year 1
                    primaryQueryItems = SqlHelper.GetFirst(
                    ""
                    + str(Parameter1.QUERY_CRITERIA_1)
                    + "  SAQITM SET YEAR_1_INGL_CURR = CASE WHEN BILTYP=''VARIABLE'' THEN TENVGC ELSE TNTVGC END, YEAR_1 =  CASE WHEN BILTYP=''VARIABLE'' THEN TENVDC ELSE TNTVDC END FROM SAQRIT SAQITM(NOLOCK) JOIN(SELECT SUM(SAQICO.TNTVGC) AS TNTVGC,SAQICO.QTEREV_ID,SAQICO.LINE,SAQICO.QUOTE_ID,SAQICO.SERVICE_ID,SUM(TNTVDC) AS TNTVDC,SUM(TENVGC) AS TENVGC,SUM(TENVDC) AS TENVDC,BILTYP FROM SAQICO (NOLOCK) JOIN (SELECT DISTINCT LINE FROM SAQICO_INBOUND (NOLOCK) WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND REVISION_ID = ''"+str(Qt_Id.REVISION_ID)+"'')B ON SAQICO.LINE = B.LINE WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND CNTYER=''YEAR 1''  GROUP BY SAQICO.QUOTE_ID,SAQICO.SERVICE_ID,SAQICO.QTEREV_ID,SAQICO.LINE,BILTYP) SUB_SAQITM  ON SAQITM.QUOTE_ID = SUB_SAQITM.QUOTE_ID AND SUB_SAQITM.QTEREV_ID = SAQITM.QTEREV_ID  AND SAQITM.LINE = SUB_SAQITM.LINE ' ")

                    #Item Roll Up Year 2
                    primaryQueryItems = SqlHelper.GetFirst(
                    ""
                    + str(Parameter1.QUERY_CRITERIA_1)
                    + "  SAQITM SET YEAR_2_INGL_CURR = CASE WHEN BILTYP=''VARIABLE'' THEN TENVGC ELSE TNTVGC END, YEAR_2 =  CASE WHEN BILTYP=''VARIABLE'' THEN TENVDC ELSE TNTVDC END FROM SAQRIT SAQITM(NOLOCK) JOIN(SELECT SUM(SAQICO.TNTVGC) AS TNTVGC,SAQICO.QTEREV_ID,SAQICO.LINE,SAQICO.QUOTE_ID,SAQICO.SERVICE_ID,SUM(TNTVDC) AS TNTVDC,SUM(TENVGC) AS TENVGC,SUM(TENVDC) AS TENVDC,BILTYP FROM SAQICO (NOLOCK) JOIN (SELECT DISTINCT LINE FROM SAQICO_INBOUND (NOLOCK) WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND REVISION_ID = ''"+str(Qt_Id.REVISION_ID)+"'')B ON SAQICO.LINE = B.LINE  WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND CNTYER=''YEAR 2''   GROUP BY SAQICO.QUOTE_ID,SAQICO.SERVICE_ID,SAQICO.QTEREV_ID,SAQICO.LINE,BILTYP) SUB_SAQITM  ON SAQITM.QUOTE_ID = SUB_SAQITM.QUOTE_ID AND SUB_SAQITM.QTEREV_ID = SAQITM.QTEREV_ID  AND SAQITM.LINE = SUB_SAQITM.LINE ' ")

                    #Item Roll Up Year 3
                    primaryQueryItems = SqlHelper.GetFirst(
                    ""
                    + str(Parameter1.QUERY_CRITERIA_1)
                    + "  SAQITM SET YEAR_3_INGL_CURR = CASE WHEN BILTYP=''VARIABLE'' THEN TENVGC ELSE TNTVGC END, YEAR_3 =  CASE WHEN BILTYP=''VARIABLE'' THEN TENVDC ELSE TNTVDC END FROM SAQRIT SAQITM(NOLOCK) JOIN(SELECT SUM(SAQICO.TNTVGC) AS TNTVGC,SAQICO.QTEREV_ID,SAQICO.LINE,SAQICO.QUOTE_ID,SAQICO.SERVICE_ID,SUM(TNTVDC) AS TNTVDC,SUM(TENVGC) AS TENVGC,SUM(TENVDC) AS TENVDC,BILTYP FROM SAQICO (NOLOCK) JOIN (SELECT DISTINCT LINE FROM SAQICO_INBOUND (NOLOCK) WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND REVISION_ID = ''"+str(Qt_Id.REVISION_ID)+"'')B ON SAQICO.LINE = B.LINE  WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND CNTYER=''YEAR 3''  GROUP BY SAQICO.QUOTE_ID,SAQICO.SERVICE_ID,SAQICO.QTEREV_ID,SAQICO.LINE,BILTYP) SUB_SAQITM  ON SAQITM.QUOTE_ID = SUB_SAQITM.QUOTE_ID AND SUB_SAQITM.QTEREV_ID = SAQITM.QTEREV_ID  AND SAQITM.LINE = SUB_SAQITM.LINE ' ")

                    #Item Roll Up Year 4
                    primaryQueryItems = SqlHelper.GetFirst(
                    ""
                    + str(Parameter1.QUERY_CRITERIA_1)
                    + "  SAQITM SET YEAR_4_INGL_CURR = CASE WHEN BILTYP=''VARIABLE'' THEN TENVGC ELSE TNTVGC END, YEAR_4 =  CASE WHEN BILTYP=''VARIABLE'' THEN TENVDC ELSE TNTVDC END FROM SAQRIT SAQITM(NOLOCK) JOIN(SELECT SUM(SAQICO.TNTVGC) AS TNTVGC,SAQICO.QTEREV_ID,SAQICO.LINE,SAQICO.QUOTE_ID,SAQICO.SERVICE_ID,SUM(TNTVDC) AS TNTVDC,SUM(TENVGC) AS TENVGC,SUM(TENVDC) AS TENVDC,BILTYP FROM SAQICO (NOLOCK) JOIN (SELECT DISTINCT LINE FROM SAQICO_INBOUND (NOLOCK) WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND REVISION_ID = ''"+str(Qt_Id.REVISION_ID)+"'')B ON SAQICO.LINE = B.LINE  WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND CNTYER=''YEAR 4''   GROUP BY SAQICO.QUOTE_ID,SAQICO.SERVICE_ID,SAQICO.QTEREV_ID,SAQICO.LINE,BILTYP) SUB_SAQITM  ON SAQITM.QUOTE_ID = SUB_SAQITM.QUOTE_ID AND SUB_SAQITM.QTEREV_ID = SAQITM.QTEREV_ID  AND SAQITM.LINE = SUB_SAQITM.LINE ' ")

                    #Item Roll Up Year 5
                    primaryQueryItems = SqlHelper.GetFirst(
                    ""
                    + str(Parameter1.QUERY_CRITERIA_1)
                    + "  SAQITM SET YEAR_5_INGL_CURR = CASE WHEN BILTYP=''VARIABLE'' THEN TENVGC ELSE TNTVGC END, YEAR_5 =  CASE WHEN BILTYP=''VARIABLE'' THEN TENVDC ELSE TNTVDC END FROM SAQRIT SAQITM(NOLOCK) JOIN(SELECT SUM(SAQICO.TNTVGC) AS TNTVGC,SAQICO.QTEREV_ID,SAQICO.LINE,SAQICO.QUOTE_ID,SAQICO.SERVICE_ID,SUM(TNTVDC) AS TNTVDC,SUM(TENVGC) AS TENVGC,SUM(TENVDC) AS TENVDC,BILTYP FROM SAQICO (NOLOCK) JOIN (SELECT DISTINCT LINE FROM SAQICO_INBOUND (NOLOCK) WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND REVISION_ID = ''"+str(Qt_Id.REVISION_ID)+"'')B ON SAQICO.LINE = B.LINE  WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND CNTYER=''YEAR 5''  GROUP BY SAQICO.QUOTE_ID,SAQICO.SERVICE_ID,SAQICO.QTEREV_ID,SAQICO.LINE,BILTYP) SUB_SAQITM  ON SAQITM.QUOTE_ID = SUB_SAQITM.QUOTE_ID AND SUB_SAQITM.QTEREV_ID = SAQITM.QTEREV_ID  AND SAQITM.LINE = SUB_SAQITM.LINE ' ")
                    
                    #Status - On Hold Costing
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                    + str(Parameter1.QUERY_CRITERIA_1)
                    + "  SAQICO SET STATUS=''CFG-ON HOLD - COSTING'' FROM SAQICO (NOLOCK) JOIN (SELECT DISTINCT QUOTE_ID,SERVICE_ID,LINE,REVISION_ID,CONTRACT_YEAR FROM SAQICO_INBOUND(NOLOCK)  WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND ISNULL(COST_MODULE_AVAILABLE,'''')=''UNAVAILABLE'' AND ISNULL(COST_CALCULATION_STATUS,'''') <> ''Chamber map not required'' )SAQICO_INBOUND ON SAQICO.QUOTE_ID = SAQICO_INBOUND.QUOTE_ID AND SAQICO.SERVICE_ID = SAQICO_INBOUND.SERVICE_ID AND SAQICO.LINE = SAQICO_INBOUND.LINE AND SAQICO.QTEREV_ID = SAQICO_INBOUND.REVISION_ID AND CONTRACT_YEAR = CNTYER '")
                    
                    #Status - On Hold Costing (No Cost in SSCM)
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                    + str(Parameter1.QUERY_CRITERIA_1)
                    + "  SAQICO SET STATUS=''CFG-ON HOLD - COSTING'' FROM SAQICO (NOLOCK) WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND STATUS NOT IN (''ERROR'',''ASSEMBLY IS MISSING'',''OFFLINE PRICING'') AND ISNULL(CNTCST,0)<=0 AND LINE IN (SELECT DISTINCT LINE FROM SAQICO_INBOUND WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' )  '")
                    
                    #Status - On Hold Pricing (No Price in CPQ)
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                    + str(Parameter1.QUERY_CRITERIA_1)
                    + "  SAQICO SET STATUS=''PRR-ON HOLD PRICING'' FROM SAQICO (NOLOCK) WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND STATUS NOT IN (''ERROR'',''ASSEMBLY IS MISSING'',''CFG-ON HOLD - COSTING'') AND ISNULL(CNTCST,0)>0 AND ISNULL(CNTPRC,0)<=0 AND LINE IN (SELECT DISTINCT LINE FROM SAQICO_INBOUND WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' )  '")
                    
                    #Status - On Hold Pricing (Up Time Percent)
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                    + str(Parameter1.QUERY_CRITERIA_1)
                    + "  SAQICO SET STATUS=''PRR-ON HOLD PRICING'' FROM SAQICO (NOLOCK) WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND STATUS NOT IN (''ERROR'',''ASSEMBLY IS MISSING'',''CFG-ON HOLD - COSTING'') AND ISNULL(CNTPRC,0)>0 AND ITSDUI > 2 AND ISNULL(AIUICI,0)=0 AND ISNULL(AIUIPI,0)=0 AND LINE IN (SELECT DISTINCT LINE FROM SAQICO_INBOUND WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' )  '")
                    
                    #Status - On Hold Pricing (Head Rebuild In)
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                    + str(Parameter1.QUERY_CRITERIA_1)
                    + "  SAQICO SET STATUS=''PRR-ON HOLD PRICING'' FROM SAQICO (NOLOCK) WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND STATUS NOT IN (''ERROR'',''ASSEMBLY IS MISSING'',''CFG-ON HOLD - COSTING'') AND ISNULL(CNTPRC,0)>0 AND HEDBIN = ''INCLUDED'' AND ISNULL(HEDBIC,0)=0 AND ISNULL(HEDBIP,0)=0 AND LINE IN (SELECT DISTINCT LINE FROM SAQICO_INBOUND WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' )  '")
                    
                    #Status - On Hold Pricing (Non Consumables)
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                    + str(Parameter1.QUERY_CRITERIA_1)
                    + "  SAQICO SET STATUS=''PRR-ON HOLD PRICING'' FROM SAQICO (NOLOCK) WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND STATUS NOT IN (''ERROR'',''ASSEMBLY IS MISSING'',''CFG-ON HOLD - COSTING'') AND ISNULL(CNTPRC,0)>0 AND ISNULL(NCNSMB_ENT,''EXCLUDED'') IN (''Some Exclusions'',''Some Inclusions'') AND ISNULL(NONCCI,0)=0 AND ISNULL(NONCPI,0)=0 AND LINE IN (SELECT DISTINCT LINE FROM SAQICO_INBOUND WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' )  '")
                    
                    #Status - On Hold Pricing (Consumables)
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                    + str(Parameter1.QUERY_CRITERIA_1)
                    + "  SAQICO SET STATUS=''PRR-ON HOLD PRICING'' FROM SAQICO (NOLOCK) WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND STATUS NOT IN (''ERROR'',''ASSEMBLY IS MISSING'',''CFG-ON HOLD - COSTING'') AND ISNULL(CNTPRC,0)>0 AND ISNULL(CNSMBL_ENT,''EXCLUDED'') IN (''Some Exclusions'',''Some Inclusions'') AND ISNULL(CONSCP,0)=0 AND ISNULL(CONSPI,0)=0 AND LINE IN (SELECT DISTINCT LINE FROM SAQICO_INBOUND WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' ) AND SERVICE_ID NOT IN (''Z0092'')  '")
                    
                    #Status - On Hold Pricing (Specialized Cleaning)
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                    + str(Parameter1.QUERY_CRITERIA_1)
                    + "  SAQICO SET STATUS=''PRR-ON HOLD PRICING'' FROM SAQICO (NOLOCK) WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND STATUS NOT IN (''ERROR'',''ASSEMBLY IS MISSING'',''CFG-ON HOLD - COSTING'',''PRR-ON HOLD PRICING'') AND ISNULL(CNTPRC,0)>0 AND SPCCLN = ''INCLUDED'' AND ISNULL(SPCCLC,0)=0 AND ISNULL(SPCCLP,0)=0 AND LINE IN (SELECT DISTINCT LINE FROM SAQICO_INBOUND WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' ) '")
                    
                    #Status - On Hold Pricing (Specialized Coating)
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                    + str(Parameter1.QUERY_CRITERIA_1)
                    + "  SAQICO SET STATUS=''PRR-ON HOLD PRICING'' FROM SAQICO (NOLOCK) WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND STATUS NOT IN (''ERROR'',''ASSEMBLY IS MISSING'',''CFG-ON HOLD - COSTING'',''PRR-ON HOLD PRICING'') AND ISNULL(CNTPRC,0)>0 AND SPCCOT = ''INCLUDED'' AND ISNULL(SPCCCI,0)=0 AND ISNULL(SPCCPI,0)=0 AND LINE IN (SELECT DISTINCT LINE FROM SAQICO_INBOUND WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' ) '")
                    
                    #Status - On Hold Pricing (Number Of Layers)
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                    + str(Parameter1.QUERY_CRITERIA_1)
                    + "  SAQICO SET STATUS=''PRR-ON HOLD PRICING'' FROM SAQICO (NOLOCK) WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND STATUS NOT IN (''ERROR'',''ASSEMBLY IS MISSING'',''CFG-ON HOLD - COSTING'',''PRR-ON HOLD PRICING'') AND ISNULL(CNTPRC,0)>0 AND ISNULL(NUMLAY,'''') <> '''' AND ISNULL(NUMLCI,0)=0 AND ISNULL(NUMLPI,0)=0 AND LINE IN (SELECT DISTINCT LINE FROM SAQICO_INBOUND WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' ) '")
                    
                    #Status - On Hold Pricing (Additional Target KPI)
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                    + str(Parameter1.QUERY_CRITERIA_1)
                    + "  SAQICO SET STATUS=''PRR-ON HOLD PRICING'' FROM SAQICO (NOLOCK) WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND STATUS NOT IN (''ERROR'',''ASSEMBLY IS MISSING'',''CFG-ON HOLD - COSTING'') AND ISNULL(CNTPRC,0)>0 AND ISNULL(ATGKEY,''EXCLUDED'') <> ''EXCLUDED'' AND ISNULL(ATGKEC,0)=0 AND ISNULL(ATGKEP,0)=0 AND LINE IN (SELECT DISTINCT LINE FROM SAQICO_INBOUND WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' ) '")
                    
                    #Status - On Hold Pricing (New Parts)
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                    + str(Parameter1.QUERY_CRITERIA_1)
                    + "  SAQICO SET STATUS=''PRR-ON HOLD PRICING'' FROM SAQICO (NOLOCK) WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND STATUS NOT IN (''ERROR'',''ASSEMBLY IS MISSING'',''CFG-ON HOLD - COSTING'',''PRR-ON HOLD PRICING'') AND ISNULL(CNTPRC,0)>0 AND ISNULL(NWPTON,''NO'') = ''YES'' AND ISNULL(NWPTOC,0)=0 AND ISNULL(NWPTOP,0)=0 AND LINE IN (SELECT DISTINCT LINE FROM SAQICO_INBOUND WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' ) '")
                    
                    #Status - On Hold Pricing (PDC)
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                    + str(Parameter1.QUERY_CRITERIA_1)
                    + "  SAQICO SET STATUS=''PRR-ON HOLD PRICING'' FROM SAQICO (NOLOCK) WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND STATUS NOT IN (''ERROR'',''ASSEMBLY IS MISSING'',''CFG-ON HOLD - COSTING'',''PRR-ON HOLD PRICING'') AND GRNBOK=''PDC'' AND SERVICE_ID IN (''Z0091'',''Z0035'',''Z0099'') AND LINE IN (SELECT DISTINCT LINE FROM SAQICO_INBOUND WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' ) '")
                    
                    #Status - On Hold TKM
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                    + str(Parameter1.QUERY_CRITERIA_1)
                    + "  SAQICO SET STATUS=''CFG-ON HOLD TKM'' FROM SAQICO (NOLOCK) JOIN SAQGPA (NOLOCK) ON SAQICO.QUOTE_ID = SAQGPA.QUOTE_ID AND SAQICO.QTEREV_ID = SAQGPA.QTEREV_ID AND SAQICO.SERVICE_ID = SAQGPA.SERVICE_ID AND SAQICO.EQUIPMENT_ID = SAQGPA.EQUIPMENT_ID AND CASE WHEN ISNULL(SAQICO.PM_ID,'''')='''' THEN SAQGPA.PM_ID ELSE SAQICO.PM_ID END = SAQGPA.PM_ID AND CASE WHEN ISNULL(SAQICO.KIT_ID,'''')='''' THEN SAQGPA.KIT_ID ELSE SAQICO.KIT_ID END = SAQGPA.KIT_ID AND SAQICO.GOT_CODE = SAQGPA.GOT_CODE  AND ISNULL(SAQICO.PROCES,'''') = ISNULL(SAQGPA.PROCESS_TYPE,'''') AND ISNULL(SAQICO.DEVICE_NODE,'''') = ISNULL(SAQGPA.DEVICE_NODE,'''') JOIN SAQRIO (NOLOCK) ON SAQICO.QUOTE_ID = SAQRIO.QUOTE_ID AND SAQICO.QTEREV_ID = SAQRIO.QTEREV_ID AND SAQICO.LINE = SAQRIO.LINE AND SAQICO.EQUIPMENT_ID = SAQRIO.EQUIPMENT_ID AND SAQRIO.ASSEMBLY_ID = SAQGPA.ASSEMBLY_ID   WHERE SAQICO.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND SAQICO.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND SAQICO.LINE IN (SELECT DISTINCT LINE FROM SAQICO_INBOUND WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' ) AND ISNULL(SAQICO.STATUS,'''') NOT IN (''PRR-ON HOLD PRICING'',''CFG-ON HOLD - COSTING'',''ASSEMBLY IS MISSING'') AND ISNULL(SAQGPA.KIT_ID,'''')<>'''' AND ISNULL(SAQGPA.KIT_NUMBER,'''')='''' '")
                    
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                    + str(Parameter1.QUERY_CRITERIA_1)
                    + "  SAQICO SET STATUS=''CFG-ON HOLD TKM'' FROM SAQICO (NOLOCK) JOIN SAQSAP (NOLOCK) ON SAQICO.QUOTE_ID = SAQSAP.QUOTE_ID AND SAQICO.QTEREV_ID = SAQSAP.QTEREV_ID AND SAQICO.SERVICE_ID = SAQSAP.SERVICE_ID AND SAQICO.EQUIPMENT_ID = SAQSAP.EQUIPMENT_ID  WHERE SAQICO.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND SAQICO.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' AND SAQICO.LINE IN (SELECT DISTINCT LINE FROM SAQICO_INBOUND WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' ) AND ISNULL(SAQICO.STATUS,'''') NOT IN (''PRR-ON HOLD PRICING'',''CFG-ON HOLD - COSTING'',''ASSEMBLY IS MISSING'') AND ISNULL(SAQSAP.KIT_ID,'''')<>'''' AND ISNULL(SAQSAP.KIT_NUMBER,'''')='''' '")
                                    
                    #Status - Acquired
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                    + str(Parameter1.QUERY_CRITERIA_1)
                    + "  SAQICO SET STATUS=''ACQUIRED'' FROM SAQICO (NOLOCK) JOIN SAQICO_INBOUND C(NOLOCK)ON SAQICO.QUOTE_ID = C.QUOTE_ID AND SAQICO.QTEREV_ID = C.REVISION_ID  AND SAQICO.SERVICE_ID = C.SERVICE_ID AND SAQICO.LINE = C.LINE WHERE TIMESTAMP = '"+str(timestamp_sessionid)+"' AND STATUS NOT IN (''ERROR'',''ASSEMBLY IS MISSING'',''CFG-ON HOLD - COSTING'',''PRR-ON HOLD PRICING'',''CFG-ON HOLD TKM'') '")
                    
                    #Status Item - On Hold Costing
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                    + str(Parameter1.QUERY_CRITERIA_1)
                    + "  SAQITM SET STATUS=''CFG-ON HOLD - COSTING'' FROM SAQRIT SAQITM (NOLOCK) WHERE QUOTE_REVISION_CONTRACT_ITEM_ID IN (SELECT DISTINCT QTEITM_RECORD_ID FROM SAQICO_INBOUND(NOLOCK)A JOIN SAQICO B(NOLOCK) ON A.QUOTE_ID= B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.LINE = B.LINE AND A.REVISION_ID = B.QTEREV_ID WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND B.STATUS=''CFG-ON HOLD - COSTING'' AND B.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND B.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' ) AND SERVICE_ID IN (SELECT DISTINCT SERVICE_ID FROM PRSPRV(NOLOCK) WHERE ISNULL(SSCM_COST,''FALSE'')=''TRUE'' )  '")
                    
                    #Status Item - On Hold Pricing
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                    + str(Parameter1.QUERY_CRITERIA_1)
                    + "  SAQITM SET STATUS=''PRR-ON HOLD PRICING'' FROM SAQRIT SAQITM (NOLOCK) WHERE QUOTE_REVISION_CONTRACT_ITEM_ID IN (SELECT DISTINCT QTEITM_RECORD_ID FROM SAQICO_INBOUND(NOLOCK)A JOIN SAQICO B(NOLOCK) ON A.QUOTE_ID= B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.LINE = B.LINE AND A.REVISION_ID = B.QTEREV_ID WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND B.STATUS=''PRR-ON HOLD PRICING'' AND B.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND B.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' ) AND SERVICE_ID IN (SELECT DISTINCT SERVICE_ID FROM PRSPRV(NOLOCK) WHERE ISNULL(SSCM_COST,''FALSE'')=''TRUE'' ) AND ISNULL(STATUS,'''') NOT IN (''CFG-ON HOLD - COSTING'') '")
                    
                    #Status Item - On Hold TKM
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                    + str(Parameter1.QUERY_CRITERIA_1)
                    + "  SAQITM SET STATUS=''CFG-ON HOLD TKM'' FROM SAQRIT SAQITM (NOLOCK) WHERE QUOTE_REVISION_CONTRACT_ITEM_ID IN (SELECT DISTINCT QTEITM_RECORD_ID FROM SAQICO_INBOUND(NOLOCK)A JOIN SAQICO B(NOLOCK) ON A.QUOTE_ID= B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.LINE = B.LINE AND A.REVISION_ID = B.QTEREV_ID WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND B.STATUS=''CFG-ON HOLD TKM'' AND B.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND B.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' ) AND SERVICE_ID IN (SELECT DISTINCT SERVICE_ID FROM PRSPRV(NOLOCK) WHERE ISNULL(SSCM_COST,''FALSE'')=''TRUE'' ) AND ISNULL(STATUS,'''') NOT IN (''CFG-ON HOLD - COSTING'',''PRR-ON HOLD PRICING'') '")
                    
                    #Status Item - Acquired
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                    + str(Parameter1.QUERY_CRITERIA_1)
                    + "  SAQITM SET STATUS=''ACQUIRED'' FROM SAQRIT SAQITM (NOLOCK) WHERE QUOTE_REVISION_CONTRACT_ITEM_ID IN (SELECT DISTINCT QTEITM_RECORD_ID FROM SAQICO_INBOUND(NOLOCK)A JOIN SAQICO B(NOLOCK) ON A.QUOTE_ID= B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.LINE = B.LINE AND A.REVISION_ID = B.QTEREV_ID WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' AND B.STATUS=''ACQUIRED'' AND B.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND B.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' ) AND SERVICE_ID IN (SELECT DISTINCT SERVICE_ID FROM PRSPRV(NOLOCK) WHERE ISNULL(SSCM_COST,''FALSE'')=''TRUE'' ) AND ISNULL(STATUS,'''') NOT IN (''CFG-ON HOLD - COSTING'',''PRR-ON HOLD PRICING'',''CFG-ON HOLD TKM'') '")
                    
                    #Revision Status check
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                    + str(Parameter1.QUERY_CRITERIA_1)
                    + "  SAQTRV SET REVISION_STATUS=''CFG-ACQUIRING'',WORKFLOW_STATUS = ''CONFIGURE'' FROM SAQTRV A(NOLOCK) WHERE A.QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'' '")
                    
                    #Revision Status - On Hold Costing
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                    + str(Parameter1.QUERY_CRITERIA_1)
                    + "  SAQTRV SET REVISION_STATUS=''CFG-ON HOLD - COSTING'',WORKFLOW_STATUS = ''CONFIGURE'' FROM SAQTRV A(NOLOCK) JOIN (SELECT DISTINCT QUOTE_ID,QTEREV_ID FROM SAQRIT B(NOLOCK)  WHERE  ISNULL(STATUS,'''')  IN (''CFG-ON HOLD - COSTING'',''ERROR'',''ASSEMBLY IS MISSING'','''') AND QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'')B ON A.QUOTE_ID = B.QUOTE_ID AND A.QTEREV_ID = B.QTEREV_ID '")
                    
                    #Revision Status - On Hold Pricing
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                    + str(Parameter1.QUERY_CRITERIA_1)
                    + "  SAQTRV SET REVISION_STATUS=''PRR-ON HOLD PRICING'',WORKFLOW_STATUS = ''PRICING REVIEW'' FROM SAQTRV A(NOLOCK) JOIN (SELECT DISTINCT QUOTE_ID,QTEREV_ID FROM SAQRIT B(NOLOCK)  WHERE  ISNULL(STATUS,'''')  IN (''PRR-ON HOLD PRICING'',''OFFLINE PRICING'') AND QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'')B ON A.QUOTE_ID = B.QUOTE_ID AND A.QTEREV_ID = B.QTEREV_ID AND REVISION_STATUS NOT IN (''CFG-ON HOLD - COSTING'') '")
                    
                    #Revision Status - Pricing
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                    + str(Parameter1.QUERY_CRITERIA_1)
                    + "  SAQTRV SET REVISION_STATUS=''PRI-PRICING'',WORKFLOW_STATUS = ''PRICING'' FROM SAQTRV A(NOLOCK) JOIN (SELECT DISTINCT QUOTE_ID,QTEREV_ID FROM SAQRIT B(NOLOCK)  WHERE  ISNULL(STATUS,'''')  IN (''ACQUIRED'',''CFG-ON HOLD TKM'') AND QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'')B ON A.QUOTE_ID = B.QUOTE_ID AND A.QTEREV_ID = B.QTEREV_ID AND REVISION_STATUS NOT IN (''CFG-ON HOLD - COSTING'',''PRR-ON HOLD PRICING'') '")
                    
                    #Revision History
                    primaryQueryItems = SqlHelper.GetFirst(
                        ""
                    + str(Parameter.QUERY_CRITERIA_1)
                    + "  SAQRSH (QUOTE_ID,QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,REVISION_STATUS,REVSTS_CHANGE_DATE,CpqTableEntryDateModified,CPQTABLEENTRYDATEADDED,QUOTE_REVISION_STATUS_HISTROY_ID,CPQTABLEENTRYADDEDBY,CpqTableEntryModifiedBy) SELECT A.*,CONVERT(VARCHAR(100),NEWID()),''"
                    + str(User.UserName)+ "'',''"+ str(User.Id)+ "'' FROM (SELECT DISTINCT QUOTE_ID,QUOTE_RECORD_ID,QTEREV_ID,QUOTE_REVISION_RECORD_ID AS QTEREV_RECORD_ID,REVISION_STATUS,GETDATE() AS REVSTS_CHANGE_DATE,GETDATE() AS CpqTableEntryDateModified,GETDATE() AS CPQTABLEENTRYDATEADDED  FROM SAQTRV(NOLOCK) WHERE QUOTE_ID = ''"+str(Qt_Id.QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(Qt_Id.REVISION_ID)+"'')A  '")
                    
                                        
                    quote_revision_object = SqlHelper.GetFirst("SELECT QUOTE_RECORD_ID, QTEREV_RECORD_ID FROM SAQTRV WHERE QUOTE_ID = '"+str(Qt_Id.QUOTE_ID)+"' AND QTEREV_ID = '"+str(Qt_Id.REVISION_ID)+"' ")

                    ##Calling the iflow script to update the details in c4c..(cpq to c4c write back...)
                    CQCPQC4CWB.writeback_to_c4c("quote_header",quote_revision_object.QUOTE_RECORD_ID,quote_revision_object.QTEREV_RECORD_ID)
                    CQCPQC4CWB.writeback_to_c4c("opportunity_header",quote_revision_object.QUOTE_RECORD_ID,quote_revision_object.QTEREV_RECORD_ID)
                    
                    #Status Completed in SYINPL by CPQ Table Entry ID
                    StatusUpdateQuery = SqlHelper.GetFirst(""+ str(Parameter1.QUERY_CRITERIA_1)+ "  SYINPL SET STATUS = ''COMPLETED'' FROM SYINPL (NOLOCK) A WHERE CpqTableEntryId = ''"+str(json_data.CpqTableEntryId)+"'' AND SESSION_ID =''"+str(SYINPL_SESSION.A)+"'' ' ")

                    StatusUpdateQuery = SqlHelper.GetFirst(""+ str(Parameter2.QUERY_CRITERIA_1)+ " FROM SAQICO_INBOUND  WHERE ISNULL(SESSION_ID,'''')=''"+str(sessiondetail.A)+ "'' ' ")

                    SAQIEN_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQIEN)+"'' ) BEGIN DROP TABLE "+str(SAQIEN)+" END  ' ")
                    
                    CRMTMP_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(CRMTMP)+"'' ) BEGIN DROP TABLE "+str(CRMTMP)+" END  ' ")
                    
                    Log.Info("QTPOSTQTPR pricing async call End --->"+str(Qt_Id.QUOTE_ID))
                    # Mail system               
                    Header = "<!DOCTYPE html><html><head><style>table {font-family: Calibri, sans-serif; border-collapse: collapse; width: 75%}td, th {  border: 1px solid #dddddd;  text-align: left; padding: 8px;}.im {color: #222;}tr:nth-child(even) {background-color: #dddddd;} #grey{background: rgb(245,245,245);} #bd{color : 'black';} </style></head><body id = 'bd'>"

                    Table_start = "<p>Hi Team,<br><br>Pricing has been completed in CPQ, for the equipment's in below Quote ID.</p><table class='table table-bordered'><tr><th id = 'grey'>Quote ID</th><th id = 'grey'>Tools sent (CPQ-SSCM)</th><th id = 'grey'>Tools received (SSCM-CPQ)</th><th id = 'grey'>Price Calculation Status</th></tr><tr><td >"+str(Emailinfo.QUOTE_ID)+"</td><td>"+str(Emailinfo.SSCM)+"</td ><td>"+str(Emailinfo1.CPQ)+"</td><td>Completed</td></tr>"

                    Table_info = ""
                    Table_End = "</table><p><strong>Note : </strong>Please do not reply to this email.</p></body></html>"

                    Error_Info = Header + Table_start + Table_info + Table_End

                    LOGIN_CRE = SqlHelper.GetFirst("SELECT USER_NAME as Username,Password FROM SYCONF where Domain ='SUPPORT_MAIL'")

                    # Create new SmtpClient object
                    mailClient = SmtpClient("10.150.65.7")

                    #Current user email(Toemail)
                    #UserId = User.Id
                    #Log.Info("123 UserId.UserId --->"+str(UserId))
                    if ToEml is None:

                        UserEmail = SqlHelper.GetFirst("SELECT isnull(email,'"+str(LOGIN_CRE.Username)+"') as email FROM saempl (nolock) where employee_id  = 'X0116954'")

                    else:

                        UserEmail = SqlHelper.GetFirst("SELECT isnull(email,'"+str(LOGIN_CRE.Username)+"') as email FROM saempl (nolock) where employee_id  = '"+str(ToEml.OWNER_ID)+"'")
                    #Log.Info("123 UserEmail.email --->"+str(UserEmail.email))

                    # Create two mail adresses, one for send from and the another for recipient
                    if UserEmail is None:
                        toEmail = MailAddress("suresh.muniyandi@bostonharborconsulting.com")
                    else:
                        toEmail = MailAddress(UserEmail.email)
                    fromEmail = 'noreply@calliduscloud.com'

                    # Create new MailMessage object
                    msg = MailMessage()
            
                    msg.From = MailAddress(fromEmail)
                    msg.To.Add(toEmail)

                    # Set message subject and body
                    msg.Subject = "Pricing Completed - AMAT CPQ(P-Tenant)"
                    msg.IsBodyHtml = True
                    msg.Body = Error_Info

                    # Bcc Emails    
                    copyEmail4 = MailAddress("baji.baba@bostonharborconsulting.com")
                    msg.Bcc.Add(copyEmail4)

                    copyEmail6 = MailAddress("suresh.muniyandi@bostonharborconsulting.com")
                    msg.Bcc.Add(copyEmail6)

                    copyEmail7 = MailAddress("christoper.aravinth@bostonharborconsulting.com")
                    msg.Bcc.Add(copyEmail7)


                    # Send the message
                    mailClient.Send(msg)

 
                    Greenbkquery=SqlHelper.GetList("SELECT DISTINCT SAQICO.GRNBOK as GREENBOOK,ISNULL(SABUUN.DISTRIBUTION_EMAIL,'') AS DISTRIBUTION_EMAIL  FROM SAQICO(NOLOCK) JOIN SABUUN (NOLOCK) ON SAQICO.GRNBOK = SABUUN.BUSINESSUNIT_ID WHERE SAQICO.STATUS IN ('ERROR','ASSEMBLY IS MISSING','CFG-ON HOLD - COSTING','PRR-ON HOLD PRICING') AND SAQICO.QUOTE_ID = '"+str(Qt_Id.QUOTE_ID)+"' AND SAQICO.QTEREV_ID = '"+str(Qt_Id.REVISION_ID)+"' ")

                    for Gbk in Greenbkquery:


                        Grnbkdataquery=SqlHelper.GetList("SELECT SAQICO.GRNBOK as GREENBOOK,SAQICO.QUOTE_ID,SAQICO.SERVICE_ID,SAQICO.EQUIPMENT_ID,SAQICA.ASSEMBLY_ID,SAQICA.COST_MODULE_AVAILABLE,CASE WHEN ISNULL(TOTAL_COST_WOSEEDSTOCK,0)<=0 AND ISNULL (COST_MODULE_STATUS,'')='' AND ISNULL (COST_MODULE_AVAILABLE,'')='AVAILABLE' THEN 'No Cost in SSCM' else ISNULL(SAQICA.COST_MODULE_STATUS,'') END AS COST_MODULE_STATUS FROM SAQICO (NOLOCK) JOIN SAQICA (NOLOCK) ON SAQICO.QUOTE_ID = SAQICA.QUOTE_ID AND SAQICO.QTEREV_ID = SAQICA.QTEREV_ID AND SAQICO.LINE = SAQICA.LINE AND SAQICO.EQUIPMENT_ID = SAQICA.EQUIPMENT_ID WHERE SAQICO.STATUS IN ('ERROR','CFG-ON HOLD - COSTING') AND SAQICO.GRNBOK= '"+str(Gbk.GREENBOOK)+"' AND SAQICO.QUOTE_ID = '"+str(Qt_Id.QUOTE_ID)+"' AND SAQICO.QTEREV_ID = '"+str(Qt_Id.REVISION_ID)+"' AND (ISNULL(TOTAL_COST_WOSEEDSTOCK,0)<=0 OR ISNULL (COST_MODULE_STATUS,'')<>'') UNION ALL SELECT SAQICO.GRNBOK,SAQICO.QUOTE_ID,SAQICO.SERVICE_ID,SAQICO.EQUIPMENT_ID,'' AS ASSEMBLY_ID,'' AS COST_MODULE_AVAILABLE,'ASSEMBLY IS MISSING' AS COST_MODULE_STATUS FROM SAQICO (NOLOCK)  WHERE SAQICO.STATUS IN ('ASSEMBLY IS MISSING' ) AND SAQICO.GRNBOK= '"+str(Gbk.GREENBOOK)+"' AND SAQICO.QUOTE_ID = '"+str(Qt_Id.QUOTE_ID)+"' AND SAQICO.QTEREV_ID = '"+str(Qt_Id.REVISION_ID)+"' ")

                        tbl_info = ''
                        for gbkinfo in Grnbkdataquery:
                            tbl_info = tbl_info+"<tr><td>"+str(gbkinfo.SERVICE_ID)+"</td><td>"+str(gbkinfo.GREENBOOK)+"</td ><td>"+str(gbkinfo.EQUIPMENT_ID)+"</td><td>"+str(gbkinfo.ASSEMBLY_ID)+"</td><td>"+str(gbkinfo.COST_MODULE_AVAILABLE)+"</td><td>"+str(gbkinfo.COST_MODULE_STATUS)+"</td></tr>"
                        if len(tbl_info) > 0:
                            Header = "<!DOCTYPE html><html><head><style>table {font-family: Calibri, sans-serif; border-collapse: collapse; width: 75%}td, th {  border: 1px solid #dddddd;  text-align: left; padding: 8px;}.im {color: #222;}tr:nth-child(even) {background-color: #dddddd;} #grey{background: rgb(245,245,245);} #bd{color : 'black';} </style></head><body id = 'bd'>"

                            Table_start = "<p>Hi Team,<br><br>This Quote "+str(Qt_Id.QUOTE_ID)+"  is placed on ON HOLD COSTING status for the below cost information pending from SSCM system or Assembly missing in CPQ from IBASE.</p><table class='table table-bordered'><tr><th id = 'grey'>Service ID</th><th id = 'grey'>Green Book</th><th id = 'grey'>Equipment ID</th><th id = 'grey'>Assembly ID</th><th id = 'grey'>Cost Module Available</th><th id = 'grey'>Cost Module Status</th></tr>"+str(tbl_info)

                            Table_info = ""
                            Table_End = "</table><p><strong>Note : </strong>Please do not reply to this email.</p></body></html>"

                            Error_Info = Header + Table_start + Table_info + Table_End

                            LOGIN_CRE = SqlHelper.GetFirst("SELECT USER_NAME as Username,Password FROM SYCONF where Domain ='SUPPORT_MAIL'")

                            # Create new SmtpClient object
                            mailClient = SmtpClient("10.150.65.7")

                            UserEmail = []
                            if len(Gbk.DISTRIBUTION_EMAIL) > 0:
                                UserEmail = str(Gbk.DISTRIBUTION_EMAIL).split(';')

                            if len(UserEmail) == 0:
                                    toEmail = MailAddress("suresh.muniyandi@bostonharborconsulting.com")
                            else:                               
                                toEmail = MailAddress(UserEmail[0])
                            
                            fromEmail = 'noreply@calliduscloud.com' 

                            # Create new MailMessage object
                            msg = MailMessage()
            
                            msg.From = MailAddress(fromEmail)
                            msg.To.Add(toEmail)                         

                            # Set message subject and body
                            sub = "On Hold - Costing Quote("+str(Gbk.GREENBOOK)+")- AMAT CPQ (P-Tenant)"
                            msg.Subject = sub
                            msg.IsBodyHtml = True
                            msg.Body = Error_Info

                            #Comon CC mails
                            copyEmail = MailAddress("suresh.muniyandi@bostonharborconsulting.com")
                            msg.Bcc.Add(copyEmail)                   

                            copyEmail5 = MailAddress("baji.baba@bostonharborconsulting.com")
                            msg.Bcc.Add(copyEmail5) 

                            copyEmail7 = MailAddress("christoper.aravinth@bostonharborconsulting.com")
                            msg.Bcc.Add(copyEmail7)

                            # Bcc Emails    
                            if len(UserEmail) > 0:
                                for emalinfo in  UserEmail:
                                    copyEmail = MailAddress(emalinfo)
                                    msg.Bcc.Add(copyEmail)

                            # Send the message QT_REC_ID
                            mailClient.Send(msg)
                    #opening quote for update quote items
                    try:
                        quote_Edit = QuoteHelper.Edit(Qt_Id.QUOTE_ID)
                    except:
                        Log.Info("quote error")
                    CallingCQIFWUDQTM = ScriptExecutor.ExecuteGlobal("CQIFWUDQTM",{"QT_REC_ID":Qt_Id.QUOTE_ID}) 
                    # Billing matrix async call
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
                        
                        result = '''<?xml version="1.0" encoding="UTF-8"?><soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">  <soapenv:Body><CPQ_Columns> <QUOTE_ID>{Qt_Id}</QUOTE_ID><REVISION_ID>{Rev_Id}</REVISION_ID></CPQ_Columns></soapenv:Body></soapenv:Envelope>'''.format( Qt_Id= quote_revision_object.QUOTE_RECORD_ID,Rev_Id = quote_revision_object.QTEREV_RECORD_ID)
                        
                        #LOGIN_CRE = SqlHelper.GetFirst("SELECT URL FROM SYCONF where EXTERNAL_TABLE_NAME ='BILLING_MATRIX_ASYNC'")
                        #Async = webclient.UploadString(str(LOGIN_CRE.URL), str(result))

                        level = "QT_QTQICO LEVEL"
                        try:
                            CQVLDRIFLW.iflow_valuedriver_rolldown(str(Emailinfo.QUOTE_RECORD_ID),level)
                        except:
                            Log.Info('Quote error')
                    
                    
                    Unprocsseddataquery = SqlHelper.GetFirst("SELECT count(*) as cnt from SYINPL(NOLOCK) WHERE INTEGRATION_NAME = 'SSCM_TO_CPQ_PRICING_DATA' AND ISNULL(STATUS,'') = '' ")  

                    if Unprocsseddataquery.cnt > 0 :
                        #Async call for SSCM TO CPQ Unprocessed data 
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
                    else: 
                        ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "200", "Message": "Data Successfully Uploaded"}]})
                else:
                    if Saqico_Flag == 0:
                        Header = "<!DOCTYPE html><html><head><style>table {font-family: Calibri, sans-serif; border-collapse: collapse; width: 75%}td, th {  border: 1px solid #dddddd;  text-align: left; padding: 8px;}.im {color: #222;}tr:nth-child(even) {background-color: #dddddd;} #bd{color : 'black';} </style></head><body id = 'bd'>"

                        Table_start = "<p>Hi Team,<br><br>SSCM Pricing script having follwing SAQICO data error for following Quote Id ---  "+str(Qt_Id.QUOTE_ID)+".<br><br></p><br>"
                        
                        Table_End = "</table><p><strong>Note : </strong>Please do not reply to this email.</p></body></html>"
                        Table_info = ""     

                        Error_Info = Header + Table_start + Table_info + Table_End

                        LOGIN_CRE = SqlHelper.GetFirst("SELECT USER_NAME as Username,Password FROM SYCONF where Domain ='SUPPORT_MAIL'")
                        
                        StatusUpdateQuery = SqlHelper.GetFirst(""+ str(Parameter2.QUERY_CRITERIA_1)+ " FROM SAQICO_INBOUND  WHERE ISNULL(SESSION_ID,'''')=''"+str(sessiondetail.A)+ "'' ' ")

                        # Create new SmtpClient object
                        mailClient = SmtpClient("10.150.65.7")

                        if ToEml is None:

                            UserEmail = SqlHelper.GetFirst("SELECT isnull(email,'"+str(LOGIN_CRE.Username)+"') as email FROM saempl (nolock) where employee_id  = 'X0116954'")

                        else:

                            UserEmail = SqlHelper.GetFirst("SELECT isnull(email,'"+str(LOGIN_CRE.Username)+"') as email FROM saempl (nolock) where employee_id  = '"+str(ToEml.OWNER_ID)+"'")

                        # Create two mail adresses, one for send from and the another for recipient
                        if UserEmail is None:
                            toEmail = MailAddress("suresh.muniyandi@bostonharborconsulting.com")
                        else:
                            toEmail = MailAddress(UserEmail.email)
                        fromEmail = 'noreply@calliduscloud.com'                     

                        # Create new MailMessage object
                        msg = MailMessage()
            
                        msg.From = MailAddress(fromEmail)
                        msg.To.Add(toEmail)

                        # Set message subject and body
                        msg.Subject = "SSCM to CPQ - SAQICO Error Notification(P-Tenant)"
                        msg.IsBodyHtml = True
                        msg.Body = Error_Info

                        # CC Emails     
                        copyEmail4 = MailAddress("baji.baba@bostonharborconsulting.com")
                        msg.Bcc.Add(copyEmail4)
                        
                        copyEmail5 = MailAddress("suresh.muniyandi@bostonharborconsulting.com")
                        msg.Bcc.Add(copyEmail5)      

                        copyEmail7 = MailAddress("christoper.aravinth@bostonharborconsulting.com")
                        msg.Bcc.Add(copyEmail7)      

                        # Send the message
                        mailClient.Send(msg)
                    if Check_flag == 1:
                        #Status Empty in SYINPL
                        StatusUpdateQuery = SqlHelper.GetFirst(""+ str(Parameter1.QUERY_CRITERIA_1)+ "  A SET STATUS = ''Hold'' FROM SYINPL (NOLOCK) A WHERE SESSION_ID=''"+str(SYINPL_SESSION.A)+"''   AND  STATUS = ''INPROGRESS'' '")
    else:
        ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "200", "Message": "Session is running.Status is Inprogress"}]})
        

except:
    #Status Empty in SYINPL
    StatusUpdateQuery = SqlHelper.GetFirst(""+ str(Parameter1.QUERY_CRITERIA_1)+ "  A SET STATUS = '''' FROM SYINPL (NOLOCK) A WHERE SESSION_ID=''"+str(SYINPL_SESSION.A)+"''  ' ")
                
    Header = "<!DOCTYPE html><html><head><style>table {font-family: Calibri, sans-serif; border-collapse: collapse; width: 75%}td, th {  border: 1px solid #dddddd;  text-align: left; padding: 8px;}.im {color: #222;}tr:nth-child(even) {background-color: #dddddd;} #bd{color : 'black';} </style></head><body id = 'bd'>"

    Table_start = "<p>Hi Team,<br><br>SSCM Pricing script having follwing Error in Line number "+str(sys.exc_info()[-1].tb_lineno)+".<br><br>"+str(sys.exc_info()[1])+"</p><br>"
    
    Table_End = "</table><p><strong>Note : </strong>Please do not reply to this email.</p></body></html>"
    Table_info = ""     

    Error_Info = Header + Table_start + Table_info + Table_End

    ToEml = SqlHelper.GetFirst("SELECT ISNULL(OWNER_ID,'X0116954') as OWNER_ID FROM SAQTMT (NOLOCK) WHERE SAQTMT.QUOTE_ID = '"+str(Glb_Quote_Id)+"'  ")

    LOGIN_CRE = SqlHelper.GetFirst("SELECT USER_NAME as Username,Password FROM SYCONF where Domain ='SUPPORT_MAIL'")

    # Create new SmtpClient object
    mailClient = SmtpClient("10.150.65.7")
    
    if ToEml is None:

        UserEmail = SqlHelper.GetFirst("SELECT isnull(email,'"+str(LOGIN_CRE.Username)+"') as email FROM saempl (nolock) where employee_id  = 'X0116954'")

    else:

        UserEmail = SqlHelper.GetFirst("SELECT isnull(email,'"+str(LOGIN_CRE.Username)+"') as email FROM saempl (nolock) where employee_id  = '"+str(ToEml.OWNER_ID)+"'")

    # Create two mail adresses, one for send from and the another for recipient
    if UserEmail is None:
        toEmail = MailAddress("suresh.muniyandi@bostonharborconsulting.com")
    else:
        toEmail = MailAddress(UserEmail.email)
    fromEmail = 'noreply@calliduscloud.com' 
    

    # Create new MailMessage object
    msg = MailMessage()
            
    msg.From = MailAddress(fromEmail)
    msg.To.Add(toEmail)

    # Set message subject and body
    msg.Subject = "SSCM to CPQ - Pricing Error Notification(P-Tenant)"
    msg.IsBodyHtml = True
    msg.Body = Error_Info

    # CC Emails     
    copyEmail4 = MailAddress("baji.baba@bostonharborconsulting.com")
    msg.Bcc.Add(copyEmail4)

    copyEmail5 = MailAddress("suresh.muniyandi@bostonharborconsulting.com")
    msg.Bcc.Add(copyEmail5)

    copyEmail7 = MailAddress("christoper.aravinth@bostonharborconsulting.com")
    msg.Bcc.Add(copyEmail7)

    
    # Send the message
    mailClient.Send(msg) 
    
    Log.Info("QTPOSTQTPR ERROR---->:" + str(sys.exc_info()[1]))
    Log.Info("QTPOSTQTPR ERROR LINE NO---->:" + str(sys.exc_info()[-1].tb_lineno))
    ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "400", "Message": str(sys.exc_info()[1])}]})
    ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "400", "Message": str(sys.exc_info()[1])}]})
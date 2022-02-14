# =========================================================================================================================================
#   __script_name : QTPOSTPRSM.PY
#   __script_description : THIS SCRIPT IS USED TO GET SSCM DATA FROM THE QTQCAS TABLE AND RETURN IN JSON FORMAT RESULT
#   __primary_author__ : SURESH MUNIYANDI, Baji
#   __create_date :
#	Modified Date : 25-Nov-2020 JIRA 12516 (PMSA Tool Based)
#  BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import sys
import clr
import System.Net
from System.Text.Encoding import UTF8
from System import Convert
from System.Net import HttpWebRequest, NetworkCredential
from System.Net import *
from System.Net import CookieContainer
from System.Net import Cookie
from System.Net import WebRequest
from System.Net import HttpWebResponse
from System import Uri
clr.AddReference("System.Net")
from System.Net import CookieContainer, NetworkCredential, Mail
from System.Net.Mail import SmtpClient, MailAddress, Attachment, MailMessage
import time


input_data = [str(param_result.Value) for param_result in Param.CPQ_Columns]
input_data = [input_data]
sess = SqlHelper.GetFirst("select left(convert(varchar(100),newid()),5) as sess  ")
Log.Info("28/12  input_data --->"+str(input_data))

try:

	for crmifno in input_data:	

		Qt_id = crmifno[0]
		REVISION_ID = crmifno[-1]
		
		Log.Info("28/12 QTPOSTPRSM Qt_id ---->"+str(Qt_id))
		
		sessionid = SqlHelper.GetFirst("SELECT NEWID() AS A")
		timestamp_sessionid = "'" + str(sessionid.A) + "'"
		
		Flag = 'False'
		
		CRMQT = SqlHelper.GetFirst("select convert(varchar(100),c4c_quote_id) as c4c_quote_id from SAQTMT(nolock) WHERE QUOTE_ID = '"+str(Qt_id)+"' ")
		
		SAQSCO = "SAQSCO_BKP_1"+str(CRMQT.c4c_quote_id)+str(sess.sess)
		SAQIEN = "SAQIEN_BKP_1"+str(CRMQT.c4c_quote_id)+str(sess.sess)
		SAQSCA = "SAQSCA_BKP_1"+str(CRMQT.c4c_quote_id)+str(sess.sess)
		SAQSAP = "SAQSAP_BKP_1"+str(CRMQT.c4c_quote_id)+str(sess.sess)
		SAQSAE = "SAQSAE_BKP_1"+str(CRMQT.c4c_quote_id)+str(sess.sess)
		
		SAQSCO_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQSCO)+"'' ) BEGIN DROP TABLE "+str(SAQSCO)+" END  ' ")
		
		SAQIEN_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQIEN)+"'' ) BEGIN DROP TABLE "+str(SAQIEN)+" END  ' ")
		
		SAQSCA_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQSCA)+"'' ) BEGIN DROP TABLE "+str(SAQSCA)+" END  ' ")

		SAQSAP_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQSAP)+"'' ) BEGIN DROP TABLE "+str(SAQSAP)+" END  ' ")
		
		SAQSAE_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQSAE)+"'' ) BEGIN DROP TABLE "+str(SAQSAE)+" END  ' ")
		
		SAQSCO_SEL = SqlHelper.GetFirst("sp_executesql @T=N'select DISTINCT A.QUOTE_ID,D.EQUIPMENT_ID,A.SERVICE_ID,B.SALESORG_ID,C.REGION,A.QTEREV_ID,B.CONTRACT_VALID_FROM,B.CONTRACT_VALID_TO,C.ACCOUNT_NAME,(SELECT DISTINCT FABLOCATION_NAME FROM MAEQUP(NOLOCK) WHERE MAEQUP.EQUIPMENT_ID = A.EQUIPMENT_ID) AS FAB_NAME,(SELECT DISTINCT VALDRV_WAFERNODE FROM MAEQUP(NOLOCK) WHERE MAEQUP.EQUIPMENT_ID = A.EQUIPMENT_ID) AS TECH_NODE_RANGE,D.LINE,A.CMLAB_ENT,A.CNSMBL_ENT, A.CNTCVG_ENT,A.NCNSMB_ENT,A.PMEVNT_ENT,A.PMLAB_ENT,A.PRMKPI_ENT,A.WETCLN_ENT INTO "+str(SAQSCO)+" from SAQICO(NOLOCK) A JOIN SAQTRV B(NOLOCK) ON A.QUOTE_ID = B.QUOTE_ID AND A.QTEREV_ID = B.QTEREV_ID JOIN SAQTMT C(NOLOCK) ON B.QUOTE_ID = C.QUOTE_ID AND B.QTEREV_ID = C.QTEREV_ID JOIN SAQRIO D(NOLOCK) ON A.QUOTE_ID = D.QUOTE_ID AND A.QTEREV_ID = D.QTEREV_ID AND A.LINE = D.LINE WHERE A.QUOTE_ID = ''"+str(Qt_id)+"'' AND A.QTEREV_ID=''"+str(REVISION_ID) +"'' AND A.SERVICE_ID IN (SELECT DISTINCT SERVICE_ID FROM PRSPRV(NOLOCK) WHERE ISNULL(SSCM_COST,''FALSE'')=''TRUE'' ) AND ISNULL(A.STATUS,'''')=''''  ' ")
		
		"""
		start = 1
		end = 1
		Check_flag = 1
		while Check_flag == 1:
			ent_query = SqlHelper.GetFirst("SELECT DISTINCT QUOTE_ID,LINE FROM (SELECT DISTINCT quote_id,LINE, ROW_NUMBER()OVER(ORDER BY LINE) AS SNO FROM SAQITE (NOLOCK) where quote_id='"+str(Qt_id)+"' AND QTEREV_ID='"+str(REVISION_ID) +"' AND SERVICE_ID IN (SELECT DISTINCT SERVICE_ID FROM PRSPRV(NOLOCK) WHERE ISNULL(SSCM_COST,'FALSE')='TRUE') ) A WHERE SNO>= "+str(start)+" AND SNO<="+str(end)+" ")
			if str(ent_query) != "None":
				
				start = start + 1
				end = end + 1
				
				
				if start == 2:
					SAQIEN_SEL = SqlHelper.GetFirst("sp_executesql @T=N'declare @H int; Declare @val Varchar(MAX);DECLARE @XML XML; SELECT @val = FINAL from(select  REPLACE(entitlement_xml,''<QUOTE_ITEM_ENTITLEMENT>'',sml) AS FINAL FROM (select ''<QUOTE_ITEM_ENTITLEMENT><QUOTE_ID>''+quote_id+''</QUOTE_ID><QTEREV_ID>''+CONVERT(VARCHAR,QTEREV_ID)+''</QTEREV_ID><SERVICE_ID>''+service_id+''</SERVICE_ID><LINE>''+LINE+''</LINE>'' AS sml,replace(replace(replace(replace(replace(replace(replace(ENTITLEMENT_XML,''&'','';#38''),'''','';#39''),'' < '','' &lt; '' ),'' > '','' &gt; '' ),''_>'',''_&gt;''),''_<'',''_&lt;''),''&'','';#38'')  as entitlement_xml from SAQITE(nolock) where quote_id=''"+str(Qt_id)+"'' AND QTEREV_ID=''"+str(REVISION_ID) +"'' AND LINE = "+str(ent_query.LINE)+" )A )a SELECT @XML = CONVERT(XML,''<ROOT>''+@VAL+''</ROOT>'') exec sys.sp_xml_preparedocument @H output,@XML; select QUOTE_ID,QTEREV_ID,LINE,SERVICE_ID,ENTITLEMENT_ID,ENTITLEMENT_NAME,ENTITLEMENT_VALUE_CODE,ENTITLEMENT_DISPLAY_VALUE INTO "+str(SAQIEN)+"  from openxml(@H, ''ROOT/QUOTE_ITEM_ENTITLEMENT'', 0) with (QUOTE_ID VARCHAR(100) ''QUOTE_ID'',QTEREV_ID VARCHAR(100) ''QTEREV_ID'',LINE INT ''LINE'',ENTITLEMENT_ID VARCHAR(100) ''ENTITLEMENT_ID'',SERVICE_ID VARCHAR(100) ''SERVICE_ID'',ENTITLEMENT_VALUE_CODE VARCHAR(100) ''ENTITLEMENT_VALUE_CODE'',ENTITLEMENT_NAME VARCHAR(100) ''ENTITLEMENT_NAME'',ENTITLEMENT_DISPLAY_VALUE VARCHAR(100) ''ENTITLEMENT_DISPLAY_VALUE'' ) ; exec sys.sp_xml_removedocument @H; '")
				
				else:
					SAQIEN_SEL = SqlHelper.GetFirst("sp_executesql @T=N'declare @H int; Declare @val Varchar(MAX);DECLARE @XML XML; SELECT @val = FINAL from(select  REPLACE(entitlement_xml,''<QUOTE_ITEM_ENTITLEMENT>'',sml) AS FINAL FROM (select ''<QUOTE_ITEM_ENTITLEMENT><QUOTE_ID>''+quote_id+''</QUOTE_ID><QTEREV_ID>''+CONVERT(VARCHAR,QTEREV_ID)+''</QTEREV_ID><SERVICE_ID>''+service_id+''</SERVICE_ID><LINE>''+LINE+''</LINE>'' AS sml,replace(replace(replace(replace(replace(replace(replace(ENTITLEMENT_XML,''&'','';#38''),'''','';#39''),'' < '','' &lt; '' ),'' > '','' &gt; '' ),''_>'',''_&gt;''),''_<'',''_&lt;''),''&'','';#38'')  as entitlement_xml from SAQITE(nolock) where quote_id=''"+str(Qt_id)+"''   AND QTEREV_ID=''"+str(REVISION_ID) +"'' AND LINE = "+str(ent_query.LINE)+" )A )a SELECT @XML = CONVERT(XML,''<ROOT>''+@VAL+''</ROOT>'') exec sys.sp_xml_preparedocument @H output,@XML; insert "+str(SAQIEN)+" (QUOTE_ID,QTEREV_ID,LINE,SERVICE_ID,ENTITLEMENT_ID,ENTITLEMENT_NAME,ENTITLEMENT_VALUE_CODE,ENTITLEMENT_DISPLAY_VALUE) select QUOTE_ID,QTEREV_ID,LINE,SERVICE_ID,ENTITLEMENT_ID,ENTITLEMENT_NAME,ENTITLEMENT_VALUE_CODE,ENTITLEMENT_DISPLAY_VALUE  from openxml(@H, ''ROOT/QUOTE_ITEM_ENTITLEMENT'', 0) with (QUOTE_ID VARCHAR(100) ''QUOTE_ID'',QTEREV_ID VARCHAR(100) ''QTEREV_ID'',LINE INT ''LINE'',ENTITLEMENT_ID VARCHAR(100) ''ENTITLEMENT_ID'',SERVICE_ID VARCHAR(100) ''SERVICE_ID'',ENTITLEMENT_VALUE_CODE VARCHAR(100) ''ENTITLEMENT_VALUE_CODE'',ENTITLEMENT_NAME VARCHAR(100) ''ENTITLEMENT_NAME'',ENTITLEMENT_DISPLAY_VALUE VARCHAR(100) ''ENTITLEMENT_DISPLAY_VALUE''); exec sys.sp_xml_removedocument @H; '")
			
			else:
				Check_flag=0 
		"""
		
		SAQSCA_SEL = SqlHelper.GetFirst("sp_executesql @T=N'select DISTINCT QUOTE_ID,EQUIPMENT_ID,SERVICE_ID,ASSEMBLY_ID,CONVERT(VARCHAR(100),NULL) AS COVERAGE,CONVERT(VARCHAR(100),NULL) AS WETCLEAN,CONVERT(VARCHAR(100),NULL) AS PERFGUARANTEE,CONVERT(VARCHAR(100),NULL) AS PMLABOR,CONVERT(VARCHAR(100),NULL) AS CMLABOR,CONVERT(VARCHAR(100),NULL) AS PM_EVENTS,CONVERT(VARCHAR(100),NULL) AS CONSUMABLE,CONVERT(VARCHAR(100),NULL) AS NON_CONSUMABLE,QTEREV_ID,LINE INTO "+str(SAQSCA)+" from SAQICA(NOLOCK) WHERE QUOTE_ID = ''"+str(Qt_id)+"'' AND QTEREV_ID=''"+str(REVISION_ID) +"'' AND SERVICE_ID IN (SELECT DISTINCT SERVICE_ID FROM PRSPRV(NOLOCK) WHERE ISNULL(SSCM_COST,''FALSE'')=''TRUE'' ) ' ")
		
		SAQSCO_DEL = SqlHelper.GetFirst("sp_executesql @T=N'DELETE FROM "+str(SAQSCO)+" WHERE EQUIPMENT_ID NOT IN (SELECT DISTINCT EQUIPMENT_ID FROM "+str(SAQSCA)+" ) ' ")
		
		#Contract Coverage
		S = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET COVERAGE=CNTCVG_ENT FROM  "+str(SAQSCA)+" A(NOLOCK) JOIN "+str(SAQSCO)+" B(NOLOCK) ON A.QUOTE_ID = B.QUOTE_ID AND A.QTEREV_ID = B.QTEREV_ID AND A.LINE = B.LINE AND A.EQUIPMENT_ID = B.EQUIPMENT_ID '")
		
		#Wet Cleans Labor
		S = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET WETCLEAN=WETCLN_ENT FROM  "+str(SAQSCA)+" A(NOLOCK) JOIN "+str(SAQSCO)+" B(NOLOCK) ON A.QUOTE_ID = B.QUOTE_ID AND A.QTEREV_ID = B.QTEREV_ID AND A.LINE = B.LINE AND A.EQUIPMENT_ID = B.EQUIPMENT_ID '")
		
		#Preventive Maintenance Labor
		S = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET PMLABOR=PMLAB_ENT FROM  "+str(SAQSCA)+" A(NOLOCK) JOIN "+str(SAQSCO)+" B(NOLOCK) ON A.QUOTE_ID = B.QUOTE_ID AND A.QTEREV_ID = B.QTEREV_ID AND A.LINE = B.LINE AND A.EQUIPMENT_ID = B.EQUIPMENT_ID '")
		
		#Corrective Maintenance Labor
		S = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET CMLABOR=CMLAB_ENT FROM  "+str(SAQSCA)+" A(NOLOCK) JOIN "+str(SAQSCO)+" B(NOLOCK) ON A.QUOTE_ID = B.QUOTE_ID AND A.QTEREV_ID = B.QTEREV_ID AND A.LINE = B.LINE AND A.EQUIPMENT_ID = B.EQUIPMENT_ID '")
		
		#Primary KPI. Perf Guarantee
		S = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET PERFGUARANTEE=PRMKPI_ENT FROM  "+str(SAQSCA)+" A(NOLOCK) JOIN "+str(SAQSCO)+" B(NOLOCK) ON A.QUOTE_ID = B.QUOTE_ID AND A.QTEREV_ID = B.QTEREV_ID AND A.LINE = B.LINE AND A.EQUIPMENT_ID = B.EQUIPMENT_ID '")
		
		#PM Event
		S = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET PM_EVENTS=PMEVNT_ENT FROM  "+str(SAQSCA)+" A(NOLOCK) JOIN "+str(SAQSCO)+" B(NOLOCK) ON A.QUOTE_ID = B.QUOTE_ID AND A.QTEREV_ID = B.QTEREV_ID AND A.LINE = B.LINE AND A.EQUIPMENT_ID = B.EQUIPMENT_ID '")
		
		#Consumable
		S = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET CONSUMABLE=CNSMBL_ENT FROM  "+str(SAQSCA)+" A(NOLOCK) JOIN "+str(SAQSCO)+" B(NOLOCK) ON A.QUOTE_ID = B.QUOTE_ID AND A.QTEREV_ID = B.QTEREV_ID AND A.LINE = B.LINE AND A.EQUIPMENT_ID = B.EQUIPMENT_ID '")
		
		#Non Consumable
		S = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET NON_CONSUMABLE=NCNSMB_ENT FROM  "+str(SAQSCA)+" A(NOLOCK) JOIN "+str(SAQSCO)+" B(NOLOCK) ON A.QUOTE_ID = B.QUOTE_ID AND A.QTEREV_ID = B.QTEREV_ID AND A.LINE = B.LINE AND A.EQUIPMENT_ID = B.EQUIPMENT_ID '")
		
		SAQSAP_SEL = SqlHelper.GetFirst("sp_executesql @T=N'select QUOTE_ID,EQUIPMENT_ID,SERVICE_ID,ASSEMBLY_ID,PM_FREQUENCY, PM_NAME INTO "+str(SAQSAP)+" from SAQSAP(NOLOCK) WHERE QUOTE_ID = ''"+str(Qt_id)+"'' AND QTEREV_ID=''"+str(REVISION_ID) +"'' AND PM_NAME = ''Wet Clean'' AND SERVICE_ID IN (SELECT DISTINCT SERVICE_ID FROM PRSPRV(NOLOCK) WHERE ISNULL(SSCM_COST,''FALSE'')=''TRUE''  )' ")
		
		SAQSAP_SEL = SqlHelper.GetFirst("sp_executesql @T=N'DELETE A FROM "+str(SAQSCO)+" A JOIN "+str(SAQSCA)+" B ON A.QUOTE_ID = B.QUOTE_ID AND A.QTEREV_ID = B.QTEREV_ID AND A.SERVICE_ID = B.SERVICE_ID WHERE A.SERVICE_ID = ''Z0100'' AND ISNULL(B.CONSUMABLE,'''') <> ''INCLUDED'' AND  ISNULL(B.NON_CONSUMABLE,'''') <> ''INCLUDED''  ' ")
		
		table = SqlHelper.GetFirst(
			"SELECT replace ('{\"QTQICA\": ['+STUFF((SELECT ','+ JSON FROM (SELECT DISTINCT '{\"SESSION_ID\" : \"'+SESSION_ID+'\",\"QUOTE_ID\" : \"'+QUOTE_ID+'\",\"EQUIPMENT_ID\" : \"'+EQUIPMENT_ID+'\",\"CONTRACT_VALID_FROM\" : \"'+CONTRACT_VALID_FROM+'\",\"CONTRACT_VALID_TO\" : \"'+CONTRACT_VALID_TO+'\",\"SERVICE_ID\" : \"'+SERVICE_ID+'\",\"SALESORG_ID\" : \"'+SALESORG_ID+'\",\"REGION\" : \"'+REGION+'\",\"ASSEMBLY_ID\" : \"'+ASSEMBLY_ID+'\",\"LABOR_COVERAGE\" : \"'+LABOR_COVERAGE+'\",\"PREVENTIVE_MAINTENANCE\" : \"'+PREVENTIVE_MAINTENANCE+'\",\"CORRECTIVE_MAINTENANCE\" : \"'+CORRECTIVE_MAINTENANCE+'\",\"PERFORMANCE_GUARANTEE\" : \"'+PERFORMANCE_GUARANTEE+'\",\"WET_CLEAN\" : \"'+WET_CLEAN+'\",\"PM_EVENTS\" : \"'+PM_EVENTS+'\",\"ACCOUNT_NAME\" : \"'+ACCOUNT_NAME+'\",\"FAB_NAME\" : \"'+FAB_NAME+'\",\"CONSUMABLE\" : \"'+CONSUMABLE+'\",\"NON_CONSUMABLE\" : \"'+NON_CONSUMABLE+'\",\"TECH_NODE_RANGE\" : \"'+TECH_NODE_RANGE+'\",\"PM_NAME\" : \"'+PM_NAME+'\",\"PM_PER_YEAR\" : \"'+PM_PER_YEAR+'\"}' AS JSON from (SELECT DISTINCT  "+str(timestamp_sessionid)+" as SESSION_ID, B.QUOTE_ID+'-'+ CONVERT(VARCHAR,B.QTEREV_ID) AS QUOTE_ID,ISNULL(SALESORG_ID,'') AS SALESORG_ID,ISNULL(REGION,'') AS REGION, ISNULL(B.EQUIPMENT_ID,'') AS EQUIPMENT_ID,ISNULL(B.SERVICE_ID,'') AS SERVICE_ID,ISNULL(A.ASSEMBLY_ID,'') AS ASSEMBLY_ID,ISNULL( COVERAGE,'' ) AS LABOR_COVERAGE,ISNULL(PMLABOR,'') AS PREVENTIVE_MAINTENANCE,ISNULL(CMLABOR,'') AS CORRECTIVE_MAINTENANCE,ISNULL(PERFGUARANTEE,'') AS PERFORMANCE_GUARANTEE,ISNULL(WETCLEAN,'') AS WET_CLEAN,ISNULL(PM_EVENTS,'') AS PM_EVENTS, ISNULL(PM_NAME,'') AS PM_NAME,ISNULL(CONVERT(VARCHAR(50),PM_FREQUENCY),'') AS PM_PER_YEAR,CONVERT(VARCHAR(11),B.CONTRACT_VALID_FROM,121) AS CONTRACT_VALID_FROM,CONVERT(VARCHAR(11),B.CONTRACT_VALID_TO,121) AS CONTRACT_VALID_TO,ISNULL(CONSUMABLE,'') AS CONSUMABLE,ISNULL(NON_CONSUMABLE,'') AS NON_CONSUMABLE,ISNULL(ACCOUNT_NAME,'') AS ACCOUNT_NAME,ISNULL(FAB_NAME,'') AS FAB_NAME,ISNULL(TECH_NODE_RANGE,'') AS TECH_NODE_RANGE FROM "+str(SAQSCO)+" B(NOLOCK) JOIN "+str(SAQSCA)+"(NOLOCK) A ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID= B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID LEFT JOIN "+str(SAQSAP)+" C(NOLOCK) ON A.QUOTE_ID = C.QUOTE_ID AND A.SERVICE_ID = C.SERVICE_ID AND A.EQUIPMENT_ID = C.EQUIPMENT_ID AND A.ASSEMBLY_ID=C.ASSEMBLY_ID WHERE B.QUOTE_ID = '"+str(Qt_id)+"' ) t 	) A FOR XML PATH ('')  ), 1, 1, '')+']}','amp;#','#') AS RESULT "
		)
			
		if str(table).upper() != "NONE" and str(type(table.RESULT)) == "<type 'str'>":
			Flag = "True"

			Parameter = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'SELECT' ")

			primaryQueryItems = SqlHelper.GetFirst( ""+ str(Parameter.QUERY_CRITERIA_1)+ " SYINPL (INTEGRATION_PAYLOAD,SESSION_ID,INTEGRATION_NAME)  select ''"+str(table.RESULT)+ "'','"+ str(timestamp_sessionid)+ "',''CPQ_TO_SSCM_LOAD'' ' ")
			
			#F5 AUTHENTICATION				
			LOGIN_CRE = SqlHelper.GetFirst("SELECT  URL FROM SYCONF where EXTERNAL_TABLE_NAME ='CPQ_TO_SSCM_QUOTE'")
			Oauth_info = SqlHelper.GetFirst("SELECT  DOMAIN,URL FROM SYCONF where EXTERNAL_TABLE_NAME ='OAUTH'")
			
			requestdata =Oauth_info.DOMAIN
			webclient = System.Net.WebClient()
			webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/x-www-form-urlencoded"
			response = webclient.UploadString(Oauth_info.URL,str(requestdata))

			response = eval(response)
			access_token = response['access_token']
			
			authorization = "Bearer " + access_token
			webclient = System.Net.WebClient()
			webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/json"
			webclient.Headers[System.Net.HttpRequestHeader.Authorization] = authorization;	
			Log.Info("28/12 sscm tiggerd --->")
			crm_response = webclient.UploadString(str(LOGIN_CRE.URL),str(table.RESULT))	
			Log.Info("28/12 sscm_response --->"+str(crm_response))
		
		if "Status: 200" in crm_response:

			StatusUpdate = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE SAQICO SET STATUS=''ACQUIRING'' FROM SAQICO (NOLOCK) JOIN "+str(SAQSCA)+"  SAQSCA(NOLOCK) ON SAQSCA.QUOTE_ID = SAQICO.QUOTE_ID AND SAQSCA.EQUIPMENT_ID = SAQICO.EQUIPMENT_ID AND SAQSCA.SERVICE_ID = SAQICO.SERVICE_ID WHERE SAQSCA.QUOTE_ID = ''"+str(Qt_id)+"'' AND SAQICO.QTEREV_ID= ''"+str(REVISION_ID) +"'' '")

			StatusUpdate = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE SAQICO SET STATUS=''ASSEMBLY IS MISSING'' FROM SAQICO (NOLOCK) LEFT JOIN "+str(SAQSCA)+"  SAQSCA(NOLOCK) ON SAQSCA.QUOTE_ID = SAQICO.QUOTE_ID AND SAQSCA.EQUIPMENT_ID = SAQICO.EQUIPMENT_ID AND SAQSCA.SERVICE_ID = SAQICO.SERVICE_ID WHERE SAQICO.QUOTE_ID = ''"+str(Qt_id)+"'' AND SAQICO.QTEREV_ID= ''"+str(REVISION_ID) +"'' AND SAQSCA.EQUIPMENT_ID IS NULL AND SAQICO.SERVICE_ID IN (SELECT DISTINCT SERVICE_ID FROM PRSPRV(NOLOCK) WHERE ISNULL(SSCM_COST,''FALSE'')=''TRUE'' ) '")

			Emailinfo = SqlHelper.GetFirst("SELECT QUOTE_ID,CPQ,SSCM,CPQ-SSCM AS REMANING FROM (SELECT SAQICO.QUOTE_ID,COUNT(DISTINCT SAQICO.EQUIPMENT_ID) AS CPQ,COUNT(DISTINCT SAQSCA.EQUIPMENT_ID) AS SSCM  FROM SAQICO (NOLOCK) LEFT JOIN "+str(SAQSCA)+" SAQSCA(NOLOCK) ON SAQSCA.QUOTE_ID = SAQICO.QUOTE_ID AND SAQSCA.EQUIPMENT_ID = SAQICO.EQUIPMENT_ID AND SAQSCA.SERVICE_ID = SAQICO.SERVICE_ID WHERE SAQICO.QUOTE_ID = '"+str(Qt_id)+"' AND SAQICO.QTEREV_ID = '"+str(REVISION_ID) +"' group by SAQICO.Quote_ID )SUB_SAQICO ")
			
			SAQSCO_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQSCO)+"'' ) BEGIN DROP TABLE "+str(SAQSCO)+" END  ' ")
			
			SAQIEN_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQIEN)+"'' ) BEGIN DROP TABLE "+str(SAQIEN)+" END  ' ")
			
			SAQSCA_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQSCA)+"'' ) BEGIN DROP TABLE "+str(SAQSCA)+" END  ' ")

			SAQSAP_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQSAP)+"'' ) BEGIN DROP TABLE "+str(SAQSAP)+" END  ' ")
			
			SAQSAE_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQSAE)+"'' ) BEGIN DROP TABLE "+str(SAQSAE)+" END  ' ")
			
			ToEml = SqlHelper.GetFirst("SELECT ISNULL(OWNER_ID,'X0116959') AS OWNER_ID FROM SAQTMT (NOLOCK) WHERE SAQTMT.QUOTE_ID = '"+str(Qt_id)+"'  ") 

			Header = "<!DOCTYPE html><html><head><style>table {font-family: Calibri, sans-serif; border-collapse: collapse; width: 75%}td, th {  border: 1px solid #dddddd;  text-align: left; padding: 8px;}.im {color: #222;}tr:nth-child(even) {background-color: #dddddd;} #grey{background: rgb(245,245,245);} #bd{color : 'black'} </style></head><body id = 'bd'>"


			Table_start = "<p>Hi Team,<br><br>The Tools and Assembly information has been successfully sent to retrieve the cost information from SSCM for the below Quote</p><table class='table table-bordered'><tr><th id ='grey'>QUOTE ID</th><th id = 'grey'>TOTAL TOOLS (CPQ)</th><th id = 'grey'>TOOLS SENT (SSCM)</th><th id = 'grey'>TOOLS NOT SENT TO SSCM (NO ASSEMBLY MAPPED)</th><th id = 'grey'>PRICING STATUS</th></tr><tr><td >"+str(Qt_id)+"</td><td >"+str(Emailinfo.CPQ)+"</td ><td >"+str(Emailinfo.SSCM)+"</td><td >"+str(Emailinfo.REMANING)+"</td><td>Acquiring</td></tr>"

			Table_info = ""
			Table_End = "</table><p><strong>Note : </strong>Please do not reply to this email.</p></body></html>"

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

			#Current user email(ToEmail)
			#UserId = User.Id
			#Log.Info("123 UserId.UserId --->"+str(UserId))
			UserEmail = SqlHelper.GetFirst("SELECT isnull(email,'"+str(LOGIN_CRE.Username)+"') as email FROM saempl (nolock) where employee_id  = '"+str(ToEml.OWNER_ID)+"'")
			#Log.Info("123 UserEmail.email --->"+str(UserEmail.email))

			# Create two mail adresses, one for send from and the another for recipient
			if UserEmail is None:
				toEmail = MailAddress("suresh.muniyandi@bostonharborconsulting.com")
			else:
				toEmail = MailAddress(UserEmail.email)
			fromEmail = MailAddress(str(LOGIN_CRE.Username))

			# Create new MailMessage object
			msg = MailMessage(fromEmail, toEmail)

			# Set message subject and body
			msg.Subject = "Quote Successfully Sent to SSCM(X-Tenant)"
			msg.IsBodyHtml = True
			msg.Body = Error_Info

			# Bcc Emails			

			copyEmail4 = MailAddress("baji.baba@bostonharborconsulting.com")
			msg.Bcc.Add(copyEmail4)

			copyEmail5 = MailAddress("suresh.muniyandi@bostonharborconsulting.com")
			msg.Bcc.Add(copyEmail5)

			# Send the message
			mailClient.Send(msg)		
		
		if "Status: 400" in  crm_response:
			Header = "<!DOCTYPE html><html><head><style>table {font-family: Calibri, sans-serif; border-collapse: collapse; width: 75%}td, th {  border: 1px solid #dddddd;  text-align: left; padding: 8px;}.im {color: #222;}tr:nth-child(even) {background-color: #dddddd;} #bd{color : 'black';} </style></head><body id = 'bd'>"

			Table_start = "<p>Hi Team,<br><br>The Quote Id "+Qt_id+" is not triggered for SSCM Pricing for below error.<br><br>"+str(crm_response)+"</p><br>"
			
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
			fromEmail = MailAddress(str(LOGIN_CRE.Username))

			# Create new MailMessage object
			msg = MailMessage(fromEmail, toEmail)

			# Set message subject and body
			msg.Subject = "CPQ to SSCM - Triggering Error Notification(X-Tenant)"
			msg.IsBodyHtml = True
			msg.Body = Error_Info

			# CC Emails 		

			copyEmail3 = MailAddress("suresh.muniyandi@bostonharborconsulting.com")
			msg.Bcc.Add(copyEmail3)	

			copyEmail4 = MailAddress("baji.baba@bostonharborconsulting.com")
			msg.CC.Add(copyEmail4)
			
			# Send the message
			mailClient.Send(msg)
		
		if crm_response == '':
			ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "200", "Message": "NO DATA AVAILABLE FOR SYNCHRONIZATION"}]})

		if Flag == "True":
			ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "200", "Message": str(crm_response)}]})
		else:

			SAQSCO_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQSCO)+"'' ) BEGIN DROP TABLE "+str(SAQSCO)+" END  ' ")
		
			SAQIEN_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQIEN)+"'' ) BEGIN DROP TABLE "+str(SAQIEN)+" END  ' ")
			
			SAQSCA_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQSCA)+"'' ) BEGIN DROP TABLE "+str(SAQSCA)+" END  ' ")

			SAQSAP_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQSAP)+"'' ) BEGIN DROP TABLE "+str(SAQSAP)+" END  ' ")
			
			SAQSAE_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQSAE)+"'' ) BEGIN DROP TABLE "+str(SAQSAE)+" END  ' ")

			ApiResponse = ApiResponseFactory.JsonResponse(
				{"Response": [{"Status": "200", "Message": "No Data available to process the request."}]}
			)


except:

	for crmifno in input_data:	

		Qt_id = crmifno[0]
		REVISION_ID = crmifno[-1]
		Log.Info("--->"+str(Qt_id))
		CRMQT = SqlHelper.GetFirst("select convert(varchar(100),c4c_quote_id) as c4c_quote_id from SAQTMT(nolock) WHERE QUOTE_ID = '"+str(Qt_id)+"' ")
		
		SAQSCO = "SAQSCO_BKP_1"+str(CRMQT.c4c_quote_id)+str(sess.sess)
		SAQIEN = "SAQIEN_BKP_1"+str(CRMQT.c4c_quote_id)+str(sess.sess)
		SAQSCA = "SAQSCA_BKP_1"+str(CRMQT.c4c_quote_id)+str(sess.sess)
		SAQSAP = "SAQSAP_BKP_1"+str(CRMQT.c4c_quote_id)+str(sess.sess)
		SAQSAE = "SAQSAE_BKP_1"+str(CRMQT.c4c_quote_id)+str(sess.sess)
		
		SAQSCO_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQSCO)+"'' ) BEGIN DROP TABLE "+str(SAQSCO)+" END  ' ")
		
		SAQIEN_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQIEN)+"'' ) BEGIN DROP TABLE "+str(SAQIEN)+" END  ' ")
		
		SAQSCA_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQSCA)+"'' ) BEGIN DROP TABLE "+str(SAQSCA)+" END  ' ")

		SAQSAP_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQSAP)+"'' ) BEGIN DROP TABLE "+str(SAQSAP)+" END  ' ")
		
		SAQSAE_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQSAE)+"'' ) BEGIN DROP TABLE "+str(SAQSAE)+" END  ' ")
		
		Log.Info("QTPOSTPRSM ERROR---->:" + str(sys.exc_info()[1]))
		Log.Info("QTPOSTPRSM ERROR LINE NO---->:" + str(sys.exc_info()[-1].tb_lineno))
		ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "400", "Message": str(sys.exc_info()[1])}]})
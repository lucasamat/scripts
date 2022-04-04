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
		SAQGPA = "SAQGPA_BKP_1"+str(CRMQT.c4c_quote_id)+str(sess.sess)
		SAQGPM = "SAQGPM_BKP_1"+str(CRMQT.c4c_quote_id)+str(sess.sess)
		
		SAQSCO_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQSCO)+"'' ) BEGIN DROP TABLE "+str(SAQSCO)+" END  ' ")
		
		SAQIEN_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQIEN)+"'' ) BEGIN DROP TABLE "+str(SAQIEN)+" END  ' ")
		
		SAQSCA_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQSCA)+"'' ) BEGIN DROP TABLE "+str(SAQSCA)+" END  ' ")

		SAQSAP_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQSAP)+"'' ) BEGIN DROP TABLE "+str(SAQSAP)+" END  ' ")
		
		SAQSAE_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQSAE)+"'' ) BEGIN DROP TABLE "+str(SAQSAE)+" END  ' ")
		
		SAQGPA_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQGPA)+"'' ) BEGIN DROP TABLE "+str(SAQGPA)+" END  ' ")
		
		SAQGPM_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQGPM)+"'' ) BEGIN DROP TABLE "+str(SAQGPM)+" END  ' ")
		
		SAQSCO_SEL = SqlHelper.GetFirst("sp_executesql @T=N'select DISTINCT A.QUOTE_ID,D.EQUIPMENT_ID,CASE WHEN ISNULL(INWRTY,''FALSE'') = ''FALSE'' THEN A.SERVICE_ID WHEN ISNULL(INWRTY,''FALSE'') = ''TRUE'' THEN REPLACE(A.SERVICE_ID,''W'','''') ELSE A.SERVICE_ID END SERVICE_ID,B.SALESORG_ID,C.REGION,A.QTEREV_ID,E.CONTRACT_VALID_FROM,E.CONTRACT_VALID_TO,C.ACCOUNT_NAME,(SELECT DISTINCT FABLOCATION_NAME FROM MAEQUP(NOLOCK) WHERE MAEQUP.EQUIPMENT_ID = A.EQUIPMENT_ID) AS FAB_NAME,(SELECT DISTINCT VALDRV_WAFERNODE FROM MAEQUP(NOLOCK) WHERE MAEQUP.EQUIPMENT_ID = A.EQUIPMENT_ID) AS TECH_NODE_RANGE,D.LINE,A.CMLAB_ENT,A.CNSMBL_ENT, A.CNTCVG_ENT,A.NCNSMB_ENT,A.PMEVNT_ENT,A.PMLAB_ENT,A.PRMKPI_ENT,A.WETCLN_ENT,QTETYP AS QUOTE_TYPE,E.PM_ID,E.GOT_CODE,E.GREENBOOK,E.PROCESS_TYPE,E.DEVICE_NODE,E.MNTEVT_LEVEL,E.KIT_ID,CNTYER AS CONTRACT_YEAR INTO "+str(SAQSCO)+" from SAQICO(NOLOCK) A JOIN SAQTRV B(NOLOCK) ON A.QUOTE_ID = B.QUOTE_ID AND A.QTEREV_ID = B.QTEREV_ID JOIN SAQTMT C(NOLOCK) ON B.QUOTE_ID = C.QUOTE_ID AND B.QTEREV_ID = C.QTEREV_ID JOIN SAQRIO D(NOLOCK) ON A.QUOTE_ID = D.QUOTE_ID AND A.QTEREV_ID = D.QTEREV_ID AND A.LINE = D.LINE JOIN SAQRIT(NOLOCK) E ON A.QUOTE_ID = E.QUOTE_ID AND A.QTEREV_ID = E.QTEREV_ID AND A.LINE = E.LINE WHERE A.QUOTE_ID = ''"+str(Qt_id)+"'' AND A.QTEREV_ID=''"+str(REVISION_ID) +"'' AND CASE WHEN ISNULL(INWRTY,''FALSE'') = ''FALSE'' THEN A.SERVICE_ID WHEN ISNULL(INWRTY,''FALSE'') = ''TRUE'' THEN REPLACE(A.SERVICE_ID,''W'','''') ELSE A.SERVICE_ID END IN (SELECT DISTINCT SERVICE_ID FROM PRSPRV(NOLOCK) WHERE ISNULL(SSCM_COST,''FALSE'')=''TRUE'' ) AND ISNULL(A.STATUS,'''')=''''  ' ")
		
		SAQSCA_SEL = SqlHelper.GetFirst("sp_executesql @T=N'select DISTINCT A.QUOTE_ID,A.EQUIPMENT_ID,REPLACE(A.SERVICE_ID,''W'','''') AS SERVICE_ID,A.ASSEMBLY_ID,CONVERT(VARCHAR(100),NULL) AS COVERAGE,CONVERT(VARCHAR(100),NULL) AS WETCLEAN,CONVERT(VARCHAR(100),NULL) AS PERFGUARANTEE,CONVERT(VARCHAR(100),NULL) AS PMLABOR,CONVERT(VARCHAR(100),NULL) AS CMLABOR,CONVERT(VARCHAR(100),NULL) AS PM_EVENTS,CONVERT(VARCHAR(100),NULL) AS CONSUMABLE,CONVERT(VARCHAR(100),NULL) AS NON_CONSUMABLE,A.QTEREV_ID,A.LINE INTO "+str(SAQSCA)+" from SAQICA(NOLOCK) A JOIN SAQICO (NOLOCK)B ON A.QUOTE_ID = B.QUOTE_ID AND A.QTEREV_ID = B.QTEREV_ID AND A.LINE= B.LINE AND A.EQUIPMENT_ID = B.EQUIPMENT_ID WHERE A.QUOTE_ID = ''"+str(Qt_id)+"'' AND A.QTEREV_ID=''"+str(REVISION_ID) +"'' AND REPLACE(A.SERVICE_ID,''W'','''') IN (SELECT DISTINCT SERVICE_ID FROM PRSPRV(NOLOCK) WHERE ISNULL(SSCM_COST,''FALSE'')=''TRUE'' ) AND ISNULL(B.STATUS,'''')='''' ' ")
		
		SAQGPA_SEL = SqlHelper.GetFirst("sp_executesql @T=N'select DISTINCT QUOTE_ID,EQUIPMENT_ID,REPLACE(SERVICE_ID,''W'','''') AS SERVICE_ID,ASSEMBLY_ID,PM_FREQUENCY, PM_ID,GOT_CODE,GREENBOOK,PROCESS_TYPE,DEVICE_NODE,CONVERT(VARCHAR(100),NULL) AS COVERAGE,CONVERT(VARCHAR(100),NULL) AS WETCLEAN,CONVERT(VARCHAR(100),NULL) AS PERFGUARANTEE,CONVERT(VARCHAR(100),NULL) AS PMLABOR,CONVERT(VARCHAR(100),NULL) AS CMLABOR,CONVERT(VARCHAR(100),NULL) AS PM_EVENTS,CONVERT(VARCHAR(100),NULL) AS CONSUMABLE,CONVERT(VARCHAR(100),NULL) AS NON_CONSUMABLE,QTEREV_ID,KIT_ID INTO "+str(SAQGPA)+" from SAQGPA(NOLOCK) WHERE QUOTE_ID = ''"+str(Qt_id)+"'' AND QTEREV_ID=''"+str(REVISION_ID) +"'' AND REPLACE(SERVICE_ID,''W'','''') IN (SELECT DISTINCT SERVICE_ID FROM PRSPRV(NOLOCK) WHERE ISNULL(SSCM_COST,''FALSE'')=''TRUE''  )' ")
		
		SAQGPM_SEL = SqlHelper.GetFirst("sp_executesql @T=N'select DISTINCT QUOTE_ID,REPLACE(SERVICE_ID,''W'','''') AS SERVICE_ID, PM_ID,GOT_CODE,GREENBOOK,PROCESS_TYPE,DEVICE_NODE,QTEREV_ID,MNTEVT_LEVEL,KIT_ID INTO "+str(SAQGPM)+" from SAQGPM(NOLOCK) WHERE QUOTE_ID = ''"+str(Qt_id)+"'' AND QTEREV_ID=''"+str(REVISION_ID) +"'' AND REPLACE(SERVICE_ID,''W'','''') IN (SELECT DISTINCT SERVICE_ID FROM PRSPRV(NOLOCK) WHERE ISNULL(SSCM_COST,''FALSE'')=''TRUE''  )' ")
				
		#Contract Coverage
		S = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET COVERAGE=CNTCVG_ENT FROM  "+str(SAQSCA)+" A(NOLOCK) JOIN "+str(SAQSCO)+" B(NOLOCK) ON A.QUOTE_ID = B.QUOTE_ID AND A.QTEREV_ID = B.QTEREV_ID AND A.LINE = B.LINE AND A.EQUIPMENT_ID = B.EQUIPMENT_ID '")
		
		S = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET COVERAGE=CNTCVG_ENT FROM  "+str(SAQGPA)+" A(NOLOCK) JOIN "+str(SAQSCO)+" B(NOLOCK) ON A.QUOTE_ID = B.QUOTE_ID AND A.QTEREV_ID = B.QTEREV_ID AND A.GOT_CODE = B.GOT_CODE AND ISNULL(A.PROCESS_TYPE,'''') = ISNULL(B.PROCESS_TYPE,'''') AND ISNULL(A.DEVICE_NODE,'''') = ISNULL(B.DEVICE_NODE,'''')  '")
		
		#Wet Cleans Labor
		S = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET WETCLEAN=WETCLN_ENT FROM  "+str(SAQSCA)+" A(NOLOCK) JOIN "+str(SAQSCO)+" B(NOLOCK) ON A.QUOTE_ID = B.QUOTE_ID AND A.QTEREV_ID = B.QTEREV_ID AND A.LINE = B.LINE  '")
		
		S = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET WETCLEAN=WETCLN_ENT FROM  "+str(SAQGPA)+" A(NOLOCK) JOIN "+str(SAQSCO)+" B(NOLOCK) ON A.QUOTE_ID = B.QUOTE_ID AND A.QTEREV_ID = B.QTEREV_ID AND A.GOT_CODE = B.GOT_CODE AND ISNULL(A.PROCESS_TYPE,'''') = ISNULL(B.PROCESS_TYPE,'''') AND ISNULL(A.DEVICE_NODE,'''') = ISNULL(B.DEVICE_NODE,'''')  '")
		
		#Preventive Maintenance Labor
		S = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET PMLABOR=PMLAB_ENT FROM  "+str(SAQSCA)+" A(NOLOCK) JOIN "+str(SAQSCO)+" B(NOLOCK) ON A.QUOTE_ID = B.QUOTE_ID AND A.QTEREV_ID = B.QTEREV_ID AND A.LINE = B.LINE  '")
		
		S = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET PMLABOR=PMLAB_ENT FROM  "+str(SAQGPA)+" A(NOLOCK) JOIN "+str(SAQSCO)+" B(NOLOCK) ON A.QUOTE_ID = B.QUOTE_ID AND A.QTEREV_ID = B.QTEREV_ID  AND A.GOT_CODE = B.GOT_CODE AND ISNULL(A.PROCESS_TYPE,'''') = ISNULL(B.PROCESS_TYPE,'''') AND ISNULL(A.DEVICE_NODE,'''') = ISNULL(B.DEVICE_NODE,'''')  '")
		
		#Corrective Maintenance Labor
		S = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET CMLABOR=CMLAB_ENT FROM  "+str(SAQSCA)+" A(NOLOCK) JOIN "+str(SAQSCO)+" B(NOLOCK) ON A.QUOTE_ID = B.QUOTE_ID AND A.QTEREV_ID = B.QTEREV_ID AND A.LINE = B.LINE '")
		
		S = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET CMLABOR=CMLAB_ENT FROM  "+str(SAQGPA)+" A(NOLOCK) JOIN "+str(SAQSCO)+" B(NOLOCK) ON A.QUOTE_ID = B.QUOTE_ID AND A.QTEREV_ID = B.QTEREV_ID AND A.GOT_CODE = B.GOT_CODE AND ISNULL(A.PROCESS_TYPE,'''') = ISNULL(B.PROCESS_TYPE,'''') AND ISNULL(A.DEVICE_NODE,'''') = ISNULL(B.DEVICE_NODE,'''')  '")
		
		#Primary KPI. Perf Guarantee
		S = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET PERFGUARANTEE=PRMKPI_ENT FROM  "+str(SAQSCA)+" A(NOLOCK) JOIN "+str(SAQSCO)+" B(NOLOCK) ON A.QUOTE_ID = B.QUOTE_ID AND A.QTEREV_ID = B.QTEREV_ID AND A.LINE = B.LINE  '")
		
		S = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET PERFGUARANTEE=PRMKPI_ENT FROM  "+str(SAQGPA)+" A(NOLOCK) JOIN "+str(SAQSCO)+" B(NOLOCK) ON A.QUOTE_ID = B.QUOTE_ID AND A.QTEREV_ID = B.QTEREV_ID  AND A.GOT_CODE = B.GOT_CODE AND ISNULL(A.PROCESS_TYPE,'''') = ISNULL(B.PROCESS_TYPE,'''') AND ISNULL(A.DEVICE_NODE,'''') = ISNULL(B.DEVICE_NODE,'''')  '")
		
		#PM Event
		S = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET PM_EVENTS=PMEVNT_ENT FROM  "+str(SAQSCA)+" A(NOLOCK) JOIN "+str(SAQSCO)+" B(NOLOCK) ON A.QUOTE_ID = B.QUOTE_ID AND A.QTEREV_ID = B.QTEREV_ID AND A.LINE = B.LINE  '")
		
		S = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET PM_EVENTS=PMEVNT_ENT FROM  "+str(SAQGPA)+" A(NOLOCK) JOIN "+str(SAQSCO)+" B(NOLOCK) ON A.QUOTE_ID = B.QUOTE_ID AND A.QTEREV_ID = B.QTEREV_ID AND A.GOT_CODE = B.GOT_CODE AND ISNULL(A.PROCESS_TYPE,'''') = ISNULL(B.PROCESS_TYPE,'''') AND ISNULL(A.DEVICE_NODE,'''') = ISNULL(B.DEVICE_NODE,'''')  '")
		
		#Consumable
		S = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET CONSUMABLE=CNSMBL_ENT FROM  "+str(SAQSCA)+" A(NOLOCK) JOIN "+str(SAQSCO)+" B(NOLOCK) ON A.QUOTE_ID = B.QUOTE_ID AND A.QTEREV_ID = B.QTEREV_ID AND A.LINE = B.LINE  '")
		
		S = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET CONSUMABLE=CNSMBL_ENT FROM  "+str(SAQGPA)+" A(NOLOCK) JOIN "+str(SAQSCO)+" B(NOLOCK) ON A.QUOTE_ID = B.QUOTE_ID AND A.QTEREV_ID = B.QTEREV_ID  AND A.GOT_CODE = B.GOT_CODE AND ISNULL(A.PROCESS_TYPE,'''') = ISNULL(B.PROCESS_TYPE,'''') AND ISNULL(A.DEVICE_NODE,'''') = ISNULL(B.DEVICE_NODE,'''')  '")
		
		#Non Consumable
		S = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET NON_CONSUMABLE=NCNSMB_ENT FROM  "+str(SAQSCA)+" A(NOLOCK) JOIN "+str(SAQSCO)+" B(NOLOCK) ON A.QUOTE_ID = B.QUOTE_ID AND A.QTEREV_ID = B.QTEREV_ID AND A.LINE = B.LINE  '")
		
		S = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET NON_CONSUMABLE=NCNSMB_ENT FROM  "+str(SAQGPA)+" A(NOLOCK) JOIN "+str(SAQSCO)+" B(NOLOCK) ON A.QUOTE_ID = B.QUOTE_ID AND A.QTEREV_ID = B.QTEREV_ID AND A.GOT_CODE = B.GOT_CODE AND ISNULL(A.PROCESS_TYPE,'''') = ISNULL(B.PROCESS_TYPE,'''') AND ISNULL(A.DEVICE_NODE,'''') = ISNULL(B.DEVICE_NODE,'''')  '")
		
		SAQSAP_SEL = SqlHelper.GetFirst("sp_executesql @T=N'select QUOTE_ID,EQUIPMENT_ID,REPLACE(SERVICE_ID,''W'','''') AS SERVICE_ID,ASSEMBLY_ID,PM_FREQUENCY, PM_ID INTO "+str(SAQSAP)+" from SAQSAP(NOLOCK) WHERE QUOTE_ID = ''"+str(Qt_id)+"'' AND QTEREV_ID=''"+str(REVISION_ID) +"'' AND REPLACE(SERVICE_ID,''W'','''') IN (SELECT DISTINCT SERVICE_ID FROM PRSPRV(NOLOCK) WHERE ISNULL(SSCM_COST,''FALSE'')=''TRUE''  )' ")
		
		SAQSAP_SEL = SqlHelper.GetFirst("sp_executesql @T=N'DELETE A FROM "+str(SAQSCO)+" A JOIN "+str(SAQSCA)+" B ON A.QUOTE_ID = B.QUOTE_ID AND A.QTEREV_ID = B.QTEREV_ID AND A.SERVICE_ID = B.SERVICE_ID WHERE A.SERVICE_ID = ''Z0100'' AND ISNULL(B.CONSUMABLE,'''') <> ''INCLUDED'' AND  ISNULL(B.NON_CONSUMABLE,'''') <> ''INCLUDED''  ' ")
		
		SAQSAP_SEL = SqlHelper.GetFirst("sp_executesql @T=N'DELETE A FROM "+str(SAQSCO)+" A JOIN "+str(SAQGPA)+" B ON A.QUOTE_ID = B.QUOTE_ID AND A.QTEREV_ID = B.QTEREV_ID AND A.SERVICE_ID = B.SERVICE_ID WHERE A.SERVICE_ID = ''Z0100'' AND ISNULL(B.CONSUMABLE,'''') <> ''INCLUDED'' AND  ISNULL(B.NON_CONSUMABLE,'''') <> ''INCLUDED''  ' ")
		
		table = SqlHelper.GetFirst(
			"SELECT replace ('{\"QTQICA\": ['+STUFF((SELECT ','+ JSON FROM (SELECT DISTINCT '{\"SESSION_ID\" : \"'+SESSION_ID+'\",\"QUOTE_ID\" : \"'+QUOTE_ID+'\",\"EQUIPMENT_ID\" : \"'+EQUIPMENT_ID+'\",\"CONTRACT_VALID_FROM\" : \"'+CONTRACT_VALID_FROM+'\",\"CONTRACT_VALID_TO\" : \"'+CONTRACT_VALID_TO+'\",\"SERVICE_ID\" : \"'+SERVICE_ID+'\",\"SALESORG_ID\" : \"'+SALESORG_ID+'\",\"REGION\" : \"'+REGION+'\",\"ASSEMBLY_ID\" : \"'+ASSEMBLY_ID+'\",\"LABOR_COVERAGE\" : \"'+LABOR_COVERAGE+'\",\"PREVENTIVE_MAINTENANCE\" : \"'+PREVENTIVE_MAINTENANCE+'\",\"CORRECTIVE_MAINTENANCE\" : \"'+CORRECTIVE_MAINTENANCE+'\",\"PERFORMANCE_GUARANTEE\" : \"'+PERFORMANCE_GUARANTEE+'\",\"WET_CLEAN\" : \"'+WET_CLEAN+'\",\"PM_EVENTS\" : \"'+PM_EVENTS+'\",\"ACCOUNT_NAME\" : \"'+ACCOUNT_NAME+'\",\"FAB_NAME\" : \"'+FAB_NAME+'\",\"CONSUMABLE\" : \"'+CONSUMABLE+'\",\"CONTRACT_YEAR\" : \"'+CONTRACT_YEAR+'\",\"LINE\" : \"'+LINE+'\",\"NON_CONSUMABLE\" : \"'+NON_CONSUMABLE+'\",\"TECH_NODE_RANGE\" : \"'+TECH_NODE_RANGE+'\",\"PM_NAME\" : \"'+PM_NAME+'\",\"PM_PER_YEAR\" : \"'+PM_PER_YEAR+'\"}' AS JSON from (SELECT DISTINCT  "+str(timestamp_sessionid)+" as SESSION_ID, B.QUOTE_ID+'-'+ CONVERT(VARCHAR,B.QTEREV_ID) AS QUOTE_ID,ISNULL(SALESORG_ID,'') AS SALESORG_ID,ISNULL(REGION,'') AS REGION, ISNULL(B.EQUIPMENT_ID,'') AS EQUIPMENT_ID,ISNULL(B.SERVICE_ID,'') AS SERVICE_ID,ISNULL(A.ASSEMBLY_ID,'') AS ASSEMBLY_ID,ISNULL( COVERAGE,'' ) AS LABOR_COVERAGE,ISNULL(PMLABOR,'') AS PREVENTIVE_MAINTENANCE,ISNULL(CMLABOR,'') AS CORRECTIVE_MAINTENANCE,ISNULL(PERFGUARANTEE,'') AS PERFORMANCE_GUARANTEE,ISNULL(WETCLEAN,'') AS WET_CLEAN,ISNULL(PM_EVENTS,'') AS PM_EVENTS, ISNULL(C.PM_ID,'') AS PM_NAME,ISNULL(CONVERT(VARCHAR(50),PM_FREQUENCY),'') AS PM_PER_YEAR,CONVERT(VARCHAR(11),B.CONTRACT_VALID_FROM,121) AS CONTRACT_VALID_FROM,CONVERT(VARCHAR(11),B.CONTRACT_VALID_TO,121) AS CONTRACT_VALID_TO,ISNULL(CONSUMABLE,'') AS CONSUMABLE,ISNULL(NON_CONSUMABLE,'') AS NON_CONSUMABLE,ISNULL(ACCOUNT_NAME,'') AS ACCOUNT_NAME,ISNULL(FAB_NAME,'') AS FAB_NAME,ISNULL(TECH_NODE_RANGE,'') AS TECH_NODE_RANGE,convert(varchar,B.LINE) as LINE,CONTRACT_YEAR FROM "+str(SAQSCO)+" B(NOLOCK) JOIN "+str(SAQSCA)+"(NOLOCK) A ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID= B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID LEFT JOIN "+str(SAQSAP)+" C(NOLOCK) ON A.QUOTE_ID = C.QUOTE_ID AND A.SERVICE_ID = C.SERVICE_ID AND A.EQUIPMENT_ID = C.EQUIPMENT_ID AND A.ASSEMBLY_ID=C.ASSEMBLY_ID WHERE B.QUOTE_ID = '"+str(Qt_id)+"' AND ISNULL(QUOTE_TYPE,'TOOL BASED')='TOOL BASED'  AND B.SERVICE_ID<>'Z0100' ) t 	) A FOR XML PATH ('')  ), 1, 1, '')+']}','amp;#','#') AS RESULT "
		)
		
		table_Z0100 = SqlHelper.GetFirst(
			"SELECT replace ('{\"QTQICA\": ['+STUFF((SELECT ','+ JSON FROM (SELECT DISTINCT '{\"SESSION_ID\" : \"'+SESSION_ID+'\",\"QUOTE_ID\" : \"'+QUOTE_ID+'\",\"EQUIPMENT_ID\" : \"'+EQUIPMENT_ID+'\",\"CONTRACT_VALID_FROM\" : \"'+CONTRACT_VALID_FROM+'\",\"CONTRACT_VALID_TO\" : \"'+CONTRACT_VALID_TO+'\",\"SERVICE_ID\" : \"'+SERVICE_ID+'\",\"SALESORG_ID\" : \"'+SALESORG_ID+'\",\"REGION\" : \"'+REGION+'\",\"ASSEMBLY_ID\" : \"'+ASSEMBLY_ID+'\",\"LABOR_COVERAGE\" : \"'+LABOR_COVERAGE+'\",\"PREVENTIVE_MAINTENANCE\" : \"'+PREVENTIVE_MAINTENANCE+'\",\"CORRECTIVE_MAINTENANCE\" : \"'+CORRECTIVE_MAINTENANCE+'\",\"PERFORMANCE_GUARANTEE\" : \"'+PERFORMANCE_GUARANTEE+'\",\"WET_CLEAN\" : \"'+WET_CLEAN+'\",\"PM_EVENTS\" : \"'+PM_EVENTS+'\",\"ACCOUNT_NAME\" : \"'+ACCOUNT_NAME+'\",\"FAB_NAME\" : \"'+FAB_NAME+'\",\"CONSUMABLE\" : \"'+CONSUMABLE+'\",\"CONTRACT_YEAR\" : \"'+CONTRACT_YEAR+'\",\"LINE\" : \"'+LINE+'\",\"NON_CONSUMABLE\" : \"'+NON_CONSUMABLE+'\",\"TECH_NODE_RANGE\" : \"'+TECH_NODE_RANGE+'\",\"PM_NAME\" : \"'+PM_NAME+'\",\"PM_PER_YEAR\" : \"'+PM_PER_YEAR+'\"}' AS JSON from (SELECT DISTINCT  "+str(timestamp_sessionid)+"+'Z0100' as SESSION_ID, B.QUOTE_ID+'-'+ CONVERT(VARCHAR,B.QTEREV_ID) AS QUOTE_ID,ISNULL(SALESORG_ID,'') AS SALESORG_ID,ISNULL(REGION,'') AS REGION, ISNULL(B.EQUIPMENT_ID,'') AS EQUIPMENT_ID,ISNULL(B.SERVICE_ID,'') AS SERVICE_ID,ISNULL(A.ASSEMBLY_ID,'') AS ASSEMBLY_ID,ISNULL( COVERAGE,'' ) AS LABOR_COVERAGE,ISNULL(PMLABOR,'') AS PREVENTIVE_MAINTENANCE,ISNULL(CMLABOR,'') AS CORRECTIVE_MAINTENANCE,ISNULL(PERFGUARANTEE,'') AS PERFORMANCE_GUARANTEE,ISNULL(WETCLEAN,'') AS WET_CLEAN,ISNULL(PM_EVENTS,'') AS PM_EVENTS, ISNULL(C.PM_ID,'') AS PM_NAME,ISNULL(CONVERT(VARCHAR(50),PM_FREQUENCY),'') AS PM_PER_YEAR,CONVERT(VARCHAR(11),B.CONTRACT_VALID_FROM,121) AS CONTRACT_VALID_FROM,CONVERT(VARCHAR(11),B.CONTRACT_VALID_TO,121) AS CONTRACT_VALID_TO,ISNULL(CONSUMABLE,'') AS CONSUMABLE,ISNULL(NON_CONSUMABLE,'') AS NON_CONSUMABLE,ISNULL(ACCOUNT_NAME,'') AS ACCOUNT_NAME,ISNULL(FAB_NAME,'') AS FAB_NAME,ISNULL(TECH_NODE_RANGE,'') AS TECH_NODE_RANGE,convert(varchar,B.LINE) as LINE,CONTRACT_YEAR FROM "+str(SAQSCO)+" B(NOLOCK) JOIN "+str(SAQSCA)+"(NOLOCK) A ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID= B.SERVICE_ID AND A.EQUIPMENT_ID = B.EQUIPMENT_ID LEFT JOIN "+str(SAQSAP)+" C(NOLOCK) ON A.QUOTE_ID = C.QUOTE_ID AND A.SERVICE_ID = C.SERVICE_ID AND A.EQUIPMENT_ID = C.EQUIPMENT_ID AND A.ASSEMBLY_ID=C.ASSEMBLY_ID WHERE B.QUOTE_ID = '"+str(Qt_id)+"' AND ISNULL(QUOTE_TYPE,'TOOL BASED')IN( 'TOOL BASED' )  AND B.SERVICE_ID='Z0100' ) t 	) A FOR XML PATH ('')  ), 1, 1, '')+']}','amp;#','#') AS RESULT "
		)
		
		PMSA_EVENT = SqlHelper.GetFirst(
			"SELECT replace ('{\"QTQICA\": ['+STUFF((SELECT ','+ JSON FROM (SELECT DISTINCT '{\"SESSION_ID\" : \"'+SESSION_ID+'\",\"QUOTE_ID\" : \"'+QUOTE_ID+'\",\"EQUIPMENT_ID\" : \"'+EQUIPMENT_ID+'\",\"CONTRACT_VALID_FROM\" : \"'+CONTRACT_VALID_FROM+'\",\"CONTRACT_VALID_TO\" : \"'+CONTRACT_VALID_TO+'\",\"SERVICE_ID\" : \"'+SERVICE_ID+'\",\"SALESORG_ID\" : \"'+SALESORG_ID+'\",\"REGION\" : \"'+REGION+'\",\"ASSEMBLY_ID\" : \"'+ASSEMBLY_ID+'\",\"LABOR_COVERAGE\" : \"'+LABOR_COVERAGE+'\",\"PREVENTIVE_MAINTENANCE\" : \"'+PREVENTIVE_MAINTENANCE+'\",\"CORRECTIVE_MAINTENANCE\" : \"'+CORRECTIVE_MAINTENANCE+'\",\"PERFORMANCE_GUARANTEE\" : \"'+PERFORMANCE_GUARANTEE+'\",\"WET_CLEAN\" : \"'+WET_CLEAN+'\",\"PM_EVENTS\" : \"'+PM_EVENTS+'\",\"ACCOUNT_NAME\" : \"'+ACCOUNT_NAME+'\",\"FAB_NAME\" : \"'+FAB_NAME+'\",\"CONSUMABLES\" : \"'+CONSUMABLE+'\",\"CONTRACT_YEAR\" : \"'+CONTRACT_YEAR+'\",\"LINE\" : \"'+LINE+'\",\"NON_CONSUMABLE\" : \"'+NON_CONSUMABLE+'\",\"TECH_NODE_RANGE\" : \"'+TECH_NODE_RANGE+'\",\"PM_NAME\" : \"'+PM_NAME+'\",\"PM_PER_YEAR\" : \"'+PM_PER_YEAR+'\"}' AS JSON from (SELECT DISTINCT  "+str(timestamp_sessionid)+" + 'Flex' as SESSION_ID, B.QUOTE_ID+'-'+ CONVERT(VARCHAR,B.QTEREV_ID) AS QUOTE_ID,ISNULL(SALESORG_ID,'') AS SALESORG_ID,ISNULL(REGION,'') AS REGION, ISNULL(B.EQUIPMENT_ID,'') AS EQUIPMENT_ID,ISNULL(B.SERVICE_ID,'') AS SERVICE_ID,ISNULL(C.ASSEMBLY_ID,'') AS ASSEMBLY_ID,ISNULL( COVERAGE,'' ) AS LABOR_COVERAGE,ISNULL(PMLABOR,'') AS PREVENTIVE_MAINTENANCE,ISNULL(CMLABOR,'') AS CORRECTIVE_MAINTENANCE,ISNULL(PERFGUARANTEE,'') AS PERFORMANCE_GUARANTEE,ISNULL(WETCLEAN,'') AS WET_CLEAN,ISNULL(PM_EVENTS,'') AS PM_EVENTS, ISNULL(C.PM_ID,'') AS PM_NAME,ISNULL(CONVERT(VARCHAR(50),C.PM_FREQUENCY),'') AS PM_PER_YEAR,CONVERT(VARCHAR(11),B.CONTRACT_VALID_FROM,121) AS CONTRACT_VALID_FROM,CONVERT(VARCHAR(11),B.CONTRACT_VALID_TO,121) AS CONTRACT_VALID_TO,ISNULL(CONSUMABLE,'') AS CONSUMABLE,ISNULL(NON_CONSUMABLE,'') AS NON_CONSUMABLE,ISNULL(ACCOUNT_NAME,'') AS ACCOUNT_NAME,ISNULL(FAB_NAME,'') AS FAB_NAME,ISNULL(TECH_NODE_RANGE,'') AS TECH_NODE_RANGE,convert(varchar,B.LINE) as LINE,CONTRACT_YEAR FROM "+str(SAQSCO)+" B(NOLOCK) JOIN "+str(SAQGPM)+" SAQGPM ON B.QUOTE_ID = SAQGPM.QUOTE_ID AND B.QTEREV_ID = SAQGPM.QTEREV_ID AND B.SERVICE_ID = SAQGPM.SERVICE_ID AND B.GOT_CODE = SAQGPM.GOT_CODE  AND ISNULL(B.PROCESS_TYPE,'') = ISNULL(SAQGPM.PROCESS_TYPE,'') AND ISNULL(B.DEVICE_NODE,'') = ISNULL(SAQGPM.DEVICE_NODE,'') AND B.MNTEVT_LEVEL = SAQGPM.MNTEVT_LEVEL AND CASE WHEN ISNULL(B.PM_ID,'')='' THEN SAQGPM.PM_ID ELSE B.PM_ID END = SAQGPM.PM_ID JOIN "+str(SAQGPA)+" C(NOLOCK) ON B.QUOTE_ID = C.QUOTE_ID AND B.SERVICE_ID = C.SERVICE_ID AND B.GOT_CODE = C.GOT_CODE  AND ISNULL(B.PROCESS_TYPE,'') = ISNULL(C.PROCESS_TYPE,'') AND ISNULL(B.DEVICE_NODE,'') = ISNULL(C.DEVICE_NODE,'') AND SAQGPM.PM_ID = C.PM_ID WHERE B.QUOTE_ID = '"+str(Qt_id)+"' AND ISNULL(QUOTE_TYPE,'TOOL BASED') IN ('EVENT BASED', 'FLEX EVENT BASED') ) t 	) A FOR XML PATH ('')  ), 1, 1, '')+']}','amp;#','#') AS RESULT "
		)
		
		TKM_EVENT = SqlHelper.GetFirst(
			"SELECT replace ('{\"QTQICA\": ['+STUFF((SELECT ','+ JSON FROM (SELECT DISTINCT '{\"SESSION_ID\" : \"'+SESSION_ID+'\",\"QUOTE_ID\" : \"'+QUOTE_ID+'\",\"EQUIPMENT_ID\" : \"'+EQUIPMENT_ID+'\",\"CONTRACT_VALID_FROM\" : \"'+CONTRACT_VALID_FROM+'\",\"CONTRACT_VALID_TO\" : \"'+CONTRACT_VALID_TO+'\",\"SERVICE_ID\" : \"'+SERVICE_ID+'\",\"SALESORG_ID\" : \"'+SALESORG_ID+'\",\"REGION\" : \"'+REGION+'\",\"ASSEMBLY_ID\" : \"'+ASSEMBLY_ID+'\",\"LABOR_COVERAGE\" : \"'+LABOR_COVERAGE+'\",\"PREVENTIVE_MAINTENANCE\" : \"'+PREVENTIVE_MAINTENANCE+'\",\"CORRECTIVE_MAINTENANCE\" : \"'+CORRECTIVE_MAINTENANCE+'\",\"PERFORMANCE_GUARANTEE\" : \"'+PERFORMANCE_GUARANTEE+'\",\"WET_CLEAN\" : \"'+WET_CLEAN+'\",\"PM_EVENTS\" : \"'+PM_EVENTS+'\",\"ACCOUNT_NAME\" : \"'+ACCOUNT_NAME+'\",\"FAB_NAME\" : \"'+FAB_NAME+'\",\"CONSUMABLES\" : \"'+CONSUMABLE+'\",\"CONTRACT_YEAR\" : \"'+CONTRACT_YEAR+'\",\"LINE\" : \"'+LINE+'\",\"KIT_ID\" : \"'+KIT_ID+'\",\"NON_CONSUMABLE\" : \"'+NON_CONSUMABLE+'\",\"TECH_NODE_RANGE\" : \"'+TECH_NODE_RANGE+'\",\"PM_NAME\" : \"'+PM_NAME+'\",\"PM_PER_YEAR\" : \"'+PM_PER_YEAR+'\"}' AS JSON from (SELECT DISTINCT  "+str(timestamp_sessionid)+" + 'TKMKIT' as SESSION_ID, B.QUOTE_ID+'-'+ CONVERT(VARCHAR,B.QTEREV_ID) AS QUOTE_ID,ISNULL(SALESORG_ID,'') AS SALESORG_ID,ISNULL(REGION,'') AS REGION, ISNULL(B.EQUIPMENT_ID,'') AS EQUIPMENT_ID,ISNULL(B.SERVICE_ID,'') AS SERVICE_ID,ISNULL(C.ASSEMBLY_ID,'') AS ASSEMBLY_ID,ISNULL( COVERAGE,'' ) AS LABOR_COVERAGE,ISNULL(PMLABOR,'') AS PREVENTIVE_MAINTENANCE,ISNULL(CMLABOR,'') AS CORRECTIVE_MAINTENANCE,ISNULL(PERFGUARANTEE,'') AS PERFORMANCE_GUARANTEE,ISNULL(WETCLEAN,'') AS WET_CLEAN,ISNULL(PM_EVENTS,'') AS PM_EVENTS, ISNULL(C.PM_ID,'') AS PM_NAME,ISNULL(CONVERT(VARCHAR(50),C.PM_FREQUENCY),'') AS PM_PER_YEAR,CONVERT(VARCHAR(11),B.CONTRACT_VALID_FROM,121) AS CONTRACT_VALID_FROM,CONVERT(VARCHAR(11),B.CONTRACT_VALID_TO,121) AS CONTRACT_VALID_TO,ISNULL(CONSUMABLE,'') AS CONSUMABLE,ISNULL(NON_CONSUMABLE,'') AS NON_CONSUMABLE,ISNULL(ACCOUNT_NAME,'') AS ACCOUNT_NAME,ISNULL(FAB_NAME,'') AS FAB_NAME,ISNULL(TECH_NODE_RANGE,'') AS TECH_NODE_RANGE,convert(varchar,B.LINE) as LINE,ISNULL(CONVERT(VARCHAR,B.KIT_ID),'') AS KIT_ID,CONTRACT_YEAR FROM "+str(SAQSCO)+" B(NOLOCK) JOIN "+str(SAQGPM)+" SAQGPM ON B.QUOTE_ID = SAQGPM.QUOTE_ID AND B.QTEREV_ID = SAQGPM.QTEREV_ID AND B.SERVICE_ID = SAQGPM.SERVICE_ID AND B.GOT_CODE = SAQGPM.GOT_CODE  AND ISNULL(B.PROCESS_TYPE,'') = ISNULL(SAQGPM.PROCESS_TYPE,'') AND ISNULL(B.DEVICE_NODE,'') = ISNULL(SAQGPM.DEVICE_NODE,'') AND CASE WHEN ISNULL(B.KIT_ID,'')='' THEN SAQGPM.KIT_ID ELSE B.KIT_ID END = SAQGPM.KIT_ID JOIN "+str(SAQGPA)+" C(NOLOCK) ON B.QUOTE_ID = C.QUOTE_ID AND B.SERVICE_ID = C.SERVICE_ID AND B.GOT_CODE = C.GOT_CODE  AND ISNULL(B.PROCESS_TYPE,'') = ISNULL(C.PROCESS_TYPE,'') AND ISNULL(B.DEVICE_NODE,'') = ISNULL(C.DEVICE_NODE,'') AND SAQGPM.KIT_ID = C.KIT_ID WHERE B.QUOTE_ID = '"+str(Qt_id)+"' AND B.SERVICE_ID='Z0010' ) t 	) A FOR XML PATH ('')  ), 1, 1, '')+']}','amp;#','#') AS RESULT "
		)
		
		StatusUpdate = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE SAQICO SET STATUS=''ASSEMBLY IS MISSING'' FROM SAQICO (NOLOCK) LEFT JOIN "+str(SAQSCA)+"  SAQSCA(NOLOCK) ON SAQSCA.QUOTE_ID = SAQICO.QUOTE_ID AND SAQSCA.EQUIPMENT_ID = SAQICO.EQUIPMENT_ID AND SAQSCA.SERVICE_ID = SAQICO.SERVICE_ID AND SAQSCA.QTEREV_ID = SAQICO.QTEREV_ID WHERE SAQICO.QUOTE_ID = ''"+str(Qt_id)+"'' AND SAQICO.QTEREV_ID= ''"+str(REVISION_ID) +"'' AND SAQSCA.EQUIPMENT_ID IS NULL AND SAQICO.SERVICE_ID IN (SELECT DISTINCT SERVICE_ID FROM PRSPRV(NOLOCK) WHERE ISNULL(SSCM_COST,''FALSE'')=''TRUE'' ) AND QTETYP=''TOOL BASED'' '")
		
		StatusUpdate = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE SAQICO SET STATUS=''ASSEMBLY IS MISSING'' FROM SAQICO (NOLOCK) LEFT JOIN "+str(SAQGPA)+"  SAQSCA(NOLOCK) ON SAQSCA.QUOTE_ID = SAQICO.QUOTE_ID AND SAQSCA.SERVICE_ID = SAQICO.SERVICE_ID AND SAQSCA.QTEREV_ID = SAQICO.QTEREV_ID WHERE SAQICO.QUOTE_ID = ''"+str(Qt_id)+"'' AND SAQICO.QTEREV_ID= ''"+str(REVISION_ID) +"'' AND SAQSCA.ASSEMBLY_ID IS NULL AND SAQICO.SERVICE_ID IN (SELECT DISTINCT SERVICE_ID FROM PRSPRV(NOLOCK) WHERE ISNULL(SSCM_COST,''FALSE'')=''TRUE'' ) AND QTETYP IN (''EVENT BASED'' ,''FLEX EVENT BASED'') '")
			
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
			webclient.Headers.Add("Environment-Identifier", "X")
			crm_response1 = webclient.UploadString(str(LOGIN_CRE.URL),str(table.RESULT))
			Log.Info("28/12 sscm response --->"+str(crm_response1))	
			
		if str(PMSA_EVENT).upper() != "NONE" and str(type(PMSA_EVENT.RESULT)) == "<type 'str'>":
			Flag = "True"

			Parameter = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'SELECT' ")

			primaryQueryItems = SqlHelper.GetFirst( ""+ str(Parameter.QUERY_CRITERIA_1)+ " SYINPL (INTEGRATION_PAYLOAD,SESSION_ID,INTEGRATION_NAME)  select ''"+str(PMSA_EVENT.RESULT)+ "'','"+ str(timestamp_sessionid)+ "'+''Flex'',''CPQ_TO_SSCM_LOAD'' ' ")
			
			#F5 AUTHENTICATION				
			LOGIN_CRE = SqlHelper.GetFirst("SELECT  URL FROM SYCONF where EXTERNAL_TABLE_NAME ='CPQ_TO_SSCM_PMSA_QUOTE'")
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
			webclient.Headers.Add("Environment-Identifier", "X")
			Log.Info("28/12 PMSA_EVENT tiggerd --->")
			crm_response1 = webclient.UploadString(str(LOGIN_CRE.URL),str(PMSA_EVENT.RESULT))	
			Log.Info("28/12 PMSA_EVENT response --->"+str(crm_response1))
		
		if str(TKM_EVENT).upper() != "NONE" and str(type(TKM_EVENT.RESULT)) == "<type 'str'>":
			Flag = "True"

			Parameter = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'SELECT' ")

			primaryQueryItems = SqlHelper.GetFirst( ""+ str(Parameter.QUERY_CRITERIA_1)+ " SYINPL (INTEGRATION_PAYLOAD,SESSION_ID,INTEGRATION_NAME)  select ''"+str(TKM_EVENT.RESULT)+ "'','"+ str(timestamp_sessionid)+ "'+''Flex'',''CPQ_TO_SSCM_LOAD'' ' ")
			
			#F5 AUTHENTICATION				
			LOGIN_CRE = SqlHelper.GetFirst("SELECT  URL FROM SYCONF where EXTERNAL_TABLE_NAME ='CPQ_TO_SSCM_TKM_QUOTE'")
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
			webclient.Headers.Add("Environment-Identifier", "X")
			Log.Info("28/12 TKM_EVENT tiggerd --->")
			crm_response1 = webclient.UploadString(str(LOGIN_CRE.URL),str(TKM_EVENT.RESULT))	
			Log.Info("28/12 TKM_EVENT response --->"+str(crm_response1))
		
		if str(table_Z0100).upper() != "NONE" and str(type(table_Z0100.RESULT)) == "<type 'str'>":
			Flag = "True"

			Parameter = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'SELECT' ")

			primaryQueryItems = SqlHelper.GetFirst( ""+ str(Parameter.QUERY_CRITERIA_1)+ " SYINPL (INTEGRATION_PAYLOAD,SESSION_ID,INTEGRATION_NAME)  select ''"+str(table_Z0100.RESULT)+ "'','"+ str(timestamp_sessionid)+ "',''CPQ_TO_SSCM_LOAD'' ' ")
			
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
			webclient.Headers.Add("Environment-Identifier", "X")
			crm_response1 = webclient.UploadString(str(LOGIN_CRE.URL),str(table_Z0100.RESULT))
		
		if "Successfully" in crm_response1:
			
			Log.Info("14/02 sscm_response --->"+str(crm_response1))
			
			StatusUpdate = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE SAQICO SET STATUS=''ACQUIRING'' FROM SAQICO (NOLOCK) JOIN "+str(SAQSCA)+"  SAQSCA(NOLOCK) ON SAQSCA.QUOTE_ID = SAQICO.QUOTE_ID AND SAQSCA.EQUIPMENT_ID = SAQICO.EQUIPMENT_ID AND SAQSCA.SERVICE_ID = SAQICO.SERVICE_ID WHERE SAQSCA.QUOTE_ID = ''"+str(Qt_id)+"'' AND SAQICO.QTEREV_ID= ''"+str(REVISION_ID) +"'' AND QTETYP=''TOOL BASED'' '")
			
			StatusUpdate = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE SAQICO SET STATUS=''ACQUIRING'' FROM SAQICO (NOLOCK) JOIN "+str(SAQGPA)+"  SAQSCA(NOLOCK) ON SAQSCA.QUOTE_ID = SAQICO.QUOTE_ID AND SAQSCA.SERVICE_ID = SAQICO.SERVICE_ID WHERE SAQSCA.QUOTE_ID = ''"+str(Qt_id)+"'' AND SAQICO.QTEREV_ID= ''"+str(REVISION_ID) +"'' AND QTETYP IN (''EVENT BASED'' ,''FLEX EVENT BASED'') '")

			Emailinfo = SqlHelper.GetFirst("SELECT QUOTE_ID,CPQ,SSCM,CPQ-SSCM AS REMANING FROM (SELECT SAQICO.QUOTE_ID,COUNT(DISTINCT SAQICO.EQUIPMENT_ID) AS CPQ,COUNT(DISTINCT SAQSCA.EQUIPMENT_ID) AS SSCM  FROM SAQICO (NOLOCK) LEFT JOIN "+str(SAQSCA)+" SAQSCA(NOLOCK) ON SAQSCA.QUOTE_ID = SAQICO.QUOTE_ID AND SAQSCA.EQUIPMENT_ID = SAQICO.EQUIPMENT_ID AND SAQSCA.SERVICE_ID = SAQICO.SERVICE_ID WHERE SAQICO.QUOTE_ID = '"+str(Qt_id)+"' AND SAQICO.QTEREV_ID = '"+str(REVISION_ID) +"' AND QTETYP='TOOL BASED' group by SAQICO.Quote_ID UNION SELECT SAQICO.QUOTE_ID,COUNT(DISTINCT SAQICO.EQUIPMENT_ID) AS CPQ,COUNT(DISTINCT SAQSCA.EQUIPMENT_ID) AS SSCM  FROM SAQICO (NOLOCK) LEFT JOIN "+str(SAQGPA)+" SAQSCA(NOLOCK) ON SAQSCA.QUOTE_ID = SAQICO.QUOTE_ID AND SAQSCA.SERVICE_ID = SAQICO.SERVICE_ID WHERE SAQICO.QUOTE_ID = '"+str(Qt_id)+"' AND SAQICO.QTEREV_ID = '"+str(REVISION_ID) +"' AND QTETYP IN ('EVENT BASED' ,'FLEX EVENT BASED') group by SAQICO.Quote_ID )SUB_SAQICO ")
			
			SAQSCO_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQSCO)+"'' ) BEGIN DROP TABLE "+str(SAQSCO)+" END  ' ")
			
			SAQIEN_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQIEN)+"'' ) BEGIN DROP TABLE "+str(SAQIEN)+" END  ' ")
			
			SAQSCA_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQSCA)+"'' ) BEGIN DROP TABLE "+str(SAQSCA)+" END  ' ")

			SAQSAP_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQSAP)+"'' ) BEGIN DROP TABLE "+str(SAQSAP)+" END  ' ")
			
			SAQSAE_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQSAE)+"'' ) BEGIN DROP TABLE "+str(SAQSAE)+" END  ' ")
			
			SAQGPA_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQGPA)+"'' ) BEGIN DROP TABLE "+str(SAQGPA)+" END  ' ")
			
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

			copyEmail7 = MailAddress("christoper.aravinth@bostonharborconsulting.com")
			msg.Bcc.Add(copyEmail7)

			# Send the message
			mailClient.Send(msg)		
		
		if "Status: 400" in  str(crm_response1):

			indx_start = str(crm_response1).find('[')
			indx_end = str(crm_response1).find(']')+1

			Header = "<!DOCTYPE html><html><head><style>table {font-family: Calibri, sans-serif; border-collapse: collapse; width: 75%}td, th {  border: 1px solid #dddddd;  text-align: left; padding: 8px;}.im {color: #222;}tr:nth-child(even) {background-color: #dddddd;} #bd{color : 'black';} </style></head><body id = 'bd'>"

			Table_start = "<p>Hi Team,<br><br>The Quote Id "+Qt_id+" is not triggered for SSCM Pricing for below error.<br><br>"+str(crm_response1[indx_start:indx_end])+"</p><br>"
			
			Table_End = "</table><p><strong>Note : </strong>Please do not reply to this email.</p></body></html>"
			Table_info = ""     

			Error_Info = Header + Table_start + Table_info + Table_End

			LOGIN_CRE = SqlHelper.GetFirst("SELECT USER_NAME as Username,Password FROM SYCONF where Domain ='SUPPORT_MAIL'")
			ToEml = SqlHelper.GetFirst("SELECT ISNULL(OWNER_ID,'X0116959') AS OWNER_ID FROM SAQTMT (NOLOCK) WHERE SAQTMT.QUOTE_ID = '"+str(Qt_id)+"'  ") 

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
			msg.Subject = "CPQ to SSCM - Triggering Error Notification(X-Tenant)"
			msg.IsBodyHtml = True
			msg.Body = Error_Info

			# CC Emails 		

			copyEmail3 = MailAddress("suresh.muniyandi@bostonharborconsulting.com")
			msg.Bcc.Add(copyEmail3)	

			copyEmail4 = MailAddress("baji.baba@bostonharborconsulting.com")
			msg.CC.Add(copyEmail4)

			copyEmail7 = MailAddress("christoper.aravinth@bostonharborconsulting.com")
			msg.Bcc.Add(copyEmail7)
			
			# Send the message
			mailClient.Send(msg)
		
		if crm_response1 == '':
			ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "200", "Message": "NO DATA AVAILABLE FOR SYNCHRONIZATION"}]})

		if Flag == "True":
			ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "200", "Message": str(crm_response1)}]})
		else:

			SAQSCO_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQSCO)+"'' ) BEGIN DROP TABLE "+str(SAQSCO)+" END  ' ")
		
			SAQIEN_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQIEN)+"'' ) BEGIN DROP TABLE "+str(SAQIEN)+" END  ' ")
			
			SAQSCA_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQSCA)+"'' ) BEGIN DROP TABLE "+str(SAQSCA)+" END  ' ")

			SAQSAP_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQSAP)+"'' ) BEGIN DROP TABLE "+str(SAQSAP)+" END  ' ")
			
			SAQSAE_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQSAE)+"'' ) BEGIN DROP TABLE "+str(SAQSAE)+" END  ' ")
			
			SAQGPA_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQGPA)+"'' ) BEGIN DROP TABLE "+str(SAQGPA)+" END  ' ")

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
		
		SAQGPA_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQGPA)+"'' ) BEGIN DROP TABLE "+str(SAQGPA)+" END  ' ")
		
		Log.Info("QTPOSTPRSM ERROR---->:" + str(sys.exc_info()[1]))
		Log.Info("QTPOSTPRSM ERROR LINE NO---->:" + str(sys.exc_info()[-1].tb_lineno))
		ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "400", "Message": str(sys.exc_info()[1])}]})
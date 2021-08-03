# =========================================================================================================================================
#   __script_name : MAPOSTBULK.PY(AMAT)
#   __script_description : THIS SCRIPT IS USED TO UPDATE MATERIALS FROM STAGING TABLE TO THE MAIN TABLE
#   __primary_author__ : SURESH MUNIYANDI
#   __create_date :
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import sys
import datetime
import clr

clr.AddReference("System.Net")
from System.Net import CookieContainer, NetworkCredential, Mail
from System.Net.Mail import SmtpClient, MailAddress, Attachment, MailMessage

try:	

	sessionid = SqlHelper.GetFirst("SELECT NEWID() AS A")
	timestamp_sessionid = "'" + str(sessionid.A) + "'"

	Parameter = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'SELECT' ")
	Parameter1 = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'UPD' ")
	Parameter2 = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'DEL' ")

	today = datetime.datetime.now()
	Modi_date = today.strftime("%m/%d/%Y %H:%M:%S %p")
	
	UpdateTable1=SqlHelper.GetFirst("sp_executesql @T=N'update mamtrl_inbound set sap_part_number =  convert(varchar(100),convert(bigint,sap_part_number)) where isnumeric(sap_part_number)=1 and sap_part_number not like ''%.%'' '")

	UpdateTable1=SqlHelper.GetFirst("sp_executesql @T=N'update mamsop_inbound set sap_part_number =  convert(varchar(100),convert(bigint,sap_part_number)) where isnumeric(sap_part_number)=1 and sap_part_number not like ''%.%'' '")

	UpdateTable1=SqlHelper.GetFirst("sp_executesql @T=N'update mamact_inbound set sap_part_number =  convert(varchar(100),convert(bigint,sap_part_number)) where isnumeric(sap_part_number)=1 and sap_part_number not like ''%.%'' '")

	UpdateTable1=SqlHelper.GetFirst("sp_executesql @T=N'update a set sap_part_number = b.sap_part_number,division_id = b.division_id from mamsop_inbound a join mamtrl_inbound b on a.session_id = b.session_id  '")

	
	primaryQueryItems = SqlHelper.GetFirst(
			""
			+ str(Parameter1.QUERY_CRITERIA_1)
			+ "  mamtrl_inbound set process_status = ''DUPLICATE'' from mamtrl_inbound(nolock) join (select sap_part_number,max(cpqtableentryid) as cpqtableentryid from mamtrl_inbound where isnull(process_status,'''')='''' group by sap_part_number having count(cpqtableentryid)>1 )SUB_MAMTRL on mamtrl_inbound.sap_part_number = SUB_MAMTRL.sap_part_number where mamtrl_inbound.cpqtableentryid<> SUB_MAMTRL.cpqtableentryid and isnull(process_status,'''')=''''  ' "
		)

	primaryQueryItems = SqlHelper.GetFirst(
			""
			+ str(Parameter1.QUERY_CRITERIA_1)
			+ "  mamtrl_inbound set process_status=''DUPLICATE'' from mamtrl_inbound (nolock) left join mamsop_inbound(nolock) on mamtrl_inbound.session_id = mamsop_inbound.session_id where mamsop_inbound.session_id is null' "
		)
	
	primaryQueryItems = SqlHelper.GetFirst(
			""
			+ str(Parameter1.QUERY_CRITERIA_1)
			+ "  mamsop_inbound set process_status=''DUPLICATE'' from mamtrl_inbound(nolock) join mamsop_inbound(nolock) on mamtrl_inbound.session_id = mamsop_inbound.session_id where isnull(mamtrl_inbound.process_status,'''')=''DUPLICATE''  ' "
		)
		
	primaryQueryItems = SqlHelper.GetFirst(""+ str(Parameter1.QUERY_CRITERIA_1)+ "  mamtrl_INBOUND set mamtrl_INBOUND.TIMESTAMP='"+ str(timestamp_sessionid)+ "',process_status='''' FROM mamtrl_INBOUND (nolock) where session_id in (select session_id from mamsop_INBOUND (nolock) where isnull(process_status,'''')IN (''READY FOR UPLOAD'',''INPROGRESS'',''''))  ' ")

	primaryQueryItems = SqlHelper.GetFirst(""+ str(Parameter1.QUERY_CRITERIA_1)+ "  mamsop_INBOUND set mamsop_INBOUND.TIMESTAMP='"+ str(timestamp_sessionid)+ "',process_status='''' FROM mamsop_INBOUND(nolock) where isnull(process_status,'''')IN (''READY FOR UPLOAD'',''INPROGRESS'','''')  ' ")

	primaryQueryItems = SqlHelper.GetFirst(""+ str(Parameter1.QUERY_CRITERIA_1)+ "  mamtrl_INBOUND set mamtrl_INBOUND.TIMESTAMP='"+ str(timestamp_sessionid)+ "',process_status='''' FROM mamtrl_INBOUND (nolock) where isnull(process_status,'''')IN (''READY FOR UPLOAD'',''INPROGRESS'','''')  ' ")



	primaryQueryItems = SqlHelper.GetFirst(
				""
				+ str(Parameter1.QUERY_CRITERIA_1)
				+ "  MAMTRL_INBOUND set MAMTRL_INBOUND.process_status=''Inprogress'',MAMTRL_INBOUND.ERROR='''',MAMTRL_INBOUND.TIMESTAMP='"
				+ str(timestamp_sessionid)
				+ "' FROM MAMTRL_INBOUND (nolock) where isnull(MAMTRL_INBOUND.process_status,'''')='''' and MAMTRL_INBOUND.TIMESTAMP='"
				+ str(timestamp_sessionid)
				+ "'' "
			)
			
	primaryQueryItems = SqlHelper.GetFirst(
				""
				+ str(Parameter1.QUERY_CRITERIA_1)
				+ "  MAMSOP_INBOUND set MAMSOP_INBOUND.process_status=''Inprogress'',MAMSOP_INBOUND.ERROR='''',MAMSOP_INBOUND.TIMESTAMP='"
				+ str(timestamp_sessionid)
				+ "' from MAMSOP_INBOUND (nolock) join MAMTRL_INBOUND (nolock) on MAMSOP_INBOUND.session_id = MAMTRL_INBOUND.session_id where isnull(MAMSOP_INBOUND.process_status,'''')='''' and MAMTRL_INBOUND.process_status=''Inprogress'' ' "
			)

	primaryQueryItems = SqlHelper.GetFirst(
				""
				+ str(Parameter1.QUERY_CRITERIA_1)
				+ "  MAMACT_INBOUND set MAMACT_INBOUND.process_status=''Inprogress'',MAMACT_INBOUND.ERROR='''',MAMACT_INBOUND.TIMESTAMP='"
				+ str(timestamp_sessionid)
				+ "' from MAMACT_INBOUND (nolock) join MAMTRL_INBOUND (nolock) on MAMACT_INBOUND.session_id = MAMTRL_INBOUND.session_id where isnull(MAMACT_INBOUND.process_status,'''')='''' and MAMTRL_INBOUND.process_status=''Inprogress'' ' "
			)

	#MAMTRL Validation
	primaryQueryItems = SqlHelper.GetFirst(
				""
				+ str(Parameter1.QUERY_CRITERIA_1)
				+ "  MAMTRL_INBOUND SET ERROR = ISNULL(ERROR,'''') + ''||''+convert(nvarchar,SYMSGS.MESSAGE_CODE)+''-''+convert(nvarchar,MAMTRL_INBOUND.ERP_CREATE_DATE),MAMTRL_INBOUND.PROCESS_STATUS=''ERROR'' FROM MAMTRL_INBOUND(NOLOCK) LEFT JOIN SYMSGS(NOLOCK) ON SYMSGS.MESSAGE_CODE = ''200000'' WHERE MAMTRL_INBOUND.PROCESS_STATUS IN (''Inprogress'',''ERROR'')  AND ISDATE(ERP_CREATE_DATE) = ''0'' AND ISNULL(ERP_CREATE_DATE,'''')<>'''' AND SYMSGS.OBJECT_APINAME = ''MAMTRL'' AND MAMTRL_INBOUND.TIMESTAMP='"
				+ str(timestamp_sessionid)
				+ "' '"
			)

	primaryQueryItems = SqlHelper.GetFirst(
				""
				+ str(Parameter1.QUERY_CRITERIA_1)
				+ "  MAMTRL_INBOUND SET ERROR = ISNULL(ERROR,'''') + ''||''+convert(nvarchar,SYMSGS.MESSAGE_CODE),MAMTRL_INBOUND.PROCESS_STATUS=''ERROR'' FROM MAMTRL_INBOUND(NOLOCK) LEFT JOIN SYMSGS(NOLOCK) ON SYMSGS.MESSAGE_CODE = ''200001'' WHERE MAMTRL_INBOUND.PROCESS_STATUS IN (''Inprogress'',''ERROR'')  AND ISNULL(MATERIALTYPE_ID,'''') = '''' AND SYMSGS.OBJECT_APINAME = ''MAMTRL'' AND MAMTRL_INBOUND.TIMESTAMP='"
				+ str(timestamp_sessionid)
				+ "' '"
			)
	primaryQueryItems = SqlHelper.GetFirst(
		""
		+ str(Parameter1.QUERY_CRITERIA_1)
		+ "  MAMTRL_INBOUND SET ERROR = ISNULL(ERROR,'''') + ''||''+convert(nvarchar,SYMSGS.MESSAGE_CODE),MAMTRL_INBOUND.PROCESS_STATUS=''ERROR'' FROM MAMTRL_INBOUND(NOLOCK) LEFT JOIN SYMSGS(NOLOCK) ON SYMSGS.MESSAGE_CODE = ''200002'' WHERE MAMTRL_INBOUND.PROCESS_STATUS IN (''Inprogress'',''ERROR'')  AND ISNULL(SAP_PART_NUMBER,'''') = '''' AND SYMSGS.OBJECT_APINAME = ''MAMTRL'' AND MAMTRL_INBOUND.TIMESTAMP='"
		+ str(timestamp_sessionid)
		+ "'  '"
	)

	primaryQueryItems = SqlHelper.GetFirst(
		""
		+ str(Parameter1.QUERY_CRITERIA_1)
		+ "  MAMTRL_INBOUND SET ERROR = ISNULL(ERROR,'''') + ''||''+convert(nvarchar,SYMSGS.MESSAGE_CODE),MAMTRL_INBOUND.PROCESS_STATUS=''ERROR'' FROM MAMTRL_INBOUND(NOLOCK) LEFT JOIN SYMSGS(NOLOCK) ON SYMSGS.MESSAGE_CODE = ''200003'' WHERE MAMTRL_INBOUND.PROCESS_STATUS IN (''Inprogress'',''ERROR'')  AND ISNULL(SAP_DESCRIPTION,'''') = '''' AND SYMSGS.OBJECT_APINAME = ''MAMTRL'' AND MAMTRL_INBOUND.TIMESTAMP='"
		+ str(timestamp_sessionid)
		+ "'  '"
	)

	primaryQueryItems = SqlHelper.GetFirst(
		""
		+ str(Parameter1.QUERY_CRITERIA_1)
		+ "  MAMTRL_INBOUND SET ERROR = ISNULL(ERROR,'''') + ''||''+convert(nvarchar,SYMSGS.MESSAGE_CODE),MAMTRL_INBOUND.PROCESS_STATUS=''ERROR'' FROM MAMTRL_INBOUND(NOLOCK) LEFT JOIN SYMSGS(NOLOCK) ON SYMSGS.MESSAGE_CODE = ''200004'' WHERE MAMTRL_INBOUND.PROCESS_STATUS IN (''Inprogress'',''ERROR'') AND ISNULL(MATERIALGROUP_ID,'''') = '''' AND SYMSGS.OBJECT_APINAME = ''MAMTRL'' AND MAMTRL_INBOUND.TIMESTAMP='"
		+ str(timestamp_sessionid)
		+ "'  '"
	)

	#MAMSOP Validation
	primaryQueryItems = SqlHelper.GetFirst(
				""
				+ str(Parameter1.QUERY_CRITERIA_1)
				+ "  MAMSOP_INBOUND SET MAMSOP_INBOUND.ERROR = MAMSOP_INBOUND.ERROR + ''||''+convert(nvarchar,SYMSGS.MESSAGE_CODE)+''-''+convert(nvarchar,MAMSOP_INBOUND.SALESORG_ID),MAMSOP_INBOUND.PROCESS_STATUS=''ERROR'' FROM MAMSOP_INBOUND(NOLOCK) LEFT JOIN SASORG (NOLOCK) ON MAMSOP_INBOUND.SALESORG_ID = SASORG.SALESORG_ID LEFT JOIN SYMSGS(NOLOCK) ON SYMSGS.MESSAGE_CODE = ''200005'' WHERE MAMSOP_INBOUND.PROCESS_STATUS IN (''Inprogress'',''ERROR'') AND SYMSGS.OBJECT_APINAME = ''MAMSOP'' AND MAMSOP_INBOUND.TIMESTAMP='"
				+ str(timestamp_sessionid)
				+ "'  AND SASORG.SALESORG_ID IS NULL AND MAMSOP_INBOUND.SALESORG_ID <> '''' '"
			)

	primaryQueryItems = SqlHelper.GetFirst(
		""
		+ str(Parameter1.QUERY_CRITERIA_1)
		+ "  MAMSOP_INBOUND SET MAMSOP_INBOUND.ERROR = MAMSOP_INBOUND.ERROR + ''||''+convert(nvarchar,SYMSGS.MESSAGE_CODE)+''-''+convert(nvarchar,MAMSOP_INBOUND.PLANT_ID),MAMSOP_INBOUND.PROCESS_STATUS=''ERROR'' FROM MAMSOP_INBOUND(NOLOCK) LEFT JOIN MAPLNT (NOLOCK) ON MAMSOP_INBOUND.PLANT_ID = MAPLNT.PLANT_ID LEFT JOIN SYMSGS(NOLOCK)  ON SYMSGS.MESSAGE_CODE = ''200006'' WHERE MAMSOP_INBOUND.PROCESS_STATUS IN (''Inprogress'',''ERROR'') AND SYMSGS.OBJECT_APINAME = ''MAMSOP'' AND MAMSOP_INBOUND.TIMESTAMP='"
		+ str(timestamp_sessionid)
		+ "'  AND MAPLNT.PLANT_ID IS NULL AND MAMSOP_INBOUND.PLANT_ID <> '''''"
	)

	primaryQueryItems = SqlHelper.GetFirst(
		""
		+ str(Parameter1.QUERY_CRITERIA_1)
		+ "  MAMSOP_INBOUND SET MAMSOP_INBOUND.ERROR = MAMSOP_INBOUND.ERROR + ''||''+convert(nvarchar,SYMSGS.MESSAGE_CODE)+''-''+convert(nvarchar,MAMSOP_INBOUND.DISTRIBUTIONCHANNEL_ID),MAMSOP_INBOUND.PROCESS_STATUS=''ERROR'' FROM MAMSOP_INBOUND(NOLOCK) LEFT JOIN SADSCH (NOLOCK) ON MAMSOP_INBOUND.DISTRIBUTIONCHANNEL_ID = SADSCH.DISTRIBUTIONCHANNEL_ID LEFT JOIN SYMSGS(NOLOCK) ON SYMSGS.MESSAGE_CODE = ''200007'' WHERE MAMSOP_INBOUND.PROCESS_STATUS IN (''Inprogress'',''ERROR'') AND SYMSGS.OBJECT_APINAME = ''MAMSOP'' AND MAMSOP_INBOUND.TIMESTAMP='"
		+ str(timestamp_sessionid)
		+ "'  AND SADSCH.DISTRIBUTIONCHANNEL_ID IS NULL AND MAMSOP_INBOUND.DISTRIBUTIONCHANNEL_ID <> '''''"
	)

	primaryQueryItems = SqlHelper.GetFirst(
		""
		+ str(Parameter1.QUERY_CRITERIA_1)
		+ "  MAMSOP_INBOUND SET MAMSOP_INBOUND.ERROR = MAMSOP_INBOUND.ERROR + ''||''+convert(nvarchar,SYMSGS.MESSAGE_CODE)+''-''+convert(nvarchar,MAMSOP_INBOUND.DIVISION_ID),MAMSOP_INBOUND.PROCESS_STATUS=''ERROR'' FROM MAMSOP_INBOUND(NOLOCK) LEFT JOIN SADIVN (NOLOCK) ON MAMSOP_INBOUND.DIVISION_ID = SADIVN.DIVISION_ID LEFT JOIN SYMSGS(NOLOCK)  ON SYMSGS.MESSAGE_CODE = ''200008'' WHERE MAMSOP_INBOUND.PROCESS_STATUS IN (''Inprogress'',''ERROR'') AND SYMSGS.OBJECT_APINAME = ''MAMSOP'' AND MAMSOP_INBOUND.TIMESTAMP='"
		+ str(timestamp_sessionid)
		+ "'  AND SADIVN.DIVISION_ID IS NULL AND MAMSOP_INBOUND.DIVISION_ID <> '''''"
	)

	primaryQueryItems = SqlHelper.GetFirst(
		""
		+ str(Parameter1.QUERY_CRITERIA_1)
		+ "  MAMSOP_INBOUND SET MAMSOP_INBOUND.ERROR = MAMSOP_INBOUND.ERROR + ''||''+convert(nvarchar,SYMSGS.MESSAGE_CODE)+''-''+convert(nvarchar,MAMSOP_INBOUND.MATERIALSTATUS_ID),MAMSOP_INBOUND.PROCESS_STATUS=''ERROR'' FROM MAMSOP_INBOUND(NOLOCK) LEFT JOIN MAMTST (NOLOCK) ON MAMSOP_INBOUND.MATERIALSTATUS_ID = MAMTST.MATERIALSTATUS_ID LEFT JOIN SYMSGS(NOLOCK)  ON SYMSGS.MESSAGE_CODE = ''200009'' WHERE MAMSOP_INBOUND.PROCESS_STATUS IN (''Inprogress'',''ERROR'') AND SYMSGS.OBJECT_APINAME = ''MAMSOP'' AND MAMSOP_INBOUND.TIMESTAMP='"
		+ str(timestamp_sessionid)
		+ "'  AND MAMTST.MATERIALSTATUS_ID IS NULL AND MAMSOP_INBOUND.MATERIALSTATUS_ID <> '''''"
	)

	primaryQueryItems = SqlHelper.GetFirst(
				""
				+ str(Parameter1.QUERY_CRITERIA_1)
				+ "  MAMSOP_INBOUND SET MAMSOP_INBOUND.ERROR = MAMSOP_INBOUND.ERROR + ''||''+convert(nvarchar,SYMSGS.MESSAGE_CODE),MAMSOP_INBOUND.PROCESS_STATUS=''ERROR'' FROM MAMSOP_INBOUND(NOLOCK) LEFT JOIN SYMSGS(NOLOCK)  ON SYMSGS.MESSAGE_CODE = ''200010'' WHERE MAMSOP_INBOUND.PROCESS_STATUS IN (''Inprogress'',''ERROR'') AND SYMSGS.OBJECT_APINAME = ''MAMSOP'' AND MAMSOP_INBOUND.TIMESTAMP='"
				+ str(timestamp_sessionid)
				+ "'  AND SALESORG_ID = '''''"
			)

	primaryQueryItems = SqlHelper.GetFirst(
				""
				+ str(Parameter1.QUERY_CRITERIA_1)
				+ "  MAMSOP_INBOUND SET MAMSOP_INBOUND.ERROR = MAMSOP_INBOUND.ERROR + ''||''+convert(nvarchar,SYMSGS.MESSAGE_CODE),MAMSOP_INBOUND.PROCESS_STATUS=''ERROR'' FROM MAMSOP_INBOUND(NOLOCK) LEFT JOIN SYMSGS(NOLOCK) ON SYMSGS.MESSAGE_CODE = ''200011'' WHERE MAMSOP_INBOUND.PROCESS_STATUS IN (''Inprogress'',''ERROR'') AND SYMSGS.OBJECT_APINAME = ''MAMSOP'' AND MAMSOP_INBOUND.TIMESTAMP='"
				+ str(timestamp_sessionid)
				+ "'   AND SAP_PART_NUMBER = '''' '"
			)

	primaryQueryItems = SqlHelper.GetFirst(
		""
		+ str(Parameter1.QUERY_CRITERIA_1)
		+ "  MAMSOP_INBOUND SET MAMSOP_INBOUND.ERROR = MAMSOP_INBOUND.ERROR + ''||''+convert(nvarchar,SYMSGS.MESSAGE_CODE),MAMSOP_INBOUND.PROCESS_STATUS=''ERROR'' FROM MAMSOP_INBOUND(NOLOCK)  LEFT JOIN SYMSGS(NOLOCK) ON SYMSGS.MESSAGE_CODE = ''200012'' WHERE MAMSOP_INBOUND.PROCESS_STATUS IN (''Inprogress'',''ERROR'') AND SYMSGS.OBJECT_APINAME = ''MAMSOP'' AND MAMSOP_INBOUND.TIMESTAMP='"
		+ str(timestamp_sessionid)
		+ "'  AND PLANT_ID = '''''"
	)

	primaryQueryItems = SqlHelper.GetFirst(
		""
		+ str(Parameter1.QUERY_CRITERIA_1)
		+ "  MAMSOP_INBOUND SET MAMSOP_INBOUND.ERROR = MAMSOP_INBOUND.ERROR + ''||''+convert(nvarchar,SYMSGS.MESSAGE_CODE),MAMSOP_INBOUND.PROCESS_STATUS=''ERROR'' FROM MAMSOP_INBOUND(NOLOCK) LEFT JOIN SYMSGS(NOLOCK)  ON SYMSGS.MESSAGE_CODE = ''200013'' WHERE MAMSOP_INBOUND.PROCESS_STATUS IN (''Inprogress'',''ERROR'') AND SYMSGS.OBJECT_APINAME = ''MAMSOP'' AND MAMSOP_INBOUND.TIMESTAMP='"
		+ str(timestamp_sessionid)
		+ "'  AND DISTRIBUTIONCHANNEL_ID = '''''"
	)

	#MAMACT Validation
	
	primaryQueryItems = SqlHelper.GetFirst(
		""
		+ str(Parameter1.QUERY_CRITERIA_1)
		+ "  MAMACT_INBOUND SET MAMACT_INBOUND.ERROR = MAMACT_INBOUND.ERROR + ''||''+convert(nvarchar,SYMSGS.MESSAGE_CODE)+''-''+convert(nvarchar,MAMACT_INBOUND.CATEGORY_ID),MAMACT_INBOUND.PROCESS_STATUS=''ERROR'' FROM MAMACT_INBOUND(NOLOCK) LEFT JOIN MACATG(NOLOCK) ON MAMACT_INBOUND.CATEGORY_ID = MACATG.CATEGORY_ID LEFT JOIN SYMSGS(NOLOCK) SYMSGS ON SYMSGS.MESSAGE_CODE = ''200014'' WHERE MAMACT_INBOUND.PROCESS_STATUS IN (''Inprogress'',''ERROR'') AND SYMSGS.OBJECT_APINAME = ''MAMACT'' AND MAMACT_INBOUND.TIMESTAMP='"
		+ str(timestamp_sessionid)
		+ "'  AND MACATG.CATEGORY_ID IS NULL AND MAMACT_INBOUND.CATEGORY_ID <> '''''"
	)

	primaryQueryItems = SqlHelper.GetFirst(
				""
				+ str(Parameter1.QUERY_CRITERIA_1)
				+ "  MAMACT_INBOUND SET MAMACT_INBOUND.ERROR = MAMACT_INBOUND.ERROR + ''||''+convert(nvarchar,SYMSGS.MESSAGE_CODE),MAMACT_INBOUND.PROCESS_STATUS=''ERROR'' FROM MAMACT_INBOUND(NOLOCK) LEFT JOIN SYMSGS(NOLOCK) ON SYMSGS.MESSAGE_CODE = ''200015'' WHERE MAMACT_INBOUND.PROCESS_STATUS IN (''Inprogress'',''ERROR'') AND SYMSGS.OBJECT_APINAME = ''MAMACT'' AND MAMACT_INBOUND.TIMESTAMP='"
				+ str(timestamp_sessionid)
				+ "'   AND SAP_PART_NUMBER = '''' '"
			)

	primaryQueryItems = SqlHelper.GetFirst(
		""
		+ str(Parameter1.QUERY_CRITERIA_1)
		+ "  MAMACT_INBOUND SET MAMACT_INBOUND.ERROR = MAMACT_INBOUND.ERROR + ''||''+convert(nvarchar,SYMSGS.MESSAGE_CODE),MAMACT_INBOUND.PROCESS_STATUS=''ERROR'' FROM MAMACT_INBOUND(NOLOCK) LEFT JOIN SYMSGS(NOLOCK) ON SYMSGS.MESSAGE_CODE = ''200016'' WHERE MAMACT_INBOUND.PROCESS_STATUS IN (''Inprogress'',''ERROR'') AND SYMSGS.OBJECT_APINAME = ''MAMACT'' AND MAMACT_INBOUND.TIMESTAMP='"
		+ str(timestamp_sessionid)
		+ "'  AND CATEGORY_ID = '''''"
	)

	#Validation Completed

	primaryQueryItems = SqlHelper.GetFirst(
		""
		+ str(Parameter1.QUERY_CRITERIA_1)
		+ "  MAMTRL_INBOUND SET PROCESS_STATUS=''READY FOR UPLOAD'' WHERE PROCESS_STATUS=''Inprogress'' AND TIMESTAMP='"
		+ str(timestamp_sessionid)
		+ "' AND ISNULL(ERROR,'''')='''' '"
	)

	primaryQueryItems = SqlHelper.GetFirst(
		""
		+ str(Parameter1.QUERY_CRITERIA_1)
		+ "  MAMSOP_INBOUND SET PROCESS_STATUS=''READY FOR UPLOAD'' WHERE PROCESS_STATUS=''Inprogress'' AND TIMESTAMP='"
		+ str(timestamp_sessionid)
		+ "' AND ISNULL(ERROR,'''')='''' '"
	)

	primaryQueryItems = SqlHelper.GetFirst(
		""
		+ str(Parameter1.QUERY_CRITERIA_1)
		+ "  MAMACT_INBOUND SET PROCESS_STATUS=''READY FOR UPLOAD'' WHERE PROCESS_STATUS=''Inprogress'' AND TIMESTAMP='"
		+ str(timestamp_sessionid)
		+ "' AND ISNULL(ERROR,'''')='''' '"
	)

	#Error Logging 
	
	#Error log table creating dynamically

	Temp_Table_Name = 'ERROR_LOG'
	
	ERRLOG_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(Temp_Table_Name)+"'' ) BEGIN DROP TABLE "+str(Temp_Table_Name)+" END  ' ")

	TempTable = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(Temp_Table_Name)+"'' ) BEGIN DROP TABLE "+str(Temp_Table_Name)+" END CREATE TABLE "+str(Temp_Table_Name)+" (SESSION_ID VARCHAR(100),INTEGRATION_TYPE VARCHAR(100) ,PROCESS_STATUS VARCHAR(100),CpqTableEntryDateModified date )'")

	primaryQueryItems = SqlHelper.GetFirst(""+ str(Parameter.QUERY_CRITERIA_1)+ " ERROR_LOG (SESSION_ID,CpqTableEntryDateModified) SELECT SESSION_ID,getdate() FROM (SELECT DISTINCT MAMTRL_INBOUND.SESSION_ID as SESSION_ID FROM MAMTRL_INBOUND (NOLOCK) WHERE  ISNULL(MAMTRL_INBOUND.PROCESS_STATUS,'''')=''ERROR'' AND MAMTRL_INBOUND.TIMESTAMP='"+ str(timestamp_sessionid)+ "'  union 	SELECT MAMSOP_INBOUND.SESSION_ID FROM MAMSOP_INBOUND (NOLOCK)  JOIN MAMTRL_INBOUND (NOLOCK) ON MAMSOP_INBOUND.SESSION_ID=MAMTRL_INBOUND.SESSION_ID WHERE  ISNULL(MAMSOP_INBOUND.PROCESS_STATUS,'''')=''ERROR'' AND MAMSOP_INBOUND.TIMESTAMP='"+ str(timestamp_sessionid)+ "' UNION SELECT MAMACT_INBOUND.SESSION_ID FROM MAMACT_INBOUND (NOLOCK)  JOIN MAMTRL_INBOUND(NOLOCK) ON MAMACT_INBOUND.SESSION_ID=MAMTRL_INBOUND.SESSION_ID WHERE  ISNULL(MAMACT_INBOUND.PROCESS_STATUS,'''')=''ERROR'' AND MAMACT_INBOUND.TIMESTAMP='"+ str(timestamp_sessionid)+ "')SUB_ERRLOG  ' ")

	primaryQueryItems = SqlHelper.GetFirst(
		""
		+ str(Parameter1.QUERY_CRITERIA_1)
		+ "  MAMTRL_INBOUND SET PROCESS_STATUS=''ERROR'' FROM MAMTRL_INBOUND(NOLOCK) JOIN ERROR_LOG(NOLOCK) ON MAMTRL_INBOUND.SESSION_ID = ERROR_LOG.SESSION_ID WHERE MAMTRL_INBOUND.TIMESTAMP='"
		+ str(timestamp_sessionid)
		+ "' '"
	)

	primaryQueryItems = SqlHelper.GetFirst(
		""
		+ str(Parameter1.QUERY_CRITERIA_1)
		+ "  MAMSOP_INBOUND SET PROCESS_STATUS=''ERROR'' FROM MAMSOP_INBOUND(NOLOCK) JOIN ERROR_LOG(NOLOCK) ON MAMSOP_INBOUND.SESSION_ID = ERROR_LOG.SESSION_ID WHERE MAMSOP_INBOUND.TIMESTAMP='"
		+ str(timestamp_sessionid)
		+ "' '"
	)
	
	primaryQueryItems = SqlHelper.GetFirst(
		""
		+ str(Parameter1.QUERY_CRITERIA_1)
		+ "  MAMACT_INBOUND SET PROCESS_STATUS=''ERROR'' FROM MAMACT_INBOUND JOIN ERROR_LOG ON MAMACT_INBOUND.SESSION_ID = ERROR_LOG.SESSION_ID WHERE MAMACT_INBOUND.TIMESTAMP='"
		+ str(timestamp_sessionid)
		+ "' '"
	)

	#Upload Starts
	#MAMTRL

	primaryQueryItems = SqlHelper.GetFirst(
	""
	+ str(Parameter1.QUERY_CRITERIA_1)
	+ "  MAMTRL SET MAMTRL.CpqTableEntryModifiedBy = ''"
	+ str(User.Id)
	+ "'',MAMTRL.CpqTableEntryDateModified = GetDate(),MAMTRL.UNIT_OF_MEASURE =  MAMUOM.UOM, MAMTRL.UOM_RECORD_ID = MAMUOM.UNIT_OF_MEASURE_RECORD_ID,MATERIALCONFIG_TYPE  = MAMTRL_INBOUND.MATERIALCONFIG_TYPE,  MAMTRL.ERP_CREATE_DATE = CONVERT(DATE,MAMTRL_INBOUND.ERP_CREATE_DATE), MAMTRL.MATERIALGROUP_ID = MAMGRP.MATERIALGROUP_ID, MAMTRL.MATERIALGROUP_RECORD_ID = MAMGRP.MATERIAL_GROUP_RECORD_ID, MAMTRL.MATERIALTYPE_ID = MAMTYP.MATERIALTYPE_ID, MAMTRL.MATERIALTYPE_RECORD_ID = MAMTYP.MATERIAL_TYPE_RECORD_ID,MAMTRL.SAP_DESCRIPTION = MAMTRL_INBOUND.SAP_DESCRIPTION,  MAMTRL.MATERIALSTATUS_ID = MAMTST.MATERIALSTATUS_ID, MAMTRL.MATERIALSTATUS_RECORD_ID = MAMTST.MATERIAL_STATUS_RECORD_ID FROM MAMTRL_INBOUND(NOLOCK) JOIN MAMTYP(NOLOCK) on MAMTRL_INBOUND.MATERIALTYPE_ID = MAMTYP.MATERIALTYPE_ID LEFT JOIN MAMUOM(NOLOCK) ON MAMTRL_INBOUND.UNIT_OF_MEASURE = MAMUOM.UOM LEFT JOIN MAMTST(NOLOCK) ON MAMTRL_INBOUND.MATERIALSTATUS_ID = MAMTST.MATERIALSTATUS_ID JOIN MAMGRP(NOLOCK) on MAMTRL_INBOUND.MATERIALGROUP_ID = MAMGRP.MATERIALGROUP_ID JOIN MAMTRL(NOLOCK) ON MAMTRL_INBOUND.SAP_PART_NUMBER = MAMTRL.SAP_PART_NUMBER   WHERE MAMTRL_INBOUND.PROCESS_STATUS = ''READY FOR UPLOAD''  AND ISNULL(MAMTRL_INBOUND.ERROR,'''') = '''' AND MAMTRL_INBOUND.TIMESTAMP='"
	+ str(timestamp_sessionid)
	+ "'  ' "
	)

	primaryQueryItems = SqlHelper.GetFirst(
	""
	+ str(Parameter.QUERY_CRITERIA_1)
	+ " MAMTRL (UNIT_OF_MEASURE,UOM_RECORD_ID,MATERIALCONFIG_TYPE,ERP_CREATE_DATE,INTERNAL_NOTES,MATERIALGROUP_ID,MATERIALGROUP_RECORD_ID,MATERIALTYPE_ID,MATERIALTYPE_RECORD_ID,SAP_DESCRIPTION,SAP_PART_NUMBER,MATERIALSTATUS_ID,MATERIALSTATUS_RECORD_ID,DIVISION_ID,DIVISION_RECORD_ID,MATERIAL_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED)SELECT SUB_MAMTRL.*, CONVERT(VARCHAR(4000),NEWID()),''"+ str(User.UserName)+ "'',GETDATE() FROM (SELECT DISTINCT MAMUOM.UOM AS UNIT_OF_MEASURE,MAMUOM.UNIT_OF_MEASURE_RECORD_ID AS UOM_RECORD_ID , MAMTRL_INBOUND.MATERIALCONFIG_TYPE,CONVERT(DATE,ERP_CREATE_DATE) AS ERP_CREATE_DATE,INTERNAL_NOTES,MAMGRP.MATERIALGROUP_ID,MAMGRP.MATERIAL_GROUP_RECORD_ID,MAMTYP.MATERIALTYPE_ID,MAMTYP.MATERIAL_TYPE_RECORD_ID,MAMTRL_INBOUND.SAP_DESCRIPTION,MAMTRL_INBOUND.SAP_PART_NUMBER, MAMTST.MATERIALSTATUS_ID,MAMTST.MATERIAL_STATUS_RECORD_ID,MAMTRL_INBOUND.DIVISION_ID,SADIVN.DIVISION_RECORD_ID FROM MAMTRL_INBOUND(NOLOCK) JOIN MAMTYP(NOLOCK) on MAMTRL_INBOUND.MATERIALTYPE_ID = MAMTYP.MATERIALTYPE_ID LEFT JOIN MAMUOM(NOLOCK) ON MAMTRL_INBOUND.UNIT_OF_MEASURE = MAMUOM.UOM  LEFT JOIN MAMTST(NOLOCK) ON CASE WHEN ISNULL(MAMTRL_INBOUND.MATERIALSTATUS_ID,'''')='''' THEN ''AC'' ELSE MAMTRL_INBOUND.MATERIALSTATUS_ID END = MAMTST.MATERIALSTATUS_ID JOIN MAMGRP(NOLOCK) on MAMTRL_INBOUND.MATERIALGROUP_ID = MAMGRP.MATERIALGROUP_ID JOIN SADIVN (NOLOCK) ON MAMTRL_INBOUND.DIVISION_ID = SADIVN.DIVISION_ID WHERE MAMTRL_INBOUND.PROCESS_STATUS = ''READY FOR UPLOAD''  AND ISNULL(MAMTRL_INBOUND.ERROR,'''') = '''' AND MAMTRL_INBOUND.TIMESTAMP='"	+ str(timestamp_sessionid)+ "')SUB_MAMTRL LEFT JOIN MAMTRL(NOLOCK)  ON SUB_MAMTRL.SAP_PART_NUMBER = MAMTRL.SAP_PART_NUMBER WHERE MAMTRL.SAP_PART_NUMBER IS NULL '"	)
	
	primaryQueryItems = SqlHelper.GetFirst("sp_executesql @t=N'update mamtrl set materialconfig_type =''SIMPLE MATERIAL'' where isnull(materialconfig_type,'''')=''''  ' ")

	primaryQueryItems = SqlHelper.GetFirst("sp_executesql @t=N'update mamtrl set materialconfig_type =''CONFIGURABLE MATERIAL'' where isnull(materialconfig_type,'''')=''X''  ' ")
	
	UpdateTable1=SqlHelper.GetFirst("sp_executesql @T=N'update mamtrl set IS_SPARE_PART= case when isnull(is_spares,'''')=''SP'' then ''true'' else ''false'' end from mamtrl join mamsop_inbound  on mamtrl.sap_part_number = mamsop_inbound.sap_part_number'")

	primaryQueryItems = SqlHelper.GetFirst(
	""
	+ str(Parameter1.QUERY_CRITERIA_1)
	+ "  MAMTRL_INBOUND SET PROCESS_STATUS = ''UPLOADED'' WHERE PROCESS_STATUS=''READY FOR UPLOAD'' AND TIMESTAMP='"
	+ str(timestamp_sessionid)
	+ "'  '"
	)

	#MAMSOP

	Sql = SqlHelper.GetFirst(""+ str(Parameter1.QUERY_CRITERIA_1)+ " MAMSOP SET MAMSOP.CpqTableEntryModifiedBy = ''"+ str(User.Id)+ "'',MAMSOP.CpqTableEntryDateModified = GetDate(),MAMSOP.MATERIALSTATUS_ID=MAMSOP_INBOUND.MATERIALSTATUS_ID,MAMSOP.ITMCATGRP_ID=MAMSOP_INBOUND.ITMCATGRP_ID FROM MAMSOP (NOLOCK) JOIN MAMSOP_INBOUND (NOLOCK) ON MAMSOP.SAP_PART_NUMBER=MAMSOP_INBOUND.SAP_PART_NUMBER AND MAMSOP.SALESORG_ID=MAMSOP_INBOUND.SALESORG_ID AND MAMSOP.PLANT_ID=MAMSOP_INBOUND.PLANT_ID AND MAMSOP.DISTRIBUTIONCHANNEL_ID = MAMSOP_INBOUND.DISTRIBUTIONCHANNEL_ID AND MAMSOP.DIVISION_ID = MAMSOP_INBOUND.DIVISION_ID WHERE ISNULL(MAMSOP_INBOUND.PROCESS_STATUS,'''')=''READY FOR UPLOAD'' AND ISNULL(ERROR,'''')='''' AND TIMESTAMP = '"+ str(timestamp_sessionid)+ "'  '")
	
	ERRLOG_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''TEMP_PROCESS'' ) BEGIN DROP TABLE TEMP_PROCESS END CREATE TABLE TEMP_PROCESS (SESSION_ID VARCHAR(100),PROCESS_STATUS VARCHAR(100)) ' ")
 
	Check_flag = 1
	while Check_flag == 1:
		primaryQueryItems = SqlHelper.GetFirst(
			""
			+ str(Parameter.QUERY_CRITERIA_1)
			+ " TEMP_PROCESS (SESSION_ID)SELECT DISTINCT TOP 5000 MAMSOP_INBOUND.SAP_PART_NUMBER FROM MAMSOP_INBOUND (NOLOCK) LEFT JOIN TEMP_PROCESS (NOLOCK) ON MAMSOP_INBOUND.SAP_PART_NUMBER = TEMP_PROCESS.SESSION_ID WHERE MAMSOP_INBOUND.PROCESS_STATUS=''READY FOR UPLOAD'' AND ISNULL(ERROR,'''')=''''  AND MAMSOP_INBOUND.TIMESTAMP='"
			+ str(timestamp_sessionid)
			+ "' AND TEMP_PROCESS.SESSION_ID IS NULL  ' "
		)

		primaryQueryItems = SqlHelper.GetFirst(
			"select 'x' as a from TEMP_PROCESS(nolock)  where isnull(PROCESS_STATUS,'')='' "
		)

		if str(primaryQueryItems) != "None":

			MamsopInsertQuery = SqlHelper.GetFirst(
				""
				+ str(Parameter.QUERY_CRITERIA_1)
				+ " MAMSOP (PLANT_ID,PLANT_RECORD_ID,MATERIAL_RECORD_ID,MATERIALSTATUS_ID,MATERIALSTATUS_RECORD_ID,SALESORG_ID,SAP_PART_NUMBER,MATERIAL_NAME,SALESORG_RECORD_ID,SALESORG_NAME,ITMCATGRP_ID,ITMCATGRP_RECORD_ID,DISTRIBUTIONCHANNEL_ID,DISTRIBUTIONCHANNEL_RECORD_ID,DIVISION_ID,DIVISION_RECORD_ID,MATERIAL_SALES_ORG_PLANT__RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED)SELECT SUB_MAMSOP.*,CONVERT(VARCHAR(4000),NEWID()),''"
				+ str(User.UserName)
				+ "'',GETDATE() FROM (	SELECT DISTINCT  MAMSOP_INBOUND.PLANT_ID,MAPLNT.PLANT_RECORD_ID,MAMTRL.MATERIAL_RECORD_ID,MAMTST.MATERIALSTATUS_ID,MAMTST.MATERIAL_STATUS_RECORD_ID,MAMSOP_INBOUND.SALESORG_ID,MAMSOP_INBOUND.SAP_PART_NUMBER,MAMTRL.SAP_DESCRIPTION AS MATERIAL_NAME,SASORG.SALES_ORG_RECORD_ID AS SALESORG_RECORD_ID,SASORG.SALESORG_NAME,MAMSOP_INBOUND.ITMCATGRP_ID,MAITCG.ITEM_CATEGORY_GROUP_RECORD_ID AS ITMCATGRP_RECORD_ID,SADSCH.DISTRIBUTIONCHANNEL_ID,SADSCH.DISTRIBUTION_CHANNEL_RECORD_ID AS DISTRIBUTIONCHANNEL_RECORD_ID,SADIVN.DIVISION_ID,SADIVN.DIVISION_RECORD_ID FROM MAMSOP_INBOUND (NOLOCK) JOIN TEMP_PROCESS(NOLOCK) ON MAMSOP_INBOUND.SAP_PART_NUMBER = TEMP_PROCESS.SESSION_ID INNER JOIN MAMTRL (NOLOCK) ON MAMSOP_INBOUND.SAP_PART_NUMBER = MAMTRL.SAP_PART_NUMBER JOIN SASORG (NOLOCK) ON MAMSOP_INBOUND.SALESORG_ID = SASORG.SALESORG_ID JOIN SADSCH (NOLOCK) ON MAMSOP_INBOUND.DISTRIBUTIONCHANNEL_ID = SADSCH.DISTRIBUTIONCHANNEL_ID JOIN SADIVN (NOLOCK) ON MAMSOP_INBOUND.DIVISION_ID = SADIVN.DIVISION_ID LEFT JOIN MAPLNT (NOLOCK) ON MAMSOP_INBOUND.PLANT_ID = MAPLNT.PLANT_ID LEFT JOIN MAMTST (NOLOCK) ON CASE WHEN ISNULL(MAMSOP_INBOUND.MATERIALSTATUS_ID,'''')='''' THEN ''AC'' ELSE MAMSOP_INBOUND.MATERIALSTATUS_ID END = MAMTST.MATERIALSTATUS_ID LEFT JOIN MAITCG (NOLOCK) ON MAMSOP_INBOUND.ITMCATGRP_ID = MAITCG.ITMCATGRP_ID WHERE ISNULL(MAMSOP_INBOUND.PROCESS_STATUS,'''')=''READY FOR UPLOAD'' AND ISNULL(MAMSOP_INBOUND.ERROR,'''')='''' AND MAMSOP_INBOUND.TIMESTAMP = '"+ str(timestamp_sessionid)+ "' AND ISNULL(TEMP_PROCESS.PROCESS_STATUS,'''')='''' )SUB_MAMSOP LEFT JOIN MAMSOP (NOLOCK) ON SUB_MAMSOP.SAP_PART_NUMBER = MAMSOP.SAP_PART_NUMBER AND SUB_MAMSOP.SALESORG_ID = MAMSOP.SALESORG_ID AND SUB_MAMSOP.PLANT_ID = MAMSOP.PLANT_ID WHERE MAMSOP.SAP_PART_NUMBER IS NULL '"
				)
				
			UpdateQuery = SqlHelper.GetFirst(
				"sp_executesql @T=N'update TEMP_PROCESS set process_status=''completed'' where isnulL(process_status,'''')='''' ' "
				)
		else:
			Check_flag = 0
	
	DeleteQuery = SqlHelper.GetFirst(
				"sp_executesql @T=N'Delete from TEMP_PROCESS Where process_status=''completed'' ' "
				)
	
	Check_flag1 = 1
	while Check_flag1 == 1:
		primaryQueryItems = SqlHelper.GetFirst(
			""
			+ str(Parameter.QUERY_CRITERIA_1)
			+ " TEMP_PROCESS (SESSION_ID)SELECT DISTINCT TOP 5000 MAMSOP_INBOUND.SAP_PART_NUMBER FROM MAMSOP_INBOUND(NOLOCK) LEFT JOIN TEMP_PROCESS(NOLOCK) ON MAMSOP_INBOUND.SAP_PART_NUMBER = TEMP_PROCESS.SESSION_ID WHERE MAMSOP_INBOUND.PROCESS_STATUS=''READY FOR UPLOAD'' AND ISNULL(ERROR,'''')=''''  AND MAMSOP_INBOUND.TIMESTAMP='"
			+ str(timestamp_sessionid)
			+ "' AND TEMP_PROCESS.SESSION_ID IS NULL  ' "
		)

		primaryQueryItems = SqlHelper.GetFirst(
			"select 'x' as a from TEMP_PROCESS(nolock)  where isnull(PROCESS_STATUS,'')='' "
		)

		if str(primaryQueryItems) != "None":

			primaryQueryItems = SqlHelper.GetFirst(
				""
				+ str(Parameter.QUERY_CRITERIA_1)
				+ " MAMASO(SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,SAP_DESCRIPTION,MATERIAL_RECORD_ID,SAP_PART_NUMBER,MATERIAL_SALES_ORG_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED) SELECT SUB_MAMSOP.SALESORG_ID,SUB_MAMSOP.SALESORG_NAME ,SUB_MAMSOP.SALESORG_RECORD_ID ,SUB_MAMSOP.SAP_DESCRIPTION ,SUB_MAMSOP.MATERIAL_RECORD_ID ,SUB_MAMSOP.SAP_PART_NUMBER  ,CONVERT(VARCHAR(4000),NEWID()),''"+ str(User.UserName)
				+ "'',GETDATE() FROM (SELECT DISTINCT MAMSOP.SALESORG_ID,MAMSOP.SALESORG_NAME ,MAMSOP.SALESORG_RECORD_ID ,MAMSOP.MATERIAL_NAME AS SAP_DESCRIPTION ,MAMSOP.MATERIAL_RECORD_ID ,MAMSOP.SAP_PART_NUMBER FROM MAMSOP(NOLOCK) JOIN TEMP_PROCESS(NOLOCK) ON MAMSOP.SAP_PART_NUMBER = TEMP_PROCESS.SESSION_ID WHERE ISNULL(TEMP_PROCESS.PROCESS_STATUS,'''')='''' )SUB_MAMSOP LEFT JOIN MAMASO(NOLOCK) ON SUB_MAMSOP.SAP_PART_NUMBER = MAMASO.SAP_PART_NUMBER AND SUB_MAMSOP.SALESORG_ID = MAMASO.SALESORG_ID WHERE MAMASO.SAP_PART_NUMBER IS NULL' ")
				
			UpdateQuery = SqlHelper.GetFirst(
				"sp_executesql @T=N'update TEMP_PROCESS set process_status=''completed'' where isnulL(process_status,'''')='''' ' "
				)
		else:
			Check_flag1 = 0
	
	DeleteQuery = SqlHelper.GetFirst(
				"sp_executesql @T=N'Delete from TEMP_PROCESS Where process_status=''completed'' ' "
				)
				
	primaryQueryItems = SqlHelper.GetFirst(
	""
	+ str(Parameter1.QUERY_CRITERIA_1)
	+ "  MAMSOP SET MATSOR_RECORD_ID = MATERIAL_SALES_ORG_RECORD_ID FROM MAMSOP (NOLOCK) JOIN MAMASO(NOLOCK) ON MAMSOP.SAP_PART_NUMBER = MAMASO.SAP_PART_NUMBER AND MAMSOP.SALESORG_ID = MAMASO.SALESORG_ID WHERE ISNULL(MATSOR_RECORD_ID,'''')='''' '")

	primaryQueryItems = SqlHelper.GetFirst(
	""
	+ str(Parameter1.QUERY_CRITERIA_1)
	+ "  MAMSOP SET MATPRIGRP_ID =MAMSOP_INBOUND.PRICEGROUP_ID,MATPRIGRP_RECORD_ID = MAPGRP.PRICE_GROUP_RECORD_ID,MATPRIGRP_NAME=PRICEGROUP_DESCRIPTION FROM MAMSOP (NOLOCK) JOIN MAMSOP_INBOUND(NOLOCK) ON MAMSOP.SAP_PART_NUMBER = MAMSOP_INBOUND.SAP_PART_NUMBER AND MAMSOP.SALESORG_ID = MAMSOP_INBOUND.SALESORG_ID JOIN MAPGRP (NOLOCK) ON MAPGRP.PRICEGROUP_ID = MAMSOP_INBOUND.PRICEGROUP_ID WHERE MAMSOP_INBOUND.PROCESS_STATUS=''READY FOR UPLOAD'' AND MAMSOP_INBOUND.TIMESTAMP='"
			+ str(timestamp_sessionid)
			+ "' '")
	

	primaryQueryItems = SqlHelper.GetFirst(
	""
	+ str(Parameter1.QUERY_CRITERIA_1)
	+ "  MAMSOP_INBOUND SET PROCESS_STATUS = ''UPLOADED'' WHERE PROCESS_STATUS=''READY FOR UPLOAD'' AND TIMESTAMP='"
	+ str(timestamp_sessionid)
	+ "'  '"
	)
	
	#Insert Query
	primaryQueryItems = SqlHelper.GetFirst(
	""
	+ str(Parameter.QUERY_CRITERIA_1)
	+ " MAMACT (CATEGORY_ID,CATEGORY_NAME,CATEGORY_RECORD_ID,MATERIAL_RECORD_ID,PAR_CATEGORY_ID,PAR_CATEGORY_NAME,SAP_DESCRIPTION,SAP_PART_NUMBER,CATEGORY_PRODUCT_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED)SELECT SUB_MAMACT.*, CONVERT(VARCHAR(4000),NEWID()),''"+ str(User.UserName)+ "'',GETDATE() FROM (SELECT DISTINCT MACATG.CATEGORY_ID,MACATG.CATEGORY_NAME,MACATG.CATEGORY_RECORD_ID,MAMTRL.MATERIAL_RECORD_ID,MACATG.PAR_CATEGORY_ID,MACATG.PAR_CATEGORY_NAME,MAMTRL.SAP_DESCRIPTION,MAMTRL.SAP_PART_NUMBER FROM MAMACT_INBOUND(NOLOCK) JOIN MACATG(NOLOCK) on MAMACT_INBOUND.CATEGORY_ID = MACATG.CATEGORY_ID JOIN MAMTRL(NOLOCK) ON MAMACT_INBOUND.SAP_PART_NUMBER = MAMTRL.SAP_PART_NUMBER   WHERE MAMACT_INBOUND.PROCESS_STATUS = ''READY FOR UPLOAD''  AND ISNULL(MAMACT_INBOUND.ERROR,'''') = '''' AND MAMACT_INBOUND.TIMESTAMP='"+ str(timestamp_sessionid)+ "')SUB_MAMACT LEFT JOIN MAMACT(NOLOCK) ON SUB_MAMACT.CATEGORY_ID = MAMACT.CATEGORY_ID AND SUB_MAMACT.SAP_PART_NUMBER = MAMACT.SAP_PART_NUMBER WHERE MAMACT.CATEGORY_ID IS NULL '"
	)
	
	primaryQueryItems = SqlHelper.GetFirst(
	""
	+ str(Parameter1.QUERY_CRITERIA_1)
	+ "  MAMACT_INBOUND SET PROCESS_STATUS = ''UPLOADED'' WHERE PROCESS_STATUS=''READY FOR UPLOAD'' AND TIMESTAMP='"
	+ str(timestamp_sessionid)
	+ "'  '"
	)
	
	primaryQueryItems = SqlHelper.GetFirst(
	""
	+ str(Parameter1.QUERY_CRITERIA_1)
	+ "  MAKTPT SET PART_RECORD_ID = MATERIAL_RECORD_ID FROM MAKTPT (NOLOCK) JOIN MAMTRL(NOLOCK) ON MAKTPT.PART_NUMBER = MAMTRL.SAP_PART_NUMBER WHERE ISNULL(MAKTPT.PART_RECORD_ID,'''')=''''  '"
	)
	
	#MATMAS Errors mail system 
	Error_list = []
	Resp_msg = {}
	Lst_resp = []
	Error_check = 1
	while Error_check == 1:
		Error_primaryQuery = SqlHelper.GetList(
			"select top 10 SESSION_ID from ERROR_LOG(NOLOCK) where ISNULL(PROCESS_STATUS,'')= '' and isnull(SESSION_ID,'')<>''  "
		)

		Session_lst_count = []
		for data in Error_primaryQuery:
			Session_lst_count.append(data.SESSION_ID)

		Session_lst = tuple(Session_lst_count)
		# Log.Info("2608 2608 Session_lst------>"+str(Session_lst))
		if len(Session_lst_count) == 1:
			Session_lst = "('" + Session_lst_count[0] + "')"
		
		if len(Session_lst_count) > 0:
			primaryQueryItems = SqlHelper.GetList(
				"select distinct sap_part_number,ERROR from mamtrl_inbound (nolock) where isnull(ERROR,'')<>'' and session_id in "
				+ str(Session_lst)
				+ " union select distinct sap_part_number,ERROR from mamsop_inbound (nolock) where isnull(ERROR,'')<>'' and session_id in "
				+ str(Session_lst)
				+ "union select distinct sap_part_number,ERROR from mamsop_inbound (nolock) where isnull(ERROR,'')<>'' and session_id in "
				+ str(Session_lst)
				+ " union select distinct sap_part_number,ERROR from mamact_inbound (nolock) where isnull(ERROR,'')<>'' and session_id in "
				+ str(Session_lst)
				+ " "
			)
			Dt = {}
			for ins in primaryQueryItems:
				Modi_integration_status = []
				inte_status = str(ins.ERROR).split("||")
				ERROR = set(inte_status)
				ERROR = list(ERROR)
				if "" in ERROR:
					ERROR.remove("")
				
				for uu in ERROR:
					split_data = uu.split("-", 1)
					SYMSGS_MSG_TEXT = SqlHelper.GetFirst(
						"SELECT MESSAGE_TEXT,RECORD_ID AS REC_ID,OBJECT_APINAME,OBJECT_RECORD_ID,MESSAGE_TYPE FROM SYMSGS(NOLOCK) WHERE MESSAGE_CODE = '"
						+ str(split_data[0])
						+ "'"
					)

					if len(split_data) > 1:
						CONVERTED_MSG = SYMSGS_MSG_TEXT.MESSAGE_TEXT + " - " + split_data[-1]
					else:
						CONVERTED_MSG = SYMSGS_MSG_TEXT.MESSAGE_TEXT

					Modi_integration_status.append(CONVERTED_MSG)
					
					SYELOG_tableInfo = SqlHelper.GetTable("SYELOG")
					GuidQuery = SqlHelper.GetFirst("SELECT CONVERT(VARCHAR(4000),NEWID()) AS A")
					Dit = {}
					Dit["ERROR_LOGS_RECORD_ID"] = GuidQuery.A
					Dit["ERRORMESSAGE_RECORD_ID"] = SYMSGS_MSG_TEXT.REC_ID
					Dit["ERRORMESSAGE_DESCRIPTION"] = SYMSGS_MSG_TEXT.MESSAGE_TEXT
					Dit["OBJECT_RECORD_ID"] = SYMSGS_MSG_TEXT.OBJECT_RECORD_ID
					Dit["OBJECT_TYPE"] = SYMSGS_MSG_TEXT.MESSAGE_TYPE
					Dit["OBJECT_NAME"] = SYMSGS_MSG_TEXT.OBJECT_APINAME
					if len(split_data) > 1:
						Dit["OBJECT_VALUE"] = split_data[-1]
					if len(split_data) == 1:
						Dit["OBJECT_VALUE"] = ""
					Dit["CPQTABLEENTRYDATEADDED"] = Modi_date
					Dit["CPQTABLEENTRYADDEDBY"] = User.UserName
					SYELOG_tableInfo.AddRow(Dit)
				sqlInfo = SqlHelper.Upsert(SYELOG_tableInfo)
				if str(ins.sap_part_number) in Dt:
					for data in Modi_integration_status:
						if data not in Dt[ins.sap_part_number]:
							Dt[ins.sap_part_number].append(data)
				else:
					Dt[ins.sap_part_number] = Modi_integration_status
					
				for sap_part_number in Dt:
					inte_status_info = ""
					# Log.Info("232323 sap_part_number--->"+str(sap_part_number))
					for data in Dt[sap_part_number]:
						inte_status_info = inte_status_info + data + "||"

					Error_list.append(sap_part_number + "--" + inte_status_info[:-2])

				ErrorQueryItems = SqlHelper.GetFirst(""+ str(Parameter1.QUERY_CRITERIA_1)+ "  "+str(Temp_Table_Name)+" SET PROCESS_STATUS = ''UPLOADED'' WHERE SESSION_ID  IN "+ str(Session_lst).replace("'","''")+ "  '")



		
		else:
			Error_check = 0
	Log.Info("456789 ---->"+str(Error_list))		
	if len(Error_list) > 0:
	
		Header = "<!DOCTYPE html><html><head><style>table {font-family: Calibri, sans-serif; border-collapse: collapse; width: 75%}td, th {  border: 1px solid #dddddd;  text-align: left; padding: 8px;}.im {color: #222;}tr:nth-child(even) {background-color: #dddddd;}</style></head><body>"

		Table_start = "<p>Hi Team,<br>Please find the below exceptions for your reference</p><table class='table table-bordered'><tr><th>SNO</th><th>SAP_PART_NUMBER</th><th>ERROR MESSAGE</th></tr>"
		Table_End = "</table><p><strong>Note : </strong>Please do not reply to this email.</p></body></html>"
		Table_info = ""
		unique_Error_list = set(Error_list)
		for indx, data in enumerate(unique_Error_list, 1):
			data = data.split("--")
			Table_record = (
				"<tr>"
				+ "<td>"
				+ str(indx)
				+ "</td>"
				+ "<td>"
				+ str(data[0])
				+ "</td>"
				+ "<td>"
				+ str(data[-1])
				+ "</td>"
				+ "</tr>"
			)
			Table_info = Table_info + Table_record

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
		msg.Subject = "AMAT INTEGRATION MATMAS EXCEPTIONS - CPQ TST"
		msg.IsBodyHtml = True
		msg.Body = Error_Info

		# CC Emails	
		copyEmail5 = MailAddress("suresh.muniyandi@bostonharborconsulting.com")
		msg.CC.Add(copyEmail5)
		
		copyEmail4 = MailAddress("baji.baba@bostonharborconsulting.com")
		msg.CC.Add(copyEmail4)
		
		# Send the message
		mailClient.Send(msg)

	#Deleting dynamically created table(ERROR_LOG
	#TempTable = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(Temp_Table_Name)+"'' ) BEGIN DROP TABLE "+str(Temp_Table_Name)+" END'")
	ERRLOG_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''TEMP_PROCESS'' ) BEGIN DROP TABLE TEMP_PROCESS END ' ")
	ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "400", "Message": "Data successfully uploaded"}]})
		
except:

	#Deleting dynamically created table(ERROR_LOG)
	Temp_Table_Name = 'ERROR_LOG'
	TempTable = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(Temp_Table_Name)+"'' ) BEGIN DROP TABLE "+str(Temp_Table_Name)+" END'")

	Log.Info("BULK MATMAS ERROR---->:" + str(sys.exc_info()[1]))
	Log.Info("BULK MATMAS ERROR LINE NO---->:" + str(sys.exc_info()[-1].tb_lineno))
	ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "400", "Message": str(sys.exc_info()[1])}]})
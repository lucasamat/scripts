# =========================================================================================================================================
#   __script_name : MAPOSTFLBK.PY
#   __script_description : THIS SCRIPT IS USED TO  GET THE DATA FROM FAB LOCATION STAGING TABLE TO FAB LOCATION MAIN TABLE
#   __primary_author__ : BAJI
#   __create_date :
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================

import sys
import datetime

clr.AddReference("System.Net")
from System.Net import CookieContainer, NetworkCredential, Mail
from System.Net.Mail import SmtpClient, MailAddress, Attachment, MailMessage

today = datetime.datetime.now()
Modi_date = today.strftime("%m/%d/%Y %H:%M:%S %p")

try:

	sessionid = SqlHelper.GetFirst("SELECT NEWID() AS A")
	timestamp_sessionid = "'" + str(sessionid.A) + "'"

	Parameter = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'SELECT' ")
	Parameter1 = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'UPD' ")
	Parameter2 = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'DEL' ")

	#Timestamp update
	primaryQueryItems = SqlHelper.GetFirst(
		""
		+ str(Parameter1.QUERY_CRITERIA_1)
		+ "  MAFBLC_INBOUND set MAFBLC_INBOUND.TIMESTAMP='"
		+ str(timestamp_sessionid)
		+ "' FROM MAFBLC_INBOUND where isnull(MAFBLC_INBOUND.process_status,'''')='''' and isnull(MAFBLC_INBOUND.session_id,'''')<>'''' ' ")
		
	primaryQueryItems = SqlHelper.GetFirst(
		""
		+ str(Parameter1.QUERY_CRITERIA_1)
		+ "  MAFBLC_INBOUND SET PROCESS_STATUS=''DUPLICATE'' FROM MAFBLC_INBOUND (NOLOCK) JOIN (SELECT FAB_LOCATION_ID,MAX(CPQTABLEENTRYID) AS CPQTABLEENTRYID FROM MAFBLC_INBOUND(NOLOCK) GROUP BY FAB_LOCATION_ID HAVING COUNT(CPQTABLEENTRYID)>1)SUB_MAFBLC ON MAFBLC_INBOUND.FAB_LOCATION_ID = SUB_MAFBLC.FAB_LOCATION_ID WHERE MAFBLC_INBOUND.CPQTABLEENTRYID <> SUB_MAFBLC.CPQTABLEENTRYID  ' "
	)

	#Process status updating as "Inprogress"
	primaryQueryItems = SqlHelper.GetFirst(
		""
		+ str(Parameter1.QUERY_CRITERIA_1)
		+ "  MAFBLC_INBOUND set MAFBLC_INBOUND.process_status=''Inprogress'',MAFBLC_INBOUND.integration_status='''',MAFBLC_INBOUND.TIMESTAMP='"
		+ str(timestamp_sessionid)
		+ "' FROM MAFBLC_INBOUND where isnull(MAFBLC_INBOUND.process_status,'''')='''' and isnull(MAFBLC_INBOUND.session_id,'''')<>'''' and MAFBLC_INBOUND.TIMESTAMP='"
		+ str(timestamp_sessionid)
		+ "' ' "
	)

	primaryQueryItems = SqlHelper.GetFirst(
	""
	+ str(Parameter1.QUERY_CRITERIA_1)
	+ "  MAFBLC_INBOUND SET ACCOUNT_ID =CONVERT(INT,ACCOUNT_ID) FROM MAFBLC_INBOUND(NOLOCK) WHERE ISNUMERIC(ACCOUNT_ID)=1  '"
) 	
	primaryQueryItems = SqlHelper.GetFirst(
	""
	+ str(Parameter1.QUERY_CRITERIA_1)
	+ "  MAFBLC_INBOUND SET FAB_LOCATION_ID = ''UNMAPPED'' FROM MAFBLC_INBOUND(NOLOCK) WHERE ISNULL(FAB_LOCATION_ID,'''')='''' '"
)  
	
	primaryQueryItems = SqlHelper.GetFirst(
	""
	+ str(Parameter1.QUERY_CRITERIA_1)
	+ "  MAFBLC_INBOUND SET FAB_LOCATION_NAME = FAB_LOCATION_ID FROM MAFBLC_INBOUND(NOLOCK) WHERE ISNULL(FAB_LOCATION_NAME,'''')='''' '"
)
	

	# MAFBLC VALIDATION  
	# MAFBLC Does not exist validations
	primaryQueryItems = SqlHelper.GetFirst(
		""
		+ str(Parameter1.QUERY_CRITERIA_1)
		+ "  MAFBLC_INBOUND SET MAFBLC_INBOUND.INTEGRATION_STATUS = MAFBLC_INBOUND.INTEGRATION_STATUS +convert(nvarchar,SYMSGS.MESSAGE_CODE)+''-''+convert(nvarchar,MAFBLC_INBOUND.ACCOUNT_ID),MAFBLC_INBOUND.PROCESS_STATUS=''ERROR'' FROM MAFBLC_INBOUND(NOLOCK) LEFT JOIN SAACNT (NOLOCK) ON MAFBLC_INBOUND.ACCOUNT_ID = SAACNT.ACCOUNT_ID  LEFT JOIN SYMSGS(NOLOCK) ON SYMSGS.MESSAGE_CODE = ''200017'' WHERE MAFBLC_INBOUND.PROCESS_STATUS IN (''Inprogress'',''ERROR'') AND SYMSGS.OBJECT_APINAME = ''MAFBLC'' AND MAFBLC_INBOUND.TIMESTAMP='"
		+ str(timestamp_sessionid)
		+ "'  AND SAACNT.ACCOUNT_ID IS NULL AND MAFBLC_INBOUND.ACCOUNT_ID <> '''''"
	) 

	primaryQueryItems = SqlHelper.GetFirst(
		""
		+ str(Parameter1.QUERY_CRITERIA_1)
		+ "  MAFBLC_INBOUND SET MAFBLC_INBOUND.INTEGRATION_STATUS = MAFBLC_INBOUND.INTEGRATION_STATUS +convert(nvarchar,SYMSGS.MESSAGE_CODE)+''-''+convert(nvarchar,MAFBLC_INBOUND.DISTRIBUTIONCHANNEL_ID),MAFBLC_INBOUND.PROCESS_STATUS=''ERROR'' FROM MAFBLC_INBOUND(NOLOCK) LEFT JOIN SADSCH (NOLOCK) ON MAFBLC_INBOUND.DISTRIBUTIONCHANNEL_ID = SADSCH.DISTRIBUTIONCHANNEL_ID  LEFT JOIN SYMSGS(NOLOCK) ON SYMSGS.MESSAGE_CODE = ''200018'' WHERE MAFBLC_INBOUND.PROCESS_STATUS IN (''Inprogress'',''ERROR'') AND SYMSGS.OBJECT_APINAME = ''MAFBLC'' AND MAFBLC_INBOUND.TIMESTAMP='"
		+ str(timestamp_sessionid)
		+ "'  AND SADSCH.DISTRIBUTIONCHANNEL_ID IS NULL AND MAFBLC_INBOUND.DISTRIBUTIONCHANNEL_ID <> '''' '"
	)

	primaryQueryItems = SqlHelper.GetFirst(
		""
		+ str(Parameter1.QUERY_CRITERIA_1)
		+ "  MAFBLC_INBOUND SET MAFBLC_INBOUND.INTEGRATION_STATUS = MAFBLC_INBOUND.INTEGRATION_STATUS +convert(nvarchar,SYMSGS.MESSAGE_CODE)+''-''+convert(nvarchar,MAFBLC_INBOUND.DIVISION_ID),MAFBLC_INBOUND.PROCESS_STATUS=''ERROR'' FROM MAFBLC_INBOUND(NOLOCK) LEFT JOIN SADIVN (NOLOCK) ON MAFBLC_INBOUND.DIVISION_ID = SADIVN.DIVISION_ID  LEFT JOIN SYMSGS(NOLOCK) ON SYMSGS.MESSAGE_CODE = ''200019'' WHERE MAFBLC_INBOUND.PROCESS_STATUS IN (''Inprogress'',''ERROR'') AND SYMSGS.OBJECT_APINAME = ''MAFBLC'' AND MAFBLC_INBOUND.TIMESTAMP='"
		+ str(timestamp_sessionid)
		+ "'  AND SADIVN.DIVISION_ID IS NULL  AND MAFBLC_INBOUND.DIVISION_ID <> '''' '"
	)

	primaryQueryItems = SqlHelper.GetFirst(
		""
		+ str(Parameter1.QUERY_CRITERIA_1)
		+ "  MAFBLC_INBOUND SET MAFBLC_INBOUND.INTEGRATION_STATUS = MAFBLC_INBOUND.INTEGRATION_STATUS +convert(nvarchar,SYMSGS.MESSAGE_CODE)+''-''+convert(nvarchar,MAFBLC_INBOUND.MNT_PLANT_ID),MAFBLC_INBOUND.PROCESS_STATUS=''ERROR'' FROM MAFBLC_INBOUND(NOLOCK) LEFT JOIN MAPLNT (NOLOCK) ON MAFBLC_INBOUND.MNT_PLANT_ID = MAPLNT.PLANT_ID  LEFT JOIN SYMSGS(NOLOCK) ON SYMSGS.MESSAGE_CODE = ''200020'' WHERE MAFBLC_INBOUND.PROCESS_STATUS IN (''Inprogress'',''ERROR'') AND SYMSGS.OBJECT_APINAME = ''MAFBLC'' AND MAFBLC_INBOUND.TIMESTAMP='"
		+ str(timestamp_sessionid)
		+ "'  AND MAPLNT.PLANT_ID IS NULL  AND MAFBLC_INBOUND.MNT_PLANT_ID <> ''''  '"
	)

	primaryQueryItems = SqlHelper.GetFirst(
		""
		+ str(Parameter1.QUERY_CRITERIA_1)
		+ "  MAFBLC_INBOUND SET MAFBLC_INBOUND.INTEGRATION_STATUS = MAFBLC_INBOUND.INTEGRATION_STATUS +convert(nvarchar,SYMSGS.MESSAGE_CODE)+''-''+convert(nvarchar,MAFBLC_INBOUND.SALESORG_ID),MAFBLC_INBOUND.PROCESS_STATUS=''ERROR'' FROM MAFBLC_INBOUND(NOLOCK) LEFT JOIN SASORG (NOLOCK) ON MAFBLC_INBOUND.SALESORG_ID = SASORG.SALESORG_ID  LEFT JOIN SYMSGS(NOLOCK) ON SYMSGS.MESSAGE_CODE = ''200021'' WHERE MAFBLC_INBOUND.PROCESS_STATUS IN (''Inprogress'',''ERROR'') AND SYMSGS.OBJECT_APINAME = ''MAFBLC'' AND MAFBLC_INBOUND.TIMESTAMP='"
		+ str(timestamp_sessionid)
		+ "'  AND SASORG.SALESORG_ID IS NULL  AND MAFBLC_INBOUND.SALESORG_ID <> '''' '"
	)

	primaryQueryItems = SqlHelper.GetFirst(
		""
		+ str(Parameter1.QUERY_CRITERIA_1)
		+ "  MAFBLC_INBOUND SET MAFBLC_INBOUND.INTEGRATION_STATUS = MAFBLC_INBOUND.INTEGRATION_STATUS +convert(nvarchar,SYMSGS.MESSAGE_CODE)+''-''+convert(nvarchar,MAFBLC_INBOUND.FABCATEGORY_ID),MAFBLC_INBOUND.PROCESS_STATUS=''ERROR'' FROM MAFBLC_INBOUND(NOLOCK) LEFT JOIN MAEQCT (NOLOCK) ON MAFBLC_INBOUND.FABCATEGORY_ID = MAEQCT.EQUIPMENTCATEGORY_ID  LEFT JOIN SYMSGS(NOLOCK) ON SYMSGS.MESSAGE_CODE = ''200022'' WHERE MAFBLC_INBOUND.PROCESS_STATUS IN (''Inprogress'',''ERROR'') AND SYMSGS.OBJECT_APINAME = ''MAFBLC'' AND MAFBLC_INBOUND.TIMESTAMP='"
		+ str(timestamp_sessionid)
		+ "'  AND MAEQCT.EQUIPMENTCATEGORY_ID IS NULL  AND MAFBLC_INBOUND.FABCATEGORY_ID <> '''' '"
	)

	# MAFBLC Mandatory validations
	primaryQueryItems = SqlHelper.GetFirst(
		""
		+ str(Parameter1.QUERY_CRITERIA_1)
		+ "  MAFBLC_INBOUND SET MAFBLC_INBOUND.INTEGRATION_STATUS = MAFBLC_INBOUND.INTEGRATION_STATUS + ''||''+convert(nvarchar,SYMSGS.MESSAGE_CODE)+''-''+convert(nvarchar,MAFBLC_INBOUND.ACCOUNT_ID),MAFBLC_INBOUND.PROCESS_STATUS=''ERROR'' FROM MAFBLC_INBOUND(NOLOCK) LEFT JOIN SYMSGS(NOLOCK) ON SYMSGS.MESSAGE_CODE = ''200023'' WHERE MAFBLC_INBOUND.PROCESS_STATUS IN (''Inprogress'',''ERROR'') AND SYMSGS.OBJECT_APINAME = ''MAFBLC'' AND MAFBLC_INBOUND.TIMESTAMP='"
		+ str(timestamp_sessionid)
		+ "' AND  ISNULL(ACCOUNT_ID,'''') = '''' '"
	)

	primaryQueryItems = SqlHelper.GetFirst(
		""
		+ str(Parameter1.QUERY_CRITERIA_1)
		+ "  MAFBLC_INBOUND SET MAFBLC_INBOUND.INTEGRATION_STATUS = MAFBLC_INBOUND.INTEGRATION_STATUS + ''||''+convert(nvarchar,SYMSGS.MESSAGE_CODE)+''-''+convert(nvarchar,MAFBLC_INBOUND.DISTRIBUTIONCHANNEL_ID),MAFBLC_INBOUND.PROCESS_STATUS=''ERROR'' FROM MAFBLC_INBOUND(NOLOCK) LEFT JOIN SYMSGS(NOLOCK) ON SYMSGS.MESSAGE_CODE = ''200024'' WHERE MAFBLC_INBOUND.PROCESS_STATUS IN (''Inprogress'',''ERROR'') AND SYMSGS.OBJECT_APINAME = ''MAFBLC'' AND MAFBLC_INBOUND.TIMESTAMP='"
		+ str(timestamp_sessionid)
		+ "' AND  ISNULL(DISTRIBUTIONCHANNEL_ID,'''') = '''' '"
	)

	primaryQueryItems = SqlHelper.GetFirst(
		""
		+ str(Parameter1.QUERY_CRITERIA_1)
		+ "  MAFBLC_INBOUND SET MAFBLC_INBOUND.INTEGRATION_STATUS = MAFBLC_INBOUND.INTEGRATION_STATUS + ''||''+convert(nvarchar,SYMSGS.MESSAGE_CODE)+''-''+convert(nvarchar,MAFBLC_INBOUND.DIVISION_ID),MAFBLC_INBOUND.PROCESS_STATUS=''ERROR'' FROM MAFBLC_INBOUND(NOLOCK) LEFT JOIN SYMSGS(NOLOCK) ON SYMSGS.MESSAGE_CODE = ''200025'' WHERE MAFBLC_INBOUND.PROCESS_STATUS IN (''Inprogress'',''ERROR'') AND SYMSGS.OBJECT_APINAME = ''MAFBLC'' AND MAFBLC_INBOUND.TIMESTAMP='"
		+ str(timestamp_sessionid)
		+ "' AND  ISNULL(DIVISION_ID,'''') = '''' '"
	)

	primaryQueryItems = SqlHelper.GetFirst(
		""
		+ str(Parameter1.QUERY_CRITERIA_1)
		+ "  MAFBLC_INBOUND SET MAFBLC_INBOUND.INTEGRATION_STATUS = MAFBLC_INBOUND.INTEGRATION_STATUS + ''||''+convert(nvarchar,SYMSGS.MESSAGE_CODE)+''-''+convert(nvarchar,MAFBLC_INBOUND.FAB_LOCATION_ID),MAFBLC_INBOUND.PROCESS_STATUS=''ERROR'' FROM MAFBLC_INBOUND(NOLOCK) LEFT JOIN SYMSGS(NOLOCK) ON SYMSGS.MESSAGE_CODE = ''200026'' WHERE MAFBLC_INBOUND.PROCESS_STATUS IN (''Inprogress'',''ERROR'') AND SYMSGS.OBJECT_APINAME = ''MAFBLC'' AND MAFBLC_INBOUND.TIMESTAMP='"
		+ str(timestamp_sessionid)
		+ "' AND  ISNULL(FAB_LOCATION_ID,'''') = '''' '"
	)

	primaryQueryItems = SqlHelper.GetFirst(
		""
		+ str(Parameter1.QUERY_CRITERIA_1)
		+ "  MAFBLC_INBOUND SET MAFBLC_INBOUND.INTEGRATION_STATUS = MAFBLC_INBOUND.INTEGRATION_STATUS + ''||''+convert(nvarchar,SYMSGS.MESSAGE_CODE)+''-''+convert(nvarchar,MAFBLC_INBOUND.FAB_LOCATION_NAME),MAFBLC_INBOUND.PROCESS_STATUS=''ERROR'' FROM MAFBLC_INBOUND(NOLOCK) LEFT JOIN SYMSGS(NOLOCK) ON SYMSGS.MESSAGE_CODE = ''200027'' WHERE MAFBLC_INBOUND.PROCESS_STATUS IN (''Inprogress'',''ERROR'') AND SYMSGS.OBJECT_APINAME = ''MAFBLC'' AND MAFBLC_INBOUND.TIMESTAMP='"
		+ str(timestamp_sessionid)
		+ "' AND  ISNULL(FAB_LOCATION_NAME,'''') = '''' '"
	)

	primaryQueryItems = SqlHelper.GetFirst(
		""
		+ str(Parameter1.QUERY_CRITERIA_1)
		+ "  MAFBLC_INBOUND SET MAFBLC_INBOUND.INTEGRATION_STATUS = MAFBLC_INBOUND.INTEGRATION_STATUS + ''||''+convert(nvarchar,SYMSGS.MESSAGE_CODE)+''-''+convert(nvarchar,MAFBLC_INBOUND.MNT_PLANT_ID),MAFBLC_INBOUND.PROCESS_STATUS=''ERROR'' FROM MAFBLC_INBOUND(NOLOCK) LEFT JOIN SYMSGS(NOLOCK) ON SYMSGS.MESSAGE_CODE = ''200028'' WHERE MAFBLC_INBOUND.PROCESS_STATUS IN (''Inprogress'',''ERROR'') AND SYMSGS.OBJECT_APINAME = ''MAFBLC'' AND MAFBLC_INBOUND.TIMESTAMP='"
		+ str(timestamp_sessionid)
		+ "' AND  ISNULL(MNT_PLANT_ID,'''') = '''' '"
	)

	primaryQueryItems = SqlHelper.GetFirst(
		""
		+ str(Parameter1.QUERY_CRITERIA_1)
		+ "  MAFBLC_INBOUND SET MAFBLC_INBOUND.INTEGRATION_STATUS = MAFBLC_INBOUND.INTEGRATION_STATUS + ''||''+convert(nvarchar,SYMSGS.MESSAGE_CODE)+''-''+convert(nvarchar,MAFBLC_INBOUND.SALESORG_ID),MAFBLC_INBOUND.PROCESS_STATUS=''ERROR'' FROM MAFBLC_INBOUND(NOLOCK) LEFT JOIN SYMSGS(NOLOCK) ON SYMSGS.MESSAGE_CODE = ''200029'' WHERE MAFBLC_INBOUND.PROCESS_STATUS IN (''Inprogress'',''ERROR'') AND SYMSGS.OBJECT_APINAME = ''MAFBLC'' AND MAFBLC_INBOUND.TIMESTAMP='"
		+ str(timestamp_sessionid)
		+ "' AND  ISNULL(SALES_ORG_ID,'''') = '''' '"
	)

	primaryQueryItems = SqlHelper.GetFirst(
		""
		+ str(Parameter1.QUERY_CRITERIA_1)
		+ "  MAFBLC_INBOUND SET MAFBLC_INBOUND.INTEGRATION_STATUS = MAFBLC_INBOUND.INTEGRATION_STATUS + ''||''+convert(nvarchar,SYMSGS.MESSAGE_CODE)+''-''+convert(nvarchar,MAFBLC_INBOUND.FABCATEGORY_ID),MAFBLC_INBOUND.PROCESS_STATUS=''ERROR'' FROM MAFBLC_INBOUND(NOLOCK) LEFT JOIN SYMSGS(NOLOCK) ON SYMSGS.MESSAGE_CODE = ''200030'' WHERE MAFBLC_INBOUND.PROCESS_STATUS IN (''Inprogress'',''ERROR'') AND SYMSGS.OBJECT_APINAME = ''MAFBLC'' AND MAFBLC_INBOUND.TIMESTAMP='"
		+ str(timestamp_sessionid)
		+ "' AND  ISNULL(FABCATEGORY_ID,'''') = '''' '"
	)

	# Validation Completed and updating process status as "READY FOR UPLOAD"
	primaryQueryItems = SqlHelper.GetFirst(
		""
		+ str(Parameter1.QUERY_CRITERIA_1)
		+ "  MAFBLC_INBOUND SET PROCESS_STATUS=''READY FOR UPLOAD'' WHERE PROCESS_STATUS=''Inprogress'' AND TIMESTAMP='"
		+ str(timestamp_sessionid)
		+ "' AND ISNULL(INTEGRATION_STATUS,'''')='''' '"
	)

	# Updating Error sessions in "ERROR_SESSION" table

	# Dynamically creating ERROR SESSION table
	Temp_Table_Name = 'ERROR_SESSION'

	ERRLOG_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(Temp_Table_Name)+"'' ) BEGIN DROP TABLE "+str(Temp_Table_Name)+" END  ' ")

	TempTable = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(Temp_Table_Name)+"'' ) BEGIN DROP TABLE "+str(Temp_Table_Name)+" END CREATE TABLE "+str(Temp_Table_Name)+" (SESSION_ID VARCHAR(100),INTEGRATION_TYPE VARCHAR(100) ,PROCESS_STATUS VARCHAR(100) ,ERROR_MESSAGE VARCHAR(4000),ERROR_DESCRIPTION VARCHAR(4000),TIMESTAMP VARCHAR(250),CpqTableEntryDateModified date)'")


	primaryQueryItems = SqlHelper.GetFirst(
		""
		+ str(Parameter.QUERY_CRITERIA_1)
		+ "   ERROR_SESSION (SESSION_ID,CpqTableEntryDateModified) SELECT SUB_ERRLOG.SESSION_ID,getdate() FROM (SELECT DISTINCT MAFBLC_INBOUND.SESSION_ID as SESSION_ID FROM MAFBLC_INBOUND (NOLOCK) WHERE  ISNULL(MAFBLC_INBOUND.PROCESS_STATUS,'''')=''ERROR'' )SUB_ERRLOG  ' "
	)

	# Updating process status as "ERROR" SUB_ERRLOG
	primaryQueryItems = SqlHelper.GetFirst(
		""
		+ str(Parameter1.QUERY_CRITERIA_1)
		+ "  MAFBLC_INBOUND SET PROCESS_STATUS=''ERROR'' FROM MAFBLC_INBOUND JOIN ERROR_SESSION  ON MAFBLC_INBOUND.SESSION_ID = ERROR_SESSION.SESSION_ID WHERE MAFBLC_INBOUND.TIMESTAMP='"
		+ str(timestamp_sessionid)
		+ "' '"
	)



	#UPLOAD 
	# MAFBLC Update
	primaryQueryItems = SqlHelper.GetFirst(
	""
	+ str(Parameter1.QUERY_CRITERIA_1)
	+ "  MAFBLC SET MAFBLC.CpqTableEntryModifiedBy = ''"
	+ str(User.Id)
	+ "'',MAFBLC.CpqTableEntryDateModified = GetDate(),MAFBLC.FABCATEGORY_ID = MAEQCT.EQUIPMENTCATEGORY_ID,MAFBLC.FABCATEGORY_NAME = MAEQCT.EQUIPMENTCATEGORY_DESCRIPTION,MAFBLC.FABCATEGORY_RECORD_ID = MAEQCT.EQUIPMENT_CATEGORY_RECORD_ID,MAFBLC.MNT_PLANT_ID = MAPLNT.PLANT_ID,MAFBLC.MNT_PLANT_NAME = MAPLNT.PLANT_NAME,MAFBLC.MNT_PLANT_RECORD_ID = MAPLNT.PLANT_RECORD_ID,BLUEBOOK= MAFBLC_INBOUND.BLUEBOOK,BLUEBOOK_RECORD_ID=SABLBK.BLUEBOOK_RECORD_ID,FAB_LOCATION_NAME = MAFBLC_INBOUND.FAB_LOCATION_NAME,ACCOUNT_ID = SAACNT.ACCOUNT_ID,ACCOUNT_NAME = SAACNT.ACCOUNT_NAME,ACCOUNT_RECORD_ID = SAACNT.ACCOUNT_RECORD_ID,CITY = MAFBLC_INBOUND.CITY,ADDRESS_1 = MAFBLC_INBOUND.ADDRESS_1,COUNTRY = MAFBLC_INBOUND.COUNTRY,COUNTRY_RECORD_ID = SACTRY.COUNTRY_RECORD_ID,POSTAL_CODE= MAFBLC_INBOUND.POSTAL_CODE FROM MAFBLC_INBOUND(NOLOCK)  JOIN MAFBLC (NOLOCK) ON MAFBLC_INBOUND.FAB_LOCATION_ID = MAFBLC.FAB_LOCATION_ID JOIN MAPLNT (NOLOCK) ON MAFBLC_INBOUND.MNT_PLANT_ID = MAPLNT.PLANT_ID JOIN MAEQCT (NOLOCK) ON MAFBLC_INBOUND.FABCATEGORY_ID = MAEQCT.EQUIPMENTCATEGORY_ID LEFT JOIN SABLBK SABLBK(NOLOCK) ON MAFBLC_INBOUND.BLUEBOOK = SABLBK.BLUEBOOK JOIN SAACNT SAACNT(NOLOCK) ON MAFBLC_INBOUND.ACCOUNT_ID = SAACNT.ACCOUNT_ID LEFT JOIN SACTRY (NOLOCK) ON MAFBLC_INBOUND.COUNTRY = SACTRY.COUNTRY WHERE  MAFBLC_INBOUND.TIMESTAMP='"+ str(timestamp_sessionid)+ "'  AND ISNULL(MAFBLC_INBOUND.INTEGRATION_STATUS,'''') ='''' AND ISNULL(PROCESS_STATUS,'''')=''READY FOR UPLOAD'' '"	)

	# MAFBLC Add
	primaryQueryItems = SqlHelper.GetFirst(
		""
		+ str(Parameter.QUERY_CRITERIA_1)
		+ "   MAFBLC (ACCOUNT_ID,ACCOUNT_NAME,ACCOUNT_RECORD_ID,ADDRESS_1,ADDRESS_2,CITY,COUNTRY,COUNTRY_RECORD_ID,DISTRIBUTIONCHANNEL_ID,DISTRIBUTIONCHANNEL_RECORD_ID,DIVISION_ID,DIVISION_RECORD_ID,FAB_LOCATION_ID,FAB_LOCATION_NAME, MNT_PLANT_ID,MNT_PLANT_RECORD_ID,POSTAL_CODE,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,STATE,STATE_RECORD_ID,STATUS,CATEGORY_TYPE,MNT_PLANT_NAME,PHONE,FABCATEGORY_ID,FABCATEGORY_NAME,FABCATEGORY_RECORD_ID,BLUEBOOK_RECORD_ID,BLUEBOOK,FAB_LOCATION_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED)SELECT SUB_MAFBLC.*, CONVERT(VARCHAR(4000),NEWID()),''"
		+ str(User.UserName)
		+ "'',GETDATE() FROM (SELECT DISTINCT SAACNT.ACCOUNT_ID,SAACNT.ACCOUNT_NAME,SAACNT.ACCOUNT_RECORD_ID,MAFBLC_INBOUND.ADDRESS_1,MAFBLC_INBOUND.ADDRESS_2,MAFBLC_INBOUND.CITY,MAFBLC_INBOUND.COUNTRY,SACTRY.COUNTRY_RECORD_ID,SADSCH.DISTRIBUTIONCHANNEL_ID,SADSCH.DISTRIBUTION_CHANNEL_RECORD_ID AS DISTRIBUTIONCHANNEL_RECORD_ID,	SADIVN.DIVISION_ID,SADIVN.DIVISION_RECORD_ID,MAFBLC_INBOUND.FAB_LOCATION_ID,MAFBLC_INBOUND.FAB_LOCATION_NAME, MAPLNT.PLANT_ID AS MNT_PLANT_ID,MAPLNT.PLANT_RECORD_ID AS MNT_PLANT_RECORD_ID,MAFBLC_INBOUND.POSTAL_CODE,SASORG.SALESORG_ID,SASORG.SALESORG_NAME,SASORG.SALES_ORG_RECORD_ID AS SALESORG_RECORD_ID,SACYST.STATE,SACYST.STATE_RECORD_ID,MAFBLC_INBOUND.STATUS,MAFBLC_INBOUND.CATEGORY_TYPE,MAPLNT.PLANT_NAME AS MNT_PLANT_NAME,MAFBLC_INBOUND.PHONE,MAEQCT.EQUIPMENTCATEGORY_ID AS FABCATEGORY_ID,MAEQCT.EQUIPMENTCATEGORY_DESCRIPTION AS  FABCATEGORY_NAME, MAEQCT.EQUIPMENT_CATEGORY_RECORD_ID AS FABCATEGORY_RECORD_ID,SABLBK.BLUEBOOK_RECORD_ID,MAFBLC_INBOUND.BLUEBOOK FROM MAFBLC_INBOUND(NOLOCK)  JOIN SAACNT(NOLOCK) ON MAFBLC_INBOUND.ACCOUNT_ID = SAACNT.ACCOUNT_ID JOIN SACTRY (NOLOCK) ON MAFBLC_INBOUND.COUNTRY = SACTRY.COUNTRY LEFT JOIN SADSCH(NOLOCK) ON MAFBLC_INBOUND.DISTRIBUTIONCHANNEL_ID = SADSCH.DISTRIBUTIONCHANNEL_ID LEFT JOIN SADIVN(NOLOCK) ON MAFBLC_INBOUND.DIVISION_ID = SADIVN.DIVISION_ID LEFT JOIN MAPLNT(NOLOCK) ON MAFBLC_INBOUND.MNT_PLANT_ID = MAPLNT.PLANT_ID JOIN SASORG(NOLOCK) ON MAFBLC_INBOUND.SALESORG_ID = SASORG.SALESORG_ID LEFT JOIN MAEQCT(NOLOCK)  ON MAFBLC_INBOUND.FABCATEGORY_ID = MAEQCT.EQUIPMENTCATEGORY_ID LEFT JOIN SACYST (NOLOCK) ON MAFBLC_INBOUND.STATE = SACYST.STATE  LEFT JOIN SABLBK SABLBK(NOLOCK) ON MAFBLC_INBOUND.BLUEBOOK = SABLBK.BLUEBOOK  WHERE  MAFBLC_INBOUND.TIMESTAMP='"+ str(timestamp_sessionid)+ "'  AND ISNULL(MAFBLC_INBOUND.INTEGRATION_STATUS,'''') ='''' AND ISNULL(MAFBLC_INBOUND.PROCESS_STATUS,'''') =''READY FOR UPLOAD'' )SUB_MAFBLC LEFT JOIN MAFBLC(NOLOCK) ON SUB_MAFBLC.FAB_LOCATION_ID = MAFBLC.FAB_LOCATION_ID WHERE MAFBLC.FAB_LOCATION_ID IS NULL '" )
	
	primaryQueryItems = SqlHelper.GetFirst(
		""
		+ str(Parameter1.QUERY_CRITERIA_1)
		+ "  MAFBLC_INBOUND SET PROCESS_STATUS=''UPLOADED'' WHERE PROCESS_STATUS=''READY FOR UPLOAD'' AND TIMESTAMP='"
		+ str(timestamp_sessionid)
		+ "' AND ISNULL(INTEGRATION_STATUS,'''')='''' '"
	)

	primaryQueryItems = SqlHelper.GetFirst(
                        ""
                        + str(Parameter1.QUERY_CRITERIA_1)
                        + "  A SET CRM_FABLOCATION_ID = ACCOUNT_ID FROM MAFBLC A(NOLOCK) JOIN SAACNT B (NOLOCK) ON A.FAB_LOCATION_ID = B.LEGACY_FBL_ID WHERE ACCOUNTGROUP_ID = ''ZFAB'' ' ")
	
	primaryQueryItems = SqlHelper.GetFirst(
                        ""
                        + str(Parameter1.QUERY_CRITERIA_1)
                        + "  A SET ACCOUNT_ID = B.ACCOUNT_ID,ACCOUNT_RECORD_ID = B.ACCOUNT_RECORD_ID,ACCOUNT_NAME = B.ACCOUNT_NAME FROM MAEQUP (NOLOCK) A JOIN MAFBLC B(NOLOCK) ON A.FABLOCATION_ID = B.FAB_LOCATION_ID WHERE ISNULL(A.ACCOUNT_ID,'''')='''' ' ")
	
	# ERROR MESSAGE SAVING IN SYELOG
	Error_list = []
	Resp_msg = {}
	Lst_resp = []
	Email_flag = 1
	while Email_flag == 1:
		Error_primaryQuery = SqlHelper.GetList(
			"select top 10 SESSION_ID from ERROR_SESSION(NOLOCK) where ISNULL(PROCESS_STATUS,'')= '' and isnull(SESSION_ID,'')<>''  "
		)

		Session_lst_count = []
		for data in Error_primaryQuery:
			Session_lst_count.append(data.SESSION_ID)

		Session_lst = tuple(Session_lst_count)
		if len(Session_lst_count) == 1:
			Session_lst = "('" + Session_lst_count[0] + "')"

		if len(Session_lst_count) > 0:

			primaryQueryItems = SqlHelper.GetList(
				"select distinct FAB_LOCATION_ID,integration_status from MAFBLC_INBOUND(nolock) where isnull(integration_status,'')<>'' and session_id in "
				+ str(Session_lst)
				+ "  "
			)

			Dt = {}
			for ins in primaryQueryItems:
				Modi_integration_status = []
				inte_status = str(ins.integration_status).split("||")
				integration_status = set(inte_status)
				integration_status = list(integration_status)
				if "" in integration_status:
					integration_status.remove("")

				SYELOG_tableInfo = SqlHelper.GetTable("SYELOG")
				for uu in integration_status:
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

				if str(ins.FAB_LOCATION_ID) in Dt:
					for data in Modi_integration_status:
						if data not in Dt[ins.FAB_LOCATION_ID]:
							Dt[ins.FAB_LOCATION_ID].append(data)
				else:
					Dt[ins.FAB_LOCATION_ID] = Modi_integration_status
			for FAB_LOCATION_ID in Dt:
				inte_status_info = ""
				for data in Dt[FAB_LOCATION_ID]:
					inte_status_info = inte_status_info + data + "||"

				Error_list.append(FAB_LOCATION_ID + "--" + inte_status_info[:-2])

			ErrorQueryItems = SqlHelper.GetFirst(""+ str(Parameter1.QUERY_CRITERIA_1)+ "  ERROR_SESSION SET PROCESS_STATUS = ''UPLOADED'',CpqTableEntryDateModified = GetDate() WHERE SESSION_ID  IN "+ str(Session_lst).replace("'","''")+ "  '")

		else:
			Email_flag = 0

	# Deleted dynamically created table
	TempTable = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(Temp_Table_Name)+"'' ) BEGIN DROP TABLE "+str(Temp_Table_Name)+" END'")

	if len(Error_list) > 0:

		Header = "<!DOCTYPE html><html><head><style>table {font-family: Calibri, sans-serif; border-collapse: collapse; width: 75%}td, th {  border: 1px solid #dddddd;  text-align: left; padding: 8px;}.im {color: #222;}tr:nth-child(even) {background-color: #dddddd;}</style></head><body>"

		Table_start = "<p>Hi Team,<br>Please find the below exceptions for your reference</p><table class='table table-bordered'><tr><th>SNO</th><th>FAB_LOCATION_ID</th><th>ERROR MESSAGE</th></tr>"
		Table_End = "</table><p><strong>Note : </strong>Please do not reply to this email.</p></body></html>"
		Table_info = ""
		unique_Error_list = set(Error_list)
		for indx, data in enumerate(unique_Error_list, 1):
			data = str(data).split("--")
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

		LOGIN_CRE = SqlHelper.GetFirst("SELECT USER_NAME AS Username,Password FROM SYCONF where Domain ='SUPPORT_MAIL'")

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
		msg.Subject = "FAB LOCATION EXCEPTIONS - AMAT CPQ(X-Tenant)"
		msg.IsBodyHtml = True
		msg.Body = Error_Info

		# CC Emails
		copyEmail = MailAddress("Baji.baba@bostonharborconsulting.com")
		msg.CC.Add(copyEmail)		

		# Send the message
		mailClient.Send(msg)
		Lst_resp.append({"Status": "400", "Message": unique_Error_list})
	else:
		Lst_resp.append({"Status": "200", "Message": "FAB LOCATION DATA SUCCESSFULLY UPLOADED"})

	Resp_msg["Response"] = Lst_resp

	Result = Resp_msg

	
except:

	# Deleted dynamically created table
	Temp_Table_Name = 'ERROR_SESSION'
	TempTable = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(Temp_Table_Name)+"'' ) BEGIN DROP TABLE "+str(Temp_Table_Name)+" END'")
	
	Log.Info("MAPOSTFLBK ERROR---->:" + str(sys.exc_info()[1]))
	Log.Info("MAPOSTFLBK ERROR LINE NO---->:" + str(sys.exc_info()[-1].tb_lineno))
	error_info = {"Response": [{"Status": "400", "Message": str(sys.exc_info()[1])}]}
	Result  = str(error_info)
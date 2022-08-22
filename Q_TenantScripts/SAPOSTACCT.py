# =========================================================================================================================================
#   __script_name : SAPOSTACCT.PY(DEV)
#   __script_description : THIS SCRIPT IS USED TO UPDATE CONTACT_PERSON INFORMATION.
#   __primary_author__ : Baji
#   __create_date : 2021-20-10
#   Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import sys
import datetime

cpqentryid = ''

try :

	check_flag = 1
	status_flag = 0
	Parameter = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'SELECT' ")	
	Parameter1 = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'UPD' ")
	Parameter2 = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'DEL' ")
	while check_flag == 1:
		Jsonquery = SqlHelper.GetList("SELECT INTEGRATION_PAYLOAD,CpqTableEntryId from SYINPL(NOLOCK) WHERE INTEGRATION_NAME = 'CONTACT_PERSON' AND ISNULL(STATUS,'')='' ")
		if len(Jsonquery) > 0:
			for json_data in Jsonquery:
				splited_list = str(json_data.INTEGRATION_PAYLOAD)
				rebuilt_data = eval(splited_list)
				cpqentryid = str(json_data.CpqTableEntryId)

				
				primaryQuerysession =  SqlHelper.GetFirst("SELECT NEWID() AS A")
				today = datetime.datetime.now()
				Modi_date = today.strftime("%m/%d/%Y %H:%M:%S %p")


				if len(rebuilt_data) != 0:      

					rebuilt_data = rebuilt_data["CPQ_Columns"]
					Table_Names = rebuilt_data.keys()
					
					
					for tn in Table_Names:
						if tn in rebuilt_data:
							status_flag = 1	
							if str(tn).upper() == "SAACCT":
								if str(type(rebuilt_data[tn])) == "<type 'dict'>":
									Tbl_data = [rebuilt_data[tn]]
								else:
									Tbl_data = rebuilt_data[tn]
									
								for record_dict in Tbl_data:	
									
									for col in ['ACCOUNT_ID','FIRST_NAME','LAST_NAME','CONTACT_ID','PHONE','EMAIL','MOBILE','FAX']:
										if col not in record_dict:
											record_dict[col] = ''					
											
									primaryQueryItems = SqlHelper.GetFirst( ""+ str(Parameter.QUERY_CRITERIA_1)+ " SAACNT_INBOUND (CONTACT_ID,PHONE,ACCOUNT_ID,FIRSTNAME,LASTNAME,EMAIL,FAX,MOBILE,INTEGRATION_OBJECT,cpqtableentrydatemodified,SESSION_ID)  select  N''"+str(record_dict['CONTACT_ID'])+ "'',''"+str(record_dict['PHONE'])+ "'',''"+str(record_dict['ACCOUNT_ID'])+ "'',N''"+record_dict['FIRST_NAME']+ "'',N''"+record_dict['LAST_NAME']+ "'',N''"+record_dict['EMAIL']+ "'',N''"+record_dict['FAX']+ "'',N''"+record_dict['MOBILE']+ "'',''SAACCT'',''"+ str(Modi_date)+ "'',''"+ str(primaryQuerysession.A)+ "'' ' ")
									
							


									
					primaryItems = SqlHelper.GetFirst(  ""+ str(Parameter1.QUERY_CRITERIA_1)+ "  SYINPL set STATUS = ''PROCESSED'' from SYINPL  (NOLOCK) WHERE CpqTableEntryId  = ''"+str(json_data.CpqTableEntryId)+ "'' AND ISNULL(STATUS ,'''')= '''' ' "    )
					
		
		else:
			check_flag = 0
			
	if status_flag== 1 :  
		#Validations
		#SAACCT

		primaryQueryItems = SqlHelper.GetFirst(
                ""
                + str(Parameter1.QUERY_CRITERIA_1)
                + "  SAACNT_INBOUND SET SAACNT_INBOUND.ERROR = SAACNT_INBOUND.ERROR + ''||''+convert(nvarchar,SYMSGS.MESSAGE_CODE),SAACNT_INBOUND.INTEGRATION_STATUS=''ERROR'' FROM SAACNT_INBOUND(NOLOCK) LEFT JOIN SYMSGS(NOLOCK)  ON SYMSGS.MESSAGE_CODE = ''200121'' AND SAACNT_INBOUND.INTEGRATION_OBJECT= ''SAACCT'' WHERE SAACNT_INBOUND.INTEGRATION_STATUS IN (''Inprogress'',''ERROR'') AND SYMSGS.OBJECT_APINAME = ''SAACCT''  AND ACCOUNT_ID = '''''"
            )
		
		#PREPARING RECORDS TO BE LOADED
		UpdateQueryItems = SqlHelper.GetFirst(
		""
		+ str(Parameter1.QUERY_CRITERIA_1)
		+ "  SAACNT_INBOUND SET INTEGRATION_STATUS = ''READY FOR UPLOAD'' WHERE ISNULL(INTEGRATION_STATUS,'''')='''' AND INTEGRATION_OBJECT = ''SAACCT''  ' ")

		S = SqlHelper.GetFirst("sp_executesql @T=N'update saacnt_inbound set account_id = convert(bigint,account_id)  where isnumeric(account_id)=1  ' ")

		S = SqlHelper.GetFirst("sp_executesql @T=N'update saacnt_inbound set CONTACT_ID = convert(bigint,CONTACT_ID)  where isnumeric(CONTACT_ID)=1  ' ")		

		#Contact Person(SACONT)
		InsertQueryItems = SqlHelper.GetFirst(
        ""
        + str(Parameter.QUERY_CRITERIA_1)
        + " SACONT (CITY,CONTACT_ID,CONTACT_NAME,COUNTRY,COUNTRY_RECORD_ID,ADDRESS,PHONE,POSTAL_CODE,FAX,EMAIL,FIRST_NAME,LAST_NAME,STATE,STATE_RECORD_ID,CPQTABLEENTRYDATEADDED,CONTACT_RECORD_ID)SELECT SUB_SACONT.*,GetDate() ,CONVERT(VARCHAR(4000),NEWID()) FROM (SELECT DISTINCT SAACNT_INBOUND.CITY,SAACNT_INBOUND.CONTACT_ID,(FIRSTNAME+'' ''+LASTNAME) AS CONTACT_NAME,SAACNT.COUNTRY,SAACNT.COUNTRY_RECORD_ID,SAACNT.ADDRESS_1,SAACNT_INBOUND.PHONE,SAACNT.POSTAL_CODE,SAACNT_INBOUND.FAX,SAACNT_INBOUND.EMAIL,SAACNT_INBOUND.FIRSTNAME,SAACNT_INBOUND.LASTNAME,SAACNT.STATE,SAACNT.STATE_RECORD_ID FROM SAACNT_INBOUND(NOLOCK) LEFT JOIN SAACNT(NOLOCK) ON SAACNT_INBOUND.ACCOUNT_ID=SAACNT.ACCOUNT_ID WHERE  SAACNT_INBOUND.INTEGRATION_STATUS = ''READY FOR UPLOAD'' AND ISNULL(SAACNT_INBOUND.INTEGRATION_OBJECT,'''')=''SAACCT''  )SUB_SACONT LEFT JOIN SACONT(NOLOCK)  ON SUB_SACONT.CONTACT_ID=SACONT.CONTACT_ID WHERE  SACONT.CONTACT_ID IS NULL'"
        )

		
		#Update Query    
		UpdateQueryItems = SqlHelper.GetFirst(
		""
		+ str(Parameter1.QUERY_CRITERIA_1)
		+ "  SAACCT SET SAACCT.CpqTableEntryModifiedBy = ''"
		+ str(User.Id)
		+ "'',SAACCT.CpqTableEntryDateModified = GetDate(),SAACCT.ACCOUNT_ID = SAACNT_INBOUND.ACCOUNT_ID,SAACCT.ACCOUNT_NAME = SAACNT.ACCOUNT_NAME,SAACCT.ACCOUNT_RECORD_ID = SAACNT.ACCOUNT_RECORD_ID,SAACCT.CONTACT_ID = SAACNT_INBOUND.CONTACT_ID,SAACCT.CONTACT_NAME = SACONT.CONTACT_NAME,SAACCT.CONTACT_RECORD_ID = SACONT.CONTACT_RECORD_ID,SAACCT.EMAIL = SAACNT_INBOUND.EMAIL,SAACCT.PHONE = SAACNT_INBOUND.PHONE,SAACCT.FAX = SAACNT_INBOUND.FAX FROM SAACNT_INBOUND(NOLOCK) JOIN SAACNT(NOLOCK) ON SAACNT_INBOUND.ACCOUNT_ID=SAACNT.ACCOUNT_ID LEFT JOIN SACONT(NOLOCK) ON SAACNT_INBOUND.CONTACT_ID=SACONT.CONTACT_ID   JOIN SAACCT(NOLOCK)  ON SAACNT_INBOUND.ACCOUNT_ID=SAACCT.ACCOUNT_ID AND SAACNT_INBOUND.CONTACT_ID=SAACCT.CONTACT_ID WHERE  SAACNT_INBOUND.INTEGRATION_STATUS = ''READY FOR UPLOAD'' AND ISNULL(SAACNT_INBOUND.INTEGRATION_OBJECT,'''')=''SAACCT''  ' ")
		
		InsertQueryItems = SqlHelper.GetFirst(
		""
		+ str(Parameter.QUERY_CRITERIA_1)
		+ " SAACCT (ACCOUNT_ID,ACCOUNT_NAME,ACCOUNT_RECORD_ID,CONTACT_ID,CONTACT_NAME,CONTACT_RECORD_ID,EMAIL,FAX,PHONE,ACCOUNT_CONTACTS_RECORD_ID,CPQTABLEENTRYDATEADDED)SELECT SUB_SAACCT.*, CONVERT(VARCHAR(4000),NEWID()),GetDate() FROM (SELECT DISTINCT SAACNT_INBOUND.ACCOUNT_ID,SAACNT.ACCOUNT_NAME,SAACNT.ACCOUNT_RECORD_ID,SAACNT_INBOUND.CONTACT_ID,SACONT.CONTACT_NAME,SACONT.CONTACT_RECORD_ID,SACONT.EMAIL,SAACNT_INBOUND.FAX,SACONT.PHONE FROM SAACNT_INBOUND(NOLOCK) JOIN SAACNT(NOLOCK)  ON SAACNT_INBOUND.ACCOUNT_ID=SAACNT.ACCOUNT_ID JOIN SACONT(NOLOCK) ON  SAACNT_INBOUND.CONTACT_ID=SACONT.CONTACT_ID  WHERE  SAACNT_INBOUND.INTEGRATION_STATUS = ''READY FOR UPLOAD'' AND ISNULL(SAACNT_INBOUND.INTEGRATION_OBJECT,'''')=''SAACCT''  )SUB_SAACCT LEFT JOIN SAACCT(NOLOCK) ON SUB_SAACCT.ACCOUNT_ID=SAACCT.ACCOUNT_ID AND SUB_SAACCT.CONTACT_ID=SAACCT.CONTACT_ID WHERE SAACCT.ACCOUNT_ID IS NULL'"
		)
		
		#Status Update
		UpdateQueryItems = SqlHelper.GetFirst(
		""
		+ str(Parameter1.QUERY_CRITERIA_1)
		+ "  SAACNT_INBOUND SET INTEGRATION_STATUS = ''UPLOADED'' WHERE INTEGRATION_STATUS=''READY FOR UPLOAD'' AND INTEGRATION_OBJECT = ''SAACCT'' ' ")
		
		ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "200", "Message": "Data successfully uploaded"}]})
	
except:
	Log.Info("SAPOSTACCT ERROR---->:" + str(sys.exc_info()[1]))
	Log.Info("SAPOSTACCT ERROR LINE NO---->:" + str(sys.exc_info()[-1].tb_lineno))
	ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "400", "Message": str(sys.exc_info()[1])}]})
	
# =========================================================================================================================================
#   __script_name : MAPOSTMTRL.PY(AMAT)
#   __script_description : THIS SCRIPT IS USED TO UPDATE MATERIALS IN STAGING TABLE.
#   __primary_author__ : BAJI
#   __create_date : 2021-04-09
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import sys
import datetime
import System
from System.Text.Encoding import UTF8
from System import Convert
clr.AddReference("System.Net")
from System.Net import CookieContainer, NetworkCredential, Mail
from System.Net.Mail import SmtpClient, MailAddress, Attachment, MailMessage
from System.Net import HttpWebRequest, NetworkCredential
from System.Net import *
from System.Net import CookieContainer
from System.Net import Cookie
from System.Net import WebRequest
from System.Net import HttpWebResponse
from System import Uri


catch_info = ''
try :

	check_flag = 1
	status_flag = 0
	Parameter = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'SELECT' ")	
	Parameter1 = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'UPD' ")
	Parameter2 = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'DEL' ")
	while check_flag == 1:
		Jsonquery = SqlHelper.GetList("SELECT  INTEGRATION_PAYLOAD,CpqTableEntryId from SYINPL(NOLOCK) WHERE INTEGRATION_NAME = 'MATMAS' AND ISNULL(STATUS,'')=''")
		if len(Jsonquery) > 0:
			for json_data in Jsonquery:

				MATNR = ''
				MATKL = ''
				MEINS = ''
				PRDHA = ''
				MAKTX = ''
				Config_type = ''

				if "Param" in str(json_data.INTEGRATION_PAYLOAD):
					splited_list = str(json_data.INTEGRATION_PAYLOAD).split("'")
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
					
					
					for tn in Table_Names:
						if tn in rebuilt_data:
							if str(tn).upper() == "MAMTRL":
								if str(type(rebuilt_data[tn])) == "<type 'dict'>":
									Tbl_data = [rebuilt_data[tn]]
								else:
									Tbl_data = rebuilt_data[tn]
									
								#Trace.Write("Tbl_data 8888 --->"+str(Tbl_data)) 
									
								for record_dict in Tbl_data:



									for col in ['ERP_CREATE_DATE','HAZMAT_ID','SAP_PART_NUMBER','SAP_DESCRIPTION','MATERIALGROUP_ID','MATERIALSTATUS_ID','MATERIALTYPE_ID','MINIMUM_ORDER_QUANTITY','UNIT_OF_MEASURE','DIVISION_ID','MATERIALCONFIG_TYPE','PROD_INSP_MEMP']: 
										if col not in record_dict:
											record_dict[col] = ''
									
									primaryQueryItems = SqlHelper.GetFirst( ""+ str(Parameter.QUERY_CRITERIA_1)+ " MAMTRL_INBOUND (ERP_CREATE_DATE,HAZMAT_ID,SAP_PART_NUMBER,SAP_DESCRIPTION,MATERIALCONFIG_TYPE,PROD_INSP_MEMO,MATERIALTYPE_ID,MINIMUM_ORDER_QUANTITY,UNIT_OF_MEASURE,DIVISION_ID,MATERIALSTATUS_ID,MATERIALGROUP_ID,cpqtableentrydatemodified,SESSION_ID)  select  ''"+str(record_dict['ERP_CREATE_DATE'])+ "'',''"+str(record_dict['HAZMAT_ID'])+ "'',''"+record_dict['SAP_PART_NUMBER']+ "'',N''"+record_dict['SAP_DESCRIPTION']+ "'',''"+str(record_dict['MATERIALCONFIG_TYPE'])+ "'',N''"+str(record_dict['PROD_INSP_MEMP'])+ "'',''"+str(record_dict['MATERIALTYPE_ID'])+ "'',''"+str(record_dict['MINIMUM_ORDER_QUANTITY'])+ "'',''"+str(record_dict['UNIT_OF_MEASURE'])+ "'',''"+str(record_dict['DIVISION_ID'])+ "'',''"+str(record_dict['MATERIALSTATUS_ID'])+ "'',''"+str(record_dict['MATERIALGROUP_ID'])+ "'',''"+ str(Modi_date)+ "'',''"+ str(primaryQuerysession.A)+ "'' ' ")								
									
									MATNR = record_dict['SAP_PART_NUMBER']
									MATKL = str(record_dict['MATERIALGROUP_ID'])
									MEINS = str(record_dict['UNIT_OF_MEASURE']) 
									MAKTX = record_dict['SAP_DESCRIPTION']
									Config_type = str(record_dict['MATERIALCONFIG_TYPE'])



							elif str(tn).upper() == "MAMSOP":
								if str(type(rebuilt_data[tn])) == "<type 'dict'>":
									Tbl_data = [rebuilt_data[tn]]
								else:
									Tbl_data = rebuilt_data[tn]
									
								for record_dict in Tbl_data:	
									
									for col in ['SAP_PART_NUMBER','SALESORG_ID','MATERIALSTATUS_ID','PLANT_ID','ITMCATGRP_ID','DISTRIBUTIONCHANNEL_ID','DIVISION_ID','IS_SPARES','VALID_FROM','PRICEGROUP_ID','ACCASSIGNMENT_GROUP_ID','SALESUOM_ID']:
										if col not in record_dict:
											record_dict[col] = ''
									
									primaryQueryItems = SqlHelper.GetFirst( ""+ str(Parameter.QUERY_CRITERIA_1)+ " MAMSOP_INBOUND (SAP_PART_NUMBER,SALESORG_ID,MATERIALSTATUS_ID,PLANT_ID,ITMCATGRP_ID,DISTRIBUTIONCHANNEL_ID,DIVISION_ID,IS_SPARES,VALID_FROM,PRICEGROUP_ID,ACCASSIGNMENT_GROUP_ID,SALESUOM_ID,cpqtableentrydatemodified,SESSION_ID)  select  ''"+record_dict['SAP_PART_NUMBER']+ "'',''"+str(record_dict['SALESORG_ID'])+ "'',''"+str(record_dict['MATERIALSTATUS_ID'])+ "'',''"+str(record_dict['PLANT_ID'])+ "'',''"+str(record_dict['ITMCATGRP_ID'])+ "'',''"+str(record_dict['DISTRIBUTIONCHANNEL_ID'])+ "'',''"+str(record_dict['DIVISION_ID'])+ "'',''"+str(record_dict['IS_SPARES'])+ "'',''"+str(record_dict['VALID_FROM'])+ "'',''"+str(record_dict['PRICEGROUP_ID'])+ "'',''"+str(record_dict['ACCASSIGNMENT_GROUP_ID'])+ "'',''"+str(record_dict['SALESUOM_ID'])+ "'',''"+ str(Modi_date)+ "'',''"+ str(primaryQuerysession.A)+ "'' ' ")
									

	
							elif str(tn).upper() == "MAMACT":
								if str(type(rebuilt_data[tn])) == "<type 'dict'>":
									Tbl_data = [rebuilt_data[tn]]
								else:
									Tbl_data = rebuilt_data[tn]
									
								for record_dict in Tbl_data:
								
									for col in ['SAP_PART_NUMBER','CATEGORY_ID']:
										if col not in record_dict:
											record_dict[col] = ''
																		
									primaryQueryItems = SqlHelper.GetFirst( ""+ str(Parameter.QUERY_CRITERIA_1)+ " MAMACT_INBOUND (SAP_PART_NUMBER,CATEGORY_ID,cpqtableentrydatemodified,SESSION_ID)  select  ''"+record_dict['SAP_PART_NUMBER']+ "'',''"+str(record_dict['CATEGORY_ID'])+ "'',''"+ str(Modi_date)+ "'',''"+ str(primaryQuerysession.A)+ "'' ' ")
									PRDHA = str(record_dict['CATEGORY_ID'])


					status_flag = 1					
					primaryItems = SqlHelper.GetFirst(  ""+ str(Parameter1.QUERY_CRITERIA_1)+ "  SYINPL set STATUS = ''PROCESSED'' from SYINPL  (NOLOCK) WHERE CpqTableEntryId  = ''"+str(json_data.CpqTableEntryId)+ "'' AND ISNULL(STATUS ,'''')= '''' ' "    )
				
				if len(Config_type) > 0:

					Native_tbl_info = """<?xml version="1.0" encoding="UTF-8"?>
										<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"> 
										 <soapenv:Body>
										<MATMAS05>
										    <IDOC BEGIN="1">
										        <EDI_DC40 SEGMENT="1">
										            <TABNAM>EDI_DC40</TABNAM>
										            <DOCNUM>0000000539385362</DOCNUM>
										        </EDI_DC40>
										        <E1MARAM SEGMENT="1">
										            <MATNR>{MATNR}</MATNR>
										            <MATKL>{MATKL}</MATKL>
										            <MEINS>{MEINS}</MEINS>
										            <PRDHA>{PRDHA}</PRDHA>
										            <E1MAKTM SEGMENT="1">
										                <MAKTX>{MAKTX}</MAKTX> 
										                <SPRAS_ISO>EN</SPRAS_ISO>
										            </E1MAKTM>
										            </E1MARAM>
										        </IDOC>
										    </MATMAS05>
										 </soapenv:Body></soapenv:Envelope>""".format(MATNR = MATNR,MATKL=MATKL,MEINS=MEINS,PRDHA=PRDHA,MAKTX =MAKTX.encode('utf-8').replace('&','&amp;'))
					catch_info = ''
					catch_info = Native_tbl_info
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
						
						
						LOGIN_CRE = SqlHelper.GetFirst("SELECT URL FROM SYCONF where EXTERNAL_TABLE_NAME ='MATMAS_NATIVE'")
						Async = webclient.UploadString(LOGIN_CRE.URL,Native_tbl_info)

		
		else:
			check_flag = 0
			
	if status_flag== 1 : 
		resp = ScriptExecutor.ExecuteGlobal("MAPOSTBULK")              
		ApiResponse = ApiResponseFactory.JsonResponse(resp)
	
except:
	Log.Info("MAPOSTMTRL ERROR---->:" + str(sys.exc_info()[1]))
	Log.Info("MAPOSTMTRL ERROR LINE NO---->:" + str(sys.exc_info()[-1].tb_lineno))
	Log.Info("MAPOSTMTRL catch_info ---->:" + str(catch_info))

	ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "400", "Message": str(sys.exc_info()[1])}]})
			
			

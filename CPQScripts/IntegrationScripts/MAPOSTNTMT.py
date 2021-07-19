# =========================================================================================================================================
#   __script_name : MAPOSTNTMT.PY
#   __script_description : THIS SCRIPT IS USED TO INSERT MATMAD DATA IN NATIVE TABLE 
#   __primary_author__ : BAJI
#   __create_date : 2021-04-23
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================

import clr
import sys
import datetime
import System.Net
from System.Text.Encoding import UTF8
from System import Convert
import System
from System.Net import HttpWebRequest, NetworkCredential
from System.Net import *
from System.Net import CookieContainer
from System.Net import Cookie
from System.Net import WebRequest
from System.Net import HttpWebResponse
from System import Uri

try :
	check_flag = 0	
	Parameter = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'SELECT' ")
	Parameter1 = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'UPD' ")	
	
	xml_start = '<?xml version="1.0" encoding="UTF-8"?><soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"><soapenv:Body ><MATMAS05><IDOC BEGIN="1">'
	
	xml_end = '</E1MARAM></IDOC></MATMAS05></soapenv:Body></soapenv:Envelope>'
	
	
	#Final_result = []
	
	while check_flag == 0:	
		
		
		Nativetablequery = SqlHelper.GetList("SELECT top 1 A.SAP_PART_NUMBER,A.MATERIALTYPE_ID,A.UNIT_OF_MEASURE,B.CATEGORY_ID FROM MAMTRL(NOLOCK) A JOIN CACTPR(NOLOCK) B ON A.SAP_PART_NUMBER = B.SAP_PART_NUMBER WHERE isnull(PRODUCT_HIRARCHY_ID,'') = '' ")		
		
		if len(Nativetablequery) > 0:
			for data in Nativetablequery:
				
				primaryQueryItems = SqlHelper.GetFirst("SELECT NEWID() AS A")
				Guid_info = ''
				Guid_info = '<EDI_DC40 SEGMENT="1"><TABNAM>EDI_DC40</TABNAM><DOCNUM>0000000539385362</DOCNUM></EDI_DC40><E1MARAM SEGMENT="1">'

			
				matirial_info = ''
				matirial_info = matirial_info+'<MATNR>'+str(data.SAP_PART_NUMBER)+'</MATNR><MATKL>'+str(data.MATERIALTYPE_ID)+'</MATKL><MEINS>'+str(data.UNIT_OF_MEASURE)+'</MEINS><PRDHA>'+str(data.CATEGORY_ID)+'</PRDHA>'			
				
				
				NativelangQuery = SqlHelper.GetList("SELECT ISNULL(LNGMAT_SHORTDESC,'') AS LNGMAT_SHORTDESC ,ISNULL(LANGUAGE_ID,'') AS LANGUAGE_ID FROM MALGMA(NOLOCK) WHERE SAP_PART_NUMBER = '"+str(data.SAP_PART_NUMBER)+"' ")
				Lang_info = ''
				for lang in NativelangQuery:	
					NC_Shot_desp = lang.LNGMAT_SHORTDESC
					Shot_desp = NC_Shot_desp.encode('utf-8').replace('&','&amp;')
					Lang_info = Lang_info+'<E1MAKTM SEGMENT="1"><MAKTX>'+Shot_desp+'</MAKTX><SPRAS_ISO>'+lang.LANGUAGE_ID+'</SPRAS_ISO></E1MAKTM>'
					
				Final_result = ''
				Final_result = xml_start+Guid_info+matirial_info+Lang_info+xml_end
				primaryQueryItems = SqlHelper.GetFirst(""+ str(Parameter1.QUERY_CRITERIA_1)+ "  A SET PRODUCT_HIRARCHY_ID = ''UPLOADED'' FROM MAMTRL(NOLOCK) A  WHERE SAP_PART_NUMBER = ''"+str(data.SAP_PART_NUMBER)+"'' '") 
				
				
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
					
					
					#LOGIN_CRE = SqlHelper.GetFirst("SELECT URL FROM SYCONF where ExternalTableName ='MATMAS_NATIVE'")
					Async = webclient.UploadString('https://e250360-iflmap.hcisbt.us3.hana.ondemand.com/cxf/ERP/CPQ/MATMAS_CFS.MATMAS05_TST', Final_result)
					
		else:		
			check_flag = 1
	
except:
	#Log.Info("03-05-2021 4545 Final_result --->"+Final_result)
	Log.Info("MAPOSTNTMT ERROR---->:" + str(sys.exc_info()[1]))
	Log.Info("MAPOSTNTMT ERROR LINE NO---->:" + str(sys.exc_info()[-1].tb_lineno))
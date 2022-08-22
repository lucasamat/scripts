# =========================================================================================================================================
#   __script_name : QTPOSTQERS.PY
#   __script_description : THIS SCRIPT IS USED TO SEND QUOTE INFROMATION FROM CPQ TO ECC
#   __primary_author__ : SURESH MUNIYANDI,BAJI
#   __create_date :
#   Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import sys
import datetime
import clr
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
from SYDATABASE import SQL

input_data = [str(param_result.Value) for param_result in Param.CPQ_Columns]	
input_data = [input_data]
Parameter = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'SELECT' ")

try:
	
	today = datetime.datetime.now()
	Modi_date = today.strftime("%m/%d/%Y %H:%M:%S %p")
	Log.Info("22222 start_time ---->"+str(Modi_date))
	

	data = ''
	QUOTE_ID = ''
	

	for crmifno in input_data:	
		
		QUOTE_ID = crmifno[0]
		REVISION_ID = crmifno[-1]
		
		CRMQT = SqlHelper.GetFirst("select convert(varchar(100),c4c_quote_id) as c4c_quote_id from SAQTMT(nolock) WHERE QUOTE_ID = '"+str(QUOTE_ID)+"' ")
		
		QTYPE = SqlHelper.GetFirst("select doctyp_id as quote_type from SAQTRV(nolock) WHERE QUOTE_ID = '"+str(QUOTE_ID)+"' and QTEREV_ID = '"+str(REVISION_ID)+"' ")
		
		SAOPPR = SqlHelper.GetFirst("select convert(varchar(100),OPPORTUNITY_ID) as OPPORTUNITY_ID,OPPORTUNITY_NAME from SAOPQT(nolock) WHERE QUOTE_ID = '"+str(QUOTE_ID)+"'  ")
		
		SAQICO = "SAQICO_BKP_"+str(CRMQT.c4c_quote_id)
		SAQIBP = "SAQIBP_BKP_"+str(CRMQT.c4c_quote_id)
		SAQIEN = "SAQIEN_BKP_"+str(CRMQT.c4c_quote_id)
		SAQSAP = "SAQSAP_BKP_"+str(CRMQT.c4c_quote_id)
		SAQTSE = "SAQTSE_BKP_"+str(CRMQT.c4c_quote_id)
		SAQITM = "SAQITM_BKP_"+str(CRMQT.c4c_quote_id)
		CRMTMP = "CRMTMP_BKP_"+str(CRMQT.c4c_quote_id)

		SAQICO_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQICO)+"'' ) BEGIN DROP TABLE "+str(SAQICO)+" END  ' ")
		SAQIBP_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQIBP)+"'' ) BEGIN DROP TABLE "+str(SAQIBP)+" END  ' ")
		SAQIEN_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQIEN)+"'' ) BEGIN DROP TABLE "+str(SAQIEN)+" END  ' ")
		SAQSAP_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQSAP)+"'' ) BEGIN DROP TABLE "+str(SAQSAP)+" END  ' ")
		SAQTSE_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQTSE)+"'' ) BEGIN DROP TABLE "+str(SAQTSE)+" END  ' ")
		SAQITM_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQITM)+"'' ) BEGIN DROP TABLE "+str(SAQITM)+" END  ' ")
		CRMTMP_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(CRMTMP)+"'' ) BEGIN DROP TABLE "+str(CRMTMP)+" END  ' ")

		SAQITM_DRP = SqlHelper.GetFirst("sp_executesql @T=N'select distinct SAQRIT.QUOTE_ID,SAQRIT.SERVICE_ID,SAQRIT.LINE,SAQRIT.QUANTITY,MAMTRL.UNIT_OF_MEASURE AS UOM_ID,SAQRIT.NET_PRICE AS EXTENDED_PRICE,'''' AS ITEM_TYPE,'''' AS PO_NUMBER,'''' AS PO_ITEM,'''' AS PO_NOTES,SAQRIT.PLANT_ID,SAQRIT.CONTRACT_VALID_FROM AS LINE_ITEM_FROM_DATE,SAQRIT.CONTRACT_VALID_TO AS LINE_ITEM_TO_DATE,'''' AS INTERNAL_NOTES,SAQRIT.STATUS,SAQRIT.SERVICE_RECORD_ID,SAQRIT.TAXCLASSIFICATION_ID AS SRVTAXCLA_ID,CONVERT(NVARCHAR(MAX),'''') AS BP_XML,CONVERT(NVARCHAR(MAX),'''') AS ET_XML,ISNULL(GL_ACCOUNT_NO,'''') AS GL_ACCOUNT_NO,ISNULL(REF_SALESORDER,'''') AS REF_SALESORDER_NO,QTEREV_ID INTO "+str(SAQITM)+" FROM SAQRIT (NOLOCK) JOIN MAMTRL (NOLOCK) ON SAQRIT.SERVICE_ID = MAMTRL.SAP_PART_NUMBER WHERE SAQRIT.QUOTE_ID = ''"+str(QUOTE_ID)+"'' AND SAQRIT.QTEREV_ID = ''"+str(REVISION_ID)+"''  ' ")

		SAQITM_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQIEN)+"'' ) BEGIN DROP TABLE "+str(SAQIEN)+" END CREATE TABLE "+str(SAQIEN)+" (QUOTE_ID VARCHAR(100),SERVICE_ID VARCHAR(100),LINE VARCHAR(100),ENTITLEMENT_NAME VARCHAR(100),ENTITLEMENT_VALUE_CODE VARCHAR(100))' ")

		SAQICO_BKP = SqlHelper.GetFirst("sp_executesql @T=N'select QUOTE_ID,SERVICE_ID,LINE,EQUIPMENT_ID,SERIAL_NUMBER,NULL AS EXTENDED_PRICE,NULL AS SRVTAXCLA_ID,CONVERT(VARCHAR(100),NULL) AS PAR_SERVICE_ID INTO "+str(SAQICO)+" from SAQRIO(NOLOCK) WHERE QUOTE_ID = ''"+str(QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(REVISION_ID)+"'' ' ")

		SAQIBP_BKP = SqlHelper.GetFirst("sp_executesql @T=N'select QUOTE_ID,LINE ,REPLACE(REPLACE(CONVERT(VARCHAR(11),DELIVERY_SCHED_DATE,121),''-'',''''),'' '','''') AS DELIVERY_DATE,CONVERT(VARCHAR,QUANTITY) AS QUANTITY,PART_NUMBER,CONVERT(VARCHAR,REPLACE(DELIVERY_SCHED_CAT,''DELIVERY '','''')) AS SCHEDULE_NO,QTEREV_ID,RELSCH_ECC_STATUS INTO "+str(SAQIBP)+" from SAQIPD(NOLOCK)  WHERE QUOTE_ID = ''"+str(QUOTE_ID)+"''  AND QTEREV_ID = ''"+str(REVISION_ID)+"'' ' ")

		SAQSAP_BKP = SqlHelper.GetFirst("sp_executesql @T=N'select QUOTE_ID,SERVICE_ID,LINE,PART_NUMBER,PART_DESCRIPTION,ISNULL(NEW_PART,''FALSE'') AS NEW_PART,QUANTITY INTO "+str(SAQSAP)+" from SAQRIP(NOLOCK) WHERE QUOTE_ID = ''"+str(QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(REVISION_ID)+"''  ' ")

		SAQTSE_BKP = SqlHelper.GetFirst("sp_executesql @T=N'select LINE,QUOTE_ID,MAMTRL.SAP_PART_NUMBER AS SERVICE_ID,CONVERT(VARCHAR(MAX),'''') AS ET_XML INTO "+str(SAQTSE)+" from SAQRIT(NOLOCK) JOIN MAMTRL (NOLOCK) ON SAQRIT.SERVICE_RECORD_ID = MAMTRL.MATERIAL_RECORD_ID WHERE QUOTE_ID = ''"+str(QUOTE_ID)+"'' AND SAQRIT.QTEREV_ID = ''"+str(REVISION_ID)+"'' ' ")
		
		
		# QUOTE_HEADER QUERY
		Quoteheaderquery = SqlHelper.GetFirst("select replace(replace(STUFF((SELECT  ' '+final_xml FROM (SELECT '<QUOTE_HEADER>'+'<QUOTE_ID>"+str(CRMQT.c4c_quote_id)+"</QUOTE_ID>'+'<QTEREV_ID>'+ISNULL(CONVERT(VARCHAR,SAQTRV.QTEREV_ID),'')+'</QTEREV_ID>'+'<CREATE>'+ISNULL(NULL,'')+'</CREATE>'+'<REVISION_DESCRIPTION>'+ISNULL(SAQTRV.REVISION_DESCRIPTION,'')+'</REVISION_DESCRIPTION>'+'<DOCTYP_ID>'+ISNULL(SAQTRV.DOCTYP_ID,'')+'</DOCTYP_ID>'+'<CONTRACT_VALID_FROM>'+REPLACE(ISNULL(convert(varchar(11),SAQTRV.CONTRACT_VALID_FROM,121),''),'-','')+'</CONTRACT_VALID_FROM>'+'<CONTRACT_VALID_TO>'+REPLACE(ISNULL(convert(varchar(11),SAQTRV.CONTRACT_VALID_TO,121),''),'-','')+'</CONTRACT_VALID_TO>'+'<DOC_CURRENCY>'+ISNULL(SAQTRV.DOC_CURRENCY,'')+'</DOC_CURRENCY>'+'<SALESORG_ID>'+ISNULL(SAQTRV.SALESORG_ID,'')+'</SALESORG_ID>'+'<DISTRIBUTIONCHANNEL_ID>'+ISNULL(SAQTRV.DISTRIBUTIONCHANNEL_ID,'')+'</DISTRIBUTIONCHANNEL_ID>'+'<DIVISION_ID>'+ISNULL(SAQTRV.DIVISION_ID,'')+'</DIVISION_ID>'+'<SALESOFFICE_ID>'+ISNULL(SAQTRV.SALESOFFICE_ID,'')+'</SALESOFFICE_ID>'+'<INCOTERM_ID>'+ISNULL(SAQTRV.INCOTERM_ID,'')+'</INCOTERM_ID>'+'<INCOTERM_NAME>'+ISNULL(SAQTRV.INCOTERM_NAME,'')+'</INCOTERM_NAME>'+'<PAYMENTTERM_ID>'+ISNULL(SAQTRV.PAYMENTTERM_ID,'')+'</PAYMENTTERM_ID>'+'<OPPORTUNITY_ID>"+str(SAOPPR.OPPORTUNITY_ID)+"</OPPORTUNITY_ID>'+'<OPPORTUNITY_NAME>"+str(SAOPPR.OPPORTUNITY_NAME)+"</OPPORTUNITY_NAME>'+'<PRICING_DATE>'+REPLACE(ISNULL(convert(varchar(11),CONVERT(DATE,SAQTRV.EXCHANGE_RATE_DATE),121),''),'-','')+'</PRICING_DATE>'+'<EXCHANGE_RATE>'+ISNULL(convert(varchar,SAQTRV.EXCHANGE_RATE),'1')+'</EXCHANGE_RATE><CONTRACT_ID>'+ISNULL(CRM_CONTRACT_ID,'')+'</CONTRACT_ID><RELEASE_CREATE>'+ISNULL('C','')+'</RELEASE_CREATE>' AS final_xml  FROM SAQTMT(NOLOCK)  JOIN SAQTRV (NOLOCK) ON SAQTMT.QUOTE_ID = SAQTRV.QUOTE_ID WHERE SAQTMT.QUOTE_ID = '"+str(QUOTE_ID)+"' AND SAQTRV.QTEREV_ID = '"+str(REVISION_ID)+"' )A FOR XML PATH ('')  ), 1, 1, ''),'&lt;','<'),'&gt;','>')AS RESULT")
		
		if str(Quoteheaderquery.RESULT) != "" :
			Quoteheaderquery = str(Quoteheaderquery.RESULT)
		else:
			Quoteheaderquery = "<QUOTE_HEADER>"
		
		# QUOTE_INVOLVED_PARTY QUERY
		QuoteInvolvedPartiesquery = SqlHelper.GetFirst("select NULL AS RESULT")
		
		QuoteInvolvedPartiesquery1 = SqlHelper.GetFirst("select replace(replace(STUFF((SELECT  ' '+final_xml FROM (SELECT DISTINCT  '<SHIP_TO>'+ISNULL(PARTY_ID,'')+'</SHIP_TO>' AS final_xml  FROM SAQTIP(NOLOCK) WHERE QUOTE_ID = '"+str(QUOTE_ID)+"' AND QTEREV_ID = '"+str(REVISION_ID)+"' AND ISNULL([PRIMARY],'FALSE')='FALSE'  )A FOR XML PATH ('')  ), 1, 1, ''),'&lt;','<'),'&gt;','>')AS RESULT")
		
		if str(QuoteInvolvedPartiesquery.RESULT) != "" :
			QuoteInvolvedPartiesquery = str(QuoteInvolvedPartiesquery.RESULT)
			
			if str(QuoteInvolvedPartiesquery1.RESULT) != "" :
				QuoteInvolvedPartiesquery = QuoteInvolvedPartiesquery+str(QuoteInvolvedPartiesquery1.RESULT)
			
			QuoteInvolvedPartiesfabquery = SqlHelper.GetFirst("select replace(replace(STUFF((SELECT  ' '+final_xml FROM (SELECT  DISTINCT '<FAB>'+CASE WHEN ISNULl(CRM_FABLOCATION_ID,'')<>'' THEN CRM_FABLOCATION_ID ELSE ISNULL(SAQFBL.FABLOCATION_ID,'') END+'</FAB>' AS final_xml  FROM SAQICO SAQFBL(NOLOCK) JOIN MAFBLC (NOLOCK) ON SAQFBL.FABLOCATION_ID = MAFBLC.FAB_LOCATION_ID WHERE QUOTE_ID  = '"+str(QUOTE_ID)+"' AND QTEREV_ID = '"+str(REVISION_ID)+"')SUB_SAQFBL FOR XML PATH ('')  ), 1, 1, ''),'&lt;','<'),'&gt;','>')AS RESULT")
			
			QuoteInvolvedPartiescontactquery = SqlHelper.GetFirst("select replace(replace(STUFF((SELECT  ' '+final_xml FROM (SELECT  DISTINCT '<EMAIL'+CONVERT(VARCHAR,ROW_NUMBER()OVER(ORDER BY CPQTABLEENTRYID))+'>'+ISNULL(SAQICT.EMAIL,'') +'</EMAIL'+CONVERT(VARCHAR,ROW_NUMBER()OVER(ORDER BY CPQTABLEENTRYID))+'>' AS final_xml  FROM SAQICT (NOLOCK) WHERE QUOTE_ID  = '"+str(QUOTE_ID)+"' AND QTEREV_ID = '"+str(REVISION_ID)+"' AND ISNULL(SHIP_NOTIFY_EMAIL,'FALSE')='TRUE' UNION SELECT  DISTINCT '<EMAIL4>'+ISNULL(SAQICT.EMAIL,'') +'</EMAIL4>' FROM SAQICT (NOLOCK) WHERE QUOTE_ID  = '"+str(QUOTE_ID)+"' AND QTEREV_ID = '"+str(REVISION_ID)+"' AND ISNULL(RETURN_NOTIFY_EMAIL,'FALSE')='TRUE' )SAQICT FOR XML PATH ('')  ), 1, 1, ''),'&lt;','<'),'&gt;','>')AS RESULT")
			
			if str(QuoteInvolvedPartiesfabquery.RESULT) != "" :
			
				QuoteInvolvedPartiesquery = QuoteInvolvedPartiesquery+str(QuoteInvolvedPartiesfabquery.RESULT)
			else:
				QuoteInvolvedPartiesquery = QuoteInvolvedPartiesquery+'<FAB></FAB>'
			
			if str(QuoteInvolvedPartiescontactquery.RESULT) != "" :
			
				QuoteInvolvedPartiesquery = QuoteInvolvedPartiesquery+str(QuoteInvolvedPartiescontactquery.RESULT)+'</QUOTE_INVOLVED_PARTY>'
			else:
				QuoteInvolvedPartiesquery = QuoteInvolvedPartiesquery+'<EMAIL1></EMAIL1><EMAIL2></EMAIL2><EMAIL3></EMAIL3><EMAIL4></EMAIL4></QUOTE_INVOLVED_PARTY>'
			
		else:
			QuoteInvolvedPartiesquery = "<QUOTE_INVOLVED_PARTY></QUOTE_INVOLVED_PARTY>"
		
		start1 = 1
		end1 = 1

		Check_flag1 = 1
		while Check_flag1 == 1:
			
			data = ''
			
			table1 = SqlHelper.GetFirst(
				"SELECT DISTINCT SCHEDULE_NO FROM (select distinct SCHEDULE_NO, ROW_NUMBER()OVER(ORDER BY SCHEDULE_NO) AS SNO FROM(SELECT DISTINCT SCHEDULE_NO FROM "+str(SAQIBP)+"  (NOLOCK) where quote_id='"+str(QUOTE_ID)+"' and isnull(RELSCH_ECC_STATUS,'false')='false' ) A )A WHERE SNO>= "+str(start1)+" AND SNO<="+str(end1)+""
			)
			
			start1 = start1 
			end1 = end1 

			if str(table1) != "None":
		
				if str(QTYPE.quote_type) == "ZWK1":
					
					Quoteitemquery = SqlHelper.GetFirst("SELECT REPLACE((select replace(replace(STUFF((SELECT  ' '+final_xml FROM ( SELECT '<QUOTE_ITEM>'+'<LINE>'+ISNULL(convert(varchar(100),SAQITM.LINE),'')+'</LINE>'+'<SERVICE_ID>'+SAQITM.SERVICE_ID+'</SERVICE_ID>'+'<NET_VALUE>'+ISNULL(convert(varchar,SAQITM.EXTENDED_PRICE),'')+'</NET_VALUE>'+'<PLANT_ID>'+ISNULL(convert(varchar,SAQITM.PLANT_ID),'')+'</PLANT_ID>'+'<CONTRACT_VALID_FROM>'+REPLACE(ISNULL(convert(varchar(11),SAQITM.LINE_ITEM_FROM_DATE,121),''),'-','')+'</CONTRACT_VALID_FROM>'+'<CONTRACT_VALID_TO>'+REPLACE(ISNULL(convert(varchar(11),SAQITM.LINE_ITEM_TO_DATE,121),''),'-','')+'</CONTRACT_VALID_TO>'+ ISNULL(ET_XML,'<QUOTE_ITEM_ENTITLEMENT></QUOTE_ITEM_ENTITLEMENT>')+ISNULL(NULL,'<QUOTE_ITEM_PARTS></QUOTE_ITEM_PARTS>')+ISNULL(REPLACE(REPLACE(STUFF((SELECT ' '+ JSON FROM (SELECT '<QUOTE_PARTS_RELEASE_SCHEDULES_HEAD>'+'<LINE>'+ISNULL(convert(varchar(100),SUB_SAQITM.LINE),'')+'</LINE>'+'<SCHEDULE_NO>'+ISNULL(SCHEDULE_NO,'')+'</SCHEDULE_NO>'+'<DELIVERY_DATE>'+ISNULL(DELIVERY_DATE,'')+'</DELIVERY_DATE>'+'</QUOTE_PARTS_RELEASE_SCHEDULES_HEAD>' AS JSON FROM (SELECT DISTINCT LINE,SCHEDULE_NO,DELIVERY_DATE FROM "+str(SAQIBP)+"(NOLOCK)SAQIBP WHERE SAQIBP.QUOTE_ID = '"+str(QUOTE_ID)+"' AND SAQIBP.QTEREV_ID = '"+str(REVISION_ID)+"' AND SAQITM.QUOTE_ID  = SAQIBP.QUOTE_ID AND SAQITM.QTEREV_ID  = SAQIBP.QTEREV_ID AND SAQITM.LINE = SAQIBP.LINE AND SCHEDULE_NO = '"+str(table1.SCHEDULE_NO)+"'  )SUB_SAQITM )A FOR XML PATH ('')  ), 1, 1,'' ),'&lt;','<'),'&gt;','>'),'<QUOTE_PARTS_RELEASE_SCHEDULES_HEAD></QUOTE_PARTS_RELEASE_SCHEDULES_HEAD>')+ISNULL(REPLACE(REPLACE(STUFF((SELECT ' '+ JSON FROM (SELECT '<QUOTE_PARTS_RELEASE_SCHEDULES_ITEM>'+'<LINE>'+ISNULL(convert(varchar(100),SUB_SAQITM.LINE),'')+'</LINE>'+'<SCHEDULE_NO>'+ISNULL(SCHEDULE_NO,'')+'</SCHEDULE_NO>'+'<QUANTITY>'+ISNULL(QUANTITY,'')+'</QUANTITY><PART_NUMBER>'+ISNULL(PART_NUMBER,'')+'</PART_NUMBER>'+'</QUOTE_PARTS_RELEASE_SCHEDULES_ITEM>' AS JSON FROM (SELECT LINE,SCHEDULE_NO,QUANTITY,PART_NUMBER FROM "+str(SAQIBP)+"(NOLOCK)SAQIBP WHERE SAQIBP.QUOTE_ID = '"+str(QUOTE_ID)+"' AND SAQIBP.QTEREV_ID = '"+str(REVISION_ID)+"' AND SAQITM.QUOTE_ID  = SAQIBP.QUOTE_ID AND SAQITM.QTEREV_ID  = SAQIBP.QTEREV_ID AND SAQITM.LINE = SAQIBP.LINE AND SCHEDULE_NO = '"+str(table1.SCHEDULE_NO)+"'  )SUB_SAQITM )A FOR XML PATH ('')  ), 1, 1,'' ),'&lt;','<'),'&gt;','>'),'<QUOTE_PARTS_RELEASE_SCHEDULES_ITEM></QUOTE_PARTS_RELEASE_SCHEDULES_ITEM>')+'</QUOTE_ITEM>' AS final_xml  FROM "+str(SAQITM)+" SAQITM(NOLOCK) WHERE SAQITM.QUOTE_ID = '"+str(QUOTE_ID)+"' )A FOR XML PATH ('')  ), 1, 1, ''),'&lt;','<'),'&gt;','>')AS RESULT),'','' ) AS A ")

				if str(Quoteitemquery.A) == '':
					Quoteiteminfo = '<QUOTE_ITEM><QUOTE_ITEM_PARTS></QUOTE_ITEM_PARTS><QUOTE_ITEM_ENTITLEMENT></QUOTE_ITEM_ENTITLEMENT></QUOTE_ITEM>'
				else:
					Quoteiteminfo = str(Quoteitemquery.A)
			
				str_xml = str(Quoteiteminfo)
				
				data = data+str_xml
				
				data = str(Quoteheaderquery)+str(data)+str(QuoteInvolvedPartiesquery)+'</QUOTE_HEADER>'	
				
				Final_xml = "<QUOTE>"+str(data)+"</QUOTE>"
				
				primaryQueryItems = SqlHelper.GetFirst( ""+ str(Parameter.QUERY_CRITERIA_1)+ " SYINPL (INTEGRATION_PAYLOAD,INTEGRATION_KEY,CpqTableEntryDateModified,INTEGRATION_NAME)  select ''"+str(Final_xml)+ "'',''"+ str(QUOTE_ID)+ "'',getdate(),''CPQ to ECC Quote Replication'' ' ")
				
				#OAUTH AUTHENTICATION
	
				LOGIN_CRE = SqlHelper.GetFirst("SELECT URL FROM SYCONF (nolock) where EXTERNAL_TABLE_NAME ='CPQ_TO_ECC_QUOTE'")
				Oauth_info = SqlHelper.GetFirst("SELECT  DOMAIN,URL FROM SYCONF where EXTERNAL_TABLE_NAME ='OAUTH'")
					
				requestdata =Oauth_info.DOMAIN
				webclient = System.Net.WebClient()
				webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/x-www-form-urlencoded"
				response = webclient.UploadString(Oauth_info.URL,str(requestdata))

				response = eval(response)
				access_token = response['access_token']
				
				authorization = "Bearer " + access_token
				webclient = System.Net.WebClient()
				webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/xml"
				webclient.Headers[System.Net.HttpRequestHeader.Authorization] = authorization;	

				crm_response = webclient.UploadString(str(LOGIN_CRE.URL),Final_xml)	
				
				if 'tid' in crm_response:	
					SAQIBP_UPD = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE "+str(SAQIBP)+" SET RELSCH_ECC_STATUS = ''TRUE'' WHERE QUOTE_ID = ''"+str(QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(REVISION_ID)+"'' AND SCHEDULE_NO = ''"+str(table1.SCHEDULE_NO)+"''  ' ")
					
					SAQIBP_UPD = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE SAQIPD SET RELSCH_ECC_STATUS = ''TRUE'' WHERE QUOTE_ID = ''"+str(QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(REVISION_ID)+"'' AND CONVERT(VARCHAR,REPLACE(DELIVERY_SCHED_CAT,''DELIVERY '',''''))  = ''"+str(table1.SCHEDULE_NO)+"''  ' ")
				
			else:
				Check_flag1=0

	SAQICO_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQICO)+"'' ) BEGIN DROP TABLE "+str(SAQICO)+" END  ' ")
	SAQIBP_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQIBP)+"'' ) BEGIN DROP TABLE "+str(SAQIBP)+" END  ' ")
	SAQIEN_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQIEN)+"'' ) BEGIN DROP TABLE "+str(SAQIEN)+" END  ' ")
	SAQSAP_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQSAP)+"'' ) BEGIN DROP TABLE "+str(SAQSAP)+" END  ' ")
	SAQTSE_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQTSE)+"'' ) BEGIN DROP TABLE "+str(SAQTSE)+" END  ' ")
	SAQITM_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQITM)+"'' ) BEGIN DROP TABLE "+str(SAQITM)+" END  ' ")
	CRMTMP_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(CRMTMP)+"'' ) BEGIN DROP TABLE "+str(CRMTMP)+" END  ' ")
	
	if 'tid' in crm_response:		
		ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "200", "Message": "Data Successfully Sent to ECC."}]})
	else:
		SAQICO_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQICO)+"'' ) BEGIN DROP TABLE "+str(SAQICO)+" END  ' ")
		SAQIBP_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQIBP)+"'' ) BEGIN DROP TABLE "+str(SAQIBP)+" END  ' ")
		SAQIEN_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQIEN)+"'' ) BEGIN DROP TABLE "+str(SAQIEN)+" END  ' ")
		SAQSAP_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQSAP)+"'' ) BEGIN DROP TABLE "+str(SAQSAP)+" END  ' ")
		SAQTSE_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQTSE)+"'' ) BEGIN DROP TABLE "+str(SAQTSE)+" END  ' ")
		SAQITM_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQITM)+"'' ) BEGIN DROP TABLE "+str(SAQITM)+" END  ' ")
		CRMTMP_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(CRMTMP)+"'' ) BEGIN DROP TABLE "+str(CRMTMP)+" END  ' ")
		
		ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "400", "Message": str(crm_response)}]})
	
	
except:
	for crmifno in input_data:	
		
		QUOTE_ID = crmifno[0]
		REVISION_ID = crmifno[-1]

		CRMQT = SqlHelper.GetFirst("select convert(varchar(100),c4c_quote_id) as c4c_quote_id from SAQTMT(nolock) WHERE QUOTE_ID = '"+str(QUOTE_ID)+"' ")

		QTYPE = SqlHelper.GetFirst("select left(quote_type,4) as quote_type from SAQTMT(nolock) WHERE QUOTE_ID = '"+str(QUOTE_ID)+"' ")

		SAOPPR = SqlHelper.GetFirst("select convert(varchar(100),OPPORTUNITY_ID) as OPPORTUNITY_ID,OPPORTUNITY_NAME from SAOPQT(nolock) WHERE QUOTE_ID = '"+str(QUOTE_ID)+"' ")

		SAQICO = "SAQICO_BKP_"+str(CRMQT.c4c_quote_id)
		SAQIBP = "SAQIBP_BKP_"+str(CRMQT.c4c_quote_id)
		SAQIEN = "SAQIEN_BKP_"+str(CRMQT.c4c_quote_id)
		SAQSAP = "SAQSAP_BKP_"+str(CRMQT.c4c_quote_id)
		SAQTSE = "SAQTSE_BKP_"+str(CRMQT.c4c_quote_id)
		SAQITM = "SAQITM_BKP_"+str(CRMQT.c4c_quote_id)
		CRMTMP = "CRMTMP_BKP_"+str(CRMQT.c4c_quote_id)
		
		SAQICO_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQICO)+"'' ) BEGIN DROP TABLE "+str(SAQICO)+" END  ' ")
		SAQIBP_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQIBP)+"'' ) BEGIN DROP TABLE "+str(SAQIBP)+" END  ' ")
		SAQIEN_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQIEN)+"'' ) BEGIN DROP TABLE "+str(SAQIEN)+" END  ' ")
		SAQSAP_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQSAP)+"'' ) BEGIN DROP TABLE "+str(SAQSAP)+" END  ' ")
		SAQTSE_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQTSE)+"'' ) BEGIN DROP TABLE "+str(SAQTSE)+" END  ' ")
		SAQITM_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQITM)+"'' ) BEGIN DROP TABLE "+str(SAQITM)+" END  ' ")
		CRMTMP_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(CRMTMP)+"'' ) BEGIN DROP TABLE "+str(CRMTMP)+" END  ' ")
		

	Log.Info("QTPOSTQERS ERROR---->:" + str(sys.exc_info()[1]))
	Log.Info("QTPOSTQERS ERROR LINE NO---->:" + str(sys.exc_info()[-1].tb_lineno))
	ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "400", "Message": str(sys.exc_info()[1])}]})
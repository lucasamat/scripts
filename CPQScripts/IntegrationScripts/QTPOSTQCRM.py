# =========================================================================================================================================
#   __script_name : QTPOSTQCRM.PY
#   __script_description : THIS SCRIPT IS USED TO SEND QUOTE INFROMATION FROM CPQ TO CRM
#   __primary_author__ : SURESH MUNIYANDI,BAJI
#   __create_date :
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
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

try:
	
	today = datetime.datetime.now()
	Modi_date = today.strftime("%m/%d/%Y %H:%M:%S %p")
	Log.Info("22222 start_time ---->"+str(Modi_date))
	

	data = ''
	Qt_id = ''
	

	for QUOTE_ID in input_data:	
		
		Qt_id = QUOTE_ID
		
		CRMQT = SqlHelper.GetFirst("select convert(varchar(100),c4c_quote_id) as c4c_quote_id from SAQTMT(nolock) WHERE QUOTE_ID = '"+str(QUOTE_ID)+"' ")
		
		QTYPE = SqlHelper.GetFirst("select left(quote_type,4) as quote_type from SAQTMT(nolock) WHERE QUOTE_ID = '"+str(QUOTE_ID)+"' ")
		
		SAOPPR = SqlHelper.GetFirst("select convert(varchar(100),OPPORTUNITY_ID) as OPPORTUNITY_ID,OPPORTUNITY_NAME from SAOPQT(nolock) WHERE QUOTE_ID = '"+str(QUOTE_ID)+"' ")
		
		SAQICO = "SAQICO_BKP_"+str(CRMQT.c4c_quote_id)
		SAQIBP = "SAQIBP_BKP_"+str(CRMQT.c4c_quote_id)
		SAQIEN = "SAQIEN_BKP_"+str(CRMQT.c4c_quote_id)
		SAQSAP = "SAQSAP_BKP_"+str(CRMQT.c4c_quote_id)
		SAQTSE = "SAQTSE_BKP_"+str(CRMQT.c4c_quote_id)
		SAQITM = "SAQITM_BKP_"+str(CRMQT.c4c_quote_id)

		SAQICO_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQICO)+"'' ) BEGIN DROP TABLE "+str(SAQICO)+" END  ' ")
		SAQIBP_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQIBP)+"'' ) BEGIN DROP TABLE "+str(SAQIBP)+" END  ' ")
		SAQIEN_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQIEN)+"'' ) BEGIN DROP TABLE "+str(SAQIEN)+" END  ' ")
		SAQSAP_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQSAP)+"'' ) BEGIN DROP TABLE "+str(SAQSAP)+" END  ' ")
		SAQTSE_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQTSE)+"'' ) BEGIN DROP TABLE "+str(SAQTSE)+" END  ' ")
		SAQITM_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQITM)+"'' ) BEGIN DROP TABLE "+str(SAQITM)+" END  ' ")

		SAQITM_DRP = SqlHelper.GetFirst("sp_executesql @T=N'select distinct SAQITM.QUOTE_ID,SAQICO.SERVICE_ID,SAQICO.EQUIPMENT_LINE_ID,SAQITM.QUANTITY,SAQITM.UOM_ID,SAQITM.EXTENDED_PRICE,SAQITM.ITEM_TYPE,SAQITM.PO_NUMBER,SAQITM.PO_ITEM,SAQITM.PO_NOTES,SAQITM.PLANT_ID,SAQITM.LINE_ITEM_FROM_DATE,SAQITM.LINE_ITEM_TO_DATE,SAQITM.INTERNAL_NOTES,SAQITM.ITEM_STATUS,SAQITM.SERVICE_RECORD_ID,SAQITM.SRVTAXCLA_ID INTO "+str(SAQITM)+" from SAQICO(NOLOCK) JOIN SAQITM (NOLOCK) ON SAQICO.QUOTE_ID = SAQITM.QUOTE_ID AND SAQICO.LINE_ITEM_ID = SAQITM.LINE_ITEM_ID WHERE SAQITM.QUOTE_ID = ''"+str(QUOTE_ID)+"''  ' ")

		SAQICO_BKP = SqlHelper.GetFirst("sp_executesql @T=N'select QUOTE_ID,MAMTRL.SAP_PART_NUMBER AS SERVICE_ID,LINE_ITEM_ID AS ITEM_LINE_ID,EQUIPMENT_LINE_ID,CONVERT(NVARCHAR(MAX),'''') AS BP_XML,CONVERT(NVARCHAR(MAX),'''') AS ET_XML,EQUIPMENT_ID,SERIAL_NO,EXTENDED_PRICE,SRVTAXCLA_ID,CONVERT(VARCHAR(100),NULL) AS PAR_SERVICE_ID INTO "+str(SAQICO)+" from SAQICO(NOLOCK) JOIN MAMTRL (NOLOCK) ON SAQICO.SERVICE_RECORD_ID = MAMTRL.MATERIAL_RECORD_ID WHERE QUOTE_ID = ''"+str(QUOTE_ID)+"''  ' ")

		SAQICO_BKP = SqlHelper.GetFirst("sp_executesql @T=N'INSERT "+str(SAQICO)+" (QUOTE_ID,SERVICE_ID,ITEM_LINE_ID,EQUIPMENT_LINE_ID,BP_XML,ET_XML,EQUIPMENT_ID,SERIAL_NO,EXTENDED_PRICE,SRVTAXCLA_ID,PAR_SERVICE_ID) SELECT DISTINCT SAQITM.QUOTE_ID,MAMTRL.SAP_PART_NUMBER AS SERVICE_ID,SAQITM.LINE_ITEM_ID AS ITEM_LINE_ID,0 AS EQUIPMENT_LINE_ID,CONVERT(NVARCHAR(MAX),'''') AS BP_XML,CONVERT(NVARCHAR(MAX),'''') AS ET_XML,NULL AS EQUIPMENT_ID,NULL AS SERIAL_NO,NULL AS EXTENDED_PRICE,SAQITM.SRVTAXCLA_ID,MAMTRL.SAP_PART_NUMBER AS PAR_SERVICE_ID FROM SAQITM(NOLOCK) JOIN MAMTRL (NOLOCK) ON SAQITM.SERVICE_RECORD_ID = MAMTRL.MATERIAL_RECORD_ID JOIN SAQITM SAQITM1(NOLOCK) ON SAQITM.PARQTEITM_LINE = SAQITM1.LINE_ITEM_ID AND SAQITM.QUOTE_ID = SAQITM1.QUOTE_ID JOIN MAMTRL MAMTRL1(NOLOCK) ON SAQITM.SERVICE_RECORD_ID = MAMTRL1.MATERIAL_RECORD_ID WHERE SAQITM.QUOTE_ID = ''"+str(QUOTE_ID)+"'' AND SAQITM.LINE_ITEM_ID NOT IN (SELECT DISTINCT LINE_ITEM_ID FROM SAQICO(NOLOCK) WHERE QUOTE_ID = ''"+str(QUOTE_ID)+"'' ) ' ")


		SAQICO_BKP = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET EQUIPMENT_LINE_ID = B.EQUIPMENT_LINE_ID FROM "+str(SAQICO)+" A JOIN (SELECT QUOTE_ID,SERVICE_ID,EQUIPMENT_LINE_ID AS ELINE,ITEM_LINE_ID,(SEQ * 10) + (SELECT MAX(EQUIPMENT_LINE_ID) FROM "+str(SAQICO)+") AS EQUIPMENT_LINE_ID  FROM (SELECT DISTINCT QUOTE_ID,SERVICE_ID,EQUIPMENT_LINE_ID,ITEM_LINE_ID,ROW_NUMBER() OVER(ORDER BY QUOTE_ID) as SEQ FROM "+str(SAQICO)+" WHERE ISNULL(EQUIPMENT_LINE_ID,0)=0)A ) B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.ITEM_LINE_ID = B.ITEM_LINE_ID AND A.EQUIPMENT_LINE_ID = B.ELINE' ")

		SAQIBP_BKP = SqlHelper.GetFirst("sp_executesql @T=N'select QUOTE_ID,MAMTRL.SAP_PART_NUMBER AS SERVICE_ID,LINE_ITEM_ID AS ITEM_LINE_ID,EQUIPMENT_LINE_ID,REPLACE(CONVERT(VARCHAR(11),BILLING_DATE,121),''-'','''') AS BILLING_DATE,BILLING_AMOUNT,EQUIPMENT_ID INTO "+str(SAQIBP)+" from SAQIBP(NOLOCK)  JOIN MAMTRL (NOLOCK) ON SAQIBP.SERVICE_RECORD_ID = MAMTRL.MATERIAL_RECORD_ID WHERE QUOTE_ID = ''"+str(QUOTE_ID)+"''  ' ")

		SAQSAP_BKP = SqlHelper.GetFirst("sp_executesql @T=N'select QUOTE_ID,SERVICE_ID,EQUIPMENT_ID,KIT_NUMBER,KIT_NAME INTO "+str(SAQSAP)+" from SAQSAP(NOLOCK) WHERE QUOTE_ID = ''"+str(QUOTE_ID)+"''  ' ")

		SAQTSE_BKP = SqlHelper.GetFirst("sp_executesql @T=N'select LINE_ITEM_ID,QUOTE_ID,MAMTRL.SAP_PART_NUMBER AS SERVICE_ID,CONVERT(VARCHAR(MAX),'''') AS ET_XML INTO "+str(SAQTSE)+" from SAQITM(NOLOCK) JOIN MAMTRL (NOLOCK) ON SAQITM.SERVICE_RECORD_ID = MAMTRL.MATERIAL_RECORD_ID WHERE QUOTE_ID = ''"+str(QUOTE_ID)+"''  ' ")

		Quoteitemquer = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE B SET BP_XML= final_xml FROM (SELECT A.EQUIPMENT_LINE_ID, ISNULL(REPLACE(REPLACE(STUFF((SELECT '' ''+ JSON FROM (SELECT ''<QUOTE_ITEM_BILLING_PLAN>''+''<ITEM_LINE_ID>''+ISNULL(CONVERT(VARCHAR(100),A.EQUIPMENT_LINE_ID),'''')+''</ITEM_LINE_ID>''+''<SERVICE_ID>''+ISNULL(A.SERVICE_ID,'''')+''</SERVICE_ID>''+''<BILLING_START_DATE>''+ISNULL(A.BILLING_DATE,'''')+''</BILLING_START_DATE>''+''<BILLING_AMOUNT>''+ISNULL(CONVERT(VARCHAR(100),A.BILLING_AMOUNT),'''')+''</BILLING_AMOUNT>''+''</QUOTE_ITEM_BILLING_PLAN>'' AS JSON FROM ( 	SELECT B.EQUIPMENT_LINE_ID,B.SERVICE_ID,REPLACE(CONVERT(VARCHAR(11),BILLING_DATE,121),''-'','''') AS BILLING_DATE, SUM(BILLING_AMOUNT) AS BILLING_AMOUNT FROM "+str(SAQIBP)+" B(NOLOCK) WHERE A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.EQUIPMENT_LINE_ID = B.EQUIPMENT_LINE_ID AND B.QUOTE_ID = ''"+str(QUOTE_ID)+"'' GROUP BY B.EQUIPMENT_LINE_ID,B.SERVICE_ID,BILLING_DATE )A )A FOR XML PATH ('''')  ), 1, 1,'''' ),''&lt;'',''<''),''&gt;'',''>''),''<QUOTE_ITEM_BILLING_PLAN></QUOTE_ITEM_BILLING_PLAN>'') AS final_xml,A.EQUIPMENT_ID  FROM "+str(SAQICO)+" (NOLOCK) A WHERE A.QUOTE_ID = ''"+str(QUOTE_ID)+"'' )A JOIN "+str(SAQICO)+" B(NOLOCK) ON A.EQUIPMENT_LINE_ID = B.EQUIPMENT_LINE_ID '")

		Quoteitemquer = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE B SET ET_XML= FINAL FROM (select  replace(REPLACE(entitlement_xml,''<QUOTE_ITEM_ENTITLEMENT>'',sml),''ENTITLEMENT_VALUE_CODE'',''ENTITLEMENT_VALUE'') AS FINAL,EQUIPMENT_LINE_ID from(select distinct ''<QUOTE_ITEM_ENTITLEMENT><ITEM_LINE_ID>''+convert(varchar(100),EQUIPMENT_LINE_ID)+''</ITEM_LINE_ID><SERVICE_ID>''+service_id+''</SERVICE_ID>'' AS sml,replace(entitlement_xml,''&'','';#38'')  as entitlement_xml,EQUIPMENT_LINE_ID from SAQIEN(nolock) where quote_id=''"+str(QUOTE_ID)+"'' )A)A JOIN "+str(SAQICO)+" B(NOLOCK) ON A.EQUIPMENT_LINE_ID = B.EQUIPMENT_LINE_ID '")

		Quoteitemquer = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE B SET ET_XML= FINAL FROM (select  replace(REPLACE(entitlement_xml,''<QUOTE_ITEM_ENTITLEMENT>'',sml),''ENTITLEMENT_VALUE_CODE'',''ENTITLEMENT_VALUE'') AS FINAL,A.PAR_SERVICE_ID,A.SERVICE_ID,A.QUOTE_ID from(select ''<QUOTE_ITEM_ENTITLEMENT><ITEM_LINE_ID>''+convert(varchar(100),B.EQUIPMENT_LINE_ID)+''</ITEM_LINE_ID><SERVICE_ID>''+A.SERVICE_ID+''</SERVICE_ID>'' AS sml,replace(entitlement_xml,''&'','';#38'')  as entitlement_xml,A.PAR_SERVICE_ID,A.SERVICE_ID,A.QUOTE_ID from SAQTSE(nolock) A JOIN "+str(SAQICO)+" B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.PAR_SERVICE_ID = B.PAR_SERVICE_ID where A.quote_id=''"+str(QUOTE_ID)+"'' AND ISNULL(A.PAR_SERVICE_ID,'''')<>'''' AND ISNULL(B.EQUIPMENT_ID,'''')='''')A)A JOIN "+str(SAQICO)+" B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.PAR_SERVICE_ID = B.PAR_SERVICE_ID AND ISNULL(B.PAR_SERVICE_ID,'''')<>'''' AND ISNULL(B.EQUIPMENT_ID,'''')=''''  '")
		
		if str(QTYPE.quote_type) == "ZWK1":

			Quoteitemquer = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE B SET ET_XML= FINAL FROM (select  replace(REPLACE(entitlement_xml,''<QUOTE_ITEM_ENTITLEMENT>'',sml),''ENTITLEMENT_VALUE_CODE'',''ENTITLEMENT_VALUE'') AS FINAL,LINE_ITEM_ID from(select ''<QUOTE_ITEM_ENTITLEMENT><ITEM_LINE_ID>''+convert(varchar(100),''10'')+''</ITEM_LINE_ID><SERVICE_ID>''+service_id+''</SERVICE_ID>'' AS sml,replace(entitlement_xml,''&'','';#38'')  as entitlement_xml,''10'' AS LINE_ITEM_ID from SAQTSE(nolock) where quote_id=''"+str(QUOTE_ID)+"'' )A)A JOIN "+str(SAQTSE)+" B(NOLOCK) ON A.LINE_ITEM_ID = B.LINE_ITEM_ID '")

		# QUOTE_HEADER QUERY
		Quoteheaderquery = SqlHelper.GetFirst("select replace(replace(STUFF((SELECT  ' '+final_xml FROM (SELECT '<QUOTE_HEADER>'+'<QUOTE_ID>"+str(CRMQT.c4c_quote_id)+"</QUOTE_ID>'+'<QUOTE_NAME>'+ISNULL(SAQTMT.QUOTE_NAME,'')+'</QUOTE_NAME>'+'<QUOTE_TYPE>'+ISNULL(LEFT(SAQTMT.QUOTE_TYPE,4),'')+'</QUOTE_TYPE>'+'<SORG_CURRENCY>'+ISNULL(SAQTSO.SORG_CURRENCY,'')+'</SORG_CURRENCY>'+'<QUOTE_CURRENCY>'+ISNULL(SAQTMT.QUOTE_CURRENCY,'')+'</QUOTE_CURRENCY>'+'<SALESORG_ID>'+ISNULL(SAQTSO.SALESORG_ID,'')+'</SALESORG_ID>'+'<DISTRIBUTIONCHANNEL_ID>'+ISNULL(SAQTSO.DISTRIBUTIONCHANNEL_ID,'')+'</DISTRIBUTIONCHANNEL_ID>'+'<DIVISION_ID>'+ISNULL(SAQTSO.DIVISION_ID,'')+'</DIVISION_ID>'+'<SALESOFFICE_ID>'+ISNULL(SAQTSO.SALESOFFICE_ID,'')+'</SALESOFFICE_ID>'+'<CONTRACT_VALID_FROM>'+REPLACE(ISNULL(convert(varchar(11),CONTRACT_VALID_FROM,121),''),'-','')+'</CONTRACT_VALID_FROM>'+'<CONTRACT_VALID_TO>'+REPLACE(ISNULL(convert(varchar(11),CONTRACT_VALID_TO,121),''),'-','')+'</CONTRACT_VALID_TO>'+'<PO_NUMBER>'+ISNULL(NULL,'CPQ')+'</PO_NUMBER>'+'<PO_DATE>'+ISNULL(NULL,'')+'</PO_DATE>'+'<PO_NOTES>'+ISNULL(NULL,'')+'</PO_NOTES>'+'<INCOTERMS>'+ISNULL(CASE WHEN ISNULL(INCOTERMS,'')='' THEN 'DDP' ELSE INCOTERMS END,'DDP')+'</INCOTERMS>'+'<INCOTERMS_NOTES>'+ISNULL(CASE WHEN ISNULL(INCOTERMS_LOCATION,'')='' THEN 'Delivery At Airport' ELSE INCOTERMS_LOCATION END,'')+'</INCOTERMS_NOTES>'+'<PAYMENTTERM_ID>'+ISNULL(PAYMENTTERM_ID,'')+'</PAYMENTTERM_ID>'+'<NET_VALUE>'+ISNULL(convert(varchar,NET_VALUE),'')+'</NET_VALUE>'+'<OPPORTUNITY_ID>"+str(SAOPPR.OPPORTUNITY_ID)+"</OPPORTUNITY_ID>'+'<OPPORTUNITY_NAME>"+str(SAOPPR.OPPORTUNITY_NAME)+"</OPPORTUNITY_NAME>'+'<QUOTE_STATUS>'+ISNULL(QUOTE_STATUS,'')+'</QUOTE_STATUS>'+'<PRICING_DATE>'+REPLACE(ISNULL(convert(varchar(11),SAQTSO.EXCHANGE_RATE_DATE,121),''),'-','')+'</PRICING_DATE>'+'<EXCHANGE_RATE>'+ISNULL(convert(varchar,SAQTSO.EXCHANGE_RATE),'1')+'</EXCHANGE_RATE>'+'<EXCHANGE_RATE_TYPE>'+ISNULL('','')+'</EXCHANGE_RATE_TYPE>'+'<SALE_TYPE>'+ISNULL('','')+'</SALE_TYPE>'+'<CRM_CONTRACT_ID>'+ISNULL(CRM_CONTRACT_ID,'')+'</CRM_CONTRACT_ID>'+'<CANCELLATION_PERIOD>'+ISNULL(CANCELLATION_PERIOD,'')+'</CANCELLATION_PERIOD>'+'<EMAIL1>'+ISNULL('poc@email.com','')+'</EMAIL1>'+'<EMAIL2>'+ISNULL('poc@email.com','')+'</EMAIL2>'+'<EMAIL3>'+ISNULL('poc@email.com','')+'</EMAIL3>' AS final_xml  FROM SAQTMT(NOLOCK)  JOIN SAQTSO (NOLOCK) ON SAQTMT.QUOTE_ID = SAQTSO.QUOTE_ID WHERE SAQTMT.QUOTE_ID = '"+str(QUOTE_ID)+"')A FOR XML PATH ('')  ), 1, 1, ''),'&lt;','<'),'&gt;','>')AS RESULT")
		
		if str(Quoteheaderquery.RESULT) != "" :
			Quoteheaderquery = str(Quoteheaderquery.RESULT)
		else:
			Quoteheaderquery = "<QUOTE_HEADER>"
		
		# QUOTE_INVOLVED_PARTY QUERY
		QuoteInvolvedPartiesquery = SqlHelper.GetFirst("select replace(replace(STUFF((SELECT  ' '+final_xml FROM (SELECT DISTINCT  '<QUOTE_INVOLVED_PARTY>'+'<QUOTE_ID>"+str(CRMQT.c4c_quote_id)+"</QUOTE_ID><SOLD_TO>'+ ISNULL((SELECT REPLACE(ACCOUNT_ID,'STP-','') FROM SAQTMT(NOLOCK) WHERE QUOTE_ID = '"+str(QUOTE_ID)+"' ),'') + '</SOLD_TO><BILL_TO>'+ISNULL((SELECT TOP 1 PARTY_ID FROM SAQTIP(NOLOCK) WHERE QUOTE_ID = '"+str(QUOTE_ID)+"' AND PARTY_ROLE = 'BILL TO' ),'')+'</BILL_TO><SHIP_TO>'+ISNULL((SELECT TOP 1 PARTY_ID FROM SAQTIP(NOLOCK) WHERE QUOTE_ID = '"+str(QUOTE_ID)+"' AND PARTY_ROLE = 'SHIP TO' ),'')+'</SHIP_TO><PAYER>'+ISNULL((SELECT TOP 1 PARTY_ID FROM SAQTIP(NOLOCK) WHERE QUOTE_ID = '"+str(QUOTE_ID)+"' AND PARTY_ROLE = 'PAYER' ),'')+'</PAYER><GPMRPM>'+ISNULL((SELECT TOP 1 PARTY_ID FROM SAQTIP(NOLOCK) WHERE QUOTE_ID = '"+str(QUOTE_ID)+"' AND PARTY_ROLE = 'GPMRPM' ),'')+'</GPMRPM><CONT_MNGR>'+ISNULL((SELECT TOP 1  CONVERT(VARCHAR(10),PARTY_ID) FROM SAQTIP(NOLOCK) WHERE QUOTE_ID = '"+str(QUOTE_ID)+"' AND PARTY_ROLE = 'CONTRACT MANAGER' ),'')+'</CONT_MNGR><SALES_PERSON>'+ISNULL((SELECT TOP 1 CONVERT(VARCHAR(10),PARTY_ID) FROM SAQTIP(NOLOCK) WHERE QUOTE_ID = '"+str(QUOTE_ID)+"' AND PARTY_ROLE = 'SALES EMPLOYEE' ),'')+'</SALES_PERSON>' AS final_xml  FROM SAQTIP(NOLOCK) WHERE QUOTE_ID = '"+str(QUOTE_ID)+"')A FOR XML PATH ('')  ), 1, 1, ''),'&lt;','<'),'&gt;','>')AS RESULT")
		
		if str(QuoteInvolvedPartiesquery.RESULT) != "" :
			QuoteInvolvedPartiesquery = str(QuoteInvolvedPartiesquery.RESULT)
			
			QuoteInvolvedPartiesfabquery = SqlHelper.GetFirst("select replace(replace(STUFF((SELECT  ' '+final_xml FROM (SELECT  '<FAB>'+CASE WHEN ISNULl(CRM_FABLOCATION_ID,'')<>'' THEN CRM_FABLOCATION_ID ELSE ISNULL(SAQFBL.FABLOCATION_ID,'') END+'</FAB>' AS final_xml  FROM SAQFBL(NOLOCK) JOIN MAFBLC (NOLOCK) ON SAQFBL.FABLOCATION_ID = MAFBLC.FAB_LOCATION_ID WHERE QUOTE_ID  = '"+str(QUOTE_ID)+"')SUB_SAQFBL FOR XML PATH ('')  ), 1, 1, ''),'&lt;','<'),'&gt;','>')AS RESULT")
			
			if str(QuoteInvolvedPartiesfabquery.RESULT) != "" :
			
				QuoteInvolvedPartiesquery = QuoteInvolvedPartiesquery+str(QuoteInvolvedPartiesfabquery.RESULT)+'</QUOTE_INVOLVED_PARTY>'
			else:
				QuoteInvolvedPartiesquery = QuoteInvolvedPartiesquery+'<FAB></FAB></QUOTE_INVOLVED_PARTY>'
			
		else:
			QuoteInvolvedPartiesquery = "<QUOTE_INVOLVED_PARTY></QUOTE_INVOLVED_PARTY>"
		
		if str(QTYPE.quote_type) == "ZWK1":
			
			Quoteitemquery = SqlHelper.GetFirst("SELECT REPLACE(REPLACE(REPLACE(REPLACE(REPLACE((select replace(replace(STUFF((SELECT  ' '+final_xml FROM ( SELECT '<QUOTE_ITEM>'+'<QUOTE_ID>"+str(CRMQT.c4c_quote_id)+"</QUOTE_ID>'+'<ITEM_LINE_ID>'+ISNULL(convert(varchar(100),A.LINE_ITEM_ID),'')+'</ITEM_LINE_ID>'+'<SERVICE_ID>'+A.SERVICE_ID+'</SERVICE_ID>'+'<QUANTITY>'+ISNULL(convert(varchar,A.QUANTITY),'')+'</QUANTITY>'+'<TAX_GROUP>'+ISNULL(convert(varchar,A.SRVTAXCLA_ID),'')+'</TAX_GROUP>'+'<UOM_ID>'+ISNULL(A.UOM_ID,'')+'</UOM_ID>'+'<NET_VALUE>'+ISNULL(convert(varchar,A.EXTENDED_PRICE),'')+'</NET_VALUE>'+'<ITEM_TYPE>'+ISNULL(A.ITEM_TYPE,'')+'</ITEM_TYPE>'+'<PO_NUMBER>'+CASE WHEN ISNULL(A.PO_NUMBER,'')='' THEN CONVERT(VARCHAR(10),A.CPQTABLEENTRYID) ELSE A.PO_NUMBER END +'</PO_NUMBER>'+'<PO_ITEM>'+CASE WHEN ISNULL(A.PO_ITEM,'')='' THEN  CONVERT(VARCHAR(10),A.LINE_ITEM_ID) ELSE A.PO_ITEM END +'</PO_ITEM>'+'<PO_TEXT>'+ISNULL(A.PO_NOTES,'')+'</PO_TEXT>' +'<PLANT_ID>'+ISNULL(A.PLANT_ID,'')+'</PLANT_ID>'+'<QUOTE_START_DATE>'+REPLACE(ISNULL(convert(varchar(11),A.LINE_ITEM_FROM_DATE,121),''),'-','')+'</QUOTE_START_DATE>'+'<QUOTE_END_DATE>'+REPLACE(ISNULL(convert(varchar(11),A.LINE_ITEM_TO_DATE,121),''),'-','')+'</QUOTE_END_DATE>'+'<INTERNAL_NOTES>'+ISNULL(INTERNAL_NOTES,'')+'</INTERNAL_NOTES>'+'<ITEM_STATUS>'+ISNULL(A.ITEM_STATUS,'')+'</ITEM_STATUS><CONTRACT_TYPE>'+(SELECT LEFT(QUOTE_TYPE,4) FROM SAQTMT (NOLOCK ) WHERE SAQTMT.QUOTE_ID= '"+str(QUOTE_ID)+"')+'</CONTRACT_TYPE><QUOTE_ITEM_COVERED_OBJECT></QUOTE_ITEM_COVERED_OBJECT><QUOTE_ITEM_BILLING_PLAN><ITEM_LINE_ID></ITEM_LINE_ID><BILLING_START_DATE></BILLING_START_DATE><BILLING_AMOUNT></BILLING_AMOUNT></QUOTE_ITEM_BILLING_PLAN><QUOTE_ITEM_PARTS></QUOTE_ITEM_PARTS>'+ ISNULL((SELECT TOP 1 ET_XML FROM "+str(SAQTSE)+" WHERE QUOTE_ID = '"+str(QUOTE_ID)+"'),'<QUOTE_ITEM_ENTITLEMENT></QUOTE_ITEM_ENTITLEMENT>')+ISNULL(REPLACE(REPLACE(STUFF((SELECT ' '+ JSON FROM (SELECT '<QUOTE_ITEM_FPM>'+'<ITEM_LINE_ID>'+ISNULL(convert(varchar(100),SUB_SAQITM.LINE_ITEM_ID),'')+'</ITEM_LINE_ID>'+'<ACCPRT_NUMBER>'+ISNULL(CUSTOMER_PART_NUMBER,'')+'</ACCPRT_NUMBER>'+'<PART_NUMBER>'+ISNULL(PART_NUMBER,'')+'</PART_NUMBER>'+'<PRICEGROUP_ID>'+ISNULL(MATPRIGRP_ID,'')+'</PRICEGROUP_ID>'+'<SCHEDULE_MODE>'+ISNULL(SCHEDULE_MODE,'')+'</SCHEDULE_MODE>'+'<DELIVERY_MODE>'+ISNULL(DELIVERY_MODE,'')+'</DELIVERY_MODE>' +'<ANNUAL_QUANTITY>'+ISNULL(convert(varchar,ANNUAL_QUANTITY),'')+'</ANNUAL_QUANTITY>'+'<UNIT_PRICE>'+ISNULL(convert(varchar,UNIT_PRICE),'')+'</UNIT_PRICE>'+'<VALID_FROM_DATE>'+REPLACE(ISNULL(convert(varchar(11),VALID_FROM_DATE,121),''),'-','')+'</VALID_FROM_DATE>'+'<VALID_TO_DATE>'+REPLACE(ISNULL(convert(varchar(11),VALID_TO_DATE,121),''),'-','')+'</VALID_TO_DATE>'+'</QUOTE_ITEM_FPM>' AS JSON FROM (SELECT ISNULL(convert(varchar(100),SAQITM.LINE_ITEM_ID),'') AS LINE_ITEM_ID,CUSTOMER_PART_NUMBER,PART_NUMBER,SAQIFP.MATPRIGRP_ID, CASE WHEN SCHEDULE_MODE='SCHEDULED' THEN '1' WHEN SCHEDULE_MODE='UNSCHEDULED' THEN '2' WHEN SCHEDULE_MODE='TLS SHARED' THEN '3' WHEN SCHEDULE_MODE='TLS NON-SHARED' THEN '4' WHEN SCHEDULE_MODE='LOW QTY ONSITE' THEN '5' WHEN SCHEDULE_MODE='ON REQUEST' THEN '6' ELSE SCHEDULE_MODE END AS SCHEDULE_MODE, CASE WHEN DELIVERY_MODE='ONSITE' THEN '1' WHEN DELIVERY_MODE='OFFSITE' THEN '2' ELSE DELIVERY_MODE END AS DELIVERY_MODE,ANNUAL_QUANTITY,UNIT_PRICE,VALID_FROM_DATE,VALID_TO_DATE  FROM SAQITM(NOLOCK) JOIN SAQIFP (NOLOCK) ON SAQITM.QUOTE_ID = SAQIFP.QUOTE_ID AND SAQITM.LINE_ITEM_ID = SAQIFP.LINE_ITEM_ID WHERE SAQITM.QUOTE_ID = '"+str(QUOTE_ID)+"' )SUB_SAQITM )A FOR XML PATH ('')  ), 1, 1,'' ),'&lt;','<'),'&gt;','>'),'<QUOTE_ITEM_FPM></QUOTE_ITEM_FPM>')+'</QUOTE_ITEM>' AS final_xml  FROM SAQITM(NOLOCK) WHERE SAQITM.QUOTE_ID = '"+str(QUOTE_ID)+"' )A FOR XML PATH ('')  ), 1, 1, ''),'&lt;','<'),'&gt;','>')AS RESULT),'<QUOTE_ITEM_BILLING_PLAN><ITEM_LINE_ID></ITEM_LINE_ID><BILLING_START_DATE></BILLING_START_DATE><BILLING_AMOUNT></BILLING_AMOUNT></QUOTE_ITEM_BILLING_PLAN>','<QUOTE_ITEM_BILLING_PLAN></QUOTE_ITEM_BILLING_PLAN>' ),'<QUOTE_ITEM_COVERED_OBJECT><ITEM_LINE_ID></ITEM_LINE_ID><EQUIPMENT_ID></EQUIPMENT_ID><SERIAL_NUMBER></SERIAL_NUMBER> </QUOTE_ITEM_COVERED_OBJECT>','<QUOTE_ITEM_COVERED_OBJECT></QUOTE_ITEM_COVERED_OBJECT>'),'<QUOTE_ITEM_PARTS><QUOTE_ID></QUOTE_ID><ITEM_LINE_ID></ITEM_LINE_ID><PART_NUMBER></PART_NUMBER><PART_DESCRIPTION></PART_DESCRIPTION><QUANTITY></QUANTITY></QUOTE_ITEM_PARTS>','<QUOTE_ITEM_PARTS></QUOTE_ITEM_PARTS>' ),'<QUOTE_ITEM_ENTITLEMENT><ITEM_LINE_ID></ITEM_LINE_ID><SERVICE_ID></SERVICE_ID><ENTITLEMENT_NAME></ENTITLEMENT_NAME><ENTITLEMENT_VALUE></ENTITLEMENT_VALUE></QUOTE_ITEM_ENTITLEMENT>','<QUOTE_ITEM_ENTITLEMENT></QUOTE_ITEM_ENTITLEMENT>'),'<QUOTE_ITEM_FPM><ITEM_LINE_ID></ITEM_LINE_ID><ACCPRT_NUMBER></ACCPRT_NUMBER><PART_NUMBER></PART_NUMBER><PRICEGROUP_ID></PRICEGROUP_ID><SCHEDULE_MODE></SCHEDULE_MODE><DELIVERY_MODE></DELIVERY_MODE><ANNUAL_QUANTITY></ANNUAL_QUANTITY><UNIT_PRICE></UNIT_PRICE><VALID_FROM_DATE></VALID_FROM_DATE><VALID_TO_DATE></VALID_TO_DATE></QUOTE_ITEM_FPM>','<QUOTE_ITEM_FPM></QUOTE_ITEM_FPM>' ) AS A ")
			
		
		else:
		
			Quoteitemquery = SqlHelper.GetFirst("select replace(replace(STUFF((SELECT  ' '+final_xml FROM ( SELECT DISTINCT '<QUOTE_ITEM>'+'<QUOTE_ID>"+str(CRMQT.c4c_quote_id)+"</QUOTE_ID>'+'<ITEM_LINE_ID>'+ISNULL(convert(varchar(100),A.EQUIPMENT_LINE_ID),'')+'</ITEM_LINE_ID>'+'<SERVICE_ID>'+SAP_PART_NUMBER+'</SERVICE_ID>'+'<QUANTITY>'+ISNULL(convert(varchar,A.QUANTITY),'')+'</QUANTITY>'+'<TAX_GROUP>'+ISNULL(convert(varchar,A.SRVTAXCLA_ID),'')+'</TAX_GROUP>'+'<UOM_ID>'+ISNULL(A.UOM_ID,'')+'</UOM_ID>'+'<NET_VALUE>'+ISNULL(convert(varchar,A.EXTENDED_PRICE),'')+'</NET_VALUE>'+'<ITEM_TYPE>'+ISNULL(A.ITEM_TYPE,'')+'</ITEM_TYPE>'+'<PO_NUMBER>'+CASE WHEN ISNULL(A.PO_NUMBER,'')='' THEN '' ELSE A.PO_NUMBER END +'</PO_NUMBER>'+'<PO_ITEM>'+CASE WHEN ISNULL(A.PO_ITEM,'')='' THEN '' ELSE A.PO_ITEM END+'</PO_ITEM>'+'<PO_TEXT>'+ISNULL(A.PO_NOTES,'')+'</PO_TEXT>' +'<PLANT_ID>'+ISNULL(A.PLANT_ID,'')+'</PLANT_ID>'+'<QUOTE_START_DATE>'+REPLACE(ISNULL(convert(varchar(11),A.LINE_ITEM_FROM_DATE,121),''),'-','')+'</QUOTE_START_DATE>'+'<QUOTE_END_DATE>'+REPLACE(ISNULL(convert(varchar(11),A.LINE_ITEM_TO_DATE,121),''),'-','')+'</QUOTE_END_DATE>'+'<INTERNAL_NOTES>'+ISNULL(A.INTERNAL_NOTES,'')+'</INTERNAL_NOTES>'+'<ITEM_STATUS>'+ISNULL(A.ITEM_STATUS,'')+'</ITEM_STATUS><CONTRACT_TYPE>'+(SELECT LEFT(QUOTE_TYPE,4) FROM SAQTMT A(NOLOCK ) WHERE A.QUOTE_ID= '"+str(QUOTE_ID)+"')+'</CONTRACT_TYPE>'+ISNULL(REPLACE(REPLACE(STUFF((SELECT ' '+ JSON FROM (SELECT '<QUOTE_ITEM_COVERED_OBJECT>'+'<ITEM_LINE_ID>'+CASE WHEN ISNULL(A.EQUIPMENT_ID,'') <> '' THEN ISNULL(convert(varchar(100),A.EQUIPMENT_LINE_ID),'')ELSE '' END+'</ITEM_LINE_ID>'+'<EQUIPMENT_ID>'+ISNULL(A.EQUIPMENT_ID,'')+'</EQUIPMENT_ID>'+'<SERIAL_NUMBER>'+ISNULL(A.SERIAL_NO,'')+'</SERIAL_NUMBER>'+'</QUOTE_ITEM_COVERED_OBJECT>'  AS JSON FROM ( SELECT DISTINCT B.EQUIPMENT_LINE_ID,B.EQUIPMENT_ID,B.SERIAL_NO FROM "+str(SAQICO)+" (NOLOCK)B WHERE B.QUOTE_ID = A.QUOTE_ID AND B.SERVICE_ID = A.SERVICE_ID AND B.EQUIPMENT_LINE_ID = A.EQUIPMENT_LINE_ID )A )A FOR XML PATH ('')  ), 1, 1,'' ),'&lt;','<'),'&gt;','>'),'<QUOTE_ITEM_COVERED_OBJECT></QUOTE_ITEM_COVERED_OBJECT>')+ISNULL(BP_XML ,'<QUOTE_ITEM_BILLING_PLAN></QUOTE_ITEM_BILLING_PLAN>')+ISNULL(REPLACE(REPLACE(STUFF((SELECT ' '+ JSON FROM (SELECT '<QUOTE_ITEM_PARTS>'+'<QUOTE_ID>"+str(CRMQT.c4c_quote_id)+"</QUOTE_ID>'+'<ITEM_LINE_ID>'+ISNULL(CONVERT(VARCHAR(100),A.EQUIPMENT_LINE_ID),'')+'</ITEM_LINE_ID>'+'<PART_NUMBER>'+ISNULL(A.PART_NUMBER,'')+'</PART_NUMBER>'+'<PART_DESCRIPTION>'+ISNULL(A.PART_DESCRIPTION,'')+'</PART_DESCRIPTION>'+'<QUANTITY>'+ISNULL(convert(varchar,A.QUANTITY),'')+'</QUANTITY>'+'</QUOTE_ITEM_PARTS>'  AS JSON FROM ( SELECT DISTINCT A.EQUIPMENT_LINE_ID,KIT_NUMBER AS PART_NUMBER,KIT_NAME AS PART_DESCRIPTION, 1 AS QUANTITY FROM "+str(SAQSAP)+" (NOLOCK)B JOIN "+str(SAQICO)+" C(NOLOCK) ON B.QUOTE_ID = C.QUOTE_ID AND B.SERVICE_ID = C.SERVICE_ID AND B.EQUIPMENT_ID = C.EQUIPMENT_ID WHERE B.QUOTE_ID = A.QUOTE_ID AND B.SERVICE_ID = A.SERVICE_ID AND C.EQUIPMENT_LINE_ID = A.EQUIPMENT_LINE_ID AND ISNULL(KIT_NUMBER,'')<>'' )A )A FOR XML PATH ('')  ), 1, 1,'' ),'&lt;','<'),'&gt;','>'),'<QUOTE_ITEM_PARTS></QUOTE_ITEM_PARTS>')+ISNULL(ET_XML,'<QUOTE_ITEM_ENTITLEMENT></QUOTE_ITEM_ENTITLEMENT>')+ISNULL(REPLACE(REPLACE(STUFF((SELECT ' '+ JSON FROM (SELECT '<QUOTE_ITEM_FPM>'+'<ITEM_LINE_ID>'+ISNULL(convert(varchar(100),A.EQUIPMENT_LINE_ID),'')+'</ITEM_LINE_ID>'+'<ACCPRT_NUMBER>'+ISNULL(CUSTOMER_PART_NUMBER,'')+'</ACCPRT_NUMBER>'+'<PART_NUMBER>'+ISNULL(PART_NUMBER,'')+'</PART_NUMBER>'+'<PRICEGROUP_ID>'+ISNULL(MATPRIGRP_ID,'')+'</PRICEGROUP_ID>'+'<SCHEDULE_MODE>'+ISNULL(SCHEDULE_MODE,'')+'</SCHEDULE_MODE>'+'<DELIVERY_MODE>'+ISNULL(DELIVERY_MODE,'')+'</DELIVERY_MODE>' +'<ANNUAL_QUANTITY>'+ISNULL(convert(varchar,ANNUAL_QUANTITY),'')+'</ANNUAL_QUANTITY>'+'<UNIT_PRICE>'+ISNULL(convert(varchar,UNIT_PRICE),'')+'</UNIT_PRICE>'+'<VALID_FROM_DATE>'+REPLACE(ISNULL(convert(varchar(11),VALID_FROM_DATE,121),''),'-','')+'</VALID_FROM_DATE>'+'<VALID_TO_DATE>'+REPLACE(ISNULL(convert(varchar(11),VALID_TO_DATE,121),''),'-','')+'</VALID_TO_DATE>'+'</QUOTE_ITEM_FPM>' AS JSON FROM ( SELECT ISNULL(convert(varchar(100),A.EQUIPMENT_LINE_ID),'') AS EQUIPMENT_LINE_ID,CUSTOMER_PART_NUMBER,PART_NUMBER,B.MATPRIGRP_ID, CASE WHEN SCHEDULE_MODE='SCHEDULED' THEN '1' WHEN SCHEDULE_MODE='UNSCHEDULED' THEN '2' WHEN SCHEDULE_MODE='TLS SHARED' THEN '3' WHEN SCHEDULE_MODE='TLS NON-SHARED' THEN '4' WHEN SCHEDULE_MODE='LOW QTY ONSITE' THEN '5' WHEN SCHEDULE_MODE='ON REQUEST' THEN '6' ELSE SCHEDULE_MODE END AS SCHEDULE_MODE, CASE WHEN DELIVERY_MODE='ONSITE' THEN '1' WHEN DELIVERY_MODE='OFFSITE' THEN '2' ELSE DELIVERY_MODE END AS DELIVERY_MODE,ANNUAL_QUANTITY,UNIT_PRICE,VALID_FROM_DATE,VALID_TO_DATE  FROM "+str(SAQICO)+"(NOLOCK) A JOIN SAQIFP B(NOLOCK) ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID WHERE A.QUOTE_ID = '"+str(QUOTE_ID)+"'  )A )A FOR XML PATH ('')  ), 1, 1,'' ),'&lt;','<'),'&gt;','>'),'<QUOTE_ITEM_FPM></QUOTE_ITEM_FPM>')+'</QUOTE_ITEM>' AS final_xml  FROM "+str(SAQITM)+" (NOLOCK) A JOIN "+str(SAQICO)+"  B1(NOLOCK) ON A.QUOTE_ID = B1.QUOTE_ID AND A.SERVICE_ID = B1.SERVICE_ID AND A.EQUIPMENT_LINE_ID = B1.EQUIPMENT_LINE_ID JOIN MAMTRL V(NOLOCK) ON A.SERVICE_RECORD_ID = V.MATERIAL_RECORD_ID WHERE A.QUOTE_ID = '"+str(QUOTE_ID)+"'   )A FOR XML PATH ('')  ), 1, 1, ''),'&lt;','<'),'&gt;','>')AS A ")

		if str(Quoteitemquery.A) == '':
			Quoteiteminfo = '<QUOTE_ITEM><QUOTE_ITEM_COVERED_OBJECT></QUOTE_ITEM_COVERED_OBJECT><QUOTE_ITEM_BILLING_PLAN></QUOTE_ITEM_BILLING_PLAN><QUOTE_ITEM_PARTS></QUOTE_ITEM_PARTS><QUOTE_ITEM_ENTITLEMENT></QUOTE_ITEM_ENTITLEMENT><QUOTE_ITEM_FPM></QUOTE_ITEM_FPM></QUOTE_ITEM>'
		else:
			Quoteiteminfo = str(Quoteitemquery.A)
	
		str_xml = str(Quoteheaderquery)+str(Quoteiteminfo)+str(QuoteInvolvedPartiesquery)+'</QUOTE_HEADER>'
		data = data+str_xml

	Final_xml = "<QUOTE>"+str(data)+"</QUOTE>"

	Parameter = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'SELECT' ")
		
	"""primaryQueryItems = SqlHelper.GetFirst( ""+ str(Parameter.QUERY_CRITERIA_1)+ " SYINPL (INTEGRATION_PAYLOAD,INTEGRATION_KEY,CpqTableEntryDateModified,INTEGRATION_NAME)  select ''"+str(Final_xml)+ "'',''"+ str(Qt_id)+ "'',getdate(),''CPQ to CRM Quote Replication'' ' ")"""

	SAQICO_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQICO)+"'' ) BEGIN DROP TABLE "+str(SAQICO)+" END  ' ")
	SAQIBP_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQIBP)+"'' ) BEGIN DROP TABLE "+str(SAQIBP)+" END  ' ")
	SAQIEN_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQIEN)+"'' ) BEGIN DROP TABLE "+str(SAQIEN)+" END  ' ")
	SAQSAP_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQSAP)+"'' ) BEGIN DROP TABLE "+str(SAQSAP)+" END  ' ")
	SAQTSE_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQTSE)+"'' ) BEGIN DROP TABLE "+str(SAQTSE)+" END  ' ")
	SAQITM_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQITM)+"'' ) BEGIN DROP TABLE "+str(SAQITM)+" END  ' ")
	
	#OAUTH AUTHENTICATION
	
	LOGIN_CRE = SqlHelper.GetFirst("SELECT URL FROM SYCONF (nolock) where EXTERNAL_TABLE_NAME ='CPQ_TO_CRM_QUOTE'")
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
	Log.Info("789 crm_response --->"+str(crm_response))	
	
	if 'tid' in crm_response:		
		ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "200", "Message": "Data Successfully Sent to CRM."}]})
	else:
		SAQICO_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQICO)+"'' ) BEGIN DROP TABLE "+str(SAQICO)+" END  ' ")
		SAQIBP_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQIBP)+"'' ) BEGIN DROP TABLE "+str(SAQIBP)+" END  ' ")
		SAQIEN_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQIEN)+"'' ) BEGIN DROP TABLE "+str(SAQIEN)+" END  ' ")
		SAQSAP_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQSAP)+"'' ) BEGIN DROP TABLE "+str(SAQSAP)+" END  ' ")
		SAQTSE_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQTSE)+"'' ) BEGIN DROP TABLE "+str(SAQTSE)+" END  ' ")
		SAQITM_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQITM)+"'' ) BEGIN DROP TABLE "+str(SAQITM)+" END  ' ")
		
		ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "400", "Message": str(crm_response)}]})
	
	
except:
	for QUOTE_ID in input_data:	

		Qt_id = QUOTE_ID

		CRMQT = SqlHelper.GetFirst("select convert(varchar(100),c4c_quote_id) as c4c_quote_id from SAQTMT(nolock) WHERE QUOTE_ID = '"+str(QUOTE_ID)+"' ")

		QTYPE = SqlHelper.GetFirst("select left(quote_type,4) as quote_type from SAQTMT(nolock) WHERE QUOTE_ID = '"+str(QUOTE_ID)+"' ")

		SAOPPR = SqlHelper.GetFirst("select convert(varchar(100),OPPORTUNITY_ID) as OPPORTUNITY_ID,OPPORTUNITY_NAME from SAOPQT(nolock) WHERE QUOTE_ID = '"+str(QUOTE_ID)+"' ")

		SAQICO = "SAQICO_BKP_"+str(CRMQT.c4c_quote_id)
		SAQIBP = "SAQIBP_BKP_"+str(CRMQT.c4c_quote_id)
		SAQIEN = "SAQIEN_BKP_"+str(CRMQT.c4c_quote_id)
		SAQSAP = "SAQSAP_BKP_"+str(CRMQT.c4c_quote_id)
		SAQTSE = "SAQTSE_BKP_"+str(CRMQT.c4c_quote_id)
		SAQITM = "SAQITM_BKP_"+str(CRMQT.c4c_quote_id)
		
		SAQICO_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQICO)+"'' ) BEGIN DROP TABLE "+str(SAQICO)+" END  ' ")
		SAQIBP_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQIBP)+"'' ) BEGIN DROP TABLE "+str(SAQIBP)+" END  ' ")
		SAQIEN_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQIEN)+"'' ) BEGIN DROP TABLE "+str(SAQIEN)+" END  ' ")
		SAQSAP_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQSAP)+"'' ) BEGIN DROP TABLE "+str(SAQSAP)+" END  ' ")
		SAQTSE_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQTSE)+"'' ) BEGIN DROP TABLE "+str(SAQTSE)+" END  ' ")
		SAQITM_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQITM)+"'' ) BEGIN DROP TABLE "+str(SAQITM)+" END  ' ")
		

	Log.Info("QTPOSTQCRMQTPOSTQCRM ERROR---->:" + str(sys.exc_info()[1]))
	Log.Info("QTPOSTQCRM ERROR LINE NO---->:" + str(sys.exc_info()[-1].tb_lineno))
	ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "400", "Message": str(sys.exc_info()[1])}]})
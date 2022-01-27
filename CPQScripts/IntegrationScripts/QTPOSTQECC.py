# =========================================================================================================================================
#   __script_name : QTPOSTQECC.PY
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

		SAQITM_DRP = SqlHelper.GetFirst("sp_executesql @T=N'select distinct SAQRIT.QUOTE_ID,SAQRIT.SERVICE_ID,SAQRIT.LINE,SAQRIT.QUANTITY,MAMTRL.UNIT_OF_MEASURE AS UOM_ID,SAQRIT.NET_PRICE AS EXTENDED_PRICE,'''' AS ITEM_TYPE,'''' AS PO_NUMBER,'''' AS PO_ITEM,'''' AS PO_NOTES,SAQRIT.PLANT_ID,SAQRIT.CONTRACT_VALID_FROM AS LINE_ITEM_FROM_DATE,SAQRIT.CONTRACT_VALID_TO AS LINE_ITEM_TO_DATE,'''' AS INTERNAL_NOTES,SAQRIT.STATUS,SAQRIT.SERVICE_RECORD_ID,SAQRIT.TAXCLASSIFICATION_ID AS SRVTAXCLA_ID,CONVERT(NVARCHAR(MAX),'''') AS BP_XML,CONVERT(NVARCHAR(MAX),'''') AS ET_XML,ISNULL(GL_ACCOUNT_NO,'''') AS GL_ACCOUNT_NO,ISNULL(REF_SALESORDER,'''') AS REF_SALESORDER_NO INTO "+str(SAQITM)+" FROM SAQRIT (NOLOCK) JOIN MAMTRL (NOLOCK) ON SAQRIT.SERVICE_ID = MAMTRL.SAP_PART_NUMBER WHERE SAQRIT.QUOTE_ID = ''"+str(QUOTE_ID)+"'' AND SAQRIT.QTEREV_ID = ''"+str(REVISION_ID)+"''  ' ")

		SAQITM_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQIEN)+"'' ) BEGIN DROP TABLE "+str(SAQIBP)+" END CREATE TABLE "+str(SAQIEN)+" (QUOTE_ID VARCHAR(100),SERVICE_ID VARCHAR(100),LINE VARCHAR(100),ENTITLEMENT_NAME VARCHAR(100),ENTITLEMENT_VALUE_CODE VARCHAR(100))' ")

		SAQICO_BKP = SqlHelper.GetFirst("sp_executesql @T=N'select QUOTE_ID,SERVICE_ID,LINE,EQUIPMENT_ID,SERIAL_NUMBER,NULL AS EXTENDED_PRICE,NULL AS SRVTAXCLA_ID,CONVERT(VARCHAR(100),NULL) AS PAR_SERVICE_ID INTO "+str(SAQICO)+" from SAQRIO(NOLOCK) WHERE QUOTE_ID = ''"+str(QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(REVISION_ID)+"'' ' ")

		SAQIBP_BKP = SqlHelper.GetFirst("sp_executesql @T=N'select QUOTE_ID,MAMTRL.SAP_PART_NUMBER AS SERVICE_ID,LINE ,REPLACE(CONVERT(VARCHAR(11),BILLING_DATE,121),''-'','''') AS BILLING_DATE,BILLING_VALUE AS BILLING_AMOUNT,EQUIPMENT_ID INTO "+str(SAQIBP)+" from SAQIBP(NOLOCK)  JOIN MAMTRL (NOLOCK) ON SAQIBP.SERVICE_RECORD_ID = MAMTRL.MATERIAL_RECORD_ID WHERE QUOTE_ID = ''"+str(QUOTE_ID)+"''  AND QTEREV_ID = ''"+str(REVISION_ID)+"'' ' ")

		SAQSAP_BKP = SqlHelper.GetFirst("sp_executesql @T=N'select QUOTE_ID,SERVICE_ID,LINE,PART_NUMBER,PART_DESCRIPTION,ISNULL(NEW_PART,''FALSE'') AS NEW_PART,QUANTITY INTO "+str(SAQSAP)+" from SAQRIP(NOLOCK) WHERE QUOTE_ID = ''"+str(QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(REVISION_ID)+"''  ' ")

		SAQTSE_BKP = SqlHelper.GetFirst("sp_executesql @T=N'select LINE,QUOTE_ID,MAMTRL.SAP_PART_NUMBER AS SERVICE_ID,CONVERT(VARCHAR(MAX),'''') AS ET_XML INTO "+str(SAQTSE)+" from SAQRIT(NOLOCK) JOIN MAMTRL (NOLOCK) ON SAQRIT.SERVICE_RECORD_ID = MAMTRL.MATERIAL_RECORD_ID WHERE QUOTE_ID = ''"+str(QUOTE_ID)+"'' AND SAQRIT.QTEREV_ID = ''"+str(REVISION_ID)+"'' ' ")

		Quoteitemquer = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE B SET BP_XML= final_xml FROM (SELECT A.LINE, ISNULL(REPLACE(REPLACE(STUFF((SELECT '' ''+ JSON FROM (SELECT ''<QUOTE_ITEM_BILLING_PLAN>''+''<ITEM_LINE_ID>''+ISNULL(CONVERT(VARCHAR(100),A.LINE),'''')+''</ITEM_LINE_ID>''+''<SERVICE_ID>''+ISNULL(A.SERVICE_ID,'''')+''</SERVICE_ID>''+''<BILLING_START_DATE>''+ISNULL(A.BILLING_DATE,'''')+''</BILLING_START_DATE>''+''<BILLING_AMOUNT>''+ISNULL(CONVERT(VARCHAR(100),A.BILLING_AMOUNT),'''')+''</BILLING_AMOUNT>''+''</QUOTE_ITEM_BILLING_PLAN>'' AS JSON FROM ( 	SELECT LINE,B.SERVICE_ID,REPLACE(CONVERT(VARCHAR(11),BILLING_DATE,121),''-'','''') AS BILLING_DATE, SUM(BILLING_AMOUNT) AS BILLING_AMOUNT FROM "+str(SAQIBP)+" B(NOLOCK) WHERE A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.LINE = B.LINE AND B.QUOTE_ID = ''"+str(QUOTE_ID)+"'' GROUP BY B.LINE,B.SERVICE_ID,BILLING_DATE )A )A FOR XML PATH ('''')  ), 1, 1,'''' ),''&lt;'',''<''),''&gt;'',''>''),'''') AS final_xml  FROM "+str(SAQITM)+" (NOLOCK) A WHERE A.QUOTE_ID = ''"+str(QUOTE_ID)+"'' )A JOIN "+str(SAQITM)+" B(NOLOCK) ON A.LINE = B.LINE '")
		
		start2 = 1
		end2 = 1

		Check_flag2 = 1
		while Check_flag2 == 1:

			table11 = SqlHelper.GetFirst(
				"SELECT DISTINCT LINE FROM (SELECT DISTINCT LINE, ROW_NUMBER()OVER(ORDER BY LINE) AS SNO FROM(SELECT DISTINCT LINE FROM "+str(SAQITM)+"  (NOLOCK) where quote_id='"+str(QUOTE_ID)+"' ) A )A WHERE SNO>= "+str(start2)+" AND SNO<="+str(end2)+""
			)
					
			CRMTMP11 = SqlHelper.GetFirst("sp_executesql @T=N'IF NOT EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(CRMTMP)+"'' ) BEGIN CREATE TABLE "+str(CRMTMP)+" (EQUIPMENT_IDD VARCHAR(100)) END  ' ")
			
			table3 = SqlHelper.GetFirst(
		"sp_executesql @T=N'INSERT "+str(CRMTMP)+" SELECT DISTINCT LINE FROM (SELECT DISTINCT LINE, ROW_NUMBER()OVER(ORDER BY LINE) AS SNO FROM(SELECT DISTINCT LINE FROM "+str(SAQITM)+"  (NOLOCK) where quote_id=''"+str(QUOTE_ID)+"'' ) A )A WHERE SNO>= "+str(start2)+" AND SNO<="+str(end2)+"  '")
			
			start2 = start2 + 1
			end2 = end2 + 1

			if str(table11) != "None":
					
				SAQIEN_SEL = SqlHelper.GetFirst("sp_executesql @T=N'declare @H int; Declare @val Varchar(MAX);DECLARE @XML XML; SELECT @val = FINAL from(select  REPLACE(entitlement_xml,''<QUOTE_ITEM_ENTITLEMENT>'',sml) AS FINAL FROM (select ''<QUOTE_ITEM_ENTITLEMENT><QUOTE_ID>''+quote_id+''</QUOTE_ID><SERVICE_ID>''+service_id+''</SERVICE_ID><LINE>''+CONVERT(VARCHAR,LINE)+''</LINE>'' AS sml,replace(replace(replace(replace(replace(replace(replace(ENTITLEMENT_XML,''&'','';#38''),'''','';#39''),'' < '','' &lt; '' ),'' > '','' &gt; '' ),''_>'',''_&gt;''),''_<'',''_&lt;''),''&'','';#38'')  as entitlement_xml from SAQITE(nolock) where quote_id=''"+str(QUOTE_ID)+"'' AND LINE IN (SELECT EQUIPMENT_IDD FROM "+str(CRMTMP)+")  )A )a SELECT @XML = CONVERT(XML,''<ROOT>''+@VAL+''</ROOT>'') exec sys.sp_xml_preparedocument @H output,@XML; INSERT "+str(SAQIEN)+" (QUOTE_ID,SERVICE_ID,LINE,ENTITLEMENT_NAME,ENTITLEMENT_VALUE_CODE)SELECT QUOTE_ID,SERVICE_ID,LINE,ENTITLEMENT_ID,name as ENTITLEMENT_VALUE_CODE FROM (select QUOTE_ID,SERVICE_ID,LINE,ENTITLEMENT_ID,ENTITLEMENT_VALUE_CODE from openxml(@H, ''ROOT/QUOTE_ITEM_ENTITLEMENT'', 0) with (QUOTE_ID VARCHAR(100) ''QUOTE_ID'',LINE VARCHAR(100) ''LINE'',SERVICE_ID VARCHAR(100) ''SERVICE_ID'',ENTITLEMENT_VALUE_CODE VARCHAR(100) ''ENTITLEMENT_VALUE_CODE'',ENTITLEMENT_ID VARCHAR(100) ''ENTITLEMENT_ID''))A CROSS apply SplitString (ENTITLEMENT_VALUE_CODE) ; exec sys.sp_xml_removedocument @H; '")
				
				Quoteitemquer = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE B SET ET_XML= final_xml FROM (SELECT A.LINE, ISNULL(REPLACE(REPLACE(STUFF((SELECT '' ''+ JSON FROM (SELECT ''<QUOTE_ITEM_ENTITLEMENT>''+''<ITEM_LINE_ID>''+ISNULL(CONVERT(VARCHAR(100),A.LINE),'''')+''</ITEM_LINE_ID>''+''<SERVICE_ID>''+ISNULL(A.SERVICE_ID,'''')+''</SERVICE_ID>''+''<ENTITLEMENT_NAME>''+ISNULL(A.ENTITLEMENT_NAME,'''')+''</ENTITLEMENT_NAME>''+''<ENTITLEMENT_VALUE>''+ISNULL(CONVERT(VARCHAR(100),A.ENTITLEMENT_VALUE_CODE),'''')+''</ENTITLEMENT_VALUE>''+''</QUOTE_ITEM_ENTITLEMENT>'' AS JSON FROM ( 	SELECT B.LINE,B.SERVICE_ID,B.QUOTE_ID, B.ENTITLEMENT_NAME,B.ENTITLEMENT_VALUE_CODE FROM "+str(SAQIEN)+" B(NOLOCK) WHERE A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.LINE = B.LINE AND B.QUOTE_ID = ''"+str(QUOTE_ID)+"'' AND LINE IN (SELECT EQUIPMENT_IDD FROM "+str(CRMTMP)+") )A )A FOR XML PATH ('''')  ), 1, 1,'''' ),''&lt;'',''<''),''&gt;'',''>''),''<QUOTE_ITEM_ENTITLEMENT></QUOTE_ITEM_ENTITLEMENT>'') AS final_xml  FROM "+str(SAQITM)+" (NOLOCK) A WHERE A.QUOTE_ID = ''"+str(QUOTE_ID)+"''  AND LINE IN (SELECT EQUIPMENT_IDD FROM "+str(CRMTMP)+") )A JOIN "+str(SAQITM)+" B(NOLOCK) ON A.LINE = B.LINE '")
				
				CRMTMP11 = SqlHelper.GetFirst("sp_executesql @T=N'DELETE FROM "+str(CRMTMP)+" ' ")
						
			else:
				Check_flag2=0

		# QUOTE_HEADER QUERY
		Quoteheaderquery = SqlHelper.GetFirst("select replace(replace(STUFF((SELECT  ' '+final_xml FROM (SELECT '<QUOTE_HEADER>'+'<QUOTE_ID>"+str(CRMQT.c4c_quote_id)+"</QUOTE_ID>'+'<QTEREV_ID>'+ISNULL(CONVERT(VARCHAR,SAQTRV.QTEREV_ID),'')+'</QTEREV_ID>'+'<CREATE>'+ISNULL('C','')+'</CREATE>'+'<REVISION_DESCRIPTION>'+ISNULL(SAQTRV.REVISION_DESCRIPTION,'')+'</REVISION_DESCRIPTION>'+'<DOCTYP_ID>'+ISNULL(SAQTRV.DOCTYP_ID,'')+'</DOCTYP_ID>'+'<CONTRACT_VALID_FROM>'+REPLACE(ISNULL(convert(varchar(11),SAQTRV.CONTRACT_VALID_FROM,121),''),'-','')+'</CONTRACT_VALID_FROM>'+'<CONTRACT_VALID_TO>'+REPLACE(ISNULL(convert(varchar(11),SAQTRV.CONTRACT_VALID_TO,121),''),'-','')+'</CONTRACT_VALID_TO>'+'<DOC_CURRENCY>'+ISNULL(SAQTRV.DOC_CURRENCY,'')+'</DOC_CURRENCY>'+'<SALESORG_ID>'+ISNULL(SAQTRV.SALESORG_ID,'')+'</SALESORG_ID>'+'<DISTRIBUTIONCHANNEL_ID>'+ISNULL(SAQTRV.DISTRIBUTIONCHANNEL_ID,'')+'</DISTRIBUTIONCHANNEL_ID>'+'<DIVISION_ID>'+ISNULL(SAQTRV.DIVISION_ID,'')+'</DIVISION_ID>'+'<SALESOFFICE_ID>'+ISNULL(SAQTRV.SALESOFFICE_ID,'')+'</SALESOFFICE_ID>'+'<INCOTERM_ID>'+ISNULL(SAQTRV.INCOTERM_ID,'')+'</INCOTERM_ID>'+'<INCOTERM_NAME>'+ISNULL(SAQTRV.INCOTERM_NAME,'')+'</INCOTERM_NAME>'+'<PAYMENTTERM_ID>'+ISNULL(SAQTRV.PAYMENTTERM_ID,'')+'</PAYMENTTERM_ID>'+'<OPPORTUNITY_ID>"+str(SAOPPR.OPPORTUNITY_ID)+"</OPPORTUNITY_ID>'+'<OPPORTUNITY_NAME>"+str(SAOPPR.OPPORTUNITY_NAME)+"</OPPORTUNITY_NAME>'+'<PRICING_DATE>'+REPLACE(ISNULL(convert(varchar(11),CONVERT(DATE,SAQTRV.EXCHANGE_RATE_DATE),121),''),'-','')+'</PRICING_DATE>'+'<EXCHANGE_RATE>'+ISNULL(convert(varchar,SAQTRV.EXCHANGE_RATE),'1')+'</EXCHANGE_RATE><CONTRACT_ID>'+ISNULL(CRM_CONTRACT_ID,'')+'</CONTRACT_ID><RELEASE_SCHEDULE>'+ISNULL(NULL,'')+'</RELEASE_SCHEDULE>' AS final_xml  FROM SAQTMT(NOLOCK)  JOIN SAQTRV (NOLOCK) ON SAQTMT.QUOTE_ID = SAQTRV.QUOTE_ID WHERE SAQTMT.QUOTE_ID = '"+str(QUOTE_ID)+"' AND SAQTRV.QTEREV_ID = '"+str(REVISION_ID)+"' )A FOR XML PATH ('')  ), 1, 1, ''),'&lt;','<'),'&gt;','>')AS RESULT")
		
		if str(Quoteheaderquery.RESULT) != "" :
			Quoteheaderquery = str(Quoteheaderquery.RESULT)
		else:
			Quoteheaderquery = "<QUOTE_HEADER>"
		
		# QUOTE_INVOLVED_PARTY QUERY
		QuoteInvolvedPartiesquery = SqlHelper.GetFirst("select replace(replace(STUFF((SELECT  ' '+final_xml FROM (SELECT DISTINCT  '<QUOTE_INVOLVED_PARTY>'+'<QUOTE_ID>"+str(CRMQT.c4c_quote_id)+"</QUOTE_ID><SOLD_TO>'+ ISNULL((SELECT REPLACE(ACCOUNT_ID,'STP-','') FROM SAQTMT(NOLOCK) WHERE QUOTE_ID = '"+str(QUOTE_ID)+"' ),'') + '</SOLD_TO><BILL_TO>'+ISNULL((SELECT TOP 1 PARTY_ID FROM SAQTIP(NOLOCK) WHERE QUOTE_ID = '"+str(QUOTE_ID)+"' AND PARTY_ROLE = 'BILL TO' AND QTEREV_ID = '"+str(REVISION_ID)+"' ),'')+'</BILL_TO><SHIP_TO>'+ISNULL((SELECT TOP 1 PARTY_ID FROM SAQTIP(NOLOCK) WHERE QUOTE_ID = '"+str(QUOTE_ID)+"' AND PARTY_ROLE = 'SHIP TO' AND QTEREV_ID = '"+str(REVISION_ID)+"' ),'')+'</SHIP_TO><PAYER>'+ISNULL((SELECT TOP 1 PARTY_ID FROM SAQTIP(NOLOCK) WHERE QUOTE_ID = '"+str(QUOTE_ID)+"' AND QTEREV_ID = '"+str(REVISION_ID)+"' AND PARTY_ROLE = 'PAYER' ),'')+'</PAYER><GPMRPM>'+ISNULL((SELECT TOP 1 CONVERT(VARCHAR(10),CRM_EMPLOYEE_ID) FROM SAQDLT(NOLOCK)A JOIN SAEMPL (NOLOCK) ON MEMBER_ID = EMPLOYEE_ID WHERE QUOTE_ID = '"+str(QUOTE_ID)+"' AND C4C_PARTNERFUNCTION_ID = 'BD MANAGER' AND QTEREV_ID = '"+str(REVISION_ID)+"' ),'')+'</GPMRPM><CONT_MNGR>'+ISNULL((SELECT TOP 1 CONVERT(VARCHAR(10),CRM_EMPLOYEE_ID) FROM SAQDLT(NOLOCK)A JOIN SAEMPL (NOLOCK) ON MEMBER_ID = EMPLOYEE_ID WHERE QUOTE_ID = '"+str(QUOTE_ID)+"' AND C4C_PARTNERFUNCTION_ID = 'CONTRACT MANAGER' AND QTEREV_ID = '"+str(REVISION_ID)+"' ),'')+'</CONT_MNGR><SALES_PERSON>'+ISNULL((SELECT TOP 1 CONVERT(VARCHAR(10),CRM_EMPLOYEE_ID) FROM SAQDLT(NOLOCK)A JOIN SAEMPL (NOLOCK) ON MEMBER_ID = EMPLOYEE_ID WHERE QUOTE_ID = '"+str(QUOTE_ID)+"' AND PARTNERFUNCTION_ID = 'ER' AND QTEREV_ID = '"+str(REVISION_ID)+"' ),'')+'</SALES_PERSON>' AS final_xml  FROM SAQTIP(NOLOCK) WHERE QUOTE_ID = '"+str(QUOTE_ID)+"' AND QTEREV_ID = '"+str(REVISION_ID)+"')A FOR XML PATH ('')  ), 1, 1, ''),'&lt;','<'),'&gt;','>')AS RESULT")
		
		if str(QuoteInvolvedPartiesquery.RESULT) != "" :
			QuoteInvolvedPartiesquery = str(QuoteInvolvedPartiesquery.RESULT)
			
			QuoteInvolvedPartiesfabquery = SqlHelper.GetFirst("select replace(replace(STUFF((SELECT  ' '+final_xml FROM (SELECT  DISTINCT '<FAB>'+CASE WHEN ISNULl(CRM_FABLOCATION_ID,'')<>'' THEN CRM_FABLOCATION_ID ELSE ISNULL(SAQFBL.FABLOCATION_ID,'') END+'</FAB>' AS final_xml  FROM SAQICO SAQFBL(NOLOCK) JOIN MAFBLC (NOLOCK) ON SAQFBL.FABLOCATION_ID = MAFBLC.FAB_LOCATION_ID WHERE QUOTE_ID  = '"+str(QUOTE_ID)+"' AND QTEREV_ID = '"+str(REVISION_ID)+"')SUB_SAQFBL FOR XML PATH ('')  ), 1, 1, ''),'&lt;','<'),'&gt;','>')AS RESULT")
			
			QuoteInvolvedPartiescontactquery = SqlHelper.GetFirst("select replace(replace(STUFF((SELECT  ' '+final_xml FROM (SELECT  DISTINCT '<EMAIL'+CONVERT(VARCHAR,ROW_NUMBER()OVER(ORDER BY CPQTABLEENTRYID))+'>'+ISNULL(SAQICT.CONTACT_ID,'') +'</EMAIL'+CONVERT(VARCHAR,ROW_NUMBER()OVER(ORDER BY CPQTABLEENTRYID))+'>' AS final_xml  FROM SAQICT (NOLOCK) WHERE QUOTE_ID  = '"+str(QUOTE_ID)+"' AND QTEREV_ID = '"+str(REVISION_ID)+"' AND ISNULL(SHIP_NOTIFY_EMAIL,'FALSE')='TRUE' )SAQICT FOR XML PATH ('')  ), 1, 1, ''),'&lt;','<'),'&gt;','>')AS RESULT")
			
			if str(QuoteInvolvedPartiesfabquery.RESULT) != "" :
			
				QuoteInvolvedPartiesquery = QuoteInvolvedPartiesquery+str(QuoteInvolvedPartiesfabquery.RESULT)
			else:
				QuoteInvolvedPartiesquery = QuoteInvolvedPartiesquery+'<FAB></FAB>'
			
			if str(QuoteInvolvedPartiescontactquery.RESULT) != "" :
			
				QuoteInvolvedPartiesquery = QuoteInvolvedPartiesquery+str(QuoteInvolvedPartiescontactquery.RESULT)+'</QUOTE_INVOLVED_PARTY>'
			else:
				QuoteInvolvedPartiesquery = QuoteInvolvedPartiesquery+'<CUST_CONTACT></CUST_CONTACT></QUOTE_INVOLVED_PARTY>'
			
		else:
			QuoteInvolvedPartiesquery = "<QUOTE_INVOLVED_PARTY></QUOTE_INVOLVED_PARTY>"
		
		start1 = 1
		end1 = 500

		Check_flag1 = 1
		while Check_flag1 == 1:
		
			table1 = SqlHelper.GetFirst(
				"SELECT DISTINCT LINE FROM (select distinct LINE, ROW_NUMBER()OVER(ORDER BY LINE) AS SNO FROM(SELECT DISTINCT LINE FROM "+str(SAQITM)+"  (NOLOCK) where quote_id='"+str(QUOTE_ID)+"' ) A )A WHERE SNO>= "+str(start1)+" AND SNO<="+str(end1)+""
			)
			
			CRMTMP2 = SqlHelper.GetFirst("sp_executesql @T=N'IF NOT EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(CRMTMP)+"'' ) BEGIN CREATE TABLE "+str(CRMTMP)+" (EQUIPMENT_IDD VARCHAR(100)) END  ' ")
			
			table3 = SqlHelper.GetFirst(
				"sp_executesql @T=N'INSERT "+str(CRMTMP)+" SELECT DISTINCT LINE FROM (SELECT DISTINCT LINE, ROW_NUMBER()OVER(ORDER BY LINE) AS SNO FROM(SELECT DISTINCT LINE FROM "+str(SAQITM)+"  (NOLOCK) where quote_id=''"+str(QUOTE_ID)+"'' ) A )A WHERE SNO>= "+str(start1)+" AND SNO<="+str(end1)+"  '")
			
			start1 = start1 + 500
			end1 = end1 + 500

			if str(table1) != "None":
		
				if str(QTYPE.quote_type) == "ZWK1":
					
					Quoteitemquery = SqlHelper.GetFirst("SELECT REPLACE((select replace(replace(STUFF((SELECT  ' '+final_xml FROM ( SELECT '<QUOTE_ITEM>'+'<LINE>'+ISNULL(convert(varchar(100),SAQITM.LINE),'')+'</LINE>'+'<SERVICE_ID>'+SAQITM.SERVICE_ID+'</SERVICE_ID>'+'<NET_VALUE>'+ISNULL(convert(varchar,SAQITM.NET_VALUE),'')+'</NET_VALUE>'+'<PLANT_ID>'+ISNULL(convert(varchar,SAQITM.PLANT_ID),'')+'</PLANT_ID>'+'<CONTRACT_VALID_FROM>'+REPLACE(ISNULL(convert(varchar(11),SAQITM.LINE_ITEM_FROM_DATE,121),''),'-','')+'</CONTRACT_VALID_FROM>'+'<CONTRACT_VALID_TO>'+REPLACE(ISNULL(convert(varchar(11),SAQITM.LINE_ITEM_TO_DATE,121),''),'-','')+'</CONTRACT_VALID_TO>'+ ISNULL(ET_XML,'<QUOTE_ITEM_ENTITLEMENT></QUOTE_ITEM_ENTITLEMENT>')+ISNULL(REPLACE(REPLACE(STUFF((SELECT ' '+ JSON FROM (SELECT '<QUOTE_ITEM_PARTS>'+'<LINE>'+ISNULL(convert(varchar(100),SUB_SAQITM.LINE),'')+'</LINE>'+'<CUSTOMER_PART_NUMBER>'+ISNULL(CUSTOMER_PART_NUMBER,'')+'</CUSTOMER_PART_NUMBER>'+'<PART_NUMBER>'+ISNULL(PART_NUMBER,'')+'</PART_NUMBER>'+'<SCHEDULE_MODE>'+ISNULL(SCHEDULE_MODE,'')+'</SCHEDULE_MODE>'+'<DELIVERY_MODE>'+ISNULL(DELIVERY_MODE,'')+'</DELIVERY_MODE>' +'<CUSTOMER_ANNUAL_QUANTITY>'+ISNULL(convert(varchar,ANNUAL_QUANTITY),'')+'</CUSTOMER_ANNUAL_QUANTITY>'+'<UNIT_PRICE>'+ISNULL(convert(varchar,UNIT_PRICE),'')+'</UNIT_PRICE>'+'<CORE_CREDIT_PRICE>'+ISNULL(convert(varchar,CORE_CREDIT_PRICE),'')+'</CORE_CREDIT_PRICE>'+'<EXCHANGE_ELIGIBLE>'+ISNULL(convert(varchar,EXCHANGE_ELIGIBLE),'')+'</EXCHANGE_ELIGIBLE>'+'<CUSTOMER_PARTICIPATE>'+ISNULL(convert(varchar,CUSTOMER_PARTICIPATE),'')+'</CUSTOMER_PARTICIPATE>'+'<CUSTOMER_ACCEPT_PART>'+ISNULL(convert(varchar,CUSTOMER_ACCEPT_PART),'')+'</CUSTOMER_ACCEPT_PART>'+'<ODCC_FLAG>'+ISNULL(convert(varchar,ODCC_FLAG),'')+'</ODCC_FLAG>'+'</QUOTE_ITEM_PARTS>' AS JSON FROM (SELECT ISNULL(convert(varchar(100),SAQITM.LINE),'') AS LINE,PART_NUMBER,ANNUAL_QUANTITY,CASE WHEN DELIVERY_MODE='ONSITE' THEN '1' WHEN DELIVERY_MODE='OFFSITE' THEN '2' ELSE DELIVERY_MODE END AS DELIVERY_MODE, CASE WHEN SCHEDULE_MODE='SCHEDULED' THEN '1' WHEN SCHEDULE_MODE='UNSCHEDULED' THEN '2' WHEN SCHEDULE_MODE='TLS SHARED' THEN '3' WHEN SCHEDULE_MODE='TLS NON-SHARED' THEN '4' WHEN SCHEDULE_MODE='LOW QTY ONSITE' THEN '5' WHEN SCHEDULE_MODE='ON REQUEST' THEN '6' ELSE SCHEDULE_MODE END AS SCHEDULE_MODE ,EXCHANGE_ELIGIBLE,CUSTOMER_PARTICIPATE,CUSTOMER_ACCEPT_PART,SAQIFP.UNIT_PRICE,CORE_CREDIT_PRICE,CUSTOMER_PART_NUMBER,ODCC_FLAG FROM SAQRIT(NOLOCK) JOIN SAQIFP (NOLOCK) ON SAQRIT.QUOTE_ID = SAQIFP.QUOTE_ID AND SAQRIT.LINE = SAQIFP.LINE AND SAQRIT.QTEREV_ID = SAQIFP.QTEREV_ID  WHERE SAQRIT.QUOTE_ID = '"+str(QUOTE_ID)+"' AND SAQRIT.QTEREV_ID = '"+str(REVISION_ID)+"' AND SAQITM.QUOTE_ID  = SAQRIT.QUOTE_ID AND SAQITM.LINE = SAQRIT.LINE )SUB_SAQITM )A FOR XML PATH ('')  ), 1, 1,'' ),'&lt;','<'),'&gt;','>'),'<QUOTE_ITEM_FPM></QUOTE_ITEM_FPM>')+'</QUOTE_ITEM>' AS final_xml  FROM "+str(SAQITM)+" SAQITM(NOLOCK) WHERE SAQITM.QUOTE_ID = '"+str(QUOTE_ID)+"' )A FOR XML PATH ('')  ), 1, 1, ''),'&lt;','<'),'&gt;','>')AS RESULT),'','' ) AS A ")

				if str(Quoteitemquery.A) == '':
					Quoteiteminfo = '<QUOTE_ITEM><QUOTE_ITEM_PARTS></QUOTE_ITEM_PARTS><QUOTE_ITEM_ENTITLEMENT></QUOTE_ITEM_ENTITLEMENT></QUOTE_ITEM>'
				else:
					Quoteiteminfo = str(Quoteitemquery.A)
			
				str_xml = str(Quoteiteminfo)
				data = data+str_xml
				CRMTMP1 = SqlHelper.GetFirst("sp_executesql @T=N'DELETE FROM "+str(CRMTMP)+" ' ")
			else:
				Check_flag1=0
		
	
	data = str(Quoteheaderquery)+str(data)+str(QuoteInvolvedPartiesquery)+'</QUOTE_HEADER>'			

	Final_xml = "<QUOTE>"+str(data)+"</QUOTE>"

	Parameter = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'SELECT' ")
		
	primaryQueryItems = SqlHelper.GetFirst( ""+ str(Parameter.QUERY_CRITERIA_1)+ " SYINPL (INTEGRATION_PAYLOAD,INTEGRATION_KEY,CpqTableEntryDateModified,INTEGRATION_NAME)  select ''"+str(Final_xml)+ "'',''"+ str(QUOTE_ID)+ "'',getdate(),''CPQ to ECC Quote Replication'' ' ")

	SAQICO_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQICO)+"'' ) BEGIN DROP TABLE "+str(SAQICO)+" END  ' ")
	SAQIBP_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQIBP)+"'' ) BEGIN DROP TABLE "+str(SAQIBP)+" END  ' ")
	SAQIEN_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQIEN)+"'' ) BEGIN DROP TABLE "+str(SAQIEN)+" END  ' ")
	SAQSAP_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQSAP)+"'' ) BEGIN DROP TABLE "+str(SAQSAP)+" END  ' ")
	SAQTSE_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQTSE)+"'' ) BEGIN DROP TABLE "+str(SAQTSE)+" END  ' ")
	SAQITM_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQITM)+"'' ) BEGIN DROP TABLE "+str(SAQITM)+" END  ' ")
	CRMTMP_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(CRMTMP)+"'' ) BEGIN DROP TABLE "+str(CRMTMP)+" END  ' ")
	
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
		

	Log.Info("QTPOSTQECC ERROR---->:" + str(sys.exc_info()[1]))
	Log.Info("QTPOSTQECC ERROR LINE NO---->:" + str(sys.exc_info()[-1].tb_lineno))
	ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "400", "Message": str(sys.exc_info()[1])}]})
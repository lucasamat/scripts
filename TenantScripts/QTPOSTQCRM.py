# =========================================================================================================================================
#   __script_name : QTPOSTQCRM.PY
#   __script_description : THIS SCRIPT IS USED TO SEND QUOTE INFROMATION FROM CPQ TO CRM
#   __primary_author__ : SURESH MUNIYANDI,BAJI
#   __create_date :
#   Ã‚Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
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
        
        QTYPE = SqlHelper.GetFirst("select left(quote_type,4) as quote_type from SAQTMT(nolock) WHERE QUOTE_ID = '"+str(QUOTE_ID)+"' ")
        
        SAOPPR = SqlHelper.GetFirst("select convert(varchar(100),OPPORTUNITY_ID) as OPPORTUNITY_ID,OPPORTUNITY_NAME from SAOPQT(nolock) WHERE QUOTE_ID = '"+str(QUOTE_ID)+"'  ")
        
        SAQICO = "SAQICO_BKP_"+str(CRMQT.c4c_quote_id)
        SAQIBP = "SAQIBP_BKP_"+str(CRMQT.c4c_quote_id)
        SAQIEN = "SAQIEN_BKP_"+str(CRMQT.c4c_quote_id)
        SAQSAP = "SAQSAP_BKP_"+str(CRMQT.c4c_quote_id)
        SAQTSE = "SAQTSE_BKP_"+str(CRMQT.c4c_quote_id)
        SAQITM = "SAQITM_BKP_"+str(CRMQT.c4c_quote_id)
        CRMTMP = "CRMTMP_BKP_"+str(CRMQT.c4c_quote_id)
        SAQITE = "SAQITE_BKP_"+str(CRMQT.c4c_quote_id)

        SAQICO_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQICO)+"'' ) BEGIN DROP TABLE "+str(SAQICO)+" END  ' ")
        SAQIBP_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQIBP)+"'' ) BEGIN DROP TABLE "+str(SAQIBP)+" END  ' ")
        SAQIEN_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQIEN)+"'' ) BEGIN DROP TABLE "+str(SAQIEN)+" END  ' ")
        SAQSAP_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQSAP)+"'' ) BEGIN DROP TABLE "+str(SAQSAP)+" END  ' ")
        SAQTSE_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQTSE)+"'' ) BEGIN DROP TABLE "+str(SAQTSE)+" END  ' ")
        SAQITM_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQITM)+"'' ) BEGIN DROP TABLE "+str(SAQITM)+" END  ' ")
        CRMTMP_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(CRMTMP)+"'' ) BEGIN DROP TABLE "+str(CRMTMP)+" END  ' ")
        SAQITE_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQITE)+"'' ) BEGIN DROP TABLE "+str(SAQITE)+" END  ' ")

        SAQITM_DRP = SqlHelper.GetFirst("sp_executesql @T=N'select distinct SAQRIT.QUOTE_ID,SAQRIT.SERVICE_ID,SAQRIT.LINE,SAQRIT.QUANTITY,MAMTRL.UNIT_OF_MEASURE AS UOM_ID,SAQRIT.NET_PRICE AS EXTENDED_PRICE,'''' AS ITEM_TYPE,'''' AS PO_NUMBER,'''' AS PO_ITEM,'''' AS PO_NOTES,SAQRIT.PLANT_ID,SAQRIT.CONTRACT_VALID_FROM AS LINE_ITEM_FROM_DATE,SAQRIT.CONTRACT_VALID_TO AS LINE_ITEM_TO_DATE,'''' AS INTERNAL_NOTES,SAQRIT.STATUS,SAQRIT.SERVICE_RECORD_ID,SAQRIT.TAXCLASSIFICATION_ID AS SRVTAXCLA_ID,CONVERT(NVARCHAR(MAX),'''') AS BP_XML,CONVERT(NVARCHAR(MAX),'''') AS ET_XML,ISNULL(GL_ACCOUNT_NO,'''') AS GL_ACCOUNT_NO,ISNULL(REF_SALESORDER,'''') AS REF_SALESORDER_NO,SAQRIT.LINE AS NEW_LINE,CASE WHEN ISNULL(PM_ID,'''')='''' THEN MNTEVT_LEVEL ELSE PM_ID END AS PM_ID,MNTEVT_LEVEL,CONVERT(VARCHAR,PEREVTPRC_INDT_CURR) AS PEREVTPRC_INDT_CURR,NULL AS TARGET_QTY,ISNULL(SAQRIT.DIVISION_ID,'''') AS DIVISION_ID,ISNULL(POSS_NSO_PART_ID,'''') AS NSO_PART INTO "+str(SAQITM)+" FROM SAQRIT (NOLOCK) JOIN MAMTRL (NOLOCK) ON SAQRIT.SERVICE_ID = MAMTRL.SAP_PART_NUMBER WHERE SAQRIT.QUOTE_ID = ''"+str(QUOTE_ID)+"'' AND SAQRIT.QTEREV_ID = ''"+str(REVISION_ID)+"'' AND SAQRIT.LINE NOT IN (SELECT DISTINCT LINE FROM SAQRIO(NOLOCK) WHERE SAQRIO.QUOTE_ID = ''"+str(QUOTE_ID)+"'' AND SAQRIO.QTEREV_ID = ''"+str(REVISION_ID)+"'' AND ISNULL(TEMP_TOOL,''FALSE'')=''TRUE'' ) ' ")
        
        #Target Qty
        SAQITM_DRP = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET TARGET_QTY= A.QUANTITY,QUANTITY=0  FROM "+str(SAQITM)+" A JOIN SAQICO(NOLOCK) B ON A.QUOTE_ID = B.QUOTE_ID AND A.LINE = B.LINE WHERE B.QUOTE_ID = ''"+str(QUOTE_ID)+"'' AND B.QTEREV_ID = ''"+str(REVISION_ID)+"'' AND B.BILTYP=''Variable'' ' ")
        
        #Z0117 Positive
        SAQITM_DRP = SqlHelper.GetFirst("sp_executesql @T=N'INSERT "+str(SAQITM)+" (QUOTE_ID,SERVICE_ID,LINE,QUANTITY,UOM_ID,EXTENDED_PRICE,PLANT_ID, LINE_ITEM_FROM_DATE,LINE_ITEM_TO_DATE,STATUS,SERVICE_RECORD_ID,SRVTAXCLA_ID,NEW_LINE,ITEM_TYPE,PO_NUMBER,PO_ITEM,PO_NOTES,INTERNAL_NOTES,BP_XML,ET_XML,GL_ACCOUNT_NO,REF_SALESORDER_NO,NSO_PART,DIVISION_ID) SELECT DISTINCT QUOTE_ID,SERVICE_ID,LINE,QUANTITY,UOM_ID,EXTENDED_PRICE * -1,PLANT_ID, LINE_ITEM_FROM_DATE,LINE_ITEM_TO_DATE,STATUS,SERVICE_RECORD_ID,SRVTAXCLA_ID,(select max(line) from "+str(SAQITM)+")+row_number() over(order by line) AS NEW_LINE,'''','''','''','''','''','''','''','''','''','''',''''  FROM "+str(SAQITM)+" (NOLOCK) WHERE  SERVICE_ID = ''Z0117'' ' ")

        SAQITM_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQIEN)+"'' ) BEGIN DROP TABLE "+str(SAQIBP)+" END CREATE TABLE "+str(SAQIEN)+" (QUOTE_ID VARCHAR(100),SERVICE_ID VARCHAR(100),LINE VARCHAR(100),ENTITLEMENT_NAME VARCHAR(100),ENTITLEMENT_VALUE_CODE VARCHAR(100))' ")

        SAQICO_BKP = SqlHelper.GetFirst("sp_executesql @T=N'select QUOTE_ID,SERVICE_ID,LINE,EQUIPMENT_ID,SERIAL_NUMBER,NULL AS EXTENDED_PRICE,NULL AS SRVTAXCLA_ID,CONVERT(VARCHAR(100),NULL) AS PAR_SERVICE_ID,QTEREV_ID INTO "+str(SAQICO)+" from SAQRIO(NOLOCK) WHERE QUOTE_ID = ''"+str(QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(REVISION_ID)+"'' AND ISNULL(ASSEMBLY_ID,'''')='''' UNION select QUOTE_ID,SERVICE_ID,LINE,ASSEMBLY_ID,NULL AS SERIAL_NUMBER,NULL AS EXTENDED_PRICE,NULL AS SRVTAXCLA_ID,CONVERT(VARCHAR(100),NULL) AS PAR_SERVICE_ID,QTEREV_ID from SAQRIO(NOLOCK) WHERE QUOTE_ID = ''"+str(QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(REVISION_ID)+"'' AND ISNULL(ASSEMBLY_ID,'''')<>'''' ' ")
        
        #SAQIBP_BKP = SqlHelper.GetFirst("sp_executesql @T=N'select QUOTE_ID,MAMTRL.SAP_PART_NUMBER AS SERVICE_ID,LINE ,REPLACE(CONVERT(VARCHAR(11),BILLING_DATE,121),''-'','''') AS BILLING_DATE,BILLING_VALUE AS BILLING_AMOUNT,EQUIPMENT_ID,ESTVAL_INDT_CURR  INTO "+str(SAQIBP)+" from SAQIBP(NOLOCK)  JOIN MAMTRL (NOLOCK) ON SAQIBP.SERVICE_RECORD_ID = MAMTRL.MATERIAL_RECORD_ID WHERE QUOTE_ID = ''"+str(QUOTE_ID)+"''  AND QTEREV_ID = ''"+str(REVISION_ID)+"'' ' ")

        SAQSAP_BKP = SqlHelper.GetFirst("sp_executesql @T=N'select QUOTE_ID,SERVICE_ID,LINE,PART_NUMBER,PART_DESCRIPTION,ISNULL(NEW_PART,''FALSE'') AS NEW_PART,QUANTITY INTO "+str(SAQSAP)+" from SAQRIP(NOLOCK) WHERE QUOTE_ID = ''"+str(QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(REVISION_ID)+"''  ' ")

        SAQTSE_BKP = SqlHelper.GetFirst("sp_executesql @T=N'select LINE,QUOTE_ID,MAMTRL.SAP_PART_NUMBER AS SERVICE_ID,CONVERT(VARCHAR(MAX),'''') AS ET_XML INTO "+str(SAQTSE)+" from SAQRIT(NOLOCK) JOIN MAMTRL (NOLOCK) ON SAQRIT.SERVICE_RECORD_ID = MAMTRL.MATERIAL_RECORD_ID WHERE QUOTE_ID = ''"+str(QUOTE_ID)+"'' AND SAQRIT.QTEREV_ID = ''"+str(REVISION_ID)+"'' ' ")
        

        start23 = 1
        end23 = 500

        Check_flag23 = 1
        while Check_flag23 == 1:

            table23 = SqlHelper.GetFirst(
                "SELECT DISTINCT LINE FROM (SELECT DISTINCT LINE, ROW_NUMBER()OVER(ORDER BY LINE) AS SNO FROM(SELECT DISTINCT LINE FROM "+str(SAQITM)+"  (NOLOCK) where quote_id='"+str(QUOTE_ID)+"' ) A )A WHERE SNO>= "+str(start23)+" AND SNO<="+str(end23)+""
            )
                    
            CRMTMP23 = SqlHelper.GetFirst("sp_executesql @T=N'IF NOT EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(CRMTMP)+"'' ) BEGIN CREATE TABLE "+str(CRMTMP)+" (EQUIPMENT_IDD VARCHAR(100)) END  ' ")
            
            table213 = SqlHelper.GetFirst(
        "sp_executesql @T=N'INSERT "+str(CRMTMP)+" SELECT DISTINCT LINE FROM (SELECT DISTINCT LINE, ROW_NUMBER()OVER(ORDER BY LINE) AS SNO FROM(SELECT DISTINCT LINE FROM "+str(SAQITM)+"  (NOLOCK) where quote_id=''"+str(QUOTE_ID)+"'' ) A )A WHERE SNO>= "+str(start23)+" AND SNO<="+str(end23)+"  '")
        
            """SAQITE_BKP = SqlHelper.GetFirst("sp_executesql @T=N'update saqite set entitlement_xml = replace(ENTITLEMENT_XML,'''','';#39'')  from SAQITE(NOLOCK) WHERE QUOTE_ID =''"+str(QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(REVISION_ID)+"''  AND LINE>= "+str(start23)+" AND LINE<="+str(end23)+"  '")

            SAQITE_BKP = SqlHelper.GetFirst("sp_executesql @T=N'update saqite set entitlement_xml = replace(ENTITLEMENT_XML,''\n'','''')   from SAQITE(NOLOCK) WHERE QUOTE_ID =''"+str(QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(REVISION_ID)+"'' AND LINE>= "+str(start23)+" AND LINE<="+str(end23)+"  '")

            SAQITE_BKP = SqlHelper.GetFirst("sp_executesql @T=N'update saqite set entitlement_xml = replace(ENTITLEMENT_XML,''&'','''')  from SAQITE(NOLOCK) WHERE QUOTE_ID =''"+str(QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(REVISION_ID)+"'' AND LINE>= "+str(start23)+" AND LINE<="+str(end23)+"  '")

            SAQITE_BKP = SqlHelper.GetFirst("sp_executesql @T=N'update saqite set entitlement_xml = replace(ENTITLEMENT_XML,'' < '','' &lt; '' )  from SAQITE(NOLOCK) WHERE QUOTE_ID =''"+str(QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(REVISION_ID)+"'' AND LINE>= "+str(start23)+" AND LINE<="+str(end23)+"  '")

            SAQITE_BKP = SqlHelper.GetFirst("sp_executesql @T=N'update saqite set entitlement_xml = replace(ENTITLEMENT_XML,'' > '','' &gt; '' )  from SAQITE(NOLOCK) WHERE QUOTE_ID =''"+str(QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(REVISION_ID)+"'' AND LINE>= "+str(start23)+" AND LINE<="+str(end23)+"  '")

            SAQITE_BKP = SqlHelper.GetFirst("sp_executesql @T=N'update saqite set entitlement_xml = replace(ENTITLEMENT_XML,''_>'',''_&gt;'')   from SAQITE(NOLOCK) WHERE QUOTE_ID =''"+str(QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(REVISION_ID)+"'' AND LINE>= "+str(start23)+" AND LINE<="+str(end23)+"  '")

            SAQITE_BKP = SqlHelper.GetFirst("sp_executesql @T=N'update saqite set entitlement_xml = replace(ENTITLEMENT_XML,''_<'',''_&lt;'')   from SAQITE(NOLOCK) WHERE QUOTE_ID =''"+str(QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(REVISION_ID)+"'' AND LINE>= "+str(start23)+" AND LINE<="+str(end23)+"  '")

            SAQITE_BKP = SqlHelper.GetFirst("sp_executesql @T=N'update saqite set entitlement_xml = replace(ENTITLEMENT_XML,'';#38'','''')   from SAQITE(NOLOCK) WHERE QUOTE_ID =''"+str(QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(REVISION_ID)+"'' AND LINE>= "+str(start23)+" AND LINE<="+str(end23)+"  '")

            SAQITE_BKP = SqlHelper.GetFirst("sp_executesql @T=N'update saqite set entitlement_xml = replace(ENTITLEMENT_XML,''>>'',''>'')   from SAQITE(NOLOCK) WHERE QUOTE_ID =''"+str(QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(REVISION_ID)+"'' AND LINE>= "+str(start23)+" AND LINE<="+str(end23)+"  '")

            SAQITE_BKP = SqlHelper.GetFirst("sp_executesql @T=N'update saqite set entitlement_xml = replace(ENTITLEMENT_XML,''<='','''')   from SAQITE(NOLOCK) WHERE QUOTE_ID =''"+str(QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(REVISION_ID)+"'' AND LINE>= "+str(start23)+" AND LINE<="+str(end23)+"  '") """

            
            start23 = start23 + 500
            end23 = end23 + 500

            if str(table23) != "None":
            
                SAQIBP_BKP = SqlHelper.GetFirst("sp_executesql @T=N'select QUOTE_ID,MAMTRL.SAP_PART_NUMBER AS SERVICE_ID,LINE ,REPLACE(CONVERT(VARCHAR(11),BILLING_DATE,121),''-'','''') AS BILLING_DATE,BILLING_VALUE AS BILLING_AMOUNT,EQUIPMENT_ID,ESTVAL_INDT_CURR  INTO "+str(SAQIBP)+" from SAQIBP(NOLOCK)  JOIN MAMTRL (NOLOCK) ON SAQIBP.SERVICE_RECORD_ID = MAMTRL.MATERIAL_RECORD_ID WHERE QUOTE_ID = ''"+str(QUOTE_ID)+"''  AND QTEREV_ID = ''"+str(REVISION_ID)+"'' AND LINE IN (SELECT EQUIPMENT_IDD FROM "+str(CRMTMP)+") ' ")
                    
                Quoteitemquer = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE B SET BP_XML= final_xml FROM (SELECT A.LINE, ISNULL(REPLACE(REPLACE(STUFF((SELECT '' ''+ JSON FROM (SELECT ''<QUOTE_ITEM_BILLING_PLAN>''+''<ITEM_LINE_ID>''+ISNULL(CONVERT(VARCHAR(100),A.LINE),'''')+''</ITEM_LINE_ID>''+''<SERVICE_ID>''+ISNULL(A.SERVICE_ID,'''')+''</SERVICE_ID>''+''<BILLING_START_DATE>''+ISNULL(A.BILLING_DATE,'''')+''</BILLING_START_DATE>''+''<BILLING_AMOUNT>''+ISNULL(CONVERT(VARCHAR(100),A.BILLING_AMOUNT),'''')+''</BILLING_AMOUNT>''+''<ESTVAL_INDT_CURR>''+ISNULL(CONVERT(VARCHAR(100),A.ESTVAL_INDT_CURR),'''')+''</ESTVAL_INDT_CURR>''+''</QUOTE_ITEM_BILLING_PLAN>'' AS JSON FROM ( 	SELECT LINE,B.SERVICE_ID,REPLACE(CONVERT(VARCHAR(11),BILLING_DATE,121),''-'','''') AS BILLING_DATE, SUM(BILLING_AMOUNT) AS BILLING_AMOUNT,SUM(ESTVAL_INDT_CURR) AS ESTVAL_INDT_CURR FROM "+str(SAQIBP)+" B(NOLOCK) WHERE A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.LINE = B.LINE AND B.QUOTE_ID = ''"+str(QUOTE_ID)+"'' AND B.LINE IN (SELECT EQUIPMENT_IDD FROM "+str(CRMTMP)+") GROUP BY B.LINE,B.SERVICE_ID,BILLING_DATE )A )A FOR XML PATH ('''')  ), 1, 1,'''' ),''&lt;'',''<''),''&gt;'',''>''),'''') AS final_xml  FROM "+str(SAQITM)+" (NOLOCK) A WHERE A.QUOTE_ID = ''"+str(QUOTE_ID)+"'' AND A.LINE IN (SELECT EQUIPMENT_IDD FROM "+str(CRMTMP)+") )A JOIN "+str(SAQITM)+" B(NOLOCK) ON A.LINE = B.LINE '")
                
                CRMTMP23 = SqlHelper.GetFirst("sp_executesql @T=N'DELETE FROM "+str(CRMTMP)+" ' ")
                
                SAQIBP_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQIBP)+"'' ) BEGIN DROP TABLE "+str(SAQIBP)+" END  ' ")
                        
            else:
                Check_flag23=0
                
        
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
                
                SAQITE_BKP = SqlHelper.GetFirst("sp_executesql @T=N'select * INTO "+str(SAQITE)+" from SAQITE(NOLOCK) WHERE QUOTE_ID = ''"+str(QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(REVISION_ID)+"'' AND LINE IN (SELECT EQUIPMENT_IDD FROM "+str(CRMTMP)+") ' ")
                
                
                SAQIEN_SEL = SqlHelper.GetFirst("sp_executesql @T=N'declare @H int; Declare @val Varchar(MAX);DECLARE @XML XML; SELECT @val = FINAL from(select  REPLACE(entitlement_xml,''<QUOTE_ITEM_ENTITLEMENT>'',sml) AS FINAL FROM (select ''<QUOTE_ITEM_ENTITLEMENT><QUOTE_ID>''+quote_id+''</QUOTE_ID><SERVICE_ID>''+service_id+''</SERVICE_ID><LINE>''+CONVERT(VARCHAR,LINE)+''</LINE>'' AS sml,REPLACE(replace(ENTITLEMENT_XML,'''','';#39''),''\n'','''')  as entitlement_xml from "+str(SAQITE)+" (nolock) where quote_id=''"+str(QUOTE_ID)+"'' AND QTEREV_ID = ''"+str(REVISION_ID)+"''   )A )a SELECT @XML = CONVERT(XML,''<ROOT>''+@VAL+''</ROOT>'') exec sys.sp_xml_preparedocument @H output,@XML; INSERT "+str(SAQIEN)+" (QUOTE_ID,SERVICE_ID,LINE,ENTITLEMENT_NAME,ENTITLEMENT_VALUE_CODE)SELECT QUOTE_ID,SERVICE_ID,LINE,ENTITLEMENT_ID,name as ENTITLEMENT_VALUE_CODE FROM (select QUOTE_ID,SERVICE_ID,LINE,ENTITLEMENT_ID,ENTITLEMENT_VALUE_CODE from openxml(@H, ''ROOT/QUOTE_ITEM_ENTITLEMENT'', 0) with (QUOTE_ID VARCHAR(100) ''QUOTE_ID'',LINE VARCHAR(100) ''LINE'',SERVICE_ID VARCHAR(100) ''SERVICE_ID'',ENTITLEMENT_VALUE_CODE VARCHAR(100) ''ENTITLEMENT_VALUE_CODE'',ENTITLEMENT_ID VARCHAR(100) ''ENTITLEMENT_ID''))A CROSS apply SplitString (ENTITLEMENT_VALUE_CODE) ; exec sys.sp_xml_removedocument @H; '")
                
                Quoteitemquer = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE B SET ET_XML= final_xml FROM (SELECT A.LINE, ISNULL(REPLACE(REPLACE(STUFF((SELECT '' ''+ JSON FROM (SELECT ''<QUOTE_ITEM_ENTITLEMENT>''+''<ITEM_LINE_ID>''+ISNULL(CONVERT(VARCHAR(100),A.LINE),'''')+''</ITEM_LINE_ID>''+''<SERVICE_ID>''+ISNULL(A.SERVICE_ID,'''')+''</SERVICE_ID>''+''<ENTITLEMENT_NAME>''+ISNULL(A.ENTITLEMENT_NAME,'''')+''</ENTITLEMENT_NAME>''+''<ENTITLEMENT_VALUE>''+ISNULL(CONVERT(VARCHAR(100),A.ENTITLEMENT_VALUE_CODE),'''')+''</ENTITLEMENT_VALUE>''+''</QUOTE_ITEM_ENTITLEMENT>'' AS JSON FROM ( 	SELECT B.LINE,B.SERVICE_ID,B.QUOTE_ID, B.ENTITLEMENT_NAME,B.ENTITLEMENT_VALUE_CODE FROM "+str(SAQIEN)+" B(NOLOCK) WHERE A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.LINE = B.LINE AND B.QUOTE_ID = ''"+str(QUOTE_ID)+"'' AND LINE IN (SELECT EQUIPMENT_IDD FROM "+str(CRMTMP)+") )A )A FOR XML PATH ('''')  ), 1, 1,'''' ),''&lt;'',''<''),''&gt;'',''>''),''<QUOTE_ITEM_ENTITLEMENT></QUOTE_ITEM_ENTITLEMENT>'') AS final_xml  FROM "+str(SAQITM)+" (NOLOCK) A WHERE A.QUOTE_ID = ''"+str(QUOTE_ID)+"''  AND LINE IN (SELECT EQUIPMENT_IDD FROM "+str(CRMTMP)+") )A JOIN "+str(SAQITM)+" B(NOLOCK) ON A.LINE = B.LINE '")
                
                CRMTMP11 = SqlHelper.GetFirst("sp_executesql @T=N'DELETE FROM "+str(CRMTMP)+" ' ")
                
                SAQITE_DRP1 = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQITE)+"'' ) BEGIN DROP TABLE "+str(SAQITE)+" END  ' ")
                        
            else:
                Check_flag2=0
        
        ET = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE  "+str(SAQITM)+"  SET ET_XML = REPLACE(ET_XML,''<ITEM_LINE_ID>''+ISNULL(CONVERT(VARCHAR(100),LINE),'''')+''</ITEM_LINE_ID>'',''<ITEM_LINE_ID>''+ISNULL(CONVERT(VARCHAR(100),NEW_LINE),'''')+''</ITEM_LINE_ID>'') WHERE LINE <> NEW_LINE ' ")
        
        BP = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE  "+str(SAQITM)+"  SET BP_XML = REPLACE(BP_XML,''<ITEM_LINE_ID>''+ISNULL(CONVERT(VARCHAR(100),LINE),'''')+''</ITEM_LINE_ID>'',''<ITEM_LINE_ID>''+ISNULL(CONVERT(VARCHAR(100),NEW_LINE),'''')+''</ITEM_LINE_ID>'') WHERE LINE <> NEW_LINE ' ")
        
        BP = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE  "+str(SAQITM)+"  SET BP_XML = REPLACE(BP_XML,''-'','''') WHERE LINE <> NEW_LINE ' ")
        
        Z0117_LINE = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE  "+str(SAQITM)+"  SET LINE = NEW_LINE WHERE LINE <> NEW_LINE ' ")
        
        #Z0017 Positive
        SAQICO_BKP = SqlHelper.GetFirst("sp_executesql @T=N'INSERT "+str(SAQICO)+" (QUOTE_ID,SERVICE_ID,LINE,EQUIPMENT_ID) SELECT a.* FROM (select A.QUOTE_ID,A.SERVICE_ID,B.LINE,A.EQUIPMENT_ID from SAQRIO(NOLOCK) A JOIN "+str(SAQITM)+" B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID WHERE A.QUOTE_ID = ''"+str(QUOTE_ID)+"'' AND A.QTEREV_ID = ''"+str(REVISION_ID)+"'' AND A.SERVICE_ID=''Z0117'')A LEFT JOIN "+str(SAQICO)+" B ON A.QUOTE_ID = B.QUOTE_ID AND A.LINE = B.LINE AND A.EQUIPMENT_ID = B.EQUIPMENT_ID WHERE B.EQUIPMENT_ID IS NULL ' ")

        # QUOTE_HEADER QUERY
        Quoteheaderquery = SqlHelper.GetFirst("select replace(replace(STUFF((SELECT  ' '+final_xml FROM (SELECT '<QUOTE_HEADER>'+'<QUOTE_ID>"+str(CRMQT.c4c_quote_id)+"</QUOTE_ID>'+'<QUOTE_NAME>'+ISNULL(SAQTRV.REVISION_DESCRIPTION,'')+'</QUOTE_NAME>'+'<QUOTE_TYPE>'+ISNULL(SAQTRV.DOCTYP_ID,'')+'</QUOTE_TYPE>'+'<SORG_CURRENCY>'+ISNULL(SAQTRV.DOC_CURRENCY,'')+'</SORG_CURRENCY>'+'<QUOTE_CURRENCY>'+ISNULL(SAQTMT.GLOBAL_CURRENCY,'')+'</QUOTE_CURRENCY>'+'<SALESORG_ID>'+ISNULL(SAQTRV.SALESORG_ID,'')+'</SALESORG_ID>'+'<DISTRIBUTIONCHANNEL_ID>'+ISNULL(SAQTRV.DISTRIBUTIONCHANNEL_ID,'')+'</DISTRIBUTIONCHANNEL_ID>'+'<DIVISION_ID>'+ISNULL(SAQTRV.DIVISION_ID,'')+'</DIVISION_ID>'+'<SALESOFFICE_ID>'+ISNULL(SAQTRV.SALESOFFICE_ID,'')+'</SALESOFFICE_ID>'+'<QTEREV_ID>'+ISNULL(CONVERT(VARCHAR,SAQTRV.QTEREV_ID),'')+'</QTEREV_ID>'+'<CONTRACT_VALID_FROM>'+REPLACE(ISNULL(convert(varchar(11),SAQTRV.CONTRACT_VALID_FROM,121),''),'-','')+'</CONTRACT_VALID_FROM>'+'<CONTRACT_VALID_TO>'+REPLACE(ISNULL(convert(varchar(11),SAQTRV.CONTRACT_VALID_TO,121),''),'-','')+'</CONTRACT_VALID_TO>'+'<PO_NUMBER>'+ISNULL(NULL,'')+'</PO_NUMBER>'+'<PO_DATE>'+ISNULL(NULL,'')+'</PO_DATE>'+'<PO_NOTES>'+ISNULL(NULL,'')+'</PO_NOTES>'+'<INCOTERMS>'+ISNULl(INCOTERM_ID,'')+'</INCOTERMS>'+'<INCOTERMS_NOTES>'+CASE WHEN ISNULL(SAQTRV.INCOTERM_LOCATION,'') = '' THEN ISNULL(INCOTERM_NAME,'') ELSE ISNULL(INCOTERM_LOCATION,'') END+'</INCOTERMS_NOTES>'+'<PAYMENTTERM_ID>'+ISNULL(SAQTRV.PAYMENTTERM_ID,'')+'</PAYMENTTERM_ID>'+'<NET_VALUE></NET_VALUE>'+'<OPPORTUNITY_ID>"+str(SAOPPR.OPPORTUNITY_ID)+"</OPPORTUNITY_ID>'+'<OPPORTUNITY_NAME>"+str(SAOPPR.OPPORTUNITY_NAME)+"</OPPORTUNITY_NAME>'+'<QUOTE_STATUS>'+ISNULL(REVISION_STATUS,'')+'</QUOTE_STATUS>'+'<PRICING_DATE>'+REPLACE(ISNULL(convert(varchar(11),CONVERT(DATE,SAQTRV.EXCHANGE_RATE_DATE),121),''),'-','')+'</PRICING_DATE>'+'<EXCH_DATE>'+REPLACE(ISNULL(convert(varchar(11),CONVERT(DATE,SAQTRV.EXCHANGE_RATE_DATE),121),''),'-','')+'</EXCH_DATE>'+'<EXCHANGE_RATE>'+ISNULL(convert(varchar,SAQTRV.EXCHANGE_RATE),'1')+'</EXCHANGE_RATE>'+'<EXCHANGE_RATE_TYPE>'+ISNULL(EXCHANGE_RATE_TYPE,'')+'</EXCHANGE_RATE_TYPE>'+'<SALE_TYPE>'+ISNULL('','')+'</SALE_TYPE>'+'<CRM_CONTRACT_ID>'+ISNULL(SAQTRV.CRM_CONTRACT_ID,'')+'</CRM_CONTRACT_ID>'+'<CANCELLATION_PERIOD>'+ISNULL(CONVERT(VARCHAR,SAQTRV.CANCELLATION_PERIOD),'')+'</CANCELLATION_PERIOD>'+'<CANCELLATION_NOT_PERMITTED>'+ISNULL(CONVERT(VARCHAR,SAQTRV.CANCELLATION_PERIOD_NOTPER),'')+'</CANCELLATION_NOT_PERMITTED>'+'<EMAIL1>'+ISNULL('poc@email.com','')+'</EMAIL1>'+'<EMAIL2>'+ISNULL('poc@email.com','')+'</EMAIL2>'+'<EMAIL3>'+ISNULL('poc@email.com','')+'</EMAIL3>' AS final_xml  FROM SAQTMT(NOLOCK)  JOIN SAQTRV (NOLOCK) ON SAQTMT.QUOTE_ID = SAQTRV.QUOTE_ID WHERE SAQTMT.QUOTE_ID = '"+str(QUOTE_ID)+"' AND SAQTRV.QTEREV_ID = '"+str(REVISION_ID)+"' )A FOR XML PATH ('')  ), 1, 1, ''),'&lt;','<'),'&gt;','>')AS RESULT")
        
        if Quoteheaderquery.RESULT != "" :
            Quoteheaderquery = Quoteheaderquery.RESULT
        else:
            Quoteheaderquery = "<QUOTE_HEADER>"
        
        # QUOTE_INVOLVED_PARTY QUERY
        QuoteInvolvedPartiesquery = SqlHelper.GetFirst("select replace(replace(STUFF((SELECT  ' '+final_xml FROM (SELECT DISTINCT  '<QUOTE_INVOLVED_PARTY>'+'<QUOTE_ID>"+str(CRMQT.c4c_quote_id)+"</QUOTE_ID><SOLD_TO>'+ ISNULL((SELECT REPLACE(ACCOUNT_ID,'STP-','') FROM SAQTMT(NOLOCK) WHERE QUOTE_ID = '"+str(QUOTE_ID)+"' ),'') + '</SOLD_TO><BILL_TO>'+ISNULL((SELECT TOP 1 PARTY_ID FROM SAQTIP(NOLOCK) WHERE QUOTE_ID = '"+str(QUOTE_ID)+"' AND CPQ_PARTNER_FUNCTION = 'BILL TO' AND QTEREV_ID = '"+str(REVISION_ID)+"' ),'')+'</BILL_TO><SHIP_TO>'+ISNULL((SELECT TOP 1 PARTY_ID FROM SAQTIP(NOLOCK) WHERE QUOTE_ID = '"+str(QUOTE_ID)+"' AND CPQ_PARTNER_FUNCTION = 'SHIP TO' AND QTEREV_ID = '"+str(REVISION_ID)+"' ),'')+'</SHIP_TO><PAYER>'+ISNULL((SELECT TOP 1 PARTY_ID FROM SAQTIP(NOLOCK) WHERE QUOTE_ID = '"+str(QUOTE_ID)+"' AND QTEREV_ID = '"+str(REVISION_ID)+"' AND CPQ_PARTNER_FUNCTION = 'PAYER' ),'')+'</PAYER><GPMRPM>'+ISNULL((SELECT TOP 1 CONVERT(VARCHAR(10),CRM_EMPLOYEE_ID) FROM SAQDLT(NOLOCK)A JOIN SAEMPL (NOLOCK) ON MEMBER_ID = EMPLOYEE_ID WHERE QUOTE_ID = '"+str(QUOTE_ID)+"' AND C4C_PARTNERFUNCTION_ID = 'BD MANAGER' AND QTEREV_ID = '"+str(REVISION_ID)+"' ),'')+'</GPMRPM><CONT_MNGR>'+ISNULL((SELECT TOP 1 CONVERT(VARCHAR(10),CRM_EMPLOYEE_ID) FROM SAQDLT(NOLOCK)A JOIN SAEMPL (NOLOCK) ON MEMBER_ID = EMPLOYEE_ID WHERE QUOTE_ID = '"+str(QUOTE_ID)+"' AND C4C_PARTNERFUNCTION_ID = 'CONTRACT MANAGER' AND QTEREV_ID = '"+str(REVISION_ID)+"' AND ISNULL([PRIMARY],'FALSE')='TRUE' ),'')+'</CONT_MNGR><SALES_PERSON>'+ISNULL((SELECT TOP 1 CONVERT(VARCHAR(10),CRM_EMPLOYEE_ID) FROM SAQDLT(NOLOCK)A JOIN SAEMPL (NOLOCK) ON MEMBER_ID = EMPLOYEE_ID WHERE QUOTE_ID = '"+str(QUOTE_ID)+"' AND C4C_PARTNERFUNCTION_ID = 'Sales Employee' AND QTEREV_ID = '"+str(REVISION_ID)+"' AND ISNULL([PRIMARY],'FALSE')='TRUE' ),'')+'</SALES_PERSON>' AS final_xml  FROM SAQTIP(NOLOCK) WHERE QUOTE_ID = '"+str(QUOTE_ID)+"' AND QTEREV_ID = '"+str(REVISION_ID)+"')A FOR XML PATH ('')  ), 1, 1, ''),'&lt;','<'),'&gt;','>')AS RESULT")
        
        if str(QuoteInvolvedPartiesquery.RESULT) != "" :
            QuoteInvolvedPartiesquery = str(QuoteInvolvedPartiesquery.RESULT)
            
            QuoteInvolvedPartiesfabquery = SqlHelper.GetFirst("select replace(replace(STUFF((SELECT  ' '+final_xml FROM (SELECT  DISTINCT '<FAB>'+CASE WHEN ISNULl(CRM_FABLOCATION_ID,'')<>'' THEN CRM_FABLOCATION_ID ELSE ISNULL(SAQFBL.FABLOCATION_ID,'') END+'</FAB>' AS final_xml  FROM SAQICO SAQFBL(NOLOCK) JOIN MAFBLC (NOLOCK) ON SAQFBL.FABLOCATION_ID = MAFBLC.FAB_LOCATION_ID WHERE QUOTE_ID  = '"+str(QUOTE_ID)+"' AND QTEREV_ID = '"+str(REVISION_ID)+"')SUB_SAQFBL FOR XML PATH ('')  ), 1, 1, ''),'&lt;','<'),'&gt;','>')AS RESULT")
            
            QuoteInvolvedPartiescontactquery = SqlHelper.GetFirst("select replace(replace(STUFF((SELECT  ' '+final_xml FROM (SELECT  DISTINCT '<CUST_CONTACT>'+ISNULL(SAEMPL.CRM_EMPLOYEE_ID,'') +'</CUST_CONTACT>' AS final_xml  FROM SAQICT (NOLOCK) JOIN SAEMPL (NOLOCK) ON SAQICT.CONTACT_ID = SAEMPL.EMPLOYEE_ID WHERE QUOTE_ID  = '"+str(QUOTE_ID)+"' AND QTEREV_ID = '"+str(REVISION_ID)+"')SAQICT FOR XML PATH ('')  ), 1, 1, ''),'&lt;','<'),'&gt;','>')AS RESULT")
            
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
        
        QuoteToolIdlingfabquery = SqlHelper.GetFirst("select replace(replace(replace(STUFF((SELECT  ' '+final_xml FROM (SELECT  DISTINCT '<IDLING_PERM>'+ISNULL(TOOLIDLING_VALUE_CODE,'')+'</IDLING_PERM>' AS final_xml  FROM SAQTDA(NOLOCK) WHERE QUOTE_ID  = '"+str(QUOTE_ID)+"' AND QTEREV_ID = '"+str(REVISION_ID)+"' AND TOOLIDLING_ID = 'Idling type' UNION SELECT  DISTINCT '<HOT_IDLE>'+ISNULL(TOOLIDLING_VALUE_CODE,'')+'</HOT_IDLE>'  FROM SAQTDA(NOLOCK) WHERE QUOTE_ID  = '"+str(QUOTE_ID)+"' AND QTEREV_ID = '"+str(REVISION_ID)+"' AND TOOLIDLING_ID = 'Warm / Hot Idle Allowed' UNION SELECT  DISTINCT '<HOT_IDLE_FEE>'+ISNULL(TOOLIDLING_VALUE_CODE,'')+'</HOT_IDLE_FEE>'  FROM SAQTDA(NOLOCK) WHERE QUOTE_ID  = '"+str(QUOTE_ID)+"' AND QTEREV_ID = '"+str(REVISION_ID)+"' AND TOOLIDLING_ID = 'Warm / Hot Idle Fee' UNION SELECT  DISTINCT '<HOT_IDLE_NOTICE>'+ISNULL(TOOLIDLING_VALUE_CODE,'')+'</HOT_IDLE_NOTICE>'  FROM SAQTDA(NOLOCK) WHERE QUOTE_ID  = '"+str(QUOTE_ID)+"' AND QTEREV_ID = '"+str(REVISION_ID)+"' AND TOOLIDLING_ID = 'Max % of Tools to be idled' UNION SELECT  DISTINCT '<COLD_IDLE>'+ISNULL(TOOLIDLING_VALUE_CODE,'')+'</COLD_IDLE>'  FROM SAQTDA(NOLOCK) WHERE QUOTE_ID  = '"+str(QUOTE_ID)+"' AND QTEREV_ID = '"+str(REVISION_ID)+"' AND TOOLIDLING_ID = 'Cold Idle Allowed'  UNION SELECT  DISTINCT '<COLD_IDLE_FEE>'+ISNULL(TOOLIDLING_VALUE_CODE,'')+'</COLD_IDLE_FEE>'  FROM SAQTDA(NOLOCK) WHERE QUOTE_ID  = '"+str(QUOTE_ID)+"' AND QTEREV_ID = '"+str(REVISION_ID)+"' AND TOOLIDLING_ID = 'Cold Idle Fee'  UNION SELECT  DISTINCT '<COLD_IDLE_NOTICE>'+ISNULL(TOOLIDLING_VALUE_CODE,'')+'</COLD_IDLE_NOTICE>'  FROM SAQTDA(NOLOCK) WHERE QUOTE_ID  = '"+str(QUOTE_ID)+"' AND QTEREV_ID = '"+str(REVISION_ID)+"' AND TOOLIDLING_ID = 'Idle Notice' UNION SELECT  DISTINCT '<COLD_IDLE_NOTICE_EXCP>'+ISNULL(TOOLIDLING_VALUE_CODE,'')+'</COLD_IDLE_NOTICE_EXCP>'  FROM SAQTDA(NOLOCK) WHERE QUOTE_ID  = '"+str(QUOTE_ID)+"' AND QTEREV_ID = '"+str(REVISION_ID)+"' AND TOOLIDLING_ID = 'Idle Notice Exception' UNION SELECT  DISTINCT '<IDLING_NOTES>'+ISNULL(TOOLIDLING_VALUE_CODE,'')+'</IDLING_NOTES>'  FROM SAQTDA(NOLOCK) WHERE QUOTE_ID  = '"+str(QUOTE_ID)+"' AND QTEREV_ID = '"+str(REVISION_ID)+"' AND TOOLIDLING_ID = 'Idling Exception Notes' UNION SELECT  DISTINCT '<IDLE_DURATION>'+ISNULL(TOOLIDLING_VALUE_CODE,'')+'</IDLE_DURATION>'  FROM SAQTDA(NOLOCK) WHERE QUOTE_ID  = '"+str(QUOTE_ID)+"' AND QTEREV_ID = '"+str(REVISION_ID)+"' AND TOOLIDLING_ID = 'Idle Duration'   )SUB_SAQFBL FOR XML PATH ('')  ), 1, 1, ''),'&lt;','<'),'&gt;','>'),'â‰¥','&#8805;')  AS RESULT")
        
        if str(QuoteToolIdlingfabquery.RESULT) != "" :
            QuoteInvolvedPartiesquery = QuoteInvolvedPartiesquery+'<QUOTE_TOOL_IDLING><QUOTE_ID>'+str(QUOTE_ID)+'</QUOTE_ID>'+str(QuoteToolIdlingfabquery.RESULT)+'</QUOTE_TOOL_IDLING>'
        else:
            QuoteInvolvedPartiesquery = QuoteInvolvedPartiesquery+'<QUOTE_TOOL_IDLING></QUOTE_TOOL_IDLING>'
        
        """Quoteitemquer = SqlHelper.GetFirst("sp_executesql @T=N'INSERT "+str(SAQITM)+" (QUOTE_ID,SERVICE_ID,LINE,QUANTITY,UOM_ID,EXTENDED_PRICE,PLANT_ID,LINE_ITEM_FROM_DATE,LINE_ITEM_TO_DATE,STATUS,SERVICE_RECORD_ID,SRVTAXCLA_ID,BP_XML,ET_XML,GL_ACCOUNT_NO,REF_SALESORDER_NO ) SELECT QUOTE_ID,SERVICE_ID,(select convert(varchar,max(line)) from "+str(SAQITM)+")+ row_number()over(order by line) as LINE,QUANTITY,UOM_ID,EXTENDED_PRICE * -1,PLANT_ID,LINE_ITEM_FROM_DATE,LINE_ITEM_TO_DATE,STATUS,SERVICE_RECORD_ID,SRVTAXCLA_ID,REPLACE(BP_XML,''<ITEM_LINE_ID>''+ISNULL(CONVERT(VARCHAR(100),(select convert(varchar,max(line)) from "+str(SAQITM)+")+ row_number()over(order by line) as LINE)+''</ITEM_LINE_ID>'',''<ITEM_LINE_ID>''+ISNULL(CONVERT(VARCHAR(100),(select convert(varchar,max(line)) from "+str(SAQITM)+")+ row_number()over(order by line) as LINE)+''</ITEM_LINE_ID>'') AS BP_XML,ET_XML,GL_ACCOUNT_NO,REF_SALESORDER_NO FROM "+str(SAQITM)+" WHERE SERVICE_ID=''Z0117'' '")"""
        
        
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
                    
                    Quoteitemquery = SqlHelper.GetFirst("SELECT REPLACE(REPLACE(REPLACE(REPLACE(REPLACE((select replace(replace(STUFF((SELECT  ' '+final_xml FROM ( SELECT '<QUOTE_ITEM>'+'<QUOTE_ID>"+str(CRMQT.c4c_quote_id)+"</QUOTE_ID>'+'<ITEM_LINE_ID>'+ISNULL(convert(varchar(100),A.LINE_ITEM_ID),'')+'</ITEM_LINE_ID>'+'<SERVICE_ID>'+A.SERVICE_ID+'</SERVICE_ID>'+'<QUANTITY>'+ISNULL(convert(varchar,A.QUANTITY),'')+'</QUANTITY>'+'<TAX_GROUP>'+ISNULL('','')+'</TAX_GROUP>'+'<UOM_ID>'+ISNULL(A.UOM_ID,'')+'</UOM_ID>'+'<NET_VALUE>'+ISNULL(convert(varchar,A.EXTENDED_PRICE),'')+'</NET_VALUE>'+'<ITEM_TYPE>'+ISNULL(A.ITEM_TYPE,'')+'</ITEM_TYPE>'+'<PO_NUMBER>'+CASE WHEN ISNULL(A.PO_NUMBER,'')='' THEN CONVERT(VARCHAR(10),A.CPQTABLEENTRYID) ELSE A.PO_NUMBER END +'</PO_NUMBER>'+'<PO_ITEM>'+CASE WHEN ISNULL(A.PO_ITEM,'')='' THEN  CONVERT(VARCHAR(10),A.LINE_ITEM_ID) ELSE A.PO_ITEM END +'</PO_ITEM>'+'<PO_TEXT>'+ISNULL(A.PO_NOTES,'')+'</PO_TEXT>' +'<PLANT_ID>'+ISNULL(A.PLANT_ID,'')+'</PLANT_ID>'+'<QUOTE_START_DATE>'+REPLACE(ISNULL(convert(varchar(11),A.LINE_ITEM_FROM_DATE,121),''),'-','')+'</QUOTE_START_DATE>'+'<QUOTE_END_DATE>'+REPLACE(ISNULL(convert(varchar(11),A.LINE_ITEM_TO_DATE,121),''),'-','')+'</QUOTE_END_DATE>'+'<INTERNAL_NOTES>'+ISNULL(INTERNAL_NOTES,'')+'</INTERNAL_NOTES>'+'<ITEM_STATUS>'+ISNULL(A.ITEM_STATUS,'')+'</ITEM_STATUS><CONTRACT_TYPE>'+(SELECT LEFT(QUOTE_TYPE,4) FROM SAQTMT (NOLOCK ) WHERE SAQTMT.QUOTE_ID= '"+str(QUOTE_ID)+"')+'</CONTRACT_TYPE><QUOTE_ITEM_COVERED_OBJECT></QUOTE_ITEM_COVERED_OBJECT><QUOTE_ITEM_BILLING_PLAN><ITEM_LINE_ID></ITEM_LINE_ID><BILLING_START_DATE></BILLING_START_DATE><BILLING_AMOUNT></BILLING_AMOUNT></QUOTE_ITEM_BILLING_PLAN><QUOTE_ITEM_PARTS></QUOTE_ITEM_PARTS>'+ ISNULL((SELECT TOP 1 ET_XML FROM "+str(SAQTSE)+" WHERE QUOTE_ID = '"+str(QUOTE_ID)+"'),'<QUOTE_ITEM_ENTITLEMENT></QUOTE_ITEM_ENTITLEMENT>')+ISNULL(REPLACE(REPLACE(STUFF((SELECT ' '+ JSON FROM (SELECT '<QUOTE_ITEM_FPM>'+'<ITEM_LINE_ID>'+ISNULL(convert(varchar(100),SUB_SAQITM.LINE_ITEM_ID),'')+'</ITEM_LINE_ID>'+'<ACCPRT_NUMBER>'+ISNULL(CUSTOMER_PART_NUMBER,'')+'</ACCPRT_NUMBER>'+'<PART_NUMBER>'+ISNULL(PART_NUMBER,'')+'</PART_NUMBER>'+'<PRICEGROUP_ID>'+ISNULL(MATPRIGRP_ID,'')+'</PRICEGROUP_ID>'+'<SCHEDULE_MODE>'+ISNULL(SCHEDULE_MODE,'')+'</SCHEDULE_MODE>'+'<DELIVERY_MODE>'+ISNULL(DELIVERY_MODE,'')+'</DELIVERY_MODE>' +'<ANNUAL_QUANTITY>'+ISNULL(convert(varchar,ANNUAL_QUANTITY),'')+'</ANNUAL_QUANTITY>'+'<UNIT_PRICE>'+ISNULL(convert(varchar,UNIT_PRICE),'')+'</UNIT_PRICE>'+'<VALID_FROM_DATE>'+REPLACE(ISNULL(convert(varchar(11),VALID_FROM_DATE,121),''),'-','')+'</VALID_FROM_DATE>'+'<VALID_TO_DATE>'+REPLACE(ISNULL(convert(varchar(11),VALID_TO_DATE,121),''),'-','')+'</VALID_TO_DATE>'+'</QUOTE_ITEM_FPM>' AS JSON FROM (SELECT ISNULL(convert(varchar(100),SAQITM.LINE_ITEM_ID),'') AS LINE_ITEM_ID,CUSTOMER_PART_NUMBER,PART_NUMBER,SAQIFP.MATPRIGRP_ID, CASE WHEN SCHEDULE_MODE='SCHEDULED' THEN '1' WHEN SCHEDULE_MODE='UNSCHEDULED' THEN '2' WHEN SCHEDULE_MODE='TLS SHARED' THEN '3' WHEN SCHEDULE_MODE='TLS NON-SHARED' THEN '4' WHEN SCHEDULE_MODE='LOW QTY ONSITE' THEN '5' WHEN SCHEDULE_MODE='ON REQUEST' THEN '6' ELSE SCHEDULE_MODE END AS SCHEDULE_MODE, CASE WHEN DELIVERY_MODE='ONSITE' THEN '1' WHEN DELIVERY_MODE='OFFSITE' THEN '2' ELSE DELIVERY_MODE END AS DELIVERY_MODE,ANNUAL_QUANTITY,UNIT_PRICE,VALID_FROM_DATE,VALID_TO_DATE  FROM SAQITM(NOLOCK) JOIN SAQIFP (NOLOCK) ON SAQITM.QUOTE_ID = SAQIFP.QUOTE_ID AND SAQITM.LINE_ITEM_ID = SAQIFP.LINE_ITEM_ID WHERE SAQITM.QUOTE_ID = '"+str(QUOTE_ID)+"' )SUB_SAQITM )A FOR XML PATH ('')  ), 1, 1,'' ),'&lt;','<'),'&gt;','>'),'<QUOTE_ITEM_FPM></QUOTE_ITEM_FPM>')+'</QUOTE_ITEM>' AS final_xml  FROM SAQITM(NOLOCK) WHERE SAQITM.QUOTE_ID = '"+str(QUOTE_ID)+"' )A FOR XML PATH ('')  ), 1, 1, ''),'&lt;','<'),'&gt;','>')AS RESULT),'<QUOTE_ITEM_BILLING_PLAN><ITEM_LINE_ID></ITEM_LINE_ID><BILLING_START_DATE></BILLING_START_DATE><BILLING_AMOUNT></BILLING_AMOUNT></QUOTE_ITEM_BILLING_PLAN>','<QUOTE_ITEM_BILLING_PLAN></QUOTE_ITEM_BILLING_PLAN>' ),'<QUOTE_ITEM_COVERED_OBJECT><ITEM_LINE_ID></ITEM_LINE_ID><EQUIPMENT_ID></EQUIPMENT_ID><SERIAL_NUMBER></SERIAL_NUMBER> </QUOTE_ITEM_COVERED_OBJECT>','<QUOTE_ITEM_COVERED_OBJECT></QUOTE_ITEM_COVERED_OBJECT>'),'<QUOTE_ITEM_PARTS><QUOTE_ID></QUOTE_ID><ITEM_LINE_ID></ITEM_LINE_ID><PART_NUMBER></PART_NUMBER><PART_DESCRIPTION></PART_DESCRIPTION><QUANTITY></QUANTITY></QUOTE_ITEM_PARTS>','<QUOTE_ITEM_PARTS></QUOTE_ITEM_PARTS>' ),'<QUOTE_ITEM_ENTITLEMENT><ITEM_LINE_ID></ITEM_LINE_ID><SERVICE_ID></SERVICE_ID><ENTITLEMENT_NAME></ENTITLEMENT_NAME><ENTITLEMENT_VALUE></ENTITLEMENT_VALUE></QUOTE_ITEM_ENTITLEMENT>','<QUOTE_ITEM_ENTITLEMENT></QUOTE_ITEM_ENTITLEMENT>'),'<QUOTE_ITEM_FPM><ITEM_LINE_ID></ITEM_LINE_ID><ACCPRT_NUMBER></ACCPRT_NUMBER><PART_NUMBER></PART_NUMBER><PRICEGROUP_ID></PRICEGROUP_ID><SCHEDULE_MODE></SCHEDULE_MODE><DELIVERY_MODE></DELIVERY_MODE><ANNUAL_QUANTITY></ANNUAL_QUANTITY><UNIT_PRICE></UNIT_PRICE><VALID_FROM_DATE></VALID_FROM_DATE><VALID_TO_DATE></VALID_TO_DATE></QUOTE_ITEM_FPM>','<QUOTE_ITEM_FPM></QUOTE_ITEM_FPM>' ) AS A ")
                    
                
                else:
                
                    Quoteitemquery = SqlHelper.GetFirst("select replace(replace(STUFF((SELECT  ' '+final_xml FROM ( SELECT DISTINCT '<QUOTE_ITEM>'+'<QUOTE_ID>"+str(CRMQT.c4c_quote_id)+"</QUOTE_ID>'+'<ITEM_LINE_ID>'+ISNULL(convert(varchar(100),A.LINE),'')+'</ITEM_LINE_ID>'+'<SERVICE_ID>'+SAP_PART_NUMBER+'</SERVICE_ID>'+'<QUANTITY>'+ISNULL(convert(varchar,A.QUANTITY),'')+'</QUANTITY>'+'<TARGET_QTY>'+ISNULL(convert(varchar,A.TARGET_QTY),'')+'</TARGET_QTY>'+'<TAX_GROUP>'+ISNULL(A.SRVTAXCLA_ID,'')+'</TAX_GROUP>'+'<UOM_ID>'+ISNULL(A.UOM_ID,'')+'</UOM_ID>'+'<GL_ACCOUNT_NO>'+ISNULL(A.GL_ACCOUNT_NO,'')+'</GL_ACCOUNT_NO>'+'<REF_SALESORDER_NO>'+ISNULL(A.REF_SALESORDER_NO,'')+'</REF_SALESORDER_NO>'+'<DIVISION_ID>'+ISNULL(A.DIVISION_ID,'')+'</DIVISION_ID>'+'<NSO_PART>'+ISNULL(A.NSO_PART,'')+'</NSO_PART>'+'<EVENT_NAME>'+ISNULL(ISNULL(A.PM_ID,MNTEVT_LEVEL),'')+'</EVENT_NAME>'+'<EVENT_TYPE>'+ISNULL(A.MNTEVT_LEVEL,'')+'</EVENT_TYPE>'+'<PRICE_PER_EVENT>'+ISNULL(CASE WHEN SAP_PART_NUMBER ='Z0009' THEN A.PEREVTPRC_INDT_CURR ELSE NULL END,'')+'</PRICE_PER_EVENT>'+'<PRICE_PER_KIT>'+ISNULL(CASE WHEN SAP_PART_NUMBER ='Z0010' THEN A.PEREVTPRC_INDT_CURR ELSE NULL END,'')+'</PRICE_PER_KIT>'+'<NET_VALUE>'+ISNULL(convert(varchar,A.EXTENDED_PRICE),'')+'</NET_VALUE>'+'<ITEM_TYPE>'+ISNULL(A.ITEM_TYPE,'')+'</ITEM_TYPE>'+'<PO_NUMBER>'+CASE WHEN ISNULL(A.PO_NUMBER,'')='' THEN '' ELSE A.PO_NUMBER END +'</PO_NUMBER>'+'<PO_ITEM>'+CASE WHEN ISNULL(A.PO_ITEM,'')='' THEN '' ELSE A.PO_ITEM END+'</PO_ITEM>'+'<PO_TEXT>'+ISNULL(A.PO_NOTES,'')+'</PO_TEXT>' +'<PLANT_ID>'+ISNULL(convert(varchar,A.PLANT_ID),'')+'</PLANT_ID>'+'<QUOTE_START_DATE>'+REPLACE(ISNULL(convert(varchar(11),A.LINE_ITEM_FROM_DATE,121),''),'-','')+'</QUOTE_START_DATE>'+'<QUOTE_END_DATE>'+REPLACE(ISNULL(convert(varchar(11),A.LINE_ITEM_TO_DATE,121),''),'-','')+'</QUOTE_END_DATE>'+'<INTERNAL_NOTES>'+ISNULL(A.INTERNAL_NOTES,'')+'</INTERNAL_NOTES>'+'<ITEM_STATUS>'+ISNULL(A.STATUS,'')+'</ITEM_STATUS><CONTRACT_TYPE>'+(SELECT DOCTYP_ID FROM SAQTRV A(NOLOCK ) WHERE A.QUOTE_ID= '"+str(QUOTE_ID)+"' AND QTEREV_ID = '"+str(REVISION_ID)+"' )+'</CONTRACT_TYPE>'+ISNULL(REPLACE(REPLACE(STUFF((SELECT ' '+ JSON FROM (SELECT '<QUOTE_ITEM_COVERED_OBJECT>'+'<ITEM_LINE_ID>'+CASE WHEN ISNULL(A.EQUIPMENT_ID,'') <> '' THEN ISNULL(convert(varchar(100),A.LINE),'')ELSE '' END+'</ITEM_LINE_ID>'+'<EQUIPMENT_ID>'+ISNULL(A.EQUIPMENT_ID,'')+'</EQUIPMENT_ID>'+'<SERIAL_NUMBER>'+ISNULL(A.SERIAL_NUMBER,'')+'</SERIAL_NUMBER>'+'</QUOTE_ITEM_COVERED_OBJECT>'  AS JSON FROM ( SELECT DISTINCT B.LINE,B.EQUIPMENT_ID,B.SERIAL_NUMBER FROM "+str(SAQICO)+" (NOLOCK)B WHERE B.QUOTE_ID = A.QUOTE_ID AND B.SERVICE_ID = A.SERVICE_ID AND B.LINE = A.LINE )A )A FOR XML PATH ('')  ), 1, 1,'' ),'&lt;','<'),'&gt;','>'),'')+ISNULL(BP_XML ,'')+ISNULL(REPLACE(REPLACE(STUFF((SELECT ' '+ JSON FROM (SELECT '<QUOTE_ITEM_PARTS>'+'<QUOTE_ID>"+str(CRMQT.c4c_quote_id)+"</QUOTE_ID>'+'<ITEM_LINE_ID>'+ISNULL(CONVERT(VARCHAR(100),A.LINE),'')+'</ITEM_LINE_ID>'+'<PART_NUMBER>'+ISNULL(A.PART_NUMBER,'')+'</PART_NUMBER>'+'<PART_DESCRIPTION>'+ISNULL(A.PART_DESCRIPTION,'')+'</PART_DESCRIPTION>'+'<NEW_PART>'+ISNULL(CONVERT(VARCHAR(100),NEW_PART),'')+'</NEW_PART>'+'<QUANTITY>'+ISNULL(convert(varchar,A.QUANTITY),'')+'</QUANTITY>'+'<PRICE_PER_KIT>'+ISNULL(convert(varchar,PRICE_PER_KIT),'')+'</PRICE_PER_KIT>'+'</QUOTE_ITEM_PARTS>'  AS JSON FROM ( SELECT DISTINCT A.LINE,PART_NUMBER AS PART_NUMBER,PART_DESCRIPTION AS PART_DESCRIPTION, ISNULL(CONVERT(VARCHAR,B.QUANTITY),'') AS QUANTITY,ISNULL(NEW_PART,'') AS NEW_PART,ISNULL(CASE WHEN SAP_PART_NUMBER ='Z0010' THEN C.PEREVTPRC_INDT_CURR ELSE NULL END,'') AS PRICE_PER_KIT FROM "+str(SAQSAP)+" (NOLOCK)B JOIN "+str(SAQITM)+" C(NOLOCK) ON B.QUOTE_ID = C.QUOTE_ID AND B.SERVICE_ID = C.SERVICE_ID AND B.LINE = C.LINE WHERE B.QUOTE_ID = A.QUOTE_ID AND B.SERVICE_ID = A.SERVICE_ID AND C.LINE = A.LINE AND ISNULL(PART_NUMBER,'')<>'' )A )A FOR XML PATH ('')  ), 1, 1,'' ),'&lt;','<'),'&gt;','>'),'<QUOTE_ITEM_PARTS></QUOTE_ITEM_PARTS>')+ISNULL(ET_XML,'<QUOTE_ITEM_ENTITLEMENT></QUOTE_ITEM_ENTITLEMENT>')+ISNULL(REPLACE(REPLACE(STUFF((SELECT ' '+ JSON FROM (SELECT '<QUOTE_ITEM_FPM>'+'<ITEM_LINE_ID>'+ISNULL(convert(varchar(100),A.LINE),'')+'</ITEM_LINE_ID>'+'<ACCPRT_NUMBER>'+ISNULL(CUSTOMER_PART_NUMBER,'')+'</ACCPRT_NUMBER>'+'<PART_NUMBER>'+ISNULL(PART_NUMBER,'')+'</PART_NUMBER>'+'<PRICEGROUP_ID>'+ISNULL(MATPRIGRP_ID,'')+'</PRICEGROUP_ID>'+'<SCHEDULE_MODE>'+ISNULL(SCHEDULE_MODE,'')+'</SCHEDULE_MODE>'+'<DELIVERY_MODE>'+ISNULL(DELIVERY_MODE,'')+'</DELIVERY_MODE>' +'<ANNUAL_QUANTITY>'+ISNULL(convert(varchar,ANNUAL_QUANTITY),'')+'</ANNUAL_QUANTITY>'+'<UNIT_PRICE>'+ISNULL(convert(varchar,UNIT_PRICE),'')+'</UNIT_PRICE>'+'<VALID_FROM_DATE>'+REPLACE(ISNULL(convert(varchar(11),VALID_FROM_DATE,121),''),'-','')+'</VALID_FROM_DATE>'+'<VALID_TO_DATE>'+REPLACE(ISNULL(convert(varchar(11),VALID_TO_DATE,121),''),'-','')+'</VALID_TO_DATE>'+'</QUOTE_ITEM_FPM>' AS JSON FROM ( SELECT ISNULL(convert(varchar(100),A.LINE),'') AS LINE,CUSTOMER_PART_NUMBER,PART_NUMBER,B.MATPRIGRP_ID, CASE WHEN SCHEDULE_MODE='SCHEDULED' THEN '1' WHEN SCHEDULE_MODE='UNSCHEDULED' THEN '2' WHEN SCHEDULE_MODE='TLS SHARED' THEN '3' WHEN SCHEDULE_MODE='TLS NON-SHARED' THEN '4' WHEN SCHEDULE_MODE='LOW QTY ONSITE' THEN '5' WHEN SCHEDULE_MODE='ON REQUEST' THEN '6' ELSE SCHEDULE_MODE END AS SCHEDULE_MODE, CASE WHEN DELIVERY_MODE='ONSITE' THEN '1' WHEN DELIVERY_MODE='OFFSITE' THEN '2' ELSE DELIVERY_MODE END AS DELIVERY_MODE,ANNUAL_QUANTITY,UNIT_PRICE,VALID_FROM_DATE,VALID_TO_DATE  FROM "+str(SAQICO)+"(NOLOCK) A JOIN SAQIFP B(NOLOCK) ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID WHERE A.QUOTE_ID = '"+str(QUOTE_ID)+"' AND B1.LINE = B.LINE )A )A FOR XML PATH ('')  ), 1, 1,'' ),'&lt;','<'),'&gt;','>'),'<QUOTE_ITEM_FPM></QUOTE_ITEM_FPM>')+'</QUOTE_ITEM>' AS final_xml  FROM "+str(SAQITM)+" (NOLOCK) A LEFT JOIN "+str(SAQICO)+"  B1(NOLOCK) ON A.QUOTE_ID = B1.QUOTE_ID AND A.SERVICE_ID = B1.SERVICE_ID AND A.LINE = B1.LINE JOIN "+str(CRMTMP)+" TEMP (NOLOCK) ON A.LINE = TEMP.EQUIPMENT_IDD JOIN MAMTRL V(NOLOCK) ON A.SERVICE_RECORD_ID = V.MATERIAL_RECORD_ID WHERE A.QUOTE_ID = '"+str(QUOTE_ID)+"'   )A FOR XML PATH ('')  ), 1, 1, ''),'&lt;','<'),'&gt;','>')AS A ")

                if str(Quoteitemquery.A) == '':
                    Quoteiteminfo = '<QUOTE_ITEM><QUOTE_ITEM_COVERED_OBJECT></QUOTE_ITEM_COVERED_OBJECT><QUOTE_ITEM_BILLING_PLAN></QUOTE_ITEM_BILLING_PLAN><QUOTE_ITEM_PARTS></QUOTE_ITEM_PARTS><QUOTE_ITEM_ENTITLEMENT></QUOTE_ITEM_ENTITLEMENT><QUOTE_ITEM_FPM></QUOTE_ITEM_FPM></QUOTE_ITEM>'
                else:
                    Quoteiteminfo = str(Quoteitemquery.A)
            
                str_xml = str(Quoteiteminfo)
                data = data+str_xml
                CRMTMP1 = SqlHelper.GetFirst("sp_executesql @T=N'DELETE FROM "+str(CRMTMP)+" ' ")
            else:
                Check_flag1=0
        
    
    data = Quoteheaderquery+str(data)+str(QuoteInvolvedPartiesquery)+'</QUOTE_HEADER>'			

    Final_xml = "<QUOTE>"+data+"</QUOTE>"

    Parameter = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'SELECT' ")
        
    primaryQueryItems = SqlHelper.GetFirst( ""+ str(Parameter.QUERY_CRITERIA_1)+ " SYINPL (INTEGRATION_PAYLOAD,INTEGRATION_KEY,CpqTableEntryDateModified,INTEGRATION_NAME)  select ''"+Final_xml+ "'',''"+ str(QUOTE_ID)+ "'',getdate(),''CPQ to CRM Quote Replication'' ' ")

    SAQICO_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQICO)+"'' ) BEGIN DROP TABLE "+str(SAQICO)+" END  ' ")
    SAQIBP_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQIBP)+"'' ) BEGIN DROP TABLE "+str(SAQIBP)+" END  ' ")
    SAQIEN_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQIEN)+"'' ) BEGIN DROP TABLE "+str(SAQIEN)+" END  ' ")
    SAQSAP_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQSAP)+"'' ) BEGIN DROP TABLE "+str(SAQSAP)+" END  ' ")
    SAQTSE_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQTSE)+"'' ) BEGIN DROP TABLE "+str(SAQTSE)+" END  ' ")
    SAQITM_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQITM)+"'' ) BEGIN DROP TABLE "+str(SAQITM)+" END  ' ")
    CRMTMP_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(CRMTMP)+"'' ) BEGIN DROP TABLE "+str(CRMTMP)+" END  ' ")
    
    #OAUTH AUTHENTICATION
    try:	
        Oauth_info = SqlHelper.GetFirst("SELECT  DOMAIN,URL FROM SYCONF where EXTERNAL_TABLE_NAME ='OAUTH'")
        requestdata =Oauth_info.DOMAIN
        webclient = System.Net.WebClient()
        webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/x-www-form-urlencoded"
        response = webclient.UploadString(Oauth_info.URL,str(requestdata))
    except:
        Log.Info("except in prsm1--->")
        time.sleep(5)
        Oauth_info = SqlHelper.GetFirst("SELECT  DOMAIN,URL FROM SYCONF where EXTERNAL_TABLE_NAME ='OAUTH'")
        requestdata =Oauth_info.DOMAIN
        webclient = System.Net.WebClient()
        webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/x-www-form-urlencoded"
        response = webclient.UploadString(Oauth_info.URL,str(requestdata))

    response = eval(response)
    access_token = response['access_token']
    
    
    LOGIN_CREDENTIALS = SqlHelper.GetFirst("SELECT USER_NAME as Username,Password,Domain FROM SYCONF where Domain='AMAT_TST'")
    
    if LOGIN_CREDENTIALS is not None:
        Login_Username = str(LOGIN_CREDENTIALS.Username)
        Login_Password = str(LOGIN_CREDENTIALS.Password)
        authorization = Login_Username+":"+Login_Password
        binaryAuthorization = UTF8.GetBytes(authorization)
        authorization = Convert.ToBase64String(binaryAuthorization)
        authorization = "Basic " + authorization

        webclient = System.Net.WebClient()
        webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/xml"
        webclient.Headers.Add("BearerToken", str(access_token)) 
        webclient.Headers[System.Net.HttpRequestHeader.Authorization] = authorization;
        
        LOGIN_CRE = SqlHelper.GetFirst("SELECT URL FROM SYCONF (nolock) where EXTERNAL_TABLE_NAME ='CPQ_TO_CRM_QUOTE'")

        final_xml_data = """<?xml version="1.0" encoding="UTF-8"?><soapenv:Envelope   xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"> <soapenv:Body>{}</soapenv:Body></soapenv:Envelope>""".format(Final_xml)
        
        crm_response = webclient.UploadString(str(LOGIN_CRE.URL), final_xml_data)	
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
        


    Log.Info("QTPOSTQCRMQTPOSTQCRM ERROR---->:" + str(sys.exc_info()[1]))
    Log.Info("QTPOSTQCRM ERROR LINE NO---->:" + str(sys.exc_info()[-1].tb_lineno))
    ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "400", "Message": str(sys.exc_info()[1])}]})
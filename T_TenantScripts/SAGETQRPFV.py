# =========================================================================================================================================
#   __script_name : SAGETQRPFV.PY
#   __script_description : THIS SCRIPT IS RECEIVED C4C DATA  AND SEND TO C4C SYSTEM
#   __primary_author__ : BAJI
#   __create_date :
#   Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import sys
import datetime
import time
import clr
import System.Net
import CQCPQC4CWB
#from System.Text.Encoding import UTF8A
from System import Convert
from System.Net import HttpWebRequest, NetworkCredential

clr.AddReference("System.Net")
from System.Net import CookieContainer, NetworkCredential, Mail
from System.Net.Mail import SmtpClient, MailAddress, Attachment, MailMessage

try:
    if 'Param' in globals():    
        if hasattr(Param, 'CPQ_Columns'): 
            Quote_ID = ''
            Revision_ID = ''    
            
            primaryQueryItems = SqlHelper.GetFirst("SELECT NEWID() AS A")       
            for table_dict in Param.CPQ_Columns: 
                tbl = str(table_dict.Key)
                if str(tbl).upper() == "QUOTE_ID":
                    Quote_ID = str(table_dict.Value)
                if str(tbl).upper() == "REVISION_ID":
                    Revision_ID = str(table_dict.Value)
               
            
            Opportunity = SqlHelper.GetFirst("SELECT CASE WHEN ISNULL(RESULT,'') = '' THEN '' ELSE RESULT END AS RESULT FROM (SELECT replace ('\"Opportunity\": ['+STUFF((SELECT ','+ JSON FROM (SELECT DISTINCT '{\"OppID\" : \"'+OppID+'\",\"ContractValidFrom\" : \"'+ContractValidFrom+'\",\"ContractValidTo\" : \"'+ContractValidTo+'\"}' AS JSON from (SELECT DISTINCT ISNULL((SELECT TOP 1 OPPORTUNITY_ID FROM SAOPQT WHERE QUOTE_ID='"+ str(Quote_ID) +"'),'') AS OppID,ISNULL(CONVERT(VARCHAR(11),SAQTMT.QUOTE_CREATED_DATE,101),'') AS ExpectedBookingDate,ISNULL(CONVERT(VARCHAR(11),SAQTMT.CONTRACT_VALID_FROM,101),'') AS ContractValidFrom,ISNULL(CONVERT(VARCHAR(11),SAQTMT.CONTRACT_VALID_TO,101),'') AS ContractValidTo FROM SAQTMT (NOLOCK)  WHERE SAQTMT.QUOTE_ID ='"+ str(Quote_ID) +"' AND SAQTMT.QTEREV_ID ='"+ str(Revision_ID) + "'  ) t    ) A FOR XML PATH ('')  ), 1, 1, '')+']','amp;#','#') AS RESULT)A " )
            
        
            Fab = SqlHelper.GetFirst("SELECT CASE WHEN ISNULL(RESULT,'') = '' THEN '' ELSE RESULT END AS RESULT FROM (SELECT replace ('\"Fab\": ['+STUFF((SELECT ','+ JSON FROM (SELECT DISTINCT '{\"FabID\" : \"'+FabID+'\",\"FabName\" : \"'+FabName+'\",\"FabLocation\" : \"'+FabLocation+'\",\"FabCity\" : \"'+FabCity+'\",\"FabCountry\" : \"'+FabCountry+'\",\"FabSalesOrg\" : \"'+FabSalesOrg+'\"}' AS JSON from (SELECT DISTINCT ISNULL(A.FABLOCATION_ID,'') AS FabID, ISNULL(A.FABLOCATION_NAME,'') AS FabName,ISNULL(B.ADDRESS_1,'') AS FabLocation, ISNULL(B.CITY,'') AS FabCity,ISNULL(B.COUNTRY,'') AS FabCountry,ISNULL(B.SALESORG_ID,'') AS FabSalesOrg FROM SAQRIO (NOLOCK) A JOIN MAEQUP (NOLOCK) C ON A.EQUIPMENT_iD = C.EQUIPMENT_iD JOIN MAFBLC B(NOLOCK) ON C.FABLOCATION_ID = B.FAB_LOCATION_ID   WHERE A.QUOTE_ID ='"+ str(Quote_ID) +"' AND A.QTEREV_ID ='"+ str(Revision_ID) + "'  ) t    ) A FOR XML PATH ('')  ), 1, 1, '')+']','amp;#','#') AS RESULT)A " )
            
            ProductOffering = SqlHelper.GetFirst("SELECT CASE WHEN ISNULL(RESULT,'') = '' THEN '' ELSE RESULT END AS RESULT FROM (SELECT replace ('\"ProductOffering\": ['+STUFF((SELECT ','+ JSON FROM (SELECT DISTINCT '{\"ServiceID\" : \"'+ServiceID+'\",\"RevenueStartDate\" : \"'+RevenueStartDate+'\",\"ForcastValue\" : \"'+ForcastValue+'\",\"ServiceDescription\" : \"'+ServiceDescription+'\",\"RevenueEndDate\" : \"'+RevenueEndDate+'\" '+ItemRevenueSchedule+' }' AS JSON from (SELECT DISTINCT ISNULL(SAQRIS.SERVICE_ID,'') AS ServiceID,ISNULL(CONVERT(VARCHAR(11),CONTRACT_VALID_FROM,101),'') AS RevenueStartDate,ISNULL(CONVERT(VARCHAR(11),CONTRACT_VALID_TO,101),'') AS RevenueEndDate,ISNULL(CONVERT(VARCHAR,ISNULL(SAQRIS.ESTVAL_INGL_CURR,0) + ISNULL(SAQRIS.NET_VALUE_INGL_CURR,0)),'') AS ForcastValue,ISNULL(SERVICE_DESCRIPTION,'') AS ServiceDescription,ISNULL(','+(SELECT replace ('\"ItemRevenueSchedule\": ['+STUFF((SELECT ','+ JSON FROM (SELECT DISTINCT '{\"ItemScheduleDate\" : \"'+ItemScheduleDate+'\",\"Value\" : \"'+Value+'\"}' AS JSON from (SELECT DISTINCT CONVERT(VARCHAR,CASE WHEN  SAQIBP.SERVICE_ID IN ('Z0116','Z0117') AND sum(ISNULL(SAQIBP.BILLING_VALUE_INGL_CURR,0)) <0 THEN  sum(ISNULL(SAQIBP.BILLING_VALUE_INGL_CURR,0)) * -1 ELSE sum(ISNULL(SAQIBP.ESTVAL_INGL_CURR,0) + ISNULL(SAQIBP.BILLING_VALUE_INGL_CURR,0)) END ) AS Value,CONVERT(VARCHAR,BILLING_DATE,101) AS ItemScheduleDate FROM SAQIBP (NOLOCK)  WHERE SAQIBP.QUOTE_ID =SAQRIS.QUOTE_ID AND SAQIBP.QTEREV_ID = SAQRIS.QTEREV_ID  AND SAQIBP.SERVICE_ID = SAQRIS.SERVICE_ID GROUP BY CONVERT(VARCHAR,BILLING_DATE,101),SERVICE_ID ) t    ) A FOR XML PATH ('')  ), 1, 1, '')+']','amp;#','#')),'') As ItemRevenueSchedule FROM SAQRIS (NOLOCK)  WHERE SAQRIS.QUOTE_ID ='"+ str(Quote_ID) +"' AND SAQRIS.QTEREV_ID ='"+ str(Revision_ID) + "'  ) t    ) A FOR XML PATH ('')  ), 1, 1, '')+']','amp;#','#') AS RESULT)A " )
            
            Tools = SqlHelper.GetFirst("SELECT CASE WHEN ISNULL(RESULT,'') = '' THEN '' ELSE RESULT END AS RESULT FROM (SELECT replace ('\"Tools\": ['+STUFF((SELECT ','+ JSON FROM (SELECT DISTINCT '{\"ToolId\" : \"'+ToolId+'\",\"ToolDescription\" : \"'+ToolDescription+'\",\"SerialID\" : \"'+SerialID+'\",\"CustomerToolID\" : \"'+CustomerToolID+'\",\"FabName\" : \"'+FabName+'\",\"FabID\" : \"'+FabID+'\",\"FabLocation\" : \"'+FabLocation+'\",\"GreenBook\" : \"'+GreenBook+'\",\"WarrantyDate\" : \"'+WarrantyDate+'\",\"PLATFORM\" : \"'+PLATFORM+'\"}' AS JSON from (SELECT DISTINCT ISNULL(SAQICO.EQUIPMENT_ID,'') AS ToolId,ISNULL(EQUIPMENT_DESCRIPTION,'') AS ToolDescription, ISNULL(SERIAL_NO,'') AS SerialID, ISNULL(CUSTOMER_TOOL_ID,'') AS CustomerToolID,  ISNULL(FABLOCATION_NAME,'') AS FabName, ISNULL(GREENBOOK,'') AS GreenBook,ISNULL(PLTFRM,'') AS Platform,ISNULL(FABLOCATION_ID,'') AS FabID,ISNULL((SELECT TOP 1 ADDRESS_1 FROM MAFBLC(NOLOCK) WHERE  MAFBLC.FAB_LOCATION_ID = SAQICO.FABLOCATION_ID),'') AS FabLocation,ISNULL(CONVERT(VARCHAR(11),WTYEND),'') AS WarrantyDate FROM SAQICO (NOLOCK)  WHERE SAQICO.QUOTE_ID ='"+ str(Quote_ID) +"' AND SAQICO.QTEREV_ID ='"+ str(Revision_ID) + "'  AND ISNULL(EQUIPMENT_ID,'')<>'' ) t    ) A FOR XML PATH ('')  ), 1, 1, '')+']','amp;#','#') AS RESULT)A " )

            ToolWorksheet = SqlHelper.GetFirst("SELECT CASE WHEN ISNULL(RESULT,'') = '' THEN '' ELSE RESULT END AS RESULT FROM (SELECT replace ('\"ToolWorksheet\": ['+STUFF((SELECT ','+ JSON FROM (SELECT DISTINCT '{\"ToolId\" : \"'+ToolId+'\",\"ServiceID\" : \"'+ServiceID+'\",\"ToolDescription\" : \"'+ToolDescription+'\",\"REgisteredProdctCatogory\" : \"'+REgisteredProdctCatogory+'\",\"DateFrom\" : \"'+DateFrom+'\",\"DateTo\" : \"'+DateTo+'\",\"Platform\" : \"'+Platform+'\",\"Greenbook\" : \"'+Greenbook+'\",\"Technology\" : \"'+Technology+'\",\"Select\" : \"'+Flag+'\",\"ProductOfferingName\" : \"'+ProductOfferingName+'\"}' AS JSON from (SELECT DISTINCT ISNULL(SAQRIO.EQUIPMENT_ID,'') AS ToolId,ISNULL(SAQRIO.SERVICE_ID,'') AS ServiceID,ISNULL(SAQRIO.EQUIPMENT_DESCRIPTION,'') AS  ToolDescription ,ISNULL(MAEQUP.EQUIPMENTCATEGORY_ID,'') AS REgisteredProdctCatogory, ISNULL(MAEQUP.PLATFORM,'') AS Platform,ISNULL(SAQRIO.GREENBOOK,'') AS Greenbook,ISNULL(SAQRIO.TECHNOLOGY,'') AS Technology,ISNULL(SAQRIO.SERVICE_DESCRIPTION,'') AS ProductOfferingName,ISNULL(CONVERT(VARCHAR(11),SAQRIT.CONTRACT_VALID_FROM,101),'') AS DateFrom,ISNULL(CONVERT(VARCHAR(11),SAQRIT.CONTRACT_VALID_TO,101),'') AS DateTo ,'True' as Flag FROM SAQRIO (NOLOCK) JOIN SAQRIT (NOLOCK) ON SAQRIO.QUOTE_ID = SAQRIT.QUOTE_ID AND SAQRIO.QTEREV_ID = SAQRIT.QTEREV_ID AND SAQRIO.LINE = SAQRIT.LINE JOIN MAEQUP(NOLOCK) ON SAQRIO.EQUIPMENT_ID = MAEQUP.EQUIPMENT_ID WHERE SAQRIO.QUOTE_ID ='"+ str(Quote_ID) +"' AND SAQRIO.QTEREV_ID ='"+ str(Revision_ID) + "' AND ISNULL(SAQRIO.EQUIPMENT_ID,'')<>'' ) t    ) A FOR XML PATH ('')  ), 1, 1, '')+']','amp;#','#') AS RESULT)A " )
            
            ForcastWorksheet = SqlHelper.GetFirst("SELECT CASE WHEN ISNULL(RESULT,'') = '' THEN '' ELSE RESULT END AS RESULT FROM (SELECT replace ('\"ForcastWorksheet\": ['+STUFF((SELECT ','+ JSON FROM (SELECT DISTINCT '{\"GreenBook\" : \"'+GreenBook+'\",\"ServiceID\" : \"'+ServiceID+'\",\"ForcastValue\" : \"'+ForcastValue+'\",\"ProductOfferingName\" : \"'+ProductOfferingName+'\"}' AS JSON from (SELECT DISTINCT ISNULL(SAQIGS.GREENBOOK,'') AS GreenBook,ISNULL(SAQIGS.SERVICE_ID,'') AS ServiceID, ISNULL(CONVERT(VARCHAR(100),ISNULL(SAQIGS.ESTVAL_INGL_CURR,0) + ISNULL(SAQIGS.NET_VALUE_INGL_CURR,0)),'') AS ForcastValue,ISNULL(SERVICE_DESCRIPTION,'') AS ProductOfferingName FROM SAQIGS (NOLOCK)  WHERE SAQIGS.QUOTE_ID ='"+ str(Quote_ID) +"' AND SAQIGS.QTEREV_ID ='"+ str(Revision_ID) + "'  ) t    ) A FOR XML PATH ('')  ), 1, 1, '')+']','amp;#','#') AS RESULT)A " )
            
            BookingForcast = SqlHelper.GetFirst("SELECT CASE WHEN ISNULL(RESULT,'') = '' THEN '' ELSE RESULT END AS RESULT FROM (SELECT replace ('\"BookingForecast\": ['+STUFF((SELECT ','+ JSON FROM (SELECT DISTINCT '{\"ServiceID\" : \"'+ServiceID+'\",\"ForcastValue\" : \"'+ForcastValue+'\",\"ServiceDescription\" : \"'+ServiceDescription+'\"}' AS JSON from (SELECT DISTINCT ISNULL(SAQRIS.SERVICE_ID,'') AS ServiceID, ISNULL(CONVERT(VARCHAR(100),ISNULL(SAQRIS.ESTVAL_INGL_CURR,0) + ISNULL(SAQRIS.NET_VALUE_INGL_CURR,0)),'')  AS ForcastValue,ISNULL(SERVICE_DESCRIPTION,'') AS ServiceDescription FROM SAQRIS (NOLOCK)  WHERE SAQRIS.QUOTE_ID ='"+ str(Quote_ID) +"' AND SAQRIS.QTEREV_ID ='"+ str(Revision_ID) + "' ) t    ) A FOR XML PATH ('')  ), 1, 1, '')+']','amp;#','#') AS RESULT)A " )
            
            final_json = ''
            if Opportunity.RESULT != '':
                final_json = Opportunity.RESULT+','
            if Fab.RESULT != '':
                final_json = final_json+Fab.RESULT+','
            if ProductOffering.RESULT != '':
                final_json = final_json+ProductOffering.RESULT+','
            if Tools.RESULT != '':
                final_json = final_json+Tools.RESULT+','
            if ToolWorksheet.RESULT != '':
                final_json = final_json+ToolWorksheet.RESULT+','
            if ForcastWorksheet.RESULT != '':
                final_json = final_json+ForcastWorksheet.RESULT+','
            if BookingForcast.RESULT != '':
                final_json = final_json+BookingForcast.RESULT+','
            #Log.Info("6666--->"+str(final_json))


            Parameter = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'SELECT' ")
                
            Final_json = eval('{'+final_json[:-1]+'}')
            
            if len(Final_json)>0:       
            
                ApiResponse = ApiResponseFactory.JsonResponse(Final_json)  

            else:
                ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "200", "Message": "NO DATA AVAILABLE FOR SYNCHRONIZATION"}]})

            ####Calling the iflow script to update the details in c4c..(cpq to c4c write back...)
            revision_object = SqlHelper.GetFirst("SELECT QUOTE_RECORD_ID,QTEREV_RECORD_ID FROM SAQTRV(NOLOCK) WHERE QUOTE_ID = '{}' AND QTEREV_ID = '{}'".format(Quote_ID,Revision_ID))
            if revision_object:
                CQCPQC4CWB.writeback_to_c4c("quote_header",revision_object.QUOTE_RECORD_ID,revision_object.QTEREV_RECORD_ID)
                time.sleep(5)
                CQCPQC4CWB.writeback_to_c4c("opportunity_header",revision_object.QUOTE_RECORD_ID,revision_object.QTEREV_RECORD_ID)
            
            final_json = final_json.replace("'","")

            primaryQueryItems = SqlHelper.GetFirst( ""+ str(Parameter.QUERY_CRITERIA_1)+ " SYINPL (INTEGRATION_PAYLOAD,CPQTABLEENTRYDATEADDED,INTEGRATION_NAME)  select ''"+final_json[:-1]+ "'',GETDATE() AS CPQTABLEENTRYDATEADDED,''CPQ_TO_C4C_WRITEBACK'' ' ")
            
                            
except:
    Log.Info("SAGETQRPFV ERROR---->:" + str(sys.exc_info()[1]))
    Log.Info("SAGETQRPFV ERROR LINE NO---->:" + str(sys.exc_info()[-1].tb_lineno))
    ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "400", "Message": str(sys.exc_info()[1])}]})
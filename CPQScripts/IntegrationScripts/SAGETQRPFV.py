# =========================================================================================================================================
#   __script_name : SAGETQRPFV.PY
#   __script_description : THIS SCRIPT IS RECEIVED C4C DATA  AND SEND TO C4C SYSTEM
#   __primary_author__ : BAJI
#   __create_date :
#   Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import sys
import datetime 
import clr
import System.Net
from System.Text.Encoding import UTF8
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
               
            
            Opportunity = SqlHelper.GetFirst("SELECT CASE WHEN ISNULL(RESULT,'') = '' THEN '' ELSE RESULT END AS RESULT FROM (SELECT replace ('\"Opportunity\": ['+STUFF((SELECT ','+ JSON FROM (SELECT DISTINCT '{\"OppID\" : \"'+OppID+'\",\"ExpectedBookingDate\" : \"'+ExpectedBookingDate+'\",\"ContractValidFrom\" : \"'+ContractValidFrom+'\",\"ContractValidTo\" : \"'+ContractValidTo+'\"}' AS JSON from (SELECT DISTINCT ISNULL((SELECT TOP 1 OPPORTUNITY_ID FROM SAOPQT WHERE QUOTE_ID='"+ str(Quote_ID) +"'),'') AS OppID,ISNULL(CONVERT(VARCHAR(11),SAQTMT.QUOTE_CREATED_DATE,101),'') AS ExpectedBookingDate,ISNULL(CONVERT(VARCHAR(11),SAQTMT.CONTRACT_VALID_FROM,101),'') AS ContractValidFrom,ISNULL(CONVERT(VARCHAR(11),SAQTMT.CONTRACT_VALID_TO,101),'') AS ContractValidTo FROM SAQTMT (NOLOCK)  WHERE SAQTMT.QUOTE_ID ='"+ str(Quote_ID) +"' AND SAQTMT.QTEREV_ID ='"+ str(Revision_ID) + "'  ) t    ) A FOR XML PATH ('')  ), 1, 1, '')+']','amp;#','#') AS RESULT)A " )
            
        
            Fab = SqlHelper.GetFirst("SELECT CASE WHEN ISNULL(RESULT,'') = '' THEN '' ELSE RESULT END AS RESULT FROM (SELECT replace ('\"Fab\": ['+STUFF((SELECT ','+ JSON FROM (SELECT DISTINCT '{\"FabID\" : \"'+FabID+'\",\"FabName\" : \"'+FabName+'\",\"FabLocation\" : \"'+FabLocation+'\",\"FabCity\" : \"'+FabCity+'\",\"FabCountry\" : \"'+FabCountry+'\",\"FabSalesOrg\" : \"'+FabSalesOrg+'\"}' AS JSON from (SELECT DISTINCT ISNULL(A.FABLOCATION_ID,'') AS FabID, ISNULL(A.FABLOCATION_NAME,'') AS FabName,ISNULL(B.ADDRESS_1,'') AS FabLocation, ISNULL(B.CITY,'') AS FabCity,ISNULL(COUNTRY,'') AS FabCountry,ISNULL(A.SALESORG_ID,'') AS FabSalesOrg FROM SAQICO (NOLOCK) A JOIN MAFBLC B(NOLOCK) ON A.FABLOCATION_ID = B.FAB_LOCATION_ID  WHERE A.QUOTE_ID ='"+ str(Quote_ID) +"' AND A.QTEREV_ID ='"+ str(Revision_ID) + "'  ) t    ) A FOR XML PATH ('')  ), 1, 1, '')+']','amp;#','#') AS RESULT)A " )
            
            ProductOffering = SqlHelper.GetFirst("SELECT CASE WHEN ISNULL(RESULT,'') = '' THEN '' ELSE RESULT END AS RESULT FROM (SELECT replace ('\"ProductOffering\": ['+STUFF((SELECT ','+ JSON FROM (SELECT DISTINCT '{\"ServiceID\" : \"'+ServiceID+'\",\"RevenueStartDate\" : \"'+RevenueStartDate+'\",\"RevenueEndDate\" : \"'+RevenueEndDate+'\"}' AS JSON from (SELECT DISTINCT ISNULL(SAQICO.SERVICE_ID,'') AS ServiceID,ISNULL(CONVERT(VARCHAR(11),SAQICO.CONTRACT_VALID_FROM,101),'') AS RevenueStartDate,ISNULL(CONVERT(VARCHAR(11),SAQICO.CONTRACT_VALID_TO,101),'') AS RevenueEndDate FROM SAQICO (NOLOCK)  WHERE SAQICO.QUOTE_ID ='"+ str(Quote_ID) +"' AND SAQICO.QTEREV_ID ='"+ str(Revision_ID) + "'  ) t    ) A FOR XML PATH ('')  ), 1, 1, '')+']','amp;#','#') AS RESULT)A " )
            
            Tools = SqlHelper.GetFirst("SELECT CASE WHEN ISNULL(RESULT,'') = '' THEN '' ELSE RESULT END AS RESULT FROM (SELECT replace ('\"Tools\": ['+STUFF((SELECT ','+ JSON FROM (SELECT DISTINCT '{\"ToolId\" : \"'+ToolId+'\",\"ToolDescription\" : \"'+ToolDescription+'\",\"SerialID\" : \"'+SerialID+'\",\"CustomerToolID\" : \"'+CustomerToolID+'\",\"FabName\" : \"'+FabName+'\",\"FabID\" : \"'+FabID+'\",\"FabLocation\" : \"'+FabLocation+'\",\"GreenBook\" : \"'+GreenBook+'\",\"PLATFORM\" : \"'+PLATFORM+'\"}' AS JSON from (SELECT DISTINCT ISNULL(SAQICO.EQUIPMENT_ID,'') AS ToolId,ISNULL(EQUIPMENT_DESCRIPTION,'') AS ToolDescription, ISNULL(SERIAL_NO,'') AS SerialID, ISNULL(CUSTOMER_TOOL_ID,'') AS CustomerToolID,  ISNULL(FABLOCATION_NAME,'') AS FabName, ISNULL(GREENBOOK,'') AS GreenBook,ISNULL(PLATFORM,'') AS Platform,ISNULL(FABLOCATION_ID,'') AS FabID,ISNULL((SELECT TOP 1 ADDRESS_1 FROM MAFBLC(NOLOCK) WHERE  MAFBLC.FAB_LOCATION_ID = SAQICO.FABLOCATION_ID),'') AS FabLocation FROM SAQICO (NOLOCK)  WHERE SAQICO.QUOTE_ID ='"+ str(Quote_ID) +"' AND SAQICO.QTEREV_ID ='"+ str(Revision_ID) + "'  ) t    ) A FOR XML PATH ('')  ), 1, 1, '')+']','amp;#','#') AS RESULT)A " )


            ToolWorksheet = SqlHelper.GetFirst("SELECT CASE WHEN ISNULL(RESULT,'') = '' THEN '' ELSE RESULT END AS RESULT FROM (SELECT replace ('\"ToolWorksheet\": ['+STUFF((SELECT ','+ JSON FROM (SELECT DISTINCT '{\"ToolId\" : \"'+ToolId+'\",\"ServiceID\" : \"'+ServiceID+'\",\"ToolDescription\" : \"'+ToolDescription+'\",\"REgisteredProdctCatogory\" : \"'+REgisteredProdctCatogory+'\",\"DateFrom\" : \"'+DateFrom+'\",\"DateTo\" : \"'+DateTo+'\",\"Platform\" : \"'+Platform+'\",\"Greenbook\" : \"'+Greenbook+'\",\"Technology\" : \"'+Technology+'\",\"ProductOfferingName\" : \"'+ProductOfferingName+'\"}' AS JSON from (SELECT DISTINCT ISNULL(SAQICO.EQUIPMENT_ID,'') AS ToolId,ISNULL(SAQICO.SERVICE_ID,'') AS ServiceID,ISNULL(EQUIPMENT_DESCRIPTION,'') AS  ToolDescription ,ISNULL(EQUIPMENTCATEGORY_ID,'') AS REgisteredProdctCatogory, ISNULL(PLATFORM,'') AS Platform,ISNULL(GREENBOOK,'') AS Greenbook,ISNULL(TECHNOLOGY,'') AS Technology,ISNULL(SERVICE_DESCRIPTION,'') AS ProductOfferingName,ISNULL(CONVERT(VARCHAR(11),SAQICO.CONTRACT_VALID_FROM,101),'') AS DateFrom,ISNULL(CONVERT(VARCHAR(11),SAQICO.CONTRACT_VALID_TO,101),'') AS DateTo FROM SAQICO (NOLOCK)  WHERE SAQICO.QUOTE_ID ='"+ str(Quote_ID) +"' AND SAQICO.QTEREV_ID ='"+ str(Revision_ID) + "'  ) t    ) A FOR XML PATH ('')  ), 1, 1, '')+']','amp;#','#') AS RESULT)A " )
            
            ForcastWorksheet = SqlHelper.GetFirst("SELECT CASE WHEN ISNULL(RESULT,'') = '' THEN '' ELSE RESULT END AS RESULT FROM (SELECT replace ('\"ForcastWorksheet\": ['+STUFF((SELECT ','+ JSON FROM (SELECT DISTINCT '{\"GreenBook\" : \"'+GreenBook+'\",\"ServiceID\" : \"'+ServiceID+'\",\"ForcastValue\" : \"'+ForcastValue+'\",\"ProductOfferingName\" : \"'+ProductOfferingName+'\"}' AS JSON from (SELECT DISTINCT ISNULL(SAQRIT.GREENBOOK,'') AS GreenBook,ISNULL(SAQRIT.SERVICE_ID,'') AS ServiceID,CONVERT(VARCHAR,sum(ISNULL(SAQRIT.NET_VALUE,0))) AS ForcastValue,ISNULL(SERVICE_DESCRIPTION,'') AS ProductOfferingName FROM SAQRIT (NOLOCK)  WHERE SAQRIT.QUOTE_ID ='"+ str(Quote_ID) +"' AND SAQRIT.QTEREV_ID ='"+ str(Revision_ID) + "' GROUP BY SERVICE_ID,GREENBOOK,SERVICE_DESCRIPTION  ) t    ) A FOR XML PATH ('')  ), 1, 1, '')+']','amp;#','#') AS RESULT)A " )
            
            
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
            #Log.Info("6666--->"+str(final_json))
                
            Final_json = eval('{'+final_json[:-1]+'}')
            
            if len(Final_json)>0:       
            
                ApiResponse = ApiResponseFactory.JsonResponse(Final_json)  

            else:
                ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "200", "Message": "NO DATA AVAILABLE FOR SYNCHRONIZATION"}]})                
                            
except:
    Log.Info("SAGETQRPFV ERROR---->:" + str(sys.exc_info()[1]))
    Log.Info("SAGETQRPFV ERROR LINE NO---->:" + str(sys.exc_info()[-1].tb_lineno))
    ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "400", "Message": str(sys.exc_info()[1])}]})
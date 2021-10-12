# =========================================================================================================================================
#   __script_name : SAGETQRPFV.PY
#   __script_description : THIS SCRIPT IS RECEIVED C4C DATA  AND SEND TO C4C SYSTEM
#   __primary_author__ : BAJI
#   __create_date :
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
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
               
            
            Opportunity = SqlHelper.GetFirst("SELECT CASE WHEN ISNULL(RESULT,'') = '' THEN '' ELSE RESULT END AS RESULT FROM (SELECT replace ('\"Opportunity\": ['+STUFF((SELECT ','+ JSON FROM (SELECT DISTINCT '{\"OppID\" : \"'+OppID+'\",\"ExpectedBookingDate\" : \"'+ExpectedBookingDate+'\",\"ContractValidFrom\" : \"'+ContractValidFrom+'\",\"ContractValidTo\" : \"'+ContractValidTo+'\"}' AS JSON from (SELECT DISTINCT ISNULL(SAQTMT.QUOTE_ID,'') AS OppID,ISNULL(CONVERT(VARCHAR(11),SAQTMT.QUOTE_CREATED_DATE,101),'') AS ExpectedBookingDate,ISNULL(CONVERT(VARCHAR(11),SAQTMT.CONTRACT_VALID_FROM,101),'') AS ContractValidFrom,ISNULL(CONVERT(VARCHAR(11),SAQTMT.CONTRACT_VALID_TO,101),'') AS ContractValidTo FROM SAQTMT (NOLOCK)  WHERE SAQTMT.QUOTE_ID ='"+ str(Quote_ID) +"' AND SAQTMT.QTEREV_ID ='"+ str(Revision_ID) + "'  ) t    ) A FOR XML PATH ('')  ), 1, 1, '')+']','amp;#','#') AS RESULT)A " )
            
        
            Fab = SqlHelper.GetFirst("SELECT CASE WHEN ISNULL(RESULT,'') = '' THEN '' ELSE RESULT END AS RESULT FROM (SELECT replace ('\"Fab\": ['+STUFF((SELECT ','+ JSON FROM (SELECT DISTINCT '{\"FabID\" : \"'+FabID+'\"}' AS JSON from (SELECT DISTINCT ISNULL(SAQICO.FABLOCATION_ID,'') AS FabID FROM SAQICO (NOLOCK)  WHERE SAQICO.QUOTE_ID ='"+ str(Quote_ID) +"' AND SAQICO.QTEREV_ID ='"+ str(Revision_ID) + "'  ) t    ) A FOR XML PATH ('')  ), 1, 1, '')+']','amp;#','#') AS RESULT)A " )
            
            ProductOffering = SqlHelper.GetFirst("SELECT CASE WHEN ISNULL(RESULT,'') = '' THEN '' ELSE RESULT END AS RESULT FROM (SELECT replace ('\"ProductOffering\": ['+STUFF((SELECT ','+ JSON FROM (SELECT DISTINCT '{\"ServiceID\" : \"'+ServiceID+'\",\"RevenueStartDate\" : \"'+RevenueStartDate+'\",\"RevenueEndDate\" : \"'+RevenueEndDate+'\"}' AS JSON from (SELECT DISTINCT ISNULL(SAQICO.SERVICE_ID,'') AS ServiceID,ISNULL(CONVERT(VARCHAR(11),SAQICO.CONTRACT_VALID_FROM,101),'') AS RevenueStartDate,ISNULL(CONVERT(VARCHAR(11),SAQICO.CONTRACT_VALID_TO,101),'') AS RevenueEndDate FROM SAQICO (NOLOCK)  WHERE SAQICO.QUOTE_ID ='"+ str(Quote_ID) +"' AND SAQICO.QTEREV_ID ='"+ str(Revision_ID) + "'  ) t    ) A FOR XML PATH ('')  ), 1, 1, '')+']','amp;#','#') AS RESULT)A " )
            
            Tools = SqlHelper.GetFirst("SELECT CASE WHEN ISNULL(RESULT,'') = '' THEN '' ELSE RESULT END AS RESULT FROM (SELECT replace ('\"Tools\": ['+STUFF((SELECT ','+ JSON FROM (SELECT DISTINCT '{\"ToolId\" : \"'+ToolId+'\"}' AS JSON from (SELECT DISTINCT ISNULL(SAQICO.EQUIPMENT_ID,'') AS ToolId FROM SAQICO (NOLOCK)  WHERE SAQICO.QUOTE_ID ='"+ str(Quote_ID) +"' AND SAQICO.QTEREV_ID ='"+ str(Revision_ID) + "'  ) t    ) A FOR XML PATH ('')  ), 1, 1, '')+']','amp;#','#') AS RESULT)A " )


            ToolWorksheet = SqlHelper.GetFirst("SELECT CASE WHEN ISNULL(RESULT,'') = '' THEN '' ELSE RESULT END AS RESULT FROM (SELECT replace ('\"ToolWorksheet\": ['+STUFF((SELECT ','+ JSON FROM (SELECT DISTINCT '{\"ToolId\" : \"'+ToolId+'\",\"ServiceID\" : \"'+ServiceID+'\"}' AS JSON from (SELECT DISTINCT ISNULL(SAQICO.EQUIPMENT_ID,'') AS ToolId,ISNULL(SAQICO.SERVICE_ID,'') AS ServiceID FROM SAQICO (NOLOCK)  WHERE SAQICO.QUOTE_ID ='"+ str(Quote_ID) +"' AND SAQICO.QTEREV_ID ='"+ str(Revision_ID) + "'  ) t    ) A FOR XML PATH ('')  ), 1, 1, '')+']','amp;#','#') AS RESULT)A " )
            
            ForcastWorksheet = SqlHelper.GetFirst("SELECT CASE WHEN ISNULL(RESULT,'') = '' THEN '' ELSE RESULT END AS RESULT FROM (SELECT replace ('\"ForcastWorksheet\": ['+STUFF((SELECT ','+ JSON FROM (SELECT DISTINCT '{\"GreenBook\" : \"'+GreenBook+'\",\"ServiceID\" : \"'+ServiceID+'\",\"ForcastValue\" : \"'+ForcastValue+'\"}' AS JSON from (SELECT DISTINCT ISNULL(SAQICO.GREENBOOK,'') AS GreenBook,ISNULL(SAQICO.SERVICE_ID,'') AS ServiceID,ISNULL(CONVERT(VARCHAR,SAQICO.NET_VALUE),'') AS ForcastValue FROM SAQICO (NOLOCK)  WHERE SAQICO.QUOTE_ID ='"+ str(Quote_ID) +"' AND SAQICO.QTEREV_ID ='"+ str(Revision_ID) + "'  ) t    ) A FOR XML PATH ('')  ), 1, 1, '')+']','amp;#','#') AS RESULT)A " )
            
            
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
                
            Final_json = '{'+final_json[:-1]+'}'
            
            if len(Final_json)>0:       
            
                ApiResponse = ApiResponseFactory.JsonResponse(Final_json)  

            else:
                ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "200", "Message": "NO DATA AVAILABLE FOR SYNCHRONIZATION"}]})                
                            
except:
    Log.Info("SAGETQRPFV ERROR---->:" + str(sys.exc_info()[1]))
    Log.Info("SAGETQRPFV ERROR LINE NO---->:" + str(sys.exc_info()[-1].tb_lineno))
    ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "400", "Message": str(sys.exc_info()[1])}]})
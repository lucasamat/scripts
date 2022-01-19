# =========================================================================================================================================
#   __script_name : SAPOSTCLMA.PY
#   __script_description : THIS SCRIPT IS USED FOR CPQ TO CLM INTEGRATIONS
#   __primary_author__ : BAJI
#   __create_date :
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import sys
import clr
import System.Net
from System.Text.Encoding import UTF8
from System import Convert
from System.Net import HttpWebRequest, NetworkCredential
from System.Net import *
from System.Net import CookieContainer
from System.Net import Cookie
from System.Net import WebRequest
from System.Net import HttpWebResponse

try:
	Quote_Id = Param.QUOTE_ID #'3050000339'
	Revision_Id = Param.REVISION_ID #'0'

	CLMQuery = SqlHelper.GetList("SELECT DISTINCT top 1 ISNULL(SAQTRV.CLM_CONTRACT_TYPE,'') AS ContractTypeName,ISNULL(SAQTRV.CLM_TEMPLATE_NAME,'') AS StatementOfWorkType,ISNULL(CASE WHEN SAQTRV.HLV_ORG_BUN='AGS - SSC' THEN '004' ELSE NULL END,'') AS HighLevelOrg,ISNULL((SELECT REPLICATE('0',(10-LEN(ACCOUNT_ID)))+ACCOUNT_ID FROM SAQTMT(NOLOCK) WHERE QUOTE_ID = '"+str(Quote_Id)+"' AND QTEREV_ID = '"+str(Revision_Id)+"'  ),'') AS SAPOtherPartyID,ISNULL(SAQTRV.COMPANY_NAME,'') AS AppliedPartyName,ISNULL((SELECT OWNER_NAME FROM SAQTMT(NOLOCK) WHERE QUOTE_ID = '"+str(Quote_Id)+"' AND QTEREV_ID = '"+str(Revision_Id)+"'  ),'') AS CPQContractInitiator,ISNULL(SAQTRV.APPLIED_EMAIL,'test@gmail.com') AS  AppliedSignatory1Email,ISNULL(SAQTRV.APPLIED_TITLE,'test') AS AppliedSignatoryTitle,ISNULL(SAQTRV.EXTERNAL_EMAIL,'test@gmail.com') AS ExternalSignatory1Email,ISNULL(SAQTRV.EXTERNAL_TITLE,'test') AS OtherPartySignatoryTitle,ISNULL(CONVERT(VARCHAR,SAQTRV.NET_VALUE_INGL_CURR),'0') AS ExpectedValue,ISNULL(SAQTRV.GLOBAL_CURRENCY,'') AS ExpectedValueCurrency,ISNULL(SAQTRV.CUSTOMER_NOTES,'test') AS Comments,ISNULL(CONVERT(VARCHAR,SAQTRV.CONTRACT_VALID_TO),'') AS ContractExpirationDate,SAQTRV.QUOTE_ID +'-'+CONVERT(VARCHAR,SAQTRV.QTEREV_ID) AS CorrelationID,'CPQ Quote#'+SAQTRV.QUOTE_ID +'-'+CONVERT(VARCHAR,SAQTRV.QTEREV_ID) AS AgreementName,ISNULL(OPPORTUNITY_ID,'') AS OpportunityNumber,CONVERT(VARCHAR(11),CONTRACT_VALID_FROM,121) AS ContractEffectiveDate  FROM SAQTRV(NOLOCK) JOIN SAOPQT (NOLOCK) on SAQTRV.QUOTE_ID = SAOPQT.QUOTE_ID WHERE SAQTRV.QTEREV_ID = '"+str(Revision_Id)+"' AND SAQTRV.QUOTE_ID = '"+str(Quote_Id)+"'")

	dt={}  

	for data in CLMQuery:
	
		dt['ContractTypeName'] = data.StatementOfWorkType
		dt['StatementOfWorkType'] = data.StatementOfWorkType
		dt['CorrelationID'] = data.CorrelationID
		dt['HighLevelOrg-BUID'] = data.HighLevelOrg	
		dt['AppliedPartyName'] = data.AppliedPartyName
		dt['SAPOtherPartyID'] = data.SAPOtherPartyID
		dt['CPQContractInitiator'] = data.CPQContractInitiator
		dt['QuotationNumber'] = Quote_Id
		dt['QuoteRevision'] = Revision_Id
		dt['OpportunityNumber'] = data.OpportunityNumber
		dt['AppliedSignatory1Email'] = data.AppliedSignatory1Email
		dt['AppliedSignatoryTitle'] = data.AppliedSignatoryTitle
		dt['ExternalSignatory1Email'] = data.ExternalSignatory1Email
		dt['OtherPartySignatoryTitle'] = data.OtherPartySignatoryTitle
		dt['ExpectedValue(USDonly)'] = data.ExpectedValue
		dt['ExpectedValueCurrency'] = data.ExpectedValueCurrency	
		dt['AgreementName'] = data.AgreementName
		dt['Comments'] = data.Comments
		dt['ContractExpirationDate'] = data.ContractExpirationDate
		dt['ContractEffectiveDate'] = data.ContractEffectiveDate
		
	Timestamp = SqlHelper.GetFirst("select Getdate() as date")
	result = {

	  "EventType": "Agreement",
	  "Action": "Create",
	  "TimeStamp": str(Timestamp.date),
	  "Data":dt}
	Result = result
	#Log.Info("22222 result --->"+str(result))
	LOGIN_CRE = SqlHelper.GetFirst("SELECT  URL FROM SYCONF where EXTERNAL_TABLE_NAME ='CPQ_TO_CLM'")
	Oauth_info = SqlHelper.GetFirst("SELECT  DOMAIN,URL FROM SYCONF where EXTERNAL_TABLE_NAME ='OAUTH'")

	requestdata =Oauth_info.DOMAIN
	webclient = System.Net.WebClient()
	webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/x-www-form-urlencoded"
	response = webclient.UploadString(Oauth_info.URL,str(requestdata))

	response = eval(response)
	access_token = response['access_token']

	authorization = "Bearer " + access_token
	webclient = System.Net.WebClient()
	webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/json"
	webclient.Headers[System.Net.HttpRequestHeader.Authorization] = authorization;	
	clm_response = webclient.UploadString(str(LOGIN_CRE.URL),str(result))	
	Log.Info("28/12 clm_response --->"+str(clm_response))
except:
    Log.Info("SAPOSTCLMA ERROR---->:" + str(sys.exc_info()[1]))
    Log.Info("SAPOSTCLMA ERROR LINE NO---->:" + str(sys.exc_info()[-1].tb_lineno))
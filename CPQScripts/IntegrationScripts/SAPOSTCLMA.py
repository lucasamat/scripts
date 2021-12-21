# =========================================================================================================================================
#   __script_name : SAPOSTCLMA.PY
#   __script_description : THIS SCRIPT IS USED FOR CPQ TO CLM INTEGRATIONS
#   __primary_author__ : BAJI
#   __create_date :
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================

try:
	Quote_Id = Param.QUOTE_ID #'3050000339'
	Revision_Id = Param.REVISION_ID #'0'

	CLMQuery = SqlHelper.GetList("SELECT DISTINCT top 1 ISNULL(SAQTRV.CLM_CONTRACT_TYPE,'') AS ContractTypeName,ISNULL(SAQTRV.CLM_TEMPLATE_NAME,'') AS StatementOfWorkType,ISNULL(SAQTRV.HLV_ORG_BUN,'') AS HighLevelOrg,ISNULL(SAQTRV.APPLIED_NAME,'') AS AppliedPartyName,ISNULL(SAQTRV.COMPANY_ID,'') AS SAPOtherPartyID,ISNULL(SAQTRV.CLM_AGREEMENT_OWNER,'') AS CPQContractInitiator,ISNULL(SAQTRV.APPLIED_EMAIL,'') AS  AppliedSignatory1Email,ISNULL(SAQTRV.APPLIED_TITLE,'') AS AppliedSignatoryTitle,ISNULL(SAQTRV.EXTERNAL_EMAIL,'') AS ExternalSignatory1Email,ISNULL(SAQTRV.EXTERNAL_TITLE,'') AS OtherPartySignatoryTitle,ISNULL(CONVERT(VARCHAR,SAQTRV.NET_VALUE_INGL_CURR),'') AS ExpectedValue,ISNULL(SAQTRV.GLOBAL_CURRENCY,'') AS ExpectedValueCurrency,ISNULL(SAQTRV.CUSTOMER_NOTES,'') AS Comments,ISNULL(CONVERT(VARCHAR,SAQTRV.CONTRACT_VALID_TO),'') AS ContractExpirationDate,ISNULL(SAQTSV.SERVICE_ID,'') AS ProductOffering FROM SAQTRV(NOLOCK) JOIN SAQTSV(NOLOCK) ON SAQTRV.QUOTE_ID = '"+str(Quote_Id)+"' AND SAQTRV.QTEREV_ID = '"+str(Revision_Id)+"' AND SAQTSV.QUOTE_ID = '"+str(Quote_Id)+"'")

	dt={}  

	for data in CLMQuery:

		dt['ContractTypeName'] = data.ContractTypeName
		dt['StatementOfWorkType'] = data.StatementOfWorkType
		dt['CorrelationID'] = ''
		dt['HighLevelOrg-BUID'] = data.HighLevelOrg	
		dt['AppliedPartyName'] = data.AppliedPartyName
		dt['SAPOtherPartyID'] = data.SAPOtherPartyID
		dt['CPQContractInitiator'] = data.CPQContractInitiator
		dt['QuotationNumber'] = Quote_Id
		dt['QuoteRevision'] = Revision_Id
		dt['OpportunityNumber'] = ''
		dt['AppliedSignatory1Email'] = data.AppliedSignatory1Email
		dt['AppliedSignatoryTitle'] = data.AppliedSignatoryTitle
		dt['ExternalSignatory1Email'] = data.ExternalSignatory1Email
		dt['OtherPartySignatoryTitle'] = data.OtherPartySignatoryTitle
		dt['ExpectedValue(USDonly)'] = data.ExpectedValue
		dt['ExpectedValueCurrency'] = data.ExpectedValueCurrency	
		dt['AgreementName'] = ''
		dt['Comments'] = data.Comments
		dt['ContractExpirationDate'] = data.ContractExpirationDate
		dt['ContractEffectiveDate'] = ''
		dt['LegalPerson'] = ''


	result = {

	  "EventType": "Agreement",
	  "Action": "Create",
	  "TimeStamp": "2021-11-21T06:06:33",
	  "CorrelationID" : "",
	  "Data":dt}
	Result = result
	Log.Info("22222 result --->"+str(result))
except:
    Log.Info("SAPOSTCLMA ERROR---->:" + str(sys.exc_info()[1]))
    Log.Info("SAPOSTCLMA ERROR LINE NO---->:" + str(sys.exc_info()[-1].tb_lineno)) 
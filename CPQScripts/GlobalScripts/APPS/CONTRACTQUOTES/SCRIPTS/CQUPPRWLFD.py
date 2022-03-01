# =========================================================================================================================================
#   __script_name : CQUPPRWLFD.PY
#   __script_description : THIS SCRIPT IS USED TO UPDATE PRICING FIELDS IN ANNUALIZED ITEMS(WATERFALL)
#   __primary_author__ : AYYAPPAN SUBRAMANIYAN
#   __create_date :01-03-2021
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED -
# ==========================================================================================================================================

import datetime
from SYDATABASE import SQL

Sql = SQL()
Parameter1 = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'UPD' ")

class ContractQuoteItemAnnualizedPricing:
	def __init__(self, **kwargs):		
		self.user_id = str(User.Id)
		self.user_name = str(User.UserName)		
		self.datetime_value = datetime.datetime.now()
		self.contract_quote_record_id = kwargs.get('contract_quote_record_id')
		self.contract_quote_revision_record_id = kwargs.get('contract_quote_revision_record_id')
		self.records = kwargs.get('records')
		
	
	def _do_process(self):
		if self.records:
			self.records = eval(self.records)			
			for data in self.records:
				for line_id, value in data.items():					
					update_fields_str = ' ,'.join(["{} = {}".format(field_name,field_value if field_value else 0) for field_name, field_value in value.items()])					

					Sql.RunQuery("""UPDATE SAQICO
							SET {UpdateFields}	
							FROM SAQICO (NOLOCK)							
							WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.LINE_ID = '{LineId}'""".format(UpdateFields=update_fields_str, QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, LineId=line_id))
					if 'ADDCOF' in update_fields_str:
						self._rolldown_from_coeff_level(line_id)
					else:
						self._rolldown_from_total_price_level(line_id)

	def _rolldown_from_coeff_level(self, line_id = None):
		#SUMCOF - Sum of All Coefficient
		Sql.RunQuery("UPDATE SAQICO SET SUMCOF = ISNULL(INTCPC,0) + ISNULL(LTCOSS,0) + ISNULL(POFVDC,0) + ISNULL(GBKVDC,0) + ISNULL(UIMVDC,0) + ISNULL(CAVVDC,0) + ISNULL(WNDVDC,0) + ISNULL(SCMVDC,0) + ISNULL(CCDFFC,0) + ISNULL(NPIVDC,0) + ISNULL(DTPVDC,0) + ISNULL(CSTVDC,0) + ISNULL(CSGVDC,0) + ISNULL(QRQVDC,0) + ISNULL(SVCVDC,0) + ISNULL(RKFVDC,0) + ISNULL(PBPVDC,0) + ISNULL(ADDCOF,0) FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND LINE_ID = '{LineId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, LineId=line_id))
					
		#INMP01 - Intermediate Model Price 1
		Sql.RunQuery("UPDATE SAQICO SET INMP01 = EXP(SUMCOF) FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND LINE_ID = '{LineId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, LineId=line_id))
			
		#INMP02 / FNMDPR - Intermediate Model Price 2 /  Final Model Price
		Sql.RunQuery("UPDATE SAQICO SET INMP02 = INMP01 * (1 + ISNULL(CCRTMC,0)), FNMDPR = INMP01 * (1 + ISNULL(CCRTMC,0)) FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND LINE_ID = '{LineId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, LineId=line_id))
		
		#FNMDPR - Final Model Price (Z0100 / Z0101)
		Sql.RunQuery("UPDATE SAQICO SET CNSM_MARGIN_PERCENT = SABGMR.CNSM_MARGIN_PERCENT FROM SAQICO (NOLOCK) JOIN SABGMR (NOLOCK) ON SAQICO.GREENBOOK = SABGMR.GREENBOOK AND SAQICO.BLUEBOOK = SABGMR.BLUEBOOK WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND LINE_ID = '{LineId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, LineId=line_id))
		
		Sql.RunQuery("UPDATE SAQICO SET CNSM_MARGIN_PERCENT = SABGMR.CNSM_MARGIN_PERCENT FROM SAQICO_INBOUND(NOLOCK) JOIN SABGMR (NOLOCK) ON SAQICO.GREENBOOK = SABGMR.GREENBOOK AND SAQICO.REGION = SABGMR.REGION WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND LINE_ID = '{LineId}' AND SAQICO.CNSM_MARGIN_PERCENT IS NULL'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, LineId=line_id))
		
		Sql.RunQuery("UPDATE SAQICO SET FNMDPR =  TCWISS / (1 - (CNSM_MARGIN_PERCENT/100)), MTGPRC =  TCWISS / (1 - (CNSM_MARGIN_PERCENT/100)), MSLPRC =  TCWISS / (1 - (CNSM_MARGIN_PERCENT/100)), MBDPRC =  TCWISS / (1 - (CNSM_MARGIN_PERCENT/100)), MCLPRC =  TCWISS / (1 - (CNSM_MARGIN_PERCENT/100)) ,CNTCST = TCWISS, CNTPRC = TCWISS / (1 - (CNSM_MARGIN_PERCENT/100)) FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND LINE_ID = '{LineId}' AND ISNULL(TCWISS,0)>0 AND SERVICE_ID IN ('Z0100','Z0101')".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, LineId=line_id))
		
		#MTGPRC - Target Model Price
		Sql.RunQuery("UPDATE SAQICO SET MTGPRC = CASE WHEN ISNULL(FNMDPR/(1-(CONVERT(FLOAT,SADSPC)/100)),0) > ISNULL(TCWISS / (1-(TAPMMP/100)),0) THEN ISNULL(FNMDPR/(1-(CONVERT(FLOAT,SADSPC)/100)),0) ELSE ISNULL(TCWISS / (1-(TAPMMP/100)),0) END FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND LINE_ID = '{LineId}' AND SERVICE_ID NOT IN ('Z0100','Z0101')".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, LineId=line_id))
		
		#MSLPRC - Sales Model Price
		Sql.RunQuery("UPDATE SAQICO SET MSLPRC = CASE WHEN ISNULL(FNMDPR,0) > ISNULL(TCWISS / (1-(CONVERT(FLOAT,SAPMMP)/100)),0) THEN ISNULL(FNMDPR,0) ELSE ISNULL(TCWISS / (1-(CONVERT(FLOAT,SAPMMP)/100)),0) END FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND LINE_ID = '{LineId}' AND SERVICE_ID NOT IN ('Z0100','Z0101')".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, LineId=line_id))
		
		#MBDPRC - BD Model Price
		Sql.RunQuery("UPDATE SAQICO SET MBDPRC = CASE WHEN ISNULL(FNMDPR * (1-(CONVERT(FLOAT,BDDSPC)/100)) ,0) > ISNULL(TCWISS / (1-(CONVERT(FLOAT,BDPMMP)/100)),0) THEN ISNULL(FNMDPR * (1-(CONVERT(FLOAT,BDDSPC)/100)) ,0) ELSE ISNULL(TCWISS / (1-(CONVERT(FLOAT,BDPMMP)/100)),0) END FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND LINE_ID = '{LineId}' AND SERVICE_ID NOT IN ('Z0100','Z0101')".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, LineId=line_id))
		
		#MCLPRC - Ceiling Model Price
		Sql.RunQuery("UPDATE SAQICO SET MCLPRC = MTGPRC * (1 + ISNULL(CEPRUP/100,0)) FROM SAQICO A(NOLOCK) JOIN (SELECT  DISTINCT QUOTE_ID,SERVICE_ID,REVISION_ID,LINE FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND LINE_ID = '{LineId}' AND SERVICE_ID NOT IN (''Z0100'',''Z0101'') ' ".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, LineId=line_id))		
		
	def _rolldown_from_total_price_level(self):
		#TOTLCI - Total Cost Impact
		primaryQueryItems = SqlHelper.GetFirst(
			""
			+ str(Parameter1.QUERY_CRITERIA_1)
			+ "  A SET TOTLCI = ISNULL(CAVVCI,0) + ISNULL(UIMVCI,0) + ISNULL(ATGKEC,0) + ISNULL(AMNCCI,0) + ISNULL(HEDBIC,0) + ISNULL(NWPTOC,0) + ISNULL(NUMLCI,0) + ISNULL(SPCCLC,0) + ISNULL(SPCCCI,0) FROM SAQICO A(NOLOCK) JOIN (SELECT  DISTINCT QUOTE_ID,SERVICE_ID,REVISION_ID,LINE  FROM SAQICO_INBOUND B(NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.QTEREV_ID = B.REVISION_ID AND A.LINE = B.LINE  ' ")
		
		#TOTLPI - Total Price Impact
		primaryQueryItems = SqlHelper.GetFirst(
			""
			+ str(Parameter1.QUERY_CRITERIA_1)
			+ "  A SET TOTLPI = ISNULL(ATGKEP,0) + ISNULL(AMNPPI,0) + ISNULL(CAVVPI,0) + ISNULL(HEDBIP,0) + ISNULL(NWPTOP,0) + ISNULL(NUMLPI,0) + ISNULL(SPCCLP,0) + ISNULL(SPCCPI,0) + ISNULL(UIMVPI,0) FROM SAQICO A(NOLOCK) JOIN (SELECT  DISTINCT QUOTE_ID,SERVICE_ID,REVISION_ID,LINE  FROM SAQICO_INBOUND B(NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.QTEREV_ID = B.REVISION_ID AND A.LINE = B.LINE  ' ")
		
		#FCWOSS - Final Total Cost without Seedstock
		primaryQueryItems = SqlHelper.GetFirst(
			""
			+ str(Parameter1.QUERY_CRITERIA_1)
			+ "  A SET FCWOSS = ISNULL(TCWOSS,0) + ISNULL(TOTLCI,0) FROM SAQICO A(NOLOCK) JOIN (SELECT  DISTINCT QUOTE_ID,SERVICE_ID,REVISION_ID,LINE  FROM SAQICO_INBOUND B(NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.QTEREV_ID = B.REVISION_ID AND A.LINE = B.LINE  ' ")
		
		#FCWISS - Final Total Cost with Seedstock
		primaryQueryItems = SqlHelper.GetFirst(
			""
			+ str(Parameter1.QUERY_CRITERIA_1)
			+ "  A SET FCWISS = ISNULL(TCWISS,0) + ISNULL(TOTLCI,0) FROM SAQICO A(NOLOCK) JOIN (SELECT  DISTINCT QUOTE_ID,SERVICE_ID,REVISION_ID,LINE  FROM SAQICO_INBOUND B(NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.QTEREV_ID = B.REVISION_ID AND A.LINE = B.LINE  ' ")
		
		#TRGPRC /SLSPRC / BDVPRC /CELPRC - Target / Sales / BD / Ceiling Price
		primaryQueryItems = SqlHelper.GetFirst(
			""
			+ str(Parameter1.QUERY_CRITERIA_1)
			+ "  A SET TRGPRC = ISNULL(MTGPRC,0) + ISNULL(TOTLPI,0), SLSPRC = ISNULL(MSLPRC,0) + ISNULL(TOTLPI,0), BDVPRC = ISNULL(MBDPRC,0) + ISNULL(TOTLPI,0), CELPRC = ISNULL(MCLPRC,0) + ISNULL(TOTLPI,0)  FROM SAQICO A(NOLOCK) JOIN (SELECT  DISTINCT QUOTE_ID,SERVICE_ID,REVISION_ID,LINE  FROM SAQICO_INBOUND B(NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.QTEREV_ID = B.REVISION_ID AND A.LINE = B.LINE  ' ")
		
		#USRPRC / TGADJP - User Price / Target User Price Adjustment
		primaryQueryItems = SqlHelper.GetFirst(
			""
			+ str(Parameter1.QUERY_CRITERIA_1)
			+ "  A SET USRPRC = TRGPRC,TGADJP = ''0.00'' FROM SAQICO A(NOLOCK) JOIN (SELECT  DISTINCT QUOTE_ID,SERVICE_ID,REVISION_ID,LINE  FROM SAQICO_INBOUND B(NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.QTEREV_ID = B.REVISION_ID AND A.LINE = B.LINE  ' ")
		
		#CNTPRC - Contractual Price
		primaryQueryItems = SqlHelper.GetFirst(
			""
			+ str(Parameter1.QUERY_CRITERIA_1)
			+ "  A SET CNTPRC = ((USRPRC / 365) * CNTDAY * ISNULL(CTPDFP ,1) ) * (1 - (ISNULL(YOYPCT,0)/100))  FROM SAQICO A(NOLOCK) JOIN (SELECT  DISTINCT QUOTE_ID,SERVICE_ID,REVISION_ID,LINE  FROM SAQICO_INBOUND B(NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID  AND A.QTEREV_ID = B.REVISION_ID AND A.LINE = B.LINE WHERE A.SERVICE_ID NOT IN (''Z0100'',''Z0101'')  ' ")
		
		#CNTCST - Contractual Cost
		primaryQueryItems = SqlHelper.GetFirst(
			""
			+ str(Parameter1.QUERY_CRITERIA_1)
			+ "  A SET CNTCST = ((FCWISS / 365) * CNTDAY )  FROM SAQICO A(NOLOCK) JOIN (SELECT  DISTINCT QUOTE_ID,SERVICE_ID,REVISION_ID,LINE  FROM SAQICO_INBOUND B(NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.QTEREV_ID = B.REVISION_ID AND A.LINE = B.LINE WHERE A.SERVICE_ID NOT IN (''Z0100'',''Z0101'') ' ")
		
		#CNTMGN - Contractual Margin
		primaryQueryItems = SqlHelper.GetFirst(
			""
			+ str(Parameter1.QUERY_CRITERIA_1)
			+ "  A SET CNTMGN = CNTPRC - CNTCST FROM SAQICO A(NOLOCK) JOIN (SELECT  DISTINCT QUOTE_ID,SERVICE_ID,REVISION_ID,LINE  FROM SAQICO_INBOUND B(NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.QTEREV_ID = B.REVISION_ID AND A.LINE = B.LINE WHERE A.SERVICE_ID NOT IN (''Z0100'',''Z0101'') ' ")
		
		#SPCTPR /SPCTCS - Spares Contractual Price / Cost
		primaryQueryItems = SqlHelper.GetFirst(
			""
			+ str(Parameter1.QUERY_CRITERIA_1)
			+ "  A SET SPCTPR = CNTPRC * SPSPCT, SPCTCS = CNTCST * SPSPCT FROM SAQICO A(NOLOCK) JOIN (SELECT  DISTINCT QUOTE_ID,SERVICE_ID,REVISION_ID,LINE  FROM SAQICO_INBOUND B(NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.QTEREV_ID = B.REVISION_ID AND A.LINE = B.LINE  ' ")
			
		#SPCTMG - Spares Contractual Margin
		primaryQueryItems = SqlHelper.GetFirst(
			""
			+ str(Parameter1.QUERY_CRITERIA_1)
			+ "  A SET SPCTMG = (SPCTPR - SPCTCS) / SPCTPR FROM SAQICO A(NOLOCK) JOIN (SELECT  DISTINCT QUOTE_ID,SERVICE_ID,REVISION_ID,LINE  FROM SAQICO_INBOUND B(NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.QTEREV_ID = B.REVISION_ID AND A.LINE = B.LINE  ' ")
		
		#SVCTPR /SVCTCS - Service Contractual Price / Cost
		primaryQueryItems = SqlHelper.GetFirst(
			""
			+ str(Parameter1.QUERY_CRITERIA_1)
			+ "  A SET SVCTPR = CNTPRC * SVSPCT, SVCTCS = CNTCST * SVSPCT FROM SAQICO A(NOLOCK) JOIN (SELECT  DISTINCT QUOTE_ID,SERVICE_ID,REVISION_ID,LINE  FROM SAQICO_INBOUND B(NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID  AND A.QTEREV_ID = B.REVISION_ID AND A.LINE = B.LINE  ' ")
		
		#SVCTMG - Service Contractual Margin
		primaryQueryItems = SqlHelper.GetFirst(
			""
			+ str(Parameter1.QUERY_CRITERIA_1)
			+ "  A SET SVCTMG = (SVCTPR - SVCTCS) / SVCTPR FROM SAQICO A(NOLOCK) JOIN (SELECT  DISTINCT QUOTE_ID,SERVICE_ID,REVISION_ID,LINE  FROM SAQICO_INBOUND B(NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.QTEREV_ID = B.REVISION_ID AND A.LINE = B.LINE  ' ")
		
		#TNTVGC / TNTMGC / TNTMPC - Total Net Value / Total Net Value in Margin / Margin % (Global Currency) 
		primaryQueryItems = SqlHelper.GetFirst(
			""
			+ str(Parameter1.QUERY_CRITERIA_1)
			+ "  A SET TNTVGC = CNTPRC , TNTMGC = CNTPRC - CNTCST, TNTMPC = (CNTPRC - CNTCST) / CNTPRC FROM SAQICO A(NOLOCK) JOIN (SELECT  DISTINCT QUOTE_ID,SERVICE_ID,REVISION_ID,LINE  FROM SAQICO_INBOUND B(NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.QTEREV_ID = B.REVISION_ID AND A.LINE = B.LINE WHERE A.BILTYP <> ''VARIABLE'' AND ISNULL(CNTPRC,0)>0 ' ")
		
		#TENVGC - Estimated Value (Global Currency)
		primaryQueryItems = SqlHelper.GetFirst(
			""
			+ str(Parameter1.QUERY_CRITERIA_1)
			+ "  A SET TENVGC = CNTPRC , TNTMGC = CNTPRC - CNTCST FROM SAQICO A(NOLOCK) JOIN (SELECT  DISTINCT QUOTE_ID,SERVICE_ID,REVISION_ID,LINE  FROM SAQICO_INBOUND B(NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID  AND A.QTEREV_ID = B.REVISION_ID AND A.LINE = B.LINE WHERE A.BILTYP = ''VARIABLE'' ' ")
			
		#TAXVGC - Tax Amount (Global Currency) 
		primaryQueryItems = SqlHelper.GetFirst(
			""
			+ str(Parameter1.QUERY_CRITERIA_1)
			+ "  A SET TAXVGC = TNTVGC * (ISNULL(TAXVTP,0)/100) FROM SAQICO A(NOLOCK) JOIN (SELECT  DISTINCT QUOTE_ID,SERVICE_ID,REVISION_ID,LINE  FROM SAQICO_INBOUND B(NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.QTEREV_ID = B.REVISION_ID AND A.LINE = B.LINE ' ")
		
		#TAMTGC - Total Amount (Global Currency) 
		primaryQueryItems = SqlHelper.GetFirst(
			""
			+ str(Parameter1.QUERY_CRITERIA_1)
			+ "  A SET TAMTGC = TNTVGC + ISNULL(TAXVGC,0) FROM SAQICO A(NOLOCK) JOIN (SELECT  DISTINCT QUOTE_ID,SERVICE_ID,REVISION_ID,LINE  FROM SAQICO_INBOUND B(NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.QTEREV_ID = B.REVISION_ID AND A.LINE = B.LINE ' ")
		
		#Round Off
		primaryQueryItems = SqlHelper.GetFirst(
			""
			+ str(Parameter1.QUERY_CRITERIA_1)
			+ "  A SET TAMTGC = ROUND(TAMTGC ,CONVERT(INT,"+str(roundcurr.DECIMAL_PLACES)+"),CONVERT(INT,"+str(roundcurr.ROUNDING_METHOD)+")), TAXVGC = ROUND(TAXVGC ,CONVERT(INT,"+str(roundcurr.DECIMAL_PLACES)+"),CONVERT(INT,"+str(roundcurr.ROUNDING_METHOD)+")), TNTVGC = ROUND(TNTVGC ,CONVERT(INT,"+str(roundcurr.DECIMAL_PLACES)+"),CONVERT(INT,"+str(roundcurr.ROUNDING_METHOD)+")) FROM SAQICO A(NOLOCK) JOIN (SELECT  DISTINCT QUOTE_ID,SERVICE_ID,REVISION_ID,LINE  FROM SAQICO_INBOUND B(NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.QTEREV_ID = B.REVISION_ID AND A.LINE = B.LINE ' ")
		
		#TNTVDC / TAXVDC / TAMTDC /TENVDC - Total Net Value / Tax / Total Amount/ Estimated (Document Currency) 
		primaryQueryItems = SqlHelper.GetFirst(
			""
			+ str(Parameter1.QUERY_CRITERIA_1)
			+ "  A SET TNTVDC = ROUND( (TNTVGC * ISNULL(DCCRFX,1)) ,CONVERT(INT,"+str(roundcurr.DECIMAL_PLACES)+"),CONVERT(INT,"+str(roundcurr.ROUNDING_METHOD)+")), TAXVDC = ROUND( (TAXVGC * ISNULL(DCCRFX,1)) ,CONVERT(INT,"+str(roundcurr.DECIMAL_PLACES)+"),CONVERT(INT,"+str(roundcurr.ROUNDING_METHOD)+")), TAMTDC = ROUND( (TAMTGC * ISNULL(DCCRFX,1)) ,CONVERT(INT,"+str(roundcurr.DECIMAL_PLACES)+"),CONVERT(INT,"+str(roundcurr.ROUNDING_METHOD)+")), TENVDC = ROUND( (TENVGC * ISNULL(DCCRFX,1)) ,CONVERT(INT,"+str(roundcurr.DECIMAL_PLACES)+"),CONVERT(INT,"+str(roundcurr.ROUNDING_METHOD)+"))  FROM SAQICO A(NOLOCK) JOIN (SELECT  DISTINCT QUOTE_ID,SERVICE_ID,REVISION_ID,LINE  FROM SAQICO_INBOUND B(NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"'  )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.QTEREV_ID = B.REVISION_ID AND A.LINE = B.LINE ' ")
			
		primaryQueryItems = SqlHelper.GetFirst(
			""
			+ str(Parameter1.QUERY_CRITERIA_1)
			+ "  A SET  TCWOSS = B.TOTAL_COST_WOSEEDSTOCK,TCWISS = TOTAL_COST_WISEEDSTOCK FROM SAQICO A(NOLOCK) JOIN (SELECT QUOTE_ID,SERVICE_ID,SUM(CONVERT(FLOAT,TOTAL_COST_WOSEEDSTOCK)) AS TOTAL_COST_WOSEEDSTOCK,SUM(CONVERT(FLOAT,TOTAL_COST_WISEEDSTOCK)) AS TOTAL_COST_WISEEDSTOCK,REVISION_ID,LINE FROM SAQICO_INBOUND B(NOLOCK) WHERE ISNULL(PROCESS_STATUS,'''')=''INPROGRESS'' AND TIMESTAMP = '"+str(timestamp_sessionid)+"' GROUP BY QUOTE_ID,SERVICE_ID,REVISION_ID,LINE  )B ON A.QUOTE_ID = B.QUOTE_ID AND A.SERVICE_ID = B.SERVICE_ID AND A.QTEREV_ID = B.REVISION_ID AND A.LINE = B.LINE  ' ")




parameters = {}
parameters['contract_quote_record_id']=str(Param.ContractQuoteRecordId)
parameters['contract_quote_revision_record_id']=str(Param.ContractQuoteRevisionRecordId)

contract_quote_item_obj = ContractQuoteItemAnnualizedPricing(**parameters)
contract_quote_item_obj._do_opertion()

	






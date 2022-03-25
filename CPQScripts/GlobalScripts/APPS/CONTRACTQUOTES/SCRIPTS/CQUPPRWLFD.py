# =========================================================================================================================================
#   __script_name : CQUPPRWLFD.PY
#   __script_description : THIS SCRIPT IS USED TO UPDATE PRICING FIELDS IN ANNUALIZED ITEMS(WATERFALL)
#   __primary_author__ : AYYAPPAN SUBRAMANIYAN
#   __create_date :01-03-2021
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED -
# ==========================================================================================================================================

import datetime
from SYDATABASE import SQL
import re
Sql = SQL()

class ContractQuoteItemAnnualizedPricing:
	def __init__(self, **kwargs):		
		self.user_id = str(User.Id)
		self.user_name = str(User.UserName)		
		self.datetime_value = datetime.datetime.now()
		self.contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
		self.contract_quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
		self.contract_quote_id = Quote.CompositeNumber
		self.records = kwargs.get('records')		
		self.auto_update_flag = kwargs.get('auto_update_flag')
	
	def _do_opertion(self):
		if self.records:
			self.records = eval(self.records)		
			Trace.Write("-------------+++ "+str(self.records))	
			for data in self.records:
				for line_id, value in data.items():					
					update_fields_str = ' ,'.join(["{} = {}".format(field_name,float(field_value) if field_value else 0) for field_name, field_value in value.items()])					

					Sql.RunQuery("""UPDATE SAQICO
							SET {UpdateFields}	
							FROM SAQICO (NOLOCK)							
							WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.LINE = '{LineId}'""".format(UpdateFields=update_fields_str, QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, LineId=line_id))
					if 'ADDCOF' in update_fields_str:
						self._rolldown_from_coeff_level(line_id)
						self._rolldown_from_total_price_level(line_id)
					else:
						self._rolldown_from_total_price_level(line_id, update_fields_str)
					# Approval Trigger Field Update 
					Sql.RunQuery("""UPDATE SAQICO
							SET SAQICO.UACBDA = 'True'	
							FROM SAQICO (NOLOCK)							
							WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.LINE = '{LineId}' AND (SAQICO.USRPRC > SAQICO.CELPRC)""".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, LineId=line_id))
					Sql.RunQuery("""UPDATE SAQICO
							SET SAQICO.UBSBDA = 'True'	
							FROM SAQICO (NOLOCK)							
							WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.LINE = '{LineId}' AND (SAQICO.BDVPRC < SAQICO.SLSPRC) AND (SAQICO.USRPRC < SAQICO.SLSPRC)""".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, LineId=line_id))
					Sql.RunQuery("""UPDATE SAQICO
							SET SAQICO.UBSNSA = 'True'	
							FROM SAQICO (NOLOCK)							
							WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.LINE = '{LineId}' AND (SAQICO.USRPRC < SAQICO.SLSPRC) AND (SAQICO.SLSPRC < SAQICO.BDVPRC)""".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, LineId=line_id))
			##roll up script call
			try:
				CallingCQIFWUDQTM = ScriptExecutor.ExecuteGlobal("CQIFWUDQTM",{"QT_REC_ID":self.contract_quote_id,"manual_pricing":"True"})
			except:
				Trace.Write("error in pricing roll up")

	def _rolldown_from_coeff_level(self, line_id = None):
		#SUMCOF - Sum of All Coefficient
		Sql.RunQuery("UPDATE SAQICO SET SUMCOF = ISNULL(INTCPC,0) + ISNULL(LTCOSS,0) + ISNULL(POFVDC,0) + ISNULL(GBKVDC,0) + ISNULL(UIMVDC,0) + ISNULL(CAVVDC,0) + ISNULL(WNDVDC,0) + ISNULL(SCMVDC,0) + ISNULL(CCDFFC,0) + ISNULL(NPIVDC,0) + ISNULL(DTPVDC,0) + ISNULL(CSTVDC,0) + ISNULL(CSGVDC,0) + ISNULL(QRQVDC,0) + ISNULL(SVCVDC,0) + ISNULL(RKFVDC,0) + ISNULL(PBPVDC,0) + ISNULL(ADDCOF,0) FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND LINE = '{LineId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, LineId=line_id))
					
		#INMP01 - Intermediate Model Price 1
		Sql.RunQuery("UPDATE SAQICO SET INMP01 = EXP(SUMCOF) FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND LINE = '{LineId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, LineId=line_id))
			
		#INMP02 / FNMDPR - Intermediate Model Price 2 /  Final Model Price
		Sql.RunQuery("UPDATE SAQICO SET INMP02 = INMP01 * (1 + ISNULL(CCRTMC,0)), FNMDPR = INMP01 * (1 + ISNULL(CCRTMC,0)) FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND LINE = '{LineId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, LineId=line_id))
		
		# #FNMDPR - Final Model Price (Z0100 / Z0101)		
		# Sql.RunQuery("UPDATE SAQICO SET CNSM_MARGIN_PERCENT = SABGMR.CNSM_MARGIN_PERCENT FROM SAQICO (NOLOCK) JOIN SABGMR (NOLOCK) ON SAQICO.GREENBOOK = SABGMR.GREENBOOK AND SAQICO.BLUEBOOK = SABGMR.BLUEBOOK WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND LINE = '{LineId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, LineId=line_id))
		
		# Sql.RunQuery("UPDATE SAQICO SET CNSM_MARGIN_PERCENT = SABGMR.CNSM_MARGIN_PERCENT FROM SAQICO_INBOUND(NOLOCK) JOIN SABGMR (NOLOCK) ON SAQICO.GREENBOOK = SABGMR.GREENBOOK AND SAQICO.REGION = SABGMR.REGION WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND LINE = '{LineId}' AND SAQICO.CNSM_MARGIN_PERCENT IS NULL'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, LineId=line_id))
		
		# Sql.RunQuery("UPDATE SAQICO SET FNMDPR =  TCWISS / (1 - (CNSM_MARGIN_PERCENT/100)), MTGPRC =  TCWISS / (1 - (CNSM_MARGIN_PERCENT/100)), MSLPRC =  TCWISS / (1 - (CNSM_MARGIN_PERCENT/100)), MBDPRC =  TCWISS / (1 - (CNSM_MARGIN_PERCENT/100)), MCLPRC =  TCWISS / (1 - (CNSM_MARGIN_PERCENT/100)) ,CNTCST = TCWISS, CNTPRC = TCWISS / (1 - (CNSM_MARGIN_PERCENT/100)) FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND LINE = '{LineId}' AND ISNULL(TCWISS,0)>0 AND SERVICE_ID IN ('Z0100','Z0101')".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, LineId=line_id))
		
		#MTGPRC - Target Model Price
		Sql.RunQuery("UPDATE SAQICO SET MTGPRC = CASE WHEN ISNULL(FNMDPR/(1-(CONVERT(FLOAT,SADSPC)/100)),0) > ISNULL(TCWISS / (1-(TAPMMP/100)),0) THEN ISNULL(FNMDPR/(1-(CONVERT(FLOAT,SADSPC)/100)),0) ELSE ISNULL(TCWISS / (1-(TAPMMP/100)),0) END FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND LINE = '{LineId}' AND SERVICE_ID NOT IN ('Z0100','Z0101')".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, LineId=line_id))
		
		#MSLPRC - Sales Model Price
		Sql.RunQuery("UPDATE SAQICO SET MSLPRC = CASE WHEN ISNULL(FNMDPR,0) > ISNULL(TCWISS / (1-(CONVERT(FLOAT,SAPMMP)/100)),0) THEN ISNULL(FNMDPR,0) ELSE ISNULL(TCWISS / (1-(CONVERT(FLOAT,SAPMMP)/100)),0) END FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND LINE = '{LineId}' AND SERVICE_ID NOT IN ('Z0100','Z0101')".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, LineId=line_id))
		
		#MBDPRC - BD Model Price
		Sql.RunQuery("UPDATE SAQICO SET MBDPRC = CASE WHEN ISNULL(FNMDPR * (1-(CONVERT(FLOAT,BDDSPC)/100)) ,0) > ISNULL(TCWISS / (1-(CONVERT(FLOAT,BDPMMP)/100)),0) THEN ISNULL(FNMDPR * (1-(CONVERT(FLOAT,BDDSPC)/100)) ,0) ELSE ISNULL(TCWISS / (1-(CONVERT(FLOAT,BDPMMP)/100)),0) END FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND LINE = '{LineId}' AND SERVICE_ID NOT IN ('Z0100','Z0101')".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, LineId=line_id))
		
		#MCLPRC - Ceiling Model Price
		Sql.RunQuery("UPDATE SAQICO SET MCLPRC = MTGPRC * (1 + ISNULL(CEPRUP/100,0)) FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND LINE = '{LineId}' AND SERVICE_ID NOT IN ('Z0100','Z0101')".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, LineId=line_id))		
		
	def _rolldown_from_total_price_level(self, line_id=None, updated_fields=''):
		where_condition = ""
		if self.auto_update_flag == 'True':
			where_condition = " AND SERVICE_ID != 'Z0123'"
		#
		#TOTLCI - Total Cost Impact
		Sql.RunQuery("UPDATE SAQICO SET TOTLCI = ISNULL(CAVVCI,0) + ISNULL(UIMVCI,0) + ISNULL(ATGKEC,0) + ISNULL(AMNCCI,0) + ISNULL(HEDBIC,0) + ISNULL(NWPTOC,0) + ISNULL(NUMLCI,0) + ISNULL(SPCCLC,0) + ISNULL(SPCCCI,0) + ISNULL(AMNCCI,0) FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND LINE = '{LineId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, LineId=line_id))
		
		#TOTLPI - Total Price Impact
		Sql.RunQuery("UPDATE SAQICO SET TOTLPI = ISNULL(ATGKEP,0) + ISNULL(AMNPPI,0) + ISNULL(CAVVPI,0) + ISNULL(HEDBIP,0) + ISNULL(NWPTOP,0) + ISNULL(NUMLPI,0) + ISNULL(SPCCLP,0) + ISNULL(SPCCPI,0) + ISNULL(UIMVPI,0) + ISNULL(AMNPPI,0) FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND LINE = '{LineId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, LineId=line_id))

		#FINPRC - Final Price
		Sql.RunQuery("UPDATE SAQICO SET FINPRC = ISNULL(MTGPRC,0) + ISNULL(TOTLPI,0) + ISNULL(ADDMPI,0) FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND LINE = '{LineId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, LineId=line_id))
		
		#FCWOSS - Final Total Cost without Seedstock
		Sql.RunQuery("UPDATE SAQICO SET FCWOSS = ISNULL(TCWOSS,0) + ISNULL(TOTLCI,0) FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND LINE = '{LineId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, LineId=line_id))
		
		#FCWISS - Final Total Cost with Seedstock
		Sql.RunQuery("UPDATE SAQICO SET FCWISS = ISNULL(TCWISS,0) + ISNULL(TOTLCI,0) FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND LINE = '{LineId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, LineId=line_id))

		#SBTCST - Sub Total Cost
		Sql.RunQuery("UPDATE SAQICO SET SBTCST = ISNULL(TCWISS,0) + (ISNULL(CAVVCI,0) + ISNULL(UIMVCI,0) + ISNULL(ATGKEC,0) + ISNULL(AMNCCI,0) + ISNULL(HEDBIC,0) + ISNULL(NWPTOC,0) + ISNULL(NUMLCI,0) + ISNULL(SPCCLC,0) + ISNULL(SPCCCI,0)) FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND LINE = '{LineId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, LineId=line_id))
		
		#SBTPRC - Sub Total Price
		Sql.RunQuery("UPDATE SAQICO SET SBTPRC = ISNULL(MTGPRC,0) + (ISNULL(ATGKEP,0) + ISNULL(AMNPPI,0) + ISNULL(CAVVPI,0) + ISNULL(HEDBIP,0) + ISNULL(NWPTOP,0) + ISNULL(NUMLPI,0) + ISNULL(SPCCLP,0) + ISNULL(SPCCPI,0) + ISNULL(UIMVPI,0)) FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND LINE = '{LineId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, LineId=line_id))
		
		#AMNCPE - Additional Manual Cost and Price
		Sql.RunQuery("UPDATE SAQICO SET AMNCPE = 1 FROM SAQICO (NOLOCK) JOIN PRSPRV (NOLOCK) ON PRSPRV.SERVICE_ID = SAQICO.SERVICE_ID WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND LINE = '{LineId}' AND ISNULL(SAQICO.SBTCST, 0) <= 0 AND ISNULL(SAQICO.SBTPRC, 0) <= 0 AND ISNULL(PRSPRV.SSCM_COST,0) = 0 AND ISNULL(PRSPRV.TARGET_PRICE,0) = 0".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, LineId=line_id))

		#AMNCPI - Additional Manual Cost and Price Complet
		Sql.RunQuery("UPDATE SAQICO SET AMNCPI = CASE WHEN ISNULL(SAQICO.AMNCPE, 0) = 1 AND (ISNULL(SAQICO.AMNCCI,0) > 0 AND ISNULL(SAQICO.AMNPPI,0) > 0) THEN 1 WHEN ISNULL(SAQICO.AMNCPE, 0) = 1 AND (ISNULL(SAQICO.AMNCCI,0) <= 0 OR ISNULL(SAQICO.AMNPPI,0) <= 0) THEN 0 ELSE null END FROM SAQICO (NOLOCK) JOIN PRSPRV (NOLOCK) ON PRSPRV.SERVICE_ID = SAQICO.SERVICE_ID WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND LINE = '{LineId}' AND ISNULL(SAQICO.SBTCST, 0) <= 0 AND ISNULL(SAQICO.SBTPRC, 0) <= 0 AND ISNULL(PRSPRV.SSCM_COST,0) = 0 AND ISNULL(PRSPRV.TARGET_PRICE,0) = 0".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, LineId=line_id))

		#Status
		Sql.RunQuery("UPDATE SAQICO SET STATUS = CASE WHEN ISNULL(SAQICO.AMNCPE, 0) = 1 AND (ISNULL(SAQICO.AMNCCI,0) > 0 AND ISNULL(SAQICO.AMNPPI,0) > 0) THEN 'ACQUIRED' WHEN ISNULL(SAQICO.AMNCPE, 0) = 1 AND (ISNULL(SAQICO.AMNCCI,0) <= 0 OR ISNULL(SAQICO.AMNPPI,0) <= 0) THEN 'ERROR' ELSE SAQICO.STATUS END FROM SAQICO (NOLOCK) JOIN PRSPRV (NOLOCK) ON PRSPRV.SERVICE_ID = SAQICO.SERVICE_ID WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND LINE = '{LineId}' AND ISNULL(SAQICO.SBTCST, 0) <= 0 AND ISNULL(SAQICO.SBTPRC, 0) <= 0 AND ISNULL(PRSPRV.SSCM_COST,0) = 0 AND ISNULL(PRSPRV.TARGET_PRICE,0) = 0".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, LineId=line_id))
		
		#SLSPRC / BDVPRC /CELPRC - Target / Sales / BD / Ceiling Price
		Sql.RunQuery("UPDATE SAQICO SET SLSPRC = ISNULL(MSLPRC,0) + ISNULL(TOTLPI,0), BDVPRC = ISNULL(MBDPRC,0) + ISNULL(TOTLPI,0), CELPRC = ISNULL(MCLPRC,0) + ISNULL(TOTLPI,0)  FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND LINE = '{LineId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, LineId=line_id))

		#TRGPRC 
		Sql.RunQuery("UPDATE SAQICO SET TRGPRC = ISNULL(MTGPRC,0) + ISNULL(TOTLPI,0)  FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND LINE = '{LineId}' {WhereCondition}".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, LineId=line_id, WhereCondition =  where_condition))
		
		#USRPRC / TGADJP - User Price / Target User Price Adjustment
		Trace.Write("=================>>>> "+str(updated_fields))
		if 'USRPRC' not in updated_fields:
			Sql.RunQuery("UPDATE SAQICO SET USRPRC = TRGPRC FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND LINE = '{LineId}' {WhereCondition}".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, LineId=line_id, WhereCondition =  where_condition))
		if 'TGADJP' not in updated_fields:
			Sql.RunQuery("UPDATE SAQICO SET TGADJP = (TRGPRC - USRPRC) / TRGPRC * -1 FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND LINE = '{LineId}' {WhereCondition}".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, LineId=line_id, WhereCondition =  where_condition))
		else:	
			Sql.RunQuery("UPDATE SAQICO SET USRPRC = TRGPRC * (TGADJP / 100) FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND LINE = '{LineId}' {WhereCondition}".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, LineId=line_id, WhereCondition =  where_condition))
		#CNTPRC - Contractual Price
		Sql.RunQuery("UPDATE SAQICO SET CNTPRC = ((USRPRC / 365) * CNTDAY * ISNULL(CTPDFP ,1) ) * (1 - (ISNULL(YOYPCT,0)/100)) FROM SAQICO (NOLOCK) WHERE  QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND LINE = '{LineId}' AND SERVICE_ID NOT IN ('Z0100','Z0101') {WhereCondition}".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, LineId=line_id, WhereCondition =  where_condition))
		
		#CNTCST - Contractual Cost
		Sql.RunQuery("UPDATE SAQICO SET CNTCST = ((FCWISS / 365) * CNTDAY ) FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND LINE = '{LineId}' AND SERVICE_ID NOT IN ('Z0100','Z0101')".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, LineId=line_id))
		
		#CNTMGN - Contractual Margin
		Sql.RunQuery("UPDATE SAQICO SET CNTMGN = CNTPRC - CNTCST FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND LINE = '{LineId}' AND SERVICE_ID NOT IN ('Z0100','Z0101')".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, LineId=line_id))
		
		#SPCTPR /SPCTCS - Spares Contractual Price / Cost
		Sql.RunQuery("UPDATE SAQICO SET SPCTPR = CNTPRC * SPSPCT, SPCTCS = CNTCST * SPSPCT FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND LINE = '{LineId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, LineId=line_id))
			
		#SPCTMG - Spares Contractual Margin
		Sql.RunQuery("UPDATE SAQICO SET SPCTMG = (SPCTPR - SPCTCS) / SPCTPR FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND LINE = '{LineId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, LineId=line_id))
		
		#SVCTPR /SVCTCS - Service Contractual Price / Cost
		Sql.RunQuery("UPDATE SAQICO SET SVCTPR = CNTPRC * SVSPCT, SVCTCS = CNTCST * SVSPCT FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND LINE = '{LineId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, LineId=line_id))
		
		#SVCTMG - Service Contractual Margin
		Sql.RunQuery("UPDATE SAQICO SET SVCTMG = (SVCTPR - SVCTCS) / SVCTPR FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND LINE = '{LineId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, LineId=line_id))
		
		#TNTVGC / TNTMGC / TNTMPC - Total Net Value / Total Net Value in Margin / Margin % (Global Currency) 
		Sql.RunQuery("UPDATE SAQICO SET TNTVGC = CNTPRC, TNTMGC = CNTPRC - CNTCST, TNTMPC = (CNTPRC - CNTCST) / CNTPRC FROM SAQICO(NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND LINE = '{LineId}' AND BILTYP <> 'VARIABLE' AND ISNULL(CNTPRC,0)>0".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, LineId=line_id))
		
		#TENVGC - Estimated Value (Global Currency)
		Sql.RunQuery("UPDATE SAQICO SET TENVGC = CNTPRC, TNTMGC = CNTPRC - CNTCST FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND LINE = '{LineId}' AND BILTYP = 'VARIABLE'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, LineId=line_id))
			
		#TAXVGC - Tax Amount (Global Currency) 
		Sql.RunQuery("UPDATE SAQICO SET TAXVGC = TNTVGC * (ISNULL(TAXVTP,0)/100) FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND LINE = '{LineId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, LineId=line_id))
		
		#TAMTGC - Total Amount (Global Currency) 
		Sql.RunQuery("UPDATE SAQICO SET TAMTGC = TNTVGC + ISNULL(TAXVGC,0) FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND LINE = '{LineId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, LineId=line_id))
		
		currency_rounding_obj = Sql.GetFirst("SELECT DISTINCT CASE WHEN ROUNDING_DECIMAL_PLACES = '' THEN 0 ELSE ROUNDING_DECIMAL_PLACES END  AS DECIMAL_PLACES, CASE WHEN ROUNDING_METHOD='ROUND DOWN' THEN 1 ELSE 0 END AS ROUNDING_METHOD FROM SAQRIT(NOLOCK) JOIN PRCURR (NOLOCK) ON SAQRIT.DOC_CURRENCY = PRCURR.CURRENCY WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' ".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id))
		if currency_rounding_obj:
			#Round Off
			Sql.RunQuery("UPDATE SAQICO SET TAMTGC = ROUND(TAMTGC ,CONVERT(INT,{DecimalPlaces}),CONVERT(INT,{RoundingMethod})), TAXVGC = ROUND(TAXVGC ,CONVERT(INT,{DecimalPlaces}),CONVERT(INT,{RoundingMethod})), TNTVGC = ROUND(TNTVGC ,CONVERT(INT,{DecimalPlaces}),CONVERT(INT,{RoundingMethod})) FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND LINE = '{LineId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, LineId=line_id, DecimalPlaces=currency_rounding_obj.DECIMAL_PLACES, RoundingMethod=currency_rounding_obj.ROUNDING_METHOD))
			
			#TNTVDC / TAXVDC / TAMTDC /TENVDC - Total Net Value / Tax / Total Amount/ Estimated (Document Currency) 
			Sql.RunQuery("UPDATE SAQICO SET TNTVDC = ROUND( (TNTVGC * ISNULL(DCCRFX,1)) ,CONVERT(INT,{DecimalPlaces}),CONVERT(INT,{RoundingMethod})), TAXVDC = ROUND( (TAXVGC * ISNULL(DCCRFX,1)) ,CONVERT(INT,{DecimalPlaces}),CONVERT(INT,{RoundingMethod})), TAMTDC = ROUND( (TAMTGC * ISNULL(DCCRFX,1)) ,CONVERT(INT,{DecimalPlaces}),CONVERT(INT,{RoundingMethod})), TENVDC = ROUND( (TENVGC * ISNULL(DCCRFX,1)) ,CONVERT(INT,{DecimalPlaces}),CONVERT(INT,{RoundingMethod})) FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND LINE = '{LineId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, LineId=line_id, DecimalPlaces=currency_rounding_obj.DECIMAL_PLACES, RoundingMethod=currency_rounding_obj.ROUNDING_METHOD))


	def _insert_billing_matrix(self):
		Sql.RunQuery("DELETE FROM SAQRIB WHERE WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'".format(QuoteRecordId= self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id))
		Sql.RunQuery("""
				INSERT SAQRIB (
				QUOTE_BILLING_PLAN_RECORD_ID,
				BILLING_END_DATE,
				BILLING_DAY,
				BILLING_START_DATE,
				QUOTE_ID,
				QUOTE_NAME,
				QUOTE_RECORD_ID,
				QTEREV_ID,
				QTEREV_RECORD_ID,
				CPQTABLEENTRYADDEDBY,
				CPQTABLEENTRYDATEADDED,
				CpqTableEntryModifiedBy,
				CpqTableEntryDateModified,
				SALESORG_ID,
				SALESORG_NAME,
				SALESORG_RECORD_ID,
				PRDOFR_ID,
				PRDOFR_RECORD_ID,
				SERVICE_ID,
				SERVICE_DESCRIPTION
				) 
				SELECT 
				CONVERT(VARCHAR(4000),NEWID()) as QUOTE_BILLING_PLAN_RECORD_ID,
				SAQTMT.CONTRACT_VALID_TO as BILLING_END_DATE,
				30 as BILLING_DAY,
				SAQTMT.CONTRACT_VALID_FROM as BILLING_START_DATE,
				SAQTMT.QUOTE_ID,
				SAQTMT.QUOTE_NAME,
				SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID as QUOTE_RECORD_ID,
				SAQTMT.QTEREV_ID as QTEREV_ID,
				SAQTMT.QTEREV_RECORD_ID as QTEREV_RECORD_ID,
				'{UserName}' AS CPQTABLEENTRYADDEDBY,
				GETDATE() as CPQTABLEENTRYDATEADDED,
				{UserId} as CpqTableEntryModifiedBy,
				GETDATE() as CpqTableEntryDateModified,
				SAQTSV.SALESORG_ID,
				SAQTSV.SALESORG_NAME,
				SAQTSV.SALESORG_RECORD_ID,
				SAQTSV.SERVICE_ID as PRDOFR_ID,
				SAQTSV.SERVICE_RECORD_ID as PRDOFR_RECORD_ID,
				SAQTSV.SERVICE_ID,
				SAQTSV.SERVICE_DESCRIPTION                   
				FROM SAQTMT (NOLOCK) JOIN SAQTSV on SAQTSV.QUOTE_ID = SAQTMT.QUOTE_ID AND SAQTSV.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID
				WHERE SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQTMT.QTEREV_RECORD_ID = '{RevisionRecordId}'
				AND SAQTSV.SERVICE_ID NOT IN ('Z0101','A6200','Z0108','Z0110') AND SAQTSV.SERVICE_ID NOT IN (SELECT PRDOFR_ID FROM SAQRIB (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}')
														
		""".format(                        
			QuoteRecordId= self.contract_quote_record_id,
			RevisionRecordId=self.contract_quote_revision_record_id,
			UserId=user_id,
			UserName=user_name
		))

	def billingmatrix_create(self):
		#Trace.Write('4739---------------')
		_quote_items_greenbook_summary_insert()
		billing_plan_obj = Sql.GetList("SELECT DISTINCT PRDOFR_ID,BILLING_START_DATE,BILLING_END_DATE,BILLING_DAY FROM SAQRIB (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(self.contract_quote_record_id,self.contract_quote_revision_record_id))
		quotedetails = Sql.GetFirst("SELECT CONTRACT_VALID_FROM,CONTRACT_VALID_TO FROM SAQTMT (NOLOCK) WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(self.contract_quote_record_id,self.contract_quote_revision_record_id))
		get_billling_data_dict = {}
		contract_start_date = quotedetails.CONTRACT_VALID_FROM
		contract_end_date = quotedetails.CONTRACT_VALID_TO
		get_ent_val = get_ent_billing_type_value = get_ent_bill_cycle = get_billing_type = ''
		if contract_start_date and contract_end_date and billing_plan_obj:
			Sql.RunQuery("""DELETE FROM SAQIBP WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'""".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id))
			#Trace.Write('4739---------4744------')
			for val in billing_plan_obj:
				if billing_plan_obj:				
					contract_start_date = val.BILLING_START_DATE
					contract_end_date = val.BILLING_END_DATE				
					start_date = datetime.datetime.strptime(UserPersonalizationHelper.ToUserFormat(contract_start_date), '%m/%d/%Y')
					#start_date = str(contract_start_date).split(' ')[0]
					billing_day = int(val.BILLING_DAY)
					get_service_val = val.PRDOFR_ID
					get_billing_cycle = Sql.GetFirst("select ENTITLEMENT_XML from SAQITE where QUOTE_RECORD_ID = '{qtid}' AND QTEREV_RECORD_ID = '{qt_rev_id}' and SERVICE_ID = '{get_service}'".format(qtid =self.contract_quote_record_id,qt_rev_id=self.contract_quote_revision_record_id,get_service = str(get_service_val).strip()))
					if get_billing_cycle:
						updateentXML = get_billing_cycle.ENTITLEMENT_XML
						pattern_tag = re.compile(r'(<QUOTE_ITEM_ENTITLEMENT>[\w\W]*?</QUOTE_ITEM_ENTITLEMENT>)')
						pattern_id = re.compile(r'<ENTITLEMENT_ID>(AGS_'+str(get_service_val)+'_PQB_BILCYC|AGS_'+str(get_service_val)+'_PQB_BILTYP)</ENTITLEMENT_ID>')
						#pattern_id_billing_type = re.compile(r'<ENTITLEMENT_ID>(AGS_'+str(get_service_val)+'_PQB_BILTYP|AGS_'+str(get_service_val)+'_PQB_BILTYP)</ENTITLEMENT_ID>')
						pattern_name = re.compile(r'<ENTITLEMENT_DISPLAY_VALUE>([^>]*?)</ENTITLEMENT_DISPLAY_VALUE>')
						for m in re.finditer(pattern_tag, updateentXML):
							sub_string = m.group(1)
							get_ent_id = re.findall(pattern_id,sub_string)
							#get_ent_bill_type = re.findall(pattern_id_billing_type,sub_string)
							get_ent_val= re.findall(pattern_name,sub_string)
							if get_ent_id:
								get_ent_val = str(get_ent_val[0])
								get_billling_data_dict[get_ent_id[0]] = str(get_ent_val)
								#get_ent_bill_cycle = str(get_ent_val)
								for data,val in get_billling_data_dict.items():
									if 'AGS_'+str(get_service_val)+'_PQB_BILCYC' in data:
										get_ent_bill_cycle = val
									elif 'AGS_'+str(get_service_val)+'_PQB_BILTYP' in data:
										get_billing_type =val
								
					billing_month_end = 0
					entitlement_obj = Sql.GetFirst("select convert(xml,replace(replace(replace(replace(replace(replace(ENTITLEMENT_XML,'&',';#38'),'''',';#39'),' < ',' &lt; ' ),' > ',' &gt; ' ),'_>','_&gt;'),'_<','_&lt;')) as ENTITLEMENT_XML,QUOTE_RECORD_ID,SERVICE_ID from SAQTSE (nolock) where QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'".format(QuoteRecordId =self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id))
					if str(get_ent_bill_cycle).upper() == "ONE ITEM PER QUOTE":
						if billing_day in (29,30,31):
							if start_date.month == 2:
								isLeap = lambda x: x % 4 == 0 and (x % 100 != 0 or x % 400 == 0)
								end_day = 29 if isLeap(start_date.year) else 28
								start_date = start_date.replace(day=end_day)
							elif start_date.month in (4, 6, 9, 11) and billing_day == 31:
								start_date = start_date.replace(day=30)
							else:
								start_date = start_date.replace(day=billing_day)
						else:
							start_date = start_date.replace(day=billing_day)
						end_date = datetime.datetime.strptime(UserPersonalizationHelper.ToUserFormat(contract_end_date), '%m/%d/%Y')
						#end_date = str(contract_end_date).split(' ')[0]
						diff1 = end_date - start_date

						avgyear = 365.2425        # pedants definition of a year length with leap years
						avgmonth = 365.2425/12.0  # even leap years have 12 months
						years, remainder = divmod(diff1.days, avgyear)
						years, months = int(years), int(remainder // avgmonth)            
						
						total_months = years * 12 + months
						for index in range(0, total_months+1):
							Trace.Write('index--'+str(index))
							billing_month_end += 1
							if str(index) in ['0','12','24','36','48']:
								insert_item_per_billing(total_months=total_months, 
														billing_date="DATEADD(month, {Month}, '{BillingDate}')".format(
															Month=index, BillingDate=start_date.strftime('%m/%d/%Y')
															),billing_end_date="DATEADD(month, {Month_add}, '{BillingDate}')".format(
															Month_add=billing_month_end, BillingDate=start_date.strftime('%m/%d/%Y')
															), amount_column="YEAR_"+str((index/12) + 1),
															entitlement_obj=entitlement_obj,service_id = get_service_val,get_ent_val_type = get_ent_bill_cycle,get_ent_billing_type_value = get_ent_billing_type_value,get_billling_data_dict=get_billling_data_dict)
					
					elif str(get_ent_bill_cycle).upper() == "MONTHLY" :
						if billing_day in (29,30,31):
							if start_date.month == 2:
								isLeap = lambda x: x % 4 == 0 and (x % 100 != 0 or x % 400 == 0)
								end_day = 29 if isLeap(start_date.year) else 28
								start_date = start_date.replace(day=end_day)
							elif start_date.month in (4, 6, 9, 11) and billing_day == 31:
								start_date = start_date.replace(day=30)
							else:
								start_date = start_date.replace(day=billing_day)
						else:
							start_date = start_date.replace(day=billing_day)
						end_date = datetime.datetime.strptime(UserPersonalizationHelper.ToUserFormat(contract_end_date), '%m/%d/%Y')
						#end_date = str(contract_end_date).split(' ')[0]
						diff1 = end_date - start_date

						avgyear = 365.2425        # pedants definition of a year length with leap years
						avgmonth = 365.2425/12.0  # even leap years have 12 months
						years, remainder = divmod(diff1.days, avgyear)
						years, months = int(years), int(remainder // avgmonth)            
						
						total_months = years * 12 + months
						if get_service_val != 'Z0007':
							for index in range(0, total_months+1):
								billing_month_end += 1
								insert_items_billing_plan(total_months=total_months, 
														billing_date="DATEADD(month, {Month}, '{BillingDate}')".format(
															Month=index, BillingDate=start_date.strftime('%m/%d/%Y')
															),billing_end_date="DATEADD(month, {Month_add}, '{BillingDate}')".format(
															Month_add=billing_month_end, BillingDate=start_date.strftime('%m/%d/%Y')
															), amount_column="YEAR_"+str((index/12) + 1),
															entitlement_obj=entitlement_obj,service_id = get_service_val,get_ent_val_type = get_ent_bill_cycle,get_ent_billing_type_value = get_ent_billing_type_value,get_billling_data_dict=get_billling_data_dict)
						else:

							get_milestones_data_dict = {}
							get_total_milestons= ''
							
							get_service_val = service_id
							
							get_milestone_details = Sql.GetFirst("select ENTITLEMENT_XML from SAQTSE where QUOTE_RECORD_ID='{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'  and SERVICE_ID = '{get_service}'".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id,get_service = str(service_id).strip()))
							if get_milestone_details:
								updateentXML = get_milestone_details.ENTITLEMENT_XML
								pattern_tag = re.compile(r'(<QUOTE_ITEM_ENTITLEMENT>[\w\W]*?</QUOTE_ITEM_ENTITLEMENT>)')
								pattern_id = re.compile(r'<ENTITLEMENT_ID>(AGS_Z0007_PQB_MILEST|AGS_'+str(get_service_val)+'_PQB_MILST1|AGS_'+str(get_service_val)+'_PQB_MILST2|AGS_'+str(get_service_val)+'_PQB_MILST3|AGS_'+str(get_service_val)+'_PQB_MIL3DS|AGS_'+str(get_service_val)+'_PQB_MIL1DS|AGS_'+str(get_service_val)+'_PQB_MIL2DS|AGS_'+str(get_service_val)+'_PQB_MIL3BD|AGS_'+str(get_service_val)+'_PQB_MIL2BD|AGS_'+str(get_service_val)+'_PQB_MIL1BD)</ENTITLEMENT_ID>')
								pattern_name = re.compile(r'<ENTITLEMENT_DISPLAY_VALUE>([^>]*?)</ENTITLEMENT_DISPLAY_VALUE>')
								for m in re.finditer(pattern_tag, updateentXML):
									sub_string = m.group(1)
									get_ent_id = re.findall(pattern_id,sub_string)
									get_ent_val= re.findall(pattern_name,sub_string)
									if get_ent_id:
										get_ent_val = str(get_ent_val[0])
										get_milestones_data_dict[get_ent_id[0]] = str(get_ent_val)
							for data,val in get_milestones_data_dict.items():
								count =0
								if ('AGS_Z0007_PQB_MIL3BD','AGS_Z0007_PQB_MIL2BD','AGS_Z0007_PQB_MIL1BD') in data:
									billing_month_end += 1
									if val:
										fts_zoo7_insert(total_months=total_months, 
															billing_date="DATEADD(month, {Month}, '{BillingDate}')".format(
																Month=count, BillingDate=val.strftime('%m/%d/%Y')
																),billing_end_date="DATEADD(month, {Month_add}, '{BillingDate}')".format(
																Month_add=billing_month_end, BillingDate=val.strftime('%m/%d/%Y')
																), amount_column="YEAR_"+str((count/12) + 1),
																entitlement_obj=entitlement_obj,service_id = get_service_val,get_ent_val_type = get_ent_bill_cycle,get_ent_billing_type_value = get_ent_billing_type_value,get_billling_data_dict=get_billling_data_dict,get_milestones_data_dict=get_milestones_data_dict)
										count += 1
					elif str(get_ent_bill_cycle).upper() == "QUARTELY":
						ct_start_date =contract_start_date
						ct_end_date =contract_end_date
						if ct_start_date>ct_end_date:
							ct_start_date,ct_end_date=ct_end_date,ct_start_date
						m1=ct_start_date.Year*12+ct_start_date.Month  
						m2=ct_end_date.Year*12+ct_end_date.Month  
						months=m2-m1
						months=months/3
						for index in range(0, months):
							billing_month_end += 1
							insert_items_billing_plan(total_months=months, 
													billing_date="DATEADD(month, {Month}, '{BillingDate}')".format(
														Month=index, BillingDate=start_date.strftime('%m/%d/%Y')
														),billing_end_date="DATEADD(month, {Month_add}, '{BillingDate}')".format(
														Month_add=billing_month_end, BillingDate=start_date.strftime('%m/%d/%Y')
														),amount_column="YEAR_"+str((index/4) + 1),
														entitlement_obj=entitlement_obj,service_id = get_service_val,get_ent_val_type = get_ent_val,get_ent_billing_type_value=get_ent_billing_type_value,get_billling_data_dict=get_billling_data_dict)
				
					else:
						Trace.Write('get_ent_val---'+str(get_ent_bill_cycle))
						if billing_day in (29,30,31):
							if start_date.month == 2:
								isLeap = lambda x: x % 4 == 0 and (x % 100 != 0 or x % 400 == 0)
								end_day = 29 if isLeap(start_date.year) else 28
								start_date = start_date.replace(day=end_day)
							elif start_date.month in (4, 6, 9, 11) and billing_day == 31:
								start_date = start_date.replace(day=30)
							else:
								start_date = start_date.replace(day=billing_day)
						else:
							start_date = start_date.replace(day=billing_day)
						end_date = datetime.datetime.strptime(UserPersonalizationHelper.ToUserFormat(contract_end_date), '%m/%d/%Y')			
						diff1 = end_date - start_date

						avgyear = 365.2425        # pedants definition of a year length with leap years
						avgmonth = 365.2425/12.0  # even leap years have 12 months
						years, remainder = divmod(diff1.days, avgyear)
						years, months = int(years), int(remainder // avgmonth)
						for index in range(0, years+1):
							billing_month_end += 1
							insert_items_billing_plan(total_months=years, 
													billing_date="DATEADD(month, {Month}, '{BillingDate}')".format(
														Month=index, BillingDate=start_date.strftime('%m/%d/%Y')
														),billing_end_date="DATEADD(month, {Month_add}, '{BillingDate}')".format(
														Month_add=billing_month_end, BillingDate=start_date.strftime('%m/%d/%Y')
														),amount_column="YEAR_"+str((index) + 1),
														entitlement_obj=entitlement_obj,service_id = get_service_val,get_ent_val_type = get_ent_val,get_ent_billing_type_value = get_ent_billing_type_value,get_billling_data_dict=get_billling_data_dict)	

	def generate_billing_matrix(self):
		#_insert_billing_matrix()
		Trace.Write('Genarte billing matrix')

parameters = {}
parameters['records']=str(Param.Records)
try:
	parameters['auto_update_flag'] = str(Param.auto_update_flag)
except:
	parameters['auto_update_flag'] = "False"
contract_quote_item_obj = ContractQuoteItemAnnualizedPricing(**parameters)
contract_quote_item_obj._do_opertion()
contract_quote_item_obj.generate_billing_matrix()






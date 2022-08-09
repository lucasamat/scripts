# =========================================================================================================================================
#   __script_name : CQUPPRWLFD.PY
#   __script_description : THIS SCRIPT IS USED TO UPDATE PRICING FIELDS IN ANNUALIZED ITEMS(WATERFALL)
#   __primary_author__ : AYYAPPAN SUBRAMANIYAN
#   __create_date :01-03-2021
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED -
# ==========================================================================================================================================

import datetime
import System.Net
from System.Text.Encoding import UTF8
from System import Convert
from SYDATABASE import SQL
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
            price_updated_services = []
            for data in self.records:
                for annual_item_record_id, value in data.items():					
                    update_fields_str = ' ,'.join(["{} = {}".format(field_name,float(field_value.replace(" USD","")) if field_value else 0) for field_name, field_value in value.items()])					
                    annualaized_item_obj = Sql.GetFirst("SELECT SERVICE_ID FROM SAQICO (NOLOCK) WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnaualItemRecordId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnaualItemRecordId=annual_item_record_id))
                    if annualaized_item_obj:
                        price_updated_services.append(annualaized_item_obj.SERVICE_ID)
                    Sql.RunQuery("""UPDATE SAQICO
                            SET {UpdateFields}	
                            FROM SAQICO (NOLOCK)							
                            WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}'""".format(UpdateFields=update_fields_str, QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id))
                    Log.Info("update_fields_str--"+str(update_fields_str))
                    #if 'ADDCOF' in update_fields_str:
                    #    Log.Info("Inside If"+str(update_fields_str))
                    #    self._rolldown_from_coeff_level(annual_item_record_id)
                    #    self._rolldown_from_total_price_level(annual_item_record_id)
                    #else:
                    Log.Info("Inside else"+str(update_fields_str))
                    self._rolldown_from_coeff_level(annual_item_record_id)
                    self._rolldown_from_total_price_level(annual_item_record_id, update_fields_str)
                    # Approval Trigger Field Update 
                    Sql.RunQuery("""UPDATE SAQICO
                            SET SAQICO.UACBDA = 'True'	
                            FROM SAQICO (NOLOCK)							
                            WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}' AND (SAQICO.USRPRC > SAQICO.CELPRC)""".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id))
                    Sql.RunQuery("""UPDATE SAQICO
                            SET SAQICO.UBSBDA = 'True'	
                            FROM SAQICO (NOLOCK)							
                            WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}' AND (SAQICO.BDVPRC < SAQICO.SLSPRC) AND (SAQICO.USRPRC < SAQICO.SLSPRC)""".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id))
                    Sql.RunQuery("""UPDATE SAQICO
                            SET SAQICO.UBSNSA = 'True'	
                            FROM SAQICO (NOLOCK)							
                            WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}' AND (SAQICO.USRPRC < SAQICO.SLSPRC) AND (SAQICO.SLSPRC < SAQICO.BDVPRC)""".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id))
            ##roll up script call
            if self.auto_update_flag != 'True':
                try:
                    CallingCQIFWUDQTM = ScriptExecutor.ExecuteGlobal("CQIFWUDQTM",{"QT_REC_ID":self.contract_quote_id,"manual_pricing":"True",'service_ids':list(set(price_updated_services))})
                except:
                    Trace.Write("error in pricing roll up")
            
            #SAQRIT - Status - Offline Pricing
            Sql.RunQuery("UPDATE SAQRIT SET STATUS = SAQICO.STATUS FROM SAQRIT (NOLOCK) JOIN SAQICO (NOLOCK) ON SAQICO.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND SAQICO.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID AND SAQICO.SERVICE_ID = SAQRIT.SERVICE_ID AND SAQICO.QTEITM_RECORD_ID = SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID WHERE SAQRIT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id))

            Sql.RunQuery("UPDATE SAQRIT SET STATUS = 'OFFLINE PRICING' FROM SAQRIT (NOLOCK) JOIN SAQICO (NOLOCK) ON SAQICO.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND SAQICO.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID AND SAQICO.SERVICE_ID = SAQRIT.SERVICE_ID AND SAQICO.QTEITM_RECORD_ID = SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID WHERE SAQRIT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND ISNULL(SAQICO.STATUS,'') = 'OFFLINE PRICING'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id))

            Sql.RunQuery("UPDATE SAQRIT SET STATUS = 'PRR-ON HOLD PRICING' FROM SAQRIT (NOLOCK) JOIN SAQICO (NOLOCK) ON SAQICO.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND SAQICO.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID AND SAQICO.SERVICE_ID = SAQRIT.SERVICE_ID AND SAQICO.QTEITM_RECORD_ID = SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID WHERE SAQRIT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND ISNULL(SAQICO.STATUS,'') = 'PRR-ON HOLD PRICING'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id))
            
            Sql.RunQuery("UPDATE SAQRIT SET STATUS = 'CFG-ON HOLD TKM' FROM SAQRIT (NOLOCK) JOIN SAQICO (NOLOCK) ON SAQICO.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND SAQICO.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID AND SAQICO.SERVICE_ID = SAQRIT.SERVICE_ID AND SAQICO.QTEITM_RECORD_ID = SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID WHERE SAQRIT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND ISNULL(SAQICO.STATUS,'') = 'CFG-ON HOLD TKM'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id))

            items_status = []
            items_obj = Sql.GetList("SELECT DISTINCT ISNULL(STATUS,'') as STATUS FROM SAQRIT (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' and QTEREV_RECORD_ID = '{QuoteRevisionRecordId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id))
            if items_obj:
                items_status = [item_obj.STATUS for item_obj in items_obj]
            
            Trace.Write("===========>"+str(items_status))
            if 'CFG-ON HOLD - COSTING' in items_status:
                Sql.RunQuery("UPDATE SAQTRV SET WORKFLOW_STATUS = 'CONFIGURE',REVISION_STATUS='CFG-ON HOLD - COSTING' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' and QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' ".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id))
            elif 'PRR-ON HOLD PRICING' in items_status or 'OFFLINE PRICING' in items_status:
                Sql.RunQuery("UPDATE SAQTRV SET WORKFLOW_STATUS = 'PRICING REVIEW',REVISION_STATUS='PRR-ON HOLD PRICING' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' and QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' ".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id))			
            else:
                #items_status = list(set(items_status))
                #if len(items_status) == 1 and items_status[0].upper() == 'ACQUIRED':
                Log.Info('check pricing update--->'+str(self.contract_quote_record_id))
                get_workflow_status = Sql.GetFirst("SELECT WORKFLOW_STATUS from SAQTRV WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' and QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' ".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id))
                if get_workflow_status.WORKFLOW_STATUS not in ('APPROVALS'):
                    Sql.RunQuery("UPDATE SAQTRV SET WORKFLOW_STATUS = 'PRICING',REVISION_STATUS='PRI-PRICING' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' and QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' ".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id))
                
            # Billing Call			
            #self._billing_call()
            
    # def _billing_call(self):
    # 	#Log.Info('Billing---contract_quote_record_id---'+str(contract_quote_record_id))
    # 	LOGIN_CREDENTIALS = Sql.GetFirst("SELECT USER_NAME as Username,Password,Domain FROM SYCONF where Domain='AMAT_TST'")
    # 	if LOGIN_CREDENTIALS is not None:
    # 		Login_Username = str(LOGIN_CREDENTIALS.Username)
    # 		Login_Password = str(LOGIN_CREDENTIALS.Password)
    # 		authorization = Login_Username+":"+Login_Password
    # 		binaryAuthorization = UTF8.GetBytes(authorization)
    # 		authorization = Convert.ToBase64String(binaryAuthorization)
    # 		authorization = "Basic " + authorization
    # 		webclient = System.Net.WebClient()
    # 		webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/json"
    # 		webclient.Headers[System.Net.HttpRequestHeader.Authorization] = authorization;		
    # 		result = '''<?xml version="1.0" encoding="UTF-8"?><soapenv:Envelope	xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">	<soapenv:Body><CPQ_Columns>	<QUOTE_ID>{Qt_Id}</QUOTE_ID><REVISION_ID>{Rev_Id}</REVISION_ID></CPQ_Columns></soapenv:Body></soapenv:Envelope>'''.format( Qt_Id= self.contract_quote_record_id,Rev_Id = self.contract_quote_revision_record_id)		
    # 		LOGIN_CRE = Sql.GetFirst("SELECT URL FROM SYCONF where EXTERNAL_TABLE_NAME ='BILLING_MATRIX_ASYNC'")
    # 		Async = webclient.UploadString(str(LOGIN_CRE.URL), str(result))

    def _rolldown_from_coeff_level(self, annual_item_record_id = None):
        #SUMCOF - Sum of All Coefficient
        #Sql.RunQuery("UPDATE SAQICO SET SUMCOF = ISNULL(INTCPC,0) + ISNULL(LTCOSS,0) + ISNULL(POFVDC,0) + ISNULL(GBKVDC,0) + ISNULL(UIMVDC,0) + ISNULL(CAVVDC,0) + ISNULL(WNDVDC,0) + ISNULL(SCMVDC,0) + ISNULL(CCDFFC,0) + ISNULL(NPIVDC,0) + ISNULL(DTPVDC,0) + ISNULL(ITNTVC,0) + ISNULL(CSGVDC,0) + ISNULL(QRQVDC,0) + ISNULL(SVCVDC,0) + ISNULL(RKFVDC,0) + ISNULL(PBPVDC,0) + ISNULL(ADDCOF,0) + ISNULL(ITTNBC,0) FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id))
                    
        #INMP01 - Intermediate Model Price 1
        #Sql.RunQuery("UPDATE SAQICO SET INMP01 = EXP(SUMCOF) FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id))
            
        #INMP02 / FNMDPR - Intermediate Model Price 2 /  Final Model Price
        #Sql.RunQuery("UPDATE SAQICO SET INMP02 = INMP01 * (1 + ISNULL(CCRTMC,0)), FNMDPR = INMP01 * (1 + ISNULL(CCRTMC,0)) FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id))
        
        # #FNMDPR - Final Model Price (Z0100 / Z0101)		
        # Sql.RunQuery("UPDATE SAQICO SET CNSM_MARGIN_PERCENT = SABGMR.CNSM_MARGIN_PERCENT FROM SAQICO (NOLOCK) JOIN SABGMR (NOLOCK) ON SAQICO.GREENBOOK = SABGMR.GREENBOOK AND SAQICO.BLUEBOOK = SABGMR.BLUEBOOK WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id))
        
        # Sql.RunQuery("UPDATE SAQICO SET CNSM_MARGIN_PERCENT = SABGMR.CNSM_MARGIN_PERCENT FROM SAQICO_INBOUND(NOLOCK) JOIN SABGMR (NOLOCK) ON SAQICO.GREENBOOK = SABGMR.GREENBOOK AND SAQICO.REGION = SABGMR.REGION WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}' AND SAQICO.CNSM_MARGIN_PERCENT IS NULL'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id))
        
        # Sql.RunQuery("UPDATE SAQICO SET FNMDPR =  TCWISS / (1 - (CNSM_MARGIN_PERCENT/100)), MTGPRC =  TCWISS / (1 - (CNSM_MARGIN_PERCENT/100)), MSLPRC =  TCWISS / (1 - (CNSM_MARGIN_PERCENT/100)), MBDPRC =  TCWISS / (1 - (CNSM_MARGIN_PERCENT/100)), MCLPRC =  TCWISS / (1 - (CNSM_MARGIN_PERCENT/100)) ,CNTCST = TCWISS, CNTPRC = TCWISS / (1 - (CNSM_MARGIN_PERCENT/100)) FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}' AND ISNULL(TCWISS,0)>0 AND SERVICE_ID IN ('Z0100','Z0101')".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id))
        
        #AIPBNC - Pricebook Non Model Cost
        Sql.RunQuery("UPDATE SAQICO SET AIPBNC = ISNULL(AMNCCI, 0) FROM SAQICO (NOLOCK) WHERE (ISNULL(SAQICO.STATUS,'') = 'OFFLINE PRICING' OR (ISNULL(SAQICO.STATUS,'') = 'PRR-ON HOLD PRICING' AND GREENBOOK = 'PDC' AND SERVICE_ID in ('Z0091','Z0099','Z0035')) OR (SERVICE_ID in ('Z0117','Z0116','Z0100','Z0046','Z0123'))) AND QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id))
        
        #AITPNP - Target Non Model Price
        Sql.RunQuery("UPDATE SAQICO SET AITPNP = ISNULL(AMNPPI, 0) FROM SAQICO (NOLOCK) WHERE (ISNULL(SAQICO.STATUS,'') = 'OFFLINE PRICING' OR (ISNULL(SAQICO.STATUS,'') = 'PRR-ON HOLD PRICING' AND GREENBOOK = 'PDC' AND SERVICE_ID in ('Z0091','Z0099','Z0035'))) AND QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id))

        #AISPNP, AICPNP, AIBPNP - Sales, Ceiling, BD Non Model Price
        Sql.RunQuery("UPDATE SAQICO SET AISPNP = ISNULL(ISNULL(AITPNP, 0) * (1-(CONVERT(FLOAT,SADSPC)/100)), 0), AICPNP = ISNULL(ISNULL(AITPNP, 0) * (1+(CONVERT(FLOAT,CEPRUP)/100)), 0), AIBPNP = ISNULL(ISNULL(AITPNP, 0) * (1-(CONVERT(FLOAT,BDDSPC)/100)), 0) FROM SAQICO (NOLOCK) WHERE (ISNULL(SAQICO.STATUS,'') = 'OFFLINE PRICING' OR (ISNULL(SAQICO.STATUS,'') = 'PRR-ON HOLD PRICING' AND GREENBOOK = 'PDC' AND SERVICE_ID in ('Z0091','Z0099','Z0035')) OR (SERVICE_ID in ('Z0117','Z0116','Z0100','Z0046','Z0123'))) AND QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id))
        
        #MTGPRC - Target Model Price
        Sql.RunQuery("UPDATE SAQICO SET MTGPRC = CASE WHEN (ISNULL(SAQICO.STATUS,'') = 'OFFLINE PRICING' OR (ISNULL(SAQICO.STATUS,'') = 'PRR-ON HOLD PRICING' AND GREENBOOK = 'PDC' AND SERVICE_ID in ('Z0091','Z0099','Z0035')) OR (SERVICE_ID in ('Z0117','Z0116','Z0100','Z0046','Z0123'))) THEN ISNULL(AITPNP,0) WHEN ISNULL(FNMDPR/(1-(CONVERT(FLOAT,SADSPC)/100)),0) > ISNULL(TCWISS / (1-(TAPMMP/100)),0) THEN ISNULL(FNMDPR/(1-(CONVERT(FLOAT,SADSPC)/100)),0) ELSE ISNULL(TCWISS / (1-(TAPMMP/100)),0) END FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id))
        
        #MSLPRC - Sales Model Price
        Sql.RunQuery("UPDATE SAQICO SET MSLPRC = CASE WHEN (ISNULL(SAQICO.STATUS,'') = 'OFFLINE PRICING' OR (ISNULL(SAQICO.STATUS,'') = 'PRR-ON HOLD PRICING' AND GREENBOOK = 'PDC' AND SERVICE_ID in ('Z0091','Z0099','Z0035')) OR (SERVICE_ID in ('Z0117','Z0116','Z0100','Z0046','Z0123'))) THEN ISNULL(AISPNP,0) WHEN ISNULL(FNMDPR,0) > ISNULL(TCWISS / (1-(CONVERT(FLOAT,SAPMMP)/100)),0) THEN ISNULL(FNMDPR,0) ELSE ISNULL(TCWISS / (1-(CONVERT(FLOAT,SAPMMP)/100)),0) END FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id))
        
        #MBDPRC - BD Model Price
        Sql.RunQuery("UPDATE SAQICO SET MBDPRC = CASE WHEN (ISNULL(SAQICO.STATUS,'') = 'OFFLINE PRICING' OR (ISNULL(SAQICO.STATUS,'') = 'PRR-ON HOLD PRICING' AND GREENBOOK = 'PDC' AND SERVICE_ID in ('Z0091','Z0099','Z0035')) OR (SERVICE_ID in ('Z0117','Z0116','Z0100','Z0046','Z0123'))) THEN ISNULL(AIBPNP,0) WHEN ISNULL(FNMDPR * (1-(CONVERT(FLOAT,BDDSPC)/100)) ,0) > ISNULL(TCWISS / (1-(CONVERT(FLOAT,BDPMMP)/100)),0) THEN ISNULL(FNMDPR * (1-(CONVERT(FLOAT,BDDSPC)/100)) ,0) ELSE ISNULL(TCWISS / (1-(CONVERT(FLOAT,BDPMMP)/100)),0) END FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id))
        
        #MCLPRC - Ceiling Model Price
        Sql.RunQuery("UPDATE SAQICO SET MCLPRC = CASE WHEN (ISNULL(SAQICO.STATUS,'') = 'OFFLINE PRICING' OR (ISNULL(SAQICO.STATUS,'') = 'PRR-ON HOLD PRICING' AND GREENBOOK = 'PDC' AND SERVICE_ID in ('Z0091','Z0099','Z0035')) OR (SERVICE_ID in ('Z0117','Z0116','Z0100','Z0046','Z0123'))) THEN ISNULL(AICPNP,0) ELSE MTGPRC * (1 + ISNULL(CEPRUP/100,0)) END FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id))		
        
    def _rolldown_from_total_price_level(self, annual_item_record_id=None, updated_fields=''):
        where_condition = ""
        if self.auto_update_flag == 'True':
            where_condition = " AND SERVICE_ID <> 'Z0123'"
        # HEDBIC - Head Break In Cost Impact
        Sql.RunQuery("UPDATE SAQICO SET HEDBIC = (ISNULL(CONVERT(FLOAT,PRCFVA.FACTOR_TXTVAR),0) * ISNULL(SAQICO.TNHRPT,0)) FROM SAQICO (NOLOCK) JOIN MAEQUP (NOLOCK) ON MAEQUP.EQUIPMENT_ID  = SAQICO.EQUIPMENT_ID JOIN PRCFVA (NOLOCK) ON PRCFVA.FACTOR_VARIABLE_ID = MAEQUP.SUBSTRATE_SIZE_GROUP WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}' AND SERVICE_ID IN ('Z0091', 'Z0035', 'Z0009') AND HEDBIN = 'Included' AND FACTOR_ID = 'HBWFCT'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id))

        # HEDBIP - Head Break In Price Impact
        Sql.RunQuery("UPDATE SAQICO SET HEDBIP = (ISNULL(CONVERT(FLOAT,PRCFVA.FACTOR_TXTVAR),0) * ISNULL(SAQICO.TNHRPT,0)) FROM SAQICO (NOLOCK) JOIN MAEQUP (NOLOCK) ON MAEQUP.EQUIPMENT_ID  = SAQICO.EQUIPMENT_ID JOIN PRCFVA (NOLOCK) ON PRCFVA.FACTOR_VARIABLE_ID = MAEQUP.SUBSTRATE_SIZE_GROUP WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}' AND SAQICO.SERVICE_ID IN ('Z0091', 'Z0035', 'Z0009') AND HEDBIN = 'Included' AND FACTOR_ID = 'HBWFPR'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id))

        # SPCCLC - Specialized Cleaning Cost Impact
        Sql.RunQuery("UPDATE SAQICO SET SPCCLC = (ISNULL(CONVERT(FLOAT,PREGBV.ENTITLEMENT_COST_IMPACT),0) * ISNULL(SAQICO.TNHRPT,0)) FROM SAQICO (NOLOCK) JOIN PREGBV (NOLOCK) ON PREGBV.SERVICE_ID = SAQICO.SERVICE_ID AND PREGBV.ENTITLEMENT_VALUE_CODE = SAQICO.SPCCLN AND PREGBV.ENTITLEMENT_NAME = 'Specialized Cleaning' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}' AND SAQICO.SERVICE_ID IN ('Z0091', 'Z0035', 'Z0009')".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id))

        # SPCCLP - Specialized Cleaning Price Impact
        Sql.RunQuery("UPDATE SAQICO SET SPCCLP = (ISNULL(CONVERT(FLOAT,PREGBV.ENTITLEMENT_PRICE_IMPACT),0) * ISNULL(SAQICO.TNHRPT,0)) FROM SAQICO (NOLOCK) JOIN PREGBV (NOLOCK) ON PREGBV.SERVICE_ID = SAQICO.SERVICE_ID AND PREGBV.ENTITLEMENT_VALUE_CODE = SAQICO.SPCCLN AND PREGBV.ENTITLEMENT_NAME = 'Specialized Cleaning' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}' AND SAQICO.SERVICE_ID IN ('Z0091', 'Z0035', 'Z0009')".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id))

        # SPCCCI - Specialized Coating Cost Impact
        Sql.RunQuery("UPDATE SAQICO SET SPCCCI = (ISNULL(CONVERT(FLOAT,PREGBV.ENTITLEMENT_COST_IMPACT),0) * ISNULL(SAQICO.TNHRPT,0)) FROM SAQICO (NOLOCK) JOIN PREGBV (NOLOCK) ON PREGBV.SERVICE_ID = SAQICO.SERVICE_ID AND PREGBV.ENTITLEMENT_VALUE_CODE = SAQICO.SPCCLN AND PREGBV.ENTITLEMENT_NAME = 'Specialized Coating' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}' AND SAQICO.SERVICE_ID IN ('Z0091', 'Z0035', 'Z0009')".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id))

        # SPCCPI - Specialized Coating Price Impact
        Sql.RunQuery("UPDATE SAQICO SET SPCCPI = (ISNULL(CONVERT(FLOAT,PREGBV.ENTITLEMENT_PRICE_IMPACT),0) * ISNULL(SAQICO.TNHRPT,0)) FROM SAQICO (NOLOCK) JOIN PREGBV (NOLOCK) ON PREGBV.SERVICE_ID = SAQICO.SERVICE_ID AND PREGBV.ENTITLEMENT_VALUE_CODE = SAQICO.SPCCLN AND PREGBV.ENTITLEMENT_NAME = 'Specialized Coating' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}' AND SAQICO.SERVICE_ID IN ('Z0091', 'Z0035', 'Z0009')".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id))

        #TOTLCI - Total Cost Impact
        Sql.RunQuery("UPDATE SAQICO SET TOTLCI = ISNULL(CAVVCI,0) + ISNULL(UIMVCI,0) + ISNULL(ATGKEC,0) + ISNULL(AMNCCI,0) + ISNULL(HEDBIC,0) + ISNULL(NWPTOC,0) + ISNULL(NUMLCI,0) + ISNULL(SPCCLC,0) + ISNULL(SPCCCI,0) + ISNULL(ATKNCI,0) + ISNULL(CONSCP,0) + ISNULL(NONCCI,0) + ISNULL(AIUICI,0) FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id))
        
        #TOTLPI - Total Price Impact
        Sql.RunQuery("UPDATE SAQICO SET TOTLPI = ISNULL(ATGKEP,0) + ISNULL(AMNPPI,0) + ISNULL(CAVVPI,0) + ISNULL(HEDBIP,0) + ISNULL(NWPTOP,0) + ISNULL(NUMLPI,0) + ISNULL(SPCCLP,0) + ISNULL(SPCCPI,0) + ISNULL(UIMVPI,0) + ISNULL(ATKNPI,0) + ISNULL(CONSPI,0) + ISNULL(NONCPI,0) + ISNULL(AIUIPI,0) FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id))

        #FINPRC - Final Price 
        # Removed - Need to check later (+ ISNULL(ADDMPI,0))
        Sql.RunQuery("UPDATE SAQICO SET FINPRC = CASE WHEN (ISNULL(SAQICO.STATUS,'') = 'OFFLINE PRICING' OR (ISNULL(SAQICO.STATUS,'') = 'PRR-ON HOLD PRICING' AND GREENBOOK = 'PDC' AND SERVICE_ID in ('Z0091','Z0099','Z0035')) OR (SERVICE_ID in ('Z0117','Z0116','Z0100','Z0046','Z0123'))) THEN ISNULL(TOTLPI,0) ELSE ISNULL(MTGPRC,0) + ISNULL(TOTLPI,0) END FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id))
        
        #FCWOSS - Final Total Cost without Seedstock
        Sql.RunQuery("UPDATE SAQICO SET FCWOSS = ISNULL(TCWOSS,0) + ISNULL(TOTLCI,0) FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id))
        
        #FCWISS - Final Total Cost with Seedstock
        Sql.RunQuery("UPDATE SAQICO SET FCWISS = ISNULL(TCWISS,0) + ISNULL(TOTLCI,0) FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id))

        #SBTCST - Sub Total Cost
        Sql.RunQuery("UPDATE SAQICO SET SBTCST = ISNULL(TCWISS,0) + (ISNULL(CAVVCI,0) + ISNULL(UIMVCI,0) + ISNULL(ATGKEC,0) + ISNULL(HEDBIC,0) + ISNULL(NWPTOC,0) + ISNULL(NUMLCI,0) + ISNULL(SPCCLC,0) + ISNULL(SPCCCI,0)) + ISNULL(ATKNCI,0) + ISNULL(CONSCP,0) + ISNULL(NONCCI,0) + ISNULL(AIUICI,0) FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id))
        
        #SBTPRC - Sub Total Price
        Sql.RunQuery("UPDATE SAQICO SET SBTPRC = CASE WHEN (ISNULL(SAQICO.STATUS,'') = 'OFFLINE PRICING' OR (ISNULL(SAQICO.STATUS,'') = 'PRR-ON HOLD PRICING' AND GREENBOOK = 'PDC' AND SERVICE_ID in ('Z0091','Z0099','Z0035')) OR (SERVICE_ID in ('Z0117','Z0116','Z0100','Z0046','Z0123'))) THEN (ISNULL(ATGKEP,0) + ISNULL(CAVVPI,0) + ISNULL(HEDBIP,0) + ISNULL(NWPTOP,0) + ISNULL(NUMLPI,0) + ISNULL(SPCCLP,0) + ISNULL(SPCCPI,0) + ISNULL(UIMVPI,0)) + ISNULL(ATKNPI,0) + ISNULL(CONSPI,0) + ISNULL(NONCPI,0) + ISNULL(AIUIPI,0) ELSE ISNULL(MTGPRC,0) + (ISNULL(ATGKEP,0) + ISNULL(CAVVPI,0) + ISNULL(HEDBIP,0) + ISNULL(NWPTOP,0) + ISNULL(NUMLPI,0) + ISNULL(SPCCLP,0) + ISNULL(SPCCPI,0) + ISNULL(UIMVPI,0)) + ISNULL(ATKNPI,0) + ISNULL(CONSPI,0) + ISNULL(NONCPI,0) + ISNULL(AIUIPI,0) END FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id))


        #AMNCPE - Additional Manual Cost and Price
        Sql.RunQuery("UPDATE SAQICO SET AMNCPE = 1 FROM SAQICO (NOLOCK) JOIN PRSPRV (NOLOCK) ON PRSPRV.SERVICE_ID = SAQICO.SERVICE_ID WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}' AND ISNULL(SAQICO.SBTCST, 0) <= 0 AND ISNULL(SAQICO.SBTPRC, 0) <= 0 AND ISNULL(PRSPRV.SSCM_COST,0) = 0 AND ISNULL(SAQICO.SERVICE_ID,'') NOT IN ('Z0100','Z0101')".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id))

        #AMNCPI - Additional Manual Cost and Price Complet
        Sql.RunQuery("UPDATE SAQICO SET AMNCPI = CASE WHEN ISNULL(SAQICO.AMNCPE, 0) = 1 AND (ISNULL(SAQICO.AMNCCI,0) > 0 AND ISNULL(SAQICO.AMNPPI,0) > 0) THEN 'ACTIVE' WHEN ISNULL(SAQICO.AMNCPE, 0) = 1 AND (ISNULL(SAQICO.AMNCCI,0) <= 0 OR ISNULL(SAQICO.AMNPPI,0) <= 0) THEN 'INACTIVE' ELSE null END FROM SAQICO (NOLOCK) JOIN PRSPRV (NOLOCK) ON PRSPRV.SERVICE_ID = SAQICO.SERVICE_ID WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}' AND ISNULL(SAQICO.AMNCPE, 0) = 1 AND ISNULL(PRSPRV.SSCM_COST,0) = 0 AND ISNULL(SAQICO.SERVICE_ID,'') NOT IN ('Z0100','Z0101')".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id))

        # A055S000P01-18463 - Start
        #AIATCM - Add. Tgt. KPI Cst Prc
        Sql.RunQuery("UPDATE SAQICO SET AIATCM = CASE WHEN SAQICO.ITATKP IS NULL THEN null WHEN ISNULL(SAQICO.ITATKP, '') <> 'Excluded' AND (ISNULL(SAQICO.ATGKEC,0) = 0 OR ISNULL(SAQICO.ATGKEP,0) = 0) THEN 0 WHEN ISNULL(SAQICO.ITATKP, '') <> 'Excluded' AND (ISNULL(SAQICO.ATGKEC,0) > 0 AND ISNULL(SAQICO.ATGKEP,0) > 0) THEN 1 ELSE null END FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id))
        # A055S000P01-18463 - End

        # A055S000P01-18464 - Start
        #AIANCM - AddTgtKPI(Non-Std) C&P
        Sql.RunQuery("UPDATE SAQICO SET AIANCM = CASE WHEN ISNULL(SAQICO.ITATKP, '') = 'Exception' AND ISNULL(SAQICO.ITATKN, '') <> '' AND (ISNULL(SAQICO.ATKNCI,0) = 0 OR ISNULL(SAQICO.ATKNPI,0) = 0) THEN 0 WHEN ISNULL(SAQICO.ITATKP, '') = 'Exception' AND ISNULL(SAQICO.ITATKN, '') <> '' AND (ISNULL(SAQICO.ATKNCI,0) > 0 AND ISNULL(SAQICO.ATKNPI,0) > 0) THEN 1 ELSE null END FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id))
        # A055S000P01-18464 - End

        # A055S000P01-18465 - Start
        #AINPCM - New Parts Only Cst Prc
        Sql.RunQuery("UPDATE SAQICO SET AINPCM = CASE WHEN ISNULL(SAQICO.ITNWPO, '') = 'Yes' AND (ISNULL(SAQICO.NWPTOC,0) = 0 OR ISNULL(SAQICO.NWPTOP,0) = 0) THEN 0 WHEN ISNULL(SAQICO.ITNWPO, '') = 'Yes' AND (ISNULL(SAQICO.NWPTOC,0) > 0 AND ISNULL(SAQICO.NWPTOP,0) > 0) THEN 1 ELSE null END FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id))
        # A055S000P01-18465 - End

        # A055S000P01-18466 - Start
        #AICNCM - Consumable Cst and Prc
        Sql.RunQuery("UPDATE SAQICO SET AICNCM = CASE WHEN ISNULL(SAQICO.ITCNSM, '') IN ('Some Inclusions', 'Some Exclusions') AND (ISNULL(SAQICO.CONSCP,0) = 0 OR ISNULL(SAQICO.CONSPI,0) = 0) THEN 0 WHEN ISNULL(SAQICO.ITCNSM, '') IN ('Some Inclusions', 'Some Exclusions') AND (ISNULL(SAQICO.CONSCP,0) > 0 AND ISNULL(SAQICO.CONSPI,0) > 0) THEN 1 ELSE null END FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id))
        # A055S000P01-18466 - End

        # A055S000P01-18467 - Start
        #AINCCM - Non Consum. Cst & Prc
        Sql.RunQuery("UPDATE SAQICO SET AINCCM = CASE WHEN ISNULL(SAQICO.ITNCNS, '') IN ('Some Inclusions', 'Some Exclusions') AND (ISNULL(SAQICO.NONCCI,0) = 0 OR ISNULL(SAQICO.NONCPI,0) = 0) THEN 0 WHEN ISNULL(SAQICO.ITNCNS, '') IN ('Some Inclusions', 'Some Exclusions') AND (ISNULL(SAQICO.NONCCI,0) > 0 AND ISNULL(SAQICO.NONCPI,0) > 0) THEN 1 ELSE null END FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id))
        # A055S000P01-18467 - End

        # A055S000P01-19721 - Start
        #AIUICC - Upt Impr Cost and Price Complete
        Sql.RunQuery("UPDATE SAQICO SET AIUICC = CASE WHEN ISNULL(SAQICO.AIUICI, 0) > 0 AND ISNULL(SAQICO.AIUIPI, 0) > 0 THEN 1 WHEN CAST(SAQICO.ITSDUI as NUMERIC(13,3)) > '2.000' THEN 0 ELSE null END FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id))

        #AIFCPE - Final Total Cost Per Event
        Sql.RunQuery("UPDATE SAQICO SET AIFCPE = FCWISS / ISNULL(ADJ_PM_FREQUENCY,0) FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}' AND ISNULL(ADJ_PM_FREQUENCY,0) > 0 AND UPPER(QTETYP) IN ('FLEX EVENT BASED','EVENT BASED') ".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id))

        #SLSPRC / BDVPRC /CELPRC - Target / Sales / BD / Ceiling Price
        Sql.RunQuery("UPDATE SAQICO SET SLSPRC = CASE WHEN (ISNULL(SAQICO.STATUS,'') = 'OFFLINE PRICING' OR (ISNULL(SAQICO.STATUS,'') = 'PRR-ON HOLD PRICING' AND GREENBOOK = 'PDC' AND SERVICE_ID in ('Z0091','Z0099','Z0035')) OR (SERVICE_ID in ('Z0117','Z0116','Z0100','Z0046','Z0123'))) THEN ISNULL(MSLPRC,0) ELSE ISNULL(MSLPRC,0) + ISNULL(TOTLPI,0) END, BDVPRC = CASE WHEN (ISNULL(SAQICO.STATUS,'') = 'OFFLINE PRICING' OR (ISNULL(SAQICO.STATUS,'') = 'PRR-ON HOLD PRICING' AND GREENBOOK = 'PDC' AND SERVICE_ID in ('Z0091','Z0099','Z0035')) OR (SERVICE_ID in ('Z0117','Z0116','Z0100','Z0046','Z0123'))) THEN ISNULL(MBDPRC,0) ELSE ISNULL(MBDPRC,0) + ISNULL(TOTLPI,0) END, CELPRC = CASE WHEN ISNULL(MCLPRC,0)= 0 THEN ISNULL(TOTLPI,0) + (ISNULL(TOTLPI,0) * ISNULL(CEPRUP,0)/100) WHEN (ISNULL(SAQICO.STATUS,'') = 'OFFLINE PRICING' OR (ISNULL(SAQICO.STATUS,'') = 'PRR-ON HOLD PRICING' AND GREENBOOK = 'PDC' AND SERVICE_ID in ('Z0091','Z0099','Z0035')) OR (SERVICE_ID in ('Z0117','Z0116','Z0100','Z0046','Z0123'))) THEN ISNULL(MCLPRC,0) ELSE ISNULL(MCLPRC,0) + ISNULL(TOTLPI,0) END FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id))

        #TRGPRC 
        Sql.RunQuery("UPDATE SAQICO SET TRGPRC = CASE WHEN (ISNULL(SAQICO.STATUS,'') = 'OFFLINE PRICING' OR (ISNULL(SAQICO.STATUS,'') = 'PRR-ON HOLD PRICING' AND GREENBOOK = 'PDC' AND SERVICE_ID in ('Z0091','Z0099','Z0035')) OR (SERVICE_ID in ('Z0117','Z0116','Z0100','Z0046','Z0123'))) THEN ISNULL(MTGPRC,0) ELSE ISNULL(MTGPRC,0) + ISNULL(TOTLPI,0) END FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}' {WhereCondition}".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id, WhereCondition =  where_condition))

        #AIUPPE - User Price Per Event Kit
        Sql.RunQuery("UPDATE SAQICO SET AIUPPE = TRGPRC / ADJ_PM_FREQUENCY FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}' AND ISNULL(ADJ_PM_FREQUENCY,0) > 0 AND UPPER(QTETYP) IN ('FLEX EVENT BASED','EVENT BASED') ".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id))

        #USRPRC / TGADJP - User Price / Target User Price Adjustment
        Trace.Write("=================>>>> "+str(updated_fields))
        if 'USRPRC' not in updated_fields:
            Sql.RunQuery("UPDATE SAQICO SET USRPRC = TRGPRC FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}' {WhereCondition}".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id, WhereCondition =  where_condition))
        if 'TGADJP' not in updated_fields:
            Sql.RunQuery("UPDATE SAQICO SET TGADJP = ((TRGPRC - USRPRC) / TRGPRC * -1) * 100 FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}' {WhereCondition}".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id, WhereCondition =  where_condition))
        else:	
            Sql.RunQuery("UPDATE SAQICO SET USRPRC = TRGPRC + (TRGPRC * (TGADJP / 100)) FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}' {WhereCondition}".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id, WhereCondition =  where_condition))
        #CNTPRC - Contractual Price
        Sql.RunQuery("UPDATE SAQICO SET CNTPRC = ((USRPRC / 365) * CNTDAY * ISNULL(CTPDFP ,1) ) * (1 - (ISNULL(YOYPCT,0)/100)) FROM SAQICO (NOLOCK) WHERE  QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}' AND SERVICE_ID NOT IN ('Z0100','Z0101') {WhereCondition}".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id, WhereCondition =  where_condition))

        Sql.RunQuery("UPDATE SAQICO SET CNTPRC = ((USRPRC / 365) * CNTDAY * ISNULL(CTPDFP ,1) ) * (1 - (ISNULL(YOYPCT,0)/100)) FROM SAQICO (NOLOCK) WHERE  QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}' AND SERVICE_ID IN ('Z0100','Z0101') AND CNSMBL_ENT = 'Included' {WhereCondition}".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id, WhereCondition =  where_condition))
        
        #CNTCST - Contractual Cost
        Sql.RunQuery("UPDATE SAQICO SET CNTCST = ((FCWISS / 365) * CNTDAY ) FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}' AND SERVICE_ID NOT IN ('Z0100','Z0101')".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id))
        
        #CNTMGN - Contractual Margin
        Sql.RunQuery("UPDATE SAQICO SET CNTMGN = CNTPRC - CNTCST FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}' AND SERVICE_ID NOT IN ('Z0100','Z0101')".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id))

        #AICCPE - Price Per Event Kit
        Sql.RunQuery("UPDATE SAQICO SET AICCPE = CNTCST / ADJ_PM_FREQUENCY FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}' AND UPPER(QTETYP) IN ('FLEX EVENT BASED','EVENT BASED') AND ISNULL(ADJ_PM_FREQUENCY,0)>0".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id))

        #SPCTPR /SPCTCS - Spares Contractual Price / Cost
        Sql.RunQuery("UPDATE SAQICO SET SPCTPR = CNTPRC * SPSPCT, SPCTCS = CNTCST * SPSPCT FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id))
            
        #SPCTMG - Spares Contractual Margin
        Sql.RunQuery("UPDATE SAQICO SET SPCTMG = (SPCTPR - SPCTCS) / SPCTPR FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id))
        
        #SVCTPR /SVCTCS - Service Contractual Price / Cost
        Sql.RunQuery("UPDATE SAQICO SET SVCTPR = CNTPRC * SVSPCT, SVCTCS = CNTCST * SVSPCT FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id))
        
        #SVCTMG - Service Contractual Margin
        Sql.RunQuery("UPDATE SAQICO SET SVCTMG = (SVCTPR - SVCTCS) / SVCTPR FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id))
        
        #TNTVGC / TNTMGC / TNTMPC - Total Net Value / Total Net Value in Margin / Margin % (Global Currency) 
        Sql.RunQuery("UPDATE SAQICO SET TNTVGC = CNTPRC, TNTMGC = CNTPRC - CNTCST, TNTMPC = (CNTPRC - CNTCST) / CNTPRC FROM SAQICO(NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}' AND BILTYP <> 'VARIABLE' AND ISNULL(CNTPRC,0)>0".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id))
        
        #TENVGC - Estimated Value (Global Currency)
        Sql.RunQuery("UPDATE SAQICO SET TENVGC = CNTPRC, TNTMGC = CNTPRC - CNTCST FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}' AND BILTYP = 'VARIABLE'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id))
            
        #TAXVGC - Tax Amount (Global Currency) 
        Sql.RunQuery("UPDATE SAQICO SET TAXVGC = TNTVGC * (ISNULL(TAXVTP,0)/100) FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id))
        
        #TAMTGC - Total Amount (Global Currency) 
        Sql.RunQuery("UPDATE SAQICO SET TAMTGC = TNTVGC + ISNULL(TAXVGC,0) FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id))
        
        #TAMTGC - Total Amount (Global Currency) - Variable
        Sql.RunQuery("UPDATE SAQICO SET TAMTGC = TENVGC FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}' AND ISNULL(BILTYP,'') = 'VARIABLE'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id))
        
        currency_rounding_obj = Sql.GetFirst("SELECT DISTINCT CASE WHEN ROUNDING_DECIMAL_PLACES = '' THEN 0 ELSE ROUNDING_DECIMAL_PLACES END  AS DECIMAL_PLACES, CASE WHEN ROUNDING_METHOD='ROUND DOWN' THEN 1 ELSE 0 END AS ROUNDING_METHOD FROM SAQRIT(NOLOCK) JOIN PRCURR (NOLOCK) ON SAQRIT.DOC_CURRENCY = PRCURR.CURRENCY WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' ".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id))
        if currency_rounding_obj:
            #Round Off
            Sql.RunQuery("UPDATE SAQICO SET TAMTGC = ROUND(TAMTGC ,CONVERT(INT,{DecimalPlaces}),CONVERT(INT,{RoundingMethod})), TAXVGC = ROUND(TAXVGC ,CONVERT(INT,{DecimalPlaces}),CONVERT(INT,{RoundingMethod})), TNTVGC = ROUND(TNTVGC ,CONVERT(INT,{DecimalPlaces}),CONVERT(INT,{RoundingMethod})) FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}' AND SERVICE_ID  NOT IN ('Z0123','Z0046','Z0100','Z0116','Z0117')".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id, DecimalPlaces=currency_rounding_obj.DECIMAL_PLACES, RoundingMethod=currency_rounding_obj.ROUNDING_METHOD))#1835,#317
            
            #Round Off
            Sql.RunQuery("UPDATE SAQICO SET TAMTGC = ROUND(TAMTGC ,CONVERT(INT,{DecimalPlaces}),CONVERT(INT,{RoundingMethod})) FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}' AND ISNULL(BILTYP,'') = 'VARIABLE'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id, DecimalPlaces=currency_rounding_obj.DECIMAL_PLACES, RoundingMethod=currency_rounding_obj.ROUNDING_METHOD))
            
            #TNTVDC / TAXVDC / TAMTDC /TENVDC - Total Net Value / Tax / Total Amount/ Estimated (Document Currency) 
            Sql.RunQuery("UPDATE SAQICO SET TNTVDC = ROUND( (TNTVGC * ISNULL(DCCRFX,1)) ,CONVERT(INT,{DecimalPlaces}),CONVERT(INT,{RoundingMethod})), TAXVDC = ROUND( (TAXVGC * ISNULL(DCCRFX,1)) ,CONVERT(INT,{DecimalPlaces}),CONVERT(INT,{RoundingMethod})), TAMTDC = ROUND( (TAMTGC * ISNULL(DCCRFX,1)) ,CONVERT(INT,{DecimalPlaces}),CONVERT(INT,{RoundingMethod})), TENVDC = ROUND( (TENVGC * ISNULL(DCCRFX,1)) ,CONVERT(INT,{DecimalPlaces}),CONVERT(INT,{RoundingMethod})) FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}' AND SERVICE_ID  NOT IN ('Z0123','Z0046','Z0100','Z0116','Z0117')".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id, DecimalPlaces=currency_rounding_obj.DECIMAL_PLACES, RoundingMethod=currency_rounding_obj.ROUNDING_METHOD))#1835,#317

            Sql.RunQuery("UPDATE SAQICO SET TNTVDC = TNTVGC * ISNULL(DCCRFX,1), TAXVDC = TNTVGC * ISNULL(DCCRFX,1), TAMTDC = TAMTGC * ISNULL(DCCRFX,1), TENVDC = TENVGC * ISNULL(DCCRFX,1) FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}' AND SERVICE_ID IN ('Z0123','Z0046','Z0100','Z0116','Z0117')".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id))#317
        
        #Status
        Sql.RunQuery("UPDATE SAQICO SET STATUS = CASE WHEN ISNULL(SAQICO.AMNCPI, '') = 'ACTIVE' AND (ISNULL(SAQICO.AMNCCI,0) > 0 AND ISNULL(SAQICO.AMNPPI,0) > 0) AND (ISNULL(SAQICO.SBTCST, 0) > 0 AND ISNULL(SAQICO.SBTPRC, 0) > 0) THEN 'ACQUIRED' WHEN ISNULL(SAQICO.AMNCPI, '') = 'INACTIVE' AND (ISNULL(SAQICO.AMNCCI,0) <= 0 OR ISNULL(SAQICO.AMNPPI,0) <= 0) AND (ISNULL(SAQICO.SBTCST, 0) <= 0 AND ISNULL(SAQICO.SBTPRC, 0) <= 0) THEN 'OFFLINE PRICING' ELSE SAQICO.STATUS END FROM SAQICO (NOLOCK) JOIN PRSPRV (NOLOCK) ON PRSPRV.SERVICE_ID = SAQICO.SERVICE_ID WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}' AND ISNULL(PRSPRV.SSCM_COST,0) = 0 AND ISNULL(SAQICO.SERVICE_ID,'') NOT IN ('Z0100','Z0101')".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id))

        #Status - For SSCM pricing offerings - Additional Target KPI != 'Excluded'
        Sql.RunQuery("UPDATE SAQICO SET STATUS = 'ACQUIRED' FROM SAQICO (NOLOCK) JOIN PRSPRV (NOLOCK) ON PRSPRV.SERVICE_ID = SAQICO.SERVICE_ID WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}' AND ISNULL(PRSPRV.SSCM_COST,0) = 1".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id))
        
        #Z0100 OFFLINE PRICING
        if self.auto_update_flag != 'True':#312
            Sql.RunQuery("UPDATE SAQICO SET STATUS = 'ACQUIRED' FROM SAQICO (NOLOCK)  WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}' AND ISNULL(CNSMBL_ENT,'') = 'Included' AND SERVICE_ID ='Z0100'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id))
        
        Sql.RunQuery("UPDATE SAQICO SET STATUS = 'PRR-ON HOLD PRICING' FROM SAQICO (NOLOCK) JOIN PRSPRV (NOLOCK) ON PRSPRV.SERVICE_ID = SAQICO.SERVICE_ID WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}' AND ISNULL(PRSPRV.SSCM_COST,0) = 1 AND ((ISNULL(BPTTKP,'No') = 'Yes' AND (ISNULL(BPTKCI,0) <= 0 AND ISNULL(BPTKPI,0) <= 0)) OR (ISNULL(ATGKEY,'Excluded') != 'Excluded' AND (ISNULL(ATGKEC,0) <= 0 AND ISNULL(ATGKEP,0) <= 0)) OR (ISNULL(NWPTON,'') = 'YES' AND (ISNULL(NWPTOC,0) <= 0 AND ISNULL(NWPTOP,0) <= 0)) OR (ISNULL(CNSMBL_ENT,'') in ('Some Inclusions','Some Exclusions') AND (ISNULL(CONSCP,0) <= 0 AND ISNULL(CONSPI,0) <= 0)) OR (ISNULL(NCNSMB_ENT,'') in ('Some Inclusions','Some Exclusions') AND (ISNULL(NONCCI,0) = 0 AND ISNULL(NONCPI,0) = 0)) OR (ISNULL(TGKPNS,'Excluded') != 'Excluded' AND (ISNULL(ATKNCI,0) <= 0 AND ISNULL(ATKNPI,0) <= 0)) OR (ISNULL(AMNCPE,0) = 1 AND (ISNULL(AMNCCI,0) <= 0 AND ISNULL(AMNPPI,0) <= 0)) OR ISNULL(SAQICO.AIUICC,1) = 0)".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id))

        #Status - On Hold TKM
        Sql.RunQuery("UPDATE SAQICO SET STATUS = 'CFG-ON HOLD TKM' FROM SAQICO (NOLOCK) JOIN SAQGPA (NOLOCK) ON SAQICO.QUOTE_ID = SAQGPA.QUOTE_ID AND SAQICO.QTEREV_ID = SAQGPA.QTEREV_ID AND SAQICO.SERVICE_ID = SAQGPA.SERVICE_ID AND SAQICO.EQUIPMENT_ID = SAQGPA.EQUIPMENT_ID WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}' AND  ISNULL(SAQICO.STATUS,'') NOT IN ('PRR-ON HOLD PRICING','CFG-ON HOLD - COSTING','ASSEMBLY IS MISSING') AND ISNULL(SAQGPA.KIT_ID,'')<>'' AND ISNULL(SAQGPA.KIT_NUMBER,'')=''".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id))

        Sql.RunQuery("UPDATE SAQICO SET STATUS = 'CFG-ON HOLD TKM' FROM SAQICO (NOLOCK) JOIN SAQSAP (NOLOCK) ON SAQICO.QUOTE_ID = SAQSAP.QUOTE_ID AND SAQICO.QTEREV_ID = SAQSAP.QTEREV_ID AND SAQICO.SERVICE_ID = SAQSAP.SERVICE_ID AND SAQICO.EQUIPMENT_ID = SAQSAP.EQUIPMENT_ID WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}' AND ISNULL(SAQICO.STATUS,'') NOT IN ('PRR-ON HOLD PRICING','CFG-ON HOLD - COSTING','ASSEMBLY IS MISSING') AND ISNULL(SAQSAP.KIT_ID,'')<>'' AND ISNULL(SAQSAP.KIT_NUMBER,'')=''".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id))

parameters = {}
parameters['records']=str(Param.Records)
try:
    parameters['auto_update_flag'] = str(Param.auto_update_flag)
except:
    parameters['auto_update_flag'] = "False"
contract_quote_item_obj = ContractQuoteItemAnnualizedPricing(**parameters)
contract_quote_item_obj._do_opertion()
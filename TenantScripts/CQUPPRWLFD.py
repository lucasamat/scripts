# =========================================================================================================================================
#   __script_name : CQUPPRWLFD.PY
#   __script_description : THIS SCRIPT IS USED TO UPDATE PRICING FIELDS IN ANNUALIZED ITEMS(WATERFALL)
#   __primary_author__ : AYYAPPAN SUBRAMANIYAN
#   __create_date :01-03-2021
#   CR095B- Bulk Update Pricing (Most of the codes were updated)
# ==========================================================================================================================================

import datetime
import System.Net
from System.Text.Encoding import UTF8
from System import Convert
# INC08641016 - Start - A
import CQCPQC4CWB
# INC08641016 - End - A
from SYDATABASE import SQL
Sql = SQL()

class ContractQuoteItemAnnualizedPricing:
    def __init__(self, **kwargs):
        self.user_id = str(User.Id)
        self.user_name = str(User.UserName)
        self.datetime_value = datetime.datetime.now()
        self.contract_quote_record_id = kwargs.get('quote_record_id')
        self.contract_quote_revision_record_id = kwargs.get('qterev_record_id')
        self.search_condition = kwargs.get('search_condition')
        try:
            self.contract_quote_id = Quote.CompositeNumber
        except:
            get_quoteid = Sql.GetFirst("SELECT QUOTE_ID FROM SAQTRV (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(self.contract_quote_record_id,self.contract_quote_revision_record_id))
            self.contract_quote_id = get_quoteid.QUOTE_ID if get_quoteid is not None else ''
        self.records = kwargs.get('records')
        self.auto_update_flag = kwargs.get('auto_update_flag')
        self.mode = kwargs.get('mode')

    def _do_opertion(self):
        if self.records:
            self.records = eval(self.records)
            Log.Info("-------------+++ "+str(self.records))
            price_updated_services = []
            for data in self.records:
                for annual_item_record_id, value in data.items():
                    #INC09037750-Start-M
                    update_fields_str = ' ,'.join(["{} = {}".format(field_name,float(field_value.replace(" USD","").replace(" ","").replace("USD","")) if field_value else 0) for field_name, field_value in value.items()])
                    #INC09037750-End-M
                    if self.contract_quote_record_id:
                        annualaized_item_obj = Sql.GetFirst("SELECT SERVICE_ID FROM SAQICO (NOLOCK) WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnaualItemRecordId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnaualItemRecordId=annual_item_record_id))
                    else:
                        annualaized_item_obj = Sql.GetFirst("SELECT SERVICE_ID,QUOTE_RECORD_ID,QTEREV_RECORD_ID,QUOTE_ID FROM SAQICO (NOLOCK) WHERE SAQICO.QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnaualItemRecordId}'".format( AnnaualItemRecordId=annual_item_record_id))
                    if annualaized_item_obj and not self.contract_quote_record_id:
                        self.contract_quote_record_id = annualaized_item_obj.QUOTE_RECORD_ID
                        self.contract_quote_revision_record_id = annualaized_item_obj.QTEREV_RECORD_ID
                        self.contract_quote_id = annualaized_item_obj.QUOTE_ID
                    if annualaized_item_obj:
                        price_updated_services.append(annualaized_item_obj.SERVICE_ID)
                    Sql.RunQuery("""UPDATE SAQICO
                            SET {UpdateFields}
                            FROM SAQICO (NOLOCK)
                            WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}'""".format(UpdateFields=update_fields_str, QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id))

                    #A055S000P01-20868 Start - A
                    if 'USRPRC' in update_fields_str:
                        Sql.RunQuery("""UPDATE SAQICO
                            SET AIUPPE = USRPRC / NULLIF(ADJ_PM_FREQUENCY, 0)
                            FROM SAQICO (NOLOCK)
                            WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}'""".format(UpdateFields=update_fields_str, QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id))
                    #A055S000P01-20868 End - A

                    if self.mode!="Bulk Edit":
                        # INC08813185 - Start - M
                        if 'USRPRC' not in update_fields_str and 'TGADJP' not in update_fields_str:
                            self._rolldown_from_coeff_level(annual_item_record_id)
                        # INC08813185 - End - M
                        self._rolldown_from_total_price_level(annual_item_record_id, update_fields_str)
                        self._user_price_approval_trigger(annual_item_record_id)
                    #if 'ADDCOF' in update_fields_str:
                    #    Log.Info("Inside If"+str(update_fields_str))
                    #    self._rolldown_from_coeff_level(annual_item_record_id)
                    #    self._rolldown_from_total_price_level(annual_item_record_id)
            if self.mode!="Bulk Edit": # Added for CR095B (A055S000P01-20380)
            ##roll up script call
                if self.auto_update_flag != 'True':
                    try:
                        Log.Info("===> CQIFWUDQTM called from CQUPPRWLFD for "+str(self.contract_quote_id)+":"+str(list(set(price_updated_services))))
                        CallingCQIFWUDQTM = ScriptExecutor.ExecuteGlobal("CQIFWUDQTM",{"QT_REC_ID":self.contract_quote_id,"manual_pricing":"True",'service_ids':list(set(price_updated_services))})
                    except:
                        Trace.Write("error in pricing roll up")
                self._update_items()
                items_status = []
                items_obj = Sql.GetList("SELECT DISTINCT ISNULL(STATUS,'') as STATUS FROM SAQRIT (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' and QTEREV_RECORD_ID = '{QuoteRevisionRecordId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id))
                if items_obj:
                    items_status = [item_obj.STATUS for item_obj in items_obj]
                Trace.Write("===========>"+str(items_status))
                reviewed_flag = True
                for sts in items_status:
                    if sts not in ('ACQUIRED','CFG-ON HOLD TKM'):
                        reviewed_flag = False
                #INC08784949 - Start - M
                if reviewed_flag and self.mode == "Inline Edit":
                    #INC08784949 - End - M
                    Sql.RunQuery("UPDATE SAQTRV SET REVISION_STATUS = 'PRR-PRICING REVIEWED',WORKFLOW_STATUS = 'PRICING REVIEW' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' and QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND REVISION_STATUS!='PRI-PRICING' ".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id))
                elif 'PRR-ON HOLD PRICING' in items_status or 'OFFLINE PRICING' in items_status:
                    Sql.RunQuery("UPDATE SAQTRV SET WORKFLOW_STATUS = 'PRICING REVIEW',REVISION_STATUS='PRR-ON HOLD PRICING' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' and QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' ".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id))
                elif 'CFG-ON HOLD - COSTING' in items_status:
                    Sql.RunQuery("UPDATE SAQTRV SET WORKFLOW_STATUS = 'CONFIGURE',REVISION_STATUS='CFG-ON HOLD - COSTING' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' and QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' ".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id))
                else:
                    #items_status = list(set(items_status))
                    #if len(items_status) == 1 and items_status[0].upper() == 'ACQUIRED':
                    #STATUS UPDATE
                    # getstatus=SqlHelper.GetFirst("""SELECT COUNT(PRICING_STATUS) AS CNT FROM SAQRSP WHERE QUOTE_RECORD_ID='{QuoteRecordId}' AND PRICING_STATUS IN('ERROR','ACQUIRING','NOT PRICED') AND QTEREV_RECORD_ID='{rev}'""".format(QuoteRecordId=self.contract_quote_record_id,rev =self.contract_quote_revision_record_id))
                    # if getstatus.CNT > 0:
                    #     Sql.RunQuery("""UPDATE SAQTRV SET WORKFLOW_STATUS='CONFIGURE',REVISION_STATUS='CFG-CONFIGURING' WHERE QUOTE_RECORD_ID='{QuoteRecordId}' AND QTEREV_RECORD_ID='{QuoteRevisionRecordId}'""".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id))
                    # else:
                    if self.mode != "Inline Edit":
                        Sql.RunQuery("UPDATE SAQTRV SET WORKFLOW_STATUS = 'PRICING',REVISION_STATUS='PRI-PRICING' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' and QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' ".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id))
                #Log.Info('115--->'+str(self.contract_quote_record_id))
            # INC08641016 - Start - A
            CQCPQC4CWB.writeback_to_c4c("quote_header",self.contract_quote_record_id,self.contract_quote_revision_record_id)
            CQCPQC4CWB.writeback_to_c4c("opportunity_header",self.contract_quote_record_id,self.contract_quote_revision_record_id)
            #A055S000P01-20944 - Start - A
            import CQREVSTSCH
            CQREVSTSCH.Revisionstatusdatecapture(self.contract_quote_record_id,self.contract_quote_revision_record_id)
            #A055S000P01-20944 - End - A
            # INC08641016 - End - A

    def _rolldown_from_coeff_level(self, annual_item_record_id = None):
        if self.mode=="Bulk Edit Rolldown":
            search_condition_modified = str(self.search_condition[:-4])
            if search_condition_modified!="":
                records_affected = (" AND "+str(search_condition_modified))
                #INC09092287 - Start - M
                join_records_affected  = " AND " + (" AND ".join(str(i) for i in search_condition_modified.split(" AND ")))
                #INC09092287 - End - M
            else:
                records_affected = ""
                join_records_affected  = ""
        else:
            records_affected = " AND QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{}' ".format(annual_item_record_id)
            join_records_affected = " AND SAQICO.QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{}' ".format(annual_item_record_id)
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

        # INC08638577 - Start - M
        where_condition = ""
        if self.auto_update_flag == 'True':
            where_condition = " AND SERVICE_ID NOT IN ('Z0117','Z0116','Z0100','Z0046','Z0123') "
        #AIPBNC - Pricebook Non Model Cost
        Sql.RunQuery("UPDATE SAQICO SET AIPBNC = ISNULL(AMNCCI, 0) FROM SAQICO (NOLOCK) WHERE (ISNULL(SAQICO.STATUS,'') IN ('OFFLINE PRICING','CFG-ON HOLD TKM','ACQUIRED') OR (ISNULL(SAQICO.STATUS,'') IN ('PRR-ON HOLD PRICING','CFG-ON HOLD TKM','ACQUIRED') AND GREENBOOK = 'PDC' AND SERVICE_ID in ('Z0091','Z0099','Z0035')) OR (SERVICE_ID in ('Z0117','Z0116','Z0100','Z0046'))) AND QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' {records_affected}".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, records_affected = records_affected))
        #AITPNP - Target Non Model Price
        Sql.RunQuery("UPDATE SAQICO SET AITPNP = ISNULL(ATGKEP,0) + ISNULL(AMNPPI,0) + ISNULL(CAVVPI,0) + ISNULL(HEDBIP,0) + ISNULL(NWPTOP,0) + ISNULL(NUMLPI,0) + ISNULL(SPCCLP,0) + ISNULL(SPCCPI,0) + ISNULL(UIMVPI,0) + ISNULL(ATKNPI,0) + ISNULL(CONSPI,0) + ISNULL(NONCPI,0) + ISNULL(AIUIPI,0) FROM SAQICO (NOLOCK) WHERE (ISNULL(SAQICO.STATUS,'') IN ('OFFLINE PRICING','CFG-ON HOLD TKM','ACQUIRED') OR (ISNULL(SAQICO.STATUS,'') IN ('PRR-ON HOLD PRICING','CFG-ON HOLD TKM','ACQUIRED') AND GREENBOOK = 'PDC' AND SERVICE_ID in ('Z0091','Z0099','Z0035'))) {ancillary_whr} AND QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' {records_affected}".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, records_affected = records_affected, ancillary_whr = where_condition))

        #INC08632060 M
        #AISPNP, AICPNP - Sales, Ceiling, BD Non Model Price
        Sql.RunQuery("UPDATE SAQICO SET AISPNP = ISNULL(ISNULL(AITPNP, 0) * (1-(CONVERT(FLOAT,SADSPC)/100)), 0), AICPNP = ISNULL(ISNULL(AITPNP, 0) * (1+(CONVERT(FLOAT,CEPRUP)/100)), 0) FROM SAQICO (NOLOCK) WHERE (ISNULL(SAQICO.STATUS,'') IN ('OFFLINE PRICING','CFG-ON HOLD TKM','ACQUIRED') OR (ISNULL(SAQICO.STATUS,'') IN ('PRR-ON HOLD PRICING','CFG-ON HOLD TKM','ACQUIRED') AND GREENBOOK = 'PDC' AND SERVICE_ID in ('Z0091','Z0099','Z0035')) OR (SERVICE_ID in ('Z0117','Z0116','Z0100','Z0046','Z0123'))) AND QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' {records_affected}".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, records_affected = records_affected))
        #AIBPNP
        Sql.RunQuery("UPDATE SAQICO SET AIBPNP = ISNULL(ISNULL(AISPNP, 0) * (1-(CONVERT(FLOAT,BDDSPC)/100)), 0) FROM SAQICO (NOLOCK) WHERE (ISNULL(SAQICO.STATUS,'') IN ('OFFLINE PRICING','CFG-ON HOLD TKM','ACQUIRED') OR (ISNULL(SAQICO.STATUS,'') IN ('PRR-ON HOLD PRICING','CFG-ON HOLD TKM','ACQUIRED') AND GREENBOOK = 'PDC' AND SERVICE_ID in ('Z0091','Z0099','Z0035')) OR (SERVICE_ID in ('Z0117','Z0116','Z0100','Z0046','Z0123'))) AND QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' {records_affected}".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, records_affected = records_affected))
        #INC08632060 M
        # INC08699893 - Start - M
        #MTGPRC - Target Model Price - ISNULL(AITPNP,0)
        # INC08696998 - Starts - M
        Sql.RunQuery("UPDATE SAQICO SET MTGPRC = CASE WHEN (ISNULL(SAQICO.STATUS,'') IN ('PRR-ON HOLD PRICING','CFG-ON HOLD TKM','ACQUIRED') AND GREENBOOK = 'PDC' AND SAQICO.SERVICE_ID in ('Z0091','Z0099','Z0035')) THEN 0 WHEN SAQICO.SERVICE_ID in ('Z0117','Z0116','Z0100','Z0046','Z0123') THEN ISNULL(AITPNP,0) WHEN (ISNULL(SAQICO.STATUS,'') IN ('OFFLINE PRICING','CFG-ON HOLD TKM','ACQUIRED') AND ((GREENBOOK != 'PDC' AND SAQICO.SERVICE_ID not in ('Z0091','Z0099','Z0035'))) AND ISNULL(PRSPRV.SSCM_COST, 0) = 0) THEN 0 WHEN ISNULL(FNMDPR/(1-(CONVERT(FLOAT,SADSPC)/100)),0) > ISNULL(TCWISS / (1-(TAPMMP/100)),0) THEN ISNULL(FNMDPR/(1-(CONVERT(FLOAT,SADSPC)/100)),0) * (1 + ISNULL(RKFVDC,0)) ELSE ISNULL(TCWISS / (1-(TAPMMP/100)),0) * (1 + ISNULL(RKFVDC,0)) END FROM SAQICO (NOLOCK) JOIN PRSPRV (NOLOCK) ON PRSPRV.SERVICE_ID = SAQICO.SERVICE_ID WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' {records_affected} AND ISNULL(SAQICO.STATUS,'') IN ('PRR-ON HOLD PRICING','OFFLINE PRICING','CFG-ON HOLD TKM','ACQUIRED')".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, records_affected = join_records_affected))
        # INC08696998 - Ends - M

        #MSLPRC - Sales Model Price
        # INC08719583 start M
        Sql.RunQuery("UPDATE SAQICO SET MSLPRC = CASE WHEN (ISNULL(SAQICO.STATUS,'') IN ('PRR-ON HOLD PRICING','CFG-ON HOLD TKM','ACQUIRED') AND GREENBOOK = 'PDC' AND SAQICO.SERVICE_ID in ('Z0091','Z0099','Z0035')) THEN 0 WHEN SAQICO.SERVICE_ID in ('Z0117','Z0116','Z0100','Z0046','Z0123') THEN ISNULL(AISPNP,0) WHEN (ISNULL(SAQICO.STATUS,'') IN ('OFFLINE PRICING','CFG-ON HOLD TKM','ACQUIRED') AND ((GREENBOOK != 'PDC' AND SAQICO.SERVICE_ID not in ('Z0091','Z0099','Z0035'))) AND ISNULL(PRSPRV.SSCM_COST, 0) = 0) THEN 0 WHEN (ISNULL(SAQICO.STATUS,'') IN ('OFFLINE PRICING','CFG-ON HOLD TKM','ACQUIRED') AND (GREENBOOK IN ('CMP','PPC') AND SAQICO.SERVICE_ID in ('Z0010'))) THEN 0 WHEN ISNULL(FNMDPR,0) > ISNULL(TCWISS / (1-(CONVERT(FLOAT,SAPMMP)/100)),0) THEN ISNULL(FNMDPR,0) * (1 + ISNULL(RKFVDC,0)) ELSE ISNULL(TCWISS / (1-(CONVERT(FLOAT,SAPMMP)/100)),0) * (1 + ISNULL(RKFVDC,0)) END FROM SAQICO (NOLOCK) JOIN PRSPRV (NOLOCK) ON PRSPRV.SERVICE_ID = SAQICO.SERVICE_ID WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' {records_affected} AND ISNULL(SAQICO.STATUS,'') IN ('PRR-ON HOLD PRICING','OFFLINE PRICING','CFG-ON HOLD TKM','ACQUIRED')".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, records_affected = join_records_affected))
        # INC08719583 end M

        #MBDPRC - BD Model Price
        # INC08719583 start M
        Sql.RunQuery("UPDATE SAQICO SET MBDPRC = CASE WHEN (ISNULL(SAQICO.STATUS,'') IN ('PRR-ON HOLD PRICING','CFG-ON HOLD TKM','ACQUIRED') AND GREENBOOK = 'PDC' AND SAQICO.SERVICE_ID in ('Z0091','Z0099','Z0035')) THEN 0 WHEN SAQICO.SERVICE_ID in ('Z0117','Z0116','Z0100','Z0046','Z0123') THEN ISNULL(AIBPNP,0) WHEN (ISNULL(SAQICO.STATUS,'') IN ('OFFLINE PRICING','CFG-ON HOLD TKM','ACQUIRED') AND ((GREENBOOK != 'PDC' AND SAQICO.SERVICE_ID not in ('Z0091','Z0099','Z0035'))) AND ISNULL(PRSPRV.SSCM_COST, 0) = 0) THEN 0 WHEN (ISNULL(SAQICO.STATUS,'') IN ('OFFLINE PRICING','CFG-ON HOLD TKM','ACQUIRED') AND (GREENBOOK IN ('CMP','PPC') AND SAQICO.SERVICE_ID in ('Z0010'))) THEN 0 WHEN ISNULL(FNMDPR * (1-(CONVERT(FLOAT,BDDSPC)/100)) ,0) > ISNULL(TCWISS / (1-(CONVERT(FLOAT,BDPMMP)/100)),0) THEN ISNULL(FNMDPR * (1-(CONVERT(FLOAT,BDDSPC)/100)) ,0) * (1 + ISNULL(RKFVDC,0)) ELSE ISNULL(TCWISS / (1-(CONVERT(FLOAT,BDPMMP)/100)),0) * (1 + ISNULL(RKFVDC,0)) END FROM SAQICO (NOLOCK) JOIN PRSPRV (NOLOCK) ON PRSPRV.SERVICE_ID = SAQICO.SERVICE_ID WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' {records_affected} AND ISNULL(SAQICO.STATUS,'') IN ('PRR-ON HOLD PRICING','OFFLINE PRICING','CFG-ON HOLD TKM','ACQUIRED')".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, records_affected = join_records_affected))
        # INC08719583 end M

        #MCLPRC - Ceiling Model Price
        # INC08719583 - start - m
        # INC08696998 - Starts - M
        Sql.RunQuery("UPDATE SAQICO SET MCLPRC = CASE WHEN (ISNULL(SAQICO.STATUS,'') IN ('PRR-ON HOLD PRICING','CFG-ON HOLD TKM','ACQUIRED') AND GREENBOOK = 'PDC' AND SAQICO.SERVICE_ID in ('Z0091','Z0099','Z0035')) THEN 0 WHEN SAQICO.SERVICE_ID in ('Z0117','Z0116','Z0100','Z0046','Z0123') THEN ISNULL(AICPNP,0) WHEN (ISNULL(SAQICO.STATUS,'') IN ('OFFLINE PRICING','CFG-ON HOLD TKM','ACQUIRED') AND ((GREENBOOK != 'PDC' AND SAQICO.SERVICE_ID not in ('Z0091','Z0099','Z0035'))) AND ISNULL(PRSPRV.SSCM_COST, 0) = 0) THEN 0 WHEN (ISNULL(SAQICO.STATUS,'') IN ('OFFLINE PRICING','CFG-ON HOLD TKM','ACQUIRED') AND (GREENBOOK IN ('CMP','PPC') AND SAQICO.SERVICE_ID in ('Z0010'))) THEN 0 ELSE MTGPRC * (1 + ISNULL(CEPRUP/100,0)) END FROM SAQICO (NOLOCK) JOIN PRSPRV (NOLOCK) ON PRSPRV.SERVICE_ID = SAQICO.SERVICE_ID WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' {records_affected} AND ISNULL(SAQICO.STATUS,'') IN ('PRR-ON HOLD PRICING','OFFLINE PRICING','CFG-ON HOLD TKM','ACQUIRED')".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, records_affected = join_records_affected))
        # INC08696998 - Ends - M
        # INC08719583 - start - m
        # INC08699893 - END - M
        # INC08638577 - End - M

    def _rolldown_from_total_price_level(self, annual_item_record_id=None, updated_fields=''):
        if self.mode=="Bulk Edit Rolldown":
            search_condition_modified = str(self.search_condition[:-4])
            if search_condition_modified!="":
                records_affected = (" AND "+str(search_condition_modified))
                #INC09092287 - Start - M
                join_records_affected  = " AND " + (" AND ".join(str(i) for i in search_condition_modified.split(" AND ")))
                #INC09092287 - End -M
            else:
                records_affected = ""
                join_records_affected  = ""
        else:
            records_affected = " AND QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{}' ".format(annual_item_record_id)
            join_records_affected = " AND SAQICO.QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{}' ".format(annual_item_record_id)
        where_condition = ""
        if self.auto_update_flag == 'True':
            where_condition = " AND SERVICE_ID not in ('Z0123','Z0117','Z0116','Z0046')"
        # INC08813185 - Start - M
        if 'USRPRC' not in updated_fields and 'TGADJP' not in updated_fields: 
            # HEDBIC - Head Break In Cost Impact
            Sql.RunQuery("UPDATE SAQICO SET HEDBIC = (ISNULL(CONVERT(FLOAT,PRCFVA.FACTOR_TXTVAR),0) * ISNULL(SAQICO.TNHRPT,0)) FROM SAQICO (NOLOCK) JOIN MAEQUP (NOLOCK) ON MAEQUP.EQUIPMENT_ID  = SAQICO.EQUIPMENT_ID JOIN PRCFVA (NOLOCK) ON PRCFVA.FACTOR_VARIABLE_ID = MAEQUP.SUBSTRATE_SIZE_GROUP WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' {records_affected} AND SERVICE_ID IN ('Z0091', 'Z0035', 'Z0009') AND HEDBIN = 'Included' AND FACTOR_ID = 'HBWFCT'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, records_affected = join_records_affected))

            # HEDBIP - Head Break In Price Impact
            Sql.RunQuery("UPDATE SAQICO SET HEDBIP = (ISNULL(CONVERT(FLOAT,PRCFVA.FACTOR_TXTVAR),0) * ISNULL(SAQICO.TNHRPT,0)) FROM SAQICO (NOLOCK) JOIN MAEQUP (NOLOCK) ON MAEQUP.EQUIPMENT_ID  = SAQICO.EQUIPMENT_ID JOIN PRCFVA (NOLOCK) ON PRCFVA.FACTOR_VARIABLE_ID = MAEQUP.SUBSTRATE_SIZE_GROUP WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' {records_affected} AND SAQICO.SERVICE_ID IN ('Z0091', 'Z0035', 'Z0009') AND HEDBIN = 'Included' AND FACTOR_ID = 'HBWFPR'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, records_affected = join_records_affected))

            #INC08922527
            # SPCCLC - Specialized Cleaning Cost Impact
            Sql.RunQuery("UPDATE SAQICO SET SPCCLC = (ISNULL(CONVERT(FLOAT,PRCFVA.FACTOR_TXTVAR),0) * ISNULL(SAQICO.TNHRPT,0)) FROM SAQICO (NOLOCK) JOIN PRCFVA (NOLOCK) ON PRCFVA.FACTOR_VARIABLE_ID = SAQICO.SERVICE_ID AND SAQICO.SPCCLN = 'Included' AND ISNULL(PRCFVA.FACTOR_ID,'') = 'AISCCI' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' {records_affected} AND SAQICO.SERVICE_ID IN ('Z0091', 'Z0035', 'Z0009')".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, records_affected = join_records_affected))

            # SPCCLP - Specialized Cleaning Price Impact
            Sql.RunQuery("UPDATE SAQICO SET SPCCLP = (ISNULL(CONVERT(FLOAT,PRCFVA.FACTOR_TXTVAR),0) * ISNULL(SAQICO.TNHRPT,0)) FROM SAQICO (NOLOCK) JOIN PRCFVA (NOLOCK) ON PRCFVA.FACTOR_VARIABLE_ID = SAQICO.SERVICE_ID AND SAQICO.SPCCLN = 'Included' AND ISNULL(PRCFVA.FACTOR_ID,'') = 'AISCPI' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' {records_affected} AND SAQICO.SERVICE_ID IN ('Z0091', 'Z0035', 'Z0009')".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, records_affected = join_records_affected))

            # SPCCCI - Specialized Coating Cost Impact
            Sql.RunQuery("UPDATE SAQICO SET SPCCCI = (ISNULL(CONVERT(FLOAT,PRCFVA.FACTOR_TXTVAR),0) * ISNULL(SAQICO.TNHRPT,0)) FROM SAQICO (NOLOCK) JOIN PRCFVA (NOLOCK) ON PRCFVA.FACTOR_VARIABLE_ID = SAQICO.SERVICE_ID AND SAQICO.SPCCOT = 'Included' AND ISNULL(PRCFVA.FACTOR_ID,'') = 'AISTCI' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' {records_affected} AND SAQICO.SERVICE_ID IN ('Z0091', 'Z0035', 'Z0009')".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, records_affected = join_records_affected))

            # SPCCPI - Specialized Coating Price Impact
            Sql.RunQuery("UPDATE SAQICO SET SPCCPI = (ISNULL(CONVERT(FLOAT,PRCFVA.FACTOR_TXTVAR),0) * ISNULL(SAQICO.TNHRPT,0)) FROM SAQICO (NOLOCK) JOIN PRCFVA (NOLOCK) ON PRCFVA.FACTOR_VARIABLE_ID = SAQICO.SERVICE_ID AND SAQICO.SPCCOT = 'Included' AND ISNULL(PRCFVA.FACTOR_ID,'') = 'AISTPI' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' {records_affected} AND SAQICO.SERVICE_ID IN ('Z0091', 'Z0035', 'Z0009')".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, records_affected = join_records_affected))
            #INC08922527

            # #TOTLCI - Total Cost Impact
            Sql.RunQuery("UPDATE SAQICO SET TOTLCI = ISNULL(CAVVCI,0) + ISNULL(UIMVCI,0) + ISNULL(ATGKEC,0) + ISNULL(AMNCCI,0) + ISNULL(HEDBIC,0) + ISNULL(NWPTOC,0) + ISNULL(NUMLCI,0) + ISNULL(SPCCLC,0) + ISNULL(SPCCCI,0) + ISNULL(ATKNCI,0) + ISNULL(CONSCP,0) + ISNULL(NONCCI,0) + ISNULL(AIUICI,0) FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' {records_affected}".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, records_affected = records_affected))

            #TOTLPI - Total Price Impact
            Sql.RunQuery("UPDATE SAQICO SET TOTLPI = ISNULL(ATGKEP,0) + ISNULL(AMNPPI,0) + ISNULL(CAVVPI,0) + ISNULL(HEDBIP,0) + ISNULL(NWPTOP,0) + ISNULL(NUMLPI,0) + ISNULL(SPCCLP,0) + ISNULL(SPCCPI,0) + ISNULL(UIMVPI,0) + ISNULL(ATKNPI,0) + ISNULL(CONSPI,0) + ISNULL(NONCPI,0) + ISNULL(AIUIPI,0) FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' {records_affected}".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, records_affected = records_affected))

            # INC08638577 - Start - M
            # INC08699893 - Start - M
            #FINPRC - Final Price
            # Removed - Need to check later (+ ISNULL(ADDMPI,0))
            Sql.RunQuery("UPDATE SAQICO SET FINPRC = CASE WHEN ((ISNULL(SAQICO.STATUS,'') IN ('PRR-ON HOLD PRICING','CFG-ON HOLD TKM','ACQUIRED') AND GREENBOOK = 'PDC' AND SERVICE_ID in ('Z0091','Z0099','Z0035')) OR (SERVICE_ID in ('Z0117','Z0116','Z0100','Z0046','Z0123'))) THEN ISNULL(TOTLPI,0) WHEN (ISNULL(SAQICO.STATUS,'') IN ('OFFLINE PRICING','CFG-ON HOLD TKM','ACQUIRED') AND ((GREENBOOK != 'PDC' AND SERVICE_ID not in ('Z0091','Z0099','Z0035')) OR SERVICE_ID not in ('Z0117','Z0116','Z0100','Z0046','Z0123'))) THEN ISNULL(MTGPRC,0) + ISNULL(TOTLPI,0) ELSE ISNULL(MTGPRC,0) + ISNULL(TOTLPI,0) END FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' {records_affected} AND ISNULL(SAQICO.STATUS,'') IN ('PRR-ON HOLD PRICING','CFG-ON HOLD TKM','OFFLINE PRICING','ACQUIRED')".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, records_affected = records_affected))
            # INC08699893 - End- M
            # INC08638577 - End - M

            #FCWOSS - Final Total Cost without Seedstock
            Sql.RunQuery("UPDATE SAQICO SET FCWOSS = ISNULL(TCWOSS,0) + ISNULL(TOTLCI,0) FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' {records_affected}".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, records_affected = records_affected))

            #FCWISS - Final Total Cost with Seedstock
            Sql.RunQuery("UPDATE SAQICO SET FCWISS = ISNULL(TCWISS,0) + ISNULL(TOTLCI,0) FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' {records_affected}".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, records_affected = records_affected))

            #INC08784949 - Start - M
            #SBTCST - Sub Total Cost
            Sql.RunQuery("UPDATE SAQICO SET SBTCST = ISNULL(TCWISS,0) + (ISNULL(CAVVCI,0) + ISNULL(UIMVCI,0) + ISNULL(ATGKEC,0) + ISNULL(HEDBIC,0) + ISNULL(NWPTOC,0) + ISNULL(NUMLCI,0) + ISNULL(SPCCLC,0) + ISNULL(SPCCCI,0)) + ISNULL(ATKNCI,0) + ISNULL(CONSCP,0) + ISNULL(NONCCI,0) + ISNULL(AIUICI,0) + ISNULL(AMNCCI,0) FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' {records_affected}".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, records_affected = records_affected + " AND SERVICE_ID not in ('Z0046','Z0048','Z0123') " if self.mode=="Bulk Edit Rolldown" else records_affected))
            #INC08784949 - End - M

            # INC08638577 - Start - M
            # INC08699893 - Start - M
            # INC08784949 - Start - M
            #SBTPRC - Sub Total Price
            Sql.RunQuery("UPDATE SAQICO SET SBTPRC = CASE WHEN (ISNULL(SAQICO.STATUS,'') IN ('OFFLINE PRICING','CFG-ON HOLD TKM','ACQUIRED') OR (ISNULL(SAQICO.STATUS,'') IN ('PRR-ON HOLD PRICING','CFG-ON HOLD TKM','ACQUIRED') AND GREENBOOK = 'PDC' AND SERVICE_ID in ('Z0091','Z0099','Z0035')) OR (SERVICE_ID in ('Z0117','Z0116','Z0100','Z0046','Z0123'))) THEN (ISNULL(ATGKEP,0) + ISNULL(CAVVPI,0) + ISNULL(HEDBIP,0) + ISNULL(NWPTOP,0) + ISNULL(NUMLPI,0) + ISNULL(SPCCLP,0) + ISNULL(SPCCPI,0) + ISNULL(UIMVPI,0)) + ISNULL(ATKNPI,0) + ISNULL(CONSPI,0) + ISNULL(NONCPI,0) + ISNULL(AIUIPI,0) + ISNULL(AMNPPI,0) ELSE ISNULL(MTGPRC,0) + (ISNULL(ATGKEP,0) + ISNULL(CAVVPI,0) + ISNULL(HEDBIP,0) + ISNULL(NWPTOP,0) + ISNULL(NUMLPI,0) + ISNULL(SPCCLP,0) + ISNULL(SPCCPI,0) + ISNULL(UIMVPI,0)) + ISNULL(ATKNPI,0) + ISNULL(CONSPI,0) + ISNULL(NONCPI,0) + ISNULL(AIUIPI,0)  END FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' {records_affected} AND ISNULL(SAQICO.STATUS,'') IN ('PRR-ON HOLD PRICING','CFG-ON HOLD TKM','OFFLINE PRICING','ACQUIRED')".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, records_affected =  records_affected + " AND SERVICE_ID not in ('Z0046','Z0048','Z0123') " if self.mode=="Bulk Edit Rolldown" else records_affected))
            # INC08784949 - End - M
            # INC08699893 - End - M
            # INC08638577 - Start - M

            #AMNCPE - Additional Manual Cost and Price
            Sql.RunQuery("UPDATE SAQICO SET AMNCPE = 1 FROM SAQICO (NOLOCK) JOIN PRSPRV (NOLOCK) ON PRSPRV.SERVICE_ID = SAQICO.SERVICE_ID WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' {records_affected} AND ISNULL(SAQICO.SBTCST, 0) <= 0 AND ISNULL(SAQICO.SBTPRC, 0) <= 0 AND ISNULL(PRSPRV.SSCM_COST,0) = 0 AND ISNULL(SAQICO.SERVICE_ID,'') NOT IN ('Z0101')".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, records_affected = join_records_affected))

            #A055S000P01-20640 - Start
            Sql.RunQuery("UPDATE SAQICO SET AMNCPE = 1 FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' {records_affected} AND ISNULL(SAQICO.SBTCST, 0) <= 0 AND ISNULL(SAQICO.SBTPRC, 0) <= 0 AND ISNULL(SAQICO.SERVICE_ID,'') IN ('Z0010','Z0128') AND SAQICO.GREENBOOK IN ('CMP','PPC')".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, records_affected = records_affected))
            #A055S000P01-20640 - End

            Sql.RunQuery("UPDATE SAQICO SET AMNCPE = 1 FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' {records_affected} AND ISNULL(SAQICO.SBTCST, 0) <= 0 AND ISNULL(SAQICO.SBTPRC, 0) <= 0 AND ISNULL(SAQICO.SERVICE_ID,'') IN ('Z0091','Z0099','Z0035') AND SAQICO.GREENBOOK = 'PDC'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, records_affected = records_affected))

            #AMNCPI - Additional Manual Cost and Price Complet
            Sql.RunQuery("UPDATE SAQICO SET AMNCPI = CASE WHEN ISNULL(SAQICO.AMNCPE, 0) = 1 AND (ISNULL(SAQICO.AMNCCI,0) > 0 AND ISNULL(SAQICO.AMNPPI,0) > 0) THEN 'ACTIVE' WHEN ISNULL(SAQICO.AMNCPE, 0) = 1 AND (ISNULL(SAQICO.AMNCCI,0) <= 0 OR ISNULL(SAQICO.AMNPPI,0) <= 0) THEN 'INACTIVE' ELSE null END FROM SAQICO (NOLOCK) JOIN PRSPRV (NOLOCK) ON PRSPRV.SERVICE_ID = SAQICO.SERVICE_ID WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' {records_affected} AND ISNULL(SAQICO.AMNCPE, 0) = 1 AND ISNULL(PRSPRV.SSCM_COST,0) = 0 AND ISNULL(SAQICO.SERVICE_ID,'') NOT IN ('Z0100','Z0101')".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, records_affected = join_records_affected))
            # A055S000P01-19721 - Start
            #AIUICC - Upt Impr Cost and Price Complete
            Sql.RunQuery("UPDATE SAQICO SET AIUICC = CASE WHEN ISNULL(SAQICO.AIUICI, 0) > 0 AND ISNULL(SAQICO.AIUIPI, 0) > 0 THEN 1 WHEN CAST(SAQICO.ITSDUI as NUMERIC(13,3)) > '2.000' THEN 0 ELSE null END FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' {records_affected}".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, records_affected = records_affected))

            #AIFCPE - Final Total Cost Per Event
            Sql.RunQuery("UPDATE SAQICO SET AIFCPE = FCWISS / ISNULL(ADJ_PM_FREQUENCY,0) FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' {records_affected} AND ISNULL(ADJ_PM_FREQUENCY,0) > 0 AND UPPER(QTETYP) IN ('FLEX EVENT BASED','EVENT BASED') ".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, records_affected = records_affected))

            # INC08638577 - Start - M
            #SLSPRC / BDVPRC /CELPRC - Target / Sales / BD / Ceiling Price
            # Sql.RunQuery("UPDATE SAQICO SET SLSPRC = CASE WHEN (ISNULL(SAQICO.STATUS,'') IN ('OFFLINE PRICING','ACQUIRED') OR (ISNULL(SAQICO.STATUS,'') IN ('PRR-ON HOLD PRICING','ACQUIRED') AND GREENBOOK = 'PDC' AND SERVICE_ID in ('Z0091','Z0099','Z0035')) OR (SERVICE_ID in ('Z0117','Z0116','Z0100','Z0046','Z0123'))) THEN ISNULL(MSLPRC,0) ELSE ISNULL(MSLPRC,0) + ISNULL(TOTLPI,0) END, BDVPRC = CASE WHEN (ISNULL(SAQICO.STATUS,'') IN ('OFFLINE PRICING','ACQUIRED') OR (ISNULL(SAQICO.STATUS,'') IN ('PRR-ON HOLD PRICING','ACQUIRED') AND GREENBOOK = 'PDC' AND SERVICE_ID in ('Z0091','Z0099','Z0035')) OR (SERVICE_ID in ('Z0117','Z0116','Z0100','Z0046','Z0123'))) THEN ISNULL(MBDPRC,0) ELSE ISNULL(MBDPRC,0) + ISNULL(TOTLPI,0) END, CELPRC = CASE WHEN ISNULL(MCLPRC,0)= 0 THEN ISNULL(TOTLPI,0) + (ISNULL(TOTLPI,0) * ISNULL(CEPRUP,0)/100) WHEN (ISNULL(SAQICO.STATUS,'') IN ('OFFLINE PRICING','ACQUIRED') OR (ISNULL(SAQICO.STATUS,'') IN ('PRR-ON HOLD PRICING','ACQUIRED') AND GREENBOOK = 'PDC' AND SERVICE_ID in ('Z0091','Z0099','Z0035')) OR (SERVICE_ID in ('Z0117','Z0116','Z0100','Z0046','Z0123'))) THEN ISNULL(MCLPRC,0) ELSE ISNULL(MCLPRC,0) + ISNULL(TOTLPI,0) END FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{AnnualItemRecordId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, AnnualItemRecordId=annual_item_record_id))
            # INC08699893 - Start - M
            # INC08719583 - start - M
            # INC08784949 - End - M
            Sql.RunQuery("UPDATE SAQICO SET SLSPRC = CASE WHEN ((ISNULL(SAQICO.STATUS,'') IN ('PRR-ON HOLD PRICING','CFG-ON HOLD TKM','ACQUIRED') AND GREENBOOK = 'PDC' AND SAQICO.SERVICE_ID in ('Z0091','Z0099','Z0035'))) THEN ISNULL(AISPNP,0) WHEN (SAQICO.SERVICE_ID in ('Z0117','Z0116','Z0100','Z0046','Z0123')) THEN ISNULL(MSLPRC,0) WHEN (ISNULL(SAQICO.STATUS,'') IN ('OFFLINE PRICING','CFG-ON HOLD TKM','ACQUIRED') AND ((GREENBOOK != 'PDC' AND SAQICO.SERVICE_ID not in ('Z0091','Z0099','Z0035'))) AND ISNULL(PRSPRV.SSCM_COST, 0) = 0) THEN ISNULL(AISPNP,0) WHEN (ISNULL(SAQICO.STATUS,'') IN ('OFFLINE PRICING','CFG-ON HOLD TKM','ACQUIRED') AND (GREENBOOK IN ('CMP','PPC') AND SAQICO.SERVICE_ID in ('Z0010'))) THEN ISNULL(AISPNP,0) ELSE ISNULL(MSLPRC,0) + ISNULL(TOTLPI,0) END, BDVPRC = CASE WHEN ((ISNULL(SAQICO.STATUS,'') IN ('PRR-ON HOLD PRICING','CFG-ON HOLD TKM','ACQUIRED') AND GREENBOOK = 'PDC' AND SAQICO.SERVICE_ID in ('Z0091','Z0099','Z0035'))) THEN ISNULL(AIBPNP,0) WHEN (SAQICO.SERVICE_ID in ('Z0117','Z0116','Z0100','Z0046','Z0123')) THEN  ISNULL(MBDPRC,0) WHEN (ISNULL(SAQICO.STATUS,'') IN ('OFFLINE PRICING','CFG-ON HOLD TKM','ACQUIRED') AND ((GREENBOOK != 'PDC' AND SAQICO.SERVICE_ID not in ('Z0091','Z0099','Z0035'))) AND ISNULL(PRSPRV.SSCM_COST, 0) = 0) THEN ISNULL(AIBPNP,0) WHEN (ISNULL(SAQICO.STATUS,'') IN ('OFFLINE PRICING','CFG-ON HOLD TKM','ACQUIRED') AND (GREENBOOK IN ('CMP','PPC') AND SAQICO.SERVICE_ID in ('Z0010'))) THEN ISNULL(AIBPNP,0) ELSE ISNULL(MBDPRC,0) + ISNULL(TOTLPI,0) END, CELPRC = CASE WHEN ISNULL(MCLPRC,0)= 0 THEN ISNULL(TOTLPI,0) + (ISNULL(TOTLPI,0) * ISNULL(CEPRUP,0)/100) 	WHEN ((ISNULL(SAQICO.STATUS,'') IN ('PRR-ON HOLD PRICING','CFG-ON HOLD TKM','ACQUIRED') AND GREENBOOK = 'PDC' AND SAQICO.SERVICE_ID in ('Z0091','Z0099','Z0035'))) THEN ISNULL(MCLPRC,0) + ISNULL(TOTLPI,0) WHEN (SAQICO.SERVICE_ID in ('Z0117','Z0116','Z0100','Z0046','Z0123')) THEN ISNULL(MCLPRC,0) WHEN (ISNULL(SAQICO.STATUS,'') IN ('OFFLINE PRICING','CFG-ON HOLD TKM','ACQUIRED') AND ((GREENBOOK != 'PDC' AND SAQICO.SERVICE_ID not in ('Z0091','Z0099','Z0035'))) AND ISNULL(PRSPRV.SSCM_COST, 0) = 0) THEN ISNULL(MCLPRC,0) + ISNULL(TOTLPI,0) WHEN (ISNULL(SAQICO.STATUS,'') IN ('OFFLINE PRICING','CFG-ON HOLD TKM','ACQUIRED') AND (GREENBOOK IN ('CMP','PPC') AND SAQICO.SERVICE_ID in ('Z0010'))) THEN ISNULL(MCLPRC,0) + ISNULL(TOTLPI,0) ELSE ISNULL(MCLPRC,0) + ISNULL(TOTLPI,0) END FROM SAQICO (NOLOCK) JOIN PRSPRV (NOLOCK) ON PRSPRV.SERVICE_ID = SAQICO.SERVICE_ID WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' {records_affected} AND ISNULL(SAQICO.STATUS,'') IN ('PRR-ON HOLD PRICING','CFG-ON HOLD TKM','OFFLINE PRICING','ACQUIRED')".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, records_affected = join_records_affected + " AND SAQICO.SERVICE_ID not in ('Z0046','Z0048','Z0123')" if self.mode=="Bulk Edit Rolldown" else join_records_affected))
            # INC08719583 end - M
            # INC08784949 - End - M

            # INC08756683 - Start - M
            #A055S000P01-20625 - Start
            #TRGPRC
            Sql.RunQuery("UPDATE SAQICO SET TRGPRC = CASE WHEN ((ISNULL(SAQICO.STATUS,'') IN ('PRR-ON HOLD PRICING','CFG-ON HOLD TKM','ACQUIRED') AND GREENBOOK = 'PDC' AND SAQICO.SERVICE_ID in ('Z0091','Z0099','Z0035'))) THEN ISNULL(AITPNP,0) WHEN (SAQICO.SERVICE_ID in ('Z0117','Z0116','Z0100','Z0046','Z0123')) THEN ISNULL(AITPNP,0) WHEN (ISNULL(SAQICO.STATUS,'') IN ('OFFLINE PRICING','CFG-ON HOLD TKM','ACQUIRED') AND ((GREENBOOK != 'PDC' AND SAQICO.SERVICE_ID not in ('Z0091','Z0099','Z0035'))) AND ISNULL(PRSPRV.SSCM_COST, 0) = 0) THEN ISNULL(AITPNP,0) ELSE ISNULL(MTGPRC,0) + ISNULL(TOTLPI,0) END FROM SAQICO (NOLOCK) JOIN PRSPRV (NOLOCK) ON PRSPRV.SERVICE_ID = SAQICO.SERVICE_ID WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' {records_affected} AND ISNULL(SAQICO.STATUS,'') IN ('PRR-ON HOLD PRICING','CFG-ON HOLD TKM','OFFLINE PRICING','ACQUIRED')".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, records_affected = join_records_affected + " AND SAQICO.SERVICE_ID not in ('Z0046','Z0048','Z0123')" if self.mode=="Bulk Edit Rolldown" else join_records_affected))
            #A055S000P01-20625 - End
            # INC08699893 - END - M
            # INC08638577 - End - M
            # INC08756683 - End - M

            #AIUPPE - User Price Per Event Kit
            Sql.RunQuery("UPDATE SAQICO SET AIUPPE = TRGPRC / ADJ_PM_FREQUENCY FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' {records_affected} AND ISNULL(ADJ_PM_FREQUENCY,0) > 0 AND UPPER(QTETYP) IN ('FLEX EVENT BASED','EVENT BASED') ".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, records_affected = records_affected))
        # INC08813185 - End - M
        #USRPRC / TGADJP - User Price / Target User Price Adjustment
        Trace.Write("=================>>>> "+str(updated_fields))
        if 'USRPRC' not in updated_fields:
            Sql.RunQuery("UPDATE SAQICO SET USRPRC = TRGPRC FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' {records_affected}".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, records_affected = records_affected))
        if 'TGADJP' not in updated_fields:
            Sql.RunQuery("UPDATE SAQICO SET TGADJP = ((TRGPRC - USRPRC) / TRGPRC * -1) * 100 FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' {records_affected} {WhereCondition}".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, records_affected = records_affected, WhereCondition =  where_condition))
        else:
            Sql.RunQuery("UPDATE SAQICO SET USRPRC = TRGPRC + (TRGPRC * (TGADJP / 100)) FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' {records_affected} {WhereCondition}".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, records_affected = records_affected, WhereCondition =  where_condition))
        #CNTPRC - Contractual Price
        #A055S000P01-21105 Start - M
        Sql.RunQuery("UPDATE SAQICO SET CNTPRC = ((USRPRC / 365) * CNTDAY * ISNULL(CTPDFP ,1) ) * (1 - (ISNULL(YOYPCT,0)/100)) FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' {records_affected} AND SERVICE_ID NOT IN ('Z0100','Z0101','Z0123') {WhereCondition}".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, records_affected = records_affected, WhereCondition =  where_condition))
        #A055S000P01-21105 End - M

        #INC08858696-M starts
        #INC08874274 - Start - M
        Sql.RunQuery("UPDATE SAQICO SET CNTPRC = ((USRPRC / 365) * CNTDAY * ISNULL(CTPDFP ,1) ) * (1 - (ISNULL(YOYPCT,0)/100)) FROM SAQICO (NOLOCK) WHERE  QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' {records_affected} AND SERVICE_ID IN ('Z0100','Z0101') AND ISNULL(CNSMBL_ENT,'') in ('Included','Some Inclusions') {WhereCondition}".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, records_affected = records_affected, WhereCondition =  where_condition))
        if self.auto_update_flag == 'True':
            Sql.RunQuery("UPDATE SAQICO SET CNTPRC = USRPRC FROM SAQICO (NOLOCK) WHERE  QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' {records_affected} AND SERVICE_ID NOT IN ('Z0100','Z0101') AND ISNULL(CNSMBL_ENT,'') NOT IN ('Included','Some Inclusions')".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, records_affected = records_affected ))
        #INC08874274 - End - M
        #INC08858696-M ends

        #CNTCST - Contractual Cost
        Sql.RunQuery("UPDATE SAQICO SET CNTCST = ((FCWISS / 365) * CNTDAY ) FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' {records_affected} AND SERVICE_ID NOT IN ('Z0100','Z0101')".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, records_affected = records_affected))

        #CNTMGN - Contractual Margin
        Sql.RunQuery("UPDATE SAQICO SET CNTMGN = CNTPRC - CNTCST FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' {records_affected} AND SERVICE_ID NOT IN ('Z0100','Z0101')".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, records_affected = records_affected))

        #AICCPE - Price Per Event Kit
        Sql.RunQuery("UPDATE SAQICO SET AICCPE = CNTCST / ADJ_PM_FREQUENCY FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' {records_affected} AND UPPER(QTETYP) IN ('FLEX EVENT BASED','EVENT BASED') AND ISNULL(ADJ_PM_FREQUENCY,0)>0".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, records_affected = records_affected))

        #INC08597652 - Start - A
        #AICPPE - Contractual Price Per Event/Kit
        Sql.RunQuery("UPDATE SAQICO SET AICPPE = CNTPRC / ADJ_PM_FREQUENCY FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' {records_affected} AND UPPER(QTETYP) IN ('FLEX EVENT BASED','EVENT BASED') AND ISNULL(ADJ_PM_FREQUENCY,0)>0".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, records_affected = records_affected))
        #INC08597652 - End - A

        #SPCTPR /SPCTCS - Spares Contractual Price / Cost
        Sql.RunQuery("UPDATE SAQICO SET SPCTPR = CNTPRC * SPSPCT, SPCTCS = CNTCST * SPSPCT FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' {records_affected}".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, records_affected = records_affected))

        #SPCTMG - Spares Contractual Margin
        Sql.RunQuery("UPDATE SAQICO SET SPCTMG = (SPCTPR - SPCTCS) / SPCTPR FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' {records_affected}".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, records_affected = records_affected))

        #SVCTPR /SVCTCS - Service Contractual Price / Cost
        Sql.RunQuery("UPDATE SAQICO SET SVCTPR = CNTPRC * SVSPCT, SVCTCS = CNTCST * SVSPCT FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' {records_affected}".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, records_affected = records_affected))

        #SVCTMG - Service Contractual Margin
        Sql.RunQuery("UPDATE SAQICO SET SVCTMG = (SVCTPR - SVCTCS) / SVCTPR FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' {records_affected}".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, records_affected = records_affected))


        #TNTVGC / TNTMGC / TNTMPC - Total Net Value / Total Net Value in Margin / Margin % (Global Currency)
        Sql.RunQuery("UPDATE SAQICO SET TNTVGC = CNTPRC, TNTMGC = CNTPRC - CNTCST, TNTMPC = (CNTPRC - CNTCST) / CNTPRC FROM SAQICO(NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' {records_affected} AND BILTYP <> 'VARIABLE' AND (ISNULL(CNTPRC,0)>0 OR  SERVICE_ID IN ('Z0116','Z0117') )".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, records_affected = records_affected))

        #TENVGC - Estimated Value (Global Currency)
        Sql.RunQuery("UPDATE SAQICO SET TENVGC = CNTPRC, TNTMGC = CNTPRC - CNTCST FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' {records_affected} AND BILTYP = 'VARIABLE'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, records_affected = records_affected))

        #TAXVGC - Tax Amount (Global Currency)
        Sql.RunQuery("UPDATE SAQICO SET TAXVGC = TNTVGC * (ISNULL(TAXVTP,0)/100) FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' {records_affected}".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, records_affected = records_affected))

        #TAMTGC - Total Amount (Global Currency)
        Sql.RunQuery("UPDATE SAQICO SET TAMTGC = TNTVGC + ISNULL(TAXVGC,0) FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' {records_affected}".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, records_affected = records_affected))

        #TAMTGC - Total Amount (Global Currency) - Variable
        Sql.RunQuery("UPDATE SAQICO SET TAMTGC = TENVGC FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' {records_affected} AND ISNULL(BILTYP,'') = 'VARIABLE'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, records_affected = records_affected))

        # INC08627904 - Start - M
        # currency_rounding_obj = Sql.GetFirst("SELECT DISTINCT CASE WHEN ROUNDING_DECIMAL_PLACES = '' THEN 0 ELSE ROUNDING_DECIMAL_PLACES END  AS DECIMAL_PLACES, CASE WHEN ROUNDING_METHOD='ROUND DOWN' THEN 1 ELSE 0 END AS ROUNDING_METHOD FROM SAQRIT(NOLOCK) JOIN PRCURR (NOLOCK) ON SAQRIT.DOC_CURRENCY = PRCURR.CURRENCY WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' ".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id))
        # if currency_rounding_obj:
        #Round Off
        Sql.RunQuery("UPDATE SAQICO SET TAMTGC = ROUND(SAQICO.TAMTGC ,CONVERT(INT,CASE WHEN ROUNDING_DECIMAL_PLACES = '' THEN 0 ELSE ROUNDING_DECIMAL_PLACES END),CONVERT(INT,CASE WHEN ROUNDING_METHOD='ROUND DOWN' THEN 1 ELSE 0 END)), TAXVGC = ROUND(SAQICO.TAXVGC ,CONVERT(INT,CASE WHEN ROUNDING_DECIMAL_PLACES = '' THEN 0 ELSE ROUNDING_DECIMAL_PLACES END),CONVERT(INT,CASE WHEN ROUNDING_METHOD='ROUND DOWN' THEN 1 ELSE 0 END)), TNTVGC = ROUND(SAQICO.TNTVGC ,CONVERT(INT,CASE WHEN ROUNDING_DECIMAL_PLACES = '' THEN 0 ELSE ROUNDING_DECIMAL_PLACES END),CONVERT(INT,CASE WHEN ROUNDING_METHOD='ROUND DOWN' THEN 1 ELSE 0 END)) FROM SAQICO (NOLOCK) JOIN PRCURR (NOLOCK) ON SAQICO.GLOBAL_CURRENCY = PRCURR.CURRENCY WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' {records_affected} AND SAQICO.SERVICE_ID  NOT IN ('Z0123','Z0046','Z0100','Z0116','Z0117')".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, records_affected = join_records_affected))
        #Round Off
        Sql.RunQuery("UPDATE SAQICO SET TAMTGC = ROUND(SAQICO.TAMTGC ,CONVERT(INT,CASE WHEN ROUNDING_DECIMAL_PLACES = '' THEN 0 ELSE ROUNDING_DECIMAL_PLACES END),CONVERT(INT,CASE WHEN ROUNDING_METHOD='ROUND DOWN' THEN 1 ELSE 0 END)) FROM SAQICO (NOLOCK) JOIN PRCURR (NOLOCK) ON SAQICO.GLOBAL_CURRENCY = PRCURR.CURRENCY WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' {records_affected} AND ISNULL(SAQICO.BILTYP,'') = 'VARIABLE' AND SAQICO.SERVICE_ID  NOT IN ('Z0123','Z0046','Z0100','Z0116','Z0117')".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, records_affected = join_records_affected))
        # INC08638273 - Start - M
        #TNTVDC / TAXVDC / TAMTDC /TENVDC - Total Net Value / Tax / Total Amount/ Estimated (Document Currency) 
        Sql.RunQuery("UPDATE SAQICO SET TNTVDC = ROUND( (SAQICO.TNTVGC * ISNULL(SAQICO.DCCRFX,1)) ,CONVERT(INT,CASE WHEN ROUNDING_DECIMAL_PLACES = '' THEN 0 ELSE ROUNDING_DECIMAL_PLACES END),CONVERT(INT,CASE WHEN ROUNDING_METHOD='ROUND DOWN' THEN 1 ELSE 0 END)), TAXVDC = ROUND( (SAQICO.TAXVGC * ISNULL(SAQICO.DCCRFX,1)) ,CONVERT(INT,CASE WHEN ROUNDING_DECIMAL_PLACES = '' THEN 0 ELSE ROUNDING_DECIMAL_PLACES END),CONVERT(INT,CASE WHEN ROUNDING_METHOD='ROUND DOWN' THEN 1 ELSE 0 END)), TAMTDC = ROUND( (SAQICO.TAMTGC * ISNULL(SAQICO.DCCRFX,1)) ,CONVERT(INT,CASE WHEN ROUNDING_DECIMAL_PLACES = '' THEN 0 ELSE ROUNDING_DECIMAL_PLACES END),CONVERT(INT,CASE WHEN ROUNDING_METHOD='ROUND DOWN' THEN 1 ELSE 0 END)), TENVDC = ROUND( (SAQICO.TENVGC * ISNULL(SAQICO.DCCRFX,1)) ,CONVERT(INT,CASE WHEN ROUNDING_DECIMAL_PLACES = '' THEN 0 ELSE ROUNDING_DECIMAL_PLACES END),CONVERT(INT,CASE WHEN ROUNDING_METHOD='ROUND DOWN' THEN 1 ELSE 0 END)) FROM SAQICO (NOLOCK) JOIN PRCURR (NOLOCK) ON SAQICO.DOCCUR = PRCURR.CURRENCY WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' {records_affected} AND SAQICO.SERVICE_ID  NOT IN ('Z0123','Z0046','Z0100','Z0116','Z0117')".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, records_affected = join_records_affected))
        # INC08638273 - End - M
        # Rounding will be done in another script(CQIFWUDQTM) for ancillary products
        Sql.RunQuery("UPDATE SAQICO SET TNTVDC = TNTVGC * ISNULL(DCCRFX,1), TAXVDC = TAXVGC * ISNULL(DCCRFX,1), TAMTDC = TAMTGC * ISNULL(DCCRFX,1), TENVDC = TENVGC * ISNULL(DCCRFX,1) FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' {records_affected} AND SERVICE_ID  IN ('Z0123','Z0046','Z0100','Z0116','Z0117')".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, records_affected = records_affected))
        # INC08627904 - End - M

        #Status
        Sql.RunQuery("UPDATE SAQICO SET STATUS = CASE WHEN ISNULL(SAQICO.AMNCPI, '') = 'ACTIVE' AND (ISNULL(SAQICO.AMNCCI,0) > 0 AND ISNULL(SAQICO.AMNPPI,0) > 0) THEN 'ACQUIRED' WHEN ISNULL(SAQICO.AMNCPI, '') = 'INACTIVE' AND (ISNULL(SAQICO.AMNCCI,0) <= 0 OR ISNULL(SAQICO.AMNPPI,0) <= 0) THEN 'OFFLINE PRICING' ELSE SAQICO.STATUS END FROM SAQICO (NOLOCK) JOIN PRSPRV (NOLOCK) ON PRSPRV.SERVICE_ID = SAQICO.SERVICE_ID WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' {records_affected} AND ISNULL(PRSPRV.SSCM_COST,0) = 0 AND ISNULL(SAQICO.SERVICE_ID,'') NOT IN ('Z0100','Z0101')".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, records_affected = records_affected))

        #Status - For SSCM pricing offerings - Additional Target KPI != 'Excluded'
        Sql.RunQuery("UPDATE SAQICO SET STATUS = 'ACQUIRED' FROM SAQICO (NOLOCK) JOIN PRSPRV (NOLOCK) ON PRSPRV.SERVICE_ID = SAQICO.SERVICE_ID WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' {records_affected} AND ISNULL(PRSPRV.SSCM_COST,0) = 1".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, records_affected = join_records_affected))

        # INC08668632 A
        #update status for Z0123
        Sql.RunQuery("UPDATE SAQICO SET STATUS = 'ACQUIRED' FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SERVICE_ID='Z0123' {records_affected}".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, records_affected = records_affected))
        # INC08668632 A

        #Z0100 OFFLINE PRICING
        #INC08858696-M starts
        #INC09067815/A055S000P01-21000 starts-M
        if self.auto_update_flag != 'True':#312
            Sql.RunQuery("UPDATE SAQICO SET STATUS = 'ACQUIRED' FROM SAQICO (NOLOCK)  WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' {records_affected} AND ISNULL(CNSMBL_ENT,'') in ('Included','Some Inclusions') AND SERVICE_ID ='Z0100'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, records_affected = records_affected))
        #INC09067815/A055S000P01-21000 ends-M
        #INC08858696-M ends
        #A055S000P01-20515 To prevent offline products ('Z0090','Z0006','Z0007') to acquired without filling CAT4's
        #INC08754197 - Start - M
        # INC08784949 - Start - M
        Sql.RunQuery("UPDATE SAQICO SET STATUS = CASE  WHEN ( ISNULL(ATGKEY, 'Excluded') not in ('Excluded','Exception') AND ( ISNULL(ATGKEC, 0) <= 0 AND ISNULL(ATGKEP, 0) <= 0 ) ) THEN 'PRR-ON HOLD PRICING' WHEN ( ISNULL(NWPTON, '') = 'YES' AND ( ISNULL(NWPTOC, 0) <= 0 AND ISNULL(NWPTOP, 0) <= 0 ) ) THEN 'PRR-ON HOLD PRICING' WHEN ( ISNULL(CNSMBL_ENT, '') IN ('Some Inclusions', 'Some Exclusions' ) AND ( ISNULL(CONSCP, 0) <= 0 AND ISNULL(CONSPI, 0) <= 0 )) THEN 'PRR-ON HOLD PRICING' WHEN ( ISNULL(NCNSMB_ENT, '') IN ('Some Inclusions', 'Some Exclusions' ) AND ( ISNULL(NONCCI, 0) = 0 AND ISNULL(NONCPI, 0) = 0 ) ) THEN 'PRR-ON HOLD PRICING' WHEN ( ISNULL(TGKPNS, 'Excluded') not in ('','Excluded') AND ( ISNULL(ATKNCI, 0) <= 0 AND ISNULL(ATKNPI, 0) <= 0 ) ) THEN 'PRR-ON HOLD PRICING' WHEN ( ISNULL(AMNCPE, 0) = 1 AND ( ISNULL(AMNCCI, 0) <= 0 AND ISNULL(AMNPPI, 0) <= 0 ) ) THEN 'PRR-ON HOLD PRICING' WHEN ISNULL(SAQICO.aiuicc, 1) = 0 THEN 'PRR-ON HOLD PRICING' ELSE 'ACQUIRED' END FROM   SAQICO (nolock) JOIN PRSPRV (nolock) ON PRSPRV.SERVICE_ID = SAQICO.SERVICE_ID WHERE  QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' {records_affected} AND ISNULL(PRSPRV.SSCM_COST, 0) = 0 AND SAQICO.SERVICE_ID IN ('Z0090','Z0006','Z0007') ".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, records_affected = join_records_affected))
        #INC08754197 - Start - M
        Sql.RunQuery("UPDATE SAQICO SET STATUS = 'PRR-ON HOLD PRICING' FROM SAQICO (NOLOCK) JOIN PRSPRV (NOLOCK) ON PRSPRV.SERVICE_ID = SAQICO.SERVICE_ID WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' {records_affected} AND ISNULL(PRSPRV.SSCM_COST,0) = 1 AND ( (ISNULL(ATGKEY,'Excluded') not in ('Excluded','Exception') AND (ISNULL(ATGKEC,0) <= 0 AND ISNULL(ATGKEP,0) <= 0)) OR (ISNULL(NWPTON,'') = 'YES' AND (ISNULL(NWPTOC,0) <= 0 AND ISNULL(NWPTOP,0) <= 0)) OR (ISNULL(CNSMBL_ENT,'') in ('Some Inclusions','Some Exclusions') AND (ISNULL(CONSCP,0) <= 0 AND ISNULL(CONSPI,0) <= 0)) OR (ISNULL(NCNSMB_ENT,'') in ('Some Inclusions','Some Exclusions') AND (ISNULL(NONCCI,0) = 0 AND ISNULL(NONCPI,0) = 0)) OR (ISNULL(TGKPNS,'Excluded') not in ('','Excluded') AND (ISNULL(ATKNCI,0) <= 0 AND ISNULL(ATKNPI,0) <= 0)) OR (ISNULL(AMNCPE,0) = 1 AND (ISNULL(AMNCCI,0) <= 0 AND ISNULL(AMNPPI,0) <= 0)) OR ISNULL(SAQICO.AIUICC,1) = 0) AND SAQICO.SERVICE_ID <> 'Z0092'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, records_affected = join_records_affected))

        Sql.RunQuery("UPDATE SAQICO SET STATUS = 'PRR-ON HOLD PRICING' FROM SAQICO (NOLOCK) JOIN PRSPRV (NOLOCK) ON PRSPRV.SERVICE_ID = SAQICO.SERVICE_ID WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' {records_affected} AND ISNULL(PRSPRV.SSCM_COST,0) = 1 AND (  (ISNULL(ATGKEY,'Excluded')  not in ('Excluded','Exception') AND (ISNULL(ATGKEC,0) <= 0 AND ISNULL(ATGKEP,0) <= 0)) OR (ISNULL(NWPTON,'') = 'YES' AND (ISNULL(NWPTOC,0) <= 0 AND ISNULL(NWPTOP,0) <= 0)) OR (ISNULL(CNSMBL_ENT,'') = 'Some Exclusions' AND (ISNULL(CONSCP,0) <= 0 AND ISNULL(CONSPI,0) <= 0)) OR (ISNULL(NCNSMB_ENT,'') in ('Some Inclusions','Some Exclusions') AND (ISNULL(NONCCI,0) = 0 AND ISNULL(NONCPI,0) = 0)) OR (ISNULL(TGKPNS,'Excluded') not in ('','Excluded') AND (ISNULL(ATKNCI,0) <= 0 AND ISNULL(ATKNPI,0) <= 0)) OR (ISNULL(AMNCPE,0) = 1 AND (ISNULL(AMNCCI,0) <= 0 AND ISNULL(AMNPPI,0) <= 0)) OR ISNULL(SAQICO.AIUICC,1) = 0) AND SAQICO.SERVICE_ID = 'Z0092'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, records_affected = join_records_affected))
        #INC08754197 - End - M
        # INC08784949 - End - M

        #Status - On Hold TKM
        #INC08773833 - Start - M
        Sql.RunQuery("UPDATE SAQICO SET STATUS = 'CFG-ON HOLD TKM' FROM SAQICO (NOLOCK) JOIN SAQGPA (NOLOCK) ON SAQICO.QUOTE_ID = SAQGPA.QUOTE_ID AND SAQICO.QTEREV_ID = SAQGPA.QTEREV_ID AND SAQICO.SERVICE_ID = SAQGPA.SERVICE_ID AND SAQICO.EQUIPMENT_ID = SAQGPA.EQUIPMENT_ID WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' {records_affected} AND  ISNULL(SAQICO.STATUS,'') NOT IN ('PRR-ON HOLD PRICING','CFG-ON HOLD - COSTING','ASSEMBLY IS MISSING') AND ISNULL(SAQGPA.KIT_ID,'')<>'' AND ISNULL(SAQGPA.KIT_NUMBER,'')='' AND SAQGPA.INCLUDED = 1".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, records_affected = join_records_affected))
        #INC08773833 - End - M

        Sql.RunQuery("UPDATE SAQICO SET STATUS = 'CFG-ON HOLD TKM' FROM SAQICO (NOLOCK) JOIN SAQSAP (NOLOCK) ON SAQICO.QUOTE_ID = SAQSAP.QUOTE_ID AND SAQICO.QTEREV_ID = SAQSAP.QTEREV_ID AND SAQICO.SERVICE_ID = SAQSAP.SERVICE_ID AND SAQICO.EQUIPMENT_ID = SAQSAP.EQUIPMENT_ID WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' {records_affected} AND ISNULL(SAQICO.STATUS,'') NOT IN ('PRR-ON HOLD PRICING','CFG-ON HOLD - COSTING','ASSEMBLY IS MISSING') AND ISNULL(SAQSAP.KIT_ID,'')<>'' AND ISNULL(SAQSAP.KIT_NUMBER,'')=''".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, records_affected = join_records_affected))

        # INC08813185 - Start - A
        # Service based status update --> ('Z0046','Z0123','Z0116','Z0117','Z0048','Z0101')
        Sql.RunQuery("UPDATE SAQICO SET STATUS = 'ACQUIRED' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SERVICE_ID IN ('Z0046','Z0123','Z0116','Z0117','Z0048','Z0101') {records_affected} ".format(QuoteRecordId= self.contract_quote_record_id ,QuoteRevisionRecordId =self.contract_quote_revision_record_id, records_affected = join_records_affected))

        # Service based status update --> ('Z0103','Z0100')
        #INC08858696-Start-M
        #INC09067815/A055S000P01-21000 starts-M
        #Sql.RunQuery("UPDATE SAQICO SET STATUS = CASE WHEN SERVICE_ID = 'Z0103' OR (SERVICE_ID ='Z0100' AND CNSMBL_ENT = 'Included' AND (ISNULL(CONSCP,0) = 0 OR ISNULL(CONSPI,0) = 0)) THEN 'OFFLINE PRICING' ELSE 'ACQUIRED' END WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SERVICE_ID IN ('Z0103','Z0100') {records_affected}".format(QuoteRecordId= self.contract_quote_record_id ,QuoteRevisionRecordId =self.contract_quote_revision_record_id, records_affected = join_records_affected))
        #INC09067815/A055S000P01-21000 ends-M
        # INC08813185 - End - A

        #INC08858696-End-M

    def _update_items(self):
        #SAQRIT - Status - Offline Pricing
        Sql.RunQuery("UPDATE SAQRIT SET STATUS = SAQICO.STATUS FROM SAQRIT (NOLOCK) JOIN SAQICO (NOLOCK) ON SAQICO.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND SAQICO.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID AND SAQICO.SERVICE_ID = SAQRIT.SERVICE_ID AND SAQICO.QTEITM_RECORD_ID = SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID WHERE SAQRIT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id))

        Sql.RunQuery("UPDATE SAQRIT SET STATUS = 'OFFLINE PRICING' FROM SAQRIT (NOLOCK) JOIN SAQICO (NOLOCK) ON SAQICO.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND SAQICO.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID AND SAQICO.SERVICE_ID = SAQRIT.SERVICE_ID AND SAQICO.QTEITM_RECORD_ID = SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID WHERE SAQRIT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND ISNULL(SAQICO.STATUS,'') = 'OFFLINE PRICING'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id))

        Sql.RunQuery("UPDATE SAQRIT SET STATUS = 'PRR-ON HOLD PRICING' FROM SAQRIT (NOLOCK) JOIN SAQICO (NOLOCK) ON SAQICO.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND SAQICO.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID AND SAQICO.SERVICE_ID = SAQRIT.SERVICE_ID AND SAQICO.QTEITM_RECORD_ID = SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID WHERE SAQRIT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND ISNULL(SAQICO.STATUS,'') = 'PRR-ON HOLD PRICING'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id))

        Sql.RunQuery("UPDATE SAQRIT SET STATUS = 'CFG-ON HOLD TKM' FROM SAQRIT (NOLOCK) JOIN SAQICO (NOLOCK) ON SAQICO.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND SAQICO.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID AND SAQICO.SERVICE_ID = SAQRIT.SERVICE_ID AND SAQICO.QTEITM_RECORD_ID = SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID WHERE SAQRIT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND ISNULL(SAQICO.STATUS,'') = 'CFG-ON HOLD TKM'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id))

    def _user_price_approval_trigger(self,annual_item_record_id = None):
        # Approval Trigger Field Update
        if annual_item_record_id:
            records_affected = " AND SAQICO.QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{}' ".format(annual_item_record_id)
        else:
            search_condition_modified = str(self.search_condition[:-4])
            #INC09092287 - Start - M
            records_affected = " AND " + (" AND ".join(str(i) for i in search_condition_modified.split(" AND "))) if search_condition_modified!="" else ""
            ##INC09092287 - End - M
        Sql.RunQuery("""UPDATE SAQICO
                SET SAQICO.UACBDA = 'True'
                FROM SAQICO (NOLOCK)
                WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' {records_affected} AND (SAQICO.USRPRC > SAQICO.CELPRC)""".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, records_affected=records_affected))
        Sql.RunQuery("""UPDATE SAQICO
                SET SAQICO.UBSBDA = 'True'
                FROM SAQICO (NOLOCK)
                WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' {records_affected} AND (SAQICO.BDVPRC < SAQICO.SLSPRC) AND (SAQICO.USRPRC < SAQICO.SLSPRC)""".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, records_affected=records_affected))
        Sql.RunQuery("""UPDATE SAQICO
                SET SAQICO.UBSNSA = 'True'
                FROM SAQICO (NOLOCK)
                WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' {records_affected} AND (SAQICO.USRPRC < SAQICO.SLSPRC) AND (SAQICO.SLSPRC < SAQICO.BDVPRC)""".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, records_affected=records_affected))

parameters = {}
try:
    parameters['records']=str(Param.Records)
except:
    parameters['records']=""
try:
    parameters['auto_update_flag'] = str(Param.auto_update_flag)
except:
    parameters['auto_update_flag'] = "False"
#INC08841829 - Start - M
try:
    parameters['mode'] = str(Param.Mode)
except:
    parameters['mode'] = ""
try:
    parameters['search_condition'] = str(Param.search_condition)
except:
    parameters['search_condition'] = ""
#INC08841829 - End - M
try:
    parameters['quote_record_id'] = str(Param.quote_record_id)
    parameters['qterev_record_id'] = str(Param.qterev_record_id)
except:
    parameters['quote_record_id'] = Quote.GetGlobal("contract_quote_record_id")
    parameters['qterev_record_id'] = Quote.GetGlobal("quote_revision_record_id")
contract_quote_item_obj = ContractQuoteItemAnnualizedPricing(**parameters)
if parameters['mode']=="Bulk Edit Rolldown":
    contract_quote_item_obj._rolldown_from_coeff_level()
    contract_quote_item_obj._rolldown_from_total_price_level()
    contract_quote_item_obj._user_price_approval_trigger()
    contract_quote_item_obj._update_items()
    Log.Info('CQUPPRWLFD Rolldown Ends!!!-->'+str(contract_quote_item_obj.contract_quote_id))
else:
    contract_quote_item_obj._do_opertion()
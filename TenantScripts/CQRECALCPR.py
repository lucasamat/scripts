# =========================================================================================================================================
#   __script_name : CQRECALCPR.PY
#   __script_description : THIS SCRIPT IS AN IFLOW SCRIPT FOR RECALCULATING PRICING WHILE BULK UPDATE
#   __primary_author__ : VIKNESH DURAISAMY
#   __create_date :02-09-2022
# ==========================================================================================================================================
from SYDATABASE import SQL
import CQCPQC4CWB
import CQREVSTSCH
import time
import System.Net
import Webcom.Configurator.Scripting.Test.TestProduct
Sql = SQL()
productAttributesGetByName = lambda productAttribute: Product.Attributes.GetByName(productAttribute) or ""

class RecalculatePricing:
    def __init__(self):
        try:
            self.contract_quote_record_id = QUOTE_RECORD_ID
        except:
            self.contract_quote_record_id = ''	
        try:
            self.quote_revision_record_id = QTEREV_RECORD_ID
        except:
            self.quote_revision_record_id = ''
        self.unique_serviceids = []
    def process_values(self,attr_values,line_values):
        if line_values.SERVICE_ID not in self.unique_serviceids:
            self.unique_serviceids.append(line_values.SERVICE_ID)
        unique_keys = attr_values.keys()
        for key in unique_keys:
            triggered_flag = False
            if key in ('ATGKEC','ATGKEP') and (line_values.ATGKEY != 'Excluded' and line_values.ATGKEY != 'Exception' and str(line_values.ATGKEY) != ''):
                triggered_flag = True
            elif key in ('ATKNCI','ATKNPI') and (line_values.TGKPNS != 'Excluded' and str(line_values.TGKPNS) != ''):
                triggered_flag = True
            elif key in ('CONSCP','CONSPI') and (((line_values.CNSMBL_ENT in ('Some Exclusions','Some Inclusions') and line_values.SERVICE_ID != 'Z0100') or (line_values.CNSMBL_ENT in ('Included','Some Inclusions') and line_values.SERVICE_ID == 'Z0100') ) and not (line_values.CNSMBL_ENT == 'Some Inclusions' and line_values.SERVICE_ID == 'Z0092')):#A055S000P01-20741 - M
                triggered_flag = True
            elif key in ('NONCCI','NONCPI') and (line_values.NCNSMB_ENT in ('Some Inclusions','Some Exclusions') and line_values.SERVICE_ID != 'Z0100'):
                triggered_flag = True
            elif key in ('NWPTOC','NWPTOP') and (line_values.NWPTON == 'Yes'):
                triggered_flag = True
            elif key in ('AIUICI','AIUIPI') and ((line_values.AIUICC == "0" or line_values.AIUICC == False) or (line_values.AIUICI > 0 or line_values.AIUIPI > 0)):
                triggered_flag = True
            elif key in ('AMNCCI','AMNPPI') and ((line_values.AMNCPE == "1" or line_values.AMNCPE == True) or line_values.STATUS == 'PRR-ON HOLD PRICING' or (line_values.AMNCCI > 0 or line_values.AMNPPI > 0)):
                triggered_flag = True
            if not triggered_flag:
                attr_values.pop(key)
        return attr_values
    def split_process(self):
        start_time = time.time()
        Sql.RunQuery("UPDATE SAQTRV SET REVISION_STATUS = 'PRR-RECALCULATING'  WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' ".format(self.contract_quote_record_id,self.quote_revision_record_id))
        self.writeback()
        get_query = Sql.GetFirst("SELECT TOP 1 * FROM SAQIBE (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' ORDER BY BULK_EDIT_FILTERQUERY_ID DESC ".format(self.contract_quote_record_id,self.quote_revision_record_id))
        #A055S000P01-20746 - Start - M        
        values = {
                        'ATGKEC': str(get_query.ANNITMS_ADDTNL_TGT_KPI_CI),
                        'ATGKEP': str(get_query.ANNITMS_ADDTNL_TGT_KPI_PI),
                        'ATKNCI': str(get_query.ANNITMS_ADDTNL_TGT_KPI_NS_CI),
                        'ATKNPI': str(get_query.ANNITMS_ADDTNL_TGT_KPI_NS_PI),
                        'CONSCP': str(get_query.ANNITMS_CONSUMABLE_CI),
                        'CONSPI': str(get_query.ANNITMS_CONSUMABLE_PI),
                        'NONCCI': str(get_query.ANNITMS_NONCONSUMABLE_CI),
                        'NONCPI': str(get_query.ANNITMS_NONCONSUMABLE_PI),
                        'NWPTOC': str(get_query.ANNITMS_NEW_PARTS_ONLY_CI),
                        'NWPTOP': str(get_query.ANNITMS_NEW_PARTS_ONLY_PI),
                        'AIUICI': str(get_query.ANNITMS_UPTIME_IMPROVEMENT_CI),
                        'AIUIPI': str(get_query.ANNITMS_UPTIME_IMPROVEMENT_PI),
                        'AMNCCI': str(get_query.ANNITMS_ADDTNL_MANUAL_CI),
                        'AMNPPI': str(get_query.ANNITMS_ADDTNL_MANUAL_PI),
                    }
        values = {key:val for key,val in values.items() if val!='' and val is not None}
        
        get_count = Sql.GetFirst("SELECT COUNT(CpqTableEntryId) as CNT FROM SAQICO (NOLOCK) WHERE {} {} QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID NOT IN ('Z0117','Z0116','Z0101','Z0046','Z0048','Z0123') ".format(get_query.BULK_EDIT_FILTERQUERY_VALUE," STATUS IN ('CFG-ON HOLD TKM','OFFLINE PRICING','PRR-ON HOLD PRICING','ACQUIRED') AND " if "STATUS" not in get_query.BULK_EDIT_FILTERQUERY_VALUE else "",self.contract_quote_record_id,self.quote_revision_record_id))
        #A055S000P01-20746 - End - M
        matched_records = get_count.CNT
        limit = 1000
        if matched_records>limit:
            select_group_count = matched_records/limit
            remaining_group = matched_records%limit
            start_count = 0
            for iter in range(select_group_count):
                Log.Info("Fetching from "+str(start_count)+" Rows")
                self.calculate(get_query,values,start_count)
                start_count+=limit
            if remaining_group > 0:
                self.calculate(get_query,values,start_count)
        else:
            self.calculate(get_query,values,0)
        Log.Info("Update for CAT4's complete on "+str(get_query.QUOTE_ID))
        calling_waterfall = ScriptExecutor.ExecuteGlobal("CQUPPRWLFD",{"SQL_OBJ":Sql,"quote_record_id":self.contract_quote_record_id,"qterev_record_id":self.quote_revision_record_id,"Mode":"Bulk Edit Rolldown","search_condition":get_query.BULK_EDIT_FILTERQUERY_VALUE})
        Log.Info("===> CQIFWUDQTM called from CQRECALCPR for "+str(get_query.QUOTE_ID)+","+str(list(set(self.unique_serviceids))))
        CallingCQIFWUDQTM = ScriptExecutor.ExecuteGlobal("CQIFWUDQTM",{"QT_REC_ID":get_query.QUOTE_ID,"manual_pricing":"True",'service_ids':list(set(self.unique_serviceids))})
        items_status = []
        reviewed_flag = True
        items_obj = Sql.GetList("SELECT ISNULL(STATUS,'') as STATUS FROM SAQRIT (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' and QTEREV_RECORD_ID = '{QuoteRevisionRecordId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.quote_revision_record_id))
        if items_obj:
            items_status = [item_obj.STATUS for item_obj in items_obj]
        for sts in items_status:
            if sts not in ('ACQUIRED','CFG-ON HOLD TKM'):
                reviewed_flag = False
        if reviewed_flag:
            Sql.RunQuery("UPDATE SAQTRV SET REVISION_STATUS = 'PRR-PRICING REVIEWED',WORKFLOW_STATUS = 'PRICING REVIEW' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' and QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' and REVISION_STATUS !='PRI-PRICING' ".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.quote_revision_record_id))
        elif 'PRR-ON HOLD PRICING' in items_status or 'OFFLINE PRICING' in items_status:
            Sql.RunQuery("UPDATE SAQTRV SET WORKFLOW_STATUS = 'PRICING REVIEW',REVISION_STATUS='PRR-ON HOLD PRICING' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' and QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' ".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.quote_revision_record_id))
        elif 'CFG-ON HOLD - COSTING' in items_status:
            Sql.RunQuery("UPDATE SAQTRV SET WORKFLOW_STATUS = 'CONFIGURE',REVISION_STATUS='CFG-ON HOLD - COSTING' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' and QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' ".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.quote_revision_record_id))
        self.writeback()
        end_time = time.time()
        Log.Info('Recalculation done for QUOTE_ID:'+str(get_query.QUOTE_ID)+', Lines updated: '+str(matched_records)+', Total Time Taken-->'+str(round(end_time-start_time,2))+'seconds & Time taken per line in seconds-->'+str(round((end_time-start_time)/matched_records,2)))	

    def calculate(self,get_query,values,start):
        get_records = Sql.GetList("SELECT QUOTE_ITEM_COVERED_OBJECT_RECORD_ID,ATGKEY,NWPTON,CNSMBL_ENT,SERVICE_ID,NCNSMB_ENT,TGKPNS,AMNCPE,STATUS,AMNCCI,AMNPPI,AIUICC,AIUICI,AIUIPI FROM SAQICO (NOLOCK) WHERE {} {} QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' ORDER BY LINE ASC OFFSET {} ROWS FETCH NEXT 1000 ROWS ONLY ".format(get_query.BULK_EDIT_FILTERQUERY_VALUE," STATUS IN ('CFG-ON HOLD TKM','OFFLINE PRICING','PRR-ON HOLD PRICING','ACQUIRED') AND " if "STATUS" not in get_query.BULK_EDIT_FILTERQUERY_VALUE else "",self.contract_quote_record_id,self.quote_revision_record_id,start))
        
        quote_items_list = []
        for line in get_records:
            line_dict = {}
            temp_values = values.copy()
            line_dict[str(line.QUOTE_ITEM_COVERED_OBJECT_RECORD_ID)] = self.process_values(temp_values,line)
            quote_items_list.append(line_dict)
        dict_length = len(quote_items_list)
        batch = 100
        if dict_length>batch:
            loop_count = dict_length/batch
            remaining = dict_length%batch
            count = 0
            for record in range(loop_count):
                trimmed_list = quote_items_list[count:count+batch]
                calling_waterfall = ScriptExecutor.ExecuteGlobal("CQUPPRWLFD",{"Records":str(trimmed_list),"SQL_OBJ":Sql,"quote_record_id":self.contract_quote_record_id,"qterev_record_id":self.quote_revision_record_id,"Mode":"Bulk Edit","search_condition":str(get_query.BULK_EDIT_FILTERQUERY_VALUE)})
                count+=batch
            if remaining > 0:
                trimmed_list = quote_items_list[count:count+remaining]
                calling_waterfall = ScriptExecutor.ExecuteGlobal("CQUPPRWLFD",{"Records":str(trimmed_list),"SQL_OBJ":Sql,"quote_record_id":self.contract_quote_record_id,"qterev_record_id":self.quote_revision_record_id,"Mode":"Bulk Edit","search_condition":str(get_query.BULK_EDIT_FILTERQUERY_VALUE)})
        else:
            calling_waterfall = ScriptExecutor.ExecuteGlobal("CQUPPRWLFD",{"Records":str(quote_items_list),"SQL_OBJ":Sql,"quote_record_id":self.contract_quote_record_id,"qterev_record_id":self.quote_revision_record_id,"Mode":"Bulk Edit","search_condition":str(get_query.BULK_EDIT_FILTERQUERY_VALUE)})	
    
    def writeback(self):
        CQCPQC4CWB.writeback_to_c4c("quote_header",self.contract_quote_record_id,self.quote_revision_record_id)
        CQCPQC4CWB.writeback_to_c4c("opportunity_header",self.contract_quote_record_id,self.quote_revision_record_id)
        CQREVSTSCH.Revisionstatusdatecapture(self.contract_quote_record_id,self.quote_revision_record_id)
if 'Param' in globals():
    if hasattr(Param, 'CPQ_Columns'):
        QUOTE_RECORD_ID = str(Param.CPQ_Columns['QUOTE_RECORD_ID'])
        QTEREV_RECORD_ID = str(Param.CPQ_Columns['QTEREV_RECORD_ID'])
recalc = RecalculatePricing()
recalc.split_process()

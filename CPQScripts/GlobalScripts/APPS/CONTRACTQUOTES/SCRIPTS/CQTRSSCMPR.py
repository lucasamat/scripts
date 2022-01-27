# ====================================================================================================
#   __script_name : CQTRSSCMPR.PY
#   __script_description : This script is used to do the trigger the sscm pricing call by clicking on the complete stage button when all the product offerings are complete.
#   __primary_author__ : GAYATHRI AMARESAN
#   __create_date : 06/12/2021
#   © BOSTON HARBOR CONSULTING INC - ALL RIGHTS RESERVED
# ====================================================================================================

from SYDATABASE import SQL
Sql = SQL()
import re

class pricing_call:
    def sscm_pricing_call(self):
        service_entitlement_object_sscm_pricing_call  = ""
        greenbook_entitlement_object_sscm_pricing_call = ""
        source_object_name = ""
        contract_quote_revision_object = Sql.GetFirst("select QUOTE_RECORD_ID,QTEREV_RECORD_ID,QUOTE_ID,QTEREV_ID FROM SAQTRV(NOLOCK) WHERE QUOTE_RECORD_ID = '{}' and QTEREV_RECORD_ID = '{}' AND ACTIVE = 1 ".format(Quote.GetGlobal("contract_quote_record_id"),Quote.GetGlobal("quote_revision_record_id")))
        if contract_quote_revision_object:
            self.contract_quote_id = contract_quote_revision_object.QUOTE_ID
            self.contract_quote_revision_id = contract_quote_revision_object.QTEREV_ID
            self.contract_quote_record_id = contract_quote_revision_object.QUOTE_RECORD_ID
            self.contract_quote_revision_record_id = contract_quote_revision_object.QTEREV_RECORD_ID

        service_object = Sql.GetList("select SERVICE_ID from SAQTSV(NOLOCK) where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' ".format(self.contract_quote_record_id,self.contract_quote_revision_record_id))
        for service in service_object:
            service_id = service.SERVICE_ID
            material_object = Sql.GetFirst("select MATERIALCONFIG_TYPE from MAMTRL(NOLOCK) WHERE SAP_PART_NUMBER = '{}'".format(service_id))
            if material_object and material_object.MATERIALCONFIG_TYPE != "SIMPLE MATERIAL":
                where_str = " QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' and SERVICE_ID = '{ServiceId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id,ServiceId=service_id)
                service_entitlement_obj = Sql.GetFirst("""SELECT SERVICE_ID, ENTITLEMENT_XML FROM  {obj_name} (NOLOCK) WHERE {where_str}""".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id,ServiceId=service_id, obj_name = "SAQTSE", where_str = where_str))
                if service_entitlement_obj:
                    quote_item_tag_pattern = re.compile(r'(<QUOTE_ITEM_ENTITLEMENT>[\w\W]*?</QUOTE_ITEM_ENTITLEMENT>)')
                    entitlement_id_tag_pattern = re.compile(r'<ENTITLEMENT_ID>AGS_'+str(service_id)+'_PQB_QTITST</ENTITLEMENT_ID>')
                    ##getting billing type
                    billing_type_pattern = re.compile(r'<ENTITLEMENT_ID>AGS_'+str(service_id)+'_PQB_BILTYP</ENTITLEMENT_ID>')
                    entitlement_display_value_tag_pattern = re.compile(r'<ENTITLEMENT_DISPLAY_VALUE>([^>]*?)</ENTITLEMENT_DISPLAY_VALUE>')
                    for quote_item_tag in re.finditer(quote_item_tag_pattern, service_entitlement_obj.ENTITLEMENT_XML):
                        quote_item_tag_content = quote_item_tag.group(1)
                        entitlement_id_tag_match = re.findall(entitlement_id_tag_pattern,quote_item_tag_content)	
                        entitlement_billing_id_tag_match = re.findall(billing_type_pattern,quote_item_tag_content)
                        if entitlement_id_tag_match:
                            entitlement_display_value_tag_match = re.findall(entitlement_display_value_tag_pattern,quote_item_tag_content)
                            if entitlement_display_value_tag_match:
                                quote_service_entitlement_type = entitlement_display_value_tag_match[0].upper()
                                if quote_service_entitlement_type == 'OFFERING + EQUIPMENT':
                                    source_object_name = 'SAQSCE'
                                elif quote_service_entitlement_type in ('OFFERING + FAB + GREENBOOK + GROUP OF EQUIPMENT', 'OFFERING + GREENBOOK + GR EQUI', 'OFFERING + CHILD GROUP OF PART'):
                                    source_object_name = 'SAQSGE'
                            #Trace.Write("source_object_name"+str(source_object_name))
                    if source_object_name == "SAQSCE":
                        service_entitlement_object = Sql.GetList("select CONFIGURATION_STATUS from SAQSCE(NOLOCK) where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' ".format(self.contract_quote_record_id,self.contract_quote_revision_record_id))
                        for status in service_entitlement_object:
                            service_configuration_status = status.CONFIGURATION_STATUS
                            if service_configuration_status != "COMPLETE":
                                service_entitlement_object_sscm_pricing_call = "NO"
                                #Trace.Write("service_entitlement_object_sscm_pricing_call  "+str(service_entitlement_object_sscm_pricing_call))
                                break
                                
                    if source_object_name == "SAQSGE":
                        greenbook_entitlement_object = Sql.GetList("select CONFIGURATION_STATUS from SAQSGE(NOLOCK) where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' ".format(self.contract_quote_record_id,self.contract_quote_revision_record_id))
                        for greenbook_status in greenbook_entitlement_object:
                            greenbook_configuration_status = greenbook_status.CONFIGURATION_STATUS
                            if greenbook_configuration_status != "COMPLETE":
                                greenbook_entitlement_object_sscm_pricing_call = "NO"
                                #Trace.Write("greenbook_entitlement_object_sscm_pricing_call  "+str(greenbook_entitlement_object_sscm_pricing_call))
                                break
                    if (service_entitlement_object_sscm_pricing_call != "NO")or (greenbook_entitlement_object_sscm_pricing_call != "NO"):
                        #ScriptExecutor.ExecuteGlobal('QTPOSTACRM',{'QUOTE_ID':self.contract_quote_id,'REVISION_ID':self.contract_quote_revision_id, 'Fun_type':'cpq_to_sscm'})
                        Trace.Write("commented the pricing call")
        return True


sscm_pricing = pricing_call()
ApiResponse = ApiResponseFactory.JsonResponse(sscm_pricing.sscm_pricing_call())                
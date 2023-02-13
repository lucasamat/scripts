# =========================================================================================================================================
#   __script_name : CQINSQTITM.PY(PRD)
#   __script_description : THIS SCRIPT IS USED TO INSERT QUOTE ITEMS AND ITS RELATED TABLES BASED ENTITLEMENT
#   __primary_author__ : AYYAPPAN SUBRAMANIYAN
#   __create_date :30-09-2021
# ==========================================================================================================================================
import re
import datetime
import CQPARTIFLW
import time
from SYDATABASE import SQL
Sql = SQL()
class ContractQuoteItem:
    def __init__(self, **kwargs):
        self.user_id = str(User.Id)
        self.user_name = str(User.UserName)
        self.datetime_value = datetime.datetime.now()
        self.contract_quote_record_id = kwargs.get('contract_quote_record_id')
        self.contract_quote_revision_record_id = kwargs.get('contract_quote_revision_record_id')
        self.action_type = kwargs.get('action_type')
        self.service_id = kwargs.get('service_id')
        self.split_parent_service_id = kwargs.get('parent_service_id') ##809 HPQC DEFECT cpde starts.. ends..
        self.greenbook_id = kwargs.get('greenbook_id')
        self.fablocation_id = kwargs.get('fablocation_id')
        self.equipment_id = kwargs.get('equipment_id') 
        self.entitlement_level_obj = kwargs.get('entitlement_level_obj')
        self.pricing_temp_table = ''
        self.quote_line_item_temp_table = '' 
        self.quote_service_entitlement_type = ''
        self.get_billing_type_val = ""
        self.parent_service_id = ""
        self.source_object_name = ''
        self.where_condition_string = kwargs.get('where_condition_string')
        self.triggered_from = kwargs.get('triggered_from')
        self.set_contract_quote_related_details()
        self._set_service_type()
        self._set_fpm_service_type()
        self._get_material_type()
        self._get_ancillary_product()
        self._get_billing_type()
        self.generate_contract_based_years()#CR704 - A
    #A055S000P01-21072 Start M
    def update_cntday(self):
        Log.Info("LN 50 UPDATE CNTDAY")
        Sql.RunQuery("UPDATE SAQICO SET CNTDAY = IIF((DATEDIFF(day, CONTRACT_VALID_FROM, CONTRACT_VALID_TO) + 1)>365, 365, DATEDIFF(day, CONTRACT_VALID_FROM, CONTRACT_VALID_TO) + 1) FROM SAQICO WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id))
    #A055S000P01-21072 End M
    #CR704 - Start - A
    def generate_contract_based_years(self):
        quote_revision_obj = Sql.GetFirst("SELECT CONTRACT_VALID_FROM,CONTRACT_VALID_TO,QUOTE_ID,QTEREV_ID FROM SAQTRV (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(self.contract_quote_record_id,self.contract_quote_revision_record_id))
        check_contract_obj = Sql.GetFirst("SELECT COUNT(*) as CNT FROM SAQCYR (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(self.contract_quote_record_id,self.contract_quote_revision_record_id))
        if quote_revision_obj and check_contract_obj.CNT == 0:
            contract_header_start_date = quote_revision_obj.CONTRACT_VALID_FROM
            contract_header_start_datetime = datetime.datetime.strptime(str(quote_revision_obj.CONTRACT_VALID_FROM).split(' ')[0], '%m/%d/%Y')
            contract_header_end_datetime = datetime.datetime.strptime(str(quote_revision_obj.CONTRACT_VALID_TO).split(' ')[0], '%m/%d/%Y')
            contract_header_end_date = contract_header_end_datetime
            contract_datediff = contract_header_end_datetime - contract_header_start_datetime
            avgyear = 365.2425       # pedants definition of a year length with leap years
            avgmonth = 365.2425/12.0  # even leap years have 12 months
            years, remainder = divmod(contract_datediff.days, avgyear)
            years, months = int(years), (remainder / avgmonth) #INC08814916 - M
            if months > 0:
                years += 1 
            yearwise_dates_dict = {}
            for year in range(1, years+1):
                # Find yearwise start and end date till contract end - start
                date_obj = Sql.GetFirst("""SELECT DATEADD(day,-1,DATEADD(year, {YearIncrement}, '{DateString}')) AS EndDate, DATEADD(year, {YearIncrement}, '{DateString}') AS StartDate""".format(DateString=contract_header_start_date, YearIncrement=year))
                yearwise_start_date = datetime.datetime.strptime(str(date_obj.StartDate).split(' ')[0], '%m/%d/%Y')
                yearwise_end_date = datetime.datetime.strptime(str(date_obj.EndDate).split(' ')[0], '%m/%d/%Y')
                if year == 1:
                    yearwise_dates_dict[year] = {'YEAR':'YEAR '+str(year),'start_date':contract_header_start_datetime.date()}
                year_end_date = yearwise_end_date.date()
                if contract_header_end_date.date() < year_end_date:
                    year_end_date = contract_header_end_date.date()
                    yearwise_dates_dict[year].update({'end_date':contract_header_end_datetime.date()})
                else:
                    yearwise_dates_dict[year].update({'end_date':yearwise_end_date})
                if year+1 <= years:
                    yearwise_dates_dict[year+1] = {'YEAR':'YEAR '+str(year+1),'start_date':yearwise_start_date}
                # Find yearwise start and end date till contract end - end
            datas = []
            modified_date = str(datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            columns = 'CONTRACT_END_DATE,CONTRACT_START_DATE,CNTYER,QUOTE_RECORD_ID,QUOTE_ID,QTEREV_RECORD_ID,QTEREV_ID,CpqTableEntryModifiedBy,CpqTableEntryDateModified'
            for val in yearwise_dates_dict.Values:
                datas.append([str(val['end_date']),str(val['start_date']),val['YEAR'],self.contract_quote_record_id,quote_revision_obj.QUOTE_ID,self.contract_quote_revision_record_id,quote_revision_obj.QTEREV_ID,self.user_id,modified_date])
            dates_temp = (", ".join(map(str,[str(tuple(data)) for data in datas],)).replace("None", "null").replace("'", "''"))
            insert = SqlHelper.GetFirst("sp_executesql @T=N'INSERT INTO SAQCYR ("+str(columns)+") SELECT DISTINCT "+str(columns)+" FROM (VALUES "+str(dates_temp)+") AS TEMP("+str(columns)+") ' ")
    #CR704 - End - A
    def set_contract_quote_related_details(self):
        contract_quote_obj = Sql.GetFirst("SELECT QUOTE_ID, QUOTE_TYPE, SALE_TYPE, C4C_QUOTE_ID, QTEREV_ID, QUOTE_CURRENCY, QUOTE_CURRENCY_RECORD_ID FROM SAQTMT (NOLOCK) WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{QuoteRecordId}'".format(QuoteRecordId=self.contract_quote_record_id))
        get_contract_revision_obj = Sql.GetFirst("SELECT * FROM SAQTRV (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QUOTE_REVISION_RECORD_ID = '{QuoteRevisionRecordId}'".format(QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id))
        if contract_quote_obj:
            self.contract_quote_id = contract_quote_obj.QUOTE_ID
            self.quote_type = contract_quote_obj.QUOTE_TYPE
            self.sale_type = contract_quote_obj.SALE_TYPE
            self.c4c_quote_id = contract_quote_obj.C4C_QUOTE_ID
            self.contract_quote_revision_id = contract_quote_obj.QTEREV_ID
            self.contract_currency = contract_quote_obj.QUOTE_CURRENCY
            self.contract_currency_record_id = contract_quote_obj.QUOTE_CURRENCY_RECORD_ID
        else:
            self.contract_quote_id = ''  
            self.quote_type = ''
            self.sale_type = ''
            self.c4c_quote_id = ''
            self.contract_quote_revision_id = ''
        if get_contract_revision_obj:
            self.exchange_rate = get_contract_revision_obj.EXCHANGE_RATE
        else:
            self.exchange_rate = ''
        return True
    
    def _set_service_type(self):
        spare_parts_count_object = Sql.GetFirst("SELECT CpqTableEntryId FROM SAQRSP (NOLOCK) WHERE QUOTE_RECORD_ID ='{QuoteRecordId}' AND QTEREV_RECORD_ID='{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id))
        if spare_parts_count_object:
            self.is_spare_service = True
        else:
            self.is_spare_service = False
        return True
    def _set_fpm_service_type(self):
        fpm_spare_parts_count_object = Sql.GetFirst("SELECT CpqTableEntryId FROM SAQSPT (NOLOCK) WHERE QUOTE_RECORD_ID ='{QuoteRecordId}' AND QTEREV_RECORD_ID='{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id))
        if fpm_spare_parts_count_object:
            self.is_fpm_spare_service = True
        else:
            self.is_fpm_spare_service = False
        return True
    def _get_billing_type(self):
        self.get_billing_type_val =''
        get_billing_cycle = Sql.GetFirst("select ENTITLEMENT_XML,SERVICE_ID from SAQTSE where QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' and SERVICE_ID = '{get_service}'".format(QuoteRecordId =self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id,get_service = self.service_id))
        if get_billing_cycle:
            updateentXML = get_billing_cycle.ENTITLEMENT_XML
            pattern_tag = re.compile(r'(<QUOTE_ITEM_ENTITLEMENT>[\w\W]*?</QUOTE_ITEM_ENTITLEMENT>)')
            pattern_id = re.compile(r'<ENTITLEMENT_ID>(AGS_'+str(get_billing_cycle.SERVICE_ID)+'_PQB_BILTYP)</ENTITLEMENT_ID>')
            pattern_name = re.compile(r'<ENTITLEMENT_DISPLAY_VALUE>([^>]*?)</ENTITLEMENT_DISPLAY_VALUE>')
            for m in re.finditer(pattern_tag, updateentXML):
                sub_string = m.group(1)
                get_ent_id = re.findall(pattern_id,sub_string)
                get_ent_val= re.findall(pattern_name,sub_string)
                if get_ent_id:
                    self.get_billing_type_val = str(get_ent_val[0])
                    break
        return True
    def _get_material_type(self):
        get_service_config_type = Sql.GetFirst("SELECT * FROM MAMTRL (NOLOCK) WHERE SAP_PART_NUMBER = '{}' AND MATERIALCONFIG_TYPE = 'SIMPLE MATERIAL'".format(self.service_id))
        if get_service_config_type:
            self.is_simple_service = True
        else:
            self.is_simple_service = False
        return True
    def _get_ancillary_product(self):
        self.is_ancillary = False
        self.parent_service_id = ''
        self.addon_product = False
        ##ancillary product
        check_ancillary = Sql.GetFirst("SELECT PAR_SERVICE_ID FROM SAQTSV (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' and SERVICE_ID = '{ServiceId}' AND SERVICE_ID NOT IN (SELECT ADNPRD_ID FROM SAQSAO WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' )".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id))
        if check_ancillary:
            if check_ancillary.PAR_SERVICE_ID:
                self.is_ancillary = True
                self.parent_service_id = check_ancillary.PAR_SERVICE_ID
        else:
            self.is_ancillary = False
        #addon product
        check_addon = Sql.GetFirst("SELECT SERVICE_ID FROM SAQSAO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id) )
        if check_addon:
            if check_addon.SERVICE_ID :
                self.addon_product = True
                self.parent_service_id = check_addon.SERVICE_ID
        return True
    def _quote_items_assembly_insert(self, update=True):
        import re
        quotetype_value_for_offering =''
        service_entitlement_object =Sql.GetFirst("""select ENTITLEMENT_XML from SAQTSE (nolock) where QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' and SERVICE_ID = '{service_id}' """.format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id,service_id = self.service_id))
        if service_entitlement_object is not None:
            pattern_tag = re.compile(r'(<QUOTE_ITEM_ENTITLEMENT>[\w\W]*?</QUOTE_ITEM_ENTITLEMENT>)')
            quote_type_attribute = re.compile(r'<ENTITLEMENT_ID>AGS_[^>]*?_PQB_QTETYP</ENTITLEMENT_ID>')
            quote_type_attribute_value = re.compile(r'<ENTITLEMENT_DISPLAY_VALUE>([^>]*?)</ENTITLEMENT_DISPLAY_VALUE>')
            XML = service_entitlement_object.ENTITLEMENT_XML
            for values in re.finditer(pattern_tag, XML):
                sub_string = values.group(1)
                quotetype_id =re.findall(quote_type_attribute,sub_string)
                if quotetype_id:
                    quotetype_value =re.findall(quote_type_attribute_value,sub_string)
                    quotetype_value_for_offering = str(quotetype_value[0]).upper()
        datetime_string = self.datetime_value.strftime("%d%m%Y%H%M%S")
        if str(quotetype_value_for_offering) == "TOOL BASED":
            # SAQSCE_BKP = "SAQSCE_BKP_{}_{}".format(self.contract_quote_id, datetime_string)
            SAQSCA_BKP = "SAQSCA_BKP_{}_{}".format(self.contract_quote_id, datetime_string)
            SAQICO_BKP = "SAQICO_BKP_{}_{}".format(self.contract_quote_id, datetime_string)
            # SAQSCE_BKP_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQSCE_BKP)+"'' ) BEGIN DROP TABLE "+str(SAQSCE_BKP)+" END  ' ")
            SAQSCA_BKP_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQSCA_BKP)+"'' ) BEGIN DROP TABLE "+str(SAQSCA_BKP)+" END  ' ")
            SAQICO_BKP_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQICO_BKP)+"'' ) BEGIN DROP TABLE "+str(SAQICO_BKP)+" END  ' ")
            try:
                SAQSCA_BKP_INS = SqlHelper.GetFirst(
                    "sp_executesql @T=N'SELECT SAQSCA.* INTO "+str(SAQSCA_BKP)+" FROM SAQSCA (NOLOCK) WHERE SAQSCA.QUOTE_ID = ''"+str(self.contract_quote_id)+"'' AND SAQSCA.QTEREV_ID = ''"+str(self.contract_quote_revision_id)+"'' AND SAQSCA.SERVICE_ID = ''"+str(self.service_id)+"'' '")
                SAQICO_BKP_INS = SqlHelper.GetFirst(
                    "sp_executesql @T=N'SELECT SAQICO.* INTO "+str(SAQICO_BKP)+" FROM SAQICO (NOLOCK) WHERE SAQICO.QUOTE_ID = ''"+str(self.contract_quote_id)+"'' AND SAQICO.QTEREV_ID = ''"+str(self.contract_quote_revision_id)+"'' AND SAQICO.SERVICE_ID = ''"+str(self.service_id)+"'' '")
                Sql.RunQuery("""INSERT SAQICA (EQUIPMENT_ID,EQUIPMENT_RECORD_ID,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,GREENBOOK,GREENBOOK_RECORD_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,ASSEMBLY_DESCRIPTION,ASSEMBLY_ID,ASSEMBLY_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,EQUIPMENTTYPE_ID,QTEITMCOB_RECORD_ID,CNTYEAR,LINE,QTEITM_RECORD_ID,QUOTE_ITEM_COVERED_OBJECT_ASSEMBLY_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified) 
                    SELECT OQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_COVERED_OBJECT_ASSEMBLY_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED,{UserId} as CpqTableEntryModifiedBy,GETDATE() as CpqTableEntryDateModified 
                    FROM ( 
                        SELECT IQ.* FROM (
                                SELECT 
                                    DISTINCT SAQSCA.EQUIPMENT_ID,SAQSCA.EQUIPMENT_RECORD_ID,SAQSCA.QUOTE_ID,SAQSCA.QUOTE_RECORD_ID,SAQSCA.QTEREV_ID,SAQSCA.QTEREV_RECORD_ID,SAQSCA.SERVICE_DESCRIPTION,SAQSCA.SERVICE_ID,SAQSCA.SERVICE_RECORD_ID,SAQSCA.GREENBOOK,SAQSCA.GREENBOOK_RECORD_ID,SAQSCA.FABLOCATION_ID,SAQSCA.FABLOCATION_NAME,SAQSCA.FABLOCATION_RECORD_ID,SAQSCA.ASSEMBLY_DESCRIPTION,SAQSCA.ASSEMBLY_ID,SAQSCA.ASSEMBLY_RECORD_ID,SAQSCA.SALESORG_ID,SAQSCA.SALESORG_NAME,SAQSCA.SALESORG_RECORD_ID,SAQSCA.EQUIPMENTTYPE_ID ,SAQICO.QUOTE_ITEM_COVERED_OBJECT_RECORD_ID,SAQICO.CNTYER,SAQICO.LINE,SAQICO.QTEITM_RECORD_ID FROM
                                {TempSAQSCA} (NOLOCK) SAQSCA  JOIN {item_level_covered_object} SAQICO ON 
                                SAQICO.QUOTE_RECORD_ID = SAQSCA.QUOTE_RECORD_ID AND SAQICO.QTEREV_RECORD_ID = 
                                SAQSCA.QTEREV_RECORD_ID AND SAQICO.SERVICE_RECORD_ID = SAQSCA.SERVICE_RECORD_ID AND SAQICO.EQUIPMENT_ID = SAQSCA.EQUIPMENT_ID
                                WHERE SAQSCA.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCA.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQSCA.SERVICE_ID = '{ServiceId}'
                        ) IQ    
                        LEFT JOIN SAQICA (NOLOCK) ON SAQICA.QUOTE_ID = IQ.QUOTE_ID AND SAQICA.QTEREV_ID = IQ.QTEREV_ID AND SAQICA.LINE = IQ.LINE AND SAQICA.CNTYEAR = IQ.CNTYER AND SAQICA.EQUIPMENT_ID = IQ.EQUIPMENT_ID AND SAQICA.ASSEMBLY_ID = IQ.ASSEMBLY_ID WHERE SAQICA.ASSEMBLY_RECORD_ID IS NULL
                    )OQ""".format(UserId=self.user_id, UserName=self.user_name, QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id, TempSAQSCA=SAQSCA_BKP,item_level_covered_object = SAQICO_BKP))
                SAQSCA_BKP_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQSCA_BKP)+"'' ) BEGIN DROP TABLE "+str(SAQSCA_BKP)+" END  ' ")
                SAQICO_BKP_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQICO_BKP)+"'' ) BEGIN DROP TABLE "+str(SAQICO_BKP)+" END  ' ")
            except Exception:
                SAQSCA_BKP_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQSCA_BKP)+"'' ) BEGIN DROP TABLE "+str(SAQSCA_BKP)+" END  ' ")
                SAQICO_BKP_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQICO_BKP)+"'' ) BEGIN DROP TABLE "+str(SAQICO_BKP)+" END  ' ")
                Log.Info("Occured Exception In Quote Item Assembly Insert For The Quote: {} And Revision: {}".format(self.contract_quote_id, self.contract_quote_revision_id))
        else:
            ##HPQC DEFECT 601 code starts...
            SAQGPA_BKP = "SAQGPA_BKP_{}_{}".format(self.contract_quote_id, datetime_string)     
            SAQICO_BKP = "SAQICO_BKP_{}_{}".format(self.contract_quote_id, datetime_string)
            try:
                SAQGPA_BKP_INS = SqlHelper.GetFirst(
                    "sp_executesql @T=N'SELECT SAQGPA.* INTO "+str(SAQGPA_BKP)+" FROM SAQGPA (NOLOCK) WHERE SAQGPA.QUOTE_ID = ''"+str(self.contract_quote_id)+"'' AND SAQGPA.QTEREV_ID = ''"+str(self.contract_quote_revision_id)+"'' AND SAQGPA.SERVICE_ID = ''"+str(self.service_id)+"'' '")
                SAQICO_BKP_INS = SqlHelper.GetFirst(
                                "sp_executesql @T=N'SELECT SAQICO.* INTO "+str(SAQICO_BKP)+" FROM SAQICO (NOLOCK) WHERE SAQICO.QUOTE_ID = ''"+str(self.contract_quote_id)+"'' AND SAQICO.QTEREV_ID = ''"+str(self.contract_quote_revision_id)+"'' AND SAQICO.SERVICE_ID = ''"+str(self.service_id)+"'' '")
                Sql.RunQuery("""INSERT SAQICA (EQUIPMENT_ID,EQUIPMENT_RECORD_ID,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,GREENBOOK,GREENBOOK_RECORD_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,ASSEMBLY_DESCRIPTION,ASSEMBLY_ID,ASSEMBLY_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,EQUIPMENTTYPE_ID,QTEITMCOB_RECORD_ID,CNTYEAR,LINE,QTEITM_RECORD_ID,QUOTE_ITEM_COVERED_OBJECT_ASSEMBLY_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified) 
                        SELECT OQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_COVERED_OBJECT_ASSEMBLY_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED,{UserId} as CpqTableEntryModifiedBy,GETDATE() as CpqTableEntryDateModified 
                        FROM ( 
                            SELECT IQ.* FROM (
                                SELECT SQ.*,SAQRIO.QTEITM_RECORD_ID
                                FROM (
                                    SELECT 
                                        DISTINCT SAQGPA.EQUIPMENT_ID,SAQGPA.EQUIPMENT_RECORD_ID,SAQGPA.QUOTE_ID,SAQGPA.QUOTE_RECORD_ID,SAQGPA.QTEREV_ID,SAQGPA.QTEREV_RECORD_ID,SAQGPA.SERVICE_DESCRIPTION,SAQGPA.SERVICE_ID,SAQGPA.SERVICE_RECORD_ID,SAQGPA.GREENBOOK,SAQGPA.GREENBOOK_RECORD_ID,SAQGPA.FABLOCATION_ID,SAQGPA.FABLOCATION_NAME,SAQGPA.FABLOCATION_RECORD_ID,SAQGPA.ASSEMBLY_DESCRIPTION,SAQGPA.ASSEMBLY_ID,SAQGPA.ASSEMBLY_RECORD_ID,SAQICO.SALESORG_ID,SAQICO.SALESORG_NAME,SAQICO.SALESORG_RECORD_ID,SAQGPA.EQUIPMENTTYPE_ID,SAQICO.QUOTE_ITEM_COVERED_OBJECT_RECORD_ID, SAQICO.CNTYER,SAQICO.LINE FROM                    
                                    {pmsa_assembly} (NOLOCK) SAQGPA JOIN {item_level_covered_object} SAQICO ON 
                                    SAQICO.QUOTE_RECORD_ID = SAQGPA.QUOTE_RECORD_ID AND SAQICO.QTEREV_RECORD_ID = 
                                    SAQGPA.QTEREV_RECORD_ID AND SAQICO.SERVICE_RECORD_ID = SAQGPA.SERVICE_RECORD_ID AND SAQICO.FABLOCATION_RECORD_ID = SAQGPA.FABLOCATION_RECORD_ID AND SAQICO.GREENBOOK_RECORD_ID = SAQGPA.GREENBOOK_RECORD_ID AND SAQICO.EQUIPMENT_ID = SAQGPA.EQUIPMENT_ID
                                    AND SAQICO.FABLOCATION_ID = SAQGPA.FABLOCATION_ID
                                    AND SAQICO.GOT_CODE = SAQGPA.GOT_CODE
                                    AND ISNULL(SAQICO.DEVICE_NODE,'') = ISNULL(SAQGPA.DEVICE_NODE,'')
                                    AND ISNULL(SAQICO.PROCES,'') = ISNULL(SAQGPA.PROCESS_TYPE,'')
                                    {condition} 
                                    WHERE SAQGPA.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQGPA.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQGPA.SERVICE_ID = '{ServiceId}'
                                ) SQ                            
                                JOIN SAQRIO (NOLOCK) ON SAQRIO.QUOTE_RECORD_ID = SQ.QUOTE_RECORD_ID AND SAQRIO.QTEREV_RECORD_ID = SQ.QTEREV_RECORD_ID AND SAQRIO.SERVICE_RECORD_ID = SQ.SERVICE_RECORD_ID AND SAQRIO.LINE = SQ.LINE AND SAQRIO.ASSEMBLY_ID = SQ.ASSEMBLY_ID
                                WHERE SAQRIO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRIO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQRIO.SERVICE_ID = '{ServiceId}'
                            ) IQ    
                            LEFT JOIN SAQICA (NOLOCK) ON SAQICA.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND SAQICA.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND SAQICA.SERVICE_RECORD_ID = IQ.SERVICE_RECORD_ID AND SAQICA.GREENBOOK_RECORD_ID = IQ.GREENBOOK_RECORD_ID AND SAQICA.FABLOCATION_RECORD_ID = IQ.FABLOCATION_RECORD_ID AND SAQICA.EQUIPMENT_RECORD_ID = IQ.EQUIPMENT_RECORD_ID AND SAQICA.ASSEMBLY_RECORD_ID = IQ.ASSEMBLY_RECORD_ID
                            WHERE ISNULL(SAQICA.ASSEMBLY_RECORD_ID,'') = ''
                        )OQ""".format(UserId=self.user_id, UserName=self.user_name, QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id, pmsa_assembly=SAQGPA_BKP,item_level_covered_object = SAQICO_BKP,condition = "AND ISNULL(SAQICO.KIT_ID,'') = ISNULL(SAQGPA.KIT_ID,'')" if self.service_id in ("Z0010","Z0128") else " AND ISNULL(SAQICO.KIT_ID,'') = ISNULL(SAQGPA.KIT_ID,'') AND ISNULL(SAQICO.OBJECT_ID,'') = CASE WHEN SAQICO.OBJECT_ID = 'Scheduled Maintenance' THEN SAQGPA.MNTEVT_LEVEL ELSE ISNULL(SAQGPA.PM_ID,'') END "  ))
                SAQGPA_BKP_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQGPA_BKP)+"'' ) BEGIN DROP TABLE "+str(SAQGPA_BKP)+" END  ' ")
                SAQICO_BKP_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQICO_BKP)+"'' ) BEGIN DROP TABLE "+str(SAQICO_BKP)+" END  ' ")
            except Exception:
                SAQGPA_BKP_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQGPA_BKP)+"'' ) BEGIN DROP TABLE "+str(SAQGPA_BKP)+" END  ' ")
                SAQICO_BKP_DRP = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(SAQICO_BKP)+"'' ) BEGIN DROP TABLE "+str(SAQICO_BKP)+" END  ' ")
                Log.Info("Occured Exception In Quote Item Assembly Insert For The Quote: {} And Revision: {}".format(self.contract_quote_id, self.contract_quote_revision_id))
            ##HPQC DEFECT 601 code ends...
                                    
    def _construct_dict_xml(self,updateentXML):
        entxmldict = {}
        pattern_tag = re.compile(r'(<QUOTE_ITEM_ENTITLEMENT>[\w\W]*?</QUOTE_ITEM_ENTITLEMENT>)')
        pattern_name = re.compile(r'<ENTITLEMENT_ID>([^>]*?)</ENTITLEMENT_ID>')
        entitlement_display_value_tag_pattern = re.compile(r'<ENTITLEMENT_DISPLAY_VALUE>([^>]*?)</ENTITLEMENT_DISPLAY_VALUE>')
        if updateentXML:
            for m in re.finditer(pattern_tag, updateentXML):
                sub_string = m.group(1)
                x=re.findall(pattern_name,sub_string)
                entitlement_display_value_tag_match = re.findall(entitlement_display_value_tag_pattern,sub_string)
                entxmldict[x[0]]=entitlement_display_value_tag_match[0].upper()
        return entxmldict			
    
    def _quote_items_assembly_entitlement_insert(self, update=True):
        # Update - Start
        #item_line_covered_object_assembly_entitlement_join_string = ""	
        #item_line_covered_object_assembly_entitlement_where_string = ""		
        #if update:
        item_line_covered_object_assembly_entitlement_where_string = "AND ISNULL(SAQIAE.ASSEMBLY_RECORD_ID,'') = '' "
        item_line_covered_object_assembly_entitlement_join_string = "LEFT JOIN SAQIAE (NOLOCK) ON SAQIAE.QUOTE_RECORD_ID = SAQSCE.QUOTE_RECORD_ID AND SAQIAE.QTEREV_RECORD_ID = SAQSCE.QTEREV_RECORD_ID AND SAQIAE.SERVICE_RECORD_ID = SAQSCE.SERVICE_RECORD_ID AND SAQIAE.FABLOCATION_RECORD_ID = SAQSCE.FABLOCATION_RECORD_ID AND SAQIAE.EQUIPMENT_RECORD_ID = SAQSCE.EQUIPMENT_RECORD_ID AND SAQIAE.ASSEMBLY_RECORD_ID = IQ.ASSEMBLY_RECORD_ID"
        # Update - End
        Log.Info("===>INSERT SAQIAE===> "+str("""INSERT SAQIAE (EQUIPMENT_ID,EQUIPMENT_RECORD_ID,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,CPS_CONFIGURATION_ID,CPS_MATCH_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,ASSEMBLY_ID,ASSEMBLY_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,ENTITLEMENT_XML,QUOTE_ITEM_ASSEMBLY_ENTITLEMENT_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified) 
        SELECT OQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_ASSEMBLY_ENTITLEMENT_RECORD_ID,'{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED,{UserId} as CpqTableEntryModifiedBy,GETDATE() as CpqTableEntryDateModified FROM (
            SELECT IQ.*,SAQSCE.ENTITLEMENT_XML FROM (
                SELECT 
                    DISTINCT SAQSCA.EQUIPMENT_ID,SAQSCA.EQUIPMENT_RECORD_ID,SAQTSE.QUOTE_ID,SAQTSE.QUOTE_RECORD_ID,SAQTSE.QTEREV_ID,SAQTSE.QTEREV_RECORD_ID,SAQTSE.SERVICE_DESCRIPTION,SAQTSE.SERVICE_ID,SAQTSE.SERVICE_RECORD_ID,SAQTSE.CPS_CONFIGURATION_ID,SAQTSE.CPS_MATCH_ID,SAQSCA.FABLOCATION_ID,SAQSCA.FABLOCATION_NAME,SAQSCA.FABLOCATION_RECORD_ID,SAQSCA.ASSEMBLY_ID,SAQSCA.ASSEMBLY_RECORD_ID,SAQTSE.SALESORG_ID,SAQTSE.SALESORG_NAME,SAQTSE.SALESORG_RECORD_ID 
                FROM SAQTSE (NOLOCK) 
                JOIN SAQSCA (NOLOCK) ON SAQSCA.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID AND SAQSCA.SERVICE_RECORD_ID = SAQTSE.SERVICE_RECORD_ID AND SAQSCA.QTEREV_RECORD_ID = SAQTSE.QTEREV_RECORD_ID WHERE SAQTSE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQTSE.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQTSE.SERVICE_ID = '{ServiceId}'
            ) IQ 
            JOIN SAQSCE (NOLOCK) ON SAQSCE.SERVICE_RECORD_ID = IQ.SERVICE_RECORD_ID AND SAQSCE.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND SAQSCE.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND SAQSCE.EQUIPMENT_ID = IQ.EQUIPMENT_ID AND ISNULL(SAQSCE.CONFIGURATION_STATUS,'') = 'COMPLETE' 
            {JoinString}
            WHERE SAQSCE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCE.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQSCE.SERVICE_ID = '{ServiceId}' {WhereString}
        )OQ""".format(UserId=self.user_id, UserName=self.user_name, QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id,JoinString=item_line_covered_object_assembly_entitlement_join_string, WhereString=item_line_covered_object_assembly_entitlement_where_string))
        )
        Sql.RunQuery("""INSERT SAQIAE (EQUIPMENT_ID,EQUIPMENT_RECORD_ID,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,CPS_CONFIGURATION_ID,CPS_MATCH_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,ASSEMBLY_ID,ASSEMBLY_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,ENTITLEMENT_XML,QUOTE_ITEM_ASSEMBLY_ENTITLEMENT_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified) 
        SELECT OQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_ASSEMBLY_ENTITLEMENT_RECORD_ID,'{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED,{UserId} as CpqTableEntryModifiedBy,GETDATE() as CpqTableEntryDateModified FROM (
            SELECT IQ.*,SAQSCE.ENTITLEMENT_XML FROM (
                SELECT 
                    DISTINCT SAQSCA.EQUIPMENT_ID,SAQSCA.EQUIPMENT_RECORD_ID,SAQTSE.QUOTE_ID,SAQTSE.QUOTE_RECORD_ID,SAQTSE.QTEREV_ID,SAQTSE.QTEREV_RECORD_ID,SAQTSE.SERVICE_DESCRIPTION,SAQTSE.SERVICE_ID,SAQTSE.SERVICE_RECORD_ID,SAQTSE.CPS_CONFIGURATION_ID,SAQTSE.CPS_MATCH_ID,SAQSCA.FABLOCATION_ID,SAQSCA.FABLOCATION_NAME,SAQSCA.FABLOCATION_RECORD_ID,SAQSCA.ASSEMBLY_ID,SAQSCA.ASSEMBLY_RECORD_ID,SAQTSE.SALESORG_ID,SAQTSE.SALESORG_NAME,SAQTSE.SALESORG_RECORD_ID 
                FROM SAQTSE (NOLOCK) 
                JOIN SAQSCA (NOLOCK) ON SAQSCA.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID AND SAQSCA.SERVICE_RECORD_ID = SAQTSE.SERVICE_RECORD_ID AND SAQSCA.QTEREV_RECORD_ID = SAQTSE.QTEREV_RECORD_ID WHERE SAQTSE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQTSE.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQTSE.SERVICE_ID = '{ServiceId}'
            ) IQ 
            JOIN SAQSCE (NOLOCK) ON SAQSCE.SERVICE_RECORD_ID = IQ.SERVICE_RECORD_ID AND SAQSCE.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND SAQSCE.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND SAQSCE.EQUIPMENT_ID = IQ.EQUIPMENT_ID AND ISNULL(SAQSCE.CONFIGURATION_STATUS,'') = 'COMPLETE' 
            {JoinString}
            WHERE SAQSCE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCE.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQSCE.SERVICE_ID = '{ServiceId}' {WhereString}
        )OQ""".format(UserId=self.user_id, UserName=self.user_name, QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id,JoinString=item_line_covered_object_assembly_entitlement_join_string, WhereString=item_line_covered_object_assembly_entitlement_where_string))
    
    def _entitlement_valuedriver(self):
        
        if self.service_id =='Z0004':
            Sql.RunQuery("""UPDATE SAQICO
                SET SAQICO.ITPRMD = CASE WHEN {Objectame}.PRMKPI_ENT = 'Supplier Dependent Uptime' THEN 'MSLIKE' ELSE 'SSLIKE' END
                    FROM SAQICO (NOLOCK)
                    JOIN {Objectame} (NOLOCK) ON {Objectame}.QUOTE_RECORD_ID = SAQICO.QUOTE_RECORD_ID AND {Objectame}.SERVICE_ID = SAQICO.SERVICE_ID AND {Objectame}.QTEREV_RECORD_ID = SAQICO.QTEREV_RECORD_ID
                    AND {Objectame}.GREENBOOK = SAQICO.GREENBOOK AND {Objectame}.EQUIPMENT_ID = SAQICO.EQUIPMENT_ID
                    WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}'
                    """.format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id, Objectame = self.source_object_name))
        elif self.service_id =='Z0099':
            Sql.RunQuery("""UPDATE SAQICO
                SET SAQICO.ITPRMD = CASE WHEN {Objectame}.PRMKPI_ENT = 'Response Time' THEN 'SSLIKE' ELSE NULL END
                    FROM SAQICO (NOLOCK)
                    JOIN {Objectame} (NOLOCK) ON {Objectame}.QUOTE_RECORD_ID = SAQICO.QUOTE_RECORD_ID AND {Objectame}.SERVICE_ID = SAQICO.SERVICE_ID AND {Objectame}.QTEREV_RECORD_ID = SAQICO.QTEREV_RECORD_ID
                    AND {Objectame}.GREENBOOK = SAQICO.GREENBOOK AND {Objectame}.EQUIPMENT_ID = SAQICO.EQUIPMENT_ID
                    WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}'
                    """.format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id, Objectame = self.source_object_name))
        ##PMSA
        elif self.service_id == "Z0009" and self.quote_service_entitlement_type not in ("STR-OFFBGBSMKTGCPCND OBJ-AS"):
            if self.quote_service_entitlement_type == "STR-OFFBGBPMCMKTGCPCND OBJ-AS":
                join_display_condition = " AND {Objectame}.PM_ID = SAQICO.PM_ID AND {Objectame}.GOT_CODE = SAQICO.GOT_CODE AND {Objectame}.KIT_ID = SAQICO.KIT_ID".format(Objectame =self.source_object_name)
            else:
                join_display_condition= " AND {Objectame}.GREENBOOK = SAQICO.GREENBOOK AND {Objectame}.EQUIPMENT_ID = SAQICO.EQUIPMENT_ID ".format(Objectame=self.source_object_name)
            Sql.RunQuery("""UPDATE SAQICO
                SET SAQICO.ITPRMD = CASE WHEN {Objectame}.QTETYP = 'Event Based' THEN 'EVENT' WHEN {Objectame}.QTETYP = 'Flex Event Based' THEN 'FLEX' ELSE 'TOOL' END
                    FROM SAQICO (NOLOCK)
                    JOIN {Objectame} (NOLOCK) ON {Objectame}.QUOTE_RECORD_ID = SAQICO.QUOTE_RECORD_ID AND {Objectame}.QTEREV_RECORD_ID = SAQICO.QTEREV_RECORD_ID AND {Objectame}.SERVICE_ID = SAQICO.SERVICE_ID {join_display_condition}
                    
                    WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}'
                    """.format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id, Objectame = self.source_object_name, join_display_condition= join_display_condition))
        #Schl.Maintainance
        elif self.quote_service_entitlement_type in ("STR-OFFBGBSMKTGCPCND OBJ-AS"):	
            Sql.RunQuery("""UPDATE SAQICO
                SET SAQICO.ITPRMD = CASE WHEN {Objectame}.QTETYP = 'Event Based' THEN 'EVENT' WHEN {Objectame}.QTETYP = 'Flex Event Based' THEN 'FLEX' ELSE 'TOOL' END
                    FROM SAQICO (NOLOCK)
                    JOIN {Objectame} (NOLOCK) ON {Objectame}.QUOTE_RECORD_ID = SAQICO.QUOTE_RECORD_ID AND {Objectame}.QTEREV_RECORD_ID = SAQICO.QTEREV_RECORD_ID AND {Objectame}.SERVICE_ID = SAQICO.SERVICE_ID AND {Objectame}.PM_ID = SAQICO.PM_ID AND SAQGPE.KIT_ID = SAQICO.KIT_ID AND {Objectame}.GOT_CODE = SAQICO.GOT_CODE AND SAQICO.MNTEVT_LEVEL != 'Scheduled Maintenance' 
                    
                    WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}' AND SAQICO.MNTEVT_LEVEL != 'Scheduled Maintenance' 
                    """.format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id, Objectame = self.source_object_name))
            
            Sql.RunQuery("""UPDATE SAQICO
                SET SAQICO.ITPRMD = CASE WHEN SAQSGE.QTETYP = 'Event Based' THEN 'EVENT' WHEN SAQSGE.QTETYP = 'Flex Event Based' THEN 'FLEX' ELSE 'TOOL' END
                    FROM SAQICO (NOLOCK)
                    INNER JOIN SAQSGE (NOLOCK) ON SAQSGE.QUOTE_RECORD_ID = SAQICO.QUOTE_RECORD_ID AND SAQSGE.QTEREV_RECORD_ID = SAQICO.QTEREV_RECORD_ID AND SAQSGE.SERVICE_ID = SAQICO.SERVICE_ID AND SAQSGE.GREENBOOK = SAQICO.GREENBOOK AND SAQICO.MNTEVT_LEVEL = 'Scheduled Maintenance' WHERE 
                        SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}' AND SAQICO.MNTEVT_LEVEL = 'Scheduled Maintenance'""".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id) )	
        ##Kit based			
        elif self.quote_service_entitlement_type in ("STR-OFFBGBKTGCPCND OBJ-GPAS"):
            check_valuedriver = Sql.GetFirst("SELECT * FROM PREGBV WHERE ENTITLEMENT_ID = 'AGS_{}_VAL_CCDVAL' AND PREGBV.ACTIVE = 1".format(self.service_id) )
            if check_valuedriver:
                Sql.RunQuery("""UPDATE SAQICO
                SET SAQICO.CCDFFV = SAQGPA.CLEAN_COAT_DIFF
                    FROM SAQICO (NOLOCK)
                    JOIN SAQGPA (NOLOCK) ON SAQGPA.QUOTE_RECORD_ID = SAQICO.QUOTE_RECORD_ID AND SAQGPA.QTEREV_RECORD_ID = SAQICO.QTEREV_RECORD_ID AND SAQGPA.SERVICE_ID = SAQICO.SERVICE_ID AND SAQGPA.KIT_ID = SAQICO.KIT_ID AND SAQGPA.GOT_CODE = SAQICO.GOT_CODE AND SAQICO.EQUIPMENT_ID = SAQGPA.EQUIPMENT_ID
                    WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}' 
                    """.format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id, Objectame = self.source_object_name))
            Sql.RunQuery("""UPDATE SAQICO
                SET SAQICO.ITPRMD = CASE WHEN {Objectame}.QTETYP = 'Event Based' THEN 'EVENT' WHEN {Objectame}.QTETYP = 'Flex Event Based' THEN 'FLEX' ELSE 'TOOL' END
                    FROM SAQICO (NOLOCK)
                    JOIN {Objectame} (NOLOCK) ON {Objectame}.QUOTE_RECORD_ID = SAQICO.QUOTE_RECORD_ID AND {Objectame}.QTEREV_RECORD_ID = SAQICO.QTEREV_RECORD_ID AND {Objectame}.SERVICE_ID = SAQICO.SERVICE_ID AND {Objectame}.KIT_ID = SAQICO.KIT_ID AND {Objectame}.GOT_CODE = SAQICO.GOT_CODE AND {Objectame}.GREENBOOK = SAQICO.GREENBOOK 
                    
                    WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}' 
                    """.format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id, Objectame = self.source_object_name))
        Sql.RunQuery("""UPDATE SAQICO
                SET SAQICO.QRQVDV = SAQFBL.QUALITY_REQUIRED
                    FROM SAQICO (NOLOCK)
                    JOIN SAQFBL (NOLOCK) ON SAQFBL.FABLOCATION_ID = SAQICO.FABLOCATION_ID AND SAQICO.QUOTE_RECORD_ID = SAQFBL.QUOTE_RECORD_ID AND SAQICO.QTEREV_RECORD_ID = SAQFBL.QTEREV_RECORD_ID
                    WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}'
                    """.format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
        ##cleaning and coating
        Sql.RunQuery("""UPDATE SAQICO SET SPCCLN = ITSPCL,SPCCOT = ITSPCT WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}'""".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id))
        #INC08922527 - Start - M
        #Specialized Cleaning Cost Impact
        Sql.RunQuery("""UPDATE SAQICO
                                SET SPCCLC = CONVERT(DECIMAL(18,5),PRCFVA.FACTOR_TXTVAR)		
                                    FROM SAQICO (NOLOCK)
                                    JOIN PRCFVA (NOLOCK) ON PRCFVA.FACTOR_VARIABLE_ID = SAQICO.SERVICE_ID
                                    WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}' AND SAQICO.ITSPCL = 'Included' AND ISNULL(PRCFVA.FACTOR_ID,'') = 'AISCCI'
                                    """.format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
        #Specialized Cleaning Price Impact
        Sql.RunQuery("""UPDATE SAQICO
                                SET SPCCLP = CONVERT(DECIMAL(18,5),PRCFVA.FACTOR_TXTVAR)		
                                    FROM SAQICO (NOLOCK)
                                    JOIN PRCFVA (NOLOCK) ON PRCFVA.FACTOR_VARIABLE_ID = SAQICO.SERVICE_ID
                                    WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}' AND SAQICO.ITSPCL = 'Included' AND ISNULL(PRCFVA.FACTOR_ID,'') = 'AISCPI'
                                    """.format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
                                
        #Specialized Coating Cost Impact
        Sql.RunQuery("""UPDATE SAQICO
                                SET SPCCCI = CONVERT(DECIMAL(18,5),PRCFVA.FACTOR_TXTVAR)		
                                    FROM SAQICO (NOLOCK)
                                    JOIN PRCFVA (NOLOCK) ON PRCFVA.FACTOR_VARIABLE_ID = SAQICO.SERVICE_ID
                                    WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}' AND SAQICO.ITSPCT = 'Included' AND ISNULL(PRCFVA.FACTOR_ID,'') = 'AISTCI'
                                    """.format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
        #Specialized Coating Cost Impact
        Sql.RunQuery("""UPDATE SAQICO
                                SET SPCCPI = CONVERT(DECIMAL(18,5),PRCFVA.FACTOR_TXTVAR)		
                                    FROM SAQICO (NOLOCK)
                                    JOIN PRCFVA (NOLOCK) ON PRCFVA.FACTOR_VARIABLE_ID = SAQICO.SERVICE_ID
                                    WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}' AND SAQICO.ITSPCT = 'Included' AND ISNULL(PRCFVA.FACTOR_ID,'') = 'AISTPI'
                                    """.format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
        #INC08922527 - End - M 
        ##quality required, wafer node, device type, csa tool
        if self.quote_service_entitlement_type in ('STR-OFFBGB OBJ-GREQ PRD-GRPT','STR-OFFBGB OBJ-GREQ','STR-OFFBGB OBJ-EQ','STR-OFFBGR OBJ-GREQ','STR-OFFBGB OBJ-ASKT','STR-OFFBGBCRSOGL OBJ-GREQ','STR-OFFBGBPMCMKTGCPCND OBJ-AS','STR-OFFBGBSMKTGCPCND OBJ-AS','STR-OFFBGBKTGCPCND OBJ-GPAS'):
            if self.quote_service_entitlement_type in ("STR-OFFBGBKTGCPCND OBJ-GPAS","STR-OFFBGBPMCMKTGCPCND OBJ-AS","STR-OFFBGBSMKTGCPCND OBJ-AS"):
                Sql.RunQuery("""UPDATE SAQICO
                        SET SAQICO.DTPVDV = MAEQUP.VALDRV_DEVICETYPE,
                            SAQICO.WNDVDV = MAEQUP.VALDRV_WAFERNODE
                            FROM SAQICO (NOLOCK)
                            JOIN MAEQUP (NOLOCK) ON MAEQUP.EQUIPMENT_ID = SAQICO.EQUIPMENT_ID
                            WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}'
                            """.format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
                #csa tool
                ent_value_des = ''
                ent_value_non_des = ''
                account_id_query = Sql.GetFirst("SELECT BLUEBOOK FROM SAQTRV WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' ".format(self.contract_quote_record_id,self.contract_quote_revision_record_id ))
                tools_count_query = Sql.GetFirst("SELECT COUNT(EQUIPMENT_ID) AS COUNT FROM SAQSCO (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' ".format(self.contract_quote_record_id,self.contract_quote_revision_record_id ))
                if account_id_query.BLUEBOOK != "DES":
                    if tools_count_query.COUNT < 10:
                        ent_value_non_des = '<10'
                    elif tools_count_query.COUNT in range(10,51):
                        ent_value_non_des = '>10 to <=50'
                    elif tools_count_query.COUNT > 50:
                        ent_value_non_des = '>50'
                elif account_id_query.BLUEBOOK == "DES" :
                    if tools_count_query.COUNT > 7:
                        ent_value_des = '>7'
                    elif tools_count_query.COUNT in range(3,8):
                        ent_value_des = '>=3 to <=7'
                    elif tools_count_query.COUNT < 3:
                        ent_value_des = '<3'
                #if ent_value_des :
                Sql.RunQuery("""UPDATE SAQICO
                        SET SAQICO.CSTVDV = '{ent_value_des}',
                            SAQICO.ITTNBV = '{ent_value_non_des}'
                            FROM SAQICO (NOLOCK)
                            WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}'
                            """.format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id,ent_value_non_des =ent_value_non_des,ent_value_des = ent_value_des))
        ##coefficient value updating
        ent_dict = [{
                        "field":["DTPVDC","Device Type Coefficient","DTPVDV","AGS_{}_VAL_DEVTYP".format(self.service_id)]
                        },
                        {
                        "field":["WNDVDC","Wafer Node Coefficient","WNDVDV","AGS_{}_VAL_WAFNOD".format(self.service_id)]	
                        },
                        {
                        "field":["QRQVDC","Quality Required Coefficient","QRQVDV","AGS_{}_VAL_QLYREQ".format(self.service_id)]	
                        },
                        {
                        "field":["UIMVDC","Uptime Improvement Coefficient","UIMVDV","AGS_{}_VAL_UPIMPV".format(self.service_id)]	
                        },
                        {
                        "field":["CAVVDC","Capital Avoidance Coefficient","CAVVDV","AGS_{}_VAL_CAPACO".format(self.service_id)]	
                        },
                        {
                        "field":["CCRTMC","Contract Coverage & Response Time Coefficient","CCRTMV","AGS_{}_VAL_CCRTME".format(self.service_id)]	
                        },
                        {
                        "field":["CCDFFC","Cleaning Coating Diff coeff.","CCDFFV","AGS_{}_VAL_CCDVAL".format(self.service_id)]
                        },
                        {
                        "field":["INTCPC","Intercept Coefficient","INTCPV","AGS_{}_VAL_INTCPT".format(self.service_id)]
                        },
                        {
                        "field":["OSSVDV","Total Cost W/O Seedstock","","AGS_{}_VAL_TBCOST".format(self.service_id)]	
                        },
                        {
                        "field":["POFVDC","Product Offering Coefficient","POFVDV","AGS_{}_VAL_POFFER".format(self.service_id)]
                        },
                        {
                        "field":["GBKVDC","Greenbook Coefficient","GREENBOOK","AGS_{}_VAL_GRNBKV".format(self.service_id)]
                        },
                        {
                        "field":["CSTVDC", "# CSA Tools per Fab Coefficient","CSTVDV","AGS_{}_VAL_TLSFAB".format(self.service_id)]
                        },
                        {
                        "field":["ITTNBC", "# CSA Tools/Fab BL<>DES Coeff","ITTNBV","AGS_{}_VAL_CTFNBB".format(self.service_id)]
                        },
                        {
                        "field":["CSGVDC", "Customer Segment Coefficent","CSGVDV","AGS_{}_VAL_CSTSEG".format(self.service_id)]
                        },
                        {
                        "field":["SVCVDC", "Service Competition Coefficient","SVCVDV","AGS_{}_VAL_SVCCMP".format(self.service_id)]
                        },	
                    ]
        if ent_dict:
            join_condition =''
            if self.service_id in ('Z0128','Z0010','Z0009','Z0099'):
                join_condition = " AND SAQICO.ITPRMD = PREGBV.MODE"
            
            for rec in ent_dict:
                uptime_join_condition = ''
                if rec['field'][0] in ('UIMVDC','CSTVDC','ITTNBC'):
                    uptime_join_condition = " AND ENTITLEMENT_DISPLAY_VALUE in (SELECT REPLACE(REPLACE(REPLACE(REPLACE({},';#38gt;','>'),';#38lt;','<'),'&lt;','<'),'&gt;','>') FROM SAQICO GB WHERE GB.CPQTABLEENTRYID = SAQICO.CPQTABLEENTRYID  )".format(rec['field'][2])
                    join_display_condition = ''
                else:
                    join_display_condition = " AND ENTITLEMENT_DISPLAY_VALUE = "+"SAQICO."+str(rec['field'][2])	
                coeff_col_value = 'PREGBV.ENTITLEMENT_COEFFICIENT'
                if rec['field'][0] == 'OSSVDV':
                    coeff_col_value = 'PREGBV.ENTITLEMENT_DISPLAY_VALUE'
                    join_display_condition = ''
                #ROUND(ISNULL(PREGBV.ENTITLEMENT_COEFFICIENT,0),CONVERT(NUMERIC,3) )
                Sql.RunQuery("""UPDATE SAQICO 
                        SET SAQICO.{coeff_field} = {coeff_col_value}
                        FROM SAQICO (NOLOCK)
                        INNER JOIN PREGBV ON PREGBV.SERVICE_ID = SAQICO.SERVICE_ID AND ENTITLEMENT_ID = '{entitlement_id}'  AND SAQICO.GREENBOOK = PREGBV.GREENBOOK {join_condition}
                            WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND ENTITLEMENT_ID = '{entitlement_id}' AND ISNULL(ENTITLEMENT_DISPLAY_VALUE,'') != ''  {uptime_join_condition}
                        """.format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id, coeff_field = rec['field'][0], entitlement_id = rec['field'][3], join_condition = join_condition + join_display_condition,coeff_col_value = coeff_col_value ,uptime_join_condition = uptime_join_condition ))
        #INC08821708 - Start - A/M
        api_names = ['UIMVDV','ITTNBV']
        replace_dict = {
                        "&gt;":">",
                        "&lt;":"<",
                        ";&gt;":">",
                        ";&lt;":"<",
                        "#38gt;":">",
                        "#38lt;":"<",
                        ";#38gt;":">",
                        ";#38lt;":"<",
                        ";>":">",
                        ";<":"<",
                        }
        condition_strs = []
        condition_str = ""
        for api in api_names:
            condition_str = ""
            for index,symbol in enumerate(replace_dict.Keys):
                if index==0:
                    condition_str += " REPLACE({},'{}','{}')".format(api,symbol,replace_dict.get(symbol))
                else:
                    condition_str = " REPLACE({},'{}','{}')".format(condition_str,symbol,replace_dict.get(symbol))
            condition_strs.append(api+" = "+condition_str)
        Sql.RunQuery(""" UPDATE SAQICO SET {cndtn} WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}' """.format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id,cndtn = ",".join(condition_strs)))
        #INC08821708 - End - A/M
        return True
        
    def _quote_annualized_items_insert(self, update=False):
        basic_insert_start = time.time()
        ancillary_join = ""
        # if self.service_id != 'Z0105':
        #     ancillary_join =" AND ISNULL(SAQRIT.PAR_PRDOFR_ID,'') = ISNULL(SAQSCO.PAR_SERVICE_ID,'')"
        ancillary_where =""
        # if self.is_ancillary == True or self.addon_product == True:
        # 	ancillary_join = """JOIN SAQRIT (NOLOCK) PAR_SAQRIT ON PAR_SAQRIT.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID 
        # 												AND PAR_SAQRIT.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID 
        # 												AND PAR_SAQRIT.SERVICE_ID =SAQRIT.PAR_SERVICE_ID 
        # 												AND PAR_SAQRIT.SERVICE_ID = '{par_service_id}' 
        # 												AND ISNULL(PAR_SAQRIT.GREENBOOK_RECORD_ID,'') = ISNULL(SAQRIT.GREENBOOK_RECORD_ID,'') 
        # 												AND PAR_SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID = SAQRIT.PARQTEITM_LINE_RECORD_ID """.format(par_service_id = self.parent_service_id)	
        # 	if self.quote_service_entitlement_type in ('OFFERING + EQUIPMENT','OFFERING+EQUIPMENT','OFRNG+EQUIP','STR-OFFBGREQPODV OBJ-EQ'):
        # 		ancillary_join += " AND PAR_SAQRIT.FABLOCATION_RECORD_ID = SAQRIT.FABLOCATION_RECORD_ID AND ISNULL(PAR_SAQRIT.EQUIPMENT_ID,'') = SAQRIT.EQUIPMENT_ID"
        # 	ancillary_where =  " AND PAR_SAQRIT.SERVICE_ID = '{parent_service_id}'".format(parent_service_id = self.parent_service_id)
        contract_years_obj = Sql.GetList("SELECT CONTRACT_END_DATE, CONTRACT_START_DATE, CNTYER FROM SAQCYR (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id))
        # CR704 - End - M
        if self.quote_service_entitlement_type in ('STR-OFFBGREQPODV OBJ-EQ','STR-OFFBGBEQ OBJ-EQ'):
            # CR704 - Start - M		 
            for contract_year_obj in contract_years_obj:
                if contract_year_obj.CNTYER == 'YEAR 1':
                    yearwise_join_str = "JOIN SAQCYR (NOLOCK) ON SAQCYR.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND SAQCYR.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID AND SAQCYR.CONTRACT_START_DATE <= SAQRIT.CONTRACT_VALID_FROM AND SAQCYR.CONTRACT_END_DATE >= SAQRIT.CONTRACT_VALID_FROM"
                else:
                    yearwise_join_str = "JOIN SAQCYR (NOLOCK) ON SAQCYR.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND SAQCYR.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID AND ((SAQCYR.CONTRACT_START_DATE >= SAQRIT.CONTRACT_VALID_FROM AND SAQCYR.CONTRACT_START_DATE <= SAQRIT.CONTRACT_VALID_TO) OR (SAQCYR.CONTRACT_START_DATE <= SAQRIT.CONTRACT_VALID_FROM AND SAQCYR.CONTRACT_END_DATE >= SAQRIT.CONTRACT_VALID_FROM))"
                #INC08675532 #INC08675479 - START - M
                Sql.RunQuery("""INSERT SAQICO (EQUIPMENT_DESCRIPTION, STATUS, QUANTITY, OBJECT_ID, EQUPID, EQUIPMENT_ID, EQUIPMENT_RECORD_ID, LINE, QUOTE_ID, QTEITM_RECORD_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, KPU, SERNUM, SERIAL_NO, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, TECHNOLOGY, CUSTOMER_TOOL_ID, EQUCAT, EQUIPMENTCATEGORY_ID, EQUIPMENTCATEGORY_RECORD_ID, EQUIPMENT_STATUS, MNT_PLANT_ID, MNT_PLANT_NAME, MNT_PLANT_RECORD_ID, SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID, FABLOC, FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, GRNBOK, GREENBOOK, GREENBOOK_RECORD_ID, GLOBAL_CURRENCY,GLOBAL_CURRENCY_RECORD_ID, OBJECT_TYPE, BLUBOK, WTYSTE, WTYEND, WTYDAY, PLTFRM, SUBSIZ, REGION, ISPOES, CSTSRC, PRCSRC, TAXVTP,TAXGRP,DCCRFX,DCCRXD,DOCCUR, INTCPV, INTCPC, OSSVDV, LTCOSS, POFVDV, POFVDC, GBKVDV, GBKVDC, UIMVDV, UIMVDC, CAVVDV, CAVVDC, WNDVDV, WNDVDC, CCRTMV, CCRTMC, SCMVDV, SCMVDC, CCDFFV, CCDFFC, NPIVDV, NPIVDC, DTPVDV, DTPVDC, CSTVDV, CSTVDC, CSGVDV, CSGVDC, QRQVDV, QRQVDC, SVCVDV, SVCVDC, RKFVDV, RKFVDC, PBPVDV, PBPVDC, CMLAB_ENT, CNSMBL_ENT, CNTCVG_ENT, NCNSMB_ENT, PMEVNT_ENT, PMLAB_ENT, PRMKPI_ENT, OFRING, QTETYP, BILTYP, BPTTKP, ATGKEY, TGKPNS, NWPTON, HEDBIN, WETCLN_ENT, SPQTEV, SVSPCT, SPSPCT,SWPKTA,NUMLAY,ITTNBV,ITSDUB,ITSDUT,ITSPCL,ITSPCT,CNTYER, STADTE, CONTRACT_VALID_FROM, ENDDTE, CONTRACT_VALID_TO, CNTDAY, QUOTE_ITEM_COVERED_OBJECT_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified)
                        SELECT DISTINCT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_COVERED_OBJECT_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED,{UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (                        
                        SELECT DISTINCT					
                            SAQSCO.EQUIPMENT_DESCRIPTION,
                            null as STATUS,
                            SAQSCO.EQUIPMENT_QUANTITY,
                            SAQRIT.OBJECT_ID,
                            SAQSCO.EQUIPMENT_ID as EQUPID,
                            SAQSCO.EQUIPMENT_ID,
                            SAQSCO.EQUIPMENT_RECORD_ID,
                            SAQRIT.LINE,
                            SAQRIT.QUOTE_ID, 
                            SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID, 
                            SAQRIT.QUOTE_RECORD_ID,
                            SAQRIT.QTEREV_ID,
                            SAQRIT.QTEREV_RECORD_ID,
                            SAQSCO.KPU,
                            SAQSCO.SERIAL_NO as SERNUM, 
                            SAQSCO.SERIAL_NO, 
                            SAQRIT.SERVICE_DESCRIPTION, 
                            SAQRIT.SERVICE_ID, 
                            SAQRIT.SERVICE_RECORD_ID,								
                            SAQSCO.TECHNOLOGY,																			
                            SAQSCO.CUSTOMER_TOOL_ID, 
                            SAQSCO.EQUIPMENTCATEGORY_ID as EQUCAT, 
                            SAQSCO.EQUIPMENTCATEGORY_ID, 
                            SAQSCO.EQUIPMENTCATEGORY_RECORD_ID, 
                            SAQSCO.EQUIPMENT_STATUS,					
                            SAQSCO.MNT_PLANT_ID, 
                            SAQSCO.MNT_PLANT_NAME, 
                            SAQSCO.MNT_PLANT_RECORD_ID,				
                            SAQSCO.SALESORG_ID, 
                            SAQSCO.SALESORG_NAME, 
                            SAQSCO.SALESORG_RECORD_ID,  
                            SAQRIT.FABLOCATION_ID as FABLOC,
                            SAQRIT.FABLOCATION_ID,
                            SAQRIT.FABLOCATION_NAME,
                            SAQRIT.FABLOCATION_RECORD_ID,
                            SAQRIT.GREENBOOK as GRNBOK, 
                            SAQRIT.GREENBOOK, 
                            SAQRIT.GREENBOOK_RECORD_ID, 			
                            SAQTRV.GLOBAL_CURRENCY,
                            SAQTRV.GLOBAL_CURRENCY_RECORD_ID,					
                            SAQRIT.OBJECT_TYPE,
                            SAQTRV.BLUEBOOK as BLUBOK,
                            SAQSCO.WARRANTY_START_DATE as WTYSTE,
                            SAQSCO.WARRANTY_END_DATE as WTYEND,
                            Abs(DATEDIFF(day,SAQSCO.WARRANTY_END_DATE, SAQSCO.WARRANTY_START_DATE)) as WTYDAY,
                            SAQSCO.PLATFORM	as PLTFRM,
                            SAQSCO.WAFER_SIZE as SUBSIZ,
                            SAQTRV.REGION as REGION,
                            SAQTMT.POES as ISPOES,
                            CASE WHEN ISNULL(PRSPRV.SSCM_COST, 0) = 1 THEN 'SSCM' ELSE 'CPQ' END as CSTSRC,
                            CASE WHEN ISNULL(PRSPRV.SSCM_COST, 0) = 1 THEN 'VALUE PRICING-SSCM' ELSE 'OFFLINE PRICING' END as PRCSRC,
                            --'No' as SPQTEV,
                            SAQRIT.TAX_PERCENTAGE as TAXVTP,
                            SAQRIT.TAXCLASSIFICATION_ID,
                            SAQTRV.EXCHANGE_RATE,
                            SAQTRV.EXCHANGE_RATE_DATE,
                            SAQTRV.DOC_CURRENCY,
                            SAQSCE.INTCPV,
                            SAQSCE.INTCPC,
                            SAQSCE.OSSVDV,
                            SAQSCE.LTCOSS,
                            SAQSCE.POFVDV,
                            SAQSCE.POFVDC,
                            SAQSCE.GREENBOOK as GBKVDV,
                            SAQSCE.GBKVDC,
                            SAQSCE.UIMVDV,
                            SAQSCE.UIMVDC,
                            SAQSCE.CAVVDV,
                            SAQSCE.CAVVDC,
                            SAQSCE.WNDVDV,
                            SAQSCE.WNDVDC,
                            SAQSCE.CCRTMV,
                            SAQSCE.CCRTMC,
                            SAQSCE.SCMVDV,
                            SAQSCE.SCMVDC,
                            SAQSCE.CCDFFV,
                            SAQSCE.CCDFFC,
                            SAQSCE.NPIVDV,
                            SAQSCE.NPIVDC,
                            SAQSCE.DTPVDV,
                            SAQSCE.DTPVDC,
                            SAQSCE.CSTVDV,
                            SAQSCE.CSTVDC,
                            SAQSCE.CSGVDV,
                            SAQSCE.CSGVDC,
                            SAQSCE.QRQVDV,
                            SAQSCE.QRQVDC,
                            SAQSCE.SVCVDV,
                            SAQSCE.SVCVDC,
                            SAQSCE.RKFVDV,
                            SAQSCE.RKFVDC,
                            SAQSCE.PBPVDV,
                            SAQSCE.PBPVDC,
                            SAQSCE.CMLAB_ENT,
                                                
                            SAQSCE.CNSMBL_ENT,
                            SAQSCE.CNTCVG_ENT,
                            SAQSCE.NCNSMB_ENT,
                            SAQSCE.PMEVNT_ENT,
                            SAQSCE.PMLAB_ENT,
                            SAQSCE.PRMKPI_ENT,
                            SAQSCE.OFRING,
                            SAQSCE.QTETYP,
                            SAQSCE.BILTYP,
                            SAQSCE.BPTKPI,
                            SAQSCE.ATGKEY,
                            SAQSCE.ATNKEY,                            
                            SAQSCE.NWPTON,
                            SAQSCE.HEDBIN,
                            SAQSCE.WETCLN_ENT,
                            SAQSCE.SPQTEV,
                            SAQSCE.SVSPCT,
                            SAQSCE.SPSPCT,
                            SAQSCE.SWPKTA,
                            SAQSCE.NUMLAY,
                            SAQSCE.ITTNBV,
                            SAQSCE.ITSDUB,
                            SAQSCE.ITSDUT,
                            SAQSCE.ITSPCL,
                            SAQSCE.ITSPCT,
                            SAQCYR.CNTYER as CNTYER,
                            CASE WHEN SAQRIT.CONTRACT_VALID_FROM > SAQCYR.CONTRACT_START_DATE THEN SAQRIT.CONTRACT_VALID_FROM ELSE SAQCYR.CONTRACT_START_DATE END as STADTE,
                            CASE WHEN SAQRIT.CONTRACT_VALID_FROM > SAQCYR.CONTRACT_START_DATE THEN SAQRIT.CONTRACT_VALID_FROM ELSE SAQCYR.CONTRACT_START_DATE END as CONTRACT_VALID_FROM,
                            CASE WHEN SAQCYR.CONTRACT_END_DATE > SAQRIT.CONTRACT_VALID_TO THEN SAQRIT.CONTRACT_VALID_TO ELSE SAQCYR.CONTRACT_END_DATE END as ENDDTE,
                            CASE WHEN SAQCYR.CONTRACT_END_DATE > SAQRIT.CONTRACT_VALID_TO THEN SAQRIT.CONTRACT_VALID_TO ELSE SAQCYR.CONTRACT_END_DATE END as CONTRACT_VALID_TO,
                            Abs(DATEDIFF(day,CASE WHEN SAQCYR.CONTRACT_END_DATE > SAQRIT.CONTRACT_VALID_TO THEN SAQRIT.CONTRACT_VALID_TO ELSE SAQCYR.CONTRACT_END_DATE END , CASE WHEN SAQRIT.CONTRACT_VALID_FROM > SAQCYR.CONTRACT_START_DATE THEN SAQRIT.CONTRACT_VALID_FROM ELSE SAQCYR.CONTRACT_START_DATE END)) + 1 as CNTDAY                  
                        FROM 
                            SAQSCO (NOLOCK)					 
                            JOIN SAQSCE (NOLOCK) ON SAQSCE.QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID AND SAQSCE.SERVICE_ID = SAQSCO.SERVICE_ID AND SAQSCE.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID AND ISNULL(SAQSCO.PAR_SERVICE_ID,'') = ISNULL(SAQSCE.PAR_SERVICE_ID,'') AND QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID = SAQSCE.QTESRVCOB_RECORD_ID
                            AND SAQSCE.EQUIPMENT_RECORD_ID = SAQSCO.EQUIPMENT_RECORD_ID
                            JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID         
                            JOIN SAQTRV (NOLOCK) ON SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID 
                            JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = SAQTRV.QUOTE_RECORD_ID
                                                    AND SAQRIT.SERVICE_RECORD_ID = SAQSCO.SERVICE_RECORD_ID
                                                    AND SAQRIT.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID
                                                    AND SAQRIT.GREENBOOK_RECORD_ID = SAQSCO.GREENBOOK_RECORD_ID
                                                    AND SAQRIT.EQUIPMENT_ID = SAQSCO.EQUIPMENT_ID
                                                    AND SAQRIT.QTESRVCOB_RECORD_ID = SAQSCE.QTESRVCOB_RECORD_ID
                                                    {ancillary_join}
                            LEFT JOIN SAQRIT (NOLOCK) SAQRIT_SELF ON SAQRIT_SELF.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID
                                                    AND SAQRIT_SELF.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID
                                                    AND SAQRIT_SELF.LINE = SAQRIT.PARQTEITM_LINE
                                                    --AND ISNULL(SAQSCO.PAR_SERVICE_ID,'') = ISNULL(SAQRIT_SELF.SERVICE_ID,'')
                        
                            LEFT JOIN PRSPRV (NOLOCK) ON PRSPRV.SERVICE_RECORD_ID = SAQSCO.SERVICE_RECORD_ID		
                            {YearWiseJoinString}			
                        WHERE 
                            SAQSCO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQSCO.SERVICE_ID = '{ServiceId}' AND ISNULL(SAQSCE.CONFIGURATION_STATUS,'') = 'COMPLETE' {ancillary_where}
                        ) IQ                        
                        LEFT JOIN SAQICO (NOLOCK) ON SAQICO.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND SAQICO.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND SAQICO.SERVICE_RECORD_ID = IQ.SERVICE_RECORD_ID AND SAQICO.GREENBOOK_RECORD_ID = IQ.GREENBOOK_RECORD_ID AND ISNULL(SAQICO.FABLOCATION_RECORD_ID,'') = ISNULL(IQ.FABLOCATION_RECORD_ID,'') AND SAQICO.EQUIPMENT_RECORD_ID = IQ.EQUIPMENT_RECORD_ID AND SAQICO.LINE = IQ.LINE AND SAQICO.CNTYER = IQ.CNTYER 
                        WHERE ISNULL(SAQICO.EQUIPMENT_RECORD_ID,'') = ''
                        """.format(UserId=self.user_id, UserName=self.user_name, QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id, ancillary_join = ancillary_join, ancillary_where = ancillary_where, YearWiseJoinString = yearwise_join_str)
                )
            # CR704 - End - M
            #A055S000P01-21072 Start M
            self.update_cntday()
            #A055S000P01-21072 End M
            #CR713 - Start - M
            # #INC08693886 - Start - A
            # Sql.RunQuery("""UPDATE SAQICO
            #                 SET SAQICO.KIT_NUMBER = SAQSAP.KIT_NUMBER
            #                 FROM SAQICO (NOLOCK)
            #                 INNER JOIN SAQSAP (NOLOCK) ON SAQSAP.QUOTE_RECORD_ID = SAQICO.QUOTE_RECORD_ID AND SAQSAP.QTEREV_RECORD_ID = SAQICO.QTEREV_RECORD_ID AND SAQSAP.SERVICE_ID = SAQICO.SERVICE_ID AND SAQSAP.EQUIPMENT_ID = SAQICO.EQUIPMENT_ID 
            #                 WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}'
            #             """.format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
            # #INC08693886 - End - A
            #CR713 - End - M
            if self.service_id == 'Z0091':
                Sql.RunQuery("""UPDATE SAQICO
                        SET SAQICO.PDCBPR = PRLPBE.BASPRC_IN_GLBCUR,
                            SAQICO.PDCCST = PRLPBE.POSCST_IN_GLBCUR
                        FROM SAQICO 
                        INNER JOIN(SELECT PRLPBE.BLUEBOOK,
                                PRLPBE.REGION,
                                MAEQUP.PRODUCT_ID,
                                PRLPBE.GREENBOOK,
                                --PRLPBE.LICENSE,
                                MAEQUP.ENGG_LINK,
                                SAQITE.CONCOV,
                                SAQITE.LINE,
                                PRLPBE.BASPRC_IN_GLBCUR,
                                PRLPBE.POSCST_IN_GLBCUR,
                                SAQSCO.SERVICE_ID,
                                SAQSCO.QTEREV_RECORD_ID,
                                SAQSCO.QUOTE_RECORD_ID
                                FROM PRLPBE 
                            INNER JOIN MAEQUP on MAEQUP.PRODUCT_ID = PRLPBE.PRODUCT_ID AND MAEQUP.GREENBOOK = PRLPBE.GREENBOOK AND MAEQUP.REGION = PRLPBE.REGION
                            INNER JOIN SAQSCO on MAEQUP.EQUIPMENT_ID = SAQSCO.EQUIPMENT_ID 
                            INNER JOIN SAQTRV (NOLOCK) ON SAQSCO.QUOTE_RECORD_ID = SAQTRV.QUOTE_RECORD_ID AND SAQSCO.QTEREV_RECORD_ID = SAQTRV.QTEREV_RECORD_ID AND isnull(SAQTRV.BLUEBOOK,'') = isnull(PRLPBE.BLUEBOOK,'') AND SAQTRV.REGION = PRLPBE.REGION
                            INNER JOIN SAQITE (NOLOCK) ON SAQITE.QUOTE_RECORD_ID = SAQTRV.QUOTE_RECORD_ID AND SAQITE.QTEREV_RECORD_ID = SAQTRV.QTEREV_RECORD_ID AND SAQITE.GREENBOOK = PRLPBE.GREENBOOK AND PRLPBE.CONTRACT_COVERAGE = SAQITE.CONCOV and SAQITE.SERVICE_ID ='Z0091'
                            WHERE SAQTRV.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQTRV.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQSCO.SERVICE_ID = '{ServiceId}' AND PRLPBE.GREENBOOK = 'PDC' ) PRLPBE ON SAQICO.LINE = PRLPBE.LINE AND PRLPBE.QUOTE_RECORD_ID = SAQICO.QUOTE_RECORD_ID AND PRLPBE.QTEREV_RECORD_ID = SAQICO.QTEREV_RECORD_ID AND 
                            PRLPBE.SERVICE_ID = SAQICO.SERVICE_ID
                        WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.SERVICE_ID = 'Z0091' AND SAQICO.GREENBOOK = 'PDC'
                    """.format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
        #A055S000P01-21015 - Start - M
        elif self.quote_service_entitlement_type == "STR-OFFBGBPMCMKTGCPCND OBJ-AS":
            # CR704 - Start - M
            for contract_year_obj in contract_years_obj:
                if contract_year_obj.CNTYER == 'YEAR 1':
                    yearwise_join_str = "JOIN SAQCYR (NOLOCK) ON SAQCYR.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND SAQCYR.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID AND SAQCYR.CONTRACT_START_DATE <= SAQRIT.CONTRACT_VALID_FROM AND SAQCYR.CONTRACT_END_DATE >= SAQRIT.CONTRACT_VALID_FROM"
                else:
                    yearwise_join_str = "JOIN SAQCYR (NOLOCK) ON SAQCYR.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND SAQCYR.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID AND ((SAQCYR.CONTRACT_START_DATE >= SAQRIT.CONTRACT_VALID_FROM AND SAQCYR.CONTRACT_START_DATE <= SAQRIT.CONTRACT_VALID_TO) OR (SAQCYR.CONTRACT_START_DATE <= SAQRIT.CONTRACT_VALID_FROM AND SAQCYR.CONTRACT_END_DATE >= SAQRIT.CONTRACT_VALID_FROM))"            
                #INC08754197 - Start - M
                Sql.RunQuery("""INSERT SAQICO (EQUIPMENT_DESCRIPTION, STATUS, QUANTITY, OBJECT_ID, EQUPID, EQUIPMENT_ID, EQUIPMENT_RECORD_ID, LINE, QUOTE_ID, QTEITM_RECORD_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, KPU, SERNUM, SERIAL_NO, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, TECHNOLOGY, CUSTOMER_TOOL_ID, EQUCAT, EQUIPMENTCATEGORY_ID, EQUIPMENTCATEGORY_RECORD_ID, EQUIPMENT_STATUS, MNT_PLANT_ID, MNT_PLANT_NAME, MNT_PLANT_RECORD_ID, SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID, FABLOC, FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, GRNBOK, GREENBOOK, GREENBOOK_RECORD_ID, GLOBAL_CURRENCY,GLOBAL_CURRENCY_RECORD_ID, OBJECT_TYPE, BLUBOK, WTYSTE, WTYEND, WTYDAY, PLTFRM, SUBSIZ, REGION, ISPOES, CSTSRC, PRCSRC, TAXVTP,TAXGRP,DCCRFX,DCCRXD,DOCCUR, PM_ID,KIT_ID, MNTEVT_LEVEL, PM_RECORD_ID, ASSEMBLY_ID, ASSEMBLY_RECORD_ID, GOT_CODE, PROCES, INTCPV, INTCPC, OSSVDV, LTCOSS, POFVDV, POFVDC, GBKVDV, GBKVDC, UIMVDV, UIMVDC, CAVVDV, CAVVDC, WNDVDV, WNDVDC, CCRTMV, CCRTMC, SCMVDV, SCMVDC, CCDFFV, CCDFFC, NPIVDV, NPIVDC, DTPVDV, DTPVDC, CSTVDV, CSTVDC, CSGVDV, CSGVDC, QRQVDV, QRQVDC, SVCVDV, SVCVDC, RKFVDV, RKFVDC, PBPVDV, PBPVDC, CMLAB_ENT, CNSMBL_ENT, CNTCVG_ENT, NCNSMB_ENT, PMEVNT_ENT, PMLAB_ENT, PRMKPI_ENT, OFRING, QTETYP, BILTYP, BPTTKP, ATGKEY, TGKPNS, NWPTON, HEDBIN, WETCLN_ENT, SPQTEV, SVSPCT, SPSPCT,SWPKTA,NUMLAY,ITTNBV,ITCTAS,ITSDUB,ITSDUT,ITSPCL,ITSPCT,CNTYER,QTESRVCOB_RECORD_ID,TEMP_TOOL, STADTE, CONTRACT_VALID_FROM, ENDDTE, CONTRACT_VALID_TO, CNTDAY, QUOTE_ITEM_COVERED_OBJECT_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified)
                        SELECT DISTINCT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_COVERED_OBJECT_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED,{UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (                        
                        SELECT DISTINCT					
                            SAQGPA.EQUIPMENT_DESCRIPTION,
                            null as STATUS,
                            null as EQUIPMENT_QUANTITY,
                            SAQRIT.OBJECT_ID,
                            SAQGPA.EQUIPMENT_ID as EQUPID,
                            SAQGPA.EQUIPMENT_ID,
                            SAQGPA.EQUIPMENT_RECORD_ID,
                            SAQRIT.LINE,
                            SAQRIT.QUOTE_ID, 
                            SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID, 
                            SAQRIT.QUOTE_RECORD_ID,
                            SAQRIT.QTEREV_ID,
                            SAQRIT.QTEREV_RECORD_ID,
                            SAQSCO.KPU,
                            SAQSCO.SERIAL_NO as SERNUM, 
                            SAQSCO.SERIAL_NO, 
                            SAQRIT.SERVICE_DESCRIPTION, 
                            SAQRIT.SERVICE_ID, 
                            SAQRIT.SERVICE_RECORD_ID,								
                            SAQSCO.TECHNOLOGY,			
                            SAQSCO.CUSTOMER_TOOL_ID, 
                            SAQSCO.EQUIPMENTCATEGORY_ID as EQUCAT, 
                            SAQSCO.EQUIPMENTCATEGORY_ID, 
                            SAQSCO.EQUIPMENTCATEGORY_RECORD_ID, 
                            SAQSCO.EQUIPMENT_STATUS,			
                            SAQRIT.PLANT_ID as MNT_PLANT_ID, 
                            SAQRIT.PLANT_NAME as MNT_PLANT_NAME, 
                            SAQRIT.PLANT_RECORD_ID as MNT_PLANT_RECORD_ID,				
                            SAQTRV.SALESORG_ID, 
                            SAQTRV.SALESORG_NAME, 
                            SAQTRV.SALESORG_RECORD_ID,  
                            SAQRIT.FABLOCATION_ID as FABLOC,
                            SAQRIT.FABLOCATION_ID,
                            SAQRIT.FABLOCATION_NAME,
                            SAQRIT.FABLOCATION_RECORD_ID,
                            SAQRIT.GREENBOOK as GRNBOK, 
                            SAQRIT.GREENBOOK, 
                            SAQRIT.GREENBOOK_RECORD_ID, 			
                            SAQTRV.GLOBAL_CURRENCY,
                            SAQTRV.GLOBAL_CURRENCY_RECORD_ID,					
                            SAQRIT.OBJECT_TYPE,
                            SAQTRV.BLUEBOOK as BLUBOK,
                            null as WTYSTE,
                            null as WTYEND,
                            null as WTYDAY,
                            null as PLTFRM,
                            SAQSCO.WAFER_SIZE as SUBSIZ,
                            SAQTRV.REGION as REGION,
                            SAQTMT.POES as ISPOES,
                            CASE WHEN ISNULL(PRSPRV.SSCM_COST, 0) = 1 THEN 'SSCM' ELSE 'CPQ' END as CSTSRC,
                            CASE WHEN ISNULL(PRSPRV.SSCM_COST, 0) = 1 THEN 'VALUE PRICING-SSCM' ELSE 'OFFLINE PRICING' END as PRCSRC,
                            --'No' as SPQTEV,
                            SAQRIT.TAX_PERCENTAGE as TAXVTP,
                            SAQRIT.TAXCLASSIFICATION_ID,
                            SAQTRV.EXCHANGE_RATE,
                            SAQTRV.EXCHANGE_RATE_DATE,
                            SAQTRV.DOC_CURRENCY,
                            SAQGPA.PM_ID,
                            SAQGPA.KIT_ID,
                            SAQGPA.MNTEVT_LEVEL,
                            SAQGPA.PM_RECORD_ID,
                            null as ASSEMBLY_ID,
                            null as ASSEMBLY_RECORD_ID,
                            SAQGPA.GOT_CODE,
                            --SAQGPA.DEVICE_NODE as EQNODE,
                            SAQGPA.PROCESS_TYPE as PROCES,
                            SAQGPE.INTCPV,
                            SAQGPE.INTCPC,
                            SAQGPE.OSSVDV,
                            SAQGPE.LTCOSS,
                            SAQGPE.POFVDV,
                            SAQGPE.POFVDC,
                            SAQGPE.GREENBOOK as GBKVDV,
                            SAQGPE.GBKVDC,
                            SAQGPE.UIMVDV,
                            SAQGPE.UIMVDC,
                            SAQGPE.CAVVDV,
                            SAQGPE.CAVVDC,
                            SAQGPE.WNDVDV,
                            SAQGPE.WNDVDC,
                            SAQGPE.CCRTMV,
                            SAQGPE.CCRTMC,
                            SAQGPE.SCMVDV,
                            SAQGPE.SCMVDC,
                            SAQGPE.CCDFFV,
                            SAQGPE.CCDFFC,
                            SAQGPE.NPIVDV,
                            SAQGPE.NPIVDC,
                            SAQGPE.DTPVDV,
                            SAQGPE.DTPVDC,
                            SAQGPE.CSTVDV,
                            SAQGPE.CSTVDC,
                            SAQGPE.CSGVDV,
                            SAQGPE.CSGVDC,
                            SAQGPE.QRQVDV,
                            SAQGPE.QRQVDC,
                            SAQGPE.SVCVDV,
                            SAQGPE.SVCVDC,
                            SAQGPE.RKFVDV,
                            SAQGPE.RKFVDC,
                            SAQGPE.PBPVDV,
                            SAQGPE.PBPVDC,
                            SAQGPE.CMLAB_ENT,
                            SAQGPE.CNSMBL_ENT,
                            SAQGPE.CNTCVG_ENT,
                            SAQGPE.NCNSMB_ENT,
                            SAQGPE.PMEVNT_ENT,
                            SAQGPE.PMLAB_ENT,
                            SAQGPE.PRMKPI_ENT,
                            SAQGPE.OFRING,
                            SAQGPE.QTETYP,
                            SAQGPE.BILTYP,
                            SAQGPE.BPTKPI,
                            SAQGPE.ATGKEY,
                            SAQGPE.ATNKEY,                            
                            SAQGPE.NWPTON,
                            SAQGPE.HEDBIN,
                            SAQGPE.WETCLN_ENT,
                            SAQGPE.SPQTEV,
                            SAQGPE.SVSPCT,
                            SAQGPE.SPSPCT,
                            SAQGPE.SWPKTA,
                            SAQGPE.NUMLAY,
                            SAQGPE.ITTNBV,
                            SAQGPA.CHAMBER_QTY AS ITCTAS,
                            SAQGPE.ITSDUB,
                            SAQGPE.ITSDUT,
                            SAQGPE.ITSPCL,
                            SAQGPE.ITSPCT,
                            SAQCYR.CNTYER as CNTYER,
                            SAQGPA.QTESRVCOB_RECORD_ID,
                            SAQSCO.TEMP_TOOL,
                            CASE WHEN SAQRIT.CONTRACT_VALID_FROM > SAQCYR.CONTRACT_START_DATE THEN SAQRIT.CONTRACT_VALID_FROM ELSE SAQCYR.CONTRACT_START_DATE END as STADTE,
                            CASE WHEN SAQRIT.CONTRACT_VALID_FROM > SAQCYR.CONTRACT_START_DATE THEN SAQRIT.CONTRACT_VALID_FROM ELSE SAQCYR.CONTRACT_START_DATE END as CONTRACT_VALID_FROM,
                            CASE WHEN SAQCYR.CONTRACT_END_DATE > SAQRIT.CONTRACT_VALID_TO THEN SAQRIT.CONTRACT_VALID_TO ELSE SAQCYR.CONTRACT_END_DATE END as ENDDTE,
                            CASE WHEN SAQCYR.CONTRACT_END_DATE > SAQRIT.CONTRACT_VALID_TO THEN SAQRIT.CONTRACT_VALID_TO ELSE SAQCYR.CONTRACT_END_DATE END as CONTRACT_VALID_TO,
                            Abs(DATEDIFF(day,CASE WHEN SAQCYR.CONTRACT_END_DATE > SAQRIT.CONTRACT_VALID_TO THEN SAQRIT.CONTRACT_VALID_TO ELSE SAQCYR.CONTRACT_END_DATE END , CASE WHEN SAQRIT.CONTRACT_VALID_FROM > SAQCYR.CONTRACT_START_DATE THEN SAQRIT.CONTRACT_VALID_FROM ELSE SAQCYR.CONTRACT_START_DATE END)) + 1 as CNTDAY                                 
                        FROM 
                            SAQRIT (NOLOCK)		
                            JOIN (
                                SELECT SAQGPA.SERVICE_ID,SAQGPA.GREENBOOK,SAQGPA.FABLOCATION_ID,SAQGPA.GOT_CODE,SAQGPA.PM_ID,SAQGPA.QUOTE_RECORD_ID,SAQGPA.QTEREV_RECORD_ID,SAQGPA.PM_RECORD_ID,KIT_ID, SAQGPA.GOTCODE_RECORD_ID, SAQGPA.MNTEVT_LEVEL,SAQGPA.SERVICE_DESCRIPTION, SAQGPA.SERVICE_RECORD_ID, SAQGPA.FABLOCATION_NAME, SAQGPA.FABLOCATION_RECORD_ID,SAQGPA.GREENBOOK_RECORD_ID, ISNULL(PROCESS_TYPE,'') AS PROCESS_TYPE , ISNULL(DEVICE_NODE,'') AS DEVICE_NODE,SAQGPA.EQUIPMENT_ID, SAQGPA.EQUIPMENT_RECORD_ID,SAQGPA.EQUIPMENT_DESCRIPTION,COUNT(ISNULL(ASSEMBLY_ID,0)) AS CHAMBER_QTY,QTESRVCOB_RECORD_ID
                                    FROM SAQGPA (NOLOCK) 
                                    WHERE SAQGPA.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQGPA.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQGPA.SERVICE_ID = '{ServiceId}' AND SAQGPA.INCLUDED = 1
                                    GROUP BY SAQGPA.SERVICE_ID,SAQGPA.GREENBOOK,SAQGPA.FABLOCATION_ID,SAQGPA.GOT_CODE,SAQGPA.PM_ID,SAQGPA.QUOTE_RECORD_ID,SAQGPA.QTEREV_RECORD_ID,SAQGPA.PM_RECORD_ID,KIT_ID, SAQGPA.GOTCODE_RECORD_ID, SAQGPA.MNTEVT_LEVEL,SAQGPA.SERVICE_DESCRIPTION, SAQGPA.SERVICE_RECORD_ID, SAQGPA.FABLOCATION_NAME, SAQGPA.FABLOCATION_RECORD_ID,SAQGPA.GREENBOOK_RECORD_ID, ISNULL(PROCESS_TYPE,'')  , ISNULL(DEVICE_NODE,''),SAQGPA.EQUIPMENT_ID, SAQGPA.EQUIPMENT_RECORD_ID,SAQGPA.EQUIPMENT_DESCRIPTION,QTESRVCOB_RECORD_ID
                            ) SAQGPA ON SAQGPA.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND SAQGPA.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID AND SAQGPA.SERVICE_ID = SAQRIT.SERVICE_ID AND SAQGPA.GREENBOOK_RECORD_ID = SAQRIT.GREENBOOK_RECORD_ID AND SAQGPA.PM_ID = SAQRIT.OBJECT_ID	AND SAQGPA.GOT_CODE = SAQRIT.GOT_CODE AND SAQGPA.KIT_ID = SAQRIT.KIT_ID AND ISNULL(SAQGPA.PROCESS_TYPE,'') = ISNULL(SAQRIT.PROCESS_TYPE,'') AND ISNULL(SAQGPA.DEVICE_NODE,'') = ISNULL(SAQRIT.DEVICE_NODE,'') AND SAQGPA.FABLOCATION_ID = SAQRIT.FABLOCATION_ID
                            JOIN SAQGPE (NOLOCK) ON SAQGPE.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND SAQGPE.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID AND SAQGPE.SERVICE_ID = SAQRIT.SERVICE_ID AND SAQGPE.PM_ID = SAQGPA.PM_ID AND SAQGPE.GOT_CODE = SAQGPA.GOT_CODE AND SAQGPA.KIT_ID = SAQGPE.KIT_ID
                            JOIN SAQSCO (NOLOCK) ON SAQSCO.QUOTE_RECORD_ID = SAQGPA.QUOTE_RECORD_ID AND SAQSCO.QTEREV_RECORD_ID = SAQGPA.QTEREV_RECORD_ID AND SAQSCO.SERVICE_RECORD_ID = SAQGPA.SERVICE_RECORD_ID AND SAQSCO.GREENBOOK = SAQGPA.GREENBOOK AND SAQSCO.FABLOCATION_RECORD_ID = SAQGPA.FABLOCATION_RECORD_ID AND SAQSCO.EQUIPMENT_ID = SAQGPA.EQUIPMENT_ID AND SAQGPA.QTESRVCOB_RECORD_ID = QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID
                            JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID         
                            JOIN SAQTRV (NOLOCK) ON SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID 						
                            LEFT JOIN PRSPRV (NOLOCK) ON PRSPRV.SERVICE_RECORD_ID = SAQRIT.SERVICE_RECORD_ID	
                            {YearWiseJoinString}				
                        WHERE 
                            SAQRIT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQRIT.SERVICE_ID = '{ServiceId}' AND ISNULL(SAQGPE.CONFIGURATION_STATUS,'') = 'COMPLETE'
                        ) IQ                        
                        LEFT JOIN SAQICO (NOLOCK) ON SAQICO.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND SAQICO.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND SAQICO.SERVICE_RECORD_ID = IQ.SERVICE_RECORD_ID AND SAQICO.GREENBOOK_RECORD_ID = IQ.GREENBOOK_RECORD_ID AND ISNULL(SAQICO.FABLOCATION_RECORD_ID,'') = ISNULL(IQ.FABLOCATION_RECORD_ID,'') AND SAQICO.PM_ID = IQ.PM_ID AND SAQICO.GOT_CODE = IQ.GOT_CODE AND SAQICO.KIT_ID = IQ.KIT_ID AND SAQICO.CNTYER = IQ.CNTYER AND SAQICO.QTESRVCOB_RECORD_ID = IQ.QTESRVCOB_RECORD_ID
                        WHERE ISNULL(SAQICO.PM_ID,'') = ''
                        """.format(UserId=self.user_id, UserName=self.user_name, QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id,YearWiseJoinString = yearwise_join_str)
                )	
            # CR704 - End - M
            #INC08675532 #INC08675479,INC08754197  - END - M
            #A055S000P01-21072 Start M
            self.update_cntday()
            #A055S000P01-21072 End M
            # PMSA - Quantity Update
            #INC08745555 Start - M
            #A055S000P01-20653, A055S000P01-20868 - M
            Sql.RunQuery("""UPDATE SAQICO SET QUANTITY = SAQGPA.QUANTITY,
                ADJ_PM_FREQUENCY = SAQGPA.QUANTITY,
                CTAJPM = CASE WHEN SAQICO.QTETYP IN ('Flex Event Based','Event Based') THEN ROUND((CONVERT(FLOAT, SAQGPA.QUANTITY)*1.0/365) * CNTDAY,5,0) ELSE NULL END,
                SSCM_PM_FREQUENCY =  SAQGPA.SSCM_PM_FREQUENCY,
                AIUPPE = SAQICO.USRPRC / NULLIF(SAQGPA.QUANTITY, 0)
                FROM SAQICO (NOLOCK) 
                JOIN (
                    SELECT SAQGPA.EQUIPMENT_ID,SAQGPA.SERVICE_ID,SAQGPA.GREENBOOK,SAQGPA.FABLOCATION_ID,SAQGPA.GOT_CODE,SAQGPA.PM_ID,KIT_ID,SAQGPA.QUOTE_RECORD_ID,SAQGPA.QTEREV_RECORD_ID, SAQGPA.MNTEVT_LEVEL, ISNULL(PROCESS_TYPE,'') AS PROCESS_TYPE , ISNULL(DEVICE_NODE,'') AS DEVICE_NODE, SUM(ISNULL(SAQGPA.PM_FREQUENCY, 0)) as QUANTITY, SUM(ISNULL(SAQGPA.SSCM_PM_FREQUENCY, 0)) as SSCM_PM_FREQUENCY,QTESRVCOB_RECORD_ID
                        FROM SAQGPA (NOLOCK) 
                        WHERE SAQGPA.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQGPA.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQGPA.SERVICE_ID = '{ServiceId}' AND SAQGPA.INCLUDED = 1
                        GROUP BY SAQGPA.EQUIPMENT_ID,SAQGPA.SERVICE_ID,SAQGPA.GREENBOOK,SAQGPA.FABLOCATION_ID,SAQGPA.GOT_CODE,SAQGPA.PM_ID,KIT_ID,SAQGPA.QUOTE_RECORD_ID,SAQGPA.QTEREV_RECORD_ID, SAQGPA.MNTEVT_LEVEL, ISNULL(PROCESS_TYPE,'')  , ISNULL(DEVICE_NODE,''),QTESRVCOB_RECORD_ID
                ) SAQGPA ON SAQGPA.QUOTE_RECORD_ID = SAQICO.QUOTE_RECORD_ID AND SAQGPA.QTEREV_RECORD_ID = SAQICO.QTEREV_RECORD_ID AND SAQGPA.SERVICE_ID = SAQICO.SERVICE_ID AND SAQGPA.FABLOCATION_ID = SAQICO.FABLOCATION_ID AND SAQGPA.GREENBOOK = SAQICO.GREENBOOK AND SAQGPA.PM_ID = SAQICO.PM_ID AND SAQGPA.KIT_ID = SAQICO.KIT_ID AND SAQGPA.GOT_CODE = SAQICO.GOT_CODE AND SAQGPA.EQUIPMENT_ID = SAQICO.EQUIPMENT_ID AND ISNULL(SAQGPA.PROCESS_TYPE,'')= ISNULL(SAQICO.PROCES,'') AND ISNULL(SAQGPA.DEVICE_NODE,'') = ISNULL(SAQICO.DEVICE_NODE,'') AND SAQICO.QTESRVCOB_RECORD_ID = SAQGPA.QTESRVCOB_RECORD_ID
                WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}'""".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id)
            )
            #INC08745555 End - M
            #A055S000P01-20653, A055S000P01-20868 - M
            ##saqrit quantity update
                                        
            self._quote_item_qty_update()
        elif self.quote_service_entitlement_type in ("STR-OFFBGBSMKTGCPCND OBJ-AS"):				
            # CR704 - Start - M		 
            for contract_year_obj in contract_years_obj:
                if contract_year_obj.CNTYER == 'YEAR 1':
                    yearwise_join_str = "JOIN SAQCYR (NOLOCK) ON SAQCYR.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND SAQCYR.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID AND SAQCYR.CONTRACT_START_DATE <= SAQRIT.CONTRACT_VALID_FROM AND SAQCYR.CONTRACT_END_DATE >= SAQRIT.CONTRACT_VALID_FROM"
                else:
                    yearwise_join_str = "JOIN SAQCYR (NOLOCK) ON SAQCYR.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND SAQCYR.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID AND ((SAQCYR.CONTRACT_START_DATE >= SAQRIT.CONTRACT_VALID_FROM AND SAQCYR.CONTRACT_START_DATE <= SAQRIT.CONTRACT_VALID_TO) OR (SAQCYR.CONTRACT_START_DATE <= SAQRIT.CONTRACT_VALID_FROM AND SAQCYR.CONTRACT_END_DATE >= SAQRIT.CONTRACT_VALID_FROM))"       
                #INC08675532 #INC08675479,INC08754197  - START - M
                Sql.RunQuery("""INSERT SAQICO (EQUIPMENT_DESCRIPTION, STATUS, QUANTITY, OBJECT_ID, EQUPID, EQUIPMENT_ID, EQUIPMENT_RECORD_ID, LINE, QUOTE_ID, QTEITM_RECORD_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, KPU, SERNUM, SERIAL_NO, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, TECHNOLOGY, CUSTOMER_TOOL_ID, EQUCAT, EQUIPMENTCATEGORY_ID, EQUIPMENTCATEGORY_RECORD_ID, EQUIPMENT_STATUS, MNT_PLANT_ID, MNT_PLANT_NAME, MNT_PLANT_RECORD_ID, SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID, FABLOC, FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, GRNBOK, GREENBOOK, GREENBOOK_RECORD_ID, GLOBAL_CURRENCY,GLOBAL_CURRENCY_RECORD_ID, OBJECT_TYPE, BLUBOK, WTYSTE, WTYEND, WTYDAY, PLTFRM, SUBSIZ, REGION, ISPOES, CSTSRC, PRCSRC, TAXVTP,TAXGRP,DCCRFX,DCCRXD,DOCCUR, PM_ID,KIT_ID, MNTEVT_LEVEL, PM_RECORD_ID, ASSEMBLY_ID, ASSEMBLY_RECORD_ID, GOT_CODE, PROCES,ITCTAS, CNTYER,QTESRVCOB_RECORD_ID,TEMP_TOOL, STADTE, CONTRACT_VALID_FROM, ENDDTE, CONTRACT_VALID_TO, CNTDAY, QUOTE_ITEM_COVERED_OBJECT_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified)
                        SELECT DISTINCT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_COVERED_OBJECT_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED,{UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
                        SELECT DISTINCT					
                            SAQGPA.EQUIPMENT_DESCRIPTION,
                            null as STATUS,
                            null as EQUIPMENT_QUANTITY,
                            SAQRIT.OBJECT_ID,
                            SAQGPA.EQUIPMENT_ID as EQUPID,
                            SAQGPA.EQUIPMENT_ID,
                            SAQGPA.EQUIPMENT_RECORD_ID,
                            SAQRIT.LINE,
                            SAQRIT.QUOTE_ID, 
                            SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID, 
                            SAQRIT.QUOTE_RECORD_ID,
                            SAQRIT.QTEREV_ID,
                            SAQRIT.QTEREV_RECORD_ID,
                            SAQSCO.KPU,
                            SAQSCO.SERIAL_NO as SERNUM, 
                            SAQSCO.SERIAL_NO, 
                            SAQRIT.SERVICE_DESCRIPTION, 
                            SAQRIT.SERVICE_ID, 
                            SAQRIT.SERVICE_RECORD_ID,								
                            SAQSCO.TECHNOLOGY,																			
                            SAQSCO.CUSTOMER_TOOL_ID, 
                            SAQSCO.EQUIPMENTCATEGORY_ID as EQUCAT, 
                            SAQSCO.EQUIPMENTCATEGORY_ID, 
                            SAQSCO.EQUIPMENTCATEGORY_RECORD_ID, 
                            SAQSCO.EQUIPMENT_STATUS,				
                            SAQRIT.PLANT_ID as MNT_PLANT_ID, 
                            SAQRIT.PLANT_NAME as MNT_PLANT_NAME, 
                            SAQRIT.PLANT_RECORD_ID as MNT_PLANT_RECORD_ID,				
                            SAQTRV.SALESORG_ID, 
                            SAQTRV.SALESORG_NAME, 
                            SAQTRV.SALESORG_RECORD_ID,  
                            SAQRIT.FABLOCATION_ID as FABLOC,
                            SAQRIT.FABLOCATION_ID,
                            SAQRIT.FABLOCATION_NAME,
                            SAQRIT.FABLOCATION_RECORD_ID,
                            SAQRIT.GREENBOOK as GRNBOK, 
                            SAQRIT.GREENBOOK, 
                            SAQRIT.GREENBOOK_RECORD_ID, 			
                            SAQTRV.GLOBAL_CURRENCY,
                            SAQTRV.GLOBAL_CURRENCY_RECORD_ID,					
                            SAQRIT.OBJECT_TYPE,
                            SAQTRV.BLUEBOOK as BLUBOK,
                            null as WTYSTE,
                            null as WTYEND,
                            null as WTYDAY,
                            null as PLTFRM,
                            SAQSCO.WAFER_SIZE as SUBSIZ,
                            SAQTRV.REGION as REGION,
                            SAQTMT.POES as ISPOES,
                            CASE WHEN ISNULL(PRSPRV.SSCM_COST, 0) = 1 THEN 'SSCM' ELSE 'CPQ' END as CSTSRC,
                            CASE WHEN ISNULL(PRSPRV.SSCM_COST, 0) = 1 THEN 'VALUE PRICING-SSCM' ELSE 'OFFLINE PRICING' END as PRCSRC,
                            --'No' as SPQTEV,
                            SAQRIT.TAX_PERCENTAGE as TAXVTP,
                            SAQRIT.TAXCLASSIFICATION_ID,
                            SAQTRV.EXCHANGE_RATE,
                            SAQTRV.EXCHANGE_RATE_DATE,
                            SAQTRV.DOC_CURRENCY,
                            SAQRIT.PM_ID,
                            SAQRIT.KIT_ID,
                            SAQRIT.MNTEVT_LEVEL,
                            SAQRIT.PM_RECORD_ID,
                            null as ASSEMBLY_ID,
                            null as ASSEMBLY_RECORD_ID,
                            SAQGPA.GOT_CODE,
                            --SAQGPA.DEVICE_NODE as EQNODE,
                            SAQGPA.PROCESS_TYPE as PROCES,
                            SAQGPA.CHAMBER_QTY AS ITCTAS,
                            SAQCYR.CNTYER as CNTYER,
                            SAQGPA.QTESRVCOB_RECORD_ID,
                            SAQSCO.TEMP_TOOL,
                            CASE WHEN SAQRIT.CONTRACT_VALID_FROM > SAQCYR.CONTRACT_START_DATE THEN SAQRIT.CONTRACT_VALID_FROM ELSE SAQCYR.CONTRACT_START_DATE END as STADTE,
                            CASE WHEN SAQRIT.CONTRACT_VALID_FROM > SAQCYR.CONTRACT_START_DATE THEN SAQRIT.CONTRACT_VALID_FROM ELSE SAQCYR.CONTRACT_START_DATE END as CONTRACT_VALID_FROM,
                            CASE WHEN SAQCYR.CONTRACT_END_DATE > SAQRIT.CONTRACT_VALID_TO THEN SAQRIT.CONTRACT_VALID_TO ELSE SAQCYR.CONTRACT_END_DATE END as ENDDTE,
                            CASE WHEN SAQCYR.CONTRACT_END_DATE > SAQRIT.CONTRACT_VALID_TO THEN SAQRIT.CONTRACT_VALID_TO ELSE SAQCYR.CONTRACT_END_DATE END as CONTRACT_VALID_TO,
                            Abs(DATEDIFF(day,CASE WHEN SAQCYR.CONTRACT_END_DATE > SAQRIT.CONTRACT_VALID_TO THEN SAQRIT.CONTRACT_VALID_TO ELSE SAQCYR.CONTRACT_END_DATE END , CASE WHEN SAQRIT.CONTRACT_VALID_FROM > SAQCYR.CONTRACT_START_DATE THEN SAQRIT.CONTRACT_VALID_FROM ELSE SAQCYR.CONTRACT_START_DATE END)) + 1 as CNTDAY	
                        FROM 
                            SAQRIT (NOLOCK)		
                            JOIN (
                                SELECT SAQGPA.SERVICE_ID,SAQGPA.GREENBOOK,SAQGPA.FABLOCATION_ID,SAQGPA.GOT_CODE,SAQGPA.PM_ID,SAQGPA.KIT_ID,SAQGPA.QUOTE_RECORD_ID,SAQGPA.QTEREV_RECORD_ID,SAQGPA.PM_RECORD_ID, SAQGPA.GOTCODE_RECORD_ID,SAQGPA.SERVICE_DESCRIPTION, SAQGPA.SERVICE_RECORD_ID, SAQGPA.FABLOCATION_NAME, SAQGPA.FABLOCATION_RECORD_ID,SAQGPA.GREENBOOK_RECORD_ID, ISNULL(SAQGPA.PROCESS_TYPE,'') AS PROCESS_TYPE , ISNULL(SAQGPA.DEVICE_NODE,'') AS DEVICE_NODE,CONFIGURATION_STATUS,SAQGPA.EQUIPMENT_ID, SAQGPA.EQUIPMENT_RECORD_ID,SAQGPA.EQUIPMENT_DESCRIPTION,COUNT(ISNULL(ASSEMBLY_ID,0)) AS CHAMBER_QTY,QTESRVCOB_RECORD_ID
                                        FROM SAQGPA (NOLOCK) 
                                        JOIN SAQGPE (NOLOCK) ON SAQGPE.QUOTE_RECORD_ID = SAQGPA.QUOTE_RECORD_ID AND SAQGPE.QTEREV_RECORD_ID = SAQGPA.QTEREV_RECORD_ID AND SAQGPE.SERVICE_ID = SAQGPA.SERVICE_ID AND SAQGPE.PM_ID = SAQGPA.PM_ID AND SAQGPE.GOT_CODE = SAQGPA.GOT_CODE AND SAQGPE.KIT_ID = SAQGPA.KIT_ID
                                        WHERE SAQGPA.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQGPA.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQGPA.SERVICE_ID = '{ServiceId}' AND MNTEVT_LEVEL != 'Scheduled Maintenance' AND SAQGPA.INCLUDED = 1                                        
                                        GROUP BY SAQGPA.SERVICE_ID,SAQGPA.GREENBOOK,SAQGPA.FABLOCATION_ID,SAQGPA.GOT_CODE,SAQGPA.PM_ID,SAQGPA.KIT_ID,SAQGPA.QUOTE_RECORD_ID,SAQGPA.QTEREV_RECORD_ID,SAQGPA.PM_RECORD_ID, SAQGPA.GOTCODE_RECORD_ID,SAQGPA.SERVICE_DESCRIPTION, SAQGPA.SERVICE_RECORD_ID, SAQGPA.FABLOCATION_NAME, SAQGPA.FABLOCATION_RECORD_ID,SAQGPA.GREENBOOK_RECORD_ID, ISNULL(SAQGPA.PROCESS_TYPE,'')  , ISNULL(SAQGPA.DEVICE_NODE,''),CONFIGURATION_STATUS,SAQGPA.EQUIPMENT_ID, SAQGPA.EQUIPMENT_RECORD_ID,SAQGPA.EQUIPMENT_DESCRIPTION,QTESRVCOB_RECORD_ID
                                UNION
                                SELECT SAQGPA.SERVICE_ID,SAQGPA.GREENBOOK,SAQGPA.FABLOCATION_ID,SAQGPA.GOT_CODE,SAQGPA.MNTEVT_LEVEL,SAQGPA.KIT_ID,SAQGPA.QUOTE_RECORD_ID,SAQGPA.QTEREV_RECORD_ID,null as PM_RECORD_ID, SAQGPA.GOTCODE_RECORD_ID,SAQGPA.SERVICE_DESCRIPTION, SAQGPA.SERVICE_RECORD_ID, SAQGPA.FABLOCATION_NAME, SAQGPA.FABLOCATION_RECORD_ID,SAQGPA.GREENBOOK_RECORD_ID, ISNULL(SAQGPA.PROCESS_TYPE,'') AS PROCESS_TYPE , ISNULL(SAQGPA.DEVICE_NODE,'') AS DEVICE_NODE,CONFIGURATION_STATUS,SAQGPA.EQUIPMENT_ID, SAQGPA.EQUIPMENT_RECORD_ID,SAQGPA.EQUIPMENT_DESCRIPTION,COUNT(ISNULL(ASSEMBLY_ID,0)) AS CHAMBER_QTY,QTESRVCOB_RECORD_ID
                                    FROM SAQGPA (NOLOCK) 
                                    JOIN SAQSGE SAQGPE (NOLOCK) ON SAQGPE.QUOTE_RECORD_ID = SAQGPA.QUOTE_RECORD_ID AND SAQGPE.QTEREV_RECORD_ID = SAQGPA.QTEREV_RECORD_ID AND SAQGPE.GREENBOOK = SAQGPA.GREENBOOK  AND SAQGPA.SERVICE_ID = SAQGPE.SERVICE_ID
                                    WHERE SAQGPA.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQGPA.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQGPA.SERVICE_ID = '{ServiceId}' AND MNTEVT_LEVEL = 'Scheduled Maintenance' AND SAQGPA.INCLUDED = 1
                                    GROUP BY SAQGPA.SERVICE_ID,SAQGPA.GREENBOOK,SAQGPA.FABLOCATION_ID,SAQGPA.GOT_CODE,SAQGPA.MNTEVT_LEVEL,SAQGPA.KIT_ID,SAQGPA.QUOTE_RECORD_ID,SAQGPA.QTEREV_RECORD_ID, SAQGPA.GOTCODE_RECORD_ID,SAQGPA.SERVICE_DESCRIPTION, SAQGPA.SERVICE_RECORD_ID, SAQGPA.FABLOCATION_NAME, SAQGPA.FABLOCATION_RECORD_ID,SAQGPA.GREENBOOK_RECORD_ID, ISNULL(SAQGPA.PROCESS_TYPE,'')  , ISNULL(SAQGPA.DEVICE_NODE,''),CONFIGURATION_STATUS,SAQGPA.EQUIPMENT_ID, SAQGPA.EQUIPMENT_RECORD_ID,SAQGPA.EQUIPMENT_DESCRIPTION,QTESRVCOB_RECORD_ID
                            ) SAQGPA ON SAQGPA.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND SAQGPA.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID AND SAQGPA.SERVICE_ID = SAQRIT.SERVICE_ID AND SAQGPA.GREENBOOK_RECORD_ID = SAQRIT.GREENBOOK_RECORD_ID AND SAQGPA.PM_ID = SAQRIT.OBJECT_ID	AND SAQGPA.GOT_CODE = SAQRIT.GOT_CODE AND SAQGPA.KIT_ID = SAQRIT.KIT_ID AND ISNULL(SAQGPA.PROCESS_TYPE,'') = ISNULL(SAQRIT.PROCESS_TYPE,'') AND ISNULL(SAQGPA.DEVICE_NODE,'') = ISNULL(SAQRIT.DEVICE_NODE,'') AND SAQGPA.FABLOCATION_ID = SAQRIT.FABLOCATION_ID
                            JOIN SAQSCO (NOLOCK) ON SAQSCO.QUOTE_RECORD_ID = SAQGPA.QUOTE_RECORD_ID AND SAQSCO.QTEREV_RECORD_ID = SAQGPA.QTEREV_RECORD_ID AND SAQSCO.SERVICE_RECORD_ID = SAQGPA.SERVICE_RECORD_ID AND SAQSCO.GREENBOOK = SAQGPA.GREENBOOK AND SAQSCO.FABLOCATION_RECORD_ID = SAQGPA.FABLOCATION_RECORD_ID AND SAQSCO.EQUIPMENT_ID = SAQGPA.EQUIPMENT_ID AND SAQGPA.QTESRVCOB_RECORD_ID = QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID
                            JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID         
                            JOIN SAQTRV (NOLOCK) ON SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID 						
                            LEFT JOIN PRSPRV (NOLOCK) ON PRSPRV.SERVICE_RECORD_ID = SAQRIT.SERVICE_RECORD_ID		
                            {YearWiseJoinString}			
                        WHERE 
                            SAQRIT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQRIT.SERVICE_ID = '{ServiceId}' AND ISNULL(SAQGPA.CONFIGURATION_STATUS,'') = 'COMPLETE'
                        ) IQ
                        LEFT JOIN SAQICO (NOLOCK) ON SAQICO.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND SAQICO.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND SAQICO.SERVICE_RECORD_ID = IQ.SERVICE_RECORD_ID AND SAQICO.GREENBOOK_RECORD_ID = IQ.GREENBOOK_RECORD_ID AND ISNULL(SAQICO.FABLOCATION_RECORD_ID,'') = ISNULL(IQ.FABLOCATION_RECORD_ID,'') AND SAQICO.PM_ID = IQ.PM_ID AND SAQICO.KIT_ID = IQ.KIT_ID AND SAQICO.GOT_CODE = IQ.GOT_CODE AND ISNULL(IQ.OBJECT_ID,'') = ISNULL(SAQICO.OBJECT_ID,'') AND SAQICO.CNTYER = IQ.CNTYER AND SAQICO.QTESRVCOB_RECORD_ID = IQ.QTESRVCOB_RECORD_ID
                        WHERE ISNULL(SAQICO.OBJECT_ID,'') = ''
                        """.format(UserId=self.user_id, UserName=self.user_name, QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id,YearWiseJoinString = yearwise_join_str)
                )	
            # CR704 - End - M	
            #INC08675532 #INC08675479,INC08754197  - END - M
            #A055S000P01-21072 Start M
            self.update_cntday()
            #A055S000P01-21072 End M
            # PMSA - Quantity Update
            #update for value drivers fields
            # ##for non Scheduled Maintenance pm level
            Sql.RunQuery("""UPDATE SAQICO SET INTCPV = SAQGPE.INTCPV , INTCPC= SAQGPE.INTCPC , OSSVDV= SAQGPE.OSSVDV , LTCOSS= SAQGPE.LTCOSS , POFVDV= SAQGPE.POFVDV , POFVDC= SAQGPE.POFVDC , GBKVDV= SAQGPE.GREENBOOK , GBKVDC= SAQGPE.GBKVDC , UIMVDV= SAQGPE.UIMVDV , UIMVDC= SAQGPE.UIMVDC , CAVVDV= SAQGPE.CAVVDV , CAVVDC= SAQGPE.CAVVDC , WNDVDV= SAQGPE.WNDVDV , WNDVDC= SAQGPE.WNDVDC , CCRTMV= SAQGPE.CCRTMV , CCRTMC= SAQGPE.CCRTMC , SCMVDV= SAQGPE.SCMVDV , SCMVDC= SAQGPE.SCMVDC , CCDFFV= SAQGPE.CCDFFV , CCDFFC= SAQGPE.CCDFFC , NPIVDV= SAQGPE.NPIVDV , NPIVDC= SAQGPE.NPIVDC, DTPVDV= SAQGPE.DTPVDV , DTPVDC= SAQGPE.DTPVDC , CSTVDV= SAQGPE.CSTVDV , CSTVDC= SAQGPE.CSTVDC , CSGVDV= SAQGPE.CSGVDV , CSGVDC= SAQGPE.CSGVDC , QRQVDV= SAQGPE.QRQVDV , QRQVDC= SAQGPE.QRQVDC , SVCVDV= SAQGPE.SVCVDV , SVCVDC= SAQGPE.SVCVDC , RKFVDV= SAQGPE.RKFVDV , RKFVDC= SAQGPE.RKFVDC , PBPVDV= SAQGPE.PBPVDV , PBPVDC= SAQGPE.PBPVDC , CMLAB_ENT= SAQGPE.CMLAB_ENT , CNSMBL_ENT= SAQGPE.CNSMBL_ENT , CNTCVG_ENT= SAQGPE.CNTCVG_ENT , NCNSMB_ENT= SAQGPE.NCNSMB_ENT , PMEVNT_ENT= SAQGPE.PMEVNT_ENT , PMLAB_ENT= SAQGPE.PMLAB_ENT , PRMKPI_ENT= SAQGPE.PRMKPI_ENT , OFRING= SAQGPE.OFRING , QTETYP= SAQGPE.QTETYP , BILTYP= SAQGPE.BILTYP , BPTTKP= SAQGPE.BPTKPI , ATGKEY= SAQGPE.ATGKEY , TGKPNS= SAQGPE.ATNKEY , HEDBIN = SAQGPE.HEDBIN, WETCLN_ENT = SAQGPE.WETCLN_ENT, SPQTEV = SAQGPE.SPQTEV, SVSPCT = SAQGPE.SVSPCT, SPSPCT = SAQGPE.SPSPCT, SWPKTA = SAQGPE.SWPKTA, NUMLAY = SAQGPE.NUMLAY, ITTNBV= SAQGPE.ITTNBV,ITSDUB = SAQGPE.ITSDUB, ITSDUT = SAQGPE.ITSDUT, ITSPCL = SAQGPE.ITSPCL, ITSPCT = SAQGPE.ITSPCT
            FROM SAQICO (NOLOCK) INNER JOIN SAQGPA (NOLOCK) ON SAQGPA.QUOTE_RECORD_ID = SAQICO.QUOTE_RECORD_ID AND SAQGPA.QTEREV_RECORD_ID = SAQICO.QTEREV_RECORD_ID AND SAQGPA.SERVICE_ID = SAQICO.SERVICE_ID AND SAQGPA.PM_ID = SAQICO.PM_ID AND SAQGPA.KIT_ID = SAQICO.KIT_ID AND SAQGPA.GOT_CODE = SAQICO.GOT_CODE INNER JOIN SAQGPE (NOLOCK) ON SAQGPE.QUOTE_RECORD_ID = SAQICO.QUOTE_RECORD_ID AND SAQGPE.QTEREV_RECORD_ID = SAQICO.QTEREV_RECORD_ID AND SAQGPE.SERVICE_ID = SAQICO.SERVICE_ID AND SAQGPE.PM_ID = SAQICO.PM_ID AND SAQGPE.KIT_ID = SAQICO.KIT_ID AND SAQGPE.GOT_CODE = SAQICO.GOT_CODE  AND SAQICO.MNTEVT_LEVEL != 'Scheduled Maintenance' WHERE 
                        SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}' AND ISNULL(SAQGPE.CONFIGURATION_STATUS,'') = 'COMPLETE' AND SAQICO.MNTEVT_LEVEL != 'Scheduled Maintenance'""".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id) )
            ##for Scheduled Maintenance pm level
            Sql.RunQuery("""UPDATE SAQICO SET INTCPV = SAQSGE.INTCPV , INTCPC= SAQSGE.INTCPC , OSSVDV= SAQSGE.OSSVDV , LTCOSS= SAQSGE.LTCOSS , POFVDV= SAQSGE.POFVDV , POFVDC= SAQSGE.POFVDC , GBKVDV= SAQSGE.GREENBOOK , GBKVDC= SAQSGE.GBKVDC , UIMVDV= SAQSGE.UIMVDV , UIMVDC= SAQSGE.UIMVDC , CAVVDV= SAQSGE.CAVVDV , CAVVDC= SAQSGE.CAVVDC , WNDVDV= SAQSGE.WNDVDV , WNDVDC= SAQSGE.WNDVDC , CCRTMV= SAQSGE.CCRTMV , CCRTMC= SAQSGE.CCRTMC , SCMVDV= SAQSGE.SCMVDV , SCMVDC= SAQSGE.SCMVDC , CCDFFV= SAQSGE.CCDFFV , CCDFFC= SAQSGE.CCDFFC , NPIVDV= SAQSGE.NPIVDV , NPIVDC= SAQSGE.NPIVDC, DTPVDV= SAQSGE.DTPVDV , DTPVDC= SAQSGE.DTPVDC , CSTVDV= SAQSGE.CSTVDV , CSTVDC= SAQSGE.CSTVDC , CSGVDV= SAQSGE.CSGVDV , CSGVDC= SAQSGE.CSGVDC , QRQVDV= SAQSGE.QRQVDV , QRQVDC= SAQSGE.QRQVDC , SVCVDV= SAQSGE.SVCVDV , SVCVDC= SAQSGE.SVCVDC , RKFVDV= SAQSGE.RKFVDV , RKFVDC= SAQSGE.RKFVDC , PBPVDV= SAQSGE.PBPVDV , PBPVDC= SAQSGE.PBPVDC , CMLAB_ENT= SAQSGE.CMLAB_ENT , CNSMBL_ENT= SAQSGE.CNSMBL_ENT , CNTCVG_ENT= SAQSGE.CNTCVG_ENT , NCNSMB_ENT= SAQSGE.NCNSMB_ENT , PMEVNT_ENT= SAQSGE.PMEVNT_ENT , PMLAB_ENT= SAQSGE.PMLAB_ENT , PRMKPI_ENT= SAQSGE.PRMKPI_ENT , OFRING= SAQSGE.OFRING , QTETYP= SAQSGE.QTETYP , BILTYP= SAQSGE.BILTYP , BPTTKP= SAQSGE.BPTKPI , ATGKEY= SAQSGE.ATGKEY , TGKPNS= SAQSGE.ATNKEY ,HEDBIN = SAQSGE.HEDBIN, WETCLN_ENT = SAQSGE.WETCLN_ENT, SPQTEV = SAQSGE.SPQTEV, SVSPCT = SAQSGE.SVSPCT, SPSPCT = SAQSGE.SPSPCT, SWPKTA = SAQSGE.SWPKTA, NUMLAY = SAQSGE.NUMLAY, ITTNBV = SAQSGE.ITTNBV,ITSDUB = SAQSGE.ITSDUB, ITSDUT = SAQSGE.ITSDUT, ITSPCL = SAQSGE.ITSPCL, ITSPCT = SAQSGE.ITSPCT
            FROM SAQICO (NOLOCK) INNER JOIN SAQSGE (NOLOCK) ON SAQSGE.QUOTE_RECORD_ID = SAQICO.QUOTE_RECORD_ID AND SAQSGE.QTEREV_RECORD_ID = SAQICO.QTEREV_RECORD_ID AND SAQSGE.SERVICE_ID = SAQICO.SERVICE_ID AND SAQSGE.GREENBOOK = SAQICO.GREENBOOK AND SAQICO.MNTEVT_LEVEL = 'Scheduled Maintenance' WHERE 
                        SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}' AND ISNULL(SAQSGE.CONFIGURATION_STATUS,'') = 'COMPLETE' AND SAQICO.MNTEVT_LEVEL = 'Scheduled Maintenance'""".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id) )
            #INC08745555,A055S000P01-20653,A055S000P01-20868,INC09124996,INC09128949 -S
            Sql.RunQuery("""UPDATE SAQICO SET QUANTITY = SAQGPA.QUANTITY,
                ADJ_PM_FREQUENCY = SAQGPA.QUANTITY,
                CTAJPM = CASE WHEN SAQICO.QTETYP IN ('Flex Event Based','Event Based') THEN ROUND((CONVERT(FLOAT, SAQGPA.QUANTITY)*1.0/365) * CNTDAY,5,0) ELSE NULL END,
                SSCM_PM_FREQUENCY =  SAQGPA.SSCM_PM_FREQUENCY,
                AIUPPE = SAQICO.USRPRC / NULLIF(SAQGPA.QUANTITY, 0)
                FROM SAQICO (NOLOCK)
                JOIN (
                    SELECT SAQGPA.EQUIPMENT_ID,SAQGPA.SERVICE_ID,SAQGPA.GREENBOOK,SAQGPA.FABLOCATION_ID,SAQGPA.GOT_CODE,SAQGPA.PM_ID,KIT_ID,SAQGPA.QUOTE_RECORD_ID,SAQGPA.QTEREV_RECORD_ID, SAQGPA.MNTEVT_LEVEL, ISNULL(PROCESS_TYPE,'') AS PROCESS_TYPE , ISNULL(DEVICE_NODE,'') AS DEVICE_NODE, SUM(ISNULL(SAQGPA.PM_FREQUENCY, 0)) as QUANTITY, SUM(ISNULL(SAQGPA.SSCM_PM_FREQUENCY, 0)) as SSCM_PM_FREQUENCY,QTESRVCOB_RECORD_ID
                        FROM SAQGPA (NOLOCK)
                        WHERE SAQGPA.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQGPA.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQGPA.SERVICE_ID = '{ServiceId}' AND MNTEVT_LEVEL != 'Scheduled Maintenance' AND SAQGPA.INCLUDED = 1
                        GROUP BY SAQGPA.SERVICE_ID,SAQGPA.GREENBOOK,SAQGPA.FABLOCATION_ID,SAQGPA.GOT_CODE,SAQGPA.PM_ID,KIT_ID,SAQGPA.QUOTE_RECORD_ID,SAQGPA.QTEREV_RECORD_ID,SAQGPA.PM_RECORD_ID,SAQGPA.EQUIPMENT_ID,SAQGPA.GOTCODE_RECORD_ID, SAQGPA.MNTEVT_LEVEL,SAQGPA.SERVICE_DESCRIPTION, SAQGPA.SERVICE_RECORD_ID, SAQGPA.FABLOCATION_NAME, SAQGPA.FABLOCATION_RECORD_ID,SAQGPA.GREENBOOK_RECORD_ID, ISNULL(PROCESS_TYPE,'')  , ISNULL(DEVICE_NODE,''),QTESRVCOB_RECORD_ID
                    ) SAQGPA ON SAQGPA.QUOTE_RECORD_ID = SAQICO.QUOTE_RECORD_ID AND SAQGPA.QTEREV_RECORD_ID = SAQICO.QTEREV_RECORD_ID AND SAQGPA.SERVICE_ID = SAQICO.SERVICE_ID AND SAQGPA.FABLOCATION_ID = SAQICO.FABLOCATION_ID AND SAQGPA.GREENBOOK = SAQICO.GREENBOOK AND SAQICO.OBJECT_ID = SAQGPA.PM_ID AND SAQGPA.GOT_CODE = SAQICO.GOT_CODE AND SAQGPA.KIT_ID = SAQICO.KIT_ID AND SAQGPA.EQUIPMENT_ID = SAQICO.EQUIPMENT_ID AND ISNULL(SAQGPA.PROCESS_TYPE,'')= ISNULL(SAQICO.PROCES,'') AND ISNULL(SAQGPA.DEVICE_NODE,'') = ISNULL(SAQICO.DEVICE_NODE,'')  AND SAQICO.QTESRVCOB_RECORD_ID = SAQGPA.QTESRVCOB_RECORD_ID
                WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}'""".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id)
            )
            Sql.RunQuery("""UPDATE SAQICO SET QUANTITY = SAQGPA.QUANTITY,
                ADJ_PM_FREQUENCY = SAQGPA.QUANTITY,
                CTAJPM = CASE WHEN SAQICO.QTETYP IN ('Flex Event Based','Event Based') THEN ROUND((CONVERT(FLOAT, SAQGPA.QUANTITY)*1.0/365) * CNTDAY,5,0) ELSE NULL END,
                SSCM_PM_FREQUENCY =  SAQGPA.SSCM_PM_FREQUENCY,
                AIUPPE = SAQICO.USRPRC / NULLIF(SAQGPA.QUANTITY, 0)
                FROM SAQICO (NOLOCK)
                JOIN (
                    SELECT SAQGPA.EQUIPMENT_ID,SAQGPA.SERVICE_ID,SAQGPA.GREENBOOK,SAQGPA.FABLOCATION_ID,SAQGPA.GOT_CODE,NULL AS PM_ID,SAQGPA.QUOTE_RECORD_ID,SAQGPA.QTEREV_RECORD_ID,KIT_ID, SAQGPA.MNTEVT_LEVEL, ISNULL(PROCESS_TYPE,'') AS PROCESS_TYPE , ISNULL(DEVICE_NODE,'') AS DEVICE_NODE, SUM(ISNULL(SAQGPA.PM_FREQUENCY, 0)) as QUANTITY, SUM(ISNULL(SAQGPA.SSCM_PM_FREQUENCY, 0)) as SSCM_PM_FREQUENCY,QTESRVCOB_RECORD_ID
                        FROM SAQGPA (NOLOCK)
                        WHERE SAQGPA.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQGPA.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQGPA.SERVICE_ID = '{ServiceId}' AND MNTEVT_LEVEL = 'Scheduled Maintenance'  AND SAQGPA.INCLUDED = 1
                        GROUP BY SAQGPA.EQUIPMENT_ID,KIT_ID,SAQGPA.SERVICE_ID,SAQGPA.GREENBOOK,SAQGPA.FABLOCATION_ID,SAQGPA.GOT_CODE,SAQGPA.QUOTE_RECORD_ID,SAQGPA.QTEREV_RECORD_ID, SAQGPA.MNTEVT_LEVEL, ISNULL(PROCESS_TYPE,'')  , ISNULL(DEVICE_NODE,''),QTESRVCOB_RECORD_ID
                ) SAQGPA ON SAQGPA.QUOTE_RECORD_ID = SAQICO.QUOTE_RECORD_ID AND SAQGPA.QTEREV_RECORD_ID = SAQICO.QTEREV_RECORD_ID AND SAQGPA.SERVICE_ID = SAQICO.SERVICE_ID AND SAQGPA.FABLOCATION_ID = SAQICO.FABLOCATION_ID AND SAQGPA.GREENBOOK = SAQICO.GREENBOOK AND SAQICO.OBJECT_ID = SAQGPA.MNTEVT_LEVEL AND SAQGPA.GOT_CODE = SAQICO.GOT_CODE AND SAQGPA.KIT_ID = SAQICO.KIT_ID AND SAQGPA.EQUIPMENT_ID = SAQICO.EQUIPMENT_ID AND ISNULL(SAQGPA.PROCESS_TYPE,'')= ISNULL(SAQICO.PROCES,'') AND ISNULL(SAQGPA.DEVICE_NODE,'') = ISNULL(SAQICO.DEVICE_NODE,'')  AND SAQICO.QTESRVCOB_RECORD_ID = SAQGPA.QTESRVCOB_RECORD_ID
                WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}'""".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id)
            )
            #INC08745555,A055S000P01-20653,A055S000P01-20868,INC09124996,INC09128949 -E
            ##saqrit quantity update
            self._quote_item_qty_update()
        elif self.quote_service_entitlement_type in ("STR-OFFBGBKTGCPCND OBJ-GPAS"):
            # CR704 - Start - M
            for contract_year_obj in contract_years_obj:
                if contract_year_obj.CNTYER == 'YEAR 1':
                    yearwise_join_str = "JOIN SAQCYR (NOLOCK) ON SAQCYR.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND SAQCYR.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID AND SAQCYR.CONTRACT_START_DATE <= SAQRIT.CONTRACT_VALID_FROM AND SAQCYR.CONTRACT_END_DATE >= SAQRIT.CONTRACT_VALID_FROM"
                else:
                    yearwise_join_str = "JOIN SAQCYR (NOLOCK) ON SAQCYR.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND SAQCYR.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID AND ((SAQCYR.CONTRACT_START_DATE >= SAQRIT.CONTRACT_VALID_FROM AND SAQCYR.CONTRACT_START_DATE <= SAQRIT.CONTRACT_VALID_TO) OR (SAQCYR.CONTRACT_START_DATE <= SAQRIT.CONTRACT_VALID_FROM AND SAQCYR.CONTRACT_END_DATE >= SAQRIT.CONTRACT_VALID_FROM))"
                ##changed the below query for HPQC DEFECT 545...
                #INC08675532 #INC08675479 - START - M
                Sql.RunQuery("""INSERT SAQICO (EQUIPMENT_DESCRIPTION, STATUS, QUANTITY, OBJECT_ID, EQUPID, EQUIPMENT_ID, EQUIPMENT_RECORD_ID, LINE, QUOTE_ID, QTEITM_RECORD_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, KPU, SERNUM, SERIAL_NO, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, TECHNOLOGY, CUSTOMER_TOOL_ID, EQUCAT, EQUIPMENTCATEGORY_ID, EQUIPMENTCATEGORY_RECORD_ID, EQUIPMENT_STATUS, MNT_PLANT_ID, MNT_PLANT_NAME, MNT_PLANT_RECORD_ID, SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID, FABLOC, FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, GRNBOK, GREENBOOK, GREENBOOK_RECORD_ID, GLOBAL_CURRENCY,GLOBAL_CURRENCY_RECORD_ID, OBJECT_TYPE, BLUBOK, WTYSTE, WTYEND, WTYDAY, PLTFRM, SUBSIZ, REGION, ISPOES, CSTSRC, PRCSRC, TAXVTP,TAXGRP,DCCRFX,DCCRXD,DOCCUR, PM_ID, MNTEVT_LEVEL, PM_RECORD_ID, ASSEMBLY_ID, ASSEMBLY_RECORD_ID, GOT_CODE, PROCES, KIT_ID, INTCPV, INTCPC, OSSVDV, LTCOSS, POFVDV, POFVDC, GBKVDV, GBKVDC, UIMVDV, UIMVDC, CAVVDV, CAVVDC, WNDVDV, WNDVDC, CCRTMV, CCRTMC, SCMVDV, SCMVDC, CCDFFV, CCDFFC, NPIVDV, NPIVDC, DTPVDV, DTPVDC, CSTVDV, CSTVDC, CSGVDV, CSGVDC, QRQVDV, QRQVDC, SVCVDV, SVCVDC, RKFVDV, RKFVDC, PBPVDV, PBPVDC, CMLAB_ENT, CNSMBL_ENT, CNTCVG_ENT, NCNSMB_ENT, PMEVNT_ENT, PMLAB_ENT, PRMKPI_ENT, OFRING, QTETYP, BILTYP, BPTTKP, ATGKEY, TGKPNS, NWPTON, HEDBIN, WETCLN_ENT, SPQTEV, SVSPCT, SPSPCT, SWPKTA,NUMLAY,ITTNBV,ITCTAS,ITSDUB,ITSDUT,ITSPCL,ITSPCT,CNTYER,QTESRVCOB_RECORD_ID,TEMP_TOOL, STADTE, CONTRACT_VALID_FROM, ENDDTE, CONTRACT_VALID_TO, CNTDAY, QUOTE_ITEM_COVERED_OBJECT_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified)
                        SELECT DISTINCT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_COVERED_OBJECT_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED,{UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
                        SELECT DISTINCT					
                            SAQGPA.EQUIPMENT_DESCRIPTION,
                            null as STATUS,
                            null as EQUIPMENT_QUANTITY,
                            SAQRIT.OBJECT_ID,
                            SAQGPA.EQUIPMENT_ID as EQUPID,
                            SAQGPA.EQUIPMENT_ID,
                            SAQGPA.EQUIPMENT_RECORD_ID,
                            SAQRIT.LINE,
                            SAQRIT.QUOTE_ID, 
                            SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID, 
                            SAQRIT.QUOTE_RECORD_ID,
                            SAQRIT.QTEREV_ID,
                            SAQRIT.QTEREV_RECORD_ID,
                            SAQSCO.KPU,
                            SAQSCO.SERIAL_NO as SERNUM, 
                            SAQSCO.SERIAL_NO, 
                            SAQRIT.SERVICE_DESCRIPTION, 
                            SAQRIT.SERVICE_ID, 
                            SAQRIT.SERVICE_RECORD_ID,								
                            SAQSCO.TECHNOLOGY,																			
                            SAQSCO.CUSTOMER_TOOL_ID, 
                            SAQSCO.EQUIPMENTCATEGORY_ID as EQUCAT, 
                            SAQSCO.EQUIPMENTCATEGORY_ID, 
                            SAQSCO.EQUIPMENTCATEGORY_RECORD_ID, 
                            SAQSCO.EQUIPMENT_STATUS,						
                            SAQRIT.PLANT_ID as MNT_PLANT_ID, 
                            SAQRIT.PLANT_NAME as MNT_PLANT_NAME, 
                            SAQRIT.PLANT_RECORD_ID as MNT_PLANT_RECORD_ID,				
                            SAQTRV.SALESORG_ID, 
                            SAQTRV.SALESORG_NAME, 
                            SAQTRV.SALESORG_RECORD_ID,  
                            SAQRIT.FABLOCATION_ID as FABLOC,
                            SAQRIT.FABLOCATION_ID,
                            SAQRIT.FABLOCATION_NAME,
                            SAQRIT.FABLOCATION_RECORD_ID,
                            SAQRIT.GREENBOOK as GRNBOK, 
                            SAQRIT.GREENBOOK, 
                            SAQRIT.GREENBOOK_RECORD_ID, 			
                            SAQTRV.GLOBAL_CURRENCY,
                            SAQTRV.GLOBAL_CURRENCY_RECORD_ID,					
                            SAQRIT.OBJECT_TYPE,
                            SAQTRV.BLUEBOOK as BLUBOK,
                            null as WTYSTE,
                            null as WTYEND,
                            null as WTYDAY,
                            null as PLTFRM,
                            SAQSCO.WAFER_SIZE as SUBSIZ,
                            SAQTRV.REGION as REGION,
                            SAQTMT.POES as ISPOES,
                            CASE WHEN ISNULL(PRSPRV.SSCM_COST, 0) = 1 THEN 'SSCM' ELSE 'CPQ' END as CSTSRC,
                            CASE WHEN ISNULL(PRSPRV.SSCM_COST, 0) = 1 THEN 'VALUE PRICING-SSCM' ELSE 'OFFLINE PRICING' END as PRCSRC,
                            --'No' as SPQTEV,
                            SAQRIT.TAX_PERCENTAGE as TAXVTP,
                            SAQRIT.TAXCLASSIFICATION_ID,
                            SAQTRV.EXCHANGE_RATE,
                            SAQTRV.EXCHANGE_RATE_DATE,
                            SAQTRV.DOC_CURRENCY,
                            null as PM_ID,
                            SAQGPA.MNTEVT_LEVEL,
                            null as PM_RECORD_ID,
                            null as ASSEMBLY_ID,
                            null as ASSEMBLY_RECORD_ID,
                            SAQGPA.GOT_CODE,
                            --SAQGPA.DEVICE_NODE as EQNODE,
                            SAQGPA.PROCESS_TYPE as PROCES,
                            SAQGPA.KIT_ID as KIT_ID,
                            --SAQRIT.KIT_NUMBER as KIT_NUMBER,
                            --SAQRIT.KITNUMBER_RECORD_ID as TKM_RECORD_ID,
                            SAQGPE.INTCPV,
                            SAQGPE.INTCPC,
                            SAQGPE.OSSVDV,
                            SAQGPE.LTCOSS,
                            SAQGPE.POFVDV,
                            SAQGPE.POFVDC,
                            SAQGPE.GREENBOOK as GBKVDV,
                            SAQGPE.GBKVDC,
                            SAQGPE.UIMVDV,
                            SAQGPE.UIMVDC,
                            SAQGPE.CAVVDV,
                            SAQGPE.CAVVDC,
                            SAQGPE.WNDVDV,
                            SAQGPE.WNDVDC,
                            SAQGPE.CCRTMV,
                            SAQGPE.CCRTMC,
                            SAQGPE.SCMVDV,
                            SAQGPE.SCMVDC,
                            SAQGPE.CCDFFV,
                            NULL AS CCDFFC,
                            SAQGPE.NPIVDV,
                            SAQGPE.NPIVDC,
                            SAQGPE.DTPVDV,
                            SAQGPE.DTPVDC,
                            SAQGPE.CSTVDV,
                            SAQGPE.CSTVDC,
                            SAQGPE.CSGVDV,
                            SAQGPE.CSGVDC,
                            SAQGPE.QRQVDV,
                            SAQGPE.QRQVDC,
                            SAQGPE.SVCVDV,
                            SAQGPE.SVCVDC,
                            SAQGPE.RKFVDV,
                            SAQGPE.RKFVDC,
                            SAQGPE.PBPVDV,
                            SAQGPE.PBPVDC,
                            SAQGPE.CMLAB_ENT,
                            SAQGPE.CNSMBL_ENT,
                            SAQGPE.CNTCVG_ENT,
                            SAQGPE.NCNSMB_ENT,
                            SAQGPE.PMEVNT_ENT,
                            SAQGPE.PMLAB_ENT,
                            SAQGPE.PRMKPI_ENT,
                            SAQGPE.OFRING,
                            SAQGPE.QTETYP,
                            SAQGPE.BILTYP,
                            SAQGPE.BPTKPI,
                            SAQGPE.ATGKEY,
                            SAQGPE.ATNKEY,                           
                            SAQGPE.NWPTON,
                            SAQGPE.HEDBIN,
                            SAQGPE.WETCLN_ENT,
                            SAQGPE.SPQTEV,
                            SAQGPE.SVSPCT,
                            SAQGPE.SPSPCT,
                            SAQGPE.SWPKTA,
                            SAQGPE.NUMLAY,
                            SAQGPE.ITTNBV,
                            SAQGPA.CHAMBER_QTY AS ITCTAS,
                            SAQGPE.ITSDUB,
                            SAQGPE.ITSDUT,
                            SAQGPE.ITSPCL,
                            SAQGPE.ITSPCT,
                            SAQCYR.CNTYER as CNTYER,
                            SAQGPA.QTESRVCOB_RECORD_ID,
                            SAQSCO.TEMP_TOOL,
                            CASE WHEN SAQRIT.CONTRACT_VALID_FROM > SAQCYR.CONTRACT_START_DATE THEN SAQRIT.CONTRACT_VALID_FROM ELSE SAQCYR.CONTRACT_START_DATE END as STADTE,
                            CASE WHEN SAQRIT.CONTRACT_VALID_FROM > SAQCYR.CONTRACT_START_DATE THEN SAQRIT.CONTRACT_VALID_FROM ELSE SAQCYR.CONTRACT_START_DATE END as CONTRACT_VALID_FROM,
                            CASE WHEN SAQCYR.CONTRACT_END_DATE > SAQRIT.CONTRACT_VALID_TO THEN SAQRIT.CONTRACT_VALID_TO ELSE SAQCYR.CONTRACT_END_DATE END as ENDDTE,
                            CASE WHEN SAQCYR.CONTRACT_END_DATE > SAQRIT.CONTRACT_VALID_TO THEN SAQRIT.CONTRACT_VALID_TO ELSE SAQCYR.CONTRACT_END_DATE END as CONTRACT_VALID_TO,
                            Abs(DATEDIFF(day,CASE WHEN SAQCYR.CONTRACT_END_DATE > SAQRIT.CONTRACT_VALID_TO THEN SAQRIT.CONTRACT_VALID_TO ELSE SAQCYR.CONTRACT_END_DATE END , CASE WHEN SAQRIT.CONTRACT_VALID_FROM > SAQCYR.CONTRACT_START_DATE THEN SAQRIT.CONTRACT_VALID_FROM ELSE SAQCYR.CONTRACT_START_DATE END)) + 1 as CNTDAY
                        FROM 
                            SAQRIT (NOLOCK)		
                            JOIN (
                                SELECT SAQGPA.SERVICE_ID, SAQGPA.GREENBOOK, SAQGPA.FABLOCATION_ID, SAQGPA.GOT_CODE, SAQGPA.KIT_ID, SAQGPA.QUOTE_RECORD_ID, SAQGPA.QTEREV_RECORD_ID, SAQGPA.GOTCODE_RECORD_ID, SAQGPA.MNTEVT_LEVEL, SAQGPA.SERVICE_DESCRIPTION, SAQGPA.SERVICE_RECORD_ID, SAQGPA.FABLOCATION_NAME, SAQGPA.FABLOCATION_RECORD_ID, SAQGPA.GREENBOOK_RECORD_ID, ISNULL(SAQGPA.PROCESS_TYPE,'') as PROCESS_TYPE, ISNULL(DEVICE_NODE,'') as DEVICE_NODE, SAQGPA.EQUIPMENT_ID, SAQGPA.EQUIPMENT_RECORD_ID,SAQGPA.EQUIPMENT_DESCRIPTION, COUNT(ISNULL(ASSEMBLY_ID,0)) AS CHAMBER_QTY,QTESRVCOB_RECORD_ID
                                    FROM SAQGPA (NOLOCK) 								
                                    WHERE SAQGPA.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQGPA.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQGPA.SERVICE_ID = '{ServiceId}'  AND ISNULL(SAQGPA.KIT_ID,'') != '' AND INCLUDED = 1
                                    GROUP BY SAQGPA.SERVICE_ID, SAQGPA.GREENBOOK, SAQGPA.FABLOCATION_ID,SAQGPA.GOT_CODE, SAQGPA.KIT_ID,  SAQGPA.QUOTE_RECORD_ID, SAQGPA.QTEREV_RECORD_ID, SAQGPA.GOTCODE_RECORD_ID, SAQGPA.MNTEVT_LEVEL, SAQGPA.SERVICE_DESCRIPTION, SAQGPA.SERVICE_RECORD_ID, SAQGPA.FABLOCATION_NAME, SAQGPA.FABLOCATION_RECORD_ID,SAQGPA.GREENBOOK_RECORD_ID, ISNULL(PROCESS_TYPE,''), ISNULL(DEVICE_NODE,''), SAQGPA.EQUIPMENT_ID, SAQGPA.EQUIPMENT_RECORD_ID,SAQGPA.EQUIPMENT_DESCRIPTION,QTESRVCOB_RECORD_ID
                            ) SAQGPA ON SAQGPA.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND SAQGPA.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID AND SAQGPA.SERVICE_ID = SAQRIT.SERVICE_ID AND SAQGPA.GREENBOOK_RECORD_ID = SAQRIT.GREENBOOK_RECORD_ID AND SAQGPA.KIT_ID = SAQRIT.KIT_ID AND SAQGPA.GOT_CODE = SAQRIT.GOT_CODE AND ISNULL(SAQGPA.PROCESS_TYPE,'') = ISNULL(SAQRIT.PROCESS_TYPE,'') AND ISNULL(SAQGPA.DEVICE_NODE,'') = ISNULL(SAQRIT.DEVICE_NODE,'') AND SAQGPA.FABLOCATION_ID = SAQRIT.FABLOCATION_ID
                            JOIN SAQGPE (NOLOCK) ON SAQGPE.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND SAQGPE.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID AND SAQGPE.SERVICE_ID = SAQRIT.SERVICE_ID AND SAQGPE.KIT_ID = SAQGPA.KIT_ID AND SAQGPE.GOT_CODE = SAQGPA.GOT_CODE			
                            JOIN SAQSCO (NOLOCK) ON SAQSCO.QUOTE_RECORD_ID = SAQGPA.QUOTE_RECORD_ID AND SAQSCO.QTEREV_RECORD_ID = SAQGPA.QTEREV_RECORD_ID AND SAQSCO.SERVICE_RECORD_ID = SAQGPA.SERVICE_RECORD_ID AND SAQSCO.GREENBOOK = SAQGPA.GREENBOOK AND SAQSCO.FABLOCATION_RECORD_ID = SAQGPA.FABLOCATION_RECORD_ID AND SAQSCO.EQUIPMENT_ID = SAQGPA.EQUIPMENT_ID AND SAQGPA.QTESRVCOB_RECORD_ID = QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID
                            JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID         
                            JOIN SAQTRV (NOLOCK) ON SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID 						
                            LEFT JOIN PRSPRV (NOLOCK) ON PRSPRV.SERVICE_RECORD_ID = SAQRIT.SERVICE_RECORD_ID	
                            {YearWiseJoinString}				
                        WHERE 
                            SAQRIT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQRIT.SERVICE_ID = '{ServiceId}' AND ISNULL(SAQGPE.CONFIGURATION_STATUS,'') = 'COMPLETE'
                        ) IQ
                        LEFT JOIN SAQICO (NOLOCK) ON SAQICO.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND SAQICO.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND SAQICO.SERVICE_RECORD_ID = IQ.SERVICE_RECORD_ID AND SAQICO.GREENBOOK_RECORD_ID = IQ.GREENBOOK_RECORD_ID AND ISNULL(SAQICO.FABLOCATION_RECORD_ID,'') = ISNULL(IQ.FABLOCATION_RECORD_ID,'') AND SAQICO.KIT_ID = IQ.KIT_ID AND SAQICO.GOT_CODE = IQ.GOT_CODE AND SAQICO.CNTYER = IQ.CNTYER AND SAQICO.QTESRVCOB_RECORD_ID = IQ.QTESRVCOB_RECORD_ID
                        WHERE ISNULL(SAQICO.KIT_ID,'') = ''
                        """.format(UserId=self.user_id, UserName=self.user_name, QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id, YearWiseJoinString = yearwise_join_str)
                )
                #INC08675532 #INC08675479 - END - M
            # CR704 - Start - M
            #A055S000P01-21072 Start M
            self.update_cntday()
            #A055S000P01-21072 End M
            # PMSA - Quantity Update
            #INC08745555 Start - M
            #A055S000P01-20653, A055S000P01-20868 - M
            Sql.RunQuery("""UPDATE SAQICO SET QUANTITY = SAQGPA.QUANTITY,
                ADJ_PM_FREQUENCY = SAQGPA.QUANTITY,
                CTAJPM = CASE WHEN SAQICO.QTETYP IN ('Flex Event Based','Event Based') THEN ROUND((CONVERT(FLOAT, SAQGPA.QUANTITY)*1.0/365) * CNTDAY,5,0) ELSE NULL END,
                SSCM_PM_FREQUENCY =  SAQGPA.SSCM_PM_FREQUENCY,
                AIUPPE = SAQICO.USRPRC / NULLIF(SAQGPA.QUANTITY, 0)
                FROM SAQICO (NOLOCK)
                JOIN (
                    SELECT SAQGPA.EQUIPMENT_ID,SAQGPA.SERVICE_ID,SAQGPA.GREENBOOK,SAQGPA.FABLOCATION_ID,SAQGPA.GOT_CODE,SAQGPA.KIT_ID,SAQGPA.QUOTE_RECORD_ID,SAQGPA.QTEREV_RECORD_ID, SAQGPA.GOTCODE_RECORD_ID, SAQGPA.MNTEVT_LEVEL,SAQGPA.SERVICE_DESCRIPTION, SAQGPA.SERVICE_RECORD_ID, SAQGPA.FABLOCATION_NAME, SAQGPA.FABLOCATION_RECORD_ID,SAQGPA.GREENBOOK_RECORD_ID, ISNULL(PROCESS_TYPE,'') AS PROCESS_TYPE , ISNULL(DEVICE_NODE,'') AS DEVICE_NODE, SUM(ISNULL(SAQGPA.PM_FREQUENCY, 0)) as QUANTITY, SUM(ISNULL(SAQGPA.SSCM_PM_FREQUENCY, 0)) as SSCM_PM_FREQUENCY,QTESRVCOB_RECORD_ID
                        FROM SAQGPA (NOLOCK)
                        WHERE SAQGPA.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQGPA.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQGPA.SERVICE_ID = '{ServiceId}' AND SAQGPA.INCLUDED = 1 AND ISNULL(SAQGPA.KIT_ID,'') != ''
                        GROUP BY SAQGPA.SERVICE_ID,SAQGPA.GREENBOOK,SAQGPA.FABLOCATION_ID,SAQGPA.GOT_CODE,SAQGPA.KIT_ID,SAQGPA.QUOTE_RECORD_ID,SAQGPA.QTEREV_RECORD_ID,SAQGPA.EQUIPMENT_ID, SAQGPA.GOTCODE_RECORD_ID, SAQGPA.MNTEVT_LEVEL,SAQGPA.SERVICE_DESCRIPTION, SAQGPA.SERVICE_RECORD_ID, SAQGPA.FABLOCATION_NAME, SAQGPA.FABLOCATION_RECORD_ID,SAQGPA.GREENBOOK_RECORD_ID, ISNULL(PROCESS_TYPE,'')  , ISNULL(DEVICE_NODE,''),QTESRVCOB_RECORD_ID
                ) SAQGPA ON SAQGPA.QUOTE_RECORD_ID = SAQICO.QUOTE_RECORD_ID AND SAQGPA.QTEREV_RECORD_ID = SAQICO.QTEREV_RECORD_ID AND SAQGPA.SERVICE_ID = SAQICO.SERVICE_ID AND SAQGPA.FABLOCATION_ID = SAQICO.FABLOCATION_ID AND SAQGPA.GREENBOOK = SAQICO.GREENBOOK AND SAQGPA.KIT_ID = SAQICO.KIT_ID AND SAQGPA.GOT_CODE = SAQICO.GOT_CODE AND SAQGPA.EQUIPMENT_ID = SAQICO.EQUIPMENT_ID AND ISNULL(SAQGPA.PROCESS_TYPE,'')= ISNULL(SAQICO.PROCES,'') AND ISNULL(SAQGPA.DEVICE_NODE,'') = ISNULL(SAQICO.DEVICE_NODE,'') AND SAQICO.QTESRVCOB_RECORD_ID = SAQGPA.QTESRVCOB_RECORD_ID
                WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}'""".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id)
            )
            #INC08745555 End - M
            #A055S000P01-20653, A055S000P01-20868 - M
            ##saqrit quantity update
            self._quote_item_qty_update()
        elif self.quote_service_entitlement_type == 'STR-OFFBGBEQAS OBJ-AS':
            # CR704 - Start - M		 
            for contract_year_obj in contract_years_obj:
                if contract_year_obj.CNTYER == 'YEAR 1':
                    yearwise_join_str = "JOIN SAQCYR (NOLOCK) ON SAQCYR.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND SAQCYR.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID AND SAQCYR.CONTRACT_START_DATE <= SAQRIT.CONTRACT_VALID_FROM AND SAQCYR.CONTRACT_END_DATE >= SAQRIT.CONTRACT_VALID_FROM"
                else:
                    yearwise_join_str = "JOIN SAQCYR (NOLOCK) ON SAQCYR.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND SAQCYR.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID AND ((SAQCYR.CONTRACT_START_DATE >= SAQRIT.CONTRACT_VALID_FROM AND SAQCYR.CONTRACT_START_DATE <= SAQRIT.CONTRACT_VALID_TO) OR (SAQCYR.CONTRACT_START_DATE <= SAQRIT.CONTRACT_VALID_FROM AND SAQCYR.CONTRACT_END_DATE >= SAQRIT.CONTRACT_VALID_FROM))"
                #INC08675532 #INC08675479,INC09026574 - START - M
                Sql.RunQuery("""INSERT SAQICO (EQUIPMENT_DESCRIPTION, STATUS, QUANTITY, OBJECT_ID, EQUPID, EQUIPMENT_ID, EQUIPMENT_RECORD_ID, LINE, QUOTE_ID, QTEITM_RECORD_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, KPU, SERNUM, SERIAL_NO, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, TECHNOLOGY, CUSTOMER_TOOL_ID, EQUCAT, EQUIPMENTCATEGORY_ID, EQUIPMENTCATEGORY_RECORD_ID, EQUIPMENT_STATUS, MNT_PLANT_ID, MNT_PLANT_NAME, MNT_PLANT_RECORD_ID, SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID, FABLOC, FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, GRNBOK, GREENBOOK, GREENBOOK_RECORD_ID,ASSEMBLY_ID,ASSEMBLY_RECORD_ID, GLOBAL_CURRENCY,GLOBAL_CURRENCY_RECORD_ID, OBJECT_TYPE, BLUBOK, WTYSTE, WTYEND, WTYDAY, PLTFRM, SUBSIZ, REGION, ISPOES, CSTSRC, PRCSRC, TAXVTP,TAXGRP,DCCRFX,DCCRXD,DOCCUR, INTCPV, INTCPC, OSSVDV, LTCOSS, POFVDV, POFVDC, GBKVDV, GBKVDC, UIMVDV, UIMVDC, CAVVDV, CAVVDC, WNDVDV, WNDVDC, CCRTMV, CCRTMC, SCMVDV, SCMVDC, CCDFFV, CCDFFC, NPIVDV, NPIVDC, DTPVDV, DTPVDC, CSTVDV, CSTVDC, CSGVDV, CSGVDC, QRQVDV, QRQVDC, SVCVDV, SVCVDC, RKFVDV, RKFVDC, PBPVDV, PBPVDC, CMLAB_ENT, CNSMBL_ENT, CNTCVG_ENT, NCNSMB_ENT, PMEVNT_ENT, PMLAB_ENT, PRMKPI_ENT, OFRING, QTETYP, BILTYP, BPTTKP, ATGKEY, TGKPNS, NWPTON, HEDBIN, WETCLN_ENT, SPQTEV, SVSPCT, SPSPCT,SWPKTA,NUMLAY,ITTNBV,ITSDUB,ITSDUT,ITSPCL,ITSPCT,CNTYER, STADTE, CONTRACT_VALID_FROM, ENDDTE, CONTRACT_VALID_TO, CNTDAY, QUOTE_ITEM_COVERED_OBJECT_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified)
                        SELECT DISTINCT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_COVERED_OBJECT_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED,{UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (                        
                        SELECT DISTINCT					
                            SAQSCA.EQUIPMENT_DESCRIPTION,
                            null as STATUS,
                            null as EQUIPMENT_QUANTITY,
                            SAQRIT.OBJECT_ID,
                            SAQSCA.EQUIPMENT_ID as EQUPID,
                            SAQSCA.EQUIPMENT_ID,
                            SAQSCA.EQUIPMENT_RECORD_ID,
                            SAQRIT.LINE,
                            SAQRIT.QUOTE_ID, 
                            SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID, 
                            SAQRIT.QUOTE_RECORD_ID,
                            SAQRIT.QTEREV_ID,
                            SAQRIT.QTEREV_RECORD_ID,
                            null as  KPU,
                            null as SERNUM, 
                            null as SERIAL_NO, 
                            SAQRIT.SERVICE_DESCRIPTION, 
                            SAQRIT.SERVICE_ID, 
                            SAQRIT.SERVICE_RECORD_ID,								
                            null as TECHNOLOGY,																			
                            null as CUSTOMER_TOOL_ID, 
                            SAQSCA.EQUIPMENTCATEGORY_ID as EQUCAT, 
                            SAQSCA.EQUIPMENTCATEGORY_ID, 
                            SAQSCA.EQUIPMENTCATEGORY_RECORD_ID, 
                            null as EQUIPMENT_STATUS,					
                            SAQSCA.MNT_PLANT_ID, 
                            SAQSCA.MNT_PLANT_NAME, 
                            SAQSCA.MNT_PLANT_RECORD_ID,				
                            SAQSCA.SALESORG_ID, 
                            SAQSCA.SALESORG_NAME, 
                            SAQSCA.SALESORG_RECORD_ID,  
                            SAQRIT.FABLOCATION_ID as FABLOC,
                            SAQRIT.FABLOCATION_ID,
                            SAQRIT.FABLOCATION_NAME,
                            SAQRIT.FABLOCATION_RECORD_ID,
                            SAQRIT.GREENBOOK as GRNBOK, 
                            SAQRIT.GREENBOOK, 
                            SAQRIT.GREENBOOK_RECORD_ID, 
                            SAQRIT.ASSEMBLY_ID,
                            SAQRIT.ASSEMBLY_RECORD_ID,		
                            SAQTRV.GLOBAL_CURRENCY,
                            SAQTRV.GLOBAL_CURRENCY_RECORD_ID,					
                            SAQRIT.OBJECT_TYPE,
                            SAQTRV.BLUEBOOK as BLUBOK,
                            SAQSCA.WARRANTY_START_DATE as WTYSTE,
                            SAQSCA.WARRANTY_END_DATE as WTYEND,
                            Abs(DATEDIFF(day,SAQSCA.WARRANTY_END_DATE, SAQSCA.WARRANTY_START_DATE)) as WTYDAY,
                            null as PLTFRM,
                            SAQSCO.WAFER_SIZE as SUBSIZ,
                            SAQTRV.REGION as REGION,
                            SAQTMT.POES as ISPOES,
                            CASE WHEN ISNULL(PRSPRV.SSCM_COST, 0) = 1 THEN 'SSCM' ELSE 'CPQ' END as CSTSRC,
                            CASE WHEN ISNULL(PRSPRV.SSCM_COST, 0) = 1 THEN 'VALUE PRICING-SSCM' ELSE 'OFFLINE PRICING' END as PRCSRC,
                            --'No' as SPQTEV,
                            SAQRIT.TAX_PERCENTAGE as TAXVTP,
                            SAQRIT.TAXCLASSIFICATION_ID,
                            SAQTRV.EXCHANGE_RATE,
                            SAQTRV.EXCHANGE_RATE_DATE,
                            SAQTRV.DOC_CURRENCY,
                            SAQSCE.INTCPV,
                            SAQSCE.INTCPC,
                            SAQSCE.OSSVDV,
                            SAQSCE.LTCOSS,
                            SAQSCE.POFVDV,
                            SAQSCE.POFVDC,
                            SAQSCE.GREENBOOK as GBKVDV,
                            SAQSCE.GBKVDC,
                            SAQSCE.UIMVDV,
                            SAQSCE.UIMVDC,
                            SAQSCE.CAVVDV,
                            SAQSCE.CAVVDC,
                            SAQSCE.WNDVDV,
                            SAQSCE.WNDVDC,
                            SAQSCE.CCRTMV,
                            SAQSCE.CCRTMC,
                            SAQSCE.SCMVDV,
                            SAQSCE.SCMVDC,
                            SAQSCE.CCDFFV,
                            SAQSCE.CCDFFC,
                            SAQSCE.NPIVDV,
                            SAQSCE.NPIVDC,
                            SAQSCE.DTPVDV,
                            SAQSCE.DTPVDC,
                            SAQSCE.CSTVDV,
                            SAQSCE.CSTVDC,
                            SAQSCE.CSGVDV,
                            SAQSCE.CSGVDC,
                            SAQSCE.QRQVDV,
                            SAQSCE.QRQVDC,
                            SAQSCE.SVCVDV,
                            SAQSCE.SVCVDC,
                            SAQSCE.RKFVDV,
                            SAQSCE.RKFVDC,
                            SAQSCE.PBPVDV,
                            SAQSCE.PBPVDC,
                            SAQSCE.CMLAB_ENT,             
                            SAQSCE.CNSMBL_ENT,
                            SAQSCE.CNTCVG_ENT,
                            SAQSCE.NCNSMB_ENT,
                            SAQSCE.PMEVNT_ENT,
                            SAQSCE.PMLAB_ENT,
                            SAQSCE.PRMKPI_ENT,
                            SAQSCE.OFRING,
                            SAQSCE.QTETYP,
                            SAQSCE.BILTYP,
                            SAQSCE.BPTKPI,
                            SAQSCE.ATGKEY,
                            SAQSCE.ATNKEY,                          
                            SAQSCE.NWPTON,
                            SAQSCE.HEDBIN,
                            SAQSCE.WETCLN_ENT,
                            SAQSCE.SPQTEV,
                            SAQSCE.SVSPCT,
                            SAQSCE.SPSPCT,
                            SAQSCE.SWPKTA,
                            SAQSCE.NUMLAY,
                            SAQSCE.ITTNBV,
                            SAQSCE.ITSDUB,
                            SAQSCE.ITSDUT,
                            SAQSCE.ITSPCL,
                            SAQSCE.ITSPCT,
                            SAQCYR.CNTYER as CNTYER,
                            CASE WHEN SAQRIT.CONTRACT_VALID_FROM > SAQCYR.CONTRACT_START_DATE THEN SAQRIT.CONTRACT_VALID_FROM ELSE SAQCYR.CONTRACT_START_DATE END as STADTE,
                            CASE WHEN SAQRIT.CONTRACT_VALID_FROM > SAQCYR.CONTRACT_START_DATE THEN SAQRIT.CONTRACT_VALID_FROM ELSE SAQCYR.CONTRACT_START_DATE END as CONTRACT_VALID_FROM,
                            CASE WHEN SAQCYR.CONTRACT_END_DATE > SAQRIT.CONTRACT_VALID_TO THEN SAQRIT.CONTRACT_VALID_TO ELSE SAQCYR.CONTRACT_END_DATE END as ENDDTE,
                            CASE WHEN SAQCYR.CONTRACT_END_DATE > SAQRIT.CONTRACT_VALID_TO THEN SAQRIT.CONTRACT_VALID_TO ELSE SAQCYR.CONTRACT_END_DATE END as CONTRACT_VALID_TO,
                            Abs(DATEDIFF(day,CASE WHEN SAQCYR.CONTRACT_END_DATE > SAQRIT.CONTRACT_VALID_TO THEN SAQRIT.CONTRACT_VALID_TO ELSE SAQCYR.CONTRACT_END_DATE END , CASE WHEN SAQRIT.CONTRACT_VALID_FROM > SAQCYR.CONTRACT_START_DATE THEN SAQRIT.CONTRACT_VALID_FROM ELSE SAQCYR.CONTRACT_START_DATE END)) + 1 as CNTDAY
                        FROM 
                            SAQSCA (NOLOCK)	
                            JOIN SAQSCO (NOLOCK) ON SAQSCO.QUOTE_RECORD_ID = SAQSCA.QUOTE_RECORD_ID AND SAQSCO.SERVICE_ID = SAQSCA.SERVICE_ID AND SAQSCO.QTEREV_RECORD_ID = SAQSCA.QTEREV_RECORD_ID AND SAQSCO.EQUIPMENT_ID = SAQSCA.EQUIPMENT_ID AND SAQSCO.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID = SAQSCA.QTESRVCOB_RECORD_ID
                            JOIN SAQSCE (NOLOCK) ON SAQSCE.QUOTE_RECORD_ID = SAQSCA.QUOTE_RECORD_ID AND SAQSCE.SERVICE_ID = SAQSCA.SERVICE_ID AND SAQSCE.QTEREV_RECORD_ID = SAQSCA.QTEREV_RECORD_ID AND SAQSCO.EQUIPMENT_ID = SAQSCE.EQUIPMENT_ID AND  SAQSCA.QTESRVCOB_RECORD_ID=  SAQSCE.QTESRVCOB_RECORD_ID
                            AND SAQSCE.EQUIPMENT_RECORD_ID = SAQSCA.EQUIPMENT_RECORD_ID
                            JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQSCA.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = SAQSCA.QTEREV_RECORD_ID         
                            JOIN SAQTRV (NOLOCK) ON SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID 
                            JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = SAQTRV.QUOTE_RECORD_ID
                                                    AND SAQRIT.SERVICE_RECORD_ID = SAQSCA.SERVICE_RECORD_ID
                                                    AND SAQRIT.QTEREV_RECORD_ID = SAQSCA.QTEREV_RECORD_ID
                                                    AND SAQRIT.GREENBOOK_RECORD_ID = SAQSCA.GREENBOOK_RECORD_ID
                                                    AND SAQRIT.EQUIPMENT_ID = SAQSCA.EQUIPMENT_ID
                                                    AND SAQRIT.ASSEMBLY_ID = SAQSCA.ASSEMBLY_ID
                                                    AND SAQRIT.QTESRVCOB_RECORD_ID =  SAQSCA.QTESRVCOB_RECORD_ID
                            LEFT JOIN PRSPRV (NOLOCK) ON PRSPRV.SERVICE_RECORD_ID = SAQSCA.SERVICE_RECORD_ID
                            {YearWiseJoinString}					
                        WHERE 
                            SAQSCA.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCA.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQSCA.SERVICE_ID = '{ServiceId}' AND ISNULL(SAQSCE.CONFIGURATION_STATUS,'') = 'COMPLETE'
                        ) IQ
                        LEFT JOIN SAQICO (NOLOCK) ON SAQICO.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND SAQICO.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND SAQICO.SERVICE_RECORD_ID = IQ.SERVICE_RECORD_ID AND SAQICO.GREENBOOK_RECORD_ID = IQ.GREENBOOK_RECORD_ID AND ISNULL(SAQICO.FABLOCATION_RECORD_ID,'') = ISNULL(IQ.FABLOCATION_RECORD_ID,'') AND SAQICO.EQUIPMENT_RECORD_ID = IQ.EQUIPMENT_RECORD_ID AND SAQICO.ASSEMBLY_RECORD_ID = IQ.ASSEMBLY_RECORD_ID AND SAQICO.CNTYER = IQ.CNTYER
                        WHERE ISNULL(SAQICO.ASSEMBLY_RECORD_ID,'') = ''
                        """.format(UserId=self.user_id, UserName=self.user_name, QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id, YearWiseJoinString = yearwise_join_str)
                )
                #INC08675532 #INC08675479,INC09026574 - END - M
        #A055S000P01-21015 - End - M
            #A055S000P01-21072 Start M
            self.update_cntday()
            #A055S000P01-21072 End M
            # CR704 - Start - M
        else:
            if self.service_id in ('Z0110','Z0108'):
                self._simple_quote_annualized_items_insert()
            else:
                # CR704 - Start - M	
                for contract_year_obj in contract_years_obj:
                    if contract_year_obj.CNTYER == 'YEAR 1':
                        yearwise_join_str = "JOIN SAQCYR (NOLOCK) ON SAQCYR.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND SAQCYR.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID AND SAQCYR.CONTRACT_START_DATE <= SAQRIT.CONTRACT_VALID_FROM AND SAQCYR.CONTRACT_END_DATE >= SAQRIT.CONTRACT_VALID_FROM"
                    else:
                        yearwise_join_str = "JOIN SAQCYR (NOLOCK) ON SAQCYR.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND SAQCYR.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID AND ((SAQCYR.CONTRACT_START_DATE >= SAQRIT.CONTRACT_VALID_FROM AND SAQCYR.CONTRACT_START_DATE <= SAQRIT.CONTRACT_VALID_TO) OR (SAQCYR.CONTRACT_START_DATE <= SAQRIT.CONTRACT_VALID_FROM AND SAQCYR.CONTRACT_END_DATE >= SAQRIT.CONTRACT_VALID_FROM))"	
                    #INC08675532 #INC08675479 - START - M
                    Sql.RunQuery("""INSERT SAQICO (EQUIPMENT_DESCRIPTION, STATUS, QUANTITY, OBJECT_ID, EQUPID, EQUIPMENT_ID, EQUIPMENT_RECORD_ID, LINE, QUOTE_ID, QTEITM_RECORD_ID, QUOTE_RECORD_ID, QTEREV_ID,QTEREV_RECORD_ID, KPU, SERNUM, SERIAL_NO, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, TECHNOLOGY,CUSTOMER_TOOL_ID, EQUCAT, EQUIPMENTCATEGORY_ID, EQUIPMENTCATEGORY_RECORD_ID, EQUIPMENT_STATUS, MNT_PLANT_ID, MNT_PLANT_NAME, MNT_PLANT_RECORD_ID, SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID,  FABLOC, FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, GRNBOK, GREENBOOK, GREENBOOK_RECORD_ID, GLOBAL_CURRENCY, GLOBAL_CURRENCY_RECORD_ID, OBJECT_TYPE, BLUBOK, WTYSTE, WTYEND, WTYDAY, PLTFRM, SUBSIZ, REGION, ISPOES, CSTSRC, PRCSRC, TAXVTP,TAXGRP,DCCRFX,DCCRXD,DOCCUR, INTCPV, INTCPC, OSSVDV, LTCOSS, POFVDV, POFVDC, GBKVDV, GBKVDC, UIMVDV, UIMVDC, CAVVDV, CAVVDC, WNDVDV, WNDVDC, CCRTMV, CCRTMC, SCMVDV, SCMVDC, CCDFFV, CCDFFC, NPIVDV, NPIVDC, DTPVDV, DTPVDC, CSTVDV, CSTVDC, CSGVDV, CSGVDC, QRQVDV, QRQVDC, SVCVDV, SVCVDC, RKFVDV, RKFVDC, PBPVDV, PBPVDC, CMLAB_ENT, CNSMBL_ENT, CNTCVG_ENT, NCNSMB_ENT, PMEVNT_ENT, PMLAB_ENT, PRMKPI_ENT, OFRING, QTETYP, BILTYP, BPTTKP, ATGKEY, TGKPNS, NWPTON, HEDBIN, WETCLN_ENT, SPQTEV, SVSPCT, SPSPCT,SWPKTA,NUMLAY,ITTNBV,ITSDUB,ITSDUT,ITSPCL,ITSPCT, CNTYER, STADTE, CONTRACT_VALID_FROM, ENDDTE, CONTRACT_VALID_TO, CNTDAY, QUOTE_ITEM_COVERED_OBJECT_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified)
                            SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_COVERED_OBJECT_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED,{UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
                                SELECT DISTINCT					
                                    null as EQUIPMENT_DESCRIPTION,
                                    null as STATUS,
                                    null as EQUIPMENT_QUANTITY,
                                    SAQRIT.OBJECT_ID,
                                    null as EQUPID,
                                    null as EQUIPMENT_ID,
                                    null as EQUIPMENT_RECORD_ID,
                                    SAQRIT.LINE,
                                    SAQRIT.QUOTE_ID, 
                                    SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID, 
                                    SAQRIT.QUOTE_RECORD_ID,
                                    SAQRIT.QTEREV_ID,
                                    SAQRIT.QTEREV_RECORD_ID,
                                    null as KPU,
                                    null as SERNUM, 
                                    null as SERIAL_NO, 
                                    SAQRIT.SERVICE_DESCRIPTION, 
                                    SAQRIT.SERVICE_ID, 
                                    SAQRIT.SERVICE_RECORD_ID,								
                                    null as TECHNOLOGY,																			
                                    null as CUSTOMER_TOOL_ID, 
                                    null as EQUCAT, 
                                    null as EQUIPMENTCATEGORY_ID, 
                                    null as EQUIPMENTCATEGORY_RECORD_ID, 
                                    null as EQUIPMENT_STATUS,					
                                    null as MNT_PLANT_ID, 
                                    null as MNT_PLANT_NAME, 
                                    null as MNT_PLANT_RECORD_ID,			
                                    SAQTRV.SALESORG_ID, 
                                    SAQTRV.SALESORG_NAME, 
                                    SAQTRV.SALESORG_RECORD_ID, 
                                    SAQRIT.FABLOCATION_ID as FABLOC,
                                    SAQRIT.FABLOCATION_ID,
                                    SAQRIT.FABLOCATION_NAME,
                                    SAQRIT.FABLOCATION_RECORD_ID,
                                    SAQRIT.GREENBOOK as GRNBOK, 
                                    SAQRIT.GREENBOOK, 
                                    SAQRIT.GREENBOOK_RECORD_ID, 			
                                    SAQTRV.GLOBAL_CURRENCY,
                                    SAQTRV.GLOBAL_CURRENCY_RECORD_ID,					
                                    SAQRIT.OBJECT_TYPE,
                                    SAQTRV.BLUEBOOK as BLUBOK,
                                    null as WTYSTE,
                                    null as WTYEND,
                                    null as WTYDAY,
                                    null as PLTFRM,
                                    null as SUBSIZ,
                                    SAQTRV.REGION as REGION,
                                    SAQTMT.POES as ISPOES,
                                    CASE WHEN ISNULL(PRSPRV.SSCM_COST, 0) = 1 THEN 'SSCM' ELSE 'CPQ' END as CSTSRC,
                                    CASE WHEN ISNULL(PRSPRV.SSCM_COST, 0) = 1 THEN 'VALUE PRICING-SSCM' ELSE 'OFFLINE PRICING' END as PRCSRC,--'No' as SPQTEV,
                                    SAQRIT.TAX_PERCENTAGE as TAXVTP,
                                    SAQRIT.TAXCLASSIFICATION_ID,
                                    SAQTRV.EXCHANGE_RATE,
                                    SAQTRV.EXCHANGE_RATE_DATE,
                                    SAQTRV.DOC_CURRENCY,
                                    SAQSGE.INTCPV,
                                    SAQSGE.INTCPC,
                                    SAQSGE.OSSVDV,
                                    SAQSGE.LTCOSS,
                                    null as POFVDV,
                                    SAQSGE.POFVDC,
                                    SAQSGE.GREENBOOK as GBKVDV,
                                    SAQSGE.GBKVDC,
                                    SAQSGE.UIMVDV,
                                    SAQSGE.UIMVDC,
                                    SAQSGE.CAVVDV,
                                    SAQSGE.CAVVDC,
                                    SAQSGE.WNDVDV,
                                    SAQSGE.WNDVDC,
                                    SAQSGE.CCRTMV,
                                    SAQSGE.CCRTMC,
                                    SAQSGE.SCMVDV,
                                    SAQSGE.SCMVDC,
                                    SAQSGE.CCDFFV,
                                    SAQSGE.CCDFFC,
                                    SAQSGE.NPIVDV,
                                    SAQSGE.NPIVDC,
                                    SAQSGE.DTPVDV,
                                    SAQSGE.DTPVDC,
                                    SAQSGE.CSTVDV,
                                    SAQSGE.CSTVDC,
                                    SAQSGE.CSGVDV,
                                    SAQSGE.CSGVDC,
                                    SAQSGE.QRQVDV,
                                    SAQSGE.QRQVDC,
                                    SAQSGE.SVCVDV,
                                    SAQSGE.SVCVDC,
                                    SAQSGE.RKFVDV,
                                    SAQSGE.RKFVDC,
                                    SAQSGE.PBPVDV,
                                    SAQSGE.PBPVDC,
                                    SAQSGE.CMLAB_ENT,           
                                    SAQSGE.CNSMBL_ENT,
                                    SAQSGE.CNTCVG_ENT,
                                    SAQSGE.NCNSMB_ENT,
                                    SAQSGE.PMEVNT_ENT,
                                    SAQSGE.PMLAB_ENT,
                                    SAQSGE.PRMKPI_ENT,
                                    SAQSGE.OFRING,
                                    SAQSGE.QTETYP,
                                    SAQSGE.BILTYP,
                                    SAQSGE.BPTKPI,
                                    SAQSGE.ATGKEY,
                                    SAQSGE.ATNKEY,                            
                                    SAQSGE.NWPTON,
                                    SAQSGE.HEDBIN,
                                    SAQSGE.WETCLN_ENT,
                                    SAQSGE.SPQTEV,
                                    SAQSGE.SVSPCT,
                                    SAQSGE.SPSPCT,
                                    SAQSGE.SWPKTA,
                                    SAQSGE.NUMLAY,
                                    SAQSGE.ITTNBV,
                                    SAQSGE.ITSDUB,
                                    SAQSGE.ITSDUT,
                                    SAQSGE.ITSPCL,
                                    SAQSGE.ITSPCT,
                                    SAQCYR.CNTYER as CNTYER,
                                    CASE WHEN SAQRIT.CONTRACT_VALID_FROM > SAQCYR.CONTRACT_START_DATE THEN SAQRIT.CONTRACT_VALID_FROM ELSE SAQCYR.CONTRACT_START_DATE END as STADTE,
                                    CASE WHEN SAQRIT.CONTRACT_VALID_FROM > SAQCYR.CONTRACT_START_DATE THEN SAQRIT.CONTRACT_VALID_FROM ELSE SAQCYR.CONTRACT_START_DATE END as CONTRACT_VALID_FROM,
                                    CASE WHEN SAQCYR.CONTRACT_END_DATE > SAQRIT.CONTRACT_VALID_TO THEN SAQRIT.CONTRACT_VALID_TO ELSE SAQCYR.CONTRACT_END_DATE END as ENDDTE,
                                    CASE WHEN SAQCYR.CONTRACT_END_DATE > SAQRIT.CONTRACT_VALID_TO THEN SAQRIT.CONTRACT_VALID_TO ELSE SAQCYR.CONTRACT_END_DATE END as CONTRACT_VALID_TO,
                                    Abs(DATEDIFF(day,CASE WHEN SAQCYR.CONTRACT_END_DATE > SAQRIT.CONTRACT_VALID_TO THEN SAQRIT.CONTRACT_VALID_TO ELSE SAQCYR.CONTRACT_END_DATE END , CASE WHEN SAQRIT.CONTRACT_VALID_FROM > SAQCYR.CONTRACT_START_DATE THEN SAQRIT.CONTRACT_VALID_FROM ELSE SAQCYR.CONTRACT_START_DATE END)) + 1 as CNTDAY	    
                                FROM 
                                    SAQRIT 
                                    JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID         
                                    JOIN SAQTRV (NOLOCK) ON SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID 
                                    JOIN SAQSGE (NOLOCK) ON SAQSGE.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND SAQSGE.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID AND SAQSGE.SERVICE_ID = SAQRIT.SERVICE_ID AND SAQSGE.GREENBOOK = SAQRIT.GREENBOOK  AND ISNULL(SAQRIT.PAR_PRDOFR_ID,'') = ISNULL(SAQSGE.PAR_SERVICE_ID,'')
                                    {ancillary_join}
                                    LEFT JOIN PRSPRV (NOLOCK) ON PRSPRV.SERVICE_RECORD_ID = SAQRIT.SERVICE_RECORD_ID	
                                    {YearWiseJoinString}                
                                WHERE 
                                    SAQRIT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQRIT.SERVICE_ID = '{ServiceId}' AND ISNULL(SAQSGE.CONFIGURATION_STATUS,'') = 'COMPLETE' {ancillary_where}
                            ) IQ
                            LEFT JOIN SAQICO (NOLOCK) ON SAQICO.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND SAQICO.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND SAQICO.SERVICE_RECORD_ID = IQ.SERVICE_RECORD_ID AND ISNULL(SAQICO.FABLOCATION_RECORD_ID,'') = ISNULL(IQ.FABLOCATION_RECORD_ID,'') AND SAQICO.GREENBOOK_RECORD_ID = IQ.GREENBOOK_RECORD_ID AND SAQICO.CNTYER = IQ.CNTYER
                            WHERE ISNULL(SAQICO.FABLOCATION_RECORD_ID,'') = '' AND ISNULL(SAQICO.GREENBOOK_RECORD_ID,'') = ''
                            """.format(UserId=self.user_id, UserName=self.user_name, QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id, ancillary_where = ancillary_where, ancillary_join = ancillary_join, YearWiseJoinString = yearwise_join_str)
                    )
                    #INC08675532 #INC08675479 - END - M
                # CR704 - End - M
                #A055S000P01-21072 Start M
                self.update_cntday()
                #A055S000P01-21072 End M
        basic_insert_end = time.time()
        #Trace.Write("Basic Insert Time-----"+str(basic_insert_end-basic_insert_start))
        #Sql.RunQuery("""UPDATE SAQTRV SET REVISION_STATUS = 'CFG-ACQUIRING' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}'""".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id))
        
        #A055S000P01-20577
        Sql.RunQuery("UPDATE A SET A.OFRING = UPPER(CONCAT(B.SERVICE_ID,' - ',B.SERVICE_DESCRIPTION)) FROM SAQICO A JOIN SAQTSV B ON B.SERVICE_RECORD_ID = A.SERVICE_RECORD_ID WHERE A.QUOTE_RECORD_ID = '{QuoteRecordId}' AND A.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND ISNULL(A.OFRING,'') = '' ".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id))
        
        # Update Tool Config
        Sql.RunQuery("""UPDATE SAQICO
                    SET SAQICO.TOLCFG = MAEQUP.TOOL_CONFIGURATION,
                        SAQICO.PRODID = MAEQUP.PRODUCT_ID,
                        SAQICO.EQNODE = MAEQUP.DEVICE_NODE                            
                        FROM SAQICO (NOLOCK)
                        JOIN MAEQUP (NOLOCK) ON MAEQUP.EQUIPMENT_ID = SAQICO.EQUIPMENT_ID
                        WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}'
                        """.format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
                     
        #1574 starts
        #CR713 - Start -M
        if self.quote_service_entitlement_type in ("STR-OFFBGBPMCMKTGCPCND OBJ-AS","STR-OFFBGBSMKTGCPCND OBJ-AS","STR-OFFBGBKTGCPCND OBJ-GPAS","STR-OFFBGBEQ OBJ-EQ"):
            kit_col = 'KIT_NUMBER_RECORD_ID'
            join_cond =''	
            obj_table ='SAQSAP'
            if self.quote_service_entitlement_type in ("STR-OFFBGBPMCMKTGCPCND OBJ-AS","STR-OFFBGBSMKTGCPCND OBJ-AS","STR-OFFBGBKTGCPCND OBJ-GPAS",""):
                kit_col = 'KITNUMBER_RECORD_ID'
                obj_table ='SAQGPA'
                join_cond = " AND {obj_table}.FABLOCATION_ID = SAQICO.FABLOCATION_ID AND {obj_table}.GREENBOOK = SAQICO.GREENBOOK AND SAQGPA.KIT_ID = SAQICO.KIT_ID AND SAQGPA.GOT_CODE = SAQICO.GOT_CODE AND ISNULL(SAQGPA.PROCESS_TYPE,'')= ISNULL(SAQICO.PROCES,'') AND ISNULL(SAQGPA.DEVICE_NODE,'') = ISNULL(SAQICO.DEVICE_NODE,'')".format(obj_table= obj_table)
                if self.quote_service_entitlement_type in ("STR-OFFBGBPMCMKTGCPCND OBJ-AS","STR-OFFBGBSMKTGCPCND OBJ-AS"):
                    join_cond += " AND SAQICO.OBJECT_ID = CASE WHEN SAQICO.OBJECT_ID = 'Scheduled Maintenance' THEN SAQGPA.MNTEVT_LEVEL ELSE SAQGPA.PM_ID END  "	
            Sql.RunQuery("""UPDATE SAQICO SET KIT_NUMBER = {obj_table}.KIT_NUMBER, TKM_RECORD_ID = {obj_table}.{kit_col} FROM SAQICO (NOLOCK) 
            INNER JOIN {obj_table} (NOLOCK) ON {obj_table}.QUOTE_RECORD_ID = SAQICO.QUOTE_RECORD_ID AND {obj_table}.QTEREV_RECORD_ID = SAQICO.QTEREV_RECORD_ID AND {obj_table}.SERVICE_ID = SAQICO.SERVICE_ID  AND {obj_table}.EQUIPMENT_ID = SAQICO.EQUIPMENT_ID {join_cond}
            WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}' AND ISNULL({obj_table}.KIT_ID,'') != '' AND ISNULL({obj_table}.KIT_NUMBER,'') != ''""".format(obj_table = obj_table, QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id, join_cond = join_cond,kit_col =kit_col) )
        #kit number populate ends
        #1574 ends
        #CR713 - End -M
        # Target (Sales) Price Discount %
        Sql.RunQuery("""UPDATE SAQICO
                        SET SADSPC = CONVERT(DECIMAL(18,2),PRCFVA.FACTOR_PCTVAR)		
                            FROM SAQICO (NOLOCK)
                            JOIN PRCFVA (NOLOCK) ON PRCFVA.FACTOR_VARIABLE_ID = SAQICO.SERVICE_ID
                            WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}' AND ISNULL(PRCFVA.FACTOR_ID,'') = 'AISPDP'
                            """.format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
        
        # Target Price Min Margin %
        Sql.RunQuery("""UPDATE SAQICO
                        SET TAPMMP = CONVERT(DECIMAL(18,2),PRCFVA.FACTOR_PCTVAR)		
                            FROM SAQICO (NOLOCK)
                            JOIN PRCFVA (NOLOCK) ON PRCFVA.FACTOR_VARIABLE_ID = SAQICO.SERVICE_ID
                            WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}' AND ISNULL(PRCFVA.FACTOR_ID,'') = 'AITPMM'
                            """.format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
        # BD Price Discount %
        Sql.RunQuery("""UPDATE SAQICO
                        SET BDDSPC = CONVERT(DECIMAL(18,2),PRCFVA.FACTOR_PCTVAR)		
                            FROM SAQICO (NOLOCK)
                            JOIN PRCFVA (NOLOCK) ON PRCFVA.FACTOR_VARIABLE_ID = SAQICO.SERVICE_ID
                            WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}' AND ISNULL(PRCFVA.FACTOR_ID,'') = 'AIBPDP'
                            """.format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
        
        # BD Price Min Margin %
        Sql.RunQuery("""UPDATE SAQICO
                        SET BDPMMP = CONVERT(DECIMAL(18,2),PRCFVA.FACTOR_PCTVAR)		
                            FROM SAQICO (NOLOCK)
                            JOIN PRCFVA (NOLOCK) ON PRCFVA.FACTOR_VARIABLE_ID = SAQICO.SERVICE_ID
                            WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}' AND ISNULL(PRCFVA.FACTOR_ID,'') = 'AIBPMM'
                            """.format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
        
        # Ceiling Price Uplift %
        Sql.RunQuery("""UPDATE SAQICO
                        SET CEPRUP = CONVERT(DECIMAL(18,2),PRCFVA.FACTOR_PCTVAR)		
                            FROM SAQICO (NOLOCK)
                            JOIN PRCFVA (NOLOCK) ON PRCFVA.FACTOR_VARIABLE_ID = SAQICO.SERVICE_ID
                            WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}' AND ISNULL(PRCFVA.FACTOR_ID,'') = 'AICPUP'
                            """.format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))		
        
        #A055S000P01-20909 Start
        # Head Break In Cost Impact
        Sql.RunQuery("""UPDATE SAQICO
                        SET HEDBIC = CONVERT(DECIMAL(18,5),PRCFVA.FACTOR_TXTVAR)		
                            FROM SAQICO (NOLOCK)
                            JOIN MAEQUP (NOLOCK) ON MAEQUP.EQUIPMENT_ID = SAQICO.EQUIPMENT_ID
                            JOIN PRCFVA (NOLOCK) ON PRCFVA.FACTOR_VARIABLE_ID = MAEQUP.SUBSTRATE_SIZE_GROUP
                            WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}' AND SAQICO.HEDBIN = 'Included' AND ISNULL(PRCFVA.FACTOR_ID,'') = 'AIHBCI'
                            """.format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
        
        # Head Break In Price Impact
        Sql.RunQuery("""UPDATE SAQICO
                        SET HEDBIP = CONVERT(DECIMAL(18,5),PRCFVA.FACTOR_TXTVAR)		
                            FROM SAQICO (NOLOCK)
                            JOIN MAEQUP (NOLOCK) ON MAEQUP.EQUIPMENT_ID = SAQICO.EQUIPMENT_ID
                            JOIN PRCFVA (NOLOCK) ON PRCFVA.FACTOR_VARIABLE_ID = MAEQUP.SUBSTRATE_SIZE_GROUP
                            WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}' AND SAQICO.HEDBIN = 'Included' AND ISNULL(PRCFVA.FACTOR_ID,'') = 'AIHBPI'
                            """.format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
        #A055S000P01-20909 End               
        # Sales Price Min Margin %
        Sql.RunQuery("""UPDATE SAQICO
                        SET SAPMMP = CONVERT(DECIMAL(18,2),PRCFVA.FACTOR_TXTVAR)		
                            FROM SAQICO (NOLOCK)							
                            JOIN PRCFVA (NOLOCK) ON PRCFVA.FACTOR_VARIABLE_ID = SAQICO.SERVICE_ID
                            WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}' AND ISNULL(PRCFVA.FACTOR_ID,'') = 'AISPMM' AND SAQICO.SAPMMP IS NULL
                            """.format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))	
        # Contract Period Factor %
        Sql.RunQuery("""UPDATE SAQICO
                        SET CTPDFP = ISNULL(CONTRACT_PERIOD_FACTOR,1)		
                            FROM SAQICO (NOLOCK)							
                            JOIN (SELECT LINE,CONTRACT_PERIOD_FACTOR,SERVICE_ID,QUOTE_RECORD_ID,QTEREV_RECORD_ID,datediff(dd,dateadd(dd,-1,CONTRACT_VALID_FROM),CONTRACT_VALID_TO) as contractdays FROM SAQRIT,PRCTPF WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND datediff(mm,dateadd(dd,-1,CONTRACT_VALID_FROM),CONTRACT_VALID_TO) BETWEEN PERIOD_FROM AND PERIOD_TO)SQ ON SQ.QUOTE_RECORD_ID = SAQICO.QUOTE_RECORD_ID AND SQ.QTEREV_RECORD_ID = SAQICO.QTEREV_RECORD_ID AND SQ.LINE = SAQICO.LINE AND SQ.SERVICE_ID = SAQICO.SERVICE_ID 
                            WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}'
                            """.format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
        # Price Bench Marking 
        # INC08638500 Benchmark Price Deviation % Threshold
        Sql.RunQuery("""UPDATE SAQICO
                        SET SAQICO.BCHDAP = PRCAFC.FACTOR_VALUE		
                            FROM SAQICO (NOLOCK), PRCAFC (NOLOCK) 
                            WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}' AND ISNULL(PRCAFC.FACTOR_ID,'') = 'AIBPDT'
                            """.format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
        # layers cost&price Impact
        EntitlementId = 'AGS_{}_NET_NUMLAY'.format(self.service_id)                
        Sql.RunQuery("""UPDATE SAQICO
                        SET
                        SAQICO.NUMLCI = PREGBV.ENTITLEMENT_COST_IMPACT,
                        SAQICO.NUMLPI = PREGBV.ENTITLEMENT_PRICE_IMPACT
                        FROM SAQICO (NOLOCK) JOIN PREGBV (NOLOCK) ON PREGBV.SERVICE_ID = SAQICO.SERVICE_ID AND PREGBV.GREENBOOK = SAQICO.GREENBOOK AND PREGBV.ENTITLEMENT_DISPLAY_VALUE = SAQICO.NUMLAY WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}' AND PREGBV.ENTITLEMENT_ID = '{EntitlementId}'""".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id,EntitlementId= EntitlementId))                   
        # INC08638500 Benchmark Price Deviation % Threshold
        # Sql.RunQuery("""UPDATE SAQICO
        # 	SET
        # 	SAQICO.BCHPGC = PRPRBM.ANNUALIZED_BOOKING_PRICE,
        # 	SAQICO.BCHDPT = ((SAQICO.TNTVGC - ISNULL(PRPRBM.ANNUALIZED_BOOKING_PRICE,0))/SAQICO.TNTVGC) * 100
        # 	FROM SAQICO	(NOLOCK)
        # 	JOIN PRPRBM (NOLOCK) ON PRPRBM.EQUIPMENT_NUMBER = SAQICO.EQUIPMENT_ID AND PRPRBM.SERVICE_PRODUCT_NAME = SAQICO.SERVICE_ID
        # 	WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}'							
        # 	""".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
        # Sql.RunQuery("""UPDATE SAQICO
        # 	SET
        # 	SAQICO.BCHPGC = PRPRBM.ANNUALIZED_BOOKING_PRICE,
        # 	SAQICO.BCHDPT = ((SAQICO.TNTVGC - ISNULL(PRPRBM.ANNUALIZED_BOOKING_PRICE,0))/SAQICO.TNTVGC) * 100
        # 	FROM SAQICO	(NOLOCK)
        # 	JOIN PRPRBM (NOLOCK) ON PRPRBM.TOOLCONFG = SAQICO.TOLCFG AND PRPRBM.SERVICE_PRODUCT_NAME = SAQICO.SERVICE_ID
        # 	WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}' AND ISNULL(SAQICO.BCHPGC,'')	= ''					
        # 	""".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
        
        # Sql.RunQuery("""UPDATE SAQICO
        # 	SET
        # 	SAQICO.BMPPDA = CASE WHEN ISNULL(BCHDPT,0) > ISNULL(BCHDAP,0) THEN 1 ELSE 0 END
        # 	FROM SAQICO	(NOLOCK)			
        # 	WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}'				
        # 	""".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
        #Item Uptime Improvement Percentage
        Sql.RunQuery("""UPDATE SAQICO
                        SET ITSDUI = ITSDUT - ITSDUB		
                            FROM SAQICO (NOLOCK) 
                            WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}'
                            """.format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
        #item Uptime condition field update
        Sql.RunQuery("""UPDATE SAQICO
                        SET AIUICC = 'False'
                            FROM SAQICO (NOLOCK) 
                            WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}' AND CAST(ITSDUI as NUMERIC(13,3)) > '2.000'
                            """.format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
        # In Warranty
        Trace.Write("===========> In Warranty ++ "+str(self.contract_quote_id)+"=== "+str(self.service_id))
        if self.service_id.endswith("W"):
            Trace.Write("===========> In Warranty ++1111 "+str(self.contract_quote_id)+"=== "+str(self.service_id))
            Sql.RunQuery("""UPDATE SAQICO
                            SET INWRTY = 1		
                                FROM SAQICO (NOLOCK)							
                                WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}'
                                """.format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
        ##value driver value and its coefficient
        self._entitlement_valuedriver()
        
        pricing_46_start = time.time()
        #Z0046 pricing update
        quote_items_list = [] 
        #1417
        if self.service_id == 'Z0046':
            # get_items_entitlement = Sql.GetList("SELECT SAQITE.*,SAQICO.QUOTE_ITEM_COVERED_OBJECT_RECORD_ID FROM SAQITE (NOLOCK) INNER JOIN SAQICO ON SAQITE.QUOTE_RECORD_ID = SAQICO.QUOTE_RECORD_ID AND SAQITE.QTEREV_RECORD_ID = SAQICO.QTEREV_RECORD_ID AND SAQITE.SERVICE_ID = SAQICO.SERVICE_ID AND SAQITE.GREENBOOK  = SAQICO.GREENBOOK AND SAQICO.LINE = SAQITE.LINE WHERE SAQITE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQITE.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQITE.SERVICE_ID = '{ServiceId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
            get_items_entitlement = Sql.GetList("SELECT * FROM SAQITE WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
            for item in get_items_entitlement:
                xml_dict =  self._construct_dict_xml(item.ENTITLEMENT_XML)
                Trace.Write("xml_dict"+str(xml_dict))
                total_price = 0
                for i in range(1,11):
                    x = "AGS_Z0046_PQB_AP{}FU".format(str(i).zfill(2))
                    y = "AGS_Z0046_PQB_AP{}PR".format(str(i).zfill(2))
                    if x in xml_dict.keys() and y in xml_dict.keys() :
                        if xml_dict[x] and xml_dict[y]:
                            qty = float(xml_dict[x])
                            price = float(xml_dict[y])
                            #Trace.Write("ifff-- "+str(qty) +'--'+str(price) )
                            total_price += price * qty
                # Trace.Write("price-- "+str(total_price))
                # Sql.RunQuery("""UPDATE SAQICO 
                #     SET TENVGC = '{total_price}',
                #     TENVDC = {total_price}*IQ.EXCHANGE_RATE
                #     FROM SAQICO (NOLOCK)                         
                #         INNER JOIN (SELECT SAQRIT.QUOTE_RECORD_ID, SAQRIT.QTEREV_RECORD_ID,SAQRIT.SERVICE_ID,SAQRIT.GREENBOOK,SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID,SAQRIT.EXCHANGE_RATE FROM SAQRIT (NOLOCK) WHERE SAQRIT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQRIT.SERVICE_ID = 'Z0046' AND BILLING_TYPE = 'Variable') IQ ON SAQICO.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND SAQICO.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND SAQICO.SERVICE_ID = IQ.SERVICE_ID AND SAQICO.GRNBOK  = IQ.GREENBOOK AND SAQICO.QTEITM_RECORD_ID = IQ.QUOTE_REVISION_CONTRACT_ITEM_ID
                #     WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}' AND SAQICO.GRNBOK = '{greenbook}'""".format( QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id,total_price= total_price,greenbook = item.GREENBOOK,ServiceId= self.service_id))
                get_line_items_values = Sql.GetList("""SELECT QUOTE_ITEM_COVERED_OBJECT_RECORD_ID FROM SAQICO (NOLOCK) 
                        INNER JOIN (SELECT SAQRIT.QUOTE_RECORD_ID, SAQRIT.QTEREV_RECORD_ID,SAQRIT.SERVICE_ID,SAQRIT.GREENBOOK,SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID,SAQRIT.EXCHANGE_RATE FROM SAQRIT (NOLOCK) WHERE SAQRIT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQRIT.SERVICE_ID = 'Z0046' AND BILLING_TYPE = 'Variable') IQ ON SAQICO.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND SAQICO.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND SAQICO.SERVICE_ID = IQ.SERVICE_ID AND SAQICO.GRNBOK  = IQ.GREENBOOK AND SAQICO.QTEITM_RECORD_ID = IQ.QUOTE_REVISION_CONTRACT_ITEM_ID
                    WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}' AND SAQICO.GRNBOK = '{greenbook}'""".format( QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id,greenbook = item.GREENBOOK,ServiceId= self.service_id))
                for line in get_line_items_values:
                    line_dict = {}
                    line_dict[str(line.QUOTE_ITEM_COVERED_OBJECT_RECORD_ID)] = {'AITPNP': str(total_price) }
                    quote_items_list.append(line_dict)
        pricing_46_end = time.time()
        
        Trace.Write("Z0046 Pricing Insert Time-----"+str(pricing_46_end-pricing_46_start))
        if self.service_id == 'Z0116':
            #INC08637742, A055S000P01-21072, INC09167190 - Start - M
            get_line_items_values = Sql.GetList("""SELECT (SAQRCV.CREDIT_APPLIED_INGL_CURR /CASE WHEN DATEDIFF(day,SAQRIT.CONTRACT_VALID_FROM, SAQRIT.CONTRACT_VALID_TO) = 0 THEN 1 ELSE (SELECT SUM(CNTDAY) AS TOTAL_CNTDAY FROM SAQICO A (NOLOCK) WHERE A.QUOTE_RECORD_ID = '{QuoteRecordId}' AND A.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND A.SERVICE_ID = '{ServiceId}' AND A.LINE = B.LINE) END ) * CNTDAY AS PRICE_AMT, QUOTE_ITEM_COVERED_OBJECT_RECORD_ID FROM SAQICO B (NOLOCK)
                 INNER JOIN SAQRIT (NOLOCK) ON B.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND B.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID AND B.SERVICE_ID = SAQRIT.SERVICE_ID AND B.GRNBOK = SAQRIT.GREENBOOK AND B.QTEITM_RECORD_ID = SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID
            INNER JOIN
            (SELECT QUOTE_RECORD_ID, QTEREV_RECORD_ID,SERVICE_ID,GREENBOOK,GL_ACCOUNT_NO,SALESORDER_NO,
            CASE WHEN SUM(ISNULL(CREDIT_APPLIED_INGL_CURR, 0)) < 0 then SUM(ISNULL(CREDIT_APPLIED_INGL_CURR, 0)) else concat('-',SUM(ISNULL(CREDIT_APPLIED_INGL_CURR, 0))) end as CREDIT_APPLIED_INGL_CURR,PAR_SERVICE_ID
            FROM SAQRCV (NOLOCK)
            WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}'
            GROUP BY QUOTE_RECORD_ID, QTEREV_RECORD_ID,SERVICE_ID,GREENBOOK,GL_ACCOUNT_NO,SALESORDER_NO,PAR_SERVICE_ID
            ) SAQRCV ON B.QUOTE_RECORD_ID = SAQRCV.QUOTE_RECORD_ID AND B.QTEREV_RECORD_ID = SAQRCV.QTEREV_RECORD_ID AND B.SERVICE_ID = SAQRCV.SERVICE_ID AND B.GRNBOK = SAQRCV.GREENBOOK AND SAQRCV.GL_ACCOUNT_NO = SAQRIT.GL_ACCOUNT_NO AND SAQRCV.SALESORDER_NO = SAQRIT.REF_SALESORDER AND ISNULL(SAQRCV.PAR_SERVICE_ID,'') = ISNULL(SAQRIT.PAR_PRDOFR_ID,'')
            WHERE B.QUOTE_RECORD_ID = '{QuoteRecordId}' AND B.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND B.SERVICE_ID = '{ServiceId}'""".format( QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId= self.service_id, par_service_id = self.parent_service_id ))
            #INC08637742, INC09167190, A055S000P01-21072 - End - M
            for line in get_line_items_values:
                line_dict = {}
                line_dict[str(line.QUOTE_ITEM_COVERED_OBJECT_RECORD_ID)] = {'AITPNP': str(line.PRICE_AMT) }
                quote_items_list.append(line_dict)
            # Sql.RunQuery("""UPDATE SAQICO 
            #     SET TENVGC  = CONCAT('-',SAQRCV.CREDIT_APPLIED_INGL_CURR), 
            #     TENVDC = Convert(float,CONCAT('-',ISNULL(SAQRCV.CREDIT_APPLIED_INGL_CURR,0))) * SAQRIT.EXCHANGE_RATE 
            #     FROM SAQICO (NOLOCK) 
            #         INNER JOIN SAQRIT (NOLOCK) ON  SAQICO.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND SAQICO.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID AND SAQICO.SERVICE_ID = SAQRIT.SERVICE_ID AND SAQICO.GRNBOK = SAQRIT.GREENBOOK AND SAQICO.QTEITM_RECORD_ID = SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID
            #         INNER JOIN 
            #             (SELECT QUOTE_RECORD_ID, QTEREV_RECORD_ID,SERVICE_ID,GREENBOOK,GL_ACCOUNT_NO,SALESORDER_NO,
            #                 SUM(ISNULL(CREDIT_APPLIED_INGL_CURR, 0)) as CREDIT_APPLIED_INGL_CURR                                     
            #         FROM SAQRCV (NOLOCK)
            #         WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}' 
            #         GROUP BY QUOTE_RECORD_ID, QTEREV_RECORD_ID,SERVICE_ID,GREENBOOK,GL_ACCOUNT_NO,SALESORDER_NO) SAQRCV ON SAQICO.QUOTE_RECORD_ID = SAQRCV.QUOTE_RECORD_ID AND SAQICO.QTEREV_RECORD_ID = SAQRCV.QTEREV_RECORD_ID AND SAQICO.SERVICE_ID = SAQRCV.SERVICE_ID AND SAQICO.GRNBOK  = SAQRCV.GREENBOOK AND SAQRCV.GL_ACCOUNT_NO = SAQRIT.GL_ACCOUNT_NO AND SAQRCV.SALESORDER_NO = SAQRIT.REF_SALESORDER 
            #         WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}' AND UPPER(BILTYP) = 'VARIABLE' """.format( QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId= self.service_id, pricing_field_doc= pricing_field_doc,pricing_field_gl = pricing_field_gl ))
            # Sql.RunQuery("""UPDATE SAQICO 
            #     SET TNTVGC = CONCAT('-',SAQRCV.CREDIT_APPLIED_INGL_CURR), 
            #     TNTVDC = Convert(float,CONCAT('-',ISNULL(SAQRCV.CREDIT_APPLIED_INGL_CURR,0))) * SAQRIT.EXCHANGE_RATE 
            #     FROM SAQICO (NOLOCK) 
            #         INNER JOIN SAQRIT (NOLOCK) ON  SAQICO.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND SAQICO.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID AND SAQICO.SERVICE_ID = SAQRIT.SERVICE_ID AND SAQICO.GRNBOK = SAQRIT.GREENBOOK AND SAQICO.QTEITM_RECORD_ID = SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID
            #         INNER JOIN 
            #             (SELECT QUOTE_RECORD_ID, QTEREV_RECORD_ID,SERVICE_ID,GREENBOOK,GL_ACCOUNT_NO,SALESORDER_NO,
            #                 SUM(ISNULL(CREDIT_APPLIED_INGL_CURR, 0)) as CREDIT_APPLIED_INGL_CURR                                     
            #         FROM SAQRCV (NOLOCK)
            #         WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}' 
            #         GROUP BY QUOTE_RECORD_ID, QTEREV_RECORD_ID,SERVICE_ID,GREENBOOK,GL_ACCOUNT_NO,SALESORDER_NO) SAQRCV ON SAQICO.QUOTE_RECORD_ID = SAQRCV.QUOTE_RECORD_ID AND SAQICO.QTEREV_RECORD_ID = SAQRCV.QTEREV_RECORD_ID AND SAQICO.SERVICE_ID = SAQRCV.SERVICE_ID AND SAQICO.GRNBOK  = SAQRCV.GREENBOOK AND SAQRCV.GL_ACCOUNT_NO = SAQRIT.GL_ACCOUNT_NO AND SAQRCV.SALESORDER_NO = SAQRIT.REF_SALESORDER 
            #         WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}' AND UPPER(BILTYP) <> 'VARIABLE'""".format( QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId= self.service_id, pricing_field_doc= pricing_field_doc,pricing_field_gl = pricing_field_gl ))
        
        elif self.service_id == 'Z0117':
            get_greenbook_record = Sql.GetList("SELECT DISTINCT SAQSGE.GREENBOOK,SAQSGE.ENTITLEMENT_XML,SAQSGE.SERVICE_ID,SAQSGE.PAR_SERVICE_ID,SAQSGE.BILTYP,QUOTE_ITEM_COVERED_OBJECT_RECORD_ID FROM SAQSGE (NOLOCK) JOIN SAQRIT (NOLOCK) ON SAQSGE.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND SAQSGE.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID AND SAQSGE.SERVICE_ID = SAQRIT.SERVICE_ID AND SAQSGE.GREENBOOK = SAQRIT.GREENBOOK AND SAQRIT.PAR_PRDOFR_ID  = SAQSGE.PAR_SERVICE_ID INNER JOIN SAQICO (NOLOCK) ON SAQICO.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND SAQICO.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID AND SAQICO.SERVICE_ID = SAQRIT.SERVICE_ID AND SAQICO.GRNBOK = SAQRIT.GREENBOOK AND SAQICO.QTEITM_RECORD_ID = SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID WHERE SAQSGE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSGE.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQSGE.SERVICE_ID = '{ServiceId}' ".format(QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId= self.service_id))
            tag_pattern = re.compile(r'(<QUOTE_ITEM_ENTITLEMENT>[\w\W]*?</QUOTE_ITEM_ENTITLEMENT>)')
            entitlement_id_tag_pattern = re.compile(r'<ENTITLEMENT_ID>AGS_Z0117_PQB_VCRAMT</ENTITLEMENT_ID>')
            entitlement_display_value_tag_pattern = re.compile(r'<ENTITLEMENT_DISPLAY_VALUE>([^>]*?)</ENTITLEMENT_DISPLAY_VALUE>')
            if get_greenbook_record:
                for record in get_greenbook_record:
                    get_voucher_value = ''
                    for quote_item_tag in re.finditer(tag_pattern, record.ENTITLEMENT_XML):
                        quote_item_tag_content = quote_item_tag.group(1)
                        entitlement_id_tag_match = re.findall(entitlement_id_tag_pattern,quote_item_tag_content)	
                        if entitlement_id_tag_match:
                            entitlement_display_value_tag_match = re.findall(entitlement_display_value_tag_pattern,quote_item_tag_content)
                            if entitlement_display_value_tag_match:
                                get_voucher_value = entitlement_display_value_tag_match[0].upper()
                                break
                    Trace.Write("get_voucher_value-"+str(record.GREENBOOK)+"-"+str(get_voucher_value))
                    if get_voucher_value:
                        line_dict = {}
                        line_dict[str(record.QUOTE_ITEM_COVERED_OBJECT_RECORD_ID)] = {'AITPNP': str(get_voucher_value) }
                        quote_items_list.append(line_dict)
                    #     if record.BILTYP.upper() == 'VARIABLE':
                    #         pricing_field_doc = 'TENVDC'
                    #         pricing_field_gl = 'TENVGC'
                    #     else:
                    #         pricing_field_doc= 'TNTVDC'
                    #         pricing_field_gl = 'TNTVGC'
                    #     Sql.RunQuery("UPDATE SAQICO SET {pricing_field_gl} = '{voucher_amt}', {pricing_field_doc} = '{doc_curr}'  FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}' AND GRNBOK = '{grnbok}' ".format(QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId= self.service_id ,voucher_amt = get_voucher_value, grnbok = record.GREENBOOK, pricing_field_doc = pricing_field_doc, pricing_field_gl =pricing_field_gl, doc_curr = float(get_voucher_value) * float(self.exchange_rate)  ))
                                                    
        elif self.service_id == 'Z0123':
            #1835,2103 starts
            Sql.RunQuery("""UPDATE SAQICO 
                            SET QUANTITY = ROUND(ISNULL(CAST(ISNULL(SAQSCN.QUANTITY,0) AS DECIMAL(7,2) ) /  CASE WHEN DATEDIFF(DD,SAQRIT.CONTRACT_VALID_FROM, SAQRIT.CONTRACT_VALID_TO) < 365 THEN 1 ELSE (CEILING(DATEDIFF(DD,SAQRIT.CONTRACT_VALID_FROM, SAQRIT.CONTRACT_VALID_TO) /365.00)  ) END,0), 2) 
                            FROM SAQICO (NOLOCK) 
                            INNER JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = SAQICO.QUOTE_RECORD_ID AND SAQRIT.QTEREV_RECORD_ID = SAQICO.QTEREV_RECORD_ID AND SAQRIT.SERVICE_ID = SAQICO.SERVICE_ID AND SAQRIT.GREENBOOK  = SAQICO.GREENBOOK AND SAQRIT.EQUIPMENT_ID = SAQICO.EQUIPMENT_ID AND SAQICO.LINE = SAQRIT.LINE
                            INNER JOIN SAQSCN (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = SAQSCN.QUOTE_RECORD_ID AND SAQRIT.QTEREV_RECORD_ID = SAQSCN.QTEREV_RECORD_ID AND SAQRIT.SERVICE_ID = SAQSCN.SERVICE_ID AND SAQRIT.GREENBOOK  = SAQSCN.GREENBOOK AND SAQRIT.EQUIPMENT_ID = SAQSCN.EQUIPMENT_ID AND SAQSCN.POSS_NSO_PART_ID = SAQRIT.POSS_NSO_PART_ID
                            WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}' AND SAQSCN.INCLUDED = 1""".format(QuoteRecordId= self.contract_quote_record_id ,QuoteRevisionRecordId =self.contract_quote_revision_record_id, ServiceId= self.service_id))
            
            #1835,2103 ENDS
            #INC08745555 Start - M
            Sql.RunQuery("""UPDATE SAQRIT 
                            SET QUANTITY = CEILING(SAQICO.QTY)
                            FROM SAQRIT (NOLOCK) 
                                INNER JOIN (SELECT QUOTE_RECORD_ID,QTEREV_RECORD_ID,SERVICE_ID,LINE, SUM(ISNULL(SAQICO.QUANTITY,1)) AS QTY
                                FROM SAQICO (NOLOCK)
                                WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}' 
                                GROUP BY QUOTE_RECORD_ID,QTEREV_RECORD_ID,SERVICE_ID,LINE) SAQICO
                                ON SAQRIT.QUOTE_RECORD_ID = SAQICO.QUOTE_RECORD_ID AND SAQRIT.QTEREV_RECORD_ID = SAQICO.QTEREV_RECORD_ID AND SAQRIT.SERVICE_ID = SAQICO.SERVICE_ID AND SAQICO.LINE = SAQRIT.LINE
                            WHERE SAQRIT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQRIT.SERVICE_ID = '{ServiceId}'""".format(QuoteRecordId= self.contract_quote_record_id ,QuoteRevisionRecordId =self.contract_quote_revision_record_id, ServiceId= self.service_id))
            #INC08745555 End - M
            # 1835,(#1965 starts..)
            #INC08744823 M
            get_line_items_values = Sql.GetList("""SELECT SAQRIT.QUOTE_RECORD_ID, SAQRIT.QTEREV_RECORD_ID, SAQRIT.SERVICE_ID, SAQRIT.GREENBOOK, SAQRIT.FABLOCATION_ID, SAQRIT.EQUIPMENT_ID, SAQSCN.POSS_NSO_PART_ID, SAQSCN.EXTENDED_POSS_PRICE/SAQICO_CNT.CNT AS EXTENDED_POSS_PRICE,  SAQSCN.EXTENDED_POSS_COST/SAQICO_CNT.CNT AS EXTENDED_POSS_COST ,SAQRIT.LINE,SAQICO.QUOTE_ITEM_COVERED_OBJECT_RECORD_ID,SAQICO_CNT.CNT
                            FROM SAQSCN (NOLOCK) 
                            INNER JOIN SAQRIT ON SAQRIT.QUOTE_RECORD_ID = SAQSCN.QUOTE_RECORD_ID AND SAQRIT.QTEREV_RECORD_ID = SAQSCN.QTEREV_RECORD_ID AND SAQRIT.SERVICE_ID = SAQSCN.SERVICE_ID AND SAQRIT.GREENBOOK  = SAQSCN.GREENBOOK AND SAQRIT.EQUIPMENT_ID = SAQSCN.EQUIPMENT_ID AND SAQSCN.POSS_NSO_PART_ID = SAQRIT.POSS_NSO_PART_ID and SAQRIT.FABLOCATION_ID = SAQSCN.FABLOCATION_ID and SAQRIT.BUSINESS_UNIT = SAQSCN.BUSINESS_UNIT
                            INNER JOIN SAQICO ON SAQICO.QUOTE_RECORD_ID = SAQSCN.QUOTE_RECORD_ID AND SAQICO.QTEREV_RECORD_ID = SAQSCN.QTEREV_RECORD_ID AND SAQICO.SERVICE_ID = SAQSCN.SERVICE_ID AND SAQICO.GREENBOOK = SAQSCN.GREENBOOK AND SAQICO.EQUIPMENT_ID = SAQSCN.EQUIPMENT_ID AND SAQICO.LINE = SAQRIT.LINE
                            LEFT JOIN (SELECT COUNT(*) CNT,QUOTE_RECORD_ID,QTEREV_RECORD_ID,SERVICE_ID,LINE,GREENBOOK,EQUIPMENT_ID FROM SAQICO WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}' GROUP BY QUOTE_RECORD_ID,QTEREV_RECORD_ID,SERVICE_ID,LINE,GREENBOOK,EQUIPMENT_ID) SAQICO_CNT ON SAQICO_CNT.QUOTE_RECORD_ID = SAQSCN.QUOTE_RECORD_ID AND SAQICO_CNT.QTEREV_RECORD_ID = SAQSCN.QTEREV_RECORD_ID AND SAQICO_CNT.SERVICE_ID = SAQSCN.SERVICE_ID AND SAQICO_CNT.GREENBOOK = SAQSCN.GREENBOOK AND SAQICO_CNT.EQUIPMENT_ID = SAQSCN.EQUIPMENT_ID AND SAQICO_CNT.LINE = SAQRIT.LINE
            WHERE SAQRIT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQRIT.SERVICE_ID = '{ServiceId}' AND SAQSCN.INCLUDED = 1""".format(QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId= self.service_id, exch_rate = float(self.exchange_rate) ))
            # 1835,(#1945,1365,1323 ends..)
            for line in get_line_items_values:
                line_dict = {}
                line_dict[str(line.QUOTE_ITEM_COVERED_OBJECT_RECORD_ID)] = {'AIPBNC': str(line.EXTENDED_POSS_COST),
                                                                            'AITPNP': str(line.EXTENDED_POSS_PRICE) }
                quote_items_list.append(line_dict)
                # line_dict[str(line.QUOTE_ITEM_COVERED_OBJECT_RECORD_ID)] = {'TCWISS': str(line.EXTENDED_POSS_COST),
                #                         'CNTCST': str(line.EXTENDED_POSS_COST),
                #                         'CNTPRC': str(line.EXTENDED_POSS_PRICE), 
                #                         'TRGPRC': str(line.EXTENDED_POSS_PRICE),
                #                         'USRPRC': str(line.EXTENDED_POSS_PRICE)  }               
        #312 ends
        #calling waterfall
        if self.service_id in ('Z0046','Z0123','Z0116','Z0117','Z0048','Z0101'):	
            for obj in ['SAQICO','SAQRIT']:	
                Sql.RunQuery("UPDATE {obj} SET STATUS = 'ACQUIRED' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}'  ".format(QuoteRecordId= self.contract_quote_record_id ,QuoteRevisionRecordId =self.contract_quote_revision_record_id, ServiceId= self.service_id, obj = obj))
        Log.Info("quote_items_list--->> "+str(quote_items_list))
        if quote_items_list:
            Log.Info("quote_items_list-"+str(quote_items_list))
            calling_waterfall = ScriptExecutor.ExecuteGlobal("CQUPPRWLFD",{"Records":str(quote_items_list),"auto_update_flag":"True"})
            # if self.service_id == 'Z0123':
            # 	Sql.RunQuery("""UPDATE SAQICO SET STATUS = CASE 'ACQUIRED'
                                            
            # 	FROM SAQICO (NOLOCK) 
            # 	WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}'""".format(QuoteRecordId= self.contract_quote_record_id ,QuoteRevisionRecordId =self.contract_quote_revision_record_id, ServiceId= self.service_id))
        # if self.service_id in ('Z0046','Z0123','Z0116','Z0117'):
            # Sql.RunQuery("""UPDATE SAQICO SET STATUS = CASE WHEN isnull(TNTVDC,0) = 0 AND isnull(TENVDC,0) = 0 AND SERVICE_ID = 'Z0046' THEN 'PRR-ON HOLD PRICING' ELSE 'ACQUIRED' END
            # FROM SAQICO (NOLOCK) 
                                                                                                                                                    
            # WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}'""".format( QuoteRecordId= self.contract_quote_record_id ,QuoteRevisionRecordId =self.contract_quote_revision_record_id, ServiceId= self.service_id))
        if self.service_id in ('Z0046','Z0123','Z0116','Z0117','Z0048','Z0101'):
            for obj in ['SAQICO','SAQRIT']:
                Sql.RunQuery("UPDATE {obj} SET STATUS = 'ACQUIRED' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}'  ".format(QuoteRecordId= self.contract_quote_record_id ,QuoteRevisionRecordId =self.contract_quote_revision_record_id, ServiceId= self.service_id, obj = obj))
        #INC08858696-M starts
        if self.service_id in ('Z0103','Z0100'): 
            Sql.RunQuery("UPDATE SAQICO SET STATUS = CASE WHEN SERVICE_ID = 'Z0103' OR (SERVICE_ID ='Z0100' AND CNSMBL_ENT = 'Included') THEN 'OFFLINE PRICING' ELSE 'ACQUIRING' END WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}'  ".format(QuoteRecordId= self.contract_quote_record_id ,QuoteRevisionRecordId =self.contract_quote_revision_record_id, ServiceId= self.service_id ))
        #INC08858696-M ends
            # Sql.RunQuery("""UPDATE SAQICO 
            # 	SET TCWISS = EXTENDED_POSS_COST,
            # 		CNTCST = EXTENDED_POSS_COST,
            # 		CNTPRC = EXTENDED_POSS_PRICE,
            # 		TRGPRC = EXTENDED_POSS_PRICE,
            # 		USRPRC = EXTENDED_POSS_PRICE,
            # 		{pricing_field_gl} = EXTENDED_POSS_PRICE, 
            # 		{pricing_field_doc} = Convert(float,EXTENDED_POSS_PRICE) * {exch_rate}
            # 		FROM SAQICO (NOLOCK) 
            # 		INNER JOIN SAQRIT (NOLOCK) ON  SAQICO.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND SAQICO.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID AND SAQICO.SERVICE_ID = SAQRIT.SERVICE_ID AND SAQICO.GRNBOK = SAQRIT.GREENBOOK AND SAQRIT.EQUIPMENT_ID = SAQICO.EQUPID AND SAQICO.QTEITM_RECORD_ID = SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID
            # 		INNER JOIN  
            # 			(SELECT QUOTE_RECORD_ID, QTEREV_RECORD_ID, SERVICE_ID, GREENBOOK, FABLOCATION_ID, EQUIPMENT_ID, POSS_NSO_PART_ID, EXTENDED_POSS_PRICE, EXTENDED_POSS_COST  
                        
        
            # 				FROM SAQSCN (NOLOCK) 
            # 			WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}'  ) SAQSCN ON SAQRIT.QUOTE_RECORD_ID = SAQSCN.QUOTE_RECORD_ID AND SAQRIT.QTEREV_RECORD_ID = SAQSCN.QTEREV_RECORD_ID AND SAQICO.SERVICE_ID = SAQSCN.SERVICE_ID AND SAQICO.GRNBOK  = SAQSCN.GREENBOOK AND SAQRIT.EQUIPMENT_ID = SAQICO.EQUPID AND SAQSCN.POSS_NSO_PART_ID = SAQRIT.POSS_NSO_PART_ID
            # 		WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}' """.format( QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId= self.service_id, pricing_field_doc= pricing_field_doc,pricing_field_gl = pricing_field_gl, exch_rate = float(self.exchange_rate) ))	
        # elif self.service_id in ('Z0048','Z0101'):
        #     for obj in ['SAQICO','SAQRIT']:
        
        #         Sql.RunQuery("UPDATE {obj} SET STATUS = 'ACQUIRED' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}'  ".format(QuoteRecordId= self.contract_quote_record_id ,QuoteRevisionRecordId =self.contract_quote_revision_record_id, ServiceId= self.service_id, obj = obj))
    
        #SBTCST - Sub Total Cost
                                        
                                
        Sql.RunQuery("UPDATE SAQICO SET SBTCST = ISNULL(TCWISS,0) + (ISNULL(CAVVCI,0) + ISNULL(UIMVCI,0) + ISNULL(ATGKEC,0) + ISNULL(AMNCCI,0) + (ISNULL(TNHRPT,0) * ISNULL(HEDBIC,0)) + ISNULL(NWPTOC,0) + ISNULL(NUMLCI,0) + (ISNULL(TNHRPT,0) *  ISNULL(SPCCLC,0)) + (ISNULL(TNHRPT,0) * ISNULL(SPCCCI,0))) + ISNULL(AIUICI,0) FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
        
        #SBTPRC - Sub Total Price
        Sql.RunQuery("UPDATE SAQICO SET SBTPRC = ISNULL(MTGPRC,0) + (ISNULL(ATGKEP,0) + ISNULL(AMNPPI,0) + ISNULL(CAVVPI,0) + (ISNULL(HEDBIP,0) * ISNULL(TNHRPT,0)) + ISNULL(NWPTOP,0) + ISNULL(NUMLPI,0) + (ISNULL(TNHRPT,0) * ISNULL(SPCCLP,0)) + (ISNULL(TNHRPT,0) * ISNULL(SPCCPI,0)) + ISNULL(UIMVPI,0)) + ISNULL(AIUIPI,0) FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
        # INC08668632 - Start - M
        if self.service_id not in ('Z0048','A6200','Z0101','Z0046','Z0123','Z0116','Z0117'):
            # INC08668632 - End - M
            #AMNCPE - Additional Manual Cost and Price
            Sql.RunQuery("UPDATE SAQICO SET AMNCPE = 1 FROM SAQICO (NOLOCK) JOIN PRSPRV (NOLOCK) ON PRSPRV.SERVICE_ID = SAQICO.SERVICE_ID WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}' AND ISNULL(SAQICO.SBTCST, 0) <= 0 AND ISNULL(SAQICO.SBTPRC, 0) <= 0 AND ISNULL(PRSPRV.SSCM_COST,0) = 0".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
            if self.service_id in ('Z0010','Z0128'):
                Sql.RunQuery("UPDATE SAQICO SET AMNCPE = 1 FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}' AND ISNULL(SAQICO.SBTCST, 0) <= 0 AND ISNULL(SAQICO.SBTPRC, 0) <= 0 AND SAQICO.GREENBOOK IN ('CMP','PPC')".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
            elif self.service_id in ('Z0091','Z0099','Z0035'):
                Sql.RunQuery("UPDATE SAQICO SET AMNCPE = 1 FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}' AND ISNULL(SAQICO.SBTCST, 0) <= 0 AND ISNULL(SAQICO.SBTPRC, 0) <= 0 AND SAQICO.GREENBOOK = 'PDC'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
            #AMNCPI - Additional Manual Cost and Price Complet
                                        
            Sql.RunQuery("UPDATE SAQICO SET AMNCPI = CASE WHEN ISNULL(SAQICO.AMNCPE, 0) = 1 AND (ISNULL(SAQICO.AMNCCI,0) > 0 AND ISNULL(SAQICO.AMNPPI,0) > 0) THEN 'ACTIVE' WHEN ISNULL(SAQICO.AMNCPE, 0) = 1 AND (ISNULL(SAQICO.AMNCCI,0) <= 0 OR ISNULL(SAQICO.AMNPPI,0) <= 0) THEN 'INACTIVE' ELSE null END FROM SAQICO (NOLOCK) JOIN PRSPRV (NOLOCK) ON PRSPRV.SERVICE_ID = SAQICO.SERVICE_ID WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}' AND ISNULL(SAQICO.SBTCST, 0) <= 0 AND ISNULL(SAQICO.SBTPRC, 0) <= 0 AND ISNULL(PRSPRV.SSCM_COST,0) = 0".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
        
            #Status
            if self.service_id != 'Z0100':
                Sql.RunQuery("UPDATE SAQICO SET STATUS = CASE WHEN ISNULL(SAQICO.AMNCPI, '') = 'ACTIVE' AND (ISNULL(SAQICO.AMNCCI,0) > 0 AND ISNULL(SAQICO.AMNPPI,0) > 0) AND (ISNULL(SAQICO.SBTCST, 0) > 0 AND ISNULL(SAQICO.SBTPRC, 0) > 0) THEN 'ACQUIRED' WHEN ISNULL(SAQICO.AMNCPI, '') = 'INACTIVE' AND (ISNULL(SAQICO.AMNCCI,0) <= 0 OR ISNULL(SAQICO.AMNPPI,0) <= 0) AND (ISNULL(SAQICO.SBTCST, 0) <= 0 AND ISNULL(SAQICO.SBTPRC, 0) <= 0) THEN 'OFFLINE PRICING' ELSE SAQICO.STATUS END FROM SAQICO (NOLOCK) JOIN PRSPRV (NOLOCK) ON PRSPRV.SERVICE_ID = SAQICO.SERVICE_ID WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}' AND ISNULL(PRSPRV.SSCM_COST,0) = 0".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id))
                                                        
        if self.service_id in ('Z0010','Z0128','Z0103'):
                                                
            Sql.RunQuery("UPDATE SAQICO SET STATUS = 'OFFLINE PRICING' FROM SAQICO (NOLOCK)  WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND (SAQICO.SERVICE_ID IN ('Z0010','Z0128','Z0103') AND GREENBOOK IN ('CMP','PPC') )   ".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id))
        # if self.quote_service_entitlement_type in ("STR-OFFBGBPMCMKTGCPCND OBJ-AS","","STR-OFFBGBSMKTGCPCND OBJ-AS","STR-OFFBGBKTGCPCND OBJ-GPAS"):
        #     if self.quote_service_entitlement_type in ("STR-OFFBGBKTGCPCND OBJ-GPAS"):
        #         grouping_col = "KIT_ID"
        #     else:
        #         grouping_col = "PM_ID"
        #     #CHAMBER_QUANTITY
        #     Sql.RunQuery("""UPDATE SAQICO SET ITCTAS = CHAMBER_QTY
        #         FROM SAQICO (NOLOCK)
        #             INNER JOIN (SELECT SUM(ISNULL(CHAMBER_QUANTITY,0)) AS CHAMBER_QTY, GOT_CODE, GREENBOOK, {grouping_col}, SERVICE_ID, QUOTE_RECORD_ID, QTEREV_RECORD_ID
        #             FROM SAQGPM (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}' GROUP BY GOT_CODE, GREENBOOK, {grouping_col}, SERVICE_ID, QUOTE_RECORD_ID, QTEREV_RECORD_ID) SAQGPM ON SAQGPM.GOT_CODE = SAQICO.GOT_CODE AND SAQGPM.GREENBOOK =
        #         SAQICO.GREENBOOK AND SAQGPM.{grouping_col} = SAQICO.{grouping_col} AND SAQGPM.SERVICE_ID = SAQICO.SERVICE_ID AND SAQGPM.QUOTE_RECORD_ID = SAQICO.QUOTE_RECORD_ID AND SAQGPM.QTEREV_RECORD_ID = SAQICO.QTEREV_RECORD_ID 
                                    
        #         WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}'""".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id, grouping_col = grouping_col) )
                            
        #     Sql.RunQuery("""UPDATE SAQRIT SET CHAMBER_QUANTITY = CHAMBER_QTY
        #         FROM SAQRIT (NOLOCK)
        #             INNER JOIN (SELECT SUM(ISNULL(ITCTAS,0)) AS CHAMBER_QTY,LINE, SERVICE_ID, QUOTE_RECORD_ID, QTEREV_RECORD_ID
        #             FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}' GROUP BY LINE, SERVICE_ID, QUOTE_RECORD_ID, QTEREV_RECORD_ID) SAQICO ON SAQRIT.LINE = SAQICO.LINE AND SAQICO.SERVICE_ID = SAQRIT.SERVICE_ID AND SAQICO.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND SAQICO.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID 
                                                    
        #         WHERE SAQRIT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQRIT.SERVICE_ID = '{ServiceId}'""".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id) )
        return True
    
    def _quote_items_object_insert(self, update=False):
        join_condition_string = ""
        ancillary_join =""
        ancillary_where =""
        #item_object_where_string = ""
        #item_object_join_string = ""
        if self.quote_service_entitlement_type != 'STR-OFFBGBCRSOGL OBJ-GREQ':
            join_condition_string = ' AND SAQRIT.FABLOCATION_ID = SAQSCO.FABLOCATION_ID '
        if self.quote_service_entitlement_type in ('STR-OFFBGREQPODV OBJ-EQ','STR-OFFBGBEQ OBJ-EQ'):
            join_condition_string += ' AND SAQRIT.EQUIPMENT_ID = SAQSCO.EQUIPMENT_ID '
        #if update:
        
        item_object_where_string = "AND ISNULL(SAQRIO.EQUIPMENT_RECORD_ID,'') = '' "
        item_object_join_string = "LEFT JOIN SAQRIO (NOLOCK) ON SAQRIO.QUOTE_RECORD_ID = SAQSCE.QUOTE_RECORD_ID AND SAQRIO.QTEREV_RECORD_ID = SAQSCE.QTEREV_RECORD_ID AND SAQRIO.SERVICE_RECORD_ID = SAQSCE.SERVICE_RECORD_ID AND SAQRIO.GREENBOOK_RECORD_ID = SAQSCE.GREENBOOK_RECORD_ID AND SAQRIO.EQUIPMENT_RECORD_ID = SAQSCE.EQUIPMENT_RECORD_ID AND SAQRIO.LINE = SAQRIT.LINE"
        # if self.is_ancillary == True or self.addon_product == True:
        # 	ancillary_join = """JOIN SAQRIT (NOLOCK) PAR_SAQRIT ON PAR_SAQRIT.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID 
        # 												AND PAR_SAQRIT.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID 
        # 												AND PAR_SAQRIT.SERVICE_ID =SAQRIT.PAR_SERVICE_ID 
        # 												AND PAR_SAQRIT.SERVICE_ID = '{par_service_id}' 
        # 												AND ISNULL(PAR_SAQRIT.GREENBOOK_RECORD_ID,'') = ISNULL(SAQRIT.GREENBOOK_RECORD_ID,'') 
        # 												AND PAR_SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID = SAQRIT.PARQTEITM_LINE_RECORD_ID """.format(par_service_id = self.parent_service_id)	
        # 	if self.quote_service_entitlement_type in ('OFFERING + EQUIPMENT','OFFERING+EQUIPMENT','OFRNG+EQUIP','STR-OFFBGREQPODV OBJ-EQ'):
        # 		ancillary_join += " AND PAR_SAQRIT.FABLOCATION_RECORD_ID = SAQRIT.FABLOCATION_RECORD_ID AND ISNULL(PAR_SAQRIT.EQUIPMENT_ID,'') = SAQRIT.EQUIPMENT_ID"
        # 	ancillary_where =  " AND PAR_SAQRIT.SERVICE_ID = '{parent_service_id}'".format(parent_service_id = self.parent_service_id)
        #INC08879280 - Start - M
        #A055S000P01-21015 - Start - M
        if self.quote_service_entitlement_type == "STR-OFFBGBPMCMKTGCPCND OBJ-AS":
            Sql.RunQuery("""INSERT SAQRIO (CUSTOMER_TOOL_ID, EQUIPMENT_DESCRIPTION, EQUIPMENT_ID, EQUIPMENT_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID, KPU, LINE, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, QTEITM_RECORD_ID, QUOTE_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, SERIAL_NUMBER, TECHNOLOGY, TOOL_CONFIGURATION, WAFER_SIZE,ASSEMBLY_DESCRIPTION,ASSEMBLY_RECORD_ID,ASSEMBLY_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID, QTESRVCOB_RECORD_ID, QUOTE_REVISION_ITEM_OBJECT_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified)
                    SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REVISION_ITEM_OBJECT_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED,{UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
                    SELECT DISTINCT
                        null as CUSTOMER_TOOL_ID,
                        IQ.EQUIPMENT_DESCRIPTION,					
                        IQ.EQUIPMENT_ID,
                        IQ.EQUIPMENT_RECORD_ID,                        
                        IQ.GREENBOOK, 
                        IQ.GREENBOOK_RECORD_ID,
                        null as KPU,
                        SAQRIT.LINE as LINE,
                        IQ.SERVICE_DESCRIPTION, 
                        IQ.SERVICE_ID, 
                        IQ.SERVICE_RECORD_ID, 
                        SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID, 
                        SAQTRV.QUOTE_ID,
                        SAQTRV.QUOTE_RECORD_ID,
                        SAQTRV.QTEREV_ID,
                        SAQTRV.QTEREV_RECORD_ID,
                        null as SERIAL_NUMBER, 
                        null as TECHNOLOGY, 
                        --PRPRBM.TOOL_CONFIGURATION,
                        null as TOOL_CONFIGURATION,
                        null as WAFER_SIZE,
                        IQ.ASSEMBLY_DESCRIPTION,
                        IQ.ASSEMBLY_RECORD_ID,
                        IQ.ASSEMBLY_ID,
                        IQ.FABLOCATION_ID,
                        IQ.FABLOCATION_NAME,
                        IQ.FABLOCATION_RECORD_ID,
                        IQ.QTESRVCOB_RECORD_ID
                    FROM 
                        (
                            SELECT SAQGPA.SERVICE_ID,SAQGPA.GREENBOOK,SAQGPA.FABLOCATION_ID,SAQGPA.FABLOCATION_NAME,SAQGPA.FABLOCATION_RECORD_ID,SAQGPA.GOT_CODE,SAQGPA.PM_ID,SAQGPA.QUOTE_RECORD_ID,SAQGPA.QTEREV_RECORD_ID,SAQGPA.PM_RECORD_ID,SAQGPA.GOTCODE_RECORD_ID,SAQGPA.EQUIPMENT_ID,SAQGPA.EQUIPMENT_RECORD_ID,SAQGPA.EQUIPMENT_DESCRIPTION,SAQGPA.GREENBOOK_RECORD_ID,SERVICE_DESCRIPTION,SERVICE_RECORD_ID,ISNULL(PROCESS_TYPE,'') AS PROCESS_TYPE , ISNULL(DEVICE_NODE,'') AS DEVICE_NODE,ASSEMBLY_DESCRIPTION,ASSEMBLY_RECORD_ID,ASSEMBLY_ID,KIT_ID,QTESRVCOB_RECORD_ID
                                FROM SAQGPA (NOLOCK)
                                WHERE SAQGPA.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQGPA.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQGPA.SERVICE_ID = '{ServiceId}' 
                                GROUP BY SAQGPA.SERVICE_ID,SAQGPA.GREENBOOK,SAQGPA.FABLOCATION_ID,SAQGPA.FABLOCATION_NAME,SAQGPA.FABLOCATION_RECORD_ID,SAQGPA.GOT_CODE,SAQGPA.PM_ID,SAQGPA.QUOTE_RECORD_ID,SAQGPA.QTEREV_RECORD_ID,SAQGPA.PM_RECORD_ID,SAQGPA.GOTCODE_RECORD_ID,SAQGPA.EQUIPMENT_ID,SAQGPA.EQUIPMENT_RECORD_ID,SAQGPA.EQUIPMENT_DESCRIPTION,SAQGPA.GREENBOOK_RECORD_ID,SERVICE_DESCRIPTION,SERVICE_RECORD_ID, ISNULL(PROCESS_TYPE,'')  , ISNULL(DEVICE_NODE,''),ASSEMBLY_DESCRIPTION,ASSEMBLY_RECORD_ID,ASSEMBLY_ID,KIT_ID,QTESRVCOB_RECORD_ID
                        ) IQ
                        
                        JOIN SAQGPE (NOLOCK) ON SAQGPE.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID  AND SAQGPE.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID  AND IQ.GREENBOOK = SAQGPE.GREENBOOK AND IQ.GOT_CODE = SAQGPE.GOT_CODE AND IQ.PM_ID = SAQGPE.PM_ID AND IQ.SERVICE_ID = SAQGPE.SERVICE_ID AND IQ.KIT_ID = SAQGPE.KIT_ID
                        JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID         
                        JOIN SAQTRV (NOLOCK) ON SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID 
                        JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = SAQTRV.QUOTE_RECORD_ID
                                                AND SAQRIT.SERVICE_RECORD_ID = IQ.SERVICE_RECORD_ID
                                                AND SAQRIT.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID
                                                AND SAQRIT.FABLOCATION_ID = IQ.FABLOCATION_ID
                                                AND SAQRIT.GREENBOOK = IQ.GREENBOOK
                                                AND SAQRIT.OBJECT_ID = IQ.PM_ID
                                                AND SAQRIT.GOT_CODE = IQ.GOT_CODE
                                                AND SAQRIT.KIT_ID = IQ.KIT_ID
                                                AND  ISNULL(SAQRIT.PROCESS_TYPE,'') =  ISNULL(IQ.PROCESS_TYPE,'')
                                                AND  ISNULL(SAQRIT.DEVICE_NODE,'') =  ISNULL(IQ.DEVICE_NODE,'')
                        -- LEFT JOIN PRPRBM (NOLOCK) ON PRPRBM.ACCOUNT_RECORD_ID = SAQTMT.ACCOUNT_RECORD_ID AND PRPRBM.EQUIPMENT_RECORD_ID = IQ.EQUIPMENT_RECORD_ID AND PRPRBM.SERVICE_RECORD_ID = IQ.SERVICE_RECORD_ID		
                        LEFT JOIN SAQRIO (NOLOCK) ON SAQRIO.QUOTE_RECORD_ID = SAQGPE.QUOTE_RECORD_ID AND SAQRIO.QTEREV_RECORD_ID = SAQGPE.QTEREV_RECORD_ID AND SAQRIO.SERVICE_RECORD_ID = IQ.SERVICE_RECORD_ID AND SAQRIO.GREENBOOK_RECORD_ID = SAQGPE.GREENBOOK_RECORD_ID AND SAQRIO.EQUIPMENT_RECORD_ID = IQ.EQUIPMENT_RECORD_ID AND SAQRIO.ASSEMBLY_ID = IQ.ASSEMBLY_ID	AND SAQRIO.QTESRVCOB_RECORD_ID= IQ.QTESRVCOB_RECORD_ID
                        WHERE 
                            IQ.QUOTE_RECORD_ID = '{QuoteRecordId}' AND IQ.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND IQ.SERVICE_ID = '{ServiceId}' AND ISNULL(SAQGPE.CONFIGURATION_STATUS,'') = 'COMPLETE' AND ISNULL(SAQRIO.ASSEMBLY_ID,'') = ''
                        ) IQ
                    """.format(UserId=self.user_id, UserName=self.user_name, QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id,
                    JoinString=item_object_join_string, JoinConditionString=join_condition_string, WhereConditionString=item_object_where_string)
                )		
        elif self.quote_service_entitlement_type in ("STR-OFFBGBSMKTGCPCND OBJ-AS"):
            Sql.RunQuery("""INSERT SAQRIO (CUSTOMER_TOOL_ID, EQUIPMENT_DESCRIPTION, EQUIPMENT_ID, EQUIPMENT_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID, KPU, LINE, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, QTEITM_RECORD_ID, QUOTE_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, SERIAL_NUMBER, TECHNOLOGY, TOOL_CONFIGURATION, WAFER_SIZE,ASSEMBLY_DESCRIPTION,ASSEMBLY_RECORD_ID,ASSEMBLY_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,QTESRVCOB_RECORD_ID, QUOTE_REVISION_ITEM_OBJECT_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified)
                    SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REVISION_ITEM_OBJECT_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED,{UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
                    SELECT DISTINCT
                        null as CUSTOMER_TOOL_ID,
                        IQ.EQUIPMENT_DESCRIPTION,					
                        IQ.EQUIPMENT_ID,
                        IQ.EQUIPMENT_RECORD_ID,                        
                        IQ.GREENBOOK, 
                        IQ.GREENBOOK_RECORD_ID,
                        null as KPU,
                        SAQRIT.LINE as LINE,
                        IQ.SERVICE_DESCRIPTION, 
                        IQ.SERVICE_ID, 
                        IQ.SERVICE_RECORD_ID, 
                        SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID, 
                        SAQTRV.QUOTE_ID,
                        SAQTRV.QUOTE_RECORD_ID,
                        SAQTRV.QTEREV_ID,
                        SAQTRV.QTEREV_RECORD_ID,
                        null as SERIAL_NUMBER, 
                        null as TECHNOLOGY, 
                        --PRPRBM.TOOL_CONFIGURATION,
                        null as TOOL_CONFIGURATION,
                        null as WAFER_SIZE,
                        IQ.ASSEMBLY_DESCRIPTION,
                        IQ.ASSEMBLY_RECORD_ID,
                        IQ.ASSEMBLY_ID,
                        IQ.FABLOCATION_ID,
                        IQ.FABLOCATION_NAME,
                        IQ.FABLOCATION_RECORD_ID,		
                        IQ.QTESRVCOB_RECORD_ID			
                    FROM 
                        (
                            SELECT SAQGPA.SERVICE_ID,SAQGPA.GREENBOOK,SAQGPA.FABLOCATION_ID,SAQGPA.FABLOCATION_NAME,SAQGPA.FABLOCATION_RECORD_ID,SAQGPA.GOT_CODE,SAQGPA.PM_ID,SAQGPA.QUOTE_RECORD_ID,SAQGPA.QTEREV_RECORD_ID,SAQGPA.PM_RECORD_ID,SAQGPA.GOTCODE_RECORD_ID,SAQGPA.EQUIPMENT_ID,SAQGPA.EQUIPMENT_RECORD_ID,SAQGPA.EQUIPMENT_DESCRIPTION,SAQGPA.GREENBOOK_RECORD_ID,SAQGPA.SERVICE_DESCRIPTION,SAQGPA.SERVICE_RECORD_ID,ISNULL(PROCESS_TYPE,'') AS PROCESS_TYPE , ISNULL(DEVICE_NODE,'') AS DEVICE_NODE,CONFIGURATION_STATUS,ASSEMBLY_DESCRIPTION,ASSEMBLY_RECORD_ID,ASSEMBLY_ID,SAQGPA.KIT_ID,QTESRVCOB_RECORD_ID
                                FROM SAQGPA (NOLOCK)
                                JOIN SAQGPE (NOLOCK) ON SAQGPE.QUOTE_RECORD_ID = SAQGPA.QUOTE_RECORD_ID AND SAQGPE.QTEREV_RECORD_ID = SAQGPA.QTEREV_RECORD_ID AND SAQGPE.GREENBOOK = SAQGPA.GREENBOOK AND SAQGPE.GOT_CODE = SAQGPA.GOT_CODE AND SAQGPE.PM_ID  = SAQGPA.PM_ID  AND SAQGPA.SERVICE_ID = SAQGPE.SERVICE_ID AND SAQGPA.KIT_ID = SAQGPE.KIT_ID
                                WHERE SAQGPA.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQGPA.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQGPA.SERVICE_ID = '{ServiceId}' AND MNTEVT_LEVEL != 'Scheduled Maintenance'
                                GROUP BY SAQGPA.SERVICE_ID,SAQGPA.GREENBOOK,SAQGPA.FABLOCATION_ID,SAQGPA.FABLOCATION_NAME,SAQGPA.FABLOCATION_RECORD_ID,SAQGPA.GOT_CODE,SAQGPA.MNTEVT_LEVEL,SAQGPA.QUOTE_RECORD_ID,SAQGPA.QTEREV_RECORD_ID,SAQGPA.PM_RECORD_ID,SAQGPA.GOTCODE_RECORD_ID,SAQGPA.EQUIPMENT_ID,SAQGPA.EQUIPMENT_RECORD_ID,SAQGPA.EQUIPMENT_DESCRIPTION,SAQGPA.GREENBOOK_RECORD_ID,SAQGPA.SERVICE_DESCRIPTION,SAQGPA.SERVICE_RECORD_ID, ISNULL(PROCESS_TYPE,'')  , ISNULL(DEVICE_NODE,''),CONFIGURATION_STATUS,SAQGPA.PM_ID,ASSEMBLY_DESCRIPTION,ASSEMBLY_RECORD_ID,ASSEMBLY_ID,SAQGPA.KIT_ID,QTESRVCOB_RECORD_ID
                            UNION
                            SELECT SAQGPA.SERVICE_ID,SAQGPA.GREENBOOK,SAQGPA.FABLOCATION_ID,SAQGPA.FABLOCATION_NAME,SAQGPA.FABLOCATION_RECORD_ID,SAQGPA.GOT_CODE,SAQGPA.MNTEVT_LEVEL,SAQGPA.QUOTE_RECORD_ID,SAQGPA.QTEREV_RECORD_ID, null as PM_RECORD_ID, SAQGPA.GOTCODE_RECORD_ID,SAQGPA.EQUIPMENT_ID,SAQGPA.EQUIPMENT_RECORD_ID,SAQGPA.EQUIPMENT_DESCRIPTION,SAQGPA.GREENBOOK_RECORD_ID,SAQGPA.SERVICE_DESCRIPTION,SAQGPA.SERVICE_RECORD_ID,ISNULL(PROCESS_TYPE,'') AS PROCESS_TYPE , ISNULL(DEVICE_NODE,'') AS DEVICE_NODE,CONFIGURATION_STATUS,ASSEMBLY_DESCRIPTION,ASSEMBLY_RECORD_ID,ASSEMBLY_ID,SAQGPA.KIT_ID,QTESRVCOB_RECORD_ID
                            FROM SAQGPA (NOLOCK)
                            JOIN SAQSGE SAQGPE (NOLOCK) ON SAQGPE.QUOTE_RECORD_ID = SAQGPA.QUOTE_RECORD_ID AND SAQGPE.QTEREV_RECORD_ID = SAQGPA.QTEREV_RECORD_ID AND SAQGPE.GREENBOOK = SAQGPA.GREENBOOK  AND SAQGPA.SERVICE_ID = SAQGPE.SERVICE_ID
                                WHERE SAQGPA.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQGPA.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQGPA.SERVICE_ID = '{ServiceId}' AND MNTEVT_LEVEL = 'Scheduled Maintenance'
                                GROUP BY SAQGPA.SERVICE_ID,SAQGPA.GREENBOOK,SAQGPA.FABLOCATION_ID,SAQGPA.FABLOCATION_NAME,SAQGPA.FABLOCATION_RECORD_ID,SAQGPA.GOT_CODE,SAQGPA.MNTEVT_LEVEL,SAQGPA.QUOTE_RECORD_ID,SAQGPA.QTEREV_RECORD_ID,SAQGPA.GOTCODE_RECORD_ID,SAQGPA.EQUIPMENT_ID,SAQGPA.EQUIPMENT_RECORD_ID,SAQGPA.EQUIPMENT_DESCRIPTION,SAQGPA.GREENBOOK_RECORD_ID,SAQGPA.SERVICE_DESCRIPTION,SAQGPA.SERVICE_RECORD_ID, ISNULL(PROCESS_TYPE,'')  , ISNULL(DEVICE_NODE,''),CONFIGURATION_STATUS,ASSEMBLY_DESCRIPTION,ASSEMBLY_RECORD_ID,ASSEMBLY_ID,SAQGPA.KIT_ID,QTESRVCOB_RECORD_ID
                        ) IQ
                        
                        
                        JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID         
                        JOIN SAQTRV (NOLOCK) ON SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID 
                        JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = SAQTRV.QUOTE_RECORD_ID
                                                AND SAQRIT.SERVICE_RECORD_ID = IQ.SERVICE_RECORD_ID
                                                AND SAQRIT.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID
                                                AND SAQRIT.FABLOCATION_ID = IQ.FABLOCATION_ID
                                                AND SAQRIT.GREENBOOK = IQ.GREENBOOK
                                                AND SAQRIT.OBJECT_ID = IQ.PM_ID
                                                AND SAQRIT.GOT_CODE = IQ.GOT_CODE
                                                AND SAQRIT.KIT_ID = IQ.KIT_ID
                                                AND  ISNULL(SAQRIT.PROCESS_TYPE,'') =  ISNULL(IQ.PROCESS_TYPE,'')
                                                AND  ISNULL(SAQRIT.DEVICE_NODE,'') =  ISNULL(IQ.DEVICE_NODE,'')
                        -- LEFT JOIN PRPRBM (NOLOCK) ON PRPRBM.ACCOUNT_RECORD_ID = SAQTMT.ACCOUNT_RECORD_ID AND PRPRBM.EQUIPMENT_RECORD_ID = IQ.EQUIPMENT_RECORD_ID AND PRPRBM.SERVICE_RECORD_ID = IQ.SERVICE_RECORD_ID		
                        LEFT JOIN SAQRIO (NOLOCK) ON SAQRIO.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND SAQRIO.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND SAQRIO.SERVICE_RECORD_ID = IQ.SERVICE_RECORD_ID AND SAQRIO.GREENBOOK_RECORD_ID = IQ.GREENBOOK_RECORD_ID AND SAQRIO.EQUIPMENT_RECORD_ID = IQ.EQUIPMENT_RECORD_ID	AND SAQRIO.ASSEMBLY_ID = IQ.ASSEMBLY_ID AND SAQRIO.QTESRVCOB_RECORD_ID= IQ.QTESRVCOB_RECORD_ID
                        WHERE 
                            IQ.QUOTE_RECORD_ID = '{QuoteRecordId}' AND IQ.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND IQ.SERVICE_ID = '{ServiceId}' AND ISNULL(IQ.CONFIGURATION_STATUS,'') = 'COMPLETE' AND ISNULL(SAQRIO.ASSEMBLY_ID,'') = ''
                        ) IQ
                    """.format(UserId=self.user_id, UserName=self.user_name, QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id,
                    JoinString=item_object_join_string, JoinConditionString=join_condition_string, WhereConditionString=item_object_where_string)
                )
        elif self.quote_service_entitlement_type in ('STR-OFFBGBKTGCPCND OBJ-GPAS'):
            Sql.RunQuery("""INSERT SAQRIO (CUSTOMER_TOOL_ID, EQUIPMENT_DESCRIPTION, EQUIPMENT_ID, EQUIPMENT_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID, KPU, LINE, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, QTEITM_RECORD_ID, QUOTE_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, SERIAL_NUMBER, TECHNOLOGY, TOOL_CONFIGURATION, WAFER_SIZE,ASSEMBLY_DESCRIPTION,ASSEMBLY_RECORD_ID, ASSEMBLY_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,QTESRVCOB_RECORD_ID, QUOTE_REVISION_ITEM_OBJECT_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified)
                    SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REVISION_ITEM_OBJECT_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED,{UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
                    SELECT DISTINCT
                        null as CUSTOMER_TOOL_ID,
                        IQ.EQUIPMENT_DESCRIPTION,					
                        IQ.EQUIPMENT_ID,
                        IQ.EQUIPMENT_RECORD_ID,                        
                        IQ.GREENBOOK, 
                        IQ.GREENBOOK_RECORD_ID,
                        null as KPU,
                        SAQRIT.LINE as LINE,
                        IQ.SERVICE_DESCRIPTION, 
                        IQ.SERVICE_ID, 
                        IQ.SERVICE_RECORD_ID, 
                        SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID, 
                        SAQTRV.QUOTE_ID,
                        SAQTRV.QUOTE_RECORD_ID,
                        SAQTRV.QTEREV_ID,
                        SAQTRV.QTEREV_RECORD_ID,
                        null as SERIAL_NUMBER, 
                        null as TECHNOLOGY, 
                        --PRPRBM.TOOL_CONFIGURATION,
                        null as TOOL_CONFIGURATION,
                        null as WAFER_SIZE,
                        IQ.ASSEMBLY_DESCRIPTION,
                        IQ.ASSEMBLY_RECORD_ID,
                        IQ.ASSEMBLY_ID,
                        IQ.FABLOCATION_ID,
                        IQ.FABLOCATION_NAME,
                        IQ.FABLOCATION_RECORD_ID,
                        IQ.QTESRVCOB_RECORD_ID
                    FROM 
                        (
                            SELECT SAQGPA.SERVICE_ID,SAQGPA.GREENBOOK,SAQGPA.FABLOCATION_ID,SAQGPA.FABLOCATION_NAME,SAQGPA.FABLOCATION_RECORD_ID,SAQGPA.GOT_CODE,SAQGPA.KIT_ID,SAQGPA.QUOTE_RECORD_ID,SAQGPA.QTEREV_RECORD_ID,SAQGPA.GOTCODE_RECORD_ID,SAQGPA.EQUIPMENT_ID,SAQGPA.EQUIPMENT_RECORD_ID,SAQGPA.EQUIPMENT_DESCRIPTION,SAQGPA.GREENBOOK_RECORD_ID,SERVICE_DESCRIPTION,SERVICE_RECORD_ID,ISNULL(PROCESS_TYPE,'') AS PROCESS_TYPE , ISNULL(DEVICE_NODE,'') AS DEVICE_NODE,SAQGPA.ASSEMBLY_ID, SAQGPA.ASSEMBLY_DESCRIPTION, SAQGPA.ASSEMBLY_RECORD_ID,QTESRVCOB_RECORD_ID
                                FROM SAQGPA (NOLOCK) 
                                WHERE SAQGPA.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQGPA.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQGPA.SERVICE_ID = '{ServiceId}'  AND ISNULL(SAQGPA.KIT_ID,'') != '' AND INCLUDED =1
                                GROUP BY SAQGPA.SERVICE_ID,SAQGPA.GREENBOOK,SAQGPA.FABLOCATION_ID,SAQGPA.FABLOCATION_NAME,SAQGPA.FABLOCATION_RECORD_ID,SAQGPA.GOT_CODE,SAQGPA.KIT_ID,SAQGPA.QUOTE_RECORD_ID,SAQGPA.QTEREV_RECORD_ID,SAQGPA.GOTCODE_RECORD_ID,SAQGPA.EQUIPMENT_ID,SAQGPA.EQUIPMENT_RECORD_ID,SAQGPA.EQUIPMENT_DESCRIPTION,SAQGPA.GREENBOOK_RECORD_ID,SERVICE_DESCRIPTION,SERVICE_RECORD_ID, ISNULL(PROCESS_TYPE,'')  , ISNULL(DEVICE_NODE,''),SAQGPA.ASSEMBLY_ID, SAQGPA.ASSEMBLY_DESCRIPTION, SAQGPA.ASSEMBLY_RECORD_ID,QTESRVCOB_RECORD_ID
                        ) IQ
                        
                        JOIN SAQGPE (NOLOCK) ON SAQGPE.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID  AND SAQGPE.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID  AND IQ.GREENBOOK = SAQGPE.GREENBOOK AND IQ.GOT_CODE = SAQGPE.GOT_CODE 
                        JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID         
                        JOIN SAQTRV (NOLOCK) ON SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID 
                        JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = SAQTRV.QUOTE_RECORD_ID
                                                AND SAQRIT.SERVICE_RECORD_ID = IQ.SERVICE_RECORD_ID
                                                AND SAQRIT.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID
                                                AND SAQRIT.FABLOCATION_ID = IQ.FABLOCATION_ID
                                                AND SAQRIT.GREENBOOK = IQ.GREENBOOK
                                                AND SAQRIT.KIT_ID = IQ.KIT_ID
                                                AND SAQRIT.GOT_CODE = IQ.GOT_CODE
                                                AND  ISNULL(SAQRIT.PROCESS_TYPE,'') =  ISNULL(IQ.PROCESS_TYPE,'')
                                                AND  ISNULL(SAQRIT.DEVICE_NODE,'') =  ISNULL(IQ.DEVICE_NODE,'')
                        -- LEFT JOIN PRPRBM (NOLOCK) ON PRPRBM.ACCOUNT_RECORD_ID = SAQTMT.ACCOUNT_RECORD_ID AND PRPRBM.EQUIPMENT_RECORD_ID = IQ.EQUIPMENT_RECORD_ID AND PRPRBM.SERVICE_RECORD_ID = IQ.SERVICE_RECORD_ID		
                        LEFT JOIN SAQRIO (NOLOCK) ON SAQRIO.QUOTE_RECORD_ID = SAQGPE.QUOTE_RECORD_ID AND SAQRIO.QTEREV_RECORD_ID = SAQGPE.QTEREV_RECORD_ID AND SAQRIO.SERVICE_RECORD_ID = IQ.SERVICE_RECORD_ID AND SAQRIO.GREENBOOK_RECORD_ID = SAQGPE.GREENBOOK_RECORD_ID AND SAQRIO.EQUIPMENT_RECORD_ID = IQ.EQUIPMENT_RECORD_ID	AND SAQRIO.ASSEMBLY_RECORD_ID = IQ.ASSEMBLY_RECORD_ID AND SAQRIO.QTESRVCOB_RECORD_ID= IQ.QTESRVCOB_RECORD_ID
                        WHERE 
                            IQ.QUOTE_RECORD_ID = '{QuoteRecordId}' AND IQ.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND IQ.SERVICE_ID = '{ServiceId}' AND ISNULL(SAQGPE.CONFIGURATION_STATUS,'') = 'COMPLETE' AND ISNULL(SAQRIO.ASSEMBLY_RECORD_ID,'') = '' 
                        ) IQ
                    """.format(UserId=self.user_id, UserName=self.user_name, QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id,
                    JoinString=item_object_join_string, JoinConditionString=join_condition_string, WhereConditionString=item_object_where_string)
                )
        #A055S000P01-21015 - End - M
        #INC08879280 - End - M
        elif self.quote_service_entitlement_type == 'STR-OFFBGBEQAS OBJ-AS':
            #INC09026574 - Start - M
            Sql.RunQuery("""INSERT SAQRIO (CUSTOMER_TOOL_ID, EQUIPMENT_DESCRIPTION, EQUIPMENT_ID, EQUIPMENT_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID, KPU, LINE, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, QTEITM_RECORD_ID, QUOTE_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, SERIAL_NUMBER, TECHNOLOGY, TOOL_CONFIGURATION, WAFER_SIZE,TEMP_TOOL, ASSEMBLY_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID, QUOTE_REVISION_ITEM_OBJECT_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified)
                    SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REVISION_ITEM_OBJECT_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED,{UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
                    SELECT DISTINCT
                        NULL AS CUSTOMER_TOOL_ID,
                        SAQSCA.EQUIPMENT_DESCRIPTION,					
                        SAQSCA.EQUIPMENT_ID,
                        SAQSCA.EQUIPMENT_RECORD_ID,                        
                        SAQSCA.GREENBOOK, 
                        SAQSCA.GREENBOOK_RECORD_ID,
                        NULL AS KPU,
                        SAQRIT.LINE as LINE,
                        SAQSCA.SERVICE_DESCRIPTION, 
                        SAQSCA.SERVICE_ID, 
                        SAQSCA.SERVICE_RECORD_ID, 
                        SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID, 
                        SAQSCA.QUOTE_ID,
                        SAQSCA.QUOTE_RECORD_ID,
                        SAQSCA.QTEREV_ID,
                        SAQSCA.QTEREV_RECORD_ID,
                        null as SERIAL_NUMBER, 
                        null as TECHNOLOGY, 
                        --PRPRBM.TOOL_CONFIGURATION,
                        null as TOOL_CONFIGURATION,
                        SAQSCO.WAFER_SIZE,
                        SAQSCO.TEMP_TOOL,
                        SAQRIT.ASSEMBLY_ID,
                        SAQSCO.FABLOCATION_ID,
                        SAQSCO.FABLOCATION_NAME,
                        SAQSCO.FABLOCATION_RECORD_ID					
                    FROM 
                        SAQSCA (NOLOCK)	
                        JOIN SAQSCO ON SAQSCO.QUOTE_RECORD_ID = SAQSCA.QUOTE_RECORD_ID AND SAQSCO.SERVICE_ID = SAQSCA.SERVICE_ID AND SAQSCO.QTEREV_RECORD_ID = SAQSCA.QTEREV_RECORD_ID AND SAQSCO.EQUIPMENT_RECORD_ID = SAQSCA.EQUIPMENT_RECORD_ID AND SAQSCO.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID = SAQSCA.QTESRVCOB_RECORD_ID
                        JOIN SAQSAE (NOLOCK) ON SAQSAE.QUOTE_RECORD_ID = SAQSCA.QUOTE_RECORD_ID AND SAQSAE.SERVICE_ID = SAQSCA.SERVICE_ID AND SAQSAE.QTEREV_RECORD_ID = SAQSCA.QTEREV_RECORD_ID 
                        AND SAQSAE.EQUIPMENT_RECORD_ID = SAQSCA.EQUIPMENT_RECORD_ID AND SAQSAE.ASSEMBLY_ID =SAQSCA.ASSEMBLY_ID
                        JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = SAQSCA.QTEREV_RECORD_ID         
                        JOIN SAQTRV (NOLOCK) ON SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID 
                        JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = SAQTRV.QUOTE_RECORD_ID
                                                AND SAQRIT.SERVICE_RECORD_ID = SAQSCO.SERVICE_RECORD_ID
                                                AND SAQRIT.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID
                                                AND SAQRIT.GREENBOOK_RECORD_ID = SAQSCO.GREENBOOK_RECORD_ID
                                                AND SAQRIT.EQUIPMENT_ID = SAQSCA.EQUIPMENT_ID
                                                AND SAQRIT.ASSEMBLY_ID = SAQSCA.ASSEMBLY_ID
                                                AND SAQRIT.FABLOCATION_ID = SAQSCO.FABLOCATION_ID
                                                AND SAQSCO.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID = SAQRIT.QTESRVCOB_RECORD_ID
                        --LEFT JOIN PRPRBM (NOLOCK) ON PRPRBM.ACCOUNT_RECORD_ID = SAQTMT.ACCOUNT_RECORD_ID AND PRPRBM.EQUIPMENT_RECORD_ID = SAQSCO.EQUIPMENT_RECORD_ID AND PRPRBM.SERVICE_RECORD_ID = SAQSCO.SERVICE_RECORD_ID		
                        LEFT JOIN SAQRIO (NOLOCK) ON SAQRIO.QUOTE_RECORD_ID = SAQSAE.QUOTE_RECORD_ID AND SAQRIO.QTEREV_RECORD_ID = SAQSAE.QTEREV_RECORD_ID AND SAQRIO.SERVICE_RECORD_ID = SAQSAE.SERVICE_RECORD_ID AND SAQRIO.GREENBOOK_RECORD_ID = SAQSAE.GREENBOOK_RECORD_ID AND SAQRIO.EQUIPMENT_RECORD_ID = SAQSAE.EQUIPMENT_RECORD_ID AND SAQRIO.ASSEMBLY_ID = SAQSAE.ASSEMBLY_ID				
                    WHERE 
                        SAQSCO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQSCO.SERVICE_ID = '{ServiceId}' AND ISNULL(SAQSAE.CONFIGURATION_STATUS,'') = 'COMPLETE' AND ISNULL(SAQRIO.ASSEMBLY_ID,'') = ''
                    ) IQ
                    """.format(UserId=self.user_id, UserName=self.user_name, QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id,
                    WhereConditionString=item_object_where_string)
                )
        
        else:
            #INC09026574 - Start - M
            Log.Info("====>INSERT SAQRIO===> "+str("""INSERT SAQRIO (CUSTOMER_TOOL_ID, EQUIPMENT_DESCRIPTION, EQUIPMENT_ID, EQUIPMENT_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID, KPU, LINE, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, QTEITM_RECORD_ID, QUOTE_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, SERIAL_NUMBER, TECHNOLOGY, TOOL_CONFIGURATION, WAFER_SIZE,TEMP_TOOL,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID, QUOTE_REVISION_ITEM_OBJECT_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified)
                    SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REVISION_ITEM_OBJECT_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED,{UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
                    SELECT DISTINCT
                        SAQSCO.CUSTOMER_TOOL_ID,
                        SAQSCO.EQUIPMENT_DESCRIPTION,					
                        SAQSCO.EQUIPMENT_ID,
                        SAQSCO.EQUIPMENT_RECORD_ID,                        
                        SAQSCO.GREENBOOK, 
                        SAQSCO.GREENBOOK_RECORD_ID,
                        SAQSCO.KPU,
                        SAQRIT.LINE as LINE,
                        SAQSCO.SERVICE_DESCRIPTION, 
                        SAQSCO.SERVICE_ID, 
                        SAQSCO.SERVICE_RECORD_ID, 
                        SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID, 
                        SAQSCO.QUOTE_ID,
                        SAQSCO.QUOTE_RECORD_ID,
                        SAQSCO.QTEREV_ID,
                        SAQSCO.QTEREV_RECORD_ID,
                        SAQSCO.SERIAL_NO as SERIAL_NUMBER, 
                        SAQSCO.TECHNOLOGY, 
                        --PRPRBM.TOOL_CONFIGURATION,
                        null as TOOL_CONFIGURATION,
                        SAQSCO.WAFER_SIZE,
                        SAQSCO.TEMP_TOOL,
                        SAQSCO.FABLOCATION_ID,
                        SAQSCO.FABLOCATION_NAME,
                        SAQSCO.FABLOCATION_RECORD_ID					
                    FROM 
                        SAQSCO (NOLOCK)					 
                        JOIN SAQSCE (NOLOCK) ON SAQSCE.QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID AND SAQSCE.SERVICE_ID = SAQSCO.SERVICE_ID AND SAQSCE.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID
                        AND SAQSCE.EQUIPMENT_RECORD_ID = SAQSCO.EQUIPMENT_RECORD_ID
                        JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID         
                        JOIN SAQTRV (NOLOCK) ON SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID 
                        JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = SAQTRV.QUOTE_RECORD_ID
                                                AND SAQRIT.SERVICE_RECORD_ID = SAQSCO.SERVICE_RECORD_ID
                                                AND SAQRIT.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID
                                                AND SAQRIT.GREENBOOK_RECORD_ID = SAQSCO.GREENBOOK_RECORD_ID
                                                AND ISNULL(SAQSCO.TEMP_TOOL,'') = ISNULL(SAQRIT.TEMP_TOOL,'')
                                                AND SAQSCE.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID = SAQRIT.QTESRVCOB_RECORD_ID
                                                {JoinConditionString}
                        LEFT JOIN SAQRIT (NOLOCK) SAQRIT_SELF ON SAQRIT_SELF.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID
                                                AND SAQRIT_SELF.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID
                                                AND SAQRIT_SELF.LINE = SAQRIT.PARQTEITM_LINE
                        --LEFT JOIN PRPRBM (NOLOCK) ON PRPRBM.ACCOUNT_RECORD_ID = SAQTMT.ACCOUNT_RECORD_ID AND PRPRBM.EQUIPMENT_RECORD_ID = SAQSCO.EQUIPMENT_RECORD_ID AND PRPRBM.SERVICE_RECORD_ID = SAQSCO.SERVICE_RECORD_ID
                        {ancillary_join}		
                        {JoinString}					
                    WHERE 
                        SAQSCO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQSCO.SERVICE_ID = '{ServiceId}' AND ISNULL(SAQSCE.CONFIGURATION_STATUS,'') = 'COMPLETE' {WhereConditionString} {ancillary_where}
                    ) IQ
                    """.format(UserId=self.user_id, UserName=self.user_name, QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id,
                    JoinString=item_object_join_string, JoinConditionString=join_condition_string, WhereConditionString=item_object_where_string, ancillary_where =ancillary_where, ancillary_join= ancillary_join)
                ))
            Sql.RunQuery("""INSERT SAQRIO (CUSTOMER_TOOL_ID, EQUIPMENT_DESCRIPTION, EQUIPMENT_ID, EQUIPMENT_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID, KPU, LINE, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, QTEITM_RECORD_ID, QUOTE_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, SERIAL_NUMBER, TECHNOLOGY, TOOL_CONFIGURATION, WAFER_SIZE,TEMP_TOOL,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID, QUOTE_REVISION_ITEM_OBJECT_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified)
                    SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REVISION_ITEM_OBJECT_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED,{UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
                    SELECT DISTINCT
                        SAQSCO.CUSTOMER_TOOL_ID,
                        SAQSCO.EQUIPMENT_DESCRIPTION,					
                        SAQSCO.EQUIPMENT_ID,
                        SAQSCO.EQUIPMENT_RECORD_ID,                        
                        SAQSCO.GREENBOOK, 
                        SAQSCO.GREENBOOK_RECORD_ID,
                        SAQSCO.KPU,
                        SAQRIT.LINE as LINE,
                        SAQSCO.SERVICE_DESCRIPTION, 
                        SAQSCO.SERVICE_ID, 
                        SAQSCO.SERVICE_RECORD_ID, 
                        SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID, 
                        SAQSCO.QUOTE_ID,
                        SAQSCO.QUOTE_RECORD_ID,
                        SAQSCO.QTEREV_ID,
                        SAQSCO.QTEREV_RECORD_ID,
                        SAQSCO.SERIAL_NO as SERIAL_NUMBER, 
                        SAQSCO.TECHNOLOGY, 
                        --PRPRBM.TOOL_CONFIGURATION,
                        null as TOOL_CONFIGURATION,
                        SAQSCO.WAFER_SIZE,
                        SAQSCO.TEMP_TOOL,
                        SAQSCO.FABLOCATION_ID,
                        SAQSCO.FABLOCATION_NAME,
                        SAQSCO.FABLOCATION_RECORD_ID					
                    FROM 
                        SAQSCO (NOLOCK)					 
                        JOIN SAQSCE (NOLOCK) ON SAQSCE.QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID AND SAQSCE.SERVICE_ID = SAQSCO.SERVICE_ID AND SAQSCE.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID
                        AND SAQSCE.EQUIPMENT_RECORD_ID = SAQSCO.EQUIPMENT_RECORD_ID
                        JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID         
                        JOIN SAQTRV (NOLOCK) ON SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID 
                        JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = SAQTRV.QUOTE_RECORD_ID
                                                AND SAQRIT.SERVICE_RECORD_ID = SAQSCO.SERVICE_RECORD_ID
                                                AND SAQRIT.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID
                                                AND SAQRIT.GREENBOOK_RECORD_ID = SAQSCO.GREENBOOK_RECORD_ID
                                                AND ISNULL(SAQSCO.TEMP_TOOL,'') = ISNULL(SAQRIT.TEMP_TOOL,'')
                                                AND SAQSCE.QTESRVCOB_RECORD_ID = SAQRIT.QTESRVCOB_RECORD_ID
                                                {JoinConditionString}
                        LEFT JOIN SAQRIT (NOLOCK) SAQRIT_SELF ON SAQRIT_SELF.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID
                                                AND SAQRIT_SELF.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID
                                                AND SAQRIT_SELF.LINE = SAQRIT.PARQTEITM_LINE
                        --LEFT JOIN PRPRBM (NOLOCK) ON PRPRBM.ACCOUNT_RECORD_ID = SAQTMT.ACCOUNT_RECORD_ID AND PRPRBM.EQUIPMENT_RECORD_ID = SAQSCO.EQUIPMENT_RECORD_ID AND PRPRBM.SERVICE_RECORD_ID = SAQSCO.SERVICE_RECORD_ID
                        {ancillary_join}		
                        {JoinString}					
                    WHERE 
                        SAQSCO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQSCO.SERVICE_ID = '{ServiceId}' AND ISNULL(SAQSCE.CONFIGURATION_STATUS,'') = 'COMPLETE' {WhereConditionString} {ancillary_where}
                    ) IQ
                    """.format(UserId=self.user_id, UserName=self.user_name, QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id,
                    JoinString=item_object_join_string, JoinConditionString=join_condition_string, WhereConditionString=item_object_where_string, ancillary_where =ancillary_where, ancillary_join= ancillary_join)
                )
            #INC09026574 - End - M
        ##update quantity in SAQRIT
        if self.quote_service_entitlement_type not in ('STR-OFFBGBSMKTGCPCND OBJ-AS','STR-OFFBGBPMCMKTGCPCND OBJ-AS','STR-OFFBGREQPODV OBJ-EQ','STR-OFFBGBEQ OBJ-EQ','STR-OFFBGBKTGCPCND OBJ-GPAS'):
            self._quote_item_qty_update()
    def _quote_items_entitlement_insert(self, update=False):		
        join_condition_string = ''
        ancillary_join =""
        ancillary_where =""
        dynamic_group_id_value = 'null as ENTITLEMENT_GROUP_ID'
        dynamic_is_changed_value = 'null as IS_CHANGED'
        if self.quote_service_entitlement_type in ('STR-OFFBGBEQ OBJ-EQ'):
            join_condition_string = ' AND SAQRIT.FABLOCATION_RECORD_ID = {ObjectName}.FABLOCATION_RECORD_ID AND SAQRIT.OBJECT_ID = {ObjectName}.EQUIPMENT_ID AND SAQRIT.QTESRVCOB_RECORD_ID = {ObjectName}.QTESRVCOB_RECORD_ID '.format(ObjectName=self.source_object_name)
            dynamic_group_id_value = '{ObjectName}.ENTITLEMENT_GROUP_ID'.format(ObjectName=self.source_object_name)
            dynamic_is_changed_value = '{ObjectName}.IS_CHANGED'.format(ObjectName=self.source_object_name)
        elif self.quote_service_entitlement_type == 'STR-OFFBGBEQAS OBJ-AS':
            
            join_condition_string = ' AND SAQRIT.FABLOCATION_RECORD_ID = {ObjectName}.FABLOCATION_RECORD_ID AND SAQRIT.ASSEMBLY_ID = {ObjectName}.ASSEMBLY_ID AND SAQRIT.EQUIPMENT_ID = {ObjectName}.EQUIPMENT_ID  INNER JOIN SAQSCE ON SAQRIT.QTESRVCOB_RECORD_ID = SAQSCE.QTESRVCOB_RECORD_ID AND SAQSCE.EQUIPMENT_ID = SAQSAE.EQUIPMENT_ID and SAQRIT.FABLOCATION_RECORD_ID = SAQSCE.FABLOCATION_RECORD_ID AND QTESRVCOE_RECORD_ID = QUOTE_SERVICE_COVERED_OBJ_ENTITLEMENTS_RECORD_ID '.format(ObjectName=self.source_object_name)
            
        # if self.is_ancillary == True or self.addon_product == True:
        # 	ancillary_join = """JOIN SAQRIT (NOLOCK) PAR_SAQRIT ON PAR_SAQRIT.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID 
        # 												AND PAR_SAQRIT.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID 
        # 												AND PAR_SAQRIT.SERVICE_ID =SAQRIT.PAR_SERVICE_ID 
        # 												AND PAR_SAQRIT.SERVICE_ID = '{par_service_id}' 
        # 												AND ISNULL(PAR_SAQRIT.GREENBOOK_RECORD_ID,'') = ISNULL(SAQRIT.GREENBOOK_RECORD_ID,'') 
        # 												AND PAR_SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID = SAQRIT.PARQTEITM_LINE_RECORD_ID """.format(par_service_id = self.parent_service_id)	
        # 	if self.quote_service_entitlement_type in ('OFFERING + EQUIPMENT','OFFERING+EQUIPMENT','OFRNG+EQUIP','STR-OFFBGREQPODV OBJ-EQ'):
        # 		ancillary_join += " AND PAR_SAQRIT.FABLOCATION_RECORD_ID = SAQRIT.FABLOCATION_RECORD_ID AND ISNULL(PAR_SAQRIT.EQUIPMENT_ID,'') = SAQRIT.EQUIPMENT_ID"
        # 	ancillary_where =  " AND PAR_SAQRIT.SERVICE_ID = '{parent_service_id}'".format(parent_service_id = self.parent_service_id)
        
        #if update: # need to verify one more time
        Sql.RunQuery("DELETE SAQITE FROM SAQITE WHERE SAQITE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQITE.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQITE.SERVICE_ID = '{ServiceId}'".format(QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
        if self.quote_service_entitlement_type in ('STR-OFFBGREQPODV OBJ-EQ','STR-OFFBGBEQ OBJ-EQ'):
            #INC09026574 - Start - M
            Sql.RunQuery("""INSERT SAQITE (QUOTE_REV_ITEM_ENTITLEMENT_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified, CPS_CONFIGURATION_ID, CPS_MATCH_ID, ENTITLEMENT_COST_IMPACT, ENTITLEMENT_GROUP_ID, ENTITLEMENT_GROUP_XML, ENTITLEMENT_PRICE_IMPACT, ENTITLEMENT_XML, IS_CHANGED, LINE, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, QTEITM_RECORD_ID, QUOTE_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID,BASE_FEE,BILLING_CONDITION,BILLING_CYCLE,LOW_QTY_PART,CONCOV,COO_RED_GUAR,COMMIT_CONSIGNED_PART,COMMIT_REQUEST_PART,CUST_PURCH_COMMIT,FORECAST_REDIS_FREQ,FORECAST_ADJ_FREQ,IDLE_DURATION,IDLE_NOTICE,IDLING_EXCEP,KPI_ON_REQUEST,KPI_MONTHLY_CON,MAX_OF_TOOLS,MISC_TERM,ONSITE_CONSPRT,WAF_SPEC_INP,CREDIT_CONSIGNED_PART,CREDIT_NTE_CON,CREDIT_NTE_REQ,CREDIT_REQUEST_PART,PM_QTY_CRD,RPRCUS_OWNPRT,REPONSE_TIME,SCHEDULE_PART,SOFT_MNT_FEE,UNSCHEDULED_PART,WARM_HOT_IDLE,SRV_SPT_ENT,SPR_SPT_ENT,PARTS_BURN_DOWN,PARTS_BUY_BACK,ADDITIONAL_TGTKPI,BONUS_PEN_TIED_KPI,CONSUMABLE,LMT_PARTS_PAY,NEW_PARTS_ONLY,NON_CONSUMABLE,PRICE_CRITICAL_PARAM,PRIMARY_KPI,PROCESS_PARTS_KITS_CLEAN_RECY,RESPONSE_TIME,SPLIT_QUOTE,SWAP_KITS_AMAT_PROVIDED,WET_CLEAN_LABOR,SOFTWARE_SUPPORT,INSTALL_T3,PSE_SUPPORT,NOT_EXCEEDVAL,DECONTAMINATION,CUST_COMMIT_SCHED_PARTS,COMMIT_OR_PTS_METHOD,QUOTE_TYPE,BILLING_TYPE )
                        SELECT
                            CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REV_ITEM_ENTITLEMENT_RECORD_ID,
                            '{UserName}' AS CPQTABLEENTRYADDEDBY,
                            GETDATE() as CPQTABLEENTRYDATEADDED,
                            {UserId} as CpqTableEntryModifiedBy,
                            GETDATE() as CpqTableEntryDateModified,
                            {ObjectName}.CPS_CONFIGURATION_ID,
                            {ObjectName}.CPS_MATCH_ID,
                            null as ENTITLEMENT_COST_IMPACT,
                            {dynamic_group_id_value},
                            null as ENTITLEMENT_GROUP_XML,
                            null as ENTITLEMENT_PRICE_IMPACT,
                            {ObjectName}.ENTITLEMENT_XML,
                            {dynamic_is_changed_value},
                            SAQRIT.LINE,						
                            SAQRIT.SERVICE_DESCRIPTION,
                            SAQRIT.SERVICE_ID,
                            SAQRIT.SERVICE_RECORD_ID,
                            SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID,						
                            SAQRIT.QUOTE_ID,
                            SAQRIT.QUOTE_RECORD_ID,
                            SAQRIT.QTEREV_ID,
                            SAQRIT.QTEREV_RECORD_ID,						
                            SAQRIT.GREENBOOK,
                            SAQRIT.GREENBOOK_RECORD_ID,
                            {ObjectName}.BASE_FEE,
                            {ObjectName}.BILLING_CONDITION,
                            {ObjectName}.BILLING_CYCLE,
                            {ObjectName}.LOW_QTY_PART,
                            {ObjectName}.CONCOV,
                            {ObjectName}.COO_RED_GUAR,
                            {ObjectName}.COMMIT_CONSIGNED_PART,
                            {ObjectName}.COMMIT_REQUEST_PART,
                            {ObjectName}.CUST_PURCH_COMMIT,
                            {ObjectName}.FORECAST_REDIS_FREQ,
                            {ObjectName}.FORECAST_ADJ_FREQ,
                            {ObjectName}.IDLE_DURATION,
                            {ObjectName}.IDLE_NOTICE,
                            {ObjectName}.IDLING_EXCEP,
                            {ObjectName}.KPI_ON_REQUEST,
                            {ObjectName}.KPI_MONTHLY_CON,
                            {ObjectName}.MAX_OF_TOOLS,
                            {ObjectName}.MISC_TERM,
                            {ObjectName}.ONSITE_CONSPRT,
                            {ObjectName}.WAF_SPEC_INP,
                            {ObjectName}.CREDIT_CONSIGNED_PART,
                            {ObjectName}.CREDIT_NTE_CON,
                            {ObjectName}.CREDIT_NTE_REQ,
                            {ObjectName}.CREDIT_REQUEST_PART,
                            {ObjectName}.PM_QTY_CRD,
                            {ObjectName}.RPRCUS_OWNPRT,
                            {ObjectName}.REPONSE_TIME,
                            {ObjectName}.SCHEDULE_PART,
                            {ObjectName}.SOFT_MNT_FEE,
                            {ObjectName}.UNSCHEDULED_PART,
                            {ObjectName}.WARM_HOT_IDLE,
                            {ObjectName}.SRV_SPT_ENT,
                            {ObjectName}.SPR_SPT_ENT,
                            {ObjectName}.PARTS_BURN_DOWN,
                            {ObjectName}.PARTS_BUY_BACK,
                            {ObjectName}.ATGKEY,
                            {ObjectName}.BPTKPI,
                            {ObjectName}.CNSMBL_ENT,
                            {ObjectName}.LMT_PARTS_PAY,
                            {ObjectName}.NWPTON,
                            {ObjectName}.NCNSMB_ENT,
                            {ObjectName}.PRICE_CRITICAL_PARAM,
                            {ObjectName}.PRMKPI_ENT,
                            {ObjectName}.PROCESS_PARTS_KITS_CLEAN_RECY,
                            {ObjectName}.REPONSE_TIME AS RESPONSE_TIME,
                            {ObjectName}.SPQTEV,
                            {ObjectName}.SWPKTA,
                            {ObjectName}.WETCLN_ENT,
                            {ObjectName}.SOFTWARE_SUPPORT,
                            {ObjectName}.INSTALL_T3,
                            {ObjectName}.PSE_SUPPORT,
                            {ObjectName}.NOT_EXCEEDVAL,
                            {ObjectName}.DECONTAMINATION,
                            {ObjectName}.CUST_COMMIT_SCHED_PARTS,
                            {ObjectName}.COMMIT_OR_PTS_METHOD,
                            {ObjectName}.QTETYP,
                            {ObjectName}.BILTYP 
                        FROM (SELECT SAQRIT.* FROM SAQSCO 
                                INNER JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID
                                AND SAQRIT.SERVICE_RECORD_ID = SAQSCO.SERVICE_RECORD_ID
                                AND SAQRIT.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID	
                                AND ISNULL(SAQRIT.GREENBOOK_RECORD_ID,'') = ISNULL(SAQSCO.GREENBOOK_RECORD_ID,'')
                                AND ISNULL(SAQSCO.TEMP_TOOL,'') = ISNULL(SAQRIT.TEMP_TOOL,'')
                                AND SAQRIT.FABLOCATION_RECORD_ID = SAQSCO.FABLOCATION_RECORD_ID AND SAQRIT.EQUIPMENT_ID = SAQSCO.EQUIPMENT_ID
                                AND QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID = SAQRIT.QTESRVCOB_RECORD_ID
                                WHERE SAQSCO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQSCO.SERVICE_ID = '{ServiceId}'
                        ) SAQRIT
                        JOIN {ObjectName} (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = {ObjectName}.QUOTE_RECORD_ID
                                                    AND SAQRIT.SERVICE_RECORD_ID = {ObjectName}.SERVICE_RECORD_ID
                                                    AND SAQRIT.QTEREV_RECORD_ID = {ObjectName}.QTEREV_RECORD_ID	
                                                    AND ISNULL(SAQRIT.GREENBOOK_RECORD_ID,'') = ISNULL({ObjectName}.GREENBOOK_RECORD_ID,'')
                                                    AND SAQRIT.QTESRVCOB_RECORD_ID = {ObjectName}.QTESRVCOB_RECORD_ID
                                                    {JoinConditionString}			
                        {ancillary_join}
                        WHERE {ObjectName}.QUOTE_RECORD_ID = '{QuoteRecordId}' AND {ObjectName}.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND {ObjectName}.SERVICE_ID = '{ServiceId}' AND ISNULL({ObjectName}.CONFIGURATION_STATUS,'') = 'COMPLETE'	{ancillary_where}	
                    """.format(UserId=self.user_id, UserName=self.user_name, ObjectName=self.source_object_name, QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id, JoinConditionString=join_condition_string, dynamic_is_changed_value = dynamic_is_changed_value, dynamic_group_id_value = dynamic_group_id_value, ancillary_join = ancillary_join , ancillary_where = ancillary_where))
            #INC09026574 - End - M
        else:
            #INC09026574 - Start - M
            Sql.RunQuery("""INSERT SAQITE (QUOTE_REV_ITEM_ENTITLEMENT_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified, CPS_CONFIGURATION_ID, CPS_MATCH_ID, ENTITLEMENT_COST_IMPACT, ENTITLEMENT_GROUP_ID, ENTITLEMENT_GROUP_XML, ENTITLEMENT_PRICE_IMPACT, ENTITLEMENT_XML, IS_CHANGED, LINE, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, QTEITM_RECORD_ID, QUOTE_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID,BASE_FEE,BILLING_CONDITION,BILLING_CYCLE,LOW_QTY_PART,CONCOV,COO_RED_GUAR,COMMIT_CONSIGNED_PART,COMMIT_REQUEST_PART,CUST_PURCH_COMMIT,FORECAST_REDIS_FREQ,FORECAST_ADJ_FREQ,IDLE_DURATION,IDLE_NOTICE,IDLING_EXCEP,KPI_ON_REQUEST,KPI_MONTHLY_CON,MAX_OF_TOOLS,MISC_TERM,ONSITE_CONSPRT,WAF_SPEC_INP,CREDIT_CONSIGNED_PART,CREDIT_NTE_CON,CREDIT_NTE_REQ,CREDIT_REQUEST_PART,PM_QTY_CRD,RPRCUS_OWNPRT,REPONSE_TIME,SCHEDULE_PART,SOFT_MNT_FEE,UNSCHEDULED_PART,WARM_HOT_IDLE,SRV_SPT_ENT,SPR_SPT_ENT,PARTS_BURN_DOWN,PARTS_BUY_BACK,ADDITIONAL_TGTKPI,BONUS_PEN_TIED_KPI,CONSUMABLE,LMT_PARTS_PAY,NEW_PARTS_ONLY,NON_CONSUMABLE,PRICE_CRITICAL_PARAM,PRIMARY_KPI,PROCESS_PARTS_KITS_CLEAN_RECY,RESPONSE_TIME,SPLIT_QUOTE,SWAP_KITS_AMAT_PROVIDED,WET_CLEAN_LABOR,SOFTWARE_SUPPORT,INSTALL_T3,PSE_SUPPORT,NOT_EXCEEDVAL,DECONTAMINATION,CUST_COMMIT_SCHED_PARTS,COMMIT_OR_PTS_METHOD,QUOTE_TYPE,BILLING_TYPE)
                        SELECT
                            CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REV_ITEM_ENTITLEMENT_RECORD_ID,
                            '{UserName}' AS CPQTABLEENTRYADDEDBY,
                            GETDATE() as CPQTABLEENTRYDATEADDED,
                            {UserId} as CpqTableEntryModifiedBy,
                            GETDATE() as CpqTableEntryDateModified,
                            {ObjectName}.CPS_CONFIGURATION_ID,
                            {ObjectName}.CPS_MATCH_ID,
                            null as ENTITLEMENT_COST_IMPACT,
                            {dynamic_group_id_value},
                            null as ENTITLEMENT_GROUP_XML,
                            null as ENTITLEMENT_PRICE_IMPACT,
                            {ObjectName}.ENTITLEMENT_XML,
                            {dynamic_is_changed_value},
                            SAQRIT.LINE,						
                            SAQRIT.SERVICE_DESCRIPTION,
                            SAQRIT.SERVICE_ID,
                            SAQRIT.SERVICE_RECORD_ID,
                            SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID,						
                            SAQRIT.QUOTE_ID,
                            SAQRIT.QUOTE_RECORD_ID,
                            SAQRIT.QTEREV_ID,
                            SAQRIT.QTEREV_RECORD_ID,						
                            SAQRIT.GREENBOOK,
                            SAQRIT.GREENBOOK_RECORD_ID,
                            {ObjectName}.BASE_FEE,
                            {ObjectName}.BILLING_CONDITION,
                            {ObjectName}.BILLING_CYCLE,
                            {ObjectName}.LOW_QTY_PART,
                            {ObjectName}.CONCOV,
                            {ObjectName}.COO_RED_GUAR,
                            {ObjectName}.COMMIT_CONSIGNED_PART,
                            {ObjectName}.COMMIT_REQUEST_PART,
                            {ObjectName}.CUST_PURCH_COMMIT,
                            {ObjectName}.FORECAST_REDIS_FREQ,
                            {ObjectName}.FORECAST_ADJ_FREQ,
                            {ObjectName}.IDLE_DURATION,
                            {ObjectName}.IDLE_NOTICE,
                            {ObjectName}.IDLING_EXCEP,
                            {ObjectName}.KPI_ON_REQUEST,
                            {ObjectName}.KPI_MONTHLY_CON,
                            {ObjectName}.MAX_OF_TOOLS,
                            {ObjectName}.MISC_TERM,
                            {ObjectName}.ONSITE_CONSPRT,
                            {ObjectName}.WAF_SPEC_INP,
                            {ObjectName}.CREDIT_CONSIGNED_PART,
                            {ObjectName}.CREDIT_NTE_CON,
                            {ObjectName}.CREDIT_NTE_REQ,
                            {ObjectName}.CREDIT_REQUEST_PART,
                            {ObjectName}.PM_QTY_CRD,
                            {ObjectName}.RPRCUS_OWNPRT,
                            {ObjectName}.REPONSE_TIME,
                            {ObjectName}.SCHEDULE_PART,
                            {ObjectName}.SOFT_MNT_FEE,
                            {ObjectName}.UNSCHEDULED_PART,
                            {ObjectName}.WARM_HOT_IDLE,
                            {ObjectName}.SRV_SPT_ENT,
                            {ObjectName}.SPR_SPT_ENT,
                            {ObjectName}.PARTS_BURN_DOWN,
                            {ObjectName}.PARTS_BUY_BACK,
                            {ObjectName}.ATGKEY,
                            {ObjectName}.BPTKPI,
                            {ObjectName}.CNSMBL_ENT,
                            {ObjectName}.LMT_PARTS_PAY,
                            {ObjectName}.NWPTON,
                            {ObjectName}.NCNSMB_ENT,
                            {ObjectName}.PRICE_CRITICAL_PARAM,
                            {ObjectName}.PRMKPI_ENT,
                            {ObjectName}.PROCESS_PARTS_KITS_CLEAN_RECY,
                            {ObjectName}.REPONSE_TIME AS RESPONSE_TIME,
                            {ObjectName}.SPQTEV,
                            {ObjectName}.SWPKTA,
                            {ObjectName}.WETCLN_ENT,
                            {ObjectName}.SOFTWARE_SUPPORT,
                            {ObjectName}.INSTALL_T3,
                            {ObjectName}.PSE_SUPPORT,
                            {ObjectName}.NOT_EXCEEDVAL,
                            {ObjectName}.DECONTAMINATION,
                            {ObjectName}.CUST_COMMIT_SCHED_PARTS,
                            {ObjectName}.COMMIT_OR_PTS_METHOD,
                            {ObjectName}.QTETYP,
                            {ObjectName}.BILTYP
                        FROM {ObjectName} (NOLOCK) 
                        JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = {ObjectName}.QUOTE_RECORD_ID
                                                    AND SAQRIT.SERVICE_RECORD_ID = {ObjectName}.SERVICE_RECORD_ID
                                                    AND SAQRIT.QTEREV_RECORD_ID = {ObjectName}.QTEREV_RECORD_ID	
                                                    AND ISNULL(SAQRIT.GREENBOOK_RECORD_ID,'') = ISNULL({ObjectName}.GREENBOOK_RECORD_ID,'')
                                                    {JoinConditionString}	
                        {ancillary_join}		
                        WHERE {ObjectName}.QUOTE_RECORD_ID = '{QuoteRecordId}' AND {ObjectName}.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND {ObjectName}.SERVICE_ID = '{ServiceId}' AND ISNULL({ObjectName}.CONFIGURATION_STATUS,'') = 'COMPLETE'	{ancillary_where}		
                    """.format(UserId=self.user_id, UserName=self.user_name, ObjectName=self.source_object_name, QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id, JoinConditionString=join_condition_string, dynamic_is_changed_value = dynamic_is_changed_value, dynamic_group_id_value = dynamic_group_id_value, ancillary_join =ancillary_join, ancillary_where = ancillary_where))
            #INC09026574 - End - M
        return True
    def _quote_items_fpm_entitlement_insert(self, update=False):		
        join_condition_string = ''
        dynamic_group_id_value = 'null as ENTITLEMENT_GROUP_ID'
        dynamic_is_changed_value = 'null as IS_CHANGED'
        # if self.quote_service_entitlement_type in ('OFFERING + EQUIPMENT','OFFERING+EQUIPMENT'):
        # 	join_condition_string = ' AND SAQRIT.FABLOCATION_RECORD_ID = {ObjectName}.FABLOCATION_RECORD_ID AND SAQRIT.OBJECT_ID = {ObjectName}.EQUIPMENT_ID'.format(ObjectName=self.source_object_name)
        # 	dynamic_group_id_value = '{ObjectName}.ENTITLEMENT_GROUP_ID'.format(ObjectName=self.source_object_name)
        # 	dynamic_is_changed_value = '{ObjectName}.IS_CHANGED'.format(ObjectName=self.source_object_name)
        #if update: # need to verify one more time
        Sql.RunQuery("DELETE SAQITE FROM SAQITE WHERE SAQITE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQITE.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQITE.SERVICE_ID = '{ServiceId}'".format(QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
        Log.Info("===> INSERT SAQITE ===> "+str("""INSERT SAQITE (QUOTE_REV_ITEM_ENTITLEMENT_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified, CPS_CONFIGURATION_ID, CPS_MATCH_ID, ENTITLEMENT_COST_IMPACT, ENTITLEMENT_GROUP_ID, ENTITLEMENT_GROUP_XML, ENTITLEMENT_PRICE_IMPACT, ENTITLEMENT_XML, IS_CHANGED, LINE, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, QTEITM_RECORD_ID, QUOTE_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID)
                    SELECT
                        CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REV_ITEM_ENTITLEMENT_RECORD_ID,
                        '{UserName}' AS CPQTABLEENTRYADDEDBY,
                        GETDATE() as CPQTABLEENTRYDATEADDED,
                        {UserId} as CpqTableEntryModifiedBy,
                        GETDATE() as CpqTableEntryDateModified,
                        {ObjectName}.CPS_CONFIGURATION_ID,
                        {ObjectName}.CPS_MATCH_ID,
                        null as ENTITLEMENT_COST_IMPACT,
                        {dynamic_group_id_value},
                        null as ENTITLEMENT_GROUP_XML,
                        null as ENTITLEMENT_PRICE_IMPACT,
                        {ObjectName}.ENTITLEMENT_XML,
                        {dynamic_is_changed_value},
                        SAQRIT.LINE,						
                        SAQRIT.SERVICE_DESCRIPTION,
                        SAQRIT.SERVICE_ID,
                        SAQRIT.SERVICE_RECORD_ID,
                        SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID,						
                        SAQRIT.QUOTE_ID,
                        SAQRIT.QUOTE_RECORD_ID,
                        SAQRIT.QTEREV_ID,
                        SAQRIT.QTEREV_RECORD_ID						
                    FROM {ObjectName} (NOLOCK) 
                    JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = {ObjectName}.QUOTE_RECORD_ID
                                                AND SAQRIT.SERVICE_ID = {ObjectName}.SERVICE_ID
                                                AND SAQRIT.QTEREV_RECORD_ID = {ObjectName}.QTEREV_RECORD_ID		
                                                {JoinConditionString}			
                    WHERE {ObjectName}.QUOTE_RECORD_ID = '{QuoteRecordId}' AND {ObjectName}.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND {ObjectName}.SERVICE_ID = '{ServiceId}' AND ISNULL({ObjectName}.CONFIGURATION_STATUS,'') = 'COMPLETE'			
                """.format(UserId=self.user_id, UserName=self.user_name, ObjectName=self.source_object_name, QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id, JoinConditionString=join_condition_string, dynamic_is_changed_value = dynamic_is_changed_value, dynamic_group_id_value = dynamic_group_id_value)))
        Sql.RunQuery("""INSERT SAQITE (QUOTE_REV_ITEM_ENTITLEMENT_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified, CPS_CONFIGURATION_ID, CPS_MATCH_ID, ENTITLEMENT_COST_IMPACT, ENTITLEMENT_GROUP_ID, ENTITLEMENT_GROUP_XML, ENTITLEMENT_PRICE_IMPACT, ENTITLEMENT_XML, IS_CHANGED, LINE, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, QTEITM_RECORD_ID, QUOTE_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID,CUST_COMMIT_SCHED_PARTS,FCST_ADJ_PER_YEAR,SCHEDULE_PART,UNSCHEDULED_PART,LOW_QTY_PARTS,COMMIT_CONSIGNED_PART,COMMIT_COSGN_PTS_METHOD,COMMIT_REQUEST_PTS,COMMIT_OR_PTS_METHOD,FCST_REDIST_PER_YEAR,KPI_ON_REQST_DAYS,KPI_MONTH_CONSIGN,ONSITE_CONSPRT,CREDIT_CONSIGNED_PART,CREDIT_NTE_CON,CREDIT_NTE_REQ,CREDIT_REQUEST_PART)
                    SELECT
                        CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REV_ITEM_ENTITLEMENT_RECORD_ID,
                        '{UserName}' AS CPQTABLEENTRYADDEDBY,
                        GETDATE() as CPQTABLEENTRYDATEADDED,
                        {UserId} as CpqTableEntryModifiedBy,
                        GETDATE() as CpqTableEntryDateModified,
                        {ObjectName}.CPS_CONFIGURATION_ID,
                        {ObjectName}.CPS_MATCH_ID,
                        null as ENTITLEMENT_COST_IMPACT,
                        {dynamic_group_id_value},
                        null as ENTITLEMENT_GROUP_XML,
                        null as ENTITLEMENT_PRICE_IMPACT,
                        {ObjectName}.ENTITLEMENT_XML,
                        {dynamic_is_changed_value},
                        SAQRIT.LINE,						
                        SAQRIT.SERVICE_DESCRIPTION,
                        SAQRIT.SERVICE_ID,
                        SAQRIT.SERVICE_RECORD_ID,
                        SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID,						
                        SAQRIT.QUOTE_ID,
                        SAQRIT.QUOTE_RECORD_ID,
                        SAQRIT.QTEREV_ID,
                        SAQRIT.QTEREV_RECORD_ID,
                        {ObjectName}.CUST_COMMIT_SCHED_PARTS,
                        {ObjectName}.FCST_ADJ_PER_YEAR,
                        {ObjectName}.SCHEDULE_PART,
                        {ObjectName}.UNSCHEDULED_PART,
                        {ObjectName}.LOW_QTY_PARTS,
                        {ObjectName}.COMMIT_CONSIGNED_PART,
                        CONVERT(VARCHAR(80),{ObjectName}.COMMIT_COSGN_PTS_METHOD) AS COMMIT_COSGN_PTS_METHOD,
                        {ObjectName}.COMMIT_REQUEST_PTS,
                        {ObjectName}.COMMIT_OR_PTS_METHOD,
                        {ObjectName}.FCST_REDIST_PER_YEAR,
                        {ObjectName}.KPI_ON_REQST_DAYS,
                        {ObjectName}.KPI_MONTH_CONSIGN,
                        {ObjectName}.ONSITE_CONSPRT,
                        {ObjectName}.CREDIT_CONSIGNED_PART,
                        {ObjectName}.CREDIT_NTE_CON,
                        {ObjectName}.CREDIT_NTE_REQ,
                        {ObjectName}.CREDIT_REQUEST_PART
                    FROM {ObjectName} (NOLOCK) 
                    JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = {ObjectName}.QUOTE_RECORD_ID
                                                AND SAQRIT.SERVICE_ID = {ObjectName}.SERVICE_ID
                                                AND SAQRIT.QTEREV_RECORD_ID = {ObjectName}.QTEREV_RECORD_ID	
                                                {JoinConditionString}			
                    WHERE {ObjectName}.QUOTE_RECORD_ID = '{QuoteRecordId}' AND {ObjectName}.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND {ObjectName}.SERVICE_ID = '{ServiceId}' AND ISNULL({ObjectName}.CONFIGURATION_STATUS,'') = 'COMPLETE'			
                """.format(UserId=self.user_id, UserName=self.user_name, ObjectName=self.source_object_name, QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id, JoinConditionString=join_condition_string, dynamic_is_changed_value = dynamic_is_changed_value, dynamic_group_id_value = dynamic_group_id_value))
        return True
    def _ordering_item_line_no(self):
        doctype_obj = Sql.GetFirst("SELECT ITEM_NUMBER_INCREMENT FROM SAQTRV LEFT JOIN SADOTY ON SADOTY.DOCTYPE_ID=SAQTRV.DOCTYP_ID WHERE SAQTRV.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQTRV.QTEREV_RECORD_ID = '{RevisionRecordId}'".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id))
        if doctype_obj:
            item_number_inc = int(doctype_obj.ITEM_NUMBER_INCREMENT)
            Log.Info("item_number_inc--"+str(item_number_inc)+'-'+str(self.contract_quote_revision_record_id))
            
        check_saqrit_record = Sql.GetFirst("SELECT CpqTableEntryId FROM SAQRIT (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' ".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id))
        if check_saqrit_record:
            Sql.RunQuery("""UPDATE SAQRIT SET LINE  = IQ.line_order from SAQRIT (NOLOCK) INNER JOIN (SELECT CpqTableEntryId,ROW_NUMBER()OVER(ORDER BY(CpqTableEntryId)) * {itemnumberinc} as line_order FROM SAQRIT (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' ) IQ on IQ.CpqTableEntryId = SAQRIT.CpqTableEntryId  WHERE SAQRIT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID = '{RevisionRecordId}' """.format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id,itemnumberinc=item_number_inc))
            Log.Info("""UPDATE SAQRIT SET LINE  = IQ.line_order from SAQRIT (NOLOCK) INNER JOIN (SELECT CpqTableEntryId,ROW_NUMBER()OVER(ORDER BY(CpqTableEntryId)) * {itemnumberinc} as line_order FROM SAQRIT (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' ) IQ on IQ.CpqTableEntryId = SAQRIT.CpqTableEntryId  WHERE SAQRIT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID = '{RevisionRecordId}' """.format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id,itemnumberinc=item_number_inc))
            for obj in ['SAQICO','SAQRIO','SAQITE','SAQRIP','SAQIFP','SAQIBP']:
                Sql.RunQuery("""UPDATE {obj} SET LINE  = SAQRIT.LINE from {obj} (NOLOCK) INNER JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = {obj}.QUOTE_RECORD_ID AND {obj}.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID AND QTEITM_RECORD_ID = QUOTE_REVISION_CONTRACT_ITEM_ID WHERE SAQRIT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID = '{RevisionRecordId}' """.format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id, obj=obj))
            # if self.is_ancillary == True or self.addon_product == True:
            # 	Sql.RunQuery("""UPDATE SAQRIT SET SAQRIT.PARQTEITM_LINE  = PAR_SAQRIT.LINE from SAQRIT (NOLOCK) INNER JOIN SAQRIT (NOLOCK) PAR_SAQRIT ON SAQRIT.QUOTE_RECORD_ID = PAR_SAQRIT.QUOTE_RECORD_ID AND PAR_SAQRIT.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID AND PAR_SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID = SAQRIT.PARQTEITM_LINE_RECORD_ID WHERE SAQRIT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID = '{RevisionRecordId}'""".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id, obj=obj))
        
    def _set_quote_service_entitlement_type(self):              
        ##chk ancillary offering
        check_ancillary = Sql.GetFirst("SELECT PAR_SERVICE_ID FROM SAQTSV (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' and SERVICE_ID = '{ServiceId}' ".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id))
        if check_ancillary:
            if check_ancillary.PAR_SERVICE_ID:
                self.parent_service_id = check_ancillary.PAR_SERVICE_ID
        
        where_str = " QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' and SERVICE_ID = '{ServiceId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id)
        
        service_entitlement_obj = Sql.GetFirst("""SELECT SERVICE_ID, ENTITLEMENT_XML FROM  {obj_name} (NOLOCK) WHERE {where_str}""".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id, obj_name = self.entitlement_level_obj, where_str = where_str))
        if service_entitlement_obj:
            quote_item_tag_pattern = re.compile(r'(<QUOTE_ITEM_ENTITLEMENT>[\w\W]*?</QUOTE_ITEM_ENTITLEMENT>)')
            entitlement_id_tag_pattern = re.compile(r'<ENTITLEMENT_ID>AGS_'+str(self.service_id)+'_PQB_QTITST</ENTITLEMENT_ID>')
            entitlement_display_value_tag_pattern = re.compile(r'<ENTITLEMENT_DISPLAY_VALUE>([^>]*?)</ENTITLEMENT_DISPLAY_VALUE>')
            for quote_item_tag in re.finditer(quote_item_tag_pattern, service_entitlement_obj.ENTITLEMENT_XML):
                quote_item_tag_content = quote_item_tag.group(1)
                entitlement_id_tag_match = re.findall(entitlement_id_tag_pattern,quote_item_tag_content)	
                
                if entitlement_id_tag_match:
                    entitlement_display_value_tag_match = re.findall(entitlement_display_value_tag_pattern,quote_item_tag_content)
                    if entitlement_display_value_tag_match:
                        self.quote_service_entitlement_type = entitlement_display_value_tag_match[0].upper()                    
                        Trace.Write("---self.quote_service_entitlement_type"+str(self.quote_service_entitlement_type))
                        if self.quote_service_entitlement_type in ('STR-OFFBGREQPODV OBJ-EQ','STR-OFFBGBEQ OBJ-EQ'):
                            Trace.Write("---===self.quote_service_entitlement_type"+str(self.quote_service_entitlement_type))
                            self.source_object_name = 'SAQSCE'
                        elif self.quote_service_entitlement_type in ('STR-OFFBGB OBJ-GREQ PRD-GRPT','STR-OFFBGB OBJ-GREQ','STR-OFFBGB OBJ-EQ','STR-OFFBGR OBJ-GREQ','STR-OFFBGB OBJ-ASKT','STR-OFFBGBCRSOGL OBJ-GREQ'):
                            self.source_object_name = 'SAQSGE'
                        elif self.quote_service_entitlement_type in ('OFFERING+CONSIGNED+ON REQUEST','STR-OF PRD-GRPT'):
                            self.source_object_name = 'SAQTSE'
                        elif self.quote_service_entitlement_type in ('STR-OFFBGBPMCMKTGCPCND OBJ-AS','STR-OFFBGBSMKTGCPCND OBJ-AS','STR-OFFBGBKTGCPCND OBJ-GPAS'):
                            self.source_object_name = 'SAQGPE'
                        elif self.quote_service_entitlement_type == 'STR-OFFBGBEQAS OBJ-AS':
                            self.source_object_name = 'SAQSAE'
                        break				
                else:
                    continue
    
            Log.Info(str(self.contract_quote_id)+"_set_quote_service_entitlement_type ===> 2"+str(self.quote_service_entitlement_type))
    def _quote_items_summary_insert(self, update=False):
        Trace.Write("==============>>> "+str(self.source_object_name))
        if self.source_object_name:	
            item_summary_where_string = " AND ISNULL(SAQRIS.SERVICE_RECORD_ID,'') = '' "
            item_summary_join_string = "LEFT JOIN SAQRIS (NOLOCK) ON SAQRIS.QUOTE_RECORD_ID = {ObjectName}.QUOTE_RECORD_ID AND SAQRIS.QTEREV_RECORD_ID = {ObjectName}.QTEREV_RECORD_ID AND SAQRIS.SERVICE_RECORD_ID = {ObjectName}.SERVICE_RECORD_ID".format(ObjectName=self.source_object_name)	
            summary_last_line_no = 0
            quote_item_summary_obj = Sql.GetFirst("SELECT TOP 1 LINE FROM SAQRIS (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' ORDER BY LINE DESC".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id))
            if quote_item_summary_obj:
                summary_last_line_no = int(quote_item_summary_obj.LINE) 	
            #Trace.Write('###--->Inside Quote items summary insert function###')
            Log.Info("===> INSERT SAQRIS ===> "+str("""INSERT SAQRIS (CONTRACT_VALID_FROM, CONTRACT_VALID_TO, DIVISION_ID, DIVISION_RECORD_ID, DOC_CURRENCY, DOCCURR_RECORD_ID, GLOBAL_CURRENCY, GLOBAL_CURRENCY_RECORD_ID, PLANT_ID, PLANT_RECORD_ID, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, QUANTITY, QUOTE_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, LINE, QUOTE_REV_ITEM_SUMMARY_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified)
                SELECT IQ.*, ROW_NUMBER()OVER(ORDER BY(IQ.SERVICE_ID)) + {ItemSummaryLastLineNo} as LINE, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REV_ITEM_SUMMARY_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED,{UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
                    SELECT DISTINCT
                        SAQTRV.CONTRACT_VALID_FROM,
                        SAQTRV.CONTRACT_VALID_TO,
                        SAQTRV.DIVISION_ID,
                        SAQTRV.DIVISION_RECORD_ID,
                        SAQTRV.DOC_CURRENCY,
                        SAQTRV.DOCCURR_RECORD_ID,
                        SAQTRV.GLOBAL_CURRENCY,
                        SAQTRV.GLOBAL_CURRENCY_RECORD_ID,						
                        MAMSOP.PLANT_ID,
                        MAMSOP.PLANT_RECORD_ID,
                        {ObjectName}.SERVICE_DESCRIPTION,
                        {ObjectName}.SERVICE_ID,
                        {ObjectName}.SERVICE_RECORD_ID,						
                        1 as QUANTITY,
                        SAQTRV.QUOTE_ID,
                        SAQTRV.QUOTE_RECORD_ID,
                        SAQTMT.QTEREV_ID,
                        SAQTMT.QTEREV_RECORD_ID
                                                    
                    FROM {ObjectName} (NOLOCK) 
                    JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = {ObjectName}.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = {ObjectName}.QTEREV_RECORD_ID     
                    JOIN SAQTRV (NOLOCK) ON SAQTRV.SALESORG_RECORD_ID = {ObjectName}.SALESORG_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = {ObjectName}.QTEREV_RECORD_ID AND SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID
                                                                                                                                                                                                                                                                                                                                                                            
                    LEFT JOIN MAMSOP (NOLOCK) ON MAMSOP.SAP_PART_NUMBER = {ObjectName}.SERVICE_ID AND MAMSOP.SALESORG_ID = SAQTRV.SALESORG_ID AND MAMSOP.DISTRIBUTIONCHANNEL_ID = SAQTRV.DISTRIBUTIONCHANNEL_ID			
                    {JoinString}
                    WHERE {ObjectName}.QUOTE_RECORD_ID = '{QuoteRecordId}' AND {ObjectName}.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND {ObjectName}.SERVICE_ID = '{ServiceId}' AND ISNULL({ObjectName}.CONFIGURATION_STATUS,'') = 'COMPLETE' {WhereConditionString}) IQ			
            """.format(UserId=self.user_id, UserName=self.user_name, ObjectName=self.source_object_name, QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id, ItemSummaryLastLineNo=summary_last_line_no, WhereConditionString=item_summary_where_string, JoinString=item_summary_join_string)))
            #INC08862424 - Start - M
            Sql.RunQuery("""INSERT SAQRIS (CONTRACT_VALID_FROM, CONTRACT_VALID_TO, DIVISION_ID, DIVISION_RECORD_ID, DOC_CURRENCY, DOCCURR_RECORD_ID, GLOBAL_CURRENCY, GLOBAL_CURRENCY_RECORD_ID, PLANT_ID, PLANT_RECORD_ID, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID,PAR_SERVICE_DESCRIPTION,PAR_SERVICE_ID,PAR_SERVICE_RECORD_ID, QUANTITY, QUOTE_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, BILLING_TYPE, LINE, QUOTE_REV_ITEM_SUMMARY_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified)
                SELECT IQ.*, ROW_NUMBER()OVER(ORDER BY(IQ.SERVICE_ID)) + {ItemSummaryLastLineNo} as LINE, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REV_ITEM_SUMMARY_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED,{UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
                    SELECT DISTINCT
                        SAQTSV.CONTRACT_VALID_FROM,
                        SAQTSV.CONTRACT_VALID_TO,
                        SAQTRV.DIVISION_ID,
                        SAQTRV.DIVISION_RECORD_ID,
                        SAQTRV.DOC_CURRENCY,
                        SAQTRV.DOCCURR_RECORD_ID,
                        SAQTRV.GLOBAL_CURRENCY,
                        SAQTRV.GLOBAL_CURRENCY_RECORD_ID,						
                        MAMSOP.PLANT_ID,
                        MAMSOP.PLANT_RECORD_ID,
                        {ObjectName}.SERVICE_DESCRIPTION,
                        {ObjectName}.SERVICE_ID,
                        {ObjectName}.SERVICE_RECORD_ID,	
                        SAQTSV.PAR_SERVICE_DESCRIPTION,
                        SAQTSV.PAR_SERVICE_ID,
                        SAQTSV.PAR_SERVICE_RECORD_ID,						
                        1 as QUANTITY,
                        SAQTRV.QUOTE_ID,
                        SAQTRV.QUOTE_RECORD_ID,
                        SAQTMT.QTEREV_ID,
                        SAQTMT.QTEREV_RECORD_ID,
                        '{BillingType}' as BILLING_TYPE
                    FROM {ObjectName} (NOLOCK)
                    JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = {ObjectName}.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = {ObjectName}.QTEREV_RECORD_ID     
                    JOIN SAQTRV (NOLOCK) ON SAQTRV.SALESORG_RECORD_ID = {ObjectName}.SALESORG_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = {ObjectName}.QTEREV_RECORD_ID AND SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID
                    JOIN SAQTSV (NOLOCK) ON SAQTSV.QTEREV_RECORD_ID = SAQTRV.QUOTE_REVISION_RECORD_ID AND SAQTSV.QUOTE_RECORD_ID = SAQTRV.QUOTE_RECORD_ID AND SAQTSV.SERVICE_ID = {ObjectName}.SERVICE_ID AND ISNULL(SAQTSV.PAR_SERVICE_ID,'') = ISNULL({ObjectName}.PAR_SERVICE_ID,'')
                    LEFT JOIN MAMSOP (NOLOCK) ON MAMSOP.SAP_PART_NUMBER = {ObjectName}.SERVICE_ID AND MAMSOP.SALESORG_ID = SAQTRV.SALESORG_ID AND MAMSOP.DISTRIBUTIONCHANNEL_ID = SAQTRV.DISTRIBUTIONCHANNEL_ID			
                    {JoinString}
                    WHERE {ObjectName}.QUOTE_RECORD_ID = '{QuoteRecordId}' AND {ObjectName}.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND {ObjectName}.SERVICE_ID = '{ServiceId}' AND ISNULL({ObjectName}.CONFIGURATION_STATUS,'') = 'COMPLETE' {WhereConditionString}) IQ			
            """.format(UserId=self.user_id, UserName=self.user_name, ObjectName=self.source_object_name, QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id, ItemSummaryLastLineNo=summary_last_line_no, WhereConditionString=item_summary_where_string, JoinString=item_summary_join_string,BillingType=self.get_billing_type_val))
            #self.getting_cps_tax(self.service_id)
            #INC08862424 - End - M
            if self.triggered_from != 'Split':
                ScriptExecutor.ExecuteGlobal('CQCPSTAXRE',{'service_id':self.service_id, 'Fun_type':'CPQ_TO_ECC'})
        return True		
    
    def _pmsa_quote_items_entitlement_insert(self,update=False):
        #if update: # need to verify one more time
        Sql.RunQuery("DELETE SAQITE FROM SAQITE WHERE SAQITE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQITE.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQITE.SERVICE_ID = '{ServiceId}'".format(QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
        if self.quote_service_entitlement_type in ('STR-OFFBGBKTGCPCND OBJ-GPAS'):
            Sql.RunQuery("""INSERT SAQITE (QUOTE_REV_ITEM_ENTITLEMENT_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified, CPS_CONFIGURATION_ID, CPS_MATCH_ID, ENTITLEMENT_COST_IMPACT, ENTITLEMENT_GROUP_ID, ENTITLEMENT_GROUP_XML, ENTITLEMENT_PRICE_IMPACT, ENTITLEMENT_XML, IS_CHANGED, LINE, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, QTEITM_RECORD_ID, QUOTE_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID,BASE_FEE,BILLING_CONDITION,BILLING_CYCLE,LOW_QTY_PART,CONCOV,COO_RED_GUAR,COMMIT_CONSIGNED_PART,COMMIT_REQUEST_PART,CUST_PURCH_COMMIT,FORECAST_REDIS_FREQ,FORECAST_ADJ_FREQ,IDLE_DURATION,IDLE_NOTICE,IDLING_EXCEP,KPI_ON_REQUEST,KPI_MONTHLY_CON,MAX_OF_TOOLS,MISC_TERM,ONSITE_CONSPRT,WAF_SPEC_INP,CREDIT_CONSIGNED_PART,CREDIT_NTE_CON,CREDIT_NTE_REQ,CREDIT_REQUEST_PART,PM_QTY_CRD,RPRCUS_OWNPRT,REPONSE_TIME,SCHEDULE_PART,SOFT_MNT_FEE,UNSCHEDULED_PART,WARM_HOT_IDLE,SRV_SPT_ENT,SPR_SPT_ENT,PARTS_BURN_DOWN,PARTS_BUY_BACK,ADDITIONAL_TGTKPI,BONUS_PEN_TIED_KPI,CONSUMABLE,LMT_PARTS_PAY,NEW_PARTS_ONLY,NON_CONSUMABLE,PRICE_CRITICAL_PARAM,PRIMARY_KPI,PROCESS_PARTS_KITS_CLEAN_RECY,RESPONSE_TIME,SPLIT_QUOTE,SWAP_KITS_AMAT_PROVIDED,WET_CLEAN_LABOR,SOFTWARE_SUPPORT,INSTALL_T3,PSE_SUPPORT,NOT_EXCEEDVAL,DECONTAMINATION,CUST_COMMIT_SCHED_PARTS,COMMIT_OR_PTS_METHOD,QUOTE_TYPE,BILLING_TYPE)
                    SELECT
                        CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REV_ITEM_ENTITLEMENT_RECORD_ID,
                        '{UserName}' AS CPQTABLEENTRYADDEDBY,
                        GETDATE() as CPQTABLEENTRYDATEADDED,
                        {UserId} as CpqTableEntryModifiedBy,
                        GETDATE() as CpqTableEntryDateModified,OQ.* FROM ( SELECT DISTINCT 
                        {ObjectName}.CPS_CONFIGURATION_ID,
                        {ObjectName}.CPS_MATCH_ID,
                        null as ENTITLEMENT_COST_IMPACT,
                        null as ENTITLEMENT_GROUP_ID,
                        null as ENTITLEMENT_GROUP_XML,
                        null as ENTITLEMENT_PRICE_IMPACT,
                        {ObjectName}.ENTITLEMENT_XML,
                        null as IS_CHANGED,
                        SAQRIT.LINE,						
                        SAQRIT.SERVICE_DESCRIPTION,
                        SAQRIT.SERVICE_ID,
                        SAQRIT.SERVICE_RECORD_ID,
                        SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID,						
                        SAQRIT.QUOTE_ID,
                        SAQRIT.QUOTE_RECORD_ID,
                        SAQRIT.QTEREV_ID,
                        SAQRIT.QTEREV_RECORD_ID,						
                        IQ.GREENBOOK,
                        IQ.GREENBOOK_RECORD_ID,
                        {ObjectName}.BASE_FEE,
                        {ObjectName}.BILLING_CONDITION,
                        {ObjectName}.BILLING_CYCLE,
                        {ObjectName}.LOW_QTY_PART,
                        {ObjectName}.CONCOV,
                        {ObjectName}.COO_RED_GUAR,
                        {ObjectName}.COMMIT_CONSIGNED_PART,
                        {ObjectName}.COMMIT_REQUEST_PART,
                        {ObjectName}.CUST_PURCH_COMMIT,
                        {ObjectName}.FORECAST_REDIS_FREQ,
                        {ObjectName}.FORECAST_ADJ_FREQ,
                        {ObjectName}.IDLE_DURATION,
                        {ObjectName}.IDLE_NOTICE,
                        {ObjectName}.IDLING_EXCEP,
                        {ObjectName}.KPI_ON_REQUEST,
                        {ObjectName}.KPI_MONTHLY_CON,
                        {ObjectName}.MAX_OF_TOOLS,
                        {ObjectName}.MISC_TERM,
                        {ObjectName}.ONSITE_CONSPRT,
                        {ObjectName}.WAF_SPEC_INP,
                        {ObjectName}.CREDIT_CONSIGNED_PART,
                        {ObjectName}.CREDIT_NTE_CON,
                        {ObjectName}.CREDIT_NTE_REQ,
                        {ObjectName}.CREDIT_REQUEST_PART,
                        {ObjectName}.PM_QTY_CRD,
                        {ObjectName}.RPRCUS_OWNPRT,
                        {ObjectName}.REPONSE_TIME,
                        {ObjectName}.SCHEDULE_PART,
                        {ObjectName}.SOFT_MNT_FEE,
                        {ObjectName}.UNSCHEDULED_PART,
                        {ObjectName}.WARM_HOT_IDLE,
                        {ObjectName}.SRV_SPT_ENT,
                        {ObjectName}.SPR_SPT_ENT,
                        {ObjectName}.PARTS_BURN_DOWN,
                        {ObjectName}.PARTS_BUY_BACK,
                        {ObjectName}.ATGKEY,
                        {ObjectName}.BPTKPI,
                        {ObjectName}.CNSMBL_ENT,
                        {ObjectName}.LMT_PARTS_PAY,
                        {ObjectName}.NWPTON,
                        {ObjectName}.NCNSMB_ENT,
                        {ObjectName}.PRICE_CRITICAL_PARAM,
                        {ObjectName}.PRMKPI_ENT,
                        {ObjectName}.PROCESS_PARTS_KITS_CLEAN_RECY,
                        {ObjectName}.REPONSE_TIME AS RESPONSE_TIME,
                        {ObjectName}.SPQTEV,
                        {ObjectName}.SWPKTA,
                        {ObjectName}.WETCLN_ENT,
                        {ObjectName}.SOFTWARE_SUPPORT,
                        {ObjectName}.INSTALL_T3,
                        {ObjectName}.PSE_SUPPORT,
                        {ObjectName}.NOT_EXCEEDVAL,
                        {ObjectName}.DECONTAMINATION,
                        {ObjectName}.CUST_COMMIT_SCHED_PARTS,
                        {ObjectName}.COMMIT_OR_PTS_METHOD,
                        {ObjectName}.QTETYP,
                        {ObjectName}.BILTYP
                        FROM (
                            SELECT SAQGPA.SERVICE_ID,SAQGPA.GREENBOOK,SAQGPA.GREENBOOK_RECORD_ID,SAQGPA.FABLOCATION_ID,SAQGPA.GOT_CODE,SAQGPA.KIT_ID,SAQGPA.QUOTE_RECORD_ID,SAQGPA.QTEREV_RECORD_ID,SAQGPA.PROCESS_TYPE,SAQGPA.DEVICE_NODE,SERVICE_RECORD_ID
                                FROM SAQGPA (NOLOCK) 
                                    
                                WHERE SAQGPA.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQGPA.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQGPA.SERVICE_ID = '{ServiceId}'  AND ISNULL(SAQGPA.KIT_ID,'') != '' AND INCLUDED = 1
                                GROUP BY SAQGPA.SERVICE_ID,SAQGPA.GREENBOOK,SAQGPA.GREENBOOK_RECORD_ID,SAQGPA.FABLOCATION_ID,SAQGPA.GOT_CODE,SAQGPA.KIT_ID,SAQGPA.QUOTE_RECORD_ID,SAQGPA.QTEREV_RECORD_ID,SAQGPA.PROCESS_TYPE,SAQGPA.DEVICE_NODE,SERVICE_RECORD_ID
                                
                        ) IQ
                        JOIN {ObjectName} (NOLOCK) ON {ObjectName}.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND {ObjectName}.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND {ObjectName}.GREENBOOK = IQ.GREENBOOK AND {ObjectName}.GOT_CODE = IQ.GOT_CODE AND IQ.SERVICE_ID = SAQGPE.SERVICE_ID
                        JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID
                                                AND SAQRIT.SERVICE_RECORD_ID = IQ.SERVICE_RECORD_ID
                                                AND SAQRIT.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID
                                                AND SAQRIT.GREENBOOK = IQ.GREENBOOK
                                                AND SAQRIT.FABLOCATION_ID = IQ.FABLOCATION_ID
                                                AND SAQRIT.KIT_ID = IQ.KIT_ID
                                                AND SAQRIT.GOT_CODE = IQ.GOT_CODE
                                                            
                    WHERE {ObjectName}.QUOTE_RECORD_ID = '{QuoteRecordId}' AND {ObjectName}.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND IQ.SERVICE_ID = '{ServiceId}' AND ISNULL({ObjectName}.CONFIGURATION_STATUS,'') = 'COMPLETE' ) OQ			
                """.format(UserId=self.user_id, UserName=self.user_name, ObjectName='SAQGPE', QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
        elif self.quote_service_entitlement_type in ("STR-OFFBGBSMKTGCPCND OBJ-AS"):
            Sql.RunQuery("""INSERT SAQITE (QUOTE_REV_ITEM_ENTITLEMENT_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified, CPS_CONFIGURATION_ID, CPS_MATCH_ID, ENTITLEMENT_COST_IMPACT, ENTITLEMENT_GROUP_ID, ENTITLEMENT_GROUP_XML, ENTITLEMENT_PRICE_IMPACT, ENTITLEMENT_XML, IS_CHANGED, LINE, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, QTEITM_RECORD_ID, QUOTE_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID,BASE_FEE,BILLING_CONDITION,BILLING_CYCLE,LOW_QTY_PART,CONCOV,COO_RED_GUAR,COMMIT_CONSIGNED_PART,COMMIT_REQUEST_PART,CUST_PURCH_COMMIT,FORECAST_REDIS_FREQ,FORECAST_ADJ_FREQ,IDLE_DURATION,IDLE_NOTICE,IDLING_EXCEP,KPI_ON_REQUEST,KPI_MONTHLY_CON,MAX_OF_TOOLS,MISC_TERM,ONSITE_CONSPRT,WAF_SPEC_INP,CREDIT_CONSIGNED_PART,CREDIT_NTE_CON,CREDIT_NTE_REQ,CREDIT_REQUEST_PART,PM_QTY_CRD,RPRCUS_OWNPRT,REPONSE_TIME,SCHEDULE_PART,SOFT_MNT_FEE,UNSCHEDULED_PART,WARM_HOT_IDLE,SRV_SPT_ENT,SPR_SPT_ENT,PARTS_BURN_DOWN,PARTS_BUY_BACK,ADDITIONAL_TGTKPI,BONUS_PEN_TIED_KPI,CONSUMABLE,LMT_PARTS_PAY,NEW_PARTS_ONLY,NON_CONSUMABLE,PRICE_CRITICAL_PARAM,PRIMARY_KPI,PROCESS_PARTS_KITS_CLEAN_RECY,RESPONSE_TIME,SPLIT_QUOTE,SWAP_KITS_AMAT_PROVIDED,WET_CLEAN_LABOR,SOFTWARE_SUPPORT,INSTALL_T3,PSE_SUPPORT,NOT_EXCEEDVAL,DECONTAMINATION,CUST_COMMIT_SCHED_PARTS,COMMIT_OR_PTS_METHOD,QUOTE_TYPE,BILLING_TYPE)
                        SELECT
                            CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REV_ITEM_ENTITLEMENT_RECORD_ID,
                            '{UserName}' AS CPQTABLEENTRYADDEDBY,
                            GETDATE() as CPQTABLEENTRYDATEADDED,
                            {UserId} as CpqTableEntryModifiedBy,
                            GETDATE() as CpqTableEntryDateModified,OQ.* FROM ( SELECT DISTINCT 
                            {ObjectName}.CPS_CONFIGURATION_ID,
                            {ObjectName}.CPS_MATCH_ID,
                            null as ENTITLEMENT_COST_IMPACT,
                            null as ENTITLEMENT_GROUP_ID,
                            null as ENTITLEMENT_GROUP_XML,
                            null as ENTITLEMENT_PRICE_IMPACT,
                            {ObjectName}.ENTITLEMENT_XML,
                            null as IS_CHANGED,
                            SAQRIT.LINE,						
                            SAQRIT.SERVICE_DESCRIPTION,
                            SAQRIT.SERVICE_ID,
                            SAQRIT.SERVICE_RECORD_ID,
                            SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID,						
                            SAQRIT.QUOTE_ID,
                            SAQRIT.QUOTE_RECORD_ID,
                            SAQRIT.QTEREV_ID,
                            SAQRIT.QTEREV_RECORD_ID,						
                            IQ.GREENBOOK,
                            IQ.GREENBOOK_RECORD_ID,
                            {ObjectName}.BASE_FEE,
                            {ObjectName}.BILLING_CONDITION,
                            {ObjectName}.BILLING_CYCLE,
                            {ObjectName}.LOW_QTY_PART,
                            {ObjectName}.CONCOV,
                            {ObjectName}.COO_RED_GUAR,
                            {ObjectName}.COMMIT_CONSIGNED_PART,
                            {ObjectName}.COMMIT_REQUEST_PART,
                            {ObjectName}.CUST_PURCH_COMMIT,
                            {ObjectName}.FORECAST_REDIS_FREQ,
                            {ObjectName}.FORECAST_ADJ_FREQ,
                            {ObjectName}.IDLE_DURATION,
                            {ObjectName}.IDLE_NOTICE,
                            {ObjectName}.IDLING_EXCEP,
                            {ObjectName}.KPI_ON_REQUEST,
                            {ObjectName}.KPI_MONTHLY_CON,
                            {ObjectName}.MAX_OF_TOOLS,
                            {ObjectName}.MISC_TERM,
                            {ObjectName}.ONSITE_CONSPRT,
                            {ObjectName}.WAF_SPEC_INP,
                            {ObjectName}.CREDIT_CONSIGNED_PART,
                            {ObjectName}.CREDIT_NTE_CON,
                            {ObjectName}.CREDIT_NTE_REQ,
                            {ObjectName}.CREDIT_REQUEST_PART,
                            {ObjectName}.PM_QTY_CRD,
                            {ObjectName}.RPRCUS_OWNPRT,
                            {ObjectName}.REPONSE_TIME,
                            {ObjectName}.SCHEDULE_PART,
                            {ObjectName}.SOFT_MNT_FEE,
                            {ObjectName}.UNSCHEDULED_PART,
                            {ObjectName}.WARM_HOT_IDLE,
                            {ObjectName}.SRV_SPT_ENT,
                            {ObjectName}.SPR_SPT_ENT,
                            {ObjectName}.PARTS_BURN_DOWN,
                            {ObjectName}.PARTS_BUY_BACK,
                            {ObjectName}.ATGKEY,
                            {ObjectName}.BPTKPI,
                            {ObjectName}.CNSMBL_ENT,
                            {ObjectName}.LMT_PARTS_PAY,
                            {ObjectName}.NWPTON,
                            {ObjectName}.NCNSMB_ENT,
                            {ObjectName}.PRICE_CRITICAL_PARAM,
                            {ObjectName}.PRMKPI_ENT,
                            {ObjectName}.PROCESS_PARTS_KITS_CLEAN_RECY,
                            {ObjectName}.REPONSE_TIME AS RESPONSE_TIME,
                            {ObjectName}.SPQTEV,
                            {ObjectName}.SWPKTA,
                            {ObjectName}.WETCLN_ENT,
                            {ObjectName}.SOFTWARE_SUPPORT,
                            {ObjectName}.INSTALL_T3,
                            {ObjectName}.PSE_SUPPORT,
                            {ObjectName}.NOT_EXCEEDVAL,
                            {ObjectName}.DECONTAMINATION,
                            {ObjectName}.CUST_COMMIT_SCHED_PARTS,
                            {ObjectName}.COMMIT_OR_PTS_METHOD,
                            {ObjectName}.QTETYP,
                            {ObjectName}.BILTYP
                            FROM (
                                SELECT SAQGPA.SERVICE_ID,SAQGPA.GREENBOOK,SAQGPA.FABLOCATION_ID,SAQGPA.GOT_CODE,SAQGPA.PM_ID,SAQGPA.QUOTE_RECORD_ID,SAQGPA.QTEREV_RECORD_ID,SAQGPA.GOTCODE_RECORD_ID,SAQGPA.SERVICE_DESCRIPTION,SAQGPA.SERVICE_RECORD_ID,SAQGPA.GREENBOOK_RECORD_ID,ISNULL(PROCESS_TYPE,'') AS PROCESS_TYPE , ISNULL(DEVICE_NODE,'') AS DEVICE_NODE,MNTEVT_LEVEL,SAQGPA.KIT_ID
                                    FROM SAQGPA (NOLOCK) 
                                    WHERE SAQGPA.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQGPA.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQGPA.SERVICE_ID = '{ServiceId}' AND MNTEVT_LEVEL != 'Scheduled Maintenance'
                                    GROUP BY SAQGPA.SERVICE_ID,SAQGPA.GREENBOOK,SAQGPA.FABLOCATION_ID,SAQGPA.GOT_CODE,SAQGPA.PM_ID,SAQGPA.QUOTE_RECORD_ID,SAQGPA.QTEREV_RECORD_ID,SAQGPA.GOTCODE_RECORD_ID,SAQGPA.SERVICE_DESCRIPTION,SAQGPA.SERVICE_RECORD_ID,SAQGPA.GREENBOOK_RECORD_ID, ISNULL(PROCESS_TYPE,'')  , ISNULL(DEVICE_NODE,''),MNTEVT_LEVEL,SAQGPA.KIT_ID
                            ) IQ
                            JOIN {ObjectName} (NOLOCK) ON {ObjectName}.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND {ObjectName}.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND {ObjectName}.GREENBOOK = IQ.GREENBOOK AND {ObjectName}.GOT_CODE = IQ.GOT_CODE AND {ObjectName}.PM_ID = IQ.PM_ID AND IQ.SERVICE_ID = SAQGPE.SERVICE_ID AND {ObjectName}.KIT_ID = IQ.KIT_ID
                            JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID
                                                    AND SAQRIT.SERVICE_RECORD_ID = IQ.SERVICE_RECORD_ID
                                                    AND SAQRIT.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID
                                                    AND SAQRIT.GREENBOOK = IQ.GREENBOOK
                                                    AND SAQRIT.FABLOCATION_ID = IQ.FABLOCATION_ID
                                                    AND SAQRIT.OBJECT_ID = IQ.PM_ID
                                                    AND SAQRIT.GOT_CODE = IQ.GOT_CODE
                                                    AND SAQRIT.KIT_ID = IQ.KIT_ID        
                        WHERE {ObjectName}.QUOTE_RECORD_ID = '{QuoteRecordId}' AND {ObjectName}.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND IQ.SERVICE_ID = '{ServiceId}' AND IQ.MNTEVT_LEVEL != 'Scheduled Maintenance' AND ISNULL({ObjectName}.CONFIGURATION_STATUS,'') = 'COMPLETE' ) OQ			
                    """.format(UserId=self.user_id, UserName=self.user_name, ObjectName='SAQGPE', QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
            Sql.RunQuery("""INSERT SAQITE (QUOTE_REV_ITEM_ENTITLEMENT_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified, CPS_CONFIGURATION_ID, CPS_MATCH_ID, ENTITLEMENT_COST_IMPACT, ENTITLEMENT_GROUP_ID, ENTITLEMENT_GROUP_XML, ENTITLEMENT_PRICE_IMPACT, ENTITLEMENT_XML, IS_CHANGED, LINE, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, QTEITM_RECORD_ID, QUOTE_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID,BASE_FEE,BILLING_CONDITION,BILLING_CYCLE,LOW_QTY_PART,CONCOV,COO_RED_GUAR,COMMIT_CONSIGNED_PART,COMMIT_REQUEST_PART,CUST_PURCH_COMMIT,FORECAST_REDIS_FREQ,FORECAST_ADJ_FREQ,IDLE_DURATION,IDLE_NOTICE,IDLING_EXCEP,KPI_ON_REQUEST,KPI_MONTHLY_CON,MAX_OF_TOOLS,MISC_TERM,ONSITE_CONSPRT,WAF_SPEC_INP,CREDIT_CONSIGNED_PART,CREDIT_NTE_CON,CREDIT_NTE_REQ,CREDIT_REQUEST_PART,PM_QTY_CRD,RPRCUS_OWNPRT,REPONSE_TIME,SCHEDULE_PART,SOFT_MNT_FEE,UNSCHEDULED_PART,WARM_HOT_IDLE,SRV_SPT_ENT,SPR_SPT_ENT,PARTS_BURN_DOWN,PARTS_BUY_BACK,ADDITIONAL_TGTKPI,BONUS_PEN_TIED_KPI,CONSUMABLE,LMT_PARTS_PAY,NEW_PARTS_ONLY,NON_CONSUMABLE,PRICE_CRITICAL_PARAM,PRIMARY_KPI,PROCESS_PARTS_KITS_CLEAN_RECY,RESPONSE_TIME,SPLIT_QUOTE,SWAP_KITS_AMAT_PROVIDED,WET_CLEAN_LABOR,SOFTWARE_SUPPORT,INSTALL_T3,PSE_SUPPORT,NOT_EXCEEDVAL,DECONTAMINATION,CUST_COMMIT_SCHED_PARTS,COMMIT_OR_PTS_METHOD,QUOTE_TYPE,BILLING_TYPE)
                        SELECT
                            CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REV_ITEM_ENTITLEMENT_RECORD_ID,
                            '{UserName}' AS CPQTABLEENTRYADDEDBY,
                            GETDATE() as CPQTABLEENTRYDATEADDED,
                            {UserId} as CpqTableEntryModifiedBy,
                            GETDATE() as CpqTableEntryDateModified,OQ.* FROM ( SELECT DISTINCT 
                            {ObjectName}.CPS_CONFIGURATION_ID,
                            {ObjectName}.CPS_MATCH_ID,
                            null as ENTITLEMENT_COST_IMPACT,
                            null as ENTITLEMENT_GROUP_ID,
                            null as ENTITLEMENT_GROUP_XML,
                            null as ENTITLEMENT_PRICE_IMPACT,
                            {ObjectName}.ENTITLEMENT_XML,
                            null as IS_CHANGED,
                            SAQRIT.LINE,						
                            SAQRIT.SERVICE_DESCRIPTION,
                            SAQRIT.SERVICE_ID,
                            SAQRIT.SERVICE_RECORD_ID,
                            SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID,						
                            SAQRIT.QUOTE_ID,
                            SAQRIT.QUOTE_RECORD_ID,
                            SAQRIT.QTEREV_ID,
                            SAQRIT.QTEREV_RECORD_ID,						
                            IQ.GREENBOOK,
                            IQ.GREENBOOK_RECORD_ID,
                            {ObjectName}.BASE_FEE,
                            {ObjectName}.BILLING_CONDITION,
                            {ObjectName}.BILLING_CYCLE,
                            {ObjectName}.LOW_QTY_PART,
                            {ObjectName}.CONCOV,
                            {ObjectName}.COO_RED_GUAR,
                            {ObjectName}.COMMIT_CONSIGNED_PART,
                            {ObjectName}.COMMIT_REQUEST_PART,
                            {ObjectName}.CUST_PURCH_COMMIT,
                            {ObjectName}.FORECAST_REDIS_FREQ,
                            {ObjectName}.FORECAST_ADJ_FREQ,
                            {ObjectName}.IDLE_DURATION,
                            {ObjectName}.IDLE_NOTICE,
                            {ObjectName}.IDLING_EXCEP,
                            {ObjectName}.KPI_ON_REQUEST,
                            {ObjectName}.KPI_MONTHLY_CON,
                            {ObjectName}.MAX_OF_TOOLS,
                            {ObjectName}.MISC_TERM,
                            {ObjectName}.ONSITE_CONSPRT,
                            {ObjectName}.WAF_SPEC_INP,
                            {ObjectName}.CREDIT_CONSIGNED_PART,
                            {ObjectName}.CREDIT_NTE_CON,
                            {ObjectName}.CREDIT_NTE_REQ,
                            {ObjectName}.CREDIT_REQUEST_PART,
                            {ObjectName}.PM_QTY_CRD,
                            {ObjectName}.RPRCUS_OWNPRT,
                            {ObjectName}.REPONSE_TIME,
                            {ObjectName}.SCHEDULE_PART,
                            {ObjectName}.SOFT_MNT_FEE,
                            {ObjectName}.UNSCHEDULED_PART,
                            {ObjectName}.WARM_HOT_IDLE,
                            {ObjectName}.SRV_SPT_ENT,
                            {ObjectName}.SPR_SPT_ENT,
                            {ObjectName}.PARTS_BURN_DOWN,
                            {ObjectName}.PARTS_BUY_BACK,
                            {ObjectName}.ATGKEY,
                            {ObjectName}.BPTKPI,
                            {ObjectName}.CNSMBL_ENT,
                            {ObjectName}.LMT_PARTS_PAY,
                            {ObjectName}.NWPTON,
                            {ObjectName}.NCNSMB_ENT,
                            {ObjectName}.PRICE_CRITICAL_PARAM,
                            {ObjectName}.PRMKPI_ENT,
                            {ObjectName}.PROCESS_PARTS_KITS_CLEAN_RECY,
                            {ObjectName}.REPONSE_TIME AS RESPONSE_TIME,
                            {ObjectName}.SPQTEV,
                            {ObjectName}.SWPKTA,
                            {ObjectName}.WETCLN_ENT,
                            {ObjectName}.SOFTWARE_SUPPORT,
                            {ObjectName}.INSTALL_T3,
                            {ObjectName}.PSE_SUPPORT,
                            {ObjectName}.NOT_EXCEEDVAL,
                            {ObjectName}.DECONTAMINATION,
                            {ObjectName}.CUST_COMMIT_SCHED_PARTS,
                            {ObjectName}.COMMIT_OR_PTS_METHOD,
                            {ObjectName}.QTETYP,
                            {ObjectName}.BILTYP
                            FROM (
                                SELECT SAQGPA.SERVICE_ID,SAQGPA.GREENBOOK,SAQGPA.FABLOCATION_ID,SAQGPA.GOT_CODE,SAQGPA.MNTEVT_LEVEL,SAQGPA.QUOTE_RECORD_ID,SAQGPA.QTEREV_RECORD_ID,SAQGPA.GOTCODE_RECORD_ID,SAQGPA.SERVICE_DESCRIPTION,SAQGPA.SERVICE_RECORD_ID,SAQGPA.GREENBOOK_RECORD_ID,ISNULL(PROCESS_TYPE,'') AS PROCESS_TYPE , ISNULL(DEVICE_NODE,'') AS DEVICE_NODE,KIT_ID
                                FROM SAQGPA (NOLOCK) 
                                    WHERE SAQGPA.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQGPA.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQGPA.SERVICE_ID = '{ServiceId}' AND MNTEVT_LEVEL = 'Scheduled Maintenance'
                                    GROUP BY SAQGPA.SERVICE_ID,SAQGPA.GREENBOOK,SAQGPA.FABLOCATION_ID,SAQGPA.GOT_CODE,SAQGPA.PM_ID,SAQGPA.QUOTE_RECORD_ID,SAQGPA.QTEREV_RECORD_ID,SAQGPA.GOTCODE_RECORD_ID,SAQGPA.SERVICE_DESCRIPTION,SAQGPA.SERVICE_RECORD_ID,SAQGPA.GREENBOOK_RECORD_ID,SAQGPA.MNTEVT_LEVEL, ISNULL(PROCESS_TYPE,'')  , ISNULL(DEVICE_NODE,''),KIT_ID
                            ) IQ
                            JOIN {ObjectName} (NOLOCK) ON {ObjectName}.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND {ObjectName}.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND {ObjectName}.GREENBOOK = IQ.GREENBOOK  AND IQ.SERVICE_ID = {ObjectName}.SERVICE_ID
                            JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID
                                                    AND SAQRIT.SERVICE_RECORD_ID = IQ.SERVICE_RECORD_ID
                                                    AND SAQRIT.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID
                                                    AND SAQRIT.GREENBOOK = IQ.GREENBOOK
                                                    AND SAQRIT.FABLOCATION_ID = IQ.FABLOCATION_ID
                                                    AND SAQRIT.OBJECT_ID = IQ.MNTEVT_LEVEL
                                                    AND SAQRIT.GOT_CODE = IQ.GOT_CODE
                                                    AND SAQRIT.KIT_ID = IQ.KIT_ID	       
                        WHERE {ObjectName}.QUOTE_RECORD_ID = '{QuoteRecordId}' AND {ObjectName}.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND IQ.SERVICE_ID = '{ServiceId}' AND ISNULL({ObjectName}.CONFIGURATION_STATUS,'') = 'COMPLETE' AND IQ.MNTEVT_LEVEL = 'Scheduled Maintenance' ) OQ			
                    """.format(UserId=self.user_id, UserName=self.user_name, ObjectName='SAQSGE', QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
        
        else:
            Sql.RunQuery("""INSERT SAQITE (QUOTE_REV_ITEM_ENTITLEMENT_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified, CPS_CONFIGURATION_ID, CPS_MATCH_ID, ENTITLEMENT_COST_IMPACT, ENTITLEMENT_GROUP_ID, ENTITLEMENT_GROUP_XML, ENTITLEMENT_PRICE_IMPACT, ENTITLEMENT_XML, IS_CHANGED, LINE, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, QTEITM_RECORD_ID, QUOTE_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID,BASE_FEE,BILLING_CONDITION,BILLING_CYCLE,LOW_QTY_PART,CONCOV,COO_RED_GUAR,COMMIT_CONSIGNED_PART,COMMIT_REQUEST_PART,CUST_PURCH_COMMIT,FORECAST_REDIS_FREQ,FORECAST_ADJ_FREQ,IDLE_DURATION,IDLE_NOTICE,IDLING_EXCEP,KPI_ON_REQUEST,KPI_MONTHLY_CON,MAX_OF_TOOLS,MISC_TERM,ONSITE_CONSPRT,WAF_SPEC_INP,CREDIT_CONSIGNED_PART,CREDIT_NTE_CON,CREDIT_NTE_REQ,CREDIT_REQUEST_PART,PM_QTY_CRD,RPRCUS_OWNPRT,REPONSE_TIME,SCHEDULE_PART,SOFT_MNT_FEE,UNSCHEDULED_PART,WARM_HOT_IDLE,SRV_SPT_ENT,SPR_SPT_ENT,PARTS_BURN_DOWN,PARTS_BUY_BACK,ADDITIONAL_TGTKPI,BONUS_PEN_TIED_KPI,CONSUMABLE,LMT_PARTS_PAY,NEW_PARTS_ONLY,NON_CONSUMABLE,PRICE_CRITICAL_PARAM,PRIMARY_KPI,PROCESS_PARTS_KITS_CLEAN_RECY,RESPONSE_TIME,SPLIT_QUOTE,SWAP_KITS_AMAT_PROVIDED,WET_CLEAN_LABOR,SOFTWARE_SUPPORT,INSTALL_T3,PSE_SUPPORT,NOT_EXCEEDVAL,DECONTAMINATION,CUST_COMMIT_SCHED_PARTS,COMMIT_OR_PTS_METHOD,QUOTE_TYPE,BILLING_TYPE)
                        SELECT
                            CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REV_ITEM_ENTITLEMENT_RECORD_ID,
                            '{UserName}' AS CPQTABLEENTRYADDEDBY,
                            GETDATE() as CPQTABLEENTRYDATEADDED,
                            {UserId} as CpqTableEntryModifiedBy,
                            GETDATE() as CpqTableEntryDateModified,OQ.* FROM ( SELECT DISTINCT 
                            {ObjectName}.CPS_CONFIGURATION_ID,
                            {ObjectName}.CPS_MATCH_ID,
                            null as ENTITLEMENT_COST_IMPACT,
                            null as ENTITLEMENT_GROUP_ID,
                            null as ENTITLEMENT_GROUP_XML,
                            null as ENTITLEMENT_PRICE_IMPACT,
                            {ObjectName}.ENTITLEMENT_XML,
                            null as IS_CHANGED,
                            SAQRIT.LINE,						
                            SAQRIT.SERVICE_DESCRIPTION,
                            SAQRIT.SERVICE_ID,
                            SAQRIT.SERVICE_RECORD_ID,
                            SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID,						
                            SAQRIT.QUOTE_ID,
                            SAQRIT.QUOTE_RECORD_ID,
                            SAQRIT.QTEREV_ID,
                            SAQRIT.QTEREV_RECORD_ID,						
                            IQ.GREENBOOK,
                            IQ.GREENBOOK_RECORD_ID,
                            {ObjectName}.BASE_FEE,
                            {ObjectName}.BILLING_CONDITION,
                            {ObjectName}.BILLING_CYCLE,
                            {ObjectName}.LOW_QTY_PART,
                            {ObjectName}.CONCOV,
                            {ObjectName}.COO_RED_GUAR,
                            {ObjectName}.COMMIT_CONSIGNED_PART,
                            {ObjectName}.COMMIT_REQUEST_PART,
                            {ObjectName}.CUST_PURCH_COMMIT,
                            {ObjectName}.FORECAST_REDIS_FREQ,
                            {ObjectName}.FORECAST_ADJ_FREQ,
                            {ObjectName}.IDLE_DURATION,
                            {ObjectName}.IDLE_NOTICE,
                            {ObjectName}.IDLING_EXCEP,
                            {ObjectName}.KPI_ON_REQUEST,
                            {ObjectName}.KPI_MONTHLY_CON,
                            {ObjectName}.MAX_OF_TOOLS,
                            {ObjectName}.MISC_TERM,
                            {ObjectName}.ONSITE_CONSPRT,
                            {ObjectName}.WAF_SPEC_INP,
                            {ObjectName}.CREDIT_CONSIGNED_PART,
                            {ObjectName}.CREDIT_NTE_CON,
                            {ObjectName}.CREDIT_NTE_REQ,
                            {ObjectName}.CREDIT_REQUEST_PART,
                            {ObjectName}.PM_QTY_CRD,
                            {ObjectName}.RPRCUS_OWNPRT,
                            {ObjectName}.REPONSE_TIME,
                            {ObjectName}.SCHEDULE_PART,
                            {ObjectName}.SOFT_MNT_FEE,
                            {ObjectName}.UNSCHEDULED_PART,
                            {ObjectName}.WARM_HOT_IDLE,
                            {ObjectName}.SRV_SPT_ENT,
                            {ObjectName}.SPR_SPT_ENT,
                            {ObjectName}.PARTS_BURN_DOWN,
                            {ObjectName}.PARTS_BUY_BACK,
                            {ObjectName}.ATGKEY,
                            {ObjectName}.BPTKPI,
                            {ObjectName}.CNSMBL_ENT,
                            {ObjectName}.LMT_PARTS_PAY,
                            {ObjectName}.NWPTON,
                            {ObjectName}.NCNSMB_ENT,
                            {ObjectName}.PRICE_CRITICAL_PARAM,
                            {ObjectName}.PRMKPI_ENT,
                            {ObjectName}.PROCESS_PARTS_KITS_CLEAN_RECY,
                            {ObjectName}.REPONSE_TIME AS RESPONSE_TIME,
                            {ObjectName}.SPQTEV,
                            {ObjectName}.SWPKTA,
                            {ObjectName}.WETCLN_ENT,
                            {ObjectName}.SOFTWARE_SUPPORT,
                            {ObjectName}.INSTALL_T3,
                            {ObjectName}.PSE_SUPPORT,
                            {ObjectName}.NOT_EXCEEDVAL,
                            {ObjectName}.DECONTAMINATION,
                            {ObjectName}.CUST_COMMIT_SCHED_PARTS,
                            {ObjectName}.COMMIT_OR_PTS_METHOD,
                            {ObjectName}.QTETYP,
                            {ObjectName}.BILTYP
                            FROM (
                                SELECT SAQGPA.SERVICE_ID,SAQGPA.GREENBOOK,SAQGPA.FABLOCATION_ID,SAQGPA.GOT_CODE,SAQGPA.PM_ID,SAQGPA.QUOTE_RECORD_ID,SAQGPA.QTEREV_RECORD_ID,SAQGPA.PM_RECORD_ID,SAQGPA.GOTCODE_RECORD_ID,SAQGPA.SERVICE_DESCRIPTION,SAQGPA.SERVICE_RECORD_ID,SAQGPA.GREENBOOK_RECORD_ID,ISNULL(PROCESS_TYPE,'') AS PROCESS_TYPE , ISNULL(DEVICE_NODE,'') AS DEVICE_NODE,KIT_ID
                                    FROM SAQGPA (NOLOCK) 
                                    WHERE SAQGPA.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQGPA.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQGPA.SERVICE_ID = '{ServiceId}'
                                    GROUP BY SAQGPA.SERVICE_ID,SAQGPA.GREENBOOK,SAQGPA.FABLOCATION_ID,SAQGPA.GOT_CODE,SAQGPA.PM_ID,SAQGPA.QUOTE_RECORD_ID,SAQGPA.QTEREV_RECORD_ID,SAQGPA.PM_RECORD_ID,SAQGPA.GOTCODE_RECORD_ID,SAQGPA.SERVICE_DESCRIPTION,SAQGPA.SERVICE_RECORD_ID,SAQGPA.GREENBOOK_RECORD_ID, ISNULL(PROCESS_TYPE,'')  , ISNULL(DEVICE_NODE,''),KIT_ID
                                    
                            ) IQ
                            JOIN {ObjectName} (NOLOCK) ON {ObjectName}.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND {ObjectName}.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND {ObjectName}.GREENBOOK = IQ.GREENBOOK AND {ObjectName}.GOT_CODE = IQ.GOT_CODE AND {ObjectName}.PM_ID = IQ.PM_ID AND IQ.SERVICE_ID = SAQGPE.SERVICE_ID AND {ObjectName}.KIT_ID = IQ.KIT_ID
                            JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID
                                                    AND SAQRIT.SERVICE_RECORD_ID = IQ.SERVICE_RECORD_ID
                                                    AND SAQRIT.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID
                                                    AND SAQRIT.GREENBOOK = IQ.GREENBOOK
                                                    AND SAQRIT.FABLOCATION_ID = IQ.FABLOCATION_ID
                                                    AND SAQRIT.OBJECT_ID = IQ.PM_ID
                                                    AND SAQRIT.GOT_CODE = IQ.GOT_CODE
                                                    AND SAQRIT.KIT_ID = IQ.KIT_ID    
                        WHERE {ObjectName}.QUOTE_RECORD_ID = '{QuoteRecordId}' AND {ObjectName}.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND IQ.SERVICE_ID = '{ServiceId}' AND ISNULL({ObjectName}.CONFIGURATION_STATUS,'') = 'COMPLETE' ) OQ			
                    """.format(UserId=self.user_id, UserName=self.user_name, ObjectName='SAQGPE', QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
            
        return True
            
    def _quote_items_insert(self, update=False):		
        dynamic_ancillary_columns = ""
        dynamic_columns = ""
        ancillary_join = ''
        ancillary_whr_cond =''
        if self.is_ancillary == True or self.addon_product == True:
            dynamic_ancillary_columns = " '0' AS NET_VALUE_INGL_CURR, '0' AS NET_PRICE_INGL_CURR,"
            #PAR_SAQRIT.LINE AS PARQTEITM_LINE, PAR_SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID AS PARQTEITM_LINE_RECORD_ID,
            dynamic_columns = "NET_VALUE_INGL_CURR, NET_PRICE_INGL_CURR,"
            #PARQTEITM_LINE, PARQTEITM_LINE_RECORD_ID,
            if self.service_id == 'Z0046' and self.get_billing_type_val.upper() == 'VARIABLE':
                dynamic_ancillary_columns += " '0' AS ESTVAL_INGL_CURR,  '0' AS COMVAL_INGL_CURR,"
                dynamic_columns += "ESTVAL_INGL_CURR, COMVAL_INGL_CURR,"
            ##condition for getting parent line 
            # ancillary_whr_cond = " AND PAR_SAQRIT.SERVICE_ID = '{par_service_id}'".format(par_service_id = self.parent_service_id)
            # ancillary_join = "JOIN SAQRIT (NOLOCK) PAR_SAQRIT ON PAR_SAQRIT.QUOTE_RECORD_ID = {ObjectName}.QUOTE_RECORD_ID AND PAR_SAQRIT.QTEREV_RECORD_ID = {ObjectName}.QTEREV_RECORD_ID AND PAR_SAQRIT.SERVICE_ID = {ObjectName}.PAR_SERVICE_ID AND PAR_SAQRIT.SERVICE_ID = '{par_service_id}' AND ISNULL(PAR_SAQRIT.GREENBOOK_RECORD_ID,'') = ISNULL({ObjectName}.GREENBOOK_RECORD_ID,'')  ".format(ObjectName = self.source_object_name, par_service_id = self.parent_service_id)	
            # if self.quote_service_entitlement_type in ('OFFERING + EQUIPMENT','OFFERING+EQUIPMENT','OFRNG+EQUIP'):
            # 	ancillary_join +=" AND PAR_SAQRIT.FABLOCATION_RECORD_ID = {ObjectName}. FABLOCATION_RECORD_ID AND ISNULL(PAR_SAQRIT.EQUIPMENT_ID,'') = {ObjectName}.EQUIPMENT_ID".format(ObjectName = self.source_object_name)
        
        if self.source_object_name:
            ##809 HPQC DEFECT code starts...
            split_quote_condition = "AND SAQRIS.PAR_SERVICE_ID = '{}'".format(self.split_parent_service_id) if self.service_id == "Z0105" else ""
            ##809 HPQC DEFECT code ends..		
            equipments_count = 0
            quote_item_obj = Sql.GetFirst("SELECT TOP 1 LINE FROM SAQRIT (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' ORDER BY LINE DESC".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id))
            # if quote_item_obj:
            #     equipments_count = int(quote_item_obj.LINE)
                    
            if self.quote_service_entitlement_type in ('STR-OFFBGBEQ OBJ-EQ') and not self.triggered_from:
                #get billing type start
                #INC08898664 Start - M
                
                #A055S000P01-20908,INC09026574 - Start - M
                Sql.RunQuery("""INSERT SAQRIT (QUOTE_REVISION_CONTRACT_ITEM_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified, CONTRACT_VALID_FROM, CONTRACT_VALID_TO, DOC_CURRENCY, DOCURR_RECORD_ID, EXCHANGE_RATE, EXCHANGE_RATE_DATE, EXCHANGE_RATE_RECORD_ID, GL_ACCOUNT_NO, GLOBAL_CURRENCY, GLOBAL_CURRENCY_RECORD_ID, LINE,EQUIPMENT_ID,EQUIPMENT_RECORD_ID, OBJECT_ID,TEMP_TOOL, OBJECT_TYPE, FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID,PAR_PRDOFR_ID,PAR_PRDOFR_RECORD_ID, PROFIT_CENTER, QUANTITY, QUOTE_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, REF_SALESORDER, STATUS, TAXCLASSIFICATION_DESCRIPTION, TAXCLASSIFICATION_ID, TAXCLASSIFICATION_RECORD_ID,TAX_PERCENTAGE,{DynamicColumnNames} GREENBOOK,BILLING_TYPE,GREENBOOK_RECORD_ID,QTESRVCOB_RECORD_ID, QTEITMSUM_RECORD_ID)
                    SELECT CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REVISION_CONTRACT_ITEM_ID,
                        '{UserName}' AS CPQTABLEENTRYADDEDBY,
                        GETDATE() as CPQTABLEENTRYDATEADDED,
                        {UserId} as CpqTableEntryModifiedBy,
                        GETDATE() as CpqTableEntryDateModified, 
                        IQ.* FROM (
                    SELECT
                        distinct
                        SAQSCO.CONTRACT_VALID_FROM,
                        SAQSCO.CONTRACT_VALID_TO,
                        SAQTRV.DOC_CURRENCY,
                        SAQTRV.DOCCURR_RECORD_ID as DOCURR_RECORD_ID,
                        ISNULL(CONVERT(FLOAT,SAQTRV.EXCHANGE_RATE),'') AS EXCHANGE_RATE,
                        SAQTRV.EXCHANGE_RATE_DATE,
                        SAQTRV.EXCHANGERATE_RECORD_ID as EXCHANGE_RATE_RECORD_ID,
                        null as GL_ACCOUNT_NO,
                        SAQTRV.GLOBAL_CURRENCY,
                        SAQTRV.GLOBAL_CURRENCY_RECORD_ID,
                        --ROW_NUMBER()OVER(ORDER BY({ObjectName}.CpqTableEntryId)) + {EquipmentsCount} as LINE,
                        null as LINE,
                        SAQSCE.EQUIPMENT_ID as EQUIPMENT_ID,
                        SAQSCE.EQUIPMENT_RECORD_ID as EQUIPMENT_RECORD_ID,
                        SAQSCE.EQUIPMENT_ID as OBJECT_ID,
                        SAQSCO.TEMP_TOOL,
                        'EQUIPMENT' as OBJECT_TYPE,
                        SAQSCE.FABLOCATION_ID as FABLOCATION_ID,
                        SAQSCE.FABLOCATION_NAME as FABLOCATION_NAME,
                        SAQSCE.FABLOCATION_RECORD_ID as FABLOCATION_RECORD_ID,			
                        {ObjectName}.SERVICE_DESCRIPTION,
                        {ObjectName}.SERVICE_ID,
                        {ObjectName}.SERVICE_RECORD_ID,
                        {ObjectName}.PAR_SERVICE_ID as PAR_PRDOFR_ID,
                        {ObjectName}.PAR_SERVICE_RECORD_ID as PAR_PRDOFR_RECORD_ID,
                        null as PROFIT_CENTER,
                        1 as QUANTITY,
                        SAQTRV.QUOTE_ID,
                        SAQTRV.QUOTE_RECORD_ID,
                        SAQTMT.QTEREV_ID,
                        SAQTMT.QTEREV_RECORD_ID,
                        null as REF_SALESORDER,
                        null as STATUS,
                        MAMSCT.TAXCLASSIFICATION_DESCRIPTION,
                        MAMSCT.TAXCLASSIFICATION_ID,
                        MAMSCT.TAXCLASSIFICATION_RECORD_ID,
                        SAQRIS.TAX_PERCENTAGE,
                        {DynamicValues}					
                        {ObjectName}.GREENBOOK,
                        {ObjectName}.BILTYP as BILLING_TYPE,
                        {ObjectName}.GREENBOOK_RECORD_ID,
                        SAQSCO.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID AS QTESRVCOB_RECORD_ID,
                        SAQRIS.QUOTE_REV_ITEM_SUMMARY_RECORD_ID as QTEITMSUM_RECORD_ID
                    FROM (SELECT QUOTE_RECORD_ID,QTEREV_RECORD_ID,SERVICE_ID,GREENBOOK,FABLOCATION_ID,EQUIPMENT_ID,TEMP_TOOL,CONTRACT_VALID_FROM,CONTRACT_VALID_TO,ISNULL(PAR_SERVICE_ID,'') AS PAR_SERVICE_ID, ISNULL(PAR_SERVICE_RECORD_ID,'') AS PAR_SERVICE_RECORD_ID,QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID FROM SAQSCO (NOLOCK) WHERE SAQSCO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQSCO.SERVICE_ID = '{ServiceId}'  GROUP BY QUOTE_RECORD_ID,QTEREV_RECORD_ID,SERVICE_ID,GREENBOOK,FABLOCATION_ID,EQUIPMENT_ID,TEMP_TOOL,CONTRACT_VALID_FROM,CONTRACT_VALID_TO,ISNULL(PAR_SERVICE_ID,''),ISNULL(PAR_SERVICE_RECORD_ID,''),QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID) SAQSCO
                    JOIN {ObjectName} (NOLOCK) ON SAQSCO.QUOTE_RECORD_ID = {ObjectName}.QUOTE_RECORD_ID AND SAQSCO.QTEREV_RECORD_ID = {ObjectName}.QTEREV_RECORD_ID AND SAQSCO.SERVICE_ID = {ObjectName}.SERVICE_ID AND SAQSCO.FABLOCATION_ID = SAQSCO.FABLOCATION_ID AND ISNULL(SAQSCO.GREENBOOK,'') = ISNULL({ObjectName}.GREENBOOK,'') AND SAQSCO.EQUIPMENT_ID = {ObjectName}.EQUIPMENT_ID AND ISNULL(SAQSCO.PAR_SERVICE_ID,'') = ISNULL({ObjectName}.PAR_SERVICE_ID,'') AND QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID = QTESRVCOB_RECORD_ID
                    {AncillaryJoin}
                    JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = {ObjectName}.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = {ObjectName}.QTEREV_RECORD_ID     
                    JOIN SAQTRV (NOLOCK) ON SAQTRV.SALESORG_RECORD_ID = {ObjectName}.SALESORG_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = {ObjectName}.QTEREV_RECORD_ID AND SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID
                    JOIN SAQRIS (NOLOCK) ON SAQRIS.QTEREV_RECORD_ID = SAQTRV.QUOTE_REVISION_RECORD_ID AND SAQRIS.QUOTE_RECORD_ID = SAQTRV.QUOTE_RECORD_ID AND SAQRIS.SERVICE_ID = {ObjectName}.SERVICE_ID AND ISNULL(SAQRIS.PAR_SERVICE_ID,'') = ISNULL({ObjectName}.PAR_SERVICE_ID,'') {split_quote_condition}					
                    LEFT JOIN MAMSCT (NOLOCK) ON MAMSCT.DISTRIBUTIONCHANNEL_RECORD_ID = SAQTRV.DISTRIBUTIONCHANNEL_RECORD_ID AND MAMSCT.COUNTRY_RECORD_ID = SAQTRV.COUNTRY_RECORD_ID AND MAMSCT.SALESORG_ID = SAQTRV.SALESORG_ID AND MAMSCT.SAP_PART_NUMBER = {ObjectName}.SERVICE_ID AND SAQTRV.ACCTAXCAT_RECORD_ID = MAMSCT.TAXCATEGORY_RECORD_ID
                    WHERE {ObjectName}.QUOTE_RECORD_ID = '{QuoteRecordId}' AND {ObjectName}.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND {ObjectName}.SERVICE_ID = '{ServiceId}' AND ISNULL({ObjectName}.CONFIGURATION_STATUS,'') = 'COMPLETE'  {AncillaryWhere}
                    ) IQ
                    LEFT JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND SAQRIT.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND SAQRIT.SERVICE_RECORD_ID = IQ.SERVICE_RECORD_ID AND SAQRIT.FABLOCATION_RECORD_ID = IQ. FABLOCATION_RECORD_ID AND ISNULL(SAQRIT.GREENBOOK_RECORD_ID,'') = ISNULL(IQ.GREENBOOK_RECORD_ID,'') AND ISNULL(SAQRIT.PAR_PRDOFR_ID,'') = ISNULL(IQ.PAR_PRDOFR_ID,'')  AND ISNULL(SAQRIT.OBJECT_ID,'') = IQ.OBJECT_ID AND ISNULL(SAQRIT.TEMP_TOOL, 'False') = ISNULL(IQ.TEMP_TOOL, 'False') AND SAQRIT.QTESRVCOB_RECORD_ID = IQ.QTESRVCOB_RECORD_ID
                    WHERE ISNULL(SAQRIT.QTESRVCOB_RECORD_ID,'') = ''			
                """.format(UserId=self.user_id, UserName=self.user_name, ObjectName=self.source_object_name, QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id, EquipmentsCount=equipments_count, DynamicValues=dynamic_ancillary_columns,billing_type=self.get_billing_type_val,DynamicColumnNames=dynamic_columns, AncillaryJoin =ancillary_join, AncillaryWhere = ancillary_whr_cond,split_quote_condition = split_quote_condition))
                #INC08898664 End - M
                #A055S000P01-20908,INC09026574 - End - M
            elif self.quote_service_entitlement_type in ('STR-OFFBGB OBJ-GREQ PRD-GRPT','STR-OFFBGB OBJ-GREQ','STR-OFFBGB OBJ-EQ','STR-OFFBGR OBJ-GREQ','STR-OFFBGB OBJ-ASKT') and not self.triggered_from:				
                Sql.RunQuery("""INSERT SAQRIT (QUOTE_REVISION_CONTRACT_ITEM_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified, CONTRACT_VALID_FROM, CONTRACT_VALID_TO, DOC_CURRENCY, DOCURR_RECORD_ID, EXCHANGE_RATE, EXCHANGE_RATE_DATE, EXCHANGE_RATE_RECORD_ID, GL_ACCOUNT_NO, GLOBAL_CURRENCY, GLOBAL_CURRENCY_RECORD_ID, LINE, OBJECT_ID, OBJECT_TYPE, FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID,PAR_PRDOFR_ID,PAR_PRDOFR_RECORD_ID, PROFIT_CENTER, QUANTITY, QUOTE_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, REF_SALESORDER, STATUS, TAXCLASSIFICATION_DESCRIPTION, TAXCLASSIFICATION_ID, TAXCLASSIFICATION_RECORD_ID,TAX_PERCENTAGE,{DynamicColumnNames} GREENBOOK,BILLING_TYPE,GREENBOOK_RECORD_ID, QTEITMSUM_RECORD_ID)
                    SELECT CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REVISION_CONTRACT_ITEM_ID,
                        '{UserName}' AS CPQTABLEENTRYADDEDBY,
                        GETDATE() as CPQTABLEENTRYDATEADDED,
                        {UserId} as CpqTableEntryModifiedBy,
                        GETDATE() as CpqTableEntryDateModified, 
                        OQ.* 
                    FROM (
                        SELECT 
                            DISTINCT
                            SAQTSV.CONTRACT_VALID_FROM,
                            SAQTSV.CONTRACT_VALID_TO,
                            SAQTRV.DOC_CURRENCY,
                            SAQTRV.DOCCURR_RECORD_ID as DOCURR_RECORD_ID,
                            ISNULL(CONVERT(FLOAT,SAQTRV.EXCHANGE_RATE),'') AS EXCHANGE_RATE,
                            SAQTRV.EXCHANGE_RATE_DATE,
                            SAQTRV.EXCHANGERATE_RECORD_ID as EXCHANGE_RATE_RECORD_ID,
                            null as GL_ACCOUNT_NO,
                            SAQTRV.GLOBAL_CURRENCY,
                            SAQTRV.GLOBAL_CURRENCY_RECORD_ID,
                            --ROW_NUMBER()OVER(ORDER BY({ObjectName}.CpqTableEntryId)) + {EquipmentsCount} as LINE,
                            null  as LINE,
                            null as OBJECT_ID,
                            'GREENBOOK' as OBJECT_TYPE,
                            IQ.FABLOCATION_ID as FABLOCATION_ID,
                            IQ.FABLOCATION_NAME as FABLOCATION_NAME,
                            IQ.FABLOCATION_RECORD_ID as FABLOCATION_RECORD_ID,			
                            {ObjectName}.SERVICE_DESCRIPTION,
                            {ObjectName}.SERVICE_ID,
                            {ObjectName}.SERVICE_RECORD_ID,
                            {ObjectName}.PAR_SERVICE_ID AS PAR_PRDOFR_ID,
                            {ObjectName}.PAR_SERVICE_RECORD_ID AS PAR_PRDOFR_RECORD_ID,
                            null as PROFIT_CENTER,
                            1 as QUANTITY,
                            SAQTRV.QUOTE_ID,
                            SAQTRV.QUOTE_RECORD_ID,
                            SAQTMT.QTEREV_ID,
                            SAQTMT.QTEREV_RECORD_ID,
                            null as REF_SALESORDER,
                            CASE WHEN {ObjectName}.SERVICE_ID = 'Z0101' THEN 'ACQUIRED' ELSE 'ACQUIRING' END AS STATUS,
                            MAMSCT.TAXCLASSIFICATION_DESCRIPTION,
                            MAMSCT.TAXCLASSIFICATION_ID,
                            MAMSCT.TAXCLASSIFICATION_RECORD_ID,
                            SAQRIS.TAX_PERCENTAGE,
                            {DynamicValues}					
                            {ObjectName}.GREENBOOK,
                            {ObjectName}.BILTYP as BILLING_TYPE,
                            {ObjectName}.GREENBOOK_RECORD_ID,
                            SAQRIS.QUOTE_REV_ITEM_SUMMARY_RECORD_ID as QTEITMSUM_RECORD_ID
                        FROM (
                            SELECT 
                                QUOTE_RECORD_ID, QTEREV_RECORD_ID, SERVICE_ID, FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID,PAR_SERVICE_ID,PAR_SERVICE_RECORD_ID 
                            FROM SAQSCO (NOLOCK)
                            WHERE SAQSCO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQSCO.SERVICE_ID = '{ServiceId}' 
                            GROUP BY QUOTE_RECORD_ID, QTEREV_RECORD_ID, SERVICE_ID, FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID,PAR_SERVICE_ID,PAR_SERVICE_RECORD_ID 
                        ) IQ
                        JOIN {ObjectName} (NOLOCK) ON {ObjectName}.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND {ObjectName}.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND {ObjectName}.SERVICE_ID = IQ.SERVICE_ID AND {ObjectName}.GREENBOOK_RECORD_ID = IQ.GREENBOOK_RECORD_ID AND ISNULL({ObjectName}.PAR_SERVICE_ID,'') = ISNULL(IQ.PAR_SERVICE_ID,'')
                        {AncillaryJoin}
                        JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = {ObjectName}.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = {ObjectName}.QTEREV_RECORD_ID     
                        JOIN SAQTRV (NOLOCK) ON SAQTRV.SALESORG_RECORD_ID = {ObjectName}.SALESORG_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = {ObjectName}.QTEREV_RECORD_ID AND SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID
                        JOIN SAQTSV (NOLOCK) ON SAQTSV.QTEREV_RECORD_ID = SAQTRV.QUOTE_REVISION_RECORD_ID AND SAQTSV.QUOTE_RECORD_ID = SAQTRV.QUOTE_RECORD_ID AND SAQTSV.SERVICE_ID = {ObjectName}.SERVICE_ID  AND ISNULL(SAQTSV.PAR_SERVICE_ID,'') = ISNULL({ObjectName}.PAR_SERVICE_ID,'')
                        JOIN SAQRIS (NOLOCK) ON SAQRIS.QTEREV_RECORD_ID = SAQTRV.QUOTE_REVISION_RECORD_ID AND SAQRIS.QUOTE_RECORD_ID = SAQTRV.QUOTE_RECORD_ID AND SAQRIS.SERVICE_ID = {ObjectName}.SERVICE_ID AND ISNULL(SAQRIS.PAR_SERVICE_ID,'') = ISNULL({ObjectName}.PAR_SERVICE_ID,'') {split_quote_condition}
                        LEFT JOIN MAMSCT (NOLOCK) ON MAMSCT.DISTRIBUTIONCHANNEL_RECORD_ID = SAQTRV.DISTRIBUTIONCHANNEL_RECORD_ID AND MAMSCT.COUNTRY_RECORD_ID = SAQTRV.COUNTRY_RECORD_ID AND MAMSCT.SALESORG_ID = SAQTRV.SALESORG_ID AND MAMSCT.SAP_PART_NUMBER = {ObjectName}.SERVICE_ID  AND SAQTRV.ACCTAXCAT_RECORD_ID = MAMSCT.TAXCATEGORY_RECORD_ID
                        WHERE {ObjectName}.QUOTE_RECORD_ID = '{QuoteRecordId}' AND {ObjectName}.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND {ObjectName}.SERVICE_ID = '{ServiceId}' AND ISNULL({ObjectName}.CONFIGURATION_STATUS,'') = 'COMPLETE' {AncillaryWhere}
                    ) OQ
                    LEFT JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = OQ.QUOTE_RECORD_ID AND SAQRIT.QTEREV_RECORD_ID = OQ.QTEREV_RECORD_ID AND SAQRIT.SERVICE_RECORD_ID = OQ.SERVICE_RECORD_ID  AND SAQRIT.GREENBOOK_RECORD_ID = OQ.GREENBOOK_RECORD_ID AND ISNULL(SAQRIT.PAR_PRDOFR_ID,'') = ISNULL(OQ.PAR_PRDOFR_ID,'')
                    WHERE ISNULL(SAQRIT.GREENBOOK_RECORD_ID,'') = ''
                """.format(UserId=self.user_id, UserName=self.user_name, ObjectName=self.source_object_name, QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id, EquipmentsCount=equipments_count,billing_type=self.get_billing_type_val, DynamicValues=dynamic_ancillary_columns,DynamicColumnNames=dynamic_columns, AncillaryJoin =ancillary_join, AncillaryWhere = ancillary_whr_cond,split_quote_condition = split_quote_condition))
            elif self.quote_service_entitlement_type == "STR-OFFBGBPMCMKTGCPCND OBJ-AS" and not self.triggered_from:
                Sql.RunQuery("""INSERT SAQRIT (QUOTE_REVISION_CONTRACT_ITEM_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified, CONTRACT_VALID_FROM, CONTRACT_VALID_TO, DOC_CURRENCY, DOCURR_RECORD_ID, EXCHANGE_RATE, EXCHANGE_RATE_DATE, EXCHANGE_RATE_RECORD_ID, GL_ACCOUNT_NO, GLOBAL_CURRENCY, GLOBAL_CURRENCY_RECORD_ID, LINE, OBJECT_ID, OBJECT_TYPE,PM_ID,PM_RECORD_ID,KIT_ID,KIT_NAME,KIT_RECORD_ID,GOTCODE_RECORD_ID,GOT_CODE,MNTEVT_LEVEL, FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, PROFIT_CENTER, QUANTITY, QUOTE_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, REF_SALESORDER, STATUS, TAXCLASSIFICATION_DESCRIPTION, TAXCLASSIFICATION_ID, TAXCLASSIFICATION_RECORD_ID,TAX_PERCENTAGE,{DynamicColumnNames} GREENBOOK,BILLING_TYPE,GREENBOOK_RECORD_ID, QTEITMSUM_RECORD_ID,DEVICE_NODE,PROCESS_TYPE,CHAMBER_QUANTITY,COUNT_OF_ASSEMBLIES)
                    SELECT CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REVISION_CONTRACT_ITEM_ID,
                        '{UserName}' AS CPQTABLEENTRYADDEDBY,
                        GETDATE() as CPQTABLEENTRYDATEADDED,
                        {UserId} as CpqTableEntryModifiedBy,
                        GETDATE() as CpqTableEntryDateModified, 
                        OQ.* 
                    FROM (
                        SELECT 
                            DISTINCT
                            SAQTSV.CONTRACT_VALID_FROM,
                            SAQTSV.CONTRACT_VALID_TO,
                            SAQTRV.DOC_CURRENCY,
                            SAQTRV.DOCCURR_RECORD_ID as DOCURR_RECORD_ID,
                            ISNULL(CONVERT(FLOAT,SAQTRV.EXCHANGE_RATE),'') AS EXCHANGE_RATE,
                            SAQTRV.EXCHANGE_RATE_DATE,
                            SAQTRV.EXCHANGERATE_RECORD_ID as EXCHANGE_RATE_RECORD_ID,
                            null as GL_ACCOUNT_NO,
                            SAQTRV.GLOBAL_CURRENCY,
                            SAQTRV.GLOBAL_CURRENCY_RECORD_ID,
                            --ROW_NUMBER()OVER(ORDER BY(IQ.PM_ID)) + {EquipmentsCount} as LINE,
                            null as LINE,
                            IQ.PM_ID as OBJECT_ID,
                            'EVENT' as OBJECT_TYPE,
                            IQ.PM_ID,
                            IQ.PM_RECORD_ID, 
                            IQ.KIT_ID as KIT_ID,
                            IQ.KIT_NAME as KIT_NAME,
                            IQ.KIT_RECORD_ID as KIT_RECORD_ID,
                                            
                            IQ.GOTCODE_RECORD_ID,
                            IQ.GOT_CODE,
                            IQ.MNTEVT_LEVEL,
                            IQ.FABLOCATION_ID as FABLOCATION_ID,
                            IQ.FABLOCATION_NAME as FABLOCATION_NAME,
                            IQ.FABLOCATION_RECORD_ID as FABLOCATION_RECORD_ID,			
                            IQ.SERVICE_DESCRIPTION,
                            IQ.SERVICE_ID,
                            IQ.SERVICE_RECORD_ID,
                            null as PROFIT_CENTER,
                            1 as QUANTITY,
                            SAQTRV.QUOTE_ID,
                            SAQTRV.QUOTE_RECORD_ID,
                            SAQTMT.QTEREV_ID,
                            SAQTMT.QTEREV_RECORD_ID,
                            null as REF_SALESORDER,
                            'ACQUIRING' as STATUS,
                            MAMSCT.TAXCLASSIFICATION_DESCRIPTION,
                            MAMSCT.TAXCLASSIFICATION_ID,
                            MAMSCT.TAXCLASSIFICATION_RECORD_ID,
                            SAQRIS.TAX_PERCENTAGE,
                            {DynamicValues}					
                            IQ.GREENBOOK,
                            {ObjectName}.BILTYP as BILLING_TYPE,
                            IQ.GREENBOOK_RECORD_ID,
                            SAQRIS.QUOTE_REV_ITEM_SUMMARY_RECORD_ID as QTEITMSUM_RECORD_ID,
                            IQ.DEVICE_NODE as DEVICE_NODE,
                            IQ.PROCESS_TYPE as PROCESS_TYPE,
                            IQ.CHAMBER_QTY AS CHAMBER_QUANTITY,
                            IQ.CHAMBER_QTY AS COUNT_OF_ASSEMBLIES
                        FROM (
                            SELECT SAQGPA.SERVICE_ID,SAQGPA.GREENBOOK,SAQGPA.FABLOCATION_ID,SAQGPA.GOT_CODE,SAQGPA.PM_ID,KIT_ID,KIT_NAME,KIT_RECORD_ID,SAQGPA.QUOTE_RECORD_ID,SAQGPA.QTEREV_RECORD_ID,SAQGPA.PM_RECORD_ID, SAQGPA.GOTCODE_RECORD_ID, SAQGPA.SERVICE_DESCRIPTION, SAQGPA.SERVICE_RECORD_ID, SAQGPA.FABLOCATION_NAME, SAQGPA.FABLOCATION_RECORD_ID,SAQGPA.GREENBOOK_RECORD_ID, ISNULL(PROCESS_TYPE,'') AS PROCESS_TYPE , ISNULL(DEVICE_NODE,'') AS DEVICE_NODE,MNTEVT_LEVEL, COUNT(ISNULL(ASSEMBLY_ID,0)) AS CHAMBER_QTY
                                FROM SAQGPA (NOLOCK) 
                                WHERE SAQGPA.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQGPA.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQGPA.SERVICE_ID = '{ServiceId}' AND SAQGPA.INCLUDED = 1
                                GROUP BY SAQGPA.SERVICE_ID,SAQGPA.GREENBOOK,SAQGPA.FABLOCATION_ID,SAQGPA.GOT_CODE,SAQGPA.PM_ID,KIT_ID,KIT_NAME,KIT_RECORD_ID,SAQGPA.QUOTE_RECORD_ID,SAQGPA.QTEREV_RECORD_ID,SAQGPA.PM_RECORD_ID, SAQGPA.GOTCODE_RECORD_ID,SAQGPA.SERVICE_DESCRIPTION, SAQGPA.SERVICE_RECORD_ID, SAQGPA.FABLOCATION_NAME, SAQGPA.FABLOCATION_RECORD_ID,SAQGPA.GREENBOOK_RECORD_ID, ISNULL(PROCESS_TYPE,'')  , ISNULL(DEVICE_NODE,''),MNTEVT_LEVEL
                                
                        ) IQ
                        JOIN {ObjectName} (NOLOCK) ON {ObjectName}.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND {ObjectName}.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND {ObjectName}.GREENBOOK = IQ.GREENBOOK AND {ObjectName}.GOT_CODE = IQ.GOT_CODE AND {ObjectName}.PM_ID = IQ.PM_ID AND {ObjectName}.KIT_ID = IQ.KIT_ID AND IQ.SERVICE_ID = SAQGPE.SERVICE_ID
                        JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = {ObjectName}.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = {ObjectName}.QTEREV_RECORD_ID     
                        JOIN SAQTRV (NOLOCK) ON SAQTRV.QTEREV_RECORD_ID = {ObjectName}.QTEREV_RECORD_ID AND SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID
                        JOIN SAQTSV (NOLOCK) ON SAQTSV.QTEREV_RECORD_ID = SAQTRV.QUOTE_REVISION_RECORD_ID AND SAQTSV.QUOTE_RECORD_ID = SAQTRV.QUOTE_RECORD_ID AND SAQTSV.SERVICE_ID = IQ.SERVICE_ID
                        JOIN SAQRIS (NOLOCK) ON SAQRIS.QTEREV_RECORD_ID = SAQTRV.QUOTE_REVISION_RECORD_ID AND SAQRIS.QUOTE_RECORD_ID = SAQTRV.QUOTE_RECORD_ID AND SAQRIS.SERVICE_ID = IQ.SERVICE_ID	{split_quote_condition}					
                        LEFT JOIN MAMSCT (NOLOCK) ON MAMSCT.DISTRIBUTIONCHANNEL_RECORD_ID = SAQTRV.DISTRIBUTIONCHANNEL_RECORD_ID AND MAMSCT.COUNTRY_RECORD_ID = SAQTRV.COUNTRY_RECORD_ID AND MAMSCT.SALESORG_ID = SAQTRV.SALESORG_ID AND MAMSCT.SAP_PART_NUMBER = {ObjectName}.SERVICE_ID  AND SAQTRV.ACCTAXCAT_RECORD_ID = MAMSCT.TAXCATEGORY_RECORD_ID
                        WHERE {ObjectName}.QUOTE_RECORD_ID = '{QuoteRecordId}' AND {ObjectName}.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND IQ.SERVICE_ID = '{ServiceId}' AND ISNULL({ObjectName}.CONFIGURATION_STATUS,'') = 'COMPLETE' 
                    ) OQ
                    LEFT JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = OQ.QUOTE_RECORD_ID AND SAQRIT.QTEREV_RECORD_ID = OQ.QTEREV_RECORD_ID AND SAQRIT.SERVICE_RECORD_ID = OQ.SERVICE_RECORD_ID  AND SAQRIT.OBJECT_ID = OQ.OBJECT_ID AND SAQRIT.FABLOCATION_ID = OQ.FABLOCATION_ID AND SAQRIT.GREENBOOK = OQ.GREENBOOK AND SAQRIT.GOT_CODE = OQ.GOT_CODE AND SAQRIT.KIT_ID = OQ.KIT_ID
                    WHERE ISNULL(SAQRIT.OBJECT_ID,'') = ''
                """.format(UserId=self.user_id, UserName=self.user_name, ObjectName=self.source_object_name, QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id, EquipmentsCount=equipments_count,billing_type=self.get_billing_type_val, DynamicValues=dynamic_ancillary_columns,DynamicColumnNames=dynamic_columns,split_quote_condition = split_quote_condition))				
            elif self.quote_service_entitlement_type in ("STR-OFFBGBSMKTGCPCND OBJ-AS") and not self.triggered_from:
                Sql.RunQuery("""INSERT SAQRIT (QUOTE_REVISION_CONTRACT_ITEM_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified, CONTRACT_VALID_FROM, CONTRACT_VALID_TO, DOC_CURRENCY, DOCURR_RECORD_ID, EXCHANGE_RATE, EXCHANGE_RATE_DATE, EXCHANGE_RATE_RECORD_ID, GL_ACCOUNT_NO, GLOBAL_CURRENCY, GLOBAL_CURRENCY_RECORD_ID, LINE, OBJECT_ID, OBJECT_TYPE,PM_ID,PM_RECORD_ID,KIT_ID,KIT_NAME,KIT_RECORD_ID,GOTCODE_RECORD_ID,GOT_CODE,MNTEVT_LEVEL, FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, PROFIT_CENTER, QUANTITY, QUOTE_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, REF_SALESORDER, STATUS, TAXCLASSIFICATION_DESCRIPTION, TAXCLASSIFICATION_ID, TAXCLASSIFICATION_RECORD_ID,TAX_PERCENTAGE,{DynamicColumnNames} GREENBOOK,BILLING_TYPE,GREENBOOK_RECORD_ID, QTEITMSUM_RECORD_ID,DEVICE_NODE,PROCESS_TYPE,CHAMBER_QUANTITY,COUNT_OF_ASSEMBLIES)
                    SELECT CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REVISION_CONTRACT_ITEM_ID,
                        '{UserName}' AS CPQTABLEENTRYADDEDBY,
                        GETDATE() as CPQTABLEENTRYDATEADDED,
                        {UserId} as CpqTableEntryModifiedBy,
                        GETDATE() as CpqTableEntryDateModified, 
                        OQ.* 
                    FROM (
                        SELECT 
                            SAQTSV.CONTRACT_VALID_FROM,
                            SAQTSV.CONTRACT_VALID_TO,
                            SAQTRV.DOC_CURRENCY,
                            SAQTRV.DOCCURR_RECORD_ID as DOCURR_RECORD_ID,
                            ISNULL(CONVERT(FLOAT,SAQTRV.EXCHANGE_RATE),'') AS EXCHANGE_RATE,
                            SAQTRV.EXCHANGE_RATE_DATE,
                            SAQTRV.EXCHANGERATE_RECORD_ID as EXCHANGE_RATE_RECORD_ID,
                            null as GL_ACCOUNT_NO,
                            SAQTRV.GLOBAL_CURRENCY,
                            SAQTRV.GLOBAL_CURRENCY_RECORD_ID,
                            null as LINE,
                            --CASE WHEN IQ.PM_ID = 'Scheduled Maintenance' THEN '' ELSE IQ.PM_ID END as OBJECT_ID,
                            IQ.PM_ID as OBJECT_ID,
                            'EVENT' as OBJECT_TYPE,
                            CASE WHEN IQ.PM_ID = 'Scheduled Maintenance' THEN '' ELSE IQ.PM_ID END as PM_ID,
                            IQ.PM_RECORD_ID as PM_RECORD_ID, 
                            IQ.KIT_ID as KIT_ID,
                            IQ.KIT_NAME as KIT_NAME,
                            IQ.KIT_RECORD_ID as KIT_RECORD_ID,
                                                            
                            IQ.GOTCODE_RECORD_ID,
                            IQ.GOT_CODE,
                            CASE WHEN IQ.PM_ID = 'Scheduled Maintenance' THEN IQ.PM_ID ELSE IQ.LEVEL END as MNTEVT_LEVEL,
                            IQ.FABLOCATION_ID as FABLOCATION_ID,
                            IQ.FABLOCATION_NAME as FABLOCATION_NAME,
                            IQ.FABLOCATION_RECORD_ID as FABLOCATION_RECORD_ID,			
                            IQ.SERVICE_DESCRIPTION,
                            IQ.SERVICE_ID,
                            IQ.SERVICE_RECORD_ID,
                            null as PROFIT_CENTER,
                            1 as QUANTITY,
                            SAQTRV.QUOTE_ID,
                            SAQTRV.QUOTE_RECORD_ID,
                            SAQTMT.QTEREV_ID,
                            SAQTMT.QTEREV_RECORD_ID,
                            null as REF_SALESORDER,
                            'ACQUIRING' as STATUS,
                            MAMSCT.TAXCLASSIFICATION_DESCRIPTION,
                            MAMSCT.TAXCLASSIFICATION_ID,
                            MAMSCT.TAXCLASSIFICATION_RECORD_ID,
                            SAQRIS.TAX_PERCENTAGE,
                            {DynamicValues}					
                            IQ.GREENBOOK,
                            '{billing_type}' as BILLING_TYPE,
                            IQ.GREENBOOK_RECORD_ID,
                            SAQRIS.QUOTE_REV_ITEM_SUMMARY_RECORD_ID as QTEITMSUM_RECORD_ID,
                            IQ.DEVICE_NODE as DEVICE_NODE,
                            IQ.PROCESS_TYPE as PROCESS_TYPE,
                            IQ.CHAMBER_QTY AS CHAMBER_QUANTITY,
                            IQ.CHAMBER_QTY AS COUNT_OF_ASSEMBLIES
                        FROM (
                            SELECT SAQGPA.SERVICE_ID,SAQGPA.GREENBOOK,SAQGPA.FABLOCATION_ID,SAQGPA.GOT_CODE,SAQGPA.PM_ID,SAQGPA.PM_RECORD_ID,SAQGPA.KIT_ID,SAQGPA.KIT_NAME,SAQGPA.KIT_RECORD_ID,SAQGPA.QUOTE_RECORD_ID,SAQGPA.QTEREV_RECORD_ID,SAQGPA.GOTCODE_RECORD_ID, SAQGPA.SERVICE_DESCRIPTION, SAQGPA.SERVICE_RECORD_ID, SAQGPA.FABLOCATION_NAME, SAQGPA.FABLOCATION_RECORD_ID,SAQGPA.GREENBOOK_RECORD_ID, ISNULL(PROCESS_TYPE,'') AS PROCESS_TYPE , ISNULL(DEVICE_NODE,'') AS DEVICE_NODE,CONFIGURATION_STATUS,SAQGPA.MNTEVT_LEVEL as LEVEL, COUNT(ISNULL(ASSEMBLY_ID,0)) AS CHAMBER_QTY
                                FROM SAQGPA (NOLOCK)  
                                JOIN SAQGPE (NOLOCK) ON SAQGPE.QUOTE_RECORD_ID = SAQGPA.QUOTE_RECORD_ID AND SAQGPE.QTEREV_RECORD_ID = SAQGPA.QTEREV_RECORD_ID AND SAQGPE.GREENBOOK = SAQGPA.GREENBOOK AND SAQGPE.GOT_CODE = SAQGPA.GOT_CODE AND SAQGPE.PM_ID  = SAQGPA.PM_ID AND SAQGPE.KIT_ID  = SAQGPA.KIT_ID AND SAQGPA.SERVICE_ID = SAQGPE.SERVICE_ID
                                WHERE SAQGPA.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQGPA.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQGPA.SERVICE_ID = '{ServiceId}' AND MNTEVT_LEVEL != 'Scheduled Maintenance' AND SAQGPA.INCLUDED = 1
                                GROUP BY SAQGPA.SERVICE_ID,SAQGPA.GREENBOOK,SAQGPA.FABLOCATION_ID,SAQGPA.GOT_CODE,SAQGPA.PM_ID,SAQGPA.KIT_ID,SAQGPA.KIT_NAME,SAQGPA.KIT_RECORD_ID,SAQGPA.QUOTE_RECORD_ID,SAQGPA.QTEREV_RECORD_ID,SAQGPA.GOTCODE_RECORD_ID, SAQGPA.SERVICE_DESCRIPTION, SAQGPA.SERVICE_RECORD_ID, SAQGPA.FABLOCATION_NAME, SAQGPA.FABLOCATION_RECORD_ID,SAQGPA.GREENBOOK_RECORD_ID, ISNULL(PROCESS_TYPE,'')  , ISNULL(DEVICE_NODE,''), SAQGPA.PM_RECORD_ID,CONFIGURATION_STATUS,SAQGPA.MNTEVT_LEVEL
                            UNION
                            SELECT SAQGPA.SERVICE_ID,SAQGPA.GREENBOOK,SAQGPA.FABLOCATION_ID,SAQGPA.GOT_CODE,MNTEVT_LEVEL, null as PM_RECORD_ID,SAQGPA.KIT_ID,SAQGPA.KIT_NAME,SAQGPA.KIT_RECORD_ID, SAQGPA.QUOTE_RECORD_ID, SAQGPA.QTEREV_RECORD_ID, SAQGPA.GOTCODE_RECORD_ID, SAQGPA.SERVICE_DESCRIPTION, SAQGPA.SERVICE_RECORD_ID, SAQGPA.FABLOCATION_NAME, SAQGPA.FABLOCATION_RECORD_ID, SAQGPA.GREENBOOK_RECORD_ID, ISNULL(PROCESS_TYPE,'') AS PROCESS_TYPE , ISNULL(DEVICE_NODE,'') AS DEVICE_NODE, CONFIGURATION_STATUS,SAQGPA.MNTEVT_LEVEL as LEVEL, COUNT(ISNULL(ASSEMBLY_ID,0)) AS CHAMBER_QTY
                                FROM SAQGPA (NOLOCK)  
                                JOIN SAQSGE SAQGPE (NOLOCK) ON SAQGPE.QUOTE_RECORD_ID = SAQGPA.QUOTE_RECORD_ID AND SAQGPE.QTEREV_RECORD_ID = SAQGPA.QTEREV_RECORD_ID AND SAQGPE.GREENBOOK = SAQGPA.GREENBOOK  AND SAQGPA.SERVICE_ID = SAQGPE.SERVICE_ID
                                WHERE SAQGPA.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQGPA.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQGPA.SERVICE_ID = '{ServiceId}' AND MNTEVT_LEVEL = 'Scheduled Maintenance' AND SAQGPA.INCLUDED = 1
                                GROUP BY SAQGPA.SERVICE_ID,SAQGPA.GREENBOOK,SAQGPA.FABLOCATION_ID,SAQGPA.GOT_CODE,MNTEVT_LEVEL,SAQGPA.KIT_ID,SAQGPA.KIT_NAME,SAQGPA.KIT_RECORD_ID,SAQGPA.QUOTE_RECORD_ID,SAQGPA.QTEREV_RECORD_ID,SAQGPA.GOTCODE_RECORD_ID, SAQGPA.SERVICE_DESCRIPTION, SAQGPA.SERVICE_RECORD_ID, SAQGPA.FABLOCATION_NAME, SAQGPA.FABLOCATION_RECORD_ID,SAQGPA.GREENBOOK_RECORD_ID,  ISNULL(PROCESS_TYPE,'')  , ISNULL(DEVICE_NODE,''),CONFIGURATION_STATUS	
                                
                        ) IQ
                        JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID     
                        JOIN SAQTRV (NOLOCK) ON SAQTRV.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID
                        JOIN SAQTSV (NOLOCK) ON SAQTSV.QTEREV_RECORD_ID = SAQTRV.QUOTE_REVISION_RECORD_ID AND SAQTSV.QUOTE_RECORD_ID = SAQTRV.QUOTE_RECORD_ID AND SAQTSV.SERVICE_ID = IQ.SERVICE_ID
                        JOIN SAQRIS (NOLOCK) ON SAQRIS.QTEREV_RECORD_ID = SAQTRV.QUOTE_REVISION_RECORD_ID AND SAQRIS.QUOTE_RECORD_ID = SAQTRV.QUOTE_RECORD_ID AND SAQRIS.SERVICE_ID = IQ.SERVICE_ID	{split_quote_condition}					
                        LEFT JOIN MAMSCT (NOLOCK) ON MAMSCT.DISTRIBUTIONCHANNEL_RECORD_ID = SAQTRV.DISTRIBUTIONCHANNEL_RECORD_ID AND MAMSCT.COUNTRY_RECORD_ID = SAQTRV.COUNTRY_RECORD_ID AND MAMSCT.SALESORG_ID = SAQTRV.SALESORG_ID AND MAMSCT.SAP_PART_NUMBER = IQ.SERVICE_ID  AND SAQTRV.ACCTAXCAT_RECORD_ID = MAMSCT.TAXCATEGORY_RECORD_ID
                        WHERE IQ.QUOTE_RECORD_ID = '{QuoteRecordId}' AND IQ.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND IQ.SERVICE_ID = '{ServiceId}' AND ISNULL(IQ.CONFIGURATION_STATUS,'') = 'COMPLETE' 
                    ) OQ
                    LEFT JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = OQ.QUOTE_RECORD_ID AND SAQRIT.QTEREV_RECORD_ID = OQ.QTEREV_RECORD_ID AND SAQRIT.SERVICE_RECORD_ID = OQ.SERVICE_RECORD_ID  AND SAQRIT.FABLOCATION_ID = OQ.FABLOCATION_ID AND SAQRIT.GREENBOOK = OQ.GREENBOOK AND SAQRIT.GOT_CODE = OQ.GOT_CODE AND ISNULL(OQ.OBJECT_ID,'') = ISNULL(SAQRIT.OBJECT_ID,'') AND SAQRIT.KIT_ID = OQ.KIT_ID
                    WHERE ISNULL(SAQRIT.OBJECT_ID,'') = ''
                """.format(UserId=self.user_id, UserName=self.user_name, ObjectName=self.source_object_name, QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id, EquipmentsCount=equipments_count,billing_type=self.get_billing_type_val, DynamicValues=dynamic_ancillary_columns,DynamicColumnNames=dynamic_columns,split_quote_condition = split_quote_condition))			
            elif self.quote_service_entitlement_type in ('STR-OFFBGBKTGCPCND OBJ-GPAS') and not self.triggered_from:
                Sql.RunQuery("""INSERT SAQRIT (QUOTE_REVISION_CONTRACT_ITEM_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified, CONTRACT_VALID_FROM, CONTRACT_VALID_TO, DOC_CURRENCY, DOCURR_RECORD_ID, EXCHANGE_RATE, EXCHANGE_RATE_DATE, EXCHANGE_RATE_RECORD_ID, GL_ACCOUNT_NO, GLOBAL_CURRENCY, GLOBAL_CURRENCY_RECORD_ID, LINE, OBJECT_ID, OBJECT_TYPE,PM_ID,PM_RECORD_ID,GOTCODE_RECORD_ID,GOT_CODE,MNTEVT_LEVEL, FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, PROFIT_CENTER, QUANTITY, QUOTE_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, REF_SALESORDER, STATUS, TAXCLASSIFICATION_DESCRIPTION, TAXCLASSIFICATION_ID, TAXCLASSIFICATION_RECORD_ID,TAX_PERCENTAGE,{DynamicColumnNames} GREENBOOK,BILLING_TYPE,GREENBOOK_RECORD_ID, QTEITMSUM_RECORD_ID,DEVICE_NODE,PROCESS_TYPE,KIT_ID,KIT_NAME,KIT_RECORD_ID,CHAMBER_QUANTITY,COUNT_OF_ASSEMBLIES)
                    SELECT CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REVISION_CONTRACT_ITEM_ID,
                        '{UserName}' AS CPQTABLEENTRYADDEDBY,
                        GETDATE() as CPQTABLEENTRYDATEADDED,
                        {UserId} as CpqTableEntryModifiedBy,
                        GETDATE() as CpqTableEntryDateModified, 
                        OQ.* 
                    FROM (
                        SELECT 
                            DISTINCT
                            SAQTSV.CONTRACT_VALID_FROM,
                            SAQTSV.CONTRACT_VALID_TO,
                            SAQTRV.DOC_CURRENCY,
                            SAQTRV.DOCCURR_RECORD_ID as DOCURR_RECORD_ID,
                            ISNULL(CONVERT(FLOAT,SAQTRV.EXCHANGE_RATE),'') AS EXCHANGE_RATE,
                            SAQTRV.EXCHANGE_RATE_DATE,
                            SAQTRV.EXCHANGERATE_RECORD_ID as EXCHANGE_RATE_RECORD_ID,
                            null as GL_ACCOUNT_NO,
                            SAQTRV.GLOBAL_CURRENCY,
                            SAQTRV.GLOBAL_CURRENCY_RECORD_ID,
                            --ROW_NUMBER()OVER(ORDER BY(IQ.PM_ID)) + {EquipmentsCount} as LINE,
                            null as LINE,
                            NULL as OBJECT_ID,
                            'KIT' as OBJECT_TYPE,
                            null as PM_ID,
                            null as PM_RECORD_ID, 
                            IQ.GOTCODE_RECORD_ID,
                            IQ.GOT_CODE,
                            null as MNTEVT_LEVEL,
                            IQ.FABLOCATION_ID as FABLOCATION_ID,
                            IQ.FABLOCATION_NAME as FABLOCATION_NAME,
                            IQ.FABLOCATION_RECORD_ID as FABLOCATION_RECORD_ID,			
                            IQ.SERVICE_DESCRIPTION,
                            IQ.SERVICE_ID,
                            IQ.SERVICE_RECORD_ID,
                            null as PROFIT_CENTER,
                            1 as QUANTITY,
                            SAQTRV.QUOTE_ID,
                            SAQTRV.QUOTE_RECORD_ID,
                            SAQTMT.QTEREV_ID,
                            SAQTMT.QTEREV_RECORD_ID,
                            null as REF_SALESORDER,
                            'ACQUIRING' as STATUS,
                            MAMSCT.TAXCLASSIFICATION_DESCRIPTION,
                            MAMSCT.TAXCLASSIFICATION_ID,
                            MAMSCT.TAXCLASSIFICATION_RECORD_ID,
                            SAQRIS.TAX_PERCENTAGE,
                            {DynamicValues}					
                            IQ.GREENBOOK,
                            {ObjectName}.BILTYP as BILLING_TYPE,
                            IQ.GREENBOOK_RECORD_ID,
                            SAQRIS.QUOTE_REV_ITEM_SUMMARY_RECORD_ID as QTEITMSUM_RECORD_ID,
                            IQ.DEVICE_NODE as DEVICE_NODE,
                            IQ.PROCESS_TYPE as PROCESS_TYPE,
                            IQ.KIT_ID as KIT_ID,
                            IQ.KIT_NAME as KIT_NAME,
                            IQ.KIT_RECORD_ID as KIT_RECORD_ID,
                            IQ.CHAMBER_QTY AS CHAMBER_QUANTITY,
                            IQ.CHAMBER_QTY AS COUNT_OF_ASSEMBLIES
                        FROM (
                            SELECT SAQGPA.SERVICE_ID, SAQGPA.GREENBOOK, SAQGPA.FABLOCATION_ID, SAQGPA.GOT_CODE, SAQGPA.KIT_ID,SAQGPA.QUOTE_RECORD_ID, SAQGPA.QTEREV_RECORD_ID, SAQGPA.GOTCODE_RECORD_ID,  SAQGPA.SERVICE_DESCRIPTION, SAQGPA.SERVICE_RECORD_ID, SAQGPA.FABLOCATION_NAME, SAQGPA.FABLOCATION_RECORD_ID,SAQGPA.GREENBOOK_RECORD_ID,ISNULL(PROCESS_TYPE,'') AS PROCESS_TYPE , ISNULL(DEVICE_NODE,'') AS DEVICE_NODE,KIT_NAME,KIT_RECORD_ID, COUNT(ISNULL(ASSEMBLY_ID,0)) AS CHAMBER_QTY
                                FROM SAQGPA (NOLOCK)  
                                WHERE SAQGPA.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQGPA.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQGPA.SERVICE_ID = '{ServiceId}'  AND ISNULL(SAQGPA.KIT_ID,'') != '' AND SAQGPA.INCLUDED = 1 
                                GROUP BY SAQGPA.SERVICE_ID,SAQGPA.GREENBOOK,SAQGPA.FABLOCATION_ID,SAQGPA.GOT_CODE,SAQGPA.KIT_ID,SAQGPA.QUOTE_RECORD_ID,SAQGPA.QTEREV_RECORD_ID, SAQGPA.GOTCODE_RECORD_ID, SAQGPA.SERVICE_DESCRIPTION, SAQGPA.SERVICE_RECORD_ID, SAQGPA.FABLOCATION_NAME, SAQGPA.FABLOCATION_RECORD_ID,SAQGPA.GREENBOOK_RECORD_ID,  ISNULL(PROCESS_TYPE,'')  , ISNULL(DEVICE_NODE,''),KIT_NAME,KIT_RECORD_ID
                        ) IQ
                        JOIN {ObjectName} (NOLOCK) ON {ObjectName}.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND {ObjectName}.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND {ObjectName}.GREENBOOK = IQ.GREENBOOK AND {ObjectName}.GOT_CODE = IQ.GOT_CODE AND IQ.SERVICE_ID = SAQGPE.SERVICE_ID
                        JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = {ObjectName}.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = {ObjectName}.QTEREV_RECORD_ID     
                        JOIN SAQTRV (NOLOCK) ON SAQTRV.QTEREV_RECORD_ID = {ObjectName}.QTEREV_RECORD_ID AND SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID
                        JOIN SAQTSV (NOLOCK) ON SAQTSV.QTEREV_RECORD_ID = SAQTRV.QUOTE_REVISION_RECORD_ID AND SAQTSV.QUOTE_RECORD_ID = SAQTRV.QUOTE_RECORD_ID AND SAQTSV.SERVICE_ID = IQ.SERVICE_ID
                        JOIN SAQRIS (NOLOCK) ON SAQRIS.QTEREV_RECORD_ID = SAQTRV.QUOTE_REVISION_RECORD_ID AND SAQRIS.QUOTE_RECORD_ID = SAQTRV.QUOTE_RECORD_ID AND SAQRIS.SERVICE_ID = IQ.SERVICE_ID	{split_quote_condition}					
                        LEFT JOIN MAMSCT (NOLOCK) ON MAMSCT.DISTRIBUTIONCHANNEL_RECORD_ID = SAQTRV.DISTRIBUTIONCHANNEL_RECORD_ID AND MAMSCT.COUNTRY_RECORD_ID = SAQTRV.COUNTRY_RECORD_ID AND MAMSCT.SALESORG_ID = SAQTRV.SALESORG_ID AND MAMSCT.SAP_PART_NUMBER = {ObjectName}.SERVICE_ID  AND SAQTRV.ACCTAXCAT_RECORD_ID = MAMSCT.TAXCATEGORY_RECORD_ID
                        WHERE {ObjectName}.QUOTE_RECORD_ID = '{QuoteRecordId}' AND {ObjectName}.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND IQ.SERVICE_ID = '{ServiceId}' AND ISNULL({ObjectName}.CONFIGURATION_STATUS,'') = 'COMPLETE' 
                    ) OQ
                    LEFT JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = OQ.QUOTE_RECORD_ID AND SAQRIT.QTEREV_RECORD_ID = OQ.QTEREV_RECORD_ID AND SAQRIT.SERVICE_RECORD_ID = OQ.SERVICE_RECORD_ID  AND SAQRIT.KIT_ID = OQ.KIT_ID AND SAQRIT.FABLOCATION_ID = OQ.FABLOCATION_ID AND SAQRIT.GREENBOOK = OQ.GREENBOOK AND SAQRIT.GOT_CODE = OQ.GOT_CODE
                    WHERE ISNULL(SAQRIT.KIT_ID,'') = ''
                """.format(UserId=self.user_id, UserName=self.user_name, ObjectName=self.source_object_name, QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id, EquipmentsCount=equipments_count,billing_type=self.get_billing_type_val, DynamicValues=dynamic_ancillary_columns,DynamicColumnNames=dynamic_columns,split_quote_condition = split_quote_condition))	
                # ##kit number 
                
                # Sql.RunQuery("""UPDATE SAQRIT SET KIT_NUMBER = SAQGPA.KIT_NUMBER,
                #                 KITNUMBER_RECORD_ID = SAQGPA.KITNUMBER_RECORD_ID
                #                 FROM SAQRIT (NOLOCK) 
                #                 INNER JOIN SAQGPA ON SAQGPA.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND SAQGPA.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID AND SAQGPA.SERVICE_ID = SAQRIT.SERVICE_ID AND SAQGPA.FABLOCATION_ID = SAQRIT.FABLOCATION_ID AND SAQGPA.GREENBOOK = SAQRIT.GREENBOOK AND SAQGPA.KIT_ID = SAQRIT.KIT_ID AND SAQGPA.GOT_CODE = SAQRIT.GOT_CODE AND ISNULL(SAQGPA.PROCESS_TYPE,'')= ISNULL(SAQRIT.PROCESS_TYPE,'') AND ISNULL(SAQGPA.DEVICE_NODE,'') = ISNULL(SAQRIT.DEVICE_NODE,'')
                #                 WHERE SAQRIT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQRIT.SERVICE_ID = '{ServiceId}' AND ISNULL(SAQGPA.KIT_ID,'') != ''""".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id)
                # )
            ##saqrit quantity update					
            elif self.quote_service_entitlement_type == 'STR-OFFBGBCRSOGL OBJ-GREQ' and not self.triggered_from:
                #1917 starts
                check_equipment_count = Sql.GetFirst("SELECT count(*) as cnt FROM SAQSCO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}'".format(QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
                #A055S000P01-20305
                check_event_count = Sql.GetFirst("SELECT COUNT(*) AS CNT FROM SAQSGE (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SERVICE_ID IN (SELECT PAR_SERVICE_ID FROM SAQTSV WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}' ) AND QTETYP IN ('Flex Event Based','Event Based') ".format(QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
                if check_equipment_count.cnt != 0 or check_event_count.CNT != 0:
                #1917 ends
                    Sql.RunQuery("""INSERT SAQRIT (QUOTE_REVISION_CONTRACT_ITEM_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified, CONTRACT_VALID_FROM, CONTRACT_VALID_TO, DOC_CURRENCY, DOCURR_RECORD_ID, EXCHANGE_RATE, EXCHANGE_RATE_DATE, EXCHANGE_RATE_RECORD_ID, GL_ACCOUNT_NO,DIVISION_ID,DIVISION_RECORD_ID, GLOBAL_CURRENCY, GLOBAL_CURRENCY_RECORD_ID, LINE, OBJECT_ID, OBJECT_TYPE, FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID,PAR_PRDOFR_ID,PAR_PRDOFR_RECORD_ID, PROFIT_CENTER, QUANTITY, QUOTE_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, REF_SALESORDER, STATUS, TAXCLASSIFICATION_DESCRIPTION, TAXCLASSIFICATION_ID, TAXCLASSIFICATION_RECORD_ID,TAX_PERCENTAGE,NET_VALUE_INGL_CURR, NET_PRICE_INGL_CURR,NET_PRICE,YEAR_1_INGL_CURR,YEAR_1,COMVAL_INGL_CURR,ESTVAL_INGL_CURR,COMMITTED_VALUE,ESTIMATED_VALUE, GREENBOOK,BILLING_TYPE,GREENBOOK_RECORD_ID, QTEITMSUM_RECORD_ID)
                        SELECT CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REVISION_CONTRACT_ITEM_ID,
                            '{UserName}' AS CPQTABLEENTRYADDEDBY,
                            GETDATE() as CPQTABLEENTRYDATEADDED,
                            {UserId} as CpqTableEntryModifiedBy,
                            GETDATE() as CpqTableEntryDateModified, 
                            OQ.* 
                        FROM (
                            SELECT 
                                DISTINCT
                                SAQTSV.CONTRACT_VALID_FROM,
                                SAQTSV.CONTRACT_VALID_TO,
                                SAQTRV.DOC_CURRENCY,
                                SAQTRV.DOCCURR_RECORD_ID as DOCURR_RECORD_ID,
                                ISNULL(CONVERT(FLOAT,SAQTRV.EXCHANGE_RATE),'') AS EXCHANGE_RATE,
                                SAQTRV.EXCHANGE_RATE_DATE,
                                SAQTRV.EXCHANGERATE_RECORD_ID as EXCHANGE_RATE_RECORD_ID,
                                IQ.GL_ACCOUNT_NO as GL_ACCOUNT_NO,
                                IQ.DIVISION_ID,
                                IQ.DIVISION_RECORD_ID,
                                SAQTRV.GLOBAL_CURRENCY,
                                SAQTRV.GLOBAL_CURRENCY_RECORD_ID,
                                NULL as LINE,
                                null as OBJECT_ID,
                                'GREENBOOK' as OBJECT_TYPE,
                                null as FABLOCATION_ID,
                                null as FABLOCATION_NAME,
                                null as FABLOCATION_RECORD_ID,			
                                {ObjectName}.SERVICE_DESCRIPTION,
                                {ObjectName}.SERVICE_ID,
                                {ObjectName}.SERVICE_RECORD_ID,
                                {ObjectName}.PAR_SERVICE_ID AS PAR_PRDOFR_ID,
                                {ObjectName}.PAR_SERVICE_RECORD_ID AS PAR_PRDOFR_RECORD_ID,
                                null as PROFIT_CENTER,
                                1 as QUANTITY,
                                SAQTRV.QUOTE_ID,
                                SAQTRV.QUOTE_RECORD_ID,
                                SAQTMT.QTEREV_ID,
                                SAQTMT.QTEREV_RECORD_ID,
                                IQ.SALESORDER_NO as REF_SALESORDER,
                                --SAQTMT.ACCOUNT_ID as REF_SALESORDER,
                                'ACQUIRED' AS STATUS,
                                MAMSCT.TAXCLASSIFICATION_DESCRIPTION,
                                MAMSCT.TAXCLASSIFICATION_ID,
                                MAMSCT.TAXCLASSIFICATION_RECORD_ID,
                                SAQRIS.TAX_PERCENTAGE,
                                '0' AS NET_VALUE_INGL_CURR, 
                                '0' AS NET_PRICE_INGL_CURR,
                                '0' AS NET_PRICE,
                                --CONCAT('-',IQ.CREDIT_APPLIED_INGL_CURR) AS NET_PRICE_INGL_CURR,
                                --CONCAT('-',IQ.CREDIT_APPLIED_INGL_CURR) AS NET_PRICE,
                                '0' AS YEAR_1_INGL_CURR,
                                '0' AS YEAR_1,
                                --IQ.CREDIT_APPLIED_INGL_CURR AS YEAR_1_INGL_CURR,
                                --IQ.CREDIT_APPLIED_INGL_CURR AS YEAR_1,
                                '0' AS COMVAL_INGL_CURR ,
                                '0' AS ESTVAL_INGL_CURR,
                                '0' AS COMMITTED_VALUE,
                                '0' AS ESTIMATED_VALUE,
                                {ObjectName}.GREENBOOK,
                                {ObjectName}.BILTYP as BILLING_TYPE,
                                {ObjectName}.GREENBOOK_RECORD_ID,
                                SAQRIS.QUOTE_REV_ITEM_SUMMARY_RECORD_ID as QTEITMSUM_RECORD_ID
                            FROM (
                                SELECT 
                                    QUOTE_RECORD_ID, QTEREV_RECORD_ID, SERVICE_ID, GREENBOOK, GREENBOOK_RECORD_ID,GL_ACCOUNT_NO,SALESORDER_NO,DIVISION_ID,DIVISION_RECORD_ID
                                FROM SAQRCV (NOLOCK)
                                WHERE SAQRCV.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRCV.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQRCV.SERVICE_ID = '{ServiceId}' 
                                GROUP BY QUOTE_RECORD_ID, QTEREV_RECORD_ID, SERVICE_ID, GREENBOOK, GREENBOOK_RECORD_ID,GL_ACCOUNT_NO,SALESORDER_NO,DIVISION_ID,DIVISION_RECORD_ID
                            ) IQ
                            JOIN {ObjectName} (NOLOCK) ON {ObjectName}.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND {ObjectName}.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND {ObjectName}.SERVICE_ID = IQ.SERVICE_ID AND {ObjectName}.GREENBOOK_RECORD_ID = IQ.GREENBOOK_RECORD_ID 
                            
                            JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = {ObjectName}.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = {ObjectName}.QTEREV_RECORD_ID     
                            JOIN SAQTRV (NOLOCK) ON SAQTRV.SALESORG_RECORD_ID = {ObjectName}.SALESORG_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = {ObjectName}.QTEREV_RECORD_ID AND SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID
                            JOIN SAQTSV (NOLOCK) ON SAQTSV.QTEREV_RECORD_ID = SAQTRV.QUOTE_REVISION_RECORD_ID AND SAQTSV.QUOTE_RECORD_ID = SAQTRV.QUOTE_RECORD_ID AND SAQTSV.SERVICE_ID = {ObjectName}.SERVICE_ID  AND ISNULL(SAQTSV.PAR_SERVICE_ID,'') = ISNULL({ObjectName}.PAR_SERVICE_ID,'')
                            JOIN SAQRIS (NOLOCK) ON SAQRIS.QTEREV_RECORD_ID = SAQTRV.QUOTE_REVISION_RECORD_ID AND SAQRIS.QUOTE_RECORD_ID = SAQTRV.QUOTE_RECORD_ID AND SAQRIS.SERVICE_ID = {ObjectName}.SERVICE_ID AND ISNULL(SAQRIS.PAR_SERVICE_ID,'') = ISNULL({ObjectName}.PAR_SERVICE_ID,'') {split_quote_condition}	
                            LEFT JOIN MAMSCT (NOLOCK) ON MAMSCT.DISTRIBUTIONCHANNEL_RECORD_ID = SAQTRV.DISTRIBUTIONCHANNEL_RECORD_ID AND MAMSCT.COUNTRY_RECORD_ID = SAQTRV.COUNTRY_RECORD_ID AND MAMSCT.SALESORG_ID = SAQTRV.SALESORG_ID AND MAMSCT.SAP_PART_NUMBER = {ObjectName}.SERVICE_ID  AND SAQTRV.ACCTAXCAT_RECORD_ID = MAMSCT.TAXCATEGORY_RECORD_ID
                            WHERE {ObjectName}.QUOTE_RECORD_ID = '{QuoteRecordId}' AND {ObjectName}.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND {ObjectName}.SERVICE_ID = '{ServiceId}' AND ISNULL({ObjectName}.CONFIGURATION_STATUS,'') = 'COMPLETE' 
                        ) OQ
                        LEFT JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = OQ.QUOTE_RECORD_ID AND SAQRIT.QTEREV_RECORD_ID = OQ.QTEREV_RECORD_ID AND SAQRIT.SERVICE_RECORD_ID = OQ.SERVICE_RECORD_ID  AND SAQRIT.GREENBOOK_RECORD_ID = OQ.GREENBOOK_RECORD_ID AND ISNULL(SAQRIT.PAR_PRDOFR_ID,'') = ISNULL(OQ.PAR_PRDOFR_ID,'')
                        WHERE ISNULL(SAQRIT.GREENBOOK_RECORD_ID,'') = ''
                    """.format(UserId=self.user_id, UserName=self.user_name, ObjectName=self.source_object_name, QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id, EquipmentsCount=equipments_count,billing_type=self.get_billing_type_val, par_service_id = self.parent_service_id,split_quote_condition = split_quote_condition))		
            #INC08702009 M    
            elif self.quote_service_entitlement_type == 'STR-OFFBGBEQAS OBJ-AS' and not self.triggered_from:
                #INC09026574 - Start - M
                Sql.RunQuery("""INSERT SAQRIT (QUOTE_REVISION_CONTRACT_ITEM_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified, CONTRACT_VALID_FROM, CONTRACT_VALID_TO, DOC_CURRENCY, DOCURR_RECORD_ID, EXCHANGE_RATE, EXCHANGE_RATE_DATE, EXCHANGE_RATE_RECORD_ID, GL_ACCOUNT_NO, GLOBAL_CURRENCY, GLOBAL_CURRENCY_RECORD_ID, LINE, OBJECT_ID, OBJECT_TYPE, FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, PROFIT_CENTER, QUANTITY, QUOTE_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, REF_SALESORDER, STATUS, TAXCLASSIFICATION_DESCRIPTION, TAXCLASSIFICATION_ID, TAXCLASSIFICATION_RECORD_ID,TAX_PERCENTAGE,{DynamicColumnNames} GREENBOOK,ASSEMBLY_ID,ASSEMBLY_RECORD_ID,EQUIPMENT_ID,EQUIPMENT_RECORD_ID,BILLING_TYPE,GREENBOOK_RECORD_ID,QTESRVCOB_RECORD_ID, QTEITMSUM_RECORD_ID)
                    SELECT CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REVISION_CONTRACT_ITEM_ID,
                        '{UserName}' AS CPQTABLEENTRYADDEDBY,
                        GETDATE() as CPQTABLEENTRYDATEADDED,
                        {UserId} as CpqTableEntryModifiedBy,
                        GETDATE() as CpqTableEntryDateModified, 
                        IQ.* FROM (
                    SELECT
                        DISTINCT
                        SAQTSV.CONTRACT_VALID_FROM,
                        SAQTSV.CONTRACT_VALID_TO,
                        SAQTRV.DOC_CURRENCY,
                        SAQTRV.DOCCURR_RECORD_ID as DOCURR_RECORD_ID,
                        ISNULL(CONVERT(FLOAT,SAQTRV.EXCHANGE_RATE),'') AS EXCHANGE_RATE,
                        SAQTRV.EXCHANGE_RATE_DATE,
                        SAQTRV.EXCHANGERATE_RECORD_ID as EXCHANGE_RATE_RECORD_ID,
                        null as GL_ACCOUNT_NO,
                        SAQTRV.GLOBAL_CURRENCY,
                        SAQTRV.GLOBAL_CURRENCY_RECORD_ID,
                        --ROW_NUMBER()OVER(ORDER BY(SAQSCE.CpqTableEntryId)) + {EquipmentsCount} as LINE,
                        null as LINE,
                        SAQSCA.ASSEMBLY_ID as OBJECT_ID,
                        'ASSEMBLY' as OBJECT_TYPE,
                        SAQSCE.FABLOCATION_ID as FABLOCATION_ID,
                        SAQSCE.FABLOCATION_NAME as FABLOCATION_NAME,
                        SAQSCE.FABLOCATION_RECORD_ID as FABLOCATION_RECORD_ID,			
                        SAQSCE.SERVICE_DESCRIPTION,
                        SAQSCE.SERVICE_ID,
                        SAQSCE.SERVICE_RECORD_ID,
                        null as PROFIT_CENTER,
                        1 as QUANTITY,
                        SAQTRV.QUOTE_ID,
                        SAQTRV.QUOTE_RECORD_ID,
                        SAQTMT.QTEREV_ID,
                        SAQTMT.QTEREV_RECORD_ID,
                        null as REF_SALESORDER,
                        null as STATUS,
                        MAMSCT.TAXCLASSIFICATION_DESCRIPTION,
                        MAMSCT.TAXCLASSIFICATION_ID,
                        MAMSCT.TAXCLASSIFICATION_RECORD_ID,
                        SAQRIS.TAX_PERCENTAGE,
                        {DynamicValues}					
                        SAQSCE.GREENBOOK,
                        SAQSCA.ASSEMBLY_ID,
                        SAQSCA.ASSEMBLY_RECORD_ID,
                        SAQSCE.EQUIPMENT_ID,
                        SAQSCE.EQUIPMENT_RECORD_ID,
                        SAQSCE.BILTYP as BILLING_TYPE,
                        SAQSCE.GREENBOOK_RECORD_ID,
                        SAQSCA.QTESRVCOB_RECORD_ID,
                        SAQRIS.QUOTE_REV_ITEM_SUMMARY_RECORD_ID as QTEITMSUM_RECORD_ID
                    FROM SAQSCE (NOLOCK) 
                    INNER JOIN SAQSCA ON SAQSCE.QUOTE_RECORD_ID = SAQSCA.QUOTE_RECORD_ID AND SAQSCE.QTEREV_RECORD_ID = 	SAQSCA.QTEREV_RECORD_ID AND SAQSCE.SERVICE_RECORD_ID = SAQSCA.SERVICE_RECORD_ID AND SAQSCE.FABLOCATION_RECORD_ID = SAQSCA. FABLOCATION_RECORD_ID AND SAQSCE.EQUIPMENT_ID = SAQSCA.EQUIPMENT_ID AND SAQSCA.INCLUDED = 1 AND SAQSCE.QTESRVCOB_RECORD_ID = SAQSCA.QTESRVCOB_RECORD_ID
                    JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQSCE.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = SAQSCE.QTEREV_RECORD_ID     
                    JOIN SAQTRV (NOLOCK) ON SAQTRV.SALESORG_RECORD_ID = SAQSCE.SALESORG_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = SAQSCE.QTEREV_RECORD_ID AND SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID
                    JOIN SAQTSV (NOLOCK) ON SAQTSV.QTEREV_RECORD_ID = SAQTRV.QUOTE_REVISION_RECORD_ID AND SAQTSV.QUOTE_RECORD_ID = SAQTRV.QUOTE_RECORD_ID AND SAQTSV.SERVICE_ID = SAQSCE.SERVICE_ID
                    JOIN SAQRIS (NOLOCK) ON SAQRIS.QTEREV_RECORD_ID = SAQTRV.QUOTE_REVISION_RECORD_ID AND SAQRIS.QUOTE_RECORD_ID = SAQTRV.QUOTE_RECORD_ID AND SAQRIS.SERVICE_ID = SAQSCE.SERVICE_ID {split_quote_condition}					
                    LEFT JOIN MAMSCT (NOLOCK) ON MAMSCT.DISTRIBUTIONCHANNEL_RECORD_ID = SAQTRV.DISTRIBUTIONCHANNEL_RECORD_ID AND MAMSCT.COUNTRY_RECORD_ID = SAQTRV.COUNTRY_RECORD_ID AND MAMSCT.SALESORG_ID = SAQTRV.SALESORG_ID AND MAMSCT.SAP_PART_NUMBER = SAQSCE.SERVICE_ID AND SAQTRV.ACCTAXCAT_RECORD_ID = MAMSCT.TAXCATEGORY_RECORD_ID
                    WHERE SAQSCE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCE.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQSCE.SERVICE_ID = '{ServiceId}' AND ISNULL(SAQSCE.CONFIGURATION_STATUS,'') = 'COMPLETE' AND SAQSCA.INCLUDED = 1
                    ) IQ
                    LEFT JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND SAQRIT.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND SAQRIT.SERVICE_RECORD_ID = IQ.SERVICE_RECORD_ID AND SAQRIT.FABLOCATION_RECORD_ID = IQ. FABLOCATION_RECORD_ID AND ISNULL(SAQRIT.GREENBOOK_RECORD_ID,'') = ISNULL(IQ.GREENBOOK_RECORD_ID,'') AND ISNULL(SAQRIT.OBJECT_ID,'') = IQ.OBJECT_ID AND SAQRIT.QTESRVCOB_RECORD_ID = IQ.QTESRVCOB_RECORD_ID
                    WHERE ISNULL(SAQRIT.OBJECT_ID,'') = ''			
                """.format(UserId=self.user_id, UserName=self.user_name, ObjectName=self.source_object_name, QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id, EquipmentsCount=equipments_count, DynamicValues=dynamic_ancillary_columns,billing_type=self.get_billing_type_val,DynamicColumnNames=dynamic_columns,split_quote_condition = split_quote_condition))
                #INC09026574 - End - M
            #INC08702009 M
            elif self.quote_service_entitlement_type == 'STR-OFFBGREQPODV OBJ-EQ' and not self.triggered_from:
                #INC09026574,A055S000P01-21015 - Start - M
                Sql.RunQuery("""INSERT SAQRIT (QUOTE_REVISION_CONTRACT_ITEM_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified, CONTRACT_VALID_FROM, CONTRACT_VALID_TO, DOC_CURRENCY, DOCURR_RECORD_ID, EXCHANGE_RATE, EXCHANGE_RATE_DATE, EXCHANGE_RATE_RECORD_ID, GL_ACCOUNT_NO, GLOBAL_CURRENCY, GLOBAL_CURRENCY_RECORD_ID, LINE, EQUIPMENT_ID, EQUIPMENT_RECORD_ID, OBJECT_ID, POSS_NSO_PART_ID, OBJECT_TYPE, FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID,PAR_PRDOFR_ID, PAR_PRDOFR_RECORD_ID,PROFIT_CENTER, QUANTITY, QUOTE_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, REF_SALESORDER, STATUS, TAXCLASSIFICATION_DESCRIPTION, TAXCLASSIFICATION_ID, TAXCLASSIFICATION_RECORD_ID,TAX_PERCENTAGE,NET_VALUE_INGL_CURR, NET_PRICE_INGL_CURR,NET_PRICE,YEAR_1_INGL_CURR,YEAR_1,COMVAL_INGL_CURR,ESTVAL_INGL_CURR,COMMITTED_VALUE,ESTIMATED_VALUE, GREENBOOK,BILLING_TYPE,GREENBOOK_RECORD_ID, QTESRVCOB_RECORD_ID,TEMP_TOOL,QTEITMSUM_RECORD_ID, BUSINESS_UNIT)
                    SELECT CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REVISION_CONTRACT_ITEM_ID,
                        '{UserName}' AS CPQTABLEENTRYADDEDBY,
                        GETDATE() as CPQTABLEENTRYDATEADDED,
                        {UserId} as CpqTableEntryModifiedBy,
                        GETDATE() as CpqTableEntryDateModified, 
                        OQ.* 
                    FROM (
                        SELECT 
                            DISTINCT
                            SAQTSV.CONTRACT_VALID_FROM,
                            SAQTSV.CONTRACT_VALID_TO,
                            SAQTRV.DOC_CURRENCY,
                            SAQTRV.DOCCURR_RECORD_ID as DOCURR_RECORD_ID,
                            ISNULL(CONVERT(FLOAT,SAQTRV.EXCHANGE_RATE),'') AS EXCHANGE_RATE,
                            SAQTRV.EXCHANGE_RATE_DATE,
                            SAQTRV.EXCHANGERATE_RECORD_ID as EXCHANGE_RATE_RECORD_ID,
                            null as GL_ACCOUNT_NO,
                            SAQTRV.GLOBAL_CURRENCY,
                            SAQTRV.GLOBAL_CURRENCY_RECORD_ID,
                            --ROW_NUMBER()OVER(ORDER BY({ObjectName}.CpqTableEntryId)) + {EquipmentsCount} as LINE,
                            null as LINE,
                            SAQSCE.EQUIPMENT_ID as EQUIPMENT_ID,
                            SAQSCE.EQUIPMENT_RECORD_ID as EQUIPMENT_RECORD_ID,
                            IQ.POSS_NSO_PART_ID as OBJECT_ID,
                            IQ.POSS_NSO_PART_ID, 
                            'NSO' as OBJECT_TYPE,
                            {ObjectName}.FABLOCATION_ID,
                            {ObjectName}.FABLOCATION_NAME,
                            {ObjectName}.FABLOCATION_RECORD_ID,			
                            {ObjectName}.SERVICE_DESCRIPTION,
                            {ObjectName}.SERVICE_ID,
                            {ObjectName}.SERVICE_RECORD_ID,
                            {ObjectName}.PAR_SERVICE_ID AS PAR_PRDOFR_ID,
                            {ObjectName}.PAR_SERVICE_RECORD_ID AS PAR_PRDOFR_RECORD_ID,
                            null as PROFIT_CENTER,
                            null as QUANTITY,
                            SAQTRV.QUOTE_ID,
                            SAQTRV.QUOTE_RECORD_ID,
                            SAQTMT.QTEREV_ID,
                            SAQTMT.QTEREV_RECORD_ID,
                            null as REF_SALESORDER,
                            'ACQUIRED' AS STATUS,
                            MAMSCT.TAXCLASSIFICATION_DESCRIPTION,
                            MAMSCT.TAXCLASSIFICATION_ID,
                            MAMSCT.TAXCLASSIFICATION_RECORD_ID,
                            SAQRIS.TAX_PERCENTAGE,
                            '0' AS NET_VALUE_INGL_CURR, 
                            '0' AS NET_PRICE_INGL_CURR,
                            '0' AS NET_PRICE,
                            '0' AS YEAR_1_INGL_CURR,
                            '0' AS YEAR_1,
                            '0' AS COMVAL_INGL_CURR ,
                            '0' AS ESTVAL_INGL_CURR,
                            '0' AS COMMITTED_VALUE,
                            '0' AS ESTIMATED_VALUE,
                            {ObjectName}.GREENBOOK,
                            {ObjectName}.BILTYP as BILLING_TYPE,
                            {ObjectName}.GREENBOOK_RECORD_ID,
                            IQ.QTESRVCOB_RECORD_ID,
                            SAQSCO.TEMP_TOOL,
                            SAQRIS.QUOTE_REV_ITEM_SUMMARY_RECORD_ID as QTEITMSUM_RECORD_ID,
                            IQ.BUSINESS_UNIT
                        FROM (
                            SELECT 
                                QUOTE_RECORD_ID, QTEREV_RECORD_ID, SERVICE_ID, GREENBOOK, FABLOCATION_ID, EQUIPMENT_ID, POSS_NSO_PART_ID, BUSINESS_UNIT,QTESRVCOB_RECORD_ID
                            FROM SAQSCN (NOLOCK)
                            WHERE SAQSCN.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCN.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQSCN.SERVICE_ID = '{ServiceId}' AND SAQSCN.INCLUDED = 1 AND SAQSCN.QUANTITY > 0
                            GROUP BY QUOTE_RECORD_ID, QTEREV_RECORD_ID, SERVICE_ID, GREENBOOK, FABLOCATION_ID, EQUIPMENT_ID, QUANTITY, POSS_NSO_PART_ID, BUSINESS_UNIT,QTESRVCOB_RECORD_ID
                        ) IQ
                        JOIN {ObjectName} (NOLOCK) ON {ObjectName}.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND {ObjectName}.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND {ObjectName}.SERVICE_ID = IQ.SERVICE_ID AND {ObjectName}.GREENBOOK = IQ.GREENBOOK AND {ObjectName}.FABLOCATION_ID = IQ.FABLOCATION_ID AND SAQSCE.EQUIPMENT_ID = IQ.EQUIPMENT_ID  AND {ObjectName}.QTESRVCOB_RECORD_ID = IQ.QTESRVCOB_RECORD_ID
                        JOIN SAQSCO (NOLOCK) ON {ObjectName}.QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID AND {ObjectName}.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID AND {ObjectName}.SERVICE_ID = SAQSCO.SERVICE_ID AND {ObjectName}.GREENBOOK = SAQSCO.GREENBOOK AND {ObjectName}.FABLOCATION_ID = SAQSCO.FABLOCATION_ID AND SAQSCE.EQUIPMENT_ID = SAQSCO.EQUIPMENT_ID  AND {ObjectName}.QTESRVCOB_RECORD_ID = SAQSCO.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID
                        JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = {ObjectName}.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = {ObjectName}.QTEREV_RECORD_ID     
                        JOIN SAQTRV (NOLOCK) ON SAQTRV.SALESORG_RECORD_ID = {ObjectName}.SALESORG_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = {ObjectName}.QTEREV_RECORD_ID AND SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID
                        JOIN SAQTSV (NOLOCK) ON SAQTSV.QTEREV_RECORD_ID = SAQTRV.QUOTE_REVISION_RECORD_ID AND SAQTSV.QUOTE_RECORD_ID = SAQTRV.QUOTE_RECORD_ID AND SAQTSV.SERVICE_ID = {ObjectName}.SERVICE_ID AND ISNULL(SAQTSV.PAR_SERVICE_ID,'') = ISNULL({ObjectName}.PAR_SERVICE_ID,'')
                        JOIN SAQRIS (NOLOCK) ON SAQRIS.QTEREV_RECORD_ID = SAQTRV.QUOTE_REVISION_RECORD_ID AND SAQRIS.QUOTE_RECORD_ID = SAQTRV.QUOTE_RECORD_ID AND SAQRIS.SERVICE_ID = {ObjectName}.SERVICE_ID  AND ISNULL(SAQRIS.PAR_SERVICE_ID,'') = ISNULL({ObjectName}.PAR_SERVICE_ID,'') {split_quote_condition}			
                        LEFT JOIN MAMSCT (NOLOCK) ON MAMSCT.DISTRIBUTIONCHANNEL_RECORD_ID = SAQTRV.DISTRIBUTIONCHANNEL_RECORD_ID AND MAMSCT.COUNTRY_RECORD_ID = SAQTRV.COUNTRY_RECORD_ID AND MAMSCT.SALESORG_ID = SAQTRV.SALESORG_ID AND MAMSCT.SAP_PART_NUMBER = {ObjectName}.SERVICE_ID  AND SAQTRV.ACCTAXCAT_RECORD_ID = MAMSCT.TAXCATEGORY_RECORD_ID
                        WHERE {ObjectName}.QUOTE_RECORD_ID = '{QuoteRecordId}' AND {ObjectName}.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND {ObjectName}.SERVICE_ID = '{ServiceId}' AND ISNULL({ObjectName}.CONFIGURATION_STATUS,'') = 'COMPLETE' 
                    ) OQ
                    LEFT JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = OQ.QUOTE_RECORD_ID AND SAQRIT.QTEREV_RECORD_ID = OQ.QTEREV_RECORD_ID AND SAQRIT.SERVICE_RECORD_ID = OQ.SERVICE_RECORD_ID  AND SAQRIT.GREENBOOK_RECORD_ID = OQ.GREENBOOK_RECORD_ID AND SAQRIT.EQUIPMENT_RECORD_ID = OQ.EQUIPMENT_RECORD_ID AND SAQRIT.POSS_NSO_PART_ID = OQ.POSS_NSO_PART_ID AND ISNULL(SAQRIT.PAR_PRDOFR_ID,'') = ISNULL(OQ.PAR_PRDOFR_ID,'') AND SAQRIT.QTESRVCOB_RECORD_ID = OQ.QTESRVCOB_RECORD_ID
                    WHERE ISNULL(SAQRIT.POSS_NSO_PART_ID,'') = '' AND ISNULL(SAQRIT.QTESRVCOB_RECORD_ID,'') = ''
                """.format(UserId=self.user_id, UserName=self.user_name, ObjectName=self.source_object_name, QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id, EquipmentsCount=equipments_count,billing_type=self.get_billing_type_val, par_service_id = self.parent_service_id,split_quote_condition = split_quote_condition))				
            
            ##ordering line field in saqrit
            self._ordering_item_line_no()
            # Item Level entitlement Insert
            if self.quote_service_entitlement_type in ('OFFERING+CONSIGNED+ON REQUEST','STR-OF PRD-GRPT'):
                self._service_based_quote_items_entitlement_insert(update=update)  
            elif self.quote_service_entitlement_type in ('STR-OFFBGBPMCMKTGCPCND OBJ-AS','STR-OFFBGBSMKTGCPCND OBJ-AS','STR-OFFBGBKTGCPCND OBJ-GPAS'):
                self._pmsa_quote_items_entitlement_insert(update=update)  
            else:
                self._quote_items_entitlement_insert(update=update)
        return True		
    
    def _simple_quote_items_insert(self):
        equipments_count = 0
        item_number_inc = 0
                                                                                                                
        validate_axcliary = Sql.GetFirst("SELECT COUNT(SERVICE_ID) AS AXCLIARY_PRODUCT_FLAG from SAQTSV (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID='{ServiceId}'".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id))
        if validate_axcliary.AXCLIARY_PRODUCT_FLAG:                            
            quote_item_obj = Sql.GetFirst("SELECT COUNT(LINE) as LINE FROM SAQRIT (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id))
            equipments_count = int(quote_item_obj.LINE)
                
        #quote_line_item_obj = Sql.GetFirst("SELECT TOP 1 LINE FROM SAQRIT (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' ORDER BY LINE DESC".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id))
        #quote_item_obj = Sql.GetFirst("SELECT COUNT(LINE) as LINE FROM SAQRIT (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id))
        #if quote_line_item_obj:
        #	if quote_line_item_obj.LINE:
        #		equipments_count = int(quote_line_item_obj.LINE) 
        doctype_obj = Sql.GetFirst("SELECT ITEM_NUMBER_INCREMENT FROM SAQTRV LEFT JOIN SADOTY ON SADOTY.DOCTYPE_ID=SAQTRV.DOCTYP_ID WHERE SAQTRV.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQTRV.QTEREV_RECORD_ID = '{RevisionRecordId}'".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id))
        if doctype_obj:
            item_number_inc = int(doctype_obj.ITEM_NUMBER_INCREMENT)
        ####809 HPQC DEFECT code starts..
        split_quote_condition = " AND SAQRIS.PAR_SERVICE_ID = '{}'".format(self.split_parent_service_id) if self.service_id == "Z0105" else ""
        ##809 HPQC DEFECT code ends..
        #INC08620970 - Start - M
        Sql.RunQuery("""INSERT SAQRIT (QUOTE_REVISION_CONTRACT_ITEM_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified, CONTRACT_VALID_FROM, CONTRACT_VALID_TO, DOC_CURRENCY, DOCURR_RECORD_ID, EXCHANGE_RATE, EXCHANGE_RATE_DATE, EXCHANGE_RATE_RECORD_ID, GL_ACCOUNT_NO, GLOBAL_CURRENCY, GLOBAL_CURRENCY_RECORD_ID, LINE, OBJECT_ID, OBJECT_TYPE, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, PAR_PRDOFR_ID, PROFIT_CENTER, QUANTITY, QUOTE_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, REF_SALESORDER, STATUS, TAXCLASSIFICATION_DESCRIPTION, TAXCLASSIFICATION_ID, TAXCLASSIFICATION_RECORD_ID,TAX_PERCENTAGE, GREENBOOK, GREENBOOK_RECORD_ID, FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID,NET_VALUE_INGL_CURR, NET_PRICE_INGL_CURR, QTEITMSUM_RECORD_ID) 
            SELECT
                CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REVISION_CONTRACT_ITEM_ID,
                '{UserName}' AS CPQTABLEENTRYADDEDBY,
                GETDATE() as CPQTABLEENTRYDATEADDED,
                {UserId} as CpqTableEntryModifiedBy,
                GETDATE() as CpqTableEntryDateModified,
                SAQTRV.CONTRACT_VALID_FROM,
                SAQTRV.CONTRACT_VALID_TO,
                SAQTRV.DOC_CURRENCY,
                SAQTRV.DOCCURR_RECORD_ID as DOCURR_RECORD_ID,
                ISNULL(CONVERT(FLOAT,SAQTRV.EXCHANGE_RATE),'') AS EXCHANGE_RATE,
                SAQTRV.EXCHANGE_RATE_DATE,
                SAQTRV.EXCHANGERATE_RECORD_ID as EXCHANGE_RATE_RECORD_ID,
                null as GL_ACCOUNT_NO,
                SAQTRV.GLOBAL_CURRENCY,
                SAQTRV.GLOBAL_CURRENCY_RECORD_ID,
                ROW_NUMBER()OVER(ORDER BY(OQ.GREENBOOK)) + {EquipmentsCount} as LINE,
                null as OBJECT_ID,
                'GREENBOOK' as OBJECT_TYPE,
                OQ.SERVICE_DESCRIPTION,
                OQ.SERVICE_ID,
                OQ.SERVICE_RECORD_ID,
                OQ.PAR_SERVICE_ID AS PAR_PRDOFR_ID,
                null as PROFIT_CENTER,
                1 as QUANTITY,
                SAQTRV.QUOTE_ID,
                SAQTRV.QUOTE_RECORD_ID,
                SAQTMT.QTEREV_ID,
                SAQTMT.QTEREV_RECORD_ID,
                null as REF_SALESORDER,
                'ACQUIRED' as STATUS,
                MAMSCT.TAXCLASSIFICATION_DESCRIPTION,
                MAMSCT.TAXCLASSIFICATION_ID,
                MAMSCT.TAXCLASSIFICATION_RECORD_ID,
                SAQRIS.TAX_PERCENTAGE,
                OQ.GREENBOOK,
                OQ.GREENBOOK_RECORD_ID,
                OQ.FABLOCATION_ID as FABLOCATION_ID,
                OQ.FABLOCATION_NAME as FABLOCATION_NAME,
                OQ.FABLOCATION_RECORD_ID as FABLOCATION_RECORD_ID,
                '0' AS NET_VALUE_INGL_CURR,
                '0' AS NET_PRICE_INGL_CURR,
                SAQRIS.QUOTE_REV_ITEM_SUMMARY_RECORD_ID as QTEITMSUM_RECORD_ID
            FROM (
                    SELECT 
                        QUOTE_RECORD_ID, QTEREV_RECORD_ID, SERVICE_ID, FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID, SERVICE_RECORD_ID, SERVICE_DESCRIPTION, PAR_SERVICE_ID
                    FROM SAQSCO (NOLOCK)
                    WHERE SAQSCO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQSCO.SERVICE_ID = '{ServiceId}' 
                    GROUP BY QUOTE_RECORD_ID, QTEREV_RECORD_ID, SERVICE_ID, FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID, SERVICE_RECORD_ID,SERVICE_DESCRIPTION, PAR_SERVICE_ID
                ) OQ 
            JOIN (
                SELECT DISTINCT SAQSGE.QUOTE_RECORD_ID,SAQSGE.QTEREV_RECORD_ID, SAQTSV.SERVICE_ID,SAQSGE.GREENBOOK,SAQSGE.SALESORG_RECORD_ID,SAQTSV.PAR_SERVICE_ID FROM SAQSGE (NOLOCK) INNER JOIN SAQTSV ON SAQSGE.QUOTE_RECORD_ID = SAQTSV.QUOTE_RECORD_ID  AND SAQSGE.QTEREV_RECORD_ID = SAQTSV.QTEREV_RECORD_ID AND SAQSGE.SERVICE_ID = SAQTSV.PAR_SERVICE_ID 
                WHERE SAQSGE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSGE.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND ISNULL(CONFIGURATION_STATUS, '') = 'COMPLETE' AND SAQTSV.SERVICE_ID ='{ServiceId}'
                
            ) AS IQ ON IQ.QUOTE_RECORD_ID = OQ.QUOTE_RECORD_ID AND IQ.QTEREV_RECORD_ID = OQ.QTEREV_RECORD_ID AND IQ.SERVICE_ID = OQ.SERVICE_ID	AND IQ.SERVICE_ID = '{ServiceId}' AND IQ.GREENBOOK = OQ.GREENBOOK AND IQ.PAR_SERVICE_ID = OQ.PAR_SERVICE_ID
            
            JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = OQ.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = OQ.QTEREV_RECORD_ID     
                                                                                                    
            JOIN SAQTRV (NOLOCK) ON SAQTRV.SALESORG_RECORD_ID = IQ.SALESORG_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = OQ.QTEREV_RECORD_ID AND SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID
                                                                                                            
            JOIN SAQRIS (NOLOCK) ON SAQRIS.QTEREV_RECORD_ID = SAQTRV.QUOTE_REVISION_RECORD_ID AND SAQRIS.QUOTE_RECORD_ID = SAQTRV.QUOTE_RECORD_ID AND SAQRIS.SERVICE_ID = OQ.SERVICE_ID	AND OQ.PAR_SERVICE_ID = SAQRIS.PAR_SERVICE_ID {split_quote_condition}		
            LEFT JOIN MAMSCT (NOLOCK) ON MAMSCT.DISTRIBUTIONCHANNEL_RECORD_ID = SAQTRV.DISTRIBUTIONCHANNEL_RECORD_ID AND MAMSCT.COUNTRY_RECORD_ID = SAQTRV.COUNTRY_RECORD_ID AND MAMSCT.SALESORG_ID = SAQTRV.SALESORG_ID AND MAMSCT.SAP_PART_NUMBER = OQ.SERVICE_ID  AND SAQTRV.ACCTAXCAT_RECORD_ID = MAMSCT.TAXCATEGORY_RECORD_ID
            LEFT JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = OQ.QUOTE_RECORD_ID AND SAQRIT.QTEREV_RECORD_ID = OQ.QTEREV_RECORD_ID AND SAQRIT.SERVICE_RECORD_ID = OQ.SERVICE_RECORD_ID AND ISNULL(SAQRIT.GREENBOOK_RECORD_ID,'') = ISNULL(OQ.GREENBOOK_RECORD_ID,'')
            WHERE OQ.QUOTE_RECORD_ID = '{QuoteRecordId}' AND OQ.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND OQ.SERVICE_ID = '{ServiceId}'  AND  ISNULL(SAQRIT.GREENBOOK_RECORD_ID,'') = '' """.format(UserId=self.user_id, UserName=self.user_name, QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id, EquipmentsCount=equipments_count, par_service_id = self.parent_service_id,split_quote_condition = split_quote_condition))
        #INC08620970 - End - M
        ##ordering line field in saqrit
        self._ordering_item_line_no()
    
    def _simple_fpm_quote_items_insert(self):
        equipments_count = 0
        Sql.RunQuery("DELETE FROM SAQRIT WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID LIKE '{ServiceId}%'".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id))
        
        quote_line_item_obj = Sql.GetFirst("SELECT TOP 1 LINE FROM SAQRIT (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' ORDER BY LINE DESC".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id))
        if quote_line_item_obj:
            equipments_count = int(quote_line_item_obj.LINE)
        
        Log.Info("SAQRIT=== 5")
        Sql.RunQuery("""INSERT SAQRIT (QUOTE_REVISION_CONTRACT_ITEM_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified, CONTRACT_VALID_FROM, CONTRACT_VALID_TO, DOC_CURRENCY, DOCURR_RECORD_ID, EXCHANGE_RATE, EXCHANGE_RATE_DATE, EXCHANGE_RATE_RECORD_ID, GL_ACCOUNT_NO, GLOBAL_CURRENCY, GLOBAL_CURRENCY_RECORD_ID, LINE, OBJECT_ID, OBJECT_TYPE, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, PROFIT_CENTER, QUANTITY, QUOTE_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, REF_SALESORDER, STATUS, TAXCLASSIFICATION_DESCRIPTION, TAXCLASSIFICATION_ID, TAXCLASSIFICATION_RECORD_ID,TAX_PERCENTAGE, GREENBOOK, GREENBOOK_RECORD_ID,NET_VALUE_INGL_CURR, NET_PRICE_INGL_CURR) 
        SELECT
            CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REVISION_CONTRACT_ITEM_ID,
            '{UserName}' AS CPQTABLEENTRYADDEDBY,
            GETDATE() as CPQTABLEENTRYDATEADDED,
            {UserId} as CpqTableEntryModifiedBy,
            GETDATE() as CpqTableEntryDateModified,
            SAQTRV.CONTRACT_VALID_FROM,
            SAQTRV.CONTRACT_VALID_TO,
            SAQTRV.DOC_CURRENCY,
            SAQTRV.DOCCURR_RECORD_ID as DOCURR_RECORD_ID,
            ISNULL(CONVERT(FLOAT,SAQTRV.EXCHANGE_RATE),'') AS EXCHANGE_RATE,
            SAQTRV.EXCHANGE_RATE_DATE,
            SAQTRV.EXCHANGERATE_RECORD_ID as EXCHANGE_RATE_RECORD_ID,
            null as GL_ACCOUNT_NO,
            SAQTRV.GLOBAL_CURRENCY,
            SAQTRV.GLOBAL_CURRENCY_RECORD_ID,
                
            ROW_NUMBER()OVER(ORDER BY(SAQSPT.CpqTableEntryId)) + {EquipmentsCount} as LINE,
            null as OBJECT_ID,
            null as OBJECT_TYPE,
            SAQSPT.SERVICE_DESCRIPTION,
            SAQSPT.SERVICE_ID,
            SAQSPT.SERVICE_RECORD_ID,
            null as PROFIT_CENTER,
            1 as QUANTITY,
            SAQTRV.QUOTE_ID,
            SAQTRV.QUOTE_RECORD_ID,
            SAQTMT.QTEREV_ID,
            SAQTMT.QTEREV_RECORD_ID,
            null as REF_SALESORDER,
            null as STATUS,
            MAMSCT.TAXCLASSIFICATION_DESCRIPTION,
            MAMSCT.TAXCLASSIFICATION_ID,
            MAMSCT.TAXCLASSIFICATION_RECORD_ID,
            SAQRIS.TAX_PERCENTAGE,
            null as GREENBOOK,
            null as GREENBOOK_RECORD_ID,
            '0' AS NET_VALUE_INGL_CURR,
            '0' AS NET_PRICE_INGL_CURR
        FROM SAQSPT (NOLOCK) 
        JOIN (
            SELECT SAQSPT.QUOTE_RECORD_ID, SAQSPT.SERVICE_ID, MAX(CpqTableEntryId) as CpqTableEntryId, CAST(ROW_NUMBER()OVER(ORDER BY SAQSPT.SERVICE_ID) + {EquipmentsCount} AS DECIMAL(5,1)) AS LINE_ITEM_ID FROM SAQSPT (NOLOCK) 
            WHERE SAQSPT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSPT.QTEREV_RECORD_ID ='{QuoteRevisionRecordId}'
            AND SAQSPT.CUSTOMER_ANNUAL_QUANTITY > 0
            GROUP BY SAQSPT.QUOTE_RECORD_ID, SAQSPT.SERVICE_ID
        ) AS IQ ON IQ.CpqTableEntryId = SAQSPT.CpqTableEntryId
        JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQSPT.QUOTE_RECORD_ID  AND SAQTMT.QTEREV_RECORD_ID = SAQSPT.QTEREV_RECORD_ID            
        JOIN MAMTRL (NOLOCK) ON MAMTRL.SAP_PART_NUMBER = SAQSPT.SERVICE_ID 
        JOIN SAQTRV (NOLOCK) ON SAQTRV.SALESORG_RECORD_ID = SAQSPT.SALESORG_RECORD_ID AND SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID
                                                                                                                                            
        JOIN SAQRIS (NOLOCK) ON SAQRIS.QTEREV_RECORD_ID = SAQSPT.QTEREV_RECORD_ID AND SAQRIS.QUOTE_RECORD_ID = SAQSPT.QUOTE_RECORD_ID AND SAQRIS.SERVICE_ID = SAQSPT.SERVICE_ID
        LEFT JOIN MAMSCT (NOLOCK) ON SAQTRV.DISTRIBUTIONCHANNEL_RECORD_ID = MAMSCT.DISTRIBUTIONCHANNEL_RECORD_ID AND SAQTRV.COUNTRY_RECORD_ID = MAMSCT.COUNTRY_RECORD_ID AND SAQTRV.SALESORG_ID = MAMSCT.SALESORG_ID AND MAMSCT.SAP_PART_NUMBER = MAMTRL.SAP_PART_NUMBER AND MAMSCT.SALESORG_ID = SAQSPT.SALESORG_ID  AND SAQTRV.ACCTAXCAT_RECORD_ID = MAMSCT.TAXCATEGORY_RECORD_ID WHERE SAQSPT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSPT.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQSPT.SERVICE_ID = '{ServiceId}' """.format(UserId=self.user_id, UserName=self.user_name, QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id, EquipmentsCount=equipments_count))
        ##ordering line field in saqrit
        self._ordering_item_line_no()
    def _simple_items_object_insert(self):
        ancillary_where = ""
        ancillary_join = ""
        # if self.is_ancillary == True or self.addon_product == True:
        # 	ancillary_join = """ JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = SAQTRV.QUOTE_RECORD_ID
        # 									AND SAQRIT.SERVICE_RECORD_ID = SAQSCO.SERVICE_RECORD_ID
        # 									AND SAQRIT.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID
        # 									AND SAQRIT.GREENBOOK_RECORD_ID = SAQSCO.GREENBOOK_RECORD_ID
        # 									AND PAR_SAQRIT.SERVICE_ID = '{parent_service_id}'
        # 									AND PAR_SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID = SAQRIT.PARQTEITM_LINE_RECORD_ID""".format(parent_service_id = self.parent_service_id)
        # 	ancillary_where= " AND PAR_SAQRIT.SERVICE_ID = '{parent_service_id}'".format(parent_service_id = self.parent_service_id)
        #INC08704936 M
        Sql.RunQuery("""INSERT SAQRIO (CUSTOMER_TOOL_ID, EQUIPMENT_DESCRIPTION, EQUIPMENT_ID, EQUIPMENT_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID, KPU, LINE, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, QTEITM_RECORD_ID, QUOTE_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, SERIAL_NUMBER, TECHNOLOGY, TOOL_CONFIGURATION, WAFER_SIZE,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID, QUOTE_REVISION_ITEM_OBJECT_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified)
                SELECT OQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REVISION_ITEM_OBJECT_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED,{UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
                SELECT DISTINCT
                    SAQSCO.CUSTOMER_TOOL_ID,
                    SAQSCO.EQUIPMENT_DESCRIPTION,					
                    SAQSCO.EQUIPMENT_ID,
                    SAQSCO.EQUIPMENT_RECORD_ID,                        
                    SAQSCO.GREENBOOK, 
                    SAQSCO.GREENBOOK_RECORD_ID,
                    SAQSCO.KPU,
                    SAQRIT.LINE as LINE,
                    SAQSCO.SERVICE_DESCRIPTION, 
                    SAQSCO.SERVICE_ID, 
                    SAQSCO.SERVICE_RECORD_ID, 
                    SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID, 
                    SAQSCO.QUOTE_ID,
                    SAQSCO.QUOTE_RECORD_ID,
                    SAQSCO.QTEREV_ID,
                    SAQSCO.QTEREV_RECORD_ID,
                    SAQSCO.SERIAL_NO as SERIAL_NUMBER, 
                    SAQSCO.TECHNOLOGY, 
                    --PRPRBM.TOOL_CONFIGURATION,
                    null as TOOL_CONFIGURATION,
                    SAQSCO.WAFER_SIZE,
                    SAQSCO.FABLOCATION_ID,
                    SAQSCO.FABLOCATION_NAME,
                    SAQSCO.FABLOCATION_RECORD_ID					
                FROM 
                    SAQSCO (NOLOCK)					 
                    JOIN (
                        SELECT SAQSCE.QUOTE_RECORD_ID,SAQSCE.QTEREV_RECORD_ID, SAQTSV.SERVICE_ID,SAQSCE.EQUIPMENT_ID FROM SAQSCE (NOLOCK) INNER JOIN SAQTSV ON SAQSCE.QUOTE_RECORD_ID = SAQTSV.QUOTE_RECORD_ID  AND SAQSCE.QTEREV_RECORD_ID = SAQTSV.QTEREV_RECORD_ID AND SAQSCE.SERVICE_ID = SAQTSV.PAR_SERVICE_ID 
                        WHERE SAQSCE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCE.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND ISNULL(CONFIGURATION_STATUS, '') = 'COMPLETE' AND SAQTSV.SERVICE_ID ='{ServiceId}'
                        
                    ) AS IQ ON IQ.QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID AND IQ.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID AND IQ.SERVICE_ID = SAQSCO.SERVICE_ID	AND IQ.EQUIPMENT_ID	 = SAQSCO.EQUIPMENT_ID	AND IQ.SERVICE_ID = '{ServiceId}'
                    JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID         
                    JOIN SAQTRV (NOLOCK) ON SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID 
                    JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = SAQTRV.QUOTE_RECORD_ID
                                            AND SAQRIT.SERVICE_RECORD_ID = SAQSCO.SERVICE_RECORD_ID
                                            AND SAQRIT.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID
                                            AND SAQRIT.GREENBOOK_RECORD_ID = SAQSCO.GREENBOOK_RECORD_ID
                    {ancillary_join}
                    --LEFT JOIN PRPRBM (NOLOCK) ON PRPRBM.ACCOUNT_RECORD_ID = SAQTMT.ACCOUNT_RECORD_ID AND PRPRBM.EQUIPMENT_RECORD_ID = SAQSCO.EQUIPMENT_RECORD_ID AND PRPRBM.SERVICE_RECORD_ID = SAQSCO.SERVICE_RECORD_ID		
                    LEFT JOIN SAQRIO (NOLOCK) ON SAQRIO.QUOTE_RECORD_ID = SAQSCO.QUOTE_RECORD_ID AND SAQRIO.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID AND SAQRIO.SERVICE_RECORD_ID = SAQSCO.SERVICE_RECORD_ID AND SAQRIO.GREENBOOK_RECORD_ID = SAQSCO.GREENBOOK_RECORD_ID AND SAQRIO.EQUIPMENT_RECORD_ID = SAQSCO.EQUIPMENT_RECORD_ID			
                WHERE 
                    SAQSCO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQSCO.SERVICE_ID = '{ServiceId}'  AND ISNULL(SAQRIO.EQUIPMENT_RECORD_ID,'') = ''  {ancillary_where}
                ) OQ
                """.format(UserId=self.user_id, UserName=self.user_name, QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id,ancillary_where = ancillary_where, ancillary_join = ancillary_join
                )
            )
        #INC08704936 M
        ##update quantity in SAQRIT
        self._quote_item_qty_update()
    def _simple_quote_annualized_items_insert(self):
        ancillary_join =""
        ancillary_where =""
        # if self.is_ancillary == True or self.addon_product == True:
        # 	ancillary_join = """JOIN SAQRIT (NOLOCK) PAR_SAQRIT ON PAR_SAQRIT.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID 
        # 												AND PAR_SAQRIT.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID 
        # 												AND PAR_SAQRIT.SERVICE_ID =SAQRIT.PAR_SERVICE_ID 
        # 												AND PAR_SAQRIT.SERVICE_ID = '{par_service_id}' 
        # 												AND ISNULL(PAR_SAQRIT.GREENBOOK_RECORD_ID,'') = ISNULL(SAQRIT.GREENBOOK_RECORD_ID,'') 
        # 												AND PAR_SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID = SAQRIT.PARQTEITM_LINE_RECORD_ID """.format(par_service_id = self.parent_service_id)	
        # 	if self.quote_service_entitlement_type in ('OFFERING + EQUIPMENT','OFFERING+EQUIPMENT','OFRNG+EQUIP','STR-OFFBGREQPODV OBJ-EQ'):
        # 		ancillary_join += " AND PAR_SAQRIT.FABLOCATION_RECORD_ID = SAQRIT.FABLOCATION_RECORD_ID AND ISNULL(PAR_SAQRIT.EQUIPMENT_ID,'') = SAQRIT.EQUIPMENT_ID"
        # 	ancillary_where =  " AND PAR_SAQRIT.SERVICE_ID = '{parent_service_id}'".format(parent_service_id = self.parent_service_id)
        # CR704 - Start - M		 
        contract_years_obj = Sql.GetList("SELECT CONTRACT_END_DATE, CONTRACT_START_DATE, CNTYER FROM SAQCYR (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}'".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id))
        for contract_year_obj in contract_years_obj:
            if contract_year_obj.CNTYER == 'YEAR 1':
                yearwise_join_str = "JOIN SAQCYR (NOLOCK) ON SAQCYR.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND SAQCYR.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID AND SAQCYR.CONTRACT_START_DATE <= SAQRIT.CONTRACT_VALID_FROM AND SAQCYR.CONTRACT_END_DATE >= SAQRIT.CONTRACT_VALID_FROM"
            else:
                yearwise_join_str = "JOIN SAQCYR (NOLOCK) ON SAQCYR.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND SAQCYR.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID AND ((SAQCYR.CONTRACT_START_DATE >= SAQRIT.CONTRACT_VALID_FROM AND SAQCYR.CONTRACT_START_DATE <= SAQRIT.CONTRACT_VALID_TO) OR (SAQCYR.CONTRACT_START_DATE <= SAQRIT.CONTRACT_VALID_FROM AND SAQCYR.CONTRACT_END_DATE >= SAQRIT.CONTRACT_VALID_FROM))"
            #INC08675532 #INC08675479 - START - M
            Sql.RunQuery("""INSERT SAQICO (EQUIPMENT_DESCRIPTION, STATUS, QUANTITY, OBJECT_ID, EQUPID, EQUIPMENT_ID, EQUIPMENT_RECORD_ID, LINE, QUOTE_ID, QTEITM_RECORD_ID, QUOTE_RECORD_ID, QTEREV_ID,QTEREV_RECORD_ID, KPU, SERNUM, SERIAL_NO, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, TECHNOLOGY,CUSTOMER_TOOL_ID, EQUCAT, EQUIPMENTCATEGORY_ID, EQUIPMENTCATEGORY_RECORD_ID, EQUIPMENT_STATUS, MNT_PLANT_ID, MNT_PLANT_NAME, MNT_PLANT_RECORD_ID, SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID,  FABLOC, FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, GRNBOK, GREENBOOK, GREENBOOK_RECORD_ID, GLOBAL_CURRENCY, GLOBAL_CURRENCY_RECORD_ID, OBJECT_TYPE, BLUBOK, WTYSTE, WTYEND, WTYDAY, PLTFRM, SUBSIZ, REGION, ISPOES, CSTSRC, PRCSRC, SPQTEV, TAXVTP,TAXGRP,DCCRFX,DCCRXD,DOCCUR, CNTYER, STADTE, CONTRACT_VALID_FROM, ENDDTE, CONTRACT_VALID_TO, CNTDAY, QUOTE_ITEM_COVERED_OBJECT_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified)
                            SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_COVERED_OBJECT_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED,{UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (                            
                                SELECT DISTINCT					
                                    null as EQUIPMENT_DESCRIPTION,
                                    'ACQUIRED' as STATUS,
                                    null as EQUIPMENT_QUANTITY,
                                    SAQRIT.OBJECT_ID,
                                    null as EQUPID,
                                    null as EQUIPMENT_ID,
                                    null as EQUIPMENT_RECORD_ID,
                                    SAQRIT.LINE,
                                    SAQRIT.QUOTE_ID, 
                                    SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID, 
                                    SAQRIT.QUOTE_RECORD_ID,
                                    SAQRIT.QTEREV_ID,
                                    SAQRIT.QTEREV_RECORD_ID,
                                    null as KPU,
                                    null as SERNUM, 
                                    null as SERIAL_NO, 
                                    SAQRIT.SERVICE_DESCRIPTION, 
                                    SAQRIT.SERVICE_ID, 
                                    SAQRIT.SERVICE_RECORD_ID,								
                                    null as TECHNOLOGY,																			
                                    null as CUSTOMER_TOOL_ID, 
                                    null as EQUCAT, 
                                    null as EQUIPMENTCATEGORY_ID, 
                                    null as EQUIPMENTCATEGORY_RECORD_ID, 
                                    null as EQUIPMENT_STATUS,					
                                    null as MNT_PLANT_ID, 
                                    null as MNT_PLANT_NAME, 
                                    null as MNT_PLANT_RECORD_ID,			
                                    SAQTRV.SALESORG_ID, 
                                    SAQTRV.SALESORG_NAME, 
                                    SAQTRV.SALESORG_RECORD_ID, 
                                    SAQRIT.FABLOCATION_ID as FABLOC,
                                    SAQRIT.FABLOCATION_ID,
                                    SAQRIT.FABLOCATION_NAME,
                                    SAQRIT.FABLOCATION_RECORD_ID,
                                    SAQRIT.GREENBOOK as GRNBOK, 
                                    SAQRIT.GREENBOOK, 
                                    SAQRIT.GREENBOOK_RECORD_ID, 			
                                    SAQTRV.GLOBAL_CURRENCY,
                                    SAQTRV.GLOBAL_CURRENCY_RECORD_ID,					
                                    SAQRIT.OBJECT_TYPE,
                                    SAQTRV.BLUEBOOK as BLUBOK,
                                    null as WTYSTE,
                                    null as WTYEND,
                                    null as WTYDAY,
                                    null as PLTFRM,
                                    null as SUBSIZ,
                                    SAQTRV.REGION as REGION,
                                    SAQTMT.POES as ISPOES,
                                    CASE WHEN ISNULL(PRSPRV.SSCM_COST, 0) = 1 THEN 'SSCM' ELSE 'CPQ' END as CSTSRC,
                                    CASE WHEN ISNULL(PRSPRV.SSCM_COST, 0) = 1 THEN 'VALUE PRICING-SSCM' ELSE 'OFFLINE PRICING' END as PRCSRC,'No' as SPQTEV,
                                    SAQRIT.TAX_PERCENTAGE as TAXVTP,
                                    SAQRIT.TAXCLASSIFICATION_ID,
                                    SAQTRV.EXCHANGE_RATE,
                                    SAQTRV.EXCHANGE_RATE_DATE,
                                    SAQTRV.DOC_CURRENCY,
                                    SAQCYR.CNTYER as CNTYER,
                                    CASE WHEN SAQRIT.CONTRACT_VALID_FROM > SAQCYR.CONTRACT_START_DATE THEN SAQRIT.CONTRACT_VALID_FROM ELSE SAQCYR.CONTRACT_START_DATE END as STADTE,
                                    CASE WHEN SAQRIT.CONTRACT_VALID_FROM > SAQCYR.CONTRACT_START_DATE THEN SAQRIT.CONTRACT_VALID_FROM ELSE SAQCYR.CONTRACT_START_DATE END as CONTRACT_VALID_FROM,
                                    CASE WHEN SAQCYR.CONTRACT_END_DATE > SAQRIT.CONTRACT_VALID_TO THEN SAQRIT.CONTRACT_VALID_TO ELSE SAQCYR.CONTRACT_END_DATE END as ENDDTE,
                                    CASE WHEN SAQCYR.CONTRACT_END_DATE > SAQRIT.CONTRACT_VALID_TO THEN SAQRIT.CONTRACT_VALID_TO ELSE SAQCYR.CONTRACT_END_DATE END as CONTRACT_VALID_TO,
                                    Abs(DATEDIFF(day,CASE WHEN SAQCYR.CONTRACT_END_DATE > SAQRIT.CONTRACT_VALID_TO THEN SAQRIT.CONTRACT_VALID_TO ELSE SAQCYR.CONTRACT_END_DATE END , CASE WHEN SAQRIT.CONTRACT_VALID_FROM > SAQCYR.CONTRACT_START_DATE THEN SAQRIT.CONTRACT_VALID_FROM ELSE SAQCYR.CONTRACT_START_DATE END)) + 1 as CNTDAY          
                                FROM 
                                    SAQRIT 
                                    JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID         
                                    JOIN SAQTRV (NOLOCK) ON SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID 
                                    LEFT JOIN PRSPRV (NOLOCK) ON PRSPRV.SERVICE_RECORD_ID = SAQRIT.SERVICE_RECORD_ID	
                                    {ancillary_join}	
                                    {YearWiseJoinString}				
                                WHERE 
                                    SAQRIT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQRIT.SERVICE_ID = '{ServiceId}' {ancillary_where}
                            ) IQ
                            LEFT JOIN SAQICO (NOLOCK) ON SAQICO.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND SAQICO.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND SAQICO.SERVICE_RECORD_ID = IQ.SERVICE_RECORD_ID AND ISNULL(SAQICO.FABLOCATION_RECORD_ID,'') = ISNULL(IQ.FABLOCATION_RECORD_ID,'') AND SAQICO.GREENBOOK_RECORD_ID = IQ.GREENBOOK_RECORD_ID AND SAQICO.CNTYER = IQ.CNTYER
                            WHERE ISNULL(SAQICO.FABLOCATION_RECORD_ID,'') = '' AND ISNULL(SAQICO.GREENBOOK_RECORD_ID,'') = ''
                            """.format(UserId=self.user_id, UserName=self.user_name, QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id, ancillary_join = ancillary_join, ancillary_where =ancillary_where, YearWiseJoinString = yearwise_join_str)
                    )
                    #INC08675532 #INC08675479 - END - M
        # CR704 - End - M
        #A055S000P01-20577
        Sql.RunQuery("UPDATE A SET A.OFRING = UPPER(CONCAT(B.SERVICE_ID,' - ',B.SERVICE_DESCRIPTION)) FROM SAQICO A JOIN SAQTSV B ON B.SERVICE_RECORD_ID = A.SERVICE_RECORD_ID WHERE A.QUOTE_RECORD_ID = '{QuoteRecordId}' AND A.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND ISNULL(A.OFRING,'') = '' ".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id))
        #A055S000P01-21072 Start M
        self.update_cntday()
        #A055S000P01-21072 End M
        #Sql.RunQuery("""UPDATE SAQTRV SET REVISION_STATUS = 'CFG-ACQUIRING' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}'""".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id))
    def _simple_fpm_quote_annualized_items_insert(self):
        Trace.Write('FPM_ANNUALIZED_ITEM_INSERT')
        Log.Info("""INSERT SAQICO (EQUIPMENT_DESCRIPTION,STATUS,QUANTITY,OBJECT_ID,EQUIPMENT_ID, EQUIPMENT_RECORD_ID, CONTRACT_VALID_FROM, CONTRACT_VALID_TO,LINE, QUOTE_ID, QTEITM_RECORD_ID,  QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,KPU, SERIAL_NO, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, TECHNOLOGY,CUSTOMER_TOOL_ID, EQUIPMENTCATEGORY_ID, EQUIPMENTCATEGORY_RECORD_ID, EQUIPMENT_STATUS, MNT_PLANT_ID, MNT_PLANT_NAME, MNT_PLANT_RECORD_ID, SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID, FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID, GLOBAL_CURRENCY,GLOBAL_CURRENCY_RECORD_ID,OBJECT_TYPE, QUOTE_ITEM_COVERED_OBJECT_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified)
            SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_COVERED_OBJECT_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED,{UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
            SELECT DISTINCT					
                null as EQUIPMENT_DESCRIPTION,
                'ACQUIRED' AS STATUS,
                null as QUANTITY,
                SAQRIT.OBJECT_ID,
                null as EQUIPMENT_ID,
                null as EQUIPMENT_RECORD_ID,                        
                SAQRIT.CONTRACT_VALID_FROM,
                SAQRIT.CONTRACT_VALID_TO,
                SAQRIT.LINE,
                SAQRIT.QUOTE_ID, 
                SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID, 
                SAQRIT.QUOTE_RECORD_ID,
                SAQRIT.QTEREV_ID,
                SAQRIT.QTEREV_RECORD_ID,
                null as KPU,
                null as SERIAL_NO, 
                SAQRIT.SERVICE_DESCRIPTION, 
                SAQRIT.SERVICE_ID, 
                SAQRIT.SERVICE_RECORD_ID,								
                null as TECHNOLOGY,																			
                null as CUSTOMER_TOOL_ID, 
                null as EQUIPMENTCATEGORY_ID, 
                null as EQUIPMENTCATEGORY_RECORD_ID, 
                null as EQUIPMENT_STATUS,					
                null as MNT_PLANT_ID, 
                null as MNT_PLANT_NAME, 
                null as MNT_PLANT_RECORD_ID,			
                SAQTRV.SALESORG_ID, 
                SAQTRV.SALESORG_NAME, 
                SAQTRV.SALESORG_RECORD_ID, 
                SAQRIT.FABLOCATION_ID,
                SAQRIT.FABLOCATION_NAME,
                SAQRIT.FABLOCATION_RECORD_ID,
                SAQRIT.GREENBOOK, 
                SAQRIT.GREENBOOK_RECORD_ID, 			
                SAQTRV.GLOBAL_CURRENCY,
                SAQTRV.GLOBAL_CURRENCY_RECORD_ID,
                SAQRIT.OBJECT_TYPE				
                                        
            FROM 
                SAQRIT (NOLOCK)					 
                JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID         
                JOIN SAQTRV (NOLOCK) ON SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID 
                LEFT JOIN PRCFVA (NOLOCK) ON PRCFVA.FACTOR_VARIABLE_ID = SAQRIT.SERVICE_ID AND PRCFVA.FACTOR_ID = 'AIYUPD'
                LEFT JOIN (
                    SELECT DATEADD(year,1,CONTRACT_VALID_FROM) as date_year,'YEAR 1' AS year,QUOTE_RECORD_ID,SERVICE_ID,QTEREV_RECORD_ID,FABLOCATION_ID,GREENBOOK FROM SAQRIT WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}' 
                    UNION ALL  
                    SELECT DATEADD(year,2,CONTRACT_VALID_FROM) as date_year,'YEAR 2' AS year,QUOTE_RECORD_ID,SERVICE_ID,QTEREV_RECORD_ID,FABLOCATION_ID,GREENBOOK FROM SAQRIT WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}' AND  1 = (CASE WHEN DATEDIFF(MONTH, SAQRIT.CONTRACT_VALID_FROM, SAQRIT.CONTRACT_VALID_TO) > 12 then 1 else 0 end )
                    UNION ALL  
                    SELECT DATEADD(year,3,CONTRACT_VALID_FROM) as date_year,'YEAR 3' AS year,QUOTE_RECORD_ID,SERVICE_ID,QTEREV_RECORD_ID,FABLOCATION_ID,GREENBOOK FROM SAQRIT WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}' AND  1 = (CASE WHEN DATEDIFF(MONTH, SAQRIT.CONTRACT_VALID_FROM, SAQRIT.CONTRACT_VALID_TO) > 24 then 1 else 0 end )
                    UNION ALL  
                    SELECT DATEADD(year,4,CONTRACT_VALID_FROM) as date_year,'YEAR 4' AS year,QUOTE_RECORD_ID,SERVICE_ID,QTEREV_RECORD_ID,FABLOCATION_ID,GREENBOOK FROM SAQRIT WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}' AND  1 = (CASE WHEN DATEDIFF(MONTH, SAQRIT.CONTRACT_VALID_FROM, SAQRIT.CONTRACT_VALID_TO) > 36  then 1 else 0 end )
                    UNION ALL  
                    SELECT DATEADD(year,5,CONTRACT_VALID_FROM) as date_year,'YEAR 5' AS year,QUOTE_RECORD_ID,SERVICE_ID,QTEREV_RECORD_ID,FABLOCATION_ID,GREENBOOK FROM SAQRIT WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}' AND  1 = (CASE WHEN DATEDIFF(MONTH, SAQRIT.CONTRACT_VALID_FROM, SAQRIT.CONTRACT_VALID_TO) > 48  then 1 else 0 end )
                ) CONTRACT_TEMP ON  CONTRACT_TEMP.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND CONTRACT_TEMP.SERVICE_ID = SAQRIT.SERVICE_ID AND CONTRACT_TEMP.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID AND CONTRACT_TEMP.FABLOCATION_ID = SAQRIT.FABLOCATION_ID AND CONTRACT_TEMP.GREENBOOK = SAQRIT.GREENBOOK					
            WHERE 
                SAQRIT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQRIT.SERVICE_ID = '{ServiceId}'
            ) IQ
            
            LEFT JOIN SAQICO (NOLOCK) ON SAQICO.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND SAQICO.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND SAQICO.SERVICE_RECORD_ID = IQ.SERVICE_RECORD_ID AND ISNULL(SAQICO.FABLOCATION_RECORD_ID,'') = ISNULL(IQ.FABLOCATION_RECORD_ID,'') AND SAQICO.GREENBOOK_RECORD_ID = IQ.GREENBOOK_RECORD_ID 
            WHERE ISNULL(SAQICO.FABLOCATION_RECORD_ID,'') = '' AND ISNULL(SAQICO.GREENBOOK_RECORD_ID,'') = '' AND NOT EXISTS (SELECT SERVICE_ID FROM SAQICO WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}')
            """.format(UserId=self.user_id, UserName=self.user_name, QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id)
        )
        Sql.RunQuery("""INSERT SAQICO (EQUIPMENT_DESCRIPTION,STATUS,QUANTITY,OBJECT_ID,EQUIPMENT_ID, EQUIPMENT_RECORD_ID, CONTRACT_VALID_FROM, CONTRACT_VALID_TO,LINE, QUOTE_ID, QTEITM_RECORD_ID,  QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,KPU, SERIAL_NO, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, TECHNOLOGY,CUSTOMER_TOOL_ID, EQUIPMENTCATEGORY_ID, EQUIPMENTCATEGORY_RECORD_ID, EQUIPMENT_STATUS, MNT_PLANT_ID, MNT_PLANT_NAME, MNT_PLANT_RECORD_ID, SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID, FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID, GLOBAL_CURRENCY,GLOBAL_CURRENCY_RECORD_ID,OBJECT_TYPE, QUOTE_ITEM_COVERED_OBJECT_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified)
            SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_COVERED_OBJECT_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED,{UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
            SELECT DISTINCT					
                                    
                null as EQUIPMENT_DESCRIPTION,
                'ACQUIRED' AS STATUS,
                null as QUANTITY,
                SAQRIT.OBJECT_ID,
                null as EQUIPMENT_ID,
                null as EQUIPMENT_RECORD_ID,                        
                SAQRIT.CONTRACT_VALID_FROM,
                SAQRIT.CONTRACT_VALID_TO,
                SAQRIT.LINE,
                SAQRIT.QUOTE_ID, 
                SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID, 
                SAQRIT.QUOTE_RECORD_ID,
                SAQRIT.QTEREV_ID,
                SAQRIT.QTEREV_RECORD_ID,
                null as KPU,
                null as SERIAL_NO, 
                SAQRIT.SERVICE_DESCRIPTION, 
                SAQRIT.SERVICE_ID, 
                SAQRIT.SERVICE_RECORD_ID,								
                null as TECHNOLOGY,																			
                null as CUSTOMER_TOOL_ID, 
                null as EQUIPMENTCATEGORY_ID, 
                null as EQUIPMENTCATEGORY_RECORD_ID, 
                null as EQUIPMENT_STATUS,					
                null as MNT_PLANT_ID, 
                null as MNT_PLANT_NAME, 
                null as MNT_PLANT_RECORD_ID,			
                SAQTRV.SALESORG_ID, 
                SAQTRV.SALESORG_NAME, 
                SAQTRV.SALESORG_RECORD_ID, 
                SAQRIT.FABLOCATION_ID,
                SAQRIT.FABLOCATION_NAME,
                SAQRIT.FABLOCATION_RECORD_ID,
                SAQRIT.GREENBOOK, 
                SAQRIT.GREENBOOK_RECORD_ID, 			
                SAQTRV.GLOBAL_CURRENCY,
                SAQTRV.GLOBAL_CURRENCY_RECORD_ID,
                SAQRIT.OBJECT_TYPE				
            FROM 
                SAQRIT (NOLOCK)					 
                JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID         
                JOIN SAQTRV (NOLOCK) ON SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = SAQTMT.QTEREV_RECORD_ID 
                LEFT JOIN PRCFVA (NOLOCK) ON PRCFVA.FACTOR_VARIABLE_ID = SAQRIT.SERVICE_ID AND PRCFVA.FACTOR_ID = 'AIYUPD'
                LEFT JOIN (
                    SELECT DATEADD(year,1,CONTRACT_VALID_FROM) as date_year,'YEAR 1' AS year,QUOTE_RECORD_ID,SERVICE_ID,QTEREV_RECORD_ID,FABLOCATION_ID,GREENBOOK FROM SAQRIT WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}' 
                    UNION ALL  
                    SELECT DATEADD(year,2,CONTRACT_VALID_FROM) as date_year,'YEAR 2' AS year,QUOTE_RECORD_ID,SERVICE_ID,QTEREV_RECORD_ID,FABLOCATION_ID,GREENBOOK FROM SAQRIT WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}' AND  1 = (CASE WHEN DATEDIFF(MONTH, SAQRIT.CONTRACT_VALID_FROM, SAQRIT.CONTRACT_VALID_TO) > 12 then 1 else 0 end )
                    UNION ALL  
                    SELECT DATEADD(year,3,CONTRACT_VALID_FROM) as date_year,'YEAR 3' AS year,QUOTE_RECORD_ID,SERVICE_ID,QTEREV_RECORD_ID,FABLOCATION_ID,GREENBOOK FROM SAQRIT WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}' AND  1 = (CASE WHEN DATEDIFF(MONTH, SAQRIT.CONTRACT_VALID_FROM, SAQRIT.CONTRACT_VALID_TO) > 24 then 1 else 0 end )
                    UNION ALL  
                    SELECT DATEADD(year,4,CONTRACT_VALID_FROM) as date_year,'YEAR 4' AS year,QUOTE_RECORD_ID,SERVICE_ID,QTEREV_RECORD_ID,FABLOCATION_ID,GREENBOOK FROM SAQRIT WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}' AND  1 = (CASE WHEN DATEDIFF(MONTH, SAQRIT.CONTRACT_VALID_FROM, SAQRIT.CONTRACT_VALID_TO) > 36  then 1 else 0 end )
                    UNION ALL  
                    SELECT DATEADD(year,5,CONTRACT_VALID_FROM) as date_year,'YEAR 5' AS year,QUOTE_RECORD_ID,SERVICE_ID,QTEREV_RECORD_ID,FABLOCATION_ID,GREENBOOK FROM SAQRIT WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}' AND  1 = (CASE WHEN DATEDIFF(MONTH, SAQRIT.CONTRACT_VALID_FROM, SAQRIT.CONTRACT_VALID_TO) > 48  then 1 else 0 end )
                ) CONTRACT_TEMP ON  CONTRACT_TEMP.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND CONTRACT_TEMP.SERVICE_ID = SAQRIT.SERVICE_ID AND CONTRACT_TEMP.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID AND CONTRACT_TEMP.FABLOCATION_ID = SAQRIT.FABLOCATION_ID AND CONTRACT_TEMP.GREENBOOK = SAQRIT.GREENBOOK					
            WHERE 
                SAQRIT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQRIT.SERVICE_ID = '{ServiceId}'
            ) IQ
            
            LEFT JOIN SAQICO (NOLOCK) ON SAQICO.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND SAQICO.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND SAQICO.SERVICE_RECORD_ID = IQ.SERVICE_RECORD_ID AND ISNULL(SAQICO.FABLOCATION_RECORD_ID,'') = ISNULL(IQ.FABLOCATION_RECORD_ID,'') AND SAQICO.GREENBOOK_RECORD_ID = IQ.GREENBOOK_RECORD_ID 
            WHERE ISNULL(SAQICO.FABLOCATION_RECORD_ID,'') = '' AND ISNULL(SAQICO.GREENBOOK_RECORD_ID,'') = '' AND NOT EXISTS (SELECT SERVICE_ID FROM SAQICO WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}')
            """.format(UserId=self.user_id, UserName=self.user_name, QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id)
        )
        #A055S000P01-20577
        Sql.RunQuery("UPDATE A SET A.OFRING = UPPER(CONCAT(B.SERVICE_ID,' - ',B.SERVICE_DESCRIPTION)) FROM SAQICO A JOIN SAQTSV B ON B.SERVICE_RECORD_ID = A.SERVICE_RECORD_ID WHERE A.QUOTE_RECORD_ID = '{QuoteRecordId}' AND A.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND ISNULL(A.OFRING,'') = '' ".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id))
        #A055S000P01-21072 Start M
        self.update_cntday()
        #A055S000P01-21072 End M
        #Sql.RunQuery("""UPDATE SAQTRV SET REVISION_STATUS = 'CFG-ACQUIRING' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}'""".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id))
        ##Calling the iflow for quote header writeback to cpq to c4c code starts..
        # CQCPQC4CWB.writeback_to_c4c("quote_header",Quote.GetGlobal("contract_quote_record_id"),Quote.GetGlobal("quote_revision_record_id"))
        # CQCPQC4CWB.writeback_to_c4c("opportunity_header",Quote.GetGlobal("contract_quote_record_id"),Quote.GetGlobal("quote_revision_record_id"))
        ##Calling the iflow for quote header writeback to cpq to c4c code ends...
    def _insert_quote_item_forecast_parts(self):		
        #CR713 - A055S000P01-20911 - Start - M
        if self.quote_service_entitlement_type == 'STR-OFFBGBKTGCPCND OBJ-GPAS':
            Sql.RunQuery("""INSERT SAQRIP (QUOTE_REVISION_ITEM_PRODUCT_LIST_RECORD_ID,CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified, PART_DESCRIPTION, PART_NUMBER, PART_RECORD_ID, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, QUANTITY, QUOTE_ID, QTEITM_RECORD_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, LINE, NEW_PART,GREENBOOK,GREENBOOK_RECORD_ID,FABLOCATION_ID, FABLOCATION_NAME,FABLOCATION_RECORD_ID  ) 
            SELECT 
                CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REVISION_ITEM_PRODUCT_LIST_RECORD_ID,
                '{UserName}' AS CPQTABLEENTRYADDEDBY,
                GETDATE() as CPQTABLEENTRYDATEADDED,
                {UserId} as CpqTableEntryModifiedBy,
                GETDATE() as CpqTableEntryDateModified,IQ.* FROM 
                (SELECT DISTINCT
                SAQGPA.KIT_NAME AS PART_DESCRIPTION,
                SAQGPA.KIT_NUMBER AS PART_NUMBER,
                SAQGPA.KITNUMBER_RECORD_ID AS PART_RECORD_ID,
                SAQRIT.SERVICE_DESCRIPTION,
                SAQRIT.SERVICE_ID,
                SAQRIT.SERVICE_RECORD_ID,
                NULL as QUANTITY,
                SAQRIT.QUOTE_ID,
                SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID,
                SAQRIT.QUOTE_RECORD_ID,
                SAQRIT.QTEREV_ID,
                SAQRIT.QTEREV_RECORD_ID,
                SAQRIT.LINE,
                NULL AS NEW_PART,
                SAQRIT.GREENBOOK,
                SAQRIT.GREENBOOK_RECORD_ID,
                SAQRIT.FABLOCATION_ID,
                SAQRIT.FABLOCATION_NAME, 
                SAQRIT.FABLOCATION_RECORD_ID    
                FROM (SELECT SAQGPA.SERVICE_ID, SAQGPA.GREENBOOK, SAQGPA.FABLOCATION_ID, SAQGPA.GOT_CODE, SAQGPA.KIT_ID,SAQGPA.		QUOTE_RECORD_ID, SAQGPA.QTEREV_RECORD_ID, ISNULL(PROCESS_TYPE,'') AS PROCESS_TYPE , ISNULL(DEVICE_NODE,'') AS DEVICE_NODE,KIT_NUMBER,KITNUMBER_RECORD_ID,KIT_NAME
                    FROM SAQGPA (NOLOCK)  
                    WHERE SAQGPA.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQGPA.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQGPA.SERVICE_ID = '{ServiceId}' AND SAQGPA.INCLUDED = 1 AND ISNULL(SAQGPA.KIT_ID,'') != ''
                    GROUP BY SAQGPA.SERVICE_ID, SAQGPA.GREENBOOK, SAQGPA.FABLOCATION_ID, SAQGPA.GOT_CODE, SAQGPA.KIT_ID,SAQGPA.		QUOTE_RECORD_ID, SAQGPA.QTEREV_RECORD_ID,  ISNULL(PROCESS_TYPE,'')  , ISNULL(DEVICE_NODE,''),KIT_NUMBER,KITNUMBER_RECORD_ID,KIT_NAME ) SAQGPA 
                INNER JOIN SAQRIT ON SAQGPA.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND SAQGPA.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID AND SAQGPA.SERVICE_ID = SAQRIT.SERVICE_ID AND SAQGPA.GREENBOOK = SAQRIT.GREENBOOK AND SAQGPA.KIT_ID = SAQRIT.KIT_ID AND SAQGPA.GOT_CODE = SAQRIT.GOT_CODE AND ISNULL(SAQGPA.PROCESS_TYPE,'') = ISNULL(SAQRIT.PROCESS_TYPE,'') AND ISNULL(SAQGPA.DEVICE_NODE,'') = ISNULL(SAQRIT.DEVICE_NODE,'') AND SAQGPA.FABLOCATION_ID = SAQRIT.FABLOCATION_ID
                LEFT JOIN SAQRIP (NOLOCK) ON SAQRIP.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND SAQRIP.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID AND SAQRIP.SERVICE_RECORD_ID = SAQRIT.SERVICE_RECORD_ID AND SAQRIP.PART_RECORD_ID = SAQRIT.KITNUMBER_RECORD_ID 
                WHERE SAQRIT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQRIT.SERVICE_ID = '{ServiceId}' AND ISNULL(SAQGPA.KIT_NUMBER,'') != '' AND ISNULL(SAQRIP.PART_RECORD_ID,'') = '')IQ """.format(UserId=self.user_id, UserName=self.user_name, QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))                                                                                                       
        elif self.quote_service_entitlement_type in ('STR-OFFBGBPMCMKTGCPCND OBJ-AS','STR-OFFBGBSMKTGCPCND OBJ-AS'):
        
            Sql.RunQuery("""INSERT SAQRIP (QUOTE_REVISION_ITEM_PRODUCT_LIST_RECORD_ID,CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified, PART_DESCRIPTION, PART_NUMBER, PART_RECORD_ID, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, QUANTITY, QUOTE_ID, QTEITM_RECORD_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, LINE, NEW_PART,GREENBOOK,GREENBOOK_RECORD_ID,FABLOCATION_ID, FABLOCATION_NAME,FABLOCATION_RECORD_ID  ) 
            SELECT 
                CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REVISION_ITEM_PRODUCT_LIST_RECORD_ID,
                '{UserName}' AS CPQTABLEENTRYADDEDBY,
                GETDATE() as CPQTABLEENTRYDATEADDED,
                {UserId} as CpqTableEntryModifiedBy,
                GETDATE() as CpqTableEntryDateModified,IQ.* FROM 
                (SELECT DISTINCT
                SAQGPA.KIT_NAME AS PART_DESCRIPTION,
                SAQGPA.KIT_NUMBER AS PART_NUMBER,
                SAQGPA.KITNUMBER_RECORD_ID AS PART_RECORD_ID,
                SAQRIT.SERVICE_DESCRIPTION,
                SAQRIT.SERVICE_ID,
                SAQRIT.SERVICE_RECORD_ID,
                NULL as QUANTITY,
                SAQRIT.QUOTE_ID,
                SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID,
                SAQRIT.QUOTE_RECORD_ID,
                SAQRIT.QTEREV_ID,
                SAQRIT.QTEREV_RECORD_ID,
                SAQRIT.LINE,
                NULL AS NEW_PART,
                SAQRIT.GREENBOOK,
                SAQRIT.GREENBOOK_RECORD_ID,
                SAQRIT.FABLOCATION_ID,
                SAQRIT.FABLOCATION_NAME, 
                SAQRIT.FABLOCATION_RECORD_ID    
                FROM SAQGPA (NOLOCK) 
                INNER JOIN SAQRIT (NOLOCK) ON SAQGPA.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND SAQGPA.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID AND SAQGPA.SERVICE_ID = SAQRIT.SERVICE_ID AND SAQGPA.GOT_CODE = SAQRIT.GOT_CODE AND SAQGPA.GREENBOOK = SAQRIT.GREENBOOK AND SAQGPA.FABLOCATION_ID = SAQRIT.FABLOCATION_ID AND SAQRIT.OBJECT_ID = CASE WHEN SAQRIT.OBJECT_ID = 'Scheduled Maintenance' THEN SAQGPA.MNTEVT_LEVEL ELSE SAQGPA.PM_ID END AND SAQRIT.KIT_ID = SAQGPA.KIT_ID
                LEFT JOIN SAQRIP (NOLOCK) ON SAQRIP.QUOTE_RECORD_ID = SAQGPA.QUOTE_RECORD_ID AND SAQRIP.QTEREV_RECORD_ID = SAQGPA.QTEREV_RECORD_ID AND SAQRIP.SERVICE_ID = SAQGPA.SERVICE_ID AND SAQRIP.PART_NUMBER = SAQGPA.KIT_NUMBER 
                WHERE SAQGPA.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQGPA.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQGPA.SERVICE_ID = '{ServiceId}' AND ISNULL(SAQGPA.KIT_NUMBER,'') != '' AND ISNULL(SAQRIP.PART_NUMBER,'') = '')IQ """.format(UserId=self.user_id, UserName=self.user_name, QuoteRecordId=self.contract_quote_record_id, RevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
        #CR713 - A055S000P01-20911 - End - M   
        
        elif not (self.service_id == 'Z0100' and self.parent_service_id == 'Z0092'):
            Sql.RunQuery("""INSERT SAQRIP (QUOTE_REVISION_ITEM_PRODUCT_LIST_RECORD_ID,CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified, PART_DESCRIPTION, PART_NUMBER, PART_RECORD_ID, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID,PAR_PRDOFR_ID,PAR_PRDOFR_RECORD_ID, QUANTITY, QUOTE_ID, QTEITM_RECORD_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, LINE, NEW_PART ) 
                SELECT 
                    CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REVISION_ITEM_PRODUCT_LIST_RECORD_ID,
                    '{UserName}' AS CPQTABLEENTRYADDEDBY,
                    GETDATE() as CPQTABLEENTRYDATEADDED,
                    {UserId} as CpqTableEntryModifiedBy,
                    GETDATE() as CpqTableEntryDateModified,
                    SAQRSP.PART_DESCRIPTION,
                    SAQRSP.PART_NUMBER,
                    SAQRSP.PART_RECORD_ID,
                    SAQRSP.SERVICE_DESCRIPTION,
                    SAQRSP.SERVICE_ID,
                    SAQRSP.SERVICE_RECORD_ID,
                    SAQRIT.PAR_PRDOFR_ID,
                    SAQRIT.PAR_PRDOFR_RECORD_ID,
                    SAQRSP.QUANTITY,
                    SAQRSP.QUOTE_ID,
                    SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID,
                    SAQRSP.QUOTE_RECORD_ID,
                    SAQRSP.QTEREV_ID,
                    SAQRSP.QTEREV_RECORD_ID,
                    SAQRIT.LINE,
                    SAQRSP.NEW_PART
                FROM SAQRSP (NOLOCK) 
                JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = SAQRSP.QUOTE_RECORD_ID AND SAQRIT.QTEREV_RECORD_ID = SAQRSP.QTEREV_RECORD_ID AND SAQRIT.SERVICE_RECORD_ID = SAQRSP.SERVICE_RECORD_ID AND SAQRIT.GREENBOOK_RECORD_ID = SAQRSP.GREENBOOK_RECORD_ID AND SAQRIT.FABLOCATION_RECORD_ID = SAQRSP.FABLOCATION_RECORD_ID AND ISNULL(SAQRIT.PAR_PRDOFR_ID,'') = ISNULL(SAQRSP.PAR_SERVICE_ID,'')
                LEFT JOIN SAQRIP (NOLOCK) ON SAQRIP.QUOTE_RECORD_ID = SAQRSP.QUOTE_RECORD_ID AND SAQRIP.QTEREV_RECORD_ID = SAQRSP.QTEREV_RECORD_ID AND SAQRIP.SERVICE_RECORD_ID = SAQRSP.SERVICE_RECORD_ID AND SAQRIP.PART_RECORD_ID = SAQRSP.PART_RECORD_ID AND ISNULL(SAQRSP.PAR_SERVICE_ID,'') = ISNULL(SAQRIP.PAR_PRDOFR_ID,'')
                WHERE SAQRSP.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRSP.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQRSP.SERVICE_ID = '{ServiceId}' AND ISNULL(SAQRIP.PART_RECORD_ID,'') = '' """.format(UserId=self.user_id, UserName=self.user_name, QuoteRecordId=self.contract_quote_record_id, RevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
            
        ##calling cps pricing
        if self.service_id == 'Z0100' : 	
            ##calling the iflow for pricing..
            try:
                # if action_type == 'UPDATE_LINE_ITEMS':
                Log.Info("PART PRICING IFLOW STARTED!")
                CQPARTIFLW.iflow_pricing_call(str(self.user_name),str(self.contract_quote_id),str(self.contract_quote_revision_record_id))
            except:
                Log.Info("PART PRICING IFLOW ERROR!")
    def _insert_quote_item_fpm_forecast_parts(self):
    
        GetdelPartList=SqlHelper.GetList("""SELECT A.PART_NUMBER AS Basepart, B.PART_NUMBER AS Childpart FROM SAQSPT A JOIN SAQSPT B ON A.QUOTE_RECORD_ID=B.QUOTE_RECORD_ID AND A.PART_NUMBER=B.PAR_PART_NUMBER WHERE A.QUOTE_RECORD_ID='{}' AND A.QTEREV_RECORD_ID='{}' AND (A.CUSTOMER_ANNUAL_QUANTITY IS NULL OR A.CUSTOMER_ANNUAL_QUANTITY <=0) AND (B.CUSTOMER_ANNUAL_QUANTITY IS NOT NULL  OR B.CUSTOMER_ANNUAL_QUANTITY >0)""".format(str(self.contract_quote_record_id),str(self.contract_quote_revision_record_id)))
        partList=[]
        for ele in GetdelPartList:
            partList.append(ele.Basepart)
            partList.append(ele.Childpart)
        partList=str(tuple(partList)) or ''
        if partList !='':
            Sql.RunQuery("""DELETE FROM SAQSPT WHERE QUOTE_RECORD_ID='{}' AND QTEREV_RECORD_ID='{}' AND PART_NUMBER IN {}""".format(str(self.contract_quote_record_id),str(self.contract_quote_revision_record_id),str(partList)))
            
        Sql.RunQuery("DELETE FROM SAQIFP WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID = '{ServiceId}'".format(
                    QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id))
        
        Sql.RunQuery("""INSERT SAQIFP (QUOTE_ITEM_FORECAST_PART_RECORD_ID,CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified, PART_DESCRIPTION, PART_NUMBER, PART_RECORD_ID, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, ANNUAL_QUANTITY, QUOTE_ID,CUSTOMER_PART_NUMBER, QTEITM_RECORD_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID,BASEUOM_ID,BASEUOM_RECORD_ID,MATPRIGRP_ID,MATPRIGRP_NAME,MATPRIGRP_RECORD_ID, LINE, GLOBALCURRENCY_RECORD_ID,GLOBAL_CURRENCY,TAX_PERCENTAGE,DOCURR_RECORD_ID,DOC_CURRENCY,PRICING_STATUS,SCHEDULE_MODE,DELIVERY_MODE,VALID_FROM_DATE,VALID_TO_DATE,ODCC_FLAG,RETURN_TYPE,SHPACCOUNT_ID,STPACCOUNT_ID,YEAR_1_DEMAND,YEAR_2_DEMAND,YEAR_3_DEMAND,EXCHANGE_ELIGIBLE,CUSTOMER_PARTICIPATE,CUSTOMER_ACCEPT_PART,SALESORG_ID) 
            SELECT 
                CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_FORECAST_PART_RECORD_ID,
                '{UserName}' AS CPQTABLEENTRYADDEDBY,
                GETDATE() as CPQTABLEENTRYDATEADDED,
                {UserId} as CpqTableEntryModifiedBy,
                GETDATE() as CpqTableEntryDateModified,
                SAQSPT.PART_DESCRIPTION,
                SAQSPT.PART_NUMBER,
                SAQSPT.PART_RECORD_ID,
                SAQSPT.SERVICE_DESCRIPTION,
                SAQSPT.SERVICE_ID,
                SAQSPT.SERVICE_RECORD_ID,
                SAQSPT.CUSTOMER_ANNUAL_QUANTITY,
                SAQSPT.QUOTE_ID,
                SAQSPT.CUSTOMER_PART_NUMBER,
                SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID,
                SAQSPT.QUOTE_RECORD_ID,
                SAQSPT.QTEREV_ID,
                SAQSPT.QTEREV_RECORD_ID,
                SAQSPT.BASEUOM_ID,
                SAQSPT.BASEUOM_RECORD_ID,
                SAQSPT.MATPRIGRP_ID,
                SAQSPT.MATPRIGRP_NAME,
                SAQSPT.MATPRIGRP_RECORD_ID,
                SAQRIT.LINE,
                SAQRIT.GLOBAL_CURRENCY_RECORD_ID,
                SAQRIT.GLOBAL_CURRENCY,
                SAQRIS.TAX_PERCENTAGE,
                SAQRIT.DOCURR_RECORD_ID,
                SAQRIT.DOC_CURRENCY,
                'ACQUIRING...' AS PRICING_STATUS,
                SAQSPT.SCHEDULE_MODE,
                SAQSPT.DELIVERY_MODE,
                SAQSPT.VALID_FROM_DATE,
                SAQSPT.VALID_TO_DATE,
                SAQSPT.ODCC_FLAG,
                SAQSPT.RETURN_TYPE,
                SAQSPT.SHPACCOUNT_ID,
                SAQSPT.STPACCOUNT_ID,
                SAQSPT.YEAR_1_DEMAND,
                SAQSPT.YEAR_2_DEMAND,
                SAQSPT.YEAR_3_DEMAND,
                SAQSPT.EXCHANGE_ELIGIBLE,
                SAQSPT.CUSTOMER_PARTICIPATE,
                SAQSPT.CUSTOMER_ACCEPT_PART,
                SAQSPT.SALESORG_ID                            
                                
                                                
            FROM SAQSPT (NOLOCK) 
            JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = SAQSPT.QUOTE_RECORD_ID AND SAQRIT.QTEREV_RECORD_ID = SAQSPT.QTEREV_RECORD_ID AND SAQRIT.SERVICE_RECORD_ID = SAQSPT.SERVICE_RECORD_ID 
            JOIN SAQRIS (NOLOCK) ON SAQRIS.QTEREV_RECORD_ID = SAQSPT.QTEREV_RECORD_ID AND SAQRIS.QUOTE_RECORD_ID = SAQSPT.QUOTE_RECORD_ID AND SAQRIS.SERVICE_ID = SAQSPT.SERVICE_ID
            LEFT JOIN SAQIFP (NOLOCK) ON SAQIFP.QUOTE_RECORD_ID = SAQSPT.QUOTE_RECORD_ID AND SAQIFP.QTEREV_RECORD_ID = SAQSPT.QTEREV_RECORD_ID AND SAQIFP.SERVICE_RECORD_ID = SAQSPT.SERVICE_RECORD_ID AND SAQIFP.PART_RECORD_ID = SAQSPT.PART_RECORD_ID                                                                                    
            WHERE SAQSPT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSPT.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQSPT.SERVICE_ID = '{ServiceId}' AND SAQSPT.CUSTOMER_ANNUAL_QUANTITY > 0 AND ISNULL(SAQIFP.PART_RECORD_ID,'') = '' """.format(UserId=self.user_id, UserName=self.user_name, QuoteRecordId=self.contract_quote_record_id, RevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
        
        ##calling the iflow for pricing..
        try:
            Log.Info("PART PRICING IFLOW STARTED!")
            CQPARTIFLW.iflow_pricing_call(str(self.user_name),str(self.contract_quote_id),str(self.contract_quote_revision_record_id),'')
        except:
            Log.Info("PART PRICING IFLOW ERROR!")
                                        
        ##User story 4432 ends..
    #A055S000P01-15550 start
    # def _insert_item_level_delivery_schedule(self):
    # 	try:
    # 		Sql.RunQuery("DELETE FROM SAQIPD WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID = '{ServiceId}'".format(
    # 					QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id))
    # 		Log.Info('2089----')
    # 		insert_item_level_delivery_schedule = "INSERT SAQIPD (QUOTE_REV_ITEM_PART_DELIVERY_RECORD_ID,DELIVERY_SCHED_CAT,DELIVERY_SCHED_DATE,LINE,PART_DESCRIPTION,PART_NUMBER,PART_RECORD_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,QUANTITY,QUOTE_ID,QTEITMPRT_RECORD_ID,QTEITM_RECORD_ID,QUOTE_RECORD_ID,QTEREV_ID,QTEREVSPT_RECORD_ID,QTEREV_RECORD_ID,MATERIALSTATUS_ID,MATERIALSTATUS_RECORD_ID,SALESUOM_ID,UOM_ID,DELIVERY_MODE,CUSTOMER_ANNUAL_QUANTITY,SCHEDULED_MODE) select CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REV_ITEM_PART_DELIVERY_RECORD_ID,DS.DELIVERY_SCHED_CAT,DS.DELIVERY_SCHED_DATE,FP.LINE,DS.PART_DESCRIPTION,DS.PART_NUMBER,DS.PART_RECORD_ID,DS.SERVICE_DESCRIPTION,DS.SERVICE_ID,DS.SERVICE_RECORD_ID,DS.QUANTITY,DS.QUOTE_ID,FP.QUOTE_ITEM_FORECAST_PART_RECORD_ID as QTEITMPRT_RECORD_ID,FP.QTEITM_RECORD_ID,FP.QUOTE_RECORD_ID,FP.QTEREV_ID,DS.QTEREVSPT_RECORD_ID,DS.QTEREV_RECORD_ID,DS.MATERIALSTATUS_ID,DS.MATERIALSTATUS_RECORD_ID,DS.SALESUOM_ID,DS.UOM_ID,DS.DELIVERY_MODE,DS.CUSTOMER_ANNUAL_QUANTITY,DS.SCHEDULED_MODE FROM SAQSPD DS JOIN SAQIFP FP ON FP.PART_RECORD_ID = DS.PART_RECORD_ID and FP.QUOTE_RECORD_ID= DS.QUOTE_RECORD_ID and FP.QTEREV_ID= DS.QTEREV_ID where FP.QUOTE_ID = '{QuoteRecordId}' and FP.QTEREV_RECORD_ID= '{rev_rec_id}'".format(QuoteRecordId=self.contract_quote_id,rev_rec_id=self.contract_quote_revision_record_id)
    # 		Log.Info('insert_item_level_delivery_schedule==='+str(insert_item_level_delivery_schedule))
    # 		Sql.RunQuery(insert_item_level_delivery_schedule)
    # 	except:
    # 		pass
    #A055S000P01-15550 end
    
    def _delete_item_related_table_records(self):
        for delete_object in ['SAQIAE','SAQICA','SAQRIO','SAQICO']:
            delete_statement = "DELETE DT FROM " +str(delete_object)+" DT (NOLOCK) JOIN SAQSCE (NOLOCK) ON DT.EQUIPMENT_RECORD_ID = SAQSCE.EQUIPMENT_RECORD_ID AND DT.SERVICE_ID=SAQSCE.SERVICE_ID AND DT.QUOTE_RECORD_ID=SAQSCE.QUOTE_RECORD_ID AND DT.QTEREV_RECORD_ID=SAQSCE.QTEREV_RECORD_ID WHERE DT.QUOTE_RECORD_ID='{}' AND DT.QTEREV_RECORD_ID='{}' AND ISNULL(SAQSCE.CONFIGURATION_STATUS, '')='INCOMPLETE' AND DT.SERVICE_ID='{}' ".format(self.contract_quote_record_id, self.contract_quote_revision_record_id, self.service_id)
            if delete_object == "SAQICO" and self.service_id in ('Z0110','Z0108'):
                delete_statement = "DELETE DT FROM " +str(delete_object)+" DT (NOLOCK) WHERE DT.QUOTE_RECORD_ID='{}' AND DT.QTEREV_RECORD_ID='{}' AND DT.SERVICE_ID='{}' ".format(self.contract_quote_record_id, self.contract_quote_revision_record_id, self.service_id)			
            Sql.RunQuery(delete_statement)
    
        join_condition_string = ''
        if self.quote_service_entitlement_type in ('STR-OFFBGBEQ OBJ-EQ'):
            join_condition_string = """AND ISNULL(SAQRIT.OBJECT_ID, '') = SAQSCE.EQUIPMENT_ID"""
        # item entitlement delete
        quote_item_entitlement_delete_statement = """
                DELETE SAQITE 
                    FROM SAQITE (NOLOCK) 
                    JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID = SAQITE.QTEITM_RECORD_ID 
                    JOIN SAQSCE ON SAQSCE.QUOTE_RECORD_ID=SAQRIT.QUOTE_RECORD_ID AND SAQSCE.QTEREV_RECORD_ID=SAQRIT.QTEREV_RECORD_ID AND SAQSCE.SERVICE_ID=SAQRIT.SERVICE_ID AND SAQSCE.FABLOCATION_RECORD_ID = SAQRIT.FABLOCATION_RECORD_ID AND SAQSCE.GREENBOOK_RECORD_ID = SAQRIT.GREENBOOK_RECORD_ID {JoinCondition}
                    WHERE SAQITE.QUOTE_RECORD_ID='{QuoteRecordId}' AND SAQITE.QTEREV_RECORD_ID='{QuoteRevisionRecordId}' AND ISNULL(SAQSCE.CONFIGURATION_STATUS, '')='INCOMPLETE' AND SAQITE.SERVICE_ID='{ServiceId}' """.format(QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id, JoinCondition=join_condition_string)	
        Sql.RunQuery(quote_item_entitlement_delete_statement)
        # item delete
        quote_item_delete_statement = """
                DELETE SAQRIT                                
                    FROM SAQRIT (NOLOCK) 
                    JOIN SAQSCE ON SAQSCE.QUOTE_RECORD_ID=SAQRIT.QUOTE_RECORD_ID AND SAQSCE.QTEREV_RECORD_ID=SAQRIT.QTEREV_RECORD_ID AND SAQSCE.SERVICE_ID=SAQRIT.SERVICE_ID AND SAQSCE.FABLOCATION_RECORD_ID = SAQRIT.FABLOCATION_RECORD_ID AND SAQSCE.GREENBOOK_RECORD_ID = SAQRIT.GREENBOOK_RECORD_ID {JoinCondition}                                         
                    WHERE SAQRIT.QUOTE_RECORD_ID='{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID='{QuoteRevisionRecordId}' AND ISNULL(SAQSCE.CONFIGURATION_STATUS, '') ='INCOMPLETE' AND SAQRIT.SERVICE_ID='{ServiceId}' """.format(QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id, JoinCondition=join_condition_string)	
        Sql.RunQuery(quote_item_delete_statement)
    def _service_based_quote_items_entitlement_insert(self, update=False):		
        #if update: # need to verify one more time
        ancillary_join = ""
        ancillary_where = ""
        # if self.is_ancillary == True or self.addon_product == True:
        # 	ancillary_join = """JOIN SAQRIT (NOLOCK) PAR_SAQRIT ON 	SAQRIT.QUOTE_RECORD_ID = PAR_SAQRIT.QUOTE_RECORD_ID
        # 										AND SAQRIT.SERVICE_RECORD_ID = PAR_SAQRIT.SERVICE_RECORD_ID
        # 										AND SAQRIT.QTEREV_RECORD_ID = PAR_SAQRIT.QTEREV_RECORD_ID
        # 										AND PAR_SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID = SAQRIT.PARQTEITM_LINE_RECORD_ID	
        # 										AND PAR_SAQRIT.SERVICE_ID = '{parent_service_id}'""".format(parent_service_id = self.parent_service_id)
        # 	ancillary_where = " AND PAR_SAQRIT.SERVICE_ID = '{parent_service_id}'".format(parent_service_id = self.parent_service_id)
        Sql.RunQuery("DELETE SAQITE FROM SAQITE WHERE SAQITE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQITE.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQITE.SERVICE_ID = '{ServiceId}'".format(QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
        Sql.RunQuery("""INSERT SAQITE (QUOTE_REV_ITEM_ENTITLEMENT_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified, CPS_CONFIGURATION_ID, CPS_MATCH_ID, ENTITLEMENT_COST_IMPACT, ENTITLEMENT_GROUP_ID, ENTITLEMENT_GROUP_XML, ENTITLEMENT_PRICE_IMPACT, ENTITLEMENT_XML, IS_CHANGED, LINE, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, QTEITM_RECORD_ID, QUOTE_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID)
                    SELECT
                        CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REV_ITEM_ENTITLEMENT_RECORD_ID,
                        '{UserName}' AS CPQTABLEENTRYADDEDBY,
                        GETDATE() as CPQTABLEENTRYDATEADDED,
                        {UserId} as CpqTableEntryModifiedBy,
                        GETDATE() as CpqTableEntryDateModified,
                        {ObjectName}.CPS_CONFIGURATION_ID,
                        {ObjectName}.CPS_MATCH_ID,
                        null as ENTITLEMENT_COST_IMPACT,
                        null as ENTITLEMENT_GROUP_ID,
                        null as ENTITLEMENT_GROUP_XML,
                        null as ENTITLEMENT_PRICE_IMPACT,
                        {ObjectName}.ENTITLEMENT_XML,
                        null as IS_CHANGED,
                        SAQRIT.LINE,						
                        SAQRIT.SERVICE_DESCRIPTION,
                        SAQRIT.SERVICE_ID,
                        SAQRIT.SERVICE_RECORD_ID,
                        SAQRIT.QUOTE_REVISION_CONTRACT_ITEM_ID as QTEITM_RECORD_ID,						
                        SAQRIT.QUOTE_ID,
                        SAQRIT.QUOTE_RECORD_ID,
                        SAQRIT.QTEREV_ID,
                        SAQRIT.QTEREV_RECORD_ID,						
                        null as GREENBOOK,
                        null as GREENBOOK_RECORD_ID
                    FROM {ObjectName} (NOLOCK) 
                    JOIN SAQRIT (NOLOCK) ON SAQRIT.QUOTE_RECORD_ID = {ObjectName}.QUOTE_RECORD_ID
                                                AND SAQRIT.SERVICE_RECORD_ID = {ObjectName}.SERVICE_RECORD_ID
                                                AND SAQRIT.QTEREV_RECORD_ID = {ObjectName}.QTEREV_RECORD_ID
                    {ancillary_join}					
                    WHERE {ObjectName}.QUOTE_RECORD_ID = '{QuoteRecordId}' AND {ObjectName}.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND {ObjectName}.SERVICE_ID = '{ServiceId}' AND ISNULL({ObjectName}.CONFIGURATION_STATUS,'') = 'COMPLETE'	{ancillary_where}		
                """.format(UserId=self.user_id, UserName=self.user_name, ObjectName='SAQTSE', QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id,parent_service_id=  self.parent_service_id, ancillary_join =ancillary_join, ancillary_where =ancillary_where))
        return True
    def _simple_delete_item_related_table_records(self):
        for delete_object in ['SAQRIO','SAQICO']:
            delete_statement = "DELETE DT FROM " +str(delete_object)+" DT (NOLOCK) JOIN SAQSCO ON DT.EQUIPMENT_RECORD_ID = SAQSCO.EQUIPMENT_RECORD_ID AND DT.SERVICE_ID=SAQSCO.SERVICE_ID  AND DT.QUOTE_RECORD_ID=SAQSCO.QUOTE_RECORD_ID AND DT.QTEREV_RECORD_ID=SAQSCO.QTEREV_RECORD_ID JOIN SAQSCE (NOLOCK) ON DT.EQUIPMENT_RECORD_ID = SAQSCE.EQUIPMENT_RECORD_ID AND SAQSCO.PAR_SERVICE_ID=SAQSCE.SERVICE_ID AND DT.QUOTE_RECORD_ID=SAQSCE.QUOTE_RECORD_ID AND DT.QTEREV_RECORD_ID=SAQSCE.QTEREV_RECORD_ID WHERE DT.QUOTE_RECORD_ID='{}' AND DT.QTEREV_RECORD_ID='{}' AND ISNULL(SAQSCE.CONFIGURATION_STATUS, '')='INCOMPLETE' AND DT.SERVICE_ID='{}' ".format(self.contract_quote_record_id, self.contract_quote_revision_record_id, self.service_id)			
            Sql.RunQuery(delete_statement)
        
        # item delete
        quote_item_delete_statement = """                                                                    
                DELETE SAQRIT 
                    FROM SAQRIT (NOLOCK)                                  
                    JOIN SAQSCO (NOLOCK) ON SAQRIT.SERVICE_ID=SAQSCO.SERVICE_ID  AND SAQRIT.QUOTE_RECORD_ID=SAQSCO.QUOTE_RECORD_ID AND SAQRIT.QTEREV_RECORD_ID=SAQSCO.QTEREV_RECORD_ID JOIN SAQSCE (NOLOCK) ON SAQSCE.QUOTE_RECORD_ID=SAQRIT.QUOTE_RECORD_ID AND SAQSCE.QTEREV_RECORD_ID=SAQRIT.QTEREV_RECORD_ID AND SAQSCE.SERVICE_ID=SAQSCO.PAR_SERVICE_ID AND SAQSCE.FABLOCATION_RECORD_ID = SAQRIT.FABLOCATION_RECORD_ID AND SAQSCE.GREENBOOK_RECORD_ID = SAQRIT.GREENBOOK_RECORD_ID                                                 
                    WHERE SAQRIT.QUOTE_RECORD_ID='{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID='{QuoteRevisionRecordId}' AND ISNULL(SAQSCE.CONFIGURATION_STATUS, '') ='INCOMPLETE' AND SAQRIT.SERVICE_ID='{ServiceId}' """.format(QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id)	
        Sql.RunQuery(quote_item_delete_statement)
    def _quote_item_qty_update(self):
        if self.quote_service_entitlement_type in ("STR-OFFBGBPMCMKTGCPCND OBJ-AS","STR-OFFBGBSMKTGCPCND OBJ-AS"):
            #INC08745555 Start - M
            #A055S000P01-20653, INC08921516, A055S000P01-21072 - M
            Sql.RunQuery(""" UPDATE SAQRIT SET QUANTITY = CASE WHEN SAQRIT.OBJECT_TYPE IN ('EVENT','KIT') AND SAQRIT.BILLING_TYPE IN ('VARIABLE', 'MILESTONE') THEN CEILING(SAQICO.CTAJPM) ELSE 1 END,
                            ADJ_PM_FREQUENCY = SAQICO.ADJ_PM_FREQUENCY,
                            CTAJPM = SAQICO.CTAJPM
                            FROM SAQRIT (NOLOCK) 
                            INNER JOIN (SELECT SAQICO.QUOTE_RECORD_ID, SAQICO.QTEREV_RECORD_ID,SAQICO.SERVICE_ID,SAQICO.GRNBOK,
                                SAQICO.OBJECT_ID, SAQICO.GOT_CODE,SAQICO.MNTEVT_LEVEL,SAQICO.LINE,SAQICO.KIT_ID,
                                SUM(ISNULL(SAQICO.QUANTITY, 0)) as QUANTITY,
                                SUM(ISNULL(SAQICO.ADJ_PM_FREQUENCY, 0)) as ADJ_PM_FREQUENCY,
                                SUM(ISNULL(SAQICO.CTAJPM, 0)) as CTAJPM,
                                SUM(ISNULL(SAQICO.SSCM_PM_FREQUENCY, 0)) as SSCM_PM_FREQUENCY
                                FROM SAQICO (NOLOCK) WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}' GROUP BY SAQICO.QUOTE_RECORD_ID, SAQICO.QTEREV_RECORD_ID, SAQICO.SERVICE_ID, SAQICO.GRNBOK,
                                SAQICO.OBJECT_ID, SAQICO.GOT_CODE,SAQICO.KIT_ID,SAQICO.MNTEVT_LEVEL,SAQICO.LINE) SAQICO ON SAQICO.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND SAQICO.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID AND SAQICO.SERVICE_ID = SAQRIT.SERVICE_ID AND SAQICO.GRNBOK = SAQRIT.GREENBOOK AND SAQICO.OBJECT_ID = SAQRIT.OBJECT_ID AND SAQICO.GOT_CODE = SAQRIT.GOT_CODE AND SAQICO.MNTEVT_LEVEL = SAQRIT.MNTEVT_LEVEL AND SAQRIT.LINE = SAQICO.LINE AND SAQICO.KIT_ID = SAQRIT.KIT_ID
                            WHERE SAQRIT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQRIT.SERVICE_ID = '{ServiceId}'""".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id))	
        #INC08745555 End - M
        #A055S000P01-20653, INC08921516, A055S000P01-21072 - M
        # elif self.quote_service_entitlement_type == "STR-OFFBGBSMKTGCPCND OBJ-AS":
        # 	Sql.RunQuery(""" UPDATE SAQRIT SET QUANTITY = IQ.QUANTITY 
        # 	FROM SAQRIT (NOLOCK) 
        # 	INNER JOIN (SELECT SERVICE_ID,SAQGPA.GREENBOOK,SAQGPA.FABLOCATION_ID,SAQGPA.GOT_CODE,SAQGPA.PM_ID,SAQGPA.QUOTE_RECORD_ID,SAQGPA.QTEREV_RECORD_ID,SUM(ISNULL(SAQGPA.PM_FREQUENCY, 0)) AS QUANTITY, ISNULL(PROCESS_TYPE,'') AS PROCESS_TYPE , ISNULL(DEVICE_NODE,'') AS DEVICE_NODE
        # 		FROM SAQGPA (NOLOCK)  
        # 		WHERE SAQGPA.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQGPA.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQGPA.SERVICE_ID = '{ServiceId}' AND MNTEVT_LEVEL != 'Scheduled Maintenance'
        # 		GROUP BY SERVICE_ID,SAQGPA.GREENBOOK,SAQGPA.FABLOCATION_ID,SAQGPA.GOT_CODE,SAQGPA.PM_ID,SAQGPA.QUOTE_RECORD_ID,SAQGPA.QTEREV_RECORD_ID,ISNULL(PROCESS_TYPE,'')  , ISNULL(DEVICE_NODE,'')
        # 		UNION
        # 		SELECT SERVICE_ID,SAQGPA.GREENBOOK,SAQGPA.FABLOCATION_ID,SAQGPA.GOT_CODE,SAQGPA.MNTEVT_LEVEL,SAQGPA.QUOTE_RECORD_ID,SAQGPA.QTEREV_RECORD_ID,SUM(ISNULL(SAQGPA.PM_FREQUENCY, 0)) AS QUANTITY, ISNULL(PROCESS_TYPE,'') AS PROCESS_TYPE , ISNULL(DEVICE_NODE,'') AS DEVICE_NODE
        # 		FROM SAQGPA (NOLOCK)  
        # 		WHERE SAQGPA.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQGPA.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQGPA.SERVICE_ID = '{ServiceId}' AND MNTEVT_LEVEL = 'Scheduled Maintenance'
        # 		GROUP BY SERVICE_ID,SAQGPA.GREENBOOK,SAQGPA.FABLOCATION_ID,SAQGPA.GOT_CODE,SAQGPA.MNTEVT_LEVEL,SAQGPA.QUOTE_RECORD_ID,SAQGPA.
        # 	QTEREV_RECORD_ID,ISNULL(PROCESS_TYPE,'') , ISNULL(DEVICE_NODE,'') ) IQ ON IQ.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND IQ.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID AND IQ.SERVICE_ID = SAQRIT.SERVICE_ID AND SAQRIT.OBJECT_ID = IQ.PM_ID AND SAQRIT.FABLOCATION_ID = IQ.FABLOCATION_ID AND SAQRIT.GREENBOOK = IQ.GREENBOOK AND SAQRIT.GOT_CODE = IQ.GOT_CODE
        # 	WHERE SAQRIT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQRIT.SERVICE_ID = '{ServiceId}'""".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id))
            
        elif self.quote_service_entitlement_type in ('STR-OFFBGBKTGCPCND OBJ-GPAS'):
            #INC08745555 Start - M
            #A055S000P01-20653, INC08921516, A055S000P01-21072 - M
            Sql.RunQuery(""" UPDATE SAQRIT SET QUANTITY = CASE WHEN SAQRIT.OBJECT_TYPE IN ('EVENT','KIT') AND SAQRIT.BILLING_TYPE IN ('VARIABLE', 'MILESTONE') THEN CEILING(SAQICO.CTAJPM) ELSE 1 END,
                            ADJ_PM_FREQUENCY = SAQICO.ADJ_PM_FREQUENCY,
                            CTAJPM = SAQICO.CTAJPM
                            FROM SAQRIT (NOLOCK) 
                            INNER JOIN (SELECT SAQICO.QUOTE_RECORD_ID, SAQICO.QTEREV_RECORD_ID,SAQICO.SERVICE_ID,SAQICO.GRNBOK,
                                SAQICO.KIT_ID, SAQICO.GOT_CODE,SAQICO.LINE,
                                SUM(ISNULL(SAQICO.QUANTITY, 0)) as QUANTITY,
                                SUM(ISNULL(SAQICO.ADJ_PM_FREQUENCY, 0)) as ADJ_PM_FREQUENCY,
                                SUM(ISNULL(SAQICO.CTAJPM, 0)) as CTAJPM,
                                SUM(ISNULL(SAQICO.SSCM_PM_FREQUENCY, 0)) as SSCM_PM_FREQUENCY
                                FROM SAQICO (NOLOCK) WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQICO.SERVICE_ID = '{ServiceId}' GROUP BY SAQICO.QUOTE_RECORD_ID, SAQICO.QTEREV_RECORD_ID,SAQICO.SERVICE_ID,SAQICO.GRNBOK,
                                SAQICO.KIT_ID, SAQICO.GOT_CODE,SAQICO.LINE) SAQICO ON SAQICO.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND SAQICO.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID AND SAQICO.SERVICE_ID = SAQRIT.SERVICE_ID AND SAQICO.GRNBOK = SAQRIT.GREENBOOK AND SAQICO.KIT_ID = SAQRIT.KIT_ID AND SAQICO.GOT_CODE = SAQRIT.GOT_CODE AND SAQRIT.LINE = SAQICO.LINE
                            WHERE SAQRIT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQRIT.SERVICE_ID = '{ServiceId}'""".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id))
            #INC08745555 End - M
            #A055S000P01-20653, INC08921516, A055S000P01-21072 - M
        else:
            Sql.RunQuery(""" UPDATE SAQRIT SET QUANTITY = IQ.QUANTITY FROM SAQRIT (NOLOCK) INNER JOIN (SELECT COUNT(*) AS QUANTITY,QTEREV_RECORD_ID, QUOTE_RECORD_ID, SERVICE_ID,GREENBOOK,LINE FROM SAQRIO (NOLOCK) WHERE 
                    QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}' GROUP BY QTEREV_RECORD_ID, QUOTE_RECORD_ID, SERVICE_ID,GREENBOOK,LINE ) IQ ON IQ.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID AND IQ.QTEREV_RECORD_ID = SAQRIT.QTEREV_RECORD_ID AND IQ.SERVICE_ID = SAQRIT.SERVICE_ID AND SAQRIT.GREENBOOK = IQ.GREENBOOK AND IQ.LINE = SAQRIT.LINE WHERE 
                    SAQRIT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQRIT.SERVICE_ID = '{ServiceId}'""".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.service_id))
    def _simple_quote_items_summary_insert(self):
        if self.quote_service_entitlement_type in ("STR-OFFBGBPMCMKTGCPCND OBJ-AS","STR-OFFBGBSMKTGCPCND OBJ-AS","STR-OFFBGBKTGCPCND OBJ-GPAS"):
            condition_str = ' AND SAQTSE.SERVICE_ID = SAQTSV.SERVICE_ID '
        else:
            condition_str = ' AND SAQTSE.SERVICE_ID = SAQTSV.PAR_SERVICE_ID '
        summary_last_line_no = 0
        quote_item_summary_obj = Sql.GetFirst("SELECT TOP 1 LINE FROM SAQRIS (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' ORDER BY LINE DESC".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id))
        if quote_item_summary_obj:
            summary_last_line_no = int(quote_item_summary_obj.LINE)
        Sql.RunQuery("""INSERT SAQRIS (CONTRACT_VALID_FROM, CONTRACT_VALID_TO, DIVISION_ID, DIVISION_RECORD_ID, DOC_CURRENCY, DOCCURR_RECORD_ID, GLOBAL_CURRENCY, GLOBAL_CURRENCY_RECORD_ID, PLANT_ID, PLANT_RECORD_ID, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID,PAR_SERVICE_DESCRIPTION,PAR_SERVICE_ID,PAR_SERVICE_RECORD_ID, QUANTITY, QUOTE_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, BILLING_TYPE, LINE, QUOTE_REV_ITEM_SUMMARY_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified)
            SELECT IQ.*, ROW_NUMBER()OVER(ORDER BY(IQ.SERVICE_ID)) + {ItemSummaryLastLineNo} as LINE, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REV_ITEM_SUMMARY_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED,{UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
                SELECT DISTINCT
                    SAQTSV.CONTRACT_VALID_FROM,
                    SAQTSV.CONTRACT_VALID_TO,
                    SAQTRV.DIVISION_ID,
                    SAQTRV.DIVISION_RECORD_ID,
                    SAQTRV.DOC_CURRENCY,
                    SAQTRV.DOCCURR_RECORD_ID,
                    SAQTRV.GLOBAL_CURRENCY,
                    SAQTRV.GLOBAL_CURRENCY_RECORD_ID,
                    MAMSOP.PLANT_ID,
                    MAMSOP.PLANT_RECORD_ID,
                    SAQTSV.SERVICE_DESCRIPTION,
                    SAQTSV.SERVICE_ID,
                    SAQTSV.SERVICE_RECORD_ID,
                    SAQTSV.PAR_SERVICE_DESCRIPTION,
                    SAQTSV.PAR_SERVICE_ID,
                    SAQTSV.PAR_SERVICE_RECORD_ID,
                    1 as QUANTITY,
                    SAQTRV.QUOTE_ID,
                    SAQTRV.QUOTE_RECORD_ID,
                    SAQTMT.QTEREV_ID,
                    SAQTMT.QTEREV_RECORD_ID,
                    '{BillingType}' as BILLING_TYPE
                FROM SAQTSV (NOLOCK) 
                JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQTSV.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = SAQTSV.QTEREV_RECORD_ID  
                JOIN (
                SELECT DISTINCT SAQTSE.QUOTE_RECORD_ID,SAQTSE.QTEREV_RECORD_ID, SAQTSV.SERVICE_ID,SAQTSE.SALESORG_RECORD_ID FROM SAQTSE (NOLOCK) INNER JOIN SAQTSV ON SAQTSE.QUOTE_RECORD_ID = SAQTSV.QUOTE_RECORD_ID  AND SAQTSE.QTEREV_RECORD_ID = SAQTSV.QTEREV_RECORD_ID {condition_str}
                WHERE SAQTSE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQTSE.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND ISNULL(CONFIGURATION_STATUS, '') = 'COMPLETE' AND SAQTSV.SERVICE_ID ='{ServiceId}'
                ) AS IQ ON IQ.QUOTE_RECORD_ID = SAQTSV.QUOTE_RECORD_ID AND IQ.QTEREV_RECORD_ID = SAQTSV.QTEREV_RECORD_ID AND IQ.SERVICE_ID = SAQTSV.SERVICE_ID	AND IQ.SERVICE_ID = '{ServiceId}' 
                JOIN SAQTRV (NOLOCK) ON SAQTRV.SALESORG_RECORD_ID = SAQTSV.SALESORG_RECORD_ID AND SAQTRV.QTEREV_RECORD_ID = SAQTSV.QTEREV_RECORD_ID AND SAQTRV.QUOTE_RECORD_ID = SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID
                LEFT JOIN MAMSOP (NOLOCK) ON MAMSOP.SAP_PART_NUMBER = SAQTSV.SERVICE_ID AND MAMSOP.SALESORG_ID = SAQTRV.SALESORG_ID AND MAMSOP.DISTRIBUTIONCHANNEL_ID = SAQTRV.DISTRIBUTIONCHANNEL_ID
                LEFT JOIN SAQRIS (NOLOCK) ON SAQRIS.QUOTE_RECORD_ID = SAQTSV.QUOTE_RECORD_ID AND SAQRIS.QTEREV_RECORD_ID = SAQTSV.QTEREV_RECORD_ID AND SAQRIS.SERVICE_RECORD_ID = SAQTSV.SERVICE_RECORD_ID
                WHERE SAQTSV.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQTSV.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQTSV.SERVICE_ID = '{ServiceId}' AND ISNULL(SAQRIS.SERVICE_RECORD_ID,'') = '') IQ
        """.format(UserId=self.user_id, UserName=self.user_name, QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id, ItemSummaryLastLineNo=summary_last_line_no, condition_str = condition_str, BillingType = self.get_billing_type_val) 
        )
        #self.getting_cps_tax(self.service_id)
        if self.triggered_from != 'Split':
            ScriptExecutor.ExecuteGlobal('CQCPSTAXRE',{'service_id':self.service_id, 'Fun_type':'CPQ_TO_ECC'})
        return True
    def _quote_items_product_list_insert(self):
        #CR713 - A055S000P01-20911 - Start - M
        Sql.RunQuery("""INSERT SAQRIP (QUOTE_REVISION_ITEM_PRODUCT_LIST_RECORD_ID,CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified, PART_DESCRIPTION, PART_NUMBER, PART_RECORD_ID, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, QUANTITY, QUOTE_ID, QTEITM_RECORD_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, LINE, NEW_PART,GREENBOOK,GREENBOOK_RECORD_ID,FABLOCATION_ID, FABLOCATION_NAME,FABLOCATION_RECORD_ID  ) 
            SELECT 
                CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REVISION_ITEM_PRODUCT_LIST_RECORD_ID,
                '{UserName}' AS CPQTABLEENTRYADDEDBY,
                GETDATE() as CPQTABLEENTRYDATEADDED,
                {UserId} as CpqTableEntryModifiedBy,
                GETDATE() as CpqTableEntryDateModified,IQ.* FROM 
                (SELECT DISTINCT SAQSAP.KIT_NAME AS PART_DESCRIPTION,
                SAQSAP.KIT_NUMBER AS PART_NUMBER,
                SAQSAP.KIT_NUMBER_RECORD_ID AS PART_RECORD_ID,
                SAQRIO.SERVICE_DESCRIPTION,
                SAQRIO.SERVICE_ID,
                SAQRIO.SERVICE_RECORD_ID,
                NULL as QUANTITY,
                SAQRIO.QUOTE_ID,
                SAQRIO.QTEITM_RECORD_ID,
                SAQRIO.QUOTE_RECORD_ID,
                SAQRIO.QTEREV_ID,
                SAQRIO.QTEREV_RECORD_ID,
                SAQRIO.LINE,
                NULL AS NEW_PART,
                SAQRIO.GREENBOOK,
                SAQRIO.GREENBOOK_RECORD_ID,
                SAQRIO.FABLOCATION_ID,
                SAQRIO.FABLOCATION_NAME, 
                SAQRIO.FABLOCATION_RECORD_ID
                FROM SAQSAP (NOLOCK) 
                INNER JOIN SAQRIO (NOLOCK) ON SAQSAP.QUOTE_RECORD_ID = SAQRIO.QUOTE_RECORD_ID AND SAQSAP.QTEREV_RECORD_ID = SAQRIO.QTEREV_RECORD_ID AND SAQSAP.SERVICE_ID = SAQRIO.SERVICE_ID AND SAQSAP.EQUIPMENT_ID = SAQRIO.EQUIPMENT_ID 
                LEFT JOIN SAQRIP (NOLOCK) ON SAQRIP.QUOTE_RECORD_ID = SAQSAP.QUOTE_RECORD_ID AND SAQRIP.QTEREV_RECORD_ID = SAQSAP.QTEREV_RECORD_ID AND SAQRIP.SERVICE_ID = SAQSAP.SERVICE_ID AND SAQRIP.LINE = SAQRIO.LINE AND SAQRIP.PART_NUMBER = SAQSAP.KIT_NUMBER
                WHERE SAQSAP.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSAP.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQSAP.SERVICE_ID = '{ServiceId}' AND ISNULL(SAQSAP.KIT_NUMBER,'') != '' AND ISNULL(SAQRIP.PART_NUMBER,'') = '') IQ """.format(UserId=self.user_id, UserName=self.user_name, QuoteRecordId=self.contract_quote_record_id, RevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
        #CR713 - A055S000P01-20911 - End - M
    #A055S000P01-20843 - CR713 - Start - A
    def _update_kit_number_items(self):
        Sql.RunQuery("""UPDATE SAQRIT SET KIT_NUMBER = B.KIT_NUMBER FROM SAQRIT (NOLOCK) JOIN (SELECT SAQRIT.QUOTE_RECORD_ID,SAQRIT.QTEREV_RECORD_ID,SAQRIT.LINE , STUFF((SELECT DISTINCT ',' + SAQRIP.PART_NUMBER FROM SAQRIP(NOLOCK) WHERE SAQRIT.QUOTE_RECORD_ID = SAQRIP.QUOTE_RECORD_ID AND SAQRIT.QTEREV_RECORD_ID = SAQRIP.QTEREV_RECORD_ID AND SAQRIT.LINE = SAQRIP.LINE FOR XML PATH ('')) , 1, 1, '')AS KIT_NUMBER FROM SAQRIT (NOLOCK) WHERE SAQRIT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQRIT.SERVICE_ID = '{ServiceId}' GROUP BY QUOTE_RECORD_ID,QTEREV_RECORD_ID,LINE) B ON SAQRIT.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND SAQRIT.QTEREV_RECORD_ID = B.QTEREV_RECORD_ID AND SAQRIT.LINE = B.LINE WHERE ISNULL(B.KIT_NUMBER,'')<>'' AND SAQRIT.SERVICE_ID IN (SELECT SERVICE_ID FROM PRSPRV(NOLOCK) WHERE ISNULL(SSCM_COST,'FALSE')='TRUE') AND SAQRIT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SAQRIT.SERVICE_ID = '{ServiceId}'""".format(QuoteRecordId=self.contract_quote_record_id, QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
        return True
    #A055S000P01-20843 - CR713 - End - A 
    def _do_opertion(self):
        self._set_quote_service_entitlement_type()
        if self.action_type == "INSERT_LINE_ITEMS":
            if self.is_spare_service == True and self.service_id in ('Z0101','Z0100'):
                # Spare Parts Insert/Update
                self._quote_items_summary_insert()
                self._quote_items_insert()
                self._quote_items_object_insert()
                self._quote_annualized_items_insert()
                self._insert_quote_item_forecast_parts()
            elif self.is_fpm_spare_service == True:
                # Spare Parts Insert/Update (Z0108)...
                saqspt_have_qty = Sql.GetFirst("SELECT COUNT(*) AS CNT FROM SAQSPT (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND CUSTOMER_ANNUAL_QUANTITY IS NOT NULL AND (PAR_PART_NUMBER IS NULL OR PAR_PART_NUMBER ='') AND QTEREV_RECORD_ID = '{RevisionRecordId}'".format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.contract_quote_revision_record_id))
                if saqspt_have_qty.CNT>0:
                    self._quote_items_summary_insert()
                    self._simple_fpm_quote_items_insert()
                    self._insert_quote_item_fpm_forecast_parts()
                    #self._insert_item_level_delivery_schedule()
                    self._simple_fpm_quote_annualized_items_insert()
                    self._quote_items_fpm_entitlement_insert()
            elif self.is_simple_service == True:
                self._simple_quote_items_summary_insert()
                self._simple_quote_items_insert()
                self._simple_items_object_insert()
                self._simple_quote_annualized_items_insert()
            else:
                if self.quote_service_entitlement_type in ("STR-OFFBGBPMCMKTGCPCND OBJ-AS","STR-OFFBGBSMKTGCPCND OBJ-AS",'STR-OFFBGBKTGCPCND OBJ-GPAS'):
                    self._simple_quote_items_summary_insert()
                else:
                    self._quote_items_summary_insert()
                self._quote_items_insert()
                self._quote_items_object_insert()
                self._quote_annualized_items_insert()
                if self.quote_service_entitlement_type in ('STR-OFFBGBPMCMKTGCPCND OBJ-AS','STR-OFFBGBSMKTGCPCND OBJ-AS','STR-OFFBGBKTGCPCND OBJ-GPAS'):
                    self._insert_quote_item_forecast_parts()
                #self._quote_item_line_entitlement_insert()
                self._quote_items_assembly_insert()
                #self._quote_items_assembly_entitlement_insert()
            if self.quote_service_entitlement_type not in ('STR-OFFBGBPMCMKTGCPCND OBJ-AS','STR-OFFBGBSMKTGCPCND OBJ-AS','STR-OFFBGBKTGCPCND OBJ-GPAS') and self.service_id not in ('Z0101','Z0100') :
                #Trace.Write("inside--"+str(self.quote_service_entitlement_type))
                self._quote_items_product_list_insert()
            #A055S000P01-20843 - CR713 - Start - A
            self._update_kit_number_items()
            #A055S000P01-20843 - CR713 - End - A
        if self.service_id in ('Z0117','Z0046','Z0116','Z0123'):
            Log.Info("===> QIFWUDQTM called from CQINS")
            CallingCQIFWUDQTM = ScriptExecutor.ExecuteGlobal("CQIFWUDQTM",{"QT_REC_ID":self.contract_quote_id,"Operation":"ANCILLARY_PRICING",'ANC_SERVICE_ID':"('"+str(self.service_id)+"')"})
        # Pricing Calculation - Start
        # quote_line_item_obj = Sql.GetFirst("SELECT LINE FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}' AND ISNULL(STATUS,'') = ''".format(QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.service_id))
        # #added condition to restrict email trigger thrice
        # if quote_line_item_obj and self.action_type == "UPDATE_LINE_ITEMS":
        # 	Log.Info("====> QTPOSTACRM called from ==> "+str(self.contract_quote_id)+'--'+str(self.service_id))
        # 	ScriptExecutor.ExecuteGlobal('QTPOSTACRM',{'QUOTE_ID':self.contract_quote_id,'REVISION_ID':self.contract_quote_revision_id, 'Fun_type':'cpq_to_sscm'})
        # 	SqlHelper.GetFirst("sp_executesql @T=N'update A SET A.STATUS = (CASE WHEN A.STATUS =''ERROR'' THEN ''ERROR'' WHEN A.STATUS =''PARTIALLY PRICED'' THEN ''ERROR'' END) from SAQRIT A inner join ( select SERVICE_ID,LINE,SAQICO.QUOTE_ID from SAQICO WHERE SAQICO.QUOTE_ID = ''"+str(self.contract_quote_id)+"'' group by SERVICE_ID,LINE,SAQICO.QUOTE_ID Having count(*) > 1 ) as od on od.LINE = A.LINE AND od.SERVICE_ID = A.SERVICE_ID '")
        # 	SqlHelper.GetFirst("sp_executesql @T=N'update A SET A.STATUS = (CASE WHEN A.STATUS =''ACQUIRING'' THEN ''ACQUIRING'' WHEN A.STATUS =''ERROR'' THEN ''ERROR'' END) from SAQRIT A inner join ( select SERVICE_ID,LINE,SAQICO.QUOTE_ID from SAQICO WHERE SAQICO.QUOTE_ID = ''"+str(self.contract_quote_id)+"'' group by SERVICE_ID,LINE,SAQICO.QUOTE_ID Having count(*) > 1 ) as od on od.LINE = A.LINE AND od.SERVICE_ID = A.SERVICE_ID '")
        # 	SqlHelper.GetFirst("sp_executesql @T=N'update A SET A.STATUS = (CASE WHEN A.STATUS =''ACQUIRING'' THEN ''PARTIALLY PRICING'' WHEN A.STATUS =''PARTIALLY PRICING'' THEN ''PARTIALLY PRICING'' END) from SAQRIT A inner join ( select SERVICE_ID,LINE,SAQICO.QUOTE_ID from SAQICO WHERE SAQICO.QUOTE_ID = ''"+str(self.contract_quote_id)+"'' group by SERVICE_ID,LINE,SAQICO.QUOTE_ID Having count(*) > 1 ) as od on od.LINE = A.LINE AND od.SERVICE_ID = A.SERVICE_ID '")
        # Pricing Calculation - End
        return True
try:
    where_condition_string = Param.WhereString
except:
    where_condition_string = ''
action_type = Param.ActionType
try:
    entitlement_level_obj = Param.EntitlementLevel
except:
    entitlement_level_obj = "SAQTSE"
try:
    triggered_from = Param.TriggeredFrom
except Exception:
    triggered_from = ''
try:
    parent_service_id = Param.ParentServiceId
except Exception:
    parent_service_id = ''
parameters = {}
keysofparameters = {
    "QUOTE_RECORD_ID" : "contract_quote_record_id",
    "QTEREV_RECORD_ID" : "contract_quote_revision_record_id",
    "SERVICE_ID" : "service_id",
    "GREENBOOK" : "greenbook_id",
    "FABLOCATION_ID" : "fablocation_id",
    "EQUIPMENT_ID" : "equipment_id",
}
parameters['action_type']=str(action_type)
parameters['triggered_from']=str(triggered_from)
parameters['entitlement_level_obj'] = str(entitlement_level_obj)
parameters['parent_service_id'] = str(parent_service_id)
if where_condition_string:
    parameters['where_condition_string'] = str(where_condition_string)
if action_type == "UPDATE_LINE_ITEMS":
    for key in keysofparameters.keys():
        if str(key) in where_condition_string:
            pattern = re.compile(r''+str(key)+'\s*\=\s*\'([^>]*?)\'')
            result = re.search(pattern, where_condition_string).group(1)
            parameters[keysofparameters[key]]=str(result)
else:
    parameters[keysofparameters['QUOTE_RECORD_ID']]=str(Param.ContractQuoteRecordId)
    parameters[keysofparameters['QTEREV_RECORD_ID']]=str(Param.ContractQuoteRevisionRecordId)
    parameters[keysofparameters['SERVICE_ID']]=str(Param.ServiceId)
contract_quote_item_obj = ContractQuoteItem(**parameters)
contract_quote_item_obj._do_opertion()
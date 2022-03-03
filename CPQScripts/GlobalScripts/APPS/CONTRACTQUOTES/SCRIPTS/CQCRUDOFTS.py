# =========================================================================================================================================
#   __script_name : CQCRUDOFTS.PY
#   __script_description : THIS SCRIPT IS USED TO INSERT TABLES RELATED TO FTS SCENARIOS.
#   __primary_author__ : GAYATHRI AMARESAN
#   __create_date :24-04-2022
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================



import datetime

import sys
import re
import SYCNGEGUID as CPQID
from SYDATABASE import SQL

Sql = SQL()
ScriptExecutor = ScriptExecutor


try:
    contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
except:
    contract_quote_record_id = ''	
try:
    quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
except:
    quote_revision_record_id = ''

contract_quote_record_obj = Sql.GetFirst("SELECT * FROM SAQTRV(NOLOCK) WHERE QUOTE_RECORD_ID = '{}'".format(contract_quote_record_id))
if contract_quote_record_obj:
    contract_quote_id = contract_quote_record_obj.QUOTE_ID
    #contract_quote_name = contract_quote_record_obj.QUOTE_NAME
    #quote_type = contract_quote_record_obj.QUOTE_TYPE
    quote_revision_id = contract_quote_record_obj.QTEREV_ID
    quote_revision_record_id = contract_quote_record_obj.QTEREV_RECORD_ID
    salesorg_id = contract_quote_record_obj.SALESORG_ID
    salesorg_name = contract_quote_record_obj.SALESORG_NAME
    salesorg_record_id = contract_quote_record_obj.SALESORG_RECORD_ID
    #account_id = contract_quote_record_obj.ACCOUNT_ID
    #account_name = contract_quote_record_obj.ACCOUNT_NAME
    #account_record_id = contract_quote_record_obj.ACCOUNT_RECORD_ID
    contract_start_date = contract_quote_record_obj.CONTRACT_VALID_FROM
    contract_end_date = contract_quote_record_obj.CONTRACT_VALID_TO
    #contract_currency = contract_quote_record_obj.QUOTE_CURRENCY
    #contract_currency_record_id = contract_quote_record_obj.QUOTE_CURRENCY_RECORD_ID
    #c4c_quote_id = contract_quote_record_obj.C4C_QUOTE_ID
    #source_contract_id = contract_quote_record_obj.SOURCE_CONTRACT_ID
else:
    contract_quote_id = None
    #contract_quote_name = None
    salesorg_id = None
    salesorg_name = None
    salesorg_record_id = None
    #account_id = None
    #account_record_id = None
    #account_name = None
    contract_start_date = None
    contract_end_date = None
    #contract_currency = None
    #contract_currency_record_id = None
    #c4c_quote_id = None
    #source_contract_id = None
def get_res(self, query_string, table_total_rows):
    for offset_skip_count in range(0, table_total_rows+1, 1000):
        pagination_condition = "WHERE SNO>={Skip_Count} AND SNO<={Fetch_Count}".format(Skip_Count=offset_skip_count+1, Fetch_Count=offset_skip_count+1000)
        query_string_with_pagination = 'SELECT * FROM (SELECT *, ROW_NUMBER()OVER(ORDER BY EQUIPMENT_RECORD_ID) AS SNO FROM ({Query_String}) IQ)OQ {Pagination_Condition}'.format(
                                        Query_String=query_string, Pagination_Condition=pagination_condition)
        table_data = Sql.GetList(query_string_with_pagination)
        if table_data is not None:
            for row_data in table_data:
                yield row_data.EQUIPMENT_RECORD_ID


def sending_fablocation_insert(values,all_values,A_Keys,A_Values):
    master_object_name = "MAFBLC"
    if values:
        record_ids = []
        if all_values:
            query_string = "SELECT FAB_LOCATION_RECORD_ID FROM MAFBLC (NOLOCK) WHERE ACCOUNT_RECORD_ID = '{acc}' AND ISNULL(SERIAL_NO, '') <> '' AND ISNULL(GREENBOOK, '') <> '' AND  FAB_LOCATION_ID NOT IN  (SELECT SNDFBL_ID FROM SAQSAF (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' )".format(
                    acc=Product.GetGlobal("stp_account_id"),
                    salesorgrecid=salesorg_record_id,
                    QuoteRecordId=contract_quote_record_id,
                    RevisionRecordId=quote_revision_record_id
                )			
            query_string_for_count = "SELECT COUNT(*) as count FROM ({Query_String})OQ".format(
                Query_String=query_string
            )
            table_count_data = Sql.GetFirst(query_string_for_count)
            if table_count_data is not None:
                table_total_rows = table_count_data.count
            if table_total_rows:
                record_ids = [data for data in get_res(query_string, table_total_rows)]
        else:                    
            record_ids = [
                CPQID.KeyCPQId.GetKEYId(master_object_name, str(value))
                if value.strip() != "" and master_object_name in value
                else value
                for value in values
            ]
        batch_group_record_id = str(Guid.NewGuid()).upper()
        record_ids = str(str(record_ids)[1:-1].replace("'",""))
        parameter = Sql.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'SELECT' ")		
        primaryQueryItems = Sql.GetFirst(""+str(parameter.QUERY_CRITERIA_1)+" SYSPBT(BATCH_RECORD_ID, BATCH_STATUS, QUOTE_ID, QUOTE_RECORD_ID, BATCH_GROUP_RECORD_ID,QTEREV_RECORD_ID) SELECT MAFBLC.FAB_LOCATION_RECORD_ID as BATCH_RECORD_ID, ''IN PROGRESS'' as BATCH_STATUS, ''"+str(contract_quote_id)+"'' as QUOTE_ID, ''"+str(contract_quote_record_id)+"'' as QUOTE_RECORD_ID, ''"+str(batch_group_record_id)+"'' as BATCH_GROUP_RECORD_ID,''"+str(quote_revision_record_id)+"'' as QTEREV_RECORD_ID FROM MAFBLC (NOLOCK) JOIN splitstring(''"+record_ids+"'') ON ltrim(rtrim(NAME)) = MAFBLC.FAB_LOCATION_RECORD_ID'")
        
        Sql.RunQuery("""INSERT SAQSAF(SNDFBL_ID,
            SNDFBL_NAME,
            SNDFBL_RECORD_ID,
            SNDACC_ID,
            SNDACC_NAME,
            SNDACC_RECORD_ID,
            QUOTE_ID,
            QUOTE_RECORD_ID,
            --QTEREV_ID,
            QTEREV_RECORD_ID,
            COUNTRY, 
            COUNTRY_RECORD_ID, 
            MNT_PLANT_ID, 
            MNT_PLANT_NAME,
            MNT_PLANT_RECORD_ID,
            SNDFBL_STATUS, 
            ADDRESS_1, 
            ADDRESS_2, 
            CITY, 
            STATE,
            STATE_RECORD_ID,
            QUOTE_REV_SENDING_ACC_FAB_LOCATION_RECORD_ID,
            CPQTABLEENTRYADDEDBY,
            CPQTABLEENTRYDATEADDED, 
            CpqTableEntryModifiedBy,
            CpqTableEntryDateModified) 
            SELECT fab_location.*,CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REV_SENDING_ACC_FAB_LOCATION_RECORD_ID,'{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED,'{UserId}' as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM 
                (SELECT DISTINCT MAFBLC.FAB_LOCATION_ID,
                MAFBLC.FAB_LOCATION_NAME,
                MAFBLC.FAB_LOCATION_RECORD_ID,
                MAFBLC.ACCOUNT_ID,
                MAFBLC.ACCOUNT_NAME,
                MAFBLC.ACCOUNT_RECORD_ID,
                '{QuoteId}' as QUOTE_ID,
                '{QuoteRecId}' as QUOTE_RECORD_ID,
                --'{RevisionId}' as QTEREV_ID,
                '{RevisionRecordId}' as QTEREV_RECORD_ID,
                MAFBLC.COUNTRY,
                MAFBLC.COUNTRY_RECORD_ID,
                MAFBLC.MNT_PLANT_ID,
                MAFBLC.MNT_PLANT_NAME,
                MAFBLC.MNT_PLANT_RECORD_ID,
                MAFBLC.STATUS AS FABLOCATION_STATUS,
                MAFBLC.ADDRESS_1,
                MAFBLC.ADDRESS_2,
                MAFBLC.CITY,
                MAFBLC.STATE,
                MAFBLC.STATE_RECORD_ID
                FROM SYSPBT(NOLOCK)
                JOIN MAFBLC(NOLOCK) ON MAFBLC.FAB_LOCATION_RECORD_ID = SYSPBT.BATCH_RECORD_ID 
            WHERE QUOTE_RECORD_ID = '{QuoteRecId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}' )fab_location """.format(
            UserName=User.UserName,
            UserId=User.Id,
            QuoteId =contract_quote_id ,
            QuoteRecId=contract_quote_record_id,
            RevisionId=quote_revision_id,
            RevisionRecordId=quote_revision_record_id,
            BatchGroupRecordId = batch_group_record_id))
        
        
        Sql.RunQuery("""DELETE FROM SYSPBT WHERE SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}' and SYSPBT.QTEREV_RECORD_ID = '{RevisionRecordId}' and SYSPBT.BATCH_STATUS = 'IN PROGRESS'""".format(
                                    BatchGroupRecordId=batch_group_record_id,RevisionRecordId=quote_revision_record_id
                                )
                            )
        
        


def sending_equipment_insert(values,all_values,A_Keys,A_Values):
    master_object_name = "MAEQUP"
    if values:
        record_ids = []
        if all_values:
            query_string = "SELECT EQUIPMENT_RECORD_ID FROM MAEQUP (NOLOCK) WHERE ACCOUNT_RECORD_ID = '{acc}' AND FABLOCATION_ID = '{fab}' AND ISNULL(SERIAL_NO, '') <> '' AND ISNULL(GREENBOOK, '') <> '' AND  EQUIPMENT_RECORD_ID NOT IN  (SELECT EQUIPMENT_RECORD_ID FROM SAQFEQ (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND FABLOCATION_ID = '{fab}' )".format(
                    acc=Product.GetGlobal("stp_account_id"),
                    fab=Product.GetGlobal("sending_fab_id"),
                    salesorgrecid=salesorg_record_id,
                    QuoteRecordId=contract_quote_record_id,
                    RevisionRecordId=quote_revision_record_id
                )			
            query_string_for_count = "SELECT COUNT(*) as count FROM ({Query_String})OQ".format(
                Query_String=query_string
            )
            table_count_data = Sql.GetFirst(query_string_for_count)
            if table_count_data is not None:
                table_total_rows = table_count_data.count
            if table_total_rows:
                record_ids = [data for data in get_res(query_string, table_total_rows)]
        else:                    
            record_ids = [
                CPQID.KeyCPQId.GetKEYId(master_object_name, str(value))
                if value.strip() != "" and master_object_name in value
                else value
                for value in values
            ]
            
        ##To Fetch fab location details...
        get_fab_details = Sql.GetFirst("SELECT FABLOCATION_RECORD_ID,FABLOCATION_ID,FABLOCATION_NAME from MAEQUP WHERE FABLOCATION_ID = '{}'".format(Product.GetGlobal("sending_fab_id")))    
        batch_group_record_id = str(Guid.NewGuid()).upper()
        record_ids = str(str(record_ids)[1:-1].replace("'",""))
        parameter = Sql.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'SELECT' ")		
        primaryQueryItems = Sql.GetFirst(""+str(parameter.QUERY_CRITERIA_1)+" SYSPBT(BATCH_RECORD_ID, BATCH_STATUS, QUOTE_ID, QUOTE_RECORD_ID, BATCH_GROUP_RECORD_ID,QTEREV_RECORD_ID) SELECT MAEQUP.EQUIPMENT_RECORD_ID as BATCH_RECORD_ID, ''IN PROGRESS'' as BATCH_STATUS, ''"+str(contract_quote_id)+"'' as QUOTE_ID, ''"+str(contract_quote_record_id)+"'' as QUOTE_RECORD_ID, ''"+str(batch_group_record_id)+"'' as BATCH_GROUP_RECORD_ID,''"+str(quote_revision_record_id)+"'' as QTEREV_RECORD_ID FROM MAEQUP (NOLOCK) JOIN splitstring(''"+record_ids+"'') ON ltrim(rtrim(NAME)) = MAEQUP.EQUIPMENT_RECORD_ID'")
        Sql.RunQuery("""
                                INSERT SAQASE (
                                    QUOTE_REV_SENDING_ACC_FAB_EQUIPMENT_RECORD_ID,
                                    SND_EQUIPMENT_ID,
                                    SND_EQUIPMENT_RECORD_ID,
                                    SND_EQUIPMENT_DESCRIPTION,                            
                                    SNDFBL_ID,
                                    SNDFBL_NAME,
                                    SNDFBL_RECORD_ID,
                                    SNDACC_ID,
                                    SNDACC_NAME,
                                    SNDACC_RECORD_ID,
                                    QUOTE_RECORD_ID,
                                    QUOTE_ID,
                                    QTEREV_ID,
                                    QTEREV_RECORD_ID,
                                    KPU,
                                    PLATFORM,
                                    EQUIPMENTCATEGORY_RECORD_ID,
                                    EQUIPMENTCATEGORY_ID,
                                    EQUIPMENTCATEGORY_DESCRIPTION,
                                    EQUIPMENT_STATUS,
                                    GREENBOOK,
                                    GREENBOOK_RECORD_ID,
                                    MNT_PLANT_RECORD_ID,
                                    MNT_PLANT_ID,
                                    MNT_PLANT_NAME,
                                    CPQTABLEENTRYDATEADDED,
                                    CpqTableEntryModifiedBy,
                                    CpqTableEntryDateModified,
                                    WAFER_SIZE,
                                    TECHNOLOGY
                                    ) SELECT
                                        CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REV_SENDING_ACC_FAB_EQUIPMENT_RECORD_ID,
                                        MAEQUP.EQUIPMENT_ID,
                                        MAEQUP.EQUIPMENT_RECORD_ID,
                                        MAEQUP.EQUIPMENT_DESCRIPTION,  
                                        {fab_id} as SNDFBL_ID,
                                        '{fab_name}' as SNDFBL_NAME,
                                        '{fab_recid}' as SNDFBL_RECORD_ID,
                                        MAEQUP.ACCOUNT_ID,
                                        MAEQUP.ACCOUNT_NAME,
                                        MAEQUP.ACCOUNT_RECORD_ID,
                                        '{QuoteRecId}' as QUOTE_RECORD_ID,
                                        '{QuoteId}' as QUOTE_ID,
                                        '{RevisionId}' as QTEREV_ID,
                                        '{RevisionRecordId}' as QTEREV_RECORD_ID,
                                        MAEQUP.KPU,
                                        MAEQUP.PLATFORM,
                                        MAEQUP.EQUIPMENTCATEGORY_RECORD_ID,
                                        MAEQUP.EQUIPMENTCATEGORY_ID,
                                        MAEQCT.EQUIPMENTCATEGORY_DESCRIPTION,
                                        MAEQUP.EQUIPMENT_STATUS,
                                        MAEQUP.GREENBOOK,
                                        MAEQUP.GREENBOOK_RECORD_ID,
                                        MAEQUP.MNT_PLANT_RECORD_ID,
                                        MAEQUP.MNT_PLANT_ID,
                                        MAEQUP.MNT_PLANT_NAME,
                                        GETDATE() as CPQTABLEENTRYDATEADDED,
                                        {UserId} as CpqTableEntryModifiedBy,
                                        GETDATE() as CpqTableEntryDateModified,
                                        MAEQUP.SUBSTRATE_SIZE,
                                        MAEQUP.TECHNOLOGY
                                        FROM MAEQUP (NOLOCK)
                                        JOIN SYSPBT (NOLOCK) ON SYSPBT.BATCH_RECORD_ID = MAEQUP.EQUIPMENT_RECORD_ID JOIN MAEQCT(NOLOCK)
                                        ON MAEQUP.EQUIPMENTCATEGORY_ID = MAEQCT.EQUIPMENTCATEGORY_ID
                                        WHERE 
                                        SYSPBT.QUOTE_RECORD_ID = '{QuoteRecId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'
                                        AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}'                        
                                """.format(
                                fab_id=Product.GetGlobal("sending_fab_id"),
                                fab_name= get_fab_details.FABLOCATION_NAME,
                                fab_recid = get_fab_details.FABLOCATION_RECORD_ID,
                                UserName=User.UserName,
                                UserId=User.Id,
                                QuoteId=contract_quote_id,
                                QuoteRecId=contract_quote_record_id,
                                RevisionId=quote_revision_id,
                                RevisionRecordId=quote_revision_record_id,
                                BatchGroupRecordId=batch_group_record_id
                            )
                        )
        # Sql.RunQuery("""DELETE FROM SYSPBT WHERE SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}' and SYSPBT.QTEREV_RECORD_ID = '{RevisionRecordId}' and SYSPBT.BATCH_STATUS = 'IN PROGRESS'""".format(BatchGroupRecordId=batch_group_record_id,RevisionRecordId=quote_revision_record_id))


def receiving_fablocation_insert(values,all_values,A_Keys,A_Values):
    master_object_name = "SAQSAF"
    if values:
        record_ids = []
        if all_values:
            query_string = "SELECT QUOTE_REV_SENDING_ACC_FAB_LOCATION_RECORD_ID FROM SAQSAF (NOLOCK) WHERE SNDACC_ID = '{acc}' AND  FAB_LOCATION_ID NOT IN  (SELECT FABLOCATION_ID FROM SAQFBL (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' )".format(
                    acc=Product.GetGlobal("stp_account_id"),
                    salesorgrecid=salesorg_record_id,
                    QuoteRecordId=contract_quote_record_id,
                    RevisionRecordId=quote_revision_record_id
                )			
            query_string_for_count = "SELECT COUNT(*) as count FROM ({Query_String})OQ".format(
                Query_String=query_string
            )
            table_count_data = Sql.GetFirst(query_string_for_count)
            if table_count_data is not None:
                table_total_rows = table_count_data.count
            if table_total_rows:
                record_ids = [data for data in get_res(query_string, table_total_rows)]
        else:                    
            record_ids = [
                CPQID.KeyCPQId.GetKEYId(master_object_name, str(value))
                if value.strip() != "" and master_object_name in value
                else value
                for value in values
            ]
        batch_group_record_id = str(Guid.NewGuid()).upper()
        record_ids = str(str(record_ids)[1:-1].replace("'",""))
        parameter = Sql.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'SELECT' ")		
        primaryQueryItems = Sql.GetFirst(""+str(parameter.QUERY_CRITERIA_1)+" SYSPBT(BATCH_RECORD_ID, BATCH_STATUS, QUOTE_ID, QUOTE_RECORD_ID, BATCH_GROUP_RECORD_ID,QTEREV_RECORD_ID) SELECT SAQSAF.QUOTE_REV_SENDING_ACC_FAB_LOCATION_RECORD_ID as BATCH_RECORD_ID, ''IN PROGRESS'' as BATCH_STATUS, ''"+str(contract_quote_id)+"'' as QUOTE_ID, ''"+str(contract_quote_record_id)+"'' as QUOTE_RECORD_ID, ''"+str(batch_group_record_id)+"'' as BATCH_GROUP_RECORD_ID,''"+str(quote_revision_record_id)+"'' as QTEREV_RECORD_ID FROM SAQSAF (NOLOCK) JOIN splitstring(''"+record_ids+"'') ON ltrim(rtrim(NAME)) = SAQSAF.QUOTE_REV_SENDING_ACC_FAB_LOCATION_RECORD_ID'")
        
        Sql.RunQuery(""" INSERT SAQFBL (FABLOCATION_ID,
                FABLOCATION_NAME,
                FABLOCATION_RECORD_ID,
                ACCOUNT_ID,
                ACCOUNT_NAME,
                ACCOUNT_RECORD_ID,
                QUOTE_ID,
                QUOTE_RECORD_ID,
                QTEREV_ID,
                QTEREV_RECORD_ID,
                COUNTRY, 
                COUNTRY_RECORD_ID, 
                MNT_PLANT_ID, 
                MNT_PLANT_NAME,
                MNT_PLANT_RECORD_ID,
                FABLOCATION_STATUS, 
                ADDRESS_1, 
                ADDRESS_2, 
                CITY, 
                STATE,
                STATE_RECORD_ID,
                QUOTE_FABLOCATION_RECORD_ID,
                CPQTABLEENTRYADDEDBY,
                CPQTABLEENTRYDATEADDED, 
                CpqTableEntryModifiedBy,
                CpqTableEntryDateModified) 
                SELECT fab_location.*,CONVERT(VARCHAR(4000),NEWID()) as QUOTE_FABLOCATION_RECORD_ID,'{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED,'{UserId}' as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM 
                    (SELECT DISTINCT 
                    SAQSAF.SNDFBL_ID,
                    SAQSAF.SNDFBL_NAME,
                    SAQSAF.SNDFBL_RECORD_ID,
                    SAQSAF.SNDACC_ID,
                    SAQSAF.SNDACC_NAME,
                    SAQSAF.SNDACC_RECORD_ID,
                    '{QuoteId}' as QUOTE_ID,
                    '{QuoteRecId}' as QUOTE_RECORD_ID,
                    '{RevisionId}' as QTEREV_ID,
                    '{RevisionRecordId}' as QTEREV_RECORD_ID,
                    SAQSAF.COUNTRY,
                    SAQSAF.COUNTRY_RECORD_ID,
                    SAQSAF.MNT_PLANT_ID,
                    SAQSAF.MNT_PLANT_NAME,
                    SAQSAF.MNT_PLANT_RECORD_ID,
                    SAQSAF.SNDFBL_STATUS AS FABLOCATION_STATUS,
                    SAQSAF.ADDRESS_1,
                    SAQSAF.ADDRESS_2,
                    SAQSAF.CITY,
                    SAQSAF.STATE,
                    SAQSAF.STATE_RECORD_ID
                    FROM SYSPBT(NOLOCK)
                    JOIN SAQSAF(NOLOCK) ON SAQSAF.QUOTE_REV_SENDING_ACC_FAB_LOCATION_RECORD_ID = SYSPBT.BATCH_RECORD_ID 
                WHERE SYSPBT.QUOTE_RECORD_ID = '{QuoteRecId}' AND SYSPBT.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}')fab_location """.format(
                UserName=User.UserName,
                UserId=User.Id,
                QuoteId =contract_quote_id ,
                QuoteRecId=contract_quote_record_id,
                RevisionId=quote_revision_id,
                RevisionRecordId=quote_revision_record_id,
                BatchGroupRecordId=batch_group_record_id))
                    
        
        # Sql.RunQuery("""DELETE FROM SYSPBT WHERE SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}' and SYSPBT.QTEREV_RECORD_ID = '{RevisionRecordId}' and SYSPBT.BATCH_STATUS = 'IN PROGRESS'""".format(
        #                             BatchGroupRecordId=batch_group_record_id,RevisionRecordId=quote_revision_record_id
        #                         )
        #                     )


def receiving_equipment_insert(values,all_values,A_Keys,A_Values):
    master_object_name = "SAQASE"
    if values:
        record_ids = []
        if all_values:
            query_string = "SELECT SND_EQUIPMENT_RECORD_ID FROM SAQASE (NOLOCK) WHERE ACCOUNT_RECORD_ID = '{acc}' AND FABLOCATION_ID = '{fab}' AND ISNULL(SERIAL_NO, '') <> '' AND ISNULL(GREENBOOK, '') <> '' AND  SND_EQUIPMENT_RECORD_ID NOT IN  (SELECT SND_EQUIPMENT_RECORD_ID FROM SAQFEQ (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND FABLOCATION_ID = '{fab}' )".format(
                    acc=Product.GetGlobal("stp_account_id"),
                    fab=Product.GetGlobal("receiving_fab_id"),
                    salesorgrecid=salesorg_record_id,
                    QuoteRecordId=contract_quote_record_id,
                    RevisionRecordId=quote_revision_record_id
                )			
            query_string_for_count = "SELECT COUNT(*) as count FROM ({Query_String})OQ".format(
                Query_String=query_string
            )
            table_count_data = Sql.GetFirst(query_string_for_count)
            if table_count_data is not None:
                table_total_rows = table_count_data.count
            if table_total_rows:
                record_ids = [data for data in get_res(query_string, table_total_rows)]
        else:                    
            record_ids = [
                CPQID.KeyCPQId.GetKEYId(master_object_name, str(value))
                if value.strip() != "" and master_object_name in value
                else value
                for value in values
            ]
        batch_group_record_id = str(Guid.NewGuid()).upper()
        record_ids = str(str(record_ids)[1:-1].replace("'",""))
        parameter = Sql.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'SELECT' ")		
        primaryQueryItems = Sql.GetFirst(""+str(parameter.QUERY_CRITERIA_1)+" SYSPBT(BATCH_RECORD_ID, BATCH_STATUS, QUOTE_ID, QUOTE_RECORD_ID, BATCH_GROUP_RECORD_ID,QTEREV_RECORD_ID) SELECT SAQASE.SND_EQUIPMENT_RECORD_ID as BATCH_RECORD_ID, ''IN PROGRESS'' as BATCH_STATUS, ''"+str(contract_quote_id)+"'' as QUOTE_ID, ''"+str(contract_quote_record_id)+"'' as QUOTE_RECORD_ID, ''"+str(batch_group_record_id)+"'' as BATCH_GROUP_RECORD_ID,''"+str(quote_revision_record_id)+"'' as QTEREV_RECORD_ID FROM SAQASE (NOLOCK) JOIN splitstring(''"+record_ids+"'') ON ltrim(rtrim(NAME)) = SAQASE.SND_EQUIPMENT_RECORD_ID'")
        
        Sql.RunQuery(
                            """
                                INSERT SAQFEQ (
                                    QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID,
                                    EQUIPMENT_ID,
                                    EQUIPMENT_RECORD_ID,
                                    EQUIPMENT_DESCRIPTION,                            
                                    FABLOCATION_ID,
                                    FABLOCATION_NAME,
                                    FABLOCATION_RECORD_ID,
                                    #SERIAL_NUMBER,
                                    QUOTE_RECORD_ID,
                                    QUOTE_ID,
                                    QUOTE_NAME,
                                    QTEREV_ID,
                                    QTEREV_RECORD_ID,
                                    KPU,
                                    PLATFORM,
                                    EQUIPMENTCATEGORY_RECORD_ID,
                                    EQUIPMENTCATEGORY_ID,
                                    EQUIPMENTCATEGORY_DESCRIPTION,
                                    EQUIPMENT_STATUS,
                                    #PBG,
                                    GREENBOOK,
                                    GREENBOOK_RECORD_ID,
                                    MNT_PLANT_RECORD_ID,
                                    MNT_PLANT_ID,
                                    MNT_PLANT_NAME,
                                    # WARRANTY_START_DATE,
                                    # WARRANTY_END_DATE,
                                    SALESORG_ID,
                                    SALESORG_NAME,
                                    SALESORG_RECORD_ID,
                                    #CUSTOMER_TOOL_ID,
                                    CPQTABLEENTRYADDEDBY,
                                    CPQTABLEENTRYDATEADDED,
                                    CpqTableEntryModifiedBy,
                                    CpqTableEntryDateModified,
                                    RELOCATION_FAB_TYPE,
                                    RELOCATION_EQUIPMENT_TYPE,WAFER_SIZE,
                                    TECHNOLOGY
                                    ) SELECT
                                        CONVERT(VARCHAR(4000),NEWID()) as QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID,
                                        SAQASE.SND_EQUIPMENT_ID,
                                        SAQASE.SND_EQUIPMENT_RECORD_ID,
                                        SAQASE.SND_EQUIPMENT_DESCRIPTION,  
                                        SAQASE.SNDFBL_ID,
                                        SAQASE.SNDFBL_NAME,
                                        SAQASE.SNDFBL_RECORD_ID,                    
                                        #SAQASE.SERIAL_NO,
                                        '{QuoteRecId}' as QUOTE_RECORD_ID,
                                        '{QuoteId}' as QUOTE_ID,
                                        ' ' as QUOTE_NAME,
                                        '{RevisionId}' as QTEREV_ID,
                                        '{RevisionRecordId}' as QTEREV_RECORD_ID,
                                        SAQASE.KPU,
                                        SAQASE.PLATFORM,
                                        SAQASE.EQUIPMENTCATEGORY_RECORD_ID,
                                        SAQASE.EQUIPMENTCATEGORY_ID,
                                        MAEQCT.EQUIPMENTCATEGORY_DESCRIPTION,
                                        SAQASE.EQUIPMENT_STATUS,
                                        #SAQASE.PBG,
                                        SAQASE.GREENBOOK,
                                        SAQASE.GREENBOOK_RECORD_ID,
                                        SAQASE.MNT_PLANT_RECORD_ID,
                                        SAQASE.MNT_PLANT_ID,
                                        SAQASE.MNT_PLANT_NAME,
                                        # SAQASE.WARRANTY_START_DATE,
                                        # SAQASE.WARRANTY_END_DATE,
                                        '' as SALESORG_ID,
                                        '' as SALESORG_NAME,
                                        '' as SALESORG_RECORD_ID,
                                        #SAQASE.CUSTOMER_TOOL_ID,
                                        '{UserName}' AS CPQTABLEENTRYADDEDBY,
                                        GETDATE() as CPQTABLEENTRYDATEADDED,
                                        {UserId} as CpqTableEntryModifiedBy,
                                        GETDATE() as CpqTableEntryDateModified,
                                        '{relocation_fab_type}' AS RELOCATION_FAB_TYPE,
                                        '{relocation_equp_type}' AS RELOCATION_EQUIPMENT_TYPE,
                                        SAQASE.TECHNOLOGY
                                        FROM SYSPBT (NOLOCK)
                                        JOIN SAQASE (NOLOCK) ON SYSPBT.BATCH_RECORD_ID = SAQASE.EQUIPMENT_RECORD_ID JOIN MAEQCT(NOLOCK)
                                        ON SAQASE.EQUIPMENTCATEGORY_ID = MAEQCT.EQUIPMENTCATEGORY_ID
                                        WHERE 
                                        SYSPBT.QUOTE_RECORD_ID = '{QuoteRecId}' AND SYSPBT.QTEREV_RECORD_ID = '{RevisionRecordId}'
                                        AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}'                        
                                """.format(
                                QuoteId=contract_quote_id,
                                BatchGroupRecordId=batch_group_record_id,
                                UserName=User.UserName,
                                UserId=User.Id,
                                QuoteRecId=contract_quote_record_id,
                                RevisionId=quote_revision_id,
                                RevisionRecordId=quote_revision_record_id,
                                relocation_fab_type = "RECEIVING FAB",
                                relocation_equp_type ="RECEIVING EQUIPMENT",
                            )
                        )
            
        Sql.RunQuery(
                    """INSERT SAQFGB(
                        FABLOCATION_ID,
                        FABLOCATION_NAME,
                        FABLOCATION_RECORD_ID,
                        GREENBOOK,
                        GREENBOOK_RECORD_ID,
                        QUOTE_ID,
                        QUOTE_NAME,
                        QUOTE_RECORD_ID,
                        QTEREV_ID,
                        QTEREV_RECORD_ID,
                        SALESORG_ID,
                        SALESORG_NAME,
                        SALESORG_RECORD_ID,						
                        CpqTableEntryModifiedBy,
                        CpqTableEntryDateModified,
                        QUOTE_FAB_LOC_GB_RECORD_ID,
                        CPQTABLEENTRYADDEDBY,
                        CPQTABLEENTRYDATEADDED
                        ) SELECT FB.*,CONVERT(VARCHAR(4000),NEWID()) as QUOTE_FAB_LOC_GB_RECORD_ID,
                        '{UserName}' AS CPQTABLEENTRYADDEDBY,
                        GETDATE() as CPQTABLEENTRYDATEADDED FROM (
                        SELECT DISTINCT
                        SAQFEQ.FABLOCATION_ID,
                        SAQFEQ.FABLOCATION_NAME,
                        SAQFEQ.FABLOCATION_RECORD_ID,
                        SAQFEQ.GREENBOOK,
                        SAQFEQ.GREENBOOK_RECORD_ID,
                        SAQFEQ.QUOTE_ID,
                        SAQFEQ.QUOTE_NAME,
                        SAQFEQ.QUOTE_RECORD_ID,
                        SAQFEQ.QTEREV_ID,
                        SAQFEQ.QTEREV_RECORD_ID,
                        SAQFEQ.SALESORG_ID,
                        SAQFEQ.SALESORG_NAME,
                        SAQFEQ.SALESORG_RECORD_ID,
                        {UserId} as CpqTableEntryModifiedBy,
                        GETDATE() as CpqTableEntryDateModified
                        FROM SYSPBT (NOLOCK)
                        JOIN SAQFEQ (NOLOCK) ON SYSPBT.QUOTE_RECORD_ID = SAQFEQ.QUOTE_RECORD_ID AND SYSPBT.BATCH_RECORD_ID = SAQFEQ.EQUIPMENT_RECORD_ID AND SYSPBT.QTEREV_RECORD_ID = SAQFEQ.QTEREV_RECORD_ID
                        JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQFEQ.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = SAQFEQ.QTEREV_RECORD_ID
                        WHERE SAQFEQ.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQFEQ.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}'  AND NOT EXISTS (SELECT * FROM SAQFGB B WHERE QUOTE_RECORD_ID ='{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQFEQ.GREENBOOK = B.GREENBOOK AND FABLOCATION_ID IN {fab})
                        ) FB""".format(
                                        QuoteRecordId=contract_quote_record_id,
                                        RevisionRecordId=quote_revision_record_id,
                                        BatchGroupRecordId=batch_group_record_id,
                                        UserName=User.UserName,
                                        UserId=User.Id,
                                        fab = get_fab,
                                    )
                    )		
        Sql.RunQuery(
                    """
                        INSERT SAQFEA (
                            QUOTE_FAB_LOC_COV_OBJ_ASSEMBLY_RECORD_ID,
                            EQUIPMENT_ID,
                            EQUIPMENT_RECORD_ID,
                            EQUIPMENT_DESCRIPTION,
                            ASSEMBLY_ID,
                            ASSEMBLY_STATUS,
                            ASSEMBLY_DESCRIPTION,
                            ASSEMBLY_RECORD_ID,                           
                            FABLOCATION_ID,
                            FABLOCATION_NAME,
                            FABLOCATION_RECORD_ID,
                            SERIAL_NUMBER,
                            QUOTE_RECORD_ID,
                            QUOTE_ID,
                            QUOTE_NAME,
                            QTEREV_ID,
                            QTEREV_RECORD_ID,
                            EQUIPMENTCATEGORY_RECORD_ID,
                            EQUIPMENTCATEGORY_ID,
                            EQUIPMENTCATEGORY_DESCRIPTION,
                            EQUIPMENTTYPE_ID,
                            EQUIPMENTTYPE_DESCRIPTION,
                            EQUIPMENTTYPE_RECORD_ID,
                            GOT_CODE,
                            MNT_PLANT_RECORD_ID,
                            MNT_PLANT_ID,
                            WARRANTY_START_DATE,
                            WARRANTY_END_DATE,
                            SALESORG_ID,
                            SALESORG_NAME,
                            SALESORG_RECORD_ID,
                            GREENBOOK,
                            GREENBOOK_RECORD_ID,
                            CPQTABLEENTRYADDEDBY,
                            CPQTABLEENTRYDATEADDED,
                            CpqTableEntryModifiedBy,
                            CpqTableEntryDateModified
                            ) SELECT
                                CONVERT(VARCHAR(4000),NEWID()) as QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID,
                                SAQASE.PAR_EQUIPMENT_ID,
                                SAQASE.PAR_EQUIPMENT_RECORD_ID,
                                SAQASE.PAR_EQUIPMENT_DESCRIPTION,
                                SAQASE.SND_EQUIPMENT_ID,
                                SAQASE.EQUIPMENT_STATUS,
                                SAQASE.SND_EQUIPMENT_DESCRIPTION,       
                                SAQASE.SND_EQUIPMENT_RECORD_ID,                  
                                SAQASE.SNDFBL_ID,
                                SAQASE.SNDFBL_NAME,
                                SAQASE.SNDFBL_RECORD_ID,  
                                #SAQASE.SERIAL_NO,
                                '{QuoteRecId}' as QUOTE_RECORD_ID,
                                '{QuoteId}' as QUOTE_ID,
                                '{QuoteName}' as QUOTE_NAME,
                                '{RevisionId}' as QTEREV_ID,
                                '{RevisionRecordId}' as QTEREV_RECORD_ID,
                                SAQASE.EQUIPMENTCATEGORY_RECORD_ID,
                                SAQASE.EQUIPMENTCATEGORY_ID,
                                MAEQCT.EQUIPMENTCATEGORY_DESCRIPTION,
                                SAQASE.EQUIPMENTTYPE_ID,
                                MAEQTY.EQUIPMENT_TYPE_DESCRIPTION,
                                SAQASE.EQUIPMENTTYPE_RECORD_ID,
                                SAQASE.GOT_CODE,
                                SAQASE.MNT_PLANT_RECORD_ID,
                                SAQASE.MNT_PLANT_ID,
                                SAQASE.WARRANTY_START_DATE,
                                SAQASE.WARRANTY_END_DATE,
                                SAQASE.SALESORG_ID,
                                SAQASE.SALESORG_NAME,
                                SAQASE.SALESORG_RECORD_ID,
                                SAQASE.GREENBOOK,
                                SAQASE.GREENBOOK_RECORD_ID,
                                '{UserName}' AS CPQTABLEENTRYADDEDBY,
                                GETDATE() as CPQTABLEENTRYDATEADDED,
                                {UserId} as CpqTableEntryModifiedBy,
                                GETDATE() as CpqTableEntryDateModified
                                FROM SAQASE (NOLOCK)
                                JOIN SYSPBT (NOLOCK)
                                ON SYSPBT.BATCH_RECORD_ID = SAQASE.PAR_EQUIPMENT_RECORD_ID JOIN MAEQCT(NOLOCK)
                                ON SAQASE.EQUIPMENTCATEGORY_ID = MAEQCT.EQUIPMENTCATEGORY_ID JOIN MAEQTY (NOLOCK)
                                ON MAEQTY.EQUIPMENT_TYPE_ID = SAQASE.EQUIPMENTTYPE_ID
                                WHERE 
                                SYSPBT.QUOTE_RECORD_ID = '{QuoteRecId}' AND MAEQTY.COSTING_RELEVANT = 'True'
                                AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}'                        
                        """.format(
                        QuoteId=contract_quote_id,
                        BatchGroupRecordId=batch_group_record_id,
                        UserName=User.UserName,
                        UserId=User.Id,
                        QuoteRecId=contract_quote_record_id,
                        RevisionId=quote_revision_id,
                        RevisionRecordId=quote_revision_record_id,
                        QuoteName=contract_quote_name
                    )
                )







try: 
    node_type = Param.NodeType
except:
    node_type = ""
try: 
    subtab_name = Param.subtab_name
except:
    subtab_name = ""
try:
    values = Param.Values
except Exception:
    values = []
try:
    all_values = Param.AllValues
except Exception:
    all_values = False
try:
    A_Keys = Param.A_Keys
    A_Values = Param.A_Values
except:
    A_Keys = ""
    A_Values = ""

if subtab_name == "Sending Fab Locations":
    sending_fablocation_insert(values,all_values,A_Keys,A_Values)
elif subtab_name == "Sending Equipment":
    sending_equipment_insert(values,all_values,A_Keys,A_Values)
elif subtab_name == "Receiving Fab Locations":
    receiving_fablocation_insert(values,all_values,A_Keys,A_Values)
elif subtab_name == "Receiving Equipment":
    receiving_equipment_insert(values,all_values,A_Keys,A_Values)
    
        
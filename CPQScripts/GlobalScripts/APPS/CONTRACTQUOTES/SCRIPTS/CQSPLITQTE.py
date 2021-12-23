# =========================================================================================================================================
#   __script_name : CQSPLITQTE.PY
#   __script_description : THIS SCRIPT IS USED TO SPLIT THE ITEMS BY PRODUCT OFFERINGS
#   __primary_author__ : WASIM.ABDUL
#   __create_date :12-13-2021
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct
import clr
import System.Net
import sys
import re
import datetime
from System.Net import CookieContainer, NetworkCredential, Mail
from System.Net.Mail import SmtpClient, MailAddress, Attachment, MailMessage
from SYDATABASE import SQL
Sql = SQL()

TestProduct = Webcom.Configurator.Scripting.Test.TestProduct() or "Sales"
try:
    contract_quote_record_id = Quote.QuoteId
except:
    contract_quote_record_id = ''

try:
    quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
except:
    quote_revision_record_id = ""

try:
    current_prod = Product.Name
    
except:
    current_prod = "Sales"
try:
    TabName = TestProduct.CurrentTab
except:
    TabName = "Quotes"

contract_quote_rec_id = Quote.GetGlobal("contract_quote_record_id")
quote_revision_rec_id = Quote.GetGlobal("quote_revision_record_id")
user_id = str(User.Id)
user_name = str(User.UserName) 

def splitserviceinsert():
    splitservice_object = 'Z0105'
    material_obj = Sql.GetFirst("SELECT MATERIAL_RECORD_ID,SAP_DESCRIPTION,MATERIALCONFIG_TYPE FROM MAMTRL WHERE SAP_PART_NUMBER = '{}'".format(splitservice_object))
    #delete Z0105
    Sql.RunQuery("DELETE FROM SAQTSV WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_rec_id}' AND SERVICE_ID LIKE '{ServiceId}%'".format(
            contract_quote_rec_id=contract_quote_rec_id,quote_revision_rec_id=quote_revision_rec_id,ServiceId=splitservice_object))
    service_list=[]
    #NEED TO change Query for SAQRIT
    get_existing_record = Sql.GetList("SELECT SERVICE_ID FROM SAQTSV WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_rec_id}'".format(contract_quote_rec_id = contract_quote_rec_id,quote_revision_rec_id =quote_revision_rec_id))
    for i in get_existing_record:
        service_list.append(i.SERVICE_ID)
    parservice_values=tuple(service_list)
    parservice_values=re.sub('\,\)',')',str(parservice_values))
    if get_existing_record:
        description = material_obj.SAP_DESCRIPTION
        material_record_id = material_obj.MATERIAL_RECORD_ID

        Sql.RunQuery("""INSERT SAQTSV (QTEREV_RECORD_ID,QTEREV_ID,QUOTE_ID, QUOTE_NAME,UOM_ID,UOM_RECORD_ID, QUOTE_RECORD_ID, SERVICE_DESCRIPTION, SERVICE_ID, PAR_SERVICE_ID,PAR_SERVICE_DESCRIPTION,PAR_SERVICE_RECORD_ID,SERVICE_RECORD_ID, SERVICE_TYPE, CONTRACT_VALID_FROM, CONTRACT_VALID_TO, SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID, QUOTE_SERVICE_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified)
                        SELECT A.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED, {UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
                        SELECT DISTINCT QTEREV_RECORD_ID, QTEREV_ID,QUOTE_ID, QUOTE_NAME,UOM_ID,UOM_RECORD_ID, QUOTE_RECORD_ID, '{description}' AS SERVICE_DESCRIPTION, '{splitservice_object}' AS SERVICE_ID,SERVICE_ID as PAR_SERVICE_ID,SERVICE_DESCRIPTION AS PAR_SERVICE_DESCRIPTION,QUOTE_SERVICE_RECORD_ID as PAR_SERVICE_RECORD_ID, '{material_record_id}' AS SERVICE_RECORD_ID, '' AS SERVICE_TYPE, CONTRACT_VALID_FROM, CONTRACT_VALID_TO, SALESORG_ID, SALESORG_NAME,SALESORG_RECORD_ID FROM SAQTSV (NOLOCK)
                        WHERE SERVICE_ID IN {service_id} AND QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_rec_id}'
                        ) A""".format(description=description, service_id = parservice_values, material_record_id = material_record_id,contract_quote_rec_id = contract_quote_rec_id , quote_revision_rec_id = quote_revision_rec_id ,UserName = user_name, UserId = user_id,splitservice_object = splitservice_object ))
    
    ###split the items with new insert and updation:
    split_service =Sql.GetFirst("Select * FROM SAQTSV WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID ='Z0105'".format(contract_quote_rec_id,quote_revision_rec_id))
    splitservice_id = split_service.SERVICE_ID
    splitservice_name = split_service.SERVICE_DESCRIPTION
    splitservice_recid = split_service.SERVICE_RECORD_ID
    # SPLIT SAQRIS 
    equipmentservice_count = 0
    item_number_saqris_start = 0
    item_number_saqris_inc = 0
    quote_item_obj_service = Sql.GetFirst("SELECT TOP 1 LINE FROM SAQRIS (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' ORDER BY LINE DESC".format(QuoteRecordId=contract_quote_rec_id,RevisionRecordId=quote_revision_rec_id))
    if quote_item_obj_service:
        equipmentservice_count = int(quote_item_obj_service.LINE)
    doctype_service_obj = Sql.GetFirst("SELECT ITEM_NUMBER_START, ITEM_NUMBER_INCREMENT FROM SAQTRV LEFT JOIN SADOTY ON SADOTY.DOCTYPE_ID=SAQTRV.DOCTYP_ID WHERE SAQTRV.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQTRV.QTEREV_RECORD_ID = '{RevisionRecordId}'".format(QuoteRecordId=contract_quote_rec_id,RevisionRecordId=quote_revision_rec_id))
    if doctype_service_obj:
        item_number_saqris_start = int(doctype_service_obj.ITEM_NUMBER_START)
        item_number_saqris_inc = int(doctype_service_obj.ITEM_NUMBER_INCREMENT)
    
    QueryStatement ="""MERGE SAQRIS SRC USING (SELECT 	
    QUOTE_REV_ITEM_SUMMARY_RECORD_ID,COMMITTED_VALUE,CONTRACT_VALID_FROM,CONTRACT_VALID_TO,DIVISION_ID,DIVISION_RECORD_ID,DOC_CURRENCY,DOCCURR_RECORD_ID,ESTIMATED_VALUE,GLOBAL_CURRENCY,GLOBAL_CURRENCY_RECORD_ID,(({equipmentservice_count} + ROW_NUMBER()OVER(ORDER BY(SAQRIS.CpqTableEntryId))) * {item_number_saqris_inc}) as LINE,NET_PRICE,NET_PRICE_INGL_CURR,NET_VALUE,NET_VALUE_INGL_CURR,PLANT_ID,PLANT_RECORD_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,QUANTITY,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,TAX_PERCENTAGE,TAX_AMOUNT,TAX_AMOUNT_INGL_CURR,UNIT_PRICE,UNIT_PRICE_INGL_CURR  FROM SAQRIS where QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID  = '{quote_revision_rec_id}'  )
    TGT ON (SRC.QUOTE_RECORD_ID = TGT.QUOTE_RECORD_ID AND SRC.QTEREV_RECORD_ID = TGT.QTEREV_RECORD_ID AND SRC.SERVICE_ID = 'Z0105')
    WHEN NOT MATCHED BY TARGET
    THEN INSERT(QUOTE_REV_ITEM_SUMMARY_RECORD_ID,COMMITTED_VALUE,CONTRACT_VALID_FROM,CONTRACT_VALID_TO,DIVISION_ID,DIVISION_RECORD_ID,DOC_CURRENCY,DOCCURR_RECORD_ID,ESTIMATED_VALUE,GLOBAL_CURRENCY,GLOBAL_CURRENCY_RECORD_ID,LINE,NET_PRICE,NET_PRICE_INGL_CURR,NET_VALUE,NET_VALUE_INGL_CURR,PLANT_ID,PLANT_RECORD_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,QUANTITY,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,TAX_PERCENTAGE,TAX_AMOUNT,TAX_AMOUNT_INGL_CURR,UNIT_PRICE,UNIT_PRICE_INGL_CURR)
    VALUES (NEWID(),COMMITTED_VALUE,CONTRACT_VALID_FROM,CONTRACT_VALID_TO,DIVISION_ID,DIVISION_RECORD_ID,DOC_CURRENCY,DOCCURR_RECORD_ID,ESTIMATED_VALUE,GLOBAL_CURRENCY,GLOBAL_CURRENCY_RECORD_ID,LINE,NET_PRICE,NET_PRICE_INGL_CURR,NET_VALUE,NET_VALUE_INGL_CURR,PLANT_ID,PLANT_RECORD_ID,'{splitservice_name}', '{splitservice_id}','{splitservice_recid}',QUANTITY,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,TAX_PERCENTAGE,TAX_AMOUNT,TAX_AMOUNT_INGL_CURR,UNIT_PRICE,UNIT_PRICE_INGL_CURR);""".format(contract_quote_rec_id=contract_quote_rec_id,quote_revision_rec_id = quote_revision_rec_id,splitservice_recid = splitservice_recid,splitservice_id=splitservice_id,splitservice_name = splitservice_name,equipmentservice_count =equipmentservice_count,item_number_saqris_inc =item_number_saqris_inc )
    Sql.RunQuery(QueryStatement)
    #INSERT FOR SAQRIT
    service_entitlement_objs = Sql.GetList("""SELECT SERVICE_ID, ENTITLEMENT_XML FROM  SAQTSE (NOLOCK) WHERE QUOTE_RECORD_ID ='{contract_quote_rec_id}' AND QTEREV_RECORD_ID ='{quote_revision_rec_id}'""".format(contract_quote_rec_id=contract_quote_rec_id,quote_revision_rec_id=quote_revision_rec_id) )
    for service_entitlement_obj in service_entitlement_objs:	
        quote_item_tag_pattern = re.compile(r'(<QUOTE_ITEM_ENTITLEMENT>[\w\W]*?</QUOTE_ITEM_ENTITLEMENT>)')
        entitlement_id_tag_pattern = re.compile(r'<ENTITLEMENT_ID>AGS_'+str(service_entitlement_obj.SERVICE_ID)+'_PQB_QTITST</ENTITLEMENT_ID>')
        ##getting billing type
        billing_type_pattern = re.compile(r'<ENTITLEMENT_ID>AGS_'+str(service_entitlement_obj.SERVICE_ID)+'_PQB_BILTYP</ENTITLEMENT_ID>')
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
                        Trace.Write("1")
                        servicelevel_split_equip(service_entitlement_obj.SERVICE_ID)
                    elif quote_service_entitlement_type in ('OFFERING + FAB + GREENBOOK + GROUP OF EQUIPMENT', 'OFFERING + GREENBOOK + GR EQUI', 'OFFERING + CHILD GROUP OF PART'):
                        Trace.Write("2")
                        servicelevel_split_green(service_entitlement_obj.SERVICE_ID)
                    elif quote_service_entitlement_type in ('OFFERING + PM EVENT','OFFERING+CONSIGNED+ON REQUEST'):
                        Trace.Write("3")    


def servicelevel_split_equip(seid):
    Trace.Write("SAQSCE_SPLIT"+str(seid))
    #seid ="Z0091"
    where_condition = "WHERE SERVICE_ID = ''"+str(seid)+"'' AND QUOTE_RECORD_ID = ''"+str(contract_quote_rec_id)+"'' and QTEREV_RECORD_ID = ''"+str(quote_revision_rec_id)+"''  "
    get_c4c_quote_id = Sql.GetFirst("select * from SAQTMT where MASTER_TABLE_QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_rec_id}'".format(contract_quote_rec_id =contract_quote_rec_id,quote_revision_rec_id = quote_revision_rec_id))
    ent_temp = "ENT_SPLIT_BKP_"+str(get_c4c_quote_id.C4C_QUOTE_ID)

    Trace.Write("aaaaaaa"+str(ent_temp))
    ent_child_temp_drop = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(ent_temp)+"'' ) BEGIN DROP TABLE "+str(ent_temp)+" END  ' ")

    SqlHelper.GetFirst("sp_executesql @T=N'declare @H int; Declare @val Varchar(MAX);DECLARE @XML XML; SELECT @val =  replace(replace(STUFF((SELECT ''''+FINAL from(select  REPLACE(entitlement_xml,''<QUOTE_ITEM_ENTITLEMENT>'',sml) AS FINAL FROM (select ''  <QUOTE_ITEM_ENTITLEMENT><QUOTE_ID>''+quote_id+''</QUOTE_ID><QUOTE_RECORD_ID>''+QUOTE_RECORD_ID+''</QUOTE_RECORD_ID><QTEREV_RECORD_ID>''+QTEREV_RECORD_ID+''</QTEREV_RECORD_ID><SERVICE_ID>''+service_id+''</SERVICE_ID><FABLOCATION_ID>''+FABLOCATION_ID+''</FABLOCATION_ID><GREENBOOK>''+GREENBOOK+''</GREENBOOK><EQUIPMENT_ID>''+equipment_id+''</EQUIPMENT_ID>'' AS sml,replace(replace(replace(replace(replace(replace(replace(replace(ENTITLEMENT_XML,''&'','';#38''),'''','';#39''),'' < '','' &lt; '' ),'' > '','' &gt; '' ),''_>'',''_&gt;''),''_<'',''_&lt;''),''&'','';#38''),''<10%'',''&lt;10%'')  as entitlement_xml from SAQSCE(nolock) "+str(where_condition)+" )A )a FOR XML PATH ('''')), 1, 1, ''''),''&lt;'',''<''),''&gt;'',''>'')  SELECT @XML = CONVERT(XML,''<ROOT>''+@VAL+''</ROOT>'') exec sys.sp_xml_preparedocument @H output,@XML; select QUOTE_ID,QUOTE_RECORD_ID,QTEREV_RECORD_ID,EQUIPMENT_ID,SERVICE_ID,ENTITLEMENT_ID,ENTITLEMENT_NAME,ENTITLEMENT_COST_IMPACT,FABLOCATION_ID,GREENBOOK,ENTITLEMENT_VALUE_CODE,ENTITLEMENT_DISPLAY_VALUE,ENTITLEMENT_PRICE_IMPACT,IS_DEFAULT,ENTITLEMENT_TYPE,ENTITLEMENT_DESCRIPTION,PRICE_METHOD,CALCULATION_FACTOR INTO "+str(ent_temp)+"  from openxml(@H, ''ROOT/QUOTE_ITEM_ENTITLEMENT'', 0) with (QUOTE_ID VARCHAR(100) ''QUOTE_ID'',QUOTE_RECORD_ID VARCHAR(100) ''QUOTE_RECORD_ID'',QTEREV_RECORD_ID VARCHAR(100) ''QTEREV_RECORD_ID'',EQUIPMENT_ID VARCHAR(100) ''EQUIPMENT_ID'',ENTITLEMENT_NAME VARCHAR(100) ''ENTITLEMENT_NAME'',ENTITLEMENT_ID VARCHAR(100) ''ENTITLEMENT_ID'',SERVICE_ID VARCHAR(100) ''SERVICE_ID'',ENTITLEMENT_COST_IMPACT VARCHAR(100) ''ENTITLEMENT_COST_IMPACT'',FABLOCATION_ID VARCHAR(100) ''FABLOCATION_ID'',GREENBOOK VARCHAR(100) ''GREENBOOK'',ENTITLEMENT_VALUE_CODE VARCHAR(100) ''ENTITLEMENT_VALUE_CODE'',ENTITLEMENT_DISPLAY_VALUE VARCHAR(100) ''ENTITLEMENT_DISPLAY_VALUE'',ENTITLEMENT_PRICE_IMPACT VARCHAR(100) ''ENTITLEMENT_PRICE_IMPACT'',IS_DEFAULT VARCHAR(100) ''IS_DEFAULT'',ENTITLEMENT_TYPE VARCHAR(100) ''ENTITLEMENT_TYPE'',ENTITLEMENT_DESCRIPTION VARCHAR(100) ''ENTITLEMENT_DESCRIPTION'',PRICE_METHOD VARCHAR(100) ''PRICE_METHOD'',CALCULATION_FACTOR VARCHAR(100) ''CALCULATION_FACTOR'') ; exec sys.sp_xml_removedocument @H; '")

    #a = SqlHelper.GetList("select * from ENT_SPLIT_BKP_3050008527 where ENTITLEMENT_ID  ='AGS_Z0091_SER_SPLIT_PER'")
    #updating the split percent from Xml
    entitlement_service_id = 'AGS_'+str(seid)+'_SER_SPLIT_PER'
    updatesaqritchild ="""UPDATE A SET A.SPLIT_PERCENT =  B.ENTITLEMENT_DISPLAY_VALUE  FROM SAQRIT A JOIN {ent_temp} B ON A.QUOTE_RECORD_ID =B.QUOTE_RECORD_ID  AND A.QTEREV_RECORD_ID  =B.QTEREV_RECORD_ID AND A.SERVICE_ID =B.SERVICE_ID AND A.FABLOCATION_ID  = B.FABLOCATION_ID AND A.GREENBOOK  = B.GREENBOOK AND A.OBJECT_ID = B.EQUIPMENT_ID WHERE  A.QUOTE_RECORD_ID ='{contract_quote_rec_id}' AND A.QTEREV_RECORD_ID='{quote_revision_rec_id}' AND A.SERVICE_ID ='{seid}' AND B.ENTITLEMENT_ID  ='{entitlement_service_id}'""".format(contract_quote_rec_id =contract_quote_rec_id,quote_revision_rec_id =quote_revision_rec_id,ent_temp = ent_temp,entitlement_service_id =entitlement_service_id,seid =seid)
    Sql.RunQuery(updatesaqritchild)
    ent_child_temp_drop = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(ent_temp)+"'' ) BEGIN DROP TABLE "+str(ent_temp)+" END  ' ")
    ##INSERTING CHILD TO PARENT SERVICE.
    split_service =Sql.GetFirst("Select * FROM SAQTSV WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID ='Z0105'".format(contract_quote_rec_id,quote_revision_rec_id))
    splitservice_id = split_service.SERVICE_ID
    splitservice_name = split_service.SERVICE_DESCRIPTION
    splitservice_recid = split_service.SERVICE_RECORD_ID
    equipments_count = 0
    item_number_saqrit_start = 0
    item_number_saqrit_inc = 0
    quote_item_obj = Sql.GetFirst("SELECT TOP 1 LINE FROM SAQRIT (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' ORDER BY LINE DESC".format(QuoteRecordId=contract_quote_rec_id,RevisionRecordId=quote_revision_rec_id))
    if quote_item_obj:
        equipments_count = int(quote_item_obj.LINE)
    doctype_obj = Sql.GetFirst("SELECT ITEM_NUMBER_START, ITEM_NUMBER_INCREMENT FROM SAQTRV LEFT JOIN SADOTY ON SADOTY.DOCTYPE_ID=SAQTRV.DOCTYP_ID WHERE SAQTRV.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQTRV.QTEREV_RECORD_ID = '{RevisionRecordId}'".format(QuoteRecordId=contract_quote_rec_id,RevisionRecordId=quote_revision_rec_id))
    if doctype_obj:
        item_number_saqrit_start = int(doctype_obj.ITEM_NUMBER_START)
        item_number_saqrit_inc = int(doctype_obj.ITEM_NUMBER_INCREMENT)
    
    Sql.RunQuery("""INSERT SAQRIT (CONTRACT_VALID_FROM,CONTRACT_VALID_TO,DOC_CURRENCY,DOCURR_RECORD_ID,EXCHANGE_RATE,EXCHANGE_RATE_DATE,EXCHANGE_RATE_RECORD_ID,GL_ACCOUNT_NO,GLOBAL_CURRENCY,GLOBAL_CURRENCY_RECORD_ID,LINE,OBJECT_ID,OBJECT_TYPE,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,PROFIT_CENTER,QUANTITY,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,REF_SALESORDER,TAX_PERCENTAGE,TAX_AMOUNT,TAX_AMOUNT_INGL_CURR,TAXCLASSIFICATION_DESCRIPTION,TAXCLASSIFICATION_ID,TAXCLASSIFICATION_RECORD_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,GREENBOOK,GREENBOOK_RECORD_ID,NET_PRICE,NET_PRICE_INGL_CURR,PLANT_ID,PLANT_NAME,PLANT_RECORD_ID,COMVAL_INGL_CURR,ESTVAL_INGL_CURR,NET_VALUE,NET_VALUE_INGL_CURR,UNIT_PRICE,UNIT_PRICE_INGL_CURR,QTEITMSUM_RECORD_ID,MODULE_ID,MODULE_NAME,MODULE_RECORD_ID,PARQTEITM_LINE,PARQTEITM_LINE_RECORD_ID,BILLING_TYPE,COMMITTED_VALUE,ESTIMATED_VALUE,SPLIT_PERCENT,SPLIT,STATUS,QUOTE_REVISION_CONTRACT_ITEM_ID) 
    SELECT A.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REVISION_CONTRACT_ITEM_ID FROM (
    SELECT DISTINCT CONTRACT_VALID_FROM,CONTRACT_VALID_TO,DOC_CURRENCY,DOCURR_RECORD_ID,EXCHANGE_RATE,EXCHANGE_RATE_DATE,EXCHANGE_RATE_RECORD_ID,GL_ACCOUNT_NO,GLOBAL_CURRENCY,GLOBAL_CURRENCY_RECORD_ID,(({equipments_count} + ROW_NUMBER()OVER(ORDER BY(SAQRIT.CpqTableEntryId))) * {item_number_saqrit_inc}) AS LINE,OBJECT_ID,OBJECT_TYPE,'{splitservice_name}' as SERVICE_DESCRIPTION,'{splitservice_id}' as SERVICE_ID,'{splitservice_recid}' as SERVICE_RECORD_ID,PROFIT_CENTER,QUANTITY,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,REF_SALESORDER,TAX_PERCENTAGE,TAX_AMOUNT,TAX_AMOUNT_INGL_CURR,TAXCLASSIFICATION_DESCRIPTION,TAXCLASSIFICATION_ID,TAXCLASSIFICATION_RECORD_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,GREENBOOK,GREENBOOK_RECORD_ID,NET_PRICE ,NET_PRICE_INGL_CURR,PLANT_ID,PLANT_NAME,PLANT_RECORD_ID,COMVAL_INGL_CURR,ESTVAL_INGL_CURR,NET_VALUE ,NET_VALUE_INGL_CURR,UNIT_PRICE,UNIT_PRICE_INGL_CURR,QTEITMSUM_RECORD_ID,MODULE_ID,MODULE_NAME,MODULE_RECORD_ID,LINE AS PARQTEITM_LINE,QUOTE_REVISION_CONTRACT_ITEM_ID AS PARQTEITM_LINE_RECORD_ID,BILLING_TYPE,COMMITTED_VALUE,ESTIMATED_VALUE,SPLIT_PERCENT,SPLIT,'ACQUIRED' AS STATUS FROM SAQRIT WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_rec_id}' AND SERVICE_ID = '{seid}' AND SPLIT ='' )A""".format(contract_quote_rec_id = contract_quote_rec_id , quote_revision_rec_id = quote_revision_rec_id,item_number_saqrit_inc =item_number_saqrit_inc,equipments_count =equipments_count,splitservice_recid = splitservice_recid,splitservice_id=splitservice_id,splitservice_name = splitservice_name,seid = seid))
    
    #UPDATE PRICING TO CLONE RECORD AS WELL AS MASTER
    update_pricing = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET A.NET_PRICE = (CASE WHEN ISNULL(A.PARQTEITM_LINE_RECORD_ID,'''')='''' AND ISNULL(A.PARQTEITM_LINE,'''') = '''' THEN NET_PRICE * XY.SPLIT_PERCENT/100 WHEN A.PARQTEITM_LINE_RECORD_ID <> A.QUOTE_REVISION_CONTRACT_ITEM_ID AND ISNULL(A.PARQTEITM_LINE,'''') <> ''''  and ISNULL(A.PARQTEITM_LINE_RECORD_ID,'''') <> '''' THEN NET_PRICE * (100-XY.SPLIT_PERCENT)/100 END),A.NET_PRICE_INGL_CURR = (CASE WHEN ISNULL(A.PARQTEITM_LINE_RECORD_ID,'''')='''' AND ISNULL(A.PARQTEITM_LINE,'''') = '''' THEN NET_PRICE_INGL_CURR * XY.SPLIT_PERCENT/100 WHEN A.PARQTEITM_LINE_RECORD_ID <> A.QUOTE_REVISION_CONTRACT_ITEM_ID AND ISNULL(A.PARQTEITM_LINE,'''') <> ''''  and ISNULL(A.PARQTEITM_LINE_RECORD_ID,'''') <> '''' THEN NET_PRICE_INGL_CURR * (100-XY.SPLIT_PERCENT)/100 END),A.NET_VALUE = (CASE WHEN ISNULL(A.PARQTEITM_LINE_RECORD_ID,'''')='''' AND ISNULL(A.PARQTEITM_LINE,'''') = '''' THEN NET_PRICE * XY.SPLIT_PERCENT/100 WHEN A.PARQTEITM_LINE_RECORD_ID <> A.QUOTE_REVISION_CONTRACT_ITEM_ID AND ISNULL(A.PARQTEITM_LINE,'''') <> ''''  and ISNULL(A.PARQTEITM_LINE_RECORD_ID,'''') <> '''' THEN NET_PRICE * (100-XY.SPLIT_PERCENT)/100 END) + TAX_AMOUNT,A.NET_VALUE_INGL_CURR = (CASE WHEN ISNULL(A.PARQTEITM_LINE_RECORD_ID,'''')='''' AND ISNULL(A.PARQTEITM_LINE,'''') = '''' THEN NET_PRICE_INGL_CURR * XY.SPLIT_PERCENT/100 WHEN A.PARQTEITM_LINE_RECORD_ID <> A.QUOTE_REVISION_CONTRACT_ITEM_ID AND ISNULL(A.PARQTEITM_LINE,'''') <> ''''  and ISNULL(A.PARQTEITM_LINE_RECORD_ID,'''') <> '''' THEN NET_PRICE_INGL_CURR * (100-XY.SPLIT_PERCENT)/100 END) + TAX_AMOUNT,A.SPLIT = ''YES'',A.SPLIT_PERCENT = (CASE WHEN ISNULL(A.PARQTEITM_LINE_RECORD_ID,'''')='''' AND ISNULL(A.PARQTEITM_LINE,'''') = '''' THEN XY.SPLIT_PERCENT WHEN A.PARQTEITM_LINE_RECORD_ID <> A.QUOTE_REVISION_CONTRACT_ITEM_ID AND ISNULL(A.PARQTEITM_LINE,'''') <> ''''  and ISNULL(A.PARQTEITM_LINE_RECORD_ID,'''') <> '''' THEN 100-XY.SPLIT_PERCENT END),A.UNIT_PRICE_INGL_CURR = (CASE WHEN A.PARQTEITM_LINE_RECORD_ID <> A.QUOTE_REVISION_CONTRACT_ITEM_ID AND ISNULL(A.PARQTEITM_LINE,'''') <> ''''  and ISNULL(A.PARQTEITM_LINE_RECORD_ID,'''') <> '''' THEN NET_PRICE_INGL_CURR * (100-XY.SPLIT_PERCENT)/100 END),A.UNIT_PRICE = (CASE WHEN A.PARQTEITM_LINE_RECORD_ID <> A.QUOTE_REVISION_CONTRACT_ITEM_ID AND ISNULL(A.PARQTEITM_LINE,'''') <> ''''  and ISNULL(A.PARQTEITM_LINE_RECORD_ID,'''') <> '''' THEN NET_PRICE * (100-XY.SPLIT_PERCENT)/100 END) FROM SAQRIT(NOLOCK)A INNER JOIN(SELECT DISTINCT B.SPLIT_PERCENT,B.QUOTE_RECORD_ID,B.QTEREV_RECORD_ID,B.OBJECT_ID FROM SAQRIT B(NOLOCK) WHERE B.QUOTE_RECORD_ID = ''"+str(contract_quote_rec_id)+"'' AND B.SERVICE_ID = ''"+str(seid)+"'') AS XY ON A.QUOTE_RECORD_ID = XY.QUOTE_RECORD_ID AND A.QTEREV_RECORD_ID = XY.QTEREV_RECORD_ID AND A.OBJECT_ID = XY.OBJECT_ID  WHERE A.QUOTE_RECORD_ID = ''"+str(contract_quote_rec_id)+"'' AND A.SPLIT <> ''YES'' '".format(contract_quote_rec_id =contract_quote_rec_id,seid =seid))
    #SUM UPTO SAQRIS:
    update_service_parent_summary = """UPDATE A  SET A.NET_PRICE = B.NET_PRICE,A.NET_PRICE_INGL_CURR = B.NET_PRICE_INGL_CURR,A.NET_VALUE = B.NET_VALUE,A.NET_VALUE_INGL_CURR = B.NET_VALUE_INGL_CURR,A.UNIT_PRICE = B.UNIT_PRICE,A.UNIT_PRICE_INGL_CURR = B.UNIT_PRICE_INGL_CURR FROM SAQRIS A(NOLOCK) JOIN (SELECT SUM(NET_PRICE) AS NET_PRICE,SUM(NET_PRICE_INGL_CURR) AS NET_PRICE_INGL_CURR,SUM(NET_VALUE) AS NET_VALUE,SUM(NET_VALUE_INGL_CURR) AS NET_VALUE_INGL_CURR,SUM(UNIT_PRICE) AS UNIT_PRICE,SUM(UNIT_PRICE_INGL_CURR) AS UNIT_PRICE_INGL_CURR,QUOTE_RECORD_ID,QTEREV_RECORD_ID,SERVICE_ID from SAQRIT(NOLOCK) WHERE QUOTE_RECORD_ID ='{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_rec_id}'  AND SERVICE_ID = '{seid}' GROUP BY QUOTE_RECORD_ID,QTEREV_RECORD_ID,SERVICE_ID) B ON A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.SERVICE_ID=B.SERVICE_ID AND A.QTEREV_RECORD_ID = B.QTEREV_RECORD_ID """.format(contract_quote_rec_id= contract_quote_rec_id,quote_revision_rec_id = quote_revision_rec_id,seid =seid)
    Sql.RunQuery(update_service_parent_summary)
    update_service_child_summary = """UPDATE A  SET A.NET_PRICE = B.NET_PRICE,A.NET_PRICE_INGL_CURR = B.NET_PRICE_INGL_CURR,A.NET_VALUE = B.NET_VALUE,A.NET_VALUE_INGL_CURR = B.NET_VALUE_INGL_CURR,A.UNIT_PRICE = B.UNIT_PRICE,A.UNIT_PRICE_INGL_CURR = B.UNIT_PRICE_INGL_CURR FROM SAQRIS A(NOLOCK) JOIN (SELECT SUM(NET_PRICE) AS NET_PRICE,SUM(NET_PRICE_INGL_CURR) AS NET_PRICE_INGL_CURR,SUM(NET_VALUE) AS NET_VALUE,SUM(NET_VALUE_INGL_CURR) AS NET_VALUE_INGL_CURR,SUM(UNIT_PRICE) AS UNIT_PRICE,SUM(UNIT_PRICE_INGL_CURR) AS UNIT_PRICE_INGL_CURR,QUOTE_RECORD_ID,QTEREV_RECORD_ID,SERVICE_ID from SAQRIT(NOLOCK) WHERE QUOTE_RECORD_ID ='{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_rec_id}'  AND SERVICE_ID = '{splitservice_id}' GROUP BY QUOTE_RECORD_ID,QTEREV_RECORD_ID,SERVICE_ID) B ON A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.SERVICE_ID=B.SERVICE_ID AND A.QTEREV_RECORD_ID = B.QTEREV_RECORD_ID """.format(contract_quote_rec_id= contract_quote_rec_id,quote_revision_rec_id = quote_revision_rec_id,seid =seid,splitservice_id =splitservice_id)
    Sql.RunQuery(update_service_child_summary)
    #Object list grid
    saqrioinsert ="""MERGE SAQRIO SRC USING (SELECT A.QUOTE_REVISION_ITEM_OBJECT_RECORD_ID,A.CUSTOMER_TOOL_ID,A.EQUIPMENT_DESCRIPTION,A.EQUIPMENT_ID,A.EQUIPMENT_RECORD_ID,A.GREENBOOK,A.GREENBOOK_RECORD_ID,A.KPU,B.LINE,B.SERVICE_DESCRIPTION,B.SERVICE_ID,B.SERVICE_RECORD_ID,A.QUOTE_ID,A.QTEITM_RECORD_ID,A.QUOTE_RECORD_ID,A.QTEREV_ID,A.QTEREV_RECORD_ID,A.SERIAL_NUMBER,A.TECHNOLOGY,A.TOOL_CONFIGURATION,A.WAFER_SIZE,B.QUOTE_REVISION_CONTRACT_ITEM_ID FROM SAQRIO(NOLOCK) A JOIN SAQRIT (NOLOCK) B ON A.QUOTE_RECORD_ID  = B.QUOTE_RECORD_ID AND A.LINE = B.PARQTEITM_LINE where B.QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND B.QTEREV_RECORD_ID  = '{quote_revision_rec_id}' AND B.SERVICE_ID = '{splitservice_id}')
    TGT ON (SRC.QUOTE_RECORD_ID = TGT.QUOTE_RECORD_ID AND SRC.QTEREV_RECORD_ID = TGT.QTEREV_RECORD_ID AND SRC.SERVICE_ID = '{splitservice_id}')
    WHEN NOT MATCHED BY TARGET
    THEN INSERT(QUOTE_REVISION_ITEM_OBJECT_RECORD_ID,CUSTOMER_TOOL_ID,EQUIPMENT_DESCRIPTION,EQUIPMENT_ID,EQUIPMENT_RECORD_ID,GREENBOOK,GREENBOOK_RECORD_ID,KPU,LINE,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,QUOTE_ID,QTEITM_RECORD_ID,QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,SERIAL_NUMBER,TECHNOLOGY,TOOL_CONFIGURATION,WAFER_SIZE)
    VALUES (NEWID(),CUSTOMER_TOOL_ID,EQUIPMENT_DESCRIPTION,EQUIPMENT_ID,EQUIPMENT_RECORD_ID,GREENBOOK,GREENBOOK_RECORD_ID,KPU,LINE,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,QUOTE_ID,QUOTE_REVISION_CONTRACT_ITEM_ID,QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,SERIAL_NUMBER,TECHNOLOGY,TOOL_CONFIGURATION,WAFER_SIZE);""".format(contract_quote_rec_id=contract_quote_rec_id,quote_revision_rec_id = quote_revision_rec_id,splitservice_id =splitservice_id )
    Sql.RunQuery(saqrioinsert)

def servicelevel_split_green(seid):
    Trace.Write("thisgreen service"+str(seid))
    where_condition = "WHERE SERVICE_ID = ''"+str(seid)+"'' AND QUOTE_RECORD_ID = ''"+str(contract_quote_rec_id)+"'' and QTEREV_RECORD_ID = ''"+str(quote_revision_rec_id)+"''  "
    get_c4c_quote_id = Sql.GetFirst("select * from SAQTMT where MASTER_TABLE_QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_rec_id}'".format(contract_quote_rec_id =contract_quote_rec_id,quote_revision_rec_id = quote_revision_rec_id))
    ent_temp = "ENT_SPLIT_BKP_"+str(get_c4c_quote_id.C4C_QUOTE_ID)

    Trace.Write("aaaaaaa"+str(ent_temp))
    ent_child_temp_drop = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(ent_temp)+"'' ) BEGIN DROP TABLE "+str(ent_temp)+" END  ' ")

    SqlHelper.GetFirst("sp_executesql @T=N'declare @H int; Declare @val Varchar(MAX);DECLARE @XML XML; SELECT @val =  replace(replace(STUFF((SELECT ''''+FINAL from(select  REPLACE(entitlement_xml,''<QUOTE_ITEM_ENTITLEMENT>'',sml) AS FINAL FROM (select ''  <QUOTE_ITEM_ENTITLEMENT><QUOTE_ID>''+quote_id+''</QUOTE_ID><QUOTE_RECORD_ID>''+QUOTE_RECORD_ID+''</QUOTE_RECORD_ID><QTEREV_RECORD_ID>''+QTEREV_RECORD_ID+''</QTEREV_RECORD_ID><SERVICE_ID>''+service_id+''</SERVICE_ID><FABLOCATION_ID>''+FABLOCATION_ID+''</FABLOCATION_ID><GREENBOOK>''+GREENBOOK+''</GREENBOOK><EQUIPMENT_ID>''+equipment_id+''</EQUIPMENT_ID>'' AS sml,replace(replace(replace(replace(replace(replace(replace(replace(ENTITLEMENT_XML,''&'','';#38''),'''','';#39''),'' < '','' &lt; '' ),'' > '','' &gt; '' ),''_>'',''_&gt;''),''_<'',''_&lt;''),''&'','';#38''),''<10%'',''&lt;10%'')  as entitlement_xml from SAQSCE(nolock) "+str(where_condition)+" )A )a FOR XML PATH ('''')), 1, 1, ''''),''&lt;'',''<''),''&gt;'',''>'')  SELECT @XML = CONVERT(XML,''<ROOT>''+@VAL+''</ROOT>'') exec sys.sp_xml_preparedocument @H output,@XML; select QUOTE_ID,QUOTE_RECORD_ID,QTEREV_RECORD_ID,EQUIPMENT_ID,SERVICE_ID,ENTITLEMENT_ID,ENTITLEMENT_NAME,ENTITLEMENT_COST_IMPACT,FABLOCATION_ID,GREENBOOK,ENTITLEMENT_VALUE_CODE,ENTITLEMENT_DISPLAY_VALUE,ENTITLEMENT_PRICE_IMPACT,IS_DEFAULT,ENTITLEMENT_TYPE,ENTITLEMENT_DESCRIPTION,PRICE_METHOD,CALCULATION_FACTOR INTO "+str(ent_temp)+"  from openxml(@H, ''ROOT/QUOTE_ITEM_ENTITLEMENT'', 0) with (QUOTE_ID VARCHAR(100) ''QUOTE_ID'',QUOTE_RECORD_ID VARCHAR(100) ''QUOTE_RECORD_ID'',QTEREV_RECORD_ID VARCHAR(100) ''QTEREV_RECORD_ID'',EQUIPMENT_ID VARCHAR(100) ''EQUIPMENT_ID'',ENTITLEMENT_NAME VARCHAR(100) ''ENTITLEMENT_NAME'',ENTITLEMENT_ID VARCHAR(100) ''ENTITLEMENT_ID'',SERVICE_ID VARCHAR(100) ''SERVICE_ID'',ENTITLEMENT_COST_IMPACT VARCHAR(100) ''ENTITLEMENT_COST_IMPACT'',FABLOCATION_ID VARCHAR(100) ''FABLOCATION_ID'',GREENBOOK VARCHAR(100) ''GREENBOOK'',ENTITLEMENT_VALUE_CODE VARCHAR(100) ''ENTITLEMENT_VALUE_CODE'',ENTITLEMENT_DISPLAY_VALUE VARCHAR(100) ''ENTITLEMENT_DISPLAY_VALUE'',ENTITLEMENT_PRICE_IMPACT VARCHAR(100) ''ENTITLEMENT_PRICE_IMPACT'',IS_DEFAULT VARCHAR(100) ''IS_DEFAULT'',ENTITLEMENT_TYPE VARCHAR(100) ''ENTITLEMENT_TYPE'',ENTITLEMENT_DESCRIPTION VARCHAR(100) ''ENTITLEMENT_DESCRIPTION'',PRICE_METHOD VARCHAR(100) ''PRICE_METHOD'',CALCULATION_FACTOR VARCHAR(100) ''CALCULATION_FACTOR'') ; exec sys.sp_xml_removedocument @H; '")

    #a = SqlHelper.GetList("select * from ENT_SPLIT_BKP_3050008527 where ENTITLEMENT_ID  ='AGS_Z0091_SER_SPLIT_PER'")
    #updating the split percent from Xml
    entitlement_service_id = 'AGS_'+str(seid)+'_SER_SPLIT_PER'
    updatesaqritchild ="""UPDATE A SET A.SPLIT_PERCENT =  B.ENTITLEMENT_DISPLAY_VALUE  FROM SAQRIT A JOIN {ent_temp} B ON A.QUOTE_RECORD_ID =B.QUOTE_RECORD_ID  AND A.QTEREV_RECORD_ID  =B.QTEREV_RECORD_ID AND A.SERVICE_ID =B.SERVICE_ID AND A.FABLOCATION_ID  = B.FABLOCATION_ID AND A.GREENBOOK  = B.GREENBOOK WHERE  A.QUOTE_RECORD_ID ='{contract_quote_rec_id}' AND A.QTEREV_RECORD_ID='{quote_revision_rec_id}' AND A.SERVICE_ID ='{seid}' AND B.ENTITLEMENT_ID  ='{entitlement_service_id}'""".format(contract_quote_rec_id =contract_quote_rec_id,quote_revision_rec_id =quote_revision_rec_id,ent_temp = ent_temp,entitlement_service_id =entitlement_service_id,seid =seid)
    Sql.RunQuery(updatesaqritchild)
    ent_child_temp_drop = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(ent_temp)+"'' ) BEGIN DROP TABLE "+str(ent_temp)+" END  ' ")
    ##INSERTING CHILD TO PARENT SERVICE.
    split_service =Sql.GetFirst("Select * FROM SAQTSV WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID ='Z0105'".format(contract_quote_rec_id,quote_revision_rec_id))
    splitservice_id = split_service.SERVICE_ID
    splitservice_name = split_service.SERVICE_DESCRIPTION
    splitservice_recid = split_service.SERVICE_RECORD_ID
    equipments_count = 0
    item_number_saqrit_start = 0
    item_number_saqrit_inc = 0
    quote_item_obj = Sql.GetFirst("SELECT TOP 1 LINE FROM SAQRIT (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' ORDER BY LINE DESC".format(QuoteRecordId=contract_quote_rec_id,RevisionRecordId=quote_revision_rec_id))
    if quote_item_obj:
        equipments_count = int(quote_item_obj.LINE)
    doctype_obj = Sql.GetFirst("SELECT ITEM_NUMBER_START, ITEM_NUMBER_INCREMENT FROM SAQTRV LEFT JOIN SADOTY ON SADOTY.DOCTYPE_ID=SAQTRV.DOCTYP_ID WHERE SAQTRV.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQTRV.QTEREV_RECORD_ID = '{RevisionRecordId}'".format(QuoteRecordId=contract_quote_rec_id,RevisionRecordId=quote_revision_rec_id))
    if doctype_obj:
        item_number_saqrit_start = int(doctype_obj.ITEM_NUMBER_START)
        item_number_saqrit_inc = int(doctype_obj.ITEM_NUMBER_INCREMENT)
    
    Sql.RunQuery("""INSERT SAQRIT (CONTRACT_VALID_FROM,CONTRACT_VALID_TO,DOC_CURRENCY,DOCURR_RECORD_ID,EXCHANGE_RATE,EXCHANGE_RATE_DATE,EXCHANGE_RATE_RECORD_ID,GL_ACCOUNT_NO,GLOBAL_CURRENCY,GLOBAL_CURRENCY_RECORD_ID,LINE,OBJECT_ID,OBJECT_TYPE,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,PROFIT_CENTER,QUANTITY,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,REF_SALESORDER,TAX_PERCENTAGE,TAX_AMOUNT,TAX_AMOUNT_INGL_CURR,TAXCLASSIFICATION_DESCRIPTION,TAXCLASSIFICATION_ID,TAXCLASSIFICATION_RECORD_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,GREENBOOK,GREENBOOK_RECORD_ID,NET_PRICE,NET_PRICE_INGL_CURR,PLANT_ID,PLANT_NAME,PLANT_RECORD_ID,COMVAL_INGL_CURR,ESTVAL_INGL_CURR,NET_VALUE,NET_VALUE_INGL_CURR,UNIT_PRICE,UNIT_PRICE_INGL_CURR,QTEITMSUM_RECORD_ID,MODULE_ID,MODULE_NAME,MODULE_RECORD_ID,PARQTEITM_LINE,PARQTEITM_LINE_RECORD_ID,BILLING_TYPE,COMMITTED_VALUE,ESTIMATED_VALUE,SPLIT_PERCENT,SPLIT,STATUS,QUOTE_REVISION_CONTRACT_ITEM_ID) 
        SELECT A.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REVISION_CONTRACT_ITEM_ID FROM (
    SELECT DISTINCT CONTRACT_VALID_FROM,CONTRACT_VALID_TO,DOC_CURRENCY,DOCURR_RECORD_ID,EXCHANGE_RATE,EXCHANGE_RATE_DATE,EXCHANGE_RATE_RECORD_ID,GL_ACCOUNT_NO,GLOBAL_CURRENCY,GLOBAL_CURRENCY_RECORD_ID,(({equipments_count} + ROW_NUMBER()OVER(ORDER BY(SAQRIT.CpqTableEntryId))) * {item_number_saqrit_inc}) AS LINE,OBJECT_ID,OBJECT_TYPE,'{splitservice_name}' as SERVICE_DESCRIPTION,'{splitservice_id}' as SERVICE_ID,'{splitservice_recid}' as SERVICE_RECORD_ID,PROFIT_CENTER,QUANTITY,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,REF_SALESORDER,TAX_PERCENTAGE,TAX_AMOUNT,TAX_AMOUNT_INGL_CURR,TAXCLASSIFICATION_DESCRIPTION,TAXCLASSIFICATION_ID,TAXCLASSIFICATION_RECORD_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,GREENBOOK,GREENBOOK_RECORD_ID,NET_PRICE ,NET_PRICE_INGL_CURR,PLANT_ID,PLANT_NAME,PLANT_RECORD_ID,COMVAL_INGL_CURR,ESTVAL_INGL_CURR,NET_VALUE ,NET_VALUE_INGL_CURR,UNIT_PRICE,UNIT_PRICE_INGL_CURR,QTEITMSUM_RECORD_ID,MODULE_ID,MODULE_NAME,MODULE_RECORD_ID,LINE AS PARQTEITM_LINE,QUOTE_REVISION_CONTRACT_ITEM_ID AS PARQTEITM_LINE_RECORD_ID,BILLING_TYPE,COMMITTED_VALUE,ESTIMATED_VALUE,SPLIT_PERCENT,SPLIT, 'ACQUIRED' as STATUS FROM SAQRIT WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_rec_id}' AND SERVICE_ID = '{seid}' AND SPLIT ='')A""".format(contract_quote_rec_id = contract_quote_rec_id , quote_revision_rec_id = quote_revision_rec_id,item_number_saqrit_inc =item_number_saqrit_inc,equipments_count =equipments_count,splitservice_recid = splitservice_recid,splitservice_id=splitservice_id,splitservice_name = splitservice_name,seid = seid))
    
    update_pricing = SqlHelper.GetFirst("sp_executesql @T=N'UPDATE A SET A.NET_PRICE = (CASE WHEN ISNULL(A.PARQTEITM_LINE_RECORD_ID,'''')='''' AND ISNULL(A.PARQTEITM_LINE,'''') = '''' THEN NET_PRICE * XY.SPLIT_PERCENT/100 WHEN A.PARQTEITM_LINE_RECORD_ID <> A.QUOTE_REVISION_CONTRACT_ITEM_ID AND ISNULL(A.PARQTEITM_LINE,'''') <> ''''  and ISNULL(A.PARQTEITM_LINE_RECORD_ID,'''') <> '''' THEN NET_PRICE * (100-XY.SPLIT_PERCENT)/100 END),A.NET_PRICE_INGL_CURR = (CASE WHEN ISNULL(A.PARQTEITM_LINE_RECORD_ID,'''')='''' AND ISNULL(A.PARQTEITM_LINE,'''') = '''' THEN NET_PRICE_INGL_CURR * XY.SPLIT_PERCENT/100 WHEN A.PARQTEITM_LINE_RECORD_ID <> A.QUOTE_REVISION_CONTRACT_ITEM_ID AND ISNULL(A.PARQTEITM_LINE,'''') <> ''''  and ISNULL(A.PARQTEITM_LINE_RECORD_ID,'''') <> '''' THEN NET_PRICE_INGL_CURR * (100-XY.SPLIT_PERCENT)/100 END),A.NET_VALUE = (CASE WHEN ISNULL(A.PARQTEITM_LINE_RECORD_ID,'''')='''' AND ISNULL(A.PARQTEITM_LINE,'''') = '''' THEN NET_PRICE * XY.SPLIT_PERCENT/100 WHEN A.PARQTEITM_LINE_RECORD_ID <> A.QUOTE_REVISION_CONTRACT_ITEM_ID AND ISNULL(A.PARQTEITM_LINE,'''') <> ''''  and ISNULL(A.PARQTEITM_LINE_RECORD_ID,'''') <> '''' THEN NET_PRICE * (100-XY.SPLIT_PERCENT)/100 END) + TAX_AMOUNT,A.NET_VALUE_INGL_CURR = (CASE WHEN ISNULL(A.PARQTEITM_LINE_RECORD_ID,'''')='''' AND ISNULL(A.PARQTEITM_LINE,'''') = '''' THEN NET_PRICE_INGL_CURR * XY.SPLIT_PERCENT/100 WHEN A.PARQTEITM_LINE_RECORD_ID <> A.QUOTE_REVISION_CONTRACT_ITEM_ID AND ISNULL(A.PARQTEITM_LINE,'''') <> ''''  and ISNULL(A.PARQTEITM_LINE_RECORD_ID,'''') <> '''' THEN NET_PRICE_INGL_CURR * (100-XY.SPLIT_PERCENT)/100 END) + TAX_AMOUNT,A.SPLIT = ''YES'',A.SPLIT_PERCENT = (CASE WHEN ISNULL(A.PARQTEITM_LINE_RECORD_ID,'''')='''' AND ISNULL(A.PARQTEITM_LINE,'''') = '''' THEN XY.SPLIT_PERCENT WHEN A.PARQTEITM_LINE_RECORD_ID <> A.QUOTE_REVISION_CONTRACT_ITEM_ID AND ISNULL(A.PARQTEITM_LINE,'''') <> ''''  and ISNULL(A.PARQTEITM_LINE_RECORD_ID,'''') <> '''' THEN 100-XY.SPLIT_PERCENT END),A.UNIT_PRICE_INGL_CURR = (CASE WHEN A.PARQTEITM_LINE_RECORD_ID <> A.QUOTE_REVISION_CONTRACT_ITEM_ID AND ISNULL(A.PARQTEITM_LINE,'''') <> ''''  and ISNULL(A.PARQTEITM_LINE_RECORD_ID,'''') <> '''' THEN NET_PRICE_INGL_CURR * (100-XY.SPLIT_PERCENT)/100 END),A.UNIT_PRICE = (CASE WHEN A.PARQTEITM_LINE_RECORD_ID <> A.QUOTE_REVISION_CONTRACT_ITEM_ID AND ISNULL(A.PARQTEITM_LINE,'''') <> ''''  and ISNULL(A.PARQTEITM_LINE_RECORD_ID,'''') <> '''' THEN NET_PRICE * (100-XY.SPLIT_PERCENT)/100 END) FROM SAQRIT(NOLOCK)A INNER JOIN(SELECT DISTINCT B.SPLIT_PERCENT,B.QUOTE_RECORD_ID,B.QTEREV_RECORD_ID,B.GREENBOOK FROM SAQRIT B(NOLOCK) WHERE B.QUOTE_RECORD_ID = ''"+str(contract_quote_rec_id)+"'' AND B.SERVICE_ID = ''"+str(seid)+"'') AS XY ON A.QUOTE_RECORD_ID = XY.QUOTE_RECORD_ID AND A.QTEREV_RECORD_ID = XY.QTEREV_RECORD_ID AND A.GREENBOOK = XY.GREENBOOK WHERE A.QUOTE_RECORD_ID = ''"+str(contract_quote_rec_id)+"'' AND A.SPLIT <> ''YES'' '".format(contract_quote_rec_id =contract_quote_rec_id,seid =seid))
    #summary update
    update_service_parent_summary = """UPDATE A  SET A.NET_PRICE = B.NET_PRICE,A.NET_PRICE_INGL_CURR = B.NET_PRICE_INGL_CURR,A.NET_VALUE = B.NET_VALUE,A.NET_VALUE_INGL_CURR = B.NET_VALUE_INGL_CURR,A.UNIT_PRICE = B.UNIT_PRICE,A.UNIT_PRICE_INGL_CURR = B.UNIT_PRICE_INGL_CURR FROM SAQRIS A(NOLOCK) JOIN (SELECT SUM(NET_PRICE) AS NET_PRICE,SUM(NET_PRICE_INGL_CURR) AS NET_PRICE_INGL_CURR,SUM(NET_VALUE) AS NET_VALUE,SUM(NET_VALUE_INGL_CURR) AS NET_VALUE_INGL_CURR,SUM(UNIT_PRICE) AS UNIT_PRICE,SUM(UNIT_PRICE_INGL_CURR) AS UNIT_PRICE_INGL_CURR,QUOTE_RECORD_ID,QTEREV_RECORD_ID,SERVICE_ID from SAQRIT(NOLOCK) WHERE QUOTE_RECORD_ID ='{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_rec_id}'  AND SERVICE_ID = '{seid}' GROUP BY QUOTE_RECORD_ID,QTEREV_RECORD_ID,SERVICE_ID) B ON A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.SERVICE_ID=B.SERVICE_ID AND A.QTEREV_RECORD_ID = B.QTEREV_RECORD_ID """.format(contract_quote_rec_id= contract_quote_rec_id,quote_revision_rec_id = quote_revision_rec_id,seid =seid)
    Sql.RunQuery(update_service_parent_summary)
    update_service_child_summary = """UPDATE A  SET A.NET_PRICE = B.NET_PRICE,A.NET_PRICE_INGL_CURR = B.NET_PRICE_INGL_CURR,A.NET_VALUE = B.NET_VALUE,A.NET_VALUE_INGL_CURR = B.NET_VALUE_INGL_CURR,A.UNIT_PRICE = B.UNIT_PRICE,A.UNIT_PRICE_INGL_CURR = B.UNIT_PRICE_INGL_CURR FROM SAQRIS A(NOLOCK) JOIN (SELECT SUM(NET_PRICE) AS NET_PRICE,SUM(NET_PRICE_INGL_CURR) AS NET_PRICE_INGL_CURR,SUM(NET_VALUE) AS NET_VALUE,SUM(NET_VALUE_INGL_CURR) AS NET_VALUE_INGL_CURR,SUM(UNIT_PRICE) AS UNIT_PRICE,SUM(UNIT_PRICE_INGL_CURR) AS UNIT_PRICE_INGL_CURR,QUOTE_RECORD_ID,QTEREV_RECORD_ID,SERVICE_ID from SAQRIT(NOLOCK) WHERE QUOTE_RECORD_ID ='{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_rec_id}'  AND SERVICE_ID = '{splitservice_id}' GROUP BY QUOTE_RECORD_ID,QTEREV_RECORD_ID,SERVICE_ID) B ON A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.SERVICE_ID=B.SERVICE_ID AND A.QTEREV_RECORD_ID = B.QTEREV_RECORD_ID """.format(contract_quote_rec_id= contract_quote_rec_id,quote_revision_rec_id = quote_revision_rec_id,seid =seid,splitservice_id =splitservice_id)
    Sql.RunQuery(update_service_child_summary)
    saqrioinsert ="""MERGE SAQRIO SRC USING (SELECT A.QUOTE_REVISION_ITEM_OBJECT_RECORD_ID,A.CUSTOMER_TOOL_ID,A.EQUIPMENT_DESCRIPTION,A.EQUIPMENT_ID,A.EQUIPMENT_RECORD_ID,A.GREENBOOK,A.GREENBOOK_RECORD_ID,A.KPU,B.LINE,B.SERVICE_DESCRIPTION,B.SERVICE_ID,B.SERVICE_RECORD_ID,A.QUOTE_ID,A.QTEITM_RECORD_ID,A.QUOTE_RECORD_ID,A.QTEREV_ID,A.QTEREV_RECORD_ID,A.SERIAL_NUMBER,A.TECHNOLOGY,A.TOOL_CONFIGURATION,A.WAFER_SIZE,B.QUOTE_REVISION_CONTRACT_ITEM_ID FROM SAQRIO(NOLOCK) A JOIN SAQRIT (NOLOCK) B ON A.QUOTE_RECORD_ID  = B.QUOTE_RECORD_ID AND A.LINE = B.PARQTEITM_LINE where B.QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND B.QTEREV_RECORD_ID  = '{quote_revision_rec_id}' AND B.SERVICE_ID = '{splitservice_id}')
    TGT ON (SRC.QUOTE_RECORD_ID = TGT.QUOTE_RECORD_ID AND SRC.QTEREV_RECORD_ID = TGT.QTEREV_RECORD_ID AND SRC.SERVICE_ID = '{splitservice_id}')
    WHEN NOT MATCHED BY TARGET
    THEN INSERT(QUOTE_REVISION_ITEM_OBJECT_RECORD_ID,CUSTOMER_TOOL_ID,EQUIPMENT_DESCRIPTION,EQUIPMENT_ID,EQUIPMENT_RECORD_ID,GREENBOOK,GREENBOOK_RECORD_ID,KPU,LINE,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,QUOTE_ID,QTEITM_RECORD_ID,QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,SERIAL_NUMBER,TECHNOLOGY,TOOL_CONFIGURATION,WAFER_SIZE)
    VALUES (NEWID(),CUSTOMER_TOOL_ID,EQUIPMENT_DESCRIPTION,EQUIPMENT_ID,EQUIPMENT_RECORD_ID,GREENBOOK,GREENBOOK_RECORD_ID,KPU,LINE,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,QUOTE_ID,QUOTE_REVISION_CONTRACT_ITEM_ID,QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,SERIAL_NUMBER,TECHNOLOGY,TOOL_CONFIGURATION,WAFER_SIZE);""".format(contract_quote_rec_id=contract_quote_rec_id,quote_revision_rec_id = quote_revision_rec_id,splitservice_id =splitservice_id )
    Sql.RunQuery(saqrioinsert)
splitserviceinsert()

#===================================================================================================================#======================
#   __script_name : CQREVISION.PY
#   __script_description : THIS SCRIPT IS USED TO CREATE NEW REVISIONS,EDIT REVISIONS AND UPDATE CUSTOM TABLES
#   __primary_author__ : SRIJAYDHURGA
#   __create_date :08/30/2021
# #====================================================================================================================#======================
import Webcom.Configurator.Scripting.Test.TestProduct
import datetime
import time
from SYDATABASE import SQL
import clr
import sys
import System.Net
from System.Text.Encoding import UTF8
from System import Convert
import re
from datetime import datetime, timedelta
import SYTABACTIN as Table
import SYCNGEGUID as CPQID
import CQCPQC4CWB
import CQREVSTSCH
Sql = SQL()
ScriptExecutor = ScriptExecutor
# When we create a new revision for existing quote from C4C, quote edit is taking some time. So if quote is not edited in backend, we do again here.
if not Quote:
    
    try:
        Quote = QuoteHelper.Edit(Param.QuoteId)
    except Exception:
        Trace.Write("========>>> Quote is edit error")
try:
    quote_contract_recordId = Quote.GetGlobal("contract_quote_record_id")
except:
    quote_contract_recordId = ''
Trace.Write('23----test'+str(quote_contract_recordId))
#A055S000P01-8729 start
def create_new_revision(Opertion,cartrev):
    #INC08621140- Removed SAQSAP,SAQSKP,SAQGPM,SAQGPA,SAQGPE,SAQRGG from cloning dict since calling we are real time integration for these insertion
    cloneobject={
        "SAQFBL":"QUOTE_FABLOCATION_RECORD_ID",
        "SAQFEQ":"QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID",
        "SAQTSV":"QUOTE_SERVICE_RECORD_ID",
        "SAQTSE":"QUOTE_SERVICE_ENTITLEMENT_RECORD_ID",
        "SAQSCO":"QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID",
        "SAQSCA":"QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID",
        "SAQSCE":"QUOTE_SERVICE_COVERED_OBJ_ENTITLEMENTS_RECORD_ID",
        "SAQSGE":"QUOTE_SERVICE_GREENBOOK_ENTITLEMENT_RECORD_ID",
        "SAQSAE":"QUOTE_SERVICE_COV_OBJ_ASS_ENT_RECORD_ID",
        "SAQSGB":"QUOTE_SERVICE_GREENBOOK_RECORD_ID",
        "SAQSPT":"QUOTE_SERVICE_PART_RECORD_ID",
        "SAQSRA":"QUOTE_SENDING_RECEIVING_ACCOUNT",
        "SAQSSE":"QUOTE_SERVICE_SENDING_FAB_LOC_EQUIP_ID",
        "SAQSSA":"QUOTE_SERVICE_SENDING_FAB_EQUIP_ASS_ID",
        "SAQFEA":"QUOTE_FAB_LOC_COV_OBJ_ASSEMBLY_RECORD_ID",
        "SAQFGB":"QUOTE_FAB_LOC_GB_RECORD_ID",
        "SAQSFB":"QUOTE_SERVICE_FAB_LOCATION_RECORD_ID",
        "SAQSSF":"QUOTE_SERVICE_SENDING_FAB_LOC_ID",
        "SAQCBC":"QUOTE_REV_CLEAN_BOOKING_CHECKLIST_ID",
        "SAQDLT":"QUOTE_REV_DEAL_TEAM_MEMBER_ID",
        "SAQTIP":"QUOTE_INVOLVED_PARTY_RECORD_ID",
        "SAQICT":"QUOTE_REV_INVOLVED_PARTY_CONTACT_ID",
        "SAQRDS":"QUOTE_REV_DELIVERY_SCHEDULE_RECORD_ID",	
        "SAQSAO":"QUOTE_SERVICE_ADD_ON_PRODUCT_RECORD_ID",
        "SAQSCN":"QUOTE_REV_PO_EQUIPMENT_PARTS_RECORD_ID",
        "SAQRSP":"QUOTE_REV_PO_PRODUCT_LIST_ID",
        "SAQTDA":"QUOTE_REV_TOOL_IDLING_ATTR_VAL_RECORD_ID",
        }
    
    #"SAQSAP":"QUOTE_SERVICE_COV_OBJ_ASS_PM_KIT_RECORD_ID",
    # "SAQRGG":"QUOTE_REV_PO_GREENBOOK_GOT_CODES_RECORD_ID",
    # "SAQSKP":"QUOTE_SERVICE_COV_OBJ_ASS_PM_KIT_PARTS_RECORD_ID",
    # "SAQGPM":"QUOTE_REV_PO_GBK_GOT_CODE_PM_EVENTS_RECORD_ID",
    # "SAQGPA":"QUOTE_REV_PO_GRNBK_PM_EVEN_ASSEMBLIES_RECORD_ID",
    # "SAQGPE":"QUOTE_REV_GOT_CD_PM_EVNT_ENTITLEMENTS_RECORD_ID",
    #"SAQIBP":"QUOTE_ITEM_BILLING_PLAN_RECORD_ID"
    # "SAQITM":"QUOTE_ITEM_RECORD_ID",
    # "SAQIFL":"QUOTE_ITEM_FAB_LOCATION_RECORD_ID",
    # "SAQIGB":"QUOTE_ITEM_GREENBOOK_RECORD_ID",
    # "SAQIAP":"QUOTE_ITEM_COV_OBJ_ASS_PM_RECORD_ID",
    # "SAQICA":"QUOTE_ITEM_COVERED_OBJECT_ASSEMBLY_RECORD_ID",
    # "SAQIPE":"QUOTE_ITEM_FORECAST_PART_ENT_RECORD_ID",
    # "SAQIFP":"QUOTE_ITEM_FORECAST_PART_RECORD_ID"
    # "SAQGPM":"QUOTE_REV_PO_GBK_GOT_CODE_PM_EVENTS_RECORD_ID",
    # "SAQGPA":"QUOTE_REV_PO_GRNBK_PM_EVEN_ASSEMBLIES_RECORD_ID",
    # "SAQGPE":"QUOTE_REV_GOT_CD_PM_EVNT_ENTITLEMENTS_RECORD_ID",
    # "SAQSKP":"QUOTE_SERVICE_COV_OBJ_ASS_PM_KIT_PARTS_RECORD_ID",
    if Quote is not None:
        global quote_contract_recordId
        if not quote_contract_recordId:
            get_rev_info = Sql.GetFirst("SELECT QTEREV_ID,QTEREV_RECORD_ID,MASTER_TABLE_QUOTE_RECORD_ID FROM SAQTMT (NOLOCK) WHERE C4C_QUOTE_ID='" + str(Param.QuoteId) + "'")
            if get_rev_info:
                try:
                    quote_contract_recordId = get_rev_info.MASTER_TABLE_QUOTE_RECORD_ID
                    Quote.SetGlobal("contract_quote_record_id", str(get_rev_info.MASTER_TABLE_QUOTE_RECORD_ID))
                    Quote.SetGlobal("quote_revision_record_id",str(get_rev_info.QTEREV_RECORD_ID))
                    Quote.SetGlobal("quote_revision_id",str(get_rev_info.QTEREV_ID))
                except Exception:
                    pass
        get_quote_info_details = Sql.GetFirst("select * from SAQTMT where MASTER_TABLE_QUOTE_RECORD_ID = '"+str(quote_contract_recordId)+"'")
        #Get Old Revision ID - Start
        get_old_revision_id = Sql.GetFirst("SELECT QTEREV_ID FROM SAQTRV WHERE ACTIVE='True' AND QUOTE_RECORD_ID= '"+str(quote_contract_recordId)+"'")
        Trace.Write(get_old_revision_id.QTEREV_ID)
        old_revision_no=get_old_revision_id.QTEREV_ID
        #Get Old Revision ID - END

        #create new revision start
        #edit_new_rev_quote = QuoteHelper.Edit(Quote.CompositeNumber)
        create_new_rev = Quote.CreateNewRevision(True)
        Quote.SetGlobal("contract_quote_record_id",quote_contract_recordId)
        #composite_number = create_new_rev.CompositeNumber
        current_revison = Quote.RevisionNumber
        Trace.Write("============>> "+str(current_revison))
        #craete new revision ends
        get_quote_id = create_new_rev.QuoteId
        #create new revision -SAQTRV - update-start
        quote_revision_table_info = Sql.GetTable("SAQTRV")
        quote_revision_id = str(Guid.NewGuid()).upper()
        Quote.SetGlobal("quote_revision_record_id",str(quote_revision_id))
        get_current_rev = Sql.GetFirst("select MAX(QTEREV_ID) as rev_id from SAQTRV where QUOTE_RECORD_ID = '"+str(quote_contract_recordId)+"'")
        
        get_previous_rev_data = Sql.GetFirst("select * from SAQTRV where QUOTE_RECORD_ID = '"+str(quote_contract_recordId)+"' AND ACTIVE = 1")
        #Hadoop fix - Start - A
        update_quote_rev = Sql.RunQuery("""UPDATE SAQTRV SET ACTIVE = {active_rev} WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND ACTIVE = 1 """.format(QuoteRecordId=quote_contract_recordId,active_rev = 0))
        #Hadoop fix - End - A
        newrev_inc = int(get_current_rev.rev_id)+1

        get_rev_details = Sql.GetFirst("SELECT DISTINCT TOP 1 CART2.CARTCOMPOSITENUMBER, CART_REVISIONS.REVISION_ID, CART_REVISIONS.DESCRIPTION as DESCRIPTION,CART.ACTIVE_REV, CART_REVISIONS.CART_ID, CART_REVISIONS.PARENT_ID, CART.USERID FROM CART_REVISIONS (nolock) INNER JOIN CART2 (nolock) ON CART_REVISIONS.CART_ID = CART2.CartId INNER JOIN CART(NOLOCK) ON CART.CART_ID = CART2.CartId WHERE CART2.CARTCOMPOSITENUMBER = '{}'  and REVISION_ID  = '{}' ".format(Quote.CompositeNumber,newrev_inc))
        #INC08614363 - M
        get_exchgrate = Sql.GetFirst("SELECT SDFI_EXCHRATE FROM SASAAC (NOLOCK) WHERE ACCOUNT_ID = '{}' AND DISTRIBUTIONCHANNEL_ID = '{}' AND DIVISION_ID = '{}' AND SALESORG_ID = '{}' ".format(Quote.GetCustomField('STPAccountID').Content,get_previous_rev_data.DISTRIBUTIONCHANNEL_ID,get_previous_rev_data.DIVISION_ID,get_previous_rev_data.SALESORG_ID))
        if get_exchgrate.SDFI_EXCHRATE:
            exchange_rate = Sql.GetFirst("SELECT EXCRATTYP_ID FROM PRERTY (NOLOCK) WHERE SDFI_EXCHRATE = '{}' ".format(get_exchgrate.SDFI_EXCHRATE))
            exchange_ratetyp = exchange_rate.EXCRATTYP_ID
        else:
            exchange_ratetyp = 'M'
        #HPQC 1642 start
        exchange_obj = Sql.GetFirst("SELECT EXCHANGE_RATE,RATIO_FROM,RATIO_TO,EXCHANGE_RATE_BEGIN_DATE,EXCHANGE_RATE_END_DATE,EXCHANGE_RATE_RECORD_ID from PREXRT where FROM_CURRENCY = '{}' and TO_CURRENCY='{}' AND ACTIVE = 1 and EXCHANGE_RATE_TYPE = '{}'".format(get_previous_rev_data.GLOBAL_CURRENCY,get_previous_rev_data.DOC_CURRENCY,exchange_ratetyp))
        #INC08614363 - M
        if exchange_obj:
            if exchange_obj.RATIO_FROM > 1:
                exchange_val = exchange_obj.EXCHANGE_RATE/exchange_obj.RATIO_FROM
            elif exchange_obj.RATIO_TO > 1:
                exchange_val = exchange_obj.EXCHANGE_RATE*exchange_obj.RATIO_TO
            else:
                exchange_val = exchange_obj.EXCHANGE_RATE
        else:
            #INC08614363 - M
            if get_previous_rev_data.GLOBAL_CURRENCY == get_previous_rev_data.DOC_CURRENCY:
                exchange_val = 1.00
            else:
                exchange_val = ''
            #INC08614363 - M
        #HPQC 1642 end
        current_date = datetime.now()
        end_date = current_date + timedelta(days=365)
        if get_previous_rev_data:
            quote_rev_data = {
                "QUOTE_REVISION_RECORD_ID": str(quote_revision_id),
                "QUOTE_ID": get_quote_info_details.QUOTE_ID,
                "REVISION_DESCRIPTION": "REVISION {newrev_inc} DESCRIPTION".format(newrev_inc=newrev_inc),
                "REVISION_NAME":get_previous_rev_data.REVISION_NAME,			
                "QUOTE_RECORD_ID": quote_contract_recordId,
                "ACTIVE":1,
                "REV_CREATE_DATE":current_date.strftime('%m/%d/%Y'),
                "REV_EXPIRE_DATE":'',
                "REVISION_STATUS":"CFG-CONFIGURING",
                "WORKFLOW_STATUS": "CONFIGURE",
                "QTEREV_ID":newrev_inc,
                "QTEREV_RECORD_ID":quote_revision_id, 
                "REV_APPROVE_DATE":'',
                "CART_ID":get_quote_id,
                "SALESORG_ID": get_previous_rev_data.SALESORG_ID,
                "COUNTRY": get_previous_rev_data.COUNTRY,
                "COUNTRY_NAME": get_previous_rev_data.COUNTRY_NAME,
                "COUNTRY_RECORD_ID":get_previous_rev_data.COUNTRY_RECORD_ID,
                "REGION":get_previous_rev_data.REGION,
                "SALESORG_NAME": get_previous_rev_data.SALESORG_NAME,
                "SALESORG_RECORD_ID": get_previous_rev_data.SALESORG_RECORD_ID,							
                "GLOBAL_CURRENCY":get_previous_rev_data.GLOBAL_CURRENCY,							
                "GLOBAL_CURRENCY_RECORD_ID":get_previous_rev_data.GLOBAL_CURRENCY,
                "SALESOFFICE_ID":get_previous_rev_data.SALESOFFICE_ID,
                "SALESOFFICE_NAME":get_previous_rev_data.SALESOFFICE_NAME,
                "SALESOFFICE_RECORD_ID":get_previous_rev_data.SALESOFFICE_RECORD_ID,
                "DIVISION_ID" : get_previous_rev_data.DIVISION_ID,
                "DISTRIBUTIONCHANNEL_RECORD_ID" :get_previous_rev_data.DISTRIBUTIONCHANNEL_RECORD_ID,
                "DIVISION_RECORD_ID" : get_previous_rev_data.DIVISION_RECORD_ID,
                "DOC_CURRENCY" : get_previous_rev_data.DOC_CURRENCY,
                "DOCCURR_RECORD_ID" : get_previous_rev_data.DOCCURR_RECORD_ID,
                "DOCTYP_ID":get_previous_rev_data.DOCTYP_ID,
                "DOCTYP_RECORD_ID":get_previous_rev_data.DOCTYP_RECORD_ID,
                "DOCUMENT_PRICING_PROCEDURE" : get_previous_rev_data.DOCUMENT_PRICING_PROCEDURE,
                "DISTRIBUTIONCHANNEL_ID" : get_previous_rev_data.DISTRIBUTIONCHANNEL_ID,
                "EXCHANGE_RATE" : exchange_val,
                "EXCHANGE_RATE_DATE" : datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"),
                "EXCHANGE_RATE_TYPE" : exchange_ratetyp,#INC08614363 - M
                "EXCHANGERATE_RECORD_ID" : get_previous_rev_data.EXCHANGERATE_RECORD_ID,
                "GLOBAL_CURRENCY" : get_previous_rev_data.GLOBAL_CURRENCY,
                "GLOBAL_CURRENCY_RECORD_ID" : get_previous_rev_data.GLOBAL_CURRENCY_RECORD_ID,
                "INCOTERM_ID" : get_previous_rev_data.INCOTERM_ID,
                "INCOTERM_NAME" : get_previous_rev_data.INCOTERM_NAME,
                "INCOTERM_RECORD_ID" : get_previous_rev_data.INCOTERM_RECORD_ID,
                "INCOTERM_LOCATION" : get_previous_rev_data.INCOTERM_LOCATION,
                "BLUEBOOK" : get_previous_rev_data.BLUEBOOK,
                "BLUEBOOK_RECORD_ID" : get_previous_rev_data.BLUEBOOK_RECORD_ID,
                "MODUSR_RECORD_ID" : get_previous_rev_data.MODUSR_RECORD_ID,
                "PAYMENTTERM_DAYS" : get_previous_rev_data.PAYMENTTERM_DAYS,
                "PAYMENTTERM_ID" : get_previous_rev_data.PAYMENTTERM_ID,
                "PAYMENTTERM_NAME" : get_previous_rev_data.PAYMENTTERM_NAME,
                "PAYMENTTERM_RECORD_ID" : get_previous_rev_data.PAYMENTTERM_RECORD_ID,
                "QT_PAYMENTTERM_DAYS": get_previous_rev_data.QT_PAYMENTTERM_DAYS,#INC08726687
                "QT_PAYMENTTERMS_ID": get_previous_rev_data.QT_PAYMENTTERMS_ID,#INC08726687
                "QT_PAYMENTTERM_NAME": get_previous_rev_data.QT_PAYMENTTERM_NAME,#INC08726687
                "PRICINGPROCEDURE_ID" : get_previous_rev_data.PRICINGPROCEDURE_ID,
                "PRICINGPROCEDURE_NAME" : get_previous_rev_data.PRICINGPROCEDURE_NAME,
                "PRICINGPROCEDURE_RECORD_ID" :get_previous_rev_data.PRICINGPROCEDURE_RECORD_ID,
                "ACCTAXCAT_ID": get_previous_rev_data.ACCTAXCAT_ID,
                "ACCTAXCAT_DESCRIPTION" : get_previous_rev_data.ACCTAXCAT_DESCRIPTION,
                "ACCTAXCLA_DESCRIPTION" : get_previous_rev_data.ACCTAXCLA_DESCRIPTION,
                "ACCTAXCLA_ID" : get_previous_rev_data.ACCTAXCLA_ID,
                "CANCELLATION_PERIOD_NOTPER" : get_previous_rev_data.CANCELLATION_PERIOD_NOTPER,
                "PRICELIST_DESCRIPTION" : get_previous_rev_data.PRICELIST_DESCRIPTION,
                "PRICELIST_ID" : get_previous_rev_data.PRICELIST_ID,
                "CANCELLATION_PERIOD":"180",
                "CANCELLATION_PERIOD_NOTPER":"",
                "CONTRACT_VALID_FROM":get_previous_rev_data.CONTRACT_VALID_FROM,
                "CONTRACT_VALID_TO":get_previous_rev_data.CONTRACT_VALID_TO,
                "COMPANY_ID":get_previous_rev_data.COMPANY_ID,
                "COMPANY_NAME":get_previous_rev_data.COMPANY_NAME,
                "COMPANY_RECORD_ID":get_previous_rev_data.COMPANY_RECORD_ID,
                "CLM_CONTRACT_TYPE":get_previous_rev_data.CLM_CONTRACT_TYPE,
                "CLM_TEMPLATE_NAME":get_previous_rev_data.CLM_TEMPLATE_NAME,
                "APPLIED_EMAIL":get_previous_rev_data.APPLIED_EMAIL,
                "APPLIED_NAME":get_previous_rev_data.APPLIED_NAME,
                "APPLIED_TITLE":get_previous_rev_data.APPLIED_TITLE,
                "EXTERNAL_EMAIL":get_previous_rev_data.EXTERNAL_EMAIL,
                "EXTERNAL_NAME":get_previous_rev_data.EXTERNAL_NAME,
                "EXTERNAL_TITLE":get_previous_rev_data.EXTERNAL_TITLE,
                "HLV_ORG_BUN":"AGS - SSC",
                "TRANSACTION_TYPE":get_previous_rev_data.TRANSACTION_TYPE,
                "BANK_ID":get_previous_rev_data.BANK_ID,
                "BANK_NAME":get_previous_rev_data.BANK_NAME,
                "BANK_RECORD_ID":get_previous_rev_data.BANK_RECORD_ID
            }

        quote_revision_table_info.AddRow(quote_rev_data)
        Sql.Upsert(quote_revision_table_info)
        Quote.GetCustomField('QUOTE_REVISION_DESC').Content  = "REVISION {newrev_inc} DESCRIPTION".format(newrev_inc=newrev_inc)
        Quote.GetCustomField('QUOTE_EXCHANGE_RATE').Content = str(get_previous_rev_data.EXCHANGE_RATE)
        Quote.GetCustomField('QUOTE_PAYMENT_TERM').Content = get_previous_rev_data.PAYMENTTERM_NAME
        #create new revision -SAQTRV - update-end
        #get quote data for update in SAQTMT start

        ##Calling the iflow for quote header writeback to cpq to c4c code starts..
        #INC08656425 M
        try:
            CQCPQC4CWB.writeback_to_c4c("quote_header",Quote.GetGlobal("contract_quote_record_id"),Quote.GetGlobal("quote_revision_record_id"))
            CQCPQC4CWB.writeback_to_c4c("opportunity_header",Quote.GetGlobal("contract_quote_record_id"),Quote.GetGlobal("quote_revision_record_id"))
        except Exception as e:
            Log.Info("EXCEPTION: CPI CALL FAILED TO SEND DATA TO c4c" + str(e))
        ##Calling the iflow for quote header writeback to cpq to c4c code ends...
        
        quote_table_info = Sql.GetTable("SAQTMT")
        if get_quote_info_details:
            quote_detials = ''
            #update SAQTMT start
            
            Sql.RunQuery("""UPDATE SAQTMT SET QTEREV_ID = {newrev_inc},QTEREV_RECORD_ID = '{quote_revision_id}',ACTIVE_REV={active_rev},CONTRACT_VALID_FROM = '{contract_valid_from}',CONTRACT_VALID_TO='{contract_valid_to}' WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{QuoteRecordId}'""".format(quote_revision_id=quote_revision_id,newrev_inc= newrev_inc,QuoteRecordId=quote_contract_recordId,active_rev = 1,contract_valid_from =get_quote_info_details.CONTRACT_VALID_FROM,contract_valid_to =get_quote_info_details.CONTRACT_VALID_TO))
            #update SAQTMT end
            
            ##Calling the iflow for quote header writeback to cpq to c4c code starts..
            Log.Info("===> writeback_to_c4c calling from new Revision===> ")
            #INC08656425 M
            try:
                CQCPQC4CWB.writeback_to_c4c("quote_header",Quote.GetGlobal("contract_quote_record_id"),quote_revision_id)
                CQCPQC4CWB.writeback_to_c4c("opportunity_header",Quote.GetGlobal("contract_quote_record_id"),quote_revision_id)
            except Exception as e:
                Log.Info("EXCEPTION: CPI CALL FAILED TO SEND DATA TO c4c in Quote" + str(e))
            ##Calling the iflow for quote header writeback to cpq to c4c code ends...
            
            #update SAQTIP start
            # Sql.RunQuery("""UPDATE SAQTIP SET QTEREV_ID = {newrev_inc},QTEREV_RECORD_ID = '{quote_revision_id}' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}'""".format(quote_revision_id=quote_revision_id,newrev_inc= newrev_inc,QuoteRecordId=quote_contract_recordId))
            #update SAQTIP end
            
            #CLONE ALL OBJECTS 
            for cloneobjectname in cloneobject.keys():
                insertval = 'INSERT INTO '+ str(cloneobjectname) +'( '
                selectval = "SELECT "
                sqlobj=Sql.GetList("""SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{}'""".format(str(cloneobjectname)))
                insertcols = ''
                selectcols = ''
                table_cols = []
                for col in sqlobj:
                    table_cols.append(col.COLUMN_NAME)
                    if col.COLUMN_NAME == cloneobject[cloneobjectname]:
                        insertcols =  str(col.COLUMN_NAME) if insertcols == '' else insertcols + "," + str(col.COLUMN_NAME)
                        selectcols = "CONVERT(VARCHAR(4000),NEWID()) AS " + str(col.COLUMN_NAME) if selectcols == '' else selectcols + ", CONVERT(VARCHAR(4000),NEWID()) AS " + str(col.COLUMN_NAME)
                    elif col.COLUMN_NAME == "QTEREV_ID":
                        insertcols = str(col.COLUMN_NAME) if insertcols == '' else insertcols + "," + str(col.COLUMN_NAME)
                        selectcols =  "{} AS ".format(int(newrev_inc)) + str(col.COLUMN_NAME) if selectcols == '' else selectcols + ", {} AS ".format(int(newrev_inc)) + str(col.COLUMN_NAME)
                    elif col.COLUMN_NAME == "QTEREV_RECORD_ID":
                        insertcols = str(col.COLUMN_NAME) if insertcols == '' else insertcols + "," + str(col.COLUMN_NAME)
                        selectcols = "'{}' AS ".format(str(quote_revision_id)) + str(col.COLUMN_NAME) if selectcols == '' else selectcols + "," + "'{}' AS ".format(str(quote_revision_id)) + str(col.COLUMN_NAME)
                    elif (col.COLUMN_NAME == "CpqTableEntryId") or  (cloneobjectname == 'SAQRSP' and col.COLUMN_NAME  in ('EXTENDED_PRICE','UNIT_PRICE','EXTENDED_PRICE_INGL_CURR','UNIT_PRICE_INGL_CURR')):
                        continue
                    else:
                        insertcols = str(col.COLUMN_NAME) if insertcols == '' else insertcols + "," + str(col.COLUMN_NAME)
                        selectcols = str(col.COLUMN_NAME) if selectcols == '' else selectcols + "," + str(col.COLUMN_NAME)
                insertcols += " )"
                insertcols  = insertcols.replace("PRIMARY","[PRIMARY]")
                selectcols = selectcols.replace("PRIMARY","[PRIMARY]")
                # A055S000P01-17876 - Start
                service_level_where_condition = ''
                # if cloneobjectname == 'SAQTSV':
                #     service_level_where_condition = " AND SERVICE_ID != 'Z0105'"
                #INC09024172 - Start
                if 'SERVICE_ID' in table_cols:
                    service_level_where_condition = " AND SERVICE_ID != 'Z0105'"
                selectcols += " FROM "+ str(cloneobjectname) +" WHERE QUOTE_RECORD_ID='{}'".format(str(quote_contract_recordId))+" AND QTEREV_ID={}".format(int(old_revision_no)) + service_level_where_condition + "ORDER BY CpqTableEntryId"
                #INC09024172 - End
                # A055S000P01-17876 - End
                finalquery=insertval + insertcols +' '+ selectval + selectcols
                Trace.Write(finalquery)
                ExecObjQuery = Sql.RunQuery(finalquery)
                # Remove CBC details during clone
                if cloneobjectname == 'SAQCBC':
                    Sql.RunQuery("UPDATE SAQCBC SET SERVICE_CONTRACT = 'False', SPECIALIST_REVIEW = 'False' FROM SAQCBC WHERE QUOTE_RECORD_ID='{}' AND QTEREV_ID={}".format(quote_contract_recordId, newrev_inc))
                elif cloneobjectname == 'SAQSPT':
                    Sql.RunQuery("UPDATE SAQSPT SET CUSTOMER_ANNUAL_QUANTITY = NULL,EXTENDED_UNIT_PRICE = NULL,UNIT_PRICE = NULL, CORE_CREDIT_PRICE=NULL,PRICING_STATUS='NOT PRICED' ,DELIVERY_1 =NULL,DELIVERY_2 =NULL,DELIVERY_3 =NULL,DELIVERY_4 =NULL,DELIVERY_5 =NULL,DELIVERY_6 =NULL,DELIVERY_7 =NULL,DELIVERY_8 =NULL,DELIVERY_9 =NULL,DELIVERY_10 =NULL,DELIVERY_11 =NULL,DELIVERY_12 =NULL,DELIVERY_13 =NULL,DELIVERY_14 =NULL,DELIVERY_15 =NULL,DELIVERY_16 =NULL,DELIVERY_17 =NULL,DELIVERY_18 =NULL,DELIVERY_19 =NULL,DELIVERY_20 =NULL,DELIVERY_21 =NULL,DELIVERY_22 =NULL,DELIVERY_23 =NULL,DELIVERY_24 =NULL,DELIVERY_25 =NULL,DELIVERY_26 =NULL,DELIVERY_27 =NULL,DELIVERY_28 =NULL,DELIVERY_29 =NULL,DELIVERY_30 =NULL,DELIVERY_31 =NULL,DELIVERY_32 =NULL,DELIVERY_33 =NULL,DELIVERY_34 =NULL,DELIVERY_35 =NULL,DELIVERY_36 =NULL,DELIVERY_37 =NULL,DELIVERY_38 =NULL,DELIVERY_39 =NULL,DELIVERY_40 =NULL,DELIVERY_41 =NULL,DELIVERY_42 =NULL,DELIVERY_43 =NULL,DELIVERY_44 =NULL,DELIVERY_45 =NULL,DELIVERY_46 =NULL,DELIVERY_47 =NULL,DELIVERY_48 =NULL,DELIVERY_49 =NULL,DELIVERY_50 =NULL,DELIVERY_51 =NULL,DELIVERY_52 =NULL  FROM SAQSPT WHERE QUOTE_RECORD_ID='{}' AND QTEREV_ID={}".format(quote_contract_recordId, newrev_inc))                    
                elif cloneobjectname == 'SAQRSP':
                    Sql.RunQuery("UPDATE SAQRSP SET PRICING_STATUS='NOT PRICED',EXTENDED_PRICE = NULL,UNIT_PRICE = NULL,EXTENDED_PRICE_INGL_CURR = NULL ,QUANTITY = NULL,UNIT_PRICE_INGL_CURR = NULL FROM SAQRSP WHERE QUOTE_RECORD_ID='{}' AND QTEREV_ID={}".format(quote_contract_recordId, newrev_inc))
            #INC08971027 - Starts - M		
            #A055S000P01-20908 - Start - M
            ### SAQTSV (QUOTE_SERVICE_RECORD_ID) MAPPED INTO  SAQTSE (QTESRV_RECORD_ID):
            updatestatement_saqtse = """UPDATE B SET B.QTESRV_RECORD_ID = A.QUOTE_SERVICE_RECORD_ID FROM SAQTSV A JOIN SAQTSE B ON A.SERVICE_ID=B.SERVICE_ID AND A.QTEREV_RECORD_ID=B.QTEREV_RECORD_ID AND A.QUOTE_ID=B.QUOTE_ID  WHERE A.QTEREV_ID={} AND B.QTEREV_ID={} AND A.QUOTE_RECORD_ID=''{}'' AND B.QUOTE_RECORD_ID=''{}'' """.format(int(newrev_inc),int(newrev_inc),str(quote_contract_recordId),str(quote_contract_recordId))
            ##SAQSGE QTESRVGBK_RECORD_ID MAPPED FROM SAQSGB QUOTE_SERVICE_GREENBOOK_RECORD_ID
            updatestatement_saqsgb = """UPDATE B SET B.QTESRVGBK_RECORD_ID = A.QUOTE_SERVICE_GREENBOOK_RECORD_ID FROM SAQSGB A JOIN SAQSGE B ON A.GREENBOOK=B.GREENBOOK AND A.SERVICE_ID=B.SERVICE_ID AND A.QUOTE_ID=B.QUOTE_ID  AND A.QTEREV_ID = B.QTEREV_ID WHERE A.QTEREV_ID={} AND B.QTEREV_ID={} AND A.QUOTE_RECORD_ID=''{}'' AND B.QUOTE_RECORD_ID=''{}'' """.format(int(newrev_inc),int(newrev_inc),str(quote_contract_recordId),str(quote_contract_recordId))
            # SAQSCO (QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID) MAPPED INTO  SAQSCE (QTESRVCOB_RECORD_ID)
            updatestatement_saqsce = """UPDATE SAQSCE SET SAQSCE.QTESRVCOB_RECORD_ID =  SAQSCO.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID FROM SAQSCE (NOLOCK) INNER JOIN (SELECT QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,QUOTE_ID,QTEREV_ID,EQUIPMENT_ID,SERVICE_ID, QTEREVFEQ_RECORD_ID FROM SAQSCO (NOLOCK) WHERE SAQSCO.QTEREV_ID={old_rev} AND SAQSCO.QUOTE_RECORD_ID=''{quote_rec_id}'') OLD ON OLD.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID = SAQSCE.QTESRVCOB_RECORD_ID AND SAQSCE.QUOTE_ID=OLD.QUOTE_ID AND SAQSCE.EQUIPMENT_ID=OLD.EQUIPMENT_ID AND SAQSCE.SERVICE_ID=OLD.SERVICE_ID INNER JOIN SAQSCO (NOLOCK) ON SAQSCE.EQUIPMENT_ID=SAQSCO.EQUIPMENT_ID  AND SAQSCE.QUOTE_ID=SAQSCO.QUOTE_ID AND SAQSCE.QTEREV_RECORD_ID=SAQSCO.QTEREV_RECORD_ID AND SAQSCO.QTEREVFEQ_RECORD_ID = OLD.QTEREVFEQ_RECORD_ID AND SAQSCE.SERVICE_ID=SAQSCO.SERVICE_ID WHERE SAQSCE.QTEREV_ID={new_rev} AND SAQSCE.QUOTE_RECORD_ID=''{quote_rec_id}'' """.format(quote_rec_id=str(quote_contract_recordId),old_rev=str(old_revision_no),new_rev=str(newrev_inc))
            # SAQSCO (QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID) MAPPED INTO  SAQSCN (QTESRVCOB_RECORD_ID)
            updatestatement_saqscn = """UPDATE SAQSCN SET SAQSCN.QTESRVCOB_RECORD_ID =  SAQSCO.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID FROM SAQSCN (NOLOCK) INNER JOIN (SELECT QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,QUOTE_ID,QTEREV_ID,EQUIPMENT_ID,SERVICE_ID, QTEREVFEQ_RECORD_ID FROM SAQSCO (NOLOCK) WHERE SAQSCO.QTEREV_ID={old_rev} AND SAQSCO.QUOTE_RECORD_ID=''{quote_rec_id}'') OLD ON OLD.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID = SAQSCN.QTESRVCOB_RECORD_ID AND SAQSCN.QUOTE_ID=OLD.QUOTE_ID AND SAQSCN.EQUIPMENT_ID=OLD.EQUIPMENT_ID AND SAQSCN.SERVICE_ID=OLD.SERVICE_ID INNER JOIN SAQSCO (NOLOCK) ON SAQSCN.EQUIPMENT_ID=SAQSCO.EQUIPMENT_ID  AND SAQSCN.QUOTE_ID=SAQSCO.QUOTE_ID AND SAQSCN.QTEREV_RECORD_ID=SAQSCO.QTEREV_RECORD_ID AND SAQSCO.QTEREVFEQ_RECORD_ID = OLD.QTEREVFEQ_RECORD_ID AND SAQSCN.SERVICE_ID=SAQSCO.SERVICE_ID WHERE SAQSCN.QTEREV_ID={new_rev} AND SAQSCN.QUOTE_RECORD_ID=''{quote_rec_id}'' """.format(quote_rec_id=str(quote_contract_recordId),old_rev=str(old_revision_no),new_rev=str(newrev_inc))
            #A055S000P01-21042 - Start - M
            # SAQSCA (QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID) MAPPED INTO  SAQSAE (QTESRVCOA_RECORD_ID )
            updatestatement_saqsae = """UPDATE SAQSAE SET SAQSAE.QTESRVCOA_RECORD_ID =  SAQSCA.QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID FROM SAQSAE (NOLOCK) INNER JOIN (SELECT QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID,QUOTE_ID,QTEREV_ID,EQUIPMENT_ID,SERVICE_ID, QTESRVCOB_RECORD_ID,ASSEMBLY_ID FROM SAQSCA (NOLOCK) WHERE SAQSCA.QTEREV_ID={old_rev} AND SAQSCA.QUOTE_RECORD_ID=''{quote_rec_id}'') OLD ON OLD.QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID = SAQSAE.QTESRVCOA_RECORD_ID AND SAQSAE.QUOTE_ID=OLD.QUOTE_ID AND SAQSAE.EQUIPMENT_ID=OLD.EQUIPMENT_ID AND SAQSAE.ASSEMBLY_ID=OLD.ASSEMBLY_ID AND SAQSAE.SERVICE_ID=OLD.SERVICE_ID INNER JOIN SAQSCA (NOLOCK) ON SAQSAE.EQUIPMENT_ID=SAQSCA.EQUIPMENT_ID AND SAQSAE.ASSEMBLY_ID=SAQSCA.ASSEMBLY_ID AND SAQSAE.QUOTE_ID=SAQSCA.QUOTE_ID AND SAQSAE.QTEREV_RECORD_ID=SAQSCA.QTEREV_RECORD_ID AND SAQSCA.QTESRVCOB_RECORD_ID = OLD.QTESRVCOB_RECORD_ID AND SAQSAE.SERVICE_ID=SAQSCA.SERVICE_ID WHERE SAQSAE.QTEREV_ID={new_rev} AND SAQSAE.QUOTE_RECORD_ID=''{quote_rec_id}'' """.format(quote_rec_id=str(quote_contract_recordId),old_rev=str(old_revision_no),new_rev=str(newrev_inc))
            
            query_result1 = SqlHelper.GetFirst("sp_executesql @statement = N'" + str(updatestatement_saqtse) + "'")
            query_result1 = SqlHelper.GetFirst("sp_executesql @statement = N'" + str(updatestatement_saqsgb) + "'")
            query_result1 = SqlHelper.GetFirst("sp_executesql @statement = N'" + str(updatestatement_saqsce) + "'")
            query_result1 = SqlHelper.GetFirst("sp_executesql @statement = N'" + str(updatestatement_saqsae) + "'")
            query_result1 = SqlHelper.GetFirst("sp_executesql @statement = N'" + str(updatestatement_saqscn) + "'")
            #A055S000P01-21059 - Start - M
            ##SAQFEQ QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID MAPPED TO SAQSCA QTEREVFEQ_RECORD_ID
            #SAQSCO (QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID) MAPPED TO SAQSCA (QTESRVCOB_RECORD_ID) 
            updatestatement_saqsca = """UPDATE SAQSCA SET SAQSCA.QTESRVCOB_RECORD_ID =  SAQSCO.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID, SAQSCA.QTEREVFEQ_RECORD_ID =  SAQSCO.QTEREVFEQ_RECORD_ID FROM SAQSCA (NOLOCK) INNER JOIN (SELECT QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,QUOTE_ID,QTEREV_ID,EQUIPMENT_ID,SERVICE_ID,ISNULL(PAR_SERVICE_ID,'''') AS  PAR_SERVICE_ID,QTEREVFEQ_RECORD_ID FROM SAQSCO (NOLOCK) WHERE SAQSCO.QTEREV_ID={old_rev} AND SAQSCO.QUOTE_RECORD_ID=''{quote_rec_id}'') OLD ON OLD.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID = SAQSCA.QTESRVCOB_RECORD_ID AND SAQSCA.QUOTE_ID=OLD.QUOTE_ID AND SAQSCA.EQUIPMENT_ID=OLD.EQUIPMENT_ID AND SAQSCA.SERVICE_ID=OLD.SERVICE_ID AND ISNULL(SAQSCA.PAR_SERVICE_ID,'''')=ISNULL(OLD.PAR_SERVICE_ID,'''') INNER JOIN SAQSCO (NOLOCK) ON SAQSCA.EQUIPMENT_ID=SAQSCO.EQUIPMENT_ID  AND SAQSCA.QUOTE_ID=SAQSCO.QUOTE_ID AND SAQSCA.QTEREV_RECORD_ID=SAQSCO.QTEREV_RECORD_ID AND SAQSCO.QTEREVFEQ_RECORD_ID = OLD.QTEREVFEQ_RECORD_ID AND SAQSCA.SERVICE_ID=SAQSCO.SERVICE_ID AND ISNULL(SAQSCA.PAR_SERVICE_ID,'''')=ISNULL(SAQSCO.PAR_SERVICE_ID,'''') WHERE SAQSCA.QTEREV_ID={new_rev} AND SAQSCA.QUOTE_RECORD_ID=''{quote_rec_id}'' """.format(quote_rec_id=str(quote_contract_recordId),old_rev=str(old_revision_no),new_rev=str(newrev_inc))
            Trace.Write("updatestatement_saqsca-"+str(updatestatement_saqsca))
            query_result3 = SqlHelper.GetFirst("sp_executesql @statement = N'" + str(updatestatement_saqsca) + "'")
            #A055S000P01-21042,A055S000P01-21059 - End - M
            # INC08638273 - Start - M
            # INC08638273 - End - M
            #NON TEMPTOOL UPDATE STARTS
            ##SAQFEQ (QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID) MAPPED TO SAQSCO (QTEREVFEQ_RECORD_ID)
            #A055S000P01-21042 - Start -M
            updatestatement_saqsco_nt = """UPDATE SAQSCO SET QTEREVFEQ_RECORD_ID = QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID FROM SAQSCO INNER JOIN SAQFEQ ON SAQSCO.QUOTE_RECORD_ID = SAQFEQ.QUOTE_RECORD_ID AND SAQSCO.QTEREV_RECORD_ID = SAQFEQ.QTEREV_RECORD_ID AND SAQSCO.FABLOCATION_ID = SAQFEQ.FABLOCATION_ID AND SAQSCO.GREENBOOK = SAQFEQ.GREENBOOK AND SAQSCO.EQUIPMENT_ID = SAQFEQ.EQUIPMENT_ID AND ISNULL(SAQFEQ.TEMP_TOOL,'''') = ISNULL(SAQSCO.TEMP_TOOL,'''')  WHERE SAQSCO.QUOTE_RECORD_ID = ''{}'' AND SAQSCO.QTEREV_ID  = ''{}'' AND (ISNULL(SAQSCO.TEMP_TOOL,0) = 0 OR SAQSCO.TEMP_TOOL = '''') """.format(str(quote_contract_recordId),int(newrev_inc))
            #A055S000P01-21042 - End - M
            ##SAQFEQ QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID MAPPED TO SAQFEA QTEREVFEQ_RECORD_ID
            updatestatement_saqfea_nt = """UPDATE SAQFEA SET SAQFEA.QTEREVFEQ_RECORD_ID =  SAQFEQ.QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID FROM SAQFEA (NOLOCK) INNER JOIN (SELECT QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID,QUOTE_ID,QTEREV_ID,EQUIPMENT_ID,TEMP_TOOL FROM SAQFEQ (NOLOCK) WHERE SAQFEQ.QTEREV_ID={old_rev} AND SAQFEQ.QUOTE_RECORD_ID=''{quote_rec_id}'') OLD ON OLD.QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID = SAQFEA.QTEREVFEQ_RECORD_ID AND SAQFEA.QUOTE_ID=OLD.QUOTE_ID AND SAQFEA.EQUIPMENT_ID=OLD.EQUIPMENT_ID INNER JOIN SAQFEQ (NOLOCK) ON SAQFEA.EQUIPMENT_ID=SAQFEQ.EQUIPMENT_ID  AND SAQFEA.QUOTE_ID=SAQFEQ.QUOTE_ID AND SAQFEA.QTEREV_RECORD_ID=SAQFEQ.QTEREV_RECORD_ID AND SAQFEQ.TEMP_TOOL = OLD.TEMP_TOOL WHERE SAQFEA.QTEREV_ID={new_rev} AND SAQFEA.QUOTE_RECORD_ID=''{quote_rec_id}'' AND (SAQFEQ.TEMP_TOOL = 0 OR SAQFEQ.TEMP_TOOL ='''')   """.format(quote_rec_id=str(quote_contract_recordId),old_rev=str(old_revision_no),new_rev=str(newrev_inc))
            #INC09115153 -START
            updatestatement_saqsae_nt ="""UPDATE SAQSAE SET SAQSAE.QTESRVCOE_RECORD_ID = SAQSCE.QUOTE_SERVICE_COVERED_OBJ_ENTITLEMENTS_RECORD_ID  FROM SAQSAE (NOLOCK) INNER JOIN SAQSCE ON SAQSCE.QUOTE_RECORD_ID = SAQSAE.QUOTE_RECORD_ID AND SAQSCE.QTEREV_ID =SAQSAE.QTEREV_ID   WHERE SAQSCE.QTEREV_ID = {new_rev} AND SAQSCE.QUOTE_RECORD_ID =''{quote_rec_id}'' """.format(quote_rec_id=str(quote_contract_recordId),new_rev=str(newrev_inc))

            query_result3 = SqlHelper.GetFirst("sp_executesql @statement = N'" + str(updatestatement_saqfea_nt) + "'")
            #INC08709720 - End - A
            query_result2 = SqlHelper.GetFirst("sp_executesql @statement = N'" + str(updatestatement_saqsco_nt) + "'")
            query_result4 = SqlHelper.GetFirst("sp_executesql @statement = N'" + str(updatestatement_saqsae_nt) + "'")
            #INC09115153 -END
            #NON TEMPTOOL UPDATE ENDS
            
            #TEMPTOOL UPDATE STARTS
            saqfeq_list = ["SAQFEQ_OLD_BKP_{}".format(Quote.CompositeNumber),"SAQFEQ_NEW_BKP_{}".format(Quote.CompositeNumber)]
            for saqfeq_table in saqfeq_list:
                saqfeq = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS (NOLOCK) WHERE NAME= ''"+str(saqfeq_table)+"'' ) BEGIN DROP TABLE "+str(saqfeq_table)+" END  ' ")
                qry_result = SqlHelper.GetFirst("sp_executesql @T=N'SELECT EQUIPMENT_ID,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,ROW_NUMBER()OVER(ORDER BY(SAQFEQ.CpqTableEntryId)) AS TMPTOL_SEQ,QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID,TEMP_TOOL INTO {saqfeq_table} FROM SAQFEQ(NOLOCK) WHERE ISNULL(TEMP_TOOL,0) = 1 AND QUOTE_RECORD_ID =''{quote_rec_id}'' AND QTEREV_ID = {rev_id}  ' ".format(quote_rec_id = str(quote_contract_recordId), rev_id = str(old_revision_no) if "SAQFEQ_OLD_BKP_" in  saqfeq_table else str(newrev_inc) ,saqfeq_table =saqfeq_table))

            # SAQFEQ (QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID) MAPPED TO SAQSCO (QTEREVFEQ_RECORD_ID)
            updatestatement_saqsco_tt = """UPDATE SAQSCO SET SAQSCO.QTEREVFEQ_RECORD_ID =  SAQFEQ_NEW.QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID FROM SAQSCO (NOLOCK) INNER JOIN (SELECT QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID,QUOTE_ID,QTEREV_ID,EQUIPMENT_ID,TMPTOL_SEQ FROM {saqfeq_old} SAQFEQ_OLD  WHERE SAQFEQ_OLD.QTEREV_ID={old_rev} AND SAQFEQ_OLD.QUOTE_RECORD_ID=''{quote_rec_id}'') OLD ON OLD.QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID = SAQSCO.QTEREVFEQ_RECORD_ID AND SAQSCO.QUOTE_ID=OLD.QUOTE_ID AND SAQSCO.EQUIPMENT_ID=OLD.EQUIPMENT_ID INNER JOIN {saqfeq_new} SAQFEQ_NEW  ON  SAQSCO.QUOTE_ID=SAQFEQ_NEW.QUOTE_ID AND SAQSCO.QTEREV_RECORD_ID=SAQFEQ_NEW.QTEREV_RECORD_ID AND SAQFEQ_NEW.TMPTOL_SEQ = OLD.TMPTOL_SEQ WHERE SAQSCO.QTEREV_ID={new_rev} AND SAQSCO.QUOTE_RECORD_ID=''{quote_rec_id}'' and SAQFEQ_NEW.temp_tool =1  """.format(quote_rec_id=str(quote_contract_recordId),old_rev=str(old_revision_no),new_rev=str(newrev_inc),saqfeq_old = saqfeq_list[0], saqfeq_new = saqfeq_list[1] )
            ##SAQFEQ QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID MAPPED TO SAQFEA QTEREVFEQ_RECORD_ID
            updatestatement_saqfea_tt = """UPDATE SAQFEA SET SAQFEA.QTEREVFEQ_RECORD_ID =  SAQFEQ_NEW.QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID FROM SAQFEA (NOLOCK) INNER JOIN (SELECT QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID,QUOTE_ID,QTEREV_ID,EQUIPMENT_ID,TMPTOL_SEQ FROM {saqfeq_old} SAQFEQ_OLD  WHERE SAQFEQ_OLD.QTEREV_ID={old_rev} AND SAQFEQ_OLD.QUOTE_RECORD_ID=''{quote_rec_id}'') OLD ON OLD.QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID = SAQFEA.QTEREVFEQ_RECORD_ID AND SAQFEA.QUOTE_ID=OLD.QUOTE_ID AND SAQFEA.EQUIPMENT_ID=OLD.EQUIPMENT_ID INNER JOIN {saqfeq_new} SAQFEQ_NEW  ON  SAQFEA.QUOTE_ID=SAQFEQ_NEW.QUOTE_ID AND SAQFEA.QTEREV_RECORD_ID=SAQFEQ_NEW.QTEREV_RECORD_ID AND SAQFEQ_NEW.TMPTOL_SEQ = OLD.TMPTOL_SEQ WHERE SAQFEA.QTEREV_ID={new_rev} AND SAQFEA.QUOTE_RECORD_ID=''{quote_rec_id}'' and SAQFEQ_NEW.temp_tool =1  """.format(quote_rec_id=str(quote_contract_recordId),old_rev=str(old_revision_no),new_rev=str(newrev_inc),saqfeq_old = saqfeq_list[0], saqfeq_new = saqfeq_list[1] )

            query_result3 = SqlHelper.GetFirst("sp_executesql @statement = N'" + str(updatestatement_saqfea_tt) + "'")
            query_result2 = SqlHelper.GetFirst("sp_executesql @statement = N'" + str(updatestatement_saqsco_tt) + "'")
            for saqfeq_table in saqfeq_list:
                saqfeq = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS (NOLOCK) WHERE NAME= ''"+str(saqfeq_table)+"'' ) BEGIN DROP TABLE "+str(saqfeq_table)+" END  ' ")
            #TEMPTOOL UPDATE ENDS
            #INC08971027 - Ends - M
            #A055S000P01-20908 - Ends - M
            for update_table in ['SAQSCA','SAQSCN','SAQSCE']:
                additonal_where = "AND ISNULL({}.PAR_SERVICE_ID,'''') = ISNULL(SAQSCO.PAR_SERVICE_ID,'''')".format(update_table)
                updatestatement_feq = """UPDATE {update_table} SET {update_table}.QTEREVFEQ_RECORD_ID =  SAQSCO.QTEREVFEQ_RECORD_ID FROM {update_table} (NOLOCK) INNER JOIN SAQSCO (NOLOCK) ON {update_table}.EQUIPMENT_ID=SAQSCO.EQUIPMENT_ID  AND {update_table}.QUOTE_ID=SAQSCO.QUOTE_ID AND {update_table}.QTEREV_RECORD_ID=SAQSCO.QTEREV_RECORD_ID AND SAQSCO.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID = {update_table}.QTESRVCOB_RECORD_ID AND {update_table}.SERVICE_ID=SAQSCO.SERVICE_ID {additonal_where} WHERE {update_table}.QTEREV_ID={new_rev} AND {update_table}.QUOTE_RECORD_ID=''{quote_rec_id}'' """.format(quote_rec_id=str(quote_contract_recordId),old_rev=str(old_revision_no),new_rev=str(newrev_inc),update_table = update_table, additonal_where = additonal_where if update_table != 'SAQSCN' else '' )
                query_result3 = SqlHelper.GetFirst("sp_executesql @statement = N'" + str(updatestatement_feq) + "'")
            
            #A055S000P01-21059,A055S000P01-21042 - End - M
            ## END CLONE OBJECT SAQSCO TO SAQSCE
            
            #Sql.RunQuery("""UPDATE SAQTSO SET QTEREV_ID = '{newrev_inc}',QTEREV_RECORD_ID = '{quote_revision_id}' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}'""".format(quote_revision_id=quote_revision_id,newrev_inc= newrev_inc,QuoteRecordId=quote_contract_recordId))
            #INSERT salesorg end

            #Insert fabs start
            
            #Sql.RunQuery("""UPDATE SAQFBL SET QTEREV_ID = '{newrev_inc}',QTEREV_RECORD_ID = '{quote_revision_id}' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}'""".format(quote_revision_id=quote_revision_id,newrev_inc= newrev_inc,QuoteRecordId=quote_contract_recordId))
            #Insert fabs end


            #Sql.RunQuery("""UPDATE SAQTMT SET QTEREV_ID = {newrev_inc},QTEREV_RECORD_ID = '{quote_revision_id}',ACTIVE_REV={active_rev} WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{QuoteRecordId}'""".format(quote_revision_id=quote_revision_id,newrev_inc= newrev_inc,QuoteRecordId=quote_contract_recordId,active_rev = 0))
            #quote_detials = {"MASTER_TABLE_QUOTE_RECORD_ID": str(Guid.NewGuid()).upper(),"QUOTE_ID": get_quote_info_details.QUOTE_ID,"QUOTE_NAME":get_quote_info_details.QUOTE_NAME,"ACCCNT_RECORD_ID":get_quote_info_details.ACCCNT_RECORD_ID,"ACCOUNT_ID":get_quote_info_details.ACCOUNT_ID,"ACCOUNT_NAME":get_quote_info_details.ACCOUNT_NAME,"ACCOUNT_RECORD_ID":get_quote_info_details.ACCOUNT_RECORD_ID,"CRM_CONTRACT_ID":get_quote_info_details.CRM_CONTRACT_ID,"QUOTE_TYPE":get_quote_info_details.QUOTE_TYPE,"SALE_TYPE":get_quote_info_details.SALE_TYPE,"QUOTE_LEVEL":get_quote_info_details.QUOTE_LEVEL,"REGION":get_quote_info_details.REGION,"QUOTE_STATUS":get_quote_info_details.QUOTE_STATUS,"CONTRACT_VALID_FROM":get_quote_info_details.CONTRACT_VALID_FROM,"CONTRACT_VALID_TO":get_quote_info_details.CONTRACT_VALID_TO,"PARENTQUOTE_ID":get_quote_info_details.PARENTQUOTE_ID,"PARENTQUOTE_NAME":get_quote_info_details.PARENTQUOTE_NAME,"PARENTQUOTE_RECORD_ID":get_quote_info_details.PARENTQUOTE_RECORD_ID,"PAYMENTTERM_ID":get_quote_info_details.PAYMENTTERM_ID,"INCOTERMS":get_quote_info_details.INCOTERMS,"PAYMENTTERM_NAME":get_quote_info_details.PAYMENTTERM_NAME,"PAYMENTTERM_RECORD_ID":get_quote_info_details.PAYMENTTERM_RECORD_ID,"DOCUMENT_TYPE":get_quote_info_details.DOCUMENT_TYPE,"SEGMENT_RECORD_ID":get_quote_info_details.SEGMENT_RECORD_ID,"C4C_QUOTE_ID":get_quote_info_details.C4C_QUOTE_ID,"QUOTE_CURRENCY":get_quote_info_details.QUOTE_CURRENCY,"QUOTE_CURRENCY_RECORD_ID":get_quote_info_details.QUOTE_CURRENCY_RECORD_ID,"CANCELLATION_PERIOD":get_quote_info_details.CANCELLATION_PERIOD,"SEGMENT_ID":get_quote_info_details.SEGMENT_ID,"GLOBAL_CURRENCY":get_quote_info_details.GLOBAL_CURRENCY,"GLOBAL_CURRENCY_RECORD_ID":get_quote_info_details.GLOBAL_CURRENCY_RECORD_ID,"PAYMENTTERM_DAYS":get_quote_info_details.PAYMENTTERM_DAYS,"QUOTE_EXPIRE_DATE":get_quote_info_details.QUOTE_EXPIRE_DATE,"ACTIVE_REV":0,"QTEREV_ID":newrev_inc,"QTEREV_RECORD_ID":quote_revision_id,"QUOTE_APPROVE_DATE":get_quote_info_details.QUOTE_APPROVE_DATE}
            #quote_table_info.AddRow(quote_detials)
            #Sql.Upsert(quote_table_info)
        #get quote data for update in SAQTMT end
        NRev = QuoteHelper.Edit(get_quote_info_details.QUOTE_ID)
        time.sleep( 5 )
        Quote.RefreshActions()
        for item in Quote.MainItems:
            item.Delete()
        ## making the quote summary custom field empty
        # Quote.GetCustomField('TARGET_PRICE').Content = '' 
        # Quote.GetCustomField('CEILING_PRICE').Content = ''
        # Quote.GetCustomField('TOTAL_COST').Content = '' 
        # Quote.GetCustomField('SALES_DISCOUNTED_PRICE').Content = ''
        # Quote.GetCustomField('BD_PRICE_MARGIN').Content = ''
        # Quote.GetCustomField('BD_PRICE_DISCOUNT').Content = ''
        # Quote.GetCustomField('TOTAL_NET_PRICE').Content = ''
        # Quote.GetCustomField('YEAR_OVER_YEAR').Content = ''
        # Quote.GetCustomField('YEAR_1').Content = '' 
        # Quote.GetCustomField('YEAR_2').Content = '' 
        # Quote.GetCustomField('YEAR_3').Content = '' 
        # Quote.GetCustomField('TAX').Content = '' 
        # Quote.GetCustomField('TOTAL_NET_VALUE').Content = ''
        # Quote.GetCustomField('MODEL_PRICE').Content = '' 
        # Quote.GetCustomField('BD_PRICE').Content = ''
        # Quote.GetCustomField('DISCOUNT').Content = ''

        # APPROVALS - NEW REVISION START
        Quote_status = Quote.OrderStatus.Name
        if str(Quote_status.upper()) == 'APPROVED' or str(Quote_status.upper()) == 'REJECTED' or str(Quote_status.upper()) == 'AWAITING INTERNAL APPROVAL':
            Quote.ChangeQuoteStatus("Preparing")
        
        Quote.Save()
        #Quote.RefreshActions()
        current_revison1 = Quote.RevisionNumber
        
        get_quote_info_details = Sql.GetFirst("select * from SAQTMT where QUOTE_ID = '"+str(Quote.CompositeNumber)+"'")
        Quote.SetGlobal("contract_quote_record_id",get_quote_info_details.MASTER_TABLE_QUOTE_RECORD_ID)
        Quote.SetGlobal("quote_revision_record_id",str(get_quote_info_details.QTEREV_RECORD_ID))
        #Hadoop fix - Start - A
        Sql.RunQuery("""UPDATE SAQTRV SET CpqTableEntryModifiedBy = {CURRENT_USER} ,CpqTableEntryDateModified = GETDATE() WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' and QUOTE_REVISION_RECORD_ID='{REV_recordid}'""".format(CURRENT_USER=User.Id,QuoteRecordId=quote_contract_recordId,REV_recordid =quote_revision_id))
        #Hadoop fix - End - A		
        ##newrevision edot active for expiry Quote:A055S000P01-14308
        updatesaqtmtexpire = (""" UPDATE SAQTMT SET EXPIRED = 0 FROM SAQTMT INNER JOIN SAQTRV ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQTRV.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = SAQTRV.QTEREV_RECORD_ID WHERE  SAQTRV.REV_CREATE_DATE = '{current_date}' AND SAQTRV.QTEREV_RECORD_ID ='{quote_revision_record_id}' AND SAQTRV.QUOTE_RECORD_ID = '{contract_quote_record_id}'  AND ACTIVE = '1' """.format(current_date = current_date,quote_revision_record_id=get_quote_info_details.QTEREV_RECORD_ID,contract_quote_record_id =get_quote_info_details.MASTER_TABLE_QUOTE_RECORD_ID))
        Sql.RunQuery(updatesaqtmtexpire)
        CQREVSTSCH.Revisionstatusdatecapture(Quote.GetGlobal("contract_quote_record_id"),str(get_quote_info_details.QTEREV_RECORD_ID),)
        
        ##A055S000P01-19173 code starts..
        ##Calling the below script to retrieve and update the events from sscm while creating new revision....		
        service_object = Sql.GetList("SELECT SERVICE_ID FROM SAQTSV WHERE QUOTE_ID = '{Quote_id}' and QTEREV_ID = {newrev_inc}".format(Quote_id =Quote.CompositeNumber, newrev_inc = newrev_inc))
        for service in service_object:
            service_id = service.SERVICE_ID	
            #INC08638619 - Start - M, #CR681 - Start - M
            service_entitlement_obj =Sql.GetFirst("""select QUOTE_TYPE,PMLAB_ENT,CMLAB_ENT from SAQTSE (nolock) where QUOTE_ID = '{Quote_id}' AND QTEREV_ID = '{RevisionId}' and SERVICE_ID = '{service_id}' """.format(Quote_id =Quote.CompositeNumber,RevisionId=newrev_inc,service_id = service.SERVICE_ID))
            if service_entitlement_obj is not None:
                #INC08851332 - Start - M
                if service_entitlement_obj.QUOTE_TYPE and (service_entitlement_obj.CMLAB_ENT or service_entitlement_obj.PMLAB_ENT or service.SERVICE_ID in ('Z0128','Z0010')):
                #INC08851332 - End - M
                #CR681 - End - M
                # entitlement_xml = service_entitlement_obj.ENTITLEMENT_XML
                # pattern_tag = re.compile(r'(<QUOTE_ITEM_ENTITLEMENT>[\w\W]*?</QUOTE_ITEM_ENTITLEMENT>)')
                # pattern_name = re.compile(r'<ENTITLEMENT_DISPLAY_VALUE>([^>]*?)</ENTITLEMENT_DISPLAY_VALUE>')
                # quote_type_id = re.compile(r'<ENTITLEMENT_ID>AGS_[^>]*?_PQB_QTETYP</ENTITLEMENT_ID>')
                # for value in re.finditer(pattern_tag, entitlement_xml):
                # 	sub_string = value.group(1)
                # 	quote_type_attribute_id =re.findall(quote_type_id,sub_string)
                # 	if quote_type_attribute_id:
                # 		quote_type_value =re.findall(pattern_name,sub_string)
                # 		QuoteTypeValue = quote_type_value[0]
                    ScriptExecutor.ExecuteGlobal(
                                        "CQCRUDOPTN",
                                        {
                                            "NodeType": "COVERED OBJ MODEL",
                                            "Opertion": "ADD",
                                            "NewRevision": "YES",
                                            "QuoteTypeValue": service_entitlement_obj.QUOTE_TYPE,
                                            "ServiceId": service_id,
                                            "RealTimeIntegrationService":service_id,
                                        },
                                    )
                        #Log.Info("Script ended")				
                ##A055S000P01-19173 code ends..	
            #INC08638619 - End - M

    return True



#set active revision  from grid- start
def set_active_revision(Opertion,cartrev):
    #for val in select_active:
    ObjectName = cartrev.split('-')[0].strip()
    cpqid = cartrev.split('-')[1].strip()
    #Hadoop fix - Start - A
    active_rev_id = None
    active_rev_cart_id = None
    #Hadoop fix - End - A	
    active_rev_obj = Sql.GetFirst("select QTEREV_ID, CART_ID from SAQTRV (NOLOCK) where QUOTE_ID = '{}' and ACTIVE = 1".format(ObjectName))
    if active_rev_obj:
        active_rev_id = active_rev_obj.QTEREV_ID
        active_rev_cart_id = active_rev_obj.CART_ID
    get_rev_quote_info_details = Sql.GetFirst("SELECT SAQTRV.*, SAQTMT.ADDUSR_RECORD_ID as ADDUSR_ID FROM SAQTRV (NOLOCK) JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQTRV.QUOTE_RECORD_ID WHERE SAQTRV.QUOTE_ID = '{}' AND SAQTRV.QTEREV_ID = {}".format(ObjectName,cpqid))
    if get_rev_quote_info_details:
        recid = get_rev_quote_info_details.QUOTE_REVISION_RECORD_ID
        get_quote_info_details = Sql.GetFirst("select * from SAQTMT (NOLOCK) where MASTER_TABLE_QUOTE_RECORD_ID = '"+str(quote_contract_recordId)+"'")
        Quote.SetGlobal("contract_quote_record_id",quote_contract_recordId)
        #Hadoop fix - Start - A
        Sql.RunQuery("""UPDATE SAQTRV SET ACTIVE = {active_rev} WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_ID = {QuoteRevisionId}""".format(QuoteRecordId=quote_contract_recordId,QuoteRevisionId=active_rev_id,active_rev = 0))
        #Hadoop fix - End - A		
        Sql.RunQuery("""UPDATE SAQTRV SET ACTIVE = {active_rev} WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' and QUOTE_REVISION_RECORD_ID = '{recid}'""".format(QuoteRecordId=quote_contract_recordId,active_rev = 1,recid =recid))
        # INC08706882 START A
        Sql.RunQuery("""UPDATE SAQTRV SET CpqTableEntryModifiedBy = {CURRENT_USER} ,CpqTableEntryDateModified = GETDATE() WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' and QUOTE_REVISION_RECORD_ID='{REV_recordid}'""".format(CURRENT_USER=User.Id,QuoteRecordId=quote_contract_recordId,REV_recordid =recid))
        # INC08706882 END A
        # INC08702610 START A
        Sql.RunQuery("""UPDATE A SET A.CONTRACT_VALID_FROM = B.CONTRACT_VALID_FROM, A.CONTRACT_VALID_TO = B.CONTRACT_VALID_TO FROM SAQTMT A JOIN SAQTRV B ON A.MASTER_TABLE_QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.QTEREV_RECORD_ID = B.QTEREV_RECORD_ID WHERE B.QUOTE_RECORD_ID = '{QuoteRecordId}' and A.QTEREV_RECORD_ID='{quote_revision_record_id}'""".format(QuoteRecordId=quote_contract_recordId,quote_revision_record_id =recid))
        # INC08702610 END A		

        #get_rev_info_details = Sql.GetFirst("select QTEREV_ID,CART_ID,ADDUSR_RECORD_ID,REVISION_STATUS from SAQTRV (NOLOCK) where QUOTE_RECORD_ID = '"+str(quote_contract_recordId)+"' and QUOTE_REVISION_RECORD_ID = '"+str(recid)+"'")
        gtcart_idval = get_rev_quote_info_details.CART_ID
        Sql.RunQuery("""UPDATE SAQTMT SET QTEREV_ID = {newrev_inc},QTEREV_RECORD_ID = '{quote_revision_id}',ACTIVE_REV={active_rev} WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{QuoteRecordId}'""".format(quote_revision_id=recid,newrev_inc= get_rev_quote_info_details.QTEREV_ID,QuoteRecordId=quote_contract_recordId,active_rev = 1))
        Quote.SetGlobal("quote_revision_record_id",recid)

        inactive_cart_activerev = SqlHelper.GetFirst("sp_executesql @t = N'UPDATE CART SET ACTIVE_REV =''0'' FROM CART (nolock) JOIN CART_REVISIONS (nolock) ON CART_REVISIONS.CART_ID = CART.CART_ID AND CART_REVISIONS.VISITOR_ID = CART.USERID WHERE CART.CART_ID = ''"+ str(active_rev_cart_id)+ "'' AND CART.ExternalId = ''"+ str(Quote.CompositeNumber)+ "'' AND CART.USERID = ''"+ str(get_rev_quote_info_details.ADDUSR_ID)+ "'' '")

        update_cart_activerev = SqlHelper.GetFirst("sp_executesql @t = N'UPDATE CART SET ACTIVE_REV =''1'' FROM CART (nolock) WHERE CART.CART_ID = ''"+ str(gtcart_idval)+ "'' AND CART.ExternalId = ''"+ str(Quote.CompositeNumber)+ "'' AND CART.USERID = ''"+ str(get_rev_quote_info_details.ADDUSR_ID)+ "'' '")

        # GETCARTID=SqlHelper.GetFirst("sp_executesql @t = N'update CART set ACTIVE_REV =''0'' WHERE CART_ID in (select distinct top 10 CART_REVISIONS.CART_ID as ID from CART_REVISIONS (nolock) INNER JOIN CART2 (nolock) ON CART_REVISIONS.CART_ID = CART2.CartId AND CART_REVISIONS.VISITOR_ID = CART2.OwnerId INNER JOIN CART(NOLOCK) ON CART.CART_ID = CART2.CartId and CART.USERID = CART2.OwnerId WHERE CART2.CartCompositeNumber = ''"+ str(Quote.CompositeNumber)+ "'') '")
        # UPDATEACTIVE = SqlHelper.GetFirst("sp_executesql @t=N'update CART set ACTIVE_REV =''1'' where CART_ID = ''"+str(gtcart_idval)+"'' and USERID =''"+str(User.Id)+"'' '")
        # cart_obj = SqlHelper.GetList("SELECT DATE_CREATED, USERID, CART_ID, ACTIVE_REV FROM cart WHERE ExternalId = '{}' AND ACTIVE_REV = 1".format(get_quote_info_details.QUOTE_ID)) 
        # if not cart_obj:
        # 	UPDATEACTIVE = SqlHelper.GetFirst("sp_executesql @t=N'update CART set ACTIVE_REV =''1'' where CART_ID = ''"+str(gtcart_idval)+"'' and ExternalId =''"+str(get_quote_info_details.QUOTE_ID)+"'''")
        NRev = QuoteHelper.Edit(get_quote_info_details.QUOTE_ID)
        # APPROVALS - SET ACTIVE START

        #update contrcta valid from start
        Sql.RunQuery("""UPDATE SAQTMT SET CONTRACT_VALID_FROM = '{contract_valid_from}',CONTRACT_VALID_TO='{contract_valid_to}' WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{QuoteRecordId}' """.format(QuoteRecordId=quote_contract_recordId,contract_valid_from =get_rev_quote_info_details.CONTRACT_VALID_FROM,contract_valid_to =get_rev_quote_info_details.CONTRACT_VALID_TO))
        #update contract valid to end

        Quote_status = Quote.OrderStatus.Name
        revision_status = get_rev_quote_info_details.REVISION_STATUS
        cartid = get_rev_quote_info_details.CART_ID
        ownerid = get_rev_quote_info_details.ADDUSR_RECORD_ID
        if str(revision_status.upper()) in ('APR-APPROVED','BOK-CONTRACT BOOKED','OPD-PREPARING QUOTE DOCUMENTS','OPD-CUSTOMER REJECTED','OPD-CUSTOMER ACCEPTED','LGL-PREPARING LEGAL SOW','LGL-LEGAL SOW REJECTED','LGL-LEGAL SOW ACCEPTED','CBC-PREPARING CBC','CBC-CBC COMPLETED','BOK-CONTRACT CREATED'):
            Quote.ChangeQuoteStatus("Approved")
        elif str(revision_status.upper()) in ('CFG-CONFIGURING','CFG-ACQUIRING','CFG-ON HOLD - COSTING','PRR-ON HOLD PRICING','PRI-PRICING'):
            Quote.ChangeQuoteStatus("Preparing")
        
        #INC08990845
        elif str(revision_status.upper()) == "APR-APPROVAL PENDING":
            GetApprovalRequested = Sql.GetFirst("SELECT STATUS FROM QT__SAQAPP (NOLOCK) WHERE CartId = {} and OwnerId = {} AND STATUS = 'Approval Requested'".format(cartid,ownerid))

            if GetApprovalRequested:
                Quote.ChangeQuoteStatus("Awaiting Internal Approval")
            else:
                Quote.ChangeQuoteStatus("Preparing")
        #INC08990845

        elif str(revision_status.upper()) == "APR-REJECTED":
            Quote.ChangeQuoteStatus("Rejected")
        
        elif str(revision_status.upper()) == "APR-RECALLED":
            Quote.ChangeQuoteStatus("Recalled")


        # APPROVALS - SET ACTIVE END
        time.sleep( 5 )
        #Hadoop fix - Start - A
        # INC08706882 START A
        Sql.RunQuery("""UPDATE SAQTRV SET CpqTableEntryModifiedBy = {CURRENT_USER} ,CpqTableEntryDateModified = GETDATE() WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' and QUOTE_REVISION_RECORD_ID='{REV_recordid}'""".format(CURRENT_USER=User.Id,QuoteRecordId=quote_contract_recordId,REV_recordid =recid))
        # INC08706882 END A
        #Hadoop fix - End - A		
        Quote.RefreshActions()
                                
        get_quote_info_details = Sql.GetFirst("select * from SAQTMT (NOLOCK) where QUOTE_ID = '"+str(Quote.CompositeNumber)+"'")
        Quote.SetGlobal("contract_quote_record_id",get_quote_info_details.MASTER_TABLE_QUOTE_RECORD_ID)
        Quote.SetGlobal("quote_revision_record_id",str(get_quote_info_details.QTEREV_RECORD_ID))
        ##Calling the iflow for quote header writeback to cpq to c4c code starts..
        #INC08656425 M
        try:
            CQCPQC4CWB.writeback_to_c4c(writeback="quote_header",contract_quote_record_id=Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id =Quote.GetGlobal("quote_revision_record_id"),Sql=Sql)
            CQCPQC4CWB.writeback_to_c4c(writeback="opportunity_header",contract_quote_record_id=Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id=Quote.GetGlobal("quote_revision_record_id"),Sql=Sql)
        except Exception as e:
            Log.Info("EXCEPTION: CPI CALL FAILED TO SEND DATA TO c4c in SET ACTIVE" + str(e))
        #INC08656425 M
        ##Calling the iflow for quote header writeback to cpq to c4c code ends...		
    return True

#edit quote description field start
def save_desc_revision(Opertion,cartrev,cartrev_id,):
    Trace.Write(str(cartrev_id)+"-------cartrev----146---------"+str(cartrev))
    ObjectName = cartrev_id.split('-')[0].strip()
    recid =''
    cpqid = cartrev_id.split('-')[1].strip()
    get_rev_quote_info_details = Sql.GetFirst("select * from SAQTRV where QUOTE_ID = '{}' and QTEREV_ID = {}".format(ObjectName,cpqid))
    cartrev = re.sub(r"'","''",cartrev)
    if get_rev_quote_info_details:
        recid = get_rev_quote_info_details.QUOTE_REVISION_RECORD_ID
    #recid = CPQID.KeyCPQId.GetKEYId(ObjectName,str(cpqid))
    update_quote_rev = Sql.RunQuery("""UPDATE SAQTRV SET REVISION_DESCRIPTION = '{rev_desc}' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND  QUOTE_REVISION_RECORD_ID = '{recid}' """.format(QuoteRecordId=quote_contract_recordId,recid =recid,rev_desc= cartrev))
    productdesc = Sql.RunQuery("""UPDATE  CART_REVISIONS SET DESCRIPTION = '{rev_desc}' WHERE CART_ID = '{quote_idnative}' AND  VISITOR_ID = '{recid}' """.format(quote_idnative=Quote.QuoteId,recid =Quote.UserId,rev_desc= cartrev))
    #productdesc = SqlHelper.GetFirst("sp_executesql @t=N'update CART_REVISIONS set DESCRIPTION =''"+str(cartrev)+"'' where CART_ID = ''"+str(Quote.QuoteId)+"'' and VISITOR_ID =''"+str(Quote.UserId)+"''  '")
    return True
#edit quote description field end



Opertion = Param.Opertion
cartrev = Param.cartrev
try:
    cartrev_id =Param.cartrev_id
except:
    cartrev_id =''

if Opertion == "SET_ACTIVE":
    ApiResponse = ApiResponseFactory.JsonResponse(set_active_revision(Opertion,cartrev,))
elif Opertion == "SAVE_DESC":
    ApiResponse = ApiResponseFactory.JsonResponse(save_desc_revision(Opertion,cartrev,cartrev_id,))
else:
    ApiResponse = ApiResponseFactory.JsonResponse(create_new_revision(Opertion,cartrev,))
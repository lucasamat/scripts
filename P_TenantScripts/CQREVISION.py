#===================================================================================================================#======================
#   __script_name : CQREVISION.PY
#   __script_description : THIS SCRIPT IS USED TO CREATE NEW REVISIONS,EDIT REVISIONS AND UPDATE CUSTOM TABLES
#   __primary_author__ : SRIJAYDHURGA
#   __create_date :08/30/2021
#   Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
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
        "SAQSAP":"QUOTE_SERVICE_COV_OBJ_ASS_PM_KIT_RECORD_ID",
        "SAQRDS":"QUOTE_REV_DELIVERY_SCHEDULE_RECORD_ID",
        "SAQRGG":"QUOTE_REV_PO_GREENBOOK_GOT_CODES_RECORD_ID",
        "SAQGPM":"QUOTE_REV_PO_GBK_GOT_CODE_PM_EVENTS_RECORD_ID",
        "SAQGPA":"QUOTE_REV_PO_GRNBK_PM_EVEN_ASSEMBLIES_RECORD_ID",
        "SAQGPE":"QUOTE_REV_GOT_CD_PM_EVNT_ENTITLEMENTS_RECORD_ID",
        "SAQSKP":"QUOTE_SERVICE_COV_OBJ_ASS_PM_KIT_PARTS_RECORD_ID",
        "SAQSAO":"QUOTE_SERVICE_ADD_ON_PRODUCT_RECORD_ID",
        "SAQSCN":"QUOTE_REV_PO_EQUIPMENT_PARTS_RECORD_ID",
        "SAQRSP":"QUOTE_REV_PO_PRODUCT_LIST_ID",
        "SAQTDA":"QUOTE_REV_TOOL_IDLING_ATTR_VAL_RECORD_ID",
        }
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

        update_quote_rev = Sql.RunQuery("""UPDATE SAQTRV SET ACTIVE = {active_rev} WHERE QUOTE_RECORD_ID = '{QuoteRecordId}'""".format(QuoteRecordId=quote_contract_recordId,active_rev = 0))
        newrev_inc = int(get_current_rev.rev_id)+1

        get_rev_details = Sql.GetFirst("SELECT DISTINCT TOP 1 CART2.CARTCOMPOSITENUMBER, CART_REVISIONS.REVISION_ID, CART_REVISIONS.DESCRIPTION as DESCRIPTION,CART.ACTIVE_REV, CART_REVISIONS.CART_ID, CART_REVISIONS.PARENT_ID, CART.USERID FROM CART_REVISIONS (nolock) INNER JOIN CART2 (nolock) ON CART_REVISIONS.CART_ID = CART2.CartId INNER JOIN CART(NOLOCK) ON CART.CART_ID = CART2.CartId WHERE CART2.CARTCOMPOSITENUMBER = '{}'  and REVISION_ID  = '{}' ".format(Quote.CompositeNumber,newrev_inc))
        #HPQC 1642 start
        exchange_obj = Sql.GetFirst("SELECT EXCHANGE_RATE,RATIO_FROM,RATIO_TO,EXCHANGE_RATE_BEGIN_DATE,EXCHANGE_RATE_END_DATE,EXCHANGE_RATE_RECORD_ID from PREXRT where FROM_CURRENCY = '{}' and TO_CURRENCY='{}' AND ACTIVE = 1 and EXCHANGE_RATE_TYPE = '{}'".format(get_previous_rev_data.GLOBAL_CURRENCY,get_previous_rev_data.DOC_CURRENCY,get_previous_rev_data.EXCHANGE_RATE_TYPE))
        if exchange_obj:
            if exchange_obj.RATIO_FROM > 1:
                exchange_val = exchange_obj.EXCHANGE_RATE/exchange_obj.RATIO_FROM
            elif exchange_obj.RATIO_TO > 1:
                exchange_val = exchange_obj.EXCHANGE_RATE*exchange_obj.RATIO_TO
            else:
                exchange_val = exchange_obj.EXCHANGE_RATE
        else:
            exchange_val = 1.00
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
                "EXCHANGE_RATE_TYPE" : get_previous_rev_data.EXCHANGE_RATE_TYPE,
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
                "QT_PAYMENTTERM_DAYS": get_previous_rev_data.PAYMENTTERM_DAYS,
                "QT_PAYMENTTERMS_ID": get_previous_rev_data.PAYMENTTERM_ID,
                "QT_PAYMENTTERM_NAME": get_previous_rev_data.PAYMENTTERM_NAME,
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
        CQCPQC4CWB.writeback_to_c4c("quote_header",Quote.GetGlobal("contract_quote_record_id"),Quote.GetGlobal("quote_revision_record_id"))
        CQCPQC4CWB.writeback_to_c4c("opportunity_header",Quote.GetGlobal("contract_quote_record_id"),Quote.GetGlobal("quote_revision_record_id"))
        
        ##Calling the iflow for quote header writeback to cpq to c4c code ends...
        
        quote_table_info = Sql.GetTable("SAQTMT")
        if get_quote_info_details:
            quote_detials = ''
            #update SAQTMT start
            Sql.RunQuery("""UPDATE SAQTMT SET QTEREV_ID = {newrev_inc},QTEREV_RECORD_ID = '{quote_revision_id}',ACTIVE_REV={active_rev} WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{QuoteRecordId}'""".format(quote_revision_id=quote_revision_id,newrev_inc= newrev_inc,QuoteRecordId=quote_contract_recordId,active_rev = 1))
            #update SAQTMT end
            
            ##Calling the iflow for quote header writeback to cpq to c4c code starts..
            Log.Info("===> writeback_to_c4c calling from new Revision===> ")
            CQCPQC4CWB.writeback_to_c4c("quote_header",Quote.GetGlobal("contract_quote_record_id"),quote_revision_id)
            CQCPQC4CWB.writeback_to_c4c("opportunity_header",Quote.GetGlobal("contract_quote_record_id"),quote_revision_id)
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
                if 'SERVICE_ID' in table_cols:
                    service_level_where_condition = " AND SERVICE_ID != 'Z0105'"
                selectcols += " FROM "+ str(cloneobjectname) +" WHERE QUOTE_RECORD_ID='{}'".format(str(quote_contract_recordId))+" AND QTEREV_ID={}".format(int(old_revision_no)) + service_level_where_condition
                # A055S000P01-17876 - End
                finalquery=insertval + insertcols +' '+ selectval + selectcols
                Trace.Write(finalquery)
                ExecObjQuery = Sql.RunQuery(finalquery)
                # Remove CBC details during clone
                if cloneobjectname == 'SAQCBC':
                    Sql.RunQuery("UPDATE SAQCBC SET SERVICE_CONTRACT = 'False', SPECIALIST_REVIEW = 'False' FROM SAQCBC WHERE QUOTE_RECORD_ID='{}' AND QTEREV_ID={}".format(quote_contract_recordId, newrev_inc))
                elif cloneobjectname == 'SAQSPT':
                    Sql.RunQuery("UPDATE SAQSPT SET CUSTOMER_ANNUAL_QUANTITY = NULL,EXTENDED_UNIT_PRICE = NULL,UNIT_PRICE = NULL, CORE_CREDIT_PRICE=NULL,PRICING_STATUS='NOT PRICED'  FROM SAQSPT WHERE QUOTE_RECORD_ID='{}' AND QTEREV_ID={}".format(quote_contract_recordId, newrev_inc))                    
                elif cloneobjectname == 'SAQRSP':
                    Sql.RunQuery("UPDATE SAQRSP SET PRICING_STATUS='NOT PRICED',EXTENDED_PRICE = NULL,UNIT_PRICE = NULL,EXTENDED_PRICE_INGL_CURR = NULL ,QUANTITY = NULL,UNIT_PRICE_INGL_CURR = NULL FROM SAQRSP WHERE QUOTE_RECORD_ID='{}' AND QTEREV_ID={}".format(quote_contract_recordId, newrev_inc))
                    
            
            ## SAQSCO (QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID) MAPPED INTO  SAQSCE (QTESRVCOB_RECORD_ID):
            updatestatement = """UPDATE B SET B.QTESRVCOB_RECORD_ID = A.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID FROM SAQSCO A JOIN SAQSCE B ON A.EQUIPMENT_ID=B.EQUIPMENT_ID AND A.SERVICE_ID=B.SERVICE_ID AND A.FABLOCATION_ID=B.FABLOCATION_ID AND A.QUOTE_ID=B.QUOTE_ID AND A.SERIAL_NO=B.SERIAL_NO WHERE A.QTEREV_ID={} AND B.QTEREV_ID={} AND A.QUOTE_RECORD_ID=''{}'' AND B.QUOTE_RECORD_ID=''{}'' """.format(int(newrev_inc),int(newrev_inc),str(quote_contract_recordId),str(quote_contract_recordId))

            ##SAQFEQ (QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID) MAPPED TO SAQSCO (QTEREVFEQ_RECORD_ID)
            updatestatement2 = """UPDATE SAQSCO SET QTEREVFEQ_RECORD_ID = QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID FROM SAQSCO INNER JOIN SAQFEQ ON SAQSCO.QUOTE_RECORD_ID = SAQFEQ.QUOTE_RECORD_ID AND SAQSCO.QTEREV_RECORD_ID = SAQFEQ.QTEREV_RECORD_ID AND SAQSCO.FABLOCATION_ID = SAQFEQ.FABLOCATION_ID AND SAQSCO.GREENBOOK = SAQFEQ.GREENBOOK AND SAQSCO.EQUIPMENT_ID = SAQFEQ.EQUIPMENT_ID  WHERE SAQSCO.QUOTE_RECORD_ID = ''{}'' AND SAQSCO.QTEREV_ID  = ''{}'' """.format(str(quote_contract_recordId),int(newrev_inc))

            ### SAQTSV (QUOTE_SERVICE_RECORD_ID) MAPPED INTO  SAQTSE (QTESRV_RECORD_ID):
            updatestatement1 = """UPDATE B SET B.QTESRV_RECORD_ID = A.QUOTE_SERVICE_RECORD_ID FROM SAQTSV A JOIN SAQTSE B ON A.SERVICE_ID=B.SERVICE_ID AND A.QTEREV_RECORD_ID=B.QTEREV_RECORD_ID AND A.QUOTE_ID=B.QUOTE_ID  WHERE A.QTEREV_ID={} AND B.QTEREV_ID={} AND A.QUOTE_RECORD_ID=''{}'' AND B.QUOTE_RECORD_ID=''{}'' """.format(int(newrev_inc),int(newrev_inc),str(quote_contract_recordId),str(quote_contract_recordId))

            ##SAQSGE QTESRVGBK_RECORD_ID MAPPED FROM SAQSGB QUOTE_SERVICE_GREENBOOK_RECORD_ID
            updatestatement3 = """UPDATE B SET B.QTESRVGBK_RECORD_ID = A.QUOTE_SERVICE_GREENBOOK_RECORD_ID FROM SAQSGB A JOIN SAQSGE B ON A.GREENBOOK=B.GREENBOOK AND A.SERVICE_ID=B.SERVICE_ID AND A.QUOTE_ID=B.QUOTE_ID  AND A.QTEREV_ID = B.QTEREV_ID WHERE A.QTEREV_ID={} AND B.QTEREV_ID={} AND A.QUOTE_RECORD_ID=''{}'' AND B.QUOTE_RECORD_ID=''{}'' """.format(int(newrev_inc),int(newrev_inc),str(quote_contract_recordId),str(quote_contract_recordId))

            query_result = SqlHelper.GetFirst("sp_executesql @statement = N'" + str(updatestatement) + "'")
            query_result1 = SqlHelper.GetFirst("sp_executesql @statement = N'" + str(updatestatement1) + "'")
            query_result2 = SqlHelper.GetFirst("sp_executesql @statement = N'" + str(updatestatement2) + "'")
            query_result3 = SqlHelper.GetFirst("sp_executesql @statement = N'" + str(updatestatement3) + "'")
            Trace.Write(query_result)
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
        
        # APPROVALS - NEW REVISION END
        Quote.Save()
        #Quote.RefreshActions()
        current_revison1 = Quote.RevisionNumber
        
        get_quote_info_details = Sql.GetFirst("select * from SAQTMT where QUOTE_ID = '"+str(Quote.CompositeNumber)+"'")
        Quote.SetGlobal("contract_quote_record_id",get_quote_info_details.MASTER_TABLE_QUOTE_RECORD_ID)
        Quote.SetGlobal("quote_revision_record_id",str(get_quote_info_details.QTEREV_RECORD_ID))
        ##newrevision edot active for expiry Quote:A055S000P01-14308
        updatesaqtmtexpire = (""" UPDATE SAQTMT SET EXPIRED = 0 FROM SAQTMT INNER JOIN SAQTRV ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQTRV.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = SAQTRV.QTEREV_RECORD_ID WHERE  SAQTRV.REV_CREATE_DATE = '{current_date}' AND SAQTRV.QTEREV_RECORD_ID ='{quote_revision_record_id}' AND SAQTRV.QUOTE_RECORD_ID = '{contract_quote_record_id}'  AND ACTIVE = '1' """.format(current_date = current_date,quote_revision_record_id=get_quote_info_details.QTEREV_RECORD_ID,contract_quote_record_id =get_quote_info_details.MASTER_TABLE_QUOTE_RECORD_ID))
        Sql.RunQuery(updatesaqtmtexpire)
        CQREVSTSCH.Revisionstatusdatecapture(Quote.GetGlobal("contract_quote_record_id"),str(get_quote_info_details.QTEREV_RECORD_ID),)
        
        ##A055S000P01-19173 code starts..
        ##Calling the below script to retrieve and update the events from sscm while creating new revision....		
        service_object = Sql.GetList("SELECT SERVICE_ID FROM SAQTSV WHERE QUOTE_ID = '{Quote_id}' and QTEREV_ID = {newrev_inc}".format(Quote_id =Quote.CompositeNumber, newrev_inc = newrev_inc))
        for service in service_object:
            service_id = service.SERVICE_ID						
            service_entitlement_obj =Sql.GetFirst("""select ENTITLEMENT_XML from SAQTSE (nolock) where QUOTE_ID = '{Quote_id}' AND QTEREV_ID = '{RevisionId}' and SERVICE_ID = '{service_id}' """.format(Quote_id =Quote.CompositeNumber,RevisionId=newrev_inc,service_id = service.SERVICE_ID))
            quote_type_value = ""
            if service_entitlement_obj is not None:
                entitlement_xml = service_entitlement_obj.ENTITLEMENT_XML
                pattern_tag = re.compile(r'(<QUOTE_ITEM_ENTITLEMENT>[\w\W]*?</QUOTE_ITEM_ENTITLEMENT>)')
                pattern_name = re.compile(r'<ENTITLEMENT_DISPLAY_VALUE>([^>]*?)</ENTITLEMENT_DISPLAY_VALUE>')
                quote_type_id = re.compile(r'<ENTITLEMENT_ID>AGS_[^>]*?_PQB_QTETYP</ENTITLEMENT_ID>')
                for value in re.finditer(pattern_tag, entitlement_xml):
                    sub_string = value.group(1)
                    quote_type_attribute_id =re.findall(quote_type_id,sub_string)
                    if quote_type_attribute_id:
                        quote_type_value =re.findall(pattern_name,sub_string)
                        QuoteTypeValue = quote_type_value[0]
                        ScriptExecutor.ExecuteGlobal(
                                            "CQCRUDOPTN",
                                            {
                                                "NodeType": "COVERED OBJ MODEL",
                                                "Opertion": "ADD",
                                                "NewRevision": "YES",
                                                "QuoteTypeValue": QuoteTypeValue,
                                                "ServiceId": service_id,
                                                "RealTimeIntegrationService":service_id,
                                            },
                                        )
                        # Log.Info("Script Ended"+str(service.QUOTE_ID)+'-'+str(newrev_inc))				
                ##A055S000P01-19173 code ends..	

    return True



#set active revision  from grid- start
def set_active_revision(Opertion,cartrev):
    recid = ''
    Trace.Write('223----cartrev----'+str(cartrev))
    #for val in select_active:
    ObjectName = cartrev.split('-')[0].strip()
    cpqid = cartrev.split('-')[1].strip()
    #recid = CPQID.KeyCPQId.GetKEYId(ObjectName,str(cpqid))
    get_rev_quote_info_details = Sql.GetFirst("select * from SAQTRV where QUOTE_ID = '{}' and QTEREV_ID = {}".format(ObjectName,cpqid))
    if get_rev_quote_info_details:
        recid = get_rev_quote_info_details.QUOTE_REVISION_RECORD_ID
        get_quote_info_details = Sql.GetFirst("select * from SAQTMT where MASTER_TABLE_QUOTE_RECORD_ID = '"+str(quote_contract_recordId)+"'")
        Quote.SetGlobal("contract_quote_record_id",quote_contract_recordId)
        Sql.RunQuery("""UPDATE SAQTRV SET ACTIVE = {active_rev} WHERE QUOTE_RECORD_ID = '{QuoteRecordId}'""".format(QuoteRecordId=quote_contract_recordId,active_rev = 0))
        Sql.RunQuery("""UPDATE SAQTRV SET ACTIVE = {active_rev} WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' and QUOTE_REVISION_RECORD_ID = '{recid}'""".format(QuoteRecordId=quote_contract_recordId,active_rev = 1,recid =recid))
        get_rev_info_details = Sql.GetFirst("select QTEREV_ID,CART_ID,ADDUSR_RECORD_ID from SAQTRV where QUOTE_RECORD_ID = '"+str(quote_contract_recordId)+"' and QUOTE_REVISION_RECORD_ID = '"+str(recid)+"'")
        gtcart_idval = get_rev_info_details.CART_ID
        Sql.RunQuery("""UPDATE SAQTMT SET QTEREV_ID = {newrev_inc},QTEREV_RECORD_ID = '{quote_revision_id}',ACTIVE_REV={active_rev} WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{QuoteRecordId}'""".format(quote_revision_id=recid,newrev_inc= get_rev_info_details.QTEREV_ID,QuoteRecordId=quote_contract_recordId,active_rev = 1))
        Quote.SetGlobal("quote_revision_record_id",recid)
        GETCARTID=SqlHelper.GetFirst("sp_executesql @t = N'update CART set ACTIVE_REV =''0'' WHERE CART_ID in (select distinct top 10 CART_REVISIONS.CART_ID as ID from CART_REVISIONS (nolock) INNER JOIN CART2 (nolock) ON CART_REVISIONS.CART_ID = CART2.CartId AND CART_REVISIONS.VISITOR_ID = CART2.OwnerId INNER JOIN CART(NOLOCK) ON CART.CART_ID = CART2.CartId and CART.USERID = CART2.OwnerId WHERE CART2.CartCompositeNumber = ''"+ str(Quote.CompositeNumber)+ "'') '")
        UPDATEACTIVE = SqlHelper.GetFirst("sp_executesql @t=N'update CART set ACTIVE_REV =''1'' where CART_ID = ''"+str(gtcart_idval)+"'' and USERID =''"+str(User.Id)+"'' '")
        cart_obj = SqlHelper.GetList("SELECT DATE_CREATED, USERID, CART_ID, ACTIVE_REV FROM cart WHERE ExternalId = '{}' AND ACTIVE_REV = 1".format(get_quote_info_details.QUOTE_ID)) 
        if not cart_obj:
            UPDATEACTIVE = SqlHelper.GetFirst("sp_executesql @t=N'update CART set ACTIVE_REV =''1'' where CART_ID = ''"+str(gtcart_idval)+"'' and ExternalId =''"+str(get_quote_info_details.QUOTE_ID)+"'''")
        NRev = QuoteHelper.Edit(get_quote_info_details.QUOTE_ID)
        
        time.sleep( 5 )
        Quote.RefreshActions()
        ##assigning active revision custom field value
        # get_act_rev_custom_val = SqlHelper.GetFirst("select globals from cart where  ExternalId = '{}' and cart_id ='{}' and userid = '{}'".format(quote_contract_recordId, get_rev_info_details.CART_ID, Quote.UserId ))
        # cust_list = ['TARGET_PRICE','CEILING_PRICE','TOTAL_COST','CEILING_PRICE','SALES_DISCOUNTED_PRICE','BD_PRICE_MARGIN','BD_PRICE_DISCOUNT','TOTAL_NET_PRICE','YEAR_OVER_YEAR','YEAR_1','YEAR_2','TAX','TOTAL_NET_VALUE','MODEL_PRICE','BD_PRICE','DISCOUNT']
        # if get_act_rev_custom_val:
        # 	for i in cust_list:
        # 		#a = "TOTAL_COST:0.0 USD,TOTAL_NET_PRICE:0.0 USD,DISCOUNT:60 %25,"
        # 		val = re.findall(r''+i+':[\w\W]*?,', get_act_rev_custom_val.globals)
        # 		val = str(val[0][:-1].split(':')[1].strip() )
        # 		Trace.Write('res-'+str(val) )
        # 		Quote.GetCustomField(i).Content = val
                        
        get_quote_info_details = Sql.GetFirst("select * from SAQTMT where QUOTE_ID = '"+str(Quote.CompositeNumber)+"'")
        Quote.SetGlobal("contract_quote_record_id",get_quote_info_details.MASTER_TABLE_QUOTE_RECORD_ID)
        Quote.SetGlobal("quote_revision_record_id",str(get_quote_info_details.QTEREV_RECORD_ID))
        ##Calling the iflow for quote header writeback to cpq to c4c code starts..
        CQCPQC4CWB.writeback_to_c4c("quote_header",Quote.GetGlobal("contract_quote_record_id"),Quote.GetGlobal("quote_revision_record_id"))
        CQCPQC4CWB.writeback_to_c4c("opportunity_header",Quote.GetGlobal("contract_quote_record_id"),Quote.GetGlobal("quote_revision_record_id"))
        ##Calling the iflow for quote header writeback to cpq to c4c code ends...		
    return True
#set active revision  from grid- end


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
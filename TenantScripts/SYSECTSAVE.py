# =========================================================================================================================================
#   __script_name : SYSECTSAVE.PY
#   __script_description :  THIS SCRIPT IS USED TO SAVE THE SEGMENT DATA AND MATERIAL DATA IN CUSTOM TABLES DURING ADD NEW OR EDIT
#   __primary_author__ : JOE EBENEZER
#   __create_date :
#   Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import SYTABACTIN as Table
import Webcom.Configurator.Scripting.Test.TestProduct
import SYCNGEGUID as CPQID
import System.Net
#import PRIFLWTRGR
from datetime import datetime,date
#import datetime
from SYDATABASE import SQL
import CQCPQC4CWB
#import CQREVSTSCH
import re
import time
import CQREVSTSCH
Sql = SQL()
#from PAUPDDRYFG import DirtyFlag
from System import Convert
from System.Text.Encoding import UTF8
import re
#from datetime import datetime

login_is_admin = User.IsAdmin

def MaterialSave(ObjectName, RECORD, warning_msg, SectionRecId=None,subtab_name=None):
    row = ""
    result = ""
    RecordId = ""
    disc = []
    newdict = {}
    next_val = ""
    cp_con_factor_result = notification = notificationinterval = ""
    cp_con_factor = ""
    SecRecId = ""
    pricing_sap_prt_num = ""
    RECORD = eval(RECORD)
    billstart = ""
    constartdt = ""
    conenddt = ""
    contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
    quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
    TreeParam = Product.GetGlobal("TreeParam")
    if subtab_name =="Legal SoW":
        get_revesion_values =Sql.GetFirst("Select * FROM SAQTRV WHERE QUOTE_REVISION_RECORD_ID = '{quote_revision_record_id}'".format(quote_revision_record_id = quote_revision_record_id))
        record_value_update = {"QUOTE_REVISION_RECORD_ID":quote_revision_record_id,"QTEREV_ID":get_revesion_values.QTEREV_ID,"REVISION_STATUS":get_revesion_values.REVISION_STATUS,"REV_APPROVE_DATE":get_revesion_values.REV_APPROVE_DATE}
        RECORD.update(record_value_update)

        ##Calling the iflow script to update the details in c4c..(cpq to c4c write back...)
        CQCPQC4CWB.writeback_to_c4c("quote_header",Quote.GetGlobal("contract_quote_record_id"),Quote.GetGlobal("quote_revision_record_id"))
        #time.sleep(5)
        CQCPQC4CWB.writeback_to_c4c("opportunity_header",Quote.GetGlobal("contract_quote_record_id"),Quote.GetGlobal("quote_revision_record_id"))
    
    if Product.GetGlobal("TreeParentLevel2") == "Quote Items":
        ObjectName = "SAQIGB"
    elif Product.GetGlobal("TreeParentLevel1") == "Quote Items":
        ObjectName = "SAQIFL"
    # elif Product.GetGlobal("TreeParentLevel0") == "Quote Items":
    # 	ObjectName = "SAQITM"
    # 	sect_name = RECORD.get("SECTION_ID")
    # 	Trace.Write("section name = "+str(sect_name))
    # INC08642678 - Start - M
    elif Product.GetGlobal("TreeParentLevel1") == "Product Offerings" and subtab_name == "Periods":
        ObjectName = "SAQRDS"
        RECORD.pop('CPQTABLEENTRYMODIFIEDBY')
        RECORD.pop('CPQTABLEENTRYDATEMODIFIED')
    # INC08642678 - End - M
    elif Product.GetGlobal("TreeParentLevel1") == "Product Offerings":
        ObjectName = "SAQTSV"
    elif Product.GetGlobal("TreeParentLevel2") == "Product Offerings"  and subtab_name == "Details":
        ObjectName = "SAQSGB"
    elif Product.GetGlobal("TreeParentLevel2") == "Product Offerings":
        ObjectName = "SAQSFB"
    elif Product.GetGlobal("TreeParentLevel3") == "Product Offerings" and subtab_name == "Details":
        ObjectName = "SAQSGB"
    if (Product.GetGlobal("TreeParentLevel3") == "Product Offerings" or Product.GetGlobal("TreeParentLevel2") == "Product Offerings") and subtab_name == "Equipment Details":
        ObjectName = "SAQSCO"
    Trace.Write("SubTab_Name "+str(subtab_name))
    Trace.Write("RECORD_RECORD "+str(RECORD))
    if str(ObjectName) == "SYPRSN":
        
        permissions_id_val = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00128").GetValue()
        sect_edit = RECORD.get("EDITABLE")
        
        VISIBLEval = RECORD.get("VISIBLE")
        sect_name = RECORD.get("SECTION_ID")
        Trace.Write("section name = "+str(sect_name))
        sect_rec_id = RECORD.get("PROFILE_SECTION_RECORD_ID")
        tableInfosf = Sql.GetTable("SYPRSF")
        newdictSF = {}
        getsection_record = CPQID.KeyCPQId.GetKEYId('SYPRSN', sect_rec_id)
        querySYPRsn = Sql.GetFirst(
            "Select SECTION_RECORD_ID,CpqTableEntryId from SYPRSN where PROFILE_ID = '"
            + str(permissions_id_val)
            + "' and PROFILE_SECTION_RECORD_ID = '"
            + str(getsection_record)
            + "'"
        )
        newdictsn = {}

        if querySYPRsn:
            TableName = 'SYPRSN'
            tableInfo = Sql.GetTable(TableName)
            newdictsn.update({"CpqTableEntryId": str(querySYPRsn.CpqTableEntryId),"VISIBLE": str(VISIBLEval),"EDITABLE": str(sect_edit)})                
            tableInfo.AddRow(newdictsn)
            Sql.Upsert(tableInfo)
            querySYPRsf = Sql.GetList(
                "Select * from SYPRSF where PROFILE_ID = '"
                + str(permissions_id_val)
                + "' and SECTION_RECORD_ID = '"
                + str(querySYPRsn.SECTION_RECORD_ID)
                + "'"
            )
            for val in querySYPRsf:
                
                newdictSF["VISIBLE"] = str(VISIBLEval)
                newdictSF["EDITABLE"] = str(sect_edit)
                newdictSF["CpqTableEntryId"] = val.CpqTableEntryId
                
                
                tablerow = newdictSF
                tableInfosf.AddRow(tablerow)
                Sql.Upsert(tableInfosf)
    if str(ObjectName) == "SYPROH":
        
        permissions_id_val = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00128").GetValue()
        objName = RECORD.get("OBJECT_NAME")
        # permissions_id_val = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00128").GetValue()
        
        VISIBLEval = RECORD.get("VISIBLE")
        ObjectNameSection = RECORD.get("OBJECT_NAME")
        CAN_EDIT_VAL = RECORD.get("CAN_EDIT")
        Trace.Write("permissions_id_val--->" + str(permissions_id_val))
        Trace.Write("ObjectNameSection--->" + str(ObjectNameSection))
        CAN_DELETE_VAL = RECORD.get("CAN_DELETE")
        CAN_ADD_VAL = RECORD.get("CAN_ADD")
        Trace.Write(str(CAN_DELETE_VAL) + "40----CAN_EDIT_VAL-----" + str(CAN_EDIT_VAL))
        tableInfo = Sql.GetTable("SYPROD")
        newdict = {}
        newdictH = {}
        newdictF = {}
        tableInfoH = Sql.GetTable("SYPROH")
        querySYPROH = Sql.GetList(
            "Select * from SYPROH where PROFILE_ID = '"
            + str(permissions_id_val)
            + "' and OBJECT_NAME = '"
            + str(objName)
            + "'"
        )
        if querySYPROH:
            
            for val in querySYPROH:
                if VISIBLEval == "true":
                    
                    newdictH["VISIBLE"] = VISIBLEval
                    newdictH["CAN_EDIT"] = CAN_EDIT_VAL
                    newdictH["CAN_ADD"] = CAN_ADD_VAL
                    newdictH["CAN_DELETE"] = CAN_DELETE_VAL
                    newdictH["CpqTableEntryId"] = val.CpqTableEntryId
                else:
                    
                    newdictH["VISIBLE"] = VISIBLEval
                    newdictH["CAN_EDIT"] = VISIBLEval
                    newdictH["CAN_ADD"] = VISIBLEval
                    newdictH["CAN_DELETE"] = VISIBLEval
                    newdictH["CpqTableEntryId"] = val.CpqTableEntryId
                tablerow = newdictH
                tableInfoH.AddRow(tablerow)
            Sql.Upsert(tableInfoH)
        tableInfoSF = Sql.GetTable("SYPRSF")
        
        querySYPRSF = Sql.GetList(
            "Select * from SYPRSF where PROFILE_ID = '"
            + str(permissions_id_val)
            + "' and OBJECT_NAME = '"
            + str(objName)
            + "'"
        )
        if querySYPRSF:
            for val in querySYPRSF:
                if VISIBLEval == 1:
                    newdictF["VISIBLE"] = VISIBLEval
                    newdictF["EDITABLE"] = CAN_EDIT_VAL
                    newdictF["CpqTableEntryId"] = val.CpqTableEntryId
                else:
                    newdictF["VISIBLE"] = VISIBLEval
                    newdictF["EDITABLE"] = VISIBLEval
                    newdictF["CpqTableEntryId"] = val.CpqTableEntryId
                # Trace.Write("newdictF--" + str(newdictF))
                tablerow = newdictF
                tableInfoSF.AddRow(tablerow)
            Sql.Upsert(tableInfoSF)
        tableInfoSN = Sql.GetTable("SYPRSN")
        querySYPRSN = Sql.GetList(
            "Select * from SYPRSN where PROFILE_ID = '"
            + str(permissions_id_val)
            + "' and OBJECT_NAME = '"
            + str(objName)
            + "'"
        )
        if querySYPRSN:
            for val in querySYPRSN:
                
                if VISIBLEval == 1:
                    newdictF["VISIBLE"] = VISIBLEval
                    newdictF["EDITABLE"] = CAN_EDIT_VAL
                    newdictF["CpqTableEntryId"] = val.CpqTableEntryId
                else:
                    newdictF["VISIBLE"] = VISIBLEval
                    newdictF["EDITABLE"] = VISIBLEval
                    newdictF["CpqTableEntryId"] = val.CpqTableEntryId
                tablerow = newdictF
                tableInfoSN.AddRow(tablerow)
            Sql.Upsert(tableInfoSN)

        querySYPROD = Sql.GetList(
            "Select * from SYPROD where PROFILE_ID = '"
            + str(permissions_id_val)
            + "' and OBJECT_NAME = '"
            + str(objName)
            + "'"
        )
        if querySYPROD:
            
            for val in querySYPROD:
                if VISIBLEval == 1:
                    newdict["VISIBLE"] = VISIBLEval
                    newdict["EDITABLE"] = CAN_EDIT_VAL

                    newdict["CpqTableEntryId"] = val.CpqTableEntryId
                else:
                    newdict["VISIBLE"] = VISIBLEval
                    newdict["EDITABLE"] = VISIBLEval

                    newdict["CpqTableEntryId"] = val.CpqTableEntryId
                tablerow = newdict
                tableInfo.AddRow(tablerow)
            Sql.Upsert(tableInfo)
        tableInfTB = Sql.GetTable("SYPRTB")
        get_tab_rec = Sql.GetList(
            "Select SYPAGE.TAB_RECORD_ID from SYSECT (NOLOCK) INNER JOIN SYPAGE (NOLOCK) on SYSECT.PAGE_RECORD_ID = SYPAGE.RECORD_ID where PRIMARY_OBJECT_NAME = '"
            + str(ObjectNameSection)
            + "'"
        )
        newdictTB = {}

        
        if get_tab_rec:
            for val in get_tab_rec:
                if str(val.TAB_RECORD_ID):
                    
                    permissions_id_val = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00128").GetValue()
                    querytab = Sql.GetList(
                        "SELECT CpqTableEntryId from SYPRTB WHERE TAB_RECORD_ID='"
                        + str(val.TAB_RECORD_ID)
                        + "' and PROFILE_ID = '"
                        + str(permissions_id_val)
                        + "'"
                    )
                    if querytab:
                        
                        for val in querytab:
                            
                            newdictTB["VISIBLE"] = VISIBLEval

                            newdictTB["CpqTableEntryId"] = val.CpqTableEntryId
                        tablerow = newdictTB
                        tableInfTB.AddRow(tablerow)
                    Sql.Upsert(tableInfTB)

    

    ACCOUNT_ID = ""
    ACCOUNT_NAME = ""
    ACCOUNT_RECORD_ID = ""
    cp_con_factor = Metal = CustomValue = ""
    cp_con_factor_result = (
        ErrorequiredDict
    ) = (
        ErrorequiredtabDictMSg
    ) = (
        ErrorequiredDictMSg
    ) = (
        nSpotPriceSpa
    ) = (
        nCustomSPAUnits
    ) = nAdjSPAUnits = nSpotPriceGpa = nCustomGPAUnits = nAdjGPAUnits = Points_curr_ex_rate_date = Points_curr_ex_rate = ""
    TableName = ObjectName
    Trace.Write("TableName=====>" + str(TableName))
    CURRENCY_SYMBOL = Sql.GetFirst("SELECT CURRENCY_RECORD_ID FROM PRCURR(NOLOCK) WHERE CURRENCY = 'USD'")
    #CURRENCY_SYMBOL_VALUE = CURRENCY_SYMBOL.CURRENCY_RECORD_ID
    if TableName == "SAQIGS":
        TableName = "SAQRIB"
    if TableName != "":
        Trace.Write("SELECT API_NAME FROM SYOBJD WHERE DATA_TYPE = 'AUTO NUMBER' AND OBJECT_NAME = '" + str(TableName) + "'")
        TABLE_OBJS = Sql.GetFirst(
            "SELECT API_NAME FROM SYOBJD WHERE DATA_TYPE = 'AUTO NUMBER' AND OBJECT_NAME = '" + str(TableName) + "'"
        )
        AutoNumb = TABLE_OBJS.API_NAME
        RECID_OBJ = RECORD[str(AutoNumb)]
        RECID_OBJ_SLICE = RECID_OBJ[slice(0, 6)]
        if RECID_OBJ_SLICE == str(TableName):
            RECID = CPQID.KeyCPQId.GetKEYId(str(TableName), str(RECID_OBJ))
        else:
            RECID = RECID_OBJ
        

        RECORD.update({str(AutoNumb): str(RECID)})
        if str(ObjectName) == "ACACSS":
            RECORD.update({"APROBJ_STATUSFIELD_VAL" : RECORD.get("APROBJ_STATUSFIELD_VAL").upper()})
            Trace.Write("Testing ACACSS----" + RECORD.get("APROBJ_STATUSFIELD_VAL"))
        elif str(ObjectName) == "ACACST":
            Trace.Write("Table name------" + str(ObjectName))
            RECORD["APRCHNSTP_NAME"] = str(RECORD.get("APRCHNSTP_NAME").upper())
            if RECORD["REQUIRE_EXPLICIT_APPROVAL"] =='false':
                RECORD["ENABLE_SMARTAPPROVAL"] ='true'
            elif RECORD["REQUIRE_EXPLICIT_APPROVAL"] =='true':
                RECORD["ENABLE_SMARTAPPROVAL"] = 'false'
            Trace.Write("APRCHNSTP_NAME-----"+ str(RECORD["APRCHNSTP_NAME"]))

        
        if str(TableName) == "USERS":
            
            RECORD.pop("RECORDID")
        
        Trace.Write("SELECT * FROM " + str(TableName) + " WHERE " + str(AutoNumb) + "='" + str(RECID) + "'")
        sql_cpq = Sql.GetFirst("SELECT * FROM " + str(TableName) + " WHERE " + str(AutoNumb) + "='" + str(RECID) + "'")
        Trace.Write("SELECT * FROM " + str(TableName) + " WHERE " + str(AutoNumb) + "='" + str(RECID) + "'")
        sql_sgs = Sql.GetList("SELECT API_NAME FROM SYOBJD WHERE OBJECT_NAME='" + str(TableName) + "'")
        if sql_cpq is not None:
            for attr in sql_sgs:
                for KEY in RECORD:
                    if str(attr.API_NAME) == KEY:
                        newdict[attr.API_NAME] = RECORD[KEY]
                    else:
                        if str(attr.API_NAME) == "PRICEMODEL_ID":
                            KEY = "PRICEMODEL_ID"
                            newdict[attr.API_NAME] = RECORD[KEY] if str(TableName) != "PRPBMA" else RECORD[KEY + "_VALUE"]
            
            if str(TableName) != "USERS":
                old_billing_matrix_obj = None
                # if TableName == 'SAQRIB':
                # 	billenddate = RECORD.get('BILLING_END_DATE')
                # 	billstartdt = RECORD.get('BILLING_START_DATE')
                # 	billingdateinterval = RECORD.get('BILLING_DAY')
                # 	billstart = datetime.datetime.strptime(billstartdt, '%m/%d/%Y ')
                # 	constart = Product.Attributes.GetByName("QSTN_SYSEFL_QT_00006").GetValue()
                # 	conend = Product.Attributes.GetByName("QSTN_SYSEFL_QT_00007").GetValue()
                # 	billend = datetime.datetime.strptime(billenddate, '%m/%d/%Y ')
                # 	constartdt = datetime.datetime.strptime(constart, '%m/%d/%Y ')
                # 	conenddt = datetime.datetime.strptime(conend, '%m/%d/%Y ')
                # 	old_billing_matrix_obj = Sql.GetFirst("""SELECT BILLING_START_DATE, 
                # 					BILLING_END_DATE, QUOTE_BILLING_PLAN_RECORD_ID, BILLING_DAY
                # 					FROM SAQRIB (NOLOCK) 
                # 					WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'""".format(Product.GetGlobal("contract_quote_record_id"),quote_revision_record_id))
                if TableName:
                    
                    if TableName == "SAQTRV":
                        dictc = {"CpqTableEntryId": str(sql_cpq.CpqTableEntryId)}
                        newdict.update(dictc)
                        tableInfo = Sql.GetTable(str(TableName))
                        Trace.Write('subtab_name---'+str(subtab_name))
                        #get_previous_payment_term =Sql.GetFirst("SELECT PAYMENTTERM_ID FROM SAQTRV(NOLOCK) WHERE QUOTE_RECORD_ID ='{contract_quote_record_id}' AND QTEREV_RECORD_ID ='{quote_revision_record_id}'".format(contract_quote_record_id =contract_quote_record_id,quote_revision_record_id =quote_revision_record_id))
                        #payment_term_name_previous = get_previous_payment_term.PAYMENTTERM_ID
                        if subtab_name not in  ("Legal SoW","Basic Information"):
                            #newdict["SLSDIS_PRICE_INGL_CURR"] = re.sub('USD','',newdict["SLSDIS_PRICE_INGL_CURR"])
                            #current_payment_term = newdict.get("PAYMENTTERM_ID")
                            #if current_payment_term != payment_term_name_previous:
                            #	Trace.Write("current_payment_term"+str(current_payment_term))
                            #	Trace.Write("payment_term_name_previous"+str(payment_term_name_previous))
                            #	newdict["PAYMENTTERM_NAME_ISCHANGED"] = 'True'
                            #newdict["BD_PRICE_INGL_CURR"] = re.sub('USD','',newdict["BD_PRICE_INGL_CURR"])
                            #newdict["CEILING_PRICE_INGL_CURR"] = re.sub('USD','',newdict["CEILING_PRICE_INGL_CURR"])
                            # newdict["NET_PRICE_INGL_CURR"] = re.sub('USD','',newdict["NET_PRICE_INGL_CURR"])
                            newdict["TAX_AMOUNT_INGL_CURR"] = re.sub('USD','',newdict["TAX_AMOUNT_INGL_CURR"])
                            #newdict["TARGET_PRICE_INGL_CURR"] = re.sub('USD','',newdict["TARGET_PRICE_INGL_CURR"])
                            #newdict["NET_VALUE_INGL_CURR"] = re.sub('USD','',newdict["NET_VALUE_INGL_CURR"])
                            #newdict["DISCOUNT_AMOUNT_INGL_CURR"] = re.sub('USD','',newdict["DISCOUNT_AMOUNT_INGL_CURR"])
                            newdict["CANCELLATION_PERIOD_EXCEPTION"] = "" if newdict["CANCELLATION_PERIOD"]!="EXCEPTION" else newdict["CANCELLATION_PERIOD_EXCEPTION"]
                            #INC08872530 - Start - M
                            if sql_cpq.DOC_CURRENCY !=newdict.get("DOC_CURRENCY"):
                                exchange_rate_type = newdict.get("EXCHANGE_RATE_TYPE")
                                exchange_rate_object = Sql.GetFirst("SELECT  EXCHANGE_RATE,RATIO_FROM,RATIO_TO,EXCHANGE_RATE_BEGIN_DATE,EXCHANGE_RATE_RECORD_ID FROM PREXRT(NOLOCK) WHERE FROM_CURRENCY = '{}' AND TO_CURRENCY = '{}' AND ACTIVE = 1 AND EXCHANGE_RATE_TYPE = '{}' ".format(newdict.get("GLOBAL_CURRENCY"),newdict.get("DOC_CURRENCY"),newdict.get("EXCHANGE_RATE_TYPE")))
                                if exchange_rate_object:
                                    if exchange_rate_object.RATIO_FROM > 1:
                                        exchange_val = exchange_rate_object.EXCHANGE_RATE/exchange_rate_object.RATIO_FROM
                                    elif exchange_rate_object.RATIO_TO > 1:
                                        exchange_val = exchange_rate_object.EXCHANGE_RATE*exchange_rate_object.RATIO_TO
                                    else:
                                        exchange_val = exchange_rate_object.EXCHANGE_RATE
                                    newdict["EXCHANGE_RATE"] = exchange_val or ""
                                    newdict["EXCHANGERATE_RECORD_ID"] = exchange_rate_object.EXCHANGE_RATE_RECORD_ID or ""
                                else:
                                    #INC08614363 - M
                                    if newdict.get("GLOBAL_CURRENCY")==newdict.get("DOC_CURRENCY"):
                                        newdict["EXCHANGE_RATE"] = 1.00
                                    else:
                                        newdict["EXCHANGE_RATE"] = ''
                                    #INC08614363 - M
                                newdict["EXCHANGE_RATE_DATE"] = datetime.now().strftime("%m/%d/%Y")
                            #INC08872530 - End - M
                        tablerow = newdict
                        tableInfo.AddRow(tablerow)
                        try:
                            currency_query = Sql.GetFirst("SELECT CURRENCY_RECORD_ID FROM PRCURR (NOLOCK) WHERE CURRENCY = '{currency}'".format(currency=tablerow['DOC_CURRENCY']))
                            Sql.RunQuery("UPDATE SAQTRV SET DOCCURR_RECORD_ID = '{currency_rec_id}' WHERE QUOTE_RECORD_ID = '{quote_rec}' AND QTEREV_RECORD_ID = '{quote_rev_rec_id}'".format(currency_rec_id=currency_query.CURRENCY_RECORD_ID,quote_rec=Quote.GetGlobal("contract_quote_record_id") ,quote_rev_rec_id=Quote.GetGlobal("quote_revision_record_id")))
                        except:
                            Trace.Write("EXCEPTION OCCURED KEY NOT FOUNT DOC_CURRENCY")
                        Trace.Write("TEZTZ--475---"+str(tablerow))
                        Sql.Upsert(tableInfo)				
                        getactive = newdict.get("ACTIVE")
                        get_record_val =  newdict.get("QUOTE_REVISION_RECORD_ID")
                        get_rev_val =  newdict.get("QTEREV_ID")
                        get_approved_date = newdict.get("REV_APPROVE_DATE")
                        get_status = newdict.get("REVISION_STATUS")
                        if sql_cpq.REVISION_STATUS !="APR-APPROVED" and get_status == "APR-APPROVED":
                            Trace.Write('Mail Triggering for Contract Manager')
                            result = ScriptExecutor.ExecuteGlobal("ACSECTACTN", {"ACTION": "CBC_MAIL_TRIGGER"})
                        if getactive == 'false':
                            getactive = 0
                        else:
                            getactive = 1
                        contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
                        quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")

                        revision_desc = newdict.get("REVISION_DESCRIPTION")
                       #A055S000P01-20972
                        if revision_desc:
                            revision_desc = re.sub(r"[^a-zA-Z0-9 \n\.><&_-~',?]", '', revision_desc)
                            productdesc = SqlHelper.GetFirst("sp_executesql @t=N'update CART_REVISIONS set DESCRIPTION =''"+str(revision_desc)+"'' where CART_ID = ''"+str(Quote.QuoteId)+"'' and VISITOR_ID =''"+str(Quote.UserId)+"''  '")
                            get_quote_info_details = Sql.GetFirst("select * from SAQTMT where QUOTE_ID = '"+str(Quote.CompositeNumber)+"'")
                            Quote.SetGlobal("contract_quote_record_id",get_quote_info_details.MASTER_TABLE_QUOTE_RECORD_ID)
                            Quote.SetGlobal("quote_revision_record_id",str(get_quote_info_details.QTEREV_RECORD_ID))
                        #A055S000P01-20972
                        #getpaymentterm changes
                        #A055S000P01-17165 started
                        if get_status.upper() in ("APR-REJECTED","APR-RECALLED","APR-APPROVAL PENDING","APR-APPROVED"):
                            Sql.RunQuery("UPDATE SAQTRV SET WORKFLOW_STATUS = 'APPROVALS' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' ".format(QuoteRecordId = Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id")))
                        if get_status.upper() in ("OPD-PREPARING QUOTE DOCUMENTS","OPD-CUSTOMER ACCEPTED","OPD-CUSTOMER REJECTED"):
                            Sql.RunQuery("UPDATE SAQTRV SET WORKFLOW_STATUS = 'QUOTE DOCUMENTS' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' ".format(QuoteRecordId = Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id")))
                        if get_status.upper() in ("LGL-PREPARING LEGAL SOW","LGL-LEGAL SOW ACCEPTED","LGL-LEGAL SOW REJECTED"):
                            Sql.RunQuery("UPDATE SAQTRV SET WORKFLOW_STATUS = 'LEGAL SOW' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' ".format(QuoteRecordId = Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id")))
                        if get_status.upper() in ("PRI-PRICING"):
                            Sql.RunQuery("UPDATE SAQTRV SET WORKFLOW_STATUS = 'PRICING' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' ".format(QuoteRecordId = Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id")))
                        if get_status.upper() in ("PRR-ON HOLD PRICING"):
                            Sql.RunQuery("UPDATE SAQTRV SET WORKFLOW_STATUS = 'PRICING REVIEW' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' ".format(QuoteRecordId = Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id")))
                        if get_status.upper() in ("CFG-CONFIGURING","CFG-ACQUIRING","CFG-ON HOLD -COSTING"):
                            Sql.RunQuery("UPDATE SAQTRV SET WORKFLOW_STATUS = 'CONFIGURE' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' ".format(QuoteRecordId = Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id")))
                        #A055S000P01-17165 Rejected
                        if get_status.upper() == "APR-APPROVED":
                            Sql.RunQuery("UPDATE SAQTRV SET WORKFLOW_STATUS = 'APPROVALS' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' ".format(QuoteRecordId = Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id")))
                            ##Updating the Revision Approved Date while changing the status to Approved...
                            if get_approved_date == "":
                                RevisionApprovedDate = datetime.now().date()
                                Sql.RunQuery("UPDATE SAQTRV SET REV_APPROVE_DATE = '{RevisionApprovedDate}' WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' ".format(RevisionApprovedDate = RevisionApprovedDate,QuoteRecordId = Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id")))
                            ##Updating the Revision Approved Date while changing the status to Approved...
                            #crm_result = ScriptExecutor.ExecuteGlobal('QTPOSTACRM',{'QUOTE_ID':str(newdict.get("QUOTE_ID")),'REVISION_ID':str(get_rev_val),'Fun_type':'cpq_to_crm'})
                        ##Calling the iflow script to update the details in c4c..(cpq to c4c write back...)
                        CQCPQC4CWB.writeback_to_c4c("quote_header",contract_quote_record_id,quote_revision_record_id)
                        #time.sleep(5)
                        CQCPQC4CWB.writeback_to_c4c("opportunity_header",contract_quote_record_id,quote_revision_record_id)
                        CQREVSTSCH.Revisionstatusdatecapture(Quote.GetGlobal("contract_quote_record_id"),Quote.GetGlobal("quote_revision_record_id"),)
                    #A055S000P01-4288 end

                    if TreeParam == "Quote Information":

                        contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
                        quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")

                        product_offering_contract_validity = Sql.GetFirst("SELECT CONTRACT_VALID_FROM, CONTRACT_VALID_TO FROM SAQTRV (NOLOCK) WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}'".format(Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id)))
                        
                        #update dirty flag start
                        #HP QC -326 start
                        get_saqico_data = Sql.GetFirst("SELECT * from SAQRIT  WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(contract_quote_record_id,quote_revision_record_id))
                        if get_saqico_data:
                            if get_saqico_data.CONTRACT_VALID_FROM != product_offering_contract_validity.CONTRACT_VALID_FROM or get_saqico_data.CONTRACT_VALID_TO != product_offering_contract_validity.CONTRACT_VALID_TO:
                                Sql.RunQuery("UPDATE SAQTRV SET DIRTY_FLAG='{}',REVISION_STATUS='CFG-CONFIGURING',WORKFLOW_STATUS='CONFIGURE' WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(True,contract_quote_record_id,quote_revision_record_id))
                        #update dirty flag end-#HP QC -326 end
                    else:
                        notification = 'Billing Start Date should be less than Billing End Date'
                        dictc = {"CpqTableEntryId": str(sql_cpq.CpqTableEntryId)}
                        newdict.update(dictc)
                        tableInfo = Sql.GetTable(str(TableName))
                        tablerow = newdict
                        if ObjectName == 'SAQFBL':
                            tablerow.pop("CITY")#added to convert ascii in SAQFBL
                        tableInfo.AddRow(tablerow)
                        Trace.Write("TEZTZ--475---"+str(tablerow))
                        # sectional edit error message - starts
                        req_obj = Sql.GetList(
                            "select API_NAME from  SYOBJD(NOLOCK) where OBJECT_NAME = '" + str(TableName) + "' and REQUIRED = 1 "
                        )
                        Trace.Write("select API_NAME from  SYOBJD(NOLOCK) where OBJECT_NAME = '" + str(TableName) + "' and REQUIRED = 1 ")
                        #INC08839716
                        Req_Flag = 0
                        if req_obj is not None and len(req_obj) > 0: 
                            required_val = [str(i.API_NAME) for i in req_obj]
                            for data, datas in tablerow.items():
                                #INC09026420
                                #Trace.Write("data_chk_j---"+str(data)+" datas_chk_j---"+str(datas))
                                #INC09026420
                                if data in required_val:
                                    for req in required_val:
                                        Trace.Write("req_chk_j---"+str(req)+" tablerow_chk_j---"+str(tablerow))
                                        if (tablerow[req] == "" or tablerow[req] == "Select"):
                                            #INC09026420
                                            #Trace.Write("955---------------------------"+str(datas)+"--required_val--"+ str(required_val)+ "--data--"+str(data))
                                            #INC09026420
                                            Req_Flag = 1
                                            field_label = Sql.GetFirst("select FIELD_LABEL from SYOBJD(NOLOCK) where OBJECT_NAME = '" + str(TableName) + "' AND API_NAME = '"+str(data)+"' ")
                                            dates = "Contract Dates"
                                            if 'CONTRACT' in data:
                                                warning_msg = ' ERROR : "{}" is a required field'.format(dates)
                                            else:
                                                warning_msg = ' ERROR : "{}" is a required field'.format(field_label.FIELD_LABEL)
                                            break
                                        else:
                                            warning_msg = ""
                            if Req_Flag == 0:            
                                Sql.Upsert(tableInfo)
                        #INC08839716
                        else:
                            Trace.Write('533-----------'+str(TableName))
                            Sql.Upsert(tableInfo)
                            if str(TableName) == "SAQRIB":
                                Trace.Write('533-----------'+str(newdict))
                                get_service = newdict.get("SERVICE_ID")
                                get_bill_day = newdict.get("BILLING_DAY")
                                Trace.Write('533-----get_service------'+str(get_service))
                                Sql.RunQuery("UPDATE SAQRIB SET BILLING_DAY= '{get_bill_day}' where SERVICE_ID='{get_service}' AND QUOTE_RECORD_ID='{contract_quote_record_id}' and QTEREV_RECORD_ID='{quote_revision_record_id}'".format(get_service=get_service,contract_quote_record_id=contract_quote_record_id,quote_revision_record_id=quote_revision_record_id,get_bill_day=get_bill_day))
                                Trace.Write('533----contract_quote_record_id-------'+str(contract_quote_record_id))
                                LOGIN_CREDENTIALS = Sql.GetFirst("SELECT USER_NAME as Username,Password,Domain FROM SYCONF where Domain='AMAT_TST'")
                                if LOGIN_CREDENTIALS is not None:
                                    Login_Username = str(LOGIN_CREDENTIALS.Username)
                                    Login_Password = str(LOGIN_CREDENTIALS.Password)
                                    authorization = Login_Username+":"+Login_Password
                                    binaryAuthorization = UTF8.GetBytes(authorization)
                                    authorization = Convert.ToBase64String(binaryAuthorization)
                                    authorization = "Basic " + authorization
                                    webclient = System.Net.WebClient()
                                    webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/json"
                                    webclient.Headers[System.Net.HttpRequestHeader.Authorization] = authorization;		
                                    result = '''<?xml version="1.0" encoding="UTF-8"?><soapenv:Envelope	xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">	<soapenv:Body><CPQ_Columns>	<QUOTE_ID>{Qt_Id}</QUOTE_ID><REVISION_ID>{Rev_Id}</REVISION_ID></CPQ_Columns></soapenv:Body></soapenv:Envelope>'''.format( Qt_Id= contract_quote_record_id,Rev_Id = quote_revision_record_id)		
                                    LOGIN_CRE = Sql.GetFirst("SELECT URL FROM SYCONF where EXTERNAL_TABLE_NAME ='BILLING_MATRIX_ASYNC'")
                                    Async = webclient.UploadString(str(LOGIN_CRE.URL), str(result))
                        # sectional edit error message - ends
                        if TableName == "SAQFBL":
                            fab_id = TreeParam.split("-")[0]
                            get_driver = Sql.GetFirst("SELECT QUALITY_REQUIRED FROM WHERE SAQFBL QUOTE_RECORD_ID='{}' AND QTEREV_RECORD_ID='{}' AND FABLOCATION_ID ='{}'".format(contract_quote_record_id, quote_revision_record_id,fab_id))
                            if get_driver:
                                update_query = "UPDATE SAQSCE SET QRQVDV = '{}' WHERE SAQFBL QUOTE_RECORD_ID='{}' AND QTEREV_RECORD_ID='{}' AND FABLOCATION_ID ='{}'".format(get_driver.QUALITY_REQUIRED,contract_quote_record_id, quote_revision_record_id,fab_id)
                                Sql.RunQuery(update_query)
    
                        if Product.GetGlobal("TreeParentLevel1") == "Product Offerings":
                            contract_quote_record_id = Product.GetGlobal("contract_quote_record_id")
                            quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
                            #INC08656612 A
                            product_offering_contract_validity = Sql.GetFirst("SELECT CONTRACT_VALID_FROM, CONTRACT_VALID_TO,SERVICE_ID FROM SAQTSV (NOLOCK) WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND SERVICE_ID = '{service_id}'".format(Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(TreeParam)))
                            addon_offering_update ="UPDATE SAQTSV SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND PAR_SERVICE_ID = '{service_id}'".format(valid_from= product_offering_contract_validity.CONTRACT_VALID_FROM, valid_to =   product_offering_contract_validity.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID))
                            validity_from_date = Sql.GetFirst("SELECT MIN(CONTRACT_VALID_FROM) AS CONTRACT_VALID_FROM FROM SAQTSV (NOLOCK) WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}'".format(Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id)))

                            validity_to_date = Sql.GetFirst("SELECT MAX(CONTRACT_VALID_TO) AS CONTRACT_VALID_TO FROM SAQTSV (NOLOCK) WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}'".format(Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id)))

                            greenbook_contract_update = "UPDATE SAQSGB SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND SERVICE_ID = '{service_id}'".format(valid_from= product_offering_contract_validity.CONTRACT_VALID_FROM, valid_to = product_offering_contract_validity.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID))
                            greenbook_contract_adddon_update = "UPDATE SAQSGB SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND PAR_SERVICE_ID = '{service_id}'".format(valid_from= product_offering_contract_validity.CONTRACT_VALID_FROM, valid_to =   product_offering_contract_validity.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID))
                            
                            equipment_contract_update = "UPDATE SAQSCO SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND SERVICE_ID = '{service_id}' ".format(valid_from= product_offering_contract_validity.CONTRACT_VALID_FROM, valid_to =   product_offering_contract_validity.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID))

                            equipment_contract_addon_update = "UPDATE SAQSCO SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND PAR_SERVICE_ID = '{service_id}' ".format(valid_from= product_offering_contract_validity.CONTRACT_VALID_FROM, valid_to =   product_offering_contract_validity.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID))

                            assembly_contract_update = "UPDATE A SET A.CONTRACT_VALID_FROM = '{valid_from}' , A.CONTRACT_VALID_TO = '{valid_to}' from SAQSCA A JOIN SAQSCO B ON A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.QTEREV_RECORD_ID = B.QTEREV_RECORD_ID AND A.SERVICE_ID = B.SERVICE_ID WHERE B.QUOTE_RECORD_ID = '{Quote_rec_id}' AND B.QTEREV_RECORD_ID = '{Quote_revision_id}' AND B.SERVICE_ID = '{service_id}' ".format(valid_from= product_offering_contract_validity.CONTRACT_VALID_FROM, valid_to =   product_offering_contract_validity.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID))

                            assembly_contract_addon_update = "UPDATE A SET A.CONTRACT_VALID_FROM = '{valid_from}' , A.CONTRACT_VALID_TO = '{valid_to}' from SAQSCA A JOIN SAQSCO B ON A.EQUIPMENT_ID = B.EQUIPMENT_ID AND A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.QTEREV_RECORD_ID = B.QTEREV_RECORD_ID AND A.PAR_SERVICE_ID = B.PAR_SERVICE_ID WHERE B.QUOTE_RECORD_ID = '{Quote_rec_id}' AND B.QTEREV_RECORD_ID = '{Quote_revision_id}' AND B.PAR_SERVICE_ID = '{service_id}' ".format(valid_from= product_offering_contract_validity.CONTRACT_VALID_FROM, valid_to =   product_offering_contract_validity.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID))

                            item_contract_update = "UPDATE SAQRIT SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND SERVICE_ID = '{service_id}'".format(valid_from= product_offering_contract_validity.CONTRACT_VALID_FROM, valid_to =   product_offering_contract_validity.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID))
                            
                            saqico_contract_update = "UPDATE SAQICO SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND SERVICE_ID = '{service_id}'".format(valid_from= product_offering_contract_validity.CONTRACT_VALID_FROM, valid_to =   product_offering_contract_validity.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID))
                            
                            saqtrv_contract_update = "UPDATE SAQTRV SET CONTRACT_VALID_FROM = '{validity_from_date}' , CONTRACT_VALID_TO = '{validity_to_date}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}'".format(validity_from_date= validity_from_date.CONTRACT_VALID_FROM, validity_to_date =   validity_to_date.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id))

                            Sql.RunQuery(addon_offering_update)
                            Sql.RunQuery(greenbook_contract_update)
                            Sql.RunQuery(greenbook_contract_adddon_update)
                            Sql.RunQuery(equipment_contract_update)
                            Sql.RunQuery(equipment_contract_addon_update)
                            Sql.RunQuery(assembly_contract_update)
                            Sql.RunQuery(assembly_contract_addon_update)
                            Sql.RunQuery(saqico_contract_update)
                            Sql.RunQuery(saqtrv_contract_update)
                            Sql.RunQuery(item_contract_update)
                            #INC08656612 A

                        elif Product.GetGlobal("TreeParentLevel2") == "Product Offerings" and subtab_name != "Equipment Details":
                            contract_quote_record_id = Product.GetGlobal("contract_quote_record_id")
                            quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
                            
                            # to update equipment and assemblies's contract dates when adjusted in greenbook level -- start A055S000p01-19493
                            product_offering_contract_validity = Sql.GetFirst("SELECT CONTRACT_VALID_FROM, CONTRACT_VALID_TO,SERVICE_ID FROM SAQSGB (NOLOCK) WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND SERVICE_ID = '{service_id}' AND GREENBOOK = '{greenbook}' ".format(Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= Product.GetGlobal("TreeParentLevel0"),greenbook = Product.GetGlobal("Treeparam")))

                            #INC08656612 A
                            greenbook_contract_adddon_update = "UPDATE SAQSGB SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND PAR_SERVICE_ID = '{service_id}' AND GREENBOOK = '{greenbook}'".format(valid_from= product_offering_contract_validity.CONTRACT_VALID_FROM, valid_to =   product_offering_contract_validity.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID),greenbook = Quote.GetGlobal("Treeparam"))

                            equipment_contract_update = "UPDATE SAQSCO SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND SERVICE_ID = '{service_id}' AND GREENBOOK = '{greenbook}' ".format(valid_from= product_offering_contract_validity.CONTRACT_VALID_FROM, valid_to =   product_offering_contract_validity.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID),greenbook = Product.GetGlobal("Treeparam"))

                            equipment_contract_addon_update = "UPDATE SAQSCO SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND PAR_SERVICE_ID = '{service_id}' AND GREENBOOK = '{greenbook}' ".format(valid_from= product_offering_contract_validity.CONTRACT_VALID_FROM, valid_to =   product_offering_contract_validity.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID),greenbook = Quote.GetGlobal("Treeparam"))

                            assembly_contract_update = "UPDATE SAQSCA SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND SERVICE_ID = '{service_id}'  AND GREENBOOK = '{greenbook}' ".format(valid_from= product_offering_contract_validity.CONTRACT_VALID_FROM, valid_to =   product_offering_contract_validity.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID),greenbook = Product.GetGlobal("Treeparam"))

                            assembly_contract_addon_update = "UPDATE SAQSCA SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND PAR_SERVICE_ID = '{service_id}'  AND GREENBOOK = '{greenbook}' ".format(valid_from= product_offering_contract_validity.CONTRACT_VALID_FROM, valid_to =   product_offering_contract_validity.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID),greenbook = Quote.GetGlobal("Treeparam"))

                            validity_from_date = Sql.GetFirst("SELECT MIN(CONTRACT_VALID_FROM) AS CONTRACT_VALID_FROM FROM SAQSGB (NOLOCK) WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND SERVICE_ID = '{service_id}' ".format(Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID)))

                            validity_to_date = Sql.GetFirst("SELECT MAX(CONTRACT_VALID_TO) AS CONTRACT_VALID_TO FROM SAQSGB (NOLOCK) WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND SERVICE_ID = '{service_id}' ".format(Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID)))

                            service_contract_update = "UPDATE SAQTSV SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND SERVICE_ID = '{service_id}'".format(valid_from= validity_from_date.CONTRACT_VALID_FROM, valid_to =  validity_to_date.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID))

                            service_contract_addon_update = "UPDATE SAQTSV SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND PAR_SERVICE_ID = '{service_id}'".format(valid_from= validity_from_date.CONTRACT_VALID_FROM, valid_to =  validity_to_date.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID))

                            item_contract_update = "UPDATE SAQRIT SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND SERVICE_ID = '{service_id}' AND GREENBOOK = '{greenbook}' ".format(valid_from= validity_from_date.CONTRACT_VALID_FROM, valid_to =  validity_to_date.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID),greenbook = Product.GetGlobal("Treeparam"))

                            saqico_contract_update = "UPDATE SAQICO SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND SERVICE_ID = '{service_id}' AND GREENBOOK = '{greenbook}' ".format(valid_from= validity_from_date.CONTRACT_VALID_FROM, valid_to =   validity_to_date.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID),greenbook = str(Product.GetGlobal("Treeparam")))

                            Sql.RunQuery(greenbook_contract_adddon_update)
                            Sql.RunQuery(equipment_contract_update)
                            Sql.RunQuery(equipment_contract_addon_update)
                            Sql.RunQuery(assembly_contract_update)
                            Sql.RunQuery(assembly_contract_addon_update)
                            Sql.RunQuery(service_contract_update)
                            Sql.RunQuery(service_contract_addon_update)
                            Sql.RunQuery(saqico_contract_update)
                            Sql.RunQuery(item_contract_update)
                            #INC08656612 A

                        elif Product.GetGlobal("TreeParentLevel3") == "Product Offerings" and subtab_name == "Details":
                            contract_quote_record_id = Product.GetGlobal("contract_quote_record_id")
                            quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")

                            product_offering_contract_validity = Sql.GetFirst("SELECT CONTRACT_VALID_FROM, CONTRACT_VALID_TO,SERVICE_ID FROM SAQSGB (NOLOCK) WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND SERVICE_ID = '{service_id}' AND GREENBOOK = '{Treeparam}'".format(Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= Product.GetGlobal("TreeParentLevel1"),Treeparam= Product.GetGlobal("Treeparam")))

                            validity_from_date = Sql.GetFirst("SELECT MIN(CONTRACT_VALID_FROM) AS CONTRACT_VALID_FROM FROM SAQSGB (NOLOCK) WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}'".format(Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id)))

                            validity_to_date = Sql.GetFirst("SELECT MAX(CONTRACT_VALID_TO) AS CONTRACT_VALID_TO FROM SAQSGB (NOLOCK) WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}'".format(Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id)))

                            #INC08656612 A
                            greenbook_contract_adddon_update = "UPDATE SAQSGB SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND PAR_SERVICE_ID = '{service_id}'".format(valid_from= product_offering_contract_validity.CONTRACT_VALID_FROM, valid_to =   product_offering_contract_validity.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID))

                            service_contract_update = "UPDATE SAQTSV SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND SERVICE_ID = '{service_id}'".format(valid_from= product_offering_contract_validity.CONTRACT_VALID_FROM, valid_to =   product_offering_contract_validity.CONTRACT_VALID_TO, Quote_rec_id= contract_quote_record_id,Quote_revision_id= quote_revision_record_id,service_id= product_offering_contract_validity.SERVICE_ID)

                            service_contract_addon_update = "UPDATE SAQTSV SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND PAR_SERVICE_ID = '{service_id}'".format(valid_from= product_offering_contract_validity.CONTRACT_VALID_FROM, valid_to =   product_offering_contract_validity.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID))

                            equipment_contract_update = "UPDATE SAQSCO SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND SERVICE_ID = '{service_id}'".format(valid_from= product_offering_contract_validity.CONTRACT_VALID_FROM, valid_to =   product_offering_contract_validity.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID))

                            equipment_contract_addon_update = "UPDATE SAQSCO SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND PAR_SERVICE_ID = '{service_id}'".format(valid_from= product_offering_contract_validity.CONTRACT_VALID_FROM, valid_to =   product_offering_contract_validity.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID))

                            assembly_contract_update = "UPDATE SAQSCA SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND SERVICE_ID = '{service_id}'".format(valid_from= product_offering_contract_validity.CONTRACT_VALID_FROM, valid_to =   product_offering_contract_validity.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID))

                            assembly_contract_addon_update = "UPDATE SAQSCA SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND PAR_SERVICE_ID = '{service_id}'".format(valid_from= product_offering_contract_validity.CONTRACT_VALID_FROM, valid_to =   product_offering_contract_validity.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID))

                            saqico_contract_update = "UPDATE SAQICO SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND SERVICE_ID = '{service_id}'".format(valid_from= product_offering_contract_validity.CONTRACT_VALID_FROM, valid_to =   product_offering_contract_validity.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID))

                            saqtrv_contract_update = "UPDATE SAQTRV SET CONTRACT_VALID_FROM = '{validity_from_date}' , CONTRACT_VALID_TO = '{validity_to_date}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}'".format(validity_from_date= validity_from_date.CONTRACT_VALID_FROM, validity_to_date =   validity_to_date.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id))

                            item_contract_update = "UPDATE SAQRIT SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND SERVICE_ID = '{service_id}'".format(valid_from= product_offering_contract_validity.CONTRACT_VALID_FROM, valid_to =   product_offering_contract_validity.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID))

                            Sql.RunQuery(greenbook_contract_adddon_update)
                            Sql.RunQuery(service_contract_update)
                            Sql.RunQuery(service_contract_addon_update)
                            Sql.RunQuery(equipment_contract_update)
                            Sql.RunQuery(equipment_contract_addon_update)
                            Sql.RunQuery(assembly_contract_update)
                            Sql.RunQuery(assembly_contract_addon_update)
                            Sql.RunQuery(saqico_contract_update)
                            Sql.RunQuery(saqtrv_contract_update)
                            Sql.RunQuery(item_contract_update)
                            #INC08656612 A


                        if (Product.GetGlobal("TreeParentLevel3") == "Product Offerings" or Product.GetGlobal("TreeParentLevel2") == "Product Offerings") and subtab_name == "Equipment Details":
                            contract_quote_record_id = Product.GetGlobal("contract_quote_record_id")
                            quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")

                            product_offering_contract_validity = Sql.GetFirst("SELECT CONTRACT_VALID_FROM, CONTRACT_VALID_TO,SERVICE_ID,GREENBOOK, EQUIPMENT_ID FROM SAQSCO (NOLOCK) WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND CpqTableEntryId = '{Equipment}'".format(Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),Equipment=tablerow['CpqTableEntryId']))
                            #INC08656612 A
                            equipment_contract_addon_update = "UPDATE SAQSCO SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND PAR_SERVICE_ID = '{service_id}' AND GREENBOOK = '{greenbook}' AND EQUIPMENT_ID = '{equipment_id}' ".format(valid_from= product_offering_contract_validity.CONTRACT_VALID_FROM, valid_to =   product_offering_contract_validity.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID),greenbook = str(product_offering_contract_validity.GREENBOOK),equipment_id = str(product_offering_contract_validity.EQUIPMENT_ID))
                            Sql.RunQuery(equipment_contract_addon_update)

                            assembly_contract_update = "UPDATE SAQSCA SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND SERVICE_ID = '{service_id}' AND GREENBOOK = '{greenbook}' ".format(valid_from= product_offering_contract_validity.CONTRACT_VALID_FROM, valid_to =   product_offering_contract_validity.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID),greenbook = str(product_offering_contract_validity.GREENBOOK))                         
                            Sql.RunQuery(assembly_contract_update)

                            assembly_contract_addon_update = "UPDATE SAQSCA SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND PAR_SERVICE_ID = '{service_id}' AND GREENBOOK = '{greenbook}' AND EQUIPMENT_ID = '{equipment_id}' ".format(valid_from= product_offering_contract_validity.CONTRACT_VALID_FROM, valid_to =   product_offering_contract_validity.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID),greenbook = str(product_offering_contract_validity.GREENBOOK),equipment_id = str(product_offering_contract_validity.EQUIPMENT_ID))
                            Sql.RunQuery(assembly_contract_addon_update)

                            validity_from_date = Sql.GetFirst("SELECT MIN(CONTRACT_VALID_FROM) AS CONTRACT_VALID_FROM FROM SAQSCO (NOLOCK) WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND SERVICE_ID = '{service_id}' AND GREENBOOK = '{greenbook}' ".format(Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID),greenbook = str(product_offering_contract_validity.GREENBOOK)))

                            validity_to_date = Sql.GetFirst("SELECT MAX(CONTRACT_VALID_TO) AS CONTRACT_VALID_TO FROM SAQSCO (NOLOCK) WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND SERVICE_ID = '{service_id}' AND GREENBOOK = '{greenbook}' ".format(Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID),greenbook = str(product_offering_contract_validity.GREENBOOK)))

                            greenbook_contract_update = "UPDATE SAQSGB SET CONTRACT_VALID_FROM = '{validity_from_date}' , CONTRACT_VALID_TO = '{validity_to_date}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND SERVICE_ID = '{service_id}' AND GREENBOOK = '{greenbook}' ".format(validity_from_date= validity_from_date.CONTRACT_VALID_FROM, validity_to_date =   validity_to_date.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID),greenbook = str(product_offering_contract_validity.GREENBOOK))
                            Sql.RunQuery(greenbook_contract_update)

                            greenbook_contract_adddon_update = "UPDATE SAQSGB SET CONTRACT_VALID_FROM = '{validity_from_date}' , CONTRACT_VALID_TO = '{validity_to_date}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND PAR_SERVICE_ID = '{service_id}' AND GREENBOOK = '{greenbook}' ".format(validity_from_date= validity_from_date.CONTRACT_VALID_FROM, validity_to_date =   validity_to_date.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID),greenbook = str(product_offering_contract_validity.GREENBOOK))
                            Sql.RunQuery(greenbook_contract_adddon_update)
                             # jira A055S000P01-20759 start
                            validity_from_date = Sql.GetFirst("SELECT MIN(CONTRACT_VALID_FROM) AS CONTRACT_VALID_FROM FROM SAQSGB (NOLOCK) WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND SERVICE_ID = '{service_id}'".format(Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID)))

                            validity_to_date = Sql.GetFirst("SELECT MAX(CONTRACT_VALID_TO) AS CONTRACT_VALID_TO FROM SAQSGB (NOLOCK) WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND SERVICE_ID = '{service_id}' ".format(Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID)))  
                             # jira A055S000P01-20759 end

                            service_contract_update = "UPDATE SAQTSV SET CONTRACT_VALID_FROM = '{validity_from_date}' , CONTRACT_VALID_TO = '{validity_to_date}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND SERVICE_ID = '{service_id}'".format(validity_from_date= validity_from_date.CONTRACT_VALID_FROM, validity_to_date =   validity_to_date.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(Product.GetGlobal("TreeParentLevel0")))

                            service_contract_addon_update = "UPDATE SAQTSV SET CONTRACT_VALID_FROM = '{validity_from_date}' , CONTRACT_VALID_TO = '{validity_to_date}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND PAR_SERVICE_ID = '{service_id}'".format(validity_from_date= validity_from_date.CONTRACT_VALID_FROM, validity_to_date =   validity_to_date.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(Quote.GetGlobal("TreeParentLevel0")))
                            #INC08656612 A
                            saqico_contract_update = "UPDATE SAQICO SET CONTRACT_VALID_FROM = '{validity_from_date}' , CONTRACT_VALID_TO = '{validity_to_date}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND SERVICE_ID = '{service_id}'".format(validity_from_date= validity_from_date.CONTRACT_VALID_FROM, validity_to_date =   validity_to_date.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(Product.GetGlobal("TreeParentLevel1")))

                            item_contract_update = "UPDATE SAQRIT SET CONTRACT_VALID_FROM = '{valid_from}' , CONTRACT_VALID_TO = '{valid_to}' WHERE QUOTE_RECORD_ID = '{Quote_rec_id}' AND QTEREV_RECORD_ID = '{Quote_revision_id}' AND SERVICE_ID = '{service_id}'".format(valid_from= product_offering_contract_validity.CONTRACT_VALID_FROM, valid_to =   product_offering_contract_validity.CONTRACT_VALID_TO, Quote_rec_id= str(contract_quote_record_id),Quote_revision_id= str(quote_revision_record_id),service_id= str(product_offering_contract_validity.SERVICE_ID))

                            
                            
                            Sql.RunQuery(service_contract_addon_update)
                            Sql.RunQuery(service_contract_update)
                            Sql.RunQuery(item_contract_update)
                            Sql.RunQuery(saqico_contract_update)
                            
                if TableName == 'SAQRIB' and old_billing_matrix_obj:                    
                    billing_matrix_obj = Sql.GetFirst("""SELECT BILLING_START_DATE, 
                                    BILLING_END_DATE, QUOTE_BILLING_PLAN_RECORD_ID, BILLING_DAY
                                    FROM SAQRIB (NOLOCK)
                                    WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' """.format(Product.GetGlobal("contract_quote_record_id"), quote_revision_record_id ))
                    if billing_matrix_obj:
                        if billing_matrix_obj.BILLING_START_DATE != old_billing_matrix_obj.BILLING_START_DATE or billing_matrix_obj.BILLING_END_DATE != old_billing_matrix_obj.BILLING_END_DATE or billing_matrix_obj.BILLING_DAY != old_billing_matrix_obj.BILLING_DAY:                        						
                            billing_query = "UPDATE SAQRIB SET IS_CHANGED = 1 WHERE QUOTE_BILLING_PLAN_RECORD_ID ='{}'".format(billing_matrix_obj.QUOTE_BILLING_PLAN_RECORD_ID)
                            Sql.RunQuery(billing_query)
                    #generate_year_based_billing_matrix(newdict)
                if TableName == 'SAQTIP':
                    Trace.Write('SAQTIP_CHK_J '+str(RECORD['CPQ_PARTNER_FUNCTION']))
                    Sql.RunQuery("UPDATE SAQTIP SET [PRIMARY] = 'false' WHERE CPQ_PARTNER_FUNCTION = 'SHIP TO' AND QUOTE_RECORD_ID = '{qte_rec_id}' AND QTEREV_RECORD_ID = '{qte_rev_id}'".format(qte_rec_id=Product.GetGlobal("contract_quote_record_id"),qte_rev_id=quote_revision_record_id))

                    saqtip_ship_to_update_query = "UPDATE SAQTIP SET PARTY_ID = {party_id}, [PRIMARY] = '{primary}' WHERE QUOTE_INVOLVED_PARTY_RECORD_ID = '{ship_to_id}'".format(party_id=RECORD['PARTY_ID'],primary=RECORD['PRIMARY'],ship_to_id=RECORD['QUOTE_INVOLVED_PARTY_RECORD_ID'])


                    Sql.RunQuery(saqtip_ship_to_update_query)

                    account_details = Sql.GetFirst("SELECT * FROM SAACNT (NOLOCK) WHERE ACCOUNT_ID = '"+str(RECORD['PARTY_ID'])+"'")
                    send_n_receive_acunt = "UPDATE SAQSRA SET ACCOUNT_ID = '{}', ACCOUNT_NAME = '{}', ACCOUNT_RECORD_ID = '{}', ADDRESS_1 = '{}', CITY = '{}', COUNTRY = '{}', COUNTRY_RECORD_ID = '{}', PHONE = '{}', STATE = '{}', STATE_RECORD_ID = '{}', POSTAL_CODE = '{}' WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND RELOCATION_TYPE = '{}'".format(str(account_details.ACCOUNT_ID), str(account_details.ACCOUNT_NAME), str(account_details.ACCOUNT_RECORD_ID), str(account_details.ADDRESS_1), str(account_details.CITY), str(account_details.COUNTRY), str(account_details.COUNTRY_RECORD_ID), str(account_details.PHONE), str(account_details.STATE), str(account_details.STATE_RECORD_ID), str(account_details.POSTAL_CODE), Product.GetGlobal("contract_quote_record_id"), quote_revision_record_id, str(RECORD['CPQ_PARTNER_FUNCTION']))
                    Sql.RunQuery(send_n_receive_acunt)
                # A055S000P01-3324 start 
                if TableName == 'SAQTMT':
                    #A055S000P01-4393 start 
                    WARRANTY_val =''
                    warrant_enddat_alert_update = SqlHelper.GetFirst("sp_executesql @T=N'update B SET B.WARRANTY_END_DATE_ALERT = (CASE WHEN B.WARRANTY_END_DATE >= A.CONTRACT_VALID_FROM AND B.WARRANTY_END_DATE <=A.CONTRACT_VALID_TO THEN 1 ELSE 0 END) FROM SAQTMT A JOIN SAQSCO B ON A.MASTER_TABLE_QUOTE_RECORD_ID=B.QUOTE_RECORD_ID AND A.QTEREV_RECORD_ID=B.QTEREV_RECORD_ID WHERE A.MASTER_TABLE_QUOTE_RECORD_ID = ''"+str(Quote.GetGlobal("contract_quote_record_id"))+"'' AND A.QTEREV_RECORD_ID = ''"+str(quote_revision_record_id)+"'' AND B.WARRANTY_END_DATE >= A.CONTRACT_VALID_FROM and B.WARRANTY_END_DATE <=A.CONTRACT_VALID_TO '")
            else:
                Trace.Write("1237------5444------------" + str(newdict))
                newdict.update(RECORD)
                Trace.Write("1237------5444------------" + str(newdict))
                activeval = newdict.get("Active")
                idval = newdict.get("ID")
                UPDATE_USERS = "UPDATE USERS SET Active = '{}' WHERE ID = '{}'".format(activeval,idval)
                Sql.RunQuery(UPDATE_USERS)
                #tableInfo = SqlHelper.GetTable("USERS")
                #tableInfo.AddRow(newdict)
                #SqlHelper.Upsert(tableInfo)
        else:            
            new_val = str(Guid.NewGuid()).upper()
            RECID = {str(AutoNumb): new_val}
            RECORD.update(RECID)
            sql_sgs = Sql.GetList("SELECT API_NAME FROM SYOBJD WHERE OBJECT_NAME='" + str(TableName) + "'")
            for attr in sql_sgs:
                for KEY in RECORD:

                    if str(attr.API_NAME) == KEY:
                        newdict[attr.API_NAME] = RECORD[KEY]
                    else:
                        if str(attr.API_NAME) == "PRICEMODEL_ID":
                            KEY = "PRICEMODEL_ID"
                            newdict[attr.API_NAME] = RECORD[KEY] if str(TableName) != "PRPBMA" else RECORD[KEY + "_VALUE"]
                    tableInfo = Sql.GetTable(str(TableName))
                    tablerow = newdict
                    tableInfo.AddRow(tablerow)
                    Trace.Write("else1469")
                    Sql.Upsert(tableInfo)
        ##calling QTPOSTACRM script for CRM Contract idoc
        try:
            if TableName == 'SAQTMT' and 'QUOTE_STATUS' in RECORD.keys() and section_text == " EDITBASIC INFORMATION":
                Trace.Write('QUOTE_STATUS -- inside')
                if RECORD.get("QUOTE_STATUS") ==  'APPROVED':
                    quote_id = Sql.GetFirst(
                        """SELECT QUOTE_ID,QTEREV_ID FROM SAQTMT (NOLOCK) WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID='{revision_rec_id}' """.format(
                        QuoteRecordId= Quote.GetGlobal("contract_quote_record_id"),
                        revision_rec_id = quote_revision_record_id
                        )
                    )
                    
                    Trace.Write('inside---'+str({'QUOTE_ID':str(quote_id.QUOTE_ID),'Fun_type':'cpq_to_crm'}))
                    crm_result = ScriptExecutor.ExecuteGlobal('QTPOSTACRM',{'QUOTE_ID':str(quote_id.QUOTE_ID),'REVISION_ID':str(quote_id.QTEREV_ID),'Fun_type':'cpq_to_crm'})
                    Trace.Write("ends--"+str(crm_result))
        except Exception:
            Trace.Write("except---")
        ##ends
        try: # To update the min and max contract start and end date to quote header and C4C while doing section edit in Equipment, Greenbook and service level
            if str(TableName) in ("SAQTSV","SAQSCO","SAQSGB"):
                get_min_max=Sql.GetFirst("SELECT MIN(CONTRACT_VALID_FROM) AS MIN,MAX(CONTRACT_VALID_TO) AS MAX FROM (SELECT CONTRACT_VALID_FROM,CONTRACT_VALID_TO FROM SAQTSV WHERE QUOTE_RECORD_ID = '{quote_rec}' AND QTEREV_RECORD_ID = '{quote_rev_rec_id}' UNION ALL SELECT CONTRACT_VALID_FROM,CONTRACT_VALID_TO FROM SAQSCO WHERE QUOTE_RECORD_ID = '{quote_rec}' AND QTEREV_RECORD_ID = '{quote_rev_rec_id}' ) as Q".format(quote_rec=Quote.GetGlobal("contract_quote_record_id"),quote_rev_rec_id=Quote.GetGlobal("quote_revision_record_id")))
                if get_min_max:
                    Sql.RunQuery("UPDATE SAQTRV SET CONTRACT_VALID_FROM = '{min}', CONTRACT_VALID_TO = '{max}' WHERE QUOTE_RECORD_ID = '{quote_rec}' AND QTEREV_RECORD_ID = '{quote_rev_rec_id}' ".format(min = get_min_max.MIN,max= get_min_max.MAX,quote_rec=Quote.GetGlobal("contract_quote_record_id"),quote_rev_rec_id=Quote.GetGlobal("quote_revision_record_id")))
                    Sql.RunQuery("UPDATE SAQTMT SET CONTRACT_VALID_FROM = '{min}', CONTRACT_VALID_TO = '{max}' WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{quote_rec}' ".format(min = get_min_max.MIN,max= get_min_max.MAX,quote_rec=Quote.GetGlobal("contract_quote_record_id")))
                    CQCPQC4CWB.writeback_to_c4c("quote_header",Quote.GetGlobal("contract_quote_record_id"),Quote.GetGlobal("quote_revision_record_id"))
        except:
            Trace.Write('Exception occured on Contract Start & End Date Updation')	
        ##entitlement contract date update for z0016
        try:
            if Quote is not None:
                quote_record_id = Quote.GetGlobal("contract_quote_record_id")
            else:
                quote_record_id = ''
        except:
            quote_record_id = ''
        

        try:
            get_service_id = Sql.GetList("Select * from SAQTSV (nolock) where QUOTE_RECORD_ID ='"+str(quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' AND SERVICE_ID LIKE '%Z0016%' ")
            if get_service_id:
                for service in get_service_id:
                    if TableName == 'SAQTMT' and 'CONTRACT_VALID_TO' in RECORD.keys() and 'CONTRACT_VALID_FROM' in RECORD.keys() and section_text == " EDITQUOTE TIMELINE INFORMATION" :
                        Trace.Write('CONTRACT_VALID_TO -- inside')
                        try:
                            
                            get_value = Sql.GetFirst("Select * from SAQTMT (nolock) where MASTER_TABLE_QUOTE_RECORD_ID ='"+str(quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' ")
                            Trace.Write('get_value.CONTRACT_VALID_TO--'+str(get_value.CONTRACT_VALID_TO))
                            QuoteEndDate = datetime.datetime(get_value.CONTRACT_VALID_TO)
                            QuoteStartDate = datetime.datetime(get_value.CONTRACT_VALID_FROM)
                            contract_days = (QuoteEndDate - QuoteStartDate).days
                            Trace.Write('contract_days-----'+str(contract_days))
                            ent_disp_val = 	str(contract_days)
                        except:
                            Trace.Write('except--1---')
                            ent_disp_val = ""
                        
                        if int(ent_disp_val) > 364:
                            try:
                                quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
                                AttributeID = 'AGS_CON_DAY'
                                add_where =''
                                ServiceId = service.SERVICE_ID
                                whereReq =  """QUOTE_RECORD_ID ='"+str(quote_record_id)+"'  AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' AND SERVICE_ID = '{}' """.format(service.SERVICE_ID)
                                ent_params_list = str(whereReq)+"||"+str(add_where)+"||"+str(AttributeID)+"||"+str(ent_disp_val)+"||"+str(ServiceId) + "||" + 'SAQTSE'
                                result = ScriptExecutor.ExecuteGlobal("CQASSMEDIT", {"ACTION": 'UPDATE_ENTITLEMENT', 'ent_params_list':ent_params_list})
                            except:
                                    pass
                
        except Exception:
            Trace.Write("except---")
            pass



    return "", warning_msg, str(ErrorequiredDict), ErrorequiredDictMSg, SecRecId, ErrorequiredtabDictMSg,notification,notificationinterval


def UpdateBurdenSettings(Column):

    UpdateBurdenSet = (
        "update PASACS set DEF_MERCH_BURDEN_FACTOR = '0.00' where PRICEAGREEMENT_RECORD_ID = '"
        + str(Product.GetGlobal("segment_rec_id"))
        + "' and AGMREV_ID = '"
        + str(Product.GetGlobal("segmentRevisionId"))
        + "'"
    )
    Trace.Write("UpdateBurdenSet---->" + str(UpdateBurdenSet))
    Sql.RunQuery(UpdateBurdenSet)


def getting_cps_tax(item_obj,quote_type):
    webclient = System.Net.WebClient()
    response=''
    webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/x-www-form-urlencoded"
    cps_credential_obj = SqlHelper.GetFirst("SELECT USER_NAME, PASSWORD, URL FROM SYCONF (NOLOCK) WHERE EXTERNAL_TABLE_NAME='CPS_VARIANT_PRICING'")
    if cps_credential_obj:
        response = webclient.DownloadString(cps_credential_obj.URL+'?grant_type=client_credentials&client_id='+cps_credential_obj.USER_NAME+'&client_secret='+cps_credential_obj.PASSWORD)
    response = eval(response)
    
    Request_URL="https://cpservices-pricing.cfapps.us10.hana.ondemand.com/api/v1/statelesspricing"
    webclient.Headers[System.Net.HttpRequestHeader.Authorization] ="Bearer "+str(response['access_token'])

    x = datetime.datetime.today()
    x= str(x)
    y = x.split(" ")
    
    GetPricingProcedure = Sql.GetFirst("SELECT ISNULL(DIVISION_ID, '') as DIVISION_ID,ISNULL(COUNTRY, '') as COUNTRY, ISNULL(DISTRIBUTIONCHANNEL_ID, '') as DISTRIBUTIONCHANNEL_ID, ISNULL(SALESORG_ID, '') as SALESORG_ID, ISNULL(DOC_CURRENCY,'') as DOC_CURRENCY, ISNULL(PRICINGPROCEDURE_ID,'') as PRICINGPROCEDURE_ID, QUOTE_RECORD_ID FROM SAQTRV (NOLOCK) WHERE QUOTE_ID = '{}'".format(contract_quote_obj.QUOTE_ID))
    if GetPricingProcedure is not None:			
        PricingProcedure = GetPricingProcedure.PRICINGPROCEDURE_ID
        curr = GetPricingProcedure.DOC_CURRENCY
        dis = GetPricingProcedure.DISTRIBUTIONCHANNEL_ID
        salesorg = GetPricingProcedure.SALESORG_ID
        div = GetPricingProcedure.DIVISION_ID
        #exch = GetPricingProcedure.EXCHANGE_RATE_TYPE
        #taxk1 = GetPricingProcedure.CUSTAXCLA_ID
        country = GetPricingProcedure.COUNTRY
    #update_SAQITM = "UPDATE SAQITM SET PRICINGPROCEDURE_ID = '{prc}' WHERE SAQITM.QUOTE_ID = '{quote}'".format(prc=str(PricingProcedure), quote=self.contract_quote_id)
    #Sql.RunQuery(update_SAQITM)
    STPObj=Sql.GetFirst("SELECT ACCOUNT_ID FROM SAOPQT (NOLOCK) WHERE QUOTE_ID ='{quote}'".format(quote=contract_quote_obj.QUOTE_ID))		
    stp_account_id = ""
    if STPObj:
        stp_account_id = str(STPObj.ACCOUNT_ID)		
        
    itemid = 1	
    TreeParam = Product.GetGlobal("TreeParam")	
    Service_id = TreeParam.split('-')[1].strip()
    if item_obj:			
        item_string = '{"itemId":"'+str(itemid)+'","externalId":null,"quantity":{"value":'+str(1)+',"unit":"EA"},"exchRateType":"'+str(exch)+'","exchRateDate":"'+str(y[0])+'","productDetails":{"productId":"'+str(Service_id)+'","baseUnit":"EA","alternateProductUnits":null},"attributes":[{"name":"KOMK-LAND1","values":["'+country+'"]},{"name":"KOMK-ALAND","values":["'+country+'"]},{"name":"KOMK-REGIO","values":["TX"]},{"name":"KOMK-KUNNR","values":["'+stp_account_id+'"]},{"name":"KOMK-KUNWE","values":["'+stp_account_id+'"]},{"name":"KOMP-TAXM1","values":["'+str(item_obj.SRVTAXCLA_ID)+'"]},{"name":"KOMK-TAXK1","values":["'+str(taxk1)+'"]},{"name":"KOMK-SPART","values":["'+str(div)+'"]},{"name":"KOMP-SPART","values":["'+str(div)+'"]},{"name":"KOMP-PMATN","values":["'+str(Service_id)+'"]},{"name":"KOMK-WAERK","values":["'+str(curr)+'"]},{"name":"KOMK-HWAER","values":["'+str(curr)+'"]},{"name":"KOMP-PRSFD","values":["X"]},{"name":"KOMK-VTWEG","values":["'+str(dis)+'"]},{"name":"KOMK-VKORG","values":["'+str(salesorg)+'"]},{"name":"KOMP-KPOSN","values":["0"]},{"name":"KOMP-KZNEP","values":[""]},{"name":"KOMP-ZZEXE","values":["true"]}],"accessDateList":[{"name":"KOMK-PRSDT","value":"'+str(y[0])+'"},{"name":"KOMK-FBUDA","value":"'+str(y[0])+'"}],"variantConditions":[],"statistical":true,"subItems":[]}'
        requestdata = '{"docCurrency":"'+curr+'","locCurrency":"'+curr+'","pricingProcedure":"'+PricingProcedure+'","groupCondition":false,"itemConditionsRequired":true,"items": ['+str(item_string)+']}'
        Trace.Write("requestdata======>>>> "+str(requestdata))
        response1 = webclient.UploadString(Request_URL,str(requestdata))			
        response1 = str(response1).replace(": true", ': "true"').replace(": false", ': "false"').replace(": null",': " None"')
        response1 = eval(response1)
        Trace.Write("response1 ===> "+str(response1))
        price = []
        for root, value in response1.items():
            if root == "items":
                price = value[:]
                break
        tax_percentage = 0
        for data in price[0]['conditions']:
            if data['conditionType'] == 'ZWSC' and data['conditionTypeDescription'] == 'VAT Asia':
                tax_percentage = data['conditionRate']
                break
        # update_tax = "UPDATE SAQITM SET TAX_PERCENTAGE = {TaxPercentage} WHERE SAQITM.QUOTE_ITEM_RECORD_ID = '{ItemRecordId}'".format(
        # TaxPercentage=tax_percentage,			
        # ItemRecordId=item_obj.QUOTE_ITEM_RECORD_ID
        # )
        # Sql.RunQuery(update_tax)
        if quote_type == 'tool':
            Trace.Write("update saqico---")
            #commented the query because of removing the api_name TAX_PERCENTAGE from SAQICO - start
            # update_tax_item_covered_obj = "UPDATE SAQICO SET TAX_PERCENTAGE = {TaxPercentage} WHERE SAQICO.SERVICE_ID = '{ServiceId}' and QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID='{revision_rec_id}' ".format(
            # TaxPercentage=tax_percentage,			
            # ServiceId=TreeParam.split('-')[1].strip(),
            # QuoteRecordId=Quote.GetGlobal("contract_quote_record_id"),
            # revision_rec_id = quote_revision_record_id
            # )
            # Sql.RunQuery(update_tax_item_covered_obj)
            #commented the query because of removing the api_name TAX_PERCENTAGE from SAQICO - end	
            #update TAX column  and Extended price for each SAQICO records
            '''QueryStatement ="""UPDATE a SET a.TAX = CASE WHEN a.TAX_PERCENTAGE > 0 THEN (ISNULL(a.YEAR_1, 0)+ISNULL(a.YEAR_2, 0)+ISNULL(a.YEAR_3, 0)+ISNULL(a.YEAR_4, 0)+ISNULL(a.YEAR_5, 0)) * (a.TAX_PERCENTAGE/100) ELSE a.TAX_PERCENTAGE END FROM SAQICO a INNER JOIN SAQICO b on a.EQUIPMENT_ID = b.EQUIPMENT_ID and a.QUOTE_RECORD_ID = b.QUOTE_RECORD_ID and  a.QTEREV_RECORD_ID = b.QTEREV_RECORD_ID where a.QUOTE_RECORD_ID = '{QuoteRecordId}' and a.SERVICE_ID = '{ServiceId}' AND a.QTEREV_RECORD_ID='{revision_rec_id}'""".format(			
            ServiceId=TreeParam.split('-')[1].strip(),
            QuoteRecordId=Quote.GetGlobal("contract_quote_record_id"),
            revision_rec_id = quote_revision_record_id
            )
            Sql.RunQuery(QueryStatement)'''
            '''QueryStatement ="""UPDATE a SET a.EXTENDED_PRICE = CASE WHEN a.TAX > 0 THEN (ISNULL(a.YEAR_1, 0)+ISNULL(a.YEAR_2, 0)+ISNULL(a.YEAR_3, 0)+ISNULL(a.YEAR_4, 0)+ISNULL(a.YEAR_5, 0)) + (a.TAX) ELSE a.TAX END FROM SAQICO a INNER JOIN SAQICO b on a.EQUIPMENT_ID = b.EQUIPMENT_ID and a.QUOTE_RECORD_ID = b.QUOTE_RECORD_ID and  a.QTEREV_RECORD_ID = b.QTEREV_RECORD_ID where a.QUOTE_RECORD_ID = '{QuoteRecordId}' and a.SERVICE_ID = '{ServiceId}' AND a.QTEREV_RECORD_ID='{revision_rec_id}' """.format(			
            ServiceId=TreeParam.split('-')[1].strip(),
            QuoteRecordId=Quote.GetGlobal("contract_quote_record_id"),
            revision_rec_id = quote_revision_record_id
            )
            Sql.RunQuery(QueryStatement)'''
            #update SAQITM role up 
            # QueryStatement = """UPDATE A  SET A.EXTENDED_PRICE = B.EXTENDED_PRICE FROM SAQITM A(NOLOCK) JOIN (SELECT SUM(EXTENDED_PRICE) AS EXTENDED_PRICE,QUOTE_RECORD_ID,QTEREV_RECORD_ID,SERVICE_RECORD_ID from SAQICO(NOLOCK) WHERE QUOTE_RECORD_ID ='{QuoteRecordId}' and SERVICE_ID = '{ServiceId}' AND QTEREV_RECORD_ID='{revision_rec_id}' GROUP BY QUOTE_RECORD_ID,SERVICE_RECORD_ID,QTEREV_RECORD_ID) B ON A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.SERVICE_RECORD_ID=B.SERVICE_RECORD_ID AND A.QTEREV_RECORD_ID = B.QTEREV_RECORD_ID """.format(			
            # ServiceId=TreeParam.split('-')[1].strip(),
            # QuoteRecordId=Quote.GetGlobal("contract_quote_record_id"),
            # revision_rec_id = quote_revision_record_id
            # )
            # Sql.RunQuery(QueryStatement)
            '''QueryStatement = """UPDATE A  SET A.TAX = B.TAX FROM SAQITM A(NOLOCK) JOIN (SELECT SUM(TAX) AS TAX,QUOTE_RECORD_ID,QTEREV_RECORD_ID, SERVICE_RECORD_ID from SAQICO(NOLOCK) WHERE QUOTE_RECORD_ID ='{QuoteRecordId}' and SERVICE_ID = '{ServiceId}' AND QTEREV_RECORD_ID='{revision_rec_id}' GROUP BY QUOTE_RECORD_ID,SERVICE_RECORD_ID,QTEREV_RECORD_ID) B ON A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.SERVICE_RECORD_ID=B.SERVICE_RECORD_ID  AND A.QTEREV_RECORD_ID = B.QTEREV_RECORD_ID""".format(			
            ServiceId=TreeParam.split('-')[1].strip(),
            QuoteRecordId=Quote.GetGlobal("contract_quote_record_id"),
            revision_rec_id = quote_revision_record_id
            )
            Sql.RunQuery(QueryStatement)'''


RECORD = Param.RECORD
try:
    SecRecId = Param.SecRecId
except:
    SecRecId = ""
try:
    section_text = Param.SECTION_TEXT
except:
    section_text = ""
TreeParam = Param.TreeParam
TreeParentParam = Param.TreeParentParam
TreeSuperParentParam = Param.TreeSuperParentParam

TopSuperParentParam = Param.TopSuperParentParam
try:
    quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
except:
    quote_revision_record_id = ""

try:
    subtab_name = Param.subtab_name
except:
    subtab_name = ""

TableId = Param.TableId
Trace.Write(RECORD)
ObjectName = ""
warning_msg = ""
Trace.Write("TableId-" + str(TableId))
#Trace.Write("RECORD" + str(RECORD))
Trace.Write("TreeParam" + str(TreeParam))
Trace.Write("TreeParentParam" + str(TreeParentParam))
Trace.Write("TreeSuperParentParam" + str(TreeSuperParentParam))
Trace.Write("TopSuperParentParam" + str(TopSuperParentParam))

if (
    str(TreeParentParam) == "Tabs"
    and str(TopSuperParentParam) == "App Level Permissions"
    and str(TreeParam) != ""
    and "SYPRTB" in RECORD
):
    ObjectName = "SYPRTB"
    TableId = "SYOBJR-93159"
if TreeParam == 'Billing Matrix':    
    ObjectName = "SAQRIB"
elif TreeParentParam == "Questions" and TopSuperParentParam == "Sections":
    ObjectName = "SYPRQN"
    TableId = "SYOBJR-93188"
elif TreeParentParam == "App Level Permissions":
    ObjectName = "SYPRAP"
    TableId = "SYOBJR-93121"
elif TreeParam == "Quote Documents":
    ObjectName = "SAQDOC"
    TableId = " "
elif TreeParentParam == "Actions" and TopSuperParentParam == "Sections":
    ObjectName = "SYPRSN"
    TableId = "SYOBJR-93160"
elif TopSuperParentParam == "Tabs" and TreeParentParam == "Actions":
    ObjectName = "SYPRSN"
    TableId = "SYOBJR-93160"
elif TreeParentParam == "Actions" and TopSuperParentParam == "Sections":
    ObjectName = "SYPRAC"
    TableId = "SYOBJR-93188"
elif TreeParentParam == "Questions" and TopSuperParentParam == "Sections" and TableId == "SYOBJR-93159":
    ObjectName = "SYPRTB"
# elif TreeParam == "Quote Information" and TableId == "SYOBJR-98798":
# 	ObjectName = "SAQTIP"    
elif TreeParam == "Quote Information":
    ObjectName = "SAQTRV"
    
elif TreeParam == "Approval Chain Information":
    ObjectName = "ACAPCH"
    
elif TreeSuperParentParam == "Constraints":
    ObjectName = "SYOBJC"
elif TreeParentParam == "Fab Locations":
    ObjectName = "SAQFBL"

    
elif TableId is not None:
    objr_obj = Sql.GetFirst("select * FROM SYOBJR where SAPCPQ_ATTRIBUTE_NAME = '" + str(TableId) + "' ")
    Trace.Write("select * FROM SYOBJR where SAPCPQ_ATTRIBUTE_NAME = '" + str(TableId) + "' ")
    if objr_obj is not None:
        objr_obj_id = str(objr_obj.OBJ_REC_ID)
        Trace.Write("objr_obj_id" + str(objr_obj_id))
        if objr_obj_id is not None:
            objh_obj = Sql.GetFirst("select * FROM SYOBJH where RECORD_ID = '" + str(objr_obj_id) + "' ")
            Trace.Write("select * FROM SYOBJH where RECORD_ID = '" + str(objr_obj_id) + "' ")
            if objh_obj is not None:
                ObjectName = str(objh_obj.OBJECT_NAME)



ApiResponse = ApiResponseFactory.JsonResponse(MaterialSave(ObjectName, RECORD, warning_msg, SecRecId,subtab_name))
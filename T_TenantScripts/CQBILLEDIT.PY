#   __script_name : CQBILLEDIT.PY
#   __script_description : THIS SCRIPT IS USED TO EDIT A RECORD WHEN THE USER CLICKS ON THE GRID.
#   __primary_author__ : DHURGA
#   __create_date : 17/11/2020
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================

import Webcom.Configurator.Scripting.Test.TestProduct
from SYDATABASE import SQL
import re

#gettotalannualamt = ""
SubTab = getdatestart = getmonthavle = getmonthavl = ""
Sql = SQL()
ContractRecordId = Quote.GetGlobal("contract_quote_record_id")
quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
get_total_qty =0
get_edited_bill_amt = 0


get_billig_date_list = []
def BILLEDIT_SAVE(GET_DICT,totalyear,getedited_amt,TreeParam,TreeParentParam):
    Trace.Write(str(TreeParam)+'--TreeParentParam---'+str(TreeParentParam)+'---BULK EDIT SAVE BILLING MATRIX--inside function---GET_DICT----'+str(GET_DICT))
    #@HPQC-1686 start
    count = get_edited_bill_amt = 0
    
    savebill_msg = savebill = ''
    for val in GET_DICT:
        count += 1
        value = val.split('*')
        getmonthavl = value[1].replace("/",'-').strip()		
        getamtval = re.findall(r"\d",str(totalyear))
        get_billig_date_list.append(value[1])
        get_edited_bill_amt += float(value[2].replace(',',''))
    for val in GET_DICT:
        count += 1
        value = val.split('*')
        getmonthavl = value[1].replace("/",'-').strip()		
        getamtval = re.findall(r"\d",str(totalyear))
        SubTab = getamtval[0]
        SubTab_Year = "Year "+SubTab
        getannual_amt = value[3]
        getline = value[4]
        get_edited_bill_amt = float(value[2].replace(',',''))
        bill_type = ''
        #if str(TreeParam) in ("Z0010","Z0016"):
            #getline = value[5]
    
        Trace.Write('getannual_amt--1111111----'+str(getannual_amt))
        getannual_amt = int(float(getannual_amt.replace(',','')))
    
        get_bill_type = Sql.GetFirst("SELECT BILLING_TYPE FROM SAQRIT WHERE  QUOTE_RECORD_ID ='{cq}' and SERVICE_ID = '{service_id_param}' AND QTEREV_RECORD_ID ='{revision_rec_id}' ".format(cq=str(ContractRecordId),service_id_param=TreeParam,revision_rec_id = quote_revision_record_id))
        Trace.Write('get_bill' +str(get_bill_type.BILLING_TYPE))
        if get_bill_type:
            bill_type = get_bill_type.BILLING_TYPE
        gettotalamt_beforeupdate = Sql.GetFirst("SELECT SUM(BILLING_VALUE_INGL_CURR) as ANNUAL_BILLING_AMOUNT,SUM(ESTVAL_INGL_CURR) as ESTVAL_INGL_CURR,SERVICE_ID,BILLING_TYPE FROM SAQIBP WHERE  QUOTE_RECORD_ID ='{cq}' and SERVICE_ID = '{service_id_param}' AND QTEREV_RECORD_ID ='{revision_rec_id}' and LINE='{getline}' and BILLING_YEAR = '{SubTab_Year}' and EQUIPMENT_ID = '{EID}' and BILLING_DATE NOT IN {BD} GROUP BY SERVICE_ID,BILLING_TYPE".format(cq=str(ContractRecordId),SubTab_Year=SubTab_Year,EID=value[0],service_id_param=TreeParam,getline=getline, revision_rec_id = quote_revision_record_id ,BD=str(tuple(get_billig_date_list)).replace(',)',')') ))
        gettotalamt =0
        gettotalamt_update =0
        get_edited_total_amt = 0
        Trace.Write('get_edited_bill_amt---.'+str(get_edited_bill_amt))
        try:
            get_edited_total_amt = int(float(getannual_amt.replace(',','')))+int(get_edited_bill_amt)
        except:
            get_edited_total_amt = int(float(getannual_amt))+int(get_edited_bill_amt)
        if gettotalamt_beforeupdate:
            if str(get_bill_type.BILLING_TYPE).upper() in  ("FIXED","MILESTONE"):
                Trace.Write('gettotalamt_beforeupdate-->'+str(float(gettotalamt_beforeupdate.ANNUAL_BILLING_AMOUNT)))
                gettotalamt = float(gettotalamt_beforeupdate.ANNUAL_BILLING_AMOUNT)+float(get_edited_bill_amt)
                if gettotalamt_beforeupdate:
                    gettotalamt_update = float(gettotalamt_beforeupdate.ANNUAL_BILLING_AMOUNT)+float(value[2].replace(",",""))
            else:
                gettotalamt = float(gettotalamt_beforeupdate.ESTVAL_INGL_CURR)+float(get_edited_bill_amt)
                if gettotalamt_beforeupdate:
                    gettotalamt_update = float(gettotalamt_beforeupdate.ESTVAL_INGL_CURR)+float(value[2].replace(",",""))
        
        get_edited_total_amt = 0
        get_edited_total_amt = int(getannual_amt)+int(get_edited_bill_amt)
        #if int(get_edited_total_amt) < int(getannual_amt):
        #Trace.Write('get_edited_bill_amt--->'+str(get_edited_bill_amt))
        Trace.Write('gettotalamt--->'+str(gettotalamt))
        Trace.Write('getannual_amt--->'+str(getannual_amt))
        countVal = SqlHelper.GetFirst("select cnt=count(1) from SAQIBP (nolock) where QUOTE_RECORD_ID ='{CT}' AND QTEREV_RECORD_ID ='{revision_rec_id}' and  EQUIPMENT_ID ='{EID}' and SERVICE_ID = '{service_id_param}' and LINE='{getline}' and BILLING_DATE = '{BD}'".format(service_id_param=TreeParam,CT = str(ContractRecordId),EID=value[0],BD = value[1],getline=getline, revision_rec_id = quote_revision_record_id))
        if int(countVal.cnt) > 1:
            billVal = float(value[2].replace(",","")) / 2
        else:
            billVal = float(value[2].replace(",",""))
        Trace.Write('billVal--->'+str(type(billVal)))
        get_exchange_val = Sql.GetFirst("SELECT EXCHANGE_RATE FROM SAQTRV where QUOTE_RECORD_ID ='{CT}' AND QTEREV_RECORD_ID ='{revision_rec_id}'".format(CT = str(ContractRecordId),revision_rec_id = quote_revision_record_id))
        bill_val_in_doc_currency = float(get_exchange_val.EXCHANGE_RATE)*float(billVal)
        Trace.Write('bill_val_in_doc_currency--->'+str(bill_val_in_doc_currency))
        if str(get_bill_type.BILLING_TYPE).upper() in  ("FIXED","MILESTONE"):
            if billVal >= 0.0 and TreeParam != 'Z0116':
                edit_billmatrix = "UPDATE SAQIBP SET BILLING_VALUE_INGL_CURR = {BT},BILLING_VALUE={BV} where QUOTE_RECORD_ID ='{CT}' AND QTEREV_RECORD_ID ='{revision_rec_id}' and  EQUIPMENT_ID ='{EID}' and SERVICE_ID = '{service_id_param}' and LINE='{getline}' and BILLING_DATE = '{BD}'".format(BT= billVal,service_id_param=TreeParam,CT = str(ContractRecordId),EID=value[0],BD = value[1],getline=getline, revision_rec_id = quote_revision_record_id,BV=bill_val_in_doc_currency)
                Sql.RunQuery(edit_billmatrix)
            if TreeParam == 'Z0116':
                edit_billmatrix = "UPDATE SAQIBP SET BILLING_VALUE_INGL_CURR = {BT},BILLING_VALUE={BV} where QUOTE_RECORD_ID ='{CT}' AND QTEREV_RECORD_ID ='{revision_rec_id}'  and SERVICE_ID = '{service_id_param}' and LINE='{getline}' and BILLING_DATE = '{BD}'".format(BT= billVal,service_id_param=TreeParam,CT = str(ContractRecordId),BD = value[1],getline=getline, revision_rec_id = quote_revision_record_id,BV=bill_val_in_doc_currency)
                Sql.RunQuery(edit_billmatrix)
        else:
            if billVal >= 0.0 and TreeParam != 'Z0116':
                edit_billmatrix = "UPDATE SAQIBP SET ESTVAL_INGL_CURR = {BT},ESTVAL_INDT_CURR={BTV} where QUOTE_RECORD_ID ='{CT}' AND QTEREV_RECORD_ID ='{revision_rec_id}' and  EQUIPMENT_ID ='{EID}' and SERVICE_ID = '{service_id_param}' and BILLING_DATE = '{BD}' and LINE='{getline}'".format(BT= billVal,service_id_param=TreeParam,CT = str(ContractRecordId),EID=value[0],BD = value[1],getline=getline, revision_rec_id = quote_revision_record_id,BTV=bill_val_in_doc_currency)
                Sql.RunQuery(edit_billmatrix)
            if TreeParam == 'Z0116':
                edit_billmatrix = "UPDATE SAQIBP SET ESTVAL_INGL_CURR = {BT},ESTVAL_INDT_CURR={BTV} where QUOTE_RECORD_ID ='{CT}' AND QTEREV_RECORD_ID ='{revision_rec_id}'  and SERVICE_ID = '{service_id_param}' and BILLING_DATE = '{BD}' and LINE='{getline}'".format(BT= billVal,service_id_param=TreeParam,CT = str(ContractRecordId),BD = value[1],getline=getline, revision_rec_id = quote_revision_record_id,BTV=bill_val_in_doc_currency)
                Sql.RunQuery(edit_billmatrix)
            
            #@HPQC-1686 end
        if TreeParam != 'Z0116':
            gettotalamt_afterupdate = Sql.GetFirst("SELECT SUM(BILLING_VALUE_INGL_CURR) as ANNUAL_BILLING_AMOUNT,SUM(ESTVAL_INGL_CURR) as ESTVAL_INGL_CURR,SERVICE_ID,BILLING_TYPE FROM SAQIBP WHERE  QUOTE_RECORD_ID ='{cq}' and SERVICE_ID = '{service_id_param}' AND QTEREV_RECORD_ID ='{revision_rec_id}' and LINE='{getline}' and BILLING_YEAR = '{SubTab_Year}' and EQUIPMENT_ID = '{EID}'   GROUP BY SERVICE_ID,BILLING_TYPE".format(cq=str(ContractRecordId),SubTab_Year=SubTab_Year,EID=value[0],service_id_param=TreeParam,getline=getline, revision_rec_id = quote_revision_record_id  ))
            get_amt_after_update = gettotalamt_afterupdate.ANNUAL_BILLING_AMOUNT
        else:
            gettotalamt_afterupdate = Sql.GetFirst("SELECT SUM(BILLING_VALUE_INGL_CURR) as ANNUAL_BILLING_AMOUNT,SUM(ESTVAL_INGL_CURR) as ESTVAL_INGL_CURR,SERVICE_ID,BILLING_TYPE FROM SAQIBP WHERE  QUOTE_RECORD_ID ='{cq}' and SERVICE_ID = '{service_id_param}' AND QTEREV_RECORD_ID ='{revision_rec_id}' and LINE='{getline}' and BILLING_YEAR = '{SubTab_Year}'    GROUP BY SERVICE_ID,BILLING_TYPE".format(cq=str(ContractRecordId),SubTab_Year=SubTab_Year,service_id_param=TreeParam,getline=getline, revision_rec_id = quote_revision_record_id  ))
            get_amt_after_update = gettotalamt_afterupdate.ANNUAL_BILLING_AMOUNT
        if (float(get_amt_after_update) > float(getannual_amt) or float(get_amt_after_update) < float(getannual_amt)) and not savebill_msg:
            savebill = 'NOTSAVE'
            #Quote.GetCustomField('BILLING_MESSAGE').Content = 'BILLIING_MESSAGE_SHOW'
            savebill_msg += 'This Quote has the following notifications:'
            savebill_msg += ('<div class="col-md-12" ><label> <img src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/warning1.svg" alt="Warning"> 99999 | INCORRECT BILLING ITEMS | The billing items total price does not equal Annual Billing Amount. In order to complete pricing stage they must be equal.</label></div>')
            Quote.GetCustomField('BILL_FLAG').Content = 'BILL_FLAG_MESSAGE'
            Quote.SetGlobal("BILL_FLAG","BILL_FLAG_MESSAGE")
        elif float(get_amt_after_update) == float(getannual_amt):
            Trace.Write('savebill----EQUAL-->>'+str(savebill_msg)+'---savebill---'+str(savebill))
            savebill_msg = ''
            savebill  =''
            Quote.GetCustomField('BILL_FLAG').Content = ''
        else:
            if Quote.GetCustomField('BILL_FLAG').Content:
                Quote.GetCustomField('BILL_FLAG').Content = 'BILL_FLAG_MESSAGE'
            else:
                Quote.GetCustomField('BILL_FLAG').Content = ''
            savebill_msg += ''
            Trace.Write('savebill------>>'+str(savebill_msg)+'---BILL_FLAG---'+str(Quote.GetCustomField('BILL_FLAG').Content))
            #savebill  =''
    Trace.Write('savebill------>>'+str(savebill_msg)+'---savebill---'+str(savebill))
    return 'not saved',savebill,savebill_msg

try:
    GET_DICT =list(Param.billdict)
    
    #getedited_amt = Param.getedited_amt
except:
    Trace.Write('131---')
    GET_DICT = []
    #totalyear = "" 
    #getedited_amt = ""
try:
    totalyear = Param.totalyear
except:
    totalyear = ""
try:
    getedited_amt = Param.getedited_amt
except:
    getedited_amt = ""
try:
    TreeParentParam = Param.TreeParentParam
except:
    TreeParentParam = ""
try:
    TreeParam = Param.TreeParam
except:
    TreeParam = ""

ApiResponse = ApiResponseFactory.JsonResponse(BILLEDIT_SAVE(GET_DICT,totalyear,getedited_amt,TreeParam,TreeParentParam))
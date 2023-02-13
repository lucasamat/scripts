#   __script_name : CQBILLEDIT.PY
#   __script_description : THIS SCRIPT IS USED TO EDIT A RECORD WHEN THE USER CLICKS ON THE GRID.
#   __primary_author__ : DHURGA
#   __create_date : 17/11/2020
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
#INC08641933 M
def update_billing_plan_amt(bill_year=None,service_id=None):
    Sql.RunQuery("""UPDATE SAQIBP SET 
                    BILLING_VALUE=CASE WHEN SAQIBP.BILLING_TYPE IN ('MILESTONE','FIXED') THEN ISNULL(SAQIBP.BILLING_VALUE, 0) + (ISNULL(SAQIBP.ANNUAL_BILLING_AMOUNT, 0) - ISNULL(IQ.SUM_BILLING_VALUE,0)) ELSE 0 END,
                    ESTVAL_INDT_CURR=CASE WHEN SAQIBP.BILLING_TYPE = 'VARIABLE' THEN ISNULL(SAQIBP.ESTVAL_INDT_CURR, 0) + (ISNULL(SAQIBP.ANNUAL_BILLING_AMOUNT, 0) - ISNULL(IQ.SUM_ESTVAL_INDT_CURR,0)) ELSE 0 END                    
                FROM SAQIBP 
                JOIN (
                        SELECT 
                            SUM(ISNULL(BILLING_VALUE,0)) as SUM_BILLING_VALUE, 
                            SUM(ISNULL(ESTVAL_INDT_CURR,0)) as SUM_ESTVAL_INDT_CURR,                          
                            QUOTE_RECORD_ID, QTEREV_RECORD_ID, LINE, SERVICE_ID, 
                            BILLING_YEAR, MAX(CpqTableEntryId) AS MAX_ID
                        FROM SAQIBP 
                        WHERE QUOTE_RECORD_ID='{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID = '{ServiceId}' AND BILLING_YEAR = '{BillingYear}' 
                        GROUP BY QUOTE_RECORD_ID, QTEREV_RECORD_ID, SERVICE_ID, LINE, BILLING_YEAR
                    ) IQ ON SAQIBP.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND SAQIBP.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND SAQIBP.SERVICE_ID = IQ.SERVICE_ID AND SAQIBP.LINE = IQ.LINE AND SAQIBP.BILLING_YEAR = IQ.BILLING_YEAR AND SAQIBP.CpqTableEntryId = IQ.MAX_ID
                
                WHERE SAQIBP.QUOTE_RECORD_ID='{QuoteRecordId}' AND SAQIBP.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQIBP.SERVICE_ID = '{ServiceId}' AND SAQIBP.BILLING_YEAR = '{BillingYear}'""".format(QuoteRecordId=ContractRecordId,RevisionRecordId=quote_revision_record_id, ServiceId=service_id,BillingYear=bill_year))
#INC08641933 M
            
def BILLEDIT_SAVE(GET_DICT,totalyear,getedited_amt,TreeParam,TreeParentParam):
    
    #@HPQC-1686 start
    count = get_edited_bill_amt = 0

    #A055S000P01-20779 Start - M
    billing_lines = set()
    #A055S000P01-20779 End - M

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
        Trace.Write('SubTab_Year-->'+str(SubTab_Year))
        getannual_amt = value[3]

        #A055S000P01-20779 Start - M
        getline = value[4].strip()
        billing_lines.add(getline)
        #Trace.Write('billing_lines ' + str(billing_lines))
        #A055S000P01-20779 End - M

        get_edited_bill_amt = float(value[2].replace(',',''))
        bill_type = ''
        getannual_amt = int(float(getannual_amt.replace(',','')))
        if TreeParam == "Z0103 - BASE FEE":
            TreeParam = 'Z0103'
        get_bill_type = Sql.GetFirst("SELECT BILLING_TYPE FROM SAQRIT WHERE  QUOTE_RECORD_ID ='{cq}' and SERVICE_ID = '{service_id_param}' AND QTEREV_RECORD_ID ='{revision_rec_id}' ".format(cq=str(ContractRecordId),service_id_param=TreeParam,revision_rec_id = quote_revision_record_id))
    
        if get_bill_type:
            bill_type = get_bill_type.BILLING_TYPE        
        Trace.Write('billVal 0 --->'+str(float(value[2].replace(",",""))))
        countVal = Sql.GetFirst("select cnt=count(1) from SAQIBP (nolock) where QUOTE_RECORD_ID ='{CT}' AND QTEREV_RECORD_ID ='{revision_rec_id}' and  EQUIPMENT_ID ='{EID}' and SERVICE_ID = '{service_id_param}' and LINE='{getline}' and BILLING_DATE = '{BD}' and BILLING_YEAR='{billyear}'".format(service_id_param=TreeParam,CT = str(ContractRecordId),EID=value[0],BD = value[1],getline=getline, revision_rec_id = quote_revision_record_id,billyear=SubTab_Year))
        if int(countVal.cnt) > 1:
            billVal = float(value[2].replace(",","")) / 2
        else:
            billVal = float(value[2].replace(",",""))
        Trace.Write('billVal--->'+str(billVal))
        get_exchange_val = Sql.GetFirst("SELECT EXCHANGE_RATE FROM SAQTRV where QUOTE_RECORD_ID ='{CT}' AND QTEREV_RECORD_ID ='{revision_rec_id}'".format(CT = str(ContractRecordId),revision_rec_id = quote_revision_record_id))
        bill_val_in_doc_currency = float(get_exchange_val.EXCHANGE_RATE)*float(billVal)
        Trace.Write('bill_val_in_doc_currency--->'+str(bill_val_in_doc_currency))
        #INC08641933 M
        currency_rounding_obj = Sql.GetFirst("SELECT DISTINCT CASE WHEN ROUNDING_DECIMAL_PLACES = '' THEN 0 ELSE ROUNDING_DECIMAL_PLACES END  AS DECIMAL_PLACES, CASE WHEN ROUNDING_METHOD='ROUND DOWN' THEN 1 ELSE 0 END AS ROUNDING_METHOD FROM SAQRIT(NOLOCK) JOIN PRCURR (NOLOCK) ON SAQRIT.DOC_CURRENCY = PRCURR.CURRENCY WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' ".format(QuoteRecordId=ContractRecordId,QuoteRevisionRecordId=quote_revision_record_id))
        #INC08641933 M
        
        #INC08848914 - Start M
        currency_rounding_obj_GLCR = Sql.GetFirst("SELECT DISTINCT CASE WHEN ROUNDING_DECIMAL_PLACES = '' THEN 0 ELSE ROUNDING_DECIMAL_PLACES END  AS DECIMAL_PLACES, CASE WHEN ROUNDING_METHOD='ROUND DOWN' THEN 1 ELSE 0 END AS ROUNDING_METHOD FROM SAQRIT(NOLOCK) JOIN PRCURR (NOLOCK) ON SAQRIT.GLOBAL_CURRENCY = PRCURR.CURRENCY WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' ".format(QuoteRecordId=ContractRecordId,QuoteRevisionRecordId=quote_revision_record_id))
        #INC08848914 - End M
        
        if str(get_bill_type.BILLING_TYPE).upper() in  ("FIXED","MILESTONE"):
            if billVal >= 0.0 and TreeParam != 'Z0116':
                #INC08672366 M
                edit_billmatrix = "UPDATE SAQIBP SET BILLING_VALUE_INGL_CURR = {BT},BILLING_VALUE={BV} where QUOTE_RECORD_ID ='{CT}' AND QTEREV_RECORD_ID ='{revision_rec_id}' and  ISNULL(EQUIPMENT_ID, '') ='{EID}' and SERVICE_ID = '{service_id_param}' and LINE='{getline}' and BILLING_DATE = '{BD}' and BILLING_YEAR='{billyear}'".format(BT= billVal,service_id_param=TreeParam,CT = str(ContractRecordId),EID=value[0],BD = value[1],getline=getline,billyear=SubTab_Year, revision_rec_id = quote_revision_record_id,BV=bill_val_in_doc_currency)
                Sql.RunQuery(edit_billmatrix)
            if TreeParam == 'Z0116':
                edit_billmatrix = "UPDATE SAQIBP SET BILLING_VALUE_INGL_CURR = {BT},BILLING_VALUE={BV} where QUOTE_RECORD_ID ='{CT}' AND QTEREV_RECORD_ID ='{revision_rec_id}'  and SERVICE_ID = '{service_id_param}' and LINE='{getline}' and BILLING_DATE = '{BD}' and BILLING_YEAR='{billyear}'".format(BT= billVal,service_id_param=TreeParam,billyear=SubTab_Year,CT = str(ContractRecordId),BD = value[1],getline=getline, revision_rec_id = quote_revision_record_id,BV=bill_val_in_doc_currency)
                Sql.RunQuery(edit_billmatrix)
                #INC08672366 M
            #INC08641933 M,#INC08672366 M, INC08848914 - Start M
            if currency_rounding_obj:
                Sql.RunQuery("UPDATE SAQIBP SET BILLING_VALUE = ROUND(BILLING_VALUE ,CONVERT(INT,{DecimalPlaces}),CONVERT(INT,{RoundingMethod})),CpqTableEntryModifiedBy={user_id}, BILLING_VALUE_INGL_CURR = ROUND(BILLING_VALUE_INGL_CURR ,CONVERT(INT,{DecimalPlaces_INGL}),CONVERT(INT,{RoundingMethod_INGL})), CpqTableEntryDateModified = GETDATE() FROM SAQIBP (NOLOCK) where QUOTE_RECORD_ID ='{CT}' AND QTEREV_RECORD_ID ='{revision_rec_id}'  and BILLING_YEAR='{billyear}' and SERVICE_ID = '{service_id_param}' and LINE='{getline}' and BILLING_DATE = '{BD}' ".format(DecimalPlaces=currency_rounding_obj.DECIMAL_PLACES, RoundingMethod=currency_rounding_obj.ROUNDING_METHOD,service_id_param=TreeParam,CT = str(ContractRecordId),BD = value[1],getline=getline, user_id=User.Id,revision_rec_id = quote_revision_record_id,billyear=SubTab_Year, DecimalPlaces_INGL = currency_rounding_obj_GLCR.DECIMAL_PLACES, RoundingMethod_INGL = currency_rounding_obj_GLCR.ROUNDING_METHOD))
            #INC08641933 M,#INC08672366 M, INC08848914 - End M
        else:
            #INC08672366 M
            if billVal >= 0.0 and TreeParam != 'Z0116':
                edit_billmatrix = "UPDATE SAQIBP SET ESTVAL_INGL_CURR = {BT},ESTVAL_INDT_CURR={BTV} where QUOTE_RECORD_ID ='{CT}' AND QTEREV_RECORD_ID ='{revision_rec_id}' and  ISNULL(EQUIPMENT_ID, '') ='{EID}' and BILLING_YEAR='{billyear}' and SERVICE_ID = '{service_id_param}' and BILLING_DATE = '{BD}' and LINE='{getline}'".format(BT= billVal,service_id_param=TreeParam,CT = str(ContractRecordId),EID=value[0],BD = value[1],getline=getline,billyear=SubTab_Year, revision_rec_id = quote_revision_record_id,BTV=bill_val_in_doc_currency)
                Sql.RunQuery(edit_billmatrix)
            if TreeParam == 'Z0116':
                edit_billmatrix = "UPDATE SAQIBP SET ESTVAL_INGL_CURR = {BT},ESTVAL_INDT_CURR={BTV} where QUOTE_RECORD_ID ='{CT}' AND QTEREV_RECORD_ID ='{revision_rec_id}'  and SERVICE_ID = '{service_id_param}' and BILLING_DATE = '{BD}' and LINE='{getline}' and BILLING_YEAR='{billyear}'".format(BT= billVal,service_id_param=TreeParam,billyear=SubTab_Year,CT = str(ContractRecordId),BD = value[1],getline=getline, revision_rec_id = quote_revision_record_id,BTV=bill_val_in_doc_currency)
                Sql.RunQuery(edit_billmatrix)
            #INC08641933, INC08848914 - Start M
            if currency_rounding_obj:
                Sql.RunQuery("UPDATE SAQIBP SET BILLING_VALUE = ROUND(BILLING_VALUE ,CONVERT(INT,{DecimalPlaces}),CONVERT(INT,{RoundingMethod})),CpqTableEntryModifiedBy={user_id}, BILLING_VALUE_INGL_CURR = ROUND(BILLING_VALUE_INGL_CURR ,CONVERT(INT,{DecimalPlaces_INGL}),CONVERT(INT,{RoundingMethod_INGL})), CpqTableEntryDateModified = GETDATE() FROM SAQIBP (NOLOCK) where QUOTE_RECORD_ID ='{CT}' AND QTEREV_RECORD_ID ='{revision_rec_id}'  and SERVICE_ID = '{service_id_param}' and LINE='{getline}' and BILLING_YEAR='{billyear}' and BILLING_DATE = '{BD}' and  ISNULL(EQUIPMENT_ID,'') ='{EID}' ".format(DecimalPlaces=currency_rounding_obj.DECIMAL_PLACES, RoundingMethod=currency_rounding_obj.ROUNDING_METHOD,service_id_param=TreeParam,user_id=User.Id,CT = str(ContractRecordId),BD = value[1],getline=getline, revision_rec_id = quote_revision_record_id,billyear=SubTab_Year,EID=value[0], DecimalPlaces_INGL = currency_rounding_obj_GLCR.DECIMAL_PLACES, RoundingMethod_INGL = currency_rounding_obj_GLCR.ROUNDING_METHOD))
            #INC08641933 M,#INC08672366 M, INC08848914 - End M
            
            #@HPQC-1686 end

    #A055S000P01-20779 Start - M
    for line in billing_lines:
        bill_value = Sql.GetFirst("""SELECT SUM(CASE WHEN BILLING_TYPE IN ('MILESTONE','FIXED') THEN BILLING_VALUE_INGL_CURR ELSE ESTVAL_INGL_CURR END) AS total FROM SAQIBP (NOLOCK) WHERE QUOTE_RECORD_ID = '{CT}' AND QTEREV_RECORD_ID = '{revision_rec_id}' AND BILLING_YEAR = '{billyear}' AND SERVICE_ID = '{service_id_param}' AND LINE = '{getline}'""".format(CT = str(ContractRecordId), revision_rec_id = quote_revision_record_id, billyear = SubTab_Year, getline = line, service_id_param = TreeParam))

        Sql.RunQuery("UPDATE SAQIBP SET BILADJAMT_INGL_CURR = '{total}', BILADJ_DTYFLG = CASE WHEN ANNBILAMT_INGL_CURR <> {total} THEN 1 ELSE 0 END FROM SAQIBP (NOLOCK) WHERE QUOTE_RECORD_ID = '{CT}' AND QTEREV_RECORD_ID = '{revision_rec_id}' AND BILLING_YEAR = '{billyear}' AND SERVICE_ID = '{service_id_param}' AND LINE = '{getline}' ".format(CT = str(ContractRecordId), revision_rec_id = quote_revision_record_id, billyear = SubTab_Year, getline = line, service_id_param = TreeParam, total = bill_value.total))
    #A055S000P01-20779 End - M

        #INC08848914 - Start M    
    mismatched_billings_obj = Sql.GetList("SELECT MAX(SAQIBP.LINE) as LINE FROM SAQIBP JOIN SAQRIT ON SAQRIT.QUOTE_RECORD_ID = SAQIBP.QUOTE_RECORD_ID AND SAQRIT.QTEREV_RECORD_ID = SAQIBP.QTEREV_RECORD_ID AND SAQRIT.SERVICE_ID = SAQIBP.SERVICE_ID AND SAQRIT.LINE = SAQIBP.LINE WHERE SAQIBP.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQIBP.QTEREV_RECORD_ID = '{QuoteRevisionRecordId}' GROUP BY SAQIBP.QUOTE_RECORD_ID, SAQIBP.QTEREV_RECORD_ID, SAQIBP.SERVICE_ID, SAQIBP.LINE, SAQIBP.BILLING_YEAR HAVING SUM(CASE WHEN SAQIBP.BILLING_TYPE IN ('MILESTONE','FIXED') THEN SAQIBP.BILLING_VALUE_INGL_CURR ELSE SAQIBP.ESTVAL_INGL_CURR END) <> MAX(ANNBILAMT_INGL_CURR)".format(QuoteRecordId=str(ContractRecordId), QuoteRevisionRecordId=quote_revision_record_id))
    
    if mismatched_billings_obj:
        savebill = 'NOTSAVE'
        #Quote.GetCustomField('BILLING_MESSAGE').Content = 'BILLIING_MESSAGE_SHOW'
        #INC08818816 - Start - M
        get_error_msg = Sql.GetFirst("SELECT MESSAGE_TEXT FROM SYMSGS WHERE MESSAGE_CODE = 'BILL_MISMATCH' ")
        msg_text = get_error_msg.MESSAGE_TEXT
        savebill_msg += 'This Quote has the following notifications:'
        savebill_msg += ('<div class="col-md-12 alert-warning" ><label> <img src="/mt/APPLIEDMATERIALS_PRD/Additionalfiles/warning1.svg" alt="Warning">'+str(msg_text)+'</label></div>')            
        #INC08818816 - End - M
        Quote.SetGlobal("BILL_FLAG","BILL_FLAG_MESSAGE")
    else:
        savebill_msg += ''
        #Trace.Write('savebill------>>'+str(savebill_msg)+'---BILL_FLAG---'+str(Quote.GetCustomField('BILL_FLAG').Content))
        #savebill  =''
    #INC08848914 - End M
    #INC08641933 M - Round off document currency value
    if savebill == '':
        if TreeParam == "Z0103 - BASE FEE":
            TreeParam = 'Z0103'
        update_billing_plan_amt(bill_year=totalyear,service_id=TreeParam)
    #INC08641933 M
    Trace.Write('savebill------>>'+str(savebill_msg)+'---savebill---'+str(savebill))
    return 'not saved',savebill,savebill_msg

try:
    GET_DICT =list(Param.billdict)
except:
    GET_DICT = []
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
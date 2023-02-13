# =========================================================================================================================================
#   __script_name : CQANULEDIT.PY
#   __script_description : THIS SCRIPT IS USED TO EDIT THE ANNUAL GRID BASED ON ENTITLEMENT PRICING
#   __primary_author__ : WASIM ABDUL 
# ==========================================================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct
from SYDATABASE import SQL
							 
Sql = SQL()
import SYCNGEGUID as CPQID
						
try:
    contract_quote_rec_id = Quote.GetGlobal("contract_quote_record_id")
    quote_revision_rec_id = Quote.GetGlobal("quote_revision_record_id")
except:
    contract_quote_rec_id = ''
    quote_revision_rec_id = ''
					  
user_id = str(User.Id)
user_name = str(User.UserName) 
def constructcat4editablity(Quote_rec_id,MODE,values):
    get_revision_status = Sql.GetFirst("Select REVISION_STATUS FROM SAQTRV WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'  ".format(Quote_rec_id,quote_revision_rec_id))
    revision_status = get_revision_status.REVISION_STATUS
    #Trace.Write("Quote_rec_id"+str(Quote_rec_id))
    #Trace.Write("valuesvaluesvalues"+str(list(values)))
    #A055S000P01-20746 - Start - M
    get_all_lines =Sql.GetList("Select * from SAQICO(NOLOCK) WHERE QUOTE_RECORD_ID ='{contract_quote_rec_id}' and QTEREV_RECORD_ID = '{quote_revision_rec_id}' AND CpqTableEntryId IN ({values}) AND SERVICE_ID not in ('Z0117','Z0116','Z0101','Z0046','Z0048','Z0123')".format(contract_quote_rec_id = contract_quote_rec_id,quote_revision_rec_id = quote_revision_rec_id,values=",".join(values).replace("SAQICO-","")))
    annual_dict={}
    for line_values in get_all_lines:
        record_list=[]
        cpqid = CPQID.KeyCPQId.GetCPQId('SAQICO', str(line_values.QUOTE_ITEM_COVERED_OBJECT_RECORD_ID))
        # INC08699893 - Start - M
        if revision_status not in ('APR-APPROVAL PENDING','APR-RECALLED','APR-REJECTED','APR-APPROVED','OPD-PREPARING QUOTE DOCUMENTS','OPD-CUSTOMER REJECTED','OPD-CUSTOMER ACCEPTED','APR-SUBMITTED TO CUSTOMER','LGL-PREPARING LEGAL SOW','LGL-LEGAL SOW REJECTED','LGL-LEGAL SOW ACCEPTED','CBC-PREPARING CBC','CBC-CBC COMPLETED','BOK-CONTRACT CREATED','BOK-CONTRACT BOOKED') and line_values and line_values.STATUS in ('PRR-ON HOLD PRICING','OFFLINE PRICING','ACQUIRED','CFG-ON HOLD TKM'):
            # INC08699893 - END - M
                if (line_values.BPTTKP == 'Yes'):
                    editvalue1 ="BPTKCI"
                    editvalue2 ="BPTKPI"
                    record_list.append(editvalue1)
                    record_list.append(editvalue2)
                if(line_values.ATGKEY != 'Excluded' and line_values.ATGKEY != 'Exception' and str(line_values.ATGKEY) != ''):
                    editvalue3 = "ATGKEC"
                    editvalue4 = "ATGKEP"
                    record_list.append(editvalue3)
                    record_list.append(editvalue4)
                if(line_values.NWPTON == 'Yes'):
                    editvalue5 = "NWPTOC"
                    editvalue6 = "NWPTOP"
                    record_list.append(editvalue5)
                    record_list.append(editvalue6)
                if((line_values.CNSMBL_ENT in ('Some Exclusions','Some Inclusions') and  line_values.SERVICE_ID != 'Z0100') or (line_values.CNSMBL_ENT in ('Included','Some Inclusions') and line_values.SERVICE_ID == 'Z0100') ) and not (line_values.CNSMBL_ENT == 'Some Inclusions' and line_values.SERVICE_ID == 'Z0092') :#2004,#2047,#A055S000P01-20741 - M
                    editvalue7 = "CONSCP"
                    editvalue8 = "CONSPI"
                    record_list.append(editvalue7)
                    record_list.append(editvalue8)
                if(line_values.NCNSMB_ENT in ('Some Inclusions','Some Exclusions') and  line_values.SERVICE_ID != 'Z0100'):
                    editvalue9 = "NONCCI"
                    editvalue10 = "NONCPI"
                    record_list.append(editvalue9)
                    record_list.append(editvalue10)
                if(line_values.TGKPNS != 'Excluded' and str(line_values.TGKPNS) != ''):
                    editvalue11 = "ATKNCI"
                    editvalue12 = "ATKNPI"
                    record_list.append(editvalue11)
                    record_list.append(editvalue12)
                if((line_values.AMNCPE == True or line_values.AMNCPE == "1") and line_values.SERVICE_ID != 'Z0100') or line_values.STATUS == 'PRR-ON HOLD PRICING' or (line_values.AMNCCI > 0 or line_values.AMNPPI > 0) :
                    editvalue13="AMNCCI"
                    editvalue14="AMNPPI"
                    record_list.append(editvalue13)
                    record_list.append(editvalue14)
                if(line_values.AIUICC == "0" or line_values.AIUICC == False) or (line_values.AIUICI > 0 or line_values.AIUIPI > 0):
                    editvalue15="AIUICI"
                    editvalue16="AIUIPI"
                    record_list.append(editvalue15)
                    record_list.append(editvalue16)
                #A055S000P01-20746 - End - M
        annual_dict[str(cpqid)] = record_list
    Trace.Write("dictdictdict--->"+str(annual_dict)) 
    return str(annual_dict)

def constructpricingsummary(Quote_rec_id,MODE,values):
    get_revision_status = Sql.GetFirst("Select REVISION_STATUS FROM SAQTRV WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'  ".format(Quote_rec_id,quote_revision_rec_id))
    revision_status = get_revision_status.REVISION_STATUS
    get_all_lines =Sql.GetList("Select * from SAQICO(NOLOCK) WHERE QUOTE_RECORD_ID ='{contract_quote_rec_id}' and QTEREV_RECORD_ID = '{quote_revision_rec_id}' AND CpqTableEntryId IN ({values})".format(contract_quote_rec_id = contract_quote_rec_id,quote_revision_rec_id = quote_revision_rec_id,values=",".join(values).replace("SAQICO-","")))
    annual_dict_pricing={}
    for line_values in get_all_lines:
        record_list=[]
        cpqid = CPQID.KeyCPQId.GetCPQId('SAQICO', str(line_values.QUOTE_ITEM_COVERED_OBJECT_RECORD_ID))
        if revision_status not in ('APR-APPROVAL PENDING','APR-RECALLED','APR-REJECTED','APR-APPROVED','OPD-PREPARING QUOTE DOCUMENTS','OPD-CUSTOMER REJECTED','OPD-CUSTOMER ACCEPTED','APR-SUBMITTED TO CUSTOMER','LGL-PREPARING LEGAL SOW','LGL-LEGAL SOW REJECTED','LGL-LEGAL SOW ACCEPTED','CBC-PREPARING CBC','CBC-CBC COMPLETED','BOK-CONTRACT CREATED','BOK-CONTRACT BOOKED') and line_values:
            if (line_values.BPTTKP == 'Yes'):                
								   
                editvalue1 ="BPTKCI"
                editvalue2 ="BPTKPI"
                record_list.append(editvalue1)
                record_list.append(editvalue2)
            allvalue_edit1="TGADJP"
            allvalue_edit2="YOYPCT"
            allvalue_edit3="USRPRC"
            record_list.append(allvalue_edit1)
            record_list.append(allvalue_edit2)
            record_list.append(allvalue_edit3)
        annual_dict_pricing[str(cpqid)] = record_list
    Trace.Write("dictdictdict"+str(annual_dict_pricing)) 
    return str(annual_dict_pricing)

ACTION = Param.ACTION
try:
    values = Param.values
except:
    values = ""

if ACTION == 'CAT4_ENTITLMENT':
    MODE="EDIT"
    Quote_rec_id = Quote.GetGlobal("contract_quote_record_id")
    ApiResponse = ApiResponseFactory.JsonResponse(constructcat4editablity(Quote_rec_id,MODE,values))
elif ACTION == 'PRICING_SUMMARY':
    MODE="EDIT"
    Quote_rec_id = Quote.GetGlobal("contract_quote_record_id")
    ApiResponse = ApiResponseFactory.JsonResponse(constructpricingsummary(Quote_rec_id,MODE,values))
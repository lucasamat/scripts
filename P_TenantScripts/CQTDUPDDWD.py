# =========================================================================================================================================
#   __script_name : CQTDUPDDWD.PY
#   __script_description : THIS SCRIPT IS USED TO UPLOAD AND DOWMLOAD TABLE DATA
#   __primary_author__ : AYYAPPAN SUBRAMANIYAN
#   __create_date :23-12-2021
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import re
import datetime
import sys
import System.Net
from SYDATABASE import SQL
import time
from datetime import timedelta , date
Sql = SQL()
ScriptExecutor = ScriptExecutor
webclient = System.Net.WebClient()

class ContractQuoteSpareOpertion:

    def __init__(self, **kwargs):		
        self.user_id = str(User.Id)
        self.user_name = str(User.UserName)		
        self.datetime_value = datetime.datetime.now()		
        self.action_type = kwargs.get('action_type')	
        self.related_list_attr_name = kwargs.get('related_list_attr_name')	
        self.object_name = ''	
        self.tree_param = Quote.GetGlobal("TreeParam")
        self.upload_data = kwargs.get('upload_data')
        self.set_contract_quote_related_details()
        
    def set_contract_quote_related_details(self):
        try:
            self.contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
        except Exception:
            self.contract_quote_record_id = ''	
        try:
            self.contract_quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
        except Exception:
            self.contract_quote_revision_record_id = ''
        contract_quote_obj = Sql.GetFirst("SELECT QUOTE_ID, QUOTE_TYPE, QTEREV_ID FROM SAQTMT (NOLOCK) WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{QuoteRecordId}'".format(QuoteRecordId=self.contract_quote_record_id))
        if contract_quote_obj:
            self.contract_quote_id = contract_quote_obj.QUOTE_ID
            self.contract_quote_revision_id = contract_quote_obj.QTEREV_ID				
        else:
            self.contract_quote_id = ''
            self.contract_quote_revision_id = ''
        return True


class ContractQuoteDownloadTableData(ContractQuoteSpareOpertion):	

    def __init__(self, **kwargs):
        ContractQuoteSpareOpertion.__init__(self,  **kwargs)

    def get_results(self, table_total_rows=0, colums='*'):		
        start = 1
        end = 1000
        col=colums
        All_col=col.split(",")
        rpl_col ={'CONSUMABLE/NON CONSUMABLE':'MATPRIGRP_ID','CUSTOMER WILL ACCPET W/6K PART': 'CUSTOMER_ACCEPT_PART','CUSTOMER ANNUAL COMMIT':'CUSTOMER_ANNUAL_QUANTITY'}
        xls_cols=rpl_col.get
        All_col = [xls_cols(val,val) for val in All_col]
        col=','.join(All_col)
        cols=str(col)

        All_value=colums.split(",")
        replace_col ={'CONSUMABLE/NON CONSUMABLE':'MATPRIGRP_ID','CUSTOMER WILL ACCPET W/6K PART':"CASE WHEN CUSTOMER_ACCEPT_PART ='True' OR CUSTOMER_ACCEPT_PART ='TRUE' THEN 'Yes' ELSE 'No' END AS CUSTOMER_ACCEPT_PART",'CUSTOMER ANNUAL COMMIT':'CUSTOMER_ANNUAL_QUANTITY','EXCHANGE_ELIGIBLE':"CASE WHEN EXCHANGE_ELIGIBLE ='True' OR EXCHANGE_ELIGIBLE ='TRUE' THEN 'Yes' ELSE 'No' END AS EXCHANGE_ELIGIBLE",'CUSTOMER_PARTICIPATE':"CASE WHEN CUSTOMER_PARTICIPATE = 'True'  OR CUSTOMER_PARTICIPATE = 'TRUE'  THEN 'Yes' ELSE 'No' END AS CUSTOMER_PARTICIPATE",'CUSTOMER_ELIGIBLE':"CASE WHEN CUSTOMER_ELIGIBLE = 'True'  OR CUSTOMER_ELIGIBLE= 'TRUE'   THEN 'Yes' ELSE 'No' END AS CUSTOMER_ELIGIBLE"}
        xls_col=replace_col.get
        All_value = [xls_col(val,val) for val in All_value]
        colums=','.join(All_value)
        colums=str(colums)
        #source_object_primary_key_column_obj = Sql.GetFirst("SELECT RECORD_NAME FROM SYOBJH (NOLOCK) WHERE OBJECT_NAME = '{}'".format(self.object_name))				
        while start < table_total_rows:
            query_string_with_pagination = """
                            SELECT DISTINCT {Cols} FROM (
                                SELECT DISTINCT {Cols}, ROW_NUMBER()OVER(ORDER BY CpqTableEntryId) AS SNO FROM (
                                    SELECT DISTINCT {Columns}, CpqTableEntryId
                                    FROM {TableName} (NOLOCK)
                                    WHERE QUOTE_RECORD_ID ='{QuoteRecordId}' AND QTEREV_RECORD_ID='{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}'
                                    ) IQ)OQ
                            WHERE SNO>={Skip_Count} AND SNO<={Fetch_Count}              
                            """.format(Cols=cols,Columns=colums, TableName=self.object_name, QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id, ServiceId=self.tree_param, Skip_Count=start, Fetch_Count=end)

            table_data = Sql.GetList(query_string_with_pagination)
            if table_data is not None:				
                for row_data in table_data:
                    data = [row_obj.Value for row_obj in row_data]
                    #data = ['Yes' if str(val) =='TRUE'or str(val) =='True' else 'No' if str(val) == 'FALSE' or str(val) =='False' else val for val in data]
                    yield data
            start += 1000		
            end += 1000			
            if end > table_total_rows:
                end = table_total_rows			

    def _do_opertion(self):
        table_columns = []
        table_records = []
        related_list_obj = Sql.GetFirst(
            """SELECT SYOBJR.RECORD_ID, SYOBJR.SAPCPQ_ATTRIBUTE_NAME, SYOBJR.PARENT_LOOKUP_REC_ID, SYOBJR.OBJ_REC_ID, SYOBJR.NAME, SYOBJR.COLUMN_REC_ID, SYOBJR.COLUMNS, SYOBJH.OBJECT_NAME
                FROM SYOBJR (NOLOCK) 
                INNER JOIN SYOBJH (NOLOCK) ON SYOBJH.RECORD_ID = SYOBJR.OBJ_REC_ID
                WHERE SYOBJR.SAPCPQ_ATTRIBUTE_NAME = '{AttributeName}'
                """.format(	AttributeName=self.related_list_attr_name)
        )
        if related_list_obj:			
            table_columns = eval(related_list_obj.COLUMNS)
            Trace.Write("table_columns"+str(table_columns))

            replace_col ={'MATPRIGRP_ID':'CONSUMABLE/NON CONSUMABLE','CUSTOMER_ACCEPT_PART':'CUSTOMER WILL ACCPET W/6K PART','CUSTOMER_ANNUAL_QUANTITY' :'CUSTOMER ANNUAL COMMIT'}
            xls_col=replace_col.get
            table_columns = [xls_col(val,val) for val in table_columns]
            Trace.Write("table_columns_after"+str(table_columns))

            if (self.tree_param) == 'Z0108' or (self.tree_param) == 'Z0110':
                col=table_columns
                if (self.tree_param) == 'Z0108':
                    col[0:2]=[]
                    Trace.Write("@Z0108_columns"+str(col))
                else:
                    col[0:2]=[]
                    col=[x for x in col if "DELIVERY" not in x]
                    col.insert(14,'DELIVERY_MODE')
                    
                    Trace.Write("@Z0110_columns"+str(col))
                table_columns=col

            columns = ",".join(table_columns)
            Trace.Write(str(columns))		
            self.object_name = related_list_obj.OBJECT_NAME
            total_count_obj = Sql.GetFirst("""
                                            SELECT COUNT(*) as count
                                            FROM {TableName} (NOLOCK)
                                            WHERE QUOTE_RECORD_ID ='{QuoteRecordId}' AND QTEREV_RECORD_ID='{QuoteRevisionRecordId}' AND SERVICE_ID = '{ServiceId}'""".format(TableName=self.object_name, QuoteRecordId=self.contract_quote_record_id,QuoteRevisionRecordId=self.contract_quote_revision_record_id,ServiceId=self.tree_param))
            if total_count_obj:
                Trace.Write("inside"+str(total_count_obj))
                table_total_rows = total_count_obj.count
                if table_total_rows:
                    table_records = [data for data in self.get_results(table_total_rows, columns)]
            
            Trace.Write("@@")
            msg_txt = (
                    '<div  class="col-md-12" id="dirty-flag-warning"><div class="col-md-12 alert-info"><label> <img src="/mt/APPLIEDMATERIALS_PRD/Additionalfiles/infor_icon_green.svg" alt="Warning">'
                    + "NUMBER OF PART NUMBER IMPORTED SUCCESSFULLY"
                    + " :  : "
                    + " PART NUMBER FAILED : </label></div></div>"
                )	

        return table_columns, table_records, msg_txt		
        
    
class ContractQuoteUploadTableData(ContractQuoteSpareOpertion):	

    def __init__(self, **kwargs):
        ContractQuoteSpareOpertion.__init__(self,  **kwargs)
        self.columns = ""
        self.records = ""
        self.add_part_numbers =[]
        self.parts_attr={}
        self.subrecords=[]
        self.quote_id=Quote.CompositeNumber
        self.col =""
        self.rec =""
        self.all_rec=""
        self.temp_table_name=""

    def _dvalidation(self,end):
        start=26
        delivery_sum=0
        if str(self.subrecords[21]) == 'None' or str(self.subrecords[21]) == '':
            return 'NULL'
        for val in range(start, end+1):
            if str(self.subrecords[val]) == 'None' or str(self.subrecords[val]) == '':
                delivery_sum += 0
                continue
            else:
                delivery_sum += int(self.subrecords[val])
        if delivery_sum <= int(self.subrecords[21]):
            if str(self.subrecords[val]) == 'None' or str(self.subrecords[val]) == '':
                return 'NULL'
            else:	
                return int(self.subrecords[end])
        else:
            return 'NULL'

    def _prepare_bkp_table(self):
        self.col=re.sub(r'\[|\]',"",str(self.col))
        self.rec=re.sub(r'\[',"(",str(self.rec))
        self.rec=re.sub(r'\]',")",str(self.rec))
        self.rec=re.sub(r"None","''",str(self.rec))
        self.rec=re.sub(r"'NULL'","''",str(self.rec))
        self.rec=re.sub(r"'","''",str(self.rec))
        self.col = re.sub(r"'","",self.col)
        self.all_rec=str(self.all_rec)+","+str(self.rec)
    
    def _update_spare_parts(self):
        rec=self.all_rec[1:]
        spare_parts_temp_table_bkp = SqlHelper.GetFirst("sp_executesql @T=N'SELECT "+str(self.col)+" INTO "+str(self.temp_table_name)+" FROM (SELECT DISTINCT "+str(self.col)+" FROM (VALUES "+str(rec)+") AS TEMP("+str(self.col)+")) OQ ' ")

    def _do_opertion(self):
        try:
            self.temp_table_name ="EXCELUPDATE_SAQSPT_{}".format(self.quote_id)		
            if self.temp_table_name:
                spare_parts_temp_table_drop = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(self.temp_table_name)+"'' ) BEGIN DROP TABLE "+str(self.temp_table_name)+" END  ' ")
            
            for sheet_data in self.upload_data:	
                if not sheet_data.Value:	
                    break	
                xls_spare_records = list(sheet_data.Value)
                if xls_spare_records:
                    for index,sub_records in enumerate (list(xls_spare_records)):
                        self.subrecords=sub_records
                        if (sub_records[3]) != 'PART_DESCRIPTION':
                            #sub_records[1]=re.sub('Ã‚','',sub_records[1])
                            self.add_part_numbers.append(sub_records[2])
                            sub_records[1] = str(sub_records[1]).strip() if sub_records[1] else ''
                            sub_records[2] = str(sub_records[2]).strip() if sub_records[2] else ''
                            if (self.tree_param == 'Z0108'):
                                sub_records[14] = sub_records[14].upper() if sub_records[14] and sub_records[14].upper()  in ('OFFSITE') else ''
                                sub_records[15] = sub_records[15].upper() if sub_records[15] and sub_records[15].upper()  in ('SCHEDULED','UNSCHEDULED') else '' 
                                if sub_records[15] == '' or sub_records[14] == '':
                                    sub_records[14]=''
                                    sub_records[15]=''
                                self.parts_attr={"PART_NUMBER":sub_records[2],"CUSTOMER_PART_NUMBER":sub_records[1],"CUSTOMER_PARTICIPATE":sub_records[12],"CUSTOMER_ACCEPT_PART":sub_records[13],"DELIVERY_MODE":sub_records[14],"SCHEDULE_MODE":sub_records[15],"CUSTOMER_ANNUAL_QUANTITY":sub_records[21],"DELIVERY_1":self._dvalidation(26),"DELIVERY_2":self._dvalidation(27),"DELIVERY_3":self._dvalidation(28),"DELIVERY_4":self._dvalidation(29),"DELIVERY_5":self._dvalidation(30),"DELIVERY_6":self._dvalidation(31),"DELIVERY_7":self._dvalidation(32),"DELIVERY_8":self._dvalidation(33),"DELIVERY_9":self._dvalidation(34),"DELIVERY_10":self._dvalidation(35),"DELIVERY_11":self._dvalidation(36),"DELIVERY_12":self._dvalidation(37),"DELIVERY_13":self._dvalidation(38),"DELIVERY_14":self._dvalidation(39),"DELIVERY_15":self._dvalidation(40),"DELIVERY_16":self._dvalidation(41),"DELIVERY_17":self._dvalidation(42),"DELIVERY_18":self._dvalidation(43),"DELIVERY_19":self._dvalidation(44),"DELIVERY_20":self._dvalidation(45),"DELIVERY_21":self._dvalidation(46),"DELIVERY_22":self._dvalidation(47),"DELIVERY_23":self._dvalidation(48),"DELIVERY_24":self._dvalidation(49),"DELIVERY_25":self._dvalidation(50),"DELIVERY_26":self._dvalidation(51),"DELIVERY_27":self._dvalidation(52),"DELIVERY_28":self._dvalidation(53),"DELIVERY_29":self._dvalidation(54),"DELIVERY_30":self._dvalidation(55),"DELIVERY_31":self._dvalidation(56),"DELIVERY_32":self._dvalidation(57),"DELIVERY_33":self._dvalidation(58),"DELIVERY_34":self._dvalidation(59),"DELIVERY_35":self._dvalidation(60),"DELIVERY_36":self._dvalidation(61),"DELIVERY_37":self._dvalidation(62),"DELIVERY_38":self._dvalidation(63),"DELIVERY_39":self._dvalidation(64),"DELIVERY_40":self._dvalidation(65),"DELIVERY_41":self._dvalidation(66),"DELIVERY_42":self._dvalidation(67),"DELIVERY_43":self._dvalidation(68),"DELIVERY_44":self._dvalidation(69),"DELIVERY_45":self._dvalidation(70),"DELIVERY_46":self._dvalidation(71),"DELIVERY_47":self._dvalidation(72),"DELIVERY_48":self._dvalidation(73),"DELIVERY_49":self._dvalidation(74),"DELIVERY_50":self._dvalidation(75),"DELIVERY_51":self._dvalidation(76),"DELIVERY_52":self._dvalidation(77)}

                            elif(self.tree_param =='Z0110'):
                                sub_records[14] = sub_records[14].upper() if sub_records[14] and sub_records[14].upper()  in ('ONSITE','OFFSITE') else ''
                                sub_records[15] = sub_records[15].upper() if sub_records[15] and sub_records[15].upper()  in ('TSL SHARED','TSL NON-SHARED','LOW QTY ONSITE','ON REQUEST') else '' 
                                if sub_records[15] == '' or sub_records[14] == '':
                                    sub_records[14]=''
                                    sub_records[15]=''
                                self.parts_attr={"PART_NUMBER":sub_records[2],"CUSTOMER_PART_NUMBER":sub_records[1],"CUSTOMER_PARTICIPATE":sub_records[12],"CUSTOMER_ACCEPT_PART":sub_records[13],"DELIVERY_MODE":sub_records[14],"SCHEDULE_MODE":sub_records[15],"CUSTOMER_ANNUAL_QUANTITY":sub_records[21]}

                            self.col = self.parts_attr.keys()
                            self.rec = self.parts_attr.values()
                            self._prepare_bkp_table()

                            sub_records[3] =''				
        
                header = list(xls_spare_records[0]) + ['QUOTE_RECORD_ID','QTEREV_RECORD_ID']
                
                self.columns = ",".join(header)
                col=self.columns
                table_columns = col.split(",")
                replace_col ={'CONSUMABLE/NON CONSUMABLE':'MATPRIGRP_ID','CUSTOMER WILL ACCPET W/6K PART':'CUSTOMER_ACCEPT_PART','CUSTOMER ANNUAL COMMIT':'CUSTOMER_ANNUAL_QUANTITY'}
                xls_col=replace_col.get
                table_columns = [xls_col(val,val) for val in table_columns]

                self.columns = ",".join(table_columns)
                modified_records = []
                for spare_record in xls_spare_records[1:]:
                    
                    modified_records.append(str(tuple([float(spare_val) if type(spare_val) == "<type 'Decimal'>" else spare_val for spare_val in spare_record])))

                for spare_record in xls_spare_records:
                    if spare_record[1] and spare_record[1] != "NULL" and spare_record[1] != "null":
                        spare_record[1]=str(spare_record[1])
                    else:
                        spare_record[1] =""
                self.records = ', '.join(map(str, [str(tuple(list(spare_record)+[self.contract_quote_record_id, self.contract_quote_revision_record_id])) for spare_record in xls_spare_records[1:]])).replace("None","null").replace("'","''")
                self.records = self.records.replace("True","1").replace("False","0").replace ("Ã‚" ," ").replace("?","")
                self.records = re.sub(r"<?[a-zA-Z0-9_.\[ \]]+>", "0.00", self.records)
        except:
            Log.Info(" ERROR---->:" + str(sys.exc_info()[1]))
            Log.Info(" ERROR LINE NO---->:" + str(sys.exc_info()[-1].tb_lineno))
        self._update_spare_parts()
        self._add_parts()
        msg_text = self._message_txt()
        return "Import Success",msg_text

    def _message_txt(self):
        msg_txt = (
                    '<div  class="col-md-12" id="dirty-flag-warning"><div class="col-md-12 alert-info"><label> <img src="/mt/APPLIEDMATERIALS_PRD/Additionalfiles/infor_icon_green.svg" alt="Warning">PART NUMBERS IMPORTED SUCCESSFULLY </label></div></div>'
                )
        return msg_txt

    def _add_parts(self):
        spare_parts_existing_records_delete = SqlHelper.GetFirst("sp_executesql @T=N'DELETE FROM SAQSPT WHERE QUOTE_RECORD_ID = ''"+str(self.contract_quote_record_id)+"'' AND QTEREV_RECORD_ID = ''"+str(self.contract_quote_revision_record_id)+"'' ' ")
        spare_parts_existing_SAQIFP_records_delete = SqlHelper.GetFirst("sp_executesql @T=N'DELETE FROM SAQIFP WHERE QUOTE_RECORD_ID = ''"+str(self.contract_quote_record_id)+"'' AND QTEREV_RECORD_ID = ''"+str(self.contract_quote_revision_record_id)+"'' ' ")
        spare_parts_existing_SAQRIT_records_delete = SqlHelper.GetFirst("sp_executesql @T=N'DELETE FROM SAQRIT WHERE QUOTE_RECORD_ID = ''"+str(self.contract_quote_record_id)+"'' AND QTEREV_RECORD_ID = ''"+str(self.contract_quote_revision_record_id)+"'' ' ")
        spare_parts_existing_SAQRIS_records_delete = SqlHelper.GetFirst("sp_executesql @T=N'DELETE FROM SAQRIS WHERE QUOTE_RECORD_ID = ''"+str(self.contract_quote_record_id)+"'' AND QTEREV_RECORD_ID = ''"+str(self.contract_quote_revision_record_id)+"'' ' ")
        spare_parts_existing_SAQICO_records_delete = SqlHelper.GetFirst("sp_executesql @T=N'DELETE FROM SAQICO WHERE QUOTE_RECORD_ID = ''"+str(self.contract_quote_record_id)+"'' AND QTEREV_RECORD_ID = ''"+str(self.contract_quote_revision_record_id)+"'' ' ")

        nullify_SAQTRV = """UPDATE SAQTRV SET NET_VALUE_INGL_CURR = NULL ,ESTVAL_INGL_CURR = NULL, TAX_AMOUNT_INGL_CURR=NULL,TOTAL_AMOUNT_INGL_CURR= NULL,TOTAL_MARGIN_PERCENT=NULL,SALES_PRICE_INGL_CURR=NULL FROM SAQTRV  WHERE  QUOTE_RECORD_ID = '{quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_rec_id}'""".format(quote_rec_id = self.contract_quote_record_id,quote_revision_rec_id =self.contract_quote_revision_record_id)
        Sql.RunQuery(nullify_SAQTRV)
        part_numbers = [ele for ele in self.add_part_numbers if ele is not None]
        if part_numbers:			
            part_numbers=re.sub(r"'",'"',str(part_numbers))
            ScriptExecutor.ExecuteGlobal('CQPARTSINS',{"CPQ_Columns":{"Action": "LoadParts","Part_number":part_numbers,"QuoteID":Quote.CompositeNumber}})

def Factory(node=None):
    """Factory Method"""
    models = {
        "Download": ContractQuoteDownloadTableData,		
        "Upload": ContractQuoteUploadTableData,
    }
    return models[node]

parameters = {'related_list_attr_name':Param.RelatedListAttributeName, 'action_type':Param.ActionType}
try:
    parameters['upload_data'] = Param.UploadData
except Exception:
    parameters['upload_data'] = []
process_object = Factory(parameters.get('action_type'))(**parameters)
ApiResponse = ApiResponseFactory.JsonResponse(process_object._do_opertion())
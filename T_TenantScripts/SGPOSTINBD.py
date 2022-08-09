# =========================================================================================================================================
#   __script_name : SGPOSTINBD.PY(DEV)
#   __script_description : THIS SCRIPT IS USED TO UPDATE Accounts IN STAGING TABLE.
#   __primary_author__ : Abubakkar
#   __create_date : 2021-04-09
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import sys
import datetime

cpqentryid = ''

try :

    check_flag = 1
    status_flag = 0
    Parameter = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'SELECT' ")	
    Parameter1 = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'UPD' ")
    Parameter2 = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'DEL' ")
    while check_flag == 1:
        Jsonquery = SqlHelper.GetList("SELECT INTEGRATION_PAYLOAD,CpqTableEntryId from SYINPL(NOLOCK) WHERE INTEGRATION_NAME = 'DEBMAS' AND ISNULL(STATUS,'')='' ")
        if len(Jsonquery) > 0:
            for json_data in Jsonquery:
                splited_list = str(json_data.INTEGRATION_PAYLOAD)
                rebuilt_data = eval(splited_list)
                cpqentryid = str(json_data.CpqTableEntryId)

                
                primaryQuerysession =  SqlHelper.GetFirst("SELECT NEWID() AS A")
                today = datetime.datetime.now()
                Modi_date = today.strftime("%m/%d/%Y %H:%M:%S %p")


                if len(rebuilt_data) != 0:      

                    rebuilt_data = rebuilt_data["CPQ_Columns"]
                    Table_Names = rebuilt_data.keys()
                    
                    
                    for tn in Table_Names:
                        if tn in rebuilt_data:
                            if str(tn).upper() == "SAACNT":
                                if str(type(rebuilt_data[tn])) == "<type 'dict'>":
                                    Tbl_data = [rebuilt_data[tn]]
                                else:
                                    Tbl_data = rebuilt_data[tn]
                                    
                                Trace.Write("Tbl_data 8888 --->"+str(Tbl_data))  
                                    
                                for record_dict in Tbl_data:	

                                    for col in ['ACCOUNT_ID','ACCOUNT_NAME','ADDRESS_1','CITY','COUNTRY','POSTAL_CODE','STATE','ACCOUNTGROUP_ID','TAX_CODE','PAR_ACCOUNT_ID','LEGACY_FABLOC_ID','AGS_BLUEBOOK','AGS_CUST_SGMT','AGS_CUSSHT_NAME']:
                                        if col not in record_dict:
                                            record_dict[col] = ''	
                                    
                                    primaryQueryItems = SqlHelper.GetFirst( ""+ str(Parameter.QUERY_CRITERIA_1)+ " SAACNT_INBOUND (CITY,POSTAL_CODE,ACCOUNT_NAME,COUNTRY,STATE,ACCOUNT_ID,ADDRESS_1,ACCOUNTGROUP_ID,TAX_CODE,PAR_ACCOUNT_ID,	LEGACY_FBL_ID,cpqtableentrydatemodified,SESSION_ID,AGS_BLUEBOOK,AGS_CUST_SGMT,AGS_CUSSHT_NAME)  select  N''"+record_dict['CITY']+ "'',''"+record_dict['POSTAL_CODE']+ "'',N''"+record_dict['ACCOUNT_NAME']+ "'',N''"+record_dict['COUNTRY']+ "'',N''"+record_dict['STATE']+ "'',N''"+record_dict['ACCOUNT_ID']+ "'',N''"+record_dict['ADDRESS_1']+"'',N''"+record_dict['ACCOUNTGROUP_ID']+"'',N''"+record_dict['TAX_CODE']+ "'',N''"+record_dict['PAR_ACCOUNT_ID']+ "'',N''"+record_dict['LEGACY_FABLOC_ID']+ "'',''"+ str(Modi_date)+ "'',''"+ str(primaryQuerysession.A)+ "'',N''"+record_dict['AGS_BLUEBOOK']+ "'',N''"+record_dict['AGS_CUST_SGMT']+ "'',N''"+record_dict['AGS_CUSSHT_NAME']+ "'' ' ")		
                            
                            elif str(tn).upper() == "SAACCT": 
                                if str(type(rebuilt_data[tn])) == "<type 'dict'>":
                                    Tbl_data = [rebuilt_data[tn]]
                                else:
                                    Tbl_data = rebuilt_data[tn]
                                    
                                for record_dict in Tbl_data:	
                                    
                                    for col in ['ACCOUNT_ID','FIRST_NAME','LAST_NAME','CONTACT_ID','PHONE','EMAIL','MOBILE','FAX']:
                                        if col not in record_dict:
                                            record_dict[col] = ''					
                                            
                                    primaryQueryItems = SqlHelper.GetFirst( ""+ str(Parameter.QUERY_CRITERIA_1)+ " SAACNT_INBOUND (CONTACT_ID,PHONE,ACCOUNT_ID,FIRSTNAME,LASTNAME,EMAIL,FAX,MOBILE,INTEGRATION_OBJECT,cpqtableentrydatemodified,SESSION_ID)  select  N''"+str(record_dict['CONTACT_ID'])+ "'',''"+str(record_dict['PHONE'])+ "'',''"+str(record_dict['ACCOUNT_ID'])+ "'',N''"+record_dict['FIRST_NAME']+ "'',N''"+record_dict['LAST_NAME']+ "'',N''"+record_dict['EMAIL']+ "'',N''"+record_dict['FAX']+ "'',N''"+record_dict['MOBILE']+ "'',''SAACCT'',''"+ str(Modi_date)+ "'',''"+ str(primaryQuerysession.A)+ "'' ' ")
                                    
                            elif str(tn).upper() == "SASAAC": 
                                if str(type(rebuilt_data[tn])) == "<type 'dict'>":
                                    Tbl_data = [rebuilt_data[tn]]
                                else:
                                    Tbl_data = rebuilt_data[tn]
                                    
                                for record_dict in Tbl_data:
                                
                                    for col in ['ACCOUNT_ID','BLUEBOOK','CUSTOMER_PRICING_PROCEDURE','DISTRIBUTIONCHANNEL_ID','DIVISION_ID','SALESORG_ID','PAYMENTTERM_ID','EXCHANGE_RATE_TYPE','INCOTERM_ID','CURRENCY','PRICEGROUP_ID','REGION','PRICELIST_ID']:
                                        if col not in record_dict:
                                            record_dict[col] = ''
                                                                        
                                    primaryQueryItems = SqlHelper.GetFirst( ""+ str(Parameter.QUERY_CRITERIA_1)+ " SAACNT_INBOUND (DISTRIBUTIONCHANNEL_ID,BLUEBOOK,INCOTERM_ID,CUSTOMER_PRICING_PROCEDURE,REGION,SALESORG_ID,ACCOUNT_ID,PAYMENTTERM_ID,CURRENCY,DIVISION_ID,EXCHANGE_RATE_TYPE,PRICEGROUP_ID,PRICELIST_ID,INTEGRATION_OBJECT,cpqtableentrydatemodified,SESSION_ID)  select  ''"+str(record_dict['DISTRIBUTIONCHANNEL_ID'])+ "'',''"+str(record_dict['BLUEBOOK'])+"'',''"+str(record_dict['INCOTERM_ID'])+ "'',N''"+str(record_dict['CUSTOMER_PRICING_PROCEDURE'])+ "'',''"+str(record_dict['REGION'])+ "'',''"+str(record_dict['SALESORG_ID'])+ "'',N''"+str(record_dict['ACCOUNT_ID'])+ "'',''"+str(record_dict['PAYMENTTERM_ID'])+ "'',N''"+str(record_dict['CURRENCY'])+ "'',''"+str(record_dict['DIVISION_ID'])+ "'',''"+str(record_dict['EXCHANGE_RATE_TYPE'])+ "'',''"+record_dict['PRICEGROUP_ID']+ "'',''"+record_dict['PRICELIST_ID']+ "'',''SASAAC'',''"+ str(Modi_date)+ "'',''"+ str(primaryQuerysession.A)+ "'' ' ")
                            
                            elif str(tn).upper() == "SAACPF":
                                if str(type(rebuilt_data[tn])) == "<type 'dict'>":
                                    Tbl_data = [rebuilt_data[tn]]
                                else:
                                    Tbl_data = rebuilt_data[tn]									
                                
                                for record_dict in Tbl_data:

                                    for col in ['ACCOUNT_ID','PARTNER_ID','DISTRIBUTIONCHANNEL_ID','DIVISION_ID','SALESORG_ID','RANK','PARTNERFUNCTION_ID',]:
                                        
                                        if col not in record_dict:
                                            record_dict[col] = ''					
                                                                        
                                    primaryQueryItems = SqlHelper.GetFirst( ""+ str(Parameter.QUERY_CRITERIA_1)+ " SAACNT_INBOUND (DISTRIBUTIONCHANNEL_ID,PARTNERFUNCTION_ID,SALESORG_ID,ACCOUNT_ID,DIVISION_ID,RANK,PARTNER_ID,INTEGRATION_OBJECT,cpqtableentrydatemodified,SESSION_ID)  select  ''"+str(record_dict['DISTRIBUTIONCHANNEL_ID'])+"'',N''"+str(record_dict['PARTNERFUNCTION_ID'])+ "'',''"+str(record_dict['SALESORG_ID'])+ "'',''"+str(record_dict['ACCOUNT_ID'])+ "'',''"+str(record_dict['DIVISION_ID'])+ "'',''"+str(record_dict['RANK'])+ "'',''"+str(record_dict['PARTNER_ID'])+ "'',''SAACPF'',''"+ str(Modi_date)+ "'',''"+ str(primaryQuerysession.A)+ "'' ' ")
                            
                                    
                            elif str(tn).upper() == "SAASCT":
                                if str(type(rebuilt_data[tn])) == "<type 'dict'>":
                                    Tbl_data = [rebuilt_data[tn]]
                                else:
                                    Tbl_data = rebuilt_data[tn]
                                    
                                for record_dict in Tbl_data: 
                                
                                    for col in ['ACCOUNT_ID','COUNTRY','DISTRIBUTIONCHANNEL_ID','DIVISION_ID','SALESORG_ID','TAXCATEGORY_ID','TAXCLASSIFICATION_ID']:
                                        if col not in record_dict:
                                            record_dict[col] = ''					
                    
                                    primaryQueryItems = SqlHelper.GetFirst( ""+ str(Parameter.QUERY_CRITERIA_1)+ " SAACNT_INBOUND (TAXCLASSIFICATION_ID,DISTRIBUTIONCHANNEL_ID,TAXCATEGORY_ID,COUNTRY,SALESORG_ID,ACCOUNT_ID,DIVISION_ID,INTEGRATION_OBJECT,cpqtableentrydatemodified,SESSION_ID)  select  ''"+str(record_dict['TAXCLASSIFICATION_ID'])+ "'',''"+str(record_dict['DISTRIBUTIONCHANNEL_ID'])+ "'',N''"+record_dict['TAXCATEGORY_ID']+ "'',N''"+record_dict['COUNTRY']+ "'',''"+record_dict['SALESORG_ID']+ "'',N''"+record_dict['ACCOUNT_ID']+ "'',''"+record_dict['DIVISION_ID']+ "'',''"+str('SAASCT')+ "'',''"+ str(Modi_date)+ "'',''"+ str(primaryQuerysession.A)+ "'' ' ")


                    status_flag = 1					
                    primaryItems = SqlHelper.GetFirst(  ""+ str(Parameter1.QUERY_CRITERIA_1)+ "  SYINPL set STATUS = ''PROCESSED'' from SYINPL  (NOLOCK) WHERE CpqTableEntryId  = ''"+str(json_data.CpqTableEntryId)+ "'' AND ISNULL(STATUS ,'''')= '''' ' "    )
                    
        
        else:
            check_flag = 0
            
    if status_flag== 1 :  
        resp = ScriptExecutor.ExecuteGlobal("SGPOSTCACT")               
        ApiResponse = ApiResponseFactory.JsonResponse(str(resp))
    
except:
    #Log.Info("SGPOSTINBD cpqentryid ---->:" + str(cpqentryid))
    Log.Info("SGPOSTINBD ERROR---->:" + str(sys.exc_info()[1]))
    Log.Info("SGPOSTINBD ERROR LINE NO---->:" + str(sys.exc_info()[-1].tb_lineno))
    ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "400", "Message": str(sys.exc_info()[1])}]})
            
            

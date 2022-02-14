# =========================================================================================================================================
#   __script_name : CTPOSTCSGP.PY
#   __script_description : THIS SCRIPT IS USED TO INSERT CRM TO CPQ DATA IN STAGING TABLE FROM ECC TO CPQ
#   __primary_author__ : BAJI
#   __create_date : 2020-11-16
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import sys
import datetime

try :
    Jsonquery = SqlHelper.GetList("SELECT  INTEGRATION_PAYLOAD,INTEGRATION_KEY from SYINPL(NOLOCK) WHERE INTEGRATION_NAME = 'CRM_TO_CPQ_CONTRACT_DATA' AND ISNULL(STATUS,'')='' ")
    for json_data in Jsonquery:
        if "Param" in json_data.INTEGRATION_PAYLOAD:
            splited_list = json_data.INTEGRATION_PAYLOAD.split("%%")
            rebuilt_data = eval(splited_list[1])
        else:
            splited_list = json_data.INTEGRATION_PAYLOAD
            rebuilt_data = eval(splited_list)
        
        primaryQuerysession =  SqlHelper.GetFirst("SELECT NEWID() AS Guid")
        today = datetime.datetime.now()
        Modi_date = today.strftime("%m/%d/%Y %H:%M:%S %p")
        Parameter=SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME='SELECT' ")
        Parameter1 = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'UPD' ")

        if len(rebuilt_data) != 0 and 'CPQ_Columns' in rebuilt_data:      

            rebuilt_data = rebuilt_data["CPQ_Columns"]
            Table_Names = rebuilt_data.keys()
            Check_flag = 0
            
            for tn in Table_Names:
                if tn in rebuilt_data:
                    Check_flag = 1
                    if str(tn).upper() == "CTCNRT":
                        if str(type(rebuilt_data[tn])) == "<type 'dict'>":
                            Tbl_data = [rebuilt_data[tn]]
                        else:
                            Tbl_data = rebuilt_data[tn]
                            
                        for record_dict in Tbl_data:
                            if "QUOTE_ID" not in record_dict:
                                record_dict['QUOTE_ID'] = ""

                            if "OPPORTUNITY_ID" not in record_dict:
                                record_dict['OPPORTUNITY_ID'] = ""
                                
                            primaryQueryItems = SqlHelper.GetFirst( ""+ str(Parameter.QUERY_CRITERIA_1)+ " CTCNRT_INBOUND (SESSION_ID,CONTRACT_VALID_FROM,CONTRACT_VALID_TO,NET_VALUE,PO_NUMBER,CONTRACT_CURRENCY,CONTRACT_ID,CONTRACT_NAME,CONTRACT_STATUS,CONTRACT_TYPE,SALESOFFICE_ID,SALESORG_ID,cpqtableentrydatemodified,QUOTE_ID,OPPORTUNITY_ID)  select  ''"+ str(primaryQuerysession.Guid)+ "'',''"+str(record_dict['CONTRACT_VALID_FROM'])+ "'',''"+str(record_dict['CONTRACT_VALID_TO'])+ "'',''"+str(record_dict['NET_VALUE'])+ "'',''"+str(record_dict['PO_NUMBER'])+ "'',''"+record_dict['CONTRACT_CURRENCY']+ "'',''"+str(record_dict['CONTRACT_ID'])+ "'',''"+record_dict['CONTRACT_NAME']+ "'',''"+record_dict['CONTRACT_STATUS']+ "'',''"+record_dict['CONTRACT_TYPE']+ "'',''"+str(record_dict['SALESOFFICE_ID'])+ "'',''"+str(record_dict['SALESORG_ID'])+ "'',''"+ str(Modi_date)+ "'',''"+str(record_dict['QUOTE_ID'])+ "'',''"+str(record_dict['OPPORTUNITY_ID'])+ "'' ' ")
                            
                    elif str(tn).upper() == "CTCITM":
                        if str(type(rebuilt_data[tn])) == "<type 'dict'>":
                            Tbl_data = [rebuilt_data[tn]]
                        else:
                            Tbl_data = rebuilt_data[tn]
                            
                        for record_dict in Tbl_data:
                            primaryQueryItems = SqlHelper.GetFirst( ""+ str(Parameter.QUERY_CRITERIA_1)+ " CTCITM_INBOUND (SESSION_ID,CONTRACT_VALID_FROM,CONTRACT_VALID_TO,CURRENCY,DIVISION_ID,EXTENDED_PRICE,ITEM_STATUS,ITEM_TYPE,LINE_ITEM_ID,PO_ITEM,PO_NUMBER,QUANTITY,CONTRACT_ID,SERVICE_ID,UOM_ID,cpqtableentrydatemodified)  select  ''"+ str(primaryQuerysession.Guid)+ "'',''"+str(record_dict['CONTRACT_VALID_FROM'])+ "'',''"+str(record_dict['CONTRACT_VALID_TO'])+ "'',''"+str(record_dict['CURRENCY'])+ "'',''"+str(record_dict['DIVISION_ID'])+ "'',''"+str(record_dict['EXTENDED_PRICE'])+ "'',''"+str(record_dict['ITEM_STATUS'])+ "'',''"+str(record_dict['ITEM_TYPE'])+ "'',''"+str(record_dict['LINE_ITEM_ID'])+ "'',''"+str(record_dict['PO_ITEM'])+ "'',''"+str(record_dict['PO_NUMBER'])+ "'',''"+str(record_dict['QUANTITY'])+ "'',''"+str(record_dict['CONTRACT_ID'])+ "'',''"+str(record_dict['SERVICE_ID'])+ "'',''"+str(record_dict['UOM_ID'])+ "'',''"+ str(Modi_date)+ "'' ' ")
                            
                    elif str(tn).upper() == "CTCICO":
                        if str(type(rebuilt_data[tn])) == "<type 'dict'>":
                            Tbl_data = [rebuilt_data[tn]]
                        else:
                            Tbl_data = rebuilt_data[tn]
                            
                        for record_dict in Tbl_data:
                            primaryQueryItems = SqlHelper.GetFirst( ""+ str(Parameter.QUERY_CRITERIA_1)+ " CTCICO_INBOUND (SESSION_ID,EQUIPMENT_ID,LINE_ITEM_ID,CONTRACT_ID,SERIAL_NO,cpqtableentrydatemodified)  select  ''"+ str(primaryQuerysession.Guid)+ "'',''"+str(record_dict['EQUIPMENT_ID'])+ "'',''"+str(record_dict['LINE_ITEM_ID'])+ "'',''"+str(record_dict['CONTRACT_ID'])+ "'',''"+str(record_dict['SERIAL_NO'])+ "'',''"+ str(Modi_date)+ "'' ' ")
                            
                    elif str(tn).upper() == "CTCSCE":
                        if str(type(rebuilt_data[tn])) == "<type 'dict'>":
                            Tbl_data = [rebuilt_data[tn]]
                        else:
                            Tbl_data = rebuilt_data[tn]
                            
                        for record_dict in Tbl_data:
                            if "ENTITLEMENT_VALUE_CODE" not in record_dict:
                                record_dict['ENTITLEMENT_VALUE_CODE'] = ""
                            primaryQueryItems = SqlHelper.GetFirst( ""+ str(Parameter.QUERY_CRITERIA_1)+ " CTCSCE_INBOUND (SESSION_ID,ENTITLEMENT_NAME,ENTITLEMENT_VALUE_CODE,CONTRACT_ID,LINE_ITEM_ID,cpqtableentrydatemodified)  select  ''"+ str(primaryQuerysession.Guid)+ "'',''"+record_dict['ENTITLEMENT_NAME']+ "'',''"+str(record_dict['ENTITLEMENT_VALUE_CODE'])+ "'',''"+str(record_dict['CONTRACT_ID'])+ "'',''"+str(record_dict['LINE_ITEM_ID'])+ "'',''"+ str(Modi_date)+ "'' ' ")
                            
                    elif str(tn).upper() == "CTCIFP":
                        if str(type(rebuilt_data[tn])) == "<type 'dict'>":
                            Tbl_data = [rebuilt_data[tn]]
                        else:
                            Tbl_data = rebuilt_data[tn]
                            
                        for record_dict in Tbl_data:
                            primaryQueryItems = SqlHelper.GetFirst( ""+ str(Parameter.QUERY_CRITERIA_1)+ " CTCIFP_INBOUND (SESSION_ID,ANNUAL_QUANTITY,DELIVERY_MODE,EXTENDED_PRICE,LINE_ITEM_ID,PART_NUMBER,CONTRACT_ID,SCHEDULE_MODE,UNIT_PRICE,VALID_FROM_DATE,VALID_TO_DATE,RELEASED_QUANTITY,cpqtableentrydatemodified)  select  ''"+ str(primaryQuerysession.Guid)+ "'',''"+str(record_dict['ANNUAL_QUANTITY'])+ "'',''"+str(record_dict['DELIVERY_MODE'])+ "'',''"+str(record_dict['EXTENDED_PRICE'])+ "'',''"+str(record_dict['LINE_ITEM_ID'])+ "'',''"+str(record_dict['PART_NUMBER'])+ "'',''"+str(record_dict['CONTRACT_ID'])+ "'',''"+str(record_dict['SCHEDULE_MODE'])+ "'',''"+str(record_dict['UNIT_PRICE'])+ "'',''"+str(record_dict['VALID_FROM_DATE'])+ "'',''"+str(record_dict['VALID_TO_DATE'])+ "'',''"+str(record_dict['RELEASED_QUANTITY'])+ "'',''"+ str(Modi_date)+ "'' ' ")
                            
                    elif str(tn).upper() == "CTCTIP":
                        if str(type(rebuilt_data[tn])) == "<type 'dict'>":
                            Tbl_data = [rebuilt_data[tn]]
                        else:
                            Tbl_data = rebuilt_data[tn]
                            
                        for record_dict in Tbl_data:
                            Dt = {}
                            Dt['CONTRACT_ID'] = record_dict['CONTRACT_ID']                                              
                            del record_dict['CONTRACT_ID']
                            for partyrole in record_dict:
                                PARTY_ID= record_dict[partyrole] 
                            
                                primaryQueryItems = SqlHelper.GetFirst( ""+ str(Parameter.QUERY_CRITERIA_1)+ " CTCTIP_INBOUND (SESSION_ID,CONTRACT_ID,PARTY_ROLE,PARTY_ID,cpqtableentrydatemodified) select ''"+ str(primaryQuerysession.Guid)+ "'',''"+str(Dt['CONTRACT_ID'])+ "'',''"+partyrole+ "'',''"+str(PARTY_ID)+ "'',''"+ str(Modi_date)+ "'' ' ")
                                
            primaryItems = SqlHelper.GetFirst(  ""+ str(Parameter1.QUERY_CRITERIA_1)+ "  SYINPL set STATUS = ''PROCESSED'' from SYINPL  (NOLOCK) WHERE INTEGRATION_KEY  = ''"+str(json_data.INTEGRATION_KEY)+ "'' AND ISNULL(STATUS ,'''')= '''' ' "    )
            if Check_flag == 1:     
                resp = ScriptExecutor.ExecuteGlobal("CTPOSTCTBK")  
                ApiResponse = ApiResponseFactory.JsonResponse(resp)          
                #ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "200", "Message": "Contract has been successfully stored in the staging table in CPQ."}]})
                
except:
    Log.Info("CTPOSTCSGP ERROR---->:" + str(sys.exc_info()[1]))
    Log.Info("CTPOSTCSGP ERROR LINE NO---->:" + str(sys.exc_info()[-1].tb_lineno))
    ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "400", "Message": str(sys.exc_info()[1])}]})
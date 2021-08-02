# __script_name : CQUPDLNITM .PY
# __script_description : THIS SCRIPT IS used to load additional data for quote line items
# __primary_author__ :Dhurga
# __create_date :7/29/2021
# © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import re
import datetime
gettodaydate = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S %p")
def getData():
    Quotelinecommments = Quote.QuoteTables["SAQICD"]
    data = []
    sec_list = []
    counter = 0
    data_info = ''
    tr_class = 'editable'
    section_row1 = {}
    CrtId = TagParserProduct.ParseString("<*CTX( Quote.CartId )*>")
    Ownrid = TagParserProduct.ParseString("<*CTX( Quote.OwnerId )*>")
    QuoteNumber=Quote.GetGlobal("contract_quote_record_id")
    getquoteid = SqlHelper.GetFirst("select QUOTE_ID from SAQTMT where MASTER_TABLE_QUOTE_RECORD_ID = '"+str(QuoteNumber)+"'")
    for item in Quote.Items :
        rolled_up_id = factor_id =rate = con_type = ""
        section_row1[str("dyn_" + str(item.Rank))] = ""
        Queryload = SqlHelper.GetList("select ownerId,cartId,CONDITION_COUNTER,CONDITION_CURRENCY,CONDITION_DATA_TYPE,CONDITION_RATE,CONDITION_TYPE,CONDITIONTYPE_NAME,CONDITIONTYPE_RECORD_ID,UOM,CONDITION_VALUE,UOM_RECORD_ID,LINE,QUOTE_ID,QTEITM_RECORD_ID,QUOTE_NAME,SERVICE_DESCRIPTION,SERVICE_ID,STEP_NUMBER,SERVICE_RECORD_ID,QUOTE_RECORD_ID,CONDITION_BASE from QT__SAQICD where QUOTE_ID = '"+str(getquoteid.QUOTE_ID)+"'  and SERVICE_ID= '"+str(item.PartNumber)+"' ")
        if Queryload and counter == 0:
            for row in Queryload:
                rolled_up_id ="dyn_" + "1"
                rate += "<td class='numberalign'>"+str(row.CONDITION_RATE).strip()+"</td>"
                if str(item.PartNumber) == str(row.SERVICE_ID) :
                    Trace.Write('CONDITION_TYPE----'+str(row.CONDITION_TYPE))
                    con_type = str(row.CONDITION_TYPE).strip()
                    if con_type == "None":
                        con_type = ''
                    else:
                        con_type
                    Trace.Write('CONDITION_TYPE--con_type----'+str(con_type))
                    data_info += "<tr class='"+tr_class+"' id='1' > <td class='textalign' id=' "+str(row.SERVICE_ID)+"'>"+str(row.STEP_NUMBER)+"</td> <td class='textalign'>"+str(con_type)+"</td> <td class='textalign'>"+str(row.CONDITIONTYPE_NAME).replace("`","'")+"</td> <td class='numberalign'>"+str(row.CONDITION_RATE).strip()+"</td> <td class='textalign'>"+str(row.CONDITION_CURRENCY).strip()+"</td> <td class='numberalign'>"+str(row.CONDITIONTYPE_RECORD_ID)+"</td> <td class='numberalign'>"+str(row.CONDITION_VALUE)+"</td> <td class='textalign'>"+str(row.UOM)+"</td> <td class='textalign'>STATIC</td> <td class='textalign'>"+str(row.CONDITION_DATA_TYPE).strip()+"</td><td class='textalign'>"+str(row.CONDITION_BASE).strip()+"</td></tr>"
        data.append({rolled_up_id:data_info})
    Trace.Write(str(data))
    return data
LoadAction = Param.LoadAction
if LoadAction == "LOADQT":
    ApiResponse = ApiResponseFactory.JsonResponse(getData())
# __script_name : CQUPDLNITM .PY
# __script_description : This script is used to load additional data for quote line items
# __primary_author__ :Dhurga
# __create_date :7/29/2021
# © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================

import datetime

gettodaydate = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S %p")

def getData():    
    data = []    
    counter = 0
    data_info = ''
    tr_class = 'editable'
    section_row1 = {}    
    quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
    QuoteNumber=Quote.GetGlobal("contract_quote_record_id")
    getquoteid = SqlHelper.GetFirst("select QUOTE_ID from SAQTMT where MASTER_TABLE_QUOTE_RECORD_ID = '"+str(QuoteNumber)+"' and QTEREV_RECORD_ID ='"+str(quote_revision_record_id)+"' ")
    for item in Quote.Items :
        rolled_up_id = rate = con_type = con_uom = con_rec = ""
        section_row1[str("dyn_" + str(item.Rank))] = ""
        Queryload = SqlHelper.GetList("select ownerId,cartId,CONDITION_COUNTER,CONDITION_CURRENCY,CONDITION_DATA_TYPE,CONDITION_RATE,CONDITION_TYPE,CONDITIONTYPE_NAME,CONDITIONTYPE_RECORD_ID,UOM,CONDITION_VALUE,UOM_RECORD_ID,LINE,QUOTE_ID,QTEITM_RECORD_ID,QUOTE_NAME,SERVICE_DESCRIPTION,SERVICE_ID,STEP_NUMBER,SERVICE_RECORD_ID,QUOTE_RECORD_ID,CONDITION_BASE from QT__SAQICD where QUOTE_ID = '"+str(getquoteid.QUOTE_ID)+"'  and SERVICE_ID= '"+str(item.PartNumber)+"' and QTEREV_RECORD_ID ='"+str(quote_revision_record_id)+"' ")
        if Queryload and counter == 0:
            for row in Queryload:
                rolled_up_id ="dyn_" + "1"
                rate += "<td class='numberalign'>"+str(row.CONDITION_RATE).strip()+"</td>"
                if str(item.PartNumber) == str(row.SERVICE_ID) :
                    Trace.Write('CONDITION_TYPE----'+str(row.CONDITION_TYPE))
                    con_type = str(row.CONDITION_TYPE).strip()
                    if con_type == "None":
                        con_type = ''
                    con_uom = str(row.UOM).strip()
                    if con_uom == "None":
                        con_uom = ''
                    else:
                        con_uom
                    con_rec = str(row.CONDITIONTYPE_RECORD_ID).strip()
                    if con_rec == "None":
                        con_rec = ''
                    else:
                        con_rec
                    Trace.Write('CONDITION_TYPE--con_type----'+str(con_type))
                    data_info += "<tr class='"+tr_class+"' id='1' > <td class='textalign' id=' "+str(row.SERVICE_ID)+"'>"+str(row.STEP_NUMBER)+"</td> <td class='textalign'>"+str(con_type)+"</td> <td class='textalign'>"+str(row.CONDITIONTYPE_NAME).replace("`","'")+"</td> <td class='numberalign'>"+str(row.CONDITION_RATE).strip()+"</td> <td class='textalign'>"+str(row.CONDITION_CURRENCY).strip()+"</td> <td class='numberalign'>"+str(con_rec)+"</td> <td class='numberalign'>"+str(row.CONDITION_VALUE)+"</td> <td class='textalign'>"+str(con_uom)+"</td> <td class='textalign'>STATIC</td> <td class='textalign'>"+str(row.CONDITION_DATA_TYPE).strip()+"</td><td class='textalign'>"+str(row.CONDITION_BASE).strip()+"</td></tr>"
        data.append({rolled_up_id:data_info})
    Trace.Write(str(data))
    return data
    
LoadAction = Param.LoadAction
if LoadAction == "LOADQT":
    ApiResponse = ApiResponseFactory.JsonResponse(getData())
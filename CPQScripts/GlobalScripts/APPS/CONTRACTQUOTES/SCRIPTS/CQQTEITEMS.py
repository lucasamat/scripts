# =========================================================================================================================================
#   __script_name : CQQTEITEMS.PY
#   __script_description : THIS SCRIPT IS USED TO LOAD SUMMARY IN QUOTE ITEMS
#   __primary_author__ : NAMRATA SIVAKUMAR
#   __create_date : 12/10/2021
#   Ã‚Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import re
import SYTABACTIN as Table
import SYCNGEGUID as CPQID
from SYDATABASE import SQL
Sql = SQL()

def LoadSummary():
    #ent_value = Quote.GetGlobal("IdlingAllowed")
    getRows = Sql.GetFirst("SELECT COUNT(CpqTableEntryId) as cnt FROM SAQTDA (NOLOCK) WHERE QTEREV_RECORD_ID = '{}'".format(quote_revision_record_id))
    if getRows:
        if getRows.cnt > 1:
            ent_value = "Yes"
        else:
            ent_value = "No"

    getValueSAQTDA = Sql.GetFirst("SELECT TOOLIDLING_DISPLAY_VALUE FROM SAQTDA(NOLOCK) WHERE TOOLIDLING_ID = 'Idling Allowed' AND QTEREV_RECORD_ID = '{}'".format(Quote.GetGlobal("quote_revision_record_id")))
    if getValueSAQTDA is None:
        ent_value = ent_value
    else:
        ent_value = getValueSAQTDA.TOOLIDLING_DISPLAY_VALUE
    sec_str = ""
    #Quote.SetGlobal("IdlingAllowed",ent_value)
    if ent_value == "Yes":
        yes_selected = ' selected=""'
        no_selected = ""
        sec_str += ('<table id="63FE9099-59CD-4CF2-BC6D-DD85CB96395B" class="getentdata table table-hover" data-filter-control="true" data-maintain-selected="true" data-locale="en-US" data-escape="true" data-html="true" data-show-header="true" onmouseup="relatedmouseup(this)"ondblclick="QuoteItemsIdlingEdit()"> <thead><tr><th title="TOOL IDLING" style="width:10%;" data-field="TOOL IDLING"><div class="th-inner sortable both">TOOL IDLING</div><div class="fht-cell"><div class="no-filter-control"></div></div></th><th title="DESCRIPTION" style="" data-field="DESCRIPTION"><div class="th-inner ">DESCRIPTION</div><div class="fht-cell"><div class="no-filter-control"></div></div></th><th title="*" class="required_symbol" style="" data-field="REQUIRED"><div class="th-inner ">*</div><div class="fht-cell"><div class="no-filter-control"></div></div></th><th title="VALUE" style="" data-field="VALUE"><div class="th-inner ">VALUE</div></tr></thead><tbody onclick="Table_Onclick_Scroll(this)"><tr data-index="0" class="hovergreyent" ><td style=""><abbr title="Idling Allowed">Idling Allowed</abbr></td><td style=""><abbr title="Option to Idle tools covered by Comprehensive Service agreements">Option to Idle tools covered by Comprehe..</abbr></td><td class="required_symbol" style=""><abbr class="required_symbol" title="Idling Allowed"> </abbr></td><td style=""><select class="form-control remove_yellow disable_edit" style="" id="IdlingAllowed" type="text" data-content="AGS_Z0091_KPI_PRPFGT" onchange="editent_bt(this)" title="'+ent_value+'" disabled=""><option value="select" style="display:none;"> </option><option id="IdlingAllowed" value="Yes" '+yes_selected+'>Yes</option><option id="IdlingAllowed" value="No" '+no_selected+'>No</option></select><a href="#" class="editclick"><i title="Double Click to Edit" class="fa fa-lock" aria-hidden="true"></i></a></td></tr>')
        
        ToolId = {}

        #getPRTIDA = Sql.GetFirst("SELECT TOOLIDLING_ID,TOOLIDLING_NAME FROM PRTIDA (NOLOCK)")
        getPRTIAV = Sql.GetList("SELECT TOP 25 SAQTDA.TOOLIDLING_ID,SAQTDA.TOOLIDLING_NAME,SAQTDA.TOOLIDLING_VALUE_CODE,SAQTDA.TOOLIDLING_DISPLAY_VALUE FROM SAQTDA (NOLOCK) JOIN PRTIDA (NOLOCK) ON SAQTDA.TOOLIDLING_ID = PRTIDA.TOOLIDLING_ID WHERE SAQTDA.QTEREV_RECORD_ID = '{}' AND SAQTDA.TOOLIDLING_ID != 'Idling Allowed' ORDER BY PRTIDA.DISPLAY_ORDER ASC ".format(Quote.GetGlobal("quote_revision_record_id")))
        
        ToolId = [x.TOOLIDLING_ID for x in getPRTIAV]
        ToolDesc = [x.TOOLIDLING_NAME for x in getPRTIAV]
        i = 1
        #listofkeys=sorted(ToolId.keys(), key=lambda x:x.lower())
        #Trace.Write("DICT="+str(ToolId))
        for x,y in zip(ToolId,ToolDesc):

            sec_str += '<tr data-index="'+str(i)+'" class="hovergreyent" ><td style="text-align: left;"><abbr title="'+x+'">'+x+'</abbr></td><td style="text-overflow:ellipsis; overflow: hidden; max-width:1px;"><abbr title="'+y+'">'+y+'</abbr></td>'

            
            i = int(i)
            i += 1
            getDefaultValue = Sql.GetFirst("SELECT TOOLIDLING_VALUE_CODE FROM SAQTDA (NOLOCK) WHERE TOOLIDLING_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(x,quote_revision_record_id))
            if getDefaultValue:
                if x == "Idle Notice Exception":
                    Trace.Write("Idle Notice")
                    sec_str += '<td class="required_symbol" style=""><abbr class="required_symbol" title="'+x+'"> </abbr></td><td style=""><input '+'value="'+getDefaultValue.TOOLIDLING_VALUE_CODE+'"  class="form-control no_border_bg disable_edit" style="" id="'+x.replace(" ","_")+'" type="text" onchange="QuoteItemsNoticeOnChange()" data-content="'+x.replace(" ","_")+'" style="color:#1B78D2" title="'+getDefaultValue.TOOLIDLING_VALUE_CODE+'" disabled = "">'
                elif x == "Idle Duration Exception":
                    Trace.Write("Idle Duration")
                    sec_str += '<td class="required_symbol" style=""><abbr class="required_symbol" title="'+x+'"> </abbr></td><td style=""><input '+'value="'+getDefaultValue.TOOLIDLING_VALUE_CODE+'"  class="form-control remove_yellow disable_edit" style="" id="'+x.replace(" ","_")+'" type="text" onchange="QuoteItemsDurationOnChange()" data-content="'+x.replace(" ","_")+'"  title="'+getDefaultValue.TOOLIDLING_VALUE_CODE+'" disabled = "" style="color:#1B78D2" >'
                elif x == "Idling Exception Notes":
                    Trace.Write("Idle Exception")
                    sec_str += '<td class="required_symbol" style=""><abbr class="required_symbol" title="'+x+'"> </abbr></td><td style=""><textarea '+'value="'+getDefaultValue.TOOLIDLING_VALUE_CODE+'"  class="form-control remove_yellow disable_edit" style="" id="'+x.replace(" ","_")+'" type="text" onchange="QuoteItemsExceptionOnChange()" data-content="'+x.replace(" ","_")+'"  title="'+getDefaultValue.TOOLIDLING_VALUE_CODE+'" disabled = "" rows = "1" cols="100" style="color:#1B78D2" >'+getDefaultValue.TOOLIDLING_VALUE_CODE+'</textarea>'
                else:
                    Trace.Write("Idle Else")
                    # style = ""
                    # if "of Tools" in x or "Fee" in x or "Notice" in x or "Duration" in x or "Exception" in x:
                    #     style = ' style="color:#1B78D2"'
                    if (x == "Cold Idle Allowed") or (x == "Warm / Hot Idle Allowed"):
                        sec_str += '<td class="required_symbol" style=""><abbr class="required_symbol" title="'+x+'">*</abbr></td><td style=""><select class="form-control remove_yellow disable_edit" style="" id="'+x.replace(" ","_")+'" type="text"  data-content="'+x.replace(" ","_")+'"  title="'+getDefaultValue.TOOLIDLING_VALUE_CODE+'" disabled = ""><option value="select" style="display:none;"> </option><option id="'+x.replace(" ","_")+'" value="'+getDefaultValue.TOOLIDLING_VALUE_CODE+'" selected = "">'+getDefaultValue.TOOLIDLING_VALUE_CODE+'</option>'

                    else:

                        sec_str += '<td class="required_symbol" style=""><abbr class="required_symbol" title="'+x+'"> </abbr></td><td style=""><select class="form-control remove_yellow disable_edit" style="" id="'+x.replace(" ","_")+'" type="text"  data-content="'+x.replace(" ","_")+'"  title="'+getDefaultValue.TOOLIDLING_VALUE_CODE+'" disabled = ""><option value="select" style="display:none;"> </option><option id="'+x.replace(" ","_")+'" value="'+getDefaultValue.TOOLIDLING_VALUE_CODE+'" selected = "">'+getDefaultValue.TOOLIDLING_VALUE_CODE+'</option>'

                
                    getAllValues = Sql.GetList("SELECT TOOLIDLING_VALUE_CODE FROM SAQTDA (NOLOCK) WHERE TOOLIDLING_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(x,quote_revision_record_id))
                    if getAllValues:
                        for val in getAllValues:
                            sec_str += '<option id="AGS_'+val.TOOLIDLING_VALUE_CODE+'" value="'+val.TOOLIDLING_VALUE_CODE+'" >'+val.TOOLIDLING_VALUE_CODE+'</option>'

                if ("Cold Idle Allowed" in x and "Yes" in getDefaultValue.TOOLIDLING_VALUE_CODE) or ("Hot Idle Allowed" in x and "Yes" in getDefaultValue.TOOLIDLING_VALUE_CODE) or "Idling type" in x:
                    sec_str += '</select><a href="#" class="editclick" style=" color:#dcdcdc !important;"><i title="" class="fa fa-lock" aria-hidden="true"></i></a></td></tr>'
                else:
                    sec_str += '</select><a href="#" class="editclick" style=" color:#dcdcdc !important;"><i title="Double Click to Edit" class="fa fa-pencil" aria-hidden="true"></i></a></td></tr>'
                
        sec_str += "</tbody></table>"
    elif ent_value == "No":
        yes_selected = ""
        no_selected =  ' selected=""'
        sec_str += ('<table id="63FE9099-59CD-4CF2-BC6D-DD85CB96395B" class="getentdata table table-hover" data-filter-control="true" data-maintain-selected="true" data-locale="en-US" data-escape="true" data-html="true" data-show-header="true" onmouseup="relatedmouseup(this)"ondblclick="QuoteItemsIdlingEdit()"> <thead><tr><th title="TOOL IDLING" style="" data-field="TOOL IDLING"><div class="th-inner sortable both">TOOL IDLING</div><div class="fht-cell"><div class="no-filter-control"></div></div></th><th title="DESCRIPTION" style="" data-field="DESCRIPTION"><div class="th-inner ">DESCRIPTION</div><div class="fht-cell"><div class="no-filter-control"></div></div></th><th title="*" class="required_symbol" style="" data-field="REQUIRED"><div class="th-inner ">*</div><div class="fht-cell"><div class="no-filter-control"></div></div></th><th title="VALUE" style="" data-field="VALUE"><div class="th-inner ">VALUE</div></tr></thead><tbody onclick="Table_Onclick_Scroll(this)"><tr data-index="0" class="hovergreyent" ><td style="text-align: left;"><abbr title="Idling Allowed">Idling Allowed</abbr></td><td style=""><abbr title="Option to Idle tools covered by">Option to Idle tools covered by</abbr></td><td class="required_symbol" style=""><abbr class="required_symbol" title="Idling Allowed"> </abbr></td><td style=""><select class="form-control remove_yellow disable_edit" style="" id="Idling_Allowed" type="text" data-content="AGS_Z0091_KPI_PRPFGT" onchange="editent_bt(this)" title="'+ent_value+'" disabled=""><option value="select" style="display:none;"> </option><option id="Idling_Allowed" value="Yes" '+yes_selected+'>Yes</option><option id="Idling_Allowed" value="No" '+no_selected+'>No</option></select><a href="#" class="editclick"><i title="Double Click to Edit" class="fa fa-lock" aria-hidden="true"></i></a></td></tr></tbody></table>')
    edit_lock_icon = "fa fa-lock"
    sec_str += "</div>"
    sec_str += "</div>"
    sec_str += "</div>"
    sec_str += '<table class="wth100mrg8"><tbody>'
    sec_str += "</tbody></table></div>"
    sec_str += "</div>"
    #Trace.Write("sec_str --->"+str(sec_str))
    
    getRevisionDetails = Sql.GetFirst("SELECT ISNULL(NET_VALUE_INGL_CURR,0.00) AS NET_VALUE_INGL_CURR,ISNULL(TAX_AMOUNT_INGL_CURR,0.00) AS TAX_AMOUNT_INGL_CURR,ISNULL(ESTVAL_INGL_CURR,0.00) AS ESTVAL_INGL_CURR, ISNULL(TOTAL_AMOUNT_INGL_CURR,0.00) AS TOTAL_AMOUNT_INGL_CURR,GLOBAL_CURRENCY,GLOBAL_CURRENCY_RECORD_ID,ISNULL(CNTMRG_INGL_CURR,0.00) AS CNTMRG_INGL_CURR,ISNULL(TOTAL_MARGIN_PERCENT,0.00) AS TOTAL_MARGIN_PERCENT FROM SAQTRV (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QUOTE_REVISION_RECORD_ID = '{}'".format(quote_record_id, quote_revision_record_id))
    curr = ""
    total_amount = 0.00    
    total_excluding = 0.00
    tax_amt = 0.00
    total_est = 0.00
    total_margin = 0.00
    total_margin_percent = 0.00
    
    if getRevisionDetails:
        get_rounding_place = Sql.GetFirst("SELECT * FROM PRCURR WHERE CURRENCY_RECORD_ID = '{}' ".format(getRevisionDetails.GLOBAL_CURRENCY_RECORD_ID))
        if get_rounding_place.DISPLAY_DECIMAL_PLACES:
            rounding_precsion = get_rounding_place.DISPLAY_DECIMAL_PLACES
        else:
            rounding_precsion = '3'
        decimal_format = "{:,." + str(rounding_precsion) + "f}"
        curr = str(getRevisionDetails.GLOBAL_CURRENCY)
        
        total_excluding = decimal_format.format(float(getRevisionDetails.NET_VALUE_INGL_CURR))
        tax_amt = decimal_format.format(float(getRevisionDetails.TAX_AMOUNT_INGL_CURR))
        total_est = decimal_format.format(float(getRevisionDetails.ESTVAL_INGL_CURR))
        total_amount = decimal_format.format(float(getRevisionDetails.TOTAL_AMOUNT_INGL_CURR))
        total_margin = decimal_format.format(float(getRevisionDetails.CNTMRG_INGL_CURR))
        total_margin_percent = decimal_format.format(float(getRevisionDetails.TOTAL_MARGIN_PERCENT))
        #BDPrice = decimal_format.format(float(getRevisionDetails.BD_PRICE_INGL_CURR))
        #CeilingPrice = decimal_format.format(float(getRevisionDetails.CEILING_PRICE_INGL_CURR))
        
        #argetPrice = decimal_format.format(float(getRevisionDetails.TARGET_PRICE_INGL_CURR))
        #Credit = decimal_format.format(float(getRevisionDetails.CREDIT_INGL_CURR))
    
        ##Updating the revision table values to custom fields  code starts...
        # Quote.GetCustomField('TARGET_PRICE').Content =decimal_format.format(float(getRevisionDetails.TARGET_PRICE_INGL_CURR))+ " " +curr
        # Quote.GetCustomField('BD_PRICE').Content = decimal_format.format(float(getRevisionDetails.BD_PRICE_INGL_CURR))+ " " +curr
        # Quote.GetCustomField('CEILING_PRICE').Content = decimal_format.format(float(getRevisionDetails.CEILING_PRICE_INGL_CURR))+ " " +curr
        # Quote.GetCustomField('TOTAL_NET_PRICE').Content = decimal_format.format(float(getRevisionDetails.TOTAL_AMOUNT_INGL_CURR))+ " " +curr
        #Quote.GetCustomField('TOTAL_NET_VALUE').Content = decimal_format.format(float(getRevisionDetails.TOTAL_AMOUNT_INGL_CURR))+ " " +curr
        ##Updating the revision table values to custom fields code ends..


    getQuoteDetails = Sql.GetFirst("SELECT QUOTE_ID,QUOTE_RECORD_ID, QTEREV_ID FROM SAQTRV (NOLOCK) WHERE QUOTE_REVISION_RECORD_ID = '{}'".format(Quote.GetGlobal("quote_revision_record_id")))
    QuoteId = getQuoteDetails.QUOTE_ID
    QuoteRecordId = getQuoteDetails.QUOTE_RECORD_ID
    QuoteRevisionId = getQuoteDetails.QTEREV_ID
    QuoteRevisionRecordId = Quote.GetGlobal("quote_revision_record_id")
    # return sec_str,str(TotalSalesPrice) + " " +curr,str(TotalDiscount)+ " %",str(total_excluding)+ " " +curr,str(tax_amt)+ " " +curr,str(total_amount)+ " " +curr,str(NetValue)+ " " +curr,str(Credit)+ " " +curr,str(DiscountAmount)+ " " +curr

    return sec_str,str(total_excluding) + " " +curr, str(tax_amt)+ " " +curr, str(total_est)+ " " +curr, str(total_amount)+ " " +curr, str(total_margin)+ " " +curr, str(total_margin_percent)+ " %"

quote_record_id = Quote.GetGlobal("contract_quote_record_id")
quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")


def EditToolIdling():
    #ent_value = Quote.GetGlobal("IdlingAllowed")
    getRows = Sql.GetFirst("SELECT COUNT(CpqTableEntryId) as cnt FROM SAQTDA (NOLOCK) WHERE QTEREV_RECORD_ID = '{}'".format(quote_revision_record_id))
    if getRows:
        if getRows.cnt > 1:
            ent_value = "Yes"
        else:
            ent_value = "No"
    if ent_value == "Yes":
        yes_selected = ' selected=""'
        no_selected = ""
    elif ent_value == "No":
        yes_selected = ""
        no_selected =  ' selected=""'
    sec_str = ""
    ToolId = {}
    if ent_value == "Yes":
        sec_str += ('<table id="63FE9099-59CD-4CF2-BC6D-DD85CB96395B" class="getentdata table table-hover" data-filter-control="true" data-maintain-selected="true" data-locale="en-US" data-escape="true" data-html="true" data-show-header="true" onmouseup="relatedmouseup(this)" ondblclick="QuoteItemsIdlingEdit()"> <thead><tr><th title="TOOL IDLING" style="" data-field="TOOL IDLING"><div class="th-inner sortable both">TOOL IDLING</div><div class="fht-cell"><div class="no-filter-control"></div></div></th><th title="DESCRIPTION" style="" data-field="DESCRIPTION"><div class="th-inner ">DESCRIPTION</div><div class="fht-cell"><div class="no-filter-control"></div></div></th><th title="*" class="required_symbol" style="" data-field="REQUIRED"><div class="th-inner ">*</div><div class="fht-cell"><div class="no-filter-control"></div></div></th><th title="VALUE" style="" data-field="VALUE"><div class="th-inner ">VALUE</div></tr></thead><tbody onclick="Table_Onclick_Scroll(this)"><tr data-index="0" class="hovergreyent" ><td style=""><abbr title="Idling Allowed">Idling Allowed</abbr></td><td style=""><abbr title="Option to Idle tools covered by Comprehensive Service agreements">Option to Idle tools covered by Comprehen..</abbr></td><td class="required_symbol" style=""><abbr class="required_symbol" title="Idling Allowed"> </abbr></td><td style=""><select class="form-control remove_yellow disable_edit" style="" id="Idling_Allowed" type="text" data-content="AGS_Z0091_KPI_PRPFGT" onchange="QuoteItemsIdlingOnChange()" title="'+ent_value+'" disabled ="" ><option value="select" style="display:none;"> </option><option id="Idling_Allowed" value="Yes" '+yes_selected+'>Yes</option><option id="Idling_Allowed" value="No" '+no_selected+'>No</option></select><a href="#" class="editclick"><i title="Double Click to Edit" class="fa fa-lock" aria-hidden="true"></i></a></td></tr>')
        getValueSAQTDA = Sql.GetFirst("SELECT TOOLIDLING_DISPLAY_VALUE FROM SAQTDA(NOLOCK) WHERE TOOLIDLING_ID = 'Idling Allowed' AND QTEREV_RECORD_ID = '{}'".format(Quote.GetGlobal("quote_revision_record_id")))
        if getValueSAQTDA is not None:
            #getPRTIDA = Sql.GetFirst("SELECT TOOLIDLING_ID,TOOLIDLING_NAME FROM PRTIDA (NOLOCK)")
            getPRTIAV = Sql.GetList("SELECT TOP 25 SAQTDA.TOOLIDLING_ID,SAQTDA.TOOLIDLING_NAME,SAQTDA.TOOLIDLING_VALUE_CODE,SAQTDA.TOOLIDLING_DISPLAY_VALUE FROM SAQTDA (NOLOCK) JOIN PRTIDA (NOLOCK) ON SAQTDA.TOOLIDLING_ID = PRTIDA.TOOLIDLING_ID WHERE SAQTDA.QTEREV_RECORD_ID = '{}' AND SAQTDA.TOOLIDLING_ID != 'Idling Allowed' ORDER BY PRTIDA.DISPLAY_ORDER ASC".format(Quote.GetGlobal("quote_revision_record_id")))
            

                
            ToolId = [x.TOOLIDLING_ID for x in getPRTIAV]
            ToolDesc = [x.TOOLIDLING_NAME for x in getPRTIAV]

            i = 1
            #listofkeys=sorted(ToolId.keys(), key=lambda x:x.lower())
            for x,y in zip(ToolId,ToolDesc):
                
                sec_str += '<tr data-index="'+str(i)+'" class="hovergreyent" ><td style="text-align: left;"><abbr title="'+x+'">'+x+'</abbr></td><td style="text-overflow:ellipsis; overflow: hidden; max-width:1px;"><abbr title="'+y+'">'+y+'</abbr></td>'
                i = int(i)
                i += 1
                getDefaultValue = Sql.GetFirst("SELECT TOOLIDLING_VALUE_CODE FROM SAQTDA (NOLOCK) WHERE TOOLIDLING_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(x,quote_revision_record_id))
                if getDefaultValue:
                    if x == "Idle Notice":
                        Trace.Write("Idle Notice")
                        sec_str += '<td class="required_symbol" style=""><abbr class="required_symbol" title="'+x+'"> </abbr></td><td style=""><select class="form-control light_yellow" style="" id="'+x.replace(" ","_")+'" type="text" onchange="QuoteItemsNoticeOnChange()" data-content="'+x.replace(" ","_")+'"  title="'+getDefaultValue.TOOLIDLING_VALUE_CODE+'" ><option value="select" style="display:none;"> </option><option id="'+x.replace(" ","_")+'" value="'+getDefaultValue.TOOLIDLING_VALUE_CODE+'" selected = "">'+getDefaultValue.TOOLIDLING_VALUE_CODE+'</option>'
                    elif x == "Idle Duration":
                        Trace.Write("Idle Duration")
                        sec_str += '<td class="required_symbol" style=""><abbr class="required_symbol" title="'+x+'"> </abbr></td><td style=""><select class="form-control light_yellow" style="" id="'+x.replace(" ","_")+'" type="text" onchange="QuoteItemsDurationOnChange()" data-content="'+x.replace(" ","_")+'"  title="'+getDefaultValue.TOOLIDLING_VALUE_CODE+'" ><option value="select" style="display:none;"> </option><option id="'+x.replace(" ","_")+'" value="'+getDefaultValue.TOOLIDLING_VALUE_CODE+'" selected = "">'+getDefaultValue.TOOLIDLING_VALUE_CODE+'</option>'
                    elif x == "Idling Exception":
                        Trace.Write("Idle Exception")
                        sec_str += '<td class="required_symbol" style=""><abbr class="required_symbol" title="'+x+'"> </abbr></td><td style=""><select class="form-control light_yellow" style="" id="'+x.replace(" ","_")+'" type="text" onchange="QuoteItemsExceptionOnChange()" data-content="'+x.replace(" ","_")+'"  title="'+getDefaultValue.TOOLIDLING_VALUE_CODE+'" ><option value="select" style="display:none;"> </option><option id="'+x.replace(" ","_")+'" value="'+getDefaultValue.TOOLIDLING_VALUE_CODE+'" selected = "">'+getDefaultValue.TOOLIDLING_VALUE_CODE+'</option>'
                    elif x == "Idle Notice Exception":
                        sec_str += '<td class="required_symbol" style=""><abbr class="required_symbol" title="'+x+'"> </abbr></td><td style=""><input '+'value="'+getDefaultValue.TOOLIDLING_VALUE_CODE+'"  class="form-control light_yellow" style="" id="'+x.replace(" ","_")+'" type="number" onchange="QuoteItemsNoticeOnChange()" data-content="'+x.replace(" ","_")+'"  title="'+getDefaultValue.TOOLIDLING_VALUE_CODE+'" oninput="this.value|=0">'
                    
                    elif x == "Idle Duration Exception":
                        sec_str += '<td class="required_symbol" style=""><abbr class="required_symbol" title="'+x+'"> </abbr></td><td style=""><input '+'value="'+getDefaultValue.TOOLIDLING_VALUE_CODE+'" class="form-control light_yellow" style="" id="'+x.replace(" ","_")+'" type="number" onchange="QuoteItemsDurationOnChange()" data-content="'+x.replace(" ","_")+'"  title="'+getDefaultValue.TOOLIDLING_VALUE_CODE+'" oninput="this.value|=0">'
                    elif x == "Idling Exception Notes":
                        sec_str += '<td class="required_symbol" style=""><abbr class="required_symbol" title="'+x+'"> </abbr></td><td style=""><textarea '+'value="'+getDefaultValue.TOOLIDLING_VALUE_CODE+'"  class="form-control related_popup_css txtArea light_yellow wid_90" style="" id="'+x.replace(" ","_")+'" type="text" onchange="QuoteItemsExceptionOnChange()" data-content="'+x.replace(" ","_")+'"  title="'+getDefaultValue.TOOLIDLING_VALUE_CODE+'" maxlength = "255" rows="1" cols="100" >'+getDefaultValue.TOOLIDLING_VALUE_CODE+'</textarea>'
                    elif x == "Cold Idle Allowed":
                        if getDefaultValue.TOOLIDLING_VALUE_CODE == "Yes":
                            sec_str += '<td class="required_symbol" style=""><abbr class="required_symbol" title="'+x+'">*</abbr></td><td style=""><select class="form-control remove_yellow disable_edit" style="" id="'+x.replace(" ","_")+'" type="text"  data-content="'+x.replace(" ","_")+'"  title="'+getDefaultValue.TOOLIDLING_VALUE_CODE+'" onchange="QuoteItemsColdOnChange()" disabled=""><option value="select" style="display:none;"> </option><option id="'+x.replace(" ","_")+'" value="'+getDefaultValue.TOOLIDLING_VALUE_CODE+'" selected = "">'+getDefaultValue.TOOLIDLING_VALUE_CODE+'</option>'
                        else:
                            sec_str += '<td class="required_symbol" style=""><abbr class="required_symbol" title="'+x+'">*</abbr></td><td style=""><select class="form-control light_yellow" style="" id="'+x.replace(" ","_")+'" type="text"  data-content="'+x.replace(" ","_")+'"  title="'+getDefaultValue.TOOLIDLING_VALUE_CODE+'" onchange="QuoteItemsColdOnChange()" ><option value="select" style="display:none;"> </option><option id="'+x.replace(" ","_")+'" value="'+getDefaultValue.TOOLIDLING_VALUE_CODE+'" selected = "">'+getDefaultValue.TOOLIDLING_VALUE_CODE+'</option>'
                    elif x == "Warm / Hot Idle Allowed":
                        if getDefaultValue.TOOLIDLING_VALUE_CODE == "Yes":
                            sec_str += '<td class="required_symbol" style=""><abbr class="required_symbol" title="'+x+'">*</abbr></td><td style=""><select class="form-control remove_yellow disable_edit" style="" id="WarmHotIdleAllowed" type="text"  data-content="'+x.replace(" ","_")+'"  title="'+getDefaultValue.TOOLIDLING_VALUE_CODE+'" onchange="QuoteItemsHotOnChange()" disabled=""><option value="select" style="display:none;"> </option><option id="'+x.replace(" ","_")+'" value="'+getDefaultValue.TOOLIDLING_VALUE_CODE+'" selected = "">'+getDefaultValue.TOOLIDLING_VALUE_CODE+'</option>'
                    
                        else:
                            sec_str += '<td class="required_symbol" style=""><abbr class="required_symbol" title="'+x+'">*</abbr></td><td style=""><select class="form-control light_yellow" style="" id="WarmHotIdleAllowed" type="text"  data-content="'+x.replace(" ","_")+'"  title="'+getDefaultValue.TOOLIDLING_VALUE_CODE+'" onchange="QuoteItemsHotOnChange()" ><option value="select" style="display:none;"> </option><option id="'+x.replace(" ","_")+'" value="'+getDefaultValue.TOOLIDLING_VALUE_CODE+'" selected = "">'+getDefaultValue.TOOLIDLING_VALUE_CODE+'</option>'
                    elif x == "Idling type":
                        sec_str += '<td class="required_symbol" style=""><abbr class="required_symbol" title="'+x+'"></abbr></td><td style=""><select class="form-control remove_yellow disable_edit" style="" id="Idling_type" type="text"  data-content="'+x.replace(" ","_")+'"  title="'+getDefaultValue.TOOLIDLING_VALUE_CODE+'" disabled=""><option value="select" style="display:none;"> </option><option id="'+x.replace(" ","_")+'" value="'+getDefaultValue.TOOLIDLING_VALUE_CODE+'" selected = "">'+getDefaultValue.TOOLIDLING_VALUE_CODE+'</option>'
                    else:
                        Trace.Write("Idle Else")
                        sec_str += '<td class="required_symbol" style=""><abbr class="required_symbol" title="'+x+'"> </abbr></td><td style=""><select class="form-control light_yellow" style="" id="'+x.replace(" ","_")+'" type="text"  data-content="'+x.replace(" ","_")+'"  title="'+getDefaultValue.TOOLIDLING_VALUE_CODE+'" ><option value="select" style="display:none;"> </option><option id="'+x.replace(" ","_")+'" value="'+getDefaultValue.TOOLIDLING_VALUE_CODE+'" selected = "">'+getDefaultValue.TOOLIDLING_VALUE_CODE+'</option>'

                    
                    getAllValues = Sql.GetList("SELECT TOOLIDLING_VALUE_CODE FROM PRTIAV (NOLOCK) WHERE TOOLIDLING_ID = '{}' AND TOOLIDLING_VALUE_CODE != {}'{}'".format(x,"N" if "28" in getDefaultValue.TOOLIDLING_VALUE_CODE or "30" in getDefaultValue.TOOLIDLING_VALUE_CODE else "",getDefaultValue.TOOLIDLING_VALUE_CODE))
                    if getAllValues:
                        for val in getAllValues:
                            sec_str += '<option id="'+x.replace(" ","_")+'" value="'+val.TOOLIDLING_VALUE_CODE+'" >'+val.TOOLIDLING_VALUE_CODE+'</option>'
                    if ("Cold Idle Allowed" in x and "Yes" in getDefaultValue.TOOLIDLING_VALUE_CODE) or ("Hot Idle Allowed" in x and "Yes" in getDefaultValue.TOOLIDLING_VALUE_CODE) or "Idling type" in x:
                        sec_str += '</select><a href="#" class="editclick" style=" color:#dcdcdc !important;"><i title="" class="fa fa-lock" aria-hidden="true"></i></a></td></tr>'
                    else:
                        sec_str += '</select><a href="#" class="editclick" style=" color:#dcdcdc !important;"><i title="Double Click to Edit" class="fa fa-pencil" aria-hidden="true"></i></a></td></tr>'
                    #sec_str += '</select><a href="#" class="editclick"><i title="Double Click to Edit" class="fa fa-pencil" aria-hidden="true"></i></a></td></tr>'
            sec_str += "</tbody></table>"
        else:
            #getPRTIDA = Sql.GetFirst("SELECT TOOLIDLING_ID,TOOLIDLING_NAME FROM PRTIDA (NOLOCK)")
            getPRTIAV = Sql.GetList("SELECT TOOLIDLING_ID,TOOLIDLING_NAME,TOOLIDLING_VALUE_CODE,TOOLIDLING_DISPLAY_VALUE FROM PRTIAV (NOLOCK) WHERE TOOLIDLING_ID != 'Idling Allowed'")
            
            for x in getPRTIAV:
                ToolId[x.TOOLIDLING_ID] = x.TOOLIDLING_NAME
            i = 1
            for x,y in ToolId.items():
                if x == "Idle Notice Exception":
                    Trace.Write("Idle Notice")
                    sec_str += '<tr id = "notice_onchange" data-index="'+str(i)+'" class="hovergreyent" ><td style="text-align: left;"><abbr title="'+x+'">'+x+'</abbr></td><td style="text-overflow:ellipsis; overflow: hidden; max-width:1px;"><abbr title="'+y+'">'+y+'</abbr></td><td class="required_symbol" style=""><abbr class="required_symbol" title="'+x+'"> </abbr></td><td style="">'
                elif x == "Idle Duration Exception":
                    Trace.Write("Idle Duration")
                    sec_str += '<tr id = "duration_onchange" data-index="'+str(i)+'" class="hovergreyent" ><td style="text-align: left;"><abbr title="'+x+'">'+x+'</abbr></td><td style="text-overflow:ellipsis; overflow: hidden; max-width:1px;"><abbr title="'+y+'">'+y+'</abbr></td><td class="required_symbol" style=""><abbr class="required_symbol" title="'+x+'"> </abbr></td><td style="">'
                elif x == "Idling Exception Notes":
                    Trace.Write("Idle Exception")
                    sec_str += '<tr id = "exception_onchange" data-index="'+str(i)+'" class="hovergreyent" ><td style="text-align: left;"><abbr title="'+x+'">'+x+'</abbr></td><td style="text-overflow:ellipsis; overflow: hidden; max-width:1px;"><abbr title="'+y+'">'+y+'</abbr></td><td class="required_symbol" style=""><abbr class="required_symbol" title="'+x+'"> </abbr></td><td style="">'
                else:
                    sec_str += '<tr data-index="'+str(i)+'" class="hovergreyent" ><td style="text-align: left;"><abbr title="'+x+'">'+x+'</abbr></td><td style="text-overflow:ellipsis; overflow: hidden; max-width:1px;"><abbr title="'+y+'">'+y+'</abbr></td><td class="required_symbol" style=""><abbr class="required_symbol" title="'+x+'"> </abbr></td><td style="">'
                i = int(i)
                i += 1
                getDefaultValue = Sql.GetFirst("SELECT TOOLIDLING_VALUE_CODE FROM PRTIAV (NOLOCK) WHERE TOOLIDLING_ID = '{}'".format(x))
                if getDefaultValue:
                    sec_str += '<select class="form-control light_yellow" style="" id="'+x.replace(" ","_")+'" type="text" data-content="AGS_'+x.strip()+'"  title="'+getDefaultValue.TOOLIDLING_VALUE_CODE+'" ><option value="select" style="display:none;"> </option><option id="'+x.replace(" ","_")+'" value="'+getDefaultValue.TOOLIDLING_VALUE_CODE+'" selected = "">'+getDefaultValue.TOOLIDLING_VALUE_CODE+'</option>'
                    
                    getAllValues = Sql.GetList("SELECT TOOLIDLING_VALUE_CODE FROM PRTIAV (NOLOCK) WHERE TOOLIDLING_ID = '{}' AND [DEFAULT] = 0".format(x))
                    if getAllValues:
                        for val in getAllValues:
                            sec_str += '<option id="'+x.replace(" ","_")+'" value="'+str(val.TOOLIDLING_VALUE_CODE)+'" >'+str(val.TOOLIDLING_VALUE_CODE)+'</option>'
                sec_str += '</select><a href="#" class="editclick"><i title="Double Click to Edit" class="fa fa-pencil" aria-hidden="true"></i></a></td></tr>'
            sec_str += "</tbody></table>"
    else:
        sec_str += ('<table id="63FE9099-59CD-4CF2-BC6D-DD85CB96395B" class="getentdata table table-hover" data-filter-control="true" data-maintain-selected="true" data-locale="en-US" data-escape="true" data-html="true" data-show-header="true" onmouseup="relatedmouseup(this)" ondblclick="QuoteItemsIdlingEdit()"> <thead><tr><th title="TOOL IDLING" style="" data-field="TOOL IDLING"><div class="th-inner sortable both">TOOL IDLING</div><div class="fht-cell"><div class="no-filter-control"></div></div></th><th title="DESCRIPTION" style="" data-field="DESCRIPTION"><div class="th-inner ">DESCRIPTION</div><div class="fht-cell"><div class="no-filter-control"></div></div></th><th title="*" class="required_symbol" style="" data-field="REQUIRED"><div class="th-inner ">*</div><div class="fht-cell"><div class="no-filter-control"></div></div></th><th title="VALUE" style="" data-field="VALUE"><div class="th-inner ">VALUE</div></tr></thead><tbody onclick="Table_Onclick_Scroll(this)"><tr data-index="0" class="hovergreyent" ><td style="text-align: left;"><abbr title="Idling Allowed">Idling Allowed</abbr></td><td style=""><abbr title="Option to Idle tools covered by">Option to Idle tools covered by</abbr></td><td class="required_symbol" style=""><abbr class="required_symbol" title="Idling Allowed"> </abbr></td><td style=""><select class="form-control light_yellow" style="" id="Idling_Allowed" type="text" data-content="AGS_Z0091_KPI_PRPFGT" onchange="QuoteItemsIdlingOnChange()" title="'+ent_value+'" ><option value="select" style="display:none;"> </option><option id="Idling_Allowed" value="Yes" '+yes_selected+'>Yes</option><option id="Idling_Allowed" value="No" '+no_selected+'>No</option></select></td></tr></tbody></table>')


    sec_str += '<div id="quotesummarysavecancel" class="col-md-12 text-center"><button id="hidesavecancel" class="btnconfig btnMainBanner sec_edit_sty_btn flt_none" onclick="QuoteItemsView()">CANCEL</button><button id="hidesavecancel" class="btnconfig btnMainBanner sec_edit_sty_btn flt_none" onclick="QuoteItemsIdlingSave()">SAVE</button></div>'
    return sec_str

def SaveToolIdling(VALUES):
    GetSAQTDA = Sql.GetFirst("SELECT CpqTableEntryId FROM SAQTDA (NOLOCK) WHERE QTEREV_RECORD_ID= '{}'".format(Quote.GetGlobal("quote_revision_record_id")))
    if GetSAQTDA:
        Sql.RunQuery("DELETE FROM SAQTDA WHERE QTEREV_RECORD_ID = '{}'".format(Quote.GetGlobal("quote_revision_record_id")))
    getQuoteDetails = Sql.GetFirst("SELECT QUOTE_ID,QUOTE_RECORD_ID, QTEREV_ID FROM SAQTRV (NOLOCK) WHERE QUOTE_REVISION_RECORD_ID = '{}'".format(Quote.GetGlobal("quote_revision_record_id")))
    if getQuoteDetails:
        QuoteId = getQuoteDetails.QUOTE_ID
        QuoteRecordId = getQuoteDetails.QUOTE_RECORD_ID
        QuoteRevisionId = getQuoteDetails.QTEREV_ID
        QuoteRevisionRecordId = Quote.GetGlobal("quote_revision_record_id")
    for x,y in VALUES.items():
        if "28 Days" in y or "30 Days" in y:
            #y = ord(y)
            a = SqlHelper.GetFirst("sp_executesql @T=N'INSERT SAQTDA( QUOTE_REV_TOOL_IDLING_ATTR_VAL_RECORD_ID, QUOTE_ID, QUOTE_RECORD_ID, QTEREV_ID, QTEREV_RECORD_ID, TOLIDLVAL_RECORD_ID, TOOLIDLING_DISPLAY_VALUE, TOOLIDLING_ID, TOOLIDLING_NAME, TOOLIDLING_RECORD_ID, TOOLIDLING_VALUE_CODE, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED ) SELECT CONVERT(VARCHAR(4000),NEWID()), ''{}'' AS QUOTE_ID, ''{}'' AS QUOTE_RECORD_ID, ''{}'' AS QTEREV_ID, ''{}'' AS QTEREV_RECORD_ID, PRTIAV.TOLIDLATTVAL_RECORD_ID, PRTIAV.TOOLIDLING_DISPLAY_VALUE, PRTIAV.TOOLIDLING_ID, PRTIAV.TOOLIDLING_NAME, PRTIAV.TOOLIDLING_RECORD_ID, PRTIAV.TOOLIDLING_VALUE_CODE, ''{}'' AS CPQTABLEENTRYADDEDBY, GETDATE() AS CPQTABLEENTRYDATEADDED FROM PRTIAV (NOLOCK) WHERE TOOLIDLING_VALUE_CODE = N''{}'' AND TOOLIDLING_ID = ''{}'' '".format(QuoteId,QuoteRecordId,QuoteRevisionId,QuoteRevisionRecordId,User.UserName,y.encode('utf-8').decode('utf-8'),x.replace("_"," ")))
        elif "Idle Notice Exception" in x.replace("_"," ") or "Idle Duration Exception" in x.replace("_"," ") or "Idling Exception Notes" in x.replace("_"," "):
            Sql.RunQuery(""" INSERT SAQTDA(
                QUOTE_REV_TOOL_IDLING_ATTR_VAL_RECORD_ID,
                QUOTE_ID,
                QUOTE_RECORD_ID,
                QTEREV_ID,
                QTEREV_RECORD_ID,
                TOLIDLVAL_RECORD_ID,
                TOOLIDLING_DISPLAY_VALUE,
                TOOLIDLING_ID,
                TOOLIDLING_NAME,
                TOOLIDLING_RECORD_ID,
                TOOLIDLING_VALUE_CODE,
                CPQTABLEENTRYADDEDBY,
                CPQTABLEENTRYDATEADDED
                ) SELECT 
                CONVERT(VARCHAR(4000),NEWID()),
                '{}' AS QUOTE_ID,
                '{}' AS QUOTE_RECORD_ID,
                '{}' AS QTEREV_ID,
                '{}' AS QTEREV_RECORD_ID,
                '',
                '{}',
                PRTIDA.TOOLIDLING_ID,
                PRTIDA.TOOLIDLING_NAME,
                PRTIDA.TOLIDLATT_RECORD_ID,
                '{}',
                '{}' AS CPQTABLEENTRYADDEDBY,
                GETDATE() AS CPQTABLEENTRYDATEADDED
                FROM PRTIDA (NOLOCK) WHERE TOOLIDLING_ID = '{}'
                """.format(QuoteId,QuoteRecordId,QuoteRevisionId,QuoteRevisionRecordId,y,y,User.UserName,x.replace("_"," ")))
        else:    
            Sql.RunQuery(""" INSERT SAQTDA(
                QUOTE_REV_TOOL_IDLING_ATTR_VAL_RECORD_ID,
                QUOTE_ID,
                QUOTE_RECORD_ID,
                QTEREV_ID,
                QTEREV_RECORD_ID,
                TOLIDLVAL_RECORD_ID,
                TOOLIDLING_DISPLAY_VALUE,
                TOOLIDLING_ID,
                TOOLIDLING_NAME,
                TOOLIDLING_RECORD_ID,
                TOOLIDLING_VALUE_CODE,
                CPQTABLEENTRYADDEDBY,
                CPQTABLEENTRYDATEADDED
                ) SELECT 
                CONVERT(VARCHAR(4000),NEWID()),
                '{}' AS QUOTE_ID,
                '{}' AS QUOTE_RECORD_ID,
                '{}' AS QTEREV_ID,
                '{}' AS QTEREV_RECORD_ID,
                PRTIAV.TOLIDLATTVAL_RECORD_ID,
                PRTIAV.TOOLIDLING_DISPLAY_VALUE,
                PRTIAV.TOOLIDLING_ID,
                PRTIAV.TOOLIDLING_NAME,
                PRTIAV.TOOLIDLING_RECORD_ID,
                PRTIAV.TOOLIDLING_VALUE_CODE,
                '{}' AS CPQTABLEENTRYADDEDBY,
                GETDATE() AS CPQTABLEENTRYDATEADDED
                FROM PRTIAV (NOLOCK) WHERE TOOLIDLING_VALUE_CODE = '{}' AND TOOLIDLING_ID = '{}'
                """.format(QuoteId,QuoteRecordId,QuoteRevisionId,QuoteRevisionRecordId,User.UserName,y,x.replace("_"," ")))
    
    GetSelf = Sql.GetFirst("SELECT CpqTableEntryId,APRTRXOBJ_ID FROM ACAPMA (NOLOCK) WHERE APRCHN_ID = 'SELFAPPR' AND APRTRXOBJ_RECORD_ID = '{}'".format(quote_revision_record_id))
    if GetSelf is not None:
        Sql.RunQuery("DELETE FROM ACAPMA WHERE APRTRXOBJ_RECORD_ID = '{}' AND APRCHN_ID = 'SELFAPPR'".format(quote_revision_record_id))
        Sql.RunQuery("DELETE FROM ACAPTX WHERE APRTRXOBJ_ID = '{}' AND APRCHN_ID = 'SELFAPPR'".format(GetSelf.APRTRXOBJ_ID))
        Sql.RunQuery("DELETE FROM ACACHR WHERE APPROVAL_ID LIKE '%{}%' AND APRCHN_ID = 'SELFAPPR'".format(GetSelf.APRTRXOBJ_ID))
    # Approval Trigger - Start								
    import ACVIORULES
    violationruleInsert = ACVIORULES.ViolationConditions()
    header_obj = Sql.GetFirst("SELECT RECORD_ID FROM SYOBJH (NOLOCK) WHERE OBJECT_NAME = 'SAQTRV'")
    if header_obj:
        violationruleInsert.InsertAction(
                                        header_obj.RECORD_ID, quote_revision_record_id, "SAQTRV"
                                        )
    # Approval Trigger - End
    return ""

def NoticeOnChange(IdleNotice):
    if IdleNotice == "Restricted Entry(Days)":
        Trace.Write("inside NoticeOnChange")
        getPRTIAV = Sql.GetFirst("SELECT TOOLIDLING_ID,TOOLIDLING_NAME FROM PRTIDA (NOLOCK) WHERE TOOLIDLING_ID = 'Idle Notice Exception'")
        x = getPRTIAV.TOOLIDLING_ID
        y = getPRTIAV.TOOLIDLING_NAME
            
        secstr = '<tr id = "notice_onchange" data-index="'+str(9)+'" class="hovergreyent" ><td style="text-align: left;"><abbr title="'+x+'">'+x+'</abbr></td><td style="text-overflow:ellipsis; overflow: hidden; max-width:1px;"><abbr title="'+y+'">'+y+'</abbr></td><td class="required_symbol" style=""><abbr class="required_symbol" title="'+x+'"> </abbr></td><td style="">'
        secstr += '<input class="form-control no_border_bg disable_edit light_yellow" id="Idle_Notice_Exception" type="number" style="color:#1B78D2" data-content="" value="" title="" onchange="" oninput="this.value|=0">'
    return secstr
def DurationOnChange(IdleDuration):
    if IdleDuration == "Restricted Entry(Days)":
        Trace.Write("inside DurationOnChange")
        getPRTIAV = Sql.GetFirst("SELECT TOOLIDLING_ID,TOOLIDLING_NAME FROM PRTIDA (NOLOCK) WHERE TOOLIDLING_ID = 'Idle Duration Exception'")
        x = getPRTIAV.TOOLIDLING_ID
        y = getPRTIAV.TOOLIDLING_NAME
            
        secstr = '<tr id = "duration_onchange" data-index="'+str(9)+'" class="hovergreyent" ><td style="text-align: left;"><abbr title="'+x+'">'+x+'</abbr></td><td style="text-overflow:ellipsis; overflow: hidden; max-width:1px;"><abbr title="'+y+'">'+y+'</abbr></td><td class="required_symbol" style=""><abbr class="required_symbol" title="'+x+'"> </abbr></td><td style="">'
        secstr += '<input class="form-control no_border_bg disable_edit light_yellow" id="Idle_Duration_Exception" type="number" style="color:#1B78D2" data-content="" value="" title="" onchange="" oninput="this.value|=0">'
    return secstr
def ExceptionOnChange(IdlingException):
    if IdlingException == "Yes":
        Trace.Write("inside ExceptionOnChange")
        getPRTIAV = Sql.GetFirst("SELECT TOOLIDLING_ID,TOOLIDLING_NAME FROM PRTIDA (NOLOCK) WHERE TOOLIDLING_ID = 'Idling Exception Notes'")
        x = getPRTIAV.TOOLIDLING_ID
        y = getPRTIAV.TOOLIDLING_NAME
            
        secstr = '<tr id = "exception_onchange" data-index="'+str(9)+'" class="hovergreyent" ><td style="text-align: left;"><abbr title="'+x+'">'+x+'</abbr></td><td style="text-overflow:ellipsis; overflow: hidden; max-width:1px;"><abbr title="'+y+'">'+y+'</abbr></td><td class="required_symbol" style=""><abbr class="required_symbol" title="'+x+'"> </abbr></td><td style="">'
        secstr += '<textarea '+'value="'+x+'"  class="form-control related_popup_css txtArea light_yellow wid_90" style="" id="'+x.replace(" ","_")+'" type="text" onchange="QuoteItemsExceptionOnChange()" data-content="'+x.replace(" ","_")+'"  title="'+x+'" maxlength = "255" rows="1" cols="100" ></textarea>'
    return secstr
def ColdOnChange(Cold):
    if Cold == "Yes":
        Trace.Write("inside Cold yes")
        getPRTIAV = Sql.GetFirst("SELECT TOOLIDLING_ID,TOOLIDLING_NAME FROM PRTIDA (NOLOCK) WHERE TOOLIDLING_ID = 'Cold Idle Fee'")
        x = getPRTIAV.TOOLIDLING_ID
        y = getPRTIAV.TOOLIDLING_NAME
        getDefaultValue = Sql.GetFirst("SELECT TOOLIDLING_VALUE_CODE FROM PRTIAV (NOLOCK) WHERE TOOLIDLING_ID = 'Cold Idle Fee' AND [DEFAULT] = 1")
        secstr = '<tr id = "cold_onchange" data-index="'+str(15)+'" class="hovergreyent" ><td style="text-align: left;"><abbr title="'+x+'">'+x+'</abbr></td><td style="text-overflow:ellipsis; overflow: hidden; max-width:1px;"><abbr title="'+y+'">'+y+'</abbr></td><td class="required_symbol" style=""><abbr class="required_symbol" title="'+x+'"> </abbr></td><td style="">'
        secstr += '<select class="form-control light_yellow" style="" id="'+x.replace(" ","_")+'" type="text"  data-content="'+x.replace(" ","_")+'"  title="'+getDefaultValue.TOOLIDLING_VALUE_CODE+'"  ><option value="select" style="display:none;"> </option><option id="'+x.replace(" ","_")+'" value="'+getDefaultValue.TOOLIDLING_VALUE_CODE+'" selected = "">'+getDefaultValue.TOOLIDLING_VALUE_CODE+'</option>'
        
        getAllValues = Sql.GetList("SELECT TOOLIDLING_VALUE_CODE FROM PRTIAV (NOLOCK) WHERE TOOLIDLING_ID = '{}' AND TOOLIDLING_VALUE_CODE != {}'{}'".format(x,"N" if "28" in getDefaultValue.TOOLIDLING_VALUE_CODE or "30" in getDefaultValue.TOOLIDLING_VALUE_CODE else "",getDefaultValue.TOOLIDLING_VALUE_CODE))
        if getAllValues:
            for val in getAllValues:
                secstr += '<option id="'+x.replace(" ","_")+'" value="'+val.TOOLIDLING_VALUE_CODE+'" >'+val.TOOLIDLING_VALUE_CODE+'</option>'
    return secstr
def HotOnChange(Hot):
    if Hot == "Yes":
        Trace.Write("inside Hot yes")
        getPRTIAV = Sql.GetFirst("SELECT TOOLIDLING_ID,TOOLIDLING_NAME FROM PRTIDA (NOLOCK) WHERE TOOLIDLING_ID = 'Warm / Hot Idle Fee'")
        x = getPRTIAV.TOOLIDLING_ID
        y = getPRTIAV.TOOLIDLING_NAME
        getDefaultValue = Sql.GetFirst("SELECT TOOLIDLING_VALUE_CODE FROM PRTIAV (NOLOCK) WHERE TOOLIDLING_ID = 'Warm / Hot Idle Fee' AND [DEFAULT] = 1")
        secstr = '<tr id = "hot_onchange" data-index="'+str(15)+'" class="hovergreyent" ><td style="text-align: left;"><abbr title="'+x+'">'+x+'</abbr></td><td style="text-overflow:ellipsis; overflow: hidden; max-width:1px;"><abbr title="'+y+'">'+y+'</abbr></td><td class="required_symbol" style=""><abbr class="required_symbol" title="'+x+'"> </abbr></td><td style="">'
        secstr += '<select class="form-control light_yellow" style="" id="'+x.replace(" ","_")+'" type="text"  data-content="'+x.replace(" ","_")+'"  title="'+getDefaultValue.TOOLIDLING_VALUE_CODE+'"  ><option value="select" style="display:none;"> </option><option id="'+x.replace(" ","_")+'" value="'+getDefaultValue.TOOLIDLING_VALUE_CODE+'" selected = "">'+getDefaultValue.TOOLIDLING_VALUE_CODE+'</option>'
        
        getAllValues = Sql.GetList("SELECT TOOLIDLING_VALUE_CODE FROM PRTIAV (NOLOCK) WHERE TOOLIDLING_ID = '{}' AND TOOLIDLING_VALUE_CODE != {}'{}'".format(x,"N" if "28" in getDefaultValue.TOOLIDLING_VALUE_CODE or "30" in getDefaultValue.TOOLIDLING_VALUE_CODE else "",getDefaultValue.TOOLIDLING_VALUE_CODE))
        if getAllValues:
            for val in getAllValues:
                secstr += '<option id="'+x.replace(" ","_")+'" value="'+val.TOOLIDLING_VALUE_CODE+'" >'+val.TOOLIDLING_VALUE_CODE+'</option>'
    return secstr


def EditItems():
    line = []
    GetLine = Sql.GetList("SELECT LINE FROM SAQRIT(NOLOCK) WHERE (BILLING_TYPE ='VARIABLE' OR BILLING_TYPE ='Variable') AND QTEREV_RECORD_ID = '{}'".format(quote_revision_record_id))
    for x in GetLine:
        line.append(str(x.LINE))
    
    return str(line)

def LoadQuoteSummary():
    sec_str = ""
    GetDetails = Sql.GetFirst("SELECT NET_VALUE_INGL_CURR,TAX_AMOUNT_INGL_CURR,ESTVAL_INGL_CURR,TOTAL_AMOUNT_INGL_CURR,CNTMRG_INGL_CURR,TOTAL_MARGIN_PERCENT FROM SAQTRV(NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(quote_record_id,quote_revision_record_id))

    values = {}
    values["Total Excluding Tax/VAT/GST"] = str(GetDetails.NET_VALUE_INGL_CURR) + " USD"
    values["Total Tax/VAT/GST"] = str(GetDetails.TAX_AMOUNT_INGL_CURR) + " USD"
    values["Total Est Net Val"] = str(GetDetails.ESTVAL_INGL_CURR) + " USD"
    values["Total Amt"] = str(GetDetails.TOTAL_AMOUNT_INGL_CURR) + " USD"
    values["Total Margin"] = str(GetDetails.CNTMRG_INGL_CURR) + " USD"
    values["Total Margin Pct"] = str(GetDetails.TOTAL_MARGIN_PERCENT) + " %"
    sec_str = """ <div onclick="dyn_main_sec_collapse_arrow(this)" data-bind="attr: {'data-toggle':'collapse','data-target':'.col'+stdAttrCode(), 
			'id':'dyn'+stdAttrCode(),'class': isWholeRow() ? 'g4 dyn_main_head master_manufac add_level glyphicon glyphicon-chevron-down pointer' : 'g1 dyn_main_head master_manufac add_level glyphicon glyphicon-chevron-down pointer'}" data-target=".sec_5802398A-50DA-40C7-8C80-99149E0C2561" id="dyn1577" data-toggle="collapse" class="g4 dyn_main_head master_manufac add_level glyphicon glyphicon-chevron-down pointer"> 
			<label data-bind="html: hint" class="onlytext"><div><div id="ctr_drop" class="btn-group dropdown"><div class="dropdown"><i data-toggle="dropdown" class="fa fa-sort-desc dropdown-toggle"></i><ul class="dropdown-menu left" aria-labelledby="dropdownMenuButton"><li class="edit_list"> <a id="5802398A-50DA-40C7-8C80-99149E0C2561" class="dropdown-item" href="#" onclick="QuoteSummaryEdit(this)">EDIT</a></li></ul></div></div>QUOTE SUMMARY</div></label> </div>"""
    for x,y in values.items():
        sec_str += '''
        <div id="sec_5802398A-50DA-40C7-8C80-99149E0C2561" class="sec_5802398A-50DA-40C7-8C80-99149E0C2561 collapse in ">
        <div style="height:30px;border-left: 0;border-right: 0;border-bottom:1px solid  #dcdcdc;" data-bind="attr: {" id ':'mat '+stdattrcode(),'class ':="" iswholerow()="" ?="" 'g4="" except_sec="" removehorline="" iconhvr '="" :="" 'g1="" } '="" id="mat1578" class="g4  except_sec removeHorLine iconhvr"><div class="col-md-5">	<abbr data-bind="attr:{" title':label} '="" title="'''+str(x)+'''"> <label class="col-md-11 pull-left" style="padding: 5px 5px;margin: 0;" data-bind="html: label, css: { requiredLabel: incomplete() &amp;&amp; $root.highlightIncomplete(), " pull-left':="" hint()="" } '="">'''+str(x)+'''</label> </abbr> <a href="#" title="" data-placement="auto top" data-toggle="popover" data-trigger="focus" data-content="'''+str(x)+'''" class="col-md-1 bgcccwth10" style="text-align:right;padding: 7px 5px;color:green;" data-original-title=""><i title="'''+str(x)+'''" class="fa fa-info-circle fltlt"></i></a> </div><div class="col-md-3 pad-0"> <input type="text" id="'''+str(x)+'''" title="'''+str(y)+'''" value="'''+str(y)+'''" 'title ':userinput},="" incrementaltabindex,="" enable:="" isenabled'="" class="form-control" style="height: 28px;border-top: 0 !important;border-bottom: 0 !important;" tabindex="" disabled=""> </div>
        <div class="col-md-3" style="display:none;"> <span class="" data-bind="attr:{" id ':="" $data.name()}'="" id="">  </span></div>
        <div class="col-md-1" style="float: right;">
            <div class="col-md-12 editiconright">
                <a href="#" onclick="editclick_row(this)" class="editclick"> <i class="fa fa-lock" aria-hidden="true"></i></a>
            </div>
        </div>
        </div>'''
    return sec_str	
try:
    SubtabName = Param.SUBTAB
except:
    SubtabName = ""
quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
quote_record_id = Quote.GetGlobal("contract_quote_record_id")
try:
    Action = Param.ACTION
except:
    Action = ""
try:
    Trace.Write("try idle notice")
    IdleNotice = str(Param.IDLENOTICE)
    Trace.Write("IDLE NOTICE="+str(IdleNotice))
except:
    Trace.Write("except idle notice")
    IdleNotice = ""
try:
    Trace.Write("try idle duration")
    IdleDuration = str(Param.IDLEDURATION)
    Trace.Write("IDLE DURATION="+str(IdleDuration))
except:
    Trace.Write("except idle duration")
    IdleDuration = ""
try:
    Trace.Write("try idling ecxxeption")
    IdlingException = str(Param.IDLINGEXCEPTION)
except:
    Trace.Write("except idling ecxxeption")
    IdlingException = ""
try:
    Trace.Write("try cold ")
    Cold = str(Param.COLD)
except:
    Trace.Write("except cold")
    Cold = ""
try:
    Trace.Write("try hot ")
    Hot = str(Param.HOT)
except:
    Trace.Write("except hot")
    Hot = ""
GetPOES = Sql.GetFirst("SELECT POES FROM SAQTMT(NOLOCK) WHERE QTEREV_RECORD_ID  = '{}' AND MASTER_TABLE_QUOTE_RECORD_ID  = '{}' ".format(quote_revision_record_id,quote_record_id))

if GetPOES:

    if SubtabName == "Summary" and (GetPOES.POES == 1):

        ApiResponse = ApiResponseFactory.JsonResponse(LoadQuoteSummary())
if Action == "NOTICE ONCHANGE" and IdleNotice == "Restricted Entry(Days)":
    Trace.Write("276")
    ApiResponse = ApiResponseFactory.JsonResponse(NoticeOnChange(IdleNotice))
if Action == "DURATION ONCHANGE" and IdleDuration == "Restricted Entry(Days)":
    Trace.Write("342")
    ApiResponse = ApiResponseFactory.JsonResponse(DurationOnChange(IdleDuration))
if Action == "EXCEPTION ONCHANGE" and IdlingException == "Yes":
    ApiResponse = ApiResponseFactory.JsonResponse(ExceptionOnChange(IdlingException))
if Action == "COLD ONCHANGE" and Cold == "Yes":
    ApiResponse = ApiResponseFactory.JsonResponse(ColdOnChange(Cold))
if Action == "HOT ONCHANGE" and Hot == "Yes":
    ApiResponse = ApiResponseFactory.JsonResponse(HotOnChange(Hot))
if SubtabName == "Summary" and Action == "VIEW" and GetPOES.POES != 1:
    ApiResponse = ApiResponseFactory.JsonResponse(LoadSummary())
elif SubtabName == "Summary" and Action == "EDIT":
    ApiResponse = ApiResponseFactory.JsonResponse(EditToolIdling())
elif SubtabName == "Summary" and Action == "SAVE":
    VALUES = dict(Param.VALUES)
    Trace.Write("values="+str(VALUES))
    ApiResponse = ApiResponseFactory.JsonResponse(SaveToolIdling(VALUES))
if SubtabName == "Items" and Action == "Edit":
    ApiResponse = ApiResponseFactory.JsonResponse(EditItems())



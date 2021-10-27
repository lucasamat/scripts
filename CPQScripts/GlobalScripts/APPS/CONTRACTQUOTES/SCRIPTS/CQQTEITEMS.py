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
        sec_str += ('<table id="63FE9099-59CD-4CF2-BC6D-DD85CB96395B" class="getentdata table table-hover" data-filter-control="true" data-maintain-selected="true" data-locale="en-US" data-escape="true" data-html="true" data-show-header="true" onmouseup="relatedmouseup(this)"> <thead><tr><th title="TOOL IDLING" style="" data-field="TOOL IDLING"><div class="th-inner sortable both">TOOL IDLING</div><div class="fht-cell"><div class="no-filter-control"></div></div></th><th title="DESCRIPTION" style="" data-field="DESCRIPTION"><div class="th-inner ">DESCRIPTION</div><div class="fht-cell"><div class="no-filter-control"></div></div></th><th title="*" class="required_symbol" style="" data-field="REQUIRED"><div class="th-inner ">*</div><div class="fht-cell"><div class="no-filter-control"></div></div></th><th title="VALUE" style="" data-field="VALUE"><div class="th-inner ">VALUE</div></tr></thead><tbody onclick="Table_Onclick_Scroll(this)"><tr data-index="0" class="hovergreyent" ><td style=""><abbr title="Idling Allowed">Idling Allowed</abbr></td><td style=""><abbr title="Option to Idle tools covered by Comprehensive Service agreements">Option to Idle tools covered by Comprehe..</abbr></td><td class="required_symbol" style=""><abbr class="required_symbol" title="Idling Allowed">*</abbr></td><td style=""><select class="form-control remove_yellow disable_edit" style="" id="IdlingAllowed" type="text" data-content="AGS_Z0091_KPI_PRPFGT" onchange="editent_bt(this)" title="'+ent_value+'" disabled=""><option value="select" style="display:none;"> </option><option id="IdlingAllowed" value="Yes" '+yes_selected+'>Yes</option><option id="IdlingAllowed" value="No" '+no_selected+'>No</option></select></td></tr>')
        ToolId = {}

        #getPRTIDA = Sql.GetFirst("SELECT TOOLIDLING_ID,TOOLIDLING_NAME FROM PRTIDA (NOLOCK)")
        getPRTIAV = Sql.GetList("SELECT TOOLIDLING_ID,TOOLIDLING_NAME,TOOLIDLING_VALUE_CODE,TOOLIDLING_DISPLAY_VALUE FROM SAQTDA (NOLOCK) WHERE QTEREV_RECORD_ID = '{}' AND TOOLIDLING_ID != 'Idling Allowed'".format(Quote.GetGlobal("quote_revision_record_id")))
        
        for x in getPRTIAV:
            ToolId[x.TOOLIDLING_ID] = x.TOOLIDLING_NAME
        i = 1
        for x,y in ToolId.items():
            
            sec_str += '<tr data-index="'+str(i)+'" class="hovergreyent" ><td style="text-align: left;"><abbr title="'+x+'">'+x+'</abbr></td><td style="text-overflow:ellipsis; overflow: hidden; max-width:1px;"><abbr title="'+y+'">'+y+'</abbr></td><td class="required_symbol" style=""><abbr class="required_symbol" title="'+x+'">*</abbr></td><td style="">'
            i = int(i)
            i += 1
            getDefaultValue = Sql.GetFirst("SELECT TOOLIDLING_VALUE_CODE FROM SAQTDA (NOLOCK) WHERE TOOLIDLING_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(x,quote_revision_record_id))
            if getDefaultValue:
                if x == "Idle Notice Exception":
                    Trace.Write("Idle Notice")
                    sec_str += '<input class="form-control no_border_bg disable_edit" style="" id="'+x.replace(" ","_")+'" type="text" onchange="QuoteItemsNoticeOnChange()" data-content="'+x.replace(" ","_")+'"  title="'+getDefaultValue.TOOLIDLING_VALUE_CODE+'" disabled = "">'
                elif x == "Idle Duration Exception":
                    Trace.Write("Idle Duration")
                    sec_str += '<input class="form-control remove_yellow disable_edit" style="" id="'+x.replace(" ","_")+'" type="text" onchange="QuoteItemsDurationOnChange()" data-content="'+x.replace(" ","_")+'"  title="'+getDefaultValue.TOOLIDLING_VALUE_CODE+'" disabled = "" >'
                elif x == "Idling Exception Notes":
                    Trace.Write("Idle Exception")
                    sec_str += '<input class="form-control remove_yellow disable_edit" style="" id="'+x.replace(" ","_")+'" type="text" onchange="QuoteItemsExceptionOnChange()" data-content="'+x.replace(" ","_")+'"  title="'+getDefaultValue.TOOLIDLING_VALUE_CODE+'" disabled = "" >'
                else:
                    Trace.Write("Idle Else")
                    sec_str += '<select class="form-control remove_yellow disable_edit" style="" id="'+x.replace(" ","_")+'" type="text"  data-content="'+x.replace(" ","_")+'"  title="'+getDefaultValue.TOOLIDLING_VALUE_CODE+'" disabled = ""><option value="select" style="display:none;"> </option><option id="'+x.replace(" ","_")+'" value="'+getDefaultValue.TOOLIDLING_VALUE_CODE+'" selected = "">'+getDefaultValue.TOOLIDLING_VALUE_CODE+'</option>'

                
                getAllValues = Sql.GetList("SELECT TOOLIDLING_VALUE_CODE FROM SAQTDA (NOLOCK) WHERE TOOLIDLING_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(x,quote_revision_record_id))
                if getAllValues:
                    for val in getAllValues:
                        sec_str += '<option id="AGS_'+val.TOOLIDLING_VALUE_CODE+'" value="'+val.TOOLIDLING_VALUE_CODE+'" >'+val.TOOLIDLING_VALUE_CODE+'</option>'
                sec_str += '</select></td></tr>'
        sec_str += "</tbody></table>"
    elif ent_value == "No":
        yes_selected = ""
        no_selected =  ' selected=""'
        sec_str += ('<table id="63FE9099-59CD-4CF2-BC6D-DD85CB96395B" class="getentdata table table-hover" data-filter-control="true" data-maintain-selected="true" data-locale="en-US" data-escape="true" data-html="true" data-show-header="true" onmouseup="relatedmouseup(this)"> <thead><tr><th title="TOOL IDLING" style="" data-field="TOOL IDLING"><div class="th-inner sortable both">TOOL IDLING</div><div class="fht-cell"><div class="no-filter-control"></div></div></th><th title="DESCRIPTION" style="" data-field="DESCRIPTION"><div class="th-inner ">DESCRIPTION</div><div class="fht-cell"><div class="no-filter-control"></div></div></th><th title="*" class="required_symbol" style="" data-field="REQUIRED"><div class="th-inner ">*</div><div class="fht-cell"><div class="no-filter-control"></div></div></th><th title="VALUE" style="" data-field="VALUE"><div class="th-inner ">VALUE</div></tr></thead><tbody onclick="Table_Onclick_Scroll(this)"><tr data-index="0" class="hovergreyent" ><td style="text-align: left;"><abbr title="Idling Allowed">Idling Allowed</abbr></td><td style=""><abbr title="Option to Idle tools covered by">Option to Idle tools covered by</abbr></td><td class="required_symbol" style=""><abbr class="required_symbol" title="Idling Allowed">*</abbr></td><td style=""><select class="form-control remove_yellow disable_edit" style="" id="Idling_Allowed" type="text" data-content="AGS_Z0091_KPI_PRPFGT" onchange="editent_bt(this)" title="'+ent_value+'" disabled=""><option value="select" style="display:none;"> </option><option id="Idling_Allowed" value="Yes" '+yes_selected+'>Yes</option><option id="Idling_Allowed" value="No" '+no_selected+'>No</option></select></td></tr></tbody></table>')
    edit_lock_icon = "fa fa-lock"
    sec_str += "</div>"
    sec_str += "</div>"
    sec_str += "</div>"
    sec_str += '<table class="wth100mrg8"><tbody>'
    sec_str += "</tbody></table></div>"
    sec_str += "</div>"
    #Trace.Write("sec_str --->"+str(sec_str))
    
    getRevisionDetails = Sql.GetFirst("SELECT GLOBAL_CURRENCY,ISNULL(TOTAL_AMOUNT_INGL_CURR,0.00) AS TOTAL_AMOUNT_INGL_CURR,ISNULL(BD_PRICE_INGL_CURR,0.00) AS BD_PRICE_INGL_CURR,ISNULL(TARGET_PRICE_INGL_CURR,0.00) AS TARGET_PRICE_INGL_CURR,ISNULL(CEILING_PRICE_INGL_CURR,0.00) AS CEILING_PRICE_INGL_CURR,ISNULL(NET_PRICE_INGL_CURR,0.00) AS NET_PRICE_INGL_CURR,ISNULL(NET_VALUE,0.00) AS NET_VALUE FROM SAQTRV (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QUOTE_REVISION_RECORD_ID = '{}'".format(quote_record_id, quote_revision_record_id))
    
    if getRevisionDetails:
        curr = str(getRevisionDetails.GLOBAL_CURRENCY)
        TotalCost = ""
        BDPrice = "{0:.2f}".format(float(getRevisionDetails.BD_PRICE_INGL_CURR))
        CeilingPrice = "{0:.2f}".format(float(getRevisionDetails.CEILING_PRICE_INGL_CURR))
        NetPrice = "{0:.2f}".format(float(getRevisionDetails.NET_PRICE_INGL_CURR))
        NetValue = "{0:.2f}".format(float(getRevisionDetails.TOTAL_AMOUNT_INGL_CURR))
        TargetPrice = "{0:.2f}".format(float(getRevisionDetails.TARGET_PRICE_INGL_CURR))
    else:
        TotalCost = 0.00
        BDPrice = 0.00
        CeilingPrice = 0.00
        TargetPrice = 0.00
        NetPrice = 0.00
        NetValue = 0.00
    return sec_str,str(TotalCost),str(BDPrice)+ " " +curr,str(CeilingPrice)+ " " +curr,str(TargetPrice)+ " " +curr,str(NetPrice)+ " " +curr,str(NetValue)+ " " +curr

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
        sec_str += ('<table id="63FE9099-59CD-4CF2-BC6D-DD85CB96395B" class="getentdata table table-hover" data-filter-control="true" data-maintain-selected="true" data-locale="en-US" data-escape="true" data-html="true" data-show-header="true" onmouseup="relatedmouseup(this)"> <thead><tr><th title="TOOL IDLING" style="" data-field="TOOL IDLING"><div class="th-inner sortable both">TOOL IDLING</div><div class="fht-cell"><div class="no-filter-control"></div></div></th><th title="DESCRIPTION" style="" data-field="DESCRIPTION"><div class="th-inner ">DESCRIPTION</div><div class="fht-cell"><div class="no-filter-control"></div></div></th><th title="*" class="required_symbol" style="" data-field="REQUIRED"><div class="th-inner ">*</div><div class="fht-cell"><div class="no-filter-control"></div></div></th><th title="VALUE" style="" data-field="VALUE"><div class="th-inner ">VALUE</div></tr></thead><tbody onclick="Table_Onclick_Scroll(this)"><tr data-index="0" class="hovergreyent" ><td style=""><abbr title="Idling Allowed">Idling Allowed</abbr></td><td style=""><abbr title="Option to Idle tools covered by Comprehensive Service agreements">Option to Idle tools covered by Comprehen..</abbr></td><td class="required_symbol" style=""><abbr class="required_symbol" title="Idling Allowed">*</abbr></td><td style=""><select class="form-control remove_yellow disable_edit" style="" id="Idling_Allowed" type="text" data-content="AGS_Z0091_KPI_PRPFGT" onchange="QuoteItemsIdlingOnChange()" title="'+ent_value+'" disabled ="" ><option value="select" style="display:none;"> </option><option id="Idling_Allowed" value="Yes" '+yes_selected+'>Yes</option><option id="Idling_Allowed" value="No" '+no_selected+'>No</option></select></td></tr>')
        getValueSAQTDA = Sql.GetFirst("SELECT TOOLIDLING_DISPLAY_VALUE FROM SAQTDA(NOLOCK) WHERE TOOLIDLING_ID = 'Idling Allowed' AND QTEREV_RECORD_ID = '{}'".format(Quote.GetGlobal("quote_revision_record_id")))
        if getValueSAQTDA is not None:
            #getPRTIDA = Sql.GetFirst("SELECT TOOLIDLING_ID,TOOLIDLING_NAME FROM PRTIDA (NOLOCK)")
            getPRTIAV = Sql.GetList("SELECT TOOLIDLING_ID,TOOLIDLING_NAME,TOOLIDLING_VALUE_CODE,TOOLIDLING_DISPLAY_VALUE FROM SAQTDA (NOLOCK) WHERE QTEREV_RECORD_ID = '{}' AND TOOLIDLING_ID != 'Idling Allowed'".format(Quote.GetGlobal("quote_revision_record_id")))
            
            for x in getPRTIAV:
                ToolId[x.TOOLIDLING_ID] = x.TOOLIDLING_NAME
            i = 1
            for x,y in ToolId.items():
                
                sec_str += '<tr data-index="'+str(i)+'" class="hovergreyent" ><td style="text-align: left;"><abbr title="'+x+'">'+x+'</abbr></td><td style="text-overflow:ellipsis; overflow: hidden; max-width:1px;"><abbr title="'+y+'">'+y+'</abbr></td><td class="required_symbol" style=""><abbr class="required_symbol" title="'+x+'">*</abbr></td><td style="">'
                i = int(i)
                i += 1
                getDefaultValue = Sql.GetFirst("SELECT TOOLIDLING_VALUE_CODE FROM SAQTDA (NOLOCK) WHERE TOOLIDLING_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(x,quote_revision_record_id))
                if getDefaultValue:
                    if x == "Idle Notice Exception":
                        Trace.Write("Idle Notice")
                        sec_str += '<input class="form-control light_yellow" style="" id="'+x.replace(" ","_")+'" type="text" onchange="QuoteItemsNoticeOnChange()" data-content="'+x.replace(" ","_")+'"  title="'+getDefaultValue.TOOLIDLING_VALUE_CODE+'" >'
                    elif x == "Idle Duration Exception":
                        Trace.Write("Idle Duration")
                        sec_str += '<input class="form-control light_yellow" style="" id="'+x.replace(" ","_")+'" type="text" onchange="QuoteItemsDurationOnChange()" data-content="'+x.replace(" ","_")+'"  title="'+getDefaultValue.TOOLIDLING_VALUE_CODE+'" >'
                    elif x == "Idling Exception Notes":
                        Trace.Write("Idle Exception")
                        sec_str += '<input class="form-control light_yellow" style="" id="'+x.replace(" ","_")+'" type="text" onchange="QuoteItemsExceptionOnChange()" data-content="'+x.replace(" ","_")+'"  title="'+getDefaultValue.TOOLIDLING_VALUE_CODE+'" >'
                    else:
                        Trace.Write("Idle Else")
                        sec_str += '<select class="form-control light_yellow" style="" id="'+x.replace(" ","_")+'" type="text"  data-content="'+x.replace(" ","_")+'"  title="'+getDefaultValue.TOOLIDLING_VALUE_CODE+'" ><option value="select" style="display:none;"> </option><option id="'+x.replace(" ","_")+'" value="'+getDefaultValue.TOOLIDLING_VALUE_CODE+'" selected = "">'+getDefaultValue.TOOLIDLING_VALUE_CODE+'</option>'

                    
                    getAllValues = Sql.GetList("SELECT TOOLIDLING_VALUE_CODE FROM PRTIAV (NOLOCK) WHERE TOOLIDLING_ID = '{}' AND TOOLIDLING_VALUE_CODE != {}'{}'".format(x,"N" if "28" in getDefaultValue.TOOLIDLING_VALUE_CODE or "30" in getDefaultValue.TOOLIDLING_VALUE_CODE else "",getDefaultValue.TOOLIDLING_VALUE_CODE))
                    if getAllValues:
                        for val in getAllValues:
                            sec_str += '<option id="'+x.replace(" ","_")+'" value="'+val.TOOLIDLING_VALUE_CODE+'" >'+val.TOOLIDLING_VALUE_CODE+'</option>'
                    sec_str += '</select></td></tr>'
            sec_str += "</tbody></table>"
        else:
            #getPRTIDA = Sql.GetFirst("SELECT TOOLIDLING_ID,TOOLIDLING_NAME FROM PRTIDA (NOLOCK)")
            getPRTIAV = Sql.GetList("SELECT TOOLIDLING_ID,TOOLIDLING_NAME,TOOLIDLING_VALUE_CODE,TOOLIDLING_DISPLAY_VALUE FROM PRTIAV (NOLOCK) WHERE TOOLIDLING_ID != 'Idling Allowed'")
            
            for x in getPRTIAV:
                ToolId[x.TOOLIDLING_ID] = x.TOOLIDLING_NAME
            i = 1
            for x,y in ToolId.items():
                
                sec_str += '<tr data-index="'+str(i)+'" class="hovergreyent" ><td style="text-align: left;"><abbr title="'+x+'">'+x+'</abbr></td><td style="text-overflow:ellipsis; overflow: hidden; max-width:1px;"><abbr title="'+y+'">'+y+'</abbr></td><td class="required_symbol" style=""><abbr class="required_symbol" title="'+x+'">*</abbr></td><td style="">'
                i = int(i)
                i += 1
                getDefaultValue = Sql.GetFirst("SELECT TOOLIDLING_VALUE_CODE FROM PRTIAV (NOLOCK) WHERE TOOLIDLING_ID = '{}'".format(x))
                if getDefaultValue:
                    sec_str += '<select class="form-control light_yellow" style="" id="'+x.replace(" ","_")+'" type="text" data-content="AGS_'+x.strip()+'"  title="'+getDefaultValue.TOOLIDLING_VALUE_CODE+'" ><option value="select" style="display:none;"> </option><option id="'+x.replace(" ","_")+'" value="'+getDefaultValue.TOOLIDLING_VALUE_CODE+'" selected = "">'+getDefaultValue.TOOLIDLING_VALUE_CODE+'</option>'
                    
                    getAllValues = Sql.GetList("SELECT TOOLIDLING_VALUE_CODE FROM PRTIAV (NOLOCK) WHERE TOOLIDLING_ID = '{}' AND [DEFAULT] = 0".format(x))
                    if getAllValues:
                        for val in getAllValues:
                            sec_str += '<option id="'+x.replace(" ","_")+'" value="'+str(val.TOOLIDLING_VALUE_CODE)+'" >'+str(val.TOOLIDLING_VALUE_CODE)+'</option>'
                    sec_str += '</select></td></tr>'
            sec_str += "</tbody></table>"
    else:
        sec_str += ('<table id="63FE9099-59CD-4CF2-BC6D-DD85CB96395B" class="getentdata table table-hover" data-filter-control="true" data-maintain-selected="true" data-locale="en-US" data-escape="true" data-html="true" data-show-header="true" onmouseup="relatedmouseup(this)"> <thead><tr><th title="TOOL IDLING" style="" data-field="TOOL IDLING"><div class="th-inner sortable both">TOOL IDLING</div><div class="fht-cell"><div class="no-filter-control"></div></div></th><th title="DESCRIPTION" style="" data-field="DESCRIPTION"><div class="th-inner ">DESCRIPTION</div><div class="fht-cell"><div class="no-filter-control"></div></div></th><th title="*" class="required_symbol" style="" data-field="REQUIRED"><div class="th-inner ">*</div><div class="fht-cell"><div class="no-filter-control"></div></div></th><th title="VALUE" style="" data-field="VALUE"><div class="th-inner ">VALUE</div></tr></thead><tbody onclick="Table_Onclick_Scroll(this)"><tr data-index="0" class="hovergreyent" ><td style="text-align: left;"><abbr title="Idling Allowed">Idling Allowed</abbr></td><td style=""><abbr title="Option to Idle tools covered by">Option to Idle tools covered by</abbr></td><td class="required_symbol" style=""><abbr class="required_symbol" title="Idling Allowed">*</abbr></td><td style=""><select class="form-control light_yellow" style="" id="Idling_Allowed" type="text" data-content="AGS_Z0091_KPI_PRPFGT" onchange="QuoteItemsIdlingOnChange()" title="'+ent_value+'" ><option value="select" style="display:none;"> </option><option id="Idling_Allowed" value="Yes" '+yes_selected+'>Yes</option><option id="Idling_Allowed" value="No" '+no_selected+'>No</option></select></td></tr></tbody></table>')


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
    return ""

def NoticeOnChange(IdleNotice):
    if IdleNotice == "Restricted Entry(Days)":
        Trace.Write("inside NoticeOnChange")
        getPRTIAV = Sql.GetFirst("SELECT TOOLIDLING_ID,TOOLIDLING_NAME FROM PRTIDA (NOLOCK) WHERE TOOLIDLING_ID = 'Idle Notice Exception'")
        x = getPRTIAV.TOOLIDLING_ID
        y = getPRTIAV.TOOLIDLING_NAME
            
        secstr = '<tr id = "notice_onchange" data-index="'+str(9)+'" class="hovergreyent" ><td style="text-align: left;"><abbr title="'+x+'">'+x+'</abbr></td><td style="text-overflow:ellipsis; overflow: hidden; max-width:1px;"><abbr title="'+y+'">'+y+'</abbr></td><td class="required_symbol" style=""><abbr class="required_symbol" title="'+x+'">*</abbr></td><td style="">'
        secstr += '<input class="form-control no_border_bg disable_edit light_yellow" id="Idle_Notice_Exception" type="text" style="color:#1B78D2" data-content="" value="" title="" onchange="">'
    return secstr
def DurationOnChange(IdleDuration):
    if IdleDuration == "Restricted Entry(Days)":
        Trace.Write("inside DurationOnChange")
        getPRTIAV = Sql.GetFirst("SELECT TOOLIDLING_ID,TOOLIDLING_NAME FROM PRTIDA (NOLOCK) WHERE TOOLIDLING_ID = 'Idle Duration Exception'")
        x = getPRTIAV.TOOLIDLING_ID
        y = getPRTIAV.TOOLIDLING_NAME
            
        secstr = '<tr id = "duration_onchange" data-index="'+str(9)+'" class="hovergreyent" ><td style="text-align: left;"><abbr title="'+x+'">'+x+'</abbr></td><td style="text-overflow:ellipsis; overflow: hidden; max-width:1px;"><abbr title="'+y+'">'+y+'</abbr></td><td class="required_symbol" style=""><abbr class="required_symbol" title="'+x+'">*</abbr></td><td style="">'
        secstr += '<input class="form-control no_border_bg disable_edit light_yellow" id="Idle_Duration_Exception" type="text" style="color:#1B78D2" data-content="" value="" title="" onchange="">'
    return secstr
def ExceptionOnChange(IdlingException):
    if IdlingException == "Yes":
        Trace.Write("inside ExceptionOnChange")
        getPRTIAV = Sql.GetFirst("SELECT TOOLIDLING_ID,TOOLIDLING_NAME FROM PRTIDA (NOLOCK) WHERE TOOLIDLING_ID = 'Idling Exception Notes'")
        x = getPRTIAV.TOOLIDLING_ID
        y = getPRTIAV.TOOLIDLING_NAME
            
        secstr = '<tr id = "exception_onchange" data-index="'+str(9)+'" class="hovergreyent" ><td style="text-align: left;"><abbr title="'+x+'">'+x+'</abbr></td><td style="text-overflow:ellipsis; overflow: hidden; max-width:1px;"><abbr title="'+y+'">'+y+'</abbr></td><td class="required_symbol" style=""><abbr class="required_symbol" title="'+x+'">*</abbr></td><td style="">'
        secstr += '<input class="form-control no_border_bg disable_edit light_yellow" id="Idling_Exception_Notes" type="text" style="color:#1B78D2" data-content="" value="" title="" onchange="">'
    return secstr
SubtabName = Param.SUBTAB
quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")

Action = Param.ACTION
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
if Action == "NOTICE ONCHANGE" and IdleNotice == "Restricted Entry(Days)":
    Trace.Write("276")
    ApiResponse = ApiResponseFactory.JsonResponse(NoticeOnChange(IdleNotice))
if Action == "DURATION ONCHANGE" and IdleDuration == "Restricted Entry(Days)":
    ApiResponse = ApiResponseFactory.JsonResponse(DurationOnChange(IdleDuration))
if Action == " EXCEPTION ONCHANGE" and IdlingException == "Yes":
    ApiResponse = ApiResponseFactory.JsonResponse(ExceptionOnChange(IdlingException))
if SubtabName == "Summary" and Action == "VIEW":
    ApiResponse = ApiResponseFactory.JsonResponse(LoadSummary())
elif SubtabName == "Summary" and Action == "EDIT":
    ApiResponse = ApiResponseFactory.JsonResponse(EditToolIdling())
elif SubtabName == "Summary" and Action == "SAVE":
    VALUES = dict(Param.VALUES)
    Trace.Write("values="+str(VALUES))
    ApiResponse = ApiResponseFactory.JsonResponse(SaveToolIdling(VALUES))


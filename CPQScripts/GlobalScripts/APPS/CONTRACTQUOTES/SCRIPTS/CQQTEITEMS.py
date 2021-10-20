# =========================================================================================================================================
#   __script_name : CQQTEITEMS.PY
#   __script_description : THIS SCRIPT IS USED TO LOAD SUMMARY IN QUOTE ITEMS
#   __primary_author__ : NAMRATA SIVAKUMAR
#   __create_date : 12/10/2021
#   Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import re
import SYTABACTIN as Table
import SYCNGEGUID as CPQID
from SYDATABASE import SQL
Sql = SQL()

def LoadSummary():
    where = " QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(quote_record_id,quote_revision_record_id)
    ObjectName = "SAQSCE"
    getinnercon  = Sql.GetFirst("select QUOTE_RECORD_ID,QTEREV_RECORD_ID,convert(xml,replace(replace(replace(replace(replace(replace(ENTITLEMENT_XML,'&',';#38'),'''',';#39'),' < ',' &lt; ' ),' > ',' &gt; ' ),'_>','_&gt;'),'_<','_&lt;')) as ENTITLEMENT_XML from "+str(ObjectName)+" (nolock)  where  "+str(where)+"")
    if getinnercon:
        GetXMLsecField = Sql.GetList("SELECT distinct e.QUOTE_RECORD_ID,e.QTEREV_RECORD_ID, replace(X.Y.value('(ENTITLEMENT_NAME)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_NAME,replace(X.Y.value('(ENTITLEMENT_ID)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_ID,replace(X.Y.value('(IS_DEFAULT)[1]', 'VARCHAR(128)'),';#38','&') as IS_DEFAULT,replace(X.Y.value('(ENTITLEMENT_COST_IMPACT)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_COST_IMPACT,replace(X.Y.value('(CALCULATION_FACTOR)[1]', 'VARCHAR(128)'),';#38','&') as CALCULATION_FACTOR,replace(X.Y.value('(ENTITLEMENT_PRICE_IMPACT)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_PRICE_IMPACT,replace(X.Y.value('(ENTITLEMENT_TYPE)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_TYPE,replace(X.Y.value('(ENTITLEMENT_VALUE_CODE)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_VALUE_CODE,replace(replace(replace(replace(X.Y.value('(ENTITLEMENT_DESCRIPTION)[1]', 'VARCHAR(128)'),';#38','&'),';#39',''''),'&lt;','<' ),'&gt;','>') as ENTITLEMENT_DESCRIPTION,replace(replace(replace(replace(X.Y.value('(ENTITLEMENT_DISPLAY_VALUE)[1]', 'VARCHAR(128)'),';#38','&'),';#39',''''),'_&lt;','_<' ),'_&gt;','_>') as ENTITLEMENT_DISPLAY_VALUE,replace(X.Y.value('(PRICE_METHOD)[1]', 'VARCHAR(128)'),';#38','&') as PRICE_METHOD FROM (select '"+str(getinnercon.QUOTE_RECORD_ID)+"' as QUOTE_RECORD_ID,'"+str(getinnercon.QTEREV_RECORD_ID)+"' as QTEREV_RECORD_ID,convert(xml,'"+str(getinnercon.ENTITLEMENT_XML)+"') as ENTITLEMENT_XML ) e OUTER APPLY e.ENTITLEMENT_XML.nodes('QUOTE_ITEM_ENTITLEMENT') as X(Y) ")
        for value in GetXMLsecField:
        
            get_name = value.ENTITLEMENT_ID
            #Trace.Write("VALUE IN XML--------->"+str(get_name))
            get_value = value.ENTITLEMENT_DISPLAY_VALUE
            get_cost_impact = value.ENTITLEMENT_COST_IMPACT
            get_price_impact = value.ENTITLEMENT_PRICE_IMPACT
            get_curr = value.PRICE_METHOD
            if 'AGS_Z0091_GEN_IDLALW' in get_name:
                ent_value = get_value
                if ent_value == "Yes":
                    break
    else:
        ent_value = "No"


    sec_str = ""
    Quote.SetGlobal("IdlingAllowed",ent_value)
    if ent_value == "Yes":
        yes_selected = ' selected=""'
        no_selected = ""
    elif ent_value == "No":
        yes_selected = ""
        no_selected =  ' selected=""'
    sec_str += ('<table id="63FE9099-59CD-4CF2-BC6D-DD85CB96395B" class="getentdata table table-hover" data-filter-control="true" data-maintain-selected="true" data-locale="en-US" data-escape="true" data-html="true" data-show-header="true" onmouseup="relatedmouseup(this)"> <thead><tr><th title="TOOL IDLING" style="" data-field="TOOL IDLING"><div class="th-inner sortable both">TOOL IDLING</div><div class="fht-cell"><div class="no-filter-control"></div></div></th><th title="DESCRIPTION" style="" data-field="DESCRIPTION"><div class="th-inner ">DESCRIPTION</div><div class="fht-cell"><div class="no-filter-control"></div></div></th><th title="*" class="required_symbol" style="" data-field="REQUIRED"><div class="th-inner ">*</div><div class="fht-cell"><div class="no-filter-control"></div></div></th><th title="VALUE" style="" data-field="VALUE"><div class="th-inner ">VALUE</div></tr></thead><tbody onclick="Table_Onclick_Scroll(this)"><tr data-index="0" class="hovergreyent" ><td style="text-align: left;"><abbr title="Idling Allowed">Idling Allowed</abbr></td><td style=""><abbr title="Option to Idle tools covered by">Option to Idle tools covered by</abbr></td><td class="required_symbol" style=""><abbr class="required_symbol" title="Idling Allowed">*</abbr></td><td style=""><select class="form-control remove_yellow disable_edit" style="" id="AGS_Z0091_KPI_PRPFGT" type="text" data-content="AGS_Z0091_KPI_PRPFGT" onchange="editent_bt(this)" title="'+ent_value+'" disabled=""><option value="select" style="display:none;"> </option><option id="AGS_Z0091_GEN_IDLALW_001" value="Yes" '+yes_selected+'>Yes</option><option id="AGS_Z0091_GEN_IDLALW_002" value="No" '+no_selected+'>No</option></select></td></tr></tbody></table>')
    edit_lock_icon = "fa fa-lock"
    sec_str += "</div>"
    sec_str += "</div>"
    sec_str += "</div>"
    sec_str += '<table class="wth100mrg8"><tbody>'
    sec_str += "</tbody></table></div>"
    sec_str += "</div>"
    Trace.Write("sec_str --->"+str(sec_str))
    
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
    return str(sec_str),str(TotalCost),str(BDPrice)+ " " +curr,str(CeilingPrice)+ " " +curr,str(TargetPrice)+ " " +curr,str(NetPrice)+ " " +curr,str(NetValue)+ " " +curr

quote_record_id = Quote.GetGlobal("contract_quote_record_id")
quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")

def EditToolIdling(option):
    if option == "Yes":
        ent_value = Quote.GetGlobal("IdlingAllowed")
        if ent_value == "Yes":
            yes_selected = ' selected=""'
            no_selected = ""
        elif ent_value == "No":
            yes_selected = ""
            no_selected =  ' selected=""'
        ToolId = {}

        #getPRTIDA = Sql.GetFirst("SELECT TOOLIDLING_ID,TOOLIDLING_NAME FROM PRTIDA (NOLOCK)")
        getPRTIAV = Sql.GetList("SELECT TOOLIDLING_ID,TOOLIDLING_NAME,TOOLIDLING_VALUE_CODE,TOOLIDLING_DISPLAY_VALUE FROM PRTIAV (NOLOCK)")
        
        for x in getPRTIAV:
            ToolId[x.TOOLIDLING_ID] = x.TOOLIDLING_NAME

        secstr = '<table id="63FE9099-59CD-4CF2-BC6D-DD85CB96395B" class="getentdata table table-hover" data-filter-control="true" data-maintain-selected="true" data-locale="en-US" data-escape="true" data-html="true" data-show-header="true" onmouseup="relatedmouseup(this)"> <thead><tr><th title="TOOL IDLING" style="" data-field="TOOL IDLING"><div class="th-inner sortable both">TOOL IDLING</div><div class="fht-cell"><div class="no-filter-control"></div></div></th><th title="DESCRIPTION" style="width: 16.66%" data-field="DESCRIPTION"><div class="th-inner ">DESCRIPTION</div><div class="fht-cell"><div class="no-filter-control"></div></div></th><th title="*" class="required_symbol" style="" data-field="REQUIRED"><div class="th-inner ">*</div><div class="fht-cell"><div class="no-filter-control"></div></div></th><th title="VALUE" style="" data-field="VALUE"><div class="th-inner ">VALUE</div></tr></thead><tbody onclick="Table_Onclick_Scroll(this)"><tr data-index="0" class="hovergreyent" >'

        secstr += '<td style="text-align: left;"><abbr title="Idling Allowed">Idling Allowed</abbr></td><td style=""><abbr title="Option to Idle tools covered by">Option to Idle tools covered by</abbr></td><td class="required_symbol" style=""><abbr class="required_symbol" title="Idling Allowed">*</abbr></td><td style=""><select class="form-control remove_yellow disable_edit" style="" id="AGS_Z0091_KPI_PRPFGT" type="text" data-content="AGS_Z0091_KPI_PRPFGT" onchange="editent_bt(this)" title="'+ent_value+'" disabled=""><option value="select" style="display:none;"> </option><option id="AGS_Z0091_GEN_IDLALW_001" value="Yes" '+yes_selected+'>Yes</option><option id="AGS_Z0091_GEN_IDLALW_002" value="No" '+no_selected+'>No</option></select></td>'
        i = 1
        for x,y in ToolId.items():
            
            secstr += '<tr data-index="'+str(i)+'" class="hovergreyent" ><td style="text-align: left;"><abbr title="'+x+'">'+x+'</abbr></td><td style="text-overflow:ellipsis; overflow: hidden; max-width:1px;"><abbr title="'+y+'">'+y+'</abbr></td><td class="required_symbol" style=""><abbr class="required_symbol" title="'+x+'">*</abbr></td><td style="">'
            i = int(i)
            i += 1
            getDefaultValue = Sql.GetFirst("SELECT TOOLIDLING_VALUE_CODE FROM PRTIAV (NOLOCK) WHERE TOOLIDLING_ID = '{}' AND [DEFAULT] = 1".format(x))
            if getDefaultValue:
                secstr += '<select class="form-control light_yellow" style="" id="AGS_Z0091_KPI_PRPFGT" type="text" data-content="AGS_'+x.strip()+'"  title="'+getDefaultValue.TOOLIDLING_VALUE_CODE+'" ><option value="select" style="display:none;"> </option><option id="AGS_'+getDefaultValue.TOOLIDLING_VALUE_CODE+'" value="'+getDefaultValue.TOOLIDLING_VALUE_CODE+'" selected = "">'+getDefaultValue.TOOLIDLING_VALUE_CODE+'</option>'
                
                getAllValues = Sql.GetList("SELECT TOOLIDLING_VALUE_CODE FROM PRTIAV (NOLOCK) WHERE TOOLIDLING_ID = '{}' AND [DEFAULT] = 0".format(x))
                if getAllValues:
                    for val in getAllValues:
                        secstr += '<option id="AGS_'+str(val.TOOLIDLING_VALUE_CODE)+'" value="'+str(val.TOOLIDLING_VALUE_CODE)+'" >'+str(val.TOOLIDLING_VALUE_CODE)+'</option>'
                secstr += '</select></td></tr>'
        secstr += "</tbody></table>"
        secstr += '<div id="quotesummarysavecancel" class="col-md-12 text-center"><button id="hidesavecancel" class="btnconfig btnMainBanner sec_edit_sty_btn flt_none" onclick="">CANCEL</button><button id="hidesavecancel" class="btnconfig btnMainBanner sec_edit_sty_btn flt_none" onclick="QuoteItemsIdlingSave()">SAVE</button></div>'
    return secstr
SubtabName = Param.SUBTAB

Action = Param.ACTION
if Action == "EDIT":
    option = Param.OPTION
if SubtabName == "Summary" and Action == "VIEW":
    ApiResponse = ApiResponseFactory.JsonResponse(LoadSummary())
elif SubtabName == "Summary" and Action == "EDIT":
    ApiResponse = ApiResponseFactory.JsonResponse(EditToolIdling(option))

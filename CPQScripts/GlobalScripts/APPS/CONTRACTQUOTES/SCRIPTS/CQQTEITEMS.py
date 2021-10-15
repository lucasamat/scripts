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
    sec_str = ""
    sec_str += ('<table id="63FE9099-59CD-4CF2-BC6D-DD85CB96395B" class="getentdata table table-hover" data-filter-control="true" data-maintain-selected="true" data-locale="en-US" data-escape="true" data-html="true" data-show-header="true" onmouseup="relatedmouseup(this)"> <thead><tr><th title="TOOL IDLING" style="" data-field="TOOL IDLING"><div class="th-inner ">TOOL IDLING</div><div class="fht-cell"><div class="no-filter-control"></div></div></th><th title="DESCRIPTION" style="" data-field="DESCRIPTION"><div class="th-inner ">DESCRIPTION</div><div class="fht-cell"><div class="no-filter-control"></div></div></th><th title="*" class="required_symbol" style="" data-field="REQUIRED"><div class="th-inner ">*</div><div class="fht-cell"><div class="no-filter-control"></div></div></th><th title="VALUE" style="" data-field="VALUE"><div class="th-inner ">VALUE</div></tr></thead><tbody onclick="Table_Onclick_Scroll(this)"><tr data-index="0" class="hovergreyent" ><td style="text-align: left;"><abbr title="Idling Allowed">Idling Allowed</abbr></td><td style=""><abbr title="Option to Idle tools covered by">Option to Idle tools covered by</abbr></td><td class="required_symbol" style=""></td><td style=""><select class="form-control remove_yellow disable_edit" style="" id="AGS_Z0091_KPI_PRPFGT" type="text" data-content="AGS_Z0091_KPI_PRPFGT" onchange="editent_bt(this)" title="Yes" disabled=""><option value="select" style="display:none;"> </option><option id="AGS_Z0091_KPI_PRPFGT_001" value="Supplier Dependent Uptime" selected="">Yes</option><option id="AGS_Z0091_KPI_PRPFGT_002" value="Std Srvcs</option></select></td></tr></tbody></table>'
    )
    edit_lock_icon = "fa fa-lock"
    sec_str += "</div>"
    sec_str += "</div>"
    sec_str += "</div>"
    sec_str += '<table class="wth100mrg8"><tbody>'
    sec_str += "</tbody></table></div>"
    sec_str += "</div>"
    Trace.Write("sec_str --->"+str(sec_str))
    getRevisionDetails = Sql.GetFirst("SELECT ISNULL(TOTAL_AMOUNT_INGL_CURR,0) AS TOTAL_AMOUNT_INGL_CURR,BD_PRICE_INGL_CURR,TARGET_PRICE_INGL_CURR,CEILING_PRICE_INGL_CURR,NET_PRICE_INGL_CURR,NET_VALUE FROM SAQTRV (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QUOTE_REVISION_RECORD_ID = '{}'".format(quote_record_id, quote_revision_record_id))
    if getRevisionDetails:
        TotalCost = getRevisionDetails.TOTAL_AMOUNT_INGL_CURR
    
    return str(sec_str),TotalCost,BDPrice,CeilingPrice,TargetPrice,NetPrice,NetValue

SubtabName = Param.SUBTAB
if SubtabName == "Summary":
    ApiResponse = ApiResponseFactory.JsonResponse(LoadSummary())


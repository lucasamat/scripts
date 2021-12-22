



import clr
#clr.AddReference("System.Net")
clr.AddReference("IronPython")
clr.AddReference("Microsoft.Scripting")
from System.Net import WebRequest
from System.Net import HttpWebResponse
from Microsoft.Scripting import SourceCodeKind
from IronPython.Hosting import Python
from IronPython import Compiler
import Webcom.Configurator.Scripting.Test.TestProduct

from SYDATABASE import SQL
import datetime
Sql = SQL()
import SYCNGEGUID as CPQID

UserId = str(User.Id)
UserName = str(User.UserName)
INCLUDESPARE =add_style =  ""

quoteid = Product.GetGlobal("contract_quote_record_id")
contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
get_spare=Sql.GetFirst("select * from QTQIFP where QUOTE_RECORD_ID='"+str(quoteid)+"'")
gettoolquote=Sql.GetFirst("select QUOTE_TYPE,QUOTE_ID from SAQTMT where MASTER_TABLE_QUOTE_RECORD_ID='"+str(contract_quote_record_id)+"'")
if get_spare and gettoolquote.QUOTE_TYPE =="ZTBC - TOOL BASED":
	INCLUDESPARE = 'INCLUDESPARES'
	add_style = "display:block"
else:
	Trace.Write('succes--NO--')
	INCLUDESPARE = ''
	add_style = "display:none"



get_quote_details = Sql.GetFirst("SELECT QUOTE_ID,QTEREV_ID,QUOTE_NAME,C4C_QUOTE_ID, QUOTE_TYPE FROM SAQTMT(NOLOCK) WHERE MASTER_TABLE_QUOTE_RECORD_ID =  '"+str(contract_quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id) + "'")
#Quote=QuoteHelper.Edit(get_quote_details.C4C_QUOTE_ID)
saqdoc_output_insert="""INSERT SAQDOC (
                    QUOTE_DOCUMENT_RECORD_ID,
                    DOCUMENT_ID,
                    DOCUMENT_NAME,
                    DOCUMENT_PATH,
                    QUOTE_ID,
                    QUOTE_NAME,
                    QUOTE_RECORD_ID,
                    LANGUAGE_ID,
                    LANGUAGE_NAME,
                    LANGUAGE_RECORD_ID,
                    CPQTABLEENTRYADDEDBY,
                    CPQTABLEENTRYDATEADDED,
                    CpqTableEntryModifiedBy,
                    CpqTableEntryDateModified,
                    STATUS,
                    QTEREV_ID,
                    QTEREV_RECORD_ID
                    )SELECT
                    CONVERT(VARCHAR(4000),NEWID()) as QUOTE_DOCUMENT_RECORD_ID,
                    'Pending' AS DOCUMENT_ID,
                    '' AS DOCUMENT_NAME,
                    '' AS DOCUMENT_PATH,
                    '{quoteid}' AS QUOTE_ID,
                    '{quotename}' AS QUOTE_NAME,
                    '{quoterecid}' AS QUOTE_RECORD_ID,
                    'EN' AS LANGUAGE_ID,
                    'English' AS LANGUAGE_NAME,
                    MALANG.LANGUAGE_RECORD_ID AS LANGUAGE_RECORD_ID,
                    '{UserName}' as CPQTABLEENTRYADDEDBY,
                    '{dateadded}' as CPQTABLEENTRYDATEADDED,
                    '{UserId}' as CpqTableEntryModifiedBy,
                    '{date}' as CpqTableEntryDateModified,
                    'PENDING' as STATUS,
                    '{qt_revid}' as QTEREV_ID,
                    '{qt_rev_rec_id}' as QTEREV_RECORD_ID
                    FROM MALANG (NOLOCK) WHERE MALANG.LANGUAGE_NAME = 'English'""".format(quoteid=get_quote_details.QUOTE_ID,quotename=get_quote_details.QUOTE_NAME,quoterecid=contract_quote_record_id,qt_revid= get_quote_details.QTEREV_ID,qt_rev_rec_id = quote_revision_record_id,UserName=UserName,dateadded=datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"),UserId=UserId,date=datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"))
#Log.Info(qtqdoc)
Sql.RunQuery(saqdoc_output_insert)
_insert_subtotal_by_offerring_quote_table()


#Document XML
def _insert_subtotal_by_offerring_quote_table():
	c4c_quote_id = gettoolquote.QUOTE_ID
	cartobj = Sql.GetFirst("select CART_ID, USERID from CART where ExternalId = '{}'".format(c4c_quote_id))
	insrt_subtotal_offering = ("""INSERT QT__QT_SAQRIS (COMMITTED_VALUE,CONTRACT_VALID_FROM,CONTRACT_VALID_TO,DIVISION_ID,DIVISION_RECORD_ID,DOC_CURRENCY,DOCCURR_RECORD_ID,ESTIMATED_VALUE,GLOBAL_CURRENCY,GLOBAL_CURRENCY_RECORD_ID,LINE,NET_PRICE,NET_PRICE_INGL_CURR,NET_VALUE,NET_VALUE_INGL_CURR,PLANT_ID,PLANT_RECORD_ID,SERVICE_DESCRIPTION,SERVICE_RECORD_ID,QUANTITY,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID,TAX_PERCENTAGE,TAX_AMOUNT,TAX_AMOUNT_INGL_CURR,UNIT_PRICE,UNIT_PRICE_INGL_CURR,ownerId, cartId) select SAQRIS.COMMITTED_VALUE,SAQRIS.CONTRACT_VALID_FROM,SAQRIS.CONTRACT_VALID_TO,SAQRIS.DIVISION_ID,SAQRIS.DIVISION_RECORD_ID,SAQRIS.DOC_CURRENCY,SAQRIS.DOCCURR_RECORD_ID,SAQRIS.ESTIMATED_VALUE,SAQRIS.GLOBAL_CURRENCY,SAQRIS.GLOBAL_CURRENCY_RECORD_ID,SAQRIS.LINE,SAQRIS.NET_PRICE,SAQRIS.NET_PRICE_INGL_CURR,SAQRIS.NET_VALUE,SAQRIS.NET_VALUE_INGL_CURR,SAQRIS.PLANT_ID,SAQRIS.PLANT_RECORD_ID,SAQRIS.SERVICE_DESCRIPTION,SAQRIS.SERVICE_RECORD_ID,SAQRIS.QUANTITY,SAQRIS.QUOTE_ID,SAQRIS.QUOTE_RECORD_ID,SAQRIS.QTEREV_ID,SAQRIS.QTEREV_RECORD_ID,SAQRIS.TAX_PERCENTAGE,SAQRIS.TAX_AMOUNT,SAQRIS.TAX_AMOUNT_INGL_CURR,SAQRIS.UNIT_PRICE,SAQRIS.UNIT_PRICE_INGL_CURR,{UserId} as ownerId,{CartId} as cartId from SAQRIS (NOLOCK)  where SAQRIS.QUOTE_RECORD_ID ='{c4c_quote_id}' and  SAQRIS.QTEREV_RECORD_ID= '{rev_rec_id}'""".format(CartId = cartobj.CART_ID,UserId= cartobj.USERID,c4c_quote_id = contract_quote_record_id,rev_rec_id = quote_revision_record_id))
	Sql.RunQuery(insrt_subtotal_offering)
	return True
#Document XML end


def language_select():
	Trace.Write("Inside language select")
	sec_str =  ''
	get_quote_status = Sql.GetFirst("SELECT REVISION_STATUS FROM SAQTRV WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(contract_quote_record_id,quote_revision_record_id))
	if str(get_quote_status.REVISION_STATUS).upper() == "APPROVED":
		Trace.Write("If")
		sec_str += ('<div id="container">')
		sec_str += (
				'<div class="dyn_main_head master_manufac glyphicon pointer   glyphicon-chevron-down" onclick="dyn_main_sec_collapse_arrow(this)" data-target=".sec_" data-toggle="collapse"><label class="onlytext"><label class="onlytext"><div><div id="ctr_drop" class="btn-group dropdown"><div class="dropdown"><i data-toggle="dropdown" class="fa fa-sort-desc dropdown-toggle"></i><ul class="dropdown-menu left" aria-labelledby="dropdownMenuButton"><li class="edit_list"> <a class="dropdown-item" href="#" onclick="CommonEDIT(this)">EDIT</a></li></ul></div></div>GENERAL SETTINGS</div></label></div>')

	
		sec_str += ('<div id="sec_LANG" class= sec_LANG>')
		#dropdown
		sec_str += (
		'<div style="height: 30px; border-left: 0px; border-right: 0px; border-bottom: 1px solid rgb(204, 204, 204); padding-bottom: 10px;" data-bind="attr: {"id":"drop_cont"+stdAttrCode(),"class": isWholeRow() ? "g4 except_sec dropDownHeight iconhvr" : "g1 except_sec dropDownHeight iconhvr" }" id="drop_cont11744" class="g4 except_sec dropDownHeight iconhvr">')
		sec_str += (
		'<div class="col-md-5">	<abbr data-bind="attr:{"title":label}" title="doc_lang"><label class="col-md-11" data-bind="html: label" style="padding: 5px 5px;margin: 0;" title="doc_lang">Document Language</label></abbr><a href="#" class="col-md-1" style="text-align:right;padding: 7px 5px;color:green">	<i class="fa fa-info-circle autoClosePopover" data-bind="popover: { templateId: "HintTemplate", container: "body", placement: "top", autoClose: true, html: true}" data-original-title="doc_lang" title=""></i></a></div><!--ko if: $data.template() === "DropDownTemplate" && $data.name().toString().indexOf("") === -1 && $data.name().toString().indexOf("") === -1 && $data.name().toString().indexOf("") === -1--><div class="col-md-3 pad-0"><select class="form-control light_yellow" id="Lang"><option value="Select">Select</option><option value="English">English</option><option value="Chinese">Chinese</option></select></div><!-- /ko --><!-- ko if: $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1--><!-- /ko --><div class="col-md-3 " style="display:none;"> <span class="" data-bind="attr:{"id": $data.name()}" id=""></span></div><div class="col-md-1" style="float: right;"><div class="col-md-12 editiconright"><a href="#" onclick="editclick_row(this)" class="editclick">	<i class="fa fa-pencil" aria-hidden="true"></i></a></div></div><div class="col-md-3 pad-0 mrg-bt-5"></div></div>')


		#dropdown
		sec_str += (
		'<div style="height: 30px; border-left: 0px; border-right: 0px; border-bottom: 1px solid rgb(204, 204, 204); padding-bottom: 10px;" data-bind="attr: {"id":"drop_cont"+stdAttrCode(),"class": isWholeRow() ? "g4 except_sec dropDownHeight iconhvr" : "g1 except_sec dropDownHeight iconhvr" }" id="drop_cont11744" class="g4 except_sec dropDownHeight iconhvr">')
		sec_str += (
		'<div class="col-md-5">	<abbr data-bind="attr:{"title":label}" title="doc_Cur"><label class="col-md-11" data-bind="html: label" style="padding: 5px 5px;margin: 0;" title="doc_lang">Document  Currency</label></abbr><a href="#" class="col-md-1" style="text-align:right;padding: 7px 5px;color:green">	<i class="fa fa-info-circle autoClosePopover" data-bind="popover: { templateId: "HintTemplate", container: "body", placement: "top", autoClose: true, html: true}" data-original-title="doc_lang" title=""></i></a></div><!--ko if: $data.template() === "DropDownTemplate" && $data.name().toString().indexOf("") === -1 && $data.name().toString().indexOf("") === -1 && $data.name().toString().indexOf("") === -1--><div class="col-md-3 pad-0"><select class="form-control light_yellow" id="Lang" ><option value="Select">Select</option><option value="Japan">YEN</option><option value="Dollar">USD</option><option value="Chinese">YUAN</option></select></div><!-- /ko --><!-- ko if: $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1--><!-- /ko --><div class="col-md-3 " style="display:none;"> <span class="" data-bind="attr:{"id": $data.name()}" id=""></span></div><div class="col-md-1" style="float: right;"><div class="col-md-12 editiconright"><a href="#" onclick="editclick_row(this)" class="editclick">	<i class="fa fa-pencil" aria-hidden="true"></i></a></div></div><div class="col-md-3 pad-0 mrg-bt-5"></div></div>')
	
		#Checkbox 1
		sec_str += (
		'<div style="height: 30px; border-left: 0px; border-right: 0px; border-bottom: 1px solid rgb(204, 204, 204); padding-bottom: 10px;" data-bind="attr: {"id":"drop_cont"+stdAttrCode(),"class": isWholeRow() ? "g4 except_sec dropDownHeight iconhvr" : "g1 except_sec dropDownHeight iconhvr" }" id="drop_cont11744" class="g4 except_sec dropDownHeight iconhvr">')
		sec_str += ('<div class="col-md-5">	<abbr data-bind="attr:{"title":label}" title="doc_lang"><label class="col-md-11" data-bind="html: label" style="padding: 5px 5px;margin: 0;" title="doc_lang">Include Expected Date of Fx Rate</label></abbr><a href="#" class="col-md-1" style="text-align:right;padding: 7px 5px;color:green">	<i class="fa fa-info-circle autoClosePopover" data-bind="popover: { templateId: "HintTemplate", container: "body", placement: "top", autoClose: true, html: true}" data-original-title="doc_lang" title=""></i></a></div><div class="col-md-3 pad-0 padt_7"><input id="bm" class="custom custom_gen_doc" type="checkbox" ><span class="lbl"></span></div><!-- /ko --><div class="col-md-3 " style="display:none;"> <span class="" data-bind="attr:{"id": $data.name()}" id=""></span></div><div class="col-md-1" style="float: right;"><div class="col-md-12 editiconright"><a href="#" onclick="editclick_row(this)" class="editclick">	<i class="fa fa-pencil" aria-hidden="true"></i></a></div></div><div class="col-md-3 pad-0 mrg-bt-5"></div></div><!-- /ko --><!-- ko if: $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1--><!-- /ko -->')
	
	
		#Checkbox 2
		sec_str += (
		'<div style="height: 30px; border-left: 0px; border-right: 0px; border-bottom: 1px solid rgb(204, 204, 204); padding-bottom: 10px;" data-bind="attr: {"id":"drop_cont"+stdAttrCode(),"class": isWholeRow() ? "g4 except_sec dropDownHeight iconhvr" : "g1 except_sec dropDownHeight iconhvr" }" id="drop_cont11744" class="g4 except_sec dropDownHeight iconhvr">')
		sec_str += ('<div class="col-md-5">	<abbr data-bind="attr:{"title":label}" title="doc_lang"><label class="col-md-11" data-bind="html: label" style="padding: 5px 5px;margin: 0;" title="doc_lang">Include Items</label></abbr><a href="#" class="col-md-1" style="text-align:right;padding: 7px 5px;color:green">	<i class="fa fa-info-circle autoClosePopover" data-bind="popover: { templateId: "HintTemplate", container: "body", placement: "top", autoClose: true, html: true}" data-original-title="doc_lang" title=""></i></a></div><div class="col-md-3 pad-0 padt_7"><input id="bm" class="custom custom_gen_doc" type="checkbox" ><span class="lbl"></span></div><!-- /ko --><div class="col-md-3 " style="display:none;"> <span class="" data-bind="attr:{"id": $data.name()}" id=""></span></div><div class="col-md-1" style="float: right;"><div class="col-md-12 editiconright"><a href="#" onclick="editclick_row(this)" class="editclick">	<i class="fa fa-pencil" aria-hidden="true"></i></a></div></div><div class="col-md-3 pad-0 mrg-bt-5"></div></div><!-- /ko --><!-- ko if: $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1--><!-- /ko -->')
	
	
	
		#Checkbox 3
		sec_str += (
		'<div style="height: 30px; border-left: 0px; border-right: 0px; border-bottom: 1px solid rgb(204, 204, 204); padding-bottom: 10px;" data-bind="attr: {"id":"drop_cont"+stdAttrCode(),"class": isWholeRow() ? "g4 except_sec dropDownHeight iconhvr" : "g1 except_sec dropDownHeight iconhvr" }" id="drop_cont11744" class="g4 except_sec dropDownHeight iconhvr">')
		sec_str += ('<div class="col-md-5">	<abbr data-bind="attr:{"title":label}" title="doc_lang"><label class="col-md-11" data-bind="html: label" style="padding: 5px 5px;margin: 0;" title="doc_lang">Include Signature Line</label></abbr><a href="#" class="col-md-1" style="text-align:right;padding: 7px 5px;color:green">	<i class="fa fa-info-circle autoClosePopover" data-bind="popover: { templateId: "HintTemplate", container: "body", placement: "top", autoClose: true, html: true}" data-original-title="doc_lang" title=""></i></a></div><div class="col-md-3 pad-0 padt_7"><input id="bm" class="custom custom_gen_doc" type="checkbox" ><span class="lbl"></span></div><!-- /ko --><div class="col-md-3 " style="display:none;"> <span class="" data-bind="attr:{"id": $data.name()}" id=""></span></div><div class="col-md-1" style="float: right;"><div class="col-md-12 editiconright"><a href="#" onclick="editclick_row(this)" class="editclick">	<i class="fa fa-pencil" aria-hidden="true"></i></a></div></div><div class="col-md-3 pad-0 mrg-bt-5"></div></div><!-- /ko --><!-- ko if: $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1--><!-- /ko -->')
	
		#Appendixes
		sec_str += ('<div id="container">')
		sec_str += (
				'<div class="dyn_main_head master_manufac glyphicon pointer   glyphicon-chevron-down" onclick="dyn_main_sec_collapse_arrow(this)" data-target=".sec_" data-toggle="collapse"><label class="onlytext"><label class="onlytext"><div><div id="ctr_drop" class="btn-group dropdown"><div class="dropdown"><i data-toggle="dropdown" class="fa fa-sort-desc dropdown-toggle"></i><ul class="dropdown-menu left" aria-labelledby="dropdownMenuButton"><li class="edit_list"> <a  class="dropdown-item" href="#" onclick="CommonEDIT(this)">EDIT</a></li></ul></div></div>APPENDIXES</div></label></div>')

		sec_str += ('<div id="sec_LANG" class= sec_LANG>')
 		#Checkbox 4
		sec_str += (
		'<div style="height: 30px; border-left: 0px; border-right: 0px; border-bottom: 1px solid rgb(204, 204, 204); padding-bottom: 10px;" data-bind="attr: {"id":"drop_cont"+stdAttrCode(),"class": isWholeRow() ? "g4 except_sec dropDownHeight iconhvr" : "g1 except_sec dropDownHeight iconhvr" }" id="drop_cont11744" class="g4 except_sec dropDownHeight iconhvr">')
		sec_str += ('<div class="col-md-5">	<abbr data-bind="attr:{"title":label}" title="doc_lang"><label class="col-md-11" data-bind="html: label" style="padding: 5px 5px;margin: 0;" title="doc_lang">Include Parts List</label></abbr><a href="#" class="col-md-1" style="text-align:right;padding: 7px 5px;color:green">	<i class="fa fa-info-circle autoClosePopover" data-bind="popover: { templateId: "HintTemplate", container: "body", placement: "top", autoClose: true, html: true}" data-original-title="doc_lang" title=""></i></a></div><div class="col-md-3 pad-0 padt_7"><input id="bm" class="custom custom_gen_doc" type="checkbox" ><span class="lbl"></span></div><!-- /ko --><div class="col-md-3 " style="display:none;"> <span class="" data-bind="attr:{"id": $data.name()}" id=""></span></div><div class="col-md-1" style="float: right;"><div class="col-md-12 editiconright"><a href="#" onclick="editclick_row(this)" class="editclick">	<i class="fa fa-pencil" aria-hidden="true"></i></a></div></div><div class="col-md-3 pad-0 mrg-bt-5"></div></div><!-- /ko --><!-- ko if: $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1--><!-- /ko -->')
		#checkbox 5
		sec_str += (
		'<div style="height: 30px; border-left: 0px; border-right: 0px; border-bottom: 1px solid rgb(204, 204, 204); padding-bottom: 10px;" data-bind="attr: {"id":"drop_cont"+stdAttrCode(),"class": isWholeRow() ? "g4 except_sec dropDownHeight iconhvr" : "g1 except_sec dropDownHeight iconhvr" }" id="drop_cont11744" class="g4 except_sec dropDownHeight iconhvr">')
		sec_str += ('<div class="col-md-5">	<abbr data-bind="attr:{"title":label}" title="doc_lang"><label class="col-md-11" data-bind="html: label" style="padding: 5px 5px;margin: 0;" title="doc_lang">Include Part Delivery schedule(FPM only)</label></abbr><a href="#" class="col-md-1" style="text-align:right;padding: 7px 5px;color:green">	<i class="fa fa-info-circle autoClosePopover" data-bind="popover: { templateId: "HintTemplate", container: "body", placement: "top", autoClose: true, html: true}" data-original-title="doc_lang" title=""></i></a></div><div class="col-md-3 pad-0 padt_7"><input id="bm" class="custom custom_gen_doc" type="checkbox" ><span class="lbl"></span></div><!-- /ko --><div class="col-md-3 " style="display:none;"> <span class="" data-bind="attr:{"id": $data.name()}" id=""></span></div><div class="col-md-1" style="float: right;"><div class="col-md-12 editiconright"><a href="#" onclick="editclick_row(this)" class="editclick">	<i class="fa fa-pencil" aria-hidden="true"></i></a></div></div><div class="col-md-3 pad-0 mrg-bt-5"></div></div><!-- /ko --><!-- ko if: $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1--><!-- /ko -->')	
    	#checkbox 5
		sec_str += (
		'<div style="height: 30px; border-left: 0px; border-right: 0px; border-bottom: 1px solid rgb(204, 204, 204); padding-bottom: 10px;" data-bind="attr: {"id":"drop_cont"+stdAttrCode(),"class": isWholeRow() ? "g4 except_sec dropDownHeight iconhvr" : "g1 except_sec dropDownHeight iconhvr" }" id="drop_cont11744" class="g4 except_sec dropDownHeight iconhvr">')
		sec_str += ('<div class="col-md-5">	<abbr data-bind="attr:{"title":label}" title="doc_lang"><label class="col-md-11" data-bind="html: label" style="padding: 5px 5px;margin: 0;" title="doc_lang">Include Detailed Billing Matrix by Offering</label></abbr><a href="#" class="col-md-1" style="text-align:right;padding: 7px 5px;color:green">	<i class="fa fa-info-circle autoClosePopover" data-bind="popover: { templateId: "HintTemplate", container: "body", placement: "top", autoClose: true, html: true}" data-original-title="doc_lang" title=""></i></a></div><div class="col-md-3 pad-0 padt_7"><input id="bm" class="custom custom_gen_doc" type="checkbox" ><span class="lbl"></span></div><!-- /ko --><div class="col-md-3 " style="display:none;"> <span class="" data-bind="attr:{"id": $data.name()}" id=""></span></div><div class="col-md-1" style="float: right;"><div class="col-md-12 editiconright"><a href="#" onclick="editclick_row(this)" class="editclick">	<i class="fa fa-pencil" aria-hidden="true"></i></a></div></div><div class="col-md-3 pad-0 mrg-bt-5"></div></div><!-- /ko --><!-- ko if: $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1--><!-- /ko -->')

		#dropdown
		sec_str += (
		'<div style="height: 30px; border-left: 0px; border-right: 0px; border-bottom: 1px solid rgb(204, 204, 204); padding-bottom: 10px;" data-bind="attr: {"id":"drop_cont"+stdAttrCode(),"class": isWholeRow() ? "g4 except_sec dropDownHeight iconhvr" : "g1 except_sec dropDownHeight iconhvr" }" id="drop_cont11744" class="g4 except_sec dropDownHeight iconhvr">')
		sec_str += (
		'<div class="col-md-5">	<abbr data-bind="attr:{"title":label}" title="doc_lang"><label class="col-md-11" data-bind="html: label" style="padding: 5px 5px;margin: 0;" title="doc_lang">Include Critical parameter</label></abbr><a href="#" class="col-md-1" style="text-align:right;padding: 7px 5px;color:green">	<i class="fa fa-info-circle autoClosePopover" data-bind="popover: { templateId: "HintTemplate", container: "body", placement: "top", autoClose: true, html: true}" data-original-title="doc_lang" title=""></i></a></div><!--ko if: $data.template() === "DropDownTemplate" && $data.name().toString().indexOf("") === -1 && $data.name().toString().indexOf("") === -1 && $data.name().toString().indexOf("") === -1--><div class="col-md-3 pad-0"><select id="doc" class="form-control light_yellow" id="Lang"><option value="Select">Select</option><option value="Critical Parameters by Greenbook">Critical Parameters by Greenbook</option><option value="Critical Parameters by Fab and Greenbook">Critical Parameters by Fab and Greenbook</option></select></div><!-- /ko --><!-- ko if: $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1--><!-- /ko --><div class="col-md-3 " style="display:none;"> <span class="" data-bind="attr:{"id": $data.name()}" id=""></span></div><div class="col-md-1" style="float: right;"><div class="col-md-12 editiconright"><a href="#" onclick="editclick_row(this)" class="editclick">	<i class="fa fa-pencil" aria-hidden="true"></i></a></div></div><div class="col-md-3 pad-0 mrg-bt-5"></div></div>')


		#sec_str += (
		#	'<div class="g4  except_sec removeHorLine iconhvr sec_edit_sty"><button id="SEC_DIS_CLOSE" style="display: none;"></button><button id="Lang_cancel" class="btnconfig btnMainBanner sec_edit_sty_btn" onclick="lang_cancel()" name="SECT_CANCEL">CANCEL</button><button id="Lang_Select" class="btnconfig btnMainBanner sec_edit_sty_btn_inh" onclick="lang_save()" name="SECT_SAVE">SAVE</button></div>'
		#)

		sec_str += (
		"</div>")

		sec_str += '<table class="wth100mrg8"><tbody>'
	else:
		Trace.Write("Else")
		sec_str += ('<div id="container">')
		sec_str += (
				'<div class="dyn_main_head master_manufac glyphicon pointer   glyphicon-chevron-down" onclick="dyn_main_sec_collapse_arrow(this)" data-target=".sec_" data-toggle="collapse"><label class="onlytext"><label class="onlytext"><div><div id="ctr_drop" class="btn-group dropdown"><div class="dropdown"><i data-toggle="dropdown" class="fa fa-sort-desc dropdown-toggle"></i><ul class="dropdown-menu left" aria-labelledby="dropdownMenuButton"><li class="edit_list"> <a class="dropdown-item" href="#" onclick="CommonEDIT(this)">EDIT</a></li></ul></div></div>GENERAL SETTINGS</div></label></div>')

	
		sec_str += ('<div id="sec_LANG" class= sec_LANG>')
		#dropdown
		sec_str += (
		'<div style="height: 30px; border-left: 0px; border-right: 0px; border-bottom: 1px solid rgb(204, 204, 204); padding-bottom: 10px;" data-bind="attr: {"id":"drop_cont"+stdAttrCode(),"class": isWholeRow() ? "g4 except_sec dropDownHeight iconhvr" : "g1 except_sec dropDownHeight iconhvr" }" id="drop_cont11744" class="g4 except_sec dropDownHeight iconhvr">')
		sec_str += (
		'<div class="col-md-5">	<abbr data-bind="attr:{"title":label}" title="doc_lang"><label class="col-md-11" data-bind="html: label" style="padding: 5px 5px;margin: 0;" title="doc_lang">Document Language</label></abbr><a href="#" class="col-md-1" style="text-align:right;padding: 7px 5px;color:green">	<i class="fa fa-info-circle autoClosePopover" data-bind="popover: { templateId: "HintTemplate", container: "body", placement: "top", autoClose: true, html: true}" data-original-title="doc_lang" title=""></i></a></div><!--ko if: $data.template() === "DropDownTemplate" && $data.name().toString().indexOf("") === -1 && $data.name().toString().indexOf("") === -1 && $data.name().toString().indexOf("") === -1--><div class="col-md-3 pad-0"><select class="form-control" id="Lang" disabled><option value="Select">Select</option><option value="English">English</option><option value="Chinese">Chinese</option></select></div><!-- /ko --><!-- ko if: $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1--><!-- /ko --><div class="col-md-3 " style="display:none;"> <span class="" data-bind="attr:{"id": $data.name()}" id=""></span></div><div class="col-md-1" style="float: right;"><div class="col-md-12 editiconright"><a href="#" onclick="editclick_row(this)" class="editclick">	<i class="fa fa-pencil" aria-hidden="true"></i></a></div></div><div class="col-md-3 pad-0 mrg-bt-5"></div></div>')


		#dropdown
		sec_str += (
		'<div style="height: 30px; border-left: 0px; border-right: 0px; border-bottom: 1px solid rgb(204, 204, 204); padding-bottom: 10px;" data-bind="attr: {"id":"drop_cont"+stdAttrCode(),"class": isWholeRow() ? "g4 except_sec dropDownHeight iconhvr" : "g1 except_sec dropDownHeight iconhvr" }" id="drop_cont11744" class="g4 except_sec dropDownHeight iconhvr">')
		sec_str += (
		'<div class="col-md-5">	<abbr data-bind="attr:{"title":label}" title="doc_Cur"><label class="col-md-11" data-bind="html: label" style="padding: 5px 5px;margin: 0;" title="doc_lang">Document  Currency</label></abbr><a href="#" class="col-md-1" style="text-align:right;padding: 7px 5px;color:green">	<i class="fa fa-info-circle autoClosePopover" data-bind="popover: { templateId: "HintTemplate", container: "body", placement: "top", autoClose: true, html: true}" data-original-title="doc_lang" title=""></i></a></div><!--ko if: $data.template() === "DropDownTemplate" && $data.name().toString().indexOf("") === -1 && $data.name().toString().indexOf("") === -1 && $data.name().toString().indexOf("") === -1--><div class="col-md-3 pad-0"><select class="form-control" id="Lang" disabled><option value="Select">Select</option><option value="Japan">YEN</option><option value="Dollar">USD</option><option value="Chinese">YUAN</option></select></div><!-- /ko --><!-- ko if: $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1--><!-- /ko --><div class="col-md-3 " style="display:none;"> <span class="" data-bind="attr:{"id": $data.name()}" id=""></span></div><div class="col-md-1" style="float: right;"><div class="col-md-12 editiconright"><a href="#" onclick="editclick_row(this)" class="editclick">	<i class="fa fa-pencil" aria-hidden="true"></i></a></div></div><div class="col-md-3 pad-0 mrg-bt-5"></div></div>')
	
		#Checkbox 1
		sec_str += (
		'<div style="height: 30px; border-left: 0px; border-right: 0px; border-bottom: 1px solid rgb(204, 204, 204); padding-bottom: 10px;" data-bind="attr: {"id":"drop_cont"+stdAttrCode(),"class": isWholeRow() ? "g4 except_sec dropDownHeight iconhvr" : "g1 except_sec dropDownHeight iconhvr" }" id="drop_cont11744" class="g4 except_sec dropDownHeight iconhvr">')
		sec_str += ('<div class="col-md-5">	<abbr data-bind="attr:{"title":label}" title="doc_lang"><label class="col-md-11" data-bind="html: label" style="padding: 5px 5px;margin: 0;" title="doc_lang">Include Expected Date of Fx Rate</label></abbr><a href="#" class="col-md-1" style="text-align:right;padding: 7px 5px;color:green">	<i class="fa fa-info-circle autoClosePopover" data-bind="popover: { templateId: "HintTemplate", container: "body", placement: "top", autoClose: true, html: true}" data-original-title="doc_lang" title=""></i></a></div><div class="col-md-3 pad-0 padt_7"><input id="bm" class="custom custom_gen_doc" type="checkbox" ><span class="lbl"></span></div><!-- /ko --><div class="col-md-3 " style="display:none;"> <span class="" data-bind="attr:{"id": $data.name()}" id=""></span></div><div class="col-md-1" style="float: right;"><div class="col-md-12 editiconright"><a href="#" onclick="editclick_row(this)" class="editclick">	<i class="fa fa-pencil" aria-hidden="true"></i></a></div></div><div class="col-md-3 pad-0 mrg-bt-5"></div></div><!-- /ko --><!-- ko if: $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1--><!-- /ko -->')
	
	
		#Checkbox 2
		sec_str += (
		'<div style="height: 30px; border-left: 0px; border-right: 0px; border-bottom: 1px solid rgb(204, 204, 204); padding-bottom: 10px;" data-bind="attr: {"id":"drop_cont"+stdAttrCode(),"class": isWholeRow() ? "g4 except_sec dropDownHeight iconhvr" : "g1 except_sec dropDownHeight iconhvr" }" id="drop_cont11744" class="g4 except_sec dropDownHeight iconhvr">')
		sec_str += ('<div class="col-md-5">	<abbr data-bind="attr:{"title":label}" title="doc_lang"><label class="col-md-11" data-bind="html: label" style="padding: 5px 5px;margin: 0;" title="doc_lang">Include Items</label></abbr><a href="#" class="col-md-1" style="text-align:right;padding: 7px 5px;color:green">	<i class="fa fa-info-circle autoClosePopover" data-bind="popover: { templateId: "HintTemplate", container: "body", placement: "top", autoClose: true, html: true}" data-original-title="doc_lang" title=""></i></a></div><div class="col-md-3 pad-0 padt_7"><input id="bm" class="custom custom_gen_doc" type="checkbox" ><span class="lbl"></span></div><!-- /ko --><div class="col-md-3 " style="display:none;"> <span class="" data-bind="attr:{"id": $data.name()}" id=""></span></div><div class="col-md-1" style="float: right;"><div class="col-md-12 editiconright"><a href="#" onclick="editclick_row(this)" class="editclick">	<i class="fa fa-pencil" aria-hidden="true"></i></a></div></div><div class="col-md-3 pad-0 mrg-bt-5"></div></div><!-- /ko --><!-- ko if: $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1--><!-- /ko -->')
	
	
	
		#Checkbox 3
		sec_str += (
		'<div style="height: 30px; border-left: 0px; border-right: 0px; border-bottom: 1px solid rgb(204, 204, 204); padding-bottom: 10px;" data-bind="attr: {"id":"drop_cont"+stdAttrCode(),"class": isWholeRow() ? "g4 except_sec dropDownHeight iconhvr" : "g1 except_sec dropDownHeight iconhvr" }" id="drop_cont11744" class="g4 except_sec dropDownHeight iconhvr">')
		sec_str += ('<div class="col-md-5">	<abbr data-bind="attr:{"title":label}" title="doc_lang"><label class="col-md-11" data-bind="html: label" style="padding: 5px 5px;margin: 0;" title="doc_lang">Include Signature Line</label></abbr><a href="#" class="col-md-1" style="text-align:right;padding: 7px 5px;color:green">	<i class="fa fa-info-circle autoClosePopover" data-bind="popover: { templateId: "HintTemplate", container: "body", placement: "top", autoClose: true, html: true}" data-original-title="doc_lang" title=""></i></a></div><div class="col-md-3 pad-0 padt_7"><input id="bm" class="custom custom_gen_doc" type="checkbox" ><span class="lbl"></span></div><!-- /ko --><div class="col-md-3 " style="display:none;"> <span class="" data-bind="attr:{"id": $data.name()}" id=""></span></div><div class="col-md-1" style="float: right;"><div class="col-md-12 editiconright"><a href="#" onclick="editclick_row(this)" class="editclick">	<i class="fa fa-pencil" aria-hidden="true"></i></a></div></div><div class="col-md-3 pad-0 mrg-bt-5"></div></div><!-- /ko --><!-- ko if: $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1--><!-- /ko -->')
	
		#Appendixes
		sec_str += ('<div id="container">')
		sec_str += (
				'<div class="dyn_main_head master_manufac glyphicon pointer   glyphicon-chevron-down" onclick="dyn_main_sec_collapse_arrow(this)" data-target=".sec_" data-toggle="collapse"><label class="onlytext"><label class="onlytext"><div><div id="ctr_drop" class="btn-group dropdown"><div class="dropdown"><i data-toggle="dropdown" class="fa fa-sort-desc dropdown-toggle"></i><ul class="dropdown-menu left" aria-labelledby="dropdownMenuButton"><li class="edit_list"> <a  class="dropdown-item" href="#" onclick="CommonEDIT(this)">EDIT</a></li></ul></div></div>APPENDIXES</div></label></div>')

		sec_str += ('<div id="sec_LANG" class= sec_LANG>')
 		#Checkbox 4
		sec_str += (
		'<div style="height: 30px; border-left: 0px; border-right: 0px; border-bottom: 1px solid rgb(204, 204, 204); padding-bottom: 10px;" data-bind="attr: {"id":"drop_cont"+stdAttrCode(),"class": isWholeRow() ? "g4 except_sec dropDownHeight iconhvr" : "g1 except_sec dropDownHeight iconhvr" }" id="drop_cont11744" class="g4 except_sec dropDownHeight iconhvr">')
		sec_str += ('<div class="col-md-5">	<abbr data-bind="attr:{"title":label}" title="doc_lang"><label class="col-md-11" data-bind="html: label" style="padding: 5px 5px;margin: 0;" title="doc_lang">Include Parts List</label></abbr><a href="#" class="col-md-1" style="text-align:right;padding: 7px 5px;color:green">	<i class="fa fa-info-circle autoClosePopover" data-bind="popover: { templateId: "HintTemplate", container: "body", placement: "top", autoClose: true, html: true}" data-original-title="doc_lang" title=""></i></a></div><div class="col-md-3 pad-0 padt_7"><input id="bm" class="custom custom_gen_doc" type="checkbox" ><span class="lbl"></span></div><!-- /ko --><div class="col-md-3 " style="display:none;"> <span class="" data-bind="attr:{"id": $data.name()}" id=""></span></div><div class="col-md-1" style="float: right;"><div class="col-md-12 editiconright"><a href="#" onclick="editclick_row(this)" class="editclick">	<i class="fa fa-pencil" aria-hidden="true"></i></a></div></div><div class="col-md-3 pad-0 mrg-bt-5"></div></div><!-- /ko --><!-- ko if: $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1--><!-- /ko -->')
		#checkbox 5
		sec_str += (
		'<div style="height: 30px; border-left: 0px; border-right: 0px; border-bottom: 1px solid rgb(204, 204, 204); padding-bottom: 10px;" data-bind="attr: {"id":"drop_cont"+stdAttrCode(),"class": isWholeRow() ? "g4 except_sec dropDownHeight iconhvr" : "g1 except_sec dropDownHeight iconhvr" }" id="drop_cont11744" class="g4 except_sec dropDownHeight iconhvr">')
		sec_str += ('<div class="col-md-5">	<abbr data-bind="attr:{"title":label}" title="doc_lang"><label class="col-md-11" data-bind="html: label" style="padding: 5px 5px;margin: 0;" title="doc_lang">Include Part Delivery schedule(FPM only)</label></abbr><a href="#" class="col-md-1" style="text-align:right;padding: 7px 5px;color:green">	<i class="fa fa-info-circle autoClosePopover" data-bind="popover: { templateId: "HintTemplate", container: "body", placement: "top", autoClose: true, html: true}" data-original-title="doc_lang" title=""></i></a></div><div class="col-md-3 pad-0 padt_7"><input id="bm" class="custom custom_gen_doc" type="checkbox" ><span class="lbl"></span></div><!-- /ko --><div class="col-md-3 " style="display:none;"> <span class="" data-bind="attr:{"id": $data.name()}" id=""></span></div><div class="col-md-1" style="float: right;"><div class="col-md-12 editiconright"><a href="#" onclick="editclick_row(this)" class="editclick">	<i class="fa fa-pencil" aria-hidden="true"></i></a></div></div><div class="col-md-3 pad-0 mrg-bt-5"></div></div><!-- /ko --><!-- ko if: $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1--><!-- /ko -->')	
    	#checkbox 5
		sec_str += (
		'<div style="height: 30px; border-left: 0px; border-right: 0px; border-bottom: 1px solid rgb(204, 204, 204); padding-bottom: 10px;" data-bind="attr: {"id":"drop_cont"+stdAttrCode(),"class": isWholeRow() ? "g4 except_sec dropDownHeight iconhvr" : "g1 except_sec dropDownHeight iconhvr" }" id="drop_cont11744" class="g4 except_sec dropDownHeight iconhvr">')
		sec_str += ('<div class="col-md-5">	<abbr data-bind="attr:{"title":label}" title="doc_lang"><label class="col-md-11" data-bind="html: label" style="padding: 5px 5px;margin: 0;" title="doc_lang">Include Detailed Billing Matrix by Offering</label></abbr><a href="#" class="col-md-1" style="text-align:right;padding: 7px 5px;color:green">	<i class="fa fa-info-circle autoClosePopover" data-bind="popover: { templateId: "HintTemplate", container: "body", placement: "top", autoClose: true, html: true}" data-original-title="doc_lang" title=""></i></a></div><div class="col-md-3 pad-0 padt_7"><input id="bm" class="custom custom_gen_doc" type="checkbox" ><span class="lbl"></span></div><!-- /ko --><div class="col-md-3 " style="display:none;"> <span class="" data-bind="attr:{"id": $data.name()}" id=""></span></div><div class="col-md-1" style="float: right;"><div class="col-md-12 editiconright"><a href="#" onclick="editclick_row(this)" class="editclick">	<i class="fa fa-pencil" aria-hidden="true"></i></a></div></div><div class="col-md-3 pad-0 mrg-bt-5"></div></div><!-- /ko --><!-- ko if: $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1--><!-- /ko -->')

		#dropdown
		sec_str += (
		'<div style="height: 30px; border-left: 0px; border-right: 0px; border-bottom: 1px solid rgb(204, 204, 204); padding-bottom: 10px;" data-bind="attr: {"id":"drop_cont"+stdAttrCode(),"class": isWholeRow() ? "g4 except_sec dropDownHeight iconhvr" : "g1 except_sec dropDownHeight iconhvr" }" id="drop_cont11744" class="g4 except_sec dropDownHeight iconhvr">')
		sec_str += (
		'<div class="col-md-5">	<abbr data-bind="attr:{"title":label}" title="doc_lang"><label class="col-md-11" data-bind="html: label" style="padding: 5px 5px;margin: 0;" title="doc_lang">Include Critical parameter</label></abbr><a href="#" class="col-md-1" style="text-align:right;padding: 7px 5px;color:green">	<i class="fa fa-info-circle autoClosePopover" data-bind="popover: { templateId: "HintTemplate", container: "body", placement: "top", autoClose: true, html: true}" data-original-title="doc_lang" title=""></i></a></div><!--ko if: $data.template() === "DropDownTemplate" && $data.name().toString().indexOf("") === -1 && $data.name().toString().indexOf("") === -1 && $data.name().toString().indexOf("") === -1--><div class="col-md-3 pad-0"><select id="doc" class="form-control" id="Lang" disabled><option value="Select">Select</option><option value="Critical Parameters by Greenbook">Critical Parameters by Greenbook</option><option value="Critical Parameters by Fab and Greenbook">Critical Parameters by Fab and Greenbook</option></select></div><!-- /ko --><!-- ko if: $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1 || $data.name().toString().indexOf("") !== -1--><!-- /ko --><div class="col-md-3 " style="display:none;"> <span class="" data-bind="attr:{"id": $data.name()}" id=""></span></div><div class="col-md-1" style="float: right;"><div class="col-md-12 editiconright"><a href="#" onclick="editclick_row(this)" class="editclick">	<i class="fa fa-pencil" aria-hidden="true"></i></a></div></div><div class="col-md-3 pad-0 mrg-bt-5"></div></div>')


		#sec_str += (
		#	'<div class="g4  except_sec removeHorLine iconhvr sec_edit_sty"><button id="SEC_DIS_CLOSE" style="display: none;"></button><button id="Lang_cancel" class="btnconfig btnMainBanner sec_edit_sty_btn" onclick="lang_cancel()" name="SECT_CANCEL">CANCEL</button><button id="Lang_Select" class="btnconfig btnMainBanner sec_edit_sty_btn_inh" onclick="lang_save()" name="SECT_SAVE">SAVE</button></div>'
		#)

		sec_str += (
		"</div>")

		sec_str += '<table class="wth100mrg8"><tbody>'
	return sec_str

try:
    action_type = Param.LOAD
except:
    action_type = ''


Trace.Write("inside"+str(action_type))

    

if action_type == "DOCUMENT":
	Trace.Write("inside"+str(action_type))
	ApiResponse = ApiResponseFactory.JsonResponse(language_select())
	
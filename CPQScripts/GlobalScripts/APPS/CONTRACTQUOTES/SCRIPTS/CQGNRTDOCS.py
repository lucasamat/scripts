# ==========================================================================================================================================
#   __script_name : CQGNRTDOCS.PY
#   __script_description : THIS SCRIPT IS USED TO GENERATE DOCUMENTS IN CONTRACT QUOTES APP.
#   __primary_author__ : Prithvi Reddy
#   __create_date :
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct
import re
import System
import sys
import time
from System import IO
from System import Web
import System.Net
from System.Net import WebClient

import System
from System.Net import WebRequest
from System.Net import HttpWebResponse

from datetime import datetime
import CQDOCIFLOW
from SYDATABASE import SQL
Sql = SQL()
userId = str(User.Id)
userName = str(User.UserName)

tableInfo = SqlHelper.GetTable("SAQDOC")
try:

	recid = Product.Attr('QSTN_SYSEFL_QT_00001').GetValue()
except:
	pass
try:
	quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
except:
	quote_revision_record_id = ""
try:
	quoteid = SqlHelper.GetFirst("SELECT QUOTE_ID, QUOTE_NAME,C4C_QUOTE_ID FROM SAQTMT(NOLOCK) WHERE MASTER_TABLE_QUOTE_RECORD_ID =  '"+str(recid)+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id) + "'")


	audit_fields = SqlHelper.GetFirst("SELECT USERS.USERNAME,SAQDOC.CpqTableEntryDateModified,SAQDOC.CPQTABLEENTRYDATEADDED,SAQDOC.CPQTABLEENTRYADDEDBY,SAQDOC.CpqTableEntryModifiedBy from USERS inner join SAQDOC(NOLOCK)  on SAQDOC.CpqTableEntryModifiedBy = USERS.ID  ")

	Log.Info('16-------spare quote---'+str(recid))
	extline_pri = 0.00
	# QuoteproductTotals = Quote.QuoteTables["SAQITM"]

	# for i in QuoteproductTotals.Rows:
	# 	Log.Info('38--extline_pri---SAQITM---'+str(extline_pri))
	# 	extline_pri += float(i['EXTENDED_UNIT_PRICE'])
	# 	Quote.SetGlobal('SubtotalLineItems', str(extline_pri))
	Quote.GetCustomField('SubtotalLineItems').Content = str(extline_pri)
	Log.Info('52--extline_pri------'+str(extline_pri))



	extitm_price = extd_pr =  taxtotal = 0.00


	Quote.GetCustomField('SubtotalTools').Content = str(extitm_price)


	exts_price = 0.00
	QuoteproductTotalsco = Quote.QuoteTables["SAQICO"]

	for i in QuoteproductTotalsco.Rows:
		Log.Info('SAQICO---'+str(i['EXTENDED_PRICE']))
		#exts_price += float(i['EXTENDED_PRICE'])
		exts_price += float(i['EXTENDED_PRICE'] +(i['TAX']))
		Quote.SetGlobal('SubtotalTools', str(exts_price))
	Quote.GetCustomField('SubtotalTools').Content = str(exts_price)



	extt_price = 0
	fptotal =  0

	getdynamicrcords = SqlHelper.GetList("Select * from QT__SAQIFP where QUOTE_RECORD_ID = '"+str(recid)+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id) + "'")
	for val in getdynamicrcords:
		Log.Info('16---spare quote--UNIT_PRICE entry--')
		extt_price += float(val.UNIT_PRICE)
		fptotal += float(val.EXTENDED_PRICE)
		Quote.SetGlobal('SubtotalspareTools', str(extt_price))
		Log.Info('16--75---extt_price--UNIT_PRICE--SAQIFP--SUBTOTSL---'+str(extt_price))
		Quote.SetGlobal('SubtotalTools', str(extt_price))
		Quote.SetGlobal('totalspareTools', str(fptotal))
	Quote.GetCustomField('SubtotalTools').Content = str(extt_price)
	Log.Info('16---spare quote--extt_price--UNIT_PRICE--SAQIFP--SUBTOTSL---'+str(extt_price))
	Log.Info('16---spare quote---TOTAL_PRICE--SAQIFP--total--'+str(fptotal))

	ext_price = 0.00
	QuoteproductTotals = Quote.QuoteTables["SAQICO"]
	Log.Info('150------QuoteproductTotalsfp----'+str(QuoteproductTotals.Rows.Count))
	for i in QuoteproductTotals.Rows:
		Log.Info('93---'+str(ext_price))
		#ext_price += float(i['SUBTOTAL'])
		#ext_price = round(float(ext_price) + float(i['SUBTOTAL']), 2)
		Quote.GetCustomField('SubtotalTools').Content = str(ext_price)
	Log.Info(str(ext_price))
	tableInfo = SqlHelper.GetTable("SAQDOC")
except:
	pass
try:
	recid = Product.Attr('QSTN_SYSEFL_QT_00001').GetValue()
except:
	pass


def english_doc():
	cv = Param.Condensed_View
	if cv == True:
		Quote.GetCustomField('Condensed_View').Content = 'Yes'
		Quote.SetGlobal('condview', 'Yes')
		
	elif cv == False:
		Quote.GetCustomField('Condensed_View').Content = 'No'
		Quote.SetGlobal('condview', 'No')
		
	# Quote.Save()
	lidv = Param.Line_View
	if lidv == True:
		Quote.GetCustomField('Line_Item_Detail_View').Content = 'Yes'
		Quote.GetCustomField('Condensed_View').Content = 'Yes'
		Quote.SetGlobal('condview', 'Yes')
		Log.Info('Checked')
	elif lidv == False:
		Quote.GetCustomField('Line_Item_Detail_View').Content = 'No'
		Quote.SetGlobal('condview', 'No')
		Log.Info('unChecked')
	sp_view = Param.Spare_view
	'''if sp_view == True:
		Quote.GetCustomField('Include_Spare_Item_Detail').Content = 'Yes'
		Quote.SetGlobal('spareview', 'Yes')
		Log.Info('Checked')
	elif sp_view == False:
		Quote.GetCustomField('Include_Spare_Item_Detail').Content = 'No'
		Quote.SetGlobal('spareview', 'No')
		Log.Info('unChecked')'''
	recid = Product.Attr('QSTN_SYSEFL_QT_00001').GetValue()    
	getyears = ""
	Getyear = SqlHelper.GetFirst("select CONTRACT_VALID_FROM,CONTRACT_VALID_TO from SAQTMT where MASTER_TABLE_QUOTE_RECORD_ID = '"+str(recid)+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id) + "'")
	if Getyear:
		start_date = datetime(Getyear.CONTRACT_VALID_FROM)
		end_date = datetime(Getyear.CONTRACT_VALID_TO)
		mm = (end_date. year - start_date. year) * 12 + (end_date. month - start_date. month)
		quotient, remainder = divmod(mm, 12)
		getyears = quotient + (1 if remainder > 0 else 0)
		Log.Info('getyears-----'+str(getyears))
		Quote.GetCustomField('GetBillingMatrix_Year').Content = str(getyears)
	# Quote.Save()
	
	
	Quote.Save()
	
	tableInfo = SqlHelper.GetTable("SAQDOC")
	recid = Product.Attr('QSTN_SYSEFL_QT_00001').GetValue()
	#Param 2 - Language 
	try:
		quote = recid
		language = "ENGLISH DOC,"+str(userId)+","+str(userName)
		CQDOCIFLOW.docgeneration(quote,language,quote_revision_record_id)
		
	except:
		
		Log.Info("EXCEPT english doc")


def chinese_doc():
	cv = Param.Condensed_View
	if cv == True:
		Quote.GetCustomField('Condensed_View').Content = 'Yes'
		Quote.SetGlobal('condview', 'Yes')
		Log.Info('Checked')
	elif cv == False:
		Quote.GetCustomField('Condensed_View').Content = 'No'
		Quote.SetGlobal('condview', 'No')
		Log.Info('unChecked')
	Quote.Save()
	lidv = Param.Line_View
	if lidv == True:
		Quote.GetCustomField('Line_Item_Detail_View').Content = 'Yes'
		Quote.GetCustomField('Condensed_View').Content = 'Yes'
		Quote.SetGlobal('condview', 'Yes')
		Log.Info('Checked')
	elif lidv == False:
		Quote.GetCustomField('Line_Item_Detail_View').Content = 'No'
		Quote.SetGlobal('condview', 'No')
		Log.Info('unChecked')
	
	recid = Product.Attr('QSTN_SYSEFL_QT_00001').GetValue()
	getyears = ""
	Getyear = SqlHelper.GetFirst("select CONTRACT_VALID_FROM,CONTRACT_VALID_TO from SAQTMT where MASTER_TABLE_QUOTE_RECORD_ID = '"+str(recid)+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id) + "'")
	if Getyear:
		start_date = datetime(Getyear.CONTRACT_VALID_FROM)
		end_date = datetime(Getyear.CONTRACT_VALID_TO)
		mm = (end_date. year - start_date. year) * 12 + (end_date. month - start_date. month)
		quotient, remainder = divmod(mm, 12)
		getyears = quotient + (1 if remainder > 0 else 0)
		Log.Info('getyears-----'+str(getyears))
		Quote.GetCustomField('GetBillingMatrix_Year').Content = str(getyears)
	Quote.Save()
	
	Quote.Save()
	
	tableInfo = SqlHelper.GetTable("SAQDOC")
	recid = Product.Attr('QSTN_SYSEFL_QT_00001').GetValue()
	try:
		quote = recid
		language = "CHINESE DOC,"+str(userId)+","+str(userName)
		CQDOCIFLOW.docgeneration(quote,language,quote_revision_record_id)
		
	except:
		
		Log.Info("EXCEPT english doc")
	
def fpm_doc():
	cv = Param.Condensed_View
	Log.Info('cv'+str(cv))
	if cv == True:
		Quote.GetCustomField('Condensed_View').Content = 'Yes'
		Quote.SetGlobal('condview', 'Yes')
		Log.Info('Checked')
	elif cv == False:
		Quote.GetCustomField('Condensed_View').Content = 'No'
		Quote.SetGlobal('condview', 'No')
		Log.Info('unChecked')
	Quote.Save()
	lidv = Param.Line_View
	Log.Info('lidv'+str(lidv))
	if lidv == True:
		Quote.GetCustomField('Line_Item_Detail_View').Content = 'Yes'
		Quote.GetCustomField('Condensed_View').Content = 'Yes'
		Quote.SetGlobal('condview', 'Yes')
		Log.Info('Checked'+str(Quote.GetCustomField('Line_Item_Detail_View').Content))
	elif lidv == False:
		Quote.GetCustomField('Line_Item_Detail_View').Content = 'No'
		Quote.SetGlobal('condview', 'No')
		Log.Info('unChecked')
	Quote.Save()
	
	Quote.Save()
	#Quote=QuoteHelper.Edit(quoteid.C4C_QUOTE_ID)
	#tableInfo = SqlHelper.GetTable("SAQDOC")
	recid = Product.Attr('QSTN_SYSEFL_QT_00001').GetValue()
	try:
		quote = recid
		language = "FPM DOC,"+str(userId)+","+str(userName)
		CQDOCIFLOW.docgeneration(quote,language,quote_revision_record_id)
		
	except:
		
		Log.Info("EXCEPT english doc")

def attachments():
	secstr = ""
	secstr += '<div class="row modulebnr brdr ma_mar_btm">UPLOAD ATTACHMENT <button type="button" class="close flt_rt" onclick="closepopup_scrl()" data-dismiss="modal">X</button></div><div class="col-md-12 padlftrhtnone"><div class="row pad-10 bg-lt-wt brdr" id="seginnerbnr"><img style="height:40px;margin-top:-1px;margin-left:-1px;float:left" src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/Secondary Icon.svg"><div class="product_txt_div_child secondary_highlight" style="display:block;text-align:left"><div class="product_txt_child"><abbr title="Key">Upload Attachment</abbr></div><div class="product_txt_to_top_child"><abbr title="ALL">Please click on the file upload icon to add an attachment to your quote revision...</abbr></div></div></div></div><div style="padding-left:0!important;padding-right:5px!important" class="col-md-12 col-sm-12 col-xs-12 section_row_fld opport_info trans_hide enable_custom_fld transaction_summary_new quote_summary collapse in upload_attachment"><div class="col-md-5 col-sm-6 col-xs-12 property_label section_cust_fld_txt"><label style="display:inline-block">Attachment File Name</label></div><div class="col-md-7 col-sm-6 col-xs-12 property_value section_cust_fld_val"><div class="col-md-2"><span class="hint_icon_req"><i class="fa fa-info-circle autoClosePopover"></i></span> <span class="required" style="display:none;">*</span></div><div class="col-md-9"><div id="divDocAttachement"></div>   <label class="upload_attachment_label"><img class="upload_icon" src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/document_upload_icon.svg" width="20px"> <input class="upload_icon_file" type="file" id="my_file" style="display:none;" value="test.pdf" oninput="OnChangeAttachFile()"></label></div><div class="col-md-1"><i class="fa fa-pencil" aria-hidden="true" style="font-size:13px;float:right;color:#cccaca!important"></i></div></div></div><div class="modal-footer col-md-12"><button type="button" class="btnconfig" data-dismiss="modal" onclick="closepopup_scrl()">CANCEL</button> <button type="button" id="add-offerings" class="btnconfig" onclick="Saveattachfile()" data-dismiss="modal">SAVE</button></div><script>$(document).ready(function() { console.log("inside script tag");$(".upload_icon_file").change(function(){var i=document.getElementById("my_file").files[0].name;$("#input_file").val(i);}); });</script>'

	return secstr

def SaveAttachments():
	FileFormat = DocumentName.split(".")[1]
	getrevdetails = Sql.GetFirst("SELECT QUOTE_ID,QTEREV_ID FROM SAQTRV WHERE QUOTE_REVISION_RECORD_ID = '{rec_id}' ".format(rec_id=Quote.GetGlobal("quote_revision_record_id")))
	Sql.RunQuery("INSERT INTO SAQRAT(QUOTE_REV_ATTACHMENT_RECORD_ID,ATTACH_FILE_FORMAT,ATTACH_FILE_NAME,ATTACH_FILE_PATH,ATTACH_TYPE,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_ID,QTEREV_RECORD_ID) VALUES (CONVERT(VARCHAR(4000), NEWID()),'{}','{}','{}','{}','{}','{}','{}','{}')".format(FileFormat,DocumentName,"",FileFormat,getrevdetails.QUOTE_ID,Quote.GetGlobal("contract_quote_record_id"),getrevdetails.QTEREV_ID,Quote.GetGlobal("quote_revision_record_id")))		
	Trace.Write("Save Success")
	return ""
	
try:
	RECORD_ID=Param.RECORD_ID
except:
	RECORD_ID = ""
try:
	ObjectName=Param.ObjectName
except:
	ObjectName = ""
try:
	QT_DWD=Param.QT_DWD
except:
	QT_DWD = ""
	
try:
	Language = Param.Language_selection
except:
	Language = ""
try:
	attach = Param.ATTACH
except:
	attach = ""
try:
	save = Param.SAVE
except:
	save = ""
try:
	save = Param.SAVE
except:
	save = ""
try:
	DocumentName = Param.DOCUMENT_NAME
except:
	DocumentName = ""
try:
	quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
except:
	quote_revision_record_id = ""
try:
	recid = Product.Attr('QSTN_SYSEFL_QT_00001').GetValue()
	quoteid = SqlHelper.GetFirst("SELECT QUOTE_TYPE FROM SAQTMT(NOLOCK) WHERE MASTER_TABLE_QUOTE_RECORD_ID =  '"+str(recid)+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id) + "'")
except:
	pass




if attach == "YES":
	ApiResponse = ApiResponseFactory.JsonResponse(attachments())
if save == "YES" and DocumentName != "":
	ApiResponse = ApiResponseFactory.JsonResponse(SaveAttachments())
if Language == "English" and quoteid.QUOTE_TYPE != 'ZWK1 - SPARES':
	english_doc()
elif Language == "English" and quoteid.QUOTE_TYPE == 'ZWK1 - SPARES':
	fpm_doc()
elif Language == "Chinese":
	chinese_doc()

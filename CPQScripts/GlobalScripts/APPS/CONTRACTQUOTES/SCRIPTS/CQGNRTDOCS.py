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
userId = str(User.Id)
userName = str(User.UserName)

tableInfo = SqlHelper.GetTable("SAQDOC")
recid = Product.Attr('QSTN_SYSEFL_QT_00001').GetValue()
try:
	quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
except:
	quote_revision_record_id = ""

quoteid = SqlHelper.GetFirst("SELECT QUOTE_ID, QUOTE_NAME,C4C_QUOTE_ID FROM SAQTMT(NOLOCK) WHERE MASTER_TABLE_QUOTE_RECORD_ID =  '"+str(recid)+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id) + "'")


audit_fields = SqlHelper.GetFirst("SELECT USERS.USERNAME,SAQDOC.CpqTableEntryDateModified,SAQDOC.CPQTABLEENTRYDATEADDED,SAQDOC.CPQTABLEENTRYADDEDBY,SAQDOC.CpqTableEntryModifiedBy from USERS inner join SAQDOC(NOLOCK)  on SAQDOC.CpqTableEntryModifiedBy = USERS.ID  ")

Log.Info('16-------spare quote---'+str(recid))
extline_pri = 0.00
QuoteproductTotals = Quote.QuoteTables["SAQITM"]

for i in QuoteproductTotals.Rows:
	Log.Info('38--extline_pri---SAQITM---'+str(extline_pri))
	extline_pri += float(i['EXTENDED_UNIT_PRICE'])
	Quote.SetGlobal('SubtotalLineItems', str(extline_pri))
Quote.GetCustomField('SubtotalLineItems').Content = str(extline_pri)
Log.Info('52--extline_pri------'+str(extline_pri))



extitm_price = extd_pr =  taxtotal = 0.00
'''QuoteproductTotalsTM = Quote.QuoteTables["SAQITM"]
#Log.Info('50----QuoteproductTotalsTM----'+str(QuoteproductTotalsTM.Rows.Count))
for i in QuoteproductTotalsTM.Rows:
	Log.Info('16---spare quote-SAQITM----UNIT_PRICE entry--'+i['EXTENDED_PRICE'])
	extd_pr += float(i['EXTENDED_UNIT_PRICE'])
	extitm_price += float(i['EXTENDED_UNIT_PRICE'] +(i['TAX']))
	Quote.SetGlobal('SubitemTools', str(extitm_price))
	Quote.SetGlobal('SubitemextTools', str(extd_pr))
Quote.GetCustomField('SubtotalTools').Content = str(extitm_price)
#Log.Info('64--vextitm_price-----'+str(extitm_price))'''
getdynamicrcords = SqlHelper.GetList("Select EXTENDED_UNIT_PRICE,TAX from QT__SAQITM where QUOTE_RECORD_ID = '"+str(recid)+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id) + "'")
for i in getdynamicrcords:
	Log.Info('16---spare quote-SAQITM----UNIT_PRICE entry--')
	extd_pr += float(i.EXTENDED_UNIT_PRICE)
	extitm_price += float(i.EXTENDED_UNIT_PRICE)
	taxtotal += float(i.TAX)
	Quote.SetGlobal('SubitemTools', str(extitm_price))
	Quote.SetGlobal('SubitemextTools', str(extd_pr))
	Quote.SetGlobal('taxtotal', str(taxtotal))
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
'''QuoteproductTotalsfp = Quote.QuoteTables["SAQIFP"]
Log.Info('50------QuoteproductTotalsfp----'+str(QuoteproductTotalsfp.Rows.Count))

for i in QuoteproductTotalsfp.Rows:'''
getdynamicrcords = SqlHelper.GetList("Select * from QT__SAQIFP where QUOTE_RECORD_ID = '"+str(recid)+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id) + "'")
for val in getdynamicrcords:
	Log.Info('16---spare quote--UNIT_PRICE entry--')
	extt_price += float(val.UNIT_PRICE)
	fptotal += float(val.EXTENDED_UNIT_PRICE)
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
recid = Product.Attr('QSTN_SYSEFL_QT_00001').GetValue()


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
	
Language = Param.Language_selection
try:
	quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
except:
	quote_revision_record_id = ""
recid = Product.Attr('QSTN_SYSEFL_QT_00001').GetValue()

quoteid = SqlHelper.GetFirst("SELECT QUOTE_TYPE FROM SAQTMT(NOLOCK) WHERE MASTER_TABLE_QUOTE_RECORD_ID =  '"+str(recid)+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id) + "'")



if Language == "English" and quoteid.QUOTE_TYPE != 'ZWK1 - SPARES':
	english_doc()
elif Language == "English" and quoteid.QUOTE_TYPE == 'ZWK1 - SPARES':
	fpm_doc()
elif Language == "Chinese":
	chinese_doc()

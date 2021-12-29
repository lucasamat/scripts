#========================================================================================================#================================
#   __script_name : CQIFWUDQTM.PY
#   __script_description : THIS SCRIPT USED TO UPDATE QUOTE ITEMS AND QUOTE LINE ITEMS 
#   __primary_author__ : WASIM
#   __create_date :24-08-2021
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================

import datetime
import Webcom.Configurator.Scripting.Test.TestProduct
import sys
import re
import System.Net
import SYCNGEGUID as CPQID
from SYDATABASE import SQL
Sql = SQL()
ScriptExecutor = ScriptExecutor
#Log.Info('quote_revision_record_id- '+str(quote_revision_record_id))
def quoteiteminsert(Qt_id):
	#quote_number = Qt_id[2:12]
	Log.Info('quote_id---'+str(Qt_id))
	#quote_Edit = QuoteHelper.Edit(Qt_id)
	#get_curr = str(Quote.GetCustomField('Currency').Content)
	# total_cost = 0.00
	# total_target_price = 0.00
	# total_ceiling_price = 0.00
	# total_sls_discount_price = 0.00
	# total_bd_margin = 0.00
	# total_bd_price = 0.00
	# total_sales_price = 0.00
	# total_yoy = 0.00
	# total_year_1 = 0.00
	# total_year_2 = 0.00
	# total_year_3 = 0.00
	# total_year_4 = 0.00
	# total_year_5 = 0.00
	# total_tax = 0.00
	# total_extended_price = 0.00
	# total_model_price = 0.00
	# items_data = {}
	
	get_rev_rec_id = Sql.GetFirst("SELECT QTEREV_RECORD_ID,QUOTE_CURRENCY,MASTER_TABLE_QUOTE_RECORD_ID FROM SAQTMT where QUOTE_ID = '{}'".format(Qt_id))
	get_exch_rate = Sql.GetFirst("SELECT * FROM SAQTRV where QUOTE_ID = '{}' AND QUOTE_REVISION_RECORD_ID = '{}'".format(Qt_id,get_rev_rec_id.QTEREV_RECORD_ID))
	# get_curr = get_rev_rec_id.QUOTE_CURRENCY
	# items_obj = Sql.GetList("SELECT SERVICE_ID, LINE,ISNULL(TOTAL_COST_WOSEEDSTOCK, 0) as TOTAL_COST,ISNULL(TARGET_PRICE, 0) as TARGET_PRICE, ISNULL(MODEL_PRICE, 0) as MODEL_PRICE, ISNULL(CEILING_PRICE, 0) as CEILING_PRICE, ISNULL(SALES_DISCOUNT_PRICE, 0) as SALES_DISCOUNT_PRICE, ISNULL(BD_PRICE, 0) as BD_PRICE,ISNULL(BD_PRICE_MARGIN, 0) as BD_PRICE_MARGIN, ISNULL(NET_PRICE, 0) as NET_PRICE, ISNULL(YEAR_1, 0) as YEAR_1,ISNULL(YEAR_2, 0) as YEAR_2, ISNULL(YEAR_3, 0) as YEAR_3,ISNULL(YEAR_4, 0) as YEAR_4, ISNULL(YEAR_5, 0) as YEAR_5, CURRENCY, ISNULL(YEAR_OVER_YEAR, 0) as YEAR_OVER_YEAR, ISNULL(NET_VALUE, 0) as NET_VALUE, OBJECT_QUANTITY FROM SAQITM (NOLOCK) WHERE QUOTE_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(Qt_id,get_rev_rec_id.QTEREV_RECORD_ID))
	# if items_obj:
	# 	for item_obj in items_obj:
	# 		items_data[int(float(item_obj.LINE))] = {'TOTAL_COST':item_obj.TOTAL_COST, 'TARGET_PRICE':item_obj.TARGET_PRICE, 'SERVICE_ID':(item_obj.SERVICE_ID.replace('- BASE', '')).strip(), 'YEAR_1':item_obj.YEAR_1, 'YEAR_2':item_obj.YEAR_2, 'YEAR_3':item_obj.YEAR_3, 'YEAR_4':item_obj.YEAR_4, 'YEAR_5':item_obj.YEAR_5, 'YEAR_OVER_YEAR':item_obj.YEAR_OVER_YEAR, 'OBJECT_QUANTITY':item_obj.OBJECT_QUANTITY, 'MODEL_PRICE':item_obj.MODEL_PRICE, 'CEILING_PRICE':item_obj.CEILING_PRICE, 'SALES_DISCOUNT_PRICE':item_obj.SALES_DISCOUNT_PRICE, 'BD_PRICE':item_obj.BD_PRICE, 'NET_PRICE':item_obj.NET_PRICE, 'BD_PRICE_MARGIN':item_obj.BD_PRICE_MARGIN, 'NET_VALUE' :item_obj.NET_VALUE}
	# quote_Edit = QuoteHelper.Edit(Qt_id)
	# for item in Quote.MainItems:
	# 	item_number = int(item.RolledUpQuoteItem)
	# 	if item_number in items_data.keys():
	# 		if items_data.get(item_number).get('SERVICE_ID') == item.PartNumber:
	# 			item_data = items_data.get(item_number)
	# 			item.TOTAL_COST.Value = float(item_data.get('TOTAL_COST'))					
	# 			total_cost += float(item_data.get('TOTAL_COST'))
	# 			item.TARGET_PRICE.Value = item_data.get('TARGET_PRICE')
				
	# 			item.MODEL_PRICE.Value = item_data.get('MODEL_PRICE')
	# 			item.CEILING_PRICE.Value = item_data.get('CEILING_PRICE')
	# 			item.SALES_DISCOUNT_PRICE.Value = item_data.get('SALES_DISCOUNT_PRICE')
	# 			item.BD_PRICE.Value = item_data.get('BD_PRICE')
	# 			item.NET_PRICE.Value = item_data.get('NET_PRICE')
	# 			item.BD_PRICE_MARGIN.Value = item_data.get('BD_PRICE_MARGIN')

	# 			total_target_price += item.TARGET_PRICE.Value
	# 			total_ceiling_price += item.CEILING_PRICE.Value
	# 			total_sls_discount_price += item.SALES_DISCOUNT_PRICE.Value
	# 			total_bd_margin += item.BD_PRICE_MARGIN.Value
	# 			total_bd_price += item.BD_PRICE.Value
	# 			total_model_price += item.MODEL_PRICE.Value
	# 			total_sales_price += item.NET_PRICE.Value
	# 			item.YEAR_OVER_YEAR.Value = item_data.get('YEAR_OVER_YEAR')
	# 			total_yoy += item.YEAR_OVER_YEAR.Value
	# 			item.YEAR_1.Value = item_data.get('YEAR_1')
	# 			total_year_1 += item.YEAR_1.Value
	# 			item.YEAR_2.Value = item_data.get('YEAR_2')
	# 			total_year_2 += item.YEAR_2.Value
	# 			item.YEAR_3.Value = item_data.get('YEAR_3')
	# 			total_year_3 += item.YEAR_3.Value
	# 			item.YEAR_4.Value = item_data.get('YEAR_4')
	# 			total_year_4 += item.YEAR_4.Value
	# 			item.YEAR_5.Value = item_data.get('YEAR_5')
	# 			total_year_5 += item.YEAR_5.Value
	# 			total_tax += item.TAX.Value
	# 			item.NET_VALUE.Value = item_data.get('NET_VALUE')
	# 			total_extended_price += item.NET_VALUE.Value	
	# 			item.OBJECT_QUANTITY.Value = item_data.get('OBJECT_QUANTITY')
	

	# 			Log.Info('SALES_DISCOUNT_PRICE--'+str(item.SALES_DISCOUNT_PRICE.Value))
	# ##controlling decimal based on currency
	# if get_curr:
	# 	get_decimal_place = Sql.GetFirst("SELECT * FROM PRCURR (NOLOCK) WHERE CURRENCY ='{}'".format(get_curr))
	# 	if get_decimal_place:
	# 		decimal_value = get_decimal_place.DISPLAY_DECIMAL_PLACES
	# 		formatting_string = "{0:." + str(decimal_value) + "f}"
			
	# 		total_cost =formatting_string.format(total_cost)
	# 		total_target_price =formatting_string.format(total_target_price)
	# 		total_ceiling_price =formatting_string.format(total_ceiling_price)
	# 		total_sls_discount_price =formatting_string.format(total_sls_discount_price)
	# 		total_sales_price =formatting_string.format(total_sales_price)
	# 		total_year_1 =formatting_string.format(total_year_1)
	# 		total_year_2 =formatting_string.format(total_year_2)
	# 		total_year_3 =formatting_string.format(total_year_3)
	# 		total_year_4 =formatting_string.format(total_year_4)
	# 		total_year_5 =formatting_string.format(total_year_5)
	# 		total_tax =formatting_string.format(total_tax)
	# 		total_extended_price =formatting_string.format(total_extended_price)
	# 		total_model_price =formatting_string.format(total_model_price)
	# 		total_bd_price =formatting_string.format(total_bd_price)


	# Quote.GetCustomField('TOTAL_COST').Content = str(total_cost) + " " + get_curr
	# Quote.GetCustomField('TARGET_PRICE').Content = str(total_target_price) + " " + get_curr
	# Quote.GetCustomField('CEILING_PRICE').Content = str(total_ceiling_price) + " " + get_curr
	# Quote.GetCustomField('SALES_DISCOUNTED_PRICE').Content = str(total_sls_discount_price) + " " + get_curr
	# Quote.GetCustomField('BD_PRICE_MARGIN').Content =str(total_bd_margin) + " %"
	# Quote.GetCustomField('BD_PRICE_DISCOUNT').Content = str(total_bd_price) + " %"
	# Quote.GetCustomField('TOTAL_NET_PRICE').Content =str(total_sales_price) + " " + get_curr
	# Quote.GetCustomField('YEAR_OVER_YEAR').Content =str(total_yoy) + " %"
	# Quote.GetCustomField('YEAR_1').Content = str(total_year_1) + " " + get_curr
	# Quote.GetCustomField('YEAR_2').Content = str(total_year_2) + " " + get_curr
	# Quote.GetCustomField('YEAR_3').Content = str(total_year_3) + " " + get_curr
	# Quote.GetCustomField('TAX').Content = str(total_tax) + " " + get_curr
	# Quote.GetCustomField('TOTAL_NET_VALUE').Content = str(total_extended_price) + " " + get_curr
	
	# Quote.GetCustomField('MODEL_PRICE').Content = str(total_model_price) + " " + get_curr
	# Quote.GetCustomField('BD_PRICE').Content = str(total_bd_price) + " " + get_curr
	
	

	#Quote.Save()
	get_exch_rate = get_exch_rate.EXCHANGE_RATE
	# Sql.RunQuery("""UPDATE SAQRIT 
	# 			SET NET_VALUE = NET_PRICE + ISNULL(TAX_AMOUNT, 0) 
	# 			FROM SAQRIT (NOLOCK)
	# 				WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID='{rev}' """.format(QuoteRecordId=get_rev_rec_id.MASTER_TABLE_QUOTE_RECORD_ID,rev =get_rev_rec_id.QTEREV_RECORD_ID ))
	# Sql.RunQuery("""UPDATE SAQRIT 
	# 	SET NET_PRICE_INGL_CURR = NET_PRICE*"""+str(get_exch_rate)+""" , 
	# 	NET_VALUE_INGL_CURR = NET_VALUE*"""+str(get_exch_rate)+""",
	# 	UNIT_PRICE_INGL_CURR =  UNIT_PRICE*"""+str(get_exch_rate)+"""
	# 	FROM SAQRIT (NOLOCK)
	# 		WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID='{rev}' """.format(QuoteRecordId=get_rev_rec_id.MASTER_TABLE_QUOTE_RECORD_ID, rev =get_rev_rec_id.QTEREV_RECORD_ID))
	
	
	##updating saqris
	Sql.RunQuery("""UPDATE SAQRIS 
							SET UNIT_PRICE_INGL_CURR = IQ.UNIT_PRICE_INGL_CURR, 
							NET_PRICE_INGL_CURR=IQ.NET_PRICE_INGL_CURR,
							UNIT_PRICE = IQ.UNIT_PRICE, 
							NET_PRICE=IQ.NET_PRICE, 
							NET_VALUE = IQ.NET_VALUE,
							NET_VALUE_INGL_CURR = IQ.NET_VALUE_INGL_CURR,
							ESTIMATED_VALUE = IQ.ESTIMATED_VALUE,
							COMMITTED_VALUE = IQ.COMMITTED_VALUE,
							TAX_AMOUNT_INGL_CURR = IQ.TAX_AMOUNT_INGL_CURR,
							TAX_AMOUNT = IQ.TAX_AMOUNT

							FROM SAQRIS 
								INNER JOIN (SELECT SAQRIT.QUOTE_RECORD_ID, SAQRIT.QTEREV_RECORD_ID,SAQRIT.SERVICE_ID,
								SUM(ISNULL(SAQRIT.UNIT_PRICE_INGL_CURR, 0)) as UNIT_PRICE_INGL_CURR,
								SUM(ISNULL(SAQRIT.NET_PRICE_INGL_CURR, 0)) as NET_PRICE_INGL_CURR,
								SUM(ISNULL(SAQRIT.UNIT_PRICE, 0)) as UNIT_PRICE,
								SUM(ISNULL(SAQRIT.NET_PRICE, 0)) as NET_PRICE,
								SUM(ISNULL(SAQRIT.NET_VALUE, 0)) as NET_VALUE,
								SUM(ISNULL(SAQRIT.NET_VALUE_INGL_CURR, 0)) as NET_VALUE_INGL_CURR,
								SUM(ISNULL(SAQRIT.ESTIMATED_VALUE, 0)) as ESTIMATED_VALUE,
								SUM(ISNULL(SAQRIT.COMMITTED_VALUE, 0)) as COMMITTED_VALUE,
								SUM(ISNULL(SAQRIT.TAX_AMOUNT_INGL_CURR, 0)) as TAX_AMOUNT_INGL_CURR,
								SUM(ISNULL(SAQRIT.TAX_AMOUNT, 0)) as TAX_AMOUNT

								FROM SAQRIT 
								WHERE SAQRIT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRIT.QTEREV_RECORD_ID = '{rev}'  GROUP BY SAQRIT.QUOTE_RECORD_ID, SAQRIT.QTEREV_RECORD_ID,SAQRIT.SERVICE_ID) IQ ON SAQRIS.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND SAQRIS.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND SAQRIS.SERVICE_ID = IQ.SERVICE_ID
						WHERE SAQRIS.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRIS.QTEREV_RECORD_ID='{rev}' """.format( QuoteRecordId= get_rev_rec_id.MASTER_TABLE_QUOTE_RECORD_ID ,rev =get_rev_rec_id.QTEREV_RECORD_ID))
						
	##updating quote summary values in saqtrv
	get_saqtrv_price = Sql.GetFirst("SELECT * FROM SAQTRV WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID='{rev}'".format(QuoteRecordId=get_rev_rec_id.MASTER_TABLE_QUOTE_RECORD_ID,rev =get_rev_rec_id.QTEREV_RECORD_ID))
	net_price_ingl = 0
	net_value_ingl = 0
	tax_amt_ingl = 0
	#net_price = 0
	# if get_saqtrv_price:
	# 	if get_saqtrv_price.NET_PRICE_INGL_CURR:
	# 		net_price_ingl = get_saqtrv_price.NET_PRICE_INGL_CURR
	# 	if get_saqtrv_price.NET_VALUE_INGL_CURR:
	# 		net_value_ingl = get_saqtrv_price.NET_VALUE_INGL_CURR
	# 	if get_saqtrv_price.TAX_AMOUNT_INGL_CURR:
	# 		tax_amt_ingl = get_saqtrv_price.TAX_AMOUNT_INGL_CURR

	Sql.RunQuery("""UPDATE SAQTRV
						SET 
						SAQTRV.TAX_AMOUNT_INGL_CURR = IQ.TAX_AMOUNT_INGL_CURR,						
						SAQTRV.NET_PRICE_INGL_CURR = IQ.NET_PRICE_INGL_CURR,
						SAQTRV.NET_VALUE_INGL_CURR = IQ.NET_VALUE_INGL_CURR - IQ.TOTAL_CREDIT,
						SAQTRV.CREDIT_INGL_CURR	= IQ.TOTAL_CREDIT
									
						FROM SAQTRV (NOLOCK)
						INNER JOIN (SELECT SAQRIS.QUOTE_RECORD_ID, SAQRIS.QTEREV_RECORD_ID,
									SUM(ISNULL(SAQRIS.TAX_AMOUNT_INGL_CURR, 0)) as TAX_AMOUNT_INGL_CURR,
									SUM(ISNULL(SAQRIS.NET_PRICE_INGL_CURR, 0)) as NET_PRICE_INGL_CURR,
									SUM(ISNULL(SAQRIS.NET_PRICE, 0)) as NET_PRICE,
									SUM(ISNULL(SAQRIS.NET_VALUE, 0)) as NET_VALUE,
									SUM(ISNULL(SAQRIS.NET_VALUE_INGL_CURR, 0)) as NET_VALUE_INGL_CURR,
									SUM(ISNULL(SAQRIS.TAX_AMOUNT, 0)) as TAX_AMOUNT,
									CASE WHEN SERVICE_ID = 'Z0116' THEN ISNULL(SAQRIS.NET_PRICE_INGL_CURR, 0) ELSE 0 as TOTAL_CREDIT
									FROM SAQRIS (NOLOCK) WHERE SAQRIS.QUOTE_RECORD_ID = '{quote_rec_id}' AND SAQRIS.QTEREV_RECORD_ID = '{quote_revision_rec_id}' GROUP BY SAQRIS.QTEREV_RECORD_ID, SAQRIS.QUOTE_RECORD_ID) IQ ON SAQTRV.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND SAQTRV.QUOTE_REVISION_RECORD_ID = IQ.QTEREV_RECORD_ID
						WHERE SAQTRV.QUOTE_RECORD_ID = '{quote_rec_id}' AND SAQTRV.QUOTE_REVISION_RECORD_ID = '{quote_revision_rec_id}' 	""".format(quote_rec_id = get_rev_rec_id.MASTER_TABLE_QUOTE_RECORD_ID ,quote_revision_rec_id = get_rev_rec_id.QTEREV_RECORD_ID ) )

	# SUM(ISNULL(SAQITM.YEAR_1_INGL_CURR, 0)) as YEAR_1_INGL_CURR,
	# SUM(ISNULL(SAQITM.YEAR_2_INGL_CURR, 0)) as YEAR_2_INGL_CURR,
	# SUM(ISNULL(SAQITM.YEAR_3_INGL_CURR, 0)) as YEAR_3_INGL_CURR,
	# SUM(ISNULL(SAQITM.YEAR_4_INGL_CURR, 0)) as YEAR_4_INGL_CURR,
	# SUM(ISNULL(SAQITM.YEAR_5_INGL_CURR, 0)) as YEAR_5_INGL_CURR
	#updating value to quote summary ends

	return "True"
try: 
	Qt_id = Param.QT_REC_ID
except:
	Qt_id = ""

try:
	calling_function = quoteiteminsert(Qt_id)
except Exception as e:
	Log.Info('pricing error-'+str(e))

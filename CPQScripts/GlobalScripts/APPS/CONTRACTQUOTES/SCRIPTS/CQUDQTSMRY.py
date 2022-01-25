# =========================================================================================================================================
#   __script_name : CQUDQTSMRY.PY
#   __script_description : THIS SCRIPT IS USED TO UPDATE DISCOUNT IN QUOTE ITEM SUMMARY. CALCULATE ITEM AND LINE ITEM PRICES BASED ON DISCOUNT ENTERED.
#   __primary_author__ : AYYAPPAN SUBRAMANIYAN
#   __create_date :24-08-2021
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct
from SYDATABASE import SQL

Sql = SQL()


class ContractQuoteSummaryUpdate:
	def __init__(self, discount=0):
		if "+" not in discount and "-" not in discount:
			self.discount = discount
		else:
			if "+" in discount:
				self.discount = str(discount).replace("+","").replace("%","").strip()
			elif "-" in discount:
				self.discount = str(discount).replace("-","").replace("%","").strip()
		try:
			self.contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
		except Exception:
			self.contract_quote_record_id = ''
		try:
			self.quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
		except:
			self.quote_revision_record_id = ''
	
	def _update_year(self):
		for count in range(2, 6):
			Sql.RunQuery("""UPDATE SAQICO SET
											SAQICO.YEAR_{Year} = CASE  
												WHEN CAST(DATEDIFF(day,SAQTMT.CONTRACT_VALID_FROM,SAQTMT.CONTRACT_VALID_TO) / 365.2425 AS INT) >= {Count} 
													THEN ISNULL(SAQICO.YEAR_{Count}, 0) - (ISNULL(SAQICO.YEAR_{Count}, 0) * ISNULL(SAQICO.YEAR_OVER_YEAR, 0))/100.0                                                   
												ELSE 0
											END
										FROM SAQICO (NOLOCK) 
										JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQICO.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = SAQICO.QTEREV_RECORD_ID
										WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{RevisionRecordId}'""".format(
											QuoteRecordId=self.contract_quote_record_id,
											RevisionRecordId=self.quote_revision_record_id,
											Year=count,
											Count=count - 1 
											)
						)    
	
	def _quote_item_lines_update(self):
		decimal_discount = float(int(self.discount)) / 100.0
		# Sql.RunQuery("""UPDATE SAQICO SET
		# 								DISCOUNT = {Discount}
		# 							FROM SAQICO (NOLOCK)                                     
		# 							WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'""".format(
		# 								QuoteRecordId=self.contract_quote_record_id,
		# 								RevisionRecordId=self.quote_revision_record_id,
		# 								DecimalDiscount=decimal_discount if decimal_discount > 0 else 1,
		# 								Discount=self.discount)
		# 			)
		# Update Year2 to Year5 - Start
	#COMMENTING since NET_VALUE IS REMOVED FROM SAQICO
	#	self._update_year()
		# Update Year2 to Year5 - End
	#	Sql.RunQuery("""UPDATE SAQICO SET 
	#									NET_VALUE = ISNULL(YEAR_1,0) + ISNULL(YEAR_2,0) + ISNULL(YEAR_3,0) + ISNULL(YEAR_4,0) + ISNULL(YEAR_5,0)
	#								FROM SAQICO (NOLOCK)                                     
	#								WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'""".format(
	#									QuoteRecordId=self.contract_quote_record_id,
	#									RevisionRecordId=self.quote_revision_record_id 
										)
					)
	
	# def _quote_item_update(self):
	# 	Sql.RunQuery("""UPDATE SAQITM
	# 						SET 
	# 						NET_VALUE = IQ.NET_VALUE,
	# 						NET_PRICE = IQ.NET_PRICE,
	# 						YEAR_1 = IQ.YEAR_1,
	# 						YEAR_2 = IQ.YEAR_2,
	# 						YEAR_3 = IQ.YEAR_3,
	# 						YEAR_4 = IQ.YEAR_4,
	# 						YEAR_5 = IQ.YEAR_5,
	# 						DISCOUNT = {Discount}							
	# 						FROM SAQITM (NOLOCK)
	# 						INNER JOIN (SELECT SAQITM.CpqTableEntryId,
	# 									CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.NET_VALUE, 0)), 0), 0) as decimal(18,2)) as NET_VALUE,
	# 									CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.NET_PRICE, 0)), 0), 0) as decimal(18,2)) as NET_PRICE,
	# 									CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_1, 0)), 0), 0) as decimal(18,2)) as YEAR_1,
	# 									CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_2, 0)), 0), 0) as decimal(18,2)) as YEAR_2,
	# 									CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_3, 0)), 0), 0) as decimal(18,2)) as YEAR_3,
	# 									CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_4, 0)), 0), 0) as decimal(18,2)) as YEAR_4,
	# 									CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_5, 0)), 0), 0) as decimal(18,2)) as YEAR_5
	# 									FROM SAQITM (NOLOCK) 
	# 									JOIN SAQICO (NOLOCK) ON SAQICO.QUOTE_RECORD_ID = SAQITM.QUOTE_RECORD_ID AND SAQICO.LINE_ITEM_ID = SAQITM.LINE_ITEM_ID
	# 									WHERE SAQITM.QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'
	# 									GROUP BY SAQITM.LINE_ITEM_ID, SAQITM.QUOTE_RECORD_ID, SAQITM.CpqTableEntryId)IQ
	# 						ON SAQITM.CpqTableEntryId = IQ.CpqTableEntryId 
	# 						WHERE SAQITM.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQITM.QTEREV_RECORD_ID = '{RevisionRecordId}' """.format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id,
	# 						Discount=self.discount))
	
	def _update_quote_summary(self):
		quote_currency = str(Quote.GetCustomField('Currency').Content)		
		total_net_price = 0.00		
		total_year_1 = 0.00
		total_year_2 = 0.00
		total_year_3 = 0.00       
		total_year_4 = 0.00 
		total_year_5 = 0.00  
		total_net_value = 0.00
		items_data = {}
		
		# items_obj = Sql.GetList("SELECT SERVICE_ID, LINE_ITEM_ID, ISNULL(YEAR_1, 0) as YEAR_1 ,ISNULL(YEAR_2, 0) as YEAR_2 ,ISNULL(YEAR_3, 0) as YEAR_3,ISNULL(YEAR_4, 0) as YEAR_4,ISNULL(YEAR_5, 0) as YEAR_5, ISNULL(NET_VALUE,0) AS NET_VALUE, ISNULL(NET_PRICE, 0) as NET_PRICE FROM SAQITM (NOLOCK) WHERE QUOTE_RECORD_ID = '{}'".format(self.contract_quote_record_id))
		# if items_obj:
		# 	for item_obj in items_obj:
		# 		items_data[int(float(item_obj.LINE_ITEM_ID))] = {'NET_VALUE':item_obj.NET_VALUE, 'SERVICE_ID':(item_obj.SERVICE_ID.replace('- BASE', '')).strip(), 'YEAR_1':item_obj.YEAR_1, 'YEAR_2':item_obj.YEAR_2, 'YEAR_3':item_obj.YEAR_3, 'YEAR_4':item_obj.YEAR_4, 'YEAR_5':item_obj.YEAR_5, 'NET_PRICE':item_obj.NET_PRICE}
		for item in Quote.MainItems:
			item_number = int(item.RolledUpQuoteItem)
			if item_number in items_data.keys():
				if items_data.get(item_number).get('SERVICE_ID') == item.PartNumber:
					item_data = items_data.get(item_number)
					item.NET_PRICE.Value = float(item_data.get('NET_PRICE'))
					total_net_price += item.NET_PRICE.Value
					item.NET_VALUE.Value = item_data.get('NET_VALUE')
					total_net_value += item.NET_VALUE.Value	
					item.YEAR_1.Value = item_data.get('YEAR_1')
					total_year_1 += item.YEAR_1.Value
					item.YEAR_2.Value = item_data.get('YEAR_2')
					total_year_2 += item.YEAR_2.Value
					item.YEAR_3.Value = item_data.get('YEAR_3')
					total_year_3 += item.YEAR_3.Value 
					item.YEAR_4.Value = item_data.get('YEAR_4')
					total_year_4 += item.YEAR_4.Value 
					item.YEAR_5.Value = item_data.get('YEAR_5')
					total_year_5 += item.YEAR_5.Value
					item.DISCOUNT.Value = str(self.discount)
		##Added the percentage symbol for discount custom field...
		Percentage = '%'
		Quote.GetCustomField('DISCOUNT').Content = str(self.discount)+ " " + Percentage
		#discount_value = Quote.GetCustomField('DISCOUNT').Content
		#Trace.Write("discount"+str(discount_value))
		# Quote.GetCustomField('TOTAL_NET_PRICE').Content =str(total_net_price) + " " + quote_currency
		# Quote.GetCustomField('YEAR_1').Content = str(total_year_1) + " " + quote_currency
		# Quote.GetCustomField('YEAR_2').Content = str(total_year_2) + " " + quote_currency    
		# Quote.GetCustomField('YEAR_3').Content = str(total_year_3) + " " + quote_currency     
		# Quote.GetCustomField('TOTAL_NET_VALUE').Content = str(total_net_value) + " " + quote_currency
		Quote.Save()
		Sql.RunQuery("""UPDATE SAQTRV
						SET 									
						SAQTRV.NET_PRICE_INGL_CURR = IQ.NET_PRICE_INGL_CURR,					
						SAQTRV.DISCOUNT_PERCENT = '{discount}'
						
						FROM SAQTRV (NOLOCK)
						INNER JOIN (SELECT SAQRIT.QUOTE_RECORD_ID, SAQRIT.QTEREV_RECORD_ID,
									SUM(ISNULL(SAQRIT.NET_PRICE_INGL_CURR, 0)) as NET_PRICE_INGL_CURR								
									FROM SAQRIT (NOLOCK) WHERE SAQRIT.QUOTE_RECORD_ID = '{quote_rec_id}' AND SAQRIT.QTEREV_RECORD_ID = '{quote_revision_rec_id}') IQ ON SAQTRV.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND SAQTRV.QUOTE_REVISION_RECORD_ID = IQ.QTEREV_RECORD_ID
						WHERE SAQTRV.QUOTE_RECORD_ID = '{quote_rec_id}' AND SAQTRV.QUOTE_REVISION_RECORD_ID = '{quote_revision_rec_id}' 	""".format(discount = str(self.discount), quote_rec_id = self.contract_quote_record_id, quote_revision_rec_id = self.quote_revision_record_id ) )

	def update_summary(self):
		if self.contract_quote_record_id:
			self._quote_item_lines_update()
			# self._quote_item_update()
			self._update_quote_summary()
	def CalculatePlusDiscount(self):
		Trace.Write("Plus")
		decimal_discount = float(self.discount) / 100.0
		Sql.RunQuery("""UPDATE SAQICO SET										
										SALES_PRICE_INGL_CURR = ISNULL(TARGET_PRICE_INGL_CURR,0) + (ISNULL(TARGET_PRICE_INGL_CURR,0) * {DecimalDiscount}),									
										DISCOUNT_AMOUNT_INGL_CURR = ISNULL(TARGET_PRICE_INGL_CURR,0)  - ISNULL(SALES_PRICE_INGL_CURR,0),
										NET_PRICE = '',
										NET_PRICE_INGL_CURR = '',
									FROM SAQICO (NOLOCK)                                     
									WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'""".format(
										QuoteRecordId=self.contract_quote_record_id,
										RevisionRecordId=self.quote_revision_record_id,
										DecimalDiscount=decimal_discount if decimal_discount > 0 else 1))

		# Sql.RunQuery("""UPDATE SAQICO SET 
		# 								NET_PRICE = ISNULL(TARGET_PRICE,0) - (ISNULL(TARGET_PRICE,0) * {DecimalDiscount}),
		# 								NET_PRICE_INGL_CURR = ISNULL(TARGET_PRICE_INGL_CURR,0) - (ISNULL(TARGET_PRICE_INGL_CURR,0) * {DecimalDiscount}),
		# 								YEAR_1 = ISNULL(TARGET_PRICE,0) - (ISNULL(TARGET_PRICE,0) * {DecimalDiscount}),
		# 								YEAR_1_INGL_CURR = ISNULL(TARGET_PRICE_INGL_CURR,0) - (ISNULL(TARGET_PRICE_INGL_CURR,0) * {DecimalDiscount}),
		# 								DISCOUNT = '{Discount}'
		# 							FROM SAQICO (NOLOCK)                                     
		# 							WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'""".format(
		# 								QuoteRecordId=self.contract_quote_record_id,
		# 								RevisionRecordId=self.quote_revision_record_id,
		# 								DecimalDiscount=decimal_discount if decimal_discount > 0 else 1,
		# 								Discount=self.discount,
		# 								plus="+"))
		self._update_year()
		Sql.RunQuery("""UPDATE SAQIRT
							SET							
							SALES_PRICE_INGL_CURR = IQ.SALES_PRICE_INGL_CURR,							
							DISCOUNT_AMOUNT_INGL_CURR = IQ.DISCOUNT_AMOUNT_INGL_CURR,
							NET_PRICE_INGL_CURR = IQ.NET_PRICE_INGL_CURR,
							DISCOUNT = '{Discount}'					
							FROM SAQIRT (NOLOCK)
							INNER JOIN (SELECT SAQIRT.CpqTableEntryId,										
										CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.SALES_PRICE_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as SALES_PRICE_INGL_CURR,										
										CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.DISCOUNT_AMOUNT_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as DISCOUNT_AMOUNT_INGL_CURR,
										CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.NET_PRICE_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as NET_PRICE_INGL_CURR
										FROM SAQIRT (NOLOCK) 
										JOIN SAQICO (NOLOCK) ON SAQICO.QUOTE_RECORD_ID = SAQIRT.QUOTE_RECORD_ID  AND SAQICO.QTEREV_RECORD_ID = SAQIRT.QTEREV_RECORD_ID 
										WHERE SAQIRT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQIRT.QTEREV_RECORD_ID = '{RevisionRecordId}'
										GROUP BY SAQIRT.LINE_ITEM_ID, SAQIRT.QUOTE_RECORD_ID, SAQIRT.CpqTableEntryId,SAQIRT.QTEREV_RECORD_ID)IQ
							ON SAQIRT.CpqTableEntryId = IQ.CpqTableEntryId 
							WHERE SAQIRT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQIRT.QTEREV_RECORD_ID = '{RevisionRecordId}' """.format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id,
							Discount=self.discount,plus="+"))
		# Sql.RunQuery("""UPDATE SAQICO SET 
		# 								NET_VALUE = ISNULL(YEAR_1,0) + ISNULL(YEAR_2,0) + ISNULL(YEAR_3,0) + ISNULL(YEAR_4,0) + ISNULL(YEAR_5,0),
		# 								NET_VALUE_INGL_CURR = ISNULL(YEAR_1_INGL_CURR,0) + ISNULL(YEAR_2_INGL_CURR,0) + ISNULL(YEAR_3_INGL_CURR,0) + ISNULL(YEAR_4_INGL_CURR,0) + ISNULL(YEAR_5_INGL_CURR,0)
		# 							FROM SAQICO (NOLOCK)                                     
		# 							WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'""".format(
		# 								QuoteRecordId=self.contract_quote_record_id,
		# 								RevisionRecordId=self.quote_revision_record_id 
		# 								))
		# Sql.RunQuery("""UPDATE SAQIFL
		# 	SET 
		# 	NET_VALUE = IQ.NET_VALUE,
		# 	NET_PRICE = IQ.NET_PRICE,
		# 	YEAR_1 = IQ.YEAR_1,
		# 	YEAR_2 = IQ.YEAR_2,
		# 	YEAR_3 = IQ.YEAR_3,
		# 	YEAR_4 = IQ.YEAR_4,
		# 	YEAR_5 = IQ.YEAR_5,
		# 	NET_VALUE_INGL_CURR = IQ.NET_VALUE_INGL_CURR,
		# 	NET_PRICE_INGL_CURR = IQ.NET_PRICE_INGL_CURR,
		# 	YEAR_1_INGL_CURR = IQ.YEAR_1_INGL_CURR,
		# 	YEAR_2_INGL_CURR = IQ.YEAR_2_INGL_CURR,
		# 	YEAR_3_INGL_CURR = IQ.YEAR_3_INGL_CURR,
		# 	YEAR_4_INGL_CURR = IQ.YEAR_4_INGL_CURR,
		# 	YEAR_5_INGL_CURR = IQ.YEAR_5_INGL_CURR,
		# 	DISCOUNT_AMOUNT_INGL_CURR = IQ.DISCOUNT_AMOUNT_INGL_CURR,
		# 	DISCOUNT = '{Discount}'					
		# 	FROM  SAQIFL SAQICO (NOLOCK)
		# 	INNER JOIN (SELECT FABLOCATION_ID, SERVICE_ID,QTEREV_RECORD_ID,QUOTE_RECORD_ID,
		# 				CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.NET_VALUE, 0)), 0), 0) as decimal(18,2)) as NET_VALUE,
		# 				CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.NET_PRICE, 0)), 0), 0) as decimal(18,2)) as NET_PRICE,
		# 				CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_1, 0)), 0), 0) as decimal(18,2)) as YEAR_1,
		# 				CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_2, 0)), 0), 0) as decimal(18,2)) as YEAR_2,
		# 				CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_3, 0)), 0), 0) as decimal(18,2)) as YEAR_3,
		# 				CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_4, 0)), 0), 0) as decimal(18,2)) as YEAR_4,
		# 				CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_5, 0)), 0), 0) as decimal(18,2)) as YEAR_5,
		# 				CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.DISCOUNT_AMOUNT_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as DISCOUNT_AMOUNT_INGL_CURR,
		# 				CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.NET_VALUE_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as NET_VALUE_INGL_CURR,
		# 				CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.NET_PRICE_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as NET_PRICE_INGL_CURR,
		# 				CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_1_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as YEAR_1_INGL_CURR,
		# 				CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_2_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as YEAR_2_INGL_CURR,
		# 				CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_3_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as YEAR_3_INGL_CURR,
		# 				CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_4_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as YEAR_4_INGL_CURR,
		# 				CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_5_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as YEAR_5_INGL_CURR
		# 				FROM SAQICO (NOLOCK) 
		# 				WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'
		# 				GROUP BY FABLOCATION_ID, QUOTE_RECORD_ID,QTEREV_RECORD_ID,LINE_ITEM_ID,SERVICE_ID)IQ
		# 	ON SAQICO.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND SAQICO.SERVICE_ID = IQ.SERVICE_ID AND SAQICO.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND SAQICO.FABLOCATION_ID = IQ.FABLOCATION_ID 
		# 	WHERE SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQICO.QTEREV_RECORD_ID = '{RevisionRecordId}' """.format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id,
		# 	Discount=self.discount))
		# Sql.RunQuery("""UPDATE SAQIGB
		# 	SET
		# 	NET_VALUE = IQ.NET_VALUE,
		# 	NET_PRICE = IQ.NET_PRICE,
		# 	YEAR_1 = IQ.YEAR_1,
		# 	YEAR_2 = IQ.YEAR_2,
		# 	YEAR_3 = IQ.YEAR_3,
		# 	YEAR_4 = IQ.YEAR_4,
		# 	YEAR_5 = IQ.YEAR_5,
		# 	DISCOUNT_AMOUNT_INGL_CURR = IQ.DISCOUNT_AMOUNT_INGL_CURR,
		# 	NET_VALUE_INGL_CURR = IQ.NET_VALUE_INGL_CURR,
		# 	NET_PRICE_INGL_CURR = IQ.NET_PRICE_INGL_CURR,
		# 	YEAR_1_INGL_CURR = IQ.YEAR_1_INGL_CURR,
		# 	YEAR_2_INGL_CURR = IQ.YEAR_2_INGL_CURR,
		# 	YEAR_3_INGL_CURR = IQ.YEAR_3_INGL_CURR,
		# 	YEAR_4_INGL_CURR = IQ.YEAR_4_INGL_CURR,
		# 	YEAR_5_INGL_CURR = IQ.YEAR_5_INGL_CURR,
		# 	DISCOUNT = '{Discount}'
		# 	FROM SAQIGB (NOLOCK)
		# 	INNER JOIN (SELECT 
		# 	GREENBOOK_RECORD_ID,
		# 	QUOTE_RECORD_ID,
		# 	SERVICE_ID,
		# 	FABLOCATION_RECORD_ID,
		# 	QTEREV_RECORD_ID,
		# 	CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.NET_VALUE, 0)), 0), 0) as decimal(18,2)) as NET_VALUE,
		# 	CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.NET_PRICE, 0)), 0), 0) as decimal(18,2)) as NET_PRICE,
		# 	CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_1, 0)), 0), 0) as decimal(18,2)) as YEAR_1,
		# 	CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_2, 0)), 0), 0) as decimal(18,2)) as YEAR_2,
		# 	CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_3, 0)), 0), 0) as decimal(18,2)) as YEAR_3,
		# 	CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_4, 0)), 0), 0) as decimal(18,2)) as YEAR_4,
		# 	CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_5, 0)), 0), 0) as decimal(18,2)) as YEAR_5,
		# 	CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.DISCOUNT_AMOUNT_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as DISCOUNT_AMOUNT_INGL_CURR,
		# 	CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.NET_VALUE_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as NET_VALUE_INGL_CURR,
		# 	CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.NET_PRICE_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as NET_PRICE_INGL_CURR,
		# 	CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_1_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as YEAR_1_INGL_CURR,
		# 	CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_2_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as YEAR_2_INGL_CURR,
		# 	CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_3_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as YEAR_3_INGL_CURR,
		# 	CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_4_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as YEAR_4_INGL_CURR,
		# 	CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_5_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as YEAR_5_INGL_CURR
		# 	FROM SAQICO (NOLOCK)
		# 	WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'
		# 	GROUP BY LINE_ITEM_ID, QUOTE_RECORD_ID,QTEREV_RECORD_ID,GREENBOOK_RECORD_ID,SERVICE_ID,FABLOCATION_RECORD_ID)IQ
		# 	ON SAQIGB.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID  AND SAQIGB.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND SAQIGB.SERVICE_ID = IQ.SERVICE_ID AND SAQIGB.FABLOCATION_RECORD_ID = IQ.FABLOCATION_RECORD_ID AND SAQIGB.GREENBOOK_RECORD_ID = IQ.GREENBOOK_RECORD_ID
		# 	WHERE SAQIGB.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQIGB.QTEREV_RECORD_ID = '{RevisionRecordId}' """.format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id,Discount=self.discount))
		# Sql.RunQuery("""UPDATE SAQITM
		# 					SET 
		# 					NET_VALUE = IQ.NET_VALUE,
		# 					NET_VALUE_INGL_CURR = IQ.NET_VALUE_INGL_CURR,
		# 					NET_PRICE = IQ.NET_PRICE,
		# 					NET_PRICE_INGL_CURR = IQ.NET_PRICE_INGL_CURR,
		# 					YEAR_1 = IQ.YEAR_1,
		# 					YEAR_1_INGL_CURR = IQ.YEAR_1_INGL_CURR,
		# 					YEAR_2 = IQ.YEAR_2,
		# 					YEAR_2_INGL_CURR = IQ.YEAR_2_INGL_CURR,
		# 					YEAR_3 = IQ.YEAR_3,
		# 					YEAR_3_INGL_CURR = IQ.YEAR_3_INGL_CURR,
		# 					YEAR_4 = IQ.YEAR_4,
		# 					YEAR_4_INGL_CURR = IQ.YEAR_4_INGL_CURR,
		# 					YEAR_5 = IQ.YEAR_5,
		# 					YEAR_5_INGL_CURR = IQ.YEAR_5_INGL_CURR,
		# 					DISCOUNT = '{Discount}'					
		# 					FROM SAQITM (NOLOCK)
		# 					INNER JOIN (SELECT SAQITM.CpqTableEntryId,
		# 								CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.NET_VALUE, 0)), 0), 0) as decimal(18,2)) as NET_VALUE,
		# 								CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.NET_VALUE_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as NET_VALUE_INGL_CURR,
		# 								CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.NET_PRICE, 0)), 0), 0) as decimal(18,2)) as NET_PRICE,
		# 								CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.NET_PRICE_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as NET_PRICE_INGL_CURR,
		# 								CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_1, 0)), 0), 0) as decimal(18,2)) as YEAR_1,
		# 								CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_1_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as YEAR_1_INGL_CURR,
		# 								CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_2, 0)), 0), 0) as decimal(18,2)) as YEAR_2,
		# 								CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_2_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as YEAR_2_INGL_CURR,
		# 								CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_3, 0)), 0), 0) as decimal(18,2)) as YEAR_3,
		# 								CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_3_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as YEAR_3_INGL_CURR,
		# 								CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_4, 0)), 0), 0) as decimal(18,2)) as YEAR_4,
		# 								CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_4_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as YEAR_4_INGL_CURR,
		# 								CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_5, 0)), 0), 0) as decimal(18,2)) as YEAR_5,
		# 								CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_5_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as YEAR_5_INGL_CURR
		# 								FROM SAQITM (NOLOCK) 
		# 								JOIN SAQICO (NOLOCK) ON SAQICO.QUOTE_RECORD_ID = SAQITM.QUOTE_RECORD_ID AND SAQICO.LINE_ITEM_ID = SAQITM.LINE_ITEM_ID
		# 								WHERE SAQITM.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQITM.QTEREV_RECORD_ID = '{RevisionRecordId}'
		# 								GROUP BY SAQITM.LINE_ITEM_ID, SAQITM.QUOTE_RECORD_ID, SAQITM.CpqTableEntryId,SAQITM.QTEREV_RECORD_ID)IQ
		# 					ON SAQITM.CpqTableEntryId = IQ.CpqTableEntryId 
		# 					WHERE SAQITM.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQITM.QTEREV_RECORD_ID = '{RevisionRecordId}' """.format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id,
		# 					Discount=self.discount,plus="+"))
		quote_currency = str(Quote.GetCustomField('Currency').Content)		
		total_net_price = 0.00		
		total_year_1 = 0.00
		total_year_2 = 0.00
		total_year_3 = 0.00
		total_year_4 = 0.00       
		total_year_5 = 0.00
		total_net_value = 0.00
		items_data = {}
		
		# items_obj = Sql.GetList("SELECT SERVICE_ID, LINE_ITEM_ID, ISNULL(YEAR_1, 0) as YEAR_1 ,ISNULL(YEAR_2, 0) as YEAR_2 ,ISNULL(YEAR_3, 0) as YEAR_3,ISNULL(YEAR_4, 0) as YEAR_4,ISNULL(YEAR_5, 0) as YEAR_5, ISNULL(NET_VALUE,0) AS NET_VALUE, ISNULL(NET_PRICE, 0) as NET_PRICE,ISNULL(YEAR_1_INGL_CURR, 0) as YEAR_1_INGL_CURR ,ISNULL(YEAR_2_INGL_CURR, 0) as YEAR_2_INGL_CURR ,ISNULL(YEAR_3_INGL_CURR, 0) as YEAR_3_INGL_CURR,ISNULL(YEAR_4_INGL_CURR, 0) as YEAR_4_INGL_CURR,ISNULL(YEAR_5_INGL_CURR, 0) as YEAR_5_INGL_CURR, ISNULL(NET_VALUE_INGL_CURR,0) AS NET_VALUE_INGL_CURR, ISNULL(NET_PRICE_INGL_CURR, 0) as NET_PRICE_INGL_CURR FROM SAQITM (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' ".format(self.contract_quote_record_id,self.quote_revision_record_id))
		# if items_obj:
		# 	for item_obj in items_obj:
		# 		items_data[int(float(item_obj.LINE_ITEM_ID))] = {'NET_VALUE':item_obj.NET_VALUE, 'SERVICE_ID':(item_obj.SERVICE_ID.replace('- BASE', '')).strip(), 'YEAR_1':item_obj.YEAR_1, 'YEAR_2':item_obj.YEAR_2,'YEAR_3':item_obj.YEAR_3,'YEAR_4':item_obj.YEAR_4,'YEAR_5':item_obj.YEAR_5, 'NET_PRICE':item_obj.NET_PRICE}
		for item in Quote.MainItems:
			item_number = int(item.RolledUpQuoteItem)
			if item_number in items_data.keys():
				if items_data.get(item_number).get('SERVICE_ID') == item.PartNumber:
					item_data = items_data.get(item_number)
					item.NET_PRICE.Value = float(item_data.get('NET_PRICE'))
					total_net_price += item.NET_PRICE.Value
					item.NET_VALUE.Value = item_data.get('NET_VALUE')
					total_net_value += item.NET_VALUE.Value	
					item.YEAR_1.Value = item_data.get('YEAR_1')
					total_year_1 += item.YEAR_1.Value
					item.YEAR_2.Value = item_data.get('YEAR_2')
					total_year_2 += item.YEAR_2.Value
					item.YEAR_3.Value = item_data.get('YEAR_3')
					total_year_3 += item.YEAR_2.Value
					item.YEAR_4.Value = item_data.get('YEAR_4')
					total_year_4 += item.YEAR_2.Value       
					item.YEAR_5.Value = item_data.get('YEAR_5')
					total_year_5 += item.YEAR_2.Value
					item.DISCOUNT.Value = str(self.discount)
		##Added the percentage symbol for discount custom field...
		Percentage = '%'
		Quote.GetCustomField('DISCOUNT').Content = str(self.discount)+ " " + Percentage
		#discount_value = Quote.GetCustomField('DISCOUNT').Content
		#Trace.Write("discount"+str(discount_value))
		# Quote.GetCustomField('TOTAL_NET_PRICE').Content =str(total_net_price) + " " + quote_currency
		# Quote.GetCustomField('YEAR_1').Content = str(total_year_1) + " " + quote_currency
		# Quote.GetCustomField('YEAR_2').Content = str(total_year_2) + " " + quote_currency
		# Quote.GetCustomField('YEAR_3').Content = str(total_year_3) + " " + quote_currency     
		# Quote.GetCustomField('TOTAL_NET_VALUE').Content = str(total_net_value) + " " + quote_currency
		Quote.Save()
		Sql.RunQuery("""UPDATE SAQTRV
						SET 									
						DISCOUNT_PERCENT = '{Discount}' WHERE QUOTE_REVISION_RECORD_ID = '{quote_revision_rec_id}'""".format(Discount = str(self.discount), quote_rec_id = self.contract_quote_record_id, quote_revision_rec_id = self.quote_revision_record_id,DecimalDiscount=decimal_discount ))


		#self._quote_item_update()
		#self._update_quote_summary()
	def CalculateMinusDiscount(self):
		Trace.Write("Minus")
		decimal_discount = float(int(self.discount)) / 100.0
		Sql.RunQuery("""UPDATE SAQICO SET 
										NET_PRICE = ISNULL(TARGET_PRICE,0) + (ISNULL(TARGET_PRICE,0) * {DecimalDiscount}),
										NET_PRICE_INGL_CURR = ISNULL(TARGET_PRICE_INGL_CURR,0) + (ISNULL(TARGET_PRICE_INGL_CURR,0) * {DecimalDiscount}),
										YEAR_1 = ISNULL(TARGET_PRICE,0) + (ISNULL(TARGET_PRICE,0) * {DecimalDiscount})
									FROM SAQICO (NOLOCK)                                     
									WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'""".format(
										QuoteRecordId=self.contract_quote_record_id,
										RevisionRecordId=self.quote_revision_record_id,
										DecimalDiscount=decimal_discount if decimal_discount > 0 else 1
										))
	#NET_VALUE REMOVAL FROM SAQICO
		self._update_year()
<<<<<<< Updated upstream
		Sql.RunQuery("""UPDATE SAQICO SET 
										NET_VALUE = ISNULL(YEAR_1,0) + ISNULL(YEAR_2,0) + ISNULL(YEAR_3,0) + ISNULL(YEAR_4,0) + ISNULL(YEAR_5,0),
										NET_VALUE_INGL_CURR = ''
									FROM SAQICO (NOLOCK)                                     
									WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'""".format(
										QuoteRecordId=self.contract_quote_record_id,
										RevisionRecordId=self.quote_revision_record_id 
										))
=======
	#	Sql.RunQuery("""UPDATE SAQICO SET 
    #									NET_VALUE = ISNULL(YEAR_1,0) + ISNULL(YEAR_2,0) + ISNULL(YEAR_3,0) + ISNULL(YEAR_4,0) + ISNULL(YEAR_5,0),
	#									NET_VALUE_INGL_CURR = ISNULL(YEAR_1_INGL_CURR,0) + ISNULL(YEAR_2_INGL_CURR
#,0) + ISNULL(YEAR_3_INGL_CURR,0) + ISNULL(YEAR_4_INGL_CURR,0) + ISNULL(YEAR_5_INGL_CURR,0)
#									FROM SAQICO (NOLOCK)                                     
#									WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}'""".format(
#										QuoteRecordId=self.contract_quote_record_id,
#										RevisionRecordId=self.quote_revision_record_id 
#										))
>>>>>>> Stashed changes
		# Sql.RunQuery("""UPDATE SAQITM
		# 					SET 
		# 					NET_VALUE = IQ.NET_VALUE,
		# 					NET_VALUE_INGL_CURR = IQ.NET_VALUE_INGL_CURR,
		# 					NET_PRICE = IQ.NET_PRICE,
		# 					NET_PRICE_INGL_CURR = IQ.NET_PRICE_INGL_CURR,
		# 					YEAR_1 = IQ.YEAR_1,
		# 					YEAR_1_INGL_CURR = IQ.YEAR_1_INGL_CURR,
		# 					YEAR_2 = IQ.YEAR_2,
		# 					YEAR_2_INGL_CURR = IQ.YEAR_2_INGL_CURR,
		# 					YEAR_3 = IQ.YEAR_3,
		# 					YEAR_3_INGL_CURR = IQ.YEAR_3_INGL_CURR,
		# 					YEAR_4 = IQ.YEAR_4,
		# 					YEAR_4_INGL_CURR = IQ.YEAR_4_INGL_CURR,
		# 					YEAR_5 = IQ.YEAR_5,
		# 					YEAR_5_INGL_CURR = IQ.YEAR_5_INGL_CURR
		# 					DISCOUNT = '{plus}{Discount}'					
		# 					FROM SAQITM (NOLOCK)
		# 					INNER JOIN (SELECT SAQITM.CpqTableEntryId,
		# 								CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.NET_VALUE, 0)), 0), 0) as decimal(18,2)) as NET_VALUE,
		# 								CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.NET_VALUE_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as NET_VALUE_INGL_CURR,
		# 								CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.NET_PRICE, 0)), 0), 0) as decimal(18,2)) as NET_PRICE,
		# 								CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.NET_PRICE_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as NET_PRICE_INGL_CURR,
		# 								CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_1, 0)), 0), 0) as decimal(18,2)) as YEAR_1,
		# 								CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_1_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as YEAR_1_INGL_CURR,
		# 								CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_2, 0)), 0), 0) as decimal(18,2)) as YEAR_2,
		# 								CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_2_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as YEAR_2_INGL_CURR,
		# 								CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_3, 0)), 0), 0) as decimal(18,2)) as YEAR_3,
		# 								CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_3_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as YEAR_3_INGL_CURR,
		# 								CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_4, 0)), 0), 0) as decimal(18,2)) as YEAR_4,
		# 								CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_4_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as YEAR_4_INGL_CURR,
		# 								CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_5, 0)), 0), 0) as decimal(18,2)) as YEAR_5,
		# 								CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_5_INGL_CURR, 0)), 0), 0) as decimal(18,2)) as YEAR_5_INGL_CURR
		# 								FROM SAQITM (NOLOCK) 
		# 								JOIN SAQICO (NOLOCK) ON SAQICO.QUOTE_RECORD_ID = SAQITM.QUOTE_RECORD_ID AND SAQICO.LINE_ITEM_ID = SAQITM.LINE_ITEM_ID
		# 								WHERE SAQITM.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQITM.QTEREV_RECORD_ID = '{RevisionRecordId}'
		# 								GROUP BY SAQITM.LINE_ITEM_ID, SAQITM.QUOTE_RECORD_ID, SAQITM.CpqTableEntryId,SAQITM.QTEREV_RECORD_ID)IQ
		# 					ON SAQITM.CpqTableEntryId = IQ.CpqTableEntryId 
		# 					WHERE SAQITM.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQITM.QTEREV_RECORD_ID = '{RevisionRecordId}' """.format(QuoteRecordId=self.contract_quote_record_id,RevisionRecordId=self.quote_revision_record_id,
		# 					Discount=self.discount,plus="+"))
		quote_currency = str(Quote.GetCustomField('Currency').Content)		
		total_net_price = 0.00		
		total_year_1 = 0.00
		total_year_2 = 0.00
		total_year_3 = 0.00
		total_year_4 = 0.00
		total_year_5 = 0.00        
		total_net_value = 0.00
		items_data = {}
		
		# items_obj = Sql.GetList("SELECT SERVICE_ID, LINE_ITEM_ID, ISNULL(YEAR_1, 0) as YEAR_1 ,ISNULL(YEAR_2, 0) as YEAR_2 , ISNULL(YEAR_3, 0) as YEAR_3,ISNULL(YEAR_4, 0) as YEAR_4,ISNULL(YEAR_5, 0) as YEAR_5,ISNULL(NET_VALUE,0) AS NET_VALUE, ISNULL(NET_PRICE, 0) as NET_PRICE FROM SAQITM (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' ".format(self.contract_quote_record_id,self.quote_revision_record_id))
		# if items_obj:
		# 	for item_obj in items_obj:
		# 		items_data[int(float(item_obj.LINE_ITEM_ID))] = {'NET_VALUE':item_obj.NET_VALUE, 'SERVICE_ID':(item_obj.SERVICE_ID.replace('- BASE', '')).strip(), 'YEAR_1':item_obj.YEAR_1, 'YEAR_2':item_obj.YEAR_2, 'YEAR_3':item_obj.YEAR_3,'YEAR_4':item_obj.YEAR_4,'YEAR_5':item_obj.YEAR_5,'NET_PRICE':item_obj.NET_PRICE}
		for item in Quote.MainItems:
			item_number = int(item.RolledUpQuoteItem)
			if item_number in items_data.keys():
				if items_data.get(item_number).get('SERVICE_ID') == item.PartNumber:
					item_data = items_data.get(item_number)
					item.NET_PRICE.Value = float(item_data.get('NET_PRICE'))
					total_net_price += item.NET_PRICE.Value
					item.NET_VALUE.Value = item_data.get('NET_VALUE')
					total_net_value += item.NET_VALUE.Value	
					item.YEAR_1.Value = item_data.get('YEAR_1')
					total_year_1 += item.YEAR_1.Value
					item.YEAR_2.Value = item_data.get('YEAR_2')
					total_year_2 += item.YEAR_2.Value
					item.YEAR_3.Value = item_data.get('YEAR_3')
					total_year_3 += item.YEAR_3.Value
					item.YEAR_4.Value = item_data.get('YEAR_4')
					total_year_4 += item.YEAR_4.Value
					item.YEAR_5.Value = item_data.get('YEAR_5')
					total_year_5 += item.YEAR_5.Value       
					item.DISCOUNT.Value = "+"+str(self.discount)
		##Added the percentage symbol for discount custom field...
		Percentage = '%'
		Quote.GetCustomField('DISCOUNT').Content = "-"+str(self.discount)+ " " + Percentage
		##controlling decimal based on currency
		if quote_currency:
			get_decimal_place = Sql.GetFirst("SELECT DISPLAY_DECIMAL_PLACES FROM PRCURR (NOLOCK) WHERE CURRENCY ='{}'".format(quote_currency))
			if get_decimal_place:
				decimal_value = get_decimal_place.DISPLAY_DECIMAL_PLACES
				formatting_string = "{0:." + str(decimal_value) + "f}"
				
				total_net_price =formatting_string.format(total_net_price)
				total_year_1 =formatting_string.format(total_year_1)
				total_year_2 =formatting_string.format(total_year_2)
				total_net_value =formatting_string.format(total_net_value)
		#discount_value = Quote.GetCustomField('DISCOUNT').Content
		#Trace.Write("discount"+str(discount_value))
		# Quote.GetCustomField('TOTAL_NET_PRICE').Content =str(total_net_price) + " " + quote_currency
		# Quote.GetCustomField('YEAR_1').Content = str(total_year_1) + " " + quote_currency
		# Quote.GetCustomField('YEAR_2').Content = str(total_year_2) + " " + quote_currency
		# Quote.GetCustomField('YEAR_3').Content = str(total_year_2) + " " + quote_currency     
		# Quote.GetCustomField('TOTAL_NET_VALUE').Content = str(total_net_value) + " " + quote_currency
		Quote.Save()

		Sql.RunQuery("""UPDATE SAQTRV
						SET 									
						DISCOUNT_PERCENT = '{Discount}' WHERE QUOTE_REVISION_RECORD_ID = '{quote_revision_rec_id}'""".format(Discount = str(self.discount), quote_rec_id = self.contract_quote_record_id, quote_revision_rec_id = self.quote_revision_record_id,DecimalDiscount=decimal_discount ))



discount = Param.Discount
summary_obj = ContractQuoteSummaryUpdate(discount=discount)

if "-" in discount:
	discount = str(discount).replace("-","").replace("%","").strip()
	summary_obj.CalculateMinusDiscount()
else:
	discount = str(discount).replace("+","").replace("%","").strip()
	Trace.Write("DISCOUNT="+str(discount))
	summary_obj.CalculatePlusDiscount()
#     summary_obj.update_summary()

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
        self.discount = discount
        try:
            self.contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
        except Exception:
            self.contract_quote_record_id = ''
    
    def _update_year(self):
        for count in range(2, 6):
            Sql.RunQuery("""UPDATE SAQICO SET
                                            SAQICO.YEAR_{Year} = CASE  
                                                WHEN CAST(DATEDIFF(day,SAQTMT.CONTRACT_VALID_FROM,SAQTMT.CONTRACT_VALID_TO) / 365.2425 AS INT) <= {Count} 
                                                    THEN ISNULL(SAQICO.YEAR_{Count}, 0) - (ISNULL(SAQICO.YEAR_{Count}, 0) * ISNULL(SAQICO.YEAR_OVER_YEAR, 0))/100.0                                                   
                                                ELSE 0
                                            END
                                        FROM SAQICO (NOLOCK) 
                                        JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQICO.QUOTE_RECORD_ID
                                        WHERE QUOTE_RECORD_ID = '{QuoteRecordId}'""".format(
                                            QuoteRecordId=self.contract_quote_record_id,
                                            Year=count,
                                            Count=count - 1 
                                            )
                        )    
    
    def _quote_item_lines_update(self):
        decimal_discount = float(int(self.discount)) / 100.0
        Sql.RunQuery("""UPDATE SAQICO SET 
                                        NET_PRICE = ISNULL(NET_PRICE,0) - (ISNULL(NET_PRICE,0) * {DecimalDiscount}),
                                        YEAR_1 = ISNULL(NET_PRICE,0) - (ISNULL(NET_PRICE,0) * {DecimalDiscount}),
                                        DISCOUNT = {Discount}
                                    FROM SAQICO (NOLOCK)                                     
                                    WHERE QUOTE_RECORD_ID = '{QuoteRecordId}'""".format(
                                        QuoteRecordId=self.contract_quote_record_id, 
                                        DecimalDiscount=decimal_discount if decimal_discount > 0 else 1,
                                        Discount=self.discount)
                    )
        # Update Year2 to Year5 - Start
        self._update_year()
        # Update Year2 to Year5 - End
        Sql.RunQuery("""UPDATE SAQICO SET 
                                        NET_VALUE = ISNULL(YEAR_1,0) + ISNULL(YEAR_2,0) + ISNULL(YEAR_3,0) + ISNULL(YEAR_4,0) + ISNULL(YEAR_5,0)
                                    FROM SAQICO (NOLOCK)                                     
                                    WHERE QUOTE_RECORD_ID = '{QuoteRecordId}'""".format(
                                        QuoteRecordId=self.contract_quote_record_id 
                                        )
                    )
    
    def _quote_item_update(self):
        Sql.RunQuery("""UPDATE SAQITM
                            SET 
                            NET_VALUE = IQ.NET_VALUE,
                            NET_PRICE = IQ.NET_PRICE,
                            YEAR_1 = IQ.YEAR_1,
                            YEAR_2 = IQ.YEAR_2,
                            DISCOUNT = {Discount}							
                            FROM SAQITM (NOLOCK)
                            INNER JOIN (SELECT SAQITM.CpqTableEntryId,
                                        CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.NET_VALUE, 0)), 0), 0) as decimal(18,2)) as NET_VALUE,
                                        CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.NET_PRICE, 0)), 0), 0) as decimal(18,2)) as NET_PRICE,
                                        CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_1, 0)), 0), 0) as decimal(18,2)) as YEAR_1,
                                        CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_2, 0)), 0), 0) as decimal(18,2)) as YEAR_2
                                        FROM SAQITM (NOLOCK) 
                                        JOIN SAQICO (NOLOCK) ON SAQICO.QUOTE_RECORD_ID = SAQITM.QUOTE_RECORD_ID AND SAQICO.LINE_ITEM_ID = SAQITM.LINE_ITEM_ID
                                        WHERE SAQITM.QUOTE_RECORD_ID = '{QuoteRecordId}' 
                                        GROUP BY SAQITM.LINE_ITEM_ID, SAQITM.QUOTE_RECORD_ID, SAQITM.CpqTableEntryId)IQ
                            ON SAQITM.CpqTableEntryId = IQ.CpqTableEntryId 
                            WHERE SAQITM.QUOTE_RECORD_ID = '{QuoteRecordId}' """.format(QuoteRecordId=self.contract_quote_record_id,
                            Discount=self.discount))
    
    def _update_quote_summary(self):
        quote_currency = str(Quote.GetCustomField('Currency').Content)		
        total_net_price = 0.00		
        total_year_1 = 0.00
        total_year_2 = 0.00        
        total_net_value = 0.00
        items_data = {}
        
        items_obj = Sql.GetList("SELECT SERVICE_ID, LINE_ITEM_ID, ISNULL(YEAR_1, 0) as YEAR_1 ,ISNULL(YEAR_2, 0) as YEAR_2 , ISNULL(NET_VALUE,0) AS NET_VALUE, ISNULL(NET_PRICE, 0) as NET_PRICE FROM SAQITM (NOLOCK) WHERE QUOTE_RECORD_ID = '{}'".format(self.contract_quote_record_id))
        if items_obj:
            for item_obj in items_obj:
                items_data[int(float(item_obj.LINE_ITEM_ID))] = {'NET_VALUE':item_obj.NET_VALUE, 'SERVICE_ID':(item_obj.SERVICE_ID.replace('- BASE', '')).strip(), 'YEAR_1':item_obj.YEAR_1, 'YEAR_2':item_obj.YEAR_2, 'NET_PRICE':item_obj.NET_PRICE}
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
                    item.DISCOUNT.Value = str(self.discount)
        ##Added the percentage symbol for discount custom field...
        Percentage = '%'
        Quote.GetCustomField('DISCOUNT').Content = str(self.discount)+ " " + Percentage
        #discount_value = Quote.GetCustomField('DISCOUNT').Content
        #Trace.Write("discount"+str(discount_value))
        Quote.GetCustomField('TOTAL_NET_PRICE').Content =str(total_net_price) + " " + quote_currency
        Quote.GetCustomField('YEAR_1').Content = str(total_year_1) + " " + quote_currency
        Quote.GetCustomField('YEAR_2').Content = str(total_year_2) + " " + quote_currency        
        Quote.GetCustomField('TOTAL_NET_VALUE').Content = str(total_net_value) + " " + quote_currency
        Quote.Save()

    def update_summary(self):
        if self.contract_quote_record_id:
            self._quote_item_lines_update()
            self._quote_item_update()
            self._update_quote_summary()

discount = Param.Discount
summary_obj = ContractQuoteSummaryUpdate(discount=discount)
summary_obj.update_summary()

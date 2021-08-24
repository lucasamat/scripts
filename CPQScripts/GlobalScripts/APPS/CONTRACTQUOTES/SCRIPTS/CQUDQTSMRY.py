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
                                                WHEN CAST(DATEDIFF(day,SAQTMT.CONTRACT_VALID_FROM,SAQTMT.CONTRACT_VALID_TO) / 365.2425 AS INT) == 1 
                                                    THEN ISNULL(SAQICO.YEAR_{PreviousYear}, 0) - (ISNULL(SAQICO.YEAR_{PreviousYear}, 0) * ISNULL(SAQICO.YEAR_OVER_YEAR, 0))/100                                                   
                                                ELSE 0
                                            END
                                        FROM SAQICO (NOLOCK) 
                                        JOIN SAQTMT (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQICO.QUOTE_RECORD_ID
                                        WHERE QUOTE_RECORD_ID = '{QuoteRecordId}'""".format(
                                            QuoteRecordId=self.contract_quote_record_id,
                                            Year=count,
                                            PreviousYear=count - 1 
                                            )
                        )    
    
    def _quote_item_lines_update(self):
        decimal_discount = int(self.discount) / 100
        Sql.RunQuery("""UPDATE SAQICO SET 
                                        SALES_PRICE = ISNULL(SALES_PRICE,0) - (ISNULL(SALES_PRICE,0) * {Discount}),
                                        YEAR_1 = ISNULL(SALES_PRICE,0) - (ISNULL(SALES_PRICE,0) * {Discount})
                                        DISCOUNT = {Discount}
                                    FROM SAQICO (NOLOCK)                                     
                                    WHERE QUOTE_RECORD_ID = '{QuoteRecordId}'""".format(
                                        QuoteRecordId=self.contract_quote_record_id, 
                                        Discount=decimal_discount if decimal_discount > 0 else 1)
                    )
        # Update Year2 to Year5 - Start
        self._update_year()
        # Update Year2 to Year5 - End
        Sql.RunQuery("""UPDATE SAQICO SET 
                                        EXTENDED_PRICE = ISNULL(YEAR_1,0) + ISNULL(YEAR_2,0) + ISNULL(YEAR_3,0) + ISNULL(YEAR_4,0) + ISNULL(YEAR_5,0)
                                    FROM SAQICO (NOLOCK)                                     
                                    WHERE QUOTE_RECORD_ID = '{QuoteRecordId}'""".format(
                                        QuoteRecordId=self.contract_quote_record_id 
                                        )
                    )
    def _quote_item_update(self):
        Sql.RunQuery("""UPDATE SAQITM
							SET 
							TARGET_PRICE = IQ.TARGET_PRICE,
							YEAR_1 = IQ.YEAR_1,
							YEAR_2 = IQ.YEAR_2							
							FROM SAQITM (NOLOCK)
							INNER JOIN (SELECT SAQITM.CpqTableEntryId,
										CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.TARGET_PRICE, 0)), 0), 0) as decimal(18,2)) as TARGET_PRICE,
										CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_1, 0)), 0), 0) as decimal(18,2)) as YEAR_1,
										CAST(ROUND(ISNULL(SUM(ISNULL(SAQICO.YEAR_2, 0)), 0), 0) as decimal(18,2)) as YEAR_2
										FROM SAQITM (NOLOCK) 
										JOIN SAQICO (NOLOCK) ON SAQICO.QUOTE_RECORD_ID = SAQITM.QUOTE_RECORD_ID AND SAQICO.LINE_ITEM_ID = SAQITM.LINE_ITEM_ID
										WHERE SAQITM.QUOTE_RECORD_ID = '{QuoteRecordId}' 
										GROUP BY SAQITM.LINE_ITEM_ID, SAQITM.QUOTE_RECORD_ID, SAQITM.CpqTableEntryId)IQ
							ON SAQITM.CpqTableEntryId = IQ.CpqTableEntryId 
							WHERE SAQITM.QUOTE_RECORD_ID = '{QuoteRecordId}' """.format(QuoteRecordId=self.contract_quote_record_id))
    
    def update_summary(self):
        if self.contract_quote_record_id:
            Quote.GetCustomField('DISCOUNT').Content = str(self.discount)
            for item in Quote.MainItems:
                item.DISCOUNT.Value = str(self.discount)
            Quote.Save()
            self._quote_item_lines_update()
            self._quote_item_update()
discount = Param.Discount
summary_obj = ContractQuoteSummaryUpdate(discount=discount)
summary_obj.update_summary()

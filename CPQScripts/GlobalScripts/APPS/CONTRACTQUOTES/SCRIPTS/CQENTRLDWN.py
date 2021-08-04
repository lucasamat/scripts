# =========================================================================================================================================
#   __script_name : CQENTRLDWN.PY
#   __script_description : THIS SCRIPT IS USED FOR ENTITLEMENT ROLLDOWN 
#   __primary_author__ : ASHA LYSANDAR
#   __create_date : 12-11-2020
#   � BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct
import clr
import System.Net
import sys
import datetime
from System.Net import CookieContainer, NetworkCredential, Mail
from System.Net.Mail import SmtpClient, MailAddress, Attachment, MailMessage
from SYDATABASE import SQL
Sql = SQL()
userId = str(User.Id)
userName = str(User.UserName)


try:
	objs = Param.CPQ_Columns['objectName']    
	wherecon = Param.CPQ_Columns['where']
	get_prev_dict = Param.CPQ_Columns['get_prev_dict']
except:
	objectName = Param.objectName
	wherecon = Param.where
	get_prev_dict = Param.get_prev_dict
wherecon = wherecon.replace("&#39;","'")
get_prev_dict = eval(get_prev_dict.replace("&#39;","'").replace("&#38;","&"))
objItems = objs.split('=')
where = wherecon.split(",")[0]
SAQITMWhere = wherecon.split(",")[1]
sectionid = wherecon.split(",")[2]
objectName = objItems[0]
quote = objItems[2].split(",")[1]
Log.Info("QUOTE--------->"+str(quote))
userid = objItems[2].split(",")[0]
try: 
	attributeList = objItems[1].split(",")
except:
	attributeList = ""
get_serviceid = SAQITMWhere.split('SERVICE_ID = ')
get_serviceid = get_serviceid[len(get_serviceid)-1].replace("'","")
#Log.Info("attributeList ============>"+str(attributeList)+str(objs))
Log.Info("script called..40-----"+str(objectName)+" - "+str(where)+" - "+str(SAQITMWhere)+"------ "+str(attributeList)+'--'+str(get_serviceid))

def update_entitlement_price_impact(where_condition=None):
	# Update ENTITLEMENT_PRICE_IMPACT in SAQICO - Start 
	
	#Log.Info('quote---44-----'+str(quote))  
	"""Log.Info("======>>>>>>>><<<<<ENTITLEMENT_PRICE_IMPACT "+str(UPDATE SAQICO
						SET SAQICO.ENTITLEMENT_PRICE_IMPACT = CASE
												WHEN SAQICO.EXCHANGE_RATE > 0 THEN ISNULL(SAQIEN.ENTITLEMENT_PRICE_IMPACT, 0) * ISNULL(SAQICO.EXCHANGE_RATE,0)
												ELSE SAQIEN.ENTITLEMENT_PRICE_IMPACT
												END,
						SAQICO.ENTITLEMENT_COST_IMPACT = CASE
												WHEN SAQICO.EXCHANGE_RATE > 0 THEN ISNULL(SAQIEN.ENTITLEMENT_COST_IMPACT, 0) * ISNULL(SAQICO.EXCHANGE_RATE,0)
												ELSE SAQIEN.ENTITLEMENT_COST_IMPACT
												END,
						SAQICO.TOTAL_COST = CASE  
												WHEN SAQICO.TOTAL_COST > 0 THEN ISNULL(SAQIEN.ENTITLEMENT_COST_IMPACT, 0) + ISNULL(SAQICO.TOTAL_COST,0)
												ELSE SAQICO.TOTAL_COST
												END,
						SAQICO.TARGET_PRICE = CASE  
												WHEN SAQICO.TARGET_PRICE > 0 THEN SAQICO.TARGET_PRICE + (ISNULL(SAQICO.EXCHANGE_RATE, 0) * ISNULL(SAQIEN.ENTITLEMENT_PRICE_IMPACT, 0))
												ELSE SAQICO.TARGET_PRICE
											END,
						SAQICO.BD_PRICE = CASE  
											WHEN SAQICO.BD_PRICE > 0 THEN SAQICO.BD_PRICE + (ISNULL(SAQICO.EXCHANGE_RATE, 0) * ISNULL(SAQIEN.ENTITLEMENT_PRICE_IMPACT, 0))
											ELSE SAQICO.BD_PRICE
										END,  
						SAQICO.SALES_PRICE = CASE  
												WHEN SAQICO.SALES_PRICE > 0 THEN SAQICO.SALES_PRICE + (ISNULL(SAQICO.EXCHANGE_RATE, 0) * ISNULL(SAQIEN.ENTITLEMENT_PRICE_IMPACT, 0))
												ELSE SAQICO.SALES_PRICE
											END,
						SAQICO.SALES_DISCOUNT_PRICE = CASE  
												WHEN SAQICO.SALES_DISCOUNT_PRICE > 0 THEN SAQICO.SALES_DISCOUNT_PRICE + (ISNULL(SAQICO.EXCHANGE_RATE, 0) * ISNULL(SAQIEN.ENTITLEMENT_PRICE_IMPACT, 0))
												ELSE SAQICO.SALES_DISCOUNT_PRICE
											END,
						SAQICO.YEAR_1 = CASE  
											WHEN SAQICO.YEAR_1 > 0 THEN SAQICO.YEAR_1 + (ISNULL(SAQICO.EXCHANGE_RATE, 0) * ISNULL(SAQIEN.ENTITLEMENT_PRICE_IMPACT, 0))
											ELSE ISNULL(SAQICO.YEAR_1, 0)
										END,
						SAQICO.YEAR_2 = CASE  
											WHEN SAQICO.YEAR_2 > 0 THEN SAQICO.YEAR_2 + (ISNULL(SAQICO.EXCHANGE_RATE, 0) * ISNULL(SAQIEN.ENTITLEMENT_PRICE_IMPACT, 0))
											ELSE ISNULL(SAQICO.YEAR_2,0)
										END,
						SAQICO.YEAR_3 = CASE  
											WHEN ISNULL(SAQICO.YEAR_3,0) > 0 THEN SAQICO.YEAR_3 + (ISNULL(SAQICO.EXCHANGE_RATE, 0) * ISNULL(SAQIEN.ENTITLEMENT_PRICE_IMPACT, 0))
											ELSE ISNULL(SAQICO.YEAR_3,0)
										END,
						SAQICO.YEAR_4 = CASE  
											WHEN ISNULL(SAQICO.YEAR_4,0) > 0 THEN SAQICO.YEAR_4 + (ISNULL(SAQICO.EXCHANGE_RATE, 0) * ISNULL(SAQIEN.ENTITLEMENT_PRICE_IMPACT, 0))
											ELSE ISNULL(SAQICO.YEAR_4,0)
										END,
						SAQICO.YEAR_5 = CASE  
											WHEN ISNULL(SAQICO.YEAR_5,0) > 0 THEN SAQICO.YEAR_5 + (ISNULL(SAQICO.EXCHANGE_RATE, 0) * ISNULL(SAQIEN.ENTITLEMENT_PRICE_IMPACT, 0))
											ELSE ISNULL(SAQICO.YEAR_5,0)
										END,
						SAQICO.EXTENDED_PRICE = CASE 
													WHEN ISNULL(SAQICO.EXTENDED_PRICE,0) > 0 THEN
																						CASE  
																							WHEN ISNULL(SAQICO.YEAR_1, 0) > 0 THEN SAQICO.YEAR_1 + (ISNULL(SAQICO.EXCHANGE_RATE, 0) * ISNULL(SAQIEN.ENTITLEMENT_PRICE_IMPACT, 0))
																							ELSE ISNULL(SAQICO.YEAR_1, 0)
																						END +
																						CASE  
																							WHEN ISNULL(SAQICO.YEAR_2, 0) > 0 THEN SAQICO.YEAR_2 + (ISNULL(SAQICO.EXCHANGE_RATE, 0) * ISNULL(SAQIEN.ENTITLEMENT_PRICE_IMPACT, 0))
																							ELSE ISNULL(SAQICO.YEAR_2, 0)
																						END +
																						CASE  
																							WHEN ISNULL(SAQICO.YEAR_3,0) > 0 THEN SAQICO.YEAR_3 + (ISNULL(SAQICO.EXCHANGE_RATE, 0) * ISNULL(SAQIEN.ENTITLEMENT_PRICE_IMPACT, 0))
																							ELSE ISNULL(SAQICO.YEAR_3,0)
																						END +
																						CASE  
																							WHEN ISNULL(SAQICO.YEAR_4,0) > 0 THEN SAQICO.YEAR_4 + (ISNULL(SAQICO.EXCHANGE_RATE, 0) * ISNULL(SAQIEN.ENTITLEMENT_PRICE_IMPACT, 0))
																							ELSE ISNULL(SAQICO.YEAR_4,0)
																						END +
																						CASE  
																							WHEN ISNULL(SAQICO.YEAR_5,0) > 0 THEN SAQICO.YEAR_5 + (ISNULL(SAQICO.EXCHANGE_RATE, 0) * ISNULL(SAQIEN.ENTITLEMENT_PRICE_IMPACT, 0))
																							ELSE ISNULL(SAQICO.YEAR_5,0)
																						END
													ELSE ISNULL(SAQICO.EXTENDED_PRICE,0)
												END,
						SAQICO.PRICING_STATUS = CASE
												WHEN SAQIEN.ENTITLEMENT_PRICE_IMPACT > 0 THEN 'ACQUIRED'
												ELSE SAQICO.PRICING_STATUS
												END
						FROM SAQICO
						JOIN SAQIEN (NOLOCK) ON SAQIEN.QUOTE_RECORD_ID = SAQICO.QUOTE_RECORD_ID AND 
												SAQIEN.EQUIPMENT_RECORD_ID = SAQICO.EQUIPMENT_RECORD_ID AND
												SAQIEN.SERVICE_RECORD_ID = SAQICO.SERVICE_RECORD_ID AND
												SAQIEN.QTEITMCOB_RECORD_ID = SAQICO.QUOTE_ITEM_COVERED_OBJECT_RECORD_ID						
						{WhereCondition}
					AND SAQICO.PRICING_STATUS IN ('PARTIALLY PRICED','ACQUIRED') AND SAQIEN.ENTITLEMENT_NAME = 'ADDL_PERF_GUARANTEE_91_1'.format(WhereCondition=where_condition)))"""
	costimp = priceimp = ''
	entitlement_obj = Sql.GetFirst("""select ENTITLEMENT_COST_IMPACT,ENTITLEMENT_PRICE_IMPACT,ENTITLEMENT_NAME from (SELECT distinct e.QUOTE_RECORD_ID, replace(X.Y.value('(ENTITLEMENT_NAME)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_NAME,replace(X.Y.value('(IS_DEFAULT)[1]', 'VARCHAR(128)'),';#38','&') as IS_DEFAULT,replace(X.Y.value('(ENTITLEMENT_COST_IMPACT)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_COST_IMPACT,replace(X.Y.value('(ENTITLEMENT_PRICE_IMPACT)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_PRICE_IMPACT FROM (select SAQIEN.QUOTE_RECORD_ID,convert(xml,replace(ENTITLEMENT_XML,'&',';#38')) as ENTITLEMENT_XML from {} (nolock) JOIN SAQICO (NOLOCK) ON SAQIEN.QUOTE_RECORD_ID = SAQICO.QUOTE_RECORD_ID AND
	SAQIEN.EQUIPMENT_RECORD_ID = SAQICO.EQUIPMENT_RECORD_ID AND
	SAQIEN.SERVICE_RECORD_ID = SAQICO.SERVICE_RECORD_ID AND
	SAQIEN.QTEITMCOB_RECORD_ID = SAQICO.QUOTE_ITEM_COVERED_OBJECT_RECORD_ID where SAQIEN.QUOTE_RECORD_ID = '{}' ) e OUTER APPLY e.ENTITLEMENT_XML.nodes('QUOTE_ITEM_ENTITLEMENT') as X(Y) ) as m where ENTITLEMENT_NAME LIKE 'ADDL_PERF_GUARANTEE_91_1%'""".format('SAQIEN',quote))
	if entitlement_obj:
		costimp = entitlement_obj.ENTITLEMENT_COST_IMPACT
		priceimp = entitlement_obj.ENTITLEMENT_PRICE_IMPACT
	Log.Info('137---------'+str("""UPDATE SAQICO
						SET SAQICO.ENTITLEMENT_PRICE_IMPACT = CASE
												WHEN SAQICO.EXCHANGE_RATE > 0 THEN ISNULL({price_impact}, 0) * ISNULL(SAQICO.EXCHANGE_RATE,0)
												ELSE {price_impact}
												END,
						SAQICO.ENTITLEMENT_COST_IMPACT = CASE
												WHEN SAQICO.EXCHANGE_RATE > 0 THEN ISNULL({cost_impact}, 0) * ISNULL(SAQICO.EXCHANGE_RATE,0)
												ELSE {cost_impact}
												END,
						SAQICO.TOTAL_COST = CASE  
												WHEN SAQICO.TOTAL_COST > 0 THEN ISNULL({cost_impact}, 0) + ISNULL(SAQICO.TOTAL_COST,0)
												ELSE SAQICO.TOTAL_COST
												END,
						SAQICO.TARGET_PRICE = CASE  
												WHEN SAQICO.TARGET_PRICE > 0 THEN SAQICO.TARGET_PRICE + (ISNULL(SAQICO.EXCHANGE_RATE, 0) * ISNULL({price_impact}, 0))
												ELSE SAQICO.TARGET_PRICE
											END,
						SAQICO.BD_PRICE = CASE  
											WHEN SAQICO.BD_PRICE > 0 THEN SAQICO.BD_PRICE + (ISNULL(SAQICO.EXCHANGE_RATE, 0) * ISNULL({price_impact}, 0))
											ELSE SAQICO.BD_PRICE
										END,  
						SAQICO.SALES_PRICE = CASE  
												WHEN SAQICO.SALES_PRICE > 0 THEN SAQICO.SALES_PRICE + (ISNULL(SAQICO.EXCHANGE_RATE, 0) * ISNULL({price_impact}, 0))
												ELSE SAQICO.SALES_PRICE
											END,
						SAQICO.SALES_DISCOUNT_PRICE = CASE  
												WHEN SAQICO.SALES_DISCOUNT_PRICE > 0 THEN SAQICO.SALES_DISCOUNT_PRICE + (ISNULL(SAQICO.EXCHANGE_RATE, 0) * ISNULL({price_impact}, 0))
												ELSE SAQICO.SALES_DISCOUNT_PRICE
											END,
						SAQICO.YEAR_1 = CASE  
											WHEN SAQICO.YEAR_1 > 0 THEN SAQICO.YEAR_1 + (ISNULL(SAQICO.EXCHANGE_RATE, 0) * ISNULL({price_impact}, 0))
											ELSE ISNULL(SAQICO.YEAR_1, 0)
										END,
						SAQICO.YEAR_2 = CASE  
											WHEN SAQICO.YEAR_2 > 0 THEN SAQICO.YEAR_2 + (ISNULL(SAQICO.EXCHANGE_RATE, 0) * ISNULL({price_impact}, 0))
											ELSE ISNULL(SAQICO.YEAR_2,0)
										END,
						SAQICO.YEAR_3 = CASE  
											WHEN ISNULL(SAQICO.YEAR_3,0) > 0 THEN SAQICO.YEAR_3 + (ISNULL(SAQICO.EXCHANGE_RATE, 0) * ISNULL({price_impact}, 0))
											ELSE ISNULL(SAQICO.YEAR_3,0)
										END,
						SAQICO.YEAR_4 = CASE  
											WHEN ISNULL(SAQICO.YEAR_4,0) > 0 THEN SAQICO.YEAR_4 + (ISNULL(SAQICO.EXCHANGE_RATE, 0) * ISNULL({price_impact}, 0))
											ELSE ISNULL(SAQICO.YEAR_4,0)
										END,
						SAQICO.YEAR_5 = CASE  
											WHEN ISNULL(SAQICO.YEAR_5,0) > 0 THEN SAQICO.YEAR_5 + (ISNULL(SAQICO.EXCHANGE_RATE, 0) * ISNULL({price_impact}, 0))
											ELSE ISNULL(SAQICO.YEAR_5,0)
										END,
						SAQICO.EXTENDED_PRICE = CASE 
													WHEN ISNULL(SAQICO.EXTENDED_PRICE,0) > 0 THEN
																						CASE  
																							WHEN ISNULL(SAQICO.YEAR_1, 0) > 0 THEN SAQICO.YEAR_1 + (ISNULL(SAQICO.EXCHANGE_RATE, 0) * ISNULL({price_impact}, 0))
																							ELSE ISNULL(SAQICO.YEAR_1, 0)
																						END +
																						CASE  
																							WHEN ISNULL(SAQICO.YEAR_2, 0) > 0 THEN SAQICO.YEAR_2 + (ISNULL(SAQICO.EXCHANGE_RATE, 0) * ISNULL({price_impact}, 0))
																							ELSE ISNULL(SAQICO.YEAR_2, 0)
																						END +
																						CASE  
																							WHEN ISNULL(SAQICO.YEAR_3,0) > 0 THEN SAQICO.YEAR_3 + (ISNULL(SAQICO.EXCHANGE_RATE, 0) * ISNULL({price_impact}, 0))
																							ELSE ISNULL(SAQICO.YEAR_3,0)
																						END +
																						CASE  
																							WHEN ISNULL(SAQICO.YEAR_4,0) > 0 THEN SAQICO.YEAR_4 + (ISNULL(SAQICO.EXCHANGE_RATE, 0) * ISNULL({price_impact}, 0))
																							ELSE ISNULL(SAQICO.YEAR_4,0)
																						END +
																						CASE  
																							WHEN ISNULL(SAQICO.YEAR_5,0) > 0 THEN SAQICO.YEAR_5 + (ISNULL(SAQICO.EXCHANGE_RATE, 0) * ISNULL({price_impact}, 0))
																							ELSE ISNULL(SAQICO.YEAR_5,0)
																						END
													ELSE ISNULL(SAQICO.EXTENDED_PRICE,0)
												END,
						SAQICO.PRICING_STATUS = CASE
												WHEN {price_impact} > 0 OR {cost_impact}> 0 THEN 'ACQUIRED'
												ELSE SAQICO.PRICING_STATUS
												END
						FROM SAQICO
						JOIN SAQIEN (NOLOCK) ON SAQIEN.QUOTE_RECORD_ID = SAQICO.QUOTE_RECORD_ID AND 
												SAQIEN.EQUIPMENT_RECORD_ID = SAQICO.EQUIPMENT_RECORD_ID AND
												SAQIEN.SERVICE_RECORD_ID = SAQICO.SERVICE_RECORD_ID AND
												SAQIEN.QTEITMCOB_RECORD_ID = SAQICO.QUOTE_ITEM_COVERED_OBJECT_RECORD_ID						
						{WhereCondition}
					AND SAQICO.PRICING_STATUS IN ('PARTIALLY PRICED','ACQUIRED') """.format(WhereCondition=where_condition,price_impact=priceimp,cost_impact=costimp)))
	Sql.RunQuery("""UPDATE SAQICO
						SET SAQICO.ENTITLEMENT_PRICE_IMPACT = CASE
												WHEN SAQICO.EXCHANGE_RATE > 0 THEN ISNULL({price_impact}, 0) * ISNULL(SAQICO.EXCHANGE_RATE,0)
												ELSE {price_impact}
												END,
						SAQICO.ENTITLEMENT_COST_IMPACT = CASE
												WHEN SAQICO.EXCHANGE_RATE > 0 THEN ISNULL({cost_impact}, 0) * ISNULL(SAQICO.EXCHANGE_RATE,0)
												ELSE {cost_impact}
												END,
						SAQICO.TOTAL_COST = CASE  
												WHEN SAQICO.TOTAL_COST > 0 THEN ISNULL({cost_impact}, 0) + ISNULL(SAQICO.TOTAL_COST,0)
												ELSE SAQICO.TOTAL_COST
												END,
						SAQICO.TARGET_PRICE = CASE  
												WHEN SAQICO.TARGET_PRICE > 0 THEN SAQICO.TARGET_PRICE + (ISNULL(SAQICO.EXCHANGE_RATE, 0) * ISNULL({price_impact}, 0))
												ELSE SAQICO.TARGET_PRICE
											END,
						SAQICO.BD_PRICE = CASE  
											WHEN SAQICO.BD_PRICE > 0 THEN SAQICO.BD_PRICE + (ISNULL(SAQICO.EXCHANGE_RATE, 0) * ISNULL({price_impact}, 0))
											ELSE SAQICO.BD_PRICE
										END,  
						SAQICO.SALES_PRICE = CASE  
												WHEN SAQICO.SALES_PRICE > 0 THEN SAQICO.SALES_PRICE + (ISNULL(SAQICO.EXCHANGE_RATE, 0) * ISNULL({price_impact}, 0))
												ELSE SAQICO.SALES_PRICE
											END,
						SAQICO.SALES_DISCOUNT_PRICE = CASE  
												WHEN SAQICO.SALES_DISCOUNT_PRICE > 0 THEN SAQICO.SALES_DISCOUNT_PRICE + (ISNULL(SAQICO.EXCHANGE_RATE, 0) * ISNULL({price_impact}, 0))
												ELSE SAQICO.SALES_DISCOUNT_PRICE
											END,
						SAQICO.YEAR_1 = CASE  
											WHEN SAQICO.YEAR_1 > 0 THEN SAQICO.YEAR_1 + (ISNULL(SAQICO.EXCHANGE_RATE, 0) * ISNULL({price_impact}, 0))
											ELSE ISNULL(SAQICO.YEAR_1, 0)
										END,
						SAQICO.YEAR_2 = CASE  
											WHEN SAQICO.YEAR_2 > 0 THEN SAQICO.YEAR_2 + (ISNULL(SAQICO.EXCHANGE_RATE, 0) * ISNULL({price_impact}, 0))
											ELSE ISNULL(SAQICO.YEAR_2,0)
										END,
						SAQICO.YEAR_3 = CASE  
											WHEN ISNULL(SAQICO.YEAR_3,0) > 0 THEN SAQICO.YEAR_3 + (ISNULL(SAQICO.EXCHANGE_RATE, 0) * ISNULL({price_impact}, 0))
											ELSE ISNULL(SAQICO.YEAR_3,0)
										END,
						SAQICO.YEAR_4 = CASE  
											WHEN ISNULL(SAQICO.YEAR_4,0) > 0 THEN SAQICO.YEAR_4 + (ISNULL(SAQICO.EXCHANGE_RATE, 0) * ISNULL({price_impact}, 0))
											ELSE ISNULL(SAQICO.YEAR_4,0)
										END,
						SAQICO.YEAR_5 = CASE  
											WHEN ISNULL(SAQICO.YEAR_5,0) > 0 THEN SAQICO.YEAR_5 + (ISNULL(SAQICO.EXCHANGE_RATE, 0) * ISNULL({price_impact}, 0))
											ELSE ISNULL(SAQICO.YEAR_5,0)
										END,
						SAQICO.EXTENDED_PRICE = CASE 
													WHEN ISNULL(SAQICO.EXTENDED_PRICE,0) > 0 THEN
																						CASE  
																							WHEN ISNULL(SAQICO.YEAR_1, 0) > 0 THEN SAQICO.YEAR_1 + (ISNULL(SAQICO.EXCHANGE_RATE, 0) * ISNULL({price_impact}, 0))
																							ELSE ISNULL(SAQICO.YEAR_1, 0)
																						END +
																						CASE  
																							WHEN ISNULL(SAQICO.YEAR_2, 0) > 0 THEN SAQICO.YEAR_2 + (ISNULL(SAQICO.EXCHANGE_RATE, 0) * ISNULL({price_impact}, 0))
																							ELSE ISNULL(SAQICO.YEAR_2, 0)
																						END +
																						CASE  
																							WHEN ISNULL(SAQICO.YEAR_3,0) > 0 THEN SAQICO.YEAR_3 + (ISNULL(SAQICO.EXCHANGE_RATE, 0) * ISNULL({price_impact}, 0))
																							ELSE ISNULL(SAQICO.YEAR_3,0)
																						END +
																						CASE  
																							WHEN ISNULL(SAQICO.YEAR_4,0) > 0 THEN SAQICO.YEAR_4 + (ISNULL(SAQICO.EXCHANGE_RATE, 0) * ISNULL({price_impact}, 0))
																							ELSE ISNULL(SAQICO.YEAR_4,0)
																						END +
																						CASE  
																							WHEN ISNULL(SAQICO.YEAR_5,0) > 0 THEN SAQICO.YEAR_5 + (ISNULL(SAQICO.EXCHANGE_RATE, 0) * ISNULL({price_impact}, 0))
																							ELSE ISNULL(SAQICO.YEAR_5,0)
																						END
													ELSE ISNULL(SAQICO.EXTENDED_PRICE,0)
												END,
						SAQICO.PRICING_STATUS = CASE
												WHEN {price_impact} > 0 OR {cost_impact}> 0 THEN 'ACQUIRED'
												ELSE SAQICO.PRICING_STATUS
												END
						FROM SAQICO
						JOIN SAQIEN (NOLOCK) ON SAQIEN.QUOTE_RECORD_ID = SAQICO.QUOTE_RECORD_ID AND 
												SAQIEN.EQUIPMENT_RECORD_ID = SAQICO.EQUIPMENT_RECORD_ID AND
												SAQIEN.SERVICE_RECORD_ID = SAQICO.SERVICE_RECORD_ID AND
												SAQIEN.QTEITMCOB_RECORD_ID = SAQICO.QUOTE_ITEM_COVERED_OBJECT_RECORD_ID						
						{WhereCondition}
					AND SAQICO.PRICING_STATUS IN ('PARTIALLY PRICED','ACQUIRED') """.format(WhereCondition=where_condition,price_impact=priceimp,cost_impact=costimp))
	# Update ENTITLEMENT_PRICE_IMPACT in SAQICO - End
	# Update SAQITM from SAQICO - Start
	'''Log.Info("""UPDATE A
				SET OBJECT_QUANTITY = EQUIPMENT_ID_COUNT,
				TOTAL_COST = B.TOTAL_COST,
				EXTENDED_PRICE = B.EXTENDED_PRICE,
				BD_PRICE = B.BD_PRICE,
				SALES_PRICE = B.SALES_PRICE,
				TARGET_PRICE = B.TARGET_PRICE,
				CEILING_PRICE = B.CEILING_PRICE,
				SALES_DISCOUNT_PRICE = B.SALES_DISCOUNT_PRICE,
				YEAR_1=B.TOTAL_YEAR_1,
				YEAR_2=B.TOTAL_YEAR_2,
				YEAR_3=B.TOTAL_YEAR_3,
				YEAR_4=B.TOTAL_YEAR_4,
				YEAR_5=B.TOTAL_YEAR_5
				FROM SAQITM A(NOLOCK)
				INNER JOIN (SELECT QUOTE_ID,QTEITM_RECORD_ID AS QUOTE_ITEM_RECORD_ID,
				COUNT(EQUIPMENT_ID) as EQUIPMENT_ID_COUNT,
				ISNULL(SUM(ISNULL(TOTAL_COST, 0)), 0) as TOTAL_COST,
				ISNULL(SUM(ISNULL(BD_PRICE, 0)), 0) as BD_PRICE,
				ISNULL(SUM(ISNULL(SALES_PRICE, 0)), 0) as SALES_PRICE,
				ISNULL(SUM(ISNULL(TARGET_PRICE, 0)), 0) as TARGET_PRICE,
				ISNULL(SUM(ISNULL(BASE_PRICE, 0)), 0) as BASE_PRICE,
				ISNULL(SUM(ISNULL(CEILING_PRICE, 0)), 0) as CEILING_PRICE,
				ISNULL(SUM(ISNULL(SALES_DISCOUNT_PRICE, 0)), 0) as SALES_DISCOUNT_PRICE,
				ISNULL(SUM(ISNULL(EXTENDED_PRICE, 0)), 0) as EXTENDED_PRICE,
				ISNULL(SUM(ISNULL(LIST_PRICE, 0)), 0) as LIST_PRICE,
				ISNULL(SUM(ISNULL(YEAR_1, 0)), 0) as TOTAL_YEAR_1,
				ISNULL(SUM(ISNULL(YEAR_2, 0)), 0) as TOTAL_YEAR_2,
				ISNULL(SUM(ISNULL(YEAR_3, 0)), 0) as TOTAL_YEAR_3,
				ISNULL(SUM(ISNULL(YEAR_4, 0)), 0) as TOTAL_YEAR_4,
				ISNULL(SUM(ISNULL(YEAR_5, 0)), 0) as TOTAL_YEAR_5
				FROM SAQICO (NOLOCK) A WHERE {WhereCondition} GROUP BY A.QUOTE_ID,A.QTEITM_RECORD_ID)B
				ON A.QUOTE_ID = B.QUOTE_ID AND A.QUOTE_ITEM_RECORD_ID = B.QUOTE_ITEM_RECORD_ID
				WHERE {Where} """.format(WhereCondition=where_condition.replace("SAQICO","A"),Where=SAQITMWhere))'''
	Sql.RunQuery("""UPDATE A
				SET OBJECT_QUANTITY = EQUIPMENT_ID_COUNT,
				TOTAL_COST = B.TOTAL_COST,
				EXTENDED_PRICE = B.EXTENDED_PRICE,
				BD_PRICE = B.BD_PRICE,
				SALES_PRICE = B.SALES_PRICE,
				TARGET_PRICE = B.TARGET_PRICE,
				CEILING_PRICE = B.CEILING_PRICE,
				SALES_DISCOUNT_PRICE = B.SALES_DISCOUNT_PRICE,
				YEAR_1=B.TOTAL_YEAR_1,
				YEAR_2=B.TOTAL_YEAR_2,
				YEAR_3=B.TOTAL_YEAR_3,
				YEAR_4=B.TOTAL_YEAR_4,
				YEAR_5=B.TOTAL_YEAR_5
				FROM SAQITM A(NOLOCK)
				INNER JOIN (SELECT QUOTE_ID,QTEITM_RECORD_ID AS QUOTE_ITEM_RECORD_ID,
				COUNT(EQUIPMENT_ID) as EQUIPMENT_ID_COUNT,
				ISNULL(SUM(ISNULL(TOTAL_COST, 0)), 0) as TOTAL_COST,
				ISNULL(SUM(ISNULL(BD_PRICE, 0)), 0) as BD_PRICE,
				ISNULL(SUM(ISNULL(SALES_PRICE, 0)), 0) as SALES_PRICE,
				ISNULL(SUM(ISNULL(TARGET_PRICE, 0)), 0) as TARGET_PRICE,
				ISNULL(SUM(ISNULL(BASE_PRICE, 0)), 0) as BASE_PRICE,
				ISNULL(SUM(ISNULL(CEILING_PRICE, 0)), 0) as CEILING_PRICE,
				ISNULL(SUM(ISNULL(SALES_DISCOUNT_PRICE, 0)), 0) as SALES_DISCOUNT_PRICE,
				ISNULL(SUM(ISNULL(EXTENDED_PRICE, 0)), 0) as EXTENDED_PRICE,
				ISNULL(SUM(ISNULL(LIST_PRICE, 0)), 0) as LIST_PRICE,
				ISNULL(SUM(ISNULL(YEAR_1, 0)), 0) as TOTAL_YEAR_1,
				ISNULL(SUM(ISNULL(YEAR_2, 0)), 0) as TOTAL_YEAR_2,
				ISNULL(SUM(ISNULL(YEAR_3, 0)), 0) as TOTAL_YEAR_3,
				ISNULL(SUM(ISNULL(YEAR_4, 0)), 0) as TOTAL_YEAR_4,
				ISNULL(SUM(ISNULL(YEAR_5, 0)), 0) as TOTAL_YEAR_5
				FROM SAQICO (NOLOCK) A WHERE {WhereCondition} GROUP BY A.QUOTE_ID,A.QTEITM_RECORD_ID)B
				ON A.QUOTE_ID = B.QUOTE_ID AND A.QUOTE_ITEM_RECORD_ID = B.QUOTE_ITEM_RECORD_ID
				WHERE {Where} """.format(WhereCondition=where_condition.replace("SAQICO","A"),Where = SAQITMWhere))	
	# Update SAQITM from SAQICO - End	
	#Update tool relocation:
	
	
	return True

def sendEmail(level):
	#Log.Info('284-----entitlement email started-----')
	getQuoteId = Sql.GetFirst("SELECT QUOTE_ID FROM SAQTMT WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{}'".format(quote))
	getEmail = Sql.GetFirst("SELECT email from users where id={}".format(userid))
	#Log.Info("SELECT email from users where id='{}'".format(userid))
	userEmail = ""
	userEmail = str(getEmail.email)
	Header = "<!DOCTYPE html><html><head><style>h4{font-weight:normal; font-family:sans-serif;} table {font-family: Calibri, sans-serif; border-collapse: collapse; width: 75%}td, th {  border: 1px solid #dddddd;  text-align: left; padding: 8px;}.im {color: #222;}tr:nth-child(even) {background-color: #dddddd;} #grey{background: rgb(245,245,245);} #bd{color : 'black';}</style> </head> <body><h4>Hi, <br> <br>The Entitlement settings have been applied to the equipment in the following quote:</br></h4>"

	Table_start ="<table class='table table-bordered'><tr><th id = 'grey'>Quote ID</th><th id = 'grey'>Rolldown Level</th><th id = 'grey'>Rolldown Status</th></tr><tr><td >"+str(getQuoteId.QUOTE_ID)+"</td><td>"+str(level)+"</td><td>Completed</td></tr></table> <br> <br>Note: Please do not reply to this email.</body></html>"

	Error_Info = Header + Table_start

	LOGIN_CRE = Sql.GetFirst("SELECT User_name,Password FROM SYCONF where Domain ='SUPPORT_MAIL'")

	# Create new SmtpClient object
	mailClient = SmtpClient()

	# Set the host and port (eg. smtp.gmail.com)
	mailClient.Host = "smtp.gmail.com"
	mailClient.Port = 587
	mailClient.EnableSsl = "true"

	# Setup NetworkCredential
	mailCred = NetworkCredential()
	mailCred.UserName = str(LOGIN_CRE.User_name)
	mailCred.Password = str(LOGIN_CRE.Password)
	mailClient.Credentials = mailCred
	to_email = ''
	to_email += str(userEmail)
	#Log.Info()
	from_email = ''
	from_email += str(userEmail)
	# Create two mail adresses, one for send from and the another for recipient
	toEmail = MailAddress(to_email)
	fromEmail = MailAddress(from_email)

	# Create new MailMessage object
	msg = MailMessage(fromEmail, toEmail)

	# Set message subject and body
	msg.Subject = str(level)+" Rolldown"
	msg.IsBodyHtml = True
	msg.Body = Error_Info
	copyEmail1 = MailAddress("sathyabama.akhala@bostonharborconsulting.com")
	#copyEmail2 = MailAddress("mayura.priya@bostonharborconsulting.com")
	#copyEmail3 = MailAddress("dhurga.gopalakrishnan@bostonharborconsulting.com")
	copyEmail4 = MailAddress("ranjani.parkavi@bostonharborconsulting.com")
	copyEmail5 = MailAddress("ashish.gandotra@bostonharborconsulting.com")
	#copyEmail6 = MailAddress("aditya.shivkumar@bostonharborconsulting.com")
	msg.Bcc.Add(copyEmail1)
	#msg.Bcc.Add(copyEmail2)
	#msg.Bcc.Add(copyEmail3)
	msg.Bcc.Add(copyEmail4)
	msg.Bcc.Add(copyEmail5)
	#msg.Bcc.Add(copyEmail6)
	# CC Emails
	# Send the message
	mailClient.Send(msg)

	return True
datetimenow = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p")    
obj_list = []
is_changed = False

level = ""
if objectName == 'SAQTSE':
	level = "Offering Entitlement "
elif objectName == 'SAQSFE':
	level = "Fab Location Entitlement "
elif objectName == 'SAQSGE':
	level = "Greenbook Entitlement "
elif objectName == "SAQSCE":
	level = "Equipment Entitlement "
elif objectName == "SAQSAE":
	level = "Assembly Entitlement "
Log.Info("level1---"+str(level))
if 'Z0007' in get_serviceid:
	objectName = 'SAQSCE'
if objectName == 'SAQTSE':
	if 'Z0007' not in get_serviceid:
		obj_list = ['SAQSCE','SAQSGE','SAQSFE','SAQIEN','SAQSAE']
	else:
		obj_list = ['SAQSGE','SAQSFE','SAQIEN','SAQSAE']
elif objectName == 'SAQSFE':
	obj_list = ['SAQSCE','SAQSGE','SAQTSE','SAQIEN','SAQSAE']
	is_changed = True
elif objectName == 'SAQSGE':
	obj_list = ['SAQSCE','SAQSFE','SAQTSE','SAQIEN','SAQSAE']
	is_changed = True
elif objectName == 'SAQSCE':
	obj_list = ['SAQTSE','SAQSFE','SAQSGE','SAQIEN','SAQSAE']
	is_changed = True

# Log.Info('459----objectName------'+str(objectName))
# Log.Info('459----wherecon------'+str(wherecon))
# Log.Info('get_prev_dict----'+str(get_prev_dict))
datetimenow = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p") 
where_cond = where.replace('SRC.','')
Log.Info('where_cond----'+str(where_cond))
getinnercon  = Sql.GetFirst("select QUOTE_RECORD_ID,convert(xml,replace(replace(ENTITLEMENT_XML,'&',';#38'),'''',';#39')) as ENTITLEMENT_XML,CPS_MATCH_ID,CPS_CONFIGURATION_ID from "+str(objectName)+" (nolock) "+str(where_cond)+"")
#Log.Info('getinnercon-----'+str(("select QUOTE_RECORD_ID,convert(xml,replace(replace(ENTITLEMENT_XML,'&',';#38'),'''',';#39')) as ENTITLEMENT_XML,CPS_MATCH_ID,CPS_CONFIGURATION_ID from "+str(objectName)+" (nolock) "+str(where_cond)+"")))

##get c4c quote id
get_c4c_quote_id = Sql.GetFirst("select * from SAQTMT where MASTER_TABLE_QUOTE_RECORD_ID = '{}'".format(getinnercon.QUOTE_RECORD_ID))
###SAQSCE temp table
ent_temp =""
if 'Z0007' in get_serviceid or ('Z0016' in get_serviceid and objectName == 'SAQSCE'):
	where_condition = SAQITMWhere.replace('A.','').replace("'","''")
	#get_c4c_quote_id = Sql.GetFirst("select * from SAQTMT where MASTER_TABLE_QUOTE_RECORD_ID = '{}'".format(getinnercon.QUOTE_RECORD_ID))
	ent_temp = "SAQSCE_ENT_BKP_"+str(get_c4c_quote_id.C4C_QUOTE_ID)
	ent_temp_drop = Sql.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(ent_temp)+"'' ) BEGIN DROP TABLE "+str(ent_temp)+" END  ' ")
	Sql.GetFirst("sp_executesql @T=N'declare @H int; Declare @val Varchar(MAX);DECLARE @XML XML; SELECT @val =  replace(replace(STUFF((SELECT ''''+FINAL from(select  REPLACE(entitlement_xml,''<QUOTE_ITEM_ENTITLEMENT>'',sml) AS FINAL FROM (select ''  <QUOTE_ITEM_ENTITLEMENT><QUOTE_ID>''+quote_id+''</QUOTE_ID><QUOTE_RECORD_ID>''+QUOTE_RECORD_ID+''</QUOTE_RECORD_ID><SERVICE_ID>''+service_id+''</SERVICE_ID><FABLOCATION_ID>''+FABLOCATION_ID+''</FABLOCATION_ID><GREENBOOK>''+GREENBOOK+''</GREENBOOK><EQUIPMENT_ID>''+equipment_id+''</EQUIPMENT_ID>'' AS sml,replace(entitlement_xml,''&'','';#38'')  as entitlement_xml from SAQSCE(nolock) "+str(where_condition)+" )A )a FOR XML PATH ('''')), 1, 1, ''''),''&lt;'',''<''),''&gt;'',''>'')  SELECT @XML = CONVERT(XML,''<ROOT>''+@VAL+''</ROOT>'') exec sys.sp_xml_preparedocument @H output,@XML; select QUOTE_ID,QUOTE_RECORD_ID,EQUIPMENT_ID,SERVICE_ID,ENTITLEMENT_NAME,ENTITLEMENT_COST_IMPACT,FABLOCATION_ID,GREENBOOK,ENTITLEMENT_VALUE_CODE,ENTITLEMENT_DISPLAY_VALUE,ENTITLEMENT_PRICE_IMPACT,IS_DEFAULT,ENTITLEMENT_TYPE,ENTITLEMENT_DESCRIPTION,PRICE_METHOD,CALCULATION_FACTOR INTO "+str(ent_temp)+"  from openxml(@H, ''ROOT/QUOTE_ITEM_ENTITLEMENT'', 0) with (QUOTE_ID VARCHAR(100) ''QUOTE_ID'',QUOTE_RECORD_ID VARCHAR(100) ''QUOTE_RECORD_ID'',EQUIPMENT_ID VARCHAR(100) ''EQUIPMENT_ID'',ENTITLEMENT_NAME VARCHAR(100) ''ENTITLEMENT_NAME'',SERVICE_ID VARCHAR(100) ''SERVICE_ID'',ENTITLEMENT_COST_IMPACT VARCHAR(100) ''ENTITLEMENT_COST_IMPACT'',FABLOCATION_ID VARCHAR(100) ''FABLOCATION_ID'',GREENBOOK VARCHAR(100) ''GREENBOOK'',ENTITLEMENT_VALUE_CODE VARCHAR(100) ''ENTITLEMENT_VALUE_CODE'',ENTITLEMENT_DISPLAY_VALUE VARCHAR(100) ''ENTITLEMENT_DISPLAY_VALUE'',ENTITLEMENT_PRICE_IMPACT VARCHAR(100) ''ENTITLEMENT_PRICE_IMPACT'',IS_DEFAULT VARCHAR(100) ''IS_DEFAULT'',ENTITLEMENT_TYPE VARCHAR(100) ''ENTITLEMENT_TYPE'',ENTITLEMENT_DESCRIPTION VARCHAR(100) ''ENTITLEMENT_DESCRIPTION'',PRICE_METHOD VARCHAR(100) ''PRICE_METHOD'',CALCULATION_FACTOR VARCHAR(100) ''CALCULATION_FACTOR'') ; exec sys.sp_xml_removedocument @H; '")



where_conditn = where_cond.replace("'","''")
#get_c4c_quote_id = Sql.GetFirst("select * from SAQTMT where MASTER_TABLE_QUOTE_RECORD_ID = '{}'".format(getinnercon.QUOTE_RECORD_ID))
ent_roll_temp = "ENT_ROLL_BKP_"+str(get_c4c_quote_id.C4C_QUOTE_ID)
ent_temp_drop1 = Sql.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(ent_roll_temp)+"'' ) BEGIN DROP TABLE "+str(ent_roll_temp)+" END  ' ")
Sql.GetFirst("sp_executesql @T=N'declare @H int; Declare @val Varchar(MAX);DECLARE @XML XML; SELECT @val =  replace(replace(STUFF((SELECT ''''+FINAL from(select  REPLACE(entitlement_xml,''<QUOTE_ITEM_ENTITLEMENT>'',sml) AS FINAL FROM (select ''  <QUOTE_ITEM_ENTITLEMENT><QUOTE_ID>''+quote_id+''</QUOTE_ID><QUOTE_RECORD_ID>''+QUOTE_RECORD_ID+''</QUOTE_RECORD_ID><SERVICE_ID>''+service_id+''</SERVICE_ID>'' AS sml,replace(entitlement_xml,''&'','';#38'')  as entitlement_xml from "+str(objectName)+"(nolock) "+str(where_conditn)+" )A )a FOR XML PATH ('''')), 1, 1, ''''),''&lt;'',''<''),''&gt;'',''>'')  SELECT @XML = CONVERT(XML,''<ROOT>''+@VAL+''</ROOT>'') exec sys.sp_xml_preparedocument @H output,@XML; select QUOTE_ID,QUOTE_RECORD_ID,SERVICE_ID,ENTITLEMENT_NAME,ENTITLEMENT_COST_IMPACT,ENTITLEMENT_VALUE_CODE,ENTITLEMENT_DISPLAY_VALUE,ENTITLEMENT_PRICE_IMPACT,IS_DEFAULT,ENTITLEMENT_TYPE,ENTITLEMENT_DESCRIPTION,PRICE_METHOD,CALCULATION_FACTOR INTO "+str(ent_roll_temp)+"  from openxml(@H, ''ROOT/QUOTE_ITEM_ENTITLEMENT'', 0) with (QUOTE_ID VARCHAR(100) ''QUOTE_ID'',QUOTE_RECORD_ID VARCHAR(100) ''QUOTE_RECORD_ID'',ENTITLEMENT_NAME VARCHAR(100) ''ENTITLEMENT_NAME'',SERVICE_ID VARCHAR(100) ''SERVICE_ID'',ENTITLEMENT_COST_IMPACT VARCHAR(100) ''ENTITLEMENT_COST_IMPACT'',ENTITLEMENT_VALUE_CODE VARCHAR(100) ''ENTITLEMENT_VALUE_CODE'',ENTITLEMENT_DISPLAY_VALUE VARCHAR(100) ''ENTITLEMENT_DISPLAY_VALUE'',ENTITLEMENT_PRICE_IMPACT VARCHAR(100) ''ENTITLEMENT_PRICE_IMPACT'',IS_DEFAULT VARCHAR(100) ''IS_DEFAULT'',ENTITLEMENT_TYPE VARCHAR(100) ''ENTITLEMENT_TYPE'',ENTITLEMENT_DESCRIPTION VARCHAR(100) ''ENTITLEMENT_DESCRIPTION'',PRICE_METHOD VARCHAR(100) ''PRICE_METHOD'',CALCULATION_FACTOR VARCHAR(100) ''CALCULATION_FACTOR'') ; exec sys.sp_xml_removedocument @H; '")

GetXMLsecField = Sql.GetList("SELECT * from {} ".format(ent_roll_temp))				



fab_dict = {}
grnbk_dict = {}

for obj in obj_list:
	join =""
	update_fields = " CPS_CONFIGURATION_ID = '{}', CpqTableEntryModifiedBy = {}, CpqTableEntryDateModified = '{}'".format(getinnercon.CPS_CONFIGURATION_ID,userId,datetimenow)
	if objectName == 'SAQSGE' and obj == 'SAQIEN':
		join = " JOIN SAQICO ON SAQICO.QUOTE_RECORD_ID = SRC.QUOTE_RECORD_ID AND SAQICO.SERVICE_ID = SRC.SERVICE_ID AND SAQICO.FABLOCATION_ID = SRC.FABLOCATION_ID AND SAQICO.GREENBOOK = SRC.GREENBOOK AND TGT.QTEITMCOB_RECORD_ID = SAQICO.QUOTE_ITEM_COVERED_OBJECT_RECORD_ID "
	# elif objectName == 'SAQSGE':
	# 	join = " AND SRC.FABLOCATION_ID = TGT.FABLOCATION_ID AND SRC.GREENBOOK = TGT.GREENBOOK "    
	# elif objectName == 'SAQSFE':
	# 	join = " AND SRC.FABLOCATION_ID = TGT.FABLOCATION_ID "
	elif objectName == 'SAQSCE' and obj == 'SAQIEN':
		join = " JOIN SAQICO ON SAQICO.QUOTE_RECORD_ID = SRC.QUOTE_RECORD_ID AND SAQICO.SERVICE_ID = SRC.SERVICE_ID AND SAQICO.FABLOCATION_ID = SRC.FABLOCATION_ID AND SAQICO.GREENBOOK = SRC.GREENBOOK AND SAQICO.EQUIPMENT_ID = SRC.EQUIPMENT_ID AND TGT.QTEITMCOB_RECORD_ID = SAQICO.QUOTE_ITEM_COVERED_OBJECT_RECORD_ID "
	elif objectName == 'SAQSCE' and obj == 'SAQSAE':
		join = "  AND SRC.EQUIPMENT_ID = TGT.EQUIPMENT_ID JOIN SAQICO ON SAQICO.QUOTE_RECORD_ID = SRC.QUOTE_RECORD_ID AND SAQICO.SERVICE_ID = SRC.SERVICE_ID AND SAQICO.FABLOCATION_ID = SRC.FABLOCATION_ID AND SAQICO.GREENBOOK = SRC.GREENBOOK AND SAQICO.EQUIPMENT_ID = SRC.EQUIPMENT_ID "
	elif objectName == 'SAQSAE':
		join = " AND SRC.GREENBOOK =TGT.GREENBOOK AND SRC.FABLOCATION_ID = TGT.FABLOCATION_ID AND SRC.EQUIPMENT_ID = TGT.EQUIPMENT_ID  AND SRC.ASSEMBLY_ID = TGT.ASSEMBLY_ID "
	#elif objectname == 'SAQTSE':
	
	
	if is_changed and obj == "SAQSCE":
		update_fields += ",IS_CHANGED = 1"
	
	###roll down and up for all levels starts
	if obj == 'SAQTSE'  and GetXMLsecField :
		where_condition = SAQITMWhere.replace('A.','')
		# " WHERE QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}' ".format(self.ContractRecordId, serviceId)	
		
		if 'Z0016' in get_serviceid:
			#get_value_query = Sql.GetFirst("select QUOTE_RECORD_ID,convert(xml,replace(replace(ENTITLEMENT_XML,'&',';#38'),'''',';#39')) as ENTITLEMENT_XML from SAQTSE {} ".format(where_condition) )
			GetXMLsec = Sql.GetList("select distinct ENTITLEMENT_NAME,IS_DEFAULT,case when ENTITLEMENT_TYPE in ('Check Box','CheckBox') then 'Check Box' else ENTITLEMENT_TYPE end as ENTITLEMENT_TYPE,ENTITLEMENT_DESCRIPTION,PRICE_METHOD,CASE WHEN Isnumeric(ENTITLEMENT_COST_IMPACT) = 1 THEN CONVERT(DECIMAL(18,2),ENTITLEMENT_COST_IMPACT) ELSE null END as ENTITLEMENT_COST_IMPACT from {} {}".format(ent_temp,where_condition))
			Log.Info('getxml----'+str("select distinct ENTITLEMENT_NAME,IS_DEFAULT,case when ENTITLEMENT_TYPE in ('Check Box','CheckBox') then 'Check Box' else ENTITLEMENT_TYPE end as ENTITLEMENT_TYPE,ENTITLEMENT_DESCRIPTION,PRICE_METHOD,CASE WHEN Isnumeric(ENTITLEMENT_COST_IMPACT) = 1 THEN CONVERT(DECIMAL(18,2),ENTITLEMENT_COST_IMPACT) ELSE null END as ENTITLEMENT_COST_IMPACT from {} {}".format(ent_temp,where_condition)))
			updateentXML = ""
			if GetXMLsec:
				for value in GetXMLsec:
					where_condition = SAQITMWhere.replace('A.','')
					where_condition += " AND ENTITLEMENT_NAME = '{}'".format(value.ENTITLEMENT_NAME) 
					#get_value_query = Sql.GetFirst("select * from {} {} ".format(ent_temp,where_condition) )
					get_cost_impact = value.ENTITLEMENT_COST_IMPACT
					get_currency = value.PRICE_METHOD
					GetXML = Sql.GetFirst("SELECT * from {} where ENTITLEMENT_NAME = '{}' ".format(ent_roll_temp,value.ENTITLEMENT_NAME))
					
					get_value = GetXML.ENTITLEMENT_DISPLAY_VALUE
					get_calc_factor = GetXML.CALCULATION_FACTOR 
					get_price_impact = GetXML.ENTITLEMENT_PRICE_IMPACT
					get_code = GetXML.ENTITLEMENT_VALUE_CODE
					#try:
					
					if value.ENTITLEMENT_TYPE == 'FreeInputNoMatching' and 'AGS_LAB_OPT' in value.ENTITLEMENT_NAME:

						get_value_qry = Sql.GetFirst("select SUM(CASE WHEN Isnumeric(ENTITLEMENT_DISPLAY_VALUE) = 1 THEN CONVERT(DECIMAL(18,2),ENTITLEMENT_DISPLAY_VALUE) ELSE 0 END) AS ENTITLEMENT_DISPLAY_VALUE from {pricetemp} where ENTITLEMENT_NAME = '{ent_name}' ".format(pricetemp = ent_temp,where_condition = where_condition,ent_name = value.ENTITLEMENT_NAME))

						if get_value_qry:
							#if get_value_diff != 0.00:
							get_calc_factor = get_value = int(round(float(get_value_qry.ENTITLEMENT_DISPLAY_VALUE) ) )
							if value.ENTITLEMENT_COST_IMPACT and get_value:
								get_price_impact = get_value * float(value.ENTITLEMENT_COST_IMPACT)
							else:
								get_price_impact = 0.00
							#get_price_impact = get_value * float(value.ENTITLEMENT_COST_IMPACT)
							
						else:
							get_calc_factor = get_value = GetXMLfab.ENTITLEMENT_DISPLAY_VALUE
							#get_cost_impact = GetXMLfab.ENTITLEMENT_COST_IMPACT
					elif value.ENTITLEMENT_TYPE in ('Check Box','CheckBox'):
						get_value_qry = Sql.GetList("select ENTITLEMENT_DISPLAY_VALUE,ENTITLEMENT_VALUE_CODE from {pricetemp} where ENTITLEMENT_NAME = '{ent_name}' ".format(pricetemp = ent_temp,ent_name = value.ENTITLEMENT_NAME))
						getvalue = []
						getcode = []
						for val in get_value_qry:
							#Trace.Write('ENTITLEMENT_NAME----'+str(i.ENTITLEMENT_NAME)+'--'+str(i.ENTITLEMENT_DISPLAY_VALUE))
							if val.ENTITLEMENT_VALUE_CODE:
								getcode.extend(eval(val.ENTITLEMENT_VALUE_CODE) )
								
							if val.ENTITLEMENT_DISPLAY_VALUE:
								getvalue.extend(eval(val.ENTITLEMENT_DISPLAY_VALUE) )
						get_val = list(set(getvalue) )
						get_cod = list(set(getcode))
						get_value = str(get_val).replace("'", '"')
						get_code = str(get_cod).replace("'", '"')
					updateentXML  += """<QUOTE_ITEM_ENTITLEMENT>
						<ENTITLEMENT_NAME>{ent_name}</ENTITLEMENT_NAME>
						<ENTITLEMENT_VALUE_CODE>{ent_val_code}</ENTITLEMENT_VALUE_CODE>
						<ENTITLEMENT_DISPLAY_VALUE>{ent_disp_val}</ENTITLEMENT_DISPLAY_VALUE>
						<ENTITLEMENT_COST_IMPACT>{ct}</ENTITLEMENT_COST_IMPACT>
						<ENTITLEMENT_PRICE_IMPACT>{pi}</ENTITLEMENT_PRICE_IMPACT>
						<IS_DEFAULT>{is_default}</IS_DEFAULT>
						<ENTITLEMENT_TYPE>{ent_type}</ENTITLEMENT_TYPE>
						<ENTITLEMENT_DESCRIPTION>{ent_desc}</ENTITLEMENT_DESCRIPTION>
						<PRICE_METHOD>{pm}</PRICE_METHOD>
						<CALCULATION_FACTOR>{cf}</CALCULATION_FACTOR>
						</QUOTE_ITEM_ENTITLEMENT>""".format(ent_name = value.ENTITLEMENT_NAME,ent_val_code = get_code,ent_disp_val = get_value ,ct = get_cost_impact ,pi = get_price_impact ,is_default = value.IS_DEFAULT ,ent_desc= value.ENTITLEMENT_DESCRIPTION ,pm = value.PRICE_METHOD ,cf= get_calc_factor, ent_type = value.ENTITLEMENT_TYPE)

		else:
			updateentXML = ""
			for value in GetXMLsecField:
				get_value = value.ENTITLEMENT_DISPLAY_VALUE
				get_calc_factor = value.CALCULATION_FACTOR 
				get_price_impact = value.ENTITLEMENT_PRICE_IMPACT
				get_cost_impact = value.ENTITLEMENT_COST_IMPACT
				#try:
				get_currency = value.PRICE_METHOD
				#except:
				#get_currency = ""
				#Log.Info('ENTITLEMENT_COST_IMPACT-----'+str(value.ENTITLEMENT_COST_IMPACT))
							
				if (value.ENTITLEMENT_TYPE in ('Drop Down','DropDown') and 'Z0007' in get_serviceid and value.ENTITLEMENT_COST_IMPACT):
					#if (value.ENTITLEMENT_COST_IMPACT and get_serviceid =='Z0007_AG'):
					#GetXMLfab = Sql.GetFirst("select SUM(CASE WHEN Isnumeric(ENTITLEMENT_COST_IMPACT) = 1 THEN CONVERT(DECIMAL(18,2),ENTITLEMENT_COST_IMPACT) ELSE 0 END) AS ENTITLEMENT_COST_IMPACT from (SELECT distinct e.QUOTE_RECORD_ID, e.EQUIPMENT_RECORD_ID, e.EQUIPMENT_ID ,replace(X.Y.value('(ENTITLEMENT_COST_IMPACT)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_COST_IMPACT,replace(X.Y.value('(ENTITLEMENT_NAME)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_NAME,replace(X.Y.value('(ENTITLEMENT_PRICE_IMPACT)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_PRICE_IMPACT FROM (select SAQSCE.QUOTE_RECORD_ID as QUOTE_RECORD_ID, SAQSCE.EQUIPMENT_RECORD_ID, SAQSCE.EQUIPMENT_ID, CONVERT(xml, replace(cast(SAQSCE.ENTITLEMENT_XML as varchar(max)),'&','&amp;'), 2) as ENTITLEMENT_XML FROM SAQSCE (NOLOCK) {}) e OUTER APPLY e.ENTITLEMENT_XML.nodes('QUOTE_ITEM_ENTITLEMENT') as X(Y) ) IQ where ENTITLEMENT_NAME =  '{}'  ".format(where_condition,value.ENTITLEMENT_NAME))
					GetXMLfab = Sql.GetFirst("select SUM(CASE WHEN Isnumeric(ENTITLEMENT_COST_IMPACT) = 1 THEN CONVERT(DECIMAL(18,2),ENTITLEMENT_COST_IMPACT) ELSE 0 END) AS ENTITLEMENT_COST_IMPACT from (SELECT * FROM {pricetemp} {where_condition} AND ENTITLEMENT_NAME = '{ent_name}') IQ ".format(pricetemp = ent_temp,where_condition = where_condition,ent_name = value.ENTITLEMENT_NAME))

					if GetXMLfab:
						get_cost_impact = GetXMLfab.ENTITLEMENT_COST_IMPACT
					#Log.Info("get_calc_factor---"+str(get_calc_factor))

					
				updateentXML  += """<QUOTE_ITEM_ENTITLEMENT>
					<ENTITLEMENT_NAME>{ent_name}</ENTITLEMENT_NAME>
					<ENTITLEMENT_VALUE_CODE>{ent_val_code}</ENTITLEMENT_VALUE_CODE>
					<ENTITLEMENT_DISPLAY_VALUE>{ent_disp_val}</ENTITLEMENT_DISPLAY_VALUE>
					<ENTITLEMENT_COST_IMPACT>{ct}</ENTITLEMENT_COST_IMPACT>
					<ENTITLEMENT_PRICE_IMPACT>{pi}</ENTITLEMENT_PRICE_IMPACT>
					<IS_DEFAULT>{is_default}</IS_DEFAULT>
					<ENTITLEMENT_TYPE>{ent_type}</ENTITLEMENT_TYPE>
					<ENTITLEMENT_DESCRIPTION>{ent_desc}</ENTITLEMENT_DESCRIPTION>
					<PRICE_METHOD>{pm}</PRICE_METHOD>
					<CALCULATION_FACTOR>{cf}</CALCULATION_FACTOR>
					</QUOTE_ITEM_ENTITLEMENT>""".format(ent_name = value.ENTITLEMENT_NAME,ent_val_code = value.ENTITLEMENT_VALUE_CODE,ent_disp_val = get_value ,ct = get_cost_impact ,pi = get_price_impact ,is_default = value.IS_DEFAULT ,ent_desc= value.ENTITLEMENT_DESCRIPTION ,pm = value.PRICE_METHOD ,cf= get_calc_factor, ent_type = value.ENTITLEMENT_TYPE) 
				
		Log.Info('updateentXML--ser-'+str(updateentXML))
		where_condition = SAQITMWhere.replace('A.','')
		UpdateEntitlement = " UPDATE {} SET ENTITLEMENT_XML= '{}', {} {} ".format(obj, updateentXML,update_fields,where_condition)
		Log.Info('UpdateEntitlement--'+str(" UPDATE {} SET ENTITLEMENT_XML= '', {} {} ".format(obj, update_fields,where_condition)))		
		Sql.RunQuery(UpdateEntitlement)
		

	elif obj == 'SAQSFE' and GetXMLsecField:
		if objectName == 'SAQTSE' and GetXMLsecField:
			Log.Info('fab_dict----'+str(grnbk_dict))
			get_value_query = Sql.GetList("select * from SAQSFB {} ".format(where_cond))
			updateentXML = ""
			for fab in get_value_query:
				where_condition = where_cond + " AND FABLOCATION_ID = '{}' ".format(fab.FABLOCATION_ID)
				get_equipment_count = Sql.GetFirst("select count(*) as cnt from SAQSCO {}".format(where_condition))
				for value in GetXMLsecField:
					get_value = value.ENTITLEMENT_DISPLAY_VALUE
					get_cost_impact = value.ENTITLEMENT_COST_IMPACT
					get_price_impact = value.ENTITLEMENT_PRICE_IMPACT
					get_currency = value.PRICE_METHOD
					get_calc_factor = value.CALCULATION_FACTOR 
					if value.ENTITLEMENT_TYPE == 'FreeInputNoMatching' and 'AGS_LAB_OPT' in value.ENTITLEMENT_NAME and 'Z0016' in get_serviceid:
						if get_value_query and value.ENTITLEMENT_DISPLAY_VALUE and value.ENTITLEMENT_NAME in grnbk_dict.keys() :
							get_calc_factor = get_value = int(round(float(grnbk_dict[value.ENTITLEMENT_NAME]) *	float(get_equipment_count.cnt)) )
							if value.ENTITLEMENT_COST_IMPACT and get_value:
								get_price_impact = get_value * float(value.ENTITLEMENT_COST_IMPACT)
							else:
								get_price_impact = 0.00
							#get_price_impact = get_value * float(value.ENTITLEMENT_COST_IMPACT)
						
						#Log.Info('get_cost_impact---'+str(value.ENTITLEMENT_NAME)+'---'+str(get_cost_impact))
					updateentXML  += """<QUOTE_ITEM_ENTITLEMENT>
							<ENTITLEMENT_NAME>{ent_name}</ENTITLEMENT_NAME>
							<ENTITLEMENT_VALUE_CODE>{ent_val_code}</ENTITLEMENT_VALUE_CODE>
							<ENTITLEMENT_DISPLAY_VALUE>{ent_disp_val}</ENTITLEMENT_DISPLAY_VALUE>
							<ENTITLEMENT_COST_IMPACT>{ct}</ENTITLEMENT_COST_IMPACT>
							<ENTITLEMENT_PRICE_IMPACT>{pi}</ENTITLEMENT_PRICE_IMPACT>
							<IS_DEFAULT>{is_default}</IS_DEFAULT>
							<ENTITLEMENT_TYPE>{ent_type}</ENTITLEMENT_TYPE>
							<ENTITLEMENT_DESCRIPTION>{ent_desc}</ENTITLEMENT_DESCRIPTION>
							<PRICE_METHOD>{pm}</PRICE_METHOD>
							<CALCULATION_FACTOR>{cf}</CALCULATION_FACTOR>
							</QUOTE_ITEM_ENTITLEMENT>""".format(ent_name = value.ENTITLEMENT_NAME,ent_val_code = value.ENTITLEMENT_VALUE_CODE,ent_disp_val = get_value ,ct = get_cost_impact ,pi = get_price_impact ,is_default = value.IS_DEFAULT ,ent_desc= value.ENTITLEMENT_DESCRIPTION ,pm = value.PRICE_METHOD ,cf= get_calc_factor , ent_type = value.ENTITLEMENT_TYPE)  
				Log.Info('updateentXML--fab1-'+str(updateentXML))
				UpdateEntitlement = " UPDATE {} SET ENTITLEMENT_XML= '{}', {} {} ".format(obj, updateentXML,update_fields,where_condition)
				
				Log.Info("UpdateEntitlement---"+str(" UPDATE {} SET ENTITLEMENT_XML= '', {} {} ".format(obj, update_fields,where_condition)))	
				Sql.RunQuery(UpdateEntitlement)
		else: 				
			if 'Z0007' in get_serviceid and objectName == 'SAQSCE':
				where_condition = SAQITMWhere.replace('A.','')
				#fab_val = where_cond.split('AND ')
				#where_condition += ' AND {}'.format( fab_val[len(fab_val)-1] )
				#Log.Info('where_condition-----1307--'+str(where_condition))	
				get_value_query = Sql.GetList("select QUOTE_RECORD_ID ,FABLOCATION_RECORD_ID, FABLOCATION_ID from SAQSFB {} ".format(where_condition) )
				
				for fab in get_value_query:
					where_condition = SAQITMWhere.replace('A.','')
					updateentXML = ""
					where_condition += " AND FABLOCATION_ID = '{}'".format(fab.FABLOCATION_ID )
					for value in GetXMLsecField:
						get_value = value.ENTITLEMENT_DISPLAY_VALUE
						get_price_impact = value.ENTITLEMENT_PRICE_IMPACT
						get_calc_factor = value.CALCULATION_FACTOR 
						get_cost_impact = value.ENTITLEMENT_COST_IMPACT
						
						if (value.ENTITLEMENT_TYPE in ('Drop Down','DropDown')  and value.ENTITLEMENT_COST_IMPACT):
							#GetXMLfab = Sql.GetFirst("select SUM(CASE WHEN Isnumeric(ENTITLEMENT_COST_IMPACT) = 1 THEN CONVERT(DECIMAL(18,2),ENTITLEMENT_COST_IMPACT) ELSE 0 END) AS ENTITLEMENT_COST_IMPACT,FABLOCATION_ID from (SELECT distinct e.QUOTE_RECORD_ID, e.FABLOCATION_RECORD_ID,e.EQUIPMENT_ID, e.FABLOCATION_ID ,replace(X.Y.value('(ENTITLEMENT_COST_IMPACT)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_COST_IMPACT,replace(X.Y.value('(ENTITLEMENT_NAME)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_NAME,replace(X.Y.value('(ENTITLEMENT_PRICE_IMPACT)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_PRICE_IMPACT FROM (select SAQSCE.EQUIPMENT_ID,SAQSCE.QUOTE_RECORD_ID as QUOTE_RECORD_ID, SAQSCE.FABLOCATION_RECORD_ID, SAQSCE.FABLOCATION_ID, CONVERT(xml, replace(cast(SAQSCE.ENTITLEMENT_XML as varchar(max)),'&','&amp;'), 2) as ENTITLEMENT_XML FROM SAQSCE (NOLOCK) {}) e OUTER APPLY e.ENTITLEMENT_XML.nodes('QUOTE_ITEM_ENTITLEMENT') as X(Y) ) IQ where ENTITLEMENT_NAME =  '{}' GROUP BY QUOTE_RECORD_ID, FABLOCATION_ID, FABLOCATION_RECORD_ID   ".format(where_condition,value.ENTITLEMENT_NAME))
							GetXMLfab = Sql.GetFirst("select SUM(CASE WHEN Isnumeric(ENTITLEMENT_COST_IMPACT) = 1 THEN CONVERT(DECIMAL(18,2),ENTITLEMENT_COST_IMPACT) ELSE 0 END) AS ENTITLEMENT_COST_IMPACT from (SELECT * FROM {pricetemp} {where_condition} AND ENTITLEMENT_NAME = '{ent_name}') IQ ".format(pricetemp = ent_temp,where_condition = where_condition,ent_name = value.ENTITLEMENT_NAME))
							if GetXMLfab:
								get_cost_impact = GetXMLfab.ENTITLEMENT_COST_IMPACT
							#Log.Info("get_calc_factor---"+str(get_calc_factor))
						updateentXML  += """<QUOTE_ITEM_ENTITLEMENT>
							<ENTITLEMENT_NAME>{ent_name}</ENTITLEMENT_NAME>
							<ENTITLEMENT_VALUE_CODE>{ent_val_code}</ENTITLEMENT_VALUE_CODE>
							<ENTITLEMENT_DISPLAY_VALUE>{ent_disp_val}</ENTITLEMENT_DISPLAY_VALUE>
							<ENTITLEMENT_COST_IMPACT>{ct}</ENTITLEMENT_COST_IMPACT>
							<ENTITLEMENT_PRICE_IMPACT>{pi}</ENTITLEMENT_PRICE_IMPACT>
							<IS_DEFAULT>{is_default}</IS_DEFAULT>
							<ENTITLEMENT_TYPE>{ent_type}</ENTITLEMENT_TYPE>
							<ENTITLEMENT_DESCRIPTION>{ent_desc}</ENTITLEMENT_DESCRIPTION>
							<PRICE_METHOD>{pm}</PRICE_METHOD>
							<CALCULATION_FACTOR>{cf}</CALCULATION_FACTOR>
							</QUOTE_ITEM_ENTITLEMENT>""".format(ent_name = value.ENTITLEMENT_NAME,ent_val_code = value.ENTITLEMENT_VALUE_CODE,ent_disp_val = get_value ,ct = get_cost_impact ,pi = get_price_impact ,is_default = value.IS_DEFAULT ,ent_desc= value.ENTITLEMENT_DESCRIPTION ,pm = value.PRICE_METHOD ,cf= get_calc_factor , ent_type = value.ENTITLEMENT_TYPE) 
					
					Log.Info('updateentXML--fab2-'+str(updateentXML))
				
					UpdateEntitlement = " UPDATE {} SET ENTITLEMENT_XML= '{}', {} {} ".format(obj, updateentXML,update_fields,where_condition)
								
					Sql.RunQuery(UpdateEntitlement)
			
			elif 'Z0016' in get_serviceid:
				where_condition = SAQITMWhere.replace('A.','')
				#fab_val = where_cond.split('AND ')
				#where_condition += ' AND {}'.format( fab_val[len(fab_val)-1] )
				#Log.Info('where_condition-----1307--'+str(where_condition))	
				get_value_query = Sql.GetList("select QUOTE_RECORD_ID ,FABLOCATION_RECORD_ID, FABLOCATION_ID from SAQSFB {} ".format(where_condition) )
				
				for fab in get_value_query:
					where_condition = SAQITMWhere.replace('A.','')
					updateentXML = ""
					where_condition += " AND FABLOCATION_ID = '{}'".format(fab.FABLOCATION_ID )
					GetXMLsec = Sql.GetList("select distinct ENTITLEMENT_NAME,IS_DEFAULT,case when ENTITLEMENT_TYPE in ('Check Box','CheckBox') then 'Check Box' else ENTITLEMENT_TYPE end as ENTITLEMENT_TYPE,ENTITLEMENT_DESCRIPTION,PRICE_METHOD,CASE WHEN Isnumeric(ENTITLEMENT_COST_IMPACT) = 1 THEN CONVERT(DECIMAL(18,2),ENTITLEMENT_COST_IMPACT) ELSE null END as ENTITLEMENT_COST_IMPACT from {} {}".format(ent_temp,where_condition))
					if GetXMLsec:
						for value in GetXMLsec:
							where_condtn = SAQITMWhere.replace('A.','')
							where_condtn += " AND ENTITLEMENT_NAME = '{}'".format(value.ENTITLEMENT_NAME) 
							#get_value_query = Sql.GetFirst("select * from {} {} ".format(ent_temp,where_condition) )
							get_cost_impact = value.ENTITLEMENT_COST_IMPACT
							get_currency = value.PRICE_METHOD
							GetXML = Sql.GetFirst("SELECT * from {} where ENTITLEMENT_NAME = '{}' ".format(ent_roll_temp,value.ENTITLEMENT_NAME))

							get_value = GetXML.ENTITLEMENT_DISPLAY_VALUE
							get_calc_factor = GetXML.CALCULATION_FACTOR 
							get_price_impact = GetXML.ENTITLEMENT_PRICE_IMPACT
							get_code = GetXML.ENTITLEMENT_VALUE_CODE
						
						
							if value.ENTITLEMENT_TYPE == 'FreeInputNoMatching' and 'AGS_LAB_OPT' in value.ENTITLEMENT_NAME:

								get_value_qry = Sql.GetFirst("select SUM(CASE WHEN Isnumeric(ENTITLEMENT_DISPLAY_VALUE) = 1 THEN CONVERT(DECIMAL(18,2),ENTITLEMENT_DISPLAY_VALUE) ELSE 0 END) AS ENTITLEMENT_DISPLAY_VALUE from {pricetemp} where ENTITLEMENT_NAME = '{ent_name}' ".format(pricetemp = ent_temp,where_condition = where_condtn,ent_name = value.ENTITLEMENT_NAME))

								if get_value_qry:
									#if get_value_diff != 0.00:
									get_calc_factor = get_value = int(round(float(get_value_qry.ENTITLEMENT_DISPLAY_VALUE) ) )
									if value.ENTITLEMENT_COST_IMPACT and get_value:
										get_price_impact = get_value * float(value.ENTITLEMENT_COST_IMPACT)
									else:
										get_price_impact = 0.00
									#get_price_impact = get_value * float(value.ENTITLEMENT_COST_IMPACT)
									
								else:
									get_calc_factor = get_value = GetXMLfab.ENTITLEMENT_DISPLAY_VALUE
									#get_cost_impact = GetXMLfab.ENTITLEMENT_COST_IMPACT
							elif value.ENTITLEMENT_TYPE in ('Check Box','CheckBox'):
								get_value_qry = Sql.GetList("select ENTITLEMENT_DISPLAY_VALUE,ENTITLEMENT_VALUE_CODE from {pricetemp} where ENTITLEMENT_NAME = '{ent_name}' ".format(pricetemp = ent_temp,ent_name = value.ENTITLEMENT_NAME))
								getvalue = []
								getcode = []
								for val in get_value_qry:
								#Trace.Write('ENTITLEMENT_NAME----'+str(i.ENTITLEMENT_NAME)+'--'+str(i.ENTITLEMENT_DISPLAY_VALUE))
									if val.ENTITLEMENT_VALUE_CODE:
										getcode.extend(eval(val.ENTITLEMENT_VALUE_CODE) )
										
									if val.ENTITLEMENT_DISPLAY_VALUE:
										getvalue.extend(eval(val.ENTITLEMENT_DISPLAY_VALUE) )
								get_val = list(set(getvalue) )
								get_cod = list(set(getcode))
								get_value = str(get_val).replace("'", '"')
								get_code = str(get_cod).replace("'", '"')
							updateentXML  += """<QUOTE_ITEM_ENTITLEMENT>
								<ENTITLEMENT_NAME>{ent_name}</ENTITLEMENT_NAME>
								<ENTITLEMENT_VALUE_CODE>{ent_val_code}</ENTITLEMENT_VALUE_CODE>
								<ENTITLEMENT_DISPLAY_VALUE>{ent_disp_val}</ENTITLEMENT_DISPLAY_VALUE>
								<ENTITLEMENT_COST_IMPACT>{ct}</ENTITLEMENT_COST_IMPACT>
								<ENTITLEMENT_PRICE_IMPACT>{pi}</ENTITLEMENT_PRICE_IMPACT>
								<IS_DEFAULT>{is_default}</IS_DEFAULT>
								<ENTITLEMENT_TYPE>{ent_type}</ENTITLEMENT_TYPE>
								<ENTITLEMENT_DESCRIPTION>{ent_desc}</ENTITLEMENT_DESCRIPTION>
								<PRICE_METHOD>{pm}</PRICE_METHOD>
								<CALCULATION_FACTOR>{cf}</CALCULATION_FACTOR>
								</QUOTE_ITEM_ENTITLEMENT>""".format(ent_name = value.ENTITLEMENT_NAME,ent_val_code = get_code,ent_disp_val = get_value ,ct = get_cost_impact ,pi = get_price_impact ,is_default = value.IS_DEFAULT ,ent_desc= value.ENTITLEMENT_DESCRIPTION ,pm = value.PRICE_METHOD ,cf= get_calc_factor, ent_type = value.ENTITLEMENT_TYPE)


					Log.Info('updateentXML--fab2-'+str(updateentXML))
				
					UpdateEntitlement = " UPDATE {} SET ENTITLEMENT_XML= '{}', {} {} ".format(obj, updateentXML,update_fields,where_condition)
								
					Sql.RunQuery(UpdateEntitlement)
			
			else:
				where_condition = SAQITMWhere.replace('A.','')
				fab_val = where_cond.split('AND ')
				where_condition += ' AND {}'.format( fab_val[len(fab_val)-1] )
				#Log.Info('where_condition-----1307--'+str(where_condition))	
				get_value_query = Sql.GetFirst("select QUOTE_RECORD_ID,convert(xml,replace(replace(ENTITLEMENT_XML,'&',';#38'),'''',';#39')) as ENTITLEMENT_XML from SAQSFE {} ".format(where_condition) )
				updateentXML = ""
				
				for value in GetXMLsecField:
					get_value = value.ENTITLEMENT_DISPLAY_VALUE
					get_price_impact = value.ENTITLEMENT_PRICE_IMPACT
					get_currency = value.PRICE_METHOD
					get_calc_factor = value.CALCULATION_FACTOR 
					get_cost_impact = value.ENTITLEMENT_COST_IMPACT
					if value.ENTITLEMENT_TYPE == 'FreeInputNoMatching' and 'AGS_LAB_OPT' in value.ENTITLEMENT_NAME and 'Z0016' in get_serviceid:
						if value.ENTITLEMENT_DISPLAY_VALUE:
							if value.ENTITLEMENT_NAME in get_prev_dict.keys():
								get_value_diff = float(value.ENTITLEMENT_DISPLAY_VALUE) -  float(get_prev_dict[value.ENTITLEMENT_NAME].split('||')[0])
								GetXMLfab = Sql.GetFirst("SELECT distinct e.QUOTE_RECORD_ID, replace(X.Y.value('(ENTITLEMENT_NAME)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_NAME,replace(X.Y.value('(IS_DEFAULT)[1]', 'VARCHAR(128)'),';#38','&') as IS_DEFAULT,replace(X.Y.value('(ENTITLEMENT_COST_IMPACT)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_COST_IMPACT,replace(X.Y.value('(CALCULATION_FACTOR)[1]', 'VARCHAR(128)'),';#38','&') as CALCULATION_FACTOR,replace(X.Y.value('(ENTITLEMENT_PRICE_IMPACT)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_PRICE_IMPACT,replace(X.Y.value('(ENTITLEMENT_TYPE)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_TYPE,replace(X.Y.value('(ENTITLEMENT_VALUE_CODE)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_VALUE_CODE,replace(X.Y.value('(ENTITLEMENT_DESCRIPTION)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_DESCRIPTION,replace(replace(X.Y.value('(ENTITLEMENT_DISPLAY_VALUE)[1]', 'VARCHAR(128)'),';#38','&'),';#39','''') as ENTITLEMENT_DISPLAY_VALUE FROM (select '"+str(get_value_query.QUOTE_RECORD_ID)+"' as QUOTE_RECORD_ID,convert(xml,'"+str(get_value_query.ENTITLEMENT_XML)+"') as ENTITLEMENT_XML ) e OUTER APPLY e.ENTITLEMENT_XML.nodes('QUOTE_ITEM_ENTITLEMENT') as X(Y) WHERE X.Y.value('(ENTITLEMENT_NAME)[1]', 'VARCHAR(128)') ='"+str(value.ENTITLEMENT_NAME)+"'  ")
								if get_value_diff != 0.00:
									get_calc_factor = get_value = int(round(float(GetXMLfab.ENTITLEMENT_DISPLAY_VALUE) + get_value_diff) )
									if value.ENTITLEMENT_COST_IMPACT and get_value:
										get_price_impact = get_value * float(value.ENTITLEMENT_COST_IMPACT)
									else:
										get_price_impact = 0.00
									#get_price_impact = get_value * float(value.ENTITLEMENT_COST_IMPACT)
								else:
									get_calc_factor = get_value = GetXMLfab.ENTITLEMENT_DISPLAY_VALUE
								Log.Info('get_value--fab-'+str(value.ENTITLEMENT_NAME)+'---'+str(get_value)+'---'+str(get_value_diff)+'---'+str(GetXMLfab.ENTITLEMENT_DISPLAY_VALUE))
					
					
					updateentXML  += """<QUOTE_ITEM_ENTITLEMENT>
						<ENTITLEMENT_NAME>{ent_name}</ENTITLEMENT_NAME>
						<ENTITLEMENT_VALUE_CODE>{ent_val_code}</ENTITLEMENT_VALUE_CODE>
						<ENTITLEMENT_DISPLAY_VALUE>{ent_disp_val}</ENTITLEMENT_DISPLAY_VALUE>
						<ENTITLEMENT_COST_IMPACT>{ct}</ENTITLEMENT_COST_IMPACT>
						<ENTITLEMENT_PRICE_IMPACT>{pi}</ENTITLEMENT_PRICE_IMPACT>
						<IS_DEFAULT>{is_default}</IS_DEFAULT>
						<ENTITLEMENT_TYPE>{ent_type}</ENTITLEMENT_TYPE>
						<ENTITLEMENT_DESCRIPTION>{ent_desc}</ENTITLEMENT_DESCRIPTION>
						<PRICE_METHOD>{pm}</PRICE_METHOD>
						<CALCULATION_FACTOR>{cf}</CALCULATION_FACTOR>
						</QUOTE_ITEM_ENTITLEMENT>""".format(ent_name = value.ENTITLEMENT_NAME,ent_val_code = value.ENTITLEMENT_VALUE_CODE,ent_disp_val = get_value ,ct = get_cost_impact ,pi = get_price_impact ,is_default = value.IS_DEFAULT ,ent_desc= value.ENTITLEMENT_DESCRIPTION ,pm = value.PRICE_METHOD ,cf= get_calc_factor , ent_type = value.ENTITLEMENT_TYPE) 
				
				Log.Info('updateentXML--fab2-'+str(updateentXML))
			
				UpdateEntitlement = " UPDATE {} SET ENTITLEMENT_XML= '{}', {} {} ".format(obj, updateentXML,update_fields,where_condition)
							
				Sql.RunQuery(UpdateEntitlement)
			

	elif obj == 'SAQSGE' and GetXMLsecField:
		if objectName == 'SAQSCE' and GetXMLsecField and 'Z0007' not in get_serviceid:
			where_condition = SAQITMWhere.replace('A.','')
			fab_val = where_cond.split('AND ')
			where_condition += ' AND {} AND {} '.format( fab_val[len(fab_val)-1], fab_val[len(fab_val)-2]  )
			#where_condition = " WHERE QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}' AND FABLOCATION_ID = '{}' AND GREENBOOK ='{}' ".format(self.ContractRecordId, serviceId, self.treeparentparam,self.treeparam)	
			get_value_query = Sql.GetFirst("select QUOTE_RECORD_ID,convert(xml,replace(replace(ENTITLEMENT_XML,'&',';#38'),'''',';#39')) as ENTITLEMENT_XML from SAQSGE {} ".format(where_condition) )
			updateentXML = ""
			for value in GetXMLsecField:
				get_value = value.ENTITLEMENT_DISPLAY_VALUE
				get_cost_impact = value.ENTITLEMENT_COST_IMPACT
				get_price_impact = value.ENTITLEMENT_PRICE_IMPACT
				#try:
				get_currency = value.PRICE_METHOD
				#except:
				#	get_currency = ""
				get_calc_factor = value.CALCULATION_FACTOR
				if value.ENTITLEMENT_TYPE == 'FreeInputNoMatching' and 'AGS_LAB_OPT' in value.ENTITLEMENT_NAME and 'Z0016' in get_serviceid:
					if value.ENTITLEMENT_DISPLAY_VALUE:
						if value.ENTITLEMENT_NAME in get_prev_dict.keys():
							get_value_diff = float(value.ENTITLEMENT_DISPLAY_VALUE) -  float(get_prev_dict[value.ENTITLEMENT_NAME].split('||')[0])
							
							GetXMLfab = Sql.GetFirst("SELECT distinct e.QUOTE_RECORD_ID, replace(X.Y.value('(ENTITLEMENT_NAME)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_NAME,replace(X.Y.value('(IS_DEFAULT)[1]', 'VARCHAR(128)'),';#38','&') as IS_DEFAULT,replace(X.Y.value('(ENTITLEMENT_COST_IMPACT)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_COST_IMPACT,replace(X.Y.value('(CALCULATION_FACTOR)[1]', 'VARCHAR(128)'),';#38','&') as CALCULATION_FACTOR,replace(X.Y.value('(ENTITLEMENT_PRICE_IMPACT)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_PRICE_IMPACT,replace(X.Y.value('(ENTITLEMENT_TYPE)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_TYPE,replace(X.Y.value('(ENTITLEMENT_VALUE_CODE)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_VALUE_CODE,replace(X.Y.value('(ENTITLEMENT_DESCRIPTION)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_DESCRIPTION,replace(replace(X.Y.value('(ENTITLEMENT_DISPLAY_VALUE)[1]', 'VARCHAR(128)'),';#38','&'),';#39','''') as ENTITLEMENT_DISPLAY_VALUE FROM (select '"+str(get_value_query.QUOTE_RECORD_ID)+"' as QUOTE_RECORD_ID,convert(xml,'"+str(get_value_query.ENTITLEMENT_XML)+"') as ENTITLEMENT_XML ) e OUTER APPLY e.ENTITLEMENT_XML.nodes('QUOTE_ITEM_ENTITLEMENT') as X(Y) WHERE X.Y.value('(ENTITLEMENT_NAME)[1]', 'VARCHAR(128)') ='"+str(value.ENTITLEMENT_NAME)+"'  ")
							if get_value_diff != 0.00:
								get_val = float(GetXMLfab.ENTITLEMENT_DISPLAY_VALUE) + get_value_diff
								if value.ENTITLEMENT_COST_IMPACT and get_val:
									get_price_impact = get_val * float(value.ENTITLEMENT_COST_IMPACT)
								else:
									get_price_impact = 0.00
								get_calc_factor = get_value = round(get_val,2)
							else:
								get_calc_factor = get_value = GetXMLfab.ENTITLEMENT_DISPLAY_VALUE
							#Log.Info('get_value--grn-'+str(value.ENTITLEMENT_NAME)+'---'+str(get_value)+'---'+str(get_value_diff)+'---'+str(GetXMLfab.ENTITLEMENT_DISPLAY_VALUE))

				updateentXML  += """<QUOTE_ITEM_ENTITLEMENT>
					<ENTITLEMENT_NAME>{ent_name}</ENTITLEMENT_NAME>
					<ENTITLEMENT_VALUE_CODE>{ent_val_code}</ENTITLEMENT_VALUE_CODE>
					<ENTITLEMENT_DISPLAY_VALUE>{ent_disp_val}</ENTITLEMENT_DISPLAY_VALUE>
					<ENTITLEMENT_COST_IMPACT>{ct}</ENTITLEMENT_COST_IMPACT>
					<ENTITLEMENT_PRICE_IMPACT>{pi}</ENTITLEMENT_PRICE_IMPACT>
					<IS_DEFAULT>{is_default}</IS_DEFAULT>
					<ENTITLEMENT_TYPE>{ent_type}</ENTITLEMENT_TYPE>
					<ENTITLEMENT_DESCRIPTION>{ent_desc}</ENTITLEMENT_DESCRIPTION>
					<PRICE_METHOD>{pm}</PRICE_METHOD>
					<CALCULATION_FACTOR>{cf}</CALCULATION_FACTOR>
					</QUOTE_ITEM_ENTITLEMENT>""".format(ent_name = value.ENTITLEMENT_NAME,ent_val_code = value.ENTITLEMENT_VALUE_CODE,ent_disp_val = get_value ,ct = get_cost_impact ,pi = get_price_impact ,is_default = value.IS_DEFAULT ,ent_desc= value.ENTITLEMENT_DESCRIPTION ,pm = value.PRICE_METHOD ,cf= get_calc_factor , ent_type = value.ENTITLEMENT_TYPE) 
			Log.Info('updateentXML--grn1-'+str(updateentXML))
			
			UpdateEntitlement = " UPDATE {} SET ENTITLEMENT_XML= '{}', {} {} ".format(obj, updateentXML,update_fields,where_condition)
						
			Sql.RunQuery(UpdateEntitlement)
		elif 'Z0007' in get_serviceid and objectName == 'SAQSCE':
			where_condition = SAQITMWhere.replace('A.','')
			#fab_val = where_cond.split('AND ')
			#where_condition += ' AND {}'.format( fab_val[len(fab_val)-1] )
			#Log.Info('where_condition-----1307--'+str(where_condition))	
			
			get_value_query = Sql.GetList("select FABLOCATION_ID,GREENBOOK,count(*) as cnt from SAQSCO {} group by FABLOCATION_ID,GREENBOOK ".format(where_cond ))
			for fab in get_value_query:
				updateentXML = ""
				where_condition = SAQITMWhere.replace('A.','')
				where_condition += " AND FABLOCATION_ID = '{}' and GREENBOOK = '{}'".format(fab.FABLOCATION_ID,fab.GREENBOOK )
				for value in GetXMLsecField:
					get_value = value.ENTITLEMENT_DISPLAY_VALUE
					get_price_impact = value.ENTITLEMENT_PRICE_IMPACT
					get_calc_factor = value.CALCULATION_FACTOR 
					get_cost_impact = value.ENTITLEMENT_COST_IMPACT
					
					if (value.ENTITLEMENT_TYPE in ('Drop Down','DropDown') and value.ENTITLEMENT_COST_IMPACT):
						#GetXMLfab = Sql.GetFirst("select SUM(CASE WHEN Isnumeric(ENTITLEMENT_COST_IMPACT) = 1 THEN CONVERT(DECIMAL(18,2),ENTITLEMENT_COST_IMPACT) ELSE 0 END) AS ENTITLEMENT_COST_IMPACT,FABLOCATION_ID,GREENBOOK from (SELECT distinct e.QUOTE_RECORD_ID, e.FABLOCATION_RECORD_ID, e.FABLOCATION_ID,e.GREENBOOK,e.EQUIPMENT_ID ,replace(X.Y.value('(ENTITLEMENT_COST_IMPACT)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_COST_IMPACT,replace(X.Y.value('(ENTITLEMENT_NAME)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_NAME,replace(X.Y.value('(ENTITLEMENT_PRICE_IMPACT)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_PRICE_IMPACT FROM (select SAQSCE.EQUIPMENT_ID,SAQSCE.QUOTE_RECORD_ID as QUOTE_RECORD_ID, SAQSCE.FABLOCATION_RECORD_ID, SAQSCE.FABLOCATION_ID,SAQSCE.GREENBOOK, CONVERT(xml, replace(cast(SAQSCE.ENTITLEMENT_XML as varchar(max)),'&','&amp;'), 2) as ENTITLEMENT_XML FROM SAQSCE (NOLOCK) {}) e OUTER APPLY e.ENTITLEMENT_XML.nodes('QUOTE_ITEM_ENTITLEMENT') as X(Y) ) IQ where ENTITLEMENT_NAME =  '{}' GROUP BY QUOTE_RECORD_ID, FABLOCATION_ID, FABLOCATION_RECORD_ID, GREENBOOK ".format(where_condition,value.ENTITLEMENT_NAME))
						GetXMLfab = Sql.GetFirst("select SUM(CASE WHEN Isnumeric(ENTITLEMENT_COST_IMPACT) = 1 THEN CONVERT(DECIMAL(18,2),ENTITLEMENT_COST_IMPACT) ELSE 0 END) AS ENTITLEMENT_COST_IMPACT from (SELECT * FROM {pricetemp} {where_condition} AND ENTITLEMENT_NAME = '{ent_name}') IQ ".format(pricetemp = ent_temp,where_condition = where_condition,ent_name = value.ENTITLEMENT_NAME))
						if GetXMLfab:
							get_cost_impact = GetXMLfab.ENTITLEMENT_COST_IMPACT
						#Log.Info("get_calc_factor---"+str(get_calc_factor))
					updateentXML  += """<QUOTE_ITEM_ENTITLEMENT>
						<ENTITLEMENT_NAME>{ent_name}</ENTITLEMENT_NAME>
						<ENTITLEMENT_VALUE_CODE>{ent_val_code}</ENTITLEMENT_VALUE_CODE>
						<ENTITLEMENT_DISPLAY_VALUE>{ent_disp_val}</ENTITLEMENT_DISPLAY_VALUE>
						<ENTITLEMENT_COST_IMPACT>{ct}</ENTITLEMENT_COST_IMPACT>
						<ENTITLEMENT_PRICE_IMPACT>{pi}</ENTITLEMENT_PRICE_IMPACT>
						<IS_DEFAULT>{is_default}</IS_DEFAULT>
						<ENTITLEMENT_TYPE>{ent_type}</ENTITLEMENT_TYPE>
						<ENTITLEMENT_DESCRIPTION>{ent_desc}</ENTITLEMENT_DESCRIPTION>
						<PRICE_METHOD>{pm}</PRICE_METHOD>
						<CALCULATION_FACTOR>{cf}</CALCULATION_FACTOR>
						</QUOTE_ITEM_ENTITLEMENT>""".format(ent_name = value.ENTITLEMENT_NAME,ent_val_code = value.ENTITLEMENT_VALUE_CODE,ent_disp_val = get_value ,ct = get_cost_impact ,pi = get_price_impact ,is_default = value.IS_DEFAULT ,ent_desc= value.ENTITLEMENT_DESCRIPTION ,pm = value.PRICE_METHOD ,cf= get_calc_factor , ent_type = value.ENTITLEMENT_TYPE) 
				
				Log.Info('updateentXML--fab2-'+str(updateentXML))
			
				UpdateEntitlement = " UPDATE {} SET ENTITLEMENT_XML= '{}', {} {} ".format(obj, updateentXML,update_fields,where_condition)
							
				Sql.RunQuery(UpdateEntitlement)
			
		elif 'Z0016' in get_serviceid and objectName == 'SAQSCE':
			where_condition = SAQITMWhere.replace('A.','')
			#fab_val = where_cond.split('AND ')
			#where_condition += ' AND {}'.format( fab_val[len(fab_val)-1] )
			#Log.Info('where_condition-----1307--'+str(where_condition))	
			
			get_value_query = Sql.GetList("select FABLOCATION_ID,GREENBOOK,count(*) as cnt from SAQSCO {} group by FABLOCATION_ID,GREENBOOK ".format(where_cond ))
			for fab in get_value_query:
				updateentXML = ""
				where_condition = SAQITMWhere.replace('A.','')
				where_condition += " AND FABLOCATION_ID = '{}' and GREENBOOK = '{}'".format(fab.FABLOCATION_ID,fab.GREENBOOK )
				GetXMLsec = Sql.GetList("select distinct ENTITLEMENT_NAME,IS_DEFAULT,case when ENTITLEMENT_TYPE in ('Check Box','CheckBox') then 'Check Box' else ENTITLEMENT_TYPE end as ENTITLEMENT_TYPE,ENTITLEMENT_DESCRIPTION,PRICE_METHOD,CASE WHEN Isnumeric(ENTITLEMENT_COST_IMPACT) = 1 THEN CONVERT(DECIMAL(18,2),ENTITLEMENT_COST_IMPACT) ELSE null END as ENTITLEMENT_COST_IMPACT from {} {}".format(ent_temp,where_condition))
				if GetXMLsec:
					for value in GetXMLsec:
						where_condtn = SAQITMWhere.replace('A.','')
						where_condtn += " AND ENTITLEMENT_NAME = '{}'".format(value.ENTITLEMENT_NAME) 
						#get_value_query = Sql.GetFirst("select * from {} {} ".format(ent_temp,where_condition) )
						get_cost_impact = value.ENTITLEMENT_COST_IMPACT
						get_currency = value.PRICE_METHOD
						GetXML = Sql.GetFirst("SELECT * from {} where ENTITLEMENT_NAME = '{}' ".format(ent_roll_temp,value.ENTITLEMENT_NAME))

						get_value = GetXML.ENTITLEMENT_DISPLAY_VALUE
						get_calc_factor = GetXML.CALCULATION_FACTOR 
						get_price_impact = GetXML.ENTITLEMENT_PRICE_IMPACT
						get_code = GetXML.ENTITLEMENT_VALUE_CODE
					
					
						if value.ENTITLEMENT_TYPE == 'FreeInputNoMatching' and 'AGS_LAB_OPT' in value.ENTITLEMENT_NAME:

							get_value_qry = Sql.GetFirst("select SUM(CASE WHEN Isnumeric(ENTITLEMENT_DISPLAY_VALUE) = 1 THEN CONVERT(DECIMAL(18,2),ENTITLEMENT_DISPLAY_VALUE) ELSE 0 END) AS ENTITLEMENT_DISPLAY_VALUE from {pricetemp} where ENTITLEMENT_NAME = '{ent_name}' ".format(pricetemp = ent_temp,where_condition = where_condtn,ent_name = value.ENTITLEMENT_NAME))

							if get_value_qry:
								#if get_value_diff != 0.00:
								get_calc_factor = get_value = int(round(float(get_value_qry.ENTITLEMENT_DISPLAY_VALUE) ) )
								if value.ENTITLEMENT_COST_IMPACT and get_value:
									get_price_impact = get_value * float(value.ENTITLEMENT_COST_IMPACT)
								else:
									get_price_impact = 0.00
								#get_price_impact = get_value * float(value.ENTITLEMENT_COST_IMPACT)
								
							else:
								get_calc_factor = get_value = GetXMLfab.ENTITLEMENT_DISPLAY_VALUE
								#get_cost_impact = GetXMLfab.ENTITLEMENT_COST_IMPACT
						elif value.ENTITLEMENT_TYPE in ('Check Box','CheckBox'):
							get_value_qry = Sql.GetList("select ENTITLEMENT_DISPLAY_VALUE,ENTITLEMENT_VALUE_CODE from {pricetemp} where ENTITLEMENT_NAME = '{ent_name}' ".format(pricetemp = ent_temp,ent_name = value.ENTITLEMENT_NAME))
							getvalue = []
							getcode = []
							for val in get_value_qry:
							#Trace.Write('ENTITLEMENT_NAME----'+str(i.ENTITLEMENT_NAME)+'--'+str(i.ENTITLEMENT_DISPLAY_VALUE))
								if val.ENTITLEMENT_VALUE_CODE:
									getcode.extend(eval(val.ENTITLEMENT_VALUE_CODE) )
									
								if val.ENTITLEMENT_DISPLAY_VALUE:
									getvalue.extend(eval(val.ENTITLEMENT_DISPLAY_VALUE) )
							get_val = list(set(getvalue) )
							get_cod = list(set(getcode))
							get_value = str(get_val).replace("'", '"')
							get_code = str(get_cod).replace("'", '"')
						updateentXML  += """<QUOTE_ITEM_ENTITLEMENT>
							<ENTITLEMENT_NAME>{ent_name}</ENTITLEMENT_NAME>
							<ENTITLEMENT_VALUE_CODE>{ent_val_code}</ENTITLEMENT_VALUE_CODE>
							<ENTITLEMENT_DISPLAY_VALUE>{ent_disp_val}</ENTITLEMENT_DISPLAY_VALUE>
							<ENTITLEMENT_COST_IMPACT>{ct}</ENTITLEMENT_COST_IMPACT>
							<ENTITLEMENT_PRICE_IMPACT>{pi}</ENTITLEMENT_PRICE_IMPACT>
							<IS_DEFAULT>{is_default}</IS_DEFAULT>
							<ENTITLEMENT_TYPE>{ent_type}</ENTITLEMENT_TYPE>
							<ENTITLEMENT_DESCRIPTION>{ent_desc}</ENTITLEMENT_DESCRIPTION>
							<PRICE_METHOD>{pm}</PRICE_METHOD>
							<CALCULATION_FACTOR>{cf}</CALCULATION_FACTOR>
							</QUOTE_ITEM_ENTITLEMENT>""".format(ent_name = value.ENTITLEMENT_NAME,ent_val_code = get_code,ent_disp_val = get_value ,ct = get_cost_impact ,pi = get_price_impact ,is_default = value.IS_DEFAULT ,ent_desc= value.ENTITLEMENT_DESCRIPTION ,pm = value.PRICE_METHOD ,cf= get_calc_factor, ent_type = value.ENTITLEMENT_TYPE)


				Log.Info('updateentXML--fab2-'+str(updateentXML))
			
				UpdateEntitlement = " UPDATE {} SET ENTITLEMENT_XML= '{}', {} {} ".format(obj, updateentXML,update_fields,where_condition)
							
				Sql.RunQuery(UpdateEntitlement)
			

		else:
			Log.Info('grnbk_dict----'+str(grnbk_dict))
			#where_condition = where_cond 
			get_value_query = Sql.GetList("select FABLOCATION_ID,GREENBOOK,count(*) as cnt from SAQSCO {} group by FABLOCATION_ID,GREENBOOK ".format(where_cond ))			
			for grnbk in get_value_query:
				# fab_dict[fab.FABLOCATION_ID] = fab.cnt
				where_condition = where_cond + "AND FABLOCATION_ID = '{}' AND GREENBOOK = '{}' ".format(grnbk.FABLOCATION_ID,grnbk.GREENBOOK)
				updateentXML = ""
				for value in GetXMLsecField:
					get_value = value.ENTITLEMENT_DISPLAY_VALUE
					get_cost_impact = value.ENTITLEMENT_COST_IMPACT
					get_price_impact = value.ENTITLEMENT_PRICE_IMPACT
					get_calc_factor = value.CALCULATION_FACTOR
					get_currency = value.PRICE_METHOD
					if value.ENTITLEMENT_TYPE == 'FreeInputNoMatching' and 'AGS_LAB_OPT' in value.ENTITLEMENT_NAME and 'Z0016' in get_serviceid:
						
						if get_value_query and value.ENTITLEMENT_DISPLAY_VALUE and value.ENTITLEMENT_NAME in grnbk_dict.keys() :
							get_val = float(grnbk_dict[value.ENTITLEMENT_NAME]) * float(grnbk.cnt)
							if value.ENTITLEMENT_COST_IMPACT and get_val:
								get_price_impact = get_val * float(value.ENTITLEMENT_COST_IMPACT)
							else:
								get_price_impact = 0.00
							get_calc_factor = get_value = round(get_val,2)
							#Log.Info('get_value--1-'+str(value.ENTITLEMENT_NAME)+'---'+str(get_value)+'--'+str(grnbk.cnt))
					updateentXML  += """<QUOTE_ITEM_ENTITLEMENT>
						<ENTITLEMENT_NAME>{ent_name}</ENTITLEMENT_NAME>
						<ENTITLEMENT_VALUE_CODE>{ent_val_code}</ENTITLEMENT_VALUE_CODE>
						<ENTITLEMENT_DISPLAY_VALUE>{ent_disp_val}</ENTITLEMENT_DISPLAY_VALUE>
						<ENTITLEMENT_COST_IMPACT>{ct}</ENTITLEMENT_COST_IMPACT>
						<ENTITLEMENT_PRICE_IMPACT>{pi}</ENTITLEMENT_PRICE_IMPACT>
						<IS_DEFAULT>{is_default}</IS_DEFAULT>
						<ENTITLEMENT_TYPE>{ent_type}</ENTITLEMENT_TYPE>
						<ENTITLEMENT_DESCRIPTION>{ent_desc}</ENTITLEMENT_DESCRIPTION>
						<PRICE_METHOD>{pm}</PRICE_METHOD>
						<CALCULATION_FACTOR>{cf}</CALCULATION_FACTOR>
						</QUOTE_ITEM_ENTITLEMENT>""".format(ent_name = value.ENTITLEMENT_NAME,ent_val_code = value.ENTITLEMENT_VALUE_CODE,ent_disp_val = get_value ,ct = get_cost_impact ,pi = get_price_impact ,is_default = value.IS_DEFAULT ,ent_desc= value.ENTITLEMENT_DESCRIPTION ,pm = value.PRICE_METHOD ,cf= get_calc_factor , ent_type = value.ENTITLEMENT_TYPE)  
				
				Log.Info('updateentXML--grn2-'+str(updateentXML))
				UpdateEntitlement = " UPDATE {} SET ENTITLEMENT_XML= '{}', {} {} ".format(obj, updateentXML,update_fields,where_condition)
				Log.Info('UpdateEntitlement_grn---'+str(" UPDATE {} SET ENTITLEMENT_XML= '', {} {} ".format(obj, update_fields,where_condition)))		
				Sql.RunQuery(UpdateEntitlement)

	elif obj == 'SAQSCE' and GetXMLsecField:
		# if objectName == 'SAQSGE':
		# 	get_fab_query = Sql.GetList("select FABLOCATION_ID,count(*) as cnt from SAQSGB  {} group by FABLOCATION_ID".format(where_cond))
		# 	for fab in get_fab_query:
		# 		fab_dict[fab.FABLOCATION_ID] = fab.cnt

		get_value_query = Sql.GetFirst("select count(*) as cnt from SAQSCO  {}   ".format(where_cond))
		
		# for grnbk in get_value_query:
		# 	where_condition = where_cond + " AND FABLOCATION_ID = '{}' AND GREENBOOK = '{}' ".format(grnbk.FABLOCATION_ID,grnbk.GREENBOOK)
		where_condition = where_cond
		updateentXML = ""
		for value in GetXMLsecField:
			get_value = value.ENTITLEMENT_DISPLAY_VALUE
			get_cost_impact = value.ENTITLEMENT_COST_IMPACT
			get_price_impact = value.ENTITLEMENT_PRICE_IMPACT
			get_calc_factor = value.CALCULATION_FACTOR
			#try:
			get_currency = value.PRICE_METHOD
			#except:
			#	get_currency = ""
			if value.ENTITLEMENT_TYPE == 'FreeInputNoMatching' and 'AGS_LAB_OPT' in value.ENTITLEMENT_NAME and 'Z0016' in get_serviceid:
				if get_value_query and value.ENTITLEMENT_DISPLAY_VALUE:
					get_val = float(value.ENTITLEMENT_DISPLAY_VALUE) / float(get_value_query.cnt)
					grnbk_dict[value.ENTITLEMENT_NAME] = get_val
					if value.ENTITLEMENT_COST_IMPACT and get_val:
						get_price_impact = get_val * float(value.ENTITLEMENT_COST_IMPACT)
					else:
						get_price_impact = 0.00
					get_calc_factor = get_value = round(get_val,2)
			updateentXML  += """<QUOTE_ITEM_ENTITLEMENT>
				<ENTITLEMENT_NAME>{ent_name}</ENTITLEMENT_NAME>
				<ENTITLEMENT_VALUE_CODE>{ent_val_code}</ENTITLEMENT_VALUE_CODE>
				<ENTITLEMENT_DISPLAY_VALUE>{ent_disp_val}</ENTITLEMENT_DISPLAY_VALUE>
				<ENTITLEMENT_COST_IMPACT>{ct}</ENTITLEMENT_COST_IMPACT>
				<ENTITLEMENT_PRICE_IMPACT>{pi}</ENTITLEMENT_PRICE_IMPACT>
				<IS_DEFAULT>{is_default}</IS_DEFAULT>
				<ENTITLEMENT_TYPE>{ent_type}</ENTITLEMENT_TYPE>
				<ENTITLEMENT_DESCRIPTION>{ent_desc}</ENTITLEMENT_DESCRIPTION>
				<PRICE_METHOD>{pm}</PRICE_METHOD>
				<CALCULATION_FACTOR>{cf}</CALCULATION_FACTOR>
				</QUOTE_ITEM_ENTITLEMENT>""".format(ent_name = value.ENTITLEMENT_NAME,ent_val_code = value.ENTITLEMENT_VALUE_CODE,ent_disp_val = get_value ,ct = get_cost_impact ,pi = get_price_impact ,is_default = value.IS_DEFAULT ,ent_desc= value.ENTITLEMENT_DESCRIPTION ,pm = value.PRICE_METHOD ,cf= get_calc_factor , ent_type = value.ENTITLEMENT_TYPE) 
		Log.Info('updateentXML--equp-'+str(updateentXML))
		UpdateEntitlement = " UPDATE {} SET ENTITLEMENT_XML= '{}', {} {} ".format(obj, updateentXML,update_fields,where_condition)
		Log.Info("UpdateEntitlement_tst---"+" UPDATE {} SET ENTITLEMENT_XML= '', {} {} ".format(obj,update_fields,where_condition))
		Sql.RunQuery(UpdateEntitlement)

		##temp table creation for z0016
		if 'Z0016' in get_serviceid:
			where_condition = SAQITMWhere.replace('A.','').replace("'","''")
			#get_c4c_quote_id = Sql.GetFirst("select * from SAQTMT where MASTER_TABLE_QUOTE_RECORD_ID = '{}'".format(getinnercon.QUOTE_RECORD_ID))
			ent_temp = "SAQSCE_ENT1_BKP_"+str(get_c4c_quote_id.C4C_QUOTE_ID)
			ent_temp_drop = Sql.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(ent_temp)+"'' ) BEGIN DROP TABLE "+str(ent_temp)+" END  ' ")
			Sql.GetFirst("sp_executesql @T=N'declare @H int; Declare @val Varchar(MAX);DECLARE @XML XML; SELECT @val =  replace(replace(STUFF((SELECT ''''+FINAL from(select  REPLACE(entitlement_xml,''<QUOTE_ITEM_ENTITLEMENT>'',sml) AS FINAL FROM (select ''  <QUOTE_ITEM_ENTITLEMENT><QUOTE_ID>''+quote_id+''</QUOTE_ID><QUOTE_RECORD_ID>''+QUOTE_RECORD_ID+''</QUOTE_RECORD_ID><SERVICE_ID>''+service_id+''</SERVICE_ID><FABLOCATION_ID>''+FABLOCATION_ID+''</FABLOCATION_ID><GREENBOOK>''+GREENBOOK+''</GREENBOOK><EQUIPMENT_ID>''+equipment_id+''</EQUIPMENT_ID>'' AS sml,replace(entitlement_xml,''&'','';#38'')  as entitlement_xml from SAQSCE(nolock) "+str(where_condition)+" )A )a FOR XML PATH ('''')), 1, 1, ''''),''&lt;'',''<''),''&gt;'',''>'')  SELECT @XML = CONVERT(XML,''<ROOT>''+@VAL+''</ROOT>'') exec sys.sp_xml_preparedocument @H output,@XML; select QUOTE_ID,QUOTE_RECORD_ID,EQUIPMENT_ID,SERVICE_ID,ENTITLEMENT_NAME,ENTITLEMENT_COST_IMPACT,FABLOCATION_ID,GREENBOOK,ENTITLEMENT_VALUE_CODE,ENTITLEMENT_DISPLAY_VALUE,ENTITLEMENT_PRICE_IMPACT,IS_DEFAULT,ENTITLEMENT_TYPE,ENTITLEMENT_DESCRIPTION,PRICE_METHOD,CALCULATION_FACTOR INTO "+str(ent_temp)+"  from openxml(@H, ''ROOT/QUOTE_ITEM_ENTITLEMENT'', 0) with (QUOTE_ID VARCHAR(100) ''QUOTE_ID'',QUOTE_RECORD_ID VARCHAR(100) ''QUOTE_RECORD_ID'',EQUIPMENT_ID VARCHAR(100) ''EQUIPMENT_ID'',ENTITLEMENT_NAME VARCHAR(100) ''ENTITLEMENT_NAME'',SERVICE_ID VARCHAR(100) ''SERVICE_ID'',ENTITLEMENT_COST_IMPACT VARCHAR(100) ''ENTITLEMENT_COST_IMPACT'',FABLOCATION_ID VARCHAR(100) ''FABLOCATION_ID'',GREENBOOK VARCHAR(100) ''GREENBOOK'',ENTITLEMENT_VALUE_CODE VARCHAR(100) ''ENTITLEMENT_VALUE_CODE'',ENTITLEMENT_DISPLAY_VALUE VARCHAR(100) ''ENTITLEMENT_DISPLAY_VALUE'',ENTITLEMENT_PRICE_IMPACT VARCHAR(100) ''ENTITLEMENT_PRICE_IMPACT'',IS_DEFAULT VARCHAR(100) ''IS_DEFAULT'',ENTITLEMENT_TYPE VARCHAR(100) ''ENTITLEMENT_TYPE'',ENTITLEMENT_DESCRIPTION VARCHAR(100) ''ENTITLEMENT_DESCRIPTION'',PRICE_METHOD VARCHAR(100) ''PRICE_METHOD'',CALCULATION_FACTOR VARCHAR(100) ''CALCULATION_FACTOR'') ; exec sys.sp_xml_removedocument @H; '")



	else:
		Log.Info('else part roll down')
		update_field_str = ""
		update_query = """ UPDATE TGT 
		SET TGT.ENTITLEMENT_XML = SRC.ENTITLEMENT_XML,
		TGT.CPS_MATCH_ID = SRC.CPS_MATCH_ID,
		TGT.CPS_CONFIGURATION_ID = SRC.CPS_CONFIGURATION_ID,
		TGT.CpqTableEntryModifiedBy = {},
		TGT.CpqTableEntryDateModified = '{}'
		{}
		FROM {} (NOLOCK) SRC JOIN {} (NOLOCK) TGT 
		ON  TGT.QUOTE_RECORD_ID = SRC.QUOTE_RECORD_ID AND TGT.SERVICE_ID = SRC.SERVICE_ID {} {} """.format(userId,datetimenow,update_field_str,objectName,obj,join,where)
		Sql.RunQuery(update_query)
		

	##roll down and up for all levels ends
	if obj == "SAQSCE" or objectName == "SAQSCE":            
		where_string_splitted = ''
		where_str = where.split('AND')
		if where_str:
			where_string_splitted = 'AND'.join(where_str[0:2])
		Log.Info("""UPDATE SAQSCE
							SET
							ENTITLEMENT_GROUP_ID = OQ.RowNo                            
							FROM SAQSCE (NOLOCK)
							INNER JOIN (
								SELECT *, ROW_NUMBER()OVER(ORDER BY IQ.QUOTE_RECORD_ID) AS RowNo  FROM (
								SELECT DISTINCT SRC.QUOTE_RECORD_ID, SRC.SERVICE_ID, SRC.ENTITLEMENT_XML
								FROM SAQSCE (NOLOCK) SRC
								JOIN MAMTRL ON MAMTRL.SAP_PART_NUMBER = SRC.SERVICE_ID AND MAMTRL.SERVICE_TYPE = 'NON TOOL BASED'
								{WhereString} )AS IQ
							)AS OQ
							ON OQ.QUOTE_RECORD_ID = SAQSCE.QUOTE_RECORD_ID AND OQ.SERVICE_ID = SAQSCE.SERVICE_ID AND OQ.ENTITLEMENT_XML = SAQSCE.ENTITLEMENT_XML""".format(WhereString=where_string_splitted))
		Sql.RunQuery("""UPDATE SAQSCE
							SET
							ENTITLEMENT_GROUP_ID = OQ.RowNo                            
							FROM SAQSCE (NOLOCK)
							INNER JOIN (
								SELECT *, ROW_NUMBER()OVER(ORDER BY IQ.QUOTE_RECORD_ID) AS RowNo  FROM (
								SELECT DISTINCT SRC.QUOTE_RECORD_ID, SRC.SERVICE_ID, SRC.ENTITLEMENT_XML
								FROM SAQSCE (NOLOCK) SRC
								JOIN MAMTRL ON MAMTRL.SAP_PART_NUMBER = SRC.SERVICE_ID AND MAMTRL.SERVICE_TYPE = 'NON TOOL BASED'
								{WhereString} )AS IQ
							)AS OQ
							ON OQ.QUOTE_RECORD_ID = SAQSCE.QUOTE_RECORD_ID AND OQ.SERVICE_ID = SAQSCE.SERVICE_ID AND OQ.ENTITLEMENT_XML = SAQSCE.ENTITLEMENT_XML""".format(WhereString=where_string_splitted))


	for attribute in attributeList:
		if "calc" in attribute:
			attribute = attribute.replace("_calc","")
		
		
		
		
		
		# update_query = """ UPDATE TGT 
		# 	SET TGT.ENTITLEMENT_XML = SRC.ENTITLEMENT_XML,
		# 	TGT.CPS_MATCH_ID = SRC.CPS_MATCH_ID,
		# 	TGT.CPS_CONFIGURATION_ID = SRC.CPS_CONFIGURATION_ID,
		# 	TGT.CpqTableEntryModifiedBy = {},
		# 	TGT.CpqTableEntryDateModified = '{}'
		# 	{}
		# 	FROM {} (NOLOCK) SRC JOIN {} (NOLOCK) TGT 
		# 	ON  TGT.QUOTE_RECORD_ID = SRC.QUOTE_RECORD_ID AND TGT.SERVICE_ID = SRC.SERVICE_ID {} {} """.format(userId,datetimenow,update_field_str,objectName,obj,join,where)
		#Log.Info("ENTITLEMENT IFLOW-548-------update_query-------------- "+str(update_query))
		#Sql.RunQuery(update_query)
		#Log.Info("ENTITLEMENT IFLOW--update_query1-- "+str(update_query1))
		
		#update SAQICO after reprice based on entitlement 
		if obj == 'SAQIEN' and attribute == 'ADDL_PERF_GUARANTEE_91_1':
			where_condition = where.replace('SRC.ENTITLEMENT_NAME','SAQIEN.ENTITLEMENT_NAME').replace('SRC.QUOTE_RECORD_ID','SAQICO.QUOTE_RECORD_ID').replace('SRC.SERVICE_ID','SAQICO.SERVICE_ID').replace('SRC.FABLOCATION_ID','SAQICO.FABLOCATION_ID').replace('SRC.GREENBOOK','SAQICO.GREENBOOK').replace('SRC.EQUIPMENT_ID','SAQICO.EQUIPMENT_ID')
			#Log.Info('452---SAQICO-where_condition---'+str(where_condition))
			update_entitlement_price_impact(where_condition)
	
#Log.Info('Log before calling ftscostcalc--')
#FTSCostCalc("SAQTSE")
if ent_temp:
	ent_temp_drop = Sql.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(ent_temp)+"'' ) BEGIN DROP TABLE "+str(ent_temp)+" END  ' ")
if ent_roll_temp:
	ent_temp_drop1 = Sql.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(ent_roll_temp)+"'' ) BEGIN DROP TABLE "+str(ent_roll_temp)+" END  ' ")
#Log.Info("level1---"+str(level))
sendEmail(level)



# =========================================================================================================================================
#   __script_name : QTPOSTPTPR.PY(AMAT)
#   __script_description : THIS SCRIPT IS USED TO UPDATE PART PRICING RESPONCE FROM CPS TO CPQ.
#   __primary_author__ : BAJI
#   __create_date :
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import clr
#clr.AddReference("System.Net")
clr.AddReference("IronPython")
clr.AddReference("Microsoft.Scripting")
from System.Net import WebRequest
from System.Net import HttpWebResponse
from Microsoft.Scripting import SourceCodeKind
from IronPython.Hosting import Python

import System.Net
import sys
import datetime
import time
from SYDATABASE import SQL

Sql = SQL()
Log.Info("QTPOSTPTPR hitting from CPI --->")
Log.Info('iflow script called---- QTPOST')
try:
	start_time = time.time()
	if 'Param' in globals(): 
		Lst_resp = []
		Resp_msg = {}
		Sucess = ""
		Error = ""
		SC_PartNumber_Data = ""
		
		if hasattr(Param, 'CPQ_Columns'): 
		
			rebuilt_data = {}
			primaryQueryItems = SqlHelper.GetFirst("SELECT NEWID() AS A")
			for table_dict in Param.CPQ_Columns: 
				tbl = str(table_dict.Key)
				
				#Table_Names.append(tbl)
				colu_Info = {}
				uu = []         
				for record_dict in table_dict.Value:
					tyty = str(type(record_dict))
					if str(tyty) == "<type 'KeyValuePair[str, object]'>":
						j = record_dict
						
						j_Valu = j.Value
						
						if "&#34;" in j_Valu:
							j_Valu =  j_Valu.replace("&#34;","\"")
						if "&#39;" in j_Valu:
							j_Valu = j_Valu.replace("&#39;" , "\'")
						if "&#92;" in j_Valu:
							j_Valu = j_Valu.replace("&#92;" , "\\")                 
						
						colu_Info[str(j.Key)] = j_Valu
					else:
						colu_Info1 = {}
						for j in record_dict:
							j_Valu = j.Value    
							
							j_key = str(j.Key)
							
							if "&#34;" in j_Valu:
								j_Valu =  j_Valu.replace("&#34;","\"")
							if "&#39;" in j_Valu:
								j_Valu = j_Valu.replace("&#39;" , "\'")
							if "&#92;" in j_Valu:
								j_Valu = j_Valu.replace("&#92;" , "\\") 
												
							colu_Info1[str(j.Key)] = j_Valu 			
						uu.append(colu_Info1)
				#Log.Info("7575 uu --->"+str(uu))			
				if len(colu_Info) !=  0:    
					rebuilt_data[tbl] = [colu_Info]
						
				if len(uu) !=  0:   
					rebuilt_data[tbl] = uu


			response1 = rebuilt_data
			Log.Info("response1 5858---->")
			Log.Info("response1 5858---->"+str(response1))

			price = []
			QUOTE = ''

			for root, value in response1.items():
				for root1 in value:
					for inv in root1:			
						if inv == "items":
							#Log.Info("6666 i[u] --->"+str(list(root1[inv])))
							price = root1[inv]			 
							break
					
			insert_data = []
			batch_group_record_id = str(Guid.NewGuid()).upper()
			contract_quote_record_id = None				


			Log.Info("456 type(price) --->")
			if str(type(price)) == "<type 'Dictionary[str, object]'>":
				#Log.Info("type condition--->")
				price = [price]
			#Log.Info("456789 type(price) --->"+str(type(price)))
			for i in price:		
				Itemidinfo = str(i["itemId"]).split(";")
				Log.Info("456 Itemidinfo --->"+str(Itemidinfo))
				QUOTE = str(Itemidinfo[1])
				currencyType = str(Itemidinfo[3])
				contract_quote_record_id = None		
				Taxrate = ''
				Taxvalue = ''		
				GetPricingProcedure = Sql.GetFirst("SELECT EXCHANGE_RATE_TYPE,DIVISION_ID, DISTRIBUTIONCHANNEL_ID, SALESORG_ID, GLOBAL_CURRENCY, PRICINGPROCEDURE_ID, QUOTE_RECORD_ID FROM SAQTRV (NOLOCK) WHERE QUOTE_ID = '{}'".format(QUOTE))
				getservicerecord = Sql.GetFirst("select QUOTE_NAME,SERVICE_DESCRIPTION,SERVICE_ID,	SERVICE_RECORD_ID from SAQTSE (NOLOCK) where QUOTE_ID = '{}'".format(QUOTE))
				if GetPricingProcedure is not None:
					#PricingProcedure = GetPricingProcedure.PRICINGPROCEDURE_ID
					PricingProcedure = GetPricingProcedure.PRICINGPROCEDURE_ID
					curr = GetPricingProcedure.GLOBAL_CURRENCY
					dis = GetPricingProcedure.DISTRIBUTIONCHANNEL_ID
					salesorg = GetPricingProcedure.SALESORG_ID
					div = GetPricingProcedure.DIVISION_ID
					exch = GetPricingProcedure.EXCHANGE_RATE_TYPE
					contract_quote_record_id = GetPricingProcedure.QUOTE_RECORD_ID
				#Log.Info("123 i[conditions] -->"+str(type(i['conditions'])))
				Taxrate = '0.00'
				getuomrec_val =''
				'''
				QuoteItemList = Quote.QuoteTables["SAQICD"]
				if str(type(i['conditions'])) == "<type 'ArrayList'>":
					for cond_info in i['conditions']:
						Log.Info("333 cond_info['conditionType'] --->")
						getuomrec = Sql.GetFirst("select UOM_RECORD_ID from MAMTRL where UNIT_OF_MEASURE = '"+str(cond_info['conditionUnit'])+"'")
						newRow = QuoteItemList.AddNewRow()
						newRow['CONDITION_COUNTER'] = cond_info['conditionCounter']
						newRow['CONDITION_DATA_TYPE'] =  cond_info['conditionType']
						newRow['CONDITION_RATE'] = cond_info['conditionRate'].strip()
						newRow['CONDITION_TYPE'] = cond_info['conditionType']
						newRow['CONDITIONTYPE_NAME'] = cond_info['conditionTypeDescription'].strip()
						newRow['UOM'] =  cond_info['conditionUnit']
						newRow['CONDITIONTYPE_RECORD_ID'] = ''
						newRow['CONDITION_VALUE'] = cond_info['conditionValue']
						newRow['UOM_RECORD_ID'] = getuomrec.UOM_RECORD_ID
						newRow['LINE'] = ''
						newRow['QTEITM_RECORD_ID'] = ''
						newRow['QUOTE_NAME'] = getservicerecord.QUOTE_NAME
						newRow['SERVICE_DESCRIPTION'] = getservicerecord.SERVICE_DESCRIPTION
						newRow['SERVICE_ID'] = getservicerecord.SERVICE_ID
						newRow['STEP_NUMBER'] = cond_info['stepNo']
						newRow['SERVICE_RECORD_ID'] = getservicerecord.SERVICE_RECORD_ID
						newRow['QUOTE_RECORD_ID'] = contract_quote_record_id
						newRow['QUOTE_ID'] = QUOTE
						getuomrec = Sql.GetFirst("select UOM_RECORD_ID from MAMTRL where UNIT_OF_MEASURE = '"+str(cond_info['conditionUnit'])+"'")
						if getuomrec:
							getuomrec_val = getuomrec.UOM_RECORD_ID
						else:
							getuomrec_val = 'EA'
						saqicd_insert = SqlHelper.GetFirst("sp_executesql @T=N'INSERT QT__SAQICD (CONDITION_COUNTER,CONDITION_DATA_TYPE,CONDITION_RATE,CONDITION_TYPE,CONDITIONTYPE_NAME,CONDITIONTYPE_RECORD_ID,UOM,CONDITION_VALUE,UOM_RECORD_ID,LINE,QUOTE_ID,QTEITM_RECORD_ID,QUOTE_NAME,SERVICE_DESCRIPTION,SERVICE_ID,STEP_NUMBER,SERVICE_RECORD_ID,QUOTE_RECORD_ID,CONDITION_CURRENCY,CONDITION_BASE) values (''"+str(cond_info['conditionCounter'])+"'',''"+str(cond_info['calculationType'])+"'',''"+str(cond_info['conditionRate'].strip())+"'',''"+str(cond_info['conditionType'])+ "'',''"+ str(cond_info['conditionTypeDescription'].strip())+ "'' , ''"+ str(cond_info['conditionUnitValue'])+ "'',''"+ str(cond_info['conditionUnit'])+ "'',''"+ str(cond_info['conditionValue'])+ "'',''"+ str(getuomrec_val)+ "'','''',''"+ str(QUOTE)+ "'','''',''"+ str(getservicerecord.QUOTE_NAME)+ "'',''"+ str(getservicerecord.SERVICE_DESCRIPTION)+ "'',''"+ str(getservicerecord.SERVICE_ID)+ "'',''"+ str(cond_info['stepNo'])+ "'',''"+ str(getservicerecord.SERVICE_RECORD_ID)+ "'',''"+ str(getservicerecord.QUOTE_RECORD_ID)+ "'',''"+str(cond_info['conditionCurrency'])+"'',''"+str(cond_info['conditionBase'])+"'')'")
						if str(cond_info['conditionType']).upper() == 'ZWSC':
							Taxrate = cond_info['conditionRate']		
							if Taxrate == '':
									Taxrate = '0.00'
					QuoteItemList.Save()					
				'''
				
				insert_data.append((str(Guid.NewGuid()).upper(), Itemidinfo[0], Itemidinfo[-2], i["netPrice"], 'IN PROGRESS', QUOTE, contract_quote_record_id, batch_group_record_id,str(Taxrate)))
			
			#Log.Info("4521 batch_group_record_id --->"+str(batch_group_record_id))
			#Log.Info("4521 contract_quote_record_id --->"+str(contract_quote_record_id))
			getpartsdata = Sql.GetFirst("select * from SAQIFP where QUOTE_RECORD_ID = '"+str(contract_quote_record_id)+"'")
			if getpartsdata:
				Sql.RunQuery("INSERT INTO SYSPBT (BATCH_RECORD_ID, SAP_PART_NUMBER, QUANTITY, UNIT_PRICE, BATCH_STATUS, QUOTE_ID, QUOTE_RECORD_ID, BATCH_GROUP_RECORD_ID,TAXRATE) VALUES {}".format(', '.join(map(str, insert_data))))			
				Log.Info('getpartsdata -->'+str(getpartsdata.PART_NUMBER))
			
				
				if currencyType == 'docCurrency':
					Sql.RunQuery("""UPDATE SAQSPT SET UNIT_PRICE = SYSPBT.UNIT_PRICE ,EXTENDED_UNIT_PRICE = SYSPBT.UNIT_PRICE * SYSPBT.QUANTITY FROM SAQSPT 				
							JOIN SYSPBT (NOLOCK) ON SYSPBT.SAP_PART_NUMBER = SAQSPT.PART_NUMBER AND SYSPBT.QUOTE_RECORD_ID = SAQSPT.QUOTE_RECORD_ID
							WHERE SAQSPT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}'
						""".format(BatchGroupRecordId=batch_group_record_id, QuoteRecordId=contract_quote_record_id))
					Sql.RunQuery("""UPDATE SAQIFP
							SET PRICING_STATUS = 'ACQUIRED',TAX = (SYSPBT.UNIT_PRICE * SYSPBT.QUANTITY)- ((SYSPBT.UNIT_PRICE * SYSPBT.QUANTITY)/(1 +(convert(decimal(13,5),SYSPBT.TAXRATE)/100))),TAX_PERCENTAGE = convert(decimal(13,5),CASE WHEN ISNULL(SYSPBT.TAXRATE,'')='' THEN NULL ELSE SYSPBT.TAXRATE END) ,EXTENDED_PRICE = SYSPBT.UNIT_PRICE * SYSPBT.QUANTITY,UNIT_PRICE = (SYSPBT.UNIT_PRICE * SYSPBT.QUANTITY)/(1 +(convert(decimal(13,5),SYSPBT.TAXRATE)/100))
							FROM SAQIFP 				
							JOIN SYSPBT (NOLOCK) ON SYSPBT.SAP_PART_NUMBER = SAQIFP.PART_NUMBER AND SYSPBT.QUOTE_RECORD_ID = SAQIFP.QUOTE_RECORD_ID
							WHERE SAQIFP.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}'
						""".format(BatchGroupRecordId=batch_group_record_id, QuoteRecordId=contract_quote_record_id))
					GetSum = SqlHelper.GetFirst( "SELECT SUM(UNIT_PRICE_INGL_CURR) AS TOTAL FROM SAQIFP WHERE QUOTE_ID = '{}' ".format(QUOTE))
					Log.Info("QTPOSTPTPR TOTAL ==> "+str(GetSum.TOTAL))					
					Sql.RunQuery("""UPDATE SAQRIT SET STATUS='ACQUIRED', UNIT_PRICE_INGL_CURR = SAQIFP.UNIT_PRICE, NET_PRICE_INGL_CURR={total} FROM SAQRIT
					JOIN SAQIFP (NOLOCK) ON SAQIFP.PART_NUMBER = SAQRIT.OBJECT_ID AND SAQIFP.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID WHERE SAQRIT.QUOTE_RECORD_ID = '{QuoteRecordId}' SAQRIT.OBJECT_ID='{PartNo}'""".format(total=GetSum.TOTAL, QuoteRecordId=contract_quote_record_id,PartNo=getpartsdata.PART_NUMBER))
					
				else:
					Sql.RunQuery("""UPDATE SAQSPT SET UNIT_PRICE = SYSPBT.UNIT_PRICE ,EXTENDED_UNIT_PRICE = SYSPBT.UNIT_PRICE * SYSPBT.QUANTITY FROM SAQSPT 				
							JOIN SYSPBT (NOLOCK) ON SYSPBT.SAP_PART_NUMBER = SAQSPT.PART_NUMBER AND SYSPBT.QUOTE_RECORD_ID = SAQSPT.QUOTE_RECORD_ID
							WHERE SAQSPT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}'
						""".format(BatchGroupRecordId=batch_group_record_id, QuoteRecordId=contract_quote_record_id))
					Sql.RunQuery("""UPDATE SAQIFP
							SET PRICING_STATUS = 'ACQUIRED',TAX_AMOUNT_INGL_CURR = (SYSPBT.UNIT_PRICE * SYSPBT.QUANTITY)- ((SYSPBT.UNIT_PRICE * SYSPBT.QUANTITY)/(1 +(convert(decimal(13,5),SYSPBT.TAXRATE)/100))),UNIT_PRICE_INGL_CURR = (SYSPBT.UNIT_PRICE * SYSPBT.QUANTITY)/(1 +(convert(decimal(13,5),SYSPBT.TAXRATE)/100))
							FROM SAQIFP 				
							JOIN SYSPBT (NOLOCK) ON SYSPBT.SAP_PART_NUMBER = SAQIFP.PART_NUMBER AND SYSPBT.QUOTE_RECORD_ID = SAQIFP.QUOTE_RECORD_ID
							WHERE SAQIFP.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}'
						""".format(BatchGroupRecordId=batch_group_record_id, QuoteRecordId=contract_quote_record_id))
					
					GetSum = SqlHelper.GetFirst( "SELECT SUM(UNIT_PRICE_INGL_CURR) AS TOTAL FROM SAQIFP WHERE QUOTE_ID = '{}' ".format(QUOTE))
					Log.Info("QTPOSTPTPR TOTAL ==> "+str(GetSum.TOTAL))
					Sql.RunQuery("""UPDATE SAQRIT SET STATUS='ACQUIRED', UNIT_PRICE_INGL_CURR = SAQIFP.UNIT_PRICE, NET_PRICE_INGL_CURR={total} FROM SAQRIT
					JOIN SAQIFP (NOLOCK) ON SAQIFP.PART_NUMBER = SAQRIT.OBJECT_ID AND SAQIFP.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID WHERE SAQRIT.QUOTE_RECORD_ID = '{QuoteRecordId}' SAQRIT.OBJECT_ID='{PartNo}'""".format(total=GetSum.TOTAL, QuoteRecordId=contract_quote_record_id,PartNo=getpartsdata.PART_NUMBER))
					
				
				Sql.RunQuery(
							"""DELETE FROM SYSPBT WHERE SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}' and SYSPBT.BATCH_STATUS = 'IN PROGRESS'""".format(
								BatchGroupRecordId=batch_group_record_id
							)
						)
				end_time = time.time() 
				Log.Info("CPS PRICING end==> "+str(end_time - start_time) +" QUOTE REC ID----"+str(contract_quote_record_id))
				'''
				#UPDATE QUOTE TABLE SAQIFP
				try:
					update_quote = """UPDATE QT__QTQIFP SET UNIT_PRICE = SAQIFP.UNIT_PRICE, EXTENDED_UNIT_PRICE = SAQIFP.EXTENDED_PRICE,TAX =SAQIFP.TAX  FROM SAQIFP INNER JOIN QT__QTQIFP ON  SAQIFP.PART_NUMBER = QT__QTQIFP.PART_NUMBER AND SAQIFP.QUOTE_ID = QT__QTQIFP.QUOTE_ID WHERE SAQIFP.QUOTE_ID = '{quote}'""".format(quote=QUOTE)
					Sql.RunQuery(update_quote)
				except:
					Log.Info("EXCEPT ERROR QUOTE TABLE UPDATE")
				#UPDATE SAQITM
				'''
			'''	
			try:
				total = 0.00
				onsite = 0.00
				ext_itm = 0.00
				tax = 0.00
				GetQuoteType = SqlHelper.GetFirst("SELECT QUOTE_TYPE FROM SAQTMT WHERE QUOTE_ID = '{}'".format(QUOTE))
				if  "TOOL" in str(GetQuoteType.QUOTE_TYPE):
					
					GetSum = SqlHelper.GetFirst( "SELECT SUM(EXTENDED_PRICE) AS PRICE FROM SAQIFP WHERE QUOTE_ID = '{}' AND SERVICE_ID = 'Z0091'".format(QUOTE))
					
					GetTax = SqlHelper.GetFirst("SELECT SUM(TAX) AS TAX FROM SAQIFP WHERE QUOTE_ID = '{}' AND SERVICE_ID = 'Z0091'".format(QUOTE))
					
					# Sql.RunQuery("UPDATE SAQITM SET EXTENDED_PRICE = {}, TOTAL_COST = {}, TAX = {}, PRICING_STATUS = 'ACQUIRED' WHERE SAQITM.QUOTE_ID = '{}' AND SAQITM.SERVICE_ID LIKE '%Z0091%'".format(GetSum.PRICE,GetSum.PRICE,GetTax.TAX,QUOTE))
				Obj_Qty_query = SqlHelper.GetFirst("select count(*) as cnt from SAQIFP(NOLOCK) WHERE  QUOTE_ID = '"+str(QUOTE)+"' ")

				#Log.Info('03-03-2021---QT_SAQITM---')
				update_quote_price = "UPDATE QT__QTQITM SET FORECAST_VALUE = {total}, EXTENDED_UNIT_PRICE = {ext},TAX = {tax} WHERE QT__QTQITM.QUOTE_ID ='{quote}'".format(
					total=total,
					ext=ext_itm,
					quote=QUOTE,
					tax = tax
						)
				Sql.RunQuery(update_quote_price) 
				Status_query = SqlHelper.GetFirst("select count(*) as cnt from SAQIFP(NOLOCK) WHERE PRICING_STATUS = 'ACQUIRING...'  AND QUOTE_ID = '"+str(QUOTE)+"' ")

				if str(Status_query.cnt) == '0':

					#Log.Info("456789 if QUOTE --->"+str(QUOTE))

					Parameter1 = SqlHelper.GetFirst("SELECT QUERY_CRITERIA_1 FROM SYDBQS (NOLOCK) WHERE QUERY_NAME = 'UPD' ")
					# primaryQueryItems = SqlHelper.GetFirst(""+ str(Parameter1.QUERY_CRITERIA_1)+ "  A set PRICING_STATUS = ''ACQUIRED'' FROM SAQITM a where a.QUOTE_ID = ''"+str(QUOTE)+"'' ' ")


				ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "200", "Message": "Part Pricing data succussfully updated."}]})
			except: 
				Log.Info("QTPOSTPTPR ERROR---->:" + str(sys.exc_info()[1]))
				Log.Info("QTPOSTPTPR ERROR LINE NO---->:" + str(sys.exc_info()[-1].tb_lineno))
		'''


except:
	Log.Info("QTPOSTPTPR ERROR---->:" + str(sys.exc_info()[1]))
	Log.Info("QTPOSTPTPR ERROR LINE NO---->:" + str(sys.exc_info()[-1].tb_lineno))
	ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "400", "Message": str(sys.exc_info()[1])}]})
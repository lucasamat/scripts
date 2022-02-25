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
import re
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
			#Log.Info("Param.CPQ_Column----"+str(Param.CPQ_Column))
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
					
			
			batch_group_record_id = str(Guid.NewGuid()).upper()
			contract_quote_record_id = None				

			for ele in price:
				Log.Info("456 type(price) --->"+str(ele))
			if str(type(price)) == "<type 'Dictionary[str, object]'>":
				#Log.Info("type condition--->")
				price = [price]
			#Log.Info("456789 type(price) --->"+str(type(price)))
			try:
				get_billing_type_val = ''
				if price and len(price) > 0:	
					Itemidinfo = str(price[0]["itemId"]).split(";")
					QUOTE = str(Itemidinfo[1])
					Log.Info("QUOTE-billing-"+str(QUOTE))
					get_revision = Sql.GetFirst("SELECT * FROM SAQTMT WHERE QUOTE_ID = '{}'".format(QUOTE))
					
					get_billing_type = Sql.GetFirst("select ENTITLEMENT_XML,SERVICE_ID from SAQTSE where QUOTE_ID = '{QuoteId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' and SERVICE_ID = 'Z0100'".format(QuoteId =QUOTE ,RevisionRecordId=get_revision.QTEREV_RECORD_ID))
					if get_billing_type:
						updateentXML = get_billing_type.ENTITLEMENT_XML
						pattern_tag = re.compile(r'(<QUOTE_ITEM_ENTITLEMENT>[\w\W]*?</QUOTE_ITEM_ENTITLEMENT>)')
						pattern_id = re.compile(r'<ENTITLEMENT_ID>AGS_Z0100_PQB_BILTYP</ENTITLEMENT_ID>')
						
						pattern_name = re.compile(r'<ENTITLEMENT_DISPLAY_VALUE>([^>]*?)</ENTITLEMENT_DISPLAY_VALUE>')
						for m in re.finditer(pattern_tag, updateentXML):
							sub_string = m.group(1)
							get_ent_id = re.findall(pattern_id,sub_string)
							get_ent_val= re.findall(pattern_name,sub_string)
							if get_ent_id:
								get_billing_type_val = str(get_ent_val[0])
								break
			except:
				get_billing_type_val = ''
			Log.Info("get_billing_type-"+str(get_billing_type_val))
			for i in price:	
				insert_data = []	
				Itemidinfo = str(i["itemId"]).split(";")
				Log.Info("456 Itemidinfo --->"+str(i))
				QUOTE = str(Itemidinfo[1])
				currencyType = str(Itemidinfo[3])
				contract_quote_record_id = None		
				Taxrate = ''
				Taxvalue = ''		
				GetPricingProcedure = Sql.GetFirst("SELECT EXCHANGE_RATE_TYPE,DIVISION_ID, DISTRIBUTIONCHANNEL_ID, SALESORG_ID, GLOBAL_CURRENCY, PRICINGPROCEDURE_ID, QUOTE_RECORD_ID,QTEREV_RECORD_ID,EXCHANGE_RATE FROM SAQTRV (NOLOCK) WHERE QUOTE_ID = '{}'".format(QUOTE))
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
					revision_rec_id = GetPricingProcedure.QTEREV_RECORD_ID
					exch_rate = GetPricingProcedure.EXCHANGE_RATE
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
				core_credit_amount = ''
				cust_participate = Sql.GetFirst("SELECT CUSTOMER_PARTICIPATE,ODCC_FLAG FROM SAQSPT WHERE QUOTE_RECORD_ID = '"+str(contract_quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(revision_rec_id)+"' AND PART_NUMBER = '"+str(Itemidinfo[0])+"' ")
				if cust_participate and str(cust_participate.CUSTOMER_PARTICIPATE).upper() == "TRUE" and str(cust_participate.ODCC_FLAG).upper() == "TRUE":
					conditions = response1['Entries'][0]['items'][0]['conditions']
					for condition in conditions:
						if condition['conditionType'] == "ZERU":
							core_credit_amount = condition['conditionValue']
							break
				Log.Info("core_credit_amount--->"+str(core_credit_amount))
				#insert_data.append((str(Guid.NewGuid()).upper(), Itemidinfo[0], Itemidinfo[-2], i["netPrice"], 'IN PROGRESS', QUOTE, contract_quote_record_id, batch_group_record_id,str(Taxrate),str(core_credit_amount),i["taxValue"]))
				insert_data.append((str(Guid.NewGuid()).upper(), Itemidinfo[0], Itemidinfo[-2], i["netPrice"], 'IN PROGRESS', QUOTE, contract_quote_record_id, batch_group_record_id,str(Taxrate),str(core_credit_amount),i["taxValue"],i["grossValue"]))
				
				Log.Info("UNIT_PRICE---22---"+str(insert_data))
				#Log.Info("4521 batch_group_record_id --->"+str(batch_group_record_id))
				#Log.Info("4521 contract_quote_record_id --->"+str(contract_quote_record_id))
				getpartsdata =''
				get_ancillary_spare = ''
				getpartsdata = Sql.GetFirst("select * from SAQIFP where QUOTE_RECORD_ID = '"+str(contract_quote_record_id)+"'")
				if not getpartsdata:
					get_ancillary_spare = Sql.GetFirst("SELECT * FROM SAQRIP WHERE QUOTE_RECORD_ID = '"+str(contract_quote_record_id)+"'")
				if not getpartsdata and  not get_ancillary_spare:
					getpartsdata = Sql.GetFirst("select * from SAQSPT where QUOTE_RECORD_ID = '"+str(contract_quote_record_id)+"'")
					
				if getpartsdata or get_ancillary_spare:
					Sql.RunQuery("INSERT INTO SYSPBT (BATCH_RECORD_ID, SAP_PART_NUMBER, QUANTITY, UNIT_PRICE, BATCH_STATUS, QUOTE_ID, QUOTE_RECORD_ID, BATCH_GROUP_RECORD_ID,TAXRATE,CORE_CREDIT_PRICE,TAX_VALUE,TAX) VALUES {}".format(', '.join(map(str, insert_data))))			
					#Log.Info('getpartsdata -->'+str(getpartsdata.PART_NUMBER))
				
					if getpartsdata:
						if currencyType == 'docCurrency':
							# Log.Info("UPDATE SAQSPT SET UNIT_PRICE = SYSPBT.UNIT_PRICE ,CORE_CREDIT_PRICE = CASE WHEN SYSPBT.CORE_CREDIT_PRICE = '' THEN NULL ELSE SYSPBT.CORE_CREDIT_PRICE END,EXTENDED_UNIT_PRICE = SYSPBT.UNIT_PRICE * SYSPBT.QUANTITY FROM SAQSPT JOIN SYSPBT (NOLOCK) ON SYSPBT.SAP_PART_NUMBER = SAQSPT.PART_NUMBER AND SYSPBT.QUOTE_RECORD_ID = SAQSPT.QUOTE_RECORD_ID WHERE SAQSPT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}'	""".format(BatchGroupRecordId=batch_group_record_id, QuoteRecordId=contract_quote_record_id))
							# Sql.RunQuery("""UPDATE SAQSPT SET UNIT_PRICE = SYSPBT.UNIT_PRICE ,CORE_CREDIT_PRICE = CASE WHEN SYSPBT.CORE_CREDIT_PRICE = '' THEN NULL ELSE SYSPBT.CORE_CREDIT_PRICE END,EXTENDED_UNIT_PRICE = SYSPBT.UNIT_PRICE * SYSPBT.QUANTITY FROM SAQSPT 				
							# 		JOIN SYSPBT (NOLOCK) ON SYSPBT.SAP_PART_NUMBER = SAQSPT.PART_NUMBER AND SYSPBT.QUOTE_RECORD_ID = SAQSPT.QUOTE_RECORD_ID
							# 		WHERE SAQSPT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}'
							# 	""".format(BatchGroupRecordId=batch_group_record_id, QuoteRecordId=contract_quote_record_id))
							'''
								Sql.RunQuery("""UPDATE SAQIFP
									SET PRICING_STATUS = CASE WHEN SYSPBT.UNIT_PRICE IS NULL THEN 'ERROR' WHEN SYSPBT.UNIT_PRICE = '0.00000' THEN 'ERROR' ELSE 'ACQUIRED' END,TAX = (SYSPBT.UNIT_PRICE * SYSPBT.QUANTITY)- ((SYSPBT.UNIT_PRICE * SYSPBT.QUANTITY)/(1 +(convert(decimal(13,5),SYSPBT.TAXRATE)/100))),EXTENDED_PRICE = SYSPBT.UNIT_PRICE * SYSPBT.QUANTITY,UNIT_PRICE = SYSPBT.UNIT_PRICE
									FROM SAQIFP 				
									JOIN SYSPBT (NOLOCK) ON SYSPBT.SAP_PART_NUMBER = SAQIFP.PART_NUMBER AND SYSPBT.QUOTE_RECORD_ID = SAQIFP.QUOTE_RECORD_ID
									WHERE SAQIFP.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}'
								""".format(BatchGroupRecordId=batch_group_record_id, QuoteRecordId=contract_quote_record_id))
							'''
							Sql.RunQuery("""UPDATE SAQIFP
									SET PRICING_STATUS = CASE WHEN SYSPBT.UNIT_PRICE IS NULL THEN 'ERROR' WHEN SYSPBT.UNIT_PRICE = '0.00000' THEN 'ERROR' ELSE 'ACQUIRED' END,TAX = SYSPBT.TAX_VALUE,EXTENDED_PRICE = SYSPBT.TAX,UNIT_PRICE = SYSPBT.UNIT_PRICE
									FROM SAQIFP 				
									JOIN SYSPBT (NOLOCK) ON SYSPBT.SAP_PART_NUMBER = SAQIFP.PART_NUMBER AND SYSPBT.QUOTE_RECORD_ID = SAQIFP.QUOTE_RECORD_ID
									WHERE SAQIFP.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}'
								""".format(BatchGroupRecordId=batch_group_record_id, QuoteRecordId=contract_quote_record_id))
							#TAX_PERCENTAGE = convert(decimal(13,5),CASE WHEN ISNULL(SYSPBT.TAXRATE,'')='' THEN NULL ELSE SYSPBT.TAXRATE END) ,						
							#UNIT_PRICE = (SYSPBT.UNIT_PRICE * SYSPBT.QUANTITY)/(1 +(convert(decimal(13,5),SYSPBT.TAXRATE)/100)
							#GetSum = SqlHelper.GetFirst( "SELECT SUM(UNIT_PRICE_INGL_CURR) AS TOTAL FROM SAQIFP WHERE QUOTE_ID = '{}' ".format(QUOTE))
							#Log.Info("QTPOSTPTPR TOTAL ==> "+str(GetSum.TOTAL))					
							#Sql.RunQuery("""UPDATE SAQRIT SET STATUS='ACQUIRED', UNIT_PRICE_INGL_CURR = SAQIFP.UNIT_PRICE, NET_PRICE_INGL_CURR={total} FROM SAQRIT
							#JOIN SAQIFP (NOLOCK) ON SAQIFP.PART_NUMBER = SAQRIT.OBJECT_ID AND SAQIFP.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID WHERE SAQRIT.QUOTE_RECORD_ID = '{QuoteRecordId}' SAQRIT.OBJECT_ID='{PartNo}'""".format(total=GetSum.TOTAL, QuoteRecordId=contract_quote_record_id,PartNo=getpartsdata.PART_NUMBER))
							##net price update
							GetEquipment_count = Sql.GetFirst("SELECT COUNT(CpqTableEntryId) AS CNT FROM SAQRIT WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{rev}' AND SERVICE_ID = '{SERVICE_ID}'".format(QuoteRecordId = contract_quote_record_id,rev =revision_rec_id,SERVICE_ID=getpartsdata.SERVICE_ID))
							if GetEquipment_count:
								GetSum = Sql.GetFirst( "SELECT SUM(UNIT_PRICE)/"+str(GetEquipment_count.CNT)+" AS TOTAL_UNIT, SUM(EXTENDED_UNIT_PRICE)/"+str(GetEquipment_count.CNT)+"  AS TOTAL_EXT , SUM(TAX_AMOUNT_INGL_CURR)/"+str(GetEquipment_count.CNT)+"  AS TOTAL_TAX FROM SAQSPT WHERE QUOTE_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID = '{}' AND (CUSTOMER_ANNUAL_QUANTITY IS NOT NULL AND CUSTOMER_ANNUAL_QUANTITY > 0) ".format( QUOTE,revision_rec_id, getpartsdata.SERVICE_ID))
								#Log.Info("QTPOSTPTPR TOTAL111 ==> "+str(GetSum.TOTAL_UNIT))
								Sql.RunQuery("""UPDATE SAQRIT SET STATUS='ACQUIRED', UNIT_PRICE = {total_unit}, NET_PRICE ={total_net} , YEAR_1 ={total_net} FROM SAQRIT
									WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID='{rev}' AND SERVICE_ID = '{SERVICE_ID}'""".format(total_unit=GetSum.TOTAL_UNIT,total_net = GetSum.TOTAL_EXT, QuoteRecordId=contract_quote_record_id,rev =revision_rec_id,SERVICE_ID=getpartsdata.SERVICE_ID))
								Sql.RunQuery("""UPDATE SAQTRV SET SALES_PRICE_INGL_CURR = {total_unit}, TOTAL_AMOUNT_INGL_CURR ={total_net}, TAX_AMOUNT_INGL_CURR ={total_tax} FROM SAQTRV
									WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID='{rev}' AND SERVICE_ID IN('Z0108','Z0110')""".format(total_unit=GetSum.TOTAL_UNIT,total_net = GetSum.TOTAL_EXT,total_tax = GetSum.TOTAL_TAX,  QuoteRecordId=contract_quote_record_id,rev =revision_rec_id))
								Sql.RunQuery("""UPDATE SAQRIT 
												SET NET_VALUE = NET_PRICE + ISNULL(TAX_AMOUNT, 0) 
												FROM SAQRIT (NOLOCK)
													WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID='{rev}' AND SERVICE_ID = '{service_id}' """.format(QuoteRecordId=contract_quote_record_id ,rev =revision_rec_id, service_id = getpartsdata.SERVICE_ID ))
								
							###calling script for saqris,saqtrv insert
							#CallingCQIFWUDQTM = ScriptExecutor.ExecuteGlobal("CQIFWUDQTM",{"QT_REC_ID":QUOTE})	
							
						else:
							# Log.Info("""UPDATE SAQSPT SET UNIT_PRICE = SYSPBT.UNIT_PRICE ,CORE_CREDIT_PRICE = CASE WHEN SYSPBT.CORE_CREDIT_PRICE = '' THEN NULL ELSE SYSPBT.CORE_CREDIT_PRICE END,EXTENDED_UNIT_PRICE = SYSPBT.UNIT_PRICE * SYSPBT.QUANTITY FROM SAQSPT 				
							# 		JOIN SYSPBT (NOLOCK) ON SYSPBT.SAP_PART_NUMBER = SAQSPT.PART_NUMBER AND SYSPBT.QUOTE_RECORD_ID = SAQSPT.QUOTE_RECORD_ID
							# 		WHERE SAQSPT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}'
							# 	""".format(BatchGroupRecordId=batch_group_record_id, QuoteRecordId=contract_quote_record_id))	
							Sql.RunQuery("""UPDATE SAQSPT SET UNIT_PRICE = SYSPBT.UNIT_PRICE ,CORE_CREDIT_PRICE = CASE WHEN SYSPBT.CORE_CREDIT_PRICE = '' THEN NULL ELSE SYSPBT.CORE_CREDIT_PRICE END,TAX_AMOUNT_INGL_CURR=SYSPBT.TAX_VALUE,EXTENDED_UNIT_PRICE = SYSPBT.TAX FROM SAQSPT 				
									JOIN SYSPBT (NOLOCK) ON SYSPBT.SAP_PART_NUMBER = SAQSPT.PART_NUMBER AND SYSPBT.QUOTE_RECORD_ID = SAQSPT.QUOTE_RECORD_ID
									WHERE SAQSPT.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}' 
								""".format(BatchGroupRecordId=batch_group_record_id, QuoteRecordId=contract_quote_record_id))
							Sql.RunQuery("""UPDATE SAQIFP
								SET PRICING_STATUS = CASE WHEN SYSPBT.UNIT_PRICE IS NULL THEN 'ERROR' WHEN SYSPBT.UNIT_PRICE = '0.00000' THEN 'ERROR' ELSE 'ACQUIRED' END,TAX_AMOUNT_INGL_CURR = SYSPBT.TAX_VALUE,UNIT_PRICE_INGL_CURR = SYSPBT.UNIT_PRICE,EXTPRI_INGL_CURR = SYSPBT.TAX FROM SAQIFP 				
								JOIN SYSPBT (NOLOCK) ON SYSPBT.SAP_PART_NUMBER = SAQIFP.PART_NUMBER AND SYSPBT.QUOTE_RECORD_ID = SAQIFP.QUOTE_RECORD_ID
								WHERE SAQIFP.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}'
							""".format(BatchGroupRecordId=batch_group_record_id, QuoteRecordId=contract_quote_record_id))
						
							'''
								Sql.RunQuery("""UPDATE SAQIFP
									SET PRICING_STATUS = CASE WHEN SYSPBT.UNIT_PRICE IS NULL THEN 'ERROR' WHEN SYSPBT.UNIT_PRICE = '0.00000' THEN 'ERROR' ELSE 'ACQUIRED' END,TAX_AMOUNT_INGL_CURR = (SYSPBT.UNIT_PRICE * SYSPBT.QUANTITY)- ((SYSPBT.UNIT_PRICE * SYSPBT.QUANTITY)/(1 +(convert(decimal(13,5),SYSPBT.TAXRATE)/100))),UNIT_PRICE_INGL_CURR = SYSPBT.UNIT_PRICE,EXTPRI_INGL_CURR = SYSPBT.UNIT_PRICE * SYSPBT.QUANTITY
									FROM SAQIFP 				
									JOIN SYSPBT (NOLOCK) ON SYSPBT.SAP_PART_NUMBER = SAQIFP.PART_NUMBER AND SYSPBT.QUOTE_RECORD_ID = SAQIFP.QUOTE_RECORD_ID
									WHERE SAQIFP.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}'
								""".format(BatchGroupRecordId=batch_group_record_id, QuoteRecordId=contract_quote_record_id))
							'''
							#,UNIT_PRICE_INGL_CURR = (SYSPBT.UNIT_PRICE * SYSPBT.QUANTITY)/(1 +(convert(decimal(13,5),SYSPBT.TAXRATE)/100))
							#GetSum = SqlHelper.GetFirst( "SELECT SUM(UNIT_PRICE_INGL_CURR) AS TOTAL FROM SAQIFP WHERE QUOTE_ID = '{}' ".format(QUOTE))
							#Log.Info("QTPOSTPTPR TOTAL ==> "+str(GetSum.TOTAL))
							#Sql.RunQuery("""UPDATE SAQRIT SET STATUS='ACQUIRED', UNIT_PRICE_INGL_CURR = SAQIFP.UNIT_PRICE, NET_PRICE_INGL_CURR={total} FROM SAQRIT
							#JOIN SAQIFP (NOLOCK) ON SAQIFP.PART_NUMBER = SAQRIT.OBJECT_ID AND SAQIFP.QUOTE_RECORD_ID = SAQRIT.QUOTE_RECORD_ID WHERE SAQRIT.QUOTE_RECORD_ID = '{QuoteRecordId}' SAQRIT.OBJECT_ID='{PartNo}'""".format(total=GetSum.TOTAL, QuoteRecordId=contract_quote_record_id,PartNo=getpartsdata.PART_NUMBER))
							##net price update
							GetEquipment_count = Sql.GetFirst("SELECT COUNT(CpqTableEntryId) AS CNT FROM SAQRIT WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{rev}' AND SERVICE_ID = '{SERVICE_ID}'".format(QuoteRecordId = contract_quote_record_id,rev =revision_rec_id,SERVICE_ID=getpartsdata.SERVICE_ID))
							if GetEquipment_count:
								GetSum = Sql.GetFirst( "SELECT SUM(UNIT_PRICE)/"+str(GetEquipment_count.CNT)+" AS TOTAL_UNIT, SUM(EXTENDED_UNIT_PRICE)/"+str(GetEquipment_count.CNT)+"  AS TOTAL_EXT FROM SAQSPT WHERE  QUOTE_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID = '{}' AND (CUSTOMER_ANNUAL_QUANTITY IS NOT NULL AND CUSTOMER_ANNUAL_QUANTITY > 0)".format( QUOTE,revision_rec_id, getpartsdata.SERVICE_ID))
								#Log.Info("QTPOSTPTPR TOTAL111 ==> "+str(GetSum.TOTAL_UNIT))
								Sql.RunQuery("""UPDATE SAQRIT SET STATUS='ACQUIRED', UNIT_PRICE_INGL_CURR = {total_unit}, NET_PRICE_INGL_CURR ={total_net}, YEAR_1_INGL_CURR={total_net}  FROM SAQRIT
									WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID='{rev}' AND SERVICE_ID = '{SERVICE_ID}'""".format(total_unit=GetSum.TOTAL_UNIT,total_net = GetSum.TOTAL_EXT, QuoteRecordId=contract_quote_record_id,rev =revision_rec_id,SERVICE_ID=getpartsdata.SERVICE_ID))
								Sql.RunQuery("""UPDATE SAQTRV SET SALES_PRICE_INGL_CURR = {total_unit}, TOTAL_AMOUNT_INGL_CURR ={total_net} FROM SAQTRV
									WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID='{rev}' AND SERVICE_ID IN('Z0108','Z0110')""".format(total_unit=GetSum.TOTAL_UNIT,total_net = GetSum.TOTAL_EXT, QuoteRecordId=contract_quote_record_id,rev =revision_rec_id))
								Sql.RunQuery("""UPDATE SAQRIT 
												SET NET_VALUE_INGL_CURR = NET_PRICE_INGL_CURR + ISNULL(TAX_AMOUNT, 0) 
												FROM SAQRIT (NOLOCK)
													WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID='{rev}' AND SERVICE_ID = '{service_id}' """.format(QuoteRecordId=contract_quote_record_id ,rev =revision_rec_id, service_id = getpartsdata.SERVICE_ID ))
								
							###calling script for saqris,saqtrv insert
							#CallingCQIFWUDQTM = ScriptExecutor.ExecuteGlobal("CQIFWUDQTM",{"QT_REC_ID":QUOTE})	
							
					elif get_ancillary_spare:
						#Log.Info("currencyType---"+str(currencyType))	
						if currencyType == 'docCurrency':
							Sql.RunQuery("""UPDATE SAQRSP SET UNIT_PRICE = SYSPBT.UNIT_PRICE ,EXTENDED_PRICE = SYSPBT.UNIT_PRICE * SYSPBT.QUANTITY FROM SAQRSP 				
									JOIN SYSPBT (NOLOCK) ON SYSPBT.SAP_PART_NUMBER = SAQRSP.PART_NUMBER AND SYSPBT.QUOTE_RECORD_ID = SAQRSP.QUOTE_RECORD_ID
									WHERE SAQRSP.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRSP.SERVICE_ID = 'Z0100' AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}'
								""".format(BatchGroupRecordId=batch_group_record_id, QuoteRecordId=contract_quote_record_id))
			
							##net price update
							GetEquipment_count = Sql.GetFirst("SELECT COUNT(CpqTableEntryId) AS CNT FROM SAQRIT WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{rev}' AND SERVICE_ID = 'Z0100'".format(QuoteRecordId = contract_quote_record_id,rev =revision_rec_id))
							if GetEquipment_count:
								GetSum = Sql.GetFirst( "SELECT SUM(UNIT_PRICE)/"+str(GetEquipment_count.CNT)+" AS TOTAL_UNIT, SUM(EXTENDED_PRICE)/"+str(GetEquipment_count.CNT)+"  AS TOTAL_EXT FROM SAQRSP WHERE QUOTE_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID = 'Z0100'".format( QUOTE,revision_rec_id))
								#Log.Info("QTPOSTPTPR TOTAL111 ==> "+str(GetSum.TOTAL_UNIT))
								if get_billing_type_val.upper() == 'VARIABLE':
									pricing_field_annualized = "TENVDC"
								else:
									pricing_field_annualized = "TNTVDC"
								#Log.Info("pricing_field-doc-"+str(QUOTE)+'-'+str(pricing_field))
								if GetSum:
									if GetSum.TOTAL_UNIT and GetSum.TOTAL_EXT:
										#Log.Info( str(GetSum.TOTAL_UNIT)+'-'+str(GetSum.TOTAL_EXT))
										Sql.RunQuery("""UPDATE SAQRIT SET UNIT_PRICE = {total_unit}  FROM SAQRIT
										WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID='{rev}' AND SERVICE_ID = 'Z0100'""".format(total_unit=GetSum.TOTAL_UNIT, QuoteRecordId=contract_quote_record_id,rev =revision_rec_id))
										
										##saqico insert 
										Sql.RunQuery("""UPDATE SAQICO SET {pricing_field} ={total_net}  FROM SAQICO (NOLOCK)
										WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID='{rev}' AND SERVICE_ID = 'Z0100'""".format(total_net = GetSum.TOTAL_EXT, QuoteRecordId=contract_quote_record_id,rev =revision_rec_id, pricing_field = pricing_field_annualized))
								# Sql.RunQuery("""UPDATE SAQRIT 
								# 				SET 
								# 				YEAR_1_INGL_CURR = YEAR_1 + ISNULL(EXCHANGE_RATE, 0),
								# 				YEAR_2_INGL_CURR = YEAR_2 + ISNULL(EXCHANGE_RATE, 0),
								# 				YEAR_3_INGL_CURR = YEAR_3 + ISNULL(EXCHANGE_RATE, 0),
								# 				YEAR_4_INGL_CURR = YEAR_4 + ISNULL(EXCHANGE_RATE, 0),
								# 				YEAR_5_INGL_CURR = YEAR_5 + ISNULL(EXCHANGE_RATE, 0)
								# 				FROM SAQRIT (NOLOCK)
								# 					WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID='{rev}' AND SERVICE_ID = 'Z0100' """.format(QuoteRecordId=contract_quote_record_id ,rev =revision_rec_id ))
								#Log.Info("exch_rate----"+str(exch_rate)+'--'+str(QUOTE))
								# Sql.RunQuery("""UPDATE SAQRIT 
								# 		SET NET_PRICE_INGL_CURR = NET_PRICE*"""+str(exch_rate)+""" , 
								# 		NET_VALUE_INGL_CURR = NET_VALUE*"""+str(exch_rate)+""",
								# 		UNIT_PRICE_INGL_CURR =  UNIT_PRICE*"""+str(exch_rate)+"""
								# 		FROM SAQRIT (NOLOCK)
								# 			WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID='{rev}' AND SERVICE_ID = '{service_id}'""".format(QuoteRecordId=contract_quote_record_id ,rev =revision_rec_id ))
								
			
			
						else:
							Sql.RunQuery("""UPDATE SAQRSP SET UNIT_PRICE_INGL_CURR = SYSPBT.UNIT_PRICE ,EXTENDED_PRICE_INGL_CURR = SYSPBT.UNIT_PRICE * SYSPBT.QUANTITY FROM SAQRSP 				
									JOIN SYSPBT (NOLOCK) ON SYSPBT.SAP_PART_NUMBER = SAQRSP.PART_NUMBER AND SYSPBT.QUOTE_RECORD_ID = SAQRSP.QUOTE_RECORD_ID
									WHERE SAQRSP.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQRSP.SERVICE_ID = 'Z0100' AND SYSPBT.BATCH_GROUP_RECORD_ID = '{BatchGroupRecordId}'
								""".format(BatchGroupRecordId=batch_group_record_id, QuoteRecordId=contract_quote_record_id))
			
							##net price update
							GetEquipment_count = Sql.GetFirst("SELECT COUNT(CpqTableEntryId) AS CNT FROM SAQRIT WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{rev}' AND SERVICE_ID = 'Z0100'".format(QuoteRecordId = contract_quote_record_id,rev =revision_rec_id))
							if GetEquipment_count:
								GetSum = Sql.GetFirst( "SELECT SUM(UNIT_PRICE_INGL_CURR)/"+str(GetEquipment_count.CNT)+" AS TOTAL_UNIT, SUM(EXTENDED_PRICE_INGL_CURR)/"+str(GetEquipment_count.CNT)+"  AS TOTAL_EXT FROM SAQRSP WHERE QUOTE_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID = 'Z0100'".format( QUOTE,revision_rec_id))
								#Log.Info("QTPOSTPTPR TOTAL111222 ==> "+str(GetSum.TOTAL_UNIT))
								if get_billing_type_val.upper() == 'VARIABLE':
									pricing_field_annualized = "TENVGC"
								else:
									pricing_field_annualized = "TNTVGC"
								#Log.Info("pricing_field--"+str(QUOTE)+'-'+str(pricing_field))
								if GetSum:
									if GetSum.TOTAL_UNIT and GetSum.TOTAL_EXT:
										# Sql.RunQuery("""UPDATE SAQRIT SET STATUS='ACQUIRED', UNIT_PRICE_INGL_CURR = {total_unit}, {pricing_field} ={total_net}  FROM SAQRIT
										# 	WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID='{rev}' AND SERVICE_ID = 'Z0100'""".format(total_unit=GetSum.TOTAL_UNIT, QuoteRecordId=contract_quote_record_id,rev =revision_rec_id, pricing_field= pricing_field))
										# Sql.RunQuery("""UPDATE SAQRIT 
										# 		SET NET_VALUE_INGL_CURR = NET_PRICE_INGL_CURR + ISNULL(TAX_AMOUNT, 0) 
										# 		FROM SAQRIT (NOLOCK)
										# 			WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID='{rev}' AND SERVICE_ID = 'Z0100' """.format(QuoteRecordId=contract_quote_record_id ,rev =revision_rec_id ))

										Sql.RunQuery("""UPDATE SAQRIT SET UNIT_PRICE_INGL_CURR = {total_unit}  FROM SAQRIT
										WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID='{rev}' AND SERVICE_ID = 'Z0100'""".format(total_unit=GetSum.TOTAL_UNIT, QuoteRecordId=contract_quote_record_id,rev =revision_rec_id))
										
										##saqico insert 
										Sql.RunQuery("""UPDATE SAQICO SET {pricing_field} ={total_net}  FROM SAQICO (NOLOCK)
										WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID='{rev}' AND SERVICE_ID = 'Z0100'""".format(total_net = GetSum.TOTAL_EXT, QuoteRecordId=contract_quote_record_id,rev =revision_rec_id, pricing_field = pricing_field_annualized))

						
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
			###calling script for saqris,saqtrv insert
			CallingCQIFWUDQTM = ScriptExecutor.ExecuteGlobal("CQIFWUDQTM",{"QT_REC_ID":QUOTE})
			
except:
	Log.Info("QTPOSTPTPR ERROR---->:" + str(sys.exc_info()[1]))
	Log.Info("QTPOSTPTPR ERROR LINE NO---->:" + str(sys.exc_info()[-1].tb_lineno))
	ApiResponse = ApiResponseFactory.JsonResponse({"Response": [{"Status": "400", "Message": str(sys.exc_info()[1])}]})
# =========================================================================================================================================
#   __script_name : CQSYNCQTBL.PY
#   __script_description : THIS SCRIPT IS USED TO SYNC THE QUOTE TABLES AND CONTRACT QUOTE CUSTOM TABLES WHEN WE CREATE A QUOTE FROM C4C
#   __primary_author__ : AYYAPPAN SUBRAMANIYAN
#   __create_date :01-10-2020
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct
import datetime
import time
from SYDATABASE import SQL
import clr
import sys
import System.Net
from System.Text.Encoding import UTF8
from System import Convert
import re
from datetime import timedelta , date

Sql = SQL()
ScriptExecutor = ScriptExecutor
#Log.Info("==========================>00000000")


class SyncQuoteAndCustomTables:
	def __init__(self, Quote):
		#Log.Info("==========================>111111111111")
		self.quote = Quote
		#Log.Info("++++++++ QUote " + str(Quote.GetCustomField("STPAccountID").Content))
		# self.user_id = ScriptExecutor.ExecuteGlobal("SYUSDETAIL", "USERID")
		# self.datetime_value = datetime.datetime.now()

	def _get_custom_fields_detail(self):		
		return {
			'STPAccountID':self.quote.GetCustomField('STPAccountID').Content,
			'STPAccountName':self.quote.GetCustomField('STPAccountName').Content,
			'STPAccountType':self.quote.GetCustomField('STPAccountType').Content,
			'Region':self.quote.GetCustomField('Region').Content,
			'SalesType':self.quote.GetCustomField('SalesType').Content,
			'OpportunityId':self.quote.GetCustomField('OpportunityId').Content,
			'OpportunityType':self.quote.GetCustomField('OpportunityType').Content,
			'QuoteLevel':self.quote.GetCustomField('QuoteLevel').Content,
			'OpportunityOwner':self.quote.GetCustomField('OpportunityOwner').Content,
			'OpportunityStage':self.quote.GetCustomField('OpportunityStage').Content,
			'SalesOrgID':self.quote.GetCustomField('SalesOrgID').Content,
			'SalesOrgName':self.quote.GetCustomField('SalesOrgName').Content,
			'SalesUnit':self.quote.GetCustomField('SalesUnit').Content,
			'DistributionChannel':self.quote.GetCustomField('DistributionChannel').Content,
			'Division':self.quote.GetCustomField('Division').Content,
			'PrimaryContactName' : self.quote.GetCustomField('PrimaryContactName').Content,
			'SalesOfficeID':self.quote.GetCustomField('SalesOfficeID').Content,            
			'SalesPerson':self.quote.GetCustomField('SalesPerson').Content,
			'PaymentTerms':self.quote.GetCustomField('PaymentTerms').Content,
			'CustomerPO':self.quote.GetCustomField('CustomerPO').Content,
			'FabLocationID':self.quote.GetCustomField('FabLocationID').Content,
			'FabLocationName':self.quote.GetCustomField('FabLocationName').Content,
			'FabLocation':self.quote.GetCustomField('FabLocation').Content,
			'QuoteExpirationDate':datetime.datetime.strptime(self.quote.GetCustomField('QuoteExpirationDate').Content, '%Y-%m-%d').date(),
			'PricingDate':datetime.datetime.strptime(self.quote.GetCustomField('PricingDate').Content, '%Y-%m-%d').date(),
			'ContractType':self.quote.GetCustomField('ContractType').Content,
			'Currency':self.quote.GetCustomField('Currency').Content,
			'Incoterms':self.quote.GetCustomField('Incoterms').Content,
			'ExchangeRateType':self.quote.GetCustomField('ExchangeRateType').Content,
			'PayerName':self.quote.GetCustomField('PayerName').Content,
			'PayerAddress1':self.quote.GetCustomField('PayerAddress1').Content,
			'PayerCity':self.quote.GetCustomField('PayerCity').Content,
			'PayerState':self.quote.GetCustomField('PayerState').Content,
			'PayerCountry':self.quote.GetCustomField('PayerCountry').Content,
			'PayerPostalCode':self.quote.GetCustomField('PayerPostalCode').Content,
			'PayerEmail':self.quote.GetCustomField('PayerEmail').Content,
			'PayerPhone':self.quote.GetCustomField('PayerPhone').Content,
			'SellerName':self.quote.GetCustomField('SellerName').Content,
			'SellerAddress':self.quote.GetCustomField('SellerAddress').Content,
			'SellerEmail':self.quote.GetCustomField('SellerEmail').Content,
			'SellerPhone':self.quote.GetCustomField('SellerPhone').Content,
			'SalesUnitName':self.quote.GetCustomField('SalesUnitName').Content,
			'SalesUnitAddress':self.quote.GetCustomField('SalesUnitAddress').Content,
			'SalesUnitEmail':self.quote.GetCustomField('SalesUnitEmail').Content,
			'SalesUnitPhone':self.quote.GetCustomField('SalesUnitPhone').Content,
			'SalesEmployeeName':self.quote.GetCustomField('SalesEmployeeName').Content,
			'SalesEmployeePhone':self.quote.GetCustomField('SalesEmployeePhone').Content,
			'EmployeeResponsibleName':self.quote.GetCustomField('EmployeeResponsibleName').Content,
			'EmployeeResponsibleAddress':self.quote.GetCustomField('EmployeeResponsibleAddress').Content,
			'EmployeeResponsibleEmail':self.quote.GetCustomField('EmployeeResponsibleEmail').Content,
			'EmployeeResponsiblePhone':self.quote.GetCustomField('EmployeeResponsiblePhone').Content,
			'SalesPersonPhone':self.quote.GetCustomField('SalesPersonPhone').Content,
			'ContractManagerName':self.quote.GetCustomField('ContractManagerName').Content,
			'ContractManagerPhone':self.quote.GetCustomField('ContractManagerPhone').Content,
			'ContractManagerEmail':self.quote.GetCustomField('ContractManagerEmail').Content,
			'ContractManagerAddress':self.quote.GetCustomField('ContractManagerAddress').Content,
			'PaymentTermName':self.quote.GetCustomField('PaymentTermName').Content,
			'ContractManagerID':self.quote.GetCustomField('ContractManagerID').Content,
			'PayerID':self.quote.GetCustomField('PayerID').Content,
			'SellerID':self.quote.GetCustomField('SellerID').Content,
			'SalesUnitID':self.quote.GetCustomField('SalesUnitID').Content,
			'SalesEmployeeID':self.quote.GetCustomField('SalesEmployeeID').Content,
			'EmployeeResponsibleID':self.quote.GetCustomField('EmployeeResponsibleID').Content,
			'SalesEmployeeEmail':self.quote.GetCustomField('SalesEmployeeEmail').Content,
			'SalesEmployeeAddress':self.quote.GetCustomField('SalesEmployeeAddress').Content,
			'IncotermsLocation':self.quote.GetCustomField('IncotermsLocation').Content,
			'SourceContractID':self.quote.GetCustomField('SourceContractID').Content,
			'QuoteStartDate':datetime.datetime.strptime(self.quote.GetCustomField('QuoteStartDate').Content, '%Y-%m-%d').date(),
			'SourceAccountID':self.quote.GetCustomField('SourceAccountID').Content,
			'SourceAccountAddress':self.quote.GetCustomField('SourceAccountAddress').Content,
			'SourceAccountEmail':self.quote.GetCustomField('SourceAccountEmail').Content,
			'SourceAccountName':self.quote.GetCustomField('SourceAccountName').Content,
			'SourceAccountPhone':self.quote.GetCustomField('SourceAccountPhone').Content,
			
		}

	@staticmethod
	def get_formatted_date(year, month, day, date_format="", separator=""):
		stryear = str(year)
		strmonth = str(month)
		strday = str(day)

		if month < 10:
			strmonth = "0" + str(month)

		if day < 10:
			strday = "0" + str(day)
		date_str = date_format.format(Date=strday, Month=strmonth, Year=stryear, Separator=separator)
		return date_str
	def CreateEntitlements(self,quote_record_id):
		SAQTSVObj=Sql.GetList("Select * from SAQTSV (nolock) where QUOTE_RECORD_ID= '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}'".format(QuoteRecordId=quote_record_id,quote_revision_record_id=Quote.GetGlobal("quote_revision_record_id")))
		#Log.Info("quote_record_id---123------"+str(quote_record_id))
		tableInfo = SqlHelper.GetTable("SAQTSE")
		x = datetime.datetime.today()
		x= str(x)
		y = x.split(" ")
		ent_disp_val = ent_val_code = ''
		for OfferingRow_detail in SAQTSVObj:
			#Log.Info("SERVICE_ID--130----"+str(OfferingRow_detail.SERVICE_ID))
			webclient = System.Net.WebClient()
			webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/json"
			webclient.Headers[System.Net.HttpRequestHeader.Authorization] = "Basic c2ItYzQwYThiMWYtYzU5NS00ZWJjLTkyYzYtYzM4ODg4ODFmMTY0IWIyNTAzfGNwc2VydmljZXMtc2VjdXJlZCFiMzkxOm9zRzgvSC9hOGtkcHVHNzl1L2JVYTJ0V0FiMD0=";
			response = webclient.DownloadString("https://cpqprojdevamat.authentication.us10.hana.ondemand.com:443/oauth/token?grant_type=client_credentials")
			response = eval(response)
			Request_URL="https://cpservices-product-configuration.cfapps.us10.hana.ondemand.com/api/v2/configurations?autoCleanup=False"
			webclient.Headers[System.Net.HttpRequestHeader.Authorization] ="Bearer "+str(response['access_token'])
			requestdata= '{"productKey":"'+OfferingRow_detail.SERVICE_ID+'","date":"'+str(y[0])+'","context":[{"name":"VBAP-MATNR","value":"'+OfferingRow_detail.SERVICE_ID+'"}]}'
			#if TreeSuperParentParam=="Offerings":
				#requestdata= '{"productKey":"'+TreeParam+'","date":"2020-10-14","context":[{"name":"VBAP-MATNR","value":"'+TreeParam+'"}]}'
				#ProductPartnumber=TreeParam
			#elif TreeTopSuperParentParam=="Offerings":
				#requestdata= '{"productKey":"'+TreeParentParam+'","date":"2020-09-01","context":[{"name":"VBAP-MATNR","value":"'+TreeParentParam+'"}]}'
				#ProductPartnumber=TreeParentParam
			response1 = webclient.UploadString(Request_URL,str(requestdata))
			response1=str(response1).replace(": true",": \"true\"").replace(": false",": \"false\"")
			Fullresponse= eval(response1)
			attributesdisallowedlst=[]
			attributeReadonlylst=[]
			attributesallowedlst=[]
			attributedefaultvalue = []
			#overallattributeslist =[]
			attributevalues={}
			for rootattribute, rootvalue in Fullresponse.items():
				if rootattribute=="rootItem":
					for Productattribute, Productvalue in rootvalue.items():
						if Productattribute=="characteristics":
							for prdvalue in Productvalue:
								#overallattributeslist.append(prdvalue['id'])
								if prdvalue['visible'] =='false':
									attributesdisallowedlst.append(prdvalue['id'])
								else:
									#Trace.Write(prdvalue['id']+" set here")
									attributesallowedlst.append(prdvalue['id'])
								if prdvalue['readOnly'] =='true':
									attributeReadonlylst.append(prdvalue['id'])
								for attribute in prdvalue['values']:
									attributevalues[str(prdvalue['id'])]=attribute['value']
									if attribute["author"] in ("Default","System"):
										Trace.Write('524------'+str(prdvalue["id"]))
										attributedefaultvalue.append(prdvalue["id"])
			
			attributesallowedlst = list(set(attributesallowedlst))
			#overallattributeslist = list(set(overallattributeslist))
			Trace.Write('attributesallowedlst---'+str(attributesallowedlst))
			HasDefaultvalue=False
			ProductVersionObj=Sql.GetFirst("Select product_id from product_versions(nolock) where SAPKBId = '"+str(Fullresponse['kbId'])+"' AND SAPKBVersion='"+str(Fullresponse['kbKey']['version'])+"'")
			if ProductVersionObj is not None:
				tbrow={}
				insertservice =ent_disp_valdate =  ""
				tblist = []
				#Log.Info("178----")
				for attrs in attributesallowedlst:
					#tbrow1 = {}
					#Log.Info("191----")
					if attrs in attributevalues:
						HasDefaultvalue=True
						STANDARD_ATTRIBUTE_VALUES=Sql.GetFirst("SELECT S.STANDARD_ATTRIBUTE_DISPLAY_VAL,S.STANDARD_ATTRIBUTE_CODE FROM STANDARD_ATTRIBUTE_VALUES (nolock) S INNER JOIN ATTRIBUTE_DEFN (NOLOCK) A ON A.STANDARD_ATTRIBUTE_CODE=S.STANDARD_ATTRIBUTE_CODE WHERE A.SYSTEM_ID = '{}'".format(attrs,attributevalues[attrs]))
						ent_disp_val = attributevalues[attrs]
						ent_val_code = attributevalues[attrs]
					else:
						HasDefaultvalue=False
						ent_disp_val = ""
						ent_val_code = ""
						STANDARD_ATTRIBUTE_VALUES=Sql.GetFirst("SELECT S.STANDARD_ATTRIBUTE_CODE FROM STANDARD_ATTRIBUTE_VALUES (nolock) S INNER JOIN ATTRIBUTE_DEFN (NOLOCK) A ON A.STANDARD_ATTRIBUTE_CODE=S.STANDARD_ATTRIBUTE_CODE WHERE A.SYSTEM_ID = '{}'".format(attrs))
					ATTRIBUTE_DEFN=Sql.GetFirst("SELECT * FROM ATTRIBUTE_DEFN (NOLOCK) WHERE SYSTEM_ID='{}'".format(attrs))
					PRODUCT_ATTRIBUTES=Sql.GetFirst("SELECT A.ATT_DISPLAY_DESC FROM ATT_DISPLAY_DEFN (NOLOCK) A INNER JOIN PRODUCT_ATTRIBUTES (NOLOCK) P ON A.ATT_DISPLAY=P.ATT_DISPLAY WHERE P.PRODUCT_ID={} AND P.STANDARD_ATTRIBUTE_CODE={}".format(ProductVersionObj.product_id,STANDARD_ATTRIBUTE_VALUES.STANDARD_ATTRIBUTE_CODE))
					if PRODUCT_ATTRIBUTES:
						if PRODUCT_ATTRIBUTES.ATT_DISPLAY_DESC in ('Drop Down','Check Box') and ent_disp_val:
							get_display_val = Sql.GetFirst("SELECT STANDARD_ATTRIBUTE_DISPLAY_VAL  from STANDARD_ATTRIBUTE_VALUES S INNER JOIN ATTRIBUTE_DEFN (NOLOCK) A ON A.STANDARD_ATTRIBUTE_CODE=S.STANDARD_ATTRIBUTE_CODE WHERE S.STANDARD_ATTRIBUTE_CODE = '{}' AND A.SYSTEM_ID = '{}' AND S.STANDARD_ATTRIBUTE_VALUE = '{}' ".format(STANDARD_ATTRIBUTE_VALUES.STANDARD_ATTRIBUTE_CODE,attrs,  attributevalues[attrs] ) )
							ent_disp_val = get_display_val.STANDARD_ATTRIBUTE_DISPLAY_VAL 

						#Log.Info(str(OfferingRow_detail.SERVICE_ID)+'---194----attrs--')
						if str(attrs) == 'AGS_REL_STDATE' and "Z0007" in OfferingRow_detail.SERVICE_ID:
							try:
								#Trace.Write('except-try----date-------')
								HasDefaultvalue = True
								QuoteStartDate = datetime.datetime.strptime(Quote.GetCustomField('QuoteStartDate').Content, '%Y-%m-%d').date()
								ent_disp_val = 	str(QuoteStartDate.strftime("%m/%d/%Y"))
								ent_val_code = ''
								#Trace.Write(str(HasDefaultvalue)+'-date--ent_disp_val---inside try--'+str(ent_disp_val))
							except:
								#HasDefaultvalue==True
								#Trace.Write(str(HasDefaultvalue)+'except--ent_disp_val------'+str(ent_disp_val))
								ent_disp_val = ent_disp_val
								ent_val_code = ''
						else:
							Trace.Write('208--attrs---'+str(attrs))
							ent_disp_val = ent_disp_val
							ent_val_code = ent_val_code
						#Trace.Write(str(attrs)+'---209----'+str(HasDefaultvalue)+'--attrs---208---ent_disp_val----'+str(ent_disp_val))
						if str(attrs) == 'AGS_CON_DAY' and 'Z0016' in OfferingRow_detail.SERVICE_ID: 
							try:
								QuoteEndDate = datetime.datetime.strptime(Quote.GetCustomField('QuoteExpirationDate').Content, '%Y-%m-%d').date()
								Trace.Write('208--attrs---date check')
								QuoteStartDate = datetime.datetime.strptime(Quote.GetCustomField('QuoteStartDate').Content, '%Y-%m-%d').date()
								contract_days = (QuoteEndDate - QuoteStartDate).days
								ent_disp_val = 	str(contract_days)
								Trace.Write('208--attrs---date check--ent_disp_val--'+str(ent_disp_val))
							except:
								#Log.Info('except-----')
								ent_disp_val = ent_disp_val 
						
									
						else:
							ent_disp_val = ent_disp_val
						#A055S000P01-7401 START
						if str(attrs) == 'AGS_POA_PROD_TYPE' and ent_disp_val != '':
							#Log.Info("ENTERED POA----------->")
							val = ""
							if str(ent_disp_val) == 'Comprehensive':
								val = "COMPREHENSIVE SERVICES"
							elif str(ent_disp_val) == 'Complementary':
								val = "COMPLEMENTARY PRODUCTS"
							Sql.RunQuery("UPDATE SAQTSV SET SERVICE_TYPE = '{}' WHERE QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(str(val),quote_record_id,OfferingRow_detail.SERVICE_ID,Quote.GetGlobal("quote_revision_record_id")))
						#A055S000P01-7401 END                    
						DTypeset={"Drop Down":"DropDown","Free Input, no Matching":"FreeInputNoMatching","Check Box":"CheckBox"}
						#Trace.Write(str(attrs)+'--------'+str(HasDefaultvalue)+'----ent_disp_val----ent_disp_val-HasDefaultvalue=True--'+str(ent_disp_val))
						#Trace.Write("ent_name--"+str(attrs))
						insertservice += """<QUOTE_ITEM_ENTITLEMENT>
						<ENTITLEMENT_NAME>{ent_name}</ENTITLEMENT_NAME>
						<ENTITLEMENT_VALUE_CODE>{ent_val_code}</ENTITLEMENT_VALUE_CODE>
						<ENTITLEMENT_TYPE>{ent_type}</ENTITLEMENT_TYPE>                        
						<ENTITLEMENT_DISPLAY_VALUE>{ent_disp_val}</ENTITLEMENT_DISPLAY_VALUE>
						<ENTITLEMENT_DESCRIPTION>{ent_desc}</ENTITLEMENT_DESCRIPTION>
						<ENTITLEMENT_COST_IMPACT>{ct}</ENTITLEMENT_COST_IMPACT>
						<ENTITLEMENT_PRICE_IMPACT>{pi}</ENTITLEMENT_PRICE_IMPACT>
						<IS_DEFAULT>{is_default}</IS_DEFAULT>
						<PRICE_METHOD>{pm}</PRICE_METHOD>
						<CALCULATION_FACTOR>{cf}</CALCULATION_FACTOR>
						</QUOTE_ITEM_ENTITLEMENT>""".format(ent_name = str(attrs),ent_val_code = ent_val_code,ent_type = DTypeset[PRODUCT_ATTRIBUTES.ATT_DISPLAY_DESC] if PRODUCT_ATTRIBUTES else  '',ent_desc = ATTRIBUTE_DEFN.STANDARD_ATTRIBUTE_NAME,ent_disp_val = ent_disp_val if  HasDefaultvalue else '' ,ct = '',pi = '',is_default = '1' if str(attrs) in attributedefaultvalue else '0',pm = '',cf = '')
				Trace.Write('238--insertservice----'+str(insertservice))   
				tbrow["QUOTE_SERVICE_ENTITLEMENT_RECORD_ID"]=str(Guid.NewGuid()).upper()
				tbrow["QUOTE_ID"]=OfferingRow_detail.QUOTE_ID
				tbrow["ENTITLEMENT_XML"]=insertservice
				tbrow["QUOTE_NAME"]=OfferingRow_detail.QUOTE_NAME
				tbrow["QUOTE_RECORD_ID"]=OfferingRow_detail.QUOTE_RECORD_ID
				tbrow["QTESRV_RECORD_ID"]=OfferingRow_detail.QUOTE_SERVICE_RECORD_ID
				tbrow["SERVICE_RECORD_ID"]=OfferingRow_detail.SERVICE_RECORD_ID
				tbrow["SERVICE_ID"]=OfferingRow_detail.SERVICE_ID
				tbrow["SERVICE_DESCRIPTION"]=OfferingRow_detail.SERVICE_DESCRIPTION
				tbrow["CPS_CONFIGURATION_ID"]=Fullresponse['id']
				tbrow["SALESORG_RECORD_ID"]=OfferingRow_detail.SALESORG_RECORD_ID
				tbrow["SALESORG_ID"]=OfferingRow_detail.SALESORG_ID
				tbrow["SALESORG_NAME"]=OfferingRow_detail.SALESORG_NAME
				tbrow["CPS_MATCH_ID"] = 11
				tbrow["CPQTABLEENTRYADDEDBY"] = User.Id
				tbrow["CPQTABLEENTRYDATEADDED"] = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p")
				tbrow["QTEREV_RECORD_ID"] = Quote.GetGlobal("quote_revision_record_id")
				tbrow["QTEREV_ID"] = Quote.GetGlobal("quote_revision_id")
				#tbrow["IS_DEFAULT"] = '1'
				#Trace.Write('254----')
				columns = ', '.join("" + str(x) + "" for x in tbrow.keys())
				values = ', '.join("'" + str(x) + "'" for x in tbrow.values())
				#Trace.Write('257----')
				insert_qtqtse_query = "INSERT INTO SAQTSE ( %s ) VALUES ( %s );" % (columns, values)
				Sql.RunQuery(insert_qtqtse_query)
				Trace.Write('269-addednew trace---')
				try:
					Trace.Write('269--')
					if 'Z0016' in OfferingRow_detail.SERVICE_ID:
						Trace.Write('269--OfferingRow_detail--')
						try:
							QuoteEndDate = datetime.datetime.strptime(Quote.GetCustomField('QuoteExpirationDate').Content, '%Y-%m-%d').date()
							QuoteStartDate = datetime.datetime.strptime(Quote.GetCustomField('QuoteStartDate').Content, '%Y-%m-%d').date()
							contract_days = (QuoteEndDate - QuoteStartDate).days
							ent_disp_val = 	str(contract_days)
						except:
							#Log.Info('except-----')
							ent_disp_val = ent_disp_val
						Trace.Write('269--OfferingRow_detail-ent_disp_val----'+str(ent_disp_val))
						cpsmatchID = tbrow["CPS_MATCH_ID"]
						cpsConfigID = Fullresponse['id']
						if int(ent_disp_val) > 364:
							
							Trace.Write("---requestdata--244-cpsConfigID0-----")
							webclient = System.Net.WebClient()
							webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/json"
							webclient.Headers[System.Net.HttpRequestHeader.Authorization] = "Basic c2ItYzQwYThiMWYtYzU5NS00ZWJjLTkyYzYtYzM4ODg4ODFmMTY0IWIyNTAzfGNwc2VydmljZXMtc2VjdXJlZCFiMzkxOm9zRzgvSC9hOGtkcHVHNzl1L2JVYTJ0V0FiMD0="
							response = webclient.DownloadString("https://cpqprojdevamat.authentication.us10.hana.ondemand.com:443/oauth/token?grant_type=client_credentials")
							response = eval(response)
							webclient = System.Net.WebClient()		
							#Log.Info("---requestdata--252--")
							Request_URL = "https://cpservices-product-configuration.cfapps.us10.hana.ondemand.com/api/v2/configurations/"+str(cpsConfigID)+"/items/1"
							webclient.Headers[System.Net.HttpRequestHeader.Authorization] = "Bearer " + str(response["access_token"])
							#webclient.Headers.Add("If-Match", "111")

							webclient.Headers.Add("If-Match", "1"+str(cpsmatchID))
									
							AttributeID = 'AGS_CON_DAY'
							NewValue = ent_disp_val
							quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
							#Trace.Write("---requestdata--252-NewValue-----"+str(NewValue))
							whereReq = "QUOTE_RECORD_ID = '"+str(quote_record_id)+"' and SERVICE_ID LIKE '%Z0016%'"+ " AND QTEREV_RECORD_ID = '" +str(quote_revision_record_id) + "'"
							#Trace.Write('whereReq---'+str(whereReq))
							requestdata = '{"characteristics":[{"id":"'+AttributeID+'","values":[{"value":"'+NewValue+'","selected":true}]}]}'
							#Trace.Write("---eqruestdata---requestdata----"+str(requestdata))
							response2 = webclient.UploadString(Request_URL, "PATCH", str(requestdata))
							#requestdata = {"characteristics":[{"id":"' + AttributeID + '":[{"value":"' +NewValue+'","selected":true}]}]}

							#Log.Info(str(Request_URL)+"---requestdata--166---" + str(response2))


							#Log.Info("patch response1---170---" + str(response2))
							Request_URL = "https://cpservices-product-configuration.cfapps.us10.hana.ondemand.com/api/v2/configurations/"+str(cpsConfigID)
							webclient.Headers[System.Net.HttpRequestHeader.Authorization] = "Bearer " + str(response["access_token"])
							#Log.Info("requestdata---180--265----" + str(requestdata))
							response2 = webclient.DownloadString(Request_URL)
							Trace.Write('response2--182----267-----'+str(response2))
							response2 = str(response2).replace(": true", ': "true"').replace(": false", ': "false"')
							Fullresponse= eval(response2)
							attributesdisallowedlst=[]
							attributeReadonlylst=[]
							attributesallowedlst=[]
							attributedefaultvalue = []
							#overallattributeslist =[]
							attributevalues={}
							for rootattribute, rootvalue in Fullresponse.items():
								if rootattribute=="rootItem":
									for Productattribute, Productvalue in rootvalue.items():
										if Productattribute=="characteristics":
											for prdvalue in Productvalue:
												#overallattributeslist.append(prdvalue['id'])
												if prdvalue['visible'] =='false':
													attributesdisallowedlst.append(prdvalue['id'])
												else:
													#Trace.Write(prdvalue['id']+" set here")
													attributesallowedlst.append(prdvalue['id'])
												if prdvalue['readOnly'] =='true':
													attributeReadonlylst.append(prdvalue['id'])
												for attribute in prdvalue['values']:
													attributevalues[str(prdvalue['id'])]=attribute['value']
													if attribute["author"] in ("Default","System"):
														Trace.Write('524------'+str(prdvalue["id"]))
														attributedefaultvalue.append(prdvalue["id"])
							
							attributesallowedlst = list(set(attributesallowedlst))
							#overallattributeslist = list(set(overallattributeslist))
							Trace.Write('attributesallowedlst---'+str(attributesallowedlst)) 
							HasDefaultvalue=False
							#Trace.Write('response2--182----315---')
							ProductVersionObj=Sql.GetFirst("Select product_id from product_versions(nolock) where SAPKBVersion='"+str(Fullresponse['kbKey']['version'])+"'")
							if ProductVersionObj is not None:
								tbrow={}   
								insertservice = ""
								tblist = []
								#Log.Info('response2--182----321-')
								for attrs in attributesallowedlst:
									#tbrow1 = {}
									if attrs in attributevalues:
										HasDefaultvalue=True
										STANDARD_ATTRIBUTE_VALUES=Sql.GetFirst("SELECT S.STANDARD_ATTRIBUTE_DISPLAY_VAL,S.STANDARD_ATTRIBUTE_CODE FROM STANDARD_ATTRIBUTE_VALUES (nolock) S INNER JOIN ATTRIBUTE_DEFN (NOLOCK) A ON A.STANDARD_ATTRIBUTE_CODE=S.STANDARD_ATTRIBUTE_CODE WHERE A.SYSTEM_ID = '{}'".format(attrs,attributevalues[attrs]))
										ent_disp_val = attributevalues[attrs]
									else:
										HasDefaultvalue=False
										ent_disp_val = ""
										STANDARD_ATTRIBUTE_VALUES=Sql.GetFirst("SELECT S.STANDARD_ATTRIBUTE_CODE FROM STANDARD_ATTRIBUTE_VALUES (nolock) S INNER JOIN ATTRIBUTE_DEFN (NOLOCK) A ON A.STANDARD_ATTRIBUTE_CODE=S.STANDARD_ATTRIBUTE_CODE WHERE A.SYSTEM_ID = '{}'".format(attrs))
									ATTRIBUTE_DEFN=Sql.GetFirst("SELECT * FROM ATTRIBUTE_DEFN (NOLOCK) WHERE SYSTEM_ID='{}'".format(attrs))
									PRODUCT_ATTRIBUTES=Sql.GetFirst("SELECT A.ATT_DISPLAY_DESC FROM ATT_DISPLAY_DEFN (NOLOCK) A INNER JOIN PRODUCT_ATTRIBUTES (NOLOCK) P ON A.ATT_DISPLAY=P.ATT_DISPLAY WHERE P.PRODUCT_ID={} AND P.STANDARD_ATTRIBUTE_CODE={}".format(ProductVersionObj.product_id,STANDARD_ATTRIBUTE_VALUES.STANDARD_ATTRIBUTE_CODE))
									
									if PRODUCT_ATTRIBUTES.ATT_DISPLAY_DESC in ('Drop Down','Check Box') and ent_disp_val:
										get_display_val = Sql.GetFirst("SELECT STANDARD_ATTRIBUTE_DISPLAY_VAL  from STANDARD_ATTRIBUTE_VALUES S INNER JOIN ATTRIBUTE_DEFN (NOLOCK) A ON A.STANDARD_ATTRIBUTE_CODE=S.STANDARD_ATTRIBUTE_CODE WHERE S.STANDARD_ATTRIBUTE_CODE = '{}' AND A.SYSTEM_ID = '{}' AND S.STANDARD_ATTRIBUTE_VALUE = '{}' ".format(STANDARD_ATTRIBUTE_VALUES.STANDARD_ATTRIBUTE_CODE,attrs,  attributevalues[attrs] ) )
										ent_disp_val = get_display_val.STANDARD_ATTRIBUTE_DISPLAY_VAL 

								
									
									DTypeset={"Drop Down":"DropDown","Free Input, no Matching":"FreeInputNoMatching","Check Box":"CheckBox"}
									#Log.Info('response2--182----342-')
									#Trace.Write("ent_name--"+str(attrs))
									insertservice += """<QUOTE_ITEM_ENTITLEMENT>
									<ENTITLEMENT_NAME>{ent_name}</ENTITLEMENT_NAME>
									<ENTITLEMENT_VALUE_CODE>{ent_val_code}</ENTITLEMENT_VALUE_CODE>
									<ENTITLEMENT_TYPE>{ent_type}</ENTITLEMENT_TYPE>                                    
									<ENTITLEMENT_DISPLAY_VALUE>{ent_disp_val}</ENTITLEMENT_DISPLAY_VALUE>
									<ENTITLEMENT_DESCRIPTION>{ent_desc}</ENTITLEMENT_DESCRIPTION>
									<ENTITLEMENT_COST_IMPACT>{ct}</ENTITLEMENT_COST_IMPACT>
									<ENTITLEMENT_PRICE_IMPACT>{pi}</ENTITLEMENT_PRICE_IMPACT>
									<IS_DEFAULT>{is_default}</IS_DEFAULT>
									<PRICE_METHOD>{pm}</PRICE_METHOD>
									<CALCULATION_FACTOR>{cf}</CALCULATION_FACTOR> 
									</QUOTE_ITEM_ENTITLEMENT>""".format(ent_name = str(attrs),ent_val_code = attributevalues[attrs] if HasDefaultvalue==True else '',ent_type = DTypeset[PRODUCT_ATTRIBUTES.ATT_DISPLAY_DESC] if PRODUCT_ATTRIBUTES else  '',ent_desc = ATTRIBUTE_DEFN.STANDARD_ATTRIBUTE_NAME,ent_disp_val = ent_disp_val if HasDefaultvalue==True else '',ct = '',pi = '',is_default = '1' if str(attrs) in attributedefaultvalue else '0',pm = '',cf = '')
									cpsmatc_incr = int(cpsmatchID) + 10
									Trace.Write('cpsmatc_incr'+str(cpsmatc_incr))
									Updatecps = "UPDATE {} SET CPS_MATCH_ID ={},CPS_CONFIGURATION_ID = '{}',ENTITLEMENT_XML='{}',CpqTableEntryModifiedBy = {}, CpqTableEntryDateModified = GETDATE() WHERE {} ".format('SAQTSE', cpsmatc_incr,cpsConfigID,insertservice, User.Id, whereReq)
									Trace.Write('Updatecps'+str(Updatecps))
									Sql.RunQuery(Updatecps)
						

				except:
					Trace.Write('except scenario----final--')
					cpsmatc_incr = ''

				#inseryservice_ent = """INSERT SAQTSE () VALUES ()"""
				#Log.Info('inseryservice_ent-----columns-----values----'+str(insert_qtqtse_query))

	def create_custom_table_record(self):
		contract_quote_data = {}
		sync_start_time = time.time()
		#Log.Info("Sync start ==> "+str(sync_start_time))
		
		try:
			if self.quote:
				quote_table_info = Sql.GetTable("SAQTMT")
				quote_involved_party_table_info = Sql.GetTable("SAQTIP")
				quote_opportunity_table_info = Sql.GetTable("SAOPQT")
				quote_fab_table_info = Sql.GetTable("SAQFBL")
				custom_fields_detail = self._get_custom_fields_detail()
				Log.Info("custom_fields_detail =====>>>>>> " + str(custom_fields_detail))              
				start_date = self.get_formatted_date(
					custom_fields_detail.get("QuoteStartDate").year,
					custom_fields_detail.get("QuoteStartDate").month,
					custom_fields_detail.get("QuoteStartDate").day,
					"{Month}{Separator}{Date}{Separator}{Year}",
					"/",
				)
				end_date = self.get_formatted_date(
					custom_fields_detail.get("QuoteExpirationDate").year,
					custom_fields_detail.get("QuoteExpirationDate").month,
					custom_fields_detail.get("QuoteExpirationDate").day,
					"{Month}{Separator}{Date}{Separator}{Year}",
					"/",
				)
				pricing_date = ''
				if custom_fields_detail.get("PricingDate"):
					pricing_date = self.get_formatted_date(
						custom_fields_detail.get("PricingDate").year,
						custom_fields_detail.get("PricingDate").month,
						custom_fields_detail.get("PricingDate").day,
						"{Month}{Separator}{Date}{Separator}{Year}",
						"/",
					)
						
				# quote_id = "SQ{}RV00-RW00AM00-{}".format(
				# 	self.quote.CompositeNumber,
				# 	self.get_formatted_date(
				# 		custom_fields_detail.get("QuoteExpirationDate").year,
				# 		custom_fields_detail.get("QuoteExpirationDate").month,
				# 		custom_fields_detail.get("QuoteExpirationDate").day,
				# 		"{Year}{Separator}{Month}{Separator}{Date}",
				# 	),
				# )
				quote_id = self.quote.CompositeNumber
				quote_obj = Sql.GetFirst(
					"SELECT * FROM SAQTMT (NOLOCK) WHERE QUOTE_ID = '{}' AND C4C_QUOTE_ID = '{}'".format(
						quote_id, self.quote.CompositeNumber
					)
				)
				payid =""
				paydesc = ""
				payrec = ""
				pay_days = pay_name = ""
				if not quote_obj:
					Trace.Write("Quote Id ==> 477---" + str(self.quote.CompositeNumber))
					if custom_fields_detail.get("SalesOrgID"):
						salesorg_obj = Sql.GetFirst(
							"SELECT SALESORG_ID,SALES_ORG_RECORD_ID, SALESORG_NAME,REGION,REGION_RECORD_ID FROM SASORG (NOLOCK) WHERE SALESORG_ID = '{}'".format(
								custom_fields_detail.get("SalesOrgID")
							)
						)
					if custom_fields_detail.get("STPAccountID"):						
						salesorg_country = Sql.GetFirst("SELECT COUNTRY,COUNTRY_RECORD_ID FROM SASORG (NOLOCK) WHERE SALESORG_ID = '{}'".format(custom_fields_detail.get("SalesOrgID")))
						salesorg_country_name = Sql.GetFirst("SELECT COUNTRY_NAME FROM SACTRY (NOLOCK) WHERE COUNTRY = '{}'".format(salesorg_country.COUNTRY))
						""" if salesorg_obj:
							contract_quote_data.update(
								{
									"SALESORG_RECORD_ID": salesorg_obj.SALES_ORG_RECORD_ID,
									"SALESORG_NAME": salesorg_obj.SALESORG_NAME,
								}
							) """
					if custom_fields_detail.get("PaymentTerms"):
						payid =""
						paydesc = ""
						payrec = ""
						payterm_obj = Sql.GetFirst(
							"SELECT PAYMENT_TERM_ID, PAYMENT_TERM_NAME,NUMBER_OF_DAYS,PAYMENT_TERM_RECORD_ID,DESCRIPTION FROM PRPTRM (NOLOCK) WHERE PAYMENT_TERM_ID = '{}'".format(
								custom_fields_detail.get("PaymentTerms")
							)
						)
						if payterm_obj:
							payid =payterm_obj.PAYMENT_TERM_ID
							paydesc = payterm_obj.DESCRIPTION
							payrec = payterm_obj.PAYMENT_TERM_RECORD_ID
							pay_days = payterm_obj.NUMBER_OF_DAYS
							pay_name = payterm_obj.PAYMENT_TERM_NAME
							# contract_quote_data.update(
							# 	{
							# 		"PAYMENTTERM_ID": payterm_obj.PAYMENT_TERM_ID,
							# 		"PAYMENTTERM_DAYS": payterm_obj.NUMBER_OF_DAYS,
							# 		"PAYMENTTERM_NAME": payterm_obj.PAYMENT_TERM_NAME,
							# 		"PAYMENTTERM_RECORD_ID": payterm_obj.PAYMENT_TERM_RECORD_ID,
							# 	}
							# )
					else:
						payid =""
						paydesc = ""
						payrec = ""
						pay_days =""
					# self.quote.OrderStatus.Name
					#Log.Info("expired"+str(start_date)+"sdate---"+str(created_date))
					created_date = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p")
					expired_date = date.today()+ timedelta(days=365)
					#A055S000P01-7866
					#document_type = {"ZTBC": "SSC", "ZWK1": "APG"}
					quote_type = {"ZTBC":"ZTBC - TOOL BASED", "ZNBC":"ZNBC - NON TOOL BASED", "ZWK1":"ZWK1 - SPARES", "ZSWC":"ZSWC - SOLD WITH SYSTEM"}
					opportunity_type = {"ZTBC":"Service", "ZWK1":"Parts"}
					contract_quote_data.update(
						{
							"QUOTE_ID": quote_id,
							"C4C_QUOTE_ID": self.quote.CompositeNumber,
							"MASTER_TABLE_QUOTE_RECORD_ID": str(Guid.NewGuid()).upper(),
							"REGION": salesorg_obj.REGION,
							#"SALESORG_ID": custom_fields_detail.get("SalesOrgID"),
							"SALE_TYPE": custom_fields_detail.get("SalesType"),
							#"CANCELLATION_PERIOD":"90 DAYS",
							#"DOCUMENT_TYPE": document_type.get(self.quote.DocumentTypeCode),
							#"DOCUMENT_TYPE": "",
							#"OPPORTUNITY_TYPE": opportunity_type.get(custom_fields_detail.get("ContractType")),
							"QUOTE_STATUS": "IN-PROGRESS",
							"QUOTE_LEVEL": custom_fields_detail.get("QuoteLevel")
							if custom_fields_detail.get("QuoteLevel")
							else "SALES ORG LEVEL",
							"CONTRACT_VALID_FROM": start_date,
							"CONTRACT_VALID_TO": end_date,
							"QUOTE_CREATED_DATE": str(created_date),                            
							"QUOTE_EXPIRE_DATE":str(expired_date),
							#"OPPORTUNITY_ID": custom_fields_detail.get("OpportunityId"),
							"QUOTE_NAME": custom_fields_detail.get("STPAccountName"),
							#"EMPLOYEE_ID": custom_fields_detail.get("SalesPerson"),
							"SOURCE_CONTRACT_ID": custom_fields_detail.get("SourceContractID"),
							"QUOTE_TYPE":quote_type.get(custom_fields_detail.get("ContractType")),
							"QUOTE_CURRENCY":custom_fields_detail.get("Currency"),
							"GLOBAL_CURRENCY":"USD",
							"QTEREV_STATUS":"NEW REVISION"
							#"INCOTERMS":custom_fields_detail.get("Incoterms"),
							#"INCOTERMS_LOCATION":custom_fields_detail.get("IncotermsLocation"),
							#"PRICING_DATE":pricing_date,
							#"EXCHANGE_RATE_TYPE":custom_fields_detail.get("ExchangeRateType"),
							
						}
					)
					#insert in revision table while creating quote start
					quote_revision_table_info = Sql.GetTable("SAQTRV")
					quote_revision_id = str(Guid.NewGuid()).upper()
					get_rev_details = Sql.GetFirst("SELECT DISTINCT TOP 1000 CART2.CARTCOMPOSITENUMBER, CART_REVISIONS.REVISION_ID as REVISION_ID,CART_REVISIONS.DESCRIPTION as DESCRIPTION, CART.ACTIVE_REV as ACTIVE_REV, CART_REVISIONS.CART_ID as CART_ID, CART_REVISIONS.PARENT_ID, CART.USERID FROM CART_REVISIONS (nolock) INNER JOIN CART2 (nolock) ON CART_REVISIONS.CART_ID = CART2.CartId INNER JOIN CART(NOLOCK) ON CART.CART_ID = CART2.CartId WHERE CART2.CARTCOMPOSITENUMBER = '{}'".format(Quote.CompositeNumber))
					Quote.SetGlobal("quote_revision_record_id",str(quote_revision_id))
					quote_rev_id = get_rev_details.REVISION_ID
					Quote.SetGlobal("quote_revision_id",str(quote_rev_id))
					#created_date = datetime.datetime.now().strftime("%m/%d/%Y")
					#expired_date = datetime.datetime.now().strftime("%m/%d/%Y")
					#Trace.Write('571-------'+str(end_date))
					#expired_date_val = date.today()+ timedelta(days=365)
					expired_date_val = datetime.datetime.strptime(end_date, '%m/%d/%Y').date()
					expired_date_val = expired_date_val + timedelta(days=365)
					Trace.Write(str(expired_date_val)+'571----expired_date_val---'+str(type(end_date)))
					#quote_rev_data = {"QUOTE_REVISION_RECORD_ID": str(quote_revision_id),"QUOTE_ID": quote_id,"QUOTE_NAME": '',"REVISION_DESCRIPTION":get_rev_details.DESCRIPTION,"QUOTE_RECORD_ID": contract_quote_data.get("MASTER_TABLE_QUOTE_RECORD_ID"),"ACTIVE":get_rev_details.ACTIVE_REV,"REV_CREATE_DATE":str(created_date),"REV_EXPIRE_DATE":str(expired_date),"REVISION_STATUS":"IN-PROGRESS","QTEREV_ID":quote_rev_id,"REV_APPROVE_DATE":'',"CART_ID":get_rev_details.CART_ID}
					# if salesorg_obj and get_rev_details:
					# 	quote_rev_data = {
					# 		"QUOTE_REVISION_RECORD_ID": str(Guid.NewGuid()).upper(),
					# 		"QUOTE_ID": quote_id,
					# 		"QUOTE_NAME": contract_quote_data.get("contract_quote_data"),
					# 		"QUOTE_RECORD_ID": contract_quote_data.get("MASTER_TABLE_QUOTE_RECORD_ID"),
					# 		"SALESORG_ID": custom_fields_detail.get("SalesOrgID"),
					# 		"COUNTRY": salesorg_country.COUNTRY,
					# 		"COUNTRY_NAME": salesorg_country_name.COUNTRY_NAME,
					# 		"COUNTRY_RECORD_ID":salesorg_country.COUNTRY_RECORD_ID,
					# 		"REGION":salesorg_obj.REGION,
					# 		"SALESORG_NAME": salesorg_obj.SALESORG_NAME,
					# 		"SALESORG_RECORD_ID": salesorg_obj.SALES_ORG_RECORD_ID,							
					# 		"GLOBAL_CURRENCY":contract_quote_data.get("GLOBAL_CURRENCY"),							
					# 		"GLOBAL_CURRENCY_RECORD_ID":contract_quote_data.get("GLOBAL_CURRENCY_RECORD_ID"),
					# 		"QTEREV_RECORD_ID":quote_revision_id,
					# 		"QTEREV_ID":quote_rev_id,
					# 		"REVISION_DESCRIPTION":get_rev_details.DESCRIPTION,
					# 		"ACTIVE":get_rev_details.ACTIVE_REV,
					# 		"REV_CREATE_DATE":str(created_date),
					# 		"REV_EXPIRE_DATE":str(expired_date),
					# 		"REVISION_STATUS":"IN-PROGRESS",
					# 		"REV_APPROVE_DATE":'',
					# 		"CART_ID":get_rev_details.CART_ID
					# 	}
					# 	#quote_revision_table_info.AddRow(quote_rev_data)
					# 	# UPDATE REVISION DETAILS TO SAQTMT
					# 	contract_quote_data.update({"QTEREV_RECORD_ID":quote_revision_id, 
					# 								"QTEREV_ID":quote_rev_id })
					# 	Quote.GetCustomField('QUOTE_REVISION_ID').Content = quote_revision_id
					# 	Log.Info('quote_revision_table_info---443--quote_rev_data--'+str(quote_rev_data))
					# 	#Sql.Upsert(quote_revision_table_info)
					# 	Trace.Write('575---quote_rev_data--'+str(quote_rev_data))
					
					#insert in revision table while creating quote end
					if custom_fields_detail.get('Currency'):
							Currency_obj = Sql.GetFirst(
								"SELECT CURRENCY,CURRENCY_NAME, CURRENCY_RECORD_ID FROM PRCURR (NOLOCK) WHERE CURRENCY = '{}'".format(
									custom_fields_detail.get('Currency')
								)
							)
							##get global currency_rec_id 
							global_currency_obj = Sql.GetFirst(
								"SELECT CURRENCY,CURRENCY_NAME, CURRENCY_RECORD_ID FROM PRCURR (NOLOCK) WHERE CURRENCY = '{}'".format(
									contract_quote_data.get('GLOBAL_CURRENCY')
								)
							)
							if Currency_obj and global_currency_obj:
								contract_quote_data.update({"QUOTE_CURRENCY":Currency_obj.CURRENCY , 
													"QUOTE_CURRENCY_RECORD_ID":Currency_obj.CURRENCY_RECORD_ID,
													"GLOBAL_CURRENCY_RECORD_ID":global_currency_obj.CURRENCY_RECORD_ID })
					if custom_fields_detail.get('EmployeeResponsibleID'):
							Employee_obj = Sql.GetFirst(
								"SELECT EMPLOYEE_ID,FIRST_NAME,LAST_NAME,EMPLOYEE_RECORD_ID FROM SAEMPL (NOLOCK) WHERE EMPLOYEE_ID = '{}'".format(
									custom_fields_detail.get('EmployeeResponsibleID')
								)
							)
							if Employee_obj:
								Owner_name = Employee_obj.FIRST_NAME+" "+Employee_obj.LAST_NAME
								contract_quote_data.update({"OWNER_ID":Employee_obj.EMPLOYEE_ID , 
													"OWNER_NAME": Owner_name,
													"OWNER_RECORD_ID":Employee_obj.EMPLOYEE_RECORD_ID})								
					if salesorg_obj and get_rev_details:
						quote_salesorg_table_info = Sql.GetTable("SAQTRV")
						salesorg_data = {
							"QUOTE_REVISION_RECORD_ID": str(quote_revision_id),
							"QUOTE_ID": quote_id,
							"QUOTE_NAME": contract_quote_data.get("contract_quote_data"),
							"QUOTE_RECORD_ID": contract_quote_data.get("MASTER_TABLE_QUOTE_RECORD_ID"),
							"SALESORG_ID": custom_fields_detail.get("SalesOrgID"),
							"COUNTRY": salesorg_country.COUNTRY,
							"COUNTRY_NAME": salesorg_country_name.COUNTRY_NAME,
							"COUNTRY_RECORD_ID":salesorg_country.COUNTRY_RECORD_ID,
							"REGION":salesorg_obj.REGION,
							"REGION_RECORD_ID":salesorg_obj.REGION_RECORD_ID,
							"SALESORG_NAME": salesorg_obj.SALESORG_NAME,
							"SALESORG_RECORD_ID": salesorg_obj.SALES_ORG_RECORD_ID,							
							"GLOBAL_CURRENCY":contract_quote_data.get("GLOBAL_CURRENCY"),							
							"GLOBAL_CURRENCY_RECORD_ID":contract_quote_data.get("GLOBAL_CURRENCY_RECORD_ID"),
							"QTEREV_RECORD_ID":quote_revision_id,
							"QTEREV_ID":quote_rev_id,
							"REVISION_DESCRIPTION":"REVISION 0 DESCRIPTION",
							"ACTIVE":get_rev_details.ACTIVE_REV,
							"REV_CREATE_DATE":str(start_date),
							"REV_EXPIRE_DATE":str(expired_date_val),
							"REVISION_STATUS":"NEW REVISION",
							"REV_APPROVE_DATE":'',
							"CART_ID":get_rev_details.CART_ID,
							"CONTRACT_VALID_FROM":start_date,
							"CONTRACT_VALID_TO":end_date,
							"PAYMENTTERM_DAYS":pay_days,
							"PAYMENTTERM_ID":payid,
							"PAYMENTTERM_NAME":pay_name,
							"PAYMENTTERM_RECORD_ID":payrec,
							"EXCHANGE_RATE_TYPE":custom_fields_detail.get("ExchangeRateType")
						}
						# UPDATE REVISION DETAILS TO SAQTMT
						contract_quote_data.update({"QTEREV_RECORD_ID":quote_revision_id, 
													"QTEREV_ID":quote_rev_id })
						Quote.GetCustomField('QUOTE_REVISION_ID').Content = quote_revision_id
						#UPDATE BLUEBOOK TO SAQTRV
						bluebook_obj = Sql.GetFirst(
							"SELECT BLUEBOOK,BLUEBOOK_RECORD_ID FROM SASAAC(NOLOCK) WHERE ACCOUNT_ID LIKE '%{}' ".format(
								custom_fields_detail.get("STPAccountID")
							)
						)
						if bluebook_obj:
							salesorg_data.update({"BLUEBOOK":bluebook_obj.BLUEBOOK,"BLUEBOOK_RECORD_ID":bluebook_obj.BLUEBOOK_RECORD_ID,})
						if custom_fields_detail.get("Incoterms"):
							incid = ""
							incdesc = ""
							increc = ""
							getInc = Sql.GetFirst("SELECT INCOTERM_ID,DESCRIPTION,INCOTERM_RECORD_ID FROM SAICTM WHERE INCOTERM_ID = '{}'".format(custom_fields_detail.get("Incoterms")))
							if getInc:
								incid = getInc.INCOTERM_ID
								incdesc = getInc.DESCRIPTION
								increc = getInc.INCOTERM_RECORD_ID
						else:
							incid = ""
							incdesc = ""
							increc = ""
						salesorg_data.update({"INCOTERM_ID":incid,"INCOTERM_NAME":incdesc,"INCOTERM_RECORD_ID":increc})
						if custom_fields_detail.get('DistributionChannel'):
							distribution_obj = Sql.GetFirst(
								"SELECT DISTRIBUTION_CHANNEL_RECORD_ID, DISTRIBUTIONCHANNEL_ID FROM SADSCH (NOLOCK) WHERE DISTRIBUTIONCHANNEL_ID = '{}'".format(
									custom_fields_detail.get('DistributionChannel')
								)
							)
							if distribution_obj:
								salesorg_data.update({"DISTRIBUTIONCHANNEL_ID":distribution_obj.DISTRIBUTIONCHANNEL_ID , 
													"DISTRIBUTIONCHANNEL_RECORD_ID":distribution_obj.DISTRIBUTION_CHANNEL_RECORD_ID})
						if custom_fields_detail.get('SalesOrgID'):
							createddate_up = ""
							SalesOrg_obj = Sql.GetFirst(
								"SELECT DEF_CURRENCY, DEF_CURRENCY_RECORD_ID FROM SASORG (NOLOCK) WHERE SALESORG_ID = '{}'".format(
									custom_fields_detail.get('SalesOrgID')
								)
							)
							
							
							salesorg_currency = Sql.GetFirst("SELECT CURRENCY,CURRENCY_RECORD_ID FROM PRCURR (NOLOCK) WHERE CURRENCY = '"+str(custom_fields_detail.get("Currency"))+"'")
							if salesorg_currency:
								salesorg_data.update({"DOC_CURRENCY":salesorg_currency.CURRENCY , 
													"DOCCURR_RECORD_ID":salesorg_currency.CURRENCY_RECORD_ID,
													})
							# if SalesOrg_obj:
								
							#     salesorg_data.update({"DOC_CURRENCY":SalesOrg_obj.DEF_CURRENCY, 
							#                         "DOCCURR_RECORD_ID":SalesOrg_obj.DEF_CURRENCY_RECORD_ID})
								##A055S000P01-4418 exchange rate details starts..
								exchange_obj = Sql.GetFirst("SELECT EXCHANGE_RATE,EXCHANGE_RATE_BEGIN_DATE,EXCHANGE_RATE_END_DATE,EXCHANGE_RATE_RECORD_ID from PREXRT where FROM_CURRENCY = '{}' and TO_CURRENCY='{}' AND ACTIVE = 1 and EXCHANGE_RATE_TYPE = '{}'".format(contract_quote_data.get("GLOBAL_CURRENCY"),SalesOrg_obj.DEF_CURRENCY,salesorg_data.get("EXCHANGE_RATE_TYPE")))
								Log.Info("SELECT EXCHANGE_RATE,EXCHANGE_RATE_BEGIN_DATE,EXCHANGE_RATE_END_DATE,EXCHANGE_RATE_RECORD_ID from PREXRT where FROM_CURRENCY = '{}' and TO_CURRENCY='{}' AND ACTIVE = 1 and EXCHANGE_RATE_TYPE = '{}'".format(contract_quote_data.get("GLOBAL_CURRENCY"),SalesOrg_obj.DEF_CURRENCY,salesorg_data.get("EXCHANGE_RATE_TYPE")))
								
								if exchange_obj:
									ex_rate_begin = exchange_obj.EXCHANGE_RATE_BEGIN_DATE
									ex_rate_end = exchange_obj.EXCHANGE_RATE_END_DATE
								
									createddate= datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p")
									if createddate > ex_rate_begin:										
										createddate_up = createddate
									
									salesorg_data.update({'EXCHANGE_RATE':exchange_obj.EXCHANGE_RATE,'EXCHANGE_RATE_DATE':createddate_up,'EXCHANGERATE_RECORD_ID':exchange_obj.EXCHANGE_RATE_RECORD_ID})
									##A055S000P01-4418 exchange rate details ends..
								##Commented the below code already we updated the exchange rate details in the above code..
								# TO_CURRENCY_val = contract_quote_data.get("GLOBAL_CURRENCY")
								# if 	TO_CURRENCY_val == 'USD' and SalesOrg_obj.DEF_CURRENCY == 'USD':
								# 	try:
								# 		QuoteStartDate = datetime.datetime.strptime(Quote.GetCustomField('QuoteStartDate').Content, '%Y-%m-%d').date()
								# 	except:
								# 		QuoteStartDate =''
								# 	Trace.Write('QuoteStartDate------'+str(QuoteStartDate))
								# 	salesorg_data.update({'EXCHANGE_RATE':'1'})
								# 	salesorg_data.update({'EXCHANGE_RATE_DATE':str(QuoteStartDate)})
								##Commented the below code already we updated the exchange rate details in the above code..

								#commented the below code we updated the exchange rate type from Custom field.	
								#exchange_rate_obj = Sql.GetFirst("SELECT EXCHANGE_RATE_TYPE from SASAAC where SALESORG_ID = '{}' and DIVISION_ID='{}' AND ACCOUNT_ID LIKE '%{}' AND DISTRIBUTIONCHANNEL_ID = '{}'".format(custom_fields_detail.get("SalesOrgID"),custom_fields_detail.get('Division'),custom_fields_detail.get("STPAccountID"),custom_fields_detail.get('DistributionChannel')))
								
								#if exchange_rate_obj:
									#salesorg_data.update({'EXCHANGE_RATE_TYPE':exchange_rate_obj.EXCHANGE_RATE_TYPE})
						if custom_fields_detail.get('Division'):
							division_obj = Sql.GetFirst(
								"SELECT DIVISION_RECORD_ID, DIVISION_ID FROM SADIVN (NOLOCK) WHERE DIVISION_ID = '{}'".format(
									custom_fields_detail.get('Division')
								)
							)
							if division_obj:
								salesorg_data.update({"DIVISION_RECORD_ID":division_obj.DIVISION_RECORD_ID , 
													"DIVISION_ID":division_obj.DIVISION_ID})
						
						if custom_fields_detail.get('SalesOfficeID'):
							salesoffice_obj = Sql.GetFirst(
								"SELECT SALES_OFFICE_RECORD_ID, SALES_OFFICE_ID, SALES_OFFICE_NAME FROM SASLOF (NOLOCK) WHERE SALES_OFFICE_ID = '{}'".format(
									custom_fields_detail.get('SalesOfficeID')
								)
							)
							if salesoffice_obj:
								salesorg_data.update({"SALESOFFICE_ID":salesoffice_obj.SALES_OFFICE_ID , 
													"SALESOFFICE_NAME":salesoffice_obj.SALES_OFFICE_NAME,
													"SALESOFFICE_RECORD_ID":salesoffice_obj.SALES_OFFICE_RECORD_ID
													})
						if custom_fields_detail.get('SalesOrgID'):
							salesorg_obj = Sql.GetFirst(
								"SELECT * FROM SASORG (NOLOCK) WHERE SALESORG_ID = '{}'".format(
									custom_fields_detail.get('SalesOrgID')
								)
							)
							salesorg_currency = Sql.GetFirst("SELECT CURRENCY,CURRENCY_RECORD_ID FROM PRCURR (NOLOCK) WHERE CURRENCY = '"+str(custom_fields_detail.get("Currency"))+"'")
							if salesorg_currency:
								salesorg_data.update({"DOC_CURRENCY":salesorg_currency.CURRENCY , 
													"DOCCURR_RECORD_ID":salesorg_currency.CURRENCY_RECORD_ID,
													})
							# if salesorg_obj:
								# salesorg_data.update({"DOC_CURRENCY":salesorg_obj.DEF_CURRENCY , 
								#                     "DOCCURR_RECORD_ID":salesorg_obj.DEF_CURRENCY_RECORD_ID,
								#                     })
						if str(salesorg_data.get('SALESORG_ID')):
							#Log.Info("TAX_DETAILS")
							tax_details = Sql.GetFirst("SELECT * FROM SAASCT (NOLOCK) WHERE SALESORG_ID = '{}' AND DISTRIBUTIONCHANNEL_ID= '{}' AND DIVISION_ID = '{}' AND COUNTRY_NAME = '{}' AND ACCOUNT_ID LIKE '%{}%'".format(salesorg_data.get('SALESORG_ID'),salesorg_data.get('DISTRIBUTIONCHANNEL_ID'),salesorg_data.get('DIVISION_ID'),salesorg_data.get('COUNTRY_NAME'),custom_fields_detail.get("STPAccountID")))
							#Log.Info("""SELECT * FROM SAASCT (NOLOCK) WHERE SALESORG_ID = '{}' AND DISTRIBUTIONCHANNEL_ID= '{}' AND DIVISION_ID = '{}'""".format(salesorg_data.get('SALESORG_ID'),salesorg_data.get('DISTRIBUTIONCHANNEL_ID'),salesorg_data.get('DIVISION_ID')))
							if tax_details:
								salesorg_data.update({"ACCTAXCAT_ID": tax_details.TAXCATEGORY_ID,"ACCTAXCAT_DESCRIPTION": tax_details.TAXCATEGORY_DESCRIPTION, "ACCTAXCLA_ID": tax_details.TAXCLASSIFICATION_ID, "ACCTAXCLA_DESCRIPTION": tax_details.TAXCLASSIFICATION_DESCRIPTION})
						quote_salesorg_table_info.AddRow(salesorg_data)
						#Log.Info('salesorg_data---443--'+str(salesorg_data))
						Log.Info('contract_quote_data---443--'+str(contract_quote_data))                        
						Sql.Upsert(quote_salesorg_table_info)
						##Commented the condition to update the pricing procedure for both spare and tool based quote
						#if 'SPARE' in str(contract_quote_data.get('QUOTE_TYPE')):
						# Get Pricing Procedure
						GetPricingProcedure = Sql.GetFirst("SELECT DISTINCT SASAPP.PRICINGPROCEDURE_ID, SASAPP.PRICINGPROCEDURE_NAME, SASAPP.PRICINGPROCEDURE_RECORD_ID, SASAPP.DOCUMENT_PRICING_PROCEDURE,SASAPP.CUSTOMER_PRICING_PROCEDURE FROM SASAPP (NOLOCK) JOIN SASAAC (NOLOCK) ON SASAPP.SALESORG_ID = SASAAC.SALESORG_ID AND SASAPP.DIVISION_ID = SASAAC.DIVISION_ID AND SASAPP.DISTRIBUTIONCHANNEL_ID = SASAAC.DISTRIBUTIONCHANNEL_ID JOIN SAQTRV (NOLOCK) ON SAQTRV.DIVISION_ID = SASAPP.DIVISION_ID AND SAQTRV.DISTRIBUTIONCHANNEL_ID = SASAPP.DISTRIBUTIONCHANNEL_ID AND SAQTRV.SALESORG_ID = SASAPP.SALESORG_ID WHERE SASAPP.DOCUMENT_PRICING_PROCEDURE = 'A' AND SAQTRV.QUOTE_ID = '{}' AND SAQTRV.QTEREV_RECORD_ID = '{}'".format(quote_id,quote_revision_id))
						if GetPricingProcedure:
							CustPricing = GetPricingProcedure.CUSTOMER_PRICING_PROCEDURE
						else:
							CustPricing = ""
						#Log.Info(GetPricingProcedure)
						if GetPricingProcedure is not None:
							# UpdateSAQTSO = """UPDATE SAQTSO SET SAQTSO.PRICINGPROCEDURE_ID = '{pricingprocedure_id}', SAQTSO.PRICINGPROCEDURE_NAME = '{prcname}',SAQTSO.PRICINGPROCEDURE_RECORD_ID = '{prcrec}',SAQTSO.CUSTOMER_PRICING_PROCEDURE = '{customer_pricing_procedure}', SAQTSO.DOCUMENT_PRICING_PROCEDURE = '{docpricingprocedure}' WHERE SAQTSO.QUOTE_ID = '{quote_id}' AND SAQTSO.QTEREV_RECORD_ID = '{quote_revision_id}'""".format(pricingprocedure_id=GetPricingProcedure.PRICINGPROCEDURE_ID,
							# prcname=GetPricingProcedure.PRICINGPROCEDURE_NAME,
							# prcrec=GetPricingProcedure.PRICINGPROCEDURE_RECORD_ID,
							# customer_pricing_procedure=GetPricingProcedure.CUSTOMER_PRICING_PROCEDURE,					
							# docpricingprocedure=GetPricingProcedure.DOCUMENT_PRICING_PROCEDURE,
							# quote_id=quote_id,quote_revision_id=quote_revision_id)
							UpdateSAQTRV = """UPDATE SAQTRV SET SAQTRV.PRICINGPROCEDURE_ID = '{pricingprocedure_id}', SAQTRV.PRICINGPROCEDURE_NAME = '{prcname}',SAQTRV.PRICINGPROCEDURE_RECORD_ID = '{prcrec}', SAQTRV.DOCUMENT_PRICING_PROCEDURE = '{docpricingprocedure}' WHERE SAQTRV.QUOTE_ID = '{quote_id}' AND SAQTRV.QTEREV_RECORD_ID = '{quote_revision_id}'""".format(pricingprocedure_id=GetPricingProcedure.PRICINGPROCEDURE_ID,
							prcname=GetPricingProcedure.PRICINGPROCEDURE_NAME,
							prcrec=GetPricingProcedure.PRICINGPROCEDURE_RECORD_ID,
							customer_pricing_procedure=GetPricingProcedure.CUSTOMER_PRICING_PROCEDURE,					
							docpricingprocedure=GetPricingProcedure.DOCUMENT_PRICING_PROCEDURE,
							quote_id=quote_id,quote_revision_id=quote_revision_id)

							# UpdateSAQTRV = """UPDATE SAQTRV SET SAQTRV.PRICINGPROCEDURE_ID = '{pricingprocedure_id}', SAQTRV.PRICINGPROCEDURE_NAME = '{prcname}',SAQTRV.PRICINGPROCEDURE_RECORD_ID = '{prcrec}',SAQTRV.CUSTOMER_PRICING_PROCEDURE = '{customer_pricing_procedure}', SAQTRV.DOCUMENT_PRICING_PROCEDURE = '{docpricingprocedure}' WHERE SAQTRV.QUOTE_ID = '{quote_id}' AND SAQTRV.QTEREV_RECORD_ID = '{quote_revision_id}'""".format(pricingprocedure_id=GetPricingProcedure.PRICINGPROCEDURE_ID,
							# prcname=GetPricingProcedure.PRICINGPROCEDURE_NAME,
							# prcrec=GetPricingProcedure.PRICINGPROCEDURE_RECORD_ID,
							# customer_pricing_procedure=GetPricingProcedure.CUSTOMER_PRICING_PROCEDURE,					
							# docpricingprocedure=GetPricingProcedure.DOCUMENT_PRICING_PROCEDURE,
							# quote_id=quote_id,quote_revision_id=quote_revision_id)

							#Log.Info(UpdateSAQTRV)
							Sql.RunQuery(UpdateSAQTRV)
					
					
					if custom_fields_detail.get("STPAccountID"):
						account_obj = Sql.GetFirst("SELECT ACCOUNT_RECORD_ID, ACCOUNT_TYPE FROM SAACNT(NOLOCK) WHERE ACCOUNT_ID LIKE '%{}'".format(custom_fields_detail.get("STPAccountID")))
						getSales = Sql.GetFirst("SELECT CpqTableEntryId FROM SASOAC (NOLOCK) WHERE SALESORG_ID = '{}' AND ACCOUNT_ID = '{}'".format(custom_fields_detail.get('SalesOrgID'),custom_fields_detail.get('STPAccountID')))
						
						if not account_obj:
							getState = Sql.GetFirst("SELECT STATE_RECORD_ID FROM SACYST WHERE STATE = '{}'".format(custom_fields_detail.get("PayerState")))
							NewAccountRecordId = str(Guid.NewGuid()).upper()
							Sql.RunQuery("""INSERT INTO SAACNT (ACCOUNT_RECORD_ID,ACCOUNT_ID,ACCOUNT_NAME,ACCOUNT_TYPE,ACTIVE,ADDRESS_1,CITY,COUNTRY,COUNTRY_RECORD_ID,PHONE,POSTAL_CODE,REGION,REGION_RECORD_ID,STATE,STATE_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED)VALUES('{AccountRecordId}','{AccountId}','{AccountName}','{Type}',1,'{Address}','{City}','{Country}','{CountryRecordId}','{Phone}','{PostalCode}','{Region}','{RegionRecordId}','{State}','{StateRecordId}','{UserName}',GETDATE())
							""".format(AccountRecordId=NewAccountRecordId,AccountId=custom_fields_detail.get("STPAccountID"),AccountName=custom_fields_detail.get("STPAccountName"),Type=custom_fields_detail.get("STPAccountType"),Address=custom_fields_detail.get("PayerAddress1"),City=custom_fields_detail.get("PayerCity"),Country=custom_fields_detail.get("PayerCountry"),CountryRecordId=salesorg_country.COUNTRY_RECORD_ID,Phone=custom_fields_detail.get("PayerPhone"),PostalCode=custom_fields_detail.get("PayerPostalCode"),Region='',RegionRecordId='',State=custom_fields_detail.get("PayerState"),StateRecordId=getState.STATE_RECORD_ID,UserName=User.UserName))
							account_obj = Sql.GetFirst("SELECT ACCOUNT_RECORD_ID, ACCOUNT_TYPE FROM SAACNT(NOLOCK) WHERE ACCOUNT_ID LIKE '%{}'".format(custom_fields_detail.get("STPAccountID")))
						getAcc = Sql.GetFirst("SELECT ACCOUNT_RECORD_ID FROM SAACNT WHERE ACCOUNT_ID = '{}'".format(custom_fields_detail.get("STPAccountID")))
						
						getDistr = Sql.GetFirst("SELECT CpqTableEntryId FROM SASOAC WHERE ACCOUNT_ID = '{}' AND SALESORG_ID = '{}' AND DISTRIBUTIONCHANNEL_ID = '{}'".format(custom_fields_detail.get("STPAccountID"),custom_fields_detail.get("SalesOrgID"),distribution_obj.DISTRIBUTIONCHANNEL_ID))

						getDiv = Sql.GetFirst("SELECT CpqTableEntryId FROM SASAAC WHERE ACCOUNT_ID = '{}' AND SALESORG_ID = '{}' AND DIVISION_ID = '{}'".format(custom_fields_detail.get("STPAccountID"),custom_fields_detail.get("SalesOrgID"),division_obj.DIVISION_ID))

						if not getSales:
							NewSalesAccountRecordId = str(Guid.NewGuid()).upper()
							Sql.RunQuery("""INSERT INTO SASOAC (SALESORG_ACCOUNTS_RECORD_ID,ACCOUNT_RECORD_ID,ACCOUNT_ID,ACCOUNT_NAME,DISTRIBUTIONCHANNEL_RECORD_ID,DISTRIBUTIONCHANNEL_ID,SALESORG_RECORD_ID,SALESORG_ID,SALESORG_NAME)VALUES('{RecordId}','{AccountRecordId}','{AccountId}','{AccountName}','{DistRecordId}','{DistId}','{SalesRecordId}','{SalesOrgId}','{SalesOrgName}')
							""".format(RecordId=NewSalesAccountRecordId,AccountRecordId=getAcc.ACCOUNT_RECORD_ID,AccountId=custom_fields_detail.get("STPAccountID"),AccountName=custom_fields_detail.get("STPAccountName"),DistRecordId=distribution_obj.DISTRIBUTION_CHANNEL_RECORD_ID,DistId=distribution_obj.DISTRIBUTIONCHANNEL_ID,SalesRecordId=salesorg_obj.SALES_ORG_RECORD_ID,SalesOrgId=custom_fields_detail.get("SalesOrgID"),SalesOrgName=salesorg_obj.SALESORG_NAME))

							if not getDiv or not getDistr:
								if custom_fields_detail.get("Incoterms"):
									incid = ""
									incdesc = ""
									increc = ""
									getInc = Sql.GetFirst("SELECT INCOTERM_ID,DESCRIPTION,INCOTERM_RECORD_ID FROM SAICTM WHERE INCOTERM_ID = '{}'".format(custom_fields_detail.get("Incoterms")))
									if getInc:
										incid = getInc.INCOTERM_ID
										incdesc = getInc.DESCRIPTION
										increc = getInc.INCOTERM_RECORD_ID
								else:
									incid = ""
									incdesc = ""
									increc = ""
								

								NewSalesAreaAccountRecordId = str(Guid.NewGuid()).upper()
								insert = Sql.RunQuery("""INSERT INTO SASAAC (SALES_AREA_ACCOUNT_RECORD_ID,ACCOUNT_RECORD_ID,ACCOUNT_ID,ACCOUNT_NAME,DISTRIBUTIONCHANNEL_RECORD_ID,DISTRIBUTIONCHANNEL_ID,SALESORG_RECORD_ID,SALESORG_ID,SALESORG_NAME, DIVISION_ID,DIVISION_RECORD_ID,EXCHANGE_RATE_TYPE,CUSTOMER_PRICING_PROCEDURE,INCOTERM_ID,INCOTERM_DESCRIPTION,INCOTERM_RECORD_ID,PAYMENTTERM_ID,PAYMENTTERM_DESCRIPTION,PAYMENTTERM_RECORD_ID)VALUES('{RecordId}','{AccountRecordId}','{AccountId}','{AccountName}','{DistRecordId}','{DistId}','{SalesRecordId}','{SalesOrgId}','{SalesOrgName}','{DivisionId}','{DivisionRecordId}','{Exch}','{CustPricing}','{incid}','{incdesc}','{increc}','{payid}','{paydesc}','{payrec}')
								""".format(RecordId=NewSalesAreaAccountRecordId,AccountRecordId=getAcc.ACCOUNT_RECORD_ID,AccountId=custom_fields_detail.get("STPAccountID"),AccountName=custom_fields_detail.get("STPAccountName"),DistRecordId=distribution_obj.DISTRIBUTION_CHANNEL_RECORD_ID,DistId=distribution_obj.DISTRIBUTIONCHANNEL_ID,SalesRecordId=salesorg_obj.SALES_ORG_RECORD_ID,SalesOrgId=custom_fields_detail.get("SalesOrgID"),SalesOrgName=salesorg_obj.SALESORG_NAME,DivisionId=division_obj.DIVISION_ID,DivisionRecordId=division_obj.DIVISION_RECORD_ID,Exch=custom_fields_detail.get("ExchangeRateType"),CustPricing=CustPricing,incid=incid,incdesc=incdesc,increc=increc,payid=payid,paydesc=paydesc,payrec=payrec))
								#Log.Info("@@@728------>"+str(insert))
								getCtry = Sql.GetFirst("SELECT COUNTRY_RECORD_ID FROM SACTRY WHERE COUNTRY = '{}'".format(custom_fields_detail.get("PayerCountry")))
								NewRecordId = str(Guid.NewGuid()).upper()
								Sql.RunQuery("""INSERT INTO SAASCT (ACCOUNT_SALES_AREA_COUNTRY_TAX_RECORD_ID,ACCOUNT_RECORD_ID,ACCOUNT_ID,ACCOUNT_NAME,DISTRIBUTIONCHANNEL_RECORD_ID,DISTRIBUTIONCHANNEL_ID,SALESORG_RECORD_ID,SALESORG_ID,SALESORG_NAME, DIVISION_ID,DIVISION_RECORD_ID,COUNTRY,COUNTRY_NAME,COUNTRY_RECORD_ID)VALUES('{RecordId}','{AccountRecordId}','{AccountId}','{AccountName}','{DistRecordId}','{DistId}','{SalesRecordId}','{SalesOrgId}','{SalesOrgName}','{DivisionId}','{DivisionRecordId}','{Country}','{CountryName}','{CountryRecordId}')
								""".format(RecordId=NewRecordId,AccountRecordId=getAcc.ACCOUNT_RECORD_ID,AccountId=custom_fields_detail.get("STPAccountID"),AccountName=custom_fields_detail.get("STPAccountName"),DistRecordId=distribution_obj.DISTRIBUTION_CHANNEL_RECORD_ID,DistId=distribution_obj.DISTRIBUTIONCHANNEL_ID,SalesRecordId=salesorg_obj.SALES_ORG_RECORD_ID,SalesOrgId=custom_fields_detail.get("SalesOrgID"),SalesOrgName=salesorg_obj.SALESORG_NAME,DivisionId=division_obj.DIVISION_ID,DivisionRecordId=division_obj.DIVISION_RECORD_ID,Country=salesorg_country.COUNTRY,CountryName=salesorg_country_name.COUNTRY_NAME,CountryRecordId=getCtry.COUNTRY_RECORD_ID))
						
						if account_obj:							
							contract_quote_data.update(
								{
									"ACCOUNT_RECORD_ID": account_obj.ACCOUNT_RECORD_ID,
									"ACCOUNT_ID": custom_fields_detail.get("STPAccountID"),
									"ACCOUNT_NAME": custom_fields_detail.get("STPAccountName"),
								}
							)

							if custom_fields_detail.get("OpportunityId"):
								opportunity_obj = Sql.GetFirst(
									"""SELECT OPPORTUNITY_RECORD_ID, OPPORTUNITY_ID, OPPORTUNITY_STAGE, OPPORTUNITY_NAME FROM SAOPPR(NOLOCK) 
															WHERE OPPORTUNITY_ID = '{}' 
															AND ACCOUNT_RECORD_ID = '{}'""".format(
										custom_fields_detail.get("OpportunityId"), contract_quote_data.get("ACCOUNT_RECORD_ID")
									)
								)
								Opportunitystagedict = {}
								if custom_fields_detail.get("OpportunityStage"):
									Opportunitystagedict = {"Z0001":"NEW","Z0002":"DEFINE OPPORTUNITY","Z0003":"CONFIGURE QUOTE","Z0004":"MANUAL PRICING REQUESTED","Z0005":"FINANCE/BD/NSDR/APPROVAL","Z0006":"FINANCE/BD/NSDR APPROVED","Z0007":"QUOTE GENERATED","Z0008":"QUOTE ACCEPTED – CUSTOMER","Z0009":"BOOKING SUBMITTED","Z0010":"WON","Z0011":"STOPPED","Z0012":"LOST","Z0013":"POES PRICING REQUESTED","Z0014":"POES PRICING GENERATED","Z0017":"PRICING DETERMINED"}
								if not opportunity_obj:
									master_opportunity_table_info = Sql.GetTable("SAOPPR")
									master_opportunity_data = {
										"OPPORTUNITY_RECORD_ID": str(Guid.NewGuid()).upper(),
										"ACCOUNT_ID": custom_fields_detail.get("STPAccountID"),
										"ACCOUNT_NAME": custom_fields_detail.get("STPAccountName"),
										"ACCOUNT_RECORD_ID": account_obj.ACCOUNT_RECORD_ID,
										"DOCUMENT_TYPE": contract_quote_data.get("DOCUMENT_TYPE"),
										"CPQTABLEENTRYDATEADDED": datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"),
										"OPPORTUNITY_ID": custom_fields_detail.get("OpportunityId"),
										"OPPORTUNITY_NAME": self.quote.OpportunityName,
										"OPPORTUNITY_TYPE": custom_fields_detail.get("OpportunityType"),
										"SALESORG_ID": salesorg_data.get("SALESORG_ID"),
										"SALESORG_NAME": salesorg_data.get("SALESORG_NAME"),
										"SALESORG_RECORD_ID": salesorg_data.get("SALESORG_RECORD_ID"),
										"SALE_TYPE": "NEW",
										"OPPORTUNITY_STAGE": Opportunitystagedict.get(custom_fields_detail.get("OpportunityStage")),
										"ACCOUNT_TYPE": "Sold to Party",
										"OPPORTUNITY_OWNER_ID": custom_fields_detail.get("OpportunityOwner"),
									}
									#Log.Info("master_opportunity_data ===>" + str(master_opportunity_data))
									master_opportunity_table_info.AddRow(master_opportunity_data)
									Sql.Upsert(master_opportunity_table_info)
									opportunity_obj = Sql.GetFirst(
										"""SELECT OPPORTUNITY_RECORD_ID, OPPORTUNITY_ID, OPPORTUNITY_NAME, OPPORTUNITY_STAGE FROM SAOPPR(NOLOCK) 
															WHERE OPPORTUNITY_RECORD_ID = '{}'""".format(
											master_opportunity_data.get("OPPORTUNITY_RECORD_ID")
										)
									)
								#Log.Info("opportunity_obj ===>" + str(opportunity_obj))
								opportunity_quote_data = {
									"OPPORTUNITY_QUOTE_RECORD_ID": str(Guid.NewGuid()).upper(),
									"OPPORTUNITY_ID": opportunity_obj.OPPORTUNITY_ID,
									"OPPORTUNITY_NAME": opportunity_obj.OPPORTUNITY_NAME,
									"OPPORTUNITY_RECORD_ID": opportunity_obj.OPPORTUNITY_RECORD_ID,
									"QUOTE_ID": contract_quote_data.get("QUOTE_ID"),
									"CPQTABLEENTRYDATEADDED": datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"),
									"QUOTE_RECORD_ID": contract_quote_data.get("MASTER_TABLE_QUOTE_RECORD_ID"),
									"ACCOUNT_ID": custom_fields_detail.get("STPAccountID"),
									"ACCOUNT_NAME": custom_fields_detail.get("STPAccountName"),
									"ACCOUNT_TYPE": account_obj.ACCOUNT_TYPE,								
									
								}

								quote_opportunity_table_info.AddRow(opportunity_quote_data)
					# A055S000P01-6618 - Starts
					if custom_fields_detail.get("PrimaryContactName"):
						primary_contact_update = {
							"QUOTE_INVOLVED_PARTY_RECORD_ID": str(Guid.NewGuid()).upper(),
							"ADDRESS": "",
							"EMAIL": "",
							"IS_MAIN": "",
							"QUOTE_ID": contract_quote_data.get("QUOTE_ID"),
							"QUOTE_NAME": custom_fields_detail.get("STPAccountName"),
							"QUOTE_RECORD_ID": contract_quote_data.get("MASTER_TABLE_QUOTE_RECORD_ID"),
							"PARTY_ID": "",
							"PARTY_NAME": custom_fields_detail.get("PrimaryContactName"),
							"PARTY_ROLE": "PRIMARY CONTACT",
							"PHONE": "",
							"QTEREV_RECORD_ID":quote_revision_id,
							"QTEREV_ID":quote_rev_id
						}
						quote_involved_party_table_info.AddRow(primary_contact_update)
					# A055S000P01-6618 - Ends
					if self.quote.BillToCustomer:
						bill_to_customer = self.quote.BillToCustomer
						billtocustomer_quote_data = {
							"QUOTE_INVOLVED_PARTY_RECORD_ID": str(Guid.NewGuid()).upper(),
							"ADDRESS": bill_to_customer.Address1 +', ' + bill_to_customer.City  +', ' + bill_to_customer.StateAbbreviation  +', ' + bill_to_customer.CountryAbbreviation +', ' + bill_to_customer.ZipCode,
							"EMAIL": bill_to_customer.Email,
							"IS_MAIN": bill_to_customer.Active,
							"QUOTE_ID": contract_quote_data.get("QUOTE_ID"),
							"QUOTE_NAME": custom_fields_detail.get("STPAccountName"),
							"QUOTE_RECORD_ID": contract_quote_data.get("MASTER_TABLE_QUOTE_RECORD_ID"),
							"PARTY_ID": bill_to_customer.CustomerCode,
							"PARTY_NAME": bill_to_customer.FirstName,
							"PARTY_ROLE": "BILL TO",
							"PHONE": bill_to_customer.BusinessPhone,
							"QTEREV_RECORD_ID":quote_revision_id,
							"QTEREV_ID":quote_rev_id
						}
						quote_involved_party_table_info.AddRow(billtocustomer_quote_data)
					#Log.Info("QUOTE_ID_CHECK_J "+str(contract_quote_data.get("QUOTE_ID")))
					#Log.Info("SALE_TYPE_CHECK_J "+str(contract_quote_data.get("SALE_TYPE")))
					# if contract_quote_data.get("SALE_TYPE") == "TOOL RELOCATION":
					#     sending_account_quote_data = {
					#         "QUOTE_INVOLVED_PARTY_RECORD_ID": str(Guid.NewGuid()).upper(),
					#         "ADDRESS": bill_to_customer.Address1 +', ' + bill_to_customer.City  +', ' + bill_to_customer.StateAbbreviation  +', ' + bill_to_customer.CountryAbbreviation +', ' + bill_to_customer.ZipCode,
					#         "EMAIL": bill_to_customer.Email,
					#         "IS_MAIN": bill_to_customer.Active,
					#         "QUOTE_ID": contract_quote_data.get("QUOTE_ID"),
					#         "QUOTE_NAME": custom_fields_detail.get("STPAccountName"),
					#         "QUOTE_RECORD_ID": contract_quote_data.get("MASTER_TABLE_QUOTE_RECORD_ID"),
					#         "PARTY_ID": bill_to_customer.CustomerCode,
					#         "PARTY_NAME": bill_to_customer.FirstName,
					#         "PARTY_ROLE": "SENDING ACCOUNT",
					#         "PHONE": bill_to_customer.BusinessPhone,
					#     }
					#     quote_involved_party_table_info.AddRow(sending_account_quote_data)
					if self.quote.ShipToCustomer:
						ship_to_customer = self.quote.ShipToCustomer
						shiptocustomer_quote_data = {
							"QUOTE_INVOLVED_PARTY_RECORD_ID": str(Guid.NewGuid()).upper(),
							"ADDRESS": ship_to_customer.Address1 +', ' + ship_to_customer.City  +', ' + ship_to_customer.StateAbbreviation  +', ' + ship_to_customer.CountryAbbreviation +', ' + ship_to_customer.ZipCode,
							"EMAIL": ship_to_customer.Email,
							"IS_MAIN": ship_to_customer.Active,
							"QUOTE_ID": contract_quote_data.get("QUOTE_ID"),
							"QUOTE_NAME": custom_fields_detail.get("STPAccountName"),
							"QUOTE_RECORD_ID": contract_quote_data.get("MASTER_TABLE_QUOTE_RECORD_ID"),
							"PARTY_ID": ship_to_customer.CustomerCode,
							"PARTY_NAME": ship_to_customer.FirstName,
							"PARTY_ROLE": "SHIP TO",
							"PHONE": ship_to_customer.BusinessPhone,
							"QTEREV_RECORD_ID":quote_revision_id,
							"QTEREV_ID":quote_rev_id
						}
						quote_involved_party_table_info.AddRow(shiptocustomer_quote_data)
					if custom_fields_detail.get("PayerID"):
						PayerDetails = {
							"QUOTE_INVOLVED_PARTY_RECORD_ID": str(Guid.NewGuid()).upper(),
							"ADDRESS": custom_fields_detail.get("PayerAddress1"),
							"EMAIL": custom_fields_detail.get("PayerEmail"),
							"IS_MAIN": "1",
							"QUOTE_ID": contract_quote_data.get("QUOTE_ID"),
							"QUOTE_NAME": custom_fields_detail.get("STPAccountName"),
							"QUOTE_RECORD_ID": contract_quote_data.get("MASTER_TABLE_QUOTE_RECORD_ID"),
							"PARTY_ID": custom_fields_detail.get("PayerID"),
							"PARTY_NAME": custom_fields_detail.get("PayerName"),
							"PARTY_ROLE": "PAYER",
							"PHONE": custom_fields_detail.get("PayerPhone"),
							"QTEREV_RECORD_ID":quote_revision_id,
							"QTEREV_ID":quote_rev_id
						}
						quote_involved_party_table_info.AddRow(PayerDetails)
					if custom_fields_detail.get("SellerID"):
						SellerDetails = {
							"QUOTE_INVOLVED_PARTY_RECORD_ID": str(Guid.NewGuid()).upper(),
							"ADDRESS": custom_fields_detail.get("SellerAddress"),
							"EMAIL": custom_fields_detail.get("SellerEmail"),
							"IS_MAIN": "1",
							"QUOTE_ID": contract_quote_data.get("QUOTE_ID"),
							"QUOTE_NAME": custom_fields_detail.get("STPAccountName"),
							"QUOTE_RECORD_ID": contract_quote_data.get("MASTER_TABLE_QUOTE_RECORD_ID"),
							"PARTY_ID": custom_fields_detail.get("SellerID"),
							"PARTY_NAME": custom_fields_detail.get("SellerName"),
							"PARTY_ROLE": "SELLER",
							"PHONE": custom_fields_detail.get("SellerPhone"),
							"QTEREV_RECORD_ID":quote_revision_id,
							"QTEREV_ID":quote_rev_id
						}
						quote_involved_party_table_info.AddRow(SellerDetails)
					if custom_fields_detail.get("SalesUnitID"):
						SalesUnitDetails = {
							"QUOTE_INVOLVED_PARTY_RECORD_ID": str(Guid.NewGuid()).upper(),
							"ADDRESS": custom_fields_detail.get("SalesUnitAddress"),
							"EMAIL": custom_fields_detail.get("SalesUnitEmail"),
							"IS_MAIN": "1",
							"QUOTE_ID": contract_quote_data.get("QUOTE_ID"),
							"QUOTE_NAME": custom_fields_detail.get("STPAccountName"),
							"QUOTE_RECORD_ID": contract_quote_data.get("MASTER_TABLE_QUOTE_RECORD_ID"),
							"PARTY_ID": custom_fields_detail.get("SalesUnitID"),
							"PARTY_NAME": custom_fields_detail.get("SalesUnitName"),
							"PARTY_ROLE": "SALES UNIT",
							"PHONE": custom_fields_detail.get("SalesUnitPhone"),
							"QTEREV_RECORD_ID":quote_revision_id,
							"QTEREV_ID":quote_rev_id
						}
						quote_involved_party_table_info.AddRow(SalesUnitDetails)
					if custom_fields_detail.get("SalesEmployeeID"):
						SalesEmployeeDetails = {
							"QUOTE_INVOLVED_PARTY_RECORD_ID": str(Guid.NewGuid()).upper(),
							"ADDRESS": custom_fields_detail.get("SalesEmployeeAddress"),
							"EMAIL": custom_fields_detail.get("SalesEmployeeEmail"),
							"IS_MAIN": "1",
							"QUOTE_ID": contract_quote_data.get("QUOTE_ID"),
							"QUOTE_NAME": custom_fields_detail.get("STPAccountName"),
							"QUOTE_RECORD_ID": contract_quote_data.get("MASTER_TABLE_QUOTE_RECORD_ID"),
							"PARTY_ID": custom_fields_detail.get("SalesEmployeeID"),
							"PARTY_NAME": custom_fields_detail.get("SalesEmployeeName"),
							"PARTY_ROLE": "SALES EMPLOYEE",
							"PHONE": custom_fields_detail.get("SalesEmployeePhone"),
							"QTEREV_RECORD_ID":quote_revision_id,
							"QTEREV_ID":quote_rev_id
						}
						quote_involved_party_table_info.AddRow(SalesEmployeeDetails)
					if custom_fields_detail.get("EmployeeResponsibleID"):
						EmployeeResponsibleDetails = {
							"QUOTE_INVOLVED_PARTY_RECORD_ID": str(Guid.NewGuid()).upper(),
							"ADDRESS": custom_fields_detail.get("EmployeeResponsibleAddress"),
							"EMAIL": custom_fields_detail.get("EmployeeResponsibleEmail"),
							"IS_MAIN": "1",
							"QUOTE_ID": contract_quote_data.get("QUOTE_ID"),
							"QUOTE_NAME": custom_fields_detail.get("STPAccountName"),
							"QUOTE_RECORD_ID": contract_quote_data.get("MASTER_TABLE_QUOTE_RECORD_ID"),
							"PARTY_ID": custom_fields_detail.get("EmployeeResponsibleID"),
							"PARTY_NAME": custom_fields_detail.get("EmployeeResponsibleName"),
							"PARTY_ROLE": "EMPLOYEE RESPONSIBLE",
							"PHONE": custom_fields_detail.get("EmployeeResponsiblePhone"),
							"QTEREV_RECORD_ID":quote_revision_id,
							"QTEREV_ID":quote_rev_id
						}
						quote_involved_party_table_info.AddRow(EmployeeResponsibleDetails)
					if custom_fields_detail.get("SourceAccountID"):
						SourceAccountDetails = {
							"QUOTE_INVOLVED_PARTY_RECORD_ID": str(Guid.NewGuid()).upper(),
							"ADDRESS": custom_fields_detail.get("SourceAccountAddress"),
							"EMAIL": custom_fields_detail.get("SourceAccountEmail"),
							"IS_MAIN": "1",
							"QUOTE_ID": contract_quote_data.get("QUOTE_ID"),
							"QUOTE_NAME": custom_fields_detail.get("STPAccountName"),
							"QUOTE_RECORD_ID": contract_quote_data.get("MASTER_TABLE_QUOTE_RECORD_ID"),
							"PARTY_ID": custom_fields_detail.get("SourceAccountID"),
							"PARTY_NAME": custom_fields_detail.get("SourceAccountName"),
							"PARTY_ROLE": "SOURCE ACCOUNT",
							"PHONE": custom_fields_detail.get("SourceAccountPhone"),
							"QTEREV_RECORD_ID":quote_revision_id,
							"QTEREV_ID":quote_rev_id
						}
						quote_involved_party_table_info.AddRow(SourceAccountDetails)		
					if custom_fields_detail.get("ContractManagerName"):
						EmployeeResponsibleDetails = {
							"QUOTE_INVOLVED_PARTY_RECORD_ID": str(Guid.NewGuid()).upper(),
							"ADDRESS": custom_fields_detail.get("ContractManagerAddress"),
							"EMAIL": custom_fields_detail.get("ContractManagerEmail"),
							"IS_MAIN": "1",
							"QUOTE_ID": contract_quote_data.get("QUOTE_ID"),
							"QUOTE_NAME": custom_fields_detail.get("STPAccountName"),
							"QUOTE_RECORD_ID": contract_quote_data.get("MASTER_TABLE_QUOTE_RECORD_ID"),
							"PARTY_ID": custom_fields_detail.get("ContractManagerID"),
							"PARTY_NAME": custom_fields_detail.get("ContractManagerName"),
							"PARTY_ROLE": "CONTRACT MANAGER",
							"PHONE": custom_fields_detail.get("ContractManagerPhone"),
							"QTEREV_RECORD_ID":quote_revision_id,
							"QTEREV_ID":quote_rev_id
						}
						quote_involved_party_table_info.AddRow(EmployeeResponsibleDetails) 
					#Log.Info("FAB =====>>>>>> " + str(custom_fields_detail.get("FabLocationID")))                      
					""" if custom_fields_detail.get("FabLocationID"):
						fab_locations = custom_fields_detail.get("FabLocationID").split(",")
						fab_locations = [fab_location for fab_location in fab_locations if fab_location]
						for fab_location in fab_locations:
							Log.Info("fabid ==> " + str(fab_location))
							master_tab_obj = Sql.GetFirst(
								"SELECT * FROM MAFBLC (NOLOCK) WHERE FAB_LOCATION_ID = '{}'".format(fab_location)
							)
							if master_tab_obj:
								fab_quote_data = {
									"QUOTE_FABLOCATION_RECORD_ID": str(Guid.NewGuid()).upper(),
									"FABLOCATION_ID": master_tab_obj.FAB_LOCATION_ID,
									"FABLOCATION_NAME": master_tab_obj.FAB_LOCATION_NAME,
									"FABLOCATION_RECORD_ID": master_tab_obj.FAB_LOCATION_RECORD_ID,
									"QUOTE_ID": contract_quote_data.get("QUOTE_ID"),
									"QUOTE_RECORD_ID": contract_quote_data.get("MASTER_TABLE_QUOTE_RECORD_ID"),
									"QUOTE_NAME": custom_fields_detail.get("STPAccountName"),
									"COUNTRY": master_tab_obj.COUNTRY,
									"COUNTRY_RECORD_ID": master_tab_obj.COUNTRY_RECORD_ID,
									"MNT_PLANT_ID": master_tab_obj.MNT_PLANT_ID,
									"MNT_PLANT_NAME": master_tab_obj.MNT_PLANT_NAME,
									"MNT_PLANT_RECORD_ID": master_tab_obj.MNT_PLANT_RECORD_ID,
									"SALESORG_ID": master_tab_obj.SALESORG_ID,
									"SALESORG_NAME": master_tab_obj.SALESORG_NAME,
									"SALESORG_RECORD_ID": master_tab_obj.SALESORG_RECORD_ID,
								}
								Log.Info("fab_quote_data===> " + str(fab_quote_data))
								quote_fab_table_info.AddRow(fab_quote_data) """
					Log.Info("contract_quote_data===> " + str(contract_quote_data))
					Log.Info("quote_involved_party_table_info===> " + str(quote_involved_party_table_info))
					quote_table_info.AddRow(contract_quote_data)
					Sql.Upsert(quote_table_info)
					Sql.Upsert(quote_opportunity_table_info)
					Sql.Upsert(quote_involved_party_table_info)
					#Sql.Upsert(quote_fab_table_info)

					cart_obj = Sql.GetFirst("SELECT CART_ID, USERID FROM CART WHERE ExternalId = '{}'".format(self.quote.CompositeNumber))
					if cart_obj:
						Sql.RunQuery("""INSERT INTO QT__QTQTMT (QUOTE_ID, QUOTE_NAME, MASTER_TABLE_QUOTE_RECORD_ID, ownerId, cartId) 
								VALUES 	(							
									'{QuoteId}',								
									'{QuoteName}',
									'{QuoteRecordId}',								
									{UserId},
									{CartId})""".format(
									CartId=cart_obj.CART_ID, UserId=cart_obj.USERID, 
									QuoteRecordId=contract_quote_data.get("MASTER_TABLE_QUOTE_RECORD_ID"),
									QuoteId=contract_quote_data.get("QUOTE_ID"),
									QuoteName=contract_quote_data.get("QUOTE_NAME")))
					
					# CALLING IFLOW C4C_TO_CPQ_TOOLS
					LOGIN_CREDENTIALS = SqlHelper.GetFirst("SELECT USER_NAME AS Username,Password,Domain FROM SYCONF where Domain='AMAT_TST'")
					if LOGIN_CREDENTIALS is not None:
						Login_Username = str(LOGIN_CREDENTIALS.Username)
						Login_Password = str(LOGIN_CREDENTIALS.Password)
						authorization = Login_Username + ":" + Login_Password
						binaryAuthorization = UTF8.GetBytes(authorization)
						authorization = Convert.ToBase64String(binaryAuthorization)
						authorization = "Basic " + authorization

						webclient = System.Net.WebClient()
						webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/json"
						webclient.Headers[System.Net.HttpRequestHeader.Authorization] = authorization

						LOGIN_CRE = SqlHelper.GetFirst("SELECT URL FROM SYCONF where EXTERNAL_TABLE_NAME  ='C4C_TO_CPQ_TOOLS'")
						
						QuoteId_info = contract_quote_data.get('C4C_QUOTE_ID')
						OpportunityId_info = custom_fields_detail.get("OpportunityId")
						
						Log.Info("11111 QuoteId_info----> "+str(QuoteId_info))
						Log.Info("2222 OpportunityId_info ---->"+str(OpportunityId_info))
						
						requestdata = '{\n  \"OpportunityId\": \"'+str(OpportunityId_info)+'\",\n  \"QuoteId\": \"'+str(QuoteId_info)+'\"\n}'
						Trace.Write("REQUEST DATA----> "+str(requestdata))
						
						response_SAQTMT = webclient.UploadString(str(LOGIN_CRE.URL), str(requestdata))
						
					payload_json_obj = Sql.GetFirst("SELECT INTEGRATION_PAYLOAD, CpqTableEntryId FROM SYINPL (NOLOCK) WHERE INTEGRATION_KEY = '{}' AND ISNULL(STATUS,'') = ''".format(contract_quote_data.get('C4C_QUOTE_ID')))
					if payload_json_obj:
						contract_quote_obj = None
						fab_location_ids, service_ids = [], []
						equipment_data = {}
						covered_object_data = {}
						payload_json = eval(payload_json_obj.INTEGRATION_PAYLOAD)
						payload_json = eval(payload_json.get('Param'))
						payload_json = payload_json.get('CPQ_Columns')
						Log.Info("payload_json----->"+str(payload_json))
						if payload_json.get('OPPORTUNITY_ID'):
							contract_quote_obj = Sql.GetFirst("SELECT SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID, SAQTMT.QUOTE_ID, SAQTMT.QUOTE_NAME, SAQTMT.ACCOUNT_RECORD_ID FROM SAQTMT (NOLOCK) WHERE SAQTMT.C4C_QUOTE_ID = '{}'".format(contract_quote_data.get('C4C_QUOTE_ID')))
							Log.Info("""SELECT SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID, SAQTMT.QUOTE_ID, SAQTMT.QUOTE_NAME, SAQTMT.ACCOUNT_RECORD_ID FROM SAQTMT (NOLOCK) WHERE SAQTMT.C4C_QUOTE_ID = '{}'""".format(contract_quote_data.get('C4C_QUOTE_ID')))
						if payload_json.get('FAB_LOCATION_IDS'):
							fab_location_ids = "','".join(list(set([str(int(fab_location)) for fab_location in payload_json.get('FAB_LOCATION_IDS').split(',') if fab_location])))		
						if payload_json.get('SERVICE_IDS'):	
							service_ids = "','".join(list(set(payload_json.get('SERVICE_IDS').split(','))))
							#Log.Info("SERVICE IDS-------->"+str(service_ids))
						if payload_json.get('SAQFEQ'):
							for equipment_json_data in payload_json.get('SAQFEQ'):       
								Log.Info(str(payload_json.get('SAQFEQ'))+" ======== equipment_json_data-------->"+str(equipment_json_data))                 
								if equipment_json_data.get('FAB_LOCATION_ID') in equipment_data:
									equipment_data[equipment_json_data.get('FAB_LOCATION_ID')].append(equipment_json_data.get('EQUIPMENT_IDS'))
								else:
									equipment_data[equipment_json_data.get('FAB_LOCATION_ID')] = [equipment_json_data.get('EQUIPMENT_IDS')]
								
								if equipment_json_data.get('SERVICE_OFFERING_ID') in covered_object_data:
									covered_object_data[equipment_json_data.get('SERVICE_OFFERING_ID')].append(equipment_json_data.get('EQUIPMENT_IDS'))
								else:
									covered_object_data[equipment_json_data.get('SERVICE_OFFERING_ID')] = [equipment_json_data.get('EQUIPMENT_IDS')] 
						##A055S000P01-8690 starts..
						if payload_json.get('SAEMPL'):
							employee = payload_json.get('SAEMPL')
							if type(employee) is dict:
								employee_obj = SqlHelper.GetFirst("select EMPLOYEE_ID from SAEMPL(nolock) where EMPLOYEE_ID = '{employee_id}'".format(employee_id = employee.get("EMPLOYEE_ID")))
								if employee_obj is None:
									country_obj = SqlHelper.GetFirst("select COUNTRY_RECORD_ID from SACTRY(nolock) where COUNTRY = '{country}'".format(country = employee.get("COUNTRY")))
									salesorg_obj = SqlHelper.GetFirst("select STATE_RECORD_ID from SASORG(nolock) where STATE = '{state}'".format(state = employee.get("STATE")))
									employee_dict = {}
									employee_dict["EMPLOYEE_RECORD_ID"] = str(Guid.NewGuid()).upper()
									employee_dict["ADDRESS_1"] = employee.get("ADDRESS1")
									employee_dict["ADDRESS_2"] = employee.get("ADDRESS2")
									employee_dict["CITY"] = employee.get("CITY")
									employee_dict["COUNTRY"] = employee.get("COUNTRY")
									employee_dict["COUNTRY_RECORD_ID"] = country_obj.COUNTRY_RECORD_ID  if country_obj else ""
									employee_dict["EMAIL"] = employee.get("EMAIL")
									employee_dict["EMPLOYEE_ID"] = employee.get("EMPLOYEE_ID")
									employee_dict["EMPLOYEE_NAME"] = employee.get("EMPLOYEE_NAME")
									employee_dict["EMPLOYEE_STATUS"] = employee.get("EMPLOYEE_STATUS")
									employee_dict["FIRST_NAME"] = employee.get("FIRST_NAME")
									employee_dict["LAST_NAME"] = employee.get("LAST_NAME")
									employee_dict["PHONE"] = employee.get("PHONE")
									employee_dict["POSTAL_CODE"] = employee.get("POSTAL_CODE")
									employee_dict["STATE"] = employee.get("STATE")
									employee_dict["STATE_RECORD_ID"] = salesorg_obj.STATE_RECORD_ID  if salesorg_obj else ""
									employee_dict["CRM_EMPLOYEE_ID"] = employee.get("CRM_EMPLOYEE_ID")
									employee_dict["CPQTABLEENTRYADDEDBY"] = User.UserName
									employee_dict["CpqTableEntryModifiedBy"] = User.Id
									employee_dict["ADDUSR_RECORD_ID"] = User.Id
									tableInfo = Sql.GetTable("SAEMPL")
									tablerow = employee_dict
									tableInfo.AddRow(tablerow)
									Sql.Upsert(tableInfo)
								self.salesteam_insert(employee,contract_quote_data,quote_rev_id,quote_revision_id)
							else:
								for employee in payload_json.get('SAEMPL'):
									employee_obj = SqlHelper.GetFirst("select EMPLOYEE_ID from SAEMPL(nolock) where EMPLOYEE_ID = '{employee_id}'".format(employee_id = employee.get("EMPLOYEE_ID")))
									if employee_obj is None:
										country_obj = SqlHelper.GetFirst("select COUNTRY_RECORD_ID from SACTRY(nolock) where COUNTRY = '{country}'".format(country = employee.get("COUNTRY")))
										salesorg_obj = SqlHelper.GetFirst("select STATE_RECORD_ID from SASORG(nolock) where STATE = '{state}'".format(state = employee.get("STATE")))
										employee_dict = {}
										employee_dict["EMPLOYEE_RECORD_ID"] = str(Guid.NewGuid()).upper()
										employee_dict["ADDRESS_1"] = employee.get("ADDRESS1")
										employee_dict["ADDRESS_2"] = employee.get("ADDRESS2")
										employee_dict["CITY"] = employee.get("CITY")
										employee_dict["COUNTRY"] = employee.get("COUNTRY")
										employee_dict["COUNTRY_RECORD_ID"] = country_obj.COUNTRY_RECORD_ID  if country_obj else ""
										employee_dict["EMAIL"] = employee.get("EMAIL")
										employee_dict["EMPLOYEE_ID"] = employee.get("EMPLOYEE_ID")
										employee_dict["EMPLOYEE_NAME"] = employee.get("EMPLOYEE_NAME")
										employee_dict["EMPLOYEE_STATUS"] = employee.get("EMPLOYEE_STATUS")
										employee_dict["FIRST_NAME"] = employee.get("FIRST_NAME")
										employee_dict["LAST_NAME"] = employee.get("LAST_NAME")
										employee_dict["PHONE"] = employee.get("PHONE")
										employee_dict["POSTAL_CODE"] = employee.get("POSTAL_CODE")
										employee_dict["STATE"] = employee.get("STATE")
										employee_dict["STATE_RECORD_ID"] = salesorg_obj.STATE_RECORD_ID  if salesorg_obj else ""
										employee_dict["CRM_EMPLOYEE_ID"] = employee.get("CRM_EMPLOYEE_ID")
										employee_dict["CPQTABLEENTRYADDEDBY"] = User.UserName
										employee_dict["CpqTableEntryModifiedBy"] = User.Id
										employee_dict["ADDUSR_RECORD_ID"] = User.Id
										tableInfo = Sql.GetTable("SAEMPL")
										tablerow = employee_dict
										tableInfo.AddRow(tablerow)
										Sql.Upsert(tableInfo)
									self.salesteam_insert(employee,contract_quote_data,quote_rev_id,quote_revision_id)
						##A055S000P01-8690 endss..
						if contract_quote_obj and payload_json.get('SalesType') and payload_json.get('OpportunityType'):
							SalesType = {"Z14":"NEW","Z15":"CONTRACT RENEWAL","Z16":"CONTRACT EXTENSION","Z17":"CONTRACT AMENDMENT","Z18":"CONVERSION","Z19":"TOOL RELOCATION"}
							OpportunityType = {"23":"PROSPECT FOR PRODUCT SALES","24":"PROSPECT FOR SERVICE","25":"PROSPECT FOR TRAINING","26":"PROSPECT FOR CONSULTING","Z27":"FPM/EXE","Z28":"TKM","Z29":"POES","Z30":"LOW","Z31":"AGS"}
							Contract_child = "UPDATE SAQTMT SET SALE_TYPE = '{SalesType}' WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{QuoteRecordId}' ".format(SalesType = SalesType.get(payload_json.get("SalesType")),QuoteRecordId = contract_quote_obj.MASTER_TABLE_QUOTE_RECORD_ID)
							Sql.RunQuery(Contract_child)
							if custom_fields_detail.get("OpportunityId"):
								Opportunity_obj = "UPDATE SAOPPR SET SALE_TYPE = '{SalesType}',OPPORTUNITY_TYPE = '{OpportunityType}' where OPPORTUNITY_ID = '{OpportunityId}'".format(SalesType = SalesType.get(payload_json.get("SalesType")), OpportunityType = OpportunityType.get(payload_json.get("OpportunityType")),OpportunityId = custom_fields_detail.get("OpportunityId"))
								Sql.RunQuery(Opportunity_obj)
						#Log.Info("fab_location_ids ===> "+str(fab_location_ids))
						#Log.Info("service_ids ===> "+str(service_ids)+"QUOTE ID----->"+str(contract_quote_data.get("QUOTE_ID")))	
						#Log.Info("CHECKING_TOOL_CONDTN_J "+str(contract_quote_obj)+" | "+str(payload_json.get('SalesType'))+" | "+str(payload_json.get('OpportunityType')))

						if  str(payload_json.get('SalesType')) == 'Z19':
							# Log.Info("CHKNG_J "+str(billtocustomer_quote_data))
							# quote_involved_party_sending_account = Sql.GetTable("SAQTIP")
							# sending_account_quote_data = {
							#     "QUOTE_INVOLVED_PARTY_RECORD_ID": str(Guid.NewGuid()).upper(),
							#     "ADDRESS": bill_to_customer.Address1 +', ' + bill_to_customer.City  +', ' + bill_to_customer.StateAbbreviation  +', ' + bill_to_customer.CountryAbbreviation +', ' + bill_to_customer.ZipCode,
							#     "EMAIL": bill_to_customer.Email,
							#     "IS_MAIN": bill_to_customer.Active,
							#     "QUOTE_ID": contract_quote_data.get("QUOTE_ID"),
							#     "QUOTE_NAME": custom_fields_detail.get("STPAccountName"),
							#     "QUOTE_RECORD_ID": contract_quote_data.get("MASTER_TABLE_QUOTE_RECORD_ID"),
							#     "PARTY_ID": bill_to_customer.CustomerCode,
							#     "PARTY_NAME": bill_to_customer.FirstName,
							#     "PARTY_ROLE": "SENDING ACCOUNT",
							#     "PHONE": bill_to_customer.BusinessPhone,
							# }
							# quote_involved_party_sending_account.AddRow(sending_account_quote_data)
							# Sql.Upsert(quote_involved_party_sending_account)
							# Log.Info("SENDING_ACCOUNT ADDED")

							getState = Sql.GetFirst("SELECT STATE_RECORD_ID FROM SACYST WHERE STATE = '{}'".format(custom_fields_detail.get("PayerState")))
							quote_sending_account_details = Sql.GetTable("SAQSRA")
							sending_account_detail_data = {
								"ACCOUNT_ID": custom_fields_detail.get("STPAccountID"),
								"ACCOUNT_NAME": custom_fields_detail.get("STPAccountName"),
								"ACCOUNT_RECORD_ID": contract_quote_obj.ACCOUNT_RECORD_ID,
								"QUOTE_ID": contract_quote_data.get("QUOTE_ID"),
								"QUOTE_NAME": custom_fields_detail.get("STPAccountName"),
								"QUOTE_RECORD_ID": contract_quote_data.get("MASTER_TABLE_QUOTE_RECORD_ID"),
								"RELOCATION_TYPE": "SENDING ACCOUNT",
								"SALESORG_ID": salesorg_data.get("SALESORG_ID"),
								"SALESORG_NAME": salesorg_data.get("SALESORG_NAME"),
								"SALESORG_RECORD_ID": salesorg_data.get("SALESORG_RECORD_ID"),
								"QUOTE_SENDING_RECEIVING_ACCOUNT": str(Guid.NewGuid()).upper(),
								"ADDRESS_1": bill_to_customer.Address1,
								"ADDRESS_2": "",
								"CITY": bill_to_customer.City,
								"COUNTRY": salesorg_country.COUNTRY,
								"COUNTRY_RECORD_ID": salesorg_country_name.COUNTRY_NAME,
								"EMAIL": bill_to_customer.Email,
								"PHONE": bill_to_customer.BusinessPhone,
								"POSTAL_CODE": custom_fields_detail.get("PayerPostalCode"),
								"STATE": custom_fields_detail.get("PayerState"),
								"STATE_RECORD_ID": getState.STATE_RECORD_ID,
								"QTEREV_RECORD_ID":quote_revision_id,
								"QTEREV_ID":quote_rev_id

							}
							quote_sending_account_details.AddRow(sending_account_detail_data)
							Sql.Upsert(quote_sending_account_details)
							#Log.Info("SENDING_ACCOUNT_Detail ADDED")
						if contract_quote_obj:
							quote_record_id = contract_quote_obj.MASTER_TABLE_QUOTE_RECORD_ID
							quote_id = contract_quote_obj.QUOTE_ID
							if fab_location_ids:
								Log.Info("""
																INSERT
																SAQFBL (FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID,QTEREV_RECORD_ID,QTEREV_ID, QUOTE_ID, QUOTE_RECORD_ID, COUNTRY, COUNTRY_RECORD_ID, MNT_PLANT_ID, MNT_PLANT_NAME, MNT_PLANT_RECORD_ID, SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID, FABLOCATION_STATUS, ADDRESS_1, ADDRESS_2, CITY, STATE, STATE_RECORD_ID, QUOTE_FABLOCATION_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified)
																SELECT A.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_FABLOCATION_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED, {UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
																	SELECT DISTINCT FAB_LOCATION_ID, FAB_LOCATION_NAME, FAB_LOCATION_RECORD_ID,
																	'{quote_revision_id}' AS QTEREV_RECORD_ID,'{quote_rev_id}' AS QTEREV_ID, '{QuoteId}' as QUOTE_ID, '{QuoteRecordId}' as QUOTE_RECORD_ID, COUNTRY, COUNTRY_RECORD_ID, MNT_PLANT_ID, '' as MNT_PLANT_NAME, MNT_PLANT_RECORD_ID, SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID, STATUS, ADDRESS_1, ADDRESS_2, CITY, STATE, STATE_RECORD_ID FROM MAFBLC (NOLOCK)
																	WHERE FAB_LOCATION_ID IN ('{FabLocationIds}')
																	) A
																""".format(UserId=User.Id, UserName=User.UserName,QuoteId=quote_id, QuoteRecordId=quote_record_id, FabLocationIds=fab_location_ids,quote_revision_id=quote_revision_id,quote_rev_id=quote_rev_id)) 
								SAQFBL_start = time.time()
								fab_insert = Sql.RunQuery("""
																INSERT
																SAQFBL (FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, QTEREV_RECORD_ID,QTEREV_ID,QUOTE_ID, QUOTE_RECORD_ID, COUNTRY, COUNTRY_RECORD_ID, MNT_PLANT_ID, MNT_PLANT_NAME, MNT_PLANT_RECORD_ID, SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID, FABLOCATION_STATUS, ADDRESS_1, ADDRESS_2, CITY, STATE, STATE_RECORD_ID, QUOTE_FABLOCATION_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified)
																SELECT A.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_FABLOCATION_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED, {UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
																	SELECT DISTINCT FAB_LOCATION_ID, FAB_LOCATION_NAME, FAB_LOCATION_RECORD_ID,'{quote_revision_id}' AS QTEREV_RECORD_ID,'{quote_rev_id}' AS QTEREV_ID, '{QuoteId}' as QUOTE_ID, '{QuoteRecordId}' as QUOTE_RECORD_ID, COUNTRY, COUNTRY_RECORD_ID, MNT_PLANT_ID, '' as MNT_PLANT_NAME, MNT_PLANT_RECORD_ID, SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID, STATUS, ADDRESS_1, ADDRESS_2, CITY, STATE, STATE_RECORD_ID FROM MAFBLC (NOLOCK)
																	WHERE FAB_LOCATION_ID IN ('{FabLocationIds}')
																	) A
																""".format(UserId=User.Id, UserName=User.UserName,QuoteId=quote_id, QuoteRecordId=quote_record_id, FabLocationIds=fab_location_ids,quote_revision_id=quote_revision_id,quote_rev_id=quote_rev_id))
								SAQFBL_end = time.time()
								#Log.Info("SAQFBL time----------"+str(SAQFBL_end-SAQFBL_start))

							
							

							if service_ids:			
								
								SAQTSV_start = time.time()
								service_insert = Sql.RunQuery("""
																INSERT
																SAQTSV (QTEREV_RECORD_ID,QTEREV_ID,QUOTE_ID, QUOTE_NAME,UOM_ID, QUOTE_RECORD_ID, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, SERVICE_TYPE, SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID, QUOTE_SERVICE_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified)
																SELECT A.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED, {UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
																	SELECT DISTINCT '{quote_revision_id}' AS QTEREV_RECORD_ID,'{quote_rev_id}' AS QTEREV_ID,'{QuoteId}' as QUOTE_ID, 'QuoteName' as QUOTE_NAME,UNIT_OF_MEASURE, '{QuoteRecordId}' as QUOTE_RECORD_ID, SAP_DESCRIPTION as SERVICE_DESCRIPTION, SAP_PART_NUMBER as SERVICE_ID, MATERIAL_RECORD_ID as SERVICE_RECORD_ID, PRODUCT_TYPE as SERVICE_TYPE, '{SalesorgId}' as SALESORG_ID, '{SalesorgName}' as SALESORG_NAME, '{SalesorgRecordId}' as SALESORG_RECORD_ID FROM MAMTRL (NOLOCK)
																	WHERE SAP_PART_NUMBER IN ('{ServiceIds}')
																	) A
																""".format(UserId=User.Id,UserName=User.UserName,QuoteId=quote_id, QuoteName=contract_quote_obj.QUOTE_NAME,QuoteRecordId=quote_record_id, SalesorgId=salesorg_data.get("SALESORG_ID"), SalesorgName=salesorg_data.get("SALESORG_NAME"), SalesorgRecordId=salesorg_data.get("SALESORG_RECORD_ID"), ServiceIds=service_ids,quote_revision_id=quote_revision_id,quote_rev_id=quote_rev_id))
								##A055S000P01-8740 code ends...
								#Log.Info("CQDOCUTYPE start ==> ")
								#ScriptExecutor.ExecuteGlobal('CQDOCUTYPE',{'QUOTE_RECORD_ID':quote_record_id,'QTEREV_RECORD_ID':quote_revision_id})
								#Log.Info("CQDOCUTYPE end ==> ")
								##A055S000P01-8740 code ends...

								#SAQTSV_end = time.time()
								#Log.Info("SAQTSV time-----"+str(SAQTSV_end-SAQTSV_start))
								#service_ADDon = Sql.RunQuery(""" INSERT SAQSAO (QUOTE_SERVICE_ADD_ON_PRODUCT_RECORD_ID,ADNPRD_DESCRIPTION,ADNPRD_ID,ADNPRDOFR_RECORD_ID,ADNPRD_RECORD_ID,ADN_TYPE,QUOTE_ID,QUOTE_NAME,QUOTE_RECORD_ID,QTESRV_RECORD_ID,SALESORG_ID,SALESORG_NAME,ACTIVE,SALESORG_RECORD_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified) SELECT CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_ADD_ON_PRODUCT_RECORD_ID,MAADPR.ADNPRDOFR_NAME,MAADPR.ADNPRDOFR_ID,MAADPR.ADNPRDOFR_RECORD_ID,MAADPR.ADD_ON_PRODUCT_RECORD_ID,MAADPR.ADN_TYPE,SAQTSV.QUOTE_ID,SAQTSV.QUOTE_NAME,SAQTSV.QUOTE_RECORD_ID,SAQTSV.QUOTE_SERVICE_RECORD_ID,SAQTSV.SALESORG_ID,SAQTSV.SALESORG_NAME,'FALSE' as ACTIVE,SAQTSV.SALESORG_RECORD_ID,SAQTSV.SERVICE_DESCRIPTION,SAQTSV.SERVICE_ID,SAQTSV.SERVICE_RECORD_ID,'{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED, {UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM MAADPR (NOLOCK) INNER JOIN  SAQTSV ON MAADPR.PRDOFR_ID = SAQTSV.SERVICE_ID WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND SERVICE_ID ='{ServiceIds}' """.format(UserId=User.Id,UserName=User.UserName,QuoteRecordId=quote_record_id,ServiceIds=service_ids))
								entitle_start_time = time.time()
								#Log.Info("CreateEntitlements start ==> "+str(entitle_start_time))
								self.CreateEntitlements(quote_record_id)
								entitle_end_time = time.time()
								#Log.Info("CreateEntitlements end==> "+str(entitle_end_time - entitle_start_time))
							if equipment_data:
								#Log.Info(""""EQUIPMENTS INSERT""")
								count = 0
								for fab_location_id, value in equipment_data.items():
									if count == 0:
										Log.Info("""Equipment_INSERT_2""")
									
									count += 1
									SAQFEQ_start = time.time()
									equipment_insert = Sql.RunQuery("""
																	INSERT SAQFEQ
																	(QTEREV_RECORD_ID,QTEREV_ID,EQUIPMENT_DESCRIPTION, EQUIPMENT_ID, EQUIPMENT_RECORD_ID, FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, MNT_PLANT_ID, MNT_PLANT_NAME, MNT_PLANT_RECORD_ID, PLATFORM, QUOTE_ID, QUOTE_NAME, QUOTE_RECORD_ID, SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID, SERIAL_NUMBER, WAFER_SIZE, TECHNOLOGY, EQUIPMENTCATEGORY_ID, EQUIPMENTCATEGORY_RECORD_ID, EQUIPMENTCATEGORY_DESCRIPTION, EQUIPMENT_STATUS, PBG,  WARRANTY_END_DATE, WARRANTY_START_DATE, CUSTOMER_TOOL_ID, GREENBOOK, GREENBOOK_RECORD_ID, QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified)
																SELECT A.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED, {UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
																	SELECT DISTINCT '{quote_revision_id}' AS QTEREV_RECORD_ID,'{quote_rev_id}' AS QTEREV_ID,EQUIPMENT_DESCRIPTION, EQUIPMENT_ID, EQUIPMENT_RECORD_ID,  FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, MNT_PLANT_ID,'' as MNT_PLANT_NAME, MNT_PLANT_RECORD_ID, PLATFORM, '{QuoteId}' as QUOTE_ID, '{QuoteName}' as QUOTE_NAME, '{QuoteRecordId}' as QUOTE_RECORD_ID, SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID, SERIAL_NO, SUBSTRATE_SIZE, TECHNOLOGY, EQUIPMENTCATEGORY_ID, EQUIPMENTCATEGORY_RECORD_ID, EQUIPMENTCATEGORY_DESCRIPTION, EQUIPMENT_STATUS, PBG, WARRANTY_END_DATE, WARRANTY_START_DATE, CUSTOMER_TOOL_ID,  GREENBOOK, GREENBOOK_RECORD_ID FROM MAEQUP (NOLOCK)
																	JOIN (SELECT NAME FROM SPLITSTRING('{EquipmentIds}'))B ON MAEQUP.EQUIPMENT_ID = NAME WHERE ISNULL(SERIAL_NO, '') <> '' AND FABLOCATION_ID = '{FabLocationId}'
																	) A
																""".format(UserId=User.Id,UserName=User.Name,QuoteId=quote_id, QuoteName=contract_quote_obj.QUOTE_NAME,QuoteRecordId=quote_record_id, FabLocationId=fab_location_id, EquipmentIds=",".join(value),quote_revision_id=quote_revision_id,quote_rev_id=quote_rev_id))
									SAQFEQ_end = time.time()
									#Log.Info("SAQFEQ----"+str(SAQFEQ_end-SAQFEQ_start))

									
									
								'''Log.Info("""
										INSERT SAQFEA
										(ASSEMBLY_DESCRIPTION, ASSEMBLY_ID, ASSEMBLY_RECORD_ID, EQUIPMENTCATEGORY_ID, EQUIPMENTCATEGORY_RECORD_ID, EQUIPMENT_DESCRIPTION, EQUIPMENT_ID, EQUIPMENT_RECORD_ID,
										FABLOCATION_ID,
										FABLOCATION_NAME, FABLOCATION_RECORD_ID, GOT_CODE, MNT_PLANT_ID, MNT_PLANT_RECORD_ID, QUOTE_ID, QUOTE_NAME, QUOTE_RECORD_ID, SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID, SERIAL_NUMBER, WARRANTY_END_DATE, WARRANTY_START_DATE, SUBSTRATE_SIZE, ASSEMBLY_STATUS, QUOTE_FAB_LOC_COV_OBJ_ASSEMBLY_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED)
									SELECT A.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_FAB_LOC_COV_OBJ_ASSEMBLY_RECORD_ID, {UserId} as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM (
										SELECT DISTINCT MAEQUP.EQUIPMENT_DESCRIPTION as ASSEMBLY_DESCRIPTION, MAEQUP.EQUIPMENT_ID as ASSEMBLY_ID, MAEQUP.EQUIPMENT_RECORD_ID as ASSEMBLY_RECORD_ID, MAEQUP.EQUIPMENTCATEGORY_ID, MAEQUP.EQUIPMENTCATEGORY_RECORD_ID, SAQFEQ.EQUIPMENT_DESCRIPTION, SAQFEQ.EQUIPMENT_ID, SAQFEQ.EQUIPMENT_RECORD_ID, SAQFEQ.FABLOCATION_ID, SAQFEQ.FABLOCATION_NAME, SAQFEQ.FABLOCATION_RECORD_ID, MAEQUP.GOT_CODE, MAEQUP.MNT_PLANT_ID, MAEQUP.MNT_PLANT_RECORD_ID, '{QuoteId}' as QUOTE_ID, '{QuoteName}' as QUOTE_NAME, '{QuoteRecordId}' as QUOTE_RECORD_ID, SAQFEQ.SALESORG_ID, SAQFEQ.SALESORG_NAME, SAQFEQ.SALESORG_RECORD_ID, MAEQUP.SERIAL_NO as SERIAL_NUMBER, MAEQUP.WARRANTY_END_DATE, MAEQUP.WARRANTY_START_DATE, MAEQUP.SUBSTRATE_SIZE, MAEQUP.EQUIPMENT_STATUS as ASSEMBLY_STATUS FROM SAQFEQ (NOLOCK) JOIN MAEQUP (NOLOCK) ON MAEQUP.PAR_EQUIPMENT_ID = SAQFEQ.EQUIPMENT_ID AND MAEQUP.FABLOCATION_ID = SAQFEQ.FABLOCATION_ID AND MAEQUP.SALESORG_RECORD_ID = SAQFEQ.SALESORG_RECORD_ID
										WHERE MAEQUP.ACCOUNT_RECORD_ID = '{AccountRecordId}' AND ISNULL(MAEQUP.SERIAL_NO, '') = '' AND SAQFEQ.QUOTE_RECORD_ID = '{QuoteRecordId}'
										) A
									""".format(UserId=User.Id,QuoteId=quote_id, QuoteName=contract_quote_obj.QUOTE_NAME, QuoteRecordId=quote_record_id, AccountRecordId=contract_quote_obj.ACCOUNT_RECORD_ID))'''
								fab_equip_assem_start_time = time.time()
								Log.Info("fab_equip_assem_start_time start ==> "+str(fab_equip_assem_start_time))


								# for fab_location_id in equipment_data.items():
								Log.Info("""INSERT SAQFGB ( 
								QTEREV_RECORD_ID,QTEREV_ID,FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID, QTEFBL_RECORD_ID,QUOTE_ID, QUOTE_NAME, QUOTE_RECORD_ID, SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,QUOTE_FAB_LOC_GB_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy
								) 
								SELECT A.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_FAB_LOC_GB_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED, {UserId} as CpqTableEntryModifiedBy FROM ( 
								select '{quote_revision_id}' AS QTEREV_RECORD_ID,'{quote_rev_id}' AS QTEREV_ID,FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID, QTEFBL_RECORD_ID,QUOTE_ID, QUOTE_NAME, QUOTE_RECORD_ID, SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID from SAQFEQ where QUOTE_RECORD_ID = '{QuoteRecordId}' group by FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID, QTEFBL_RECORD_ID,QUOTE_ID, QUOTE_NAME, QUOTE_RECORD_ID, SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID) 
								A """.format(UserId=User.Id,UserName=User.Name,QuoteId=quote_id, QuoteName=contract_quote_obj.QUOTE_NAME,QuoteRecordId=quote_record_id,quote_revision_id=quote_revision_id,quote_rev_id=quote_rev_id))

								SAQFGB_start = time.time()
								greenbook_detail_insert = Sql.RunQuery(""" INSERT SAQFGB ( 
								QTEREV_RECORD_ID,QTEREV_ID,FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID, QTEFBL_RECORD_ID,QUOTE_ID, QUOTE_NAME, QUOTE_RECORD_ID, SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,QUOTE_FAB_LOC_GB_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED,CpqTableEntryModifiedBy,CpqTableEntryDateModified
								) 
								SELECT A.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_FAB_LOC_GB_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED, {UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM ( 
								select '{quote_revision_id}' AS QTEREV_RECORD_ID,'{quote_rev_id}' AS QTEREV_ID,FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID, QTEFBL_RECORD_ID,QUOTE_ID, QUOTE_NAME, QUOTE_RECORD_ID, SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID from SAQFEQ where QUOTE_RECORD_ID = '{QuoteRecordId}' group by FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, GREENBOOK, GREENBOOK_RECORD_ID, QTEFBL_RECORD_ID,QUOTE_ID, QUOTE_NAME, QUOTE_RECORD_ID, SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID) 
								A """.format(UserId=User.Id,UserName=User.UserName,QuoteId=quote_id, QuoteName=contract_quote_obj.QUOTE_NAME,QuoteRecordId=quote_record_id,quote_revision_id=quote_revision_id,quote_rev_id=quote_rev_id))
								SAQFGB_end = time.time()
								#Log.Info("SAQFGB-------"+str(SAQFGB_start-SAQFGB_end))

								SAQFEA_start = time.time()
								Sql.RunQuery("""
												INSERT SAQFEA
												(QTEREV_RECORD_ID,QTEREV_ID,ASSEMBLY_DESCRIPTION, ASSEMBLY_ID, ASSEMBLY_RECORD_ID, EQUIPMENTCATEGORY_ID,EQUIPMENTTYPE_ID, EQUIPMENTCATEGORY_RECORD_ID, EQUIPMENT_DESCRIPTION, EQUIPMENT_ID, EQUIPMENT_RECORD_ID, FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, GOT_CODE, MNT_PLANT_ID, MNT_PLANT_RECORD_ID, QUOTE_ID, QUOTE_NAME, QUOTE_RECORD_ID, SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID, SERIAL_NUMBER, WARRANTY_END_DATE, WARRANTY_START_DATE, SUBSTRATE_SIZE, ASSEMBLY_STATUS, QUOTE_FAB_LOC_COV_OBJ_ASSEMBLY_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED)
											SELECT A.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_FAB_LOC_COV_OBJ_ASSEMBLY_RECORD_ID, {UserId} as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM (
												SELECT DISTINCT '{quote_revision_id}' AS QTEREV_RECORD_ID,'{quote_rev_id}' AS QTEREV_ID,MAEQUP.EQUIPMENT_DESCRIPTION as ASSEMBLY_DESCRIPTION, MAEQUP.EQUIPMENT_ID as ASSEMBLY_ID, MAEQUP.EQUIPMENT_RECORD_ID as ASSEMBLY_RECORD_ID, MAEQUP.EQUIPMENTCATEGORY_ID, MAEQUP.EQUIPMENTTYPE_ID, MAEQUP.EQUIPMENTCATEGORY_RECORD_ID, SAQFEQ.EQUIPMENT_DESCRIPTION, SAQFEQ.EQUIPMENT_ID, SAQFEQ.EQUIPMENT_RECORD_ID, SAQFEQ.FABLOCATION_ID, SAQFEQ.FABLOCATION_NAME, SAQFEQ.FABLOCATION_RECORD_ID, MAEQUP.GOT_CODE, MAEQUP.MNT_PLANT_ID, MAEQUP.MNT_PLANT_RECORD_ID, '{QuoteId}' as QUOTE_ID, '{QuoteName}' as QUOTE_NAME, '{QuoteRecordId}' as QUOTE_RECORD_ID, SAQFEQ.SALESORG_ID, SAQFEQ.SALESORG_NAME, SAQFEQ.SALESORG_RECORD_ID, MAEQUP.SERIAL_NO as SERIAL_NUMBER, MAEQUP.WARRANTY_END_DATE, MAEQUP.WARRANTY_START_DATE, MAEQUP.SUBSTRATE_SIZE, MAEQUP.EQUIPMENT_STATUS as ASSEMBLY_STATUS FROM SAQFEQ (NOLOCK) JOIN MAEQUP (NOLOCK) ON MAEQUP.PAR_EQUIPMENT_ID = SAQFEQ.EQUIPMENT_ID AND MAEQUP.FABLOCATION_ID = SAQFEQ.FABLOCATION_ID AND MAEQUP.SALESORG_RECORD_ID = SAQFEQ.SALESORG_RECORD_ID
												WHERE MAEQUP.ACCOUNT_RECORD_ID = '{AccountRecordId}' AND ISNULL(MAEQUP.SERIAL_NO, '') = '' AND SAQFEQ.QUOTE_RECORD_ID = '{QuoteRecordId}'
												) A
											""".format(UserId=User.Id,QuoteId=quote_id, QuoteName=contract_quote_obj.QUOTE_NAME, QuoteRecordId=quote_record_id, AccountRecordId=contract_quote_obj.ACCOUNT_RECORD_ID,quote_revision_id=quote_revision_id,quote_rev_id=quote_rev_id))
								SAQFEA_end = time.time()
								#Log.Info("SAQFEA-------"+str(SAQFEA_end-SAQFEA_start))
								fab_equip_assem_end_time = time.time()
								#Log.Info("fab_equip_assem_start_time end==> "+str(fab_equip_assem_end_time - fab_equip_assem_start_time))
								if  payload_json.get('SalesType') == 'Z15':
									#Log.Info("covered_object_data ===> "+str(covered_object_data))
									for service_id, equipment_values in covered_object_data.items():
										equipment_ids = ','.join(list(set(','.join(equipment_values).split(','))))
										'''Log.Info("===>>>>>>>> "+str("""SELECT STUFF((SELECT ', ' + SAQFEQ.QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID 
																	FROM SAQFEQ
																	JOIN (SELECT NAME FROM SPLITSTRING('{EquipmentIds}'))B ON SAQFEQ.EQUIPMENT_ID = NAME
																	WHERE SAQFEQ.QUOTE_RECORD_ID = '{QuoteRecordId}'
																	FOR XML PATH('')), 1, 1, '') as RECORD_IDS """.format(QuoteRecordId=quote_record_id,EquipmentIds=equipment_ids)))'''
										fab_equipments_obj = Sql.GetFirst("""SELECT STUFF((SELECT ', ' + SAQFEQ.QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID 
																	FROM SAQFEQ
																	JOIN (SELECT NAME FROM SPLITSTRING('{EquipmentIds}'))B ON SAQFEQ.EQUIPMENT_ID = NAME
																	WHERE SAQFEQ.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQFEQ.QTEREV_RECORD_ID = '{quote_revision_id}'
																	FOR XML PATH('')), 1, 1, '') as RECORD_IDS """.format(QuoteRecordId=quote_record_id,EquipmentIds=equipment_ids,quote_revision_id=quote_revision_id))
										if fab_equipments_obj:
											if fab_equipments_obj.RECORD_IDS:
												fab_equipment_record_ids = fab_equipments_obj.RECORD_IDS.split(',')
												quote_service_obj = Sql.GetFirst("select SERVICE_TYPE from SAQTSV (NOLOCK) where SERVICE_ID = '{Service_Id}' and QUOTE_RECORD_ID = '{QuoteRecordId}'".format(Service_Id = equipment_json_data.get('SERVICE_OFFERING_ID'),QuoteRecordId=quote_record_id))
												#Log.Info("fab_equipment_record_ids ===> "+str(fab_equipment_record_ids))							
												service_type = quote_service_obj.SERVICE_TYPE	
												tree_parent_level_1 = ''										
												Quote.SetGlobal("contract_quote_record_id",str(quote_record_id))
												#Log.Info("service_id------->"+str(service_id))
												start_time = time.time()
												#Log.Info("CQCRUDOPTN start ==> "+str(start_time))
												ScriptExecutor.ExecuteGlobal(
																		"CQCRUDOPTN",
																	{
																		"NodeType"   : "COVERED OBJ MODEL",
																		"ActionType" : "ADD_COVERED_OBJ",
																		"Opertion"    : "ADD",
																		"AllValues"  : False,
																		"TriggerFrom"   : "PythonScript",
																		"Values"	  : fab_equipment_record_ids,
																		"ServiceId"  : service_id,
																		"ServiceType" : service_type,
																		"tree_parent_level_1": tree_parent_level_1,
																	},
																)
											ScriptExecutor.ExecuteGlobal('CQDOCUTYPE',{'QUOTE_RECORD_ID':quote_record_id,'QTEREV_RECORD_ID':quote_revision_id})
											end_time = time.time()
												#Log.Info("CQCRUDOPTN end==> "+str(end_time - start_time))
									""" for equipment_json_data in payload_json.get('SAQFEQ'):
										quote_fab_equipments_obj = Sql.GetList("Select QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID FROM SAQFEQ(NOLOCK) WHERE EQUIPMENT_ID IN ({equipment_ids}) AND FABLOCATION_ID = '{fablocation_id}' AND QUOTE_ID = '{quote_id}'".format(equipment_ids = equipment_json_data.get('EQUIPMENT_IDS'),fablocation_id = equipment_json_data.get('FAB_LOCATION_ID'),quote_id = contract_quote_data.get("QUOTE_ID")))
										quote_service_obj = Sql.GetFirst("select SERVICE_TYPE from SAQTSV where SERVICE_ID = '{Service_Id}' and QUOTE_ID = '{Quote_Id}'".format(Service_Id = equipment_json_data.get('SERVICE_OFFERING_ID'),Quote_Id = contract_quote_data.get("QUOTE_ID")))
										quote_fab_equipments_record_id = [quote_fab_equipment_obj.QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID for quote_fab_equipment_obj in quote_fab_equipments_obj]
										service_id = equipment_json_data.get('SERVICE_OFFERING_ID')
										service_type = quote_service_obj.SERVICE_TYPE
										quote_record_id = contract_quote_obj.MASTER_TABLE_QUOTE_RECORD_ID
										contract_quote_record_id = Product.SetGlobal("contract_quote_record_id",str(quote_record_id))
										#Log.Info("service_id------->"+str(service_id))
										start_time = time.time()
										Log.Info("CQCRUDOPTN start ==> "+str(start_time))
										ScriptExecutor.ExecuteGlobal(
																"CQCRUDOPTN",
															{
																"NodeType"   : "COVERED OBJ MODEL",
																"ActionType" : "ADD_COVERED_OBJ",
																"Opertion"    : "ADD",
																"AllValues"  : False,
																"call_from"   : "python_script",
																"Values"	  : quote_fab_equipments_record_id,
																"service_id"  : service_id,
																"service_type" : service_type,
															},
														)
										end_time = time.time()
										Log.Info("CQCRUDOPTN end==> "+str(end_time - start_time)) """

								''' # Approval Trigger - Start								
								import ACVIORULES
								violationruleInsert = ACVIORULES.ViolationConditions()
								header_obj = Sql.GetFirst("SELECT RECORD_ID FROM SYOBJH (NOLOCK) WHERE OBJECT_NAME = 'SAQTMT'")
								if header_obj:
									Log.Info("Starting Approval Trigger--")									
									violationruleInsert.InsertAction(
																	header_obj.RECORD_ID, quote_record_id, "SAQTMT"
																	)
									Log.Info("Ending Approval Trigger--")
								# Approval Trigger - End '''
								if "Z0007" in service_ids:
									
									GetAccount = Sql.GetFirst("SELECT DISTINCT ACCOUNT_ID, ACCOUNT_NAME,ACCOUNT_RECORD_ID FROM MAEQUP (NOLOCK) JOIN (SELECT NAME FROM SPLITSTRING('{EquipmentIds}'))B ON MAEQUP.EQUIPMENT_ID = NAME".format(EquipmentIds=equipment_ids))
									account_obj = Sql.GetFirst("SELECT ACCOUNT_ID,ACCOUNT_NAME,EMAIL,ACCOUNT_RECORD_ID, ACCOUNT_TYPE,PHONE,ADDRESS_1, FROM SAACNT(NOLOCK) WHERE ACCOUNT_ID LIKE '%{}'".format(GetAccount.ACCOUNT_ID))
						
						
									if not account_obj:
										getState = Sql.GetFirst("SELECT STATE_RECORD_ID FROM SACYST WHERE STATE = '{}'".format(custom_fields_detail.get("PayerState")))
										NewAccountRecordId = str(Guid.NewGuid()).upper()
										Sql.RunQuery("""INSERT INTO SAACNT (ACCOUNT_RECORD_ID,ACCOUNT_ID,ACCOUNT_NAME,ACCOUNT_TYPE,ACTIVE,ADDRESS_1,CITY,COUNTRY,COUNTRY_RECORD_ID,PHONE,POSTAL_CODE,REGION,REGION_RECORD_ID,STATE,STATE_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED)VALUES('{AccountRecordId}','{AccountId}','{AccountName}','{Type}',1,'{Address}','{City}','{Country}','{CountryRecordId}','{Phone}','{PostalCode}','{Region}','{RegionRecordId}','{State}','{StateRecordId}','{UserName}',GETDATE())
										""".format(AccountRecordId=NewAccountRecordId,AccountId=GetAccount.ACCOUNT_ID,AccountName=GetAccount.ACCOUNT_NAME,Type="",Address=custom_fields_detail.get("PayerAddress1"),City=custom_fields_detail.get("PayerCity"),Country=custom_fields_detail.get("PayerCountry"),CountryRecordId=salesorg_country.COUNTRY_RECORD_ID,Phone=custom_fields_detail.get("PayerPhone"),PostalCode=custom_fields_detail.get("PayerPostalCode"),Region='',RegionRecordId='',State=custom_fields_detail.get("PayerState"),StateRecordId=getState.STATE_RECORD_ID,UserName=User.UserName))
										
										account_obj = Sql.GetFirst("SELECT ACCOUNT_ID,ACCOUNT_NAME,EMAIL,ACCOUNT_RECORD_ID, ACCOUNT_TYPE,PHONE,ADDRESS_1, FROM SAACNT(NOLOCK) WHERE ACCOUNT_ID LIKE '%{}'".format(GetAccount.ACCOUNT_ID))

									SourceAccountDetails = {
										"QUOTE_INVOLVED_PARTY_RECORD_ID": str(Guid.NewGuid()).upper(),
										"ADDRESS": account_obj.ADDRESS_1,
										"EMAIL": account_obj.EMAIL,
										"IS_MAIN": "1",
										"QUOTE_ID": contract_quote_data.get("QUOTE_ID"),
										"QUOTE_NAME": custom_fields_detail.get("STPAccountName"),
										"QUOTE_RECORD_ID": contract_quote_data.get("MASTER_TABLE_QUOTE_RECORD_ID"),
										"PARTY_ID": account_obj.ACCOUNT_ID,
										"PARTY_NAME": account_obj.ACCOUNT_NAME,
										"PARTY_ROLE": "SOURCE ACCOUNT",
										"PHONE": account_obj.PHONE,
										"QTEREV_RECORD_ID":quote_revision_id,
										"QTEREV_ID":quote_rev_id
									}
									quote_involved_party_table_info.AddRow(SourceAccountDetails)

									Sql.RunQuery(""" INSERT SAQSCF (QUOTE_SOURCE_FAB_LOCATION_RECORD_ID,QUOTE_ID,QUOTE_NAME,QUOTE_RECORD_ID,SRCACC_ID,SRCACC_NAME,SRCACC_RECORD_ID,SRCFBL_ID,SRCFBL_NAME,SRCFBL_RECORD_ID) SELECT  CONVERT(VARCHAR(4000),NEWID()) AS QUOTE_SOURCE_FAB_LOCATION_RECORD_ID, '{QuoteId}', '{QuoteName}','{QuoteRecordId}',MAFBLC.ACCOUNT_ID, MAFBLC.ACCOUNT_NAME,MAFBLC.ACCOUNT_RECORD_ID,MAFBLC.FAB_LOCATION_ID,MAFBLC.FAB_LOCATION_NAME,MAFBLC.	
										FAB_LOCATION_RECORD_ID FROM MAFBLC (NOLOCK) WHERE ACCOUNT_ID = '{AccountId}' """.format(QuoteId=quote_id,QuoteName=custom_fields_detail.get("STPAccountName"),QuoteRecordId=quote_record_id,AccountId=GetAccount.ACCOUNT_ID,quote_revision_id=quote_revision_id,quote_rev_id=quote_rev_id))

									Sql.RunQuery(""" INSERT SAQSTE
																(QTEREV_RECORD_ID,QTEREV_ID,SRCACC_ID,SRCACC_NAME,SRCACC_RECORD_ID,EQUIPMENT_DESCRIPTION, EQUIPMENT_ID, EQUIPMENT_RECORD_ID, SRCFBL_ID, SRCFBL_NAME, SRCFBL_RECORD_ID, MNT_PLANT_ID, MNT_PLANT_NAME, MNT_PLANT_RECORD_ID, QUOTE_ID, QUOTE_NAME, QUOTE_RECORD_ID,  EQUIPMENTCATEGORY_ID, EQUIPMENTCATEGORY_RECORD_ID, EQUIPMENTCATEGORY_DESCRIPTION, EQUIPMENT_STATUS, GREENBOOK, GREENBOOK_RECORD_ID, QUOTE_SOURCE_TARGET_FAB_LOC_EQUIP_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified)
															SELECT A.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SOURCE_TARGET_FAB_LOC_EQUIP_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED, {UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
																SELECT DISTINCT '{quote_revision_id}' AS QTEREV_RECORD_ID,'{quote_rev_id}' AS QTEREV_ID,ACCOUNT_ID,ACCOUNT_NAME,ACCOUNT_RECORD_ID,EQUIPMENT_DESCRIPTION, EQUIPMENT_ID, EQUIPMENT_RECORD_ID,  FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, MNT_PLANT_ID, '' as MNT_PLANT_NAME, MNT_PLANT_RECORD_ID, '{QuoteId}' as QUOTE_ID, '{QuoteName}' as QUOTE_NAME, '{QuoteRecordId}' as QUOTE_RECORD_ID,  EQUIPMENTCATEGORY_ID, EQUIPMENTCATEGORY_RECORD_ID, EQUIPMENTCATEGORY_DESCRIPTION, EQUIPMENT_STATUS, GREENBOOK, GREENBOOK_RECORD_ID FROM MAEQUP (NOLOCK) WHERE ACCOUNT_ID= '{AccountId}'
																) A""".format(UserId=User.Id,UserName=User.Name,QuoteId=quote_id, QuoteName=contract_quote_obj.QUOTE_NAME,QuoteRecordId=quote_record_id, FabLocationId=fab_location_id, AccountId=GetAccount.ACCOUNT_ID,quote_revision_id=quote_revision_id,quote_rev_id=quote_rev_id))
						payload_table_info = Sql.GetTable("SYINPL")
						payload_table_data = {'CpqTableEntryId':payload_json_obj.CpqTableEntryId, 'STATUS':'COMPLETED'}
						payload_table_info.AddRow(payload_table_data)
						Sql.Upsert(payload_table_info)
						#ScriptExecutor.ExecuteGlobal('CQDOCUTYPE',{'QUOTE_RECORD_ID':quote_record_id,'QTEREV_RECORD_ID':quote_revision_id})

		except Exception:   
			Log.Info("SYPOSTINSG ERROR---->:" + str(sys.exc_info()[1]))
			Log.Info("SYPOSTINSG ERROR LINE NO---->:" + str(sys.exc_info()[-1].tb_lineno))        

		sync_end_time = time.time()
		# Log.Info("SALETYPE_J "+str(SalesType.get(payload_json.get("SalesType"))))

		Log.Info("Sync end==> "+str(sync_end_time - sync_start_time))   

	def salesteam_insert(self,employee,contract_quote_data,quote_rev_id,quote_revision_id):
		Sql.RunQuery("""INSERT SAQDLT (
								C4C_PARTNERFUNCTION_ID,
								CRM_PARTNERFUNCTION_ID,
								PARTNERFUNCTION_DESC,
								PARTNERFUNCTION_ID,
								PARTNERFUNCTION_RECORD_ID,
								EMAIL,
								MEMBER_ID,
								MEMBER_NAME,
								MEMBER_RECORD_ID,
								QUOTE_ID,
								QUOTE_RECORD_ID,
								QTEREV_ID,
								QTEREV_RECORD_ID,
								QUOTE_REV_DEAL_TEAM_MEMBER_ID,
								CPQTABLEENTRYADDEDBY,
								CPQTABLEENTRYDATEADDED,
								CpqTableEntryModifiedBy, 
								CpqTableEntryDateModified
								) SELECT emp.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_REV_DEAL_TEAM_MEMBER_ID,'{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED,{UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
								SELECT DISTINCT  
								(SELECT TOP 1 C4C_PARTNER_FUNCTION FROM SYPFTY WHERE C4C_PARTNER_FUNCTION  = '{C4c_partner_function}' ) AS C4C_PARTNERFUNCTION_ID,
								(SELECT TOP 1 CRM_PARTNERFUNCTION FROM SYPFTY WHERE C4C_PARTNER_FUNCTION  = '{C4c_partner_function}' ) AS CRM_PARTNERFUNCTION_ID,
								(SELECT TOP 1 PARTNERFUNCTION_DESCRIPTION FROM SYPFTY WHERE C4C_PARTNER_FUNCTION  = '{C4c_partner_function}' ) AS PARTNERFUNCTION_DESC,
								(SELECT TOP 1 PARTNERFUNCTION_ID FROM SYPFTY WHERE C4C_PARTNER_FUNCTION  = '{C4c_partner_function}' ) AS PARTNERFUNCTION_ID,
								(SELECT TOP 1 PARTNERFUNCTION_RECORD_ID FROM SYPFTY WHERE C4C_PARTNER_FUNCTION  = '{C4c_partner_function}' ) AS PARTNERFUNCTION_RECORD_ID,
								SAEMPL.EMAIL,
								SAEMPL.EMPLOYEE_ID,
								SAEMPL.EMPLOYEE_NAME,
								SAEMPL.EMPLOYEE_RECORD_ID,
								'{QuoteId}' as QUOTE_ID,
								'{QuoteRecordId}' as QUOTE_RECORD_ID,
								'{RevisionId}' as QTEREV_ID,
								'{RevisionRecordId}' as QTEREV_RECORD_ID
								FROM SAEMPL WHERE EMPLOYEE_ID = '{EmployeeId}'
								) emp """.format(
								UserId = User.Id,
								EmployeeId = employee.get("EMPLOYEE_ID"),
								C4c_partner_function = employee.get("C4C_PARTNER_FUNCTION"),
								UserName=User.Name,
								QuoteId = contract_quote_data.get("QUOTE_ID"),
								QuoteRecordId=contract_quote_data.get("MASTER_TABLE_QUOTE_RECORD_ID"),
								RevisionId=quote_rev_id,
								RevisionRecordId=quote_revision_id,
								)
							)
sync_obj = SyncQuoteAndCustomTables(Quote)
sync_obj.create_custom_table_record()
#ScriptExecutor.ExecuteGlobal('CQDOCUTYPE',{'QUOTE_RECORD_ID':quote_record_id,'QTEREV_RECORD_ID':quote_revision_id})


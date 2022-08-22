# =========================================================================================================================================
#   __script_name : CQSYNCC4CQ.PY
#   __script_description : THIS SCRIPT IS USED TO SYNC THE QUOTE TABLES AND CONTRACT QUOTE CUSTOM TABLES WHEN WE CREATE A QUOTE FROM C4C
#   __primary_author__ : AYYAPPAN SUBRAMANIYAN
#   __create_date :25-10-2020
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct
import clr
import sys
import Webcom.Configurator.Scripting.Test.TestProduct
import System.Net
from System.Text.Encoding import UTF8
from System import Convert
from System.Net import HttpWebRequest, NetworkCredential
from datetime import datetime
import time

from SYDATABASE import SQL
Sql = SQL()

ScriptExecutor = ScriptExecutor

class ContractQuoteC4CSync:
	def __init__(self, c4c_opportunity_id=None, c4c_quote_id=None):
		self.c4c_quote_id = c4c_quote_id
		self.c4c_opportunity_id = c4c_opportunity_id
		self.contract_quote_data = {}
		self.document_type = {"ZTBC": "SSC", "ZWK1": "APG"}
		self.quote_type = {"ZTBC":"ZTBC - TOOL BASED", "ZNBC":"ZNBC - NON TOOL BASED", "ZWK1":"ZWK1 - SPARES", "ZSWC":"ZSWC - SOLD WITH SYSTEM"}
		self.opportunity_type = {"ZTBC":"Service", "ZWK1":"Parts"}
		self.cpq_quote_id = ''

	def _iflow_call(self, request_data='', external_table_name=None, content_type="application/xml"):
		iflow_url_obj = Sql.GetFirst("SELECT URL FROM SYCONF (NOLOCK) WHERE External_Table_Name='{}'".format(external_table_name))
		login_credential_obj = Sql.GetFirst("SELECT User_name as Username, Password FROM SYCONF (NOLOCK) WHERE Domain='AMAT_TST'")
		if iflow_url_obj and login_credential_obj:
			username = str(login_credential_obj.Username)
			password = str(login_credential_obj.Password)
			iflow_url = str(iflow_url_obj.URL)
			authorization = username + ":" + password
			binaryAuthorization = UTF8.GetBytes(authorization)           

			authorization = Convert.ToBase64String(binaryAuthorization)
			authorization = "Basic " + authorization
		
			webclient = System.Net.WebClient()
			webclient.Headers[System.Net.HttpRequestHeader.ContentType] = content_type
			webclient.Headers[System.Net.HttpRequestHeader.Authorization] = authorization
			Log.Info(str(request_data)+"iflow_url==>>> "+str(iflow_url))
			response = webclient.UploadString(iflow_url, request_data)
			return response
		return ''
	
	def _get_c4c_quote_details(self):    
		request_data = '{"quoteId" : '+str(self.c4c_quote_id)+'}'    
		response = self._iflow_call(request_data, 'SAQTMT')    
		return eval(response)
	
	def _create_cpq_native_quote(self):
		request_data = (
					'<?xml version="1.0" encoding="UTF-8"?><soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"><soapenv:Body><quoteid>'
					+ str(self.c4c_quote_id)
					+'</quoteid></soapenv:Body></soapenv:Envelope>'
				)
		response = self._iflow_call(request_data, 'C4C_TO_CPQ_QUOTE_CREATE')    
		return response
	
	def process_custom_field(self, custom_field_value):
		if custom_field_value:
			custom_field_result = {custom_field.get('Name'):custom_field.get('Value') for custom_field in custom_field_value.get('CustomField')}
			return custom_field_result
		return {}
	
	def _insert_quote_salesorg(self, quote_data):
		quote_salesorg_table_info = Sql.GetTable("SAQTSO")
		if self.contract_quote_data.get("SALESORG_RECORD_ID"):
			
			salesorg_data = {
				"QUOTE_SALESORG_RECORD_ID": str(Guid.NewGuid()).upper(),
				"QUOTE_ID": self.cpq_quote_id,
				"QUOTE_NAME": self.contract_quote_data.get("QUOTE_NAME"),
				"QUOTE_RECORD_ID": self.contract_quote_data.get("MASTER_TABLE_QUOTE_RECORD_ID"),
				"SALESORG_ID": self.contract_quote_data.get("SALESORG_ID"),
				"SALESORG_NAME": self.contract_quote_data.get("SALESORG_NAME"),
				"SALESORG_RECORD_ID": self.contract_quote_data.get("SALESORG_NAME"),
				"QUOTE_CURRENCY":self.contract_quote_data.get("QUOTE_CURRENCY"),
				"QUOTE_CURRENCY_RECORD_ID":self.contract_quote_data.get("QUOTE_CURRENCY_RECORD_ID"),
			}
			if quote_data.get('DistributionChannel'):
				distribution_obj = Sql.GetFirst(
					"SELECT DISTRIBUTION_CHANNEL_RECORD_ID, DISTRIBUTIONCHANNEL_ID FROM SADSCH (NOLOCK) WHERE DISTRIBUTIONCHANNEL_ID = '{}'".format(
						quote_data.get('DistributionChannel')
					)
				)
				if distribution_obj:
					salesorg_data.update({"DISTRIBUTIONCHANNEL_ID":distribution_obj.DISTRIBUTIONCHANNEL_ID , 
										"DISTRIBUTIONCHANNEL_RECORD_ID":distribution_obj.DISTRIBUTION_CHANNEL_RECORD_ID})
			if quote_data.get('SalesOrgID'):
				SalesOrg_obj = Sql.GetFirst(
					"SELECT DEF_CURRENCY, DEF_CURRENCY_RECORD_ID FROM SASORG (NOLOCK) WHERE SALESORG_ID = '{}'".format(
						quote_data.get('SalesOrgID')
					)
				)
				if SalesOrg_obj:
					salesorg_data.update({"SORG_CURRENCY":SalesOrg_obj.DEF_CURRENCY, 
										"SORGCURRENCY_RECORD_ID":SalesOrg_obj.DEF_CURRENCY_RECORD_ID})				                        
			if quote_data.get('Division'):
				division_obj = Sql.GetFirst(
					"SELECT DIVISION_RECORD_ID, DIVISION_ID FROM SADIVN (NOLOCK) WHERE DIVISION_ID = '{}'".format(
						quote_data.get('Division')
					)
				)
				if division_obj:
					quote_data.update({"DIVISION_RECORD_ID":division_obj.DIVISION_RECORD_ID , 
										"DIVISION_ID":division_obj.DIVISION_ID})
			
			if quote_data.get('SalesOfficeID'):
				salesoffice_obj = Sql.GetFirst(
					"SELECT SALES_OFFICE_RECORD_ID, SALES_OFFICE_ID, SALES_OFFICE_NAME FROM SASLOF (NOLOCK) WHERE SALES_OFFICE_ID = '{}'".format(
						quote_data.get('SalesOfficeID')
					)
				)
				if salesoffice_obj:
					salesorg_data.update({"SALESOFFICE_ID":salesoffice_obj.SALES_OFFICE_ID , 
										"SALESOFFICE_NAME":salesoffice_obj.SALES_OFFICE_NAME,
										"SALESOFFICE_RECORD_ID":salesoffice_obj.SALES_OFFICE_RECORD_ID
										})
			
			Log.Info("salesorg_data--->"+str(salesorg_data))							
			quote_salesorg_table_info.AddRow(salesorg_data)
			#Sql.Upsert(quote_salesorg_table_info)
		return quote_salesorg_table_info
	
	def _insert_opportunity_and_quote_opportunity(self, quote_data):
		quote_opportunity_table_info = Sql.GetTable("SAOPQT")
		if quote_data.get("STPAccountID"):            
			account_obj = Sql.GetFirst(
				"SELECT ACCOUNT_RECORD_ID, ACCOUNT_TYPE FROM SAACNT(NOLOCK) WHERE ACCOUNT_ID LIKE '%{}'".format(
					quote_data.get("STPAccountID")
				)
			)
			if account_obj:
				self.contract_quote_data.update(
					{
						"ACCOUNT_RECORD_ID": account_obj.ACCOUNT_RECORD_ID,
						"ACCOUNT_ID": quote_data.get("STPAccountID"),
						"ACCOUNT_NAME": quote_data.get("STPAccountName"),
					}
				)

				if quote_data.get("OpportunityId"):
					opportunity_obj = Sql.GetFirst(
						"""SELECT OPPORTUNITY_RECORD_ID, OPPORTUNITY_ID, OPPORTUNITY_STAGE, OPPORTUNITY_NAME FROM SAOPPR(NOLOCK) 
												WHERE OPPORTUNITY_ID = '{}' 
												AND ACCOUNT_RECORD_ID = '{}'""".format(
							quote_data.get("OpportunityId"), self.contract_quote_data.get("ACCOUNT_RECORD_ID")
						)
					)
					if quote_data.get("OpportunityStage"):
						Opportunitystagedict = {"Z0001":"NEW","Z0002":"DEFINE OPPORTUNITY","Z0003":"CONFIGURE QUOTE","Z0004":"MANUAL PRICING REQUESTED","Z0005":"FINANCE/BD/NSDR/APPROVAL","Z0006":"FINANCE/BD/NSDR APPROVED","Z0007":"QUOTE GENERATED","Z0008":"QUOTE ACCEPTED – CUSTOMER","Z0009":"BOOKING SUBMITTED","Z0010":"WON","Z0011":"STOPPED","Z0012":"LOST","Z0013":"POES PRICING REQUESTED","Z0014":"POES PRICING GENERATED","Z0017":"PRICING DETERMINED"}
					if not opportunity_obj:
						master_opportunity_table_info = Sql.GetTable("SAOPPR")
						master_opportunity_data = {
							"OPPORTUNITY_RECORD_ID": str(Guid.NewGuid()).upper(),
							"ACCOUNT_ID": quote_data.get("STPAccountID"),
							"ACCOUNT_NAME": quote_data.get("STPAccountName"),
							"ACCOUNT_RECORD_ID": account_obj.ACCOUNT_RECORD_ID,
							"DOCUMENT_TYPE": self.contract_quote_data.get("DOCUMENT_TYPE"),
							"CPQTABLEENTRYDATEADDED": datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"),
							"OPPORTUNITY_ID": quote_data.get("OpportunityId"),
							"OPPORTUNITY_NAME": self.quote.OpportunityName,
							"OPPORTUNITY_TYPE": quote_data.get("OpportunityType"),
							"SALESORG_ID": self.contract_quote_data.get("SALESORG_ID"),
							"SALESORG_NAME": self.contract_quote_data.get("SALESORG_NAME"),
							"SALESORG_RECORD_ID": self.contract_quote_data.get("SALESORG_RECORD_ID"),
							"SALE_TYPE": "NEW",
							"OPPORTUNITY_STAGE": Opportunitystagedict.get(quote_data.get("OpportunityStage")),
							"ACCOUNT_TYPE": "Sold to Party",
							"OPPORTUNITY_OWNER_ID": quote_data.get("OpportunityOwner"),
						}
						Log.Info("master_opportunity_data ===>" + str(master_opportunity_data))
						master_opportunity_table_info.AddRow(master_opportunity_data)
						Sql.Upsert(master_opportunity_table_info)
						opportunity_obj = Sql.GetFirst(
							"""SELECT OPPORTUNITY_RECORD_ID, OPPORTUNITY_ID, OPPORTUNITY_NAME, OPPORTUNITY_STAGE FROM SAOPPR(NOLOCK) 
												WHERE OPPORTUNITY_RECORD_ID = '{}'""".format(
								master_opportunity_data.get("OPPORTUNITY_RECORD_ID")
							)
						)
					Log.Info("opportunity_obj ===>" + str(opportunity_obj))
					opportunity_quote_data = {
						"OPPORTUNITY_QUOTE_RECORD_ID": str(Guid.NewGuid()).upper(),
						"OPPORTUNITY_ID": opportunity_obj.OPPORTUNITY_ID,
						"OPPORTUNITY_NAME": opportunity_obj.OPPORTUNITY_NAME,
						"OPPORTUNITY_RECORD_ID": opportunity_obj.OPPORTUNITY_RECORD_ID,
						"QUOTE_ID": self.contract_quote_data.get("QUOTE_ID"),
						"CPQTABLEENTRYDATEADDED": datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"),
						"QUOTE_RECORD_ID": self.contract_quote_data.get("MASTER_TABLE_QUOTE_RECORD_ID"),
						"ACCOUNT_ID": quote_data.get("STPAccountID"),
						"ACCOUNT_NAME": quote_data.get("STPAccountName"),
						"ACCOUNT_TYPE": account_obj.ACCOUNT_TYPE,                       
						
					}

					quote_opportunity_table_info.AddRow(opportunity_quote_data)
		return quote_opportunity_table_info
	
	def _insert_quote_involved_parties(self, quote_data):
		quote_involved_party_table_info = Sql.GetTable("SAQTIP")
		if quote_data.get('BillTo'):
			bill_to_customer = quote_data.get('BillTo')
			billtocustomer_quote_data = {
				"QUOTE_INVOLVED_PARTY_RECORD_ID": str(Guid.NewGuid()).upper(),
				"ADDRESS": bill_to_customer.get('Address1', '') +', ' + bill_to_customer.get('City','')  +', ' + bill_to_customer.get('StateAbbreviation', '')  +', ' + bill_to_customer.get('CountryAbbreviation', '') +', ' + bill_to_customer.get('ZipCode',''),
				"EMAIL": bill_to_customer.get('Email'),     
				"IS_MAIN": "1",           
				"QUOTE_ID": self.contract_quote_data.get("QUOTE_ID"),
				"QUOTE_NAME": quote_data.get("STPAccountName"),
				"QUOTE_RECORD_ID": self.contract_quote_data.get("MASTER_TABLE_QUOTE_RECORD_ID"),
				"PARTY_ID": bill_to_customer.get('CustomerCode',''),
				"PARTY_NAME": bill_to_customer.get('FirstName',''),
				"PARTY_ROLE": "BILL TO",
				"PHONE": bill_to_customer.get('BusinessPhone',''),
			}
			quote_involved_party_table_info.AddRow(billtocustomer_quote_data)
		if quote_data.get('ShipTo'):
			ship_to_customer = quote_data.get('ShipTo')
			shiptocustomer_quote_data = {
				"QUOTE_INVOLVED_PARTY_RECORD_ID": str(Guid.NewGuid()).upper(),
				"ADDRESS": ship_to_customer.get('Address1', '') +', ' + ship_to_customer.get('City','')  +', ' + ship_to_customer.get('StateAbbreviation', '')  +', ' + ship_to_customer.get('CountryAbbreviation', '') +', ' + ship_to_customer.get('ZipCode',''),
				"EMAIL": ship_to_customer.get('Email'),
				"IS_MAIN": "1",
				"QUOTE_ID": self.contract_quote_data.get("QUOTE_ID"),
				"QUOTE_NAME": quote_data.get("STPAccountName"),
				"QUOTE_RECORD_ID": self.contract_quote_data.get("MASTER_TABLE_QUOTE_RECORD_ID"),
				"PARTY_ID": ship_to_customer.get('CustomerCode',''),
				"PARTY_NAME": ship_to_customer.get('FirstName',''),
				"PARTY_ROLE": "SHIP TO",
				"PHONE": ship_to_customer.get('BusinessPhone',''),
			}
			quote_involved_party_table_info.AddRow(shiptocustomer_quote_data)
		if quote_data.get("PayerID"):
			PayerDetails = {
				"QUOTE_INVOLVED_PARTY_RECORD_ID": str(Guid.NewGuid()).upper(),
				"ADDRESS": quote_data.get("PayerAddress"),
				"EMAIL": quote_data.get("PayerEmail"),
				"IS_MAIN": "1",
				"QUOTE_ID": self.contract_quote_data.get("QUOTE_ID"),
				"QUOTE_NAME": quote_data.get("STPAccountName"),
				"QUOTE_RECORD_ID": self.contract_quote_data.get("MASTER_TABLE_QUOTE_RECORD_ID"),
				"PARTY_ID": quote_data.get("PayerID"),
				"PARTY_NAME": quote_data.get("PayerName"),
				"PARTY_ROLE": "PAYER",
				"PHONE": quote_data.get("PayerPhone"),
			}
			quote_involved_party_table_info.AddRow(PayerDetails)
		if quote_data.get("SellerID"):
			SellerDetails = {
				"QUOTE_INVOLVED_PARTY_RECORD_ID": str(Guid.NewGuid()).upper(),
				"ADDRESS": quote_data.get("SellerAddress"),
				"EMAIL": quote_data.get("SellerEmail"),
				"IS_MAIN": "1",
				"QUOTE_ID": self.contract_quote_data.get("QUOTE_ID"),
				"QUOTE_NAME": quote_data.get("STPAccountName"),
				"QUOTE_RECORD_ID": self.contract_quote_data.get("MASTER_TABLE_QUOTE_RECORD_ID"),
				"PARTY_ID": quote_data.get("SellerID"),
				"PARTY_NAME": quote_data.get("SellerName"),
				"PARTY_ROLE": "SELLER",
				"PHONE": quote_data.get("SellerPhone"),
			}
			quote_involved_party_table_info.AddRow(SellerDetails)
		if quote_data.get("SalesUnitID"):
			SalesUnitDetails = {
				"QUOTE_INVOLVED_PARTY_RECORD_ID": str(Guid.NewGuid()).upper(),
				"ADDRESS": quote_data.get("SalesUnitAddress"),
				"EMAIL": quote_data.get("SalesUnitEmail"),
				"IS_MAIN": "1",
				"QUOTE_ID": self.contract_quote_data.get("QUOTE_ID"),
				"QUOTE_NAME": quote_data.get("STPAccountName"),
				"QUOTE_RECORD_ID": self.contract_quote_data.get("MASTER_TABLE_QUOTE_RECORD_ID"),
				"PARTY_ID": quote_data.get("SalesUnitID"),
				"PARTY_NAME": quote_data.get("SalesUnitName"),
				"PARTY_ROLE": "SALES UNIT",
				"PHONE": quote_data.get("SalesUnitPhone"),
			}
			quote_involved_party_table_info.AddRow(SalesUnitDetails)
		if quote_data.get("SalesEmployeeID"):
			SalesEmployeeDetails = {
				"QUOTE_INVOLVED_PARTY_RECORD_ID": str(Guid.NewGuid()).upper(),
				"ADDRESS": quote_data.get("SalesEmployeeAddress"),
				"EMAIL": quote_data.get("SalesEmployeeEmail"),
				"IS_MAIN": "1",
				"QUOTE_ID": self.contract_quote_data.get("QUOTE_ID"),
				"QUOTE_NAME": quote_data.get("STPAccountName"),
				"QUOTE_RECORD_ID": self.contract_quote_data.get("MASTER_TABLE_QUOTE_RECORD_ID"),
				"PARTY_ID": quote_data.get("SalesEmployeeID"),
				"PARTY_NAME": quote_data.get("SalesEmployeeName"),
				"PARTY_ROLE": "SALES EMPLOYEE",
				"PHONE": quote_data.get("SalesEmployeePhone"),
			}
			quote_involved_party_table_info.AddRow(SalesEmployeeDetails)
		if quote_data.get("EmployeeResponsibleID"):
			EmployeeResponsibleDetails = {
				"QUOTE_INVOLVED_PARTY_RECORD_ID": str(Guid.NewGuid()).upper(),
				"ADDRESS": quote_data.get("EmployeeResponsibleAddress"),
				"EMAIL": quote_data.get("EmployeeResponsibleEmail"),
				"IS_MAIN": "1",
				"QUOTE_ID": self.contract_quote_data.get("QUOTE_ID"),
				"QUOTE_NAME": quote_data.get("STPAccountName"),
				"QUOTE_RECORD_ID": self.contract_quote_data.get("MASTER_TABLE_QUOTE_RECORD_ID"),
				"PARTY_ID": quote_data.get("EmployeeResponsibleID"),
				"PARTY_NAME": quote_data.get("EmployeeResponsibleName"),
				"PARTY_ROLE": "EMPLOYEE RESPONSIBLE",
				"PHONE": quote_data.get("EmployeeResponsiblePhone"),
			}
			quote_involved_party_table_info.AddRow(EmployeeResponsibleDetails)
		if quote_data.get("ContractManagerID"):
			EmployeeResponsibleDetails = {
				"QUOTE_INVOLVED_PARTY_RECORD_ID": str(Guid.NewGuid()).upper(),
				"ADDRESS": quote_data.get("ContractManagerAddress"),
				"EMAIL": quote_data.get("ContractManagerEmail"),
				"IS_MAIN": "1",
				"QUOTE_ID": self.contract_quote_data.get("QUOTE_ID"),
				"QUOTE_NAME": quote_data.get("STPAccountName"),
				"QUOTE_RECORD_ID": self.contract_quote_data.get("MASTER_TABLE_QUOTE_RECORD_ID"),
				"PARTY_ID": quote_data.get("ContractManagerID"),
				"PARTY_NAME": quote_data.get("ContractManagerName"),
				"PARTY_ROLE": "CONTRACT MANAGER",
				"PHONE": quote_data.get("ContractManagerPhone"),
			}
			quote_involved_party_table_info.AddRow(EmployeeResponsibleDetails) 
		return quote_involved_party_table_info
	
	def _insert_quote_contract(self):
		cart_obj = Sql.GetFirst("SELECT CART_ID, USERID FROM CART WHERE ExternalId = '{}'".format(self.c4c_quote_id))
		if cart_obj:
			Sql.RunQuery("""INSERT INTO QT__QTQTMT (QUOTE_ID, QUOTE_NAME, MASTER_TABLE_QUOTE_RECORD_ID, ownerId, cartId) 
					VALUES 	(							
						'{QuoteId}',								
						'{QuoteName}',
						'{QuoteRecordId}',								
						{UserId},
						{CartId})""".format(
						CartId=cart_obj.CART_ID, UserId=cart_obj.USERID, 
						QuoteRecordId=self.contract_quote_data.get("MASTER_TABLE_QUOTE_RECORD_ID"),
						QuoteId=self.contract_quote_data.get("QUOTE_ID"),
						QuoteName=self.contract_quote_data.get("QUOTE_NAME")))
			return True
	
	def CreateEntitlements(self,quote_record_id):
		SAQTSVObj=Sql.GetList("Select * from SAQTSV (nolock) where QUOTE_RECORD_ID= '{QuoteRecordId}'".format(QuoteRecordId=quote_record_id))
		tableInfo = SqlHelper.GetTable("SAQTSE")
		x = datetime.today()
		x= str(x)
		y = x.split(" ")
		for OfferingRow_detail in SAQTSVObj:
			webclient = System.Net.WebClient()
			response=''
			webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/x-www-form-urlencoded"
			cps_credential_obj = SqlHelper.GetFirst("SELECT USER_NAME, PASSWORD, URL FROM SYCONF (NOLOCK) WHERE EXTERNAL_TABLE_NAME='CPS_VARIANT_PRICING'")
			if cps_credential_obj:
				response = webclient.DownloadString(cps_credential_obj.URL+'?grant_type=client_credentials&client_id='+cps_credential_obj.USER_NAME+'&client_secret='+cps_credential_obj.PASSWORD)
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
			attributevalues={}
			for rootattribute, rootvalue in Fullresponse.items():
				if rootattribute=="rootItem":
					for Productattribute, Productvalue in rootvalue.items():
						if Productattribute=="characteristics":
							for prdvalue in Productvalue:
								if prdvalue['visible'] =='false':
									attributesdisallowedlst.append(prdvalue['id'])
								else:
									attributesallowedlst.append(prdvalue['id'])
								if prdvalue['readOnly'] =='true':
									attributeReadonlylst.append(prdvalue['id'])
								for attribute in prdvalue['values']:
									attributevalues[str(prdvalue['id'])]=attribute['value']
			
			attributesallowedlst = list(set(attributesallowedlst))
			HasDefaultvalue=False
			ProductVersionObj=Sql.GetFirst("Select product_id from product_versions(nolock) where SAPKBVersion='"+str(Fullresponse['kbKey']['version'])+"'")
			if ProductVersionObj is not None:
				tbrow={}
				insertservice = ""
				for attrs in attributesallowedlst:
					if attrs in attributevalues:
						HasDefaultvalue=True
						STANDARD_ATTRIBUTE_VALUES=Sql.GetFirst("SELECT S.STANDARD_ATTRIBUTE_DISPLAY_VAL,S.STANDARD_ATTRIBUTE_CODE FROM STANDARD_ATTRIBUTE_VALUES (nolock) S INNER JOIN ATTRIBUTE_DEFN (NOLOCK) A ON A.STANDARD_ATTRIBUTE_CODE=S.STANDARD_ATTRIBUTE_CODE WHERE A.SYSTEM_ID = '{}' AND S.STANDARD_ATTRIBUTE_VALUE='{}'".format(attrs,attributevalues[attrs]))
					else:
						HasDefaultvalue=False
						STANDARD_ATTRIBUTE_VALUES=Sql.GetFirst("SELECT S.STANDARD_ATTRIBUTE_CODE FROM STANDARD_ATTRIBUTE_VALUES (nolock) S INNER JOIN ATTRIBUTE_DEFN (NOLOCK) A ON A.STANDARD_ATTRIBUTE_CODE=S.STANDARD_ATTRIBUTE_CODE WHERE A.SYSTEM_ID = '{}'".format(attrs))
					ATTRIBUTE_DEFN=Sql.GetFirst("SELECT * FROM ATTRIBUTE_DEFN (NOLOCK) WHERE SYSTEM_ID='{}'".format(attrs))
					PRODUCT_ATTRIBUTES=Sql.GetFirst("SELECT A.ATT_DISPLAY_DESC FROM ATT_DISPLAY_DEFN (NOLOCK) A INNER JOIN PRODUCT_ATTRIBUTES (NOLOCK) P ON A.ATT_DISPLAY=P.ATT_DISPLAY WHERE P.PRODUCT_ID={} AND P.STANDARD_ATTRIBUTE_CODE={}".format(ProductVersionObj.product_id,STANDARD_ATTRIBUTE_VALUES.STANDARD_ATTRIBUTE_CODE))
					DTypeset={"Drop Down":"DropDown","Free Input, no Matching":"FreeInputNoMatching","Check Box":"CheckBox"}
					#tbrow={}

					insertservice += """<QUOTE_ITEM_ENTITLEMENT>
					<ENTITLEMENT_NAME>{ent_name}</ENTITLEMENT_NAME>
					<ENTITLEMENT_VALUE_CODE>{}</ENTITLEMENT_VALUE_CODE>
					<ENTITLEMENT_TYPE>{}</ENTITLEMENT_TYPE>
					<ENTITLEMENT_DESCRIPTION>{}</ENTITLEMENT_DESCRIPTION>
					<ENTITLEMENT_DISPLAY_VALUE>{}</ENTITLEMENT_DISPLAY_VALUE>
					</QUOTE_ITEM_ENTITLEMENT>""".format(ent_name = str(attrs),ent_val_code = attributevalues[attrs] ,ent_type = DTypeset[PRODUCT_ATTRIBUTES.ATT_DISPLAY_DESC],ent_desc = ATTRIBUTE_DEFN.STANDARD_ATTRIBUTE_NAME,ent_disp_val = STANDARD_ATTRIBUTE_VALUES.STANDARD_ATTRIBUTE_DISPLAY_VAL )
					Log.Info('insertservice----'+str(insertservice))
					tbrow.append(insertservice)
					Log.Info('insertservice--tbrow--'+str(tbrow))
				tbrow["QUOTE_SERVICE_ENTITLEMENT_RECORD_ID"]=str(Guid.NewGuid()).upper()
				tbrow["QUOTE_ID"]=OfferingRow_detail.QUOTE_ID
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
				tbrow["IS_DEFAULT"] = '1'
				#inseryservice_ent = """INSERT SAQTSE () VALUES ()"""
				Log.Info('inseryservice_ent-----369--------'+str(tbrow))
				#Sql.RunQuery(inseryservice_ent)
				"""if PRODUCT_ATTRIBUTES is not None:
						Trace.Write("DType--"+DTypeset[PRODUCT_ATTRIBUTES.ATT_DISPLAY_DESC])
						tbrow["ENTITLEMENT_TYPE"]=DTypeset[PRODUCT_ATTRIBUTES.ATT_DISPLAY_DESC]
					tbrow["QUOTE_SERVICE_ENTITLEMENT_RECORD_ID"]=str(Guid.NewGuid()).upper()
					tbrow["QUOTE_ID"]=OfferingRow_detail.QUOTE_ID
					tbrow["QUOTE_NAME"]=OfferingRow_detail.QUOTE_NAME
					tbrow["QUOTE_RECORD_ID"]=OfferingRow_detail.QUOTE_RECORD_ID
					tbrow["QTESRV_RECORD_ID"]=OfferingRow_detail.QUOTE_SERVICE_RECORD_ID
					tbrow["SERVICE_RECORD_ID"]=OfferingRow_detail.SERVICE_RECORD_ID
					tbrow["SERVICE_ID"]=OfferingRow_detail.SERVICE_ID
					tbrow["SERVICE_DESCRIPTION"]=OfferingRow_detail.SERVICE_DESCRIPTION
					tbrow["ENTITLEMENT_NAME"]=str(attrs)
					tbrow["ENTITLEMENT_DESCRIPTION"]=ATTRIBUTE_DEFN.STANDARD_ATTRIBUTE_NAME
					tbrow["CPS_CONFIGURATION_ID"]=Fullresponse['id']
					#tbrow["ENTITLEMENT_TYPE"]=///DType
					tbrow["SALESORG_RECORD_ID"]=OfferingRow_detail.SALESORG_RECORD_ID
					tbrow["SALESORG_ID"]=OfferingRow_detail.SALESORG_ID
					tbrow["SALESORG_NAME"]=OfferingRow_detail.SALESORG_NAME
					tbrow["CPS_MATCH_ID"] = 11
					tbrow["IS_DEFAULT"] = '1'
					#tbrow["ENTITLEMENT_TYPE"]=
					if HasDefaultvalue==True:
						tbrow["ENTITLEMENT_DISPLAY_VALUE"]=STANDARD_ATTRIBUTE_VALUES.STANDARD_ATTRIBUTE_DISPLAY_VAL
						tbrow["ENTITLEMENT_VALUE_CODE"]=attributevalues[attrs]"""
					#else:
						#tbrow["ENTITLEMENT_DISPLAY_VALUE"]=""
						#tbrow["ENTITLEMENT_VALUE_CODE"]=""
					#tableInfo.AddRow(tbrow)
			#Sql.Upsert(tableInfo)

	def _insert_contract_related_table_records(self, quote_data):
		# CALLING IFLOW C4C_TO_CPQ_TOOLS            
		request_data = '{\n  \"OpportunityId\": \"'+str(quote_data.get("OpportunityId"))+'\",\n  \"QuoteId\": \"'+str(self.c4c_quote_id)+'\"\n}'        
		Log.Info("request_data ====>>>>>>> "+request_data)
		response = self._iflow_call(request_data, 'C4C_TO_CPQ_TOOLS', 'application/json') 
		Log.Info("request_data = response ====>>>>>>> "+response)
		payload_json_obj = Sql.GetFirst("SELECT INTEGRATION_PAYLOAD, CpqTableEntryId FROM SYINPL (NOLOCK) WHERE INTEGRATION_KEY = '{}' AND ISNULL(STATUS,'') = ''".format(self.contract_quote_data.get('C4C_QUOTE_ID')))
		if payload_json_obj:
			contract_quote_obj = None
			fab_location_ids, service_ids = [], []
			equipment_data = {}
			covered_object_data = {}
			payload_json = eval(payload_json_obj.INTEGRATION_PAYLOAD)
			payload_json = eval(payload_json.get('Param'))
			payload_json = payload_json.get('CPQ_Columns')
			if payload_json.get('OPPORTUNITY_ID'):
				contract_quote_obj = Sql.GetFirst("SELECT SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID, SAQTMT.QUOTE_ID, SAQTMT.QUOTE_NAME, SAQTMT.SALESORG_ID, SAQTMT.SALESORG_NAME, SAQTMT.SALESORG_RECORD_ID, SAQTMT.ACCOUNT_RECORD_ID FROM SAQTMT (NOLOCK) WHERE SAQTMT.C4C_QUOTE_ID = '{}'".format(self.contract_quote_data.get('C4C_QUOTE_ID')))
			if payload_json.get('FAB_LOCATION_IDS'):
				fab_location_ids = "','".join(list(set([str(int(fab_location)) for fab_location in payload_json.get('FAB_LOCATION_IDS').split(',') if fab_location])))		
			if payload_json.get('SERVICE_IDS'):	
				service_ids = "','".join(list(set(payload_json.get('SERVICE_IDS').split(','))))
			if payload_json.get('SAQFEQ'):
				for equipment_json_data in payload_json.get('SAQFEQ'):                        
					if equipment_json_data.get('FAB_LOCATION_ID') in equipment_data:
						equipment_data[equipment_json_data.get('FAB_LOCATION_ID')].append(equipment_json_data.get('EQUIPMENT_IDS'))
					else:
						equipment_data[equipment_json_data.get('FAB_LOCATION_ID')] = [equipment_json_data.get('EQUIPMENT_IDS')]
					
					if equipment_json_data.get('SERVICE_OFFERING_ID') in covered_object_data:
						covered_object_data[equipment_json_data.get('SERVICE_OFFERING_ID')].append(equipment_json_data.get('EQUIPMENT_IDS'))
					else:
						covered_object_data[equipment_json_data.get('SERVICE_OFFERING_ID')] = [equipment_json_data.get('EQUIPMENT_IDS')] 
			if contract_quote_obj and payload_json.get('SalesType') and payload_json.get('OpportunityType'):
				SalesType = {"Z14":"NEW","Z15":"CONTRACT RENEWAL","Z16":"CONTRACT EXTENSION","Z17":"CONTRACT AMENDMENT","Z18":"CONVERSION"}
				OpportunityType = {"23":"PROSPECT FOR PRODUCT SALES","24":"PROSPECT FOR SERVICE","25":"PROSPECT FOR TRAINING","26":"PROSPECT FOR CONSULTING","Z27":"FPM/EXE","Z28":"TKM","Z29":"POES","Z30":"LOW","Z31":"AGS"}
				Contract_child = "UPDATE SAQTMT SET SALE_TYPE = '{SalesType}',OPPORTUNITY_TYPE = '{OpportunityType}' WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{QuoteRecordId}' ".format(SalesType = SalesType.get(payload_json.get("SalesType")),OpportunityType = OpportunityType.get(payload_json.get("OpportunityType")),QuoteRecordId = contract_quote_obj.MASTER_TABLE_QUOTE_RECORD_ID)
				Sql.RunQuery(Contract_child)
				if quote_data.get("OpportunityId"):
					Opportunity_obj = "UPDATE SAOPPR SET SALE_TYPE = '{SalesType}',OPPORTUNITY_TYPE = '{OpportunityType}' where OPPORTUNITY_ID = '{OpportunityId}'".format(SalesType = SalesType.get(payload_json.get("SalesType")), OpportunityType = OpportunityType.get(payload_json.get("OpportunityType")),OpportunityId = quote_data.get("OpportunityId"))
					Sql.RunQuery(Opportunity_obj)
			Log.Info("fab_location_ids ===> "+str(fab_location_ids))
			Log.Info("service_ids ===> "+str(service_ids))
			Log.Info("equipment_data ===> "+str(equipment_data))				

			if contract_quote_obj:
				quote_record_id = contract_quote_obj.MASTER_TABLE_QUOTE_RECORD_ID
				quote_id = contract_quote_obj.QUOTE_ID
				if fab_location_ids:
					Log.Info("""
								INSERT
								SAQFBL (FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, QUOTE_ID, QUOTE_RECORD_ID, COUNTRY, COUNTRY_RECORD_ID, MNT_PLANT_ID, MNT_PLANT_NAME, MNT_PLANT_RECORD_ID, SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID, FABLOCATION_STATUS, ADDRESS_1, ADDRESS_2, CITY, STATE, STATE_RECORD_ID, QUOTE_FABLOCATION_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED)
								SELECT A.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_FABLOCATION_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED, {UserName} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
									SELECT DISTINCT FAB_LOCATION_ID, FAB_LOCATION_NAME, FAB_LOCATION_RECORD_ID, '{QuoteId}' as QUOTE_ID, '{QuoteRecordId}' as QUOTE_RECORD_ID, COUNTRY, COUNTRY_RECORD_ID, MNT_PLANT_ID, MNT_PLANT_RECORD_ID, SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID, STATUS, ADDRESS_1, ADDRESS_2, CITY, STATE, STATE_RECORD_ID FROM MAFBLC (NOLOCK)
									WHERE FAB_LOCATION_ID IN ('{FabLocationIds}')
									) A
								""".format(UserId=User.Id,UserName= User.UserName, QuoteId=quote_id, QuoteRecordId=quote_record_id, FabLocationIds=fab_location_ids))
					fab_insert = Sql.RunQuery("""
												INSERT
												SAQFBL (FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, QUOTE_ID, QUOTE_RECORD_ID, COUNTRY, COUNTRY_RECORD_ID, MNT_PLANT_ID, MNT_PLANT_NAME, MNT_PLANT_RECORD_ID, SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID, FABLOCATION_STATUS, ADDRESS_1, ADDRESS_2, CITY, STATE, STATE_RECORD_ID, QUOTE_FABLOCATION_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED)
												SELECT A.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_FABLOCATION_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED, {UserName} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
													SELECT DISTINCT FAB_LOCATION_ID, FAB_LOCATION_NAME, FAB_LOCATION_RECORD_ID, '{QuoteId}' as QUOTE_ID, '{QuoteRecordId}' as QUOTE_RECORD_ID, COUNTRY, COUNTRY_RECORD_ID, MNT_PLANT_ID, '' as MNT_PLANT_NAME, MNT_PLANT_RECORD_ID, SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID, STATUS, ADDRESS_1, ADDRESS_2, CITY, STATE, STATE_RECORD_ID FROM MAFBLC (NOLOCK)
													WHERE FAB_LOCATION_ID IN ('{FabLocationIds}')
													) A
												""".format(UserId=User.Id,UserName= User.UserName, QuoteId=quote_id, QuoteRecordId=quote_record_id, FabLocationIds=fab_location_ids))

				if service_ids:			
					Log.Info("""
								INSERT
								SAQTSV (QUOTE_ID, QUOTE_NAME, QUOTE_RECORD_ID, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, SERVICE_TYPE, SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID, QUOTE_SERVICE_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified)
								SELECT A.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED, {UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
									SELECT DISTINCT '{QuoteId}' as QUOTE_ID, '{QuoteName}' as QUOTE_NAME, '{QuoteRecordId}' as QUOTE_RECORD_ID, SAP_DESCRIPTION as SERVICE_DESCRIPTION, SAP_PART_NUMBER as SERVICE_ID, MATERIAL_RECORD_ID as SERVICE_RECORD_ID, '{SalesorgId}' as SALESORG_ID, '{SalesorgName}' as SALESORG_NAME, '{SalesorgRecordId}' as SALESORG_RECORD_ID, PRODUCT_TYPE FROM MAMTRL (NOLOCK)
									WHERE SAP_PART_NUMBER IN ('{ServiceIds}')
									) A
								""".format(UserId=User.Id, UserName=User.UserName, QuoteId=quote_id, QuoteName=contract_quote_obj.QUOTE_NAME, QuoteRecordId=quote_record_id, SalesorgId=contract_quote_obj.SALESORG_ID, SalesorgName=contract_quote_obj.SALESORG_NAME, SalesorgRecordId=contract_quote_obj.SALESORG_RECORD_ID, ServiceIds=service_ids))
					service_insert = Sql.RunQuery("""
													INSERT
													SAQTSV (QUOTE_ID, QUOTE_NAME, QUOTE_RECORD_ID, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, SERVICE_TYPE, SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID, QUOTE_SERVICE_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified)
													SELECT A.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED, {UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
														SELECT DISTINCT '{QuoteId}' as QUOTE_ID, 'QuoteName' as QUOTE_NAME, '{QuoteRecordId}' as QUOTE_RECORD_ID, SAP_DESCRIPTION as SERVICE_DESCRIPTION, SAP_PART_NUMBER as SERVICE_ID, MATERIAL_RECORD_ID as SERVICE_RECORD_ID, '{SalesorgId}' as SALESORG_ID, '{SalesorgName}' as SALESORG_NAME, '{SalesorgRecordId}' as SALESORG_RECORD_ID, PRODUCT_TYPE FROM MAMTRL (NOLOCK)
														WHERE SAP_PART_NUMBER IN ('{ServiceIds}')
														) A
													""".format(UserId=User.Id,UserName=User.UserName,QuoteId=quote_id, QuoteName=contract_quote_obj.QUOTE_NAME,QuoteRecordId=quote_record_id, SalesorgId=contract_quote_obj.SALESORG_ID, SalesorgName=contract_quote_obj.SALESORG_NAME, SalesorgRecordId=contract_quote_obj.SALESORG_RECORD_ID, ServiceIds=service_ids))	
					#service_ADDon = Sql.RunQuery(""" INSERT SAQSAO (QUOTE_SERVICE_ADD_ON_PRODUCT_RECORD_ID,ADNPRD_DESCRIPTION,ADNPRD_ID,ADNPRDOFR_RECORD_ID,ADNPRD_RECORD_ID,ADN_TYPE,QUOTE_ID,QUOTE_NAME,QUOTE_RECORD_ID,QTESRV_RECORD_ID,SALESORG_ID,SALESORG_NAME,ACTIVE,SALESORG_RECORD_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified) SELECT CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_ADD_ON_PRODUCT_RECORD_ID,MAADPR.ADNPRDOFR_NAME,MAADPR.ADNPRDOFR_ID,MAADPR.ADNPRDOFR_RECORD_ID,MAADPR.ADD_ON_PRODUCT_RECORD_ID,MAADPR.ADN_TYPE,SAQTSV.QUOTE_ID,SAQTSV.QUOTE_NAME,SAQTSV.QUOTE_RECORD_ID,SAQTSV.QUOTE_SERVICE_RECORD_ID,SAQTSV.SALESORG_ID,SAQTSV.SALESORG_NAME,'FALSE' as ACTIVE,SAQTSV.SALESORG_RECORD_ID,SAQTSV.SERVICE_DESCRIPTION,SAQTSV.SERVICE_ID,SAQTSV.SERVICE_RECORD_ID,'{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED, {UserId} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM MAADPR (NOLOCK) INNER JOIN  SAQTSV ON MAADPR.PRDOFR_ID = SAQTSV.SERVICE_ID WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND SERVICE_ID ='{ServiceIds}' """.format(UserId=User.Id,UserName=User.UserName,QuoteRecordId=quote_record_id,ServiceIds=service_ids))
					self.CreateEntitlements(quote_record_id)

				if equipment_data:
					count = 0
					for fab_location_id, value in equipment_data.items():
						if count == 0:
							Log.Info("""
										INSERT SAQFEQ
										(EQUIPMENT_DESCRIPTION, EQUIPMENT_ID, EQUIPMENT_RECORD_ID, FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, MNT_PLANT_ID, MNT_PLANT_NAME, MNT_PLANT_RECORD_ID, PLATFORM, QUOTE_ID, QUOTE_NAME, QUOTE_RECORD_ID, SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID, SERIAL_NUMBER, WAFER_SIZE, TECHNOLOGY, EQUIPMENTCATEGORY_ID, EQUIPMENTCATEGORY_RECORD_ID,EQUIPMENTCATEGORY_DESCRIPTION, EQUIPMENT_STATUS, PBG, WARRANTY_END_DATE, WARRANTY_START_DATE, CUSTOMER_TOOL_ID, GREENBOOK, GREENBOOK_RECORD_ID, QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED)
									SELECT A.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED, {UserName} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
										SELECT DISTINCT EQUIPMENT_DESCRIPTION, EQUIPMENT_ID, EQUIPMENT_RECORD_ID,  FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, MNT_PLANT_ID, '' as MNT_PLANT_NAME, MNT_PLANT_RECORD_ID, PLATFORM, '{QuoteId}' as QUOTE_ID, '{QuoteName}' as QUOTE_NAME, '{QuoteRecordId}' as QUOTE_RECORD_ID, SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID, SERIAL_NO, SUBSTRATE_SIZE, TECHNOLOGY, EQUIPMENTCATEGORY_ID, EQUIPMENTCATEGORY_RECORD_ID,EQUIPMENTCATEGORY_DESCRIPTION, EQUIPMENT_STATUS, PBG, WARRANTY_END_DATE, WARRANTY_START_DATE, CUSTOMER_TOOL_ID,  GREENBOOK, GREENBOOK_RECORD_ID FROM MAEQUP (NOLOCK)
										JOIN (SELECT NAME FROM SPLITSTRING('{EquipmentIds}'))B ON MAEQUP.EQUIPMENT_ID = NAME WHERE ISNULL(SERIAL_NO, '') <> '' AND FABLOCATION_ID = '{FabLocationId}'
										) A
									""".format(UserId=User.Id,UserName=User.UserName, QuoteId=quote_id, QuoteName=contract_quote_obj.QUOTE_NAME,QuoteRecordId=quote_record_id, FabLocationId=fab_location_id, EquipmentIds=",".join(value)))
						
						count += 1
						equipment_insert = Sql.RunQuery("""
														INSERT SAQFEQ
														(EQUIPMENT_DESCRIPTION, EQUIPMENT_ID, EQUIPMENT_RECORD_ID, FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, MNT_PLANT_ID, MNT_PLANT_NAME, MNT_PLANT_RECORD_ID, PLATFORM, QUOTE_ID, QUOTE_NAME, QUOTE_RECORD_ID, SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID, SERIAL_NUMBER, WAFER_SIZE, TECHNOLOGY, EQUIPMENTCATEGORY_ID, EQUIPMENTCATEGORY_RECORD_ID,EQUIPMENTCATEGORY_DESCRIPTION, EQUIPMENT_STATUS, PBG, WARRANTY_END_DATE, WARRANTY_START_DATE, CUSTOMER_TOOL_ID, GREENBOOK, GREENBOOK_RECORD_ID, QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED)
													SELECT A.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID, '{UserName}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED, {UserName} as CpqTableEntryModifiedBy, GETDATE() as CpqTableEntryDateModified FROM (
														SELECT DISTINCT EQUIPMENT_DESCRIPTION, EQUIPMENT_ID, EQUIPMENT_RECORD_ID,  FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, MNT_PLANT_ID, '' as MNT_PLANT_NAME, MNT_PLANT_RECORD_ID, PLATFORM, '{QuoteId}' as QUOTE_ID, '{QuoteName}' as QUOTE_NAME, '{QuoteRecordId}' as QUOTE_RECORD_ID, SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID, SERIAL_NO, SUBSTRATE_SIZE, TECHNOLOGY, EQUIPMENTCATEGORY_ID, EQUIPMENTCATEGORY_RECORD_ID, EQUIPMENTCATEGORY_DESCRIPTION, EQUIPMENT_STATUS, PBG, WARRANTY_END_DATE, WARRANTY_START_DATE, CUSTOMER_TOOL_ID,  GREENBOOK, GREENBOOK_RECORD_ID FROM MAEQUP (NOLOCK)
														JOIN (SELECT NAME FROM SPLITSTRING('{EquipmentIds}'))B ON MAEQUP.EQUIPMENT_ID = NAME WHERE ISNULL(SERIAL_NO, '') <> '' AND FABLOCATION_ID = '{FabLocationId}'
														) A
													""".format(UserId=User.Id,UserName=User.UserName,QuoteId=quote_id, QuoteName=contract_quote_obj.QUOTE_NAME,QuoteRecordId=quote_record_id, FabLocationId=fab_location_id, EquipmentIds=",".join(value)))
					
					
					Log.Info("""
							INSERT SAQFEA
							(ASSEMBLY_DESCRIPTION, ASSEMBLY_ID, ASSEMBLY_RECORD_ID, EQUIPMENTCATEGORY_ID, EQUIPMENTCATEGORY_RECORD_ID, EQUIPMENT_DESCRIPTION, EQUIPMENT_ID, EQUIPMENT_RECORD_ID,
							FABLOCATION_ID,
							FABLOCATION_NAME, FABLOCATION_RECORD_ID, GOT_CODE, MNT_PLANT_ID, MNT_PLANT_RECORD_ID, QUOTE_ID, QUOTE_NAME, QUOTE_RECORD_ID, SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID, SERIAL_NUMBER, WARRANTY_END_DATE, WARRANTY_START_DATE, SUBSTRATE_SIZE, ASSEMBLY_STATUS, QUOTE_FAB_LOC_COV_OBJ_ASSEMBLY_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED)
						SELECT A.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_FAB_LOC_COV_OBJ_ASSEMBLY_RECORD_ID, {UserId} as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM (
							SELECT DISTINCT MAEQUP.EQUIPMENT_DESCRIPTION as ASSEMBLY_DESCRIPTION, MAEQUP.EQUIPMENT_ID as ASSEMBLY_ID, MAEQUP.EQUIPMENT_RECORD_ID as ASSEMBLY_RECORD_ID, MAEQUP.EQUIPMENTCATEGORY_ID, MAEQUP.EQUIPMENTCATEGORY_RECORD_ID, SAQFEQ.EQUIPMENT_DESCRIPTION, SAQFEQ.EQUIPMENT_ID, SAQFEQ.EQUIPMENT_RECORD_ID, SAQFEQ.FABLOCATION_ID, SAQFEQ.FABLOCATION_NAME, SAQFEQ.FABLOCATION_RECORD_ID, MAEQUP.GOT_CODE, MAEQUP.MNT_PLANT_ID, MAEQUP.MNT_PLANT_RECORD_ID, '{QuoteId}' as QUOTE_ID, '{QuoteName}' as QUOTE_NAME, '{QuoteRecordId}' as QUOTE_RECORD_ID, SAQFEQ.SALESORG_ID, SAQFEQ.SALESORG_NAME, SAQFEQ.SALESORG_RECORD_ID, MAEQUP.SERIAL_NO as SERIAL_NUMBER, MAEQUP.WARRANTY_END_DATE, MAEQUP.WARRANTY_START_DATE, MAEQUP.SUBSTRATE_SIZE, MAEQUP.EQUIPMENT_STATUS as ASSEMBLY_STATUS FROM SAQFEQ (NOLOCK) JOIN MAEQUP (NOLOCK) ON MAEQUP.PAR_EQUIPMENT_ID = SAQFEQ.EQUIPMENT_ID AND MAEQUP.FABLOCATION_ID = SAQFEQ.FABLOCATION_ID AND MAEQUP.SALESORG_RECORD_ID = SAQFEQ.SALESORG_RECORD_ID
							WHERE MAEQUP.ACCOUNT_RECORD_ID = '{AccountRecordId}' AND ISNULL(MAEQUP.SERIAL_NO, '') = '' AND SAQFEQ.QUOTE_RECORD_ID = '{QuoteRecordId}'
							) A
						""".format(UserId=User.Id,QuoteId=quote_id, QuoteName=contract_quote_obj.QUOTE_NAME, QuoteRecordId=quote_record_id, AccountRecordId=contract_quote_obj.ACCOUNT_RECORD_ID))
					equipment_assembly_insert = Sql.RunQuery("""
														INSERT SAQFEA
														(ASSEMBLY_DESCRIPTION, ASSEMBLY_ID, ASSEMBLY_RECORD_ID, EQUIPMENTCATEGORY_ID, EQUIPMENTTYPE_ID, EQUIPMENTCATEGORY_RECORD_ID, EQUIPMENT_DESCRIPTION, EQUIPMENT_ID, EQUIPMENT_RECORD_ID, FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, GOT_CODE, MNT_PLANT_ID, MNT_PLANT_RECORD_ID, QUOTE_ID, QUOTE_NAME, QUOTE_RECORD_ID, SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID, SERIAL_NUMBER, WARRANTY_END_DATE, WARRANTY_START_DATE, SUBSTRATE_SIZE, ASSEMBLY_STATUS, QUOTE_FAB_LOC_COV_OBJ_ASSEMBLY_RECORD_ID, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED)
													SELECT A.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_FAB_LOC_COV_OBJ_ASSEMBLY_RECORD_ID, {UserId} as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM (
														SELECT DISTINCT MAEQUP.EQUIPMENT_DESCRIPTION as ASSEMBLY_DESCRIPTION, MAEQUP.EQUIPMENT_ID as ASSEMBLY_ID, MAEQUP.EQUIPMENT_RECORD_ID as ASSEMBLY_RECORD_ID, MAEQUP.EQUIPMENTCATEGORY_ID, MAEQUP.EQUIPMENTTYPE_ID,  MAEQUP.EQUIPMENTCATEGORY_RECORD_ID, SAQFEQ.EQUIPMENT_DESCRIPTION, SAQFEQ.EQUIPMENT_ID, SAQFEQ.EQUIPMENT_RECORD_ID, SAQFEQ.FABLOCATION_ID, SAQFEQ.FABLOCATION_NAME, SAQFEQ.FABLOCATION_RECORD_ID, MAEQUP.GOT_CODE, MAEQUP.MNT_PLANT_ID, MAEQUP.MNT_PLANT_RECORD_ID, '{QuoteId}' as QUOTE_ID, '{QuoteName}' as QUOTE_NAME, '{QuoteRecordId}' as QUOTE_RECORD_ID, SAQFEQ.SALESORG_ID, SAQFEQ.SALESORG_NAME, SAQFEQ.SALESORG_RECORD_ID, MAEQUP.SERIAL_NO as SERIAL_NUMBER, MAEQUP.WARRANTY_END_DATE, MAEQUP.WARRANTY_START_DATE, MAEQUP.SUBSTRATE_SIZE, MAEQUP.EQUIPMENT_STATUS as ASSEMBLY_STATUS FROM SAQFEQ (NOLOCK) JOIN MAEQUP (NOLOCK) ON MAEQUP.PAR_EQUIPMENT_ID = SAQFEQ.EQUIPMENT_ID AND MAEQUP.FABLOCATION_ID = SAQFEQ.FABLOCATION_ID AND MAEQUP.SALESORG_RECORD_ID = SAQFEQ.SALESORG_RECORD_ID
														WHERE MAEQUP.ACCOUNT_RECORD_ID = '{AccountRecordId}' AND ISNULL(MAEQUP.SERIAL_NO, '') = '' AND SAQFEQ.QUOTE_RECORD_ID = '{QuoteRecordId}'
														) A
													""".format(UserId=User.Id,QuoteId=quote_id, QuoteName=contract_quote_obj.QUOTE_NAME, QuoteRecordId=quote_record_id, AccountRecordId=contract_quote_obj.ACCOUNT_RECORD_ID))
					if  payload_json.get('SalesType') == 'Z15':
						Log.Info("covered_object_data ===> "+str(covered_object_data))
						for service_id, equipment_values in covered_object_data.items():
							equipment_ids = ','.join(list(set(','.join(equipment_values).split(','))))
							Log.Info("===>>>>>>>> "+str("""SELECT STUFF((SELECT ', ' + SAQFEQ.QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID 
														FROM SAQFEQ
														JOIN (SELECT NAME FROM SPLITSTRING('{EquipmentIds}'))B ON SAQFEQ.EQUIPMENT_ID = NAME
														WHERE SAQFEQ.QUOTE_RECORD_ID = '{QuoteRecordId}'
														FOR XML PATH('')), 1, 1, '') as RECORD_IDS """.format(QuoteRecordId=quote_record_id,EquipmentIds=equipment_ids)))
							fab_equipments_obj = Sql.GetFirst("""SELECT STUFF((SELECT ', ' + SAQFEQ.QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID 
														FROM SAQFEQ
														JOIN (SELECT NAME FROM SPLITSTRING('{EquipmentIds}'))B ON SAQFEQ.EQUIPMENT_ID = NAME
														WHERE SAQFEQ.QUOTE_RECORD_ID = '{QuoteRecordId}'
														FOR XML PATH('')), 1, 1, '') as RECORD_IDS """.format(QuoteRecordId=quote_record_id,EquipmentIds=equipment_ids))
							if fab_equipments_obj:
								if fab_equipments_obj.RECORD_IDS:
									fab_equipment_record_ids = fab_equipments_obj.RECORD_IDS.split(',')
									quote_service_obj = Sql.GetFirst("select SERVICE_TYPE from SAQTSV (NOLOCK) where SERVICE_ID = '{Service_Id}' and QUOTE_RECORD_ID = '{QuoteRecordId}'".format(Service_Id = equipment_json_data.get('SERVICE_OFFERING_ID'),QuoteRecordId=quote_record_id))
									Log.Info("fab_equipment_record_ids ===> "+str(fab_equipment_record_ids))							
									service_type = quote_service_obj.SERVICE_TYPE											
									Product.SetGlobal("contract_quote_record_id",str(quote_record_id))
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
															"TriggerFrom"  : "PythonScript",
															"Values"	  : fab_equipment_record_ids,
															"ServiceId"  : service_id,
															"ServiceType" : service_type,
														},
													)
									end_time = time.time()
									Log.Info("CQCRUDOPTN end==> "+str(end_time - start_time))                        
			payload_table_info = Sql.GetTable("SYINPL")
			payload_table_data = {'CpqTableEntryId':payload_json_obj.CpqTableEntryId, 'STATUS':'COMPLETED'}
			payload_table_info.AddRow(payload_table_data)
			Sql.Upsert(payload_table_info)
		
	@staticmethod
	def get_formatted_date(date_string):
		if date_string:
			return datetime.strptime(date_string, '%Y-%m-%d').strftime('%m/%d/%Y')
		return ''
	
	def _insert_custom_table_records(self, c4c_quote_details):

		quote_table_info = Sql.GetTable("SAQTMT")

		quote_data = {}
		sales_quote_details = c4c_quote_details.get('SalesQuoteDetails')
		if sales_quote_details:
			header = sales_quote_details.get('Header')
			for key, value in header.items():
				if key == 'CustomFields':
					quote_data.update(self.process_custom_field(value))
				else:
					quote_data[key] = value
			quote_data['BillTo'] = sales_quote_details.get('BillTo')
			quote_data['ShipTo'] = sales_quote_details.get('ShipTo')
		if quote_data:            
			Log.Info("===> quote_data"+str(quote_data))
			start_date = quote_data.get('QuoteStartDate')            
			start_date = self.get_formatted_date(start_date)
			end_date = quote_data.get('QuoteExpirationDate') 
			Log.Info("===> CONTRACT_VALID_TO"+str(end_date))           
			end_date = self.get_formatted_date(end_date)

			pricing_date = quote_data.get('PricingDate')
			pricing_date = self.get_formatted_date(pricing_date)

			self.cpq_quote_id = "SQ{}RV00-RW00AM00-{}".format(
					self.c4c_quote_id,
					datetime.strptime(quote_data.get('QuoteExpirationDate'), '%Y-%m-%d').strftime('%y%m%d')					
				)
			
			if quote_data.get("SalesOrgID"):
				salesorg_obj = Sql.GetFirst(
					"SELECT SALES_ORG_RECORD_ID, SALESORG_NAME FROM SASORG (NOLOCK) WHERE SALESORG_ID = '{}'".format(
						quote_data.get("SalesOrgID")
					)
				)
				if salesorg_obj:
					self.contract_quote_data.update(
						{
							"SALESORG_RECORD_ID": salesorg_obj.SALES_ORG_RECORD_ID,
							"SALESORG_NAME": salesorg_obj.SALESORG_NAME,
						}
					)
			
			if quote_data.get("PaymentTerms"):
				payterm_obj = Sql.GetFirst(
					"SELECT PAYMENT_TERM_ID, PAYMENT_TERM_NAME, PAYMENT_TERM_RECORD_ID FROM PRPTRM (NOLOCK) WHERE PAYMENT_TERM_ID = '{}'".format(
						quote_data.get("PaymentTerms")
					)
				)
				if payterm_obj:
					self.contract_quote_data.update(
						{
							"PAYMENTTERM_ID": payterm_obj.PAYMENT_TERM_ID,
							"PAYMENTTERM_NAME": payterm_obj.PAYMENT_TERM_NAME,
							"PAYMENTTERM_RECORD_ID": payterm_obj.PAYMENT_TERM_RECORD_ID,
						}
					)
			
			self.contract_quote_data.update(
				{
					"QUOTE_ID": self.cpq_quote_id,
					"C4C_QUOTE_ID": self.c4c_quote_id,
					"MASTER_TABLE_QUOTE_RECORD_ID": str(Guid.NewGuid()).upper(),
					"REGION": quote_data.get("Region"),
					"SALESORG_ID": quote_data.get("SalesOrgID"),
					"SALE_TYPE": "NEW",
					"CANCELLATION_PERIOD":"90 DAYS",
					"DOCUMENT_TYPE": self.document_type.get(quote_data.get('DocumentTypeCode')),
					"OPPORTUNITY_TYPE": self.opportunity_type.get(quote_data.get("ContractType")),
					"QUOTE_STATUS": "IN-PROGRESS",
					"QUOTE_LEVEL": quote_data.get("QuoteLevel") if quote_data.get("QuoteLevel") else "SALES ORG LEVEL",
					"CONTRACT_VALID_FROM": start_date,
					"CONTRACT_VALID_TO": end_date,
					"OPPORTUNITY_ID": quote_data.get("OpportunityId"),
					"QUOTE_NAME": quote_data.get("STPAccountName"),
					"EMPLOYEE_ID": quote_data.get("SalesPerson"),
					"SOURCE_CONTRACT_ID": quote_data.get("SourceContractID"),
					
					"QUOTE_CURRENCY":quote_data.get("Currency"),
					"INCOTERMS":quote_data.get("Incoterms"),
					"INCOTERMS_NOTES":quote_data.get("IncotermsLocation"),
					"PRICING_DATE":pricing_date,
					"EXCHANGE_RATE_TYPE":quote_data.get("ExchangeRateType"),
				}
			)
			#"QUOTE_TYPE":self.quote_type.get(quote_data.get("ContractType")),
			if quote_data.get('Currency'):
				Currency_obj = Sql.GetFirst(
					"SELECT CURRENCY,CURRENCY_NAME, CURRENCY_RECORD_ID FROM PRCURR (NOLOCK) WHERE CURRENCY = '{}'".format(
						quote_data.get('Currency')
					)
				)
				if Currency_obj:
					self.contract_quote_data.update({"QUOTE_CURRENCY":Currency_obj.CURRENCY , 
										"QUOTE_CURRENCY_RECORD_ID":Currency_obj.CURRENCY_RECORD_ID})
			
			quote_salesorg_table_info = self._insert_quote_salesorg(quote_data)
			quote_opportunity_table_info = self._insert_opportunity_and_quote_opportunity(quote_data)
			quote_involved_party_table_info = self._insert_quote_involved_parties(quote_data)

			quote_table_info.AddRow(self.contract_quote_data)
			Sql.Upsert(quote_table_info)
			Sql.Upsert(quote_salesorg_table_info)
			Sql.Upsert(quote_opportunity_table_info)
			Sql.Upsert(quote_involved_party_table_info)

			self._insert_quote_contract()
			Log.Info("XXX*********************************************************************************")
			self._insert_contract_related_table_records(quote_data)
		return True
		
	def sync_c4c_quote(self):
		if self.c4c_opportunity_id:
			#webRequest = HttpWebRequest.Create("https://my347401.crm.ondemand.com/sap/c4c/odata/v1/cpquote/QuoteCollection/?$format=json&$filter=ExternalSystemID eq 'CPQ_TST' and ID eq '{}'".format(self.c4c_quote_id))
			
			iflow_url = "https://my347401.crm.ondemand.com/sap/c4c/odata/cust/v1/opptooltocpq/OpportunityCollection/?$format=json&$filter=ID eq '{}'".format(self.c4c_opportunity_id)
			Log.Info("====> iflow_url "+str(iflow_url))
			webRequest = HttpWebRequest.Create(iflow_url)

			authorization = "X0116946" + ":" + "Bajib@20201"
			binaryAuthorization = UTF8.GetBytes(authorization)
			authorization = Convert.ToBase64String(binaryAuthorization)
			authorization = "Basic " + authorization
			webRequest.Headers.Add("AUTHORIZATION", authorization)

			webRequest.Method = 'GET'
			webRequest.ContentType = 'application/json'
			webRequest.ContentLength = 0

			response = webRequest.GetResponse()
			streamReader = StreamReader(response.GetResponseStream())
			jsonData = streamReader.ReadToEnd()

			Log.Info("===> "+str(jsonData))
			if jsonData:
				quote_id_response = eval(jsonData)
				response_result = quote_id_response.get('d').get('results')[0]
				Log.Info("====>>><<><><<>"+str(response_result.get('ZAMAT_CurrentRefQuoteIDcontent_SDK')))
				self.c4c_quote_id = int(response_result.get('ZAMAT_CurrentRefQuoteIDcontent_SDK')) if response_result.get('ZAMAT_CurrentRefQuoteIDcontent_SDK') else None
				self.contract_quote_data.update({'QUOTE_TYPE':self.quote_type.get(response_result.get('ZContractType_KUT'))})
			Log.Info("===>>>>>>>>>>>>>>>>>>CCCC "+str(self.c4c_quote_id))
			if self.c4c_quote_id:
				contract_quote_obj = Sql.GetFirst("SELECT * FROM SAQTMT (NOLOCK) WHERE C4C_QUOTE_ID = '{}'".format(self.c4c_quote_id))
				if contract_quote_obj:
					#Quote=QuoteHelper.Edit(self.c4c_quote_id)                    
					#if Quote.CompositeNumber == '01340018':
					return (contract_quote_obj.QUOTE_ID, contract_quote_obj.MASTER_TABLE_QUOTE_RECORD_ID)
				else:
					#quote = 3050008002
					#Log.Info("===>>>>>>>>>>>>>>>>>>dddddd "+str(self.c4c_quote_id))
					c4c_quote_details = self._get_c4c_quote_details()
					Log.Info("c4c_quote_details ===> "+str(c4c_quote_details))
					cpq_quote_creation_response = self._create_cpq_native_quote()
					Log.Info("===>>>>>>>>>>>>>>>>>>dddddd "+str(cpq_quote_creation_response))
					#dit = jsonData.Key
					self._insert_custom_table_records(c4c_quote_details)
					#conv_data = jsonData.replace("'",'%%').replace("false",'"false"').replace("null",'"null"')
					#Dict = eval(conv_data) 
					
					Log.Info("self.contract_quote_data ===> "+str(self.contract_quote_data))
					return (self.contract_quote_data.get('QUOTE_ID'), self.contract_quote_data.get('MASTER_TABLE_QUOTE_RECORD_ID'))

try:
	c4c_opportunity_id = Param.C4COpportunityId
except:
	c4c_opportunity_id = ''
try:
	c4c_quote_id = Param.C4CQuoteId
except:
	c4c_quote_id = ''

Log.Info("c4c_opportunity_id ==> "+str(c4c_opportunity_id))
sync_obj = ContractQuoteC4CSync(c4c_opportunity_id=c4c_opportunity_id, c4c_quote_id=c4c_quote_id)
ApiResponse = ApiResponseFactory.JsonResponse(sync_obj.sync_c4c_quote())
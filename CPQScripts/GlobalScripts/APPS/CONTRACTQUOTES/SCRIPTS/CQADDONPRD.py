# =========================================================================================================================================
#   __script_name : CQADDONPRD.PY
#   __script_description : TO INSERT THE SAQTSE AND SAQSGE TABLE INSERT WHILE ADDING ADD ON PRODUCTS.
#   __primary_author__ : GAYATHRI AMARESAN
#   __create_date :08-12-2021
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
from SYDATABASE import SQL
Sql = SQL()
import sys
import datetime
User_name = ScriptExecutor.ExecuteGlobal("SYUSDETAIL", "USERNAME")
User_Id = ScriptExecutor.ExecuteGlobal("SYUSDETAIL", "USERID")
def addon_service_level_entitlement(OfferingRow_detail,greenbook):
	Request_URL="https://cpservices-product-configuration.cfapps.us10.hana.ondemand.com/api/v2/configurations?autoCleanup=False"
						
	Fullresponse = ScriptExecutor.ExecuteGlobal("CQENTLNVAL", {'action':'GET_RESPONSE','partnumber':OfferingRow_detail.SERVICE_ID,'request_url':Request_URL,'request_type':"New"})
	Fullresponse=str(Fullresponse).replace(": true",": \"true\"").replace(": false",": \"false\"")
	Fullresponse= eval(Fullresponse)
	##getting configuration_status status
	if Fullresponse['complete'] == 'true':
		configuration_status = 'COMPLETE'
	elif Fullresponse['complete'] == 'false':
		configuration_status = 'INCOMPLETE'
	else:
		configuration_status = 'ERROR'
	attributesdisallowedlst=[]
	attributeReadonlylst=[]
	attributesallowedlst=[]
	attributedefaultvalue = []
	overall_att_list_sub =[]
	overallattributeslist =[]
	attributevalues={}
	get_toolptip= ''
	#getquote_sales_val = AttributeID_Pass = ''
	for rootattribute, rootvalue in Fullresponse.items():
		if rootattribute=="rootItem":
			for Productattribute, Productvalue in rootvalue.items():
				if Productattribute=="characteristics":
					for prdvalue in Productvalue:
						overallattributeslist.append(prdvalue['id'])
						if prdvalue['id'].startswith('AGS_Z0046_'):
							overall_att_list_sub.append(prdvalue['id'])
						if prdvalue['visible'] =='false':
							attributesdisallowedlst.append(prdvalue['id'])
						else:								
							attributesallowedlst.append(prdvalue['id'])
						if prdvalue['readOnly'] =='true':
							attributeReadonlylst.append(prdvalue['id'])
						for attribute in prdvalue['values']:								
							attributevalues[str(prdvalue['id'])]=attribute['value']
							if attribute["author"] in ('Default','System'):
								#Trace.Write('prdvalue---1554-----'+str(prdvalue['id']))
								attributedefaultvalue.append(prdvalue["id"])
	attributesallowedlst = list(set(attributesallowedlst))
	overallattributeslist = list(set(overallattributeslist))		
	HasDefaultvalue=False

	ProductVersionObj=Sql.GetFirst("Select product_id from product_versions(nolock) where SAPKBId = '"+str(Fullresponse['kbId'])+"' AND SAPKBVersion='"+str(Fullresponse['kbKey']['version'])+"'")

	is_default = ent_val_code = ''
	AttributeID_Pass =""
	get_toolptip = ""

	if ProductVersionObj:
		insertservice = ""
		tbrow={}	
		for attrs in overallattributeslist:
			
			if attrs in attributevalues:					
				HasDefaultvalue=True					
				STANDARD_ATTRIBUTE_VALUES=Sql.GetFirst("SELECT S.STANDARD_ATTRIBUTE_DISPLAY_VAL,S.STANDARD_ATTRIBUTE_CODE FROM STANDARD_ATTRIBUTE_VALUES (nolock) S INNER JOIN ATTRIBUTE_DEFN (NOLOCK) A ON A.STANDARD_ATTRIBUTE_CODE=S.STANDARD_ATTRIBUTE_CODE WHERE A.SYSTEM_ID = '{}' ".format(attrs))
				ent_disp_val = attributevalues[attrs]
				ent_val_code = attributevalues[attrs]
				#Trace.Write("ent_disp_val----"+str(ent_disp_val))
			else:					
				HasDefaultvalue=False
				ent_disp_val = ""
				ent_val_code = ""
				STANDARD_ATTRIBUTE_VALUES=Sql.GetFirst("SELECT S.STANDARD_ATTRIBUTE_CODE FROM STANDARD_ATTRIBUTE_VALUES (nolock) S INNER JOIN ATTRIBUTE_DEFN (NOLOCK) A ON A.STANDARD_ATTRIBUTE_CODE=S.STANDARD_ATTRIBUTE_CODE WHERE A.SYSTEM_ID = '{}'".format(attrs))
				
			ATTRIBUTE_DEFN=Sql.GetFirst("SELECT * FROM ATTRIBUTE_DEFN (NOLOCK) WHERE SYSTEM_ID='{}'".format(attrs))
			PRODUCT_ATTRIBUTES=Sql.GetFirst("SELECT A.ATT_DISPLAY_DESC,P.ATTRDESC FROM ATT_DISPLAY_DEFN (NOLOCK) A INNER JOIN PRODUCT_ATTRIBUTES (NOLOCK) P ON A.ATT_DISPLAY=P.ATT_DISPLAY WHERE P.PRODUCT_ID={} AND P.STANDARD_ATTRIBUTE_CODE={}".format(ProductVersionObj.product_id,STANDARD_ATTRIBUTE_VALUES.STANDARD_ATTRIBUTE_CODE))
			if PRODUCT_ATTRIBUTES:
				if PRODUCT_ATTRIBUTES.ATTRDESC:
					get_toolptip = PRODUCT_ATTRIBUTES.ATTRDESC
			if PRODUCT_ATTRIBUTES.ATT_DISPLAY_DESC in ('Drop Down','Check Box') and ent_disp_val:
				get_display_val = Sql.GetFirst("SELECT STANDARD_ATTRIBUTE_DISPLAY_VAL  from STANDARD_ATTRIBUTE_VALUES S INNER JOIN ATTRIBUTE_DEFN (NOLOCK) A ON A.STANDARD_ATTRIBUTE_CODE=S.STANDARD_ATTRIBUTE_CODE WHERE S.STANDARD_ATTRIBUTE_CODE = '{}' AND A.SYSTEM_ID = '{}' AND S.STANDARD_ATTRIBUTE_VALUE = '{}' ".format(STANDARD_ATTRIBUTE_VALUES.STANDARD_ATTRIBUTE_CODE,attrs,  attributevalues[attrs] ) )
				ent_disp_val = get_display_val.STANDARD_ATTRIBUTE_DISPLAY_VAL 
			getslaes_value  = Sql.GetFirst("SELECT SALESORG_ID FROM SAQTRV WHERE QUOTE_RECORD_ID = '"+str(OfferingRow_detail.QUOTE_RECORD_ID)+"'")
			if getslaes_value:
				getquote_sales_val = getslaes_value.SALESORG_ID
			get_il_sales = Sql.GetList("select SALESORG_ID from SASORG where country = 'IL'")
			get_il_sales_list = [val.SALESORG_ID for val in get_il_sales]
			
			
			
			#A055S000P01-7401 START
			if str(attrs) in ('AGS_POA_PROD_TYPE','AGS_{}_GEN_POAPDT'.format(OfferingRow_detail.ADNPRD_ID) ) and ent_disp_val != '':
				val = ""
				if str(ent_disp_val) == 'Comprehensive':
					val = "COMPREHENSIVE SERVICES"
				elif str(ent_disp_val) == 'Complementary':
					val = "COMPLEMENTARY PRODUCTS"
				Sql.RunQuery("UPDATE SAQTSV SET SERVICE_TYPE = '{}' WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID = '{}'".format(str(val),self.contract_quote_record_id,self.quote_revision_record_id,OfferingRow_detail.ADNPRD_ID))
			#A055S000P01-7401 END
			DTypeset={"Drop Down":"DropDown","Free Input, no Matching":"FreeInputNoMatching","Check Box":"CheckBox"}
			insertservice += """<QUOTE_ITEM_ENTITLEMENT>
				<ENTITLEMENT_ID>{ent_name}</ENTITLEMENT_ID>
				<ENTITLEMENT_VALUE_CODE>{ent_val_code}</ENTITLEMENT_VALUE_CODE>
				<ENTITLEMENT_DESCRIPTION>{tool_desc}</ENTITLEMENT_DESCRIPTION>
				<ENTITLEMENT_TYPE>{ent_type}</ENTITLEMENT_TYPE>
				<ENTITLEMENT_DISPLAY_VALUE>{ent_disp_val}</ENTITLEMENT_DISPLAY_VALUE>
				<ENTITLEMENT_COST_IMPACT>{ct}</ENTITLEMENT_COST_IMPACT>
				<ENTITLEMENT_PRICE_IMPACT>{pi}</ENTITLEMENT_PRICE_IMPACT>
				<IS_DEFAULT>{is_default}</IS_DEFAULT>
				<PRICE_METHOD>{pm}</PRICE_METHOD>
				<CALCULATION_FACTOR>{cf}</CALCULATION_FACTOR>
				<ENTITLEMENT_NAME>{ent_desc}</ENTITLEMENT_NAME>
				</QUOTE_ITEM_ENTITLEMENT>""".format(ent_name = str(attrs),ent_val_code = ent_val_code,ent_type = DTypeset[PRODUCT_ATTRIBUTES.ATT_DISPLAY_DESC] if PRODUCT_ATTRIBUTES else  '',ent_desc = ATTRIBUTE_DEFN.STANDARD_ATTRIBUTE_NAME,ent_disp_val = ent_disp_val if HasDefaultvalue==True else '',ct = '',pi = '',is_default = '1' if str(attrs) in attributedefaultvalue else '0',pm = '',cf = '',tool_desc = get_toolptip.replace("'","''") if "'" in get_toolptip else get_toolptip)
		insertservice = insertservice.encode('ascii', 'ignore').decode('ascii')
		
		tbrow["QUOTE_SERVICE_ENTITLEMENT_RECORD_ID"]=str(Guid.NewGuid()).upper()
		tbrow["QUOTE_ID"]=OfferingRow_detail.QUOTE_ID
		tbrow["ENTITLEMENT_XML"]=insertservice
		tbrow["QUOTE_NAME"]=OfferingRow_detail.QUOTE_NAME
		tbrow["QUOTE_RECORD_ID"]=OfferingRow_detail.QUOTE_RECORD_ID
		tbrow["QTESRV_RECORD_ID"]=OfferingRow_detail.QUOTE_SERVICE_RECORD_ID
		tbrow["SERVICE_RECORD_ID"]=OfferingRow_detail.ADNPRD_RECORD_ID
		tbrow["SERVICE_ID"]=OfferingRow_detail.ADNPRD_ID
		tbrow["SERVICE_DESCRIPTION"]=OfferingRow_detail.ADNPRD_DESCRIPTION
		tbrow["PAR_SERVICE_RECORD_ID"]=OfferingRow_detail.SERVICE_RECORD_ID
		tbrow["PAR_SERVICE_ID"]=OfferingRow_detail.SERVICE_ID
		tbrow["PAR_SERVICE_DESCRIPTION"]=OfferingRow_detail.SERVICE_DESCRIPTION
		tbrow["CPS_CONFIGURATION_ID"]=Fullresponse['id']
		tbrow["SALESORG_RECORD_ID"]=OfferingRow_detail.SALESORG_RECORD_ID
		tbrow["SALESORG_ID"]=OfferingRow_detail.SALESORG_ID
		tbrow["SALESORG_NAME"]=OfferingRow_detail.SALESORG_NAME
		tbrow["CPS_MATCH_ID"] = 1
		tbrow["CPQTABLEENTRYADDEDBY"] = User_Id
		tbrow["CPQTABLEENTRYDATEADDED"] = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p")  
		tbrow["QTEREV_RECORD_ID"] = OfferingRow_detail.QTEREV_RECORD_ID
		tbrow["QTEREV_ID"] = OfferingRow_detail.QTEREV_ID
		tbrow["CONFIGURATION_STATUS"] = configuration_status
		#tbrow["IS_DEFAULT"] = '1'

		columns = ', '.join("" + str(x) + "" for x in tbrow.keys())
		values = ', '.join("'" + str(x) + "'" for x in tbrow.values())
		insert_qtqtse_query = "INSERT INTO SAQTSE ( %s ) VALUES ( %s );" % (columns, values)
		Sql.RunQuery(insert_qtqtse_query)
		
		# try:
		# 	Trace.Write("PREDEFINED WAFER DRIVER IFLOW")
		# 	where_condition = " WHERE QUOTE_RECORD_ID='{}' AND QTEREV_RECORD_ID='{}' AND SERVICE_ID = '{}' ".format(OfferingRow_detail.QUOTE_RECORD_ID, OfferingRow_detail.QTEREV_RECORD_ID, OfferingRow_detail.ADNPRD_ID)
		# 	# CQTVLDRIFW.valuedriver_predefined(self.contract_quote_record_id,"SERVICE_LEVEL",OfferingRow_detail.get("SERVICE_ID"),self.user_id,self.quote_revision_record_id, where_condition)
			
		# 	predefined = ScriptExecutor.ExecuteGlobal("CQVLDPRDEF",{"where_condition": where_condition,"quote_rec_id": OfferingRow_detail.QUOTE_RECORD_ID ,"level":"SERVICE_LEVEL", "treeparam":OfferingRow_detail.ADNPRD_ID,"user_id": user_id, "quote_rev_id":OfferingRow_detail.QTEREV_RECORD_ID})

		# except:
		# 	Trace.Write("EXCEPT---PREDEFINED DRIVER IFLOW")

def addon_greenbook_level_entitlement(OfferingRow_detail,greenbook):
	Sql.RunQuery("""INSERT SAQSGE (KB_VERSION,QUOTE_ID,QUOTE_NAME,QUOTE_RECORD_ID,QTEREV_RECORD_ID,QTEREV_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,	
			CPS_CONFIGURATION_ID, CPS_MATCH_ID,GREENBOOK,GREENBOOK_RECORD_ID,QTESRVENT_RECORD_ID,ENTITLEMENT_XML,CONFIGURATION_STATUS, QUOTE_SERVICE_GREENBOOK_ENTITLEMENT_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED )
			SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_GREENBOOK_ENTITLEMENT_RECORD_ID, {UserId} as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM (SELECT DISTINCT SAQTSE.KB_VERSION,SAQTSE.QUOTE_ID,SAQTSE.QUOTE_NAME,SAQTSE.QUOTE_RECORD_ID,SAQTSE.QTEREV_RECORD_ID,SAQTSE.QTEREV_ID,SAQTSE.SERVICE_DESCRIPTION,SAQTSE.SERVICE_ID,SAQTSE.SERVICE_RECORD_ID,SAQTSE.SALESORG_ID,SAQTSE.SALESORG_NAME,SAQTSE.SALESORG_RECORD_ID,	
			SAQTSE.CPS_CONFIGURATION_ID, SAQTSE.CPS_MATCH_ID,SAQSGB.GREENBOOK,SAQSGB.GREENBOOK_RECORD_ID,SAQTSE.QUOTE_SERVICE_ENTITLEMENT_RECORD_ID as QTESRVENT_RECORD_ID,SAQTSE.ENTITLEMENT_XML,SAQTSE.CONFIGURATION_STATUS FROM
		SAQTSE (NOLOCK) JOIN SAQSGB  (NOLOCK) ON SAQSGB.SERVICE_ID = SAQTSE.SERVICE_ID AND SAQSGB.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID  AND SAQSGB.QTEREV_RECORD_ID = SAQTSE.QTEREV_RECORD_ID  
			WHERE SAQTSE.QUOTE_RECORD_ID ='{QuoteRecordId}'  AND SAQTSE.QTEREV_RECORD_ID = '{revision_rec_id}' AND SAQTSE.PAR_SERVICE_ID = '{ServiceId}' AND  SAQTSE.SERVICE_ID = '{Addon_ServiceId}' AND SAQSGB.GREENBOOK = '{greenbook}')IQ""".format(UserId=User_Id, QuoteRecordId=OfferingRow_detail.QUOTE_RECORD_ID, ServiceId=OfferingRow_detail.SERVICE_ID, revision_rec_id = OfferingRow_detail.QTEREV_RECORD_ID,Addon_ServiceId = OfferingRow_detail.ADNPRD_ID,greenbook = greenbook))
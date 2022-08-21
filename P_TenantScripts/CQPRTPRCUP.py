 #=======================================================================================================================================
#   __script_name : CQPRTPRCUP.py
#   __script_description : THIS SCRIPT IS USED FOR CPS PART PRICING 
#   __primary_author__ : Suriyanarayanan Pazhani
#   __create_date :09-01-2022 
#   Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
#=======================================================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct
import clr
import System.Net
import datetime
import re
from System.Text.Encoding import UTF8
from System import Convert
from SYDATABASE import SQL

Sql = SQL()
QUOTE = Param.CPQ_Columns['Entries']
revision = Param.CPQ_Columns['Revision']
try:
	part_number = Param.CPQ_Columns['Partnumber']
except:
	part_number = ''
#Log.Info("partnumber-->"+str(part_number))
#script_start_time = time.time()
# Log.Info("QUOTE ID---> "+str(QUOTE)+"CPS Price Script Started")
# Log.Info("------->CPI Hitting  2021")
webclient = System.Net.WebClient()
getDomain = Sql.GetFirst("SELECT top 1 Domain FROM SYCONF (nolock) order by CpqTableEntryId")
if getDomain:
	domain=getDomain.Domain
		
if (domain).lower() == 'appliedmaterials_tst':
	webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/json"
	webclient.Headers[System.Net.HttpRequestHeader.Authorization] = "Basic c2ItYzQwYThiMWYtYzU5NS00ZWJjLTkyYzYtYzM4ODg4ODFmMTY0IWIyNTAzfGNwc2VydmljZXMtc2VjdXJlZCFiMzkxOm9zRzgvSC9hOGtkcHVHNzl1L2JVYTJ0V0FiMD0=";
	response_token = webclient.DownloadString("https://cpqprojdevamat.authentication.us10.hana.ondemand.com:443/oauth/token?grant_type=client_credentials")
	response_token = eval(response_token)
else:
	webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/x-www-form-urlencoded"
	cps_credential_obj = SqlHelper.GetFirst("SELECT USER_NAME, PASSWORD, URL FROM SYCONF (NOLOCK) WHERE EXTERNAL_TABLE_NAME='CPS_VARIANT_PRICING'")
	if cps_credential_obj:
		response_token = webclient.DownloadString(cps_credential_obj.URL+'?grant_type=client_credentials&client_id='+cps_credential_obj.USER_NAME+'&client_secret='+cps_credential_obj.PASSWORD)
	response_token = eval(response_token)

webclient.Headers[System.Net.HttpRequestHeader.Authorization] ="Bearer "+str(response_token['access_token'])

Log.Info("QUOTE_CUP==>"+str(QUOTE))
spare_temp_table_name ="EXCELUPDATE_SAQSPT_{}".format(QUOTE)
excel_bkp=SqlHelper.GetFirst("SELECT COUNT(*) AS CNT FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME ='{}'".format(str(spare_temp_table_name)))
if excel_bkp.CNT == 1:
	spare_parts_temp_table_drop = SqlHelper.GetFirst("sp_executesql @T=N'IF EXISTS (SELECT ''X'' FROM SYS.OBJECTS WHERE NAME= ''"+str(spare_temp_table_name)+"'' ) BEGIN DROP TABLE "+str(spare_temp_table_name)+" END  ' ")

x = datetime.datetime.today()
x= str(x)
y = x.split(" ")
#partids = []
all_count = 0
loop_count = 0
#GET PRICING PROCEDURE
contract_quote_record_id = None
account_info={}
taxk1=''
pricingPro={'ZZCQAP':'ZC07','ZZCQNA':'M','ZZCQEU':'M','ZZCQEU-KONDA':'75','ZZCQNA-KONDA':'75','ZZCQAP-KONDA':'S4'}

SAQTIP_INFO = SqlHelper.GetList(""" SELECT CPQ_PARTNER_FUNCTION, PARTY_ID FROM SAQTIP (NOLOCK) WHERE QUOTE_ID='{}' AND QTEREV_RECORD_ID='{}' AND CPQ_PARTNER_FUNCTION IN ('SOLD TO','SHIP TO') """.format(QUOTE,revision))
for keyobj in SAQTIP_INFO:
	account_info[keyobj.CPQ_PARTNER_FUNCTION] = keyobj.PARTY_ID

GetPricingProcedure = Sql.GetFirst("SELECT QUOTE_RECORD_ID,DIVISION_ID, DISTRIBUTIONCHANNEL_ID, SALESORG_ID, DOC_CURRENCY,COUNTRY, PRICINGPROCEDURE_ID, QUOTE_RECORD_ID,EXCHANGE_RATE_TYPE, GLOBAL_CURRENCY, ACCTAXCLA_ID, PAYMENTTERM_ID, INCOTERM_ID, COMPANY_ID, DOCTYP_ID,CONTRACT_VALID_FROM, EXCHANGE_RATE_DATE FROM SAQTRV (NOLOCK) WHERE QUOTE_ID = '{}' AND QTEREV_RECORD_ID='{}' ".format(QUOTE,revision))
if GetPricingProcedure is not None:
	Trace.Write('inside----'+str(GetPricingProcedure))
	PricingProcedure = GetPricingProcedure.PRICINGPROCEDURE_ID
	curr = GetPricingProcedure.DOC_CURRENCY
	glb_curr =  GetPricingProcedure.GLOBAL_CURRENCY
	dis = GetPricingProcedure.DISTRIBUTIONCHANNEL_ID
	salesorg = GetPricingProcedure.SALESORG_ID
	div = GetPricingProcedure.DIVISION_ID
	exch = GetPricingProcedure.EXCHANGE_RATE_TYPE
	contract_quote_record_id = GetPricingProcedure.QUOTE_RECORD_ID
	country=GetPricingProcedure.COUNTRY
	taxk1 = GetPricingProcedure.ACCTAXCLA_ID
	payterm_id = GetPricingProcedure.PAYMENTTERM_ID
	incoterm_id = GetPricingProcedure.INCOTERM_ID
	company_id = GetPricingProcedure.COMPANY_ID
	doctype_id=GetPricingProcedure.DOCTYP_ID
	contract_valid_from = GetPricingProcedure.CONTRACT_VALID_FROM
	exchange_rate_date = GetPricingProcedure.EXCHANGE_RATE_DATE
	cv=str(contract_valid_from)
	(cm,cd,cy)=re.sub(r'\s+([^>]*?)$','',cv).split('/')
	cd = '0'+str(cd) if len(cd)==1 else cd
	cm = '0'+str(cm) if len(cm)==1 else cm        
	cvf = cy+cm+cd
	cvf_1 = cy+'-'+cm+'-'+cd
	cv=str(exchange_rate_date)
	(cm,cd,cy)=re.sub(r'\s+([^>]*?)$','',cv).split('/')
	cd = '0'+str(cd) if len(cd)==1 else cd
	cm = '0'+str(cm) if len(cm)==1 else cm        
	cvf = cy+cm+cd
	exc_rate_date = cy+'-'+cm+'-'+cd 
	#taxk1 = GetPricingProcedure.CUSTAXCLA_ID
	#taxk1 = "1"
account_info['docCurrency']= '{"name":"KOMK-WAERK","values":["'+str(curr)+'"]}'
account_info['globalCurrency']= '{"name":"KOMK-HWAER","values":["'+str(glb_curr)+'"]}'
kyma_url='https://x-tenant-hanadbhelper.c-1404e87.kyma.shoot.live.k8s-hana.ondemand.com'
cpi_url="https://e250404-iflmap.hcisbt.us3.hana.ondemand.com/cxf/CPQ_CPS"
requestdata1 = "grant_type=client_credentials&client_id=30a9bc56-fb80-4d98-81ab-44e29ac34605&client_secret=G.wfjEPRj31IBJ3IA~Irtc13B4&scope=hanasafeaccess"
oauthURL='https://oauth2.c-1404e87.kyma.shoot.live.k8s-hana.ondemand.com/oauth2/token'
if (domain).lower() == 'appliedmaterials_sit':
	kyma_url='https://t-tenant-hanadbconnectivity.c-1404e87.kyma.shoot.live.k8s-hana.ondemand.com'
	cpi_url="https://e250404-iflmap.hcisbt.us3.hana.ondemand.com/cxf/QTGETENPRT"
	requestdata1 = "grant_type=client_credentials&client_id=6032a032-ec9c-418c-a576-ab4e4cc71164&client_secret=48._teByFxio4AK_d903WIot2g&scope=hanasafeaccess"
	oauthURL='https://oauth2.c-1404e87.kyma.shoot.live.k8s-hana.ondemand.com/oauth2/token'
elif (domain).lower() == 'appliedmaterials_uat':
	kyma_url='https://q-tenant-hanahelper.c-1404e87.kyma.shoot.live.k8s-hana.ondemand.com'
	cpi_url="https://e250404-iflmap.hcisbt.us3.hana.ondemand.com/cxf/QTGETENPRQ"
	requestdata1 = "grant_type=client_credentials&client_id=279b78e5-7653-442e-b0fc-331d2577a6c4&client_secret=FkkquldvqabUolR8Nn2pjDKJwD&scope=hanasafeaccess" 
	oauthURL='https://oauth2.c-1404e87.kyma.shoot.live.k8s-hana.ondemand.com/oauth2/token'
elif (domain).lower() == 'appliedmaterials_opt':
	kyma_url='https://hana-helper.c-68c90e5.kyma.ondemand.com'
	cpi_url="https://e250404-iflmap.hcisbt.us3.hana.ondemand.com/cxf/QTGETENPRY"
	requestdata1 = "grant_type=client_credentials&client_id=b1b9375b-e42b-4956-96db-b1408912a22a&client_secret=1BTwCqx8eTI0Loa6FM8b35wb22&scope=hanasafeaccess"
	oauthURL='https://oauth2.c-68c90e5.kyma.ondemand.com/oauth2/token'
elif (domain).lower() == 'appliedmaterials_prd':
	kyma_url='https://hana-helper.c-3ae981f.kyma.ondemand.com'
	cpi_url="https://l250877-iflmap.hcisbp.us3.hana.ondemand.com/cxf/QTGETENPRP"
	requestdata1 = "grant_type=client_credentials&client_id=2e0c303c-ce04-4aca-87f7-ea44e25eea43&client_secret=0CMz5Xwx7lvQA-_HnfjOOd5UrI&scope=hanasafeaccess"
	oauthURL='https://oauth2.c-3ae981f.kyma.ondemand.com/oauth2/token'
	
if doctype_id=='ZWK1':
	div = '56'

#GET ZZEXE FLAG 
partLists=[]
PartList={}
partList=''
totalParts=SqlHelper.GetList("""SELECT PART_NUMBER FROM SAQSPT (NOLOCK) WHERE QUOTE_ID = '{}' AND QTEREV_RECORD_ID='{}'""".format(QUOTE,revision))
if not totalParts:
	totalParts=SqlHelper.GetList("""SELECT PART_NUMBER FROM SAQRSP (NOLOCK) WHERE QUOTE_ID = '{}' AND QTEREV_RECORD_ID='{}' AND SERVICE_ID='Z0100'""".format(QUOTE,revision))
for ele in totalParts:
	partLists.append(ele.PART_NUMBER)
if len(partLists)>0:
	partList=str(partLists)
	partList = re.sub(r'\[','(',partList)
	partList = re.sub(r'\]',')',partList)
else:
    partList= ['XXXX-XXX']
    partList=str(partList)
    partList = re.sub(r'\[','(',partList)
    partList = re.sub(r'\]',')',partList)
    
try:
	response = ''
	webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/x-www-form-urlencoded"
	response = webclient.UploadString(str(oauthURL),str(requestdata1))
	response = eval(response)
	webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/json"
	webclient.Headers[System.Net.HttpRequestHeader.Authorization] ="Bearer "+str(response['access_token'])
	requestData2 = '{"query":"SELECT (MATNR||'+"':'"+"||ZZEXE) AS exFlag from A668 where VKORG = '{}' AND MATNR  IN {}".format(str(salesorg),str(partList)+'"}')
	responseData = webclient.UploadString(str(kyma_url),requestData2)
	responseData2=re.sub(r'"EXFLAG":','',str(responseData))
	Log.Info("exflagResponse==>"+str(responseData2))
	pattern_tag = re.compile(r'"([^>]*?):([^>]*?)"')
	for values in re.finditer(pattern_tag, str(responseData2)):
		PartList[str(values.group(1))]=str(values.group(2))
except:
	Log.Info("EXFlag applicable for FPM")

#GET ISOCODE 
ISOCode={}
getIsocode=SqlHelper.GetList("""SELECT DISTINCT UOM, UOM_ISO_CODE FROM MAMUOM (NOLOCK)""")
for code in getIsocode:
	ISOCode[code.UOM]=code.UOM_ISO_CODE

getMaterialGrpList=SqlHelper.GetList("""SELECT DISTINCT SAP_PART_NUMBER, MATPRIGRP_ID FROM MAMSOP (NOLOCK) WHERE SAP_PART_NUMBER IN {} AND SALESORG_ID='{}' AND DISTRIBUTIONCHANNEL_ID='{}'""".format(str(partList),str(salesorg),str(dis)))
MaterialGrps={}
for code in getMaterialGrpList:
	MaterialGrps[code.SAP_PART_NUMBER]=code.MATPRIGRP_ID

#UPDATE PRICING PROCEDURE TO SAQITM
getPricingProc=SqlHelper.GetFirst("""SELECT PRICINGPROCEDURE_ID FROM SASAPP (NOLOCK) WHERE DISTRIBUTIONCHANNEL_ID='{}' AND DIVISION_ID='{}' AND SALESORG_ID='{}'""".format(dis,div,salesorg))
if getPricingProc:
	PricingProcedure = getPricingProc.PRICINGPROCEDURE_ID
	if exch == '':
		exch = pricingPro[PricingProcedure]
		update_SAQTRV = "UPDATE SAQTRV  SET PRICINGPROCEDURE_ID = '{prc}', EXCHANGE_RATE_TYPE = '{EXCH}' WHERE SAQTRV.QUOTE_ID = '{quote}'".format(prc=str(PricingProcedure),EXCH=str(exch), quote=QUOTE)
		Sql.RunQuery(update_SAQTRV)

update_SAQIFP = "UPDATE SAQIFP SET PRICINGPROCEDURE_ID = '{prc}' WHERE SAQIFP.QUOTE_ID = '{quote}'".format(prc=str(PricingProcedure),tax=str(taxk1), quote=QUOTE)
Sql.RunQuery(update_SAQIFP)

price_listtype=''
price_groupid=''
PartDivisions={}

part_divisionlist = SqlHelper.GetList("SELECT SAP_PART_NUMBER, DIVISION_ID FROM MAMTRL WHERE SAP_PART_NUMBER IN (SELECT PART_NUMBER FROM SAQSPT WHERE QUOTE_ID='{quote}')".format(quote=QUOTE))
for obj in part_divisionlist:
	PartDivisions[str(obj.SAP_PART_NUMBER)]=str(obj.DIVISION_ID)

price_list = SqlHelper.GetFirst("SELECT  PRICEGROUP_ID, PRICELIST_ID FROM  SASAAC (NOLOCK) WHERE  SALESORG_ID ='"+str(salesorg)+"'AND ACCOUNT_ID='"+str(account_info['SOLD TO'])+"' AND DIVISION_ID ='"+str(div)+"'   AND DISTRIBUTIONCHANNEL_ID ='"+str(dis)+"'")

if price_list:
	price_listtype=price_list.PRICELIST_ID
	price_groupid=price_list.PRICEGROUP_ID


currency_attribute = account_info['docCurrency']+','+account_info['globalCurrency']+','+'{"name":"KOMK-KONDA","values":["'+str(price_groupid)+'"]}'

today = datetime.datetime.now()
Modi_date = today.strftime("%m/%d/%Y %H:%M:%S %p")


start = 1
end = 100
L = 1

part_query = ""
ancillary_part_query =""
fpm_part_query =""

if part_number != '':
	part_query = Sql.GetFirst("SELECT DISTINCT PART_NUMBER, CUSTOMER_ANNUAL_QUANTITY as ANNUAL_QUANTITY FROM (SELECT PART_NUMBER, CUSTOMER_ANNUAL_QUANTITY,ROW_NUMBER() OVER(ORDER BY PART_NUMBER) AS SNO FROM SAQSPT (NOLOCK) WHERE QUOTE_ID = '"+str(QUOTE)+"' AND QTEREV_RECORD_ID = '"+str(revision)+"' AND PART_NUMBER = '"+str(part_number)+"')A WHERE SNO>="+str(start)+" AND SNO<="+str(end)+" ")
if not part_query and part_number != '':
	part_query = Sql.GetFirst("SELECT DISTINCT PART_NUMBER, QUANTITY as ANNUAL_QUANTITY FROM (SELECT PART_NUMBER, QUANTITY,ROW_NUMBER() OVER(ORDER BY PART_NUMBER) AS SNO FROM SAQRSP (NOLOCK) WHERE QUOTE_ID = '"+str(QUOTE)+"' AND QTEREV_RECORD_ID = '"+str(revision)+"' AND PART_NUMBER = '"+str(part_number)+"' AND INCLUDED =1 AND SERVICE_ID IN('Z0100') )A WHERE SNO>="+str(start)+" AND SNO<="+str(end)+" ")
if not part_query:
	part_query = SqlHelper.GetList("SELECT DISTINCT PART_NUMBER, ANNUAL_QUANTITY FROM (SELECT PART_NUMBER, ANNUAL_QUANTITY,ROW_NUMBER() OVER(ORDER BY PART_NUMBER) AS SNO FROM SAQIFP (NOLOCK) WHERE QUOTE_ID = '"+str(QUOTE)+"' AND QTEREV_RECORD_ID = '"+str(revision)+"' AND PRICING_STATUS = 'ACQUIRING...' )A WHERE SNO>="+str(start)+" AND SNO<="+str(end)+"  ")
if not part_query:
	part_query = Sql.GetFirst("SELECT DISTINCT PART_NUMBER, QUANTITY as ANNUAL_QUANTITY FROM (SELECT PART_NUMBER, QUANTITY,ROW_NUMBER() OVER(ORDER BY PART_NUMBER) AS SNO FROM SAQRSP (NOLOCK) WHERE QUOTE_ID = '"+str(QUOTE)+"' AND QTEREV_RECORD_ID = '"+str(revision)+"' AND INCLUDED =1 AND SERVICE_ID IN('Z0100') AND QUANTITY >0 )A WHERE SNO>="+str(start)+" AND SNO<="+str(end)+" ")
if not part_query:
	part_query = Sql.GetFirst("SELECT DISTINCT PART_NUMBER, CUSTOMER_ANNUAL_QUANTITY as ANNUAL_QUANTITY FROM (SELECT PART_NUMBER, CUSTOMER_ANNUAL_QUANTITY,ROW_NUMBER() OVER(ORDER BY PART_NUMBER) AS SNO FROM SAQSPT (NOLOCK) WHERE QUOTE_ID = '"+str(QUOTE)+"' AND QTEREV_RECORD_ID = '"+str(revision)+"' )A WHERE SNO>="+str(start)+" AND SNO<="+str(end)+" ")
if part_query:
	Sql.RunQuery("DELETE FROM SYSPBT WHERE QUOTE_ID= '"+str(QUOTE)+"'")
	unique_no = 1
	while L == 1:
		itemid = ''
		get_part_query=""
		if part_number != '':
			get_part_query = Sql.GetList("SELECT DISTINCT PART_NUMBER, CUSTOMER_ANNUAL_QUANTITY as ANNUAL_QUANTITY,ODCC_FLAG, SHPACCOUNT_ID,SALESUOM_ID,SALESUOM_CONVERSION_FACTOR,BASEUOM_ID FROM (SELECT PART_NUMBER, CUSTOMER_ANNUAL_QUANTITY,ODCC_FLAG,SHPACCOUNT_ID ,SALESUOM_ID,SALESUOM_CONVERSION_FACTOR,BASEUOM_ID,ROW_NUMBER() OVER(ORDER BY PART_NUMBER) AS SNO FROM SAQSPT (NOLOCK) WHERE QUOTE_ID = '"+str(QUOTE)+"' AND QTEREV_RECORD_ID = '"+str(revision)+"' AND PART_NUMBER = '"+str(part_number)+"')A WHERE SNO>="+str(start)+" AND SNO<="+str(end)+"  ")
			L = 0
		if not get_part_query and part_number != '':
			get_part_query = Sql.GetList("SELECT DISTINCT PART_NUMBER, QUANTITY as ANNUAL_QUANTITY,ODCC_FLAG,SHPACCOUNT_ID,SALESUOM_ID,SALESUOM_CONVERSION_FACTOR,BASEUOM_ID FROM (SELECT PART_NUMBER, QUANTITY,null as ODCC_FLAG, null as SHPACCOUNT_ID,null as SALESUOM_ID,null as SALESUOM_CONVERSION_FACTOR, null as BASEUOM_ID, ROW_NUMBER() OVER(ORDER BY PART_NUMBER) AS SNO FROM SAQRSP (NOLOCK) WHERE QUOTE_ID = '"+str(QUOTE)+"' AND QTEREV_RECORD_ID = '"+str(revision)+"'AND PART_NUMBER = '"+str(part_number)+"' AND INCLUDED = 1 AND SERVICE_ID IN('Z0100') )A WHERE SNO>="+str(start)+" AND SNO<="+str(end)+"  ")
			L = 0
		if not get_part_query:
			get_part_query = Sql.GetList("SELECT DISTINCT PART_NUMBER, ANNUAL_QUANTITY, ODCC_FLAG,SHPACCOUNT_ID,SALESUOM_ID,SALESUOM_CONVERSION_FACTOR,BASEUOM_ID FROM (SELECT PART_NUMBER, ANNUAL_QUANTITY,ODCC_FLAG,SHPACCOUNT_ID,SALESUOM_ID,SALESUOM_CONVERSION_FACTOR,BASEUOM_ID, ROW_NUMBER() OVER(ORDER BY PART_NUMBER) AS SNO FROM SAQIFP (NOLOCK) WHERE QUOTE_ID = '"+str(QUOTE)+"' AND QTEREV_RECORD_ID = '"+str(revision)+"' AND PRICING_STATUS = 'ACQUIRING...' )A WHERE SNO>="+str(start)+" AND SNO<="+str(end)+"  ")
		if not get_part_query:
			get_part_query = Sql.GetList("SELECT DISTINCT PART_NUMBER, QUANTITY as ANNUAL_QUANTITY,ODCC_FLAG,SHPACCOUNT_ID,SALESUOM_ID,SALESUOM_CONVERSION_FACTOR,BASEUOM_ID FROM (SELECT PART_NUMBER, QUANTITY,null as ODCC_FLAG, null as SHPACCOUNT_ID,null as SALESUOM_ID,null as SALESUOM_CONVERSION_FACTOR, null as BASEUOM_ID, ROW_NUMBER() OVER(ORDER BY PART_NUMBER) AS SNO FROM SAQRSP (NOLOCK) WHERE QUOTE_ID = '"+str(QUOTE)+"' AND QTEREV_RECORD_ID = '"+str(revision)+"' AND INCLUDED = 1 AND SERVICE_ID IN('Z0100') )A WHERE SNO>="+str(start)+" AND SNO<="+str(end)+"  ")
		if not get_part_query:
			get_part_query = Sql.GetList("SELECT DISTINCT PART_NUMBER, CUSTOMER_ANNUAL_QUANTITY as ANNUAL_QUANTITY,ODCC_FLAG, SHPACCOUNT_ID,SALESUOM_ID,SALESUOM_CONVERSION_FACTOR,BASEUOM_ID FROM (SELECT PART_NUMBER, CUSTOMER_ANNUAL_QUANTITY,ODCC_FLAG,SHPACCOUNT_ID ,SALESUOM_ID,SALESUOM_CONVERSION_FACTOR,BASEUOM_ID,ROW_NUMBER() OVER(ORDER BY PART_NUMBER) AS SNO FROM SAQSPT (NOLOCK) WHERE QUOTE_ID = '"+str(QUOTE)+"' AND QTEREV_RECORD_ID = '"+str(revision)+"' )A WHERE SNO>="+str(start)+" AND SNO<="+str(end)+"  ")
		
		partids = quantity = li = []
		s = ""
		shipto_details= ""
		shipto = ""
		if get_part_query:      
			partids = [p.PART_NUMBER for p in get_part_query]
			quantity = [q.ANNUAL_QUANTITY for q in get_part_query]
			try:
				odcc_flag = [r.ODCC_FLAG for r in get_part_query]
				shipto = [s.SHPACCOUNT_ID for s in get_part_query]
				salesUOM = [t.SALESUOM_ID for t in get_part_query]
				salesUOMConv = [u.SALESUOM_CONVERSION_FACTOR for u in get_part_query]
				baseUOMs = [v.BASEUOM_ID for v in get_part_query]
				salesUOMConvs = int(salesUOMConv[0] or 1)
				shipto_details=shipto[0] or account_info['SHIP TO']
				str_odcc_flag = odcc_flag[0]
			except:
				odcc_flag = ['' for r in get_part_query] 
				str_odcc_flag =''
			start = start + 100
			end = end + 100
			requestdata = ''
			##for currencies in ('docCurrency','globalCurrency'): 0 / 1
			currencies=1
			if len(partids) == 1:
				#Log.Info("**Single-Partids**")
				if quantity[0] == 0 or quantity[0] == '':
					quantity[0]=1
				quantity[0] = int(quantity[0] or 1)
				curr_attr = currency_attribute
				salesUOMs= salesUOM[0] or 'EA'
				baseUOM= baseUOMs[0] or 'EA'
				itemleveldivison = PartDivisions.get(str(p)) or '99'
				prefixZero=''
				if re.match(r'^\d+$',partids[0]):
					totallen = len(partids[0])
					remaining = 18-totallen
					for x in range(remaining):
						prefixZero = str(prefixZero) + str(0)
					partids[0]= str(prefixZero)+str(partids[0])
				materialgroupid=MaterialGrps.get(str(partids[0])) or ''
				if salesUOMs !='':
					salesuom_attr = '"quantity":{"value":'+str(quantity[0])+',"unit":"'+str(ISOCode[salesUOMs])+'"},"exchRateType":"'+str(exch)+'","exchRateDate":"'+str(y[0])+'","productDetails":{"productId":"'+str(partids[0])+'","baseUnit":"'+str(ISOCode[baseUOM])+'","alternateProductUnits": [{"alternateUnitName": "'+str(ISOCode[salesUOMs])+'","numerator": "'+str(salesUOMConvs)+'","denominator": "1"}]}'
				if str_odcc_flag in ('CCM','CCO','CUM','CUO'):
					curr_attr += ','+'{"name":"KOMP-ZZ_ODCC_ELIGIBILITY_FLAG","values":["'+str(str_odcc_flag)+'"]}'
				
				zzexeFlag=PartList.get(str(partids[0])) or ''
				itemid = str(partids[0])+";"+str(QUOTE)+";"+str(quantity[0])+";"+str(currencies)+";"+str(prefixZero)+";"+str(ISOCode[salesUOMs] or 'EA')+";"+str(salesUOMConvs or 1)+";1"
				attriButes = '{"name":"KOMK-KALSM","values":["'+str(PricingProcedure)+'"]}'+','+'{"name":"KOMP-KONDM","values":["'+str(materialgroupid)+'"]}'
				item_string = '{"itemId":"'+str(itemid)+'","externalId":null,'+str(salesuom_attr)+',"attributes":[{"name":"KOMK-LAND1","values":["'+str(country)+'"]},{"name":"KOMP-KPOSN","values":["10"]},{"name":"KOMV-KSCHL","values":[""]},{"name":"KOMP-ZZEXE","values":["'+str(zzexeFlag)+'"]},{"name":"KOMP-KZNEP","values":[""]},{"name":"KOMK-KUNNR","values":["00'+account_info['SOLD TO']+'"]},{"name":"KOMK-KUNWE","values":["00'+str(shipto_details)+'"]},{"name":"KOMK-SPART","values":["'+str(div)+'"]},{"name":"KOMP-SPART","values":["'+str(itemleveldivison)+'"]},{"name":"KOMP-PMATN","values":["'+str(partids[0])+'"]},{"name":"KOMP-ZZPSTR_COUNTER","values":["1"]},{"name":"KOMK-ZZSPART","values":["'+str(div)+'"]},'+str(curr_attr)+',{"name":"KOMV-KDUPL","values":[""]},{"name":"KONV-KOAID","values":["A"]},{"name":"KOMP-ZZPRREASON","values":[""]},{"name":"KOMK-AUART","values":["ZQT1"]},{"name":"KOMP-PRSFD","values":["X"]},{"name":"KOMK-ZZWFSTATUS","values":[""]},{"name":"KOMP-UEPOS","values":["0000"]},{"name":"KOMP-FAREG","values":[""]},{"name":"KOMP-EVRWR","values":["X"]},{"name":"KOMK-KURST","values":["'+str(exch)+'"]},{"name":"KOMP-MGAME","values":["1.00"]},{"name":"KOMP-TAXM1","values":["1"]},{"name":"KOMK-TAXK1","values":["'+str(taxk1)+'"]},{"name":"KOMK-ZZKTOKD","values":["KUNA"]},{"name":"KOMK-BUKRS","values":["'+str(company_id)+'"]},{"name":"KOMV-KKURS","values":["1.00"]},{"name":"KONP-KNTYP","values":["L"]},{"name":"KOMK-ZTERM","values":["'+str(payterm_id)+'"]},{"name":"KOMK-INCO1","values":["'+str(incoterm_id)+'"]},{"name":"KOMK-AUART_SD","values":["ZQT1"]},{"name":"KOMK-ALAND","values":["'+str(country)+'"]},{"name":"KOMP-WERKS","values":["8639"]},{"name":"KOMP-MWSBP","values":["0.00"]},{"name":"KOMP-PRSOK","values":["X"]},{"name":"KOMP-PSTYV","values":["ZAGN"]},{"name":"KOMP-SKTOF","values":["X"]},{"name":"KOMK-PLTYP","values":["'+str(price_listtype)+'"]},{"name":"KOMP-ZZMTLSEGMCODE","values":["A01-000"]},{"name":"KOMV-KNTYP","values":["G"]},{"name":"KOMK-VTWEG","values":["'+str(dis)+'"]},{"name":"KOMP-BRTWR","values":["0.0"]},{"name":"KOMP-MGLME","values":["1.0"]},{"name":"KOMV-KPEIN","values":["1.0"]},{"name":"KOMK-FKART","values":[""]},{"name":"KOMK-ERDAT","values":["'+str(cvf)+'"]},'+str(attriButes)+',{"name":"KOMV-KNUMV","values":[""]},{"name":"KOMK-VBTYP","values":["B"]},{"name":"KOMK-VKORG","values":["'+str(salesorg)+'"]}],"accessDateList":[{"name":"KOMK-PRSDT","value":"'+str(exc_rate_date)+'"},{"name":"KOMK-FBUDA","value":"'+str(cvf_1)+'"}],"variantConditions":[],"statistical":true,"subItems":[]}'
				li.append(item_string)
				s = ','.join(li)	
				requestdata = '<?xml version=\"1.0\" encoding=\"UTF-8\"?><soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\">  <soapenv:Body> <cpq_columns><root> {"docCurrency":"USD","locCurrency":"'+str(glb_curr)+'","pricingProcedure":"'+str(PricingProcedure)+'","groupCondition":false,"itemConditionsRequired":true,"items": ['+str(s)+']} </root> <CPSToken>'+str(response_token['access_token'])+'</CPSToken></cpq_columns> </soapenv:Body></soapenv:Envelope>'
				#Log.Info("requestdata==>"+str(requestdata))
			else:
				#Log.Info("**Multiple-Partids**")
				for index,val in enumerate(zip(partids,quantity,odcc_flag,shipto,salesUOM,salesUOMConv,baseUOMs)):
					p=val[0]
					q=val[1]
					r=val[2]
					s=val[3] or account_info['SHIP TO']
					salesUOMs=val[4] or 'EA'
					salesUOMConvs=int(val[5] or 1)
					baseUOM=val[6] or 'EA'
					
					itemleveldivison = PartDivisions.get(str(p)) or 99
					materialgroupid=MaterialGrps.get(str(p)) or ''
					if q<=0 or q=='':
						q=1
					q=int(q)
					prefixZero=''
					if re.match(r'^\d+$',p):
						totallen = len(p)
						remaining = 18-totallen
						for x in range(remaining):
							prefixZero = str(prefixZero) + str(0)
						p = str(prefixZero)+str(p)
					curr_attr2 = currency_attribute
					if salesUOMs !='':
						salesuom_attr = '"quantity":{"value":'+str(q)+',"unit":"'+str(ISOCode[salesUOMs])+'"},"exchRateType":"'+str(exch)+'","exchRateDate":"'+str(y[0])+'","productDetails":{"productId":"'+str(p)+'","baseUnit":"'+str(ISOCode[baseUOM])+'","alternateProductUnits": [{"alternateUnitName": "'+str(ISOCode[salesUOMs])+'","numerator": "'+str(salesUOMConvs)+'","denominator": "1"}]}'
					
					if r in ('CCM','CCO','CUM','CUO'):
						curr_attr2 += ','+'{"name":"KOMP-ZZ_ODCC_ELIGIBILITY_FLAG","values":["'+str(r)+'"]}'
					itemid = str(p)+";"+str(QUOTE)+";"+str(q)+";"+str(currencies)+";"+str(prefixZero)+";"+str(ISOCode[salesUOMs] or 'EA')+";"+str(salesUOMConvs or 1)+";"+str(unique_no)
					unique_no += 1
					attriButes = '{"name":"KOMK-KALSM","values":["'+str(PricingProcedure)+'"]}'+','+'{"name":"KOMP-KONDM","values":["'+str(materialgroupid)+'"]}'
				
					zzexeFlag=PartList.get(str(p)) or ''
					item_string = '{"itemId":"'+str(itemid)+'","externalId":null,'+str(salesuom_attr)+',"attributes":[{"name":"KOMK-LAND1","values":["'+str(country)+'"]},{"name":"KOMP-KPOSN","values":["10"]},{"name":"KOMV-KSCHL","values":[""]},{"name":"KOMP-ZZEXE","values":["'+str(zzexeFlag)+'"]},{"name":"KOMP-KZNEP","values":[""]},{"name":"KOMK-KUNNR","values":["00'+account_info['SOLD TO']+'"]},{"name":"KOMK-KUNWE","values":["00'+str(s)+'"]},{"name":"KOMK-SPART","values":["'+str(div)+'"]},{"name":"KOMP-SPART","values":["'+str(itemleveldivison)+'"]},{"name":"KOMP-PMATN","values":["'+str(p)+'"]},{"name":"KOMP-ZZPSTR_COUNTER","values":["1"]},{"name":"KOMK-ZZSPART","values":["'+str(div)+'"]},'+str(curr_attr2)+',{"name":"KOMV-KDUPL","values":[""]},{"name":"KONV-KOAID","values":["A"]},{"name":"KOMP-ZZPRREASON","values":[""]},{"name":"KOMK-AUART","values":["ZQT1"]},{"name":"KOMP-PRSFD","values":["X"]},{"name":"KOMK-ZZWFSTATUS","values":[""]},{"name":"KOMP-UEPOS","values":["0000"]},{"name":"KOMP-FAREG","values":[""]},{"name":"KOMP-EVRWR","values":["X"]},{"name":"KOMK-KURST","values":["'+str(exch)+'"]},{"name":"KOMP-MGAME","values":["1.00"]},{"name":"KOMP-TAXM1","values":["1"]},{"name":"KOMK-TAXK1","values":["'+str(taxk1)+'"]},{"name":"KOMK-ZZKTOKD","values":["KUNA"]},{"name":"KOMK-BUKRS","values":["'+str(company_id)+'"]},{"name":"KOMV-KKURS","values":["1.00"]},{"name":"KONP-KNTYP","values":["L"]},{"name":"KOMK-ZTERM","values":["'+str(payterm_id)+'"]},{"name":"KOMK-INCO1","values":["'+str(incoterm_id)+'"]},{"name":"KOMK-AUART_SD","values":["ZQT1"]},{"name":"KOMK-ALAND","values":["'+str(country)+'"]},{"name":"KOMP-WERKS","values":["8639"]},{"name":"KOMP-MWSBP","values":["0.00"]},{"name":"KOMP-PRSOK","values":["X"]},{"name":"KOMP-PSTYV","values":["ZAGN"]},{"name":"KOMP-SKTOF","values":["X"]},{"name":"KOMK-PLTYP","values":["'+str(price_listtype)+'"]},{"name":"KOMP-ZZMTLSEGMCODE","values":["A01-000"]},{"name":"KOMV-KNTYP","values":["G"]},{"name":"KOMK-VTWEG","values":["'+str(dis)+'"]},{"name":"KOMP-BRTWR","values":["0.0"]},{"name":"KOMP-MGLME","values":["1.0"]},{"name":"KOMV-KPEIN","values":["1.0"]},{"name":"KOMK-FKART","values":[""]},{"name":"KOMK-ERDAT","values":["'+str(cvf)+'"]},'+str(attriButes)+',{"name":"KOMV-KNUMV","values":[""]},{"name":"KOMK-VBTYP","values":["B"]},{"name":"KOMK-VKORG","values":["'+str(salesorg)+'"]}],"accessDateList":[{"name":"KOMK-PRSDT","value":"'+str(exc_rate_date)+'"},{"name":"KOMK-FBUDA","value":"'+str(cvf_1)+'"}],"variantConditions":[],"statistical":true,"subItems":[]}'
					li.append(item_string)
				s = ','.join(li)
				
				#start_time = time.time()
				requestdata = '<?xml version=\"1.0\" encoding=\"UTF-8\"?><soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\">  <soapenv:Body> <cpq_columns><root>  {"docCurrency":"USD","locCurrency":"'+str(glb_curr)+'","pricingProcedure":"'+str(PricingProcedure)+'","groupCondition":false,"itemConditionsRequired":true,"items": ['+str(s)+']} </root> <CPSToken>'+str(response_token['access_token'])+'</CPSToken></cpq_columns> </soapenv:Body></soapenv:Envelope>'
			Log.Info("requestdata==>"+str(requestdata))

			LOGIN_CREDENTIALS = SqlHelper.GetFirst("SELECT USER_NAME as Username,Password,Domain FROM SYCONF where Domain='AMAT_TST'")
			Login_Username = str(LOGIN_CREDENTIALS.Username)
			Login_Password = str(LOGIN_CREDENTIALS.Password)
			authorization = Login_Username + ":" + Login_Password
			binaryAuthorization = UTF8.GetBytes(authorization)
			authorization = Convert.ToBase64String(binaryAuthorization)
			authorization = "Basic " + authorization
			webclient = System.Net.WebClient()
			webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/xml"
			webclient.Headers[System.Net.HttpRequestHeader.Authorization] = authorization
			response1 = webclient.UploadString(str(cpi_url),str(requestdata))
			#end_time = time.time()
		else:
			L=0
else:
	Log.Info('No Inputs for FPM Pricing Call.')
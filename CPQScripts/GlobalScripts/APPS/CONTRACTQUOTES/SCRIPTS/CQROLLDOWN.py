# =========================================================================================================================================
#   __script_name : CQROLLDOWN.PY
#   __script_description : roll down for entitlements after adding equipment(insert)
#   __create_date :16-11-2020
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct
import clr
import System.Net
import sys
import datetime
import re
from SYDATABASE import SQL
from System.Net import CookieContainer, NetworkCredential, Mail
from System.Net.Mail import SmtpClient, MailAddress, Attachment, MailMessage
Sql = SQL()
userId = str(User.Id)
userName = str(User.UserName)
import CQADDONPRD

gettodaydate = datetime.datetime.now().strftime("%Y-%m-%d")
Log.Info('ROLL DWON STARTS-CQROLLDWON---')
def cloneEntitlement(ProductPartnumber):
	webclient = System.Net.WebClient()
	webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/json"
	webclient.Headers[
		System.Net.HttpRequestHeader.Authorization
	] = "Basic c2ItYzQwYThiMWYtYzU5NS00ZWJjLTkyYzYtYzM4ODg4ODFmMTY0IWIyNTAzfGNwc2VydmljZXMtc2VjdXJlZCFiMzkxOm9zRzgvSC9hOGtkcHVHNzl1L2JVYTJ0V0FiMD0="
	response = webclient.DownloadString(
		"https://cpqprojdevamat.authentication.us10.hana.ondemand.com:443/oauth/token?grant_type=client_credentials"
	)
	response = eval(response)
	Request_URL = "https://cpservices-product-configuration.cfapps.us10.hana.ondemand.com/api/v2/configurations?autoCleanup=False"
	webclient.Headers[System.Net.HttpRequestHeader.Authorization] = "Bearer " + str(response["access_token"])
	requestdata = '{"productKey":"'+ ProductPartnumber+ '","date":"'+gettodaydate+'","context":[{"name":"VBAP-MATNR","value":"'+ ProductPartnumber+ '"}]}'
	
	Log.Info("requestdata--" + str(requestdata))
	response1 = webclient.UploadString(Request_URL, str(requestdata))
	response1 = str(response1).replace(": true", ': "true"').replace(": false", ': "false"')
	return eval(response1)
#not using this function start	#####################
# def ancillary_service_Z0046():
# 	Log.Info('136----')
# 	if TreeParam == "Z0091":
# 		Log.Info('Z0091-1-Z0046---')
# 		get_ancillaryservice = Sql.GetFirst("select * from SAQTSE where QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{revision_rec_id}' AND SERVICE_ID = '{ServiceId}'""".format(UserId=userId, QuoteRecordId=Qt_rec_id, ServiceId='Z0046', revision_rec_id = rev_rec_id))
# 		if get_ancillaryservice:
# 			Log.Info('Z0091--Z0046---')
# 			# SAQSFE_ancillary_query="""
# 			# 	INSERT SAQSFE (ENTITLEMENT_XML,QUOTE_ID,QUOTE_NAME,QUOTE_RECORD_ID,QTEREV_RECORD_ID,QTEREV_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,	
# 			# 	CPS_CONFIGURATION_ID, CPS_MATCH_ID,QTESRVENT_RECORD_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,QTESRVFBL_RECORD_ID,CONFIGURATION_STATUS,QUOTE_SERVICE_FAB_LOC_ENT_RECORD_ID, CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED)
# 			# 	SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_FAB_LOC_ENT_RECORD_ID, {UserId} as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM (
# 			# 	SELECT 
# 			# 		DISTINCT	
# 			# 		SAQTSE.ENTITLEMENT_XML,SAQTSE.QUOTE_ID,SAQTSE.QUOTE_NAME,SAQTSE.QUOTE_RECORD_ID,SAQTSE.QTEREV_RECORD_ID,SAQTSE.QTEREV_ID,SAQTSE.SERVICE_DESCRIPTION,SAQTSE.SERVICE_ID,SAQTSE.SERVICE_RECORD_ID,SAQTSE.SALESORG_ID,SAQTSE.SALESORG_NAME,SAQTSE.SALESORG_RECORD_ID,SAQTSE.CPS_CONFIGURATION_ID, SAQTSE.CPS_MATCH_ID,SAQTSE.QUOTE_SERVICE_ENTITLEMENT_RECORD_ID as QTESRVENT_RECORD_ID,SAQSFB.FABLOCATION_ID, SAQSFB.FABLOCATION_NAME, SAQSFB.FABLOCATION_RECORD_ID, SAQSFB.QUOTE_SERVICE_FAB_LOCATION_RECORD_ID as QTESRVFBL_RECORD_ID,SAQTSE.CONFIGURATION_STATUS
# 			# 	FROM
# 			# 	SAQTSE (NOLOCK)
# 			# 	JOIN SAQSFB ON SAQSFB.SERVICE_ID = 'Z0091' AND SAQSFB.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID AND SAQSFB.QTEREV_RECORD_ID = SAQTSE.QTEREV_RECORD_ID
# 			# 	WHERE SAQTSE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQTSE.QTEREV_RECORD_ID = '{revision_rec_id}' AND SAQTSE.SERVICE_ID = '{ServiceId}') IQ""".format(UserId=userId, QuoteRecordId=Qt_rec_id, ServiceId='Z0046', revision_rec_id = rev_rec_id)
# 			# Log.Info('SAQSFE_ancillary_query--148----ROLL DOWN----'+str(SAQSFE_ancillary_query))
# 			# Sql.RunQuery(SAQSFE_ancillary_query)



# 			qtqtse_query_anc="""
# 				INSERT SAQSGE (KB_VERSION,QUOTE_ID,QUOTE_NAME,QUOTE_RECORD_ID,QTEREV_RECORD_ID,QTEREV_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,	
# 				CPS_CONFIGURATION_ID, CPS_MATCH_ID,GREENBOOK,GREENBOOK_RECORD_ID,QTESRVENT_RECORD_ID,ENTITLEMENT_XML,CONFIGURATION_STATUS, QUOTE_SERVICE_GREENBOOK_ENTITLEMENT_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED )
# 				SELECT OQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_GREENBOOK_ENTITLEMENT_RECORD_ID, {UserId} as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM (SELECT IQ.*,M.ENTITLEMENT_XML,M.CONFIGURATION_STATUS FROM(
# 				SELECT 
# 					DISTINCT	
# 					SAQTSE.KB_VERSION,SAQTSE.QUOTE_ID,SAQTSE.QUOTE_NAME,SAQTSE.QUOTE_RECORD_ID,SAQTSE.QTEREV_RECORD_ID,SAQTSE.QTEREV_ID,SAQTSE.SERVICE_DESCRIPTION,SAQTSE.SERVICE_ID,SAQTSE.SERVICE_RECORD_ID,SAQTSE.SALESORG_ID,SAQTSE.SALESORG_NAME,SAQTSE.SALESORG_RECORD_ID,SAQTSE.CPS_CONFIGURATION_ID, SAQTSE.CPS_MATCH_ID,SAQSCO.GREENBOOK,SAQSCO.GREENBOOK_RECORD_ID,SAQTSE.QUOTE_SERVICE_ENTITLEMENT_RECORD_ID as QTESRVENT_RECORD_ID
# 				FROM
# 				SAQTSE (NOLOCK)
# 				JOIN SAQSCO  (NOLOCK) ON SAQSCO.SERVICE_ID = 'Z0091' AND SAQSCO.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID  AND SAQSCO.QTEREV_RECORD_ID = SAQTSE.QTEREV_RECORD_ID 
# 				WHERE SAQTSE.QUOTE_RECORD_ID = '{QuoteRecordId}'  AND SAQTSE.QTEREV_RECORD_ID = '{revision_rec_id}' AND SAQTSE.SERVICE_ID = '{ServiceId}') IQ )OQ""".format(UserId=userId, QuoteRecordId=Qt_rec_id, ServiceId='Z0046', revision_rec_id = rev_rec_id)
# 			Log.Info("qtqtse_query_anc---163------"+str(qtqtse_query_anc))
# 			Sql.RunQuery(qtqtse_query_anc)
# 			#ENTITLEMENT SV TO CE
# 			qtqsce_anc_query="""
# 				INSERT SAQSCE
# 				(KB_VERSION,ENTITLEMENT_XML,CONFIGURATION_STATUS,EQUIPMENT_ID,EQUIPMENT_RECORD_ID,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_RECORD_ID,QTEREV_ID,QTESRVCOB_RECORD_ID,QTESRVENT_RECORD_ID,SERIAL_NO,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,CPS_CONFIGURATION_ID,CPS_MATCH_ID,GREENBOOK,GREENBOOK_RECORD_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,QUOTE_SERVICE_COVERED_OBJ_ENTITLEMENTS_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED) 
# 				SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_COVERED_OBJ_ENTITLEMENTS_RECORD_ID, {UserId} as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM (
# 				SELECT 
# 				SAQTSE.KB_VERSION,SAQTSE.ENTITLEMENT_XML,SAQTSE.CONFIGURATION_STATUS,SAQSCO.EQUIPMENT_ID,SAQSCO.EQUIPMENT_RECORD_ID,SAQTSE.QUOTE_ID,SAQTSE.QUOTE_RECORD_ID,SAQTSE.QTEREV_RECORD_ID,SAQTSE.QTEREV_ID,SAQSCO.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID as QTESRVCOB_RECORD_ID,SAQTSE.QUOTE_SERVICE_ENTITLEMENT_RECORD_ID as QTESRVENT_RECORD_ID,SAQSCO.SERIAL_NO,SAQTSE.SERVICE_DESCRIPTION,SAQTSE.SERVICE_ID,SAQTSE.SERVICE_RECORD_ID,SAQTSE.CPS_CONFIGURATION_ID,SAQTSE.CPS_MATCH_ID,SAQSCO.GREENBOOK,SAQSCO.GREENBOOK_RECORD_ID,SAQSCO.FABLOCATION_ID,SAQSCO.FABLOCATION_NAME,SAQSCO.FABLOCATION_RECORD_ID,SAQTSE.SALESORG_ID,SAQTSE.SALESORG_NAME,SAQTSE.SALESORG_RECORD_ID
# 				FROM	
# 				SAQTSE (NOLOCK)
# 				JOIN SAQSCO (NOLOCK) ON SAQSCO.SERVICE_ID = 'Z0091' AND SAQSCO.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID  AND SAQSCO.QTEREV_RECORD_ID = SAQTSE.QTEREV_RECORD_ID 
# 				WHERE SAQTSE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQTSE.QTEREV_RECORD_ID = '{revision_rec_id}' AND SAQTSE.SERVICE_ID = '{ServiceId}' AND SAQSCO.EQUIPMENT_ID not in (SELECT EQUIPMENT_ID FROM SAQSCE (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}'   AND QTEREV_RECORD_ID = '{revision_rec_id}' AND SERVICE_ID = '{ServiceId}')) IQ""".format(
# 				UserId=userId, 
# 				QuoteRecordId=Qt_rec_id, 
# 				ServiceId='Z0046', 
# 				revision_rec_id = rev_rec_id)
# 			Log.Info('@qtqsce_anc_query-renewal----179=---Qt_rec_id--'+str(qtqsce_anc_query))
# 			Sql.RunQuery(qtqsce_anc_query)
			
# 			# get_SAQSCO = Sql.GetFirst("""SELECT count(*) as cnt FROM SAQSCO (NOLOCK) WHERE SAQSCO.QUOTE_RECORD_ID = '{ContractId}' AND QTEREV_RECORD_ID = '{revision_rec_id}'""".format(ContractId=Qt_rec_id,revision_rec_id = rev_rec_id))
# 			# Log.Info("get_SAQSCO---> "+ str(get_SAQSCO.cnt))
			
# 			# get_SAQSCE = Sql.GetFirst("""SELECT count(*) as cnt FROM SAQSCE (NOLOCK) WHERE SAQSCE.QUOTE_RECORD_ID = '{ContractId}' AND QTEREV_RECORD_ID = '{revision_rec_id}'""".format(ContractId=Qt_rec_id,revision_rec_id = rev_rec_id))
# 			# Log.Info("get_SAQSCE---> "+ str(get_SAQSCE.cnt))

# 			# Duplicate records removed from assembly level entitlement in offering - Start
# 			Sql.RunQuery("""DELETE FROM SAQSAE WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID = '{ServiceId}'""".format(QuoteRecordId=Qt_rec_id,RevisionRecordId=rev_rec_id,ServiceId='Z0046'))
# 			# Duplicate records removed from assembly level entitlement in offering - End
# 			SAQSAE_ent_anc_renewal = """INSERT SAQSAE (KB_VERSION,EQUIPMENT_ID,EQUIPMENT_RECORD_ID,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_RECORD_ID,QTEREV_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,CPS_CONFIGURATION_ID,CPS_MATCH_ID,GREENBOOK,GREENBOOK_RECORD_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,ASSEMBLY_DESCRIPTION,ASSEMBLY_ID,ASSEMBLY_RECORD_ID,QTESRVCOA_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,ENTITLEMENT_XML,CONFIGURATION_STATUS,QTESRVCOE_RECORD_ID,QUOTE_SERVICE_COV_OBJ_ASS_ENT_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED) SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_COV_OBJ_ASS_ENT_RECORD_ID, {UserId} as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM(SELECT IQ.*,M.ENTITLEMENT_XML,M.CONFIGURATION_STATUS,M.QUOTE_SERVICE_COVERED_OBJ_ENTITLEMENTS_RECORD_ID as QTESRVCOE_RECORD_ID FROM ( SELECT DISTINCT SAQTSE.KB_VERSION,SAQSCA.EQUIPMENT_ID,SAQSCA.EQUIPMENT_RECORD_ID,SAQTSE.QUOTE_ID,SAQTSE.QUOTE_RECORD_ID,SAQTSE.QTEREV_RECORD_ID,SAQTSE.QTEREV_ID,SAQTSE.SERVICE_DESCRIPTION,SAQTSE.SERVICE_ID,SAQTSE.SERVICE_RECORD_ID,SAQTSE.CPS_CONFIGURATION_ID,SAQTSE.CPS_MATCH_ID,SAQSCA.GREENBOOK,SAQSCA.GREENBOOK_RECORD_ID,SAQSCA.FABLOCATION_ID,SAQSCA.FABLOCATION_NAME,SAQSCA.FABLOCATION_RECORD_ID,SAQSCA.ASSEMBLY_DESCRIPTION,SAQSCA.ASSEMBLY_ID,SAQSCA.ASSEMBLY_RECORD_ID,SAQSCA.QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID as QTESRVCOA_RECORD_ID,SAQTSE.SALESORG_ID,SAQTSE.SALESORG_NAME,SAQTSE.SALESORG_RECORD_ID FROM SAQTSE (NOLOCK) JOIN (SELECT * FROM SAQSCA (NOLOCK) WHERE SAQSCA.QUOTE_RECORD_ID = '{ContractId}' AND SAQSCA.QTEREV_RECORD_ID = '{revision_rec_id}' ) SAQSCA ON SAQTSE.QUOTE_RECORD_ID = SAQSCA.QUOTE_RECORD_ID AND SAQTSE.QTEREV_RECORD_ID = SAQSCA.QTEREV_RECORD_ID AND SAQTSE.SERVICE_RECORD_ID = SAQSCA.SERVICE_RECORD_ID WHERE SAQTSE.QUOTE_RECORD_ID = '{ContractId}' AND SAQTSE.QTEREV_RECORD_ID = '{revision_rec_id}' AND SAQTSE.SERVICE_ID = '{serviceId}') IQ JOIN SAQSCE (NOLOCK) M ON M.SERVICE_RECORD_ID = IQ.SERVICE_RECORD_ID AND M.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND M.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND M.EQUIPMENT_ID = IQ.EQUIPMENT_ID )IQ""".format(UserId=userId,  ContractId=Qt_rec_id, serviceId='Z0046', revision_rec_id = rev_rec_id)
# 			Sql.RunQuery(SAQSAE_ent_anc_renewal)
# 			Log.Info('SAQSAE_ent_anc_renewal--393--renewal-1881-----'+str(SAQSAE_ent_anc_renewal))
#not using this function end	#####################
def _construct_dict_xml(updateentXML):
	entxmldict = {}
	pattern_tag = re.compile(r'(<QUOTE_ITEM_ENTITLEMENT>[\w\W]*?</QUOTE_ITEM_ENTITLEMENT>)')
	pattern_name = re.compile(r'<ENTITLEMENT_ID>([^>]*?)</ENTITLEMENT_ID>')
	entitlement_display_value_tag_pattern = re.compile(r'<ENTITLEMENT_DISPLAY_VALUE>([^>]*?)</ENTITLEMENT_DISPLAY_VALUE>')
	display_val_dict = {}
	if updateentXML:
		for m in re.finditer(pattern_tag, updateentXML):
			sub_string = m.group(1)
			x=re.findall(pattern_name,sub_string)
			if x:
				entitlement_display_value_tag_match = re.findall(entitlement_display_value_tag_pattern,sub_string)
				if entitlement_display_value_tag_match:
					display_val_dict[x[0]] = entitlement_display_value_tag_match[0]
			entxmldict[x[0]]=sub_string
	return entxmldict,display_val_dict

def entitlemt_attr_update(entitlement_table, where):
	get_equipment = Sql.GetList("SELECT * FROM {} {}".format(entitlement_table, where.replace('SRC.','')))
	entitlement_details = [{
								"field":["INTCPV","Intercept","AGS_{}_VAL_INTCPT".format(TreeParam)]						
								},
								{
								"field":["INTCPC","Intercept Coefficient","AGS_{}_VAL_INTCCO".format(TreeParam)]
								},
								{
								"field":["OSSVDV","Total Cost W/O Seedstock","AGS_{}_VAL_TBCOST".format(TreeParam)]	
								},
								{
								"field":["LTCOSS","Total Cost w/o Seedstock Coeff","AGS_{}_VAL_TBCOCO".format(TreeParam)]
								},
								{
								"field":["POFVDV","Product Offering","AGS_{}_VAL_POFFER".format(TreeParam)]	
								},
								{
								"field":["POFVDC","Product Offering Coefficient","AGS_{}_VAL_POFFCO".format(TreeParam)]
								},
								{
								"field":["GBKVDV","Greenbook","AGS_{}_VAL_GRNBKV".format(TreeParam)]	
								},
								{
								"field":["GBKVDC","Greenbook Coefficient","AGS_{}_VAL_GRNBCO".format(TreeParam)]
								},
								{
								"field":["UIMVDV","Uptime Improvement","AGS_{}_VAL_UPIMPV".format(TreeParam)]	
								},
								{
								"field":["UIMVDC","Uptime Improvement Coefficient","AGS_{}_VAL_UPIMCO".format(TreeParam)]
								},
								{
								"field":["CAVVDV","Capital Avoidance","AGS_{}_VAL_CAPAVD".format(TreeParam)]	
								},
								{
								"field":["CAVVDC","Capital Avoidance Coefficient","AGS_{}_VAL_CAPACO".format(TreeParam)]
								},
								{
								"field":["WNDVDV","Wafer Node","AGS_{}_VAL_WAFNOD".format(TreeParam)]	
								},
								{
								"field":["WNDVDC","Wafer Node Coefficient","AGS_{}_VAL_WAFNCO".format(TreeParam)]
								},
								{
								"field":["CCRTMV","Contract Coverage & Response Time","AGS_{}_VAL_CCRTME".format(TreeParam)]	
								},
								{
								"field":["CCRTMC","Contract Coverage & Response Time Coefficient","AGS_{}_VAL_CCRTCO".format(TreeParam)]
								},
								{
								"field":["SCMVDV","Service Complexity","AGS_{}_VAL_SCCCDF".format(TreeParam)]
								},
								{
								"field":["SCMVDC", "Service Complexity Coefficient", "AGS_{}_VAL_SCCCCO".format(TreeParam)]
								},
								{
								"field":["CCDFFV","Cleaning Coating Differentiation","AGS_{}_VAL_CCDVAL".format(TreeParam)]
								},
								{
								"field":["CCDFFC", "Cleaning Coating Diff coeff.", "AGS_{}_VAL_CCDVCO".format(TreeParam)]
								},
								{
								"field":["NPIVDV","NPI","AGS_{}_VAL_NPIREC".format(TreeParam)]
								},	
								{
								"field":["NPIVDC", "NPI Coefficient", "AGS_{}_VAL_NPICOF".format(TreeParam)]
								},	
								{
								"field":["DTPVDV","Device Type","AGS_{}_VAL_DEVTYP".format(TreeParam)]
								},
								{
								"field":["DTPVDC", "Device Type Coefficient", "AGS_{}_VAL_DEVTCO".format(TreeParam)]
								},	
								{
								"field":["CSTVDV","# CSA Tools per Fab","AGS_{}_VAL_TLSFAB".format(TreeParam)]
								},	
								{
								"field":["CSTVDC", "# CSA Tools per Fab Coefficient", "AGS_{}_VAL_TLSFCO".format(TreeParam)]
								},	
								{
								"field":["CSGVDV","Customer Segment","AGS_{}_VAL_CSTSEG".format(TreeParam)]
								},
								{
								"field":["CSGVDC", "Customer Segment Coefficent", "AGS_{}_VAL_CSSGCO".format(TreeParam)]
								},	
								{
								"field":["QRQVDV","Quality Required","AGS_{}_VAL_QLYREQ".format(TreeParam)]
								},
								{
								"field":["QRQVDC", "Quality Required Coefficient", "AGS_{}_VAL_QLYRCO".format(TreeParam)]
								},	
								{
								"field":["SVCVDV","Service Competition","AGS_{}_VAL_SVCCMP".format(TreeParam)]
								},
								{
								"field":["SVCVDC", "Service Competition Coefficient", "AGS_{}_VAL_SVCCCO".format(TreeParam)]
								},
								{
								"field":["RKFVDV","Risk Factor","AGS_{}_VAL_RSKFVD".format(TreeParam)]
								},
								{
								"field":["RKFVDC", "Risk Factor Coefficient", "AGS_{}_VAL_RSKFCO".format(TreeParam)]
								},
								{
								"field":["PBPVDV","PDC Base Price","AGS_{}_VAL_PDCBSE".format(TreeParam)]
								},
								{
								"field":["PBPVDC", "PDC Base Price Coefficient", "AGS_{}_VAL_PDCBCO".format(TreeParam)]
								},
								{
								"field":["CMLAB_ENT","Corrective Maintenance Labor","AGS_{}_NET_CRMALB".format(TreeParam)]
								},		
								{
								"field":["CNSMBL_ENT","Consumable","AGS_{}_TSC_CONSUM".format(TreeParam)]
								},
								{
								"field":["CNTCVG_ENT","Contract Coverage","AGS_{}_CVR_CNTCOV".format(TreeParam)]
								},	
								{
								"field":["NCNSMB_ENT","Non-Consumable","AGS_{}_TSC_NONCNS".format(TreeParam)]
								},	
								{
								"field":["PMEVNT_ENT","Quote Type","AGS_{}_PQB_QTETYP".format(TreeParam)]
								},		
								{
								"field":["PMLAB_ENT","Preventative Maintenance Labor","AGS_{}_NET_PRMALB".format(TreeParam)]
								},	
								{
								"field":["PRMKPI_ENT","Primary KPI. Perf Guarantee","AGS_{}_KPI_PRPFGT".format(TreeParam)]
								},
								{
								"field":["OFRING","Product Offering","AGS_{}_VAL_POFFER".format(TreeParam)]
								},	
								{
								"field":["QTETYP","Quote Type","AGS_{}_PQB_QTETYP".format(TreeParam)]
								},	
								{
								"field":["BILTYP","Billing Type","AGS_{}_PQB_BILTYP".format(TreeParam)]
								},	
								{
								"field":["BPTKPI","Bonus & Penalty Tied to KPI","AGS_{}_KPI_BPTKPI".format(TreeParam)]
								},
								{
								"field":["ATGKEY","Additional Target KPI","AGS_{}_KPI_TGTKPI".format(TreeParam)]
								},	
								{
								"field":["ATNKEY","Additional Target KPI(Non-std)","AGS_{}_KPI_TGKPNS".format(TreeParam)]
								},
								{
								"field":["NWPTON","New Parts Only","AGS_{}_TSC_RPPNNW".format(TreeParam)]
								},
								{
								"field":["HEDBIN","Head break-in","AGS_{}_STT_HDBRIN".format(TreeParam)]
								},
						]
			
	if get_equipment:
		for ent_rec in get_equipment:
			addtional_whr = ''
			update_values = ""
			if entitlement_table == 'SAQSCE':
				addtional_whr = " AND GREENBOOK = '{}' AND EQUIPMENT_ID = '{}'".format(ent_rec.GREENBOOK,ent_rec.EQUIPMENT_ID )
			elif entitlement_table == 'SAQGPE':
				addtional_whr = " AND GREENBOOK = '{}' AND GOT_CODE = '{}' AND PM_ID = '{}'".format(ent_rec.GREENBOOK,ent_rec.GOT_CODE,  ent_rec.PM_ID)
			get_xml_dict,dict_val = _construct_dict_xml(ent_rec.ENTITLEMENT_XML)
			#Trace.Write("dict_val--"+str(dict_val))
			for entitlement_detail in entitlement_details:
				entitlement_table_col = entitlement_detail['field'][0]
				entitlement_id = entitlement_detail['field'][2]
				if entitlement_id in dict_val.keys():
					entitlement_disp_val = dict_val[entitlement_id]
					update_values += ", {} = '{}' ".format(entitlement_table_col, entitlement_disp_val ) 
			if update_values:
				update_query = "UPDATE {entitlement_table} SET {cols}  {where} {addtional_whr}".format(entitlement_table = entitlement_table, cols = update_values, where =where.replace('SRC.',''),addtional_whr= addtional_whr )
				update_query = update_query.replace('SET ,','SET ')
				#Log.Info('update_query---'+str(update_query))
				Sql.RunQuery(update_query)
	
def CoveredObjEntitlement():
	#ENTITLEMENT SV TO FE
	
	# SAQSFE_query="""
	# 	INSERT SAQSFE (ENTITLEMENT_XML,QUOTE_ID,QUOTE_NAME,QUOTE_RECORD_ID,QTEREV_RECORD_ID,QTEREV_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,	
	# 	CPS_CONFIGURATION_ID, CPS_MATCH_ID,QTESRVENT_RECORD_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,QTESRVFBL_RECORD_ID,CONFIGURATION_STATUS,QUOTE_SERVICE_FAB_LOC_ENT_RECORD_ID, CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED)
	# 	SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_FAB_LOC_ENT_RECORD_ID, {UserId} as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM (
	# 	SELECT 
	# 		DISTINCT	
	# 		SAQTSE.ENTITLEMENT_XML,SAQTSE.QUOTE_ID,SAQTSE.QUOTE_NAME,SAQTSE.QUOTE_RECORD_ID,SAQTSE.QTEREV_RECORD_ID,SAQTSE.QTEREV_ID,SAQTSE.SERVICE_DESCRIPTION,SAQTSE.SERVICE_ID,SAQTSE.SERVICE_RECORD_ID,SAQTSE.SALESORG_ID,SAQTSE.SALESORG_NAME,SAQTSE.SALESORG_RECORD_ID,SAQTSE.CPS_CONFIGURATION_ID, SAQTSE.CPS_MATCH_ID,SAQTSE.QUOTE_SERVICE_ENTITLEMENT_RECORD_ID as QTESRVENT_RECORD_ID,SAQSFB.FABLOCATION_ID, SAQSFB.FABLOCATION_NAME, SAQSFB.FABLOCATION_RECORD_ID, SAQSFB.QUOTE_SERVICE_FAB_LOCATION_RECORD_ID as QTESRVFBL_RECORD_ID,SAQTSE.CONFIGURATION_STATUS
	# 	FROM
	# 	SAQTSE (NOLOCK)
	# 	JOIN SAQSFB ON SAQSFB.SERVICE_RECORD_ID = SAQTSE.SERVICE_RECORD_ID AND SAQSFB.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID AND SAQSFB.QTEREV_RECORD_ID = SAQTSE.QTEREV_RECORD_ID
	# 	WHERE SAQTSE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQTSE.QTEREV_RECORD_ID = '{revision_rec_id}' AND SAQTSE.SERVICE_ID = '{ServiceId}') IQ""".format(UserId=userId, QuoteRecordId=Qt_rec_id, ServiceId=TreeParam, revision_rec_id = rev_rec_id)
	# Log.Info('SAQSFE_query--148----ROLL DOWN----'+str(SAQSFE_query))
	# Sql.RunQuery(SAQSFE_query)
	#ENTITLEMENT SV TO GB
	
	# qtqtse_query="""
	# 	 (KB_VERSION,QUOTE_ID,QUOTE_NAME,QUOTE_RECORD_ID,QTEREV_RECORD_ID,QTEREV_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,	
	# 	CPS_CONFIGURATION_ID, CPS_MATCH_ID,GREENBOOK,GREENBOOK_RECORD_ID,QTESRVENT_RECORD_ID,QTSFBLENT_RECORD_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,ENTITLEMENT_XML,CONFIGURATION_STATUS, QUOTE_SERVICE_GREENBOOK_ENTITLEMENT_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED )
	# 	SELECT OQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_GREENBOOK_ENTITLEMENT_RECORD_ID, {UserId} as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM (SELECT IQ.*,M.ENTITLEMENT_XML,M.CONFIGURATION_STATUS FROM(
	# 	SELECT 
	# 		DISTINCT	
	# 		SAQTSE.KB_VERSION,SAQTSE.QUOTE_ID,SAQTSE.QUOTE_NAME,SAQTSE.QUOTE_RECORD_ID,SAQTSE.QTEREV_RECORD_ID,SAQTSE.QTEREV_ID,SAQTSE.SERVICE_DESCRIPTION,SAQTSE.SERVICE_ID,SAQTSE.SERVICE_RECORD_ID,SAQTSE.SALESORG_ID,SAQTSE.SALESORG_NAME,SAQTSE.SALESORG_RECORD_ID,SAQTSE.CPS_CONFIGURATION_ID, SAQTSE.CPS_MATCH_ID,SAQSCO.GREENBOOK,SAQSCO.GREENBOOK_RECORD_ID,SAQTSE.QUOTE_SERVICE_ENTITLEMENT_RECORD_ID as QTESRVENT_RECORD_ID,SAQSFE.QUOTE_SERVICE_FAB_LOC_ENT_RECORD_ID as QTSFBLENT_RECORD_ID,SAQSFE.FABLOCATION_ID,SAQSFE.FABLOCATION_NAME,SAQSFE.FABLOCATION_RECORD_ID
	# 	FROM
	# 	SAQTSE (NOLOCK)
	# 	JOIN SAQSCO  (NOLOCK) ON SAQSCO.SERVICE_RECORD_ID = SAQTSE.SERVICE_RECORD_ID AND SAQSCO.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID  AND SAQSCO.QTEREV_RECORD_ID = SAQTSE.QTEREV_RECORD_ID JOIN SAQSFE ON SAQSFE.SERVICE_RECORD_ID = SAQTSE.SERVICE_RECORD_ID AND SAQSFE.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID AND SAQSFE.QTEREV_RECORD_ID = SAQTSE.QTEREV_RECORD_ID 
	# 	WHERE SAQTSE.QUOTE_RECORD_ID = '{QuoteRecordId}'  AND SAQTSE.QTEREV_RECORD_ID = '{revision_rec_id}' AND SAQTSE.SERVICE_ID = '{ServiceId}') IQ JOIN SAQSFE (NOLOCK) M ON IQ.QTSFBLENT_RECORD_ID = QUOTE_SERVICE_FAB_LOC_ENT_RECORD_ID )OQ""".format(UserId=userId, QuoteRecordId=Qt_rec_id, ServiceId=TreeParam, revision_rec_id = rev_rec_id)


	qtqtse_query= """INSERT SAQSGE (KB_VERSION,QUOTE_ID,QUOTE_NAME,QUOTE_RECORD_ID,QTEREV_RECORD_ID,QTEREV_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,	
		CPS_CONFIGURATION_ID, CPS_MATCH_ID,GREENBOOK,GREENBOOK_RECORD_ID,QTESRVENT_RECORD_ID,ENTITLEMENT_XML,CONFIGURATION_STATUS, QUOTE_SERVICE_GREENBOOK_ENTITLEMENT_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED )
		SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_GREENBOOK_ENTITLEMENT_RECORD_ID, '{username}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM (SELECT DISTINCT SAQTSE.KB_VERSION,SAQTSE.QUOTE_ID,SAQTSE.QUOTE_NAME,SAQTSE.QUOTE_RECORD_ID,SAQTSE.QTEREV_RECORD_ID,SAQTSE.QTEREV_ID,SAQTSE.SERVICE_DESCRIPTION,SAQTSE.SERVICE_ID,SAQTSE.SERVICE_RECORD_ID,SAQTSE.SALESORG_ID,SAQTSE.SALESORG_NAME,SAQTSE.SALESORG_RECORD_ID,	
		SAQTSE.CPS_CONFIGURATION_ID, SAQTSE.CPS_MATCH_ID,SAQSCO.GREENBOOK,SAQSCO.GREENBOOK_RECORD_ID,SAQTSE.QUOTE_SERVICE_ENTITLEMENT_RECORD_ID as QTESRVENT_RECORD_ID,SAQTSE.ENTITLEMENT_XML,SAQTSE.CONFIGURATION_STATUS FROM
	SAQTSE (NOLOCK) JOIN SAQSCO  (NOLOCK) ON SAQSCO.SERVICE_RECORD_ID = SAQTSE.SERVICE_RECORD_ID AND SAQSCO.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID  AND SAQSCO.QTEREV_RECORD_ID = SAQTSE.QTEREV_RECORD_ID  
		WHERE SAQTSE.QUOTE_RECORD_ID ='{QuoteRecordId}'  AND SAQTSE.QTEREV_RECORD_ID = '{revision_rec_id}' AND SAQTSE.SERVICE_ID = '{ServiceId}')IQ""".format(username=userName, QuoteRecordId=Qt_rec_id, ServiceId=TreeParam, revision_rec_id = rev_rec_id)

	# qtqtse_query="""
	# 	INSERT SAQSGE (KB_VERSION,QUOTE_ID,QUOTE_NAME,QUOTE_RECORD_ID,QTEREV_RECORD_ID,QTEREV_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,	
	# 	CPS_CONFIGURATION_ID, CPS_MATCH_ID,GREENBOOK,GREENBOOK_RECORD_ID,QTESRVENT_RECORD_ID,ENTITLEMENT_XML,CONFIGURATION_STATUS, QUOTE_SERVICE_GREENBOOK_ENTITLEMENT_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED )
	# 	SELECT OQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_GREENBOOK_ENTITLEMENT_RECORD_ID, {UserId} as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM (SELECT IQ.*,M.ENTITLEMENT_XML,M.CONFIGURATION_STATUS FROM(
	# 	SELECT 
	# 		DISTINCT	
	# 		SAQTSE.KB_VERSION,SAQTSE.QUOTE_ID,SAQTSE.QUOTE_NAME,SAQTSE.QUOTE_RECORD_ID,SAQTSE.QTEREV_RECORD_ID,SAQTSE.QTEREV_ID,SAQTSE.SERVICE_DESCRIPTION,SAQTSE.SERVICE_ID,SAQTSE.SERVICE_RECORD_ID,SAQTSE.SALESORG_ID,SAQTSE.SALESORG_NAME,SAQTSE.SALESORG_RECORD_ID,SAQTSE.CPS_CONFIGURATION_ID, SAQTSE.CPS_MATCH_ID,SAQSCO.GREENBOOK,SAQSCO.GREENBOOK_RECORD_ID,SAQTSE.QUOTE_SERVICE_ENTITLEMENT_RECORD_ID as QTESRVENT_RECORD_ID
	# 	FROM
	# 	SAQTSE (NOLOCK)
	# 	JOIN SAQSCO  (NOLOCK) ON SAQSCO.SERVICE_RECORD_ID = SAQTSE.SERVICE_RECORD_ID AND SAQSCO.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID  AND SAQSCO.QTEREV_RECORD_ID = SAQTSE.QTEREV_RECORD_ID  
	# 	WHERE SAQTSE.QUOTE_RECORD_ID = '{QuoteRecordId}'  AND SAQTSE.QTEREV_RECORD_ID = '{revision_rec_id}' AND SAQTSE.SERVICE_ID = '{ServiceId}') IQ )OQ""".format(UserId=userId, QuoteRecordId=Qt_rec_id, ServiceId=TreeParam, revision_rec_id = rev_rec_id)
	Log.Info("SAQSGE_query---163--156--saqsgeinsert----"+str(qtqtse_query))
	Sql.RunQuery(qtqtse_query)
	#ENTITLEMENT SV TO CE
	qtqsce_query="""
		INSERT SAQSCE
		(KB_VERSION,ENTITLEMENT_XML,CONFIGURATION_STATUS,EQUIPMENT_ID,EQUIPMENT_RECORD_ID,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_RECORD_ID,QTEREV_ID,QTESRVCOB_RECORD_ID,QTESRVENT_RECORD_ID,SERIAL_NO,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,CPS_CONFIGURATION_ID,CPS_MATCH_ID,GREENBOOK,GREENBOOK_RECORD_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,QUOTE_SERVICE_COVERED_OBJ_ENTITLEMENTS_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED) 
		SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_COVERED_OBJ_ENTITLEMENTS_RECORD_ID, '{username}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM (
		SELECT 
		SAQTSE.KB_VERSION,SAQTSE.ENTITLEMENT_XML,SAQTSE.CONFIGURATION_STATUS,SAQSCO.EQUIPMENT_ID,SAQSCO.EQUIPMENT_RECORD_ID,SAQTSE.QUOTE_ID,SAQTSE.QUOTE_RECORD_ID,SAQTSE.QTEREV_RECORD_ID,SAQTSE.QTEREV_ID,SAQSCO.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID as QTESRVCOB_RECORD_ID,SAQTSE.QUOTE_SERVICE_ENTITLEMENT_RECORD_ID as QTESRVENT_RECORD_ID,SAQSCO.SERIAL_NO,SAQTSE.SERVICE_DESCRIPTION,SAQTSE.SERVICE_ID,SAQTSE.SERVICE_RECORD_ID,SAQTSE.CPS_CONFIGURATION_ID,SAQTSE.CPS_MATCH_ID,SAQSCO.GREENBOOK,SAQSCO.GREENBOOK_RECORD_ID,SAQSCO.FABLOCATION_ID,SAQSCO.FABLOCATION_NAME,SAQSCO.FABLOCATION_RECORD_ID,SAQTSE.SALESORG_ID,SAQTSE.SALESORG_NAME,SAQTSE.SALESORG_RECORD_ID
		FROM	
		SAQTSE (NOLOCK)
		JOIN SAQSCO (NOLOCK) ON SAQSCO.SERVICE_RECORD_ID = SAQTSE.SERVICE_RECORD_ID AND SAQSCO.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID  AND SAQSCO.QTEREV_RECORD_ID = SAQTSE.QTEREV_RECORD_ID 
		WHERE SAQTSE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQTSE.QTEREV_RECORD_ID = '{revision_rec_id}' AND SAQTSE.SERVICE_ID = '{ServiceId}' AND SAQSCO.EQUIPMENT_ID not in (SELECT EQUIPMENT_ID FROM SAQSCE (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}'   AND QTEREV_RECORD_ID = '{revision_rec_id}' AND SERVICE_ID = '{ServiceId}')) IQ""".format(
		username=userName, 
		QuoteRecordId=Qt_rec_id, 
		ServiceId=TreeParam, 
		revision_rec_id = rev_rec_id)
	Log.Info('@182qtqsce_query-renewal----179=---Qt_rec_id--'+str(qtqsce_query))
	Sql.RunQuery(qtqsce_query)
	
	# get_SAQSCO = Sql.GetFirst("""SELECT count(*) as cnt FROM SAQSCO (NOLOCK) WHERE SAQSCO.QUOTE_RECORD_ID = '{ContractId}' AND QTEREV_RECORD_ID = '{revision_rec_id}'""".format(ContractId=Qt_rec_id,revision_rec_id = rev_rec_id))
	# Log.Info("get_SAQSCO---> "+ str(get_SAQSCO.cnt))
	
	# get_SAQSCE = Sql.GetFirst("""SELECT count(*) as cnt FROM SAQSCE (NOLOCK) WHERE SAQSCE.QUOTE_RECORD_ID = '{ContractId}' AND QTEREV_RECORD_ID = '{revision_rec_id}'""".format(ContractId=Qt_rec_id,revision_rec_id = rev_rec_id))
	# Log.Info("get_SAQSCE---> "+ str(get_SAQSCE.cnt))

	# Duplicate records removed from assembly level entitlement in offering - Start
	Sql.RunQuery("""DELETE FROM SAQSAE WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID = '{ServiceId}'""".format(QuoteRecordId=Qt_rec_id,RevisionRecordId=rev_rec_id,ServiceId=TreeParam))
	# Duplicate records removed from assembly level entitlement in offering - End
	SAQSAE_ent_renewal = """INSERT SAQSAE (KB_VERSION,EQUIPMENT_ID,EQUIPMENT_RECORD_ID,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_RECORD_ID,QTEREV_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,CPS_CONFIGURATION_ID,CPS_MATCH_ID,GREENBOOK,GREENBOOK_RECORD_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,ASSEMBLY_DESCRIPTION,ASSEMBLY_ID,ASSEMBLY_RECORD_ID,QTESRVCOA_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,ENTITLEMENT_XML,CONFIGURATION_STATUS,QTESRVCOE_RECORD_ID,QUOTE_SERVICE_COV_OBJ_ASS_ENT_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED) SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_COV_OBJ_ASS_ENT_RECORD_ID, '{username}' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM(SELECT IQ.*,M.ENTITLEMENT_XML,M.CONFIGURATION_STATUS,M.QUOTE_SERVICE_COVERED_OBJ_ENTITLEMENTS_RECORD_ID as QTESRVCOE_RECORD_ID FROM ( SELECT DISTINCT SAQTSE.KB_VERSION,SAQSCA.EQUIPMENT_ID,SAQSCA.EQUIPMENT_RECORD_ID,SAQTSE.QUOTE_ID,SAQTSE.QUOTE_RECORD_ID,SAQTSE.QTEREV_RECORD_ID,SAQTSE.QTEREV_ID,SAQTSE.SERVICE_DESCRIPTION,SAQTSE.SERVICE_ID,SAQTSE.SERVICE_RECORD_ID,SAQTSE.CPS_CONFIGURATION_ID,SAQTSE.CPS_MATCH_ID,SAQSCA.GREENBOOK,SAQSCA.GREENBOOK_RECORD_ID,SAQSCA.FABLOCATION_ID,SAQSCA.FABLOCATION_NAME,SAQSCA.FABLOCATION_RECORD_ID,SAQSCA.ASSEMBLY_DESCRIPTION,SAQSCA.ASSEMBLY_ID,SAQSCA.ASSEMBLY_RECORD_ID,SAQSCA.QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID as QTESRVCOA_RECORD_ID,SAQTSE.SALESORG_ID,SAQTSE.SALESORG_NAME,SAQTSE.SALESORG_RECORD_ID FROM SAQTSE (NOLOCK) JOIN (SELECT * FROM SAQSCA (NOLOCK) WHERE SAQSCA.QUOTE_RECORD_ID = '{ContractId}' AND SAQSCA.QTEREV_RECORD_ID = '{revision_rec_id}' ) SAQSCA ON SAQTSE.QUOTE_RECORD_ID = SAQSCA.QUOTE_RECORD_ID AND SAQTSE.QTEREV_RECORD_ID = SAQSCA.QTEREV_RECORD_ID AND SAQTSE.SERVICE_RECORD_ID = SAQSCA.SERVICE_RECORD_ID WHERE SAQTSE.QUOTE_RECORD_ID = '{ContractId}' AND SAQTSE.QTEREV_RECORD_ID = '{revision_rec_id}' AND SAQTSE.SERVICE_ID = '{serviceId}') IQ JOIN SAQSCE (NOLOCK) M ON M.SERVICE_RECORD_ID = IQ.SERVICE_RECORD_ID AND M.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND M.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND M.EQUIPMENT_ID = IQ.EQUIPMENT_ID )IQ""".format(username = userName ,  ContractId=Qt_rec_id, serviceId=TreeParam, revision_rec_id = rev_rec_id)
	Sql.RunQuery(SAQSAE_ent_renewal)
	Log.Info('SAQSAE_ent_renewal--393--renewal-1881-----'+str(SAQSAE_ent_renewal))
	# get_cnt_SAQSAE = Sql.GetFirst("""SELECT count(*) as cnt 
	# 				FROM SAQTSE (NOLOCK) JOIN (SELECT * FROM SAQSCA (NOLOCK) WHERE SAQSCA.QUOTE_RECORD_ID = '{ContractId}' ) SAQSCA ON SAQTSE.QUOTE_RECORD_ID = SAQSCA.QUOTE_RECORD_ID AND SAQTSE.SERVICE_RECORD_ID = SAQSCA.SERVICE_RECORD_ID WHERE SAQTSE.QUOTE_RECORD_ID = '{ContractId}' AND SAQTSE.SERVICE_ID = '{serviceId}') IQ JOIN SAQSCE (NOLOCK) M ON M.SERVICE_RECORD_ID = IQ.SERVICE_RECORD_ID AND M.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND M.EQUIPMENT_ID = IQ.EQUIPMENT_ID """.format(UserId=User.Id,  ContractId=Qt_rec_id, serviceId=TreeParam))
	# Log.Info("get_cnt_SAQSAE---> "+ str(get_cnt_SAQSAE.cnt))

	# get_SAQSCA = Sql.GetFirst("""SELECT count(*) as cnt FROM SAQSCA (NOLOCK) WHERE SAQSCA.QUOTE_RECORD_ID = '{ContractId} AND QTEREV_RECORD_ID = '{revision_rec_id}'""".format(ContractId=Qt_rec_id,revision_rec_id = rev_rec_id))

	# get_SAQSCE = Sql.GetFirst("""SELECT count(*) as cnt FROM SAQSCE (NOLOCK) WHERE SAQSCE.QUOTE_RECORD_ID = '{ContractId}' AND QTEREV_RECORD_ID = '{revision_rec_id}'""".format(ContractId=Qt_rec_id,revision_rec_id = rev_rec_id))
	
	#Log.Info("get_SAQSCA--222-> "+ str(get_SAQSCA.cnt))
	#Log.Info("get_SAQSCE--222-> "+ str(get_SAQSCE.cnt))
	##ENTITLEMENT UPDATE RESTRICT THE ATTRIBUTE TO PDC AND MPS GREENBOOK A055S000P01-8873 Start
	
	level = "Offering Entitlement "
	where_condition = " WHERE QUOTE_RECORD_ID='{}' AND QTEREV_RECORD_ID='{}' AND SERVICE_ID = '{}' ".format(Qt_rec_id, rev_rec_id, TreeParam)
	try:
		Log.Info("PREDEFINED WAFER DRIVER IFLOW")
		#where_condition = " WHERE QUOTE_RECORD_ID='{}' AND QTEREV_RECORD_ID='{}' AND SERVICE_ID = '{}' ".format(Qt_rec_id, rev_rec_id, TreeParam)
		
		predefined = ScriptExecutor.ExecuteGlobal("CQVLDPRDEF",{"where_condition": where_condition,"quote_rec_id": Qt_rec_id ,"level":"EQUIPMENT_LEVEL", "treeparam": TreeParam,"user_id": userId, "quote_rev_id":rev_rec_id})

	except:
		Log.Info("EXCEPT----PREDEFINED DRIVER IFLOW")
	try:
		##saqgpe ent columns update
		for rec in ['SAQSCE','SAQGPE']:
			entitlemt_attr_update('SAQSCE',where_condition)
	except:
		Log.Info("EXCEPT----entitlement view update error IFLOW")
	#ancillary_service_Z0046()
	if not ancillary_dict:
		get_ancillary = Sql.GetList("SELECT * FROM SAQTSV WHERE QUOTE_RECORD_ID = '{Qt_rec_id}' AND QTEREV_RECORD_ID = '{rev_rec_id}' AND PAR_SERVICE_ID ='{service_id}' AND SERVICE_ID NOT IN (SELECT ADNPRD_ID FROM SAQSAO WHERE SERVICE_ID = '{service_id}' AND QUOTE_RECORD_ID = '{Qt_rec_id}' AND QTEREV_RECORD_ID = '{rev_rec_id}')".format(Qt_rec_id = Qt_rec_id,rev_rec_id = rev_rec_id,service_id = TreeParam ))
		if get_ancillary:
			for rec in get_ancillary:
				ancillary_dict[rec.SERVICE_ID] = 'INSERT'

	if ancillary_dict:
		Log.Info("inside ancillary1111"+str(ancillary_dict)+'--'+str(Qt_rec_id))
		where_condition = " WHERE QUOTE_RECORD_ID='{}' AND QTEREV_RECORD_ID='{}' AND SERVICE_ID = '{}' ".format(Qt_rec_id, rev_rec_id, TreeParam)
		for anc_key,anc_val in ancillary_dict.items():
			Log.Info("vall--"+str(anc_key)  )
			ancillary_object_qry = Sql.GetFirst("SELECT CpqTableEntryId FROM SAQTSV WHERE SERVICE_ID = '{anc_key}' AND QUOTE_RECORD_ID = '{Qt_rec_id}' AND QTEREV_RECORD_ID = '{rev_rec_id}' AND PAR_SERVICE_ID = '{service_id}' AND SERVICE_ID NOT IN (SELECT ADNPRD_ID FROM SAQSAO WHERE SERVICE_ID = '{service_id}' AND QUOTE_RECORD_ID = '{Qt_rec_id}' AND QTEREV_RECORD_ID = '{rev_rec_id}')".format(anc_key =anc_key,Qt_rec_id = Qt_rec_id,rev_rec_id = rev_rec_id,service_id = TreeParam ))
			
			if anc_val == "INSERT" :
				
				ActionType = "{}_SERVICE".format(anc_val)
				Log.Info("inside ancillary")
				ancillary_result = ScriptExecutor.ExecuteGlobal("CQENANCOPR",{"where_string": where_condition, "quote_record_id": Qt_rec_id, "revision_rec_id": rev_rec_id, "ActionType":ActionType, "ancillary_obj": anc_key, "service_id" : TreeParam , "tablename":"SAQTSE"})
	
	##ancillary entitlement insert
	try:
		ancillary_result = ScriptExecutor.ExecuteGlobal("CQENANCOPR",{"where_string": where_condition, "quote_record_id": Qt_rec_id, "revision_rec_id": rev_rec_id, "ActionType":"INSERT_ENT_EQUIPMENT",   "ancillary_obj": "", "service_id" : TreeParam , "tablename":"SAQTSE"})
	except:
		Log.Info("ancillary entitlement error")

	try:
		addon_object =Sql.GetList("SELECT SAQSAO.*, SAQSGB.GREENBOOK FROM SAQSAO (NOLOCK) INNER JOIN SAQSGB (NOLOCK) ON SAQSGB.QUOTE_RECORD_ID=SAQSAO.QUOTE_RECORD_ID and SAQSGB.QTEREV_RECORD_ID=SAQSAO.QTEREV_RECORD_ID and SAQSGB.SERVICE_ID = SAQSAO.ADNPRD_ID AND SAQSGB.PAR_SERVICE_ID = SAQSAO.SERVICE_ID WHERE SAQSAO.QUOTE_RECORD_ID= '{QuoteRecordId}' AND SAQSAO.QTEREV_RECORD_ID = '{RevisionRecordId}' AND SAQSAO.ACTIVE ='TRUE' AND SAQSAO.SERVICE_ID = '{service_id}' ".format(QuoteRecordId=Qt_rec_id,RevisionRecordId=rev_rec_id, service_id = TreeParam))
		for OfferingRow_detail in addon_object:
			CQADDONPRD.addon_operations(OfferingRow_detail,OfferingRow_detail.GREENBOOK)
	except:
		Log.Info("error in add on product")
	 
	# try:
	# 	Log.Info("Called CQINSQTITM ==>cqroll "+str(Qt_rec_id))
	# 	# data = ScriptExecutor.ExecuteGlobal("CQINSQTITM",{"ContractQuoteRecordId":Qt_rec_id, "ContractQuoteRevisionRecordId":rev_rec_id, "ServiceId":TreeParam, "ActionType":'INSERT_LINE_ITEMS'})
	# 	#Log.Info("Called CQINSQTITM ==>cqroll enddddd "+str(Qt_rec_id))
	# except Exception:
	# 	Log.Info("Exception in Quote Item insert") 
	
	# if ancillary_dict:
	# 	Log.Info("ancillary_dict--qi-"+str(ancillary_dict)+'--'+str(Qt_rec_id)) 
	# 	for anc_key,anc_val in ancillary_dict.items():
	# 		#if anc_val == 'INSERT':
	# 		try:
	# 			#temp_val = "SERVICE_ID = '{}'".format(anc_key)
	# 			#where = re.sub(r'SERVICE_ID\s*\=\s*\'[^>]*?\'', temp_val, where )
	# 			#where = where.replace('Z0091','{}'.format(anc_key))
	# 			#Log.Info('where--CQINSQTITM-'+str(where)+str(anc_key))
	# 			data = ScriptExecutor.ExecuteGlobal("CQINSQTITM",{"ContractQuoteRecordId":Qt_rec_id, "ContractQuoteRevisionRecordId":rev_rec_id, "ServiceId":anc_key, "ActionType":'INSERT_LINE_ITEMS'})
	# 			#data = ScriptExecutor.ExecuteGlobal("CQINSQTITM",{"WhereString":where, "ActionType":'UPDATE_LINE_ITEMS'})
	# 		except Exception:
	# 			Log.Info("Exception in Quote Item insert1111")
	sendEmail(level)

def CoveredObjItemEntitlement():
	
	SAQIEN_query = """
				INSERT SAQIEN 
				(KB_VERSION,ENTITLEMENT_XML,EQUIPMENT_ID,EQUIPMENT_RECORD_ID,QUOTE_ID,QTEITMCOB_RECORD_ID,QTEITM_RECORD_ID,	
				QUOTE_RECORD_ID,QTESRVENT_RECORD_ID,SERIAL_NO,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,CPS_CONFIGURATION_ID,EQUIPMENT_LINE_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID, QUOTE_ITEM_COVERED_OBJECT_ENTITLEMENTS_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED)
				SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_COVERED_OBJECT_ENTITLEMENTS_RECORD_ID, {UserId} as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM (
					SELECT 
						DISTINCT
						SAQTSE.KB_VERSION,SAQTSE.ENTITLEMENT_XML,SAQICO.EQUIPMENT_ID,SAQICO.EQUIPMENT_RECORD_ID,SAQTSE.QUOTE_ID,SAQICO.QUOTE_ITEM_COVERED_OBJECT_RECORD_ID as QTEITMCOB_RECORD_ID,SAQICO.QTEITM_RECORD_ID,SAQTSE.QUOTE_RECORD_ID,SAQTSE.QUOTE_SERVICE_ENTITLEMENT_RECORD_ID as QTESRVENT_RECORD_ID,SAQICO.SERIAL_NO,SAQTSE.SERVICE_DESCRIPTION,SAQTSE.SERVICE_ID,SAQTSE.SERVICE_RECORD_ID,SAQTSE.SALESORG_ID,SAQTSE.SALESORG_NAME,SAQTSE.SALESORG_RECORD_ID,SAQTSE.CPS_CONFIGURATION_ID,SAQICO.EQUIPMENT_LINE_ID,SAQICO.FABLOCATION_ID,SAQICO.FABLOCATION_NAME,SAQICO.FABLOCATION_RECORD_ID
					FROM	
					SAQTSE (NOLOCK)
					JOIN SAQICO (NOLOCK) ON SAQICO.SERVICE_RECORD_ID = SAQTSE.SERVICE_RECORD_ID AND SAQICO.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID
					WHERE SAQTSE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQTSE.SERVICE_ID = '{ServiceId}') IQ
				""".format(UserId=User.Id, QuoteRecordId=Qt_rec_id, ServiceId=TreeParam)
	Log.Info("SAQIEN_query--235-----"+str(SAQIEN_query))
	Sql.RunQuery(SAQIEN_query)
	#insert to SAQSPT
	SAQSPEaddon_query = """
				INSERT SAQSPE
				(KB_VERSION,ENTITLEMENT_XML,QUOTE_ID,
				QUOTE_RECORD_ID,QTESRVENT_RECORD_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,CPS_CONFIGURATION_ID,QTESRVPRT_RECORD_ID,PART_RECORD_ID,PART_DESCRIPTION,PART_NUMBER,QUOTE_SERVICE_PART_ENTITLEMENT_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED)
				SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_PART_ENTITLEMENT_RECORD_ID, {UserId} as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM (
					SELECT 
						DISTINCT
						SAQTSE.KB_VERSION,SAQTSE.ENTITLEMENT_XML,SAQTSE.QUOTE_ID,SAQTSE.QUOTE_RECORD_ID,SAQTSE.QUOTE_SERVICE_ENTITLEMENT_RECORD_ID as QTESRVENT_RECORD_ID,SAQTSE.SERVICE_DESCRIPTION,SAQTSE.SERVICE_ID,SAQTSE.SERVICE_RECORD_ID,SAQTSE.SALESORG_ID,SAQTSE.SALESORG_NAME,SAQTSE.SALESORG_RECORD_ID,SAQTSE.CPS_CONFIGURATION_ID,SAQSPT.QUOTE_SERVICE_PART_RECORD_ID as QTESRVPRT_RECORD_ID,SAQSPT.PART_RECORD_ID,SAQSPT.PART_DESCRIPTION,SAQSPT.PART_NUMBER
					FROM	
					SAQTSE (NOLOCK)
					JOIN SAQSPT (NOLOCK) ON SAQSPT.SERVICE_RECORD_ID = SAQTSE.SERVICE_RECORD_ID AND SAQSPT.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID
					WHERE SAQTSE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQTSE.SERVICE_ID = '{ServiceId}') IQ
				""".format(UserId=User.Id, QuoteRecordId=Qt_rec_id, ServiceId=TreeParam)
	Log.Info("SAQSPEaddon_query--251---------"+str(SAQSPEaddon_query))
	Sql.RunQuery(SAQSPEaddon_query)
	#insert to SAQSPT
	# SAQIPE_query = """
	# 			INSERT SAQIPE
	# 			(ENTITLEMENT_XML,QUOTE_ID,
	# 			QUOTE_RECORD_ID,LINE_ITEM_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,CPS_CONFIGURATION_ID,QTESRVPRT_RECORD_ID,PART_RECORD_ID,PART_DESCRIPTION,PART_NUMBER,QTEITMFPT_RECORD_ID,QTEITM_RECORD_ID,QUOTE_ITEM_FORECAST_PART_ENT_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED)
	# 			SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_FORECAST_PART_ENT_RECORD_ID, {UserId} as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM (
	# 				SELECT 
	# 					DISTINCT
	# 					SAQSPE.ENTITLEMENT_XML,SAQSPE.QUOTE_ID,SAQSPE.QUOTE_RECORD_ID,SAQITM.LINE_ITEM_ID,SAQSPE.SERVICE_DESCRIPTION,SAQSPE.SERVICE_ID,SAQSPE.SERVICE_RECORD_ID,SAQSPE.SALESORG_ID,SAQSPE.SALESORG_NAME,SAQSPE.SALESORG_RECORD_ID,SAQSPE.CPS_CONFIGURATION_ID,SAQSPE.QUOTE_SERVICE_PART_ENTITLEMENT_RECORD_ID as QTESRVPRT_RECORD_ID,SAQSPE.PART_RECORD_ID,SAQSPE.PART_DESCRIPTION,SAQSPE.PART_NUMBER,'' as QTEITMFPT_RECORD_ID,SAQITM.QUOTE_ITEM_RECORD_ID as QTEITM_RECORD_ID
	# 				FROM	
	# 				SAQSPE (NOLOCK)
	# 				JOIN SAQITM (NOLOCK) ON SAQSPE.SERVICE_RECORD_ID = SAQITM.SERVICE_RECORD_ID AND SAQSPE.QUOTE_RECORD_ID = SAQITM.QUOTE_RECORD_ID
	# 				WHERE SAQSPE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSPE.SERVICE_ID = '{ServiceId}') IQ
	# 			""".format(UserId=User.Id, QuoteRecordId=Qt_rec_id, ServiceId=TreeParam)
	# #Log.Info("SAQIPE_query---231-----"+str(SAQIPE_query))
	# Sql.RunQuery(SAQIPE_query)
	SAQSAE_query = SqlHelper.GetFirst("sp_executesql @T=N'INSERT SAQSAE (KB_VERSION,EQUIPMENT_ID,EQUIPMENT_RECORD_ID,QUOTE_ID,QUOTE_RECORD_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,CPS_CONFIGURATION_ID,CPS_MATCH_ID,GREENBOOK,GREENBOOK_RECORD_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,ASSEMBLY_DESCRIPTION,ASSEMBLY_ID,ASSEMBLY_RECORD_ID,QTESRVCOA_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,ENTITLEMENT_XML,QTESRVCOE_RECORD_ID,QUOTE_SERVICE_COV_OBJ_ASS_ENT_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED) SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_COV_OBJ_ASS_ENT_RECORD_ID, ''"+str(User.Id)+"'' as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM(SELECT IQ.*,M.ENTITLEMENT_XML,M.QUOTE_SERVICE_COVERED_OBJ_ENTITLEMENTS_RECORD_ID as QTESRVCOE_RECORD_ID FROM ( SELECT DISTINCT SAQTSE.KB_VERSION,SAQSCA.EQUIPMENT_ID,SAQSCA.EQUIPMENT_RECORD_ID,SAQTSE.QUOTE_ID,SAQTSE.QUOTE_RECORD_ID,SAQTSE.SERVICE_DESCRIPTION,SAQTSE.SERVICE_ID,SAQTSE.SERVICE_RECORD_ID,SAQTSE.CPS_CONFIGURATION_ID,SAQTSE.CPS_MATCH_ID,SAQSCA.GREENBOOK,SAQSCA.GREENBOOK_RECORD_ID,SAQSCA.FABLOCATION_ID,SAQSCA.FABLOCATION_NAME,SAQSCA.FABLOCATION_RECORD_ID,SAQSCA.ASSEMBLY_DESCRIPTION,SAQSCA.ASSEMBLY_ID,SAQSCA.ASSEMBLY_RECORD_ID,SAQSCA.QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID as QTESRVCOA_RECORD_ID,SAQTSE.SALESORG_ID,SAQTSE.SALESORG_NAME,SAQTSE.SALESORG_RECORD_ID FROM SAQTSE (NOLOCK) JOIN (SELECT * FROM SAQSCA (NOLOCK) WHERE SAQSCA.QUOTE_RECORD_ID = ''"+str(Qt_rec_id)+"'' ) SAQSCA ON SAQTSE.QUOTE_RECORD_ID = SAQSCA.QUOTE_RECORD_ID AND SAQTSE.SERVICE_RECORD_ID = SAQSCA.SERVICE_RECORD_ID WHERE SAQTSE.QUOTE_RECORD_ID = ''"+str(Qt_rec_id)+"'' AND SAQTSE.SERVICE_ID = ''"+str(TreeParam)+"'') IQ JOIN SAQSCE (NOLOCK) M ON M.SERVICE_RECORD_ID = IQ.SERVICE_RECORD_ID AND M.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND M.EQUIPMENT_ID = IQ.EQUIPMENT_ID )IQ '")

def sendEmail(level):
	Log.Info('284-----entitlement email started-----')
	#userid=User.Id
	getQuoteId = SqlHelper.GetFirst("SELECT QUOTE_ID FROM SAQTMT WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{}'".format(Qt_rec_id))
	getEmail = SqlHelper.GetFirst("SELECT email from users where id={}".format(userId))
	#Log.Info("SELECT email from users where id='{}'".format(userid))
	userEmail = ""
	userEmail = str(getEmail.email)
	Header = "<!DOCTYPE html><html><head><style>h4{font-weight:normal; font-family:sans-serif;} table {font-family: Calibri, sans-serif; border-collapse: collapse; width: 75%}td, th {  border: 1px solid #dddddd;  text-align: left; padding: 8px;}.im {color: #222;}tr:nth-child(even) {background-color: #dddddd;} #grey{background: rgb(245,245,245);} #bd{color : 'black';}</style> </head> <body><h4>Hi, <br> <br>The Entitlement settings have been applied to the equipment in the following quote:</br></h4>"

	Table_start ="<table class='table table-bordered'><tr><th id = 'grey'>Quote ID</th><th id = 'grey'>Rolldown Level</th><th id = 'grey'>Rolldown Status</th></tr><tr><td >"+str(getQuoteId.QUOTE_ID)+"</td><td>"+str(level)+"</td><td>Completed</td></tr></table> <br> <br>Note: Please do not reply to this email.</body></html>"

	Error_Info = Header + Table_start

	LOGIN_CRE = SqlHelper.GetFirst("SELECT User_name,Password FROM SYCONF where Domain ='SUPPORT_MAIL'")

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
	#copyEmail2 = MailAddress("dhurga.gopalakrishnan@bostonharborconsulting.com")
	#copyEmail3 = MailAddress("namrata.sivakumar@bostonharborconsulting.com")
	copyEmail4 = MailAddress("ranjani.parkavi@bostonharborconsulting.com")
	copyEmail5 = MailAddress("ashish.gandotra@bostonharborconsulting.com")
	# copyEmail6 = MailAddress("aditya.shivkumar@bostonharborconsulting.com")
	msg.Bcc.Add(copyEmail1)
	#msg.Bcc.Add(copyEmail2)
	#msg.Bcc.Add(copyEmail3)
	msg.Bcc.Add(copyEmail4)
	msg.Bcc.Add(copyEmail5)
	# msg.Bcc.Add(copyEmail6)
	# CC Emails
	# Send the message
	mailClient.Send(msg)

	return True

def covobjrenewal():
	#Log.Info('303-----')
	configuration = []
	attributeList=[]
	insertservice = ""
	attributevalueList=[]
	attributesdisallowedlst = []
	attributesallowedlst = []
	attributevalues={}
	for ProductPartnumber in ProductPart:
		Fullresponse = cloneEntitlement(ProductPartnumber)
		attrKey = []
		attrValue = []
		#attributevalues={}
		for rootattribute, rootvalue in Fullresponse.items():
			if rootattribute == "rootItem":
				for Productattribute, Productvalue in rootvalue.items():
					if Productattribute == "characteristics":
						for attribute in Productvalue:
							if attribute['visible'] =='false':
								attributesdisallowedlst.append(attribute['id'])
							else:
								attributesallowedlst.append(attribute['id'])				
							attrKey.append(attribute["id"])                            
							for attrval in attribute["values"]:						
								attrValue.append(attrval['value'])
		attributesallowedlst = list(set(attributesallowedlst))

		attributeList.append(attrKey)
		attributevalueList.append(attrValue)
		configurationId = Fullresponse["id"]        
		configuration.append(configurationId)
		HasDefaultvalue=False
		ProductVersionObj=Sql.GetFirst("Select product_id from product_versions(nolock) where SAPKBVersion='"+str(Fullresponse['kbKey']['version'])+"'")
		if ProductVersionObj is not None:
			tbrow={}
			insertservice = ""
			tblist = []  
			for attrs in attributesallowedlst:
				#tbrow1 = {}
				if attrs in attributevalues:
					HasDefaultvalue=True
					STANDARD_ATTRIBUTE_VALUES=Sql.GetFirst("SELECT S.STANDARD_ATTRIBUTE_DISPLAY_VAL,S.STANDARD_ATTRIBUTE_CODE FROM STANDARD_ATTRIBUTE_VALUES (nolock) S INNER JOIN ATTRIBUTE_DEFN (NOLOCK) A ON A.STANDARD_ATTRIBUTE_CODE=S.STANDARD_ATTRIBUTE_CODE WHERE A.SYSTEM_ID = '{}' AND S.STANDARD_ATTRIBUTE_VALUE='{}'".format(attrs,attributevalues[attrs]))
				else:
					HasDefaultvalue=False
					STANDARD_ATTRIBUTE_VALUES=Sql.GetFirst("SELECT S.STANDARD_ATTRIBUTE_CODE FROM STANDARD_ATTRIBUTE_VALUES (nolock) S INNER JOIN ATTRIBUTE_DEFN (NOLOCK) A ON A.STANDARD_ATTRIBUTE_CODE=S.STANDARD_ATTRIBUTE_CODE WHERE A.SYSTEM_ID = '{}'".format(attrs))
				ATTRIBUTE_DEFN=Sql.GetFirst("SELECT * FROM ATTRIBUTE_DEFN (NOLOCK) WHERE SYSTEM_ID='{}'".format(attrs))
				PRODUCT_ATTRIBUTES=Sql.GetFirst("SELECT A.ATT_DISPLAY_DESC,P.ATTRDESC FROM ATT_DISPLAY_DEFN (NOLOCK) A INNER JOIN PRODUCT_ATTRIBUTES (NOLOCK) P ON A.ATT_DISPLAY=P.ATT_DISPLAY WHERE P.PRODUCT_ID={} AND P.STANDARD_ATTRIBUTE_CODE={}".format(ProductVersionObj.product_id,STANDARD_ATTRIBUTE_VALUES.STANDARD_ATTRIBUTE_CODE))
				DTypeset={"Drop Down":"DropDown","Free Input, no Matching":"FreeInputNoMatching","Check Box":"CheckBox"}
				if PRODUCT_ATTRIBUTES:
					get_tooltip_desc = PRODUCT_ATTRIBUTES.ATTRDESC
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
				</QUOTE_ITEM_ENTITLEMENT>""".format(ent_name = str(attrs),ent_val_code = attributevalues[attrs] if HasDefaultvalue==True else '',ent_type = DTypeset[PRODUCT_ATTRIBUTES.ATT_DISPLAY_DESC] if PRODUCT_ATTRIBUTES else  '',ent_desc = ATTRIBUTE_DEFN.STANDARD_ATTRIBUTE_NAME,ent_disp_val = STANDARD_ATTRIBUTE_VALUES.STANDARD_ATTRIBUTE_DISPLAY_VAL if HasDefaultvalue==True else '',ct = '',pi = '',is_default = '1',pm = '',cf = '',tool_desc =get_tooltip_desc.replace("'","''") if "'" in get_tooltip_desc else get_tooltip_desc)
			SAQSFE_query="""
				INSERT SAQSFE (ENTITLEMENT_XML,QUOTE_ID,QUOTE_NAME,QUOTE_RECORD_ID,QTEREV_RECORD_ID,QTEREV_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,	
				CPS_CONFIGURATION_ID, CPS_MATCH_ID,QTESRVENT_RECORD_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,QTESRVFBL_RECORD_ID,QUOTE_SERVICE_FAB_LOC_ENT_RECORD_ID,CPQTABLEENTRYDATEADDED, CPQTABLEENTRYADDEDBY)
				SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_FAB_LOC_ENT_RECORD_ID, {UserId} as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM (
				SELECT 
					DISTINCT	
					'{en_xml}' as ENTITLEMENT_XML,SAQTSE.QUOTE_ID,SAQTSE.QUOTE_NAME,SAQTSE.QUOTE_RECORD_ID,SAQTSE.QTEREV_ID,SAQTSE.QTEREV_RECORD_ID,SAQTSE.SERVICE_DESCRIPTION,SAQTSE.SERVICE_ID,SAQTSE.SERVICE_RECORD_ID,SAQTSE.SALESORG_ID,SAQTSE.SALESORG_NAME,SAQTSE.SALESORG_RECORD_ID,SAQTSE.CPS_CONFIGURATION_ID, SAQTSE.CPS_MATCH_ID,SAQTSE.QUOTE_SERVICE_ENTITLEMENT_RECORD_ID as QTESRVENT_RECORD_ID,SAQSFB.FABLOCATION_ID, SAQSFB.FABLOCATION_NAME, SAQSFB.FABLOCATION_RECORD_ID, SAQSFB.QUOTE_SERVICE_FAB_LOCATION_RECORD_ID as QTESRVFBL_RECORD_ID
				FROM
				SAQTSE (NOLOCK)
				JOIN SAQSFB ON SAQSFB.SERVICE_RECORD_ID = SAQTSE.SERVICE_RECORD_ID AND SAQSFB.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID
				WHERE SAQTSE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQTSE.QTEREV_RECORD_ID = '{revision_rec_id}' AND SAQTSE.SERVICE_ID = '{ServiceId}') IQ""".format(UserId=User.Id, QuoteRecordId=ContractRecordId, ServiceId=ProductPartnumber,en_xml = insertservice, revision_rec_id = rev_rec_id)
			Log.Info('SAQSFE_query--41-'+str(SAQSFE_query))
			Sql.RunQuery(SAQSFE_query)
			#ENTITLEMENT SV TO GB
			
			qtqtse_query="""
				INSERT SAQSGE (KB_VERSION,QUOTE_ID,QUOTE_NAME,QUOTE_RECORD_ID,QTEREV_RECORD_ID,QTEREV_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,	
				CPS_CONFIGURATION_ID, CPS_MATCH_ID,GREENBOOK,GREENBOOK_RECORD_ID,QTESRVENT_RECORD_ID,QTSFBLENT_RECORD_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,ENTITLEMENT_XML, QUOTE_SERVICE_GREENBOOK_ENTITLEMENT_RECORD_ID,CPQTABLEENTRYDATEADDED, CPQTABLEENTRYADDEDBY)
				SELECT OQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_GREENBOOK_ENTITLEMENT_RECORD_ID, {UserId} as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM (SELECT IQ.*,M.ENTITLEMENT_XML FROM(
				SELECT 
					DISTINCT	
					SAQTSE.KB_VERSION,SAQTSE.QUOTE_ID,SAQTSE.QUOTE_NAME,SAQTSE.QUOTE_RECORD_ID,SAQTSE.QTEREV_RECORD_ID,SAQTSE.QTEREV_ID,SAQTSE.SERVICE_DESCRIPTION,SAQTSE.SERVICE_ID,SAQTSE.SERVICE_RECORD_ID,SAQTSE.SALESORG_ID,SAQTSE.SALESORG_NAME,SAQTSE.SALESORG_RECORD_ID,SAQTSE.CPS_CONFIGURATION_ID, SAQTSE.CPS_MATCH_ID,SAQSCO.GREENBOOK,SAQSCO.GREENBOOK_RECORD_ID,SAQTSE.QUOTE_SERVICE_ENTITLEMENT_RECORD_ID as QTESRVENT_RECORD_ID,SAQSFE.QUOTE_SERVICE_FAB_LOC_ENT_RECORD_ID as QTSFBLENT_RECORD_ID,SAQSFE.FABLOCATION_ID,SAQSFE.FABLOCATION_NAME,SAQSFE.FABLOCATION_RECORD_ID
				FROM
				SAQTSE (NOLOCK)
				JOIN SAQSCO  (NOLOCK) ON SAQSCO.SERVICE_RECORD_ID = SAQTSE.SERVICE_RECORD_ID AND SAQSCO.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID AND SAQSCO.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID JOIN SAQSFE ON SAQSFE.SERVICE_RECORD_ID = SAQTSE.SERVICE_RECORD_ID AND SAQSFE.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID  AND SAQSFE.QTEREV_RECORD_ID = SAQTSE.QTEREV_RECORD_ID 
				WHERE SAQTSE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQTSE.QTEREV_RECORD_ID = '{revision_rec_id}' AND SAQTSE.SERVICE_ID = '{ServiceId}') IQ JOIN SAQSFE (NOLOCK) M ON IQ.QTSFBLENT_RECORD_ID = QUOTE_SERVICE_FAB_LOC_ENT_RECORD_ID )OQ""".format(UserId=User.Id, QuoteRecordId=ContractRecordId, ServiceId=ProductPartnumber,en_xml = insertservice, revision_rec_id = rev_rec_id)
			Log.Info("qtqtse_query------"+str(qtqtse_query))
			Sql.RunQuery(qtqtse_query)
			qtqsce="""INSERT SAQSCE
			(ENTITLEMENT_XML,EQUIPMENT_ID,EQUIPMENT_RECORD_ID,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_RECORD_ID,QTEREV_ID,QTESRVCOB_RECORD_ID,QTESRVENT_RECORD_ID,SERIAL_NO,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,CPS_CONFIGURATION_ID,CPS_MATCH_ID,SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID, KB_VERSION, GREENBOOK,GREENBOOK_RECORD_ID, QUOTE_SERVICE_COVERED_OBJ_ENTITLEMENTS_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED) 
			SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_COVERED_OBJ_ENTITLEMENTS_RECORD_ID, {UserId} as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM (
				SELECT 
					
						'{en_xml}' as ENTITLEMENT_XML,CTCSCE.EQUIPMENT_ID,CTCSCE.EQUIPMENT_RECORD_ID,SAQSCO.QUOTE_ID,SAQSCO.QUOTE_RECORD_ID,SAQSCO.QTEREV_RECORD_ID,SAQSCO.QTEREV_ID,,SAQSCO.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,SAQTSE.QUOTE_SERVICE_ENTITLEMENT_RECORD_ID,CTCSCE.SERIAL_NO,CTCSCE.SERVICE_DESCRIPTION,CTCSCE.SERVICE_ID,CTCSCE.SERVICE_RECORD_ID,'{configurationId}' as CPS_CONFIGURATION_ID,'{cpsmatchId}' as  CPS_MATCH_ID,CTCTSO.SALESORG_ID, CTCTSO.SALESORG_NAME, CTCTSO.SALESORG_RECORD_ID, SAQTSE.KB_VERSION,SAQSCO.GREENBOOK,SAQSCO.GREENBOOK_RECORD_ID
				FROM	
				CTCSCE (NOLOCK) 
				JOIN SAQSCO (NOLOCK) ON (CTCSCE.SERVICE_ID= SAQSCO.SERVICE_ID AND SAQSCO.EQUIPMENT_ID = CTCSCE.EQUIPMENT_ID) JOIN SAQTSE (NOLOCK) ON (SAQSCO.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID AND SAQSCO.QTEREV_RECORD_ID = SAQTSE.QTEREV_RECORD_ID  AND CTCSCE.SERVICE_ID= SAQTSE.SERVICE_ID) JOIN CTCTSO (NOLOCK) ON CTCTSO.CONTRACT_ID = CTCSCE.CONTRACT_ID						
				WHERE CTCSCE.CONTRACT_ID = '{ContractId}' AND CTCSCE.SERVICE_ID = '{serviceId}' AND SAQSCO.QUOTE_RECORD_ID = '{ContractRecordId}' AND SAQSCO.QTEREV_RECORD_ID = '{revision_rec_id}'
			) IQ""".format(UserId=User.Id, configurationId=configurationId, cpsmatchId = '1', ContractId=Qt_rec_id, serviceId=ProductPartnumber,ContractRecordId=ContractRecordId,en_xml = insertservice, revision_rec_id = rev_rec_id)
			#Log.Info("--378----qtqsce--renewal-"+str(qtqsce))
			Sql.RunQuery(qtqsce)
			#Log.Info('insertservice----'+str(insertservice))
			# Duplicate records removed from assembly level entitlement in offering - Start
			Sql.RunQuery("""DELETE FROM SAQSAE WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID = '{ServiceId}'""".format(QuoteRecordId=ContractRecordId,RevisionRecordId=rev_rec_id,ServiceId=ProductPartnumber))
			# Duplicate records removed from assembly level entitlement in offering - Start
			SAQSAE_ent_renewal = """INSERT SAQSAE (KB_VERSION,EQUIPMENT_ID,EQUIPMENT_RECORD_ID,QUOTE_ID,QUOTE_RECORD_ID,QTEREV_RECORD_ID,QTEREV_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,CPS_CONFIGURATION_ID,CPS_MATCH_ID,GREENBOOK,GREENBOOK_RECORD_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID,ASSEMBLY_DESCRIPTION,ASSEMBLY_ID,ASSEMBLY_RECORD_ID,QTESRVCOA_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,ENTITLEMENT_XML,QTESRVCOE_RECORD_ID,QUOTE_SERVICE_COV_OBJ_ASS_ENT_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED) SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_COV_OBJ_ASS_ENT_RECORD_ID, {UserId} as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM(SELECT IQ.*,M.ENTITLEMENT_XML,M.QUOTE_SERVICE_COVERED_OBJ_ENTITLEMENTS_RECORD_ID as QTESRVCOE_RECORD_ID FROM ( SELECT DISTINCT SAQTSE.KB_VERSION,SAQSCA.EQUIPMENT_ID,SAQSCA.EQUIPMENT_RECORD_ID,SAQTSE.QUOTE_ID,SAQTSE.QUOTE_RECORD_ID,SAQTSE.QTEREV_RECORD_ID,SAQTSE.QTEREV_ID,SAQTSE.SERVICE_DESCRIPTION,SAQTSE.SERVICE_ID,SAQTSE.SERVICE_RECORD_ID,SAQTSE.CPS_CONFIGURATION_ID,SAQTSE.CPS_MATCH_ID,SAQSCA.GREENBOOK,SAQSCA.GREENBOOK_RECORD_ID,SAQSCA.FABLOCATION_ID,SAQSCA.FABLOCATION_NAME,SAQSCA.FABLOCATION_RECORD_ID,SAQSCA.ASSEMBLY_DESCRIPTION,SAQSCA.ASSEMBLY_ID,SAQSCA.ASSEMBLY_RECORD_ID,SAQSCA.QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID as QTESRVCOA_RECORD_ID,SAQTSE.SALESORG_ID,SAQTSE.SALESORG_NAME,SAQTSE.SALESORG_RECORD_ID FROM SAQTSE (NOLOCK) JOIN (SELECT * FROM SAQSCA (NOLOCK) WHERE SAQSCA.QUOTE_RECORD_ID = '{ContractId}' AND SAQSCA.QTEREV_RECORD_ID = '{revision_rec_id}') SAQSCA ON SAQTSE.QUOTE_RECORD_ID = SAQSCA.QUOTE_RECORD_ID AND SAQTSE.QTEREV_RECORD_ID = SAQSCA.QTEREV_RECORD_ID AND SAQTSE.SERVICE_RECORD_ID = SAQSCA.SERVICE_RECORD_ID WHERE SAQTSE.QUOTE_RECORD_ID = '{ContractId}' AND SAQTSE.QTEREV_RECORD_ID = '{revision_rec_id}' AND SAQTSE.SERVICE_ID = '{serviceId}') IQ JOIN SAQSCE (NOLOCK) M ON M.SERVICE_RECORD_ID = IQ.SERVICE_RECORD_ID AND M.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND M.QTEREV_RECORD_ID = IQ.QTEREV_RECORD_ID AND M.EQUIPMENT_ID = IQ.EQUIPMENT_ID )IQ""".format(UserId=User.Id,  ContractId=ContractRecordId, serviceId=ProductPartnumber, revision_rec_id = rev_rec_id)
			Log.Info('SAQSAE_ent_renewal--393--renewal----'+str(SAQSAE_ent_renewal))
			Sql.RunQuery(SAQSAE_ent_renewal)
			SAQIEN_query = """
				INSERT SAQIEN 
				(KB_VERSION,ENTITLEMENT_XML,EQUIPMENT_ID,EQUIPMENT_RECORD_ID,QUOTE_ID,QTEITMCOB_RECORD_ID,QTEITM_RECORD_ID,
				QUOTE_RECORD_ID,QTEREV_RECORD_ID,QTEREV_ID,QTESRVENT_RECORD_ID,SERIAL_NO,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,CPS_CONFIGURATION_ID,EQUIPMENT_LINE_ID,FABLOCATION_ID,FABLOCATION_NAME,FABLOCATION_RECORD_ID, QUOTE_ITEM_COVERED_OBJECT_ENTITLEMENTS_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED)
				SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_COVERED_OBJECT_ENTITLEMENTS_RECORD_ID, {UserId} as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM (
					SELECT 
						DISTINCT
						SAQTSE.KB_VERSION,SAQTSE.ENTITLEMENT_XML,SAQICO.EQUIPMENT_ID,SAQICO.EQUIPMENT_RECORD_ID,SAQTSE.QUOTE_ID,SAQICO.QUOTE_ITEM_COVERED_OBJECT_RECORD_ID as QTEITMCOB_RECORD_ID,SAQICO.QTEITM_RECORD_ID,SAQTSE.QUOTE_RECORD_ID,SAQTSE.QTEREV_RECORD_ID,SAQTSE.QTEREV_ID,SAQTSE.QUOTE_SERVICE_ENTITLEMENT_RECORD_ID as QTESRVENT_RECORD_ID,SAQICO.SERIAL_NO,SAQTSE.SERVICE_DESCRIPTION,SAQTSE.SERVICE_ID,SAQTSE.SERVICE_RECORD_ID,SAQTSE.SALESORG_ID,SAQTSE.SALESORG_NAME,SAQTSE.SALESORG_RECORD_ID,SAQTSE.CPS_CONFIGURATION_ID,SAQICO.EQUIPMENT_LINE_ID,SAQICO.FABLOCATION_ID,SAQICO.FABLOCATION_NAME,SAQICO.FABLOCATION_RECORD_ID
					FROM	
					SAQTSE (NOLOCK)
					JOIN SAQICO (NOLOCK) ON SAQICO.SERVICE_RECORD_ID = SAQTSE.SERVICE_RECORD_ID AND SAQICO.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID AND SAQICO.QTEREV_RECORD_ID = SAQTSE.QTEREV_RECORD_ID
					WHERE SAQTSE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQTSE.QTEREV_RECORD_ID = '{revision_rec_id}' AND SAQTSE.SERVICE_ID = '{ServiceId}') IQ
				""".format(UserId=User.Id, QuoteRecordId=ContractRecordId, ServiceId=ProductPartnumber, revision_rec_id = rev_rec_id)
			Log.Info("SAQIEN_query--445---"+str(SAQIEN_query))
			Sql.RunQuery(SAQIEN_query)			
	for configurationId,ProductPartnumber in zip(configuration,ProductPart):
		qtqtse_query="""
		INSERT SAQSGE (KB_VERSION,ENTITLEMENT_XML,QUOTE_ID,QUOTE_NAME,QUOTE_RECORD_ID,QTEREV_RECORD_ID,QTEREV_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,	
		CPS_CONFIGURATION_ID, CPS_MATCH_ID,GREENBOOK,GREENBOOK_RECORD_ID,QTESRVENT_RECORD_ID,DATA_TYPE,FACTOR_CURRENCY,FACTOR_CURRENCY_RECORD_ID,QUOTE_SERVICE_GREENBOOK_ENTITLEMENT_RECORD_ID,CPQTABLEENTRYDATEADDED, CPQTABLEENTRYADDEDBY)
		SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_GREENBOOK_ENTITLEMENT_RECORD_ID, {UserId} as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM (
		SELECT 
			DISTINCT	
			SAQTSE.KB_VERSION,SAQTSE.ENTITLEMENT_XML,SAQTSE.QUOTE_ID,SAQTSE.QUOTE_NAME,SAQTSE.QUOTE_RECORD_ID,SAQTSE.QTEREV_RECORD_ID,SAQTSE.QTEREV_ID,SAQTSE.SERVICE_DESCRIPTION,SAQTSE.SERVICE_ID,SAQTSE.SERVICE_RECORD_ID,SAQTSE.SALESORG_ID,SAQTSE.SALESORG_NAME,SAQTSE.SALESORG_RECORD_ID,SAQTSE.CPS_CONFIGURATION_ID, SAQTSE.CPS_MATCH_ID,SAQSCO.GREENBOOK,SAQSCO.GREENBOOK_RECORD_ID,SAQTSE.QUOTE_SERVICE_ENTITLEMENT_RECORD_ID as QTESRVENT_RECORD_ID,SAQTSE.DATA_TYPE,SAQTSE.FACTOR_CURRENCY,SAQTSE.FACTOR_CURRENCY_RECORD_ID
		FROM
		SAQTSE (NOLOCK)
		JOIN SAQSCO (NOLOCK) ON SAQSCO.SERVICE_RECORD_ID = SAQTSE.SERVICE_RECORD_ID AND SAQSCO.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID
		WHERE SAQTSE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSCO.QTEREV_RECORD_ID = SAQTSE.QTEREV_RECORD_ID
		WHERE SAQTSE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQTSE.QTEREV_RECORD_ID = '{revision_rec_id}' AND SAQTSE.SERVICE_ID = '{ServiceId}') IQ""".format(UserId=User.Id, QuoteRecordId=ContractRecordId, ServiceId=ProductPartnumber, revision_rec_id = rev_rec_id)
		#Log.Info('renewal scenaro--------'+str(qtqtse_query))
		Sql.RunQuery(qtqtse_query)
		# cov_ent =Sql.GetList("""SELECT 
		# 		DISTINCT
		# 		CTCSCE.EQUIPMENT_ID,CTCSCE.EQUIPMENT_RECORD_ID,SAQSCO.QUOTE_ID,SAQSCO.QUOTE_RECORD_ID,SAQSCO.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,SAQTSE.QUOTE_SERVICE_ENTITLEMENT_RECORD_ID,CTCSCE.SERIAL_NO,CTCSCE.SERVICE_DESCRIPTION,CTCSCE.SERVICE_ID,CTCSCE.SERVICE_RECORD_ID,'{configurationId}' as CPS_CONFIGURATION_ID,'{cpsmatchId}' as  CPS_MATCH_ID,CTCTSO.SALESORG_ID, CTCTSO.SALESORG_NAME, CTCTSO.SALESORG_RECORD_ID, SAQTSE.KB_VERSION,SAQSCO.GREENBOOK,SAQSCO.GREENBOOK_RECORD_ID
		# 	FROM	
		# 	CTCSCE (NOLOCK) 
		# 	JOIN SAQSCO (NOLOCK) ON (CTCSCE.SERVICE_ID= SAQSCO.SERVICE_ID AND SAQSCO.EQUIPMENT_ID = CTCSCE.EQUIPMENT_ID) JOIN SAQTSE (NOLOCK) ON (SAQSCO.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID AND CTCSCE.SERVICE_ID= SAQTSE.SERVICE_ID) JOIN CTCTSO (NOLOCK) ON CTCTSO.CONTRACT_ID = CTCSCE.CONTRACT_ID						
		# 	WHERE CTCSCE.CONTRACT_ID = '{ContractId}' AND CTCSCE.SERVICE_ID = '{serviceId}' AND SAQSCO.QUOTE_RECORD_ID = '{ContractRecordId}'""".format(configurationId=configurationId, cpsmatchId = '1', ContractId=Qt_rec_id, serviceId=ProductPartnumber,ContractRecordId=ContractRecordId))
		# Log.Info('renewal scenaro----ContractRecordId----'+str(ContractRecordId))

		
		if cov_ent:
			tbrow = {}
			#Log.Info('aaaa--renewl--357-'+str(aaaa))
			for val in cov_ent:
				#Log.Info('aaaa--renewl-359--'+str(aaaa))
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
					</QUOTE_ITEM_ENTITLEMENT>""".format(ent_name = val.ENTITLEMENT_NAME,ent_val_code =val.ENTITLEMENT_VALUE_CODE,ent_type = val.ENTITLEMENT_TYPE,ent_desc = val.ENTITLEMENT_DESCRIPTION,ent_disp_val = val.ENTITLEMENT_DISPLAY_VALUE,ct = '',pi = '',is_default = '1',pm = '',cf = '')
				
				tbrow["QUOTE_SERVICE_COVERED_OBJ_ENTITLEMENTS_RECORD_ID"]=str(Guid.NewGuid()).upper()
				tbrow["QUOTE_ID"]=val.QUOTE_ID
				tbrow["ENTITLEMENT_XML"]=insertservice
				#tbrow["QUOTE_NAME"]=val.QUOTE_NAME
				tbrow["QUOTE_RECORD_ID"]=val.QUOTE_RECORD_ID
				tbrow["QTESRVCOB_RECORD_ID"]=val.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID
				tbrow["SERVICE_RECORD_ID"]=val.SERVICE_RECORD_ID
				tbrow["SERVICE_ID"]=val.SERVICE_ID
				tbrow["SERVICE_DESCRIPTION"]=val.SERVICE_DESCRIPTION
				tbrow["CPS_CONFIGURATION_ID"]=val.CPS_CONFIGURATION_ID
				tbrow["SALESORG_RECORD_ID"]=val.SALESORG_RECORD_ID
				tbrow["SALESORG_ID"]=val.SALESORG_ID
				tbrow["EQUIPMENT_ID"]=val.SALESORG_ID
				tbrow["EQUIPMENT_RECORD_ID"]=val.SALESORG_ID
				tbrow["QTESRVENT_RECORD_ID"]=val.SALESORG_ID
				tbrow["SALESORG_NAME"]=val.SALESORG_NAME
				tbrow["SERIAL_NO"]=val.SERIAL_NO
				tbrow["KB_VERSION"]=val.KB_VERSION
				tbrow["GREENBOOK"]=val.GREENBOOK
				tbrow["GREENBOOK_RECORD_ID"]=val.GREENBOOK_RECORD_ID
				tbrow["KB_VERSION"]=val.KB_VERSION
				tbrow["CPS_MATCH_ID"] = val.CPS_MATCH_ID
				#Log.Info('inside --384---------------------------'+str(tbrow))
				columns = ', '.join("" + str(x) + "" for x in tbrow.keys())
				values = ', '.join("'" + str(x) + "'" for x in tbrow.values())
				insert_QTQSCE_query = "INSERT INTO SAQSCE ( %s ) VALUES ( %s );" % (columns, values)
				
				Sql.RunQuery(insert_QTQSCE_query)
		
		# qtqsce="""INSERT SAQSCE
		# (ENTITLEMENT_XML,EQUIPMENT_ID,EQUIPMENT_RECORD_ID,QUOTE_ID,QUOTE_RECORD_ID,QTESRVCOB_RECORD_ID,QTESRVENT_RECORD_ID,SERIAL_NO,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,CPS_CONFIGURATION_ID,CPS_MATCH_ID,SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID, KB_VERSION, GREENBOOK,GREENBOOK_RECORD_ID, QUOTE_SERVICE_COVERED_OBJ_ENTITLEMENTS_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED) 
		# SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_COVERED_OBJ_ENTITLEMENTS_RECORD_ID, {UserId} as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM (
		# 	SELECT 
		# 		DISTINCT
		# 		LTRIM(RTRIM(SAQTSE.ENTITLEMENT_XML)) as ENTITLEMENT_XML,CTCSCE.EQUIPMENT_ID,CTCSCE.EQUIPMENT_RECORD_ID,SAQSCO.QUOTE_ID,SAQSCO.QUOTE_RECORD_ID,SAQSCO.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,SAQTSE.QUOTE_SERVICE_ENTITLEMENT_RECORD_ID,CTCSCE.SERIAL_NO,CTCSCE.SERVICE_DESCRIPTION,CTCSCE.SERVICE_ID,CTCSCE.SERVICE_RECORD_ID,'{configurationId}' as CPS_CONFIGURATION_ID,'{cpsmatchId}' as  CPS_MATCH_ID,CTCTSO.SALESORG_ID, CTCTSO.SALESORG_NAME, CTCTSO.SALESORG_RECORD_ID, SAQTSE.KB_VERSION,SAQSCO.GREENBOOK,SAQSCO.GREENBOOK_RECORD_ID
		# 	FROM	
		# 	CTCSCE (NOLOCK) 
		# 	JOIN SAQSCO (NOLOCK) ON (CTCSCE.SERVICE_ID= SAQSCO.SERVICE_ID AND SAQSCO.EQUIPMENT_ID = CTCSCE.EQUIPMENT_ID) JOIN SAQTSE (NOLOCK) ON (SAQSCO.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID AND CTCSCE.SERVICE_ID= SAQTSE.SERVICE_ID) JOIN CTCTSO (NOLOCK) ON CTCTSO.CONTRACT_ID = CTCSCE.CONTRACT_ID						
		# 	WHERE CTCSCE.CONTRACT_ID = '{ContractId}' AND CTCSCE.SERVICE_ID = '{serviceId}' AND SAQSCO.QUOTE_RECORD_ID = '{ContractRecordId}'
		# ) IQ""".format(UserId=User.Id, configurationId=configurationId, cpsmatchId = '1', ContractId=Qt_rec_id, serviceId=ProductPartnumber,ContractRecordId=ContractRecordId)
		# Log.Info("------qtqsce---"+str(qtqsce))
		# Sql.RunQuery(qtqsce)
		#insert in qtqtsce for renewal scenario
		# qtqsce = SqlHelper.GetFirst("sp_executesql @T=N'INSERT SAQSCE (ENTITLEMENT_XML,EQUIPMENT_ID,EQUIPMENT_RECORD_ID,QUOTE_ID,QUOTE_RECORD_ID,QTESRVCOB_RECORD_ID,QTESRVENT_RECORD_ID,SERIAL_NO,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,CPS_CONFIGURATION_ID,CPS_MATCH_ID,SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID, KB_VERSION, GREENBOOK,GREENBOOK_RECORD_ID, QUOTE_SERVICE_COVERED_OBJ_ENTITLEMENTS_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED) SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_COVERED_OBJ_ENTITLEMENTS_RECORD_ID, 129 as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM ( SELECT DISTINCT (SELECT  ISNULL(REPLACE(REPLACE(STUFF((SELECT '' ''+ JSON FROM (SELECT ''<QUOTE_ITEM_ENTITLEMENT>''+''<ENTITLEMENT_NAME>''+ISNULL(A.ENTITLEMENT_NAME,'''')+''</ENTITLEMENT_NAME>''+''<ENTITLEMENT_TYPE>''+ISNULL(A.ENTITLEMENT_TYPE,'''')+''</ENTITLEMENT_TYPE>''+''<ENTITLEMENT_DISPLAY_VALUE>''+ISNULL(A.ENTITLEMENT_DISPLAY_VALUE,'''')+''</ENTITLEMENT_DISPLAY_VALUE>''+''<ENTITLEMENT_DESCRIPTION>''+ISNULL(A.ENTITLEMENT_DESCRIPTION,'''')+''</ENTITLEMENT_DESCRIPTION>''+''</QUOTE_ITEM_ENTITLEMENT>'' AS JSON FROM ( SELECT B.ENTITLEMENT_NAME,B.ENTITLEMENT_TYPE,B.ENTITLEMENT_DISPLAY_VALUE, B.ENTITLEMENT_DESCRIPTION FROM CTCSCE B(NOLOCK) WHERE CTCSCE.SERVICE_ID = B.SERVICE_ID and CTCSCE.equipment_id = b.equipment_id and CTCSCE.contract_id = b.contract_id and B.contract_ID = ''"+str(Qt_rec_id)+"'' )A )A FOR XML PATH ('''') ), 1, 1,'''' ),''&lt;'',''<''),''&gt;'',''>''),''<QUOTE_ITEM_ENTITLEMENT></QUOTE_ITEM_ENTITLEMENT>'') AS final_xml) as ENTITLEMENT_XML,CTCSCE.EQUIPMENT_ID,CTCSCE.EQUIPMENT_RECORD_ID,SAQSCO.QUOTE_ID,SAQSCO.QUOTE_RECORD_ID,SAQSCO.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,SAQTSE.QUOTE_SERVICE_ENTITLEMENT_RECORD_ID,CTCSCE.SERIAL_NO,CTCSCE.SERVICE_DESCRIPTION,CTCSCE.SERVICE_ID,CTCSCE.SERVICE_RECORD_ID,''"+str(configurationId)+"''  as CPS_CONFIGURATION_ID,''1'' as CPS_MATCH_ID,CTCTSO.SALESORG_ID, CTCTSO.SALESORG_NAME, CTCTSO.SALESORG_RECORD_ID, SAQTSE.KB_VERSION,SAQSCO.GREENBOOK,SAQSCO.GREENBOOK_RECORD_ID FROM CTCSCE (NOLOCK) JOIN SAQSCO (NOLOCK) ON (CTCSCE.SERVICE_ID= SAQSCO.SERVICE_ID AND SAQSCO.EQUIPMENT_ID = CTCSCE.EQUIPMENT_ID) JOIN SAQTSE (NOLOCK) ON (SAQSCO.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID AND CTCSCE.SERVICE_ID= SAQTSE.SERVICE_ID) JOIN CTCTSO (NOLOCK) ON CTCTSO.CONTRACT_ID = CTCSCE.CONTRACT_ID WHERE CTCSCE.CONTRACT_ID = ''"+str(Qt_rec_id)+"'' AND CTCSCE.SERVICE_ID =  ''"+str(ProductPartnumber)+"'' AND SAQSCO.QUOTE_ID = ''"+str(ContractRecordId)+"''  ) IQ  '")
		#Log.Info("------qtqsce--ContractRecordId----"+str(ContractRecordId)+'---Qt_rec_id----'+str(Qt_rec_id)+'----'+str(configurationId)+'--ProductPartnumber---'+str(ProductPartnumber))
		#qtqsce = SqlHelper.GetFirst("sp_executesql @T=N'INSERT SAQSCE (ENTITLEMENT_XML,EQUIPMENT_ID,EQUIPMENT_RECORD_ID,QUOTE_ID,QUOTE_RECORD_ID,QTESRVCOB_RECORD_ID,QTESRVENT_RECORD_ID,SERIAL_NO,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,CPS_CONFIGURATION_ID,CPS_MATCH_ID,SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID, KB_VERSION, GREENBOOK,GREENBOOK_RECORD_ID, QUOTE_SERVICE_COVERED_OBJ_ENTITLEMENTS_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED) SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_COVERED_OBJ_ENTITLEMENTS_RECORD_ID, 129 as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM ( SELECT DISTINCT (SELECT  ISNULL(REPLACE(REPLACE(STUFF((SELECT '' ''+ JSON FROM (SELECT ''<QUOTE_ITEM_ENTITLEMENT>''+''''+ISNULL(A.ENTITLEMENT_NAME,'''')+''</ENTITLEMENT_NAME>''+''<ENTITLEMENT_TYPE>''+ISNULL(A.ENTITLEMENT_TYPE,'''')+''</ENTITLEMENT_TYPE>''+''<ENTITLEMENT_DISPLAY_VALUE>''+ISNULL(A.ENTITLEMENT_DISPLAY_VALUE,'''')+''</ENTITLEMENT_DISPLAY_VALUE>''+''<ENTITLEMENT_DESCRIPTION>''+ISNULL(A.ENTITLEMENT_DESCRIPTION,'''')+''</ENTITLEMENT_DESCRIPTION>''+''</QUOTE_ITEM_ENTITLEMENT>'' AS JSON FROM ( SELECT B.ENTITLEMENT_NAME,B.ENTITLEMENT_TYPE,B.ENTITLEMENT_DISPLAY_VALUE, B.ENTITLEMENT_DESCRIPTION FROM CTCSCE B(NOLOCK) WHERE A.SERVICE_ID = B.SERVICE_ID and a.equipment_id = b.equipment_id and a.contract_id = b.contract_id and B.contract_ID = ''"+str(Qt_rec_id)+"'' )A )A FOR XML PATH ('''') ), 1, 1,'''' ),''&lt;'',''<''),''&gt;'',''>''),''<QUOTE_ITEM_ENTITLEMENT></QUOTE_ITEM_ENTITLEMENT>'') AS final_xml FROM CTCSCE (NOLOCK) A WHERE A.CONTRACT_ID = ''"+str(Qt_rec_id)+"'' ) as ENTITLEMENT_XML,CTCSCE.EQUIPMENT_ID,CTCSCE.EQUIPMENT_RECORD_ID,SAQSCO.QUOTE_ID,SAQSCO.QUOTE_RECORD_ID,SAQSCO.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,SAQTSE.QUOTE_SERVICE_ENTITLEMENT_RECORD_ID,CTCSCE.SERIAL_NO,CTCSCE.SERVICE_DESCRIPTION,CTCSCE.SERVICE_ID,CTCSCE.SERVICE_RECORD_ID,''"+str(configurationId)+"'' as CPS_CONFIGURATION_ID,''1'' as CPS_MATCH_ID,CTCTSO.SALESORG_ID, CTCTSO.SALESORG_NAME, CTCTSO.SALESORG_RECORD_ID, SAQTSE.KB_VERSION,SAQSCO.GREENBOOK,SAQSCO.GREENBOOK_RECORD_ID FROM CTCSCE (NOLOCK) JOIN SAQSCO (NOLOCK) ON (CTCSCE.SERVICE_ID= SAQSCO.SERVICE_ID AND SAQSCO.EQUIPMENT_ID = CTCSCE.EQUIPMENT_ID) JOIN SAQTSE (NOLOCK) ON (SAQSCO.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID AND CTCSCE.SERVICE_ID= SAQTSE.SERVICE_ID) JOIN CTCTSO (NOLOCK) ON CTCTSO.CONTRACT_ID = CTCSCE.CONTRACT_ID WHERE CTCSCE.CONTRACT_ID = ''"+str(Qt_rec_id)+"'' AND CTCSCE.SERVICE_ID = ''"+str(ProductPartnumber)+"'' AND SAQSCO.QUOTE_RECORD_ID = ''"+str(ContractRecordId)+"'' ) IQ  '")
		qtqsce="""INSERT SAQSCE
		(ENTITLEMENT_XML,EQUIPMENT_ID,EQUIPMENT_RECORD_ID,QUOTE_ID,QUOTE_RECORD_ID,QTESRVCOB_RECORD_ID,QTESRVENT_RECORD_ID,SERIAL_NO,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,CPS_CONFIGURATION_ID,CPS_MATCH_ID,SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID, KB_VERSION, GREENBOOK,GREENBOOK_RECORD_ID, QUOTE_SERVICE_COVERED_OBJ_ENTITLEMENTS_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED) 
		SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_COVERED_OBJ_ENTITLEMENTS_RECORD_ID, {UserId} as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM (
			SELECT 
				DISTINCT
				ISNULL(REPLACE(REPLACE(STUFF((SELECT ' '+ JSON FROM (SELECT '<QUOTE_ITEM_ENTITLEMENT>'+'<ENTITLEMENT_NAME>'+ISNULL(CTCSCE.ENTITLEMENT_NAME,'')+'</ENTITLEMENT_NAME>'+'<ENTITLEMENT_TYPE>'+ISNULL(CTCSCE.ENTITLEMENT_TYPE,'')+'</ENTITLEMENT_TYPE>'+'<ENTITLEMENT_DISPLAY_VALUE>'+ISNULL(CTCSCE.ENTITLEMENT_DISPLAY_VALUE,'')+'</ENTITLEMENT_DISPLAY_VALUE>'+'<ENTITLEMENT_DESCRIPTION>'+ISNULL(CTCSCE.ENTITLEMENT_DESCRIPTION,'')+'</ENTITLEMENT_DESCRIPTION>'+'</QUOTE_ITEM_ENTITLEMENT>' AS JSON FROM ( SELECT distinct B.ENTITLEMENT_NAME,B.ENTITLEMENT_TYPE,B.ENTITLEMENT_DISPLAY_VALUE, B.ENTITLEMENT_DESCRIPTION FROM CTCSCE B(NOLOCK) WHERE CTCSCE.SERVICE_ID = B.SERVICE_ID and CTCSCE.equipment_id = b.equipment_id and CTCSCE.contract_id = b.contract_id and B.contract_ID = '{ContractId}')CTCSCE )CTCSCE FOR XML PATH ('') ), 1, 1,'' ),'&lt;','<'),'&gt;','>'),'<QUOTE_ITEM_ENTITLEMENT></QUOTE_ITEM_ENTITLEMENT>') AS final_xml,CTCSCE.EQUIPMENT_ID,CTCSCE.EQUIPMENT_RECORD_ID,SAQSCO.QUOTE_ID,SAQSCO.QUOTE_RECORD_ID,SAQSCO.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,SAQTSE.QUOTE_SERVICE_ENTITLEMENT_RECORD_ID,CTCSCE.SERIAL_NO,CTCSCE.SERVICE_DESCRIPTION,CTCSCE.SERVICE_ID,CTCSCE.SERVICE_RECORD_ID,'{configurationId}' as CPS_CONFIGURATION_ID,'{cpsmatchId}' as  CPS_MATCH_ID,CTCTSO.SALESORG_ID, CTCTSO.SALESORG_NAME, CTCTSO.SALESORG_RECORD_ID, SAQTSE.KB_VERSION,SAQSCO.GREENBOOK,SAQSCO.GREENBOOK_RECORD_ID
			FROM	
			CTCSCE (NOLOCK) 
			JOIN SAQSCO (NOLOCK) ON (CTCSCE.SERVICE_ID= SAQSCO.SERVICE_ID AND SAQSCO.EQUIPMENT_ID = CTCSCE.EQUIPMENT_ID) JOIN SAQTSE (NOLOCK) ON (SAQSCO.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID AND CTCSCE.SERVICE_ID= SAQTSE.SERVICE_ID) JOIN CTCTSO (NOLOCK) ON CTCTSO.CONTRACT_ID = CTCSCE.CONTRACT_ID						
			WHERE CTCSCE.CONTRACT_ID = '{ContractId}' AND CTCSCE.SERVICE_ID = '{serviceId}' AND SAQSCO.QUOTE_RECORD_ID = '{ContractRecordId}') IQ""".format(UserId=User.Id, configurationId=configurationId, cpsmatchId = '1', ContractId=Qt_rec_id, serviceId=ProductPartnumber,ContractRecordId=ContractRecordId)
		Log.Info("---qtqsce---"+str(qtqsce))
		Sql.RunQuery(qtqsce)
		GetEqp = SqlHelper.GetList("select distinct EQUIPMENT_ID from CTCSCE where CONTRACT_ID = '{ContractId}' AND SERVICE_ID = '{ServiceId}' ".format(ContractId=Qt_rec_id,ServiceId=ProductPartnumber))
		tableInfo = SqlHelper.GetTable("SAQSCE")
		for eqp in GetEqp:
			qtqscelist =[]
			#qtqsce = SqlHelper.GetList("SELECT distinct replace(X.Y.value('(ENTITLEMENT_NAME)[1]', 'VARCHAR(128)'),';#38','&') as ENTITLEMENT_NAME FROM SAQSCE (NOLOCK) WHERE SERVICE_ID = '{ServiceId}' AND QUOTE_RECORD_ID = '{QuoteRecordId}' and EQUIPMENT_ID = '{EquipmentId}'".format(ServiceId=ProductPartnumber, QuoteRecordId=ContractRecordId, EquipmentId = str(eqp.EQUIPMENT_ID)))
			qtqsce = SqlHelper.GetList("SELECT ENTITLEMENT_NAME FROM SAQSCE (NOLOCK) WHERE SERVICE_ID = '{ServiceId}' AND QUOTE_RECORD_ID = '{QuoteRecordId}' and EQUIPMENT_ID = '{EquipmentId}'".format(ServiceId=ProductPartnumber, QuoteRecordId=ContractRecordId, EquipmentId = str(eqp.EQUIPMENT_ID)))
			qtqscedetail = SqlHelper.GetFirst("SELECT ENTITLEMENT_ID FROM SAQSCE (NOLOCK) WHERE SERVICE_ID = '{ServiceId}' AND QUOTE_RECORD_ID = '{QuoteRecordId}' and EQUIPMENT_ID = '{EquipmentId}'".format(ServiceId=ProductPartnumber, QuoteRecordId=ContractRecordId, EquipmentId = str(eqp.EQUIPMENT_ID)))
			for val in qtqsce:
				ENTITLEMENTNAME = val.ENTITLEMENT_ID     
				qtqscelist.append(ENTITLEMENTNAME)
				if ENTITLEMENTNAME not in attributeList:                    
					deletequery = Sql.RunQuery("DELETE FROM SAQSCE where WHERE ENTITLEMENT_ID = '{EntName}' and SERVICE_ID = '{ServiceId}' AND QUOTE_RECORD_ID = '{QuoteRecordId}' and EQUIPMENT_ID = '{EquipmentId}'".format(EntName = str(val.ENTITLEMENT_ID), ServiceId=ProductPartnumber,QuoteRecordId=ContractRecordId,EquipmentId = str(eqp.EQUIPMENT_ID)))
			for key,value in zip(attributeList,attributevalueList):
				if key not in qtqscelist:
					Log.Info(key)                    
					GetAttDetail = SqlHelper.GetFirst("SELECT S.STANDARD_ATTRIBUTE_DISPLAY_VAL,A.STANDARD_ATTRIBUTE_NAME FROM STANDARD_ATTRIBUTE_VALUES (nolock) S INNER JOIN ATTRIBUTE_DEFN (NOLOCK) A ON A.STANDARD_ATTRIBUTE_CODE=S.STANDARD_ATTRIBUTE_CODE WHERE A.SYSTEM_ID = '{}' AND S.STANDARD_ATTRIBUTE_VALUE = '{}'".format(key,value))
					tbrow = {}
					tbrow["QUOTE_SERVICE_COVERED_OBJ_ENTITLEMENTS_RECORD_ID"]= qtqscedetail.QUOTE_SERVICE_COVERED_OBJ_ENTITLEMENTS_RECORD_ID
					tbrow["ENTITLEMENT_NAME"]= str(key)
					tbrow["ENTITLEMENT_TYPE"]=''
					tbrow["ENTITLEMENT_VALUE_CODE"]= str(value)
					tbrow["EQUIPMENT_ID"]= qtqscedetail.EQUIPMENT_ID
					tbrow["EQUIPMENT_RECORD_ID"]= qtqscedetail.EQUIPMENT_RECORD_ID
					tbrow["QUOTE_ID"]= qtqscedetail.QUOTE_ID
					tbrow["QUOTE_RECORD_ID"]= qtqscedetail.QUOTE_RECORD_ID
					tbrow["QTESRVCOB_RECORD_ID"]= qtqscedetail.QTESRVCOB_RECORD_ID
					tbrow["QTESRVENT_RECORD_ID"]= qtqscedetail.QTESRVENT_RECORD_ID
					tbrow["SERIAL_NO"]= qtqscedetail.SERIAL_NO
					tbrow["SERVICE_DESCRIPTION"]= qtqscedetail.SERVICE_DESCRIPTION
					tbrow["SERVICE_ID"]= qtqscedetail.SERVICE_ID
					tbrow["SERVICE_RECORD_ID"]= qtqscedetail.SERVICE_RECORD_ID
					tbrow["ENTITLEMENT_DESCRIPTION"]= GetAttDetail.STANDARD_ATTRIBUTE_NAME
					tbrow["ENTITLEMENT_DISPLAY_VALUE"]= GetAttDetail.STANDARD_ATTRIBUTE_DISPLAY_VAL
					tbrow["CPS_CONFIGURATION_ID"]= qtqscedetail.CPS_CONFIGURATION_ID
					tbrow["CPS_MATCH_ID"]= qtqscedetail.CPS_MATCH_ID
					tbrow["SALESORG_ID"]= qtqscedetail.SALESORG_ID
					tbrow["SALESORG_NAME"]= qtqscedetail.SALESORG_NAME
					tbrow["SALESORG_RECORD_ID"]= qtqscedetail.SALESORG_RECORD_ID
					tbrow["KB_VERSION"]= qtqscedetail.KB_VERSION
					tbrow["GREENBOOK"]= qtqscedetail.GREENBOOK
					tbrow["GREENBOOK_RECORD_ID"]= qtqscedetail.GREENBOOK_RECORD_ID	
					tbrow["CPQTABLEENTRYADDEDBY"]= qtqscedetail.CPQTABLEENTRYADDEDBY
					tbrow["ADDUSR_RECORD_ID"]= qtqscedetail.ADDUSR_RECORD_ID
					tbrow["CPQTABLEENTRYDATEADDED"]= qtqscedetail.CPQTABLEENTRYDATEADDED
					tableInfo.AddRow(tbrow)
				Sql.Upsert(tableInfo)
		
	
def covobjrenewal_two():    
	for configurationId,ProductPartnumber in zip(configuration,ProductPart):
		SAQIEN = """INSERT SAQIEN 
				(ENTITLEMENT_NAME,ENTITLEMENT_TYPE,ENTITLEMENT_VALUE_CODE,EQUIPMENT_ID,EQUIPMENT_RECORD_ID,ITEM_LINE_ID,QUOTE_ID,QTEITMCOB_RECORD_ID,QTEITM_RECORD_ID,	
				QUOTE_RECORD_ID,QTESRVENT_RECORD_ID,SERIAL_NO,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,CPS_CONFIGURATION_ID,  ENTITLEMENT_DESCRIPTION,ENTITLEMENT_DISPLAY_VALUE,EQUIPMENT_LINE_ID, CPS_MATCH_ID,KB_VERSION, QUOTE_ITEM_COVERED_OBJECT_ENTITLEMENTS_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED)
				SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_COVERED_OBJECT_ENTITLEMENTS_RECORD_ID, {UserId} as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM (
					SELECT 
						DISTINCT
						CTCIEN.ENTITLEMENT_NAME,CTCIEN.ENTITLEMENT_TYPE,CTCIEN.ENTITLEMENT_VALUE_CODE,CTCIEN.EQUIPMENT_ID,CTCIEN.EQUIPMENT_RECORD_ID,CTCIEN.LINE_ITEM_ID,SAQICO.QUOTE_ID,SAQICO.QUOTE_ITEM_COVERED_OBJECT_RECORD_ID,SAQICO.QTEITM_RECORD_ID,SAQICO.QUOTE_RECORD_ID,SAQTSE.QUOTE_SERVICE_ENTITLEMENT_RECORD_ID,CTCIEN.SERIAL_NUMBER,CTCIEN.SERVICE_DESCRIPTION,CTCIEN.SERVICE_ID,CTCIEN.SERVICE_RECORD_ID,CTCIEN.SALESORG_ID,CTCIEN.SALESORG_NAME,CTCIEN.SALESORG_RECORD_ID,'{configurationId}' as CPS_CONFIGURATION_ID,CTCIEN.ENTITLEMENT_DESCRIPTION,CTCIEN.ENTITLEMENT_DISPLAY_VALUE,CTCIEN.EQUIPMENT_LINE_ID, '{cpsmatchId}' as CPS_MATCH_ID, SAQTSE.KB_VERSION
					FROM	
					CTCIEN (NOLOCK)												
					JOIN SAQICO (NOLOCK) ON (CTCIEN.SERVICE_ID= SAQICO.SERVICE_ID AND SAQICO.EQUIPMENT_RECORD_ID = CTCIEN.EQUIPMENT_RECORD_ID) JOIN SAQTSE (NOLOCK) ON (SAQICO.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID AND CTCIEN.SERVICE_ID= SAQTSE.SERVICE_ID AND CTCIEN.ENTITLEMENT_NAME = SAQTSE.ENTITLEMENT_NAME)  
					WHERE CTCIEN.CONTRACT_ID = '{ContractId}' AND CTCIEN.SERVICE_ID = '{serviceId}' AND SAQICO.QUOTE_RECORD_ID = '{ContractRecordId}'
				) IQ""".format(UserId=User.Id, configurationId=configurationId, cpsmatchId='1', ContractId=Qt_rec_id, serviceId=ProductPartnumber,ContractRecordId=ContractRecordId)
		Log.Info(SAQIEN)
		Sql.RunQuery(SAQIEN)        

def SparepartsItem():
	if TreeParam != 'Z0100':
		SAQIEN="""INSERT SAQIEN 
				(KB_VERSION,ENTITLEMENT_XML,EQUIPMENT_ID,EQUIPMENT_RECORD_ID,
				QTEITM_RECORD_ID, QTESRVENT_RECORD_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,SALESORG_ID,SALESORG_NAME,
				SALESORG_RECORD_ID,CPS_CONFIGURATION_ID,
				EQUIPMENT_LINE_ID, QUOTE_ID, QUOTE_RECORD_ID, QUOTE_ITEM_COVERED_OBJECT_ENTITLEMENTS_RECORD_ID, 
				CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED)
				SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_COVERED_OBJECT_ENTITLEMENTS_RECORD_ID, {UserId} as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM (
					SELECT 
						DISTINCT
						SAQTSE.KB_VERSION,SAQTSE.ENTITLEMENT_XML,SAQIFP.PART_NUMBER as EQUIPMENT_ID,SAQIFP.PART_RECORD_ID as EQUIPMENT_RECORD_ID,SAQIFP.QTEITM_RECORD_ID,SAQTSE.QUOTE_SERVICE_ENTITLEMENT_RECORD_ID as QTESRVENT_RECORD_ID,SAQTSE.SERVICE_DESCRIPTION,SAQTSE.SERVICE_ID,SAQTSE.SERVICE_RECORD_ID,SAQTSE.SALESORG_ID,SAQTSE.SALESORG_NAME,
						SAQTSE.SALESORG_RECORD_ID,SAQTSE.CPS_CONFIGURATION_ID,'' as EQUIPMENT_LINE_ID,
						SAQTSE.QUOTE_ID, SAQTSE.QUOTE_RECORD_ID
					FROM	
					SAQTSE (NOLOCK)
					JOIN SAQIFP (NOLOCK) ON SAQIFP.SERVICE_RECORD_ID = SAQTSE.SERVICE_RECORD_ID AND SAQIFP.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID
					
					WHERE SAQTSE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQTSE.SERVICE_ID = '{ServiceId}' 
				) IQ
				""".format(UserId=userId, QuoteRecordId= Qt_rec_id, ServiceId=TreeParam)
		Log.Info("---416---"+str(SAQIEN))
		Sql.RunQuery(SAQIEN)
	#insert to SAQSPT
	SAQSPE_query = """
				INSERT SAQSPE
				(KB_VERSION,ENTITLEMENT_XML,QUOTE_ID,
				QUOTE_RECORD_ID,QTESRVENT_RECORD_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,CPS_CONFIGURATION_ID,QTESRVPRT_RECORD_ID,PART_RECORD_ID,PART_DESCRIPTION,PART_NUMBER,QUOTE_SERVICE_PART_ENTITLEMENT_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED)
				SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_SERVICE_PART_ENTITLEMENT_RECORD_ID, {UserId} as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM (
					SELECT 
						DISTINCT
						SAQTSE.KB_VERSION,SAQTSE.ENTITLEMENT_XML,SAQTSE.QUOTE_ID,SAQTSE.QUOTE_RECORD_ID,SAQTSE.QUOTE_SERVICE_ENTITLEMENT_RECORD_ID as QTESRVENT_RECORD_ID,SAQTSE.SERVICE_DESCRIPTION,SAQTSE.SERVICE_ID,SAQTSE.SERVICE_RECORD_ID,SAQTSE.SALESORG_ID,SAQTSE.SALESORG_NAME,SAQTSE.SALESORG_RECORD_ID,SAQTSE.CPS_CONFIGURATION_ID,SAQSPT.QUOTE_SERVICE_PART_RECORD_ID as QTESRVPRT_RECORD_ID,SAQSPT.PART_RECORD_ID,SAQSPT.PART_DESCRIPTION,SAQSPT.PART_NUMBER
					FROM	
					SAQTSE (NOLOCK)
					JOIN SAQSPT (NOLOCK) ON SAQSPT.SERVICE_RECORD_ID = SAQTSE.SERVICE_RECORD_ID AND SAQSPT.QUOTE_RECORD_ID = SAQTSE.QUOTE_RECORD_ID
					WHERE SAQTSE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQTSE.SERVICE_ID = '{ServiceId}') IQ
				""".format(UserId=User.Id, QuoteRecordId=Qt_rec_id, ServiceId=TreeParam)
	#Log.Info("SAQSPE_query--23130-----"+str(SAQSPE_query))
	Sql.RunQuery(SAQSPE_query)
	#insert to SAQSPT
	# SAQIPE_query = """
	# 			INSERT SAQIPE
	# 			(ENTITLEMENT_XML,QUOTE_ID,
	# 			QUOTE_RECORD_ID,LINE_ITEM_ID,SERVICE_DESCRIPTION,SERVICE_ID,SERVICE_RECORD_ID,SALESORG_ID,SALESORG_NAME,SALESORG_RECORD_ID,CPS_CONFIGURATION_ID,PART_RECORD_ID,PART_DESCRIPTION,PART_NUMBER,QTEITMFPT_RECORD_ID,QTEITM_RECORD_ID,QUOTE_ITEM_FORECAST_PART_ENT_RECORD_ID,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEADDED)
	# 			SELECT IQ.*, CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_FORECAST_PART_ENT_RECORD_ID, {UserId} as CPQTABLEENTRYADDEDBY, GETDATE() as CPQTABLEENTRYDATEADDED FROM (
	# 				SELECT 
	# 					DISTINCT
	# 					SAQSPE.ENTITLEMENT_XML,SAQSPE.QUOTE_ID,SAQSPE.QUOTE_RECORD_ID,SAQITM.LINE_ITEM_ID,SAQSPE.SERVICE_DESCRIPTION,SAQSPE.SERVICE_ID,SAQSPE.SERVICE_RECORD_ID,SAQSPE.SALESORG_ID,SAQSPE.SALESORG_NAME,SAQSPE.SALESORG_RECORD_ID,SAQSPE.CPS_CONFIGURATION_ID,SAQSPE.PART_RECORD_ID,SAQSPE.PART_DESCRIPTION,SAQSPE.PART_NUMBER,SAQIFP.QUOTE_ITEM_FORECAST_PART_RECORD_ID as QTEITMFPT_RECORD_ID,SAQITM.QUOTE_ITEM_RECORD_ID as QTEITM_RECORD_ID
	# 				FROM	
	# 				SAQSPE (NOLOCK)
	# 				JOIN SAQITM (NOLOCK) ON SAQSPE.SERVICE_RECORD_ID = SAQITM.SERVICE_RECORD_ID AND SAQSPE.QUOTE_RECORD_ID = SAQITM.QUOTE_RECORD_ID
	# 				JOIN SAQIFP (NOLOCK) ON SAQIFP.SERVICE_RECORD_ID = SAQSPE.SERVICE_RECORD_ID AND SAQIFP.QUOTE_RECORD_ID = SAQSPE.QUOTE_RECORD_ID
	# 				WHERE SAQSPE.QUOTE_RECORD_ID = '{QuoteRecordId}' AND SAQSPE.SERVICE_ID = '{ServiceId}') IQ
	# 			""".format(UserId=User.Id, QuoteRecordId=Qt_rec_id, ServiceId=TreeParam)
	# Log.Info("SAQIPE_query--668----"+str(SAQIPE_query))
	# Sql.RunQuery(SAQIPE_query)


def quote_SAQICOupdate(cart_id,cart_user_id):
	
	Log.Info('648---CQROLLDOWN-----')
	quote_item_covered_obj_delete= """DELETE QT__SAQICO 
								FROM QT__SAQICO 
								JOIN SAQTSV (NOLOCK) ON SAQTSV.SERVICE_RECORD_ID = QT__SAQICO.SERVICE_RECORD_ID AND SAQTSV.QUOTE_RECORD_ID = QT__SAQICO.QUOTE_RECORD_ID  
								WHERE QT__SAQICO.cartId = '{CartId}' AND ownerId = {UserId} AND QT__SAQICO.QUOTE_RECORD_ID = '{QuoteRecordId}' """.format(
				CartId=cart_id, UserId=cart_user_id, QuoteRecordId=Qt_rec_id)
	Sql.RunQuery(quote_item_covered_obj_delete) 
	# Update Quote Item Pricing Columns - Start  
	# Sql.RunQuery("""UPDATE SAQITM
	# 					SET OBJECT_QUANTITY = IQ.EQUIPMENT_ID_COUNT,
	# 					EXTENDED_PRICE = IQ.EXTENDED_PRICE,					
	# 					BD_PRICE = IQ.BD_PRICE,
	# 					SALES_PRICE = IQ.SALES_PRICE,
	# 					TARGET_PRICE = IQ.TARGET_PRICE,
	# 					CEILING_PRICE = IQ.CEILING_PRICE,
	# 					SALES_DISCOUNT_PRICE = IQ.SALES_DISCOUNT_PRICE,
	# 					YEAR_1 = IQ.YEAR_1,
	# 					YEAR_2 = IQ.YEAR_2,
	# 					YEAR_3 = IQ.YEAR_3,
	# 					YEAR_4 = IQ.YEAR_4,
	# 					YEAR_5 = IQ.YEAR_5
	# 					FROM SAQITM (NOLOCK)
	# 					INNER JOIN (SELECT SAQITM.CpqTableEntryId,
	# 								COUNT(SAQICO.EQUIPMENT_ID) as EQUIPMENT_ID_COUNT,			
	# 								ISNULL(SUM(ISNULL(SAQICO.EXTENDED_PRICE, 0)), 0) as EXTENDED_PRICE,					
	# 								ISNULL(SUM(ISNULL(SAQICO.BD_PRICE, 0)), 0) as BD_PRICE,
	# 								ISNULL(SUM(ISNULL(SAQICO.SALES_PRICE, 0)), 0) as SALES_PRICE,
	# 								ISNULL(SUM(ISNULL(SAQICO.TARGET_PRICE, 0)), 0) as TARGET_PRICE,								
	# 								ISNULL(SUM(ISNULL(SAQICO.CEILING_PRICE, 0)), 0) as CEILING_PRICE,
	# 								ISNULL(SUM(ISNULL(SAQICO.SALES_DISCOUNT_PRICE, 0)), 0) as SALES_DISCOUNT_PRICE,								
	# 								ISNULL(SUM(ISNULL(SAQICO.YEAR_1, 0)), 0) as YEAR_1,
	# 								ISNULL(SUM(ISNULL(SAQICO.YEAR_2, 0)), 0) as YEAR_2,
	# 								ISNULL(SUM(ISNULL(SAQICO.YEAR_3, 0)), 0) as YEAR_3,
	# 								ISNULL(SUM(ISNULL(SAQICO.YEAR_4, 0)), 0) as YEAR_4,
	# 								ISNULL(SUM(ISNULL(SAQICO.YEAR_5, 0)), 0) as YEAR_5
	# 								FROM SAQITM (NOLOCK) 
	# 								JOIN SAQICO (NOLOCK) ON SAQICO.QUOTE_RECORD_ID = SAQITM.QUOTE_RECORD_ID AND SAQICO.LINE_ITEM_ID = SAQITM.LINE_ITEM_ID
	# 								WHERE SAQITM.QUOTE_RECORD_ID = '{QuoteRecordId}' 
	# 								GROUP BY SAQITM.LINE_ITEM_ID, SAQITM.SERVICE_ID, SAQITM.QUOTE_RECORD_ID, SAQITM.CpqTableEntryId)IQ
	# 					ON SAQITM.CpqTableEntryId = IQ.CpqTableEntryId 
	# 					WHERE SAQITM.QUOTE_RECORD_ID = '{QuoteRecordId}'""".format(QuoteRecordId=Qt_rec_id))
					
	# Sql.RunQuery("""UPDATE SAQITM
	# 	SET OBJECT_QUANTITY = IQ.OBJECT_QUANTITY,
	# 	EXTENDED_PRICE = IQ.EXTENDED_PRICE,					
	# 	TAX=IQ.TAX,
	# 	BD_PRICE = IQ.BD_PRICE,
	# 	SALES_PRICE = IQ.SALES_PRICE,
	# 	TARGET_PRICE = IQ.TARGET_PRICE,
	# 	CEILING_PRICE = IQ.CEILING_PRICE,
	# 	SALES_DISCOUNT_PRICE = IQ.SALES_DISCOUNT_PRICE,
	# 	YEAR_1 = IQ.YEAR_1,
	# 	YEAR_2 = IQ.YEAR_2,
	# 	YEAR_3 = IQ.YEAR_3,
	# 	YEAR_4 = IQ.YEAR_4,
	# 	YEAR_5 = IQ.YEAR_5
	# 	FROM SAQITM (NOLOCK)
	# 	INNER JOIN (SELECT SAQITM.PARQTEITM_LINE, SAQITM.QUOTE_RECORD_ID,
	# 				SUM(SAQITM.OBJECT_QUANTITY) as OBJECT_QUANTITY,
	
	# 				ISNULL(SUM(ISNULL(SAQITM.EXTENDED_PRICE, 0)), 0) as EXTENDED_PRICE,					
	# 				ISNULL(SUM(ISNULL(SAQITM.TAX, 0)), 0) as TAX,
	# 				ISNULL(SUM(ISNULL(SAQITM.BD_PRICE, 0)), 0) as BD_PRICE,
	# 				ISNULL(SUM(ISNULL(SAQITM.SALES_PRICE, 0)), 0) as SALES_PRICE,
	# 				ISNULL(SUM(ISNULL(SAQITM.TARGET_PRICE, 0)), 0) as TARGET_PRICE,								
	# 				ISNULL(SUM(ISNULL(SAQITM.CEILING_PRICE, 0)), 0) as CEILING_PRICE,
	# 				ISNULL(SUM(ISNULL(SAQITM.SALES_DISCOUNT_PRICE, 0)), 0) as SALES_DISCOUNT_PRICE,								
	# 				ISNULL(SUM(ISNULL(SAQITM.YEAR_1, 0)), 0) as YEAR_1,
	# 				ISNULL(SUM(ISNULL(SAQITM.YEAR_2, 0)), 0) as YEAR_2,
	# 				ISNULL(SUM(ISNULL(SAQITM.YEAR_3, 0)), 0) as YEAR_3,
	# 				ISNULL(SUM(ISNULL(SAQITM.YEAR_4, 0)), 0) as YEAR_4,
	# 				ISNULL(SUM(ISNULL(SAQITM.YEAR_5, 0)), 0) as YEAR_5
	# 				FROM SAQITM (NOLOCK) 					
	# 				WHERE SAQITM.QUOTE_RECORD_ID = '{QuoteRecordId}' AND ISNULL(SAQITM.PARQTEITM_LINE,'') <> ''
	# 				GROUP BY SAQITM.PARQTEITM_LINE, SAQITM.QUOTE_RECORD_ID)IQ
	# 	ON SAQITM.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND SAQITM.LINE_ITEM_ID = IQ.PARQTEITM_LINE 
	# 	WHERE ISNULL(SAQITM.PARQTEITM_LINE,'') = '' AND SAQITM.QUOTE_RECORD_ID = '{QuoteRecordId}'""".format(QuoteRecordId=Qt_rec_id))  


	# Sql.RunQuery("""UPDATE SAQITM
	# 	SET OBJECT_QUANTITY = IQ.OBJECT_QUANTITY
	# 	FROM SAQITM (NOLOCK)
	# 	INNER JOIN (SELECT SAQITM.PARQTEITM_LINE, SAQITM.QUOTE_RECORD_ID,
	# 				SUM(SAQITM.OBJECT_QUANTITY) as OBJECT_QUANTITY
	# 				FROM SAQITM (NOLOCK) 					
	# 				WHERE SAQITM.QUOTE_RECORD_ID = '{QuoteRecordId}' AND ISNULL(SAQITM.PARQTEITM_LINE,'') <> '' AND SERVICE_ID LIKE '%BASE'
	# 				GROUP BY SAQITM.PARQTEITM_LINE, SAQITM.QUOTE_RECORD_ID)IQ
	# 	ON SAQITM.QUOTE_RECORD_ID = IQ.QUOTE_RECORD_ID AND SAQITM.LINE_ITEM_ID = IQ.PARQTEITM_LINE 
	# 	WHERE ISNULL(SAQITM.PARQTEITM_LINE,'') = '' AND SAQITM.QUOTE_RECORD_ID = '{QuoteRecordId}'""".format(QuoteRecordId=Qt_rec_id))
	# # Update Quote Item Pricing Columns - End
	# #updating upsell price start
	# gettotal_bundle_query=Sql.GetFirst("""SELECT sum(SAQICO.YEAR_1) as YEAR_1 ,sum(SAQICO.YEAR_2) as YEAR_2,sum(SAQICO.YEAR_3) as YEAR_3,sum(SAQICO.YEAR_4) as YEAR_4,sum(SAQICO.YEAR_5) as YEAR_5,sum(SAQICO.TAX_PERCENTAGE) as TAX_PER,sum(SAQICO.EXTENDED_PRICE) AS EXTENDED_PRICE
	# 						FROM SAQICO 
	# 						JOIN SAQITM ON SAQITM.QUOTE_RECORD_ID = SAQICO.QUOTE_RECORD_ID and SAQITM.LINE_ITEM_ID = SAQICO.LINE_ITEM_ID WHERE SAQICO.QUOTE_RECORD_ID = '{Qt_rec_id}' Group by SAQICO.EQUIPMENT_ID,SAQICO.SERIAL_NO""".format(Qt_rec_id = Qt_rec_id))
	gettools_count = getext_price = serv_desct = getdiv = ""
	check_spare = Sql.GetFirst("select SERVICE_DESCRIPTION from SAQIFP where QUOTE_RECORD_ID = '{Qt_rec_id}' and SERVICE_ID ='Z0100'".format(Qt_rec_id = Qt_rec_id))
	if check_spare:
		if check_spare.SERVICE_DESCRIPTION:
			Log.Info('735------inide spar-----'+str(check_spare.SERVICE_DESCRIPTION))
			serv_desct = ' WITH '+ check_spare.SERVICE_DESCRIPTION
		else:
			serv_desct = ""
	else:
		
		serv_desct = ""
	getserid = Sql.GetFirst("select SERVICE_ID from SAQICO where QUOTE_RECORD_ID = '{Qt_rec_id}'".format(Qt_rec_id = Qt_rec_id))
	if check_spare:
		#Log.Info('735-----------'+str(check_spare.SERVICE_DESCRIPTION))
		getserid = Sql.GetFirst("select SERVICE_ID from SAQICO where QUOTE_RECORD_ID = '{Qt_rec_id}'".format(Qt_rec_id = Qt_rec_id))
		Log.Info('648---CQROLLDOWN---getserid----')
		# getserv_id = Sql.GetList("select SERVICE_ID from SAQITM where QUOTE_RECORD_ID = '{Qt_rec_id}'".format(Qt_rec_id = Qt_rec_id))
		#Log.Info('648---CQROLLDOWN---priciiiiing QT_SAQICO-------')
		# for ser_id in getserv_id:
		# 	Log.Info('648----SERVICE_ID---------QT_SAQICO-------'+str(ser_id.SERVICE_ID))
		# 	check_upsell_ext = Sql.GetFirst("SELECT EXTENDED_PRICE,SERVICE_DESCRIPTION FROM SAQITM  (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND SERVICE_ID LIKE '%- ADDON%'".format(QuoteRecordId=Qt_rec_id))
		# 	check_upsell = Sql.GetFirst("SELECT QUOTE_ITEM_RECORD_ID,EXTENDED_PRICE FROM SAQITM  (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND SERVICE_ID = '{serid}'".format(QuoteRecordId=Qt_rec_id, serid = ser_id.SERVICE_ID))
		# 	if check_upsell:
		# 		Log.Info('742---SERVICE_ID---------QT_SAQICO-------'+str(ser_id.SERVICE_ID))
		# 		quote_tools_obj = Sql.GetFirst("select count(QTEITM_RECORD_ID) as cnt from SAQICO (NOLOCK) where QTEITM_RECORD_ID = '{Quote_item_Record_id}' ".format(Quote_item_Record_id = check_upsell.QUOTE_ITEM_RECORD_ID))
		# 		if quote_tools_obj:
		# 			gettools_count = quote_tools_obj.cnt
		# 			if check_upsell_ext:
		# 				getext_price = check_upsell_ext.EXTENDED_PRICE
		# 				#serv_desct = ' WITH '+ check_upsell_ext.SERVICE_DESCRIPTION
		# 				if gettools_count > 0 and getext_price:
		# 					getdiv = str(float(getext_price/gettools_count)+gettotal_bundle_query.EXTENDED_PRICE)
		# 					Log.Info('24----getdiv---'+str(getdiv))
		# 				else:
		# 					getdiv = 0
		# 			Log.Info(str(Qt_rec_id)+'-747--getdiv--'+str(getext_price)+'---'+str(getdiv)+'---'+str(gettools_count))
				#Log.Info(str(Qt_rec_id)+'--747---getext_price--'+str(getext_price))
	# '''check_upsell = Sql.GetFirst("SELECT QUOTE_ITEM_RECORD_ID,EXTENDED_PRICE FROM SAQITM  (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{} - BASE'".format(self.contract_quote_record_id, self.tree_param))
	# if check_upsell:
	# 	quote_tools_obj = Sql.GetFirst("select count(QTEITM_RECORD_ID) as cnt from SAQICO (NOLOCK) where QTEITM_RECORD_ID = '{Quote_item_Record_id}' ".format(Quote_item_Record_id = check_upsell.QUOTE_ITEM_RECORD_ID))
	# 	if quote_tools_obj:
	# 		gettools_count = quote_tools_obj.cnt
	# 		if check_upsell_ext:
	# 			getext_price = check_upsell_ext.EXTENDED_PRICE
	# 			serv_desct = ' WITH '+ check_upsell_ext.SERVICE_DESCRIPTION'''
	
	#for gettotal_bundle_query in gettotal_bundle_query:
	
	if gettotal_bundle_query:
		
	#	YEAR_1 = YEAR_2 = YEAR_3 = YEAR_4 = YEAR_5 = 
		service_desc = ext_price = ""
		TAX_PER = 0.00
		TAX = 0.00
	#	if gettotal_bundle_query.YEAR_1:
	#		YEAR_1 = gettotal_bundle_query.YEAR_1
	#	else:
	#		YEAR_1 = 0
	#	if gettotal_bundle_query.YEAR_2:
	#		YEAR_2 = gettotal_bundle_query.YEAR_2
	#	else:
	#		YEAR_2 = 0
	#	if gettotal_bundle_query.YEAR_3:
	#		YEAR_3=gettotal_bundle_query.YEAR_3
	#	else:
	#		YEAR_3 = 0
	#	if gettotal_bundle_query.YEAR_4:
	#		YEAR_4=gettotal_bundle_query.YEAR_4
	#	else:
	#		YEAR_4 = 0
	#	if gettotal_bundle_query.YEAR_5:
	#		YEAR_5=gettotal_bundle_query.YEAR_5
	#	else:
	#		YEAR_5 = 0
	#	if gettotal_bundle_query.YEAR_5:
	#		YEAR_5=gettotal_bundle_query.YEAR_5
	#	else:
	#		YEAR_5 = 0
		if gettotal_bundle_query.EXTENDED_PRICE and check_spare:
			ext_pric = getdiv
		else:
			ext_pric = gettotal_bundle_query.EXTENDED_PRICE
		if gettotal_bundle_query.TAX_PER:
			TAX_PER=gettotal_bundle_query.TAX_PER
		if gettotal_bundle_query.TAX:
			TAX=gettotal_bundle_query.TAX
		Log.Info('2655--inside iff--qery-----'+str("""INSERT QT__SAQICO (
						QUOTE_ITEM_COVERED_OBJECT_RECORD_ID, EQUIPMENT_DESCRIPTION, EQUIPMENT_ID, EQUIPMENT_RECORD_ID,
						FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, ITEM_LINE_ID, 
						 QUOTE_ID, QTEITM_RECORD_ID, QUOTE_NAME, QUOTE_RECORD_ID, SALE_PRICE, SERIAL_NO,
						SERVICE_DESCRIPTION, SERVICE_ID,EXTENDED_PRICE, SERVICE_RECORD_ID, TECHNOLOGY, 
						BD_MARGIN,	
						BD_MARGIN_RECORD_ID, CUSTOMER_TOOL_ID,	EQUIPMENTCATEGORY_ID,	
						EQUIPMENTCATEGORY_RECORD_ID, EQUIPMENT_STATUS, MNT_PLANT_ID, MNT_PLANT_NAME,	
						MNT_PLANT_RECORD_ID,	SALE_DISCOUNT, 
						SALES_MARGIN, SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID,
						GREENBOOK, GREENBOOK_RECORD_ID, EQUIPMENT_LINE_ID, SUBTOTAL, TAX,  ownerId, cartId
					) 
					SELECT 
						CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_COVERED_OBJECT_RECORD_ID, 
						SAQICO.EQUIPMENT_DESCRIPTION, 
						SAQICO.EQUIPMENT_ID, 
						SAQICO.EQUIPMENT_RECORD_ID,                     
						SAQICO.FABLOCATION_ID, 
						SAQICO.FABLOCATION_NAME, 
						SAQICO.FABLOCATION_RECORD_ID, 
						SAQICO.LINE, 
						SAQICO.QUOTE_ID, 
						SAQICO.QTEITM_RECORD_ID, 
						SAQICO.QUOTE_NAME, 
						SAQICO.QUOTE_RECORD_ID, 
						SAQICO.SALES_PRICE, 
						SAQICO.SERIAL_NO,
						SAQICO.SERVICE_DESCRIPTION + '{service_desc}' as SERVICE_DESCRIPTION, 
						SAQICO.SERVICE_ID, 
						{ext_price} as EXTENDED_PRICE,
						SAQICO.SERVICE_RECORD_ID,						
						SAQICO.TECHNOLOGY, 
						SAQICO.CUSTOMER_TOOL_ID,	
						SAQICO.EQUIPMENTCATEGORY_ID,	
						SAQICO.EQUIPMENTCATEGORY_RECORD_ID,	
						SAQICO.EQUIPMENT_STATUS,	
						SAQICO.MNT_PLANT_ID,	
						SAQICO.MNT_PLANT_NAME,	
						SAQICO.MNT_PLANT_RECORD_ID,
						'' AS SALES_PRICE_MARGIN,		
						SAQICO.SALESORG_ID,	
						SAQICO.SALESORG_NAME,	
						SAQICO.SALESORG_RECORD_ID,	
						SAQICO.GREENBOOK,	
						SAQICO.GREENBOOK_RECORD_ID,
						SAQICO.EQUIPMENT_LINE_ID,
						SAQICO.EXTENDED_PRICE as SUBTOTAL,				
						{TAX} as TAX,
						{UserId} as ownerId,
						{CartId} as cartId
					FROM SAQICO (NOLOCK) 
					JOIN SAQTSV (NOLOCK) ON SAQTSV.SERVICE_RECORD_ID = SAQICO.SERVICE_RECORD_ID AND SAQTSV.QUOTE_RECORD_ID = SAQICO.QUOTE_RECORD_ID                
					WHERE SAQICO.QUOTE_RECORD_ID='{QuoteRecordId}' and SAQICO.SERVICE_ID='{Service_id}' """.format(
					CartId=cart_id,
					UserId=cart_user_id,
					QuoteRecordId=Qt_rec_id,
					Service_id =getserid.SERVICE_ID,TAX=TAX,service_desc=service_desc,ext_price=ext_pric,
							)))
		Sql.RunQuery("""INSERT QT__SAQICO (
						QUOTE_ITEM_COVERED_OBJECT_RECORD_ID, EQUIPMENT_DESCRIPTION, EQUIPMENT_ID, EQUIPMENT_RECORD_ID,
						FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, ITEM_LINE_ID,  QUOTE_ID, QTEITM_RECORD_ID, QUOTE_NAME, QUOTE_RECORD_ID, SALE_PRICE, SERIAL_NO,
						SERVICE_DESCRIPTION, SERVICE_ID,EXTENDED_PRICE, SERVICE_RECORD_ID, TECHNOLOGY, 
						CUSTOMER_TOOL_ID,	EQUIPMENTCATEGORY_ID,	
						EQUIPMENTCATEGORY_RECORD_ID, EQUIPMENT_STATUS, MNT_PLANT_ID, MNT_PLANT_NAME,	
						MNT_PLANT_RECORD_ID,	SALE_DISCOUNT, 
						SALES_MARGIN, SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID,
						GREENBOOK, GREENBOOK_RECORD_ID, EQUIPMENT_LINE_ID, SUBTOTAL, TAX,  ownerId, cartId
					) 
					SELECT 
						CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_COVERED_OBJECT_RECORD_ID,
						SAQICO.EQUIPMENT_DESCRIPTION, 
						SAQICO.EQUIPMENT_ID, 
						SAQICO.EQUIPMENT_RECORD_ID,                     
						SAQICO.FABLOCATION_ID, 
						SAQICO.FABLOCATION_NAME, 
						SAQICO.FABLOCATION_RECORD_ID, 
						SAQICO.LINE, 
						SAQICO.QUOTE_ID, 
						SAQICO.QTEITM_RECORD_ID, 
						SAQICO.QUOTE_NAME, 
						SAQICO.QUOTE_RECORD_ID, 
						SAQICO.SALES_PRICE, 
						SAQICO.SERIAL_NO,
						SAQICO.SERVICE_DESCRIPTION + '{service_desc}' as SERVICE_DESCRIPTION, 
						SAQICO.SERVICE_ID, 
						{ext_price} as EXTENDED_PRICE,
						SAQICO.SERVICE_RECORD_ID,						
						SAQICO.TECHNOLOGY,	
						SAQICO.CUSTOMER_TOOL_ID,	
						SAQICO.EQUIPMENTCATEGORY_ID,	
						SAQICO.EQUIPMENTCATEGORY_RECORD_ID,	
						SAQICO.EQUIPMENT_STATUS,
						SAQICO.MNT_PLANT_ID,	
						SAQICO.MNT_PLANT_NAME,	
						SAQICO.MNT_PLANT_RECORD_ID,
						'' AS SALES_PRICE_MARGIN,	
						SAQICO.SALESORG_ID,	
						SAQICO.SALESORG_NAME,	
						SAQICO.SALESORG_RECORD_ID,	
						SAQICO.GREENBOOK,	
						SAQICO.GREENBOOK_RECORD_ID,
						SAQICO.EQUIPMENT_LINE_ID,
						SAQICO.EXTENDED_PRICE as SUBTOTAL,					
						{TAX} as TAX,
						{UserId} as ownerId,
						{CartId} as cartId
					FROM SAQICO (NOLOCK) 
					JOIN SAQTSV (NOLOCK) ON SAQTSV.SERVICE_RECORD_ID = SAQICO.SERVICE_RECORD_ID AND SAQTSV.QUOTE_RECORD_ID = SAQICO.QUOTE_RECORD_ID                
					WHERE SAQICO.QUOTE_RECORD_ID='{QuoteRecordId}' and SAQICO.SERVICE_ID='{Service_id}' """.format(
					CartId=cart_id,
					UserId=cart_user_id,
					QuoteRecordId=Qt_rec_id,
					Service_id =getserid.SERVICE_ID,TAX=TAX,service_desc=serv_desct,ext_price=ext_pric
							))
	else:      
		quote_item_covered_obj_insert = """INSERT QT__SAQICO (
						QUOTE_ITEM_COVERED_OBJECT_RECORD_ID, EQUIPMENT_DESCRIPTION, EQUIPMENT_ID, EQUIPMENT_RECORD_ID,
						FABLOCATION_ID, FABLOCATION_NAME, FABLOCATION_RECORD_ID, ITEM_LINE_ID, QUOTE_ID, QTEITM_RECORD_ID, QUOTE_NAME, QUOTE_RECORD_ID, SALE_PRICE, SERIAL_NO,
						SERVICE_DESCRIPTION, SERVICE_ID,EXTENDED_PRICE, SERVICE_RECORD_ID, TECHNOLOGY, CUSTOMER_TOOL_ID,	EQUIPMENTCATEGORY_ID,	
						EQUIPMENTCATEGORY_RECORD_ID, EQUIPMENT_STATUS, MNT_PLANT_ID, MNT_PLANT_NAME,	
						MNT_PLANT_RECORD_ID,	SALE_DISCOUNT, 
						SALES_MARGIN, SALESORG_ID, SALESORG_NAME, SALESORG_RECORD_ID, 
						GREENBOOK, GREENBOOK_RECORD_ID, EQUIPMENT_LINE_ID, SUBTOTAL, ownerId, cartId
					) 
					SELECT 
						CONVERT(VARCHAR(4000),NEWID()) as QUOTE_ITEM_COVERED_OBJECT_RECORD_ID,
						SAQICO.EQUIPMENT_DESCRIPTION, 
						SAQICO.EQUIPMENT_ID, 
						SAQICO.EQUIPMENT_RECORD_ID,                     
						SAQICO.FABLOCATION_ID, 
						SAQICO.FABLOCATION_NAME, 
						SAQICO.FABLOCATION_RECORD_ID, 
						SAQICO.LINE_ITEM_ID, 
						SAQICO.QUOTE_ID, 
						SAQICO.QTEITM_RECORD_ID, 
						SAQICO.QUOTE_NAME, 
						SAQICO.QUOTE_RECORD_ID, 
						SAQICO.SALES_PRICE, 
						SAQICO.SERIAL_NO,
						SAQICO.SERVICE_DESCRIPTION, 
						SAQICO.SERVICE_ID, 
						SAQICO.EXTENDED_PRICE,
						SAQICO.SERVICE_RECORD_ID,					
						SAQICO.TECHNOLOGY, 		
						SAQICO.CUSTOMER_TOOL_ID,	
						SAQICO.EQUIPMENTCATEGORY_ID,	
						SAQICO.EQUIPMENTCATEGORY_RECORD_ID,	
						SAQICO.EQUIPMENT_STATUS,
						SAQICO.MNT_PLANT_ID,	
						SAQICO.MNT_PLANT_NAME,	
						SAQICO.MNT_PLANT_RECORD_ID,
						'' AS SALES_PRICE_MARGIN,	
						SAQICO.SALESORG_ID,	
						SAQICO.SALESORG_NAME,	
						SAQICO.SALESORG_RECORD_ID,	
						SAQICO.GREENBOOK,	
						SAQICO.GREENBOOK_RECORD_ID,
						SAQICO.EQUIPMENT_LINE_ID,
						SAQICO.EXTENDED_PRICE as SUBTOTAL,					
						{UserId} as ownerId,
						{CartId} as cartId
					FROM SAQICO (NOLOCK) 
					JOIN SAQTSV (NOLOCK) ON SAQTSV.SERVICE_RECORD_ID = SAQICO.SERVICE_RECORD_ID AND SAQTSV.QUOTE_RECORD_ID = SAQICO.QUOTE_RECORD_ID                
					WHERE SAQICO.QUOTE_RECORD_ID='{QuoteRecordId}' """.format(
					CartId=cart_id,
					UserId=cart_user_id,
					QuoteRecordId=Qt_rec_id
				)
		Log.Info('426-------QT__SAQICO--------------'+str(quote_item_covered_obj_insert))
		Sql.RunQuery(quote_item_covered_obj_insert)
	
	#update QT_SAQITM
	# updateafterreprice = """DELETE QT__SAQITM FROM QT__SAQITM 
	# 							JOIN SAQTSV (NOLOCK) ON SAQTSV.SERVICE_RECORD_ID = QT__SAQITM.SERVICE_RECORD_ID AND SAQTSV.QUOTE_RECORD_ID = QT__SAQITM.QUOTE_RECORD_ID  
	# 							WHERE QT__SAQITM.cartId = '{CartId}' AND ownerId = {UserId} AND QT__SAQITM.QUOTE_RECORD_ID = '{QuoteRecordId}'""".format(
	# 							CartId=cart_id, UserId=cart_user_id, QuoteRecordId=Qt_rec_id,)
	# Sql.RunQuery(updateafterreprice)
	Log.Info('532---QT_SAQITM---')
	# innerselect = """SELECT 
	# 				SAQITM.EXTENDED_PRICE as UNIT_PRICE,
	# 				{UserId} as ownerId,
	# 				{CartId} as cartId
	# 			FROM SAQITM (NOLOCK) 
	# 			JOIN SAQTSV (NOLOCK) ON SAQTSV.SERVICE_RECORD_ID = SAQITM.SERVICE_RECORD_ID AND SAQTSV.QUOTE_RECORD_ID = SAQITM.QUOTE_RECORD_ID                
	# 			WHERE SAQITM.QUOTE_RECORD_ID='{QuoteRecordId}' """.format(
	# 				CartId=cart_id, UserId=cart_user_id, QuoteRecordId=Qt_rec_id,)
	#Log.Info('532---QT_SAQITM--innerselect----'+str(innerselect))
	#update based on bundle after reprice
	# bundledes = bundleser = ""
	# Bundle_Query_val = Sql.GetList("SELECT SERVICE_ID,SERVICE_DESCRIPTION FROM SAQSAO (NOLOCK) WHERE QUOTE_RECORD_ID='{QuoteRecordId}'".format(QuoteRecordId=Qt_rec_id))
	# if Bundle_Query_val:
	# 	#Log.Info('532-CQROLLDOWN-----QT_SAQITM--insertitm---inside if')
	# 	for Bundle_Query in Bundle_Query_val:
	# 		if Bundle_Query.SERVICE_ID:
	# 			Log.Info('532-CQROLLDOWN-----QT_SAQITM--insertitm---inside if'+str(Bundle_Query.SERVICE_ID))
	# 			bundleser = Bundle_Query.SERVICE_ID + " - BUNDLE"
	# 			Bundle_Query_addon = Sql.GetFirst("SELECT ADNPRD_ID,ADNPRD_DESCRIPTION FROM SAQSAO (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}'".format(Qt_rec_id, Bundle_Query.SERVICE_ID))
	# 			if Bundle_Query_addon:
	# 				if Bundle_Query_addon.ADNPRD_DESCRIPTION:
	# 					bundledes =Bundle_Query.SERVICE_DESCRIPTION+ " WITH " + Bundle_Query_addon.ADNPRD_DESCRIPTION
	# 				else:
	# 					bundledes =Bundle_Query.SERVICE_DESCRIPTION
	# 			else:
	# 				bundledes = Bundle_Query.SERVICE_DESCRIPTION
	# 			Log.Info(str(bundledes)+'---bundledes----532-CQROLLDOWN-----bundleser---inside if'+str(bundleser))
	# 			insertitm = """INSERT QT__SAQITM (
	# 				ITEM_LINE_ID, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, QTY_OF_TOOLS, CURRENCY, UNIT_PRICE, EXTENDED_UNIT_PRICE,
	# 				QUANTITY, FORECAST_VALUE, ONSITE_PURCHASE_COMMIT, QUOTE_ID, QUOTE_RECORD_ID, YEAR_1, YEAR_2, YEAR_3, YEAR_4, YEAR_5, TAX_PERCENTAGE, TAX,  ownerId, cartId
	# 			) 
	# 			SELECT 
	# 				SAQITM.LINE_ITEM_ID as ITEM_LINE_ID,
	# 				'{bundledescription}'  as SERVICE_DESCRIPTION,
	# 				REPLACE(SAQITM.SERVICE_ID , '- BUNDLE', '') as SERVICE_ID,
	# 				SAQITM.SERVICE_RECORD_ID,					
	# 				10 AS QTY_OF_TOOLS,
	# 				SAQITM.CURRENCY,
	# 				SAQITM.SALES_PRICE as UNIT_PRICE,
	# 				SAQITM.EXTENDED_PRICE as EXTENDED_UNIT_PRICE,
	# 				SAQITM.OBJECT_QUANTITY,
	# 				10 AS FORECAST_VALUE,
	# 				SAQITM.ONSITE_PURCHASE_COMMIT,
	# 				SAQITM.QUOTE_ID,
	# 				SAQITM.QUOTE_RECORD_ID,
	# 				ISNULL(SAQITM.YEAR_1, 0) as YEAR_1,                        
	# 				ISNULL(SAQITM.YEAR_2, 0) as YEAR_2,                        
	# 				ISNULL(SAQITM.YEAR_3, 0) as YEAR_3,                        
	# 				ISNULL(SAQITM.YEAR_4, 0) as YEAR_4,                        
	# 				ISNULL(SAQITM.YEAR_5, 0) as YEAR_5,
	# 				SAQITM.TAX_PERCENTAGE,
	# 				SAQITM.TAX,
	# 				{UserId} as ownerId,
	# 				{CartId} as cartId
	# 			FROM SAQITM (NOLOCK) 
	# 			JOIN SAQTSV (NOLOCK) ON SAQTSV.SERVICE_RECORD_ID = SAQITM.SERVICE_RECORD_ID AND SAQTSV.QUOTE_RECORD_ID = SAQITM.QUOTE_RECORD_ID                
	# 			WHERE SAQITM.QUOTE_RECORD_ID='{QuoteRecordId}' AND SAQITM.SERVICE_ID = '{ServiceId}' """.format(
	# 					CartId=cart_id, UserId=cart_user_id, QuoteRecordId=Qt_rec_id,
	# 					ServiceId=bundleser,bundledescription = bundledes,)
	# else:		
	# 	insertitm = """INSERT QT__SAQITM (
	# 					ITEM_LINE_ID, SERVICE_DESCRIPTION, SERVICE_ID, SERVICE_RECORD_ID, QTY_OF_TOOLS, CURRENCY, UNIT_PRICE, EXTENDED_UNIT_PRICE,
	# 					QUANTITY, FORECAST_VALUE, ONSITE_PURCHASE_COMMIT, QUOTE_ID, QUOTE_RECORD_ID, YEAR_1, YEAR_2, YEAR_3, YEAR_4, YEAR_5, TAX_PERCENTAGE, TAX,  ownerId, cartId
	# 				) 
	# 				SELECT 
	# 					SAQITM.LINE_ITEM_ID as ITEM_LINE_ID,
	# 					SAQITM.SERVICE_DESCRIPTION,
	# 					SAQITM.SERVICE_ID,
	# 					SAQITM.SERVICE_RECORD_ID,					
	# 					10 AS QTY_OF_TOOLS,
	# 					SAQITM.CURRENCY,
	# 					SAQITM.SALES_PRICE as UNIT_PRICE,
	# 					SAQITM.EXTENDED_PRICE as EXTENDED_UNIT_PRICE,
	# 					SAQITM.OBJECT_QUANTITY,
	# 					10 AS FORECAST_VALUE,
	# 					SAQITM.ONSITE_PURCHASE_COMMIT,
	# 					SAQITM.QUOTE_ID,
	# 					SAQITM.QUOTE_RECORD_ID,
	# 					ISNULL(SAQITM.YEAR_1, 0) as YEAR_1,                        
	# 					ISNULL(SAQITM.YEAR_2, 0) as YEAR_2,                        
	# 					ISNULL(SAQITM.YEAR_3, 0) as YEAR_3,                        
	# 					ISNULL(SAQITM.YEAR_4, 0) as YEAR_4,                        
	# 					ISNULL(SAQITM.YEAR_5, 0) as YEAR_5,
	# 					SAQITM.TAX_PERCENTAGE,
	# 					SAQITM.TAX,
	# 					{UserId} as ownerId,
	# 					{CartId} as cartId
	# 				FROM SAQITM (NOLOCK) 
	# 				JOIN SAQTSV (NOLOCK) ON SAQTSV.SERVICE_RECORD_ID = SAQITM.SERVICE_RECORD_ID AND SAQTSV.QUOTE_RECORD_ID = SAQITM.QUOTE_RECORD_ID                
	# 				WHERE SAQITM.QUOTE_RECORD_ID='{QuoteRecordId}'  """.format(
	# 					CartId=cart_id, UserId=cart_user_id, QuoteRecordId=Qt_rec_id,)
	# Log.Info('532-CQROLLDOWN-----QT_SAQITM--insertitm-'+str(insertitm))
	# Sql.RunQuery(insertitm)

#Log.Info("Qt_rec_id ->"+str(Param.CPQ_Columns['Quote']))
Qt_rec_id = Param.CPQ_Columns['Quote']
Log.Info("Qt_rec_id ->"+str(Qt_rec_id))
LEVEL = Param.CPQ_Columns['Level']
Log.Info("LEVEL ->"+str(LEVEL))
# try:
# 	anc =Param.Quote.split("==")[1]
# except Exception as e:
# 	Log.Info("anc--"+str(e))
try:
	ancillary_dict = Param.CPQ_Columns['Ancillary_dict']
	ancillary_dict = eval(str(ancillary_dict.replace(';39;',"'").replace('_;',"{").replace("$;","}").replace("=",":")))
except Exception as e:
	Log.Info("ancillary_dict-1269---"+str(e))
	ancillary_dict = {}
Log.Info("ancillary_dict--1271--"+str(ancillary_dict))


if 'COV OBJ ENTITLEMENT' in LEVEL:
	a = LEVEL.split(",")
	TreeParam = a[1]
	TreeParentParam = a[2]
	try:
		userId = a[3]
	except:
		pass
	rev_rec_id = a[4]
	Log.Info("tree----"+str(TreeParam))
	ApiResponse = ApiResponseFactory.JsonResponse(CoveredObjEntitlement())
elif 'COV OBJ ITEM' in LEVEL:
	a = LEVEL.split(",")
	TreeParam = a[1]
	TreeParentParam = a[2]
	#Log.Info("tree----"+str(TreeParam))
	ApiResponse = ApiResponseFactory.JsonResponse(CoveredObjItemEntitlement())
elif 'COV OBJ RENEWAL ONE' in LEVEL:    
	'''a = LEVEL.split("=")
	c = a[1]
	configuration = c.split(",")
	p = a[2]
	ProductPart = p.split(",")
	ContractRecordId = a[3]
	attributeList = []
	attributevalueList = []'''
	a = LEVEL.split("=")
	p = a[1]
	ProductPart = p.split(",")
	ContractRecordId = a[2]
	rev_rec_id = a[3]
	#Log.Info("config----"+str(configuration))
	#Log.Info("service----"+str(ProductPart))
	ApiResponse = ApiResponseFactory.JsonResponse(covobjrenewal())
elif 'COV OBJ RENEWAL TWO' in LEVEL:
	a = LEVEL.split("=")
	c = a[1]
	configuration = c.split(",")
	p = a[2]
	ProductPart = p.split(",")
	ContractRecordId = a[3]
	#Log.Info("tree----"+str(TreeParam))
	ApiResponse = ApiResponseFactory.JsonResponse(covobjrenewal_two())
elif 'SPARE PART ITEM' in LEVEL:
	a = LEVEL.split(",")
	TreeParam = a[1]
	batch_group_record_id = a[2]
	userId = a[3]
	userName = a[4]
	Log.Info("===FAB LEVEL----"+str(TreeParam))
	ApiResponse = ApiResponseFactory.JsonResponse(SparepartsItem())
elif 'QT_SAQICO LEVEL' in LEVEL:
	quote_obj = Sql.GetFirst("select C4C_QUOTE_ID from SAQTMT where MASTER_TABLE_QUOTE_RECORD_ID = '{}'".format(Qt_rec_id))	
	external_id = quote_obj.C4C_QUOTE_ID
	cart_obj = SqlHelper.GetFirst("Select CART_ID,USERID from CART where ExternalId = '{}'".format(external_id))
	cart_id = cart_obj.CART_ID
	cart_user_id = cart_obj.USERID
	ApiResponse = ApiResponseFactory.JsonResponse(quote_SAQICOupdate(cart_id,cart_user_id))    

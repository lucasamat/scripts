# =========================================================================================================================================
#   __script_name : SYMCMODPRD.PY
#   __script_description : THIS SCRIPT IS USED TO DEPLOY OR REFRESH MODULES/APPS IN SYSTEM ADMIN
#   __primary_author__ : LEO JOSEPH
#   __create_date :
#   Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct
import SYTABACTIN as Table
from SYDATABASE import SQL

Sql = SQL()
user = User.Id
##BUILD TABS
ATTRIBUTES = ""
PartNumber = ""
# A043S001P01-11792 -Dhurga Start
# tabVisibilityCondition = '''<![CDATA[[AND]([NOT]([EQ](<*Value(MA_MTR_ACTIVE_TAB)*>,{0})),[EQ](<*TABLE(SELECT TOP 1 TB.VISIBLE FROM SYTABS (NOLOCK) MM INNER JOIN SYPRTB (NOLOCK) TB ON TB.TAB_RECORD_ID = MM.RECORD_ID INNER JOIN SYPRUS (NOLOCK) US  ON US.PROFILE_RECORD_ID = TB.PROFILE_RECORD_ID WHERE TB.APP_ID = '{1}'  AND US.USER_RECORD_ID = '<*CTX(Visitor.Id)*>' AND TB.VISIBLE = 1 AND TB.TAB_ID ='{2}')*>,True))]]>'''
# tabVisibilityCondition = '''<![CDATA[[AND]([NOT]([EQ](<*Value(MA_MTR_ACTIVE_TAB)*>,{0})),[EQ](<*TABLE(SELECT TOP 1 TB.VISIBLE FROM SYTABS (NOLOCK) MM INNER JOIN SYPRTB (NOLOCK) TB ON TB.TAB_RECORD_ID = MM.RECORD_ID INNER JOIN users_permissions (NOLOCK) US  ON US.permission_id = TB.PROFILE_RECORD_ID WHERE TB.APP_ID = '{1}'  AND US.user_id = "+str(user)+" AND TB.VISIBLE = 1 AND TB.TAB_ID ='{2}')*>,True))]]>'''


#tabVisibilityCondition = """<![CDATA[[AND]([NOT]([EQ](<*Value(MA_MTR_ACTIVE_TAB)*>,{0})),[EQ](<*TABLE(SELECT TOP 1 TB.VISIBLE,up.user_id FROM SYTABS (NOLOCK) MM INNER JOIN SYPRTB (NOLOCK) TB ON TB.TAB_RECORD_ID = MM.RECORD_ID  INNER JOIN cpq_permissions (NOLOCK) US ON US.permission_id = TB.PROFILE_RECORD_ID INNER JOIN users_permissions (NOLOCK) up on up.permission_id = US.permission_id WHERE TB.APP_ID = '{1}' AND US.permission_type = '0' AND up.user_id = '<*CTX(Visitor.Id)*>' AND TB.VISIBLE = 1 AND TB.TAB_ID ='{2}')*>,True))]]>"""

#tabVisibilityConditionSA = """<![CDATA[[AND]([NOT]([EQ](<*Value(MA_MTR_ACTIVE_TAB)*>,{0})),[EQ](<*TABLE(SELECT TOP 1 TB.VISIBLE,up.user_id FROM SYTABS (NOLOCK) MM INNER JOIN SYPRTB (NOLOCK) TB ON TB.TAB_RECORD_ID = MM.RECORD_ID  INNER JOIN cpq_permissions (NOLOCK) US ON US.permission_id = TB.PROFILE_RECORD_ID INNER JOIN users_permissions (NOLOCK) up on up.permission_id = US.permission_id inner join USERS (NOLOCK) U ON U.ID = UP.user_id WHERE TB.APP_ID = '{1}' AND US.permission_type = '0' AND up.user_id = '<*CTX(Visitor.Id)*>' AND TB.VISIBLE = 1 AND U.COMPANYID = '29' AND TB.TAB_ID ='{2}')*>,True))]]>"""

#check tab level permissions
#tabVisibilityCondition = """<![CDATA[[EQ](<*Value(MA_MTR_ACTIVE_TAB)*>,{0})]]>"""


tabVisibilityCondition = """<![CDATA[[AND]([NOT]([EQ](<*Value(MA_MTR_ACTIVE_TAB)*>,{0})),[EQ](<*TABLE(SELECT TOP 1 TB.VISIBLE,up.user_id FROM SYTABS (NOLOCK) MM INNER JOIN SYPRTB (NOLOCK) TB ON TB.TAB_RECORD_ID = MM.RECORD_ID  INNER JOIN cpq_permissions (NOLOCK) US ON US.permission_id = TB.PROFILE_RECORD_ID INNER JOIN users_permissions (NOLOCK) up on up.permission_id = US.permission_id WHERE TB.APP_ID = '{1}' AND US.permission_type = '0' AND up.user_id = '<*CTX(Visitor.Id)*>' AND TB.VISIBLE = 1 AND TB.TAB_ID ='{2}')*>,True))]]>"""
tabVisibilityConditionSA = """<![CDATA[[AND]([NOT]([EQ](<*Value(MA_MTR_ACTIVE_TAB)*>,{0})),[EQ](<*TABLE(SELECT TOP 1 TB.VISIBLE,up.user_id FROM SYTABS (NOLOCK) MM INNER JOIN SYPRTB (NOLOCK) TB ON TB.TAB_RECORD_ID = MM.RECORD_ID  INNER JOIN cpq_permissions (NOLOCK) US ON US.permission_id = TB.PROFILE_RECORD_ID INNER JOIN users_permissions (NOLOCK) up on up.permission_id = US.permission_id inner join USERS (NOLOCK) U ON U.ID = UP.user_id WHERE TB.APP_ID = '{1}' AND US.permission_type = '0' AND up.user_id = '<*CTX(Visitor.Id)*>' AND TB.VISIBLE = 1  AND TB.TAB_ID ='{2}')*>,True))]]>"""
#tabVisibilityConditionSA = """<![CDATA[[NOT]([EQ](<*Value(MA_MTR_ACTIVE_TAB)*>,{0}))]]>"""


#tabVisibilityCondition = """<![CDATA[[AND]([NOT]([EQ](<*Value(MA_MTR_ACTIVE_TAB)*>,{0})),[EQ](<*TABLE(SELECT TOP 1 * FROM SYTABS (NOLOCK)  WHERE APP_LABEL = '{1}'  AND TAB_NAME ='{2}')*>,True))]]>"""
# A043S001P01-11792 -Dhurga End

userId = str(User.Id)


def BuildAPIXMLBody(RecordNo, Login_Domain):
Tabrank = 10
# Decalre Varaibles
tabslist = ""
Sections = ""
SBSect_banner = ""
TABAttri = ""
Attr_Type = ""
TABNANES = ""
Attr_Disptype = ""
CustomTable = []
APIdata = ""
RecordNoApp = ""
# Get Module inforamtion
ModuleRecord = Sql.GetFirst(
	"select APP_RECORD_ID,APP_LABEL,APP_ID,APP_NAME FROM SYAPPS (NOLOCK) where APP_RECORD_ID='" + str(RecordNo) + "'"
)
if ModuleRecord is not None:
	CPQProductID = str(ModuleRecord.APP_LABEL).replace(" ", "_")
	PartNumber = str(ModuleRecord.APP_ID)
	Categories = "MODULE"
	ProductName = str(ModuleRecord.APP_LABEL)
	RecordNoApp = str(ModuleRecord.APP_RECORD_ID)
	CommmonAttribute = "<Attribute><AttributeName><USEnglish>BTN_MA_ALL_REFRESH</USEnglish></AttributeName><AttributeType>UserSelection</AttributeType><AttachScriptButton>1</AttachScriptButton><ButtonScripts><ButtonScript><Name>SYGETVRCTX</Name><Rank>1</Rank></ButtonScript><ButtonScript><Name>SYLDRLADBN</Name><Rank>1</Rank></ButtonScript></ButtonScripts><DisplayType>Button</DisplayType><ButtonText><USEnglish>REFRESH</USEnglish></ButtonText><IsFirstValuePreselected>0</IsFirstValuePreselected><Values><Value><USEnglish>att</USEnglish><Rank>10</Rank><ValueCode>1</ValueCode></Value></Values></Attribute><Attribute><AttributeName><USEnglish>SEARCH_FILTER_BTN</USEnglish></AttributeName><AttributeType>UserSelection</AttributeType><DisplayType>Button</DisplayType><ButtonText><USEnglish>SEARCH</USEnglish></ButtonText><IsFirstValuePreselected>0</IsFirstValuePreselected><Values><Value><USEnglish>att</USEnglish><Rank>10</Rank><ValueCode>1</ValueCode></Value></Values></Attribute>"

	NewCommmonAttribute = "<Attribute><AttributeName><USEnglish>MA_MTR_ACTIVE_TAB</USEnglish></AttributeName><AttributeType>UserSelection</AttributeType><DisplayType>FreeInputNoMatching</DisplayType><SpansAcrossEntireRow>1</SpansAcrossEntireRow><Label><USEnglish>Active Tab</USEnglish></Label><Hint><USEnglish>Active Tab</USEnglish></Hint><ShowOneTimePrice>0</ShowOneTimePrice><IsFirstValuePreselected>0</IsFirstValuePreselected><Values><Value><USEnglish>att</USEnglish><Rank>10</Rank><ValueCode>1</ValueCode></Value></Values></Attribute><Attribute><AttributeName><USEnglish>MA_MTR_TAB_ACTION</USEnglish></AttributeName><AttributeType>UserSelection</AttributeType><DisplayType>FreeInputNoMatching</DisplayType><SpansAcrossEntireRow>1</SpansAcrossEntireRow><Label><USEnglish>Action</USEnglish></Label><Hint><USEnglish>Action</USEnglish></Hint><ShowOneTimePrice>0</ShowOneTimePrice><IsFirstValuePreselected>0</IsFirstValuePreselected><Values><Value><USEnglish>att</USEnglish><Rank>10</Rank><ValueCode>1</ValueCode></Value></Values></Attribute><Attribute><AttributeName><USEnglish>SEC_N_TAB_PAGE_ALERT</USEnglish></AttributeName><AttributeType>UserSelection</AttributeType><DisplayType>FreeInputNoMatching</DisplayType><SpansAcrossEntireRow>1</SpansAcrossEntireRow><Label><USEnglish>TAB PAGE ALERT</USEnglish></Label><Hint><USEnglish>TAB PAGE ALERT</USEnglish></Hint><ShowOneTimePrice>0</ShowOneTimePrice><IsFirstValuePreselected>0</IsFirstValuePreselected><Values><Value><USEnglish>att</USEnglish><Rank>10</Rank><ValueCode>1</ValueCode></Value></Values></Attribute>"
	if PartNumber=="QT":
		NewCommmonAttribute=NewCommmonAttribute+"<Attribute><AttributeName><USEnglish>Services</USEnglish></AttributeName><AttributeType>Container</AttributeType><DisplayType>Container</DisplayType><SpansAcrossEntireRow>1</SpansAcrossEntireRow><Label><USEnglish>Services</USEnglish></Label><Hint><USEnglish>Services</USEnglish></Hint><ShowOneTimePrice>0</ShowOneTimePrice><IsFirstValuePreselected>0</IsFirstValuePreselected><Values><Value><USEnglish>1</USEnglish><Rank>10</Rank><ValueCode>1</ValueCode></Value></Values></Attribute>"
	global ATTRIBUTES
	ATTRIBUTES = CommmonAttribute + NewCommmonAttribute
	# Build Tabs
	TabListXML = ""
	TabRecords = Sql.GetList(
		"select top 1000 RECORD_ID,SAPCPQ_ATTRIBUTE_NAME,TAB_LABEL,DISPLAY_ORDER,TAB_TYPE,SAPCPQ_ALTTAB_NAME FROM SYTABS (NOLOCK) where APP_RECORD_ID='"
		+ str(RecordNoApp)
		+ "' ORDER BY abs(DISPLAY_ORDER)"
	)

	Allcount = 0
	pivotRank = 700
	for item in TabRecords:
		Tabrank = Tabrank + 10
		pivotRank = pivotRank + 1000
		TabId = str(item.SAPCPQ_ALTTAB_NAME).replace(" ", "_") + "_cpq"
		TabFullName = str(item.TAB_LABEL)
		#TabName = str(item.TAB_LABEL)
		TabName = str(item.SAPCPQ_ALTTAB_NAME)
		TabRecordNo = str(item.RECORD_ID)
		ListTabXML = BuildListTabAttributes(TabRecordNo, TabFullName, TabName, Tabrank)
		TabXML = BuildTabAttributes(TabId, TabName, TabRecordNo, Tabrank, pivotRank, TabFullName)
		TabListXML = TabListXML + ListTabXML + TabXML
	# Product Data Detailes (For Name,Tabs,Attributes)
	APIdata = (
		"<?xml version='1.0' encoding='utf-8'?><Products><Product><CPQProductID>"
		+ str(CPQProductID)
		+ "</CPQProductID><PartNumber>"
		+ str(PartNumber)
		+ "</PartNumber><DisplayType>Configurable</DisplayType>"
	)  # A043S001P01-13457 Start
	APIdata += (
		"<Active>"
		+ "true"
		+ "</Active><ProductType>"
		+ "MODULE"
		+ "</ProductType><ProductName><USEnglish>"
		+ str(ProductName)
		+ "</USEnglish></ProductName><Categories><USEnglish>"
		+ str(Categories)
		+ "</USEnglish></Categories><ResponderAttributes></ResponderAttributes><ResponderLineItems></ResponderLineItems><GlobalScripts><Script><Name>MATABACTVE</Name><Rank>10</Rank><Events><Event>OnProductTabChanged</Event></Events></Script><Script><Name>SYLDRLADBN</Name><Rank>10</Rank><Events><Event>OnProductRuleExecutionEnd</Event></Events></Script><Script><Name>SYSRTREXEC</Name><Rank>10</Rank><Events><Event>OnProductLoaded</Event></Events></Script><Script><Name>SYGETVRCTX</Name><Rank>10</Rank><Events><Event>OnProductRuleExecutionEnd</Event></Events></Script><Script><Name>SYRLEXEEND</Name><Rank>10</Rank><Events><Event>OnProductRuleExecutionEnd</Event></Events></Script>"
	)
	
	APIdata += "</GlobalScripts>"
	# A043S001P01-13457 End
	try:
		APIdata += "<Attributes>" + ATTRIBUTES + "</Attributes><Tabs>" + TabListXML + "</Tabs></Product></Products>"
	except:
		APIdata += (
			"<Attributes>" + str(ATTRIBUTES) + "</Attributes><Tabs>" + str(TabListXML) + "</Tabs></Product></Products>"
		)
return APIdata


# Build Tab Banner Controls
def BuildListTabAttributes(TabRecordNo, TabFullName, TabName, Tabrank):
TABAttributes = ""
global ATTRIBUTES
tabslist = ""
if str(TabFullName) == "Pricebook Sets":
	ATTRIBUTES += '<Attribute><AttributeName><USEnglish>QSTN_PRLPBS_TREEVIEW</USEnglish></AttributeName><AttributeType>String</AttributeType><DisplayType>DisplayOnlyText</DisplayType><SpansAcrossEntireRow>1</SpansAcrossEntireRow><Label><USEnglish></USEnglish></Label><Hint><USEnglish><![CDATA[<div id="prlpbs_treeGrid"></div><script type="text/javascript">$(document).ready(function(){PRLPBSTreeTable();});</script>]]></USEnglish></Hint><ShowOneTimePrice>0</ShowOneTimePrice><IsFirstValuePreselected>0</IsFirstValuePreselected><Values><Value><USEnglish>1</USEnglish></Value></Values></Attribute>'
	TABAttributes += "<Attribute><Name>QSTN_PRLPBS_TREEVIEW</Name><Rank>" + "7" + "</Rank></Attribute>"

if str(TabFullName) == "Price Model Classes":
	ATTRIBUTES += '<Attribute><AttributeName><USEnglish>QSTN_PRIMODCL_TREEVIEW</USEnglish></AttributeName><AttributeType>String</AttributeType><DisplayType>DisplayOnlyText</DisplayType><SpansAcrossEntireRow>1</SpansAcrossEntireRow><Label><USEnglish></USEnglish></Label><Hint><USEnglish><![CDATA[<div id="pricModClsTreeTable" class="pad_top64"></div><script>$(document).ready(function(){pricModClsTreeTable();});</script>]]></USEnglish></Hint><ShowOneTimePrice>0</ShowOneTimePrice><IsFirstValuePreselected>0</IsFirstValuePreselected><Values><Value><USEnglish>1</USEnglish></Value></Values></Attribute>'
	TABAttributes += "<Attribute><Name>QSTN_PRIMODCL_TREEVIEW</Name><Rank>" + "7" + "</Rank></Attribute>"

if str(TabFullName) == "Categories":
	ATTRIBUTES += '<Attribute><AttributeName><USEnglish>QSTN_CAT_TREEVIEW</USEnglish></AttributeName><AttributeType>String</AttributeType><DisplayType>DisplayOnlyText</DisplayType><SpansAcrossEntireRow>1</SpansAcrossEntireRow><Label><USEnglish></USEnglish></Label><Hint><USEnglish><![CDATA[<div id="catTreeTable"></div><script type="text/javascript">$( document ).ready(function() { catTreeTable()}); </script>]]></USEnglish></Hint><ShowOneTimePrice>0</ShowOneTimePrice><IsFirstValuePreselected>0</IsFirstValuePreselected><Values><Value><USEnglish>1</USEnglish></Value></Values></Attribute>'
	TABAttributes += "<Attribute><Name>QSTN_CAT_TREEVIEW</Name><Rank>" + "8" + "</Rank></Attribute>"

if str(TabFullName) == "Price Classes":
	ATTRIBUTES += '<Attribute><AttributeName><USEnglish>QSTN_PRICCLS_TREEVIEW</USEnglish></AttributeName><AttributeType>String</AttributeType><DisplayType>DisplayOnlyText</DisplayType><SpansAcrossEntireRow>1</SpansAcrossEntireRow><Label><USEnglish></USEnglish></Label><Hint><USEnglish><![CDATA[<div id="pricl_treeGrid"></div><script type="text/javascript">$(document).ready(function(){PRICCLSTreeTable();});</script>]]></USEnglish></Hint><ShowOneTimePrice>0</ShowOneTimePrice><IsFirstValuePreselected>0</IsFirstValuePreselected><Values><Value><USEnglish>1</USEnglish></Value></Values></Attribute>'
	TABAttributes += "<Attribute><Name>QSTN_PRICCLS_TREEVIEW</Name><Rank>" + "8" + "</Rank></Attribute>"
if str(TabFullName) == "Roles":
	ATTRIBUTES += '<Attribute><AttributeName><USEnglish>QSTN_ROLES_TREEVIEW</USEnglish></AttributeName><AttributeType>String</AttributeType><DisplayType>DisplayOnlyText</DisplayType><SpansAcrossEntireRow>1</SpansAcrossEntireRow><Label><USEnglish></USEnglish></Label><Hint><USEnglish><![CDATA[<div id="catTreeTable"></div><script type="text/javascript">$(document).ready(function(){ROLESTreeTable();});</script>]]></USEnglish></Hint><ShowOneTimePrice>0</ShowOneTimePrice><IsFirstValuePreselected>0</IsFirstValuePreselected><Values><Value><USEnglish>1</USEnglish></Value></Values></Attribute>'
	TABAttributes += "<Attribute><Name>QSTN_ROLES_TREEVIEW</Name><Rank>" + "8" + "</Rank></Attribute>"

# Get Section inforamtion
SectionRecord = Sql.GetList(
	"select top 1000 SYSECT.PRIMARY_OBJECT_NAME,SYSECT.RECORD_ID,SYSECT.SAPCPQ_ATTRIBUTE_NAME,SYSECT.PAGE_RECORD_ID,SYPAGE.TAB_RECORD_ID FROM SYSECT (NOLOCK) INNER JOIN SYPAGE (NOLOCK) on SYSECT.PAGE_RECORD_ID = SYPAGE.RECORD_ID where SYPAGE.TAB_RECORD_ID='"
	+ str(TabRecordNo)
	+ "' and SYSECT.PARENT_SECTION_RECORD_ID=''  ORDER BY abs(SYSECT.DISPLAY_ORDER)"
)

"""SectionRecord = Sql.GetList(
	"select top 1000 PRIMARY_OBJECT_NAME,RECORD_ID,SAPCPQ_ATTRIBUTE_NAME FROM SYSECT (NOLOCK) where TAB_RECORD_ID='"
	+ str(TabRecordNo)
	+ "' and PARENT_SECTION_RECORD_ID=''  ORDER BY abs(DISPLAY_ORDER)"
)"""
OBJNAME_FIRST_RECORS = "TRUE"
Trace.Write('Tab Record No'+str(TabRecordNo))
Trace.Write('At 160--Section REcords-->'+str(SectionRecord))
for SCEItem in SectionRecord:
	if OBJNAME_FIRST_RECORS == "TRUE":
		SECTION_PRIMARY_OBJNAME = str(SCEItem.PRIMARY_OBJECT_NAME).strip()
		OBJNAME_FIRST_RECORS = "FALSE"
		SYOBJH_RECORDS = Sql.GetFirst(
			"select RECORD_ID,PLURAL_LABEL FROM SYOBJH (NOLOCK) where OBJECT_NAME='" + str(SECTION_PRIMARY_OBJNAME) + "'"
		)
		Trace.Write('At line 169-->'+str(SYOBJH_RECORDS))
		if SYOBJH_RECORDS is not None:
			SYOBJH_RecordId = str(SYOBJH_RECORDS.RECORD_ID)
			SYOBJS_RECORDS = Sql.GetFirst(
				"select NAME,CAN_ADD,CAN_EDIT,CAN_DELETE,COLUMNS,CONTAINER_NAME,OBJ_REC_ID FROM SYOBJS (NOLOCK) where OBJ_REC_ID='"
				+ str(SYOBJH_RecordId)
				+ "' AND upper(NAME)='TAB LIST'"
			)
			Trace.Write('At line 177-->'+str(SYOBJS_RECORDS))
			if (
				str(TabFullName) == "Roles"
			):
				if SYOBJS_RECORDS is not None:
					ATTRIBUTES += "<Attribute><AttributeName><USEnglish>SEARCH_FILTER_BTN</USEnglish></AttributeName><AttributeType>UserSelection</AttributeType><DisplayType>Button</DisplayType><ButtonText><USEnglish>SEARCH</USEnglish></ButtonText><IsFirstValuePreselected>0</IsFirstValuePreselected><Values><Value><USEnglish>att</USEnglish><Rank>10</Rank><ValueCode>1</ValueCode></Value></Values></Attribute>"
					TABAttributes += (
						"<Attribute><Name>BTN_MA_ALL_REFRESH</Name><Rank>"
						+ "10"
						+ "</Rank></Attribute><Attribute><Name>SEARCH_FILTER_BTN</Name><Rank>"
						+ "10"
						+ "</Rank></Attribute>"
					)
					if str(SYOBJS_RECORDS.CAN_ADD).strip().upper() == "TRUE":
						ATTRIBUTES += (
							"<Attribute><AttributeName><USEnglish>BTN_"
							+ str(TabFullName).upper().replace(" ", "_")
							+ "_ADDNEW</USEnglish></AttributeName><AttributeType>UserSelection</AttributeType><DisplayType>Button</DisplayType><AttachScriptButton>1</AttachScriptButton><ButtonScripts><ButtonScript><Name>SYTBADDNEW</Name><Rank>1</Rank></ButtonScript></ButtonScripts><ButtonText><USEnglish>ADD NEW</USEnglish></ButtonText><IsFirstValuePreselected>0</IsFirstValuePreselected><Values><Value><USEnglish>att</USEnglish><Rank>10</Rank><ValueCode>1</ValueCode></Value></Values></Attribute>"
						)
						TABAttributes += (
							"<Attribute><Name>BTN_"
							+ str(TabFullName).upper().replace(" ", "_")
							+ "_ADDNEW</Name><Rank>"
							+ "10"
							+ "</Rank></Attribute>"
						)
			else:
				if SYOBJS_RECORDS is not None:
					ATTRIBUTES += "<Attribute><AttributeName><USEnglish>SEARCH_FILTER_BTN</USEnglish></AttributeName><AttributeType>UserSelection</AttributeType><DisplayType>Button</DisplayType><ButtonText><USEnglish>SEARCH</USEnglish></ButtonText><IsFirstValuePreselected>0</IsFirstValuePreselected><Values><Value><USEnglish>att</USEnglish><Rank>10</Rank><ValueCode>1</ValueCode></Value></Values></Attribute>"

					if str(SYOBJS_RECORDS.NAME).strip().upper() == "TAB LIST":
						# ATTRIBUTES+="<Attribute><AttributeName><USEnglish>LIST_"+str(SYOBJS_RECORDS.CONTAINER_NAME)+"</USEnglish></AttributeName><AttributeType>Container</AttributeType><DisplayType>Container</DisplayType><SpansAcrossEntireRow>1</SpansAcrossEntireRow><Label><USEnglish>"+str(SYOBJH_RECORDS.PLURAL_LABEL)+"</USEnglish></Label><Values><Value><USEnglish>"+"1"+"</USEnglish></Value></Values></Attribute>"
						ATTRIBUTES += '<Attribute><AttributeName><USEnglish>ALL_TABLIS</USEnglish></AttributeName><AttributeType>String</AttributeType><DisplayType>DisplayOnlyText</DisplayType><SpansAcrossEntireRow>1</SpansAcrossEntireRow><Label><USEnglish></USEnglish></Label><Hint><USEnglish><![CDATA[<div id="TabContainerFull"></div><script type="text/javascript">$(document).ready(function(){ TabContainerFullList() });</script>]]></USEnglish></Hint><ShowOneTimePrice>0</ShowOneTimePrice><IsFirstValuePreselected>0</IsFirstValuePreselected><Values><Value><USEnglish>1</USEnglish></Value></Values></Attribute>'
						TABAttributes += (
							"<Attribute><Name>BTN_MA_ALL_REFRESH</Name><Rank>"
							+ "10"
							+ "</Rank></Attribute><Attribute><Name>SEARCH_FILTER_BTN</Name><Rank>"
							+ "10"
							+ "</Rank></Attribute>"
						)
						if str(SYOBJS_RECORDS.CAN_ADD).strip().upper() == "TRUE":
							ATTRIBUTES += (
								"<Attribute><AttributeName><USEnglish>BTN_"
								+ str(TabFullName).upper().replace(" ", "_")
								+ "_ADDNEW</USEnglish></AttributeName><AttributeType>UserSelection</AttributeType><DisplayType>Button</DisplayType><AttachScriptButton>1</AttachScriptButton><ButtonScripts><ButtonScript><Name>SYTBADDNEW</Name><Rank>1</Rank></ButtonScript></ButtonScripts><ButtonText><USEnglish>ADD NEW</USEnglish></ButtonText><IsFirstValuePreselected>0</IsFirstValuePreselected><Values><Value><USEnglish>att</USEnglish><Rank>10</Rank><ValueCode>1</ValueCode></Value></Values></Attribute>"
							)
							TABAttributes += (
								"<Attribute><Name>BTN_"
								+ str(TabFullName).upper().replace(" ", "_")
								+ "_ADDNEW</Name><Rank>"
								+ "10"
								+ "</Rank></Attribute>"
							)
						# A043S001P01-12462 Start

						if str(TabFullName).upper() == "PROFILES":
							ATTRIBUTES += (
								"<Attribute><AttributeName><USEnglish>BTN_"
								+ str(TabFullName).upper().replace(" ", "_")
								+ "_REFRESH</USEnglish></AttributeName><AttributeType>UserSelection</AttributeType><DisplayType>Button</DisplayType><AttachScriptButton>1</AttachScriptButton><ButtonScripts><ButtonScript><Name>SYSYNCSYPR</Name><Rank>1</Rank></ButtonScript></ButtonScripts><ButtonText><USEnglish>REFRESH</USEnglish></ButtonText><IsFirstValuePreselected>0</IsFirstValuePreselected><Values><Value><USEnglish>att</USEnglish><Rank>10</Rank><ValueCode>1</ValueCode></Value></Values></Attribute>"
							)
							TABAttributes += (
								"<Attribute><Name>BTN_"
								+ str(TabFullName).upper().replace(" ", "_")
								+ "_REFRESH</Name><Rank>"
								+ "20"
								+ "</Rank></Attribute>"
							)
						'''if str(SYOBJS_RECORDS.COLUMNS).strip()!="":
							resp_values = str(SYOBJS_RECORDS.COLUMNS).strip().replace(" ", "").replace("['", "").replace("']", "").split("','")
							count=10
							for values in resp_values:
								count=count+1
								Searchvalues=""
								Searchvalues=str(values).replace(" ", "_")
								ATTRIBUTES+="<Attribute><AttributeName><USEnglish>SEARCH_"+str(count)+"_"+str(Searchvalues)+"</USEnglish></AttributeName><AttributeType>UserSelection</AttributeType><DisplayType>FreeInputNoMatching</DisplayType><SpansAcrossEntireRow>1</SpansAcrossEntireRow><Label><USEnglish>"+str(values).replace(" ", "_")+"</USEnglish></Label><Hint><USEnglish>"+str(Searchvalues)+"</USEnglish></Hint><ShowOneTimePrice>0</ShowOneTimePrice><IsFirstValuePreselected>0</IsFirstValuePreselected><Values><Value><USEnglish>att</USEnglish><Rank>10</Rank><ValueCode>1</ValueCode></Value></Values></Attribute>"
								TABAttributes+="<Attribute><Name>SEARCH_"+str(count)+"_"+str(Searchvalues)+"</Name><Rank>"+str(count)+"</Rank></Attribute>"'''
						# TABAttributes+="<Attribute><Name>LIST_"+str(SYOBJS_RECORDS.CONTAINER_NAME)+"</Name><Rank>"+"200"+"</Rank></Attribute>"
						TABAttributes += "<Attribute><Name>ALL_TABLIS</Name><Rank>" + "250" + "</Rank></Attribute>"
ModuleRecord = Sql.GetFirst("select APP_LABEL,APP_ID FROM SYAPPS (NOLOCK) where APP_RECORD_ID='" + str(RecordNo) + "'")
productName = ""
if ModuleRecord is not None:
	productName = str(ModuleRecord.APP_LABEL)
# A043S001P01-12462 Start

if  str(TabFullName) != "Quotes" and str(TabFullName) != "My Approval Queue":
	tabslist += (
		"<Tab><SystemId>"
		+ str(TabFullName)
		+ "_LIST_cpq</SystemId><Name>"
		+ str(TabFullName)
		+ "</Name><Rank>"
		+ str(Tabrank)
		+ "</Rank><LayoutTemplate>Standard - 1 Column</LayoutTemplate><RDTemplate>SYSALLLISTTAB</RDTemplate><VisibilityPermission>2</VisibilityPermission><VisibilityCondition>"
		+ tabVisibilityConditionSA.format(TabName, productName, str(TabFullName))
		+ "</VisibilityCondition><ShowTabHeader>1</ShowTabHeader><Attributes>"
		+ str(TABAttributes)
		+ "</Attributes></Tab>"
	)
elif str(TabFullName) == "My Approval Queue":
	tabslist += (
		"<Tab><SystemId>"
		+ str(TabFullName)
		+ "_LIST_cpq</SystemId><Name>"
		+ str(TabFullName)
		+ "</Name><Rank>"
		+ str(Tabrank)
		+ "</Rank><LayoutTemplate>Standard - 1 Column</LayoutTemplate><RDTemplate>SYSACLISTTAB</RDTemplate><VisibilityPermission>2</VisibilityPermission><VisibilityCondition>"
		+ tabVisibilityConditionSA.format(TabName, productName, str(TabFullName))
		+ "</VisibilityCondition><ShowTabHeader>1</ShowTabHeader><Attributes>"
		+ str(TABAttributes)
		+ "</Attributes></Tab>"
	)
else:
	tabslist += (
	"<Tab><SystemId>"
	+ str(TabFullName)
	+ "_LIST_cpq</SystemId><Name>"
	+ str(TabFullName)
	+ "</Name><Rank>"
	+ str(Tabrank)
	+ "</Rank><LayoutTemplate>Standard - 1 Column</LayoutTemplate><RDTemplate>SYSQTLISTTAB</RDTemplate><VisibilityPermission>2</VisibilityPermission><VisibilityCondition>"
	+ tabVisibilityCondition.format(TabName, productName, str(TabFullName))
	+ "</VisibilityCondition><ShowTabHeader>1</ShowTabHeader><Attributes>"
	+ str(TABAttributes)
	+ "</Attributes></Tab>"
)

# A043S001P01-12462 End
return tabslist


##Build Tab
def BuildTabAttributes(TabId, TabName, TabRecordNo, Tabrank, pivotRank, TabFullName):
TabAttributeXML = ""
global ATTRIBUTES
ModuleRecord = Sql.GetFirst("select APP_LABEL,APP_ID FROM SYAPPS (NOLOCK) where APP_RECORD_ID='" + str(RecordNo) + "'")
productName = ""
if ModuleRecord is not None:
	productName = str(ModuleRecord.APP_LABEL)
TabAttributeCommonForAllTab = (
	"<Attribute><Name>BTN_MA_ALL_REFRESH</Name><Rank>"
	+ "10"
	+ "</Rank></Attribute><Attribute><Name>SEC_N_TAB_PAGE_ALERT</Name><Rank>"
	+ "10"
	+ "</Rank></Attribute>"
)
ActionBannerControls = BuildActionBannerControls(TabRecordNo)
TabAttributes = BuildTabLayoutAttributes(TabRecordNo, TabName)
PivotTable = BuildPivotTabe(TabName, pivotRank)
TabRelatedListAttributes = BuildRelatedListAttributes(TabRecordNo)
GettreeEnable = Sql.GetFirst("select  ENABLE_TREE FROM SYTABS (NOLOCK) where RECORD_ID='" + str(TabRecordNo) + "'")
if str(TabName) == "Price Agreement" and RecordNo != "894DC9AF-5A59-48A4-8709-449304184433":
	TabAttributeXML = (
		"<Tab><SystemId>"
		+ str(TabId)
		+ "</SystemId><Name>"
		+ str(TabName)
		+ "</Name><Rank>"
		+ str(Tabrank)
		+ "</Rank><LayoutTemplate>Standard - 1 Column</LayoutTemplate><RDTemplate>MM_SEGMENT_TAB</RDTemplate>"
	)
	TabAttributeXML += (
		"<VisibilityPermission>2</VisibilityPermission><VisibilityCondition>"
		+ tabVisibilityCondition.format(TabName, productName, str(TabFullName))
		.replace("[CDATA[[AND]([NOT]([EQ](", "[CDATA[[AND]([EQ](")
		.replace(")),", "),")
		+ "</VisibilityCondition><ShowTabHeader>1</ShowTabHeader>"
	)
	TabAttributeXML += (
		"<Attributes>"
		+ TabAttributeCommonForAllTab
		+ ActionBannerControls
		+ TabAttributes
		+ PivotTable
		+ TabRelatedListAttributes
		+ "</Attributes></Tab>"
	)

elif str(TabName) == "Price Model":
	TabAttributeXML = (
		"<Tab><SystemId>"
		+ str(TabId)
		+ "</SystemId><Name>"
		+ str(TabName)
		+ "</Name><Rank>"
		+ str(Tabrank)
		+ "</Rank><LayoutTemplate>Standard - 1 Column</LayoutTemplate><RDTemplate>MM_PRICE_MODEL_TAB</RDTemplate>"
	)
	TabAttributeXML += (
		"<VisibilityPermission>2</VisibilityPermission><VisibilityCondition>"
		+ tabVisibilityCondition.format(TabName, productName, str(TabFullName))
		.replace("[CDATA[[AND]([NOT]([EQ](", "[CDATA[[AND]([EQ](")
		.replace(")),", "),")
		+ "</VisibilityCondition><ShowTabHeader>1</ShowTabHeader>"
	)
	TabAttributeXML += (
		"<Attributes>"
		+ TabAttributeCommonForAllTab
		+ ActionBannerControls
		+ TabAttributes
		+ PivotTable
		+ TabRelatedListAttributes
		+ "</Attributes></Tab>"
	)


elif GettreeEnable is not None and str(GettreeEnable.ENABLE_TREE).upper() == "TRUE":
	if TabName != "Email Template":
		TabAttributeXML = (
			"<Tab><SystemId>"
			+ str(TabId)
			+ "</SystemId><Name>"
			+ str(TabName)
			+ "</Name><Rank>"
			+ str(Tabrank)
			+ "</Rank><LayoutTemplate>Standard - 1 Column</LayoutTemplate><RDTemplate>SYSTREETAB</RDTemplate>"
		)
	else:
		TabAttributeXML = (
			"<Tab><SystemId>"
			+ str(TabId)
			+ "</SystemId><Name>"
			+ str(TabName)
			+ "</Name><Rank>"
			+ str(Tabrank)
			+ "</Rank><LayoutTemplate>Standard - 1 Column</LayoutTemplate><RDTemplate>AC_EmailTemplate</RDTemplate>"
		)
	TabAttributeXML += (
		"<VisibilityPermission>2</VisibilityPermission><VisibilityCondition>"
		+ tabVisibilityCondition.format(TabName, productName, str(TabFullName))
		.replace("[CDATA[[AND]([NOT]([EQ](", "[CDATA[[AND]([EQ](")
		.replace(")),", "),")
		+ "</VisibilityCondition><ShowTabHeader>1</ShowTabHeader>"
	)
	TabAttributeXML += (
		"<Attributes>"
		+ TabAttributeCommonForAllTab
		+ ActionBannerControls
		+ TabAttributes
		+ PivotTable
		+ TabRelatedListAttributes
		+ "</Attributes></Tab>"
	)

else:
	TabAttributeXML = (
		"<Tab><SystemId>"
		+ str(TabId)
		+ "</SystemId><Name>"
		+ str(TabName)
		+ "</Name><Rank>"
		+ str(Tabrank)
		+ "</Rank><LayoutTemplate>Standard - 1 Column</LayoutTemplate>"
	)
	TabAttributeXML += (
		"<VisibilityPermission>2</VisibilityPermission><VisibilityCondition>"
		+ tabVisibilityCondition.format(TabName, productName, str(TabFullName))
		.replace("[CDATA[[AND]([NOT]([EQ](", "[CDATA[[AND]([EQ](")
		.replace(")),", "),")
		+ "</VisibilityCondition><ShowTabHeader>1</ShowTabHeader>"
	)
	TabAttributeXML += (
		"<Attributes>"
		+ TabAttributeCommonForAllTab
		+ ActionBannerControls
		+ TabAttributes
		+ PivotTable
		+ TabRelatedListAttributes
		+ "</Attributes></Tab>"
	)
return TabAttributeXML


# Build Tab Action Banner Controls
def BuildActionBannerControls(TabRecordNo):
global ATTRIBUTES
ActionBannerControls = ""
ACTCount = 10
# ----A043S001P01-7192 START-----
# Object Level Messages
ObjectValue = Sql.GetFirst(
	"SELECT PRIMARY_OBJECT_RECORD_ID,PRIMARY_OBJECT_NAME,TAB_LABEL FROM SYTABS (NOLOCK) WHERE RECORD_ID='"
	+ str(TabRecordNo)
	+ "'"
)
Tab_Name = ObjectValue.TAB_LABEL
# Tab Level Messages
MessageRecords = Sql.GetList(
	"select top 1000 SAPCPQ_ATTRIBUTE_NAME,MESSAGE_TEXT,MESSAGE_TYPE,MESSAGE_LEVEL,MESSAGE_CODE FROM SYMSGS (NOLOCK) where TAB_RECORD_ID='"
	+ str(TabRecordNo)
	+ "' ORDER BY MESSAGE_CODE"
)
# ----A043S001P01-7192 END-----
for Messages in MessageRecords:
	if len(str(Messages.SAPCPQ_ATTRIBUTE_NAME)) > 0:
		ATTRIBUTES += (
			"<Attribute><AttributeName><USEnglish>"
			+ "ERR_MSG_"
			+ str(Tab_Name)
			+ "</USEnglish></AttributeName><AttributeType>String</AttributeType><DisplayType>DisplayOnlyText</DisplayType><SpansAcrossEntireRow>1</SpansAcrossEntireRow><Label><USEnglish>"
			+ "ERR_MSG_"
			+ str(Tab_Name)
			+ "</USEnglish></Label><Hint><USEnglish></USEnglish></Hint><ShowOneTimePrice>0</ShowOneTimePrice><IsFirstValuePreselected>0</IsFirstValuePreselected><Values><Value><USEnglish>1</USEnglish></Value></Values></Attribute>"
		)
		ActionBannerControls += (
			"<Attribute><Name>"
			+ "ERR_MSG_"
			+ str(Tab_Name)
			+ "</Name><Rank>"
			+ "7"
			+ "</Rank><Preselected>0</Preselected></Attribute>"
		)
ActionRecord = Sql.GetList(
	"select top 1000 SAPCPQ_ATTRIBUTE_NAME,ACTION_NAME,DISPLAY_ORDER,ACTION_DESCRIPTION,SCRIPT_NAME FROM SYPGAC (NOLOCK) where TAB_RECORD_ID='"
	+ str(TabRecordNo)
	+ "' and  (HTML_CONTENT  IS NULL OR HTML_CONTENT = '') ORDER BY DISPLAY_ORDER"
)
for ActionItem in ActionRecord:
	ACTCount = ACTCount + 1
	# ACTID = "BTN_" + str(ActionItem.ATTRIBUTE_NAME).replace(" ", "_") + "_cpq"
	ACTRecordno = str(ActionItem.SAPCPQ_ATTRIBUTE_NAME)
	ACTIONRECORDID = str(ActionItem.SAPCPQ_ATTRIBUTE_NAME).replace("-", "_")
	ACTIONNAME = str(ActionItem.ACTION_NAME).replace(" ", "")
	ACTATTRIBUTENAME = (ACTIONRECORDID + "_" + ACTIONNAME).upper()
	BUTTON_SCRIPTNAME = str(ActionItem.SCRIPT_NAME).strip()
	global ATTRIBUTES
	ATTRIBUTES += (
		"<Attribute><AttributeName><USEnglish>BTN_"
		+ str(ACTATTRIBUTENAME)
		+ "</USEnglish></AttributeName><AttributeType>UserSelection</AttributeType><DisplayType>Button</DisplayType><AttachScriptButton>1</AttachScriptButton><ButtonScripts><ButtonScript><Name>"
		+ str(BUTTON_SCRIPTNAME)
		+ "</Name><Rank>1</Rank></ButtonScript></ButtonScripts><ButtonText><USEnglish>"
		+ str(ActionItem.ACTION_NAME)
		+ "</USEnglish></ButtonText><IsFirstValuePreselected>0</IsFirstValuePreselected><Values><Value><USEnglish>att</USEnglish><Rank>10</Rank><ValueCode>1</ValueCode></Value></Values></Attribute>"
	)
	ActionBannerControls += (
		"<Attribute><Name>BTN_" + str(ACTATTRIBUTENAME) + "</Name><Rank>" + str(ACTCount) + "</Rank></Attribute>"
	)
return ActionBannerControls


def BuildTabLayoutAttributes(TabRecordNo, TabName):
global ATTRIBUTES
TabAttributes = ""
global EDIT
EDIT = "FALSE"
# Tab Section Banner Controls:
# A043S001P01-12988 Dhurga-Start
"""SectionRecords = Sql.GetList(
	"select top 1000 SAPCPQ_ATTRIBUTE_NAME,RECORD_ID,SUPPRESS_BANNER,SECTION_NAME,DISPLAY_ORDER,ATTRIBUTE_NAME,DEFAULT_BANNER_COLOR,ERROR_BANNER_COLOR,PARENT_SECTION_NAME,TAB_RECORD_ID,TAB_NAME,PRIMARY_OBJECT_NAME,PRIMARY_OBJECT_RECORD_ID FROM SYSECT (NOLOCK) where TAB_RECORD_ID='"
	+ str(TabRecordNo)
	+ "' and PARENT_SECTION_RECORD_ID=''  ORDER BY DISPLAY_ORDER"
)"""
SectionRecords = Sql.GetList(
	"select top 1000 SYSECT.SAPCPQ_ATTRIBUTE_NAME,SYSECT.RECORD_ID,SYSECT.SUPPRESS_BANNER,SYSECT.SECTION_NAME,SYSECT.DISPLAY_ORDER,SYSECT.DEFAULT_BANNER_COLOR,SYSECT.ERROR_BANNER_COLOR,SYSECT.PARENT_SECTION_TEXT,SYSECT.PRIMARY_OBJECT_NAME,SYSECT.PRIMARY_OBJECT_RECORD_ID FROM SYSECT (NOLOCK) INNER JOIN SYPAGE (NOLOCk) on SYSECT.PAGE_RECORD_ID = SYPAGE.RECORD_ID where SYPAGE.TAB_RECORD_ID='"
	+ str(TabRecordNo)
	+ "' and SYSECT.PARENT_SECTION_RECORD_ID=''  ORDER BY SYSECT.DISPLAY_ORDER"
)
# A043S001P01-12988 Dhurga-End
# Trace.Write("$$$$$$$$$$$$$"+str("select top 1000 RECORD_ID,SECTION_NAME,DISPLAY_ORDER,ATTRIBUTE_NAME,DEFAULT_BANNER_COLOR,ERROR_BANNER_COLOR,PARENT_SECTION_NAME,TAB_RECORD_ID,TAB_NAME,PRIMARY_OBJECT_NAME,PRIMARY_OBJECT_RECORD_ID FROM SYSECT where TAB_RECORD_ID='"
# + str(TabRecordNo)
# + "' and PARENT_SECTION_RECORD_ID=''  ORDER BY DISPLAY_ORDER"))
Allcountsec = 70
GettreeEnable = Sql.GetFirst("select ENABLE_TREE FROM SYTABS (NOLOCK) where RECORD_ID='" + str(TabRecordNo) + "'")

for Section in SectionRecords:
	act_obj = Sql.GetFirst(
		"select * from SYPSAC (NOLOCK) where SECTION_RECORD_ID='" + str(Section.RECORD_ID) + "' "
	)
	if act_obj is not None:
		act_txt = str(act_obj.ACTION_NAME)
		if act_txt == "EDIT":
			EDIT = "TRUE"
	else:
		EDIT = "FALSE"
	Allcountsec = Allcountsec + 130
	TabAttributes += BuildSectionAttributes(Section, TabName, Allcountsec)

if str(TabName) == "Configurable Material":
	ATTRIBUTES += '<Attribute><AttributeName><USEnglish>LIST_test_Configurable</USEnglish></AttributeName><AttributeType>String</AttributeType><DisplayType>DisplayOnlyText</DisplayType><SpansAcrossEntireRow>1</SpansAcrossEntireRow><Label><USEnglish>LIST_test_Configurable</USEnglish></Label><Hint><USEnglish><![CDATA[<div id="treeview"></div><script type="text/javascript">$(document).ready(function(){ ConfigurableLeftTreeView(); });</script>]]></USEnglish></Hint><ShowOneTimePrice>0</ShowOneTimePrice><IsFirstValuePreselected>0</IsFirstValuePreselected><Values><Value><USEnglish>1</USEnglish></Value></Values></Attribute>'
	TabAttributes += "<Attribute><Name>LIST_test_Configurable</Name><Rank>" + "1" + "</Rank></Attribute>"

elif str(TabName) == "Price Model":

	ATTRIBUTES += (
		'<Attribute><AttributeName><USEnglish>LIST_PRICEMODEL_TREEVIEW</USEnglish></AttributeName><AttributeType>String</AttributeType><DisplayType>DisplayOnlyText</DisplayType><SpansAcrossEntireRow>1</SpansAcrossEntireRow><Label><USEnglish></USEnglish></Label><Hint><USEnglish><![CDATA[<div id="prcmdltreeview"></div><script type="text/javascript">$(document).ready(function(){ PricemodelLeftTreeView(); }); </script>]]></USEnglish></Hint><ShowOneTimePrice>0</ShowOneTimePrice><IsFirstValuePreselected>0</IsFirstValuePreselected><Values><Value><USEnglish>1</USEnglish></Value></Values></Attribute><Attribute><AttributeName><USEnglish>PRICERELATED_DTL_VIEW</USEnglish></AttributeName><AttributeType>String</AttributeType><DisplayType>DisplayOnlyText</DisplayType><SpansAcrossEntireRow>1</SpansAcrossEntireRow><Label><USEnglish></USEnglish></Label><Hint><USEnglish><![CDATA[<div id="RelatedDetail"></div>]]></USEnglish></Hint><ShowOneTimePrice>0</ShowOneTimePrice><IsFirstValuePreselected>0</IsFirstValuePreselected><Values><Value><USEnglish>'
		+ "1"
		+ "</USEnglish></Value></Values></Attribute>"
	)
	TabAttributes += (
		"<Attribute><Name>LIST_PRICEMODEL_TREEVIEW</Name><Rank>"
		+ "8"
		+ "</Rank></Attribute><Attribute><Name>PRICERELATED_DTL_VIEW</Name><Rank>"
		+ "8"
		+ "</Rank></Attribute>"
	)

elif GettreeEnable is not None and str(GettreeEnable.ENABLE_TREE).upper() == "TRUE":

	ATTRIBUTES += (
		'<Attribute><AttributeName><USEnglish>TREE_LeftAttribute</USEnglish></AttributeName><AttributeType>String</AttributeType><DisplayType>DisplayOnlyText</DisplayType><SpansAcrossEntireRow>1</SpansAcrossEntireRow><Label><USEnglish></USEnglish></Label><Hint><USEnglish><![CDATA[<div id="commontreeview"></div><script type="text/javascript">$(document).ready(function(){ CommonLeftTreeView(\'commontreeview\');}); </script>]]></USEnglish></Hint><ShowOneTimePrice>0</ShowOneTimePrice><IsFirstValuePreselected>0</IsFirstValuePreselected><Values><Value><USEnglish>1</USEnglish></Value></Values></Attribute><Attribute><AttributeName><USEnglish>HTML_DETAIL_VIEW_RIGHT</USEnglish></AttributeName><AttributeType>String</AttributeType><DisplayType>DisplayOnlyText</DisplayType><SpansAcrossEntireRow>1</SpansAcrossEntireRow><Label><USEnglish></USEnglish></Label><Hint><USEnglish><![CDATA[<div id="TREE_div"></div>]]></USEnglish></Hint><ShowOneTimePrice>0</ShowOneTimePrice><IsFirstValuePreselected>0</IsFirstValuePreselected><Values><Value><USEnglish>'
		+ "1"
		+ "</USEnglish></Value></Values></Attribute>"
	)
	TabAttributes += (
		"<Attribute><Name>TREE_LeftAttribute</Name><Rank>"
		+ "8"
		+ "</Rank></Attribute><Attribute><Name>HTML_DETAIL_VIEW_RIGHT</Name><Rank>"
		+ "8"
		+ "</Rank></Attribute>"
	)

	if str(TabName) in ["Approval Chain", "My Approvals Queue"]:
		ATTRIBUTES += (
			'<Attribute><AttributeName><USEnglish>SEGMENT_QUERY_BUILDER</USEnglish></AttributeName><AttributeType>String</AttributeType><DisplayType>DisplayOnlyText</DisplayType><SpansAcrossEntireRow>1</SpansAcrossEntireRow><Label><USEnglish>SEGMENT_QUERY_BUILDER</USEnglish></Label><Hint><USEnglish><![CDATA[<div id="SegmentQueryBuilder"></div>]]></USEnglish></Hint><Values><Value><USEnglish>'
			+ "1"
			+ "</USEnglish></Value></Values></Attribute>"
		)

		TabAttributes += "<Attribute><Name>SEGMENT_QUERY_BUILDER</Name><Rank>" + "21" + "</Rank></Attribute>"

elif str(TabName) == "Price Agreement" and RecordNo != "894DC9AF-5A59-48A4-8709-449304184433":
	try:
		ATTRIBUTES += '<Attribute><AttributeName><USEnglish>LIST_test_Segment</USEnglish></AttributeName><AttributeType>String</AttributeType><DisplayType>DisplayOnlyText</DisplayType><SpansAcrossEntireRow>1</SpansAcrossEntireRow><Label><USEnglish></USEnglish></Label><Hint><USEnglish><![CDATA[<div id="treeview"></div><script type="text/javascript">$(document).ready(function(){ SegmentLeftTreeView(); }); </script>]]></USEnglish></Hint><ShowOneTimePrice>0</ShowOneTimePrice><IsFirstValuePreselected>0</IsFirstValuePreselected><Values><Value><USEnglish>1</USEnglish></Value></Values></Attribute>'
		TabAttributes += "<Attribute><Name>LIST_test_Segment</Name><Rank>" + "8" + "</Rank></Attribute>"
	except:
		Trace.Write('Segments Attribute "LIST_test_Segment"--')

	try:
		ATTRIBUTES += (
			'<Attribute><AttributeName><USEnglish>MATDETIL_VIEW_ATTR</USEnglish></AttributeName><AttributeType>String</AttributeType><DisplayType>DisplayOnlyText</DisplayType><SpansAcrossEntireRow>1</SpansAcrossEntireRow><Label><USEnglish></USEnglish></Label><Hint><USEnglish><![CDATA[<div id="MaterialDetail"></div>]]></USEnglish></Hint><ShowOneTimePrice>0</ShowOneTimePrice><IsFirstValuePreselected>0</IsFirstValuePreselected><Values><Value><USEnglish>'
			+ "1"
			+ "</USEnglish></Value></Values></Attribute>"
		)
		TabAttributes += "<Attribute><Name>MATDETIL_VIEW_ATTR</Name><Rank>" + "8" + "</Rank></Attribute>"
	except:
		Trace.Write("Error in Attr create MATDETIL_VIEW_ATTR")

	ATTRIBUTES += (
		'<Attribute><AttributeName><USEnglish>SEGMENT_QUERY_BUILDER</USEnglish></AttributeName><AttributeType>String</AttributeType><DisplayType>DisplayOnlyText</DisplayType><SpansAcrossEntireRow>1</SpansAcrossEntireRow><Label><USEnglish>SEGMENT_QUERY_BUILDER</USEnglish></Label><Hint><USEnglish><![CDATA[<div id="SegmentQueryBuilder"></div>]]></USEnglish></Hint><Values><Value><USEnglish>'
		+ "1"
		+ "</USEnglish></Value></Values></Attribute>"
	)

	TabAttributes += "<Attribute><Name>SEGMENT_QUERY_BUILDER</Name><Rank>" + "21" + "</Rank></Attribute>"
return TabAttributes


def BuildSectionAttributes(SCEItem, TabName, Allcountsec):
global ATTRIBUTES
TabAttributes = ""
# Decalre Varaibles
tabslist = ""
Sections = ""
SBSect_banner = ""
TABAttri = ""
Attr_Type = ""
TABNANES = ""
Attr_Disptype = ""
CustomTable = []
APIdata = ""
sec_attr = ""
# SCEID = "SEC_" + str(SCEItem.ATTRIBUTE_NAME).replace(" ", "_") + "_cpq"
if str(SCEItem.RECORD_ID):
	SecRecordid = str(SCEItem.RECORD_ID)
SECTIONRECORDID = str(SCEItem.SAPCPQ_ATTRIBUTE_NAME).replace("-", "_")
# /A043S001P01-12988 Start-Dhurga
SUPSECTBAN = str(SCEItem.SUPPRESS_BANNER)
SECTIONNAME = str(SCEItem.SECTION_NAME).replace(" ", "")
SECATTRIBUTENAME = (SECTIONRECORDID).upper()

if SCEItem.SECTION_NAME == "PERSONALIZATION PLANT MATERIAL + ATTRIBUTES":
	Sections = (
		'<htmlData><![CDATA[<div><div class="dropdown column-with-actions flt_lt"><i data-toggle="dropdown" class="fa fa-sort-desc"></i><ul class="dropdown-menu"><li><button id="PERSONALIZATION" onclick="cont_PERSONALIZEADDNewopenview(this, \'PERSONALIZATION\')" class="btnstyle addNewRel" data-target="#cont_viewModalSection" data-toggle="modal">ADD NEW</button></li><li><button id="PERSONALIZATION" onclick="cont_PERSONALIZEdelete(this, \'PERSONALIZATION\')" class="btnstyle addNewRel"  data-target="#related_delete_POPUP" data-toggle="modal" disabled="disabled">DELETE</button></li></ul></div><p>'
		+ str(SCEItem.SECTION_NAME)
		+ "</p></div>]]></htmlData>"
	)
elif SCEItem.SECTION_NAME == "PERSONALIZATION PLANT MATERIAL + ATTRIBUTES":
	Sections = (
		'<htmlData><![CDATA[<div><div class="dropdown column-with-actions flt_lt"><i data-toggle="dropdown" class="fa fa-sort-desc"></i><ul class="dropdown-menu"><li><button id="PLANT" onclick="cont_PERSONALIZEADDNewopenview(this, \'PLANT\')" class="btnstyle addNewRel" data-target="#cont_viewModalSection" data-toggle="modal">ADD NEW</button></li><li><button id="PLANT" onclick="cont_PERSONALIZEdelete(this, \'PLANT\')" class="btnstyle addNewRel" data-target="#related_delete_POPUP" data-toggle="modal" disabled="disabled">DELETE</button></li></ul></div><p>'
		+ str(SCEItem.SECTION_NAME)
		+ "</p></div>]]></htmlData>"
	)
else:
	# Section level-editable permissions -- 11792 start
	# permissionAcces_obj = Sql.GetFirst("Select P.EDITABLE,P.VISIBLE from SYPRSN P inner join USERS_PERMISSIONS up on up.permission_id = P.PROFILE_RECORD_ID where up.user_id = '"+str(userId)+"' and P.SECTION_RECORD_ID = '"+str(SecRecordid)+"'")
	# if permissionAcces_obj:

	# if permissionAcces_obj.EDITABLE:
	section_edit_btn = ""
	if EDIT.upper() == "TRUE":
		sec_html_btn = Sql.GetList("SELECT HTML_CONTENT FROM SYPSAC (NOLOCK) WHERE SECTION_RECORD_ID = '"+str(SecRecordid)+"'")
		if sec_html_btn is not None:
			for btn in sec_html_btn:
				if "EDIT" in btn.HTML_CONTENT:
					section_edit_btn = str(btn.HTML_CONTENT).format(rec_id=SecRecordid, edit_click="sec_edit_tab(this)")
				if "CANCEL" in btn.HTML_CONTENT:
					cancel_btn = str(btn.HTML_CONTENT)
				if "SAVE" in btn.HTML_CONTENT:
					save_btn = str(btn.HTML_CONTENT)

			# cancel_save = '<div  class="g4 sec_' + str(SECTION_EDIT) + ' collapse in except_sec removeHorLine iconhvr sec_edit_sty">'+ str(cancel_btn) + str(save_btn) +'</div>'
		# Trace.Write("CANCL_BTN "+str(cancel_save))
		if SUPSECTBAN.upper() == "FALSE":
			sec_attr += (str(section_edit_btn))
			# sec_attr = (
			# 	'<div id="ctr_drop" class="btn-group dropdown"><div class="dropdown" ><i data-toggle="dropdown" class="fa fa-sort-desc dropdown-toggle" ></i><ul class="dropdown-menu left" aria-labelledby="dropdownMenuButton"><li class="edit_list" ><a  id="'
			# 	+ str(SecRecordid)
			# 	+ '" class="dropdown-item" href="#" onclick="sec_edit_tab(this)">EDIT</a></li></ul></div></div>'
			# )
		else:
			sec_attr += ""
	else:
		sec_attr += ""
	# Section level-editable permissions 11792 end
	permissionvisible_obj = Sql.GetFirst("Select P.VISIBLE from SYPRSN P inner join USERS_PERMISSIONS up on up.permission_id =P.PROFILE_RECORD_ID where up.user_id = '"+str(userId)+"' and P.SECTION_RECORD_ID = '"+str(SecRecordid)+"'")
	if permissionvisible_obj:
		if str(permissionvisible_obj.VISIBLE).upper() == 'TRUE':
			Sections = (
				"<htmlData><![CDATA[<div>"
				+ str(sec_attr)
				+ ""
				+ str(SCEItem.SECTION_NAME)
				+ "</div>]]></htmlData>"
			)
	if SUPSECTBAN.upper() == "FALSE":
		Sections = "<htmlData><![CDATA[<div>" + str(sec_attr) + "" + str(SCEItem.SECTION_NAME) + "</div>]]></htmlData>"
	else:
		Sections = ""
	# A043S001P01-12988 END -Dhurga
global ATTRIBUTES
ATTRIBUTES += (
	"<Attribute><AttributeName><USEnglish>SEC_"
	+ str(SECATTRIBUTENAME)
	+ "</USEnglish></AttributeName><AttributeType>String</AttributeType><DisplayType>DisplayOnlyText</DisplayType><SpansAcrossEntireRow>1</SpansAcrossEntireRow><Label><USEnglish>"
	+ str(SCEItem.SECTION_NAME).replace('"', '"')
	+ "</USEnglish></Label><Hint><USEnglish>"
	+ str(Sections).replace('"', '"')
	+ "</USEnglish></Hint><ShowOneTimePrice>0</ShowOneTimePrice><IsFirstValuePreselected>0</IsFirstValuePreselected><Values><Value><USEnglish>"
	+ str(SCEItem.SECTION_NAME)
	+ "</USEnglish></Value></Values></Attribute>"
)
TabAttributes += (
	"<Attribute><Name>SEC_" + str(SECATTRIBUTENAME) + "</Name><Rank>" + str(Allcountsec) + "</Rank></Attribute>"
)
# Tab Section Question Controls:

# Question level permissions depending upon sections visible- start
# QuestionRecord = Sql.GetList("select Distinct top 100 S.RECORD_ID,S.FIELD_LABEL,S.ATTRIBUTE_NAME,S.DISPLAY_ORDER,S.DATATYPE,S.PICKLIST,S.LENGTH,S.DECIMAL_PLACES,S.HELP_TEXT_TITLE,S.HELP_TEXT_COPY,S.API_NAME,S.API_NAME FROM SYSEFL (NOLOCK) S  inner join SYPRSF (NOLOCK) P on P.SECTION_RECORD_ID = S.SECTION_RECORD_ID inner join users_permissions (NOLOCK) up on up.permission_id = P.PROFILE_RECORD_ID where P.SECTION_RECORD_ID='"+str(SecRecordid)+"' and P.VISIBLE = 'True' and up.user_id = '"+str(userId)+"' ORDER BY S.DISPLAY_ORDER")
# Question level permissions end
QuestionRecord = Sql.GetList(
	"select top 1000 SAPCPQ_ATTRIBUTE_NAME,FIELD_LABEL,DISPLAY_ORDER,DATATYPE,PICKLIST,LENGTH,DECIMAL_PLACES,HELP_TEXT_TITLE,HELP_TEXT_COPY,API_NAME,API_FIELD_NAME FROM SYSEFL (NOLOCK) where SECTION_RECORD_ID='"
	+ str(SecRecordid)
	+ "' ORDER BY DISPLAY_ORDER"
)
# Trace.Write("$$$$$$$$$$$$$$$$$$$$4"+str("select top 1000 RECORD_ID,FIELD_LABEL,ATTRIBUTE_NAME,DISPLAY_ORDER,DATATYPE,PICKLIST,LENGTH,DECIMAL_PLACES,HELP_TEXT_TITLE,HELP_TEXT_COPY,API_NAME,API_NAME FROM SYSEFL where SECTION_RECORD_ID='"
# + str(SecRecordid)
# + "' ORDER BY DISPLAY_ORDER"))

for SCEQUESItem in QuestionRecord:
	Allcountsec = Allcountsec + 1
	LOOKUPDISPLAYFIELD = ""
	LookupFiled = ""
	Custom_datatype = ""
	# SCEQUESID = "QSTN_" + str(SCEQUESItem.ATTRIBUTE_NAME).replace(" ", "_") + "_cpq"
	SecQuesRecordid = str(SCEQUESItem.SAPCPQ_ATTRIBUTE_NAME)
	SECTIONQSTNRECORDID = str(SCEQUESItem.SAPCPQ_ATTRIBUTE_NAME).replace("-", "_").replace(" ", "")
	# SECTIONQSTNNAME = str(SCEQUESItem.ATTRIBUTE_NAME).replace(" ", "").replace("  ", "")
	SECQSTNATTRIBUTENAME = (SECTIONQSTNRECORDID).upper()
	SYOBJD_Record = Sql.GetFirst(
		"select LOOKUP_API_NAME,DATA_TYPE,PERMISSION,FORMULA_DATA_TYPE FROM SYOBJD (NOLOCK) where LOOKUP_API_NAME='"
		+ str(SCEQUESItem.API_FIELD_NAME)
		+ "' and OBJECT_NAME='"
		+ str(SCEQUESItem.API_NAME)
		+ "'"
	)
	if SYOBJD_Record is not None:
		if (
			str(SYOBJD_Record.DATA_TYPE).strip().upper() == "LOOKUP"
			and str(SYOBJD_Record.PERMISSION).strip().upper() != "READ ONLY"
		):
			LOOKUPDISPLAYFIELD = "Allowed"
	Attr_value = ""
	Attr_Type = ""
	Questiondatatype = ""
	if str(SCEQUESItem.DATATYPE).strip().upper() == "PICKLIST":
		Attr_Type = "UserSelection"
		Attr_Disptype = "DropDown"
	elif (
		str(SCEQUESItem.DATATYPE).strip().upper() == "TEXT"
		or str(SCEQUESItem.DATATYPE).strip().upper() == "FORMULA"
		or str(SCEQUESItem.DATATYPE) == "LONG TEXT AREA"
		# Added by VETRI for #A043S001P01-7295 - Start
		or str(SecQuesRecordid) == "SYSEFL-SE-00895"
		# Added by wasim for #A043S001P01-5604 - start
		or str(SecQuesRecordid) == "SYSEFL-SE-00923"
		or str(SecQuesRecordid) == "SYSEFL-TQ-00895"
		# Added by wasim for #A043S001P01-5604 - End
		# Added by VETRI for #A043S001P01-7295 - End
	):
		Attr_Type = "String"
		Attr_Disptype = "FreeInputNoMatching"
	elif str(SCEQUESItem.DATATYPE) == "CHECKBOX":
		Attr_Type = "UserSelection"
		Attr_Disptype = "CheckBox"
	elif str(SCEQUESItem.DATATYPE) == "CURRENCY" or SecQuesRecordid == "SYSEFL-PB-00497":
		Attr_Type = "String"
		Attr_Disptype = "FreeInputNoMatching"
	elif (
		str(SCEQUESItem.DATATYPE) == "NUMBER"
		and SecQuesRecordid != "SYSEFL-PB-00497"
		# Added by VETRI for #A043S001P01-7295 - Start
		and SecQuesRecordid != "SYSEFL-SE-00895"
		# Added by wasim for #A043S001P01-5604 - start
		and SecQuesRecordid != "SYSEFL-SE-00923"
		and SecQuesRecordid != "SYSEFL-TQ-00895"
		# Added by wasim for #A043S001P01-5604 - End
		# Added by VETRI for #A043S001P01-7295 - End
	):
		# elif str(SCEQUESItem.DATATYPE) == "NUMBER" and SecQuesRecordid!="SYSEFL-PB-00497" and SecQuesRecordid !="SYSEFL-SE-00923" and str(SecQuesRecordid) == "SYSEFL-SE-00895" and  str(SecQuesRecordid) == "SYSEFL-TQ-00895" and  str(SecQuesRecordid) =="SYSEFL-OM-00261":
		Attr_Type = "Number"
		Attr_Disptype = "FreeInputNoMatching"
		# RELEASE NOTES FOR A043S001P01-9631
	elif str(SCEQUESItem.DATATYPE) == "DATE":
		Attr_Type = "Date"
		Attr_Disptype = "FreeInputNoMatching"
	elif str(SCEQUESItem.DATATYPE) == "DATE/TIME":
		Attr_Type = "String"
		Attr_Disptype = "FreeInputNoMatching"
	# RELEASE NOTES FOR A043S001P01-9631
	elif str(SCEQUESItem.DATATYPE) == "PICKLIST (MULTI-SELECT)":
		Attr_Type = "UserSelection"
		Attr_Disptype = "CheckBox"
	elif str(SCEQUESItem.DATATYPE) == "CUSTOM OBJECT GRID":
		Attr_Type = "UserSelection"
		Attr_Disptype = "DisplayOnlyText"
	elif str(SCEQUESItem.DATATYPE).strip() == "CONTAINER":
		Attr_Type = "UserSelection"
		Attr_Disptype = "DisplayOnlyText"
	elif str(SCEQUESItem.DATATYPE).strip() == "IMAGE":
		Attr_Type = "UserSelection"
		Attr_Disptype = "FileAttachment"
	elif str(SCEQUESItem.DATATYPE) == "CUSTOM OBJECT FIELD" and SecQuesRecordid != "SYSEFL-PB-00497":
		QuestionCustomObject = ""
		Questiondatatype = Sql.GetFirst(
			"select DATA_TYPE,PICKLIST_VALUES,LOOKUP_API_NAME,PERMISSION,FORMULA_DATA_TYPE FROM SYOBJD (NOLOCK) where OBJECT_NAME='"
			+ str(SCEQUESItem.API_NAME).strip()
			+ "' and API_NAME='"
			+ str(SCEQUESItem.API_FIELD_NAME).strip()
			+ "'"
		)
		if Questiondatatype is not None:
			if (
				str(Questiondatatype.PERMISSION).strip().upper() != "READ ONLY"
				and str(Questiondatatype.DATA_TYPE).strip().upper() == "LOOKUP"
			):
				LookupFiled = "Allow"
			Custom_datatype = str(Questiondatatype.DATA_TYPE).strip()
			if str(Questiondatatype.DATA_TYPE).strip() == "PICKLIST":
				Attr_Type = "UserSelection"
				Attr_Disptype = "DropDown"
			if str(Questiondatatype.DATA_TYPE).strip().upper() == "LOOKUP":
				Attr_Type = "UserSelection"
				Attr_Disptype = "FreeInputNoMatching"
			if str(Questiondatatype.DATA_TYPE) == "AUTO NUMBER":
				Attr_Type = "UserSelection"
				Attr_Disptype = "FreeInputNoMatching"
			elif (
				str(Questiondatatype.DATA_TYPE) == "TEXT"
				or str(Questiondatatype.DATA_TYPE).strip().upper() == "FORMULA"
				or str(Questiondatatype.DATA_TYPE) == "LONG TEXT AREA"
			) and str(Questiondatatype.FORMULA_DATA_TYPE) != "CHECKBOX":
				Attr_Type = "String"
				Attr_Disptype = "FreeInputNoMatching"
			elif str(Questiondatatype.DATA_TYPE) == "CHECKBOX" or str(Questiondatatype.FORMULA_DATA_TYPE) == "CHECKBOX":
				Attr_Type = "UserSelection"
				Attr_Disptype = "CheckBox"
			elif str(Questiondatatype.DATA_TYPE) == "CURRENCY":
				Attr_Type = "String"
				Attr_Disptype = "FreeInputNoMatching"
			elif str(Questiondatatype.DATA_TYPE) in ["NUMBER", "PERCENT"]:
				if str(SCEQUESItem.API_NAME) == "PROGRAM_YEAR" and str(SECQSTNATTRIBUTENAME) == "SYSEFL_TQ_00328":
					Attr_Type = "String"
					Attr_Disptype = "FreeInputNoMatching"
				else:
					Attr_Type = "Number"
					Attr_Disptype = "FreeInputNoMatching"
			# RELEASE NOTES FOR A043S001P01-9631
			elif str(Questiondatatype.DATA_TYPE) == "DATE":
				Attr_Type = "Date"
				Attr_Disptype = "FreeInputNoMatching"
			elif str(Questiondatatype.DATA_TYPE) == "DATE/TIME":
				Attr_Type = "String"
				Attr_Disptype = "FreeInputNoMatching"
			# RELEASE NOTES FOR A043S001P01-9631
			elif str(Questiondatatype.DATA_TYPE) == "PICKLIST (MULTI-SELECT)":
				Attr_Type = "UserSelection"
				Attr_Disptype = "CheckBox"
			elif str(Questiondatatype.DATA_TYPE).strip() == "IMAGE":
				Attr_Type = "UserSelection"
				Attr_Disptype = "FileAttachment"
			if (
				str(Questiondatatype.DATA_TYPE).strip() == "PICKLIST"
				or str(Questiondatatype.DATA_TYPE).strip() == "PICKLIST (MULTI-SELECT)"
				and str(SECQSTNATTRIBUTENAME) != "SYSEFL_TQ_00219"
			):
				try:
					resp_values = Questiondatatype.PICKLIST_VALUES.split(",")
					for i in range(0, len(resp_values)):
						if i == 0:
							Attr_value += (
								"<Value><USEnglish>"
								+ resp_values[i].strip()
								+ "</USEnglish><Preselected>0</Preselected><IsFirstValuePreselected>0</IsFirstValuePreselected></Value>"
							)
						else:
							Attr_value += "<Value><USEnglish>" + resp_values[i].strip() + "</USEnglish></Value>"
				except:
					resp_values = str(Questiondatatype.PICKLIST_VALUES).strip().split(",")
					for i in range(0, len(resp_values)):
						if i == 0:
							Attr_value += (
								"<Value><USEnglish>"
								+ resp_values[i].strip()
								+ "</USEnglish><Preselected>0</Preselected><IsFirstValuePreselected>0</IsFirstValuePreselected></Value>"
							)
						else:
							Attr_value += "<Value><USEnglish>" + resp_values[i].strip() + "</USEnglish></Value>"
		else:
			Attr_Type = "UserSelection"
			Attr_Disptype = "FreeInputNoMatching"
	if (
		(str(SCEQUESItem.DATATYPE) == "PICKLIST" or str(SCEQUESItem.DATATYPE).strip() == "PICKLIST (MULTI-SELECT)")
		and "," in str(SCEQUESItem.PICKLIST)
		and str(SECQSTNATTRIBUTENAME) != "SYSEFL_TQ_00219"
	):
		resp_values = str(SCEQUESItem.PICKLIST).split(",")
		for i in range(0, len(resp_values)):
			if i == 0:
				Attr_value += "<Value><USEnglish>" + resp_values[i] + "</USEnglish><Preselected>0</Preselected></Value>"
			else:
				Attr_value += "<Value><USEnglish>" + resp_values[i] + "</USEnglish></Value>"
	elif str(Custom_datatype) != "PICKLIST" and str(Custom_datatype) != "PICKLIST (MULTI-SELECT)":
		Attr_value = "<Value><USEnglish>" + "1" + "</USEnglish></Value>"
	# Build XML for Attributes
	if (
		str(SCEQUESItem.DATATYPE) != "CONTAINER"
		and str(SCEQUESItem.DATATYPE) != "PICKLIST"
		and str(Custom_datatype) != "PICKLIST"
		and str(Custom_datatype).strip().upper() != "LOOKUP"
		and str(LookupFiled) != "Allow"
		and str(SCEQUESItem.DATATYPE) != "LONG TEXT AREA"
		and str(Custom_datatype) != "LONG TEXT AREA"
	):
		ATTRIBUTES += (
			"<Attribute><AttributeName><USEnglish>QSTN_"
			+ str(SECQSTNATTRIBUTENAME)
			+ "</USEnglish></AttributeName><AttributeType>"
			+ str(Attr_Type)
			+ "</AttributeType><DisplayType>"
			+ str(Attr_Disptype)
			+ "</DisplayType><SpansAcrossEntireRow>1</SpansAcrossEntireRow><Label><USEnglish>"
			+ str(SCEQUESItem.FIELD_LABEL).replace('"', '"')
			+ "</USEnglish></Label><Hint><USEnglish>"
			+ str(SCEQUESItem.HELP_TEXT_TITLE).replace('"', '"')
			+ "</USEnglish></Hint><ShowOneTimePrice>0</ShowOneTimePrice><IsFirstValuePreselected>0</IsFirstValuePreselected><Values>"
			+ str(Attr_value)
			+ "</Values></Attribute>"
		)
		TabAttributes += (
			"<Attribute><Name>QSTN_"
			+ str(SECQSTNATTRIBUTENAME)
			+ "</Name><Rank>"
			+ str(Allcountsec)
			+ "</Rank></Attribute>"
		)
		if str(LOOKUPDISPLAYFIELD) == "Allowed":
			ATTRIBUTES += (
				"<Attribute><AttributeName><USEnglish>QSTN_LKP_"
				+ str(SECQSTNATTRIBUTENAME)
				+ "</USEnglish></AttributeName><AttributeType>UserSelection</AttributeType><DisplayType>Button</DisplayType><ButtonText><USEnglish>Lookup</USEnglish></ButtonText><IsFirstValuePreselected>0</IsFirstValuePreselected><Values><Value><USEnglish>att</USEnglish><Rank>"
				+ str(Allcountsec)
				+ "</Rank><ValueCode>1</ValueCode></Value></Values></Attribute>"
			)
			TabAttributes += (
				"<Attribute><Name>QSTN_LKP_"
				+ str(SECQSTNATTRIBUTENAME)
				+ "</Name><Rank>"
				+ str(Allcountsec)
				+ "</Rank></Attribute>"
			)
	elif (
		str(Custom_datatype).strip().upper() == "LOOKUP"
		and str(LookupFiled) == "Allow"
		and str(SCEQUESItem.DATATYPE) != "LONG TEXT AREA"
		and str(Custom_datatype) != "LONG TEXT AREA"
	):
		ATTRIBUTES += (
			"<Attribute><AttributeName><USEnglish>QSTN_"
			+ str(SECQSTNATTRIBUTENAME)
			+ "</USEnglish></AttributeName><AttributeType>"
			+ str(Attr_Type)
			+ "</AttributeType><DisplayType>"
			+ str(Attr_Disptype)
			+ "</DisplayType><SpansAcrossEntireRow>1</SpansAcrossEntireRow><Label><USEnglish>"
			+ str(SCEQUESItem.FIELD_LABEL).replace('"', '"')
			+ "</USEnglish></Label><Hint><USEnglish>"
			+ str(SCEQUESItem.HELP_TEXT_TITLE).replace('"', '"')
			+ "</USEnglish></Hint><ShowOneTimePrice>0</ShowOneTimePrice><IsFirstValuePreselected>0</IsFirstValuePreselected><Values>"
			+ str(Attr_value)
			+ "</Values></Attribute>"
		)
	elif (
		str(SCEQUESItem.DATATYPE) == "PICKLIST"
		or str(Custom_datatype).strip() == "PICKLIST"
		and str(Custom_datatype).strip().upper() != "LOOKUP"
		and str(LookupFiled) != "Allow"
		and str(SECQSTNATTRIBUTENAME) != "SYSEFL_TQ_00219"
		and str(SCEQUESItem.DATATYPE) != "LONG TEXT AREA"
		and str(Custom_datatype) != "LONG TEXT AREA"
	):
		try:
			if str(SECQSTNATTRIBUTENAME) in ("SYSEFL_PB_01935", "SYSEFL_PB_01919", "SYSEFL_PB_00431"):
				options = ""
				if Questiondatatype is not None:
					for value in Questiondatatype.PICKLIST_VALUES.split(","):
						options += "<option value='" + str(value) + "'>" + str(value) + "</option>"

				ATTRIBUTES += (
					"<Attribute><AttributeName><USEnglish>QSTN_"
					+ str(SECQSTNATTRIBUTENAME)
					+ "</USEnglish></AttributeName><AttributeType>"
					+ str(Attr_Type)
					+ "</AttributeType><DisplayType>"
					+ str(Attr_Disptype)
					+ "</DisplayType><SpansAcrossEntireRow>1</SpansAcrossEntireRow><Label><USEnglish>"
					+ str(SCEQUESItem.FIELD_LABEL).replace('"', '"')
					+ "</USEnglish></Label><Hint><USEnglish><htmlData><![CDATA[<div id = 'div_PICKLISTLOAD_"
					+ str(SECQSTNATTRIBUTENAME)
					+ "' class='multiselect'><select multiple='multiple' class='options_"
					+ str(SECQSTNATTRIBUTENAME)
					+ "'  >"
					+ str(options)
					+ "</select><div id='button_mvmt1'> <button onclick='unselectedval(this)'  class='leftbutton' id='"
					+ str(SECQSTNATTRIBUTENAME)
					+ "'><i class='glyphicon glyphicon-triangle-left'></i></button><button  onclick='selectedval(this)' class='rightbutton' id='"
					+ str(SECQSTNATTRIBUTENAME)
					+ "'><i class='glyphicon glyphicon-triangle-right'></i></button></div> <select multiple='multiple'  id='options1_"
					+ str(SECQSTNATTRIBUTENAME)
					+ "' ></select><div id='button_mvmt'> <button  class='topbutton' onclick='topselect(this)' id='"
					+ str(SECQSTNATTRIBUTENAME)
					+ "'><i class='glyphicon glyphicon-triangle-top'></i></button><button  class='btmbutton' onclick='btmselect(this)' id='"
					+ str(SECQSTNATTRIBUTENAME)
					+ "'><i class='glyphicon glyphicon-triangle-bottom'></i></button></div></div>]]></htmlData></USEnglish></Hint><Values>"
					+ str(Attr_value)
					+ "</Values></Attribute>"
				)
			else:
				ATTRIBUTES += (
					"<Attribute><AttributeName><USEnglish>QSTN_"
					+ str(SECQSTNATTRIBUTENAME)
					+ "</USEnglish></AttributeName><AttributeType>"
					+ str(Attr_Type)
					+ "</AttributeType><DisplayType>"
					+ str(Attr_Disptype)
					+ "</DisplayType><IsRequired>1</IsRequired><SpansAcrossEntireRow>1</SpansAcrossEntireRow><Label><USEnglish>"
					+ str(SCEQUESItem.FIELD_LABEL).replace('"', '"')
					+ "</USEnglish></Label><Hint><USEnglish>"
					+ str(SCEQUESItem.HELP_TEXT_COPY).replace('"', '"')
					+ "</USEnglish></Hint><Values>"
					+ str(Attr_value)
					+ "</Values></Attribute>"
				)
			TabAttributes += (
				"<Attribute><Name>QSTN_"
				+ str(SECQSTNATTRIBUTENAME)
				+ "</Name><Rank>"
				+ str(Allcountsec)
				+ "</Rank></Attribute>"
			)
		except:
			if str(SECQSTNATTRIBUTENAME) in ("SYSEFL_PB_01935", "SYSEFL_PB_01919", "SYSEFL_PB_00431"):
				options = ""
				if Questiondatatype is not None:
					for value in Questiondatatype.PICKLIST_VALUES.split(","):
						options += "<option value='" + str(value) + "'>" + str(value) + "</option>"

				ATTRIBUTES += (
					"<Attribute><AttributeName><USEnglish>QSTN_"
					+ str(SECQSTNATTRIBUTENAME)
					+ "</USEnglish></AttributeName><AttributeType>"
					+ str(Attr_Type)
					+ "</AttributeType><DisplayType>"
					+ str(Attr_Disptype)
					+ "</DisplayType><SpansAcrossEntireRow>1</SpansAcrossEntireRow><Label><USEnglish>"
					+ str(SCEQUESItem.FIELD_LABEL).replace('"', '"')
					+ "</USEnglish></Label><Hint><USEnglish><htmlData><![CDATA[<div id = 'div_PICKLISTLOAD_"
					+ str(SECQSTNATTRIBUTENAME)
					+ "' class='multiselect'><select multiple='multiple' class='options_"
					+ str(SECQSTNATTRIBUTENAME)
					+ "'>"
					+ str(options)
					+ "</select><div id='button_mvmt1'> <button onclick='unselectedval(this)' class='leftbutton' id='"
					+ str(SECQSTNATTRIBUTENAME)
					+ "'><i class='glyphicon glyphicon-triangle-left'></i></button><button onclick='selectedval(this)' class='rightbutton' id='"
					+ str(SECQSTNATTRIBUTENAME)
					+ "'><i class='glyphicon glyphicon-triangle-right'></i></button></div> <select multiple='multiple'  id='options1_"
					+ str(SECQSTNATTRIBUTENAME)
					+ "'></select><div id='button_mvmt'> <button onclick='topselect(this)' id='"
					+ str(SECQSTNATTRIBUTENAME)
					+ "'><i class='glyphicon glyphicon-triangle-top'></i></button><button onclick='btmselect(this)' id='"
					+ str(SECQSTNATTRIBUTENAME)
					+ "'><i class='glyphicon glyphicon-triangle-bottom'></i></button></div></div>]]></htmlData></USEnglish></Hint><Values>"
					+ Attr_value
					+ "</Values></Attribute>"
				)
			else:
				ATTRIBUTES += (
					"<Attribute><AttributeName><USEnglish>QSTN_"
					+ str(SECQSTNATTRIBUTENAME)
					+ "</USEnglish></AttributeName><AttributeType>"
					+ str(Attr_Type)
					+ "</AttributeType><DisplayType>"
					+ str(Attr_Disptype)
					+ "</DisplayType><IsRequired>1</IsRequired><SpansAcrossEntireRow>1</SpansAcrossEntireRow><Label><USEnglish>"
					+ str(SCEQUESItem.FIELD_LABEL).replace('"', '"')
					+ "</USEnglish></Label><Hint><USEnglish>"
					+ str(SCEQUESItem.HELP_TEXT_COPY).replace('"', '"')
					+ "</USEnglish></Hint><Values>"
					+ Attr_value
					+ "</Values></Attribute>"
				)
			TabAttributes += (
				"<Attribute><Name>QSTN_"
				+ str(SECQSTNATTRIBUTENAME)
				+ "</Name><Rank>"
				+ str(Allcountsec)
				+ "</Rank></Attribute>"
			)
	elif (
		str(SCEQUESItem.DATATYPE) == "PICKLIST"
		or str(Custom_datatype).strip() == "PICKLIST"
		and str(SECQSTNATTRIBUTENAME) == "SYSEFL_TQ_00219"
		and str(SCEQUESItem.DATATYPE) != "LONG TEXT AREA"
		and str(Custom_datatype) != "LONG TEXT AREA"
	):
		ATTRIBUTES += (
			"<Attribute><AttributeName><USEnglish>QSTN_"
			+ str(SECQSTNATTRIBUTENAME)
			+ "</USEnglish></AttributeName><AttributeType>"
			+ str(Attr_Type)
			+ "</AttributeType><DisplayType>"
			+ str(Attr_Disptype)
			+ "</DisplayType><IsRequired>1</IsRequired><SpansAcrossEntireRow>1</SpansAcrossEntireRow><Label><USEnglish>"
			+ str(SCEQUESItem.FIELD_LABEL).replace('"', '"')
			+ "</USEnglish></Label><Hint><USEnglish>"
			+ str(SCEQUESItem.HELP_TEXT_COPY).replace('"', '"')
			+ "</USEnglish></Hint><Values><Value><USEnglish>"
			+ "$"
			+ "</USEnglish></Value></Values></Attribute>"
		)
		TabAttributes += (
			"<Attribute><Name>QSTN_"
			+ str(SECQSTNATTRIBUTENAME)
			+ "</Name><Rank>"
			+ str(Allcountsec)
			+ "</Rank></Attribute>"
		)
	elif (
		str(LookupFiled) != "Allow"
		and str(SCEQUESItem.DATATYPE) != "LONG TEXT AREA"
		and str(Custom_datatype) != "LONG TEXT AREA"
	):
		ATTRIBUTES += (
			"<Attribute><AttributeName><USEnglish>CTR_"
			+ str(SECQSTNATTRIBUTENAME)
			+ "</USEnglish></AttributeName><AttributeType>"
			+ str(Attr_Type)
			+ "</AttributeType><DisplayType>"
			+ str(Attr_Disptype)
			+ "</DisplayType><SpansAcrossEntireRow>1</SpansAcrossEntireRow><Label><USEnglish>"
			+ str(SCEQUESItem.FIELD_LABEL).replace('"', '"')
			+ "</USEnglish></Label><Hint><USEnglish>"
			+ str(SCEQUESItem.HELP_TEXT_COPY).replace('"', '"')
			+ "</USEnglish></Hint><ShowOneTimePrice>0</ShowOneTimePrice><IsFirstValuePreselected>0</IsFirstValuePreselected><Values>"
			+ str(Attr_value)
			+ "</Values></Attribute>"
		)
		TabAttributes += (
			"<Attribute><Name>CTR_"
			+ str(SECQSTNATTRIBUTENAME)
			+ "</Name><Rank>"
			+ str(Allcountsec)
			+ "</Rank></Attribute>"
		)
	elif str(SCEQUESItem.DATATYPE) == "LONG TEXT AREA" or str(Custom_datatype) == "LONG TEXT AREA":
		ATTRIBUTES += (
			"<Attribute><AttributeName><USEnglish>QSTN_"
			+ str(SECQSTNATTRIBUTENAME)
			+ "_LONG</USEnglish></AttributeName><AttributeType>"
			+ str(Attr_Type)
			+ "</AttributeType><DisplayType>"
			+ str(Attr_Disptype)
			+ "</DisplayType><SpansAcrossEntireRow>1</SpansAcrossEntireRow><Label><USEnglish>"
			+ str(SCEQUESItem.FIELD_LABEL).replace('"', '"')
			+ "</USEnglish></Label><Hint><USEnglish>"
			+ str(SCEQUESItem.HELP_TEXT_COPY).replace('"', '"')
			+ "</USEnglish></Hint><Values><Value><USEnglish>"
			+ "$"
			+ "</USEnglish></Value></Values></Attribute>"
		)
		TabAttributes += (
			"<Attribute><Name>QSTN_"
			+ str(SECQSTNATTRIBUTENAME)
			+ "_LONG</Name><Rank>"
			+ str(Allcountsec)
			+ "</Rank></Attribute>"
		)
# SUBSECTION RECORD GET:
"""SUBSectionRecord = Sql.GetList(
	"select top 1000 SAPCPQ_ATTRIBUTE_NAME,RECORD_ID,SECTION_NAME,DISPLAY_ORDER,ATTRIBUTE_NAME,DEFAULT_BANNER_COLOR,ERROR_BANNER_COLOR,PARENT_SECTION_RECORD_ID,PARENT_SECTION_NAME,TAB_RECORD_ID,TAB_NAME FROM SYSECT (NOLOCK) where PARENT_SECTION_RECORD_ID='"
	+ str(SecRecordid)
	+ "' ORDER BY DISPLAY_ORDER"
)"""
SUBSectionRecord = Sql.GetList(
	"select top 1000 SYSECT.SAPCPQ_ATTRIBUTE_NAME,SYSECT.RECORD_ID,SYSECT.SECTION_NAME,SYSECT.DISPLAY_ORDER,SYSECT.DEFAULT_BANNER_COLOR,SYSECT.ERROR_BANNER_COLOR,SYSECT.PARENT_SECTION_RECORD_ID,SYSECT.PARENT_SECTION_TEXT,SYPAGE.TAB_RECORD_ID,SYPAGE.TAB_NAME FROM SYSECT INNER JOIN SYPAGE (NOLOCK) on SYSECT.PAGE_RECORD_ID = SYPAGE.RECORD_ID where SYSECT.PARENT_SECTION_RECORD_ID='"
	+ str(SecRecordid)
	+ "' ORDER BY SYSECT.DISPLAY_ORDER"
)
"""SectionRecord = Sql.GetList(
	"select top 1000 SYSECT.PRIMARY_OBJECT_NAME,SYSECT.RECORD_ID,SYSECT.SAPCPQ_ATTRIBUTE_NAME,SYSECT.PAGE_RECORD_ID,SYPAGE.TAB_RECORD_ID FROM SYSECT (NOLOCK) INNER JOIN SYPAGE (NOLOCK) on SYSECT.PAGE_RECORD_ID = SYPAGE.RECORD_ID where SYPAGE.TAB_RECORD_ID='"
	+ str(TabRecordNo)
	+ "' and SYSECT.PARENT_SECTION_RECORD_ID=''  ORDER BY abs(SYSECT.DISPLAY_ORDER)"
)"""
for SubsecItem in SUBSectionRecord:
	TabAttributes += BuildSectionAttributes(SubsecItem)
return TabAttributes


def BuildPivotTabe(TabName, pivotRank):
global ATTRIBUTES
TabAttributes = ""

if str(TabName) == "Attribute":

	ATTRIBUTES += (
		"<Attribute><AttributeName><USEnglish>CTR_ATTRIBUTES_PIVOT_TABLE</USEnglish></AttributeName><AttributeType>Container</AttributeType><DisplayType>Container</DisplayType><SpansAcrossEntireRow>1</SpansAcrossEntireRow><Label><USEnglish>MATERIALS WITH ATTRIBUTES</USEnglish></Label><Values><Value><USEnglish>"
		+ "1"
		+ "</USEnglish></Value></Values></Attribute>"
	)
	TabAttributes += "<Attribute><Name>CTR_ATTRIBUTES_PIVOT_TABLE</Name><Rank>" + str(pivotRank) + "</Rank></Attribute>"

if str(TabName) == "Set":

	ATTRIBUTES += (
		"<Attribute><AttributeName><USEnglish>CTR_SET_ATTRIBUTE_PIVOT_TABLE</USEnglish></AttributeName><AttributeType>Container</AttributeType><DisplayType>Container</DisplayType><SpansAcrossEntireRow>1</SpansAcrossEntireRow><Label><USEnglish>SET ATTRIBUTE MATERIALS</USEnglish></Label><Values><Value><USEnglish>"
		+ "1"
		+ "</USEnglish></Value></Values></Attribute>"
	)
	TabAttributes += (
		"<Attribute><Name>CTR_SET_ATTRIBUTE_PIVOT_TABLE</Name><Rank>" + str(pivotRank) + "</Rank></Attribute>"
	)
return TabAttributes


def BuildRelatedListAttributes(TabRecordNo):
global ATTRIBUTES
global ATTRIBUTESLIST
ATTRIBUTESLIST = []
SEC_RELATED_TabAttributes = ""
SYOBJR_TabAttributes = ""
TabAttributes = ""
Counted = 2170
rl_row = {}
SectionRecords = Sql.GetList(
	"select top 1000 SYSECT.PRIMARY_OBJECT_RECORD_ID FROM SYSECT (NOLOCK) INNER JOIN SYPAGE (NOLOCK) on SYSECT.PAGE_RECORD_ID = SYPAGE.RECORD_ID where SYPAGE.TAB_RECORD_ID='"
	+ str(TabRecordNo)
	+ "' and SYSECT.PARENT_SECTION_RECORD_ID=''"
)
ModCode = TabRecordNo.split("-")[1]
'''ModRecords = Sql.GetList(
	"select top 1000 TAB_LABEL FROM SYTABS (NOLOCK) where SAPCPQ_ATTRIBUTE_NAME like '%" + str(ModCode) + "%'"
)'''
ModRecords = Sql.GetList("select top 1000 TAB_LABEL FROM SYTABS (NOLOCK) where RECORD_ID ='"+ str(TabRecordNo) + "'")
ModTabList = [ins.TAB_LABEL for ins in ModRecords]
#SYTBRLInfoData = Sql.GetTable("SYTBRL")
for SecItem in SectionRecords:
	if str(SecItem.PRIMARY_OBJECT_RECORD_ID) != "":
		''''ATTRIBUTES += "<Attribute><AttributeName><USEnglish>SEC_RELATED_LIST_TEST</USEnglish></AttributeName><AttributeType>String</AttributeType><DisplayType>DisplayOnlyText</DisplayType><SpansAcrossEntireRow>1</SpansAcrossEntireRow><Label><USEnglish>RELATED_LIST</USEnglish></Label><Hint><USEnglish><![CDATA[<div>RELATED LISTS</div>]]></USEnglish></Hint><ShowOneTimePrice>0</ShowOneTimePrice><IsFirstValuePreselected>0</IsFirstValuePreselected><Values><Value><USEnglish>RELATED LISTS</USEnglish></Value></Values></Attribute>"'''
		SYOBJR_RecordS = Sql.GetList(
			"select top 1000 NAME,SAPCPQ_ATTRIBUTE_NAME, CAN_ADD, OBJ_REC_ID FROM SYOBJR (NOLOCK) where PARENT_LOOKUP_REC_ID='"
			+ str(SecItem.PRIMARY_OBJECT_RECORD_ID)
			+ "'and VISIBLE = 1 ORDER BY ABS(DISPLAY_ORDER)"
		)
		if SYOBJR_RecordS is not None:
			SYOBJR_RecordSCount = len([invs.NAME for invs in SYOBJR_RecordS]) - 1
			ObjR_str1 = ""
			ObjR_str = ""
			ObjR_str2 = ""
			ObjR_strs = ""
			ObjR_str3 = ""
			ObjR_strs1 = ""
			ObjR_str4 = ""
			ObjR_strs2 = ""
			Objhobj = ""
			ObjR_str5 = ""
			ObjR_strs3 = ""
			for key, SYOBJR_REC in enumerate(SYOBJR_RecordS):
				Counted = Counted + 1
				SYOBJR_NAME = ""
				SYOBJR_NAME = ""
				ObjTab = ""
				product_id = ""
				TabNameRE = ""
				product_name = ""
				MMSEC_TAB = ""
				OBJ_LST = ["PASACS"]
				SYOBJH_OBJ = Sql.GetFirst(
					"select OBJECT_NAME from SYOBJH (NOLOCK) where RECORD_ID = '" + str(SYOBJR_REC.OBJ_REC_ID) + "'"
				)
				if SYOBJH_OBJ is not None and SYOBJH_OBJ != "":
					if str(SYOBJH_OBJ.OBJECT_NAME) is not None and str(SYOBJH_OBJ.OBJECT_NAME) != "":
						Objhobj = str(SYOBJH_OBJ.OBJECT_NAME)

				if str(Objhobj) not in OBJ_LST:
					MMSEC_TAB = Sql.GetFirst(
						"select SYPAGE.TAB_NAME,SYPAGE.TAB_RECORD_ID from SYSECT (NOLOCK) INNER JOIN SYPAGE (NOLOCK) on SYSECT.PAGE_RECORD_ID = SYPAGE.RECORD_ID where SYSECT.PRIMARY_OBJECT_NAME = '"
						+ str(Objhobj)
						+ "' and SYSECT.SECTION_NAME='BASIC INFORMATION'"
					)
					if MMSEC_TAB is not None and MMSEC_TAB != "":
						ObjTab = str(MMSEC_TAB.TAB_NAME)
				SYOBJR_NAME = "div_CTR_" + str(SYOBJR_REC.NAME).replace(" ", "_")
				SYOBJR_NAMES = (
					"ADDNEW__"
					+ str(SYOBJR_REC.SAPCPQ_ATTRIBUTE_NAME).replace("-", "_")
					+ "_"
					+ str(SYOBJR_REC.OBJ_REC_ID).replace("-", "_")
				)
				library_str = ""
				if key == SYOBJR_RecordSCount:
					if str(ObjR_strs) is not None:
						if (
							str(SYOBJR_REC.SAPCPQ_ATTRIBUTE_NAME).strip() == "SYOBJR-60071"
							or str(SYOBJR_REC.SAPCPQ_ATTRIBUTE_NAME).strip() == "SYOBJR-60062"
						):
							ObjR_str2 += (
								"function Materialpers123 () {"
								+ " "
								+ str(ObjR_strs)
								+ " "
								+ "loadRelatedList('"
								+ str(SYOBJR_REC.SAPCPQ_ATTRIBUTE_NAME)
								+ "','"
								+ str(SYOBJR_NAME)
								+ "'); }"
							)
						else:
							ObjR_str2 += "function Materialpers123 () {" + " " + str(ObjR_strs) + " }"
					if str(ObjR_strs1) is not None:
						if (
							str(SYOBJR_REC.SAPCPQ_ATTRIBUTE_NAME).strip() == "SYOBJR-20005"
							or str(SYOBJR_REC.SAPCPQ_ATTRIBUTE_NAME).strip() == "SYOBJR-30500"
						):
							ObjR_str3 += (
								"function Setsattr () {"
								+ " "
								+ str(ObjR_strs1)
								+ " "
								+ "loadRelatedList('"
								+ str(SYOBJR_REC.SAPCPQ_ATTRIBUTE_NAME)
								+ "','"
								+ str(SYOBJR_NAME)
								+ "'); }"
							)
						else:
							ObjR_str3 += "function Setsattr () {" + " " + str(ObjR_strs1) + " }"
					if str(ObjR_strs2) is not None:
						if (
							str(SYOBJR_REC.SAPCPQ_ATTRIBUTE_NAME).strip() == "SYOBJR-70112"
							or str(SYOBJR_REC.SAPCPQ_ATTRIBUTE_NAME).strip() == "SYOBJR-60080"
						):
							ObjR_str4 += (
								"function Plantsattr () {"
								+ " "
								+ str(ObjR_strs2)
								+ " "
								+ "loadRelatedList('"
								+ str(SYOBJR_REC.SAPCPQ_ATTRIBUTE_NAME)
								+ "','"
								+ str(SYOBJR_NAME)
								+ "'); }"
							)
						else:
							ObjR_str4 += "function Plantsattr () {" + " " + str(ObjR_strs2) + " }"
					if str(ObjR_strs3) is not None:
						if str(SYOBJR_REC.SAPCPQ_ATTRIBUTE_NAME).strip() == "SYOBJR-70113":
							ObjR_str5 += (
								"function Materialattr123 () {"
								+ " "
								+ str(ObjR_strs3)
								+ " "
								+ "loadRelatedList('"
								+ str(SYOBJR_REC.SAPCPQ_ATTRIBUTE_NAME)
								+ "','"
								+ str(SYOBJR_NAME)
								+ "'); }"
							)
						else:
							ObjR_str5 += "function Materialattr123 () {" + " " + str(ObjR_strs3) + " }"
					'''if (
						str(SYOBJR_REC.SAPCPQ_ATTRIBUTE_NAME).strip() != "SYOBJR-70113"
						and str(SYOBJR_REC.SAPCPQ_ATTRIBUTE_NAME).strip() != "SYOBJR-60071"
						and str(SYOBJR_REC.SAPCPQ_ATTRIBUTE_NAME).strip() != "SYOBJR-60062"
						and str(SYOBJR_REC.SAPCPQ_ATTRIBUTE_NAME).strip() != "SYOBJR-20005"
						and str(SYOBJR_REC.SAPCPQ_ATTRIBUTE_NAME).strip() != "SYOBJR-30500"
						and str(SYOBJR_REC.SAPCPQ_ATTRIBUTE_NAME).strip() != "SYOBJR-70112"
						and str(SYOBJR_REC.SAPCPQ_ATTRIBUTE_NAME).strip() != "SYOBJR-60080"
					):
						ObjR_str1 += (
							"function MaterialTest1234 () {"
							+ " "
							+ str(ObjR_str)
							+ " "
							+ "loadRelatedList('"
							+ str(SYOBJR_REC.SAPCPQ_ATTRIBUTE_NAME)
							+ "','"
							+ str(SYOBJR_NAME)
							+ "'); } "
						)
						rl_row["TABRECID"] = TabRecordNo
						rl_row["RELATED_LIST_HINT"] = ObjR_str1
						#Table.TableActions.Create("SYTBRL", rl_row)
						ObjR_str1 = (
							"<* TABLE ( select top 1 RELATED_LIST_HINT from SYTBRL (NOLOCK) where TABRECID = '"
							+ str(TabRecordNo)
							+ "' order by CpqTableEntryId desc ) *>"
						)
					elif str(ObjR_str) != "":
						ObjR_str1 += "function MaterialTest1234 () {" + str(ObjR_str) + " } "
						rl_row["TABRECID"] = TabRecordNo
						rl_row["RELATED_LIST_HINT"] = ObjR_str1
						Table.TableActions.Create("SYTBRL", rl_row)
						ObjR_str1 = (
							"<* TABLE ( select top 1 RELATED_LIST_HINT from SYTBRL (NOLOCK) where TABRECID = '"
							+ str(TabRecordNo)
							+ "' order by CpqTableEntryId desc ) *>"
						)'''
				else:
					if (
						str(SYOBJR_REC.SAPCPQ_ATTRIBUTE_NAME).strip() == "SYOBJR-60071"
						or str(SYOBJR_REC.SAPCPQ_ATTRIBUTE_NAME).strip() == "SYOBJR-60062"
					):
						ObjR_strs += (
							"loadRelatedList('"
							+ str(SYOBJR_REC.SAPCPQ_ATTRIBUTE_NAME)
							+ "','"
							+ str(SYOBJR_NAME)
							+ "');"
							+ " "
						)
					elif (
						str(SYOBJR_REC.SAPCPQ_ATTRIBUTE_NAME).strip() == "SYOBJR-20005"
						or str(SYOBJR_REC.SAPCPQ_ATTRIBUTE_NAME).strip() == "SYOBJR-30500"
					):
						ObjR_strs1 += (
							"loadRelatedList('"
							+ str(SYOBJR_REC.SAPCPQ_ATTRIBUTE_NAME)
							+ "','"
							+ str(SYOBJR_NAME)
							+ "');"
							+ " "
						)
					elif (
						str(SYOBJR_REC.SAPCPQ_ATTRIBUTE_NAME).strip() == "SYOBJR-70112"
						or str(SYOBJR_REC.SAPCPQ_ATTRIBUTE_NAME).strip() == "SYOBJR-60080"
					):
						ObjR_strs2 += (
							"loadRelatedList('"
							+ str(SYOBJR_REC.SAPCPQ_ATTRIBUTE_NAME)
							+ "','"
							+ str(SYOBJR_NAME)
							+ "');"
							+ " "
						)
					elif str(SYOBJR_REC.SAPCPQ_ATTRIBUTE_NAME).strip() == "SYOBJR-70113":
						ObjR_strs3 += (
							"loadRelatedList('"
							+ str(SYOBJR_REC.SAPCPQ_ATTRIBUTE_NAME)
							+ "','"
							+ str(SYOBJR_NAME)
							+ "');"
							+ " "
						)
					elif (
						str(SYOBJR_REC.SAPCPQ_ATTRIBUTE_NAME).strip() != "SYOBJR-70113"
						and str(SYOBJR_REC.SAPCPQ_ATTRIBUTE_NAME).strip() != "SYOBJR-60071"
						and str(SYOBJR_REC.SAPCPQ_ATTRIBUTE_NAME).strip() != "SYOBJR-60062"
						and str(SYOBJR_REC.SAPCPQ_ATTRIBUTE_NAME).strip() != "SYOBJR-20005"
						and str(SYOBJR_REC.SAPCPQ_ATTRIBUTE_NAME).strip() != "SYOBJR-30500"
						and str(SYOBJR_REC.SAPCPQ_ATTRIBUTE_NAME).strip() != "SYOBJR-70112"
						and str(SYOBJR_REC.SAPCPQ_ATTRIBUTE_NAME).strip() != "SYOBJR-60080"
					):
						ObjR_str += (
							"loadRelatedList('"
							+ str(SYOBJR_REC.SAPCPQ_ATTRIBUTE_NAME)
							+ "','"
							+ str(SYOBJR_NAME)
							+ "');"
							+ " "
						)
				if str(SYOBJR_REC.CAN_ADD).upper() == "TRUE":
					if ObjTab != "":
						if ObjTab in ModTabList:
							TabNameRE = str(ObjTab)
						else:
							product_name = Sql.GetFirst(
								"select APP_LABEL from SYTABS (NOLOCK) where SAPCPQ_ATTRIBUTE_NAME='"
								+ str(MMSEC_TAB.TAB_RECORD_ID).strip()
								+ "'"
							)
							if product_name is not None:
								module_txt = str(product_name.APP_LABEL).strip()
								product_id = Sql.GetFirst(
									"select PRODUCT_ID from products (NOLOCK) where PRODUCT_NAME = '"
									+ str(module_txt)
									+ "'"
								)
							if product_id != "" and product_id is not None:
								TabNameRE = str(ObjTab) + "," + str(product_id.PRODUCT_ID)

						# A043S001P01-5893 - Start
						"""
						In Segment, 'Award Materials' Node --> Need to add ACTIVE ALL and DEACTIVE ALL buttons in 'FULFILLMENT FEES' container
						"""
						if str(SYOBJR_REC.SAPCPQ_ATTRIBUTE_NAME).strip() == "SYOBJR-90027":
							active_all_btn_id = (
								"ACTIVEALL__"
								+ str(SYOBJR_REC.SAPCPQ_ATTRIBUTE_NAME).replace("-", "_")
								+ "_"
								+ str(SYOBJR_REC.OBJ_REC_ID).replace("-", "_")
							)
							deactive_all_btn_id = (
								"DEACTIVEALL__"
								+ str(SYOBJR_REC.SAPCPQ_ATTRIBUTE_NAME).replace("-", "_")
								+ "_"
								+ str(SYOBJR_REC.OBJ_REC_ID).replace("-", "_")
							)
							ATTRIBUTES += (
								"<Attribute><AttributeName><USEnglish>QSTN_R_"
								+ str(SYOBJR_REC.SAPCPQ_ATTRIBUTE_NAME).replace("-", "_")
								+ "</USEnglish></AttributeName><AttributeType>UserSelection</AttributeType><DisplayType>DisplayOnlyText</DisplayType><SpansAcrossEntireRow>1</SpansAcrossEntireRow><Label><USEnglish>"
								+ str(SYOBJR_REC.NAME)
								+ '</USEnglish></Label><Hint><USEnglish><![CDATA[<div class="container_banner_inner_sec"><span id="container_banner_id">'
								+ str(SYOBJR_REC.NAME)
								+ '</span><div class="dropdown flt_lt"><i data-toggle="dropdown" class="fa fa-sort-desc"></i><ul class="dropdown-menu"><li><button  id = \''
								+ str(SYOBJR_NAMES)
								+ "' onclick=\"cont_RL_openaddnew_product('"
								+ str(TabNameRE)
								+ '\')" class="btnstyle addNewRel">ADD NEW</button></li><li><button  id = \''
								+ str(active_all_btn_id)
								+ "' onclick=\"awd_mtrl_actv_and_deactv_all_fulfillment_fees('ACTIVE', '"
								+ str(TabNameRE)
								+ '\')" class="btnstyle">ACTIVATE</button></li><li><button  id = \''
								+ str(deactive_all_btn_id)
								+ "' onclick=\"awd_mtrl_actv_and_deactv_all_fulfillment_fees('DEACTIVE','"
								+ str(TabNameRE)
								+ '\')" class="btnstyle">DEACTIVATE</button></li></ul></div></div><div id = \''
								+ str(SYOBJR_NAME)
								+ '\' class="container ctrstyle2"></div><script type="text/javascript">'
							)
						else:
							# A043S001P01-5893 - End
							ATTRIBUTES += (
								"<Attribute><AttributeName><USEnglish>QSTN_R_"
								+ str(SYOBJR_REC.SAPCPQ_ATTRIBUTE_NAME).replace("-", "_")
								+ "</USEnglish></AttributeName><AttributeType>UserSelection</AttributeType><DisplayType>DisplayOnlyText</DisplayType><SpansAcrossEntireRow>1</SpansAcrossEntireRow><Label><USEnglish>"
								+ str(SYOBJR_REC.NAME)
								+ '</USEnglish></Label><Hint><USEnglish><![CDATA[<div class="container_banner_inner_sec"><span id="container_banner_id">'
								+ str(SYOBJR_REC.NAME)
								+ '</span><div class="dropdown flt_lt"><i data-toggle="dropdown" class="fa fa-sort-desc"></i><ul class="dropdown-menu"><li><button  id = \''
								+ str(SYOBJR_NAMES)
								+ "' onclick=\"cont_RL_openaddnew_product('"
								+ str(TabNameRE)
								+ '\')" class="btnstyle addNewRel">ADD NEW</button></li></ul></div></div><div id = \''
								+ str(SYOBJR_NAME)
								+ '\' class="container ctrstyle2"></div><script type="text/javascript">'
							)

						ATTRIBUTES += str(ObjR_str1)

						ATTRIBUTES += str(ObjR_str2)

						ATTRIBUTES += str(ObjR_str3)
						ATTRIBUTES += str(ObjR_str4)
						ATTRIBUTES += str(ObjR_str5)
						ATTRIBUTES += (
							"</script>]]></USEnglish></Hint><ShowOneTimePrice>0</ShowOneTimePrice><IsFirstValuePreselected>0</IsFirstValuePreselected><Values><Value><USEnglish>"
							+ "1"
							+ "</USEnglish><IsFirstValuePreselected>0</IsFirstValuePreselected></Value></Values></Attribute>"
						)
					else:
						GettreeEnable = Sql.GetFirst(
							"select ENABLE_TREE FROM SYTABS (NOLOCK) where RECORD_ID='" + str(TabRecordNo) + "'"
						)
						if (
							(GettreeEnable is not None and str(GettreeEnable.ENABLE_TREE).upper() == "TRUE")
							or TabRecordNo == "SYTABS-MA-00019"
							or TabRecordNo == "SYTABS-PB-00003"
							or TabRecordNo == "SYTABS-SE-00014"
						) and SYOBJR_REC.SAPCPQ_ATTRIBUTE_NAME not in [
							"SYOBJR-30118",
							"SYOBJR-90004",
							"SYOBJR-93182",
							"SYOBJR-80012",
							"SYOBJR-93144",
						]:
							ATTRIBUTES += (
								"<Attribute><AttributeName><USEnglish>QSTN_R_"
								+ str(SYOBJR_REC.SAPCPQ_ATTRIBUTE_NAME).replace("-", "_")
								+ "</USEnglish></AttributeName><AttributeType>UserSelection</AttributeType><DisplayType>DisplayOnlyText</DisplayType><SpansAcrossEntireRow>1</SpansAcrossEntireRow><Label><USEnglish>"
								+ str(SYOBJR_REC.NAME)
								+ '</USEnglish></Label><Hint><USEnglish><![CDATA[<div class="container_banner_inner_sec"><span id="container_banner_id">'
								+ str(SYOBJR_REC.NAME)
								+ '</span><div class="dropdown flt_lt"><i data-toggle="dropdown" class="fa fa-sort-desc"></i><ul class="dropdown-menu"><li><button  id = \''
								+ str(SYOBJR_NAMES)
								+ "' onclick=\"cont_openaddnew(this, '"
								+ str(SYOBJR_NAME)
								+ '\')" class="btnstyle addNewRel">ADD NEW</button></li><li class="del_list_new" style="display:none;"><button  id = \'delete_'
								+ str(SYOBJR_NAMES)
								+ '\' class="btnstyle addNewRel del_list_new" disabled onclick="relateListBulkDelete(this)" data-target="#related_delete_POPUP" data-toggle="modal" >DELETE</button></li></ul></div></div><div id = \''
								+ str(SYOBJR_NAME)
								+ '\' class="container ctrstyle2"></div><script type="text/javascript">'
							)
						else:
							# A043S001P01-5893 - Start
							if str(SYOBJR_REC.SAPCPQ_ATTRIBUTE_NAME).strip() == "SYOBJR-90027":
								active_all_btn_id = (
									"ACTIVEALL__"
									+ str(SYOBJR_REC.SAPCPQ_ATTRIBUTE_NAME).replace("-", "_")
									+ "_"
									+ str(SYOBJR_REC.OBJ_REC_ID).replace("-", "_")
								)
								deactive_all_btn_id = (
									"DEACTIVEALL__"
									+ str(SYOBJR_REC.SAPCPQ_ATTRIBUTE_NAME).replace("-", "_")
									+ "_"
									+ str(SYOBJR_REC.OBJ_REC_ID).replace("-", "_")
								)
								ATTRIBUTES += (
									"<Attribute><AttributeName><USEnglish>QSTN_R_"
									+ str(SYOBJR_REC.SAPCPQ_ATTRIBUTE_NAME).replace("-", "_")
									+ "</USEnglish></AttributeName><AttributeType>UserSelection</AttributeType><DisplayType>DisplayOnlyText</DisplayType><SpansAcrossEntireRow>1</SpansAcrossEntireRow><Label><USEnglish>"
									+ str(SYOBJR_REC.NAME)
									+ '</USEnglish></Label><Hint><USEnglish><![CDATA[<div class="container_banner_inner_sec"><span id="container_banner_id">'
									+ str(SYOBJR_REC.NAME)
									+ '</span><div class="dropdown flt_lt"><i data-toggle="dropdown" class="fa fa-sort-desc"></i><ul class="dropdown-menu"><li><button  id = \''
									+ str(SYOBJR_NAMES)
									+ '\' onclick="cont_openaddnew(this,\'\')" class="btnstyle addNewRel" data-target="#cont_viewModalSection"  data-toggle="modal">ADD NEW</button></li><li class="del_list_new" style="display:none;"><button  id = \'delete_'
									+ str(SYOBJR_NAMES)
									+ '\' class="btnstyle addNewRel del_list_new" disabled onclick="relateListBulkDelete(this)" data-target="#related_delete_POPUP" data-toggle="modal" >DELETE</button></li><li><button  id = \''
									+ str(active_all_btn_id)
									+ "' onclick=\"awd_mtrl_actv_and_deactv_all_fulfillment_fees('ACTIVE', '"
									+ str(TabNameRE)
									+ '\')" class="btnstyle">ACTIVATE</button></li><li><button  id = \''
									+ str(deactive_all_btn_id)
									+ "' onclick=\"awd_mtrl_actv_and_deactv_all_fulfillment_fees('DEACTIVE','"
									+ str(TabNameRE)
									+ '\')" class="btnstyle">DEACTIVATE</button></li></ul></div></div><div id = \''
									+ str(SYOBJR_NAME)
									+ '\' class="container ctrstyle2"></div><script type="text/javascript">'
								)
							else:
								# A043S001P01-5893 - End
								ATTRIBUTES += (
									"<Attribute><AttributeName><USEnglish>QSTN_R_"
									+ str(SYOBJR_REC.SAPCPQ_ATTRIBUTE_NAME).replace("-", "_")
									+ "</USEnglish></AttributeName><AttributeType>UserSelection</AttributeType><DisplayType>DisplayOnlyText</DisplayType><SpansAcrossEntireRow>1</SpansAcrossEntireRow><Label><USEnglish>"
									+ str(SYOBJR_REC.NAME)
									+ '</USEnglish></Label><Hint><USEnglish><![CDATA[<div class="container_banner_inner_sec"><span id="container_banner_id">'
									+ str(SYOBJR_REC.NAME)
									+ '</span><div class="dropdown flt_lt"><i data-toggle="dropdown" class="fa fa-sort-desc"></i><ul class="dropdown-menu"><li><button  id = \''
									+ str(SYOBJR_NAMES)
									+ '\' onclick="cont_openaddnew(this,\'\')" class="btnstyle addNewRel" data-target="#cont_viewModalSection"  data-toggle="modal">ADD NEW</button></li><li class="del_list_new" style="display:none;"><button  id = \'delete_'
									+ str(SYOBJR_NAMES)
									+ '\' class="btnstyle addNewRel del_list_new" disabled onclick="relateListBulkDelete(this)" data-target="#related_delete_POPUP" data-toggle="modal" >DELETE</button></li></ul></div></div><div id = \''
									+ str(SYOBJR_NAME)
									+ '\' class="container ctrstyle2"></div><script type="text/javascript">'
								)

						ATTRIBUTES += str(ObjR_str1)
						ATTRIBUTES += str(ObjR_str2)
						ATTRIBUTES += str(ObjR_str3)
						ATTRIBUTES += str(ObjR_str4)
						ATTRIBUTES += str(ObjR_str5)
						ATTRIBUTES += (
							"</script>]]></USEnglish></Hint><ShowOneTimePrice>0</ShowOneTimePrice><IsFirstValuePreselected>0</IsFirstValuePreselected><Values><Value><USEnglish>"
							+ "1"
							+ "</USEnglish><IsFirstValuePreselected>0</IsFirstValuePreselected></Value></Values></Attribute>"
						)
				else:
					# A043S001P01-5893 - Start
					if str(SYOBJR_REC.SAPCPQ_ATTRIBUTE_NAME).strip() == "SYOBJR-90027":
						active_all_btn_id = (
							"ACTIVEALL__"
							+ str(SYOBJR_REC.SAPCPQ_ATTRIBUTE_NAME).replace("-", "_")
							+ "_"
							+ str(SYOBJR_REC.OBJ_REC_ID).replace("-", "_")
						)
						deactive_all_btn_id = (
							"DEACTIVEALL__"
							+ str(SYOBJR_REC.SAPCPQ_ATTRIBUTE_NAME).replace("-", "_")
							+ "_"
							+ str(SYOBJR_REC.OBJ_REC_ID).replace("-", "_")
						)
						ATTRIBUTES += (
							"<Attribute><AttributeName><USEnglish>QSTN_R_"
							+ str(SYOBJR_REC.SAPCPQ_ATTRIBUTE_NAME).replace("-", "_")
							+ "</USEnglish></AttributeName><AttributeType>UserSelection</AttributeType><DisplayType>DisplayOnlyText</DisplayType><SpansAcrossEntireRow>1</SpansAcrossEntireRow><Label><USEnglish>"
							+ str(SYOBJR_REC.NAME)
							+ '</USEnglish></Label><Hint><USEnglish><![CDATA[<div class="container_banner_inner_sec"><span id="container_banner_id">'
							+ str(SYOBJR_REC.NAME)
							+ '</span><div class="dropdown flt_lt"><i data-toggle="dropdown" class="fa fa-sort-desc"></i><ul class="dropdown-menu"><li><button  id = \''
							+ str(active_all_btn_id)
							+ "' onclick=\"awd_mtrl_actv_and_deactv_all_fulfillment_fees('ACTIVE', '"
							+ str(TabNameRE)
							+ '\')" class="btnstyle">ACTIVATE</button></li><li><button  id = \''
							+ str(deactive_all_btn_id)
							+ "' onclick=\"awd_mtrl_actv_and_deactv_all_fulfillment_fees('DEACTIVE','"
							+ str(TabNameRE)
							+ '\')" class="btnstyle">DEACTIVATE</button></li></ul></div></div><div id = \''
							+ str(SYOBJR_NAME)
							+ '\' class="container ctrstyle2"></div><script type="text/javascript">'
						)
					else:
						# A043S001P01-5893 - End
						ATTRIBUTES += (
							"<Attribute><AttributeName><USEnglish>QSTN_R_"
							+ str(SYOBJR_REC.SAPCPQ_ATTRIBUTE_NAME).replace("-", "_")
							+ "</USEnglish></AttributeName><AttributeType>UserSelection</AttributeType><DisplayType>DisplayOnlyText</DisplayType><SpansAcrossEntireRow>1</SpansAcrossEntireRow><Label><USEnglish>"
							+ str(SYOBJR_REC.NAME)
							+ '</USEnglish></Label><Hint><USEnglish><![CDATA[<div class="container_banner_inner_sec"><span id="container_banner_id">'
							+ str(SYOBJR_REC.NAME)
							+ "</span></div><div id = '"
							+ str(SYOBJR_NAME)
							+ '\' class="container ctrstyle2"></div><script type="text/javascript">'
						)

					ATTRIBUTES += str(ObjR_str1)

					ATTRIBUTES += str(ObjR_str2)

					ATTRIBUTES += str(ObjR_str3)
					ATTRIBUTES += str(ObjR_str4)
					ATTRIBUTES += str(ObjR_str5)

					ATTRIBUTES += (
						"</script>]]></USEnglish></Hint><ShowOneTimePrice>0</ShowOneTimePrice><IsFirstValuePreselected>0</IsFirstValuePreselected><Values><Value><USEnglish>"
						+ "1"
						+ "</USEnglish><IsFirstValuePreselected>0</IsFirstValuePreselected></Value></Values></Attribute>"
					)
				SYOBJR_TabAttributes += (
					"<Attribute><Name>QSTN_R_"
					+ str(SYOBJR_REC.SAPCPQ_ATTRIBUTE_NAME).replace("-", "_")
					+ "</Name><Rank>"
					+ str(Counted)
					+ "</Rank></Attribute>"
				)
if len(str(SYOBJR_TabAttributes)) == 0:
	TabAttributes = SYOBJR_TabAttributes
else:
	# TabAttributes ="<Attribute><Name>SEC_RELATED_LIST_TEST</Name><Rank>"+"60"+"</Rank></Attribute>"+SYOBJR_TabAttributes
	TabAttributes = SYOBJR_TabAttributes
return TabAttributes


# RECORD ID BASED ON STATUS CHANGED IN SYAPPS CUSTOM TABLE:



RecordNo = ""
if str(RecordNo) == "":
RecordNo = Param.Primary_Data

if str(RecordNo) != "":
LOGIN_CREDENTIALS = SqlHelper.GetFirst("SELECT USER_NAME, PASSWORD, DOMAIN, URL FROM SYCONF (nolock) WHERE USER_NAME = 'X0123347'")
if LOGIN_CREDENTIALS is not None:
	Login_Username = str(LOGIN_CREDENTIALS.USER_NAME)
	Login_Password = str(LOGIN_CREDENTIALS.PASSWORD)
	Login_Domain = str(LOGIN_CREDENTIALS.DOMAIN)

apiData = BuildAPIXMLBody(RecordNo, Login_Domain)

ws = WebServiceHelper.Load("http://sandbox.webcomcpq.com/wsAPI/wssrv.asmx")
data = XmlHelper.Load(apiData)
## TODO : Move login details to configuration table
username = str(Login_Username) + "#" + str(Login_Domain)
password = str(Login_Password)
Action = "ADDORUPDATE"
f = ws.SimpleProductAdministration(username, password, Action, data)
Trace.Write("Result---->" + XmlHelper.SerializeObject(f))


# =========================================================================================================================================
#   __script_name : CQNESTGRID.PY
#   __script_description : THIS SCRIPT IS USED TO LOAD THE NESTED LIST GRID FOR THE EQUIPMENT AND CHILD TABS.
#   __primary_author__ : AYYAPPAN SUBRAMANIYAN
#   __create_date :
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import Webcom
from SYDATABASE import SQL
from datetime import datetime
import Webcom.Configurator.Scripting.Test.TestProduct
import time
Sql = SQL()
import SYCNGEGUID as CPQID
import System.Net


def GetEquipmentMaster(PerPage, PageInform, A_Keys, A_Values):
	if str(PerPage) == "" and str(PageInform) == "":
		Page_start = 1
		Page_End = 10
		PerPage = 10
		PageInform = "1___10___10"
	else:
		Page_start = int(PageInform.split("___")[0])
		Page_End = int(PageInform.split("___")[1])
		PerPage = PerPage
	#Trace.Write("Page_start--->"+str(Page_start)+"Page_End--->"+str(Page_End)+"PerPage--->"+str(PerPage))    
	TreeParam = Product.GetGlobal("TreeParam")
	TreeParentParam = Product.GetGlobal("TreeParentLevel0")
	TreeSuperParentParam = Product.GetGlobal("TreeParentLevel1")
	TreeTopSuperParentParam =  Product.GetGlobal("TreeParentLevel2")
	ContractRecordId = Quote.GetGlobal("contract_quote_record_id")
	RevisionRecordId = Quote.GetGlobal("quote_revision_record_id")
	FablocationId = Product.GetGlobal("TreeParam")
	data_list = []
	obj_idval = "SYOBJ_00937_SYOBJ_00937"
	rec_id = "SYOBJ_00937"
	obj_id = "SYOBJ-00937"
	objh_getid = Sql.GetFirst(
		"SELECT TOP 1  RECORD_ID  FROM SYOBJH (NOLOCK) WHERE SAPCPQ_ATTRIBUTE_NAME='" + str(obj_id) + "'"
	)
	if objh_getid:
		obj_id = objh_getid.RECORD_ID
	objs_obj = Sql.GetFirst(
		"select CAN_ADD,CAN_EDIT,COLUMNS,CAN_DELETE from SYOBJR (NOLOCK) where OBJ_REC_ID = '" + str(obj_id) + "' "
	)
	can_edit = str(objs_obj.CAN_EDIT)
	can_add = str(objs_obj.CAN_ADD)
	can_delete = str(objs_obj.CAN_DELETE)
	table_id = "table_equipment_parent"
	table_header = (
		'<table id="'
		+ str(table_id)
		+ '"  data-pagination="false" data-sortable="true" data-search-on-enter-key="true" data-filter-control="true" data-pagination-loop = "false" data-locale = "en-US" ><thead>'
	)
	Columns = [
		"QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID",
		"EQUIPMENT_ID",
		"EQUIPMENTCATEGORY_ID",
		"SERIAL_NUMBER",
		"CUSTOMER_TOOL_ID",
		"GREENBOOK",
		"EQUIPMENT_STATUS",
		"PLATFORM",
		"MNT_PLANT_ID",
		"FABLOCATION_ID",
		"WARRANTY_START_DATE",
		"WARRANTY_END_DATE",
	]
	Objd_Obj = Sql.GetList(
		"select FIELD_LABEL,API_NAME,LOOKUP_OBJECT,LOOKUP_API_NAME,DATA_TYPE from SYOBJD (NOLOCK) where OBJECT_NAME = 'SAQFEQ'"
	)
	attr_list = []
	attrs_datatype_dict = {}
	lookup_disply_list = []
	lookup_str = ""
	if Objd_Obj is not None:
		attr_list = {}
		for attr in Objd_Obj:
			attr_list[str(attr.API_NAME)] = str(attr.FIELD_LABEL)
			attrs_datatype_dict[str(attr.API_NAME)] = str(attr.DATA_TYPE)
			if attr.LOOKUP_API_NAME != "" and attr.LOOKUP_API_NAME is not None:
				lookup_disply_list.append(str(attr.API_NAME))
		checkbox_list = [inn.API_NAME for inn in Objd_Obj if inn.DATA_TYPE == "CHECKBOX"]
		lookup_list = {ins.LOOKUP_API_NAME: ins.API_NAME for ins in Objd_Obj}
		if (("Sending Account -" in TreeParam) or ("Receiving Account -" in TreeParam)) and TreeParentParam == 'Fab Locations':
			Trace.Write('attr_list'+str(attr_list))
			if 'FABLOCATION_ID' in attr_list:
				fab_location_id  = attr_list['FABLOCATION_ID']
				attr_list['FABLOCATION_ID'] = 'Sending Fab Location' if "Sending Account -" in TreeParam else 'Receiving Fab Location' if "Receiving Account -" in TreeParam else fab_location_id
		Trace.Write('attr_list111'+str(attr_list))
	lookup_str = ",".join(list(lookup_disply_list))
	orderby = ""
	if SortColumn != '' and SortColumnOrder !='':
		orderby = SortColumn + " " + SortColumnOrder
	else:
		orderby = "QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID"
	where_string = ""
	if A_Keys != "" and A_Values != "":
		A_Keys = list(A_Keys)
		A_Values = list(A_Values)
		for key, value in zip(A_Keys, A_Values):
			if value.strip():
				if where_string:
					where_string += " AND "
				where_string += "{Key} LIKE '%{Value}%'".format(Key=key, Value=value)
	if TreeTopSuperParentParam == "Fab Locations":
		if (("Sending Account -" in TreeSuperParentParam) or ("Receiving Account -" in TreeSuperParentParam)) and TreeTopSuperParentParam == 'Fab Locations':
			Trace.Write("Fab46")
			
			account_id = TreeSuperParentParam.split(' - ')
			account_id = account_id[len(account_id)-1]
			get_fab_query = Sql.GetList("SELECT FABLOCATION_ID FROM SAQFBL WHERE QUOTE_RECORD_ID = '{}' and QTEREV_RECORD_ID = '{}' and ACCOUNT_ID = '{}'".format(ContractRecordId,RevisionRecordId,account_id) )
			if get_fab_query:
				get_fab = tuple([fab.FABLOCATION_ID for fab in get_fab_query])
			else:
				get_fab = ""
			Trace.Write("Fab47")    
			Qstr = (
				"""select top {PerPage} * from ( select  ROW_NUMBER() OVER( ORDER BY {orderby}) AS ROW, QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID,EQUIPMENTCATEGORY_ID,EQUIPMENT_ID,MNT_PLANT_ID,CUSTOMER_TOOL_ID,SERIAL_NUMBER,GREENBOOK,EQUIPMENT_STATUS,PLATFORM,FABLOCATION_ID,CONVERT(varchar,WARRANTY_START_DATE,101) AS WARRANTY_START_DATE,CONVERT(varchar,WARRANTY_END_DATE,101) WARRANTY_END_DATE from SAQFEQ (NOLOCK) where QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}'{where_string} AND FABLOCATION_ID = '{get_fab}'  and GREENBOOK = '{get_pp}' and RELOCATION_EQUIPMENT_TYPE = '{equp_type}') m where m.ROW BETWEEN {Page_start} and {Page_End} """.format(orderby = orderby, ContractRecordId = ContractRecordId,RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"), get_fab = Product.GetGlobal("TreeParentLevel0"), get_pp = Product.GetGlobal("TreeParam"),where_string = " AND "+str(where_string) if str(where_string)!="" else "", Page_start = Page_start, Page_End = Page_End,PerPage = PerPage,equp_type = 'SENDING EQUIPMENT' if "Sending Account -" in TreeSuperParentParam else "RECEIVING EQUIPMENT" if "Receiving Account -" in TreeSuperParentParam else "" ) )

			QueryCount = ""

			QueryCountObj = Sql.GetFirst(
				"""select count(CpqTableEntryId) as cnt from SAQFEQ (NOLOCK) where QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' {where_string} and FABLOCATION_ID = '{get_fab}' and GREENBOOK = '{get_pp}' and RELOCATION_EQUIPMENT_TYPE = '{equp_type}'""".format(ContractRecordId = ContractRecordId,where_string = " AND "+str(where_string) if str(where_string)!="" else "",get_fab = Product.GetGlobal("TreeParentLevel0"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"), get_pp = Product.GetGlobal("TreeParam"), equp_type = 'SENDING EQUIPMENT' if "Sending Account -" in TreeSuperParentParam else "RECEIVING EQUIPMENT" if "Receiving Account -" in TreeSuperParentParam else "" )
			)      
	elif TreeSuperParentParam == "Fab Locations":
		Trace.Write("Fab")
		if (("Sending Account -" in TreeParentParam) or ("Receiving Account -" in TreeParentParam)) and TreeSuperParentParam == 'Fab Locations':
			Trace.Write("Fab45")
			
			account_id = TreeParentParam.split(' - ')
			account_id = account_id[len(account_id)-1]
			get_fab_query = Sql.GetList("SELECT FABLOCATION_ID FROM SAQFBL WHERE QUOTE_RECORD_ID = '{}' and QTEREV_RECORD_ID = '{}' and ACCOUNT_ID = '{}'".format(ContractRecordId,RevisionRecordId,account_id) )
			if get_fab_query:
				get_fab = tuple([fab.FABLOCATION_ID for fab in get_fab_query])
			else:
				get_fab = ""
			Qstr = (
				"""select top {PerPage} * from ( select  ROW_NUMBER() OVER( ORDER BY {orderby}) AS ROW, QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID,EQUIPMENTCATEGORY_ID,EQUIPMENT_ID,MNT_PLANT_ID,CUSTOMER_TOOL_ID,SERIAL_NUMBER,GREENBOOK,EQUIPMENT_STATUS,PLATFORM,FABLOCATION_ID,CONVERT(varchar,WARRANTY_START_DATE,101) AS WARRANTY_START_DATE,CONVERT(varchar,WARRANTY_END_DATE,101) WARRANTY_END_DATE from SAQFEQ (NOLOCK) where QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' {where_string} AND FABLOCATION_ID = '{get_fab}'  and RELOCATION_EQUIPMENT_TYPE = '{equp_type}') m where m.ROW BETWEEN {Page_start} and {Page_End} """.format(orderby = orderby, ContractRecordId = ContractRecordId,RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"), get_fab = TreeParam, Page_start = Page_start, Page_End = Page_End,PerPage = PerPage,equp_type = 'SENDING EQUIPMENT' if "Sending Account -" in TreeParentParam else "RECEIVING EQUIPMENT" if "Receiving Account -" in TreeParentParam else "",where_string = " AND "+str(where_string) if str(where_string)!="" else "" ) )

			QueryCount = ""

			QueryCountObj = Sql.GetFirst(
				"""select count(CpqTableEntryId) as cnt from SAQFEQ (NOLOCK) where QUOTE_RECORD_ID = '{ContractRecordId}'and QTEREV_RECORD_ID = '{RevisionRecordId}' and FABLOCATION_ID = '{get_fab}' and RELOCATION_EQUIPMENT_TYPE = '{equp_type}'""".format(ContractRecordId = ContractRecordId,get_fab = TreeParam,RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"),equp_type = 'SENDING EQUIPMENT' if "Sending Account -" in TreeParentParam else "RECEIVING EQUIPMENT" if "Receiving Account -" in TreeParentParam else "" )
			)
		
		else:
			Trace.Write('ggggggggg')
			Qstr = (
				"select top "
				+ str(PerPage)
				+ " * from ( select  ROW_NUMBER() OVER( ORDER BY QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID) AS ROW, QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID,EQUIPMENTCATEGORY_ID,EQUIPMENT_ID,MNT_PLANT_ID,CUSTOMER_TOOL_ID,SERIAL_NUMBER,GREENBOOK,EQUIPMENT_STATUS,PLATFORM,FABLOCATION_ID,CONVERT(varchar,WARRANTY_START_DATE,101) AS WARRANTY_START_DATE,CONVERT(varchar,WARRANTY_END_DATE,101) WARRANTY_END_DATE from SAQFEQ (NOLOCK) where QUOTE_RECORD_ID = '"
				+ str(ContractRecordId)
				+ "' and QTEREV_RECORD_ID = '"
				+ str(RevisionRecordId)
				+ "'  and GREENBOOK = '"
				+ str(FablocationId)
				+ "' and FABLOCATION_ID = '"
				+ str(TreeParentParam)
				+ "') m where m.ROW BETWEEN "
				+ str(Page_start)
				+ " and "
				+ str(Page_End)
			)
			QueryCount = ""
			QueryCountObj = Sql.GetFirst(
				"select count(QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID) as cnt from SAQFEQ (NOLOCK) where QUOTE_RECORD_ID = '"
				+ str(ContractRecordId)
				+ "' and QTEREV_RECORD_ID = '"
				+ str(RevisionRecordId)
				+ "'  and GREENBOOK = '"
				+ str(TreeParam)
				+ "' and FABLOCATION_ID = '"
				+ str(TreeParentParam)
				+ "'"
			)
	elif TreeParam == "Fab Locations":
		Trace.Write("Fab22")
		if str(where_string)!="":
			where_string = " AND "+str(where_string)
		Qstr = (
			"select top "
			+ str(PerPage)
			+ " * from ( select  ROW_NUMBER() OVER( ORDER BY QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID) AS ROW, QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID,EQUIPMENTCATEGORY_ID,EQUIPMENT_ID,MNT_PLANT_ID,CUSTOMER_TOOL_ID,SERIAL_NUMBER,GREENBOOK,EQUIPMENT_STATUS,PLATFORM,FABLOCATION_ID,CONVERT(varchar,WARRANTY_START_DATE,101) AS WARRANTY_START_DATE,CONVERT(varchar,WARRANTY_END_DATE,101) WARRANTY_END_DATE from SAQFEQ (NOLOCK) where QUOTE_RECORD_ID = '"
			+ str(ContractRecordId)
			+ "' and QTEREV_RECORD_ID = '"
			+ str(RevisionRecordId)
			+ "' "+str(where_string)+") m where m.ROW BETWEEN "
			+ str(Page_start)
			+ " and "
			+ str(Page_End)
		)
		QueryCount = ""
		QueryCountObj = Sql.GetFirst(
			"select count(CpqTableEntryId) as cnt from SAQFEQ (NOLOCK) where QUOTE_RECORD_ID = '"
			+ str(ContractRecordId)
			+ "' and QTEREV_RECORD_ID = '"
			+ str(RevisionRecordId)
			+ "' "+str(where_string)
		)
	# elif TreeParam == "Quote Items":
	#     Qstr = (
	#         "select top "
	#         + str(PerPage)
	#         + " * from ( select  ROW_NUMBER() OVER( ORDER BY QUOTE_ITEM_RECORD_ID) AS ROW, QUOTE_ITEM_RECORD_ID,SERVICE_ID,SERVICE_DESCRIPTION, LINE_ITEM_ID,OBJECT_QUANTITY,TOTAL_COST,DISCOUNT,SRVTAXCLA_DESCRIPTION,TAX_PERCENTAGE,EXTENDED_PRICE  from SAQITM (NOLOCK) where QUOTE_RECORD_ID = '"
	#         + str(ContractRecordId)
	#         + "') m where m.ROW BETWEEN "
	#         + str(Page_start)
	#         + " and "
	#         + str(Page_End)
	#     )
	#     QueryCount = ""
	#     QueryCountObj = Sql.GetFirst(
	#         "select count(QUOTE_ITEM_RECORD_ID) as cnt from SAQITM (NOLOCK) where QUOTE_RECORD_ID = '"
	#         + str(ContractRecordId)
	#         + "'"
	#     )
	elif (("Sending Account -" in TreeParam) or ("Receiving Account -" in TreeParam)) and TreeParentParam == 'Fab Locations':
		Trace.Write("Fab44")
		
		account_id = TreeParam.split(' - ')

		account_id = account_id[len(account_id)-1]
		fab_type = 'SENDING FAB' if "Sending Account -" in TreeParam else 'RECEIVING FAB' if "Receiving Account -" in TreeParam else ""
		get_fab_query = Sql.GetList("SELECT FABLOCATION_ID FROM SAQFBL WHERE QUOTE_RECORD_ID = '{}' and ACCOUNT_ID = '{}' and QTEREV_RECORD_ID = '{}' and RELOCATION_FAB_TYPE = '{}'".format(ContractRecordId,account_id,RevisionRecordId,fab_type) )
		if get_fab_query:
			get_fab = "in "+ str(tuple([fab.FABLOCATION_ID for fab in get_fab_query])).replace(",)",')')
		else:
			get_fab = "= ''"
		Qstr = (
			"""select top {PerPage} * from ( select  ROW_NUMBER() OVER( ORDER BY {orderby}) AS ROW, QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID,SALESORG_ID,SERIAL_NUMBER,CUSTOMER_TOOL_ID,WARRANTY_START_DATE,WARRANTY_END_DATE,EQUIPMENTCATEGORY_ID,EQUIPMENT_ID,MNT_PLANT_ID,GREENBOOK,QUOTE_NAME,SALESORG_NAME,EQUIPMENTCATEGORY_DESCRIPTION,EQUIPMENT_STATUS,PLATFORM,FABLOCATION_ID,QUOTE_ID,FABLOCATION_NAME from SAQFEQ (NOLOCK) where QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}'{where_string} AND FABLOCATION_ID {get_fab}  and RELOCATION_EQUIPMENT_TYPE = '{equp_type}') m where m.ROW BETWEEN {Page_start} and {Page_End} """.format(orderby = orderby, ContractRecordId = ContractRecordId,RevisionRecordId = RevisionRecordId, get_fab = get_fab, Page_start = Page_start, Page_End = Page_End,PerPage = PerPage,equp_type = 'SENDING EQUIPMENT' if "Sending Account -" in TreeParam else "RECEIVING EQUIPMENT" if "Receiving Account -" in TreeParam else "",where_string = " AND "+str(where_string) if str(where_string)!="" else "" ) )

		QueryCount = ""

		QueryCountObj = Sql.GetFirst(
			"""select count(CpqTableEntryId) as cnt from SAQFEQ (NOLOCK) where QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' {where_string} AND FABLOCATION_ID  {get_fab} and RELOCATION_EQUIPMENT_TYPE = '{equp_type}'""".format(ContractRecordId = ContractRecordId,RevisionRecordId = RevisionRecordId,get_fab = get_fab,equp_type = 'SENDING EQUIPMENT' if "Sending Account -" in TreeParam else "RECEIVING EQUIPMENT" if "Receiving Account -" in TreeParam else "",where_string = " AND "+str(where_string) if str(where_string)!="" else "" )
		)

	else:
		# if TreeSuperParentParam == "Sending Equipment" or TreeSuperParentParam == "Receiving Equipment":
		#     Qstr = (
		#         "select top "
		#         + str(PerPage)
		#         + " * from ( select  ROW_NUMBER() OVER( ORDER BY "+str(orderby)+") AS ROW, QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID,EQUIPMENTCATEGORY_ID,EQUIPMENT_ID,MNT_PLANT_ID,CUSTOMER_TOOL_ID,SERIAL_NUMBER,GREENBOOK,EQUIPMENT_STATUS,PLATFORM,FABLOCATION_ID,CONVERT(varchar,WARRANTY_START_DATE,101) AS WARRANTY_START_DATE,CONVERT(varchar,WARRANTY_END_DATE,101) WARRANTY_END_DATE from SAQFEQ (NOLOCK) where QUOTE_RECORD_ID = '"
		#         + str(ContractRecordId)
		#         + "' and FABLOCATION_ID = '"
		#         + str(TreeParentParam)
		#         + "' and GREENBOOK = '"+str(TreeParam)+"') m where m.ROW BETWEEN "
		#         + str(Page_start)
		#         + " and "
		#         + str(Page_End)
		#     )

		#     QueryCount = ""

		#     QueryCountObj = Sql.GetFirst(
		#         "select count(CpqTableEntryId) as cnt from SAQFEQ (NOLOCK) where QUOTE_RECORD_ID = '"
		#         + str(ContractRecordId)
		#         + "' and FABLOCATION_ID = '"
		#         + str(TreeParentParam)
		#         + "' and GREENBOOK = '"+str(TreeParam)+"' "
		#     )
		# elif TreeParentParam == 'Sending Equipment' or TreeParentParam == 'Receiving Equipment':  
		#     Qstr = (
		#         "select top "
		#         + str(PerPage)
		#         + " * from ( select  ROW_NUMBER() OVER( ORDER BY "+str(orderby)+") AS ROW, QUOTE_SERVICE_SENDING_FAB_LOC_EQUIP_ID,SALESORG_ID,EQUIPMENTCATEGORY_ID,SND_EQUIPMENT_ID,MNT_PLANT_ID,GREENBOOK,QUOTE_NAME,SALESORG_NAME,SND_EQUIPMENT_DESCRIPTION,EQUIPMENT_STATUS,PLATFORM,SNDFBL_ID,QUOTE_ID,SNDFBL_NAME from SAQSSE (NOLOCK) where QUOTE_RECORD_ID = '"
		#         + str(ContractRecordId)
		#         + "' and SNDFBL_ID = '"
		#         + str(TreeParam)
		#         + "') m where m.ROW BETWEEN "
		#         + str(Page_start)
		#         + " and "
		#         + str(Page_End)
		#     )

		#     QueryCount = ""

		#     QueryCountObj = Sql.GetFirst(
		#         "select count(CpqTableEntryId) as cnt from SAQSSE (NOLOCK) where QUOTE_RECORD_ID = '"
		#         + str(ContractRecordId)
		#         + "' and SNDFBL_ID = '"
		#         + str(TreeParam)
		#         + "' "
		#     )  
		if TreeSuperParentParam.startswith("Sending"):
			Qstr = (
				"select top "
				+ str(PerPage)
				+ " * from ( select  ROW_NUMBER() OVER( ORDER BY "+str(orderby)+") AS ROW, QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID,EQUIPMENTCATEGORY_ID,EQUIPMENT_ID,MNT_PLANT_ID,CUSTOMER_TOOL_ID,SERIAL_NUMBER,GREENBOOK,EQUIPMENT_STATUS,PLATFORM,FABLOCATION_ID,CONVERT(varchar,WARRANTY_START_DATE,101) AS WARRANTY_START_DATE,CONVERT(varchar,WARRANTY_END_DATE,101) WARRANTY_END_DATE from SAQFEQ (NOLOCK) where QUOTE_RECORD_ID = '"
				+ str(ContractRecordId)
				+ "' and FABLOCATION_ID = '"
				+ str(TreeParentParam)
				+ "' and RELOCATION_FAB_TYPE = 'SENDING FAB' and GREENBOOK ='"
				+str(TreeParam)
				+ "') m where m.ROW BETWEEN "
				+ str(Page_start)
				+ " and "
				+ str(Page_End)
			)

			QueryCount = ""

			QueryCountObj = Sql.GetFirst(
				"select count(CpqTableEntryId) as cnt from SAQFEQ (NOLOCK) where QUOTE_RECORD_ID = '"
				+ str(ContractRecordId)
				+ "' and QTEREV_RECORD_ID = '"
				+ str(RevisionRecordId)
				+ "' and FABLOCATION_ID = '"
				+ str(TreeParentParam)
				+ "' and RELOCATION_FAB_TYPE = 'SENDING FAB' and GREENBOOK ='"
				+str(TreeParam)
				+"'"
			)
		elif TreeSuperParentParam.startswith("Receiving"):
			Qstr = (
				"select top "
				+ str(PerPage)
				+ " * from ( select  ROW_NUMBER() OVER( ORDER BY "+str(orderby)+") AS ROW, QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID,EQUIPMENTCATEGORY_ID,EQUIPMENT_ID,MNT_PLANT_ID,CUSTOMER_TOOL_ID,SERIAL_NUMBER,GREENBOOK,EQUIPMENT_STATUS,PLATFORM,FABLOCATION_ID,CONVERT(varchar,WARRANTY_START_DATE,101) AS WARRANTY_START_DATE,CONVERT(varchar,WARRANTY_END_DATE,101) WARRANTY_END_DATE from SAQFEQ (NOLOCK) where QUOTE_RECORD_ID = '"
				+ str(ContractRecordId)
				+ "' and QTEREV_RECORD_ID = '"
				+ str(RevisionRecordId)
				+ "' and FABLOCATION_ID = '"
				+ str(TreeParentParam)
				+ "' and RELOCATION_FAB_TYPE = 'RECEIVING FAB' and GREENBOOK = '"
				+str(TreeParam)
				+ "') m where m.ROW BETWEEN "
				+ str(Page_start)
				+ " and "
				+ str(Page_End)
			)

			QueryCount = ""

			QueryCountObj = Sql.GetFirst(
				"select count(CpqTableEntryId) as cnt from SAQFEQ (NOLOCK) where QUOTE_RECORD_ID = '"
				+ str(ContractRecordId)
				+ "' and QTEREV_RECORD_ID = '"
				+ str(RevisionRecordId)
				+ "' and FABLOCATION_ID = '"
				+ str(TreeParentParam)
				+ "' and RELOCATION_FAB_TYPE = 'RECEIVING FAB' and GREENBOOK ='"
				+str(TreeParam)
				+"'"
			)
		elif TreeTopSuperParentParam != "Fab Locations" or TreeParentParam != 'Sending Equipment' or TreeParentParam != 'Receiving Equipment':
			Trace.Write("else--------")
			if str(where_string):
				where_string = " AND "+str(where_string)
			Qstr = (
				"select top "
				+ str(PerPage)
				+ " * from ( select  ROW_NUMBER() OVER( ORDER BY "+str(orderby)+") AS ROW, QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID,EQUIPMENTCATEGORY_ID,EQUIPMENT_ID,MNT_PLANT_ID,CUSTOMER_TOOL_ID,SERIAL_NUMBER,GREENBOOK,EQUIPMENT_STATUS,PLATFORM,FABLOCATION_ID,CONVERT(varchar,WARRANTY_START_DATE,101) AS WARRANTY_START_DATE,CONVERT(varchar,WARRANTY_END_DATE,101) WARRANTY_END_DATE from SAQFEQ (NOLOCK) where QUOTE_RECORD_ID = '"
				+ str(ContractRecordId)
				+ "' and QTEREV_RECORD_ID = '"
				+ str(RevisionRecordId)
				+ "' and FABLOCATION_ID = '"
				+ str(FablocationId)
				+ "' "+str(where_string)+") m where m.ROW BETWEEN "
				+ str(Page_start)
				+ " and "
				+ str(Page_End)
			)

			QueryCount = ""

			QueryCountObj = Sql.GetFirst(
				"select count(CpqTableEntryId) as cnt from SAQFEQ (NOLOCK) where QUOTE_RECORD_ID = '"
				+ str(ContractRecordId)
				+ "' and QTEREV_RECORD_ID = '"
				+ str(RevisionRecordId)
				+ "' and FABLOCATION_ID = '"
				+ str(FablocationId)
				+ "' "
			)

	if QueryCountObj is not None:
		QueryCount = QueryCountObj.cnt
		#Trace.Write("count---->" + str(QueryCount))
	parent_obj = Sql.GetList(Qstr)
	for par in parent_obj:
		data_id = str(par.QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID)        
		Action_str = (
			'<div class="btn-group dropdown"><div class="dropdown" id="ctr_drop"><i data-toggle="dropdown" id="dropdownMenuButton" class="fa fa-sort-desc dropdown-toggle" aria-expanded="false"></i><ul class="dropdown-menu left" aria-labelledby="dropdownMenuButton"><li><a class="dropdown-item cur_sty" href="#" id="'
			+ str(data_id)
			+ '" onclick="Commonteree_view_RL(this)">VIEW</a></li>'
			'<li><a class="dropdown-item" id="deletebtn" data-target="#cont_CommonModalDelete" data-toggle="modal" onclick="CommonDelete(this, \'SAQFEA#'+ data_id +'\', \'WARNING\')" href="#">DELETE</a></li>'
		)
		if can_edit.upper() == "TRUE":
			Action_str += (
				'<li style="display:none" ><a class="dropdown-item cur_sty" href="#" id="'
				+ str(data_id)
				+ '" onclick="Move_to_parent_obj_edit(this)">EDIT</a></li>'
			)
		if can_delete.upper() == "TRUE":
			Action_str += '<li><a class="dropdown-item" data-target="#cont_viewModal_Material_Delete" data-toggle="modal" onclick="Material_delete_obj(this)" href="#">DELETE</a></li>'
		# if can_add.upper() == "TRUE" and par.MARKET_TYPE == "NON MARKET BASED" and par.MODEL_TYPE != "COST PLUS":
		#     Action_str += (
		#         '<li><a class="dropdown-item" id="'
		#         + str(data_id)
		#         + '" data-target="#" data-toggle="modal" onclick="Pricebook_clone_obj(this)" href="#">CLONE</a></li>'
		#     )
		Action_str += "</ul></div></div>"

		# Data formation in dictonary format.
		## hyperlink
		data_dict = {}
		data_dict["ids"] = str(data_id)
		data_dict["ACTIONS"] = str(Action_str)
		data_dict["QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID"] = CPQID.KeyCPQId.GetCPQId(
			"SAQFEQ", str(par.QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID)
		)
		data_dict["EQUIPMENTCATEGORY_ID"] = ('<abbr id ="" title="' + str(par.EQUIPMENTCATEGORY_ID) + '">' + str(par.EQUIPMENTCATEGORY_ID) + "</abbr>") 
		data_dict["EQUIPMENT_ID"] = ('<abbr id ="" title="' + str(par.EQUIPMENT_ID) + '">' + str(par.EQUIPMENT_ID) + "</abbr>")
		data_dict["SERIAL_NUMBER"] = ('<abbr id ="" title="' + str(par.SERIAL_NUMBER) + '">' + str(par.SERIAL_NUMBER) + "</abbr>")
		data_dict["CUSTOMER_TOOL_ID"] = ('<abbr id ="" title="' + str(par.CUSTOMER_TOOL_ID) + '">' + str(par.CUSTOMER_TOOL_ID) + "</abbr>")
		data_dict["GREENBOOK"] = ('<abbr id ="" title="' + str(par.GREENBOOK) + '">' + str(par.GREENBOOK) + "</abbr>")
		data_dict["EQUIPMENT_STATUS"] = ('<abbr id ="" title="' + str(par.EQUIPMENT_STATUS) + '">' + str(par.EQUIPMENT_STATUS) + "</abbr>")
		data_dict["PLATFORM"] = ('<abbr id ="" title="' + str(par.PLATFORM) + '">' + str(par.PLATFORM) + "</abbr>")
		data_dict["MNT_PLANT_ID"] = ('<abbr id ="" title="' + str(par.MNT_PLANT_ID) + '">' + str(par.MNT_PLANT_ID) + "</abbr>")
		data_dict["FABLOCATION_ID"] = ('<abbr id ="" title="' + str(par.FABLOCATION_ID) + '">' + str(par.FABLOCATION_ID) + "</abbr>")
		data_dict["WARRANTY_START_DATE"] = ('<abbr id ="" title="' + str(par.WARRANTY_START_DATE) + '">' + str(par.WARRANTY_START_DATE) + "</abbr>")
		data_dict["WARRANTY_END_DATE"] = ('<abbr id ="" title="' + str(par.WARRANTY_END_DATE) + '">' + str(par.WARRANTY_END_DATE) + "</abbr>")
		data_list.append(data_dict)
		# Trace.Write("data_dict||data_dict||data_dict"+str(data_dict))
	hyper_link = ["QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID"]
	if TreeTopSuperParentParam == "Fab Locations" and ("Sending Account -" in TreeSuperParentParam) or ("Receiving Account -" in TreeSuperParentParam):
		ParentObj = Sql.GetList(
			"select EQUIPMENT_ID from SAQFEQ (NOLOCK) where QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' and FABLOCATION_ID = '{FablocationId}'".format(
				ContractRecordId=Quote.GetGlobal("contract_quote_record_id"), FablocationId=Product.GetGlobal("TreeParentLevel0"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id")
			)
		)
	else:    
		ParentObj = Sql.GetList(
			"select EQUIPMENT_ID from SAQFEQ (NOLOCK) where QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' and FABLOCATION_ID = '{FablocationId}'".format(
				ContractRecordId=Quote.GetGlobal("contract_quote_record_id"), FablocationId=Product.GetGlobal("TreeParam"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id")
			)
		)
	table_header += "<tr>"
	table_header += (
		'<th data-field="ACTIONS"><div class="action_col">ACTIONS</div><button class="searched_button" id="Act_'
		+ str(table_id)
		+ '">Search</button></th>'
	)
	table_header += '<th data-field="SELECT" class="wid45" data-checkbox="true"></th>'
	for key, invs in enumerate(list(Columns)):
		invs = str(invs).strip()
		qstring = attr_list.get(str(invs)) or ""
		if qstring == "":
			qstring = invs.replace("_", " ")
		if checkbox_list is not None and invs in checkbox_list:
			table_header += (
				'<th  data-field="'
				+ str(invs)
				+ '" data-filter-control="input" data-align="center" data-formatter="CheckboxFieldRelatedList" data-sortable="true"><abbr title="'
				+ str(qstring)
				+ '">'
				+ str(qstring)
				+ "</abbr></th>"
			)
		elif hyper_link is not None and invs in hyper_link:            
			table_header += (
				'<th data-field="'
				+ str(invs)
				+ '" data-filter-control="input" data-title-tooltip="'+str(qstring)+'" data-formatter="EquipHyperLinkTreeLink" data-sortable="true"'+ str(qstring)+'"><abbr title="'
				+ str(qstring)
				+ '">'
				+ str(qstring)
				+ "</abbr></th>"
			)
		else:            
			table_header += (
				'<th  data-field="'
				+ str(invs)
				+ '" data-filter-control="input"  data-title-tooltip="'+str(qstring)+'" data-sortable="true"><abbr title="'
				+ str(qstring)
				+ '">'
				+ str(qstring)
				+ "</abbr></th>"
			)

	table_header += "</tr>"
	table_header += '</thead><tbody onclick="Table_Onclick_Scroll(this)"></tbody></table>'
	table_ids = "#" + str(table_id)
	filter_control_function = ""
	tbl_id = table_id
	values_list = ""
	for key, invs in enumerate(list(Columns)):
		table_ids = "#" + str(table_id)
		filter_clas = "#" + str(table_id) + " .bootstrap-table-filter-control-" + str(invs)
		values_list += "var " + str(invs) + ' = $("' + str(filter_clas) + '").val(); '
		values_list += "ATTRIBUTE_VALUEList.push(" + str(invs) + "); "
	filter_class = "#Act_" + str(table_id)
	filter_control_function += (
	'$("'
	+ filter_class
	+ '").click( function(){ var table_id = $(this).closest("table").attr("id"); ATTRIBUTE_VALUEList = []; '
	+ str(values_list)
	+ ' var attribute_value = $(this).val(); cpq.server.executeScript("CQNESTGRID", {"TABNAME":"Equipment Parent", "ACTION":"PRODUCT_ONLOAD_FILTER", "ATTRIBUTE_NAME": '
	+ str(list(Columns))
	+ ', "ATTRIBUTE_VALUE": ATTRIBUTE_VALUEList }, function(dataset) {debugger; data2 = dataset[1];  data1 = dataset[0]; data3 = dataset[2]; console.log("len ---->"+data1.length);  try { if(data1.length > 0) { $("#'
	+ str(tbl_id)
	+ '").bootstrapTable("load", data1 );$("#noRecDisp").remove(); if (document.getElementById("'+str(tbl_id) + '___totalItemCount")){document.getElementById("'+str(tbl_id)+ '___totalItemCount").innerHTML = data2;}  if (document.getElementById("'+str(tbl_id) + '___NumberofItem")) { console.log("if_chk_j"); document.getElementById("'+str(tbl_id)+ '___NumberofItem").innerHTML = data3;}} else{ console.log("else_chk_j"); $("#' + str(tbl_id) + '").bootstrapTable("load", data1  );$("#' + str(tbl_id) + '").after("<div id=\'noRecDisp\' class=\'noRecord\'>No Records to Display</div>"); if (document.getElementById("'+str(tbl_id) + '___totalItemCount")){document.getElementById("'+str(tbl_id)+ '___totalItemCount").innerHTML = data2;}  if (document.getElementById("'+str(tbl_id) + '___NumberofItem")) {document.getElementById("'+str(tbl_id)+ '___NumberofItem").innerHTML = data3;} }} catch(err){} }); filter_search_click();$(".JColResizer").mousedown(function(){ $("thead.fullHeadFirst").css("cssText","z-index: 2;border-top: 1px solid rgb(220, 220, 220);top: 154px;border-right: 0px !important;");$("thead.fullHeadSecond").css("display","none"); });$(".JColResizer").mouseup(function(){ var th_width_resize = [];$("#table_equipment_parent thead.fullHeadFirst tr th").each(function(index){var wid = $(this).css("width"); if(index ==0 || index ==1){th_width_resize.push("60px");}else{th_width_resize.push(wid);}}); $("thead.fullHeadFirst").css("cssText","position: fixed;z-index: 2;border-top: 1px solid rgb(220, 220, 220); top: 154px;border-right: 0px !important;");$("thead.fullHeadSecond").css("display","table-header-group");$("#table_equipment_parent thead.fullHeadFirst tr th").each(function(index){var num = th_width_resize[index].split("px");var numsp = parseInt(num[0]);numsp = numsp - 1;var make_str =numsp+"px"; var c = "width:"+make_str+";white-space: nowrap;overflow: hidden;text-overflow: ellipsis;";var d = "width:"+make_str+";"; $(this).css("cssText",c);$(this).children("div:first-child").css("cssText",c);$(this).children("div.fht-cell").css("cssText",d);});$("#table_equipment_parent thead.fullHeadSecond tr th").each(function(index){var num = th_width_resize[index].split("px");var numsp = parseInt(num[0]);numsp = numsp - 1;var make_str =numsp+"px"; var c = "width:"+make_str+";white-space: nowrap;overflow: hidden;text-overflow: ellipsis;";var d = "width:"+make_str+";"; $(this).css("cssText",c);$(this).children("div:first-child").css("cssText",c);$(this).children("div.fht-cell").css("cssText",d);}); });});')
	
	#Trace.Write("666 filter_control_function ---->"+str(filter_control_function))

	dbl_clk_function = (
		'$("'
		+ str(table_ids)
		+ '").on("all.bs.table", function (e, name, args) { $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); }); $("'
		+ str(table_ids)
		+ '\ th.bs-checkbox div.th-inner").before("<div style=\'padding:0; border-bottom: 1px solid #dcdcdc;\'>SELECT</div>"); $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); $("'
		+ str(table_ids)
		+ "\").on('sort.bs.table', function (e, name, order) {  console.log('Parent sort.bs.table ====> ', e); currenttab = $(\"ul#carttabs_head .active\").text().trim(); localStorage.setItem('"
		+ str(table_id)
		+ "_SortColumn', name); localStorage.setItem('"
		+ str(table_id)
		+ "_SortColumnOrder', order); NestedContainerSorting(name, order, '"
		+ str(table_id)
		+ "'); }); "
		)
	NORECORDS = ""
	if len(data_list) == 0:
		NORECORDS = "NORECORDS"

	ObjectName = "SAQFEQ"
	DropDownList = []
	filter_level_list = []
	filter_clas_name = ""
	cv_list = []
	TableclassName = "form-control" + table_id
	for key, col_name in enumerate(list(Columns)):
		StringValue_list = []
		objss_obj = Sql.GetFirst(
			"SELECT API_NAME, DATA_TYPE, FORMULA_LOGIC, PICKLIST FROM SYOBJD (NOLOCK) WHERE OBJECT_NAME='"
			+ str(ObjectName)
			+ "' and API_NAME = '"
			+ str(col_name)
			+ "'"
		)
		try:
			FORMULA_LOGIC = objss_obj.FORMULA_LOGIC.strip()
			FORMULA_col = FORMULA_LOGIC.split(" ")[1].strip()
			FORMULA_table = FORMULA_LOGIC.split(" ")[3].strip()
			ins_obj = Sql.GetFirst(
				"SELECT API_NAME, DATA_TYPE,PICKLIST FROM SYOBJD (NOLOCK) WHERE OBJECT_NAME='"
				+ str(FORMULA_table)
				+ "' and API_NAME = '"
				+ str(FORMULA_col)
				+ "'"
			)
			if str(objss_obj.PICKLIST).upper() == "TRUE":
				filter_level_data = "select"
				filter_clas_name = (
					'<div id = "'
					+ str(table_id)
					+ "_RelatedMutipleCheckBoxDrop_"
					+ str(key)
					+ '" class="form-control bootstrap-table-filter-control-'
					+ str(col_name)
					+ " RelatedMutipleCheckBoxDrop_"
					+ str(key)
					+ ' "></div>'
				)
				filter_level_list.append(filter_level_data)
			else:
				filter_level_data = "input"
				filter_clas_name = (
					'<input type="text" class="width100_vis form-control bootstrap-table-filter-control-'
					+ str(col_name)
					+ '">'
				)
				filter_level_list.append(filter_level_data)
		except:
			Trace.Write("except---->")
			if str(objss_obj.PICKLIST).upper() == "TRUE":
				filter_level_data = "select"
				filter_clas_name = (
					'<div id = "'
					+ str(table_id)
					+ "_RelatedMutipleCheckBoxDrop_"
					+ str(key)
					+ '" class="form-control bootstrap-table-filter-control-'
					+ str(col_name)
					+ " RelatedMutipleCheckBoxDrop_"
					+ str(key)
					+ ' "></div>'
				)
				filter_level_list.append(filter_level_data)

			filter_level_data = "input"
			filter_clas_name = (
				'<input type="text" class="width100_vis form-control bootstrap-table-filter-control-' + str(col_name) + '">'
			)
			filter_level_list.append(filter_level_data)
		cv_list.append(filter_clas_name)
		if filter_level_data == "select":
			try:
				xcd = Sql.GetFirst(
					"SELECT (STUFF((SELECT DISTINCT ', ' + CAST("
					+ str(col_name)
					+ " AS CHAR(100)) FROM "
					+ str(ObjectName)
					+ " FOR XML PATH('') ), 1, 2, '')  ) AS StringValue"
				)
			except:
				xcd = Sql.GetFirst(
					"SELECT (STUFF((SELECT DISTINCT ', ' + CAST("
					+ str(col_name)
					+ " AS CHAR(100)) FROM "
					+ str(ObjectName)
					+ " FOR XML PATH('') ), 1, 2, '')  ) AS StringValue"
				)
			if str(xcd.StringValue) is not None and str(xcd.StringValue) != "":
				if str(xcd.StringValue).find(",") != -1:
					StringValue_list = [ins.strip() for ins in str(xcd.StringValue).split(",") if ins.strip() != ""]
				else:
					StringValue_list.append(str(xcd.StringValue))
			else:
				StringValue_list = [""]
			StringValue_list = list(set(StringValue_list))
			DropDownList.append(StringValue_list)
		elif filter_level_data == "checkbox":
			DropDownList.append(["True", "False"])
		else:
			DropDownList.append("")
	RelatedDrop_str = (
		"try { if( document.getElementById('"
		+ str(table_id)
		+ "') ) { var listws = document.getElementById('"
		+ str(table_id)
		+ "').getElementsByClassName('filter-control');  for (i = 0; i < listws.length; i++) { document.getElementById('"
		+ str(table_id)
		+ "').getElementsByClassName('filter-control')[i].innerHTML = data6[i];  } for (j = 0; j < listws.length; j++) { if (data7[j] == 'select') { if (data8[j]) { var dataAdapter = new $.jqx.dataAdapter(data8[j]); $('#"
		+ str(table_id)
		+ "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter, autoDropDownHeight: true }); } } } } }  catch(err) { setTimeout(function() { var listws = document.getElementById('"
		+ str(table_id)
		+ "').getElementsByClassName('filter-control');  for (i = 0; i < listws.length; i++) { document.getElementById('"
		+ str(table_id)
		+ "').getElementsByClassName('filter-control')[i].innerHTML = data6[i];  } for (j = 0; j < listws.length; j++) { if (data7[j] == 'select') { if (data8[j]) { var dataAdapter = new $.jqx.dataAdapter(data8[j]); $('#"
		+ str(table_id)
		+ "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter, autoDropDownHeight: true }); } } } }, 5000); }"
	)
	page = ""
	if QueryCount < int(PerPage):
		page = str(Page_start) + " - " + str(QueryCount)
	else:
		page = str(Page_start) + " - " + str(Page_End)
	#Trace.Write("page----->"+str(page))    
	Test = (
		'<div class="col-md-12 brdr listContStyle pad2height30" ><div class="col-md-4 pager-numberofitem clear-padding"><span class="pager-number-of-items-item noofitem" id="'
		+ str(table_id)
		+ '___NumberofItem" >'
		+ str(page)
		+ ' of</span><span class="pager-number-of-items-item fltltpad2mrg0" id="'
		+ str(table_id)
		+ '___totalItemCount" >'
		+ str(QueryCount)
		+ '</span><div class="clear-padding fltltmrgtp3" ><div  class="pull-right vertmidtxtrht"><select onchange="PageFunctestChild(this,\'Quote\',\'\',\'table_equipment_parent\')" id="'
		+ str(table_id)
		+ '___PageCountValue" class="form-control wid65vermiddisinbmarl5"><option value="10" selected>10</option><option value="20">20</option><option value="50">50</option><option value="100">100</option><option value="200">200</option></select> </div></div></div><div class="col-xs-8 col-md-4  clear-padding disinpad10txtcen"  data-bind="visible: totalItemCount"><div class="clear-padding col-xs-12 col-sm-6 col-md-12 bor0" ><ul class="pagination pagination"><li class="disabled"><a href="#" onclick="FirstPageLoad_paginationChild(\'Quote\',\'\',\'table_equipment_parent\')"><i class="fa fa-caret-left font14whtbld" ></i><i class="fa fa-caret-left font14" ></i></a></li><li class="disabled"><a href="#" onclick="Previous12334Child(\'Quote\',\'\',\'table_equipment_parent\')"><i class="fa fa-caret-left font14" ></i>PREVIOUS</a></li><li class="disabled"><a href="#" class="disabledPage" onclick="Next12334Child(\'Quote\',\'\',\'table_equipment_parent\')">NEXT<i class="fa fa-caret-right font14" ></i></a></li><li class="disabled"><a href="#" onclick="LastPageLoad_paginationChild(\'Quote\',\'\',\'table_equipment_parent\')" class="disabledPage"><i class="fa fa-caret-right font14"></i><i class="fa fa-caret-right font14whtbld"></i></a></li></ul></div> </div> <div class="col-md-4 pr_page_pad"> <span id="'
		+ str(table_id)
		+ '___page_count" class="currentPage page_right_content">1</span><span class="page_right_content pad_rt_2">Page </span></div></div>'
	)
	#Log.Info("Equipment Grid table_header--->"+str(table_header)+"Equipment Grid data_list--->"+str(data_list))
	if QueryCount < int(PerPage):
		PerPage = str(QueryCount)
	else:
		PerPage = str(PerPage)   
	if Page_End > QueryCount:
		Page_End = QueryCount
	else:
		Page_End = Page_End
	#Trace.Write("Page_End----->"+str(Page_End))    
	Action_Str = ""
	#Action_Str = "1 - "
	Action_Str += str(Page_start)+" - "
	Action_Str += str(Page_End)
	Action_Str += " of"
	#Trace.Write("Action_Str--->"+str(Action_Str))
	return (
		table_header,
		data_list,
		table_id,
		filter_control_function,
		NORECORDS,
		dbl_clk_function,
		cv_list,
		filter_level_list,
		DropDownList,
		RelatedDrop_str,
		Test,
		Action_Str,
		QueryCount,
		page
	)


def GetSendingEquipmentMaster(PerPage, PageInform, A_Keys, A_Values):
	if str(PerPage) == "" and str(PageInform) == "":
		Page_start = 1
		Page_End = 10
		PerPage = 10
		PageInform = "1___10___10"
	else:
		Page_start = int(PageInform.split("___")[0])
		Page_End = int(PageInform.split("___")[1])
		PerPage = PerPage
	#Trace.Write("Page_start--->"+str(Page_start)+"Page_End--->"+str(Page_End)+"PerPage--->"+str(PerPage))    
	TreeParam = Product.GetGlobal("TreeParam")
	TreeParentParam = Product.GetGlobal("TreeParentLevel0")
	TreeSuperParentParam = Product.GetGlobal("TreeParentLevel1")
	TreeTopSuperParentParam =  Product.GetGlobal("TreeParentLevel2")
	ContractRecordId = Quote.GetGlobal("contract_quote_record_id")
	RevisionRecordId = Quote.GetGlobal("quote_revision_record_id")
	FablocationId = Product.GetGlobal("TreeParam")
	data_list = []
	obj_idval = "SYOBJ_003012_SYOBJ_003012"
	rec_id = "SYOBJ_003012"
	obj_id = "SYOBJ-003012"
	objh_getid = Sql.GetFirst(
		"SELECT TOP 1  RECORD_ID  FROM SYOBJH (NOLOCK) WHERE SAPCPQ_ATTRIBUTE_NAME='" + str(obj_id) + "'"
	)
	if objh_getid:
		obj_id = objh_getid.RECORD_ID
	objs_obj = Sql.GetFirst(
		"select CAN_ADD,CAN_EDIT,COLUMNS,CAN_DELETE from SYOBJR (NOLOCK) where OBJ_REC_ID = '" + str(obj_id) + "' "
	)
	can_edit = str(objs_obj.CAN_EDIT)
	can_add = str(objs_obj.CAN_ADD)
	can_delete = str(objs_obj.CAN_DELETE)
	table_id = "table_equipment_parent"
	table_header = (
		'<table id="'
		+ str(table_id)
		+ '"  data-pagination="false" data-sortable="true" data-search-on-enter-key="true" data-filter-control="true" data-pagination-loop = "false" data-locale = "en-US" ><thead>'
	)
	Columns = [
		"QUOTE_SERVICE_SENDING_FAB_LOC_EQUIP_ID",
		"SND_EQUIPMENT_ID",
		"EQUIPMENTCATEGORY_ID",
		"GREENBOOK",
		"SNDFBL_ID",
		"EQUIPMENT_STATUS",
		"PLATFORM",
		"MNT_PLANT_ID",
	]
	Objd_Obj = Sql.GetList(
		"select FIELD_LABEL,API_NAME,LOOKUP_OBJECT,LOOKUP_API_NAME,DATA_TYPE from SYOBJD (NOLOCK) where OBJECT_NAME = 'SAQSSE'"
	)
	attr_list = []
	attrs_datatype_dict = {}
	lookup_disply_list = []
	lookup_str = ""
	if Objd_Obj is not None:
		attr_list = {}
		for attr in Objd_Obj:
			attr_list[str(attr.API_NAME)] = str(attr.FIELD_LABEL)
			attrs_datatype_dict[str(attr.API_NAME)] = str(attr.DATA_TYPE)
			if attr.LOOKUP_API_NAME != "" and attr.LOOKUP_API_NAME is not None:
				lookup_disply_list.append(str(attr.API_NAME))
		checkbox_list = [inn.API_NAME for inn in Objd_Obj if inn.DATA_TYPE == "CHECKBOX"]
		lookup_list = {ins.LOOKUP_API_NAME: ins.API_NAME for ins in Objd_Obj}
#        if (("Sending Equipment" in TreeParam) or ("Receiving Equipment" in TreeParam)) and TreeSuperParentParam == 'Complementary Products':
#            Trace.Write('attr_list'+str(attr_list))
#            if 'FABLOCATION_ID' in attr_list:
#                fab_location_id  = attr_list['FABLOCATION_ID']
#                attr_list['FABLOCATION_ID'] = 'Sending Fab Location' if "Sending Account -" in TreeParam else 'Receiving Fab Location' if "Receiving Account -" in TreeParam else fab_location_id
		Trace.Write('attr_list111'+str(attr_list))
	lookup_str = ",".join(list(lookup_disply_list))
	orderby = ""
	if SortColumn != '' and SortColumnOrder !='':
		orderby = SortColumn + " " + SortColumnOrder
	else:
		orderby = "QUOTE_SERVICE_SENDING_FAB_LOC_EQUIP_ID"
	where_string = ""
	if A_Keys != "" and A_Values != "":
		A_Keys = list(A_Keys)
		A_Values = list(A_Values)
		for key, value in zip(A_Keys, A_Values):
			if value.strip():
				if where_string:
					where_string += " AND "
				where_string += "{Key} LIKE '%{Value}%'".format(Key=key, Value=value)
	Trace.Write('where string--->'+str(where_string))
	if (("Sending Equipment" in TreeParentParam) or ("Receiving Equipment" in TreeParentParam)):

		
		account_id = TreeParam.split(' - ')

		account_id = account_id[len(account_id)-1]
		fab_type = 'SENDING FAB' if "Sending Account -" in TreeParam else 'RECEIVING FAB' if "Receiving Account -" in TreeParam else ""
		get_fab_query = Sql.GetList("SELECT FABLOCATION_ID FROM SAQFBL WHERE QUOTE_RECORD_ID = '{}'  and QTEREV_RECORD_ID = '{}' and ACCOUNT_ID = '{}' and RELOCATION_FAB_TYPE = '{}'".format(ContractRecordId,RevisionRecordId,account_id,fab_type) )
		if get_fab_query:
			get_fab = "in "+ str(tuple([fab.FABLOCATION_ID for fab in get_fab_query])).replace(",)",')')
		else:
			get_fab = "= ''"
		Qstr = (
			"""select top {PerPage} * from ( select  ROW_NUMBER() OVER( ORDER BY {orderby}) AS ROW, QUOTE_SERVICE_SENDING_FAB_LOC_EQUIP_ID,SALESORG_ID,EQUIPMENTCATEGORY_ID,SND_EQUIPMENT_ID,MNT_PLANT_ID,GREENBOOK,QUOTE_NAME,SALESORG_NAME,SND_EQUIPMENT_DESCRIPTION,EQUIPMENT_STATUS,PLATFORM,SNDFBL_ID,QUOTE_ID,SNDFBL_NAME from SAQSSE (NOLOCK) where QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' and SNDFBL_ID = '{TreeParam}' {where_string} ) m where m.ROW BETWEEN {Page_start} and {Page_End} """.format(orderby = orderby, ContractRecordId = ContractRecordId,RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"),TreeParam = TreeParam, Page_start = Page_start, Page_End = Page_End,PerPage = PerPage,equp_type = 'SENDING EQUIPMENT' if "Sending Equipment" in TreeParam else "RECEIVING EQUIPMENT" if "Receiving Equipment" in TreeParam else "",where_string = " AND "+str(where_string) if str(where_string)!="" else "" ))

		QueryCount = ""

		QueryCountObj = Sql.GetFirst(
			"""select count(CpqTableEntryId) as cnt from SAQSSE (NOLOCK) where QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' and SNDFBL_ID = '{TreeParam}' {where_string}""".format(ContractRecordId = ContractRecordId,RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"),TreeParam = TreeParam, equp_type = 'SENDING EQUIPMENT' if "Sending Equipment" in TreeParam else "RECEIVING EQUIPMENT" if "Receiving Equipment" in TreeParam else "",where_string = " AND "+str(where_string) if str(where_string)!="" else "" )
		)
	elif (("Sending Equipment" in TreeSuperParentParam) or ("Receiving Equipment" in TreeSuperParentParam)):
		Qstr = (
			"""select top {PerPage} * from ( select  ROW_NUMBER() OVER( ORDER BY {orderby}) AS ROW, QUOTE_SERVICE_SENDING_FAB_LOC_EQUIP_ID,SALESORG_ID,EQUIPMENTCATEGORY_ID,SND_EQUIPMENT_ID,MNT_PLANT_ID,GREENBOOK,QUOTE_NAME,SALESORG_NAME,SND_EQUIPMENT_DESCRIPTION,EQUIPMENT_STATUS,PLATFORM,SNDFBL_ID,QUOTE_ID,SNDFBL_NAME from SAQSSE (NOLOCK) where QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' and SNDFBL_ID = '{TreeParentParam}' AND GREENBOOK = '{TreeParam}' {where_string}) m where m.ROW BETWEEN {Page_start} and {Page_End} """.format(orderby = orderby, ContractRecordId = ContractRecordId,RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"),TreeParentParam = TreeParentParam,TreeParam = TreeParam, Page_start = Page_start, Page_End = Page_End,PerPage = PerPage,equp_type = 'SENDING EQUIPMENT' if "Sending Equipment" in TreeParam else "RECEIVING EQUIPMENT" if "Receiving Equipment" in TreeParam else "",where_string = " AND "+str(where_string) if str(where_string)!="" else "" ) )

		QueryCount = ""

		QueryCountObj = Sql.GetFirst(
			"""select count(CpqTableEntryId) as cnt from SAQSSE (NOLOCK) where QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' and SNDFBL_ID = '{TreeParentParam}' and GREENBOOK = '{TreeParam}' {where_string}""".format(ContractRecordId = ContractRecordId,RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"),TreeParentParam = TreeParentParam,TreeParam = TreeParam, equp_type = 'SENDING EQUIPMENT' if "Sending Equipment" in TreeParentParam else "RECEIVING EQUIPMENT" if "Receiving Equipment" in TreeParentParam else "",where_string = " AND "+str(where_string) if str(where_string)!="" else "" )
		)
	elif ("Sending Equipment" in TreeParam) :
		Qstr = (
			"""select top {PerPage} * from ( select  ROW_NUMBER() OVER( ORDER BY {orderby}) AS ROW, QUOTE_SERVICE_SENDING_FAB_LOC_EQUIP_ID,SALESORG_ID,EQUIPMENTCATEGORY_ID,SND_EQUIPMENT_ID,MNT_PLANT_ID,GREENBOOK,QUOTE_NAME,SALESORG_NAME,SND_EQUIPMENT_DESCRIPTION,EQUIPMENT_STATUS,PLATFORM,SNDFBL_ID,QUOTE_ID,SNDFBL_NAME from SAQSSE (NOLOCK) where QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' and SERVICE_ID = '{TreeParentParam}' {where_string}) m where m.ROW BETWEEN {Page_start} and {Page_End} """.format(orderby = orderby, ContractRecordId = ContractRecordId, RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"), TreeParentParam = TreeParentParam, Page_start = Page_start, Page_End = Page_End,PerPage = PerPage,equp_type = 'SENDING EQUIPMENT' if "Sending Equipment" in TreeParam else "RECEIVING EQUIPMENT" if "Receiving Equipment" in TreeParam else "",where_string = " AND "+str(where_string) if str(where_string)!="" else "" ))

		QueryCount = ""

		QueryCountObj = Sql.GetFirst(
			"""select count(CpqTableEntryId) as cnt from SAQSSE (NOLOCK) where QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}'
			and SERVICE_ID = '{TreeParentParam}' {where_string}""".format(ContractRecordId = ContractRecordId,TreeParentParam = TreeParentParam,RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"),equp_type = 'SENDING EQUIPMENT' if "Sending Equipment" in TreeParentParam else "RECEIVING EQUIPMENT" if "Receiving Equipment" in TreeParentParam else "" ,where_string = " AND "+str(where_string) if str(where_string)!="" else "") )

	elif TreeParentParam == "Complementary Products":
		Qstr = (
			"""select top {PerPage} * from ( select  ROW_NUMBER() OVER( ORDER BY {orderby}) AS ROW, QUOTE_SERVICE_SENDING_FAB_LOC_EQUIP_ID,SALESORG_ID,EQUIPMENTCATEGORY_ID,SND_EQUIPMENT_ID,MNT_PLANT_ID,GREENBOOK,QUOTE_NAME,SALESORG_NAME,SND_EQUIPMENT_DESCRIPTION,EQUIPMENT_STATUS,PLATFORM,SNDFBL_ID,QUOTE_ID,SNDFBL_NAME from SAQSSE (NOLOCK) where QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' and SERVICE_ID = '{TreeParam}' {where_string}) m where m.ROW BETWEEN {Page_start} and {Page_End} """.format(orderby = orderby, ContractRecordId = ContractRecordId,RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"), TreeParam = TreeParam, Page_start = Page_start, Page_End = Page_End,PerPage = PerPage,equp_type = 'SENDING EQUIPMENT' if "Sending Equipment" in TreeParam else "RECEIVING EQUIPMENT" if "Receiving Equipment" in TreeParam else "",where_string=" AND "+str(where_string) if str(where_string)!="" else ""))

		QueryCount = ""

		QueryCountObj = Sql.GetFirst(
			"""select count(CpqTableEntryId) as cnt from SAQSSE (NOLOCK) where QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' and SERVICE_ID = '{TreeParam}' {where_string}""".format(ContractRecordId = ContractRecordId,RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"),TreeParam = TreeParam,equp_type = 'SENDING EQUIPMENT' if "Sending Equipment" in TreeParentParam else "RECEIVING EQUIPMENT" if "Receiving Equipment" in TreeParentParam else "",where_string=" AND "+str(where_string) if str(where_string)!="" else ""))            
	

	if QueryCountObj is not None:
		QueryCount = QueryCountObj.cnt
		#Trace.Write("count---->" + str(QueryCount))
	parent_obj = Sql.GetList(Qstr)
	for par in parent_obj:
		data_id = str(par.QUOTE_SERVICE_SENDING_FAB_LOC_EQUIP_ID)        
		Action_str = (
			'<div class="btn-group dropdown"><div class="dropdown" id="ctr_drop"><i data-toggle="dropdown" id="dropdownMenuButton" class="fa fa-sort-desc dropdown-toggle" aria-expanded="false"></i><ul class="dropdown-menu left" aria-labelledby="dropdownMenuButton"><li><a class="dropdown-item cur_sty" href="#" id="'
			+ str(data_id)
			+ '" onclick="Commonteree_view_RL(this)">VIEW</a></li>'
			'<li><a class="dropdown-item" id="deletebtn" data-target="#cont_CommonModalDelete" data-toggle="modal" onclick="CommonDelete(this, \'SAQFEA#'+ data_id +'\', \'WARNING\')" href="#">DELETE</a></li>'
		)
		if can_edit.upper() == "TRUE":
			Action_str += (
				'<li style="display:none" ><a class="dropdown-item cur_sty" href="#" id="'
				+ str(data_id)
				+ '" onclick="Move_to_parent_obj_edit(this)">EDIT</a></li>'
			)
		if can_delete.upper() == "TRUE":
			Action_str += '<li><a class="dropdown-item" data-target="#cont_viewModal_Material_Delete" data-toggle="modal" onclick="Material_delete_obj(this)" href="#">DELETE</a></li>'
		# if can_add.upper() == "TRUE" and par.MARKET_TYPE == "NON MARKET BASED" and par.MODEL_TYPE != "COST PLUS":
		#     Action_str += (
		#         '<li><a class="dropdown-item" id="'
		#         + str(data_id)
		#         + '" data-target="#" data-toggle="modal" onclick="Pricebook_clone_obj(this)" href="#">CLONE</a></li>'
		#     )
		Action_str += "</ul></div></div>"

		# Data formation in dictonary format.
		## hyperlink
		data_dict = {}
		data_dict["ids"] = str(data_id)
		data_dict["ACTIONS"] = str(Action_str)
		data_dict["QUOTE_SERVICE_SENDING_FAB_LOC_EQUIP_ID"] = CPQID.KeyCPQId.GetCPQId(
			"SAQSSE", str(par.QUOTE_SERVICE_SENDING_FAB_LOC_EQUIP_ID)
		)
		data_dict["EQUIPMENTCATEGORY_ID"] = ('<abbr id ="" title="' + str(par.EQUIPMENTCATEGORY_ID) + '">' + str(par.EQUIPMENTCATEGORY_ID) + "</abbr>") 
		data_dict["SND_EQUIPMENT_ID"] = ('<abbr id ="" title="' + str(par.SND_EQUIPMENT_ID) + '">' + str(par.SND_EQUIPMENT_ID) + "</abbr>")
		# data_dict["SERIAL_NUMBER"] = ('<abbr id ="" title="' + str(par.SERIAL_NUMBER) + '">' + str(par.SERIAL_NUMBER) + "</abbr>")
		# data_dict["CUSTOMER_TOOL_ID"] = ('<abbr id ="" title="' + str(par.CUSTOMER_TOOL_ID) + '">' + str(par.CUSTOMER_TOOL_ID) + "</abbr>")
		data_dict["GREENBOOK"] = ('<abbr id ="" title="' + str(par.GREENBOOK) + '">' + str(par.GREENBOOK) + "</abbr>")
		data_dict["SNDFBL_ID"] = ('<abbr id ="" title="' + str(par.SNDFBL_ID) + '">' + str(par.SNDFBL_ID) + "</abbr>")
		data_dict["EQUIPMENT_STATUS"] = ('<abbr id ="" title="' + str(par.EQUIPMENT_STATUS) + '">' + str(par.EQUIPMENT_STATUS) + "</abbr>")
		data_dict["PLATFORM"] = ('<abbr id ="" title="' + str(par.PLATFORM) + '">' + str(par.PLATFORM) + "</abbr>")
		data_dict["MNT_PLANT_ID"] = ('<abbr id ="" title="' + str(par.MNT_PLANT_ID) + '">' + str(par.MNT_PLANT_ID) + "</abbr>")
		# data_dict["FABLOCATION_ID"] = ('<abbr id ="" title="' + str(par.FABLOCATION_ID) + '">' + str(par.FABLOCATION_ID) + "</abbr>")
		# data_dict["WARRANTY_START_DATE"] = ('<abbr id ="" title="' + str(par.WARRANTY_START_DATE) + '">' + str(par.WARRANTY_START_DATE) + "</abbr>")
		# data_dict["WARRANTY_END_DATE"] = ('<abbr id ="" title="' + str(par.WARRANTY_END_DATE) + '">' + str(par.WARRANTY_END_DATE) + "</abbr>")
		data_list.append(data_dict)
		# Trace.Write("data_dict||data_dict||data_dict"+str(data_dict))
	hyper_link = ["QUOTE_SERVICE_SENDING_FAB_LOC_EQUIP_ID"]
	# if TreeTopSuperParentParam == "Fab Locations" and ("Sending Account -" in TreeSuperParentParam) or ("Receiving Account -" in TreeSuperParentParam):
	#     ParentObj = Sql.GetList(
	#         "select EQUIPMENT_ID from SAQFEQ (NOLOCK) where QUOTE_RECORD_ID = '{ContractRecordId}' and FABLOCATION_ID = '{FablocationId}'".format(
	#             ContractRecordId=Quote.GetGlobal("contract_quote_record_id"), FablocationId=Product.GetGlobal("TreeParentLevel0")
	#         )
	#     )
	# else:    
	#     ParentObj = Sql.GetList(
	#         "select EQUIPMENT_ID from SAQFEQ (NOLOCK) where QUOTE_RECORD_ID = '{ContractRecordId}' and FABLOCATION_ID = '{FablocationId}'".format(
	#             ContractRecordId=Quote.GetGlobal("contract_quote_record_id"), FablocationId=Product.GetGlobal("TreeParam")
	#         )
	#     )
	table_header += "<tr>"
	table_header += (
		'<th data-field="ACTIONS"><div class="action_col">ACTIONS</div><button class="searched_button" id="Act_'
		+ str(table_id)
		+ '">Search</button></th>'
	)
	table_header += '<th data-field="SELECT" class="wid45" data-checkbox="true"></th>'
	for key, invs in enumerate(list(Columns)):
		invs = str(invs).strip()
		qstring = attr_list.get(str(invs)) or ""
		if qstring == "":
			qstring = invs.replace("_", " ")
		if checkbox_list is not None and invs in checkbox_list:
			table_header += (
				'<th  data-field="'
				+ str(invs)
				+ '" data-filter-control="input" data-align="center" data-formatter="CheckboxFieldRelatedList" data-sortable="true"><abbr title="'
				+ str(qstring)
				+ '">'
				+ str(qstring)
				+ "</abbr></th>"
			)
		elif hyper_link is not None and invs in hyper_link:            
			table_header += (
				'<th data-field="'
				+ str(invs)
				+ '" data-filter-control="input" data-title-tooltip="'+str(qstring)+'" data-formatter="EquipHyperLinkTreeLink" data-sortable="true"'+ str(qstring)+'"><abbr title="'
				+ str(qstring)
				+ '">'
				+ str(qstring)
				+ "</abbr></th>"
			)
		else:            
			table_header += (
				'<th  data-field="'
				+ str(invs)
				+ '" data-filter-control="input"  data-title-tooltip="'+str(qstring)+'" data-sortable="true"><abbr title="'
				+ str(qstring)
				+ '">'
				+ str(qstring)
				+ "</abbr></th>"
			)

	table_header += "</tr>"
	table_header += '</thead><tbody onclick="Table_Onclick_Scroll(this)"></tbody></table>'
	table_ids = "#" + str(table_id)
	filter_control_function = ""
	tbl_id = table_id
	values_list = ""
	for key, invs in enumerate(list(Columns)):
		table_ids = "#" + str(table_id)
		filter_clas = "#" + str(table_id) + " .bootstrap-table-filter-control-" + str(invs)
		values_list += "var " + str(invs) + ' = $("' + str(filter_clas) + '").val(); '
		values_list += "ATTRIBUTE_VALUEList.push(" + str(invs) + "); "
	filter_class = "#Act_" + str(table_id)
	filter_control_function += (
	'$("'
	+ filter_class
	+ '").click( function(){ var table_id = $(this).closest("table").attr("id"); ATTRIBUTE_VALUEList = []; '
	+ str(values_list)
	+ ' var attribute_value = $(this).val(); cpq.server.executeScript("CQNESTGRID", {"TABNAME":"Sending Equipment Parent", "ACTION":"PRODUCT_ONLOAD_FILTER", "ATTRIBUTE_NAME": '
	+ str(list(Columns))
	+ ', "ATTRIBUTE_VALUE": ATTRIBUTE_VALUEList }, function(dataset) { data2 = dataset[1];  data1 = dataset[0]; data3 = dataset[2]; console.log("len ---->"+data1.length);  try { if(data1.length > 0) { $("#'
	+ str(tbl_id)
	+ '").bootstrapTable("load", data1 );$("#noRecDisp").remove(); if (document.getElementById("'+str(tbl_id) + '___totalItemCount")){document.getElementById("'+str(tbl_id)+ '___totalItemCount").innerHTML = data2;}  if (document.getElementById("'+str(tbl_id) + '___NumberofItem")) {document.getElementById("'+str(tbl_id)+ '___NumberofItem").innerHTML = data3;}} else{ $("#' + str(tbl_id) + '").bootstrapTable("load", data1  );$("#' + str(tbl_id) + '").after("<div id=\'noRecDisp\' class=\'noRecord\'>No Records to Display</div>"); $(".noRecord:not(:first)").remove(); if (document.getElementById("'+str(tbl_id) + '___totalItemCount")){document.getElementById("'+str(tbl_id)+ '___totalItemCount").innerHTML = data2;}  if (document.getElementById("'+str(tbl_id) + '___NumberofItem")) {document.getElementById("'+str(tbl_id)+ '___NumberofItem").innerHTML = data3;} }} catch(err){} }); filter_search_click();$(".JColResizer").mousedown(function(){ $("thead.fullHeadFirst").css("cssText","z-index: 2;border-top: 1px solid rgb(220, 220, 220);top: 154px;border-right: 0px !important;");$("thead.fullHeadSecond").css("display","none"); });$(".JColResizer").mouseup(function(){ var th_width_resize = [];$("#table_equipment_parent thead.fullHeadFirst tr th").each(function(index){var wid = $(this).css("width"); if(index ==0 || index ==1){th_width_resize.push("60px");}else{th_width_resize.push(wid);}}); $("thead.fullHeadFirst").css("cssText","position: fixed;z-index: 2;border-top: 1px solid rgb(220, 220, 220); top: 154px;border-right: 0px !important;");$("thead.fullHeadSecond").css("display","table-header-group");$("#table_equipment_parent thead.fullHeadFirst tr th").each(function(index){var num = th_width_resize[index].split("px");var numsp = parseInt(num[0]);numsp = numsp - 1;var make_str =numsp+"px"; var c = "width:"+make_str+";white-space: nowrap;overflow: hidden;text-overflow: ellipsis;";var d = "width:"+make_str+";"; $(this).css("cssText",c);$(this).children("div:first-child").css("cssText",c);$(this).children("div.fht-cell").css("cssText",d);});$("#table_equipment_parent thead.fullHeadSecond tr th").each(function(index){var num = th_width_resize[index].split("px");var numsp = parseInt(num[0]);numsp = numsp - 1;var make_str =numsp+"px"; var c = "width:"+make_str+";white-space: nowrap;overflow: hidden;text-overflow: ellipsis;";var d = "width:"+make_str+";"; $(this).css("cssText",c);$(this).children("div:first-child").css("cssText",c);$(this).children("div.fht-cell").css("cssText",d);}); });});')
	
	#Trace.Write("666 filter_control_function ---->"+str(filter_control_function))

	dbl_clk_function = (
		'$("'
		+ str(table_ids)
		+ '").on("all.bs.table", function (e, name, args) { $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); }); $("'
		+ str(table_ids)
		+ '\ th.bs-checkbox div.th-inner").before("<div style=\'padding:0; border-bottom: 1px solid #dcdcdc;\'>SELECT</div>"); $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); $("'
		+ str(table_ids)
		+ "\").on('sort.bs.table', function (e, name, order) {  console.log('Parent sort.bs.table ====> ', e); currenttab = $(\"ul#carttabs_head .active\").text().trim(); localStorage.setItem('"
		+ str(table_id)
		+ "_SortColumn', name); localStorage.setItem('"
		+ str(table_id)
		+ "_SortColumnOrder', order); NestedContainerSorting(name, order, '"
		+ str(table_id)
		+ "'); }); "
		)
	NORECORDS = ""
	if len(data_list) == 0:
		NORECORDS = "NORECORDS"

	ObjectName = "SAQSSE"
	DropDownList = []
	filter_level_list = []
	filter_clas_name = ""
	cv_list = []
	TableclassName = "form-control" + table_id
	for key, col_name in enumerate(list(Columns)):
		StringValue_list = []
		objss_obj = Sql.GetFirst(
			"SELECT API_NAME, DATA_TYPE, FORMULA_LOGIC, PICKLIST FROM SYOBJD (NOLOCK) WHERE OBJECT_NAME='"
			+ str(ObjectName)
			+ "' and API_NAME = '"
			+ str(col_name)
			+ "'"
		)
		try:
			FORMULA_LOGIC = objss_obj.FORMULA_LOGIC.strip()
			FORMULA_col = FORMULA_LOGIC.split(" ")[1].strip()
			FORMULA_table = FORMULA_LOGIC.split(" ")[3].strip()
			ins_obj = Sql.GetFirst(
				"SELECT API_NAME, DATA_TYPE,PICKLIST FROM SYOBJD (NOLOCK) WHERE OBJECT_NAME='"
				+ str(FORMULA_table)
				+ "' and API_NAME = '"
				+ str(FORMULA_col)
				+ "'"
			)
			if str(objss_obj.PICKLIST).upper() == "TRUE":
				filter_level_data = "select"
				filter_clas_name = (
					'<div id = "'
					+ str(table_id)
					+ "_RelatedMutipleCheckBoxDrop_"
					+ str(key)
					+ '" class="form-control bootstrap-table-filter-control-'
					+ str(col_name)
					+ " RelatedMutipleCheckBoxDrop_"
					+ str(key)
					+ ' "></div>'
				)
				filter_level_list.append(filter_level_data)
			else:
				filter_level_data = "input"
				filter_clas_name = (
					'<input type="text" class="width100_vis form-control bootstrap-table-filter-control-'
					+ str(col_name)
					+ '">'
				)
				filter_level_list.append(filter_level_data)
		except:
			Trace.Write("except---->")
			if str(objss_obj.PICKLIST).upper() == "TRUE":
				filter_level_data = "select"
				filter_clas_name = (
					'<div id = "'
					+ str(table_id)
					+ "_RelatedMutipleCheckBoxDrop_"
					+ str(key)
					+ '" class="form-control bootstrap-table-filter-control-'
					+ str(col_name)
					+ " RelatedMutipleCheckBoxDrop_"
					+ str(key)
					+ ' "></div>'
				)
				filter_level_list.append(filter_level_data)

			filter_level_data = "input"
			filter_clas_name = (
				'<input type="text" class="width100_vis form-control bootstrap-table-filter-control-' + str(col_name) + '">'
			)
			filter_level_list.append(filter_level_data)
		cv_list.append(filter_clas_name)
		if filter_level_data == "select":
			try:
				xcd = Sql.GetFirst(
					"SELECT (STUFF((SELECT DISTINCT ', ' + CAST("
					+ str(col_name)
					+ " AS CHAR(100)) FROM "
					+ str(ObjectName)
					+ " FOR XML PATH('') ), 1, 2, '')  ) AS StringValue"
				)
			except:
				xcd = Sql.GetFirst(
					"SELECT (STUFF((SELECT DISTINCT ', ' + CAST("
					+ str(col_name)
					+ " AS CHAR(100)) FROM "
					+ str(ObjectName)
					+ " FOR XML PATH('') ), 1, 2, '')  ) AS StringValue"
				)
			if str(xcd.StringValue) is not None and str(xcd.StringValue) != "":
				if str(xcd.StringValue).find(",") != -1:
					StringValue_list = [ins.strip() for ins in str(xcd.StringValue).split(",") if ins.strip() != ""]
				else:
					StringValue_list.append(str(xcd.StringValue))
			else:
				StringValue_list = [""]
			StringValue_list = list(set(StringValue_list))
			DropDownList.append(StringValue_list)
		elif filter_level_data == "checkbox":
			DropDownList.append(["True", "False"])
		else:
			DropDownList.append("")
	RelatedDrop_str = (
		"try { if( document.getElementById('"
		+ str(table_id)
		+ "') ) { var listws = document.getElementById('"
		+ str(table_id)
		+ "').getElementsByClassName('filter-control');  for (i = 0; i < listws.length; i++) { document.getElementById('"
		+ str(table_id)
		+ "').getElementsByClassName('filter-control')[i].innerHTML = data6[i];  } for (j = 0; j < listws.length; j++) { if (data7[j] == 'select') { if (data8[j]) { var dataAdapter = new $.jqx.dataAdapter(data8[j]); $('#"
		+ str(table_id)
		+ "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter, autoDropDownHeight: true }); } } } } }  catch(err) { setTimeout(function() { var listws = document.getElementById('"
		+ str(table_id)
		+ "').getElementsByClassName('filter-control');  for (i = 0; i < listws.length; i++) { document.getElementById('"
		+ str(table_id)
		+ "').getElementsByClassName('filter-control')[i].innerHTML = data6[i];  } for (j = 0; j < listws.length; j++) { if (data7[j] == 'select') { if (data8[j]) { var dataAdapter = new $.jqx.dataAdapter(data8[j]); $('#"
		+ str(table_id)
		+ "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter, autoDropDownHeight: true }); } } } }, 5000); }"
	)
	page = ""
	if QueryCount < int(PerPage):
		page = str(Page_start) + " - " + str(QueryCount)
	else:
		page = str(Page_start) + " - " + str(Page_End)
	#Trace.Write("page----->"+str(page))    
	Test = (
		'<div class="col-md-12 brdr listContStyle pad2height30" ><div class="col-md-4 pager-numberofitem clear-padding"><span class="pager-number-of-items-item noofitem" id="'
		+ str(table_id)
		+ '___NumberofItem" >'
		+ str(page)
		+ ' of</span><span class="pager-number-of-items-item fltltpad2mrg0" id="'
		+ str(table_id)
		+ '___totalItemCount" >'
		+ str(QueryCount)
		+ '</span><div class="clear-padding fltltmrgtp3" ><div  class="pull-right vertmidtxtrht"><select onchange="PageFunctestChild(this,\'Quote\',\'\',\'table_equipment_parent\')" id="'
		+ str(table_id)
		+ '___PageCountValue" class="form-control wid65vermiddisinbmarl5"><option value="10" selected>10</option><option value="20">20</option><option value="50">50</option><option value="100">100</option><option value="200">200</option></select> </div></div></div><div class="col-xs-8 col-md-4  clear-padding disinpad10txtcen"  data-bind="visible: totalItemCount"><div class="clear-padding col-xs-12 col-sm-6 col-md-12 bor0" ><ul class="pagination pagination"><li class="disabled"><a href="#" onclick="FirstPageLoad_paginationChild(\'Quote\',\'\',\'table_equipment_parent\')"><i class="fa fa-caret-left font14whtbld" ></i><i class="fa fa-caret-left font14" ></i></a></li><li class="disabled"><a href="#" onclick="Previous12334Child(\'Quote\',\'\',\'table_equipment_parent\')"><i class="fa fa-caret-left font14" ></i>PREVIOUS</a></li><li class="disabled"><a href="#" class="disabledPage" onclick="Next12334Child(\'Quote\',\'\',\'table_equipment_parent\')">NEXT<i class="fa fa-caret-right font14" ></i></a></li><li class="disabled"><a href="#" onclick="LastPageLoad_paginationChild(\'Quote\',\'\',\'table_equipment_parent\')" class="disabledPage"><i class="fa fa-caret-right font14"></i><i class="fa fa-caret-right font14whtbld"></i></a></li></ul></div> </div> <div class="col-md-4 pr_page_pad"> <span id="'
		+ str(table_id)
		+ '___page_count" class="currentPage page_right_content">1</span><span class="page_right_content pad_rt_2">Page </span></div></div>'
	)
	#Log.Info("Equipment Grid table_header--->"+str(table_header)+"Equipment Grid data_list--->"+str(data_list))
	if QueryCount < int(PerPage):
		PerPage = str(QueryCount)
	else:
		PerPage = str(PerPage)   
	if Page_End > QueryCount:
		Page_End = QueryCount
	else:
		Page_End = Page_End
	#Trace.Write("Page_End----->"+str(Page_End))    
	Action_Str = ""
	#Action_Str = "1 - "
	Action_Str += str(Page_start)+" - "
	Action_Str += str(Page_End)
	Action_Str += " of"
	#Trace.Write("Action_Str--->"+str(Action_Str))
	return (
		table_header,
		data_list,
		table_id,
		filter_control_function,
		NORECORDS,
		dbl_clk_function,
		cv_list,
		filter_level_list,
		DropDownList,
		RelatedDrop_str,
		Test,
		Action_Str,
		QueryCount,
		page
	)


def GetContractEquipmentMaster(PerPage, PageInform, A_Keys, A_Values):
	if str(PerPage) == "" and str(PageInform) == "":
		Page_start = 1
		Page_End = 10
		PerPage = 10
		PageInform = "1___10___10"
	else:
		Page_start = int(PageInform.split("___")[0])
		Page_End = int(PageInform.split("___")[1])
		PerPage = PerPage
	TreeParam = Product.GetGlobal("TreeParam")
	TreeParentParam = Product.GetGlobal("TreeParentLevel0")
	TreeSuperParentParam = Product.GetGlobal("TreeParentLevel1")
	ContractRecordId = Product.GetGlobal("contract_record_id")
	FablocationId = Product.GetGlobal("TreeParam")
	data_list = []
	obj_idval = "SYOBJ_00993_SYOBJ_00993"
	rec_id = "SYOBJ_00993"
	obj_id = "SYOBJ-00993"
	objh_getid = Sql.GetFirst(
		"SELECT TOP 1  RECORD_ID  FROM SYOBJH (NOLOCK) WHERE SAPCPQ_ATTRIBUTE_NAME='" + str(obj_id) + "'"
	)
	if objh_getid:
		obj_id = objh_getid.RECORD_ID
	objs_obj = Sql.GetFirst(
		"select CAN_ADD,CAN_EDIT,COLUMNS,CAN_DELETE from SYOBJR (NOLOCK) where OBJ_REC_ID = '" + str(obj_id) + "' "
	)
	can_edit = str(objs_obj.CAN_EDIT)
	can_add = str(objs_obj.CAN_ADD)
	can_delete = str(objs_obj.CAN_DELETE)
	table_id = "table_Contract_equipment_parent"
	table_header = (
		'<table id="'
		+ str(table_id)
		+ '"  data-pagination="false" data-sortable="true" data-search-on-enter-key="true" data-filter-control="true" data-pagination-loop = "false" data-locale = "en-US" ><thead>'
	)
	Columns = [
		"CONTRACT_FAB_LOC_GB_EQUIPMENT_RECORD_ID",
		"EQUIPMENT_ID",
		"EQUIPMENTCATEGORY_ID",
		"SERIAL_NUMBER",
		"CUSTOMER_TOOL_ID",
		"GREENBOOK",
		"EQUIPMENT_STATUS",
		"PLATFORM",
		"MNT_PLANT_ID",
		"FABLOCATION_ID",
		"WARRANTY_START_DATE",
		"WARRANTY_END_DATE",
	]
	Objd_Obj = Sql.GetList(
		"select FIELD_LABEL,API_NAME,LOOKUP_OBJECT,LOOKUP_API_NAME,DATA_TYPE from SYOBJD (NOLOCK) where OBJECT_NAME = 'CTCFEQ'"
	)
	attr_list = []
	attrs_datatype_dict = {}
	lookup_disply_list = []
	lookup_str = ""
	if Objd_Obj is not None:
		attr_list = {}
		for attr in Objd_Obj:
			attr_list[str(attr.API_NAME)] = str(attr.FIELD_LABEL)
			attrs_datatype_dict[str(attr.API_NAME)] = str(attr.DATA_TYPE)
			if attr.LOOKUP_API_NAME != "" and attr.LOOKUP_API_NAME is not None:
				lookup_disply_list.append(str(attr.API_NAME))
		checkbox_list = [inn.API_NAME for inn in Objd_Obj if inn.DATA_TYPE == "CHECKBOX"]
		lookup_list = {ins.LOOKUP_API_NAME: ins.API_NAME for ins in Objd_Obj}
	lookup_str = ",".join(list(lookup_disply_list))
	if TreeSuperParentParam == "Fab Locations":
		Qstr = (
			"select top "
			+ str(PerPage)
			+ " * from ( select  ROW_NUMBER() OVER( ORDER BY CONTRACT_FAB_LOC_GB_EQUIPMENT_RECORD_ID) AS ROW, CONTRACT_FAB_LOC_GB_EQUIPMENT_RECORD_ID,EQUIPMENTCATEGORY_ID,EQUIPMENT_ID,MNT_PLANT_ID,CUSTOMER_TOOL_ID,SERIAL_NUMBER,GREENBOOK,EQUIPMENT_STATUS,PLATFORM,FABLOCATION_ID,WARRANTY_START_DATE,WARRANTY_END_DATE from CTCFEQ (NOLOCK) where CONTRACT_RECORD_ID = '"
			+ str(ContractRecordId)
			+ "' and GREENBOOK = '"
			+ str(FablocationId)
			+ "' and FABLOCATION_ID = '"
			+ str(TreeParentParam)
			+ "') m where m.ROW BETWEEN "
			+ str(Page_start)
			+ " and "
			+ str(Page_End)
		)
		QueryCount = ""
		QueryCountObj = Sql.GetFirst(
			"select count(CONTRACT_FAB_LOC_GB_EQUIPMENT_RECORD_ID) as cnt from CTCFEQ (NOLOCK) where CONTRACT_RECORD_ID = '"
			+ str(ContractRecordId)
			+ "' and GREENBOOK = '"
			+ str(TreeParam)
			+ "' and FABLOCATION_ID = '"
			+ str(TreeParentParam)
			+ "'"
		)
	elif TreeParam == "Fab Locations":
		Qstr = (
			"select top "
			+ str(PerPage)
			+ " * from ( select  ROW_NUMBER() OVER( ORDER BY CONTRACT_FAB_LOC_GB_EQUIPMENT_RECORD_ID) AS ROW, CONTRACT_FAB_LOC_GB_EQUIPMENT_RECORD_ID,EQUIPMENTCATEGORY_ID,EQUIPMENT_ID,MNT_PLANT_ID,CUSTOMER_TOOL_ID,SERIAL_NUMBER,GREENBOOK,EQUIPMENT_STATUS,PLATFORM,FABLOCATION_ID,WARRANTY_START_DATE,WARRANTY_END_DATE from CTCFEQ (NOLOCK) where CONTRACT_RECORD_ID = '"
			+ str(ContractRecordId)
			+ "') m where m.ROW BETWEEN "
			+ str(Page_start)
			+ " and "
			+ str(Page_End)
		)
		QueryCount = ""
		QueryCountObj = Sql.GetFirst(
			"select count(CONTRACT_FAB_LOC_GB_EQUIPMENT_RECORD_ID) as cnt from CTCFEQ (NOLOCK) where CONTRACT_RECORD_ID = '"
			+ str(ContractRecordId)
			+ "'"
		)
	else:
		Qstr = (
			"select top "
			+ str(PerPage)
			+ " * from ( select  ROW_NUMBER() OVER( ORDER BY CONTRACT_FAB_LOC_GB_EQUIPMENT_RECORD_ID) AS ROW, CONTRACT_FAB_LOC_GB_EQUIPMENT_RECORD_ID,EQUIPMENTCATEGORY_ID,EQUIPMENT_ID,MNT_PLANT_ID,CUSTOMER_TOOL_ID,SERIAL_NUMBER,GREENBOOK,EQUIPMENT_STATUS,PLATFORM,FABLOCATION_ID,WARRANTY_START_DATE,WARRANTY_END_DATE from CTCFEQ (NOLOCK) where CONTRACT_RECORD_ID = '"
			+ str(ContractRecordId)
			+ "' and FABLOCATION_ID = '"
			+ str(FablocationId)
			+ "') m where m.ROW BETWEEN "
			+ str(Page_start)
			+ " and "
			+ str(Page_End)
		)
		QueryCount = ""

		QueryCountObj = Sql.GetFirst(
			"select count(CONTRACT_FAB_LOC_GB_EQUIPMENT_RECORD_ID) as cnt from CTCFEQ (NOLOCK) where CONTRACT_RECORD_ID = '"
			+ str(ContractRecordId)
			+ "' and FABLOCATION_ID = '"
			+ str(FablocationId)
			+ "' "
		)

	if QueryCountObj is not None:
		QueryCount = QueryCountObj.cnt
		#Trace.Write("count---->" + str(QueryCount))
	parent_obj = Sql.GetList(Qstr)
	for par in parent_obj:
		data_id = str(par.CONTRACT_FAB_LOC_GB_EQUIPMENT_RECORD_ID)

		Action_str = (
			'<div class="btn-group dropdown"><div class="dropdown" id="ctr_drop"><i data-toggle="dropdown" id="dropdownMenuButton" class="fa fa-sort-desc dropdown-toggle" aria-expanded="false"></i><ul class="dropdown-menu left" aria-labelledby="dropdownMenuButton"><li><a class="dropdown-item cur_sty" href="#" id="'
			+ str(data_id)
			+ '" onclick="Commonteree_view_RL(this)">VIEW</a></li>'
			'<li style="display:none"><a class="dropdown-item" id="deletebtn" data-target="#cont_CommonModalDelete" data-toggle="modal" onclick="CommonDelete(this, \'CTCFEQ#'+ data_id +'\', \'WARNING\')" style= "display"href="#">DELETE</a></li>'
		)
		if can_edit.upper() == "TRUE":
			Action_str += (
				'<li style="display:none" ><a class="dropdown-item cur_sty" href="#" id="'
				+ str(data_id)
				+ '" onclick="Move_to_parent_obj_edit(this)">EDIT</a></li>'
			)
		if can_delete.upper() == "TRUE":
			Action_str += '<li><a class="dropdown-item" data-target="#cont_viewModal_Material_Delete" data-toggle="modal" onclick="Material_delete_obj(this)" href="#">DELETE</a></li>'
		if can_add.upper() == "TRUE" and par.MARKET_TYPE == "NON MARKET BASED" and par.MODEL_TYPE != "COST PLUS":
			Action_str += (
				'<li><a class="dropdown-item" id="'
				+ str(data_id)
				+ '" data-target="#" data-toggle="modal" onclick="Pricebook_clone_obj(this)" href="#">CLONE</a></li>'
			)
		Action_str += "</ul></div></div>"

		# Data formation in dictonary format.
		## hyperlink
		data_dict = {}
		data_dict["ids"] = str(data_id)
		data_dict["ACTIONS"] = str(Action_str)
		data_dict["CONTRACT_FAB_LOC_GB_EQUIPMENT_RECORD_ID"] = CPQID.KeyCPQId.GetCPQId(
			"CTCFEQ", str(par.CONTRACT_FAB_LOC_GB_EQUIPMENT_RECORD_ID)
		)
		data_dict["EQUIPMENTCATEGORY_ID"] = str(par.EQUIPMENTCATEGORY_ID)
		data_dict["EQUIPMENT_ID"] = str(par.EQUIPMENT_ID)
		data_dict["SERIAL_NUMBER"] = str(par.SERIAL_NUMBER)
		data_dict["CUSTOMER_TOOL_ID"] = str(par.CUSTOMER_TOOL_ID)
		data_dict["GREENBOOK"] = str(par.GREENBOOK)
		data_dict["EQUIPMENT_STATUS"] = str(par.EQUIPMENT_STATUS)
		data_dict["PLATFORM"] = str(par.PLATFORM)
		data_dict["MNT_PLANT_ID"] = str(par.MNT_PLANT_ID)
		data_dict["FABLOCATION_ID"] = str(par.FABLOCATION_ID)
		data_dict["WARRANTY_START_DATE"] = str(par.WARRANTY_START_DATE)
		data_dict["WARRANTY_END_DATE"] = str(par.WARRANTY_END_DATE)
		data_list.append(data_dict)
		
	hyper_link = ["CONTRACT_FAB_LOC_GB_EQUIPMENT_RECORD_ID"]
	ParentObj = Sql.GetList(
		"select EQUIPMENT_ID from CTCFEQ (NOLOCK) where CONTRACT_RECORD_ID = '{ContractRecordId}' and FABLOCATION_ID = '{FablocationId}'".format(
			ContractRecordId=Product.GetGlobal("contract_record_id"), FablocationId=Product.GetGlobal("TreeParam")
		)
	)
	table_header += "<tr>"
	table_header += (
		'<th data-field="ACTIONS"><div class="action_col">ACTIONS</div><button class="searched_button" id="Act_'
		+ str(table_id)
		+ '">Search</button></th>'
	)
	table_header += '<th data-field="SELECT" class="wid45" data-checkbox="true"></th>'
	for key, invs in enumerate(list(Columns)):
		invs = str(invs).strip()
		qstring = attr_list.get(str(invs)) or ""
		if qstring == "":
			qstring = invs.replace("_", " ")
		if checkbox_list is not None and invs in checkbox_list:
			table_header += (
				'<th  data-field="'
				+ str(invs)
				+ '" data-filter-control="input" data-align="center" data-formatter="CheckboxFieldRelatedList" data-sortable="true"><abbr title="'
				+ str(qstring)
				+ '">'
				+ str(qstring)
				+ "</abbr></th>"
			)
		elif hyper_link is not None and invs in hyper_link:            
			# if TreeParam == "Fab Locations" or TreeParentParam == "Fab Locations":
			#     table_header += (
			#     '<th data-field="'
			#     + str(invs)
			#     + '" data-filter-control="input" data-formatter="" data-sortable="true"><abbr title="'
			#     + str(qstring)
			#     + '">'
			#     + str(qstring)
			#     + "</abbr></th>"
			#     )
			# else:
			table_header += (
				'<th data-field="'
				+ str(invs)
				+ '" data-filter-control="input" data-formatter="ContractEquipHyperLinkTreeLink" data-sortable="true"><abbr title="'
				+ str(qstring)
				+ '">'
				+ str(qstring)
				+ "</abbr></th>"
			)
		else:
			table_header += (
				'<th  data-field="'
				+ str(invs)
				+ '" data-filter-control="input" data-sortable="true"><abbr title="'
				+ str(qstring)
				+ '">'
				+ str(qstring)
				+ "</abbr></th>"
			)
	table_header += "</tr>"
	table_header += '</thead><tbody onclick="Table_Onclick_Scroll(this)"></tbody></table>'
	table_ids = "#" + str(table_id)
	filter_control_function = ""
	values_list = ""
	tbl_id = str(table_id)
	for key, invs in enumerate(list(Columns)):
		table_ids = "#" + str(table_id)
		filter_clas = "#" + str(table_id) + " .bootstrap-table-filter-control-" + str(invs)
		values_list += "var " + str(invs) + ' = $("' + str(filter_clas) + '").val(); '
		values_list += "ATTRIBUTE_VALUEList.push(" + str(invs) + "); "
		tbl_id = str(table_id)
	filter_class = "#Act_" + str(table_id)
	filter_control_function += (
		'$("'
		+ filter_class
		+ '").click( function(){ var table_id = $(this).closest("table").attr("id"); ATTRIBUTE_VALUEList = []; '
		+ str(values_list)
		+ ' var attribute_value = $(this).val(); cpq.server.executeScript("CQNESTGRID", {"TABNAME":"Contract Equipment Parent", "ACTION":"PRODUCT_ONLOAD_FILTER", "ATTRIBUTE_NAME": '
		+ str(list(Columns))
		+ ', "ATTRIBUTE_VALUE": ATTRIBUTE_VALUEList }, function(dataset) { data2 = dataset[1];  data1 = dataset[0]; data3 = dataset[2]; console.log("len ---->"+data1.length);  try { if(data1.length > 0) { $("#'+ str(tbl_id) + '").bootstrapTable("load", data1 );$("#noRecDisp").remove(); if (document.getElementById("'+str(tbl_id) + '___totalItemCount")){document.getElementById("'+str(tbl_id)+ '___totalItemCount").innerHTML = data2;}  if (document.getElementById("'+str(tbl_id) + '___NumberofItem")) {document.getElementById("'+str(tbl_id)+ '___NumberofItem").innerHTML = data3;}} else{ $("#' + str(tbl_id) + '").bootstrapTable("load", data1  );$("#' + str(tbl_id) + '").after("<div id=\'noRecDisp\' class=\'noRecord\'>No Records to Display</div>"); $(".noRecord:not(:first)").remove(); if (document.getElementById("'+str(tbl_id) + '___totalItemCount")){document.getElementById("'+str(tbl_id)+ '___totalItemCount").innerHTML = data2;}  if (document.getElementById("'+str(tbl_id) + '___NumberofItem")) {document.getElementById("'+str(tbl_id)+ '___NumberofItem").innerHTML = data3;} }} catch(err){} }); filter_search_click();$(".JColResizer").mousedown(function(){ $("thead.fullHeadFirst").css("cssText","z-index: 2;border-top: 1px solid rgb(220, 220, 220);top: 154px;border-right: 0px !important;");$("thead.fullHeadSecond").css("display","none"); });$(".JColResizer").mouseup(function(){ var th_width_resize = [];$("#table_equipment_parent thead.fullHeadFirst tr th").each(function(index){var wid = $(this).css("width"); if(index ==0 || index ==1){th_width_resize.push("60px");}else{th_width_resize.push(wid);}}); $("thead.fullHeadFirst").css("cssText","position: fixed;z-index: 2;border-top: 1px solid rgb(220, 220, 220); top: 154px;border-right: 0px !important;");$("thead.fullHeadSecond").css("display","table-header-group");$("#table_equipment_parent thead.fullHeadFirst tr th").each(function(index){var num = th_width_resize[index].split("px");var numsp = parseInt(num[0]);numsp = numsp - 1;var make_str =numsp+"px"; var c = "width:"+make_str+";white-space: nowrap;overflow: hidden;text-overflow: ellipsis;";var d = "width:"+make_str+";"; $(this).css("cssText",c);$(this).children("div:first-child").css("cssText",c);$(this).children("div.fht-cell").css("cssText",d);});$("#table_equipment_parent thead.fullHeadSecond tr th").each(function(index){var num = th_width_resize[index].split("px");var numsp = parseInt(num[0]);numsp = numsp - 1;var make_str =numsp+"px"; var c = "width:"+make_str+";white-space: nowrap;overflow: hidden;text-overflow: ellipsis;";var d = "width:"+make_str+";"; $(this).css("cssText",c);$(this).children("div:first-child").css("cssText",c);$(this).children("div.fht-cell").css("cssText",d);}); });});'
	)
	dbl_clk_function = (
		'$("'
		+ str(table_ids)
		+ '").on("all.bs.table", function (e, name, args) { $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); }); $("'
		+ str(table_ids)
		+ '\ th.bs-checkbox div.th-inner").before("<div style=\'padding:0; border-bottom: 1px solid #dcdcdc;\'>SELECT</div>"); $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); $("'
		+ str(table_ids)
		+ "\").on('sort.bs.table', function (e, name, order) { console.log('sort.bs.table ============>111111111');  currenttab = $(\"ul#carttabs_head .active\").text().trim(); localStorage.setItem('"
		+ str(table_id)
		+ "_SortColumn', name); localStorage.setItem('"
		+ str(table_id)
		+ "_SortColumnOrder', order); NestedContainerSorting(name, order, '"
		+ str(table_id)
		+ "'); }); "
		)
	#Trace.Write("GetContractEquipmentMaster --- dbl_clk_function ---->"+str(dbl_clk_function))
	NORECORDS = ""
	if len(data_list) == 0:
		NORECORDS = "NORECORDS"

	ObjectName = "CTCFEQ"
	DropDownList = []
	filter_level_list = []
	filter_clas_name = ""
	cv_list = []
	TableclassName = "form-control" + table_id
	for key, col_name in enumerate(list(Columns)):
		StringValue_list = []
		objss_obj = Sql.GetFirst(
			"SELECT API_NAME, DATA_TYPE, FORMULA_LOGIC, PICKLIST FROM SYOBJD (NOLOCK) WHERE OBJECT_NAME='"
			+ str(ObjectName)
			+ "' and API_NAME = '"
			+ str(col_name)
			+ "'"
		)
		try:
			FORMULA_LOGIC = objss_obj.FORMULA_LOGIC.strip()
			FORMULA_col = FORMULA_LOGIC.split(" ")[1].strip()
			FORMULA_table = FORMULA_LOGIC.split(" ")[3].strip()
			ins_obj = Sql.GetFirst(
				"SELECT API_NAME, DATA_TYPE,PICKLIST FROM SYOBJD (NOLOCK) WHERE OBJECT_NAME='"
				+ str(FORMULA_table)
				+ "' and API_NAME = '"
				+ str(FORMULA_col)
				+ "'"
			)
			if str(objss_obj.PICKLIST).upper() == "TRUE":
				filter_level_data = "select"
				filter_clas_name = (
					'<div id = "'
					+ str(table_id)
					+ "_RelatedMutipleCheckBoxDrop_"
					+ str(key)
					+ '" class="form-control bootstrap-table-filter-control-'
					+ str(col_name)
					+ " RelatedMutipleCheckBoxDrop_"
					+ str(key)
					+ ' "></div>'
				)
				filter_level_list.append(filter_level_data)
			else:
				filter_level_data = "input"
				filter_clas_name = (
					'<input type="text" class="width100_vis form-control bootstrap-table-filter-control-'
					+ str(col_name)
					+ '">'
				)
				filter_level_list.append(filter_level_data)
		except:
			"""if str(objss_obj.PICKLIST).upper() == "TRUE":
				filter_level_data = "select"
				filter_clas_name = (
					'<div id = "'
					+ str(table_id)
					+ "_RelatedMutipleCheckBoxDrop_"
					+ str(key)
					+ '" class="form-control bootstrap-table-filter-control-'
					+ str(col_name)
					+ " RelatedMutipleCheckBoxDrop_"
					+ str(key)
					+ ' "></div>'
				)
				filter_level_list.append(filter_level_data)"""

			filter_level_data = "input"
			filter_clas_name = (
				'<input type="text" class="width100_vis form-control bootstrap-table-filter-control-' + str(col_name) + '">'
			)
			filter_level_list.append(filter_level_data)
		cv_list.append(filter_clas_name)
		if filter_level_data == "select":
			try:
				xcd = Sql.GetFirst(
					"SELECT (STUFF((SELECT DISTINCT ', ' + CAST("
					+ str(col_name)
					+ " AS CHAR(100)) FROM "
					+ str(ObjectName)
					+ " FOR XML PATH('') ), 1, 2, '')  ) AS StringValue"
				)
			except:
				xcd = Sql.GetFirst(
					"SELECT (STUFF((SELECT DISTINCT ', ' + CAST("
					+ str(col_name)
					+ " AS CHAR(100)) FROM "
					+ str(ObjectName)
					+ " FOR XML PATH('') ), 1, 2, '')  ) AS StringValue"
				)
			if str(xcd.StringValue) is not None and str(xcd.StringValue) != "":
				if str(xcd.StringValue).find(",") != -1:
					StringValue_list = [ins.strip() for ins in str(xcd.StringValue).split(",") if ins.strip() != ""]
				else:
					StringValue_list.append(str(xcd.StringValue))
			else:
				StringValue_list = [""]
			StringValue_list = list(set(StringValue_list))
			DropDownList.append(StringValue_list)
		elif filter_level_data == "checkbox":
			DropDownList.append(["True", "False"])
		else:
			DropDownList.append("")
	RelatedDrop_str = (
		"try { if( document.getElementById('"
		+ str(table_id)
		+ "') ) { var listws = document.getElementById('"
		+ str(table_id)
		+ "').getElementsByClassName('filter-control');  for (i = 0; i < listws.length; i++) { document.getElementById('"
		+ str(table_id)
		+ "').getElementsByClassName('filter-control')[i].innerHTML = data6[i];  } for (j = 0; j < listws.length; j++) { if (data7[j] == 'select') { if (data8[j]) { var dataAdapter = new $.jqx.dataAdapter(data8[j]); $('#"
		+ str(table_id)
		+ "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter, autoDropDownHeight: true }); } } } } }  catch(err) { setTimeout(function() { var listws = document.getElementById('"
		+ str(table_id)
		+ "').getElementsByClassName('filter-control');  for (i = 0; i < listws.length; i++) { document.getElementById('"
		+ str(table_id)
		+ "').getElementsByClassName('filter-control')[i].innerHTML = data6[i];  } for (j = 0; j < listws.length; j++) { if (data7[j] == 'select') { if (data8[j]) { var dataAdapter = new $.jqx.dataAdapter(data8[j]); $('#"
		+ str(table_id)
		+ "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter, autoDropDownHeight: true }); } } } }, 5000); }"
	)
	page = ""
	if QueryCount < int(PerPage):
		page = str(Page_start) + " - " + str(QueryCount)
	else:
		page = str(Page_start) + " - " + str(Page_End)
	Test = (
		'<div class="col-md-12 brdr listContStyle pad2height30" ><div class="col-md-4 pager-numberofitem clear-padding"><span class="pager-number-of-items-item noofitem" id="'
		+ str(table_id)
		+ '___NumberofItem" >'
		+ str(page)
		+ ' of</span><span class="pager-number-of-items-item fltltpad2mrg0" id="'
		+ str(table_id)
		+ '___totalItemCount" >'
		+ str(QueryCount)
		+ '</span><div class="clear-padding fltltmrgtp3" ><div  class="pull-right vertmidtxtrht"><select onchange="PageFunctestChild(this,\'Contract\',\'\',\''
		+str(table_id)
		+'\')" id="'
		+ str(table_id)
		+ '___PageCountValue"  class="form-control wid65vermiddisinbmarl5"><option value="10" selected>10</option><option value="20">20</option><option value="50">50</option><option value="100">100</option><option value="200">200</option></select> </div></div></div><div class="col-xs-8 col-md-4  clear-padding disinpad10txtcen"  data-bind="visible: totalItemCount"><div class="clear-padding col-xs-12 col-sm-6 col-md-12 bor0" ><ul class="pagination pagination"><li class="disabled"><a href="#" onclick="FirstPageLoad_paginationChild(\'Contract\',\'\',\''
		+str(table_id)
		+'\')"><i class="fa fa-caret-left font14whtbld" ></i><i class="fa fa-caret-left font14" ></i></a></li><li class="disabled"><a href="#" onclick="Previous12334Child(\'Contract\',\'\',\''
		+str(table_id)
		+'\')"><i class="fa fa-caret-left font14" ></i>PREVIOUS</a></li><li class="disabled"><a href="#" class="disabledPage" onclick="Next12334Child(\'Contract\',\'\',\''
		+str(table_id)
		+'\')">NEXT<i class="fa fa-caret-right font14" ></i></a></li><li class="disabled"><a href="#" onclick="LastPageLoad_paginationChild(\'Contract\',\'\',\''
		+str(table_id)
		+'\')" class="disabledPage"><i class="fa fa-caret-right font14"></i><i class="fa fa-caret-right font14whtbld"></i></a></li></ul></div> </div> <div class="col-md-4 pr_page_pad"> <span id="'
		+ str(table_id)
		+ '___page_count" class="currentPage page_right_content">1</span><span class="page_right_content pad_rt_2">Page </span></div></div>'
	)

	if QueryCount < int(PerPage):
		PerPage = str(QueryCount)
	else:
		PerPage = str(PerPage)   
	if Page_End > QueryCount:
		Page_End = QueryCount
	else:
		Page_End = Page_End
	
	Action_Str = ""
	Action_Str += str(Page_start)+" - "
	Action_Str += str(Page_End)
	Action_Str += " of"

	return (
		table_header,
		data_list,
		table_id,
		filter_control_function,
		NORECORDS,
		dbl_clk_function,
		cv_list,
		filter_level_list,
		DropDownList,
		RelatedDrop_str,
		Test,
		Action_Str,
	)

def GetEquipmentChild(recid, PerPage, PageInform, A_Keys, A_Values):
	# This function is used to construct the table inside the Equipment Parent Table.(As Nested Table).

	TreeParam = Product.GetGlobal("TreeParam")
	TreeParentParam = Product.GetGlobal("TreeParentLevel0")
	TreeSuperParentParam = Product.GetGlobal("TreeParentLevel1")
	TreeTopSuperParentParam = Product.GetGlobal("TreeParentLevel2")
	if str(PerPage) == "" and str(PageInform) == "":
		Page_start = 1
		Page_End = 10
		PerPage = 10
		PageInform = "1___10___10"
	else:
		Page_start = int(PageInform.split("___")[0])
		Page_End = int(PageInform.split("___")[1])
		PerPage = PerPage
	QueryCount = ""
	chld_list = []
	FablocationId = Product.GetGlobal("TreeParam")
	ContractRecordId = Quote.GetGlobal("contract_quote_record_id")
	RevisionRecordId = Quote.GetGlobal("quote_revision_record_id")
	obj_idval = "SYOBJ_00942_SYOBJ_00942"
	obj_id1 = "SYOBJ-00942"
	objh_getid = Sql.GetFirst(
		"SELECT TOP 1  RECORD_ID  FROM SYOBJH (NOLOCK) WHERE SAPCPQ_ATTRIBUTE_NAME='" + str(obj_id1) + "'"
	)
	if objh_getid:
		obj_id1 = objh_getid.RECORD_ID
	objs_obj1 = Sql.GetFirst(
		"select CAN_ADD,CAN_EDIT,COLUMNS,CAN_DELETE from SYOBJR (NOLOCK) where OBJ_REC_ID = '" + str(obj_id1) + "' "
	)
	can_edit1 = str(objs_obj1.CAN_EDIT)
	can_add1 = str(objs_obj1.CAN_ADD)
	can_delete1 = str(objs_obj1.CAN_DELETE)
	table_id = "table_equipment_child_"+str(recid)
	table_header = (
		'<table id="'
		+ str(table_id)
		+ '" data-pagination="false" data-sortable="true" data-search-on-enter-key="true" data-filter-control="true" data-pagination-loop = "false" data-locale = "en-US" ><thead>'
	)
	Columns = [
		#"QUOTE_FAB_LOC_COV_OBJ_ASSEMBLY_RECORD_ID",
		"EQUIPMENTCATEGORY_ID",
		"SERIAL_NUMBER",
		"ASSEMBLY_ID",
		"ASSEMBLY_DESCRIPTION",
		"ASSEMBLYTYPE_ID",
		"GOT_CODE",
		"MNT_PLANT_ID",
		"FABLOCATION_ID",
		"WARRANTY_START_DATE",
		"WARRANTY_END_DATE"
	]
	Objd_Obj = Sql.GetList(
		"select FIELD_LABEL,API_NAME,LOOKUP_OBJECT,LOOKUP_API_NAME,DATA_TYPE from SYOBJD (NOLOCK) where OBJECT_NAME = 'SAQFEA'"
	)
	attr_list = []
	attrs_datatype_dict = {}
	lookup_disply_list = []
	lookup_str = ""
	if Objd_Obj is not None:
		attr_list = {}
		for attr in Objd_Obj:
			attr_list[str(attr.API_NAME)] = str(attr.FIELD_LABEL)
			attrs_datatype_dict[str(attr.API_NAME)] = str(attr.DATA_TYPE)
			if attr.LOOKUP_API_NAME != "" and attr.LOOKUP_API_NAME is not None:
				lookup_disply_list.append(str(attr.API_NAME))
		checkbox_list = [inn.API_NAME for inn in Objd_Obj if inn.DATA_TYPE == "CHECKBOX"]
		lookup_list = {ins.LOOKUP_API_NAME: ins.API_NAME for ins in Objd_Obj}
	lookup_str = ",".join(list(lookup_disply_list))
	GetSaleType = Sql.GetFirst("SELECT SALE_TYPE FROM SAQTMT WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{}'".format(ContractRecordId))
	GetSaleType = Sql.GetList("SELECT CpqTableEntryId FROM SAQTIP WHERE (PARTY_ROLE = 'RECEIVING ACCOUNT' OR PARTY_ROLE = 'SENDING ACCOUNT') AND QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' ".format(Quote.GetGlobal("contract_quote_record_id"),Quote.GetGlobal("quote_revision_record_id")))
		#Trace.Write("count--"+str(list(GetToolReloc)))
	GetSaleType = list(GetSaleType)
	if len(GetSaleType) == 2:
		sale_type = "TOOL RELOCATION"
	else:
		sale_type = None
	if sale_type != "TOOL RELOCATION":
		if TreeParam == 'Fab Locations':
			Parent_Equipmentid = Sql.GetFirst(
				"select EQUIPMENT_ID from SAQFEQ (NOLOCK) where QUOTE_RECORD_ID = '{ContractRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND EQUIPMENT_ID = '{EquipmentId}' AND ISNULL(SERIAL_NUMBER,'') <> ''".format(
					ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),
					RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"),
					EquipmentId=recid,
				)
			)
		elif TreeParentParam == 'Fab Locations':
			Parent_Equipmentid = Sql.GetFirst(
				"select EQUIPMENT_ID from SAQFEQ (NOLOCK) where QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' and  FABLOCATION_ID = '{FablocationId}' AND EQUIPMENT_ID = '{EquipmentId}' AND ISNULL(SERIAL_NUMBER,'') <> ''".format(
					ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),
					RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"),
					FablocationId=Product.GetGlobal("TreeParam"),
					EquipmentId=recid,
				)
			)
		elif TreeSuperParentParam == 'Fab Locations':
			Parent_Equipmentid = Sql.GetFirst(
				"select EQUIPMENT_ID from SAQFEQ (NOLOCK) where QUOTE_RECORD_ID = '{ContractRecordId}'  and QTEREV_RECORD_ID = '{RevisionRecordId}' and FABLOCATION_ID = '{FablocationId}' AND EQUIPMENT_ID = '{EquipmentId}'AND GREENBOOK = '{GreenBook}' AND ISNULL(SERIAL_NUMBER,'') <> ''".format(
					ContractRecordId = Quote.GetGlobal("contract_quote_record_id"),
					RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"),
					FablocationId = Product.GetGlobal("TreeParentLevel0"),
					EquipmentId = recid,
					GreenBook = Product.GetGlobal("TreeParam"),
				)
			)
	elif sale_type == "TOOL RELOCATION":
		if TreeParam == 'Fab Locations':
			Parent_Equipmentid = Sql.GetFirst(
				"select EQUIPMENT_ID from SAQFEQ (NOLOCK) where QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' AND EQUIPMENT_ID = '{EquipmentId}' AND ISNULL(SERIAL_NUMBER,'') <> ''".format(
					ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),
					RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"),
					EquipmentId=recid,
				)
			)
		elif TreeParentParam == 'Fab Locations':
			Parent_Equipmentid = Sql.GetFirst(
				"select EQUIPMENT_ID from SAQFEQ (NOLOCK) where QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' AND EQUIPMENT_ID = '{EquipmentId}' AND ISNULL(SERIAL_NUMBER,'') <> ''".format(
					ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),
					RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"),
					FablocationId=Product.GetGlobal("TreeParam"),
					EquipmentId=recid,
				)
			)
		elif TreeTopSuperParentParam == 'Fab Locations':
			Parent_Equipmentid = Sql.GetFirst(
				"select EQUIPMENT_ID from SAQFEQ (NOLOCK) where QUOTE_RECORD_ID = '{ContractRecordId}'  and QTEREV_RECORD_ID = '{RevisionRecordId}' and FABLOCATION_ID = '{FablocationId}' AND EQUIPMENT_ID = '{EquipmentId}'AND GREENBOOK = '{GreenBook}' AND ISNULL(SERIAL_NUMBER,'') <> ''".format(
					ContractRecordId = Quote.GetGlobal("contract_quote_record_id"),
					RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"),
					FablocationId = Product.GetGlobal("TreeParentLevel0"),
					EquipmentId = recid,
					GreenBook = Product.GetGlobal("TreeParam"),
				)
			)
		elif TreeSuperParentParam == 'Fab Locations':
			Parent_Equipmentid = Sql.GetFirst(
				"select EQUIPMENT_ID from SAQFEQ (NOLOCK) where QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' and FABLOCATION_ID = '{FablocationId}' AND EQUIPMENT_ID = '{EquipmentId}' AND ISNULL(SERIAL_NUMBER,'') <> ''".format(
					ContractRecordId = Quote.GetGlobal("contract_quote_record_id"),
					RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"),
					FablocationId = Product.GetGlobal("TreeParam"),
					EquipmentId = recid,
					#GreenBook = Product.GetGlobal("TreeParam"),
				)
			)

	if Parent_Equipmentid:
		EquipmentID = Parent_Equipmentid.EQUIPMENT_ID
			# child_obj_recid = Sql.GetList("select  top 5 EQUIPMENT_ID from SAQFEA (NOLOCK) where EQUIPMENT_ID = '{EquipmentID}' and QUOTE_RECORD_ID = '{ContractRecordId}' and FABLOCATION_ID = '{FablocationId}'".format(EquipmentID = Parent_Equipmentid.EQUIPMENT_ID,ContractRecordId = Quote.GetGlobal("contract_quote_record_id"),FablocationId = Product.GetGlobal("TreeParam")))
		if sale_type != "TOOL RELOCATION":
			if TreeParam == 'Fab Locations':
				child_obj_recid = Sql.GetList(
					"select top "+str(PerPage)+" * from (select ROW_NUMBER() OVER( ORDER BY QUOTE_FAB_LOC_COV_OBJ_ASSEMBLY_RECORD_ID) AS ROW, QUOTE_FAB_LOC_COV_OBJ_ASSEMBLY_RECORD_ID,EQUIPMENT_ID,SERIAL_NUMBER,ASSEMBLY_ID,ASSEMBLY_DESCRIPTION,GOT_CODE,MNT_PLANT_ID,FABLOCATION_ID,WARRANTY_START_DATE,EQUIPMENTCATEGORY_ID,WARRANTY_END_DATE,SALESORG_ID,EQUIPMENTTYPE_ID as ASSEMBLYTYPE_ID from SAQFEA (NOLOCK) where EQUIPMENT_ID = '"
					+ str(recid)
					+ "' AND QTEREV_RECORD_ID = '{}' ".format(str(Quote.GetGlobal("quote_revision_record_id")))
					+ " AND QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' ) m where m.ROW BETWEEN ".format(
							ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),
							RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"),
						)
					+ str(Page_start)
					+ " and "
					+ str(Page_End)
				)
				QueryCountObj = Sql.GetFirst(
				"select count(CpqTableEntryId) as cnt from SAQFEA (NOLOCK) where QUOTE_RECORD_ID = '"
				+ str(ContractRecordId)
				+ "' and QTEREV_RECORD_ID = '"
				+ str(RevisionRecordId)
				+ "' and EQUIPMENT_ID = '"
				+ str(EquipmentID)
				+ "' ") 
			elif TreeParentParam == 'Fab Locations':
				child_obj_recid = Sql.GetList(
					"select top "+str(PerPage)+" * from (select ROW_NUMBER() OVER( ORDER BY QUOTE_FAB_LOC_COV_OBJ_ASSEMBLY_RECORD_ID) AS ROW, QUOTE_FAB_LOC_COV_OBJ_ASSEMBLY_RECORD_ID,EQUIPMENT_ID,SERIAL_NUMBER,ASSEMBLY_ID,ASSEMBLY_DESCRIPTION,GOT_CODE,MNT_PLANT_ID,FABLOCATION_ID,WARRANTY_START_DATE,EQUIPMENTCATEGORY_ID,WARRANTY_END_DATE,SALESORG_ID,EQUIPMENTTYPE_ID as ASSEMBLYTYPE_ID from SAQFEA (NOLOCK) where EQUIPMENT_ID = '"
					+ str(recid)
					+ "' AND QTEREV_RECORD_ID = '{}' ".format(str(Quote.GetGlobal("quote_revision_record_id")))
					+ " and QUOTE_RECORD_ID = '{ContractRecordId}' and FABLOCATION_ID = '{FablocationId}') m where m.ROW BETWEEN ".format(
						ContractRecordId=Quote.GetGlobal("contract_quote_record_id"), FablocationId=Product.GetGlobal("TreeParam")
					)
					+ str(Page_start)
					+ " and "
					+ str(Page_End)
				)
				QueryCountObj = Sql.GetFirst(
				"select count(CpqTableEntryId) as cnt from SAQFEA (NOLOCK) where QUOTE_RECORD_ID = '"
				+ str(ContractRecordId)
				+ "' and FABLOCATION_ID = '"
				+ str(TreeParam)
				+ "' and EQUIPMENT_ID = '"
				+ str(EquipmentID)
				+ "'"
				+ " AND QTEREV_RECORD_ID = '{}' ".format(str(Quote.GetGlobal("quote_revision_record_id")))
			)
			elif TreeSuperParentParam == 'Fab Locations':
				child_obj_recid = Sql.GetList(
					"select top "+str(PerPage)+" * from (select ROW_NUMBER() OVER( ORDER BY QUOTE_FAB_LOC_COV_OBJ_ASSEMBLY_RECORD_ID) AS ROW, QUOTE_FAB_LOC_COV_OBJ_ASSEMBLY_RECORD_ID,EQUIPMENT_ID,SERIAL_NUMBER,ASSEMBLY_ID,ASSEMBLY_DESCRIPTION,GOT_CODE,MNT_PLANT_ID,FABLOCATION_ID,WARRANTY_START_DATE,EQUIPMENTCATEGORY_ID,WARRANTY_END_DATE,SALESORG_ID,EQUIPMENTTYPE_ID as ASSEMBLYTYPE_ID from SAQFEA (NOLOCK) where EQUIPMENT_ID = '"
					+ str(recid)
					+ "' AND QTEREV_RECORD_ID = '{}' ".format(str(Quote.GetGlobal("quote_revision_record_id")))
					+ " and QUOTE_RECORD_ID = '{ContractRecordId}' and FABLOCATION_ID = '{FablocationId}')m where m.ROW BETWEEN ".format(
					ContractRecordId=Quote.GetGlobal("contract_quote_record_id"), FablocationId=TreeParentParam
					)
					+ str(Page_start)
					+ " and "
					+ str(Page_End)
				)
				QueryCountObj = Sql.GetFirst(
				"select count(CpqTableEntryId) as cnt from SAQFEA (NOLOCK) where QUOTE_RECORD_ID = '"
				+ str(ContractRecordId)
				+ "' and FABLOCATION_ID = '"
				+ str(TreeParentParam)
				+ "' and EQUIPMENT_ID = '"
				+ str(EquipmentID)
				+ "'"
				+ " AND QTEREV_RECORD_ID = '{}' ".format(str(Quote.GetGlobal("quote_revision_record_id")))
			)
		elif sale_type == "TOOL RELOCATION":
			if TreeParam == 'Fab Locations':
				child_obj_recid = Sql.GetList(
					"select top "+str(PerPage)+" * from (select ROW_NUMBER() OVER( ORDER BY QUOTE_FAB_LOC_COV_OBJ_ASSEMBLY_RECORD_ID) AS ROW, QUOTE_FAB_LOC_COV_OBJ_ASSEMBLY_RECORD_ID,EQUIPMENT_ID,SERIAL_NUMBER,ASSEMBLY_ID,ASSEMBLY_DESCRIPTION,GOT_CODE,MNT_PLANT_ID,FABLOCATION_ID,WARRANTY_START_DATE,EQUIPMENTCATEGORY_ID,WARRANTY_END_DATE,SALESORG_ID,EQUIPMENTTYPE_ID as ASSEMBLYTYPE_ID from SAQFEA (NOLOCK) where EQUIPMENT_ID = '"
					+ str(recid)
					+ "' AND QTEREV_RECORD_ID = '{}' ".format(str(Quote.GetGlobal("quote_revision_record_id")))
					+ " and QUOTE_RECORD_ID = '{ContractRecordId}') m where m.ROW BETWEEN ".format(
							ContractRecordId=Quote.GetGlobal("contract_quote_record_id")
						)
					+ str(Page_start)
					+ " and "
					+ str(Page_End)
					)
				QueryCountObj = Sql.GetFirst(
					"select count(CpqTableEntryId) as cnt from SAQFEA (NOLOCK) where QUOTE_RECORD_ID = '"
					+ str(ContractRecordId)
					+ "'and EQUIPMENT_ID = '"
					+ str(EquipmentID)
					+ "'"
					+ " AND QTEREV_RECORD_ID = '{}' ".format(str(Quote.GetGlobal("quote_revision_record_id")))
					) 
			elif TreeParentParam == 'Fab Locations':
				child_obj_recid = Sql.GetList(
					"select top "+str(PerPage)+" * from (select ROW_NUMBER() OVER( ORDER BY QUOTE_FAB_LOC_COV_OBJ_ASSEMBLY_RECORD_ID) AS ROW, QUOTE_FAB_LOC_COV_OBJ_ASSEMBLY_RECORD_ID,EQUIPMENT_ID,SERIAL_NUMBER,ASSEMBLY_ID,ASSEMBLY_DESCRIPTION,GOT_CODE,MNT_PLANT_ID,FABLOCATION_ID,WARRANTY_START_DATE,EQUIPMENTCATEGORY_ID,WARRANTY_END_DATE,SALESORG_ID,EQUIPMENTTYPE_ID as ASSEMBLYTYPE_ID from SAQFEA (NOLOCK) where EQUIPMENT_ID = '"
					+ str(recid)
					+ "' AND QTEREV_RECORD_ID = '{}' ".format(str(Quote.GetGlobal("quote_revision_record_id")))
					+ " and QUOTE_RECORD_ID = '{ContractRecordId}' ) m where m.ROW BETWEEN ".format(
						ContractRecordId=Quote.GetGlobal("contract_quote_record_id"), FablocationId=Product.GetGlobal("TreeParam")
					)
					+ str(Page_start)
					+ " and "
					+ str(Page_End)
				)
				QueryCountObj = Sql.GetFirst(
				"select count(CpqTableEntryId) as cnt from SAQFEA (NOLOCK) where QUOTE_RECORD_ID = '"
				+ str(ContractRecordId)
				+ "' and EQUIPMENT_ID = '"
				+ str(EquipmentID)
				+ "'"
				+ " AND QTEREV_RECORD_ID = '{}' ".format(str(Quote.GetGlobal("quote_revision_record_id")))
				)
			elif TreeSuperParentParam == 'Fab Locations':
				child_obj_recid = Sql.GetList(
					"select top "+str(PerPage)+" * from (select ROW_NUMBER() OVER( ORDER BY QUOTE_FAB_LOC_COV_OBJ_ASSEMBLY_RECORD_ID) AS ROW, QUOTE_FAB_LOC_COV_OBJ_ASSEMBLY_RECORD_ID,EQUIPMENT_ID,SERIAL_NUMBER,ASSEMBLY_ID,ASSEMBLY_DESCRIPTION,GOT_CODE,MNT_PLANT_ID,FABLOCATION_ID,WARRANTY_START_DATE,EQUIPMENTCATEGORY_ID,WARRANTY_END_DATE,SALESORG_ID,EQUIPMENTTYPE_ID as ASSEMBLYTYPE_ID from SAQFEA (NOLOCK) where EQUIPMENT_ID = '"
					+ str(recid)
					+ "' AND QTEREV_RECORD_ID = '{}' ".format(str(Quote.GetGlobal("quote_revision_record_id")))
					+ " and QUOTE_RECORD_ID = '{ContractRecordId}' and FABLOCATION_ID = '{FablocationId}')m where m.ROW BETWEEN ".format(
					ContractRecordId=Quote.GetGlobal("contract_quote_record_id"), FablocationId=TreeParam
					)
					+ str(Page_start)
					+ " and "
					+ str(Page_End)
				)
				QueryCountObj = Sql.GetFirst(
				"select count(CpqTableEntryId) as cnt from SAQFEA (NOLOCK) where QUOTE_RECORD_ID = '"
				+ str(ContractRecordId)
				+ "' and FABLOCATION_ID = '"
				+ str(TreeParam)
				+ "' and EQUIPMENT_ID = '"
				+ str(EquipmentID)
				+ "'"
				+ " AND QTEREV_RECORD_ID = '{}' ".format(str(Quote.GetGlobal("quote_revision_record_id")))
			) 
			elif TreeTopSuperParentParam == 'Fab Locations':
				child_obj_recid = Sql.GetList(
					"select top "+str(PerPage)+" * from (select ROW_NUMBER() OVER( ORDER BY QUOTE_FAB_LOC_COV_OBJ_ASSEMBLY_RECORD_ID) AS ROW, QUOTE_FAB_LOC_COV_OBJ_ASSEMBLY_RECORD_ID,EQUIPMENT_ID,SERIAL_NUMBER,ASSEMBLY_ID,ASSEMBLY_DESCRIPTION,GOT_CODE,MNT_PLANT_ID,FABLOCATION_ID,WARRANTY_START_DATE,EQUIPMENTCATEGORY_ID,WARRANTY_END_DATE,SALESORG_ID,EQUIPMENTTYPE_ID as ASSEMBLYTYPE_ID from SAQFEA (NOLOCK) where EQUIPMENT_ID = '"
					+ str(recid)
					+ "' AND QTEREV_RECORD_ID = '{}' ".format(str(Quote.GetGlobal("quote_revision_record_id")))
					+ " and QUOTE_RECORD_ID = '{ContractRecordId}' and FABLOCATION_ID = '{FablocationId}')m where m.ROW BETWEEN ".format(
					ContractRecordId=Quote.GetGlobal("contract_quote_record_id"), FablocationId=TreeParentParam
					)
					+ str(Page_start)
					+ " and "
					+ str(Page_End)
				)
				QueryCountObj = Sql.GetFirst(
				"select count(CpqTableEntryId) as cnt from SAQFEA (NOLOCK) where QUOTE_RECORD_ID = '"
				+ str(ContractRecordId)
				+ "' and FABLOCATION_ID = '"
				+ str(TreeParentParam)
				+ "' and EQUIPMENT_ID = '"
				+ str(EquipmentID)
				+ "'"
				+ " AND QTEREV_RECORD_ID = '{}' ".format(str(Quote.GetGlobal("quote_revision_record_id")))
			) 
		chld_list = []
		QueryCount = ""
		if QueryCountObj is not None:
			QueryCount = QueryCountObj.cnt
		# Data construction for table.
		for child in child_obj_recid:
			data_id = str(child.QUOTE_FAB_LOC_COV_OBJ_ASSEMBLY_RECORD_ID) + "|SAQFEA"
			chld_dict = {}
			Action_str1 = (
				'<div class="btn-group dropdown"><div class="dropdown" id="ctr_drop"><i data-toggle="dropdown" id="dropdownMenuButton" class="fa fa-sort-desc dropdown-toggle" aria-expanded="false"></i><ul class="dropdown-menu left" aria-labelledby="dropdownMenuButton"><li><a  data-toggle="modal" data-target="#cont_viewModalSection" id="'
				+ str(data_id)
				+ '" class="dropdown-item cur_sty" href="#"  onclick="cont_relatedlist_openview(this) ">VIEW</a></li>'
			)
			if can_edit1.upper() == "TRUE":
				Action_str1 += (
					'<li style="display:none" ><a data-toggle="modal" data-target="#cont_viewModalSection" id="'
					+ str(data_id)
					+ '"  class="dropdown-item cur_sty" href="#"  onclick="cont_relatedlist_openedit(this)">EDIT</a></li>'
				)
			if can_delete1.upper() == "TRUE":
				Action_str1 += '<li><a class="dropdown-item" data-target="#cont_viewModal_Material_Delete" data-toggle="modal" onclick="Material_delete_obj(this)" href="#">DELETE</a></li>'
			if can_add1.upper() == "TRUE":
				Action_str1 += '<li><a class="dropdown-item" data-target="#" data-toggle="modal" onclick="Material_clone_obj(this)" href="#">CLONE</a></li>'
			Action_str1 += "</ul></div></div>"

			# data formation in Dictonary format.

			chld_dict["ACTIONS"] = str(Action_str1)
			chld_dict["QUOTE_FAB_LOC_COV_OBJ_ASSEMBLY_RECORD_ID"] = CPQID.KeyCPQId.GetCPQId(
				"SAQFEA", str(child.QUOTE_FAB_LOC_COV_OBJ_ASSEMBLY_RECORD_ID)
			)
			chld_dict["EQUIPMENTCATEGORY_ID"] = ('<abbr id ="" title="' + str(child.EQUIPMENTCATEGORY_ID) + '">' + str(child.EQUIPMENTCATEGORY_ID) + "</abbr>") 
			chld_dict["SERIAL_NUMBER"] = ('<abbr id ="" title="' + str(child.SERIAL_NUMBER) + '">' + str(child.SERIAL_NUMBER) + "</abbr>") 
			chld_dict["ASSEMBLY_ID"] = ('<abbr id ="" title="' + str(child.ASSEMBLY_ID) + '">' + str(child.ASSEMBLY_ID) + "</abbr>")
			chld_dict["ASSEMBLYTYPE_ID"] = ('<abbr id ="" title="' + str(child.ASSEMBLYTYPE_ID) + '">' + str(child.ASSEMBLYTYPE_ID) + "</abbr>")
			chld_dict["ASSEMBLY_DESCRIPTION"] = ('<abbr id ="" title="' + str(child.ASSEMBLY_DESCRIPTION) + '">' + str(child.ASSEMBLY_DESCRIPTION) + "</abbr>")
			chld_dict["GOT_CODE"] = ('<abbr id ="" title="' + str(child.GOT_CODE) + '">' + str(child.GOT_CODE) + "</abbr>")
			chld_dict["MNT_PLANT_ID"] = ('<abbr id ="" title="' + str(child.MNT_PLANT_ID) + '">' + str(child.MNT_PLANT_ID) + "</abbr>")
			chld_dict["FABLOCATION_ID"] = ('<abbr id ="" title="' + str(child.FABLOCATION_ID) + '">' + str(child.FABLOCATION_ID) + "</abbr>")
			chld_dict["WARRANTY_START_DATE"] = ('<abbr id ="" title="' + str(child.WARRANTY_START_DATE) + '">' + str(child.WARRANTY_START_DATE) + "</abbr>")
			chld_dict["WARRANTY_END_DATE"] = ('<abbr id ="" title="' + str(child.WARRANTY_END_DATE) + '">' + str(child.WARRANTY_END_DATE) + "</abbr>")
			chld_list.append(chld_dict)

	# Table formation.
	hyper_link = ["QUOTE_FAB_LOC_COV_OBJ_ASSEMBLY_RECORD_ID"]
	table_header += "<tr>"
	table_header += (
		'<th data-field="ACTIONS"><div class="action_col">ACTIONS</div><button class="searched_button" id="Act_'
		+ str(table_id)
		+ '">Search</button></th>'
	)
	table_header += '<th data-field="SELECT" class="wid45" data-checkbox="true"></th>'
	#Trace.Write("table header-------------"+str(table_header))
	for key, invs in enumerate(list(Columns)):
		invs = str(invs).strip()
		qstring = attr_list.get(str(invs)) or ""
		if qstring == "":
			qstring = invs.replace("_", " ")
		if checkbox_list is not None and invs in checkbox_list:
			table_header += (
				'<th data-field="'
				+ str(invs)
				+ '" data-filter-control="input" data-align="center" data-formatter="CheckboxFieldRelatedList" data-sortable="true"><abbr title="'
				+ str(qstring)
				+ '">'
				+ str(qstring)
				+ "</abbr></th>"
			)
		elif hyper_link is not None and invs in hyper_link:
			table_header += (
				'<th data-field="'
				+ str(invs)
				+ '" data-filter-control="input" data-formatter="primaryListHyperLink" data-sortable="true"><abbr title="'
				+ str(qstring)
				+ '">'
				+ str(qstring)
				+ "</abbr></th>"
			)
		else:
			table_header += (
				'<th data-field="'
				+ str(invs)
				+ '" data-filter-control="input" data-sortable="true"><abbr title="'
				+ str(qstring)
				+ '">'
				+ str(qstring)
				+ "</abbr></th>"
			)
	table_header += "</tr>"
	table_header += '</thead><tbody onclick="Table_Onclick_Scroll(this)"></tbody></table>'
	table_ids = "#" + str(table_id)
	filter_control_function = ""
	tbl_id = table_id
	values_list = ""
	for key, invs in enumerate(list(Columns)):
		table_ids = "#" + str(table_id)
		filter_clas = "#" + str(table_id) + " .bootstrap-table-filter-control-" + str(invs)
		values_list += "var " + str(invs) + ' = $("' + str(filter_clas) + '").val(); '
		values_list += "ATTRIBUTE_VALUEList.push(" + str(invs) + "); "
		Trace.Write('invs----'+str(values_list))
	filter_class = "#Act_" + str(table_id)
	filter_control_function += (
		'$("'
		+ filter_class
		+ '").click( function(){ var table_id = $(this).closest("table").attr("id"); ATTRIBUTE_VALUEList = []; '
		+ str(values_list)
		+ ' var attribute_value = $(this).val(); cpq.server.executeScript("CQNESTGRID", {"TABNAME":"Equipments child", "ACTION":"PRODUCT_ONLOAD_FILTER", "ATTRIBUTE_NAME": '
		+ str(list(Columns))
		+ ', "ATTRIBUTE_VALUE": ATTRIBUTE_VALUEList, "REC_ID":"'
		+ str(recid)
		+ '" }, function(dataset) { data2 = dataset[1];  data1 = dataset[0]; data3 = dataset[2]; console.log("len ---->"+data1.length);  try { if(data1.length > 0) { $("#'+ str(tbl_id) + '").bootstrapTable("load", data1 );$("#noRecDisp").remove(); if (document.getElementById("'+str(tbl_id) + '___totalItemCount")){document.getElementById("'+str(tbl_id)+ '___totalItemCount").innerHTML = data2;}  if (document.getElementById("'+str(tbl_id) + '___NumberofItem")) {document.getElementById("'+str(tbl_id)+ '___NumberofItem").innerHTML = data3;}} else{ $("#' + str(tbl_id) + '").bootstrapTable("load", data1  );$("#' + str(tbl_id) + '").after("<div id=\'noRecDisp\' class=\'noRecord\'>No Records to Display</div>"); $(".noRecord:not(:first)").remove(); if (document.getElementById("'+str(tbl_id) + '___totalItemCount")){document.getElementById("'+str(tbl_id)+ '___totalItemCount").innerHTML = data2;}  if (document.getElementById("'+str(tbl_id) + '___NumberofItem")) {document.getElementById("'+str(tbl_id)+ '___NumberofItem").innerHTML = data3;} }} catch(err){} }); filter_search_click();$(".JColResizer").mousedown(function(){ $("thead.fullHeadFirst").css("cssText","z-index: 2;border-top: 1px solid rgb(220, 220, 220);top: 154px;border-right: 0px !important;");$("thead.fullHeadSecond").css("display","none"); });$(".JColResizer").mouseup(function(){ var th_width_resize = [];$("#table_equipment_child thead.fullHeadFirst tr th").each(function(index){var wid = $(this).css("width"); if(index ==0 || index ==1){th_width_resize.push("60px");}else{th_width_resize.push(wid);}}); $("thead.fullHeadFirst").css("cssText","position: fixed;z-index: 2;border-top: 1px solid rgb(220, 220, 220); top: 154px;border-right: 0px !important;");$("thead.fullHeadSecond").css("display","table-header-group");$("#table_equipment_child thead.fullHeadFirst tr th").each(function(index){var num = th_width_resize[index].split("px");var numsp = parseInt(num[0]);numsp = numsp - 1;var make_str =numsp+"px"; var c = "width:"+make_str+";white-space: nowrap;overflow: hidden;text-overflow: ellipsis;";var d = "width:"+make_str+";"; $(this).css("cssText",c);$(this).children("div:first-child").css("cssText",c);$(this).children("div.fht-cell").css("cssText",d);});$("#table_equipment_child thead.fullHeadSecond tr th").each(function(index){var num = th_width_resize[index].split("px");var numsp = parseInt(num[0]);numsp = numsp - 1;var make_str =numsp+"px"; var c = "width:"+make_str+";white-space: nowrap;overflow: hidden;text-overflow: ellipsis;";var d = "width:"+make_str+";"; $(this).css("cssText",c);$(this).children("div:first-child").css("cssText",c);$(this).children("div.fht-cell").css("cssText",d);}); });});'
	)
	
	#Trace.Write("969696 filter_control_function --->"+str(filter_control_function))
	dbl_clk_function = (
		'$("'
		+ str(table_ids)
		+ '").on("all.bs.table", function (e, name, args) { $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); }); $("'
		+ str(table_ids)
		+ '\ th.bs-checkbox div.th-inner").before("<div style=\'padding:0; border-bottom: 1px solid #dcdcdc;\'>SELECT</div>"); $(".bs-checkbox input").addClass("custom"); $("'
		+ str(table_ids)
		+ "\").on('sort.bs.table', function (e, name, order) { console.log('sort.bs.table ============>', e); e.stopPropagation(); currenttab = $(\"ul#carttabs_head .active\").text().trim(); localStorage.setItem('"
		+ str(table_id)
		+ "_SortColumn', name); localStorage.setItem('"
		+ str(table_id)
		+ "_SortColumnOrder', order); NestedContainerSorting(name, order, '"
		+ str(table_id)
		+ "'); }); "
		)
	#Trace.Write("4444 dbl_clk_function --->"+str(dbl_clk_function))
	NORECORDS = ""
	if len(chld_list) == 0:
		NORECORDS = "NORECORDS"

	ObjectName = "SAQFEA"
	DropDownList = []
	filter_level_list = []
	filter_clas_name = ""
	cv_list = []
	TableclassName = "form-control" + table_id
	for key, col_name in enumerate(list(Columns)):
		StringValue_list = []
		objss_obj = Sql.GetFirst(
			"SELECT API_NAME, DATA_TYPE, FORMULA_LOGIC FROM SYOBJD (NOLOCK) WHERE OBJECT_NAME='"
			+ str(ObjectName)
			+ "' and API_NAME = '"
			+ str(col_name)
			+ "'"
		)
		try:
			FORMULA_LOGIC = objss_obj.FORMULA_LOGIC.strip()
			FORMULA_col = FORMULA_LOGIC.split(" ")[1].strip()
			FORMULA_table = FORMULA_LOGIC.split(" ")[3].strip()
			ins_obj = Sql.GetFirst(
				"SELECT API_NAME, DATA_TYPE,PICKLIST FROM SYOBJD (NOLOCK) WHERE OBJECT_NAME='"
				+ str(FORMULA_table)
				+ "' and API_NAME = '"
				+ str(FORMULA_col)
				+ "'"
			)
			if str(objss_obj.PICKLIST).upper() == "TRUE":
				filter_level_data = "select"
				filter_clas_name = (
					'<div id = "'
					+ str(table_id)
					+ "_RelatedMutipleCheckBoxDrop_"
					+ str(key)
					+ '" class="form-control bootstrap-table-filter-control-'
					+ str(col_name)
					+ " RelatedMutipleCheckBoxDrop_"
					+ str(key)
					+ ' "></div>'
				)
				filter_level_list.append(filter_level_data)
			else:
				filter_level_data = "input"
				filter_clas_name = (
					'<input type="text" class="width100_vis form-control bootstrap-table-filter-control-'
					+ str(col_name)
					+ '">'
				)
				filter_level_list.append(filter_level_data)
		except:
			"""if str(objss_obj.PICKLIST).upper() == "TRUE":
				filter_level_data = "select"
				filter_clas_name = (
					'<div id = "'
					+ str(table_id)
					+ "_RelatedMutipleCheckBoxDrop_"
					+ str(key)
					+ '" class="form-control bootstrap-table-filter-control-'
					+ str(col_name)
					+ " RelatedMutipleCheckBoxDrop_"
					+ str(key)
					+ ' "></div>'
				)
				filter_level_list.append(filter_level_data)"""

			filter_level_data = "input"
			filter_clas_name = (
				'<input type="text" class="width100_vis form-control bootstrap-table-filter-control-' + str(col_name) + '">'
			)
			filter_level_list.append(filter_level_data)
		cv_list.append(filter_clas_name)
		if filter_level_data == "select":
			try:
				xcd = Sql.GetFirst(
					"SELECT (STUFF((SELECT DISTINCT ', ' + CAST("
					+ str(col_name)
					+ " AS CHAR(100)) FROM "
					+ str(ObjectName)
					+ " (NOLOCK) where QUOTE_FAB_LOC_COV_OBJ_ASSEMBLY_RECORD_ID = '"
					+ str(recid)
					+ "' FOR XML PATH('') ), 1, 2, '')  ) AS StringValue"
				)
			except:
				xcd = Sql.GetFirst(
					"SELECT (STUFF((SELECT DISTINCT ', ' + CAST("
					+ str(col_name)
					+ " AS CHAR(100)) FROM "
					+ str(ObjectName)
					+ " (NOLOCK) FOR XML PATH('') ), 1, 2, '')  ) AS StringValue"
				)
			if str(xcd.StringValue) is not None and str(xcd.StringValue) != "":
				if str(xcd.StringValue).find(",") != -1:
					StringValue_list = [ins.strip() for ins in str(xcd.StringValue).split(",") if ins.strip() != ""]
				else:
					StringValue_list.append(str(xcd.StringValue))
			else:
				StringValue_list = [""]
			StringValue_list = list(set(StringValue_list))
			DropDownList.append(StringValue_list)
		elif filter_level_data == "checkbox":
			DropDownList.append(["True", "False"])
		else:
			DropDownList.append("")
	RelatedDrop_str = (
		"try { if( document.getElementById('"
		+ str(table_id)
		+ "') ) { var listws = document.getElementById('"
		+ str(table_id)
		+ "').getElementsByClassName('filter-control');  for (i = 0; i < listws.length; i++) { document.getElementById('"
		+ str(table_id)
		+ "').getElementsByClassName('filter-control')[i].innerHTML = datachld6[i];  } for (j = 0; j < listws.length; j++) { if (datachld7[j] == 'select') { if (data8[j]) { var dataAdapter = new $.jqx.dataAdapter(datachld8[j]); $('#"
		+ str(table_id)
		+ "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter, autoDropDownHeight: true }); } } } } }  catch(err) { setTimeout(function() { var listws = document.getElementById('"
		+ str(table_id)
		+ "').getElementsByClassName('filter-control');  for (i = 0; i < listws.length; i++) { document.getElementById('"
		+ str(table_id)
		+ "').getElementsByClassName('filter-control')[i].innerHTML = datachld6[i];  } for (j = 0; j < listws.length; j++) { if (datachld7[j] == 'select') { if (data8[j]) { var dataAdapter = new $.jqx.dataAdapter(datachld8[j]); $('#"
		+ str(table_id)
		+ "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter, autoDropDownHeight: true }); } } } }, 5000); } try { setTimeout(function(){ $('#"
		+ str(table_id)
		+ "').colResizable({ resizeMode:'overflow'}); }, 3000); } catch(err){}"
	)
	page = ""
	if QueryCount < int(PerPage):
		page = str(Page_start) + " - " + str(QueryCount)
	else:
		page = str(Page_start) + " - " + str(Page_End)
	Test = (
		'<div class="col-md-12 brdr listContStyle pad2height30" ><div class="col-md-4 pager-numberofitem clear-padding"><span class="pager-number-of-items-item noofitem"  id="'
		+ str(table_id)
		+ '___NumberofItem" >'
		+ str(page)
		+ ' of </span><span class="pager-number-of-items-item fltltpad2mrg0" id="'
		+ str(table_id)
		+ '___totalItemCount"  >'
		+ str(QueryCount)
		+ '</span><div class="clear-padding fltltmrgtp3" ><div  class="pull-right vertmidtxtrht"><select onchange="PageFunctestChild(this,\'Quote\',\'\',\''
		+str(table_id)
		+'\')" id="'
		+ str(table_id)
		+ '___PageCountValue"  class="form-control wid65vermiddisinbmarl5"><option value="10" selected>10</option><option value="20">20</option><option value="50">50</option><option value="100">100</option><option value="200">200</option></select> </div></div></div><div class="col-xs-8 col-md-4  clear-padding disinpad10txtcen"  data-bind="visible: totalItemCount"><div class="clear-padding col-xs-12 col-sm-6 col-md-12 bor0" ><ul class="pagination pagination"><li class="disabled"><a href="#" onclick="FirstPageLoad_paginationChild(\'Quote\',\'\',\''
		+str(table_id)
		+'\')"><i class="fa fa-caret-left font14whtbld" ></i><i class="fa fa-caret-left font14" ></i></a></li><li class="disabled"><a href="#" onclick="Previous12334Child(\'Quote\',\'\',\''
		+str(table_id)
		+'\')"><i class="fa fa-caret-left font14" ></i>PREVIOUS</a></li><li class="disabled"><a href="#" class="disabledPage" onclick="Next12334Child(\'Quote\',\'\',\''
		+str(table_id)
		+'\')">NEXT<i class="fa fa-caret-right font14" ></i></a></li><li class="disabled"><a href="#" onclick="LastPageLoad_paginationChild(\'Quote\',\'\',\''
		+str(table_id)
		+'\')" class="disabledPage"><i class="fa fa-caret-right font14"></i><i class="fa fa-caret-right font14whtbld"></i></a></li></ul></div> </div> <div class="col-md-4 pr_page_pad"> <span id="'
		+ str(table_id)
		+ '___page_count"  class="currentPage page_right_content">1</span><span class="page_right_content pad_rt_2">Page </span></div></div>'
	)

	if QueryCount < int(PerPage):
		PerPage = str(QueryCount)
	else:
		PerPage = str(PerPage)   
	if Page_End > QueryCount:
		Page_End = QueryCount
	else:
		Page_End = Page_End
	# Trace.Write("Page_start----->"+str(Page_start))     
	# Trace.Write("Page_End----->"+str(Page_End))    
	Action_Str = ""
	Action_Str += str(Page_start)+" - "
	Action_Str += str(Page_End)
	Action_Str += " of"

	return (
		table_header,
		chld_list,
		table_id,
		filter_control_function,
		NORECORDS,
		dbl_clk_function,
		cv_list,
		filter_level_list,
		DropDownList,
		RelatedDrop_str,
		Test,
		Action_Str,
	)

def GetSendingEquipmentChild(recid, PerPage, PageInform, A_Keys, A_Values):
	# This function is used to construct the table inside the Sending Equipment Parent Table.(As Nested Table).

	TreeParam = Product.GetGlobal("TreeParam")
	TreeParentParam = Product.GetGlobal("TreeParentLevel0")
	TreeSuperParentParam = Product.GetGlobal("TreeParentLevel1")
	TreeTopSuperParentParam = Product.GetGlobal("TreeParentLevel2")
	if str(PerPage) == "" and str(PageInform) == "":
		Page_start = 1
		Page_End = 10
		PerPage = 10
		PageInform = "1___10___10"
	else:
		Page_start = int(PageInform.split("___")[0])
		Page_End = int(PageInform.split("___")[1])
		PerPage = PerPage
	QueryCount = ""
	chld_list = []
	FablocationId = Product.GetGlobal("TreeParam")
	ContractRecordId = Quote.GetGlobal("contract_quote_record_id")
	RevisionRecordId = Quote.GetGlobal("quote_revision_record_id")
	obj_idval = "SYOBJ_1176889_SYOBJ_1176889"
	obj_id1 = "SYOBJ-1176889"
	objh_getid = Sql.GetFirst(
		"SELECT TOP 1  RECORD_ID  FROM SYOBJH (NOLOCK) WHERE SAPCPQ_ATTRIBUTE_NAME='" + str(obj_id1) + "'"
	)
	if objh_getid:
		obj_id1 = objh_getid.RECORD_ID
	objs_obj1 = Sql.GetFirst(
		"select CAN_ADD,CAN_EDIT,COLUMNS,CAN_DELETE from SYOBJR (NOLOCK) where OBJ_REC_ID = '" + str(obj_id1) + "' "
	)
	can_edit1 = str(objs_obj1.CAN_EDIT)
	can_add1 = str(objs_obj1.CAN_ADD)
	can_delete1 = str(objs_obj1.CAN_DELETE)
	table_id = "table_sending_equipment_child_"+str(recid)
	edit_button =""
	table_header = (
		'<table id="'
		+ str(table_id)
		+ '" data-pagination="false" data-sortable="true" data-search-on-enter-key="true" data-filter-control="true" data-pagination-loop = "false" data-locale = "en-US" ><thead>'
	)
	Columns = [
		"INCLUDED",
		"QUOTE_SERVICE_SENDING_FAB_EQUIP_ASS_ID",
		"EQUIPMENTCATEGORY_ID",
		"SND_ASSEMBLY_ID",
		"SND_ASSEMBLY_DESCRIPTION",
		"EQUIPMENTTYPE_ID",
		"GOT_CODE",
		"SNDFBL_ID",
		"GREENBOOK"
	]
	Objd_Obj = Sql.GetList(
		"select FIELD_LABEL,API_NAME,LOOKUP_OBJECT,LOOKUP_API_NAME,DATA_TYPE from SYOBJD (NOLOCK) where OBJECT_NAME = 'SAQSSA'"
	)
	attr_list = []
	attrs_datatype_dict = {}
	lookup_disply_list = []
	lookup_str = ""
	if Objd_Obj is not None:
		attr_list = {}
		for attr in Objd_Obj:
			attr_list[str(attr.API_NAME)] = str(attr.FIELD_LABEL)
			attrs_datatype_dict[str(attr.API_NAME)] = str(attr.DATA_TYPE)
			if attr.LOOKUP_API_NAME != "" and attr.LOOKUP_API_NAME is not None:
				lookup_disply_list.append(str(attr.API_NAME))
		checkbox_list = [inn.API_NAME for inn in Objd_Obj if inn.DATA_TYPE == "CHECKBOX"]
		lookup_list = {ins.LOOKUP_API_NAME: ins.API_NAME for ins in Objd_Obj}
	lookup_str = ",".join(list(lookup_disply_list))
	GetSaleType = Sql.GetFirst("SELECT SALE_TYPE FROM SAQTMT WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{}'".format(ContractRecordId))
	GetSaleType = Sql.GetList("SELECT CpqTableEntryId FROM SAQTIP WHERE (PARTY_ROLE = 'RECEIVING ACCOUNT' OR PARTY_ROLE = 'SENDING ACCOUNT') AND QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(Quote.GetGlobal("contract_quote_record_id"),Quote.GetGlobal("quote_revision_record_id")))
		#Trace.Write("count--"+str(list(GetToolReloc)))
	GetSaleType = list(GetSaleType)
	if len(GetSaleType) == 2:
		sale_type = "TOOL RELOCATION"
	else:
		sale_type = None
	if sale_type != "TOOL RELOCATION":
		if TreeParentParam == 'Complementary Products':
			Parent_Equipmentid = Sql.GetFirst(
				"select SND_EQUIPMENT_ID from SAQSSE (NOLOCK) where QUOTE_RECORD_ID = '{ContractRecordId}' AND  QTEREV_RECORD_ID = '{RevisionRecordId}' AND SND_EQUIPMENT_ID = '{EquipmentId}'".format(
					ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),
					RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"),
					EquipmentId=recid,
				)
			)
		elif TreeSuperParentParam == 'Complementary Products':
			Parent_Equipmentid = Sql.GetFirst(
				"select SND_EQUIPMENT_ID from SAQSSE (NOLOCK) where QUOTE_RECORD_ID = '{ContractRecordId}' AND  QTEREV_RECORD_ID = '{RevisionRecordId}' AND SND_EQUIPMENT_ID = '{EquipmentId}' AND SERVICE_ID = '{TreeParentParam}'".format(
					ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),
					RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"),
					EquipmentId=recid,TreeParentParam=TreeParentParam
				)
			)
		elif TreeParentParam == 'Sending Equipment':
			Parent_Equipmentid = Sql.GetFirst(
				"select SND_EQUIPMENT_ID from SAQSSE (NOLOCK) where QUOTE_RECORD_ID = '{ContractRecordId}'  AND  QTEREV_RECORD_ID = '{RevisionRecordId}' AND SND_EQUIPMENT_ID = '{EquipmentId}' AND SERVICE_ID = '{TreeSuperParentParam}' AND SNDFBL_ID='{TreeParam}'".format(
					ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),
					RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"),
					EquipmentId=recid,TreeSuperParentParam=TreeSuperParentParam,TreeParam=TreeParam
				)
			)
		elif TreeSuperParentParam == 'Sending Equipment':
			Parent_Equipmentid = Sql.GetFirst(
				"select SND_EQUIPMENT_ID from SAQSSE (NOLOCK) where QUOTE_RECORD_ID = '{ContractRecordId}' AND  QTEREV_RECORD_ID = '{RevisionRecordId}' AND SND_EQUIPMENT_ID = '{EquipmentId}' AND SERVICE_ID = '{TreeTopSuperParentParam}' AND SNDFBL_ID='{TreeParentParam}'".format(
					ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),
					RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"),
					EquipmentId=recid,TreeTopSuperParentParam=TreeTopSuperParentParam,TreeParentParam=TreeParentParam
				)
			)
	#     elif TreeParentParam == 'Fab Locations':
	#         Parent_Equipmentid = Sql.GetFirst(
	#             "select EQUIPMENT_ID from SAQFEQ (NOLOCK) where QUOTE_RECORD_ID = '{ContractRecordId}' and FABLOCATION_ID = '{FablocationId}' AND EQUIPMENT_ID = '{EquipmentId}' AND ISNULL(SERIAL_NUMBER,'') <> ''".format(
	#                 ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),
	#                 FablocationId=Product.GetGlobal("TreeParam"),
	#                 EquipmentId=recid,
	#             )
	#         )
	#     elif TreeSuperParentParam == 'Fab Locations':
	#         Parent_Equipmentid = Sql.GetFirst(
	#             "select EQUIPMENT_ID from SAQFEQ (NOLOCK) where QUOTE_RECORD_ID = '{ContractRecordId}' and FABLOCATION_ID = '{FablocationId}' AND EQUIPMENT_ID = '{EquipmentId}'AND GREENBOOK = '{GreenBook}' AND ISNULL(SERIAL_NUMBER,'') <> ''".format(
	#                 ContractRecordId = Quote.GetGlobal("contract_quote_record_id"),
	#                 FablocationId = Product.GetGlobal("TreeParentLevel0"),
	#                 EquipmentId = recid,
	#                 GreenBook = Product.GetGlobal("TreeParam"),
	#             )
	#         )
	elif sale_type == "TOOL RELOCATION":
		if TreeParentParam == 'Complementary Products':
			Parent_Equipmentid = Sql.GetFirst(
				"select SND_EQUIPMENT_ID from SAQSSE (NOLOCK) where QUOTE_RECORD_ID = '{ContractRecordId}' AND  QTEREV_RECORD_ID = '{RevisionRecordId}' AND SND_EQUIPMENT_ID = '{EquipmentId}'".format(
					ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),
					RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"),
					EquipmentId=recid,
				)
			)
		elif TreeSuperParentParam == 'Complementary Products':
			Parent_Equipmentid = Sql.GetFirst(
				"select SND_EQUIPMENT_ID from SAQSSE (NOLOCK) where QUOTE_RECORD_ID = '{ContractRecordId}' AND  QTEREV_RECORD_ID = '{RevisionRecordId}' AND SND_EQUIPMENT_ID = '{EquipmentId}' AND SERVICE_ID = '{TreeParentParam}'".format(
					ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),
					RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"),
					EquipmentId=recid,TreeParentParam=TreeParentParam
				)
			)
		elif TreeParentParam == 'Sending Equipment':
			Parent_Equipmentid = Sql.GetFirst(
				"select SND_EQUIPMENT_ID from SAQSSE (NOLOCK) where QUOTE_RECORD_ID = '{ContractRecordId}'  AND  QTEREV_RECORD_ID = '{RevisionRecordId}' AND SND_EQUIPMENT_ID = '{EquipmentId}' AND SERVICE_ID = '{TreeSuperParentParam}' AND SNDFBL_ID = '{TreeParam}'".format(
					ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),
					RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"),
					EquipmentId=recid,TreeSuperParentParam=TreeSuperParentParam,TreeParam=TreeParam
				)
			)
		elif TreeSuperParentParam == 'Sending Equipment':
			Parent_Equipmentid = Sql.GetFirst(
				"select SND_EQUIPMENT_ID from SAQSSE (NOLOCK) where QUOTE_RECORD_ID = '{ContractRecordId}' AND  QTEREV_RECORD_ID = '{RevisionRecordId}' AND SND_EQUIPMENT_ID = '{EquipmentId}' AND SERVICE_ID = '{TreeTopSuperParentParam}' AND SNDFBL_ID = '{TreeParentParam}'".format(
					ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),
					RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"),
					EquipmentId=recid,TreeTopSuperParentParam=TreeTopSuperParentParam,TreeParentParam=TreeParentParam
				)
			)
		
	

	if Parent_Equipmentid:
		EquipmentID = Parent_Equipmentid.SND_EQUIPMENT_ID
			# child_obj_recid = Sql.GetList("select  top 5 EQUIPMENT_ID from SAQFEA (NOLOCK) where EQUIPMENT_ID = '{EquipmentID}' and QUOTE_RECORD_ID = '{ContractRecordId}' and FABLOCATION_ID = '{FablocationId}'".format(EquipmentID = Parent_Equipmentid.EQUIPMENT_ID,ContractRecordId = Quote.GetGlobal("contract_quote_record_id"),FablocationId = Product.GetGlobal("TreeParam")))
		if sale_type != "TOOL RELOCATION":
			Trace.Write("NON_TOOL_RELOCATION")
			if TreeParentParam == 'Complementary Products':
				child_obj_recid = Sql.GetList(
					"select top "+str(PerPage)+" * from (select ROW_NUMBER() OVER( ORDER BY QUOTE_SERVICE_SENDING_FAB_EQUIP_ASS_ID) AS ROW, QUOTE_SERVICE_SENDING_FAB_EQUIP_ASS_ID,SND_EQUIPMENT_ID,SND_ASSEMBLY_ID,SND_ASSEMBLY_DESCRIPTION,GOT_CODE,SNDFBL_ID,GREENBOOK,EQUIPMENTCATEGORY_ID,EQUIPMENTTYPE_ID,INCLUDED from SAQSSA (NOLOCK) where SND_EQUIPMENT_ID = '"
					+ str(recid)
					+ "' AND QTEREV_RECORD_ID = '{}' ".format(str(Quote.GetGlobal("quote_revision_record_id")))
					+ " and QUOTE_RECORD_ID = '{ContractRecordId}' AND  QTEREV_RECORD_ID = '{RevisionRecordId}' ) m where m.ROW BETWEEN ".format(
							ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),
							RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"),
						)
					+ str(Page_start)
					+ " and "
					+ str(Page_End)
				)
				QueryCountObj = Sql.GetFirst(
				"select count(CpqTableEntryId) as cnt from SAQSSA (NOLOCK) where QUOTE_RECORD_ID = '"
				+ str(ContractRecordId)
				+ "'and SND_EQUIPMENT_ID = '"
				+ str(EquipmentID)
				+ "'"
				+ " AND QTEREV_RECORD_ID = '{}' ".format(str(Quote.GetGlobal("quote_revision_record_id")))
				) 
			elif TreeSuperParentParam == 'Complementary Products':
					child_obj_recid = Sql.GetList(
						"select top "+str(PerPage)+" * from (select ROW_NUMBER() OVER( ORDER BY QUOTE_SERVICE_SENDING_FAB_EQUIP_ASS_ID) AS ROW, QUOTE_SERVICE_SENDING_FAB_EQUIP_ASS_ID,SND_EQUIPMENT_ID,SND_ASSEMBLY_ID,SND_ASSEMBLY_DESCRIPTION,GOT_CODE,SNDFBL_ID,GREENBOOK,EQUIPMENTCATEGORY_ID,EQUIPMENTTYPE_ID,INCLUDED from SAQSSA (NOLOCK) where SND_EQUIPMENT_ID = '"
						+ str(recid)
						+ "' AND QTEREV_RECORD_ID = '{}' ".format(str(Quote.GetGlobal("quote_revision_record_id")))
						+ " and QUOTE_RECORD_ID = '{ContractRecordId}' and SERVICE_ID = '{TreeParentParam}') m where m.ROW BETWEEN ".format(
								ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),TreeParentParam = TreeParentParam
							)
						+ str(Page_start)
						+ " and "
						+ str(Page_End)
					)
					QueryCountObj = Sql.GetFirst(
					"select count(CpqTableEntryId) as cnt from SAQSSA (NOLOCK) where QUOTE_RECORD_ID = '"
					+ str(ContractRecordId)
					+ "'and SND_EQUIPMENT_ID = '"
					+ str(EquipmentID)
					+ "' and SERVICE_ID = '"
					+str(TreeParentParam)
					+"'"
					+ " AND QTEREV_RECORD_ID = '{}' ".format(str(Quote.GetGlobal("quote_revision_record_id")))
					) 
			elif TreeParentParam == 'Sending Equipment':
				child_obj_recid = Sql.GetList(
					"select top "+str(PerPage)+" * from (select ROW_NUMBER() OVER( ORDER BY QUOTE_SERVICE_SENDING_FAB_EQUIP_ASS_ID) AS ROW, QUOTE_SERVICE_SENDING_FAB_EQUIP_ASS_ID,SND_EQUIPMENT_ID,SND_ASSEMBLY_ID,SND_ASSEMBLY_DESCRIPTION,GOT_CODE,SNDFBL_ID,GREENBOOK,EQUIPMENTCATEGORY_ID,EQUIPMENTTYPE_ID,INCLUDED from SAQSSA (NOLOCK) where SND_EQUIPMENT_ID = '"
					+ str(recid)
					+ "' AND QTEREV_RECORD_ID = '{}' ".format(str(Quote.GetGlobal("quote_revision_record_id")))
					+ " and QUOTE_RECORD_ID = '{ContractRecordId}' and SERVICE_ID = '{TreeSuperParentParam}' and SNDFBL_ID = '{TreeParam}') m where m.ROW BETWEEN ".format(
							ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),TreeSuperParentParam = TreeSuperParentParam,TreeParam=TreeParam
						)
					+ str(Page_start)
					+ " and "
					+ str(Page_End)
				)
				QueryCountObj = Sql.GetFirst(
				"select count(CpqTableEntryId) as cnt from SAQSSA (NOLOCK) where QUOTE_RECORD_ID = '"
				+ str(ContractRecordId)
				+ "'and SND_EQUIPMENT_ID = '"
				+ str(EquipmentID)
				+ "' and SERVICE_ID = '"
				+str(TreeSuperParentParam)
				+"' and SNDFBL_ID = '"
				+str(TreeParam)
				+"'"
				+ " AND QTEREV_RECORD_ID = '{}' ".format(str(Quote.GetGlobal("quote_revision_record_id")))
					
				) 
			elif TreeSuperParentParam == 'Sending Equipment':
				child_obj_recid = Sql.GetList(
					"select top "+str(PerPage)+" * from (select ROW_NUMBER() OVER( ORDER BY QUOTE_SERVICE_SENDING_FAB_EQUIP_ASS_ID) AS ROW, QUOTE_SERVICE_SENDING_FAB_EQUIP_ASS_ID,SND_EQUIPMENT_ID,SND_ASSEMBLY_ID,SND_ASSEMBLY_DESCRIPTION,GOT_CODE,SNDFBL_ID,GREENBOOK,EQUIPMENTCATEGORY_ID,EQUIPMENTTYPE_ID,INCLUDED from SAQSSA (NOLOCK) where SND_EQUIPMENT_ID = '"
					+ str(recid)
					+ "' AND QTEREV_RECORD_ID = '{}' ".format(str(Quote.GetGlobal("quote_revision_record_id")))
					+ " and QUOTE_RECORD_ID = '{ContractRecordId}' and SERVICE_ID = '{TreeTopSuperParentParam}' and SNDFBL_ID = '{TreeParentParam}') m where m.ROW BETWEEN ".format(
							ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),TreeTopSuperParentParam = TreeTopSuperParentParam,TreeParentParam=TreeParentParam
						)
					+ str(Page_start)
					+ " and "
					+ str(Page_End)
				)
				QueryCountObj = Sql.GetFirst(
				"select count(CpqTableEntryId) as cnt from SAQSSA (NOLOCK) where QUOTE_RECORD_ID = '"
				+ str(ContractRecordId)
				+ "'and SND_EQUIPMENT_ID = '"
				+ str(EquipmentID)
				+ "' and SERVICE_ID = '"
				+str(TreeTopSuperParentParam)
				+"' and SNDFBL_ID = '"
				+str(TreeParentParam)
				+"'"
				+ " AND QTEREV_RECORD_ID = '{}' ".format(str(Quote.GetGlobal("quote_revision_record_id")))
				) 
			# elif TreeParentParam == 'Fab Locations':
			#     child_obj_recid = Sql.GetList(
			#         "select top "+str(PerPage)+" * from (select ROW_NUMBER() OVER( ORDER BY QUOTE_FAB_LOC_COV_OBJ_ASSEMBLY_RECORD_ID) AS ROW, QUOTE_FAB_LOC_COV_OBJ_ASSEMBLY_RECORD_ID,EQUIPMENT_ID,SERIAL_NUMBER,ASSEMBLY_ID,ASSEMBLY_DESCRIPTION,GOT_CODE,MNT_PLANT_ID,FABLOCATION_ID,WARRANTY_START_DATE,EQUIPMENTCATEGORY_ID,WARRANTY_END_DATE,SALESORG_ID,EQUIPMENTTYPE_ID from SAQFEA (NOLOCK) where EQUIPMENT_ID = '"
			#         + str(recid)
			#         + "' and QUOTE_RECORD_ID = '{ContractRecordId}' and FABLOCATION_ID = '{FablocationId}') m where m.ROW BETWEEN ".format(
			#             ContractRecordId=Quote.GetGlobal("contract_quote_record_id"), FablocationId=Product.GetGlobal("TreeParam")
			#         )
			#         + str(Page_start)
			#         + " and "
			#         + str(Page_End)
			#     )
			#     QueryCountObj = Sql.GetFirst(
			#     "select count(CpqTableEntryId) as cnt from SAQFEA (NOLOCK) where QUOTE_RECORD_ID = '"
			#     + str(ContractRecordId)
			#     + "' and FABLOCATION_ID = '"
			#     + str(TreeParam)
			#     + "' and EQUIPMENT_ID = '"
			#     + str(EquipmentID)
			#     + "'"
			# )
			# elif TreeSuperParentParam == 'Fab Locations':
			#     child_obj_recid = Sql.GetList(
			#         "select top "+str(PerPage)+" * from (select ROW_NUMBER() OVER( ORDER BY QUOTE_FAB_LOC_COV_OBJ_ASSEMBLY_RECORD_ID) AS ROW, QUOTE_FAB_LOC_COV_OBJ_ASSEMBLY_RECORD_ID,EQUIPMENT_ID,SERIAL_NUMBER,ASSEMBLY_ID,ASSEMBLY_DESCRIPTION,GOT_CODE,MNT_PLANT_ID,FABLOCATION_ID,WARRANTY_START_DATE,EQUIPMENTCATEGORY_ID,WARRANTY_END_DATE,SALESORG_ID,EQUIPMENTTYPE_ID from SAQFEA (NOLOCK) where EQUIPMENT_ID = '"
			#         + str(recid)
			#         + "' and QUOTE_RECORD_ID = '{ContractRecordId}' and FABLOCATION_ID = '{FablocationId}')m where m.ROW BETWEEN ".format(
			#         ContractRecordId=Quote.GetGlobal("contract_quote_record_id"), FablocationId=TreeParentParam
			#         )
			#         + str(Page_start)
			#         + " and "
			#         + str(Page_End)
			#     )
			#     QueryCountObj = Sql.GetFirst(
			#     "select count(CpqTableEntryId) as cnt from SAQFEA (NOLOCK) where QUOTE_RECORD_ID = '"
			#     + str(ContractRecordId)
			#     + "' and FABLOCATION_ID = '"
			#     + str(TreeParentParam)
			#     + "' and EQUIPMENT_ID = '"
			#     + str(EquipmentID)
			#     + "'"
			# )
		elif sale_type == "TOOL RELOCATION":
			Trace.Write("TOOL_RELOCATION"+str(TreeSuperParentParam))
			if TreeParentParam == 'Complementary Products':
				child_obj_recid = Sql.GetList(
					"select top "+str(PerPage)+" * from (select ROW_NUMBER() OVER( ORDER BY QUOTE_SERVICE_SENDING_FAB_EQUIP_ASS_ID) AS ROW, QUOTE_SERVICE_SENDING_FAB_EQUIP_ASS_ID,SND_EQUIPMENT_ID,SND_ASSEMBLY_ID,SND_ASSEMBLY_DESCRIPTION,GOT_CODE,SNDFBL_ID,GREENBOOK,EQUIPMENTCATEGORY_ID,EQUIPMENTTYPE_ID,INCLUDED from SAQSSA (NOLOCK) where SND_EQUIPMENT_ID = '"
					+ str(recid)
					+ "' AND QTEREV_RECORD_ID = '{}' ".format(str(Quote.GetGlobal("quote_revision_record_id")))
					+ " and QUOTE_RECORD_ID = '{ContractRecordId}') m where m.ROW BETWEEN ".format(
							ContractRecordId=Quote.GetGlobal("contract_quote_record_id")
						)
					+ str(Page_start)
					+ " and "
					+ str(Page_End)
					)
				QueryCountObj = Sql.GetFirst(
					"select count(CpqTableEntryId) as cnt from SAQSSA (NOLOCK) where QUOTE_RECORD_ID = '"
					+ str(ContractRecordId)
					+ "'and SND_EQUIPMENT_ID = '"
					+ str(EquipmentID)
					+ "'"
					+ " AND QTEREV_RECORD_ID = '{}' ".format(str(Quote.GetGlobal("quote_revision_record_id")))
					) 

			elif TreeSuperParentParam == 'Complementary Products':
				edit_button = '<button id="assembly_edit" onclick="SendEqupAssemblyEdit()" class="m-5px btnconfig">EDIT</button><button class="m-5px btnconfig" id="assembly_save" style="display:none" onclick="SendEqupAssemblySave()" >SAVE</button><button  id="assembly_cancel" style="display:none" onclick="SendEqupAssemblyCancel()" class="m-5px mr-0 btnconfig">CANCEL</button>'
				
				child_obj_recid = Sql.GetList(
					"select top "+str(PerPage)+" * from (select ROW_NUMBER() OVER( ORDER BY QUOTE_SERVICE_SENDING_FAB_EQUIP_ASS_ID) AS ROW, QUOTE_SERVICE_SENDING_FAB_EQUIP_ASS_ID,SND_EQUIPMENT_ID,SND_ASSEMBLY_ID,SND_ASSEMBLY_DESCRIPTION,GOT_CODE,SNDFBL_ID,GREENBOOK,EQUIPMENTCATEGORY_ID,EQUIPMENTTYPE_ID,INCLUDED from SAQSSA (NOLOCK) where SND_EQUIPMENT_ID = '"
					+ str(recid)
					+ "' AND QTEREV_RECORD_ID = '{}' ".format(str(Quote.GetGlobal("quote_revision_record_id")))
					+ " and QUOTE_RECORD_ID = '{ContractRecordId}' and SERVICE_ID = '{TreeParentParam}') m where m.ROW BETWEEN ".format(
							ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),TreeParentParam=TreeParentParam
						)
					+ str(Page_start)
					+ " and "
					+ str(Page_End)
					)
				QueryCountObj = Sql.GetFirst(
					"select count(CpqTableEntryId) as cnt from SAQSSA (NOLOCK) where QUOTE_RECORD_ID = '"
					+ str(ContractRecordId)
					+ "'and SND_EQUIPMENT_ID = '"
					+ str(EquipmentID)
					+ "' and SERVICE_ID = '"
					+str(TreeParentParam)
					+"'"
					+ " AND QTEREV_RECORD_ID = '{}' ".format(str(Quote.GetGlobal("quote_revision_record_id")))
					) 
			elif TreeParentParam == 'Sending Equipment':
				child_obj_recid = Sql.GetList(
					"select top "+str(PerPage)+" * from (select ROW_NUMBER() OVER( ORDER BY QUOTE_SERVICE_SENDING_FAB_EQUIP_ASS_ID) AS ROW, QUOTE_SERVICE_SENDING_FAB_EQUIP_ASS_ID,SND_EQUIPMENT_ID,SND_ASSEMBLY_ID,SND_ASSEMBLY_DESCRIPTION,GOT_CODE,SNDFBL_ID,GREENBOOK,EQUIPMENTCATEGORY_ID,EQUIPMENTTYPE_ID,INCLUDED from SAQSSA (NOLOCK) where SND_EQUIPMENT_ID = '"
					+ str(recid)
					+ "' AND QTEREV_RECORD_ID = '{}' ".format(str(Quote.GetGlobal("quote_revision_record_id")))
					+ " and QUOTE_RECORD_ID = '{ContractRecordId}' and SERVICE_ID = '{TreeSuperParentParam}' and SNDFBL_ID = '{TreeParam}') m where m.ROW BETWEEN ".format(
							ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),TreeSuperParentParam=TreeSuperParentParam,TreeParam=TreeParam
						)
					+ str(Page_start)
					+ " and "
					+ str(Page_End)
					)
				QueryCountObj = Sql.GetFirst(
					"select count(CpqTableEntryId) as cnt from SAQSSA (NOLOCK) where QUOTE_RECORD_ID = '"
					+ str(ContractRecordId)
					+ "'and SND_EQUIPMENT_ID = '"
					+ str(EquipmentID)
					+ "' and SERVICE_ID = '"
					+str(TreeParentParam)
					+"' and SNDFBL_ID = '"
					+str(TreeParam)
					+"'"
					+ " AND QTEREV_RECORD_ID = '{}' ".format(str(Quote.GetGlobal("quote_revision_record_id")))
					) 
			elif TreeSuperParentParam == 'Sending Equipment':
				child_obj_recid = Sql.GetList(
					"select top "+str(PerPage)+" * from (select ROW_NUMBER() OVER( ORDER BY QUOTE_SERVICE_SENDING_FAB_EQUIP_ASS_ID) AS ROW, QUOTE_SERVICE_SENDING_FAB_EQUIP_ASS_ID,SND_EQUIPMENT_ID,SND_ASSEMBLY_ID,SND_ASSEMBLY_DESCRIPTION,GOT_CODE,SNDFBL_ID,GREENBOOK,EQUIPMENTCATEGORY_ID,EQUIPMENTTYPE_ID,INCLUDED from SAQSSA (NOLOCK) where SND_EQUIPMENT_ID = '"
					+ str(recid)
					+ "' AND QTEREV_RECORD_ID = '{}' ".format(str(Quote.GetGlobal("quote_revision_record_id")))
					+ " and QUOTE_RECORD_ID = '{ContractRecordId}' and SERVICE_ID = '{TreeTopSuperParentParam}' and SNDFBL_ID = '{TreeParentParam}') m where m.ROW BETWEEN ".format(
							ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),TreeTopSuperParentParam=TreeTopSuperParentParam,TreeParentParam=TreeParentParam
						)
					+ str(Page_start)
					+ " and "
					+ str(Page_End)
					)
				QueryCountObj = Sql.GetFirst(
					"select count(CpqTableEntryId) as cnt from SAQSSA (NOLOCK) where QUOTE_RECORD_ID = '"
					+ str(ContractRecordId)
					+ "'and SND_EQUIPMENT_ID = '"
					+ str(EquipmentID)
					+ "' and SERVICE_ID = '"
					+str(TreeTopSuperParentParam)
					+"' and SNDFBL_ID = '"
					+str(TreeParentParam)
					+"'"
					+ " AND QTEREV_RECORD_ID = '{}' ".format(str(Quote.GetGlobal("quote_revision_record_id")))
					) 
			# elif TreeParentParam == 'Fab Locations':
			#     child_obj_recid = Sql.GetList(
			#         "select top "+str(PerPage)+" * from (select ROW_NUMBER() OVER( ORDER BY QUOTE_FAB_LOC_COV_OBJ_ASSEMBLY_RECORD_ID) AS ROW, QUOTE_FAB_LOC_COV_OBJ_ASSEMBLY_RECORD_ID,EQUIPMENT_ID,SERIAL_NUMBER,ASSEMBLY_ID,ASSEMBLY_DESCRIPTION,GOT_CODE,MNT_PLANT_ID,FABLOCATION_ID,WARRANTY_START_DATE,EQUIPMENTCATEGORY_ID,WARRANTY_END_DATE,SALESORG_ID,EQUIPMENTTYPE_ID from SAQFEA (NOLOCK) where EQUIPMENT_ID = '"
			#         + str(recid)
			#         + "' and QUOTE_RECORD_ID = '{ContractRecordId}' ) m where m.ROW BETWEEN ".format(
			#             ContractRecordId=Quote.GetGlobal("contract_quote_record_id"), FablocationId=Product.GetGlobal("TreeParam")
			#         )
			#         + str(Page_start)
			#         + " and "
			#         + str(Page_End)
			#     )
			#     QueryCountObj = Sql.GetFirst(
			#     "select count(CpqTableEntryId) as cnt from SAQFEA (NOLOCK) where QUOTE_RECORD_ID = '"
			#     + str(ContractRecordId)
			#     + "' and EQUIPMENT_ID = '"
			#     + str(EquipmentID)
			#     + "'"
			#     )
			# elif TreeSuperParentParam == 'Fab Locations':
			#     child_obj_recid = Sql.GetList(
			#         "select top "+str(PerPage)+" * from (select ROW_NUMBER() OVER( ORDER BY QUOTE_FAB_LOC_COV_OBJ_ASSEMBLY_RECORD_ID) AS ROW, QUOTE_FAB_LOC_COV_OBJ_ASSEMBLY_RECORD_ID,EQUIPMENT_ID,SERIAL_NUMBER,ASSEMBLY_ID,ASSEMBLY_DESCRIPTION,GOT_CODE,MNT_PLANT_ID,FABLOCATION_ID,WARRANTY_START_DATE,EQUIPMENTCATEGORY_ID,WARRANTY_END_DATE,SALESORG_ID,EQUIPMENTTYPE_ID from SAQFEA (NOLOCK) where EQUIPMENT_ID = '"
			#         + str(recid)
			#         + "' and QUOTE_RECORD_ID = '{ContractRecordId}' and FABLOCATION_ID = '{FablocationId}')m where m.ROW BETWEEN ".format(
			#         ContractRecordId=Quote.GetGlobal("contract_quote_record_id"), FablocationId=TreeParam
			#         )
			#         + str(Page_start)
			#         + " and "
			#         + str(Page_End)
			#     )
			#     QueryCountObj = Sql.GetFirst(
			#     "select count(CpqTableEntryId) as cnt from SAQFEA (NOLOCK) where QUOTE_RECORD_ID = '"
			#     + str(ContractRecordId)
			#     + "' and FABLOCATION_ID = '"
			#     + str(TreeParam)
			#     + "' and EQUIPMENT_ID = '"
			#     + str(EquipmentID)
			#     + "'"
			# ) 
			# elif TreeTopSuperParentParam == 'Fab Locations':
			#     child_obj_recid = Sql.GetList(
			#         "select top "+str(PerPage)+" * from (select ROW_NUMBER() OVER( ORDER BY QUOTE_FAB_LOC_COV_OBJ_ASSEMBLY_RECORD_ID) AS ROW, QUOTE_FAB_LOC_COV_OBJ_ASSEMBLY_RECORD_ID,EQUIPMENT_ID,SERIAL_NUMBER,ASSEMBLY_ID,ASSEMBLY_DESCRIPTION,GOT_CODE,MNT_PLANT_ID,FABLOCATION_ID,WARRANTY_START_DATE,EQUIPMENTCATEGORY_ID,WARRANTY_END_DATE,SALESORG_ID,EQUIPMENTTYPE_ID from SAQFEA (NOLOCK) where EQUIPMENT_ID = '"
			#         + str(recid)
			#         + "' and QUOTE_RECORD_ID = '{ContractRecordId}' and FABLOCATION_ID = '{FablocationId}')m where m.ROW BETWEEN ".format(
			#         ContractRecordId=Quote.GetGlobal("contract_quote_record_id"), FablocationId=TreeParentParam
			#         )
			#         + str(Page_start)
			#         + " and "
			#         + str(Page_End)
			#     )
			#     QueryCountObj = Sql.GetFirst(
			#     "select count(CpqTableEntryId) as cnt from SAQFEA (NOLOCK) where QUOTE_RECORD_ID = '"
			#     + str(ContractRecordId)
			#     + "' and FABLOCATION_ID = '"
			#     + str(TreeParentParam)
			#     + "' and EQUIPMENT_ID = '"
			#     + str(EquipmentID)
			#     + "'"
			# ) 
		chld_list = []
		QueryCount = ""
		if QueryCountObj is not None:
			QueryCount = QueryCountObj.cnt
		# Data construction for table.
		for child in child_obj_recid:
			data_id = str(child.QUOTE_SERVICE_SENDING_FAB_EQUIP_ASS_ID) + "|SAQSSA"
			chld_dict = {}
			Action_str1 = (
				'<div class="btn-group dropdown"><div class="dropdown" id="ctr_drop"><i data-toggle="dropdown" id="dropdownMenuButton" class="fa fa-sort-desc dropdown-toggle" aria-expanded="false"></i><ul class="dropdown-menu left" aria-labelledby="dropdownMenuButton"><li><a  data-toggle="modal" data-target="#cont_viewModalSection" id="'
				+ str(data_id)
				+ '" class="dropdown-item cur_sty" href="#"  onclick="cont_relatedlist_openview(this) ">VIEW</a></li>'
			)
			if can_edit1.upper() == "TRUE":
				Action_str1 += (
					'<li  ><a data-toggle="modal" data-target="#cont_viewModalSection" id="'
					+ str(data_id)
					+ '"  class="dropdown-item cur_sty" href="#"  onclick="cont_relatedlist_openedit(this)">EDIT</a></li>'
				)
			if can_delete1.upper() == "TRUE":
				Action_str1 += '<li><a class="dropdown-item" data-target="#cont_viewModal_Material_Delete" data-toggle="modal" onclick="Material_delete_obj(this)" href="#">DELETE</a></li>'
			if can_add1.upper() == "TRUE":
				Action_str1 += '<li><a class="dropdown-item" data-target="#" data-toggle="modal" onclick="Material_clone_obj(this)" href="#">CLONE</a></li>'
			Action_str1 += "</ul></div></div>"

			# data formation in Dictonary format.
			chld_dict["ids"] = str(data_id)
			chld_dict["ACTIONS"] = str(Action_str1)
			#included_id = str(child.QUOTE_SERVICE_SENDING_FAB_EQUIP_ASS_ID) + "|INCLUDED"
			chld_dict["INCLUDED"] = str(child.INCLUDED)
			chld_dict["QUOTE_SERVICE_SENDING_FAB_EQUIP_ASS_ID"] = CPQID.KeyCPQId.GetCPQId(
				"SAQSSA", str(child.QUOTE_SERVICE_SENDING_FAB_EQUIP_ASS_ID)
			)
			chld_dict["EQUIPMENTCATEGORY_ID"] = ('<abbr id ="" title="' + str(child.EQUIPMENTCATEGORY_ID) + '">' + str(child.EQUIPMENTCATEGORY_ID) + "</abbr>") 
			# chld_dict["SERIAL_NUMBER"] = ('<abbr id ="" title="' + str(child.SERIAL_NUMBER) + '">' + str(child.SERIAL_NUMBER) + "</abbr>") 
			chld_dict["SND_ASSEMBLY_ID"] = ('<abbr id ="'+str(child.SND_ASSEMBLY_ID)+'" title="' + str(child.SND_ASSEMBLY_ID) + '">' + str(child.SND_ASSEMBLY_ID) + "</abbr>")
			chld_dict["EQUIPMENTTYPE_ID"] = ('<abbr id ="" title="' + str(child.EQUIPMENTTYPE_ID) + '">' + str(child.EQUIPMENTTYPE_ID) + "</abbr>")
			chld_dict["SND_ASSEMBLY_DESCRIPTION"] = ('<abbr id ="" title="' + str(child.SND_ASSEMBLY_DESCRIPTION) + '">' + str(child.SND_ASSEMBLY_DESCRIPTION) + "</abbr>")
			chld_dict["GOT_CODE"] = ('<abbr id ="" title="' + str(child.GOT_CODE) + '">' + str(child.GOT_CODE) + "</abbr>")
			# chld_dict["MNT_PLANT_ID"] = ('<abbr id ="" title="' + str(child.MNT_PLANT_ID) + '">' + str(child.MNT_PLANT_ID) + "</abbr>")
			chld_dict["SNDFBL_ID"] = ('<abbr id ="" title="' + str(child.SNDFBL_ID) + '">' + str(child.SNDFBL_ID) + "</abbr>")
			chld_dict["GREENBOOK"] = ('<abbr id ="" title="' + str(child.GREENBOOK) + '">' + str(child.GREENBOOK) + "</abbr>")
			# chld_dict["WARRANTY_START_DATE"] = ('<abbr id ="" title="' + str(child.WARRANTY_START_DATE) + '">' + str(child.WARRANTY_START_DATE) + "</abbr>")
			# chld_dict["WARRANTY_END_DATE"] = ('<abbr id ="" title="' + str(child.WARRANTY_END_DATE) + '">' + str(child.WARRANTY_END_DATE) + "</abbr>")
			chld_list.append(chld_dict)

	# Table formation.
	hyper_link = ["QUOTE_SERVICE_SENDING_FAB_EQUIP_ASS_ID"]
	table_header += "<tr>"
	table_header += (
		'<th data-field="ACTIONS"><div class="action_col">ACTIONS</div><button class="searched_button" id="Act_'
		+ str(table_id)
		+ '">Search</button></th>'
	)
	table_header += '<th data-field="SELECT" class="wid45" data-checkbox="true"></th>'
	for key, invs in enumerate(list(Columns)):
		invs = str(invs).strip()
		qstring = attr_list.get(str(invs)) or ""
		if qstring == "":
			qstring = invs.replace("_", " ")
		if checkbox_list is not None and invs in checkbox_list:
			table_header += (
				'<th data-field="'
				+ str(invs)
				+ '" data-filter-control="input" data-align="center" data-formatter="CheckboxFieldRelatedList" data-sortable="true"><abbr title="'
				+ str(qstring)
				+ '">'
				+ str(qstring)
				+ "</abbr></th>"
			)
		elif hyper_link is not None and invs in hyper_link:
			table_header += (
				'<th data-field="'
				+ str(invs)
				+ '" data-filter-control="input" data-formatter="sendingequipmentchildHyperLink" data-sortable="true"><abbr class ="hyperlink" title="'
				+ str(qstring)
				+ '">'
				+ str(qstring)
				+ "</abbr></th>"
			)
		else:
			table_header += (
				'<th data-field="'
				+ str(invs)
				+ '" data-filter-control="input" data-sortable="true"><abbr title="'
				+ str(qstring)
				+ '">'
				+ str(qstring)
				+ "</abbr></th>"
			)
	table_header += "</tr>"
	table_header += '</thead><tbody onclick="Table_Onclick_Scroll(this)"></tbody></table>'
	table_ids = "#" + str(table_id)
	filter_control_function = ""
	tbl_id = table_id
	values_list = ""
	for key, invs in enumerate(list(Columns)):
		table_ids = "#" + str(table_id)
		filter_clas = "#" + str(table_id) + " .bootstrap-table-filter-control-" + str(invs)
		values_list += "var " + str(invs) + ' = $("' + str(filter_clas) + '").val(); '
		values_list += "ATTRIBUTE_VALUEList.push(" + str(invs) + "); "
	filter_class = "#Act_" + str(table_id)
	filter_control_function += (
		'$("'
		+ filter_class
		+ '").click( function(){ var table_id = $(this).closest("table").attr("id"); ATTRIBUTE_VALUEList = []; '
		+ str(values_list)
		+ ' var attribute_value = $(this).val(); cpq.server.executeScript("CQNESTGRID", {"TABNAME":"Sending Equipment child", "ACTION":"PRODUCT_ONLOAD_FILTER", "ATTRIBUTE_NAME": '
		+ str(list(Columns))
		+ ', "ATTRIBUTE_VALUE": ATTRIBUTE_VALUEList, "REC_ID":"'
		+ str(recid)
		+ '" }, function(dataset) { data2 = dataset[1];  data1 = dataset[0]; data3 = dataset[2]; console.log("len ---->"+data1);console.log("localStorage---", localStorage.getItem("Assembly_edit_mode") );if(localStorage.getItem("Assembly_edit_mode") == "True"){SendEqupAssemblyEdit()};  try { if(data1.length > 0) { $("#'+ str(tbl_id) + '").bootstrapTable("load", data1 );$("#noRecDisp").remove(); if (document.getElementById("'+str(tbl_id) + '___totalItemCount")){document.getElementById("'+str(tbl_id)+ '___totalItemCount").innerHTML = data2;}  if (document.getElementById("'+str(tbl_id) + '___NumberofItem")) {document.getElementById("'+str(tbl_id)+ '___NumberofItem").innerHTML = data3;}} else{ $("#' + str(tbl_id) + '").bootstrapTable("load", data1  );$("#' + str(tbl_id) + '").after("<div id=\'noRecDisp\' class=\'noRecord\'>No Records to Display</div>"); $(".noRecord:not(:first)").remove(); if (document.getElementById("'+str(tbl_id) + '___totalItemCount")){document.getElementById("'+str(tbl_id)+ '___totalItemCount").innerHTML = data2;}  if (document.getElementById("'+str(tbl_id) + '___NumberofItem")) {document.getElementById("'+str(tbl_id)+ '___NumberofItem").innerHTML = data3;} }} catch(err){} }); filter_search_click();$(".JColResizer").mousedown(function(){ $("thead.fullHeadFirst").css("cssText","z-index: 2;border-top: 1px solid rgb(220, 220, 220);top: 154px;border-right: 0px !important;");$("thead.fullHeadSecond").css("display","none"); });$(".JColResizer").mouseup(function(){ var th_width_resize = [];$("#table_equipment_child thead.fullHeadFirst tr th").each(function(index){var wid = $(this).css("width"); if(index ==0 || index ==1){th_width_resize.push("60px");}else{th_width_resize.push(wid);}}); $("thead.fullHeadFirst").css("cssText","position: fixed;z-index: 2;border-top: 1px solid rgb(220, 220, 220); top: 154px;border-right: 0px !important;");$("thead.fullHeadSecond").css("display","table-header-group");$("#table_equipment_child thead.fullHeadFirst tr th").each(function(index){var num = th_width_resize[index].split("px");var numsp = parseInt(num[0]);numsp = numsp - 1;var make_str =numsp+"px"; var c = "width:"+make_str+";white-space: nowrap;overflow: hidden;text-overflow: ellipsis;";var d = "width:"+make_str+";"; $(this).css("cssText",c);$(this).children("div:first-child").css("cssText",c);$(this).children("div.fht-cell").css("cssText",d);});$("#table_equipment_child thead.fullHeadSecond tr th").each(function(index){var num = th_width_resize[index].split("px");var numsp = parseInt(num[0]);numsp = numsp - 1;var make_str =numsp+"px"; var c = "width:"+make_str+";white-space: nowrap;overflow: hidden;text-overflow: ellipsis;";var d = "width:"+make_str+";"; $(this).css("cssText",c);$(this).children("div:first-child").css("cssText",c);$(this).children("div.fht-cell").css("cssText",d);}); });});'
	)
	#Trace.Write("969696 filter_control_function --->"+str(filter_control_function))
	dbl_clk_function = (
		'$("'
		+ str(table_ids)
		+ '").on("all.bs.table", function (e, name, args) { $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); }); $("'
		+ str(table_ids)
		+ '\ th.bs-checkbox div.th-inner").before("<div style=\'padding:0; border-bottom: 1px solid #dcdcdc;\'>SELECT</div>"); $(".bs-checkbox input").addClass("custom"); $("'
		+ str(table_ids)
		+ "\").on('sort.bs.table', function (e, name, order) { console.log('sort.bs.table ============>', e); e.stopPropagation(); currenttab = $(\"ul#carttabs_head .active\").text().trim(); localStorage.setItem('"
		+ str(table_id)
		+ "_SortColumn', name); localStorage.setItem('"
		+ str(table_id)
		+ "_SortColumnOrder', order); NestedContainerSorting(name, order, '"
		+ str(table_id)
		+ "'); }); "
		)
	#Trace.Write("4444 dbl_clk_function --->"+str(dbl_clk_function))
	NORECORDS = ""
	if len(chld_list) == 0:
		NORECORDS = "NORECORDS"

	ObjectName = "SAQSSA"
	DropDownList = []
	filter_level_list = []
	filter_clas_name = ""
	cv_list = []
	TableclassName = "form-control" + table_id
	for key, col_name in enumerate(list(Columns)):
		StringValue_list = []
		objss_obj = Sql.GetFirst(
			"SELECT API_NAME, DATA_TYPE, FORMULA_LOGIC FROM SYOBJD (NOLOCK) WHERE OBJECT_NAME='"
			+ str(ObjectName)
			+ "' and API_NAME = '"
			+ str(col_name)
			+ "'"
		)
		try:
			FORMULA_LOGIC = objss_obj.FORMULA_LOGIC.strip()
			FORMULA_col = FORMULA_LOGIC.split(" ")[1].strip()
			FORMULA_table = FORMULA_LOGIC.split(" ")[3].strip()
			ins_obj = Sql.GetFirst(
				"SELECT API_NAME, DATA_TYPE,PICKLIST FROM SYOBJD (NOLOCK) WHERE OBJECT_NAME='"
				+ str(FORMULA_table)
				+ "' and API_NAME = '"
				+ str(FORMULA_col)
				+ "'"
			)
			if str(objss_obj.PICKLIST).upper() == "TRUE":
				filter_level_data = "select"
				filter_clas_name = (
					'<div id = "'
					+ str(table_id)
					+ "_RelatedMutipleCheckBoxDrop_"
					+ str(key)
					+ '" class="form-control bootstrap-table-filter-control-'
					+ str(col_name)
					+ " RelatedMutipleCheckBoxDrop_"
					+ str(key)
					+ ' "></div>'
				)
				filter_level_list.append(filter_level_data)
			else:
				filter_level_data = "input"
				filter_clas_name = (
					'<input type="text" class="width100_vis form-control bootstrap-table-filter-control-'
					+ str(col_name)
					+ '">'
				)
				filter_level_list.append(filter_level_data)
		except:
			"""if str(objss_obj.PICKLIST).upper() == "TRUE":
				filter_level_data = "select"
				filter_clas_name = (
					'<div id = "'
					+ str(table_id)
					+ "_RelatedMutipleCheckBoxDrop_"
					+ str(key)
					+ '" class="form-control bootstrap-table-filter-control-'
					+ str(col_name)
					+ " RelatedMutipleCheckBoxDrop_"
					+ str(key)
					+ ' "></div>'
				)
				filter_level_list.append(filter_level_data)"""

			filter_level_data = "input"
			filter_clas_name = (
				'<input type="text" class="width100_vis form-control bootstrap-table-filter-control-' + str(col_name) + '">'
			)
			filter_level_list.append(filter_level_data)
		cv_list.append(filter_clas_name)
		if filter_level_data == "select":
			try:
				xcd = Sql.GetFirst(
					"SELECT (STUFF((SELECT DISTINCT ', ' + CAST("
					+ str(col_name)
					+ " AS CHAR(100)) FROM "
					+ str(ObjectName)
					+ " (NOLOCK) where QUOTE_FAB_LOC_COV_OBJ_ASSEMBLY_RECORD_ID = '"
					+ str(recid)
					+ "' FOR XML PATH('') ), 1, 2, '')  ) AS StringValue"
				)
			except:
				xcd = Sql.GetFirst(
					"SELECT (STUFF((SELECT DISTINCT ', ' + CAST("
					+ str(col_name)
					+ " AS CHAR(100)) FROM "
					+ str(ObjectName)
					+ " (NOLOCK) FOR XML PATH('') ), 1, 2, '')  ) AS StringValue"
				)
			if str(xcd.StringValue) is not None and str(xcd.StringValue) != "":
				if str(xcd.StringValue).find(",") != -1:
					StringValue_list = [ins.strip() for ins in str(xcd.StringValue).split(",") if ins.strip() != ""]
				else:
					StringValue_list.append(str(xcd.StringValue))
			else:
				StringValue_list = [""]
			StringValue_list = list(set(StringValue_list))
			DropDownList.append(StringValue_list)
		elif filter_level_data == "checkbox":
			DropDownList.append(["True", "False"])
		else:
			DropDownList.append("")
	RelatedDrop_str = (
		"try { if( document.getElementById('"
		+ str(table_id)
		+ "') ) { var listws = document.getElementById('"
		+ str(table_id)
		+ "').getElementsByClassName('filter-control');  for (i = 0; i < listws.length; i++) { document.getElementById('"
		+ str(table_id)
		+ "').getElementsByClassName('filter-control')[i].innerHTML = datachld6[i];  } for (j = 0; j < listws.length; j++) { if (datachld7[j] == 'select') { if (data8[j]) { var dataAdapter = new $.jqx.dataAdapter(datachld8[j]); $('#"
		+ str(table_id)
		+ "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter, autoDropDownHeight: true }); } } } } }  catch(err) { setTimeout(function() { var listws = document.getElementById('"
		+ str(table_id)
		+ "').getElementsByClassName('filter-control');  for (i = 0; i < listws.length; i++) { document.getElementById('"
		+ str(table_id)
		+ "').getElementsByClassName('filter-control')[i].innerHTML = datachld6[i];  } for (j = 0; j < listws.length; j++) { if (datachld7[j] == 'select') { if (data8[j]) { var dataAdapter = new $.jqx.dataAdapter(datachld8[j]); $('#"
		+ str(table_id)
		+ "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter, autoDropDownHeight: true }); } } } }, 5000); } try { setTimeout(function(){ $('#"
		+ str(table_id)
		+ "').colResizable({ resizeMode:'overflow'}); }, 3000); } catch(err){}"
	)
	page = ""
	if QueryCount < int(PerPage):
		page = str(Page_start) + " - " + str(QueryCount)
	else:
		page = str(Page_start) + " - " + str(Page_End)
	Test = (
		'<div class="col-md-12 brdr listContStyle pad2height30" ><div class="col-md-4 pager-numberofitem clear-padding"><span class="pager-number-of-items-item noofitem"  id="'
		+ str(table_id)
		+ '___NumberofItem" >'
		+ str(page)
		+ ' of </span><span class="pager-number-of-items-item fltltpad2mrg0" id="'
		+ str(table_id)
		+ '___totalItemCount"  >'
		+ str(QueryCount)
		+ '</span><div class="clear-padding fltltmrgtp3" ><div  class="pull-right vertmidtxtrht"><select onchange="PageFunctestChild(this,\'Quote\',\'\',\''
		+str(table_id)
		+'\')" id="'
		+ str(table_id)
		+ '___PageCountValue"  class="form-control wid65vermiddisinbmarl5"><option value="10" selected>10</option><option value="20">20</option><option value="50">50</option><option value="100">100</option><option value="200">200</option></select> </div></div></div><div class="col-xs-8 col-md-4  clear-padding disinpad10txtcen"  data-bind="visible: totalItemCount"><div class="clear-padding col-xs-12 col-sm-6 col-md-12 bor0" ><ul class="pagination pagination"><li class="disabled"><a href="#" onclick="FirstPageLoad_paginationChild(\'Quote\',\'\',\''
		+str(table_id)
		+'\')"><i class="fa fa-caret-left font14whtbld" ></i><i class="fa fa-caret-left font14" ></i></a></li><li class="disabled"><a href="#" onclick="Previous12334Child(\'Quote\',\'\',\''
		+str(table_id)
		+'\')"><i class="fa fa-caret-left font14" ></i>PREVIOUS</a></li><li class="disabled"><a href="#" class="disabledPage" onclick="Next12334Child(\'Quote\',\'\',\''
		+str(table_id)
		+'\')">NEXT<i class="fa fa-caret-right font14" ></i></a></li><li class="disabled"><a href="#" onclick="LastPageLoad_paginationChild(\'Quote\',\'\',\''
		+str(table_id)
		+'\')" class="disabledPage"><i class="fa fa-caret-right font14"></i><i class="fa fa-caret-right font14whtbld"></i></a></li></ul></div> </div> <div class="col-md-4 pr_page_pad"> <span id="'
		+ str(table_id)
		+ '___page_count"  class="currentPage page_right_content">1</span><span class="page_right_content pad_rt_2">Page </span></div></div>'
	)

	if QueryCount < int(PerPage):
		PerPage = str(QueryCount)
	else:
		PerPage = str(PerPage)   
	if Page_End > QueryCount:
		Page_End = QueryCount
	else:
		Page_End = Page_End
	# Trace.Write("Page_start----->"+str(Page_start))     
	# Trace.Write("Page_End----->"+str(Page_End))    
	Action_Str = ""
	Action_Str += str(Page_start)+" - "
	Action_Str += str(Page_End)
	Action_Str += " of"

	return (
		table_header,
		chld_list,
		table_id,
		filter_control_function,
		NORECORDS,
		dbl_clk_function,
		cv_list,
		filter_level_list,
		DropDownList,
		RelatedDrop_str,
		Test,
		Action_Str,
		edit_button
	)

def GetEquipmentMasterFilter(ATTRIBUTE_NAME, ATTRIBUTE_VALUE,PerPage,PageInform):
	
	if str(PerPage) == "" and str(PageInform) == "":
		Page_start = 1
		Page_End = 10
		PerPage = 10
		PageInform = "1___10___10"
	else:
		Page_start = int(PageInform.split("___")[0])
		Page_End = int(PageInform.split("___")[1])
		PerPage = PerPage
	QueryCount = ""
	TreeParam = Product.GetGlobal("TreeParam")
	TreeParentParam = Product.GetGlobal("TreeParentLevel0")
	TreeSuperParentParam = Product.GetGlobal("TreeParentLevel1")
	TreeTopSuperParentParam =  Product.GetGlobal("TreeParentLevel2")
	FablocationId = Product.GetGlobal("TreeParam")
	ContractRecordId = Quote.GetGlobal("contract_quote_record_id")
	RevisionRecordId = Quote.GetGlobal("quote_revision_record_id")
	ATTRIBUTE_VALUE_STR = ""
	Dict_formation = dict(zip(ATTRIBUTE_NAME, ATTRIBUTE_VALUE))
	for quer_key, quer_value in enumerate(Dict_formation):
		x_picklistcheckobj = Sql.GetFirst(
			"SELECT PICKLIST FROM SYOBJD (NOLOCK) WHERE OBJECT_NAME ='SAQFEQ' AND API_NAME = '" + str(quer_value) + "'"
		)
		x_picklistcheck = str(x_picklistcheckobj.PICKLIST).upper()
		if Dict_formation.get(quer_value) != "":
			quer_values = str(Dict_formation.get(quer_value)).strip()
			if str(quer_values).upper() == "TRUE":
				quer_values = "TRUE"
			elif str(quer_values).upper() == "FALSE":
				quer_values = "FALSE"
			if str(quer_values).find(",") == -1:
				if x_picklistcheck == "TRUE":
					ATTRIBUTE_VALUE_STR += str(quer_value) + " = '" + str(quer_values) + "' and "
				else:
					ATTRIBUTE_VALUE_STR += str(quer_value) + " like '%" + str(quer_values) + "%' and "
			else:
				quer_values = quer_values.split(",")
				quer_values = tuple(list(quer_values))
				ATTRIBUTE_VALUE_STR += str(quer_value) + " in " + str(quer_values) + " and "
			if str(quer_value) == 'QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID':                
				if str(str(quer_values)).find("-") == -1:                            
					ATTRIBUTE_VALUE_STR = (" CpqTableEntryId = '"+ str(quer_values)+ "' and ")                            
				else:
					xa_str = str(quer_values).split("-")[1]                            
					ATTRIBUTE_VALUE_STR = (" CpqTableEntryId = '"+ str(xa_str)+ "' and ")    

	data_list = []
	rec_id = "SYOBJ_00937"
	obj_id = "SYOBJ-00937"
	objh_getid = Sql.GetFirst(
		"SELECT TOP 1  RECORD_ID  FROM SYOBJH (NOLOCK) WHERE SAPCPQ_ATTRIBUTE_NAME='" + str(obj_id) + "'"
	)
	if objh_getid:
		obj_id = objh_getid.RECORD_ID
	objs_obj = Sql.GetFirst(
		"select CAN_ADD,CAN_EDIT,COLUMNS,CAN_DELETE from SYOBJR (NOLOCK) where OBJ_REC_ID = '" + str(obj_id) + "' "
	)
	can_edit = str(objs_obj.CAN_EDIT)
	can_clone = str(objs_obj.CAN_ADD)
	can_delete = str(objs_obj.CAN_DELETE)

	emptysearch_flag = 0
	conditionsearch_falg = 0

	orderby = ""
	if SortColumn != '' and SortColumnOrder !='':
		orderby = SortColumn + " " + SortColumnOrder
	else:
		orderby = "QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID"
	if ATTRIBUTE_VALUE is None or ATTRIBUTE_VALUE == "" or ATTRIBUTE_VALUE_STR is None or ATTRIBUTE_VALUE_STR == "":
		#Trace.Write("Empty search ")
		emptysearch_flag = 1
		if TreeParam == 'Fab Locations':
			parent_obj = Sql.GetList(
			"select top "+str(PerPage)+" QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID,SALESORG_ID,EQUIPMENTCATEGORY_ID,EQUIPMENT_ID,MNT_PLANT_ID,CUSTOMER_TOOL_ID,SERIAL_NUMBER,GREENBOOK,QUOTE_NAME,SALESORG_NAME,EQUIPMENT_DESCRIPTION,EQUIPMENT_STATUS,PLATFORM,FABLOCATION_ID,WARRANTY_START_DATE,QUOTE_ID,FABLOCATION_NAME,WARRANTY_END_DATE from SAQFEQ (NOLOCK) where QUOTE_RECORD_ID = '"
			+ str(ContractRecordId)
			+ "' AND QTEREV_RECORD_ID = '{}' ".format(str(Quote.GetGlobal("quote_revision_record_id")))
			+ " ORDER BY "
			+ str(orderby)
			)
			Count = Sql.GetFirst("select count(CpqTableEntryId) as cnt from SAQFEQ (NOLOCK) where QUOTE_RECORD_ID = '"
			+ str(ContractRecordId)
			+ "' AND QTEREV_RECORD_ID = '{}' ".format(str(Quote.GetGlobal("quote_revision_record_id")))
			+ "'")
			if Count:
				QueryCount = Count.cnt
		else:
			if (("Sending Account -" in TreeParam) or ("Receiving Account -" in TreeParam)) and TreeParentParam == 'Fab Locations':
				account_id = TreeParam.split(' - ')
				account_id = account_id[len(account_id)-1]
				fab_type = 'SENDING FAB' if "Sending Account -" in TreeParam else 'RECEIVING FAB' if "Receiving Account -" in TreeParam else ""
				get_fab_query = Sql.GetList("SELECT FABLOCATION_ID FROM SAQFBL WHERE QUOTE_RECORD_ID = '{}' and QTEREV_RECORD_ID = '{}' and ACCOUNT_ID = '{}' and RELOCATION_FAB_TYPE = '{}'".format(ContractRecordId,RevisionRecordId,account_id,fab_type) )
				if get_fab_query:
					get_fab = "in "+ str(tuple([fab.FABLOCATION_ID for fab in get_fab_query])).replace(",)",')')
				else:
					get_fab = "= ''"
				parent_obj = Sql.GetList(
					"select top "+str(PerPage)+" QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID,SALESORG_ID,EQUIPMENTCATEGORY_ID,EQUIPMENT_ID,MNT_PLANT_ID,CUSTOMER_TOOL_ID,SERIAL_NUMBER,GREENBOOK,QUOTE_NAME,SALESORG_NAME,EQUIPMENT_DESCRIPTION,EQUIPMENT_STATUS,PLATFORM,FABLOCATION_ID,WARRANTY_START_DATE,QUOTE_ID,FABLOCATION_NAME,WARRANTY_END_DATE from SAQFEQ (NOLOCK) where QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' and FABLOCATION_ID {get_fab} and RELOCATION_EQUIPMENT_TYPE = '{equp_type}' ORDER BY {orderby}".format(orderby = orderby, ContractRecordId = ContractRecordId,RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"), get_fab = get_fab,equp_type = 'SENDING EQUIPMENT' if "Sending Account -" in TreeParam else "RECEIVING EQUIPMENT" if "Receiving Account -" in TreeParam else "")
				)
				Count = Sql.GetFirst("select count(CpqTableEntryId) as cnt from SAQFEQ (NOLOCK) where QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' and FABLOCATION_ID  {get_fab} and RELOCATION_EQUIPMENT_TYPE = '{equp_type}'".format(ContractRecordId = ContractRecordId,RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"), get_fab = get_fab,equp_type = 'SENDING EQUIPMENT' if "Sending Account -" in TreeParam else "RECEIVING EQUIPMENT" if "Receiving Account -" in TreeParam else "")
				)
				if Count:
					QueryCount = Count.cnt
			elif (("Sending Account -" in TreeParentParam) or ("Receiving Account -" in TreeParentParam)) and TreeSuperParentParam == 'Fab Locations':
				parent_obj = Sql.GetList(
					"select top {PerPage} QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID,SALESORG_ID,EQUIPMENTCATEGORY_ID,EQUIPMENT_ID,MNT_PLANT_ID,CUSTOMER_TOOL_ID,SERIAL_NUMBER,GREENBOOK,QUOTE_NAME,SALESORG_NAME,EQUIPMENT_DESCRIPTION,EQUIPMENT_STATUS,PLATFORM,FABLOCATION_ID,WARRANTY_START_DATE,QUOTE_ID,FABLOCATION_NAME,WARRANTY_END_DATE from SAQFEQ (NOLOCK) where QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' and FABLOCATION_ID = '{TreeParam}' and RELOCATION_EQUIPMENT_TYPE = '{equp_type}' ORDER BY {orderby}".format(PerPage=str(PerPage),ContractRecordId=str(ContractRecordId),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"),TreeParam=str(TreeParam),equp_type = 'SENDING EQUIPMENT' if "Sending Account -" in TreeParentParam else "RECEIVING EQUIPMENT" if "Receiving Account -" in TreeParentParam else "",orderby=str(orderby))
				)
				Count = Sql.GetFirst("select count(CpqTableEntryId) as cnt from SAQFEQ (NOLOCK) where QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}'  and FABLOCATION_ID = '{TreeParam}' and RELOCATION_EQUIPMENT_TYPE = '{equp_type}' ".format(PerPage=str(PerPage),ContractRecordId=str(ContractRecordId),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"),TreeParam=str(TreeParam),equp_type = 'SENDING EQUIPMENT' if "Sending Account -" in TreeParentParam else "RECEIVING EQUIPMENT" if "Receiving Account -" in TreeParentParam else ""))
				if Count:
					QueryCount = Count.cnt
			elif (("Sending Account -" in TreeSuperParentParam) or ("Receiving Account -" in TreeSuperParentParam)) and TreeTopSuperParentParam == 'Fab Locations':
				equp_type =""
				if "Sending Account -" in TreeSuperParentParam:
					equp_type ="SENDING EQUIPMENT"
				elif "Receiving Account -" in TreeSuperParentParam:
					equp_type ="RECEIVING EQUIPMENT"
				parent_obj = Sql.GetList(
					"select top "+str(PerPage)+" QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID,SALESORG_ID,EQUIPMENTCATEGORY_ID,EQUIPMENT_ID,MNT_PLANT_ID,CUSTOMER_TOOL_ID,SERIAL_NUMBER,GREENBOOK,QUOTE_NAME,SALESORG_NAME,EQUIPMENT_DESCRIPTION,EQUIPMENT_STATUS,PLATFORM,FABLOCATION_ID,WARRANTY_START_DATE,QUOTE_ID,FABLOCATION_NAME,WARRANTY_END_DATE from SAQFEQ (NOLOCK) where QUOTE_RECORD_ID = '"
					+ str(ContractRecordId)
					+ "' and QTEREV_RECORD_ID = '"
					+ str(RevisionRecordId)
					+ "' and FABLOCATION_ID = '"
					+ str(TreeParentParam)
					+ "' AND GREENBOOK = '"
					+ str(TreeParam)
					+ "' AND RELOCATION_EQUIPMENT_TYPE = '"+str(equp_type)+"' ORDER BY "
					+ str(orderby)
				)
				Count = Sql.GetFirst("select count(CpqTableEntryId) as cnt from SAQFEQ (NOLOCK) where QUOTE_RECORD_ID = '"+ str(ContractRecordId)+ "' and QTEREV_RECORD_ID = '"+ str(RevisionRecordId)+ "' and FABLOCATION_ID = '" + str(TreeParentParam) + "' AND GREENBOOK = '" + str(TreeParam) + "' AND RELOCATION_EQUIPMENT_TYPE = '"+str(equp_type)+"' ")
				if Count:
					QueryCount = Count.cnt
			else:
				# if TreeParentParam == 'Sending Equipment' or TreeParentParam == 'Receiving equipment':
				#     parent_obj = Sql.GetList(
				#     "select top "+str(PerPage)+" QUOTE_SERVICE_SENDING_FAB_LOC_EQUIP_ID,SALESORG_ID,EQUIPMENTCATEGORY_ID,SND_EQUIPMENT_ID,MNT_PLANT_ID,GREENBOOK,QUOTE_NAME,SALESORG_NAME,SND_EQUIPMENT_DESCRIPTION,EQUIPMENT_STATUS,PLATFORM,SNDFBL_ID,QUOTE_ID,SNDFBL_NAME from SAQSSE (NOLOCK) where QUOTE_RECORD_ID = '"
				#     + str(ContractRecordId)
				#     + "' and SNDFBL_ID = '"
				#     + str(TreeParam)
				#     + "' ORDER BY "
				#     + str(orderby)
				#     )
				#     Count = Sql.GetFirst("select count(CpqTableEntryId) as cnt from SAQSSE (NOLOCK) where QUOTE_RECORD_ID = '"+ str(ContractRecordId)+ "'and SNDFBL_ID = '" + str(TreeParam) + "'")
				#     if Count:
				#         QueryCount = Count.cnt
				if str(TreeParentParam)=="Fab Locations":             
					parent_obj = Sql.GetList(
						"select top "+str(PerPage)+" QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID,SALESORG_ID,EQUIPMENTCATEGORY_ID,EQUIPMENT_ID,MNT_PLANT_ID,CUSTOMER_TOOL_ID,SERIAL_NUMBER,GREENBOOK,QUOTE_NAME,SALESORG_NAME,EQUIPMENT_DESCRIPTION,EQUIPMENT_STATUS,PLATFORM,FABLOCATION_ID,WARRANTY_START_DATE,QUOTE_ID,FABLOCATION_NAME,WARRANTY_END_DATE from SAQFEQ (NOLOCK) where QUOTE_RECORD_ID = '"
						+ str(ContractRecordId)
						+ "'and QTEREV_RECORD_ID = '"
						+ str(RevisionRecordId)
						+ "' and FABLOCATION_ID = '"
						+ str(TreeParam)
						+ "' ORDER BY "
						+ str(orderby)
					)
					Count = Sql.GetFirst("select count(CpqTableEntryId) as cnt from SAQFEQ (NOLOCK) where QUOTE_RECORD_ID = '"+ str(ContractRecordId)+ "' and QTEREV_RECORD_ID = '"+ str(RevisionRecordId)+ "' and FABLOCATION_ID = '" + str(TreeParam) + "' ")
				else:
					Trace.Write('filter---------')                  
					parent_obj = Sql.GetList(
						"select top "+str(PerPage)+" QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID,SALESORG_ID,EQUIPMENTCATEGORY_ID,EQUIPMENT_ID,MNT_PLANT_ID,CUSTOMER_TOOL_ID,SERIAL_NUMBER,GREENBOOK,QUOTE_NAME,SALESORG_NAME,EQUIPMENT_DESCRIPTION,EQUIPMENT_STATUS,PLATFORM,FABLOCATION_ID,WARRANTY_START_DATE,QUOTE_ID,FABLOCATION_NAME,WARRANTY_END_DATE from SAQFEQ (NOLOCK) where QUOTE_RECORD_ID = '"
						+ str(ContractRecordId)
						+ "' and QTEREV_RECORD_ID = '"
						+ str(RevisionRecordId)
						+ "' and FABLOCATION_ID = '"
						+ str(TreeParentParam)
						+ "' AND GREENBOOK = '"
						+ str(TreeParam)
						+ "' ORDER BY "
						+ str(orderby)
					)
					Count = Sql.GetFirst("select count(CpqTableEntryId) as cnt from SAQFEQ (NOLOCK) where QUOTE_RECORD_ID = '"+ str(ContractRecordId)+ "' and QTEREV_RECORD_ID = '"+ str(RevisionRecordId)+ "' and FABLOCATION_ID = '" + str(TreeParentParam) + "' AND GREENBOOK = '" + str(TreeParam) + "'")
				if Count:
					QueryCount = Count.cnt

	else:
		#Trace.Write("search with condition")
		conditionsearch_falg = 1
		if TreeSuperParentParam == "Fab Locations":
			if "Sending Account -" in TreeParentParam or "Receiving Account -" in TreeParentParam:
				if "Sending Account -" in TreeParentParam:
					equp_type = "SENDING EQUIPMENT"
				elif "Receiving Account -" in TreeParentParam:
					equp_type = "RECEIVING EQUIPMENT"
				parent_obj = Sql.GetList(
					"select top "+str(PerPage)+" QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID,SALESORG_ID,EQUIPMENTCATEGORY_ID,EQUIPMENT_ID,MNT_PLANT_ID,CUSTOMER_TOOL_ID,SERIAL_NUMBER,GREENBOOK,QUOTE_NAME,SALESORG_NAME,EQUIPMENT_DESCRIPTION,EQUIPMENT_STATUS,PLATFORM,FABLOCATION_ID,WARRANTY_START_DATE,QUOTE_ID,FABLOCATION_NAME,WARRANTY_END_DATE from SAQFEQ (NOLOCK) where "
					+ str(ATTRIBUTE_VALUE_STR)
					+ " 1=1 and QUOTE_RECORD_ID = '"
					+ str(ContractRecordId)
					+ "' and QTEREV_RECORD_ID = '"
					+ str(RevisionRecordId)
					+ "' and FABLOCATION_ID = '"
					+ str(TreeParam)
					+ "' and RELOCATION_EQUIPMENT_TYPE = '"+str(equp_type)+"' ORDER BY "
					+ str(orderby)
				)
				Count = Sql.GetFirst("select count(*) as cnt  from SAQFEQ (NOLOCK) where "
					+ str(ATTRIBUTE_VALUE_STR)
					+ " 1=1 and QUOTE_RECORD_ID = '"
					+ str(ContractRecordId)
					+ "' and QTEREV_RECORD_ID = '"
					+ str(RevisionRecordId)
					+ "' and FABLOCATION_ID = '"
					+ str(TreeParam)
					+ "' and RELOCATION_EQUIPMENT_TYPE = '"+str(equp_type)+"' ")
			else:
				parent_obj = Sql.GetList(
					"select top "+str(PerPage)+"  QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID,EQUIPMENTCATEGORY_ID,SERIAL_NUMBER,CUSTOMER_TOOL_ID,GREENBOOK,EQUIPMENT_STATUS,PLATFORM,MNT_PLANT_ID,EQUIPMENT_ID,EQUIPMENT_DESCRIPTION,FABLOCATION_ID,FABLOCATION_NAME,QUOTE_ID,QUOTE_NAME,SALESORG_ID,SALESORG_NAME,WARRANTY_START_DATE,WARRANTY_END_DATE,WAFER_SIZE from SAQFEQ (NOLOCK) where "
					+ str(ATTRIBUTE_VALUE_STR)
					+ " 1=1 and QUOTE_RECORD_ID = '"
					+ str(ContractRecordId)
					+ "' and QTEREV_RECORD_ID = '"
					+ str(RevisionRecordId)
					+ "' and GREENBOOK = '"
					+ str(TreeParam)
					+ "' ORDER BY "+ str(orderby) )
					
				Count = Sql.GetFirst("select count(*) as cnt  from SAQFEQ (NOLOCK) where "
					+ str(ATTRIBUTE_VALUE_STR)
					+ " 1=1 and QUOTE_RECORD_ID = '"
					+ str(ContractRecordId)
					+ "' and QTEREV_RECORD_ID = '"
					+ str(RevisionRecordId)
					+ "' and GREENBOOK = '"
					+ str(TreeParam)
					+ "'")
			if Count:
				QueryCount = Count.cnt
				
		else:
			#Trace.Write("2 level conditonal search ---->")
			if (("Sending Account -" in TreeParam) or ("Receiving Account -" in TreeParam)) and TreeParentParam == 'Fab Locations':
				account_id = TreeParam.split(' - ')
				account_id = account_id[len(account_id)-1]
				fab_type = 'SENDING FAB' if "Sending Account -" in TreeParam else 'RECEIVING FAB' if "Receiving Account -" in TreeParam else ""
				get_fab_query = Sql.GetList("SELECT FABLOCATION_ID FROM SAQFBL WHERE QUOTE_RECORD_ID = '{}' and QTEREV_RECORD_ID = '{}' and ACCOUNT_ID = '{}' and RELOCATION_FAB_TYPE = '{}'".format(ContractRecordId,RevisionRecordId,account_id,fab_type) )
				if get_fab_query:
					get_fab = "in "+ str(tuple([fab.FABLOCATION_ID for fab in get_fab_query])).replace(",)",')')
				else:
					get_fab = "= ''"
				parent_obj = Sql.GetList(
					"""select top {PerPage} QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID,SALESORG_ID,EQUIPMENTCATEGORY_ID,EQUIPMENT_ID,MNT_PLANT_ID,CUSTOMER_TOOL_ID,SERIAL_NUMBER,GREENBOOK,QUOTE_NAME,SALESORG_NAME,EQUIPMENT_DESCRIPTION,EQUIPMENT_STATUS,PLATFORM,FABLOCATION_ID,CONVERT(varchar,WARRANTY_START_DATE,101) AS WARRANTY_START_DATE,CONVERT(varchar,WARRANTY_END_DATE,101) WARRANTY_END_DATE,QUOTE_ID,FABLOCATION_NAME from SAQFEQ (NOLOCK) where {ATTRIBUTE_VALUE_STR} QUOTE_RECORD_ID = '{ContractRecordId}'  and QTEREV_RECORD_ID = '{RevisionRecordId}' and FABLOCATION_ID {get_fab}  and RELOCATION_EQUIPMENT_TYPE = '{equp_type}' ORDER BY {orderby} """.format(orderby = orderby, ContractRecordId = ContractRecordId,RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"), get_fab = get_fab,PerPage = PerPage,ATTRIBUTE_VALUE_STR=str(ATTRIBUTE_VALUE_STR) if str(ATTRIBUTE_VALUE_STR) else " ",equp_type = 'SENDING EQUIPMENT' if "Sending Account -" in TreeParam else "RECEIVING EQUIPMENT" if "Receiving Account -" in TreeParam else "" ) )
				Count = Sql.GetFirst(
					"""select count(CpqTableEntryId) as cnt from SAQFEQ (NOLOCK) where {ATTRIBUTE_VALUE_STR} QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' and FABLOCATION_ID  {get_fab} and RELOCATION_EQUIPMENT_TYPE = '{equp_type}'""".format(ATTRIBUTE_VALUE_STR=str(ATTRIBUTE_VALUE_STR) if str(ATTRIBUTE_VALUE_STR) else " ",ContractRecordId = ContractRecordId,RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"),get_fab = get_fab,equp_type = 'SENDING EQUIPMENT' if "Sending Account -" in TreeParam else "RECEIVING EQUIPMENT" if "Receiving Account -" in TreeParam else "" )
				)
				if Count:
					QueryCount = Count.cnt       
			elif (("Sending Account -" in TreeSuperParentParam) or ("Receiving Account -" in TreeSuperParentParam)) and TreeTopSuperParentParam == 'Fab Locations':
				fab_type =""
				if "Sending Account -" in TreeSuperParentParam:
					fab_type = "SENDING EQUIPMENT"
				if "Receiving Account -" in TreeSuperParentParam:
					fab_type = "RECEIVING EQUIPMENT"
				parent_obj = Sql.GetList(
					"select top "+str(PerPage)+"  QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID,EQUIPMENTCATEGORY_ID,SERIAL_NUMBER,CUSTOMER_TOOL_ID,GREENBOOK,EQUIPMENT_STATUS,PLATFORM,MNT_PLANT_ID,EQUIPMENT_ID,EQUIPMENT_DESCRIPTION,FABLOCATION_ID,FABLOCATION_NAME,QUOTE_ID,QUOTE_NAME,SALESORG_ID,SALESORG_NAME,WARRANTY_START_DATE,WARRANTY_END_DATE,WAFER_SIZE from SAQFEQ (NOLOCK) where "
					+ str(ATTRIBUTE_VALUE_STR)
					+ " 1=1 and QUOTE_RECORD_ID = '"
					+ str(ContractRecordId)
					+ "'  and QTEREV_RECORD_ID = '"
					+ str(RevisionRecordId)
					+ "' and FABLOCATION_ID = '"+str(TreeParentParam)+"' AND  RELOCATION_EQUIPMENT_TYPE ='"+str(fab_type)+"' AND GREENBOOK = '"+str(TreeParam)+"' ORDER BY "+ str(orderby)
				)
				Count = Sql.GetFirst("select count(*) as cnt from SAQFEQ (NOLOCK) where "+ str(ATTRIBUTE_VALUE_STR)+ " 1=1 and QUOTE_RECORD_ID = '"+ str(ContractRecordId)+ "' and QTEREV_RECORD_ID = '"
					+ str(RevisionRecordId)
					+ "' AND FABLOCATION_ID = '"+str(TreeParentParam)+"' AND  RELOCATION_EQUIPMENT_TYPE ='"+str(fab_type)+"' AND GREENBOOK = '"+str(TreeParam)+"' ")
				if Count:
					QueryCount = Count.cnt
			# elif TreeParentParam == 'Sending Equipment' or TreeParentParam == 'Receiving equipment':
			#     parent_obj = Sql.GetList(
			#         "select top "+str(PerPage)+" QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID,SALESORG_ID,EQUIPMENTCATEGORY_ID,EQUIPMENT_ID,MNT_PLANT_ID,CUSTOMER_TOOL_ID,SERIAL_NUMBER,GREENBOOK,QUOTE_NAME,SALESORG_NAME,EQUIPMENT_DESCRIPTION,EQUIPMENT_STATUS,PLATFORM,FABLOCATION_ID,WARRANTY_START_DATE,QUOTE_ID,FABLOCATION_NAME,WARRANTY_END_DATE from SAQFEQ (NOLOCK) where "
			#         + str(ATTRIBUTE_VALUE_STR)
			#         + " 1=1 and QUOTE_RECORD_ID = '"
			#         + str(ContractRecordId)
			#         + "' and FABLOCATION_ID = '"
			#         + str(TreeParam)
			#         + "' ORDER BY "
			#         + str(orderby)
			#     )
			#     Count = Sql.GetFirst("select count(*) as cnt  from SAQFEQ (NOLOCK) where "
			#         + str(ATTRIBUTE_VALUE_STR)
			#         + " 1=1 and QUOTE_RECORD_ID = '"
			#         + str(ContractRecordId)
			#         + "' and FABLOCATION_ID = '"
			#         + str(TreeParam)
			#         + "'")
			#     if Count:
			#         QueryCount = Count.cnt
			# elif TreeSuperParentParam == 'Sending Equipment' or TreeSuperParentParam == 'Receiving equipment':
			#     Trace.Write('teee========')
			#     parent_obj = Sql.GetList(
			#         "select top "+str(PerPage)+" QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID,SALESORG_ID,EQUIPMENTCATEGORY_ID,EQUIPMENT_ID,MNT_PLANT_ID,CUSTOMER_TOOL_ID,SERIAL_NUMBER,GREENBOOK,QUOTE_NAME,SALESORG_NAME,EQUIPMENT_DESCRIPTION,EQUIPMENT_STATUS,PLATFORM,FABLOCATION_ID,WARRANTY_START_DATE,QUOTE_ID,FABLOCATION_NAME,WARRANTY_END_DATE from SAQFEQ (NOLOCK) where "
			#         + str(ATTRIBUTE_VALUE_STR)
			#         + " 1=1 and QUOTE_RECORD_ID = '"
			#         + str(ContractRecordId)
			#         + "' and FABLOCATION_ID = '"
			#         + str(TreeParentParam)
			#         + "'  and GREENBOOK = '"
			#         + str(TreeParam)
			#         + "' ORDER BY "
			#         + str(orderby)
			#     )
			#     Count = Sql.GetFirst("select count(*) as cnt  from SAQFEQ (NOLOCK) where "
			#         + str(ATTRIBUTE_VALUE_STR)
			#         + " 1=1 and QUOTE_RECORD_ID = '"
			#         + str(ContractRecordId)
			#         + "' and FABLOCATION_ID = '"
			#         + str(TreeParentParam)
			#         + "'  and GREENBOOK = '"
			#         + str(TreeParam)
			#         + "'")
			#     if Count:
			#         QueryCount = Count.cnt    
			elif str(TreeParentParam)=="Fab Locations":
				parent_obj = Sql.GetList(
					"select top "+str(PerPage)+"  QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID,EQUIPMENTCATEGORY_ID,SERIAL_NUMBER,CUSTOMER_TOOL_ID,GREENBOOK,EQUIPMENT_STATUS,PLATFORM,MNT_PLANT_ID,EQUIPMENT_ID,EQUIPMENT_DESCRIPTION,FABLOCATION_ID,FABLOCATION_NAME,QUOTE_ID,QUOTE_NAME,SALESORG_ID,SALESORG_NAME,WARRANTY_START_DATE,WARRANTY_END_DATE,WAFER_SIZE from SAQFEQ (NOLOCK) where "
					+ str(ATTRIBUTE_VALUE_STR)
					+ " 1=1 and QUOTE_RECORD_ID = '"
					+ str(ContractRecordId)
					+ "' and QTEREV_RECORD_ID = '"
					+ str(RevisionRecordId)
					+ "' AND FABLOCATION_ID = '"+str(TreeParam)+"' ORDER BY "+ str(orderby)
				)
				Count = Sql.GetFirst("select count(*) as cnt from SAQFEQ (NOLOCK) where "+ str(ATTRIBUTE_VALUE_STR)+ " 1=1 and QUOTE_RECORD_ID = '"+ str(ContractRecordId)+ "' and QTEREV_RECORD_ID = '"+ str(RevisionRecordId)+ "' AND FABLOCATION_ID = '"+str(TreeParam)+"'")
				if Count:
					QueryCount = Count.cnt
			else:
				parent_obj = Sql.GetList(
					"select top "+str(PerPage)+"  QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID,EQUIPMENTCATEGORY_ID,SERIAL_NUMBER,CUSTOMER_TOOL_ID,GREENBOOK,EQUIPMENT_STATUS,PLATFORM,MNT_PLANT_ID,EQUIPMENT_ID,EQUIPMENT_DESCRIPTION,FABLOCATION_ID,FABLOCATION_NAME,QUOTE_ID,QUOTE_NAME,SALESORG_ID,SALESORG_NAME,WARRANTY_START_DATE,WARRANTY_END_DATE,WAFER_SIZE from SAQFEQ (NOLOCK) where "
					+ str(ATTRIBUTE_VALUE_STR)
					+ " 1=1 and QUOTE_RECORD_ID = '"
					+ str(ContractRecordId)
					+ "'  and QTEREV_RECORD_ID = '"
					+ str(RevisionRecordId)
					+ "' ORDER BY "+ str(orderby)
				)
				Count = Sql.GetFirst("select count(*) as cnt from SAQFEQ (NOLOCK) where "+ str(ATTRIBUTE_VALUE_STR)+ " 1=1 and QUOTE_RECORD_ID = '"+ str(ContractRecordId)+ "' and QTEREV_RECORD_ID = '"+ str(RevisionRecordId)+ "'")
				if Count:
					QueryCount = Count.cnt
	for par in parent_obj:
		
		data_dict = {}
		data_id = str(par.QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID)        
		Action_str = (
			'<div class="btn-group dropdown"><div class="dropdown" id="ctr_drop"><i data-toggle="dropdown" id="dropdownMenuButton" class="fa fa-sort-desc dropdown-toggle" aria-expanded="false"></i><ul class="dropdown-menu left" aria-labelledby="dropdownMenuButton"><li><a class="dropdown-item cur_sty" href="#" id="'
			+ str(data_id)
			+ '" onclick="Commonteree_view_RL(this)">VIEW</a></li>'
		)
		if can_edit.upper() == "TRUE":
			Action_str += (
				'<li ><a class="dropdown-item cur_sty" href="#" id="'
				+ str(data_id)
				+ '" onclick="Commonteree_view_RL(this)">EDIT</a></li>'
			)
		if can_delete.upper() == "TRUE":
			Action_str += '<li><a class="dropdown-item" data-target="#cont_viewModal_Material_Delete" data-toggle="modal" onclick="Material_delete_obj(this)" href="#">DELETE</a></li>'
		if can_clone.upper() == "TRUE":
			Action_str += '<li><a class="dropdown-item" data-target="#" data-toggle="modal" onclick="Material_clone_obj(this)" href="#">CLONE</a></li>'

		Action_str += "</ul></div></div>"
		data_dict["ids"] = str(data_id)
		data_dict["ACTIONS"] = str(Action_str)
		data_dict["QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID"] = CPQID.KeyCPQId.GetCPQId("SAQFEQ", str(par.QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID))
		data_dict["EQUIPMENT_ID"] = ('<abbr id ="" title="' + str(par.EQUIPMENT_ID) + '">' + str(par.EQUIPMENT_ID) + "</abbr>") 
		data_dict["PLATFORM"] = ('<abbr id ="" title="' + str(par.PLATFORM) + '">' + str(par.PLATFORM) + "</abbr>")
		data_dict["FABLOCATION_ID"] = ('<abbr id ="" title="' + str(par.FABLOCATION_ID) + '">' + str(par.FABLOCATION_ID) + "</abbr>")
		data_dict["SALESORG_ID"] = ('<abbr id ="" title="' + str(par.SALESORG_ID) + '">' + str(par.SALESORG_ID) + "</abbr>")
		data_dict["EQUIPMENTCATEGORY_ID"] = ('<abbr id ="" title="' + str(par.EQUIPMENTCATEGORY_ID) + '">' + str(par.EQUIPMENTCATEGORY_ID) + "</abbr>")
		data_dict["SERIAL_NUMBER"] = ('<abbr id ="" title="' + str(par.SERIAL_NUMBER) + '">' + str(par.SERIAL_NUMBER) + "</abbr>")
		data_dict["CUSTOMER_TOOL_ID"] = ('<abbr id ="" title="' + str(par.CUSTOMER_TOOL_ID) + '">' + str(par.CUSTOMER_TOOL_ID) + "</abbr>")
		data_dict["GREENBOOK"] = ('<abbr id ="" title="' + str(par.GREENBOOK) + '">' + str(par.GREENBOOK) + "</abbr>")
		data_dict["EQUIPMENT_STATUS"] = ('<abbr id ="" title="' + str(par.EQUIPMENT_STATUS) + '">' + str(par.EQUIPMENT_STATUS) + "</abbr>")
		data_dict["EQUIPMENT_DESCRIPTION"] = ('<abbr id ="" title="' + str(par.EQUIPMENT_DESCRIPTION) + '">' + str(par.EQUIPMENT_DESCRIPTION) + "</abbr>")
		data_dict["FABLOCATION_NAME"] = ('<abbr id ="" title="' + str(par.FABLOCATION_NAME) + '">' + str(par.FABLOCATION_NAME) + "</abbr>")
		data_dict["MNT_PLANT_ID"] = ('<abbr id ="" title="' + str(par.MNT_PLANT_ID) + '">' + str(par.MNT_PLANT_ID) + "</abbr>")
		data_dict["WARRANTY_START_DATE"] = ('<abbr id ="" title="' + str(par.WARRANTY_START_DATE) + '">' + str(par.WARRANTY_START_DATE) + "</abbr>")
		data_dict["WARRANTY_END_DATE"] = ('<abbr id ="" title="' + str(par.WARRANTY_END_DATE) + '">' + str(par.WARRANTY_END_DATE) + "</abbr>")
		data_dict["QUOTE_ID"] = ('<abbr id ="" title="' + str(par.QUOTE_ID) + '">' + str(par.QUOTE_ID) + "</abbr>")
		data_list.append(data_dict)

	page = ""
	if QueryCount == 0:
		page = str(QueryCount) + " - " + str(QueryCount) + " of "
	elif QueryCount < int(PerPage):
		page = str(Page_start) + " - " + str(QueryCount) + " of "
	else:
		page = str(Page_start) + " - " + str(Page_End)+ " of "
	# Trace.Write("6666 QueryCount --->"+str(QueryCount))
	# Trace.Write("6666 page --->"+str(page))

	return data_list,QueryCount,page 

def GetContractEquipmentMasterFilter(ATTRIBUTE_NAME, ATTRIBUTE_VALUE,PerPage,PageInform):

	if str(PerPage) == "" and str(PageInform) == "":
		Page_start = 1
		Page_End = 10
		PerPage = 10
		PageInform = "1___10___10"
	else:
		Page_start = int(PageInform.split("___")[0])
		Page_End = int(PageInform.split("___")[1])
		PerPage = PerPage
	QueryCount = ""

	TreeParam = Product.GetGlobal("TreeParam")
	TreeParentParam = Product.GetGlobal("TreeParentLevel0")
	TreeSuperParentParam = Product.GetGlobal("TreeParentLevel1")
	FablocationId = Product.GetGlobal("TreeParam")
	ContractRecordId = Product.GetGlobal("contract_record_id")
	ATTRIBUTE_VALUE_STR = ""

	orderby = ""
	if SortColumn != '' and SortColumnOrder !='':
		orderby = SortColumn + " " + SortColumnOrder
	else:
		orderby = "CONTRACT_FAB_LOC_GB_EQUIPMENT_RECORD_ID"

	Dict_formation = dict(zip(ATTRIBUTE_NAME, ATTRIBUTE_VALUE))
	for quer_key, quer_value in enumerate(Dict_formation):
		x_picklistcheckobj = Sql.GetFirst(
			"SELECT PICKLIST FROM SYOBJD (NOLOCK) WHERE OBJECT_NAME ='CTCFEQ' AND API_NAME = '" + str(quer_value) + "'"
		)
		x_picklistcheck = str(x_picklistcheckobj.PICKLIST).upper()
		if Dict_formation.get(quer_value) != "":
			quer_values = str(Dict_formation.get(quer_value)).strip()
			if str(quer_values).upper() == "TRUE":
				quer_values = "TRUE"
			elif str(quer_values).upper() == "FALSE":
				quer_values = "FALSE"
			if str(quer_values).find(",") == -1:
				if x_picklistcheck == "TRUE":
					ATTRIBUTE_VALUE_STR += str(quer_value) + " = '" + str(quer_values) + "' and "
				else:
					ATTRIBUTE_VALUE_STR += str(quer_value) + " like '%" + str(quer_values) + "%' and "
			else:
				quer_values = quer_values.split(",")
				quer_values = tuple(list(quer_values))
				ATTRIBUTE_VALUE_STR += str(quer_value) + " in " + str(quer_values) + " and "
			if str(quer_value) == 'CONTRACT_FAB_LOC_GB_EQUIPMENT_RECORD_ID':                
				if str(str(quer_values)).find("-") == -1:                            
					ATTRIBUTE_VALUE_STR = (" CpqTableEntryId = '"+ str(quer_values)+ "' and ")                            
				else:
					xa_str = str(quer_values).split("-")[1]                            
					ATTRIBUTE_VALUE_STR = (" CpqTableEntryId = '"+ str(xa_str)+ "' and ")    

	data_list = []
	rec_id = "SYOBJ_00993"
	obj_id = "SYOBJ-00993"
	objh_getid = Sql.GetFirst(
		"SELECT TOP 1  RECORD_ID  FROM SYOBJH (NOLOCK) WHERE SAPCPQ_ATTRIBUTE_NAME='" + str(obj_id) + "'"
	)
	if objh_getid:
		obj_id = objh_getid.RECORD_ID
	objs_obj = Sql.GetFirst(
		"select CAN_ADD,CAN_EDIT,COLUMNS,CAN_DELETE from SYOBJR (NOLOCK) where OBJ_REC_ID = '" + str(obj_id) + "' "
	)
	can_edit = str(objs_obj.CAN_EDIT)
	can_clone = str(objs_obj.CAN_ADD)
	can_delete = str(objs_obj.CAN_DELETE)
	if ATTRIBUTE_VALUE is None or ATTRIBUTE_VALUE == "" or ATTRIBUTE_VALUE_STR is None or ATTRIBUTE_VALUE_STR == "":
		if TreeParam == 'Fab Locations':
			#Trace.Write("1 level empty search ---->") 
			parent_obj = Sql.GetList(
			"select top "+str(PerPage)+" CONTRACT_FAB_LOC_GB_EQUIPMENT_RECORD_ID,SALESORG_ID,EQUIPMENTCATEGORY_ID,EQUIPMENT_ID,MNT_PLANT_ID,CUSTOMER_TOOL_ID,SERIAL_NUMBER,GREENBOOK,CONTRACT_NAME,SALESORG_NAME,EQUIPMENT_DESCRIPTION,EQUIPMENT_STATUS,PLATFORM,FABLOCATION_ID,WARRANTY_START_DATE,CONTRACT_ID,FABLOCATION_NAME,WARRANTY_END_DATE from CTCFEQ (NOLOCK) where CONTRACT_RECORD_ID = '"
			+ str(ContractRecordId)            
			+ "'ORDER BY "  + str(orderby) )


			QueryCountObj = Sql.GetFirst("select count(*) as cnt from CTCFEQ (NOLOCK) where CONTRACT_RECORD_ID = '"+ str(ContractRecordId) +"'")
			if QueryCountObj is not None:
				QueryCount = QueryCountObj.cnt

		elif TreeParentParam == 'Fab Locations':
			#Trace.Write("2 level empty search ---->") 
			parent_obj = Sql.GetList(
				"select top "+str(PerPage)+" CONTRACT_FAB_LOC_GB_EQUIPMENT_RECORD_ID,SALESORG_ID,EQUIPMENTCATEGORY_ID,EQUIPMENT_ID,MNT_PLANT_ID,CUSTOMER_TOOL_ID,SERIAL_NUMBER,GREENBOOK,CONTRACT_NAME,SALESORG_NAME,EQUIPMENT_DESCRIPTION,EQUIPMENT_STATUS,PLATFORM,FABLOCATION_ID,WARRANTY_START_DATE,CONTRACT_ID,FABLOCATION_NAME,WARRANTY_END_DATE from CTCFEQ (NOLOCK) where CONTRACT_RECORD_ID = '"
				+ str(ContractRecordId)
				+ "' and FABLOCATION_ID = '"
				+ str(FablocationId)
				+ "'ORDER BY "  + str(orderby) 
			)
			QueryCountObj = Sql.GetFirst("select count(*) as cnt from CTCFEQ (NOLOCK) where CONTRACT_RECORD_ID = '"+ str(ContractRecordId) +"' and FABLOCATION_ID = '"+ str(FablocationId)+ "'")
			if QueryCountObj is not None:
				QueryCount = QueryCountObj.cnt
		elif TreeSuperParentParam == 'Fab Locations':
			#Trace.Write("3 level empty search ---->") 
			parent_obj = Sql.GetList(
					"select top "+str(PerPage)+" CONTRACT_FAB_LOC_GB_EQUIPMENT_RECORD_ID,SALESORG_ID,EQUIPMENTCATEGORY_ID,EQUIPMENT_ID,MNT_PLANT_ID,CUSTOMER_TOOL_ID,SERIAL_NUMBER,GREENBOOK,CONTRACT_NAME,SALESORG_NAME,EQUIPMENT_DESCRIPTION,EQUIPMENT_STATUS,PLATFORM,FABLOCATION_ID,WARRANTY_START_DATE,CONTRACT_ID,FABLOCATION_NAME,WARRANTY_END_DATE from CTCFEQ (NOLOCK) where CONTRACT_RECORD_ID = '"
					+ str(ContractRecordId)
					+ "' and FABLOCATION_ID = '"
					+ str(TreeParentParam)
					+ "' and GREENBOOK = '"+str(TreeParam)+"' ORDER BY "  + str(orderby) 
				) 
			QueryCountObj = Sql.GetFirst("select count(*) as cnt from CTCFEQ (NOLOCK) where CONTRACT_RECORD_ID = '"+ str(ContractRecordId) +"' and FABLOCATION_ID = '"+ str(TreeParentParam)+ "' and GREENBOOK = '"+str(TreeParam)+"'")
			if QueryCountObj is not None:
				QueryCount = QueryCountObj.cnt

	else:
		if TreeSuperParentParam == "Fab Locations":
			parent_obj = Sql.GetList(
				"select top "+str(PerPage)+"   CONTRACT_FAB_LOC_GB_EQUIPMENT_RECORD_ID,EQUIPMENTCATEGORY_ID,SERIAL_NUMBER,CUSTOMER_TOOL_ID,GREENBOOK,EQUIPMENT_STATUS,PLATFORM,MNT_PLANT_ID,EQUIPMENT_ID,EQUIPMENT_DESCRIPTION,FABLOCATION_ID,FABLOCATION_NAME,CONTRACT_ID,CONTRACT_NAME,SALESORG_ID,SALESORG_NAME,WARRANTY_START_DATE,WARRANTY_END_DATE,SUBSTRATE_SIZE from CTCFEQ (NOLOCK) where "
				+ str(ATTRIBUTE_VALUE_STR)
				+ " 1=1 and CONTRACT_RECORD_ID = '"
				+ str(ContractRecordId)
				+ "' and GREENBOOK = '"
				+ str(TreeParam)
				+ "' ORDER BY "  + str(orderby)
			)

			QueryCountObj = Sql.GetFirst("select count(*) as cnt from CTCFEQ (NOLOCK) where "
				+ str(ATTRIBUTE_VALUE_STR)
				+ " 1=1 and CONTRACT_RECORD_ID = '"
				+ str(ContractRecordId)
				+ "' and GREENBOOK = '"
				+ str(TreeParam)
				+ "' " )
			if QueryCountObj is not None:
				QueryCount = QueryCountObj.cnt


		else:
			parent_obj = Sql.GetList(
				"select top "+str(PerPage)+"   CONTRACT_FAB_LOC_GB_EQUIPMENT_RECORD_ID,EQUIPMENTCATEGORY_ID,SERIAL_NUMBER,CUSTOMER_TOOL_ID,GREENBOOK,EQUIPMENT_STATUS,PLATFORM,MNT_PLANT_ID,EQUIPMENT_ID,EQUIPMENT_DESCRIPTION,FABLOCATION_ID,FABLOCATION_NAME,CONTRACT_ID,CONTRACT_NAME,SALESORG_ID,SALESORG_NAME,WARRANTY_START_DATE,WARRANTY_END_DATE,SUBSTRATE_SIZE from CTCFEQ (NOLOCK) where "
				+ str(ATTRIBUTE_VALUE_STR)
				+ " 1=1 and CONTRACT_RECORD_ID = '"
				+ str(ContractRecordId)
				+ "' ORDER BY "  + str(orderby)
			)

			QueryCountObj = Sql.GetFirst("select count(*) as cnt from CTCFEQ (NOLOCK) where "
				+ str(ATTRIBUTE_VALUE_STR)
				+ " 1=1 and CONTRACT_RECORD_ID = '"
				+ str(ContractRecordId)
				+ "' " )
			if QueryCountObj is not None:
				QueryCount = QueryCountObj.cnt

	for par in parent_obj:
		data_dict = {}
		data_id = str(par.CONTRACT_FAB_LOC_GB_EQUIPMENT_RECORD_ID) + "|Contract Equipment Master"

		Action_str = (
			'<div class="btn-group dropdown"><div class="dropdown" id="ctr_drop"><i data-toggle="dropdown" id="dropdownMenuButton" class="fa fa-sort-desc dropdown-toggle" aria-expanded="false"></i><ul class="dropdown-menu left" aria-labelledby="dropdownMenuButton"><li><a class="dropdown-item cur_sty" href="#" id="'
			+ str(data_id)
			+ '" onclick="Move_to_parent_obj(this)">VIEW</a></li>'
		)
		if can_edit.upper() == "TRUE":
			Action_str += (
				'<li  ><a class="dropdown-item cur_sty" href="#" id="'
				+ str(data_id)
				+ '" onclick="Move_to_parent_obj_edit(this)">EDIT</a></li>'
			)
		if can_delete.upper() == "TRUE":
			Action_str += '<li><a class="dropdown-item" data-target="#cont_viewModal_Material_Delete" data-toggle="modal" onclick="Material_delete_obj(this)" href="#">DELETE</a></li>'
		if can_clone.upper() == "TRUE":
			Action_str += '<li><a class="dropdown-item" data-target="#" data-toggle="modal" onclick="Material_clone_obj(this)" href="#">CLONE</a></li>'

		Action_str += "</ul></div></div>"
		data_dict["ACTIONS"] = str(Action_str)
		data_dict["CONTRACT_FAB_LOC_GB_EQUIPMENT_RECORD_ID"] = CPQID.KeyCPQId.GetCPQId("CTCFEQ", str(par.CONTRACT_FAB_LOC_GB_EQUIPMENT_RECORD_ID))
		data_dict["EQUIPMENT_ID"] = str(par.EQUIPMENT_ID)
		data_dict["PLATFORM"] = str(par.PLATFORM)
		data_dict["FABLOCATION_ID"] = str(par.FABLOCATION_ID)
		data_dict["SALESORG_ID"] = str(par.SALESORG_ID)
		data_dict["EQUIPMENTCATEGORY_ID"] = str(par.EQUIPMENTCATEGORY_ID)
		data_dict["SERIAL_NUMBER"] = str(par.SERIAL_NUMBER)
		data_dict["CUSTOMER_TOOL_ID"] = str(par.CUSTOMER_TOOL_ID)
		data_dict["GREENBOOK"] = str(par.GREENBOOK)
		data_dict["EQUIPMENT_STATUS"] = str(par.EQUIPMENT_STATUS)
		data_dict["EQUIPMENT_DESCRIPTION"] = str(par.EQUIPMENT_DESCRIPTION)
		data_dict["FABLOCATION_NAME"] = str(par.FABLOCATION_NAME)
		data_dict["MNT_PLANT_ID"] = str(par.MNT_PLANT_ID)
		data_dict["WARRANTY_START_DATE"] = str(par.WARRANTY_START_DATE)
		data_dict["WARRANTY_END_DATE"] = str(par.WARRANTY_END_DATE)
		data_dict["CONTRACT_ID"] = str(par.CONTRACT_ID)
		data_list.append(data_dict)

	page = ""
	if QueryCount < int(PerPage):
		page = str(Page_start) + " - " + str(QueryCount) + " of "
	else:
		page = str(Page_start) + " - " + str(Page_End)+ " of "
	#return data_list, QueryCount, page
	# Trace.Write("GetContractEquipmentMasterFilter data_list --->"+str(data_list))
	# Trace.Write("GetContractEquipmentMasterFilter QueryCount ---->"+str(QueryCount))
	# Trace.Write("GetContractEquipmentMasterFilter page --->"+str(page))
	return data_list, QueryCount, page


def GetEquipmentChildFilter(ATTRIBUTE_NAME, ATTRIBUTE_VALUE, RECID,PerPage,PageInform):

	if str(PerPage) == "" and str(PageInform) == "":
		Page_start = 1
		Page_End = 10
		PerPage = 10
		PageInform = "1___10___10"
	else:
		Page_start = int(PageInform.split("___")[0])
		Page_End = int(PageInform.split("___")[1])
		PerPage = PerPage
	QueryCount = ""

	TreeParam = Product.GetGlobal("TreeParam")
	TreeParentParam = Product.GetGlobal("TreeParentLevel0")
	TreeSuperParentParam = Product.GetGlobal("TreeParentLevel1")
	TreeTopSuperParentParam =  Product.GetGlobal("TreeParentLevel2")

	FablocationId = Product.GetGlobal("TreeParam")
	ContractRecordId = Quote.GetGlobal("contract_quote_record_id")
	RevisionRecordId = Quote.GetGlobal("quote_revision_record_id")
	obj_id1 = "SYOBJ-00942"
	objh_getid = Sql.GetFirst(
		"SELECT TOP 1  RECORD_ID  FROM SYOBJH (NOLOCK) WHERE SAPCPQ_ATTRIBUTE_NAME='" + str(obj_id1) + "'"
	)
	if objh_getid:
		obj_id1 = objh_getid.RECORD_ID
	objs_obj1 = Sql.GetFirst(
		"select CAN_ADD,CAN_EDIT,COLUMNS,CAN_DELETE from SYOBJR (NOLOCK) where OBJ_REC_ID = '" + str(obj_id1) + "' "
	)
	can_edit1 = str(objs_obj1.CAN_EDIT)
	can_clone1 = str(objs_obj1.CAN_ADD)
	can_delete1 = str(objs_obj1.CAN_DELETE)
	recid = str(RECID)

	orderby = ""
	if SortColumn != '' and SortColumnOrder !='':
		orderby = SortColumn + " " + SortColumnOrder
	else:
		orderby = "QUOTE_FAB_LOC_COV_OBJ_ASSEMBLY_RECORD_ID"


	ATTRIBUTE_VALUE_STR = ""
	Dict_formation = dict(zip(ATTRIBUTE_NAME, ATTRIBUTE_VALUE))
	for quer_key, quer_value in enumerate(Dict_formation):
		if Dict_formation.get(quer_value) != "":
			quer_values = str(Dict_formation.get(quer_value)).strip()
			if str(quer_values).find(",") == -1:
				ATTRIBUTE_VALUE_STR += str(quer_value) + " like '%" + str(quer_values) + "%' and "
			else:
				quer_values = quer_values.split(",")
				quer_values = tuple(list(quer_values))
				ATTRIBUTE_VALUE_STR += str(quer_value) + " in " + str(quer_values) + " and "
	Trace.Write("data query starts ----->"+str(ATTRIBUTE_VALUE)+"ll==="+str(ATTRIBUTE_NAME))
	if ATTRIBUTE_VALUE is None or ATTRIBUTE_VALUE == "" or ATTRIBUTE_VALUE_STR is None or ATTRIBUTE_VALUE_STR == "":
		#Trace.Write("empty search --->")

		if TreeParam == 'Fab Locations':
			#Trace.Write("Level 1 empty search ---->")
			child_obj_recid = Sql.GetList(
				"select top "+str(PerPage)+" QUOTE_FAB_LOC_COV_OBJ_ASSEMBLY_RECORD_ID,EQUIPMENT_ID,SERIAL_NUMBER,ASSEMBLY_ID,ASSEMBLY_DESCRIPTION,GOT_CODE,MNT_PLANT_ID,FABLOCATION_ID,WARRANTY_START_DATE,EQUIPMENTCATEGORY_ID,WARRANTY_END_DATE,SALESORG_ID,EQUIPMENTTYPE_ID AS ASSEMBLYTYPE_ID from SAQFEA (NOLOCK) where EQUIPMENT_ID = '"
				+ str(recid)
				+ "' and QUOTE_RECORD_ID = '{ContractRecordId}'  and QTEREV_RECORD_ID = '{RevisionRecordId}' ORDER BY  {ORDER_BY}".format(
					ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"), ORDER_BY = orderby
				)
			)

			Count = Sql.GetFirst(
				"select count(*) as cnt from SAQFEA (NOLOCK) where EQUIPMENT_ID = '"
				+ str(recid)
				+ "' and QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' ".format(
					ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"))
			)
			if Count:
				QueryCount = Count.cnt

		elif TreeParentParam == 'Fab Locations':
			Trace.Write("Level 2 empty search ---->")
			if (TreeParam.startswith("Sending") or TreeParam.startswith("Receiving")):
				child_obj_recid = Sql.GetList(
					"select top "+str(PerPage)+" QUOTE_FAB_LOC_COV_OBJ_ASSEMBLY_RECORD_ID,EQUIPMENT_ID,SERIAL_NUMBER,ASSEMBLY_ID,ASSEMBLY_DESCRIPTION,GOT_CODE,MNT_PLANT_ID,FABLOCATION_ID,WARRANTY_START_DATE,EQUIPMENTCATEGORY_ID,WARRANTY_END_DATE,SALESORG_ID,EQUIPMENTTYPE_ID AS ASSEMBLYTYPE_ID from SAQFEA (NOLOCK) where EQUIPMENT_ID = '"+ str(recid)+ "' and QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' ORDER BY  {ORDER_BY}".format(ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"), ORDER_BY = orderby))
				Count = Sql.GetFirst(
					"select count(*) as cnt from SAQFEA (NOLOCK) where EQUIPMENT_ID = '"+ str(recid)+ "' and QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}'".format(ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id")))
				if Count:
					QueryCount = Count.cnt
			
			else:        
				child_obj_recid = Sql.GetList(
					"select top "+str(PerPage)+" QUOTE_FAB_LOC_COV_OBJ_ASSEMBLY_RECORD_ID,EQUIPMENT_ID,SERIAL_NUMBER,ASSEMBLY_ID,ASSEMBLY_DESCRIPTION,GOT_CODE,MNT_PLANT_ID,FABLOCATION_ID,WARRANTY_START_DATE,EQUIPMENTCATEGORY_ID,WARRANTY_END_DATE,SALESORG_ID,EQUIPMENTTYPE_ID AS ASSEMBLYTYPE_ID from SAQFEA (NOLOCK) where EQUIPMENT_ID = '"
					+ str(recid)
					+ "' and QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' and FABLOCATION_ID = '{FabId}' ORDER BY  {ORDER_BY}".format(
						ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"),FabId=TreeParam, ORDER_BY = orderby
					)
				)

				Count = Sql.GetFirst(
					"select count(*) as cnt from SAQFEA (NOLOCK) where EQUIPMENT_ID = '"
					+ str(recid)
					+ "' and QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}'".format(
						ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id")
					)
				)
				if Count:
					QueryCount = Count.cnt

		else:
			Trace.Write("Level 3 empty search ---->")
			if (TreeParentParam.startswith("Sending") or TreeParentParam.startswith("Receiving")):
				child_obj_recid = Sql.GetList(
					"select top "+str(PerPage)+" QUOTE_FAB_LOC_COV_OBJ_ASSEMBLY_RECORD_ID,EQUIPMENT_ID,SERIAL_NUMBER,ASSEMBLY_ID,ASSEMBLY_DESCRIPTION,GOT_CODE,MNT_PLANT_ID,FABLOCATION_ID,WARRANTY_START_DATE,EQUIPMENTCATEGORY_ID,WARRANTY_END_DATE,SALESORG_ID,EQUIPMENTTYPE_ID AS ASSEMBLYTYPE_ID from SAQFEA (NOLOCK) where EQUIPMENT_ID = '"+ str(recid)+ "' and QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' and FABLOCATION_ID = '{FabId}' ORDER BY  {ORDER_BY}".format(ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"),FabId=TreeParam, ORDER_BY = orderby))
				Count = Sql.GetFirst(
					"select count(*) as cnt from SAQFEA (NOLOCK) where EQUIPMENT_ID = '"+ str(recid)+ "' and QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' and FABLOCATION_ID = '{FabId}'".format(ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"), FabId=TreeParam))
				if Count:
					QueryCount = Count.cnt  

			elif (TreeSuperParentParam.startswith("Sending") or TreeSuperParentParam.startswith("Receiving")):
				child_obj_recid = Sql.GetList(
					"select top "+str(PerPage)+" QUOTE_FAB_LOC_COV_OBJ_ASSEMBLY_RECORD_ID,EQUIPMENT_ID,SERIAL_NUMBER,ASSEMBLY_ID,ASSEMBLY_DESCRIPTION,GOT_CODE,MNT_PLANT_ID,FABLOCATION_ID,WARRANTY_START_DATE,EQUIPMENTCATEGORY_ID,WARRANTY_END_DATE,SALESORG_ID,EQUIPMENTTYPE_ID AS ASSEMBLYTYPE_ID from SAQFEA (NOLOCK) where EQUIPMENT_ID = '"+ str(recid)+ "' and QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' and FABLOCATION_ID = '{FabId}' ORDER BY  {ORDER_BY}".format(ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"), FabId=TreeParentParam, ORDER_BY = orderby))
				Count = Sql.GetFirst(
					"select count(*) as cnt from SAQFEA (NOLOCK) where EQUIPMENT_ID = '"+ str(recid)+ "' and QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' and FABLOCATION_ID = '{FabId}'".format(ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"),FabId=TreeParentParam))
				if Count:
					QueryCount = Count.cnt

			else:        
				child_obj_recid = Sql.GetList(
					"select top "+str(PerPage)+" QUOTE_FAB_LOC_COV_OBJ_ASSEMBLY_RECORD_ID,EQUIPMENT_ID,SERIAL_NUMBER,ASSEMBLY_ID,ASSEMBLY_DESCRIPTION,GOT_CODE,MNT_PLANT_ID,FABLOCATION_ID,WARRANTY_START_DATE,EQUIPMENTCATEGORY_ID,WARRANTY_END_DATE,SALESORG_ID,EQUIPMENTTYPE_ID AS ASSEMBLYTYPE_ID from SAQFEA (NOLOCK) where EQUIPMENT_ID = '"
					+ str(recid)
					+ "' and QUOTE_RECORD_ID = '{ContractRecordId}'  and QTEREV_RECORD_ID = '{RevisionRecordId}' and FABLOCATION_ID = '{FabId}' ORDER BY  {ORDER_BY}".format(
						ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"), FabId=TreeParentParam, ORDER_BY = orderby
					)
				)

				Count = Sql.GetFirst(
					"select count(*) as cnt from SAQFEA (NOLOCK) where EQUIPMENT_ID = '"
					+ str(recid)
					+ "' and QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' and FABLOCATION_ID = '{FabId}'".format(
						ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"), FabId=TreeParentParam
					)
				)
				if Count:
					QueryCount = Count.cnt

	else:
		#Trace.Write("conditional search --->")
		Trace.Write("ATTRIBUTE_VALUE_STR_J "+str(ATTRIBUTE_VALUE_STR))
		if TreeSuperParentParam == "Fab Locations":
			if ATTRIBUTE_VALUE_STR.startswith("ASSEMBLYTYPE_ID"):
				ATTRIBUTE_VALUE_STR = str(ATTRIBUTE_VALUE_STR).replace('ASSEMBLYTYPE_ID','EQUIPMENTTYPE_ID')
		child_obj_recid = Sql.GetList(
			"select top "+str(PerPage)+" QUOTE_FAB_LOC_COV_OBJ_ASSEMBLY_RECORD_ID,EQUIPMENT_ID,SERIAL_NUMBER,ASSEMBLY_ID,ASSEMBLY_DESCRIPTION,GOT_CODE,MNT_PLANT_ID,FABLOCATION_ID,WARRANTY_START_DATE,EQUIPMENTCATEGORY_ID,WARRANTY_END_DATE,SALESORG_ID,EQUIPMENTTYPE_ID AS ASSEMBLYTYPE_ID from SAQFEA (NOLOCK) where EQUIPMENT_ID = '"
			+ str(recid)
			+ "' and "
			+ str(ATTRIBUTE_VALUE_STR)
			+ " 1=1 and QUOTE_RECORD_ID = '"
			+ str(ContractRecordId)
			+ "' and QTEREV_RECORD_ID = '"
			+ str(RevisionRecordId)
			+ "' ORDER BY "+str(orderby)+"" 
		)
		Count = Sql.GetFirst("select count(*) as cnt from SAQFEA (NOLOCK) where EQUIPMENT_ID = '"
			+ str(recid)
			+ "' and "
			+ str(ATTRIBUTE_VALUE_STR)
			+ " 1=1 and QUOTE_RECORD_ID = '"
			+ str(ContractRecordId)
			+ "' and QTEREV_RECORD_ID = '"
			+ str(RevisionRecordId)
			+ "' " )
		if Count:
			QueryCount = Count.cnt

	chld_list = []
	# Data construction for table.
	for cld in child_obj_recid:
		'''cld = Sql.GetFirst(
			"select QUOTE_FAB_LOC_COV_OBJ_ASSEMBLY_RECORD_ID,EQUIPMENT_ID,ASSEMBLY_ID,SERIAL_NUMBER,EQUIPMENTCATEGORY_ID,ASSEMBLY_DESCRIPTION,GOT_CODE,MNT_PLANT_ID,FABLOCATION_ID,WARRANTY_START_DATE,WARRANTY_END_DATE,SALESORG_ID from SAQFEA (NOLOCK) where EQUIPMENT_ID = '{EquipmentID}' and QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}'  and FABLOCATION_ID = '{FablocationId}'".format(
				EquipmentID=child.EQUIPMENT_ID,
				ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),
				RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"),
				FablocationId=Product.GetGlobal("TreeParentLevel0"),
			)
		)'''
		if cld is not None:
			chld_dict = {}
			data_id = str(cld.QUOTE_FAB_LOC_COV_OBJ_ASSEMBLY_RECORD_ID) + "|SAQFEA"
			Action_str1 = (
				'<div class="btn-group dropdown"><div class="dropdown" id="ctr_drop"><i data-toggle="dropdown" id="dropdownMenuButton" class="fa fa-sort-desc dropdown-toggle" aria-expanded="false"></i><ul class="dropdown-menu left" aria-labelledby="dropdownMenuButton"><li ><a  data-toggle="modal" data-target="#cont_viewModalSection" id="'
				+ str(data_id)
				+ '" class="dropdown-item cur_sty" href="#"  onclick="cont_relatedlist_openview(this) ">VIEW</a></li>'
			)
			if can_edit1.upper() == "TRUE" and Lock_val.upper() != "TRUE":
				Action_str1 += (
					'<li style="display:none" ><a data-toggle="modal" data-target="#cont_viewModalSection" id="'
					+ str(data_id)
					+ '"  class="dropdown-item cur_sty" href="#"  onclick="cont_relatedlist_openedit(this)">EDIT</a></li>'
				)
			if can_delete1.upper() == "TRUE":
				Action_str1 += '<li><a class="dropdown-item" data-target="#cont_viewModal_Material_Delete" data-toggle="modal" onclick="Material_delete_obj(this)" href="#">DELETE</a></li>'
			if can_clone1.upper() == "TRUE":
				Action_str1 += '<li><a class="dropdown-item" data-target="#" data-toggle="modal" onclick="Material_clone_obj(this)" href="#">CLONE</a></li>'
			Action_str1 += "</ul></div></div>"

			# data formation in Dictonary format.
			chld_dict["ACTIONS"] = str(Action_str1)
			chld_dict["QUOTE_FAB_LOC_COV_OBJ_ASSEMBLY_RECORD_ID"] = str(cld.QUOTE_FAB_LOC_COV_OBJ_ASSEMBLY_RECORD_ID)
			chld_dict["EQUIPMENT_ID"] = str(cld.EQUIPMENT_ID)
			chld_dict["ASSEMBLY_ID"] = str(cld.ASSEMBLY_ID)
			chld_dict["EQUIPMENTCATEGORY_ID"] = str(cld.EQUIPMENTCATEGORY_ID)
			chld_dict["ASSEMBLY_DESCRIPTION"] = str(cld.ASSEMBLY_DESCRIPTION)
			chld_dict["GOT_CODE"] = str(cld.GOT_CODE)
			chld_dict["MNT_PLANT_ID"] = str(cld.MNT_PLANT_ID)
			chld_dict["FABLOCATION_ID"] = str(cld.FABLOCATION_ID)
			chld_dict["WARRANTY_START_DATE"] = str(cld.WARRANTY_START_DATE)
			chld_dict["WARRANTY_END_DATE"] = str(cld.WARRANTY_END_DATE)
			chld_dict["SALESORG_ID"] = str(cld.SALESORG_ID)
			chld_dict["SERIAL_NUMBER"] = str(cld.SERIAL_NUMBER)
			chld_dict["ASSEMBLYTYPE_ID"] = str(cld.ASSEMBLYTYPE_ID)
			chld_list.append(chld_dict)
	#Trace.Write("5555 chld_list ---->"+str(chld_list))

	page = ""
	if QueryCount < int(PerPage):
		page = str(Page_start) + " - " + str(QueryCount) + " of "
	else:
		page = str(Page_start) + " - " + str(Page_End)+ " of "
	# Trace.Write("9999 QueryCount --->"+str(QueryCount))
	# Trace.Write("9999 page --->"+str(page))

	return chld_list,QueryCount,page
##EQUIPMENTS GRID ENDS...
##PREVENTIVE MAINTAINENECE STARTS...
def QuoteAssemblyPreventiveMaintainenceParent(PerPage, PageInform, A_Keys, A_Values,ASSEMBLYID,EQUIPMENTID):
	if str(PerPage) == "" and str(PageInform) == "":
		Page_start = 1
		Page_End = 10
		PerPage = 10
		PageInform = "1___10___10"
	else:
		Page_start = int(PageInform.split("___")[0])
		Page_End = int(PageInform.split("___")[1])
		PerPage = PerPage
	TreeParam = Product.GetGlobal("TreeParam")
	TreeParentParam = Product.GetGlobal("TreeParentLevel0")
	TreeSuperParentParam = Product.GetGlobal("TreeParentLevel1")
	TopSuperParentParam = Product.GetGlobal("TreeParentLevel2")
	ContractRecordId = Quote.GetGlobal("contract_quote_record_id")
	RevisionRecordId = Quote.GetGlobal("quote_revision_record_id")
	data_list = []
	obj_idval = "SYOBJ_00974_SYOBJ_00974"
	rec_id = "SYOBJ_00974"
	obj_id = "SYOBJ-00974"
	if str(SortColumn)!='' and str(SortColumnOrder)!='':
		sort_by = " ORDER BY "+str(SortColumn)+" "+str(SortColumnOrder)
	else:
		sort_by = ' ORDER BY QUOTE_SERVICE_COV_OBJ_ASS_PM_KIT_RECORD_ID'
	objh_getid = Sql.GetFirst(
		"SELECT TOP 1  RECORD_ID  FROM SYOBJH (NOLOCK) WHERE SAPCPQ_ATTRIBUTE_NAME='" + str(obj_id) + "'"
	)
	if objh_getid:
		obj_id = objh_getid.RECORD_ID
	objs_obj = Sql.GetFirst(
		"select CAN_ADD,CAN_EDIT,COLUMNS,CAN_DELETE from SYOBJR (NOLOCK) where OBJ_REC_ID = '" + str(obj_id) + "' "
	)
	quote_status = Sql.GetFirst("SELECT REVISION_STATUS FROM SAQTRV WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(ContractRecordId,RevisionRecordId))
	can_edit = str(objs_obj.CAN_EDIT)
	can_add = str(objs_obj.CAN_ADD)
	can_delete = str(objs_obj.CAN_DELETE)
	table_id = "table_Preventive_Maintainence_parent"
	table_header = (
		'<table id="'
		+ str(table_id)
		+ '"  data-pagination="false" data-sortable="true" data-search-on-enter-key="true" data-filter-control="true" data-pagination-loop = "false" data-locale = "en-US" ><thead>'
	)
	Columns = [
		"QUOTE_SERVICE_COV_OBJ_ASS_PM_KIT_RECORD_ID",
		"EQUIPMENT_DESCRIPTION",
		"EQUIPMENT_ID",
		"SERIAL_NO",
		"ASSEMBLY_ID",
		"GOT_CODE",
		"PM_ID",
		"PM_NAME",
		#"ANNUAL_FREQUENCY_BASE",
		"SSCM_PM_FREQUENCY",
		"PM_FREQUENCY",
		"KIT_ID",
		"KIT_NAME",
		# "KIT_NUMBER",
		"TKM_FLAG",
	]
	
	Objd_Obj = Sql.GetList(
		"select FIELD_LABEL,API_NAME,LOOKUP_OBJECT,LOOKUP_API_NAME,DATA_TYPE from SYOBJD (NOLOCK) where OBJECT_NAME = 'SAQSAP'"
	)
	attr_list = []
	attrs_datatype_dict = {}
	lookup_disply_list = []
	lookup_str = ""
	QueryCountObj = ""
	QueryCount = ""
	dbl_clk_function = ""
	if Objd_Obj is not None:
		attr_list = {}
		for attr in Objd_Obj:
			attr_list[str(attr.API_NAME)] = str(attr.FIELD_LABEL)
			attrs_datatype_dict[str(attr.API_NAME)] = str(attr.DATA_TYPE)
			if attr.LOOKUP_API_NAME != "" and attr.LOOKUP_API_NAME is not None:
				lookup_disply_list.append(str(attr.API_NAME))
		checkbox_list = [inn.API_NAME for inn in Objd_Obj if inn.DATA_TYPE == "CHECKBOX"]
		lookup_list = {ins.LOOKUP_API_NAME: ins.API_NAME for ins in Objd_Obj}
	lookup_str = ",".join(list(lookup_disply_list))
	if TreeSuperParentParam == "Comprehensive Services" or TreeSuperParentParam == "Complementary Products":
		Qstr = (
			"select top "
			+ str(PerPage)
			+ " * from ( select  ROW_NUMBER() OVER( ORDER BY QUOTE_SERVICE_COV_OBJ_ASS_PM_KIT_RECORD_ID) AS ROW, QUOTE_SERVICE_COV_OBJ_ASS_PM_KIT_RECORD_ID,EQUIPMENT_DESCRIPTION,EQUIPMENT_ID,SERIAL_NO,ASSEMBLY_ID,GOT_CODE,KIT_ID,KIT_NAME,PM_ID,PM_NAME,TKM_FLAG,KIT_NUMBER,ANNUAL_FREQUENCY_BASE,SSCM_PM_FREQUENCY,PM_FREQUENCY from SAQSAP (NOLOCK) where QUOTE_RECORD_ID = '"
			+ str(ContractRecordId)
			+ "' and QTEREV_RECORD_ID = '"
			+ str(RevisionRecordId)
			+ "' and ASSEMBLY_ID = '"+str(ASSEMBLYID)+"'and EQUIPMENT_ID = '"+str(EQUIPMENTID)+"' ) m where m.ROW BETWEEN "
			+ str(Page_start)
			+ " and "
			+ str(Page_End) + " "+ str(sort_by)
		)
		QueryCountObj = Sql.GetFirst(
			"select count(QUOTE_SERVICE_COV_OBJ_ASS_PM_KIT_RECORD_ID) as cnt from SAQSAP (NOLOCK) where QUOTE_RECORD_ID = '"
			+ str(ContractRecordId)
			+ "' and QTEREV_RECORD_ID = '"
			+ str(RevisionRecordId)
			+ "' and ASSEMBLY_ID = '"+str(ASSEMBLYID)+"'and EQUIPMENT_ID = '"+str(EQUIPMENTID)+"' "
		)
	elif TreeParentParam == "Comprehensive Services" or TreeParentParam == "Complementary Products":
		Qstr = (
			"select QUOTE_SERVICE_COV_OBJ_ASS_PM_KIT_RECORD_ID,EQUIPMENT_DESCRIPTION,EQUIPMENT_ID,SERIAL_NO,GOT_CODE,ASSEMBLY_ID,KIT_ID,KIT_NAME,PM_ID,PM_NAME,TKM_FLAG,KIT_NUMBER,ANNUAL_FREQUENCY_BASE,SSCM_PM_FREQUENCY,PM_FREQUENCY from SAQSAP (NOLOCK) where QUOTE_RECORD_ID = '"
			+ str(ContractRecordId)
			+ "' and QTEREV_RECORD_ID = '"
			+ str(RevisionRecordId)
			+ "' and SERVICE_ID = '"
			+ str(TreeParam).split('-')[0]
			+ "' "+str(sort_by)+" OFFSET "+str(Page_start)+" ROWS FETCH NEXT "+str(PerPage)+" ROWS ONLY "
		)
		QueryCountObj = Sql.GetFirst(
			"select count(QUOTE_SERVICE_COV_OBJ_ASS_PM_KIT_RECORD_ID) as cnt from SAQSAP (NOLOCK) where QUOTE_RECORD_ID = '"
			+ str(ContractRecordId)
			+ "' and QTEREV_RECORD_ID = '"
			+ str(RevisionRecordId)
			+ "' and SERVICE_ID = '"
			+ str(TreeParam).split('-')[0]
			+ "' "
		)
		
	if QueryCountObj is not None:
		QueryCount = QueryCountObj.cnt
		#Trace.Write("count---->" + str(QueryCount))
	parent_obj = Sql.GetList(Qstr)
	for par in parent_obj:
		data_id = str(par.QUOTE_SERVICE_COV_OBJ_ASS_PM_KIT_RECORD_ID)

		Action_str = (
			'<div class="btn-group dropdown"><div class="dropdown" id="ctr_drop"><i data-toggle="dropdown" id="dropdownMenuButton" class="fa fa-sort-desc dropdown-toggle" aria-expanded="false"></i><ul class="dropdown-menu left" aria-labelledby="dropdownMenuButton"><li><a class="dropdown-item cur_sty" href="#" id="'
			+ str(data_id)
			+ '" onclick="Commonteree_view_RL(this)">VIEW</a></li>'
			'<li><a class="dropdown-item" id="deletebtn" data-target="#cont_CommonModalDelete" data-toggle="modal" onclick="CommonDelete(this, \'SAQFEA#'+ data_id +'\', \'WARNING\')" href="#">DELETE</a></li>'
		)
		if can_edit.upper() == "TRUE":
			Action_str += (
				'<li style="display:none" ><a class="dropdown-item cur_sty" href="#" id="'
				+ str(data_id)
				+ '" onclick="Move_to_parent_obj_edit(this)">EDIT</a></li>'
			)
		if can_delete.upper() == "TRUE":
			Action_str += '<li><a class="dropdown-item" data-target="#cont_viewModal_Material_Delete" data-toggle="modal" onclick="Material_delete_obj(this)" href="#">DELETE</a></li>'
		Action_str += "</ul></div></div>"


		decimal_place = 2 
		my_format = "{:,." + str(decimal_place) + "f}"
		original_PM_frequency = str(my_format.format(round(float(par.SSCM_PM_FREQUENCY), int(decimal_place))))
		pm_frequency = str(my_format.format(round(float(par.PM_FREQUENCY), int(decimal_place))))

		# Data formation in dictonary format.
		## hyperlink
		data_dict = {}
		data_dict["ids"] = str(data_id)
		data_dict["ACTIONS"] = str(Action_str)
		data_dict["QUOTE_SERVICE_COV_OBJ_ASS_PM_KIT_RECORD_ID"] = CPQID.KeyCPQId.GetCPQId(
			"SAQSAP", str(par.QUOTE_SERVICE_COV_OBJ_ASS_PM_KIT_RECORD_ID)
		)
		# data_dict["KIT_ID"] = str(par.KIT_ID)
		data_dict["EQUIPMENT_DESCRIPTION"] = str(par.EQUIPMENT_DESCRIPTION)
		data_dict["ASSEMBLY_ID"] = str(par.ASSEMBLY_ID)
		data_dict["EQUIPMENT_ID"] = str(par.EQUIPMENT_ID)
		data_dict["SERIAL_NO"] = str(par.SERIAL_NO)
		data_dict["GOT_CODE"] = str(par.GOT_CODE)
		data_dict["KIT_ID"] = str(par.KIT_ID)
		data_dict["KIT_NAME"] = str(par.KIT_NAME)
		# data_dict["KIT_NUMBER"] = str(par.KIT_NUMBER)
		data_dict["PM_ID"] = str(par.PM_ID)
		data_dict["PM_NAME"] = str(par.PM_NAME)
		data_dict["TKM_FLAG"] = str(par.TKM_FLAG)
		data_dict["ANNUAL_FREQUENCY_BASE"] = str(par.ANNUAL_FREQUENCY_BASE)
		data_dict["SSCM_PM_FREQUENCY"] = str(original_PM_frequency)
		data_dict["PM_FREQUENCY"] = str(pm_frequency)
		data_list.append(data_dict)

	hyper_link = ["QUOTE_SERVICE_COV_OBJ_ASS_PM_KIT_RECORD_ID","PM_FREQUENCY"]
	ParentObj = Sql.GetList(
		"select ASSEMBLY_ID from SAQSAP (NOLOCK) where QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' and ASSEMBLY_ID = '{AssemblyId}'".format(
			ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"), AssemblyId = ASSEMBLYID,
		)
	)
	table_header += "<tr>"
	table_header += (
		'<th data-field="ACTIONS"><div class="action_col">ACTIONS</div><button class="searched_button" id="Act_'
		+ str(table_id)
		+ '">Search</button></th>'
	)
	table_header += '<th data-field="SELECT" class="wid45" data-checkbox="true"></th>'
	for key, invs in enumerate(list(Columns)):
		invs = str(invs).strip()
		qstring = attr_list.get(str(invs)) or ""
		if qstring == "":
			qstring = invs.replace("_", " ")
		if checkbox_list is not None and invs in checkbox_list:
			table_header += (
				'<th  id="'
				+ str(invs)
				+ '"  data-field="'
				+ str(invs)
				+ '" data-filter-control="input" data-align="center" data-formatter="CheckboxFieldRelatedList" data-sortable="true"><abbr title="'
				+ str(qstring)
				+ '">'
				+ str(qstring)
				+ "</abbr></th>"
			)
		elif hyper_link is not None and invs in hyper_link:            
			if invs == "PM_FREQUENCY":
				data_formatter = "PMFrequencyBulkEditHyperLink" if quote_status.REVISION_STATUS!="APPROVED" else ""
			elif invs=="QUOTE_SERVICE_COV_OBJ_ASS_PM_KIT_RECORD_ID":
				data_formatter = "PreventiveMaintainenceHyperLinkTreeLink" 
			else:
				data_formatter = ""
			table_header += (
				'<th  id="'
				+ str(invs)
				+ '"  data-field="'
				+ str(invs)
				+ '" data-filter-control="input" data-formatter="'+str(data_formatter)+'" data-sortable="true"><abbr title="'
				+ str(qstring)
				+ '">'
				+ str(qstring)
				+ "</abbr></th>" 
			)
		else:
			table_header += (
				'<th  id="'
				+ str(invs)
				+ '"  data-field="'
				+ str(invs)
				+ '" data-filter-control="input" data-sortable="true"><abbr title="'
				+ str(qstring)
				+ '">'
				+ str(qstring)
				+ "</abbr></th>"
			)
	table_header += "</tr>"
	table_header += '</thead><tbody onclick="Table_Onclick_Scroll(this)"></tbody></table>'
	table_ids = "#" + str(table_id)
	filter_control_function = ""
	values_list = ""
	tbl_id = str(table_id)
	for key, invs in enumerate(list(Columns)):
		table_ids = "#" + str(table_id)
		filter_clas = "#" + str(table_id) + " .bootstrap-table-filter-control-" + str(invs)
		values_list += "var " + str(invs) + ' = $("' + str(filter_clas) + '").val(); '
		values_list += "ATTRIBUTE_VALUEList.push(" + str(invs) + "); "
		tbl_id = str(table_id)
	filter_class = "#Act_" + str(table_id)
	filter_control_function += (
		'$("'
		+ filter_class
		+ '").click( function(){ var table_id = $(this).closest("table").attr("id"); ATTRIBUTE_VALUEList = []; '
		+ str(values_list)
		+ ' var attribute_value = $(this).val(); cpq.server.executeScript("CQNESTGRID", {"TABNAME":"Preventive Maintainence Parent", "ACTION":"PRODUCT_ONLOAD_FILTER", "ATTRIBUTE_NAME": '
		+ str(list(Columns))
		+ ', "ATTRIBUTE_VALUE": ATTRIBUTE_VALUEList ,"ASSEMBLYID" : "'
		+ str(ASSEMBLYID)
		+'", "EQUIPMENTID" : "'
		+ str(EQUIPMENTID)
		+'"}, function(dataset) { data2 = dataset[1];  data1 = dataset[0]; data3 = dataset[2]; console.log("len ---->"+data1.length);  try { if(data1.length > 0) { $("#' + str(tbl_id) + '").bootstrapTable("load", data1 );$("#noRecDisp").remove(); if (document.getElementById("'+str(tbl_id) + '___totalItemCount")){document.getElementById("'+str(tbl_id)+ '___totalItemCount").innerHTML = data2;}  if (document.getElementById("'+str(tbl_id) + '___NumberofItem")) {document.getElementById("'+str(tbl_id)+ '___NumberofItem").innerHTML = data3;}} else{ $("#' + str(tbl_id) + '").bootstrapTable("load", data1  );$("#' + str(tbl_id) + '").after("<div id=\'noRecDisp\' class=\'noRecord\'>No Records to Display</div>"); $(".noRecord:not(:first)").remove(); if (document.getElementById("'+str(tbl_id) + '___totalItemCount")){document.getElementById("'+str(tbl_id)+ '___totalItemCount").innerHTML = data2;}  if (document.getElementById("'+str(tbl_id) + '___NumberofItem")) {document.getElementById("'+str(tbl_id)+ '___NumberofItem").innerHTML = data3;} }} catch(err){} }); filter_search_click();$(".JColResizer").mousedown(function(){ $("thead.fullHeadFirst").css("cssText","z-index: 2;border-top: 1px solid rgb(220, 220, 220);top: 154px;border-right: 0px !important;");$("thead.fullHeadSecond").css("display","none"); });$(".JColResizer").mouseup(function(){ var th_width_resize = [];$("#table_Preventive_Maintainence_parent thead.fullHeadFirst tr th").each(function(index){var wid = $(this).css("width"); if(index ==0 || index ==1){th_width_resize.push("60px");}else{th_width_resize.push(wid);}}); $("thead.fullHeadFirst").css("cssText","position: fixed;z-index: 2;border-top: 1px solid rgb(220, 220, 220); top: 154px;border-right: 0px !important;");$("thead.fullHeadSecond").css("display","table-header-group");$("#table_Preventive_Maintainence_parent thead.fullHeadFirst tr th").each(function(index){var num = th_width_resize[index].split("px");var numsp = parseInt(num[0]);numsp = numsp - 1;var make_str =numsp+"px"; var c = "width:"+make_str+";white-space: nowrap;overflow: hidden;text-overflow: ellipsis;";var d = "width:"+make_str+";"; $(this).css("cssText",c);$(this).children("div:first-child").css("cssText",c);$(this).children("div.fht-cell").css("cssText",d);});$("#table_Preventive_Maintainence_parent thead.fullHeadSecond tr th").each(function(index){var num = th_width_resize[index].split("px");var numsp = parseInt(num[0]);numsp = numsp - 1;var make_str =numsp+"px"; var c = "width:"+make_str+";white-space: nowrap;overflow: hidden;text-overflow: ellipsis;";var d = "width:"+make_str+";"; $(this).css("cssText",c);$(this).children("div:first-child").css("cssText",c);$(this).children("div.fht-cell").css("cssText",d);}); });});'
	)

	### editablity in Grid 
	if TopSuperParentParam in ('Comprehensive Services','Complementary Products'): 
		cls = "eq(2)"
		# dbl_clk_function = ( 
		# 	'var checkedRows=[]; debugger;localStorage.setItem("multiedit_checkbox_clicked", []); $("'
		# 	+ str(table_ids)
		# 	+ '").on("dbl-click-cell.bs.table", function (e, row, $element) { console.log("checked00009==");checkedRows.push($element.closest("tr").find("td:'
		# 	+ str(cls)
		# 	+ '").text()); localStorage.setItem("multiedit_checkbox_clicked", checkedRows); }); $("'
		# 	+ str(table_ids)
		# 	+ '").on("check-all.bs.table", function (e) { var table = $("'
		# 	+ str(table_ids)
		# 	+ '").closest("table"); table.find("tbody tr").each(function() { checkedRows.push($(this).find("td:nth-child(3)").text()); }); localStorage.setItem("multiedit_checkbox_clicked", checkedRows); });  '
		# ) 
		# buttons = "<button class=\'btnconfig\' onclick=\'multiedit_RL_cancel();\' type=\'button\' value=\'Cancel\' id=\'cancelButton\'>CANCEL</button><button class=\'btnconfig\' type=\'button\' value=\'Save\' onclick=\'multiedit_save_RL()\' id=\'saveButton\'>SAVE</button>" 
		# dbl_clk_function = (	 
		# 	'$("'	
		# 	+ str(table_ids)	
		# 	+ '").on("dbl-click-cell.bs.table", onClickCell); $("'	
		# 	+ str(table_ids)	
		# 	+ '").on("all.bs.table", function (e, name, args) { $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); }); $("'	
		# 	+ str(table_ids)	
		# 	+ '\ th.bs-checkbox div.th-inner").before(""); $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); function onClickCell(event, field, value, row, $element) { if(localStorage.getItem("InlineEdit")=="YES"){ return ;} var reco_id="";reco_id=$element.closest("tr").find("td:'	
		# 	+ str(cls)	
		# 	+ '").text().trim();console.log("reco_id2--",reco_id);reco_id=reco_id; reco_id=reco_id.split(","); localStorage.setItem("multiedit_save_date", reco_id);  localStorage.setItem("table_id_RL_edit", "SYOBJR_00011_1E92CAAD_4EE9_4E5C_AA11_80F20D295A63");console.log("value--",field);edit_index = $("'+str(table_ids)+'").find("[data-field="+ field +"]").index()+1;localStorage.setItem("edit_index",edit_index); cpq.server.executeScript("SYBLKETRLG", {"TITLE":field, "VALUE":value, "CLICKEDID":"SYOBJR_00011_1E92CAAD_4EE9_4E5C_AA11_80F20D295A63", "RECORDID":reco_id, "ELEMENT":"RELATEDEDIT"}, function(data) { debugger; data1=data[0]; data2=data[1]; data3 = data[2];if(data1 != "NO"){ if(document.getElementById("RL_EDIT_DIV_ID") ) { localStorage.setItem("saqico_title", field); inp = "#"+data3;localStorage.setItem("value_tag", "'+ str(table_id)+' "+inp);$("'+str(table_ids)+'").closest("tr").find("td:nth-child("+edit_index+")").attr("contenteditable", true); var buttonlen = $("#seginnerbnr").find("button#saveButton"); if (buttonlen.length == 0){	$("#seginnerbnr").append("<button class=\'btnconfig\' onclick=\'PreventiveMaintainenceTreeTable();\' type=\'button\' value=\'Cancel\' id=\'cancelButton\'>CANCEL</button><button class=\'btnconfig\' type=\'button\' value=\'Save\' onclick=\'multiedit_save_RL()\' id=\'saveButton\'>SAVE</button>");}else{$("#cancelButton").css("display", "block");$("#saveButton").css("display", "block");}$("'+str(table_ids)+'").closest("tr").find("td:nth-child("+edit_index+")").addClass("light_yellow"); document.getElementById("cont_multiEditModalSection").style.display = "none";  var divHeight = $("#cont_multiEditModalSection").height(); $("#cont_multiEditModalSection .modal-backdrop").css("min-height", divHeight+"px"); $("#cont_multiEditModalSection .modal-dialog").css("width","550px"); $(".modal-dialog").css("margin-top","100px"); } if (data2.length !== 0){ $.each( data2, function( key, values ) { onclick_datepicker(values) }); } } }); } ')
		dbl_clk_function = ('$(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); $("'
			+ str(table_ids)
			+ '").on("all.bs.table", function (e, name, args) { $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); }); $("'
			+ str(table_ids)
			+ '\ th.bs-checkbox div.th-inner").before("<div style=\'padding:0; border-bottom: 1px solid #dcdcdc;\'>SELECT</div>"); $(".bs-checkbox input").addClass("custom"); $("'	
			+ str(table_ids)	
			+ "\").on('sort.bs.table', function (e, name, order) {  currenttab = $(\"ul#carttabs_head .active\").text().trim(); localStorage.setItem('"	
			+ str(table_id)	
			+ "_SortColumn', name); localStorage.setItem('"	
			+ str(table_id)	
			+ "_SortColumnOrder', order); }); "	
		)
	else:
		if TreeParentParam in ('Comprehensive Services','Complementary Products'):
			cls = "eq(2)"
			dbl_clk_function += (
				'$("'	
				+ str(table_ids)	
				+ '").on("dbl-click-cell.bs.table", onClickCell);'
			)
			dbl_clk_function += (
				'function onClickCell(event, field, value, row, $element) { if(localStorage.getItem("InlineEdit")=="YES"){ return ;} var reco_id="";reco_id=$element.closest("tr").find("td:'	
				+ str(cls)	
				+ '").text().trim();console.log("reco_id2--",reco_id);reco_id=reco_id; reco_id=reco_id.split(","); localStorage.setItem("multiedit_save_date", reco_id);  localStorage.setItem("table_id_RL_edit", "SYOBJR_00011_1E92CAAD_4EE9_4E5C_AA11_80F20D295A63");console.log("field--",field);console.log("value--",value);edit_index = $("'+str(table_ids)+'").find("[data-field="+ field +"]").index()+1;localStorage.setItem("edit_index",edit_index); cpq.server.executeScript("SYBLKETRLG", {"TITLE":field, "VALUE":value, "CLICKEDID":"SYOBJR_00011_1E92CAAD_4EE9_4E5C_AA11_80F20D295A63", "RECORDID":reco_id, "ELEMENT":"RELATEDEDIT"}, function(data) { debugger;  data1=data[0]; data2=data[1]; if(data1 != "NO"){ if(document.getElementById("RL_EDIT_DIV_ID") ) { document.getElementById("RL_EDIT_DIV_ID").innerHTML = data1; document.getElementById("cont_multiEditModalSection").style.display = "block"; $("#cont_multiEditModalSection").prepend("<div class=\'modal-backdrop fade in\'></div>"); var divHeight = $("#cont_multiEditModalSection").height(); $("#cont_multiEditModalSection .modal-backdrop").css("min-height", divHeight+"px"); $("#cont_multiEditModalSection .modal-dialog").css("width","550px"); $(".modal-dialog").css("margin-top","100px"); }   var divHeight = $("#cont_multiEditModalSection").height(); $("#cont_multiEditModalSection .modal-backdrop").css("min-height", divHeight+"px"); $("#cont_multiEditModalSection .modal-dialog").css("width","550px"); $(".modal-dialog").css("margin-top","100px"); } if (data2.length !== 0){ $.each( data2, function( key, values ) { onclick_datepicker(values) }); }  }); }'
			)
		dbl_clk_function += ('$(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); $("'
			+ str(table_ids)
			+ '").on("all.bs.table", function (e, name, args) { $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); }); $("'
			+ str(table_ids)
			+ '\ th.bs-checkbox div.th-inner").before("<div style=\'padding:0; border-bottom: 1px solid #dcdcdc;\'>SELECT</div>"); $(".bs-checkbox input").addClass("custom"); $("'
			+ str(table_ids)
			+ "\").on('sort.bs.table', function (e, name, order) { console.log('sort.bs.table ============>', e); e.stopPropagation(); currenttab = $(\"ul#carttabs_head .active\").text().trim(); localStorage.setItem('"
			+ str(table_id)
			+ "_SortColumn', name); localStorage.setItem('"
			+ str(table_id)
			+ "_SortColumnOrder', order); PmEventsNestedContainerSorting(name, order, '"
			+ str(table_id)
			+ "','"+str(ASSEMBLYID)+"','"+str(EQUIPMENTID)+"'); }); "
		)
	Trace.Write("7777 dbl_clk_function --->"+str(dbl_clk_function))
	NORECORDS = ""
	if len(data_list) == 0:
		NORECORDS = "NORECORDS"

	ObjectName = "SAQSAP"
	DropDownList = []
	RelatedDrop_str = ""
	filter_level_list = []
	filter_clas_name = ""
	cv_list = []
	TableclassName = "form-control" + table_id
	for key, col_name in enumerate(list(Columns)):
		StringValue_list = []
		objss_obj = Sql.GetFirst(
			"SELECT API_NAME, DATA_TYPE, FORMULA_LOGIC, PICKLIST FROM SYOBJD (NOLOCK) WHERE OBJECT_NAME='"
			+ str(ObjectName)
			+ "' and API_NAME = '"
			+ str(col_name)
			+ "'"
		)
	page = ""
	if QueryCount < int(PerPage):
		page = str(Page_start) + " - " + str(QueryCount)
	else:
		page = str(Page_start) + " - " + str(Page_End)
	Test = (
		'<div class="col-md-12 brdr listContStyle pad2height30" ><div class="col-md-4 pager-numberofitem clear-padding"><span class="pager-number-of-items-item noofitem"  id="'
		+ str(table_id)
		+ '___NumberofItem" >'
		+ str(page)
		+ ' of </span><span class="pager-number-of-items-item fltltpad2mrg0" id="'
		+ str(table_id)
		+ '___totalItemCount"  >'
		+ str(QueryCount)
		+ '</span><div class="clear-padding fltltmrgtp3" ><div  class="pull-right vertmidtxtrht"><select onchange="PageFunctestChild(this,\'Quote\',\'\',\''
		+str(table_id)
		+'\')" id="'
		+ str(table_id)
		+ '___PageCountValue"  class="form-control wid65vermiddisinbmarl5"><option value="10" selected>10</option><option value="20">20</option><option value="50">50</option><option value="100">100</option><option value="200">200</option></select> </div></div></div><div class="col-xs-8 col-md-4  clear-padding disinpad10txtcen"  data-bind="visible: totalItemCount"><div class="clear-padding col-xs-12 col-sm-6 col-md-12 bor0" ><ul class="pagination pagination"><li class="disabled"><a href="#" onclick="FirstPageLoad_paginationChild(\'Quote\',\'\',\''  +str(table_id) +'\')"><i class="fa fa-caret-left font14whtbld" ></i><i class="fa fa-caret-left font14" ></i></a></li><li class="disabled"><a href="#" onclick="Previous12334Child(\'Quote\',\'\',\''
		+str(table_id)
		+'\')"><i class="fa fa-caret-left font14" ></i>PREVIOUS</a></li><li class="disabled"><a href="#" class="disabledPage" onclick="Next12334Child(\'Quote\',\'\',\''
		+str(table_id)
		+'\')">NEXT<i class="fa fa-caret-right font14" ></i></a></li><li class="disabled"><a href="#" onclick="LastPageLoad_paginationChild(\'Quote\',\'\',\''
		+str(table_id)
		+'\')" class="disabledPage"><i class="fa fa-caret-right font14"></i><i class="fa fa-caret-right font14whtbld"></i></a></li></ul></div> </div> <div class="col-md-4 pr_page_pad"> <span id="'
		+ str(table_id)
		+ '___page_count"  class="currentPage page_right_content">1</span><span class="page_right_content pad_rt_2">Page </span></div></div>'
	)

	#Trace.Write("456 Test ---->"+str(Test))

	if QueryCount < int(PerPage):
		PerPage = str(QueryCount)
	else:
		PerPage = str(PerPage)   
	if Page_End > QueryCount:
		Page_End = QueryCount
	else:
		Page_End = Page_End
	
	Action_Str = ""
	Action_Str += str(Page_start)+" - "
	Action_Str += str(Page_End)
	Action_Str += " of"
	
	return (
		table_header,
		data_list,
		table_id,
		filter_control_function,
		NORECORDS,
		dbl_clk_function,
		cv_list,
		filter_level_list,
		DropDownList,
		RelatedDrop_str,
		Test,
		Action_Str,
	)

def QuoteAssemblyPreventiveMaintainenceKitMaterialChild(recid, PerPage, PageInform, A_Keys, A_Values,ASSEMBLYID,EQUIPMENTID,KITID,KITNUMBER):
	# This function is used to construct the table inside the Equipment Parent Table.(As Nested Table).
	QueryCountObj = ""
	
	TreeParam = Product.GetGlobal("TreeParam")
	TreeParentParam = Product.GetGlobal("TreeParentLevel0")
	TreeSuperParentParam = Product.GetGlobal("TreeParentLevel1")
	TopSuperParentParam = Product.GetGlobal("TreeParentLevel2")
	if str(PerPage) == "" and str(PageInform) == "":
		Page_start = 1
		Page_End = 10
		PerPage = 10
		PageInform = "1___10___10"
	else:
		Page_start = int(PageInform.split("___")[0])
		Page_End = int(PageInform.split("___")[1])
		PerPage = PerPage
	QueryCount = ""
	chld_list = []
	FablocationId = Product.GetGlobal("TreeParam")
	ContractRecordId = Quote.GetGlobal("contract_quote_record_id")
	RevisionRecordId = Quote.GetGlobal("quote_revision_record_id")
	obj_idval = "SYOBJ_00948_SYOBJ_00948"
	obj_id1 = "SYOBJ-00948"
	objh_getid = Sql.GetFirst(
		"SELECT TOP 1  RECORD_ID  FROM SYOBJH (NOLOCK) WHERE SAPCPQ_ATTRIBUTE_NAME='" + str(obj_id1) + "'"
	)
	if objh_getid:
		obj_id1 = objh_getid.RECORD_ID
	objs_obj1 = Sql.GetFirst(
		"select CAN_ADD,CAN_EDIT,COLUMNS,CAN_DELETE from SYOBJR (NOLOCK) where OBJ_REC_ID = '" + str(obj_id1) + "' "
	)
	can_edit1 = str(objs_obj1.CAN_EDIT)
	can_add1 = str(objs_obj1.CAN_ADD)
	can_delete1 = str(objs_obj1.CAN_DELETE)
	##replacing space with '_' in recid
	if ' ' in recid:
		table_recid = recid.replace(' ','_')
	else:
			table_recid = recid
	table_id = "table_preventive_maintainence_child_"+str(table_recid) 
	table_header = (
		'<table id="'
		+ str(table_id)
		+ '" data-pagination="false" data-sortable="true" data-search-on-enter-key="true" data-filter-control="true" data-pagination-loop = "false" data-locale = "en-US" ><thead>'
	)
	Columns = [
		"QUOTE_SERVICE_COV_OBJ_ASS_PM_KIT_PARTS_RECORD_ID",
		"KIT_ID",
		"PART_NUMBER",
		"PART_DESCRIPTION",
		"QUANTITY",
		"TKM_FLAG",
	]
	Objd_Obj = Sql.GetList(
		"select FIELD_LABEL,API_NAME,LOOKUP_OBJECT,LOOKUP_API_NAME,DATA_TYPE,FORMULA_DATA_TYPE from SYOBJD (NOLOCK) where OBJECT_NAME = 'SAQSKP'"
	)
	attr_list = []
	attrs_datatype_dict = {}
	lookup_disply_list = []
	lookup_str = ""
	if Objd_Obj is not None:
		attr_list = {}
		for attr in Objd_Obj:
			attr_list[str(attr.API_NAME)] = str(attr.FIELD_LABEL)
			attrs_datatype_dict[str(attr.API_NAME)] = str(attr.DATA_TYPE)
			if attr.LOOKUP_API_NAME != "" and attr.LOOKUP_API_NAME is not None:
				lookup_disply_list.append(str(attr.API_NAME))
		checkbox_list = [inn.API_NAME for inn in Objd_Obj if inn.DATA_TYPE == "CHECKBOX"]
		numberlist = [inn.API_NAME for inn in Objd_Obj if inn.FORMULA_DATA_TYPE == "NUMBER"]
		lookup_list = {ins.LOOKUP_API_NAME: ins.API_NAME for ins in Objd_Obj}
	lookup_str = ",".join(list(lookup_disply_list))
	Parent_assembly_id = ""
	if TopSuperParentParam in ('Comprehensive Services','Complementary Products'):
		Parent_assembly_id = Sql.GetFirst(
			"select PM_ID from SAQSAP (NOLOCK) where QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}'  AND PM_ID = '{PreventiveMaintainenceId}' AND ASSEMBLY_ID = '{AssemblyId}' AND EQUIPMENT_ID = '{EquipmentId}'".format(
				ContractRecordId = Quote.GetGlobal("contract_quote_record_id"),
				RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"),
				PreventiveMaintainenceId = recid,
				AssemblyId = ASSEMBLYID,
				EquipmentId = EQUIPMENTID,
			)
		)
	elif TreeParentParam in ('Comprehensive Services','Complementary Products'):
		Parent_assembly_id = Sql.GetFirst("select PM_ID from SAQSAP (NOLOCK) where QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}'  AND PM_ID = '{PreventiveMaintainenceId}' ".format(ContractRecordId = Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"),PreventiveMaintainenceId = recid))	
	if Parent_assembly_id:
		Preventive_Maintainence_ID = Parent_assembly_id.PM_ID
		if TopSuperParentParam in ('Comprehensive Services','Complementary Products'):
			"""child_obj_recid = Sql.GetList(
				"select QUOTE_SERVICE_COV_OBJ_ASS_PM_KIT_PARTS_RECORD_ID,KIT_ID,PART_NUMBER,PART_DESCRIPTION,QUANTITY,TKM_FLAG from SAQSKP (NOLOCK) where PM_ID = '"
				+ str(recid)
				+ "' and QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' and ASSEMBLY_ID = '{AssemblyId}' ".format(
					ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),
					RevisionRecordId = Quote.GetGlobal("quote_revision_record_id")
					AssemblyId = ASSEMBLYID,
				)
			)"""
			child_obj_recid = Sql.GetList(
				"select top "
					+ str(PerPage)
					+ " * from (select ROW_NUMBER() OVER( ORDER BY QUOTE_SERVICE_COV_OBJ_ASS_PM_KIT_PARTS_RECORD_ID) AS ROW, QUOTE_SERVICE_COV_OBJ_ASS_PM_KIT_PARTS_RECORD_ID,KIT_ID,PART_NUMBER,PART_DESCRIPTION,QUANTITY,TKM_FLAG from SAQSKP (NOLOCK) where PM_ID = '"
					+ str(recid)
					+ "' and QUOTE_RECORD_ID = '"+str(ContractRecordId)+"' and QTEREV_RECORD_ID = '"
					+ str(RevisionRecordId)
					+ "' and ASSEMBLY_ID ='"
					+ str(ASSEMBLYID)+"' and EQUIPMENT_ID = '"+str(EQUIPMENTID)+"' and KIT_ID = '"+str(KITID)+"' and KIT_NUMBER = '"+str(KITNUMBER)+"') m where m.ROW BETWEEN "
					+ str(Page_start)
					+ " and "
					+ str(Page_End)
			)
			QueryCountObj = Sql.GetFirst(
			"select count(QUOTE_SERVICE_COV_OBJ_ASS_PM_KIT_PARTS_RECORD_ID) as cnt from SAQSKP (NOLOCK) where QUOTE_RECORD_ID = '"
			+ str(ContractRecordId)
			+ "' and QTEREV_RECORD_ID = '"
			+ str(RevisionRecordId)
			+ "' and PM_ID = '"
			+ str(Preventive_Maintainence_ID)
			+ "'and ASSEMBLY_ID = '"
			+ str(ASSEMBLYID)+"'and EQUIPMENT_ID = '"+str(EQUIPMENTID)+"'and KIT_ID = '"+str(KITID)+"' and KIT_NUMBER = '"+str(KITNUMBER)+"'")
		elif TreeParentParam in ('Comprehensive Services','Complementary Products'):
			child_obj_recid = Sql.GetList(
				"select top "
					+ str(PerPage)
					+ " * from (select ROW_NUMBER() OVER( ORDER BY QUOTE_SERVICE_COV_OBJ_ASS_PM_KIT_PARTS_RECORD_ID) AS ROW, QUOTE_SERVICE_COV_OBJ_ASS_PM_KIT_PARTS_RECORD_ID,KIT_ID,PART_NUMBER,PART_DESCRIPTION,QUANTITY,TKM_FLAG from SAQSKP (NOLOCK) where PM_ID = '"
					+ str(recid)
					+ "' and QUOTE_RECORD_ID = '"+str(ContractRecordId)+"' and QTEREV_RECORD_ID = '"
					+ str(RevisionRecordId)
					+ "' and KIT_ID = '"+str(KITID)+"' and KIT_NUMBER = '"+str(KITNUMBER)+"') m where m.ROW BETWEEN "
					+ str(Page_start)
					+ " and "
					+ str(Page_End)
			)
			QueryCountObj = Sql.GetFirst(
			"select count(QUOTE_SERVICE_COV_OBJ_ASS_PM_KIT_PARTS_RECORD_ID) as cnt from SAQSKP (NOLOCK) where QUOTE_RECORD_ID = '"
			+ str(ContractRecordId)
			+ "' and QTEREV_RECORD_ID = '"
			+ str(RevisionRecordId)
			+ "' and PM_ID = '"
			+ str(Preventive_Maintainence_ID)
			+ "' and KIT_ID = '"+str(KITID)+"' and KIT_NUMBER = '"+str(KITNUMBER)+"'")
		chld_list = []
		QueryCount = ""
		if QueryCountObj is not None:
			QueryCount = QueryCountObj.cnt
		# Data construction for table.
		for child in child_obj_recid:
			data_id = str(child.QUOTE_SERVICE_COV_OBJ_ASS_PM_KIT_PARTS_RECORD_ID) + "|Assemblies"
			chld_dict = {}
			Action_str1 = (
				'<div class="btn-group dropdown"><div class="dropdown" id="ctr_drop"><i data-toggle="dropdown" id="dropdownMenuButton" class="fa fa-sort-desc dropdown-toggle" aria-expanded="false"></i><ul class="dropdown-menu left" aria-labelledby="dropdownMenuButton"><li><a  data-toggle="modal" data-target="#cont_viewModalSection" id="'
				+ str(data_id)
				+ '" class="dropdown-item cur_sty" href="#"  onclick="cont_relatedlist_openview(this) ">VIEW</a></li>'
			)
			if can_edit1.upper() == "TRUE":
				Action_str1 += (
					'<li style="display:none" ><a data-toggle="modal" data-target="#cont_viewModalSection" id="'
					+ str(data_id)
					+ '"  class="dropdown-item cur_sty" href="#"  onclick="cont_relatedlist_openedit(this)">EDIT</a></li>'
				)
			if can_delete1.upper() == "TRUE":
				Action_str1 += '<li><a class="dropdown-item" data-target="#cont_viewModal_Material_Delete" data-toggle="modal" onclick="Material_delete_obj(this)" href="#">DELETE</a></li>'
			if can_add1.upper() == "TRUE":
				Action_str1 += '<li><a class="dropdown-item" data-target="#" data-toggle="modal" onclick="Material_clone_obj(this)" href="#">CLONE</a></li>'
			Action_str1 += "</ul></div></div>"

			# data formation in Dictonary format.

			chld_dict["ACTIONS"] = str(Action_str1)
			chld_dict["QUOTE_SERVICE_COV_OBJ_ASS_PM_KIT_PARTS_RECORD_ID"] = CPQID.KeyCPQId.GetCPQId(
				"SAQSKP", str(child.QUOTE_SERVICE_COV_OBJ_ASS_PM_KIT_PARTS_RECORD_ID)
			)
			chld_dict["KIT_ID"] = str(child.KIT_ID)
			chld_dict["PART_NUMBER"] = str(child.PART_NUMBER)
			chld_dict["PART_DESCRIPTION"] = str(child.PART_DESCRIPTION)
			chld_dict["QUANTITY"] = str(child.QUANTITY)
			chld_dict["TKM_FLAG"] = str(child.TKM_FLAG)
			chld_list.append(chld_dict)

	# Table formation.
	hyper_link = [""]
	table_header += "<tr>"
	table_header += (
		'<th data-field="ACTIONS"><div class="action_col">ACTIONS</div><button class="searched_button" id="Act_'
		+ str(table_id)
		+ '">Search</button></th>'
	)
	table_header += '<th data-field="SELECT" class="wid45" data-checkbox="true"></th>'
	for key, invs in enumerate(list(Columns)):
		invs = str(invs).strip()
		qstring = attr_list.get(str(invs)) or ""
		if qstring == "":
			qstring = invs.replace("_", " ")
		if checkbox_list is not None and invs in checkbox_list:
			table_header += (
				'<th  data-field="'
				+ str(invs)
				+ '" data-filter-control="input" data-align="center" data-formatter="CheckboxFieldRelatedList" data-sortable="true"><abbr title="'
				+ str(qstring)
				+ '">'
				+ str(qstring)
				+ "</abbr></th>"
			)
		elif hyper_link is not None and invs in hyper_link:
			table_header += (
				'<th data-field="'
				+ str(invs)
				+ '" data-filter-control="input" data-formatter="primaryListHyperLink" data-sortable="true"><abbr title="'
				+ str(qstring)
				+ '">'
				+ str(qstring)
				+ "</abbr></th>"
			)
		elif numberlist is not None and invs in numberlist:
			table_header += (
				'<th  data-field="'
				+ str(invs)
				+ '" data-filter-control="input" data-align="right" data-sortable="true"><abbr title="'
				+ str(qstring)
				+ '">'
				+ str(qstring)
				+ "</abbr></th>"
			)    
		else:
			table_header += (
				'<th data-field="'
				+ str(invs)
				+ '" data-filter-control="input" data-sortable="true"><abbr title="'
				+ str(qstring)
				+ '">'
				+ str(qstring)
				+ "</abbr></th>"
			)
	table_header += "</tr>"
	table_header += '</thead><tbody onclick="Table_Onclick_Scroll(this)"></tbody></table>'
	table_ids = "#" + str(table_id)
	filter_control_function = ""
	values_list = ""
	tbl_id = table_id
	for key, invs in enumerate(list(Columns)):
		table_ids = "#" + str(table_id)
		filter_clas = "#" + str(table_id) + " .bootstrap-table-filter-control-" + str(invs)
		values_list += "var " + str(invs) + ' = $("' + str(filter_clas) + '").val(); '
		values_list += "ATTRIBUTE_VALUEList.push(" + str(invs) + "); "
		tbl_id = str(table_id)
	filter_class = "#Act_" + str(table_id)
	filter_control_function += (
		'$("'
		+ filter_class
		+ '").click( function(){ var table_id = $(this).closest("table").attr("id"); ATTRIBUTE_VALUEList = []; '
		+ str(values_list)
		+ ' var attribute_value = $(this).val(); cpq.server.executeScript("CQNESTGRID", {"TABNAME":"Preventive Maintainence child Filter", "ACTION":"PRODUCT_ONLOAD_FILTER", "ATTRIBUTE_NAME": '
		+ str(list(Columns))
		+ ', "ATTRIBUTE_VALUE": ATTRIBUTE_VALUEList, "REC_ID":"'
		+ str(recid)
		+ '" , "ASSEMBLYID" : "'
		+ str(ASSEMBLYID)
		+'", "EQUIPMENTID" : "'
		+ str(EQUIPMENTID)
		+'","KITID" : "'+ str(KITID)+'","KITNUMBER" : "'+ str(KITNUMBER)+'"}, function(dataset) { data2 = dataset[1];  data1 = dataset[0]; data3 = dataset[2]; console.log("len ---->"+data1.length);  try { if(data1.length > 0) { $("#' + str(tbl_id) + '").bootstrapTable("load", data1 );$("#noRecDisp").remove(); if (document.getElementById("'+str(tbl_id) + '___totalItemCount")){document.getElementById("'+str(tbl_id)+ '___totalItemCount").innerHTML = data2;}  if (document.getElementById("'+str(tbl_id) + '___NumberofItem")) {document.getElementById("'+str(tbl_id)+ '___NumberofItem").innerHTML = data3;}} else{ $("#' + str(tbl_id) + '").bootstrapTable("load", data1  );$("#' + str(tbl_id) + '").after("<div id=\'noRecDisp\' class=\'noRecord\'>No Records to Display</div>"); $(".noRecord:not(:first)").remove(); if (document.getElementById("'+str(tbl_id) + '___totalItemCount")){document.getElementById("'+str(tbl_id)+ '___totalItemCount").innerHTML = data2;}  if (document.getElementById("'+str(tbl_id) + '___NumberofItem")) {document.getElementById("'+str(tbl_id)+ '___NumberofItem").innerHTML = data3;} }} catch(err){} }); filter_search_click();$(".JColResizer").mousedown(function(){ $("thead.fullHeadFirst").css("cssText","z-index: 2;border-top: 1px solid rgb(220, 220, 220);top: 154px;border-right: 0px !important;");$("thead.fullHeadSecond").css("display","none"); });$(".JColResizer").mouseup(function(){ var th_width_resize = [];$("#table_preventive_maintainence_child thead.fullHeadFirst tr th").each(function(index){var wid = $(this).css("width"); if(index ==0 || index ==1){th_width_resize.push("60px");}else{th_width_resize.push(wid);}}); $("thead.fullHeadFirst").css("cssText","position: fixed;z-index: 2;border-top: 1px solid rgb(220, 220, 220); top: 154px;border-right: 0px !important;");$("thead.fullHeadSecond").css("display","table-header-group");$("#table_preventive_maintainence_child thead.fullHeadFirst tr th").each(function(index){var num = th_width_resize[index].split("px");var numsp = parseInt(num[0]);numsp = numsp - 1;var make_str =numsp+"px"; var c = "width:"+make_str+";white-space: nowrap;overflow: hidden;text-overflow: ellipsis;";var d = "width:"+make_str+";"; $(this).css("cssText",c);$(this).children("div:first-child").css("cssText",c);$(this).children("div.fht-cell").css("cssText",d);});$("#table_preventive_maintainence_child thead.fullHeadSecond tr th").each(function(index){var num = th_width_resize[index].split("px");var numsp = parseInt(num[0]);numsp = numsp - 1;var make_str =numsp+"px"; var c = "width:"+make_str+";white-space: nowrap;overflow: hidden;text-overflow: ellipsis;";var d = "width:"+make_str+";"; $(this).css("cssText",c);$(this).children("div:first-child").css("cssText",c);$(this).children("div.fht-cell").css("cssText",d);}); });});'
	)    

	
	dbl_clk_function = (
	'$("'
	+ str(table_ids)
	+ '").on("all.bs.table", function (e, name, args) { $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); }); $("'
	+ str(table_ids)
	+ '\ th.bs-checkbox div.th-inner").before("<div style=\'padding:0; border-bottom: 1px solid #dcdcdc;\'>SELECT</div>"); $(".bs-checkbox input").addClass("custom"); $("'
	+ str(table_ids)
	+ "\").on('sort.bs.table', function (e, name, order) { console.log('sort.bs.table ============>', e); e.stopPropagation(); currenttab = $(\"ul#carttabs_head .active\").text().trim(); localStorage.setItem('"
	+ str(table_id)
	+ "_SortColumn', name); localStorage.setItem('"
	+ str(table_id)
	+ "_SortColumnOrder', order); PmEventsNestedContainerSorting(name, order, '"
	+ str(table_id)
	+ "','"+str(ASSEMBLYID)+"','"+str(EQUIPMENTID)+"'); }); "
	)
	

	NORECORDS = ""
	if len(chld_list) == 0:
		NORECORDS = "NORECORDS"

	ObjectName = "SAQSKP"
	DropDownList = []
	filter_level_list = []
	filter_clas_name = ""
	cv_list = []
	TableclassName = "form-control" + table_id
	for key, col_name in enumerate(list(Columns)):
		StringValue_list = []
		objss_obj = Sql.GetFirst(
			"SELECT API_NAME, DATA_TYPE, FORMULA_LOGIC FROM SYOBJD (NOLOCK) WHERE OBJECT_NAME='"
			+ str(ObjectName)
			+ "' and API_NAME = '"
			+ str(col_name)
			+ "'"
		)
		try:
			FORMULA_LOGIC = objss_obj.FORMULA_LOGIC.strip()
			FORMULA_col = FORMULA_LOGIC.split(" ")[1].strip()
			FORMULA_table = FORMULA_LOGIC.split(" ")[3].strip()
			ins_obj = Sql.GetFirst(
				"SELECT API_NAME, DATA_TYPE,PICKLIST FROM SYOBJD (NOLOCK) WHERE OBJECT_NAME='"
				+ str(FORMULA_table)
				+ "' and API_NAME = '"
				+ str(FORMULA_col)
				+ "'"
			)
			if str(objss_obj.PICKLIST).upper() == "TRUE":
				filter_level_data = "select"
				filter_clas_name = (
					'<div id = "'
					+ str(table_id)
					+ "_RelatedMutipleCheckBoxDrop_"
					+ str(key)
					+ '" class="form-control bootstrap-table-filter-control-'
					+ str(col_name)
					+ " RelatedMutipleCheckBoxDrop_"
					+ str(key)
					+ ' "></div>'
				)
				filter_level_list.append(filter_level_data)
			else:
				filter_level_data = "input"
				filter_clas_name = (
					'<input type="text" class="width100_vis form-control bootstrap-table-filter-control-'
					+ str(col_name)
					+ '">'
				)
				filter_level_list.append(filter_level_data)
		except:
			"""if str(objss_obj.PICKLIST).upper() == "TRUE":
				filter_level_data = "select"
				filter_clas_name = (
					'<div id = "'
					+ str(table_id)
					+ "_RelatedMutipleCheckBoxDrop_"
					+ str(key)
					+ '" class="form-control bootstrap-table-filter-control-'
					+ str(col_name)
					+ " RelatedMutipleCheckBoxDrop_"
					+ str(key)
					+ ' "></div>'
				)
				filter_level_list.append(filter_level_data)"""

			filter_level_data = "input"
			filter_clas_name = (
				'<input type="text" class="width100_vis form-control bootstrap-table-filter-control-' + str(col_name) + '">'
			)
			filter_level_list.append(filter_level_data)
		cv_list.append(filter_clas_name)
		if filter_level_data == "select":
			try:
				xcd = Sql.GetFirst(
					"SELECT (STUFF((SELECT DISTINCT ', ' + CAST("
					+ str(col_name)
					+ " AS CHAR(100)) FROM "
					+ str(ObjectName)
					+ " (NOLOCK) where QUOTE_SERVICE_COV_OBJ_ASS_PM_KIT_PARTS_RECORD_ID = '"
					+ str(recid)
					+ "' FOR XML PATH('') ), 1, 2, '')  ) AS StringValue"
				)
			except:
				xcd = Sql.GetFirst(
					"SELECT (STUFF((SELECT DISTINCT ', ' + CAST("
					+ str(col_name)
					+ " AS CHAR(100)) FROM "
					+ str(ObjectName)
					+ " (NOLOCK) FOR XML PATH('') ), 1, 2, '')  ) AS StringValue"
				)
			if str(xcd.StringValue) is not None and str(xcd.StringValue) != "":
				if str(xcd.StringValue).find(",") != -1:
					StringValue_list = [ins.strip() for ins in str(xcd.StringValue).split(",") if ins.strip() != ""]
				else:
					StringValue_list.append(str(xcd.StringValue))
			else:
				StringValue_list = [""]
			StringValue_list = list(set(StringValue_list))
			DropDownList.append(StringValue_list)
		elif filter_level_data == "checkbox":
			DropDownList.append(["True", "False"])
		else:
			DropDownList.append("")
	RelatedDrop_str = (
		"try { if( document.getElementById('"
		+ str(table_id)
		+ "') ) { var listws = document.getElementById('"
		+ str(table_id)
		+ "').getElementsByClassName('filter-control');  for (i = 0; i < listws.length; i++) { document.getElementById('"
		+ str(table_id)
		+ "').getElementsByClassName('filter-control')[i].innerHTML = datachld6[i];  } for (j = 0; j < listws.length; j++) { if (datachld7[j] == 'select') { if (data8[j]) { var dataAdapter = new $.jqx.dataAdapter(datachld8[j]); $('#"
		+ str(table_id)
		+ "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter, autoDropDownHeight: true }); } } } } }  catch(err) { setTimeout(function() { var listws = document.getElementById('"
		+ str(table_id)
		+ "').getElementsByClassName('filter-control');  for (i = 0; i < listws.length; i++) { document.getElementById('"
		+ str(table_id)
		+ "').getElementsByClassName('filter-control')[i].innerHTML = datachld6[i];  } for (j = 0; j < listws.length; j++) { if (datachld7[j] == 'select') { if (data8[j]) { var dataAdapter = new $.jqx.dataAdapter(datachld8[j]); $('#"
		+ str(table_id)
		+ "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter, autoDropDownHeight: true }); } } } }, 5000); } try { setTimeout(function(){ $('#"
		+ str(table_id)
		+ "').colResizable({ resizeMode:'overflow'}); }, 3000); } catch(err){}"
	)
	page = ""
	if QueryCount < int(PerPage):
		page = str(Page_start) + " - " + str(QueryCount)
	else:
		page = str(Page_start) + " - " + str(Page_End)
	#Trace.Write("page------"+str(page))    
	Test = (
		'<div class="col-md-12 brdr listContStyle pad2height30" ><div class="col-md-4 pager-numberofitem clear-padding"><span class="pager-number-of-items-item noofitem" id="'
		+ str(table_id)
		+ '___NumberofItem"  >'
		+ str(page)
		+ ' of</span><span class="pager-number-of-items-item fltltpad2mrg0" id="'
		+ str(table_id)
		+ '___totalItemCount" >'
		+ str(QueryCount)
		+ '</span><div class="clear-padding fltltmrgtp3" ><div  class="pull-right vertmidtxtrht"><select onchange="PageFunctestChild(this,\'Quote\',\'\',\'table_preventive_maintainence_child\')" id="'
		+ str(table_id)
		+ '___PageCountValue" class="form-control wid65vermiddisinbmarl5"><option value="10" selected>10</option><option value="20">20</option><option value="50">50</option><option value="100">100</option><option value="200">200</option></select> </div></div></div><div class="col-xs-8 col-md-4  clear-padding disinpad10txtcen"  data-bind="visible: totalItemCount"><div class="clear-padding col-xs-12 col-sm-6 col-md-12 bor0" ><ul class="pagination pagination"><li class="disabled"><a href="#" onclick="FirstPageLoad_paginationChild(\'Quote\',\'\',\''
		+str(table_id)
		+'\')"><i class="fa fa-caret-left font14whtbld" ></i><i class="fa fa-caret-left font14" ></i></a></li><li class="disabled"><a href="#" onclick="Previous12334Child(\'Quote\',\'\',\'' +str(table_id) +'\')"><i class="fa fa-caret-left font14" ></i>PREVIOUS</a></li><li class="disabled"><a href="#" class="disabledPage" onclick="Next12334Child(\'Quote\',\'\',\''+str(table_id)+'\')">NEXT<i class="fa fa-caret-right font14" ></i></a></li><li class="disabled"><a href="#" onclick="LastPageLoad_paginationChild(\'Quote\',\'\',\''
		+str(table_id)
		+'\')" class="disabledPage"><i class="fa fa-caret-right font14"></i><i class="fa fa-caret-right font14whtbld"></i></a></li></ul></div> </div> <div class="col-md-4 pr_page_pad"> <span id="'
		+ str(table_id)
		+ '___page_count" class="currentPage page_right_content">1</span><span class="page_right_content pad_rt_2">Page </span></div></div>'
	)
	#Trace.Write("4545 Test ---->"+str(Test))
	
	if QueryCount < int(PerPage):
		PerPage = str(QueryCount)
	else:
		PerPage = str(PerPage)   
	if Page_End > QueryCount:
		Page_End = QueryCount
	else:
		Page_End = Page_End
	
	Action_Str = ""
	Action_Str += str(Page_start)+" - "
	Action_Str += str(Page_End)
	Action_Str += " of"

	return (
		table_header,
		chld_list,
		table_id,
		filter_control_function,
		NORECORDS,
		dbl_clk_function,
		cv_list,
		filter_level_list,
		DropDownList,
		RelatedDrop_str,
		Test,
		Action_Str,
	)
##PREVENTIVE MAINTAINENCE GRID ENDS...
def QuoteAssemblyPreventiveMaintainenceParentFilter(ATTRIBUTE_NAME, ATTRIBUTE_VALUE,ASSEMBLYID,EQUIPMENTID,PerPage,PageInform):

	if str(PerPage) == "" and str(PageInform) == "":
		Page_start = 1
		Page_End = 10
		PerPage = 10
		PageInform = "1___10___10"
	else:
		Page_start = int(PageInform.split("___")[0])
		Page_End = int(PageInform.split("___")[1])
		PerPage = PerPage

	QueryCount = ""
	
	TreeParam = Product.GetGlobal("TreeParam")
	TreeParentParam = Product.GetGlobal("TreeParentLevel0")
	TreeSuperParentParam = Product.GetGlobal("TreeParentLevel1")
	TreeTopSuperParentParam = Product.GetGlobal("TreeParentLevel2")
	FablocationId = Product.GetGlobal("TreeParam")
	ContractRecordId = Quote.GetGlobal("contract_quote_record_id")
	RevisionRecordId = Quote.GetGlobal("quote_revision_record_id")
	ATTRIBUTE_VALUE_STR = ""
	Dict_formation = dict(zip(ATTRIBUTE_NAME, ATTRIBUTE_VALUE))
	for quer_key, quer_value in enumerate(Dict_formation):
		x_picklistcheckobj = Sql.GetFirst(
			"SELECT PICKLIST FROM SYOBJD (NOLOCK) WHERE OBJECT_NAME ='SAQSAP' AND API_NAME = '" + str(quer_value) + "'"
		)
		x_picklistcheck = str(x_picklistcheckobj.PICKLIST).upper()
		if Dict_formation.get(quer_value) != "":
			quer_values = str(Dict_formation.get(quer_value)).strip()
			if str(quer_values).upper() == "TRUE":
				quer_values = "TRUE"
			elif str(quer_values).upper() == "FALSE":
				quer_values = "FALSE"
			if str(quer_values).find(",") == -1:
				if x_picklistcheck == "TRUE":
					ATTRIBUTE_VALUE_STR += str(quer_value) + " = '" + str(quer_values) + "' and "
				else:
					ATTRIBUTE_VALUE_STR += str(quer_value) + " like '%" + str(quer_values) + "%' and "
			else:
				quer_values = quer_values.split(",")
				quer_values = tuple(list(quer_values))
				ATTRIBUTE_VALUE_STR += str(quer_value) + " in " + str(quer_values) + " and "
			if str(quer_value) == 'QUOTE_SERVICE_COV_OBJ_ASS_PM_KIT_RECORD_ID':                
				if str(str(quer_values)).find("-") == -1:                            
					ATTRIBUTE_VALUE_STR = (" CpqTableEntryId = '"+ str(quer_values)+ "' and ")                            
				else:
					xa_str = str(quer_values).split("-")[1]                            
					ATTRIBUTE_VALUE_STR = (" CpqTableEntryId = '"+ str(xa_str)+ "' and ")    

	data_list = []
	rec_id = "SYOBJ_00974"
	obj_id = "SYOBJ-00974"
	objh_getid = Sql.GetFirst(
		"SELECT TOP 1  RECORD_ID  FROM SYOBJH (NOLOCK) WHERE SAPCPQ_ATTRIBUTE_NAME='" + str(obj_id) + "'"
	)
	if objh_getid:
		obj_id = objh_getid.RECORD_ID
	objs_obj = Sql.GetFirst(
		"select CAN_ADD,CAN_EDIT,COLUMNS,CAN_DELETE from SYOBJR (NOLOCK) where OBJ_REC_ID = '" + str(obj_id) + "' "
	)
	can_edit = str(objs_obj.CAN_EDIT)
	can_clone = str(objs_obj.CAN_ADD)
	can_delete = str(objs_obj.CAN_DELETE)

	orderby = ""
	if SortColumn != '' and SortColumnOrder !='':
		orderby = SortColumn + " " + SortColumnOrder
	else:
		orderby = "QUOTE_SERVICE_COV_OBJ_ASS_PM_KIT_RECORD_ID"


	if ATTRIBUTE_VALUE is None or ATTRIBUTE_VALUE == "" or ATTRIBUTE_VALUE_STR is None or ATTRIBUTE_VALUE_STR == "":
		#Trace.Write("Empty searh --->")
		if TreeTopSuperParentParam == 'Comprehensive Services':
			parent_obj = Sql.GetList(
				"select top "+str(PerPage)+" QUOTE_SERVICE_COV_OBJ_ASS_PM_KIT_RECORD_ID,KIT_ID,KIT_NAME,PM_NAME,KIT_NUMBER,TKM_FLAG,PM_ID,ANNUAL_FREQUENCY_BASE,SSCM_PM_FREQUENCY,PM_FREQUENCY,CpqTableEntryId from SAQSAP (NOLOCK) where QUOTE_RECORD_ID = '"
				+ str(ContractRecordId)            
				+ "' and QTEREV_RECORD_ID = '"
				+ str(RevisionRecordId)
				+ "' and ASSEMBLY_ID = '"+str(ASSEMBLYID)+"' and EQUIPMENT_ID = '"+str(EQUIPMENTID)+"' ORDER BY "+str(orderby)+" "
			)
			Count = Sql.GetFirst("select count(*) as cnt from SAQSAP (NOLOCK) where QUOTE_RECORD_ID = '"
				+ str(ContractRecordId)            
				+ "' and QTEREV_RECORD_ID = '"
				+ str(RevisionRecordId)
				+ "' and ASSEMBLY_ID = '"+str(ASSEMBLYID)+"' and EQUIPMENT_ID = '"+str(EQUIPMENTID)+"' ")
		elif TreeParentParam == 'Comprehensive Services' or TreeParentParam == "Complementary Products":
			parent_obj = Sql.GetList(
				"select top "+str(PerPage)+" QUOTE_SERVICE_COV_OBJ_ASS_PM_KIT_RECORD_ID,EQUIPMENT_DESCRIPTION,EQUIPMENT_ID,SERIAL_NO,GOT_CODE,ASSEMBLY_ID,KIT_ID,KIT_NAME,PM_NAME,KIT_NUMBER,TKM_FLAG,PM_ID,ANNUAL_FREQUENCY_BASE,SSCM_PM_FREQUENCY,PM_FREQUENCY,CpqTableEntryId from SAQSAP (NOLOCK) where QUOTE_RECORD_ID = '"
				+ str(ContractRecordId)            
				+ "' and QTEREV_RECORD_ID = '"
				+ str(RevisionRecordId)
				+ "' AND SERVICE_ID = '"+str(TreeParam)+"' ORDER BY "+str(orderby)+" "
			)
			Count = Sql.GetFirst("select count(*) as cnt from SAQSAP (NOLOCK) where QUOTE_RECORD_ID = '"
				+ str(ContractRecordId)            
				+ "' and QTEREV_RECORD_ID = '"
				+ str(RevisionRecordId)
				+ "' AND SERVICE_ID = '"+str(TreeParam)+"' ")
		if Count:
			QueryCount = Count.cnt
	else:
		#Trace.Write("conditional searh --->")
		if TreeTopSuperParentParam == "Comprehensive Services" or TreeTopSuperParentParam == "Complementary Products":
			parent_obj = Sql.GetList(
				"select top "+str(PerPage)+" QUOTE_SERVICE_COV_OBJ_ASS_PM_KIT_RECORD_ID,KIT_ID,KIT_NAME,PM_NAME,KIT_NUMBER,PM_ID,ANNUAL_FREQUENCY_BASE,SSCM_PM_FREQUENCY,PM_FREQUENCY,TKM_FLAG from SAQSAP (NOLOCK) where "
				+ str(ATTRIBUTE_VALUE_STR)
				+ " 1=1 and QUOTE_RECORD_ID = '"
				+ str(ContractRecordId)
				+ "'  and QTEREV_RECORD_ID = '"
				+ str(RevisionRecordId)
				+ "' and ASSEMBLY_ID = '"+str(ASSEMBLYID)+"' and EQUIPMENT_ID = '"+str(EQUIPMENTID)+"' ORDER BY "+str(orderby)+" "
			)

			Count = Sql.GetFirst("select count(*) as cnt from SAQSAP (NOLOCK) where "
				+ str(ATTRIBUTE_VALUE_STR)
				+ " 1=1 and QUOTE_RECORD_ID = '"
				+ str(ContractRecordId)
				+ "' and QTEREV_RECORD_ID = '"
				+ str(RevisionRecordId)
				+ "' and ASSEMBLY_ID = '"+str(ASSEMBLYID)+"' and EQUIPMENT_ID = '"+str(EQUIPMENTID)+"' ")
			
		elif TreeParentParam == "Comprehensive Services" or TreeParentParam == "Complementary Products":
			parent_obj = Sql.GetList(
				"select top "+str(PerPage)+" QUOTE_SERVICE_COV_OBJ_ASS_PM_KIT_RECORD_ID,EQUIPMENT_DESCRIPTION,EQUIPMENT_ID,SERIAL_NO,GOT_CODE,ASSEMBLY_ID,KIT_ID,KIT_NAME,PM_NAME,KIT_NUMBER,PM_ID,ANNUAL_FREQUENCY_BASE,SSCM_PM_FREQUENCY,PM_FREQUENCY,TKM_FLAG from SAQSAP (NOLOCK) where "
				+ str(ATTRIBUTE_VALUE_STR)
				+ " 1=1 and QUOTE_RECORD_ID = '"
				+ str(ContractRecordId)
				+ "'  and QTEREV_RECORD_ID = '"
				+ str(RevisionRecordId)
				+ "'  AND SERVICE_ID = '"+str(TreeParam)+"' ORDER BY "+str(orderby)+" "
			)
			Count = Sql.GetFirst("select count(*) as cnt from SAQSAP (NOLOCK) where "
				+ str(ATTRIBUTE_VALUE_STR)
				+ " 1=1 and QUOTE_RECORD_ID = '"
				+ str(ContractRecordId)
				+ "' and QTEREV_RECORD_ID = '"
				+ str(RevisionRecordId)
				+ "' AND SERVICE_ID = '"+str(TreeParam)+"' ")
		if Count:
			QueryCount = Count.cnt



	for par in parent_obj:
		data_dict = {}
		data_id = str(par.QUOTE_SERVICE_COV_OBJ_ASS_PM_KIT_RECORD_ID) + "|Preventive Maintainence Master"

		Action_str = (
			'<div class="btn-group dropdown"><div class="dropdown" id="ctr_drop"><i data-toggle="dropdown" id="dropdownMenuButton" class="fa fa-sort-desc dropdown-toggle" aria-expanded="false"></i><ul class="dropdown-menu left" aria-labelledby="dropdownMenuButton"><li><a class="dropdown-item cur_sty" href="#" id="'
			+ str(data_id)
			+ '" onclick="Move_to_parent_obj(this)">VIEW</a></li>'
		)
		if can_edit.upper() == "TRUE":
			Action_str += (
				'<li style="display:none" ><a class="dropdown-item cur_sty" href="#" id="'
				+ str(data_id)
				+ '" onclick="Move_to_parent_obj_edit(this)">EDIT</a></li>'
			)
		if can_delete.upper() == "TRUE":
			Action_str += '<li><a class="dropdown-item" data-target="#cont_viewModal_Material_Delete" data-toggle="modal" onclick="Material_delete_obj(this)" href="#">DELETE</a></li>'
		if can_clone.upper() == "TRUE":
			Action_str += '<li><a class="dropdown-item" data-target="#" data-toggle="modal" onclick="Material_clone_obj(this)" href="#">CLONE</a></li>'

		Action_str += "</ul></div></div>"

		decimal_place = 2 
		my_format = "{:,." + str(decimal_place) + "f}"
		original_PM_frequency = str(my_format.format(round(float(par.SSCM_PM_FREQUENCY), int(decimal_place))))
		pm_frequency = str(my_format.format(round(float(par.PM_FREQUENCY), int(decimal_place))))

		data_dict["ACTIONS"] = str(Action_str)
		data_dict["QUOTE_SERVICE_COV_OBJ_ASS_PM_KIT_RECORD_ID"] = CPQID.KeyCPQId.GetCPQId("SAQSAP", str(par.QUOTE_SERVICE_COV_OBJ_ASS_PM_KIT_RECORD_ID))
		data_dict["KIT_ID"] = str(par.KIT_ID)
		data_dict["KIT_NAME"] = str(par.KIT_NAME)
		data_dict["KIT_NUMBER"] = str(par.KIT_NUMBER)
		data_dict["EQUIPMENT_DESCRIPTION"] = str(par.EQUIPMENT_DESCRIPTION)
		data_dict["EQUIPMENT_ID"] = str(par.EQUIPMENT_ID)
		data_dict["SERIAL_NO"] = str(par.SERIAL_NO)
		data_dict["GOT_CODE"] = str(par.GOT_CODE)
		data_dict["ASSEMBLY_ID"] = str(par.ASSEMBLY_ID)
		data_dict["PM_ID"] = str(par.PM_ID)
		data_dict["PM_NAME"] = str(par.PM_NAME)
		data_dict["ANNUAL_FREQUENCY_BASE"] = str(par.ANNUAL_FREQUENCY_BASE)
		data_dict["SSCM_PM_FREQUENCY"] = str(original_PM_frequency)
		data_dict["PM_FREQUENCY"] = str(pm_frequency)
		data_dict["TKM_FLAG"] = str(par.TKM_FLAG)
		data_list.append(data_dict)

	page = ""
	if QueryCount < int(PerPage):
		page = str(Page_start) + " - " + str(QueryCount) + " of "
	else:
		page = str(Page_start) + " - " + str(Page_End)+ " of "
	# Trace.Write("QuoteAssemblyPreventiveMaintainenceParentFilter QueryCount --->"+str(QueryCount))
	# Trace.Write("QuoteAssemblyPreventiveMaintainenceParentFilter page --->"+str(page))

	return data_list,QueryCount,page

def QuoteAssemblyPreventiveMaintainenceKitMaterialChildFilter(ATTRIBUTE_NAME, ATTRIBUTE_VALUE, RECID,ASSEMBLYID,EQUIPMENTID,KITID,KITNUMBER,PerPage,PageInform):    
	FablocationId = Product.GetGlobal("TreeParam")
	ContractRecordId = Quote.GetGlobal("contract_quote_record_id")
	RevisionRecordId = Quote.GetGlobal("quote_revision_record_id")
	obj_id1 = "SYOBJ-00948"
	objh_getid = Sql.GetFirst(
		"SELECT TOP 1  RECORD_ID  FROM SYOBJH (NOLOCK) WHERE SAPCPQ_ATTRIBUTE_NAME='" + str(obj_id1) + "'"
	)
	if objh_getid:
		obj_id1 = objh_getid.RECORD_ID
	objs_obj1 = Sql.GetFirst(
		"select CAN_ADD,CAN_EDIT,COLUMNS,CAN_DELETE from SYOBJR (NOLOCK) where OBJ_REC_ID = '" + str(obj_id1) + "' "
	)
	can_edit1 = str(objs_obj1.CAN_EDIT)
	can_clone1 = str(objs_obj1.CAN_ADD)
	can_delete1 = str(objs_obj1.CAN_DELETE)
	recid = str(RECID)

	if str(PerPage) == "" and str(PageInform) == "":
		Page_start = 1
		Page_End = 10
		PerPage = 10
		PageInform = "1___10___10"
	else:
		Page_start = int(PageInform.split("___")[0])
		Page_End = int(PageInform.split("___")[1])
		PerPage = PerPage
	QueryCount = ""
	orderby = ""
	if SortColumn != '' and SortColumnOrder !='':
		orderby = SortColumn + " " + SortColumnOrder
	else:
		orderby = "QUOTE_SERVICE_COV_OBJ_ASS_PM_KIT_PARTS_RECORD_ID"

	ATTRIBUTE_VALUE_STR = ""
	Dict_formation = dict(zip(ATTRIBUTE_NAME, ATTRIBUTE_VALUE))
	for quer_key, quer_value in enumerate(Dict_formation):
		if Dict_formation.get(quer_value) != "":
			quer_values = str(Dict_formation.get(quer_value)).strip()
			if str(quer_values).find(",") == -1:
				ATTRIBUTE_VALUE_STR += str(quer_value) + " like '%" + str(quer_values) + "%' and "
			else:
				quer_values = quer_values.split(",")
				quer_values = tuple(list(quer_values))
				ATTRIBUTE_VALUE_STR += str(quer_value) + " in " + str(quer_values) + " and "
	if ATTRIBUTE_VALUE is None or ATTRIBUTE_VALUE == "" or ATTRIBUTE_VALUE_STR is None or ATTRIBUTE_VALUE_STR == "":
		child_obj_recid = Sql.GetList(
			"select top "+str(PerPage)+" QUOTE_SERVICE_COV_OBJ_ASS_PM_KIT_PARTS_RECORD_ID,PM_ID,KIT_ID,PART_NUMBER,TKM_FLAG,PART_DESCRIPTION,QUANTITY from SAQSKP (NOLOCK) where PM_ID = '"
			+ str(recid)
			+ "' and QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' and ASSEMBLY_ID = '{AssemblyId}' and EQUIPMENT_ID = '{EquipmentId}' and KIT_ID = '{kitid}' and KIT_NUMBER = '{kitnumber}' ORDER BY {ord_by}".format(
				ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),
				RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"),
				AssemblyId = ASSEMBLYID,
				EquipmentId = EQUIPMENTID,
				kitid = KITID,
				kitnumber = KITNUMBER,
				ord_by = orderby
			)
		)

		QueryCountObj = Sql.GetFirst(
				"select count(*) as cnt from SAQSKP (NOLOCK) where PM_ID = '"
			+ str(recid)
			+ "' and QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}'and ASSEMBLY_ID = '{AssemblyId}' and EQUIPMENT_ID = '{EquipmentId}' and KIT_ID = '{kitid}' and KIT_NUMBER = '{kitnumber}' ".format(
				ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),
				RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"),
				AssemblyId = ASSEMBLYID,
				EquipmentId = EQUIPMENTID,
				kitid = KITID,
				kitnumber = KITNUMBER
			))
		if QueryCountObj is not None:
			QueryCount = QueryCountObj.cnt


	else:
		child_obj_recid = Sql.GetList(
			"select top "+str(PerPage)+"  * from SAQSKP (NOLOCK) where PM_ID = '"
			+ str(recid)
			+ "' and "
			+ str(ATTRIBUTE_VALUE_STR)
			+ " 1=1 and QUOTE_RECORD_ID = '"
			+ str(ContractRecordId)
			+ "' and QTEREV_RECORD_ID = '"
			+ str(RevisionRecordId)
			+ "'and  ASSEMBLY_ID = '"
			+ str(ASSEMBLYID)
			+ "'and EQUIPMENT_ID = '"+str(EQUIPMENTID)+"' and KIT_ID = '"+str(KITID)+"' and KIT_NUMBER = '"+str(KITNUMBER)+"' ORDER BY "+str(orderby)+" "
		)

		QueryCountObj = Sql.GetFirst(
				"select count(*) as cnt from SAQSKP (NOLOCK) where PM_ID = '"
			+ str(recid)
			+ "' and "
			+ str(ATTRIBUTE_VALUE_STR)
			+ " 1=1 and QUOTE_RECORD_ID = '"
			+ str(ContractRecordId)
			+ "' and QTEREV_RECORD_ID = '"
			+ str(RevisionRecordId)
			+ "' and  ASSEMBLY_ID = '"
			+ str(ASSEMBLYID)
			+ "'and EQUIPMENT_ID = '"+str(EQUIPMENTID)+"' and KIT_ID = '"+str(KITID)+"' and KIT_NUMBER = '"+str(KITNUMBER)+"' ")
		if QueryCountObj is not None:
			QueryCount = QueryCountObj.cnt


	chld_list = []
	# Data construction for table.
	for child in child_obj_recid:
		'''cld = Sql.GetFirst(
			"select QUOTE_SERVICE_COV_OBJ_ASS_PM_KIT_PARTS_RECORD_ID,KIT_ID,PART_NUMBER,TKM_FLAG,PART_DESCRIPTION,QUANTITY from SAQSKP (NOLOCK) where PM_ID = '{PreventiveMaintainenceId}' and QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}'
				and ASSEMBLY_ID = '{AssemblyId}' and EQUIPMENT_ID = '{EquipmentId}' ".format(
				PreventiveMaintainenceId = child.PM_ID,
				ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),
				RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"),
				AssemblyId = ASSEMBLYID,
				EquipmentId = EQUIPMENTID,
			)
		)'''
		if 1:
			chld_dict = {}
			data_id = str(child.QUOTE_SERVICE_COV_OBJ_ASS_PM_KIT_PARTS_RECORD_ID) + "|SAQSKP"
			Action_str1 = (
				'<div class="btn-group dropdown"><div class="dropdown" id="ctr_drop"><i data-toggle="dropdown" id="dropdownMenuButton" class="fa fa-sort-desc dropdown-toggle" aria-expanded="false"></i><ul class="dropdown-menu left" aria-labelledby="dropdownMenuButton"><li><a  data-toggle="modal" data-target="#cont_viewModalSection" id="'
				+ str(data_id)
				+ '" class="dropdown-item cur_sty" href="#"  onclick="cont_relatedlist_openview(this) ">VIEW</a></li>'
			)
			if can_edit1.upper() == "TRUE" and Lock_val.upper() != "TRUE":
				Action_str1 += (
					'<li style="display:none" ><a data-toggle="modal" data-target="#cont_viewModalSection" id="'
					+ str(data_id)
					+ '"  class="dropdown-item cur_sty" href="#"  onclick="cont_relatedlist_openedit(this)">EDIT</a></li>'
				)
			if can_delete1.upper() == "TRUE":
				Action_str1 += '<li><a class="dropdown-item" data-target="#cont_viewModal_Material_Delete" data-toggle="modal" onclick="Material_delete_obj(this)" href="#">DELETE</a></li>'
			if can_clone1.upper() == "TRUE":
				Action_str1 += '<li><a class="dropdown-item" data-target="#" data-toggle="modal" onclick="Material_clone_obj(this)" href="#">CLONE</a></li>'
			Action_str1 += "</ul></div></div>"

			# data formation in Dictonary format.
			chld_dict["ACTIONS"] = str(Action_str1)
			chld_dict["QUOTE_SERVICE_COV_OBJ_ASS_PM_KIT_PARTS_RECORD_ID"] = CPQID.KeyCPQId.GetCPQId("SAQSKP", str(child.QUOTE_SERVICE_COV_OBJ_ASS_PM_KIT_PARTS_RECORD_ID))
			chld_dict["KIT_ID"] = str(child.KIT_ID)
			chld_dict["PART_NUMBER"] = str(child.PART_NUMBER)
			chld_dict["PART_DESCRIPTION"] = str(child.PART_DESCRIPTION)
			chld_dict["QUANTITY"] = str(child.QUANTITY)
			chld_dict["TKM_FLAG"] = str(child.TKM_FLAG)
			chld_list.append(chld_dict)
	#return chld_list
	page = ""
	if QueryCount < int(PerPage):
		page = str(Page_start) + " - " + str(QueryCount) + " of "
	else:
		page = str(Page_start) + " - " + str(Page_End)+ " of "
	#return data_list, QueryCount, page
	# Trace.Write("GetCovObjChildFilter data_list --->"+str(chld_list))
	# Trace.Write("GetCovObjChildFilter QueryCount ---->"+str(QueryCount))
	# Trace.Write("GetCovObjChildFilter page --->"+str(page))
	return chld_list, QueryCount, page


def GetAssembliesMaster(PerPage, PageInform, A_Keys, A_Values):
	if str(PerPage) == "" and str(PageInform) == "":
		Page_start = 1
		Page_End = 10
		PerPage = 10
		PageInform = "1___10___10"
	else:
		Page_start = int(PageInform.split("___")[0])
		Page_End = int(PageInform.split("___")[1])
		PerPage = PerPage
	ContractRecordId = Quote.GetGlobal("contract_quote_record_id")
	RevisionRecordId = Quote.GetGlobal("quote_revision_record_id")
	# FablocationId = Product.GetGlobal("TreeParam")
	data_list = []
	obj_idval = "SYOBJ_00904_SYOBJ_00904"
	rec_id = "SYOBJ_00904"
	obj_id = "SYOBJ-00904"
	objh_getid = Sql.GetFirst(
		"SELECT TOP 1  RECORD_ID  FROM SYOBJH (NOLOCK) WHERE SAPCPQ_ATTRIBUTE_NAME='" + str(obj_id) + "'"
	)
	if objh_getid:
		obj_id = objh_getid.RECORD_ID
	objs_obj = Sql.GetFirst(
		"select CAN_ADD,CAN_EDIT,COLUMNS,CAN_DELETE from SYOBJR (NOLOCK) where OBJ_REC_ID = '" + str(obj_id) + "' "
	)
	can_edit = str(objs_obj.CAN_EDIT)
	can_add = str(objs_obj.CAN_ADD)
	can_delete = str(objs_obj.CAN_DELETE)
	table_id = "table_assemblies"
	table_header = (
		'<table id="'
		+ str(table_id)
		+ '"  data-pagination="false" data-sortable="true" data-search-on-enter-key="true" data-filter-control="true" data-pagination-loop = "false" data-locale = "en-US" ><thead>'
	)
	Columns = [
		"QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID",
		"EQUIPMENTCATEGORY_ID",
		"EQUIPMENT_ID",
		"SERIAL_NO",
		"CUSTOMER_TOOL_ID",
		"GREENBOOK",
		"EQUIPMENT_STATUS",
		"EQUIPMENT_DESCRIPTION",
		"MNT_PLANT_ID",
		"FABLOCATION_ID",
		"WARRANTY_START_DATE",
		"WARRANTY_END_DATE"
	]
	Objd_Obj = Sql.GetList(
		"select FIELD_LABEL,API_NAME,LOOKUP_OBJECT,LOOKUP_API_NAME,DATA_TYPE from SYOBJD (NOLOCK) where OBJECT_NAME = 'SAQSCO'"
	)
	attr_list = []
	attrs_datatype_dict = {}
	lookup_disply_list = []
	lookup_str = ""
	if Objd_Obj is not None:
		attr_list = {}
		for attr in Objd_Obj:
			attr_list[str(attr.API_NAME)] = str(attr.FIELD_LABEL)
			attrs_datatype_dict[str(attr.API_NAME)] = str(attr.DATA_TYPE)
			if attr.LOOKUP_API_NAME != "" and attr.LOOKUP_API_NAME is not None:
				lookup_disply_list.append(str(attr.API_NAME))
		checkbox_list = [inn.API_NAME for inn in Objd_Obj if inn.DATA_TYPE == "CHECKBOX"]
		lookup_list = {ins.LOOKUP_API_NAME: ins.API_NAME for ins in Objd_Obj}
	lookup_str = ",".join(list(lookup_disply_list))

	Qstr = (
		"select top "
		+ str(PerPage)
		+ " * from ( select top 10 ROW_NUMBER() OVER( ORDER BY QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID) AS ROW, QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,EQUIPMENT_ID,EQUIPMENT_DESCRIPTION,SERIAL_NO,GREENBOOK,FABLOCATION_ID,WARRANTY_END_DATE,WARRANTY_START_DATE,MNT_PLANT_ID,EQUIPMENT_STATUS,CUSTOMER_TOOL_ID,EQUIPMENTCATEGORY_ID,WARRANTY_END_DATE_ALERT from SAQSCO (NOLOCK) where QUOTE_RECORD_ID = '"
		+ str(ContractRecordId)
		+ "'"
		+ "and QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID = '"
		+ str(CURR_REC_ID)
		+ "' and QTEREV_RECORD_ID = '"
		+ str(RevisionRecordId)
		+ "') m where m.ROW BETWEEN "
		+ str(Page_start)
		+ " and "
		+ str(Page_End)
	)
	QueryCount = ""
	QueryCountObj = Sql.GetFirst(
		"select count(QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID) as cnt from SAQSCO (NOLOCK) where QUOTE_RECORD_ID = '"
		+ str(ContractRecordId)
		+ "'"
		+ " and QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID = '"
		+ str(CURR_REC_ID)
		+ "' and QTEREV_RECORD_ID = '"
		+ str(RevisionRecordId)
		+ "'"
	)
	if QueryCountObj is not None:
		QueryCount = QueryCountObj.cnt
	parent_obj = Sql.GetList(Qstr)
	for par in parent_obj:
		data_id = str(par.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID) + "|SAQSCO Key"

		Action_str = (
			'<div class="btn-group dropdown"><div class="dropdown" id="ctr_drop"><i data-toggle="dropdown" id="dropdownMenuButton" class="fa fa-sort-desc dropdown-toggle" aria-expanded="false"></i><ul class="dropdown-menu left" aria-labelledby="dropdownMenuButton"><li><a class="dropdown-item cur_sty" href="#" id="'
			+ str(data_id)
			+ '" onclick="Move_to_parent_obj(this)">VIEW</a></li>'
		)
		"""if can_edit.upper() == "TRUE":
			Action_str += (
				'<li style="display:none" ><a class="dropdown-item cur_sty" href="#" id="'
				+ str(data_id)
				+ '" onclick="Move_to_parent_obj_edit(this)">EDIT</a></li>'
			)
		if can_delete.upper() == "TRUE":
			Action_str += '<li><a class="dropdown-item" data-target="#cont_viewModal_Material_Delete" data-toggle="modal" onclick="Material_delete_obj(this)" href="#">DELETE</a></li>'
		if can_add.upper() == "TRUE" and par.MARKET_TYPE == "NON MARKET BASED" and par.MODEL_TYPE != "COST PLUS":
			Action_str += (
				'<li><a class="dropdown-item" id="'
				+ str(data_id)
				+ '" data-target="#" data-toggle="modal" onclick="Pricebook_clone_obj(this)" href="#">CLONE</a></li>'
			)"""
		Action_str += "</ul></div></div>"

		# Data formation in dictonary format.
		## hyperlink
		data_dict = {}
		data_dict["ids"] = str(data_id)
		data_dict["ACTIONS"] = str(Action_str)
		data_dict["QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID"] = CPQID.KeyCPQId.GetCPQId(
			"SAQSCO", str(par.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID)
		)
		data_dict["EQUIPMENT_ID"] = str(par.EQUIPMENT_ID)
		data_dict["EQUIPMENT_DESCRIPTION"] = str(par.EQUIPMENT_DESCRIPTION)
		data_dict["FABLOCATION_ID"] = str(par.FABLOCATION_ID)
		data_dict["GREENBOOK"] = str(par.GREENBOOK)
		data_dict["SERIAL_NO"] = str(par.SERIAL_NO)
		data_dict["EQUIPMENTCATEGORY_ID"] = str(par.EQUIPMENTCATEGORY_ID)
		data_dict["CUSTOMER_TOOL_ID"] = str(par.CUSTOMER_TOOL_ID)
		data_dict["EQUIPMENT_STATUS"] = str(par.EQUIPMENT_STATUS)
		data_dict["MNT_PLANT_ID"] = str(par.MNT_PLANT_ID)
		data_dict["WARRANTY_START_DATE"] = str(par.WARRANTY_START_DATE)
		data_dict["WARRANTY_END_DATE"] = str(par.WARRANTY_END_DATE)
		data_list.append(data_dict)

	hyper_link = ["QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID"]
	table_header += "<tr>"
	table_header += (
		'<th data-field="ACTIONS"><div class="action_col">ACTIONS</div><button class="searched_button" id="Act_'
		+ str(table_id)
		+ '">Search</button></th>'
	)
	table_header += '<th data-field="SELECT" class="wid45" data-checkbox="true"></th>'
	for key, invs in enumerate(list(Columns)):
		invs = str(invs).strip()
		qstring = attr_list.get(str(invs)) or ""
		if qstring == "":
			qstring = invs.replace("_", " ")
		if checkbox_list is not None and invs in checkbox_list:
			table_header += (
				'<th  data-field="'
				+ str(invs)
				+ '" data-filter-control="input" data-align="center" data-formatter="CheckboxFieldRelatedList" data-sortable="true"><abbr title="'
				+ str(qstring)
				+ '">'
				+ str(qstring)
				+ "</abbr></th>"
			)
		elif hyper_link is not None and invs in hyper_link:
			table_header += (
				'<th data-field="'
				+ str(invs)
				+ '" data-filter-control="input" data-formatter="ToolDetailHyperLink" data-sortable="true"><abbr title="'
				+ str(qstring)
				+ '">'
				+ str(qstring)
				+ "</abbr></th>"
			)
		else:            
			table_header += (
				'<th  data-field="'
				+ str(invs)
				+ '" data-filter-control="input" data-sortable="true"><abbr title="'
				+ str(qstring)
				+ '">'
				+ str(qstring)
				+ "</abbr></th>"
			)
	table_header += "</tr>"
	table_header += '</thead><tbody onclick="Table_Onclick_Scroll(this)"></tbody></table>'
	table_ids = "#" + str(table_id)
	filter_control_function = ""
	values_list = ""
	for key, invs in enumerate(list(Columns)):
		table_ids = "#" + str(table_id)
		filter_clas = "#" + str(table_id) + " .bootstrap-table-filter-control-" + str(invs)
		values_list += "var " + str(invs) + ' = $("' + str(filter_clas) + '").val(); '
		values_list += "ATTRIBUTE_VALUEList.push(" + str(invs) + "); "
	filter_class = "#Act_" + str(table_id)
	filter_control_function += (
		'$("'
		+ filter_class
		+ '").click( function(){ var table_id = $(this).closest("table").attr("id"); ATTRIBUTE_VALUEList = []; '
		+ str(values_list)
		+ ' var attribute_value = $(this).val(); cpq.server.executeScript("CQNESTGRID", {"TABNAME":"Assemblies Parent", "ACTION":"PRODUCT_ONLOAD_FILTER", "ATTRIBUTE_NAME": '
		+ str(list(Columns))
		+ ', "ATTRIBUTE_VALUE": ATTRIBUTE_VALUEList }, function(data) { $("'
		+ str(table_ids)
		+ '").bootstrapTable("load", data ); }); filter_search_click();$(".JColResizer").mousedown(function(){ $("thead.fullHeadFirst").css("cssText","z-index: 2;border-top: 1px solid rgb(220, 220, 220);top: 154px;border-right: 0px !important;");$("thead.fullHeadSecond").css("display","none"); });$(".JColResizer").mouseup(function(){ var th_width_resize = [];$("#table_assemblies_parent thead.fullHeadFirst tr th").each(function(index){var wid = $(this).css("width"); if(index ==0 || index ==1){th_width_resize.push("60px");}else{th_width_resize.push(wid);}}); $("thead.fullHeadFirst").css("cssText","position: fixed;z-index: 2;border-top: 1px solid rgb(220, 220, 220); top: 154px;border-right: 0px !important;");$("thead.fullHeadSecond").css("display","table-header-group");$("#table_assemblies_parent thead.fullHeadFirst tr th").each(function(index){var num = th_width_resize[index].split("px");var numsp = parseInt(num[0]);numsp = numsp - 1;var make_str =numsp+"px"; var c = "width:"+make_str+";white-space: nowrap;overflow: hidden;text-overflow: ellipsis;";var d = "width:"+make_str+";"; $(this).css("cssText",c);$(this).children("div:first-child").css("cssText",c);$(this).children("div.fht-cell").css("cssText",d);});$("#table_assemblies_parent thead.fullHeadSecond tr th").each(function(index){var num = th_width_resize[index].split("px");var numsp = parseInt(num[0]);numsp = numsp - 1;var make_str =numsp+"px"; var c = "width:"+make_str+";white-space: nowrap;overflow: hidden;text-overflow: ellipsis;";var d = "width:"+make_str+";"; $(this).css("cssText",c);$(this).children("div:first-child").css("cssText",c);$(this).children("div.fht-cell").css("cssText",d);}); });});'
	)
	dbl_clk_function = (
		'$("'
		+ str(table_ids)
		+ '").on("all.bs.table", function (e, name, args) { $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); }); $("'
		+ str(table_ids)
		+ '\ th.bs-checkbox div.th-inner").before("<div style=\'padding:0; border-bottom: 1px solid #dcdcdc;\'>SELECT</div>"); $(".bs-checkbox input").addClass("custom");$(".bs-checkbox input").after("<span class=\'lbl\'></span>");'
		)
	NORECORDS = ""
	if len(data_list) == 0:
		NORECORDS = "NORECORDS"

	ObjectName = "SAQSCO"
	DropDownList = []
	filter_level_list = []
	filter_clas_name = ""
	cv_list = []
	TableclassName = "form-control" + table_id
	for key, col_name in enumerate(list(Columns)):
		StringValue_list = []
		objss_obj = Sql.GetFirst(
			"SELECT API_NAME, DATA_TYPE, FORMULA_LOGIC, PICKLIST FROM SYOBJD (NOLOCK) WHERE OBJECT_NAME='"
			+ str(ObjectName)
			+ "' and API_NAME = '"
			+ str(col_name)
			+ "'"
		)
		try:
			FORMULA_LOGIC = objss_obj.FORMULA_LOGIC.strip()
			FORMULA_col = FORMULA_LOGIC.split(" ")[1].strip()
			FORMULA_table = FORMULA_LOGIC.split(" ")[3].strip()
			ins_obj = Sql.GetFirst(
				"SELECT API_NAME, DATA_TYPE,PICKLIST FROM SYOBJD (NOLOCK) WHERE OBJECT_NAME='"
				+ str(FORMULA_table)
				+ "' and API_NAME = '"
				+ str(FORMULA_col)
				+ "'"
			)
			if str(objss_obj.PICKLIST).upper() == "TRUE":
				filter_level_data = "select"
				filter_clas_name = (
					'<div id = "'
					+ str(table_id)
					+ "_RelatedMutipleCheckBoxDrop_"
					+ str(key)
					+ '" class="form-control bootstrap-table-filter-control-'
					+ str(col_name)
					+ " RelatedMutipleCheckBoxDrop_"
					+ str(key)
					+ ' "></div>'
				)
				filter_level_list.append(filter_level_data)
			else:
				filter_level_data = "input"
				filter_clas_name = (
					'<input type="text" class="width100_vis form-control bootstrap-table-filter-control-'
					+ str(col_name)
					+ '">'
				)
				filter_level_list.append(filter_level_data)
		except:
			"""if str(objss_obj.PICKLIST).upper() == "TRUE":
				filter_level_data = "select"
				filter_clas_name = (
					'<div id = "'
					+ str(table_id)
					+ "_RelatedMutipleCheckBoxDrop_"
					+ str(key)
					+ '" class="form-control bootstrap-table-filter-control-'
					+ str(col_name)
					+ " RelatedMutipleCheckBoxDrop_"
					+ str(key)
					+ ' "></div>'
				)
				filter_level_list.append(filter_level_data)"""

			filter_level_data = "input"
			filter_clas_name = (
				'<input type="text" class="width100_vis form-control bootstrap-table-filter-control-' + str(col_name) + '">'
			)
			filter_level_list.append(filter_level_data)
		cv_list.append(filter_clas_name)
		if filter_level_data == "select":
			try:
				xcd = Sql.GetFirst(
					"SELECT (STUFF((SELECT DISTINCT ', ' + CAST("
					+ str(col_name)
					+ " AS CHAR(100)) FROM "
					+ str(ObjectName)
					+ " (NOLOCK) FOR XML PATH('') ), 1, 2, '')  ) AS StringValue"
				)
			except:
				xcd = Sql.GetFirst(
					"SELECT (STUFF((SELECT DISTINCT ', ' + CAST("
					+ str(col_name)
					+ " AS CHAR(100)) FROM "
					+ str(ObjectName)
					+ " (NOLOCK) FOR XML PATH('') ), 1, 2, '')  ) AS StringValue"
				)
			if str(xcd.StringValue) is not None and str(xcd.StringValue) != "":
				if str(xcd.StringValue).find(",") != -1:
					StringValue_list = [ins.strip() for ins in str(xcd.StringValue).split(",") if ins.strip() != ""]
				else:
					StringValue_list.append(str(xcd.StringValue))
			else:
				StringValue_list = [""]
			StringValue_list = list(set(StringValue_list))
			DropDownList.append(StringValue_list)
		elif filter_level_data == "checkbox":
			DropDownList.append(["True", "False"])
		else:
			DropDownList.append("")
	RelatedDrop_str = (
		"try { if( document.getElementById('"
		+ str(table_id)
		+ "') ) { var listws = document.getElementById('"
		+ str(table_id)
		+ "').getElementsByClassName('filter-control');  for (i = 0; i < listws.length; i++) { document.getElementById('"
		+ str(table_id)
		+ "').getElementsByClassName('filter-control')[i].innerHTML = data6[i];  } for (j = 0; j < listws.length; j++) { if (data7[j] == 'select') { if (data8[j]) { var dataAdapter = new $.jqx.dataAdapter(data8[j]); $('#"
		+ str(table_id)
		+ "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter, autoDropDownHeight: true }); } } } } }  catch(err) { setTimeout(function() { var listws = document.getElementById('"
		+ str(table_id)
		+ "').getElementsByClassName('filter-control');  for (i = 0; i < listws.length; i++) { document.getElementById('"
		+ str(table_id)
		+ "').getElementsByClassName('filter-control')[i].innerHTML = data6[i];  } for (j = 0; j < listws.length; j++) { if (data7[j] == 'select') { if (data8[j]) { var dataAdapter = new $.jqx.dataAdapter(data8[j]); $('#"
		+ str(table_id)
		+ "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter, autoDropDownHeight: true }); } } } }, 5000); }"
	)
	page = ""
	if QueryCount < int(PerPage):
		page = str(Page_start) + " - " + str(QueryCount)
	else:
		page = str(Page_start) + " - " + str(Page_End)
	Test = (
		'<div class="col-md-12 brdr listContStyle pad2height30" ><div class="col-md-4 pager-numberofitem clear-padding"><span class="pager-number-of-items-item noofitem" id="NumberofItem" >'
		+ str(page)
		+ ' of </span><span class="pager-number-of-items-item fltltpad2mrg0" id="totalItemCount" >'
		+ str(QueryCount)
		+ '</span><div class="clear-padding fltltmrgtp3" ><div  class="pull-right vertmidtxtrht"><select onchange="PageFunctestChild(this,\'Quotes\')" id="PageCountValue"  class="form-control wid65vermiddisinbmarl5"><option value="10" selected>10</option><option value="20">20</option><option value="50">50</option><option value="100">100</option><option value="200">200</option></select> </div></div></div><div class="col-xs-8 col-md-4  clear-padding disinpad10txtcen"  data-bind="visible: totalItemCount"><div class="clear-padding col-xs-12 col-sm-6 col-md-12 bor0" ><ul class="pagination pagination"><li class="disabled"><a href="#" onclick="FirstPageLoad_paginationChild(\'Quote\',\'\',\''
		+str(table_id)
		+'\')"><i class="fa fa-caret-left font14whtbld" ></i><i class="fa fa-caret-left font14" ></i></a></li><li class="disabled"><a href="#" onclick="Previous12334Child(\'Quotes\')"><i class="fa fa-caret-left font14" ></i>PREVIOUS</a></li><li class="disabled"><a href="#" class="disabledPage" onclick="Next12334Child(\'Quotes\')">NEXT<i class="fa fa-caret-right font14" ></i></a></li><li class="disabled"><a href="#" onclick="LastPageLoad_paginationChild(\'Quote\',\'\',\''
		+str(table_id)
		+'\')" class="disabledPage"><i class="fa fa-caret-right font14"></i><i class="fa fa-caret-right font14whtbld"></i></a></li></ul></div> </div> <div class="col-md-4 pr_page_pad"> <span id="page_count" class="currentPage page_right_content">1</span><span class="page_right_content pad_rt_2">Page </span></div></div>'
	)

	return (
		table_header,
		data_list,
		table_id,
		filter_control_function,
		NORECORDS,
		dbl_clk_function,
		cv_list,
		filter_level_list,
		DropDownList,
		RelatedDrop_str,
		Test,
		"1 - 10 of",
	)

def GetContractAssembliesMaster(PerPage, PageInform, A_Keys, A_Values):
	if str(PerPage) == "" and str(PageInform) == "":
		Page_start = 1
		Page_End = 10
		PerPage = 10
		PageInform = "1___10___10"
	else:
		Page_start = int(PageInform.split("___")[0])
		Page_End = int(PageInform.split("___")[1])
		PerPage = PerPage
	ContractRecordId = Product.GetGlobal("contract_record_id")
	# FablocationId = Product.GetGlobal("TreeParam")
	data_list = []
	obj_idval = "SYOBJ_00904_SYOBJ_00904"
	rec_id = "SYOBJ_00267"
	obj_id = "SYOBJ-00267"
	objh_getid = Sql.GetFirst(
		"SELECT TOP 1  RECORD_ID  FROM SYOBJH (NOLOCK) WHERE SAPCPQ_ATTRIBUTE_NAME='" + str(obj_id) + "'"
	)
	if objh_getid:
		obj_id = objh_getid.RECORD_ID
	objs_obj = Sql.GetFirst(
		"select CAN_ADD,CAN_EDIT,COLUMNS,CAN_DELETE from SYOBJR (NOLOCK) where OBJ_REC_ID = '" + str(obj_id) + "' "
	)
	can_edit = str(objs_obj.CAN_EDIT)
	can_add = str(objs_obj.CAN_ADD)
	can_delete = str(objs_obj.CAN_DELETE)
	table_id = "table_assemblies"
	table_header = (
		'<table id="'
		+ str(table_id)
		+ '"  data-pagination="false" data-sortable="true" data-search-on-enter-key="true" data-filter-control="true" data-pagination-loop = "false" data-locale = "en-US" ><thead>'
	)
	Columns = [
		# "CONTRACT_SERVICE_EQUIPMENT_RECORD_ID",
		"EQUIPMENT_ID",
		"SERIAL_NUMBER",
		"GREENBOOK",
		"FABLOCATION_ID",
	]
	Objd_Obj = Sql.GetList(
		"select FIELD_LABEL,API_NAME,LOOKUP_OBJECT,LOOKUP_API_NAME,DATA_TYPE from SYOBJD (NOLOCK) where OBJECT_NAME = 'CTCSCO'"
	)
	attr_list = []
	attrs_datatype_dict = {}
	lookup_disply_list = []
	lookup_str = ""
	if Objd_Obj is not None:
		attr_list = {}
		for attr in Objd_Obj:
			attr_list[str(attr.API_NAME)] = str(attr.FIELD_LABEL)
			attrs_datatype_dict[str(attr.API_NAME)] = str(attr.DATA_TYPE)
			if attr.LOOKUP_API_NAME != "" and attr.LOOKUP_API_NAME is not None:
				lookup_disply_list.append(str(attr.API_NAME))
		checkbox_list = [inn.API_NAME for inn in Objd_Obj if inn.DATA_TYPE == "CHECKBOX"]
		lookup_list = {ins.LOOKUP_API_NAME: ins.API_NAME for ins in Objd_Obj}
	lookup_str = ",".join(list(lookup_disply_list))

	Qstr = (
		"select top "
		+ str(PerPage)
		+ " * from ( select top 10 ROW_NUMBER() OVER( ORDER BY CONTRACT_SERVICE_EQUIPMENT_RECORD_ID) AS ROW, CONTRACT_SERVICE_EQUIPMENT_RECORD_ID,EQUIPMENT_ID,SERIAL_NUMBER,GREENBOOK,FABLOCATION_ID from CTCSCO (NOLOCK) where CONTRACT_RECORD_ID = '"
		+ str(ContractRecordId)
		+ "'"
		+ "and CONTRACT_SERVICE_EQUIPMENT_RECORD_ID = '"
		+ str(CURR_REC_ID)
		+ "') m where m.ROW BETWEEN "
		+ str(Page_start)
		+ " and "
		+ str(Page_End)
	)
	QueryCount = ""
	QueryCountObj = Sql.GetFirst(
		"select count(CONTRACT_SERVICE_EQUIPMENT_RECORD_ID) as cnt from CTCSCO (NOLOCK) where CONTRACT_RECORD_ID = '"
		+ str(ContractRecordId)
		+ "'"
		+ " and CONTRACT_SERVICE_EQUIPMENT_RECORD_ID = '"
		+ str(CURR_REC_ID)
		+ "'"
	)
	if QueryCountObj is not None:
		QueryCount = QueryCountObj.cnt
	parent_obj = Sql.GetList(Qstr)
	for par in parent_obj:
		data_id = str(par.CONTRACT_SERVICE_EQUIPMENT_RECORD_ID) + "|CTCSCO Key"

		Action_str = (
			'<div class="btn-group dropdown"><div class="dropdown" id="ctr_drop"><i data-toggle="" id="dropdownMenuButton" class="fa fa-sort-desc dropdown-toggle" aria-expanded="false"></i><ul class="dropdown-menu left" aria-labelledby="dropdownMenuButton"><li><a class="dropdown-item cur_sty" href="#" id="'
			+ str(data_id)
			+ '" onclick="Move_to_parent_obj(this)">VIEW</a></li>'
		)
		"""if can_edit.upper() == "TRUE":
			Action_str += (
				'<li style="display:none" ><a class="dropdown-item cur_sty" href="#" id="'
				+ str(data_id)
				+ '" onclick="Move_to_parent_obj_edit(this)">EDIT</a></li>'
			)
		if can_delete.upper() == "TRUE":
			Action_str += '<li><a class="dropdown-item" data-target="#cont_viewModal_Material_Delete" data-toggle="modal" onclick="Material_delete_obj(this)" href="#">DELETE</a></li>'
		if can_add.upper() == "TRUE" and par.MARKET_TYPE == "NON MARKET BASED" and par.MODEL_TYPE != "COST PLUS":
			Action_str += (
				'<li><a class="dropdown-item" id="'
				+ str(data_id)
				+ '" data-target="#" data-toggle="modal" onclick="Pricebook_clone_obj(this)" href="#">CLONE</a></li>'
			)"""
		Action_str += "</ul></div></div>"

		# Data formation in dictonary format.
		## hyperlink
		data_dict = {}
		data_dict["ids"] = str(data_id)
		data_dict["ACTIONS"] = str(Action_str)
		data_dict["CONTRACT_SERVICE_EQUIPMENT_RECORD_ID"] = CPQID.KeyCPQId.GetCPQId(
			"CTCSCO", str(par.CONTRACT_SERVICE_EQUIPMENT_RECORD_ID)
		)
		data_dict["EQUIPMENT_ID"] = str(par.EQUIPMENT_ID)
		data_dict["FABLOCATION_ID"] = str(par.FABLOCATION_ID)
		data_dict["GREENBOOK"] = str(par.GREENBOOK)
		data_dict["SERIAL_NUMBER"] = str(par.SERIAL_NUMBER)
		data_list.append(data_dict)

	hyper_link = ["EQUIPMENT_ID"]
	table_header += "<tr>"
	table_header += (
		'<th data-field="ACTIONS"><div class="action_col">ACTIONS</div><button class="searched_button" id="Act_'
		+ str(table_id)
		+ '">Search</button></th>'
	)
	table_header += '<th data-field="SELECT" class="wid45" data-checkbox="true"></th>'
	for key, invs in enumerate(list(Columns)):
		invs = str(invs).strip()
		qstring = attr_list.get(str(invs)) or ""
		if qstring == "":
			qstring = invs.replace("_", " ")
		if checkbox_list is not None and invs in checkbox_list:
			table_header += (
				'<th  data-field="'
				+ str(invs)
				+ '" data-filter-control="input" data-align="center" data-formatter="CheckboxFieldRelatedList" data-sortable="true"><abbr title="'
				+ str(qstring)
				+ '">'
				+ str(qstring)
				+ "</abbr></th>"
			)
		elif hyper_link is not None and invs in hyper_link:
			table_header += (
				'<th data-field="'
				+ str(invs)
				+ '" data-filter-control="input" data-formatter="ToolDetailHyperLink" data-sortable="true"><abbr title="'
				+ str(qstring)
				+ '">'
				+ str(qstring)
				+ "</abbr></th>"
			)
		else:
			table_header += (
				'<th  data-field="'
				+ str(invs)
				+ '" data-filter-control="input" data-sortable="true"><abbr title="'
				+ str(qstring)
				+ '">'
				+ str(qstring)
				+ "</abbr></th>"
			)
	table_header += "</tr>"
	table_header += '</thead><tbody onclick="Table_Onclick_Scroll(this)"></tbody></table>'
	table_ids = "#" + str(table_id)
	filter_control_function = ""
	values_list = ""
	for key, invs in enumerate(list(Columns)):
		table_ids = "#" + str(table_id)
		filter_clas = "#" + str(table_id) + " .bootstrap-table-filter-control-" + str(invs)
		values_list += "var " + str(invs) + ' = $("' + str(filter_clas) + '").val(); '
		values_list += "ATTRIBUTE_VALUEList.push(" + str(invs) + "); "
	filter_class = "#Act_" + str(table_id)
	filter_control_function += (
		'$("'
		+ filter_class
		+ '").click( function(){ var table_id = $(this).closest("table").attr("id"); ATTRIBUTE_VALUEList = []; '
		+ str(values_list)
		+ ' var attribute_value = $(this).val(); cpq.server.executeScript("CQNESTGRID", {"TABNAME":"Assemblies Parent", "ACTION":"PRODUCT_ONLOAD_FILTER", "ATTRIBUTE_NAME": '
		+ str(list(Columns))
		+ ', "ATTRIBUTE_VALUE": ATTRIBUTE_VALUEList }, function(data) { $("'
		+ str(table_ids)
		+ '").bootstrapTable("load", data ); }); filter_search_click();$(".JColResizer").mousedown(function(){ $("thead.fullHeadFirst").css("cssText","z-index: 2;border-top: 1px solid rgb(220, 220, 220);top: 154px;border-right: 0px !important;");$("thead.fullHeadSecond").css("display","none"); });$(".JColResizer").mouseup(function(){ var th_width_resize = [];$("#table_assemblies_parent thead.fullHeadFirst tr th").each(function(index){var wid = $(this).css("width"); if(index ==0 || index ==1){th_width_resize.push("60px");}else{th_width_resize.push(wid);}}); $("thead.fullHeadFirst").css("cssText","position: fixed;z-index: 2;border-top: 1px solid rgb(220, 220, 220); top: 154px;border-right: 0px !important;");$("thead.fullHeadSecond").css("display","table-header-group");$("#table_assemblies_parent thead.fullHeadFirst tr th").each(function(index){var num = th_width_resize[index].split("px");var numsp = parseInt(num[0]);numsp = numsp - 1;var make_str =numsp+"px"; var c = "width:"+make_str+";white-space: nowrap;overflow: hidden;text-overflow: ellipsis;";var d = "width:"+make_str+";"; $(this).css("cssText",c);$(this).children("div:first-child").css("cssText",c);$(this).children("div.fht-cell").css("cssText",d);});$("#table_assemblies_parent thead.fullHeadSecond tr th").each(function(index){var num = th_width_resize[index].split("px");var numsp = parseInt(num[0]);numsp = numsp - 1;var make_str =numsp+"px"; var c = "width:"+make_str+";white-space: nowrap;overflow: hidden;text-overflow: ellipsis;";var d = "width:"+make_str+";"; $(this).css("cssText",c);$(this).children("div:first-child").css("cssText",c);$(this).children("div.fht-cell").css("cssText",d);}); });});'
	)
	dbl_clk_function = (
		'$("'
		+ str(table_ids)
		+ '").on("all.bs.table", function (e, name, args) { $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); }); $("'
		+ str(table_ids)
		+ '\ th.bs-checkbox div.th-inner").before("<div style=\'padding:0; border-bottom: 1px solid #dcdcdc;\'>SELECT</div>"); $(".bs-checkbox input").addClass("custom");$(".bs-checkbox input").after("<span class=\'lbl\'></span>");'
		)
	NORECORDS = ""
	if len(data_list) == 0:
		NORECORDS = "NORECORDS"

	ObjectName = "CTCSCO"
	DropDownList = []
	filter_level_list = []
	filter_clas_name = ""
	cv_list = []
	TableclassName = "form-control" + table_id
	for key, col_name in enumerate(list(Columns)):
		StringValue_list = []
		objss_obj = Sql.GetFirst(
			"SELECT API_NAME, DATA_TYPE, FORMULA_LOGIC, PICKLIST FROM SYOBJD (NOLOCK) WHERE OBJECT_NAME='"
			+ str(ObjectName)
			+ "' and API_NAME = '"
			+ str(col_name)
			+ "'"
		)
		try:
			FORMULA_LOGIC = objss_obj.FORMULA_LOGIC.strip()
			FORMULA_col = FORMULA_LOGIC.split(" ")[1].strip()
			FORMULA_table = FORMULA_LOGIC.split(" ")[3].strip()
			ins_obj = Sql.GetFirst(
				"SELECT API_NAME, DATA_TYPE,PICKLIST FROM SYOBJD (NOLOCK) WHERE OBJECT_NAME='"
				+ str(FORMULA_table)
				+ "' and API_NAME = '"
				+ str(FORMULA_col)
				+ "'"
			)
			if str(objss_obj.PICKLIST).upper() == "TRUE":
				filter_level_data = "select"
				filter_clas_name = (
					'<div id = "'
					+ str(table_id)
					+ "_RelatedMutipleCheckBoxDrop_"
					+ str(key)
					+ '" class="form-control bootstrap-table-filter-control-'
					+ str(col_name)
					+ " RelatedMutipleCheckBoxDrop_"
					+ str(key)
					+ ' "></div>'
				)
				filter_level_list.append(filter_level_data)
			else:
				filter_level_data = "input"
				filter_clas_name = (
					'<input type="text" class="width100_vis form-control bootstrap-table-filter-control-'
					+ str(col_name)
					+ '">'
				)
				filter_level_list.append(filter_level_data)
		except:
			"""if str(objss_obj.PICKLIST).upper() == "TRUE":
				filter_level_data = "select"
				filter_clas_name = (
					'<div id = "'
					+ str(table_id)
					+ "_RelatedMutipleCheckBoxDrop_"
					+ str(key)
					+ '" class="form-control bootstrap-table-filter-control-'
					+ str(col_name)
					+ " RelatedMutipleCheckBoxDrop_"
					+ str(key)
					+ ' "></div>'
				)
				filter_level_list.append(filter_level_data)"""

			filter_level_data = "input"
			filter_clas_name = (
				'<input type="text" class="width100_vis form-control bootstrap-table-filter-control-' + str(col_name) + '">'
			)
			filter_level_list.append(filter_level_data)
		cv_list.append(filter_clas_name)
		if filter_level_data == "select":
			try:
				xcd = Sql.GetFirst(
					"SELECT (STUFF((SELECT DISTINCT ', ' + CAST("
					+ str(col_name)
					+ " AS CHAR(100)) FROM "
					+ str(ObjectName)
					+ " (NOLOCK) FOR XML PATH('') ), 1, 2, '')  ) AS StringValue"
				)
			except:
				xcd = Sql.GetFirst(
					"SELECT (STUFF((SELECT DISTINCT ', ' + CAST("
					+ str(col_name)
					+ " AS CHAR(100)) FROM "
					+ str(ObjectName)
					+ " (NOLOCK) FOR XML PATH('') ), 1, 2, '')  ) AS StringValue"
				)
			if str(xcd.StringValue) is not None and str(xcd.StringValue) != "":
				if str(xcd.StringValue).find(",") != -1:
					StringValue_list = [ins.strip() for ins in str(xcd.StringValue).split(",") if ins.strip() != ""]
				else:
					StringValue_list.append(str(xcd.StringValue))
			else:
				StringValue_list = [""]
			StringValue_list = list(set(StringValue_list))
			DropDownList.append(StringValue_list)
		elif filter_level_data == "checkbox":
			DropDownList.append(["True", "False"])
		else:
			DropDownList.append("")
	RelatedDrop_str = (
		"try { if( document.getElementById('"
		+ str(table_id)
		+ "') ) { var listws = document.getElementById('"
		+ str(table_id)
		+ "').getElementsByClassName('filter-control');  for (i = 0; i < listws.length; i++) { document.getElementById('"
		+ str(table_id)
		+ "').getElementsByClassName('filter-control')[i].innerHTML = data6[i];  } for (j = 0; j < listws.length; j++) { if (data7[j] == 'select') { if (data8[j]) { var dataAdapter = new $.jqx.dataAdapter(data8[j]); $('#"
		+ str(table_id)
		+ "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter, autoDropDownHeight: true }); } } } } }  catch(err) { setTimeout(function() { var listws = document.getElementById('"
		+ str(table_id)
		+ "').getElementsByClassName('filter-control');  for (i = 0; i < listws.length; i++) { document.getElementById('"
		+ str(table_id)
		+ "').getElementsByClassName('filter-control')[i].innerHTML = data6[i];  } for (j = 0; j < listws.length; j++) { if (data7[j] == 'select') { if (data8[j]) { var dataAdapter = new $.jqx.dataAdapter(data8[j]); $('#"
		+ str(table_id)
		+ "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter, autoDropDownHeight: true }); } } } }, 5000); }"
	)
	page = ""
	if QueryCount < int(PerPage):
		page = str(Page_start) + " - " + str(QueryCount)
	else:
		page = str(Page_start) + " - " + str(Page_End)
	Test = (
		'<div class="col-md-12 brdr listContStyle pad2height30" ><div class="col-md-4 pager-numberofitem clear-padding"><span class="pager-number-of-items-item noofitem" id="NumberofItem" >'
		+ str(page)
		+ ' of </span><span class="pager-number-of-items-item fltltpad2mrg0" id="totalItemCount" >'
		+ str(QueryCount)
		+ '</span><div class="clear-padding fltltmrgtp3" ><div  class="pull-right vertmidtxtrht"><select onchange="PageFunctestChild(this,\'Quotes\')" id="PageCountValue"  class="form-control wid65vermiddisinbmarl5"><option value="10" selected>10</option><option value="20">20</option><option value="50">50</option><option value="100">100</option><option value="200">200</option></select> </div></div></div><div class="col-xs-8 col-md-4  clear-padding disinpad10txtcen"  data-bind="visible: totalItemCount"><div class="clear-padding col-xs-12 col-sm-6 col-md-12 bor0" ><ul class="pagination pagination"><li class="disabled"><a href="#" onclick="FirstPageLoad_paginationChild(\'Quote\',\'\',\''
		+str(table_id)
		+'\')"><i class="fa fa-caret-left font14whtbld" ></i><i class="fa fa-caret-left font14" ></i></a></li><li class="disabled"><a href="#" onclick="Previous12334Child(\'Quotes\')"><i class="fa fa-caret-left font14" ></i>PREVIOUS</a></li><li class="disabled"><a href="#" class="disabledPage" onclick="Next12334Child(\'Quotes\')">NEXT<i class="fa fa-caret-right font14" ></i></a></li><li class="disabled"><a href="#" onclick="LastPageLoad_paginationChild(\'Quote\',\'\',\''
		+str(table_id)
		+'\')" class="disabledPage"><i class="fa fa-caret-right font14"></i><i class="fa fa-caret-right font14whtbld"></i></a></li></ul></div> </div> <div class="col-md-4 pr_page_pad"> <span id="page_count" class="currentPage page_right_content">1</span><span class="page_right_content pad_rt_2">Page </span></div></div>'
	)

	return (
		table_header,
		data_list,
		table_id,
		filter_control_function,
		NORECORDS,
		dbl_clk_function,
		cv_list,
		filter_level_list,
		DropDownList,
		RelatedDrop_str,
		Test,
		"1 - 10 of",
	)

def GetAssembliesChild(recid, PerPage, PageInform, A_Keys, A_Values):
	TreeParam = Product.GetGlobal("TreeParam")
	TreeParentParam = Product.GetGlobal("TreeParentLevel0")
	TreeSuperParentParam = Product.GetGlobal("TreeParentLevel1")
	TreeTopSuperParentParam = Product.GetGlobal("TreeParentLevel2")
	
	if str(PerPage) == "" and str(PageInform) == "":
		Page_start = 1
		Page_End = 10
		PerPage = 10
		PageInform = "1___10___10"
	else:
		Page_start = int(PageInform.split("___")[0])
		Page_End = int(PageInform.split("___")[1])
		PerPage = PerPage
	chld_list = []
	Parent_Equipmentid = ""
	ContractRecordId = Quote.GetGlobal("contract_quote_record_id")
	RevisionRecordId = Quote.GetGlobal("quote_revision_record_id")
	obj_idval = "SYOBJ_00929_SYOBJ_00929"
	obj_id1 = "SYOBJ-00929"
	objh_getid = Sql.GetFirst(
		"SELECT TOP 1  RECORD_ID  FROM SYOBJH (NOLOCK) WHERE SAPCPQ_ATTRIBUTE_NAME='" + str(obj_id1) + "'"
	)
	if objh_getid:
		obj_id1 = objh_getid.RECORD_ID
	objs_obj1 = Sql.GetFirst(
		"select CAN_ADD,CAN_EDIT,COLUMNS,CAN_DELETE from SYOBJR (NOLOCK) where OBJ_REC_ID = '" + str(obj_id1) + "' "
	)
	can_edit1 = str(objs_obj1.CAN_EDIT)
	can_add1 = str(objs_obj1.CAN_ADD)
	can_delete1 = str(objs_obj1.CAN_DELETE)
	table_id = "covered_obj_child_" +str(recid)
	table_header = (
		'<table id="'
		+ str(table_id)
		+ '" data-pagination="false" data-sortable="true" data-search-on-enter-key="true" data-filter-control="true" data-pagination-loop = "false" data-locale = "en-US" ><thead>'
	)
	Columns = ["QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID","ASSEMBLY_ID", "ASSEMBLY_DESCRIPTION", "EQUIPMENT_DESCRIPTION", "GOT_CODE"]
	Objd_Obj = Sql.GetList(
		"select FIELD_LABEL,API_NAME,LOOKUP_OBJECT,LOOKUP_API_NAME,DATA_TYPE from SYOBJD (NOLOCK) where OBJECT_NAME = 'SAQSCA'"
	)
	attr_list = []
	attrs_datatype_dict = {}
	lookup_disply_list = []
	lookup_str = ""
	if Objd_Obj is not None:
		attr_list = {}
		for attr in Objd_Obj:
			attr_list[str(attr.API_NAME)] = str(attr.FIELD_LABEL)
			attrs_datatype_dict[str(attr.API_NAME)] = str(attr.DATA_TYPE)
			if attr.LOOKUP_API_NAME != "" and attr.LOOKUP_API_NAME is not None:
				lookup_disply_list.append(str(attr.API_NAME))
		checkbox_list = [inn.API_NAME for inn in Objd_Obj if inn.DATA_TYPE == "CHECKBOX"]
		lookup_list = {ins.LOOKUP_API_NAME: ins.API_NAME for ins in Objd_Obj}
	lookup_str = ",".join(list(lookup_disply_list))
	Parent_Equipmentid = Sql.GetFirst(
		"""select EQUIPMENT_ID from SAQSCO (NOLOCK) where QUOTE_RECORD_ID = '{ContractRecordId}' and QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID = '{CurrRecId}' and QTEREV_RECORD_ID = '{RevisionRecordId}'
		""".format(
			ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"), CurrRecId=CURR_REC_ID
		)
	)
	if Parent_Equipmentid:
		EquipmentID = Parent_Equipmentid.EQUIPMENT_ID
		if TreeTopSuperParentParam == 'Comprehensive Services' or TreeTopSuperParentParam == 'Add-On Products':
			child_obj_recid = Sql.GetList(
				"select top 10 QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID,EQUIPMENT_ID,ASSEMBLY_ID,ASSEMBLY_DESCRIPTION,GOT_CODE, EQUIPMENT_DESCRIPTION from SAQSCA (NOLOCK) where EQUIPMENT_ID = '{Parent_Equipmentid}' and QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' and SERVICE_ID = '{TreeSuperParentParam}' and FABLOCATION_ID = '{TreeParentParam}'".format(
					ContractRecordId=Quote.GetGlobal("contract_quote_record_id"), RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"),Parent_Equipmentid=recid, TreeSuperParentParam=TreeSuperParentParam,TreeParentParam = TreeParentParam
				)
			)

			QueryCountObj = Sql.GetFirst(
				"select count(QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID) as cnt from SAQSCA (NOLOCK) where QUOTE_RECORD_ID = '"
				+ str(ContractRecordId)
				+ "' and QTEREV_RECORD_ID = '"
				+ str(RevisionRecordId)
				+ "' and EQUIPMENT_ID ='"
				+ str(recid)
				+ "'and SERVICE_ID ='"
				+ str(TreeSuperParentParam)
				+ "'and FABLOCATION_ID ='"
				+ str(TreeParentParam)
				+ "'"
			)    
		if QueryCountObj is not None:
			QueryCount = QueryCountObj.cnt
		# Data construction for table.
		for child in child_obj_recid:
			
			data_id = str(child.QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID)
			chld_dict = {}
			Action_str1 = (
				'<div class="btn-group dropdown"><div class="dropdown" id="ctr_drop"><i data-toggle="" id="dropdownMenuButton" class="fa fa-sort-desc dropdown-toggle" aria-expanded="false"></i><ul class="dropdown-menu left" aria-labelledby="dropdownMenuButton"><li><a  data-toggle="modal" data-target="#cont_viewModalSection" id="'
				+ str(data_id)
				+ '" class="" href="#"  onclick="cont_relatedlist_openview(this) ">VIEW</a></li>'
			)
			if can_edit1.upper() == "TRUE":
				Action_str1 += (
					'<li style="display:none" ><a data-toggle="modal" data-target="#cont_viewModalSection" id="'
					+ str(data_id)
					+ '"  class="dropdown-item cur_sty" href="#"  onclick="cont_relatedlist_openedit(this)">EDIT</a></li>'
				)
			if can_delete1.upper() == "TRUE":
				Action_str1 += '<li><a class="dropdown-item" data-target="#cont_viewModal_Material_Delete" data-toggle="modal" onclick="Material_delete_obj(this)" href="#">DELETE</a></li>'
			if can_add1.upper() == "TRUE":
				Action_str1 += '<li><a class="dropdown-item" data-target="#" data-toggle="modal" onclick="Material_clone_obj(this)" href="#">CLONE</a></li>'
			Action_str1 += "</ul></div></div>"

			# data formation in Dictonary format.
			chld_dict["ids"] = str(data_id)
			chld_dict["ACTIONS"] = str(Action_str1)
			chld_dict["QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID"] = CPQID.KeyCPQId.GetCPQId(
				"SAQSCA", str(child.QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID)
			)
			chld_dict["EQUIPMENT_ID"] = str(child.EQUIPMENT_ID)
			chld_dict["ASSEMBLY_ID"] = str(child.ASSEMBLY_ID)
			chld_dict["ASSEMBLY_DESCRIPTION"] = str(child.ASSEMBLY_DESCRIPTION)
			chld_dict["EQUIPMENT_DESCRIPTION"] = str(child.EQUIPMENT_DESCRIPTION)
			chld_dict["GOT_CODE"] = str(child.GOT_CODE)
			#chld_dict["MODULE_ID"] = str(child.MODULE_ID)
			#chld_dict["MODULE_NAME"] = str(child.MODULE_NAME)
			chld_list.append(chld_dict)

	# Table formation.
	hyper_link = ["QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID"]    
	table_header += "<tr>"
	table_header += (
		'<th data-field="ACTIONS"><div class="action_col">ACTIONS</div><button class="searched_button" id="Act_'
		+ str(table_id)
		+ '">Search</button></th>'
	)
	table_header += '<th data-field="SELECT" class="wid45" data-checkbox="true"></th>'
	for key, invs in enumerate(list(Columns)):
		invs = str(invs).strip()
		qstring = attr_list.get(str(invs)) or ""
		if qstring == "":
			qstring = invs.replace("_", " ")
		if checkbox_list is not None and invs in checkbox_list:
			table_header += (
				'<th data-field="'
				+ str(invs)
				+ '" data-filter-control="input" data-align="center" data-formatter="CheckboxFieldRelatedList" data-sortable="true"><abbr title="'
				+ str(qstring)
				+ '">'
				+ str(qstring)
				+ "</abbr></th>"
			)
		elif hyper_link is not None and invs in hyper_link:
			table_header += (
				'<th data-field="'
				+ str(invs)
				+ '" data-filter-control="input" data-align="left" data-formatter="coveredobjectchildHyperLink" data-sortable="true"><abbr title="'
				+ str(qstring)
				+ '">'
				+ str(qstring)
				+ "</abbr></th>"
			)
		else:
			table_header += (
				'<th data-field="'
				+ str(invs)
				+ '" data-filter-control="input" data-sortable="true"><abbr title="'
				+ str(qstring)
				+ '">'
				+ str(qstring)
				+ "</abbr></th>"
			)
	table_header += "</tr>"
	table_header += '</thead><tbody onclick="Table_Onclick_Scroll(this)"></tbody></table>'
	table_ids = "#" + str(table_id)
	filter_control_function = ""
	values_list = ""
	for key, invs in enumerate(list(Columns)):
		table_ids = "#" + str(table_id)
		filter_clas = "#" + str(table_id) + " .bootstrap-table-filter-control-" + str(invs)
		values_list += "var " + str(invs) + ' = $("' + str(filter_clas) + '").val(); '
		values_list += "ATTRIBUTE_VALUEList.push(" + str(invs) + "); "
	filter_class = "#Act_" + str(table_id)
	filter_control_function += (
		'$("'
		+ filter_class
		+ '").click( function(){ var table_id = $(this).closest("table").attr("id"); ATTRIBUTE_VALUEList = []; '
		+ str(values_list)
		+ ' var attribute_value = $(this).val(); cpq.server.executeScript("CQNESTGRID", {"TABNAME":"Assemblies Child", "ACTION":"PRODUCT_ONLOAD_FILTER", "ATTRIBUTE_NAME": '
		+ str(list(Columns))
		+ ', "ATTRIBUTE_VALUE": ATTRIBUTE_VALUEList, "RECID":"'
		+ str(recid)
		+ '" }, function(data) { $("'
		+ str(table_ids)
		+ '").bootstrapTable("load", data ); }); filter_search_click();$(".JColResizer").mousedown(function(){ $("thead.fullHeadFirst").css("cssText","z-index: 2;border-top: 1px solid rgb(220, 220, 220);top: 154px;border-right: 0px !important;");$("thead.fullHeadSecond").css("display","none"); });$(".JColResizer").mouseup(function(){ var th_width_resize = [];$("#table_assemblies_child thead.fullHeadFirst tr th").each(function(index){var wid = $(this).css("width"); if(index ==0 || index ==1){th_width_resize.push("60px");}else{th_width_resize.push(wid);}}); $("thead.fullHeadFirst").css("cssText","position: fixed;z-index: 2;border-top: 1px solid rgb(220, 220, 220); top: 154px;border-right: 0px !important;");$("thead.fullHeadSecond").css("display","table-header-group");$("#table_assemblies_child thead.fullHeadFirst tr th").each(function(index){var num = th_width_resize[index].split("px");var numsp = parseInt(num[0]);numsp = numsp - 1;var make_str =numsp+"px"; var c = "width:"+make_str+";white-space: nowrap;overflow: hidden;text-overflow: ellipsis;";var d = "width:"+make_str+";"; $(this).css("cssText",c);$(this).children("div:first-child").css("cssText",c);$(this).children("div.fht-cell").css("cssText",d);});$("#table_assemblies_child thead.fullHeadSecond tr th").each(function(index){var num = th_width_resize[index].split("px");var numsp = parseInt(num[0]);numsp = numsp - 1;var make_str =numsp+"px"; var c = "width:"+make_str+";white-space: nowrap;overflow: hidden;text-overflow: ellipsis;";var d = "width:"+make_str+";"; $(this).css("cssText",c);$(this).children("div:first-child").css("cssText",c);$(this).children("div.fht-cell").css("cssText",d);}); });});'
	)
	dbl_clk_function = (
		'$("'
		+ str(table_ids)
		+ '").on("all.bs.table", function (e, name, args) { $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); }); $("'
		+ str(table_ids)
		+ '\ th.bs-checkbox div.th-inner").before("<div style=\'padding:0; border-bottom: 1px solid #dcdcdc;\'>SELECT</div>"); $(".bs-checkbox input").addClass("custom");$(".bs-checkbox input").after("<span class=\'lbl\'></span>");'
		)

	NORECORDS = ""
	if len(chld_list) == 0:
		NORECORDS = "NORECORDS"

	ObjectName = "SAQSCA"
	DropDownList = []
	filter_level_list = []
	filter_clas_name = ""
	cv_list = []
	TableclassName = "form-control" + table_id
	for key, col_name in enumerate(list(Columns)):
		StringValue_list = []
		objss_obj = Sql.GetFirst(
			"SELECT API_NAME, DATA_TYPE, FORMULA_LOGIC FROM SYOBJD (NOLOCK) WHERE OBJECT_NAME='"
			+ str(ObjectName)
			+ "' and API_NAME = '"
			+ str(col_name)
			+ "'"
		)
		try:
			FORMULA_LOGIC = objss_obj.FORMULA_LOGIC.strip()
			FORMULA_col = FORMULA_LOGIC.split(" ")[1].strip()
			FORMULA_table = FORMULA_LOGIC.split(" ")[3].strip()
			ins_obj = Sql.GetFirst(
				"SELECT API_NAME, DATA_TYPE,PICKLIST FROM SYOBJD (NOLOCK) WHERE OBJECT_NAME='"
				+ str(FORMULA_table)
				+ "' and API_NAME = '"
				+ str(FORMULA_col)
				+ "'"
			)
			if str(objss_obj.PICKLIST).upper() == "TRUE":
				filter_level_data = "select"
				filter_clas_name = (
					'<div id = "'
					+ str(table_id)
					+ "_RelatedMutipleCheckBoxDrop_"
					+ str(key)
					+ '" class="form-control bootstrap-table-filter-control-'
					+ str(col_name)
					+ " RelatedMutipleCheckBoxDrop_"
					+ str(key)
					+ ' "></div>'
				)
				filter_level_list.append(filter_level_data)
			else:
				filter_level_data = "input"
				filter_clas_name = (
					'<input type="text" class="width100_vis form-control bootstrap-table-filter-control-'
					+ str(col_name)
					+ '">'
				)
				filter_level_list.append(filter_level_data)
		except:
			"""if str(objss_obj.PICKLIST).upper() == "TRUE":
				filter_level_data = "select"
				filter_clas_name = (
					'<div id = "'
					+ str(table_id)
					+ "_RelatedMutipleCheckBoxDrop_"
					+ str(key)
					+ '" class="form-control bootstrap-table-filter-control-'
					+ str(col_name)
					+ " RelatedMutipleCheckBoxDrop_"
					+ str(key)
					+ ' "></div>'
				)
				filter_level_list.append(filter_level_data)"""

			filter_level_data = "input"
			filter_clas_name = (
				'<input type="text" class="width100_vis form-control bootstrap-table-filter-control-' + str(col_name) + '">'
			)
			filter_level_list.append(filter_level_data)
		cv_list.append(filter_clas_name)
		if filter_level_data == "select":
			try:
				xcd = Sql.GetFirst(
					"SELECT (STUFF((SELECT DISTINCT ', ' + CAST("
					+ str(col_name)
					+ " AS CHAR(100)) FROM "
					+ str(ObjectName)
					+ " (NOLOCK) where QUOTE_FAB_LOC_COV_OBJ_ASSEMBLY_RECORD_ID = '"
					+ str(recid)
					+ "' FOR XML PATH('') ), 1, 2, '')  ) AS StringValue"
				)
			except:
				xcd = Sql.GetFirst(
					"SELECT (STUFF((SELECT DISTINCT ', ' + CAST("
					+ str(col_name)
					+ " AS CHAR(100)) FROM "
					+ str(ObjectName)
					+ " (NOLOCK) FOR XML PATH('') ), 1, 2, '')  ) AS StringValue"
				)
			if str(xcd.StringValue) is not None and str(xcd.StringValue) != "":
				if str(xcd.StringValue).find(",") != -1:
					StringValue_list = [ins.strip() for ins in str(xcd.StringValue).split(",") if ins.strip() != ""]
				else:
					StringValue_list.append(str(xcd.StringValue))
			else:
				StringValue_list = [""]
			StringValue_list = list(set(StringValue_list))
			DropDownList.append(StringValue_list)
		elif filter_level_data == "checkbox":
			DropDownList.append(["True", "False"])
		else:
			DropDownList.append("")
	RelatedDrop_str = (
		"try { if( document.getElementById('"
		+ str(table_id)
		+ "') ) { var listws = document.getElementById('"
		+ str(table_id)
		+ "').getElementsByClassName('filter-control');  for (i = 0; i < listws.length; i++) { document.getElementById('"
		+ str(table_id)
		+ "').getElementsByClassName('filter-control')[i].innerHTML = datachld6[i];  } for (j = 0; j < listws.length; j++) { if (datachld7[j] == 'select') { if (data8[j]) { var dataAdapter = new $.jqx.dataAdapter(datachld8[j]); $('#"
		+ str(table_id)
		+ "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter, autoDropDownHeight: true }); } } } } }  catch(err) { setTimeout(function() { var listws = document.getElementById('"
		+ str(table_id)
		+ "').getElementsByClassName('filter-control');  for (i = 0; i < listws.length; i++) { document.getElementById('"
		+ str(table_id)
		+ "').getElementsByClassName('filter-control')[i].innerHTML = datachld6[i];  } for (j = 0; j < listws.length; j++) { if (datachld7[j] == 'select') { if (data8[j]) { var dataAdapter = new $.jqx.dataAdapter(datachld8[j]); $('#"
		+ str(table_id)
		+ "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter, autoDropDownHeight: true }); } } } }, 5000); } try { setTimeout(function(){ $('#"
		+ str(table_id)
		+ "').colResizable({ resizeMode:'overflow'}); }, 3000); } catch(err){}"
	)
	page = ""
	if QueryCount < int(PerPage):
		page = str(Page_start) + " - " + str(QueryCount)
	else:
		page = str(Page_start) + " - " + str(Page_End)
	Test = (
		'<div class="col-md-12 brdr listContStyle pad2height30" ><div class="col-md-4 pager-numberofitem clear-padding"><span class="pager-number-of-items-item noofitem" id="'
		+ str(table_id)
		+ '___NumberofItem" >'
		+ str(page)
		+ ' of </span><span class="pager-number-of-items-item fltltpad2mrg0" id="'
		+ str(table_id)
		+ '___totalItemCount" >'
		+ str(QueryCount)
		+ '</span><div class="clear-padding fltltmrgtp3" ><div  class="pull-right vertmidtxtrht"><select onchange="PageFunctestChild(this,\'Quotes\')" id="'+str(table_id)+'___PageCountValue"  class="form-control wid65vermiddisinbmarl5"><option value="10" selected>10</option><option value="20">20</option><option value="50">50</option><option value="100">100</option><option value="200">200</option></select> </div></div></div><div class="col-xs-8 col-md-4  clear-padding disinpad10txtcen"  data-bind="visible: totalItemCount"><div class="clear-padding col-xs-12 col-sm-6 col-md-12 bor0" ><ul class="pagination pagination"><li class="disabled"><a href="#" onclick="FirstPageLoad_paginationChild(\'Quote\',\'\',\''
		+str(table_id)
		+'\')"><i class="fa fa-caret-left font14whtbld" ></i><i class="fa fa-caret-left font14" ></i></a></li><li class="disabled"><a href="#" onclick="Previous12334Child(\'Quote\',\'\',\''
		+str(table_id)
		+'\')"><i class="fa fa-caret-left font14" ></i>PREVIOUS</a></li><li class="disabled"><a href="#" class="disabledPage" onclick="Next12334Child(\'Quote\',\'\',\''
		+str(table_id)
		+'\')">NEXT<i class="fa fa-caret-right font14" ></i></a></li><li class="disabled"><a href="#" onclick="LastPageLoad_paginationChild(\'Quote\',\'\',\''
		+str(table_id)
		+'\')" class="disabledPage"><i class="fa fa-caret-right font14"></i><i class="fa fa-caret-right font14whtbld"></i></a></li></ul></div> </div> <div class="col-md-4 pr_page_pad"> <span id="'+str(table_id)+'___page_count" class="currentPage page_right_content">1</span><span class="page_right_content pad_rt_2">Page </span></div></div>'
	)
	Action_Str = ""
	Action_Str = "1 - "
	Action_Str += str(PerPage)
	Action_Str += " of"

	return (
		table_header,
		chld_list,
		table_id,
		filter_control_function,
		NORECORDS,
		dbl_clk_function,
		cv_list,
		filter_level_list,
		DropDownList,
		RelatedDrop_str,
		Test,
		Action_Str,
	)


def GetAssembliesChildFilter(ATTRIBUTE_NAME, ATTRIBUTE_VALUE, RECID):
	TreeParam = Product.GetGlobal("TreeParam")
	TreeParentParam = Product.GetGlobal("TreeParentLevel0")
	TreeSuperParentParam = Product.GetGlobal("TreeParentLevel1")
	TreeTopSuperParentParam = Product.GetGlobal("TreeParentLevel2")
	# FablocationId = Product.GetGlobal("TreeParam")
	ContractRecordId = Quote.GetGlobal("contract_quote_record_id")
	RevisionRecordId = Quote.GetGlobal("quote_revision_record_id")
	ATTRIBUTE_VALUE_STR = ""
	Dict_formation = dict(zip(ATTRIBUTE_NAME, ATTRIBUTE_VALUE))
	for quer_key, quer_value in enumerate(Dict_formation):
		x_picklistcheckobj = Sql.GetFirst(
			"SELECT PICKLIST FROM SYOBJD (NOLOCK) WHERE OBJECT_NAME ='SAQSCA' AND API_NAME = '" + str(quer_value) + "'"
		)
		x_picklistcheck = str(x_picklistcheckobj.PICKLIST).upper()
		if Dict_formation.get(quer_value) != "":
			quer_values = str(Dict_formation.get(quer_value)).strip()
			if str(quer_values).upper() == "TRUE":
				quer_values = "TRUE"
			elif str(quer_values).upper() == "FALSE":
				quer_values = "FALSE"
			if str(quer_values).find(",") == -1:
				if x_picklistcheck == "TRUE":
					ATTRIBUTE_VALUE_STR += str(quer_value) + " = '" + str(quer_values) + "' and "
				else:
					ATTRIBUTE_VALUE_STR += str(quer_value) + " like '%" + str(quer_values) + "%' and "
			else:
				quer_values = quer_values.split(",")
				quer_values = tuple(list(quer_values))
				ATTRIBUTE_VALUE_STR += str(quer_value) + " in " + str(quer_values) + " and "

	data_list = []
	rec_id = "SYOBJ_00929"
	obj_id = "SYOBJ-00929"
	objh_getid = Sql.GetFirst(
		"SELECT TOP 1  RECORD_ID  FROM SYOBJH (NOLOCK) WHERE SAPCPQ_ATTRIBUTE_NAME='" + str(obj_id) + "'"
	)
	if objh_getid:
		obj_id = objh_getid.RECORD_ID
	objs_obj = Sql.GetFirst(
		"select CAN_ADD,CAN_EDIT,COLUMNS,CAN_DELETE from SYOBJR (NOLOCK) where OBJ_REC_ID = '" + str(obj_id) + "' "
	)
	can_edit = str(objs_obj.CAN_EDIT)
	can_clone = str(objs_obj.CAN_ADD)
	can_delete = str(objs_obj.CAN_DELETE)
	if ATTRIBUTE_VALUE is None or ATTRIBUTE_VALUE == "" or ATTRIBUTE_VALUE_STR is None or ATTRIBUTE_VALUE_STR == "":
		parent_obj = Sql.GetList(
			"select QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID,EQUIPMENT_ID,ASSEMBLY_ID,ASSEMBLY_DESCRIPTION,GOT_CODE, EQUIPMENT_DESCRIPTION from SAQSCA (NOLOCK) where EQUIPMENT_ID = '{recid}' and QUOTE_RECORD_ID = '{ContractRecordId}'  and QTEREV_RECORD_ID = '{RevisionRecordId}' and SERVICE_ID = '{TreeSuperParentParam}' and FABLOCATION_ID ='{TreeParentParam}'".format(
				ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"), recid=RECID, TreeParentParam=TreeParentParam,TreeSuperParentParam=TreeSuperParentParam
			)
		)
	else:
		parent_obj = Sql.GetList(
			"select QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID,EQUIPMENT_ID,ASSEMBLY_ID,ASSEMBLY_DESCRIPTION,GOT_CODE, EQUIPMENT_DESCRIPTION from SAQSCA (NOLOCK) where  "
			+ str(ATTRIBUTE_VALUE_STR)
			+ " 1=1 and QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' and EQUIPMENT_ID = '{recid}' and SERVICE_ID = '{TreeSuperParentParam}' and FABLOCATION_ID ='{TreeParentParam}'".format(
				ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"), recid=RECID, TreeParentParam=TreeParentParam,TreeSuperParentParam=TreeSuperParentParam
			)
		)

	for par in parent_obj:
		data_dict = {}
		data_id = str(par.QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID)

		Action_str = (
			'<div class="btn-group dropdown"><div class="dropdown" id="ctr_drop"><i data-toggle="dropdown" id="dropdownMenuButton" class="fa fa-sort-desc dropdown-toggle" aria-expanded="false"></i><ul class="dropdown-menu left" aria-labelledby="dropdownMenuButton"><li><a class="dropdown-item cur_sty" href="#" id="'
			+ str(data_id)
			+ '" onclick="Commonteree_view_RL(this)">VIEW</a></li>'
		)
		if can_edit.upper() == "TRUE":
			Action_str += (
				'<li style="display:none" ><a class="dropdown-item cur_sty" href="#" id="'
				+ str(data_id)
				+ '" onclick="Move_to_parent_obj_edit(this)">EDIT</a></li>'
			)
		if can_delete.upper() == "TRUE":
			Action_str += '<li><a class="dropdown-item" data-target="#cont_viewModal_Material_Delete" data-toggle="modal" onclick="Material_delete_obj(this)" href="#">DELETE</a></li>'
		if can_clone.upper() == "TRUE":
			Action_str += '<li><a class="dropdown-item" data-target="#" data-toggle="modal" onclick="Material_clone_obj(this)" href="#">CLONE</a></li>'

		Action_str += "</ul></div></div>"
		data_dict = {}
		data_dict["ids"] = str(data_id)
		data_dict["ACTIONS"] = str(Action_str)
		data_dict["INCLUDED"] = str(par.INCLUDED)
		data_dict["QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID"] = CPQID.KeyCPQId.GetCPQId(
			"SAQSCA", str(par.QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID)
		)
		data_dict["EQUIPMENT_ID"] = str(par.EQUIPMENT_ID)
		data_dict["ASSEMBLY_ID"] = str(par.ASSEMBLY_ID)
		data_dict["ASSEMBLY_DESCRIPTION"] = str(par.ASSEMBLY_DESCRIPTION)
		data_dict["EQUIPMENT_DESCRIPTION"] = str(par.EQUIPMENT_DESCRIPTION)
		data_dict["GOT_CODE"] = str(par.GOT_CODE)
		#data_dict["MODULE_ID"] = str(par.MODULE_ID)
		#data_dict["MODULE_NAME"] = str(par.MODULE_NAME)
		data_list.append(data_dict)

	return data_list


def UpdateBreadcrumb():    
	TreeParam = Product.GetGlobal("TreeParam")
	TreeParentParam = Product.GetGlobal("TreeParentLevel0")
	TreeSuperParentParam = Product.GetGlobal("TreeParentLevel1")
	TreeTopSuperParentParam = Product.GetGlobal("TreeParentLevel2")
	TestProduct = Webcom.Configurator.Scripting.Test.TestProduct()
	QuoteRecordId = Product.GetGlobal("contract_quote_record_id")
	RevisionRecordId = Quote.GetGlobal("quote_revision_record_id")
	try:
		CurrentTabName = TestProduct.CurrentTab
	except:
		CurrentTabName = 'Quotes'
	qry = ""
	eq_id = ""
	Action_Str = ""
	Trace.Write("TABLENAME_chk "+str(TABLENAME) +str(TreeParam))
	if (TreeParentParam == "Comprehensive Services" or TreeTopSuperParentParam == "Comprehensive Services" or TreeParentParam == "Complementary Products" or TreeTopSuperParentParam == "Complementary Products") and TABLENAME == 'SAQSCO' and CurrentTabName == "Quote" : 
		qry = Sql.GetFirst(
			"SELECT EQUIPMENT_ID,SERIAL_NO FROM SAQSCO (NOLOCK) WHERE QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID = '{recid}'".format(recid=CURR_REC_ID)
		)
		if qry:
			eq_id = str(qry.EQUIPMENT_ID)+"-"+str(qry.SERIAL_NO)
		else:
			eq_id = "TOOLS"
	elif (TreeTopSuperParentParam == "Quote Items" or TreeSuperParentParam == "Quote Items") and CurrentTabName == "Quote" : 
		qry = Sql.GetFirst(
			"SELECT EQUIPMENT_ID,SERIAL_NO FROM SAQICO (NOLOCK) WHERE QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{recid}'".format(recid=CURR_REC_ID)
		)
		if qry:
			eq_id = str(qry.EQUIPMENT_ID)+"-"+str(qry.SERIAL_NO)
		else:
			eq_id = "TOOLS"
	elif TreeParentParam == "Approvals" or TreeSuperParentParam == "Approvals":
		transaction_obj = Sql.GetFirst(
			"SELECT APRCHNSTPTRX_ID FROM ACAPTX (NOLOCK) WHERE APPROVAL_TRANSACTION_RECORD_ID = '{recid}'".format(recid=CURR_REC_ID)
		)
		if transaction_obj:
			eq_id = str(transaction_obj.APRCHNSTPTRX_ID)
		else:
			eq_id = "TOOLS"
	elif (TreeTopSuperParentParam == "Comprehensive Services" or TreeSuperParentParam == "Comprehensive Services") and CurrentTabName == "Contract" : 
		qry = Sql.GetFirst(
			"SELECT EQUIPMENT_ID,SERIAL_NUMBER FROM CTCSCO (NOLOCK) WHERE CONTRACT_SERVICE_EQUIPMENT_RECORD_ID = '{recid}'".format(recid=CURR_REC_ID)
		)
		if qry:
			eq_id = str(qry.EQUIPMENT_ID)+"-"+str(qry.SERIAL_NUMBER)
		else:
			eq_id = "TOOLS"
	elif TreeParam == "Quote Items" and TABLENAME == 'SAQICO':        
		qry = Sql.GetFirst(
		"SELECT EQUIPMENT_ID,EQUIPMENT_DESCRIPTION,SERIAL_NO FROM SAQICO (NOLOCK) WHERE QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{recid}'".format(recid=CURR_REC_ID)
		)
		if qry:
			eq_id = str(qry.EQUIPMENT_ID)+"-"+str(qry.SERIAL_NO)
		else:
			eq_id = "Equipment"
	elif TreeSuperParentParam == "Cart Items":        
		qry = Sql.GetFirst(
		"SELECT EQUIPMENT_ID,EQUIPMENT_DESCRIPTION,SERIAL_NO FROM CTCICO (NOLOCK) WHERE CONTRACT_ITEM_COVERED_OBJECT_RECORD_ID = '{recid}'".format(recid=CURR_REC_ID)
		)
		if qry:
			eq_id = str(qry.EQUIPMENT_ID)+"-"+str(qry.SERIAL_NO)
		else:
			eq_id = "Equipment"
	elif TreeParentParam == "Fab Locations" or TreeParam == "Fab Locations" or TreeSuperParentParam == "Fab Locations":        


		qry = Sql.GetFirst(
		"SELECT EQUIPMENT_ID,EQUIPMENT_DESCRIPTION,SERIAL_NUMBER FROM SAQFEQ (NOLOCK) WHERE QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID = '{recid}'".format(recid=CURR_REC_ID)
		)


		if qry:
			eq_id = str(qry.EQUIPMENT_ID)+"-"+str(qry.SERIAL_NUMBER)
		else:
			qry = Sql.GetFirst(
			"SELECT EQUIPMENT_ID,EQUIPMENT_DESCRIPTION,SERIAL_NUMBER FROM CTCFEQ (NOLOCK) WHERE CONTRACT_FAB_LOC_GB_EQUIPMENT_RECORD_ID = '{recid}'".format(recid=CURR_REC_ID)
			)
			if qry:
				eq_id = str(qry.EQUIPMENT_ID)+"-"+str(qry.SERIAL_NUMBER)
			else:
				eq_id = "Equipment"        
	elif TreeParentParam == "Quote Items":
		qry = Sql.GetFirst(
		"SELECT PART_NUMBER,PART_DESCRIPTION FROM SAQIFP (NOLOCK) WHERE QUOTE_ITEM_FORECAST_PART_RECORD_ID = '{recid}'".format(recid=CURR_REC_ID)
		)
		if qry:
			eq_id = str(qry.PART_NUMBER)
		else:
			eq_id = "Spare parts"  
	elif TreeParam == 'Documents':        
		qry = Sql.GetFirst(
		"SELECT DOCUMENT_ID FROM SAQDOC (NOLOCK) WHERE QUOTE_DOCUMENT_RECORD_ID = '{recid}'".format(recid=CURR_REC_ID)
		)
		if qry:
			eq_id = str(qry.DOCUMENT_ID)
		else:
			eq_id = "Pending"  
	elif TreeParentParam == 'Tracked Objects':        
		qry = Sql.GetFirst(
		"SELECT TRKOBJ_TRACKEDFIELD_NEWVALUE FROM ACAPFV (NOLOCK) WHERE APPROVAL_TRACKED_VALUE_RECORD_ID = '{recid}'".format(recid=CURR_REC_ID)
		)
		if qry:
			eq_id = str(qry.TRKOBJ_TRACKEDFIELD_NEWVALUE)
		else:
			eq_id = "Tracked value"  
		
	elif TreeParentParam == 'Approval Chain Steps':        
		qry = Sql.GetFirst(
		"SELECT APRCHNSTP_APPROVER_ID FROM ACACSA (NOLOCK) WHERE APPROVAL_CHAIN_STEP_APPROVER_RECORD_ID = '{recid}'".format(recid=CURR_REC_ID)
		)
		qry_1 = Sql.GetFirst(
		"SELECT TRKOBJ_TRACKEDFIELD_LABEL FROM ACAPTF (NOLOCK) WHERE APPROVAL_TRACKED_FIELD_RECORD_ID = '{recid}'".format(recid=CURR_REC_ID)
		)
		if qry:
			eq_id = str(qry.APRCHNSTP_APPROVER_ID)
		elif qry_1:
			eq_id = str(qry_1.TRKOBJ_TRACKEDFIELD_LABEL)
		else:
			eq_id = "Chain Step" 

	elif TreeParam == "Customer Information" and TABLENAME == 'SAQTIP':
		qry = Sql.GetFirst(
		"SELECT PARTY_ID,PARTY_NAME FROM SAQTIP (NOLOCK) WHERE QUOTE_INVOLVED_PARTY_RECORD_ID = '{recid}'".format(recid=CURR_REC_ID)
		)
		if qry:
			eq_id = str(qry.PARTY_ID)
		else:
			eq_id = "Involved Parties"
	elif TreeParam == "Customer Information" and TABLENAME == 'SAQICT':
		qry = Sql.GetFirst(
		"SELECT CONTACT_ID FROM SAQICT (NOLOCK) WHERE QUOTE_REV_INVOLVED_PARTY_CONTACT_ID = '{recid}'".format(recid=CURR_REC_ID)
		)
		if qry:
			eq_id = str(qry.CONTACT_ID)
		else:
			eq_id = "Contacts"
	elif TABLENAME == 'SAQSAP':
		qry = Sql.GetFirst(
		"SELECT EQUIPMENT_ID,SERIAL_NO FROM SAQSAP (NOLOCK) WHERE QUOTE_SERVICE_COV_OBJ_ASS_PM_KIT_RECORD_ID = '{recid}'".format(recid=CURR_REC_ID)
		)
		if qry.SERIAL_NO: 
			eq_id = str(qry.EQUIPMENT_ID)+"-"+str(qry.SERIAL_NUMBER)
		elif qry:
			eq_id = str(qry.EQUIPMENT_ID)
		else:
			eq_id = "PM Events"
	##A055S000P01-8690 code starts..
	elif TABLENAME == 'SAQDLT':
		qry = Sql.GetFirst(
		"SELECT MEMBER_ID,MEMBER_NAME FROM SAQDLT (NOLOCK) WHERE QUOTE_REV_DEAL_TEAM_MEMBER_ID = '{recid}'".format(recid=CURR_REC_ID)
		)
		if qry:
			eq_id = str(qry.MEMBER_ID)
		else:
			eq_id = "Sales Team"
	##A055S000P01-8690 code ends..      
	elif TreeParam == "Contract Information" and TABLENAME == 'CTCTIP':
		qry = Sql.GetFirst(
		"SELECT PARTY_ID FROM CTCTIP (NOLOCK) WHERE CONTRACT_INVOLVED_PARTIES_RECORD_ID = '{recid}'".format(recid=CURR_REC_ID)
		)
		if qry:
			eq_id = str(qry.PARTY_ID)
		else:
			eq_id = "Involved Parties" 
	elif TreeParam == "Quote Information" and TABLENAME == 'SAQSCF':
		qry = Sql.GetFirst(
		"SELECT PARTY_ID FROM SAQTIP (NOLOCK) WHERE QUOTE_INVOLVED_PARTY_RECORD_ID = '{recid}'".format(recid=CURR_REC_ID)
		)
		qry_1 = Sql.GetFirst(
		"SELECT SRCFBL_ID FROM SAQSCF (NOLOCK) WHERE QUOTE_SOURCE_FAB_LOCATION_RECORD_ID = '{recid}'".format(recid=CURR_REC_ID)
		)
		if qry:
			eq_id = str(qry.PARTY_ID)
		elif qry_1:
			eq_id = str(qry_1.SRCFBL_ID)

	elif TreeParam == "Quote Information" and TABLENAME == 'SAQSTE':
		qry = Sql.GetFirst(
		"SELECT PARTY_ID FROM SAQTIP (NOLOCK) WHERE QUOTE_INVOLVED_PARTY_RECORD_ID = '{recid}'".format(recid=CURR_REC_ID)
		)
		
		qry_1 = Sql.GetFirst(
		"SELECT EQUIPMENT_ID FROM SAQSTE (NOLOCK) WHERE QUOTE_SOURCE_TARGET_FAB_LOC_EQUIP_RECORD_ID = '{recid}'".format(recid=CURR_REC_ID)
		)
		if qry:
			eq_id = str(qry.PARTY_ID)
		elif qry_1:
			eq_id = str(qry_1.EQUIPMENT_ID)
	elif TABLENAME == 'SAQSPT':        
		qry = Sql.GetFirst(
			"SELECT PART_NUMBER,PART_DESCRIPTION FROM SAQSPT (NOLOCK) WHERE QUOTE_SERVICE_PART_RECORD_ID = '{recid}'".format(recid=CURR_REC_ID)
		)
		if qry:
			eq_id = str(qry.PART_NUMBER)
	elif TABLENAME == 'SAQRSP':
		qry = Sql.GetFirst(
			"SELECT PART_NUMBER,PART_DESCRIPTION FROM SAQRSP (NOLOCK) WHERE QUOTE_REV_PO_PRODUCT_LIST_ID = '{recid}'".format(recid=CURR_REC_ID)
		)
		if qry:
			eq_id = str(qry.PART_NUMBER)
	elif TreeParam == "Quote Items" and TABLENAME == 'SAQRIT':
		qry = Sql.GetFirst(
			"SELECT LINE FROM SAQRIT (NOLOCK) WHERE QUOTE_REVISION_CONTRACT_ITEM_ID = '{recid}'".format(recid=CURR_REC_ID)
		)
		if qry:
			eq_id = str(qry.LINE)
		else:
			eq_id = "Line"
	Action_Str = '<li><a onclick="breadCrumb_redirection(this)">'
	Action_Str += '<abbr title="'+str(eq_id)+'">'
	Action_Str += str(eq_id)
	Action_Str += '</abbr></a><span class="angle_symbol"><img src="/mt/appliedmaterials_tst/images/productimages/BREADCRUMB_ICON_TRANS.PNG"></span></li>'

	return Action_Str

def BreadcrumbPartNumber():
	qry = ""
	eq_id = ""
	qry = Sql.GetFirst(
		"SELECT PART_NUMBER,PART_DESCRIPTION FROM SAQSPT (NOLOCK) WHERE QUOTE_SERVICE_PART_RECORD_ID = '{recid}'".format(recid=CURR_REC_ID)
	)
	if qry:
		eq_id = str(qry.PART_NUMBER)
	else:
		eq_id = str(qry.PART_DESCRIPTION)
	Action_Str = ""
	Action_Str = '<li><a onclick="breadCrumb_redirection(this)">'
	Action_Str += '<abbr title="'+str(eq_id)+'">'
	Action_Str += str(eq_id)
	Action_Str += '</abbr></a><span class="angle_symbol"><img src="/mt/appliedmaterials_tst/images/productimages/BREADCRUMB_ICON_TRANS.PNG"></span></li>'

	return Action_Str


def GetCovObjMaster(PerPage, PageInform, A_Keys, A_Values):    
	if str(PerPage) == "" and str(PageInform) == "":
		Page_start = 1
		Page_End = 10
		PerPage = 10
		PageInform = "1___10___10"
	else:
		Page_start = int(PageInform.split("___")[0])
		Page_End = int(PageInform.split("___")[1])
		PerPage = PerPage
	ContractRecordId = Quote.GetGlobal("contract_quote_record_id")
	RevisionRecordId = Quote.GetGlobal("quote_revision_record_id")
	TreeParam = Product.GetGlobal("TreeParam")
	TreeParentParam = Product.GetGlobal("TreeParentLevel0")
	TreeSuperParentParam = Product.GetGlobal("TreeParentLevel1")
	TreeTopSuperParentParam = Product.GetGlobal("TreeParentLevel2")
	
	# FablocationId = Product.GetGlobal("TreeParam")

	data_list = []
	obj_idval = "SYOBJ_00904_SYOBJ_00904"
	rec_id = "SYOBJ_00904"
	obj_id = "SYOBJ-00904"
	objh_getid = Sql.GetFirst(
		"SELECT TOP 1  RECORD_ID  FROM SYOBJH (NOLOCK) WHERE SAPCPQ_ATTRIBUTE_NAME='" + str(obj_id) + "'"
	)
	if objh_getid:
		obj_id = objh_getid.RECORD_ID
	objs_obj = Sql.GetFirst(
		"select CAN_ADD,CAN_EDIT,COLUMNS,CAN_DELETE from SYOBJR (NOLOCK) where OBJ_REC_ID = '" + str(obj_id) + "' "
	)
	can_edit = str(objs_obj.CAN_EDIT)
	can_add = str(objs_obj.CAN_ADD)
	can_delete = str(objs_obj.CAN_DELETE)
	table_id = "table_covered_obj_parent"
	table_header = (
		'<table id="'
		+ str(table_id)
		+ '"  data-pagination="false" data-sortable="true" data-search-on-enter-key="true" data-filter-control="true" data-pagination-loop = "false" data-locale = "en-US" ><thead>'
	)
	# service_type = Sql.GetList("select * from SAQTSV where QUOTE_RECORD_ID = '"+str(ContractRecordId)+"'")
	# for ser in service_type:
	#     if ser.SERVICE_ID == 'Z007_AG':
	#         Columns = [
	#             "QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID",
	#             "DESCRIPTION",
	#             "EQUIPMENT_ID",
	#             "SERIAL_NO",
	#             "CUSTOMER_TOOL_ID",
	#             "GREENBOOK",
	#             "EQUIPMENT_STATUS",
	#             "EQUIPMENT_DESCRIPTION",
	#             "MNT_PLANT_ID", 
	#             "SNDFBL_ID",           
	#             "FABLOCATION_ID",
	#             "WARRANTY_START_DATE",
	#             "WARRANTY_END_DATE"
	#         ]
	#     else: 
	Columns = [
		"QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID",
		"EQUIPMENT_CATEGORY_DESCRIPTION",
		"EQUIPMENT_ID",
		"SERIAL_NO",
		"CUSTOMER_TOOL_ID",
		"GREENBOOK",
		"EQUIPMENT_STATUS",
		"EQUIPMENT_DESCRIPTION",
		"MNT_PLANT_ID",                                   
		"FABLOCATION_ID",
		"WARRANTY_START_DATE",
		"WARRANTY_END_DATE",
		"WARRANTY_END_DATE_ALERT"
	]      
	Objd_Obj = Sql.GetList(
		"select FIELD_LABEL,API_NAME,LOOKUP_OBJECT,LOOKUP_API_NAME,DATA_TYPE from SYOBJD (NOLOCK) where OBJECT_NAME = 'SAQSCO'"
	)
	attr_list = []
	attrs_datatype_dict = {}
	lookup_disply_list = []
	lookup_str = ""
	if Objd_Obj is not None:
		attr_list = {}
		for attr in Objd_Obj:
			attr_list[str(attr.API_NAME)] = str(attr.FIELD_LABEL)
			attrs_datatype_dict[str(attr.API_NAME)] = str(attr.DATA_TYPE)
			if attr.LOOKUP_API_NAME != "" and attr.LOOKUP_API_NAME is not None:
				lookup_disply_list.append(str(attr.API_NAME))
		checkbox_list = [inn.API_NAME for inn in Objd_Obj if inn.DATA_TYPE == "CHECKBOX"]
		lookup_list = {ins.LOOKUP_API_NAME: ins.API_NAME for ins in Objd_Obj}
	lookup_str = ",".join(list(lookup_disply_list))
	if ((active_subtab == "Sending Equipment") or (active_subtab == "Receiving Equipment")) and TreeParentParam == 'Complementary Products':
		#Trace.Write('attr_list'+str(attr_list))
		if 'FABLOCATION_ID' in attr_list:
			fab_location_id  = attr_list['FABLOCATION_ID']
			attr_list['FABLOCATION_ID'] = 'Sending Fab Location' if active_subtab == "Sending Equipment" else 'Receiving Fab Location' if active_subtab == "Receiving Equipment" else fab_location_id
	Trace.Write('attr_list1221'+str(attr_list))
	Trace.Write('checkbox_list'+str(checkbox_list))
	orderby = ""
	if SortColumn != '' and SortColumnOrder !='':
		orderby = SortColumn + " " + SortColumnOrder
	else:
		orderby = "QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID"
	where_string = ""
	Trace.Write("CHKKKIIEE_J "+str(TreeParam))
	if A_Keys != "" and A_Values != "":
		A_Keys = list(A_Keys)
		A_Values = list(A_Values)
		for key, value in zip(A_Keys, A_Values):
			if value.strip():
				if where_string:
					where_string += " AND "
				where_string += "{Key} LIKE '%{Value}%'".format(Key=key, Value=value)
				
	
	if TreeSuperParentParam == "Product Offerings" or (TreeTopSuperParentParam== "Comprehensive Services" and TreeParentParam=="Add-On Products"):
		Qstr = (
			"select top "
			+ str(PerPage)
			+ " * from ( select ROW_NUMBER() OVER( ORDER BY "+str(orderby)+") AS ROW, QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,EQUIPMENT_ID,EQUIPMENT_DESCRIPTION,SERIAL_NO,GREENBOOK,FABLOCATION_ID,WARRANTY_END_DATE,WARRANTY_END_DATE_ALERT,WARRANTY_START_DATE,CONTRACT_VALID_FROM,CONTRACT_VALID_TO,MNT_PLANT_ID,EQUIPMENT_STATUS,CUSTOMER_TOOL_ID,EQUIPMENTCATEGORY_DESCRIPTION AS EQUIPMENT_CATEGORY_DESCRIPTION,SNDFBL_ID from SAQSCO (NOLOCK) where QUOTE_RECORD_ID = '"
			+ str(ContractRecordId)
			+ "' and QTEREV_RECORD_ID = '"
			+ str(RevisionRecordId)
			+ "' and SERVICE_ID = '"
			+ str(TreeParam)
			+ "' and SERVICE_TYPE = '"
			+ str(TreeParentParam)
			+ "'"
			+ ") m where m.ROW BETWEEN "
			+ str(Page_start)
			+ " and "
			+ str(Page_End)
		)
		
	elif TreeSuperParentParam == "Add-On Products":
		Qstr = (
			"select top "
			+ str(PerPage)
			+ " * from ( select ROW_NUMBER() OVER( ORDER BY "+str(orderby)+") AS ROW, QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,EQUIPMENT_ID,EQUIPMENT_DESCRIPTION,SERIAL_NO,GREENBOOK,FABLOCATION_ID,WARRANTY_END_DATE,WARRANTY_END_DATE_ALERT,WARRANTY_START_DATE,CONTRACT_VALID_FROM,CONTRACT_VALID_TO,MNT_PLANT_ID,EQUIPMENT_STATUS,CUSTOMER_TOOL_ID,EQUIPMENTCATEGORY_DESCRIPTION AS EQUIPMENT_CATEGORY_DESCRIPTION,SNDFBL_ID from SAQSCO (NOLOCK) where QUOTE_RECORD_ID = '"
			+ str(ContractRecordId)
			+ "' and QTEREV_RECORD_ID = '"
			+ str(RevisionRecordId)
			+ "' and SERVICE_ID = '"
			+ str(TreeParentParam)
			+ "' and SERVICE_TYPE = '"
			+ str(TreeSuperParentParam)
			+ "'"
			+ ") m where m.ROW BETWEEN "
			+ str(Page_start)
			+ " and "
			+ str(Page_End)
		)
	elif (str(TreeParam) == "Sending Equipment" or str(TreeParam) == "Receiving Equipment"):
		
		if str(where_string)!="":
			where_string = " AND "+str(where_string) 
		Qstr = (
			"select top "
			+ str(PerPage)
			+ " * from ( select ROW_NUMBER() OVER( ORDER BY QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID) AS ROW, QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,EQUIPMENT_ID,EQUIPMENT_DESCRIPTION,SERIAL_NO,GREENBOOK,FABLOCATION_ID,WARRANTY_END_DATE,WARRANTY_END_DATE_ALERT,WARRANTY_START_DATE,CONTRACT_VALID_FROM,CONTRACT_VALID_TO,MNT_PLANT_ID,EQUIPMENT_STATUS,CUSTOMER_TOOL_ID,EQUIPMENTCATEGORY_DESCRIPTION AS EQUIPMENT_CATEGORY_DESCRIPTION,SNDFBL_ID from SAQSCO (NOLOCK) where QUOTE_RECORD_ID = '"
			+ str(ContractRecordId)
			+ "' and QTEREV_RECORD_ID = '"
			+ str(RevisionRecordId)
			+ "' and SERVICE_ID = '"
			+ str(TreeParentParam)
			+ "' and SERVICE_TYPE = '"
			+ str(TreeSuperParentParam)
			+ "' and RELOCATION_EQUIPMENT_TYPE = '"
			+str(TreeParam)
			+ "' "+str(where_string)+" ) m where m.ROW BETWEEN "
			+ str(Page_start)
			+ " and "
			+ str(Page_End)
		)
	else:
		if TreeTopSuperParentParam == "Product Offerings":
			Qstr = (
				"select top "
				+ str(PerPage)
				+ " * from ( select ROW_NUMBER() OVER( ORDER BY QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID) AS ROW, QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,EQUIPMENT_ID,EQUIPMENT_DESCRIPTION,SERIAL_NO,GREENBOOK,FABLOCATION_ID,WARRANTY_END_DATE,WARRANTY_END_DATE_ALERT,WARRANTY_START_DATE,CONTRACT_VALID_FROM,CONTRACT_VALID_TO,MNT_PLANT_ID,EQUIPMENT_STATUS,CUSTOMER_TOOL_ID,EQUIPMENTCATEGORY_DESCRIPTION AS EQUIPMENT_CATEGORY_DESCRIPTION,SNDFBL_ID from SAQSCO (NOLOCK) where QUOTE_RECORD_ID = '"
				+ str(ContractRecordId)
				+ "'  and QTEREV_RECORD_ID = '"
				+ str(RevisionRecordId)
				+ "'and SERVICE_ID = '"
				+ str(TreeParentParam)
				+ "' and SERVICE_TYPE = '"
				+ str(TreeSuperParentParam)
				+ "' and GREENBOOK = '"
				+ str(TreeParam)
				+ "'"
				+ ") m where m.ROW BETWEEN "
				+ str(Page_start)
				+ " and "
				+ str(Page_End)
			)
			'''
			Qstr = (
				"select top "
				+ str(PerPage)
				+ " * from ( select ROW_NUMBER() OVER( ORDER BY QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID) AS ROW, QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,EQUIPMENT_ID,EQUIPMENT_DESCRIPTION,SERIAL_NO,GREENBOOK,FABLOCATION_ID,WARRANTY_END_DATE,WARRANTY_END_DATE_ALERT,WARRANTY_START_DATE,CONTRACT_VALID_FROM,CONTRACT_VALID_TO,MNT_PLANT_ID,EQUIPMENT_STATUS,CUSTOMER_TOOL_ID,EQUIPMENTCATEGORY_DESCRIPTION AS EQUIPMENT_CATEGORY_DESCRIPTION,SNDFBL_ID from SAQSCO (NOLOCK) where QUOTE_RECORD_ID = '"
				+ str(ContractRecordId)
				+ "'  and QTEREV_RECORD_ID = '"
				+ str(RevisionRecordId)
				+ "'and SERVICE_ID = '"
				+ str(TreeParentParam)
				+ "' and SERVICE_TYPE = '"
				+ str(TreeSuperParentParam)
				+ "' and FABLOCATION_ID = '"
				+ str(TreeParam)
				+ "'"
				+ ") m where m.ROW BETWEEN "
				+ str(Page_start)
				+ " and "
				+ str(Page_End)
			)
			'''
		elif TreeTopSuperParentParam == "Add-On Products" or TreeTopSuperParentParam == "Comprehensive Services" or TreeTopSuperParentParam == "Complementary Products":
			if TreeParentParam == "Receiving Equipment":
				Qstr = (
					"select top "
					+ str(PerPage)
					+ " * from ( select ROW_NUMBER() OVER( ORDER BY QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID) AS ROW, QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,EQUIPMENT_ID,EQUIPMENT_DESCRIPTION,SERIAL_NO,GREENBOOK,FABLOCATION_ID,WARRANTY_END_DATE,WARRANTY_END_DATE_ALERT,WARRANTY_START_DATE,CONTRACT_VALID_FROM,CONTRACT_VALID_TO,MNT_PLANT_ID,EQUIPMENT_STATUS,CUSTOMER_TOOL_ID,EQUIPMENTCATEGORY_DESCRIPTION AS EQUIPMENT_CATEGORY_DESCRIPTION,SNDFBL_ID from SAQSCO (NOLOCK) where QUOTE_RECORD_ID = '"
					+ str(ContractRecordId)
					+ "' and QTEREV_RECORD_ID = '"
					+ str(RevisionRecordId)
					+ "' AND SERVICE_ID = '"
					+ str(TreeSuperParentParam)
					+ "' and SERVICE_TYPE = '"
					+ str(TreeTopSuperParentParam)
					+ "' and FABLOCATION_ID = '"
					+ str(TreeParam)
					+ "') m where m.ROW BETWEEN "
					+ str(Page_start)
					+ " and "
					+ str(Page_End)
				) 
			else:
				Qstr = (
					"select top "
					+ str(PerPage)
					+ " * from ( select ROW_NUMBER() OVER( ORDER BY QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID) AS ROW, QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,EQUIPMENT_ID,EQUIPMENT_DESCRIPTION,SERIAL_NO,GREENBOOK,FABLOCATION_ID,WARRANTY_END_DATE,WARRANTY_END_DATE_ALERT,WARRANTY_START_DATE,CONTRACT_VALID_FROM,CONTRACT_VALID_TO,MNT_PLANT_ID,EQUIPMENT_STATUS,CUSTOMER_TOOL_ID,EQUIPMENTCATEGORY_DESCRIPTION AS EQUIPMENT_CATEGORY_DESCRIPTION,SNDFBL_ID from SAQSCO (NOLOCK) where QUOTE_RECORD_ID = '"
					+ str(ContractRecordId)
					+ "'  and QTEREV_RECORD_ID = '"
					+ str(RevisionRecordId)
					+ "' and SERVICE_TYPE = '"
					+ str(TreeSuperParentParam)
					+ "'and SERVICE_ID = '"
					+ str(TreeParentParam)
					+ "' and GREENBOOK = '"
					+ str(TreeParam)
					+ "') m where m.ROW BETWEEN "
					+ str(Page_start)
					+ " and "
					+ str(Page_End)
				) # NO FAB FOR PRODUCT OFFERINGS IN SPRINT-06
				'''
				Qstr = (
					"select top "
					+ str(PerPage)
					+ " * from ( select ROW_NUMBER() OVER( ORDER BY QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID) AS ROW, QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,EQUIPMENT_ID,EQUIPMENT_DESCRIPTION,SERIAL_NO,GREENBOOK,FABLOCATION_ID,WARRANTY_END_DATE,WARRANTY_END_DATE_ALERT,WARRANTY_START_DATE,CONTRACT_VALID_FROM,CONTRACT_VALID_TO,MNT_PLANT_ID,EQUIPMENT_STATUS,CUSTOMER_TOOL_ID,EQUIPMENTCATEGORY_DESCRIPTION AS EQUIPMENT_CATEGORY_DESCRIPTION,SNDFBL_ID from SAQSCO (NOLOCK) where QUOTE_RECORD_ID = '"
					+ str(ContractRecordId)
					+ "'  and QTEREV_RECORD_ID = '"
					+ str(RevisionRecordId)
					+ "'and SERVICE_ID = '"
					+ str(TreeSuperParentParam)
					+ "' and SERVICE_TYPE = '"
					+ str(TreeTopSuperParentParam)
					+ "' and FABLOCATION_ID = '"
					+ str(TreeParentParam)
					+ "' and GREENBOOK = '"
					+ str(TreeParam)
					+ "') m where m.ROW BETWEEN "
					+ str(Page_start)
					+ " and "
					+ str(Page_End)
				)
				'''
		
		elif TreeTopSuperParentParam == "Complementary Products" and TreeSuperParentParam in ("Receiving Equipment","Sending Equipment"):
			Qstr = (
				"select top "
				+ str(PerPage)
				+ " * from ( select ROW_NUMBER() OVER( ORDER BY QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID) AS ROW, QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,EQUIPMENT_ID,EQUIPMENT_DESCRIPTION,SERIAL_NO,GREENBOOK,FABLOCATION_ID,WARRANTY_END_DATE,WARRANTY_END_DATE_ALERT,WARRANTY_START_DATE,CONTRACT_VALID_FROM,CONTRACT_VALID_TO,MNT_PLANT_ID,EQUIPMENT_STATUS,CUSTOMER_TOOL_ID,EQUIPMENTCATEGORY_DESCRIPTION AS EQUIPMENT_CATEGORY_DESCRIPTION,SNDFBL_ID from SAQSCO (NOLOCK) where QUOTE_RECORD_ID = '"
				+ str(ContractRecordId)
				+ "' and QTEREV_RECORD_ID = '"
				+ str(RevisionRecordId)
				+ "' AND SERVICE_ID = '"
				+ str(TreeSuperParentParam)
				+ "' and SERVICE_TYPE = '"
				+ str(TreeTopSuperParentParam)
				+ "' AND FABLOCATION_ID = '"
				+ str(TreeParam)
				+ "'"
				+ ") m where m.ROW BETWEEN "
				+ str(Page_start)
				+ " and "
				+ str(Page_End)
			)
		elif TreeSuperParentParam == "Receiving Equipment":
			Qstr = (
				"select top "
				+ str(PerPage)
				+ " * from ( select ROW_NUMBER() OVER( ORDER BY QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID) AS ROW, QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,EQUIPMENT_ID,EQUIPMENT_DESCRIPTION,SERIAL_NO,GREENBOOK,FABLOCATION_ID,WARRANTY_END_DATE,WARRANTY_END_DATE_ALERT,WARRANTY_START_DATE,CONTRACT_VALID_FROM,CONTRACT_VALID_TO,MNT_PLANT_ID,EQUIPMENT_STATUS,CUSTOMER_TOOL_ID,EQUIPMENTCATEGORY_DESCRIPTION AS EQUIPMENT_CATEGORY_DESCRIPTION,SNDFBL_ID from SAQSCO (NOLOCK) where QUOTE_RECORD_ID = '"
				+ str(ContractRecordId)
				+ "' and QTEREV_RECORD_ID = '"
				+ str(RevisionRecordId)
				+ "'and SERVICE_ID = '"
				+ str(TreeTopSuperParentParam)
				+ "' AND FABLOCATION_ID = '"
				+ str(TreeParentParam)
				+ "' AND GREENBOOK = '"
				+str(TreeParam)
				+ "') m where m.ROW BETWEEN "
				+ str(Page_start)
				+ " and "
				+ str(Page_End)
			)
	QueryCount = ""
	if TreeSuperParentParam == "Product Offerings" or (TreeTopSuperParentParam== "Comprehensive Services" and TreeParentParam=="Add-On Products"):
		QueryCountObj = Sql.GetFirst(
			"select count(CpqTableEntryId) as cnt from SAQSCO (NOLOCK) where QUOTE_RECORD_ID = '"
			+ str(ContractRecordId)
			+ "' and QTEREV_RECORD_ID = '"
			+ str(RevisionRecordId)
			+ "' and SERVICE_TYPE = '"
			+ str(TreeParentParam)
			+ "' and SERVICE_ID = '"
			+ str(TreeParam)
			+ "'"
		)
	elif TreeSuperParentParam == "Add-On Products" :
		QueryCountObj = Sql.GetFirst(
			"select count(CpqTableEntryId) as cnt from SAQSCO (NOLOCK) where QUOTE_RECORD_ID = '"
			+ str(ContractRecordId)
			+ "' and QTEREV_RECORD_ID = '"
			+ str(RevisionRecordId)
			+ "' and SERVICE_TYPE = '"
			+ str(TreeSuperParentParam)
			+ "' and SERVICE_ID = '"
			+ str(TreeParentParam)
			+ "'"
		)
	elif (str(TreeParam).startswith("Sending") or str(TreeParam).startswith("Receiving")):
		QueryCountObj = Sql.GetFirst(
			"select count(CpqTableEntryId) as cnt from SAQSCO (NOLOCK) where QUOTE_RECORD_ID = '"
			+ str(ContractRecordId)
			+ "' and QTEREV_RECORD_ID = '"
			+ str(RevisionRecordId)
			+ "' and SERVICE_TYPE = '"
			+ str(TreeSuperParentParam)
			+ "' and SERVICE_ID = '"
			+ str(TreeParentParam)
			+ "' and RELOCATION_EQUIPMENT_TYPE = '"
			+str(TreeParam)
			+"'"
		)
	else:
		if TreeTopSuperParentParam == "Product Offerings" :
			QueryCountObj = Sql.GetFirst(
				"select count(CpqTableEntryId) as cnt from SAQSCO (NOLOCK) where QUOTE_RECORD_ID = '"
				+ str(ContractRecordId)
				+ "' and QTEREV_RECORD_ID = '"
				+ str(RevisionRecordId)
				+ "' and SERVICE_TYPE = '"
				+ str(TreeSuperParentParam)
				+ "' and SERVICE_ID = '"
				+ str(TreeParentParam)
				+ "'and FABLOCATION_ID = '"
				+ str(TreeParam)
				+ "'"
			)
		elif TreeTopSuperParentParam == "Add-On Products" or TreeTopSuperParentParam == "Comprehensive Services" or TreeTopSuperParentParam == "Complementary Products":
			if TreeParentParam == "Receiving Equipment":
				QueryCountObj = Sql.GetFirst(
					"select count(CpqTableEntryId) as cnt from SAQSCO (NOLOCK) where QUOTE_RECORD_ID = '"
					+ str(ContractRecordId)
					+ "' and QTEREV_RECORD_ID = '"
					+ str(RevisionRecordId)
					+ "' and SERVICE_TYPE = '"
					+ str(TreeTopSuperParentParam)
					+ "' and SERVICE_ID = '"
					+ str(TreeSuperParentParam)
					+ "' and FABLOCATION_ID = '"
					+ str(TreeParam)
					+"' "
				)
			else:
				QueryCountObj = Sql.GetFirst(
					"select count(CpqTableEntryId) as cnt from SAQSCO (NOLOCK) where QUOTE_RECORD_ID = '"
					+ str(ContractRecordId)
					+ "' and QTEREV_RECORD_ID = '"
					+ str(RevisionRecordId)
					+ "'and SERVICE_TYPE = '"
					+ str(TreeTopSuperParentParam)
					+ "' and SERVICE_ID = '"
					+ str(TreeSuperParentParam)
					+ "' and FABLOCATION_ID = '"
					+ str(TreeParentParam)
					+ "' and GREENBOOK = '"
					+ str(TreeParam) +"' "
				)
		elif TreeTopSuperParentParam == "Complementary Products":
			QueryCountObj = Sql.GetFirst(
				"select count(CpqTableEntryId) as cnt from SAQSCO (NOLOCK) where QUOTE_RECORD_ID = '"
				+ str(ContractRecordId)
				+ "'  and QTEREV_RECORD_ID = '"
				+ str(RevisionRecordId)
				+ "' and SERVICE_TYPE = '"
				+ str(TreeTopSuperParentParam)
				+ "' and SERVICE_ID = '"
				+ str(TreeSuperParentParam)
				+ "' AND FABLOCATION_ID = '"
				+ str(TreeParam)
				+ "'"
			)
		elif TreeSuperParentParam == "Receiving Equipment":
			QueryCountObj = Sql.GetFirst(
				"select count(CpqTableEntryId) as cnt from SAQSCO (NOLOCK) where QUOTE_RECORD_ID = '"
				+ str(ContractRecordId)
				+ "' and QTEREV_RECORD_ID = '"
				+ str(RevisionRecordId)
				+ "' and SERVICE_ID = '"
				+ str(TreeTopSuperParentParam)
				+ "' AND FABLOCATION_ID = '"
				+ str(TreeParentParam)
				+ "' AND GREENBOOK = '"
				+str(TreeParam)
				+"'"
			)
	if QueryCountObj is not None:
		QueryCount = QueryCountObj.cnt
	parent_obj = Sql.GetList(Qstr)
	
	for par in parent_obj:
		data_id = str(par.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID)
		Trace.Write('Qstr-WARRANTY_END_DATE_ALERT ----'+str(par.WARRANTY_END_DATE_ALERT))
		Action_str = (
			'<div class="btn-group dropdown"><div class="dropdown" id="ctr_drop"><i data-toggle="dropdown" id="dropdownMenuButton" class="fa fa-sort-desc dropdown-toggle" aria-expanded="false"></i><ul class="dropdown-menu left" aria-labelledby="dropdownMenuButton"><li><a class="dropdown-item cur_sty" href="#" id="'
			+ str(data_id)
			+ '" onclick="Commonteree_view_RL(this)">VIEW</a></li>'
			+ '<li><a class="dropdown-item" id="deletebtn" data-target="#cont_CommonModalDelete" data-toggle="modal" onclick="CommonDelete(this, \'SAQSCO#'+ data_id +'\', \'WARNING\')" href="#">DELETE</a></li>'
		)
		if can_edit.upper() == "TRUE":
			Action_str += (
				'<li style="display:none" ><a class="dropdown-item cur_sty" href="#" id="'
				+ str(data_id)
				+ '" onclick="Move_to_parent_obj_edit(this)">EDIT</a></li>'
			)
		"""if can_delete.upper() == "TRUE":
			Action_str += '<li><a class="dropdown-item" data-target="#cont_viewModal_Material_Delete" data-toggle="modal" onclick="Material_delete_obj(this)" href="#">DELETE</a></li>'
		if can_add.upper() == "TRUE" and par.MARKET_TYPE == "NON MARKET BASED" and par.MODEL_TYPE != "COST PLUS":
			Action_str += (
				'<li><a class="dropdown-item" id="'
				+ str(data_id)
				+ '" data-target="#" data-toggle="modal" onclick="Pricebook_clone_obj(this)" href="#">CLONE</a></li>'
			)"""
		Action_str += "</ul></div></div>"

		# Data formation in dictonary format.
		## hyperlink
		data_dict = {}
		data_dict["ids"] = str(data_id)
		data_dict["ACTIONS"] = str(Action_str)
		data_dict["QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID"] = CPQID.KeyCPQId.GetCPQId(
			"SAQSCO", str(par.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID)
		)
		data_dict["EQUIPMENT_ID"] = ('<abbr id ="" title="' + str(par.EQUIPMENT_ID) + '">' + str(par.EQUIPMENT_ID) + "</abbr>") 
		data_dict["EQUIPMENT_DESCRIPTION"] = ('<abbr id ="" title="' + str(par.EQUIPMENT_DESCRIPTION) + '">' + str(par.EQUIPMENT_DESCRIPTION) + "</abbr>")
		data_dict["FABLOCATION_ID"] = ('<abbr id ="" title="' + str(par.SNDFBL_ID) + '">' + str(par.FABLOCATION_ID) + "</abbr>") 
		data_dict["SNDFBL_ID"] = ('<abbr id ="" title="' + str(par.FABLOCATION_ID) + '">' + str(par.SNDFBL_ID) + "</abbr>") 
		data_dict["GREENBOOK"] = ('<abbr id ="" title="' + str(par.GREENBOOK) + '">' + str(par.GREENBOOK) + "</abbr>") 
		data_dict["SERIAL_NO"] = ('<abbr id ="" title="' + str(par.SERIAL_NO) + '">' + str(par.SERIAL_NO) + "</abbr>") 
		data_dict["EQUIPMENT_CATEGORY_DESCRIPTION"] = ('<abbr id ="" title="' + str(par.EQUIPMENT_CATEGORY_DESCRIPTION) + '">' + str(par.EQUIPMENT_CATEGORY_DESCRIPTION) + "</abbr>") 
		data_dict["CUSTOMER_TOOL_ID"] = ('<abbr id ="" title="' + str(par.CUSTOMER_TOOL_ID) + '">' + str(par.CUSTOMER_TOOL_ID) + "</abbr>") 
		data_dict["EQUIPMENT_STATUS"] = ('<abbr id ="" title="' + str(par.EQUIPMENT_STATUS) + '">' + str(par.EQUIPMENT_STATUS) + "</abbr>") 
		data_dict["MNT_PLANT_ID"] = ('<abbr id ="" title="' + str(par.MNT_PLANT_ID) + '">' + str(par.MNT_PLANT_ID) + "</abbr>") 
		data_dict["WARRANTY_START_DATE"] = ('<abbr id ="" title="' + str(par.WARRANTY_START_DATE) + '">' + str(par.WARRANTY_START_DATE) + "</abbr>")
		data_dict["WARRANTY_END_DATE"] = ('<abbr id ="" title="' + str(par.WARRANTY_END_DATE) + '">' + str(par.WARRANTY_END_DATE) + "</abbr>") 
		data_dict["WARRANTY_END_DATE_ALERT"] = str(par.WARRANTY_END_DATE_ALERT) 
		#data_dict["CONTRACT_START_DATE"] = ('<abbr id ="" title="' + str(par.CONTRACT_START_DATE) + '">' + str(par.CONTRACT_START_DATE) + "</abbr>")
		#data_dict["CONTRACT_END_DATE"] = ('<abbr id ="" title="' + str(par.CONTRACT_END_DATE) + '">' + str(par.CONTRACT_END_DATE) + "</abbr>")
		data_list.append(data_dict)
	Trace.Write('data_list--'+str(data_list))
	hyper_link = ["QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID"]
	table_header += "<tr>"
	table_header += (
		'<th data-field="ACTIONS"><div class="action_col">ACTIONS</div><button class="searched_button" id="Act_'
		+ str(table_id)
		+ '">Search</button></th>'
	)
	table_header += '<th data-field="SELECT" class="wid45" data-checkbox="true"></th>'
	for key, invs in enumerate(list(Columns)):
		invs = str(invs).strip()
		qstring = attr_list.get(str(invs)) or ""
		if qstring == "":
			qstring = invs.replace("_", " ")
		if checkbox_list is not None and invs in checkbox_list:
			table_header += (
				'<th  data-field="'
				+ str(invs)
				+ '" data-filter-control="input" data-align="center" data-formatter="CheckboxFieldRelatedList" data-sortable="true"><abbr title="'
				+ str(qstring)
				+ '">'
				+ str(qstring)
				+ "</abbr></th>"
			)
		elif hyper_link is not None and invs in hyper_link:
			table_header += (
				'<th data-field="'
				+ str(invs)
				+ '" data-filter-control="input" data-formatter="covObjHyperLinkTreeLink" data-sortable="true"><abbr title="'
				+ str(qstring)
				+ '">'
				+ str(qstring)
				+ "</abbr></th>"
			)
		else:
			
			if str(invs) == "WARRANTY_START_DATE" or str(invs) == "WARRANTY_END_DATE":
				table_header += (
					'<th  data-field="'
					+ str(invs)
					+ '" data-filter-control="input" data-align="center" data-sortable="true"><abbr title="'
					+ str(qstring)
					+ '">'
					+ str(qstring)
					+ "</abbr></th>"
				)
			else:
				table_header += (
					'<th  data-field="'
					+ str(invs)
					+ '" data-filter-control="input" data-sortable="true"><abbr title="'
					+ str(qstring)
					+ '">'
					+ str(qstring)
					+ "</abbr></th>"
				)
	table_header += "</tr>"
	table_header += '</thead><tbody onclick="Table_Onclick_Scroll(this)"></tbody></table>'
	table_ids = "#" + str(table_id)
	filter_control_function = ""
	values_list = ""
	tbl_id = table_id
	for key, invs in enumerate(list(Columns)):
		table_ids = "#" + str(table_id)
		filter_clas = "#" + str(table_id) + " .bootstrap-table-filter-control-" + str(invs)
		values_list += "var " + str(invs) + ' = $("' + str(filter_clas) + '").val(); '
		values_list += "ATTRIBUTE_VALUEList.push(" + str(invs) + "); "
		tbl_id = table_id
	filter_class = "#Act_" + str(table_id)
	filter_control_function += (
		'$("'
		+ filter_class
		+ '").click( function(){ var table_id = $(this).closest("table").attr("id"); ATTRIBUTE_VALUEList = []; '
		+ str(values_list)
		+ ' var attribute_value = $(this).val(); cpq.server.executeScript("CQNESTGRID", {"TABNAME":"Covered Object Parent", "ACTION":"PRODUCT_ONLOAD_FILTER", "ATTRIBUTE_NAME": '
		+ str(list(Columns))
		+ ', "ATTRIBUTE_VALUE": ATTRIBUTE_VALUEList }, function(dataset) { data2 = dataset[1];  data1 = dataset[0]; data3 = dataset[2]; console.log("len ---->"+data1.length);  try { if(data1.length > 0) { $("#'+ str(tbl_id)  + '").bootstrapTable("load", data1 ); $("#noRecDisp").remove(); if (document.getElementById("'+str(tbl_id) + '___totalItemCount")){document.getElementById("'+str(tbl_id)+ '___totalItemCount").innerHTML = data2;}  if (document.getElementById("'+str(tbl_id) + '___NumberofItem")) {document.getElementById("'+str(tbl_id)+ '___NumberofItem").innerHTML = data3;}} else{ $("#' + str(tbl_id) + '").bootstrapTable("load", data1  );$("#' + str(tbl_id) + '").after("<div id=\'noRecDisp\' class=\'noRecord\'>No Records to Display</div>"); $(".noRecord:not(:first)").remove(); if (document.getElementById("'+str(tbl_id) + '___totalItemCount")){document.getElementById("'+str(tbl_id)+ '___totalItemCount").innerHTML = data2;}  if (document.getElementById("'+str(tbl_id) + '___NumberofItem")) {document.getElementById("'+str(tbl_id)+ '___NumberofItem").innerHTML = data3;$("td:has(#WARRANTY_END_DATE_ALERT)").addClass("pos-relative");} }} catch(err){} }); filter_search_click();$(".JColResizer").mousedown(function(){ $("thead.fullHeadFirst").css("cssText","z-index: 2;border-top: 1px solid rgb(220, 220, 220);top: 154px;border-right: 0px !important;");$("thead.fullHeadSecond").css("display","none"); });$(".JColResizer").mouseup(function(){ var th_width_resize = [];$("#table_covered_obj_parent thead.fullHeadFirst tr th").each(function(index){var wid = $(this).css("width"); if(index ==0 || index ==1){th_width_resize.push("60px");}else{th_width_resize.push(wid);}}); $("thead.fullHeadFirst").css("cssText","position: fixed;z-index: 2;border-top: 1px solid rgb(220, 220, 220); top: 154px;border-right: 0px !important;");$("thead.fullHeadSecond").css("display","table-header-group");$("#table_covered_obj_parent thead.fullHeadFirst tr th").each(function(index){var num = th_width_resize[index].split("px");var numsp = parseInt(num[0]);numsp = numsp - 1;var make_str =numsp+"px"; var c = "width:"+make_str+";white-space: nowrap;overflow: hidden;text-overflow: ellipsis;";var d = "width:"+make_str+";"; $(this).css("cssText",c);$(this).children("div:first-child").css("cssText",c);$(this).children("div.fht-cell").css("cssText",d);});$("#table_covered_obj_parent thead.fullHeadSecond tr th").each(function(index){var num = th_width_resize[index].split("px");var numsp = parseInt(num[0]);numsp = numsp - 1;var make_str =numsp+"px"; var c = "width:"+make_str+";white-space: nowrap;overflow: hidden;text-overflow: ellipsis;";var d = "width:"+make_str+";"; $(this).css("cssText",c);$(this).children("div:first-child").css("cssText",c);$(this).children("div.fht-cell").css("cssText",d);}); });});'
	)
	cls = "eq(2)"
	dbl_clk_function = (
				'$("'
				+ str(table_ids)
				+ '").on("dbl-click-cell.bs.table", onClickCell); $("'
				+ str(table_ids)
				+ '").on("all.bs.table", function (e, name, args) { $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); }); $("'
				+ str(table_ids)
				+ '\ th.bs-checkbox div.th-inner").before("<div class=\'pad0brdbt\' >SELECT</div>"); $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); function onClickCell(event, field, value, row, $element) { var reco_id=""; var reco = []; reco = localStorage.getItem("multiedit_checkbox_clicked"); if (reco === null || reco === undefined ){ reco = []; } if (reco.length > 0){reco = reco.split(",");} if (reco.length > 0){ reco.push($element.closest("tr").find("td:'
				+ str(cls)
				+ '").text());  data1 = $element.closest("tr").find("td:'
				+ str(cls)
				+ '").text(); localStorage.setItem("multiedit_save_date", data1); reco_id = removeDuplicates(reco); }else{reco_id=$element.closest("tr").find("td:'
				+ str(cls)
				+ '").text();localStorage.setItem("multiedit_selectall","no"); selectAll = false; rowselected = $("#table_covered_obj_parent tbody tr.selected").find(\'[type="checkbox"]:checked\').length; if(rowselected == 0){ $("#cont_multiEditModalSection").hide(); selectAll = "noselection"} $("#table_covered_obj_parent").find(\'[type="checkbox"]:checked\').map(function () {if ($(this).attr("name")== "btSelectAll"){selectAll = true; localStorage.setItem("multiedit_selectall","yes");} }); reco_id=reco_id.split(","); localStorage.setItem("multiedit_save_date", reco_id); } localStorage.setItem("multiedit_data_clicked", reco_id); localStorage.setItem("table_id_RL_edit", "'
				+ str(table_id)
				+ '");   cpq.server.executeScript("SYBLKETRLG", {"TITLE":field, "VALUE":value, "CLICKEDID":"'
				+ str(table_id)
				+ '", "RECORDID":reco_id, "ELEMENT":"RELATEDEDIT", "SELECTALL":selectAll }, function(data) { data1=data[0]; data2=data[1]; if(data1 != "NO"){ if(document.getElementById("RL_EDIT_DIV_ID") ) { document.getElementById("RL_EDIT_DIV_ID").innerHTML = data1; document.getElementById("cont_multiEditModalSection").style.display = "block"; $("#cont_multiEditModalSection").prepend("<div class=\'modal-backdrop fade in\'></div>"); var divHeight = $("#cont_multiEditModalSection").height(); $("#cont_multiEditModalSection .modal-backdrop").css("min-height", divHeight+"px"); $("#cont_multiEditModalSection .modal-dialog").css("width","550px"); $(".modal-dialog").css("margin-top","100px"); }TreeParentParam = localStorage.getItem("CommonTreeParentParam");var sparePartsBulkSAVEBtn = $(".secondary_highlight_panel").find("button#spare-parts-bulk-save-btn");var sparePartsBulkEDITBtn = $(".secondary_highlight_panel").find("button#spare-parts-bulk-edit-btn");var sparePartsBulkAddBtn = $(".secondary_highlight_panel").find("button#spare-parts-bulk-add-modal-btn"); if (data2.length !== 0){ $.each( data2, function( key, values ) { onclick_datepicker(values) }); } } }); }                   $("'
				+ str(table_ids)
				+ "\").on('sort.bs.table', function (e, name, order) {  currenttab = $(\"ul#carttabs_head .active\").text().trim(); localStorage.setItem('"
				+ str(table_id)
				+ "_SortColumn', name); localStorage.setItem('"
				+ str(table_id)
				+ "_SortColumnOrder', order); NestedContainerSorting(name, order, '"
				+ str(table_id)
				+ "'); }); "
			)
	#Trace.Write("12345 dbl_clk_function --->"+str(dbl_clk_function))
	NORECORDS = ""
	if len(data_list) == 0:
		NORECORDS = "NORECORDS"

	ObjectName = "SAQSCO"
	DropDownList = []
	filter_level_list = []
	filter_clas_name = ""
	cv_list = []
	TableclassName = "form-control" + table_id
	for key, col_name in enumerate(list(Columns)):
		StringValue_list = []
		objss_obj = Sql.GetFirst(
			"SELECT API_NAME, DATA_TYPE, FORMULA_LOGIC, PICKLIST FROM SYOBJD (NOLOCK) WHERE OBJECT_NAME='"
			+ str(ObjectName)
			+ "' and API_NAME = '"
			+ str(col_name)
			+ "'"
		)
		try:
			FORMULA_LOGIC = objss_obj.FORMULA_LOGIC.strip()
			FORMULA_col = FORMULA_LOGIC.split(" ")[1].strip()
			FORMULA_table = FORMULA_LOGIC.split(" ")[3].strip()
			ins_obj = Sql.GetFirst(
				"SELECT API_NAME, DATA_TYPE,PICKLIST FROM SYOBJD (NOLOCK) WHERE OBJECT_NAME='"
				+ str(FORMULA_table)
				+ "' and API_NAME = '"
				+ str(FORMULA_col)
				+ "'"
			)
			if str(objss_obj.PICKLIST).upper() == "TRUE":
				filter_level_data = "select"
				filter_clas_name = (
					'<div id = "'
					+ str(table_id)
					+ "_RelatedMutipleCheckBoxDrop_"
					+ str(key)
					+ '" class="form-control bootstrap-table-filter-control-'
					+ str(col_name)
					+ " RelatedMutipleCheckBoxDrop_"
					+ str(key)
					+ ' "></div>'
				)
				filter_level_list.append(filter_level_data)
			else:
				filter_level_data = "input"
				filter_clas_name = (
					'<input type="text" class="width100_vis form-control bootstrap-table-filter-control-'
					+ str(col_name)
					+ '">'
				)
				filter_level_list.append(filter_level_data)
		except:
			"""if str(objss_obj.PICKLIST).upper() == "TRUE":
				filter_level_data = "select"
				filter_clas_name = (
					'<div id = "'
					+ str(table_id)
					+ "_RelatedMutipleCheckBoxDrop_"
					+ str(key)
					+ '" class="form-control bootstrap-table-filter-control-'
					+ str(col_name)
					+ " RelatedMutipleCheckBoxDrop_"
					+ str(key)
					+ ' "></div>'
				)
				filter_level_list.append(filter_level_data)"""

			filter_level_data = "input"
			filter_clas_name = (
				'<input type="text" class="width100_vis form-control bootstrap-table-filter-control-' + str(col_name) + '">'
			)
			filter_level_list.append(filter_level_data)
		cv_list.append(filter_clas_name)
		if filter_level_data == "select":
			try:
				xcd = Sql.GetFirst(
					"SELECT (STUFF((SELECT DISTINCT ', ' + CAST("
					+ str(col_name)
					+ " AS CHAR(100)) FROM "
					+ str(ObjectName)
					+ " (NOLOCK) FOR XML PATH('') ), 1, 2, '')  ) AS StringValue"
				)
			except:
				xcd = Sql.GetFirst(
					"SELECT (STUFF((SELECT DISTINCT ', ' + CAST("
					+ str(col_name)
					+ " AS CHAR(100)) FROM "
					+ str(ObjectName)
					+ " (NOLOCK) FOR XML PATH('') ), 1, 2, '')  ) AS StringValue"
				)
			if str(xcd.StringValue) is not None and str(xcd.StringValue) != "":
				if str(xcd.StringValue).find(",") != -1:
					StringValue_list = [ins.strip() for ins in str(xcd.StringValue).split(",") if ins.strip() != ""]
				else:
					StringValue_list.append(str(xcd.StringValue))
			else:
				StringValue_list = [""]
			
			StringValue_list = list(set(StringValue_list))
			DropDownList.append(StringValue_list)
		elif filter_level_data == "checkbox":
			DropDownList.append(["True", "False"])
		else:
			DropDownList.append("")
		#Trace.Write("StringValue_list"+str(StringValue_list))
	RelatedDrop_str = (
		"try { if( document.getElementById('"
		+ str(table_id)
		+ "') ) { var listws = document.getElementById('"
		+ str(table_id)
		+ "').getElementsByClassName('filter-control');  for (i = 0; i < listws.length; i++) { document.getElementById('"
		+ str(table_id)
		+ "').getElementsByClassName('filter-control')[i].innerHTML = data6[i];  } for (j = 0; j < listws.length; j++) { if (data7[j] == 'select') { if (data8[j]) { var dataAdapter = new $.jqx.dataAdapter(data8[j]); $('#"
		+ str(table_id)
		+ "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter, autoDropDownHeight: true }); } } } } }  catch(err) { setTimeout(function() { var listws = document.getElementById('"
		+ str(table_id)
		+ "').getElementsByClassName('filter-control');  for (i = 0; i < listws.length; i++) { document.getElementById('"
		+ str(table_id)
		+ "').getElementsByClassName('filter-control')[i].innerHTML = data6[i];  } for (j = 0; j < listws.length; j++) { if (data7[j] == 'select') { if (data8[j]) { var dataAdapter = new $.jqx.dataAdapter(data8[j]); $('#"
		+ str(table_id)
		+ "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter, autoDropDownHeight: true }); } } } }, 5000); }"
	)
	## Pagination code starts....
	if int(QueryCount) < int(PerPage):
		Action_Str = str(Page_start) + " - " + str(QueryCount)+ " of"
	elif QueryCount == PerPage:
		Action_Str = str(Page_start) + " - " + str(PerPage)+ " of"
	else:
		Action_Str = str(Page_start) + " - " + str(Page_End)+ " of"

	Test = (
		'<div class="col-md-12 brdr listContStyle pad2height30" ><div class="col-md-4 pager-numberofitem clear-padding"><span class="pager-number-of-items-item noofitem" id="'
		+ str(table_id)
		+ '___NumberofItem">'
		+ str(Action_Str)
		+ '</span><span class="pager-number-of-items-item fltltpad2mrg0" id="'
		+ str(table_id)
		+ '___totalItemCount" >'
		+ str(QueryCount)
		+ '</span><div class="clear-padding fltltmrgtp3" ><div  class="pull-right vertmidtxtrht"><select onchange="PageFunctestChild(this,\'Quote\',\'\',\'table_covered_obj_parent\')" id="'
		+ str(table_id)
		+ '___PageCountValue" class="form-control wid65vermiddisinbmarl5"><option value="10" selected>10</option><option value="20">20</option><option value="50">50</option><option value="100">100</option><option value="200">200</option></select> </div></div></div><div class="col-xs-8 col-md-4  clear-padding disinpad10txtcen"  data-bind="visible: totalItemCount"><div class="clear-padding col-xs-12 col-sm-6 col-md-12 bor0" ><ul class="pagination pagination"><li class="disabled"><a href="#" onclick="FirstPageLoad_paginationChild(\'Quote\',\'\',\''
		+str(table_id)
		+'\')"><i class="fa fa-caret-left font14whtbld" ></i><i class="fa fa-caret-left font14" ></i></a></li><li class="disabled"><a href="#" onclick="Previous12334Child(\'Quote\',\'\',\'table_covered_obj_parent\')"><i class="fa fa-caret-left font14" ></i>PREVIOUS</a></li><li class="disabled"><a href="#" class="disabledPage" onclick="Next12334Child(\'Quote\',\'\',\'table_covered_obj_parent\')">NEXT<i class="fa fa-caret-right font14" ></i></a></li><li class="disabled"><a href="#" onclick="LastPageLoad_paginationChild(\'Quote\',\'\',\''
		+str(table_id)
		+'\')" class="disabledPage"><i class="fa fa-caret-right font14"></i><i class="fa fa-caret-right font14whtbld"></i></a></li></ul></div> </div> <div class="col-md-4 pr_page_pad"> <span  id="'
		+ str(table_id)
		+ '___page_count" class="currentPage page_right_content">1</span><span class="page_right_content pad_rt_2">Page </span></div></div>'
	) 
	if Page_End > QueryCount:
		Page_End = QueryCount
	else:
		Page_End = Page_End
	
	Action_Str = ""
	Action_Str += str(Page_start)+" - "
	Action_Str += str(Page_End)
	Action_Str += " of"
	#pagination code ends...
	# To Hide Add On Products Subtab
	quote_record_id = Quote.GetGlobal("contract_quote_record_id")
	if TreeParentParam == "Comprehensive Services" and TreeSuperParentParam == "Product Offerings":        
		quoteid = Quote.GetGlobal("contract_quote_record_id")
		RevisionRecordId = Quote.GetGlobal("quote_revision_record_id")
		addon_details = Sql.GetList("SELECT SERVICE_ID FROM SAQSAO (NOLOCK) WHERE SERVICE_ID = '"+str(TreeParam)+"'")
		equipment_details = Sql.GetFirst("SELECT * FROM SAQSCO (NOLOCK) WHERE SERVICE_ID = '"+str(TreeParam)+"' AND QUOTE_RECORD_ID ='"+str(quoteid)+"' AND QTEREV_RECORD_ID ='"+str(RevisionRecordId)+"' ")
		if addon_details and equipment_details:
			Ad_on_prd = "True"
		else:
			Ad_on_prd = "False"
	else:
		Ad_on_prd = ""
	return (
		table_header,
		data_list,
		table_id,
		filter_control_function,
		NORECORDS,
		dbl_clk_function,
		cv_list,
		filter_level_list,
		DropDownList,
		RelatedDrop_str,
		Test,
		Action_Str,
		Ad_on_prd,
		checkbox_list
	)

def GetSendEupChildFilter(ATTRIBUTE_NAME, ATTRIBUTE_VALUE,RECID,PerPage,PageInform):
	if str(PerPage) == "" and str(PageInform) == "":
		Page_start = 1
		Page_End = 10
		PerPage = 10
		PageInform = "1___10___10"
	else:
		Page_start = int(PageInform.split("___")[0])
		Page_End = int(PageInform.split("___")[1])
		PerPage = PerPage
	QueryCount = ""
	TreeParam = Product.GetGlobal("TreeParam")
	TreeParentParam = Product.GetGlobal("TreeParentLevel0")
	TreeSuperParentParam = Product.GetGlobal("TreeParentLevel1")
	TreeTopSuperParentParam = Product.GetGlobal("TreeParentLevel2")
	# FablocationId = Product.GetGlobal("TreeParam")
	ContractRecordId = Quote.GetGlobal("contract_quote_record_id")
	RevisionRecordId = Quote.GetGlobal("quote_revision_record_id")
	ATTRIBUTE_VALUE_STR = ""
	Dict_formation = dict(zip(ATTRIBUTE_NAME, ATTRIBUTE_VALUE))
	
	
	for quer_key, quer_value in enumerate(Dict_formation):
		try:
			x_picklistcheckobj = Sql.GetFirst(
				"SELECT PICKLIST FROM SYOBJD (NOLOCK) WHERE OBJECT_NAME ='SAQSSA' AND API_NAME = '" + str(quer_value) + "'"
			)
			x_picklistcheck = str(x_picklistcheckobj.PICKLIST).upper()
		except:
			x_picklistcheck = ""    
		if Dict_formation.get(quer_value) != "":
			quer_values = str(Dict_formation.get(quer_value)).strip()
			if str(quer_values).upper() == "TRUE":
				quer_values = "TRUE"
			elif str(quer_values).upper() == "FALSE":
				quer_values = "FALSE"
			if str(quer_values).find(",") == -1:
				if x_picklistcheck == "TRUE":
					ATTRIBUTE_VALUE_STR += str(quer_value) + " = '" + str(quer_values) + "' and "
				else:
					ATTRIBUTE_VALUE_STR += str(quer_value) + " like '%" + str(quer_values) + "%' and "
			else:
				quer_values = quer_values.split(",")
				quer_values = tuple(list(quer_values))
				ATTRIBUTE_VALUE_STR += str(quer_value) + " in " + str(quer_values) + " and "

	data_list = []
	rec_id = "SYOBJ_1176889_SYOBJ_1176889"
	obj_id = "SYOBJ-1176889"
	objh_getid = Sql.GetFirst(
		"SELECT TOP 1  RECORD_ID  FROM SYOBJH (NOLOCK) WHERE SAPCPQ_ATTRIBUTE_NAME='" + str(obj_id) + "'"
	)
	if objh_getid:
		obj_id = objh_getid.RECORD_ID
	objs_obj = Sql.GetFirst(
		"select CAN_ADD,CAN_EDIT,COLUMNS,CAN_DELETE from SYOBJR (NOLOCK) where OBJ_REC_ID = '" + str(obj_id) + "' "
	)
	
	orderby = ""
	if SortColumn != '' and SortColumnOrder !='':
		orderby = SortColumn + " " + SortColumnOrder
	else:
		orderby = "QUOTE_SERVICE_SENDING_FAB_EQUIP_ASS_ID"
	
	
	can_edit = str(objs_obj.CAN_EDIT)
	can_clone = str(objs_obj.CAN_ADD)
	can_delete = str(objs_obj.CAN_DELETE)
	if ATTRIBUTE_VALUE is None or ATTRIBUTE_VALUE == "" or ATTRIBUTE_VALUE_STR is None or ATTRIBUTE_VALUE_STR == "":
		Trace.Write("empty search")
		if TreeSuperParentParam == "Product Offerings":
			parent_obj = Sql.GetList("select top "+str(PerPage)+"  QUOTE_SERVICE_SENDING_FAB_EQUIP_ASS_ID,SND_EQUIPMENT_ID,SND_ASSEMBLY_ID,SND_ASSEMBLY_DESCRIPTION,GOT_CODE, SND_EQUIPMENT_DESCRIPTION,SNDFBL_ID,INCLUDED,GREENBOOK,EQUIPMENTTYPE_ID,EQUIPMENTCATEGORY_ID from SAQSSA (NOLOCK) where SND_EQUIPMENT_ID = '{recid}' and QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' and SERVICE_ID = '{treeparam}' ORDER BY {ord_by} ".format(ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"),recid=RECID, treeparam=TreeParam,ord_by = orderby
				)
			)
			
			QueryCountObj = Sql.GetFirst(
					"select count(*) as cnt from SAQSSA (NOLOCK) where SND_EQUIPMENT_ID = '{recid}' and QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' and SERVICE_ID = '{treeparam}' ".format(
					ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"), recid=RECID, treeparam=TreeParam))
			if QueryCountObj is not None:
				QueryCount = QueryCountObj.cnt
			
			
			
		else:
			if TreeTopSuperParentParam == "Product Offerings":
				parent_obj = Sql.GetList( "select top "+str(PerPage)+"  QUOTE_SERVICE_SENDING_FAB_EQUIP_ASS_ID,SND_EQUIPMENT_ID,SND_ASSEMBLY_ID,SND_ASSEMBLY_DESCRIPTION,GOT_CODE, SND_EQUIPMENT_DESCRIPTION,SNDFBL_ID,INCLUDED,GREENBOOK,EQUIPMENTTYPE_ID,EQUIPMENTCATEGORY_ID from SAQSSA (NOLOCK) where SND_EQUIPMENT_ID = '{recid}' and QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' and SERVICE_ID = '{treeparam}' ORDER BY {ord_by} ".format( ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"), recid=RECID, treeparam=TreeParentParam,ord_by = orderby
					)
				)
				
				QueryCountObj = Sql.GetFirst( "select count(*) as cnt from SAQSSA (NOLOCK) where SND_EQUIPMENT_ID = '{recid}' and QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' and SERVICE_ID = '{treeparam}' ".format(ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"), recid=RECID, treeparam=TreeParentParam))
				if QueryCountObj is not None:
					QueryCount = QueryCountObj.cnt
			
			
			else:
				Trace.Write("5 level empty search --->")
				parent_obj = Sql.GetList("select top "+str(PerPage)+"  QUOTE_SERVICE_SENDING_FAB_EQUIP_ASS_ID,SND_EQUIPMENT_ID,SND_ASSEMBLY_ID,SND_ASSEMBLY_DESCRIPTION,GOT_CODE, SND_EQUIPMENT_DESCRIPTION,SNDFBL_ID,INCLUDED,GREENBOOK,EQUIPMENTTYPE_ID,EQUIPMENTCATEGORY_ID from SAQSSA (NOLOCK) where   QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' and SND_EQUIPMENT_ID = '{recid}' and SERVICE_ID = '{service_id}'and SNDFBL_ID = '{fablocation_id}' ORDER BY {ord_by} ".format( ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"),
						recid=RECID,
						service_id=TreeSuperParentParam,
						fablocation_id = TreeParentParam,
						ord_by = orderby
					)
				)
				
				QueryCountObj = Sql.GetFirst( "select count(*) as cnt from SAQSSA (NOLOCK) where   QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' and SNDFBL_ID = '{recid}' and SERVICE_ID = '{service_id}'and SNDFBL_ID = '{fablocation_id}'".format(
						RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"),
						ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),
						recid=RECID,
						service_id=TreeSuperParentParam,
						fablocation_id = TreeParentParam,
					))
				if QueryCountObj is not None:
					QueryCount = QueryCountObj.cnt
				
	else:
		Trace.Write("search with condition-")
		if TreeSuperParentParam == "Product Offerings":
			#Trace.Write('check-TreeSuperParentParam'+str(TreeSuperParentParam))
			parent_obj = Sql.GetList(
				"select top "+str(PerPage)+"  QUOTE_SERVICE_SENDING_FAB_EQUIP_ASS_ID,SND_EQUIPMENT_ID,SND_ASSEMBLY_ID,SND_ASSEMBLY_DESCRIPTION,GOT_CODE, SND_EQUIPMENT_DESCRIPTION,SNDFBL_ID,INCLUDED,GREENBOOK,EQUIPMENTTYPE_ID,EQUIPMENTCATEGORY_ID from SAQSSA (NOLOCK) where  "
				+ str(ATTRIBUTE_VALUE_STR)
				+ " 1=1 and QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' and SND_EQUIPMENT_ID = '{recid}' and SERVICE_ID = '{treeparam}' ORDER BY {ord_by} ".format(
					ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"), recid=RECID, treeparam=TreeParam,ord_by = orderby
				)
			)
			
			QueryCountObj = Sql.GetFirst( "select count(*) as cnt from SAQSSA (NOLOCK) where  "+ str(ATTRIBUTE_VALUE_STR) + " 1=1 and QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' and SND_EQUIPMENT_ID = '{recid}' and SERVICE_ID = '{treeparam}'".format(ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"),recid=RECID, treeparam=TreeParam
				))
			if QueryCountObj is not None:
				QueryCount = QueryCountObj.cnt
		else:
			if TreeTopSuperParentParam == "Product Offerings":
				parent_obj = Sql.GetList( "select top "+str(PerPage)+"  QUOTE_SERVICE_SENDING_FAB_EQUIP_ASS_ID,SND_EQUIPMENT_ID,SND_ASSEMBLY_ID,SND_ASSEMBLY_DESCRIPTION,GOT_CODE, SND_EQUIPMENT_DESCRIPTION,SNDFBL_ID,INCLUDED,GREENBOOK,EQUIPMENTTYPE_ID,EQUIPMENTCATEGORY_ID from SAQSSA (NOLOCK) where  " + str(ATTRIBUTE_VALUE_STR) + " 1=1 and QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' and SND_EQUIPMENT_ID = '{recid}' and SERVICE_ID = '{treeparam}' ORDER BY {ord_by}".format(ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"),recid=RECID,treeparam=TreeParentParam,ord_by = orderby))
				
				QueryCountObj = Sql.GetFirst("select count(*) as cnt from SAQSSA (NOLOCK) where  " + str(ATTRIBUTE_VALUE_STR) + " 1=1 and QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' and SND_EQUIPMENT_ID = '{recid}' and SERVICE_ID = '{treeparam}'".format(ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"),recid=RECID,treeparam=TreeParentParam, ))
				if QueryCountObj is not None:
					QueryCount = QueryCountObj.cnt
			else:   
				Trace.Write("5 level coditional search --->")
				parent_obj = Sql.GetList( "select top "+str(PerPage)+"  QUOTE_SERVICE_SENDING_FAB_EQUIP_ASS_ID,SND_EQUIPMENT_ID,SND_ASSEMBLY_ID,SND_ASSEMBLY_DESCRIPTION,GOT_CODE, SND_EQUIPMENT_DESCRIPTION,SNDFBL_ID,INCLUDED,GREENBOOK,EQUIPMENTTYPE_ID,EQUIPMENTCATEGORY_ID from SAQSSA (NOLOCK) where  "+ str(ATTRIBUTE_VALUE_STR)+ " 1=1 and QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}'  and SND_EQUIPMENT_ID = '{recid}' and SERVICE_ID = '{service_id}'and SNDFBL_ID = '{fablocation_id}' ORDER BY {ord_by}".format(ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"),recid=RECID,service_id=TreeSuperParentParam,fablocation_id = TreeParentParam,ord_by = orderby  ))   
				
				QueryCountObj = Sql.GetFirst("select count(*) as cnt from SAQSSA (NOLOCK) where  "+ str(ATTRIBUTE_VALUE_STR) + " 1=1 and QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' and SND_EQUIPMENT_ID = '{recid}' and SERVICE_ID = '{service_id}'and SNDFBL_ID = '{fablocation_id}'".format(ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"),recid=RECID,service_id=TreeSuperParentParam,fablocation_id = TreeParentParam,))
				if QueryCountObj is not None:
					QueryCount = QueryCountObj.cnt
				
				

	for par in parent_obj:
		data_dict = {}
		data_id = str(par.QUOTE_SERVICE_SENDING_FAB_EQUIP_ASS_ID)

		Action_str = (
			'<div class="btn-group dropdown"><div class="dropdown" id="ctr_drop"><i data-toggle="dropdown" id="dropdownMenuButton" class="fa fa-sort-desc dropdown-toggle" aria-expanded="false"></i><ul class="dropdown-menu left" aria-labelledby="dropdownMenuButton"><li><a class="dropdown-item cur_sty" href="#" id="'
			+ str(data_id)
			+ '" onclick="Commonteree_view_RL(this)">VIEW</a></li>'
		)
		if can_edit.upper() == "TRUE":
			Action_str += (
				'<li style="display:none" ><a class="dropdown-item cur_sty" href="#" id="'
				+ str(data_id)
				+ '" onclick="Move_to_parent_obj_edit(this)">EDIT</a></li>'
			)
		if can_delete.upper() == "TRUE":
			Action_str += '<li><a class="dropdown-item" data-target="#cont_viewModal_Material_Delete" data-toggle="modal" onclick="Material_delete_obj(this)" href="#">DELETE</a></li>'
		if can_clone.upper() == "TRUE":
			Action_str += '<li><a class="dropdown-item" data-target="#" data-toggle="modal" onclick="Material_clone_obj(this)" href="#">CLONE</a></li>'

		Action_str += "</ul></div></div>"
		data_dict = {}
		data_dict["ids"] = str(data_id)
		data_dict["ACTIONS"] = str(Action_str)
		data_dict["INCLUDED"] = str(par.INCLUDED)
		data_dict["QUOTE_SERVICE_SENDING_FAB_EQUIP_ASS_ID"] = CPQID.KeyCPQId.GetCPQId(
			"SAQSSA", str(par.QUOTE_SERVICE_SENDING_FAB_EQUIP_ASS_ID)
		)
		data_dict["SND_EQUIPMENT_ID"] = str(par.SND_EQUIPMENT_ID)
		data_dict["SND_ASSEMBLY_ID"] = ('<abbr id ="'+str(par.SND_ASSEMBLY_ID)+'" title="' + str(par.SND_ASSEMBLY_ID) + '">' + str(par.SND_ASSEMBLY_ID) + "</abbr>")
		data_dict["SND_ASSEMBLY_DESCRIPTION"] = str(par.SND_ASSEMBLY_DESCRIPTION)
		data_dict["SND_EQUIPMENT_DESCRIPTION"] = str(par.SND_EQUIPMENT_DESCRIPTION)
		data_dict["GOT_CODE"] = str(par.GOT_CODE)
		#data_dict["MNT_PLANT_ID"] = str(par.MNT_PLANT_ID)
		data_dict["SNDFBL_ID"] = str(par.SNDFBL_ID) 
		data_dict["GREENBOOK"] = str(par.GREENBOOK) 
		data_dict["EQUIPMENTTYPE_ID"] = str(par.EQUIPMENTTYPE_ID) 
		data_dict["EQUIPMENTCATEGORY_ID"] = str(par.EQUIPMENTCATEGORY_ID)        
		data_list.append(data_dict)
	
	
	page = ""
	if QueryCount < int(PerPage):
		page = str(Page_start) + " - " + str(QueryCount) + " of "
	else:
		page = str(Page_start) + " - " + str(Page_End)+ " of "
	#return data_list, QueryCount, page
	Trace.Write("GetCovObjChildFilter data_list --->"+str(data_list))
	# Trace.Write("GetCovObjChildFilter QueryCount ---->"+str(QueryCount))
	# Trace.Write("GetCovObjChildFilter page --->"+str(page))
	
	return data_list, QueryCount, page

def GetContractCovObjMaster(PerPage, PageInform, A_Keys, A_Values):
	if str(PerPage) == "" and str(PageInform) == "":
		Page_start = 1
		Page_End = 10
		PerPage = 10
		PageInform = "1___10___10"
	else:
		Page_start = int(PageInform.split("___")[0])
		Page_End = int(PageInform.split("___")[1])
		PerPage = PerPage
	ContractRecordId = Product.GetGlobal("contract_record_id")
	TreeParam = Product.GetGlobal("TreeParam")
	TreeParentParam = Product.GetGlobal("TreeParentLevel0")
	TreeSuperParentParam = Product.GetGlobal("TreeParentLevel1")
	TreeTopSuperParentParam = Product.GetGlobal("TreeParentLevel2")
	
	# FablocationId = Product.GetGlobal("TreeParam")
	data_list = []
	obj_idval = "SYOBJ_00267_SYOBJ_00267"
	rec_id = "SYOBJ_00267"
	obj_id = "SYOBJ_00267"
	obj_id = obj_id.replace("_","-")
	objh_getid = Sql.GetFirst(
		"SELECT TOP 1  RECORD_ID  FROM SYOBJH (NOLOCK) WHERE SAPCPQ_ATTRIBUTE_NAME='" + str(obj_id) + "'"
	)
	if objh_getid:
		obj_id = objh_getid.RECORD_ID
	objs_obj = Sql.GetFirst(
		"select CAN_ADD,CAN_EDIT,COLUMNS,CAN_DELETE from SYOBJR (NOLOCK) where OBJ_REC_ID = '" + str(obj_id) + "' "
	)
	can_edit = str(objs_obj.CAN_EDIT)
	can_add = str(objs_obj.CAN_ADD)
	can_delete = str(objs_obj.CAN_DELETE)
	table_id = "table_contract_covered_obj_parent"
	table_header = (
		'<table id="'
		+ str(table_id)
		+ '"  data-pagination="false" data-sortable="true" data-search-on-enter-key="true" data-filter-control="true" data-pagination-loop = "false" data-locale = "en-US" ><thead>'
	)
	Columns = [
		"CONTRACT_SERVICE_EQUIPMENT_RECORD_ID",
		"EQUIPMENT_ID",
		"EQUIPMENT_DESCRIPTION",
		"SERIAL_NUMBER",
		"GREENBOOK",
		"FABLOCATION_ID",
	]
	Objd_Obj = Sql.GetList(
		"select FIELD_LABEL,API_NAME,LOOKUP_OBJECT,LOOKUP_API_NAME,DATA_TYPE from SYOBJD (NOLOCK) where OBJECT_NAME = 'CTCSCO'"
	)
	attr_list = []
	attrs_datatype_dict = {}
	lookup_disply_list = []
	lookup_str = ""
	if Objd_Obj is not None:
		attr_list = {}
		for attr in Objd_Obj:
			attr_list[str(attr.API_NAME)] = str(attr.FIELD_LABEL)
			attrs_datatype_dict[str(attr.API_NAME)] = str(attr.DATA_TYPE)
			if attr.LOOKUP_API_NAME != "" and attr.LOOKUP_API_NAME is not None:
				lookup_disply_list.append(str(attr.API_NAME))
		checkbox_list = [inn.API_NAME for inn in Objd_Obj if inn.DATA_TYPE == "CHECKBOX"]
		lookup_list = {ins.LOOKUP_API_NAME: ins.API_NAME for ins in Objd_Obj}
	lookup_str = ",".join(list(lookup_disply_list))
	if TreeSuperParentParam == "Product Offerings" or TreeSuperParentParam == "Add-On Products" :        
		Qstr = (
			"select top "
			+ str(PerPage)
			+ " * from ( select ROW_NUMBER() OVER( ORDER BY CONTRACT_SERVICE_EQUIPMENT_RECORD_ID) AS ROW, CONTRACT_SERVICE_EQUIPMENT_RECORD_ID,EQUIPMENT_ID,EQUIPMENT_DESCRIPTION,SERIAL_NUMBER,GREENBOOK,FABLOCATION_ID from CTCSCO (NOLOCK) where CONTRACT_RECORD_ID = '"
			+ str(ContractRecordId)
			+ "' and SERVICE_ID = '"
			+ str(TreeParam)
			+ "') m where m.ROW BETWEEN "
			+ str(Page_start)
			+ " and "
			+ str(Page_End)
		)
	else:
		if TreeTopSuperParentParam == "Product Offerings":
			Qstr = (
				"select top "
				+ str(PerPage)
				+ " * from ( select ROW_NUMBER() OVER( ORDER BY CONTRACT_SERVICE_EQUIPMENT_RECORD_ID) AS ROW, CONTRACT_SERVICE_EQUIPMENT_RECORD_ID,EQUIPMENT_ID,EQUIPMENT_DESCRIPTION,SERIAL_NUMBER,GREENBOOK,FABLOCATION_ID from CTCSCO (NOLOCK) where CONTRACT_RECORD_ID = '"
				+ str(ContractRecordId)
				+ "' and SERVICE_ID = '"
				+ str(TreeParentParam)
				+ "' and GREENBOOK = '"
				+ str(TreeParam)
				+ "'"
				+ ") m where m.ROW BETWEEN "
				+ str(Page_start)
				+ " and "
				+ str(Page_End)
			)
	QueryCount = ""
	if TreeSuperParentParam == "Product Offerings":
		QueryCountObj = Sql.GetFirst(
			"select count(CONTRACT_SERVICE_EQUIPMENT_RECORD_ID) as cnt from CTCSCO (NOLOCK) where CONTRACT_RECORD_ID = '"
			+ str(ContractRecordId)
			+ "' and SERVICE_ID = '"
			+ str(TreeParam)
			+ "'"
		)
	else:
		if TreeTopSuperParentParam == "Product Offerings":            
			QueryCountObj = Sql.GetFirst(
				"select count(CONTRACT_SERVICE_EQUIPMENT_RECORD_ID) as cnt from CTCSCO (NOLOCK) where CONTRACT_RECORD_ID = '"
				+ str(ContractRecordId)
				+ "' and SERVICE_ID = '"
				+ str(TreeParentParam)
				+ "'and GREENBOOK = '"
				+ str(TreeParam)
				+ "'"
			)
	if QueryCountObj is not None:
		QueryCount = QueryCountObj.cnt
	parent_obj = Sql.GetList(Qstr)
	for par in parent_obj:
		data_id = str(par.CONTRACT_SERVICE_EQUIPMENT_RECORD_ID)
		Trace.Write("B6")

		Action_str = (
			'<div class="btn-group dropdown"><div class="dropdown" id="ctr_drop"><i data-toggle="dropdown" id="dropdownMenuButton" class="fa fa-sort-desc dropdown-toggle" aria-expanded="false"></i><ul class="dropdown-menu left" aria-labelledby="dropdownMenuButton"><li><a class="dropdown-item cur_sty" href="#" id="'
			+ str(data_id)
			+ '" onclick="Commonteree_view_RL(this)">VIEW</a></li>'
			+ '<li style="display:none"><a class="dropdown-item" id="deletebtn" data-target="#cont_CommonModalDelete" data-toggle="modal" onclick="CommonDelete(this, \'CTCSCO#'+ data_id +'\', \'WARNING\')" href="#">DELETE</a></li>'
		)
		"""if can_edit.upper() == "TRUE":
			Action_str += (
				'<li style="display:none" ><a class="dropdown-item cur_sty" href="#" id="'
				+ str(data_id)
				+ '" onclick="Move_to_parent_obj_edit(this)">EDIT</a></li>'
			)
		if can_delete.upper() == "TRUE":
			Action_str += '<li style="display:none"><a class="dropdown-item" data-target="#cont_viewModal_Material_Delete" data-toggle="modal" onclick="Material_delete_obj(this)" href="#">DELETE</a></li>'
		if can_add.upper() == "TRUE" and par.MARKET_TYPE == "NON MARKET BASED" and par.MODEL_TYPE != "COST PLUS":
			Action_str += (
				'<li><a class="dropdown-item" id="'
				+ str(data_id)
				+ '" data-target="#" data-toggle="modal" onclick="Pricebook_clone_obj(this)" href="#">CLONE</a></li>'
			)"""
		Action_str += "</ul></div></div>"

		# Data formation in dictonary format.
		## hyperlink
		data_dict = {}
		data_dict["ids"] = str(data_id)
		data_dict["ACTIONS"] = str(Action_str)
		data_dict["CONTRACT_SERVICE_EQUIPMENT_RECORD_ID"] = CPQID.KeyCPQId.GetCPQId(
			"CTCSCO", str(par.CONTRACT_SERVICE_EQUIPMENT_RECORD_ID)
		)
		data_dict["EQUIPMENT_ID"] = str(par.EQUIPMENT_ID)
		data_dict["EQUIPMENT_DESCRIPTION"] = str(par.EQUIPMENT_DESCRIPTION)
		data_dict["FABLOCATION_ID"] = str(par.FABLOCATION_ID)
		data_dict["GREENBOOK"] = str(par.GREENBOOK)
		data_dict["SERIAL_NUMBER"] = str(par.SERIAL_NUMBER)
		data_list.append(data_dict)

	hyper_link = ["CONTRACT_SERVICE_EQUIPMENT_RECORD_ID"]
	table_header += "<tr>"
	table_header += (
		'<th data-field="ACTIONS"><div class="action_col">ACTIONS</div><button class="searched_button" id="Act_'
		+ str(table_id)
		+ '">Search</button></th>'
	)
	table_header += '<th data-field="SELECT" class="wid45" data-checkbox="true"></th>'
	for key, invs in enumerate(list(Columns)):
		invs = str(invs).strip()
		qstring = attr_list.get(str(invs)) or ""
		if qstring == "":
			qstring = invs.replace("_", " ")
		if checkbox_list is not None and invs in checkbox_list:
			table_header += (
				'<th  data-field="'
				+ str(invs)
				+ '" data-filter-control="input" data-align="center" data-formatter="CheckboxFieldRelatedList" data-sortable="true"><abbr title="'
				+ str(qstring)
				+ '">'
				+ str(qstring)
				+ "</abbr></th>"
			)
		elif hyper_link is not None and invs in hyper_link:
			table_header += (
				'<th data-field="'
				+ str(invs)
				+ '" data-filter-control="input" data-formatter="ContractcovObjHyperLinkTreeLink" data-sortable="true"><abbr title="'
				+ str(qstring)
				+ '">'
				+ str(qstring)
				+ "</abbr></th>"
			)
		else:
			table_header += (
				'<th  data-field="'
				+ str(invs)
				+ '" data-filter-control="input" data-sortable="true"><abbr title="'
				+ str(qstring)
				+ '">'
				+ str(qstring)
				+ "</abbr></th>"
			)
	table_header += "</tr>"
	table_header += '</thead><tbody onclick="Table_Onclick_Scroll(this)"></tbody></table>'
	table_ids = "#" + str(table_id)
	filter_control_function = ""
	values_list = ""
	tbl_id = str(table_id)
	for key, invs in enumerate(list(Columns)):
		table_ids = "#" + str(table_id)
		filter_clas = "#" + str(table_id) + " .bootstrap-table-filter-control-" + str(invs)
		values_list += "var " + str(invs) + ' = $("' + str(filter_clas) + '").val(); '
		values_list += "ATTRIBUTE_VALUEList.push(" + str(invs) + "); "
		tbl_id = str(table_id)
	filter_class = "#Act_" + str(table_id)
	filter_control_function += (
		'$("'
		+ filter_class
		+ '").click( function(){ var table_id = $(this).closest("table").attr("id"); ATTRIBUTE_VALUEList = []; '
		+ str(values_list)
		+ ' var attribute_value = $(this).val(); cpq.server.executeScript("CQNESTGRID", {"TABNAME":"Contract Covered Object Parent", "ACTION":"PRODUCT_ONLOAD_FILTER", "ATTRIBUTE_NAME": '
		+ str(list(Columns))
		+ ', "ATTRIBUTE_VALUE": ATTRIBUTE_VALUEList }, function(dataset) { data2 = dataset[1];  data1 = dataset[0]; data3 = dataset[2]; console.log("len ---->"+data1.length);  try { if(data1.length > 0) { $("#' + str(tbl_id)  + '").bootstrapTable("load", data1 );$("#noRecDisp").remove(); if (document.getElementById("'+str(tbl_id) + '___totalItemCount")){document.getElementById("'+str(tbl_id)+ '___totalItemCount").innerHTML = data2;}  if (document.getElementById("'+str(tbl_id) + '___NumberofItem")) {document.getElementById("'+str(tbl_id)+ '___NumberofItem").innerHTML = data3;}} else{ $("#' + str(tbl_id) + '").bootstrapTable("load", data1  );$("#' + str(tbl_id) + '").after("<div id=\'noRecDisp\' class=\'noRecord\'>No Records to Display</div>"); $(".noRecord:not(:first)").remove(); if (document.getElementById("'+str(tbl_id) + '___totalItemCount")){document.getElementById("'+str(tbl_id)+ '___totalItemCount").innerHTML = data2;}  if (document.getElementById("'+str(tbl_id) + '___NumberofItem")) {document.getElementById("'+str(tbl_id)+ '___NumberofItem").innerHTML = data3;} }} catch(err){} }); filter_search_click();$(".JColResizer").mousedown(function(){ $("thead.fullHeadFirst").css("cssText","z-index: 2;border-top: 1px solid rgb(220, 220, 220);top: 154px;border-right: 0px !important;");$("thead.fullHeadSecond").css("display","none"); });$(".JColResizer").mouseup(function(){ var th_width_resize = [];$("#table_covered_obj_parent thead.fullHeadFirst tr th").each(function(index){var wid = $(this).css("width"); if(index ==0 || index ==1){th_width_resize.push("60px");}else{th_width_resize.push(wid);}}); $("thead.fullHeadFirst").css("cssText","position: fixed;z-index: 2;border-top: 1px solid rgb(220, 220, 220); top: 154px;border-right: 0px !important;");$("thead.fullHeadSecond").css("display","table-header-group");$("#table_covered_obj_parent thead.fullHeadFirst tr th").each(function(index){var num = th_width_resize[index].split("px");var numsp = parseInt(num[0]);numsp = numsp - 1;var make_str =numsp+"px"; var c = "width:"+make_str+";white-space: nowrap;overflow: hidden;text-overflow: ellipsis;";var d = "width:"+make_str+";"; $(this).css("cssText",c);$(this).children("div:first-child").css("cssText",c);$(this).children("div.fht-cell").css("cssText",d);});$("#table_covered_obj_parent thead.fullHeadSecond tr th").each(function(index){var num = th_width_resize[index].split("px");var numsp = parseInt(num[0]);numsp = numsp - 1;var make_str =numsp+"px"; var c = "width:"+make_str+";white-space: nowrap;overflow: hidden;text-overflow: ellipsis;";var d = "width:"+make_str+";"; $(this).css("cssText",c);$(this).children("div:first-child").css("cssText",c);$(this).children("div.fht-cell").css("cssText",d);}); });});'
	)
	dbl_clk_function = (
		'$("'
		+ str(table_ids)
		+ '").on("all.bs.table", function (e, name, args) { $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); }); $("'
		+ str(table_ids)
		+ '\ th.bs-checkbox div.th-inner").before("<div style=\'padding:0; border-bottom: 1px solid #dcdcdc;\'>SELECT</div>"); $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); $("'
		+ str(table_ids)
		+ "\").on('sort.bs.table', function (e, name, order) { console.log('sort.bs.table ============>111111111');  currenttab = $(\"ul#carttabs_head .active\").text().trim(); localStorage.setItem('"
		+ str(table_id)
		+ "_SortColumn', name); localStorage.setItem('"
		+ str(table_id)
		+ "_SortColumnOrder', order); NestedContainerSorting(name, order, '"
		+ str(table_id)
		+ "'); }); "
		)
	#Trace.Write("GetContractCovObjMaster dbl_clk_function --->"+str(dbl_clk_function))
	NORECORDS = ""
	if len(data_list) == 0:
		NORECORDS = "NORECORDS"

	ObjectName = "CTCSCO"
	DropDownList = []
	filter_level_list = []
	filter_clas_name = ""
	cv_list = []
	TableclassName = "form-control" + table_id
	for key, col_name in enumerate(list(Columns)):
		StringValue_list = []
		objss_obj = Sql.GetFirst(
			"SELECT API_NAME, DATA_TYPE, FORMULA_LOGIC, PICKLIST FROM SYOBJD (NOLOCK) WHERE OBJECT_NAME='"
			+ str(ObjectName)
			+ "' and API_NAME = '"
			+ str(col_name)
			+ "'"
		)
		try:
			FORMULA_LOGIC = objss_obj.FORMULA_LOGIC.strip()
			FORMULA_col = FORMULA_LOGIC.split(" ")[1].strip()
			FORMULA_table = FORMULA_LOGIC.split(" ")[3].strip()
			ins_obj = Sql.GetFirst(
				"SELECT API_NAME, DATA_TYPE,PICKLIST FROM SYOBJD (NOLOCK) WHERE OBJECT_NAME='"
				+ str(FORMULA_table)
				+ "' and API_NAME = '"
				+ str(FORMULA_col)
				+ "'"
			)
			if str(objss_obj.PICKLIST).upper() == "TRUE":
				filter_level_data = "select"
				filter_clas_name = (
					'<div id = "'
					+ str(table_id)
					+ "_RelatedMutipleCheckBoxDrop_"
					+ str(key)
					+ '" class="form-control bootstrap-table-filter-control-'
					+ str(col_name)
					+ " RelatedMutipleCheckBoxDrop_"
					+ str(key)
					+ ' "></div>'
				)
				filter_level_list.append(filter_level_data)
			else:
				filter_level_data = "input"
				filter_clas_name = (
					'<input type="text" class="width100_vis form-control bootstrap-table-filter-control-'
					+ str(col_name)
					+ '">'
				)
				filter_level_list.append(filter_level_data)
		except:
			"""if str(objss_obj.PICKLIST).upper() == "TRUE":
				filter_level_data = "select"
				filter_clas_name = (
					'<div id = "'
					+ str(table_id)
					+ "_RelatedMutipleCheckBoxDrop_"
					+ str(key)
					+ '" class="form-control bootstrap-table-filter-control-'
					+ str(col_name)
					+ " RelatedMutipleCheckBoxDrop_"
					+ str(key)
					+ ' "></div>'
				)
				filter_level_list.append(filter_level_data)"""

			filter_level_data = "input"
			filter_clas_name = (
				'<input type="text" class="width100_vis form-control bootstrap-table-filter-control-' + str(col_name) + '">'
			)
			filter_level_list.append(filter_level_data)
		cv_list.append(filter_clas_name)
		if filter_level_data == "select":
			try:
				xcd = Sql.GetFirst(
					"SELECT (STUFF((SELECT DISTINCT ', ' + CAST("
					+ str(col_name)
					+ " AS CHAR(100)) FROM "
					+ str(ObjectName)
					+ " (NOLOCK) FOR XML PATH('') ), 1, 2, '')  ) AS StringValue"
				)
			except:
				xcd = Sql.GetFirst(
					"SELECT (STUFF((SELECT DISTINCT ', ' + CAST("
					+ str(col_name)
					+ " AS CHAR(100)) FROM "
					+ str(ObjectName)
					+ " (NOLOCK) FOR XML PATH('') ), 1, 2, '')  ) AS StringValue"
				)
			if str(xcd.StringValue) is not None and str(xcd.StringValue) != "":
				if str(xcd.StringValue).find(",") != -1:
					StringValue_list = [ins.strip() for ins in str(xcd.StringValue).split(",") if ins.strip() != ""]
				else:
					StringValue_list.append(str(xcd.StringValue))
			else:
				StringValue_list = [""]
			StringValue_list = list(set(StringValue_list))
			DropDownList.append(StringValue_list)
		elif filter_level_data == "checkbox":
			DropDownList.append(["True", "False"])
		else:
			DropDownList.append("")
	RelatedDrop_str = (
		"try { if( document.getElementById('"
		+ str(table_id)
		+ "') ) { var listws = document.getElementById('"
		+ str(table_id)
		+ "').getElementsByClassName('filter-control');  for (i = 0; i < listws.length; i++) { document.getElementById('"
		+ str(table_id)
		+ "').getElementsByClassName('filter-control')[i].innerHTML = data6[i];  } for (j = 0; j < listws.length; j++) { if (data7[j] == 'select') { if (data8[j]) { var dataAdapter = new $.jqx.dataAdapter(data8[j]); $('#"
		+ str(table_id)
		+ "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter, autoDropDownHeight: true }); } } } } }  catch(err) { setTimeout(function() { var listws = document.getElementById('"
		+ str(table_id)
		+ "').getElementsByClassName('filter-control');  for (i = 0; i < listws.length; i++) { document.getElementById('"
		+ str(table_id)
		+ "').getElementsByClassName('filter-control')[i].innerHTML = data6[i];  } for (j = 0; j < listws.length; j++) { if (data7[j] == 'select') { if (data8[j]) { var dataAdapter = new $.jqx.dataAdapter(data8[j]); $('#"
		+ str(table_id)
		+ "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter, autoDropDownHeight: true }); } } } }, 5000); }"
	)
	"""page = ""
	if QueryCount < int(PerPage):
		page = str(Page_start) + " - " + str(QueryCount)
	else:
		page = str(Page_start) + " - " + str(Page_End)"""

	if int(QueryCount) < int(PerPage):
		Action_Str = str(Page_start) + " - " + str(QueryCount)+ " of"
	elif QueryCount == PerPage:
		Action_Str = str(Page_start) + " - " + str(PerPage)+ " of"
	else:
		Action_Str = str(Page_start) + " - " + str(Page_End)+ " of"

	Test = (
		'<div class="col-md-12 brdr listContStyle pad2height30" ><div class="col-md-4 pager-numberofitem clear-padding"><span class="pager-number-of-items-item noofitem" id="'
		+ str(table_id)
		+ '___NumberofItem" >'
		+ str(Action_Str)
		+ '</span><span class="pager-number-of-items-item fltltpad2mrg0" id="'
		+ str(table_id)
		+ '___totalItemCount" >'
		+ str(QueryCount)
		+ '</span><div class="clear-padding fltltmrgtp3" ><div  class="pull-right vertmidtxtrht"><select onchange="PageFunctestChild(this,\'Contract\',\'\',\'table_contract_covered_obj_parent\')" id="'
		+ str(table_id)
		+ '___PageCountValue" class="form-control wid65vermiddisinbmarl5"><option value="10" selected>10</option><option value="20">20</option><option value="50">50</option><option value="100">100</option><option value="200">200</option></select> </div></div></div><div class="col-xs-8 col-md-4  clear-padding disinpad10txtcen"  data-bind="visible: totalItemCount"><div class="clear-padding col-xs-12 col-sm-6 col-md-12 bor0" ><ul class="pagination pagination"><li class="disabled"><a href="#" onclick="FirstPageLoad_paginationChild(\'Contract\',\'\',\''
		+str(table_id)
		+'\')"><i class="fa fa-caret-left font14whtbld" ></i><i class="fa fa-caret-left font14" ></i></a></li><li class="disabled"><a href="#" onclick="Previous12334Child(\'Contract\',\'\',\''
		+str(table_id)
		+'\')"><i class="fa fa-caret-left font14" ></i>PREVIOUS</a></li><li class="disabled"><a href="#" class="disabledPage" onclick="Next12334Child(\'Contract\',\'\',\''
		+str(table_id)
		+'\')">NEXT<i class="fa fa-caret-right font14" ></i></a></li><li class="disabled"><a href="#" onclick="LastPageLoad_paginationChild(\'Contract\',\'\',\''
		+str(table_id)
		+'\')" class="disabledPage"><i class="fa fa-caret-right font14"></i><i class="fa fa-caret-right font14whtbld"></i></a></li></ul></div> </div> <div class="col-md-4 pr_page_pad"> <span id="'
		+ str(table_id)
		+ '___page_count" class="currentPage page_right_content">1</span><span class="page_right_content pad_rt_2">Page </span></div></div>'
	)

	if QueryCount < int(PerPage):
		PerPage = str(QueryCount)
	else:
		PerPage = str(PerPage)   
	if Page_End > QueryCount:
		Page_End = QueryCount
	else:
		Page_End = Page_End
	
	Action_Str = ""
	Action_Str += str(Page_start)+" - "
	Action_Str += str(Page_End)
	Action_Str += " of"

	return (
		table_header,
		data_list,
		table_id,
		filter_control_function,
		NORECORDS,
		dbl_clk_function,
		cv_list,
		filter_level_list,
		DropDownList,
		RelatedDrop_str,
		Test,
		Action_Str,
	)

def GetCovObjChild(recid, PerPage, PageInform, A_Keys, A_Values):
	TreeParam = Product.GetGlobal("TreeParam")
	TreeParentParam = Product.GetGlobal("TreeParentLevel0")
	TreeSuperParentParam = Product.GetGlobal("TreeParentLevel1")
	TreeTopSuperParentParam = Product.GetGlobal("TreeParentLevel2")
	
	if str(PerPage) == "" and str(PageInform) == "":
		Page_start = 1
		Page_End = 10
		PerPage = 10
		PageInform = "1___10___10"
	else:
		Page_start = int(PageInform.split("___")[0])
		Page_End = int(PageInform.split("___")[1])
		PerPage = PerPage
	chld_list = []
	Parent_Equipmentid = ""
	ContractRecordId = Quote.GetGlobal("contract_quote_record_id")
	RevisionRecordId = Quote.GetGlobal("quote_revision_record_id")
	obj_idval = "SYOBJ_00929_SYOBJ_00929"
	obj_id1 = "SYOBJ-00929"
	objh_getid = Sql.GetFirst(
		"SELECT TOP 1  RECORD_ID  FROM SYOBJH (NOLOCK) WHERE SAPCPQ_ATTRIBUTE_NAME='" + str(obj_id1) + "'"
	)
	if objh_getid:
		obj_id1 = objh_getid.RECORD_ID
	objs_obj1 = Sql.GetFirst(
		"select CAN_ADD,CAN_EDIT,COLUMNS,CAN_DELETE from SYOBJR (NOLOCK) where OBJ_REC_ID = '" + str(obj_id1) + "' "
	)
	can_edit1 = str(objs_obj1.CAN_EDIT)
	can_add1 = str(objs_obj1.CAN_ADD)
	can_delete1 = str(objs_obj1.CAN_DELETE)
	table_id = "covered_obj_child_" +str(recid)
	table_header = (
		'<table id="'
		+ str(table_id)
		+ '" data-pagination="false" data-sortable="true" data-search-on-enter-key="true" data-filter-control="true" data-pagination-loop = "false" data-locale = "en-US" ><thead>'
	)
	Columns = ["INCLUDED","QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID","ASSEMBLY_ID", "ASSEMBLY_DESCRIPTION", "EQUIPMENT_DESCRIPTION","EQUIPMENTTYPE_ID", "GOT_CODE","MNT_PLANT_ID","FABLOCATION_ID","WARRANTY_START_DATE","WARRANTY_END_DATE"]
	Objd_Obj = Sql.GetList(
		"select FIELD_LABEL,API_NAME,LOOKUP_OBJECT,LOOKUP_API_NAME,DATA_TYPE from SYOBJD (NOLOCK) where OBJECT_NAME = 'SAQSCA'"
	)
	attr_list = []
	attrs_datatype_dict = {}
	lookup_disply_list = []
	lookup_str = ""
	if Objd_Obj is not None:
		attr_list = {}
		for attr in Objd_Obj:
			attr_list[str(attr.API_NAME)] = str(attr.FIELD_LABEL)
			attrs_datatype_dict[str(attr.API_NAME)] = str(attr.DATA_TYPE)
			if attr.LOOKUP_API_NAME != "" and attr.LOOKUP_API_NAME is not None:
				lookup_disply_list.append(str(attr.API_NAME))
		checkbox_list = [inn.API_NAME for inn in Objd_Obj if inn.DATA_TYPE == "CHECKBOX"]
		lookup_list = {ins.LOOKUP_API_NAME: ins.API_NAME for ins in Objd_Obj}
	lookup_str = ",".join(list(lookup_disply_list))
	Parent_Equipmentid = recid
	if Parent_Equipmentid:
		# child_obj_recid = Sql.GetList("select  top 5 EQUIPMENT_ID from SAQFEA (NOLOCK) where EQUIPMENT_ID = '{EquipmentID}' and QUOTE_RECORD_ID = '{ContractRecordId}' and FABLOCATION_ID = '{FablocationId}'".format(EquipmentID = Parent_Equipmentid.EQUIPMENT_ID,ContractRecordId = Quote.GetGlobal("contract_quote_record_id"),FablocationId = Product.GetGlobal("TreeParam")))
		if TreeTopSuperParentParam == "Product Offerings" or TreeSuperParentParam == "Comprehensive Services":
			child_obj_recid = Sql.GetList(
				"select top "+str(PerPage)+" * from (select ROW_NUMBER() OVER( ORDER BY QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID) AS ROW, QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID,EQUIPMENT_ID,ASSEMBLY_ID,ASSEMBLY_DESCRIPTION,EQUIPMENTTYPE_ID,GOT_CODE,EQUIPMENT_DESCRIPTION,MNT_PLANT_ID,FABLOCATION_ID,WARRANTY_START_DATE,WARRANTY_END_DATE,INCLUDED from SAQSCA (NOLOCK) where EQUIPMENT_ID = '{Parent_Equipmentid}' and QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' and SERVICE_ID = '{Service_Id}') m where m.ROW BETWEEN ".format(
					ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),
					RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"),
					Parent_Equipmentid=Parent_Equipmentid,
					Service_Id=TreeParentParam,
				)
				+ str(Page_start)
				+ " and "
				+ str(Page_End)
			)

			QueryCountObj = Sql.GetFirst(
				"select count(CpqTableEntryId) as cnt from SAQSCA (NOLOCK) where QUOTE_RECORD_ID = '"
				+ str(ContractRecordId)
				+ "' and QTEREV_RECORD_ID = '"
				+ str(RevisionRecordId)
				+ "'and EQUIPMENT_ID ='"
				+ str(Parent_Equipmentid)
				+ "'and SERVICE_ID ='{Service_Id}'".format(Service_Id=TreeParentParam)
			)
		elif TreeSuperParentParam == "Add-On Products":
			child_obj_recid = Sql.GetList(
				"select top "+str(PerPage)+" * from (select ROW_NUMBER() OVER( ORDER BY QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID) AS ROW, QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID,EQUIPMENT_ID,ASSEMBLY_ID,ASSEMBLY_DESCRIPTION,EQUIPMENTTYPE_ID,GOT_CODE,EQUIPMENT_DESCRIPTION,MNT_PLANT_ID,FABLOCATION_ID,WARRANTY_START_DATE,WARRANTY_END_DATE,INCLUDED from SAQSCA (NOLOCK) where EQUIPMENT_ID = '{Parent_Equipmentid}' and QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' and SERVICE_ID = '{treeparentparam}') m where m.ROW BETWEEN ".format(
					ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),
					RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"),
					Parent_Equipmentid=Parent_Equipmentid,
					treeparentparam=TreeParentParam,
				)
				+ str(Page_start)
				+ " and "
				+ str(Page_End)
			)

			QueryCountObj = Sql.GetFirst(
				"select count(CpqTableEntryId) as cnt from SAQSCA (NOLOCK) where QUOTE_RECORD_ID = '"
				+ str(ContractRecordId)
				+ "' and QTEREV_RECORD_ID = '"
				+ str(RevisionRecordId)
				+ "'and EQUIPMENT_ID ='"
				+ str(Parent_Equipmentid)
				+ "'and SERVICE_ID ='"
				+ str(TreeParentParam)
				+ "'"
			)
		elif (TreeParam.startswith("Sending") or TreeParam.startswith("Receiving")):
			child_obj_recid = Sql.GetList(
				"select top "+str(PerPage)+" * from (select ROW_NUMBER() OVER( ORDER BY QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID) AS ROW, QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID,EQUIPMENT_ID,ASSEMBLY_ID,ASSEMBLY_DESCRIPTION,EQUIPMENTTYPE_ID,GOT_CODE,EQUIPMENT_DESCRIPTION,MNT_PLANT_ID,FABLOCATION_ID,WARRANTY_START_DATE,WARRANTY_END_DATE,INCLUDED from SAQSCA (NOLOCK) where EQUIPMENT_ID = '{Parent_Equipmentid}' and QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' and SERVICE_ID = '{treeparentparam}') m where m.ROW BETWEEN ".format(
					ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),
					Parent_Equipmentid=Parent_Equipmentid,
					treeparentparam=TreeParentParam,
					RevisionRecordId=Quote.GetGlobal("quote_revision_record_id"),
				)
				+ str(Page_start)
				+ " and "
				+ str(Page_End)
			)

			QueryCountObj = Sql.GetFirst(
				"select count(CpqTableEntryId) as cnt from SAQSCA (NOLOCK) where QUOTE_RECORD_ID = '"
				+ str(ContractRecordId)
				+ "' and QTEREV_RECORD_ID = '"
				+ str(RevisionRecordId)
				+ "'and EQUIPMENT_ID ='"
				+ str(Parent_Equipmentid)
				+ "'and SERVICE_ID ='"
				+ str(TreeParentParam)
				+ "'"
			)
		elif TreeTopSuperParentParam == "Product Offerings":
			child_obj_recid = Sql.GetList(
				"select top "+str(PerPage)+" * from (select ROW_NUMBER() OVER( ORDER BY QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID) AS ROW, QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID,EQUIPMENT_ID,ASSEMBLY_ID,ASSEMBLY_DESCRIPTION,EQUIPMENTTYPE_ID,GOT_CODE,EQUIPMENT_DESCRIPTION,MNT_PLANT_ID,FABLOCATION_ID,WARRANTY_START_DATE,WARRANTY_END_DATE,INCLUDED from SAQSCA (NOLOCK) where EQUIPMENT_ID = '{Parent_Equipmentid}' and QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' and SERVICE_ID = '{treeparam}' AND FABLOCATION_ID = '{fab}') m where m.ROW BETWEEN ".format(
					ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),
					RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"),
					Parent_Equipmentid=Parent_Equipmentid,
					treeparam=TreeParentParam,
					fab=TreeParam
				)
				+ str(Page_start)
				+ " and "
				+ str(Page_End)
			)

			QueryCountObj = Sql.GetFirst(
				"select count(CpqTableEntryId) as cnt from SAQSCA (NOLOCK) where QUOTE_RECORD_ID = '"
				+ str(ContractRecordId)
				+ "' and QTEREV_RECORD_ID = '"
				+ str(RevisionRecordId)
				+ "' and EQUIPMENT_ID ='"
				+ str(Parent_Equipmentid)
				+ "'and SERVICE_ID ='"
				+ str(TreeParentParam)
				+ "' AND FABLOCATION_ID = '"
				+ str(TreeParam)
				+ "'"
			)
		elif TreeSuperParentParam == "Product Offerings":
			child_obj_recid = Sql.GetList(
				"select top "+str(PerPage)+" * from (select ROW_NUMBER() OVER( ORDER BY QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID) AS ROW, QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID,EQUIPMENT_ID,ASSEMBLY_ID,ASSEMBLY_DESCRIPTION,EQUIPMENTTYPE_ID,GOT_CODE,EQUIPMENT_DESCRIPTION,MNT_PLANT_ID,FABLOCATION_ID,WARRANTY_START_DATE,WARRANTY_END_DATE,INCLUDED from SAQSCA (NOLOCK) where EQUIPMENT_ID = '{Parent_Equipmentid}' and QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' and SERVICE_ID = '{treeparam}') m where m.ROW BETWEEN ".format(
					ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),
					RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"),
					Parent_Equipmentid=Parent_Equipmentid,
					treeparam=TreeParam
				)
				+ str(Page_start)
				+ " and "
				+ str(Page_End)
			)

			QueryCountObj = Sql.GetFirst(
				"select count(CpqTableEntryId) as cnt from SAQSCA (NOLOCK) where QUOTE_RECORD_ID = '"
				+ str(ContractRecordId)
				+ "' and QTEREV_RECORD_ID = '"
				+ str(RevisionRecordId)
				+ "' and EQUIPMENT_ID ='"
				+ str(Parent_Equipmentid)
				+ "'and SERVICE_ID ='"
				+ str(TreeParam)
				+ "'"
			)
		elif TreeTopSuperParentParam == "Add-On Products":
			child_obj_recid = Sql.GetList(
				"select top "+str(PerPage)+" * from (select ROW_NUMBER() OVER( ORDER BY QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID) AS ROW, QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID,EQUIPMENT_ID,ASSEMBLY_ID,ASSEMBLY_DESCRIPTION,EQUIPMENTTYPE_ID,GOT_CODE,EQUIPMENT_DESCRIPTION,MNT_PLANT_ID,FABLOCATION_ID,WARRANTY_START_DATE,WARRANTY_END_DATE,INCLUDED from SAQSCA (NOLOCK) where EQUIPMENT_ID = '{Parent_Equipmentid}' and QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' and SERVICE_ID = '{treesuperparent}' AND FABLOCATION_ID = '{fab}') m where m.ROW BETWEEN ".format(
					ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),
					RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"),
					Parent_Equipmentid=Parent_Equipmentid,
					treesuperparent=TreeSuperParentParam,
					fab=TreeParentParam
				)
				+ str(Page_start)
				+ " and "
				+ str(Page_End)
			)

			QueryCountObj = Sql.GetFirst(
				"select count(CpqTableEntryId) as cnt from SAQSCA (NOLOCK) where QUOTE_RECORD_ID = '"
				+ str(ContractRecordId)
				+ "' and QTEREV_RECORD_ID = '"
				+ str(RevisionRecordId)
				+ "' and EQUIPMENT_ID ='"
				+ str(Parent_Equipmentid)
				+ "'and SERVICE_ID ='"
				+ str(TreeSuperParentParam)
				+ "' AND FABLOCATION_ID = '"
				+ str(TreeParentParam)
				+ "'"
			)
		elif (TreeTopSuperParentParam == "Comprehensive Services" or TreeTopSuperParentParam == "Complementary Products") and TreeParentParam != "Receiving Equipment":
			child_obj_recid = Sql.GetList(
				"select top "+str(PerPage)+" * from (select ROW_NUMBER() OVER( ORDER BY QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID) AS ROW, QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID,EQUIPMENT_ID,ASSEMBLY_ID,ASSEMBLY_DESCRIPTION,EQUIPMENTTYPE_ID,GOT_CODE,EQUIPMENT_DESCRIPTION,MNT_PLANT_ID,FABLOCATION_ID,WARRANTY_START_DATE,WARRANTY_END_DATE,INCLUDED from SAQSCA (NOLOCK) where EQUIPMENT_ID = '{Parent_Equipmentid}' and QUOTE_RECORD_ID = '{ContractRecordId}'  and QTEREV_RECORD_ID = '{RevisionRecordId}' and SERVICE_ID = '{treeparam}' AND FABLOCATION_ID = '{fab}') m where m.ROW BETWEEN ".format(
					ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),
					RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"),
					Parent_Equipmentid=Parent_Equipmentid,
					treeparam=TreeSuperParentParam,
					fab=TreeParentParam
				)
				+ str(Page_start)
				+ " and "
				+ str(Page_End)
			)

			QueryCountObj = Sql.GetFirst(
				"select count(CpqTableEntryId) as cnt from SAQSCA (NOLOCK) where QUOTE_RECORD_ID = '"
				+ str(ContractRecordId)
				+ "' and QTEREV_RECORD_ID = '"
				+ str(RevisionRecordId)
				+ "'and EQUIPMENT_ID ='"
				+ str(Parent_Equipmentid)
				+ "'and SERVICE_ID ='"
				+ str(TreeSuperParentParam)
				+ "' AND FABLOCATION_ID = '"
				+ str(TreeParentParam)
				+ "'"
			)
		elif TreeParentParam == "Receiving Equipment":
			child_obj_recid = Sql.GetList(
				"select top "+str(PerPage)+" * from (select ROW_NUMBER() OVER( ORDER BY QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID) AS ROW, QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID,EQUIPMENT_ID,ASSEMBLY_ID,ASSEMBLY_DESCRIPTION,EQUIPMENTTYPE_ID,GOT_CODE,EQUIPMENT_DESCRIPTION,MNT_PLANT_ID,FABLOCATION_ID,WARRANTY_START_DATE,WARRANTY_END_DATE,INCLUDED from SAQSCA (NOLOCK) where EQUIPMENT_ID = '{Parent_Equipmentid}' and QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' and SERVICE_ID = '{treeparam}' AND FABLOCATION_ID = '{fab}') m where m.ROW BETWEEN ".format(
					ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),
					RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"),
					Parent_Equipmentid=Parent_Equipmentid,
					treeparam=TreeSuperParentParam,
					fab=TreeParam
				)
				+ str(Page_start)
				+ " and "
				+ str(Page_End)
			)

			QueryCountObj = Sql.GetFirst(
				"select count(CpqTableEntryId) as cnt from SAQSCA (NOLOCK) where QUOTE_RECORD_ID = '"
				+ str(ContractRecordId)
				+ "' and QTEREV_RECORD_ID = '"
				+ str(RevisionRecordId)
				+ "' and EQUIPMENT_ID ='"
				+ str(Parent_Equipmentid)
				+ "'and SERVICE_ID ='"
				+ str(TreeSuperParentParam)
				+ "' AND FABLOCATION_ID = '"
				+ str(TreeParam)
				+ "'"
			) 
		elif TreeSuperParentParam == "Receiving Equipment":
			child_obj_recid = Sql.GetList(
				"select top "+str(PerPage)+" * from (select ROW_NUMBER() OVER( ORDER BY QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID) AS ROW, QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID,EQUIPMENT_ID,ASSEMBLY_ID,ASSEMBLY_DESCRIPTION,EQUIPMENTTYPE_ID,GOT_CODE,EQUIPMENT_DESCRIPTION,MNT_PLANT_ID,FABLOCATION_ID,WARRANTY_START_DATE,WARRANTY_END_DATE,INCLUDED from SAQSCA (NOLOCK) where EQUIPMENT_ID = '{Parent_Equipmentid}' and QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' and SERVICE_ID = '{treeparam}' AND FABLOCATION_ID = '{fab}') m where m.ROW BETWEEN ".format(
					ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),
					RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"),
					Parent_Equipmentid=Parent_Equipmentid,
					treeparam=TreeTopSuperParentParam,
					fab=TreeParentParam
				)
				+ str(Page_start)
				+ " and "
				+ str(Page_End)
			)

			QueryCountObj = Sql.GetFirst(
				"select count(CpqTableEntryId) as cnt from SAQSCA (NOLOCK) where QUOTE_RECORD_ID = '"
				+ str(ContractRecordId)
				+ "' and QTEREV_RECORD_ID = '"
				+ str(RevisionRecordId)
				+ "' and EQUIPMENT_ID ='"
				+ str(Parent_Equipmentid)
				+ "'and SERVICE_ID ='"
				+ str(TreeTopSuperParentParam)
				+ "' AND FABLOCATION_ID = '"
				+ str(TreeParentParam)
				+ "'"
			)        
		if QueryCountObj is not None:
			QueryCount = QueryCountObj.cnt
		# Data construction for table.
		for child in child_obj_recid:
			
			data_id = str(child.QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID) + "|SAQSCA"
			chld_dict = {}
			Action_str1 = (
				'<div class="btn-group dropdown"><div class="dropdown" id="ctr_drop"><i data-toggle="dropdown" id="dropdownMenuButton" class="fa fa-sort-desc dropdown-toggle" aria-expanded="false"></i><ul class="dropdown-menu left" aria-labelledby="dropdownMenuButton"><li><a id="'
				+ str(data_id)
				+ '" class="dropdown-item cur_sty" href="#"  onclick="Commonteree_view_RL(this) ">VIEW</a></li>'
			)
			if can_edit1.upper() == "TRUE":
				Action_str1 += (
					'<li style="display:none" ><a data-toggle="modal" data-target="#cont_viewModalSection" id="'
					+ str(data_id)
					+ '"  class="dropdown-item cur_sty" href="#"  onclick="cont_relatedlist_openedit(this)">EDIT</a></li>'
				)
			if can_delete1.upper() == "TRUE":
				Action_str1 += '<li><a class="dropdown-item" data-target="#cont_viewModal_Material_Delete" data-toggle="modal" onclick="Material_delete_obj(this)" href="#">DELETE</a></li>'
			if can_add1.upper() == "TRUE":
				Action_str1 += '<li><a class="dropdown-item" data-target="#" data-toggle="modal" onclick="Material_clone_obj(this)" href="#">CLONE</a></li>'
			Action_str1 += "</ul></div></div>"
			data_dict = {}
			chld_dict["ids"] = str(data_id)
			# data formation in Dictonary format.

			chld_dict["ACTIONS"] = str(Action_str1)
			chld_dict["INCLUDED"] = str(child.INCLUDED)
			chld_dict["QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID"] = CPQID.KeyCPQId.GetCPQId("SAQSCA", str(child.QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID))
			chld_dict["EQUIPMENT_ID"] = ('<abbr id ="" title="' + str(child.EQUIPMENT_ID) + '">' + str(child.EQUIPMENT_ID) + "</abbr>") 
			chld_dict["ASSEMBLY_ID"] = ('<abbr id ="" title="' + str(child.ASSEMBLY_ID) + '">' + str(child.ASSEMBLY_ID) + "</abbr>")
			chld_dict["ASSEMBLY_DESCRIPTION"] = ('<abbr id ="" title="' + str(child.ASSEMBLY_DESCRIPTION) + '">' + str(child.ASSEMBLY_DESCRIPTION) + "</abbr>")
			chld_dict["EQUIPMENT_DESCRIPTION"] = ('<abbr id ="" title="' + str(child.EQUIPMENT_DESCRIPTION) + '">' + str(child.EQUIPMENT_DESCRIPTION) + "</abbr>")
			
			chld_dict["EQUIPMENTTYPE_ID"] = ('<abbr id ="" title="' + str(child.EQUIPMENTTYPE_ID) + '">' + str(child.EQUIPMENTTYPE_ID) + "</abbr>")
			chld_dict["GOT_CODE"] = ('<abbr id ="" title="' + str(child.GOT_CODE) + '">' + str(child.GOT_CODE) + "</abbr>")
			chld_dict["MNT_PLANT_ID"] = ('<abbr id ="" title="' + str(child.MNT_PLANT_ID) + '">' + str(child.MNT_PLANT_ID) + "</abbr>")
			chld_dict["FABLOCATION_ID"] = ('<abbr id ="" title="' + str(child.FABLOCATION_ID) + '">' + str(child.FABLOCATION_ID) + "</abbr>")
			chld_dict["WARRANTY_START_DATE"] = ('<abbr id ="" title="' + str(child.WARRANTY_START_DATE) + '">' + str(child.WARRANTY_START_DATE)+ "</abbr>")
			chld_dict["WARRANTY_END_DATE"] = ('<abbr id ="" title="' + str(child.WARRANTY_END_DATE) + '">' + str(child.WARRANTY_END_DATE) + "</abbr>")
			# chld_dict["MODULE_ID"] = str(child.MODULE_ID)
			# chld_dict["MODULE_NAME"] = str(child.MODULE_NAME)
			chld_list.append(chld_dict)

	# Table formation.
	#hyper_link = ["ASSEMBLY_ID"]
	"""if TreeParentParam == "Comprehensive Services": 
		quote_entitlement_obj = Sql.GetFirst("SELECT CpqTableEntryId FROM SAQTSE WHERE ENTITLEMENT_DESCRIPTION = 'TKM Ops Support' AND ENTITLEMENT_DISPLAY_VALUE = 'Yes' AND SERVICE_ID = '{TreeParam}' AND QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' ".format(TreeParam = Product.GetGlobal("TreeParam"),ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id")))
	else:
		if TreeSuperParentParam == "Comprehensive Services":
			quote_entitlement_obj = Sql.GetFirst("SELECT CpqTableEntryId FROM SAQTSE WHERE ENTITLEMENT_DESCRIPTION = 'TKM Ops Support' AND ENTITLEMENT_DISPLAY_VALUE = 'Yes' AND SERVICE_ID = '{TreeParentParam}' AND QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}'  ".format(TreeParentParam = Product.GetGlobal("TreeParentLevel0"),ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id")))
	if quote_entitlement_obj is not None:
		hyper_link = ["ASSEMBLY_ID"]
	else:
		hyper_link = []"""
	hyper_link = ["QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID"]   
	table_header += "<tr>"
	table_header += (
		'<th data-field="ACTIONS"><div class="action_col">ACTIONS</div><button class="searched_button" id="Act_'
		+ str(table_id)
		+ '">Search</button></th>'
	)
	table_header += '<th data-field="SELECT" class="wid45" data-checkbox="true"></th>'
	for key, invs in enumerate(list(Columns)):
		invs = str(invs).strip()
		qstring = attr_list.get(str(invs)) or ""
		if qstring == "":
			qstring = invs.replace("_", " ")
		if checkbox_list is not None and invs in checkbox_list:
			table_header += (
				'<th data-field="'
				+ str(invs)
				+ '" data-filter-control="input" data-align="center" data-formatter="CheckboxFieldRelatedList" data-sortable="true"><abbr title="'
				+ str(qstring)
				+ '">'
				+ str(qstring)
				+ "</abbr></th>"
			)
		elif hyper_link is not None and invs in hyper_link:
			table_header += (
				'<th data-field="'
				+ str(invs)
				+ '" data-filter-control="input" data-formatter="coveredobjectchildHyperLink" data-sortable="true"><abbr title="'
				+ str(qstring)
				+ '">'
				+ str(qstring)
				+ "</abbr></th>"
			)
		else:
			table_header += (
				'<th data-field="'
				+ str(invs)
				+ '" data-filter-control="input" data-sortable="true"><abbr title="'
				+ str(qstring)
				+ '">'
				+ str(qstring)
				+ "</abbr></th>"
			)
	table_header += "</tr>"
	table_header += '</thead><tbody onclick="Table_Onclick_Scroll(this)"></tbody></table>'
	table_ids = "#" + str(table_id)
	filter_control_function = ""
	values_list = ""
	tbl_id = str(table_id)
	for key, invs in enumerate(list(Columns)):
		table_ids = "#" + str(table_id)
		filter_clas = "#" + str(table_id) + " .bootstrap-table-filter-control-" + str(invs)
		values_list += "var " + str(invs) + ' = $("' + str(filter_clas) + '").val(); '
		values_list += "ATTRIBUTE_VALUEList.push(" + str(invs) + "); "
		tbl_id = str(table_id)
	filter_class = "#Act_" + str(table_id)
	filter_control_function += (
		'$("'
		+ filter_class
		+ '").click( function(){ var table_id = $(this).closest("table").attr("id"); ATTRIBUTE_VALUEList = []; '
		+ str(values_list)
		+ ' var attribute_value = $(this).val(); cpq.server.executeScript("CQNESTGRID", {"TABNAME":"Covered Object Child", "ACTION":"PRODUCT_ONLOAD_FILTER", "ATTRIBUTE_NAME": '
		+ str(list(Columns))
		+ ', "ATTRIBUTE_VALUE": ATTRIBUTE_VALUEList, "REC_ID":"'
		+ str(recid)
		+ '" }, function(dataset) { data2 = dataset[1];  data1 = dataset[0]; data3 = dataset[2]; console.log("len ---->"+data1.length);  try { if(data1.length > 0) { $("#'+ str(tbl_id) + '").bootstrapTable("load", data1 );$("#noRecDisp").remove(); if (document.getElementById("'+str(tbl_id) + '___totalItemCount")){document.getElementById("'+str(tbl_id)+ '___totalItemCount").innerHTML = data2;}  if (document.getElementById("'+str(tbl_id) + '___NumberofItem")) {document.getElementById("'+str(tbl_id)+ '___NumberofItem").innerHTML = data3;}} else{ $("#' + str(tbl_id) + '").bootstrapTable("load", data1  );$("#' + str(tbl_id) + '").after("<div id=\'noRecDisp\' class=\'noRecord\'>No Records to Display</div>"); $(".noRecord:not(:first)").remove(); if (document.getElementById("'+str(tbl_id) + '___totalItemCount")){document.getElementById("'+str(tbl_id)+ '___totalItemCount").innerHTML = data2;}  if (document.getElementById("'+str(tbl_id) + '___NumberofItem")) {document.getElementById("'+str(tbl_id)+ '___NumberofItem").innerHTML = data3;} }} catch(err){} }); filter_search_click();$(".JColResizer").mousedown(function(){ $("thead.fullHeadFirst").css("cssText","z-index: 2;border-top: 1px solid rgb(220, 220, 220);top: 154px;border-right: 0px !important;");$("thead.fullHeadSecond").css("display","none"); });$(".JColResizer").mouseup(function(){ var th_width_resize = [];$("#covered_obj_child thead.fullHeadFirst tr th").each(function(index){var wid = $(this).css("width"); if(index ==0 || index ==1){th_width_resize.push("60px");}else{th_width_resize.push(wid);}}); $("thead.fullHeadFirst").css("cssText","position: fixed;z-index: 2;border-top: 1px solid rgb(220, 220, 220); top: 154px;border-right: 0px !important;");$("thead.fullHeadSecond").css("display","table-header-group");$("#covered_obj_child thead.fullHeadFirst tr th").each(function(index){var num = th_width_resize[index].split("px");var numsp = parseInt(num[0]);numsp = numsp - 1;var make_str =numsp+"px"; var c = "width:"+make_str+";white-space: nowrap;overflow: hidden;text-overflow: ellipsis;";var d = "width:"+make_str+";"; $(this).css("cssText",c);$(this).children("div:first-child").css("cssText",c);$(this).children("div.fht-cell").css("cssText",d);});$("#covered_obj_child thead.fullHeadSecond tr th").each(function(index){var num = th_width_resize[index].split("px");var numsp = parseInt(num[0]);numsp = numsp - 1;var make_str =numsp+"px"; var c = "width:"+make_str+";white-space: nowrap;overflow: hidden;text-overflow: ellipsis;";var d = "width:"+make_str+";"; $(this).css("cssText",c);$(this).children("div:first-child").css("cssText",c);$(this).children("div.fht-cell").css("cssText",d);}); });});'
	)
	dbl_clk_function = (
		'$("'
		+ str(table_ids)
		+ '").on("all.bs.table", function (e, name, args) { $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); }); $("'
		+ str(table_ids)
		+ '\ th.bs-checkbox div.th-inner").before("<div style=\'padding:0; border-bottom: 1px solid #dcdcdc;\'>SELECT</div>"); $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); $("'
		+ str(table_ids)
		+ "\").on('sort.bs.table', function (e, name, order) { console.log('sort.bs.table ============>111111111');  currenttab = $(\"ul#carttabs_head .active\").text().trim(); localStorage.setItem('"
		+ str(table_id)
		+ "_SortColumn', name); localStorage.setItem('"
		+ str(table_id)
		+ "_SortColumnOrder', order); NestedContainerSorting(name, order, '"
		+ str(table_id)
		+ "','"
		+str(recid)+"'); }); "
		)
	#Trace.Write("GetCovObjChild dbl_clk_function ----->"+str(dbl_clk_function))

	NORECORDS = ""
	if len(chld_list) == 0:
		NORECORDS = "NORECORDS"

	ObjectName = "SAQSCA"
	DropDownList = []
	filter_level_list = []
	filter_clas_name = ""
	cv_list = []
	TableclassName = "form-control" + table_id
	for key, col_name in enumerate(list(Columns)):
		StringValue_list = []
		objss_obj = Sql.GetFirst(
			"SELECT API_NAME, DATA_TYPE, FORMULA_LOGIC FROM SYOBJD (NOLOCK) WHERE OBJECT_NAME='"
			+ str(ObjectName)
			+ "' and API_NAME = '"
			+ str(col_name)
			+ "'"
		)
		try:
			FORMULA_LOGIC = objss_obj.FORMULA_LOGIC.strip()
			FORMULA_col = FORMULA_LOGIC.split(" ")[1].strip()
			FORMULA_table = FORMULA_LOGIC.split(" ")[3].strip()
			ins_obj = Sql.GetFirst(
				"SELECT API_NAME, DATA_TYPE,PICKLIST FROM SYOBJD (NOLOCK) WHERE OBJECT_NAME='"
				+ str(FORMULA_table)
				+ "' and API_NAME = '"
				+ str(FORMULA_col)
				+ "'"
			)
			if str(objss_obj.PICKLIST).upper() == "TRUE":
				filter_level_data = "select"
				filter_clas_name = (
					'<div id = "'
					+ str(table_id)
					+ "_RelatedMutipleCheckBoxDrop_"
					+ str(key)
					+ '" class="form-control bootstrap-table-filter-control-'
					+ str(col_name)
					+ " RelatedMutipleCheckBoxDrop_"
					+ str(key)
					+ ' "></div>'
				)
				filter_level_list.append(filter_level_data)
			else:
				filter_level_data = "input"
				filter_clas_name = (
					'<input type="text" class="width100_vis form-control bootstrap-table-filter-control-'
					+ str(col_name)
					+ '">'
				)
				filter_level_list.append(filter_level_data)
		except:
			"""if str(objss_obj.PICKLIST).upper() == "TRUE":
				filter_level_data = "select"
				filter_clas_name = (
					'<div id = "'
					+ str(table_id)
					+ "_RelatedMutipleCheckBoxDrop_"
					+ str(key)
					+ '" class="form-control bootstrap-table-filter-control-'
					+ str(col_name)
					+ " RelatedMutipleCheckBoxDrop_"
					+ str(key)
					+ ' "></div>'
				)
				filter_level_list.append(filter_level_data)"""

			filter_level_data = "input"
			filter_clas_name = (
				'<input type="text" class="width100_vis form-control bootstrap-table-filter-control-' + str(col_name) + '">'
			)
			filter_level_list.append(filter_level_data)
		cv_list.append(filter_clas_name)
		if filter_level_data == "select":
			try:
				xcd = Sql.GetFirst(
					"SELECT (STUFF((SELECT DISTINCT ', ' + CAST("
					+ str(col_name)
					+ " AS CHAR(100)) FROM "
					+ str(ObjectName)
					+ " (NOLOCK) where QUOTE_FAB_LOC_COV_OBJ_ASSEMBLY_RECORD_ID = '"
					+ str(recid)
					+ "' FOR XML PATH('') ), 1, 2, '')  ) AS StringValue"
				)
			except:
				xcd = Sql.GetFirst(
					"SELECT (STUFF((SELECT DISTINCT ', ' + CAST("
					+ str(col_name)
					+ " AS CHAR(100)) FROM "
					+ str(ObjectName)
					+ " (NOLOCK) FOR XML PATH('') ), 1, 2, '')  ) AS StringValue"
				)
			if str(xcd.StringValue) is not None and str(xcd.StringValue) != "":
				if str(xcd.StringValue).find(",") != -1:
					StringValue_list = [ins.strip() for ins in str(xcd.StringValue).split(",") if ins.strip() != ""]
				else:
					StringValue_list.append(str(xcd.StringValue))
			else:
				StringValue_list = [""]
			StringValue_list = list(set(StringValue_list))
			DropDownList.append(StringValue_list)
		elif filter_level_data == "checkbox":
			DropDownList.append(["True", "False"])
		else:
			DropDownList.append("")
	RelatedDrop_str = (
		"try { if( document.getElementById('"
		+ str(table_id)
		+ "') ) { var listws = document.getElementById('"
		+ str(table_id)
		+ "').getElementsByClassName('filter-control');  for (i = 0; i < listws.length; i++) { document.getElementById('"
		+ str(table_id)
		+ "').getElementsByClassName('filter-control')[i].innerHTML = datachld6[i];  } for (j = 0; j < listws.length; j++) { if (datachld7[j] == 'select') { if (data8[j]) { var dataAdapter = new $.jqx.dataAdapter(datachld8[j]); $('#"
		+ str(table_id)
		+ "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter, autoDropDownHeight: true }); } } } } }  catch(err) { setTimeout(function() { var listws = document.getElementById('"
		+ str(table_id)
		+ "').getElementsByClassName('filter-control');  for (i = 0; i < listws.length; i++) { document.getElementById('"
		+ str(table_id)
		+ "').getElementsByClassName('filter-control')[i].innerHTML = datachld6[i];  } for (j = 0; j < listws.length; j++) { if (datachld7[j] == 'select') { if (data8[j]) { var dataAdapter = new $.jqx.dataAdapter(datachld8[j]); $('#"
		+ str(table_id)
		+ "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter, autoDropDownHeight: true }); } } } }, 5000); } try { setTimeout(function(){ $('#"
		+ str(table_id)
		+ "').colResizable({ resizeMode:'overflow'}); }, 3000); } catch(err){}"
	)
	page = ""
	if QueryCount < int(PerPage):
		page = str(Page_start) + " - " + str(QueryCount)
	else:
		page = str(Page_start) + " - " + str(Page_End)
	Test = (
		'<div class="col-md-12 brdr listContStyle pad2height30" ><div class="col-md-4 pager-numberofitem clear-padding"><span class="pager-number-of-items-item noofitem" id="'
		+ str(table_id)
		+ '___NumberofItem" >'
		+ str(page)
		+ ' of </span><span class="pager-number-of-items-item fltltpad2mrg0" id="'
		+ str(table_id)
		+ '___totalItemCount" >'
		+ str(QueryCount)
		+ '</span><div class="clear-padding fltltmrgtp3" ><div  class="pull-right vertmidtxtrht"><select onchange="PageFunctestChild(this,\'Quote\',\'\',\''
		+str(table_id)
		+'\')" id="'
		+ str(table_id)
		+ '___PageCountValue"  class="form-control wid65vermiddisinbmarl5"><option value="10" selected>10</option><option value="20">20</option><option value="50">50</option><option value="100">100</option><option value="200">200</option></select> </div></div></div><div class="col-xs-8 col-md-4  clear-padding disinpad10txtcen"  data-bind="visible: totalItemCount"><div class="clear-padding col-xs-12 col-sm-6 col-md-12 bor0" ><ul class="pagination pagination"><li class="disabled"><a href="#" onclick="FirstPageLoad_paginationChild(\'Quote\',\'\',\''
		+str(table_id)
		+'\')"><i class="fa fa-caret-left font14whtbld" ></i><i class="fa fa-caret-left font14" ></i></a></li><li class="disabled"><a href="#" onclick="Previous12334Child(\'Quote\',\'\',\''
		+str(table_id)
		+'\')"><i class="fa fa-caret-left font14" ></i>PREVIOUS</a></li><li class="disabled"><a href="#" class="disabledPage" onclick="Next12334Child(\'Quote\',\'\',\''
		+str(table_id)
		+'\')">NEXT<i class="fa fa-caret-right font14" ></i></a></li><li class="disabled"><a href="#" onclick="LastPageLoad_paginationChild(\'Quote\',\'\',\''
		+str(table_id)
		+'\')" class="disabledPage"><i class="fa fa-caret-right font14"></i><i class="fa fa-caret-right font14whtbld"></i></a></li></ul></div> </div> <div class="col-md-4 pr_page_pad"> <span id="'
		+ str(table_id)
		+ '___page_count" class="currentPage page_right_content">1</span><span class="page_right_content pad_rt_2">Page </span></div></div>'
	)

	#Trace.Write("6565 GetCovObjChild test --->"+str(Test))

	if QueryCount < int(PerPage):
		PerPage = str(QueryCount)
	else:
		PerPage = str(PerPage)   
	if Page_End > QueryCount:
		Page_End = QueryCount
	else:
		Page_End = Page_End
	
	Action_Str = ""
	Action_Str += str(Page_start)+" - "
	Action_Str += str(Page_End)
	Action_Str += " of"
	return (
		table_header,
		chld_list,
		table_id,
		filter_control_function,
		NORECORDS,
		dbl_clk_function,
		cv_list,
		filter_level_list,
		DropDownList,
		RelatedDrop_str,
		Test,
		Action_Str,
	)


def GetCovObjMasterFilter(ATTRIBUTE_NAME, ATTRIBUTE_VALUE,PerPage,PageInform):

	if str(PerPage) == "" and str(PageInform) == "":
		Page_start = 1
		Page_End = 10
		PerPage = 10
		PageInform = "1___10___10"
	else:
		Page_start = int(PageInform.split("___")[0])
		Page_End = int(PageInform.split("___")[1])
		PerPage = PerPage
	QueryCount = ""
	TreeParam = Product.GetGlobal("TreeParam")
	TreeParentParam = Product.GetGlobal("TreeParentLevel0")
	TreeSuperParentParam = Product.GetGlobal("TreeParentLevel1")
	TreeTopSuperParentParam = Product.GetGlobal("TreeParentLevel2")

	# FablocationId = Product.GetGlobal("TreeParam")
	ContractRecordId = Quote.GetGlobal("contract_quote_record_id")
	RevisionRecordId = Quote.GetGlobal("quote_revision_record_id")
	ATTRIBUTE_VALUE_STR = ""
	Dict_formation = dict(zip(ATTRIBUTE_NAME, ATTRIBUTE_VALUE))
	for quer_key, quer_value in enumerate(Dict_formation):
		if Dict_formation.get(quer_value) != "":            
			quer_values = str(Dict_formation.get(quer_value)).strip()
			if str(quer_values).upper() == "TRUE":
				quer_values = "TRUE"
			elif str(quer_values).upper() == "FALSE":
				quer_values = "FALSE"
			if str(quer_values).find(",") == -1:
				ATTRIBUTE_VALUE_STR += str(quer_value) + " like '%" + str(quer_values) + "%' and "
			else:
				quer_values = quer_values.split(",")
				quer_values = tuple(list(quer_values))
				ATTRIBUTE_VALUE_STR += str(quer_value) + " in " + str(quer_values) + " and "
			if str(quer_value) == 'QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID':                
				if str(str(quer_values)).find("-") == -1:                            
					ATTRIBUTE_VALUE_STR = (" CpqTableEntryId = '"+ str(quer_values)+ "' and ")                            
				else:
					xa_str = str(quer_values).split("-")[1]                            
					ATTRIBUTE_VALUE_STR = (" CpqTableEntryId = '"+ str(xa_str)+ "' and ")

	data_list = []
	rec_id = "SYOBJ_00904"
	obj_id = "SYOBJ-00904"
	objh_getid = Sql.GetFirst(
		"SELECT TOP 1  RECORD_ID  FROM SYOBJH (NOLOCK) WHERE SAPCPQ_ATTRIBUTE_NAME='" + str(obj_id) + "'"
	)
	if objh_getid:
		obj_id = objh_getid.RECORD_ID
	objs_obj = Sql.GetFirst(
		"select CAN_ADD,CAN_EDIT,COLUMNS,CAN_DELETE from SYOBJR (NOLOCK) where OBJ_REC_ID = '" + str(obj_id) + "' "
	)
	can_edit = str(objs_obj.CAN_EDIT)
	can_clone = str(objs_obj.CAN_ADD)
	can_delete = str(objs_obj.CAN_DELETE)

	orderby = ""
	if SortColumn != '' and SortColumnOrder !='':
		orderby = SortColumn + " " + SortColumnOrder
	else:
		orderby = "QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID"


	if ATTRIBUTE_VALUE is None or ATTRIBUTE_VALUE == "" or ATTRIBUTE_VALUE_STR is None or ATTRIBUTE_VALUE_STR == "":
		Trace.Write("empty search")
		if TreeSuperParentParam == "Product Offerings" or TreeParentParam == "Add-On Products":
			parent_obj = Sql.GetList(
				"SELECT TOP "+str(PerPage)+" QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,EQUIPMENT_ID,EQUIPMENT_DESCRIPTION,SERIAL_NO,GREENBOOK,FABLOCATION_ID, WARRANTY_END_DATE,WARRANTY_START_DATE,MNT_PLANT_ID,EQUIPMENT_STATUS,CUSTOMER_TOOL_ID,EQUIPMENTCATEGORY_ID AS DESCRIPTION,SNDFBL_ID,WARRANTY_END_DATE_ALERT from SAQSCO (NOLOCK) where QUOTE_RECORD_ID = '"
				+ str(ContractRecordId)
				+ "' and QTEREV_RECORD_ID = '"
				+ str(RevisionRecordId)
				+ "' AND SERVICE_ID = '"
				+ str(TreeParam)
				+ "' AND SERVICE_TYPE ='"
				+ str(TreeParentParam)
				+ "' ORDER BY "  + str(orderby) 
			)
			QueryCountObj = Sql.GetFirst(
					"SELECT count(*) as cnt from SAQSCO (NOLOCK) where QUOTE_RECORD_ID = '"
				+ str(ContractRecordId)
				+ "' and QTEREV_RECORD_ID = '"
				+ str(RevisionRecordId)
				+ "' AND SERVICE_ID = '"
				+ str(TreeParam)
				+ "' AND SERVICE_TYPE ='"
				+ str(TreeParentParam)
				+ "'" 
				)
			if QueryCountObj is not None:
				QueryCount = QueryCountObj.cnt




		else:
			if TreeTopSuperParentParam == "Product Offerings":
				if TreeParam == "Receiving Equipment":
					parent_obj = Sql.GetList(
						"SELECT top "+str(PerPage)+" QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,EQUIPMENT_ID,EQUIPMENT_DESCRIPTION,SERIAL_NO,GREENBOOK,FABLOCATION_ID, WARRANTY_END_DATE,WARRANTY_START_DATE,MNT_PLANT_ID,EQUIPMENT_STATUS,CUSTOMER_TOOL_ID,EQUIPMENTCATEGORY_ID AS DESCRIPTION,WARRANTY_END_DATE_ALERT from SAQSCO (NOLOCK) where  QUOTE_RECORD_ID = '"
						+ str(ContractRecordId)
						+ "' and QTEREV_RECORD_ID = '"
						+ str(RevisionRecordId)
						+ "' AND SERVICE_ID = '"
						+ str(TreeParentParam)
						+ "' AND SERVICE_TYPE ='"
						+ str(TreeSuperParentParam)
						+ "' AND RELOCATION_EQUIPMENT_TYPE = '"
						+ str(TreeParam)
						+ "' ORDER BY "  + str(orderby) 
					)
					QueryCountObj = Sql.GetFirst(
						"SELECT count(*) as cnt from SAQSCO (NOLOCK) where QUOTE_RECORD_ID = '"
						+ str(ContractRecordId)
						+ "' and QTEREV_RECORD_ID = '"
						+ str(RevisionRecordId)
						+ "' AND SERVICE_ID = '"
						+ str(TreeParentParam)
						+ "' AND SERVICE_TYPE ='"
						+ str(TreeSuperParentParam)
						+ "' AND RELOCATION_EQUIPMENT_TYPE = '"
						+ str(TreeParam)
						+ "'"
					)
				else:
					if str(TreeSuperParentParam)=="Comprehensive Services":
						equipment_column = " EQUIPMENTCATEGORY_ID AS DESCRIPTION "
					else:
						equipment_column = " EQUIPMENTCATEGORY_ID "
					parent_obj = Sql.GetList(
						"SELECT TOP "+str(PerPage)+" QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,EQUIPMENT_ID,EQUIPMENT_DESCRIPTION,SERIAL_NO,GREENBOOK,FABLOCATION_ID, WARRANTY_END_DATE,WARRANTY_START_DATE,MNT_PLANT_ID,EQUIPMENT_STATUS,CUSTOMER_TOOL_ID,"+str(equipment_column)+",WARRANTY_END_DATE_ALERT from SAQSCO (NOLOCK) where QUOTE_RECORD_ID = '"
						+ str(ContractRecordId)
						+ "' and QTEREV_RECORD_ID = '"
						+ str(RevisionRecordId)
						+ "'AND SERVICE_ID = '"
						+ str(TreeParentParam)
						+ "' AND SERVICE_TYPE ='"
						+ str(TreeSuperParentParam)
						+ "' AND FABLOCATION_ID = '"
						+ str(TreeParam)
						+ "' ORDER BY "  + str(orderby) 
					)

					QueryCountObj = Sql.GetFirst(
						"SELECT count(*) as cnt from SAQSCO (NOLOCK) where QUOTE_RECORD_ID = '"
						+ str(ContractRecordId)
						+ "' and QTEREV_RECORD_ID = '"
						+ str(RevisionRecordId)
						+ "' AND SERVICE_ID = '"
						+ str(TreeParentParam)
						+ "' AND SERVICE_TYPE ='"
						+ str(TreeSuperParentParam)
						+ "' AND FABLOCATION_ID = '"
						+ str(TreeParam)
						+ "' " 
					)
				if QueryCountObj is not None:
					QueryCount = QueryCountObj.cnt

			else:
				Trace.Write("5 level empty search --->")
				if str(TreeTopSuperParentParam)=="Comprehensive Services" or str(TreeParam) == "Receiving Equipment" or str(TreeParentParam) == "Receiving Equipment" or str(TreeSuperParentParam) == "Receiving Equipment":
					equipment_column = " EQUIPMENTCATEGORY_ID AS DESCRIPTION "
					if ATTRIBUTE_VALUE_STR.startswith("DESCRIPTION"):
						ATTRIBUTE_VALUE_STR = str(ATTRIBUTE_VALUE_STR).replace('DESCRIPTION','EQUIPMENTCATEGORY_ID')
				else:
					equipment_column = " EQUIPMENTCATEGORY_ID "

				if TreeParam == "Receiving Equipment":
					parent_obj = Sql.GetList(
						"SELECT top "+str(PerPage)+" QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,EQUIPMENT_ID,EQUIPMENT_DESCRIPTION,SERIAL_NO,GREENBOOK,FABLOCATION_ID, WARRANTY_END_DATE,WARRANTY_START_DATE,MNT_PLANT_ID,EQUIPMENT_STATUS,CUSTOMER_TOOL_ID,"+str(equipment_column)+",WARRANTY_END_DATE_ALERT from SAQSCO (NOLOCK) where "+ str(ATTRIBUTE_VALUE_STR)+ " 1=1 and QUOTE_RECORD_ID = '"+ str(ContractRecordId)+ "' and QTEREV_RECORD_ID = '"+ str(RevisionRecordId)+ "' AND SERVICE_TYPE = '"+ str(TreeTopSuperParentParam)+ "' AND SERVICE_ID ='"+ str(TreeSuperParentParam)+ "' ORDER BY "  + str(orderby))

					QueryCountObj = Sql.GetFirst(
						"SELECT count(*) as cnt from SAQSCO (NOLOCK) where "+ str(ATTRIBUTE_VALUE_STR)+ " 1=1 and QUOTE_RECORD_ID = '"+ str(ContractRecordId)+ "' and QTEREV_RECORD_ID = '"+ str(RevisionRecordId)+ "' AND SERVICE_TYPE = '"+ str(TreeTopSuperParentParam)+ "' AND SERVICE_ID ='"+ str(TreeSuperParentParam)+ "' "  
					)
					if QueryCountObj is not None:
						QueryCount = QueryCountObj.cnt 

				elif TreeParentParam == "Receiving Equipment":
					parent_obj = Sql.GetList(
						"SELECT top "+str(PerPage)+" QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,EQUIPMENT_ID,EQUIPMENT_DESCRIPTION,SERIAL_NO,GREENBOOK,FABLOCATION_ID, WARRANTY_END_DATE,WARRANTY_START_DATE,MNT_PLANT_ID,EQUIPMENT_STATUS,CUSTOMER_TOOL_ID,"+str(equipment_column)+",WARRANTY_END_DATE_ALERT from SAQSCO (NOLOCK) where "
						+ str(ATTRIBUTE_VALUE_STR)
						+ " 1=1 and QUOTE_RECORD_ID = '"
						+ str(ContractRecordId)
						+ "' and QTEREV_RECORD_ID = '"+ str(RevisionRecordId)+ "' AND SERVICE_TYPE = '"
						+ str(TreeTopSuperParentParam)
						+ "' AND SERVICE_ID ='"
						+ str(TreeSuperParentParam)
						+ "' AND FABLOCATION_ID = '"
						+ str(TreeParam)                        
						+ "' ORDER BY "  + str(orderby) 
					)

					QueryCountObj = Sql.GetFirst(
						"SELECT count(*) as cnt from SAQSCO (NOLOCK) where "
						+ str(ATTRIBUTE_VALUE_STR)
						+ " 1=1 and QUOTE_RECORD_ID = '"
						+ str(ContractRecordId)
						+ "' and QTEREV_RECORD_ID = '"
						+ str(RevisionRecordId)
						+ "' AND SERVICE_TYPE = '"
						+ str(TreeTopSuperParentParam)
						+ "' AND SERVICE_ID ='"
						+ str(TreeSuperParentParam)
						+ "' AND FABLOCATION_ID = '"
						+ str(TreeParam)                        
						+ "' "  
					)
					if QueryCountObj is not None:
						QueryCount = QueryCountObj.cnt
				else:            
					parent_obj = Sql.GetList(
						"SELECT top "+str(PerPage)+" QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,EQUIPMENT_ID,EQUIPMENT_DESCRIPTION,SERIAL_NO,GREENBOOK,FABLOCATION_ID, WARRANTY_END_DATE,WARRANTY_START_DATE,MNT_PLANT_ID,EQUIPMENT_STATUS,CUSTOMER_TOOL_ID,"+str(equipment_column)+",WARRANTY_END_DATE_ALERT from SAQSCO (NOLOCK) where QUOTE_RECORD_ID = '"
						+ str(ContractRecordId)
						+ "' and QTEREV_RECORD_ID = '"
						+ str(RevisionRecordId)
						+ "' AND SERVICE_TYPE = '"
						+ str(TreeTopSuperParentParam)
						+ "' AND SERVICE_ID ='"
						+ str(TreeSuperParentParam)
						+ "' AND FABLOCATION_ID = '"
						+ str(TreeParentParam)
						+ "' AND GREENBOOK = '"
						+ str(TreeParam)
						+ "' ORDER BY "  + str(orderby) 
					)
					
					QueryCountObj = Sql.GetFirst(
						"SELECT count(*) as cnt from SAQSCO (NOLOCK) where QUOTE_RECORD_ID = '"
						+ str(ContractRecordId)
						+ "' and QTEREV_RECORD_ID = '"
						+ str(RevisionRecordId)
						+ "' AND SERVICE_TYPE = '"
						+ str(TreeTopSuperParentParam)
						+ "' AND SERVICE_ID ='"
						+ str(TreeSuperParentParam)
						+ "' AND FABLOCATION_ID = '"
						+ str(TreeParentParam)
						+ "' AND GREENBOOK = '"
						+ str(TreeParam)
						+ "'"
						)
					if QueryCountObj is not None:
						QueryCount = QueryCountObj.cnt


	else:
		Trace.Write("search with condition123")
		if TreeSuperParentParam == "Product Offerings" or TreeParentParam == "Add-On Products":
			parent_obj = Sql.GetList(
				"SELECT top "+str(PerPage)+" QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,EQUIPMENT_ID,EQUIPMENT_DESCRIPTION,SERIAL_NO,GREENBOOK,FABLOCATION_ID, WARRANTY_END_DATE,WARRANTY_START_DATE,MNT_PLANT_ID,EQUIPMENT_STATUS,CUSTOMER_TOOL_ID,EQUIPMENTCATEGORY_ID,EQUIPMENTCATEGORY_ID AS DESCRIPTION,SNDFBL_ID,WARRANTY_END_DATE_ALERT from SAQSCO (NOLOCK) where "
				+ str(ATTRIBUTE_VALUE_STR)
				+ " 1=1 and QUOTE_RECORD_ID = '"
				+ str(ContractRecordId)
				+ "' and QTEREV_RECORD_ID = '"
				+ str(RevisionRecordId)
				+ "' AND SERVICE_ID = '"
				+ str(TreeParam)
				+ "' AND SERVICE_TYPE ='"
				+ str(TreeParentParam)
				+ "' ORDER BY "  + str(orderby) 
			)

			QueryCountObj = Sql.GetFirst(
					"SELECT count(*) as cnt from SAQSCO (NOLOCK) where "
				+ str(ATTRIBUTE_VALUE_STR)
				+ " 1=1 and QUOTE_RECORD_ID = '"
				+ str(ContractRecordId)
				+ "' and QTEREV_RECORD_ID = '"
				+ str(RevisionRecordId)
				+ "' AND SERVICE_ID = '"
				+ str(TreeParam)
				+ "' AND SERVICE_TYPE ='"
				+ str(TreeParentParam)
				+ "'" 
				)
			if QueryCountObj is not None:
				QueryCount = QueryCountObj.cnt


		else:
			if TreeTopSuperParentParam == "Product Offerings":
				if TreeParam == "Receiving Equipment":
					parent_obj = Sql.GetList(
						"SELECT top "+str(PerPage)+" QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,EQUIPMENT_ID,EQUIPMENT_DESCRIPTION,SERIAL_NO,GREENBOOK,FABLOCATION_ID, WARRANTY_END_DATE,WARRANTY_START_DATE,MNT_PLANT_ID,EQUIPMENT_STATUS,CUSTOMER_TOOL_ID,EQUIPMENTCATEGORY_ID AS DESCRIPTION,WARRANTY_END_DATE_ALERT from SAQSCO (NOLOCK) where "
						+ str(ATTRIBUTE_VALUE_STR)
						+ " 1=1 and QUOTE_RECORD_ID = '"
						+ str(ContractRecordId)
						+ "' and QTEREV_RECORD_ID = '"
						+ str(RevisionRecordId)
						+ "' AND SERVICE_ID = '"
						+ str(TreeParentParam)
						+ "' AND SERVICE_TYPE ='"
						+ str(TreeSuperParentParam)
						+ "' AND RELOCATION_EQUIPMENT_TYPE = '"
						+ str(TreeParam)
						+ "' ORDER BY "  + str(orderby) 
					)

					QueryCountObj = Sql.GetFirst(
						"SELECT count(*) as cnt from SAQSCO (NOLOCK) where "
						+ str(ATTRIBUTE_VALUE_STR)
						+ " 1=1 and QUOTE_RECORD_ID = '"
						+ str(ContractRecordId)
						+ "' and QTEREV_RECORD_ID = '"
						+ str(RevisionRecordId)
						+ "' AND SERVICE_ID = '"
						+ str(TreeParentParam)
						+ "' AND SERVICE_TYPE ='"
						+ str(TreeSuperParentParam)
						+ "' AND RELOCATION_EQUIPMENT_TYPE = '"
						+ str(TreeParam)
						+ "'"
					)
				else:    
					if str(TreeSuperParentParam)=="Comprehensive Services":
						equipment_column = " EQUIPMENTCATEGORY_ID AS DESCRIPTION "
					else:
						equipment_column = " EQUIPMENTCATEGORY_ID "
					parent_obj = Sql.GetList(
						"SELECT top "+str(PerPage)+" QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,EQUIPMENT_ID,EQUIPMENT_DESCRIPTION,SERIAL_NO,GREENBOOK,FABLOCATION_ID, WARRANTY_END_DATE,WARRANTY_START_DATE,MNT_PLANT_ID,EQUIPMENT_STATUS,CUSTOMER_TOOL_ID,"+str(equipment_column)+",WARRANTY_END_DATE_ALERT from SAQSCO (NOLOCK) where "
						+ str(ATTRIBUTE_VALUE_STR)
						+ " 1=1 and QUOTE_RECORD_ID = '"
						+ str(ContractRecordId)
						+ "' and QTEREV_RECORD_ID = '"
						+ str(RevisionRecordId)
						+ "' AND SERVICE_ID = '"
						+ str(TreeParentParam)
						+ "' AND SERVICE_TYPE ='"
						+ str(TreeSuperParentParam)
						+ "' AND FABLOCATION_ID = '"
						+ str(TreeParam)
						+ "' ORDER BY "  + str(orderby) 
					)

					QueryCountObj = Sql.GetFirst(
						"SELECT count(*) as cnt from SAQSCO (NOLOCK) where "
						+ str(ATTRIBUTE_VALUE_STR)
						+ " 1=1 and QUOTE_RECORD_ID = '"
						+ str(ContractRecordId)
						+ "' and QTEREV_RECORD_ID = '"
						+ str(RevisionRecordId)
						+ "'AND SERVICE_ID = '"
						+ str(TreeParentParam)
						+ "' AND SERVICE_TYPE ='"
						+ str(TreeSuperParentParam)
						+ "' AND FABLOCATION_ID = '"
						+ str(TreeParam)
						+ "'"
					)
				if QueryCountObj is not None:
					QueryCount = QueryCountObj.cnt

			else:
				Trace.Write("5 level tree --->")
				if str(TreeTopSuperParentParam)=="Comprehensive Services" or str(TreeParam) == "Receiving Equipment" or str(TreeParentParam) == "Receiving Equipment" or str(TreeSuperParentParam) == "Receiving Equipment":
					equipment_column = " EQUIPMENTCATEGORY_ID AS DESCRIPTION "
					if ATTRIBUTE_VALUE_STR.startswith("DESCRIPTION"):
						ATTRIBUTE_VALUE_STR = str(ATTRIBUTE_VALUE_STR).replace('DESCRIPTION','EQUIPMENTCATEGORY_ID')
				else:
					equipment_column = " EQUIPMENTCATEGORY_ID "

				if TreeParam == "Receiving Equipment":
					parent_obj = Sql.GetList(
						"SELECT top "+str(PerPage)+" QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,EQUIPMENT_ID,EQUIPMENT_DESCRIPTION,SERIAL_NO,GREENBOOK,FABLOCATION_ID, WARRANTY_END_DATE,WARRANTY_START_DATE,MNT_PLANT_ID,EQUIPMENT_STATUS,CUSTOMER_TOOL_ID,"+str(equipment_column)+",WARRANTY_END_DATE_ALERT from SAQSCO (NOLOCK) where "+ str(ATTRIBUTE_VALUE_STR)+ " 1=1 and QUOTE_RECORD_ID = '"+ str(ContractRecordId)+ "' and QTEREV_RECORD_ID = '"+ str(RevisionRecordId)+ "' AND SERVICE_TYPE = '"+ str(TreeTopSuperParentParam)+ "' AND SERVICE_ID ='"+ str(TreeSuperParentParam)+ "' ORDER BY "  + str(orderby))

					QueryCountObj = Sql.GetFirst(
						"SELECT count(*) as cnt from SAQSCO (NOLOCK) where "+ str(ATTRIBUTE_VALUE_STR)+ " 1=1 and QUOTE_RECORD_ID = '"+ str(ContractRecordId)+ "' and QTEREV_RECORD_ID = '"+ str(RevisionRecordId)+ "' AND SERVICE_TYPE = '"+ str(TreeTopSuperParentParam)+ "' AND SERVICE_ID ='"+ str(TreeSuperParentParam)+ "' "  
					)
					if QueryCountObj is not None:
						QueryCount = QueryCountObj.cnt 

				elif TreeParentParam == "Receiving Equipment":
					parent_obj = Sql.GetList(
						"SELECT top "+str(PerPage)+" QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,EQUIPMENT_ID,EQUIPMENT_DESCRIPTION,SERIAL_NO,GREENBOOK,FABLOCATION_ID, WARRANTY_END_DATE,WARRANTY_START_DATE,MNT_PLANT_ID,EQUIPMENT_STATUS,CUSTOMER_TOOL_ID,"+str(equipment_column)+",WARRANTY_END_DATE_ALERT from SAQSCO (NOLOCK) where "
						+ str(ATTRIBUTE_VALUE_STR)
						+ " 1=1 and QUOTE_RECORD_ID = '"
						+ str(ContractRecordId)
						+ "' and QTEREV_RECORD_ID = '"
						+ str(RevisionRecordId)
						+ "' AND SERVICE_TYPE = '"
						+ str(TreeTopSuperParentParam)
						+ "' AND SERVICE_ID ='"
						+ str(TreeSuperParentParam)
						+ "' AND FABLOCATION_ID = '"
						+ str(TreeParam)                        
						+ "' ORDER BY "  + str(orderby) 
					)

					QueryCountObj = Sql.GetFirst(
						"SELECT count(*) as cnt from SAQSCO (NOLOCK) where "
						+ str(ATTRIBUTE_VALUE_STR)
						+ " 1=1 and QUOTE_RECORD_ID = '"
						+ str(ContractRecordId)
						+ "' and QTEREV_RECORD_ID = '"
						+ str(RevisionRecordId)
						+ "' AND SERVICE_TYPE = '"
						+ str(TreeTopSuperParentParam)
						+ "' AND SERVICE_ID ='"
						+ str(TreeSuperParentParam)
						+ "' AND FABLOCATION_ID = '"
						+ str(TreeParam)                        
						+ "' "  
					)
					if QueryCountObj is not None:
						QueryCount = QueryCountObj.cnt
				else:             
					parent_obj = Sql.GetList(
						"SELECT top "+str(PerPage)+" QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID,EQUIPMENT_ID,EQUIPMENT_DESCRIPTION,SERIAL_NO,GREENBOOK,FABLOCATION_ID, WARRANTY_END_DATE,WARRANTY_START_DATE,MNT_PLANT_ID,EQUIPMENT_STATUS,CUSTOMER_TOOL_ID,"+str(equipment_column)+",WARRANTY_END_DATE_ALERT from SAQSCO (NOLOCK) where "
						+ str(ATTRIBUTE_VALUE_STR)
						+ " 1=1 and QUOTE_RECORD_ID = '"
						+ str(ContractRecordId)
						+ "' and QTEREV_RECORD_ID = '"
						+ str(RevisionRecordId)
						+ "' AND SERVICE_TYPE = '"
						+ str(TreeTopSuperParentParam)
						+ "' AND SERVICE_ID ='"
						+ str(TreeSuperParentParam)
						+ "' AND FABLOCATION_ID = '"
						+ str(TreeParentParam)
						+ "' AND GREENBOOK = '"
						+ str(TreeParam)
						+ "' ORDER BY "  + str(orderby) 
					)

					QueryCountObj = Sql.GetFirst(
						"SELECT count(*) as cnt from SAQSCO (NOLOCK) where "
						+ str(ATTRIBUTE_VALUE_STR)
						+ " 1=1 and QUOTE_RECORD_ID = '"
						+ str(ContractRecordId)
						+ "' and QTEREV_RECORD_ID = '"
						+ str(RevisionRecordId)
						+ "' AND SERVICE_TYPE = '"
						+ str(TreeTopSuperParentParam)
						+ "' AND SERVICE_ID ='"
						+ str(TreeSuperParentParam)
						+ "' AND FABLOCATION_ID = '"
						+ str(TreeParentParam)
						+ "' AND GREENBOOK = '"
						+ str(TreeParam)
						+ "' "  
					)
					if QueryCountObj is not None:
						QueryCount = QueryCountObj.cnt

	for par in parent_obj:
		data_dict = {}
		data_id = str(par.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID)

		Action_str = (
			'<div class="btn-group dropdown"><div class="dropdown" id="ctr_drop"><i data-toggle="dropdown" id="dropdownMenuButton" class="fa fa-sort-desc dropdown-toggle" aria-expanded="false"></i><ul class="dropdown-menu left" aria-labelledby="dropdownMenuButton"><li><a class="dropdown-item cur_sty" href="#" id="'
			+ str(data_id)
			+ '" onclick="Commonteree_view_RL(this)">VIEW</a></li>'
		)
		if can_edit.upper() == "TRUE":
			Action_str += (
				'<li style="display:none" ><a class="dropdown-item cur_sty" href="#" id="'
				+ str(data_id)
				+ '" onclick="Move_to_parent_obj_edit(this)">EDIT</a></li>'
			)
		if can_delete.upper() == "TRUE":
			Action_str += '<li><a class="dropdown-item" data-target="#cont_viewModal_Material_Delete" data-toggle="modal" onclick="Material_delete_obj(this)" href="#">DELETE</a></li>'
		if can_clone.upper() == "TRUE":
			Action_str += '<li><a class="dropdown-item" data-target="#" data-toggle="modal" onclick="Material_clone_obj(this)" href="#">CLONE</a></li>'

		Action_str += "</ul></div></div>"
		data_dict = {}
		data_dict["ids"] = str(data_id)
		data_dict["ACTIONS"] = str(Action_str)
		data_dict["QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID"] = CPQID.KeyCPQId.GetCPQId(
			"SAQSCO", str(par.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID)
		)
		data_dict["EQUIPMENT_ID"] = ('<abbr id ="" title="' + str(par.EQUIPMENT_ID) + '">' + str(par.EQUIPMENT_ID) + "</abbr>") 
		data_dict["EQUIPMENT_DESCRIPTION"] = ('<abbr id ="" title="' + str(par.EQUIPMENT_DESCRIPTION) + '">' + str(par.EQUIPMENT_DESCRIPTION) + "</abbr>")
		data_dict["FABLOCATION_ID"] = ('<abbr id ="" title="' + str(par.FABLOCATION_ID) + '">' + str(par.FABLOCATION_ID) + "</abbr>") 
		data_dict["GREENBOOK"] = ('<abbr id ="" title="' + str(par.GREENBOOK) + '">' + str(par.GREENBOOK) + "</abbr>") 
		data_dict["SERIAL_NO"] = ('<abbr id ="" title="' + str(par.SERIAL_NO) + '">' + str(par.SERIAL_NO) + "</abbr>") 
		try:
			data_dict["DESCRIPTION"] = ('<abbr id ="" title="' + str(par.DESCRIPTION) + '">' + str(par.DESCRIPTION) + "</abbr>") 
		except:
			data_dict["EQUIPMENTCATEGORY_ID"] = ('<abbr id ="" title="' + str(par.EQUIPMENTCATEGORY_ID) + '">' + str(par.EQUIPMENTCATEGORY_ID) + "</abbr>") 
		data_dict["CUSTOMER_TOOL_ID"] = ('<abbr id ="" title="' + str(par.CUSTOMER_TOOL_ID) + '">' + str(par.CUSTOMER_TOOL_ID) + "</abbr>") 
		data_dict["EQUIPMENT_STATUS"] = ('<abbr id ="" title="' + str(par.EQUIPMENT_STATUS) + '">' + str(par.EQUIPMENT_STATUS) + "</abbr>") 
		data_dict["MNT_PLANT_ID"] = ('<abbr id ="" title="' + str(par.MNT_PLANT_ID) + '">' + str(par.MNT_PLANT_ID) + "</abbr>") 
		data_dict["WARRANTY_START_DATE"] = ('<abbr id ="" title="' + str(par.WARRANTY_START_DATE) + '">' + str(par.WARRANTY_START_DATE) + "</abbr>")
		data_dict["WARRANTY_END_DATE"] = ('<abbr id ="" title="' + str(par.WARRANTY_END_DATE) + '">' + str(par.WARRANTY_END_DATE) + "</abbr>")
		data_dict["WARRANTY_END_DATE_ALERT"] = str(par.WARRANTY_END_DATE_ALERT) 
		data_list.append(data_dict)
		"""page = ""
		if QueryCount < int(PerPage):
			page = str(Page_start) + " - " + str(QueryCount)
		else:
			page = str(Page_start) + " - " + str(Page_End)
		Test = (
			'<div class="col-md-12 brdr listContStyle pad2height30" ><div class="col-md-4 pager-numberofitem clear-padding"><span class="pager-number-of-items-item noofitem" id="NumberofItem" >' + str(page) +' of </span><span class="pager-number-of-items-item fltltpad2mrg0" id="totalItemCount" >'
			+ str(QueryCount)
			+ '</span><div class="clear-padding fltltmrgtp3" ><div  class="pull-right vertmidtxtrht"><select onchange="PageFunctestChild(this,\'Quotes\')" id="PageCountValue"  class="form-control wid65vermiddisinbmarl5"><option value="10" selected>10</option><option value="20">20</option><option value="50">50</option><option value="100">100</option><option value="200">200</option></select> </div></div></div><div class="col-xs-8 col-md-4  clear-padding disinpad10txtcen"  data-bind="visible: totalItemCount"><div class="clear-padding col-xs-12 col-sm-6 col-md-12 bor0" ><ul class="pagination pagination"><li class="disabled"><a href="#" onclick="FirstPageLoad_paginationChild(
				
			)"><i class="fa fa-caret-left font14whtbld" ></i><i class="fa fa-caret-left font14" ></i></a></li><li class="disabled"><a href="#" onclick="Previous12334Child(\'Quotes\')"><i class="fa fa-caret-left font14" ></i>PREVIOUS</a></li><li class="disabled"><a href="#" class="disabledPage" onclick="Next12334Child(\'Quotes\',\'\',\'table_covered_obj_parent\')">NEXT<i class="fa fa-caret-right font14" ></i></a></li><li class="disabled"><a href="#" onclick="LastPageLoad_paginationChild(\'Quotes\')" class="disabledPage"><i class="fa fa-caret-right font14"></i><i class="fa fa-caret-right font14whtbld"></i></a></li></ul></div> </div> <div class="col-md-4 pr_page_pad"> <span id="page_count" class="currentPage page_right_content">1</span><span class="page_right_content pad_rt_2">Page </span></div></div>'
		)"""


	page = ""
	if QueryCount == 0:
		page = str(QueryCount) + " - " + str(QueryCount) + " of "
	elif QueryCount < int(PerPage):
		page = str(Page_start) + " - " + str(QueryCount) + " of "
	else:
		page = str(Page_start) + " - " + str(Page_End)+ " of "
	#return data_list, QueryCount, page
	# Trace.Write("7777 data_list --->"+str(data_list))
	# Trace.Write("7777 QueryCount ---->"+str(QueryCount))
	# Trace.Write("7777 page --->"+str(page))
	return data_list, QueryCount, page

def GetContractCovObjMasterFilter(ATTRIBUTE_NAME, ATTRIBUTE_VALUE,PerPage,PageInform):
	if str(PerPage) == "" and str(PageInform) == "":
		Page_start = 1
		Page_End = 10
		PerPage = 10
		PageInform = "1___10___10"
	else:
		Page_start = int(PageInform.split("___")[0])
		Page_End = int(PageInform.split("___")[1])
		PerPage = PerPage
	QueryCount = ""
	TreeParam = Product.GetGlobal("TreeParam")
	TreeParentParam = Product.GetGlobal("TreeParentLevel0")
	TreeSuperParentParam = Product.GetGlobal("TreeParentLevel1")
	TreeTopSuperParentParam = Product.GetGlobal("TreeParentLevel2")

	# FablocationId = Product.GetGlobal("TreeParam")
	ContractRecordId = Product.GetGlobal("contract_record_id")
	ATTRIBUTE_VALUE_STR = ""
	Dict_formation = dict(zip(ATTRIBUTE_NAME, ATTRIBUTE_VALUE))

	orderby = ""
	if SortColumn != '' and SortColumnOrder !='':
		orderby = SortColumn + " " + SortColumnOrder
	else:
		orderby = "CONTRACT_SERVICE_EQUIPMENT_RECORD_ID"


	for quer_key, quer_value in enumerate(Dict_formation):
		x_picklistcheckobj = Sql.GetFirst(
			"SELECT PICKLIST FROM SYOBJD (NOLOCK) WHERE OBJECT_NAME ='CTCSCO' AND API_NAME = '" + str(quer_value) + "'"
		)
		x_picklistcheck = str(x_picklistcheckobj.PICKLIST).upper()
		if Dict_formation.get(quer_value) != "":            
			quer_values = str(Dict_formation.get(quer_value)).strip()
			if str(quer_values).upper() == "TRUE":
				quer_values = "TRUE"
			elif str(quer_values).upper() == "FALSE":
				quer_values = "FALSE"
			if str(quer_values).find(",") == -1:
				if x_picklistcheck == "TRUE":
					ATTRIBUTE_VALUE_STR += str(quer_value) + " = '" + str(quer_values) + "' and "
				else:
					ATTRIBUTE_VALUE_STR += str(quer_value) + " like '%" + str(quer_values) + "%' and "
			else:
				quer_values = quer_values.split(",")
				quer_values = tuple(list(quer_values))
				ATTRIBUTE_VALUE_STR += str(quer_value) + " in " + str(quer_values) + " and "
			if str(quer_value) == 'CONTRACT_SERVICE_EQUIPMENT_RECORD_ID':                
				if str(str(quer_values)).find("-") == -1:                            
					ATTRIBUTE_VALUE_STR = (" CpqTableEntryId = '"+ str(quer_values)+ "' and ")                            
				else:
					xa_str = str(quer_values).split("-")[1]                            
					ATTRIBUTE_VALUE_STR = (" CpqTableEntryId = '"+ str(xa_str)+ "' and ")

	data_list = []
	rec_id = "SYOBJ_00267"
	obj_id = "SYOBJ-00267"
	objh_getid = Sql.GetFirst(
		"SELECT TOP 1  RECORD_ID  FROM SYOBJH (NOLOCK) WHERE SAPCPQ_ATTRIBUTE_NAME='" + str(obj_id) + "'"
	)
	if objh_getid:
		obj_id = objh_getid.RECORD_ID
	objs_obj = Sql.GetFirst(
		"select CAN_ADD,CAN_EDIT,COLUMNS,CAN_DELETE from SYOBJR (NOLOCK) where OBJ_REC_ID = '" + str(obj_id) + "' "
	)
	can_edit = str(objs_obj.CAN_EDIT)
	can_clone = str(objs_obj.CAN_ADD)
	can_delete = str(objs_obj.CAN_DELETE)
	if ATTRIBUTE_VALUE is None or ATTRIBUTE_VALUE == "" or ATTRIBUTE_VALUE_STR is None or ATTRIBUTE_VALUE_STR == "":
		Trace.Write("empty search")
		if TreeSuperParentParam == "Product Offerings":
			parent_obj = Sql.GetList(
				"SELECT TOP "+str(PerPage)+" CONTRACT_SERVICE_EQUIPMENT_RECORD_ID,EQUIPMENT_ID,EQUIPMENT_DESCRIPTION,SERIAL_NUMBER,GREENBOOK,FABLOCATION_ID from CTCSCO (NOLOCK) where CONTRACT_RECORD_ID = '"
				+ str(ContractRecordId)
				+ "' AND SERVICE_ID = '"
				+ str(TreeParam)
				+ "' ORDER BY "+str(orderby)+" "
			)

			QueryCountObj = Sql.GetFirst(
					"SELECT count(*) as cnt from CTCSCO (NOLOCK) where CONTRACT_RECORD_ID = '"
				+ str(ContractRecordId)
				+ "' AND SERVICE_ID = '"
				+ str(TreeParam)
				+ "' " 
				)
			if QueryCountObj is not None:
				QueryCount = QueryCountObj.cnt


		else:
			Trace.Write("conditional search --->")
			if TreeTopSuperParentParam == "Product Offerings":
				parent_obj = Sql.GetList(
					"SELECT TOP "+str(PerPage)+" CONTRACT_SERVICE_EQUIPMENT_RECORD_ID,EQUIPMENT_ID,EQUIPMENT_DESCRIPTION,SERIAL_NUMBER,GREENBOOK,FABLOCATION_ID from CTCSCO (NOLOCK) where CONTRACT_RECORD_ID = '"
					+ str(ContractRecordId)
					+ "' AND SERVICE_ID = '"
					+ str(TreeParentParam)
					+ "' AND GREENBOOK = '"
					+ str(TreeParam)
					+ "' ORDER BY "+str(orderby)+" "
				)

				QueryCountObj = Sql.GetFirst(
					"SELECT count(*) as cnt from CTCSCO (NOLOCK) where CONTRACT_RECORD_ID = '"
					+ str(ContractRecordId)
					+ "' AND SERVICE_ID = '"
					+ str(TreeParentParam)
					+ "' AND GREENBOOK = '"
					+ str(TreeParam)
					+ "'"
					)
				if QueryCountObj is not None:
					QueryCount = QueryCountObj.cnt
	else:
		Trace.Write("search with condition")
		if TreeSuperParentParam == "Product Offerings":
			parent_obj = Sql.GetList(
				"SELECT Top "+str(PerPage)+"  CONTRACT_SERVICE_EQUIPMENT_RECORD_ID,EQUIPMENT_ID,EQUIPMENT_DESCRIPTION,SERIAL_NUMBER,GREENBOOK,FABLOCATION_ID from CTCSCO (NOLOCK) where "
				+ str(ATTRIBUTE_VALUE_STR)
				+ " 1=1 and CONTRACT_RECORD_ID = '"
				+ str(ContractRecordId)
				+ "'AND SERVICE_ID = '"
				+ str(TreeParam)
				+ "' ORDER BY "+str(orderby)+" "
			)

			QueryCountObj = Sql.GetFirst(
				"SELECT count(*) as cnt from CTCSCO (NOLOCK) where "
				+ str(ATTRIBUTE_VALUE_STR)
				+ " 1=1 and CONTRACT_RECORD_ID = '"
				+ str(ContractRecordId)
				+ "'AND SERVICE_ID = '"
				+ str(TreeParam)
				+ "'"
				)
			if QueryCountObj is not None:
				QueryCount = QueryCountObj.cnt

		else:
			if TreeTopSuperParentParam == "Product Offerings":
				parent_obj = Sql.GetList(
					"SELECT Top "+str(PerPage)+" CONTRACT_SERVICE_EQUIPMENT_RECORD_ID,EQUIPMENT_ID,EQUIPMENT_DESCRIPTION,SERIAL_NUMBER,GREENBOOK,FABLOCATION_ID from CTCSCO (NOLOCK) where "
					+ str(ATTRIBUTE_VALUE_STR)
					+ " 1=1 and CONTRACT_RECORD_ID = '"
					+ str(ContractRecordId)
					+ "'AND SERVICE_ID = '"
					+ str(TreeParentParam)
					+ "' AND GREENBOOK = '"
					+ str(TreeParam)
					+ "' ORDER BY "+str(orderby)+" "
				)
				QueryCountObj = Sql.GetFirst(
					"SELECT count(*) as cnt from CTCSCO (NOLOCK) where "
					+ str(ATTRIBUTE_VALUE_STR)
					+ " 1=1 and CONTRACT_RECORD_ID = '"
					+ str(ContractRecordId)
					+ "'AND SERVICE_ID = '"
					+ str(TreeParentParam)
					+ "' AND GREENBOOK = '"
					+ str(TreeParam)
					+ "'"
				)
				if QueryCountObj is not None:
					QueryCount = QueryCountObj.cnt

	for par in parent_obj:
		data_dict = {}
		data_id = str(par.CONTRACT_SERVICE_EQUIPMENT_RECORD_ID) 

		Action_str = (
			'<div class="btn-group dropdown"><div class="dropdown" id="ctr_drop"><i data-toggle="dropdown" id="dropdownMenuButton" class="fa fa-sort-desc dropdown-toggle" aria-expanded="false"></i><ul class="dropdown-menu left" aria-labelledby="dropdownMenuButton"><li><a class="dropdown-item cur_sty" href="#" id="'
			+ str(data_id)
			+ '" onclick="Commonteree_view_RL(this)">VIEW</a></li>'
		)
		if can_edit.upper() == "TRUE":
			Action_str += (
				'<li style="display:none" ><a class="dropdown-item cur_sty" href="#" id="'
				+ str(data_id)
				+ '" onclick="Move_to_parent_obj_edit(this)">EDIT</a></li>'
			)
		if can_delete.upper() == "TRUE":
			Action_str += '<li><a class="dropdown-item" data-target="#cont_viewModal_Material_Delete" data-toggle="modal" onclick="Material_delete_obj(this)" href="#">DELETE</a></li>'
		if can_clone.upper() == "TRUE":
			Action_str += '<li><a class="dropdown-item" data-target="#" data-toggle="modal" onclick="Material_clone_obj(this)" href="#">CLONE</a></li>'

		Action_str += "</ul></div></div>"
		data_dict = {}
		data_dict["ids"] = str(data_id)
		data_dict["ACTIONS"] = str(Action_str)
		data_dict["CONTRACT_SERVICE_EQUIPMENT_RECORD_ID"] = CPQID.KeyCPQId.GetCPQId(
			"CTCSCO", str(par.CONTRACT_SERVICE_EQUIPMENT_RECORD_ID)
		)
		data_dict["EQUIPMENT_ID"] = str(par.EQUIPMENT_ID)
		data_dict["EQUIPMENT_DESCRIPTION"] = str(par.EQUIPMENT_DESCRIPTION)
		data_dict["FABLOCATION_ID"] = str(par.FABLOCATION_ID)
		data_dict["GREENBOOK"] = str(par.GREENBOOK)
		data_dict["SERIAL_NUMBER"] = str(par.SERIAL_NUMBER)
		data_list.append(data_dict)
		"""page = ""
		if QueryCount < int(PerPage):
			page = str(Page_start) + " - " + str(QueryCount)
		else:
			page = str(Page_start) + " - " + str(Page_End)
		Test = (
			'<div class="col-md-12 brdr listContStyle pad2height30" ><div class="col-md-4 pager-numberofitem clear-padding"><span class="pager-number-of-items-item noofitem" id="NumberofItem" >' + str(page) +' of </span><span class="pager-number-of-items-item fltltpad2mrg0" id="totalItemCount" >'
			+ str(QueryCount)
			+ '</span><div class="clear-padding fltltmrgtp3" ><div  class="pull-right vertmidtxtrht"><select onchange="PageFunctestChild(this,\'Quotes\')" id="PageCountValue"  class="form-control wid65vermiddisinbmarl5"><option value="10" selected>10</option><option value="20">20</option><option value="50">50</option><option value="100">100</option><option value="200">200</option></select> </div></div></div><div class="col-xs-8 col-md-4  clear-padding disinpad10txtcen"  data-bind="visible: totalItemCount"><div class="clear-padding col-xs-12 col-sm-6 col-md-12 bor0" ><ul class="pagination pagination"><li class="disabled"><a href="#" onclick="FirstPageLoad_paginationChild(\'Quotes\')"><i class="fa fa-caret-left font14whtbld" ></i><i class="fa fa-caret-left font14" ></i></a></li><li class="disabled"><a href="#" onclick="Previous12334Child(\'Quotes\')"><i class="fa fa-caret-left font14" ></i>PREVIOUS</a></li><li class="disabled"><a href="#" class="disabledPage" onclick="Next12334Child(\'Quotes\',\'\',\'table_covered_obj_parent\')">NEXT<i class="fa fa-caret-right font14" ></i></a></li><li class="disabled"><a href="#" onclick="LastPageLoad_paginationChild(\'Quotes\')" class="disabledPage"><i class="fa fa-caret-right font14"></i><i class="fa fa-caret-right font14whtbld"></i></a></li></ul></div> </div> <div class="col-md-4 pr_page_pad"> <span id="page_count" class="currentPage page_right_content">1</span><span class="page_right_content pad_rt_2">Page </span></div></div>'
		)"""

	page = ""
	if QueryCount < int(PerPage):
		page = str(Page_start) + " - " + str(QueryCount) + " of "
	else:
		page = str(Page_start) + " - " + str(Page_End)+ " of "
	#return data_list, QueryCount, page
	# Trace.Write("GetContractCovObjMasterFilter data_list --->"+str(data_list))
	# Trace.Write("GetContractCovObjMasterFilter QueryCount ---->"+str(QueryCount))
	# Trace.Write("GetContractCovObjMasterFilter page --->"+str(page))
	return data_list, QueryCount, page

def GetCovObjChildFilter(ATTRIBUTE_NAME, ATTRIBUTE_VALUE,RECID,PerPage,PageInform):

	if str(PerPage) == "" and str(PageInform) == "":
		Page_start = 1
		Page_End = 10
		PerPage = 10
		PageInform = "1___10___10"
	else:
		Page_start = int(PageInform.split("___")[0])
		Page_End = int(PageInform.split("___")[1])
		PerPage = PerPage
	QueryCount = ""
	TreeParam = Product.GetGlobal("TreeParam")
	TreeParentParam = Product.GetGlobal("TreeParentLevel0")
	TreeSuperParentParam = Product.GetGlobal("TreeParentLevel1")
	TreeTopSuperParentParam = Product.GetGlobal("TreeParentLevel2")

	# FablocationId = Product.GetGlobal("TreeParam")
	ContractRecordId = Quote.GetGlobal("contract_quote_record_id")
	RevisionRecordId = Quote.GetGlobal("quote_revision_record_id")
	ATTRIBUTE_VALUE_STR = ""
	Dict_formation = dict(zip(ATTRIBUTE_NAME, ATTRIBUTE_VALUE))
	for quer_key, quer_value in enumerate(Dict_formation):
		x_picklistcheckobj = Sql.GetFirst(
			"SELECT PICKLIST FROM SYOBJD (NOLOCK) WHERE OBJECT_NAME ='SAQSCA' AND API_NAME = '" + str(quer_value) + "'"
		)
		x_picklistcheck = str(x_picklistcheckobj.PICKLIST).upper()
		if Dict_formation.get(quer_value) != "":
			quer_values = str(Dict_formation.get(quer_value)).strip()
			if str(quer_values).upper() == "TRUE":
				quer_values = "TRUE"
			elif str(quer_values).upper() == "FALSE":
				quer_values = "FALSE"
			if str(quer_values).find(",") == -1:
				if x_picklistcheck == "TRUE":
					ATTRIBUTE_VALUE_STR += str(quer_value) + " = '" + str(quer_values) + "' and "
				else:
					ATTRIBUTE_VALUE_STR += str(quer_value) + " like '%" + str(quer_values) + "%' and "
			else:
				quer_values = quer_values.split(",")
				quer_values = tuple(list(quer_values))
				ATTRIBUTE_VALUE_STR += str(quer_value) + " in " + str(quer_values) + " and "

	data_list = []
	rec_id = "SYOBJ_00929"
	obj_id = "SYOBJ-00929"
	objh_getid = Sql.GetFirst(
		"SELECT TOP 1  RECORD_ID  FROM SYOBJH (NOLOCK) WHERE SAPCPQ_ATTRIBUTE_NAME='" + str(obj_id) + "'"
	)
	if objh_getid:
		obj_id = objh_getid.RECORD_ID
	objs_obj = Sql.GetFirst(
		"select CAN_ADD,CAN_EDIT,COLUMNS,CAN_DELETE from SYOBJR (NOLOCK) where OBJ_REC_ID = '" + str(obj_id) + "' "
	)
	
	orderby = ""
	if SortColumn != '' and SortColumnOrder !='':
		orderby = SortColumn + " " + SortColumnOrder
	else:
		orderby = "QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID"
	
	
	can_edit = str(objs_obj.CAN_EDIT)
	can_clone = str(objs_obj.CAN_ADD)
	can_delete = str(objs_obj.CAN_DELETE)
	if ATTRIBUTE_VALUE is None or ATTRIBUTE_VALUE == "" or ATTRIBUTE_VALUE_STR is None or ATTRIBUTE_VALUE_STR == "":
		Trace.Write("empty search")
		if TreeSuperParentParam == "Product Offerings":
			parent_obj = Sql.GetList(
				"select top "+str(PerPage)+"  QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID,EQUIPMENT_ID,ASSEMBLY_ID,ASSEMBLY_DESCRIPTION,GOT_CODE, EQUIPMENT_DESCRIPTION, MNT_PLANT_ID,FABLOCATION_ID,WARRANTY_START_DATE,WARRANTY_END_DATE,INCLUDED from SAQSCA (NOLOCK) where EQUIPMENT_ID = '{recid}' and QUOTE_RECORD_ID = '{ContractRecordId}'  and QTEREV_RECORD_ID = '{RevisionRecordId}' and SERVICE_ID = '{treeparam}' ORDER BY {ord_by} ".format(
					ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"), recid=RECID, treeparam=TreeParam,ord_by = orderby
				)
			)
			
			QueryCountObj = Sql.GetFirst(
					"select count(*) as cnt from SAQSCA (NOLOCK) where EQUIPMENT_ID = '{recid}' and QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' and SERVICE_ID = '{treeparam}' ".format(
					ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"), recid=RECID, treeparam=TreeParam))
			if QueryCountObj is not None:
				QueryCount = QueryCountObj.cnt
			
			
			
		else:
			if TreeTopSuperParentParam == "Product Offerings":
				parent_obj = Sql.GetList(
					"select top "+str(PerPage)+"  QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID,EQUIPMENT_ID,ASSEMBLY_ID,ASSEMBLY_DESCRIPTION,GOT_CODE, EQUIPMENT_DESCRIPTION, MNT_PLANT_ID,FABLOCATION_ID,WARRANTY_START_DATE,WARRANTY_END_DATE,INCLUDED from SAQSCA (NOLOCK) where EQUIPMENT_ID = '{recid}' and QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' and SERVICE_ID = '{treeparam}' ORDER BY {ord_by} ".format(
						ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"), recid=RECID, treeparam=TreeParentParam,ord_by = orderby
					)
				)
				
				QueryCountObj = Sql.GetFirst(
						"select count(*) as cnt from SAQSCA (NOLOCK) where EQUIPMENT_ID = '{recid}' and QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' and SERVICE_ID = '{treeparam}' ".format(
						ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"),recid=RECID, treeparam=TreeParentParam))
				if QueryCountObj is not None:
					QueryCount = QueryCountObj.cnt
			
			
			else:
				Trace.Write("5 level empty search --->")
				parent_obj = Sql.GetList(
					"select top "+str(PerPage)+"  QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID,EQUIPMENT_ID,ASSEMBLY_ID,ASSEMBLY_DESCRIPTION,GOT_CODE, EQUIPMENT_DESCRIPTION, MNT_PLANT_ID,FABLOCATION_ID,WARRANTY_START_DATE,WARRANTY_END_DATE,INCLUDED from SAQSCA (NOLOCK) where   QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' and EQUIPMENT_ID = '{recid}' and SERVICE_ID = '{service_id}'and FABLOCATION_ID = '{fablocation_id}' ORDER BY {ord_by} ".format(
						ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),
						RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"),
						recid=RECID,
						service_id=TreeSuperParentParam,
						fablocation_id = TreeParentParam,
						ord_by = orderby
					)
				)
				
				QueryCountObj = Sql.GetFirst(
						"select count(*) as cnt from SAQSCA (NOLOCK) where   QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' and EQUIPMENT_ID = '{recid}' and SERVICE_ID = '{service_id}'and FABLOCATION_ID = '{fablocation_id}'".format(
						ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),
						RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"),
						recid=RECID,
						service_id=TreeSuperParentParam,
						fablocation_id = TreeParentParam,
					))
				if QueryCountObj is not None:
					QueryCount = QueryCountObj.cnt
				
	else:
		Trace.Write("search with condition")
		if TreeSuperParentParam == "Product Offerings":
			parent_obj = Sql.GetList(
				"select top "+str(PerPage)+"  QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID,EQUIPMENT_ID,ASSEMBLY_ID,ASSEMBLY_DESCRIPTION,GOT_CODE, EQUIPMENT_DESCRIPTION, MNT_PLANT_ID,FABLOCATION_ID,WARRANTY_START_DATE,WARRANTY_END_DATE,INCLUDED from SAQSCA (NOLOCK) where  "
				+ str(ATTRIBUTE_VALUE_STR)
				+ " 1=1 and QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}'  and EQUIPMENT_ID = '{recid}' and SERVICE_ID = '{treeparam}' ORDER BY {ord_by} ".format(
					ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"), recid=RECID, treeparam=TreeParam,ord_by = orderby
				)
			)
			
			QueryCountObj = Sql.GetFirst(
					"select count(*) as cnt from SAQSCA (NOLOCK) where  "
				+ str(ATTRIBUTE_VALUE_STR)
				+ " 1=1 and QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' and EQUIPMENT_ID = '{recid}' and SERVICE_ID = '{treeparam}'".format(
					ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"), recid=RECID, treeparam=TreeParam
				))
			if QueryCountObj is not None:
				QueryCount = QueryCountObj.cnt
		else:
			if TreeTopSuperParentParam == "Product Offerings":
				parent_obj = Sql.GetList(
					"select top "+str(PerPage)+"  QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID,EQUIPMENT_ID,ASSEMBLY_ID,ASSEMBLY_DESCRIPTION,GOT_CODE, EQUIPMENT_DESCRIPTION, MNT_PLANT_ID,FABLOCATION_ID,WARRANTY_START_DATE,WARRANTY_END_DATE,INCLUDED from SAQSCA (NOLOCK) where  "
					+ str(ATTRIBUTE_VALUE_STR)
					+ " 1=1 and QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' and EQUIPMENT_ID = '{recid}' and SERVICE_ID = '{treeparam}' ORDER BY {ord_by}".format(
						ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),
						RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"),
						recid=RECID,
						treeparam=TreeParentParam,
						ord_by = orderby
					)
				)
				
				QueryCountObj = Sql.GetFirst(
						"select count(*) as cnt from SAQSCA (NOLOCK) where  "
					+ str(ATTRIBUTE_VALUE_STR)
					+ " 1=1 and QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' and EQUIPMENT_ID = '{recid}' and SERVICE_ID = '{treeparam}'".format(
						ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),
						RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"),
						recid=RECID,
						treeparam=TreeParentParam,
					))
				if QueryCountObj is not None:
					QueryCount = QueryCountObj.cnt
			else:   
				Trace.Write("5 level coditional search --->")
				parent_obj = Sql.GetList(
					"select top "+str(PerPage)+"  QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID,EQUIPMENT_ID,ASSEMBLY_ID,ASSEMBLY_DESCRIPTION,GOT_CODE, EQUIPMENT_DESCRIPTION, MNT_PLANT_ID,FABLOCATION_ID,WARRANTY_START_DATE,WARRANTY_END_DATE,INCLUDED from SAQSCA (NOLOCK) where  "
					+ str(ATTRIBUTE_VALUE_STR)
					+ " 1=1 and QUOTE_RECORD_ID = '{ContractRecordId}' and QTEREV_RECORD_ID = '{RevisionRecordId}' and EQUIPMENT_ID = '{recid}' and SERVICE_ID = '{service_id}'and FABLOCATION_ID = '{fablocation_id}' ORDER BY {ord_by}".format(
						ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),
						RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"),
						recid=RECID,
						service_id=TreeSuperParentParam,
						fablocation_id = TreeParentParam,
						ord_by = orderby
					)
				)   
				
				QueryCountObj = Sql.GetFirst(
						"select count(*) as cnt from SAQSCA (NOLOCK) where  "
					+ str(ATTRIBUTE_VALUE_STR)
					+ " 1=1 and QUOTE_RECORD_ID = '{ContractRecordId}'  and QTEREV_RECORD_ID = '{RevisionRecordId}' and EQUIPMENT_ID = '{recid}' and SERVICE_ID = '{service_id}'and FABLOCATION_ID = '{fablocation_id}'".format(
						ContractRecordId=Quote.GetGlobal("contract_quote_record_id"),
						RevisionRecordId = Quote.GetGlobal("quote_revision_record_id"),
						recid=RECID,
						service_id=TreeSuperParentParam,
						fablocation_id = TreeParentParam,
					))
				if QueryCountObj is not None:
					QueryCount = QueryCountObj.cnt
				
				

	for par in parent_obj:
		data_dict = {}
		data_id = str(par.QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID)

		Action_str = (
			'<div class="btn-group dropdown"><div class="dropdown" id="ctr_drop"><i data-toggle="dropdown" id="dropdownMenuButton" class="fa fa-sort-desc dropdown-toggle" aria-expanded="false"></i><ul class="dropdown-menu left" aria-labelledby="dropdownMenuButton"><li><a class="dropdown-item cur_sty" href="#" id="'
			+ str(data_id)
			+ '" onclick="Commonteree_view_RL(this)">VIEW</a></li>'
		)
		if can_edit.upper() == "TRUE":
			Action_str += (
				'<li style="display:none" ><a class="dropdown-item cur_sty" href="#" id="'
				+ str(data_id)
				+ '" onclick="Move_to_parent_obj_edit(this)">EDIT</a></li>'
			)
		if can_delete.upper() == "TRUE":
			Action_str += '<li><a class="dropdown-item" data-target="#cont_viewModal_Material_Delete" data-toggle="modal" onclick="Material_delete_obj(this)" href="#">DELETE</a></li>'
		if can_clone.upper() == "TRUE":
			Action_str += '<li><a class="dropdown-item" data-target="#" data-toggle="modal" onclick="Material_clone_obj(this)" href="#">CLONE</a></li>'

		Action_str += "</ul></div></div>"
		data_dict = {}
		data_dict["ids"] = str(data_id)
		data_dict["ACTIONS"] = str(Action_str)
		data_dict["QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID"] = CPQID.KeyCPQId.GetCPQId(
			"SAQSCA", str(par.QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID)
		)
		data_dict["EQUIPMENT_ID"] = str(par.EQUIPMENT_ID)
		data_dict["ASSEMBLY_ID"] = str(par.ASSEMBLY_ID)
		data_dict["ASSEMBLY_DESCRIPTION"] = str(par.ASSEMBLY_DESCRIPTION)
		data_dict["EQUIPMENT_DESCRIPTION"] = str(par.EQUIPMENT_DESCRIPTION)
		data_dict["GOT_CODE"] = str(par.GOT_CODE)
		data_dict["MNT_PLANT_ID"] = str(par.MNT_PLANT_ID)
		data_dict["FABLOCATION_ID"] = str(par.FABLOCATION_ID)
		data_dict["WARRANTY_START_DATE"] = str(par.WARRANTY_START_DATE)
		data_dict["WARRANTY_END_DATE"] = str(par.WARRANTY_END_DATE)
		#data_dict["MODULE_ID"] = str(par.MODULE_ID)
		#data_dict["MODULE_NAME"] = str(par.MODULE_NAME)
		data_list.append(data_dict)
	
	
	page = ""
	if QueryCount < int(PerPage):
		page = str(Page_start) + " - " + str(QueryCount) + " of "
	else:
		page = str(Page_start) + " - " + str(Page_End)+ " of "
	#return data_list, QueryCount, page
	# Trace.Write("GetCovObjChildFilter data_list --->"+str(data_list))
	# Trace.Write("GetCovObjChildFilter QueryCount ---->"+str(QueryCount))
	# Trace.Write("GetCovObjChildFilter page --->"+str(page))
	return data_list, QueryCount, page

def ServiceFabDetails():
	try:
		query = Sql.GetFirst("SELECT QUOTE_SERVICE_FAB_LOCATION_RECORD_ID FROM SAQSFB WHERE FABLOCATION_ID = '{}' AND QUOTE_RECORD_ID = '{}'  and QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID = '{}'".format(TreeParam,Quote.GetGlobal("contract_quote_record_id"),Quote.GetGlobal("quote_revision_record_id"),TreeParentParam))

		fab_rec_id = query.QUOTE_SERVICE_FAB_LOCATION_RECORD_ID
	except:
		Trace.Write("Contract Explorer")
		fab_rec_id = ""
	
	return fab_rec_id

# def BundleCalc(REC_ID):
# 	getservice = Sql.GetFirst("SELECT SERVICE_ID FROM SAQITM WHERE QUOTE_ITEM_RECORD_ID = '{}'".format(CPQID.KeyCPQId.GetKEYId('SAQITM', str(REC_ID))))
# 	SERVICE_ID = ""
# 	SERVICE_ID = getservice.SERVICE_ID
# 	try:
# 		query = Sql.GetFirst("SELECT CpqTableEntryId FROM SAQSAO (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}' and QTEREV_RECORD_ID = '{}' ".format(Quote.GetGlobal("contract_quote_record_id"),str(SERVICE_ID.split("-")[0]).strip(),Quote.GetGlobal("quote_revision_record_id")))
# 	except:
# 		Trace.Write("check10")   
# 		query = "" 
# 	if query.CpqTableEntryId is not None:
# 		return "YES"
# 	else:
# 		return "NO"


def GetCommonParentContract(PerPage, PageInform, A_Keys, A_Values):    
	if str(PerPage) == "" and str(PageInform) == "":
		Page_start = 1
		Page_End = 10
		PerPage = 10
		PageInform = "1___10___10"
	else:
		Page_start = int(PageInform.split("___")[0])
		Page_End = int(PageInform.split("___")[1])
		PerPage = PerPage
	
	Quote_Record_id = Quote.GetGlobal("contract_record_id")  
	TreeParam = Product.GetGlobal("TreeParam")
	TreeParentParam = Product.GetGlobal("TreeParentLevel0")
	TreeSuperParentParam = Product.GetGlobal("TreeParentLevel1")
	ContractRecordId = Quote.GetGlobal("contract_record_id")
	FablocationId = Product.GetGlobal("TreeParam")
	Trace.Write("CRID => {}".format(str(Quote_Record_id)))
	Trace.Write("CRID2 => {}".format(str(ContractRecordId)))
	data_list = []
	obj_idval = "SYOBJ-00995_SYOBJ-00995"
	rec_id = "SYOBJ-00995"
	obj_id = "SYOBJ-00995"
	objh_getid = Sql.GetFirst(
		"SELECT TOP 1  RECORD_ID  FROM SYOBJH (NOLOCK) WHERE SAPCPQ_ATTRIBUTE_NAME='" + str(obj_id) + "'"
	)
	if objh_getid:
		obj_id = objh_getid.RECORD_ID
	objs_obj = Sql.GetFirst(
		"select CAN_ADD,CAN_EDIT,COLUMNS,CAN_DELETE from SYOBJR (NOLOCK) where OBJ_REC_ID = '" + str(obj_id) + "' "
	)
	can_edit = str(objs_obj.CAN_EDIT)
	can_add = str(objs_obj.CAN_ADD)
	can_delete = str(objs_obj.CAN_DELETE)
	table_id = "table_common_parent"
	table_header = (
		'<table id="'
		+ str(table_id)
		+ '"  data-pagination="false" data-sortable="true" data-search-on-enter-key="true" data-filter-control="true" data-pagination-loop = "false" data-locale = "en-US" ><thead>'
	)
	Columns = [
		#"PRICING_STATUS",
		"CONTRACT_ITEM_RECORD_ID",
		#"PARQTEITM_LINE",
		"LINE_ITEM_ID",
		"SERVICE_ID",
		"SERVICE_DESCRIPTION",
		"OBJECT_QUANTITY",
		#"DISCOUNT"
		#"TOTAL_COST",        
		#"SRVTAXCLA_DESCRIPTION",
		#"YEAR_1",
		#"YEAR_2",
		#"YEAR_3",
		#"YEAR_4",
		#"YEAR_5",
		#"TAX_PERCENTAGE",
		#"TAX",
		#"EXTENDED_PRICE"
	]
	##Hide the year column based on the contract valid from and valid to code starts..
	Getyear = Sql.GetFirst("select CONTRACT_VALID_FROM,CONTRACT_VALID_TO from CTCNRT where CONTRACT_RECORD_ID = '{Quote_Record_id}'".format(Quote_Record_id = Quote_Record_id))
	if Getyear:
		start_date = datetime(Getyear.CONTRACT_VALID_FROM)
		end_date = datetime(Getyear.CONTRACT_VALID_TO)
		mm = (end_date. year - start_date. year) * 12 + (end_date. month - start_date. month)
		quotient, remainder = divmod(mm, 12)
		getyears = quotient + (1 if remainder > 0 else 0)
		
		'''
		if not getyears:
			getyears = 1
		if getyears == 1:
			rem_list_sp = ["YEAR_2","YEAR_3","YEAR_4","YEAR_5"]
		elif getyears == 2:
			rem_list_sp = ["YEAR_3","YEAR_4","YEAR_5"]
		elif getyears == 3:
			rem_list_sp = ["YEAR_4","YEAR_5"]
		elif getyears == 4:
			rem_list_sp = ["YEAR_5"]
		else:
			Columns
		for ele in rem_list_sp:
			Columns.remove(ele)
		'''
	##Hide the year column based on the contract valid from and valid to code ends..
	
	Objd_Obj = Sql.GetList(
		"select FIELD_LABEL,API_NAME,LOOKUP_OBJECT,LOOKUP_API_NAME,DATA_TYPE from SYOBJD (NOLOCK) where OBJECT_NAME = 'CTCITM'"
	)       
	symb = ''
	cursymbl = ''
	Decimalplace = ''
	attr_list = []
	attrs_datatype_dict = {}
	lookup_disply_list = []
	lookup_str = ""
	if Objd_Obj is not None:
		attr_list = {}
		for attr in Objd_Obj:
			attr_list[str(attr.API_NAME)] = str(attr.FIELD_LABEL)            
			attrs_datatype_dict[str(attr.API_NAME)] = str(attr.DATA_TYPE)            
			if attr.LOOKUP_API_NAME != "" and attr.LOOKUP_API_NAME is not None:
				lookup_disply_list.append(str(attr.API_NAME))
			#To show currency symbol and decimal places for columns in SAQITM quote Items node - start    
			if attr.API_NAME in Columns:                
				cur_api_name_obj = SqlHelper.GetFirst( "select CURRENCY_INDEX from  SYOBJD (nolock) where API_NAME = '{api_name}'  and OBJECT_NAME = 'CTCITM' ".format(api_name = attr.API_NAME) )                
				if str(cur_api_name_obj.CURRENCY_INDEX) =="GLOBAL_CURRENCY":                    
					Globalcurrency=SqlHelper.GetFirst("SELECT CURRENCY_RECORD_ID FROM PRCURR(NOLOCK) WHERE CURRENCY = 'USD' ")
					curr_symbol_obj = SqlHelper.GetFirst( "select SYMBOL,CURRENCY,DISPLAY_DECIMAL_PLACES from PRCURR (nolock) where CURRENCY_RECORD_ID = '"+str(Globalcurrency.CURRENCY_RECORD_ID)+"'" )
					if curr_symbol_obj is not None:
						symb = curr_symbol_obj.CURRENCY 
						decimal_place = curr_symbol_obj.DISPLAY_DECIMAL_PLACES
				elif str(cur_api_name_obj.CURRENCY_INDEX) !="":                    
					curr_symbol_obj = SqlHelper.GetFirst("""SELECT PRCURR.SYMBOL,PRCURR.CURRENCY,PRCURR.DISPLAY_DECIMAL_PLACES FROM CTCITM (NOLOCK) JOIN PRCURR (NOLOCK) ON PRCURR.CURRENCY_RECORD_ID = CTCITM.CONTRACT_CURRENCY_RECORD_ID WHERE CONTRACT_RECORD_ID = '{QuoteRecordId}'  AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID LIKE '%BUNDLE%'""".format(QuoteRecordId = Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id")))
					if curr_symbol_obj is not None:
						cursymbl = curr_symbol_obj.CURRENCY
						decimal_place = curr_symbol_obj.DISPLAY_DECIMAL_PLACES
						
				elif str(cur_api_name_obj.CURRENCY_INDEX) !="":                    
					curr_symbol_obj = SqlHelper.GetFirst("""SELECT PRCURR.SYMBOL,PRCURR.CURRENCY,PRCURR.DISPLAY_DECIMAL_PLACES FROM CTCITM (NOLOCK) JOIN PRCURR (NOLOCK) ON PRCURR.CURRENCY_RECORD_ID = CTCITM.CONTRACT_CURRENCY_RECORD_ID WHERE CONTRACT_RECORD_ID = '{QuoteRecordId}'  AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID LIKE '%BASE%'""".format(QuoteRecordId = Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id")))
					if curr_symbol_obj is not None:
						cursymbl = curr_symbol_obj.CURRENCY
						decimal_place = curr_symbol_obj.DISPLAY_DECIMAL_PLACES
				elif str(cur_api_name_obj.CURRENCY_INDEX) !="":                    
					curr_symbol_obj = SqlHelper.GetFirst("""SELECT PRCURR.SYMBOL,PRCURR.CURRENCY,PRCURR.DISPLAY_DECIMAL_PLACES FROM CTCITM (NOLOCK) JOIN PRCURR (NOLOCK) ON PRCURR.CURRENCY_RECORD_ID = CTCITM.SORGCURRENCY_RECORD_ID WHERE CONTRACT_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID LIKE '%BASE%'""".format(QuoteRecordId = Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id")))
					if curr_symbol_obj is not None:
						cursymbl = curr_symbol_obj.CURRENCY
						decimal_place = curr_symbol_obj.DISPLAY_DECIMAL_PLACES
				elif str(cur_api_name_obj.CURRENCY_INDEX) !="":                    
					curr_symbol_obj = SqlHelper.GetFirst("""SELECT PRCURR.SYMBOL,PRCURR.CURRENCY,PRCURR.DISPLAY_DECIMAL_PLACES FROM CTCITM (NOLOCK) JOIN PRCURR (NOLOCK) ON PRCURR.CURRENCY_RECORD_ID = CTCITM.SORGCURRENCY_RECORD_ID WHERE CONTRACT_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID LIKE '%BUNDLE%'""".format(QuoteRecordId = Quote.GetGlobal("contract_quote_record_id"),RevisionRecordId = Quote.GetGlobal("quote_revision_record_id")))
					if curr_symbol_obj is not None:
						cursymbl = curr_symbol_obj. CURRENCY
						decimal_place = curr_symbol_obj.DISPLAY_DECIMAL_PLACES               
			#To show currency symbol and decimal places for columns in SAQITM quote Items node - end                   
		text_list = [inn.API_NAME for inn in Objd_Obj if inn.DATA_TYPE == "TEXT"]
		checkbox_list = [inn.API_NAME for inn in Objd_Obj if inn.DATA_TYPE == "CHECKBOX"]
		lookup_list = {ins.LOOKUP_API_NAME: ins.API_NAME for ins in Objd_Obj}
	lookup_str = ",".join(list(lookup_disply_list))
	orderby = ""

	if SortColumn != '' and SortColumnOrder !='':
		orderby = SortColumn + " " + SortColumnOrder
	else:
		orderby = "CONTRACT_ITEM_RECORD_ID"
	imgstr = '<img title="Acquired" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Green_Tick.svg>'
	acquiring_img_str = '<img title="Acquiring" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Cloud_Icon.svg>'
	exclamation = '<img title="Approval Required" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/clock_exe.svg>'
	error = '<img title="Error" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/exclamation_icon.svg>'
	partially_priced = '<img title="Partially Priced" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Red1_Circle.svg>'
	assembly_missing = '<img title="Assembly Missing" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Orange1_Circle.svg>'
	CheckBundle = Sql.GetFirst("SELECT CpqTableEntryId FROM SAQSAO (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(Quote.GetGlobal("contract_record_id"),Quote.GetGlobal("quote_revision_record_id")))
	



	if CheckBundle is not None:

		Qstr = (
			"select top "
			+ str(PerPage)
			+ "CASE WHEN PRICING_STATUS = 'ACQUIRED' THEN '"+ imgstr +"' WHEN PRICING_STATUS = 'APPROVAL REQUIRED' THEN '"+ exclamation +"' WHEN PRICING_STATUS = 'ERROR' THEN '"+ error +"' WHEN PRICING_STATUS = 'PARTIALLY PRICED' THEN '"+ partially_priced +"' WHEN PRICING_STATUS = 'ASSEMBLY MISSING' THEN '"+ assembly_missing +"' ELSE '"+ acquiring_img_str +"' END AS PRICING_STATUS,CONTRACT_ITEM_RECORD_ID,SERVICE_ID,SERVICE_DESCRIPTION, LINE_ITEM_ID,OBJECT_QUANTITY,TOTAL_COST,DISCOUNT,SRVTAXCLA_DESCRIPTION,TAX,TAX_PERCENTAGE,EXTENDED_PRICE,YEAR_1,YEAR_2,YEAR_3,YEAR_4,YEAR_5 from ( select  ROW_NUMBER() OVER( ORDER BY CONTRACT_ITEM_RECORD_ID) AS ROW, CONTRACT_ITEM_RECORD_ID,PRICING_STATUS,SERVICE_ID,SERVICE_DESCRIPTION, LINE_ITEM_ID,OBJECT_QUANTITY,TOTAL_COST,DISCOUNT,SRVTAXCLA_DESCRIPTION,TAX,TAX_PERCENTAGE,EXTENDED_PRICE,YEAR_1,YEAR_2,YEAR_3,YEAR_4,YEAR_5  from CTCITM (NOLOCK) where CONTRACT_RECORD_ID = '"
			+ str(ContractRecordId)
			+ "' AND SERVICE_ID NOT LIKE '%ADDON%' AND SERVICE_ID NOT LIKE '%BASE%') m where m.ROW BETWEEN "
			+ str(Page_start)
			+ " and "
			+ str(Page_End)
			)
		QueryCount = ""
		QueryCountObj = Sql.GetFirst(
			"select count(CONTRACT_ITEM_RECORD_ID) as cnt from CTCITM (NOLOCK) where CONTRACT_RECORD_ID = '"
			+ str(ContractRecordId)
			+ "' AND SERVICE_ID NOT LIKE '%ADDON%' AND SERVICE_ID NOT LIKE '%BASE%'"
		)
	else:
		Trace.Write("Common Parent Contract")
		''' Qstr = (
			"select top "
			+ str(PerPage)
			+ "CASE WHEN PRICING_STATUS = 'ACQUIRED' THEN '"+ imgstr +"' WHEN PRICING_STATUS = 'APPROVAL REQUIRED' THEN '"+ exclamation +"' WHEN PRICING_STATUS = 'ERROR' THEN '"+ error +"' WHEN PRICING_STATUS = 'PARTIALLY PRICED' THEN '"+ partially_priced +"' WHEN PRICING_STATUS = 'ASSEMBLY MISSING' THEN '"+ assembly_missing +"' ELSE '"+ acquiring_img_str +"' END AS PRICING_STATUS,CONTRACT_ITEM_RECORD_ID,SERVICE_ID,SERVICE_DESCRIPTION, LINE_ITEM_ID,OBJECT_QUANTITY,TOTAL_COST,DISCOUNT,SRVTAXCLA_DESCRIPTION,TAX,TAX_PERCENTAGE,EXTENDED_PRICE,YEAR_1,YEAR_2,YEAR_3,YEAR_4,YEAR_5 from ( select  ROW_NUMBER() OVER( ORDER BY CONTRACT_ITEM_RECORD_ID) AS ROW, CONTRACT_ITEM_RECORD_ID,PRICING_STATUS,SERVICE_ID,SERVICE_DESCRIPTION, LINE_ITEM_ID,OBJECT_QUANTITY,TOTAL_COST,DISCOUNT,SRVTAXCLA_DESCRIPTION,TAX,TAX_PERCENTAGE,EXTENDED_PRICE,YEAR_1,YEAR_2,YEAR_3,YEAR_4,YEAR_5  from CTCITM (NOLOCK) where CONTRACT_RECORD_ID = '"
			+ str(ContractRecordId)
			+ "' AND SERVICE_ID NOT LIKE '%ADDON%' AND SERVICE_DESCRIPTION IS NOT NULL AND SERVICE_DESCRIPTION != '') m where m.ROW BETWEEN "
			+ str(Page_start)
			+ " and "
			+ str(Page_End)
		)
		'''
		Qstr = (
			"SELECT TOP 10 CONTRACT_ITEM_RECORD_ID,SERVICE_ID,SERVICE_DESCRIPTION, LINE_ITEM_ID,OBJECT_QUANTITY from ( select  ROW_NUMBER() OVER( ORDER BY CONTRACT_ITEM_RECORD_ID) AS ROW, CONTRACT_ITEM_RECORD_ID,SERVICE_ID,SERVICE_DESCRIPTION, LINE_ITEM_ID,OBJECT_QUANTITY from CTCITM (NOLOCK) where CONTRACT_RECORD_ID ='" 
			+ str(ContractRecordId) 
			+ "' AND SERVICE_ID NOT LIKE '%ADDON%' AND SERVICE_DESCRIPTION IS NOT NULL AND SERVICE_DESCRIPTION != '') m where m.ROW BETWEEN "
			+ str(Page_start)
			+ " and "
			+ str(Page_End)
		)
		QueryCount = ""
		QueryCountObj = Sql.GetFirst(
			"select count(CONTRACT_ITEM_RECORD_ID) as cnt from CTCITM (NOLOCK) where CONTRACT_RECORD_ID = '"
			+ str(ContractRecordId)
			+ "' AND SERVICE_ID NOT LIKE '%ADDON%' AND SERVICE_DESCRIPTION IS NOT NULL AND SERVICE_DESCRIPTION != ''"
		)
	
	if QueryCountObj is not None:
		QueryCount = QueryCountObj.cnt
		#Trace.Write("count---->" + str(QueryCount))
	parent_obj = Sql.GetList(Qstr)
	for par in parent_obj:
		data_id = str(par.CONTRACT_ITEM_RECORD_ID)        
		Action_str = (
			'<div class="btn-group dropdown"><div class="dropdown" id="ctr_drop"><i data-toggle="dropdown" id="dropdownMenuButton" class="fa fa-sort-desc dropdown-toggle" aria-expanded="false"></i><ul class="dropdown-menu left" aria-labelledby="dropdownMenuButton"><li><a class="dropdown-item cur_sty" href="#" id="'
			+ str(data_id)
			+ '" onclick="Commonteree_view_RL(this)">VIEW</a></li>'
			'<li><a class="dropdown-item" id="deletebtn" data-target="#cont_CommonModalDelete" data-toggle="modal" style="display:none" onclick="CommonDelete(this, \'SAQFEA#'+ data_id +'\', \'WARNING\')" href="#">DELETE</a></li>'
		)
		if can_edit.upper() == "TRUE":
			Action_str += (
				'<li style="display:none" ><a class="dropdown-item cur_sty" href="#" id="'
				+ str(data_id)
				+ '" onclick="Move_to_parent_obj_edit(this)">EDIT</a></li>'
			)
		if can_delete.upper() == "TRUE":
			Action_str += '<li><a class="dropdown-item" data-target="#cont_viewModal_Material_Delete" data-toggle="modal" onclick="Material_delete_obj(this)" href="#">DELETE</a></li>'
		if can_add.upper() == "TRUE" and par.MARKET_TYPE == "NON MARKET BASED" and par.MODEL_TYPE != "COST PLUS":
			Action_str += (
				'<li><a class="dropdown-item" id="'
				+ str(data_id)
				+ '" data-target="#" data-toggle="modal" onclick="Pricebook_clone_obj(this)" href="#">CLONE</a></li>'
			)
		Action_str += "</ul></div></div>"
		'''
		decimal_format = "{:,." + str(decimal_place) + "f}"                                
		total_cost = str(decimal_format.format(round(float(par.TOTAL_COST), int(decimal_place)))) if str(par.TOTAL_COST) else ''
		object_quantity = str(decimal_format.format(round(float(par.OBJECT_QUANTITY), int(decimal_place)))) if str(par.OBJECT_QUANTITY) else ''
		extended_price = str(decimal_format.format(round(float(par.EXTENDED_PRICE), int(decimal_place)))) if str(par.EXTENDED_PRICE) else ''
		tax_perc = str(decimal_format.format(round(float(par.TAX_PERCENTAGE), int(decimal_place)))) if str(par.TAX_PERCENTAGE) else ''
		tax = str(decimal_format.format(round(float(par.TAX), int(decimal_place)))) if str(par.TAX) else ''
		#discount = str(decimal_format.format(round(float(par.DISCOUNT), int(decimal_place)))) if str(par.DISCOUNT) else ''
		year_1 = str(decimal_format.format(round(float(par.YEAR_1), int(decimal_place)))) if str(par.YEAR_1) else ''
		year_2 = str(decimal_format.format(round(float(par.YEAR_2), int(decimal_place)))) if str(par.YEAR_2) else ''
		year_3 = str(decimal_format.format(round(float(par.YEAR_3), int(decimal_place)))) if str(par.YEAR_3) else ''
		year_4 = str(decimal_format.format(round(float(par.YEAR_4), int(decimal_place)))) if str(par.YEAR_4) else ''
		year_5 = str(decimal_format.format(round(float(par.YEAR_5), int(decimal_place)))) if str(par.YEAR_5) else ''
		# Data formation in dictonary format.
		# Status - Quote Item - Start
		'''
		icon = ''
		if 'BUNDLE' in str(par.SERVICE_ID):            
			child_items_obj = Sql.GetList("SELECT SERVICE_ID, PRICING_STATUS, CONTRACT_ITEM_RECORD_ID FROM CTCITM (NOLOCK) WHERE CONTRACT_RECORD_ID = '{}' AND PARQTEITM_LINE = '{}'".format(ContractRecordId, par.LINE_ITEM_ID))
			status_list = []
			if child_items_obj:                
				for child_item_obj in child_items_obj:
					if 'BASE' in child_item_obj.SERVICE_ID:
						line_items_status_list = []
						status = 'APPROVAL REQUIRED'
						item_lines_obj = Sql.GetList("SELECT DISTINCT PRICING_STATUS FROM CTCICO (NOLOCK) WHERE CNTITM_RECORD_ID = '{}'".format(child_item_obj.CONTRACT_ITEM_RECORD_ID))
						if item_lines_obj:
							line_items_status_list = [item_line_obj.PRICING_STATUS for item_line_obj in item_lines_obj]

							if "ACQUIRED" in line_items_status_list and ('ACQUIRING' not in line_items_status_list and 'APPROVAL REQUIRED' not in line_items_status_list and 'ERROR' not in line_items_status_list):
								status = 'ACQUIRED'
							elif "ERROR" in line_items_status_list and ('ACQUIRED' not in line_items_status_list and 'APPROVAL REQUIRED' not in line_items_status_list and 'ACQUIRING' not in line_items_status_list):
								status = 'ERROR'
							elif "APPROVAL REQUIRED" in line_items_status_list and ('ACQUIRED' not in line_items_status_list and 'ERROR' not in line_items_status_list and 'ACQUIRING' not in line_items_status_list):
								status = 'APPROVAL REQUIRED'
							elif "ACQUIRING" in line_items_status_list and 'ACQUIRED' not in line_items_status_list and 'ERROR' not in line_items_status_list and 'APPROVAL REQUIRED' not in line_items_status_list:
								status = 'ACQUIRING'
							elif ("ACQUIRED" in line_items_status_list and "ERROR" in line_items_status_list) and ('ACQUIRING' not in line_items_status_list and 'APPROVAL REQUIRED' not in line_items_status_list):
								status = 'ERROR'
							elif ("ACQUIRED" in line_items_status_list and "ACQUIRING" in line_items_status_list) and ('ERROR' not in line_items_status_list and 'APPROVAL REQUIRED' not in line_items_status_list):
								status = 'ACQUIRING'
							elif ("ACQUIRED" in line_items_status_list and "APPROVAL REQUIRED" in line_items_status_list) and ('ERROR' not in line_items_status_list and 'ACQUIRING' not in line_items_status_list):
								status = 'APPROVAL REQUIRED'
							elif ("ACQUIRED" in line_items_status_list and 'ERROR' in line_items_status_list and 'APPROVAL REQUIRED' in line_items_status_list) and "ACQUIRING" not in line_items_status_list :
								status = 'ERROR'
							elif ("ACQUIRING" in line_items_status_list and 'APPROVAL REQUIRED' in line_items_status_list) and ('ACQUIRED' not in line_items_status_list and "ERROR" not in line_items_status_list) :
								status = 'APPROVAL REQUIRED'
						status_list.append(status)
					else:                        
						status_list.append(child_item_obj.PRICING_STATUS) 
			
			if 'ACQUIRING' in status_list:
				icon = '<img title="Acquiring" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Cloud_Icon.svg>'
				status_update=SqlHelper.GetFirst("sp_executesql @statement = N'UPDATE CTCITM SET PRICING_STATUS=''ACQUIRING'' WHERE CONTRACT_RECORD_ID =''"+str(Quote.GetGlobal("contract_record_id"))+"'' AND SERVICE_ID LIKE ''%BUNDLE%'' '")
			elif 'ERROR' in status_list:
				icon = '<img title="Error" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/exclamation_icon.svg>'
				status_update=SqlHelper.GetFirst("sp_executesql @statement = N'UPDATE CTCITM SET PRICING_STATUS=''ERROR'' WHERE CONTRACT_RECORD_ID =''"+str(Quote.GetGlobal("contract_record_id"))+"'' AND SERVICE_ID LIKE ''%BUNDLE%'' '")
			elif 'APPROVAL REQUIRED' in status_list:
				icon = '<img title="Approval Required" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/clock_exe.svg>'
				status_update=SqlHelper.GetFirst("sp_executesql @statement = N'UPDATE CTCITM SET PRICING_STATUS=''APPROVAL REQUIRED'' WHERE CONTRACT_RECORD_ID =''"+str(Quote.GetGlobal("contract_record_id"))+"'' AND SERVICE_ID LIKE ''%BUNDLE%'' '")
			elif 'ACQUIRED' in status_list:
				icon = '<img title="Acquired" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Green_Tick.svg>'
				status_update=SqlHelper.GetFirst("sp_executesql @statement = N'UPDATE CTCITM SET PRICING_STATUS=''ACQUIRED'' WHERE CONTRACT_RECORD_ID =''"+str(Quote.GetGlobal("contract_record_id"))+"'' AND SERVICE_ID LIKE ''%BUNDLE%'' '")
		else:
			GetQuoteType = SqlHelper.GetFirst("SELECT CONTRACT_TYPE FROM CTCNRT WHERE CONTRACT_RECORD_ID = '{}'".format(Quote.GetGlobal("contract_record_id")))
			if 'SPARE' not in GetQuoteType.CONTRACT_TYPE:
				Trace.Write("CONTRACTYPE => {}".format(str( GetQuoteType.CONTRACT_TYPE)))
				'''
				line_items_status_list = []
				icon = '<img title="Error" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/exclamation_icon.svg>'
				item_lines_obj = Sql.GetList("SELECT DISTINCT PRICING_STATUS FROM CTCICO (NOLOCK) WHERE CNTITM_RECORD_ID = '{}'".format(data_id))
				if item_lines_obj:
					line_items_status_list = [item_line_obj.PRICING_STATUS for item_line_obj in item_lines_obj]

					if "ACQUIRED" in line_items_status_list and ('ACQUIRING' not in line_items_status_list and 'APPROVAL REQUIRED' not in line_items_status_list and 'ERROR' not in line_items_status_list):
						icon = '<img title="Acquired" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Green_Tick.svg>'
						status_update=SqlHelper.GetFirst("sp_executesql @statement = N'UPDATE CTCITM SET PRICING_STATUS=''ACQUIRED'' WHERE CONTRACT_RECORD_ID =''"+str(Quote.GetGlobal("contract_record_id"))+"'' AND SERVICE_ID LIKE ''%BASE%'' '")

					elif "ERROR" in line_items_status_list and ('ACQUIRED' not in line_items_status_list and 'APPROVAL REQUIRED' not in line_items_status_list and 'ACQUIRING' not in line_items_status_list):
						icon = '<img title="Error" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/exclamation_icon.svg>'
						status_update=SqlHelper.GetFirst("sp_executesql @statement = N'UPDATE CTCITM SET PRICING_STATUS=''ERROR'' WHERE CONTRACT_RECORD_ID =''"+str(Quote.GetGlobal("contract_record_id"))+"'' AND SERVICE_ID LIKE ''%BASE%'' '")

					elif "APPROVAL REQUIRED" in line_items_status_list and ('ACQUIRED' not in line_items_status_list and 'ERROR' not in line_items_status_list and 'ACQUIRING' not in line_items_status_list):
						icon = '<img title="Approval Required" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/clock_exe.svg>'
						status_update=SqlHelper.GetFirst("sp_executesql @statement = N'UPDATE CTCITM SET PRICING_STATUS=''APPROVAL REQUIRED'' WHERE CONTRACT_RECORD_ID =''"+str(Quote.GetGlobal("contract_record_id"))+"'' AND SERVICE_ID LIKE ''%BASE%'' '")

					elif "ACQUIRING" in line_items_status_list and 'ACQUIRED' not in line_items_status_list and 'ERROR' not in line_items_status_list and 'APPROVAL REQUIRED' not in line_items_status_list:
						icon = '<img title="Acquiring" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Cloud_Icon.svg>'
						status_update=SqlHelper.GetFirst("sp_executesql @statement = N'UPDATE CTCITM SET PRICING_STATUS=''ACQUIRING'' WHERE CONTRACT_RECORD_ID =''"+str(Quote.GetGlobal("contract_record_id"))+"'' AND SERVICE_ID LIKE ''%BASE%'' '")

					elif ("ACQUIRED" in line_items_status_list and "ERROR" in line_items_status_list) and ('ACQUIRING' not in line_items_status_list and 'APPROVAL REQUIRED' not in line_items_status_list):
						icon = '<img title="Error" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/exclamation_icon.svg>'
						status_update=SqlHelper.GetFirst("sp_executesql @statement = N'UPDATE CTCITM SET PRICING_STATUS=''ERROR'' WHERE CONTRACT_RECORD_ID =''"+str(Quote.GetGlobal("contract_record_id"))+"'' AND SERVICE_ID LIKE ''%BASE%'' '")

					elif ("ACQUIRED" in line_items_status_list and "ACQUIRING" in line_items_status_list) and ('ERROR' not in line_items_status_list and 'APPROVAL REQUIRED' not in line_items_status_list):
						icon = '<img title="Acquiring" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Cloud_Icon.svg>'
						status_update=SqlHelper.GetFirst("sp_executesql @statement = N'UPDATE CTCITM SET PRICING_STATUS=''ACQUIRING'' WHERE CONTRACT_RECORD_ID =''"+str(Quote.GetGlobal("contract_record_id"))+"'' AND SERVICE_ID LIKE ''%BASE%'' '")

					elif ("ACQUIRED" in line_items_status_list and "APPROVAL REQUIRED" in line_items_status_list) and ('ERROR' not in line_items_status_list and 'ACQUIRING' not in line_items_status_list):
						icon = '<img title="Approval Required" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/clock_exe.svg>'
						status_update=SqlHelper.GetFirst("sp_executesql @statement = N'UPDATE CTCITM SET PRICING_STATUS=''APPROVAL REQUIRED'' WHERE CONTRACT_RECORD_ID =''"+str(Quote.GetGlobal("contract_record_id"))+"'' AND SERVICE_ID LIKE ''%BASE%'' '")

					elif ("ACQUIRED" in line_items_status_list and 'ERROR' in line_items_status_list and 'APPROVAL REQUIRED' in line_items_status_list) and "ACQUIRING" not in line_items_status_list :
						icon = '<img title="Error" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/exclamation_icon.svg>'
						status_update=SqlHelper.GetFirst("sp_executesql @statement = N'UPDATE CTCITM SET PRICING_STATUS=''ERROR'' WHERE CONTRACT_RECORD_ID =''"+str(Quote.GetGlobal("contract_record_id"))+"'' AND SERVICE_ID LIKE ''%BASE%'' '")

					elif ("ACQUIRING" in line_items_status_list and 'APPROVAL REQUIRED' in line_items_status_list) and ('ACQUIRED' not in line_items_status_list and "ERROR" not in line_items_status_list) :
						icon = '<img title="Acquiring" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/clock_exe.svg>'
						status_update=SqlHelper.GetFirst("sp_executesql @statement = N'UPDATE CTCITM SET PRICING_STATUS=''ACQUIRING'' WHERE CONTRACT_RECORD_ID =''"+str(Quote.GetGlobal("contract_record_id"))+"'' AND SERVICE_ID LIKE ''%BASE%'' '")
			else:
				getStatus = Sql.GetFirst("SELECT PRICING_STATUS FROM CTCITM (NOLOCK) WHERE CONTRACT_RECORD_ID = '{}'".format(ContractRecordId))
				if getStatus.PRICING_STATUS == 'ACQUIRED':
					icon = '<img title="Acquired" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Green_Tick.svg>'
				elif getStatus.PRICING_STATUS == 'ACQUIRING':
					icon = '<img title="Acquiring" src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Cloud_Icon.svg>'
			'''
		# Status - Quote Item - End
		## hyperlink
		data_dict = {}
		data_dict["ids"] = str(data_id)
		data_dict["ACTIONS"] = str(Action_str)
		data_dict["CONTRACT_ITEM_RECORD_ID"] = CPQID.KeyCPQId.GetCPQId(
			"CTCITM", str(par.CONTRACT_ITEM_RECORD_ID)
		)
		data_dict["LINE_ITEM_ID"] = ('<abbr id ="" +  title="' + str(par.LINE_ITEM_ID) + '">' + str(par.LINE_ITEM_ID) + "</abbr>") 
		#data_dict["PRICING_STATUS"] = icon #str(par.PRICING_STATUS)
		SERVICE_ID = str(par.SERVICE_ID).replace("BUNDLE","BASE WITH ADDON") if  "BUNDLE" in str(par.SERVICE_ID) else str(par.SERVICE_ID)
		data_dict["SERVICE_ID"] = ('<abbr id ="" +  title="' + str(SERVICE_ID) + '">' + str(SERVICE_ID) + "</abbr>")
		data_dict["SERVICE_DESCRIPTION"] = ('<abbr id ="" +  title="' + str(par.SERVICE_DESCRIPTION) + '">' + str(par.SERVICE_DESCRIPTION) + "</abbr>")
		'''
		data_dict["DISCOUNT"] = str(discount)
		data_dict["OBJECT_QUANTITY"] = ('<abbr id ="" +  title="' + str(object_quantity) + '">' + str(object_quantity) + "</abbr>")
		
		TOTAL_COST = str(total_cost) +' '+ str(symb) if str(total_cost) else ''
		data_dict["TOTAL_COST"] = ('<abbr id ="" +  title="' + str(TOTAL_COST) + '">' + str(TOTAL_COST) + "</abbr>")
		# 
		data_dict["SRVTAXCLA_DESCRIPTION"] = ('<abbr id ="" +  title="' + str(par.SRVTAXCLA_DESCRIPTION) + '">' + str(par.SRVTAXCLA_DESCRIPTION) + "</abbr>")
		YEAR_1 = str(year_1) +' '+ str(cursymbl) if str(year_1) else '' 
		YEAR_2 = str(year_2) +' '+ str(cursymbl) if str(year_2) else '' 
		YEAR_3 = str(year_3) +' '+ str(cursymbl) if str(year_3) else ''
		YEAR_4 = str(year_4) +' '+ str(cursymbl) if str(year_4) else ''
		YEAR_5 = str(year_5) +' '+ str(cursymbl) if str(year_5) else ''
		TAX = str(tax) +' '+ str(cursymbl) if str(tax) else '' 
		TAX_PERCENTAGE = str(tax_perc) +' '+ '%' if str(tax_perc) else ''
		EXTENDED_PRICE = str(extended_price) +' '+ str(cursymbl) if str(extended_price) else '' 
		data_dict["YEAR_1"]= ('<abbr id ="" +  title="' + str(YEAR_1) + '">' + str(YEAR_1) + "</abbr>")
		data_dict["YEAR_2"] = ('<abbr id ="" +  title="' + str(YEAR_2) + '">' + str(YEAR_2) + "</abbr>")
		data_dict["YEAR_3"] =  ('<abbr id ="" +  title="' + str(YEAR_3) + '">' + str(YEAR_3) + "</abbr>")
		data_dict["YEAR_4"] =  ('<abbr id ="" +  title="' + str(YEAR_4) + '">' + str(YEAR_4) + "</abbr>")
		data_dict["YEAR_5"] =  ('<abbr id ="" +  title="' + str(YEAR_5) + '">' + str(YEAR_5) + "</abbr>")
		data_dict["TAX_PERCENTAGE"] =  ('<abbr id ="" +  title="' + str(TAX_PERCENTAGE) + '">' + str(TAX_PERCENTAGE) + "</abbr>")
		data_dict["TAX"] = ('<abbr id ="" +  title="' + str(TAX) + '">' + str(TAX) + "</abbr>")
		data_dict["EXTENDED_PRICE"] = ('<abbr id ="" +  title="' + str(EXTENDED_PRICE) + '">' + str(EXTENDED_PRICE) + "</abbr>")
		'''
		data_list.append(data_dict)

	hyper_link = ["CONTRACT_ITEM_RECORD_ID"]
	ParentObj = Sql.GetList(
		"select CONTRACT_ITEM_RECORD_ID from CTCITM (NOLOCK) where CONTRACT_RECORD_ID = '{ContractRecordId}'".format(
			ContractRecordId=Quote.GetGlobal("contract_record_id")
		)
	)
	table_header += "<tr>"
	table_header += (
		'<th data-field="ACTIONS"><div class="action_col">ACTIONS</div><button class="searched_button" id="Act_'
		+ str(table_id)
		+ '">Search</button></th>'
	)
	table_header += '<th data-field="SELECT" class="wid45" data-checkbox="true"></th>'
	for key, invs in enumerate(list(Columns)):
		invs = str(invs).strip()
		qstring = attr_list.get(str(invs)) or ""
		if qstring == "":
			qstring = invs.replace("_", " ")
		if checkbox_list is not None and invs in checkbox_list:
			table_header += (
				'<th  data-field="'
				+ str(invs)
				+ '" data-filter-control="input" data-align="center" data-formatter="CheckboxFieldRelatedList" data-sortable="true"><abbr title="'
				+ str(qstring)
				+ '">'
				+ str(qstring)
				+ "</abbr></th>"
			)
		elif hyper_link is not None and invs in hyper_link:            
			table_header += (
				'<th data-field="'
				+ str(invs)
				+ '" data-filter-control="input" data-formatter="CommonParentHyperLink" data-sortable="true"><abbr title="'
				+ str(qstring)
				+ '">'
				+ str(qstring)
				+ "</abbr></th>"
			)
		elif text_list is not None and invs in text_list:
			if invs == "LINE_ITEM_ID":
				table_header += (
					'<th  data-field="'
					+ str(invs)
					+ '" data-filter-control="input" data-align="right" data-sortable="true"><abbr title="'
					+ str(qstring)
					+ '">'
					+ str(qstring)
					+ "</abbr></th>"
				)      
		else:
			table_header += (
				'<th  data-field="'
				+ str(invs)
				+ '" data-filter-control="input" data-sortable="true"><abbr title="'
				+ str(qstring)
				+ '">'
				+ str(qstring)
				+ "</abbr></th>"
			)
	table_header += "</tr>"
	table_header += '</thead><tbody onclick="Table_Onclick_Scroll(this)"></tbody></table>'
	table_ids = "#" + str(table_id)
	filter_control_function = ""
	tbl_id = table_id
	values_list = ""
	for key, invs in enumerate(list(Columns)):
		table_ids = "#" + str(table_id)
		filter_clas = "#" + str(table_id) + " .bootstrap-table-filter-control-" + str(invs)
		values_list += "var " + str(invs) + ' = $("' + str(filter_clas) + '").val(); '
		values_list += "ATTRIBUTE_VALUEList.push(" + str(invs) + "); "
	filter_class = "#Act_" + str(table_id)
	filter_control_function += (
	'$("'
	+ filter_class
	+ '").click( function(){ var table_id = $(this).closest("table").attr("id"); ATTRIBUTE_VALUEList = []; '
	+ str(values_list)
	+ ' var attribute_value = $(this).val(); cpq.server.executeScript("CQNESTGRID", {"TABNAME":"Common Parent", "ACTION":"PRODUCT_ONLOAD_FILTER", "ATTRIBUTE_NAME": '
	+ str(list(Columns))
	+ ', "ATTRIBUTE_VALUE": ATTRIBUTE_VALUEList }, function(dataset) { data2 = dataset[1];  data1 = dataset[0]; data3 = dataset[2]; console.log("len ---->"+data1.length);  try { if(data1.length > 0) { $("#'
	+ str(tbl_id)
	+ '").bootstrapTable("load", data1 );$("#noRecDisp").remove(); if (document.getElementById("'+str(tbl_id) + '___totalItemCount")){document.getElementById("'+str(tbl_id)+ '___totalItemCount").innerHTML = data2;}  if (document.getElementById("'+str(tbl_id) + '___NumberofItem")) {document.getElementById("'+str(tbl_id)+ '___NumberofItem").innerHTML = data3;}} else{ $("#' + str(tbl_id) + '").bootstrapTable("load", data1  );$("#' + str(tbl_id) + '").after("<div id=\'noRecDisp\' class=\'noRecord\'>No Records to Display</div>"); $(".noRecord:not(:first)").remove(); if (document.getElementById("'+str(tbl_id) + '___totalItemCount")){document.getElementById("'+str(tbl_id)+ '___totalItemCount").innerHTML = data2;}  if (document.getElementById("'+str(tbl_id) + '___NumberofItem")) {document.getElementById("'+str(tbl_id)+ '___NumberofItem").innerHTML = data3;} }} catch(err){} }); filter_search_click();$(".JColResizer").mousedown(function(){ $("thead.fullHeadFirst").css("cssText","z-index: 2;border-top: 1px solid rgb(220, 220, 220);top: 154px;border-right: 0px !important;");$("thead.fullHeadSecond").css("display","none"); });$(".JColResizer").mouseup(function(){ var th_width_resize = [];$("#table_common_parent thead.fullHeadFirst tr th").each(function(index){var wid = $(this).css("width"); if(index ==0 || index ==1){th_width_resize.push("60px");}else{th_width_resize.push(wid);}}); $("thead.fullHeadFirst").css("cssText","position: fixed;z-index: 2;border-top: 1px solid rgb(220, 220, 220); top: 154px;border-right: 0px !important;");$("thead.fullHeadSecond").css("display","table-header-group");$("#table_common_parent thead.fullHeadFirst tr th").each(function(index){var num = th_width_resize[index].split("px");var numsp = parseInt(num[0]);numsp = numsp - 1;var make_str =numsp+"px"; var c = "width:"+make_str+";white-space: nowrap;overflow: hidden;text-overflow: ellipsis;";var d = "width:"+make_str+";"; $(this).css("cssText",c);$(this).children("div:first-child").css("cssText",c);$(this).children("div.fht-cell").css("cssText",d);});$("#table_common_parent thead.fullHeadSecond tr th").each(function(index){var num = th_width_resize[index].split("px");var numsp = parseInt(num[0]);numsp = numsp - 1;var make_str =numsp+"px"; var c = "width:"+make_str+";white-space: nowrap;overflow: hidden;text-overflow: ellipsis;";var d = "width:"+make_str+";"; $(this).css("cssText",c);$(this).children("div:first-child").css("cssText",c);$(this).children("div.fht-cell").css("cssText",d);}); });});')

	filter_control_function +=("$('#table_common_parent_RelatedMutipleCheckBoxDrop_0').on('checkChange', function (event){ setTimeout(function () { try{ var GetValInput = $('#dropdownlistContenttable_common_parent_RelatedMutipleCheckBoxDrop_0 span').text(); gevalSplit = GetValInput.split(','); if(gevalSplit[0].indexOf('>') != -1){ var RemoveImg = (GetValInput).split('>'); if(gevalSplit[1] != undefined) imgtext = RemoveImg[1]+','+gevalSplit[1]; else imgtext = RemoveImg[1]; } else if(gevalSplit[1].indexOf('>') != -1){ var RemoveImg = (GetValInput).split('>'); if(gevalSplit[0] != undefined) imgtext = gevalSplit[0]+','+RemoveImg[1]; else imgtext = RemoveImg[1]; } else{ imgtext = GetValInput; } $('#dropdownlistContenttable_common_parent_RelatedMutipleCheckBoxDrop_0 span').text(imgtext); } catch(err){ console.log('wrong---'); } }, 200); });")                                      

	#Trace.Write("666 filter_control_function ---->"+str(filter_control_function))
	# SYOBJR_00009_E5504B40_36E7_4EA6_9774_EA686705A63F
	dbl_clk_function = (
		'$("'
		+ str(table_ids)
		+ '").on("all.bs.table", function (e, name, args) { $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); }); $("'
		+ str(table_ids)
		+ '\ th.bs-checkbox div.th-inner").before("<div style=\'padding:0; border-bottom: 1px solid #dcdcdc;\'>SELECT</div>"); $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); $("'
		+ str(table_ids)
		+ "\").on('sort.bs.table', function (e, name, order) {console.log('wwwwwwwwwwwwxxxxx', localStorage.getItem('sortedTableId')); if (!localStorage.getItem('sortedTableId')){debugger;  console.log('Parent sort.bs.table ====> ', e); currenttab = $(\"ul#carttabs_head .active\").text().trim(); localStorage.setItem('"
		+ str(table_id)
		+ "_SortColumn', name); localStorage.setItem('"
		+ str(table_id)
		+ "_SortColumnOrder', order); localStorage.setItem('sortedTableId',"+str(table_id)+"); console.log("+str(table_id)+"); NestedContainerSorting(name, order, '"
		+ str(table_id)
		+ "'); debugger;}}); "
		)
	NORECORDS = ""
	if len(data_list) == 0:
		NORECORDS = "NORECORDS"

	ObjectName = "CTCITM"
	DropDownList = []
	filter_level_list = []
	filter_clas_name = ""
	cv_list = []
	TableclassName = "form-control" + table_id
	for key, col_name in enumerate(list(Columns)):
		StringValue_list = []
		objss_obj = Sql.GetFirst(
			"SELECT API_NAME, DATA_TYPE, FORMULA_LOGIC, PICKLIST FROM SYOBJD (NOLOCK) WHERE OBJECT_NAME='"
			+ str(ObjectName)
			+ "' and API_NAME = '"
			+ str(col_name)
			+ "'"
		)
		try:
			FORMULA_LOGIC = objss_obj.FORMULA_LOGIC.strip()
			FORMULA_col = FORMULA_LOGIC.split(" ")[1].strip()
			FORMULA_table = FORMULA_LOGIC.split(" ")[3].strip()
			ins_obj = Sql.GetFirst(
				"SELECT API_NAME, DATA_TYPE,PICKLIST FROM SYOBJD (NOLOCK) WHERE OBJECT_NAME='"
				+ str(FORMULA_table)
				+ "' and API_NAME = '"
				+ str(FORMULA_col)
				+ "'"
			)
			if str(objss_obj.PICKLIST).upper() == "TRUE":
				
				filter_level_data = "select"
				filter_clas_name = (
					'<div id = "'
					+ str(table_id)
					+ "_RelatedMutipleCheckBoxDrop_"
					+ str(key)
					+ '" class="form-control bootstrap-table-filter-control-'
					+ str(col_name)
					+ " RelatedMutipleCheckBoxDrop_"
					+ str(key)
					+ ' "></div>'
				)
				filter_level_list.append(filter_level_data)
			else:
				filter_level_data = "input"
				filter_clas_name = (
					'<input type="text" class="width100_vis form-control bootstrap-table-filter-control-'
					+ str(col_name)
					+ '">'
				)
				filter_level_list.append(filter_level_data)
		except:
			Trace.Write("except---->")
			'''
			if str(objss_obj.PICKLIST).upper() == "TRUE":                
				filter_level_data = "select"
				filter_clas_name = (
					'<div id = "'
					+ str(table_id)
					+ "_RelatedMutipleCheckBoxDrop_"
					+ str(key)
					+ '" class="form-control bootstrap-table-filter-control-'
					+ str(col_name)
					+ " RelatedMutipleCheckBoxDrop_"
					+ str(key)
					+ ' "></div>'
				)
				filter_level_list.append(filter_level_data)
			else:
				filter_level_data = "input"
				filter_clas_name = (
					'<input type="text" class="width100_vis form-control bootstrap-table-filter-control-' + str(col_name) + '">'
				)
			filter_level_list.append(filter_level_data)
		cv_list.append(filter_clas_name)
		if filter_level_data == "select":
			try:
				xcd = Sql.GetFirst(
					"SELECT (STUFF((SELECT DISTINCT ', ' + CAST("
					+ str(col_name)
					+ " AS CHAR(100)) FROM "
					+ str(ObjectName)
					+ " WHERE CONTRACT_RECORD_ID = '"+str(Quote.GetGlobal("contract_record_id"))+"' AND SERVICE_ID LIKE '%BUNDLE%' FOR XML PATH('') ), 1, 2, '')  ) AS StringValue"
				)
				if str(xcd.StringValue) == "":
					xcd = Sql.GetFirst(
						"SELECT (STUFF((SELECT DISTINCT ', ' + CAST("
						+ str(col_name)
						+ " AS CHAR(100)) FROM "
						+ str(ObjectName)
						+ " WHERE CONTRACT_RECORD_ID = '"+str(Quote.GetGlobal("contract_record_id"))+"' AND SERVICE_ID LIKE '%BASE%' FOR XML PATH('') ), 1, 2, '')  ) AS StringValue"
					)
			except:
				xcd = Sql.GetFirst(
					"SELECT (STUFF((SELECT DISTINCT ', ' + CAST("
					+ str(col_name)
					+ " AS CHAR(100)) FROM "
					+ str(ObjectName)
					+ " FOR XML PATH('') ), 1, 2, '')  ) AS StringValue"
				)
			if str(xcd.StringValue) is not None and str(xcd.StringValue) != "":
				if str(xcd.StringValue).find(",") != -1:
					StringValue_list = [ins.strip() for ins in str(xcd.StringValue).split(",") if ins.strip() != ""]
				else:
					StringValue_list.append(str(xcd.StringValue))
			else:
				StringValue_list = [""]
			StringValue_lists=[]
			#Trace.Write("DROPDOWN LIST-------@3129----"+str(StringValue_list))
			for string in StringValue_list:
				string = string.strip()
				if string == "ACQUIRED":
					string_value = string.replace("ACQUIRED","<img title='Acquired' src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Green_Tick.svg> ACQUIRED")
				if string == "APPROVAL REQUIRED":
					string_value = string.replace("APPROVAL REQUIRED","<img title='Approval Required' src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/clock_exe.svg> APPROVAL REQUIRED")
				if string == "ACQUIRING":                        
					string_value = string.replace("ACQUIRING","<img title='Acquiring' src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Cloud_Icon.svg> ACQUIRING")
				if string == "ERROR":
					string_value = string.replace("ERROR","<img title='Error' src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/exclamation_icon.svg> ERROR")
					status_update=SqlHelper.GetFirst("sp_executesql @statement = N'UPDATE CTCITM SET PRICING_STATUS=''ERROR'' WHERE CONTRACT_RECORD_ID =''"+str(Quote.GetGlobal("contract_record_id"))+"'' AND SERVICE_ID LIKE ''%BUNDLE%'' '")
				if string == "ASSEMBLY MISSING":
					string_value = string.replace("ASSEMBLY MISSING","<img title='Assembly Missing' src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Orange1_Circle.svg> ASSEMBLY MISSING")
				if string == "PARTIALLY PRICED":
					string_value = string.replace("PARTIALLY PRICED","<img title='Partially Priced' src=/mt/APPLIEDMATERIALS_TST/Additionalfiles/Red1_Circle.svg> PARTIALLY PRICED")
				if string != "ACQUIRED" and string != "APPROVAL REQUIRED" and string != "ERROR" and string != "ASSEMBLY MISSING" and string != "PARTIALLY PRICED" and string != "ACQUIRING":                        
					string_value = string
				StringValue_lists.append(string_value)
			StringValue_lists = list(set(StringValue_lists))
			#Trace.Write("StringValue_lists_CHK"+str(StringValue_lists))
			DropDownList.append(StringValue_lists)
			# DropDownList.append(StringValue_list)
		elif filter_level_data == "checkbox":
			DropDownList.append(["True", "False"])
		else:
			DropDownList.append("")
		
	RelatedDrop_str = (
		"try { if( document.getElementById('"
		+ str(table_id)
		+ "') ) { var listws = document.getElementById('"
		+ str(table_id)
		+ "').getElementsByClassName('filter-control');  for (i = 0; i < listws.length; i++) { document.getElementById('"
		+ str(table_id)
		+ "').getElementsByClassName('filter-control')[i].innerHTML = data6[i];  } for (j = 0; j < listws.length; j++) { if (data7[j] == 'select') { if (data8[j]) { var dataAdapter = new $.jqx.dataAdapter(data8[j]); $('#"
		+ str(table_id)
		+ "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter, dropDownWidth:135, autoDropDownHeight: true }); } } } } }  catch(err) { setTimeout(function() { var listws = document.getElementById('"
		+ str(table_id)
		+ "').getElementsByClassName('filter-control');  for (i = 0; i < listws.length; i++) { document.getElementById('"
		+ str(table_id)
		+ "').getElementsByClassName('filter-control')[i].innerHTML = data6[i];  } for (j = 0; j < listws.length; j++) { if (data7[j] == 'select') { if (data8[j]) { var dataAdapter = new $.jqx.dataAdapter(data8[j]); $('#"
		+ str(table_id)
		+ "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter, dropDownWidth:135, autoDropDownHeight: true }); } } } }, 5000); }"
	)
	'''     
	
	page = ""
	if QueryCount < int(PerPage):
		page = str(Page_start) + " - " + str(QueryCount)
	else:
		page = str(Page_start) + " - " + str(Page_End)
	#Trace.Write("page----->"+str(page))    
	Test = (
		'<div class="col-md-12 brdr listContStyle pad2height30" ><div class="col-md-4 pager-numberofitem clear-padding"><span class="pager-number-of-items-item noofitem" id="'
		+ str(table_id)
		+ '___NumberofItem" >'
		+ str(page)
		+ ' of</span><span class="pager-number-of-items-item fltltpad2mrg0" id="'
		+ str(table_id)
		+ '___totalItemCount" >'
		+ str(QueryCount)
		+ '</span><div class="clear-padding fltltmrgtp3" ><div  class="pull-right vertmidtxtrht"><select onchange="PageFunctestChild(this,\'Quote\',\'\',\'table_common_parent\')" id="'
		+ str(table_id)
		+ '___PageCountValue" class="form-control wid65vermiddisinbmarl5"><option value="10" selected>10</option><option value="20">20</option><option value="50">50</option><option value="100">100</option><option value="200">200</option></select> </div></div></div><div class="col-xs-8 col-md-4  clear-padding disinpad10txtcen"  data-bind="visible: totalItemCount"><div class="clear-padding col-xs-12 col-sm-6 col-md-12 bor0" ><ul class="pagination pagination"><li class="disabled"><a href="#" onclick="FirstPageLoad_paginationChild(\'Quote\',\'\',\'table_common_parent\')"><i class="fa fa-caret-left font14whtbld" ></i><i class="fa fa-caret-left font14" ></i></a></li><li class="disabled"><a href="#" onclick="Previous12334Child(\'Quote\',\'\',\'table_common_parent\')"><i class="fa fa-caret-left font14" ></i>PREVIOUS</a></li><li class="disabled"><a href="#" class="disabledPage" onclick="Next12334Child(\'Quote\',\'\',\'table_common_parent\')">NEXT<i class="fa fa-caret-right font14" ></i></a></li><li class="disabled"><a href="#" onclick="LastPageLoad_paginationChild(\'Quote\',\'\',\'table_common_parent\')" class="disabledPage"><i class="fa fa-caret-right font14"></i><i class="fa fa-caret-right font14whtbld"></i></a></li></ul></div> </div> <div class="col-md-4 pr_page_pad"> <span id="'
		+ str(table_id)
		+ '___page_count" class="currentPage page_right_content">1</span><span class="page_right_content pad_rt_2">Page </span></div></div>'
	)
	#Log.Info("Equipment Grid table_header--->"+str(table_header)+"Equipment Grid data_list--->"+str(data_list))
	if QueryCount < int(PerPage):
		PerPage = str(QueryCount)
	else:
		PerPage = str(PerPage)   
	if Page_End > QueryCount:
		Page_End = QueryCount
	else:
		Page_End = Page_End
	Trace.Write("Page_End----->"+str(Page_End))    
	Action_Str = ""
	#Action_Str = "1 - "
	Action_Str += str(Page_start)+" - "
	Action_Str += str(Page_End)
	Action_Str += " of"
	Trace.Write("Action_Str--->"+str(Action_Str))
	RelatedDrop_str=''
	return (
		table_header,
		data_list,
		table_id,
		filter_control_function,
		NORECORDS,
		dbl_clk_function,
		cv_list,
		filter_level_list,
		DropDownList,
		RelatedDrop_str,
		Test,
		Action_Str,
		QueryCount,
		page
	)



def GetSendingEquipmentFilter(ATTRIBUTE_NAME, ATTRIBUTE_VALUE,PerPage,PageInform):
	
	if str(PerPage) == "" and str(PageInform) == "":
		Page_start = 1
		Page_End = 10
		PerPage = 10
		PageInform = "1___10___10"
	else:
		Page_start = int(PageInform.split("___")[0])
		Page_End = int(PageInform.split("___")[1])
		PerPage = PerPage
	QueryCount = ""
	TreeParam = Product.GetGlobal("TreeParam")
	TreeParentParam = Product.GetGlobal("TreeParentLevel0")
	TreeSuperParentParam = Product.GetGlobal("TreeParentLevel1")
	FablocationId = Product.GetGlobal("TreeParam")
	ContractRecordId = Quote.GetGlobal("contract_quote_record_id")
	RevisionRecordId = Quote.GetGlobal("quote_revision_record_id")
	ATTRIBUTE_VALUE_STR = ""
	Dict_formation = dict(zip(ATTRIBUTE_NAME, ATTRIBUTE_VALUE))
	for quer_key, quer_value in enumerate(Dict_formation):
		x_picklistcheckobj = Sql.GetFirst(
			"SELECT PICKLIST FROM SYOBJD (NOLOCK) WHERE OBJECT_NAME ='SAQSSE' AND API_NAME = '" + str(quer_value) + "'"
		)
		x_picklistcheck = str(x_picklistcheckobj.PICKLIST).upper()
		if Dict_formation.get(quer_value) != "":
			quer_values = str(Dict_formation.get(quer_value)).strip()
			if str(quer_values).upper() == "TRUE":
				quer_values = "TRUE"
			elif str(quer_values).upper() == "FALSE":
				quer_values = "FALSE"
			if str(quer_values).find(",") == -1:
				if x_picklistcheck == "TRUE":
					ATTRIBUTE_VALUE_STR += str(quer_value) + " = '" + str(quer_values) + "' and "
				else:
					ATTRIBUTE_VALUE_STR += str(quer_value) + " like '%" + str(quer_values) + "%' and "
			else:
				quer_values = quer_values.split(",")
				quer_values = tuple(list(quer_values))
				ATTRIBUTE_VALUE_STR += str(quer_value) + " in " + str(quer_values) + " and "
			if str(quer_value) == 'QUOTE_SERVICE_SENDING_FAB_LOC_EQUIP_ID':                
				if str(str(quer_values)).find("-") == -1:                            
					ATTRIBUTE_VALUE_STR = (" CpqTableEntryId = '"+ str(quer_values)+ "' and ")                            
				else:
					xa_str = str(quer_values).split("-")[1]                            
					ATTRIBUTE_VALUE_STR = (" CpqTableEntryId = '"+ str(xa_str)+ "' and ")    

	data_list = []
	rec_id = "SYOBJ_003012"
	obj_id = "SYOBJ-003012"
	objh_getid = Sql.GetFirst(
		"SELECT TOP 1  RECORD_ID  FROM SYOBJH (NOLOCK) WHERE SAPCPQ_ATTRIBUTE_NAME='" + str(obj_id) + "'"
	)
	if objh_getid:
		obj_id = objh_getid.RECORD_ID
	objs_obj = Sql.GetFirst(
		"select CAN_ADD,CAN_EDIT,COLUMNS,CAN_DELETE from SYOBJR (NOLOCK) where OBJ_REC_ID = '" + str(obj_id) + "' "
	)
	can_edit = str(objs_obj.CAN_EDIT)
	can_clone = str(objs_obj.CAN_ADD)
	can_delete = str(objs_obj.CAN_DELETE)

	emptysearch_flag = 0
	conditionsearch_falg = 0

	orderby = ""
	if SortColumn != '' and SortColumnOrder !='':
		orderby = SortColumn + " " + SortColumnOrder
	else:
		orderby = "QUOTE_SERVICE_SENDING_FAB_LOC_EQUIP_ID"
	if ATTRIBUTE_VALUE is None or ATTRIBUTE_VALUE == "" or ATTRIBUTE_VALUE_STR is None or ATTRIBUTE_VALUE_STR == "":
		#Trace.Write("Empty search ")
		emptysearch_flag = 1           
			
		if TreeParentParam == 'Sending Equipment' or TreeParentParam == 'Receiving equipment':
			parent_obj = Sql.GetList(
			"select top "+str(PerPage)+" QUOTE_SERVICE_SENDING_FAB_LOC_EQUIP_ID,SALESORG_ID,EQUIPMENTCATEGORY_ID,SND_EQUIPMENT_ID,MNT_PLANT_ID,GREENBOOK,QUOTE_NAME,SALESORG_NAME,SND_EQUIPMENT_DESCRIPTION,EQUIPMENT_STATUS,PLATFORM,SNDFBL_ID,QUOTE_ID,SNDFBL_NAME from SAQSSE (NOLOCK) where QUOTE_RECORD_ID = '"
			+ str(ContractRecordId)
			+ "' and QTEREV_RECORD_ID = '"
			+ str(RevisionRecordId)
			+ "' and SNDFBL_ID = '"
			+ str(TreeParam)
			+ "' ORDER BY "
			+ str(orderby)
			)
			Count = Sql.GetFirst("select count(CpqTableEntryId) as cnt from SAQSSE (NOLOCK) where QUOTE_RECORD_ID = '"+ str(ContractRecordId)+ "' and QTEREV_RECORD_ID = '"+ str(RevisionRecordId)+ "' and SNDFBL_ID = '" + str(TreeParam) + "'")
			if Count:
				QueryCount = Count.cnt
		elif TreeParam == 'Sending Equipment' or TreeParam == 'Receiving equipment':
			parent_obj = Sql.GetList(
				"select top "+str(PerPage)+" QUOTE_SERVICE_SENDING_FAB_LOC_EQUIP_ID,SALESORG_ID,EQUIPMENTCATEGORY_ID,SND_EQUIPMENT_ID,MNT_PLANT_ID,GREENBOOK,QUOTE_NAME,SALESORG_NAME,SND_EQUIPMENT_DESCRIPTION,EQUIPMENT_STATUS,PLATFORM,SNDFBL_ID,QUOTE_ID,SNDFBL_NAME from SAQSSE (NOLOCK) where QUOTE_RECORD_ID = '"
				+ str(ContractRecordId)
				+ "' and QTEREV_RECORD_ID = '"
				+ str(RevisionRecordId)
				+ "' and SERVICE_ID = '"
				+ str(TreeParentParam)
				+ "' ORDER BY "
				+ str(orderby)
			)
			Count = Sql.GetFirst("select count(CpqTableEntryId) as cnt from SAQSSE (NOLOCK) where QUOTE_RECORD_ID = '"+ str(ContractRecordId)+ "'and SERVICE_ID = '" + str(TreeParentParam) + "'  and QTEREV_RECORD_ID = '"+ str(RevisionRecordId)+ "' ")
			if Count:
				QueryCount = Count.cnt
		elif TreeParentParam == "Complementary Products":
			parent_obj = Sql.GetList(
				"select top "+str(PerPage)+" QUOTE_SERVICE_SENDING_FAB_LOC_EQUIP_ID,SALESORG_ID,EQUIPMENTCATEGORY_ID,SND_EQUIPMENT_ID,MNT_PLANT_ID,GREENBOOK,QUOTE_NAME,SALESORG_NAME,SND_EQUIPMENT_DESCRIPTION,EQUIPMENT_STATUS,PLATFORM,SNDFBL_ID,QUOTE_ID,SNDFBL_NAME from SAQSSE (NOLOCK) where QUOTE_RECORD_ID = '"
				+ str(ContractRecordId)
				+ "'  and QTEREV_RECORD_ID = '"
				+ str(RevisionRecordId)
				+ "' and SERVICE_ID = '"
				+ str(TreeParam)
				+ "' ORDER BY "
				+ str(orderby)
			)
			Count = Sql.GetFirst("select count(CpqTableEntryId) as cnt from SAQSSE (NOLOCK) where QUOTE_RECORD_ID = '"+ str(ContractRecordId)+ "'and SERVICE_ID = '" + str(TreeParam) + "' and QTEREV_RECORD_ID = '"+ str(RevisionRecordId)+ "' ")
			if Count:
				QueryCount = Count.cnt
		else: 
			Trace.Write('filter---------')                    
			parent_obj = Sql.GetList(
				"select top "+str(PerPage)+" QUOTE_SERVICE_SENDING_FAB_LOC_EQUIP_ID,SALESORG_ID,EQUIPMENTCATEGORY_ID,SND_EQUIPMENT_ID,MNT_PLANT_ID,GREENBOOK,QUOTE_NAME,SALESORG_NAME,SND_EQUIPMENT_DESCRIPTION,EQUIPMENT_STATUS,PLATFORM,SNDFBL_ID,QUOTE_ID,SNDFBL_NAME from SAQSSE (NOLOCK) where QUOTE_RECORD_ID = '"
				+ str(ContractRecordId)
				+ "' and QTEREV_RECORD_ID = '"
				+ str(RevisionRecordId)
				+ "' and SNDFBL_ID = '"
				+ str(TreeParentParam)
				+ "' AND GREENBOOK = '"
				+ str(TreeParam)
				+ "' ORDER BY "
				+ str(orderby)
			)
			Count = Sql.GetFirst("select count(CpqTableEntryId) as cnt from SAQSSE (NOLOCK) where QUOTE_RECORD_ID = '"+ str(ContractRecordId)+ "' and QTEREV_RECORD_ID = '"+ str(RevisionRecordId)+ "' and SNDFBL_ID = '" + str(TreeParentParam) + "' AND GREENBOOK = '" + str(TreeParam) + "'")
			if Count:
				QueryCount = Count.cnt

	else:
		#Trace.Write("search with condition")
		conditionsearch_falg = 1              
		if TreeParentParam == 'Sending Equipment' or TreeParentParam == 'Receiving equipment':
			parent_obj = Sql.GetList(
				"select top "+str(PerPage)+" QUOTE_SERVICE_SENDING_FAB_LOC_EQUIP_ID,SALESORG_ID,EQUIPMENTCATEGORY_ID,SND_EQUIPMENT_ID,MNT_PLANT_ID,GREENBOOK,QUOTE_NAME,SALESORG_NAME,SND_EQUIPMENT_DESCRIPTION,EQUIPMENT_STATUS,PLATFORM,SNDFBL_ID,QUOTE_ID,SNDFBL_NAME from SAQSSE (NOLOCK) where "
				+ str(ATTRIBUTE_VALUE_STR)
				+ " 1=1 and QUOTE_RECORD_ID = '"
				+ str(ContractRecordId)
				+ "' and QTEREV_RECORD_ID = '"
				+ str(RevisionRecordId)
				+ "' and SNDFBL_ID = '"
				+ str(TreeParam)
				+ "' ORDER BY "
				+ str(orderby)
			)
			Count = Sql.GetFirst("select count(*) as cnt  from SAQSSE (NOLOCK) where "
				+ str(ATTRIBUTE_VALUE_STR)
				+ " 1=1 and QUOTE_RECORD_ID = '"
				+ str(ContractRecordId)
				+ "' and QTEREV_RECORD_ID = '"
				+ str(RevisionRecordId)
				+ "' and SNDFBL_ID = '"
				+ str(TreeParam)
				+ "'")
			if Count:
				QueryCount = Count.cnt
		elif TreeSuperParentParam == 'Sending Equipment' or TreeSuperParentParam == 'Receiving equipment':
			Trace.Write('teee========')
			parent_obj = Sql.GetList(
				"select top "+str(PerPage)+" QUOTE_SERVICE_SENDING_FAB_LOC_EQUIP_ID,SALESORG_ID,EQUIPMENTCATEGORY_ID,SND_EQUIPMENT_ID,MNT_PLANT_ID,GREENBOOK,QUOTE_NAME,SALESORG_NAME,SND_EQUIPMENT_DESCRIPTION,EQUIPMENT_STATUS,PLATFORM,SNDFBL_ID,QUOTE_ID,SNDFBL_NAME from SAQSSE (NOLOCK) where "
				+ str(ATTRIBUTE_VALUE_STR)
				+ " 1=1 and QUOTE_RECORD_ID = '"
				+ str(ContractRecordId)
				+ "' and QTEREV_RECORD_ID = '"
				+ str(RevisionRecordId)
				+ "' and SNDFBL_ID = '"
				+ str(TreeParentParam)
				+ "'  and GREENBOOK = '"
				+ str(TreeParam)
				+ "' ORDER BY "
				+ str(orderby)
			)
			Count = Sql.GetFirst("select count(*) as cnt  from SAQSSE (NOLOCK) where "
				+ str(ATTRIBUTE_VALUE_STR)
				+ " 1=1 and QUOTE_RECORD_ID = '"
				+ str(ContractRecordId)
				+ "' and QTEREV_RECORD_ID = '"
				+ str(RevisionRecordId)
				+ "' and SNDFBL_ID = '"
				+ str(TreeParentParam)
				+ "'  and GREENBOOK = '"
				+ str(TreeParam)
				+ "'")
			if Count:
				QueryCount = Count.cnt        
		else:
			parent_obj = Sql.GetList(
				"select top "+str(PerPage)+"  QUOTE_SERVICE_SENDING_FAB_LOC_EQUIP_ID,SALESORG_ID,EQUIPMENTCATEGORY_ID,SND_EQUIPMENT_ID,MNT_PLANT_ID,GREENBOOK,QUOTE_NAME,SALESORG_NAME,SND_EQUIPMENT_DESCRIPTION,EQUIPMENT_STATUS,PLATFORM,SNDFBL_ID,QUOTE_ID,SNDFBL_NAME from SAQSSE (NOLOCK) where "
				+ str(ATTRIBUTE_VALUE_STR)
				+ " 1=1 and QUOTE_RECORD_ID = '"
				+ str(ContractRecordId)
				+ "' and QTEREV_RECORD_ID = '"
				+ str(RevisionRecordId)
				+ "' ORDER BY "+ str(orderby)
			)
			Count = Sql.GetFirst("select count(*) as cnt from SAQSSE (NOLOCK) where "+ str(ATTRIBUTE_VALUE_STR)+ " 1=1 and QUOTE_RECORD_ID = '"+ str(ContractRecordId)+ "' and QTEREV_RECORD_ID = '"+ str(RevisionRecordId)+ "' ")
			if Count:
				QueryCount = Count.cnt
	for par in parent_obj:
		
		data_dict = {}
		data_id = str(par.QUOTE_SERVICE_SENDING_FAB_LOC_EQUIP_ID)        
		Action_str = (
			'<div class="btn-group dropdown"><div class="dropdown" id="ctr_drop"><i data-toggle="dropdown" id="dropdownMenuButton" class="fa fa-sort-desc dropdown-toggle" aria-expanded="false"></i><ul class="dropdown-menu left" aria-labelledby="dropdownMenuButton"><li><a class="dropdown-item cur_sty" href="#" id="'
			+ str(data_id)
			+ '" onclick="Commonteree_view_RL(this)">VIEW</a></li>'
		)
		if can_edit.upper() == "TRUE":
			Action_str += (
				'<li style="display:none" ><a class="dropdown-item cur_sty" href="#" id="'
				+ str(data_id)
				+ '" onclick="Commonteree_view_RL(this)">EDIT</a></li>'
			)
		if can_delete.upper() == "TRUE":
			Action_str += '<li><a class="dropdown-item" data-target="#cont_viewModal_Material_Delete" data-toggle="modal" onclick="Material_delete_obj(this)" href="#">DELETE</a></li>'
		if can_clone.upper() == "TRUE":
			Action_str += '<li><a class="dropdown-item" data-target="#" data-toggle="modal" onclick="Material_clone_obj(this)" href="#">CLONE</a></li>'

		Action_str += "</ul></div></div>"
		data_dict["ids"] = str(data_id)
		data_dict["ACTIONS"] = str(Action_str)
		data_dict["QUOTE_SERVICE_SENDING_FAB_LOC_EQUIP_ID"] = CPQID.KeyCPQId.GetCPQId("SAQSSE", str(par.QUOTE_SERVICE_SENDING_FAB_LOC_EQUIP_ID))
		data_dict["SND_EQUIPMENT_ID"] = ('<abbr id ="" title="' + str(par.SND_EQUIPMENT_ID) + '">' + str(par.SND_EQUIPMENT_ID) + "</abbr>") 
		data_dict["PLATFORM"] = ('<abbr id ="" title="' + str(par.PLATFORM) + '">' + str(par.PLATFORM) + "</abbr>")
		data_dict["SNDFBL_ID"] = ('<abbr id ="" title="' + str(par.SNDFBL_ID) + '">' + str(par.SNDFBL_ID) + "</abbr>")
		data_dict["SALESORG_ID"] = ('<abbr id ="" title="' + str(par.SALESORG_ID) + '">' + str(par.SALESORG_ID) + "</abbr>")
		data_dict["EQUIPMENTCATEGORY_ID"] = ('<abbr id ="" title="' + str(par.EQUIPMENTCATEGORY_ID) + '">' + str(par.EQUIPMENTCATEGORY_ID) + "</abbr>")
		#data_dict["SERIAL_NUMBER"] = ('<abbr id ="" title="' + str(par.SERIAL_NUMBER) + '">' + str(par.SERIAL_NUMBER) + "</abbr>")
		#data_dict["CUSTOMER_TOOL_ID"] = ('<abbr id ="" title="' + str(par.CUSTOMER_TOOL_ID) + '">' + str(par.CUSTOMER_TOOL_ID) + "</abbr>")
		data_dict["GREENBOOK"] = ('<abbr id ="" title="' + str(par.GREENBOOK) + '">' + str(par.GREENBOOK) + "</abbr>")
		data_dict["EQUIPMENT_STATUS"] = ('<abbr id ="" title="' + str(par.EQUIPMENT_STATUS) + '">' + str(par.EQUIPMENT_STATUS) + "</abbr>")
		data_dict["SND_EQUIPMENT_DESCRIPTION"] = ('<abbr id ="" title="' + str(par.SND_EQUIPMENT_DESCRIPTION) + '">' + str(par.SND_EQUIPMENT_DESCRIPTION) + "</abbr>")
		data_dict["SNDFBL_NAME"] = ('<abbr id ="" title="' + str(par.SNDFBL_NAME) + '">' + str(par.SNDFBL_NAME) + "</abbr>")
		data_dict["MNT_PLANT_ID"] = ('<abbr id ="" title="' + str(par.MNT_PLANT_ID) + '">' + str(par.MNT_PLANT_ID) + "</abbr>")
		#data_dict["WARRANTY_START_DATE"] = ('<abbr id ="" title="' + str(par.WARRANTY_START_DATE) + '">' + str(par.WARRANTY_START_DATE) + "</abbr>")
		#data_dict["WARRANTY_END_DATE"] = ('<abbr id ="" title="' + str(par.WARRANTY_END_DATE) + '">' + str(par.WARRANTY_END_DATE) + "</abbr>")
		data_dict["QUOTE_ID"] = ('<abbr id ="" title="' + str(par.QUOTE_ID) + '">' + str(par.QUOTE_ID) + "</abbr>")
		data_list.append(data_dict)

	page = ""
	if QueryCount ==0:
		page = str(QueryCount) + " - " + str(QueryCount) + " of "
	elif QueryCount < int(PerPage):
		page = str(Page_start) + " - " + str(QueryCount) + " of "
	else:
		page = str(Page_start) + " - " + str(Page_End)+ " of "
	# Trace.Write("6666 QueryCount --->"+str(QueryCount))
	# Trace.Write("6666 page --->"+str(page))

	return data_list,QueryCount,page 

	

# Param Variable
TABNAME = Param.TABNAME
Trace.Write('TABNAME###==='+str(TABNAME))
ACTION = Param.ACTION
try:
	TABLENAME = Param.TABLENAME
	TABLENAME = TABLENAME.strip()
except:
	TABLENAME = ""
##PM EVENTS PARAM STARTS..
try:
	ASSEMBLYID = Param.ASSEMBLYID
except:
	ASSEMBLYID = ""
try:
	EQUIPMENTID = Param.EQUIPMENTID
except:
	EQUIPMENTID = ""
try:
	KITID = Param.KITID
except:
	KITID = ""
try:
	KITNUMBER = Param.KITNUMBER
except:
	KITNUMBER = ""      
try:
	PM_ID = Param.PM_ID
except:
	PM_ID = ""    
##PM EVENTS PARAM ENDS..    

try:
	CHILDEQUIPMENT = Param.CHILDEQUIPMENT
except:
	CHILDEQUIPMENT = ""
try:
	ATTRIBUTE_NAME = Param.ATTRIBUTE_NAME
except:
	ATTRIBUTE_NAME = ""
try:
	CURR_REC_ID = Param.RECORD_ID
except:
	CURR_REC_ID = ""
try:
	SortColumn = Param.SortColumn
	SortColumnOrder = Param.SortColumnOrder
	Trace.Write("SORT COLUMN-----"+str(SortColumn))
	Trace.Write("SORT COLUMN ORDER -----"+str(SortColumnOrder))
except:
	SortColumn = ''
	SortColumnOrder = ''
try:
	SortPerPage = Param.PerPage
	SortPageInform = Param.PageInform
except:
	SortPerPage = ''
	SortPageInform = ''
	Trace.Write("SORT EMPTY")
##get pagination flag for nested grid starts
try:
	pagination_flag = Param.pagination_flag
except:
	pagination_flag = ""
##get pagination flag for nested grid ends
try:
	active_subtab = Param.active_subtab
except:
	active_subtab = ""
Trace.Write('active_subtab'+str(active_subtab))
# try:
#     selected_values= eval(Param.Values)
#     Trace.Write('selected_values-----'+str(selected_values))
# except:
#     selected_values =[]
# try:
#     unselected_values= eval(Param.unselected_list)
#     Trace.Write('unselected_list-----'+str(unselected_values))
# except Exception,e:
#     Trace.Write('unselected_values--error-'+str(e))
#     unselected_values =[]
# Trace.Write("SORT SortPerPage-----"+str(SortPerPage))
# Trace.Write("SORT SortPageInform -----"+str(SortPageInform))
# Trace.Write("Current Rec Id is " + str(CURR_REC_ID))
# Trace.Write("assembly id" + str(ASSEMBLYID))
# Trace.Write("EQUIPMENTID id" + str(EQUIPMENTID))
TreeParam = Product.GetGlobal("TreeParam")
TreeParentParam = Product.GetGlobal("TreeParentLevel0")
TreeSuperParentParam = Product.GetGlobal("TreeParentLevel1")    
TreeTopSuperParentParam = Product.GetGlobal("TreeParentLevel2")    
Trace.Write("TABNAME-----" + str(TABNAME))
Trace.Write("ACTION-----" + str(ACTION))
Trace.Write("ATTRIBUTE_NAME" + str(ATTRIBUTE_NAME))
Trace.Write("ATTRIBUTE_NAME" + str(list(ATTRIBUTE_NAME)))
try:
	ATTRIBUTE_VALUE = Param.ATTRIBUTE_VALUE
except:
	ATTRIBUTE_VALUE = ""
# Trace.Write("bbbbbbbbbbbbbbb" + str(list(ATTRIBUTE_VALUE)))
# Trace.Write("SORT KITID-----"+str(KITID))
# Trace.Write("SORT KITNUMBER -----"+str(KITNUMBER))

##CHANGED FOR CHILD TABLE PAGINATION
if ACTION == "LOAD":
	Trace.Write('load--------------------------')
	PerPage = "10"
	PageInform = "1___10___10"
	A_Keys = []
	A_Values = []
	if TABNAME == "Equipment Parent":
		ApiResponse = ApiResponseFactory.JsonResponse(GetEquipmentMaster(PerPage, PageInform, A_Keys, A_Values))
	elif TABNAME == "Sending Equipment Parent":
		ApiResponse = ApiResponseFactory.JsonResponse(GetSendingEquipmentMaster(PerPage, PageInform, A_Keys, A_Values))
	elif TABNAME == "Sending Equipment Parent Pagination":
		A_Keys = list(Param.ATTRIBUTE_NAME)
		A_Values = list(Param.ATTRIBUTE_VALUE)
		PerPage = Param.PerPage
		PageInform = Param.PageInform
		Trace.Write("Keys" + str(list(A_Keys)))
		Trace.Write("Values" + str(list(A_Values)))
		Trace.Write("PerPage" + str(PerPage))
		Trace.Write("PageInform" + str(PageInform))
		ApiResponse = ApiResponseFactory.JsonResponse(GetSendingEquipmentMaster(PerPage, PageInform, A_Keys, A_Values))    
	elif TABNAME == "Contract Equipment Parent":
		ApiResponse = ApiResponseFactory.JsonResponse(GetContractEquipmentMaster(PerPage, PageInform, A_Keys, A_Values))
	elif TABNAME == "Assemblies Parent":
		ApiResponse = ApiResponseFactory.JsonResponse(GetAssembliesMaster(PerPage, PageInform, A_Keys, A_Values))
	elif TABNAME == "Contract Assemblies Parent":
		ApiResponse = ApiResponseFactory.JsonResponse(GetContractAssembliesMaster(PerPage, PageInform, A_Keys, A_Values))
	elif TABNAME == "Covered Object Parent":
		ApiResponse = ApiResponseFactory.JsonResponse(GetCovObjMaster(PerPage, PageInform, A_Keys, A_Values))
	elif TABNAME == "Contract Covered Object Parent":
		ApiResponse = ApiResponseFactory.JsonResponse(GetContractCovObjMaster(PerPage, PageInform, A_Keys, A_Values))
	elif TABNAME == "Preventive Maintainence Parent":
		Trace.Write("Preventive Maintainence Parent")
		ApiResponse = ApiResponseFactory.JsonResponse(QuoteAssemblyPreventiveMaintainenceParent(PerPage, PageInform, A_Keys, A_Values,ASSEMBLYID,EQUIPMENTID))    
	elif TABNAME == "Equipment Master Pagination":
		A_Keys = list(Param.ATTRIBUTE_NAME)
		A_Values = list(Param.ATTRIBUTE_VALUE)
		PerPage = Param.PerPage
		PageInform = Param.PageInform
		Trace.Write("Keys" + str(list(A_Keys)))
		Trace.Write("Values" + str(list(A_Values)))
		Trace.Write("PerPage" + str(PerPage))
		Trace.Write("PageInform" + str(PageInform))
		ApiResponse = ApiResponseFactory.JsonResponse(GetEquipmentMaster(PerPage, PageInform, A_Keys, A_Values))
	elif TABNAME == "Preventive Maintainence Parent Pagination":
		A_Keys = list(Param.ATTRIBUTE_NAME)
		A_Values = list(Param.ATTRIBUTE_VALUE)
		PerPage = Param.PerPage
		PageInform = Param.PageInform
		ApiResponse = ApiResponseFactory.JsonResponse(QuoteAssemblyPreventiveMaintainenceParent(PerPage, PageInform, A_Keys, A_Values,ASSEMBLYID,EQUIPMENTID))    
	elif TABNAME == "Preventive Maintainence Child Pagination":
		A_Keys = list(Param.ATTRIBUTE_NAME)
		A_Values = list(Param.ATTRIBUTE_VALUE)
		PerPage = Param.PerPage
		PageInform = Param.PageInform
		Trace.Write("child pm event PerPage ---->"+str(PerPage))
		Trace.Write("child pm event PageInform ---->"+str(PageInform))
		ApiResponse = ApiResponseFactory.JsonResponse(QuoteAssemblyPreventiveMaintainenceKitMaterialChild(PM_ID,PerPage, PageInform, A_Keys, A_Values,ASSEMBLYID,EQUIPMENTID))    
	elif TABNAME == "Contract Equipment Master Pagination":
		A_Keys = list(Param.ATTRIBUTE_NAME)
		A_Values = list(Param.ATTRIBUTE_VALUE)
		PerPage = Param.PerPage
		PageInform = Param.PageInform
		ApiResponse = ApiResponseFactory.JsonResponse(GetContractEquipmentMaster(PerPage, PageInform, A_Keys, A_Values))
	elif TABNAME == "Equipment Child Pagination":
		A_Keys = list(Param.ATTRIBUTE_NAME)
		A_Values = list(Param.ATTRIBUTE_VALUE)
		PerPage = Param.PerPage
		PageInform = Param.PageInform
		ApiResponse = ApiResponseFactory.JsonResponse(GetEquipmentChild(CHILDEQUIPMENT, PerPage, PageInform, A_Keys, A_Values))
	elif TABNAME == "CovObj Master Pagination":
		A_Keys = list(Param.ATTRIBUTE_NAME)
		A_Values = list(Param.ATTRIBUTE_VALUE)
		PerPage = Param.PerPage
		PageInform = Param.PageInform
		ApiResponse = ApiResponseFactory.JsonResponse(GetCovObjMaster(PerPage, PageInform, A_Keys, A_Values))
		Trace.Write("Current Rec Id is " + str(CURR_REC_ID))
	elif TABNAME == "Contract CovObj Master Pagination":
		A_Keys = list(Param.ATTRIBUTE_NAME)
		A_Values = list(Param.ATTRIBUTE_VALUE)
		PerPage = Param.PerPage
		PageInform = Param.PageInform
		ApiResponse = ApiResponseFactory.JsonResponse(GetContractCovObjMaster(PerPage, PageInform, A_Keys, A_Values))
		Trace.Write("Current Rec Id is " + str(CURR_REC_ID))
	elif TABNAME == "CoveredObj Child Pagination":
		A_Keys = list(Param.ATTRIBUTE_NAME)
		A_Values = list(Param.ATTRIBUTE_VALUE)
		PerPage = Param.PerPage
		PageInform = Param.PageInform
		ApiResponse = ApiResponseFactory.JsonResponse(GetCovObjChild(EQUIPMENTID, PerPage, PageInform, A_Keys, A_Values))
		Trace.Write("Current Rec Id is " + str(CURR_REC_ID)) 
	elif TABNAME == "Sendingequp Child Pagination":
		Trace.Write('sendingequp=================')
		A_Keys = list(Param.ATTRIBUTE_NAME)
		A_Values = list(Param.ATTRIBUTE_VALUE)
		PerPage = Param.PerPage
		PageInform = Param.PageInform
		ApiResponse = ApiResponseFactory.JsonResponse(GetSendingEquipmentChild(EQUIPMENTID, PerPage, PageInform, A_Keys, A_Values))
		Trace.Write("Current Rec Id is " + str(CURR_REC_ID))         
	elif TABNAME == "Equipment Parent":
		ApiResponse = ApiResponseFactory.JsonResponse(GetEquipmentMasterFilter(ATTRIBUTE_NAME, ATTRIBUTE_VALUE))
	elif TABNAME == 'Common Parent Contracts':
		ApiResponse = ApiResponseFactory.JsonResponse(GetCommonParentContract(PerPage, PageInform, A_Keys, A_Values))
	else:
		Trace.Write('TABNAME@@@@')    

elif ACTION == "PRODUCT_ONLOAD_FILTER":
	if TABNAME == "Equipment Parent Filter":
		ApiResponse = ApiResponseFactory.JsonResponse(GetEquipmentMasterFilter(ATTRIBUTE_NAME, ATTRIBUTE_VALUE,SortPerPage,SortPageInform))
	elif TABNAME == "Equipment Parent":
		Trace.Write("EDITWORK")
		ApiResponse = ApiResponseFactory.JsonResponse(GetEquipmentMasterFilter(ATTRIBUTE_NAME, ATTRIBUTE_VALUE,SortPerPage,SortPageInform))
	elif TABNAME == "Contract Equipment Parent":
		ApiResponse = ApiResponseFactory.JsonResponse(GetContractEquipmentMasterFilter(ATTRIBUTE_NAME, ATTRIBUTE_VALUE,SortPerPage,SortPageInform))
	elif TABNAME == "Preventive Maintainence Parent":
		ApiResponse = ApiResponseFactory.JsonResponse(QuoteAssemblyPreventiveMaintainenceParentFilter(ATTRIBUTE_NAME, ATTRIBUTE_VALUE,ASSEMBLYID,EQUIPMENTID,SortPerPage,SortPageInform))
	elif TABNAME == "Preventive Maintainence child Filter":
		RECID = Param.REC_ID
		ApiResponse = ApiResponseFactory.JsonResponse(QuoteAssemblyPreventiveMaintainenceKitMaterialChildFilter(ATTRIBUTE_NAME, ATTRIBUTE_VALUE, RECID,ASSEMBLYID,EQUIPMENTID,KITID,KITNUMBER,SortPerPage,SortPageInform))        
	elif TABNAME == "Equipments child": 
		Trace.Write("111111111")
		try:
			REC_ID = Param.REC_ID
			RECID = REC_ID.split("_")[-1]
		except:
			RECID = ""
		Trace.Write("123 RECID --->"+str(RECID))
		ApiResponse = ApiResponseFactory.JsonResponse(GetEquipmentChildFilter(ATTRIBUTE_NAME, ATTRIBUTE_VALUE, RECID,SortPerPage,SortPageInform))
	elif TABNAME == "Assemblies Child":
		Trace.Write("inside assembly child filter")
		RECID = Param.RECID
		ApiResponse = ApiResponseFactory.JsonResponse(GetAssembliesChildFilter(ATTRIBUTE_NAME, ATTRIBUTE_VALUE, RECID))
	elif TABNAME == "Covered Object Parent":
		Trace.Write("trace for tabname during search----" + str(TABNAME))
		ApiResponse = ApiResponseFactory.JsonResponse(GetCovObjMasterFilter(ATTRIBUTE_NAME, ATTRIBUTE_VALUE,SortPerPage,SortPageInform))
	elif TABNAME == "Contract Covered Object Parent":
		Trace.Write("trace for tabname during search----" + str(TABNAME))
		ApiResponse = ApiResponseFactory.JsonResponse(GetContractCovObjMasterFilter(ATTRIBUTE_NAME, ATTRIBUTE_VALUE,SortPerPage,SortPageInform))
	elif TABNAME == "Covered Object Child":
		REC_ID = Param.REC_ID
		RECID = REC_ID.split("_")[-1]
		Trace.Write("123 Covered Object Child RECID --->"+str(RECID))
		ApiResponse = ApiResponseFactory.JsonResponse(
			GetCovObjChildFilter(ATTRIBUTE_NAME, ATTRIBUTE_VALUE, RECID,SortPerPage,SortPageInform)
		)
	elif TABNAME == "Sending Equipment child":
		Trace.Write('send9999====')
		REC_ID = Param.REC_ID
		RECID = REC_ID.split("_")[-1]
		Trace.Write("123 Covered Object Child RECID --->"+str(RECID))
		ApiResponse = ApiResponseFactory.JsonResponse(
			GetSendEupChildFilter(ATTRIBUTE_NAME, ATTRIBUTE_VALUE, RECID,SortPerPage,SortPageInform)
		)    
	elif TABNAME == "Common Parent":
		#REC_ID = Param.REC_ID
		#RECID = REC_ID.split("_")[-1]
		#Trace.Write("123 Covered Object Child RECID --->"+str(RECID))
		ApiResponse = ApiResponseFactory.JsonResponse(
			GetCommonParentFilter(ATTRIBUTE_NAME, ATTRIBUTE_VALUE,SortPerPage,SortPageInform)
		)

	elif TABNAME == "Common Parent Child":
		REC_ID = Param.REC_ID
		RECID = REC_ID.split("_")[-1]
		Trace.Write("123 Common Parent Child RECID --->"+str(RECID))
		ApiResponse = ApiResponseFactory.JsonResponse(
			WithBundleParentTableFilter(ATTRIBUTE_NAME, ATTRIBUTE_VALUE,RECID,SortPerPage,SortPageInform))
	elif TABNAME == "Sending Equipment Parent Filter":
		ApiResponse = ApiResponseFactory.JsonResponse(GetSendingEquipmentFilter(ATTRIBUTE_NAME, ATTRIBUTE_VALUE,SortPerPage,SortPageInform))
	elif TABNAME == "Sending Equipment Parent":
		Trace.Write("EDITWORK")
		ApiResponse = ApiResponseFactory.JsonResponse(GetSendingEquipmentFilter(ATTRIBUTE_NAME, ATTRIBUTE_VALUE,SortPerPage,SortPageInform))       
	# elif TABNAME == "Sending Equipment child": 
	#     Trace.Write("111111111_J ")
	#     REC_ID = Param.REC_ID
	#     RECID = REC_ID
	#     Trace.Write("123 RECID --->_J "+str(RECID))
	#     ApiResponse = ApiResponseFactory.JsonResponse(GetSendingEquipmentChild(ATTRIBUTE_NAME, ATTRIBUTE_VALUE, RECID,SortPerPage,SortPageInform))
elif ACTION == "CHILDLOAD":
	PerPage = "10"
	PageInform = "1___10___10"
	A_Keys = []
	A_Values = []
	if TABNAME == "Equipment child":
		ApiResponse = ApiResponseFactory.JsonResponse(
			GetEquipmentChild(ATTRIBUTE_NAME, PerPage, PageInform, A_Keys, A_Values)
		)
	elif TABNAME == "Sending Equipment child":
		ApiResponse = ApiResponseFactory.JsonResponse(
			GetSendingEquipmentChild(ATTRIBUTE_NAME, PerPage, PageInform, A_Keys, A_Values)
		)
	elif TABNAME == "Assemblies Child":
		ApiResponse = ApiResponseFactory.JsonResponse(
			GetAssembliesChild(ATTRIBUTE_NAME, PerPage, PageInform, A_Keys, A_Values)
		)
	elif TABNAME == "Preventive Maintainence child":
		ApiResponse = ApiResponseFactory.JsonResponse(
			QuoteAssemblyPreventiveMaintainenceKitMaterialChild(ATTRIBUTE_NAME, PerPage, PageInform, A_Keys, A_Values,ASSEMBLYID,EQUIPMENTID,KITID,KITNUMBER)
		)    
	elif TABNAME == "Covered Object Child":
		ApiResponse = ApiResponseFactory.JsonResponse(GetCovObjChild(ATTRIBUTE_NAME, PerPage, PageInform, A_Keys, A_Values))   
elif ACTION == "BREADCRUMB":
	if TABNAME == "Tools":
		ApiResponse = ApiResponseFactory.JsonResponse(UpdateBreadcrumb())
elif ACTION == 'SERVICE FAB DETAILS':
	ApiResponse = ApiResponseFactory.JsonResponse(ServiceFabDetails())
# elif ACTION == 'BUNDLE CALC':
# 	REC_ID = Param.REC_ID
## 	ApiResponse = ApiResponseFactory.JsonResponse(BundleCalc(REC_ID))

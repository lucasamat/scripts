# =========================================================================================================================================
#   __script_name : SYLDCTNPTL.PY
#   __script_description : THIS SCRIPT IS USED TO LOAD ALL CONTAINERS AND PIVOT TABLES ACROSS ALL THE APPS
#   __primary_author__ : JOE EBENEZER
#   __create_date :
# ==========================================================================================================================================
import re
import Webcom.Configurator.Scripting.Test.TestProduct
import SYTABACTIN as Table
import math
from SYDATABASE import SQL

Sql = SQL()


# SQLVIEW CTR_TYPE FUNCTIONALITY
def MMDYNMICSQLTABLE(QST_REC_ID):
	Qst_obj = Sql.GetFirst("select * from SYSEFL (NOLOCK) where SAPCPQ_ATTRIBUTE_NAME = '" + str(QST_REC_ID) + "'")
	SQL_Expression = ""
	table_id = ""
	if Qst_obj is not None:
		SQL_Expression = Qst_obj.CONTAINER_SQL_EXPRESSION
		table_id = Qst_obj.SAPCPQ_ATTRIBUTE_NAME.replace("-", "_")
	table_header = '<table class="table table-bordered" id="' + table_id + '">'
	if SQL_Expression:
		sql_exp = re.findall(r"Value\((.*?)\)\s\*>", SQL_Expression)

		if len(sql_exp) > 0:
			for getr in sql_exp:
				parse_val = "<* Value(" + getr + ") *>"
				ParseVal = Product.ParseString(str(parse_val)) or ""
				SQL_Expression = SQL_Expression.replace("<* Value(" + getr + ") *>", ParseVal)
		k_list = []
		Query_Obj = Sql.GetList(SQL_Expression)
		a_list = []
		dict_key = []
		for ik in Query_Obj:
			new_dict = {}
			list_lineup = []
			for inm in ik:
				value123 = str(inm).split(",")[0].replace("[", "").lstrip()
				value1234 = str(inm).split(",")[1].replace("]", "").lstrip()
				new_dict[value123] = value1234
				list_lineup.append(value123)
			dict_key = list_lineup
			a_list.append(new_dict)
		table_header += "<tr>"

		# CREATION OF TABLEHEADER_COLUMNS
		table_header += '<th class="column-with-actions-header">ACTIONS</th>'
		for invs in dict_key:
			table_header += (
				'<th class=""><abbr title="'
				+ str(invs).replace("_", " ")
				+ '">'
				+ str(invs).replace("_", " ")
				+ "</abbr></th>"
			)
		table_header += "</tr>"

		# CREATION OF TABLEDATA
		for key, insk in enumerate(a_list):
			table_header += '<tr id ="' + str(table_id) + "_" + str(key) + '" >'
			table_header += '<td class="column-with-actions dropdown ctr_action_width"><div class="btn-group dropdown">\
			<div class="dropdown" id="ctr_drop"><i data-toggle="dropdown" id="dropdownMenuButton" \
			class="fa fa-sort-desc dropdown-toggle" aria-expanded="false"></i><ul class="dropdown-menu left" \
			aria-labelledby="dropdownMenuButton"><li><a class="dropdown-item" href="#" data-target="#cont_viewModalSection" \
			onclick="cont_openview(this)" data-toggle="modal">VIEW</a></li><li><a class="dropdown-item" href="#" \
			onclick="cont_openedit(this)" data-target="#cont_viewModalSection" data-toggle="modal">EDIT</a></li><li>\
			<a class="dropdown-item" onclick="cont_delete(this)" href="#">DELETE</a></li></ul></div></div></td>'
			for key, value in insk.items():
				value = value.encode("ascii", "ignore")
				table_header += '<td><abbr title="' + str(value) + '">' + str(value) + "</abbr></td>"
			table_header += "</tr>"
	table_header += "</table>"
	return table_header


# SQLVIEW123 CTR_TYPE
def MDYNMICSQLTABLE123(QST_REC_ID):
	Qst_obj = Sql.GetFirst("select * from SYSEFL (NOLOCK) where SAPCPQ_ATTRIBUTE_NAME = '" + str(QST_REC_ID) + "'")
	SQL_Expression = ""
	table_id = ""
	if Qst_obj is not None:
		SQL_Expression = Qst_obj.CONTAINER_SQL_EXPRESSION
		table_id = Qst_obj.SAPCPQ_ATTRIBUTE_NAME.replace("-", "_")
	table_header = (
		'<table id="'
		+ table_id
		+ '" data-show-header="true" data-pagination="true" data-page-list="[5, 10, 25, 50, 100, ALL]" data-page-size="5">'
	)
	table_header_alter = '<table class="table table-bordered" id="' + table_id + '">'
	table_list = []
	if SQL_Expression:
		sql_exp = re.findall(r"Value\((.*?)\)\s\*>", SQL_Expression)
		if len(sql_exp) > 0:
			for getr in sql_exp:
				parse_val = "<* Value(" + getr + ") *>"
				ParseVal = Product.ParseString(str(parse_val)) or ""
				SQL_Expression = SQL_Expression.replace("<* Value(" + getr + ") *>", ParseVal)
		k_list = []
		Query_Obj = Sql.GetList(SQL_Expression)
		table_list = []
		dict_key = []
		for ik in Query_Obj:
			new_dict = {}
			list_lineup = []
			for inm in ik:
				value123 = str(inm).split(",")[0].replace("[", "").lstrip()
				value1234 = str(inm).split(",")[1].replace("]", "").lstrip()
				new_dict[
					"ACTIONS"
				] = '<div class="btn-group dropdown"><div class="dropdown" id="ctr_drop"><i data-toggle="dropdown" \
				id="dropdownMenuButton" class="fa fa-sort-desc dropdown-toggle" aria-expanded="false"></i><ul \
				class="dropdown-menu left" aria-labelledby="dropdownMenuButton"><li><a class="dropdown-item" \
				href="#" data-target="#cont_viewModalSection" onclick="cont_openview(this)" data-toggle="modal">\
				VIEW</a></li><li><a class="dropdown-item" href="#" onclick="cont_openedit(this)" \
				data-target="#cont_viewModalSection" data-toggle="modal">EDIT</a></li><li><a class="dropdown-item" \
				onclick="cont_delete(this)" href="#">DELETE</a></li></ul></div></div>'
				new_dict[value123] = value1234
				list_lineup.append(value123)
			list_lineup.insert(0, "ACTIONS")
			dict_key = list_lineup
			table_list.append(new_dict)
		table_header += "<thead><tr>"
		table_header_alter += "<thead><tr>"

		# CREATION OF TABLEHEADER_COLUMNS
		for invs in dict_key:
			table_header += (
				'<th data-field="'
				+ str(invs)
				+ '" class=""><abbr title="'
				+ str(invs).replace("_", " ")
				+ '">'
				+ str(invs).replace("_", " ")
				+ "</abbr></th>"
			)
			table_header_alter += (
				'<th class=""><abbr title="'
				+ str(invs).replace("_", " ")
				+ '">'
				+ str(invs).replace("_", " ")
				+ "</abbr></th>"
			)
		table_header += "</tr>"
		table_header_alter += "</tr>"
		table_header_alter += "</thead><tbody>"

		# CREATION OF TABLEDATA
		for sis in dict_key:
			table_header_alter += "<tr>"
			for inl in table_list:
				table_header_alter += '<td class=""><abbr title="' + str(inl[sis]) + '">' + str(inl[sis]) + "</abbr></th>"
			table_header_alter += "</tr>"
	table_header += "</thead><tbody></tbody></table>"
	table_header_alter += "</tbody></table>"
	return table_header, table_list, table_id, table_header_alter


# FIXEDROWS CTR_TYPE FOR MATERIAL ATTRIBUTE
# CREATED BY JW 15-04-2019
def StaticMaterialTableFormation(QST_REC_ID, Row_Count, Column_Count, Column_Names_List, New_CtrName):
	if Column_Names_List is not None:
		Column_Names_List = list(eval(Column_Names_List))
	table_header = ""
	return table_header


# FIXEDROWS CTR_TYPE FOR ATTRIBUTE MATERIAL
# CREATED BY JW 16-04-2019
def StaticAttrMtTableFormation(QST_REC_ID, Row_Count, Column_Count, Column_Names_List, New_CtrName):
	# MATERIALS_WITH_ATTRIBUTES_CTR
	table_header = ""
	return table_header


# FIXEDROWS CTR_TYPE AND DYNAMICROWS CTR_TYPE
def StaticTableFormation(
	QST_REC_ID, Row_Count, Column_Count, Column_Names_List, New_CtrName, Offset_Skip_Count=0, Fetch_Count=10,
):
	#Trace.Write("StaticTableFormation------------------------------")
	if Column_Names_List is not None:
		Column_Names_List = list(eval(Column_Names_List))
	#Trace.Write("Column_Names_List-----------------> " + str(Column_Names_List))
	Attribute_ID = [
		"SYSEFL-MA-00382",
		"SYSEFL-MA-00429",
		"SYSEFL-MA-00433",
		"SYSEFL-MA-00434",
		"SYSEFL-PB-00433",
		"SYSEFL-PB-00438",
		"SYSEFL-PB-00437",
		"SYSEFL-MA-00467",
		"SYSEFL-MA-00469",
	]
	pagination = ""
	if QST_REC_ID not in Attribute_ID:
		Row_Count = "1"
		table_header = (
			'<table class="table table-bordered" data-show-header="true" data-pagination="true"  \
			data-page-list="[10, 25, 50, 100, ALL]"  data-page-size="10" data-filter-control="true" id="'
			+ str(New_CtrName)
			+ '">'
		)
		New_CtrName = New_CtrName.replace(" ", "_")

		# CREATION OF TABLEHEADER_COLUMNS
		if Column_Names_List:
			table_header += "<tr>"
			table_header += '<th class="column-with-actions-header">Actions</th>'
			for Names_dict in list(eval(Column_Names_List)):
				table_header += (
					'<th class="column-with-actions-header"><abbr title="'
					+ Names_dict["FIELD_NAME"]
					+ '">'
					+ Names_dict["FIELD_NAME"]
					+ "</abbr></th>"
				)
			table_header += "</tr>"

			# CREATION OF TABLEDATA
			for row in range(0, int(Row_Count)):
				table_header += '<tr id="tr__' + str(New_CtrName) + "__" + str(row) + '">'
				table_header += '<td class="column-with-actions dropdown"><div class="btn-group dropdown">\
				<div class="dropdown" id="ctr_drop"><i data-toggle="dropdown" id="dropdownMenuButton" \
				class="fa fa-sort-desc dropdown-toggle" aria-expanded="false"></i><ul class="dropdown-menu left" \
				aria-labelledby="dropdownMenuButton"><li><a class="dropdown-item" href="#" onclick="DeleteFunc(this)">\
				DELETE</a></li></ul></div></div></td>'
				for inc in range(0, int(Column_Count)):
					table_header += (
						'<td id="td__'
						+ str(New_CtrName)
						+ "__"
						+ str(row)
						+ str(inc)
						+ '"><input  class="form-control" type="text" id="input__td__StaticTable__'
						+ str(row)
						+ str(inc)
						+ '"/></td>'
					)
			table_header += "</tr>"
		table_header += "</table>"
	return table_header


# CUSTOM OBJECT GRID CTR_TYPE
def MDYNMIC_CSBJ_SQLTABLE(QST_REC_ID):
	New_CtrName = str(QST_REC_ID).replace("-", "_")
	QSCO_obj = Sql.GetList(
		"select * from SYQSCO (NOLOCK) where QST_ATT_REC_NO = '" + str(QST_REC_ID) + "' and REQUIRED = 'true'"
	)
	table_header = '<table class="table table-bordered" id="' + str(New_CtrName) + '">'
	Obj_name = ""
	a_list = []
	a_value = []
	a_dict = {}
	a_key = []
	if QSCO_obj is not None:
		for ins in QSCO_obj:
			a_key = []
			Obj_name = ins.OBJECT_NAME
			a_key.append(str(ins.FIELD_LABEL))
			a_value.append(str(ins.API_NAME))
			a_dict[str(ins.FIELD_LABEL)] = ins.API_NAME
		a_value_str = ""
		if a_value:
			a_value_str = ",".join(a_value)
		Mapping_obj = ""
		if Obj_name != "":
			map_obj_str = "select top 5 " + str(a_value_str) + " from " + str(Obj_name)
			Mapping_obj = Sql.GetList(str(map_obj_str))

		#  CREATION OF TABLEHEADER_COLUMNS
		for inv in a_key:
			table_header += "<tr>"
			table_header += '<th class="column-with-actions-header">Actions</th>'
			table_header += "<th>" + str(inv) + "</th>"
		table_header += "</tr>"

		# CREATION OF TABLEDATA
		for inv in a_key:
			for sis in Mapping_obj:
				table_header += "<tr>"
				table_header += '<td class="column-with-actions dropdown"><div class="btn-group dropdown">\
				<div class="dropdown" id="ctr_drop"><i data-toggle="dropdown" id="dropdownMenuButton" \
				class="fa fa-sort-desc dropdown-toggle" aria-expanded="false"></i><ul class="dropdown-menu left" \
				aria-labelledby="dropdownMenuButton"><li><a class="dropdown-item" href="#" onclick="DeleteFunc(this)">\
				DELETE</a></li></ul></div></div></td>'
				str_s = "sis." + str(a_dict[str(inv)])
				table_header += '<td><abbr title="' + str(eval(str_s)) + '">' + str(eval(str_s)) + "</td>"
				table_header += "</tr>"
		table_header += "</table>"
	return table_header


# CTR_INPUT_ONCHANGE CTR_TYPE
def StaticTableFormationOnchange(ColValue, ColId, Upd_Arr, New_CtrName):
	SetName = ""
	SetPartNumber = ""
	row = {}
	New_CtrName = ""
	return New_CtrName, SetName, SetPartNumber, row


def PivotTableFormation(
	ParentNodeRecId, QST_REC_ID, Row_Count, Column_Count, Column_Names_List, New_CtrName, PerPage, PageInform,
):

	# VARIABLES DECLARATION
	idval = ""
	onchange_event = ""
	editable_logic = ""
	lock = ""
	KEY = ""
	Action_str = ""
	ATTRIBUTE_NAME_list = []
	desc_list = []
	NORECORDS = ""
	filter_control_function = ""
	cv_list = ""
	filter_level_list = ""
	DropDownList = ""
	RelatedDrop_str = ""
	table_header_list = ""
	sap_list123 = []
	sap_list12 = []
	sap_dict = {}
	sap_list = []
	sap_list_str123 = ""
	key12 = ""
	dbl_clk_function = ""
	HEADER_LABEL = ""
	recno = ""
	dataload = []
	QueryCount = ""
	Page_End = ""
	Page_start = ""
	if str(PerPage) == "" and str(PageInform) == "":
		Page_start = 1
		Page_End = 10
		PerPage = 10
		PageInform = "1___10___10"
	else:
		Page_start = int(PageInform.split("___")[0])
		Page_End = int(PageInform.split("___")[1])
		PerPage = PerPage
	# PRICEMODEL_ID INPUT_DATA
	key12 = Product.Attributes.GetByName("MA_MTR_TAB_ACTION").GetValue()
	
	if key12 != "CLONE":
		recno = ParentNodeRecId

	else:
		recno = Product.GetGlobal("prbk_key")

	sqlobj22 = Sql.GetFirst(
		"select PRICEMODEL_ID from PRLPBS (NOLOCK) where LIST_PRICEBOOKSET_RECORD_ID = '" + str(recno) + "'"
	)
	if sqlobj22 is not None:
		idval = str(sqlobj22.PRICEMODEL_ID)
	try:
		if Column_Names_List is not None:
			Column_Names_List = list(eval(Column_Names_List))
	except:
		Trace.Write("nnnnnn")
	RecAttValue = " SYOBJD-11569"
	data_obj = Sql.GetFirst(
		"select PICKLIST_VALUES,OBJECT_NAME from SYOBJD (NOLOCK) where SAPCPQ_ATTRIBUTE_NAME = '" + str(RecAttValue) + "'"
	)
	if data_obj is not None:
		Trace.Write("Ififififififif------")
		VALUE_LIST = data_obj.PICKLIST_VALUES
		VALUES_LIST = data_obj.PICKLIST_VALUES.split(",")
		#for name in VALUES_LIST:
	filter_control_function += (
		'setTimeout(function(){ $("#' + str(HEADER_LABEL) + '").colResizable({ resizeMode:"flex"});}, 3000);'
	)
	# Trace.Write(
	# 	"sssddd" + str(onchange_event) + "22222222222222" + str(filter_control_function) + "3333333333" + str(NORECORDS)
	# )

	table_id = HEADER_LABEL
	RECORD_ID = QST_REC_ID
	if QueryCount < int(Page_End):
		PageInformS = str(Page_start) + " - " + str(QueryCount) + " of"
	else:
		PageInformS = str(Page_start) + " - " + str(Page_End) + " of"
	Test = (
		'<div class="col-md-12 brdr listContStyle padbthgt30"><div class="col-md-4 pager-numberofitem  clear-padding">\
		<span class="pager-number-of-items-item flt_lt_pad2_mar2022" id="'
		+ str(table_id)
		+ '_NumberofItem">'
		+ str(PageInformS)
		+ ' </span><span class="pager-number-of-items-item flt_lt_pad2_mar" id="'
		+ str(table_id)
		+ '_totalItemCount">'
		+ str(QueryCount)
		+ '</span><div class="clear-padding fltltmrgtp3"><div class="pull-right vralign"><select onchange=\
		"PageFunctestChild(this, \'Pricefactor\',\''
		+ str(RECORD_ID)
		+ "','"
		+ str(table_id)
		+ '\')" id="'
		+ str(table_id)
		+ '_PageCountValue" class="form-control selcwdt"><option value="10" selected>10</option><option value="20">20\
		</option><option value="50">50</option><option value="100">100</option><option value="200">200</option>\
		</select> </div></div></div><div class="col-xs-8 col-md-4  clear-padding inpadtex" data-bind="visible: \
		totalItemCount"><div class="clear-padding col-xs-12 col-sm-6 col-md-12 brd0"><ul class="pagination pagination">\
		<li class="disabled"><a href="#" onclick="FirstPageLoad_paginationChild(\'Pricefactor\', \''
		+ str(RECORD_ID)
		+ "','"
		+ str(table_id)
		+ '\')"><i class="fa fa-caret-left fnt14bold"></i><i class="fa fa-caret-left fnt14"></i></a></li>\
		<li class="disabled">\
		<a href="#" onclick="Previous12334Child(\'Pricefactor\', \''
		+ str(RECORD_ID)
		+ "','"
		+ str(table_id)
		+ '\')"><i class="fa fa-caret-left fnt14" ></i>PREVIOUS</a></li><li class="disabled"><a href="#" \
		class="disabledPage" \
		onclick="Next12334Child(\'Pricefactor\', \''
		+ str(RECORD_ID)
		+ "','"
		+ str(table_id)
		+ '\')">NEXT<i class="fa fa-caret-right fnt14"></i></a></li><li class="disabled"><a href="#" \
		onclick="LastPageLoad_paginationChild(\'Pricefactor\', \''
		+ str(RECORD_ID)
		+ "','"
		+ str(table_id)
		+ '\')" class="disabledPage"><i class="fa fa-caret-right fnt14"></i><i class="fa fa-caret-right fnt14bold" >\
		</i></a></li></ul></div> </div> <div class="col-md-4 pad3"> <span id="'
		+ str(table_id)
		+ '_page_count" class="currentPage page_right_content">1</span><span class="page_right_content padrt2">Page \
		</span></div></div>'
	)

	dbl_clk_function += (
		'var checkedRows=[]; var selected_checkboxes_index=[]; localStorage.setItem("multiedit_checkbox_values", []); $("#'
		+ str(table_id)
		+ '").on("check.bs.table", function (e, row, $element) { var selected_checkboxes_index=[]; arr11 = $("#'
		+ str(table_id)
		+ '").find("[type=\'checkbox\']:checked").map(function(){ selected_checkboxes_index.push($(this).\
		attr("data-index"));}).get(); localStorage.setItem("selected_checkboxes_index",\
		JSON.stringify(selected_checkboxes_index)); checkedRows.push($element.closest("tr").\
		find("td:eq(2)").text()+"-"+$element.closest("tr").find("td:eq(3)").text()); localStorage.setItem\
		("multiedit_checkbox_values", checkedRows); }); $("#'
		+ str(table_id)
		+ '").on("check-all.bs.table", function (e) { var checkedRows=[]; var table = $("#'
		+ str(table_id)
		+ '").closest("table"); table.find("tbody tr").each(function() {checkedRows.push($(this).\
		find("td:nth-child(3)").text()+"-"+$(this).find("td:nth-child(4)").text()); }); localStorage.setItem\
		("multiedit_checkbox_values", checkedRows); }); $("#'
		+ str(table_id)
		+ '").on("uncheck-all.bs.table", function (e) {localStorage.setItem("multiedit_checkbox_values", []); }); $("#'
		+ str(table_id)
		+ '").on("uncheck.bs.table", function (e, row, $element) {var rec_ids=$element.closest("tr").\
		find("td:eq(2)").text()+"-"+$element.closest("tr").find("td:eq(3)").text(); $.each(checkedRows, \
		function(index, value) { if (value === rec_ids) { checkedRows.splice(index,1); arr11 = $("#'
		+ str(table_id)
		+ '").find("[type=\'checkbox\']:checked").map(function(){ selected_checkboxes_index.splice($(this).\
		attr("data-index"));}).get(); localStorage.setItem("selected_checkboxes_index",JSON.\
		stringify(selected_checkboxes_index)); } }); localStorage.setItem("multiedit_checkbox_values", checkedRows); });'
	)

	dbl_clk_function += (
		'var checkedRows=[];$("#'
		+ str(table_id)
		+ '").on("dbl-click-cell.bs.table", onClickCell); $("#'
		+ str(table_id)
		+ '").on("all.bs.table", function (e, name, args) { $(".bs-checkbox input").addClass("custom"); \
		$(".bs-checkbox input").after("<span class=\'lbl\'></span>"); });  function onClickCell\
		(event, field, value, row, $element) { var reco_id=""; var reco = []; reco = \
		localStorage.getItem("multiedit_checkbox_values") || [];  if (reco === null || reco === undefined ){ reco = []; } \
		if (reco.length > 0){reco = reco.split(",");} if (reco.length > 0){ reco.push($element.closest("tr").\
		find("td:eq(2)").text()+"-"+$element.closest("tr").find("td:eq(3)").text());  data1 = \
		$element.closest("tr").find("td:eq(2)").text()+"-"+$element.closest("tr").find("td:eq(3)").text();   \
		localStorage.setItem("multiedit_save_data", data1); reco_id = removeDuplicates(reco); }else\
		{ reco_id=$element.closest("tr").find("td:eq(2)").text()+"-"+$element.closest("tr").find("td:eq(3)").\
		text();  reco_id=reco_id.split(","); localStorage.setItem("multiedit_save_data", reco_id); } \
		localStorage.setItem("multiedit_data_checked", reco_id); localStorage.setItem("table_id_edit", "'
		+ str(table_id)
		+ '"); cpq.server.executeScript("SYBLKEDTLG", {"TITLE":field, "VALUE":value, "CLICKEDID":"'
		+ str(table_id)
		+ '", "RECORDID":reco_id, "ELEMENT":"EDIT"}, function(data) { data0=data[0]; data2=data[1]; if(data0 != "NO")\
		{ if(document.getElementById("VIEW_DIV_ID") ) { document.getElementById("VIEW_DIV_ID").innerHTML = data0; \
		document.getElementById("cont_viewModalSection").style.display = "block"; $("#cont_viewModalSection").\
		prepend("<div class=\'modal-backdrop fade in\'></div>"); var divHeight = $("#cont_viewModalSection").\
		height(); $("#cont_viewModalSection .modal-backdrop").css("min-height", divHeight+"px"); \
		$("#cont_viewModalSection .modal-dialog").css("width","550px"); $(".modal-dialog").css("margin-top","100px"); } \
		if (data2.length !== 0){ $.each( data2, function( key, values ) { onclick_datepicker(values) }); } } }); } '
	)

	# Trace.Write(str(dbl_clk_function))
	# filter_control_function += (
	# 	' try { setTimeout(function(){ $("#'
	# 	+ str(table_id)
	# 	+ '").colResizable({ resizeMode: "overflow",liveDrag: true, gripInnerHtml: "<div class=\'grip2\'></div>", \
	# 	draggingClass: "dragging"  }); }, 5000); } catch (err) { setTimeout(function(){ $("#'
	# 	+ str(table_id)
	# 	+ '").colResizable({ resizeMode: "overflow",liveDrag: true, gripInnerHtml: "<div class=\'grip2\'></div>", \
	# 	draggingClass: "dragging"  });}, 3000);  } '
	# )

	return (
		table_header_list,
		HEADER_LABEL,
		sap_list,
		NORECORDS,
		onchange_event,
		filter_control_function,
		cv_list,
		filter_level_list,
		DropDownList,
		RelatedDrop_str,
		Test,
		PageInformS,
		QueryCount,
		dbl_clk_function,
	)


def PivotTableSearch(
	ParentNodeRecId,
	QST_REC_ID,
	Row_Count,
	Column_Count,
	Column_Names_List,
	ATTRIBUTE_VALUE,
	New_CtrName,
	PerPage,
	PageInform,
):
	# 7113 STARTS...
	name = "GLOBAL + LIST PRICEBOOK SET + PRICE MODEL + SALES ORG"  # 7113 ENDS...
	recno = ParentNodeRecId
	QueryCount = ""
	Page_End = ""
	Page_start = ""
	#Trace.Write(str())
	if str(PerPage) == "" and str(PageInform) == "":
		Page_start = 1
		Page_End = 10
		PerPage = 10
		PageInform = "1___10___10"
	else:
		Page_start = int(PageInform.split("___")[0])
		Page_End = int(PageInform.split("___")[1])
		PerPage = PerPage
	table_id = New_CtrName
	RECORD_ID = QST_REC_ID
	if QueryCount < int(Page_End):
		PageInformS = str(Page_start) + " - " + str(QueryCount) + " of"
	else:
		PageInformS = str(Page_start) + " - " + str(Page_End) + " of"

	Test = (
		'<div class="col-md-12 brdr listContStyle listpag"  ><div class="col-md-4 pager-numberofitem  clear-padding">\
		<span class="pager-number-of-items-item" id="'
		+ str(table_id)
		+ '_NumberofItem">'
		+ str(PageInformS)
		+ ' </span><span class="pager-number-of-items-item flt_lt_pad2_mar" id="'
		+ str(table_id)
		+ '_totalItemCount">'
		+ str(QueryCount)
		+ '</span><div class="clear-padding fltltmrgtp3"><div class="pull-right vralign">\
		<select onchange="PageFunctestChild(this, \'Pricefactor\',\''
		+ str(RECORD_ID)
		+ "','"
		+ str(table_id)
		+ '\')" id="'
		+ str(table_id)
		+ '_PageCountValue" class="form-control selcwdt"><option value="10" selected>10</option><option value="20">20\
		</option><option value="50">50</option><option value="100">100</option><option value="200">200</option></select>\
		</div></div></div><div class="col-xs-8 col-md-4  clear-padding inpadtex" data-bind="visible: totalItemCount">\
		<div class="clear-padding col-xs-12 col-sm-6 col-md-12 brd0"><ul class="pagination pagination">\
		<li class="disabled"><a href="#" onclick="FirstPageLoad_paginationChild(\'Pricefactor\', \''
		+ str(RECORD_ID)
		+ "','"
		+ str(table_id)
		+ '\')"><i class="fa fa-caret-left fnt14bold"></i><i class="fa fa-caret-left fnt14"></i></a></li><li \
		class="disabled">\
		<a href="#" onclick="Previous12334Child(\'Pricefactor\', \''
		+ str(RECORD_ID)
		+ "','"
		+ str(table_id)
		+ '\')"><i class="fa fa-caret-left fnt14"></i>PREVIOUS</a></li><li class="disabled"><a href="#" \
		class="disabledPage" onclick="Next12334Child(\'Pricefactor\', \''
		+ str(RECORD_ID)
		+ "','"
		+ str(table_id)
		+ '\')">NEXT<i class="fa fa-caret-right fnt14"></i></a></li><li class="disabled"><a href="#" \
		onclick="LastPageLoad_paginationChild(\'Pricefactor\', \''
		+ str(RECORD_ID)
		+ "','"
		+ str(table_id)
		+ '\')" class="disabledPage"><i class="fa fa-caret-right fnt14"></i><i class="fa fa-caret-right fnt14bold" >\
		</i></a></li></ul></div> </div> <div class="col-md-4 pad3"> <span id="'
		+ str(table_id)
		+ '_page_count" class="currentPage page_right_content">1</span><span class="page_right_content padrt2" >Page\
		</span></div></div>'
	)

	return sap_list, Test


def StaticPERSONALIZATIONTableFormation(QST_REC_ID, Row_Count, Column_Count, Column_Names_List, New_CtrName):
	RecAttValue = Product.Attributes.GetByName("QSTN_SYSEFL_MA_00253").GetValue()
	dbl_clk_function = ""
	# table_header = '<table class="table table-bordered" id="'+str(New_CtrName)+'">'
	mac_map_Obj = Sql.GetList(
		"SELECT top 1000 mp.PERSONALIZATION_PLANT_MATERIAL_RECORD_ID, mp.PLANT_ID, mp.MATERIAL_RECORD_ID, \
		mp.PLANT_RECORD_ID, mp.PLANT_NAME, mp.SAP_PART_NUMBER from macpmp (NOLOCK) mp where mp.PERSONALIZATION_RECORD_ID = '"
		+ str(RecAttValue)
		+ "' order by mp.CpqTableEntryId desc"
	)
	# Mapeat_Obj = Sql.GetList("select top 1000 ATTRIBUTE_NAME from MAPEAT where PERSONALIZATION_RECORD_ID = '" +
	# str(RecAttValue) + "' order by CpqTableEntryId desc")
	table_id = "test_" + str(New_CtrName)
	table_ids = "#" + str(table_id)
	# table_header += '<tr>'
	acts = "Act_" + table_id
	# table_header += '<th class="column-with-actions-header">Actions</th>'
	table_header = (
		'<table id="'
		+ str(table_id)
		+ '" data-pagination="true" data-search-on-enter-key="true" data-filter-control="true" \
		data-maintain-selected="true" data-pagination-loop = "false" data-locale = "en-US" \
		data-page-list="[5, 10, 25, 50, 100, ALL]" data-page-size="5"><thead>'
	)
	table_header += "<tr>"
	table_header += (
		'<th data-field="ACTIONS"><div class="action_col">ACTIONS</div><button id="'
		+ str(acts)
		+ '" class="searched_button">Search</button></th>'
	)
	table_header += '<th data-field="SELECT" class="wth45" data-checkbox="true">SELECT</th>'
	for Names_dict in list(eval(Column_Names_List)):
		if str(Names_dict["API_METHOD"]) == "PERSONALIZATION_NAME":
			table_header += (
				'<th data-field="'
				+ str(Names_dict["API_METHOD"])
				+ '" data-formatter="PLANTPOPUPtHyperLink" data-filter-control="input" data-sortable="true"><abbr title="'
				+ str(Names_dict["FIELD_NAME"])
				+ '">'
				+ str(Names_dict["FIELD_NAME"])
				+ "</abbr></th>"
			)

		elif str(Names_dict["API_METHOD"]) == "PLANT_ID":
			table_header += (
				'<th data-field="'
				+ str(Names_dict["API_METHOD"])
				+ '" data-formatter="PLANTIDtHyperLink" data-filter-control="input" data-sortable="true"><abbr title="'
				+ str(Names_dict["FIELD_NAME"])
				+ '">'
				+ str(Names_dict["FIELD_NAME"])
				+ "</abbr></th>"
			)
		elif str(Names_dict["API_METHOD"]) == "SAP_PART_NUMBER":
			table_header += (
				'<th data-field="'
				+ str(Names_dict["API_METHOD"])
				+ '" data-formatter="SAP_PART_NUMBERtHyperLink" data-filter-control="input" data-sortable="true">\
				<abbr title="'
				+ str(Names_dict["FIELD_NAME"])
				+ '">'
				+ str(Names_dict["FIELD_NAME"])
				+ "</abbr></th>"
			)
			table_header += (
				'<th data-field="SAP_DESCRIPTION" data-filter-control="input" data-sortable="true">SAP DESCRIPTION</th>'
			)
		else:
			table_header += (
				'<th data-field="'
				+ str(Names_dict["API_METHOD"])
				+ '" data-filter-control="input" data-sortable="true"><abbr title="'
				+ str(Names_dict["FIELD_NAME"])
				+ '">'
				+ str(Names_dict["FIELD_NAME"])
				+ "</abbr></th>"
			)
	table_header += '<th data-field="plant_detils" data-show-header="false"</th>'
	table_header += '<th data-field="sap_detils" data-show-header="false"</th>'
	Mapeat_Obj = Sql.GetList(
		"select top 1000 ATTRIBUTE_NAME from MAPEAT (NOLOCK) where ATTRIBUTE_NAME <> '' and ATTRIBUTE_TYPE = \
		'PERSONALIZATION ATTRIBUTE' and ATTRIBUTE_TYPE = 'PERSONALIZATION ATTRIBUTE' and PERSONALIZATION_RECORD_ID = '"
		+ str(RecAttValue)
		+ "' order by CpqTableEntryId desc"
	)
	for ins in Mapeat_Obj:
		a_name = ins.ATTRIBUTE_NAME.replace(" ", "_")
		table_header += (
			'<th data-field="'
			+ str(a_name)
			+ '" data-filter-control="input" data-sortable="true"><abbr title="'
			+ str(ins.ATTRIBUTE_NAME)
			+ '">'
			+ str(ins.ATTRIBUTE_NAME)
			+ "</abbr></th>"
		)
	exp_list = [str(ikh.ATTRIBUTE_NAME) for ikh in Mapeat_Obj]
	expd_list = [str(ikhd.ATTRIBUTE_NAME.replace(" ", "_")) for ikhd in Mapeat_Obj]
	table_header += "</tr>"
	pop_list = []
	for keys, Dins in enumerate(mac_map_Obj):
		pop_val = {}
		mam_obj = Sql.GetFirst(
			"select MATERIAL_RECORD_ID, SAP_DESCRIPTION from MAMTRL (NOLOCK) where SAP_PART_NUMBER = '"
			+ str(Dins.SAP_PART_NUMBER)
			+ "'"
		)
		MATERIAL_RECORD_ID = ""
		SAP_DESCRIPTION = ""
		if mam_obj is not None:
			SAP_DESCRIPTION = mam_obj.SAP_DESCRIPTION
			MATERIAL_RECORD_ID = mam_obj.MATERIAL_RECORD_ID
		pop_val[
			"ACTIONS"
		] = '<div class="btn-group dropdown"><div class="dropdown" id="ctr_drop"><i data-toggle="dropdown" \
		id="dropdownMenuButton" class="fa fa-sort-desc dropdown-toggle" aria-expanded="false"></i><ul \
		class="dropdown-menu left" aria-labelledby="dropdownMenuButton"><li><a class="dropdown-item" \
		href="#" data-target="#cont_viewModalSection" onclick="cont_PERSONALIZEopenview(this, \'PERSONALIZATION\')" \
		data-toggle="modal">VIEW</a></li><li><a class="dropdown-item" href="#" onclick="cont_PERSONALIZEopenedit\
		(this, \'PERSONALIZATION\')" data-target="#cont_viewModalSection" data-toggle="modal">EDIT</a></li>\
		<li><a class="dropdown-item" data-target="#Personalization_delete_modal" data-toggle="modal" \
		onclick="cont_PERSONALIZEdelete(this, \'PERSONALIZATION\')" href="#">DELETE</a></li></ul></div></div>'
		# pop_val['SELECT'] = ''
		pop_val["PERSONALIZATION_NAME"] = str(Dins.PERSONALIZATION_PLANT_MATERIAL_RECORD_ID)
		pop_val["PLANT_ID"] = str(Dins.PLANT_ID)
		pop_val["PLANT_NAME"] = str(Dins.PLANT_NAME)
		pop_val["SAP_PART_NUMBER"] = str(Dins.SAP_PART_NUMBER)
		pop_val["SAP_DESCRIPTION"] = SAP_DESCRIPTION
		pop_val["plant_detils"] = str(Dins.PLANT_RECORD_ID) + "|" + "Plants"
		pop_val["sap_detils"] = str(MATERIAL_RECORD_ID) + "|" + "Materials"
		for inh in exp_list:
			a_name = inh.replace(" ", "_")
			Qstr = (
				"select top 1000 ATTRIBUTE_NAME, SAP_PART_NUMBER, ATTVAL_VALDISPLAY from mappma (NOLOCK) \
				where PERSONALIZATION_RECORD_ID = '"
				+ str(RecAttValue)
				+ "' and PLANT_ID = '"
				+ str(Dins.PLANT_ID)
				+ "' and SAP_PART_NUMBER = '"
				+ str(Dins.SAP_PART_NUMBER)
				+ "' and ATTRIBUTE_NAME = '"
				+ str(inh)
				+ "' order by CpqTableEntryId desc"
			)
			Test_Obj = Sql.GetFirst(Qstr)
			val = ""
			if Test_Obj is not None:
				val = str(Test_Obj.ATTVAL_VALDISPLAY) or ""
				pop_val[str(a_name)] = val
			else:
				pop_val[str(a_name)] = ""
		pop_list.append(pop_val)
	table_header += "</thead>"
	table_header += "</table>"
	cls = "eq(2)"
	dbl_clk_function += (
		'var checkedRows=[]; $("'
		+ str(table_ids)
		+ '").on("check.bs.table", function (e, row, $element) { checkedRows.push($element.closest("tr").find("td:'
		+ str(cls)
		+ '").text()); localStorage.setItem("multiedit_checkbox_clicked", checkedRows); }); $("'
		+ str(table_ids)
		+ '").on("check-all.bs.table", function (e) { var table = $("'
		+ str(table_ids)
		+ '").closest("table"); table.find("tbody tr").each(function() { checkedRows.push($(this).\
		find("td:nth-child(3)").text()); }); localStorage.setItem("multiedit_checkbox_clicked", checkedRows); }); $("'
		+ str(table_ids)
		+ '").on("uncheck-all.bs.table", function (e) { localStorage.setItem\
		("multiedit_checkbox_clicked", ""); checkedRows=[]; }); $("'
		+ str(table_ids)
		+ '").on("uncheck.bs.table", function (e, row, $element) { \
		var rec_ids=$element.closest("tr").find("td:'
		+ str(cls)
		+ '").text(); $.each(checkedRows, function(index, value) { if (value === rec_ids) { \
		checkedRows.splice(index,1); }}); localStorage.setItem("multiedit_checkbox_clicked", checkedRows); });'
	)

	dbl_clk_function += (
		'$("'
		+ str(table_ids)
		+ '").on("dbl-click-cell.bs.table", onClickCell); $("'
		+ str(table_ids)
		+ '\ th.bs-checkbox div.th-inner").before("<div class=\'pad0brdbt\'>SELECT</div>"); $\
		(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); \
		function onClickCell(event, field, value, row, $element) {  var reco_id=""; var reco = []; var asd = eval('
		+ str(expd_list)
		+ '); reco = localStorage.getItem("multiedit_checkbox_clicked"); if (reco == \'\') { reco = \
		row.PERSONALIZATION_NAME; localStorage.setItem("multiedit_checkbox_clicked", reco); }if \
		( asd.indexOf(field) > -1 ) { localStorage.setItem("AttrBulk", field); if (reco.length > 0){ \
		reco = reco.split(","); reco_id = removeDuplicates(reco); localStorage.\
		setItem("multiedit_checkbox_clickeds", "" ); }  reco_ids = row.PERSONALIZATION_NAME; \
		localStorage.setItem("multiedit_checkbox_clickeds", reco_ids);  cpq.server.executeScript\
		("SYLDCTNPTL", {"ContainerType":"DYNAMIC ROWS","Row_Count": field,"New_CtrName": \
		"PERSONALIZATION_POPUP", "Column_Count": "mappma","SQL_Expression":"","Column_Names_List": reco_id }, \
		function(dataset) {  if(document.getElementById("RL_EDIT_DIV_ID") ) { document.getElementById\
		("RL_EDIT_DIV_ID").innerHTML = dataset; document.getElementById("cont_multiEditModalSection").\
		style.display = "block"; } });  } }'
	)
	filter_control_function = ""
	values_list = ""
	expd_lists = ""
	#Trace.Write("expd_lists0--" + str(expd_lists))
	#Trace.Write("expd_list0--" + str(expd_list))
	expd_lists = [str(inv["API_METHOD"]) for inv in list(eval(Column_Names_List))] + expd_list
	#Trace.Write("expd_lists--" + str(expd_lists))
	#Trace.Write("expd_list--" + str(expd_list))
	for invs in expd_lists:
		table_ids = "#" + str(table_id)
		# LogInfo("4 str(invs) -- "+str(invs))
		filter_clas = "#" + str(table_id) + " .bootstrap-table-filter-control-" + str(invs)
		values_list += "var " + str(invs) + ' = $("' + str(filter_clas) + '").val(); '
		values_list += " ATTRIBUTE_VALUEList.push(" + str(invs) + "); "
	filter_class = "#Act_" + str(table_id)
	filter_control_function += (
		'$("'
		+ filter_class
		+ '").click( function(){ var table_id = $(this).closest("table").attr("id"); var a_list = '
		+ str(expd_lists)
		+ ";   ATTRIBUTE_VALUEList = []; "
		+ str(values_list)
		+ ' var attribute_value = $(this).val();cpq.server.executeScript("SYLDCTNPTL", \
		{"REC_ID":table_id, "ATTRIBUTE_NAME": '
		+ str(expd_lists)
		+ ', "Column_Names_List": ATTRIBUTE_VALUEList, "New_CtrName" : "PERSONALIZATION_PIVOT_FILTER", \
		"ContainerType": "DYNAMIC ROWS" , "SQL_Expression": "", "Row_Count":"PERSONALIZATION", \
		"Column_Count":""}, function(data) { $("'
		+ str(table_ids)
		+ '").bootstrapTable("load", data ); });  });'
	)
	#Trace.Write("ssssssscccccccc" + str(filter_control_function))
	filter_control_function += (
		' try { setTimeout(function(){ $("#'
		+ str(table_id)
		+ '").colResizable({ resizeMode: "overflow",liveDrag: true, gripInnerHtml: "<div class=\'grip2\'>\
		</div>", draggingClass: "dragging"  }); }, 5000); } catch (err) { setTimeout(function(){ $("#'
		+ str(table_id)
		+ '").colResizable({ resizeMode: "overflow",liveDrag: true, gripInnerHtml: "<div class=\'grip2\'>\
		</div>", draggingClass: "dragging"  });}, 3000);  } '
	)
	return table_header, pop_list, table_id, dbl_clk_function, filter_control_function


def StaticPLANTTableFormation(
	QST_REC_ID, Row_Count, Column_Count, Column_Names_List, New_CtrName, PerPage, PageInform,
):
	#RecAttValue = Product.Attributes.GetByName("QSTN_SYSEFL_MA_00252").GetValue()
	dbl_clk_function = ""
	Page_start = ""
	QueryCount = ""
	Page_End = ""
	if str(PerPage) == "" and str(PageInform) == "":
		Page_start = 1
		Page_End = 10
		PerPage = 10
		PageInform = "1___10___10"
	else:
		Page_start = int(PageInform.split("___")[0])
		Page_End = int(PageInform.split("___")[1])
		PerPage = PerPage
	# table_header = '<table class="table table-bordered" id="'+str(New_CtrName)+'">'
	xc_Str = (
		"select distinct(ATTRIBUTE_NAME) from MAPEAT (NOLOCK) where ATTRIBUTE_NAME <> '' and ATTRIBUTE_TYPE = \
		'PERSONALIZATION ATTRIBUTE' and PERSONALIZATION_RECORD_ID in (select PERSONALIZATION_RECORD_ID from \
		MAPLPE (NOLOCK) where PLANT_RECORD_ID = '"
		+ str(RecAttValue)
		+ "')"
	)
	# mac_map_Obj = Sql.GetList("SELECT top 1000 mp.PERSONALIZATION_PLANT_MATERIAL_RECORD_ID, \
	# mp.PERSONALIZATION_NAME, mp.PLANT_ID,mp.PERSONALIZATION_TYPE, mp.PERSONALIZATION_RECORD_ID, \
	# mp.MATERIAL_RECORD_ID, mp.PLANT_RECORD_ID, mp.PLANT_NAME, mp.SAP_PART_NUMBER from macpmp mp where \
	# mp.PLANT_RECORD_ID = '"+ str(RecAttValue) +"' order by mp.CpqTableEntryId desc")
	Qstr = (
		"select top "
		+ str(PerPage)
		+ " * from (SELECT ROW_NUMBER() OVER( order by PERSONALIZATION_PLANT_MATERIAL_RECORD_ID) AS ROW, * \
		from macpmp (NOLOCK) mp where mp.PLANT_RECORD_ID = '"
		+ str(RecAttValue)
		+ "') m where m.ROW BETWEEN "
		+ str(Page_start)
		+ " and "
		+ str(Page_End)
		+ ""
	)

	#Trace.Write("Qstr_______Qstr----->"+str(Qstr))
	mac_map_Obj = Sql.GetList(Qstr)
	mac_map_CountObj = Sql.GetFirst(
		"SELECT count(mp.PERSONALIZATION_PLANT_MATERIAL_RECORD_ID) as cnt from macpmp (NOLOCK) mp \
		where mp.PLANT_RECORD_ID = '"
		+ str(RecAttValue)
		+ "'"
	)
	#Trace.Write(str(Qstr) + "SSSSSSSSSSSSSSSSSSSSKKKKKKKKKKKKKKK")
	if mac_map_CountObj is not None:
		QueryCount = mac_map_CountObj.cnt
	Mapeat_Obj = Sql.GetList(xc_Str)
	table_id = "test_" + str(New_CtrName)
	table_ids = "#" + str(table_id)
	acts = "Act_" + table_id
	# table_header += '<tr>'
	# table_header += '<th class="column-with-actions-header">Actions</th>'
	table_header = (
		'<table id="'
		+ str(table_id)
		+ '" data-search-on-enter-key="true" data-filter-control="true" data-maintain-selected="true" \
		data-locale = "en-US"><thead>'
	)
	table_header += "<tr>"
	table_header += (
		'<th data-toggle="tooltip" data-title-tooltip="ACTIONS" data-field="ACTIONS"><div class="action_col">\
		ACTIONS</div><button id="'
		+ str(acts)
		+ '" class="searched_button">Search</button></th>'
	)
	table_header += '<th class="wth45" data-toggle="tooltip" data-title-tooltip="SELECT" data-field="SELECT" \
	data-checkbox="true">SELECT</th>'
	#Trace.Write(str(type(Column_Names_List))+'SSSSSSSSSS11111111111111'+str(Column_Names_List))
	for Names_dict in list(eval(Column_Names_List)):
		if str(Names_dict["API_METHOD"]) == "PERSONALIZATION_NAME":
			table_header += (
				'<th data-toggle="tooltip" data-field="'
				+ str(Names_dict["API_METHOD"])
				+ '" data-formatter="PLANTPoptHyperLink" data-filter-control="input" data-title-tooltip="'
				+ str(Names_dict["FIELD_NAME"])
				+ '" data-sortable="true">'
				+ str(Names_dict["FIELD_NAME"])
				+ "</th>"
			)

		elif str(Names_dict["API_METHOD"]) == "PLANT_ID":
			table_header += (
				'<th data-toggle="tooltip"  data-field="'
				+ str(Names_dict["API_METHOD"])
				+ '" data-formatter="PLANTIDtHyperLink" data-filter-control="input" data-title-tooltip="'
				+ str(Names_dict["FIELD_NAME"])
				+ '" data-sortable="true">'
				+ str(Names_dict["FIELD_NAME"])
				+ "</th>"
			)
		elif str(Names_dict["API_METHOD"]) == "SAP_PART_NUMBER":
			table_header += (
				'<th data-toggle="tooltip"  data-field="'
				+ str(Names_dict["API_METHOD"])
				+ '" data-formatter="SAP_PART_NUMBERtHyperLink" data-filter-control="input" data-title-tooltip="'
				+ str(Names_dict["FIELD_NAME"])
				+ '" data-sortable="true">'
				+ str(Names_dict["FIELD_NAME"])
				+ "</th>"
			)
			table_header += (
				'<th data-toggle="tooltip"  data-title-tooltip="'
				+ str(Names_dict["FIELD_NAME"])
				+ '" data-field="SAP_DESCRIPTION" data-filter-control="input" data-sortable="true">SAP DESCRIPTION</th>'
			)
		else:
			table_header += (
				'<th data-toggle="tooltip" data-title-tooltip="'
				+ str(Names_dict["FIELD_NAME"])
				+ '" data-field="'
				+ str(Names_dict["API_METHOD"])
				+ '" data-filter-control="input" data-sortable="true">'
				+ str(Names_dict["FIELD_NAME"])
				+ "</th>"
			)
	table_header += '<th data-field="plant_detils" data-show-header="false"</th>'
	table_header += '<th data-field="sap_detils" data-show-header="false"</th>'
	# Mapeat_Obj = Sql.GetList("select top 1000 ATTRIBUTE_NAME from MAPEAT where PERSONALIZATION_RECORD_ID = '" +  \
	# str(RecAttValue) + "' order by CpqTableEntryId desc")
	for ins in Mapeat_Obj:
		a_name = ins.ATTRIBUTE_NAME.replace(" ", "_")
		table_header += (
			'<th data-toggle="tooltip" data-field="'
			+ str(a_name)
			+ '" data-title-tooltip="'
			+ str(ins.ATTRIBUTE_NAME)
			+ '" data-filter-control="input" data-sortable="true">'
			+ str(ins.ATTRIBUTE_NAME)
			+ "</th>"
		)
	exp_list = [str(ikh.ATTRIBUTE_NAME) for ikh in Mapeat_Obj]
	expd_list = [str(ikhd.ATTRIBUTE_NAME.replace(" ", "_")) for ikhd in Mapeat_Obj]
	expds_list = [str(inv["API_METHOD"]) for inv in list(eval(Column_Names_List))] + expd_list
	table_header += "</tr>"
	pop_list = []
	for keys, Dins in enumerate(mac_map_Obj):
		pop_val = {}
		sap_desc = ""
		mam_obj = Sql.GetFirst(
			"select MATERIAL_RECORD_ID, SAP_DESCRIPTION from MAMTRL (NOLOCK) where SAP_PART_NUMBER = '"
			+ str(Dins.SAP_PART_NUMBER)
			+ "'"
		)
		MATERIAL_RECORD_ID = ""
		if mam_obj is not None:
			MATERIAL_RECORD_ID = mam_obj.MATERIAL_RECORD_ID
			sap_desc = mam_obj.SAP_DESCRIPTION
		pop_val[
			"ACTIONS"
		] = '<div class="btn-group dropdown"><div class="dropdown" id="ctr_drop"><i data-toggle="dropdown" \
		id="dropdownMenuButton" class="fa fa-sort-desc dropdown-toggle" aria-expanded="false"></i><ul \
		class="dropdown-menu left" aria-labelledby="dropdownMenuButton"><li><a class="dropdown-item" \
		href="#" data-target="#cont_viewModalSection" onclick="cont_PERSONALIZEopenview(this, \'PLANT\')" \
		data-toggle="modal">VIEW</a></li><li><a class="dropdown-item" href="#" onclick="cont_PERSONALIZEopenedit\
		(this, \'PLANT\')" data-target="#cont_viewModalSection" data-toggle="modal">EDIT</a></li><li><a \
		data-target="#Personalization_delete_modal" data-toggle="modal" class="dropdown-item" \
		onclick="cont_PERSONALIZEdelete(this, \'PLANT\')" href="#">DELETE</a></li></ul></div></div>'
		# pop_val['SELECT'] = ''
		Record_ID = str("MACPMP-" + str(Dins.CpqTableEntryId).zfill(5))
		#pop_val["PERSONALIZATION_NAME"] = str(Dins.PERSONALIZATION_PLANT_MATERIAL_RECORD_ID)

		pop_val["PERSONALIZATION_NAME"] = str(Record_ID)
		pop_val["PLANT_ID"] = str(Dins.PERSONALIZATION_NAME)
		pop_val["PLANT_NAME"] = str(Dins.PERSONALIZATION_TYPE)
		pop_val["SAP_PART_NUMBER"] = str(Dins.SAP_PART_NUMBER)
		pop_val["SAP_DESCRIPTION"] = sap_desc
		pop_val["plant_detils"] = str(Dins.PERSONALIZATION_RECORD_ID) + "|" + "Personalizations"
		pop_val["sap_detils"] = str(MATERIAL_RECORD_ID) + "|" + "Materials"
		for inh in exp_list:
			a_name = inh.replace(" ", "_")
			if inh.find("'"):
				inh = inh.replace("'", "''")
			Qstr = (
				"select top 1000 ATTRIBUTE_NAME, SAP_PART_NUMBER, ATTVAL_VALDISPLAY from mappma (NOLOCK) \
				where PERSONALIZATION_RECORD_ID = '"
				+ str(Dins.PERSONALIZATION_RECORD_ID)
				+ "' and PLANT_RECORD_ID = '"
				+ str(RecAttValue)
				+ "' and SAP_PART_NUMBER = '"
				+ str(Dins.SAP_PART_NUMBER)
				+ "' and ATTRIBUTE_NAME = '"
				+ str(inh)
				+ "' order by CpqTableEntryId desc"
			)
			Test_Obj = Sql.GetFirst(Qstr)
			val = ""
			if Test_Obj is not None:
				val = str(Test_Obj.ATTVAL_VALDISPLAY) or ""
				pop_val[str(a_name)] = val
			else:
				pop_val[str(a_name)] = ""
		pop_list.append(pop_val)
	table_header += '</thead><tbody onclick="Table_Onclick_Scroll(this)"></tbody>'
	table_header += "</table>"
	cls = "eq(2)"
	dbl_clk_function += (
		'var checkedRows=[]; $("'
		+ str(table_ids)
		+ '").on("check.bs.table", function (e, row, $element) { checkedRows.push($element.closest("tr").find("td:'
		+ str(cls)
		+ '").text());  localStorage.setItem("multiedit_checkbox_clicked", checkedRows); }); $("'
		+ str(table_ids)
		+ '").on("check-all.bs.table", function (e) { var table = $("'
		+ str(table_ids)
		+ '").closest("table"); table.find("tbody tr").each(function() { checkedRows.push($(this).\
		find("td:nth-child(3)").text()); }); localStorage.setItem("multiedit_checkbox_clicked", checkedRows); }); $("'
		+ str(table_ids)
		+ '").on("uncheck-all.bs.table", function (e) { localStorage.setItem("multiedit_checkbox_clicked", "");\
		 checkedRows=[]; }); $("'
		+ str(table_ids)
		+ '").on("uncheck.bs.table", function (e, row, $element) { var rec_ids=$element.closest("tr").find("td:'
		+ str(cls)
		+ '").text(); $.each(checkedRows, function(index, value) { if (value === rec_ids) { \
		checkedRows.splice(index,1); }}); localStorage.setItem("multiedit_checkbox_clicked", checkedRows); });'
	)
	dbl_clk_function += (
		'$("'
		+ str(table_ids)
		+ '").on("dbl-click-cell.bs.table", onClickCell); $("'
		+ str(table_ids)
		+ '\ th.bs-checkbox div.th-inner").before("<div class=\'pad0brdbt\'>SELECT</div>"); $(".bs-checkbox input").\
		addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); function onClickCell\
		(event, field, value, row, $element) {  var reco_id=""; var reco = []; var asd = eval('
		+ str(expd_list)
		+ '); reco = localStorage.getItem("multiedit_checkbox_clicked"); if (reco == \'\') { \
		reco = row.PERSONALIZATION_NAME; localStorage.setItem("multiedit_checkbox_clicked", reco); } if ( \
		asd.indexOf(field) > -1 ) { localStorage.setItem("AttrBulk", field); if (reco.length > 0){ reco = \
		reco.split(","); reco_id = removeDuplicates(reco); localStorage.setItem("multiedit_checkbox_clickeds", "" ); }  \
		reco_ids = row.PERSONALIZATION_NAME; localStorage.setItem("multiedit_checkbox_clickeds", reco_ids); \
		cpq.server.executeScript("SYLDCTNPTL", {"ContainerType":"DYNAMIC ROWS","Row_Count": field,"New_CtrName": \
		"PERSONALIZATION_POPUP", "Column_Count": "mappma","SQL_Expression":"","Column_Names_List": reco_id }, \
		function(dataset) {  if(document.getElementById("RL_EDIT_DIV_ID") ) { document.getElementById\
		("RL_EDIT_DIV_ID").innerHTML = dataset; document.getElementById("cont_multiEditModalSection").\
		style.display = "block"; } });  } }'
	)
	filter_control_function = ""
	values_list = ""
	for invs in expds_list:
		table_ids = "#" + str(table_id)
		# LogInfo("5 str(invs) -- "+str(invs))
		filter_clas = "#" + str(table_id) + " .bootstrap-table-filter-control-" + str(invs)
		values_list += "var " + str(invs) + ' = $("' + str(filter_clas) + '").val(); '
		values_list += " ATTRIBUTE_VALUEList.push(" + str(invs) + "); "
	filter_class = "#Act_" + str(table_id)
	filter_control_function += (
		'$("'
		+ filter_class
		+ '").click( function(){ var table_id = $(this).closest("table").attr("id"); var a_list = '
		+ str(expds_list)
		+ ";   ATTRIBUTE_VALUEList = []; "
		+ str(values_list)
		+ ' var attribute_value = $(this).val();  cpq.server.executeScript("SYLDCTNPTL", {"REC_ID":table_id, \
		"ATTRIBUTE_NAME": a_list, "Column_Names_List": ATTRIBUTE_VALUEList, "New_CtrName" : \
		"PPLANT_PIVOT_FILTER", "ContainerType": "DYNAMIC ROWS" , "SQL_Expression": "", "Row_Count":"PLANT", \
		"Column_Count":""}, function(data) { if(data.length > 0){ $("'
		+ str(table_ids)
		+ '").bootstrapTable("load", data ); }else{ $("'
		+ str(table_ids)
		+ 'tbody" ).html(\'<tr class="noRecordFound"><td colspan="7" class="txt_al_lft">No Records to Display</td>\
		</tr>\'); } }); });'
	)
	"""filter_control_function += '$(\"'+filter_class+'\").click( function(){ var table_id = $(this).closest(\"table\").
	attr(\"id\"); var a_list = '+str(expds_list)+';   ATTRIBUTE_VALUEList = []; '+str(values_list)+' var attribute_value = 
	$(this).val();  cpq.server.executeScript("SYLDCTNPTL", {"REC_ID":table_id, "ATTRIBUTE_NAME": a_list, 
	"Column_Names_List": ATTRIBUTE_VALUEList, "New_CtrName" : "PPLANT_PIVOT_FILTER", "ContainerType": "DYNAMIC ROWS" , 
	"SQL_Expression": "", "Row_Count":"PLANT", "Column_Count":""}, function(data) { 
	$(\"'+str(table_ids) +'\").bootstrapTable(\"load\", data ); }); });"""
	filter_control_function += (
		'setTimeout(function(){ $("#' + str(table_id) + '").colResizable({ resizeMode:"overflow"});}, 5000);'
	)
	RECORD_ID = ""
	if QueryCount < int(Page_End):
		PageInformS = str(Page_start) + " - " + str(QueryCount) + " of"
	else:
		PageInformS = str(Page_start) + " - " + str(Page_End) + " of"
	Test = (
		'<div class="col-md-12 brdr listContStyle padbthgt30"><div class="col-md-4 pager-numberofitem  clear-padding">\
		<span class="pager-number-of-items-item flt_lt_pad2_mar2022" id="'
		+ str(table_id)
		+ '_NumberofItem">'
		+ str(PageInformS)
		+ ' </span><span class="pager-number-of-items-item flt_lt_pad2_mar" id="'
		+ str(table_id)
		+ '_totalItemCount" >'
		+ str(QueryCount)
		+ '</span><div class="clear-padding fltltmrgtp3"><div class="pull-right vralign"><select onchange=\
		"PageFunctestChild(this, \'PLANT_RelatedList\',\''
		+ str(RECORD_ID)
		+ "','"
		+ str(table_id)
		+ '\')" id="'
		+ str(table_id)
		+ '_PageCountValue" class="form-control selcwdt"><option value="10">10</option><option value="20" selected>20\
		</option><option value="50">50</option><option value="100">100</option><option value="200">200</option>\
		</select> </div></div></div><div class="col-xs-8 col-md-4  clear-padding inpadtex" data-bind=\
		"visible: totalItemCount"><div class="clear-padding col-xs-12 col-sm-6 col-md-12 brd0">\
		<ul class="pagination pagination"><li class="disabled"><a href="#" onclick="FirstPageLoad_paginationChild\
		(\'PLANT_RelatedList\', \''
		+ str(RECORD_ID)
		+ "','"
		+ str(table_id)
		+ '\')"><i class="fa fa-caret-left fnt14bold"></i><i class="fa fa-caret-left fnt14"></i></a></li><li \
		class="disabled"><a href="#" onclick="Previous12334Child(\'PLANT_RelatedList\', \''
		+ str(RECORD_ID)
		+ "','"
		+ str(table_id)
		+ '\')"><i class="fa fa-caret-left fnt14"></i>PREVIOUS</a></li><li class="disabled"><a href="#" \
		class="disabledPage" onclick="Next12334Child(\'PLANT_RelatedList\', \''
		+ str(RECORD_ID)
		+ "','"
		+ str(table_id)
		+ '\')">NEXT<i class="fa fa-caret-right fnt14"></i></a></li><li class="disabled"><a href="#" \
		onclick="LastPageLoad_paginationChild(\'PLANT_RelatedList\', \''
		+ str(RECORD_ID)
		+ "','"
		+ str(table_id)
		+ '\')" class="disabledPage"><i class="fa fa-caret-right fnt14"></i><i class="fa fa-caret-right fnt14bold" >\
		</i></a></li></ul></div> </div> <div class="col-md-4 pad3"> <span id="'
		+ str(table_id)
		+ '_page_count" class="currentPage page_right_content">1</span><span class="page_right_content padrt2">Page </span>\
		</div></div>'
	)
	filter_control_function += (
		' try { setTimeout(function(){ $("#'
		+ str(table_id)
		+ '").colResizable({ resizeMode: "overflow",liveDrag: true, gripInnerHtml: "<div class=\'grip2\'></div>", \
		draggingClass: "dragging"  }); }, 5000); } catch (err) { setTimeout(function(){ $("#'
		+ str(table_id)
		+ '").colResizable({ resizeMode: "overflow",liveDrag: true, gripInnerHtml: "<div class=\'grip2\'></div>", \
		draggingClass: "dragging"  });}, 3000);  } '
	)
	#Trace.Write("pop_list____pop_list"+str(pop_list))
	return (
		table_header,
		pop_list,
		table_id,
		dbl_clk_function,
		filter_control_function,
		Test,
		PageInform,
		PageInformS,
		QueryCount,
	)


def StaticPERSONALIZATION_POPUP(QST_REC_ID, Row_Count, Column_Count, Column_Names_List, New_CtrName):
	field_lable = Row_Count
	a_attr = field_lable.replace("_", " ")
	selection = '<select class="form-control" id="VALUE_CODE">'
	selection += "</select>"
	RECORDID = Column_Names_List
	if RECORDID != "":
		RECORDID_len = str(len(list(RECORDID))) + " " + "selected"
	else:
		RECORDID_len = ""
	edt_str = (
		'<div class="row modulebnr brdr ma_mar_btm">EDIT '
		+ str(a_attr).upper()
		+ ' <button type="button" class="close flt_rt" onclick="multiedit_RL_cancel();">X</button></div>'
	)
	edt_str += (
		'<div id="container" class="g4 pad-10 brdr except_sec"><table class="width100" id="bulk_edit"><tbody><tr \
		class="fieldRow"><td class="labelCol wid50_pot_ali_font">Value Code</td><td class="dataCol"><div \
		id="massEditFieldDiv" class="inlineEditRequiredDiv">'
		+ str(selection)
		+ '</div></td></tr><tr class="selectionRow"><td class="labelCol wid50_pot_ali_font">Apply changes to</td>\
		<td class="dataCol"><div class="radio"><input type="radio" name="massOrSingleEdit" id="singleEditRadio" \
		checked="checked"><label for="singleEditRadio">The record clicked</label></div>'
	)
	if len(list(RECORDID)) != 0:
		edt_str += (
			'<div class="radio"><input type="radio" name="massOrSingleEdit" id="massEditRadio"><label \
			for="massEditRadio">All '
			+ str(RECORDID_len)
			+ " records</label></div>"
		)
	# JIRA ID 6722 CODE START
	# CHANGED THE BUTTON FORMAT FROM SAVE AND CANCEL TO CANCEL AND SAVE
	edt_str += '</td></tr></tbody></table><div class="row pad-10"><button class="btnstyle mrg-rt-8 btn" \
	onclick="multiedit_RL_cancel();" type="button" value="Cancel" id="cancelButton">CANCEL</button>\
	<button class="btnstyle mrg-rt-8 btn" type="button" value="Save" onclick=\
	"multiedit_PERSONALIZATION_Save(this)" id="saveButton">SAVE</button></div></div>'
	# JIRA ID 6722 CODE END
	# CHANGED THE BUTTON FORMAT FROM SAVE AND CANCEL TO CANCEL AND SAVE
	# edt_str+='</div>'
	return edt_str


def PERSONALIZATION_PIVOT_FILTER(QST_REC_ID, Row_Count, Column_Count, Column_Names_List, New_CtrName, ATTRIBUTE_NAME):
	Column_Names_List = list(Column_Names_List)
	x_Column_Names_List = Column_Names_List[4:]
	ATTRIBUTE_NAME = list(ATTRIBUTE_NAME)
	x_ATTRIBUTE_NAME = ATTRIBUTE_NAME[4:]
	x_dict = dict(zip(ATTRIBUTE_NAME, Column_Names_List))
	xx_dict = dict(zip(x_ATTRIBUTE_NAME, x_Column_Names_List))
	xx_dict = {value: xx_dict.get(value) for key, value in enumerate(xx_dict) if xx_dict.get(value) != ""}
	x_dict = dict(zip(ATTRIBUTE_NAME, Column_Names_List))
	RecAttValue = Product.Attributes.GetByName("QSTN_SYSEFL_MA_00253").GetValue()
	where = "mp.PERSONALIZATION_RECORD_ID like '%" + str(RecAttValue) + "%'"
	if Column_Names_List[0] != "":
		where += " and mp.PERSONALIZATION_PLANT_MATERIAL_RECORD_ID like '%" + str(Column_Names_List[0]) + "%'"
	if Column_Names_List[1] != "":
		where += " and mp.PLANT_ID like '%" + str(Column_Names_List[1]) + "%'"
	if Column_Names_List[2] != "":
		where += " and mp.PLANT_NAME like '%" + str(Column_Names_List[2]) + "%'"
	if Column_Names_List[3] != "":
		where += " and mp.SAP_PART_NUMBER like '%" + str(Column_Names_List[3]) + "%'"
	Mapeat_Obj = Sql.GetList(
		"select top 1000 ATTRIBUTE_NAME from MAPEAT (NOLOCK) where ATTRIBUTE_NAME <> '' and \
		ATTRIBUTE_TYPE = 'PERSONALIZATION ATTRIBUTE' and PERSONALIZATION_RECORD_ID = '"
		+ str(RecAttValue)
		+ "' order by CpqTableEntryId desc"
	)
	exp_list = [str(ikhd.ATTRIBUTE_NAME) for ikhd in Mapeat_Obj]
	Qstr = (
		"SELECT top 1000 mp.PERSONALIZATION_PLANT_MATERIAL_RECORD_ID, mp.PLANT_ID, mp.MATERIAL_RECORD_ID, \
		mp.PLANT_RECORD_ID, mp.PLANT_NAME, mp.SAP_PART_NUMBER from macpmp (NOLOCK) mp where "
		+ str(where)
		+ " order by mp.CpqTableEntryId desc"
	)
	mac_map_Obj = Sql.GetList(Qstr)
	bundle_list = []
	if mac_map_Obj is not None:
		for inh in mac_map_Obj:
			a_dict = {}
			a_dict[
				"ACTIONS"
			] = '<div class="btn-group dropdown"><div class="dropdown" id="ctr_drop"><i data-toggle="dropdown" \
			id="dropdownMenuButton" class="fa fa-sort-desc dropdown-toggle" aria-expanded="false"></i><ul \
			class="dropdown-menu left" aria-labelledby="dropdownMenuButton"><li><a class="dropdown-item" href="#" \
			data-target="#cont_viewModalSection" onclick="cont_PERSONALIZEopenview(this, \'PERSONALIZATION\')" \
			data-toggle="modal">VIEW</a></li><li><a class="dropdown-item" href="#" \
			onclick="cont_PERSONALIZEopenedit(this, \'PERSONALIZATION\')" data-target="#cont_viewModalSection" \
			data-toggle="modal">EDIT</a></li><li><a class="dropdown-item" onclick="cont_PERSONALIZEdelete\
			(this, \'PERSONALIZATION\')" href="#">DELETE</a></li></ul></div></div>'
			a_dict["PERSONALIZATION_NAME"] = inh.PERSONALIZATION_PLANT_MATERIAL_RECORD_ID
			a_dict["PLANT_ID"] = inh.PLANT_ID
			a_dict["PLANT_NAME"] = inh.PLANT_NAME
			a_dict["SAP_PART_NUMBER"] = inh.SAP_PART_NUMBER
			a_dict["plant_detils"] = str(inh.PLANT_RECORD_ID) + "|" + "Plants"
			a_dict["sap_detils"] = str(MATERIAL_RECORD_ID) + "|" + "Materials"
			for inhk in exp_list:
				a_name = inhk.replace(" ", "_")
				if a_name in x_ATTRIBUTE_NAME:
					Qstrr = (
						"select top 1000 ATTRIBUTE_NAME, SAP_PART_NUMBER, ATTVAL_VALDISPLAY from mappma (NOLOCK) \
						where PERSONALIZATION_RECORD_ID = '"
						+ str(RecAttValue)
						+ "' and PLANT_ID = '"
						+ str(inh.PLANT_ID)
						+ "' and SAP_PART_NUMBER = '"
						+ str(inh.SAP_PART_NUMBER)
						+ "' and ATTRIBUTE_NAME = '"
						+ str(inhk)
						+ "'"
					)
					Test_Obj = Sql.GetFirst(Qstrr)
					val = ""
					if Test_Obj is not None:
						val = str(Test_Obj.ATTVAL_VALDISPLAY) or ""
						# if x_dict.get(a_name) == val:
						a_dict[str(a_name)] = val
					else:
						a_dict[str(a_name)] = val
				if len(xx_dict) > 0:
					if xx_dict.get(a_name) == a_dict.get(a_name):
						bundle_list.append(a_dict)
				else:
					bundle_list.append(a_dict)
	return bundle_list


def PPLANT_PIVOT_FILTER(QST_REC_ID, Row_Count, Column_Count, Column_Names_List, New_CtrName, ATTRIBUTE_NAME):
	Column_Names_List = list(Column_Names_List)
	Column_Names_List = [js.strip() for js in Column_Names_List]
	x_Column_Names_List = Column_Names_List[4:]
	ATTRIBUTE_NAME = list(ATTRIBUTE_NAME)
	x_ATTRIBUTE_NAME = ATTRIBUTE_NAME[4:]
	x_dict = dict(zip(ATTRIBUTE_NAME, Column_Names_List))
	xx_dict = dict(zip(x_ATTRIBUTE_NAME, x_Column_Names_List))
	xx_dict = {value: xx_dict.get(value) for key, value in enumerate(xx_dict) if xx_dict.get(value) != ""}
	x_dict = dict(zip(ATTRIBUTE_NAME, Column_Names_List))
	if Row_Count != "PLANT":
		RecAttValue = Product.Attributes.GetByName("QSTN_SYSEFL_MA_00253").GetValue()
		where = "mp.PERSONALIZATION_RECORD_ID like '%" + str(RecAttValue) + "%'"
	else:
		RecAttValue = Product.Attributes.GetByName("QSTN_SYSEFL_MA_00339").GetValue()
		where = "mp.PLANT_ID like '%" + str(RecAttValue) + "%'"

	if Column_Names_List[0] != "":
		where += " and mp.PERSONALIZATION_PLANT_MATERIAL_RECORD_ID like '%" + str(Column_Names_List[0]) + "%'"
	if Row_Count != "PLANT":
		if Column_Names_List[1] != "":
			where += " and mp.PLANT_ID like '%" + str(Column_Names_List[1]) + "%'"
		if Column_Names_List[2] != "":
			where += " and mp.PLANT_NAME like '%" + str(Column_Names_List[2]) + "%'"
	else:
		if Column_Names_List[1] != "":
			where += " and mp.PERSONALIZATION_NAME like '%" + str(Column_Names_List[1]) + "%'"
	if Column_Names_List[3] != "":
		where += " and mp.SAP_PART_NUMBER like '%" + str(Column_Names_List[3]) + "%'"
	Mapeat_Obj = Sql.GetList(
		"select top 1000 ATTRIBUTE_NAME from MAPEAT (NOLOCK) where ATTRIBUTE_NAME <> '' and PERSONALIZATION_RECORD_ID = '"
		+ str(RecAttValue)
		+ "' order by CpqTableEntryId desc"
	)
	exp_list = [str(ikhd.ATTRIBUTE_NAME) for ikhd in Mapeat_Obj]
	Qstr = (
		"SELECT top 1000 mp.PERSONALIZATION_PLANT_MATERIAL_RECORD_ID, mp.PLANT_ID, mp.MATERIAL_RECORD_ID, \
		mp.PLANT_RECORD_ID, mp.PLANT_NAME, mp.SAP_PART_NUMBER from macpmp (NOLOCK) mp where "
		+ str(where)
		+ " order by mp.CpqTableEntryId desc"
	)
	mac_map_Obj = Sql.GetList(Qstr)
	bundle_list = []
	if mac_map_Obj is not None:
		for inh in mac_map_Obj:
			a_dict = {}
			mam_obj = Sql.GetFirst(
				"select MATERIAL_RECORD_ID from MAMTRL (NOLOCK) where SAP_PART_NUMBER = '" + str(inh.SAP_PART_NUMBER) + "'"
			)
			MATERIAL_RECORD_ID = ""
			if mam_obj is not None:
				MATERIAL_RECORD_ID = mam_obj.MATERIAL_RECORD_ID
			a_dict[
				"ACTIONS"
			] = '<div class="btn-group dropdown"><div class="dropdown" id="ctr_drop"><i data-toggle="dropdown" \
			id="dropdownMenuButton" class="fa fa-sort-desc dropdown-toggle" aria-expanded="false"></i><ul \
			class="dropdown-menu left" aria-labelledby="dropdownMenuButton"><li><a class="dropdown-item" \
			href="#" data-target="#cont_viewModalSection" onclick="cont_PERSONALIZEopenview\
			(this, \'PERSONALIZATION\')" data-toggle="modal">VIEW</a></li><li><a class="dropdown-item" href="#" \
			onclick="cont_PERSONALIZEopenedit(this, \'PERSONALIZATION\')" data-target="#cont_viewModalSection" \
			data-toggle="modal">EDIT</a></li><li><a class="dropdown-item" onclick="cont_PERSONALIZEdelete\
			(this, \'PERSONALIZATION\')" href="#">DELETE</a></li></ul></div></div>'
			a_dict["PERSONALIZATION_NAME"] = inh.PERSONALIZATION_PLANT_MATERIAL_RECORD_ID
			a_dict["PLANT_ID"] = inh.PLANT_ID
			a_dict["PLANT_NAME"] = inh.PLANT_NAME
			a_dict["SAP_PART_NUMBER"] = inh.SAP_PART_NUMBER
			a_dict["plant_detils"] = str(inh.PLANT_RECORD_ID) + "|" + "Plants"
			a_dict["sap_detils"] = str(MATERIAL_RECORD_ID) + "|" + "Materials"
			for inhk in exp_list:
				a_name = inhk.replace(" ", "_")
				if a_name in x_ATTRIBUTE_NAME:
					Qstrr = (
						"select top 1000 ATTRIBUTE_NAME, SAP_PART_NUMBER, ATTVAL_VALDISPLAY from mappma (NOLOCK) \
						where PERSONALIZATION_RECORD_ID = '"
						+ str(RecAttValue)
						+ "' and PLANT_ID = '"
						+ str(inh.PLANT_ID)
						+ "' and SAP_PART_NUMBER = '"
						+ str(inh.SAP_PART_NUMBER)
						+ "' and ATTRIBUTE_NAME = '"
						+ str(inhk)
						+ "'"
					)
					Test_Obj = Sql.GetFirst(Qstrr)
					val = ""
					if Test_Obj is not None:
						val = str(Test_Obj.ATTVAL_VALDISPLAY) or ""
						# if x_dict.get(a_name) == val:
						a_dict[str(a_name)] = val
					else:
						a_dict[str(a_name)] = val
				if len(xx_dict) > 0:
					if xx_dict.get(a_name) == a_dict.get(a_name):
						bundle_list.append(a_dict)
				else:
					bundle_list.append(a_dict)
			if len(exp_list) == 0:
				bundle_list.append(a_dict)
	return bundle_list


QST_REC_ID = Param.SQL_Expression
#Trace.Write("QST_REC_ID---" + str(QST_REC_ID))
ContainerType = Param.ContainerType
Row_Count = Param.Row_Count
Column_Count = Param.Column_Count
New_CtrName = Param.New_CtrName or ""
Column_Names_List = Param.Column_Names_List
# LogInfo('Column_Names_List-----   '+str(Column_Names_List))
offset_list = []
for val in Param:
	offset_list.append(val.Key)
if "Offset_Skip_Count" in offset_list:
	Offset_Skip_Count = Param.Offset_Skip_Count
else:
	Offset_Skip_Count = 0
if "Fetch_Count" in offset_list:
	Fetch_Count = Param.Fetch_Count
else:
	Fetch_Count = 20
# LogInfo("Fetch_Count param---" + str(Fetch_Count))
# LogInfo("Offset_Skip_Count --param"+str(Offset_Skip_Count))


def AtrrJqxDrop():
	#RECID = Product.Attributes.GetByName("QSTN_SYSEFL_MA_00259").GetValue()
	#MAATTR_obj = Sql.GetList("SELECT ATTRIBUTE_TYPE from MAATTR (NOLOCK)")
	# for obj in MAATTR_obj:
	#Current_obj = Sql.GetFirst("SELECT ATTRIBUTE_TYPE from MAATTR (NOLOCK) where ATTRIBUTE_RECORD_ID = '" + str(RECID) + "'")
	attr_list = [
		"PERSONALIZATION ATTRIBUTE",
		"CATEGORY ATTRIBUTE",
		"MATERIAL ATTRIBUTE",
	]
	# for attr in MAATTR_obj:
	# 	attr_list.append(attr.ATTRIBUTE_TYPE)
	# attr_list = [ins for ins in list(set(attr_list)) if ins != '']
	return attr_list, attr_type


try:
	ACTION = Param.ACTION
	ATTRIBUTE_VALUE = Param.ATTRIBUTE_VALUE
except:
	ACTION = ""
	ATTRIBUTE_VALUE = ""
try:
	ParentNodeRecId = Param.ParentNodeRecId
except:
	ParentNodeRecId = ""

try:
	PerPage = Param.PerPage
	PageInform = Param.PageInform
except:
	PerPage = ""
	PageInform = ""
# SQLVIEW CTR_TYPE
if ContainerType == "SQL VIEW":
	ApiResponse = ApiResponseFactory.JsonResponse(MMDYNMICSQLTABLE(QST_REC_ID))

# SQLVIEW123 CTR_TYPE
elif ContainerType == "SQL VIEW123":
	ApiResponse = ApiResponseFactory.JsonResponse(MDYNMICSQLTABLE123(QST_REC_ID))

# FIXEDROWS CTR_TYPE
elif ContainerType == "FIXED ROWS":
	ApiResponse = ApiResponseFactory.JsonResponse(
		StaticTableFormation(Row_Count, Column_Count, Column_Names_List, New_CtrName)
	)


elif ContainerType == "DYNAMIC ROWS":

	# PIVOTTABLE_CTRS
	if New_CtrName == "G_SALESMODEL_CLS_PRBSET_FACTORS" or New_CtrName == "GLOBAL SALESORG LIST PRICBOOK SET FACTORS":
		if ACTION == "":
			ApiResponse = ApiResponseFactory.JsonResponse(
				PivotTableFormation(
					ParentNodeRecId,
					QST_REC_ID,
					Row_Count,
					Column_Count,
					Column_Names_List,
					New_CtrName,
					PerPage,
					PageInform,
				)
			)
	elif ACTION == "PRODUCT_ONLOAD" and (
		New_CtrName == "PRICE_CLASS_LEVEL_FACTORS" or New_CtrName == "SALES_ORG_LEVEL_DEFAULT_FACTORS"
	):
		ApiResponse = ApiResponseFactory.JsonResponse(
			PivotTableSearch(
				ParentNodeRecId,
				QST_REC_ID,
				Row_Count,
				Column_Count,
				Column_Names_List,
				ATTRIBUTE_VALUE,
				New_CtrName,
				PerPage,
				PageInform,
			)
		)

	elif New_CtrName == "ATTJQXDROP":
		ApiResponse = ApiResponseFactory.JsonResponse(AtrrJqxDrop())
	else:
		# LogInfo('LLLLLLLLLLLL-MMDYNAMICSSQLTABLE------------LLLLLLL'+str(New_CtrName))
		ApiResponse = ApiResponseFactory.JsonResponse(
			StaticTableFormation(QST_REC_ID, Row_Count, Column_Count, Column_Names_List, New_CtrName)
		)


# CUSTOM OBJECT GRID CTR_TYPE
elif ContainerType == "CUSTOM OBJECT GRID":
	ApiResponse = ApiResponseFactory.JsonResponse(MDYNMIC_CSBJ_SQLTABLE(QST_REC_ID))

# CTR_INPUT_ONCHANGE CTR_TYPE
elif ContainerType == "CTR_INPUT_ONCHANGE":
	# 'SQL_Expression':input_val, 'QST_REC_ID ':input_id, 'ContainerType ':'CTR_INPUT_ONCHANGE', 'Row_Count ':'',
	# 'Column_Count ':'', 'New_CtrName ':'', 'Column_Names_List ':arr
	inputVal = str(QST_REC_ID)
	# LogInfo('zzzzzzzzzzzzzzzzz '+str(inputVal))
	inputId = ""
	# LogInfo('aaaaaaaaaaaaaa '+str(Param.QST_REC_ID))
	if str(Param.QST_REC_ID) is not None and str(Param.QST_REC_ID) != "":
		Upd_Arr = []
		try:
			inputId = str(Param.QST_REC_ID).split("___")[1]
			# LogInfo('inputId ----                '+str(inputId))
		except:
			pass

		Upd_Arr = list(Column_Names_List)
		# LogInfo('Upd_Arr---          '+str(list(Column_Names_List)))

	if inputId != "":
		ApiResponse = ApiResponseFactory.JsonResponse(StaticTableFormationOnchange(inputVal, inputId, Upd_Arr, New_CtrName))
	else:
		ApiResponse = ApiResponseFactory.JsonResponse("")
# =========================================================================================================================================
#   __script_name : SYUADNWPOP.PY
#   __script_description : THIS SCRIPT IS USED TO OPEN A POPUP WHEN USER CLICKS ON ADD OR NEW ACTION BUTTON ON A RELATED LIST RECORD.
#   __primary_author__ : ASHA LYSANDAR
#   __create_date : 26/08/2020
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import math
import SYCNGEGUID as CPQID
from SYDATABASE import SQL
import Webcom.Configurator.Scripting.Test.TestProduct

Sql = SQL()

TestProduct = Webcom.Configurator.Scripting.Test.TestProduct()


def POPUPLISTVALUEADDNEW(
	TABLEID,
	RECORDID,
	RECORDFEILD,
	NEWVALUE,
	LOOKUPOBJ,
	LOOKUPAPI,
	OPER,
	A_Keys,
	A_Values,
	selected_offerings_list,
	selected_program_list,
	DIVNAME,
	AwdRecordID,
	TreeParentParam,
	PerPage,
	PageInform
	
):
	api_name = ""
	btn2 = "SAVE"
	table_id = ""
	new_value_dict = {}
	new_value_dict2 = {}
	func2 = "popup_cont_SAVE(this, '" + DIVNAME + "')"
	sec_str = ""
	SaveCancel = ""
	record_field = ""
	record_value = ""
	sap_list = []
	table_header = ""
	api_name = ""
	api_value = ""
	var_str = ""
	date_field = cf_list = []
	Chkctry = ""
	attr_check = "attribute_checker(this)"
	dbl_clk_function = ""
	#getting dynamic values for consumables and non consumables start
	TreeParam = Product.GetGlobal("TreeParam")
	non_consumable_value = 'AGS_'+str(TreeParam)+'_TSC_NONCNS'
	#consumable_value ='AGS_'+str(TreeParam)+'_TSC_CONSUM'
	if TreeParam == 'Z0092':
		consumable_value = ''
	else:
		consumable_value ='AGS_'+str(TreeParam)+'_TSC_CONSUM'
	#getting dynamic values for consumables and non consumables end
	if RECORDID is not None:
		RECORD_ID = RECORDID.split("-")
	SegmentsClickParam = ""
	try:
		primary_value = RECORDID
	except:
		primary_value = ""
	primary_field = RECORDFEILD
	try:
		RECORD_FEILD = RECORDFEILD.split("_")
	except:
		RECORD_FEILD = ""
	try:
		contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
	except:
		contract_quote_record_id = ''
	try:
		quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
	except:
		quote_revision_record_id = ''
	#page = ''
	pagedata = ''  
	QryCount = ""
	disable = ''  
	try:
		if (TABLEID != "ADDNEW__SYOBJR_93123_SYOBJ_00267" and TABLEID != "ADDNEW__SYOBJR_98788_SYOBJ_00907") and RECORD_FEILD != "":
			Trace.Write('trace-----')
			RECORD_FEILD = RECORD_FEILD[1] + "-" + RECORD_FEILD[2] + "-" + RECORD_FEILD[3]
		elif (TABLEID != "ADDNEW__SYOBJR_95800_SYOBJ_00458" and TABLEID != "ADDNEW__SYOBJR_98788_SYOBJ_00907") and RECORD_FEILD != "":
			RECORD_FEILD = RECORD_FEILD[1] + "-" + RECORD_FEILD[2] + "-" + RECORD_FEILD[3]
			
		elif RECORD_FEILD != "":
			RECORD_FEILD = RECORDFEILD.split("_")
		else:
			Trace.Write('In else')
			RECORD_FEILD = ""
	except:
		RECORD_FEILD = ""
	try:	
		if TABLEID.startswith("SYOBJR"):
			TABLE_ID = ""
		else:
			TABLE_ID = TABLEID.split("__")
	except:		
		TABLE_ID = ""
		
	TreeParentParam = ""
	TreeSuperParentParam = ""
	try:
		if TABLE_ID:
			table = TABLE_ID[1]
		else:
			table = TABLEID
	except:
		table = ""
	try:
		table = table.split("_")
	except:
		table = ""
	count_value = 0
	filter_control_function = ""
	try:
		CurrentTab = TestProduct.CurrentTab
	except:
		CurrentTab = 'Quotes'    
	Trace.Write('TABLEID----'+str(TABLEID))
	try:
		table1 = table[2] + "-" + table[3]
	except:
		table1 = ""
	try:	
		popup_table_id = table[0] + "-" + table[1]
	except:
		popup_table_id = ""

	filter_tags = []
	filter_types = []
	filter_values = []
	filter_drop_down = ""

	popup_lable_obj = Sql.GetFirst(
		"SELECT NAME,OBJ_REC_ID FROM SYOBJR (NOLOCK) WHERE SAPCPQ_ATTRIBUTE_NAME='" + str(popup_table_id) + "'"
	)
	if popup_lable_obj is not None:
		SYOBJR_NAME = "div_CTR_" + str(popup_lable_obj.NAME).replace(" ", "_")
		Question_obj = Sql.GetFirst(
			"SELECT OBJECT_NAME, LABEL FROM SYOBJH (NOLOCK) WHERE RECORD_ID='" + str(popup_lable_obj.OBJ_REC_ID) + "'"
		)	

	else:
		Question_obj = Sql.GetFirst(
			"SELECT OBJECT_NAME, LABEL FROM SYOBJH (NOLOCK) WHERE SAPCPQ_ATTRIBUTE_NAME='SYOBJ-00263'"
		)

	if TABLEID != "ADDNEW__SYOBJR_93123_SYOBJ_00267" or TABLEID != "ADDNEW__SYOBJR_98788_SYOBJ_00907":
		if TABLEID != "ADDNEW__SYOBJR_95800_SYOBJ_00458":		
			rec_field = Sql.GetFirst(
				"SELECT API_NAME,API_FIELD_NAME FROM SYSEFL (NOLOCK) WHERE SAPCPQ_ATTRIBUTE_NAME='" + str(RECORD_FEILD) + "'"
			)
			if rec_field is not None and rec_field != "":
				record_field = str(eval("rec_field.API_FIELD_NAME"))
				record_value = str(eval("rec_field.API_NAME"))
			else:
				record_field = ""
				record_value = ""
		
	if str(popup_table_id) == "SYOBJR-94489":
		TreeParentParam = Product.GetGlobal("TreeParentLevel0")
		record_value = TreeParentParam
		TreeParentParam = Product.GetGlobal("TreeParentLevel0")  
		TreeSuperParentParam =  Product.GetGlobal("TreeParentLevel1")               
		TreeTopSuperParentParam = Product.GetGlobal("TreeParentLevel2")
		
	
	Product.SetGlobal("attrval_record_id", "")
	for tab in Product.Tabs:
		if tab.IsSelected == True:
			TabName = str(tab.Name)
	try:
		Trace.Write(TabName)
	except: 
		TabName = 'Quote'           
	offset_skip_count = Offset_Skip_Count
	if offset_skip_count == 1:
		offset_skip_count = 0
	fetch_count = Fetch_Count
	Flag_value = Product.GetGlobal("Flag_value")
	dict_list = []
	select_index = []
	i = 0
	id_list = []
	dict_list1 = []
	selected_offerings_list_preslect = []
	Trace.Write("DIVNAME==="+str(DIVNAME))	

	if Question_obj is not None:
		if DIVNAME == "div_CTR_Assigned_Apps":
			ObjectName = "SYPRAP"		
		elif str(popup_table_id) == "SYOBJR-98859":
			ObjectName = "SAQSAO"
		else:
			ObjectName = Question_obj.OBJECT_NAME.strip()
		Trace.Write("OBJ_NAMEE "+str(ObjectName))
		if str(ObjectName) == "USERS" and str(CurrentTab) == "Profile":
			D = {}
			new_value_dict = {}
			where_string = ""
			if A_Keys != "" and A_Values != "":
				A_Keys = list(A_Keys)
				A_Values = list(A_Values)
				D = zip(A_Keys, A_Values)
				D = dict(D)
				for key, value in zip(A_Keys, A_Values):
					if value.strip():
						if where_string:
							where_string += " AND "
						where_string += "{Key} LIKE '%{Value}%'".format(Key=key, Value=value)
			pagination_app_total_count = 0
			#Trace.Write("TESTZ: " + str(where_string))
			prof_id = ""
			prof_id = Product.GetGlobal("Profile_ID_val")
			if prof_id == "":
				prof_id = Product.GetGlobal("Profile_ID")
			pagination_condition = "OFFSET {Offset_Skip_Count} ROWS FETCH NEXT {Fetch_Count} ROWS ONLY".format(
				Offset_Skip_Count=offset_skip_count, Fetch_Count=fetch_count
			)
			if where_string:
				where_string += " AND "
			Pagination_app_M = Sql.GetFirst(
				"select count(U.ID) as count from USERS U (NOLOCK) WHERE "+str(where_string)+" U.ID  NOT IN (SELECT up.user_id FROM Users_permissions up  inner join cpq_permissions cp on cp.permission_id = up.permission_id group by up.user_id having count(user_id) > 1)"
			)
			disable_next_and_last = ""
			disable_previous_and_first = ""

			if Pagination_app_M is not None:
				pagination_app_total_count = Pagination_app_M.count
			records_end = offset_skip_count + fetch_count - 1
			#Trace.Write("records_end--182---" + str(records_end))
			if offset_skip_count == 0:
				offset_skip_count = 1
				records_end = fetch_count
			Trace.Write("pagination_app_total_count--182---" + str(pagination_app_total_count))
			if pagination_app_total_count < records_end:
				records_end = pagination_app_total_count
			else:
				records_end = records_end
			records_start_and_end = "{} - {} of ".format(offset_skip_count, records_end)
			disable_next_and_last = ""
			disable_previous_and_first = ""
			if records_end == pagination_app_total_count:
				disable_next_and_last = "class='btn-is-disabled'"
			if offset_skip_count == 0:
				disable_previous_and_first = "class='btn-is-disabled'"
			current_page = int(math.ceil(offset_skip_count / fetch_count)) + 1

			ObjectName = "USERS"
			table_id = "assignedUsers_addnew"
			table_ids = "#" + str(table_id)
			Header_details = {
				"ID": "Key",
				"USERNAME": "User Name",
				"NAME": "Name",
			}
			ordered_keys = [
				"ID",
				"USERNAME",
				"NAME",
			]

			sec_str = '<div class="row modulebnr brdr ma_mar_btm">ASSIGNED MEMBERS: ADD NEW<button type="button" class="close flt_rt" onclick="closepopup_scrl()" data-dismiss="modal">X</button></div>'

			sec_str += '<div class="col-md-12"><div class="row pad-10 bg-lt-wt brdr"><button type="button" class="btnconfig" onclick="closepopup_scrl()" data-dismiss="modal">CANCEL</button><button type="button" id="country_save" class="btnconfig" onclick="save_assignedapp()" data-dismiss="modal">SAVE</button></div></div>'

			sec_str += '<div id="container" class="g4 pad-10 brdr except_sec">'
			sec_str += (
				'<table id="'
				+ str(table_id)
				+ '" data-escape="true"  data-search-on-enter-key="true" data-show-header="true"  data-filter-control="true"> <thead><tr>'
			)
			sec_str += '<th data-field="SELECT" class="wth45" data-checkbox="true" id ="check_boxappval" ><div class="action_col">SELECT</div></th>'
			attr_dict = {
				"ID": "ID",
				"USERNAME": "USER NAME",
				"NAME": "FULL NAME",
			}
			for key, invs in enumerate(list(ordered_keys)):
				invs = str(invs).strip()
				qstring = attr_dict.get(str(invs)) or ""
				sec_str += (
					'<th data-field="'
					+ invs
					+ '" data-title-tooltip="'
					+ str(qstring)
					+ '" data-sortable="true" data-filter-control="input">'
					+ str(qstring)
					+ "</th>"
				)
			sec_str += '</tr></thead><tbody class ="app_id" ></tbody></table>'
			sec_str += '<div id="assignedapp_footer"></div>'
			order_by = "order by U.USERNAME Asc"

			# where_string += " U.ID NOT IN (SELECT up.user_id FROM Users_permissions up  )"
			where_string += " U.ID NOT IN (SELECT up.user_id FROM Users_permissions up  inner join cpq_permissions cp on cp.permission_id = up.permission_id group by up.user_id having count(user_id) > 1 )"
			Gen_USERS = SqlHelper.GetList(
				"select U.ID,U.USERNAME,U.NAME from USERS U  {} {} {} ".format(
					"WHERE " + where_string if where_string else "", order_by, pagination_condition
				)
			)
			# Trace.Write("where_string---252--" + str(where_string))
			# Trace.Write("pagination_condition---252--" + str(pagination_condition))
			Trace.Write(
				"select U.ID,U.USERNAME,U.NAME from USERS U  {} {} {} ".format(
					"WHERE " + where_string if where_string else "", order_by, pagination_condition
				)
			)
			if Gen_USERS is not None:
				for row_data in Gen_USERS:
					if row_data is not None:
						new_value_dict = {}
						for data in row_data:
							new_value_dict[data.Key] = data.Value
						date_field.append(new_value_dict)
			QueryCount = len(date_field)
			values_list = ""
			values_lists = ""
			a_test = []
			table_id = "assignedUsers_addnew"
			for invsk in list(Header_details):
				table_ids = "#" + str(table_id)
				filter_class = table_ids + " .bootstrap-table-filter-control-" + str(invsk)

				values_lists += "var " + str(invsk) + ' = $("' + str(filter_class) + '").val(); '

				values_lists += " ATTRIBUTE_VALUEList.push(" + str(invsk) + "); "
				a_test.append(invsk)

				filter_control_function += (
					'$("'
					+ filter_class
					+ '").change( function(){var table_id = $(this).closest("table").attr("id"); var a_list = '
					+ str(a_test)
					+ "; ATTRIBUTE_VALUEList = []; "
					+ str(values_lists)
					+ ' SortColumn = localStorage.getItem("SortColumn"); SortColumnOrder = localStorage.getItem("SortColumnOrder"); PerPage = $("#PageCountValue").val(); PageInform = "1___" + PerPage + "___" + PerPage; cpq.server.executeScript("SYUADNWPOP", {\'TABLEID\': "'
					+ str(TABLEID)
					+ "\", 'OPER': 'NO', 'RECORDID': \""
					+ str(RECORDID)
					+ "\", 'RECORDFEILD':  \""
					+ str(RECORDFEILD)
					+ "\", 'NEWVALUE': '', 'LOOKUPOBJ': '', 'LOOKUPAPI': '','A_Keys':a_list,'A_Values':ATTRIBUTE_VALUEList}, function(data) { date_field = data[3]; var assoc = data[1]; var api_name = data[2];data4 = data[4]; data5 = data[5]; if (date_field != \"NORECORDS\") { try { $(\""
					+ str(table_ids)
					+ '").bootstrapTable("load", date_field); $("#assignedapp_footer").html(data[6]); } catch(err) { $("'
					+ str(table_ids)
					+ '").bootstrapTable("load", date_field  ); $("#assignedapp_footer").html(data[6]); } document.getElementById("assignedapp_footer").style.border = ""; document.getElementById("assignedapp_footer").style.padding = "0px"; } else { var date_field = []; $("'
					+ str(table_ids)
					+ '").bootstrapTable("load", date_field  ); document.getElementById("assignedapp_footer").style.border = "1px solid #ccc"; document.getElementById("assignedapp_footer").style.padding = "5.5px"; document.getElementById("assignedapp_footer").innerHTML = "No Records to Display"; } });  });'
				)
			dbl_clk_function += (
				'$("'
				+ str(table_ids)
				+ '").on("all.bs.table", function (e, name, args) { $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); }); $("'
				+ str(table_ids)
				+ '\ th.bs-checkbox div.th-inner").before("<div class=\'pad0brdbt\'>SELECT</div>"); $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>");'
			)
			Product.SetGlobal("QueryCount", str(QueryCount))
			if QueryCount != 0:
				var_str += """<div class="col-md-12 brdr listContStyle padbthgt30">
						<div class="col-md-4 pager-numberofitem  clear-padding">
							<span class="pager-number-of-items-item flt_lt_pad2_mar2022" id="Rec_App_Start_End">{Records_App_Start_And_End}</span>
							<span class="pager-number-of-items-item flt_lt_pad2_mar" id="TotalRecAppCount">{Pagination_TotalApp_Count}</span>
								<div class="clear-padding fltltmrgtp3">
									<div class="pull-right vralign">
										<select onchange="ShowResultCountFunction_GS_ADD_NEW_APP_USERS(this)" id="ShowResultCountsApp" class="form-control selcwdt">
											<option value="10" {Selected_10}>10</option>
											<option value="20" {Selected_20}>20</option>
											<option value="50" {Selected_50}>50</option>
											<option value="100" {Selected_100}>100</option>
											<option value="200" {Selected_200}>200</option>
										</select>
									</div>
								</div>
						</div>
							<div class="col-xs-8 col-md-4  clear-padding inpadtex" data-bind="visible: totalItemCount">
								<div class="clear-padding col-xs-12 col-sm-6 col-md-12 brd0">
									<ul class="pagination pagination">
										<li class="disabled"><a onclick="GetFirstResultFunction_GS_ADD_NEW_APP_USERS()" {Disable_First}><i class="fa fa-caret-left fnt14bold"></i><i class="fa fa-caret-left fnt14"></i></a></li>
										<li class="disabled"><a onclick="GetPreviuosResultFunction_GS_ADD_NEW_APP_USERS()" {Disable_Previous}><i class="fa fa-caret-left fnt14"></i>PREVIOUS</a></li>
										<li class="disabled"><a onclick="GetNextResultFunction_GS_ADD_NEW_APP_USERS()" {Disable_Next}>NEXT<i class="fa fa-caret-right fnt14"></i></a></li>
										<li class="disabled"><a onclick="GetLastResultFunction_GS_ADD_NEW_APP_USERS()" {Disable_Last}><i class="fa fa-caret-right fnt14"></i><i class="fa fa-caret-right fnt14bold"></i></a></li>
									</ul>
								</div>
							</div>
							<div class="col-md-4 pad3">
							<span id="page_count" class="currentPage page_right_content">{Current_Page}</span>
								<span class="page_right_content padrt2">Page </span>
							</div>
					</div></div>""".format(
					Records_App_Start_And_End=records_start_and_end,
					Pagination_TotalApp_Count=pagination_app_total_count,
					Selected_10="selected" if fetch_count == 10 else "",
					Selected_20="selected" if fetch_count == 20 else "",
					Selected_50="selected" if fetch_count == 50 else "",
					Selected_100="selected" if fetch_count == 100 else "",
					Selected_200="selected" if fetch_count == 200 else "",
					Disable_First=disable_previous_and_first,
					Disable_Previous=disable_previous_and_first,
					Disable_Next=disable_next_and_last,
					Disable_Last=disable_next_and_last,
					Current_Page=current_page,
				)
			else:
				date_field = "NORECORDS"
		# ADD FAB POPUP STARTS JOE
		elif str(ObjectName) == "SAQFBL" and str(CurrentTab) == "Quotes":
			TreeParam = Product.GetGlobal("TreeParam")
			TreeParentParam = Product.GetGlobal("TreeParentLevel0")  
			account_id = TreeParam.split(' - ')
			fab_id = TreeParam.split(' - ')
			Trace.Write("check123"+str(account_id))
			account_id = account_id[len(account_id)-1]
			where_string = ""
			if A_Keys != "" and A_Values != "":
				A_Keys = list(A_Keys)
				A_Values = list(A_Values)
				for key, value in zip(A_Keys, A_Values):
					if key == "FAB_LOCATION_RECORD_ID":
						key = "MAFBLC.CpqTableEntryId"
					Trace.Write('Value--->'+str(value))
					if value.strip():
						if where_string:
							where_string += " AND "
						where_string += "{Key} LIKE '%{Value}%'".format(Key=key, Value=value)
			DIVNAME = "VIEW_DIV_ID"
			new_value_dict = {}
			ObjectName = "MAFBLC"
			table_id = "fablocation_addnew"            

			Header_details = {
				"FAB_LOCATION_RECORD_ID": "KEY",
				"FAB_LOCATION_ID": "FAB ID",
				"FAB_LOCATION_NAME": "FAB NAME",
				
			}
			ordered_keys = [
				"FAB_LOCATION_RECORD_ID",
				"FAB_LOCATION_ID",
				"FAB_LOCATION_NAME",
				
			]
			Objd_Obj = Sql.GetList(
				"select FIELD_LABEL,API_NAME,LOOKUP_OBJECT,LOOKUP_API_NAME,DATA_TYPE,FORMULA_DATA_TYPE from SYOBJD (NOLOCK)where OBJECT_NAME = '"
				+ str(ObjectName)
				+ "'"
			)
			lookup_disply_list = []
			if Objd_Obj is not None:
				attr_list = {}
				api_names = [inn.API_NAME for inn in Objd_Obj]
				for attr in Objd_Obj:
					attr_list[str(attr.API_NAME)] = str(attr.FIELD_LABEL)
					if str(attr.LOOKUP_API_NAME) != "" and str(attr.LOOKUP_API_NAME) is not None:
						lookup_disply_list.append(str(attr.API_NAME))
				checkbox_list = [
					inn.API_NAME for inn in Objd_Obj if (inn.DATA_TYPE == "CHECKBOX" or inn.FORMULA_DATA_TYPE == "CHECKBOX")
				]
				lookup_list = {ins.LOOKUP_API_NAME: ins.API_NAME for ins in Objd_Obj}
			sec_str = '<div class="row modulebnr brdr ma_mar_btm">ADD FAB LOCATION<button type="button" class="close flt_rt" onclick="closepopup_scrl()" data-dismiss="modal">X</button></div>'
			if (TreeParam == "Fab Locations"):
				sec_str += '<div class="col-md-12 padlftrhtnone"><div class="row pad-10 bg-lt-wt brdr"> <img style="height: 40px; margin-top: -1px; margin-left: -1px; float: left;" src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/Secondary Icon.svg"/><div class="product_txt_div_child secondary_highlight" style="display: block;"><div class="product_txt_child"><abbr title="Sales Org">Fab Location ID</abbr></div><div class="product_txt_to_top_child" style="float: left;"><abbr title="ALL">ALL</abbr></div></div><div class="product_txt_div_child secondary_highlight" style="display: block;"><div class="product_txt_child"><abbr title="Fab Name">Sales Org</abbr></div><div class="product_txt_to_top_child" style="float: left;"><abbr title="All">All</abbr></div></div> <button type="button" class="btnconfig" data-dismiss="modal" onclick="closepopup_scrl()">CANCEL</button><button type="button" id="add-offerings" class="btnconfig" onclick="addfabs()" data-dismiss="modal">ADD</button></div></div>'
			elif (("Sending Account -" in TreeParam) or ("Receiving Account -" in TreeParam) and TreeParentParam == 'Fab Locations'):
				sec_str += '<div class="col-md-12 padlftrhtnone"><div class="row pad-10 bg-lt-wt brdr"> <img style="height: 40px; margin-top: -1px; margin-left: -1px; float: left;" src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/Secondary Icon.svg"/><div class="product_txt_div_child secondary_highlight" style="display: block;"><div class="product_txt_child"><abbr title="Sales Org">{location} Account ID</abbr></div><div class="product_txt_to_top_child" style="float: left;"><abbr title="ALL">{id}</abbr></div></div><div class="product_txt_div_child secondary_highlight" style="display: block;"><div class="product_txt_child"><abbr title="Fab Name">Fab Location ID</abbr></div><div class="product_txt_to_top_child" style="float: left;"><abbr title="All">All</abbr></div></div><div class="product_txt_div_child secondary_highlight" style="display: block;"><div class="product_txt_child"><abbr title="Fab Name">Sales Org</abbr></div><div class="product_txt_to_top_child" style="float: left;"><abbr title="All">All</abbr></div></div> <button type="button" class="btnconfig" data-dismiss="modal" onclick="closepopup_scrl()">CANCEL</button><button type="button" id="add-offerings" class="btnconfig" onclick="addfabs()" data-dismiss="modal">ADD</button></div></div>'.format(location="Sending" if "Sending Account" in TreeParam else "Receiving",id=fab_id[1])

			sec_str += '<div id="container" class="g4 pad-10 brdr except_sec">'
			sec_str += (
				'<table id="'
				+ str(table_id)
				+ '" data-escape="true"  data-search-on-enter-key="true" data-show-header="true"  data-filter-control="true"> <thead><tr>'
			)
			sec_str += '<th data-field="SELECT" class="wth45" data-checkbox="true" id ="check_boxval" onchange = "get_checkedval()"><div class="action_col">SELECT</div></th>'

			for key, invs in enumerate(list(ordered_keys)):

				invs = str(invs).strip()
				qstring = Header_details.get(str(invs)) or ""
				if key == 0:
					sec_str += (
						'<th data-field="'
						+ str(invs)
						+ '" data-formatter="MAfablocationKeyHyperLink" data-sortable="true" data-title-tooltip="'
						+ str(qstring)
						+ '" data-filter-control="input">'
						+ str(qstring)
						+ "</th>"
					)
				else:
					sec_str += (
						'<th data-field="'
						+ invs
						+ '" data-title-tooltip="'
						+ str(qstring)
						+ '" data-sortable="true" data-filter-control="input">'
						+ str(qstring)
						+ "</th>"
					)
			sec_str += '</tr></thead><tbody class ="user_id" ></tbody></table>'
			sec_str += '<div id="fablocation_footer"></div>'
			values_list = ""
			values_lists = ""
			a_test = []
			Doubleclick_Info = ''
			for invsk in list(Header_details):
				table_ids = "#" + str(table_id)
				filter_class = table_ids + " .bootstrap-table-filter-control-" + str(invsk)
				values_lists += "var " + str(invsk) + ' = $("' + str(filter_class) + '").val(); '
				values_lists += " ATTRIBUTE_VALUEList.push(" + str(invsk) + "); "
				#Trace.Write("66666 ---->"+str(values_lists))
				a_test.append(invsk)
				#Doubleclick_Info.append('$("' + str(filter_class) + '").val(); ')

				filter_control_function += (
					'$("'
					+ filter_class
					+ '").change( function(){ var table_id = $(this).closest("table").attr("id"); var a_list = '
					+ str(a_test)
					+ "; ATTRIBUTE_VALUEList = []; "
					+ str(values_lists)
					+ ' SortColumn = localStorage.getItem("SortColumn"); SortColumnOrder = localStorage.getItem("SortColumnOrder"); PerPage = $("#PageCountValue").val(); PageInform = "1___" + PerPage + "___" + PerPage; cpq.server.executeScript("SYUADNWPOP", {\'TABLEID\': "'
					+ str(TABLEID)
					+ "\", 'OPER': 'NO', 'RECORDID': \""
					+ str(RECORDID)
					+ "\", 'RECORDFEILD':  \""
					+ str(RECORDFEILD)
					+ "\", 'NEWVALUE': '', 'LOOKUPOBJ': '', 'LOOKUPAPI': '','A_Keys':a_list,'A_Values':ATTRIBUTE_VALUEList,'PerPage':PerPage,'PageInform':PageInform}, function(data) {  date_field = data[3]; var assoc = data[1]; var api_name = data[2];data4 = data[4];data5 = data[5];data15 = data[15]; data16 = data[16]; try { if(date_field.length > 0) { $(\""
					+ str(table_ids)
					+ '").bootstrapTable("load", date_field  ); $("button#country_save").attr("disabled",false); $("#noRecDisp").remove(); if (document.getElementById("RecordsStartAndEnd")){document.getElementById("RecordsStartAndEnd").innerHTML = data15;}; if (document.getElementById("TotalRecordsCount")) {document.getElementById("TotalRecordsCount").innerHTML = data16;} } else{ $("'
					+ str(table_ids)
					+ '").bootstrapTable("load", date_field  ); $("button#country_save").attr("disabled",true); $("#fablocation_addnew").after("<div id=\'noRecDisp\' class=\'noRecord\'>No Records to Display</div>"); $(".noRecord:not(:first)").remove(); } } catch(err) { if(date_field.length > 0) { $("'
					+ str(table_ids)
					+ '").bootstrapTable("load", date_field  ); $("button#country_save").attr("disabled",false); } else{ $("'
					+ str(table_ids)
					+ '").bootstrapTable("load", date_field  ); $("button#country_save").attr("disabled",true); } } ; });  });'
				)            
			
				dbl_clk_function = (
					'$("'
					+ str(table_ids)
					+ '").on("all.bs.table", function (e, name, args) { $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); });  $(".bs-checkbox input").addClass("custom"); $("'
					+ str(table_ids)
					+ "\").on('sort.bs.table', function (e, name, order) { console.log('sort.bs.table ============>', e); e.stopPropagation(); currenttab = $(\"ul#carttabs_head .active\").text().trim(); localStorage.setItem('"
					+ str(table_id)
					+ "_SortColumn', name); localStorage.setItem('"
					+ str(table_id)
					+ "_SortColumnOrder', order); ATTRIBUTE_VALUEList = []; "+str(values_lists)+" AddNewContainerSorting(name, order, '"
					+ str(table_id)
					+ "',"+str(a_test)+",ATTRIBUTE_VALUEList,'"+str(TABLEID)+"','"+str(RECORDID)+"','"+str(RECORDFEILD)+"'); }); "
					)
			# Trace.Write("757575 filter_control_function ---->"+str(filter_control_function))
			# Trace.Write("757575 dbl_clk_function ---->"+str(dbl_clk_function))
			if offset_skip_count%10==1:
				offset_skip_count-=1
			pagination_condition = "OFFSET {Offset_Skip_Count} ROWS FETCH NEXT {Fetch_Count} ROWS ONLY".format(
				Offset_Skip_Count=offset_skip_count, Fetch_Count=fetch_count
			)
			if where_string:
				where_string += " AND "
			if (("Sending Account -" in TreeParam) or ("Receiving Account -" in TreeParam)) and TreeParentParam == 'Fab Locations':
				#fab_type = 'SENDING FAB' if "Sending Account -" in TreeParam else 'RECEIVING FAB' if "Receiving Account -" in TreeParam else ""
				Pagination_M = Sql.GetFirst(
				"SELECT COUNT(MAFBLC.CpqTableEntryId) as count FROM {} (NOLOCK) WHERE MAFBLC.ACCOUNT_ID = '{}' AND {}FAB_LOCATION_ID NOT IN (SELECT FABLOCATION_ID FROM SAQFBL (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' and QTEREV_RECORD_ID = '{}' and RELOCATION_FAB_TYPE in ('SENDING FAB','RECEIVING FAB'))".format(
					ObjectName, account_id, where_string,contract_quote_record_id,quote_revision_record_id
					)
				)
			else:
				Pagination_M = Sql.GetFirst(
				"SELECT COUNT(MAFBLC.CpqTableEntryId) as count FROM {} (NOLOCK) JOIN SAQTMT (NOLOCK) ON MAFBLC.ACCOUNT_RECORD_ID = SAQTMT.ACCOUNT_RECORD_ID WHERE SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = '{}'AND QTEREV_RECORD_ID = '{}' AND {} FAB_LOCATION_ID NOT IN (SELECT FABLOCATION_ID FROM SAQFBL (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' and QTEREV_RECORD_ID = '{}' )".format(
					ObjectName, contract_quote_record_id,quote_revision_record_id,where_string, contract_quote_record_id,quote_revision_record_id
				)
			)

			if str(PerPage) == "" and str(PageInform) == "":
				Page_start = 1
				Page_End = fetch_count
				PerPage = fetch_count
				PageInform = "1___"+str(fetch_count)+"___"+str(fetch_count)
			else:
				Page_start = int(PageInform.split("___")[0])
				Page_End = int(PageInform.split("___")[1])
				PerPage = PerPage

			order_by = ""
			if SortColumn != '' and SortColumnOrder !='':
				order_by = "order by "+SortColumn + " " + SortColumnOrder
			else:
				order_by = "order by FAB_LOCATION_NAME ASC"

			pop_val = {}
			
			if (("Sending Account -" in TreeParam) or ("Receiving Account -" in TreeParam)) and TreeParentParam == 'Fab Locations':
				#fab_type = 'SENDING FAB' if "Sending Account -" in TreeParam else 'RECEIVING FAB' if "Receiving Account -" in TreeParam else ""
				where_string += """  MAFBLC.ACCOUNT_ID = '{}' AND FAB_LOCATION_ID NOT IN (SELECT FABLOCATION_ID FROM SAQFBL (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' and QTEREV_RECORD_ID = '{}' and RELOCATION_FAB_TYPE in ('SENDING FAB','RECEIVING FAB'))""".format(account_id,
					contract_quote_record_id,quote_revision_record_id
				)
				table_data = Sql.GetList(
					"select  {} from {} (NOLOCK) {} {} {}".format(", ".join(ordered_keys),
						ObjectName,
						"WHERE " + where_string if where_string else "",
						order_by,pagination_condition
						
					)
				)
				QueryCountObj = Sql.GetFirst(
						"select count(*) as cnt from {} (NOLOCK) {} ".format(                    
						ObjectName,
						"WHERE " + where_string if where_string else ""	
					)
					)

			else:
				where_string += """ SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND FAB_LOCATION_ID NOT IN (SELECT FABLOCATION_ID FROM SAQFBL (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}')""".format(
					contract_quote_record_id,quote_revision_record_id, contract_quote_record_id,quote_revision_record_id
				)

				table_data = Sql.GetList(
					"select  {} from {} (NOLOCK) JOIN SAQTMT (NOLOCK) ON MAFBLC.ACCOUNT_RECORD_ID = SAQTMT.ACCOUNT_RECORD_ID {} {} {}".format(", ".join(ordered_keys),
						ObjectName,
						"WHERE " + where_string if where_string else "",
						order_by,pagination_condition
						
					)
				)

				QueryCountObj = Sql.GetFirst(
						"select count(*) as cnt from {} (NOLOCK) JOIN SAQTMT (NOLOCK) ON MAFBLC.ACCOUNT_RECORD_ID = SAQTMT.ACCOUNT_RECORD_ID {} ".format(                    
						ObjectName,
						"WHERE " + where_string if where_string else ""
						
					)
					)
			if QueryCountObj is not None:
				QryCount = QueryCountObj.cnt




			""" table_data_select = Sql.GetList(
				"select top 1000 FABLOCATION_ID,FABLOCATION_NAME from SAQFBL (NOLOCK) where QUOTE_FABLOCATION_RECORD_ID ='"
				+ str(contract_quote_record_ids)
				+ "'"
			)
			for qt_obj in table_data_select:
				cpqidval = CPQID.KeyCPQId.GetCPQId(ObjectName, str(qt_obj.COUNTRY_RECORD_ID))                
				selected_offerings_list_preslect.append(cpqidval) """

			if table_data is not None:
				for row_data in table_data:
					data_id = str(ObjectName)

					new_value_dict = {}
					""" if not selected_offerings_list:
						if row_data.FAB_LOCATION_RECORD_ID in selected_offerings_list_preslect:                            
							new_value_dict["SELECT"] = True
						else:
							new_value_dict["SELECT"] = False

					else:
						selected_offerings_list_guids = []
						for val in selected_offerings_list:
							recid = CPQID.KeyCPQId.GetKEYId(ObjectName, str(val))
							selected_offerings_list_guids.append(recid)                        
						if row_data.FAB_LOCATION_RECORD_ID in selected_offerings_list_guids:                            
							new_value_dict["SELECT"] = True
						else:
							new_value_dict["SELECT"] = False """

					for data in row_data:
						if str(data.Key) == "FAB_LOCATION_RECORD_ID":
							pop_val = str(data.Value) + "|Offerings"
							cpqidval = CPQID.KeyCPQId.GetCPQId(ObjectName, str(data.Value))
							new_value_dict[data.Key] = cpqidval
						else:
							new_value_dict[data.Key] = data.Value
						new_value_dict["pop_val"] = pop_val
					date_field.append(new_value_dict)
			QueryCount = len(date_field)
			pagination_total_count = 0
			if Pagination_M is not None:
				pagination_total_count = Pagination_M.count
			if offset_skip_count == 0:
				offset_skip_count = 1
				records_end = fetch_count
			else:
				offset_skip_count += 1
				records_end = offset_skip_count + fetch_count -1
			records_end = pagination_total_count if pagination_total_count < records_end else records_end
			records_start_and_end = "{} - {} of ".format(offset_skip_count, records_end)
			disable_next_and_last = ""
			disable_previous_and_first = ""
			if records_end == pagination_total_count:
				disable_next_and_last = "class='btn-is-disabled' style=\'pointer-events:none\' "
			if offset_skip_count == 0:
				disable_previous_and_first = "class='btn-is-disabled' style=\'pointer-events:none\' "
			current_page = int(math.ceil(offset_skip_count / fetch_count)) + 1
			Trace.Write('At line 631')
			Product.SetGlobal("QueryCount", str(QueryCount))
			pagination_table_id = "pagination_{}".format(table_id)
			var_str += """<div id="{Parent_Div_Id}" class="col-md-12 brdr listContStyle padbthgt30">
					<div class="col-md-4 pager-numberofitem  clear-padding">
						<span class="pager-number-of-items-item flt_lt_pad2_mar2022" id="RecordsStartAndEnd">{Records_Start_And_End}</span>
						<span class="pager-number-of-items-item flt_lt_pad2_mar" id="TotalRecordsCount">{Pagination_Total_Count}</span>
							<div class="clear-padding fltltmrgtp3">
								<div class="pull-right vralign">
									<select onchange="ShowResultCountFunc(this, '{ShowResultCountFuncTb}', 'addFab', '{TableId}')" id="ShowResultCount" class="form-control selcwdt">
										<option value="10" {Selected_10}>10</option>
										<option value="20" {Selected_20}>20</option>
										<option value="50" {Selected_50}>50</option>
										<option value="100" {Selected_100}>100</option>
										<option value="200" {Selected_200}>200</option>
									</select>
								</div>
							</div>
					</div>
						<div class="col-xs-8 col-md-4  clear-padding inpadtex" data-bind="visible: totalItemCount">
							<div class="clear-padding col-xs-12 col-sm-6 col-md-12 brd0">
								<ul class="pagination pagination">
									<li class="disabled">
										<a onclick="GetFirstResultFunc('{GetFirstResultFuncTb}', 'addFab', '{TableId}')" {Disable_First}><i class="fa fa-caret-left fnt14bold"></i><i class="fa fa-caret-left fnt14"></i></a>
									</li>
									<li class="disabled"><a onclick="GetPreviuosResultFunc('{GetPreviuosResultFuncTb}', 'addFab', '{TableId}')" {Disable_Previous}><i class="fa fa-caret-left fnt14"></i>PREVIOUS</a></li>
									<li class="disabled"><a onclick="GetNextResultFunc('{GetNextResultFuncTb}', 'addFab', '{TableId}')" {Disable_Next}>NEXT<i class="fa fa-caret-right fnt14"></i></a></li>
									<li class="disabled"><a onclick="GetLastResultFunc('{GetLastResultFuncTb}', 'addFab', '{TableId}')" {Disable_Last}><i class="fa fa-caret-right fnt14"></i><i class="fa fa-caret-right fnt14bold"></i></a></li>
								</ul>
							</div>
						</div>
						<div class="col-md-4 pad3">
						<span id="page_count" class="currentPage page_right_content">{Current_Page}</span>
							<span class="page_right_content padrt2">Page </span>
						</div>
				</div></div>""".format(
				Parent_Div_Id=pagination_table_id,
				Records_Start_And_End=records_start_and_end,
				Pagination_Total_Count=pagination_total_count,
				ShowResultCountFuncTb=pagination_table_id,
				Selected_10="selected" if fetch_count == 10 else "",
				Selected_20="selected" if fetch_count == 20 else "",
				Selected_50="selected" if fetch_count == 50 else "",
				Selected_100="selected" if fetch_count == 100 else "",
				Selected_200="selected" if fetch_count == 200 else "",
				GetFirstResultFuncTb=pagination_table_id,
				Disable_First=disable_previous_and_first,
				GetPreviuosResultFuncTb=pagination_table_id,
				Disable_Previous=disable_previous_and_first,
				GetNextResultFuncTb=pagination_table_id,
				Disable_Next=disable_next_and_last,
				GetLastResultFuncTb=pagination_table_id,
				Disable_Last=disable_next_and_last,
				Current_Page=current_page,
				TableId=TABLEID,
			)
			table_ids = "#" + str(table_id)
			# Filter based on table MultiSelect Dropdown column - Start

			for index, col_name in enumerate(ordered_keys):
				table, api_name = ObjectName, col_name
				obj_data = Sql.GetFirst(
					"SELECT API_NAME, DATA_TYPE, PICKLIST FROM  SYOBJD WHERE OBJECT_NAME='"
					+ str(table)
					+ "' and API_NAME = '"
					+ str(api_name)
					+ "'"
				)
				if obj_data is not None:
					if str(obj_data.PICKLIST).upper() == "TRUE":
						filter_tag = (
							'<div id = "'
							+ str(table_id)
							+ "_RelatedMutipleCheckBoxDrop_"
							+ str(index)
							+ '" class="form-control bootstrap-table-filter-control-'
							+ str(api_name)
							+ " RelatedMutipleCheckBoxDrop_"
							+ str(index)
							+ ' "></div>'
						)
						filter_tags.append(filter_tag)
						filter_types.append("select")
						if obj_data.DATA_TYPE == "CHECKBOX":
							filter_values.append(["True", "False"])
						else:
							# Trace.Write("=============$$$$$$$$$$$$$>>>>>>>>>>>>> "+"SELECT DISTINCT {Column} FROM {Table}".format(Column=api_name, Table=table))
							data_obj = Sql.GetList(
								"SELECT DISTINCT {Column} FROM {Table}".format(Column=api_name, Table=table)
							)
							if data_obj is not None:
								filter_values.append([row_data.Value for data in data_obj for row_data in data])
					else:
						filter_tag = (
							'<input type="text" class="form-control wth100visble bootstrap-table-filter-control-'
							+ str(api_name)
							+ '">'
						)
						filter_tags.append(filter_tag)
						filter_types.append("input")
						filter_values.append("")

			filter_drop_down = (
				"try { if( document.getElementById('"
				+ str(table_id)
				+ "') ) { var listws = document.getElementById('"
				+ str(table_id)
				+ "').getElementsByClassName('filter-control');  for (i = 0; i < listws.length; i++) { document.getElementById('"
				+ str(table_id)
				+ "').getElementsByClassName('filter-control')[i].innerHTML = data6[i];  } for (j = 0; j < listws.length; j++) { if (data10[j] == 'select') { var dataAdapter = new $.jqx.dataAdapter(data8[j]); if(data11[j].length>5){ $('#"
				+ str(table_id)
				+ "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter}); }else{$('#"
				+ str(table_id)
				+ "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter ,autoDropDownHeight: true});} } } } }  catch(err) { setTimeout(function() { var listws = document.getElementById('"
				+ str(table_id)
				+ "').getElementsByClassName('filter-control');  for (i = 0; i < listws.length; i++) { document.getElementById('"
				+ str(table_id)
				+ "').getElementsByClassName('filter-control')[i].innerHTML = data9[i];  } for (j = 0; j < listws.length; j++) { if (data10[j] == 'select') { var dataAdapter = new $.jqx.dataAdapter(data11[j]); $('#"
				+ str(table_id)
				+ "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter, scrollBarSize :10 }); } } }, 5000); }"
			)
			dbl_clk_function += (
				'$("'
				+ str(table_ids)
				+ '").on("all.bs.table", function (e, name, args) { $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); }); $("'
				+ str(table_ids)
				+ '\ th.bs-checkbox div.th-inner").before("<div class=\'pad0brdbt\'>SELECT</div>"); $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>");'
			)

			pagedata = ""
			if QryCount == 0:
				pagedata = str(QryCount) + " - " + str(QryCount) + " of "
			elif QryCount < int(PerPage):
				pagedata = str(Page_start) + " - " + str(QryCount) + " of "
			else:
				pagedata = str(Page_start) + " - " + str(Page_End)+ " of "
			


		elif str(ObjectName) == "SAQSCF" and str(CurrentTab) == "Quotes":
			Trace.Write("Parent_Param" + str(TreeParentParam))
			where_string = ""
			if A_Keys != "" and A_Values != "":
				A_Keys = list(A_Keys)
				A_Values = list(A_Values)
				for key, value in zip(A_Keys, A_Values):
					if key == "FAB_LOCATION_RECORD_ID":
						key = "MAFBLC.CpqTableEntryId"
					if value.strip():
						if where_string:
							where_string += " AND "
						where_string += "{Key} LIKE '%{Value}%'".format(Key=key, Value=value)
			DIVNAME = "VIEW_DIV_ID"
			new_value_dict = {}
			ObjectName = "MAFBLC"
			table_id = "source_fablocation_addnew"            

			Header_details = {
				"FAB_LOCATION_RECORD_ID": "KEY",
				"FAB_LOCATION_ID": "FAB ID",
				"FAB_LOCATION_NAME": "FAB NAME",
			}
			ordered_keys = [
				"FAB_LOCATION_RECORD_ID",
				"FAB_LOCATION_ID",
				"FAB_LOCATION_NAME",
			]
			Objd_Obj = Sql.GetList(
				"select FIELD_LABEL,API_NAME,LOOKUP_OBJECT,LOOKUP_API_NAME,DATA_TYPE,FORMULA_DATA_TYPE from SYOBJD (NOLOCK)where OBJECT_NAME = '"
				+ str(ObjectName)
				+ "'"
			)
			lookup_disply_list = []
			if Objd_Obj is not None:
				attr_list = {}
				api_names = [inn.API_NAME for inn in Objd_Obj]
				for attr in Objd_Obj:
					attr_list[str(attr.API_NAME)] = str(attr.FIELD_LABEL)
					if str(attr.LOOKUP_API_NAME) != "" and str(attr.LOOKUP_API_NAME) is not None:
						lookup_disply_list.append(str(attr.API_NAME))
				checkbox_list = [
					inn.API_NAME for inn in Objd_Obj if (inn.DATA_TYPE == "CHECKBOX" or inn.FORMULA_DATA_TYPE == "CHECKBOX")
				]
				lookup_list = {ins.LOOKUP_API_NAME: ins.API_NAME for ins in Objd_Obj}
			sec_str = '<div class="row modulebnr brdr ma_mar_btm">ADD SOURCE FAB LOCATION<button type="button" class="close flt_rt" onclick="closepopup_scrl(this)" data-dismiss="modal">X</button></div>'
			sec_str += '<div class="col-md-12 padlftrhtnone" id="source_fab_header"><div class="row pad-10 bg-lt-wt brdr"> <div class="product_txt_div_child secondary_highlight" style="display: block;"><div class="product_txt_child"><abbr title="Source Account ID">Source Account ID</abbr></div> <div class="product_txt_to_top_child" style="float: left;"><abbr title="{}">{}</abbr></div></div><div class="product_txt_div_child secondary_highlight" style="display: block;"><div class="product_txt_child"><abbr title="Source Account Name">Source Account Name</abbr></div><div class="product_txt_to_top_child" style="float: left;"><abbr title="{}">{}</abbr></div></div><div class="product_txt_div_child secondary_highlight" style="display: block;"><div class="product_txt_child"><abbr title="Sales Orgs">Sales Orgs</abbr></div><div class="product_txt_to_top_child" style="float: left;"><abbr title="All">All</abbr></div></div><div class="product_txt_div_child secondary_highlight" style="display: block;"><div class="product_txt_child"><abbr title="Source Fab Location ID">Source Fab Location ID</abbr></div><div class="product_txt_to_top_child" style="float: left;"><abbr title="All">All</abbr></div></div><button type="button" class="btnconfig" data-dismiss="modal" id = "add_source_fab" onclick="closepopup_scrl(this)">CANCEL</button><button type="button" id="add-offerings" class="btnconfig" onclick="addsourcefabs()" data-dismiss="modal">ADD</button></div></div>'.format(Product.GetGlobal("stp_account_Id"), Product.GetGlobal("stp_account_Id"), Product.GetGlobal("stp_account_name"), Product.GetGlobal("stp_account_name"))

			sec_str += '<div id="container" class="g4 pad-10 brdr except_sec">'
			sec_str += (
				'<table id="'
				+ str(table_id)
				+ '" data-escape="true"  data-search-on-enter-key="true" data-show-header="true"  data-filter-control="true"> <thead><tr>'
			)
			sec_str += '<th data-field="SELECT" class="wth45" data-checkbox="true" id ="check_boxval" onchange = "get_checkedval()"><div class="action_col">SELECT</div></th>'

			for key, invs in enumerate(list(ordered_keys)):

				invs = str(invs).strip()
				qstring = Header_details.get(str(invs)) or ""
				if key == 0:
					sec_str += (
						'<th data-field="'
						+ str(invs)
						+ '" data-formatter="sourcefablocationKeyHyperLink" data-sortable="true" data-title-tooltip="'
						+ str(qstring)
						+ '" data-filter-control="input">'
						+ str(qstring)
						+ "</th>"
					)
				else:
					sec_str += (
						'<th data-field="'
						+ invs
						+ '" data-title-tooltip="'
						+ str(qstring)
						+ '" data-sortable="true" data-filter-control="input">'
						+ str(qstring)
						+ "</th>"
					)
			sec_str += '</tr></thead><tbody class ="user_id" ></tbody></table>'
			sec_str += '<div id="source_fablocation_footer"></div>'
			values_list = ""
			values_lists = ""
			a_test = []
			Doubleclick_Info = ''
			for invsk in list(Header_details):
				table_ids = "#" + str(table_id)
				filter_class = table_ids + " .bootstrap-table-filter-control-" + str(invsk)
				values_lists += "var " + str(invsk) + ' = $("' + str(filter_class) + '").val(); '
				values_lists += " ATTRIBUTE_VALUEList.push(" + str(invsk) + "); "
				#Trace.Write("66666 ---->"+str(values_lists))
				a_test.append(invsk)
				#Doubleclick_Info.append('$("' + str(filter_class) + '").val(); ')
				filter_control_function += (
					'$("'
					+ filter_class
					+ '").change( function(){ var table_id = $(this).closest("table").attr("id"); var a_list = '
					+ str(a_test)
					+ "; ATTRIBUTE_VALUEList = []; "
					+ str(values_lists)
					+ ' SortColumn = localStorage.getItem("SortColumn"); SortColumnOrder = localStorage.getItem("SortColumnOrder"); PerPage = $("#PageCountValue").val(); PageInform = "1___" + PerPage + "___" + PerPage; cpq.server.executeScript("SYUADNWPOP", {\'TABLEID\': "'
					+ str(TABLEID)
					+ "\", 'OPER': 'NO', 'RECORDID': \""
					+ str(RECORDID)
					+ "\", 'RECORDFEILD':  \""
					+ str(RECORDFEILD)
					+ "\", 'NEWVALUE': '', 'LOOKUPOBJ': '', 'LOOKUPAPI': '','A_Keys':a_list,'A_Values':ATTRIBUTE_VALUEList,'PerPage':PerPage,'PageInform':PageInform}, function(data) {  debugger; date_field  = data[3]; var assoc = data[1]; var api_name = data[2];data4 = data[4];data5 = data[5];data15 = data[15]; data16 = data[16]; try { if(date_field.length > 0) { $(\""
					+ str(table_ids)
					+ '").bootstrapTable("load", date_field  ); $("button#country_save").attr("disabled",false); $("#noRecDisp").remove();if (document.getElementById("RecordsStartAndEnd")){document.getElementById("RecordsStartAndEnd").innerHTML = data15;}; if (document.getElementById("TotalRecordsCount")) {document.getElementById("TotalRecordsCount").innerHTML = data16;} } else{ $("'
					+ str(table_ids)
					+ '").bootstrapTable("load", date_field  ); $("button#country_save").attr("disabled",true); $("#'+str(table_ids)+'").after("<div id=\'noRecDisp\' class=\'noRecord\'>No Records to Display</div>"); $(".noRecord:not(:first)").remove(); } } catch(err) { if(date_field.length > 0) { $("'
					+ str(table_ids)
					+ '").bootstrapTable("load", date_field  ); $("button#country_save").attr("disabled",false); } else{ $("'
					+ str(table_ids)
					+ '").bootstrapTable("load", date_field  ); $("button#country_save").attr("disabled",true); } } ; });  });'
				)
				# filter_control_function += (
				#     '$("'
				#     + filter_class
				#     + '").change( function(){ var table_id = $(this).closest("table").attr("id"); var a_list = '
				#     + str(a_test)
				#     + "; ATTRIBUTE_VALUEList = []; "
				#     + str(values_lists)
				#     + ' SortColumn = localStorage.getItem("SortColumn"); SortColumnOrder = localStorage.getItem("SortColumnOrder"); PerPage = $("#PageCountValue").val(); PageInform = "1___" + PerPage + "___" + PerPage; cpq.server.executeScript("SYUADNWPOP", {\'TABLEID\': "'
				#     + str(TABLEID)
				#     + "\", 'OPER': 'NO', 'RECORDID': \""
				#     + str(RECORDID)
				#     + "\", 'RECORDFEILD':  \""
				#     + str(RECORDFEILD)
				#     + "\", 'NEWVALUE': '', 'LOOKUPOBJ': '', 'LOOKUPAPI': '','A_Keys':a_list,'A_Values':ATTRIBUTE_VALUEList}, function(data) {  date_field = data[3]; var assoc = data[1]; var api_name = data[2];data4 = data[4];data5 = data[5]; try { if(date_field.length > 0) { $(\""
				#     + str(table_ids)
				#     + '").bootstrapTable("load", date_field  ); $("button#country_save").attr("disabled",false); $("#noRecDisp").remove() } else{ var date_field = [];$("'
				#     + str(table_ids)
				#     + '").bootstrapTable("load", date_field  ); $("button#country_save").attr("disabled",true); $("#'+str(table_ids)+'").after("<div id=\'noRecDisp\' class=\'noRecord\'>No Records to Display</div>"); $(".noRecord:not(:first)").remove(); } } catch(err) { if(date_field.length > 0) { $("'
				#     + str(table_ids)
				#     + '").bootstrapTable("load", date_field  ); $("button#country_save").attr("disabled",false); } else{ $("'
				#     + str(table_ids)
				#     + '").bootstrapTable("load", date_field  ); $("button#country_save").attr("disabled",true); } } ; });  }); console.log(datafield);'
				# )      
				dbl_clk_function = (
					'$("'
					+ str(table_ids)
					+ '").on("all.bs.table", function (e, name, args) { $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); });  $(".bs-checkbox input").addClass("custom"); $("'
					+ str(table_ids)
					+ "\").on('sort.bs.table', function (e, name, order) { console.log('sort.bs.table ============>', e); e.stopPropagation(); currenttab = $(\"ul#carttabs_head .active\").text().trim(); localStorage.setItem('"
					+ str(table_id)
					+ "_SortColumn', name); localStorage.setItem('"
					+ str(table_id)
					+ "_SortColumnOrder', order); ATTRIBUTE_VALUEList = []; "+str(values_lists)+" AddNewContainerSorting(name, order, '"
					+ str(table_id)
					+ "',"+str(a_test)+",ATTRIBUTE_VALUEList,'"+str(TABLEID)+"','"+str(RECORDID)+"','"+str(RECORDFEILD)+"'); }); "
					)
			# Trace.Write("757575 filter_control_function ---->"+str(filter_control_function))
			# Trace.Write("757575 dbl_clk_function ---->"+str(dbl_clk_function))
			pagination_condition = "OFFSET {Offset_Skip_Count} ROWS FETCH NEXT {Fetch_Count} ROWS ONLY".format(
				Offset_Skip_Count=offset_skip_count-1 if offset_skip_count%10==1 else offset_skip_count, Fetch_Count=fetch_count
			)
			stp_account_id = Product.GetGlobal("stp_account_id")
			Pagination_M = Sql.GetFirst(
				"SELECT COUNT(MAFBLC.CpqTableEntryId) as count FROM {} (NOLOCK) JOIN SAACNT (NOLOCK) ON MAFBLC.ACCOUNT_RECORD_ID = SAACNT.ACCOUNT_RECORD_ID WHERE MAFBLC.ACCOUNT_ID = '{}' AND FAB_LOCATION_ID NOT IN (SELECT SRCFBL_ID FROM SAQSCF (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' )".format(
					ObjectName,stp_account_id, contract_quote_record_id,quote_revision_record_id
				)
			)

			if str(PerPage) == "" and str(PageInform) == "":
				Page_start = 1
				Page_End = fetch_count
				PerPage = fetch_count
				PageInform = "1___"+str(fetch_count)+"___"+str(fetch_count)
			else:
				Page_start = int(PageInform.split("___")[0])
				Page_End = int(PageInform.split("___")[1])
				PerPage = PerPage

			order_by = ""
			if SortColumn != '' and SortColumnOrder !='':
				order_by = "order by "+SortColumn + " " + SortColumnOrder
			else:
				order_by = "order by FAB_LOCATION_NAME ASC"

			pop_val = {}

			if where_string:
				where_string += " AND"
			where_string += """ MAFBLC.ACCOUNT_ID = '{}' AND FAB_LOCATION_ID NOT IN (SELECT SRCFBL_ID FROM SAQSCF (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' )""".format(
				stp_account_id, contract_quote_record_id, quote_revision_record_id 
			)

			table_data = Sql.GetList(
				"select top {} {} from {} (NOLOCK) JOIN SAACNT (NOLOCK) ON MAFBLC.ACCOUNT_RECORD_ID = SAACNT.ACCOUNT_RECORD_ID {} {} ".format(PerPage,
					", ".join(ordered_keys),
					ObjectName,
					"WHERE " + where_string if where_string else "",
					order_by,pagination_condition
					
				)
			)
			table_data = Sql.GetList(
				"select {} from {} (NOLOCK) JOIN SAACNT (NOLOCK) ON MAFBLC.ACCOUNT_RECORD_ID = SAACNT.ACCOUNT_RECORD_ID {} {} {}".format(", ".join(ordered_keys),
					ObjectName,
					"WHERE " + where_string if where_string else "",
					order_by,pagination_condition
					
				)
			)

			QueryCountObj = Sql.GetFirst(
					"select count(*) as cnt from {} (NOLOCK) JOIN SAACNT (NOLOCK) ON MAFBLC.ACCOUNT_RECORD_ID = SAACNT.ACCOUNT_RECORD_ID {} ".format(                    
					ObjectName,
					"WHERE " + where_string if where_string else ""
					
				)
				)
			if QueryCountObj is not None:
				QryCount = QueryCountObj.cnt




			""" table_data_select = Sql.GetList(
				"select top 1000 FABLOCATION_ID,FABLOCATION_NAME from SAQFBL (NOLOCK) where QUOTE_FABLOCATION_RECORD_ID ='"
				+ str(contract_quote_record_ids)
				+ "'"
			)
			for qt_obj in table_data_select:
				cpqidval = CPQID.KeyCPQId.GetCPQId(ObjectName, str(qt_obj.COUNTRY_RECORD_ID))                
				selected_offerings_list_preslect.append(cpqidval) """

			if table_data is not None:
				for row_data in table_data:
					data_id = str(ObjectName)

					new_value_dict = {}
					""" if not selected_offerings_list:
						if row_data.FAB_LOCATION_RECORD_ID in selected_offerings_list_preslect:                            
							new_value_dict["SELECT"] = True
						else:
							new_value_dict["SELECT"] = False

					else:
						selected_offerings_list_guids = []
						for val in selected_offerings_list:
							recid = CPQID.KeyCPQId.GetKEYId(ObjectName, str(val))
							selected_offerings_list_guids.append(recid)                        
						if row_data.FAB_LOCATION_RECORD_ID in selected_offerings_list_guids:                            
							new_value_dict["SELECT"] = True
						else:
							new_value_dict["SELECT"] = False """

					for data in row_data:
						if str(data.Key) == "FAB_LOCATION_RECORD_ID":
							pop_val = str(data.Value) + "|Offerings"
							cpqidval = CPQID.KeyCPQId.GetCPQId(ObjectName, str(data.Value))
							new_value_dict[data.Key] = cpqidval
						else:
							new_value_dict[data.Key] = data.Value
						new_value_dict["pop_val"] = pop_val
					date_field.append(new_value_dict)
			QueryCount = len(date_field)

			pagination_total_count = 0
			if Pagination_M is not None:
				pagination_total_count = Pagination_M.count
			if offset_skip_count == 0:
				records_end = fetch_count
			if offset_skip_count%10==1:
				offset_skip_count=offset_skip_count-1
			records_end = offset_skip_count + fetch_count
			if records_end >= pagination_total_count:
				records_end=pagination_total_count
			records_start_and_end = "{} - {} of ".format(offset_skip_count+1, records_end)
			disable_next_and_last = ""
			disable_previous_and_first = ""
			if records_end == pagination_total_count:
				disable_next_and_last = "class='btn-is-disabled' style=\'pointer-events:none\' "
			if offset_skip_count == 0:
				disable_previous_and_first = "class='btn-is-disabled' style=\'pointer-events:none\' "
			current_page = int(math.ceil(offset_skip_count / fetch_count)) + 1

			Product.SetGlobal("QueryCount", str(QueryCount))
			pagination_table_id = "pagination_{}".format(table_id)
			if QueryCount != 0:
				var_str += """<div id="{Parent_Div_Id}" class="col-md-12 brdr listContStyle padbthgt30">
						<div class="col-md-4 pager-numberofitem  clear-padding">
							<span class="pager-number-of-items-item flt_lt_pad2_mar2022" id="RecordsStartAndEnd">{Records_Start_And_End}</span>
							<span class="pager-number-of-items-item flt_lt_pad2_mar" id="TotalRecordsCount">{Pagination_Total_Count}</span>
								<div class="clear-padding fltltmrgtp3">
									<div class="pull-right vralign">
										<select onchange="ShowResultCountFunc(this, '{ShowResultCountFuncTb}', 'addFab', '{TableId}')" id="ShowResultCount" class="form-control selcwdt">
											<option value="10" {Selected_10}>10</option>
											<option value="20" {Selected_20}>20</option>
											<option value="50" {Selected_50}>50</option>
											<option value="100" {Selected_100}>100</option>
											<option value="200" {Selected_200}>200</option>
										</select>
									</div>
								</div>
						</div>
							<div class="col-xs-8 col-md-4  clear-padding inpadtex" data-bind="visible: totalItemCount">
								<div class="clear-padding col-xs-12 col-sm-6 col-md-12 brd0">
									<ul class="pagination pagination">
										<li class="disabled">
											<a onclick="GetFirstResultFunc('{GetFirstResultFuncTb}', 'addFab', '{TableId}')" {Disable_First}><i class="fa fa-caret-left fnt14bold"></i><i class="fa fa-caret-left fnt14"></i></a>
										</li>
										<li class="disabled"><a onclick="GetPreviuosResultFunc('{GetPreviuosResultFuncTb}', 'addFab', '{TableId}')" {Disable_Previous}><i class="fa fa-caret-left fnt14"></i>PREVIOUS</a></li>
										<li class="disabled"><a onclick="GetNextResultFunc('{GetNextResultFuncTb}', 'addFab', '{TableId}')" {Disable_Next}>NEXT<i class="fa fa-caret-right fnt14"></i></a></li>
										<li class="disabled"><a onclick="GetLastResultFunc('{GetLastResultFuncTb}', 'addFab', '{TableId}')" {Disable_Last}><i class="fa fa-caret-right fnt14"></i><i class="fa fa-caret-right fnt14bold"></i></a></li>
									</ul>
								</div>
							</div>
							<div class="col-md-4 pad3">
							<span id="page_count" class="currentPage page_right_content">{Current_Page}</span>
								<span class="page_right_content padrt2">Page </span>
							</div>
					</div></div>""".format(
					Parent_Div_Id=pagination_table_id,
					Records_Start_And_End=records_start_and_end,
					Pagination_Total_Count=pagination_total_count,
					ShowResultCountFuncTb=pagination_table_id,
					Selected_10="selected" if fetch_count == 10 else "",
					Selected_20="selected" if fetch_count == 20 else "",
					Selected_50="selected" if fetch_count == 50 else "",
					Selected_100="selected" if fetch_count == 100 else "",
					Selected_200="selected" if fetch_count == 200 else "",
					GetFirstResultFuncTb=pagination_table_id,
					Disable_First=disable_previous_and_first,
					GetPreviuosResultFuncTb=pagination_table_id,
					Disable_Previous=disable_previous_and_first,
					GetNextResultFuncTb=pagination_table_id,
					Disable_Next=disable_next_and_last,
					GetLastResultFuncTb=pagination_table_id,
					Disable_Last=disable_next_and_last,
					Current_Page=current_page,
					TableId=TABLEID,
				)
			else:
				date_field = "NORECORDS"
				Trace.Write("No Equipment Records")
			table_ids = "#" + str(table_id)
			# Filter based on table MultiSelect Dropdown column - Start

			for index, col_name in enumerate(ordered_keys):
				table, api_name = ObjectName, col_name
				obj_data = Sql.GetFirst(
					"SELECT API_NAME, DATA_TYPE, PICKLIST FROM  SYOBJD WHERE OBJECT_NAME='"
					+ str(table)
					+ "' and API_NAME = '"
					+ str(api_name)
					+ "'"
				)
				if obj_data is not None:
					if str(obj_data.PICKLIST).upper() == "TRUE":
						filter_tag = (
							'<div id = "'
							+ str(table_id)
							+ "_RelatedMutipleCheckBoxDrop_"
							+ str(index)
							+ '" class="form-control bootstrap-table-filter-control-'
							+ str(api_name)
							+ " RelatedMutipleCheckBoxDrop_"
							+ str(index)
							+ ' "></div>'
						)
						filter_tags.append(filter_tag)
						filter_types.append("select")
						if obj_data.DATA_TYPE == "CHECKBOX":
							filter_values.append(["True", "False"])
						else:
							data_obj = Sql.GetList(
								"SELECT DISTINCT {Column} FROM {Table}".format(Column=api_name, Table=table)
							)
							if data_obj is not None:
								filter_values.append([row_data.Value for data in data_obj for row_data in data])
					else:
						filter_tag = (
							'<input type="text" class="form-control wth100visble bootstrap-table-filter-control-'
							+ str(api_name)
							+ '">'
						)
						filter_tags.append(filter_tag)
						filter_types.append("input")
						filter_values.append("")

			filter_drop_down = (
				"try { if( document.getElementById('"
				+ str(table_id)
				+ "') ) { var listws = document.getElementById('"
				+ str(table_id)
				+ "').getElementsByClassName('filter-control');  for (i = 0; i < listws.length; i++) { document.getElementById('"
				+ str(table_id)
				+ "').getElementsByClassName('filter-control')[i].innerHTML = data6[i];  } for (j = 0; j < listws.length; j++) { if (data10[j] == 'select') { var dataAdapter = new $.jqx.dataAdapter(data8[j]); if(data11[j].length>5){ $('#"
				+ str(table_id)
				+ "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter}); }else{$('#"
				+ str(table_id)
				+ "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter ,autoDropDownHeight: true});} } } } }  catch(err) { setTimeout(function() { var listws = document.getElementById('"
				+ str(table_id)
				+ "').getElementsByClassName('filter-control');  for (i = 0; i < listws.length; i++) { document.getElementById('"
				+ str(table_id)
				+ "').getElementsByClassName('filter-control')[i].innerHTML = data9[i];  } for (j = 0; j < listws.length; j++) { if (data10[j] == 'select') { var dataAdapter = new $.jqx.dataAdapter(data11[j]); $('#"
				+ str(table_id)
				+ "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter, scrollBarSize :10 }); } } }, 5000); }"
			)
			dbl_clk_function += (
				'$("'
				+ str(table_ids)
				+ '").on("all.bs.table", function (e, name, args) { $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); }); $("'
				+ str(table_ids)
				+ '\ th.bs-checkbox div.th-inner").before("<div class=\'pad0brdbt\'>SELECT</div>"); $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>");'
			)

			pagedata = ""
			if QryCount < int(PerPage):
				pagedata = str(Page_start) + " - " + str(QryCount) + " of "
			else:
				pagedata = str(Page_start) + " - " + str(Page_End)+ " of "
			
		
		##involved party equipment starts
		elif str(ObjectName) == "SAQSTE" and str(CurrentTab) == "Quotes":
			where_string = ""
			TreeParam = Product.GetGlobal("TreeParam")
			
			if A_Keys != "" and A_Values != "":
				A_Keys = list(A_Keys)
				A_Values = list(A_Values)
				for key, value in zip(A_Keys, A_Values):
					if value.strip():
						if where_string:
							where_string += " AND "
						where_string += "{Key} LIKE '%{Value}%'".format(Key=key, Value=value)
			DIVNAME = "VIEW_DIV_ID"
			new_value_dict = {}
			ObjectName = "MAEQUP"
			table_id = "involved_parties_equipment_addnew"
			Header_details = {
				"EQUIPMENT_RECORD_ID": "KEY",
				"EQUIPMENT_ID":"EQUIPMENT ID",
				"GREENBOOK": "GREENBOOK",
				"PLATFORM": "PLATFORM",
			}
			ordered_keys = [
				"EQUIPMENT_RECORD_ID",
				"EQUIPMENT_ID",
				"GREENBOOK",
				"PLATFORM",
			]
			Objd_Obj = Sql.GetList(
				"select FIELD_LABEL,API_NAME,LOOKUP_OBJECT,LOOKUP_API_NAME,DATA_TYPE,FORMULA_DATA_TYPE from SYOBJD (NOLOCK)where OBJECT_NAME = '"
				+ str(ObjectName)
				+ "'"
			)
			lookup_disply_list = []
			if Objd_Obj is not None:
				attr_list = {}
				api_names = [inn.API_NAME for inn in Objd_Obj]
				for attr in Objd_Obj:
					attr_list[str(attr.API_NAME)] = str(attr.FIELD_LABEL)
					if str(attr.LOOKUP_API_NAME) != "" and str(attr.LOOKUP_API_NAME) is not None:
						lookup_disply_list.append(str(attr.API_NAME))
				checkbox_list = [
					inn.API_NAME for inn in Objd_Obj if (inn.DATA_TYPE == "CHECKBOX" or inn.FORMULA_DATA_TYPE == "CHECKBOX")
				]
				lookup_list = {ins.LOOKUP_API_NAME: ins.API_NAME for ins in Objd_Obj}
				sec_str = '<div class="row modulebnr brdr ma_mar_btm">INSTALLED BASE EQUIPMENT LIST<button type="button" id = "involved_parties_equipment" class="close flt_rt" onclick="closepopup_scrl(this)" data-dismiss="modal">X</button></div>'
				sec_str += '<div class="col-md-12 padlftrhtnone" id="btnhide"><div class="row pad-10 bg-lt-wt brdr"><img style="height: 40px; margin-top: -1px; margin-left: -1px; float: left;" src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/Secondary Icon.svg"/><div class="product_txt_div_child secondary_highlight" style="display: block;"><div class="product_txt_child"><abbr title="Source Account ID">Source Account ID</abbr></div><div class="product_txt_to_top_child" style="float: left;"><abbr title="{}">{}</abbr></div></div><div class="product_txt_div_child secondary_highlight" style="display: block;"><div class="product_txt_child"><abbr title="Source Account Name">Source Account Name</abbr></div><div class="product_txt_to_top_child" style="float: left;"><abbr title="{}">{}</abbr></div></div><div class="product_txt_div_child secondary_highlight" style="display: block;"></div><div class="product_txt_div_child secondary_highlight" style="display: block;"><div class="product_txt_child"><abbr title="Source Fab Location ID">Source Fab Location ID</abbr></div><div class="product_txt_to_top_child" style="float: left;"><abbr title="All">All</abbr></div></div><div class="product_txt_div_child secondary_highlight" style="display: block;"><div class="product_txt_child"><abbr title="Equipment">Equipment</abbr></div><div class="product_txt_to_top_child" style="float: left;"><abbr title="All">All</abbr></div></div><button type="button" class="btnconfig" data-dismiss="modal" id = "involved_parties_equipment" onclick="closepopup_scrl(this)">CANCEL</button><button type="button" id="add-equipment" class="btnconfig" onclick="addtoolrelocationequipment()" data-dismiss="modal">ADD</button></div></div>'.format(
				Product.GetGlobal("stp_account_Id"), Product.GetGlobal("stp_account_Id"), Product.GetGlobal("stp_account_name"), Product.GetGlobal("stp_account_name")
			)

			sec_str += '<div id="container" class="g4 pad-10 brdr except_sec">'
			sec_str += (
				'<table id="'
				+ str(table_id)
				+ '" data-escape="true"  data-search-on-enter-key="true" data-show-header="true"  data-filter-control="true"> <thead><tr>'
			)
			sec_str += '<th data-field="SELECT" class="wth45" data-checkbox="true" id ="check_boxval" onchange = "get_checkedval()"><div class="action_col">SELECT</div></th>'

			for key, invs in enumerate(list(ordered_keys)):

				invs = str(invs).strip()
				qstring = Header_details.get(str(invs)) or ""
				if key == 0:
					sec_str += (
						'<th data-field="'
						+ str(invs)
						+ '" data-formatter="toolrelocationKeyHyperLink" data-sortable="true" data-title-tooltip="'
						+ str(qstring)
						+ '" data-filter-control="input">'
						+ str(qstring)
						+ "</th>"
					)
				else:
					sec_str += (
						'<th data-field="'
						+ invs
						+ '" data-title-tooltip="'
						+ str(qstring)
						+ '" data-sortable="true" data-filter-control="input">'
						+ str(qstring)
						+ "</th>"
					)
			sec_str += '</tr></thead><tbody class ="equipments_id" ></tbody></table>'
			sec_str += '<div id="involved_parties_equipment_addnew_footer"></div>'
			values_list = ""
			values_lists = ""
			a_test = []
			for invsk in list(Header_details):
				table_ids = "#" + str(table_id)
				filter_class = table_ids + " .bootstrap-table-filter-control-" + str(invsk)
				values_lists += "var " + str(invsk) + ' = $("' + str(filter_class) + '").val(); '
				values_lists += " ATTRIBUTE_VALUEList.push(" + str(invsk) + "); "
				a_test.append(invsk)
				filter_control_function += (
					'$("'
					+ filter_class
					+ '").change( function(){ var table_id = $(this).closest("table").attr("id"); var a_list = '
					+ str(a_test)
					+ "; ATTRIBUTE_VALUEList = []; "
					+ str(values_lists)
					+ ' SortColumn = localStorage.getItem("SortColumn"); SortColumnOrder = localStorage.getItem("SortColumnOrder"); PerPage = $("#PageCountValue").val(); PageInform = "1___" + PerPage + "___" + PerPage; cpq.server.executeScript("SYUADNWPOP", {\'TABLEID\': "'
					+ str(TABLEID)
					+ "\", 'OPER': 'NO', 'RECORDID': \""
					+ str(RECORDID)
					+ "\", 'RECORDFEILD':  \""
					+ str(RECORDFEILD)
					+ "\", 'NEWVALUE': '', 'LOOKUPOBJ': '', 'LOOKUPAPI': '','A_Keys':a_list,'A_Values':ATTRIBUTE_VALUEList}, function(data) {  date_field = data[3]; var assoc = data[1]; var api_name = data[2];data4 = data[4];data5 = data[5]; try { if(date_field.length > 0) { $(\""
					+ str(table_ids)
					+ '").bootstrapTable("load", date_field  ); $("button#country_save").attr("disabled",false); $("#noRecDisp").remove() } else{ var date_field = [];$("'
					+ str(table_ids)
					+ '").bootstrapTable("load", date_field  ); $("button#country_save").attr("disabled",true); $("#involved_parties_equipment_addnew").after("<div id=\'noRecDisp\' class=\'noRecord\'>No Records to Display</div>"); $(".noRecord:not(:first)").remove(); } } catch(err) { if(date_field.length > 0) { $("'
					+ str(table_ids)
					+ '").bootstrapTable("load", date_field  ); $("button#country_save").attr("disabled",false); } else{ $("'
					+ str(table_ids)
					+ '").bootstrapTable("load", date_field  ); $("button#country_save").attr("disabled",true); } } ; });  });'
				)
				

			sales_org_record_id = None
			account_record_id = None
			quote_obj = Sql.GetFirst(
				"SELECT SAQTMT.ACCOUNT_RECORD_ID, SAQTRV.SALESORG_RECORD_ID FROM SAQTMT (NOLOCK) JOIN SAQTRV (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQTRV.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = SAQTRV.QTEREV_RECORD_ID WHERE SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = '{}' AND SAQTMT.QTEREV_RECORD_ID = '{}'".format(
					contract_quote_record_id,quote_revision_record_id
				)
			)
			if quote_obj:
				sales_org_record_id = quote_obj.SALESORG_RECORD_ID
				account_record_id = quote_obj.ACCOUNT_RECORD_ID
			pagination_condition = "OFFSET {Offset_Skip_Count} ROWS FETCH NEXT {Fetch_Count} ROWS ONLY".format(
				Offset_Skip_Count=offset_skip_count-1 if offset_skip_count%10==1 else offset_skip_count, Fetch_Count=fetch_count
			)

			Pagination_M = Sql.GetFirst(
				"select count(MAEQUP.CpqTableEntryId) as count from MAEQUP (NOLOCK) inner join SAQSCF (NOLOCK) on MAEQUP.FABLOCATION_RECORD_ID = SAQSCF.SRCFBL_RECORD_ID and MAEQUP.ACCOUNT_RECORD_ID = SAQSCF.SRCACC_RECORD_ID and MAEQUP.FABLOCATION_ID = SAQSCF.SRCFBL_ID inner join  MAFBLC (nolock) on MAFBLC.FAB_LOCATION_ID = SAQSCF.SRCFBL_ID AND MAFBLC.ACCOUNT_ID = SAQSCF.SRCACC_ID AND MAEQUP.PAR_EQUIPMENT_ID = '' AND SAQSCF.QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' WHERE MAEQUP.GREENBOOK_RECORD_ID != '' AND MAEQUP.GREENBOOK_RECORD_ID is not null AND MAEQUP.EQUIPMENT_ID  NOT IN (SELECT EQUIPMENT_ID FROM SAQSTE (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}')".format(
				contract_quote_record_id,quote_revision_record_id, contract_quote_record_id,quote_revision_record_id
				)
			)

			order_by = "order by MAEQUP.FABLOCATION_NAME ASC"

			if str(PerPage) == "" and str(PageInform) == "":
				Page_start = 1
				Page_End = fetch_count
				PerPage = fetch_count
				PageInform = "1___"+str(fetch_count)+"___"+str(fetch_count)
			else:
				Page_start = int(PageInform.split("___")[0])
				Page_End = int(PageInform.split("___")[1])
				PerPage = PerPage

			order_by = ""
			if SortColumn != '' and SortColumnOrder !='':
				order_by = "order by "+SortColumn + " " + SortColumnOrder
			else:
				order_by = "order by FAB_LOCATION_NAME ASC"

			pop_val = {}
			if where_string:
				where_string += " AND"
				Trace.Write("soureceequipments "+str(where_string))
			if TreeParam == "Quote Information":
				where_string += """ MAEQUP.GREENBOOK_RECORD_ID != '' AND MAEQUP.GREENBOOK_RECORD_ID is not null AND MAEQUP.EQUIPMENT_ID  NOT IN (SELECT EQUIPMENT_ID FROM SAQSTE (NOLOCK) where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}')""".format(contract_quote_record_id,quote_revision_record_id)
			
			
			# table_data = Sql.GetList(
			#     "select {} from MAEQUP (NOLOCK) inner join SAQSCF (NOLOCK) on MAEQUP.FABLOCATION_RECORD_ID = SAQSCF.SRCFBL_RECORD_ID and MAEQUP.ACCOUNT_RECORD_ID = SAQSCF.SRCACC_RECORD_ID and MAEQUP.FABLOCATION_ID = SAQSCF.SRCFBL_ID inner join  MAFBLC (nolock) on MAFBLC.FAB_LOCATION_ID = SAQSCF.SRCFBL_ID AND MAFBLC.ACCOUNT_ID = SAQSCF.SRCACC_ID AND MAEQUP.PAR_EQUIPMENT_ID is null AND SAQSCF.QUOTE_RECORD_ID = '{}' WHERE MAEQUP.GREENBOOK_RECORD_ID != '' AND MAEQUP.GREENBOOK_RECORD_ID is not null AND MAEQUP.EQUIPMENT_ID  NOT IN (SELECT EQUIPMENT_ID FROM SAQSTE (NOLOCK) where QUOTE_RECORD_ID = '{}') {} {}".format(
			#         ", ".join(ordered_keys),
			#         contract_quote_record_id,
			#         contract_quote_record_id,
			#         order_by,
			#         pagination_condition,
			#     )
			# )
			table_data = Sql.GetList(
				"select {} from MAEQUP (NOLOCK) inner join SAQSCF (NOLOCK) on MAEQUP.FABLOCATION_RECORD_ID = SAQSCF.SRCFBL_RECORD_ID and MAEQUP.ACCOUNT_RECORD_ID = SAQSCF.SRCACC_RECORD_ID and MAEQUP.FABLOCATION_ID = SAQSCF.SRCFBL_ID inner join  MAFBLC (nolock) on MAFBLC.FAB_LOCATION_ID = SAQSCF.SRCFBL_ID AND MAFBLC.ACCOUNT_ID = SAQSCF.SRCACC_ID AND MAEQUP.PAR_EQUIPMENT_ID = '' AND SAQSCF.QUOTE_RECORD_ID = '{}' {} {} {}".format(", ".join(ordered_keys),contract_quote_record_id,"WHERE " +where_string if where_string else "",order_by,
					pagination_condition,
				)
			)
			QueryCountObj = Sql.GetFirst(
				"select count(*) as cnt from MAEQUP (NOLOCK) inner join SAQSCF (NOLOCK) on MAEQUP.FABLOCATION_RECORD_ID = SAQSCF.SRCFBL_RECORD_ID and MAEQUP.ACCOUNT_RECORD_ID = SAQSCF.SRCACC_RECORD_ID and MAEQUP.FABLOCATION_ID = SAQSCF.SRCFBL_ID inner join  MAFBLC (nolock) on MAFBLC.FAB_LOCATION_ID = SAQSCF.SRCFBL_ID AND MAFBLC.ACCOUNT_ID = SAQSCF.SRCACC_ID AND MAEQUP.PAR_EQUIPMENT_ID is null AND SAQSCF.QUOTE_RECORD_ID = '{}' {}".format(
				contract_quote_record_id, "WHERE " +where_string if where_string else ""
				)
			)
			# modified where condition in above query to display correct count
			# WHERE MAEQUP.GREENBOOK_RECORD_ID != '' AND MAEQUP.GREENBOOK_RECORD_ID is not null AND MAEQUP.EQUIPMENT_ID  NOT IN (SELECT EQUIPMENT_ID FROM SAQSTE (NOLOCK) WHERE QUOTE_RECORD_ID = '{}'
			if QueryCountObj is not None:
				QryCount = QueryCountObj.cnt


			if table_data is not None :
				for row_data in table_data:
					data_id = str(ObjectName)

					new_value_dict = {}

					for data in row_data:
						if str(data.Key) == "EQUIPMENT_RECORD_ID":
							pop_val = str(data.Value) + "|equipments"
							cpqidval = CPQID.KeyCPQId.GetCPQId(ObjectName, str(data.Value))
							new_value_dict[data.Key] = cpqidval
						else:
							new_value_dict[data.Key] = data.Value
						new_value_dict["pop_val"] = pop_val
					date_field.append(new_value_dict)
			QueryCount = len(date_field)

			pagination_total_count = 0
			if Pagination_M is not None:
				pagination_total_count = Pagination_M.count
			if offset_skip_count == 0:
				offset_skip_count = 1
				records_end = fetch_count
			records_end = offset_skip_count + fetch_count - 1
			records_end = pagination_total_count if pagination_total_count < records_end else records_end
			records_start_and_end = "{} - {} of ".format(offset_skip_count, records_end)
			disable_next_and_last = ""
			disable_previous_and_first = ""
			if records_end == pagination_total_count:
				disable_next_and_last = "class='btn-is-disabled' style=\'pointer-events:none\' "
			if offset_skip_count == 0:
				disable_previous_and_first = "class='btn-is-disabled' style=\'pointer-events:none\' "
			current_page = int(math.ceil(offset_skip_count / fetch_count)) + 1

			Product.SetGlobal("QueryCount", str(QueryCount))
			pagination_table_id = "pagination_{}".format(table_id)
			if QueryCount != 0:
				var_str = """<div id="{Parent_Div_Id}" class="col-md-12 brdr listContStyle padbthgt30">
									<div class="col-md-4 pager-numberofitem  clear-padding">
										<span class="pager-number-of-items-item flt_lt_pad2_mar2022" id="RecordsStartAndEnd">{Records_Start_And_End}</span>
										<span class="pager-number-of-items-item flt_lt_pad2_mar" id="TotalRecordsCount">{Pagination_Total_Count}</span>
										<div class="clear-padding fltltmrgtp3">
											<div class="pull-right vralign">
												<select onchange="ShowResultCountFunc(this, '{ShowResultCountFuncTb}', 'addEquipment', '{TableId}')" id="ShowResultCount" class="form-control selcwdt">
													<option value="10" {Selected_10}>10</option>
													<option value="20" {Selected_20}>20</option>
													<option value="50" {Selected_50}>50</option>
													<option value="100" {Selected_100}>100</option>
													<option value="200" {Selected_200}>200</option>
												</select> 
											</div>
										</div>
									</div>
									<div class="col-xs-8 col-md-4  clear-padding inpadtex" data-bind="visible: totalItemCount">
										<div class="clear-padding col-xs-12 col-sm-6 col-md-12 brd0">
											<ul class="pagination pagination">
												<li class="disabled">
													<a onclick="GetFirstResultFunc('{GetFirstResultFuncTb}', 'addEquipment', '{TableId}')" {Disable_First}><i class="fa fa-caret-left fnt14bold"></i><i class="fa fa-caret-left fnt14"></i></a>
												</li>
												<li class="disabled"><a onclick="GetPreviuosResultFunc('{GetPreviuosResultFuncTb}', 'addEquipment', '{TableId}')" {Disable_Previous}><i class="fa fa-caret-left fnt14"></i>PREVIOUS</a></li>
												<li class="disabled"><a onclick="GetNextResultFunc('{GetNextResultFuncTb}', 'addEquipment', '{TableId}')" {Disable_Next}>NEXT<i class="fa fa-caret-right fnt14"></i></a></li>
												<li class="disabled"><a onclick="GetLastResultFunc('{GetLastResultFuncTb}', 'addEquipment', '{TableId}')" {Disable_Last}><i class="fa fa-caret-right fnt14"></i><i class="fa fa-caret-right fnt14bold"></i></a></li>
											</ul>
										</div> 
									</div> 
									<div class="col-md-4 pad3"> 
										<span id="page_count" class="currentPage page_right_content">{Current_Page}</span>
										<span class="page_right_content padrt2">Page </span>
									</div>
								</div>""".format(
					Parent_Div_Id=pagination_table_id,
					Records_Start_And_End=records_start_and_end,
					Pagination_Total_Count=pagination_total_count,
					ShowResultCountFuncTb=pagination_table_id,
					Selected_10="selected" if fetch_count == 10 else "",
					Selected_20="selected" if fetch_count == 20 else "",
					Selected_50="selected" if fetch_count == 50 else "",
					Selected_100="selected" if fetch_count == 100 else "",
					Selected_200="selected" if fetch_count == 200 else "",
					GetFirstResultFuncTb=pagination_table_id,
					Disable_First=disable_previous_and_first,
					GetPreviuosResultFuncTb=pagination_table_id,
					Disable_Previous=disable_previous_and_first,
					GetNextResultFuncTb=pagination_table_id,
					Disable_Next=disable_next_and_last,
					GetLastResultFuncTb=pagination_table_id,
					Disable_Last=disable_next_and_last,
					Current_Page=current_page,
					TableId=TABLEID,
				)
			else:
				date_field = "NORECORDS"
				Trace.Write("No Equipment Records")
			table_ids = "#" + str(table_id)
			# Filter based on table MultiSelect Dropdown column - Start

			for index, col_name in enumerate(ordered_keys):
				table, api_name = ObjectName, col_name
				obj_data = Sql.GetFirst(
					"SELECT API_NAME, DATA_TYPE, PICKLIST FROM  SYOBJD WHERE OBJECT_NAME='"
					+ str(table)
					+ "' and API_NAME = '"
					+ str(api_name)
					+ "'"
				)
				if obj_data is not None:
					if str(obj_data.PICKLIST).upper() == "TRUE":
						filter_tag = (
							'<div id = "'
							+ str(table_id)
							+ "_RelatedMutipleCheckBoxDrop_"
							+ str(index)
							+ '" class="form-control bootstrap-table-filter-control-'
							+ str(api_name)
							+ " RelatedMutipleCheckBoxDrop_"
							+ str(index)
							+ ' "></div>'
						)
						filter_tags.append(filter_tag)
						filter_types.append("select")
						if obj_data.DATA_TYPE == "CHECKBOX":
							filter_values.append(["True", "False"])
						else:
							# Trace.Write("=============$$$$$$$$$$$$$>>>>>>>>>>>>> "+"SELECT DISTINCT {Column} FROM {Table}".format(Column=api_name, Table=table))
							data_obj = Sql.GetList(
								"SELECT DISTINCT {Column} FROM {Table}".format(Column=api_name, Table=table)
							)
							if data_obj is not None:
								filter_values.append([row_data.Value for data in data_obj for row_data in data])
					else:
						filter_tag = (
							'<input type="text" class="form-control wth100visble bootstrap-table-filter-control-'
							+ str(api_name)
							+ '">'
						)
						filter_tags.append(filter_tag)
						filter_types.append("input")
						filter_values.append("")

			filter_drop_down = (
				"try { if( document.getElementById('"
				+ str(table_id)
				+ "') ) { var listws = document.getElementById('"
				+ str(table_id)
				+ "').getElementsByClassName('filter-control');  for (i = 0; i < listws.length; i++) { document.getElementById('"
				+ str(table_id)
				+ "').getElementsByClassName('filter-control')[i].innerHTML = data6[i];  } for (j = 0; j < listws.length; j++) { if (data10[j] == 'select') { var dataAdapter = new $.jqx.dataAdapter(data8[j]); if(data11[j].length>5){ $('#"
				+ str(table_id)
				+ "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter}); }else{$('#"
				+ str(table_id)
				+ "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter ,autoDropDownHeight: true});} } } } }  catch(err) { setTimeout(function() { var listws = document.getElementById('"
				+ str(table_id)
				+ "').getElementsByClassName('filter-control');  for (i = 0; i < listws.length; i++) { document.getElementById('"
				+ str(table_id)
				+ "').getElementsByClassName('filter-control')[i].innerHTML = data9[i];  } for (j = 0; j < listws.length; j++) { if (data10[j] == 'select') { var dataAdapter = new $.jqx.dataAdapter(data11[j]); $('#"
				+ str(table_id)
				+ "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter, scrollBarSize :10 }); } } }, 5000); }"
			)
			dbl_clk_function += (
				'$("'
				+ str(table_ids)
				+ '").on("all.bs.table", function (e, name, args) { $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); }); $("'
				+ str(table_ids)
				+ '\ th.bs-checkbox div.th-inner").before("<div class=\'pad0brdbt\'>SELECT</div>"); $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>");'
			)

			pagedata = ""
			if QryCount < int(PerPage):
				pagedata = str(Page_start) + " - " + str(QryCount) + " of "
			else:
				pagedata = str(Page_start) + " - " + str(Page_End)+ " of "
			

		##involved party equipment ends
		
		elif str(ObjectName) == "SAQSAO" and str(CurrentTab) == "Quotes":
			where_string = ""
			TreeParam = Product.GetGlobal("TreeParam")
			TreeParentParam = Product.GetGlobal("TreeParentLevel0")
			TreeSuperParentParam = Product.GetGlobal("TreeParentLevel1")
			
			
			if A_Keys != "" and A_Values != "":
				A_Keys = list(A_Keys)
				A_Values = list(A_Values)
				for key, value in zip(A_Keys, A_Values):
					if value.strip():
						if where_string:
							where_string += " AND "
						where_string += "{Key} LIKE '%{Value}%'".format(Key=key, Value=value)
			DIVNAME = "VIEW_DIV_ID"
			new_value_dict = {}
			ObjectName = "MAADPR"
			table_id = "Include_add_on_addnew"
			Header_details = {
				"PO_COMP_RECORD_ID": "KEY",
				"COMP_PRDOFR_ID":"SERVICE ID",
				"COMP_PRDOFR_NAME": "SERVICE NAME",
				"COMP_PRDOFR_TYPE": "TYPE",
			}
			ordered_keys = [
				#"ADD_ON_PRODUCT_RECORD_ID",
				"PO_COMP_RECORD_ID",
				"COMP_PRDOFR_ID",
				"COMP_PRDOFR_NAME",
				"COMP_PRDOFR_TYPE",
			]
			Objd_Obj = Sql.GetList(
				"select FIELD_LABEL,API_NAME,LOOKUP_OBJECT,LOOKUP_API_NAME,DATA_TYPE,FORMULA_DATA_TYPE from SYOBJD (NOLOCK)where OBJECT_NAME = '"
				+ str(ObjectName)
				+ "'"
			)
			TreeSuperParentParam =  Product.GetGlobal("TreeParentLevel1") 
			getService = Sql.GetFirst("select SERVICE_DESCRIPTION from SAQTSV(nolock) where SERVICE_ID = '"+str(TreeSuperParentParam)+"'")
			getDocType = Sql.GetFirst("SELECT DOCTYP_ID FROM SAQTRV WHERE QUOTE_RECORD_ID = '"+str(contract_quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' ")
			lookup_disply_list = []
			if Objd_Obj is not None:
				attr_list = {}
				api_names = [inn.API_NAME for inn in Objd_Obj]
				for attr in Objd_Obj:
					attr_list[str(attr.API_NAME)] = str(attr.FIELD_LABEL)
					if str(attr.LOOKUP_API_NAME) != "" and str(attr.LOOKUP_API_NAME) is not None:
						lookup_disply_list.append(str(attr.API_NAME))
				checkbox_list = [
					inn.API_NAME for inn in Objd_Obj if (inn.DATA_TYPE == "CHECKBOX" or inn.FORMULA_DATA_TYPE == "CHECKBOX")
				]
				lookup_list = {ins.LOOKUP_API_NAME: ins.API_NAME for ins in Objd_Obj}
				sec_str = '<div class="row modulebnr brdr ma_mar_btm">ADD-ON PRODUCT LIST<button type="button" id = "Include_add_on" class="close flt_rt" onclick="closepopup_scrl(this)" data-dismiss="modal">X</button></div>'
				sec_str += '<div class="col-md-12 padlftrhtnone" id="btnhide"><div class="row pad-10 bg-lt-wt brdr"><img style="height: 40px; margin-top: -1px; margin-left: -1px; float: left;" src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/Secondary Icon.svg"/><div class="product_txt_div_child secondary_highlight" style="display: block;"></div><div class="product_txt_div_child secondary_highlight" style="display: block;"><div class="product_txt_child"><abbr title="Service ID">Service ID</abbr></div><div class="product_txt_to_top_child" style="float: left;"><abbr title="{}">{}</abbr></div></div><div class="product_txt_div_child secondary_highlight" style="display: block;"><div class="product_txt_child"><abbr title="Service Description">Service Description</abbr></div><div class="product_txt_to_top_child" style="float: left;"><abbr title="{}">{}</abbr></div></div><div class="product_txt_div_child secondary_highlight" style="display: block;"><div class="product_txt_child"><abbr title="Add-On">Add-On</abbr></div><div class="product_txt_to_top_child" style="float: left;"><abbr title="All">All</abbr></div></div><button type="button" class="btnconfig" data-dismiss="modal" id = "Include_add_on" onclick="closepopup_scrl(this)">CANCEL</button><button type="button" id="add-equipment" class="btnconfig" onclick="addon_products()" data-dismiss="modal">ADD</button></div></div>'.format(
				Product.GetGlobal("TreeParentLevel1"),Product.GetGlobal("TreeParentLevel1"),
				getService.SERVICE_DESCRIPTION,getService.SERVICE_DESCRIPTION

			)

			sec_str += '<div id="container" class="g4 pad-10 brdr except_sec">'
			sec_str += (
				'<table id="'
				+ str(table_id)
				+ '" data-escape="true"  data-search-on-enter-key="true" data-show-header="true"  data-filter-control="true"> <thead><tr>'
			)
			sec_str += '<th data-field="SELECT" class="wth45" data-checkbox="true" id ="check_boxval" onchange = "get_checkedval()"><div class="action_col">SELECT</div></th>'

			for key, invs in enumerate(list(ordered_keys)):

				invs = str(invs).strip()
				qstring = Header_details.get(str(invs)) or ""
				if key == 0:
					sec_str += (
						'<th data-field="'
						+ str(invs)
						+ '" data-formatter="add_on_prdListKeyHyperLink" data-sortable="true" data-title-tooltip="'
						+ str(qstring)
						+ '" data-filter-control="input">'
						+ str(qstring)
						+ "</th>"
					)
				else:
					sec_str += (
						'<th data-field="'
						+ invs
						+ '" data-title-tooltip="'
						+ str(qstring)
						+ '" data-sortable="true" data-filter-control="input">'
						+ str(qstring)
						+ "</th>"
					)
			sec_str += '</tr></thead><tbody class ="equipments_id" ></tbody></table>'
			sec_str += '<div id="Include_add_on_addnew_footer"></div>'
			values_list = ""
			values_lists = ""
			a_test = []
			for invsk in list(Header_details):
				table_ids = "#" + str(table_id)
				filter_class = table_ids + " .bootstrap-table-filter-control-" + str(invsk)
				values_lists += "var " + str(invsk) + ' = $("' + str(filter_class) + '").val(); '
				values_lists += " ATTRIBUTE_VALUEList.push(" + str(invsk) + "); "
				a_test.append(invsk)
				filter_control_function += (
					'$("'
					+ filter_class
					+ '").change( function(){ var table_id = $(this).closest("table").attr("id"); var a_list = '
					+ str(a_test)
					+ "; ATTRIBUTE_VALUEList = []; "
					+ str(values_lists)
					+ ' SortColumn = localStorage.getItem("SortColumn"); SortColumnOrder = localStorage.getItem("SortColumnOrder"); PerPage = $("#PageCountValue").val(); PageInform = "1___" + PerPage + "___" + PerPage; cpq.server.executeScript("SYUADNWPOP", {\'TABLEID\': "'
					+ str(TABLEID)
					+ "\", 'OPER': 'NO', 'RECORDID': \""
					+ str(RECORDID)
					+ "\", 'RECORDFEILD':  \""
					+ str(RECORDFEILD)
					+ "\", 'NEWVALUE': '', 'LOOKUPOBJ': '', 'LOOKUPAPI': '','A_Keys':a_list,'A_Values':ATTRIBUTE_VALUEList}, function(data) {  date_field = data[3]; var assoc = data[1]; var api_name = data[2];data4 = data[4];data5 = data[5]; try { if(date_field.length > 0) { $(\""
					+ str(table_ids)
					+ '").bootstrapTable("load", date_field  ); $("button#country_save").attr("disabled",false); $("#noRecDisp").remove() } else{ var date_field = [];$("'
					+ str(table_ids)
					+ '").bootstrapTable("load", date_field  ); $("button#country_save").attr("disabled",true); $("#Include_add_on_addnew").after("<div id=\'noRecDisp\' class=\'noRecord\'>No Records to Display</div>"); $(".noRecord:not(:first)").remove(); } } catch(err) { if(date_field.length > 0) { $("'
					+ str(table_ids)
					+ '").bootstrapTable("load", date_field  ); $("button#country_save").attr("disabled",false); } else{ $("'
					+ str(table_ids)
					+ '").bootstrapTable("load", date_field  ); $("button#country_save").attr("disabled",true); } } ; });  });'
				)
				

			pagination_condition = "OFFSET {Offset_Skip_Count} ROWS FETCH NEXT {Fetch_Count} ROWS ONLY".format(
				Offset_Skip_Count=offset_skip_count, Fetch_Count=fetch_count
			)

			Pagination_M = Sql.GetFirst("select count(MAADPR.CpqTableEntryId) as count from MAADPR WHERE PRDOFR_ID = '"+str(TreeSuperParentParam)+"' AND PRDOFR_DOCTYP = '"+str(getDocType.DOCTYP_ID)+"' AND COMP_PRDOFR_ID NOT IN (SELECT SERVICE_ID FROM SAQSGB where QUOTE_RECORD_ID ='"+str(contract_quote_record_id)+"' AND QTEREV_RECORD_ID ='"+str(quote_revision_record_id)+"' AND GREENBOOK = '"+str(TreeParentParam)+"' ) ")

			order_by = "order by MAADPR.COMP_PRDOFR_NAME ASC"

			if str(PerPage) == "" and str(PageInform) == "":
				Page_start = 1
				Page_End = fetch_count
				PerPage = fetch_count
				PageInform = "1___"+str(fetch_count)+"___"+str(fetch_count)
			else:
				Page_start = int(PageInform.split("___")[0])
				Page_End = int(PageInform.split("___")[1])
				PerPage = PerPage

			order_by = ""
			if SortColumn != '' and SortColumnOrder !='':
				order_by = "order by "+SortColumn + " " + SortColumnOrder
			else:
				order_by = "order by COMP_PRDOFR_NAME ASC"

			pop_val = {}
				
			if where_string:
				where_string += " AND"
			where_string += """ PRDOFR_ID = '{}' AND PRDOFR_DOCTYP = '{}' AND COMP_PRDOFR_ID NOT IN (SELECT SERVICE_ID FROM SAQSGB where QUOTE_RECORD_ID ='{}' AND QTEREV_RECORD_ID = '{}' AND GREENBOOK = '{}' )""".format(str(TreeSuperParentParam),str(getDocType.DOCTYP_ID),contract_quote_record_id,quote_revision_record_id,TreeParentParam)

			table_data = Sql.GetList(
				"select {} from MAADPR (NOLOCK) {} {} {}".format(
					", ".join(ordered_keys),
					"WHERE " + where_string if where_string else "",
					order_by,
					pagination_condition,
				)
			)
			
			#table_data = Sql.GetList(
			#    "select {} from MAADPR (NOLOCK)  WHERE PRDOFR_ID = '{}'  AND ADNPRDOFR_ID NOT IN (SELECT ADNPRD_ID FROM SAQSAO where QUOTE_RECORD_ID ='{}') {} {}".format(
			#        ", ".join(ordered_keys),str(TreeParentParam),contract_quote_record_id,
			#        order_by,
			#        pagination_condition,
			#    )
			#)
			QueryCountObj = Sql.GetFirst("select count(*) as cnt from MAADPR(NOLOCK) WHERE PRDOFR_ID = '"+str(TreeSuperParentParam)+"' AND PRDOFR_DOCTYP = '"+str(getDocType.DOCTYP_ID)+"' AND COMP_PRDOFR_ID NOT IN (SELECT SERVICE_ID FROM SAQSGB where QUOTE_RECORD_ID ='"+str(contract_quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' AND GREENBOOK = '"+str(TreeParentParam)+"') ")

			if QueryCountObj is not None:
				QryCount = QueryCountObj.cnt


			if table_data is not None :
				for row_data in table_data:
					data_id = str(ObjectName)

					new_value_dict = {}

					for data in row_data:
						if str(data.Key) == "PO_COMP_RECORD_ID":
							pop_val = str(data.Value) + "|addonproducts"
							cpqidval = CPQID.KeyCPQId.GetCPQId(ObjectName, str(data.Value))
							new_value_dict[data.Key] = cpqidval
						else:
							new_value_dict[data.Key] = data.Value
						new_value_dict["pop_val"] = pop_val
					date_field.append(new_value_dict)
			QueryCount = len(date_field)

			pagination_total_count = 0
			if Pagination_M is not None:
				pagination_total_count = Pagination_M.count
			if offset_skip_count == 0:
				records_end = fetch_count
			Trace.Write('offset cnt '+str(offset_skip_count))
			records_end = offset_skip_count + fetch_count - 1
			records_end = pagination_total_count if pagination_total_count < records_end else records_end
			records_start_and_end = "{} - {} of ".format(offset_skip_count, records_end)
			disable_next_and_last = ""
			disable_previous_and_first = ""
			if records_end == pagination_total_count:
				disable_next_and_last = "class='btn-is-disabled'"
			if offset_skip_count == 0:
				disable_previous_and_first = "class='btn-is-disabled'"
			current_page = int(math.ceil(offset_skip_count / fetch_count)) + 1

			Product.SetGlobal("QueryCount", str(QueryCount))
			pagination_table_id = "pagination_{}".format(table_id)
			if QueryCount != 0:
				var_str = """<div id="{Parent_Div_Id}" class="col-md-12 brdr listContStyle padbthgt30">
									<div class="col-md-4 pager-numberofitem  clear-padding">
										<span class="pager-number-of-items-item flt_lt_pad2_mar2022" id="RecordsStartAndEnd">{Records_Start_And_End}</span>
										<span class="pager-number-of-items-item flt_lt_pad2_mar" id="TotalRecordsCount">{Pagination_Total_Count}</span>
										<div class="clear-padding fltltmrgtp3">
											<div class="pull-right vralign">
												<select onchange="ShowResultCountFunc(this, '{ShowResultCountFuncTb}', 'addEquipment', '{TableId}')" id="ShowResultCount" class="form-control selcwdt">
													<option value="10" {Selected_10}>10</option>
													<option value="20" {Selected_20}>20</option>
													<option value="50" {Selected_50}>50</option>
													<option value="100" {Selected_100}>100</option>
													<option value="200" {Selected_200}>200</option>
												</select> 
											</div>
										</div>
									</div>
									<div class="col-xs-8 col-md-4  clear-padding inpadtex" data-bind="visible: totalItemCount">
										<div class="clear-padding col-xs-12 col-sm-6 col-md-12 brd0">
											<ul class="pagination pagination">
												<li class="disabled">
													<a onclick="GetFirstResultFunc('{GetFirstResultFuncTb}', 'addEquipment', '{TableId}')" {Disable_First}><i class="fa fa-caret-left fnt14bold"></i><i class="fa fa-caret-left fnt14"></i></a>
												</li>
												<li class="disabled"><a onclick="GetPreviuosResultFunc('{GetPreviuosResultFuncTb}', 'addEquipment', '{TableId}')" {Disable_Previous}><i class="fa fa-caret-left fnt14"></i>PREVIOUS</a></li>
												<li class="disabled"><a onclick="GetNextResultFunc('{GetNextResultFuncTb}', 'addEquipment', '{TableId}')" {Disable_Next}>NEXT<i class="fa fa-caret-right fnt14"></i></a></li>
												<li class="disabled"><a onclick="GetLastResultFunc('{GetLastResultFuncTb}', 'addEquipment', '{TableId}')" {Disable_Last}><i class="fa fa-caret-right fnt14"></i><i class="fa fa-caret-right fnt14bold"></i></a></li>
											</ul>
										</div> 
									</div> 
									<div class="col-md-4 pad3"> 
										<span id="page_count" class="currentPage page_right_content">{Current_Page}</span>
										<span class="page_right_content padrt2">Page </span>
									</div>
								</div>""".format(
					Parent_Div_Id=pagination_table_id,
					Records_Start_And_End=records_start_and_end,
					Pagination_Total_Count=pagination_total_count,
					ShowResultCountFuncTb=pagination_table_id,
					Selected_10="selected" if fetch_count == 10 else "",
					Selected_20="selected" if fetch_count == 20 else "",
					Selected_50="selected" if fetch_count == 50 else "",
					Selected_100="selected" if fetch_count == 100 else "",
					Selected_200="selected" if fetch_count == 200 else "",
					GetFirstResultFuncTb=pagination_table_id,
					Disable_First=disable_previous_and_first,
					GetPreviuosResultFuncTb=pagination_table_id,
					Disable_Previous=disable_previous_and_first,
					GetNextResultFuncTb=pagination_table_id,
					Disable_Next=disable_next_and_last,
					GetLastResultFuncTb=pagination_table_id,
					Disable_Last=disable_next_and_last,
					Current_Page=current_page,
					TableId=TABLEID,
				)
			else:
				date_field = "NORECORDS"
				Trace.Write("No Equipment Records")
			table_ids = "#" + str(table_id)
			# Filter based on table MultiSelect Dropdown column - Start

			for index, col_name in enumerate(ordered_keys):
				table, api_name = ObjectName, col_name
				obj_data = Sql.GetFirst(
					"SELECT API_NAME, DATA_TYPE, PICKLIST FROM  SYOBJD WHERE OBJECT_NAME='"
					+ str(table)
					+ "' and API_NAME = '"
					+ str(api_name)
					+ "'"
				)
				if obj_data is not None:
					if str(obj_data.PICKLIST).upper() == "TRUE":
						filter_tag = (
							'<div id = "'
							+ str(table_id)
							+ "_RelatedMutipleCheckBoxDrop_"
							+ str(index)
							+ '" class="form-control bootstrap-table-filter-control-'
							+ str(api_name)
							+ " RelatedMutipleCheckBoxDrop_"
							+ str(index)
							+ ' "></div>'
						)
						filter_tags.append(filter_tag)
						filter_types.append("select")
						if obj_data.DATA_TYPE == "CHECKBOX":
							filter_values.append(["True", "False"])
						else:
							# Trace.Write("=============$$$$$$$$$$$$$>>>>>>>>>>>>> "+"SELECT DISTINCT {Column} FROM {Table}".format(Column=api_name, Table=table))
							data_obj = Sql.GetList(
								"SELECT DISTINCT {Column} FROM {Table}".format(Column=api_name, Table=table)
							)
							if data_obj is not None:
								filter_values.append([row_data.Value for data in data_obj for row_data in data])
					else:
						filter_tag = (
							'<input type="text" class="form-control wth100visble bootstrap-table-filter-control-'
							+ str(api_name)
							+ '">'
						)
						filter_tags.append(filter_tag)
						filter_types.append("input")
						filter_values.append("")

			filter_drop_down = (
				"try { if( document.getElementById('"
				+ str(table_id)
				+ "') ) { var listws = document.getElementById('"
				+ str(table_id)
				+ "').getElementsByClassName('filter-control');  for (i = 0; i < listws.length; i++) { document.getElementById('"
				+ str(table_id)
				+ "').getElementsByClassName('filter-control')[i].innerHTML = data6[i];  } for (j = 0; j < listws.length; j++) { if (data10[j] == 'select') { var dataAdapter = new $.jqx.dataAdapter(data8[j]); if(data11[j].length>5){ $('#"
				+ str(table_id)
				+ "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter}); }else{$('#"
				+ str(table_id)
				+ "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter ,autoDropDownHeight: true});} } } } }  catch(err) { setTimeout(function() { var listws = document.getElementById('"
				+ str(table_id)
				+ "').getElementsByClassName('filter-control');  for (i = 0; i < listws.length; i++) { document.getElementById('"
				+ str(table_id)
				+ "').getElementsByClassName('filter-control')[i].innerHTML = data9[i];  } for (j = 0; j < listws.length; j++) { if (data10[j] == 'select') { var dataAdapter = new $.jqx.dataAdapter(data11[j]); $('#"
				+ str(table_id)
				+ "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter, scrollBarSize :10 }); } } }, 5000); }"
			)
			dbl_clk_function += (
				'$("'
				+ str(table_ids)
				+ '").on("all.bs.table", function (e, name, args) { $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); }); $("'
				+ str(table_ids)
				+ '\ th.bs-checkbox div.th-inner").before("<div class=\'pad0brdbt\'>SELECT</div>"); $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>");'
			)

			pagedata = ""
			if QryCount < int(PerPage):
				pagedata = str(Page_start) + " - " + str(QryCount) + " of "
			else:
				pagedata = str(Page_start) + " - " + str(Page_End)+ " of "
			
		elif str(ObjectName) == "SAQRCV" and str(CurrentTab) == "Quotes":
				where_string = ""
				TreeParam = Product.GetGlobal("TreeParam")
				TreeSuperParentParam = Product.GetGlobal("TreeParentLevel1")
				
				
				if A_Keys != "" and A_Values != "":
					A_Keys = list(A_Keys)
					A_Values = list(A_Values)
					for key, value in zip(A_Keys, A_Values):
						if value.strip():
							if where_string:
								where_string += " AND "
							where_string += "{Key} LIKE '%{Value}%'".format(Key=key, Value=value)
				DIVNAME = "VIEW_DIV_ID"
				new_value_dict = {}
				ObjectName = "SACRVC"
				table_id = "add-credits"
				Header_details = {
					"CREDITVOUCHER_RECORD_ID": "KEY",
					"ZAFPLATFORM":"ZAF PLATFORM",
					"ZAFTYPE": "ZAF TYPE",
					"UNAPPLIED_BALANCE": "UNAPPLIED BALANCE",
				}
				ordered_keys = [
					#"ADD_ON_PRODUCT_RECORD_ID",
					"CREDITVOUCHER_RECORD_ID",
					"ZAFPLATFORM",
					"ZAFTYPE",
					"UNAPPLIED_BALANCE",
				]
				Objd_Obj = Sql.GetList(
					"select FIELD_LABEL,API_NAME,LOOKUP_OBJECT,LOOKUP_API_NAME,DATA_TYPE,FORMULA_DATA_TYPE from SYOBJD (NOLOCK)where OBJECT_NAME = '"
					+ str(ObjectName)
					+ "'"
				)
				TreeSuperParentParam =  Product.GetGlobal("TreeParentLevel1") 
				getService = Sql.GetFirst("select SERVICE_DESCRIPTION from SAQTSV(nolock) where SERVICE_ID = '"+str(TreeSuperParentParam)+"'")
				getDocType = Sql.GetFirst("SELECT DOCTYP_ID FROM SAQTRV WHERE QUOTE_RECORD_ID = '"+str(contract_quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' ")
				lookup_disply_list = []
				if Objd_Obj is not None:
					attr_list = {}
					api_names = [inn.API_NAME for inn in Objd_Obj]
					for attr in Objd_Obj:
						attr_list[str(attr.API_NAME)] = str(attr.FIELD_LABEL)
						if str(attr.LOOKUP_API_NAME) != "" and str(attr.LOOKUP_API_NAME) is not None:
							lookup_disply_list.append(str(attr.API_NAME))
					checkbox_list = [
						inn.API_NAME for inn in Objd_Obj if (inn.DATA_TYPE == "CHECKBOX" or inn.FORMULA_DATA_TYPE == "CHECKBOX")
					]
					lookup_list = {ins.LOOKUP_API_NAME: ins.API_NAME for ins in Objd_Obj}
					sec_str = '<div class="row modulebnr brdr ma_mar_btm">ADD-ON PRODUCT LIST<button type="button" id = "Include_add_on" class="close flt_rt" onclick="closepopup_scrl(this)" data-dismiss="modal">X</button></div>'
					sec_str += '<div class="col-md-12 padlftrhtnone" id="btnhide"><div class="row pad-10 bg-lt-wt brdr"><img style="height: 40px; margin-top: -1px; margin-left: -1px; float: left;" src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/Secondary Icon.svg"/><div class="product_txt_div_child secondary_highlight" style="display: block;"></div><div class="product_txt_div_child secondary_highlight" style="display: block;"><div class="product_txt_child"><abbr title="Service ID">Service ID</abbr></div><div class="product_txt_to_top_child" style="float: left;"><abbr title="{}">{}</abbr></div></div><div class="product_txt_div_child secondary_highlight" style="display: block;"><div class="product_txt_child"><abbr title="Service Description">Service Description</abbr></div><div class="product_txt_to_top_child" style="float: left;"><abbr title="{}">{}</abbr></div></div><div class="product_txt_div_child secondary_highlight" style="display: block;"><div class="product_txt_child"><abbr title="Add-On">Add-On</abbr></div><div class="product_txt_to_top_child" style="float: left;"><abbr title="All">All</abbr></div></div><button type="button" class="btnconfig" data-dismiss="modal" id = "Include_add_on" onclick="closepopup_scrl(this)">CANCEL</button><button type="button" id="add-equipment" class="btnconfig" onclick="addon_products()" data-dismiss="modal">ADD</button></div></div>'.format(
					Product.GetGlobal("TreeParentLevel1"),Product.GetGlobal("TreeParentLevel1"),
					getService.SERVICE_DESCRIPTION,getService.SERVICE_DESCRIPTION

				)

				sec_str += '<div id="container" class="g4 pad-10 brdr except_sec">'
				sec_str += (
					'<table id="'
					+ str(table_id)
					+ '" data-escape="true"  data-search-on-enter-key="true" data-show-header="true"  data-filter-control="true"> <thead><tr>'
				)
				sec_str += '<th data-field="SELECT" class="wth45" data-checkbox="true" id ="check_boxval" onchange = "get_checkedval()"><div class="action_col">SELECT</div></th>'

				for key, invs in enumerate(list(ordered_keys)):

					invs = str(invs).strip()
					qstring = Header_details.get(str(invs)) or ""
					if key == 0:
						sec_str += (
							'<th data-field="'
							+ str(invs)
							+ '" data-formatter="add_on_prdListKeyHyperLink" data-sortable="true" data-title-tooltip="'
							+ str(qstring)
							+ '" data-filter-control="input">'
							+ str(qstring)
							+ "</th>"
						)
					else:
						sec_str += (
							'<th data-field="'
							+ invs
							+ '" data-title-tooltip="'
							+ str(qstring)
							+ '" data-sortable="true" data-filter-control="input">'
							+ str(qstring)
							+ "</th>"
						)
				sec_str += '</tr></thead><tbody class ="equipments_id" ></tbody></table>'
				sec_str += '<div id="Include_add_on_addnew_footer"></div>'
				values_list = ""
				values_lists = ""
				a_test = []
				for invsk in list(Header_details):
					table_ids = "#" + str(table_id)
					filter_class = table_ids + " .bootstrap-table-filter-control-" + str(invsk)
					values_lists += "var " + str(invsk) + ' = $("' + str(filter_class) + '").val(); '
					values_lists += " ATTRIBUTE_VALUEList.push(" + str(invsk) + "); "
					a_test.append(invsk)
					filter_control_function += (
						'$("'
						+ filter_class
						+ '").change( function(){ var table_id = $(this).closest("table").attr("id"); var a_list = '
						+ str(a_test)
						+ "; ATTRIBUTE_VALUEList = []; "
						+ str(values_lists)
						+ ' SortColumn = localStorage.getItem("SortColumn"); SortColumnOrder = localStorage.getItem("SortColumnOrder"); PerPage = $("#PageCountValue").val(); PageInform = "1___" + PerPage + "___" + PerPage; cpq.server.executeScript("SYUADNWPOP", {\'TABLEID\': "'
						+ str(TABLEID)
						+ "\", 'OPER': 'NO', 'RECORDID': \""
						+ str(RECORDID)
						+ "\", 'RECORDFEILD':  \""
						+ str(RECORDFEILD)
						+ "\", 'NEWVALUE': '', 'LOOKUPOBJ': '', 'LOOKUPAPI': '','A_Keys':a_list,'A_Values':ATTRIBUTE_VALUEList}, function(data) {  date_field = data[3]; var assoc = data[1]; var api_name = data[2];data4 = data[4];data5 = data[5]; try { if(date_field.length > 0) { $(\""
						+ str(table_ids)
						+ '").bootstrapTable("load", date_field  ); $("button#country_save").attr("disabled",false); $("#noRecDisp").remove() } else{ var date_field = [];$("'
						+ str(table_ids)
						+ '").bootstrapTable("load", date_field  ); $("button#country_save").attr("disabled",true); $("#Include_add_on_addnew").after("<div id=\'noRecDisp\' class=\'noRecord\'>No Records to Display</div>"); $(".noRecord:not(:first)").remove(); } } catch(err) { if(date_field.length > 0) { $("'
						+ str(table_ids)
						+ '").bootstrapTable("load", date_field  ); $("button#country_save").attr("disabled",false); } else{ $("'
						+ str(table_ids)
						+ '").bootstrapTable("load", date_field  ); $("button#country_save").attr("disabled",true); } } ; });  });'
					)
					

				pagination_condition = "OFFSET {Offset_Skip_Count} ROWS FETCH NEXT {Fetch_Count} ROWS ONLY".format(
					Offset_Skip_Count=offset_skip_count, Fetch_Count=fetch_count
				)

				# Pagination_M = Sql.GetFirst("select count(MAADPR.CpqTableEntryId) as count from MAADPR WHERE PRDOFR_ID = '"+str(TreeSuperParentParam)+"' AND PRDOFR_DOCTYP = '"+str(getDocType.DOCTYP_ID)+"' AND COMP_PRDOFR_ID NOT IN (SELECT ADNPRD_ID FROM SAQSAO where QUOTE_RECORD_ID ='"+str(contract_quote_record_id)+"' AND QTEREV_RECORD_ID ='"+str(quote_revision_record_id)+"') ")

				# order_by = "order by SACRVC.COMP_PRDOFR_NAME ASC"

				# if str(PerPage) == "" and str(PageInform) == "":
				# 	Page_start = 1
				# 	Page_End = fetch_count
				# 	PerPage = fetch_count
				# 	PageInform = "1___"+str(fetch_count)+"___"+str(fetch_count)
				# else:
				# 	Page_start = int(PageInform.split("___")[0])
				# 	Page_End = int(PageInform.split("___")[1])
				# 	PerPage = PerPage

				# order_by = ""
				# if SortColumn != '' and SortColumnOrder !='':
				# 	order_by = "order by "+SortColumn + " " + SortColumnOrder
				# else:
				# 	order_by = "order by COMP_PRDOFR_NAME ASC"

				pop_val = {}
					
				# if where_string:
				# 	where_string += " AND"
				# where_string += """ PRDOFR_ID = '{}' AND PRDOFR_DOCTYP = '{}' AND COMP_PRDOFR_ID NOT IN (SELECT ADNPRD_ID FROM SAQSAO where QUOTE_RECORD_ID ='{}' AND QTEREV_RECORD_ID = '{}')""".format(str(TreeSuperParentParam),str(getDocType.DOCTYP_ID),contract_quote_record_id,quote_revision_record_id)

				# table_data = Sql.GetList(
				# 	"select {} from MAADPR (NOLOCK) {} {} {}".format(
				# 		", ".join(ordered_keys),
				# 		"WHERE " + where_string if where_string else "",
				# 		order_by,
				# 		pagination_condition,
				# 	)
				# )
				
				#table_data = Sql.GetList(
				#    "select {} from MAADPR (NOLOCK)  WHERE PRDOFR_ID = '{}'  AND ADNPRDOFR_ID NOT IN (SELECT ADNPRD_ID FROM SAQSAO where QUOTE_RECORD_ID ='{}') {} {}".format(
				#        ", ".join(ordered_keys),str(TreeParentParam),contract_quote_record_id,
				#        order_by,
				#        pagination_condition,
				#    )
				#)
				# QueryCountObj = Sql.GetFirst("select count(*) as cnt from MAADPR(NOLOCK) WHERE PRDOFR_ID = '"+str(TreeSuperParentParam)+"' AND PRDOFR_DOCTYP = '"+str(getDocType.DOCTYP_ID)+"' AND COMP_PRDOFR_ID NOT IN (SELECT ADNPRD_ID FROM SAQSAO where QUOTE_RECORD_ID ='"+str(contract_quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"') ")

				# if QueryCountObj is not None:
				# 	QryCount = QueryCountObj.cnt


				# if table_data is not None :
				# 	for row_data in table_data:
				# 		data_id = str(ObjectName)

				# 		new_value_dict = {}

				# 		for data in row_data:
				# 			if str(data.Key) == "PO_COMP_RECORD_ID":
				# 				pop_val = str(data.Value) + "|addonproducts"
				# 				cpqidval = CPQID.KeyCPQId.GetCPQId(ObjectName, str(data.Value))
				# 				new_value_dict[data.Key] = cpqidval
				# 			else:
				# 				new_value_dict[data.Key] = data.Value
				# 			new_value_dict["pop_val"] = pop_val
				# 		date_field.append(new_value_dict)
				# QueryCount = len(date_field)

				# pagination_total_count = 0
				# if Pagination_M is not None:
				# 	pagination_total_count = Pagination_M.count
				# if offset_skip_count == 0:
				# 	records_end = fetch_count
				# Trace.Write('offset cnt '+str(offset_skip_count))
				# records_end = offset_skip_count + fetch_count - 1
				# records_end = pagination_total_count if pagination_total_count < records_end else records_end
				# records_start_and_end = "{} - {} of ".format(offset_skip_count, records_end)
				# disable_next_and_last = ""
				# disable_previous_and_first = ""
				# if records_end == pagination_total_count:
				# 	disable_next_and_last = "class='btn-is-disabled'"
				# if offset_skip_count == 0:
				# 	disable_previous_and_first = "class='btn-is-disabled'"
				# current_page = int(math.ceil(offset_skip_count / fetch_count)) + 1

				# Product.SetGlobal("QueryCount", str(QueryCount))
				# pagination_table_id = "pagination_{}".format(table_id)
				# if QueryCount != 0:
				# 	var_str = """<div id="{Parent_Div_Id}" class="col-md-12 brdr listContStyle padbthgt30">
				# 						<div class="col-md-4 pager-numberofitem  clear-padding">
				# 							<span class="pager-number-of-items-item flt_lt_pad2_mar2022" id="RecordsStartAndEnd">{Records_Start_And_End}</span>
				# 							<span class="pager-number-of-items-item flt_lt_pad2_mar" id="TotalRecordsCount">{Pagination_Total_Count}</span>
				# 							<div class="clear-padding fltltmrgtp3">
				# 								<div class="pull-right vralign">
				# 									<select onchange="ShowResultCountFunc(this, '{ShowResultCountFuncTb}', 'addEquipment', '{TableId}')" id="ShowResultCount" class="form-control selcwdt">
				# 										<option value="10" {Selected_10}>10</option>
				# 										<option value="20" {Selected_20}>20</option>
				# 										<option value="50" {Selected_50}>50</option>
				# 										<option value="100" {Selected_100}>100</option>
				# 										<option value="200" {Selected_200}>200</option>
				# 									</select> 
				# 								</div>
				# 							</div>
				# 						</div>
				# 						<div class="col-xs-8 col-md-4  clear-padding inpadtex" data-bind="visible: totalItemCount">
				# 							<div class="clear-padding col-xs-12 col-sm-6 col-md-12 brd0">
				# 								<ul class="pagination pagination">
				# 									<li class="disabled">
				# 										<a onclick="GetFirstResultFunc('{GetFirstResultFuncTb}', 'addEquipment', '{TableId}')" {Disable_First}><i class="fa fa-caret-left fnt14bold"></i><i class="fa fa-caret-left fnt14"></i></a>
				# 									</li>
				# 									<li class="disabled"><a onclick="GetPreviuosResultFunc('{GetPreviuosResultFuncTb}', 'addEquipment', '{TableId}')" {Disable_Previous}><i class="fa fa-caret-left fnt14"></i>PREVIOUS</a></li>
				# 									<li class="disabled"><a onclick="GetNextResultFunc('{GetNextResultFuncTb}', 'addEquipment', '{TableId}')" {Disable_Next}>NEXT<i class="fa fa-caret-right fnt14"></i></a></li>
				# 									<li class="disabled"><a onclick="GetLastResultFunc('{GetLastResultFuncTb}', 'addEquipment', '{TableId}')" {Disable_Last}><i class="fa fa-caret-right fnt14"></i><i class="fa fa-caret-right fnt14bold"></i></a></li>
				# 								</ul>
				# 							</div> 
				# 						</div> 
				# 						<div class="col-md-4 pad3"> 
				# 							<span id="page_count" class="currentPage page_right_content">{Current_Page}</span>
				# 							<span class="page_right_content padrt2">Page </span>
				# 						</div>
				# 					</div>""".format(
				# 		Parent_Div_Id=pagination_table_id,
				# 		Records_Start_And_End=records_start_and_end,
				# 		Pagination_Total_Count=pagination_total_count,
				# 		ShowResultCountFuncTb=pagination_table_id,
				# 		Selected_10="selected" if fetch_count == 10 else "",
				# 		Selected_20="selected" if fetch_count == 20 else "",
				# 		Selected_50="selected" if fetch_count == 50 else "",
				# 		Selected_100="selected" if fetch_count == 100 else "",
				# 		Selected_200="selected" if fetch_count == 200 else "",
				# 		GetFirstResultFuncTb=pagination_table_id,
				# 		Disable_First=disable_previous_and_first,
				# 		GetPreviuosResultFuncTb=pagination_table_id,
				# 		Disable_Previous=disable_previous_and_first,
				# 		GetNextResultFuncTb=pagination_table_id,
				# 		Disable_Next=disable_next_and_last,
				# 		GetLastResultFuncTb=pagination_table_id,
				# 		Disable_Last=disable_next_and_last,
				# 		Current_Page=current_page,
				# 		TableId=TABLEID,
				# 	)
				# else:
				# 	date_field = "NORECORDS"
				# 	Trace.Write("No Equipment Records")
				# table_ids = "#" + str(table_id)
				# # Filter based on table MultiSelect Dropdown column - Start

				# for index, col_name in enumerate(ordered_keys):
				# 	table, api_name = ObjectName, col_name
				# 	obj_data = Sql.GetFirst(
				# 		"SELECT API_NAME, DATA_TYPE, PICKLIST FROM  SYOBJD WHERE OBJECT_NAME='"
				# 		+ str(table)
				# 		+ "' and API_NAME = '"
				# 		+ str(api_name)
				# 		+ "'"
				# 	)
				# 	if obj_data is not None:
				# 		if str(obj_data.PICKLIST).upper() == "TRUE":
				# 			filter_tag = (
				# 				'<div id = "'
				# 				+ str(table_id)
				# 				+ "_RelatedMutipleCheckBoxDrop_"
				# 				+ str(index)
				# 				+ '" class="form-control bootstrap-table-filter-control-'
				# 				+ str(api_name)
				# 				+ " RelatedMutipleCheckBoxDrop_"
				# 				+ str(index)
				# 				+ ' "></div>'
				# 			)
				# 			filter_tags.append(filter_tag)
				# 			filter_types.append("select")
				# 			if obj_data.DATA_TYPE == "CHECKBOX":
				# 				filter_values.append(["True", "False"])
				# 			else:
				# 				# Trace.Write("=============$$$$$$$$$$$$$>>>>>>>>>>>>> "+"SELECT DISTINCT {Column} FROM {Table}".format(Column=api_name, Table=table))
				# 				data_obj = Sql.GetList(
				# 					"SELECT DISTINCT {Column} FROM {Table}".format(Column=api_name, Table=table)
				# 				)
				# 				if data_obj is not None:
				# 					filter_values.append([row_data.Value for data in data_obj for row_data in data])
				# 		else:
				# 			filter_tag = (
				# 				'<input type="text" class="form-control wth100visble bootstrap-table-filter-control-'
				# 				+ str(api_name)
				# 				+ '">'
				# 			)
				# 			filter_tags.append(filter_tag)
				# 			filter_types.append("input")
				# 			filter_values.append("")

				# filter_drop_down = (
				# 	"try { if( document.getElementById('"
				# 	+ str(table_id)
				# 	+ "') ) { var listws = document.getElementById('"
				# 	+ str(table_id)
				# 	+ "').getElementsByClassName('filter-control');  for (i = 0; i < listws.length; i++) { document.getElementById('"
				# 	+ str(table_id)
				# 	+ "').getElementsByClassName('filter-control')[i].innerHTML = data6[i];  } for (j = 0; j < listws.length; j++) { if (data10[j] == 'select') { var dataAdapter = new $.jqx.dataAdapter(data8[j]); if(data11[j].length>5){ $('#"
				# 	+ str(table_id)
				# 	+ "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter}); }else{$('#"
				# 	+ str(table_id)
				# 	+ "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter ,autoDropDownHeight: true});} } } } }  catch(err) { setTimeout(function() { var listws = document.getElementById('"
				# 	+ str(table_id)
				# 	+ "').getElementsByClassName('filter-control');  for (i = 0; i < listws.length; i++) { document.getElementById('"
				# 	+ str(table_id)
				# 	+ "').getElementsByClassName('filter-control')[i].innerHTML = data9[i];  } for (j = 0; j < listws.length; j++) { if (data10[j] == 'select') { var dataAdapter = new $.jqx.dataAdapter(data11[j]); $('#"
				# 	+ str(table_id)
				# 	+ "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter, scrollBarSize :10 }); } } }, 5000); }"
				# )
				# dbl_clk_function += (
				# 	'$("'
				# 	+ str(table_ids)
				# 	+ '").on("all.bs.table", function (e, name, args) { $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); }); $("'
				# 	+ str(table_ids)
				# 	+ '\ th.bs-checkbox div.th-inner").before("<div class=\'pad0brdbt\'>SELECT</div>"); $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>");'
				# )

				# pagedata = ""
				# if QryCount < int(PerPage):
				# 	pagedata = str(Page_start) + " - " + str(QryCount) + " of "
				# else:
				# 	pagedata = str(Page_start) + " - " + str(Page_End)+ " of "

		elif str(ObjectName) == "SAQTSV" and str(CurrentTab) == "Quotes":
			Trace.Write('0bi------------')
			where_string = ""
			if A_Keys != "" and A_Values != "":
				A_Keys = list(A_Keys)
				A_Values = list(A_Values)
				for key, value in zip(A_Keys, A_Values):
					if value.strip():
						if where_string:
							where_string += " AND "
						if key=="MATERIAL_RECORD_ID":
							key="MAMTRL.CpqTableEntryId"
						where_string += "{Key} LIKE '%{Value}%'".format(Key=key, Value=value)
			DIVNAME = "VIEW_DIV_ID"
			new_value_dict = {}
			ObjectName = "MAMTRL"
			table_id = "offerings-addnew-model"
			Header_details = {
				"MATERIAL_RECORD_ID": "KEY",
				"SAP_PART_NUMBER": "PRODUCT OFFERING ID",
				"SAP_DESCRIPTION": "PRODUCT OFFERING DESCRIPTION",
			}
			ordered_keys = [
				"MATERIAL_RECORD_ID",
				"SAP_PART_NUMBER",
				"SAP_DESCRIPTION",
			]
			Objd_Obj = Sql.GetList(
				"select FIELD_LABEL,API_NAME,LOOKUP_OBJECT,LOOKUP_API_NAME,DATA_TYPE,FORMULA_DATA_TYPE from SYOBJD (NOLOCK)where OBJECT_NAME = '"
				+ str(ObjectName)
				+ "'"
			)
			lookup_disply_list = []
			if Objd_Obj is not None:
				attr_list = {}
				api_names = [inn.API_NAME for inn in Objd_Obj]
				for attr in Objd_Obj:
					attr_list[str(attr.API_NAME)] = str(attr.FIELD_LABEL)
					if str(attr.LOOKUP_API_NAME) != "" and str(attr.LOOKUP_API_NAME) is not None:
						lookup_disply_list.append(str(attr.API_NAME))
				checkbox_list = [
					inn.API_NAME for inn in Objd_Obj if (inn.DATA_TYPE == "CHECKBOX" or inn.FORMULA_DATA_TYPE == "CHECKBOX")
				]
				lookup_list = {ins.LOOKUP_API_NAME: ins.API_NAME for ins in Objd_Obj}
			sec_str = '<div class="row modulebnr brdr ma_mar_btm">ADD OFFERINGS<button type="button" class="close flt_rt" onclick="closepopup_scrl()" data-dismiss="modal">X</button></div>'
			sec_str += '<div class="col-md-12 padlftrhtnone"><div class="row pad-10 bg-lt-wt brdr"> <img style="height: 40px; margin-top: -1px; margin-left: -1px; float: left;" src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/Secondary Icon.svg"/><div class="product_txt_div_child secondary_highlight" style="display: block;text-align: left;"><div class="product_txt_child"><abbr title="Key">PRODUCT OFFERING</abbr></div><div class="product_txt_to_top_child"><abbr title="ALL">Select a Product Offering to add to your list of Quote Product Offerings</abbr></div></div><button type="button" class="btnconfig" data-dismiss="modal" onclick="closepopup_scrl()">CANCEL</button><button type="button" id="add-offerings" class="btnconfig" onclick="addOfferings()" data-dismiss="modal">ADD</button></div></div>'

			sec_str += '<div id="container" class="g4 pad-10 brdr except_sec">'
			sec_str += (
				'<table id="'
				+ str(table_id)
				+ '" data-escape="true"  data-search-on-enter-key="true" data-show-header="true"  data-filter-control="true"> <thead><tr>'
			)
			#sec_str += '<th data-field="SELECT" class="wth45" data-checkbox="true" id ="check_boxval" onchange = "get_checkedval()"><div class="action_col">SELECT</div></th>'

			for key, invs in enumerate(list(ordered_keys)):

				invs = str(invs).strip()
				qstring = Header_details.get(str(invs)) or ""
				if key == 0:
					sec_str += (
						'<th data-field="'
						+ str(invs)
						+ '" data-formatter="offeringsModelListKeyHyperLink" data-sortable="true" data-title-tooltip="'
						+ str(qstring)
						+ '" data-filter-control="input">'
						+ str(qstring)
						+ "</th>"
					)
				else:
					sec_str += (
						'<th data-field="'
						+ invs
						+ '" data-title-tooltip="'
						+ str(qstring)
						+ '" data-sortable="true" data-filter-control="input">'
						+ str(qstring)
						+ "</th>"
					)
			sec_str += '</tr></thead><tbody class ="user_id" ></tbody></table>'
			sec_str += '<div id="add-offerings-model-footer"></div>'
			values_list = ""
			values_lists = ""
			a_test = []
			for invsk in list(Header_details):
				table_ids = "#" + str(table_id)
				filter_class = table_ids + " .bootstrap-table-filter-control-" + str(invsk)
				values_lists += "var " + str(invsk) + ' = $("' + str(filter_class) + '").val(); '
				values_lists += " ATTRIBUTE_VALUEList.push(" + str(invsk) + "); "
				a_test.append(invsk)
				filter_control_function += (
					'$("'
					+ filter_class
					+ '").change( function(){ var table_id = $(this).closest("table").attr("id"); var a_list = '
					+ str(a_test)
					+ "; ATTRIBUTE_VALUEList = []; "
					+ str(values_lists)
					+ ' SortColumn = localStorage.getItem("SortColumn"); SortColumnOrder = localStorage.getItem("SortColumnOrder"); PerPage = $("#PageCountValue").val(); PageInform = "1___" + PerPage + "___" + PerPage; cpq.server.executeScript("SYUADNWPOP", {\'TABLEID\': "'
					+ str(TABLEID)
					+ "\", 'OPER': 'NO', 'RECORDID': \""
					+ str(RECORDID)
					+ "\", 'RECORDFEILD':  \""
					+ str(RECORDFEILD)
					+ "\", 'NEWVALUE': '', 'LOOKUPOBJ': '', 'LOOKUPAPI': '','A_Keys':a_list,'A_Values':ATTRIBUTE_VALUEList}, function(data) {  date_field = data[3]; var assoc = data[1]; var api_name = data[2];data4 = data[4];data5 = data[5]; data15 = data[15]; data16 = data[16]; try { if(date_field.length > 0) { $(\""
					+ str(table_ids)
					+ '").bootstrapTable("load", date_field  );$("#noRecDisp").remove(); if (document.getElementById("RecordsStartAndEnd")){document.getElementById("RecordsStartAndEnd").innerHTML = data15;}; if (document.getElementById("TotalRecordsCount")) {document.getElementById("TotalRecordsCount").innerHTML = data16;} } else{ $("'
					+ str(table_ids)
					+ '").bootstrapTable("load", date_field  );$("#offerings-addnew-model").after("<div id=\'noRecDisp\' class=\'noRecord\'>No Records to Display</div>"); $(".noRecord:not(:first)").remove(); } } catch(err) { if(date_field.length > 0) { $("'
					+ str(table_ids)
					+ '").bootstrapTable("load", date_field  ); } else{ $("'
					+ str(table_ids)
					+ '").bootstrapTable("load", date_field  ); document.getElementById("add-offerings-model-footer").style.border = "1px solid #ccc"; document.getElementById("add-offerings-model-footer").style.padding = "5.5px"; document.getElementById("add-offerings-model-footer").innerHTML = "No Records to Display"; } } ; });  });'
				)

				dbl_clk_function = (
					'$("'
					+ str(table_ids)
					+ '").on("all.bs.table", function (e, name, args) { console.log("popu_upid ============>"); $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); var count = 0; var selectAll = false; $("#add-offerings").css("display","none"); $("#offerings-addnew-model").find(\'[type="checkbox"]:checked\').map(function () {var sel_val = $(this).closest("tr").find("td:nth-child(2)").text(); count = 1; console.log("popu_upid3333 ============>"+$(this).attr("name")); if ($(this).attr("name") == "btSelectAll"){console.log("popu_up1111 ============>"); var selectAll = true; $("#add-offerings").css("display","block");} else if (sel_val != "") {console.log("popu_up222 ============>"); $("#add-offerings").css("display","block");} else{$("#add-offerings").css("display","none");}});if(count == 0){$("#add-offerings").css("display","none");}}); $(".bs-checkbox input").addClass("custom"); $("'
					+ str(table_ids)
					+ "\").on('sort.bs.table', function (e, name, order) { console.log('sort.bs.table ============>', e); e.stopPropagation(); currenttab = $(\"ul#carttabs_head .active\").text().trim(); localStorage.setItem('"
					+ str(table_id)
					+ "_SortColumn', name); localStorage.setItem('"
					+ str(table_id)
					+ "_SortColumnOrder', order); ATTRIBUTE_VALUEList = []; "+str(values_lists)+" AddNewContainerSorting(name, order, '"
					+ str(table_id)
					+ "',"+str(a_test)+",ATTRIBUTE_VALUEList,'"+str(TABLEID)+"','"+str(RECORDID)+"','"+str(RECORDFEILD)+"'); }); "
					)
				

			pagination_condition = "OFFSET {Offset_Skip_Count} ROWS FETCH NEXT {Fetch_Count} ROWS ONLY".format(
				Offset_Skip_Count=offset_skip_count, Fetch_Count=fetch_count
			)
			TreeParam = Product.GetGlobal("TreeParam")
			Trace.Write("TreeParam"+str(TreeParam))
			inner_join = ""
			additional_where = ""
			if where_string and 'SAP_PART_NUMBER' in where_string:
				where_string = where_string.replace("SAP_PART_NUMBER", "MAMTRL.SAP_PART_NUMBER")
			if TreeParam in ("Comprehensive Services","Product Offerings","Complementary Products"):
				get_sales_org = Sql.GetFirst("SELECT * FROM SAQTRV WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(contract_quote_record_id,quote_revision_record_id) )
				if get_sales_org :
					inner_join = " INNER JOIN MAMSOP (NOLOCK) ON MAMTRL.MATERIAL_RECORD_ID = MAMSOP.MATERIAL_RECORD_ID JOIN MAADPR  ON MAADPR.PRDOFR_ID =  MAMTRL.SAP_PART_NUMBER AND MAADPR.PRDOFR_ID = MAMSOP.SAP_PART_NUMBER"
					additional_where = " AND SALESORG_ID='{}' ".format(get_sales_org.SALESORG_ID)
			if TreeParam == "Product Offerings":
				Pagination_M = Sql.GetFirst(
					"SELECT COUNT(distinct {}.CpqTableEntryId) as count FROM {} (NOLOCK) {} WHERE {} PRODUCT_TYPE IS NOT NULL AND PRODUCT_TYPE <> '' AND  MAADPR.VISIBLE_INCONFIG = 'TRUE' AND PRODUCT_TYPE != 'Add-On Products' AND NOT EXISTS (SELECT SERVICE_ID FROM SAQTSV (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID ='{}' AND MAMTRL.SAP_PART_NUMBER =  SAQTSV.SERVICE_ID) {} ".format(
						ObjectName,ObjectName,inner_join if inner_join else "",str(where_string)+" AND " if where_string else "",contract_quote_record_id,quote_revision_record_id,additional_where
					)
				)
			else:
				Pagination_M = Sql.GetFirst(
					"SELECT COUNT({}.CpqTableEntryId) as count FROM {} (NOLOCK) {} WHERE {} PRODUCT_TYPE ='{}' AND {}.SAP_PART_NUMBER NOT IN (SELECT SERVICE_ID FROM SAQTSV (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID ='{}') {} ".format(
						ObjectName,ObjectName,inner_join if inner_join else "",str(where_string)+" AND " if where_string else "", Product.GetGlobal("TreeParam"),ObjectName, contract_quote_record_id,quote_revision_record_id,additional_where
					)
				)
			
			if str(PerPage) == "" and str(PageInform) == "":
				Page_start = 1
				Page_End = fetch_count
				PerPage = fetch_count
				PageInform = "1___"+str(fetch_count)+"___"+str(fetch_count)
			else:
				Page_start = int(PageInform.split("___")[0])
				Page_End = int(PageInform.split("___")[1])
				PerPage = PerPage

			order_by = ""
			if SortColumn != '' and SortColumnOrder !='':
				order_by = "order by "+SortColumn + " " + SortColumnOrder
			else:
				order_by = "order by MAMTRL.SAP_PART_NUMBER ASC"

			pop_val = {}

			if where_string:
				where_string += " AND"
			ordered_keys = [
				"MAMTRL.MATERIAL_RECORD_ID",
				"MAMTRL.SAP_PART_NUMBER",
				"SAP_DESCRIPTION",
				"PRODUCT_TYPE",
				]
			if TreeParam == "Product Offerings":
				where_string += """ PRODUCT_TYPE IS NOT NULL AND PRODUCT_TYPE <> '' AND PRODUCT_TYPE != 'Add-On Products' AND  MAADPR.VISIBLE_INCONFIG = 'TRUE' AND NOT EXISTS (SELECT SERVICE_ID FROM SAQTSV (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID ='{}' AND MAMTRL.SAP_PART_NUMBER =  SAQTSV.SERVICE_ID  )""".format(
					contract_quote_record_id,quote_revision_record_id
				)
			else:
				where_string += """ PRODUCT_TYPE ='{}' AND MAMTRL.SAP_PART_NUMBER NOT IN (SELECT SERVICE_ID FROM SAQTSV (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID ='{}')""".format(
					Product.GetGlobal("TreeParam"), contract_quote_record_id,quote_revision_record_id
				)
				
			#Trace.Write("order_by"+str(order_by)+str(additional_where))
			table_data = Sql.GetList(
				"select distinct {} from {} (NOLOCK) {} {} {} {} {}".format(
					", ".join(ordered_keys),
					ObjectName
					,inner_join if inner_join else "",
					"WHERE " + where_string if where_string else "" ,
					additional_where,
					order_by,pagination_condition
				)
			)
			
			QueryCountObj = Sql.GetFirst(
					"select count(distinct MAMTRL.SAP_PART_NUMBER) as cnt from {} (NOLOCK) {} {} {} ".format(
					ObjectName,
					inner_join if inner_join else "",
					"WHERE " + where_string if where_string else "",
					additional_where
				)
				)
			if QueryCountObj is not None:
				QryCount = QueryCountObj.cnt



			""" table_data_select = Sql.GetList(
				"select top 1000 SERVICE_ID,SERVICE_DESCRIPTION from SAQTSV (NOLOCK) where QUOTE_SERVICE_RECORD_ID ='"
				+ str(contract_quote_record_ids)
				+ "'"
			)
			for qt_obj in table_data_select:
				cpqidval = CPQID.KeyCPQId.GetCPQId(ObjectName, str(qt_obj.COUNTRY_RECORD_ID))                
				selected_offerings_list_preslect.append(cpqidval) """

			if table_data is not None:
				for row_data in table_data:
					data_id = str(ObjectName)
					new_value_dict = {}
					for data in row_data:
						if str(data.Key) == "MATERIAL_RECORD_ID":
							pop_val = str(data.Value) + "|Offerings"
							cpqidval = CPQID.KeyCPQId.GetCPQId(ObjectName, str(data.Value))
							new_value_dict[data.Key] = cpqidval
						else:
							new_value_dict[data.Key] = data.Value
						new_value_dict["pop_val"] = pop_val
					date_field.append(new_value_dict)
			QueryCount = len(date_field)

			pagination_total_count = 0
			if Pagination_M is not None:
				pagination_total_count = QryCount
			if offset_skip_count == 0:
				offset_skip_count = 1
				records_end = fetch_count
				disable_previous_and_first = "class='btn-is-disabled' style=\'pointer-events:none\' "
			Trace.Write('offset cnt-->'+str(offset_skip_count))
			if offset_skip_count%10==0:
				offset_skip_count+=1
			records_end = offset_skip_count + fetch_count - 1
			records_end = pagination_total_count if pagination_total_count < records_end else records_end
			if pagination_total_count==0:
				offset_skip_count=0
			records_start_and_end = "{} - {} of ".format(offset_skip_count, records_end)
			disable_next_and_last = ""
			disable_previous_and_first = ""
			if records_end == pagination_total_count:
				disable_next_and_last = "class='btn-is-disabled' style=\'pointer-events:none\' "
			current_page = int(math.ceil(offset_skip_count / fetch_count)) + 1

			Product.SetGlobal("QueryCount", str(QueryCount))
			pagination_table_id = "pagination_{}".format(table_id)
			Trace.Write('rec start end-->'+str(records_start_and_end))
			var_str = """<div id="{Parent_Div_Id}" class="col-md-12 brdr listContStyle padbthgt30">
								<div class="col-md-4 pager-numberofitem  clear-padding">
									<span class="pager-number-of-items-item flt_lt_pad2_mar2022" id="RecordsStartAndEnd">{Records_Start_And_End}</span>
									<span class="pager-number-of-items-item flt_lt_pad2_mar" id="TotalRecordsCount">{Pagination_Total_Count}</span>
									<div class="clear-padding fltltmrgtp3">
										<div class="pull-right vralign">
											<select onchange="ShowResultCountFunc(this, '{ShowResultCountFuncTb}', 'addOfferings', '{TableId}')" id="ShowResultCount" class="form-control selcwdt">
												<option value="10" {Selected_10}>10</option>
												<option value="20" {Selected_20}>20</option>
												<option value="50" {Selected_50}>50</option>
												<option value="100" {Selected_100}>100</option>
												<option value="200" {Selected_200}>200</option>
											</select> 
										</div>
									</div>
								</div>
								<div class="col-xs-8 col-md-4  clear-padding inpadtex" data-bind="visible: totalItemCount">
									<div class="clear-padding col-xs-12 col-sm-6 col-md-12 brd0">
										<ul class="pagination pagination">
											<li class="disabled">
												<a onclick="GetFirstResultFunc('{GetFirstResultFuncTb}', 'addOfferings', '{TableId}')" {Disable_First}><i class="fa fa-caret-left fnt14bold"></i><i class="fa fa-caret-left fnt14"></i></a>
											</li>
											<li class="disabled"><a onclick="GetPreviuosResultFunc('{GetPreviuosResultFuncTb}', 'addOfferings', '{TableId}')" {Disable_Previous}><i class="fa fa-caret-left fnt14"></i>PREVIOUS</a></li>
											<li class="disabled"><a onclick="GetNextResultFunc('{GetNextResultFuncTb}', 'addOfferings', '{TableId}')" {Disable_Next}>NEXT<i class="fa fa-caret-right fnt14"></i></a></li>
											<li class="disabled"><a onclick="GetLastResultFunc('{GetLastResultFuncTb}', 'addOfferings', '{TableId}')" {Disable_Last}><i class="fa fa-caret-right fnt14"></i><i class="fa fa-caret-right fnt14bold"></i></a></li>
										</ul>
									</div> 
								</div> 
								<div class="col-md-4 pad3"> 
									<span id="page_count" class="currentPage page_right_content">{Current_Page}</span>
									<span class="page_right_content padrt2">Page </span>
								</div>
							</div>""".format(
				Parent_Div_Id=pagination_table_id,
				Records_Start_And_End=records_start_and_end,
				Pagination_Total_Count=pagination_total_count,
				ShowResultCountFuncTb=pagination_table_id,
				Selected_10="selected" if fetch_count == 10 else "",
				Selected_20="selected" if fetch_count == 20 else "",
				Selected_50="selected" if fetch_count == 50 else "",
				Selected_100="selected" if fetch_count == 100 else "",
				Selected_200="selected" if fetch_count == 200 else "",
				GetFirstResultFuncTb=pagination_table_id,
				Disable_First=disable_previous_and_first,
				GetPreviuosResultFuncTb=pagination_table_id,
				Disable_Previous=disable_previous_and_first,
				GetNextResultFuncTb=pagination_table_id,
				Disable_Next=disable_next_and_last,
				GetLastResultFuncTb=pagination_table_id,
				Disable_Last=disable_next_and_last,
				Current_Page=current_page,
				TableId=TABLEID,
			)

			table_ids = "#" + str(table_id)
			# Filter based on table MultiSelect Dropdown column - Start

			for index, col_name in enumerate(ordered_keys):
				table, api_name = ObjectName, col_name
				obj_data = Sql.GetFirst(
					"SELECT API_NAME, DATA_TYPE, PICKLIST FROM  SYOBJD WHERE OBJECT_NAME='"
					+ str(table)
					+ "' and API_NAME = '"
					+ str(api_name)
					+ "'"
				)
				if obj_data is not None:
					if str(obj_data.PICKLIST).upper() == "TRUE":
						filter_tag = (
							'<div id = "'
							+ str(table_id)
							+ "_RelatedMutipleCheckBoxDrop_"
							+ str(index)
							+ '" class="form-control bootstrap-table-filter-control-'
							+ str(api_name)
							+ " RelatedMutipleCheckBoxDrop_"
							+ str(index)
							+ ' "></div>'
						)
						filter_tags.append(filter_tag)
						filter_types.append("select")
						if obj_data.DATA_TYPE == "CHECKBOX":
							filter_values.append(["True", "False"])
						else:
							data_obj = Sql.GetList(
								"SELECT DISTINCT {Column} FROM {Table} ".format(Column=api_name, Table=table)
							)
							if data_obj is not None:
								filter_values.append([row_data.Value for data in data_obj for row_data in data])
					else:
						filter_tag = (
							'<input type="text" class="form-control wth100visble bootstrap-table-filter-control-'
							+ str(api_name)
							+ '">'
						)
						filter_tags.append(filter_tag)
						filter_types.append("input")
						filter_values.append("")

			filter_drop_down = (
				"try { if( document.getElementById('"
				+ str(table_id)
				+ "') ) { var listws = document.getElementById('"
				+ str(table_id)
				+ "').getElementsByClassName('filter-control');  for (i = 0; i < listws.length; i++) { document.getElementById('"
				+ str(table_id)
				+ "').getElementsByClassName('filter-control')[i].innerHTML = data6[i];  } for (j = 0; j < listws.length; j++) { if (data10[j] == 'select') { var dataAdapter = new $.jqx.dataAdapter(data8[j]); if(data11[j].length>5){ $('#"
				+ str(table_id)
				+ "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter}); }else{$('#"
				+ str(table_id)
				+ "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter ,autoDropDownHeight: true});} } } } }  catch(err) { setTimeout(function() { var listws = document.getElementById('"
				+ str(table_id)
				+ "').getElementsByClassName('filter-control');  for (i = 0; i < listws.length; i++) { document.getElementById('"
				+ str(table_id)
				+ "').getElementsByClassName('filter-control')[i].innerHTML = data9[i];  } for (j = 0; j < listws.length; j++) { if (data10[j] == 'select') { var dataAdapter = new $.jqx.dataAdapter(data11[j]); $('#"
				+ str(table_id)
				+ "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter, scrollBarSize :10 }); } } }, 5000); }"
			)
			dbl_clk_function += (
				'$("'
				+ str(table_ids)
				+ '").on("all.bs.table", function (e, name, args) { $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); }); $("'
				+ str(table_ids)
				+ '\ th.bs-checkbox div.th-inner").before("<div class=\'pad0brdbt\'>SELECT</div>"); $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>");'
			) 

			pagedata = ""
			if QryCount==0:
				pagedata = str(QryCount) + " - " + str(QryCount) + " of "
			elif QryCount < int(PerPage):
				pagedata = str(Page_start) + " - " + str(QryCount) + " of "
			else:
				pagedata = str(Page_start) + " - " + str(Page_End)+ " of "
			

		# Offerings - End
		##COVERED OBJECTS STARTS
		elif str(ObjectName) == "SAQSCO" and str(CurrentTab) == "Quotes":
			where_string = ""
			if A_Keys != "" and A_Values != "":
				A_Keys = list(A_Keys)
				A_Values = list(A_Values)
				for key, value in zip(A_Keys, A_Values):
					if value.strip():
						if where_string:
							where_string += " AND "
						if key=="QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID":
							key="CpqTableEntryId"
						where_string += "{Key} LIKE '%{Value}%'".format(Key=key, Value=value)
			DIVNAME = "VIEW_DIV_ID"
			new_value_dict = {}
			ObjectName = "SAQFEQ"
			table_id = "Coveredobjectsaddnew"
			TreeParam = Product.GetGlobal("TreeParam")
			TreeSuperParentParam = Product.GetGlobal("TreeParentLevel1")
			TreeParentParam = Product.GetGlobal("TreeParentLevel0")
			Header_details = {
				"QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID": "KEY",
				"EQUIPMENT_ID": "EQUIPMENT ID",
				"EQUIPMENT_DESCRIPTION":"EQUIPMENT_DESCRIPTION",
				"EQUIPMENTCATEGORY_DESCRIPTION":"EQUIPMENT CATEGORY DESCRIPTION",
				"SERIAL_NUMBER": "SERIAL NUMBER",
				"GREENBOOK": "GREENBOOK",
				"PLATFORM": "PLATFORM",
				"FABLOCATION_ID": "FAB LOCATION ID",
				"FABLOCATION_NAME": "FAB LOCATION NAME",
			}
			ordered_keys = [
				"QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID",
				"EQUIPMENT_ID",
				"EQUIPMENT_DESCRIPTION",
				"EQUIPMENTCATEGORY_DESCRIPTION",
				"SERIAL_NUMBER",
				"GREENBOOK",
				"PLATFORM",
				"FABLOCATION_ID",
				"FABLOCATION_NAME",
			]
			Objd_Obj = Sql.GetList(
				"select FIELD_LABEL,API_NAME,LOOKUP_OBJECT,LOOKUP_API_NAME,DATA_TYPE,FORMULA_DATA_TYPE from SYOBJD (NOLOCK)where OBJECT_NAME = '"
				+ str(ObjectName)
				+ "'"
			)
			lookup_disply_list = []
			if Objd_Obj is not None:
				attr_list = {}
				api_names = [inn.API_NAME for inn in Objd_Obj]
				for attr in Objd_Obj:
					attr_list[str(attr.API_NAME)] = str(attr.FIELD_LABEL)
					if str(attr.LOOKUP_API_NAME) != "" and str(attr.LOOKUP_API_NAME) is not None:
						lookup_disply_list.append(str(attr.API_NAME))
				checkbox_list = [
					inn.API_NAME for inn in Objd_Obj if (inn.DATA_TYPE == "CHECKBOX" or inn.FORMULA_DATA_TYPE == "CHECKBOX")
				]
				lookup_list = {ins.LOOKUP_API_NAME: ins.API_NAME for ins in Objd_Obj}
			sec_str = '<div class="row modulebnr brdr ma_mar_btm">INSTALLED BASE EQUIPMENT LIST<button type="button" class="close flt_rt" onclick="closepopup_scrl()" data-dismiss="modal">X</button></div>'
			#add on product equipemnt popup Higlight panel starts
			if str(TABLEID) == 'ADDNEW__SYOBJR_98800_0D035FD5_F0EA_4F11_A0DB_B4E10928B59F' and str(TreeParentParam).upper() =='ADD-ON PRODUCTS':
				getService = Sql.GetFirst("select SERVICE_DESCRIPTION from SAQSAO(nolock) where SERVICE_ID = '"+str(TreeSuperParentParam)+"' and ADNPRD_ID = '"+str(TreeParam)+"'")
				#Trace.Write("TABLEID"+str(TABLEID)+str(TreeParam)+str(TreeParentParam))
				sec_str += '<div class="col-md-12 padlftrhtnone" id="btnhide"><div class="row pad-10 bg-lt-wt brdr"><img style="height: 40px; margin-top: -1px; margin-left: -1px; float: left;" src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/Secondary Icon.svg"/><div class="product_txt_div_child secondary_highlight" style="display: block;text-align: left;"><div class="product_txt_child"><abbr title="Key">Parent Product Offering ID</abbr></div><div class="product_txt_to_top_child"><abbr title="{productid}">{productid}</abbr></div></div><div class="product_txt_div_child secondary_highlight" style="display: block;text-align: left;"><div class="product_txt_child"><abbr title="Key">Parent Product Description</abbr></div><div class="product_txt_to_top_child"><abbr title="{description}">{description}</abbr></div></div><div class="product_txt_div_child secondary_highlight" style="display: block;text-align: left;"><div class="product_txt_child"><abbr title="Key">Equipment</abbr></div><div class="product_txt_to_top_child"><abbr title="ALL">ALL</abbr></div></div><button type="button" class="btnconfig" data-dismiss="modal" onclick="closepopup_scrl()">CANCEL</button><button type="button" id="add-offerings" class="btnconfig" onclick="addcoveredobjs()" data-dismiss="modal">ADD</button></div></div>'.format(productid = TreeSuperParentParam,description = getService.SERVICE_DESCRIPTION if getService else "" )
			##add on product equipemnt popup Higlight panel ends
			else:
				sec_str += '<div class="col-md-12 padlftrhtnone" id="btnhide"><div class="row pad-10 bg-lt-wt brdr"><img style="height: 40px; margin-top: -1px; margin-left: -1px; float: left;" src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/Secondary Icon.svg"/><div class="product_txt_div_child secondary_highlight" style="display: block;text-align: left;"><div class="product_txt_child"><abbr title="Key">Equipment ID</abbr></div><div class="product_txt_to_top_child"><abbr title="ALL">ALL</abbr></div></div><div class="product_txt_div_child secondary_highlight" style="display: block;text-align: left;"><div class="product_txt_child"><abbr title="Key">Fab Location ID</abbr></div><div class="product_txt_to_top_child"><abbr title="ALL">ALL</abbr></div></div><div class="product_txt_div_child secondary_highlight" style="display: none;text-align: left;"><div class="product_txt_child"><abbr title="Key">Sales Org</abbr></div><div class="product_txt_to_top_child"><abbr title="2044">2044</abbr></div></div><button type="button" class="btnconfig" data-dismiss="modal" onclick="closepopup_scrl()">CANCEL</button><button type="button" id="add-offerings" class="btnconfig" onclick="addcoveredobjs()" data-dismiss="modal">ADD</button></div></div>'    
			sec_str += '<div id="container" class="g4 pad-10 brdr except_sec">'
			sec_str += (
				'<table id="'
				+ str(table_id)
				+ '" data-escape="true"  data-search-on-enter-key="true" data-show-header="true"  data-filter-control="true"> <thead><tr>'
			)
			sec_str += '<th data-field="SELECT" class="wth45" data-checkbox="true" id ="check_boxval" onchange = "get_checkedval()"><div class="action_col">SELECT</div></th>'

			for key, invs in enumerate(list(ordered_keys)):
				
				invs = str(invs).strip()
				qstring = Header_details.get(str(invs)) or ""
				if key == 0:
					sec_str += (
						'<th data-field="'
						+ str(invs)
						+ '" data-formatter="CovObjKeyHyperLink" data-sortable="true" data-title-tooltip="'
						+ str(qstring)
						+ '" data-filter-control="input">'
						+ str(qstring)
						+ "</th>"
					)
				else:
					sec_str += (
						'<th data-field="'
						+ invs
						+ '" data-title-tooltip="'
						+ str(qstring)
						+ '" data-sortable="true" data-filter-control="input">'
						+ str(qstring)
						+ "</th>"
					)
			sec_str += '</tr></thead><tbody class ="equipments_id" ></tbody></table>'
			sec_str += '<div id="Coveredobjectsaddnew_footer"></div>'
			values_list = ""
			values_lists = ""
			a_test = []
			for invsk in list(Header_details):
				table_ids = "#" + str(table_id)
				filter_class = table_ids + " .bootstrap-table-filter-control-" + str(invsk)
				values_lists += "var " + str(invsk) + ' = $("' + str(filter_class) + '").val(); '
				values_lists += " ATTRIBUTE_VALUEList.push(" + str(invsk) + "); "
				a_test.append(invsk)
				filter_control_function += (
					'$("'
					+ filter_class
					+ '").change( function(){ var table_id = $(this).closest("table").attr("id"); var a_list = '
					+ str(a_test)
					+ "; ATTRIBUTE_VALUEList = []; "
					+ str(values_lists)
					+ ' SortColumn = localStorage.getItem("SortColumn"); SortColumnOrder = localStorage.getItem("SortColumnOrder"); PerPage = $("#PageCountValue").val(); PageInform = "1___" + PerPage + "___" + PerPage; cpq.server.executeScript("SYUADNWPOP", {\'TABLEID\': "'
					+ str(TABLEID)
					+ "\", 'OPER': 'NO', 'RECORDID': \""
					+ str(RECORDID)
					+ "\", 'RECORDFEILD':  \""
					+ str(RECORDFEILD)
					+ "\", 'NEWVALUE': '', 'LOOKUPOBJ': '', 'LOOKUPAPI': '','A_Keys':a_list,'A_Values':ATTRIBUTE_VALUEList}, function(data) {  date_field = data[3]; var assoc = data[1]; var api_name = data[2];data4 = data[4];data5 = data[5]; data15 = data[15]; data16 = data[16];  try { if(date_field.length > 0) { $(\""
					+ str(table_ids)
					+ '").bootstrapTable("load", date_field  ); $("button#country_save").attr("disabled",false); $("#noRecDisp").remove(); if (document.getElementById("RecordsStartAndEnd")){document.getElementById("RecordsStartAndEnd").innerHTML = data15;}; if (document.getElementById("TotalRecordsCount")) {document.getElementById("TotalRecordsCount").innerHTML = data16;} } else{ $("'
					+ str(table_ids)
					+ '").bootstrapTable("load", date_field  ); $("button#country_save").attr("disabled",true); $("#Coveredobjectsaddnew").after("<div id=\'noRecDisp\' class=\'noRecord\'>No Records to Display</div>"); $(".noRecord:not(:first)").remove(); } } catch(err) { if(date_field.length > 0) { $("'
					+ str(table_ids)
					+ '").bootstrapTable("load", date_field  ); $("button#country_save").attr("disabled",false); } else{ $("'
					+ str(table_ids)
					+ '").bootstrapTable("load", date_field  ); $("button#country_save").attr("disabled",true); } } ; });  });'
				)
				

				dbl_clk_function = (
					'$("'
					+ str(table_ids)
					+ '").on("all.bs.table", function (e, name, args) { $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); });  $(".bs-checkbox input").addClass("custom"); $("'
					+ str(table_ids)
					+ "\").on('sort.bs.table', function (e, name, order) { console.log('sort.bs.table ============>', e); e.stopPropagation(); currenttab = $(\"ul#carttabs_head .active\").text().trim(); localStorage.setItem('"
					+ str(table_id)
					+ "_SortColumn', name); localStorage.setItem('"
					+ str(table_id)
					+ "_SortColumnOrder', order); ATTRIBUTE_VALUEList = []; "+str(values_lists)+" AddNewContainerSorting(name, order, '"
					+ str(table_id)
					+ "',"+str(a_test)+",ATTRIBUTE_VALUEList,'"+str(TABLEID)+"','"+str(RECORDID)+"','"+str(RECORDFEILD)+"'); }); "
					)

			Trace.Write("9999 filter_control_function ---->"+str(filter_control_function))



			pagination_condition = "OFFSET {Offset_Skip_Count} ROWS FETCH NEXT {Fetch_Count} ROWS ONLY".format(
				Offset_Skip_Count=offset_skip_count-1 if offset_skip_count%10==1 else offset_skip_count, Fetch_Count=fetch_count
			)
			#TreeParam = Product.GetGlobal("TreeParam")
			TreeParentParam = Product.GetGlobal("TreeParentLevel0")
			TreeSuperParentParam = Product.GetGlobal("TreeParentLevel1")
			if TreeParentParam == "Add-On Products" and TreeParam !="":
				#getparentservice =Sql.GetFirst("Select SERVICE_ID from SAQSAO(NOLOCK) WHERE QUOTE_RECORD_ID ='{quo_rec_id}' and ADNPRD_ID = '{TreeParam}' AND ACTIVE ='TRUE' ".format(quo_rec_id=Quote.GetGlobal("contract_quote_record_id"),TreeParam = TreeParam))
				Pagination_M = Sql.GetFirst(
					"SELECT COUNT(SAQFEQ.CpqTableEntryId) as count FROM SAQFEQ (NOLOCK) JOIN SAQSCO ON SAQSCO.QUOTE_ID = SAQFEQ.QUOTE_ID  AND SAQSCO.EQUIPMENT_ID = SAQFEQ.EQUIPMENT_ID WHERE SAQFEQ.QUOTE_RECORD_ID = '{quo_rec_id}' AND QTEREV_RECORD_ID = '{qurev_rec_id}' AND SAQSCO.SERVICE_ID ='{parent}' AND SAQFEQ.EQUIPMENT_ID NOT IN(SELECT EQUIPMENT_ID FROM SAQSCO WHERE QUOTE_RECORD_ID = '{quo_rec_id}' and SERVICE_ID = '{TreeParam}' AND QTEREV_RECORD_ID = '{qurev_rec_id}')".format(
						quo_rec_id=Quote.GetGlobal("contract_quote_record_id"),TreeParam = TreeParam,parent = TreeSuperParentParam,qurev_rec_id = quote_revision_record_id
					)
				)
			else: 
				if TreeParam == 'Sending Equipment' or TreeParam == "Receiving Equipment":
					
					Pagination_M = Sql.GetFirst(
					"SELECT COUNT(CpqTableEntryId) as count FROM SAQFEQ (NOLOCK) WHERE {where_string} QUOTE_RECORD_ID = '{quo_rec_id}' AND QTEREV_RECORD_ID = '{qurev_rec_id}' AND RELOCATION_EQUIPMENT_TYPE = 'SENDING EQUIPMENT' AND EQUIPMENT_ID NOT IN(SELECT EQUIPMENT_ID FROM SAQSCO WHERE QUOTE_RECORD_ID = '{quo_rec_id}' and SERVICE_ID = '{TreeParentParam}'AND QTEREV_RECORD_ID = '{qurev_rec_id}' AND RELOCATION_EQUIPMENT_TYPE = 'RECEIVING EQUIPMENT')".format(where_string=str(where_string)+" AND " if where_string else "",
						quo_rec_id=Quote.GetGlobal("contract_quote_record_id"),TreeParentParam = TreeParentParam,qurev_rec_id = quote_revision_record_id
					)
					)
					""" elif TreeParam == 'Receiving Equipment':
						Pagination_M = Sql.GetFirst(
						"SELECT COUNT(CpqTableEntryId) as count FROM SAQFEQ (NOLOCK) WHERE {where_string} QUOTE_RECORD_ID = '{quo_rec_id}' AND RELOCATION_EQUIPMENT_TYPE = 'RECEIVING EQUIPMENT' AND EQUIPMENT_ID NOT IN(SELECT EQUIPMENT_ID FROM SAQSCO WHERE QUOTE_RECORD_ID = '{quo_rec_id}' and SERVICE_ID = '{TreeParam}' AND RELOCATION_EQUIPMENT_TYPE = 'Receiving Equipment')".format(where_string=str(where_string)+" AND " if where_string else "",
							quo_rec_id=Quote.GetGlobal("contract_quote_record_id"),TreeParam = TreeParam
						)
						) """
					
				else:
					Pagination_M = Sql.GetFirst(
					"SELECT COUNT(CpqTableEntryId) as count FROM SAQFEQ (NOLOCK) WHERE {where_string} QUOTE_RECORD_ID = '{quo_rec_id}' AND QTEREV_RECORD_ID = '{qurev_rec_id}' AND {restrict_tools} EQUIPMENT_ID NOT IN(SELECT EQUIPMENT_ID FROM SAQSCO WHERE QUOTE_RECORD_ID = '{quo_rec_id}' and SERVICE_ID = '{TreeParam}' AND QTEREV_RECORD_ID = '{qurev_rec_id}')".format(where_string=str(where_string)+" AND " if where_string else "",
						quo_rec_id=Quote.GetGlobal("contract_quote_record_id"),TreeParam = TreeParam,qurev_rec_id = quote_revision_record_id , restrict_tools = " EQUIPMENTCATEGORY_ID = 'Y' AND " if TreeParam == "Z0004" else "")
					)

			if str(PerPage) == "" and str(PageInform) == "":
				Page_start = 1
				Page_End = fetch_count
				PerPage = fetch_count
				PageInform = "1___"+str(fetch_count)+"___"+str(fetch_count)
			else:
				Page_start = int(PageInform.split("___")[0])
				Page_End = int(PageInform.split("___")[1])
				PerPage = PerPage

			if SortColumn != '' and SortColumnOrder !='':
				order_by = "order by "+SortColumn + " " + SortColumnOrder
			else:
				order_by = "order by EQUIPMENT_ID ASC"

			#order_by = "order by EQUIPMENT_ID ASC"
			# Trace.Write("SELECT COUNT(CpqTableEntryId) as count FROM {} (NOLOCK) WHERE QUOTE_RECORD_ID = '{quo}' AND EQUIPMENT_ID NOT IN(SELECT EQUIPMENT_ID FROM SAQSCO WHERE QUOTE_RECORD_ID = '{quo_rec_id}') ".format(quo=Quote.GetGlobal("contract_quote_record_id"),quo_rec_id=Quote.GetGlobal("contract_quote_record_id"))
			pop_val = {}
				
			if where_string:
				where_string += " AND"
			
			if TreeParam == 'Sending Equipment':
				where_string += " QUOTE_RECORD_ID = '{quo_rec_id}' AND QTEREV_RECORD_ID = '{qurev_rec_id}' AND RELOCATION_EQUIPMENT_TYPE = 'SENDING EQUIPMENT' AND EQUIPMENT_ID NOT IN(SELECT EQUIPMENT_ID FROM SAQSCO WHERE QUOTE_RECORD_ID = '{quo_rec_id}' and SERVICE_ID = '{TreeParam}' AND QTEREV_RECORD_ID = '{qurev_rec_id}' AND RELOCATION_EQUIPMENT_TYPE = 'RECEIVING EQUIPMENT')".format(
				quo_rec_id=Quote.GetGlobal("contract_quote_record_id"),TreeParam = TreeParentParam,qurev_rec_id = quote_revision_record_id
			)
			elif TreeParam == 'Receiving Equipment':
				where_string += " QUOTE_RECORD_ID = '{quo_rec_id}' AND QTEREV_RECORD_ID = '{qurev_rec_id}' AND RELOCATION_EQUIPMENT_TYPE = 'SENDING EQUIPMENT' AND EQUIPMENT_ID NOT IN(SELECT EQUIPMENT_ID FROM SAQSCO WHERE QUOTE_RECORD_ID = '{quo_rec_id}' and SERVICE_ID = '{TreeParam}' AND QTEREV_RECORD_ID = '{qurev_rec_id}' AND RELOCATION_EQUIPMENT_TYPE = 'RECEIVING EQUIPMENT')".format(
				quo_rec_id=Quote.GetGlobal("contract_quote_record_id"),TreeParam = TreeParentParam,qurev_rec_id = quote_revision_record_id
			)
			else:
				Trace.Write('2572--POPUPPPPPPPPPPP----')
				where_string += " QUOTE_RECORD_ID = '{quo_rec_id}' AND QTEREV_RECORD_ID = '{qurev_rec_id}' AND {restrict_tools} EQUIPMENT_ID NOT IN(SELECT EQUIPMENT_ID FROM SAQSCO WHERE QUOTE_RECORD_ID = '{quo_rec_id}' and SERVICE_ID = '{TreeParam}' AND QTEREV_RECORD_ID  = '{qurev_rec_id}')".format(
					quo_rec_id=Quote.GetGlobal("contract_quote_record_id"),TreeParam = TreeParam,qurev_rec_id = quote_revision_record_id, restrict_tools = " EQUIPMENTCATEGORY_ID = 'Y' AND " if TreeParam == "Z0004" else ""
				)
			if TreeParentParam == "Add-On Products" and TreeParam !="":
				#A055S000P01-3251--start pagination issue on addfromlist popup in addonproducts
				if offset_skip_count != 0:
					offset_val=offset_skip_count-1
				else:
					offset_val=offset_skip_count
				
				table_data =Sql.GetList("select SAQFEQ.QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID, SAQFEQ.EQUIPMENT_ID, SAQFEQ.EQUIPMENT_DESCRIPTION,SAQFEQ.SERIAL_NUMBER, SAQFEQ.PBG, SAQFEQ.PLATFORM, SAQFEQ.FABLOCATION_ID, SAQFEQ.FABLOCATION_NAME from  SAQFEQ(NOLOCK) JOIN SAQSCO ON SAQSCO.QUOTE_RECORD_ID = SAQFEQ.QUOTE_RECORD_ID AND SAQSCO.QTEREV_RECORD_ID = SAQFEQ.QTEREV_RECORD_ID AND SAQSCO.EQUIPMENT_ID = SAQFEQ.EQUIPMENT_ID  WHERE SAQFEQ.QUOTE_RECORD_ID = '{quo_rec_id}' AND SAQSCO.SERVICE_ID ='{parent}' AND SAQSCO.QTEREV_RECORD_ID ='{qurev_rec_id}' AND SAQFEQ.EQUIPMENT_ID NOT IN(SELECT EQUIPMENT_ID FROM SAQSCO WHERE QUOTE_RECORD_ID = '{quo_rec_id}' and SERVICE_ID ='{TreeParam}' AND QTEREV_RECORD_ID ='{qurev_rec_id}' ) order by EQUIPMENT_ID ASC offset {offset_skip_count} rows fetch next {per_page} rows only".format(per_page=PerPage,offset_skip_count=offset_val,quo_rec_id=Quote.GetGlobal("contract_quote_record_id"),TreeParam = TreeParam,parent = TreeSuperParentParam,qurev_rec_id = quote_revision_record_id))#A055S000P01-3251--end
			else:    
				table_data = Sql.GetList(
					"select {} from {} (NOLOCK) {} {} {} ".format(
						", ".join(ordered_keys),
						ObjectName,
						"WHERE " + where_string if where_string else "",
						order_by,pagination_condition
					)
				)

			QueryCountObj = Sql.GetFirst(
					"select count(*) as cnt from {} (NOLOCK) {} ".format(
					ObjectName,
					"WHERE " + where_string if where_string else "",
				)
				)
			if QueryCountObj is not None:
				QryCount = QueryCountObj.cnt


			if table_data is not None:
				for row_data in table_data:
					data_id = str(ObjectName)

					new_value_dict = {}

					for data in row_data:
						if str(data.Key) == "QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID":
							pop_val = str(data.Value) + "|Covered Objects"
							cpqidval = CPQID.KeyCPQId.GetCPQId(ObjectName, str(data.Value))
							new_value_dict[data.Key] = cpqidval
						else:
							new_value_dict[data.Key] = data.Value
						new_value_dict["pop_val"] = pop_val
					date_field.append(new_value_dict)
			QueryCount = len(date_field)

			pagination_total_count = 0
			if Pagination_M is not None:
				pagination_total_count = Pagination_M.count
			if offset_skip_count == 0:
				offset_skip_count = 1
				records_end = fetch_count
			records_end = offset_skip_count + fetch_count - 1
			records_end = pagination_total_count if pagination_total_count < records_end else records_end
			records_start_and_end = "{} - {} of ".format(offset_skip_count, records_end)
			disable_next_and_last = ""
			disable_previous_and_first = ""
			if records_end == pagination_total_count:
				disable_next_and_last = "class='btn-is-disabled' style=\'pointer-events:none\'"
			if offset_skip_count == 0:
				disable_previous_and_first = "class='btn-is-disabled' style=\'pointer-events:none\'"
			current_page = int(math.ceil(offset_skip_count / fetch_count)) + 1

			Product.SetGlobal("QueryCount", str(QueryCount))
			pagination_table_id = "pagination_{}".format(table_id)
			#if QueryCount != 0:
			var_str = """<div id="{Parent_Div_Id}" class="col-md-12 brdr listContStyle padbthgt30">
								<div class="col-md-4 pager-numberofitem  clear-padding">
									<span class="pager-number-of-items-item flt_lt_pad2_mar2022" id="RecordsStartAndEnd">{Records_Start_And_End}</span>
									<span class="pager-number-of-items-item flt_lt_pad2_mar" id="TotalRecordsCount">{Pagination_Total_Count}</span>
									<div class="clear-padding fltltmrgtp3">
										<div class="pull-right vralign">
											<select onchange="ShowResultCountFunc(this, '{ShowResultCountFuncTb}', 'addCoveredObj', '{TableId}')" id="ShowResultCount" class="form-control selcwdt">
												<option value="10" {Selected_10}>10</option>
												<option value="20" {Selected_20}>20</option>
												<option value="50" {Selected_50}>50</option>
												<option value="100" {Selected_100}>100</option>
												<option value="200" {Selected_200}>200</option>
											</select> 
										</div>
									</div>
								</div>
								<div class="col-xs-8 col-md-4  clear-padding inpadtex" data-bind="visible: totalItemCount">
									<div class="clear-padding col-xs-12 col-sm-6 col-md-12 brd0">
										<ul class="pagination pagination">
											<li class="disabled">
												<a onclick="GetFirstResultFunc('{GetFirstResultFuncTb}', 'addCoveredObj', '{TableId}')" {Disable_First}><i class="fa fa-caret-left fnt14bold"></i><i class="fa fa-caret-left fnt14"></i></a>
											</li>
											<li class="disabled"><a onclick="GetPreviuosResultFunc('{GetPreviuosResultFuncTb}', 'addCoveredObj', '{TableId}')" {Disable_Previous}><i class="fa fa-caret-left fnt14"></i>PREVIOUS</a></li>
											<li class="disabled"><a onclick="GetNextResultFunc('{GetNextResultFuncTb}', 'addCoveredObj', '{TableId}')" {Disable_Next}>NEXT<i class="fa fa-caret-right fnt14"></i></a></li>
											<li class="disabled"><a onclick="GetLastResultFunc('{GetLastResultFuncTb}', 'addCoveredObj', '{TableId}')" {Disable_Last}><i class="fa fa-caret-right fnt14"></i><i class="fa fa-caret-right fnt14bold"></i></a></li>
										</ul>
									</div> 
								</div> 
								<div class="col-md-4 pad3"> 
									<span id="page_count" class="currentPage page_right_content">{Current_Page}</span>
									<span class="page_right_content padrt2">Page </span>
								</div>
							</div>""".format(
				Parent_Div_Id=pagination_table_id,
				Records_Start_And_End=records_start_and_end,
				Pagination_Total_Count=pagination_total_count,
				ShowResultCountFuncTb=pagination_table_id,
				Selected_10="selected" if fetch_count == 10 else "",
				Selected_20="selected" if fetch_count == 20 else "",
				Selected_50="selected" if fetch_count == 50 else "",
				Selected_100="selected" if fetch_count == 100 else "",
				Selected_200="selected" if fetch_count == 200 else "",
				GetFirstResultFuncTb=pagination_table_id,
				Disable_First=disable_previous_and_first,
				GetPreviuosResultFuncTb=pagination_table_id,
				Disable_Previous=disable_previous_and_first,
				GetNextResultFuncTb=pagination_table_id,
				Disable_Next=disable_next_and_last,
				GetLastResultFuncTb=pagination_table_id,
				Disable_Last=disable_next_and_last,
				Current_Page=current_page,
				TableId=TABLEID,
			)
			# else:
			#     date_field = "NORECORDS"
			#     Trace.Write("No Covered object Records")   
			table_ids = "#" + str(table_id)
			# Filter based on table MultiSelect Dropdown column - Start

			for index, col_name in enumerate(ordered_keys):
				table, api_name = ObjectName, col_name
				obj_data = Sql.GetFirst(
					"SELECT API_NAME, DATA_TYPE, PICKLIST FROM  SYOBJD WHERE OBJECT_NAME='"
					+ str(table)
					+ "' and API_NAME = '"
					+ str(api_name)
					+ "'"
				)
				if obj_data is not None:
					if str(obj_data.PICKLIST).upper() == "TRUE":
						filter_tag = (
							'<div id = "'
							+ str(table_id)
							+ "_RelatedMutipleCheckBoxDrop_"
							+ str(index)
							+ '" class="form-control bootstrap-table-filter-control-'
							+ str(api_name)
							+ " RelatedMutipleCheckBoxDrop_"
							+ str(index)
							+ ' "></div>'
						)
						filter_tags.append(filter_tag)
						filter_types.append("select")
						if obj_data.DATA_TYPE == "CHECKBOX":
							filter_values.append(["True", "False"])
						else:
							data_obj = Sql.GetList(
								"SELECT DISTINCT {Column} FROM {Table}".format(Column=api_name, Table=table)
							)
							if data_obj is not None:
								filter_values.append([row_data.Value for data in data_obj for row_data in data])
					else:
						filter_tag = (
							'<input type="text" class="form-control wth100visble bootstrap-table-filter-control-'
							+ str(api_name)
							+ '">'
						)
						filter_tags.append(filter_tag)
						filter_types.append("input")
						filter_values.append("")

			filter_drop_down = (
				"try { if( document.getElementById('"
				+ str(table_id)
				+ "') ) { var listws = document.getElementById('"
				+ str(table_id)
				+ "').getElementsByClassName('filter-control');  for (i = 0; i < listws.length; i++) { document.getElementById('"
				+ str(table_id)
				+ "').getElementsByClassName('filter-control')[i].innerHTML = data6[i];  } for (j = 0; j < listws.length; j++) { if (data10[j] == 'select') { var dataAdapter = new $.jqx.dataAdapter(data8[j]); if(data11[j].length>5){ $('#"
				+ str(table_id)
				+ "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter}); }else{$('#"
				+ str(table_id)
				+ "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter ,autoDropDownHeight: true});} } } } }  catch(err) { setTimeout(function() { var listws = document.getElementById('"
				+ str(table_id)
				+ "').getElementsByClassName('filter-control');  for (i = 0; i < listws.length; i++) { document.getElementById('"
				+ str(table_id)
				+ "').getElementsByClassName('filter-control')[i].innerHTML = data9[i];  } for (j = 0; j < listws.length; j++) { if (data10[j] == 'select') { var dataAdapter = new $.jqx.dataAdapter(data11[j]); $('#"
				+ str(table_id)
				+ "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter, scrollBarSize :10 }); } } }, 5000); }"
			)
			dbl_clk_function += (
				'$("'
				+ str(table_ids)
				+ '").on("all.bs.table", function (e, name, args) { $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); }); $("'
				+ str(table_ids)
				+ '\ th.bs-checkbox div.th-inner").before("<div class=\'pad0brdbt\'>SELECT</div>"); $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>");'
			)

			pagedata = ""
			if QryCount==0:
				pagedata = str(QryCount) + " - " + str(QryCount) + " of "
			elif QryCount < int(PerPage):
				pagedata = str(Page_start) + " - " + str(QryCount) + " of "
			else:
				pagedata = str(Page_start) + " - " + str(Page_End)+ " of "
			

		## COVERED OBJECTS END..

		# UNMAPPED EQUIPMENTS STARTED
		elif TABLEID.startswith("UNMAPPED") and str(CurrentTab) == "Quotes":
			TreeParam = Product.GetGlobal("TreeParam")
			TreeParentParam = Product.GetGlobal("TreeParentLevel0")  
			account_id = TreeParam.split(' - ')
			account_id = account_id[len(account_id)-1]
			
			Trace.Write("SAQFEQ"+str(account_id))
			where_string = ""
			if A_Keys != "" and A_Values != "":
				A_Keys = list(A_Keys)
				A_Values = list(A_Values)
				for key, value in zip(A_Keys, A_Values):
					if value.strip():
						if where_string:
							where_string += " AND "
						where_string += "{Key} LIKE '%{Value}%'".format(Key=key, Value=value)
			DIVNAME = "VIEW_DIV_ID"
			new_value_dict = {}
			ObjectName = "MAEQUP"
			table_id = "unmapped_equipments_addnew"
			Header_details = {
				"EQUIPMENT_RECORD_ID": "KEY",
				"EQUIPMENT_ID":"EQUIPMENT ID",
				"SERIAL_NO": "SERIAL NUMBER",
				"GREENBOOK": "GREENBOOK",
				"PLATFORM": "PLATFORM",
			}
			ordered_keys = [
				"EQUIPMENT_RECORD_ID",
				"EQUIPMENT_ID",
				"SERIAL_NO",
				"GREENBOOK",
				"PLATFORM",
			]
			Objd_Obj = Sql.GetList(
				"select FIELD_LABEL,API_NAME,LOOKUP_OBJECT,LOOKUP_API_NAME,DATA_TYPE,FORMULA_DATA_TYPE from SYOBJD (NOLOCK)where OBJECT_NAME = '"
				+ str(ObjectName)
				+ "'"
			)
			lookup_disply_list = []
			if Objd_Obj is not None:
				attr_list = {}
				api_names = [inn.API_NAME for inn in Objd_Obj]
				for attr in Objd_Obj:
					attr_list[str(attr.API_NAME)] = str(attr.FIELD_LABEL)
					if str(attr.LOOKUP_API_NAME) != "" and str(attr.LOOKUP_API_NAME) is not None:
						lookup_disply_list.append(str(attr.API_NAME))
				checkbox_list = [
					inn.API_NAME for inn in Objd_Obj if (inn.DATA_TYPE == "CHECKBOX" or inn.FORMULA_DATA_TYPE == "CHECKBOX")
				]
				lookup_list = {ins.LOOKUP_API_NAME: ins.API_NAME for ins in Objd_Obj}
			query_shp_values = Sql.GetFirst(" SELECT SALESORG_ID FROM SAQFBL (NOLOCK) WHERE FABLOCATION_ID = '{}' AND QUOTE_RECORD_ID = '{}' ".format(Product.GetGlobal("TreeParam"),contract_quote_record_id,))
			if	query_shp_values:
				sales_org = query_shp_values.SALESORG_ID
			else:
				Trace.Write("EXCEPT: sales_org ")
				sales_org = ""
			sec_str = '<div class="row modulebnr brdr ma_mar_btm">INSTALLED BASE EQUIPMENT LIST<button type="button" class="close flt_rt" onclick="closepopup_scrl()" data-dismiss="modal">X</button></div>'
			sec_str += '<div class="col-md-12 padlftrhtnone" id="btnhide"><div class="row pad-10 bg-lt-wt brdr"><img style="height: 40px; margin-top: -1px; margin-left: -1px; float: left;" src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/Secondary Icon.svg"/><div class="product_txt_div_child secondary_highlight" style="display: block;"><div class="product_txt_child"><abbr title="Key">Customer Region</abbr></div><div class="product_txt_to_top_child" style="float: left;"><abbr title="AMC">AMC</abbr></div></div><div class="product_txt_div_child secondary_highlight" style="display: block;"><div class="product_txt_child"><abbr title="Key">Sales Org</abbr></div><div class="product_txt_to_top_child" style="float: left;"><abbr title="{sales_org}">{sales_org}</abbr></div></div><div class="product_txt_div_child secondary_highlight" style="display: block;"><div class="product_txt_child"><abbr title="Key">Fab Location ID</abbr></div><div class="product_txt_to_top_child" style="float: left;"><abbr title="{}">{}</abbr></div></div><button type="button" class="btnconfig" data-dismiss="modal" onclick="closepopup_scrl()">CANCEL</button><button type="button" id="add-unmapped_equipment" class="btnconfig" onclick="addUnmappedEquipments()" data-dismiss="modal">ADD</button></div></div>'.format(
				Product.GetGlobal("TreeParam"), Product.GetGlobal("TreeParam"),sales_org = sales_org,
			)

			sec_str += '<div id="container" class="g4 pad-10 brdr except_sec header_section_div">'
			sec_str += (
				'<table id="'
				+ str(table_id)
				+ '" data-escape="true"  data-search-on-enter-key="true" data-show-header="true"  data-filter-control="true"> <thead><tr>'
			)
			sec_str += '<th data-field="SELECT" class="wth45" data-checkbox="true" id ="check_boxval" onchange = "get_checkedval()"><div class="action_col">SELECT</div></th>'

			for key, invs in enumerate(list(ordered_keys)):

				invs = str(invs).strip()
				qstring = Header_details.get(str(invs)) or ""
				if key == 0:
					sec_str += (
						'<th data-field="'
						+ str(invs)
						+ '" data-formatter="UnmappedListKeyHyperLink" data-sortable="true" data-title-tooltip="'
						+ str(qstring)
						+ '" data-filter-control="input">'
						+ str(qstring)
						+ "</th>"
					)
				else:
					sec_str += (
						'<th data-field="'
						+ invs
						+ '" data-title-tooltip="'
						+ str(qstring)
						+ '" data-sortable="true" data-filter-control="input">'
						+ str(qstring)
						+ "</th>"
					)
			sec_str += '</tr></thead><tbody class ="equipments_id" ></tbody></table>'
			sec_str += '<div id="unmapped_equipments_footer"></div>'
			values_list = ""
			values_lists = ""
			a_test = []
			for invsk in list(Header_details):
				table_ids = "#" + str(table_id)
				filter_class = table_ids + " .bootstrap-table-filter-control-" + str(invsk)
				values_lists += "var " + str(invsk) + ' = $("' + str(filter_class) + '").val(); '
				values_lists += " ATTRIBUTE_VALUEList.push(" + str(invsk) + "); "
				a_test.append(invsk)
				filter_control_function += (
					'$("'
					+ filter_class
					+ '").change( function(){ var table_id = $(this).closest("table").attr("id"); var a_list = '
					+ str(a_test)
					+ "; ATTRIBUTE_VALUEList = []; "
					+ str(values_lists)
					+ ' SortColumn = localStorage.getItem("SortColumn"); SortColumnOrder = localStorage.getItem("SortColumnOrder"); PerPage = $("#PageCountValue").val(); PageInform = "1___" + PerPage + "___" + PerPage; cpq.server.executeScript("SYUADNWPOP", {\'TABLEID\': "'
					+ str(TABLEID)
					+ "\", 'OPER': 'NO', 'RECORDID': \""
					+ str(RECORDID)
					+ "\", 'RECORDFEILD':  \""
					+ str(RECORDFEILD)
					+ "\", 'NEWVALUE': '', 'LOOKUPOBJ': '', 'LOOKUPAPI': '','A_Keys':a_list,'A_Values':ATTRIBUTE_VALUEList}, function(data) {  date_field = data[3]; var assoc = data[1]; var api_name = data[2];data4 = data[4];data5 = data[5]; try { if(date_field.length > 0) { $(\""
					+ str(table_ids)
					+ '").bootstrapTable("load", date_field  ); $("button#country_save").attr("disabled",false); $("#noRecDisp").remove() } else{ var date_field = [];$("'
					+ str(table_ids)
					+ '").bootstrapTable("load", date_field  ); $("button#country_save").attr("disabled",true); $("#unmapped_equipments_addnew").after("<div id=\'noRecDisp\' class=\'noRecord\'>No Records to Display</div>"); $(".noRecord:not(:first)").remove(); } } catch(err) { if(date_field.length > 0) { $("'
					+ str(table_ids)
					+ '").bootstrapTable("load", date_field  ); $("button#country_save").attr("disabled",false); } else{ $("'
					+ str(table_ids)
					+ '").bootstrapTable("load", date_field  ); $("button#country_save").attr("disabled",true); } } ; });  });'
				)
				

			sales_org_record_id = None
			account_record_id = None
			quote_obj = Sql.GetFirst(
				"SELECT SAQTMT.ACCOUNT_RECORD_ID, SAQTRV.SALESORG_RECORD_ID FROM SAQTMT (NOLOCK) JOIN SAQTRV (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQTRV.QUOTE_RECORD_ID AND SAQTMT.QTEREV_RECORD_ID = SAQTRV.QTEREV_RECORD_ID WHERE SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = '{}' AND SAQTRV.QTEREV_RECORD_ID ='{}' ".format(
					contract_quote_record_id,quote_revision_record_id
				)
			)
			if quote_obj:
				sales_org_record_id = quote_obj.SALESORG_RECORD_ID
				account_record_id = quote_obj.ACCOUNT_RECORD_ID
			if offset_skip_count%10==1:
				offset_skip_count-=1
			pagination_condition = "OFFSET {Offset_Skip_Count} ROWS FETCH NEXT {Fetch_Count} ROWS ONLY".format(
				Offset_Skip_Count=offset_skip_count, Fetch_Count=fetch_count
			)
			get_fab_query = Sql.GetList("SELECT FABLOCATION_ID FROM SAQFBL WHERE QUOTE_RECORD_ID = '{}' and ACCOUNT_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(contract_quote_record_id,account_id,quote_revision_record_id) )
			if get_fab_query:
				get_fab = tuple([fab.FABLOCATION_ID for fab in get_fab_query])
			else:
				get_fab = ""
			if where_string:
				where_string += " AND"
			if (("Sending Account -" in TreeParam) or ("Receiving Account -" in TreeParam)) and TreeParentParam == 'Fab Locations':
				Pagination_M = Sql.GetFirst(
					"SELECT COUNT(CpqTableEntryId) as count FROM {ObjectName} (NOLOCK) WHERE ACCOUNT_ID = '{account_id}' AND FABLOCATION_ID = 'UNMAPPED' AND EQUIPMENT_RECORD_ID NOT IN (SELECT EQUIPMENT_RECORD_ID FROM SAQFEQ (NOLOCK) WHERE QUOTE_RECORD_ID = '{contract_quote_record_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND FABLOCATION_ID = 'UNMAPPED')".format(
						ObjectName = ObjectName,
						account_id = account_id,
						contract_quote_record_id = contract_quote_record_id,quote_revision_record_id = quote_revision_record_id
					)
				)   
			else:
				Pagination_M = Sql.GetFirst(
					"SELECT COUNT(CpqTableEntryId) as count FROM {} (NOLOCK) WHERE ACCOUNT_RECORD_ID = '{}' AND FABLOCATION_ID = '{}' AND ISNULL(SERIAL_NO, '') <> '' AND ISNULL(GREENBOOK, '') <> '' AND {} EQUIPMENT_RECORD_ID NOT IN (SELECT EQUIPMENT_RECORD_ID FROM SAQFEQ (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND FABLOCATION_ID = '{}' AND ISNULL(SERIAL_NUMBER,'') <> '')".format(
						ObjectName,
						account_record_id,
						Product.GetGlobal("TreeParam"),
						where_string,
						contract_quote_record_id,
						Product.GetGlobal("TreeParam"),
						quote_revision_record_id,
					)
				)   	
			order_by = "order by FABLOCATION_NAME ASC"
			pop_val = {}

			if (("Sending Account -" in TreeParam) or ("Receiving Account -" in TreeParam)) and TreeParentParam == 'Fab Locations':
				where_string += """ ACCOUNT_ID = '{}' AND FABLOCATION_ID ='UNMAPPED' AND EQUIPMENT_RECORD_ID NOT IN (SELECT EQUIPMENT_RECORD_ID FROM SAQFEQ (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND FABLOCATION_ID = 'UNMAPPED')""".format(
					account_id,
					contract_quote_record_id,quote_revision_record_id=quote_revision_record_id,
				)
				table_data = Sql.GetList(
					"select {} from {} (NOLOCK) {} {} {}".format(
						", ".join(ordered_keys),
						ObjectName,
						"WHERE " + where_string if where_string else "",
						order_by,
						pagination_condition,
					)
				)	
			else:
				where_string += """ ACCOUNT_RECORD_ID = '{}' AND FABLOCATION_ID = '{}' AND ISNULL(SERIAL_NO, '') <> '' AND ISNULL(GREENBOOK, '') <> '' AND {} EQUIPMENT_RECORD_ID NOT IN (SELECT EQUIPMENT_RECORD_ID FROM SAQFEQ (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND FABLOCATION_ID = '{}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND ISNULL(SERIAL_NUMBER,'') <> '')""".format(
					account_record_id,
					Product.GetGlobal("TreeParam"),
					where_string,
					contract_quote_record_id,
					Product.GetGlobal("TreeParam"),quote_revision_record_id,
				)
				table_data = Sql.GetList(
					"select {} from {} (NOLOCK) {} {} {}".format(
						", ".join(ordered_keys),
						ObjectName,
						"WHERE " + where_string if where_string else "",
						order_by,
						pagination_condition,
					)
				)
			if table_data is not None :
				for row_data in table_data:
					data_id = str(ObjectName)

					new_value_dict = {}

					for data in row_data:
						if str(data.Key) == "EQUIPMENT_RECORD_ID":
							pop_val = str(data.Value) + "|unmapped_equipments"
							cpqidval = CPQID.KeyCPQId.GetCPQId(ObjectName, str(data.Value))
							new_value_dict[data.Key] = cpqidval
						else:
							new_value_dict[data.Key] = data.Value
						new_value_dict["pop_val"] = pop_val
					date_field.append(new_value_dict)
			QueryCount = len(date_field)

			pagination_total_count = 0
			if Pagination_M is not None:
				pagination_total_count = Pagination_M.count
			if offset_skip_count == 0:
				offset_skip_count = 1
				records_end = fetch_count
			else:
				offset_skip_count += 1
				records_end = offset_skip_count + fetch_count -1
			records_end = pagination_total_count if pagination_total_count < records_end else records_end
			records_start_and_end = "{} - {} of ".format(offset_skip_count, records_end)
			disable_next_and_last = ""
			disable_previous_and_first = ""
			if records_end == pagination_total_count:
				disable_next_and_last = "class='btn-is-disabled' style=\'pointer-events:none\' "
			if offset_skip_count == 0:
				disable_previous_and_first = "class='btn-is-disabled' style=\'pointer-events:none\' "
			current_page = int(math.ceil(offset_skip_count / fetch_count)) + 1

			Product.SetGlobal("QueryCount", str(QueryCount))
			pagination_table_id = "pagination_{}".format(table_id)
			#if QueryCount != 0:
			
			var_str = """<div id="{Parent_Div_Id}" class="col-md-12 brdr listContStyle padbthgt30">
								<div class="col-md-4 pager-numberofitem  clear-padding">
									<span class="pager-number-of-items-item flt_lt_pad2_mar2022" id="RecordsStartAndEnd">{Records_Start_And_End}</span>
									<span class="pager-number-of-items-item flt_lt_pad2_mar" id="TotalRecordsCount">{Pagination_Total_Count}</span>
									<div class="clear-padding fltltmrgtp3">
										<div class="pull-right vralign">
											<select onchange="ShowResultCountFunc(this, '{ShowResultCountFuncTb}', 'addUnmappedEquipment', '{TableId}')" id="ShowResultCount" class="form-control selcwdt">
												<option value="10" {Selected_10}>10</option>
												<option value="20" {Selected_20}>20</option>
												<option value="50" {Selected_50}>50</option>
												<option value="100" {Selected_100}>100</option>
												<option value="200" {Selected_200}>200</option>
											</select> 
										</div>
									</div>
								</div>
								<div class="col-xs-8 col-md-4  clear-padding inpadtex" data-bind="visible: totalItemCount">
									<div class="clear-padding col-xs-12 col-sm-6 col-md-12 brd0">
										<ul class="pagination pagination">
											<li class="disabled">
												<a onclick="GetFirstResultFunc('{GetFirstResultFuncTb}', 'addUnmappedEquipment', '{TableId}')" {Disable_First}><i class="fa fa-caret-left fnt14bold"></i><i class="fa fa-caret-left fnt14"></i></a>
											</li>
											<li class="disabled"><a onclick="GetPreviuosResultFunc('{GetPreviuosResultFuncTb}', 'addUnmappedEquipment', '{TableId}')" {Disable_Previous}><i class="fa fa-caret-left fnt14"></i>PREVIOUS</a></li>
											<li class="disabled"><a onclick="GetNextResultFunc('{GetNextResultFuncTb}', 'addUnmappedEquipment', '{TableId}')" {Disable_Next}>NEXT<i class="fa fa-caret-right fnt14"></i></a></li>
											<li class="disabled"><a onclick="GetLastResultFunc('{GetLastResultFuncTb}', 'addUnmappedEquipment', '{TableId}')" {Disable_Last}><i class="fa fa-caret-right fnt14"></i><i class="fa fa-caret-right fnt14bold"></i></a></li>
										</ul>
									</div> 
								</div> 
								<div class="col-md-4 pad3"> 
									<span id="page_count" class="currentPage page_right_content">{Current_Page}</span>
									<span class="page_right_content padrt2">Page </span>
								</div>
							</div>""".format(
				Parent_Div_Id=pagination_table_id,
				Records_Start_And_End=records_start_and_end,
				Pagination_Total_Count=pagination_total_count,
				ShowResultCountFuncTb=pagination_table_id,
				Selected_10="selected" if fetch_count == 10 else "",
				Selected_20="selected" if fetch_count == 20 else "",
				Selected_50="selected" if fetch_count == 50 else "",
				Selected_100="selected" if fetch_count == 100 else "",
				Selected_200="selected" if fetch_count == 200 else "",
				GetFirstResultFuncTb=pagination_table_id,
				Disable_First=disable_previous_and_first,
				GetPreviuosResultFuncTb=pagination_table_id,
				Disable_Previous=disable_previous_and_first,
				GetNextResultFuncTb=pagination_table_id,
				Disable_Next=disable_next_and_last,
				GetLastResultFuncTb=pagination_table_id,
				Disable_Last=disable_next_and_last,
				Current_Page=current_page,
				TableId=TABLEID,
			)
			# else:
			#     date_field = "NORECORDS"
			#     Trace.Write("No Equipment Records")
			table_ids = "#" + str(table_id)
			# Filter based on table MultiSelect Dropdown column - Start

			for index, col_name in enumerate(ordered_keys):
				table, api_name = ObjectName, col_name
				obj_data = Sql.GetFirst(
					"SELECT API_NAME, DATA_TYPE, PICKLIST FROM  SYOBJD WHERE OBJECT_NAME='"
					+ str(table)
					+ "' and API_NAME = '"
					+ str(api_name)
					+ "'"
				)
				if obj_data is not None:
					if str(obj_data.PICKLIST).upper() == "TRUE":
						filter_tag = (
							'<div id = "'
							+ str(table_id)
							+ "_RelatedMutipleCheckBoxDrop_"
							+ str(index)
							+ '" class="form-control bootstrap-table-filter-control-'
							+ str(api_name)
							+ " RelatedMutipleCheckBoxDrop_"
							+ str(index)
							+ ' "></div>'
						)
						filter_tags.append(filter_tag)
						filter_types.append("select")
						if obj_data.DATA_TYPE == "CHECKBOX":
							filter_values.append(["True", "False"])
						else:
							# Trace.Write("=============$$$$$$$$$$$$$>>>>>>>>>>>>> "+"SELECT DISTINCT {Column} FROM {Table}".format(Column=api_name, Table=table))
							data_obj = Sql.GetList(
								"SELECT DISTINCT {Column} FROM {Table}".format(Column=api_name, Table=table)
							)
							if data_obj is not None:
								filter_values.append([row_data.Value for data in data_obj for row_data in data])
					else:
						filter_tag = (
							'<input type="text" class="form-control wth100visble bootstrap-table-filter-control-'
							+ str(api_name)
							+ '">'
						)
						filter_tags.append(filter_tag)
						filter_types.append("input")
						filter_values.append("")

			filter_drop_down = (
				"try { if( document.getElementById('"
				+ str(table_id)
				+ "') ) { var listws = document.getElementById('"
				+ str(table_id)
				+ "').getElementsByClassName('filter-control');  for (i = 0; i < listws.length; i++) { document.getElementById('"
				+ str(table_id)
				+ "').getElementsByClassName('filter-control')[i].innerHTML = data6[i];  } for (j = 0; j < listws.length; j++) { if (data10[j] == 'select') { var dataAdapter = new $.jqx.dataAdapter(data8[j]); if(data11[j].length>5){ $('#"
				+ str(table_id)
				+ "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter}); }else{$('#"
				+ str(table_id)
				+ "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter ,autoDropDownHeight: true});} } } } }  catch(err) { setTimeout(function() { var listws = document.getElementById('"
				+ str(table_id)
				+ "').getElementsByClassName('filter-control');  for (i = 0; i < listws.length; i++) { document.getElementById('"
				+ str(table_id)
				+ "').getElementsByClassName('filter-control')[i].innerHTML = data9[i];  } for (j = 0; j < listws.length; j++) { if (data10[j] == 'select') { var dataAdapter = new $.jqx.dataAdapter(data11[j]); $('#"
				+ str(table_id)
				+ "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter, scrollBarSize :10 }); } } }, 5000); }"
			)
			dbl_clk_function += (
				'$("'
				+ str(table_ids)
				+ '").on("all.bs.table", function (e, name, args) { $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); }); $("'
				+ str(table_ids)
				+ '\ th.bs-checkbox div.th-inner").before("<div class=\'pad0brdbt\'>SELECT</div>"); $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>");'
			)
		# UNMAPPED EQUIPMENTS ENDED


		elif str(ObjectName) == "SAQFEQ" and str(CurrentTab) == "Quotes":
			TreeParam = Product.GetGlobal("TreeParam")
			TreeParentParam = Product.GetGlobal("TreeParentLevel0")  
			account_id = TreeParam.split(' - ')
			account_id = account_id[len(account_id)-1]
			
			Trace.Write("SAQFEQ"+str(account_id))
			where_string = ""
			if A_Keys != "" and A_Values != "":
				A_Keys = list(A_Keys)
				A_Values = list(A_Values)
				for key, value in zip(A_Keys, A_Values):
					if value.strip():
						if where_string:
							where_string += " AND "
						where_string += "{Key} LIKE '%{Value}%'".format(Key=key, Value=value)
			DIVNAME = "VIEW_DIV_ID"
			new_value_dict = {}
			ObjectName = "MAEQUP"
			table_id = "equipments_addnew"
			Header_details = {
				"EQUIPMENT_RECORD_ID": "KEY",
				"EQUIPMENT_ID":"EQUIPMENT ID",
				"EQUIPMENT_DESCRIPTION":"EQUIPMENT_DESCRIPTION",
				"SERIAL_NO": "SERIAL NUMBER",
				"GREENBOOK": "GREENBOOK",
				"PLATFORM": "PLATFORM",
			}
			ordered_keys = [
				"EQUIPMENT_RECORD_ID",
				"EQUIPMENT_ID",
				"EQUIPMENT_DESCRIPTION",
				"SERIAL_NO",
				"GREENBOOK",
				"PLATFORM",
			]
			Trace.Write('3178--------')
			Objd_Obj = Sql.GetList(
				"select FIELD_LABEL,API_NAME,LOOKUP_OBJECT,LOOKUP_API_NAME,DATA_TYPE,FORMULA_DATA_TYPE from SYOBJD (NOLOCK)where OBJECT_NAME = '"
				+ str(ObjectName)
				+ "'"
			)
			lookup_disply_list = []
			if Objd_Obj is not None:
				attr_list = {}
				api_names = [inn.API_NAME for inn in Objd_Obj]
				for attr in Objd_Obj:
					attr_list[str(attr.API_NAME)] = str(attr.FIELD_LABEL)
					if str(attr.LOOKUP_API_NAME) != "" and str(attr.LOOKUP_API_NAME) is not None:
						lookup_disply_list.append(str(attr.API_NAME))
				checkbox_list = [
					inn.API_NAME for inn in Objd_Obj if (inn.DATA_TYPE == "CHECKBOX" or inn.FORMULA_DATA_TYPE == "CHECKBOX")
				]
				lookup_list = {ins.LOOKUP_API_NAME: ins.API_NAME for ins in Objd_Obj}
			query_shp_values = Sql.GetFirst(" SELECT SALESORG_ID,REGION FROM SAQTRV (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QUOTE_REVISION_RECORD_ID = '{}'".format(contract_quote_record_id,quote_revision_record_id))
			if	query_shp_values:
				sales_org = query_shp_values.SALESORG_ID
				region = query_shp_values.REGION	
			sec_str = '<div class="row modulebnr brdr ma_mar_btm">INSTALLED BASE EQUIPMENT LIST<button type="button" class="close flt_rt" onclick="closepopup_scrl()" data-dismiss="modal">X</button></div>'
			sec_str += '<div class="col-md-12 padlftrhtnone" id="btnhide"><div class="row pad-10 bg-lt-wt brdr"><img style="height: 40px; margin-top: -1px; margin-left: -1px; float: left;" src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/Secondary Icon.svg"/><div class="product_txt_div_child secondary_highlight" style="display: block;"><div class="product_txt_child"><abbr title="Key">Customer Region</abbr></div><div class="product_txt_to_top_child" style="float: left;"><abbr title="{region}">{region}</abbr></div></div><div class="product_txt_div_child secondary_highlight" style="display: block;"><div class="product_txt_child"><abbr title="Key">Sales Org</abbr></div><div class="product_txt_to_top_child" style="float: left;"><abbr title="{sales_org}">{sales_org}</abbr></div></div><div class="product_txt_div_child secondary_highlight" style="display: block;"><div class="product_txt_child"><abbr title="Key">Fab Location ID</abbr></div><div class="product_txt_to_top_child" style="float: left;"><abbr title="{}">{}</abbr></div></div><button type="button" class="btnconfig" data-dismiss="modal" onclick="closepopup_scrl()">CANCEL</button><button type="button" id="add-equipment" class="btnconfig" onclick="addEquipments()" data-dismiss="modal">ADD</button></div></div>'.format(
				Product.GetGlobal("TreeParam"), Product.GetGlobal("TreeParam"),sales_org = sales_org,region = region
			)

			sec_str += '<div id="container" class="g4 pad-10 brdr except_sec header_section_div">'
			sec_str += (
				'<table id="'
				+ str(table_id)
				+ '" data-escape="true"  data-search-on-enter-key="true" data-show-header="true"  data-filter-control="true"> <thead><tr>'
			)
			sec_str += '<th data-field="SELECT" class="wth45" data-checkbox="true" id ="check_boxval" onchange = "get_checkedval()"><div class="action_col">SELECT</div></th>'

			for key, invs in enumerate(list(ordered_keys)):

				invs = str(invs).strip()
				qstring = Header_details.get(str(invs)) or ""
				if key == 0:
					sec_str += (
						'<th data-field="'
						+ str(invs)
						+ '" data-formatter="fablocationListKeyHyperLink" data-sortable="true" data-title-tooltip="'
						+ str(qstring)
						+ '" data-filter-control="input">'
						+ str(qstring)
						+ "</th>"
					)
				else:
					sec_str += (
						'<th data-field="'
						+ invs
						+ '" data-title-tooltip="'
						+ str(qstring)
						+ '" data-sortable="true" data-filter-control="input">'
						+ str(qstring)
						+ "</th>"
					)
			sec_str += '</tr></thead><tbody class ="equipments_id" ></tbody></table>'
			sec_str += '<div id="equipments_footer"></div>'
			values_list = ""
			values_lists = ""
			a_test = []
			for invsk in list(Header_details):
				table_ids = "#" + str(table_id)
				filter_class = table_ids + " .bootstrap-table-filter-control-" + str(invsk)
				values_lists += "var " + str(invsk) + ' = $("' + str(filter_class) + '").val(); '
				values_lists += " ATTRIBUTE_VALUEList.push(" + str(invsk) + "); "
				a_test.append(invsk)
				filter_control_function += (
					'$("'
					+ filter_class
					+ '").change( function(){ var table_id = $(this).closest("table").attr("id"); var a_list = '
					+ str(a_test)
					+ "; ATTRIBUTE_VALUEList = []; "
					+ str(values_lists)
					+ ' SortColumn = localStorage.getItem("SortColumn"); SortColumnOrder = localStorage.getItem("SortColumnOrder"); PerPage = $("#PageCountValue").val(); PageInform = "1___" + PerPage + "___" + PerPage; cpq.server.executeScript("SYUADNWPOP", {\'TABLEID\': "'
					+ str(TABLEID)
					+ "\", 'OPER': 'NO', 'RECORDID': \""
					+ str(RECORDID)
					+ "\", 'RECORDFEILD':  \""
					+ str(RECORDFEILD)
					+ "\", 'NEWVALUE': '', 'LOOKUPOBJ': '', 'LOOKUPAPI': '','A_Keys':a_list,'A_Values':ATTRIBUTE_VALUEList}, function(data) {  date_field = data[3]; var assoc = data[1]; var api_name = data[2];data4 = data[4];data5 = data[5]; try { if(date_field.length > 0) { $(\""
					+ str(table_ids)
					+ '").bootstrapTable("load", date_field  ); $("button#country_save").attr("disabled",false); $("#noRecDisp").remove() } else{ var date_field = [];$("'
					+ str(table_ids)
					+ '").bootstrapTable("load", date_field  ); $("button#country_save").attr("disabled",true); $("#equipments_addnew").after("<div id=\'noRecDisp\' class=\'noRecord\'>No Records to Display</div>"); $(".noRecord:not(:first)").remove(); } } catch(err) { if(date_field.length > 0) { $("'
					+ str(table_ids)
					+ '").bootstrapTable("load", date_field  ); $("button#country_save").attr("disabled",false); } else{ $("'
					+ str(table_ids)
					+ '").bootstrapTable("load", date_field  ); $("button#country_save").attr("disabled",true); } } ; });  });'
				)
				

			sales_org_record_id = None
			account_record_id = None
			quote_obj = Sql.GetFirst(
				"SELECT SAQTMT.ACCOUNT_RECORD_ID, SAQTRV.SALESORG_RECORD_ID FROM SAQTMT (NOLOCK) JOIN SAQTRV (NOLOCK) ON SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = SAQTRV.QUOTE_RECORD_ID WHERE SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = '{}' AND SAQTMT.QTEREV_RECORD_ID = '{}'".format(
					contract_quote_record_id,quote_revision_record_id
				)
			)
			if quote_obj:
				sales_org_record_id = quote_obj.SALESORG_RECORD_ID
				account_record_id = quote_obj.ACCOUNT_RECORD_ID
			if offset_skip_count%10==1:
				offset_skip_count-=1
			pagination_condition = "OFFSET {Offset_Skip_Count} ROWS FETCH NEXT {Fetch_Count} ROWS ONLY".format(
				Offset_Skip_Count=offset_skip_count, Fetch_Count=fetch_count
			)
			get_fab_query = Sql.GetList("SELECT FABLOCATION_ID FROM SAQFBL WHERE QUOTE_RECORD_ID = '{}' and ACCOUNT_ID = '{}' AND QTEREV_RECORD_ID = '{}' ".format(contract_quote_record_id,account_id,quote_revision_record_id) )
			if get_fab_query:
				get_fab = tuple([fab.FABLOCATION_ID for fab in get_fab_query])
			else:
				get_fab = ""
			if where_string:
				where_string += " AND"
			if (("Sending Account -" in TreeParam) or ("Receiving Account -" in TreeParam)) and TreeParentParam == 'Fab Locations':
				Pagination_M = Sql.GetFirst(
					"SELECT COUNT(CpqTableEntryId) as count FROM {ObjectName} (NOLOCK) WHERE ACCOUNT_ID = '{account_id}' AND FABLOCATION_ID in {get_fab} AND ISNULL(SERIAL_NO, '') <> '' AND ISNULL(GREENBOOK, '') <> '' AND EQUIPMENT_RECORD_ID NOT IN (SELECT EQUIPMENT_RECORD_ID FROM SAQFEQ (NOLOCK) WHERE QUOTE_RECORD_ID = '{contract_quote_record_id}' AND FABLOCATION_ID in {get_fab}  AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND ISNULL(SERIAL_NUMBER,'') <> '')".format(
						ObjectName = ObjectName,
						account_id = account_id,
						get_fab = get_fab,
						contract_quote_record_id = contract_quote_record_id,
						quote_revision_record_id = quote_revision_record_id,
					)
				)   
			else:
				Pagination_M = Sql.GetFirst(
					"SELECT COUNT(CpqTableEntryId) as count FROM {} (NOLOCK) WHERE ACCOUNT_RECORD_ID = '{}' AND FABLOCATION_ID = '{}' AND ISNULL(SERIAL_NO, '') <> '' AND ISNULL(GREENBOOK, '') <> '' AND {} EQUIPMENT_RECORD_ID NOT IN (SELECT EQUIPMENT_RECORD_ID FROM SAQFEQ (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND FABLOCATION_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND ISNULL(SERIAL_NUMBER,'') <> '')".format(
						ObjectName,
						account_record_id,
						Product.GetGlobal("TreeParam"),
						where_string,
						contract_quote_record_id,
						Product.GetGlobal("TreeParam"),
						quote_revision_record_id,
					)
				)   	
			order_by = "order by FABLOCATION_NAME ASC"
			pop_val = {}

			if (("Sending Account -" in TreeParam) or ("Receiving Account -" in TreeParam)) and TreeParentParam == 'Fab Locations':
				where_string += """ ACCOUNT_ID = '{}' AND FABLOCATION_ID ='' AND ISNULL(SERIAL_NO, '') <> '' AND ISNULL(GREENBOOK, '') <> '' AND EQUIPMENT_RECORD_ID NOT IN (SELECT EQUIPMENT_RECORD_ID FROM SAQFEQ (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND FABLOCATION_ID = '' AND QTEREV_RECORD_ID = '{}' AND ISNULL(SERIAL_NUMBER,'') <> '')""".format(
					account_id,
					contract_quote_record_id,quote_revision_record_id
				)
				table_data = Sql.GetList(
					"select {} from {} (NOLOCK) {} {} {}".format(
						", ".join(ordered_keys),
						ObjectName,
						"WHERE " + where_string if where_string else "",
						order_by,
						pagination_condition,
					)
				)	
			else:
				where_string += """ ACCOUNT_RECORD_ID = '{}' AND FABLOCATION_ID = '{}' AND ISNULL(SERIAL_NO, '') <> '' AND ISNULL(GREENBOOK, '') <> '' AND {} EQUIPMENT_RECORD_ID NOT IN (SELECT EQUIPMENT_RECORD_ID FROM SAQFEQ (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND FABLOCATION_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND ISNULL(SERIAL_NUMBER,'') <> '')""".format(
					account_record_id,
					Product.GetGlobal("TreeParam"),
					where_string,
					contract_quote_record_id,
					Product.GetGlobal("TreeParam"),
					quote_revision_record_id,
				)
				table_data = Sql.GetList(
					"select {} from {} (NOLOCK) {} {} {}".format(
						", ".join(ordered_keys),
						ObjectName,
						"WHERE " + where_string if where_string else "",
						order_by,
						pagination_condition,
					)
				)
			if table_data is not None :
				for row_data in table_data:
					data_id = str(ObjectName)

					new_value_dict = {}

					for data in row_data:
						if str(data.Key) == "EQUIPMENT_RECORD_ID":
							pop_val = str(data.Value) + "|equipments"
							cpqidval = CPQID.KeyCPQId.GetCPQId(ObjectName, str(data.Value))
							new_value_dict[data.Key] = cpqidval
						else:
							new_value_dict[data.Key] = data.Value
						new_value_dict["pop_val"] = pop_val
					date_field.append(new_value_dict)
			QueryCount = len(date_field)

			pagination_total_count = 0
			if Pagination_M is not None:
				pagination_total_count = Pagination_M.count
			if offset_skip_count == 0:
				offset_skip_count = 1
				records_end = fetch_count
			else:
				offset_skip_count += 1
				records_end = offset_skip_count + fetch_count -1
			records_end = pagination_total_count if pagination_total_count < records_end else records_end
			records_start_and_end = "{} - {} of ".format(offset_skip_count, records_end)
			disable_next_and_last = ""
			disable_previous_and_first = ""
			if records_end == pagination_total_count:
				disable_next_and_last = "class='btn-is-disabled' style=\'pointer-events:none\' "
			if offset_skip_count == 0:
				disable_previous_and_first = "class='btn-is-disabled' style=\'pointer-events:none\' "
			current_page = int(math.ceil(offset_skip_count / fetch_count)) + 1

			Product.SetGlobal("QueryCount", str(QueryCount))
			pagination_table_id = "pagination_{}".format(table_id)
			#if QueryCount != 0:
			
			var_str = """<div id="{Parent_Div_Id}" class="col-md-12 brdr listContStyle padbthgt30">
								<div class="col-md-4 pager-numberofitem  clear-padding">
									<span class="pager-number-of-items-item flt_lt_pad2_mar2022" id="RecordsStartAndEnd">{Records_Start_And_End}</span>
									<span class="pager-number-of-items-item flt_lt_pad2_mar" id="TotalRecordsCount">{Pagination_Total_Count}</span>
									<div class="clear-padding fltltmrgtp3">
										<div class="pull-right vralign">
											<select onchange="ShowResultCountFunc(this, '{ShowResultCountFuncTb}', 'addEquipment', '{TableId}')" id="ShowResultCount" class="form-control selcwdt">
												<option value="10" {Selected_10}>10</option>
												<option value="20" {Selected_20}>20</option>
												<option value="50" {Selected_50}>50</option>
												<option value="100" {Selected_100}>100</option>
												<option value="200" {Selected_200}>200</option>
											</select> 
										</div>
									</div>
								</div>
								<div class="col-xs-8 col-md-4  clear-padding inpadtex" data-bind="visible: totalItemCount">
									<div class="clear-padding col-xs-12 col-sm-6 col-md-12 brd0">
										<ul class="pagination pagination">
											<li class="disabled">
												<a onclick="GetFirstResultFunc('{GetFirstResultFuncTb}', 'addEquipment', '{TableId}')" {Disable_First}><i class="fa fa-caret-left fnt14bold"></i><i class="fa fa-caret-left fnt14"></i></a>
											</li>
											<li class="disabled"><a onclick="GetPreviuosResultFunc('{GetPreviuosResultFuncTb}', 'addEquipment', '{TableId}')" {Disable_Previous}><i class="fa fa-caret-left fnt14"></i>PREVIOUS</a></li>
											<li class="disabled"><a onclick="GetNextResultFunc('{GetNextResultFuncTb}', 'addEquipment', '{TableId}')" {Disable_Next}>NEXT<i class="fa fa-caret-right fnt14"></i></a></li>
											<li class="disabled"><a onclick="GetLastResultFunc('{GetLastResultFuncTb}', 'addEquipment', '{TableId}')" {Disable_Last}><i class="fa fa-caret-right fnt14"></i><i class="fa fa-caret-right fnt14bold"></i></a></li>
										</ul>
									</div> 
								</div> 
								<div class="col-md-4 pad3"> 
									<span id="page_count" class="currentPage page_right_content">{Current_Page}</span>
									<span class="page_right_content padrt2">Page </span>
								</div>
							</div>""".format(
				Parent_Div_Id=pagination_table_id,
				Records_Start_And_End=records_start_and_end,
				Pagination_Total_Count=pagination_total_count,
				ShowResultCountFuncTb=pagination_table_id,
				Selected_10="selected" if fetch_count == 10 else "",
				Selected_20="selected" if fetch_count == 20 else "",
				Selected_50="selected" if fetch_count == 50 else "",
				Selected_100="selected" if fetch_count == 100 else "",
				Selected_200="selected" if fetch_count == 200 else "",
				GetFirstResultFuncTb=pagination_table_id,
				Disable_First=disable_previous_and_first,
				GetPreviuosResultFuncTb=pagination_table_id,
				Disable_Previous=disable_previous_and_first,
				GetNextResultFuncTb=pagination_table_id,
				Disable_Next=disable_next_and_last,
				GetLastResultFuncTb=pagination_table_id,
				Disable_Last=disable_next_and_last,
				Current_Page=current_page,
				TableId=TABLEID,
			)
			# else:
			#     date_field = "NORECORDS"
			#     Trace.Write("No Equipment Records")
			table_ids = "#" + str(table_id)
			# Filter based on table MultiSelect Dropdown column - Start

			for index, col_name in enumerate(ordered_keys):
				table, api_name = ObjectName, col_name
				obj_data = Sql.GetFirst(
					"SELECT API_NAME, DATA_TYPE, PICKLIST FROM  SYOBJD WHERE OBJECT_NAME='"
					+ str(table)
					+ "' and API_NAME = '"
					+ str(api_name)
					+ "'"
				)
				if obj_data is not None:
					if str(obj_data.PICKLIST).upper() == "TRUE":
						filter_tag = (
							'<div id = "'
							+ str(table_id)
							+ "_RelatedMutipleCheckBoxDrop_"
							+ str(index)
							+ '" class="form-control bootstrap-table-filter-control-'
							+ str(api_name)
							+ " RelatedMutipleCheckBoxDrop_"
							+ str(index)
							+ ' "></div>'
						)
						filter_tags.append(filter_tag)
						filter_types.append("select")
						if obj_data.DATA_TYPE == "CHECKBOX":
							filter_values.append(["True", "False"])
						else:
							# Trace.Write("=============$$$$$$$$$$$$$>>>>>>>>>>>>> "+"SELECT DISTINCT {Column} FROM {Table}".format(Column=api_name, Table=table))
							data_obj = Sql.GetList(
								"SELECT DISTINCT {Column} FROM {Table}".format(Column=api_name, Table=table)
							)
							if data_obj is not None:
								filter_values.append([row_data.Value for data in data_obj for row_data in data])
					else:
						filter_tag = (
							'<input type="text" class="form-control wth100visble bootstrap-table-filter-control-'
							+ str(api_name)
							+ '">'
						)
						filter_tags.append(filter_tag)
						filter_types.append("input")
						filter_values.append("")

			filter_drop_down = (
				"try { if( document.getElementById('"
				+ str(table_id)
				+ "') ) { var listws = document.getElementById('"
				+ str(table_id)
				+ "').getElementsByClassName('filter-control');  for (i = 0; i < listws.length; i++) { document.getElementById('"
				+ str(table_id)
				+ "').getElementsByClassName('filter-control')[i].innerHTML = data6[i];  } for (j = 0; j < listws.length; j++) { if (data10[j] == 'select') { var dataAdapter = new $.jqx.dataAdapter(data8[j]); if(data11[j].length>5){ $('#"
				+ str(table_id)
				+ "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter}); }else{$('#"
				+ str(table_id)
				+ "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter ,autoDropDownHeight: true});} } } } }  catch(err) { setTimeout(function() { var listws = document.getElementById('"
				+ str(table_id)
				+ "').getElementsByClassName('filter-control');  for (i = 0; i < listws.length; i++) { document.getElementById('"
				+ str(table_id)
				+ "').getElementsByClassName('filter-control')[i].innerHTML = data9[i];  } for (j = 0; j < listws.length; j++) { if (data10[j] == 'select') { var dataAdapter = new $.jqx.dataAdapter(data11[j]); $('#"
				+ str(table_id)
				+ "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter, scrollBarSize :10 }); } } }, 5000); }"
			)
			dbl_clk_function += (
				'$("'
				+ str(table_ids)
				+ '").on("all.bs.table", function (e, name, args) { $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); }); $("'
				+ str(table_ids)
				+ '\ th.bs-checkbox div.th-inner").before("<div class=\'pad0brdbt\'>SELECT</div>"); $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>");'
			)

		elif (str(ObjectName) == "SAQRSP" or str(ObjectName)=="SAQSPT") and str(CurrentTab) == "Quotes":
			Trace.Write('In '+str(ObjectName))
			popup_obj = ObjectName
			where_string = ""
			where_string_1 = ""
			if A_Keys != "" and A_Values != "":
				A_Keys = list(A_Keys)
				A_Values = list(A_Values)
				for key, value in zip(A_Keys, A_Values):
					if value.strip():
						if where_string:
							where_string += " AND "
						if key=="MATERIAL_RECORD_ID":
							key="MAMTRL.CpqTableEntryId"
						where_string += "{Key} LIKE '%{Value}%'".format(Key=key, Value=value)
			DIVNAME = "VIEW_DIV_ID"
			new_value_dict = {}
			ObjectName = "MAMTRL"
			table_id = "parts-addnew-model"
			Header_details = {
				"MATERIAL_RECORD_ID": "KEY",
				"SAP_PART_NUMBER": "PART NUMBER",
				"SAP_DESCRIPTION": "PARTS NAME",
				"MATPRIGRP_ID":"MATERIAL PRICING GROUP ID"
			}
			ordered_keys = [
				"MATERIAL_RECORD_ID",
				"SAP_PART_NUMBER",
				"SAP_DESCRIPTION",
				"MATPRIGRP_ID"
			]
			Objd_Obj = Sql.GetList(
				"select FIELD_LABEL,API_NAME,LOOKUP_OBJECT,LOOKUP_API_NAME,DATA_TYPE,FORMULA_DATA_TYPE from SYOBJD (NOLOCK)where OBJECT_NAME = '"
				+ str(ObjectName)
				+ "'"
			)
			lookup_disply_list = []
			if Objd_Obj is not None:
				attr_list = {}
				api_names = [inn.API_NAME for inn in Objd_Obj]
				for attr in Objd_Obj:
					attr_list[str(attr.API_NAME)] = str(attr.FIELD_LABEL)
					if str(attr.LOOKUP_API_NAME) != "" and str(attr.LOOKUP_API_NAME) is not None:
						lookup_disply_list.append(str(attr.API_NAME))
				checkbox_list = [
					inn.API_NAME for inn in Objd_Obj if (inn.DATA_TYPE == "CHECKBOX" or inn.FORMULA_DATA_TYPE == "CHECKBOX")
				]
				lookup_list = {ins.LOOKUP_API_NAME: ins.API_NAME for ins in Objd_Obj}
			sec_str = '<div class="row modulebnr brdr ma_mar_btm">ADD PARTS<button type="button" class="close flt_rt" onclick="closepopup_scrl()" data-dismiss="modal">X</button></div>'
			sec_str += '<div class="col-md-12 padlftrhtnone"><div class="row pad-10 bg-lt-wt brdr"> <img style="height: 40px; margin-top: -1px; margin-left: -1px; float: left;" src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/Secondary Icon.svg"/><div class="product_txt_div_child secondary_highlight" style="display: block;text-align: left;"><div class="product_txt_child"><abbr title="Add Parts">Add Parts</abbr></div><div class="product_txt_to_top_child"><abbr title="select from the list parts below to add them to your Product Offering...">select from the list parts below to add them to your Product Offering...</abbr></div></div><button type="button" class="btnconfig" data-dismiss="modal" onclick="closepopup_scrl()">CANCEL</button><button type="button" id="add-parts" class="btnconfig" onclick="addPartsList()" data-dismiss="modal">ADD</button></div></div>'

			sec_str += '<div id="container" class="g4 pad-10 brdr except_sec">'
			sec_str += (
				'<table id="'
				+ str(table_id)
				+ '" data-escape="true"  data-search-on-enter-key="true" data-show-header="true"  data-filter-control="true"> <thead><tr>'
			)
			sec_str += '<th data-field="SELECT" class="wth45" data-checkbox="true" id ="check_boxval" onchange = "get_checkedval()"><div class="action_col">SELECT</div></th>'

			for key, invs in enumerate(list(ordered_keys)):

				invs = str(invs).strip()
				qstring = Header_details.get(str(invs)) or ""
				if key == 0:
					sec_str += (
						'<th data-field="'
						+ str(invs)
						+ '" data-formatter="partsModelListKeyHyperLink" data-sortable="true" data-title-tooltip="'
						+ str(qstring)
						+ '" data-filter-control="input">'
						+ str(qstring)
						+ "</th>"
					)
				else:
					sec_str += (
						'<th data-field="'
						+ invs
						+ '" data-title-tooltip="'
						+ str(qstring)
						+ '" data-sortable="true" data-filter-control="input">'
						+ str(qstring)
						+ "</th>"
					)
			sec_str += '</tr></thead><tbody class ="user_id" ></tbody></table>'
			sec_str += '<div id="add-parts-model-footer"></div>'
			values_list = ""
			values_lists = ""
			a_test = []
			for invsk in list(Header_details):
				table_ids = "#" + str(table_id)
				filter_class = table_ids + " .bootstrap-table-filter-control-" + str(invsk)
				values_lists += "var " + str(invsk) + ' = $("' + str(filter_class) + '").val(); '
				values_lists += " ATTRIBUTE_VALUEList.push(" + str(invsk) + "); "
				a_test.append(invsk)
				filter_control_function += (
					'$("'
					+ filter_class
					+ '").change( function(){ var table_id = $(this).closest("table").attr("id"); var a_list = '
					+ str(a_test)
					+ "; ATTRIBUTE_VALUEList = []; "
					+ str(values_lists)
					+ ' SortColumn = localStorage.getItem("SortColumn"); SortColumnOrder = localStorage.getItem("SortColumnOrder"); PerPage = $("#PageCountValue").val(); PageInform = "1___" + PerPage + "___" + PerPage; cpq.server.executeScript("SYUADNWPOP", {\'TABLEID\': "'
					+ str(TABLEID)
					+ "\", 'OPER': 'NO', 'RECORDID': \""
					+ str(RECORDID)
					+ "\", 'RECORDFEILD':  \""
					+ str(RECORDFEILD)
					+ "\", 'NEWVALUE': '', 'LOOKUPOBJ': '', 'LOOKUPAPI': '','A_Keys':a_list,'A_Values':ATTRIBUTE_VALUEList}, function(data) {  date_field = data[3]; var assoc = data[1]; var api_name = data[2];data4 = data[4];data5 = data[5]; data15 = data[15]; data16 = data[16]; try { if(date_field.length > 0) { $(\""
					+ str(table_ids)
					+ '").bootstrapTable("load", date_field  );$("#noRecDisp").remove(); if (document.getElementById("RecordsStartAndEnd")){document.getElementById("RecordsStartAndEnd").innerHTML = data15;}; if (document.getElementById("TotalRecordsCount")) {document.getElementById("TotalRecordsCount").innerHTML = data16;} } else{ $("'
					+ str(table_ids)
					+ '").bootstrapTable("load", date_field  );$("#parts-addnew-model").after("<div id=\'noRecDisp\' class=\'noRecord\'>No Records to Display</div>"); $(".noRecord:not(:first)").remove(); } } catch(err) { if(date_field.length > 0) { $("'
					+ str(table_ids)
					+ '").bootstrapTable("load", date_field  ); } else{ $("'
					+ str(table_ids)
					+ '").bootstrapTable("load", date_field  ); document.getElementById("add-parts-model-footer").style.border = "1px solid #ccc"; document.getElementById("add-parts-model-footer").style.padding = "5.5px"; document.getElementById("add-parts-model-footer").innerHTML = "No Records to Display"; } } ; });  });'
				)

				dbl_clk_function = (
					'$("'
					+ str(table_ids)
					+ '").on("all.bs.table", function (e, name, args) { console.log("popu_upid ============>"); $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); var count = 0; var selectAll = false; $("#add-offerings").css("display","none"); $("#parts-addnew-model").find(\'[type="checkbox"]:checked\').map(function () {var sel_val = $(this).closest("tr").find("td:nth-child(2)").text(); count = 1; console.log("popu_upid3333 ============>"+$(this).attr("name")); if ($(this).attr("name") == "btSelectAll"){console.log("popu_up1111 ============>"); var selectAll = true; $("#add-offerings").css("display","block");} else if (sel_val != "") {console.log("popu_up222 ============>"); $("#add-offerings").css("display","block");} else{$("#add-offerings").css("display","none");}});if(count == 0){$("#add-offerings").css("display","none");}}); $(".bs-checkbox input").addClass("custom"); $("'
					+ str(table_ids)
					+ "\").on('sort.bs.table', function (e, name, order) { console.log('sort.bs.table ============>', e); e.stopPropagation(); currenttab = $(\"ul#carttabs_head .active\").text().trim(); localStorage.setItem('"
					+ str(table_id)
					+ "_SortColumn', name); localStorage.setItem('"
					+ str(table_id)
					+ "_SortColumnOrder', order); ATTRIBUTE_VALUEList = []; "+str(values_lists)+" AddNewContainerSorting(name, order, '"
					+ str(table_id)
					+ "',"+str(a_test)+",ATTRIBUTE_VALUEList,'"+str(TABLEID)+"','"+str(RECORDID)+"','"+str(RECORDFEILD)+"'); }); "
					)
				

			pagination_condition = "OFFSET {Offset_Skip_Count} ROWS FETCH NEXT {Fetch_Count} ROWS ONLY".format(
				Offset_Skip_Count=offset_skip_count, Fetch_Count=fetch_count
			)
			TreeParam = Product.GetGlobal("TreeParam")
			inner_join = "INNER JOIN MAMSOP (NOLOCK)  on MAMTRL.SAP_PART_NUMBER = MAMSOP.SAP_PART_NUMBER AND MAMTRL.MATERIAL_RECORD_ID = MAMSOP.MATERIAL_RECORD_ID "
			additional_where = ""
			if where_string and 'SAP_PART_NUMBER' in where_string:
				where_string = where_string.replace("SAP_PART_NUMBER", "MAMTRL.SAP_PART_NUMBER")
			#Trace.Write('where_string--3680---'+str(where_string))
			if str(PerPage) == "" and str(PageInform) == "":
				Page_start = 1
				Page_End = fetch_count
				PerPage = fetch_count
				PageInform = "1___"+str(fetch_count)+"___"+str(fetch_count)
			else:
				Page_start = int(PageInform.split("___")[0])
				Page_End = int(PageInform.split("___")[1])
				PerPage = PerPage

			order_by = iclusions_val = ""
			if SortColumn != '' and SortColumnOrder !='':
				order_by = "order by "+SortColumn + " " + SortColumnOrder
			else:
				order_by = "order by MAMTRL.SAP_PART_NUMBER ASC"

			pop_val = {}
			
			if where_string:
				where_string += " AND"
			ordered_keys = [
				"MATERIAL_RECORD_ID",
				"SAP_PART_NUMBER",
				"SAP_DESCRIPTION",
				"MATPRIGRP_ID"
				]
			ordered_keys_mam = [
				"MAMTRL.MATERIAL_RECORD_ID",
				"MAMTRL.SAP_PART_NUMBER",
				"MAMTRL.SAP_DESCRIPTION",
				"MAMSOP.MATPRIGRP_ID"
				]
			#get consumable and non consumable values from XML start
			get_salesval  = Sql.GetFirst("select SALESORG_ID from SAQTRV(NOLOCK) where QUOTE_RECORD_ID = '"+str(contract_quote_record_id)+"'")
			iclusions_val_list = []
			TreeSuperParentParam = Product.GetGlobal("TreeParentLevel1")
			TreeTopSuperParentParam = Product.GetGlobal("TreeParentLevel2")
			if str(popup_obj)=="SAQRSP":
				if TreeSuperParentParam == "Product Offerings":
					TreeParam = TreeParam
					TableName = "SAQTSE"
					entitlement_obj = Sql.GetFirst("select replace(ENTITLEMENT_XML,'&',';#38') as ENTITLEMENT_XML from {} (nolock) where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' and SERVICE_ID = '{}' ".format(TableName,contract_quote_record_id,quote_revision_record_id,TreeParam))
				else:
					Service_Id = Product.GetGlobal("TreeParentLevel0")
					TableName = "SAQSGE"
					entitlement_obj = Sql.GetFirst("select replace(ENTITLEMENT_XML,'&',';#38') as ENTITLEMENT_XML from {} (nolock) where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' and SERVICE_ID = '{}'AND GREENBOOK  = '{}'".format(TableName,contract_quote_record_id,quote_revision_record_id,Service_Id,TreeParam))
				
				entitlement_xml = entitlement_obj.ENTITLEMENT_XML
				import re
				flag=0
				iclusions_val_list = []
				quote_item_tag = re.compile(r'(<QUOTE_ITEM_ENTITLEMENT>[\w\W]*?</QUOTE_ITEM_ENTITLEMENT>)')
				pattern_non_consumable = re.compile(r'<ENTITLEMENT_ID>(?:AGS_[^>]*?_TSC_NONCNS|AGS_[^>]*?_NON_CONSUMABLE)</ENTITLEMENT_ID>')
				pattern_consumable = re.compile(r'<ENTITLEMENT_ID>AGS_[^>]*?_TSC_CONSUM</ENTITLEMENT_ID>')
				pattern_new_parts_only = re.compile(r'<ENTITLEMENT_ID>AGS_[^>]*?_TSC_RPPNNW</ENTITLEMENT_ID>')
				pattern_exclusion_or_inclusion = re.compile(r'<ENTITLEMENT_DISPLAY_VALUE>(?:Some Exclusions|Some Inclusions)</ENTITLEMENT_DISPLAY_VALUE>')
				pattern_new_parts_only_yes = re.compile(r'<ENTITLEMENT_DISPLAY_VALUE>Yes</ENTITLEMENT_DISPLAY_VALUE>')
				new_parts_yes = ""
				for m in re.finditer(quote_item_tag, entitlement_xml):
					sub_string = m.group(1)
					non_consumable =re.findall(pattern_non_consumable,sub_string)
					consumable =re.findall(pattern_consumable,sub_string)
					exclusion_or_inclusion =re.findall(pattern_exclusion_or_inclusion,sub_string)
					new_parts_only = re.findall(pattern_new_parts_only,sub_string)
					new_parts_only_value = re.findall(pattern_new_parts_only_yes,sub_string)
					if new_parts_only and new_parts_only_value:
						new_parts_yes = "Yes"
						break
					if non_consumable and exclusion_or_inclusion:
						iclusions_val_list.append('N')
					if consumable and exclusion_or_inclusion:
						iclusions_val_list.append('C')
				if new_parts_yes == "Yes":
					where_string += """ MAMTRL.IS_SPARE_PART = 'True' AND  MAMSOP.SALESORG_ID = '{sales}' AND MAMTRL.PRODUCT_TYPE IS NULL AND NOT EXISTS (SELECT PART_NUMBER FROM SAQRSP (NOLOCK) WHERE QUOTE_RECORD_ID = '{qt_rec_id}' AND QTEREV_RECORD_ID ='{qt_rev_id}' and MAMTRL.SAP_PART_NUMBER = SAQRSP.PART_NUMBER)""".format(sales = get_salesval.SALESORG_ID,qt_rec_id = contract_quote_record_id,qt_rev_id = quote_revision_record_id)
					where_string_1 += """ MAMTRL.SAP_PART_NUMBER IN (SELECT SAP_PART_NUMBER FROM MAMSOP WHERE  MAMSOP.SALESORG_ID = '{sales}' )AND MAMTRL.IS_SPARE_PART = 'True' AND MAMTRL.PRODUCT_TYPE IS NULL AND NOT EXISTS (SELECT PART_NUMBER FROM SAQRSP (NOLOCK) WHERE QUOTE_RECORD_ID = '{qt_rec_id}' AND QTEREV_RECORD_ID ='{qt_rev_id}' and MAMTRL.SAP_PART_NUMBER = SAQRSP.PART_NUMBER)""".format(sales = get_salesval.SALESORG_ID,qt_rec_id = contract_quote_record_id,qt_rev_id = quote_revision_record_id)
				else:
					iclusions_val = str(tuple(iclusions_val_list)).replace(',)',')')
					where_string += """ MAMTRL.IS_SPARE_PART = 'True' AND MAMSOP.MATPRIGRP_ID in {iclusions_val} and MAMSOP.SALESORG_ID = '{sales}' AND MAMTRL.PRODUCT_TYPE IS NULL AND NOT EXISTS (SELECT PART_NUMBER FROM SAQRSP (NOLOCK) WHERE QUOTE_RECORD_ID = '{qt_rec_id}' AND QTEREV_RECORD_ID ='{qt_rev_id}' and MAMTRL.SAP_PART_NUMBER = SAQRSP.PART_NUMBER)""".format(sales = get_salesval.SALESORG_ID,qt_rec_id = contract_quote_record_id,qt_rev_id = quote_revision_record_id,iclusions_val = iclusions_val)
					where_string_1 += """ MAMTRL.SAP_PART_NUMBER IN (SELECT SAP_PART_NUMBER FROM MAMSOP WHERE MAMSOP.MATPRIGRP_ID in {iclusions_val} and MAMSOP.SALESORG_ID = '{sales}' )AND MAMTRL.IS_SPARE_PART = 'True' AND MAMTRL.PRODUCT_TYPE IS NULL AND NOT EXISTS (SELECT PART_NUMBER FROM SAQRSP (NOLOCK) WHERE QUOTE_RECORD_ID = '{qt_rec_id}' AND QTEREV_RECORD_ID ='{qt_rev_id}' and MAMTRL.SAP_PART_NUMBER = SAQRSP.PART_NUMBER)""".format(sales = get_salesval.SALESORG_ID,qt_rec_id = contract_quote_record_id,qt_rev_id = quote_revision_record_id,iclusions_val = iclusions_val)
				Pagination_M = Sql.GetFirst(
					"SELECT COUNT({}.CpqTableEntryId) as count FROM {} (NOLOCK) WHERE {} {}".format(
						ObjectName,ObjectName,str(where_string_1) if where_string_1 else "",additional_where
					)
				)
			
			elif str(popup_obj)=="SAQSPT":
				where_string += """ MAMTRL.IS_SPARE_PART = 'True' AND MAMSOP.SALESORG_ID = '{sales}' AND MAMTRL.PRODUCT_TYPE IS NULL AND NOT EXISTS (SELECT PART_NUMBER FROM SAQSPT (NOLOCK) WHERE QUOTE_RECORD_ID = '{qt_rec_id}' AND QTEREV_RECORD_ID ='{qt_rev_id}' and MAMTRL.SAP_PART_NUMBER = SAQSPT.PART_NUMBER)""".format(sales = get_salesval.SALESORG_ID,qt_rec_id = contract_quote_record_id,qt_rev_id = quote_revision_record_id)
				where_string_1 += """ MAMTRL.SAP_PART_NUMBER IN (SELECT SAP_PART_NUMBER FROM MAMSOP WHERE  MAMSOP.SALESORG_ID = '{sales}' )AND MAMTRL.IS_SPARE_PART = 'True' AND MAMTRL.PRODUCT_TYPE IS NULL AND NOT EXISTS (SELECT PART_NUMBER FROM SAQRSP (NOLOCK) WHERE QUOTE_RECORD_ID = '{qt_rec_id}' AND QTEREV_RECORD_ID ='{qt_rev_id}' and MAMTRL.SAP_PART_NUMBER = SAQRSP.PART_NUMBER)""".format(sales = get_salesval.SALESORG_ID,qt_rec_id = contract_quote_record_id,qt_rev_id = quote_revision_record_id)
				Pagination_M = Sql.GetFirst(
					"SELECT COUNT({}.CpqTableEntryId) as count FROM {} (NOLOCK) WHERE {} {}".format(
						ObjectName,ObjectName,str(where_string_1) if where_string_1 else "",additional_where
					)
				)
			
			table_data = Sql.GetList(
				"select {} from {} (NOLOCK) {} {} {} {} {}".format(
					", ".join(ordered_keys_mam),
					ObjectName
					,inner_join if inner_join else "",
					"WHERE " + where_string if where_string else "" ,
					additional_where,
					order_by,pagination_condition
				)
			)
			Pagination_M = Sql.GetFirst(
					"SELECT COUNT({}.CpqTableEntryId) as count FROM {} (NOLOCK) WHERE {} {}".format(
						ObjectName,ObjectName,str(where_string_1) if where_string_1 else "",additional_where
					)
				)
			# QueryCountObj = Sql.GetFirst(
			# 		"select count(*) as cnt from {} (NOLOCK) {} {} ".format(
			# 		ObjectName,
			# 		"WHERE " + where_string_1 if where_string_1 else "",
			# 		additional_where
			# 	)
			# 	)
			#if QueryCountObj is not None:
			QryCount = Pagination_M.count

			if table_data is not None:
				for row_data in table_data:
					data_id = str(ObjectName)
					new_value_dict = {}
					for data in row_data:
						if str(data.Key) == "MATERIAL_RECORD_ID":
							pop_val = str(data.Value) + "|Parts"
							cpqidval = CPQID.KeyCPQId.GetCPQId(ObjectName, str(data.Value))
							new_value_dict[data.Key] = cpqidval
						else:
							new_value_dict[data.Key] = data.Value
						new_value_dict["pop_val"] = pop_val
					date_field.append(new_value_dict)
			QueryCount = len(date_field)

			pagination_total_count = 0
			if Pagination_M is not None:
				pagination_total_count = QryCount
			if offset_skip_count == 0:
				offset_skip_count = 1
				records_end = fetch_count
				disable_previous_and_first = "class='btn-is-disabled' style=\'pointer-events:none\' "
			Trace.Write('offset cnt-->'+str(offset_skip_count))
			if offset_skip_count%10==0:
				offset_skip_count+=1
			records_end = offset_skip_count + fetch_count - 1
			records_end = pagination_total_count if pagination_total_count < records_end else records_end
			if pagination_total_count==0:
				offset_skip_count=0
			records_start_and_end = "{} - {} of ".format(offset_skip_count, records_end)
			disable_next_and_last = ""
			disable_previous_and_first = ""
			if records_end == pagination_total_count:
				disable_next_and_last = "class='btn-is-disabled' style=\'pointer-events:none\' "
			current_page = int(math.ceil(offset_skip_count / fetch_count)) + 1

			Product.SetGlobal("QueryCount", str(QueryCount))
			pagination_table_id = "pagination_{}".format(table_id)
			Trace.Write('rec start end-->'+str(records_start_and_end))
			var_str = """<div id="{Parent_Div_Id}" class="col-md-12 brdr listContStyle padbthgt30">
								<div class="col-md-4 pager-numberofitem  clear-padding">
									<span class="pager-number-of-items-item flt_lt_pad2_mar2022" id="RecordsStartAndEnd">{Records_Start_And_End}</span>
									<span class="pager-number-of-items-item flt_lt_pad2_mar" id="TotalRecordsCount">{Pagination_Total_Count}</span>
									<div class="clear-padding fltltmrgtp3">
										<div class="pull-right vralign">
											<select onchange="ShowResultCountFunc(this, '{ShowResultCountFuncTb}', 'addParts', '{TableId}')" id="ShowResultCount" class="form-control selcwdt">
												<option value="10" {Selected_10}>10</option>
												<option value="20" {Selected_20}>20</option>
												<option value="50" {Selected_50}>50</option>
												<option value="100" {Selected_100}>100</option>
												<option value="200" {Selected_200}>200</option>
											</select> 
										</div>
									</div>
								</div>
								<div class="col-xs-8 col-md-4  clear-padding inpadtex" data-bind="visible: totalItemCount">
									<div class="clear-padding col-xs-12 col-sm-6 col-md-12 brd0">
										<ul class="pagination pagination">
											<li class="disabled">
												<a onclick="GetFirstResultFunc('{GetFirstResultFuncTb}', 'addParts', '{TableId}')" {Disable_First}><i class="fa fa-caret-left fnt14bold"></i><i class="fa fa-caret-left fnt14"></i></a>
											</li>
											<li class="disabled"><a onclick="GetPreviuosResultFunc('{GetPreviuosResultFuncTb}', 'addParts', '{TableId}')" {Disable_Previous}><i class="fa fa-caret-left fnt14"></i>PREVIOUS</a></li>
											<li class="disabled"><a onclick="GetNextResultFunc('{GetNextResultFuncTb}', 'addParts', '{TableId}')" {Disable_Next}>NEXT<i class="fa fa-caret-right fnt14"></i></a></li>
											<li class="disabled"><a onclick="GetLastResultFunc('{GetLastResultFuncTb}', 'addParts', '{TableId}')" {Disable_Last}><i class="fa fa-caret-right fnt14"></i><i class="fa fa-caret-right fnt14bold"></i></a></li>
										</ul>
									</div> 
								</div> 
								<div class="col-md-4 pad3"> 
									<span id="page_count" class="currentPage page_right_content">{Current_Page}</span>
									<span class="page_right_content padrt2">Page </span>
								</div>
							</div>""".format(
				Parent_Div_Id=pagination_table_id,
				Records_Start_And_End=records_start_and_end,
				Pagination_Total_Count=pagination_total_count,
				ShowResultCountFuncTb=pagination_table_id,
				Selected_10="selected" if fetch_count == 10 else "",
				Selected_20="selected" if fetch_count == 20 else "",
				Selected_50="selected" if fetch_count == 50 else "",
				Selected_100="selected" if fetch_count == 100 else "",
				Selected_200="selected" if fetch_count == 200 else "",
				GetFirstResultFuncTb=pagination_table_id,
				Disable_First=disable_previous_and_first,
				GetPreviuosResultFuncTb=pagination_table_id,
				Disable_Previous=disable_previous_and_first,
				GetNextResultFuncTb=pagination_table_id,
				Disable_Next=disable_next_and_last,
				GetLastResultFuncTb=pagination_table_id,
				Disable_Last=disable_next_and_last,
				Current_Page=current_page,
				TableId=TABLEID,
			)

			table_ids = "#" + str(table_id)
			# Filter based on table MultiSelect Dropdown column - Start

			for index, col_name in enumerate(ordered_keys):
				table, api_name = ObjectName, col_name
				obj_data = Sql.GetFirst(
					"SELECT API_NAME, DATA_TYPE, PICKLIST FROM  SYOBJD WHERE OBJECT_NAME='"
					+ str(table)
					+ "' and API_NAME = '"
					+ str(api_name)
					+ "'"
				)
				if obj_data is not None:
					if str(obj_data.PICKLIST).upper() == "TRUE":
						filter_tag = (
							'<div id = "'
							+ str(table_id)
							+ "_RelatedMutipleCheckBoxDrop_"
							+ str(index)
							+ '" class="form-control bootstrap-table-filter-control-'
							+ str(api_name)
							+ " RelatedMutipleCheckBoxDrop_"
							+ str(index)
							+ ' "></div>'
						)
						filter_tags.append(filter_tag)
						filter_types.append("select")
						if obj_data.DATA_TYPE == "CHECKBOX":
							filter_values.append(["True", "False"])
						else:
							data_obj = Sql.GetList(
								"SELECT DISTINCT {Column} FROM {Table} ".format(Column=api_name, Table=table)
							)
							if data_obj is not None:
								filter_values.append([row_data.Value for data in data_obj for row_data in data])
					else:
						filter_tag = (
							'<input type="text" class="form-control wth100visble bootstrap-table-filter-control-'
							+ str(api_name)
							+ '">'
						)
						filter_tags.append(filter_tag)
						filter_types.append("input")
						filter_values.append("")

			filter_drop_down = (
				"try { if( document.getElementById('"
				+ str(table_id)
				+ "') ) { var listws = document.getElementById('"
				+ str(table_id)
				+ "').getElementsByClassName('filter-control');  for (i = 0; i < listws.length; i++) { document.getElementById('"
				+ str(table_id)
				+ "').getElementsByClassName('filter-control')[i].innerHTML = data6[i];  } for (j = 0; j < listws.length; j++) { if (data10[j] == 'select') { var dataAdapter = new $.jqx.dataAdapter(data8[j]); if(data11[j].length>5){ $('#"
				+ str(table_id)
				+ "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter}); }else{$('#"
				+ str(table_id)
				+ "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter ,autoDropDownHeight: true});} } } } }  catch(err) { setTimeout(function() { var listws = document.getElementById('"
				+ str(table_id)
				+ "').getElementsByClassName('filter-control');  for (i = 0; i < listws.length; i++) { document.getElementById('"
				+ str(table_id)
				+ "').getElementsByClassName('filter-control')[i].innerHTML = data9[i];  } for (j = 0; j < listws.length; j++) { if (data10[j] == 'select') { var dataAdapter = new $.jqx.dataAdapter(data11[j]); $('#"
				+ str(table_id)
				+ "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter, scrollBarSize :10 }); } } }, 5000); }"
			)
			dbl_clk_function += (
				'$("'
				+ str(table_ids)
				+ '").on("all.bs.table", function (e, name, args) { $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); }); $("'
				+ str(table_ids)
				+ '\ th.bs-checkbox div.th-inner").before("<div class=\'pad0brdbt\'>SELECT</div>"); $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>");'
			) 

			pagedata = ""
			if QryCount==0:
				pagedata = str(QryCount) + " - " + str(QryCount) + " of "
			elif QryCount < int(PerPage):
				pagedata = str(Page_start) + " - " + str(QryCount) + " of "
			else:
				pagedata = str(Page_start) + " - " + str(Page_End)+ " of "
		elif str(ObjectName) =="SAQDLT" and str(CurrentTab) == "Quotes" and ACTION == "REPLACE":
			Trace.Write('In SAQDLT')
			where_string = ""
			TreeParam = Product.GetGlobal("TreeParam")
			
			if A_Keys != "" and A_Values != "":
				A_Keys = list(A_Keys)
				A_Values = list(A_Values)
				for key, value in zip(A_Keys, A_Values):
					if value.strip():
						if where_string:
							where_string += " AND "
						where_string += "{Key} LIKE '%{Value}%'".format(Key=key, Value=value)
			DIVNAME = "VIEW_DIV_ID"
			new_value_dict = {}
			ObjectName = "SAEMPL"
			table_id = "contact_manager_addnew_model"
			Header_details = {
				"EMPLOYEE_RECORD_ID": "KEY",
				"EMPLOYEE_ID": "EMPLOYEE ID",
				"EMPLOYEE_NAME": "EMPLOYEE NAME",
				"EMAIL": "EMAIL",
				"PHONE":"PHONE",
			}
			ordered_keys = [
				"EMPLOYEE_RECORD_ID",
				"EMPLOYEE_ID",
				"EMPLOYEE_NAME",
				"EMAIL",
				"PHONE",
			]
			Objd_Obj = Sql.GetList(
				"select FIELD_LABEL,API_NAME,LOOKUP_OBJECT,LOOKUP_API_NAME,DATA_TYPE,FORMULA_DATA_TYPE from SYOBJD (NOLOCK)where OBJECT_NAME = '"
				+ str(ObjectName)
				+ "'"
			)
			lookup_disply_list = []
			if Objd_Obj is not None:
				attr_list = {}
				api_names = [inn.API_NAME for inn in Objd_Obj]
				for attr in Objd_Obj:
					attr_list[str(attr.API_NAME)] = str(attr.FIELD_LABEL)
					if str(attr.LOOKUP_API_NAME) != "" and str(attr.LOOKUP_API_NAME) is not None:
						lookup_disply_list.append(str(attr.API_NAME))
				checkbox_list = [
					inn.API_NAME for inn in Objd_Obj if (inn.DATA_TYPE == "CHECKBOX" or inn.FORMULA_DATA_TYPE == "CHECKBOX")
				]
				lookup_list = {ins.LOOKUP_API_NAME: ins.API_NAME for ins in Objd_Obj}
				sec_str = '<div class="row modulebnr brdr ma_mar_btm">REPLACE CONTRACT MANAGER<button type="button" id = "contract_replace" class="close flt_rt" onclick="closepopup_scrl(this)" data-dismiss="modal">X</button></div>'
				sec_str += '<div class="col-md-12 padlftrhtnone"><div class="row pad-10 bg-lt-wt brdr"> <img style="height: 40px; margin-top: -1px; margin-left: -1px; float: left;" src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/customer_info_icon.svg"/><div class="product_txt_div_child secondary_highlight" style="display: block;text-align: left;"><div class="product_txt_child"><abbr title="Key">Contacts</abbr></div><div class="product_txt_to_top_child"><abbr title="ALL">Select a valid Contract manager record below to replace it to the list of Contracts associated with your Quote</abbr></div></div></div></div>'

			sec_str += '<div id="container" class="g4 pad-10 brdr except_sec">'
			sec_str += ('<table id="'+str(table_id)+ '" data-escape="true"  data-search-on-enter-key="true" data-show-header="true"  data-filter-control="true"> <thead><tr>')
			#sec_str += '<th data-field="SELECT" class="wth45" data-checkbox="true" id ="check_boxval" onchange = "get_checkedval()"><div class="action_col">SELECT</div></th>'

			for key, invs in enumerate(list(ordered_keys)):

				invs = str(invs).strip()
				qstring = Header_details.get(str(invs)) or ""
				if key == 0:
					sec_str += (
						'<th data-field="'
						+ str(invs)
						+ '" data-formatter="contactreplaceKeyHyperLink" data-sortable="true" data-title-tooltip="'
						+ str(qstring)
						+ '" data-filter-control="input">'
						+ str(qstring)
						+ "</th>"
					)
				else:
					sec_str += (
						'<th data-field="'
						+ invs
						+ '" data-title-tooltip="'
						+ str(qstring)
						+ '" data-sortable="true" data-filter-control="input">'
						+ str(qstring)
						+ "</th>"
					)
			sec_str += '</tr></thead><tbody class ="equipments_id" ></tbody></table>'
			sec_str += '<div id="contact_replace_addnew_model_footer"></div>'
			values_list = ""
			values_lists = ""
			a_test = []
			for invsk in list(Header_details):
				table_ids = "#" + str(table_id)
				filter_class = table_ids + " .bootstrap-table-filter-control-" + str(invsk)
				values_lists += "var " + str(invsk) + ' = $("' + str(filter_class) + '").val(); '
				values_lists += " ATTRIBUTE_VALUEList.push(" + str(invsk) + "); "
				a_test.append(invsk)
				filter_control_function += (
					'$("'
					+ filter_class
					+ '").change( function(){ var table_id = $(this).closest("table").attr("id"); var a_list = '
					+ str(a_test)
					+ "; ATTRIBUTE_VALUEList = []; "
					+ str(values_lists)
					+ ' SortColumn = localStorage.getItem("SortColumn"); SortColumnOrder = localStorage.getItem("SortColumnOrder"); PerPage = $("#PageCountValue").val(); PageInform = "1___" + PerPage + "___" + PerPage; cpq.server.executeScript("SYUADNWPOP", {\'TABLEID\': "'
					+ str(TABLEID)
					+ "\", 'OPER': 'NO', 'RECORDID': \""
					+ str(RECORDID)
					+ "\", 'RECORDFEILD':  \""
					+ str(RECORDFEILD)
					+ "\", 'NEWVALUE': '', 'LOOKUPOBJ': '', 'LOOKUPAPI': '','A_Keys':a_list,'A_Values':ATTRIBUTE_VALUEList,'ACTION':'REPLACE'}, function(data) {  date_field = data[3]; var assoc = data[1]; var api_name = data[2];data4 = data[4];data5 = data[5]; try { if(date_field.length > 0) { $(\""
					+ str(table_ids)
					+ '").bootstrapTable("load", date_field  ); $("button#country_save").attr("disabled",false); $("#noRecDisp").remove() } else{ var date_field = [];$("'
					+ str(table_ids)
					+ '").bootstrapTable("load", date_field  ); $("button#country_save").attr("disabled",true); $("#contact_manager_addnew_model").after("<div id=\'noRecDisp\' class=\'noRecord\'>No Records to Display</div>"); $(".noRecord:not(:first)").remove(); } } catch(err) { if(date_field.length > 0) { $("'
					+ str(table_ids)
					+ '").bootstrapTable("load", date_field  ); $("button#country_save").attr("disabled",false); } else{ $("'
					+ str(table_ids)
					+ '").bootstrapTable("load", date_field  ); $("button#country_save").attr("disabled",true); } } ; });  });'
				)
			pagination_condition = "OFFSET {Offset_Skip_Count} ROWS FETCH NEXT {Fetch_Count} ROWS ONLY".format(
				Offset_Skip_Count=offset_skip_count-1 if offset_skip_count%10==1 else offset_skip_count, Fetch_Count=fetch_count
			)
			Pagination_M = SqlHelper.GetFirst("""select count(SAEMPL.CpqTableEntryId) as count from SAEMPL (NOLOCK) WHERE SAEMPL.EMPLOYEE_RECORD_ID  NOT IN (SELECT MEMBER_RECORD_ID FROM SAQDLT (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}')""".format(contract_quote_record_id,quote_revision_record_id))

			order_by = "order by SAEMPL.EMPLOYEE_ID ASC"

			if str(PerPage) == "" and str(PageInform) == "":
				Page_start = 1
				Page_End = fetch_count
				PerPage = fetch_count
				PageInform = "1___"+str(fetch_count)+"___"+str(fetch_count)
			else:
				Page_start = int(PageInform.split("___")[0])
				Page_End = int(PageInform.split("___")[1])
				PerPage = PerPage

			order_by = ""
			if SortColumn != '' and SortColumnOrder !='':
				order_by = "order by "+SortColumn + " " + SortColumnOrder
			else:
				order_by = "order by EMPLOYEE_ID ASC"

			pop_val = {}
			if where_string:
				where_string += " AND"
				Trace.Write("soureceequipments "+str(where_string))
			if TreeParam == "Sales Team":
				where_string += """ SAEMPL.EMPLOYEE_RECORD_ID NOT IN (SELECT MEMBER_RECORD_ID FROM SAQDLT (NOLOCK) where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}')""".format(contract_quote_record_id,quote_revision_record_id)
			
			table_data = Sql.GetList("Select {} FROM SAEMPL {} {} {}".format(", ".join(ordered_keys),"WHERE " +where_string if where_string else "",order_by,pagination_condition))
			QueryCountObj = Sql.GetFirst(
				"select count(*) as cnt from SAEMPL (NOLOCK) {}".format(
				"WHERE " +where_string if where_string else ""
				)
			)
			if QueryCountObj is not None:
				QryCount = QueryCountObj.cnt


			if table_data is not None :
				for row_data in table_data:
					data_id = str(ObjectName)

					new_value_dict = {}

					for data in row_data:
						if str(data.Key) == "EMPLOYEE_RECORD_ID":
							pop_val = str(data.Value)
							cpqidval = CPQID.KeyCPQId.GetCPQId(ObjectName, str(data.Value))
							new_value_dict[data.Key] = cpqidval
						else:
							new_value_dict[data.Key] = data.Value
						new_value_dict["pop_val"] = pop_val
					date_field.append(new_value_dict)
			QueryCount = len(date_field)

			pagination_total_count = 0
			if Pagination_M is not None:
				pagination_total_count = Pagination_M.count
			if offset_skip_count == 0:
				offset_skip_count = 1
				records_end = fetch_count
			records_end = offset_skip_count + fetch_count - 1
			records_end = pagination_total_count if pagination_total_count < records_end else records_end
			records_start_and_end = "{} - {} of ".format(offset_skip_count, records_end)
			disable_next_and_last = ""
			disable_previous_and_first = ""
			if records_end == pagination_total_count:
				disable_next_and_last = "class='btn-is-disabled' style=\'pointer-events:none\' "
			if offset_skip_count == 0:
				disable_previous_and_first = "class='btn-is-disabled' style=\'pointer-events:none\' "
			current_page = int(math.ceil(offset_skip_count / fetch_count)) + 1

			Product.SetGlobal("QueryCount", str(QueryCount))
			pagination_table_id = "pagination_{}".format(table_id)
			if QueryCount != 0:
				var_str = """<div id="{Parent_Div_Id}" class="col-md-12 brdr listContStyle padbthgt30">
									<div class="col-md-4 pager-numberofitem  clear-padding">
										<span class="pager-number-of-items-item flt_lt_pad2_mar2022" id="RecordsStartAndEnd">{Records_Start_And_End}</span>
										<span class="pager-number-of-items-item flt_lt_pad2_mar" id="TotalRecordsCount">{Pagination_Total_Count}</span>
										<div class="clear-padding fltltmrgtp3">
											<div class="pull-right vralign">
												<select onchange="ShowResultCountFunc(this, '{ShowResultCountFuncTb}', 'addEquipment', '{TableId}')" id="ShowResultCount" class="form-control selcwdt">
													<option value="10" {Selected_10}>10</option>
													<option value="20" {Selected_20}>20</option>
													<option value="50" {Selected_50}>50</option>
													<option value="100" {Selected_100}>100</option>
													<option value="200" {Selected_200}>200</option>
												</select> 
											</div>
										</div>
									</div>
									<div class="col-xs-8 col-md-4  clear-padding inpadtex" data-bind="visible: totalItemCount">
										<div class="clear-padding col-xs-12 col-sm-6 col-md-12 brd0">
											<ul class="pagination pagination">
												<li class="disabled">
													<a onclick="GetFirstResultFunc('{GetFirstResultFuncTb}', 'addEquipment', '{TableId}')" {Disable_First}><i class="fa fa-caret-left fnt14bold"></i><i class="fa fa-caret-left fnt14"></i></a>
												</li>
												<li class="disabled"><a onclick="GetPreviuosResultFunc('{GetPreviuosResultFuncTb}', 'addEquipment', '{TableId}')" {Disable_Previous}><i class="fa fa-caret-left fnt14"></i>PREVIOUS</a></li>
												<li class="disabled"><a onclick="GetNextResultFunc('{GetNextResultFuncTb}', 'addEquipment', '{TableId}')" {Disable_Next}>NEXT<i class="fa fa-caret-right fnt14"></i></a></li>
												<li class="disabled"><a onclick="GetLastResultFunc('{GetLastResultFuncTb}', 'addEquipment', '{TableId}')" {Disable_Last}><i class="fa fa-caret-right fnt14"></i><i class="fa fa-caret-right fnt14bold"></i></a></li>
											</ul>
										</div> 
									</div> 
									<div class="col-md-4 pad3"> 
										<span id="page_count" class="currentPage page_right_content">{Current_Page}</span>
										<span class="page_right_content padrt2">Page </span>
									</div>
								</div>""".format(
					Parent_Div_Id=pagination_table_id,
					Records_Start_And_End=records_start_and_end,
					Pagination_Total_Count=pagination_total_count,
					ShowResultCountFuncTb=pagination_table_id,
					Selected_10="selected" if fetch_count == 10 else "",
					Selected_20="selected" if fetch_count == 20 else "",
					Selected_50="selected" if fetch_count == 50 else "",
					Selected_100="selected" if fetch_count == 100 else "",
					Selected_200="selected" if fetch_count == 200 else "",
					GetFirstResultFuncTb=pagination_table_id,
					Disable_First=disable_previous_and_first,
					GetPreviuosResultFuncTb=pagination_table_id,
					Disable_Previous=disable_previous_and_first,
					GetNextResultFuncTb=pagination_table_id,
					Disable_Next=disable_next_and_last,
					GetLastResultFuncTb=pagination_table_id,
					Disable_Last=disable_next_and_last,
					Current_Page=current_page,
					TableId=TABLEID,
				)
			else:
				date_field = "NORECORDS"
				Trace.Write("No Equipment Records")
			table_ids = "#" + str(table_id)
			# Filter based on table MultiSelect Dropdown column - Start

			for index, col_name in enumerate(ordered_keys):
				table, api_name = ObjectName, col_name
				obj_data = Sql.GetFirst(
					"SELECT API_NAME, DATA_TYPE, PICKLIST FROM  SYOBJD WHERE OBJECT_NAME='"
					+ str(table)
					+ "' and API_NAME = '"
					+ str(api_name)
					+ "'"
				)
				if obj_data is not None:
					if str(obj_data.PICKLIST).upper() == "TRUE":
						filter_tag = (
							'<div id = "'
							+ str(table_id)
							+ "_RelatedMutipleCheckBoxDrop_"
							+ str(index)
							+ '" class="form-control bootstrap-table-filter-control-'
							+ str(api_name)
							+ " RelatedMutipleCheckBoxDrop_"
							+ str(index)
							+ ' "></div>'
						)
						filter_tags.append(filter_tag)
						filter_types.append("select")
						if obj_data.DATA_TYPE == "CHECKBOX":
							filter_values.append(["True", "False"])
						else:
							# Trace.Write("=============$$$$$$$$$$$$$>>>>>>>>>>>>> "+"SELECT DISTINCT {Column} FROM {Table}".format(Column=api_name, Table=table))
							data_obj = Sql.GetList(
								"SELECT DISTINCT {Column} FROM {Table}".format(Column=api_name, Table=table)
							)
							if data_obj is not None:
								filter_values.append([row_data.Value for data in data_obj for row_data in data])
					else:
						filter_tag = (
							'<input type="text" class="form-control wth100visble bootstrap-table-filter-control-'
							+ str(api_name)
							+ '">'
						)
						filter_tags.append(filter_tag)
						filter_types.append("input")
						filter_values.append("")

			filter_drop_down = (
				"try { if( document.getElementById('"
				+ str(table_id)
				+ "') ) { var listws = document.getElementById('"
				+ str(table_id)
				+ "').getElementsByClassName('filter-control');  for (i = 0; i < listws.length; i++) { document.getElementById('"
				+ str(table_id)
				+ "').getElementsByClassName('filter-control')[i].innerHTML = data6[i];  } for (j = 0; j < listws.length; j++) { if (data10[j] == 'select') { var dataAdapter = new $.jqx.dataAdapter(data8[j]); if(data11[j].length>5){ $('#"
				+ str(table_id)
				+ "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter}); }else{$('#"
				+ str(table_id)
				+ "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter ,autoDropDownHeight: true});} } } } }  catch(err) { setTimeout(function() { var listws = document.getElementById('"
				+ str(table_id)
				+ "').getElementsByClassName('filter-control');  for (i = 0; i < listws.length; i++) { document.getElementById('"
				+ str(table_id)
				+ "').getElementsByClassName('filter-control')[i].innerHTML = data9[i];  } for (j = 0; j < listws.length; j++) { if (data10[j] == 'select') { var dataAdapter = new $.jqx.dataAdapter(data11[j]); $('#"
				+ str(table_id)
				+ "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter, scrollBarSize :10 }); } } }, 5000); }"
			)
			dbl_clk_function += (
				'$("'
				+ str(table_ids)
				+ '").on("all.bs.table", function (e, name, args) { $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); }); $("'
				+ str(table_ids)
				+ '\ th.bs-checkbox div.th-inner").before("<div class=\'pad0brdbt\'>SELECT</div>"); $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>");'
			)

			pagedata = ""
			if QryCount < int(PerPage):
				pagedata = str(Page_start) + " - " + str(QryCount) + " of "
			else:
				pagedata = str(Page_start) + " - " + str(Page_End)+ " of "


		elif str(ObjectName) =="SAQICT" and str(CurrentTab) == "Quotes":
			Trace.Write('In SAQICT')
			where_string = ""
			TreeParam = Product.GetGlobal("TreeParam")
			
			if A_Keys != "" and A_Values != "":
				A_Keys = list(A_Keys)
				A_Values = list(A_Values)
				for key, value in zip(A_Keys, A_Values):
					if value.strip():
						if where_string:
							where_string += " AND "
						where_string += "{Key} LIKE '%{Value}%'".format(Key=key, Value=value)
			DIVNAME = "VIEW_DIV_ID"
			new_value_dict = {}
			ObjectName = "SACONT"
			table_id = "contact_replace_addnew_model"
			Header_details = {
				"CONTACT_RECORD_ID": "KEY",
				"CONTACT_ID": "CONTACT ID",
				"CONTACT_NAME": "CONTACT NAME",
				"EMAIL": "EMAIL",
				"PHONE":"PHONE",
			}
			ordered_keys = [
				"CONTACT_RECORD_ID",
				"CONTACT_ID",
				"CONTACT_NAME",
				"EMAIL",
				"PHONE",
			]
			Objd_Obj = Sql.GetList(
				"select FIELD_LABEL,API_NAME,LOOKUP_OBJECT,LOOKUP_API_NAME,DATA_TYPE,FORMULA_DATA_TYPE from SYOBJD (NOLOCK)where OBJECT_NAME = '"
				+ str(ObjectName)
				+ "'"
			)
			lookup_disply_list = []
			if Objd_Obj is not None:
				attr_list = {}
				api_names = [inn.API_NAME for inn in Objd_Obj]
				for attr in Objd_Obj:
					attr_list[str(attr.API_NAME)] = str(attr.FIELD_LABEL)
					if str(attr.LOOKUP_API_NAME) != "" and str(attr.LOOKUP_API_NAME) is not None:
						lookup_disply_list.append(str(attr.API_NAME))
				checkbox_list = [
					inn.API_NAME for inn in Objd_Obj if (inn.DATA_TYPE == "CHECKBOX" or inn.FORMULA_DATA_TYPE == "CHECKBOX")
				]
				lookup_list = {ins.LOOKUP_API_NAME: ins.API_NAME for ins in Objd_Obj}
				sec_str = '<div class="row modulebnr brdr ma_mar_btm">ADD CONTACT<button type="button" id = "account_replace" class="close flt_rt" onclick="closepopup_scrl(this)" data-dismiss="modal">X</button></div>'
				sec_str += '<div class="col-md-12 padlftrhtnone"><div class="row pad-10 bg-lt-wt brdr"> <img style="height: 40px; margin-top: -1px; margin-left: -1px; float: left;" src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/customer_info_icon.svg"/><div class="product_txt_div_child secondary_highlight" style="display: block;text-align: left;"><div class="product_txt_child"><abbr title="Key">Contacts</abbr></div><div class="product_txt_to_top_child"><abbr title="ALL">Select a valid Contact record below to add it to the list of Contacts associated with your Quote</abbr></div></div><button type="button" class="btnconfig" data-dismiss="modal" onclick="closepopup_scrl()">CANCEL</button><button type="button" id="add-contacts" class="btnconfig" onclick="addcontacts()" data-dismiss="modal">ADD</button></div></div>'

			sec_str += '<div id="container" class="g4 pad-10 brdr except_sec">'
			sec_str += ('<table id="'+str(table_id)+ '" data-escape="true"  data-search-on-enter-key="true" data-show-header="true"  data-filter-control="true"> <thead><tr>')
			sec_str += '<th data-field="SELECT" class="wth45" data-checkbox="true" id ="check_boxval" onchange = "get_checkedval()"><div class="action_col">SELECT</div></th>'

			for key, invs in enumerate(list(ordered_keys)):

				invs = str(invs).strip()
				qstring = Header_details.get(str(invs)) or ""
				if key == 0:
					sec_str += (
						'<th data-field="'
						+ str(invs)
						+ '" data-formatter="contactreplaceKeyHyperLink" data-sortable="true" data-title-tooltip="'
						+ str(qstring)
						+ '" data-filter-control="input">'
						+ str(qstring)
						+ "</th>"
					)
				else:
					sec_str += (
						'<th data-field="'
						+ invs
						+ '" data-title-tooltip="'
						+ str(qstring)
						+ '" data-sortable="true" data-filter-control="input">'
						+ str(qstring)
						+ "</th>"
					)
			sec_str += '</tr></thead><tbody class ="equipments_id" ></tbody></table>'
			sec_str += '<div id="contact_replace_addnew_model_footer"></div>'
			values_list = ""
			values_lists = ""
			a_test = []
			for invsk in list(Header_details):
				table_ids = "#" + str(table_id)
				filter_class = table_ids + " .bootstrap-table-filter-control-" + str(invsk)
				values_lists += "var " + str(invsk) + ' = $("' + str(filter_class) + '").val(); '
				values_lists += " ATTRIBUTE_VALUEList.push(" + str(invsk) + "); "
				a_test.append(invsk)
				filter_control_function += (
					'$("'
					+ filter_class
					+ '").change( function(){ var table_id = $(this).closest("table").attr("id"); var a_list = '
					+ str(a_test)
					+ "; ATTRIBUTE_VALUEList = []; "
					+ str(values_lists)
					+ ' SortColumn = localStorage.getItem("SortColumn"); SortColumnOrder = localStorage.getItem("SortColumnOrder"); PerPage = $("#PageCountValue").val(); PageInform = "1___" + PerPage + "___" + PerPage; cpq.server.executeScript("SYUADNWPOP", {\'TABLEID\': "'
					+ str(TABLEID)
					+ "\", 'OPER': 'NO', 'RECORDID': \""
					+ str(RECORDID)
					+ "\", 'RECORDFEILD':  \""
					+ str(RECORDFEILD)
					+ "\", 'NEWVALUE': '', 'LOOKUPOBJ': '', 'LOOKUPAPI': '','A_Keys':a_list,'A_Values':ATTRIBUTE_VALUEList}, function(data) {  date_field = data[3]; var assoc = data[1]; var api_name = data[2];data4 = data[4];data5 = data[5]; try { if(date_field.length > 0) { $(\""
					+ str(table_ids)
					+ '").bootstrapTable("load", date_field  ); $("button#country_save").attr("disabled",false); $("#noRecDisp").remove() } else{ var date_field = [];$("'
					+ str(table_ids)
					+ '").bootstrapTable("load", date_field  ); $("button#country_save").attr("disabled",true); $("#contact_replace_addnew_model").after("<div id=\'noRecDisp\' class=\'noRecord\'>No Records to Display</div>"); $(".noRecord:not(:first)").remove(); } } catch(err) { if(date_field.length > 0) { $("'
					+ str(table_ids)
					+ '").bootstrapTable("load", date_field  ); $("button#country_save").attr("disabled",false); } else{ $("'
					+ str(table_ids)
					+ '").bootstrapTable("load", date_field  ); $("button#country_save").attr("disabled",true); } } ; });  });'
				)
			pagination_condition = "OFFSET {Offset_Skip_Count} ROWS FETCH NEXT {Fetch_Count} ROWS ONLY".format(
				Offset_Skip_Count=offset_skip_count-1 if offset_skip_count%10==1 else offset_skip_count, Fetch_Count=fetch_count
			)
			Pagination_M = SqlHelper.GetFirst("""select count(SACONT.CpqTableEntryId) as count from SACONT (NOLOCK) WHERE SACONT.CONTACT_RECORD_ID  NOT IN (SELECT CONTACT_RECORD_ID FROM SAQICT (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}')""".format(contract_quote_record_id,quote_revision_record_id))

			order_by = "order by SACONT.CONTACT_ID ASC"

			if str(PerPage) == "" and str(PageInform) == "":
				Page_start = 1
				Page_End = fetch_count
				PerPage = fetch_count
				PageInform = "1___"+str(fetch_count)+"___"+str(fetch_count)
			else:
				Page_start = int(PageInform.split("___")[0])
				Page_End = int(PageInform.split("___")[1])
				PerPage = PerPage

			order_by = ""
			if SortColumn != '' and SortColumnOrder !='':
				order_by = "order by "+SortColumn + " " + SortColumnOrder
			else:
				order_by = "order by CONTACT_ID ASC"

			pop_val = {}
			if where_string:
				where_string += " AND"
				Trace.Write("soureceequipments "+str(where_string))
			if TreeParam == "Customer Information":
				where_string += """ SACONT.CONTACT_RECORD_ID NOT IN (SELECT CONTACT_RECORD_ID FROM SAQICT (NOLOCK) where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}')""".format(contract_quote_record_id,quote_revision_record_id)
			
			table_data = Sql.GetList("Select {} FROM SACONT {} {} {}".format(", ".join(ordered_keys),"WHERE " +where_string if where_string else "",order_by,pagination_condition))
			QueryCountObj = Sql.GetFirst(
				"select count(*) as cnt from SACONT (NOLOCK) {}".format(
				"WHERE " +where_string if where_string else ""
				)
			)
			if QueryCountObj is not None:
				QryCount = QueryCountObj.cnt


			if table_data is not None :
				for row_data in table_data:
					data_id = str(ObjectName)

					new_value_dict = {}

					for data in row_data:
						if str(data.Key) == "CONTACT_RECORD_ID":
							pop_val = str(data.Value)
							cpqidval = CPQID.KeyCPQId.GetCPQId(ObjectName, str(data.Value))
							new_value_dict[data.Key] = cpqidval
						else:
							new_value_dict[data.Key] = data.Value
						new_value_dict["pop_val"] = pop_val
					date_field.append(new_value_dict)
			QueryCount = len(date_field)

			pagination_total_count = 0
			if Pagination_M is not None:
				pagination_total_count = Pagination_M.count
			if offset_skip_count == 0:
				offset_skip_count = 1
				records_end = fetch_count
			records_end = offset_skip_count + fetch_count - 1
			records_end = pagination_total_count if pagination_total_count < records_end else records_end
			records_start_and_end = "{} - {} of ".format(offset_skip_count, records_end)
			disable_next_and_last = ""
			disable_previous_and_first = ""
			if records_end == pagination_total_count:
				disable_next_and_last = "class='btn-is-disabled' style=\'pointer-events:none\' "
			if offset_skip_count == 0:
				disable_previous_and_first = "class='btn-is-disabled' style=\'pointer-events:none\' "
			current_page = int(math.ceil(offset_skip_count / fetch_count)) + 1

			Product.SetGlobal("QueryCount", str(QueryCount))
			pagination_table_id = "pagination_{}".format(table_id)
			if QueryCount != 0:
				var_str = """<div id="{Parent_Div_Id}" class="col-md-12 brdr listContStyle padbthgt30">
									<div class="col-md-4 pager-numberofitem  clear-padding">
										<span class="pager-number-of-items-item flt_lt_pad2_mar2022" id="RecordsStartAndEnd">{Records_Start_And_End}</span>
										<span class="pager-number-of-items-item flt_lt_pad2_mar" id="TotalRecordsCount">{Pagination_Total_Count}</span>
										<div class="clear-padding fltltmrgtp3">
											<div class="pull-right vralign">
												<select onchange="ShowResultCountFunc(this, '{ShowResultCountFuncTb}', 'addEquipment', '{TableId}')" id="ShowResultCount" class="form-control selcwdt">
													<option value="10" {Selected_10}>10</option>
													<option value="20" {Selected_20}>20</option>
													<option value="50" {Selected_50}>50</option>
													<option value="100" {Selected_100}>100</option>
													<option value="200" {Selected_200}>200</option>
												</select> 
											</div>
										</div>
									</div>
									<div class="col-xs-8 col-md-4  clear-padding inpadtex" data-bind="visible: totalItemCount">
										<div class="clear-padding col-xs-12 col-sm-6 col-md-12 brd0">
											<ul class="pagination pagination">
												<li class="disabled">
													<a onclick="GetFirstResultFunc('{GetFirstResultFuncTb}', 'addEquipment', '{TableId}')" {Disable_First}><i class="fa fa-caret-left fnt14bold"></i><i class="fa fa-caret-left fnt14"></i></a>
												</li>
												<li class="disabled"><a onclick="GetPreviuosResultFunc('{GetPreviuosResultFuncTb}', 'addEquipment', '{TableId}')" {Disable_Previous}><i class="fa fa-caret-left fnt14"></i>PREVIOUS</a></li>
												<li class="disabled"><a onclick="GetNextResultFunc('{GetNextResultFuncTb}', 'addEquipment', '{TableId}')" {Disable_Next}>NEXT<i class="fa fa-caret-right fnt14"></i></a></li>
												<li class="disabled"><a onclick="GetLastResultFunc('{GetLastResultFuncTb}', 'addEquipment', '{TableId}')" {Disable_Last}><i class="fa fa-caret-right fnt14"></i><i class="fa fa-caret-right fnt14bold"></i></a></li>
											</ul>
										</div> 
									</div> 
									<div class="col-md-4 pad3"> 
										<span id="page_count" class="currentPage page_right_content">{Current_Page}</span>
										<span class="page_right_content padrt2">Page </span>
									</div>
								</div>""".format(
					Parent_Div_Id=pagination_table_id,
					Records_Start_And_End=records_start_and_end,
					Pagination_Total_Count=pagination_total_count,
					ShowResultCountFuncTb=pagination_table_id,
					Selected_10="selected" if fetch_count == 10 else "",
					Selected_20="selected" if fetch_count == 20 else "",
					Selected_50="selected" if fetch_count == 50 else "",
					Selected_100="selected" if fetch_count == 100 else "",
					Selected_200="selected" if fetch_count == 200 else "",
					GetFirstResultFuncTb=pagination_table_id,
					Disable_First=disable_previous_and_first,
					GetPreviuosResultFuncTb=pagination_table_id,
					Disable_Previous=disable_previous_and_first,
					GetNextResultFuncTb=pagination_table_id,
					Disable_Next=disable_next_and_last,
					GetLastResultFuncTb=pagination_table_id,
					Disable_Last=disable_next_and_last,
					Current_Page=current_page,
					TableId=TABLEID,
				)
			else:
				date_field = "NORECORDS"
				Trace.Write("No Equipment Records")
			table_ids = "#" + str(table_id)
			# Filter based on table MultiSelect Dropdown column - Start

			for index, col_name in enumerate(ordered_keys):
				table, api_name = ObjectName, col_name
				obj_data = Sql.GetFirst(
					"SELECT API_NAME, DATA_TYPE, PICKLIST FROM  SYOBJD WHERE OBJECT_NAME='"
					+ str(table)
					+ "' and API_NAME = '"
					+ str(api_name)
					+ "'"
				)
				if obj_data is not None:
					if str(obj_data.PICKLIST).upper() == "TRUE":
						filter_tag = (
							'<div id = "'
							+ str(table_id)
							+ "_RelatedMutipleCheckBoxDrop_"
							+ str(index)
							+ '" class="form-control bootstrap-table-filter-control-'
							+ str(api_name)
							+ " RelatedMutipleCheckBoxDrop_"
							+ str(index)
							+ ' "></div>'
						)
						filter_tags.append(filter_tag)
						filter_types.append("select")
						if obj_data.DATA_TYPE == "CHECKBOX":
							filter_values.append(["True", "False"])
						else:
							# Trace.Write("=============$$$$$$$$$$$$$>>>>>>>>>>>>> "+"SELECT DISTINCT {Column} FROM {Table}".format(Column=api_name, Table=table))
							data_obj = Sql.GetList(
								"SELECT DISTINCT {Column} FROM {Table}".format(Column=api_name, Table=table)
							)
							if data_obj is not None:
								filter_values.append([row_data.Value for data in data_obj for row_data in data])
					else:
						filter_tag = (
							'<input type="text" class="form-control wth100visble bootstrap-table-filter-control-'
							+ str(api_name)
							+ '">'
						)
						filter_tags.append(filter_tag)
						filter_types.append("input")
						filter_values.append("")

			filter_drop_down = (
				"try { if( document.getElementById('"
				+ str(table_id)
				+ "') ) { var listws = document.getElementById('"
				+ str(table_id)
				+ "').getElementsByClassName('filter-control');  for (i = 0; i < listws.length; i++) { document.getElementById('"
				+ str(table_id)
				+ "').getElementsByClassName('filter-control')[i].innerHTML = data6[i];  } for (j = 0; j < listws.length; j++) { if (data10[j] == 'select') { var dataAdapter = new $.jqx.dataAdapter(data8[j]); if(data11[j].length>5){ $('#"
				+ str(table_id)
				+ "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter}); }else{$('#"
				+ str(table_id)
				+ "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter ,autoDropDownHeight: true});} } } } }  catch(err) { setTimeout(function() { var listws = document.getElementById('"
				+ str(table_id)
				+ "').getElementsByClassName('filter-control');  for (i = 0; i < listws.length; i++) { document.getElementById('"
				+ str(table_id)
				+ "').getElementsByClassName('filter-control')[i].innerHTML = data9[i];  } for (j = 0; j < listws.length; j++) { if (data10[j] == 'select') { var dataAdapter = new $.jqx.dataAdapter(data11[j]); $('#"
				+ str(table_id)
				+ "_RelatedMutipleCheckBoxDrop_' + j.toString() ).jqxDropDownList( { checkboxes: true, source: dataAdapter, scrollBarSize :10 }); } } }, 5000); }"
			)
			dbl_clk_function += (
				'$("'
				+ str(table_ids)
				+ '").on("all.bs.table", function (e, name, args) { $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>"); }); $("'
				+ str(table_ids)
				+ '\ th.bs-checkbox div.th-inner").before("<div class=\'pad0brdbt\'>SELECT</div>"); $(".bs-checkbox input").addClass("custom"); $(".bs-checkbox input").after("<span class=\'lbl\'></span>");'
			)

			pagedata = ""
			if QryCount < int(PerPage):
				pagedata = str(Page_start) + " - " + str(QryCount) + " of "
			else:
				pagedata = str(Page_start) + " - " + str(Page_End)+ " of "

		
					
		else:
			#Trace.Write("===============> Else")
			overflow_val = ""
			where_condition = ""
			if ObjectName == "ACACST":
				where_condition = (
					" AND API_NAME NOT IN ('CRITERIA_01','CRITERIA_02','CRITERIA_03','CRITERIA_04','CRITERIA_05')"
				)
			Sqq_obj = Sql.GetList(
				"SELECT top 1000 API_NAME, DATA_TYPE, FORMULA_DATA_TYPE, LOOKUP_OBJECT, REQUIRED, PERMISSION, FIELD_LABEL, LOOKUP_API_NAME, LENGTH FROM  SYOBJD (NOLOCK) WHERE LTRIM(RTRIM(OBJECT_NAME))='"
				+ str(ObjectName)
				+ "' "
				+ where_condition
				+ " ORDER BY abs(DISPLAY_ORDER) "
			)

			lookup_val = [val.LOOKUP_API_NAME for val in Sqq_obj]			
			if ObjectName == "ACACST":
				lookup_val.append("APROBJ_LABEL")
			lookup_list = {ins.LOOKUP_API_NAME: ins.LOOKUP_OBJECT for ins in Sqq_obj}			
			lookup_list1 = {ins.LOOKUP_API_NAME: ins.API_NAME for ins in Sqq_obj}
			Trace.Write('###Lookup List--->'+str(lookup_list))		
			new_value_dict = {}
			new_value_dict1 = {}
			val_list = []
			TreeParam = Product.GetGlobal("CommonTreeParam")
			TreeParentParam = Product.GetGlobal("TreeParentLevel0")
			TreeSuperParentParam = Product.GetGlobal("TreeParentLevel1")
			new_value_dict2 = {}
			if str(ObjectName) == "SYROUS":
				if Product.Attributes.GetByName("QSTN_SYSEFL_SY_00001"):
					record_value = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00001").GetValue()
					result = ScriptExecutor.ExecuteGlobal(
						"SYPARCEFMA",
						{"Object": str(ObjectName), "API_Name": "ROLE_RECORD_ID", "API_Value": str(record_value),},
					)
					new_value_dict1 = {API_Names.get("API_NAME"): API_Names.get("FORMULA_RESULT") for API_Names in result}
			
	
	
			else:				               
				result = ScriptExecutor.ExecuteGlobal(
					"SYPARCEFMA", {"Object": str(ObjectName), "API_Name": record_field, "API_Value": str(primary_value),},
				)
				new_value_dict1 = {API_Names.get("API_NAME"): API_Names.get("FORMULA_RESULT") for API_Names in result}
				Trace.Write("new_value_dict1==111"+str(new_value_dict1))
				attrval_obj = Sql.GetFirst(
					"SELECT API_NAME FROM  SYOBJD(NOLOCK) WHERE OBJECT_NAME='"
					+ str(ObjectName)
					+ "' AND LOOKUP_OBJECT='"
					+ str(record_value)
					+ "' "
				)
				if attrval_obj:
					api_name = attrval_obj.API_NAME.strip()
					result = ScriptExecutor.ExecuteGlobal(
						"SYPARCEFMA", {"Object": str(ObjectName), "API_Name": api_name, "API_Value": str(primary_value),},
					)
					new_value_dict_new = {}
					new_value_dict_new[api_name] = str(primary_value)
					new_value_dict = {API_Names.get("API_NAME"): API_Names.get("FORMULA_RESULT") for API_Names in result}
					new_value_dict.update(new_value_dict_new)
					# A043S001P01-12265 Start
					if str(ObjectName) == "ACACSA" or str(ObjectName) == "ACAPTF":
						TreeParam = Product.GetGlobal("TreeParam")
						ChainRec = new_value_dict.get("APRCHN_RECORD_ID")
						StepRecordId = Sql.GetFirst(
							"select * from ACACST (nolock) INNER JOIN SYOBJH (NOLOCK) ON ACACST.TSTOBJ_RECORD_ID = SYOBJH.RECORD_ID"
							+ " WHERE APRCHNSTP_NAME = '"
							+ str(TreeParam).split(': ')[1]
							+ "' AND APRCHN_RECORD_ID = '"
							+ str(ChainRec)
							+ "'"
						)
						new_value_dict["APRCHNSTP_RECORD_ID"] = str(StepRecordId.APPROVAL_CHAIN_STEP_RECORD_ID)
						new_value_dict["APRCHNSTP_NUMBER"] = str(StepRecordId.APRCHNSTP_NUMBER)
						Chain_Record_Id = new_value_dict["APRCHNSTP_RECORD_ID"]
						if str(ObjectName) == "ACAPTF":
							new_value_dict["TRKOBJ_RECORD_ID"] = str(StepRecordId.RECORD_ID)
							new_value_dict["TRKOBJ_NAME"] = str(StepRecordId.LABEL)
					# A043S001P01-12265 End
					if TABLEID == 'ADDNEW__SYOBJR_00014_SYOBJ_01024' and LOOKUPAPI == 'PROFILE_ID':
						api_name = 'PROFILE_RECORD_ID'
					
				Product.SetGlobal("Flag_value", "false")
				
			if str(ObjectName)  == "SYSEFL":
				Trace.Write("Pers Attr Value--->")
				TreeTopSuperParentParam = Product.GetGlobal("TreeParentLevel2")
				Getapiname = Sql.GetFirst(
					"SELECT RECORD_ID FROM SYSECT (NOLOCK) WHERE SECTION_NAME = '"
					+ str(TreeParentParam)
					+ "' AND PAGE_NAME = '"
					+ str(TreeTopSuperParentParam)
					+"'"
				)
				if Getapiname is not None:
					PersAttVal_rec_id = str(Getapiname.RECORD_ID)
					result = ScriptExecutor.ExecuteGlobal(
						"SYPARCEFMA",
						{
							"Object": str(ObjectName),
							"API_Name": "SECTION_RECORD_ID",
							"API_Value": str(PersAttVal_rec_id),
						},
					)
					new_value_dict3 = {}
					new_value_dict3["SECTION_RECORD_ID"] = str(PersAttVal_rec_id)
					new_value_dict2 = {API_Names.get("API_NAME"): API_Names.get("FORMULA_RESULT") for API_Names in result}
					new_value_dict1.update(new_value_dict2)
					new_value_dict1.update(new_value_dict3)
			if TreeParentParam == "Approval Chain Steps":
				TreeParam = Product.GetGlobal("TreeParam")
				StepRecordId = Sql.GetFirst(
					"select * from ACACST (nolock) where APRCHNSTP_NAME = '"
					+ str(TreeParam).split(': ')[1]
					+ "' AND APRCHN_RECORD_ID = '"
					+ str(primary_value)
					+ "'"
				)
				# Trace.Write(
				#     "select * from ACACST (nolock) where APRCHNSTP_NAME = '"
				#     + str(TreeParam).split(': ')[1]
				#     + "' AND APRCHN_RECORD_ID = '"
				#     + str(primary_value)
				#     + "'"
				# )
				if StepRecordId:
					result = ScriptExecutor.ExecuteGlobal(
						"SYPARCEFMA",
						{
							"Object": str(ObjectName),
							"API_Name": "APPROVAL_CHAIN_STEP_RECORD_ID",
							"API_Value": str(StepRecordId.APPROVAL_CHAIN_STEP_RECORD_ID),
						},
					)
					new_value_dict3 = {}
					new_value_dict3["APPROVALCHAIN_STEP_RECORD_ID"] = str(StepRecordId.APPROVAL_CHAIN_STEP_RECORD_ID)
					new_value_dict2 = {API_Names.get("API_NAME"): API_Names.get("FORMULA_RESULT") for API_Names in result}
					new_value_dict1.update(new_value_dict2)
					new_value_dict1.update(new_value_dict3)
					if LOOKUPOBJ == "cpq":
						newval = str(NEWVALUE).split("|")
						getcpqpermission = Sql.GetFirst(
							"""SELECT permission_id,permission_name FROM cpq_permissions (NOLOCK) WHERE permission_id = '{permissionid}' """.format(
								permissionid=str(newval[0])
							)
						)
						new_value_dict["PROFILE_ID"] = str(getcpqpermission.permission_name)
						new_value_dict["PROFILE_RECORD_ID"] = str(getcpqpermission.permission_id)

			if NEWVALUE != "":
				Trace.Write("else1====NEWVALUE")
				if str(OPER) == "CLEAR SELECTION":
					attrval_obj = Sql.GetFirst(
						"SELECT API_NAME FROM  SYOBJD (NOLOCK) WHERE OBJECT_NAME='"
						+ str(ObjectName)
						+ "' AND LOOKUP_OBJECT='"
						+ str(NEWVALUE)
						+ "'"
					)

					api_name = attrval_obj.API_NAME.strip()
					TABLE_OBJS = Sql.GetList(
						"select OBJECT_NAME,API_NAME,DATA_TYPE,LOOKUP_OBJECT,FORMULA_LOGIC FROM  SYOBJD (NOLOCK) where OBJECT_NAME ='"
						+ str(ObjectName)
						+ "' and FORMULA_LOGIC like '%"
						+ str(api_name)
						+ "%'"
					)
					if TABLE_OBJS is not None:
						for TABLE_OBJ in TABLE_OBJS:
							#Trace.Write("Parse Formula")
							if TABLE_OBJ.DATA_TYPE != "":
								DATA_TYPE = str(TABLE_OBJ.DATA_TYPE)

								if api_name in str(TABLE_OBJ.FORMULA_LOGIC):
									new_value_dict[str(TABLE_OBJ.API_NAME)] = ""
									new_value_dict[str(api_name)] = ""
				else:
					attrval_obj = Sql.GetFirst(
						"SELECT API_NAME FROM  SYOBJD (NOLOCK)WHERE OBJECT_NAME='"
						+ str(ObjectName)
						+ "' AND LOOKUP_OBJECT='"
						+ str(LOOKUPOBJ)
						+ "' and  LOOKUP_API_NAME='"
						+ str(LOOKUPAPI)
						+ "'"
					)
					if attrval_obj is not None:
						api_name = attrval_obj.API_NAME.strip()
						if api_name:
							NEWVALUE = NEWVALUE.split("|")
							result = ScriptExecutor.ExecuteGlobal(
								"SYPARCEFMA", {"Object": str(ObjectName), "API_Name": api_name, "API_Value": NEWVALUE[0],},
							)
							new_value_dict = {
								API_Names.get("API_NAME"): API_Names.get("FORMULA_RESULT") for API_Names in result
							}                            
							if api_name == "OBJECTFIELD_RECORD_ID" and popup_table_id == "SYOBJR-95825":
								APIName_value = new_value_dict.get("OBJECTFIELD_APINAME")
								RecAtt_objval = Product.Attr("QSTN_SYSEFL_SY_09875").GetValue()
								getobjd_val = Sql.GetFirst(
									"SELECT * FROM SYOBJD WHERE OBJECT_NAME='"
									+ str(RecAtt_objval)
									+ "' and API_NAME ='"
									+ str(APIName_value)
									+ "' and DATA_TYPE='LOOKUP'"
								)
								if getobjd_val is not None:
									new_value_dict["REFOBJECT_APINAME"] = str(getobjd_val.LOOKUP_OBJECT)
							TreeParam = Product.GetGlobal("TreeParam")
							if str(ObjectName) == "SYTABS" and str(CurrentTab).upper() == "PAGE" and str(TreeParam) == "Tabs" and api_name == "PRIMARY_OBJECT_RECORD_ID":
								new_value_dict["TAB_ID"] = str(new_value_dict["PRIMARY_OBJECT_NAME"])+"OTAB"
								#Trace.Write("api_name"+str())
							if str(ObjectName) == "SYOBFD" and str(CurrentTab) == "Object":
								cf_field_val = df_field_val = col_count = ""
								cf_field_val = new_value_dict.get("CONTROLLING_FIELD_VALUE")
								cf_list = df_list = dep_list = cntrolling_list = []
								cf_field = new_value_dict.get("CONTROLLING_FIELD")
								if str(api_name) == "DEPENDENT_FIELD_RECORD_ID":
									df_field_val = new_value_dict.get("DEPENDENT_FIELD_VALUE")
									df_field = new_value_dict.get("DEPENDENT_FIELD")
									df_list = df_field_val.split(",")
									dep_list = list(df_list)
									dep_list.insert(0, "DEPENDENT FIELD")
									dep_list.insert(1, df_field)

								if cf_field_val:
									cf_list = cf_field_val.split(",")
									sap_list = list(cf_list)
									sap_list.insert(0, "CONTROLLING FIELD")
									sap_list.insert(1, cf_field)
									Product.SetGlobal("cntrolling_list", str(list(sap_list)))
									col_count = len(sap_list)
									table_header = '<table class="table table-bordered" id="' + str(ObjectName) + '">'
									if len(sap_list) > 0 or len(dep_list) > 0:
										table_header += "<thead><tr>"
										for header in sap_list:
											Trace.Write("header---" + str(header))
											table_header += (
												'<th data-field="'
												+ str(header)
												+ '" class="ma_text_align_seventeen"><abbr title="'
												+ header
												+ '">'
												+ header
												+ "</abbr></th>"
											)
										table_header += "</tr></thead></table>"
								if str(api_name) == "DEPENDENT_FIELD_RECORD_ID":
									cntrolling_list = Product.GetGlobal("cntrolling_list")
									cntrolling_list_val = []
									cntrolling_list_val = cntrolling_list.split()

									if len(cntrolling_list) > 0 or len(dep_list) > 0:
										table_header = (
											'<table class="table table-bordered" id="' + str(ObjectName) + '"><thead><tr>'
										)
										for header in cntrolling_list_val:
											table_header += (
												'<th data-field="'
												+ str(header)
												+ '" class="ma_text_align_seventeen"><abbr title="'
												+ header
												+ '">'
												+ header
												+ "</abbr></th>"
											)
										table_header += "</tr></thead><tbody>"
										for row, inx in enumerate(dep_list):
											table_header += (
												'<tr class="iconhvr" id = "' + str(ObjectName) + "__" + str(row) + '">'
											)
											if row == 0:
												table_header += (
													'<td align="left" ><abbr title="'
													+ str(inx)
													+ '">'
													+ str(inx)
													+ "</abbr></td>"
												)
											for keys, Names_dict in enumerate(dep_list):
												if keys != 1:
													table_header += (
														'<td align="left" ><input id="'
														+ str(inx)
														+ '" type="checkbox" value="'
														+ inx
														+ '" class="custom" ><span class="lbl"></span><abbr title="'
														+ str(inx)
														+ '">'
														+ str(inx)
														+ "</abbr></td>"
													)

											table_header += "</tr>"

											table_header += "</tbody></table>"
							if TABLEID == 'ADDNEW__SYOBJR_00014_SYOBJ_01024' and LOOKUPAPI == 'PROFILE_ID':
								#Trace.Write("2116---ADDNEW__SYOBJR_00014_SYOBJ_01024")
								api_name = 'PROFILE_RECORD_ID'
			else:				
				attrval_obj = Sql.GetFirst(
					"SELECT API_NAME FROM  SYOBJD(NOLOCK) WHERE OBJECT_NAME='"
					+ str(ObjectName)
					+ "' AND LOOKUP_OBJECT='"
					+ str(record_value)
					+ "' "
				)
				if attrval_obj is not None:
					api_name = attrval_obj.API_NAME.strip()
					result = ScriptExecutor.ExecuteGlobal(
						"SYPARCEFMA", {"Object": str(ObjectName), "API_Name": api_name, "API_Value": str(primary_value),},
					)
					new_value_dict_new = {}
					new_value_dict_new[api_name] = str(primary_value)
					new_value_dict = {API_Names.get("API_NAME"): API_Names.get("FORMULA_RESULT") for API_Names in result}
					new_value_dict.update(new_value_dict_new)
					
					# A043S001P01-12265 Start
					if str(ObjectName) == "ACACSA" or str(ObjectName) == "ACAPTF":
						ChainRec = new_value_dict.get("APRCHN_RECORD_ID")
						StepRecordId = Sql.GetFirst(
							"select * from ACACST (nolock) INNER JOIN SYOBJH (NOLOCK) ON ACACST.TSTOBJ_RECORD_ID = SYOBJH.RECORD_ID"
							+ " WHERE APRCHNSTP_NAME = '"
							+ str(TreeParam).split(': ')[1]
							+ "' AND APRCHN_RECORD_ID = '"
							+ str(ChainRec)
							+ "'"
						)
						new_value_dict["APRCHNSTP_RECORD_ID"] = str(StepRecordId.APPROVAL_CHAIN_STEP_RECORD_ID)
						new_value_dict["APRCHNSTP"] = str(StepRecordId.APRCHNSTP_NUMBER)
						if str(ObjectName) == "ACAPTF":
							new_value_dict["TRKOBJ_RECORD_ID"] = str(StepRecordId.RECORD_ID)
							new_value_dict["TRKOBJ_NAME"] = str(StepRecordId.LABEL)
						if TABLEID == 'ADDNEW__SYOBJR_00014_SYOBJ_01024' and LOOKUPAPI == 'PROFILE_ID':
							#Trace.Write("PROFILE_ID---ADDNEW__SYOBJR_00014_SYOBJ_01024")
							api_name = 'PROFILE_RECORD_ID'
					# A043S001P01-12265 End
				Product.SetGlobal("Flag_value", "false")

			GettreeEnable = Sql.GetFirst("select ENABLE_TREE FROM SYTABS where SAPCPQ_ALTTAB_NAME='" + str(TabName) + "'")
			if GettreeEnable is None or str(GettreeEnable.ENABLE_TREE).upper() != "TRUE":

				sec_str += (
					'<div class="row modulebnr brdr ma_mar_btm">'
					+ str(popup_lable_obj.NAME).upper()
					+ ' : ADD NEW <button type="button" class="close flt_rt" onclick="closepopup_scrl()" data-dismiss="modal">X</button></div>'
				)
				sec_str += '<div class="col-md-12"><div class="row pad-10 bg-lt-wt brdr">'
				sec_str += '<button type="button" class="btnconfig" onclick="closepopup_scrl()" data-dismiss="modal">CANCEL</button>'

				sec_str += (
					'<button type="button" id="'
					+ str(ObjectName)
					+ '" class="btnconfig viewvalidate " onclick="'
					+ func2
					+ '">'
					+ btn2
					+ "</button>"
				)
				sec_str += "</div></div>"
			sec_str += '<div id="Headerbnr" class="mart_col_back"></div>'
			sec_str += '<div class="col-md-12"  style="display: none;"><div class="row modulesecbnr brdr" data-toggle="collapse" data-target="#SegAlert_notifcation" aria-expanded="true" >NOTIFICATIONS<i class="pull-right fa fa-chevron-down "></i><i class="pull-right fa fa-chevron-up"></i></div><div  id="SegAlert_notifcation" class="col-md-12  alert-notification  brdr collapse in" ><div class="col-md-12 alert-warning" id="alert_msg"><label><img src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/warning1.svg" alt="Warning"></label></div></div></div>'

			if GettreeEnable is not None and str(GettreeEnable.ENABLE_TREE).upper() == "TRUE":
				if str(popup_table_id) == "SYOBJR-98798":
					sec_str += (
						'<div id="container" text="'
						+ str(ObjectName)
						+ '" class="except_sec" style="'
						+ str(overflow_val)
						+ '">'
					)
				else:
					sec_str += (
						'<div id="container" text="'
						+ str(ObjectName)
						+ '" class="g4 pad-10 brdr except_sec header_section_div" style="'
						+ str(overflow_val)
						+ '">'
					)

			else:
				sec_str += (
					'<div id="container" text="'
					+ str(ObjectName)
					+ '" class="g4 pad-10 brdr except_sec" style="'
					+ str(overflow_val)
					+ '">'
				)

			if GettreeEnable is not None and str(GettreeEnable.ENABLE_TREE).upper() == "TRUE":
				Trace.Write("Involved Parties----")
				sec_str += (
				'<div class="container_banner_inner_sec" style="display:none"><span style="display:none" id="container_banner_id">'
					+ str(popup_lable_obj.NAME).upper()
					+ " : ADD NEW</span></div>"
				)
			sec_str += '<table class="width100">'

			if Sqq_obj is not None:				
				for val in Sqq_obj:					
					current_obj_api_name = val.API_NAME.strip()					
					readonly_val = val.PERMISSION.strip()
					current_obj_field_lable = val.FIELD_LABEL.strip()
					data_type = val.DATA_TYPE.strip()
					formula_data_type = str(val.FORMULA_DATA_TYPE).strip()
					current_obj_value = ""
					readonly = ""
					disable = ""
					id_val = ""
					idval = ""
					formula_permission = ""
					formula_obj_permission = ""
					id_api = ""
					checked = ""
					priceclass_val = ""
					keypressval = ""
					parrent_object_name = ""
					add_style = ""
					onchange = ""
					max_length = val.LENGTH
					datepicker = "onclick_datepicker('" + current_obj_api_name + "')"
					datepicker_onchange = "onchangedatepicker('" + current_obj_api_name + "')"
					edit_pencil_icon = '<i class="fa fa-pencil" aria-hidden="true"></i>'
					if current_obj_api_name in lookup_val:
						for key, value in lookup_list.items():
							if key == current_obj_api_name:
								parrent_object_name = value.strip()

					if current_obj_api_name in lookup_val:
						formula_obj_permission = "true"
						for key, value in lookup_list1.items():
							if key == current_obj_api_name:
								formula_permission_qry = Sql.GetFirst(
									"SELECT * FROM  SYOBJD(NOLOCK) WHERE API_NAME = '"
									+ value
									+ "' and OBJECT_NAME = '"
									+ str(ObjectName)
									+ "' "
								)
								formula_permission = str(formula_permission_qry.PERMISSION).strip()
					

					if readonly_val == "READ ONLY":
						if formula_obj_permission == "true" and formula_permission != "READ ONLY":
							edit_pencil_icon = '<i class="fa fa-pencil" aria-hidden="true"></i>'
						else:
							edit_pencil_icon = '<i class="fa fa-lock" aria-hidden="true"></i>'
							readonly = "readonly"
							disable = "disabled"
					else:
						readonly = ""
						disable = ""
						edit_pencil_icon = '<i class="fa fa-pencil" aria-hidden="true"></i>'

					if current_obj_api_name in new_value_dict1:
						TreeParam = Product.GetGlobal("TreeParam")
						if str(current_obj_api_name) == "TO_CURRENCY" or (str(current_obj_api_name) == "TAB_NAME" and str(ObjectName) == "SYPSAC" and str(TreeParam) == "Actions"):
							edit_pencil_icon = '<i class="fa fa-pencil" aria-hidden="true"></i>'
						#elif str(current_obj_api_name) == "APROBJ_LABEL":
						#    edit_pencil_icon = '<i class="fa fa-pencil" aria-hidden="true"></i>'
						#    readonly = ""
						#    disable = ""
						#    #Trace.Write("READ_TRACZZ"+str(readonly))
						else:
							#Trace.Write(str(readonly)+"------else--3451-------"+str(current_obj_api_name))
							
							if readonly == "readonly":
								readonly = "readonly"
								edit_pencil_icon = '<i class="fa fa-lock" aria-hidden="true"></i>'
							else:
								if str(current_obj_api_name) == "NODE_PAGE_NAME":
									readonly = "readonly"
									edit_pencil_icon = '<i class="fa fa-lock" aria-hidden="true"></i>'
								else:
									readonly = ''
									edit_pencil_icon = '<i class="fa fa-pencil" aria-hidden="true"></i>'
							disable = "disabled"

					ObjectName_list = [
						"MAVSDP",
						"PRPMMF",
						"MAMAEF",
						"SGASFC",
						"SAASLG",
						"MACPMP",
						"MASPMC",
						"PRLPBE",
						"PREXRT",
						"PRLPBK",
						"MAMAAT",
						"ACACST",
					]
					Currentobj_list = [
						"OUT_OF_STOCK",
						"SORTKEY3",
						"MATEMBFND_ID",
						"MODCLS_ID",
						"PRICING_CURRENCY",
						"ACCOUNT_TYPE",
						"SORACC_ID",
						"SORLNG_ID",
						"SORCTYPLTMAT_ID",
						"PERMAT_ID",
						"FULVNDACT_ID",
						"FACE_VALUE",
						"MARKET_PRICE",
						"MATERIAL_COST",
						"GIFTCARD_COST",
						"SORG_DEF_CURRENCY",
						"GPA_FACTOR",
						"SPA_FACTOR",
						"LOWPRCADJ_FACTOR",
						"CRITERIA_01",
						"CRITERIA_02",
						"CRITERIA_03",
						"CRITERIA_04",
						"CRITERIA_05",                        
					]

					if current_obj_api_name in [
						"CPQTABLEENTRYADDEDBY",
						"CPQTABLEENTRYDATEADDED",
						"CpqTableEntryModifiedBy",
						"CpqTableEntryDateModified",
						"OWNER_ID",
						"OWNED_DATE",
						"ATTVAL_VALFORMULA",                        
						"DELEGATED_APPROVER_ID",
						"DELEGATION_END",
						"DELEGATION_START",
						"TAB_ID"
					]:
						add_style = "display: none;"

					if (ObjectName == "SYSECT") and current_obj_api_name in ["SAPCPQ_ATTRIBUTE_NAME","PARENT_SECTION_TEXT","SECTION_PARTNUMBER"]:
						add_style = "display: none;"   
					
					if (ObjectName == "SYTABS") and current_obj_api_name in ["TAB_ID"] and str(CurrentTab).upper() == "PAGE":
						add_style = "display: none;" 
						#Trace.Write("added display non")                              

					if (ObjectName == "ACACSA" or ObjectName == "ACAPTF") and current_obj_api_name in ["APRCHN_ID","APRCHNSTP_APPROVER_ID"]:
						add_style = "display: none;"

					if (ObjectName == "SAQTIP") and current_obj_api_name in["QUOTE_ID","QUOTE_NAME","SALESORG_ID","SALESORG_NAME","QTEREV_ID"]:
						add_style = "display: none;"
					if ObjectName == "ACACST" and current_obj_api_name in ["MESSAGE_HEADERVALUE", "MESSAGE_BODYVALUE", "WHERE_CONDITION_01", "WHERE_CONDITION_02", "APRCHN_ID", "TSTOBJ_TESTEDFIELD_LABEL", "ENABLE_SMARTAPPROVAL"]:
						add_style = "display: none;"

					if str(ObjectName) == "ACACST" and str(CurrentTab) == "Approval Chain":
						MaxStepId = Sql.GetFirst(
							"select max(APRCHNSTP_NUMBER) as MaxId from ACACST (nolock) where APRCHN_RECORD_ID = '"
							+ str(primary_value)
							+ "'"
						)
						if MaxStepId and str(MaxStepId.MaxId) != "":
							NewMaxId = int(MaxStepId.MaxId) + 1
						else:
							NewMaxId = 1
						if str(current_obj_api_name) == "APRCHNSTP_NUMBER":
							current_obj_value = str(NewMaxId)
						elif str(current_obj_api_name) == "APRCHNSTP_NAME":
							current_obj_value = "Chain Step " + str(NewMaxId)
						elif str(current_obj_api_name) == "ACTIVE":
							
							current_obj_value = "TRUE"
						# elif str(current_obj_api_name) == "ENABLE_SMARTAPPROVAL":
						#     Trace.Write("pass_enable")
						#     current_obj_value = "TRUE"    
						Trace.Write("current_obj_value- current_obj_value-->"+str(current_obj_value))
					if data_type == "AUTO NUMBER":
						sec_str += (
							'<tr class="iconhvr borbot1" style="display: none;"><td class="width350"><label class="fltltpadlt15">'
							+ str(current_obj_field_lable)
							+ '</label></td><td class="width40"><a class="color_align_width" href="#" data-placement="top" data-toggle="popover" title="'+ str(current_obj_field_lable)+'" data-content="'
							+ str(current_obj_field_lable)
							+ '" ><i class="fa fa-info-circle flt_lt"></i>'
						)                        
						if str(val.REQUIRED).upper() == "TRUE" or val.REQUIRED == "1":
							sec_str += ""
						sec_str += "</a></td>"
						sec_str += (
							'<td><input id="'
							+ str(current_obj_api_name)
							+ '" type="text" value = "'+str(Guid.NewGuid()).upper()+'" class="form-control related_popup_css" hidden disabled></td>'
						)
						#Trace.Write("!!!!!!!!!"+str(current_obj_api_name))
						sec_str += '<td class="float_r_bor_bot"><div class="col-md-12 editiconright"><a href="#" class="editclick"><i class="fa fa-pencil" aria-hidden="true"></i></a></div></td>'
						sec_str += "</tr>"

					if data_type != "AUTO NUMBER":
						if (data_type == "LOOKUP" or current_obj_api_name == "REFOBJECT_APINAME" or current_obj_api_name == "REFOBJECTFIELD_APINAME"):
							add_style = "display: none;"
							Trace.Write("LOOKUP---->" + str(add_style))
						sec_str += (
							'<tr class="iconhvr borbot1" style=" '
							+ str(add_style)
							+ '"><td class="width350"><label class="fltltpadlt">'
							+ str(current_obj_field_lable)
							+ '</label></td><td class="width40"><a class="bgcccwth10" href="#" data-placement="top" title="'+ str(current_obj_field_lable)+'" data-toggle="popover" data-content="'
							+ str(current_obj_field_lable)
							+ '"><i class="fa fa-info-circle flt_lt"></i>'
						)
						if val.REQUIRED:
							if str(val.REQUIRED).upper() == "TRUE" or str(val.REQUIRED) == "1":
								sec_str += ""
								sec_str += '<span class="req-field mrg3fltltmt7">*</span>'
							sec_str += "</a></td>"

						if data_type == "LOOKUP":	
							Trace.Write("new_value_dict==="+str(new_value_dict))						
							if current_obj_api_name in new_value_dict:								
								current_obj_value = new_value_dict[current_obj_api_name]							

							try:
								Trace.Write("new_value_dict1==="+str(new_value_dict1))
								if current_obj_api_name in new_value_dict1:									
									current_obj_value = new_value_dict1.get(str(current_obj_api_name))

							except:
								Trace.Write("lookup field is not in the main list")

							sec_str += (
								'<td><input id="'
								+ str(current_obj_api_name)
								+ '" value="'
								+ str(current_obj_value)
								+ '" type="text" class="form-control related_popup_css" disabled></td>'
							)

						elif data_type == "FORMULA" and formula_data_type != "CHECKBOX":
							Trace.Write('current_obj_api_name---3650--'+str(current_obj_api_name))
							if current_obj_api_name == "TO_CURRENCY":
								if current_obj_api_name in lookup_val and readonly != "readonly":
									sec_str += (
										"<td><input id='"
										+ str(current_obj_api_name)
										+ "' type='text' value='"
										+ str(current_obj_value)
										+ "' class='form-control related_popup_css fltltlightyello' disabled>"
									)

									sec_str += (
										"<input class='popup flt_lt' id='"
										+ str(parrent_object_name)
										+ "' data-target='#cont_viewModalSection' onclick='cont_lookup_popup_new(this)' type='image'  src='../mt/default/images/customer_lookup.gif'></td>"
									)
							elif current_obj_api_name == "USER_NAME":
								sec_str += (
									"<td><input id='"
									+ str(current_obj_api_name)
									+ "' type='text' value='"
									+ str(current_obj_value)
									+ "' class='form-control related_popup_css fltltlightyello'>"
								)

								sec_str += (
									"<input class='popup flt_lt' id='"
									+ str(current_obj_api_name)
									+ "' data-target='#cont_viewModalSection' onclick='cont_lookup_popup_new(this)' type='image'  src='../mt/default/images/customer_lookup.gif'></td>"
								)
							elif current_obj_api_name == "OBJECTFIELD_APINAME":
								cont_event_name = "cont_lookup_popup_new(this,'VIEW_DIV_ID')"
								sec_str += (
									"<td><input id='"
									+ str(current_obj_api_name)
									+ "' type='text' value='"
									+ str(current_obj_value)
									+ "' class='form-control related_popup_css fltltlightyello'>"
								)
								sec_str += (
									'<input class="popup flt_lt" id="'
									+ str(parrent_object_name)
									+ '" data-target="#cont_viewModalSection" onclick="'
									+ cont_event_name
									+ '" type="image" data-toogle = "modal" src="../mt/default/images/customer_lookup.gif"></td>'
								)
							elif (
								str(current_obj_api_name) == "MESSAGE_HEADERVALUE"
								or str(current_obj_api_name) == "MESSAGE_BODYVALUE"
							):
								GetPrimeKey = Product.Attributes.GetByName("QSTN_SYSEFL_AC_00075").GetValue()
								sec_str += "<td>"
								sec_str += (
									'<div class="row"><div id="div_PICKLISTLOAD_'
									+ str(current_obj_api_name)
									+ '" class="multiselect"><select id="First'
									+ str(current_obj_api_name)
									+ '" multiple="multiple"'
									+ str(onchange)
									+ ' value="'
									+ current_obj_value
									+ '" class="form-control pop_up_brd_rad related_popup_css fltlt options_'
									+ str(current_obj_api_name)
									+ ' "  '
									+ " >"
								)
								currectvaluelist = current_obj_value.split(",")
								splitedlist = str(currectvaluelist).replace("[", "").replace("]", "")
								if len(currectvaluelist) == 1 and currectvaluelist[0] == "":
									splitedlist = "'1'"
								if str(current_obj_api_name) == "MESSAGE_HEADERVALUE":
									Tier_List = Sql.GetList(
										"""SELECT SYOBJD.FIELD_LABEL  FROM ACAPCH (NOLOCK) INNER JOIN SYOBJH (NOLOCK)
									ON ACAPCH.APROBJ_RECORD_ID = SYOBJH.RECORD_ID INNER JOIN SYOBJD (NOLOCK)
									ON SYOBJD.OBJECT_NAME = SYOBJH.OBJECT_NAME WHERE
									APPROVAL_CHAIN_RECORD_ID = '{chainrecordId}'
									AND SYOBJD.FIELD_LABEL NOT in ({exceptlist})""".format(
											chainrecordId=str(GetPrimeKey), exceptlist=splitedlist
										)
									)
								else:
									Tier_List = []
								for req1 in Tier_List:
									if current_obj_value == req1:
										sec_str += "<option>" + str(req1.FIELD_LABEL) + "</option>"
									else:
										sec_str += "<option>" + str(req1.FIELD_LABEL) + "</option>"
								sec_str += (
									'</select><div id="button_mvmt1"> <button onclick="unselectedval(this)" '
									+ 'class="leftbutton" id ="'
									+ str(current_obj_api_name)
									+ '"> <i class="glyphicon glyphicon-triangle-left"></i> </button> '
									+ '<button onclick="selectedval(this)" id ="'
									+ str(current_obj_api_name)
									+ '" class="rightbutton"> <i class="glyphicon glyphicon-triangle-right"></i> </button> '
									+ '</div><select multiple="multiple" id="options1_'
									+ str(current_obj_api_name)
									+ '" >'
								)
								for listval in currectvaluelist:
									sec_str += "<option>" + str(listval) + "</option>"
								sec_str += (
									'</select><div id="button_mvmt"> <button class="topbutton" onclick="topselect(this)" id ="'
									+ str(current_obj_api_name)
									+ '"> <i class="glyphicon glyphicon-triangle-top"></i> '
									+ '</button> <button class="btmbutton"'
									+ ' onclick="btmselect(this)"id ="'
									+ str(current_obj_api_name)
									+ '" > <i class="glyphicon glyphicon-triangle-bottom"></i> '
									+ "</button> </div></div></div></td>"
								)
							elif current_obj_api_name == "SECTION_NAME":
								sec_str += (
									"<td><input id='"
									+ str(current_obj_api_name)
									+ "' type='text' value='"
									+ str(TreeParentParam)
									+"' class='form-control related_popup_css' disabled>"
								)
							elif current_obj_api_name == "TREE_NAME":
								sec_str += (
									"<td><input id='"
									+ str(current_obj_api_name)
									+ "' type='text' value='"
									+ str(TreeParentParam)
									+"' class='form-control related_popup_css' disabled>"
								)
							elif current_obj_api_name == "PAGE_NAME" and str(ObjectName) == "SYPGAC":
								sec_str += (
									"<td><input id='"
									+ str(current_obj_api_name)
									+ "' type='text' value='"
									+ str(TreeParentParam)
									+"' class='form-control related_popup_css' disabled>"
								)	
							elif current_obj_api_name == "PAGE_LABEL" and str(ObjectName) == "SYSECT":
								sec_str += (
									"<td><input id='"
									+ str(current_obj_api_name)
									+ "' type='text' value='"
									+ str(TreeParentParam)
									+"' class='form-control related_popup_css' disabled>"
								)
							elif current_obj_api_name == "PAGE_NAME" and str(ObjectName) == "SYSECT":
								getpgname = Sql.GetFirst("select PAGE_NAME from SYPAGE where PAGE_LABEL = '"+ str(TreeParentParam)+ "'")
								if getpgname:
									sec_str += (
										"<td><input id='"
										+ str(current_obj_api_name)
										+ "' type='text' value='"
										+ str(getpgname.PAGE_NAME)
										+"' class='form-control related_popup_css' disabled>"
									)
								else:
									sec_str += (
										"<td><input id='"
										+ str(current_obj_api_name)
										+ "' type='text' value='"
										+ str(TreeParentParam)
										+"' class='form-control related_popup_css' disabled>"
									)
							elif current_obj_api_name == "PRIMARY_OBJECT_NAME" and str(ObjectName) == "SYSECT":
								TreeTopSuperParentParam = Product.GetGlobal("TreeParentLevel2")
								gettabname = Sql.GetFirst("SELECT OBJECT_APINAME FROM SYPAGE (NOLOCK) WHERE RECORD_ID = '"+str(new_value_dict['PAGE_RECORD_ID']+"'"))
								# gettabname = Sql.GetFirst("select PRIMARY_OBJECT_NAME from SYTABS where TAB_LABEL = '"+ str(TreeTopSuperParentParam)+ "'")
								if gettabname:
									sec_str += (
										"<td><input id='"
										+ str(current_obj_api_name)
										+ "' type='text' value='"
										+ str(gettabname.OBJECT_APINAME)
										+"' class='form-control related_popup_css' disabled>"
									)
								else:
									sec_str += (
										"<td><input id='"
										+ str(current_obj_api_name)
										+ "' type='text' value='"
										+ str(TreeParentParam)
										+"' class='form-control related_popup_css' disabled>"
									)
							else:
								# if str(current_obj_api_name) == "APROBJ_LABEL":
								#     record_value = ""
								if (
									parrent_object_name != record_value
									and current_obj_api_name in lookup_val
									and readonly != "readonly"
								):
									Trace.Write('cm to this if====')
									formula_disabled = "disabled"
									sec_str += (
										"<td><input id='"
										+ str(current_obj_api_name)
										+ "' type='text' value='"
										+ str(current_obj_value)
										+ "' class='form-control related_popup_css fltltlightyello'"
										+ " >"
									)
									if GettreeEnable is not None and str(GettreeEnable.ENABLE_TREE).upper() == "TRUE":
										cont_event_name = "cont_lookup_popup_new(this,'VIEW_DIV_ID')"
										sec_str += (
											'<input class="popup flt_lt" id="'
											+ str(parrent_object_name)
											+ '" data-target="#cont_viewModalSection" onclick="'
											+ cont_event_name
											+ '" type="image" data-toogle = "modal" src="../mt/default/images/customer_lookup.gif"></td>'
										)
									else:
										sec_str += (
											"<input class='popup flt_lt' id='"
											+ str(parrent_object_name)
											+ "' data-target='#cont_viewModalSection' onclick='cont_lookup_popup_new(this,"
											")' type='image'  src='../mt/default/images/customer_lookup.gif'></td>"
										)
								else:
									try:
										Trace.Write('cm to this else====')
										if current_obj_api_name in new_value_dict1:
											current_obj_value = new_value_dict1.get(str(current_obj_api_name))
											Trace.Write("--3742---current_obj_value--->" + str(current_obj_value))
									except:
										Trace.Write("Formula field is not in the main list")

									if readonly != "readonly":                                        
										sec_str += (
											"<td><input id='"
											+ str(current_obj_api_name)
											+ "' type='text' value='"
											+ str(current_obj_value)
											+ "' class='form-control related_popup_css flt_lt'></td>"
										)
									else:                                        
										sec_str += (
											"<td><input id='"
											+ str(current_obj_api_name)
											+ "' type='text' value='"
											+ str(current_obj_value)
											+ "' class='form-control related_popup_css flt_lt' disabled></td>"
										)

						elif data_type == "CHECKBOX" or formula_data_type == "CHECKBOX":
							#Trace.Write("cm to this elsee-----")
							current_val = new_value_dict1.get(str(current_obj_api_name))                          

							if str(current_val).upper() == "TRUE" :
								
								current_obj_value = "checked"
								
							

							elif str(current_obj_api_name) != "ACTIVE" and str(current_obj_api_name) != "ENABLE_SMARTAPPROVAL" and str(current_obj_api_name) != "REQUIRE_EXPLICIT_APPROVAL" and str(current_obj_api_name) != "UNANIMOUS_CONSENT":
								sec_str += (
									'<td><input id="'
									+ str(current_obj_api_name)
									+ '" value="'
									+ str(current_obj_value)
									+ '" '
									+ checked
									+ ' type="'
									+ str(data_type)
									+ '" class="custom" '
									+ disable
									+ ' ><span class="lbl"></span></td>'
								)
							checklist = ["ACTIVE","ENABLE_SMARTAPPROVAL","UNANIMOUS_CONSENT"]    
							if str(current_obj_api_name) in checklist:
								
								sec_str += (
									'<td><input checked id="'
									+ str(current_obj_api_name)
									+ '"  value="'
									+ str(current_obj_value)
									+ '" '
									+ checked
									+ ' type="'
									+ str(data_type)
									+ '" class="custom" onchange = "oncheckchange(this)"'
									+ disable
									+ ' ><span class="lbl"></span></td>'
								)
							if str(current_obj_api_name) == "REQUIRE_EXPLICIT_APPROVAL":
								
								sec_str += (
									'<td><input id="'
									+ str(current_obj_api_name)
									+ '"  value="'
									+ str(current_obj_value)
									+ '" '
									+ checked
									+ ' type="'
									+ str(data_type)
									+ '" class="custom" onchange = "oncheckchange(this)" '
									+ disable
									+ ' ><span class="lbl"></span></td>'
								)     
																							
						elif data_type == "DATE":
							date_field.append(current_obj_api_name)
							sec_str += (
								'<td class="wth324"><input id="'
								+ str(current_obj_api_name)
								+ '" value="'
								+ str(current_obj_value)
								+ '" type="text" class="form-control datePickerField wth155flrt" onclick="'
								+ str(datepicker)
								+ '" onchange="'
								+ str(datepicker_onchange)
								+ '"  '
								+ disable
								+ "></td>"
							)

						elif data_type == "PICKLIST":
							Trace.Write('4036---------')
							if ObjectName == "SYOBJD" or ObjectName == "ACACSA":
								sec_str += (
									'<td><select id="'
									+ str(current_obj_api_name)
									+ '" value="'
									+ str(current_obj_value)
									+ '" type="text" class="form-control pop_up_brd_rad related_popup_css hgt32fnt13 light_yellow" onchange = "onFieldChanges(this)" '
									+ disable
									+ " ><option value='Select'>..Select</option>"
								)
							else:
								sec_str += (
									'<td><select id="'
									+ str(current_obj_api_name)
									+ '" value="'
									+ str(current_obj_value)
									+ '" type="text" class="form-control pop_up_brd_rad related_popup_css hgt32fnt13 light_yellow" '
									+ disable
									+ " ><option value='Select'>..Select</option>"
								)
							Sql_Quality_Tier = Sql.GetFirst(
								"select PICKLIST_VALUES FROM  SYOBJD(NOLOCK) where OBJECT_NAME='"
								+ str(ObjectName)
								+ "' and DATA_TYPE='PICKLIST' and API_NAME = '"
								+ str(current_obj_api_name)
								+ "' "
							)
							Trace.Write('4063------')
							Tier_List1 = []
							Tier_List = (Sql_Quality_Tier.PICKLIST_VALUES).split(",")
							Tier_List1 = sorted(Tier_List)
							Trace.Write('4063--Tier_List1-----'+str(TabName))
							getlist = Sql.GetList("SELECT CpqTableEntryId FROM SAQTIP(NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND PARTY_ROLE != 'RECEIVING ACCOUNT'".format(contract_quote_record_id,quote_revision_record_id))
							if str(TabName) == "Quote":
								send_n_receive_acnt = Sql.GetList("SELECT PARTY_ROLE FROM SAQTIP(NOLOCK) WHERE QUOTE_RECORD_ID = '"+str(contract_quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"'")
								list_of_role = []
								if send_n_receive_acnt:
									for acnt in send_n_receive_acnt:
										list_of_role.append(acnt.PARTY_ROLE)
										if acnt.PARTY_ROLE == "SENDING ACCOUNT" or acnt.PARTY_ROLE == "RECEIVING ACCOUNT":
											Tier_List1.remove(acnt.PARTY_ROLE)
									# if "SENDING ACCOUNT" not in list_of_role and "RECEIVING ACCOUNT" not in list_of_role:
									# 	Tier_List1.remove("RECEIVING ACCOUNT")
							Trace.Write("CHKNG_J "+str(Tier_List1))
							for req1 in Tier_List1:
								sec_str += "<option>" + str(req1) + "</option>"
							sec_str += "</select></td>"
							
						elif data_type == "LONG TEXT AREA":
							sec_str += (
								'<td><textarea title="'
								+ str(current_obj_value)
								+ '" class="form-control related_popup_css txtArea light_yellow wid_90 " id="'
								+ str(current_obj_api_name)
								+ '" rows="1" cols="100" '
								+ disable
								+ ">"
								+ current_obj_value
								+ "</textarea></td>"
							)    

						else:
							
							sec_str += (
								'<td><input id="'
								+ str(current_obj_api_name)
								+ '" value="'
								+ str(current_obj_value)
								+ '" '
								+ str(keypressval)
								+ '  type="text" class="form-control related_popup_css" '
								+ disable
								+ " maxlength = '"+str(max_length)+"'></td>"
							)
						sec_str += (
							'<td id="'+str(current_obj_api_name)+'_err" class="err_msgs"></td><td class="float_r_bor_bot"><div class="col-md-12 editiconright"><a href="#" class="editclick">'
							+ str(edit_pencil_icon)
							+ "</a></div></td>"
						)
						sec_str += "</tr>"
			sec_str += "</table>"

			GettreeEnable = Sql.GetFirst("select ENABLE_TREE FROM SYTABS where SAPCPQ_ALTTAB_NAME='" + str(TabName) + "'")
			if GettreeEnable is not None and str(GettreeEnable.ENABLE_TREE).upper() == "TRUE":
				cancel_button = ""
				save_button = ""
				event_name = "loadRelatedList('" + str(popup_table_id) + "','" + str(DIVNAME) + "')"
				

				html_content = Sql.GetList("SELECT HTML_CONTENT,RELATED_LIST_RECORD_ID FROM SYPGAC (NOLOCK) WHERE RELATED_LIST_RECORD_ID = '"+str(popup_table_id)+"' AND TAB_NAME LIKE '%"+str(TabName)+"%'")
				if html_content:
					sec_str += (
							'<div class="row ma_text_align_sixteen">'
						)
					SaveCancel += ('<div id="HideSavecancel">')
					for btn in html_content:
						cancel_button = ""
						save_button = ""
						try:
							# if "CANCEL" in str(btn.HTML_CONTENT) and "SAVE" in str(btn.HTML_CONTENT):
							if "CANCEL" in str(btn.HTML_CONTENT):
								cancel_button = str(btn.HTML_CONTENT).format(event_name=event_name)
								sec_str += str(cancel_button)
								SaveCancel += str(cancel_button)
							if "SAVE" in str(btn.HTML_CONTENT):
								save_button = str(btn.HTML_CONTENT).format(ObjectName=ObjectName, func2=func2)
								sec_str += str(save_button)
								SaveCancel += str(save_button)
							# else:
							#     cancel_button = ""
							#     save_button = ""
						except:
							Trace.Write("Button Exceptions")
							cancel_button = ""
							save_button = ""

					SaveCancel += ("</div>")

					sec_str += "</div>"
				#Trace.Write("cancel__J "+str(cancel_button)+" save_J "+str(save_button))
	else:
		sec_str += '<div class="ma_text_align_sixteen">No matching records found </div><div class="modal-footer"><button type="button" class="btnstyle flt_rt" data-dismiss="modal">Close</button></div>'
	selected_program_list_preslect = []
	return (
		sec_str,
		new_value_dict,
		api_name,
		date_field,
		dbl_clk_function,
		filter_control_function,
		var_str,
		selected_offerings_list_preslect,
		selected_program_list_preslect,
		filter_tags,
		filter_types,
		filter_values,
		filter_drop_down,
		SaveCancel,
		table_header,
		pagedata,
		QryCount
	)


try:
	A_Keys = Param.A_Keys
	A_Values = Param.A_Values
except:
	A_Keys = ""
	A_Values = ""

Trace.Write("SORT A_Keys-----"+str(list(A_Keys)))
Trace.Write("SORT A_Values -----"+str(list(A_Values)))

try:
	DIVNAME = Param.DIVNAME
except:
	DIVNAME = ""

TABLEID = Param.TABLEID
OPER = Param.OPER

offset_list = []

for val in Param:
	offset_list.append(val.Key)
if "Offset_Skip_Count" in offset_list:
	Offset_Skip_Count = Param.Offset_Skip_Count
else:
	Offset_Skip_Count = 1
if "Fetch_Count" in offset_list:
	Fetch_Count = Param.Fetch_Count
else:
	Fetch_Count = 10

selected_country_list = []
if "selected_program_list" in offset_list:
	selected_program_list = Param.selected_program_list
else:
	selected_program_list = []

if "selected_app_list" in offset_list:
	selected_app_list = Param.selected_app_list
else:
	selected_app_list = []

RECORDID = Param.RECORDID
try:
	RECORDFEILD = Param.RECORDFEILD
	Trace.Write("RECORDFEILD==="+str(RECORDFEILD))
except:
	RECORDFEILD = ""
try:
	AwdRecordID = Param.AwdRecordID
except:
	AwdRecordID = ""
NEWVALUE = Param.NEWVALUE
Trace.Write("NEWVALUE -----"+str(NEWVALUE))
LOOKUPOBJ = Param.LOOKUPOBJ
LOOKUPAPI = Param.LOOKUPAPI
try:
	TreeParentParam = Param.TreeParentParam
except:
	TreeParentParam = ""

try:
	SortColumn = Param.SortColumn
	SortColumnOrder = Param.SortColumnOrder    
	Trace.Write("SORT COLUMN-----"+str(SortColumn))
	Trace.Write("SORT COLUMN ORDER -----"+str(SortColumnOrder))
	
except:
	SortColumn = ''
	SortColumnOrder = ''    
	Trace.Write("SORT EMPTY")

try:    
	PerPage = Param.PerPage
	PageInform = Param.PageInform    
	
except:    
	PerPage = ''
	PageInform = ''

try:
	ACTION = Param.ACTION
except:
	ACTION = ''
Trace.Write("ACTION==="+str(ACTION))


Trace.Write("PerPage-----"+str(PerPage))
Trace.Write("PageInform -----"+str(PageInform))

if LOOKUPOBJ is not None and LOOKUPOBJ != "":
	LOOKUPOBJ = LOOKUPOBJ.split("_")[1]
ApiResponse = ApiResponseFactory.JsonResponse(
	POPUPLISTVALUEADDNEW(
		TABLEID,
		RECORDID,
		RECORDFEILD,
		NEWVALUE,
		LOOKUPOBJ,
		LOOKUPAPI,
		OPER,
		A_Keys,
		A_Values,
		selected_country_list,
		selected_program_list,
		DIVNAME,
		AwdRecordID,
		TreeParentParam,
		PerPage,
		PageInform     
	)
)
